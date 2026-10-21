# =====================================================================
#  COL_TESPIT — Cemal'in uc kurali ile col tespit motoru adaylari (D13 adayi)   (2026-10-21, v1.0)
#
#  CEMAL (21 Eki): (1) Formasyonun sirasi: onceki kucuk mumlu bolge + dusus + yeni dip TEK KUTU sayilmaz. Onceki bolge dip
#    kirilimiyla biter; yeni col bolgesi dipten SONRA baslar. (2) Dip savunmasi: kucuk mum tek basina yetmez; dip olusumu, dipte
#    tutunma, parabolik yukari yuvarlanma ve kucuk mum obeklerinin dogru sirayla olusmasi BIRLIKTE olculur. (3) Tespit ile islem
#    karari ayrilir: asagi kirilip sonra toparlanan coller de tespit edilir; tespit motoru formasyonu bulur, giris ayri karar.
#    "Butun olasiliklari tek tek deneyerek kodu bul ve yaz."
#
#  YONTEM (gercek zamanli, ileriye bakis yok): her gun e icin kutu = [d, e], d = son N bardaki en dusuk Low (yeni dip). Kutu dipten
#    baslar; dipten onceki raf/dusus kutuya girmez (kural 1). Kutu uzerinde olculer:
#      dip olusumu : kutu oncesi inis (N bar penceresinde dipten onceki en yuksek kapanis / dip - 1, %) ve konum (kutu medyani,
#                    [d-250, e] araliginin neresinde; 0 = en dip)
#      savunma     : dipten beri gecen bar (dip kirilmadi, cunku d pencere minimumu) ve retest (dibe 1 normal gun yaklasan bar sayisi)
#      yuvarlanma  : dipten sonraki Low'lara parabol (a > 0 ic bukey VE son egim > 0) | ucte-bir kurali (son ucte bir medyani >
#                    orta ucte bir > 0, COL_OBEK) | SMA10 donusu (once duz/asagi sonra yukari)
#      kucuk mum   : kutu araligi medyani / onceki 60 gun medyani; dipten sonra kucuk mum OBEGI sayisi (>= 3 ardisik bar, aralik <=
#                    kutu medyani) ve obeklerin yukselip yukselmedigi
#    VARYANTLAR: N {60,120} x konum {0.35, 0.50, yok} x dipten beri bar {15, 25} x inis {0, 5, 10}% x retest {0, 2} x
#    yuvarlanma {yok, parabol, ucte-bir, sma10} x kucuk mum kat {0.9, 1.0, yok} x obek {1, 2} x obek yukselen {hayir, evet} = 3456.
#    Her varyant icin ayni dip bir kez sinyal verir (ilk saglandigi gun e).
#  SONUC OLCULERI (sinyalden sonra): 60 bar icinde ALIM (yesil kapanis > kutu tavani x 1,002) — iki sayim: (a) uretimdeki gibi once
#    dip -%2 alti kapanis olursa islem yok, (b) kural 3: kirilip toparlansa da alim sayilir; 60/120 bar ileri kapanis; once +%10 mu
#    -%10 mu; alim sonrasi URETIM cikisi getirisi (COL_KAZANC.ck_k3_cikis: dip -%2 stop, +%8'de maliyete, %20 sonra SMA20, 120 bar).
#    TABAN: her 5. gunun 15 mumluk kutusu (tavan = en yuksek govde ustu, dip = en dusuk Low), ayni sonuc olculeri.
#  GOZ TESTI: kalibre_etiketler.csv (29 COL + 8 OLUMSUZ) + goz_esle/etiket_2026-10-20.csv (21 DEGIL): COL yakalandi = etiket bitisinden
#    en gec 5 bar sonra, dibi etiket icinde (bas - 10 bar) olan bir sinyal var; DEGIL yanlis alarm = kutu icinde boyle bir sinyal var.
#    goz_esle/etiket_obek_ARZUM.csv (1 dusen bicak DEGIL + 3 OBEK) ayrica.
#  SECIM: goz testinde COL yakalama >= D12 (16/29) VE yanlis alarm <= D12 (8/29); evrende alim orani ve ileri60 tabandan iyi, 4/4 donem;
#    sinyal sayisi makul. Kazanan parametre seti rapora yazilir; uretime D13 olarak Cemal'in "yaz"i ile gecer.
#  KURAL_MOTORU: K1 veri  K2 ozellikler (her gun)  K3 varyant sinyalleri  K4 sonuclar + taban  K5 goz testi  K6 rapor
#  Calistirma: GitHub Actions 'Arastirma' (betik: COL_TESPIT.py). Cikti: arastirma_cikti/col_tespit/. Yerel prova: kalibre_veri.csv.
# =====================================================================
from __future__ import annotations

import logging
import os
import sys
import time
from dataclasses import dataclass, field
from itertools import product
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view

_CK_ONCE_CT = {k: id(v) for k, v in globals().items()}

CT_SURUM = "COL_TESPIT v1.0 (2026-10-21, D13 adayi: dip -> savunma -> yuvarlanma -> kucuk mum obekleri)"
ctlog = logging.getLogger("col.tespit")
if not ctlog.handlers:
    _ct_h = logging.StreamHandler(sys.stderr)
    _ct_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tespit: %(message)s", "%H:%M:%S"))
    ctlog.addHandler(_ct_h)
    ctlog.setLevel(logging.INFO)
    ctlog.propagate = False


@dataclass
class CTAyar:
    kok: str = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "/content/drive/MyDrive/col_tarayici"
    cikti: Optional[str] = None
    abd: bool = True
    N_list: Tuple[int, ...] = (60, 120)           # yeni dip icin geriye bakis (bar)
    min_gecmis: int = 260
    kenar: int = 3                                # dip pencerenin ilk bu kadar barinda ise inis gorunmuyor -> aday degil
    min_bar: int = 15                             # dipten beri en az bar (en kucuk varyant)
    al_pay: float = 1.002
    boz_tol: float = 0.02
    ileri: int = 60
    taban_adim: int = 5
    taban_w: int = 15
    # varyant izgarasi
    v_konum: Tuple[float, ...] = (0.35, 0.50, 1.01)
    v_bar: Tuple[int, ...] = (15, 25)
    v_inis: Tuple[float, ...] = (0.0, 5.0, 10.0)
    v_retest: Tuple[int, ...] = (0, 2)
    v_yuv: Tuple[str, ...] = ("yok", "parabol", "ucte_bir", "sma10")
    v_kucuk: Tuple[float, ...] = (0.9, 1.0, 99.0)
    v_obek: Tuple[int, ...] = (1, 2)
    v_obek_yuk: Tuple[int, ...] = (0, 1)
    donemler: Tuple = (("2016-19", "2016-01-01", "2019-12-31"), ("2020-22", "2020-01-01", "2022-12-31"),
                       ("2023", "2023-01-01", "2023-12-31"), ("2024-26", "2024-01-01", "2026-12-31"))
    donemler_abd: Tuple = (("ABD 2022-23", "2022-01-01", "2023-12-31"), ("ABD 2024-26", "2024-01-01", "2026-12-31"))
    slot: int = 30
    min_n: int = 60
    en_iyi: int = 15
    etiket_eski: str = "kalibre_etiketler.csv"
    etiket_bugun: str = os.path.join("goz_esle", "etiket_2026-10-20.csv")
    etiket_obek: str = os.path.join("goz_esle", "etiket_obek_ARZUM.csv")
    kalibre_veri: str = "kalibre_veri.csv"


def _ct_mod():
    import importlib
    kok = CTAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST"), importlib.import_module("COL_YOL"), importlib.import_module("COL_KAZANC")


# ------------------------------------------------------------------ K1 veri
def ct_k1_veri(ay: CTAyar, CD) -> Dict[str, pd.DataFrame]:
    if os.path.exists(os.path.join(ay.kok, "veri_1d_turkey.pkl")):
        cay = CD.CDAyar(kok=ay.kok)
        veri = CD.cd_k1_bist(cay); CD.cd_k2_onarim(cay, veri)
        return veri
    v = pd.read_csv(os.path.join(ay.kok, ay.kalibre_veri), parse_dates=["tarih"])
    veri = {s: g.set_index("tarih").sort_index()[["Open", "High", "Low", "Close", "Volume"]].astype(float) for s, g in v.groupby("sembol")}
    ctlog.warning("K1: onbellek yok, yerel %s (%d hisse) — prova", ay.kalibre_veri, len(veri))
    return veri


# ------------------------------------------------------------------ K2 ozellikler
def _parabol(y: np.ndarray) -> Tuple[float, float]:
    """x in [0,1] parabol: (a, son_egim). a>0 ic bukey, son_egim>0 yukari donmus."""
    n = len(y)
    if n < 8:
        return np.nan, np.nan
    x = np.linspace(0.0, 1.0, n)
    a, b, _ = np.polyfit(x, y, 2)
    return float(a), float(2 * a + b)


def _obekler(kucuk: np.ndarray, C: np.ndarray, d: int) -> Tuple[int, float]:
    """kucuk: dipten itibaren kucuk-bar maskesi. >= 3 ardisik kucuk bar = obek. Donus: (obek sayisi, yukselen pay)."""
    n = len(kucuk); i = 0; orta: List[float] = []
    while i < n:
        if kucuk[i]:
            j = i
            while j + 1 < n and kucuk[j + 1]:
                j += 1
            if j - i + 1 >= 3:
                orta.append(float(np.median(C[d + i:d + j + 1])))
            i = j + 1
        else:
            i += 1
    yuk = float(np.mean(np.diff(orta) > 0)) if len(orta) >= 2 else (1.0 if len(orta) == 1 else np.nan)
    return len(orta), yuk


def ct_k2_ozellik(ay: CTAyar, sem: str, df: pd.DataFrame, N: int) -> Tuple[List[Dict[str, Any]], Dict[str, np.ndarray]]:
    """Her gun e icin kutu [d, e] ozellikleri (d = son N barin en dusuk Low'u). Yalniz <= e kullanilir."""
    df = df[np.isfinite(df.Close)]
    O, H, L, C, V = (df[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    n = len(C)
    pc = np.r_[O[0], C[:-1]]
    with np.errstate(divide="ignore", invalid="ignore"):
        ar = 100 * (H - L) / pc
    ref60 = pd.Series(ar).rolling(60, min_periods=40).median().shift(1).to_numpy(float)
    sma10 = pd.Series(C).rolling(10, min_periods=10).mean().to_numpy(float)
    S20 = pd.Series(C).rolling(20, min_periods=20).mean().to_numpy(float)
    gu = np.maximum(O, C)
    A = {"O": O, "H": H, "L": L, "C": C, "V": V, "ar": ar, "S20": S20, "ix": df.index}
    out: List[Dict[str, Any]] = []
    if n < max(ay.min_gecmis, N) + 10:
        return out, A
    Lw = sliding_window_view(L, N)                       # satir k -> pencere [k, k+N-1], e = k+N-1
    dmin = np.argmin(Lw, axis=1)
    for e in range(max(ay.min_gecmis, N - 1), n):
        k = e - N + 1
        d = k + int(dmin[k])
        bs = e - d
        if bs < ay.min_bar or d - k < ay.kenar:
            continue
        r60 = ref60[d]
        if not (np.isfinite(r60) and r60 > 0):
            continue
        dip = L[d]
        if not (np.isfinite(dip) and dip > 0):
            continue
        o0 = max(0, d - 250)
        lo, hi = float(np.nanmin(L[o0:e + 1])), float(np.nanmax(H[o0:e + 1]))
        kutuC = C[d:e + 1]
        konum = float((np.median(kutuC) - lo) / (hi - lo)) if hi > lo else np.nan
        inis = float(np.nanmax(C[k:d]) / dip - 1) * 100
        retest = int(np.sum(L[d + 1:e + 1] <= dip * (1 + r60 / 100)))
        y = L[d:e + 1] / dip - 1
        a, son_egim = _parabol(100 * y)
        parabol = bool(np.isfinite(a) and a > 0 and son_egim > 0)
        k3 = max(2, len(y) // 3)
        ucte_bir = bool(np.median(y[-k3:]) > np.median(y[k3:2 * k3]) > 0)
        seg = sma10[d:e + 1]; kk = max(3, len(seg) // 3)
        sma_d = bool(np.isfinite(seg[kk - 1]) and np.isfinite(seg[0]) and (seg[kk - 1] - seg[0]) <= 0 and (seg[-1] - seg[-kk]) > 0)
        arb = ar[d:e + 1]; med = float(np.nanmedian(arb))
        kucuk_kat = med / r60
        ob, ob_yuk = _obekler(arb <= med, C, d)
        out.append({"sembol": sem, "N": N, "e": e, "d": d, "bar": bs, "konum": konum, "inis": inis, "retest": retest,
                    "parabol": parabol, "ucte_bir": ucte_bir, "sma10": sma_d, "kucuk_kat": kucuk_kat, "obek": ob, "obek_yuk": ob_yuk,
                    "dip": float(dip), "tavan": float(np.nanmax(gu[d:e + 1])), "sinyal": df.index[e]})
    return out, A


# ------------------------------------------------------------------ K3 varyantlar
def ct_varyantlar(ay: CTAyar) -> pd.DataFrame:
    rows = []
    for N, konum, bar, inis, retest, yuv, kucuk, obek, oy in product(ay.N_list, ay.v_konum, ay.v_bar, ay.v_inis, ay.v_retest, ay.v_yuv,
                                                                    ay.v_kucuk, ay.v_obek, ay.v_obek_yuk):
        rows.append({"N": N, "konum": konum, "bar": bar, "inis": inis, "retest": retest, "yuv": yuv, "kucuk": kucuk, "obek": obek, "obek_yuk": oy})
    V = pd.DataFrame(rows); V["vid"] = np.arange(len(V))
    return V


def _maske(F: pd.DataFrame, v: pd.Series) -> np.ndarray:
    m = (F.N.to_numpy() == v.N) & (F.bar.to_numpy() >= v.bar) & (F.inis.to_numpy() >= v.inis) & (F.retest.to_numpy() >= v.retest)
    m &= np.nan_to_num(F.konum.to_numpy(float), nan=9.0) <= v.konum
    m &= np.nan_to_num(F.kucuk_kat.to_numpy(float), nan=9.0) <= v.kucuk
    m &= F.obek.to_numpy() >= v.obek
    if v.obek_yuk:
        m &= np.nan_to_num(F.obek_yuk.to_numpy(float), nan=0.0) >= 0.999
    if v.yuv != "yok":
        m &= F[v.yuv].to_numpy(bool)
    return m


def ct_k3_sinyal(ay: CTAyar, F: pd.DataFrame, V: pd.DataFrame) -> Tuple[Dict[str, np.ndarray], pd.DataFrame]:
    """Her varyant icin (sembol, N, d) basina ILK saglanan e = sinyal. Bellek dostu: sinyaller iki int32 dizi (vid, satir),
    vid'e gore sirali; vid_bas[v]..vid_bas[v+1] o varyantin satirlari. Donus: (S dict, sirali F)."""
    t0 = time.monotonic()
    F = F.sort_values(["sembol", "N", "d", "e"]).reset_index(drop=True)
    anahtar = (F.sembol.astype(str) + "|" + F.N.astype(str) + "|" + F.d.astype(str)).to_numpy()
    kod = pd.factorize(anahtar)[0]
    parcalar: List[np.ndarray] = []; vid_bas = np.zeros(len(V) + 1, dtype=np.int64)
    for v in V.itertuples():
        m = _maske(F, v)
        idx = np.flatnonzero(m)
        if len(idx):
            _, ilk = np.unique(kod[idx], return_index=True)
            sat = idx[ilk].astype(np.int32)
        else:
            sat = np.zeros(0, dtype=np.int32)
        parcalar.append(sat); vid_bas[v.vid + 1] = vid_bas[v.vid] + len(sat)
    satir = np.concatenate(parcalar) if parcalar else np.zeros(0, dtype=np.int32)
    S = {"satir": satir, "vid_bas": vid_bas}
    ctlog.info("K3: %d varyant, %d sinyal kaydi, %d benzersiz (sembol,e) (%.0f sn)", len(V), len(satir), len(np.unique(satir)), time.monotonic() - t0)
    return S, F


def _vid_satir(S: Dict[str, np.ndarray], vid: int) -> np.ndarray:
    return S["satir"][S["vid_bas"][vid]:S["vid_bas"][vid + 1]]


# ------------------------------------------------------------------ K4 sonuclar
def _sonuc(A: Dict[str, np.ndarray], e: int, dip: float, tavan: float, ay: CTAyar) -> Dict[str, Any]:
    """Sinyal gunu e'den sonra: alim (a: bozulma kesmeli, b: kesmesiz), bozulma, ileri60/120, once +10 / -10."""
    O, H, L, C = A["O"], A["H"], A["L"], A["C"]; n = len(C)
    tv, dp = tavan * ay.al_pay, dip * (1 - ay.boz_tol)
    son = min(n - 1, e + ay.ileri)
    alim_a = alim_b = None; boz_i = None
    for i in range(e + 1, son + 1):
        if C[i] > tv and C[i] > O[i]:
            if alim_b is None: alim_b = i
            if alim_a is None and boz_i is None: alim_a = i
            if alim_a is not None: break
        if C[i] < dp and boz_i is None:
            boz_i = i
            if alim_b is not None: break
    c0 = C[e]
    out = {"alim_a": alim_a, "alim_b": alim_b, "bozulma": int(boz_i is not None and (alim_b is None or boz_i < alim_b)),
           "toparlanan": int(boz_i is not None and alim_b is not None and boz_i < alim_b)}
    for h in (60, 120):
        out[f"ileri{h}"] = round(float(C[e + h] / c0 - 1) * 100, 2) if (e + h < n and c0 > 0) else np.nan
    if e + 60 < n and c0 > 0:
        pen = slice(e + 1, e + 61)
        yu = np.where(H[pen] >= c0 * 1.10)[0]; ya = np.where(L[pen] <= c0 * 0.90)[0]
        out["once_yukari"] = int(len(yu) > 0 and (len(ya) == 0 or yu[0] < ya[0]))
    else:
        out["once_yukari"] = np.nan
    return out


def ct_k4_sonuc(ay: CTAyar, CK, CY, U: pd.DataFrame, D: Dict[str, Dict[str, np.ndarray]], veri: Dict[str, pd.DataFrame]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """U benzersiz sinyal satirlarina sonuc olculeri + uretim cikisi getirisi (alim_a ve alim_b icin ayri). Taban kutulari da uretilir."""
    t0 = time.monotonic()
    U = U.copy()
    son: List[Dict[str, Any]] = []
    for r in U.itertuples():
        son.append(_sonuc(D[r.sembol], int(r.e), float(r.dip), float(r.tavan), ay))
    U = pd.concat([U.reset_index(drop=True), pd.DataFrame(son)], axis=1)
    # uretim cikisi: alim_a (bozulma kesmeli) ve alim_b (kesmesiz) ayri
    cay = CK.CKAyar(kok=ay.kok)
    for ad in ("alim_a", "alim_b"):
        isl = []
        for r in U.itertuples():
            b = getattr(r, ad)
            if b is None or (isinstance(b, float) and not np.isfinite(b)):
                continue
            b = int(b)
            if b + 1 >= len(D[r.sembol]["C"]):
                continue
            isl.append({"sembol": r.sembol, "u": int(r.Index), "sinyal_i": int(r.e), "alim_i": b, "giris_i": b + 1, "stop0": float(r.dip) * (1 - ay.boz_tol)})
        T = CK.ck_k3_cikis(cay, CY, isl, D) if isl else pd.DataFrame(columns=["u", "getiri", "bar"])
        g = T.set_index("u").getiri if len(T) else pd.Series(dtype=float)
        U[f"getiri_{ad[-1]}"] = U.index.map(g).astype(float)
    # taban kutulari
    tb: List[Dict[str, Any]] = []
    for sem, A in D.items():
        O, H, L, C = A["O"], A["H"], A["L"], A["C"]; n = len(C); gu = np.maximum(O, C)
        for e in range(ay.min_gecmis, n - 1, ay.taban_adim):
            s = e - ay.taban_w + 1
            dip, tavan = float(np.nanmin(L[s:e + 1])), float(np.nanmax(gu[s:e + 1]))
            if not (np.isfinite(dip) and dip > 0):
                continue
            tb.append({"sembol": sem, "e": e, "d": s + int(np.nanargmin(L[s:e + 1])), "dip": dip, "tavan": tavan, "sinyal": A["ix"][e], **_sonuc(A, e, dip, tavan, ay)})
    TB = pd.DataFrame(tb)
    if len(TB):
        isl = [{"sembol": r.sembol, "u": int(r.Index), "sinyal_i": int(r.e), "alim_i": int(r.alim_a), "giris_i": int(r.alim_a) + 1, "stop0": float(r.dip) * (1 - ay.boz_tol)}
               for r in TB.itertuples() if r.alim_a is not None and not (isinstance(r.alim_a, float) and not np.isfinite(r.alim_a)) and int(r.alim_a) + 1 < len(D[r.sembol]["C"])]
        T = CK.ck_k3_cikis(cay, CY, isl, D) if isl else pd.DataFrame(columns=["u", "getiri"])
        g = T.set_index("u").getiri if len(T) else pd.Series(dtype=float)
        TB["getiri_a"] = TB.index.map(g).astype(float)
    ctlog.info("K4: %d sinyal satiri, %d taban kutusu (%.0f sn)", len(U), len(TB), time.monotonic() - t0)
    return U, TB


# ------------------------------------------------------------------ K5 goz testi
def ct_k5_etiket(ay: CTAyar) -> pd.DataFrame:
    e1 = pd.read_csv(os.path.join(ay.kok, ay.etiket_eski), parse_dates=["bas", "son"])
    e1["sinif"] = e1.sinif.map({"COL": "COL", "OLUMSUZ": "DEGIL"}).fillna(e1.sinif); e1["set"] = "eski"
    e = e1[["sembol", "bas", "son", "sinif", "set"]]
    y2 = os.path.join(ay.kok, ay.etiket_bugun)
    if os.path.exists(y2):
        e2 = pd.read_csv(y2, parse_dates=["kutu_bas", "kutu_son"])
        e2 = pd.DataFrame({"sembol": e2.sembol, "bas": e2.kutu_bas, "son": e2.kutu_son,
                           "sinif": np.where(e2.cemal.astype(str).str.upper().str.startswith("COL"), "COL", "DEGIL"), "set": "bugun"})
        e = pd.concat([e, e2], ignore_index=True)
    y3 = os.path.join(ay.kok, ay.etiket_obek)
    if os.path.exists(y3):
        e3 = pd.read_csv(y3, parse_dates=["obek_bas", "obek_son"])
        e3 = pd.DataFrame({"sembol": e3.sembol, "bas": e3.obek_bas, "son": e3.obek_son,
                           "sinif": np.where(e3.cemal.astype(str).str.upper().str.startswith("OBEK"), "COL", "DEGIL"), "set": "arzum"})
        e = pd.concat([e, e3], ignore_index=True)
    e["etiket"] = e.sembol + "_" + e.bas.dt.strftime("%Y%m%d")
    return e.reset_index(drop=True)


def ct_k5_goz(ay: CTAyar, E: pd.DataFrame, F: pd.DataFrame, S: Dict[str, np.ndarray], V: pd.DataFrame, D: Dict[str, Dict[str, np.ndarray]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Her etiket x varyant: yakalandi mi. COL: etiket bitisi + 5 bar icinde, dibi (bas - 10 bar) sonrasinda olan sinyal.
    DEGIL: ayni pencere icinde sinyal = yanlis alarm. Donus: (etiket x varyant uzun tablo, varyant ozeti)."""
    t0 = time.monotonic()
    satir, vid_bas = S["satir"], S["vid_bas"]
    # satir -> vid (sinyal kaydi sirasina gore vid dizisi) ve satira gore siralama
    vid_of = np.repeat(np.arange(len(V), dtype=np.int32), np.diff(vid_bas))
    sira = np.argsort(satir, kind="stable"); satir_s = satir[sira]; vid_s = vid_of[sira]
    Fsem = F.sembol.to_numpy(); Fe = F.e.to_numpy(); Fd = F.d.to_numpy()
    rows = []
    for r in E.itertuples():
        A = D.get(r.sembol)
        if A is None or A["ix"][-1] < r.bas:
            rows.append({"etiket": r.etiket, "sinif": r.sinif, "set": r.set, "veri": 0, "vid": -1}); continue
        ix = A["ix"]
        s_i = int(ix.searchsorted(r.bas)); e_i = int(ix.searchsorted(r.son, side="right")) - 1
        cand = np.flatnonzero((Fsem == r.sembol) & (Fe >= s_i) & (Fe <= e_i + 5) & (Fd >= s_i - 10) & (Fd <= e_i))
        vids: set = set()
        for c in cand:
            lo = np.searchsorted(satir_s, c, side="left"); hi = np.searchsorted(satir_s, c, side="right")
            if hi > lo:
                vids.update(vid_s[lo:hi].tolist())
        for vid in vids:
            rows.append({"etiket": r.etiket, "sinif": r.sinif, "set": r.set, "veri": 1, "vid": int(vid)})
        rows.append({"etiket": r.etiket, "sinif": r.sinif, "set": r.set, "veri": 1, "vid": -1})   # veri var kaydi
    G = pd.DataFrame(rows)
    var = G[G.veri == 1].drop_duplicates(["etiket"])
    n_col = int((var.sinif == "COL").sum()); n_deg = int((var.sinif == "DEGIL").sum())
    n_col_arz = int(((var.sinif == "COL") & (var.set == "arzum")).sum()); n_deg_arz = int(((var.sinif == "DEGIL") & (var.set == "arzum")).sum())
    hit = G[G.vid >= 0].copy()
    hit["c1"] = ((hit.sinif == "COL") & (hit.set != "arzum")).astype(int); hit["c2"] = ((hit.sinif == "DEGIL") & (hit.set != "arzum")).astype(int)
    hit["c3"] = ((hit.sinif == "COL") & (hit.set == "arzum")).astype(int); hit["c4"] = ((hit.sinif == "DEGIL") & (hit.set == "arzum")).astype(int)
    oz = hit.groupby("vid")[["c1", "c2", "c3", "c4"]].sum().reset_index().rename(columns={"c1": "col_yakalanan", "c2": "degil_yanlis", "c3": "arzum_obek", "c4": "arzum_bicak"})
    oz = V[["vid"]].merge(oz, on="vid", how="left").fillna(0)
    oz["col_n"] = n_col - n_col_arz; oz["degil_n"] = n_deg - n_deg_arz; oz["arzum_obek_n"] = n_col_arz; oz["arzum_bicak_n"] = n_deg_arz
    ctlog.info("K5 goz: %d etiket (veri olan COL %d, DEGIL %d) (%.0f sn)", len(E), n_col, n_deg, time.monotonic() - t0)
    return G, oz


# ------------------------------------------------------------------ K6 ozet + rapor
def ct_k6_ozet(ay: CTAyar, CD, F: pd.DataFrame, S: Dict[str, np.ndarray], U: pd.DataFrame, TB: pd.DataFrame, V: pd.DataFrame, GO: pd.DataFrame,
               donemler_hepsi: List[Tuple[str, Tuple]], pazar_of: Dict[str, str]):
    """Varyant x donem: n, alim_a %, alim_b %, bozulma %, toparlanan %, ileri60/120 ort, once+10 %, getiri_a/b ort; taban farki.
    Bellek dostu: sonuc olculeri F satirina hizali dizilere yazilir, varyant basina numpy ile toplanir."""
    t0 = time.monotonic()
    nF = len(F)
    # F satirina hizali sonuc dizileri
    kol = {"alim_a": np.full(nF, np.nan), "alim_b": np.full(nF, np.nan), "bozulma": np.full(nF, np.nan), "toparlanan": np.full(nF, np.nan),
           "ileri60": np.full(nF, np.nan), "ileri120": np.full(nF, np.nan), "once": np.full(nF, np.nan), "getiri_a": np.full(nF, np.nan), "getiri_b": np.full(nF, np.nan)}
    # U, F'nin alt kumesi (ayni sembol,e); F satir indeksini sembol|N|e anahtarindan bul
    Fkey = pd.Series(np.arange(nF), index=pd.MultiIndex.from_arrays([F.sembol.to_numpy(), F.N.to_numpy(), F.e.to_numpy()]))
    ui = Fkey.reindex(pd.MultiIndex.from_arrays([U.sembol.to_numpy(), U.N.to_numpy(), U.e.to_numpy()])).to_numpy()
    ok = np.isfinite(ui.astype(float)); ui = ui[ok].astype(int); Uo = U[ok]
    kol["alim_a"][ui] = Uo.alim_a.notna().to_numpy(float); kol["alim_b"][ui] = Uo.alim_b.notna().to_numpy(float)
    for k in ("bozulma", "toparlanan", "ileri60", "ileri120", "getiri_a", "getiri_b"):
        kol[k][ui] = Uo[k].to_numpy(float)
    kol["once"][ui] = Uo.once_yukari.to_numpy(float)
    kol["ileri60"] = np.minimum(kol["ileri60"], 200); kol["ileri120"] = np.minimum(kol["ileri120"], 200); kol["getiri_a"] = np.minimum(kol["getiri_a"], 200); kol["getiri_b"] = np.minimum(kol["getiri_b"], 200)
    # donem kodu (F satirina hizali)
    pazar = F.sembol.map(pazar_of).to_numpy()
    tarih = pd.to_datetime(F.sinyal).to_numpy()
    don_kod = np.full(nF, -1, dtype=np.int16); don_adlar: List[str] = []
    for pz, dl in donemler_hepsi:
        for ad, b_, s_ in dl:
            m = (pazar == pz) & (tarih >= np.datetime64(b_)) & (tarih <= np.datetime64(s_))
            don_kod[m] = len(don_adlar); don_adlar.append(ad)
    # taban ozetleri
    TB = TB.copy(); TB["pazar"] = TB.sembol.map(pazar_of)
    taban_oz: Dict[str, Dict[str, float]] = {}
    for pz, dl in donemler_hepsi:
        for ad, b_, s_ in dl:
            t = TB[(TB.pazar == pz) & (TB.sinyal >= b_) & (TB.sinyal <= s_)]
            if len(t):
                taban_oz[ad] = {"n": len(t), "alim_a": t.alim_a.notna().mean(), "alim_b": t.alim_b.notna().mean(), "bozulma": t.bozulma.mean(),
                                "ileri60": t.ileri60.clip(upper=200).mean(), "ileri120": t.ileri120.clip(upper=200).mean(), "once": t.once_yukari.mean(),
                                "getiri_a": t.getiri_a.clip(upper=200).mean()}
    rows = []
    def _m(a):
        a = a[np.isfinite(a)]; return float(a.mean()) if len(a) else np.nan
    for vid in range(len(V)):
        idx = _vid_satir(S, vid)
        if not len(idx):
            continue
        dk = don_kod[idx]
        for di, ad in enumerate(don_adlar):
            sel = idx[dk == di]
            if len(sel) < ay.min_n:
                continue
            tbo = taban_oz.get(ad, {})
            r = {"vid": vid, "donem": ad, "n": int(len(sel)), "alim_a": _m(kol["alim_a"][sel]), "alim_b": _m(kol["alim_b"][sel]), "bozulma": _m(kol["bozulma"][sel]),
                 "toparlanan": _m(kol["toparlanan"][sel]), "ileri60": _m(kol["ileri60"][sel]), "ileri120": _m(kol["ileri120"][sel]), "once": _m(kol["once"][sel]),
                 "getiri_a": _m(kol["getiri_a"][sel]), "getiri_b": _m(kol["getiri_b"][sel]), "n_islem_a": int(np.isfinite(kol["getiri_a"][sel]).sum())}
            for k in ("alim_a", "alim_b", "ileri60", "ileri120", "getiri_a"):
                r[f"f_{k}"] = r[k] - tbo.get(k, np.nan)
            rows.append(r)
    OZ = pd.DataFrame(rows)
    def _oz(g):
        return pd.Series({"donem": len(g), "n_top": int(g.n.sum()), "alim_arti": int((g.f_alim_a > 0.10).sum()), "i60_arti": int((g.f_ileri60 > 0).sum()),
                          "getiri_arti": int((g.f_getiri_a > 0).sum()), "f_alim": g.f_alim_a.mean(), "f_i60": g.f_ileri60.mean(), "f_i120": g.f_ileri120.mean(),
                          "f_getiri": g.f_getiri_a.mean(), "bozulma": g.bozulma.mean(), "toparlanan": g.toparlanan.mean(), "alim_b_eksi_a": (g.alim_b - g.alim_a).mean()})
    VO = OZ.groupby("vid")[["n", "f_alim_a", "f_ileri60", "f_ileri120", "f_getiri_a", "bozulma", "toparlanan", "alim_b", "alim_a"]].apply(_oz).reset_index() if len(OZ) else pd.DataFrame(columns=["vid"])
    VO = V.merge(VO, on="vid", how="left").merge(GO, on="vid", how="left")
    VO["skor"] = (VO.col_yakalanan.fillna(0) / VO.col_n.replace(0, np.nan).fillna(1) - VO.degil_yanlis.fillna(0) / VO.degil_n.replace(0, np.nan).fillna(1)) \
        + 0.1 * VO.alim_arti.fillna(0) + 0.1 * VO.i60_arti.fillna(0) + 0.05 * VO.getiri_arti.fillna(0)
    ctlog.info("K6 ozet: %d varyant x donem satiri (%.0f sn)", len(OZ), time.monotonic() - t0)
    return OZ, VO, taban_oz


def _vtanim(v) -> str:
    return (f"N{int(v.N)} konum<={v.konum:g} bar>={int(v.bar)} inis>={v.inis:g}% retest>={int(v.retest)} yuv={v.yuv} "
            f"kucuk<={v.kucuk:g} obek>={int(v.obek)} obek_yuk={'evet' if v.obek_yuk else 'hayir'}")


def ct_k7_rapor(ay: CTAyar, OZ: pd.DataFrame, VO: pd.DataFrame, taban_oz: Dict[str, Dict[str, float]], G: pd.DataFrame, E: pd.DataFrame,
                cikti: str, donemler_hepsi: List[Tuple[str, Tuple]]) -> str:
    sat = [f"# COL TESPIT — Cemal'in uc kurali ile tespit motoru adaylari   ({CT_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Kutu = [yeni dip d, bugun e] (d = son N barin en dusuk Low'u; dipten onceki raf/dusus kutuya girmez). Varyant = esikler; her dip bir kez sinyal.",
           "GOZ: Cemal'in 29 colu (yakalanan) ve 29 'degil' kutusu (yanlis alarm); ARZUM 3 obek + 1 dusen bicak ayri. D12 uretim: 16/29 yakaliyor, 8/29 yanlis alarm.",
           "EVREN: sinyalden sonra 60 barda alim (a: dip -%2 kirilirsa islem yok; b: kirilip toparlansa da sayilir), bozulma, 60/120 bar ileri getiri (%200 kirpili), once +10, alim sonrasi uretim cikisi getirisi. TABAN = her 5. gunun 15 mumluk kutusu. f_ = varyant - taban.",
           "Skor = COL yakalama orani - yanlis alarm orani + 0,1 x (alim tabandan >10 puan iyi donem) + 0,1 x (ileri60 tabandan iyi donem) + 0,05 x (getiri tabandan iyi donem).", ""]
    sat += ["## Taban (donem)", "", "| donem | n | alim a | alim b | bozulma | ileri60 | ileri120 | once +10 | getiri a |", "|---|---|---|---|---|---|---|---|---|"]
    for ad, t in taban_oz.items():
        sat.append(f"| {ad} | {t['n']} | %{100*t['alim_a']:.0f} | %{100*t['alim_b']:.0f} | %{100*t['bozulma']:.0f} | {t['ileri60']:+.2f} | {t['ileri120']:+.2f} | %{100*t['once']:.0f} | {t['getiri_a']:+.2f} |")
    sat.append("")
    VOs = VO.sort_values("skor", ascending=False)
    sat += [f"## En iyi {ay.en_iyi} varyant (skor)", "", "| sira | varyant | COL yak. | DEGIL yanlis | ARZUM obek/bicak | donem | sinyal | alim>taban+10 | i60>taban | getiri>taban | f_alim | f_i60 | f_i120 | f_getiri | bozulma | toparlanan | skor |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, v in enumerate(VOs.head(ay.en_iyi).itertuples(), 1):
        sat.append(f"| {i} | {_vtanim(v)} | {int(v.col_yakalanan)}/{int(v.col_n)} | {int(v.degil_yanlis)}/{int(v.degil_n)} | {int(v.arzum_obek)}/{int(v.arzum_obek_n)} / {int(v.arzum_bicak)}/{int(v.arzum_bicak_n)} | "
                   f"{int(v.donem) if np.isfinite(v.donem) else 0} | {int(v.n_top) if np.isfinite(v.n_top) else 0} | {int(v.alim_arti) if np.isfinite(v.alim_arti) else 0} | {int(v.i60_arti) if np.isfinite(v.i60_arti) else 0} | {int(v.getiri_arti) if np.isfinite(v.getiri_arti) else 0} | "
                   f"{100*v.f_alim:+.0f}p | {v.f_i60:+.2f} | {v.f_i120:+.2f} | {v.f_getiri:+.2f} | %{100*v.bozulma:.0f} | %{100*v.toparlanan:.0f} | {v.skor:.2f} |")
    sat.append("")
    # eksen etkileri: her eksende her deger icin ortalama goz ve evren
    sat += ["## Eksen etkileri (tum varyantlarin ortalamasi)", "", "| eksen | deger | COL yak. ort | DEGIL yanlis ort | f_alim ort | f_i60 ort | f_getiri ort | sinyal ort |", "|---|---|---|---|---|---|---|---|"]
    for ek in ("N", "konum", "bar", "inis", "retest", "yuv", "kucuk", "obek", "obek_yuk"):
        for val, g in VO.groupby(ek):
            sat.append(f"| {ek} | {val} | {g.col_yakalanan.mean():.1f} | {g.degil_yanlis.mean():.1f} | {100*g.f_alim.mean():+.0f}p | {g.f_i60.mean():+.2f} | {g.f_getiri.mean():+.2f} | {g.n_top.mean():.0f} |")
    sat.append("")
    # en iyi varyantin donem tablosu ve etiket listesi
    if len(VOs):
        best = VOs.iloc[0]
        sat += [f"## 1. varyant donem tablosu: {_vtanim(best)}", "", "| donem | n | alim a | alim b | bozulma | toparlanan | ileri60 | ileri120 | once +10 | getiri a | getiri b | f_alim | f_i60 | f_getiri |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in OZ[OZ.vid == best.vid].itertuples():
            sat.append(f"| {r.donem} | {r.n} | %{100*r.alim_a:.0f} | %{100*r.alim_b:.0f} | %{100*r.bozulma:.0f} | %{100*r.toparlanan:.0f} | {r.ileri60:+.2f} | {r.ileri120:+.2f} | %{100*r.once:.0f} | {r.getiri_a:+.2f} | {r.getiri_b:+.2f} | {100*r.f_alim_a:+.0f}p | {r.f_ileri60:+.2f} | {r.f_getiri_a:+.2f} |")
        sat.append("")
        yak = set(G[(G.vid == best.vid)].etiket)
        var = G[G.veri == 1].drop_duplicates("etiket")
        sat += ["### 1. varyant goz testi (etiket basina)", "", "| etiket | sinif | set | yakalandi |", "|---|---|---|---|"]
        for r in E.itertuples():
            v_ = "veri yok" if r.etiket not in set(var.etiket) else ("EVET" if r.etiket in yak else "hayir")
            sat.append(f"| {r.etiket} | {r.sinif} | {r.set} | {v_} |")
        sat.append("")
    sat += ["## Okuma", "", "- Kural 1 (kutu dipten baslar) tum varyantlarda yapisal; kural 3 (kirilip toparlanan) 'alim b - alim a' ve 'toparlanan' sutunlarinda.",
            "- Secim kriteri: COL yakalama >= 16/29 VE yanlis alarm <= 8/29 VE evrende alim ve ileri60 tabandan iyi 4/4 BIST donemi. Gecen yoksa 'araştırıldı, D12 kalır'.", ""]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_TESPIT_rapor.md"), "w", encoding="utf-8").write(metin)
    return metin


# ------------------------------------------------------------------ calistirici
def col_tespit(ay: Optional[CTAyar] = None, veri: Optional[Dict[str, pd.DataFrame]] = None, veri_abd: Optional[Dict[str, pd.DataFrame]] = None) -> Dict[str, Any]:
    ay = ay or CTAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_tespit")
    os.makedirs(cikti, exist_ok=True)
    t0 = time.monotonic()
    CD, CY, CK = _ct_mod()
    if veri is None:
        veri = ct_k1_veri(ay, CD)
    pazarlar: List[Tuple[str, Dict[str, pd.DataFrame], Tuple]] = [("BIST", veri, ay.donemler)]
    if ay.abd and veri_abd is None and os.path.exists(os.path.join(ay.kok, "veri_1d_turkey.pkl")):
        try:
            veri_abd = CD.cd_k1_abd(CD.CDAyar(kok=ay.kok))
        except Exception as ex:
            ctlog.error("ABD: %s", ex)
    if veri_abd:
        pazarlar.append(("ABD", veri_abd, ay.donemler_abd))
    V = ct_varyantlar(ay)
    F_list: List[Dict[str, Any]] = []; D: Dict[str, Dict[str, np.ndarray]] = {}; pazar_of: Dict[str, str] = {}
    for pazar, vr, _ in pazarlar:
        t1 = time.monotonic()
        for k, (sem, df) in enumerate(vr.items()):
            key = sem if pazar == "BIST" else f"{sem}.US"
            pazar_of[key] = pazar
            for N in ay.N_list:
                try:
                    rows, A = ct_k2_ozellik(ay, key, df, N)
                except Exception as ex:
                    ctlog.debug("%s: %s", sem, ex); continue
                F_list.extend(rows); D[key] = A
            if (k + 1) % 100 == 0:
                ctlog.info("K2 %s: %d/%d hisse, %d satir (%.0f sn)", pazar, k + 1, len(vr), len(F_list), time.monotonic() - t1)
    F = pd.DataFrame(F_list)
    ctlog.info("K2 bitti: %d aday gun (%.0f sn)", len(F), time.monotonic() - t0)
    S, F = ct_k3_sinyal(ay, F, V)
    U = F.loc[np.unique(S["satir"])].copy() if len(S["satir"]) else F.iloc[0:0].copy()
    U, TB = ct_k4_sonuc(ay, CK, CY, U, D, veri)
    U.to_csv(os.path.join(cikti, "col_tespit_sinyal.csv.gz"), index=False)
    E = ct_k5_etiket(ay)
    G, GO = ct_k5_goz(ay, E, F, S, V, D)
    donemler_hepsi = [(p, dl) for p, _, dl in pazarlar]
    OZ, VO, taban_oz = ct_k6_ozet(ay, CD, F, S, U, TB, V, GO, donemler_hepsi, pazar_of)
    VO.to_csv(os.path.join(cikti, "col_tespit_varyant.csv"), index=False)
    OZ.to_csv(os.path.join(cikti, "col_tespit_varyant_donem.csv"), index=False)
    G[G.vid >= 0].to_csv(os.path.join(cikti, "col_tespit_goz.csv"), index=False)
    metin = ct_k7_rapor(ay, OZ, VO, taban_oz, G, E, cikti, donemler_hepsi)
    ctlog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"ozellik": F, "sinyal": S, "sonuc": U, "taban": TB, "varyant": VO, "donem": OZ, "goz": G, "rapor": metin, "cikti": cikti}


def _cakisma_kontrol_ct(_once=_CK_ONCE_CT, _dosya='COL_TESPIT.py'):
    g = globals(); kayit = g.setdefault('_CK_KAYIT', {})
    atla = ('_CK_ONCE_CT', '_CK_KAYIT', '_cakisma_kontrol_ct', 'In', 'Out', '_', '_i', '_ii', '_iii', 'get_ipython', 'exit', 'quit')
    std = ('np', 'pd', 'os', 'sys', 'time', 'logging', 'annotations', 'Any', 'Dict', 'List', 'Optional', 'Tuple', 'dataclass', 'field', 'product', 'sliding_window_view')
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith('__') and k not in atla
               and not (k.startswith('_i') and k[2:].isdigit()) and not (k.startswith('_') and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith('__') and k not in atla] + degisen: kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ct()

if __name__ == "__main__":
    R = col_tespit()
    print(R["rapor"])
