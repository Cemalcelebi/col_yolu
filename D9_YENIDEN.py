"""D9_YENIDEN — AŞAMA 2/3 (iş tanımı 'AŞAMA 3'): COL_v1 D9 uzun çöl + D9b sektör rüzgârının ORTAK CETVEL ile yeniden ölçümü (14 Kasım 2026).

Cemal (14 Kas 2026): "uzun süren sıkışmanın ve rüzgâr etkisinin tespit performansını ölç".
Ç37 (IZ_KARNE): D9 'yön ADAY (%56-61); test sürüyor' diye kalmış, hiç kapanmamış; üretim ekranında (takip.py T8) duruyor.

SİNYAL (COL_v1.py'den BİREBİR; parametreler DEĞİŞMEZ, D9_PARAM sha256 ön kayıtta; COL_v1 değiştirilmez):
  D9  uzun_col_olc(df, t): pencere W = 250 bar ('12ay') ya da 125 bar ('6ay'; önce 12ay denenir); hissenin t'ye kadar en az W + 200 barı;
      kapanış %95 / %5 yüzdelik oranı <= 1,50; ortalama TR / ortalama kapanış <= 0,04; pencere medyanı, pencereden önceki 500 barın
      (Low min .. High max) aralığında <= 0,50 (dipte).
  D9b sektor_ruzgar(veri, t): her hissenin RUZ_GERI = 60 bar getirisi (başlangıç = taze hisselerin 61. son bar tarihlerinin medyanı t0;
      t0 ve öncesindeki son kapanış), piyasa = taze hisselerin getiri MEDYANI, sepet = aynı alt sektörün öteki üyelerinin eşit ağırlıklı
      ortalaması (en az 4 üye), ruz = sepet - piyasa; RÜZGÂR = ruz >= 0,10 VE sepet > 0. Taze = son barı ortak son tarihten en çok 5 iş
      günü eski (D10b).
Üç sinyal satırı (hepsi aynı cetvel, ORTAK_CETVEL.oc_olc): (a) D9; (b) D9 VE RÜZGÂR (üretim ruzgar_listesi); (c) RÜZGÂR VE D9 DEĞİL.
Sektör: BIST sektor_BIST.csv 'alt_bist' (COL_v1 sektor_tablosu ile aynı sütun), ABD sektor_ABD.csv 'endustri' (COL_v1'de ABD yok; alt
sektör karşılığı). AVR: sektör listesi yok -> yalnız (a); (b) / (c) 'AVRUPA VERİSİ YOK'.

Komut:  python D9_YENIDEN.py onkayit   ön kayıt (tanım, sha'lar, cetvel satırları, KONTROL LİSTESİ, OLAY SAYIMI; getiri hesaplanmaz)
        python D9_YENIDEN.py kos       ölçüm (OC.oc_kapi + kendi mühür / kod / git kapısı geçmezse durur)
        python D9_YENIDEN.py rapor     sonuç json'undan rapor
Colab:  exec(open('D9_YENIDEN.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   ORTAK_CETVEL.oc_veri (/tmp/veri V_*.pkl + /tmp/veri2/k34_yahoo.pkl); satır verisi /tmp/d9_yeniden (repoya girmez). Tiingo YOK.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_D9 = {k: id(v) for k, v in globals().items()}

import ast  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_D9 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_D9 not in sys.path:
    sys.path.insert(0, KOK_D9)

import ORTAK_CETVEL as OC  # noqa: E402

d9log = logging.getLogger("col.d9_yeniden")
if not d9log.handlers:
    _d9_h = logging.StreamHandler(sys.stderr)
    _d9_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s d9_yeniden: %(message)s", "%H:%M:%S"))
    d9log.addHandler(_d9_h)
    d9log.setLevel(logging.INFO)
    d9log.propagate = False

D9_SURUM = "D9_YENIDEN v1.0 (2026-11-14): COL_v1 D9 uzun çöl + D9b sektör rüzgârı, ORTAK CETVEL v1.0 ile"
D9_YOL = {"cikti": os.path.join(KOK_D9, "arastirma_cikti", "d9_yeniden"), "satir": os.environ.get("D9_SATIR", "/tmp/d9_yeniden"),
          "kod": os.path.join(KOK_D9, "D9_YENIDEN.py"), "col_v1": os.path.join(KOK_D9, "COL_v1.py"),
          "veri": os.environ.get("OC_VERI", "/tmp/veri"), "veri2": os.environ.get("OC_VERI2", "/tmp/veri2")}
D9_DOSYA = {"onkayit": "D9_YENIDEN_ON_KAYIT.md", "sonuc": "d9_yeniden_sonuc.json", "rapor": "D9_YENIDEN_RAPOR.md"}

# ================================================================ MÜHÜRLÜ PARAMETRELER (COL_v1.py'deki değerler; DEĞİŞMEZ)
D9_PARAM: Dict[str, Any] = {"UZUN_W": 250, "UZUN_BANT": 1.50, "UZUN_MUM": 0.04, "UZUN_KONUM": 0.5,
                            "RUZ_GERI": 60, "RUZ_ESIK": 0.10, "RUZ_MIN_UYE": 4, "RUZ_MUTLAK": 0.0, "RUZ_BAYAT": 5}

D9_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "param": D9_PARAM,
    "kaynak": "COL_v1.py uzun_col_olc (D9) + sektor_ruzgar (D9b / D10a / D10b); fonksiyonlar d9_uzun_ref / d9_ruzgar_ref olarak birebir "
              "kopyalandı (yalnız global VERI / Drive sektör yolu / log uyarısı parametreye alındı); vektörlü sürümler (d9_uzun_seri, "
              "d9_ruzgar_panel) test_d9_yeniden.py'de hem kopyayla hem COL_v1'in kendisiyle sentetik veride eşit",
    "satirlar": {"a": "D9 (uzun çöl; 12ay ya da 6ay)", "b": "D9 VE RÜZGÂR (D9b; üretim ruzgar_listesi)", "c": "RÜZGÂR VE D9 DEĞİL (rüzgârın kendi katkısı)"},
    "olay": "DURUM GÜNLERİ: sinyal koşulunun t kapanışında doğru olduğu her işlem günü (t = hissenin kendi barı, yalnız t'ye kadar bilgi) "
            "OC.oc_olc'a verilir; tekilleştirme (60 gün) ve giriş (ertesi geçerli açılış) cetvelindir. Üretim ekranı (T8) durumu her gün "
            "gösterdiği için durum günü seçildi (ilk gün değil); uzun durumda ~60 günde bir olay düşer.",
    "veri": "OC.oc_veri temiz bar (H>L, V>0; 31.08.2026 kesik) — sinyal de bu barlarla hesaplanır (üretim ham veriyle hesaplar; K3)",
    "sektor": {"BIST": ["sektor_BIST.csv", "alt_bist"], "ABD": ["sektor_ABD.csv", "endustri"], "AVR": None,
               "sembol": "büyük harf, '.AM' soneki silinir (sektor_ABD.csv kodları)",
               "not": "COL_v1 sektor_tablosu 'alt_bist' yoksa 'alt' okur; ABD dosyasında ikisi de yok -> 'endustri' (alt sektör karşılığı). "
                      "Sektör listesi bugünkü (K2 sınırı: sektör ataması karar günündeki hali değil; sınıf değişimi nadir)"},
    "piyasa": "pazarın (oc_veri evreni; ABD'de k34 hisseleri evren_bas gününden itibaren) taze hisselerinin 60 bar getiri MEDYANI "
              "(COL_v1 sektor_ruzgar; iş tanımındaki 'eşit ağırlıklı günlük ortalama' yerine COL_v1 tanımı korundu: sinyal değiştirilmez)",
    "evren_bas": "ABD k34 hisseleri evren_bas (k34_evren ilk_giris) gününden önce rüzgâr hesabına ve olaya girmez",
    "avr": "yalnız (a); (b) / (c) için 'AVRUPA VERİSİ YOK' (sektör listesi yok); karar en fazla ABD-ADAY",
    "bilgi": {"sure_W": [125, 190, 250],
              "sure": "aynı üç eşikle (bant, mum, konum; önceki 500 bar) W = 125 / 190 / 250: >=12 ay = 250 tutar; 9-12 = 250 tutmaz, 190 tutar; "
                      "6-9 = yalnız 125 tutar (yalnız (a) olaylarında; karar dışı)",
              "tercil": "ruz tercilleri: sınırlar her pazarın RÜZGÂR durum günlerinin (2016-01-01 .. 2026-08-31) ruz değerlerinin 1/3 ve 2/3 "
                        "yüzdeliği, ön kayıtta sayıyla yazılır; (b) ve (c) olaylarına aynı sınırlar; karar dışı"},
    "coklu": "3 ana satır; her satırın kararı ORTAK CETVEL dört karar hücresi kuralıyla; alt gruplar (süre, tercil) yalnız bilgi, etiketleri karar değildir",
    "olay_bas": "2015-06-01", "olay_son": "2026-08-31",
    "gelecek_denetimi_n": 30, "tohum": 314,
}

D9_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite "
                   "üçlüsü, aynı giriş (açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy. Mekanik üstünlük: D9 dar bant + dip "
                   "konumu düşük oynaklık / düşük momentum seçer, eş kovası momentumu eşler; oynaklık eşlenmez (raporda sınır). (c) rüzgâr "
                   "sektör momentumudur; hisse momentumu eşlenir, sektör momentumu eşlenmez (yorumda yazılır)"),
    "K2": ("EVET", "D9 t'ye kadar barlarla (rolling, geriye); rüzgâr t'ye kadar kapanışlarla (t0 taze hisselerin geçmiş tarihleri); "
                   "kos d9_gelecek_denetimi 30 rastgele olayda seriyi t'de kesip COL_v1 kopyasıyla aynı D9 / ruz değerini mekanik "
                   "denetler; test 'geleceğe bakma'. Sınır: sektör listesi bugünkü"),
    "K3": ("EVET", "OC.oc_veri temiz bar (H>L, V>0, fiyat > 0) üzerinden sinyal; geçersiz bar sinyal günü olamaz (cetvel sayımında 'sinyal barı geçersiz')"),
    "K4": ("EVET", "durum günleri cetvele verilir; oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücre tablosunda medyan"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); sinyal t kapanışında hesaplanır"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); D9 oranları birimden bağımsız; bölünme şüphesi cetvelde (geçmiş penceresi); "
                   "pencere içi bölünme bant ölçüsünü bozabilir (düzeltilmiş veride küçük)"),
    "K7": ("EVET", "evren bugün işlem görenler (+ ABD k34 nakdi biten); batanlar yok; oc_rapor notu: getiriler yukarı, -%50 olasılığı aşağı yanlı"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ ('iz değil' denmez); iki alt dönem şartı cetvelde; İZ DEĞİL yalnız güç yeterliyken; "
                   "olay sayımı ön kayıtta getiri hesaplanmadan"),
    "K9": ("EVET", "D9_ESIK sha + D9_PARAM sha + D9_YENIDEN.py sha + COL_v1.py sha + cetvel üç sha ön kayıtta; kos OC.oc_kapi + d9_onkayit_dogrula "
                   "(git işlenmiş / değişmemiş, sha eşit, D9_PARAM == COL_v1 sabitleri) geçmezse durur"),
    "K10": ("UYGULANMAZ", "metin / KAP ayrıştırma yok; yalnız OHLCV + iki sektör csv'si; 3 olay ham veriden elle doğrulanır (rapor DENETİM)"),
    "K11": ("EVET", "satır verisi /tmp/d9_yeniden/olay_<satır>.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM)"),
    "K12": ("EVET", "etiketler yalnız oc_etiket / oc_olasilik_etiket; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_d9; yasak dosyalar (COL_v1, ORTAK_CETVEL, IZ_KARNE, defterler) yalnız okunur, git diff "
                    "denetimi; e-posta / anahtar taraması testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; T8 için öneri yalnız 'kalsın / kaldırılsın' (karar Cemal'in)"),
}


class D9Hata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / git'e işlenmemiş / COL_v1 parametresi değişmiş / geleceğe bakma denetimi tutmadı."""


# ================================================================ 0) ORTAK
_D9_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _d9_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _d9_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def d9_sha(x: Any) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def _d9_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or D9_YOL["cikti"], D9_DOSYA.get(ad, ad))


def d9_col_v1_param(yol: Optional[str] = None) -> Dict[str, Any]:
    """COL_v1.py'yi ÇALIŞTIRMADAN (ast) D9 sabitlerini okur."""
    agac = ast.parse(open(yol or D9_YOL["col_v1"], encoding="utf-8").read())
    out: Dict[str, Any] = {}
    for dugum in agac.body:
        if isinstance(dugum, ast.Assign) and len(dugum.targets) == 1 and isinstance(dugum.targets[0], ast.Name):
            ad = dugum.targets[0].id
            if ad in D9_PARAM:
                out[ad] = ast.literal_eval(dugum.value)
    return out


def d9_param_denetle(yol: Optional[str] = None) -> None:
    c = d9_col_v1_param(yol)
    fark = {k: (v, c.get(k)) for k, v in D9_PARAM.items() if c.get(k) != v}
    if fark:
        raise D9Hata(f"D9_PARAM COL_v1 ile aynı değil: {fark}")


# ================================================================ 1) COL_v1 KOPYALARI (birebir; referans ve geleceğe bakma denetimi için)
def d9_uzun_ref(df: pd.DataFrame, tarih: Any = None, P: Dict[str, Any] = D9_PARAM) -> Optional[Dict[str, Any]]:
    """COL_v1.uzun_col_olc kopyası (sabitler P'den)."""
    UZUN_W, UZUN_BANT, UZUN_MUM, UZUN_KONUM = P["UZUN_W"], P["UZUN_BANT"], P["UZUN_MUM"], P["UZUN_KONUM"]
    try:
        x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
        C = x.Close.to_numpy(float); H = x.High.to_numpy(float); L = x.Low.to_numpy(float); n = len(C)
        if n < UZUN_W // 2 + 200: return None
        pc = np.roll(C, 1); pc[0] = C[0]
        TR = np.maximum(H - L, np.maximum(np.abs(H - pc), np.abs(L - pc)))
        out = None
        for W, ad in ((UZUN_W, '12ay'), (UZUN_W // 2, '6ay')):
            if n < W + 200: continue
            w = C[n - W:]
            if not np.isfinite(w).all() or np.nanmin(w) <= 0: continue
            hi, lo = np.percentile(w, 95), np.percentile(w, 5)
            bant = hi / lo - 1
            mum = float(np.nanmean(TR[n - W:]) / np.nanmean(w))
            on_l = L[max(0, n - W - 500):n - W]; on_h = H[max(0, n - W - 500):n - W]
            on_l = on_l[np.isfinite(on_l)]; on_h = on_h[np.isfinite(on_h)]
            if len(on_l) < 200: continue
            pmin, pmax = on_l.min(), on_h.max()
            konum = float((np.median(w) - pmin) / (pmax - pmin)) if pmax > pmin else np.nan
            ok = bool(hi / lo <= UZUN_BANT and mum <= UZUN_MUM and np.isfinite(konum) and konum <= UZUN_KONUM)
            if ok:
                return {'uzun': ad, 'bant': round(100 * bant, 1), 'konum': round(konum, 2), 'mum': round(mum, 3)}
            if out is None: out = {'uzun': '', 'bant': round(100 * bant, 1), 'konum': round(konum, 2) if np.isfinite(konum) else np.nan, 'mum': round(mum, 3)}
        return out
    except Exception as e:
        d9log.debug(f'uzun_col_olc: {e}'); return None


def d9_ruzgar_ref(veri: Dict[str, pd.DataFrame], sek: Dict[str, str], tarih: Any = None, P: Dict[str, Any] = D9_PARAM) -> pd.DataFrame:
    """COL_v1.sektor_ruzgar kopyası (veri ve sektör sözlüğü parametre; bayat uyarısı log yerine sessiz)."""
    RUZ_GERI, RUZ_ESIK, RUZ_MIN_UYE, RUZ_MUTLAK, RUZ_BAYAT = P["RUZ_GERI"], P["RUZ_ESIK"], P["RUZ_MIN_UYE"], P["RUZ_MUTLAK"], P["RUZ_BAYAT"]
    bos = pd.DataFrame(columns=['alt', 'ruz', 'sepet', 'piy', 'uye', 'g', 'ruzgar'])
    kes = {}
    for s, df in veri.items():
        try:
            x = df[df.index <= pd.Timestamp(tarih)] if tarih is not None else df
            if len(x) >= RUZ_GERI + 1: kes[s] = x
        except Exception as e: d9log.debug(f'{s} ruzgar: {e}')
    if not kes: return bos
    son = max(x.index[-1] for x in kes.values())
    sinir = son - pd.offsets.BDay(RUZ_BAYAT)
    taze = {s: x for s, x in kes.items() if x.index[-1] >= sinir}
    t0 = pd.Series([x.index[-RUZ_GERI - 1] for x in taze.values()]).median()
    getiri = {}
    for s, x in taze.items():
        try:
            on = x.Close[x.index <= t0]
            if on.empty: continue
            c0, c1 = float(on.iloc[-1]), float(x.Close.iloc[-1])
            if c0 > 0 and np.isfinite(c0) and np.isfinite(c1): getiri[s] = c1 / c0 - 1
        except Exception as e: d9log.debug(f'{s} ruzgar: {e}')
    g = pd.Series(getiri, dtype=float)
    if g.empty: return bos
    piy = float(g.median())
    alt = pd.Series({s: sek.get(str(s).upper()) for s in g.index})
    R = []
    for s in g.index:
        a = alt.get(s)
        if a is None or (isinstance(a, float) and np.isnan(a)):
            R.append({'sembol': s, 'alt': '', 'ruz': np.nan, 'sepet': np.nan, 'piy': piy, 'uye': 0, 'g': float(g[s])}); continue
        uy = [u for u in alt.index[alt == a] if u != s]
        if len(uy) < RUZ_MIN_UYE:
            R.append({'sembol': s, 'alt': a, 'ruz': np.nan, 'sepet': np.nan, 'piy': piy, 'uye': len(uy), 'g': float(g[s])}); continue
        sep = float(g[uy].mean())
        R.append({'sembol': s, 'alt': a, 'ruz': sep - piy, 'sepet': sep, 'piy': piy, 'uye': len(uy), 'g': float(g[s])})
    out = pd.DataFrame(R).set_index('sembol')
    out['ruzgar'] = (out.ruz >= RUZ_ESIK) & (out.sepet > RUZ_MUTLAK)
    return out


# ================================================================ 2) VEKTÖRLÜ D9 (her bar için uzun_col_olc)
def d9_uzun_seri(x: pd.DataFrame, P: Dict[str, Any] = D9_PARAM, Wler: Tuple[int, ...] = (250, 190, 125)) -> pd.DataFrame:
    """Hissenin her barı t için (seri t'de kesilmiş gibi) W penceresi tutuyor mu: sütunlar ok<W>, D9 (ok250 | ok125), uzun ('12ay' / '6ay' / '').
    uzun_col_olc ile aynı: n >= W + 200, kapanış %95/%5 <= BANT, ort TR / ort kapanış <= MUM, medyan konumu (önceki 500 bar) <= KONUM.
    Rolling pencereler yalnız geriye bakar (geleceğe bakma yok)."""
    C = x.Close.to_numpy(float); H = x.High.to_numpy(float); L = x.Low.to_numpy(float); n = len(C)
    pc = np.roll(C, 1)
    if n:
        pc[0] = C[0]
    TR = np.maximum(H - L, np.maximum(np.abs(H - pc), np.abs(L - pc)))
    s = pd.Series(C); tr = pd.Series(TR); nbar = np.arange(1, n + 1)
    Ls, Hs = pd.Series(L), pd.Series(H)
    pmin0 = Ls.rolling(500, min_periods=200).min(); pmax0 = Hs.rolling(500, min_periods=200).max()
    out = pd.DataFrame(index=x.index)
    for W in Wler:
        if n < W:
            out[f"ok{W}"] = False; continue
        hi = s.rolling(W).quantile(0.95).to_numpy(); lo = s.rolling(W).quantile(0.05).to_numpy()
        med = s.rolling(W).median().to_numpy()
        mum = (tr.rolling(W).mean() / s.rolling(W).mean()).to_numpy()
        mn = s.rolling(W).min().to_numpy()
        pmin = pmin0.shift(W).to_numpy(); pmax = pmax0.shift(W).to_numpy()
        with np.errstate(all="ignore"):
            konum = np.where(pmax > pmin, (med - pmin) / (pmax - pmin), np.nan)
            ok = (hi / lo <= P["UZUN_BANT"]) & (mum <= P["UZUN_MUM"]) & np.isfinite(konum) & (konum <= P["UZUN_KONUM"]) \
                & (nbar >= W + 200) & (mn > 0)
        out[f"ok{W}"] = ok
        if W == P["UZUN_W"]:
            out["bant250"] = hi / lo - 1; out["konum250"] = konum; out["mum250"] = mum
        if W == P["UZUN_W"] // 2:
            out["bant125"] = hi / lo - 1; out["konum125"] = konum; out["mum125"] = mum
    W12, W6 = P["UZUN_W"], P["UZUN_W"] // 2
    out["D9"] = out[f"ok{W12}"] | out[f"ok{W6}"]
    out["uzun"] = np.where(out[f"ok{W12}"], "12ay", np.where(out[f"ok{W6}"], "6ay", ""))
    if 190 in Wler:
        out["sure"] = np.where(out[f"ok{W12}"], ">=12", np.where(out["ok190"] & out["D9"], "9-12", np.where(out["D9"], "6-9", "")))
    return out


# ================================================================ 3) VEKTÖRLÜ RÜZGÂR (her takvim günü için sektor_ruzgar)
def d9_sektor(pazar: str, E: Dict[str, Any] = D9_ESIK) -> Dict[str, str]:
    """pazar -> {SEMBOL: alt sektör}. AVR -> {} (liste yok)."""
    t = E["sektor"].get(pazar)
    if not t:
        return {}
    yol = os.path.join(KOK_D9, t[0])
    if not os.path.exists(yol):
        raise D9Hata(f"sektör dosyası yok: {yol}")
    df = pd.read_csv(yol).dropna(subset=[t[1]])
    return {re.sub(r"\.AM$", "", str(r.sembol).upper().strip()): str(getattr(r, t[1])) for r in df.itertuples()}


def d9_ruzgar_panel(Vd: Dict[str, Any], sek: Dict[str, str], P: Dict[str, Any] = D9_PARAM, bas: Optional[str] = None) -> Dict[str, Any]:
    """Birleşik takvimin her günü t için sektor_ruzgar(veri, t) (hisse x gün): ruz, sepet, ruzgar. Vd: OC.oc_veri çıktısı.
    evren_bas'tan önceki hisse günleri (ABD k34) hesaba girmez. bas verilirse yalnız o günden sonrası hesaplanır."""
    V = Vd["V"]; S = sorted(V); u = len(S)
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    n = len(idx); G = P["RUZ_GERI"]
    Cl = pd.DataFrame({s: V[s].Close for s in S}).reindex(idx)
    pres = Cl.notna().to_numpy()
    Cff = Cl.ffill().to_numpy(float)
    cnt = np.cumsum(pres, axis=0)
    gun = idx.values.astype("datetime64[D]").astype(np.int64)          # takvim günü (birimden bağımsız tam sayı)
    son_tarih = pd.DataFrame(np.where(pres, gun[:, None], np.nan)).ffill().to_numpy()
    d61 = np.full((n, u), np.nan)
    sinir_on: Dict[int, int] = {}
    for j, s in enumerate(S):
        oi = V[s].index.values.astype("datetime64[D]").astype(np.int64).astype(float); k = cnt[:, j]
        ok = k >= G + 1
        d61[ok, j] = oi[k[ok] - G - 1]
    evb = np.array([idx.searchsorted(Vd.get("evren_bas", {}).get(s)) if s in Vd.get("evren_bas", {}) else 0 for s in S])
    kod = {a: i for i, a in enumerate(sorted(set(sek.values())))}
    sc = np.array([kod.get(sek.get(str(s).upper()), -1) for s in S]); nk = max(len(kod), 1)
    RUZ = np.full((n, u), np.nan); SEP = np.full((n, u), np.nan); PIY = np.full(n, np.nan)
    d0 = idx.searchsorted(pd.Timestamp(bas)) if bas else 0
    dd = np.arange(n)
    for d in range(d0, n):
        kes = (cnt[d] >= G + 1) & (d >= evb)
        if not kes.any():
            continue
        son = int(np.nanmax(son_tarih[d, kes]))
        if son not in sinir_on:
            sn = pd.Timestamp(np.datetime64(son, "D")) - pd.offsets.BDay(P["RUZ_BAYAT"])
            sinir_on[son] = int(np.datetime64(sn.normalize().date(), "D").astype(np.int64))
        taze = kes & (son_tarih[d] >= sinir_on[son])
        t0 = float(np.median(d61[d, taze]))      # pd.Series(Timestamp).median ile aynı: çift sayıda iki ortanın ortası
        p = int(np.searchsorted(gun, t0, side="right")) - 1
        if p < 0:
            continue
        c0 = Cff[p]; c1 = Cff[d]
        with np.errstate(all="ignore"):
            gec = taze & np.isfinite(c0) & (c0 > 0) & np.isfinite(c1)
            g = c1 / c0 - 1
        if not gec.any():
            continue
        piy = float(np.median(g[gec])); PIY[d] = piy
        m = gec & (sc >= 0)
        if not m.any():
            continue
        top = np.bincount(sc[m], weights=g[m], minlength=nk); say = np.bincount(sc[m], minlength=nk)
        jj = np.where(m)[0]; uy = say[sc[jj]] - 1
        tut = uy >= P["RUZ_MIN_UYE"]
        sep = (top[sc[jj]] - g[jj]) / np.where(uy > 0, uy, 1)
        SEP[d, jj[tut]] = sep[tut]; RUZ[d, jj[tut]] = sep[tut] - piy
    del dd
    with np.errstate(invalid="ignore"):
        RZ = (RUZ >= P["RUZ_ESIK"]) & (SEP > P["RUZ_MUTLAK"])
    return {"tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "ruz": RUZ, "sepet": SEP, "ruzgar": RZ, "piy": PIY}


# ================================================================ 4) DURUM GÜNLERİ ve SİNYAL SATIRLARI
def d9_durum(Vd: Dict[str, Any], pazar: str, E: Dict[str, Any] = D9_ESIK) -> pd.DataFrame:
    """Her hisse-gün (oc_veri temiz barları) için D9 ve rüzgâr; yalnız D9 ya da RÜZGÂR doğru olan satırlar döner."""
    P = E["param"]; V = Vd["V"]; sek = d9_sektor(pazar, E)
    RP = d9_ruzgar_panel(Vd, sek, P) if sek else None
    a, b = pd.Timestamp(E["olay_bas"]), pd.Timestamp(E["olay_son"])
    parca = []
    for s in sorted(V):
        x = V[s]
        U = d9_uzun_seri(x, P, tuple(E["bilgi"]["sure_W"])[::-1])
        tar = x.index
        if RP is not None:
            r = RP["tarih"].get_indexer(tar); j = RP["kol"][s]
            ruz = RP["ruz"][r, j]; sep = RP["sepet"][r, j]; rz = RP["ruzgar"][r, j]
        else:
            ruz = np.full(len(tar), np.nan); sep = ruz.copy(); rz = np.zeros(len(tar), bool)
        evb = Vd.get("evren_bas", {}).get(s)
        m = (U.D9.to_numpy() | rz) & (tar >= a) & (tar <= b)
        if evb is not None:
            m &= tar >= pd.Timestamp(evb)
        if not m.any():
            continue
        parca.append(pd.DataFrame({"sembol": s, "tarih": tar[m], "pazar": pazar, "D9": U.D9.to_numpy()[m], "uzun": U.uzun.to_numpy()[m],
                                   "sure": U.sure.to_numpy()[m], "ruz": ruz[m], "sepet": sep[m], "ruzgar": rz[m],
                                   "bant250": U.bant250.to_numpy()[m], "bant125": U.bant125.to_numpy()[m]}))
    D = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["sembol", "tarih", "pazar", "D9", "uzun", "sure", "ruz",
                                                                                "sepet", "ruzgar", "bant250", "bant125"])
    D["sektor_var"] = bool(sek)
    return D


def d9_satir(D: pd.DataFrame, satir: str) -> pd.DataFrame:
    """Durum tablosundan sinyal satırı: a = D9; b = D9 & RÜZGÂR; c = RÜZGÂR & ~D9. Sektörsüz pazarda b / c boş."""
    D9b = D.D9.astype(bool); rz = D.ruzgar.astype(bool); sv = D.sektor_var.astype(bool)
    if satir == "a":
        m = D9b
    elif satir == "b":
        m = D9b & rz & sv
    elif satir == "c":
        m = rz & ~D9b & sv
    else:
        raise D9Hata(f"bilinmeyen satır {satir}")
    return D[m].reset_index(drop=True)


def d9_tercil_sinir(D: pd.DataFrame) -> Dict[str, List[float]]:
    out = {}
    for p, x in D[D.ruzgar.astype(bool)].groupby("pazar"):
        v = x.ruz.to_numpy(float); v = v[np.isfinite(v)]
        if len(v):
            out[p] = [float(np.quantile(v, 1 / 3)), float(np.quantile(v, 2 / 3))]
    return out


def d9_tercil(X: pd.DataFrame, sinir: Dict[str, List[float]]) -> np.ndarray:
    t = np.array([""] * len(X), dtype=object)
    for p, (q1, q2) in sinir.items():
        m = (X.pazar == p).to_numpy(); r = X.ruz.to_numpy(float)
        t[m & (r < q1)] = "T1 zayıf"; t[m & (r >= q1) & (r < q2)] = "T2 orta"; t[m & (r >= q2)] = "T3 güçlü"
    return t


# ================================================================ 5) VERİ + PANEL
def d9_veri(pazarlar: Tuple[str, ...] = ("BIST", "ABD", "AVR"), veri: Optional[str] = None, veri2: Optional[str] = None) -> Dict[str, Any]:
    return {p: OC.oc_veri(p, klasor=veri, veri2=veri2) for p in pazarlar}


def d9_sayim(D: pd.DataFrame, PN: Dict[str, Any], tercil: Dict[str, List[float]]) -> Dict[str, Any]:
    """Getiri HESAPLANMADAN olay sayımı: durum günleri (t'ye göre dönem) ve cetvel olay hazırlığı sonrası (tekil, havuz; girişe göre dönem)."""
    out: Dict[str, Any] = {}
    for sat in ("a", "b", "c"):
        X = d9_satir(D, sat)
        out[sat] = {}
        for p in sorted(set(D.pazar)):
            x = X[X.pazar == p]
            if sat in ("b", "c") and not bool(D[D.pazar == p].sektor_var.any()):
                out[sat][p] = {"not": "AVRUPA VERİSİ YOK (sektör listesi yok)"}; continue
            dt = OC._oc_donem(x.tarih, OC.OC_ESIK) if len(x) else np.array([])
            Y, say = OC.oc_olay_hazirla(x[["sembol", "tarih", "pazar"]], PN[p], OC.OC_ESIK)
            out[sat][p] = {"durum_gunu": {d: int((dt == d).sum()) for d in ("2016-22", "2023", "2024-26")},
                           "olay": {d: int((Y.donem == d).sum()) for d in ("2016-22", "2023", "2024-26")} if len(Y) else {},
                           "dusme": say}
            if sat == "a" and len(Y):
                Y2 = Y.merge(x[["sembol", "tarih", "sure"]], on=["sembol", "tarih"], how="left")
                out[sat][p]["sure"] = {k: {d: int(((Y2.sure == k) & (Y2.donem == d)).sum()) for d in ("2016-22", "2023", "2024-26")}
                                       for k in ("6-9", "9-12", ">=12")}
            if sat in ("b", "c") and len(Y):
                Y2 = Y.merge(x[["sembol", "tarih", "ruz", "pazar"]], on=["sembol", "tarih"], how="left")
                tt = d9_tercil(Y2, tercil)
                out[sat][p]["tercil"] = {k: {d: int(((tt == k) & (Y2.donem == d)).sum()) for d in ("2016-22", "2023", "2024-26")}
                                         for k in ("T1 zayıf", "T2 orta", "T3 güçlü")}
    return out


# ================================================================ 6) ÖN KAYIT ve KAPI
_D9_DESEN = {"esik": r"D9_ESIK_SHA:\s*`([0-9a-f]{64})`", "param": r"D9_PARAM_SHA:\s*`([0-9a-f]{64})`",
             "kod": r"D9_KOD_SHA:\s*`([0-9a-f]{64})`", "col_v1": r"COL_V1_SHA:\s*`([0-9a-f]{64})`"}


def d9_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = D9_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _d9_say_tablo(say: Dict[str, Any]) -> List[str]:
    s = ["| Satır | Pazar | durum günü 2016-22 / 2023 / 2024-26 | OLAY (cetvel sonrası, girişe göre) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |",
         "|---|---|---|---|---|---|"]
    for sat, d in say.items():
        for p, c in d.items():
            if "not" in c:
                s.append(f"| {sat} | {p} | - | {c['not']} | - | - |"); continue
            dg = c["durum_gunu"]; ol = c.get("olay", {})
            s.append(f"| {sat} | {p} | {dg.get('2016-22', 0)} / {dg.get('2023', 0)} / {dg.get('2024-26', 0)} | "
                     f"{ol.get('2016-22', 0)} / {ol.get('2023', 0)} / {ol.get('2024-26', 0)} | {c['dusme'].get('tekil', 0)} | {c['dusme'].get('havuz_disi', 0)} |")
    return s


def d9_onkayit_metni(say: Dict[str, Any], tercil: Dict[str, List[float]], vsha: Dict[str, str], E: Dict[str, Any] = D9_ESIK) -> str:
    s = ["# D9_YENIDEN — ÖN KAYIT", "", f"{D9_SURUM}", "",
         f"- D9_ESIK_SHA: `{d9_sha(E)}`", f"- D9_PARAM_SHA: `{d9_sha(E['param'])}`", f"- D9_KOD_SHA: `{_d9_sha_dosya(D9_YOL['kod'])}`",
         f"- COL_V1_SHA: `{_d9_sha_dosya(D9_YOL['col_v1'])}`", f"- ZAMAN (UTC): `{_d9_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı). `kos` bu dosya git'e işlenmiş ve "
         "değişmemiş değilse, sha'lardan biri tutmazsa ya da D9_PARAM COL_v1 sabitlerinden farklıysa durur.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Soru", "", "Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisinin tespit performansını ölç'. Ç37 D9 uzun çöl + D9b rüzgâr (üretim ekranı T8) "
         "ORTAK CETVEL ile: eş farkı, slot portföy / plasebo, olasılık tablosu (+%100 / -%50, 250 gün).", "",
         "## Sinyal tanımı (COL_v1.py'den birebir; parametreler)", "", "```json", json.dumps(E["param"], ensure_ascii=False, indent=1, sort_keys=True), "```", "",
         "- D9 = uzun_col_olc(t)['uzun'] in {12ay, 6ay}: W = 250 (önce) / 125 bar; t'ye kadar en az W + 200 bar; kapanış %95 / %5 <= 1,50; "
         "ort TR / ort kapanış <= 0,04; pencere medyanı önceki 500 barın (Low min .. High max) aralığında <= 0,50.",
         "- RÜZGÂR (D9b / D10a) = sektor_ruzgar(t): ruz = sepet (alt sektörün öteki üyeleri, en az 4, eşit ağırlık) - piyasa (taze hisselerin 60 bar "
         "getiri MEDYANI) >= 0,10 VE sepet > 0; taze = son bar ortak son tarihten en çok 5 iş günü eski; 60 bar başlangıcı t0 = taze hisselerin "
         "61. son bar tarihlerinin medyanı.",
         f"- Satırlar: {json.dumps(E['satirlar'], ensure_ascii=False)}", f"- Olay: {E['olay']}", f"- Veri: {E['veri']}",
         f"- Sektör: BIST sektor_BIST.csv 'alt_bist'; ABD sektor_ABD.csv 'endustri'. {E['sektor']['not']}",
         f"- Piyasa: {E['piyasa']}", f"- {E['evren_bas']}", f"- AVR: {E['avr']}", f"- Çoklu karşılaştırma: {E['coklu']}", "",
         "## SAPMA (sonuç görülmeden yazıldı)", "",
         "- İş tanımı 'piyasa = pazarın eşit ağırlıklı günlük ortalaması' diyor; COL_v1 sektor_ruzgar piyasayı 60 bar getirilerinin MEDYANI olarak "
         "hesaplar. 'Sinyal tanımı değiştirilmez' kuralı öncelikli: COL_v1 medyanı kullanıldı.",
         "- COL_v1'de ABD sektör sütunu tanımlı değil (sektor_tablosu 'alt_bist' / 'alt' arar, sektor_ABD.csv'de ikisi de yok): ABD için 'endustri' "
         "seçildi (BIST alt endekslerinin karşılığı, alt sektör). ABD k34 hisselerinin çoğu sektör listesinde yok: piyasa medyanına girer, rüzgâr alamaz.",
         "- Üretim sinyali ham veriyle hesaplar; burada cetvelin temiz barları (H>L, V>0) kullanıldı (K3).",
         "- Fon süzgeci (D8, Eylül 2026) ölçüm penceresi dışında (kriz kesiği 31.08.2026): uygulanmadı.", "",
         "## Bilgi (karar dışı) alt gruplar", "", f"- Çöl süresi: {E['bilgi']['sure']}", f"- Rüzgâr şiddeti: {E['bilgi']['tercil']}",
         "- Tercil sınırları (ruz, sonuç görülmeden): " + "; ".join(f"{p}: {q[0]:.4f} / {q[1]:.4f}" for p, q in tercil.items()), "",
         "## Veri sha256", ""] + [f"- V_{p}.pkl: `{v}`" for p, v in vsha.items()] + ["",
         "## OLAY SAYIMI (getiri hesaplanmadan)", ""] + _d9_say_tablo(say) + ["",
         "Süre sınıfları ve tercil sayıları (olay, girişe göre dönem):", "", "```json", json.dumps({k: {p: {a: b for a, b in c.items() if a in ("sure", "tercil")}
                                                                                                  for p, c in v.items() if "not" not in c} for k, v in say.items()},
                                                                                              ensure_ascii=False, indent=1), "```", "",
         "Kural: bir hücrede n < 30 ise ÖLÇÜLEMEDİ yazılır, 'iz değil' denmez (cetvel oc_hucre_durum).", "",
         d9_kontrol_tablosu(), "",
         "## Test", "", "`python test_d9_yeniden.py` (sentetik: D9 / rüzgâr kopyası COL_v1 ile birebir, vektörlü sürüm kopyayla birebir, geleceğe "
         "bakma kesme testi, D9_PARAM == COL_v1 sabitleri, cetvel çağrısı, kapı, e-posta / anahtar taraması).", ""]
    return "\n".join(s)


def d9_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _d9_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise D9Hata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise D9Hata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    d9_param_denetle()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    VV = d9_veri(veri=veri); D_, PN, vsha = [], {}, {}
    for p, Vd in VV.items():
        vsha[p] = _d9_sha_dosya(os.path.join(veri or D9_YOL["veri"], f"V_{p}.pkl"))
        D_.append(d9_durum(Vd, p)); PN[p] = OC.oc_panel(Vd)
        d9log.info("%s durum günleri: %d", p, len(D_[-1]))
    D = pd.concat(D_, ignore_index=True)
    tercil = d9_tercil_sinir(D)
    say = d9_sayim(D, PN, tercil)
    metin = d9_onkayit_metni(say, tercil, vsha)
    if _D9_EPOSTA.search(metin):
        raise D9Hata("ön kayıtta e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    with open(os.path.join(os.path.dirname(yol), "d9_tercil.json"), "w", encoding="utf-8") as f:
        json.dump(tercil, f, indent=1)
    d9log.info("ön kayıt yazıldı: %s", yol)
    return yol


def d9_onkayit_dogrula(yol: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    yol = yol or _d9_yol("onkayit")
    if not os.path.exists(yol):
        raise D9Hata(f"ön kayıt yok ({yol}): önce `python D9_YENIDEN.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); b = {}
    for ad, desen in _D9_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise D9Hata(f"ön kayıt bozuk: '{ad}' satırı yok")
        b[ad] = m.group(1)
    simdi = {"esik": d9_sha(D9_ESIK), "param": d9_sha(D9_PARAM), "kod": _d9_sha_dosya(D9_YOL["kod"]), "col_v1": _d9_sha_dosya(D9_YOL["col_v1"])}
    for ad in simdi:
        if b[ad] != simdi[ad]:
            raise D9Hata(f"{ad} sha tutmuyor (ön kayıt {b[ad][:12]}…, şimdi {simdi[ad][:12]}…): koşu DURDU (SAPMA)")
    d9_param_denetle()
    out = {"yol": yol, **b}
    if git:
        try:
            out["git"] = OC._oc_git_islenmis(yol); out["git_kod"] = OC._oc_git_islenmis(D9_YOL["kod"])
            out["git_tercil"] = OC._oc_git_islenmis(os.path.join(os.path.dirname(yol), "d9_tercil.json"))
        except OC.OCHata as ex:
            raise D9Hata(str(ex))
    return out


# ================================================================ 7) GELECEĞE BAKMA DENETİMİ (koşu içinde)
def d9_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, pazar: str, n: int, tohum: int) -> int:
    """Rastgele n olayda seri t'de kesilir: COL_v1 kopyası (d9_uzun_ref / d9_ruzgar_ref) aynı D9 / ruz değerini vermeli."""
    if not len(X):
        return 0
    rng = np.random.default_rng(tohum); sec = X.iloc[rng.choice(len(X), min(n, len(X)), replace=False)]
    sek = d9_sektor(pazar); V = Vd["V"]; evb = Vd.get("evren_bas", {})
    for r in sec.itertuples():
        t = pd.Timestamp(r.tarih)
        u = d9_uzun_ref(V[r.sembol], t)
        d9 = bool(u and u["uzun"])
        if d9 != bool(r.D9) or (d9 and u["uzun"] != r.uzun):
            raise D9Hata(f"geleceğe bakma / kopya denetimi D9 tutmadı: {pazar} {r.sembol} {t.date()} ({u} vs {r.D9} {r.uzun})")
        if sek:
            kes = {s: x[x.index <= t] for s, x in V.items() if not (s in evb and t < pd.Timestamp(evb[s]))}
            R = d9_ruzgar_ref(kes, sek, t)
            rz = float(R.ruz.get(r.sembol, np.nan)) if r.sembol in R.index else np.nan
            if not ((np.isnan(rz) and np.isnan(r.ruz)) or (np.isfinite(rz) and np.isfinite(r.ruz) and abs(rz - r.ruz) < 1e-9)):
                raise D9Hata(f"geleceğe bakma / kopya denetimi rüzgâr tutmadı: {pazar} {r.sembol} {t.date()} ({rz} vs {r.ruz})")
    return len(sec)


# ================================================================ 8) KOŞU
def _d9_birlestir(parca: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pazar başına oc_olc çıktılarını tek S'de birleştirir; genel etiket OC.oc_etiket ile (cetvel kuralı)."""
    T = pd.concat([p["hucre"] for p in parca if len(p["hucre"])], ignore_index=True) if parca else pd.DataFrame()
    S = {"hucre": T, "olay": pd.concat([p["olay"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
         "olasilik": pd.concat([p["olasilik"] for p in parca], ignore_index=True) if parca else pd.DataFrame(),
         "sayim": {k: v for p in parca for k, v in p["sayim"].items()},
         "etiket": OC.oc_etiket(T) if len(T) else {"genel": "VERİ YOK", "olasilik": "ÖLÇÜLEMEDİ", "karar_hucre": {}},
         "cetvel_sha": parca[0]["cetvel_sha"] if parca else OC.oc_esik_sha(), "kod_sha": parca[0]["kod_sha"] if parca else "",
         "surum": OC.OC_SURUM}
    return S


def d9_olc_satir(X: pd.DataFrame, PN: Dict[str, Any]) -> Dict[str, Any]:
    """Bir sinyal satırını pazar pazar OC.oc_olc ile ölçer (panel önbelleği: her çağrıda tek pazar)."""
    parca = []
    for p in [q for q in OC.OC_ESIK["pazar"] if q in set(X.pazar)]:
        x = X[X.pazar == p][["sembol", "tarih", "pazar"]].reset_index(drop=True)
        parca.append(OC.oc_olc(x, {p: PN[p]}))
    return _d9_birlestir(parca)


def _d9_json_S(S: Dict[str, Any]) -> Dict[str, Any]:
    return {"hucre": json.loads(S["hucre"].to_json(orient="records", force_ascii=False)) if len(S["hucre"]) else [],
            "olasilik": json.loads(S["olasilik"].to_json(orient="records", force_ascii=False)) if len(S["olasilik"]) else [],
            "etiket": S["etiket"], "sayim": json.loads(json.dumps(S["sayim"], default=int)), "cetvel_sha": S["cetvel_sha"], "kod_sha": S["kod_sha"]}


def d9_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t_bas = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _d9_yol("onkayit", cikti)
    kapi = OC.oc_kapi(yol, git=git, kontrol=kontrol)
    oc = d9_onkayit_dogrula(yol, git=git)
    kos_zaman = _d9_simdi()
    tercil = json.load(open(os.path.join(os.path.dirname(yol), "d9_tercil.json"), encoding="utf-8"))
    satir_kl = D9_YOL["satir"]; os.makedirs(satir_kl, exist_ok=True)
    VV = d9_veri(veri=veri); D_, PN, den = [], {}, {}
    for p, Vd in VV.items():
        D_.append(d9_durum(Vd, p)); PN[p] = OC.oc_panel(Vd)
        X = D_[-1]; X = X[X.D9.astype(bool) | X.ruzgar.astype(bool)]
        den[p] = d9_gelecek_denetimi(Vd, X, p, D9_ESIK["gelecek_denetimi_n"], D9_ESIK["tohum"])
        d9log.info("%s: durum %d, geleceğe bakma denetimi %d olay TUTTU", p, len(D_[-1]), den[p])
    D = pd.concat(D_, ignore_index=True); del VV
    D.to_csv(os.path.join(satir_kl, "durum.csv.gz"), index=False)
    sonuc: Dict[str, Any] = {"surum": D9_SURUM, "onkayit": oc, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"}, "kos_zaman_utc": kos_zaman,
                             "tercil": tercil, "gelecek_denetimi": den, "ana": {}, "bilgi": {}}
    for sat in ("a", "b", "c"):
        X = d9_satir(D, sat)
        S = d9_olc_satir(X, PN)
        Ol = S["olay"].merge(X[["sembol", "tarih", "pazar", "uzun", "sure", "ruz", "sepet"]], on=["sembol", "tarih", "pazar"], how="left")
        Ol.to_csv(os.path.join(satir_kl, f"olay_{sat}.csv.gz"), index=False)
        sonuc["ana"][sat] = _d9_json_S(S); sonuc["ana"][sat]["rapor"] = OC.oc_rapor(S, f"({sat}) {D9_ESIK['satirlar'][sat]}")
        d9log.info("satır %s: %s / %s (%.0f sn)", sat, S["etiket"]["genel"], S["etiket"]["olasilik"], time.time() - t_bas)
        # bilgi alt grupları: olay listesi (tekil sonrası) aynı kalsın diye alt grup, ana satırın TEKİL olaylarından seçilir
        if sat == "a":
            grup = {k: Ol[Ol.sure == k] for k in ("6-9", "9-12", ">=12")}
        else:
            tt = d9_tercil(Ol, tercil); grup = {k: Ol[tt == k] for k in ("T1 zayıf", "T2 orta", "T3 güçlü")}
        sonuc["bilgi"][sat] = {}
        for k, g in grup.items():
            Sg = d9_olc_satir(g[["sembol", "tarih", "pazar"]], PN)
            sonuc["bilgi"][sat][k] = _d9_json_S(Sg)
    sonuc["sure_sn"] = round(time.time() - t_bas, 1)
    os.makedirs(cikti or D9_YOL["cikti"], exist_ok=True)
    with open(_d9_yol("sonuc", cikti), "w", encoding="utf-8") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1, default=str)
    return {"sonuc": sonuc, "rapor": d9_rapor(cikti)}


# ================================================================ 9) RAPOR
def _yz(x: Any, n: int = 1) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{100 * x:+.{n}f}%".replace(".", ",")


def _sy(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(x) else f"{x:.{n}f}".replace(".", ",")


def d9_ozet_satir(J: Dict[str, Any]) -> Dict[str, Any]:
    """Bir satırın karar hücreleri için kısa özet (n, ort fark, durum, up100 / dn50 katı)."""
    o = {}
    H = {(h["pazar"], h["donem"]): h for h in J["hucre"]}; Ob = {(h["pazar"], h["donem"]): h for h in J["olasilik"]}
    for p in ("ABD", "AVR", "BIST"):
        for d in ("2016-22", "2023", "2024-26"):
            h = H.get((p, d)); b = Ob.get((p, d), {})
            if h is None:
                continue
            o[f"{p} {d}"] = {"n": h.get("n", 0), "fark": h.get("ort_fark"), "alt": h.get("alt95"), "durum": h.get("durum"),
                             "up": b.get("up100_es_kat"), "up_alt": b.get("up100_es_alt"), "up_ust": b.get("up100_es_ust"),
                             "dn": b.get("dn50_es_kat"), "dn_alt": b.get("dn50_es_alt"), "dn_ust": b.get("dn50_es_ust"), "olas": h.get("olas"),
                             "n250": b.get("n250")}
    return o


def d9_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_d9_yol("sonuc", cikti), encoding="utf-8"))
    ad = D9_ESIK["satirlar"]
    s = ["# D9_YENIDEN — RAPOR (Ç37 D9 uzun çöl + D9b sektör rüzgârı, ORTAK CETVEL v1.0)", "",
         f"Ön kayıt commit {J['onkayit'].get('git', {}).get('commit', '-')[:10]} ({J['onkayit'].get('git', {}).get('commit_zamani', '-')}); "
         f"koşu {J['kos_zaman_utc']}; süre {J.get('sure_sn')} sn. Geleceğe bakma / kopya denetimi: " +
         ", ".join(f"{p} {n} olay TUTTU" for p, n in J["gelecek_denetimi"].items()) + ".", "",
         "## DÜZ DİL ÖZET", ""]
    for sat in ("a", "b", "c"):
        e = J["ana"][sat]["etiket"]
        s.append(f"- ({sat}) {ad[sat]}: GENEL **{e['genel']}**, OLASILIK **{e['olasilik']}**.")
        oz = d9_ozet_satir(J["ana"][sat])
        par = []
        for k in ("ABD 2023", "ABD 2024-26", "AVR 2023", "AVR 2024-26", "BIST 2023", "BIST 2024-26"):
            if k in oz:
                v = oz[k]
                par.append(f"{k}: n {v['n']}, eş farkı {_yz(v['fark'])} ({v['durum']}), +%100 katı {_sy(v['up'])}, -%50 katı {_sy(v['dn'])}")
        s.append("  - " + "; ".join(par) if par else "  - olay yok")
    s += ["", "- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı momentum ve likidite kovasındaki öteki hisselerin ortalaması; "
          "'+%100 katı' = 250 günde +%100'e dokunma olasılığının eşlerinkine oranı (1 = eşlerle aynı). Hayatta kalma: evren bugün işlem gören "
          "hisseler, getiriler yukarı yanlı. Komisyon yok.", ""]
    s += ["## Bilgi alt grupları (karar dışı): çöl süresi (a) ve rüzgâr şiddeti tercilleri (b, c)", "",
          "| Satır | Grup | Hücre | n | eş farkı [%95 alt] | durum | +%100 kat eş [%95] | -%50 kat eş [%95] |", "|---|---|---|---|---|---|---|---|"]
    for sat, G in J["bilgi"].items():
        for k, Jg in G.items():
            for h, v in d9_ozet_satir(Jg).items():
                s.append(f"| {sat} | {k} | {h} | {v['n']} | {_yz(v['fark'])} [{_yz(v['alt'])}] | {v['durum']} | {_sy(v['up'])} [{_sy(v['up_alt'])}, "
                         f"{_sy(v['up_ust'])}] | {_sy(v['dn'])} [{_sy(v['dn_alt'])}, {_sy(v['dn_ust'])}] |")
    s += ["", "Not: AVR için (b) ve (c) 'AVRUPA VERİSİ YOK' (sektör listesi yok); karar en fazla ABD-ADAY.", ""]
    for sat in ("a", "b", "c"):
        s += [J["ana"][sat]["rapor"], ""]
    s += ["## Tercil sınırları (ön kayıttan)", "", "; ".join(f"{p}: {q[0]:.4f} / {q[1]:.4f}" for p, q in J["tercil"].items()), ""]
    metin = "\n".join(s)
    if _D9_EPOSTA.search(metin):
        raise D9Hata("raporda e-posta biçimli parça var")
    with open(_d9_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin)
    return metin


# ================================================================ 10) ÇAKIŞMA KAPISI
def _cakisma_kontrol_d9(_once=_CK_ONCE_D9, _dosya="D9_YENIDEN.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_D9", "_CK_KAYIT", "_cakisma_kontrol_d9", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "warnings", "ast", "_dt", "OC",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_d9()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=D9_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(d9_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = d9_kos(a.cikti, a.veri)
            print(R_["rapor"].split("## Bilgi")[0])
        else:
            print(d9_rapor(a.cikti))
    except (D9Hata, OC.OCHata) as ex:
        d9log.error("%s", ex); sys.exit(1)
