# =====================================================================
#  OLCUM — Çöl Yolu sisteminin ÖLÇÜM ve KARAR modülü (tek parça)     2026-09-24 (v1.1: _olc_bant/_olc_bek, COL_v1 _bant çatışması giderildi)
#
#  Yerini aldığı dosyalar: REJIM_TEST.py, PORTFOY_v2.py, KARAR.py, TEKRAR.py, ZAMAN.py
#  (V3_TESHIS.py: sorusu cevaplandı, yöntemi eskidi — emekli.)
#
#  DENETİMDE BULUNAN VE BURADA GİDERİLEN KUSURLAR
#   K1  Rejim serisi: SMA ısınma günleri (ilk N gün, SMA=NaN) "NOTR" etiketleniyordu.
#       xu 2024 başında başlıyorsa 2024'ün çoğu sahte NÖTR olmuş, "NÖTR bek +17.3"
#       bulgusu rejim değil takvim olabilir.  -> Isınma günleri 'YOK' etiketi, rejim
#       analizinden DIŞLANIR ve sayısı raporlanır.
#   K2  Rejim mantığı 4 dosyada 4 kopya, etiketleme 3 kopya (O(n·m) döngü).
#       -> Tek uygulama, searchsorted ile vektörel.
#   K3  "BOĞA alfa" mutlak ölçülüyordu (BOĞA>0 mu?). Asıl soru göreli: BOĞA'da
#       endeks üstü, diğer rejimlerden DÜŞÜK mü?  -> Eşli fark olarak ölçülür.
#   K4  Tekrar testi BIST 2024-26 ile ABD 2024-26'yı bağımsız sayıyordu; aynı
#       takvim penceresi.  -> Takvim örtüşmesi otomatik tespit edilir, örtüşen
#       setler tek kanıt sayılır, hüküm buna göre düşürülür.
#   K5  Çoklu karşılaştırma: ~7 özellik × %90 bant → koşu başına ~0.7 sahte
#       "gerçek" beklenir.  -> Beklenen sahte sayısı her taramada yazılır.
#   K6  Portföy-eşikli hükümler (±3 puan, 2σ) — bandı 110 puan olan bir ölçüde
#       anlamsız.  -> Portföy yalnız BANT ve EŞLİ+PLASEBO ile raporlanır; hüküm
#       mercii işlem başı ölçülerdir.
#   K7  "teorik kapasite = 100/poz" yanıltıcı (poz cari özsermayenin %'si).
#       -> Kaldırıldı; gözlenen açık pozisyon sayısı raporlanır.
#   K8  Sonuç sütunları (bar, hedef, getiri…) özellik taramasına sızabiliyordu.
#       -> Kara liste + uyarı.
#
#  SAĞLAM BULUNAN VE KORUNANLAR
#   • sim() ↔ portfoy() birebir denklik (5 metrik, 1e-6)  • gün-bloklu bootstrap
#   • eşli kıyas + plasebo                                • içsel/takvim ayrımı
#     (sentetik kontrol: sahte takvim → TAKVİM, gerçek sinyal → İÇSEL %98)
#
#  MİMARİ
#   0 cfg / yardımcılar     3 işlem başı: olculer · bootstrap · kiyas · dilim · tarama
#   1 rejim (tek kaynak)    4 zaman süzgeci: donem_ici · icsel_dis
#   2 portföy motoru:       5 tekrar: çok set + takvim örtüşmesi
#     yol_kur · sim · bant  6 orkestra: olcum(t,OB,xu) · tekrar(setler)
#     esli_kiyas · kapasite · sira_kiyas
#
#  Ana sisteme HİÇBİR ŞEY yazmaz. portfoy()/islemler() değişmez.
#
#  KULLANIM (BASLAT sonrası, Colab):
#     exec(open(f'{K}/OLCUM.py').read())
#     t = islemler(OB24, 'acilis', tekil=True, xu=xu)
#     R = olcum(t, OB24, xu, ad='BIST 2024-26')          # tam rapor
#     T = tekrar([('BIST 2024-26',OB24,xu), ('BIST 2023',OB23,xu), ('ABD 2024-26',OBUS,None)])
#     dilim(t,'cds_pct') · kiyas(t, maske,'A','B') · icsel_dis(t,'cds_pct') · bant(t,OB,xu)
# =====================================================================
from __future__ import annotations
import os, logging, traceback, warnings
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
import pandas as pd

# --- ÇAKIŞMA KAPISI (yükleme başı): bellekteki adların kimlikleri ---------------------------------
_CK_ONCE = {k: id(v) for k, v in globals().items()}


warnings.filterwarnings('ignore', message='All-NaN slice encountered')
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')

olog = logging.getLogger('col.olcum')
if not olog.handlers:
    _h = logging.StreamHandler(); _h.setFormatter(logging.Formatter('[%(levelname)s] %(name)s: %(message)s'))
    olog.addHandler(_h); olog.setLevel(logging.INFO)


# =====================================================================
# 0) CFG / YARDIMCILAR
# =====================================================================
@dataclass
class OlcumCfg:
    # portföy motoru
    maliyet: float = 0.4
    maks_toplam: float = 100.0
    mevduat_yillik: float = 45.0
    port_tekrar: int = 40          # portföy bootstrap örnek sayısı
    port_at: float = 0.05          # her örnekte atılan işlem oranı
    # işlem başı bootstrap
    boot_tekrar: int = 1000
    guven_alt: float = 5.0         # %90 bant: [5, 95]
    guven_ust: float = 95.0
    min_islem: int = 30
    n_dilim: int = 4
    # rejim
    rejim_smalar: tuple = (150, 200)
    egim_bar: int = 20
    # zaman süzgeci
    n_donem: int = 3
    n_donem_ic: int = 6
    # ortak
    tohum: int = 20260923
    # sinyal anında bilinen özellikler / sonuç sütunları
    ozellikler: tuple = ('doji', 'alt_fitil', 'dar', 'gecerli', 'cds_pct', 'borc_oz', 'poz')
    sonuc_kolonlari: tuple = ('bar', 'getiri', 'endeks', 'hedef', 'cikis', 'cikis_t', 'jt', 'tekrar')

ocfg = OlcumCfg()


def _olc_g(ad, vars_=None):
    return globals().get(ad, vars_)

def _olc_K():
    return _olc_g('K', '/content/drive/MyDrive/col_tarayici')

def _rng(ek: int = 0):
    return np.random.default_rng(ocfg.tohum + int(ek))

def _olc_bek(v) -> float:
    """Beklenti = p·ort_kazanç + (1−p)·ort_kayıp. Ana sistemin bek() varsa o kullanılır."""
    f = _olc_g('bek')
    if f is not None:
        try:
            r = float(f(v))
            if np.isfinite(r): return r
        except Exception:
            pass
    v = pd.Series(v).dropna().astype(float)
    if not len(v): return np.nan
    k = v[v > 0]; z = v[v <= 0]; p = len(k) / len(v)
    return p * (k.mean() if len(k) else 0.0) + (1 - p) * (z.mean() if len(z) else 0.0)

def _olc_bant(V, anahtarlar=None) -> dict:
    """[{k:v}] listesinden her k için (medyan, p_alt, p_üst)."""
    if not V: return {}
    df = pd.DataFrame(V)
    anahtarlar = anahtarlar or list(df.columns)
    out = {}
    for k in anahtarlar:
        if k not in df: continue
        s = pd.to_numeric(df[k], errors='coerce')
        if s.notna().sum() == 0: continue
        out[k] = (float(np.nanmedian(s)), float(np.nanpercentile(s, ocfg.guven_alt)),
                  float(np.nanpercentile(s, ocfg.guven_ust)))
    return out

def _gercek(b3) -> bool:
    """(medyan, lo, hi) bandı sıfırı kapsamıyor mu?"""
    if not b3: return False
    _, lo, hi = b3
    return bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0))

def _f(x, fmt='+.1f'):
    try:
        return format(float(x), fmt) if np.isfinite(float(x)) else 'nan'
    except Exception:
        return 'nan'

def _kaydet(df: pd.DataFrame, ad: str):
    try:
        yol = os.path.join(_olc_K(), ad)
        df.to_csv(yol, index=False); print(f"-> {yol}")
    except Exception as e:
        olog.warning(f'kayıt {ad}: {e}')

def _gerekli_kolonlar(t, *kols):
    eksik = [k for k in kols if k not in t.columns]
    if eksik:
        raise ValueError(f'işlem tablosunda eksik sütun: {eksik}')


# =====================================================================
# 1) REJİM — tek kaynak  (K1, K2)
# =====================================================================
REJIMLER = ('BOGA', 'NOTR', 'AYI')

def rejim_serisi(xu: pd.DataFrame, sma: int = 200, egim_bar: Optional[int] = None,
                 egim_kullan: bool = True) -> pd.Series:
    """XU100 günlük rejim.  BOGA: kapanış>SMA (ve SMA eğimi>0)  AYI: kapanış<SMA
    NOTR: arada.  YOK: SMA henüz hesaplanamıyor (ısınma) — analizden DIŞLANIR."""
    egim_bar = ocfg.egim_bar if egim_bar is None else egim_bar
    c = xu['Close'].astype(float)
    s = c.rolling(sma).mean()
    r = pd.Series('NOTR', index=c.index, dtype=object)
    if egim_kullan:
        eg = s / s.shift(egim_bar) - 1
        r[(c > s) & (eg > 0)] = 'BOGA'
        bilinmiyor = s.isna() | eg.isna()
    else:
        r[c > s] = 'BOGA'
        bilinmiyor = s.isna()
    r[c < s] = 'AYI'
    r[bilinmiyor] = 'YOK'
    return r

def rejim_etiketle(t: pd.DataFrame, rj: pd.Series) -> pd.Series:
    """Her işlemin giriş günündeki (veya öncesindeki son) rejimi — vektörel."""
    gt = pd.to_datetime(t['giris_t']).values
    idx = rj.index.values
    pos = np.searchsorted(idx, gt, side='right') - 1
    lab = np.where(pos >= 0, rj.values[np.clip(pos, 0, len(rj) - 1)], 'YOK')
    return pd.Series(lab, index=t.index, dtype=object)

def rejim_tablo(t, xu, sma=200):
    """Rejim etiketi + ısınma sayısı. -> (etiket Series, n_yok)"""
    lab = rejim_etiketle(t, rejim_serisi(xu, sma=sma))
    return lab, int((lab == 'YOK').sum())


# =====================================================================
# 2) PORTFÖY MOTORU  (sim ↔ portfoy birebir; K6, K7)
# =====================================================================
def yol_kur(t: pd.DataFrame, OB, maliyet: Optional[float] = None):
    """Normalize günlük yolları BİR KEZ kurar.
    -> (G: ortak gün indeksi, Y: {islem_idx: (p0, p1, arr)}); arr[k−p0] = değer çarpanı."""
    maliyet = ocfg.maliyet if maliyet is None else maliyet
    if t is None or t.empty:
        return pd.DatetimeIndex([]), {}
    _gerekli_kolonlar(t, 'i', 'kb', 'jt', 'giris', 'cikis')
    ham, gunler = {}, set()
    for r in t.itertuples():
        try:
            o = OB[r.i]
            iT = pd.to_datetime(o['iT']); C = np.asarray(o['iC'], dtype=float)
            sl = slice(int(r.kb), int(r.jt) + 1)
            idx = iT[sl]; v = C[sl].astype(float).copy()
            if len(v) < 1 or not np.isfinite(r.giris) or r.giris <= 0:
                continue
            v[0] = float(r.giris)
            v[-1] = float(r.cikis) * (1 - maliyet / 100)
            ham[r.Index] = (idx, v / float(r.giris)); gunler.update(idx)
        except Exception as e:
            olog.debug(f'yol_kur[{getattr(r, "Index", "?")}]: {e}')
    if not ham:
        return pd.DatetimeIndex([]), {}
    G = pd.DatetimeIndex(sorted(gunler)); yer = {d: k for k, d in enumerate(G)}
    Y = {}
    for k, (idx, v) in ham.items():
        p0, p1 = yer[idx[0]], yer[idx[-1]]
        arr = np.full(p1 - p0 + 1, np.nan)
        arr[[yer[d] - p0 for d in idx]] = v
        m = np.isnan(arr)
        if m.any():                                   # ileri doldur (portfoy() .loc[:g] ile aynı)
            ind = np.where(~m, np.arange(len(arr)), 0); np.maximum.accumulate(ind, out=ind); arr = arr[ind]
        if np.isnan(arr[0]): continue
        Y[k] = (p0, p1, arr)
    return G, Y


def sim(t, G, Y, sira='zaman', rng=None, xu=None, egri=False) -> Optional[dict]:
    """Sermaye 100, ağırlık = t.poz (%), toplam açık ağırlık ≤ maks_toplam, nakit yoksa atla.
    sira: 'zaman' (geliş sırası = portfoy() davranışı) | 'poz' (gün içinde en iyi önce) | 'rastgele'."""
    if t is None or t.empty or not len(G): return None
    ix = [i for i in t.index if i in Y]
    if len(ix) < 2: return None
    pozs = pd.to_numeric(t['poz'], errors='coerce').to_dict()
    giren = {}
    for i in ix: giren.setdefault(Y[i][0], []).append(i)
    if sira == 'poz':
        for k in giren: giren[k].sort(key=lambda i: -float(pozs.get(i) if np.isfinite(pozs.get(i, np.nan)) else 0))
    elif sira == 'rastgele':
        rng = rng if rng is not None else _rng()
        for k in giren: rng.shuffle(giren[k])

    nakit, acik, atl, alin = 100.0, {}, 0, 0
    n = len(G); E = np.empty(n); NK = np.empty(n); AC = np.empty(n)
    for k in range(n):
        acik_deger = 0.0
        for i, lot in acik.items():
            p0, _, arr = Y[i]; acik_deger += lot * arr[k - p0]
        for i in giren.get(k, ()):
            E_simdi = nakit + acik_deger
            w = pozs.get(i, np.nan)
            if not np.isfinite(w) or w <= 0: atl += 1; continue
            tutar = E_simdi * w / 100
            agir = acik_deger / max(E_simdi, 1e-9) * 100
            if tutar > nakit or agir + w > ocfg.maks_toplam + 1e-9: atl += 1; continue
            nakit -= tutar; acik[i] = tutar; acik_deger += tutar; alin += 1
        deger = 0.0
        for i in list(acik):
            p0, p1, arr = Y[i]; lot = acik[i]
            if k >= p1: nakit += lot * arr[-1]; del acik[i]
            else: deger += lot * arr[k - p0]
        E[k] = nakit + deger; NK[k] = nakit; AC[k] = len(acik)

    eq = pd.Series(E, index=G)
    if len(eq) < 2 or not np.isfinite(eq.iloc[-1]): return None
    dd = (eq / eq.cummax() - 1) * 100
    yil = max((G[-1] - G[0]).days / 365.25, 1 / 365)
    r = {'toplam': float(eq.iloc[-1] - 100),
         'yillik': float(((eq.iloc[-1] / 100) ** (1 / yil) - 1) * 100),
         'max_dd': float(dd.min()), 'yil': yil, 'alinan': alin, 'atlanan': atl,
         'atil_nakit%': float(np.mean(NK / np.maximum(E, 1e-9)) * 100),
         'acik_ort': float(AC.mean()), 'acik_maks': float(AC.max()),
         'mevduat': float(((1 + ocfg.mevduat_yillik / 100) ** yil - 1) * 100)}
    f = _olc_g('_endeks_getiri')
    r['xu'] = float(f(xu, G[0], G[-1])) if (f is not None and xu is not None) else np.nan
    if egri: r['egri'] = eq
    return r


def _port_bant(V, ad=''):
    v = np.asarray([x for x in V if x is not None and np.isfinite(x)], dtype=float)
    if not len(v): return {}
    return {'ad': ad, 'n': len(v), 'medyan': float(np.median(v)), 'ort': float(v.mean()),
            'std': float(v.std(ddof=1)) if len(v) > 1 else 0.0,
            'p5': float(np.percentile(v, ocfg.guven_alt)), 'p95': float(np.percentile(v, ocfg.guven_ust))}


def bant(t, OB=None, xu=None, G=None, Y=None, sira='zaman', n=None, at=None, ad='', yaz=True) -> dict:
    """Portföy DAĞILIMI: işlemlerin %at'i rastgele atılarak n simülasyon."""
    n = ocfg.port_tekrar if n is None else n; at = ocfg.port_at if at is None else at
    if G is None or Y is None: G, Y = yol_kur(t, OB)
    rng = _rng(); V = []
    for b in range(n):
        tut = rng.random(len(t)) >= at
        p = sim(t[tut], G, Y, sira=sira, rng=_rng(b + 1), xu=xu)
        if p: V.append(p['toplam'])
    r = _port_bant(V, ad)
    if yaz and r:
        print(f"  {ad:26s} medyan {r['medyan']:+6.0f}%  [%5 {r['p5']:+.0f} .. %95 {r['p95']:+.0f}]  std {r['std']:.1f}")
    return r


def esli_kiyas(t, maske, G, Y, xu=None, sira='zaman', n=None, at=None,
               ad_a='A hepsi', ad_b='B filtreli', plasebo=True, yaz=True) -> dict:
    """PAIRED BOOTSTRAP + PLASEBO.  Aynı rastgele bozulma iki kümeye de uygulanır;
    plasebo = aynı SAYIDA işlemi rastgele eleyen kontrol (işlem sayısını azaltan her
    filtre sermaye kullanımını düşürüp portföyü kendiliğinden aşağı çeker)."""
    n = ocfg.port_tekrar if n is None else n; at = ocfg.port_at if at is None else at
    if t is None or t.empty: return {}
    maske = pd.Series(np.asarray(maske, dtype=bool), index=t.index)
    rng = _rng(7); A, B, P, D, DP, KA, KB = [], [], [], [], [], [], []
    for b in range(n):
        tut = pd.Series(rng.random(len(t)) >= at, index=t.index)
        alt = t[tut]; mb = maske[tut]
        pa = sim(alt, G, Y, sira=sira, rng=_rng(b + 1), xu=xu)
        pb = sim(alt[mb], G, Y, sira=sira, rng=_rng(b + 1), xu=xu)
        pp = None
        if plasebo and mb.sum() > 0:
            sec = rng.permutation(alt.index)[:int(mb.sum())]
            pp = sim(alt.loc[sorted(sec)], G, Y, sira=sira, rng=_rng(b + 1), xu=xu)
        if pa and pb:
            A.append(pa['toplam']); B.append(pb['toplam']); D.append(pb['toplam'] - pa['toplam'])
            KA.append(pa['alinan']); KB.append(pb['alinan'])
            if pp: P.append(pp['toplam']); DP.append(pb['toplam'] - pp['toplam'])
    if not D: return {}
    d = np.asarray(D, float)
    r = {'a': _port_bant(A, ad_a), 'b': _port_bant(B, ad_b), 'n': len(d),
         'alinan_a': float(np.mean(KA)), 'alinan_b': float(np.mean(KB)),
         'fark': (float(np.median(d)), float(np.percentile(d, ocfg.guven_alt)), float(np.percentile(d, ocfg.guven_ust)))}
    if DP:
        dp = np.asarray(DP, float)
        r['plasebo'] = _port_bant(P, 'plasebo')
        r['net'] = (float(np.median(dp)), float(np.percentile(dp, ocfg.guven_alt)), float(np.percentile(dp, ocfg.guven_ust)))
        r['net_gercek'] = bool(r['net'][1] > 0)
    if yaz:
        m, lo, hi = r['fark']
        print(f"    {ad_a:22s} medyan {r['a']['medyan']:+6.0f}%  (alınan ~{r['alinan_a']:.0f})")
        print(f"    {ad_b:22s} medyan {r['b']['medyan']:+6.0f}%  (alınan ~{r['alinan_b']:.0f})")
        print(f"    ham FARK  medyan {m:+6.1f}  [{lo:+.1f}, {hi:+.1f}]  -> "
              + ('bant sıfırın ' + ('ÜSTÜNDE' if m > 0 else 'ALTINDA') if _gercek(r['fark']) else 'sıfırı kapsıyor (GÜRÜLTÜ)'))
        if 'net' in r:
            nm, nlo, nhi = r['net']
            print(f"    {'plasebo (rastgele)':22s} medyan {r['plasebo']['medyan']:+6.0f}%")
            print(f"    NET (filtre−plasebo) {nm:+6.1f}  [{nlo:+.1f}, {nhi:+.1f}]  ->  "
                  f"{'GERÇEK KATKI' if r['net_gercek'] else 'KATKI YOK'}")
    return r


def kapasite(t, G, Y, xu=None, ad='') -> dict:
    """Kaç sinyal, kaçı alındı, atıl nakit, açık pozisyon (K7: teorik kapasite kaldırıldı)."""
    print(f"\n===== KAPASİTE [{ad}] =====")
    p = sim(t, G, Y, sira='zaman', xu=xu)
    if not p: print('  simülasyon yok'); return {}
    gun = t.groupby(pd.to_datetime(t['giris_t']).dt.date).size()
    print(f"  sinyal {len(t):5d} | ALINAN {p['alinan']:4d} (%{100*p['alinan']/max(len(t),1):.0f})  "
          f"ATLANAN {p['atlanan']:5d} (%{100*p['atlanan']/max(len(t),1):.0f})")
    print(f"  açık pozisyon: ort {p['acik_ort']:.1f}, maks {p['acik_maks']:.0f} | atıl nakit ort %{p['atil_nakit%']:.0f}")
    print(f"  günlük sinyal: medyan {gun.median():.0f}, %90 dilim {gun.quantile(.9):.0f}, maks {gun.max():.0f}")
    if p['alinan'] / max(len(t), 1) < 0.35:
        print("  UYARI: sinyallerin çoğu paraya yetişmiyor -> tek portföy sayısı kaliteyi değil geliş sırasını ölçer.")
    return p


def sira_kiyas(t, G, Y, xu=None, ad='', n=None) -> dict:
    print(f"\n===== SIRA KURALI [{ad}] — {n or ocfg.port_tekrar} örnekli bant =====")
    R = {s: bant(t, G=G, Y=Y, xu=xu, sira=s, n=n, ad=et)
         for s, et in (('zaman', 'zaman (mevcut)'), ('poz', 'poz (en iyi önce)'), ('rastgele', 'rastgele (kontrol)'))}
    z, p, q = R.get('zaman', {}), R.get('poz', {}), R.get('rastgele', {})
    if z and p and q:
        ust = p['medyan'] - q['medyan']
        print(f"  poz−rastgele {ust:+.0f} | zaman−rastgele {z['medyan']-q['medyan']:+.0f}  (std ~{q['std']:.0f})")
        print("  HÜKÜM: " + ('sıralama anlamlı katkı veriyor' if ust > max(5.0, 0.5 * q['std'])
                              else 'sıralama fark yaratmıyor; darboğaz sermaye, seçim değil'))
    return R


# =====================================================================
# 3) İŞLEM BAŞI ÖLÇÜLER  (karar mercii)
# =====================================================================
def olculer(t) -> dict:
    if t is None or not len(t): return {'n': 0}
    v = pd.to_numeric(t['getiri'], errors='coerce')
    e = pd.to_numeric(t['endeks'], errors='coerce') if 'endeks' in t else pd.Series(np.nan, index=t.index)
    f = (v - e).dropna()
    return {'n': int(len(v)), 'bek': _olc_bek(v), 'kazanan%': float(100 * (v > 0).mean()),
            'ort': float(v.mean()), 'medyan': float(v.median()), 'agir%': float(100 * (v < -20).mean()),
            'endeks_ustu': float(f.mean()) if len(f) else np.nan,
            'bar': float(pd.to_numeric(t['bar'], errors='coerce').median()) if 'bar' in t else np.nan}

OLCU_ANAHTAR = ('bek', 'kazanan%', 'ort', 'agir%', 'endeks_ustu')

def _gun_gruplari(t):
    g = pd.to_datetime(t['giris_t']).dt.normalize().values
    gruplar = {}
    for pos, k in enumerate(g): gruplar.setdefault(k, []).append(pos)
    return np.array(list(gruplar.keys())), {k: np.asarray(v) for k, v in gruplar.items()}

def bootstrap(t, maske=None, n=None, tohum_ek=0) -> dict:
    """GÜN BLOKLU yeniden örnekleme (aynı gün açılan işlemler birlikte hareket eder).
    maske verilirse A=~maske, B=maske ve FARK(B−A) dağılımı da döner (eşli)."""
    n = ocfg.boot_tekrar if n is None else n
    if t is None or len(t) < 5: return {}
    anahtar, gruplar = _gun_gruplari(t)
    rng = _rng(tohum_ek)
    m = None if maske is None else np.asarray(pd.Series(maske).values, dtype=bool)
    A, B, D = [], [], []
    for _ in range(n):
        sec = rng.choice(len(anahtar), size=len(anahtar), replace=True)
        pos = np.concatenate([gruplar[anahtar[s]] for s in sec])
        alt = t.iloc[pos]
        if m is None:
            A.append(olculer(alt)); continue
        mm = m[pos]
        a, b = olculer(alt[~mm]), olculer(alt[mm])
        if a.get('n', 0) >= 5 and b.get('n', 0) >= 5:
            A.append(a); B.append(b)
            D.append({k: b.get(k, np.nan) - a.get(k, np.nan) for k in OLCU_ANAHTAR})
    r = {'a': _olc_bant(A, OLCU_ANAHTAR)}
    if m is not None: r['b'] = _olc_bant(B, OLCU_ANAHTAR); r['fark'] = _olc_bant(D, OLCU_ANAHTAR)
    return r

def _yaz_olcu(ad, o):
    print(f"    {ad:24s} n={o['n']:5d}  bek {_f(o['bek'])}  kazanan %{_f(o['kazanan%'], '.0f')}  "
          f"endeks üstü {_f(o['endeks_ustu'])}  ağır %{_f(o['agir%'], '.0f')}")

def _yaz_fark(ad, fb, anahtarlar=('bek', 'kazanan%', 'endeks_ustu', 'agir%')):
    if not fb: return
    print(f"    {ad:24s} " + '  '.join(f"{k} {m:+.1f} [{lo:+.1f},{hi:+.1f}]" for k, (m, lo, hi) in
                                        ((k, fb[k]) for k in anahtarlar if k in fb)))


def kiyas(t, maske, ad_a='A', ad_b='B', n=None, yaz=True) -> dict:
    """İki dilimi eşli (aynı gün örneği) karşılaştır. maske=True olanlar B."""
    if t is None or t.empty: return {}
    m = pd.Series(np.asarray(maske, dtype=bool), index=t.index)
    oa, ob = olculer(t[~m]), olculer(t[m])
    if min(oa.get('n', 0), ob.get('n', 0)) < ocfg.min_islem:
        if yaz: print(f"    {ad_b}: dilim küçük (n={ob.get('n',0)}) — yorum yok")
        return {'olcu_a': oa, 'olcu_b': ob, 'yetersiz': True}
    r = bootstrap(t, maske=m.values, n=n); fb = r.get('fark', {})
    r.update({'olcu_a': oa, 'olcu_b': ob, 'bek_gercek': _gercek(fb.get('bek')),
              'eu_gercek': _gercek(fb.get('endeks_ustu'))})
    if yaz:
        _yaz_olcu(ad_a, oa); _yaz_olcu(ad_b, ob); _yaz_fark('FARK (B−A)', fb)
        if 'bek' in fb:
            m_, lo, hi = fb['bek']
            print("    -> " + ('B GERÇEKTEN daha iyi' if lo > 0 else 'B GERÇEKTEN daha kötü' if hi < 0
                               else 'FARK YOK (bant sıfırı kapsıyor)'))
    return r


def dilim(t, kolon, n_dilim=None, n=None, yaz=True) -> pd.DataFrame:
    """Sayısal özelliği çeyreklere böl; üst−alt çeyrek bek farkı bandı -> ayırt ediyor mu?"""
    n_dilim = ocfg.n_dilim if n_dilim is None else n_dilim
    bos = pd.DataFrame()
    if t is None or t.empty or kolon not in t:
        if yaz: print(f"  {kolon}: sütun yok"); return bos
    if kolon in ocfg.sonuc_kolonlari:
        if yaz: print(f"  {kolon}: SONUÇ sütunu — sinyal anında bilinmez, filtre kurulamaz (geleceğe bakma)")
        return bos
    s = pd.to_numeric(t[kolon], errors='coerce'); ok = s.notna()
    if ok.sum() < ocfg.min_islem * n_dilim:
        if yaz: print(f"  {kolon:12s} yetersiz veri (geçerli {int(ok.sum())}/{len(t)})"); return bos
    tt = t[ok].copy(); ss = s[ok]
    try:
        tt['_d'] = pd.qcut(ss, n_dilim, labels=False, duplicates='drop')
    except Exception as e:
        if yaz: print(f"  {kolon}: dilimlenemedi ({e})"); return bos
    S = []
    for d in sorted(tt['_d'].dropna().unique()):
        kes = tt[tt['_d'] == d]; o = olculer(kes); sv = ss[tt['_d'] == d]
        S.append({'kolon': kolon, 'dilim': int(d) + 1, 'aralik': f"{sv.min():.3g}..{sv.max():.3g}",
                  **{k: o[k] for k in ('n', 'bek', 'kazanan%', 'endeks_ustu', 'agir%')}})
    d_ = pd.DataFrame(S)
    if d_.empty: return d_
    ust = tt['_d'] == tt['_d'].max(); alt_ = tt['_d'] == tt['_d'].min()
    ikili = tt[ust | alt_]
    r = bootstrap(ikili, maske=ust[ust | alt_].values, n=n)
    fb = (r.get('fark') or {}).get('bek')
    if fb: d_.attrs['fark_bek'] = fb; d_.attrs['gercek'] = _gercek(fb)
    if yaz:
        print(f"\n  --- {kolon} ---"); print(d_.round(2).to_string(index=False))
        if fb:
            m, lo, hi = fb
            print(f"    üst − alt çeyrek bek: {m:+.1f} [{lo:+.1f}, {hi:+.1f}]  -> "
                  f"{'AYIRT EDİYOR' if _gercek(fb) else 'ayırt etmiyor'}")
    return d_


def tarama(t, kolonlar=None, n=None, yaz=True) -> pd.DataFrame:
    """Sinyal anında bilinen özellikleri tara (K5: beklenen sahte sayısı yazılır; K8: sonuç sütunları dışlanır)."""
    kolonlar = list(kolonlar or [k for k in ocfg.ozellikler if k in t.columns])
    sizan = [k for k in kolonlar if k in ocfg.sonuc_kolonlari]
    if sizan:
        print(f"  [UYARI] sonuç sütunu atlandı (geleceğe bakma): {', '.join(sizan)}")
        kolonlar = [k for k in kolonlar if k not in sizan]
    print(f"\n===== ÖZELLİK TARAMASI — hangi ölçü gerçekten ayırt ediyor? =====")
    S = []
    for k in kolonlar:
        try:
            d_ = dilim(t, k, n=n, yaz=yaz)
            if d_.empty or 'fark_bek' not in d_.attrs: continue
            m, lo, hi = d_.attrs['fark_bek']
            S.append({'ozellik': k, 'ust-alt_bek': m, 'p5': lo, 'p95': hi,
                      'gercek': bool(d_.attrs.get('gercek', False)), 'yon': 'yüksek iyi' if m > 0 else 'düşük iyi'})
        except Exception as e:
            olog.warning(f'tarama[{k}]: {e}')
    r = pd.DataFrame(S)
    if r.empty: print('  sonuç yok'); return r
    r = r.reindex(r['ust-alt_bek'].abs().sort_values(ascending=False).index)
    print(f"\n  --- SIRALAMA (ayırt edicilik) ---"); print(r.round(2).to_string(index=False))
    sahte = len(r) * (1 - (ocfg.guven_ust - ocfg.guven_alt) / 100)
    ger = r[r['gercek']]
    print(f"\n  {len(r)} özellik %{ocfg.guven_ust-ocfg.guven_alt:.0f} bantla test edildi -> "
          f"sırf şansla ~{sahte:.1f} 'gerçek' beklenir. Bulunan: {len(ger)}.")
    if len(ger):
        print(f"  GERÇEKTEN ayırt eden (bu sette): {', '.join(ger['ozellik'])}")
        print("  -> Tekrar testinden (başka dönem/piyasa) ve zaman süzgecinden geçmeden kural yapılmaz.")
    else:
        print("  HİÇBİRİ ayırt etmiyor: kazanç formasyonun kendisinden geliyor, ölçülerden değil.")
    return r


def rejim_dilim(t, xu, smalar=None, n=None, yaz=True) -> pd.DataFrame:
    """Rejim dilimlerinin işlem başı ölçüleri; AYI vs dışı ve BOĞA vs dışı EŞLİ fark (K1, K3)."""
    smalar = smalar or ocfg.rejim_smalar
    print(f"\n===== REJİM DİLİMİ — alfa hangi rejimde üretiliyor? =====")
    if xu is None: print('  xu yok'); return pd.DataFrame()
    S = []
    for sma in smalar:
        lab, n_yok = rejim_tablo(t, xu, sma=sma)
        if n_yok:
            print(f"\n  SMA{sma}: {n_yok} işlem SMA ısınma döneminde (rejim bilinmiyor) -> DIŞLANDI")
        tk = t[lab != 'YOK']; lk = lab[lab != 'YOK']
        if len(tk) < ocfg.min_islem * 2:
            print(f"  SMA{sma}: yetersiz işlem ({len(tk)})"); continue
        print(f"\n  --- SMA{sma} (n={len(tk)}) ---")
        for r_ in REJIMLER:
            o = olculer(tk[lk == r_])
            if o.get('n', 0): _yaz_olcu(f"{r_:5s}", o)
        satir = {'sma': sma, 'n': len(tk), 'n_yok': n_yok}
        for hedef, et in (('AYI', 'AYI'), ('BOGA', 'BOĞA')):
            print(f"    · {et} vs diğerleri (eşli):")
            r = kiyas(tk, (lk == hedef), ad_a=f'{et} DIŞI', ad_b=et, n=n, yaz=yaz)
            if r and not r.get('yetersiz'):
                fb, fe = r['fark'].get('bek'), r['fark'].get('endeks_ustu')
                satir.update({f'{hedef}_pay%': round(100 * float((lk == hedef).mean())),
                              f'{hedef}_bek_fark': fb[0] if fb else np.nan,
                              f'{hedef}_bek_gercek': _gercek(fb),
                              f'{hedef}_eu_fark': fe[0] if fe else np.nan,
                              f'{hedef}_eu_gercek': _gercek(fe)})
        S.append(satir)
    d = pd.DataFrame(S)
    if d.empty: return d
    print(); print(d.round(2).to_string(index=False))
    print("\n  OKUMA: *_eu_fark = o rejimde endeks üstü getirinin diğerlerine göre farkı.")
    print("         BOĞA_eu_fark belirgin negatif ve gerçekse -> boğada sistem sadece beta.")
    print("         AYI_bek_fark pozitif ve gerçekse -> AYI'yı elemek zarar verirdi (kapı YOK).")
    print("         Tek eşikte gerçek = eşik seçimi riski; tekrar testi olmadan kural yapılmaz.")
    return d


# =====================================================================
# 4) ZAMAN SÜZGECİ — özellik mi, takvim mi?
# =====================================================================
def _takvim_dilimleri(t, n_donem):
    tt = t.sort_values('giris_t', kind='stable')
    for k, ix in enumerate(np.array_split(np.arange(len(tt)), n_donem)):
        if not len(ix): continue
        p = tt.iloc[ix]; g = pd.to_datetime(p['giris_t'])
        yield k + 1, f"{g.min().date()}..{g.max().date()}", p

def donem_ici(t, kolon, n_donem=None, n=None, yaz=True) -> pd.DataFrame:
    """Ölçünün ayırt ediciliği HER takvim diliminde ayrı. Yön değişiyorsa takvim etkisi."""
    n_donem = ocfg.n_donem if n_donem is None else n_donem
    if kolon not in t or kolon in ocfg.sonuc_kolonlari:
        if yaz: print(f"  {kolon}: sütun yok / sonuç sütunu"); return pd.DataFrame()
    S = []
    for k, etiket, p in _takvim_dilimleri(t, n_donem):
        nd = max(2, min(ocfg.n_dilim, int(p[kolon].notna().sum()) // max(ocfg.min_islem, 1)))
        d_ = dilim(p, kolon, n_dilim=nd, n=n, yaz=False)
        fb = getattr(d_, 'attrs', {}).get('fark_bek') if isinstance(d_, pd.DataFrame) else None
        S.append({'donem': k, 'tarih': etiket, 'n': len(p),
                  'ust-alt_bek': fb[0] if fb else np.nan, 'p5': fb[1] if fb else np.nan,
                  'p95': fb[2] if fb else np.nan, 'gercek': _gercek(fb)})
    d = pd.DataFrame(S)
    if d.empty: return d
    ge = d.dropna(subset=['ust-alt_bek'])
    if len(ge) < 2: hkm = 'YETERSİZ'
    else:
        yon = np.sign(ge['ust-alt_bek']); ayni = int((yon == yon.iloc[0]).sum()); ger = int(ge['gercek'].sum())
        # gürültüde işaret oynar: en az bir dilim anlamlı değilse yön hakkında hüküm verilmez
        hkm = ('ETKİ YOK (hiçbir dilimde anlamlı değil)' if ger == 0 else
               'DÖNEM BAĞIMSIZ' if ayni == len(ge) and ger >= max(1, len(ge) - 1) else
               'YÖN TUTARLI, kanıt zayıf' if ayni == len(ge) else 'TAKVİM ETKİSİ (yön dilimler arası değişiyor)')
    d.attrs['hukum'] = hkm
    if yaz:
        print(f"\n  --- {kolon}: takvim dilimlerinde ---"); print(d.round(2).to_string(index=False)); print(f"    HÜKÜM: {hkm}")
    return d

def icsel_dis(t, kolon, n_donem=None, n=None, yaz=True) -> dict:
    """Ölçüyü her takvim diliminde kendi medyanına göre merkezle -> 'ne zaman' bilgisi silinir.
    Merkezlenmiş ölçü hâlâ ayırt ediyorsa etki İÇSEL (hisse), yoksa TAKVİM."""
    n_donem = ocfg.n_donem_ic if n_donem is None else n_donem
    if kolon not in t or kolon in ocfg.sonuc_kolonlari: return {}
    tt = t.copy(); tt['_ham'] = pd.to_numeric(tt[kolon], errors='coerce'); tt['_mrk'] = np.nan
    for _, _, p in _takvim_dilimleri(tt, n_donem):
        v = pd.to_numeric(p[kolon], errors='coerce'); tt.loc[p.index, '_mrk'] = v - v.median()
    al = lambda d_: (getattr(d_, 'attrs', {}).get('fark_bek') or (np.nan, np.nan, np.nan))
    hm, hlo, hhi = al(dilim(tt, '_ham', n=n, yaz=False)); mm, mlo, mhi = al(dilim(tt, '_mrk', n=n, yaz=False))
    r = {'kolon': kolon, 'ham': hm, 'ham_p5': hlo, 'ham_p95': hhi, 'ici': mm, 'ici_p5': mlo, 'ici_p95': mhi,
         'ham_gercek': _gercek((hm, hlo, hhi)), 'ici_gercek': _gercek((mm, mlo, mhi))}
    # ham etki 1 puanın altındaysa oran anlamsız (payda ~0) -> gösterilmez
    r['ici_pay%'] = float(100 * mm / hm) if np.isfinite(hm) and np.isfinite(mm) and abs(hm) >= 1.0 else np.nan
    r['hukum'] = ('İÇSEL' if r['ici_gercek'] else 'TAKVİM' if r['ham_gercek'] else 'ETKİ YOK')
    if yaz:
        print(f"\n  --- {kolon}: içsel / takvim ({n_donem} dilim) ---")
        print(f"    ham etki        {_f(hm):>6}  [{_f(hlo)}, {_f(hhi)}]")
        pay = r['ici_pay%']
        ek = ('' if not np.isfinite(pay) else '   (yön tersine döndü)' if pay < 0 else f"   (hamın %{pay:.0f}'i kaldı)")
        print(f"    dönem-içi etki  {_f(mm):>6}  [{_f(mlo)}, {_f(mhi)}]{ek}")
        print(f"    HÜKÜM: {r['hukum']}" + {'İÇSEL': ' — aynı dönem içinde bile ayırt ediyor, ölçü gerçek',
                                            'TAKVİM': ' — ham etki var ama dönem içinde kayboluyor; hisse değil zaman bilgisi',
                                            'ETKİ YOK': ''}[r['hukum']])
    return r

def zaman_suzgeci(t, kolonlar=None, n=None, ad='') -> pd.DataFrame:
    kolonlar = [k for k in (kolonlar or ocfg.ozellikler) if k in t.columns and k not in ocfg.sonuc_kolonlari]
    print(f"\n===== ZAMAN SÜZGECİ [{ad}] — ölçü hisseyi mi ayırt ediyor, 'ne zaman'ı mı söylüyor? =====")
    S = []
    atlanan = []
    for k in kolonlar:
        s = pd.to_numeric(t[k], errors='coerce')
        if s.notna().sum() < ocfg.min_islem * 2 or s.nunique() < 3:      # boş / sabit sütun: test edilemez
            atlanan.append(k); continue
        d_ = donem_ici(t, k, n=n); r = icsel_dis(t, k, n=n)
        S.append({'olcu': k, 'donem_hukmu': getattr(d_, 'attrs', {}).get('hukum', '—'), 'ham': r.get('ham', np.nan),
                  'donem_ici': r.get('ici', np.nan), 'ici_pay%': r.get('ici_pay%', np.nan), 'hukum': r.get('hukum', '—')})
    if atlanan: print(f"  (atlandı — boş/sabit sütun: {', '.join(atlanan)})")
    o = pd.DataFrame(S)
    if o.empty: return o
    print("\n  --- ÖZET ---"); print(o.round(2).to_string(index=False))
    ic = o[o['hukum'] == 'İÇSEL']; tk = o[o['hukum'] == 'TAKVİM']
    if len(ic): print(f"\n  GERÇEK HİSSE AYIRT EDİCİ: {', '.join(ic['olcu'])}")
    if len(tk): print(f"  TAKVİM ETKİSİ (boyutlandırmada kullanılmaz): {', '.join(tk['olcu'])}")
    if not len(ic) and not len(tk): print("\n  Hiçbir ölçü ne içsel ne takvim etkisi gösteriyor.")
    return o


# =====================================================================
# 5) TEKRAR — çok set + takvim örtüşmesi (K4)
# =====================================================================
def _bulgular(t, xu, ad) -> dict:
    """Takip edilen bulgular: {ad: (deger, lo, hi, gercek)}"""
    B = {}
    b = bootstrap(t).get('a', {})
    for k, et in (('endeks_ustu', 'alfa (endeks üstü)'), ('bek', 'bek (taban)')):
        if k in b: B[et] = (*b[k], _gercek(b[k]))
    if 'GECER' in t and 0 < t['GECER'].astype(bool).sum() < len(t):
        r = kiyas(t, t['GECER'].astype(bool), yaz=False); fb = r.get('fark') or {}
        for k, et in (('bek', 'GECER → bek'), ('kazanan%', 'GECER → kazanan%'), ('agir%', 'GECER → ağır%')):
            if k in fb: B[et] = (*fb[k], _gercek(fb[k]))
    if xu is not None:
        for sma in ocfg.rejim_smalar:
            try:
                lab, _ = rejim_tablo(t, xu, sma=sma); tk = t[lab != 'YOK']; lk = lab[lab != 'YOK']
                for hedef, et in (('AYI', 'AYI'), ('BOGA', 'BOĞA')):
                    r = kiyas(tk, (lk == hedef), yaz=False); fb = r.get('fark') or {}
                    if 'bek' in fb: B[f'SMA{sma} {et} → bek farkı'] = (*fb['bek'], _gercek(fb['bek']))
                    if 'endeks_ustu' in fb: B[f'SMA{sma} {et} → alfa farkı'] = (*fb['endeks_ustu'], _gercek(fb['endeks_ustu']))
            except Exception as e:
                olog.warning(f'{ad} rejim SMA{sma}: {e}')
    for k in ocfg.ozellikler:
        if k not in t: continue
        try:
            d_ = dilim(t, k, yaz=False); fb = getattr(d_, 'attrs', {}).get('fark_bek')
            if fb: B[f'{k} (üst−alt)'] = (*fb, _gercek(fb))
        except Exception as e:
            olog.warning(f'{ad} dilim {k}: {e}')
    return B

def _ortusme(aral):
    """Set çiftlerinin takvim örtüşme oranı -> {(a,b): oran}"""
    out = {}
    adlar = list(aral)
    for i in range(len(adlar)):
        for j in range(i + 1, len(adlar)):
            a0, a1 = aral[adlar[i]]; b0, b1 = aral[adlar[j]]
            kes = max(0, (min(a1, b1) - max(a0, b0)).days); kis = min((a1 - a0).days, (b1 - b0).days)
            out[(adlar[i], adlar[j])] = kes / kis if kis > 0 else 0.0
    return out

def tekrar(setler, giris='acilis', tekil=True, kaydet=True) -> pd.DataFrame:
    """setler: [(ad, OB, xu|None), ...] -> yan yana tekrar matrisi.
    Takvimi %50+ örtüşen setler BAĞIMSIZ sayılmaz: 'bağımsız kanıt' sayısı buna göre hesaplanır."""
    islemler = _olc_g('islemler')
    if islemler is None: raise RuntimeError('islemler() yok — önce BASLAT (DENETIM).')
    TUM, aral = {}, {}
    for ad, OB, xu in setler:
        if not OB: print(f"[atlandı] {ad}: önbellek yok"); continue
        try:
            t = islemler(OB, giris, tekil=tekil, xu=xu)
            if t is None or t.empty: print(f"[atlandı] {ad}: işlem yok"); continue
            g = pd.to_datetime(t['giris_t']); aral[ad] = (g.min(), g.max())
            print(f"[{ad}] n={len(t)}  {g.min().date()}..{g.max().date()} — ölçülüyor...")
            TUM[ad] = _bulgular(t, xu, ad)
        except Exception as e:
            olog.error(f'{ad}: {e}\n{traceback.format_exc()}')
    if not TUM: print('sonuç yok'); return pd.DataFrame()

    adlar = list(TUM); ort = _ortusme(aral)
    # bağımsızlık grupları: %50+ örtüşenler aynı grup
    grup = {ad: i for i, ad in enumerate(adlar)}
    for (a, b), o in ort.items():
        if o >= 0.5:
            g_ = min(grup[a], grup[b])
            for k in adlar:
                if grup[k] in (grup[a], grup[b]): grup[k] = g_
    n_grup = len(set(grup.values()))
    if n_grup < len(adlar):
        print("\n  [UYARI] takvimi örtüşen setler bağımsız değil:")
        for (a, b), o in ort.items():
            if o >= 0.5: print(f"          {a} ~ {b}: %{100*o:.0f} örtüşme -> tek kanıt sayılır")

    bulgular = []
    for d in TUM.values():
        for k in d:
            if k not in bulgular: bulgular.append(k)
    S = []
    for b in bulgular:
        satir = {'bulgu': b}; yon, ger_grup, var_grup = [], set(), set()
        for ad in adlar:
            v = TUM[ad].get(b)
            if v is None or not np.isfinite(v[0]): satir[ad] = '—'; continue
            m, lo, hi, ger = v
            satir[ad] = f"{m:+.1f}{'*' if ger else ''}"
            yon.append(np.sign(m)); var_grup.add(grup[ad])
            if ger: ger_grup.add(grup[ad])
        nb, ng = len(var_grup), len(ger_grup)
        ayni = bool(yon) and all(y == yon[0] for y in yon)
        satir.update({'bağımsız_set': nb, 'aynı_yön': ayni, 'gerçek_set': ng})
        satir['hüküm'] = ('TEK SET' if nb < 2 else
                          'SAĞLAM' if ayni and ng >= 2 else
                          'ZAYIF (yön tutarlı, kanıt az)' if ayni and ng == 1 else
                          'TESADÜF (yön tutarsız)' if ng >= 1 else 'ETKİ YOK')
        S.append(satir)
    d = pd.DataFrame(S)
    print("\n" + "=" * 80); print("  TEKRAR MATRİSİ   (* = o sette %90 bant sıfırı kapsamıyor)"); print("=" * 80)
    print(d.to_string(index=False))
    print("\n===== HÜKÜM =====")
    for et, ac in (('SAĞLAM', 'birden fazla BAĞIMSIZ sette aynı yönde ve gerçek — kullanılabilir'),
                   ('ZAYIF (yön tutarlı, kanıt az)', 'izle, tek başına kural yapma'),
                   ('TESADÜF (yön tutarsız)', 'AT — çoklu karşılaştırma artığı'),
                   ('ETKİ YOK', 'hiçbir sette gerçek değil'), ('TEK SET', 'test edilemedi')):
        kes = d[d['hüküm'] == et]
        if len(kes): print(f"  {et}: {', '.join(kes['bulgu'])}\n      -> {ac}")
    print("\n  Hatırlatma: geçmişe dönük testtir, gelecek garantisi değildir.")
    if kaydet: _kaydet(d, 'tekrar_sonuc.csv')
    return d


# =====================================================================
# 6) ORKESTRA
# =====================================================================
def olcum(t, OB, xu=None, ad='BIST 2024-26', portfoy_de=True, kaydet=True, n=None) -> dict:
    """Tam rapor: taban → GECER → rejim → özellik taraması → zaman süzgeci → (portföy: kapasite, sıra, bant)."""
    xu = xu if xu is not None else _olc_g('xu'); C = {}
    try:
        if t is None or t.empty: print('işlem yok'); return C
        _gerekli_kolonlar(t, 'getiri', 'giris_t', 'poz')
        o = olculer(t); b = bootstrap(t, n=n).get('a', {})
        print(f"===== TABAN [{ad}] =====")
        print(f"  n={o['n']}  bek {_f(o['bek'])}  kazanan %{_f(o['kazanan%'],'.0f')}  medyan {_f(o['medyan'])}  "
              f"ağır %{_f(o['agir%'],'.0f')}  endeks üstü {_f(o['endeks_ustu'])}  süre {_f(o['bar'],'.0f')}b")
        _yaz_fark('gün-bloklu %90 bant', b); C['taban'] = o; C['taban_bant'] = b
        if 'GECER' in t:
            print(f"\n===== KURAL KAPISI (GECER) =====")
            C['gecer'] = kiyas(t, t['GECER'].astype(bool), 'GECER=0 (kural dışı)', 'GECER=1 (kural içi)', n=n)
        C['rejim'] = rejim_dilim(t, xu, n=n)
        C['tarama'] = tarama(t, n=n, yaz=False)
        C['zaman'] = zaman_suzgeci(t, n=n, ad=ad)
        if portfoy_de:
            print(f"\n{'='*30} PORTFÖY (yalnız bant; karar mercii değil) {'='*30}")
            G, Y = yol_kur(t, OB); C['kapasite'] = kapasite(t, G, Y, xu=xu, ad=ad); C['sira'] = sira_kiyas(t, G, Y, xu=xu, ad=ad)
    except Exception as e:
        olog.error(f'olcum: {e}\n{traceback.format_exc()}'); return C
    if kaydet:
        par = []
        for blok in ('tarama', 'rejim', 'zaman'):
            v = C.get(blok)
            if isinstance(v, pd.DataFrame) and not v.empty: par += [{'blok': blok, **r} for r in v.to_dict('records')]
        if par: _kaydet(pd.DataFrame(par), 'olcum_sonuc.csv')
    print("\n===== NASIL OKUNUR =====")
    print("  · Bant sıfırı kapsıyorsa FARK YOKTUR — kaç puan olduğu önemsizdir.")
    print("  · Karar mercii işlem başı ölçülerdir; portföy sayısı yalnız bant olarak okunur.")
    print("  · Bir bulgu kural olmadan önce: tekrar() (başka dönem/piyasa) + zaman süzgeci (İÇSEL).")
    return C


print("[ok] OLCUM v1.1 (2026-09-24, çatışma düzeltmesi): R = olcum(t, OB24, xu) | T = tekrar(setler) | dilim · kiyas · icsel_dis · bant · esli_kiyas")


# --- ÇAKIŞMA KAPISI (yükleme sonu): bu dosya bellekte var olan bir adı ezdiyse DUR ------------------
# Aynı dosyanın yeniden yüklenmesi serbesttir (kayıt defteri _CK_KAYIT ad -> sahip dosya).
def _cakisma_kontrol(_once=_CK_ONCE, _dosya='OLCUM.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE', '_CK_KAYIT', '_cakisma_kontrol', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya)
    yeni = [k for k in g if k not in _once and not k.startswith('__') and k not in atla]
    for k in yeni + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}. Üretim modülü bozulmuş olabilir; "
                           f"çakışan adı bu dosyada yeniden adlandır (ör. _olc_ öneki), sonra BASLAT'ı yeniden yükle.")
_cakisma_kontrol()
