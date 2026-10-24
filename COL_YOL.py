# =====================================================================
#  COL_YOL — Obek -> alim -> CIKIS: cikis kurali varyantlarinin kar/zarar testi   (2026-10-21, v1.0)
#
#  CEMAL (21 Eki): "Cikisi bilmiyorum; her seyi test edip kurala donusturelim. %8 dedim ama 5 / 10 / 20 olsa? Gozlemim:
#    %8 gelince stop maliyete, %10 gelince stop maliyetin %2 ustune gibi bir yol para eder gibi."
#
#  YOL (ileriye bakis yok): obek sinyali (COL_OBEK tanimi) -> 60 gun icinde ALIM (yesil mumun kapanisi obek tavani x AL_PAY ustunde;
#    once dip -%2 altina kapanirsa dustu, islem yok) -> ertesi gun ACILIS giris -> ilk stop = obek dibi x (1 - %2) -> cikis varyanti
#    -> en gec 120 bar sonra kapanistan cikis. Stop tetiklenirse cikis = stop fiyati (acilis stopun altindaysa acilis). Maliyet %0,4.
#  CIKIS VARYANTLARI
#    stop_ufuk     : yalniz ilk stop, 120 barda cik
#    maliyet_5/8/10/20 : zirve +%t gorulunce stop maliyete (giris fiyati); sonra stop ya da 120 bar
#    cemal         : +%8 -> stop maliyet, +%10 -> maliyet +%2 (Cemal'in gozlemi)
#    merdiven      : +8->0, +10->+2, +15->+7, +20->+12, +30->+20, +50->+35 (zirve yukseldikce stop basamakla yukari)
#    zirve10       : +%8 gorulunce stop = zirvenin %10 alti (iz suren)
#    maliyet8_sma20: +%8'de maliyete; +%20 gorulunce SMA20 alti kapanista cik (mevcut trail ile birlesik)
#    mevcut        : mevcut sistem (+%20 sonra SMA20 trail, 120 bar) + ilk stop
#    mevcut_stopsuz: mevcut sistem, stop yok (COL_DIP_TEST ile ayni)
#    hedef_5/8/10/15/20: alim gelince ilk dokunusta sabit hedefte sat; gelmezse ilk stop; 120 barda kapanis (Cemal 21 Eki)
#  Stop seviyesi, bir onceki barin zirvesine gore guncellenir (ayni bar icinde hem yukselip hem stop olmak temkinli sayilir).
#  TABAN: ayni yol, obek sarti aranmadan her 5. gunun son 15 mumu kutu sayilarak (COL_OBEK tabani). Oran 1,3x kurali icin.
#  OLCULER: donem basina n, kazanan %, ort (%200'de kirpili) / medyan, agir kayip % (< -20), stopla cikan %, ort bar, slot portfoy (30 slot).
#  KURAL_MOTORU: K1 veri  K2 islemler (obek + taban)  K3 cikis varyantlari (vektorel)  K4 ozet  K5 rapor
#  Calistirma: GitHub Actions 'Arastirma' (betik: COL_YOL.py). Cikti: arastirma_cikti/col_yol/. OLCUM; kural sonucla konur.
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CY = {k: id(v) for k, v in globals().items()}

CY_SURUM = "COL_YOL v1.3 (2026-10-24, denetim: kopya islem, hisse basina tek slot, trail ufuksuz, slot bandi)"
cylog = logging.getLogger("col.yol")
if not cylog.handlers:
    _cy_h = logging.StreamHandler(sys.stderr)
    _cy_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yol: %(message)s", "%H:%M:%S"))
    cylog.addHandler(_cy_h)
    cylog.setLevel(logging.INFO)
    cylog.propagate = False


@dataclass
class CYAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    al_pay: float = 1.002
    boz_tol: float = 0.02
    alim_bekle: int = 60
    ufuk: int = 120
    maliyet: float = 0.4
    agir: float = -20.0
    slot: int = 30
    taban_adim: int = 5
    taban_w: int = 15
    donemler: Tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                       ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))
    abd: bool = True               # ABD evreni (COL_DIP_TEST.cd_k1_abd, yfinance ~5 dk), CLAUDE.md test standardi
    donemler_abd: Tuple = (("ABD 2022-23", "2022-01-01", "2023-12-31"), ("ABD 2024-26", "2024-01-01", "2026-12-31"))
    # varyant adi -> (basamak esikleri %, stop seviyeleri % [girise gore]; 'zirve' iz; sma20 trail esigi)
    varyantlar: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "stop_ufuk": {},
        "maliyet_5": {"T": [5], "S": [0]},
        "maliyet_8": {"T": [8], "S": [0]},
        "maliyet_10": {"T": [10], "S": [0]},
        "maliyet_20": {"T": [20], "S": [0]},
        "cemal": {"T": [8, 10], "S": [0, 2]},
        "merdiven": {"T": [8, 10, 15, 20, 30, 50], "S": [0, 2, 7, 12, 20, 35]},
        "zirve10": {"zirve": (8, 10)},                        # +%8'den sonra zirvenin %10 alti
        "maliyet8_sma20": {"T": [8], "S": [0], "sma20": 20},
        "mevcut": {"sma20": 20},
        "mevcut_stopsuz": {"sma20": 20, "stopsuz": True},
        # Cemal 21 Eki: "alim gelince beklemeden %5 / %8 / %10 al cik; gelmezse kutu dibi -2'de stop"
        "hedef_5": {"hedef": 5},
        "hedef_8": {"hedef": 8},
        "hedef_10": {"hedef": 10},
        "hedef_15": {"hedef": 15},
        "hedef_20": {"hedef": 20},
    })


def _cy_mod():
    import importlib
    kok = CYAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST"), importlib.import_module("COL_OBEK")


# ------------------------------------------------------------------ K2 islemler
def cy_alim(ay: CYAyar, O: np.ndarray, C: np.ndarray, e: int, tavan: float, dip: float) -> Optional[int]:
    """e'den sonra alim_bekle bar icinde ilk YESIL kapanis > tavan*al_pay -> bar indeksi; once dip altina kapanirsa None."""
    n = len(C)
    tv, dp = tavan * ay.al_pay, dip * (1 - ay.boz_tol)
    for i in range(e + 1, min(n, e + 1 + ay.alim_bekle)):
        if C[i] > tv and C[i] > O[i]:
            return i
        if C[i] < dp:
            return None
    return None


def cy_k2_islemler(ay: CYAyar, CO, veri: Dict[str, pd.DataFrame]) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, np.ndarray]]]:
    """Obek ve taban islemleri: (sembol, kaynak, sinyal_i, alim_i, giris_i, stop0). Fiyat dizileri hisse basina saklanir."""
    t0 = time.monotonic()
    oay = CO.COAyar(kok=ay.kok)
    isl: List[Dict[str, Any]] = []
    D: Dict[str, Dict[str, np.ndarray]] = {}
    for k, (sem, df) in enumerate(veri.items()):
        df = df[np.isfinite(df.Close)]
        if len(df) < oay.min_gecmis + 20:
            continue
        try:
            sig, A = CO.co_k2_tespit(oay, df)
        except Exception as ex:
            cylog.debug("%s: %s", sem, ex); continue
        O, H, L, C = A["O"], A["H"], A["L"], A["C"]
        n = len(C)
        A["S20"] = df.Close.rolling(20, min_periods=20).mean().to_numpy(float)
        A["ix"] = df.index
        D[sem] = A
        gorulen: set = set()          # denetim 24 Eki: ardisik obek sinyalleri ayni alim barina dusuyordu (BIST 50.006 -> 24.838 tekil)
        for r in sig:
            b = cy_alim(ay, O, C, r["e"], r["tavan"], r["dip"])
            if b is not None and b + 1 < n and b not in gorulen:
                gorulen.add(b)
                isl.append({"sembol": sem, "kaynak": "obek", "sinyal_i": r["e"], "alim_i": b, "giris_i": b + 1,
                            "stop0": r["dip"] * (1 - ay.boz_tol), "w": r["w"]})
        gorulen_t: set = set()
        for e in range(oay.min_gecmis, n - 1, ay.taban_adim):
            tavan, dip = H[e - ay.taban_w + 1:e + 1].max(), L[e - ay.taban_w + 1:e + 1].min()
            b = cy_alim(ay, O, C, e, tavan, dip)
            if b is not None and b + 1 < n and b not in gorulen_t:
                gorulen_t.add(b)
                isl.append({"sembol": sem, "kaynak": "taban", "sinyal_i": e, "alim_i": b, "giris_i": b + 1,
                            "stop0": dip * (1 - ay.boz_tol), "w": ay.taban_w})
        if (k + 1) % 100 == 0:
            cylog.info("K2: %d/%d hisse | %d islem (%.0f sn)", k + 1, len(veri), len(isl), time.monotonic() - t0)
    cylog.info("K2 bitti: %d islem (obek %d, taban %d) (%.0f sn)", len(isl), sum(i['kaynak'] == 'obek' for i in isl),
               sum(i['kaynak'] == 'taban' for i in isl), time.monotonic() - t0)
    return isl, D


# ------------------------------------------------------------------ K3 cikis (vektorel)
def cy_cikis(ay: CYAyar, v: Dict[str, Any], O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, S20: np.ndarray,
             g: int, stop0: float) -> Tuple[int, float, str]:
    """Giris g (acilis). Donus: (cikis_i, cikis_fiyat, neden). neden: stop | trail | ufuk | veri_sonu."""
    n = len(C)
    trail = "sma20" in v
    son = n if trail else min(n, g + ay.ufuk)       # denetim 24 Eki: uretimde trail'deki isleme ufuk yok (takip.py); yalniz hedefsize 120 bar
    p0 = O[g]
    o, h, l, c, s = O[g:son], H[g:son], L[g:son], C[g:son], S20[g:son]
    m = len(c)
    cm = np.maximum.accumulate(h)
    cm_prev = np.r_[p0, cm[:-1]]                       # bir onceki barin zirvesi (ayni bar temkinli)
    kaz = cm_prev / p0 * 100 - 100                      # su ana kadar gorulen en yuksek kazanc (%)
    stop = np.full(m, -np.inf if v.get("stopsuz") else stop0)
    if "T" in v:
        T = np.asarray(v["T"], float); S = np.asarray(v["S"], float)
        idx = np.searchsorted(T, kaz, side="right") - 1
        sev = np.where(idx >= 0, p0 * (1 + S[np.clip(idx, 0, len(S) - 1)] / 100), -np.inf)
        stop = np.maximum(stop, sev)
    if "zirve" in v:
        esik, pay = v["zirve"]
        sev = np.where(kaz >= esik, cm_prev * (1 - pay / 100), -np.inf)
        stop = np.maximum(stop, sev)
    hit = l <= stop
    k_stop = int(np.argmax(hit)) if hit.any() else None
    k_trail = None
    if "sma20" in v:
        hv = kaz >= v["sma20"]                          # hedef gorulmus mu (onceki bara kadar)
        tr = hv & np.isfinite(s) & (c < s)
        k_trail = int(np.argmax(tr)) if tr.any() else None
    k_hedef = None
    if "hedef" in v:
        hp = p0 * (1 + v["hedef"] / 100)
        hh = h >= hp
        k_hedef = int(np.argmax(hh)) if hh.any() else None
    k_ufuk = None
    if trail:
        uf = (np.arange(m) >= ay.ufuk - 1) & ~hv
        k_ufuk = int(np.argmax(uf)) if uf.any() else None
    aday = [(k_stop, "stop"), (k_trail, "trail"), (k_hedef, "hedef"), (k_ufuk, "ufuk")]
    aday = [(k, ad) for k, ad in aday if k is not None]
    if aday:
        # ayni barda stop ve hedef birlikte -> temkinli: stop (siralama: stop < trail < hedef < ufuk)
        sira = {"stop": 0, "trail": 1, "hedef": 2, "ufuk": 3}
        k, ad = min(aday, key=lambda z: (z[0], sira[z[1]]))
        if ad == "stop":
            fiyat = min(o[k], stop[k]) if o[k] < stop[k] else stop[k]
            return g + k, float(fiyat), "stop"
        if ad == "hedef":
            hp = p0 * (1 + v["hedef"] / 100)
            return g + k, float(max(o[k], hp)), "hedef"       # acilis hedefin ustundeyse acilistan
        return g + k, float(c[k]), ad
    k = m - 1
    return g + k, float(c[k]), ("ufuk" if (not trail and son == g + ay.ufuk) else "veri_sonu")


def cy_k3_varyantlar(ay: CYAyar, isl: List[Dict[str, Any]], D: Dict[str, Dict[str, np.ndarray]]) -> pd.DataFrame:
    t0 = time.monotonic()
    rows: List[Dict[str, Any]] = []
    for j, r in enumerate(isl):
        A = D[r["sembol"]]
        O, H, L, C, S20, ix = A["O"], A["H"], A["L"], A["C"], A["S20"], A["ix"]
        g = r["giris_i"]; p0 = O[g]
        if not (np.isfinite(p0) and p0 > 0):
            continue
        for ad, v in ay.varyantlar.items():
            ci, cf, neden = cy_cikis(ay, v, O, H, L, C, S20, g, r["stop0"])
            rows.append({"sembol": r["sembol"], "kaynak": r["kaynak"], "varyant": ad, "sinyal": ix[r["sinyal_i"]], "giris": ix[g],
                         "cikis": ix[ci], "bar": ci - g, "neden": neden, "getiri": (cf / p0 - 1) * 100 - ay.maliyet,
                         "mfe": (H[g:ci + 1].max() / p0 - 1) * 100})
        if (j + 1) % 20000 == 0:
            cylog.info("K3: %d/%d islem (%.0f sn)", j + 1, len(isl), time.monotonic() - t0)
    T = pd.DataFrame(rows)
    cylog.info("K3 bitti: %d satir (%.0f sn)", len(T), time.monotonic() - t0)
    return T


# ------------------------------------------------------------------ K4 ozet
def cy_k4_ozet(ay: CYAyar, CD, T: pd.DataFrame, donemler: Optional[Tuple] = None) -> pd.DataFrame:
    rows = []
    for ad, b, s_ in (donemler or ay.donemler):
        x0 = T[(T.sinyal >= b) & (T.sinyal <= s_) & (T.neden != "veri_sonu")]     # denetim: veri sonunda acik islem kapanmis sayilmaz
        for kaynak in ("obek", "taban"):
            for var in ay.varyantlar:
                x = x0[(x0.kaynak == kaynak) & (x0.varyant == var)]
                if x.empty:
                    continue
                g = x.getiri
                r = {"donem": ad, "kaynak": kaynak, "varyant": var, "n": len(x), "kazanan_%": round(100 * (g > 0).mean(), 1),
                     "ort_%": round(g.clip(upper=200).mean(), 2), "medyan_%": round(g.median(), 2),
                     "agir_%": round(100 * (g < ay.agir).mean(), 1), "stop_%": round(100 * (x.neden == "stop").mean(), 1),
                     "ort_bar": round(x.bar.mean(), 0), "mfe_medyan": round(x.mfe.median(), 1)}
                if kaynak == "obek":
                    port, port_sd, al, atla = CD._cd_slot_bant(x.assign(getiri=x.getiri.clip(upper=200)), ay.slot)
                    r.update(slot_portfoy_pct=round(port, 1), slot_sd=round(port_sd, 1), slot_alinan=int(round(al)), slot_atlanan=int(round(atla)))
                rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ K5 rapor
def cy_k5_rapor(ay: CYAyar, oz: pd.DataFrame, cikti: str, donemler: Optional[Tuple] = None, pazar: str = "BIST") -> str:
    donemler = donemler or ay.donemler
    sat = [f"# COL YOL — obek -> alim -> cikis varyantlari — {pazar}   ({CY_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Yol: obek sinyali -> 60 gunde yesil kapanis > obek tavani -> ertesi acilis giris -> ilk stop obek dibi -%2 -> cikis varyanti -> en gec 120 bar.",
           "Maliyet %0,4. Ortalama %200'de kirpili (kurus hisse veri sicramasi). Taban: obek aranmadan her 5. gunun 15 mumluk kutusu, ayni yol.",
           "Slot portfoy: 30 slot, esit agirlik, giris sirasi, dolu ise atla, hisse basina tek pozisyon; ayni gun sirasi 20 kez rastgele, ortalama (yalniz obek).",
           "v1.3 denetim: ayni alim barina dusen obek sinyalleri tek islem; trail varyantlarinda 120 bar ufku yalniz hedef gorulmemise; veri sonunda acik islem disarida.", ""]
    for ad, _, _ in donemler:
        x = oz[oz.donem == ad]
        if x.empty:
            continue
        sat += [f"## {ad}", "", "| varyant | OBEK n | kazanan | ort / medyan | agir | stop | bar | slot portfoy | TABAN n | kazanan | ort / medyan | agir | stop |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for var in ay.varyantlar:
            o = x[(x.kaynak == "obek") & (x.varyant == var)]
            t = x[(x.kaynak == "taban") & (x.varyant == var)]
            if o.empty:
                continue
            o = o.iloc[0]; t = t.iloc[0] if len(t) else None
            sat.append(f"| {var} | {o.n} | %{o['kazanan_%']:.0f} | {o['ort_%']:+.1f} / {o['medyan_%']:+.1f} | %{o['agir_%']:.0f} | %{o['stop_%']:.0f} | {o.ort_bar:.0f} | "
                       f"{o.slot_portfoy_pct:+.0f}% ({o.slot_alinan}/{o.slot_alinan + o.slot_atlanan}) | "
                       + (f"{t.n} | %{t['kazanan_%']:.0f} | {t['ort_%']:+.1f} / {t['medyan_%']:+.1f} | %{t['agir_%']:.0f} | %{t['stop_%']:.0f} |" if t is not None else "- | - | - | - | - |"))
        sat.append("")
    # dort donemde en iyi: ort ve kazanan siralamasi
    sat += [f"## {pazar} donemleri birlikte (obek): varyant basina donem ortalamalarinin ortalamasi", "", "| varyant | kazanan | ort | medyan | agir | slot portfoy ort |", "|---|---|---|---|---|---|"]
    o = oz[oz.kaynak == "obek"].groupby("varyant").agg(kazanan=("kazanan_%", "mean"), ort=("ort_%", "mean"), medyan=("medyan_%", "mean"),
                                                        agir=("agir_%", "mean"), slot=("slot_portfoy_pct", "mean")).sort_values("ort", ascending=False)
    for var, r in o.iterrows():
        sat.append(f"| {var} | %{r.kazanan:.0f} | {r.ort:+.1f} | {r.medyan:+.1f} | %{r.agir:.0f} | {r.slot:+.0f}% |")
    sat += ["", "Not: taban ile kiyas 'obek ne ekliyor' sorusuna, varyantlar arasi kiyas 'cikis nasil olmali' sorusuna bakar. OLCUM; kural sonucla.", ""]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_YOL_rapor.md" if pazar == "BIST" else f"COL_YOL_rapor_{pazar}.md"), "w", encoding="utf-8").write(metin)
    return metin


def _yol_pazar(ay: CYAyar, CD, CO, veri: Dict[str, pd.DataFrame], cikti: str, donemler: Tuple, pazar: str) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
    isl, D = cy_k2_islemler(ay, CO, veri)
    T = cy_k3_varyantlar(ay, isl, D)
    ek = "" if pazar == "BIST" else f"_{pazar}"
    T.to_csv(os.path.join(cikti, f"col_yol_islemler{ek}.csv.gz"), index=False)
    oz = cy_k4_ozet(ay, CD, T, donemler)
    oz.to_csv(os.path.join(cikti, f"col_yol_ozet{ek}.csv"), index=False)
    return T, oz, cy_k5_rapor(ay, oz, cikti, donemler, pazar)


def col_yol(ay: Optional[CYAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or CYAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_yol")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD, CO = _cy_mod()
    cay = CD.CDAyar(kok=ay.kok)
    if veri is None:
        veri = CD.cd_k1_bist(cay); CD.cd_k2_onarim(cay, veri)
    T, oz, metin = _yol_pazar(ay, CD, CO, veri, cikti, ay.donemler, "BIST")
    out: Dict[str, Any] = {"islemler": T, "ozet": oz, "rapor": metin, "cikti": cikti}
    if ay.abd:
        try:
            veri_abd = CD.cd_k1_abd(cay)
            Ta, oza, ma = _yol_pazar(ay, CD, CO, veri_abd, cikti, ay.donemler_abd, "ABD")
            out.update(islemler_abd=Ta, ozet_abd=oza, rapor_abd=ma)
            metin = metin + "\n" + ma
        except Exception as ex:
            cylog.error("ABD: %s", ex)
            out["rapor_abd"] = f"ABD calismadi: {ex}"
    out["rapor"] = metin
    cylog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return out


def _cakisma_kontrol_cy(_once=_CK_ONCE_CY, _dosya='COL_YOL.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CY', '_CK_KAYIT', '_cakisma_kontrol_cy', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_cy()

if __name__ == "__main__":
    R = col_yol()
    print(R["rapor"])
