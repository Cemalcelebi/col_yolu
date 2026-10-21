# =====================================================================
#  COL_KAZANC — Uretim yolu sabit, ustune HANGI SART eklenirse kazanc artar?   (2026-10-21, v1.0)
#
#  CEMAL (21 Eki): "Her sey ayni kalsin, mevcut koda ne eklersek iyi kazanc olur? Ornegin hacim col obeklerinde kurusun,
#    alim mumu ile 2-3-4 kati gelsin — hangisi kazandiriyor? Butun olasiliklari hesapla."
#
#  YOL (uretim, COL_YOL ile ayni, ileriye bakis yok): obek sinyali (COL_OBEK) -> 60 gun icinde ALIM (yesil mumun kapanisi > obek
#    tavani x AL_PAY; once dip -%2 altina kapanirsa islem yok) -> ertesi acilis giris -> ilk stop obek dibi -%2 (T6) ->
#    +%8 gorulunce stop maliyete (T10) -> +%20 gorulunce SMA20 alti kapanista cik -> en gec 120 bar. Maliyet %0,4.
#  OLCULER (hepsi alim gunu kapanisinda bilinir): alim gunu hacim / obek hacim medyani (Cemal'in 2-3-4 kati), alim hacmi / 60g,
#    obek hacmi / onceki 60g (kuruma), obek son hafta hacmi / obek, alim mumunun kapanis konumu (clv), alim mumu boyu / obek mumu,
#    tavanin ne kadar ustunde kapandi, acilis boslugu, sinyalden alima gecen bar, obek genisligi/yuksekligi/yuvarlanma/mum kucuklugu,
#    konum250, onceki 60/250 gun getirisi, SMA200 uzakligi, SMA50 egimi, obek oncesi bicak dususu, obek sirasi, onceki obek konumu,
#    piyasa 60g, sektor ruzgari 60g (sektor_BIST alt endeks / sektor_ABD), alim gunu piyasa getirisi, likidite (60g medyan ciro).
#  DEGERLENDIRME: her olcu kovalara bolunur (sabit esikler ya da BIST/ABD icinde terciller). Her kova icin donem basina
#    n, kazanan, ort (%200 kirpili), medyan, agir kayip, 30 slot portfoy; kovanin ort'u o donemdeki TUM obek islemlerinin ort'undan
#    cikarilir (fark). TUTARLILIK = 6 donemin (BIST 16-19, 20-22, 2023, 24-26; ABD 22-23, 24-26) kacinda fark > 0 (n >= 60 olanlar).
#    Taban islemlerinde (obek sarti aranmadan her 5. gunun 15 mumluk kutusu) ayni fark ayrica sayilir: "obek sartindan bagimsiz mi?"
#    En tutarli ikili sartlar VE ile birlestirilip yeniden olculur. CLAUDE.md: tek testte pozitif, baskasinda negatif olan iz sayilmaz.
#  NOT: "kirilim hacmi" COL_OZET 3. bolumde (segment kirilimi cercevesinde) kapanmis konudur; burada Cemal'in istegiyle obek
#    cercevesinde yeniden olculur, sonuc ne cikarsa yazilir. CDS yalniz 2022+ oldugundan donemler arasi tutarlilik olculemez, alinmadi.
#  KURAL_MOTORU: K1 veri  K2 islemler (obek + taban, olculerle)  K3 cikis + piyasa/sektor  K4 kova ozeti  K5 bilesik  K6 rapor
#  Calistirma: GitHub Actions 'Arastirma' (betik: COL_KAZANC.py). Cikti: arastirma_cikti/col_kazanc/. OLCUM; kural sonucla konur.
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CK = {k: id(v) for k, v in globals().items()}

CK_SURUM = "COL_KAZANC v1.0 (2026-10-21)"
cklog = logging.getLogger("col.kazanc")
if not cklog.handlers:
    _ck_h = logging.StreamHandler(sys.stderr)
    _ck_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kazanc: %(message)s", "%H:%M:%S"))
    cklog.addHandler(_ck_h)
    cklog.setLevel(logging.INFO)
    cklog.propagate = False


@dataclass
class CKAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    uretim: Dict[str, Any] = field(default_factory=lambda: {"T": [8], "S": [0], "sma20": 20})   # takip T6 + T10 + trail
    taban: bool = True
    taban_adim: int = 5
    taban_w: int = 15
    abd: bool = True
    min_n: int = 60                 # bir donemde kova sayilacak en az islem
    min_tutarli: int = 5            # 6 donemin en az kaci ayni yonde -> "tutarli"
    agir: float = -20.0
    slot: int = 30
    donemler: Tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                       ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))
    donemler_abd: Tuple = (("ABD 2022-23", "2022-01-01", "2023-12-31"), ("ABD 2024-26", "2024-01-01", "2026-12-31"))
    # olcu -> (kova sinirlari [sag acik], etiketler); None -> tercil (pazar icinde)
    kovalar: Dict[str, Optional[Tuple[List[float], List[str]]]] = field(default_factory=lambda: {
        "hacim_alim_kat": ([-np.inf, 1, 2, 3, 4, np.inf], ["<1", "1-2", "2-3", "3-4", ">=4"]),
        "hacim_alim_kat60": ([-np.inf, 1, 2, 3, 4, np.inf], ["<1", "1-2", "2-3", "3-4", ">=4"]),
        "hacim_obek_kat": ([-np.inf, 0.7, 1.0, 1.5, np.inf], ["<0.7 kuru", "0.7-1", "1-1.5", ">=1.5"]),
        "hacim_son_kat": ([-np.inf, 0.8, 1.2, np.inf], ["<0.8", "0.8-1.2", ">=1.2"]),
        "clv_alim": ([-np.inf, 0.5, 0.8, np.inf], ["<0.5", "0.5-0.8", ">=0.8"]),
        "alim_mum_kat": ([-np.inf, 1.5, 3, np.inf], ["<1.5", "1.5-3", ">=3"]),
        "alim_ustu_pct": ([-np.inf, 1, 3, 6, np.inf], ["<1", "1-3", "3-6", ">=6"]),
        "gap_pct": ([-np.inf, 0, 2, np.inf], ["<0", "0-2", ">=2"]),
        "bekleme": ([-np.inf, 5, 20, np.inf], ["<5", "5-20", ">=20"]),
        "w": ([-np.inf, 15, 20, 25, np.inf], ["10", "15", "20", "25"]),
        "yuv_pct": None, "mum_kat": None, "obek_yuk_pct": None,
        "konum250": ([-np.inf, 0.2, 0.5, np.inf], ["<0.2 dip", "0.2-0.5", ">=0.5"]),
        "onc60": None, "onc250": None,
        "sma200_uzak": ([-np.inf, -10, 0, 10, np.inf], ["<-10", "-10-0", "0-10", ">=10"]),
        "sma50_egim": None,
        "bicak_dusus20": ([-np.inf, -10, -3, np.inf], ["<-10 bicak", "-10--3", ">=-3"]),
        "obek_sira": ([-np.inf, 2, 3, np.inf], ["1", "2", ">=3"]),
        "onceki_obek": None,                                   # kategorik
        "piyasa60": ([-np.inf, -10, 0, 10, np.inf], ["<-10", "-10-0", "0-10", ">=10"]),
        "ruzgar60": ([-np.inf, -5, 5, np.inf], ["<-5", "-5-5", ">=5 ruzgar"]),
        "piy_gun": ([-np.inf, -1, 1, np.inf], ["<-1", "-1-1", ">=1"]),
        "lik60": None,
    })
    kategorik: Tuple[str, ...] = ("onceki_obek",)
    bilesik_en_cok: int = 4         # en tutarli bu kadar ikili sart VE ile birlestirilir


def _ck_mod():
    import importlib
    kok = CKAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST"), importlib.import_module("COL_OBEK"), importlib.import_module("COL_YOL")


# ------------------------------------------------------------------ K2 islemler + olculer
def ck_olcu(A: Dict[str, np.ndarray], r: Dict[str, Any], b: int, onceki: Optional[Dict[str, Any]], sira: int) -> Dict[str, Any]:
    """Alim bari b (kapanis bilinir) ve obek r (s,e,d,tavan,dip,med,ref60,yuv,w) icin olculer. Ileriye bakis yok."""
    O, H, L, C, V, ar = A["O"], A["H"], A["L"], A["C"], A["V"], A["ar"]
    s, e, d = r["s"], r["e"], r["d"]
    vo = float(np.nanmedian(V[s:e + 1])); v60 = float(np.nanmedian(V[max(0, b - 60):b])); vo60 = float(np.nanmedian(V[max(0, s - 60):s]))
    vson = float(np.nanmedian(V[max(s, e - 4):e + 1]))
    rng = H[b] - L[b]
    o250 = max(0, b - 249); lo, hi = float(L[o250:b + 1].min()), float(H[o250:b + 1].max())
    sma200 = float(np.mean(C[max(0, b - 199):b + 1])); sma50 = float(np.mean(C[b - 49:b + 1])); sma50o = float(np.mean(C[b - 59:b - 9]))
    ciro = float(np.nanmedian((C * V)[max(0, b - 60):b]))
    def kat(a, c):
        return round(a / c, 2) if (np.isfinite(a) and np.isfinite(c) and c > 0) else np.nan
    return {"hacim_alim_kat": kat(float(V[b]), vo), "hacim_alim_kat60": kat(float(V[b]), v60), "hacim_obek_kat": kat(vo, vo60),
            "hacim_son_kat": kat(vson, vo), "clv_alim": round(float((C[b] - L[b]) / rng), 2) if rng > 0 else np.nan,
            "alim_mum_kat": kat(float(ar[b]), r["med"]), "alim_ustu_pct": round(float(C[b] / r["tavan"] - 1) * 100, 2),
            "gap_pct": round(float(O[b] / C[b - 1] - 1) * 100, 2), "bekleme": b - e, "w": r["w"], "yuv_pct": round(r["yuv"], 2),
            "mum_kat": round(r["med"] / r["ref60"], 2) if r["ref60"] > 0 else np.nan,
            "obek_yuk_pct": round((r["tavan"] / r["dip"] - 1) * 100, 1),
            "konum250": round((C[b] - lo) / (hi - lo), 2) if hi > lo else np.nan,
            "onc60": round(float(C[b] / C[max(0, b - 60)] - 1) * 100, 1), "onc250": round(float(C[b] / C[max(0, b - 250)] - 1) * 100, 1),
            "sma200_uzak": round((C[b] / sma200 - 1) * 100, 1), "sma50_egim": round((sma50 / sma50o - 1) * 100, 1),
            "bicak_dusus20": round(float(C[max(0, s - 1)] / C[max(0, s - 21)] - 1) * 100, 1),
            "obek_sira": sira,
            "onceki_obek": ("yok" if onceki is None or s - onceki["e"] > 60 else ("asagida" if r["dip"] < onceki["dip"] else "yukarida")),
            "lik60": round(ciro / 1e6, 2)}


def ck_k2_islemler(ay: CKAyar, CO, CY, veri: Dict[str, pd.DataFrame]) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, np.ndarray]]]:
    t0 = time.monotonic()
    oay = CO.COAyar(kok=ay.kok); yay = CY.CYAyar(kok=ay.kok, abd=False)
    isl: List[Dict[str, Any]] = []
    D: Dict[str, Dict[str, np.ndarray]] = {}
    for k, (sem, df) in enumerate(veri.items()):
        df = df[np.isfinite(df.Close)]
        if len(df) < oay.min_gecmis + 20:
            continue
        try:
            sig, A = CO.co_k2_tespit(oay, df)
        except Exception as ex:
            cklog.debug("%s: %s", sem, ex); continue
        O, H, L, C = A["O"], A["H"], A["L"], A["C"]
        n = len(C)
        A["S20"] = df.Close.rolling(20, min_periods=20).mean().to_numpy(float)
        A["ix"] = df.index
        D[sem] = A
        onceki, sira = None, 0
        for r in sig:
            sira = sira + 1 if (onceki is not None and r["s"] - onceki["e"] <= 60) else 1
            b = CY.cy_alim(yay, O, C, r["e"], r["tavan"], r["dip"])
            if b is not None and b + 1 < n and b >= 60:
                isl.append({"sembol": sem, "kaynak": "obek", "sinyal_i": r["e"], "alim_i": b, "giris_i": b + 1,
                            "stop0": r["dip"] * (1 - yay.boz_tol), **ck_olcu(A, r, b, onceki, sira)})
            onceki = r
        if ay.taban:
            for e in range(oay.min_gecmis, n - 1, ay.taban_adim):
                s = e - ay.taban_w + 1
                tavan, dip = float(H[s:e + 1].max()), float(L[s:e + 1].min())
                b = CY.cy_alim(yay, O, C, e, tavan, dip)
                if b is None or b + 1 >= n or b < 60:
                    continue
                d = s + int(np.argmin(L[s:e + 1]))
                med = float(np.nanmedian(A["ar"][s:e + 1])); r60 = float(np.nanmedian(A["ar"][max(0, s - 60):s]))
                y = L[d:e + 1] / dip - 1; kk = max(2, len(y) // 3)
                rt = {"s": s, "e": e, "d": d, "w": ay.taban_w, "tavan": tavan, "dip": dip, "med": med, "ref60": r60,
                      "yuv": float(np.median(y[-kk:]) * 100) if len(y) >= 2 * kk else np.nan}
                isl.append({"sembol": sem, "kaynak": "taban", "sinyal_i": e, "alim_i": b, "giris_i": b + 1,
                            "stop0": dip * (1 - yay.boz_tol), **ck_olcu(A, rt, b, None, 1)})
        if (k + 1) % 100 == 0:
            cklog.info("K2: %d/%d hisse | %d islem (%.0f sn)", k + 1, len(veri), len(isl), time.monotonic() - t0)
    cklog.info("K2 bitti: %d islem (obek %d, taban %d) (%.0f sn)", len(isl), sum(i["kaynak"] == "obek" for i in isl),
               sum(i["kaynak"] == "taban" for i in isl), time.monotonic() - t0)
    return isl, D


# ------------------------------------------------------------------ K3 cikis + piyasa
def ck_k3_cikis(ay: CKAyar, CY, isl: List[Dict[str, Any]], D: Dict[str, Dict[str, np.ndarray]]) -> pd.DataFrame:
    t0 = time.monotonic()
    yay = CY.CYAyar(kok=ay.kok, abd=False)
    rows: List[Dict[str, Any]] = []
    for r in isl:
        A = D[r["sembol"]]
        O, H, L, C, S20, ix = A["O"], A["H"], A["L"], A["C"], A["S20"], A["ix"]
        g = r["giris_i"]; p0 = O[g]
        if not (np.isfinite(p0) and p0 > 0):
            continue
        ci, cf, neden = CY.cy_cikis(yay, ay.uretim, O, H, L, C, S20, g, r["stop0"])
        rows.append({**{k: v for k, v in r.items() if k not in ("sinyal_i", "alim_i", "giris_i", "stop0")},
                     "sinyal": ix[r["sinyal_i"]], "alim": ix[r["alim_i"]], "giris": ix[g], "cikis": ix[ci], "bar": ci - g, "neden": neden,
                     "getiri": (cf / p0 - 1) * 100 - yay.maliyet})
    T = pd.DataFrame(rows)
    cklog.info("K3 cikis bitti: %d islem (%.0f sn)", len(T), time.monotonic() - t0)
    return T


def ck_k3_piyasa(ay: CKAyar, veri: Dict[str, pd.DataFrame], T: pd.DataFrame, pazar: str) -> pd.DataFrame:
    """Alim gunune: piyasa 60g medyan getirisi, sektor ruzgari 60g (sepet medyani - piyasa), alim gunu piyasa medyan getirisi."""
    if T.empty:
        return T
    K = pd.DataFrame({s: df.Close for s, df in veri.items()}).sort_index().ffill()
    g60 = K / K.shift(60) - 1
    piy60 = g60.median(axis=1); gun = (K / K.shift(1) - 1).median(axis=1)
    sep: Dict[str, pd.Series] = {}; sek: Dict[str, str] = {}
    y = os.path.join(ay.kok, "sektor_BIST.csv" if pazar == "BIST" else "sektor_ABD.csv")
    if os.path.exists(y):
        sk = pd.read_csv(y); sk["sembol"] = sk.sembol.astype(str).str.upper().str.replace(".AM", "", regex=False)
        kol = "alt_bist" if "alt_bist" in sk.columns else ("sektor" if "sektor" in sk.columns else sk.columns[1])
        sek = dict(zip(sk.sembol, sk[kol].astype(str)))
        for grup, uy in pd.Series(sek).groupby(pd.Series(sek)):
            uy = [u for u in uy.index if u in g60.columns]
            if len(uy) >= 3:
                sep[grup] = g60[uy].median(axis=1)
    p = piy60.reindex(pd.to_datetime(T.alim)).to_numpy(float)
    gd = gun.reindex(pd.to_datetime(T.alim)).to_numpy(float)
    rz = np.full(len(T), np.nan)
    for i, (sem, t) in enumerate(zip(T.sembol, pd.to_datetime(T.alim))):
        sg = sek.get(sem)
        if sg in sep:
            sv = sep[sg].get(t, np.nan)
            if np.isfinite(sv) and np.isfinite(p[i]):
                rz[i] = 100 * (sv - p[i])
    T = T.copy()
    T["piyasa60"] = np.round(100 * p, 1); T["ruzgar60"] = np.round(rz, 1); T["piy_gun"] = np.round(100 * gd, 2)
    return T


# ------------------------------------------------------------------ K4 kova ozeti
def ck_kova(ay: CKAyar, T: pd.DataFrame, olcu: str, ref: pd.DataFrame) -> Tuple[pd.Series, List[str], str]:
    """Islemleri kovaya boler. ref: tercil sinirlari icin obek islemleri (pazar icinde). -> (kova etiketi serisi, sira, aciklama)."""
    if olcu in ay.kategorik:
        et = ["yok", "asagida", "yukarida"]
        return T[olcu].astype(str), et, "kategorik"
    k = ay.kovalar.get(olcu)
    x = T[olcu].astype(float)
    if k is None:
        q = ref[olcu].astype(float).quantile([1 / 3, 2 / 3]).to_numpy()
        sinir = [-np.inf, q[0], q[1], np.inf]; et = [f"T1 <{q[0]:.2f}", f"T2 {q[0]:.2f}-{q[1]:.2f}", f"T3 >={q[1]:.2f}"]
        acik = f"tercil ({q[0]:.2f} / {q[1]:.2f})"
    else:
        sinir, et = k; acik = "sabit esik"
    kova = pd.cut(x, bins=sinir, labels=et, right=False, include_lowest=True).astype(object)
    return kova, list(et), acik


def ck_k4_ozet(ay: CKAyar, CD, T: pd.DataFrame, donemler: Tuple, pazar: str) -> pd.DataFrame:
    """Her (olcu, kova, donem, kaynak) icin istatistik + o donemin tum islemlerine gore fark."""
    rows: List[Dict[str, Any]] = []
    ref = T[T.kaynak == "obek"]
    for olcu in ay.kovalar:
        if olcu not in T.columns:
            continue
        kova, et, acik = ck_kova(ay, T, olcu, ref)
        Tk = T.assign(_kova=kova)
        for ad, b, s_ in donemler:
            x0 = Tk[(Tk.sinyal >= b) & (Tk.sinyal <= s_)]
            for kaynak in ("obek", "taban"):
                xa = x0[x0.kaynak == kaynak]
                if xa.empty:
                    continue
                ga = xa.getiri.clip(upper=200)
                ort_all = float(ga.mean()); kaz_all = float(100 * (xa.getiri > 0).mean())
                slot_all = CD._cd_slot(xa.assign(getiri=ga), ay.slot)[0] if kaynak == "obek" else np.nan
                for e in et + ["(bos)"]:
                    x = xa[xa._kova.isna()] if e == "(bos)" else xa[xa._kova == e]
                    if len(x) == 0:
                        continue
                    g = x.getiri.clip(upper=200)
                    r = {"pazar": pazar, "olcu": olcu, "kova": e, "kova_tur": acik, "donem": ad, "kaynak": kaynak, "n": len(x),
                         "pay_%": round(100 * len(x) / len(xa), 1), "kazanan_%": round(100 * (x.getiri > 0).mean(), 1),
                         "ort_%": round(float(g.mean()), 2), "medyan_%": round(float(x.getiri.median()), 2),
                         "agir_%": round(100 * (x.getiri < ay.agir).mean(), 1), "stop_%": round(100 * (x.neden == "stop").mean(), 1),
                         "ort_all": round(ort_all, 2), "fark_ort": round(float(g.mean()) - ort_all, 2),
                         "fark_kazanan": round(100 * (x.getiri > 0).mean() - kaz_all, 1)}
                    if kaynak == "obek":
                        port, al, atla = CD._cd_slot(x.assign(getiri=g), ay.slot)
                        r.update({"slot_%": round(port, 1), "slot_all": round(slot_all, 1), "fark_slot": round(port - slot_all, 1), "slot_alinan": al})
                    rows.append(r)
    return pd.DataFrame(rows)


def ck_k4_tutarlilik(ay: CKAyar, OZ: pd.DataFrame) -> pd.DataFrame:
    """Kova basina: 6 donemde (obek) fark_ort > 0 sayisi (n >= min_n), ort fark, ort slot farki; taban ayni yon sayisi."""
    rows = []
    for (olcu, kova), g in OZ[OZ.kova != "(bos)"].groupby(["olcu", "kova"], sort=False):
        o = g[(g.kaynak == "obek") & (g.n >= ay.min_n)]
        t = g[(g.kaynak == "taban") & (g.n >= ay.min_n)]
        if o.empty:
            continue
        rows.append({"olcu": olcu, "kova": kova, "kova_tur": o.kova_tur.iloc[0], "donem_sayisi": len(o),
                     "arti_donem": int((o.fark_ort > 0).sum()), "eksi_donem": int((o.fark_ort < 0).sum()),
                     "fark_ort_ort": round(o.fark_ort.mean(), 2), "fark_ort_min": round(o.fark_ort.min(), 2),
                     "fark_slot_ort": round(o.fark_slot.mean(), 1), "slot_arti": int((o.fark_slot > 0).sum()),
                     "pay_ort_%": round(o["pay_%"].mean(), 1), "n_toplam": int(o.n.sum()),
                     "kazanan_fark_ort": round(o.fark_kazanan.mean(), 1), "agir_ort_%": round(o["agir_%"].mean(), 1),
                     "taban_arti": int((t.fark_ort > 0).sum()), "taban_donem": len(t),
                     "donemler": "; ".join(f"{r.donem} {r.fark_ort:+.1f}" for r in o.itertuples())})
    R = pd.DataFrame(rows)
    if R.empty:
        return R
    R["tutarli"] = (R.arti_donem >= ay.min_tutarli) & (R.eksi_donem == 0) & (R.donem_sayisi >= 5)
    return R.sort_values(["arti_donem", "fark_ort_ort"], ascending=[False, False]).reset_index(drop=True)


# ------------------------------------------------------------------ K5 bilesik sartlar
def ck_k5_bilesik(ay: CKAyar, CD, T: pd.DataFrame, R: pd.DataFrame, donemler_hepsi: List[Tuple[str, Tuple]]) -> pd.DataFrame:
    """En tutarli kovalar (farkli olculerden) VE ile birlestirilir; her donemde ort fark ve slot fark olculur."""
    aday = R[(R.arti_donem >= ay.min_tutarli) & (R.eksi_donem == 0)]
    aday = aday.drop_duplicates("olcu").head(ay.bilesik_en_cok)
    if len(aday) < 2:
        return pd.DataFrame()
    maskeler: Dict[str, pd.Series] = {}
    for a in aday.itertuples():
        kova, _, _ = ck_kova(ay, T, a.olcu, T[T.kaynak == "obek"])
        maskeler[f"{a.olcu}={a.kova}"] = (kova == a.kova)
    rows = []
    adlar = list(maskeler)
    for k in range(2, len(adlar) + 1):
        for comb in combinations(adlar, k):
            m = np.logical_and.reduce([maskeler[c].to_numpy() for c in comb])
            for pazar, donemler in donemler_hepsi:
                for ad, b, s_ in donemler:
                    xa = T[(T.kaynak == "obek") & (T.pazar == pazar) & (T.sinyal >= b) & (T.sinyal <= s_)]
                    x = xa[m[xa.index]]
                    if len(xa) == 0:
                        continue
                    ga = xa.getiri.clip(upper=200); g = x.getiri.clip(upper=200)
                    rows.append({"sart": " VE ".join(comb), "donem": ad, "n": len(x), "pay_%": round(100 * len(x) / len(xa), 1),
                                 "kazanan_%": round(100 * (x.getiri > 0).mean(), 1) if len(x) else np.nan,
                                 "ort_%": round(float(g.mean()), 2) if len(x) else np.nan, "ort_all": round(float(ga.mean()), 2),
                                 "fark_ort": round(float(g.mean()) - float(ga.mean()), 2) if len(x) else np.nan,
                                 "slot_%": round(CD._cd_slot(x.assign(getiri=g), ay.slot)[0], 1) if len(x) else np.nan,
                                 "slot_all": round(CD._cd_slot(xa.assign(getiri=ga), ay.slot)[0], 1)})
    B = pd.DataFrame(rows)
    if len(B):
        B["fark_slot"] = B["slot_%"] - B.slot_all
    return B


# ------------------------------------------------------------------ K6 rapor
def ck_k6_rapor(ay: CKAyar, T: pd.DataFrame, OZ: pd.DataFrame, R: pd.DataFrame, B: pd.DataFrame, cikti: str,
                donemler_hepsi: List[Tuple[str, Tuple]]) -> str:
    sat = [f"# COL KAZANC — uretim yoluna hangi sart eklenirse kazanc artar?   ({CK_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Yol (uretim): obek -> yesil kapanis > tavan -> ertesi acilis -> stop dip -%2 (T6) -> +%8'de stop maliyete (T10) -> +%20 sonra SMA20 trail -> 120 bar. Maliyet %0,4.",
           "Fark = kovanin ort getirisi - o donemdeki TUM obek islemlerinin ort getirisi (puan, %200 kirpili). Slot = 30 slot portfoy. TUTARLI = 6 donemin >= 5'inde fark > 0 ve hicbirinde < 0 (n >= 60).",
           "Taban = obek sarti aranmadan her 5. gunun 15 mumluk kutusu; 'taban arti' = ayni sartin taban islemlerinde kac donem arti verdigi (obekten bagimsiz mi?).", ""]
    # donem tabani
    sat += ["## Donem tabani (tum obek islemleri, uretim cikisi)", "", "| donem | n | kazanan | ort | medyan | agir | slot |", "|---|---|---|---|---|---|---|"]
    for pazar, donemler in donemler_hepsi:
        for ad, b, s_ in donemler:
            x = T[(T.kaynak == "obek") & (T.pazar == pazar) & (T.sinyal >= b) & (T.sinyal <= s_)]
            if x.empty:
                continue
            g = x.getiri.clip(upper=200)
            from_oz = OZ[(OZ.donem == ad) & (OZ.kaynak == "obek")]
            slot = from_oz.slot_all.iloc[0] if len(from_oz) else np.nan
            sat.append(f"| {ad} | {len(x)} | %{100 * (x.getiri > 0).mean():.0f} | {g.mean():+.1f} | {x.getiri.median():+.1f} | %{100 * (x.getiri < ay.agir).mean():.0f} | {slot:+.0f}% |")
    sat.append("")
    # tutarlilik sirasi
    sat += ["## Sartlar tutarlilik sirasina gore (obek islemleri; arti donem = 6 donemin kacinda fark > 0)", "",
            "| olcu | kova | arti/eksi donem | fark ort (min) | slot fark ort | pay % | kazanan fark | agir % | taban arti | donemler |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in R.iterrows():
        isaret = "**TUTARLI** " if r.tutarli else ""
        sat.append(f"| {isaret}{r.olcu} | {r.kova} | {r.arti_donem}/{r.eksi_donem} ({r.donem_sayisi}) | {r.fark_ort_ort:+.1f} ({r.fark_ort_min:+.1f}) | {r.fark_slot_ort:+.0f} | {r['pay_ort_%']:.0f} | {r.kazanan_fark_ort:+.1f} | {r['agir_ort_%']:.0f} | {r.taban_arti}/{r.taban_donem} | {r.donemler} |")
    sat.append("")
    # Cemal'in sorusu: hacim
    sat += ["## Cemal'in sorusu: hacim (obek kurusun, alim mumu 2-3-4 kat)", ""]
    for olcu in ("hacim_alim_kat", "hacim_obek_kat", "hacim_alim_kat60", "hacim_son_kat"):
        o = OZ[(OZ.olcu == olcu) & (OZ.kaynak == "obek") & (OZ.kova != "(bos)")]
        if o.empty:
            continue
        don = [ad for _, dl in donemler_hepsi for ad, _, _ in dl]
        sat += [f"### {olcu}", "", "| kova | " + " | ".join(don) + " |", "|---|" + "---|" * len(don)]
        for kova in ay.kovalar[olcu][1]:
            h = []
            for ad in don:
                z = o[(o.kova == kova) & (o.donem == ad)]
                h.append(f"n{int(z.n.iloc[0])} {z['ort_%'].iloc[0]:+.1f} ({z.fark_ort.iloc[0]:+.1f}) %{z['kazanan_%'].iloc[0]:.0f}" if len(z) else "-")
            sat.append(f"| {kova} | " + " | ".join(h) + " |")
        sat.append("")
        sat.append("(hucre: n, ort getiri (tum islemlere gore fark), kazanan %)")
        sat.append("")
    # bilesik
    if len(B):
        sat += ["## Bilesik sartlar (en tutarli olculer VE ile)", "", "| sart | donem | n | pay % | kazanan | ort (fark) | slot (fark) |", "|---|---|---|---|---|---|---|"]
        for _, r in B.iterrows():
            sat.append(f"| {r.sart} | {r.donem} | {r.n} | {r['pay_%']:.0f} | %{r['kazanan_%']:.0f} | {r['ort_%']:+.1f} ({r.fark_ort:+.1f}) | {r['slot_%']:+.0f}% ({r.fark_slot:+.0f}) |")
        sat.append("")
    # sonuc
    tut = R[R.tutarli]
    sat += ["## SONUC", ""]
    if tut.empty:
        sat.append("Hicbir sart 6 donemin 5'inde tutarli artı vermedi -> uretim koduna eklenecek bir sart BULUNAMADI (iz yok). Tek dönemde iyi görünenler ölçüm, bulgu değil.")
    else:
        sat.append(f"{len(tut)} sart tutarli (>= {ay.min_tutarli}/6 donem arti, hicbirinde eksi):")
        for _, r in tut.iterrows():
            sat.append(f"- {r.olcu} = {r.kova}: ort fark {r.fark_ort_ort:+.1f} puan (en kotu donem {r.fark_ort_min:+.1f}), slot fark {r.fark_slot_ort:+.0f}, islemlerin %{r['pay_ort_%']:.0f}'i, taban {r.taban_arti}/{r.taban_donem}.")
        sat.append("")
        sat.append("Uyari: slot farki eksiyse sart islem sayisini azaltip portfoyu kucultuyor demektir (islem basi iyi, toplam kotu). 1,3x kurali icin slot ve kazanan birlikte okunur.")
    sat.append("")
    sat.append("Not: 'kirilim hacmi' COL_OZET bolum 3'te segment cercevesinde kapanmisti; burada obek cercevesinde Cemal'in istegiyle yeniden olculdu. OLCUM; kural sonucla.")
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_KAZANC_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


# ------------------------------------------------------------------ calistirici
def _kazanc_pazar(ay: CKAyar, CD, CO, CY, veri: Dict[str, pd.DataFrame], pazar: str) -> pd.DataFrame:
    isl, D = ck_k2_islemler(ay, CO, CY, veri)
    T = ck_k3_cikis(ay, CY, isl, D)
    T = ck_k3_piyasa(ay, veri, T, pazar)
    T["pazar"] = pazar
    return T


def col_kazanc(ay: Optional[CKAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None,
               veri_abd: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or CKAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_kazanc")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD, CO, CY = _ck_mod()
    cay = CD.CDAyar(kok=ay.kok)
    if veri is None:
        veri = CD.cd_k1_bist(cay); CD.cd_k2_onarim(cay, veri)
    T = _kazanc_pazar(ay, CD, CO, CY, veri, "BIST")
    donemler_hepsi: List[Tuple[str, Tuple]] = [("BIST", ay.donemler)]
    OZ = ck_k4_ozet(ay, CD, T, ay.donemler, "BIST")
    if ay.abd:
        try:
            if veri_abd is None:
                veri_abd = CD.cd_k1_abd(cay)
            Ta = _kazanc_pazar(ay, CD, CO, CY, veri_abd, "ABD")
            OZa = ck_k4_ozet(ay, CD, Ta, ay.donemler_abd, "ABD")
            T = pd.concat([T, Ta], ignore_index=True); OZ = pd.concat([OZ, OZa], ignore_index=True)
            donemler_hepsi.append(("ABD", ay.donemler_abd))
        except Exception as ex:
            cklog.error("ABD: %s", ex)
    T.to_csv(os.path.join(cikti, "col_kazanc_islemler.csv.gz"), index=False)
    OZ.to_csv(os.path.join(cikti, "col_kazanc_kova.csv"), index=False)
    R = ck_k4_tutarlilik(ay, OZ)
    R.to_csv(os.path.join(cikti, "col_kazanc_tutarlilik.csv"), index=False)
    B = ck_k5_bilesik(ay, CD, T, R, donemler_hepsi)
    if len(B):
        B.to_csv(os.path.join(cikti, "col_kazanc_bilesik.csv"), index=False)
    metin = ck_k6_rapor(ay, T, OZ, R, B, cikti, donemler_hepsi)
    cklog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"islemler": T, "kova": OZ, "tutarlilik": R, "bilesik": B, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_ck(_once=_CK_ONCE_CK, _dosya='COL_KAZANC.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CK', '_CK_KAYIT', '_cakisma_kontrol_ck', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field', 'combinations')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ck()

if __name__ == "__main__":
    R = col_kazanc()
    print(R["rapor"])
