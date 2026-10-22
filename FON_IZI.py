# =====================================================================
#  FON_IZI — tasfiye fonlarinin topladigi hisselerin yukselis oncesi/sirasi izi   (2026-10-22, v1.0)
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
#  KURAL_MOTORU: K1 veri+duzeltme  K2 gunluk/pencere olculeri  K3 vaka fazlari  K4 evren olaylari + ozet  K5 rapor
#  Calistirma: FI_VERI_BIST=... FI_VERI_ABD=... python FON_IZI.py   Cikti: arastirma_cikti/fon_izi/
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

FI_SURUM = "FON_IZI v1.0 (2026-10-22, tasfiye fonu hisselerinin yukselis izi + evren testi)"
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


# ---------------------------------------------------------------- K5 rapor
def fi_k5_rapor(kos: pd.DataFrame, faz: pd.DataFrame, tet: pd.DataFrame, oz: pd.DataFrame, iz: pd.DataFrame) -> str:
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
    kos.to_csv(os.path.join(A.cikti, "fon_kosular.csv"), index=False)
    faz.to_csv(os.path.join(A.cikti, "fon_fazlar.csv"), index=False)
    tet.to_csv(os.path.join(A.cikti, "fon_iz_tetik.csv"), index=False)
    O.to_csv(os.path.join(A.cikti, "fon_izi_olaylar.csv.gz"), index=False)
    oz.to_csv(os.path.join(A.cikti, "fon_izi_ozet.csv"), index=False)
    rapor = fi_k5_rapor(kos, faz, tet, oz, iz)
    with open(os.path.join(A.cikti, "FON_IZI_rapor.md"), "w", encoding="utf-8") as f:
        f.write(rapor)
    return {"kosular": kos, "fazlar": faz, "tetik": tet, "olaylar": O, "ozet": oz, "iz": iz, "veri": veri}


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
    R = fon_izi()
    print(R["iz"].round(2).to_string(index=False))
    print(R["fazlar"].groupby("faz").median(numeric_only=True).round(2).to_string())
