#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
 TEMA SEPETİ × ÇÖL  v2.0  — rüzgârı makine kendi endüstri sepetinden, ERKEN yakalarsa Çöl kırılımı daha mı iyi?
===============================================================================
NEDEN v2 (tek revizyon hakkı — 27 Eyl 2026, Cemal ile KİLİTLENDİ; sonuca bakılıp değiştirilmez):
  v1 (tema_col.py) GEÇMEDİ ve ters çıktı: fon dalgasını yaptıktan sonraki 120 günde gelen Çöl kırılımları, aynı fonun
  diğer kırılımlarından 3–10 puan KÖTÜ. Cemal'in gerekçesi: lider konu çıkar çıkmaz koşmaz — önce çölünü kurar,
  sektör rüzgârı başlayınca uçar. Haberle öğrenmek "herkes konuşurken"e denk gelir (v1'in dalga günü) = geç.
  Yeni temanın fonu çoğu zaman yoktur → rüzgâr hazır fondan değil, HİSSELERDEN KURULAN ENDÜSTRİ SEPETİNDEN ölçülür.
TANIMLAR:
  SEPET        : aynı yfinance endüstrisindeki hisselerin eşit ağırlıklı günlük getirisi (≥ 5 üye; |günlük| > %50 = bozuk veri).
                 Kırılan hisse KENDİ sepetinden ÇIKARILIR (kendi sıçraması rüzgâr sayılmasın).
  ERKEN İŞARET : sepet 20 günde SPY'yi ≥ 5 puan geçti · sepet > SMA200 · önceki 20 işlem gününde işaret yok
                 (ilk yandığı gün = rüzgâr başlangıcı; o güne kadarki kapanışlarla bilinir).
  LİDER KIRILIM: Çöl kırılım günü, sepetin erken işaret başlangıcından sonraki 0–20 işlem günü içinde.
  KARAR        : lider kırılım vs diğer kırılımlar (Çöl resmi ölçümü: islemler_olc, ertesi açılış, 120 bar, %0.4).
                 GEÇME ŞARTI iki ABD setinde birden: (1) beklenti farkı gerçek (OLCUM.kiyas, %90 bandın altı > 0)
                 (2) ≥%30 kazanan oranı ≥ 1.3 kat ve temada ≥ 5 büyük kazanan.  Geçmezse proje KAPANIR.
BİLGİ (karar değil — geriye bakarak çizilir):
  GECİKME  : her sepet dalgası (60 günde ≥ %15, SPY'den ≥ 10 puan önde, SMA200 üstü = "herkes konuşuyor") için gerçek
             başlangıç = dalga gününden önceki 60 günün en düşük kapanışı; oradan erken işarete ve dalga gününe kaç gün.
  EĞRİ     : Çöl kırılımları, rüzgârın gerçek başlangıcından kaç gün sonra geldiklerine göre dilimlenir → beklenti.
  KONTROL  : aynı erken işaret hazır fonlarda (tema_col fon eşlemesi) — sepet fondan iyi mi?
  BUGÜN    : son 20 işlem gününde erken işareti yanan sepetler ve içlerinde çölünü kurmuş hisseler.
UYARI: hisse listesi BUGÜNÜN listesi; geçmişte batmış hisseler sepetlerde yok (sepetleri iyimser gösterir).
BAĞIMLILIK: {K}/tema_col.py (Adım 0, harita, karar birebir oradan) · veri_1d_america.pkl · tema_fon.pkl (SPY) · onbellekler.
FİYAT: sepetler {K}/tema_sepet_fiyat.pkl'den (yfinance, 2019'dan, düzeltilmiş; parti parti, kaldığı yerden sürer).
ÇIKTI ({K}/): tema_sepet.txt · tema_sepet.json · tema_sepet_islemler.csv · tema_sepet_gecikme.csv · tema_sepet_egri.png
              · tema_sepet_bugun.csv · tema_sepet_sepet.pkl (sepet önbelleği; veri değişince yenilenir)
KULLANIM (Colab):  exec(open('/content/drive/MyDrive/col_tarayici/tema_sepet.py').read()); TS = tema_sepet()
Bu bir ölçüm aracıdır, yatırım tavsiyesi değildir.
===============================================================================
"""
from __future__ import annotations
import hashlib, io, json, logging, os, pickle, sys, time, types
from contextlib import redirect_stdout
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

_CK_ONCE = {k: id(v) for k, v in globals().items()}

TS_SURUM = "2026-09-27 v2.1"
TS_K = "/content/drive/MyDrive/col_tarayici"
_ts_log = logging.getLogger("tema_sepet")
if not _ts_log.handlers:
    _ts_h = logging.StreamHandler(sys.stderr)
    _ts_h.setFormatter(logging.Formatter("%(asctime)s │ %(levelname)-7s │ %(message)s", "%H:%M:%S"))
    _ts_log.addHandler(_ts_h); _ts_log.setLevel(logging.INFO)


@dataclass(frozen=True)
class SepetTanim:
    """KİLİTLİ v2 tanımları (tek revizyon). Değiştirilirse sürüm ve gerekçe damgaya yazılır."""
    surum: str = "v2"
    revizyon_gerekce: str = ("Cemal: lider önce çölünü kurar, sektör rüzgârı başlayınca uçar; haberle öğrenmek geç kalır "
                             "(v1: dalga sonrası kırılımlar fon içinde −3/−10 puan kötü). Rüzgâr hisselerden kurulan "
                             "endüstri sepetinden, erken işaretle, makineyle yakalanır.")
    min_uye: int = 5
    getiri_sinir: float = 0.5        # |günlük getiri| > %50 → bozuk veri (NaN)
    erken_gun: int = 20
    erken_fark: float = 5.0          # sepet 20g getirisi − SPY 20g getirisi ≥ 5 puan
    sma: int = 200
    sessiz: int = 20                 # önceki 20 günde işaret yoksa → başlangıç
    pencere: int = 20                # kırılım başlangıçtan sonraki 0..20 işlem günü
    dalga_gun: int = 60              # BİLGİ: "herkes konuşuyor" (v1 dalga tanımı)
    dalga_min: float = 15.0
    dalga_spy_fark: float = 10.0
    dip_gun: int = 60                # BİLGİ: gerçek başlangıç = dalga gününden önceki 60 günün en düşüğü
    buyuk_kazanan: float = 30.0


TS_TANIM = SepetTanim()
TS_EGRI_DILIM = ((0, 10, "0–10"), (10, 20, "10–20"), (20, 40, "20–40"), (40, 60, "40–60"), (60, 120, "60–120"),
                 (120, 250, "120–250"))
TS_YOK = "rüzgâr yok"


# ----------------------------------------------------------------------------- tema_col (birebir yeniden kullanım)
def ts_tc_yukle(K: str) -> types.ModuleType:
    """tema_col.py'yi AYRI modül olarak yükler (oturumu ezmez). Adım 0, harita, karar oradan birebir."""
    yol = os.path.join(K, "tema_col.py")
    if not os.path.exists(yol):
        raise FileNotFoundError(f"{yol} yok — önce tema_col.py kurulmalı")
    m = types.ModuleType("tema_col_ts"); m.__file__ = yol; sys.modules["tema_col_ts"] = m
    with redirect_stdout(io.StringIO()):
        exec(compile(open(yol, encoding="utf-8").read(), yol, "exec"), m.__dict__)
    m.__dict__["_ts_md5"] = hashlib.md5(open(yol, "rb").read()).hexdigest()
    return m


# ----------------------------------------------------------------------------- veri
def _ts_norm(s: Any) -> str:
    s = str(s)
    return s[:-3] if s.upper().endswith(".AM") else s


def ts_veri_ac(VERI: Any) -> Any:
    """col_atilim_TEK önbellek biçimi {"kayit": ..., "veri": {sembol: OHLCV}} → iç sözlük. Düz sözlük/tablo aynen döner."""
    if isinstance(VERI, dict) and isinstance(VERI.get("veri"), dict):
        return VERI["veri"]
    return VERI


def _ts_yapi(VERI: Any) -> str:
    """Hata mesajı için yapının kısa tarifi."""
    try:
        if isinstance(VERI, dict):
            k = list(VERI)[:3]; v = VERI[k[0]] if k else None
            ek = f" · ilk değer {type(v).__name__}" + (f" sütunlar {list(v.columns)[:6]}" if isinstance(v, pd.DataFrame) else
                                                        f" anahtarlar {list(v)[:5]}" if isinstance(v, dict) else "")
            return f"dict ({len(VERI)} anahtar, ilk {k}){ek}"
        if isinstance(VERI, pd.DataFrame):
            return f"DataFrame {VERI.shape} sütunlar {list(VERI.columns)[:6]}"
        return type(VERI).__name__
    except Exception as e:
        return f"tarif edilemedi ({e})"


def ts_kapanis(VERI: Any) -> pd.DataFrame:
    """{sembol: OHLCV} ya da geniş tablo → kapanış matrisi (gün × sembol, sembol .AM'siz, tz'siz, artan tarih)."""
    if isinstance(VERI, pd.DataFrame):
        C = VERI.copy()
    else:
        seri: Dict[str, pd.Series] = {}
        for k, df in VERI.items():
            try:
                if df is None or not len(df):
                    continue
                kol = next((c for c in df.columns if str(c).lower() == "close"), None)
                if kol is None:
                    continue
                s = pd.to_numeric(df[kol], errors="coerce")
                ix = pd.to_datetime(s.index)
                ix = ix.tz_localize(None) if getattr(ix, "tz", None) is not None else ix
                s.index = ix.normalize()
                s = s[~s.index.duplicated(keep="last")].sort_index()
                seri[_ts_norm(k)] = s
            except Exception as e:
                _ts_log.debug("%s atlandı: %s", k, e)
        if not seri:
            raise RuntimeError(f"fiyat verisinde okunabilir 'Close' serisi yok — yapı: {_ts_yapi(VERI)}")
        C = pd.concat(seri, axis=1)
    C.columns = [_ts_norm(c) for c in C.columns]
    C = C.loc[:, ~pd.Index(C.columns).duplicated()].sort_index()
    return C.where(C > 0)


def _ts_yf_indir(liste: List[str], bas: str) -> pd.DataFrame:
    """yfinance toplu indirme → kapanış tablosu (gün × sembol). Düzeltilmiş fiyat (bölünme/temettü) — getiri için doğru olan."""
    import yfinance as yf
    yfad = {x.replace(".", "-"): x for x in liste}                # TradingView BRK.B → yfinance BRK-B
    d = yf.download(list(yfad), start=bas, interval="1d", auto_adjust=True, progress=False, group_by="column", threads=True)
    if d is None or not len(d):
        return pd.DataFrame()
    C = d["Close"] if isinstance(d.columns, pd.MultiIndex) else d[["Close"]].rename(columns={"Close": list(yfad)[0]})
    if isinstance(C, pd.Series):
        C = C.to_frame(list(yfad)[0])
    C = C.rename(columns=lambda c: yfad.get(str(c), str(c)))
    ix = pd.to_datetime(C.index)
    C.index = (ix.tz_localize(None) if getattr(ix, "tz", None) is not None else ix).normalize()
    return C.dropna(how="all")


def ts_uzun_fiyat(K: str, semboller: List[str], bas: str = "2019-01-01", parti: int = 100, indir: Any = None,
                  bayat_gun: int = 5) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Sepetler için UZUN kapanış verisi. {K}/tema_sepet_fiyat.pkl'e PARTİ PARTİ yazar; kesilirse kaldığı yerden sürer.
    Önbellek 'bayat_gun'den eskiyse (ya da başlangıç farklıysa) baştan indirilir. Döner: (C, bilgi)."""
    indir = indir or _ts_yf_indir
    yol = os.path.join(K, "tema_sepet_fiyat.pkl")
    D: Dict[str, Any] = {}
    if os.path.exists(yol):
        try:
            D = pickle.load(open(yol, "rb"))
            yas = (pd.Timestamp.now() - pd.Timestamp(D.get("oturum", "1900-01-01"))).days
            if D.get("bas") != bas or yas > bayat_gun:
                _ts_log.info("fiyat önbelleği bayat/farklı (yaş %s gün) — baştan indirilecek", yas); D = {}
        except Exception as e:
            _ts_log.warning("fiyat önbelleği okunamadı (%s) — baştan", e); D = {}
    if not D:
        D = {"bas": bas, "oturum": str(pd.Timestamp.now()), "bitti": [], "basarisiz": [], "C": pd.DataFrame()}
    bitti = set(D["bitti"]); kalan = [x for x in dict.fromkeys(semboller) if x not in bitti]
    if kalan:
        _ts_log.info("fiyat indiriliyor: %d sembol kaldı (%d hazır), %d'lik partiler", len(kalan), len(bitti), parti)
    t0 = time.monotonic()
    for i in range(0, len(kalan), parti):
        grup = kalan[i:i + parti]; Cp = None
        for deneme in range(2):
            try:
                Cp = indir(grup, bas); break
            except Exception as e:
                _ts_log.warning("parti %d indirilemedi (deneme %d): %s", i // parti + 1, deneme + 1, e); time.sleep(2 * (deneme + 1))
        if Cp is None:
            raise RuntimeError(f"fiyat indirme durdu (parti {i // parti + 1}) — hücreyi yeniden çalıştır, kaldığı yerden sürer")
        Cp = Cp.loc[:, [c for c in Cp.columns if c in grup and Cp[c].notna().sum() > 0]]
        D["C"] = pd.concat([D["C"], Cp], axis=1) if len(D["C"]) else Cp
        D["bitti"] = list(bitti | set(grup)); bitti = set(D["bitti"])
        D["basarisiz"] = sorted(set(D["basarisiz"]) | (set(grup) - set(Cp.columns)))
        tmp = yol + ".tmp"; pickle.dump(D, open(tmp, "wb")); os.replace(tmp, yol)
        _ts_log.info("  parti %d/%d · %d hisse · %.0f sn", i // parti + 1, -(-len(kalan) // parti), D["C"].shape[1], time.monotonic() - t0)
    C = D["C"].sort_index()
    C = C.loc[:, ~C.columns.duplicated()]
    C = C[[c for c in dict.fromkeys(semboller) if c in C.columns]]
    return C.where(C > 0), {"oturum": D["oturum"], "hisse": int(C.shape[1]), "basarisiz": len(D["basarisiz"])}


def ts_getiri(C: pd.DataFrame, T: SepetTanim = TS_TANIM) -> pd.DataFrame:
    R = C.pct_change(fill_method=None)
    return R.where(R.abs() <= T.getiri_sinir)


def ts_sepet(R: pd.DataFrame, H: pd.DataFrame, T: SepetTanim = TS_TANIM) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, List[str]]]:
    """Endüstri başına günlük getiri TOPLAMI (S) ve geçerli üye SAYISI (N). Üyesi < min_uye olan endüstri yok sayılır."""
    uyeler: Dict[str, List[str]] = {}
    e = H["endustri"].astype(str)
    for g, grup in e.groupby(e):
        if g in ("BILINMIYOR", "nan", "None", ""):
            continue
        m = [s for s in grup.index if s in R.columns]
        if len(m) >= T.min_uye:
            uyeler[g] = m
    S = pd.DataFrame({g: R[m].sum(axis=1, min_count=1) for g, m in uyeler.items()}, index=R.index)
    N = pd.DataFrame({g: R[m].notna().sum(axis=1) for g, m in uyeler.items()}, index=R.index)
    return S, N, uyeler


def ts_endeks(b: pd.Series) -> pd.Series:
    """Getiri serisinden endeks (NaN gün = değişim yok)."""
    return (1.0 + b.fillna(0.0)).cumprod()


def ts_erken(I: pd.Series, spy: pd.Series, gecerli: pd.Series, T: SepetTanim = TS_TANIM) -> Tuple[pd.Series, pd.Series]:
    """-> (işaret, başlangıç). Hepsi o güne kadarki değerlerle (rolling/shift, geleceğe bakmaz)."""
    spy = spy.reindex(I.index).ffill()
    fark = ((I / I.shift(T.erken_gun) - 1) - (spy / spy.shift(T.erken_gun) - 1)) * 100
    sma = I.rolling(T.sma, min_periods=T.sma).mean()
    g = gecerli.reindex(I.index).fillna(False).astype(bool)
    isaret = ((fark >= T.erken_fark) & (I > sma) & g & g.shift(T.erken_gun, fill_value=False)).fillna(False).astype(bool)
    onceki = isaret.astype(int).shift(1, fill_value=0).rolling(T.sessiz, min_periods=1).max()
    return isaret, (isaret & (onceki == 0))


def ts_dalga(I: pd.Series, spy: pd.Series, T: SepetTanim = TS_TANIM) -> pd.Series:
    """BİLGİ: v1 dalga tanımı sepete uygulanır ("herkes konuşuyor")."""
    spy = spy.reindex(I.index).ffill()
    r = I / I.shift(T.dalga_gun) - 1; rs = spy / spy.shift(T.dalga_gun) - 1
    sma = I.rolling(T.sma, min_periods=T.sma).mean()
    return ((r * 100 >= T.dalga_min) & ((r - rs) * 100 >= T.dalga_spy_fark) & (I > sma)).fillna(False).astype(bool)


# ----------------------------------------------------------------------------- etiket (kırılan hisse sepetten çıkarılır)
def ts_etiketle(t: pd.DataFrame, H: pd.DataFrame, R: pd.DataFrame, S: pd.DataFrame, N: pd.DataFrame, spy: pd.Series,
                T: SepetTanim = TS_TANIM) -> pd.DataFrame:
    """Her işlem: kırılım gününe kadar, KENDİSİ ÇIKARILMIŞ sepette erken işaret başlangıcı son 0..pencere günde var mı.
    lider = True/False · sepeti olmayan (endüstri bilinmiyor / < min_uye) = NaN (dışarıda)."""
    t = t.copy(); ix = S.index
    boy = T.sma + T.erken_gun + T.sessiz + T.pencere + 10
    lider: List[Optional[bool]] = []; endu: List[Optional[str]] = []; bas_gun: List[Any] = []
    for s, k in zip(t["sembol"], pd.to_datetime(t["kirilim"])):
        n = _ts_norm(s)
        g = str(H["endustri"].get(n)) if n in H.index else None
        endu.append(g)
        if g is None or g not in S.columns:
            lider.append(None); bas_gun.append(None); continue
        ik = ix.searchsorted(k, side="right") - 1
        if ik < boy:
            lider.append(None); bas_gun.append(None); continue
        sl = slice(ik - boy + 1, ik + 1)
        Sg, Ng = S[g].iloc[sl], N[g].iloc[sl]
        if n in R.columns:
            ri = R[n].iloc[sl]
            Sg = Sg - ri.fillna(0.0); Ng = Ng - ri.notna().astype(int)
        ok = Ng >= T.min_uye
        b = (Sg / Ng.where(ok)).where(ok)
        if not bool(ok.iloc[-1]):
            lider.append(None); bas_gun.append(None); continue
        _, bas = ts_erken(ts_endeks(b), spy, ok, T)
        son = bas.iloc[-(T.pencere + 1):]
        lider.append(bool(son.any())); bas_gun.append(son.index[son.values][-1].date() if son.any() else None)
    t["endustri"] = endu; t["lider"] = lider; t["erken_bas"] = bas_gun
    t["tema"] = t["lider"]                                     # tema_col.tc_karar bu sütunu okur
    t["buyuk"] = pd.to_numeric(t["getiri"], errors="coerce") >= T.buyuk_kazanan
    return t


def ts_etiketle_fon(t: pd.DataFrame, H: pd.DataFrame, P: pd.DataFrame, T: SepetTanim = TS_TANIM) -> pd.Series:
    """KONTROL: aynı erken işaret hazır fonda (tema_col eşlemesi). -> True/False/None."""
    bas_fon: Dict[str, pd.Series] = {}
    for f in P.columns:
        if f == "SPY":
            continue
        p = P[f].dropna()
        if len(p) < T.sma + T.erken_gun:
            continue
        _, bas = ts_erken(p, P["SPY"], pd.Series(True, index=p.index), T); bas_fon[f] = bas
    out: List[Optional[bool]] = []
    for s, k in zip(t["sembol"], pd.to_datetime(t["kirilim"])):
        n = _ts_norm(s); f = H["fon"].get(n) if n in H.index else None
        if not isinstance(f, str) or f not in bas_fon:
            out.append(None); continue
        b = bas_fon[f]; ik = b.index.searchsorted(k, side="right") - 1
        out.append(None if ik < 0 else bool(b.iloc[max(0, ik - T.pencere): ik + 1].any()))
    return pd.Series(out, index=t.index, dtype=object)


# ----------------------------------------------------------------------------- BİLGİ: gecikme + eğri (geriye bakarak)
def ts_bolumler(S: pd.DataFrame, N: pd.DataFrame, spy: pd.Series, T: SepetTanim = TS_TANIM) -> pd.DataFrame:
    """Her sepet dalgası: gerçek başlangıç (dip), ilk erken işaret, dalga günü ("herkes konuşuyor") ve aradaki günler."""
    Rw: List[Dict[str, Any]] = []
    for g in S.columns:
        ok = N[g] >= T.min_uye
        I = ts_endeks((S[g] / N[g].where(ok)).where(ok))
        d = ts_dalga(I, spy, T) & ok
        _, bas = ts_erken(I, spy, ok, T)
        dv = d.to_numpy(); bv = bas.to_numpy(); Iv = I.to_numpy(); ix = I.index
        onceki = pd.Series(dv).astype(int).shift(1, fill_value=0).rolling(T.sessiz, min_periods=1).max().to_numpy()
        for e0 in np.where(dv & (onceki == 0))[0]:
            a = max(0, e0 - T.dip_gun); s0 = a + int(np.argmin(Iv[a:e0 + 1]))
            ek = np.where(bv[s0:e0 + 1])[0]
            Rw.append({"endustri": g, "dip": ix[s0].date(), "dalga_gunu": ix[e0].date(),
                       "erken": ix[s0 + ek[0]].date() if len(ek) else None,
                       "gun_dip_erken": int(ek[0]) if len(ek) else np.nan, "gun_dip_dalga": int(e0 - s0),
                       "yukselis_dip_dalga%": float((Iv[e0] / Iv[s0] - 1) * 100)})
    return pd.DataFrame(Rw)


def ts_egri_etiket(t: pd.DataFrame, B: pd.DataFrame, gun_ix: pd.DatetimeIndex) -> pd.Series:
    """Her kırılım: kendi sepetinin en yakın ÖNCEKİ gerçek başlangıcından (dip) kaç işlem günü sonra? -> dilim adı."""
    dipler = {g: np.sort(gun_ix.searchsorted(pd.to_datetime(grp["dip"]))) for g, grp in B.groupby("endustri")} if len(B) else {}
    out: List[str] = []
    for g, k in zip(t["endustri"], pd.to_datetime(t["kirilim"])):
        if not isinstance(g, str) or g not in dipler:
            out.append(TS_YOK); continue
        ik = gun_ix.searchsorted(k, side="right") - 1; d = dipler[g][dipler[g] <= ik]
        if not len(d):
            out.append(TS_YOK); continue
        gun = ik - d[-1]
        out.append(next((ad for a, b, ad in TS_EGRI_DILIM if a <= gun < b), TS_YOK))
    return pd.Series(out, index=t.index)


def ts_grafik(E: pd.DataFrame, genel: Dict[str, float], yol: str) -> bool:
    """Gruplu çubuk: dilim × set beklentisi; kesikli çizgi = setin genel beklentisi. İki set = iki renk + lejant."""
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        _ts_log.warning("matplotlib yok (%s)", e); return False
    dilimler = [ad for *_, ad in TS_EGRI_DILIM] + [TS_YOK]
    setler = list(genel.keys()); renk = ["#2a78d6", "#eb6834"]
    yazi, ikincil, izgara = "#3d3d3a", "#73726c", "#e5e4de"
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=120)
    x = np.arange(len(dilimler)); w = 0.38
    for j, ad in enumerate(setler):
        e = E[E["set"] == ad].set_index("dilim").reindex(dilimler)
        xs = x + (j - 0.5) * w
        ax.bar(xs, e["bek"].fillna(0).values, width=w - 0.03, color=renk[j % 2], label=ad, zorder=2)
        for xi, (v, n) in zip(xs, zip(e["bek"].values, e["n"].values)):
            if np.isfinite(v):
                ax.annotate(f"n={int(n)}", (xi, v), textcoords="offset points", xytext=(0, 3 if v >= 0 else -10),
                            ha="center", fontsize=7, color=ikincil)
        ax.axhline(genel[ad], color=renk[j % 2], lw=1.2, ls="--", zorder=1)
    ax.axhline(0, color="#8f8e88", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(dilimler, color=yazi, fontsize=9)
    ax.set_xlabel("Çöl kırılımı, sepetin gerçek dibinden (rüzgâr başlangıcı) kaç işlem günü sonra", color=yazi, fontsize=9)
    ax.set_ylabel("işlem başı beklenti (%)", color=yazi, fontsize=9)
    ax.grid(axis="y", color=izgara, lw=0.6, zorder=0); ax.tick_params(colors=ikincil, labelsize=8)
    for k in ("top", "right"):
        ax.spines[k].set_visible(False)
    for k in ("left", "bottom"):
        ax.spines[k].set_color(izgara)
    ax.legend(frameon=False, fontsize=8, labelcolor=yazi, loc="upper right")
    ax.set_title("Rüzgâr ne kadar açık kalıyor? — kesikli çizgi: setin tüm kırılımlarının beklentisi (BİLGİ, geriye bakarak)",
                 fontsize=10, color=yazi, loc="left")
    fig.tight_layout(); fig.savefig(yol, facecolor="#ffffff"); plt.close(fig)
    return True


# ----------------------------------------------------------------------------- BUGÜN
def ts_col_durum(df: Optional[pd.DataFrame], ns: Dict[str, Any]) -> Optional[bool]:
    """Bugün çölünü kurmuş ve HENÜZ KIRILMAMIŞ mı? (COL_v1.col_segment, onbellek.py'deki eşiklerle; gerçek OHLCV)."""
    cs = ns.get("col_segment")
    if cs is None or df is None or len(df) < 60:
        return None
    x = df.rename(columns=str.title)[["Open", "High", "Low", "Close", "Volume"]].dropna(subset=["Close"])
    seg = cs(x)
    if not seg or seg.get("uzunluk", 0) < ns.get("MIN_UZ", 20) or seg.get("yukseklik_atr", 99) > ns.get("MAX_YUK", 6):
        return False
    return bool(float(x["Close"].iloc[-1]) <= float(seg["tavan"]) * float(ns.get("AL_PAY", 1.002)))


def ts_bugun(S: pd.DataFrame, N: pd.DataFrame, R: pd.DataFrame, C: pd.DataFrame, uyeler: Dict[str, List[str]], spy: pd.Series,
             ns: Dict[str, Any], T: SepetTanim = TS_TANIM, VERI: Any = None) -> pd.DataFrame:
    """Son 'pencere' işlem gününde erken işareti yanan sepetler; önde gidenler ve ÇÖLÜNÜ KURMUŞ (kırılmamış) üyeler."""
    Rw: List[Dict[str, Any]] = []
    anahtar = {_ts_norm(k): k for k in VERI} if isinstance(VERI, dict) else {}
    son20 = (C.iloc[-1] / C.iloc[-1 - T.erken_gun] - 1) * 100 if len(C) > T.erken_gun else pd.Series(dtype=float)
    for g in S.columns:
        ok = N[g] >= T.min_uye
        I = ts_endeks((S[g] / N[g].where(ok)).where(ok))
        _, bas = ts_erken(I, spy, ok, T)
        son = bas.iloc[-(T.pencere + 1):]
        if not son.any():
            continue
        gun = int(len(son) - 1 - np.where(son.values)[0][-1])
        sp = spy.reindex(I.index).ffill()
        fark = float(((I.iloc[-1] / I.iloc[-1 - T.erken_gun] - 1) - (sp.iloc[-1] / sp.iloc[-1 - T.erken_gun] - 1)) * 100)
        col_l: List[str] = []; bakildi = 0
        for s in uyeler[g]:
            try:
                d = ts_col_durum(VERI[anahtar[s]] if s in anahtar else None, ns)
                bakildi += d is not None
                if d:
                    col_l.append(s)
            except Exception as e:
                _ts_log.debug("çöl durumu %s: %s", s, e)
        ust = son20.reindex(uyeler[g]).dropna().sort_values(ascending=False)
        Rw.append({"endustri": g, "uye": len(uyeler[g]), "isaret_kac_gun_once": gun, "sepet_spy_20g_fark": round(fark, 1),
                   "onde_gidenler_20g": ", ".join(f"{s} {v:+.0f}%" for s, v in ust.head(5).items()),
                   "col_kuranlar": ", ".join(col_l[:10]) if bakildi else "(çöl durumu okunamadı)"})
    return pd.DataFrame(Rw).sort_values("isaret_kac_gun_once") if Rw else pd.DataFrame(Rw)


# ----------------------------------------------------------------------------- ana akış
def _ts_f(x, fmt="+.1f"):
    try:
        return format(float(x), fmt) if np.isfinite(float(x)) else "—"
    except Exception:
        return "—"


def _ts_sepet_onbellek(K: str, C: pd.DataFrame, R: pd.DataFrame, H: pd.DataFrame, T: SepetTanim):
    """Sepetler pahalı değil ama büyük; veri ve harita aynıysa önbellekten döner."""
    anahtar = hashlib.md5((f"{C.shape}{C.index.min()}{C.index.max()}{float(np.nansum(C.iloc[-1].values)):.6f}"
                           f"{len(H)}{T.min_uye}{T.getiri_sinir}").encode()).hexdigest()
    yol = os.path.join(K, "tema_sepet_sepet.pkl")
    if os.path.exists(yol):
        try:
            d = pickle.load(open(yol, "rb"))
            if d.get("anahtar") == anahtar:
                return d["S"], d["N"], d["uyeler"]
        except Exception as e:
            _ts_log.warning("sepet önbelleği okunamadı (%s) — yeniden", e)
    S, N, uy = ts_sepet(R, H, T)
    try:
        tmp = yol + ".tmp"; pickle.dump({"anahtar": anahtar, "S": S, "N": N, "uyeler": uy}, open(tmp, "wb")); os.replace(tmp, yol)
    except OSError as e:
        _ts_log.warning("sepet önbelleği yazılamadı: %s", e)
    return S, N, uy


def tema_sepet(K: str = TS_K, T: SepetTanim = TS_TANIM, n_boot: Optional[int] = None, VERI: Any = None,
               P: Optional[pd.DataFrame] = None, setler: Optional[Dict[str, List[Dict[str, Any]]]] = None,
               beklenen: Optional[Dict[str, Dict[str, float]]] = None, yfinance_ile: bool = True, tc: Any = None,
               indir: Any = None, fiyat_bas: str = "2019-01-01") -> Dict[str, Any]:
    t0 = time.monotonic(); L: List[str] = []; A = L.append
    A("=" * 100); A(f" TEMA SEPETİ × ÇÖL {TS_SURUM} · tanım {T.surum} (tek revizyon)"); A("=" * 100)
    A(f" Gerekçe: {T.revizyon_gerekce}")
    tc = tc or ts_tc_yukle(K)
    ns = tc.tc_yukle(K)
    tc_md5 = tc.__dict__.get("_ts_md5") or (hashlib.md5(open(tc.__file__, "rb").read()).hexdigest()
                                            if getattr(tc, "__file__", None) and os.path.exists(tc.__file__) else None)
    Cd: Dict[str, Any] = {"surum": TS_SURUM, "tanim": asdict(T), "tema_col_md5": tc_md5,
                          "kaynak": ns.get("_tc_kaynak", {})}
    if setler is None:
        setler = {ad: pickle.load(open(os.path.join(K, v["dosya"]), "rb")) for ad, v in tc.TC_TABAN.items()}
    # ---- ADIM 0
    A("\n ADIM 0 — TEMEL: resmi Çöl sayıları (tema_col.tc_adim0, birebir)")
    A0 = tc.tc_adim0(ns, setler, beklenen)
    for ad, s in A0["setler"].items():
        A(f"   {ad:12s} n={s['n']:5d} kazanan %{_ts_f(s['kazanan'], '.1f')} bek {_ts_f(s['bek'], '+.2f')}   "
          f"(resmi %{_ts_f(s['beklenen_kazanan'], '.1f')} / {_ts_f(s['beklenen_bek'], '+.2f')})  -> {'TUTTU' if s['tuttu'] else 'TUTMADI'}")
    Cd["adim0"] = A0["setler"]
    if not A0["gecti"]:
        A("\n ✖ ADIM 0 GEÇMEDİ — DURULDU."); return _ts_bitir(K, L, Cd, t0)
    A("   ✔ ADIM 0 GEÇTİ.")
    # ---- SEPETLER: evren = Çöl setlerindeki + sektör haritasındaki (endüstrisi bilinen) semboller; fiyat UZUN indirme
    ob_semb = {_ts_norm(o.get("sembol")) for OB in setler.values() for o in OB}
    hy = os.path.join(K, "sektor_ABD.csv")
    csv_semb = {_ts_norm(x) for x in pd.read_csv(hy, dtype=str)["sembol"]} if os.path.exists(hy) else set()
    H = tc.tc_harita(K, sorted(ob_semb | csv_semb), yfinance_ile=yfinance_ile)
    evren = sorted(x for x in H.index if str(H.at[x, "endustri"]) not in ("BILINMIYOR", "nan", "None", ""))
    C, fb = ts_uzun_fiyat(K, evren, bas=fiyat_bas, indir=indir)
    Cd["fiyat"] = fb
    R = ts_getiri(C, T)
    P = P if P is not None else tc.tc_fonlar(K)
    spy = P["SPY"].reindex(C.index).ffill()
    gerek_bas = min(pd.to_datetime(t["kirilim"]).min() for t in A0["islemler"].values() if len(t)) - pd.offsets.BDay(T.sma + 80)
    say = C.notna().sum(axis=1); kapsam_bas = say.index[say >= 0.5 * say.max()].min()   # hisselerin yarısının verisi olduğu ilk gün
    A(f"\n SEPETLER: evren {len(evren)} hisse (endüstrisi bilinen) · fiyatı gelen {C.shape[1]} · indirilemeyen {fb['basarisiz']} · "
      f"{C.index.min().date()} → {C.index.max().date()} (hisselerin yarısı {kapsam_bas.date()}'den beri)")
    if kapsam_bas > gerek_bas:
        A(f"   ✖ hisselerin çoğunun verisi {gerek_bas.date()} öncesine gitmiyor — ilk kırılımlar için SMA200 kurulamaz. DURULDU.")
        return _ts_bitir(K, L, Cd, t0)
    if VERI is None:                                           # yalnız BUGÜN listesindeki çöl durumu (gerçek OHLC) için
        yol = os.path.join(K, "veri_1d_america.pkl")
        try:
            VERI = pickle.load(open(yol, "rb")) if os.path.exists(yol) else None
        except Exception as e:
            _ts_log.warning("veri_1d_america.pkl okunamadı (%s) — BUGÜN listesinde çöl durumu olmayacak", e); VERI = None
    VERI = ts_veri_ac(VERI) if VERI is not None else None
    S, N, uyeler = _ts_sepet_onbellek(K, C, R, H, T)
    A(f"   {len(uyeler)} endüstri sepeti (≥ {T.min_uye} üye) · toplam {sum(len(v) for v in uyeler.values())} üye · "
      f"endüstrisi bilinmeyen/küçük sepetteki hisse dışarıda")
    A("   UYARI: liste bugünün listesi — batmış hisseler yok (sepetleri iyimser gösterir).")
    Cd["sepet"] = {"hisse": int(C.shape[1]), "sepet": len(uyeler), "bas": str(C.index.min().date()), "son": str(C.index.max().date())}
    # ---- BİLGİ 1: gecikme
    B = ts_bolumler(S, N, spy, T)
    A("\n BİLGİ 1 — NE KADAR GEÇ ÖĞRENİYORUZ? (geriye bakarak; gerçek başlangıç = dalga gününden önceki 60 günün dibi)")
    if len(B):
        de, dd = B["gun_dip_erken"].dropna(), B["gun_dip_dalga"]
        A(f"   {len(B)} sepet dalgası · dipten 'herkes konuşuyor' gününe: medyan {dd.median():.0f} işlem günü "
          f"(çeyrekler {dd.quantile(.25):.0f}–{dd.quantile(.75):.0f}), bu sürede sepet medyan %{B['yukselis_dip_dalga%'].median():.0f} yükselmiş")
        A(f"   makinenin erken işareti dalgaların %{100 * B['gun_dip_erken'].notna().mean():.0f}'inde dalga gününden önce yandı · "
          f"dipten erken işarete medyan {de.median():.0f} gün (çeyrekler {de.quantile(.25):.0f}–{de.quantile(.75):.0f})" if len(de) else
          "   erken işaret hiçbir dalgada dalga gününden önce yanmadı")
    else:
        A("   dalga bulunamadı")
    # ---- KARAR
    TS = {ad: ts_etiketle(A0["islemler"][ad], H, R, S, N, spy, T) for ad in setler}
    for ad in TS:
        TS[ad]["lider_fon"] = ts_etiketle_fon(TS[ad], H, P, T)
        TS[ad]["egri"] = ts_egri_etiket(TS[ad], B, C.index)
    KR = tc.tc_karar(ns, TS, n_boot=n_boot)
    A(f"\n KARAR — LİDER KIRILIM: kırılım, kendi sepetinin (kendisi çıkarılmış) erken işaret başlangıcından sonraki 0–{T.pencere} gün içinde")
    for ad, s in KR["setler"].items():
        ot, og, fb = s["olcu_tema"], s["olcu_gerisi"], s["bek_fark"]
        A(f"\n   [{ad}] işlem {s['n']} · ölçülen {s['n_olculen']} · dışarıda (sepet yok) {s['n_disari']}")
        A(f"     lider kırılım   n={s['n_tema']:5d} kazanan %{_ts_f(ot.get('kazanan%'), '.0f')} bek {_ts_f(ot.get('bek'))} ağır %{_ts_f(ot.get('agir%'), '.0f')} · büyük (≥%30) %{_ts_f(s['buyuk_tema%'], '.1f')}")
        A(f"     diğerleri       n={s['n_gerisi']:5d} kazanan %{_ts_f(og.get('kazanan%'), '.0f')} bek {_ts_f(og.get('bek'))} ağır %{_ts_f(og.get('agir%'), '.0f')} · büyük (≥%30) %{_ts_f(s['buyuk_gerisi%'], '.1f')}")
        A(f"     bek farkı " + (f"{fb[0]:+.1f} [%90 bant {fb[1]:+.1f}, {fb[2]:+.1f}]" if fb else "—") +
          f"  -> şart 1 {'✔' if s['sart1'] else '✖'} · büyük kazanan oranı {_ts_f(s['buyuk_oran'], '.2f')} kat -> şart 2 {'✔' if s['sart2'] else '✖'}")
    # KONTROL (bilgi): hazır fonlar
    TF = {ad: t.assign(tema=t["lider_fon"]) for ad, t in TS.items()}
    KF = tc.tc_karar(ns, TF, n_boot=n_boot)
    A("\n   KONTROL (bilgi) — aynı erken işaret HAZIR FONDA:")
    for ad, s in KF["setler"].items():
        fb = s["bek_fark"]
        A(f"     [{ad}] fon işareti n={s['n_tema']} · bek farkı " + (f"{fb[0]:+.1f} [{fb[1]:+.1f}, {fb[2]:+.1f}]" if fb else "—") +
          f" · büyük oranı {_ts_f(s['buyuk_oran'], '.2f')} kat")
    # ---- BİLGİ 2: eğri
    E_: List[Dict[str, Any]] = []; genel: Dict[str, float] = {}
    for ad, t in TS.items():
        g = pd.to_numeric(t["getiri"], errors="coerce"); genel[ad] = float(g.mean())
        for d, grp in t.groupby("egri"):
            gg = pd.to_numeric(grp["getiri"], errors="coerce")
            E_.append({"set": ad, "dilim": d, "n": int(len(gg)), "bek": float(gg.mean()), "buyuk%": float(100 * (gg >= T.buyuk_kazanan).mean())})
    E = pd.DataFrame(E_)
    A("\n BİLGİ 2 — RÜZGÂR NE KADAR AÇIK KALIYOR? (kırılım, sepetin gerçek dibinden kaç gün sonra · geriye bakarak)")
    dil = [ad for *_, ad in TS_EGRI_DILIM] + [TS_YOK]
    A("   dilim (gün)   " + "   ".join(f"{ad:>28s}" for ad in TS))
    for d in dil:
        hucre = []
        for ad in TS:
            r = E[(E["set"] == ad) & (E["dilim"] == d)]
            hucre.append(f"n={int(r['n'].iloc[0]):4d} bek {_ts_f(r['bek'].iloc[0]):>6s} büyük %{_ts_f(r['buyuk%'].iloc[0], '.0f'):>3s}" if len(r) else f"{'—':>28s}")
        A(f"   {d:12s}  " + "   ".join(f"{h:>28s}" for h in hucre))
    A("   genel        " + "   ".join(f"{'bek ' + _ts_f(genel[ad]):>28s}" for ad in TS))
    png = ts_grafik(E, genel, os.path.join(K, "tema_sepet_egri.png")) if len(E) else False
    # ---- KARAR metni
    A("\n" + "#" * 100)
    if KR["gecti"]:
        A(" KARAR: GEÇTİ — iki ABD setinde de sepetin erken işaretinden sonraki 20 günde gelen Çöl kırılımları")
        A("        beklentide gerçekten iyi VE büyük kazanan oranı ≥ 1.3 kat. Sonraki: günlük taramaya 'rüzgâr' sütunu + kâğıt defteri.")
    else:
        A(" KARAR: GEÇMEDİ")
        for n_ in KR["neden"]:
            A(f"   · {n_}")
        A(" Revizyon hakkı kullanıldı (v2). Kural gereği Tema × Çöl KAPANIR; Çöl bugünkü haliyle devam eder.")
    A("#" * 100)
    Cd["karar"] = "GEÇTİ" if KR["gecti"] else "GEÇMEDİ"; Cd["neden"] = KR["neden"]
    Cd["karar_set"] = {ad: {k: (list(v) if isinstance(v, tuple) else v) for k, v in s.items()} for ad, s in KR["setler"].items()}
    Cd["kontrol_fon"] = {ad: {"n": s["n_tema"], "bek_fark": list(s["bek_fark"]) if s["bek_fark"] else None, "buyuk_oran": s["buyuk_oran"]}
                         for ad, s in KF["setler"].items()}
    # ---- BUGÜN
    try:
        BG = ts_bugun(S, N, R, C, uyeler, spy, ns, T, VERI)
    except Exception as e:
        _ts_log.error("bugün listesi kurulamadı: %s", e); BG = pd.DataFrame()
    A(f"\n BUGÜN ({C.index.max().date()}) — son {T.pencere} işlem gününde erken işareti yanan sepetler "
      f"(test sonucu: {Cd['karar']} — geçmediyse yalnız bilgi)")
    if len(BG):
        for _, r in BG.iterrows():
            A(f"   {r['endustri'][:34]:34s} {r['isaret_kac_gun_once']:2d} gün önce · 20g SPY'den {r['sepet_spy_20g_fark']:+.1f} puan · {r['uye']} üye")
            A(f"      önde: {r['onde_gidenler_20g']}")
            A(f"      çölünü kurmuş: {r['col_kuranlar'] or '—'}")
    else:
        A("   yok")
    Cd["bugun"] = BG.to_dict("records") if len(BG) else []
    try:
        pd.concat([t.assign(set=ad) for ad, t in TS.items()]).to_csv(os.path.join(K, "tema_sepet_islemler.csv"), index=False)
        B.to_csv(os.path.join(K, "tema_sepet_gecikme.csv"), index=False)
        BG.to_csv(os.path.join(K, "tema_sepet_bugun.csv"), index=False)
    except OSError as e:
        _ts_log.error("CSV yazılamadı: %s", e)
    return _ts_bitir(K, L, Cd, t0, TS, B, E, png)


def _ts_bitir(K, L, Cd, t0, TS=None, B=None, E=None, png=False) -> Dict[str, Any]:
    L.append(f"\n  -> {K}/tema_sepet.txt · tema_sepet.json" +
             (" · tema_sepet_islemler.csv · tema_sepet_gecikme.csv · tema_sepet_bugun.csv" if TS else "") +
             (" · tema_sepet_egri.png" if png else "") + f"   ({time.monotonic() - t0:.0f} sn)")
    txt = "\n".join(L); print(txt)
    try:
        open(os.path.join(K, "tema_sepet.txt"), "w", encoding="utf-8").write(txt)
        json.dump(Cd, open(os.path.join(K, "tema_sepet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    except OSError as e:
        _ts_log.error("çıktı yazılamadı: %s", e)
    return {"ozet": txt, "damga": Cd, "islemler": TS, "gecikme": B, "egri": E}


def _cakisma_kontrol_ts(_once=_CK_ONCE, _dosya='tema_sepet.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE', '_CK_KAYIT', '_cakisma_kontrol', '_cakisma_kontrol_ts', 'In', 'Out', '_', '_i', '_ii', '_iii',
            'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'io', 'time', 'json', 'hashlib', 'pickle', 'logging', 'types', 'redirect_stdout', 'annotations',
           'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'asdict')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")
_cakisma_kontrol_ts()
print(f"[ok] tema_sepet {TS_SURUM} (tanım {TS_TANIM.surum}) — TS = tema_sepet()")
