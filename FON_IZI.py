# =====================================================================
#  FON_IZI — tasfiye fonlarinin topladigi hisselerin yukselis oncesi/sirasi izi   (2026-10-23, v1.2)
#
#  CEMAL (22 Eki): "Fonlar Eylul'e kadar onca alis yapmis, hisseler yuzde bin yukselmis; o para girisi nasil bir iz birakti?
#    Benim dusuncem: balina girisi zamanina denk gelen bolgede kucuk mum ve ufak ufak yukari yuvarlanma. TEHOL, TERA, PASEU,
#    HEDEF... bunlara bak, bu iz nedir? Bu bize buyuk bir ders verir."
#  VAKA LISTESI (FON_HISSE): tasfiye fonlarinin fiili dolasimda en buyuk paya sahip oldugu hisseler (borsaningundemi / hisse.net
#    18 Eyl 2026: TEHOL %77,7 ANELE %68,1 TRHOL %60,1 OZATD %57,5 PEKGY %54,7 IEYHO %43,1 DSTKF %34,5 ISKPL %26,4 SELEC %20,6
#    BIGEN %20,2) + COL_v1 FON_BILINEN (KTLEV GUNDG PASEU ODINE HEDEF TERA IZFAS LIDER) + taban serisine giren ALKLC UFUK PRZMA
#    BINBN DURDO. Cemal'in "Ata" dedigi hisse (ATATR?) veride yok.
#  VERI: BIST fiyatlari ham (auto_adjust=False). K1, BIST'te gunluk sinirin (2020-03 sonrasi %10, oncesi %20) otesindeki
#    sicramalari bolunme/bedelsiz sayar ve geriye dogru carpanla duzeltir (hacim ters carpanla).
#  FAZLAR (vaka): dip = tepe oncesi 900 gundeki en dusuk kapanis; ONCE = dipten onceki 120 bar; ERKEN = dip -> fiyatin ilk 2 kati;
#    KOSU = 2 kat -> tepe (15 Eyl 2026 oncesi en yuksek kapanis); COKUS = tepe -> bugun.
#  IZ OLCULERI (son W=60 bar, gercek zamanli): g = 60 bar getiri; taban = gunluk <= -%9,5 gun sayisi; tavan = >= +%9,5;
#    dd = pencere icindeki en derin geri cekilme; mk = pencere medyan mum boyu (H-L / onceki kapanis) / AYNI hissenin onceki
#    250 bar medyani (k < 1 = mumlar kendi gecmisine gore kuculdu); verim = net log getiri / gunluk log hareketlerin toplami;
#    tlk = son 60 bar TL hacim medyani / onceki 60 bar; r2 = son 120 barda log fiyatin dogruya uyumu (grafikteki duz cizgi kosu).
#  EVREN TESTI: olay = 60 barda +%30..+%100 yukselmis hisse (ayni hissede 60 bar icinde bir kez); IZ varyantlari bu olaylarin alt
#    kumesi, TABAN = ayni yukselisin izi tasimayan geri kalani. Sonuc: 250 bar icinde once 2 kat mi (High) once -%30 mu (Low);
#    250 bar sonraki getiri; 250 bardaki en yuksek / giris. Iz = 4 dilimde (BIST/ABD x 2016-21/2022-26) kat >= 1,3.
#  v1.1 (23 Eki) HACIM ESLIGI. CEMAL: "Hacmine eslik edenlere ayrica bak; balina girisine denk gelen bolgede kucuk mum ve ufak ufak
#    yukari yuvarlanma olur, o bolgeleri net goremedik." SESSIZ YUVARLANMA bolgesi (Z0, son hW=20 bar): +%5..+%30 yukselis, medyan
#    mum hissenin kendi 250 bar normalinin <= 0,85'i, verim >= 0,3, taban gunu yok, geri cekilme >= -%10. Bolge icindeki hacim:
#    hk = hacim medyani / kendi 250 bar normali; udvr = yukselis gunu hacmi / dusus gunu hacmi; dh = dusus gunu ort. hacmi / yukselis
#    gunu ort. hacmi; emilim = hk / mum kucuklugu (caba-sonuc: hacim buyuk, mum kucuk); emilim_gun = hacim >= 1,5 normal VE mum <= 0,8
#    normal olan gun sayisi; vcv = hacim degiskenlik katsayisi. K3b: fon hisselerinin dip->tepe donemindeki Z0 bolgeleri ile diger
#    BIST hisselerinin 2024-26 Z0 bolgeleri karsilastirilir. K4b: evrende Z0 olaylari (ayni hissede 20 bar icinde bir kez), hacim
#    varyantlari Z0'in hacim izi tasimayan kismina karsi; sonuc 250 barda once 2 kat / -%30 ve 60 barda once +%20 / -%10.
#  v1.2 (23 Eki) GOSTERGE BATARYASI. CEMAL: "Iz yok diyorsun ama hisseler alindi; yalniz mum ve hacme bakma, her gostergeye
#    bak: ters uyumsuzluk, Fibonacci, hepsi." K6: 40+ gosterge (RSI, Stokastik, Williams %R, CCI, MFI, CMF, OBV, A/D, MACD, ADX/DI,
#    Aroon, Bollinger %B + genislik, Keltner sikismasi, Ichimoku, SMA50/200, ROC, ATR%, Force, Ulcer, Fibonacci konum/geri cekilme)
#    + pivot tabanli UYUMSUZLUK (duz/gizli boga, ayi; RSI, MACD hist, OBV, MFI, CMF; pivot p+-k barin en dusugu/yuksegi, sinyal
#    pivotun dogrulandigi p+k gununde -> gelecege bakmaz). K7 BLOK HACIM: hacim >= 20x onceki 20 gun medyani (OZATD 14 May 2026:
#    fonlar tek gunde 13,6 mn lot, komsu kilitli tavan gunlerinde ~0,1 mn; onceki olculer kilitli O=H=L=C gunlerini disliyordu).
#    K8 KAP OLAYLARI (BIST, 2017-26, kap_ozet konu kodlari): VBTS/BISTECH tedbiri, borsada islem goren tipe donusum, toptan alis
#    satis, pay alim satim bildirimi, devre kesici, olagan disi fiyat, SPK islem yasagi, fiili dolasim degisikligi, piyasa yapicilik,
#    soylenti aciklamasi. Saat 18:00 sonrasi bildirim ertesi islem gunune sayilir. K6a fon hisselerinde faz basina 100 gunde sinyal
#    sikligi vs diger BIST (2024-26); K6b evren: her sinyal (ayni hissede 20 bar icinde bir kez) vs her 5. gun tabani; sonuc 60 bar
#    once +%20/-%10 (k20), 250 bar once 2 kat/-%30 (x2), 60 bar once -%20/+%20 (dus). Iz = 4 dilimde kat >= 1,3 (KAP yalniz BIST: 2 dilim).
#  KURAL_MOTORU: K1 veri+duzeltme  K2 gunluk/pencere olculeri  K3 vaka fazlari  K4 evren olaylari + ozet  K5 rapor
#                K6 gosterge/uyumsuzluk/Fibonacci  K7 blok hacim  K8 KAP olaylari (v1.2: fon_izi_gosterge)
#  Calistirma: FI_VERI_BIST=... FI_VERI_ABD=... python FON_IZI.py   (v1.2: ... FI_KAP=<kap_ozet klasoru> python FON_IZI.py gosterge)
#  Cikti: arastirma_cikti/fon_izi/
# =====================================================================
from __future__ import annotations

import logging
import os
import pickle
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_FI = {k: id(v) for k, v in globals().items()}

FI_SURUM = "FON_IZI v1.2 (2026-10-23, yukselis izi + hacim esligi + gosterge/uyumsuzluk/Fibonacci/blok hacim/KAP)"
filog = logging.getLogger("col.fon_izi")
if not filog.handlers:
    _fi_h = logging.StreamHandler(sys.stderr)
    _fi_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s fon_izi: %(message)s", "%H:%M:%S"))
    filog.addHandler(_fi_h)
    filog.setLevel(logging.INFO)
    filog.propagate = False

FON_HISSE = ["TEHOL", "ANELE", "TRHOL", "OZATD", "PEKGY", "IEYHO", "DSTKF", "ISKPL", "SELEC", "BIGEN", "KTLEV", "GUNDG",
             "PASEU", "ODINE", "HEDEF", "TERA", "IZFAS", "LIDER", "ALKLC", "UFUK", "PRZMA", "BINBN", "DURDO"]


@dataclass
class FIAyar:
    W: int = 60
    normal: int = 250
    normal_min: int = 120
    limit_tarih: str = "2020-03-01"
    limit_yeni: float = 0.105       # BIST gunluk sinir %10 (sonrasi); otesi sicrama = bolunme/bedelsiz
    limit_eski: float = 0.21
    sinir_gun: float = 0.095        # tavan/taban gunu esigi (her iki pazarda sabit)
    kriz_tarih: str = "2026-09-15"  # fon tasfiye cokusu oncesi tepe arama siniri
    dip_gun: int = 900
    g_alt: float = 0.30
    g_ust: float = 1.00
    ufuk: int = 250
    hedef_kat: float = 2.0
    zarar: float = 0.30
    tekrar: int = 60
    donem_siniri: str = "2022-01-01"
    # v1.1 hacim esligi
    hW: int = 20
    z0_g: Tuple[float, float] = (0.05, 0.30)
    z0_mk: float = 0.85
    z0_verim: float = 0.30
    z0_dd: float = -0.10
    hacim_tekrar: int = 20
    hacim_bas: str = "2024-01-01"   # K3b diger hisseler karsilastirma donemi baslangici (bitis kriz_tarih)
    # v1.2 gosterge bataryasi
    piv_k: int = 5                  # uyumsuzluk pivotu: p-k..p+k araliginin en dusugu/yuksegi; sinyal p+k gunu
    piv_ara: int = 60               # iki pivot arasi en fazla bar
    g_tekrar: int = 20              # ayni hissede ayni sinyal 20 bar icinde bir kez
    ornek_adim: int = 5             # taban: her 5. gun
    blok_kat: float = 20.0          # blok hacim: onceki 20 gun medyaninin 20 kati
    once_bar: int = 120             # fon vakasi ONCE fazi (dipten onceki bar)
    kap: str = os.environ.get("FI_KAP", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kap_ozet")
    # v1.3 fon islem defteri (KAP portfoy dagilim raporlari)
    kapfon: str = os.environ.get("FI_KAPFON", "/content/drive/MyDrive/COLAB_VERILER/col_tarayici/kapfon")
    kapfon_bas: str = "2023-01-01"
    kapfon_bit: str = "2026-10-20"
    kapfon_gun: int = 15            # rapor ayin ilk 6 is gunu icinde yayimlanir; ayin 1-15'i taranir
    kapfon_bekle: float = 0.3       # KAP'a nezaket beklemesi (sn)
    veri: Dict[str, str] = field(default_factory=lambda: {
        "BIST": os.environ.get("FI_VERI_BIST", "/content/drive/MyDrive/col_tarayici/veri_1d_turkey.pkl"),
        "ABD": os.environ.get("FI_VERI_ABD", "/content/drive/MyDrive/col_tarayici/veri_1d_america.pkl"),
    })
    cikti: str = "arastirma_cikti/fon_izi"


# ---------------------------------------------------------------- K1 veri
def fi_duzelt(d: pd.DataFrame, A: FIAyar) -> Tuple[pd.DataFrame, int]:
    """BIST ham fiyat: gunluk siniri asan sicramalari geriye dogru carpanla duzeltir. Donus: (duzeltilmis, sicrama sayisi)."""
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float).copy()
    oran = d.Close / d.Close.shift()
    lim = np.where(d.index >= pd.Timestamp(A.limit_tarih), A.limit_yeni, A.limit_eski)
    kir = (oran - 1).abs() > lim
    carp = oran.where(kir, 1.0)[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
    for c in ("Open", "High", "Low", "Close"):
        d[c] = d[c] * carp
    d["Volume"] = d.Volume / carp
    return d, int(kir.sum())


def fi_k1_veri(yol: str, pazar: str, A: FIAyar) -> Dict[str, pd.DataFrame]:
    if not os.path.exists(yol):
        raise FileNotFoundError(f"veri yok: {yol}")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    out = {}
    for s, d in V.items():
        try:
            if "Volume" not in d.columns:
                continue
            d = d.dropna(subset=["Open", "High", "Low", "Close"])
            d = d[(d.High >= d.Low) & (d.Close > 0)].sort_index()
            if pazar == "BIST":
                d, _ = fi_duzelt(d, A)
            else:
                d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
            if len(d) >= 150:
                out[str(s)] = d
        except Exception as ex:  # tek hisse bozuksa digerleri devam eder
            filog.warning("%s atlandi: %s", s, ex)
    filog.info("%s %s: %d hisse", pazar, yol, len(out))
    return out


# ---------------------------------------------------------------- K2 olculer
def fi_gunluk(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    pc = d.Close.shift(); r = d.Close / pc - 1; hl = (d.High - d.Low).replace(0, np.nan); v = d.Volume.replace(0, np.nan)
    return pd.DataFrame({"r": r, "rng": (d.High - d.Low) / pc, "up": (r > 0).astype(float),
                         "tavan": (r >= A.sinir_gun).astype(float), "taban": (r <= -A.sinir_gun).astype(float),
                         "clv": (d.Close - d.Low) / hl, "govde": (d.Close - d.Open).abs() / hl,
                         "gapup": (d.Open / pc - 1 > 0.01).astype(float),
                         "vk": v / v.rolling(60, min_periods=30).median().shift(), "tl": np.log10(d.Close * d.Volume + 1)})


def fi_pencere(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """Son W bar iz olculeri (gercek zamanli)."""
    W = A.W; c = d.Close; pc = c.shift(); r = c / pc - 1; rng = (d.High - d.Low) / pc
    net = np.log(c / c.shift(W)); yol = np.log(c / pc).abs().rolling(W).sum()
    tl = c * d.Volume
    return pd.DataFrame({"g": c / c.shift(W) - 1,
                         "taban": (r <= -A.sinir_gun).astype(int).rolling(W).sum(),
                         "tavan": (r >= A.sinir_gun).astype(int).rolling(W).sum(),
                         "dd": (c / c.rolling(W).max() - 1).rolling(W).min(),
                         "mk": rng.rolling(W).median() / rng.shift(W).rolling(A.normal, min_periods=A.normal_min).median(),
                         "verim": net / yol,
                         "tlk": tl.rolling(W).median() / tl.shift(W).rolling(W).median(),
                         "r2": _fi_r2(np.log(c), 2 * W)})


def _fi_r2(y: pd.Series, n: int) -> pd.Series:
    """Son n barda log fiyatin zamana dogrusal uyumu (R^2): 1'e yakin = dumduz cizgi yukselis (grafikteki 'merdiven')."""
    x = pd.Series(np.arange(len(y), dtype=float), index=y.index)
    cxy = (x * y).rolling(n).mean() - x.rolling(n).mean() * y.rolling(n).mean()
    vx = x.rolling(n).var(ddof=0); vy = y.rolling(n).var(ddof=0)
    return (cxy ** 2 / (vx * vy)).where(vy > 0)


def fi_izler(Z: pd.DataFrame) -> Dict[str, pd.Series]:
    """Vaka fazlarindan cikan izler (sabit esikler) ve birlesimleri."""
    tb = Z.taban == 0; dd = Z.dd >= -0.20; mk = Z.mk < 1.0; ve = Z.verim >= 0.25; tl = Z.tlk >= 1.5; tv = Z.tavan >= 3
    return {"taban_yok": tb, "sig_geri": dd, "mum_kucul": mk, "verim": ve, "tl_artis": tl, "tavan3": tv,
            "A_tb_dd_mk": tb & dd & mk, "B_A_verim": tb & dd & mk & ve, "C_A_tl": tb & dd & mk & tl,
            "D_tb_dd_ve_tl": tb & dd & ve & tl, "E_tek_yon": tv & tb,
            "F_duz_cizgi": (Z.r2 >= 0.85) & tb, "G_duz_cizgi_sig": (Z.r2 >= 0.85) & tb & dd}


def fi_hacim_olc(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """v1.1: son hW barin sessiz yuvarlanma (Z0) bayragi ve hacim esligi olculeri (gercek zamanli)."""
    W = A.hW; c = d.Close; pc = c.shift(); r = c / pc - 1; rng = (d.High - d.Low) / pc; v = d.Volume.replace(0, np.nan)
    up = r > 0; dn = r < 0
    mr = rng.shift(W).rolling(A.normal, min_periods=A.normal_min).median()
    mv = v.shift(W).rolling(A.normal, min_periods=A.normal_min).median()
    o = pd.DataFrame(index=d.index)
    o["g"] = c / c.shift(W) - 1
    o["mk"] = rng.rolling(W).median() / mr
    o["verim"] = np.log(c / c.shift(W)) / np.log(c / pc).abs().rolling(W).sum()
    o["taban"] = (r <= -A.sinir_gun).astype(int).rolling(W).sum()
    o["dd"] = (c / c.rolling(W).max() - 1).rolling(W).min()
    o["udvr"] = v.where(up, 0).rolling(W).sum() / v.where(dn, 0).rolling(W).sum()
    o["hk"] = v.rolling(W).median() / mv
    o["emilim"] = o.hk / o.mk
    o["vcv"] = v.rolling(W).std() / v.rolling(W).mean()
    o["dh"] = v.where(dn).rolling(W, min_periods=3).mean() / v.where(up).rolling(W, min_periods=3).mean()
    o["emilim_gun"] = ((v / mv >= 1.5) & (rng / mr <= 0.8)).astype(int).rolling(W).sum()
    o["Z0"] = ((o.g >= A.z0_g[0]) & (o.g <= A.z0_g[1]) & (o.mk <= A.z0_mk) & (o.verim >= A.z0_verim)
               & (o.taban == 0) & (o.dd >= A.z0_dd))
    return o


def fi_hacim_varyant(O: pd.DataFrame) -> Dict[str, pd.Series]:
    """v1.1 hacim varyantlari (sabit esikler; K3b'deki fon/diger farkinin yonune gore)."""
    return {"hacim_kuru": O.hk <= 0.6, "yukari_hacim": O.udvr >= 2.5, "kuru_ve_yukari": (O.hk <= 0.6) & (O.udvr >= 2.5),
            "emilim": O.emilim >= 1.5, "emilim_gun": O.emilim_gun >= 2, "dusus_hacmi_kuru": O.dh <= 0.6, "hacim_artan": O.hk >= 1.5}


_FI_HKOL = ["udvr", "hk", "emilim", "vcv", "dh", "emilim_gun", "mk", "g"]


def fi_k3b_hacim_vaka(V: Dict[str, pd.DataFrame], kos: pd.DataFrame, A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, pd.Series]]:
    """Fon hisselerinin dip->tepe donemindeki Z0 bolgeleri vs diger BIST hisselerinin ayni yillardaki Z0 bolgeleri."""
    fon, diger, zbayrak = [], [], {}
    kosd = kos.set_index("sembol")
    a0, b0 = pd.Timestamp(A.hacim_bas), pd.Timestamp(A.kriz_tarih)
    for s, d in V.items():
        try:
            o = fi_hacim_olc(d, A)
            if s in kosd.index:
                k = kosd.loc[s]; zbayrak[s] = o.Z0
                o = o.loc[k.dip:k.tepe].assign(sembol=s); fon.append(o)
            else:
                diger.append(o.loc[a0:b0].assign(sembol=s))
        except Exception as ex:
            filog.warning("hacim %s atlandi: %s", s, ex)
    Fo = pd.concat(fon); Do = pd.concat(diger)
    ozet = pd.DataFrame({"fon_Z0": Fo[Fo.Z0][_FI_HKOL].median(), "diger_Z0": Do[Do.Z0][_FI_HKOL].median(),
                         "fon_tum": Fo[_FI_HKOL].median(), "diger_tum": Do[_FI_HKOL].median()})
    ozet.loc["Z0_gun_orani_%"] = [Fo.Z0.mean() * 100, Do.Z0.mean() * 100, np.nan, np.nan]
    ozet.loc["Z0_hisse_medyan_%"] = [Fo.groupby("sembol").Z0.mean().median() * 100, Do.groupby("sembol").Z0.mean().median() * 100, np.nan, np.nan]
    hisse = Fo[Fo.Z0].groupby("sembol")[["udvr", "hk", "emilim", "dh", "emilim_gun", "mk"]].median()
    hisse["Z0_gun"] = Fo.groupby("sembol").Z0.sum()
    return ozet.reset_index().rename(columns={"index": "olcu"}), hisse.reset_index(), zbayrak


# ---------------------------------------------------------------- K3 vaka fazlari
def fi_kosu(d: pd.DataFrame, A: FIAyar) -> Optional[Dict[str, Any]]:
    c = d.Close[d.index < pd.Timestamp(A.kriz_tarih)]
    if len(c) < 30:
        return None
    tepe = c.idxmax(); onc = c.loc[:tepe]; dip = onc[onc.index >= tepe - pd.Timedelta(days=A.dip_gun)].idxmin()
    yol = c.loc[dip:tepe]; x2 = yol[yol >= c[dip] * 2].index
    return {"dip": dip, "x2": x2[0] if len(x2) else None, "tepe": tepe, "kat": float(c[tepe] / c[dip]), "bar": len(yol)}


def fi_faz_olc(d: pd.DataFrame, g: pd.DataFrame, rng_yzd: pd.Series, tl_yzd: pd.Series, a, b) -> Dict[str, float]:
    gg = g.loc[a:b]; c = d.Close.loc[a:b]
    if len(gg) < 5:
        return {}
    yol = np.log(c / c.shift()).abs().sum()
    return {"bar": len(gg), "gunluk_get": gg.r.mean() * 100, "yukari_gun": gg.up.mean() * 100,
            "tavan100": gg.tavan.mean() * 100, "taban100": gg.taban.mean() * 100, "mum_med": gg.rng.median() * 100,
            "mum_evren_yzd": rng_yzd.loc[a:b].median() * 100, "tl_evren_yzd": tl_yzd.loc[a:b].median() * 100,
            "hacim_kat": gg.vk.median(), "clv": gg.clv.mean(), "gapup": gg.gapup.mean() * 100,
            "verim": np.log(c.iloc[-1] / c.iloc[0]) / yol if yol > 0 else np.nan, "maks_dd": (c / c.cummax() - 1).min() * 100}


def fi_k3_vaka(V: Dict[str, pd.DataFrame], A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    G = {s: fi_gunluk(d, A) for s, d in V.items()}
    rng = pd.concat({s: g.rng for s, g in G.items()}, axis=1, sort=True)
    tl = pd.concat({s: g.tl for s, g in G.items()}, axis=1, sort=True)
    rng_yzd = rng.rank(axis=1, pct=True); tl_yzd = tl.rank(axis=1, pct=True)
    kos, faz, tet = [], [], []
    for s in FON_HISSE:
        if s not in V:
            filog.warning("vaka %s veride yok", s); continue
        d = V[s]; k = fi_kosu(d, A)
        if k is None:
            continue
        kos.append({"sembol": s, **k})
        ix = d.index; i0 = ix.get_loc(k["dip"])
        fz = {"ONCE": (ix[max(0, i0 - 120)], ix[max(0, i0 - 1)]), "ERKEN": (k["dip"], k["x2"]),
              "KOSU": (k["x2"], k["tepe"]), "COKUS": (k["tepe"], ix[-1])}
        for f, (a, b) in fz.items():
            if a is None or b is None or (f == "ONCE" and i0 < 30):
                continue
            o = fi_faz_olc(d, G[s], rng_yzd[s], tl_yzd[s], a, b)
            if o:
                faz.append({"sembol": s, "faz": f, **o})
        Z = fi_pencere(d, A); m = fi_izler(Z)["B_A_verim"] & (Z.g >= A.g_alt) & (Z.g < A.g_ust)
        m = m[(m.index >= k["dip"]) & (m.index <= k["tepe"])]
        t = m[m].index.min() if m.any() else None
        c = d.Close
        tet.append({"sembol": s, "kat_dip_tepe": k["kat"], "ilk_iz": t,
                    "iz_aninda_dipten_kat": c[t] / c[k["dip"]] if t is not None else np.nan,
                    "izden_tepeye_kat": c[k["tepe"]] / c[t] if t is not None else np.nan,
                    "izden_bugune_kat": c.iloc[-1] / c[t] if t is not None else np.nan,
                    "tepeden_bugun_pct": (c.iloc[-1] / c[k["tepe"]] - 1) * 100})
    return pd.DataFrame(kos), pd.DataFrame(faz), pd.DataFrame(tet)


# ---------------------------------------------------------------- K4 evren olaylari
def _fi_sonuc(d: pd.DataFrame, i: int, A: FIAyar) -> Optional[Dict[str, float]]:
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy(); n = len(c)
    if i + A.ufuk >= n:
        return None
    up = c[i] * A.hedef_kat; dn = c[i] * (1 - A.zarar); s = 0.0
    for j in range(i + 1, i + A.ufuk + 1):
        if l[j] <= dn:
            s = 0.0; break
        if h[j] >= up:
            s = 1.0; break
    return {"x2_once": s, "maks": h[i + 1:i + A.ufuk + 1].max() / c[i], "r_son": c[i + A.ufuk] / c[i] - 1}


def fi_k4_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: FIAyar) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []; t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            Z = fi_pencere(d, A); ok = ((Z.g >= A.g_alt) & (Z.g < A.g_ust) & Z.mk.notna()).to_numpy()
            iz = {k: v.to_numpy() for k, v in fi_izler(Z).items()}
            son = -10 ** 9
            for i in np.flatnonzero(ok):
                if i - son < A.tekrar:
                    continue
                o = _fi_sonuc(d, i, A)
                if o is None:
                    continue
                son = i
                rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], **{k: bool(v[i]) for k, v in iz.items()},
                             **{k: float(Z[k].iat[i]) for k in Z.columns}, **o})
        except Exception as ex:
            filog.warning("%s atlandi: %s", s, ex)
        if no % 300 == 0:
            filog.info("%s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")].copy()
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
    return O


def _fi_once(d: pd.DataFrame, i: int, ufuk: int, yukari: float, asagi: float) -> float:
    c = d.Close.to_numpy(); h = d.High.to_numpy(); l = d.Low.to_numpy()
    for j in range(i + 1, i + ufuk + 1):
        if l[j] <= c[i] * (1 - asagi):
            return 0.0
        if h[j] >= c[i] * (1 + yukari):
            return 1.0
    return 0.0


def fi_k4b_hacim_olaylar(V: Dict[str, pd.DataFrame], pazar: str, A: FIAyar) -> pd.DataFrame:
    """v1.1: evrende Z0 (sessiz yuvarlanma) olaylari ve hacim olculeri; sonuc 250 bar 2 kat / -%30 ve 60 bar +%20 / -%10."""
    rows: List[Dict[str, Any]] = []; t0 = time.time()
    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            o = fi_hacim_olc(d, A); z = o.Z0.to_numpy(); son = -10 ** 9; n = len(d); c = d.Close.to_numpy()
            for i in np.flatnonzero(z):
                if i - son < A.hacim_tekrar or i + A.ufuk >= n:
                    continue
                son = i
                rows.append({"pazar": pazar, "sembol": s, "tarih": d.index[i], **{k: float(o[k].iat[i]) for k in _FI_HKOL},
                             "x2_once": _fi_once(d, i, A.ufuk, A.hedef_kat - 1, A.zarar), "k20_once": _fi_once(d, i, 60, 0.20, 0.10),
                             "r60": c[i + 60] / c[i] - 1, "r_son": c[i + A.ufuk] / c[i] - 1})
        except Exception as ex:
            filog.warning("hacim olay %s atlandi: %s", s, ex)
        if no % 300 == 0:
            filog.info("hacim %s %d/%d hisse, %d olay, %.0f sn", pazar, no, len(V), len(rows), time.time() - t0)
    O = pd.DataFrame(rows)
    if not O.empty:
        O = O[pd.to_datetime(O.tarih) >= pd.Timestamp("2016-01-01")].copy()
        O["donem"] = np.where(pd.to_datetime(O.tarih) < pd.Timestamp(A.donem_siniri), "2016-21", "2022-26")
    return O


def fi_ozet_hacim(O: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for ad, m in fi_hacim_varyant(O).items():
        for (p, dn), g in O.groupby(["pazar", "donem"]):
            mm = m.loc[g.index]; s = g[mm]; t = g[~mm]
            if len(s) == 0 or len(t) == 0:
                continue
            rows.append({"iz": ad, "pazar": p, "donem": dn, "n": len(s),
                         "x2_once": s.x2_once.mean() * 100, "t_x2_once": t.x2_once.mean() * 100, "kat_x2": s.x2_once.mean() / t.x2_once.mean(),
                         "k20_once": s.k20_once.mean() * 100, "t_k20_once": t.k20_once.mean() * 100, "kat_k20": s.k20_once.mean() / t.k20_once.mean(),
                         "r60_med": s.r60.median() * 100, "t_r60_med": t.r60.median() * 100})
    oz = pd.DataFrame(rows)
    oz["gecti_x2"] = (oz.kat_x2 >= 1.3) & (oz.n >= 30); oz["gecti_k20"] = (oz.kat_k20 >= 1.3) & (oz.n >= 30)
    iz = oz.groupby("iz").agg(dilim=("n", "size"), gecti_x2=("gecti_x2", "sum"), kat_x2_min=("kat_x2", "min"),
                              gecti_k20=("gecti_k20", "sum"), kat_k20_min=("kat_k20", "min"), n_min=("n", "min")).reset_index()
    return oz, iz.sort_values(["gecti_x2", "gecti_k20", "kat_x2_min"], ascending=False)


def fi_ozet(O: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    adlar = [c for c in O.columns if O[c].dtype == bool]
    rows = []
    for ad in adlar:
        for (p, dn), g in O.groupby(["pazar", "donem"]):
            s = g[g[ad]]; t = g[~g[ad]]
            if len(s) == 0 or len(t) == 0:
                continue
            rows.append({"iz": ad, "pazar": p, "donem": dn, "n": len(s), "x2_once": s.x2_once.mean() * 100,
                         "t_x2_once": t.x2_once.mean() * 100, "kat": s.x2_once.mean() / t.x2_once.mean() if t.x2_once.mean() > 0 else np.nan,
                         "r250_med": s.r_son.median() * 100, "t_r250_med": t.r_son.median() * 100,
                         "maks5x": (s.maks >= 5).mean() * 100, "t_maks5x": (t.maks >= 5).mean() * 100})
    oz = pd.DataFrame(rows)
    oz["gecti"] = (oz.kat >= 1.3) & (oz.n >= 30)
    iz = oz.groupby("iz").agg(dilim=("n", "size"), gecti=("gecti", "sum"), ayni_yon=("kat", lambda k: int((k > 1).sum())),
                              kat_min=("kat", "min"), kat_ort=("kat", "mean"), n_min=("n", "min")).reset_index()
    return oz, iz.sort_values(["gecti", "ayni_yon", "kat_ort"], ascending=False)


# ---------------------------------------------------------------- K6 gosterge bataryasi + uyumsuzluk + Fibonacci (v1.2)
def _fi_ema(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def _fi_wilder(x: pd.Series, n: int) -> pd.Series:
    return x.ewm(alpha=1.0 / n, adjust=False, min_periods=n).mean()


def _fi_bar_once(x: np.ndarray, n: int, en_buyuk: bool) -> np.ndarray:
    """Her bar icin son n+1 bardaki en yuksek (en_buyuk) / en dusuk degerin kac bar once oldugu (Aroon, Fibonacci bacagi)."""
    out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    w = np.lib.stride_tricks.sliding_window_view(x, n + 1)
    k = np.argmax(w, axis=1) if en_buyuk else np.argmin(w, axis=1)
    out[n:] = n - k
    return out


def _fi_uyumsuzluk(fiyat: np.ndarray, gosterge: np.ndarray, k: int, ara: int, dip: bool) -> Tuple[np.ndarray, np.ndarray]:
    """Pivot tabanli uyumsuzluk, gelecege bakmadan. Pivot p = p-k..p+k araliginin en dusugu (dip) / en yuksegi (tepe); sinyal
    pivotun dogrulandigi p+k gunu. Ardisik iki pivot (k <= ara farki <= `ara`). Dip: duz boga = fiyat daha dusuk dip, gosterge daha
    yuksek dip; gizli boga = fiyat daha yuksek dip, gosterge daha dusuk dip. Tepe: duz ayi = fiyat daha yuksek tepe, gosterge daha
    dusuk tepe; gizli ayi tersi. Donus: (duz, gizli) bool dizileri."""
    n = len(fiyat); duz = np.zeros(n, bool); gizli = np.zeros(n, bool)
    if n < 2 * k + 2:
        return duz, gizli
    w = np.lib.stride_tricks.sliding_window_view(fiyat, 2 * k + 1)
    ext = w.min(axis=1) if dip else w.max(axis=1)
    tek = (w == ext[:, None]).sum(axis=1) == 1          # kesin uc nokta (duz rafin her bari pivot sayilmaz)
    piv = np.flatnonzero((fiyat[k:n - k] == ext) & tek) + k
    piv = piv[~np.isnan(gosterge[piv])]
    for a, b in zip(piv[:-1], piv[1:]):
        if b - a < k or b - a > ara:
            continue
        fa, fb, ga, gb = fiyat[a], fiyat[b], gosterge[a], gosterge[b]
        t = b + k
        if dip:
            if fb < fa and gb > ga:
                duz[t] = True
            elif fb > fa and gb < ga:
                gizli[t] = True
        else:
            if fb > fa and gb < ga:
                duz[t] = True
            elif fb < fa and gb > ga:
                gizli[t] = True
    return duz, gizli


_FI_UY = (("rsi", "rsi"), ("macd", "macd_hist"), ("obv", "obv"), ("mfi", "mfi"), ("cmf", "cmf"))
_FI_FIB = np.array([0.236, 0.382, 0.5, 0.618, 0.786])


def fi_gostergeler(d: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """v1.2 gunluk gosterge tablosu (hepsi yalniz o gune kadarki veriyle)."""
    c, h, l = d.Close, d.High, d.Low; v = d.Volume.astype(float); pc = c.shift(); dc = c.diff(); tp = (h + l + c) / 3
    G = pd.DataFrame(index=d.index)
    G["r"] = c / pc - 1
    up = _fi_wilder(dc.clip(lower=0), 14); dn = _fi_wilder((-dc).clip(lower=0), 14)
    G["rsi"] = 100 * up / (up + dn).replace(0, np.nan)
    hh = h.rolling(14).max(); ll = l.rolling(14).min()
    G["stoch"] = 100 * (c - ll) / (hh - ll).replace(0, np.nan)
    G["wr"] = G.stoch - 100
    m = tp.rolling(20).mean()
    G["cci"] = (tp - m) / (0.015 * (tp - m).abs().rolling(20).mean()).replace(0, np.nan)   # sapma kayan ortalamaya gore (yaklasik)
    rmf = tp * v; pos = rmf.where(tp > tp.shift(), 0.0).rolling(14).sum(); neg = rmf.where(tp < tp.shift(), 0.0).rolling(14).sum()
    G["mfi"] = 100 * pos / (pos + neg).replace(0, np.nan)
    mfm = (((c - l) - (h - c)) / (h - l).replace(0, np.nan)).fillna(0.0)
    G["cmf"] = (mfm * v).rolling(20).sum() / v.rolling(20).sum().replace(0, np.nan)
    obv = (np.sign(dc).fillna(0.0) * v).cumsum(); ad = (mfm * v).cumsum(); v20 = v.rolling(20).sum().replace(0, np.nan)
    G["obv"] = obv
    G["obv20"] = (obv - obv.shift(20)) / v20
    G["ad20"] = (ad - ad.shift(20)) / v20
    G["obv_60tepe"] = obv >= obv.rolling(60).max()
    macd = _fi_ema(c, 12) - _fi_ema(c, 26); sig = _fi_ema(macd, 9)
    G["macd"] = macd / c; G["macd_sinyal"] = sig / c; G["macd_hist"] = (macd - sig) / c
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1); atr = _fi_wilder(tr, 14)
    upm = h.diff(); dnm = -l.diff()
    pdm = upm.where((upm > dnm) & (upm > 0), 0.0); ndm = dnm.where((dnm > upm) & (dnm > 0), 0.0)
    G["pdi"] = 100 * _fi_wilder(pdm, 14) / atr.replace(0, np.nan)
    G["ndi"] = 100 * _fi_wilder(ndm, 14) / atr.replace(0, np.nan)
    G["adx"] = _fi_wilder(100 * (G.pdi - G.ndi).abs() / (G.pdi + G.ndi).replace(0, np.nan), 14)
    hn = h.to_numpy(float); ln = l.to_numpy(float)
    G["aroon_up"] = 100 * (25 - _fi_bar_once(hn, 25, True)) / 25
    G["aroon_dn"] = 100 * (25 - _fi_bar_once(ln, 25, False)) / 25
    m20 = c.rolling(20).mean(); s20 = c.rolling(20).std(ddof=0)
    G["bb_b"] = (c - (m20 - 2 * s20)) / (4 * s20).replace(0, np.nan)
    bw = 4 * s20 / m20
    G["bb_gen"] = bw / bw.rolling(A.normal, min_periods=A.normal_min).median()
    e20 = _fi_ema(c, 20); atr20 = _fi_wilder(tr, 20)
    G["sikisma"] = ((m20 + 2 * s20) < (e20 + 1.5 * atr20)) & ((m20 - 2 * s20) > (e20 - 1.5 * atr20))
    tenkan = (h.rolling(9).max() + l.rolling(9).min()) / 2; kijun = (h.rolling(26).max() + l.rolling(26).min()) / 2
    spa = ((tenkan + kijun) / 2).shift(26); spb = ((h.rolling(52).max() + l.rolling(52).min()) / 2).shift(26)
    G["bulut_ust"] = c > pd.concat([spa, spb], axis=1).max(axis=1, skipna=False)
    G["tk_ust"] = tenkan > kijun
    sma50 = c.rolling(50).mean(); sma200 = c.rolling(200).mean()
    G["sma50_mes"] = c / sma50 - 1; G["sma200_mes"] = c / sma200 - 1; G["sma50_200"] = sma50 > sma200
    G["roc20"] = c / c.shift(20) - 1
    G["c_60tepe"] = c / c.rolling(60).max()
    G["atr_yzd"] = atr / c
    G["force"] = _fi_ema(dc * v, 13) / (c * v.rolling(20).mean()).replace(0, np.nan)
    dd14 = 100 * (c / c.rolling(14).max() - 1)
    G["ulcer"] = np.sqrt((dd14 ** 2).rolling(14).mean())
    n = A.normal; lo = l.rolling(n).min(); hi = h.rolling(n).max()
    G["fib_konum"] = (c - lo) / (hi - lo).replace(0, np.nan)
    yukselis = _fi_bar_once(ln, n - 1, False) > _fi_bar_once(hn, n - 1, True)   # bacak dipten tepeye (dip once)
    geri = ((hi - c) / (hi - lo).replace(0, np.nan)).where(yukselis)
    G["fib_geri"] = geri
    gn = geri.to_numpy(float)
    G["fib_yakin"] = np.min(np.abs(gn[:, None] - _FI_FIB[None, :]), axis=1)
    G["vk"] = v / v.shift().rolling(20, min_periods=10).median().replace(0, np.nan)
    G["kilit_tavan"] = (G.r >= A.sinir_gun) & ((h - l) / c < 0.002)
    for ad, kol in _FI_UY:
        x = G[kol].to_numpy(float)
        a, b = _fi_uyumsuzluk(ln, x, A.piv_k, A.piv_ara, True)
        G[f"uy_{ad}_boga"] = a; G[f"uy_{ad}_gizli_boga"] = b
        a, _ = _fi_uyumsuzluk(hn, x, A.piv_k, A.piv_ara, False)
        G[f"uy_{ad}_ayi"] = a
    return G


def _fi_yukari_kes(x: pd.Series, e: float) -> pd.Series:
    return (x > e) & (x.shift() <= e)


def _fi_yeni(x: pd.Series) -> pd.Series:
    return x & ~x.shift(1, fill_value=False).astype(bool)


# Asagi yonlu (satis/kacinma) sinyalleri: bunlarda iz = 'dus' sonucunda kat >= 1,3.
FI_AYI = {"rsi_70_ustu", "mfi_80_ustu", "cmf_negatif", "bb_alt_kirilim", "fib_tepe_bolge", "blok_taban",
          "uy_rsi_ayi", "uy_macd_ayi", "uy_obv_ayi", "uy_mfi_ayi", "uy_cmf_ayi",
          "kap_devre_kesici", "kap_olagan_disi", "kap_spk_yasak", "kap_vbts_tedbir", "kap_tipe_donusum"}


def fi_gosterge_sinyal(G: pd.DataFrame, A: FIAyar) -> Dict[str, pd.Series]:
    """Sabit esikli ikili sinyaller (gosterge ders kitabi esikleri; veriye gore ayarlanmadi)."""
    blok = G.vk >= A.blok_kat; tavan = G.r >= A.sinir_gun
    S = {"rsi_30_alti": G.rsi < 30, "rsi_70_ustu": G.rsi > 70, "rsi_50_kesme": _fi_yukari_kes(G.rsi, 50),
         "stoch_20_donus": _fi_yukari_kes(G.stoch, 20), "wr_80_alti": G.wr < -80,
         "cci_100_alti": G.cci < -100, "cci_100_ustu": G.cci > 100,
         "mfi_20_alti": G.mfi < 20, "mfi_80_ustu": G.mfi > 80,
         "cmf_pozitif": G.cmf > 0.10, "cmf_negatif": G.cmf < -0.10,
         "obv_lider": G.obv_60tepe & (G.c_60tepe < 0.95),
         "ad_birikim_yatay": (G.ad20 > 0.20) & (G.roc20.abs() < 0.03),
         "macd_al_sifir_alti": _fi_yukari_kes(G.macd - G.macd_sinyal, 0.0) & (G.macd < 0),
         "macd_sifir_kesme": _fi_yukari_kes(G.macd, 0.0),
         "adx_25_trend": _fi_yukari_kes(G.adx, 25) & (G.pdi > G.ndi),
         "aroon_yukari": (G.aroon_up > 70) & (G.aroon_dn < 30),
         "bb_sikisma": G.bb_gen < 0.6, "bb_ust_kirilim": G.bb_b > 1, "bb_alt_kirilim": G.bb_b < 0,
         "squeeze_yukari_cozulme": (~G["sikisma"]) & G["sikisma"].shift(1, fill_value=False).astype(bool) & (G.macd_hist > 0),
         "bulut_ustu_kesme": _fi_yeni(G.bulut_ust), "tenkan_kijun_kesme": _fi_yeni(G.tk_ust), "altin_kesisim": _fi_yeni(G.sma50_200),
         "fib_618_bolge": (G.fib_geri >= 0.55) & (G.fib_geri <= 0.68), "fib_382_bolge": (G.fib_geri >= 0.33) & (G.fib_geri <= 0.43),
         "fib_dip_bolge": G.fib_konum < 0.15, "fib_tepe_bolge": G.fib_konum > 0.90,
         "force_guclu": G.force > 0.01, "ulcer_sakin_trend": (G.ulcer < 3) & (G.roc20 > 0.05),
         "blok_hacim": blok, "blok_tavan": blok & tavan,
         "blok_seri_ici": blok & tavan & (G.kilit_tavan.astype(int).rolling(5).sum().shift() >= 2),
         "blok_taban": blok & (G.r <= -A.sinir_gun), "kilit_tavan": G.kilit_tavan}
    for ad, _ in _FI_UY:
        for t in ("boga", "gizli_boga", "ayi"):
            S[f"uy_{ad}_{t}"] = G[f"uy_{ad}_{t}"]
    return {k: v.fillna(False).astype(bool) for k, v in S.items()}


def _fi_ilk(c: np.ndarray, h: np.ndarray, l: np.ndarray, ufuk: int, yukari: float, asagi: float) -> Tuple[np.ndarray, np.ndarray]:
    """Her gun icin ufuk bar icinde once +yukari (High) mi once -asagi (Low) mu; (once_yukari, once_asagi) 1/0, ufuk dolmadiysa NaN.
    Ayni barda ikisi birden: asagi sayilir (temkinli; _fi_once ile ayni)."""
    n = len(c); u = np.full(n, np.nan); a = np.full(n, np.nan)
    m = n - ufuk
    if m <= 0:
        return u, a
    Hw = np.lib.stride_tricks.sliding_window_view(h[1:], ufuk)[:m]; Lw = np.lib.stride_tricks.sliding_window_view(l[1:], ufuk)[:m]
    yu = Hw >= (c[:m] * (1 + yukari))[:, None]; ya = Lw <= (c[:m] * (1 - asagi))[:, None]
    iu = np.where(yu.any(1), yu.argmax(1), ufuk + 1); ia = np.where(ya.any(1), ya.argmax(1), ufuk + 1)
    u[:m] = (iu < ia).astype(float); a[:m] = (ia < iu).astype(float)
    return u, a


_FI_SONUC = ("k20", "x2", "dus")


def _fi_sonuclar(d: pd.DataFrame) -> Dict[str, np.ndarray]:
    c = d.Close.to_numpy(float); h = d.High.to_numpy(float); l = d.Low.to_numpy(float)
    k20, _ = _fi_ilk(c, h, l, 60, 0.20, 0.10); x2, _ = _fi_ilk(c, h, l, 250, 1.00, 0.30); _, dus = _fi_ilk(c, h, l, 60, 0.20, 0.20)
    return {"k20": k20, "x2": x2, "dus": dus}


# ---------------------------------------------------------------- K8 KAP olaylari (v1.2)
FI_KAP_KONU = {"kap_vbts_tedbir": (14,), "kap_tipe_donusum": (13,), "kap_toptan": (84, 119, 140), "kap_pay_alim_satim": (6,),
               "kap_devre_kesici": (0,), "kap_olagan_disi": (42,), "kap_spk_yasak": (30,), "kap_fiili_dolasim": (61,),
               "kap_piyasa_yapici": (3,), "kap_soylenti": (79,)}


def fi_kap_yukle(A: FIAyar) -> Dict[str, Dict[str, pd.DataFrame]]:
    """kap_ozet (tarih, saat, sembol, konu_id) -> {sembol: {grup: DataFrame(tarih, saat)}}. Klasor (kap_20*.csv.gz) ya da tek dosya."""
    yol = A.kap
    if os.path.isdir(yol):
        dosyalar = sorted(os.path.join(yol, f) for f in os.listdir(yol) if f.startswith("kap_20") and f.endswith(".csv.gz"))
    else:
        dosyalar = [yol]
    if not dosyalar or not all(os.path.exists(f) for f in dosyalar):
        raise FileNotFoundError(f"KAP ozeti yok: {yol}")
    K = pd.concat([pd.read_csv(f, usecols=["tarih", "saat", "sembol", "konu_id"]) for f in dosyalar], ignore_index=True)
    K = K.drop_duplicates()
    ters = {k: g for g, ks in FI_KAP_KONU.items() for k in ks}
    K = K[K.konu_id.isin(ters)].copy(); K["grup"] = K.konu_id.map(ters)
    K["tarih"] = pd.to_datetime(K.tarih, errors="coerce"); K = K.dropna(subset=["tarih"])
    out: Dict[str, Dict[str, pd.DataFrame]] = {}
    for (s, g), t in K.groupby(["sembol", "grup"]):
        out.setdefault(str(s), {})[g] = t[["tarih", "saat"]]
    filog.info("KAP: %d bildirim, %d sembol (%s .. %s)", len(K), len(out), K.tarih.min().date(), K.tarih.max().date())
    return out


def fi_kap_sinyal(idx: pd.DatetimeIndex, olay: Optional[Dict[str, pd.DataFrame]]) -> Dict[str, pd.Series]:
    """Bildirimleri islem gunune esler: saat 18:00 ve sonrasi -> ertesi islem gunu (D0), aksi halde ayni gun (ya da sonraki ilk islem gunu)."""
    S = {}
    for g in FI_KAP_KONU:
        b = np.zeros(len(idx), bool)
        if olay and g in olay:
            t = olay[g]
            gun = t.tarih + pd.to_timedelta((t.saat.astype(str) >= "18:00").astype(int), unit="D")
            j = idx.searchsorted(gun.to_numpy(), side="left")
            j = j[j < len(idx)]
            b[j] = True
        S[g] = pd.Series(b, index=idx)
    return S


# ---------------------------------------------------------------- K6a fon vakalari / K6b evren
_FI_GKOL = ["rsi", "mfi", "cmf", "obv20", "ad20", "adx", "bb_gen", "fib_konum", "atr_yzd", "macd_hist", "vk", "roc20", "ulcer", "force"]


def fi_k6_vaka(V: Dict[str, pd.DataFrame], kos: pd.DataFrame, kap: Dict[str, Dict[str, pd.DataFrame]], A: FIAyar
               ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Fon hisselerinin ONCE / ERKEN / KOSU fazlarinda 100 gunde sinyal sikligi ve gosterge medyanlari vs diger BIST (2024-26).
    Donus: (sinyal profili, gosterge profili, fon hisselerinin blok hacim gunleri)."""
    say: Dict[str, Dict[str, float]] = {}; gun: Dict[str, int] = {}; deger: Dict[str, List[pd.DataFrame]] = {}; blok = []
    kosd = kos.set_index("sembol"); a0, b0 = pd.Timestamp(A.hacim_bas), pd.Timestamp(A.kriz_tarih)
    for s, d in V.items():
        try:
            G = fi_gostergeler(d, A); S = fi_gosterge_sinyal(G, A); S.update(fi_kap_sinyal(d.index, kap.get(s)))
            Sd = pd.DataFrame(S)
            if s in kosd.index:
                k = kosd.loc[s]; i_dip = d.index.get_loc(k.dip)
                bitis_erken = k.x2 if pd.notna(k.x2) else k.tepe
                fazlar = {"ONCE": d.index[max(0, i_dip - A.once_bar):i_dip], "ERKEN": d.loc[k.dip:bitis_erken].index,
                          "KOSU": d.loc[bitis_erken:k.tepe].index[1:] if pd.notna(k.x2) else d.index[:0]}
                b = G.loc[k.dip:k.tepe]; b = b[b.vk >= A.blok_kat]
                for t, row in b.iterrows():
                    blok.append({"sembol": s, "tarih": t.date(), "r_yzd": row.r * 100, "hacim_kat": row.vk,
                                 "kilit_tavan_onceki5": int(G.kilit_tavan.loc[:t].iloc[-6:-1].sum()),
                                 "faz": "ERKEN" if t <= bitis_erken else "KOSU"})
            else:
                fazlar = {"DIGER": d.loc[a0:b0].index}
            for f, ix in fazlar.items():
                if len(ix) == 0:
                    continue
                q = say.setdefault(f, {})
                for c in Sd.columns:
                    q[c] = q.get(c, 0.0) + float(Sd.loc[ix, c].sum())
                gun[f] = gun.get(f, 0) + len(ix)
                deger.setdefault(f, []).append(G.loc[ix, _FI_GKOL])
        except Exception as ex:
            filog.warning("gosterge vaka %s atlandi: %s", s, ex)
    fz = [f for f in ("ONCE", "ERKEN", "KOSU", "DIGER") if f in gun]
    P = pd.DataFrame({f: {c: 100.0 * v / gun[f] for c, v in say[f].items()} for f in fz})
    if "DIGER" in P:
        for f in ("ONCE", "ERKEN", "KOSU"):
            if f in P:
                P[f"{f}/DIGER"] = P[f] / P["DIGER"].replace(0, np.nan)
    P.loc["_gun_sayisi"] = [gun.get(f, np.nan) for f in fz] + [np.nan] * (P.shape[1] - len(fz))
    D = pd.DataFrame({f: pd.concat(deger[f]).median() for f in fz})
    return P.reset_index().rename(columns={"index": "sinyal"}), D.reset_index().rename(columns={"index": "gosterge"}), pd.DataFrame(blok)


def fi_k6_evren(V: Dict[str, pd.DataFrame], pazar: str, kap: Optional[Dict[str, Dict[str, pd.DataFrame]]], A: FIAyar) -> pd.DataFrame:
    """Her sinyal (ayni hissede g_tekrar bar icinde bir kez) ve taban (her ornek_adim. gun) icin sonuc sayaclari, donem bazinda."""
    top: Dict[Tuple[str, str], List[float]] = {}; t0 = time.time(); bas = pd.Timestamp("2016-01-01"); sinir = pd.Timestamp(A.donem_siniri)

    def ekle(ad: str, ix: np.ndarray, Y: Dict[str, np.ndarray], dn: np.ndarray) -> None:
        for donem in ("2016-21", "2022-26"):
            j = ix[dn[ix] == donem]
            if len(j) == 0:
                continue
            q = top.setdefault((ad, donem), [0.0] * 7)
            q[0] += len(j)
            for k, y in enumerate(_FI_SONUC):
                yy = Y[y][j]; ok = ~np.isnan(yy)
                q[1 + 2 * k] += ok.sum(); q[2 + 2 * k] += yy[ok].sum()

    for no, (s, d) in enumerate(V.items(), 1):
        try:
            if len(d) < 400:
                continue
            G = fi_gostergeler(d, A); S = fi_gosterge_sinyal(G, A)
            if kap is not None:
                S.update(fi_kap_sinyal(d.index, kap.get(s)))
            Y = _fi_sonuclar(d)
            gecerli = (d.index >= bas)
            dn = np.where(d.index < sinir, "2016-21", "2022-26")
            taban = np.flatnonzero(gecerli & (np.arange(len(d)) % A.ornek_adim == 0) & G.rsi.notna().to_numpy())
            ekle("_TABAN", taban, Y, dn)
            for ad, sg in S.items():
                ix = np.flatnonzero(sg.to_numpy() & gecerli)
                if len(ix) == 0:
                    continue
                tut = []; son = -10 ** 9
                for i in ix:
                    if i - son >= A.g_tekrar:
                        tut.append(i); son = i
                ekle(ad, np.asarray(tut, dtype=int), Y, dn)
        except Exception as ex:
            filog.warning("gosterge evren %s %s atlandi: %s", pazar, s, ex)
        if no % 300 == 0:
            filog.info("gosterge %s %d/%d hisse, %.0f sn", pazar, no, len(V), time.time() - t0)
    rows = [{"pazar": pazar, "sinyal": a, "donem": dn, "n": q[0], "n_k20": q[1], "k20": q[2], "n_x2": q[3], "x2": q[4],
             "n_dus": q[5], "dus": q[6]} for (a, dn), q in top.items()]
    return pd.DataFrame(rows)


def fi_k6_ozet(E: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Oranlar ve kat (sinyal / taban); iz: yukari sinyalde k20 ya da x2, asagi sinyalde dus katinin >= 1,3 oldugu dilim sayisi."""
    E = E.copy()
    for y in _FI_SONUC:
        E[f"{y}_yzd"] = 100 * E[y] / E[f"n_{y}"].replace(0, np.nan)
    T = E[E.sinyal == "_TABAN"].set_index(["pazar", "donem"])
    S = E[E.sinyal != "_TABAN"].copy()
    for y in _FI_SONUC:
        S[f"t_{y}_yzd"] = [T.loc[(p, dn), f"{y}_yzd"] for p, dn in zip(S.pazar, S.donem)]
        S[f"kat_{y}"] = S[f"{y}_yzd"] / S[f"t_{y}_yzd"]
    S["yon"] = np.where(S.sinyal.isin(FI_AYI), "asagi", "yukari")
    S["gecti_k20"] = (S.yon == "yukari") & (S.kat_k20 >= 1.3) & (S.n_k20 >= 30)
    S["gecti_x2"] = (S.yon == "yukari") & (S.kat_x2 >= 1.3) & (S.n_x2 >= 30)
    S["gecti_dus"] = (S.yon == "asagi") & (S.kat_dus >= 1.3) & (S.n_dus >= 30)
    iz = S.groupby(["sinyal", "yon"]).agg(dilim=("n", "size"), n_min=("n", "min"),
                                          gecti_k20=("gecti_k20", "sum"), kat_k20_min=("kat_k20", "min"), kat_k20_ort=("kat_k20", "mean"),
                                          gecti_x2=("gecti_x2", "sum"), kat_x2_min=("kat_x2", "min"),
                                          gecti_dus=("gecti_dus", "sum"), kat_dus_min=("kat_dus", "min"), kat_dus_ort=("kat_dus", "mean")
                                          ).reset_index()
    iz["iz"] = np.where(iz.yon == "yukari", (iz.gecti_k20 == iz.dilim) | (iz.gecti_x2 == iz.dilim), iz.gecti_dus == iz.dilim) & (iz.dilim >= 4)
    iz["sira"] = np.where(iz.yon == "yukari", iz.kat_k20_min, iz.kat_dus_min)
    return S, iz.sort_values(["iz", "sira"], ascending=False).drop(columns="sira")


def fi_k6_rapor(P: pd.DataFrame, D: pd.DataFrame, blok: pd.DataFrame, iz: pd.DataFrame, S: pd.DataFrame, kos: pd.DataFrame) -> str:
    gosterge = [r for r in iz.sinyal if not r.startswith("kap_")]
    sat = [f"# FON_IZI gosterge bataryasi — {FI_SURUM}", "",
           "Soru (Cemal, 23 Eki): fonlar hisseleri alirken iz birakmadi mi? Mum ve hacim disinda her gosterge, uyumsuzluk, Fibonacci.", "",
           "## Fon hisselerinde blok hacim gunleri (hacim >= 20x onceki 20 gun medyani, dip -> tepe)", "",
           blok.round(2).to_markdown(index=False) if len(blok) else "(yok)", "",
           "## Fon hisseleri: 100 gunde sinyal sikligi (ONCE = dipten onceki 120 bar, ERKEN = dip -> 2 kat, KOSU = 2 kat -> tepe;"
           " DIGER = fon disi BIST 2024-26)", "", P.round(2).to_markdown(index=False), "",
           "## Fon hisseleri: gosterge medyanlari", "", D.round(3).to_markdown(index=False), "",
           "## Evren testi: gostergeler (4 dilim BIST/ABD x 2016-21/2022-26; kat = sinyal orani / her 5. gun tabani)", "",
           iz[iz.sinyal.isin(gosterge)].round(2).to_markdown(index=False), "",
           "## Evren testi: KAP olaylari (yalniz BIST, 2 dilim; 2017 oncesi KAP verisi yok)", "",
           iz[~iz.sinyal.isin(gosterge)].round(2).to_markdown(index=False), "",
           "## Vaka kosulari", "", kos.assign(**{c: pd.to_datetime(kos[c]).dt.date for c in ("dip", "x2", "tepe")}).round(2).to_markdown(index=False), ""]
    return "\n".join(sat)


def fon_izi_gosterge(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    """v1.2 ana giris: K6 gosterge/uyumsuzluk/Fibonacci + K7 blok hacim + K8 KAP olaylari; vaka profili ve evren testi."""
    A = A or FIAyar()
    os.makedirs(A.cikti, exist_ok=True)
    veri = {}
    for pazar, yol in A.veri.items():
        try:
            veri[pazar] = fi_k1_veri(yol, pazar, A)
        except Exception as ex:
            filog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
    if "BIST" not in veri:
        raise RuntimeError("BIST verisi yok; vaka incelemesi yapilamaz")
    try:
        kap = fi_kap_yukle(A)
    except Exception as ex:
        filog.error("KAP ozeti okunamadi (%s); KAP sinyalleri bos", ex); kap = {}
    kos = []
    for s in FON_HISSE:
        if s in veri["BIST"]:
            k = fi_kosu(veri["BIST"][s], A)
            if k:
                kos.append({"sembol": s, **k})
    kos = pd.DataFrame(kos)
    P, D, blok = fi_k6_vaka(veri["BIST"], kos, kap, A)
    E = pd.concat([fi_k6_evren(V, p, kap if p == "BIST" else None, A) for p, V in veri.items()], ignore_index=True)
    S, iz = fi_k6_ozet(E)
    P.to_csv(os.path.join(A.cikti, "fon_gosterge_profil.csv"), index=False)
    D.to_csv(os.path.join(A.cikti, "fon_gosterge_deger.csv"), index=False)
    blok.to_csv(os.path.join(A.cikti, "fon_blok_gunleri.csv"), index=False)
    S.to_csv(os.path.join(A.cikti, "fon_gosterge_evren.csv"), index=False)
    iz.to_csv(os.path.join(A.cikti, "fon_gosterge_iz.csv"), index=False)
    with open(os.path.join(A.cikti, "FON_IZI_gosterge.md"), "w", encoding="utf-8") as f:
        f.write(fi_k6_rapor(P, D, blok, iz, S, kos))
    return {"profil": P, "deger": D, "blok": blok, "evren": S, "iz": iz, "kosular": kos}


# ---------------------------------------------------------------- K9 fon islem defteri (v1.3): KAP portfoy dagilim raporlari
FI_FON_SIRKET = ("TERA PORTF", "PUSULA PORTF", "HEDEF PORTF", "ATLAS PORTF", "A1 CAPITAL PORTF", "A1 PORTF", "PARDUS PORTF", "BULLS PORTF")
_FI_KAP = "https://www.kap.org.tr"


def _fi_kap_oturum():
    import requests
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                      "Accept": "application/json, text/plain, */*", "Content-Type": "application/json;charset=UTF-8",
                      "Origin": _FI_KAP, "Referer": _FI_KAP + "/tr/bildirim-sorgu"})
    try:
        s.get(_FI_KAP + "/tr/bildirim-sorgu", timeout=30)
    except Exception as ex:
        filog.warning("KAP acilis sayfasi: %s", ex)
    return s


def _fi_kap_istek(s, yontem: str, url: str, deneme: int = 4, **kw):
    """KAP istegi; 403/429/5xx ve ag hatasinda artan beklemeyle tekrar. Basarisizsa None."""
    for i in range(deneme):
        try:
            r = s.request(yontem, url, timeout=60, **kw)
            if r.status_code == 200:
                return r
            filog.warning("KAP %s %s -> HTTP %s (deneme %d)", yontem, url[-60:], r.status_code, i + 1)
        except Exception as ex:
            filog.warning("KAP %s %s -> %s (deneme %d)", yontem, url[-60:], str(ex)[:100], i + 1)
        time.sleep(3 * (i + 1))
    return None


def fi_k9_liste(A: FIAyar) -> pd.DataFrame:
    """KAP fon bildirimlerinden 'Portfoy Dagilim Raporu' listesi (butun fonlar), gun gun; kaldigi yerden devam eder."""
    import json
    os.makedirs(A.kapfon, exist_ok=True)
    yol = os.path.join(A.kapfon, "liste.csv"); yol_gun = os.path.join(A.kapfon, "liste_gunler.txt")
    L = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame()
    bitti = set(open(yol_gun).read().split()) if os.path.exists(yol_gun) else set()
    gunler = [g for g in pd.date_range(A.kapfon_bas, A.kapfon_bit, freq="D")
              if g.day <= A.kapfon_gun and g.weekday() < 5 and str(g.date()) not in bitti]
    s = _fi_kap_oturum(); yeni: List[Dict[str, Any]] = []; t0 = time.time()
    for no, g in enumerate(gunler, 1):
        gs = str(g.date())
        r = _fi_kap_istek(s, "POST", _FI_KAP + "/tr/api/disclosure/funds/byCriteria",
                          data=json.dumps({"fromDate": gs, "toDate": gs, "mkkMemberOidList": [], "subjectList": []}))
        if r is None:
            filog.error("KAP liste %s alinamadi; sonraki calistirmada tekrar denenecek", gs); continue
        try:
            J = r.json()
        except Exception:
            filog.error("KAP liste %s JSON degil", gs); continue
        if len(J) >= 2000:
            filog.warning("KAP liste %s: 2000 kayit siniri; o gunun bir kismi eksik olabilir", gs)
        for j in J:
            if (j.get("subject") or "").strip() == "Portföy Dağılım Raporu":
                yeni.append({"yayin": j.get("publishDate"), "fon": j.get("fundCode"), "unvan": j.get("kapTitle"),
                             "indeks": j.get("disclosureIndex"), "yil": j.get("year"), "donem": j.get("period"),
                             "ek": j.get("attachmentCount")})
        bitti.add(gs)
        if no % 20 == 0 or no == len(gunler):
            L = pd.concat([L, pd.DataFrame(yeni)], ignore_index=True).drop_duplicates("indeks") if yeni else L; yeni = []
            L.to_csv(yol, index=False)
            with open(yol_gun, "w") as f:
                f.write("\n".join(sorted(bitti)))
            filog.info("KAP liste %d/%d gun, %d rapor, %.0f sn", no, len(gunler), len(L), time.time() - t0)
        time.sleep(A.kapfon_bekle)
    return L


def fi_k9_indir(L: pd.DataFrame, A: FIAyar) -> pd.DataFrame:
    """Hedef portfoy sirketlerinin raporlarinin eklerini (PDF) indirir; KAP Java sarmalini soyar. Donus: ek listesi."""
    import re
    kl = os.path.join(A.kapfon, "pdf"); os.makedirs(kl, exist_ok=True)
    yol = os.path.join(A.kapfon, "ekler.csv")
    E = pd.read_csv(yol) if os.path.exists(yol) else pd.DataFrame(columns=["indeks", "dosya"])
    var = set(E.indeks.astype(int)) if len(E) else set()
    H = L[L.unvan.astype(str).str.upper().str.contains("|".join(FI_FON_SIRKET), regex=True)].copy()
    H = H[~H.indeks.astype(int).isin(var)]
    s = _fi_kap_oturum(); yeni = []; t0 = time.time()
    for no, row in enumerate(H.itertuples(index=False), 1):
        r = _fi_kap_istek(s, "GET", f"{_FI_KAP}/tr/Bildirim/{int(row.indeks)}")
        if r is None:
            continue
        linkler = sorted(set(re.findall(r"https://www\.kap\.org\.tr/tr/api/file/download/[0-9a-f]+", r.text)))
        for u in linkler:
            d = _fi_kap_istek(s, "GET", u)
            if d is None:
                continue
            b = d.content; i = b.find(b"%PDF")
            ad = re.findall(r"filename\*=UTF-8''([^;]+)", d.headers.get("content-disposition", "")) or [u.rsplit("/", 1)[-1] + ".pdf"]
            dosya = os.path.join(kl, f"{int(row.indeks)}__{ad[0]}")
            with open(dosya, "wb") as f:
                f.write(b[i:] if i >= 0 else b)
            yeni.append({"indeks": int(row.indeks), "dosya": dosya})
            time.sleep(A.kapfon_bekle)
        if not linkler:
            yeni.append({"indeks": int(row.indeks), "dosya": ""})
        if no % 25 == 0 or no == len(H):
            E = pd.concat([E, pd.DataFrame(yeni)], ignore_index=True); yeni = []
            E.to_csv(yol, index=False)
            filog.info("KAP ek %d/%d rapor, %.0f sn", no, len(H), time.time() - t0)
    return E


def _fi_pdf_metin(dosya: str) -> str:
    """PDF -> duz metin (sutun duzeni korunur). Once pdftotext, yoksa pypdf."""
    import subprocess
    try:
        return subprocess.run(["pdftotext", "-layout", dosya, "-"], capture_output=True, timeout=60, check=True).stdout.decode("utf-8", "replace")
    except Exception:
        from pypdf import PdfReader
        return "\n".join((p.extract_text(extraction_mode="layout") or "") for p in PdfReader(dosya).pages)


def _fi_sayi(x: str) -> float:
    return float(x.replace(".", "").replace(",", "."))


import re as _fi_re
_FI_ISLEM_RE = _fi_re.compile(r"^\s*([A-Z][A-Z0-9]{2,5})\s+.*?(\d{2}/\d{2}/\d{2,4})\s+([\d.]+,\d+)\s+([\d.]+,\d+)\s*$")
_FI_POZ_RE = _fi_re.compile(r"^\s*([A-Z][A-Z0-9]{2,5})\s+TL\s+.*?(TR[A-Z0-9]{10})\s+([\d.]+,\d{2})\s")


def fi_k9_ayristir(metin: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Portfoy dagilim raporu metni -> (hisse alis/satis islemleri, hisse pozisyonlari). Islem: kod, tarih, fiyat, deger, lot = deger/fiyat.
    Pozisyon: kod, ISIN, nominal (pay adedi)."""
    islem, poz = [], []; kip = None; poz_kip = False
    for satir in metin.splitlines():
        u = satir.upper()
        if "HİSSE SENETLERİ(ALIŞLAR)" in u or "HISSE SENETLERI(ALIŞLAR)" in u or "HİSSE SENETLERİ (ALIŞLAR)" in u:
            kip = "alis"; continue
        if "HİSSE SENETLERİ(SATIŞLAR)" in u or "HISSE SENETLERI(SATIŞLAR)" in u or "HİSSE SENETLERİ (SATIŞLAR)" in u:
            kip = "satis"; continue
        if _fi_re.match(r"^\s*[B-Z]\s?\)", satir) or _fi_re.match(r"^\s*[IVX]+-", satir):
            kip = None
        if _fi_re.match(r"^\s*III-FON PORTF", u):
            poz_kip = True; continue
        if _fi_re.match(r"^\s*IV-", u):
            poz_kip = False
        if kip:
            m = _FI_ISLEM_RE.match(satir)
            if m:
                fiyat = _fi_sayi(m.group(3)); deger = _fi_sayi(m.group(4))
                if fiyat > 0:
                    gun, ay, yil = m.group(2).split("/"); yil = ("20" + yil) if len(yil) == 2 else yil
                    islem.append({"kod": m.group(1), "yon": kip, "tarih": f"{yil}-{ay}-{gun}", "fiyat": fiyat, "deger": deger,
                                  "lot": deger / fiyat})
        elif poz_kip:
            m = _FI_POZ_RE.match(satir)
            if m:
                poz.append({"kod": m.group(1), "isin": m.group(2), "nominal": _fi_sayi(m.group(3))})
    return islem, poz


def fi_k9_tablolar(L: pd.DataFrame, E: pd.DataFrame, A: FIAyar) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Indirilen PDF'leri ayristirir. Donus: (islemler, pozisyonlar) — fon, sirket, donem bilgisiyle."""
    meta = L.set_index(L.indeks.astype(int))
    son = set(L.assign(indeks=L.indeks.astype(int)).groupby(["fon", "yil", "donem"]).indeks.max())   # duzeltme raporu varsa en sonu
    I, P = [], []
    for row in E[(E.dosya.astype(str) != "") & E.indeks.astype(int).isin(son)].itertuples(index=False):
        try:
            m = meta.loc[int(row.indeks)]
            islem, poz = fi_k9_ayristir(_fi_pdf_metin(row.dosya))
            ek = {"fon": m.fon, "unvan": m.unvan, "yil": m.yil, "donem": m.donem, "indeks": int(row.indeks)}
            I += [{**ek, **x} for x in islem]; P += [{**ek, **x} for x in poz]
        except Exception as ex:
            filog.warning("rapor %s ayristirilamadi: %s", row.indeks, ex)
    I = pd.DataFrame(I); P = pd.DataFrame(P)
    if len(I):
        I["tarih"] = pd.to_datetime(I.tarih, errors="coerce")
    return I, P


# ---------------------------------------------------------------- K5 rapor
def fi_k5_rapor(kos: pd.DataFrame, faz: pd.DataFrame, tet: pd.DataFrame, oz: pd.DataFrame, iz: pd.DataFrame,
                ekler: Optional[Dict[str, pd.DataFrame]] = None) -> str:
    fm = faz.groupby("faz").median(numeric_only=True).reindex(["ONCE", "ERKEN", "KOSU", "COKUS"])
    kos = kos.copy(); tet = tet.copy()
    for t, kol in ((kos, ("dip", "x2", "tepe")), (tet, ("ilk_iz",))):
        for c in kol:
            t[c] = pd.to_datetime(t[c]).dt.date
    sat = [f"# FON_IZI — {FI_SURUM}", "",
           "Soru (Cemal, 22 Eki): tasfiye fonlarinin topladigi hisseler (20-290 kat) yukselise giderken nasil bir iz birakti?", "",
           "## Vaka kosulari (dip -> tepe, 15 Eyl 2026 oncesi; duzeltilmis fiyat)", "", kos.round(2).to_markdown(index=False), "",
           "## Faz medyanlari (23 hisse)", "", fm.round(2).to_markdown(), "",
           "## Faz ayrintisi", "", faz.round(2).to_markdown(index=False), "",
           "## Iz B ilk tetik (gercek zamanli) ve sonrasi", "", tet.round(2).to_markdown(index=False), "",
           "## Evren testi: iz varyantlari (4 dilim, kat = once 2 kat orani / ayni yukselisin izsiz kismi)", "",
           iz.round(2).to_markdown(index=False), "", "## Dilim ayrintisi", "", oz.round(2).to_markdown(index=False), ""]
    for baslik, t in (ekler or {}).items():
        sat += [f"## {baslik}", "", t.round(2).to_markdown(index=False), ""]
    return "\n".join(sat)


def fon_izi(A: Optional[FIAyar] = None) -> Dict[str, Any]:
    A = A or FIAyar()
    os.makedirs(A.cikti, exist_ok=True)
    veri = {}
    for pazar, yol in A.veri.items():
        try:
            veri[pazar] = fi_k1_veri(yol, pazar, A)
        except Exception as ex:
            filog.error("%s verisi okunamadi (%s); bu pazar atlandi", pazar, ex)
    if "BIST" not in veri:
        raise RuntimeError("BIST verisi yok; vaka incelemesi yapilamaz")
    kos, faz, tet = fi_k3_vaka(veri["BIST"], A)
    O = pd.concat([fi_k4_olaylar(V, p, A) for p, V in veri.items()], ignore_index=True)
    oz, iz = fi_ozet(O)
    ekler: Dict[str, pd.DataFrame] = {}; zbayrak: Dict[str, pd.Series] = {}
    try:
        hoz, hhisse, zbayrak = fi_k3b_hacim_vaka(veri["BIST"], kos, A)
        HO = pd.concat([fi_k4b_hacim_olaylar(V, p, A) for p, V in veri.items()], ignore_index=True)
        hev, hiz = fi_ozet_hacim(HO)
        hoz.to_csv(os.path.join(A.cikti, "fon_hacim_vaka.csv"), index=False)
        hhisse.to_csv(os.path.join(A.cikti, "fon_hacim_hisse.csv"), index=False)
        HO.to_csv(os.path.join(A.cikti, "fon_hacim_olaylar.csv.gz"), index=False)
        hev.to_csv(os.path.join(A.cikti, "fon_hacim_ozet.csv"), index=False)
        pd.DataFrame([{"sembol": s, "tarih": t} for s, z in zbayrak.items() for t in z[z].index]).to_csv(
            os.path.join(A.cikti, "fon_z0_gunleri.csv"), index=False)
        ekler = {"v1.1 HACIM ESLIGI: fon hisselerinin sessiz yuvarlanma (Z0) bolgeleri vs diger BIST hisseleri (2024-26)": hoz,
                 "v1.1 Fon hisseleri Z0 icindeki hacim (hisse basina medyan)": hhisse,
                 "v1.1 Evren testi: Z0 + hacim varyantlari (kat = varyant / Z0'in geri kalani)": hiz,
                 "v1.1 Evren dilim ayrintisi": hev}
    except Exception as ex:  # hacim eki bozulursa v1.0 sonuclari yine yazilir
        filog.error("v1.1 hacim esligi yazilamadi: %s", ex)
    kos.to_csv(os.path.join(A.cikti, "fon_kosular.csv"), index=False)
    faz.to_csv(os.path.join(A.cikti, "fon_fazlar.csv"), index=False)
    tet.to_csv(os.path.join(A.cikti, "fon_iz_tetik.csv"), index=False)
    O.to_csv(os.path.join(A.cikti, "fon_izi_olaylar.csv.gz"), index=False)
    oz.to_csv(os.path.join(A.cikti, "fon_izi_ozet.csv"), index=False)
    rapor = fi_k5_rapor(kos, faz, tet, oz, iz, ekler)
    with open(os.path.join(A.cikti, "FON_IZI_rapor.md"), "w", encoding="utf-8") as f:
        f.write(rapor)
    return {"kosular": kos, "fazlar": faz, "tetik": tet, "olaylar": O, "ozet": oz, "iz": iz, "veri": veri, "ekler": ekler}


def _cakisma_kontrol_fi(_once=_CK_ONCE_FI, _dosya='FON_IZI.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_FI', '_CK_KAYIT', '_cakisma_kontrol_fi', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'pickle', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_fi()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gosterge":
        R = fon_izi_gosterge()
        print(R["iz"].round(2).to_string(index=False))
        sys.exit(0)
    R = fon_izi()
    print(R["iz"].round(2).to_string(index=False))
    print(R["fazlar"].groupby("faz").median(numeric_only=True).round(2).to_string())
