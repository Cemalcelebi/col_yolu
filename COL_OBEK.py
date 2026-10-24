# =====================================================================
#  COL_OBEK — Yuvarlanma obegi: bul, sonucunu kaydet, ayirani ogren   (2026-10-21, v1.0)
#
#  CEMAL (21 Eki): aranan desen kucuk olcekte de var — dip -> savunma -> yukari yuvarlanan kucuk mum obegi, bir hissede
#    arka arkaya. "Iyi/kotu sinyal alimla aciklanir: alim mumlari gelmeden asagi dusen de col sayilsin ki makine kendini
#    gelistirsin." Yani: obek tespitine yon sarti yok; her obek bulunur, sonucu (alim geldi / gelmeden dustu) kaydedilir,
#    ayiran olcu sonradan ogrenilir.
#
#  YONTEM (ileriye bakis yok; her gun yalniz o gune kadarki veri)
#    OBEK (goz_esle/arastirma/obek_tani.py ile ayni tanim): pencere w in OBEK_W bar; dip pencerenin ilk %40'inda; dipten sonra
#      en az 5 bar; mumlar kucuk (pencere aralik medyani <= KUCUK_KAT x onceki 60 gun medyani); pencere dar (yukseklik <= DAR_KAT x
#      pencere aralik medyani); dipten sonra yeni dip yok; yuvarlanma: son ucte bir dip medyani > orta ucte bir dip medyani > dip.
#      Sinyal gunu = obegin ilk gorulup sartlari sagladigi gun (gercek zamanli tarayicinin gorecegi gun). Ayni dip = ayni obek.
#    SONUC (sonradan): sinyalden sonra ILERI bar icinde ilk olay — ALIM: kapanis > obek tavani x AL_PAY (Cemal: 'alim mumlari');
#      DUSUS: kapanis < dip x (1 - BOZ_TOL); yoksa 'yok'. Alimda COL_DIP_TEST._cd_islem (ertesi acilis, %20 sonra SMA20 trail / 120 bar).
#      Ayrica 60 ve 120 bar sonraki kapanis getirisi (piyasa medyanina gore fark).
#    OLCULER (sinyal gununde bilinen): w, med/ref60, konum250, dip_oncesi_dusus60, sma50_egim, sma200_uzaklik, bb_son, hacim_kat,
#      onceki_obek (60 bar icinde onceki obek var mi, seviyesi dusuk mu yuksek mi), sektor ruzgari (sepet 60g - piyasa 60g),
#      piyasa 60g, obek_sira (ust uste kacinci obek).
#    KIYAS: donem basina (2016-19, 2020-22, 2023, 2024-26) alim orani, dusus orani, trail beklenti; olcu tercilleri; taban =
#      ayni gunlerde rastgele hisse (ayni donem) 60/120 bar getirisi.
#  KURAL_MOTORU: K1 veri (COL_DIP_TEST.cd_k1_bist + onarim)  K2 tespit  K3 sonuc + olcu  K4 kiyas  K5 rapor
#  Calistirma: GitHub Actions 'Arastirma' (betik: COL_OBEK.py). Cikti: arastirma_cikti/col_obek/
#  Sinyal sayisi buyuk olsa da bu bir OLCUM; kural degil. ABD henuz yok (sonraki adim).
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

_CK_ONCE_CO = {k: id(v) for k, v in globals().items()}

CO_SURUM = "COL_OBEK v1.4 (2026-10-24, denetim: esli taban ALIM, ayni alim tek islem, islem yesil alim barindan, trail ufuksuz)"
colog = logging.getLogger("col.obek")
if not colog.handlers:
    _co_h = logging.StreamHandler(sys.stderr)
    _co_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s obek: %(message)s", "%H:%M:%S"))
    colog.addHandler(_co_h)
    colog.setLevel(logging.INFO)
    colog.propagate = False


@dataclass
class COAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    obek_w: Tuple[int, ...] = (10, 15, 20, 25)
    dip_pay: float = 0.40          # dip pencerenin ilk bu kadarinda
    kucuk_kat: float = 0.90        # pencere aralik medyani <= kat x onceki 60 gun medyani
    dar_kat: float = 5.0           # pencere yuksekligi (% fiyat) <= kat x pencere aralik medyani
    al_pay: float = 1.002
    boz_tol: float = 0.02
    ileri: int = 60                # ilk olay icin bakilan bar
    yuk_esik: Tuple[float, ...] = (8.0, 10.0)   # Cemal: alimdan sonra en az %8-10 yukselis gorulduyse stop maliyete cekilir
    yuk_bar: int = 60              # yukselis / stop icin bakilan bar (alim barindan sonra)
    min_gecmis: int = 260
    donemler: Tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                       ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))
    tohum: int = 42


def _co_cd():
    import importlib
    kok = COAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST")


# ------------------------------------------------------------------ K2 tespit
def co_obek(ay: COAyar, L: np.ndarray, H: np.ndarray, C: np.ndarray, ar: np.ndarray, ref60: np.ndarray, s: int, e: int) -> Optional[Dict[str, Any]]:
    """(s, e) penceresi yuvarlanma obegi mi? Yalniz s..e ve oncesi kullanilir."""
    w = e - s + 1
    d = s + int(np.argmin(L[s:e + 1]))
    if (d - s) / w > ay.dip_pay or e - d < 5:
        return None
    r60 = ref60[s]
    if not (np.isfinite(r60) and r60 > 0):
        return None
    med = float(np.nanmedian(ar[s:e + 1]))
    if med > ay.kucuk_kat * r60:
        return None
    hi, lo = float(H[s:e + 1].max()), float(L[s:e + 1].min())
    if (hi - lo) / C[e] * 100 > ay.dar_kat * med:
        return None
    dip = L[d]
    if L[d + 1:e + 1].min() < dip * (1 - 0.5 * r60 / 100):
        return None
    y = L[d:e + 1] / dip - 1
    k = max(2, len(y) // 3)
    if not (np.median(y[-k:]) > np.median(y[k:2 * k]) > 0):
        return None
    return {"s": s, "e": e, "d": d, "w": w, "med": med, "ref60": r60, "tavan": hi, "dip": float(dip),
            "yuv": float(np.median(y[-k:]) * 100)}


def co_k2_tespit(ay: COAyar, df: pd.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, np.ndarray]]:
    """Hissede gercek zamanli obek sinyalleri: her gun e icin w'lerden biri saglarsa sinyal; ayni dip tekrar sinyal vermez."""
    O, H, L, C, V = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    pc = np.r_[O[0], C[:-1]]
    with np.errstate(divide="ignore", invalid="ignore"):
        ar = 100 * (H - L) / pc
    ref60 = pd.Series(ar).rolling(60, min_periods=40).median().shift(1).to_numpy()   # s gununden ONCEKI 60 gun
    n = len(C)
    out: List[Dict[str, Any]] = []
    son_dip = -1
    for e in range(ay.min_gecmis, n):
        # ucuz on eleme: en kucuk pencere bile kucuk mum sartini saglamiyorsa gec
        best = None
        for w in ay.obek_w:
            s = e - w + 1
            if s < 60:
                continue
            r = co_obek(ay, L, H, C, ar, ref60, s, e)
            if r and (best is None or r["w"] > best["w"]):
                best = r
        if not best:
            continue
        if best["d"] == son_dip:
            continue
        son_dip = best["d"]
        out.append(best)
    return out, {"O": O, "H": H, "L": L, "C": C, "V": V, "ar": ar}


# ------------------------------------------------------------------ K3 sonuc + olcu
def co_yol(ay: COAyar, O: np.ndarray, H: np.ndarray, L: np.ndarray, b: int, stop: float) -> Dict[str, Any]:
    """Cemal'in yolu: alim barindan sonraki acilista gir, stop = obek dibi - tol. yuk_bar icinde once +%8/+%10 mu geldi, once stop mu?
    Ayni barda ikisi birden olursa stop sayilir (temkinli). mfe = en yuksek goruldugu %, stop_bar = stop'a kadar bar."""
    n = len(O)
    if b + 1 >= n:
        return {}
    giris = O[b + 1]
    out: Dict[str, Any] = {"giris": round(float(giris), 2), "mfe": np.nan, "stop_bar": np.nan}
    hedefler = {h: f"yuk{int(h)}" for h in ay.yuk_esik}
    durum = {k: "yok" for k in hedefler.values()}
    mfe, stop_i = -np.inf, None
    for i in range(b + 1, min(n, b + 1 + ay.yuk_bar)):
        mfe = max(mfe, H[i] / giris - 1)
        if L[i] <= stop:
            stop_i = i
            for h, k in hedefler.items():
                if durum[k] == "yok":
                    durum[k] = "stop"
            break
        for h, k in hedefler.items():
            if durum[k] == "yok" and H[i] >= giris * (1 + h / 100):
                durum[k] = "gordu"
    out.update(durum)
    out["mfe"] = round(float(mfe) * 100, 1) if np.isfinite(mfe) else np.nan
    out["stop_bar"] = (stop_i - b) if stop_i else np.nan
    return out


def co_k3_sonuc(ay: COAyar, CD, cay, A: Dict[str, np.ndarray], S20: np.ndarray, r: Dict[str, Any]) -> Dict[str, Any]:
    O, H, L, C = A["O"], A["H"], A["L"], A["C"]
    n = len(C)
    e, tavan, dip = r["e"], r["tavan"] * ay.al_pay, r["dip"] * (1 - ay.boz_tol)
    olay, olay_i = "yok", None
    for i in range(e + 1, min(n, e + 1 + ay.ileri)):
        if C[i] > tavan and C[i] > O[i]:                       # Cemal 21 Eki: alim = YESIL mumun kapanisi kutunun ustunde
            olay, olay_i = "alim", i; break
        if C[i] < dip:
            olay, olay_i = "dusus", i; break
    if e + 1 >= n:
        olay = "veri sonu"
    s: Dict[str, Any] = {"olay": olay, "olay_bar": (olay_i - e) if olay_i else np.nan,
                         # denetim 24 Eki: alim barinin tarihi (ayni alim tek islem sayilsin) ve sinyal gunu tavan/dip uzakligi (esli taban)
                         "alim_tarih": A["ix"][olay_i].date() if (olay == "alim" and "ix" in A) else None,
                         "tavan_uz": round((tavan / C[e] - 1) * 100, 2), "dip_uz": round((C[e] / dip - 1) * 100, 2)}
    for uf in (60, 120):
        s[f"get_{uf}"] = round(float(C[min(n - 1, e + uf)] / C[e] - 1) * 100, 1) if e + uf < n else np.nan
    if olay == "alim":
        # denetim 24 Eki: islem yesil alim barindan (eskiden _cd_islem renksiz ilk kirilimi aliyordu, %8,5'inde farkli bar);
        # veri sonunda acik islem getiriye girmez
        isl = CD._cd_cikis(cay, O, H, C, S20, olay_i)
        if isl and "getiri" in isl and not isl.get("acik"):
            s.update(islem_getiri=round(isl["getiri"], 1), hedef=isl["hedef"])
        s.update(co_yol(ay, O, H, L, olay_i, dip))
    return s


def co_olcu(A: Dict[str, np.ndarray], r: Dict[str, Any], onceki: Optional[Dict[str, Any]], sira: int) -> Dict[str, Any]:
    C, L, H, V = A["C"], A["L"], A["H"], A["V"]
    s, e, d = r["s"], r["e"], r["d"]
    o250 = max(0, e - 249)
    lo, hi = float(L[o250:e + 1].min()), float(H[o250:e + 1].max())
    sma50 = float(np.mean(C[e - 49:e + 1])); sma50o = float(np.mean(C[e - 59:e - 9]))
    sma200 = float(np.mean(C[max(0, e - 199):e + 1]))
    cs = pd.Series(C[max(0, e - 300):e + 1]); m = cs.rolling(20).mean(); sd = cs.rolling(20).std(ddof=0)
    bbw = (4 * sd / m).to_numpy(float); pen = bbw[np.isfinite(bbw)]
    return {"w": r["w"], "yuv_%": round(r["yuv"], 2), "mum_kat": round(r["med"] / r["ref60"], 2),
            "konum250": round((C[e] - lo) / (hi - lo), 2) if hi > lo else np.nan,
            "dusus60": round(float(C[e] / C[max(0, s - 60)] - 1) * 100, 1),
            # Cemal 21 Eki: "dusen bicak" — obek oncesi 20 barda dik dusus ve iri mumlar; esik veriden ogrenilecek
            "bicak_dusus20": round(float(C[max(0, s - 1)] / C[max(0, s - 21)] - 1) * 100, 1),
            "bicak_mum20": round(float(np.nanmedian(A["ar"][max(0, s - 20):s]) / r["ref60"]), 2) if r["ref60"] > 0 else np.nan,
            "sma50_egim": round((sma50 / sma50o - 1) * 100, 1), "sma200_uzak": round((C[e] / sma200 - 1) * 100, 1),
            "bb_son": round(float((pen <= bbw[-1]).mean()), 2) if len(pen) > 60 else np.nan,
            "hacim_kat": round(float(np.nanmedian(V[s:e + 1]) / np.nanmedian(V[max(0, s - 60):s])), 2) if np.nanmedian(V[max(0, s - 60):s]) > 0 else np.nan,
            "onceki_obek": ("yok" if onceki is None or s - onceki["e"] > 60 else ("asagida" if r["dip"] < onceki["dip"] else "yukarida")),
            "obek_sira": sira}


def co_k3_tara(ay: COAyar, CD, cay, veri: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    t0 = time.monotonic()
    rows: List[Dict[str, Any]] = []
    for k, (sem, df) in enumerate(veri.items()):
        df = df[np.isfinite(df.Close)]
        if len(df) < ay.min_gecmis + 20:
            continue
        try:
            sig, A = co_k2_tespit(ay, df)
        except Exception as ex:
            colog.debug("%s: %s", sem, ex); continue
        if not sig:
            continue
        S20 = df.Close.rolling(cay.ma, min_periods=cay.ma).mean().to_numpy(float)
        ix = df.index
        A["ix"] = ix
        onceki, sira = None, 0
        for r in sig:
            sira = sira + 1 if (onceki is not None and r["s"] - onceki["e"] <= 60) else 1
            rows.append({"sembol": sem, "sinyal": ix[r["e"]].date(), "obek_bas": ix[r["s"]].date(), "dip": ix[r["d"]].date(),
                         "tavan": round(r["tavan"], 2), "taban": round(r["dip"], 2), "kapanis": round(float(A["C"][r["e"]]), 2),
                         **co_olcu(A, r, onceki, sira), **co_k3_sonuc(ay, CD, cay, A, S20, r)})
            onceki = r
        if (k + 1) % 50 == 0:
            colog.info("K3: %d/%d hisse | %d sinyal (%.0f sn)", k + 1, len(veri), len(rows), time.monotonic() - t0)
    T = pd.DataFrame(rows)
    colog.info("K3 bitti: %d sinyal, %d hisse (%.0f sn)", len(T), T.sembol.nunique() if len(T) else 0, time.monotonic() - t0)
    return T


# ------------------------------------------------------------------ K4 piyasa / sektor / taban
def co_k4_piyasa(ay: COAyar, veri: Dict[str, pd.DataFrame], T: pd.DataFrame) -> pd.DataFrame:
    """Sinyal gunune piyasa 60g medyan getirisi, sektor sepeti 60g (sektor_BIST.csv), ileri 60/120 piyasa medyani (fark icin)."""
    if T.empty:
        return T
    K = pd.DataFrame({s: df.Close for s, df in veri.items()}).sort_index().ffill()
    g60 = K / K.shift(60) - 1
    piy60 = g60.median(axis=1)
    f60 = (K.shift(-60) / K - 1).median(axis=1); f120 = (K.shift(-120) / K - 1).median(axis=1)
    sek = None
    y = os.path.join(ay.kok, "sektor_BIST.csv")
    if os.path.exists(y):
        sk = pd.read_csv(y); sk["sembol"] = sk.sembol.astype(str).str.upper()
        kol = [c for c in sk.columns if c != "sembol"][0]
        sek = dict(zip(sk.sembol, sk[kol].astype(str)))
        sep: Dict[str, pd.Series] = {}
        for grup, uy in pd.Series(sek).groupby(pd.Series(sek)):
            uy = [u for u in uy.index if u in g60.columns]
            if len(uy) >= 3:
                sep[grup] = g60[uy].median(axis=1)
    rows = []
    for r in T.itertuples():
        t = pd.Timestamp(r.sinyal)
        p = float(piy60.get(t, np.nan))
        sg = sek.get(r.sembol) if sek else None
        sv = float(sep[sg].get(t, np.nan)) if (sek and sg in sep) else np.nan
        rows.append({"piyasa60": round(100 * p, 1) if np.isfinite(p) else np.nan,
                     "ruzgar60": round(100 * (sv - p), 1) if (np.isfinite(sv) and np.isfinite(p)) else np.nan,
                     "piy_ileri60": round(100 * float(f60.get(t, np.nan)), 1), "piy_ileri120": round(100 * float(f120.get(t, np.nan)), 1)})
    P = pd.DataFrame(rows, index=T.index)
    T = pd.concat([T, P], axis=1)
    T["fark60"] = T.get_60 - T.piy_ileri60
    T["fark120"] = T.get_120 - T.piy_ileri120
    return T


def co_k4_taban(ay: COAyar, veri: Dict[str, pd.DataFrame], adim: int = 5, w: int = 15) -> pd.DataFrame:
    """Taban: obek sarti aranmadan her adim. gunde ayni olay kurali (tavan = son w bar en yuksek, dip = son w bar en dusuk) + ileri 60/120 getiri."""
    rows = []
    for sem, df in veri.items():
        df = df[np.isfinite(df.Close)]
        O, H, L, C = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        n = len(C); ix = df.index
        for e in range(ay.min_gecmis, n - 1, adim):
            tavan = H[e - w + 1:e + 1].max() * ay.al_pay; dip = L[e - w + 1:e + 1].min() * (1 - ay.boz_tol)
            olay, oi = "yok", None
            for i in range(e + 1, min(n, e + 1 + ay.ileri)):
                if C[i] > tavan and C[i] > O[i]: olay, oi = "alim", i; break   # yesil mum
                if C[i] < dip: olay, oi = "dusus", i; break
            yol = co_yol(ay, O, H, L, oi, dip) if olay == "alim" else {}
            rows.append({"sembol": sem, "sinyal": ix[e].date(), "olay": olay, **yol,
                         "tavan_uz": round((tavan / C[e] - 1) * 100, 2), "dip_uz": round((C[e] / dip - 1) * 100, 2),
                         "get_60": round(float(C[min(n - 1, e + 60)] / C[e] - 1) * 100, 1) if e + 60 < n else np.nan,
                         "get_120": round(float(C[min(n - 1, e + 120)] / C[e] - 1) * 100, 1) if e + 120 < n else np.nan})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ K5 rapor
def _oran(x: pd.Series) -> str:
    return f"%{100 * x.mean():.0f}" if len(x) else "-"


CO_UZ_KOVA = [-1, 1, 2, 3, 4, 5, 6, 8, 10, 15, 1e9]


def co_esli_alim(x: pd.DataFrame, tb: pd.DataFrame) -> float:
    """Denetim 24 Eki: taban kutusu (son 15 bar) obekten genis; tavan kapanisa ~2 kat uzak oldugundan 'ALIM orani tabandan +15-20p'
    mekanikti. Esli taban ALIM orani: taban satirlari sinyal gunu tavan ve dip uzakligi (%) kovalarina gore gruplanir, her obek
    kendi kovasinin taban oranini alir, ortalama. Kovasi tabanda bos olan obek disarida."""
    if not len(x) or not len(tb) or "tavan_uz" not in tb or "tavan_uz" not in x:
        return np.nan
    k = lambda Z: (pd.cut(Z.tavan_uz, CO_UZ_KOVA), pd.cut(Z.dip_uz, CO_UZ_KOVA))
    h = tb.assign(_a=(tb.olay == "alim").astype(float)).groupby(list(k(tb)), observed=True)._a.mean()
    return float(h.reindex(pd.MultiIndex.from_arrays(list(k(x)))).mean())


def co_k5_rapor(ay: COAyar, T: pd.DataFrame, cikti: str, TB: Optional[pd.DataFrame] = None) -> str:
    sat = [f"# COL OBEK — yuvarlanma obegi: bul, sonucu kaydet   ({CO_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Obek: 10-25 bar, dip ilk %40'ta, dipten sonra yeni dip yok, dipler yukari yuvarlaniyor, mumlar onceki 60 gune gore kucuk, pencere dar.",
           "Sinyal = obegin ilk saglandigi gun. Olay (60 bar): ALIM = YESIL mumun kapanisi > obek tavani (Cemal: alim mumu) | DUSUS = kapanis < dip -%2 | yok.",
           "Alimda islem: ertesi acilis, %20 sonra SMA20 trail / 120 bar. fark60/120 = 60/120 bar getirisi - ayni gun piyasa medyani. Ortalamalar %200'de kirpilir (eski kurus hisse veri sicramasi). OLCUM, kural degil.", ""]
    if T.empty:
        sat.append("sinyal yok"); return "\n".join(sat)
    T = T.copy(); T["sinyal"] = pd.to_datetime(T.sinyal)
    sat += ["## Donem basina", "", "| donem | sinyal | hisse | ALIM | DUSUS | yok | alimda trail ort / medyan / kazanan | fark60 ort / medyan | fark120 ort / medyan |", "|---|---|---|---|---|---|---|---|---|"]
    for ad, b, s_ in ay.donemler:
        x = T[(T.sinyal >= b) & (T.sinyal <= s_)]
        if x.empty: continue
        a = x[x.olay == "alim"]
        if "alim_tarih" in a:      # denetim 24 Eki: ayni alim barina dusen obek sinyalleri tek islem (eskiden ~yarisi kopyaydi)
            a = a.drop_duplicates(["sembol", "alim_tarih"])
        g = a.islem_getiri.dropna()
        gk = g.clip(upper=200)        # eski kurus hisselerde veri sicramasi (TRHOL 2019 +69752%): ortalama %200'de kirpilir, medyan degismez
        sat.append(f"| {ad} | {len(x)} | {x.sembol.nunique()} | {_oran(x.olay=='alim')} | {_oran(x.olay=='dusus')} | {_oran(x.olay=='yok')} | "
                   f"{gk.mean():+.1f} / {g.median():+.1f} / %{100*(g>0).mean():.0f} (n={len(g)}, >%200 olan {int((g>200).sum())}) | "
                   f"{x.fark60.clip(-100, 200).mean():+.1f} / {x.fark60.median():+.1f} | {x.fark120.clip(-100, 200).mean():+.1f} / {x.fark120.median():+.1f} |")
        if TB is not None and len(TB):
            tb = TB[(TB.sinyal >= b) & (TB.sinyal <= s_)]
            if len(tb):
                sat.append(f"| {ad} TABAN (her 5. gun, w=15) | {len(tb)} | {tb.sembol.nunique()} | {_oran(tb.olay=='alim')} | {_oran(tb.olay=='dusus')} | {_oran(tb.olay=='yok')} | - | "
                           f"{tb.fark60.mean():+.1f} / {tb.fark60.median():+.1f} | {tb.fark120.mean():+.1f} / {tb.fark120.median():+.1f} |")
                ea = co_esli_alim(x, tb)
                sat.append(f"| {ad} ESLI TABAN (tavan/dip uzakligi ayni kova) | - | - | %{100 * ea:.0f} | - | - | - | - | - |")
    sat += ["", f"## Cemal'in yolu: alim geldikten sonra (ertesi acilis giris, stop = obek dibi -%{100*ay.boz_tol:.0f}, {ay.yuk_bar} bar)", "",
            "| donem | alim n | +%8 GORDU | +%8 gormeden STOP | ikisi de yok | +%10 GORDU | +%10 gormeden STOP | mfe medyan | stop'a kadar bar medyan |", "|---|---|---|---|---|---|---|---|---|"]
    for ad, b, s_ in ay.donemler:
        for etiket, Z in (("", T), ("TABAN", TB if TB is not None else pd.DataFrame())):
            if Z is None or not len(Z) or "yuk8" not in Z.columns: continue
            x = Z[(Z.sinyal >= b) & (Z.sinyal <= s_) & (Z.olay == "alim") & Z.yuk8.notna()]
            if "alim_tarih" in x and x.alim_tarih.notna().any():
                x = x.drop_duplicates(["sembol", "alim_tarih"])          # denetim: ayni alim tek islem
            if x.empty: continue
            sat.append(f"| {ad} {etiket} | {len(x)} | {_oran(x.yuk8=='gordu')} | {_oran(x.yuk8=='stop')} | {_oran(x.yuk8=='yok')} | {_oran(x.yuk10=='gordu')} | {_oran(x.yuk10=='stop')} | "
                       f"{x.mfe.median():+.1f} | {x.stop_bar.median():.0f} |")
    sat += ["", "## Hangi olcu ALIM'i DUSUS'ten ayiriyor? (olcu tercilleri; donem 2017-21 ve 2022-26 ayri; ALIM orani ve fark120 medyani)", ""]
    olculer = ["yuv_%", "mum_kat", "konum250", "dusus60", "bicak_dusus20", "bicak_mum20", "sma50_egim", "sma200_uzak", "bb_son", "hacim_kat", "obek_sira", "piyasa60", "ruzgar60", "w"]
    for ad, b, s_ in (("2017-21", "2017-01-01", "2021-12-31"), ("2022-26", "2022-01-01", "2026-12-31")):
        x = T[(T.sinyal >= b) & (T.sinyal <= s_) & T.olay.isin(["alim", "dusus"])]
        if len(x) < 30: continue
        sat.append(f"### {ad}  (n={len(x)}, ALIM %{100*(x.olay=='alim').mean():.0f})"); sat.append("")
        sat.append("| olcu | dusuk tercil: ALIM / +8 gordu / fark120 | orta | yuksek |"); sat.append("|---|---|---|---|")
        for m in olculer:
            if m not in x.columns or x[m].nunique() < 3: continue
            try:
                q = pd.qcut(x[m].rank(method="first"), 3, labels=["dusuk", "orta", "yuksek"])
            except Exception:
                continue
            h = []
            for lab in ("dusuk", "orta", "yuksek"):
                z = x[q == lab]
                za = z[z.olay == "alim"]
                h.append(f"%{100*(z.olay=='alim').mean():.0f} / %{100*(za.yuk8=='gordu').mean():.0f} / {z.fark120.median():+.1f}")
            sat.append(f"| {m} | {h[0]} | {h[1]} | {h[2]} |")
        for m in ("onceki_obek",):
            sat.append(""); sat.append(f"{m}: " + " | ".join(f"{k}: n={len(z)} ALIM %{100*(z.olay=='alim').mean():.0f} fark120 {z.fark120.median():+.1f}" for k, z in x.groupby(m)))
        sat.append("")
    sat += ["Dosyalar: col_obek_sinyaller.csv.gz (butun sinyaller + olculer + sonuc)", ""]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_OBEK_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


def col_obek(ay: Optional[COAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or COAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_obek")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD = _co_cd(); cay = CD.CDAyar(kok=ay.kok)
    if veri is None:
        veri = CD.cd_k1_bist(cay); CD.cd_k2_onarim(cay, veri)
    T = co_k3_tara(ay, CD, cay, veri)
    T = co_k4_piyasa(ay, veri, T)
    T.to_csv(os.path.join(cikti, "col_obek_sinyaller.csv.gz"), index=False)
    TB = co_k4_piyasa(ay, veri, co_k4_taban(ay, veri)) if len(T) else pd.DataFrame()
    if len(TB): TB["sinyal"] = pd.to_datetime(TB.sinyal)
    metin = co_k5_rapor(ay, T, cikti, TB)
    colog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"sinyal": T, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_co(_once=_CK_ONCE_CO, _dosya='COL_OBEK.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CO', '_CK_KAYIT', '_cakisma_kontrol_co', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_co()

if __name__ == "__main__":
    R = col_obek()
    print(R["rapor"])
