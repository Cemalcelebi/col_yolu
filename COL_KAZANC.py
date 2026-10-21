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
#  v1.1 K7 DOGRULAMA (Cemal 21 Eki, 'once izi dogrula'): kucuk alim mumu (alim_mum_kat < 1,5) icin donem x pazar fark + Welch p,
#    Bonferroni / BH-FDR (tum kova x donem hucreleri), taban kutularinda ayni test, esik duyarliligi (1,2/1,5/2/3), fiyat / likidite /
#    volatilite kovalari icinde fark (within-bucket) + iki yonlu tablo, OLS (fiyat, likidite, vol, w, bekleme, piyasa, donem kontrolu),
#    ATR20 normalizasyonu (mum/ATR, govde/ATR) ve desil monotonlugu (Spearman), portfoy etkisinin kaynagi (sayi mi secim mi),
#    karistiricilar, karar kurali. Yeni alanlar: fiyat, atr20_pct, alim_mum_atr, govde_atr, vol20, sektor. Rapor: COL_KAZANC_dogrulama.md.
#    Tek basina: python COL_KAZANC.py dogrula  (col_kazanc_islemler.csv.gz'den okur, veri indirmez).
#  v1.2 K8 BIRIKIM (Cemal 21 Eki, 'yfinance verisiyle kurumsal birikim: NVI ve CMF, yatay/kucuk mumlu donemde pozitif ayrisma var mi, ABD'de test et'):
#    obek (s..e) boyunca CMF20 (son deger ve ortalama), NVI degisimi (NVI[e]/NVI[s]) ve NVI > EMA255, A/D cizgisi ve OBV degisimi
#    (obek hacmine bolunmus, -100..100), obek fiyat degisimi. AKIS sinifi: BIRIKIM = CMF20 > 0,05 VE NVI yukari VE A/D yukari;
#    DAGITIM = ucu de asagi; KARISIK = geri kalan. Uc soru: (A) obekte ayrisma tabana gore daha mi sik? (B) ayrisan obekten sonra
#    alim (kirilim) daha mi sik, bozulma daha mi az, 60 gun ileri getiri daha mi iyi? (C) alim sonrasi uretim cikisiyla getiri farki
#    (K4 kovalarina da girer). Tum obekler (alim gelmeyenler dahil) col_kazanc_obekler.csv.gz'de. Rapor: COL_KAZANC_birikim.md.
#    Tek basina: python COL_KAZANC.py birikim  (kaydedilmis islem + obek dosyalarindan okur).
#  KURAL_MOTORU: K1 veri  K2 islemler (obek + taban, olculerle)  K3 cikis + piyasa/sektor  K4 kova ozeti  K5 bilesik  K6 rapor  K7 dogrulama  K8 birikim
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

CK_SURUM = "COL_KAZANC v1.2 (2026-10-21, K8 birikim: NVI / CMF / A-D ayrismasi)"
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
        # v1.2 K8 birikim (obek boyunca para akisi; alim gununde bilinir)
        "cmf_son": ([-np.inf, -0.05, 0.05, np.inf], ["<-0.05 dagitim", "-0.05-0.05", ">=0.05 birikim"]),
        "cmf_obek": ([-np.inf, -0.05, 0.05, np.inf], ["<-0.05 dagitim", "-0.05-0.05", ">=0.05 birikim"]),
        "nvi_obek_pct": ([-np.inf, 0, 2, np.inf], ["<0", "0-2", ">=2"]),
        "ad_obek": ([-np.inf, -5, 5, np.inf], ["<-5 dagitim", "-5-5", ">=5 birikim"]),
        "obv_obek": ([-np.inf, -5, 5, np.inf], ["<-5", "-5-5", ">=5"]),
        "nvi_ustu": None, "akis": None,                        # kategorik
    })
    kategorik: Tuple[str, ...] = ("onceki_obek", "nvi_ustu", "akis")
    bilesik_en_cok: int = 4         # en tutarli bu kadar ikili sart VE ile birlestirilir


def _ck_mod():
    import importlib
    kok = CKAyar().kok
    if kok not in sys.path:
        sys.path.insert(0, kok)
    return importlib.import_module("COL_DIP_TEST"), importlib.import_module("COL_OBEK"), importlib.import_module("COL_YOL")


# ------------------------------------------------------------------ K2 islemler + olculer
def ck_akis(A: Dict[str, np.ndarray], s: int, e: int) -> Dict[str, Any]:
    """v1.2: obek (s..e) boyunca para akisi. CMF20 son/ort, NVI degisimi ve EMA255 ustu, A/D ve OBV degisimi (obek hacmine bolunmus, %),
    obek fiyat degisimi (%). AKIS: birikim / dagitim / karisik. Yalniz s..e kullanilir (ileriye bakis yok)."""
    C, V = A["C"], A["V"]
    vt = float(np.nansum(V[s:e + 1]))
    def pct(a, c):
        return round(float(a / c - 1) * 100, 2) if (np.isfinite(a) and np.isfinite(c) and c > 0) else np.nan
    def pay(x):
        return round(float(x / vt) * 100, 2) if (np.isfinite(x) and vt > 0) else np.nan
    cmf_son = float(A["CMF20"][e]) if np.isfinite(A["CMF20"][e]) else np.nan
    cmf_obek = float(np.nanmean(A["CMF20"][s:e + 1])) if np.isfinite(A["CMF20"][s:e + 1]).any() else np.nan
    nvi = pct(A["NVI"][e], A["NVI"][s]); ad = pay(A["AD"][e] - A["AD"][max(0, s - 1)]); obv = pay(A["OBV"][e] - A["OBV"][max(0, s - 1)])
    nvi_ustu = int(A["NVI"][e] > A["NVI_E255"][e]) if np.isfinite(A["NVI_E255"][e]) else np.nan
    if np.isfinite(cmf_son) and np.isfinite(nvi) and np.isfinite(ad):
        akis = "birikim" if (cmf_son > 0.05 and nvi > 0 and ad > 0) else ("dagitim" if (cmf_son < -0.05 and nvi < 0 and ad < 0) else "karisik")
    else:
        akis = "?"
    return {"cmf_son": round(cmf_son, 3) if np.isfinite(cmf_son) else np.nan, "cmf_obek": round(cmf_obek, 3) if np.isfinite(cmf_obek) else np.nan,
            "nvi_obek_pct": nvi, "nvi_ustu": nvi_ustu, "ad_obek": ad, "obv_obek": obv, "fiyat_obek_pct": pct(C[e], C[s]), "akis": akis}


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
            "lik60": round(ciro / 1e6, 2),
            # v1.1 K7: fiyat / volatilite / ATR normalizasyonu (alim gunu, ileriye bakis yok)
            "fiyat": round(float(C[b]), 4), "atr20_pct": round(float(A["ATR20"][b] / C[b] * 100), 2) if np.isfinite(A["ATR20"][b]) and C[b] > 0 else np.nan,
            "alim_mum_atr": kat(float(rng), float(A["ATR20"][b])), "govde_atr": kat(float(abs(C[b] - O[b])), float(A["ATR20"][b])),
            "vol20": round(float(A["VOL20"][b]), 2) if np.isfinite(A["VOL20"][b]) else np.nan,
            # v1.1 K7: NATR'nin son 50 gun icindeki yuzdelik sirasi (0 = en dar); 5 gun ileri getiri ve vol genislemesi (SONUC olcusu, ileriye bakar, sinyal degil)
            "natr50_pct": round(float((A["NATR"][max(0, b - 49):b + 1] <= A["NATR"][b]).mean() * 100), 1) if np.isfinite(A["NATR"][b]) else np.nan,
            "ileri5_pct": round(float(C[b + 5] / C[b] * 100 - 100), 2) if b + 5 < len(C) and C[b] > 0 else np.nan,
            "ileri5_vol_kat": kat(float(np.nanmean((H - L)[b + 1:b + 6])), float(A["ATR20"][b])) if b + 5 < len(C) else np.nan,   # H-L / ATR20 (ar yuzde idi, duzeltildi)
            **ck_akis(A, s, e)}                                                                                    # v1.2 K8


def ck_k2_islemler(ay: CKAyar, CO, CY, veri: Dict[str, pd.DataFrame]) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, np.ndarray]], List[Dict[str, Any]]]:
    t0 = time.monotonic()
    oay = CO.COAyar(kok=ay.kok); yay = CY.CYAyar(kok=ay.kok, abd=False)
    isl: List[Dict[str, Any]] = []
    obk: List[Dict[str, Any]] = []                                     # v1.2: tum obek/taban kutulari (alim gelmeyenler dahil)
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
        pc = np.r_[O[0], C[:-1]]
        tr = np.maximum(H - L, np.maximum(np.abs(H - pc), np.abs(L - pc)))
        A["ATR20"] = pd.Series(tr).rolling(20, min_periods=20).mean().to_numpy(float)                       # v1.1
        A["NATR"] = A["ATR20"] / np.where(A["C"] > 0, A["C"], np.nan) * 100                                      # yuzdesel ATR
        with np.errstate(divide="ignore", invalid="ignore"):
            lr = np.log(C / pc)
        A["VOL20"] = (pd.Series(lr).rolling(20, min_periods=20).std(ddof=0) * 100).to_numpy(float)          # gunluk % std
        # v1.2 K8: para akisi serileri. MFM = ((C-L)-(H-C))/(H-L); CMF20 = sum(MFM*V,20)/sum(V,20); A/D = kumulatif MFM*V;
        # OBV = kumulatif isaret(C-pc)*V; NVI: hacim dustugu gun fiyat degisimiyle guncellenir (1000'den), EMA255 ustu klasik sinyal.
        V = A["V"]; hl = H - L
        with np.errstate(divide="ignore", invalid="ignore"):
            mfm = np.where(hl > 0, ((C - L) - (H - C)) / hl, 0.0)
        mfv = pd.Series(mfm * V)
        A["CMF20"] = (mfv.rolling(20, min_periods=20).sum() / pd.Series(V).rolling(20, min_periods=20).sum().replace(0, np.nan)).to_numpy(float)
        A["AD"] = np.nancumsum(mfm * V)
        A["OBV"] = np.nancumsum(np.sign(C - pc) * V)
        pv = np.r_[V[0], V[:-1]]
        with np.errstate(divide="ignore", invalid="ignore"):
            adim = np.where((V < pv) & np.isfinite(C / pc), C / pc, 1.0)
        A["NVI"] = 1000.0 * np.cumprod(np.where(np.isfinite(adim) & (adim > 0), adim, 1.0))
        A["NVI_E255"] = pd.Series(A["NVI"]).ewm(span=255, min_periods=255, adjust=False).mean().to_numpy(float)
        A["ix"] = df.index
        D[sem] = A
        onceki, sira = None, 0
        for r in sig:
            sira = sira + 1 if (onceki is not None and r["s"] - onceki["e"] <= 60) else 1
            b = CY.cy_alim(yay, O, C, r["e"], r["tavan"], r["dip"])
            obk.append({"sembol": sem, "kaynak": "obek", "sinyal": df.index[r["e"]], "w": r["w"], "obek_sira": sira,
                        **ck_akis(A, r["s"], r["e"]), **_ck_sonuc60(A, r["e"], r["dip"] * (1 - yay.boz_tol), b)})
            if b is not None and b + 1 < n and b >= 60:
                isl.append({"sembol": sem, "kaynak": "obek", "sinyal_i": r["e"], "alim_i": b, "giris_i": b + 1,
                            "stop0": r["dip"] * (1 - yay.boz_tol), **ck_olcu(A, r, b, onceki, sira)})
            onceki = r
        if ay.taban:
            for e in range(oay.min_gecmis, n - 1, ay.taban_adim):
                s = e - ay.taban_w + 1
                tavan, dip = float(H[s:e + 1].max()), float(L[s:e + 1].min())
                b = CY.cy_alim(yay, O, C, e, tavan, dip)
                if e >= 60:
                    obk.append({"sembol": sem, "kaynak": "taban", "sinyal": df.index[e], "w": ay.taban_w, "obek_sira": 1,
                                **ck_akis(A, s, e), **_ck_sonuc60(A, e, dip * (1 - yay.boz_tol), b)})
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
    return isl, D, obk


def _ck_sonuc60(A: Dict[str, np.ndarray], e: int, boz: float, b: Optional[int]) -> Dict[str, Any]:
    """v1.2 K8 SONUC olculeri (ileriye bakar; sinyal degil): alim geldi mi, kac barda; dip -%2 altina kapanis (bozulma) alimdan once mi;
    60 bar ileri kapanis / en yuksek / en dusuk (%); once +%10 mu -%10 mu."""
    C, H, L = A["C"], A["H"], A["L"]; n = len(C); son = min(n - 1, e + 60)
    c0 = float(C[e]); pen = slice(e + 1, son + 1)
    out: Dict[str, Any] = {"alim": int(b is not None), "alim_bar": (b - e) if b is not None else np.nan}
    cc = C[pen]
    ilk_boz = int(np.argmax(cc < boz)) + 1 if (cc < boz).any() else None
    out["bozulma"] = int(ilk_boz is not None and (b is None or ilk_boz < b - e))
    if son - e >= 60 and c0 > 0:
        out["ileri60_pct"] = round(float(C[son] / c0 - 1) * 100, 2)
        out["ileri60_max"] = round(float(np.nanmax(H[pen]) / c0 - 1) * 100, 2); out["ileri60_min"] = round(float(np.nanmin(L[pen]) / c0 - 1) * 100, 2)
        yu = np.where(H[pen] >= c0 * 1.10)[0]; ya = np.where(L[pen] <= c0 * 0.90)[0]
        out["once_yukari"] = int(len(yu) > 0 and (len(ya) == 0 or yu[0] < ya[0]))
    else:
        out.update({"ileri60_pct": np.nan, "ileri60_max": np.nan, "ileri60_min": np.nan, "once_yukari": np.nan})
    return out


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
    T["sektor"] = [sek.get(x, "?") for x in T.sembol]                                                     # v1.1
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



# ------------------------------------------------------------------ K7 dogrulama: kucuk alim mumu izi (v1.1)
def _p_welch(a: np.ndarray, b: np.ndarray) -> float:
    """Iki ortalama farki icin Welch t, normal yaklasimla iki yonlu p (n buyuk; scipy yok)."""
    import math
    a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    if se == 0:
        return np.nan
    return float(math.erfc(abs(a.mean() - b.mean()) / se / math.sqrt(2)))


def _bh_fdr(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg q degerleri (NaN'lar atlanir)."""
    q = np.full(len(p), np.nan); m = np.isfinite(p); pv = p[m]; n = len(pv)
    if n == 0:
        return q
    sira = np.argsort(pv); rank = np.arange(1, n + 1)
    qq = np.minimum.accumulate((pv[sira] * n / rank)[::-1])[::-1]
    out = np.empty(n); out[sira] = np.minimum(qq, 1.0); q[m] = out
    return q


def _spearman(x: np.ndarray, y: np.ndarray) -> float:
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan
    rx = pd.Series(x[m]).rank().to_numpy(); ry = pd.Series(y[m]).rank().to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def _ols(y: np.ndarray, X: np.ndarray, adlar: List[str]) -> pd.DataFrame:
    """Sabitli EKK; katsayi, SE (HC0 sagla), t. Eksik satirlar atilir."""
    m = np.isfinite(y) & np.all(np.isfinite(X), axis=1)
    y = y[m]; X = np.column_stack([np.ones(m.sum()), X[m]])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    XtX_inv = np.linalg.pinv(X.T @ X)
    meat = (X * (e ** 2)[:, None]).T @ X
    V = XtX_inv @ meat @ XtX_inv
    se = np.sqrt(np.diag(V))
    return pd.DataFrame({"degisken": ["sabit"] + adlar, "katsayi": beta, "se": se, "t": beta / se, "n": m.sum()})


def _slot_fark(CD, x: pd.DataFrame, xa: pd.DataFrame, slot: int) -> Tuple[float, float]:
    sa = CD._cd_slot(xa.assign(getiri=xa.getiri.clip(upper=200)), slot)[0] if len(xa) else np.nan
    sk = CD._cd_slot(x.assign(getiri=x.getiri.clip(upper=200)), slot)[0] if len(x) else np.nan
    return sk, sa


def ck_k7_dogrula(ay: CKAyar, CD, T: pd.DataFrame, cikti: str, donemler_hepsi: List[Tuple[str, Tuple]], olcu: str = "alim_mum_kat",
                  esik: float = 1.5, esikler: Tuple[float, ...] = (1.2, 1.5, 2.0, 3.0)) -> str:
    """Kucuk alim mumu (olcu < esik) izinin dogrulamasi. Rapor COL_KAZANC_dogrulama.md."""
    t0 = time.monotonic()
    T = T.copy()
    T["g"] = T.getiri.clip(upper=200)
    T["kucuk"] = (T[olcu] < esik).astype(float).where(T[olcu].notna())
    don_list = [(pazar, ad, b, s_) for pazar, dl in donemler_hepsi for ad, b, s_ in dl]
    def _don(x: pd.DataFrame, pazar: str, b: str, s_: str) -> pd.DataFrame:
        return x[(x.pazar == pazar) & (x.sinyal >= b) & (x.sinyal <= s_)]
    sat = [f"# COL KAZANC — DOGRULAMA: kucuk alim mumu izi ({olcu} < {esik})   ({CK_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Soru (Cemal 21 Eki): 'alim mumu kucuk olsun' sarti gercek iz mi, yoksa volatilite / fiyat / likidite / cok test artefakti mi?",
           "Fark = kucuk mum islemlerinin ort getirisi (%200 kirpili) - geri kalanin ort getirisi (puan). p = Welch, normal yaklasim. Slot = 30 slot portfoy.", ""]
    # ---- 1. donem x pazar, esik duyarliligi, taban, coklu test
    sat += ["## 1. Donem x pazar fark, esik duyarliligi (obek islemleri; parantez icinde TABAN kutulari)", "",
            "| esik | donem | n kucuk / n diger | fark ort | kazanan fark | p | slot kucuk / hepsi | TABAN fark (p) |", "|---|---|---|---|---|---|---|---|"]
    p_ana: Dict[Tuple[float, str], float] = {}
    for e in esikler:
        for pazar, ad, b, s_ in don_list:
            x0 = _don(T[T.kaynak == "obek"], pazar, b, s_); tb = _don(T[T.kaynak == "taban"], pazar, b, s_)
            k = x0[x0[olcu] < e]; d = x0[x0[olcu] >= e]
            if len(k) < ay.min_n or len(d) < ay.min_n:
                continue
            p = _p_welch(k.g.to_numpy(), d.g.to_numpy()); p_ana[(e, ad)] = p
            tk = tb[tb[olcu] < e]; td = tb[tb[olcu] >= e]
            tf = (tk.g.mean() - td.g.mean()) if len(tk) >= ay.min_n and len(td) >= ay.min_n else np.nan
            tp = _p_welch(tk.g.to_numpy(), td.g.to_numpy()) if np.isfinite(tf) else np.nan
            sk, sa = _slot_fark(CD, k, x0, ay.slot)
            sat.append(f"| {e} | {ad} | {len(k)} / {len(d)} | {k.g.mean() - d.g.mean():+.2f} | {100 * ((k.getiri > 0).mean() - (d.getiri > 0).mean()):+.1f} | {p:.3f} | {sk:+.0f}% / {sa:+.0f}% | {tf:+.2f} ({tp:.3f}) |")
    sat.append("")
    # havuz p + Bonferroni + BH (tum kova x donem hucreleri)
    hucre: List[Dict[str, Any]] = []
    ref = T[T.kaynak == "obek"]
    for ol in ay.kovalar:
        if ol not in T.columns:
            continue
        kova, et, _ = ck_kova(ay, T, ol, ref)
        Tk = T.assign(_k=kova)
        for pazar, ad, b, s_ in don_list:
            x0 = _don(Tk[Tk.kaynak == "obek"], pazar, b, s_)
            for kv in et:
                a = x0[x0._k == kv]; r = x0[x0._k != kv]
                if len(a) >= ay.min_n and len(r) >= ay.min_n:
                    hucre.append({"olcu": ol, "kova": kv, "donem": ad, "fark": a.g.mean() - r.g.mean(), "p": _p_welch(a.g.to_numpy(), r.g.to_numpy())})
    H = pd.DataFrame(hucre)
    H["q_bh"] = _bh_fdr(H.p.to_numpy())
    m_kova = H.groupby(["olcu", "kova"]).ngroups; m_hucre = len(H)
    H.to_csv(os.path.join(cikti, "col_kazanc_dogrulama_hucre.csv"), index=False)
    sat += ["### Coklu test duzeltmesi", "", f"Tarama: {m_kova} kova (olcu x kova), {m_hucre} kova x donem hucresi. Bonferroni esigi 0,05/{m_kova} = {0.05 / m_kova:.5f} (kova) ve 0,05/{m_hucre} = {0.05 / m_hucre:.6f} (hucre).", ""]
    for pazar, dl in donemler_hepsi:
        xo = T[(T.kaynak == "obek") & (T.pazar == pazar)]
        k = xo[xo[olcu] < esik]; d = xo[xo[olcu] >= esik]
        p = _p_welch(k.g.to_numpy(), d.g.to_numpy())
        sat.append(f"- {pazar} havuz (tum donemler): n {len(k)} / {len(d)}, fark {k.g.mean() - d.g.mean():+.2f}, p = {p:.2e} -> Bonferroni(kova) {'GECER' if p < 0.05 / m_kova else 'GECMEZ'}, Bonferroni(hucre) {'GECER' if p < 0.05 / m_hucre else 'GECMEZ'}")
    hk = H[(H.olcu == olcu) & (H.kova.astype(str).str.startswith("<1.5"))]
    sat.append(f"- BH-FDR (q < 0,10) ile ayakta kalan hucre: {int((H.q_bh < 0.10).sum())} / {m_hucre}; kucuk mum hucreleri: " +
               (", ".join(f"{r.donem} q={r.q_bh:.2f}" for r in hk.itertuples()) if len(hk) else "-"))
    sat.append("")
    # ---- 2. kaynak ayristirma: fiyat / likidite / volatilite kovalari icinde
    sat += ["## 2. Kaynak ayristirma — kova icinde kucuk vs buyuk mum farki (pazar havuzu, obek)", ""]
    within: List[Dict[str, Any]] = []
    for pazar, _ in donemler_hepsi:
        xo = T[(T.kaynak == "obek") & (T.pazar == pazar)].copy()
        if xo.empty:
            continue
        xo["fiyat_k"] = pd.cut(xo.fiyat, [-np.inf, 5, 20, 50, 100, np.inf], labels=["<5", "5-20", "20-50", "50-100", ">100"], right=False).astype(object)
        for ad, kol in (("lik60", "lik_k"), ("vol20", "vol_k"), ("atr20_pct", "atr_k")):
            try:
                xo[kol] = pd.qcut(xo[ad].rank(method="first"), 5, labels=[f"Q{i}" for i in range(1, 6)]).astype(object)
            except Exception:
                xo[kol] = "?"
        for grup, kol in (("fiyat", "fiyat_k"), ("likidite (lik60 besteblik)", "lik_k"), ("volatilite (vol20 besteblik)", "vol_k"), ("ATR% (atr20_pct besteblik)", "atr_k")):
            sat += [f"### {pazar} — {grup}", "", "| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |", "|---|---|---|---|---|---|---|"]
            for kv, g in xo.groupby(kol, sort=True):
                k = g[g.kucuk == 1]; d = g[g.kucuk == 0]
                if len(k) < ay.min_n or len(d) < ay.min_n:
                    continue
                p = _p_welch(k.g.to_numpy(), d.g.to_numpy()); f = k.g.mean() - d.g.mean()
                within.append({"pazar": pazar, "grup": grup, "kova": kv, "n_kucuk": len(k), "n_diger": len(d), "fark": f, "p": p})
                sat.append(f"| {kv} | {len(k)} / {len(d)} | {k.g.mean():+.2f} | {d.g.mean():+.2f} | {f:+.2f} | {p:.3f} | %{100 * (k.getiri > 0).mean():.0f} / %{100 * (d.getiri > 0).mean():.0f} |")
            sat.append("")
        # iki yonlu: kucuk x fiyat, kucuk x likidite (ort getiri)
        for grup, kol in (("fiyat", "fiyat_k"), ("likidite", "lik_k")):
            pv = xo.pivot_table(index="kucuk", columns=kol, values="g", aggfunc="mean")
            nn = xo.pivot_table(index="kucuk", columns=kol, values="g", aggfunc="size")
            sat += [f"### {pazar} — iki yonlu: kucuk mum x {grup} (ort getiri, n)", "", "| kucuk | " + " | ".join(str(c) for c in pv.columns) + " |", "|---|" + "---|" * len(pv.columns)]
            for idx in pv.index:
                sat.append(f"| {'kucuk' if idx == 1 else 'buyuk'} | " + " | ".join(f"{pv.loc[idx, c]:+.1f} (n{int(nn.loc[idx, c])})" if np.isfinite(pv.loc[idx, c]) else "-" for c in pv.columns) + " |")
            sat.append("")
        # iki yonlu: kucuk mum x goreli hacim (RVOL = hacim_alim_kat) — Cemal madde 2
        xo["rvol_k"] = pd.cut(xo.hacim_alim_kat, [-np.inf, 1, 2, 4, np.inf], labels=["<1", "1-2", "2-4", ">=4"], right=False).astype(object)
        sat += [f"### {pazar} — iki yonlu: kucuk mum x RVOL (alim hacmi / obek medyan hacmi): ort getiri (n, kazanan)", "", "| kucuk | <1 | 1-2 | 2-4 | >=4 |", "|---|---|---|---|---|"]
        for idx in (1.0, 0.0):
            hs = []
            for c in ("<1", "1-2", "2-4", ">=4"):
                g = xo[(xo.kucuk == idx) & (xo.rvol_k == c)]
                hs.append(f"{g.g.mean():+.1f} (n{len(g)}, %{100 * (g.getiri > 0).mean():.0f})" if len(g) >= ay.min_n else "-")
            sat.append(f"| {'kucuk' if idx == 1 else 'buyuk'} | " + " | ".join(hs) + " |")
        sat.append("")
    W = pd.DataFrame(within)
    if len(W):
        W.to_csv(os.path.join(cikti, "col_kazanc_dogrulama_within.csv"), index=False)
    # OLS kontrol
    sat += ["### OLS: getiri ~ kucuk + log fiyat + log lik60 + vol20 + w + bekleme + piyasa60 + donem kuklalari (HC0 SE)", "", "| pazar | n | kucuk katsayi | SE | t | kazanan modeli (LPM) kucuk katsayi | t | + log RVOL kontrolu: kucuk | log RVOL katsayisi |", "|---|---|---|---|---|---|---|---|---|"]
    ols_t: Dict[str, float] = {}
    for pazar, dl in donemler_hepsi:
        xo = T[(T.kaynak == "obek") & (T.pazar == pazar)].copy()
        if xo.empty:
            continue
        xo["don"] = "?"
        for ad, b, s_ in dl:
            xo.loc[(xo.sinyal >= b) & (xo.sinyal <= s_), "don"] = ad
        kuk = pd.get_dummies(xo.don, prefix="d", drop_first=True).astype(float)
        X = np.column_stack([xo.kucuk, np.log(xo.fiyat.clip(lower=1e-6)), np.log(xo.lik60.clip(lower=1e-6)), xo.vol20, xo.w, xo.bekleme, xo.piyasa60] + [kuk[c] for c in kuk.columns])
        adlar = ["kucuk", "log_fiyat", "log_lik60", "vol20", "w", "bekleme", "piyasa60"] + list(kuk.columns)
        o1 = _ols(xo.g.to_numpy(float), X, adlar); o2 = _ols((xo.getiri > 0).astype(float).to_numpy(), X, adlar)
        X3 = np.column_stack([X, np.log(xo.hacim_alim_kat.clip(lower=0.05)), xo.alim_ustu_pct]); adlar3 = adlar + ["log_rvol", "alim_ustu_pct"]
        o3 = _ols(xo.g.to_numpy(float), X3, adlar3)                                   # Cemal madde 2: alim gunu goreli hacmi kontrol
        r1 = o1[o1.degisken == "kucuk"].iloc[0]; r2 = o2[o2.degisken == "kucuk"].iloc[0]
        r3 = o3[o3.degisken == "kucuk"].iloc[0]; rv = o3[o3.degisken == "log_rvol"].iloc[0]
        ols_t[pazar] = float(r1.t); ols_t[pazar + "_rvol"] = float(r3.t)
        sat.append(f"| {pazar} | {int(r1.n)} | {r1.katsayi:+.3f} | {r1.se:.3f} | {r1.t:+.2f} | {r2.katsayi:+.4f} | {r2.t:+.2f} | {r3.katsayi:+.3f} (t {r3.t:+.2f}) | {rv.katsayi:+.3f} (t {rv.t:+.2f}) |")
        o3.assign(pazar=pazar, model="getiri+rvol").to_csv(os.path.join(cikti, f"col_kazanc_dogrulama_ols_rvol_{pazar}.csv"), index=False)
        o1.assign(pazar=pazar, model="getiri").to_csv(os.path.join(cikti, f"col_kazanc_dogrulama_ols_{pazar}.csv"), index=False)
    sat.append("")
    sat.append("Okuma: kucuk katsayisi, fiyat/likidite/volatilite/donem kontrolunden sonra |t| >= 2 ile ayni isarette kaliyorsa iz kendi basina; kayboluyorsa proxy.")
    sat.append("Son iki sutun: alim gunu goreli hacmi (RVOL = alim hacmi / obek medyan hacmi) modele girince kucuk katsayisi sifira iniyorsa, kucuk mum dusuk hacmin vekilidir (iz hacimdedir, mum boyunda degil).")
    sat.append("")
    # ---- 3-4. normalizasyon ve desil monotonlugu
    sat += ["## 3-4. Normalizasyon (mum/ATR20) ve desil monotonlugu (obek, pazar havuzu)", ""]
    mono: Dict[str, float] = {}
    for pazar, _ in donemler_hepsi:
        xo = T[(T.kaynak == "obek") & (T.pazar == pazar)]
        if xo.empty:
            continue
        for ad in (olcu, "alim_mum_atr", "govde_atr"):
            v = xo[ad].astype(float)
            try:
                des = pd.qcut(v.rank(method="first"), 10, labels=False)
            except Exception:
                continue
            g = xo.g.groupby(des).agg(["mean", "size", "median"]); g["kazanan"] = xo.getiri.gt(0).groupby(des).mean() * 100
            sinir = v.quantile(np.linspace(0.1, 0.9, 9)).to_numpy()
            rho = _spearman(np.arange(len(g), dtype=float), g["mean"].to_numpy()); mono[f"{pazar}:{ad}"] = rho
            sat += [f"### {pazar} — {ad} desilleri (D1 en kucuk mum). Spearman(desil, ort) = {rho:+.2f}", "",
                    "| desil | ust sinir | n | ort | medyan | kazanan |", "|---|---|---|---|---|---|"]
            for i, r in g.iterrows():
                us = f"<{sinir[int(i)]:.2f}" if int(i) < 9 else f">={sinir[8]:.2f}"
                sat.append(f"| D{int(i) + 1} | {us} | {int(r['size'])} | {r['mean']:+.2f} | {r['median']:+.2f} | %{r['kazanan']:.0f} |")
            sat.append("")
        # ATR esigi: mum/ATR < 1 vs rest, donem bazinda
    sat += ["### ATR normalizasyonu ile esik: alim mumu < 1,0 x ATR20 (donem bazinda, obek)", "", "| donem | n kucuk / diger | fark | p |", "|---|---|---|---|"]
    for pazar, ad, b, s_ in don_list:
        x0 = _don(T[T.kaynak == "obek"], pazar, b, s_)
        k = x0[x0.alim_mum_atr < 1.0]; d = x0[x0.alim_mum_atr >= 1.0]
        if len(k) >= ay.min_n and len(d) >= ay.min_n:
            sat.append(f"| {ad} | {len(k)} / {len(d)} | {k.g.mean() - d.g.mean():+.2f} | {_p_welch(k.g.to_numpy(), d.g.to_numpy()):.3f} |")
    sat.append("")
    # ---- 5. portfoy etkisinin kaynagi
    sat += ["## 5. Portfoy etkisinin kaynagi: sayi mi, secim mi? (obek, donem)", "",
            "| donem | n kucuk / diger | ort kucuk / diger | slot kucuk | slot diger (ayni n, 20 rastgele orneklem ort) | slot hepsi | ort bar kucuk / diger | gunluk es zamanli sinyal kucuk / diger |",
            "|---|---|---|---|---|---|---|---|"]
    rng = np.random.default_rng(42)
    for pazar, ad, b, s_ in don_list:
        x0 = _don(T[T.kaynak == "obek"], pazar, b, s_)
        k = x0[x0.kucuk == 1]; d = x0[x0.kucuk == 0]
        if len(k) < ay.min_n or len(d) < ay.min_n:
            continue
        sk, sa = _slot_fark(CD, k, x0, ay.slot)
        n = min(len(k), len(d))
        sd = float(np.mean([CD._cd_slot(d.sample(n, random_state=int(rng.integers(1e9))).assign(getiri=lambda z: z.g), ay.slot)[0] for _ in range(20)]))
        ez_k = k.groupby("alim").size().mean(); ez_d = d.groupby("alim").size().mean()
        sat.append(f"| {ad} | {len(k)} / {len(d)} | {k.g.mean():+.1f} / {d.g.mean():+.1f} | {sk:+.0f}% | {sd:+.0f}% | {sa:+.0f}% | {k.bar.mean():.0f} / {d.bar.mean():.0f} | {ez_k:.1f} / {ez_d:.1f} |")
    sat.append("")
    sat.append("Okuma: 'slot kucuk' > 'slot diger (ayni n)' ise secim; yalniz n farkindan geliyorsa sayi. Es zamanli sinyal yuksekse slotlar doluyor, islem atlaniyor.")
    sat.append("")
    # 5b. kirilim sonrasi 1-5 gun (Cemal madde 5): kucuk mum -> hemen ardindan yon ve volatilite genislemesi var mi?
    if "ileri5_pct" in T.columns:
        sat += ["### 5b. Alim mumundan sonraki 5 gun: getiri ve volatilite genislemesi (obek; sonuc olcusu)", "",
                "| donem | ileri5 ort kucuk / diger | ileri5 kazanan kucuk / diger | 5g (H-L)/ATR20 medyan kucuk / diger | NATR50 yuzdelik <=10 : n, islem getirisi, ileri5 | NATR50 yuzdelik >10 : islem getirisi |", "|---|---|---|---|---|---|"]
        for pazar, ad, b, s_ in don_list:
            x0 = _don(T[T.kaynak == "obek"], pazar, b, s_)
            k = x0[x0.kucuk == 1]; d = x0[x0.kucuk == 0]
            if len(k) < ay.min_n or len(d) < ay.min_n:
                continue
            nd = x0[x0.natr50_pct <= 10]; nu = x0[x0.natr50_pct > 10]
            on = f"| {ad} | {k.ileri5_pct.mean():+.2f} / {d.ileri5_pct.mean():+.2f} | %{100 * (k.ileri5_pct > 0).mean():.0f} / %{100 * (d.ileri5_pct > 0).mean():.0f} | {k.ileri5_vol_kat.median():.2f} / {d.ileri5_vol_kat.median():.2f} | "
            sat.append(on + (f"{len(nd)}, {nd.g.mean():+.1f}, {nd.ileri5_pct.mean():+.2f} | {nu.g.mean():+.1f} |" if len(nd) >= ay.min_n and len(nu) >= ay.min_n else "- | - |"))
        sat.append("")
        sat.append("Okuma: kucuk mumdan sonra 5 gunde getiri ve vol genislemesi digerinden buyuk degilse 'kucuk mum = hemen ardindan hacimli kirilim' hikayesi veri ile desteklenmiyor.")
        sat.append("")
    # ---- 6. karistiricilar
    sat += ["## 6. Karistiricilar: kucuk mum baska neyle birlikte geliyor? (obek, pazar havuzu)", "", "| pazar | degisken | ort kucuk | ort diger | nokta-biserial r |", "|---|---|---|---|---|"]
    for pazar, _ in donemler_hepsi:
        xo = T[(T.kaynak == "obek") & (T.pazar == pazar)]
        if xo.empty:
            continue
        for ad in ("w", "bekleme", "piyasa60", "ruzgar60", "lik60", "fiyat", "vol20", "atr20_pct", "obek_sira", "alim_ustu_pct", "gap_pct", "hacim_alim_kat", "natr50_pct", "yuv_pct", "konum250"):
            v = xo[ad].astype(float); m = np.isfinite(v) & xo.kucuk.notna()
            if m.sum() < 10:
                continue
            r = float(np.corrcoef(xo.kucuk[m], v[m])[0, 1]) if v[m].std() > 0 else np.nan
            sat.append(f"| {pazar} | {ad} | {v[xo.kucuk == 1].mean():.2f} | {v[xo.kucuk == 0].mean():.2f} | {r:+.2f} |")
        # sektor dagilimi farki
        if "sektor" in xo.columns:
            pk = xo[xo.kucuk == 1].sektor.value_counts(normalize=True); pdg = xo[xo.kucuk == 0].sektor.value_counts(normalize=True)
            fark = (pk.reindex(pk.index.union(pdg.index)).fillna(0) - pdg.reindex(pk.index.union(pdg.index)).fillna(0)).sort_values()
            sat.append(f"| {pazar} | sektor payi farki (kucuk - diger), en buyuk 3 | " + ", ".join(f"{i} {100 * v:+.1f}" for i, v in fark.tail(3).iloc[::-1].items()) + " | en kucuk 3: " + ", ".join(f"{i} {100 * v:+.1f}" for i, v in fark.head(3).items()) + " | |")
    sat.append("")
    # ---- 7. karar
    sat += ["## 7. Karar kurali", ""]
    kriter = []
    if len(W):
        for pazar, _ in donemler_hepsi:
            w = W[W.pazar == pazar]
            if len(w):
                kriter.append(f"{pazar} kova ici arti: {int((w.fark > 0).sum())}/{len(w)} kova (fiyat+likidite+vol+ATR)")
    for pazar, _ in donemler_hepsi:
        t_ = ols_t.get(pazar, np.nan); rho = mono.get(f"{pazar}:{olcu}", np.nan); rho_atr = mono.get(f"{pazar}:alim_mum_atr", np.nan)
        kriter.append(f"{pazar} OLS kucuk t = {t_:+.2f} (RVOL kontrollu t = {ols_t.get(pazar + "_rvol", np.nan):+.2f}); monotonluk Spearman {olcu} {rho:+.2f}, mum/ATR {rho_atr:+.2f}")
    sat += [f"- {k}" for k in kriter]
    gecer_ols = all(ols_t.get(p, 0) >= 2.0 and ols_t.get(p + "_rvol", 0) >= 2.0 for p, _ in donemler_hepsi)
    gecer_mono = all(mono.get(f"{p}:{olcu}", 0) <= -0.5 for p, _ in donemler_hepsi)
    gecer_within = bool(len(W)) and all(((W[W.pazar == p].fark > 0).mean() >= 0.7) for p, _ in donemler_hepsi if len(W[W.pazar == p]))
    karar = "URETIME ADAY (tum kriterler gecti; ABD'de 2025-26 ayrilarak yeniden bakilmali)" if (gecer_ols and gecer_mono and gecer_within) else "ARASTIRILDI, ALINMADI"
    sat += ["", f"Kriter: kova ici arti >= %70 (her pazar) VE OLS t >= 2 hacim kontrolu ile de (her pazar) VE desil monotonlugu Spearman <= -0,5 (her pazar). "
            f"Sonuc: kova ici {'GECTI' if gecer_within else 'GECMEDI'}, OLS {'GECTI' if gecer_ols else 'GECMEDI'}, monotonluk {'GECTI' if gecer_mono else 'GECMEDI'} -> **{karar}**.", ""]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_KAZANC_dogrulama.md"), "w", encoding="utf-8").write(metin)
    cklog.info("K7 dogrulama bitti (%.0f sn)", time.monotonic() - t0)
    return metin



# ------------------------------------------------------------------ K8 birikim: NVI / CMF / A-D ayrismasi (v1.2)
def ck_k8_birikim(ay: CKAyar, T: pd.DataFrame, OB: pd.DataFrame, cikti: str, donemler_hepsi: List[Tuple[str, Tuple]]) -> str:
    """Obek boyunca para akisi (CMF20, NVI, A/D, OBV) -> (A) obekte ayrisma tabandan sik mi, (B) ayrisan obekten sonra alim/bozulma/60g,
    (C) alim sonrasi uretim cikisiyla getiri farki. Rapor COL_KAZANC_birikim.md."""
    t0 = time.monotonic()
    OB = OB.copy(); T = T.copy(); T["g"] = T.getiri.clip(upper=200)
    OB["i60"] = OB.ileri60_pct.clip(upper=200)
    don_list = [(pazar, ad, b, s_) for pazar, dl in donemler_hepsi for ad, b, s_ in dl]
    def _don(x, pazar, b, s_):
        return x[(x.pazar == pazar) & (x.sinyal >= b) & (x.sinyal <= s_)]
    sat = [f"# COL KAZANC — BIRIKIM: NVI / CMF / A-D ayrismasi obekte ne diyor?   ({CK_SURUM}, {pd.Timestamp.now():%Y-%m-%d %H:%M})", "",
           "Soru (Cemal 21 Eki): gunluk OHLCV ile kurumsal birikim izi — fiyat yatay / kucuk mumluyken (obek) NVI ve CMF pozitif ayrisiyor mu, ayrisanlar sonra daha mi iyi?",
           "Olculer obek (s..e) boyunca, obegin son gunu itibariyla (ileriye bakis yok): CMF20 son ve ort; NVI degisimi % ve NVI > EMA255; A/D ve OBV degisimi (obek hacmine bolunmus, %).",
           "AKIS: BIRIKIM = CMF20 > 0,05 VE NVI yukari VE A/D yukari · DAGITIM = ucu de asagi · KARISIK = geri kalan. Taban = obek sarti aranmadan her 5. gunun 15 mumluk kutusu.",
           "Sonuc olculeri: alim (60 gun icinde yesil kapanis > tavan), bozulma (alimdan once dip -%2 alti kapanis), 60 bar ileri kapanis % (%200 kirpili), once +%10 mu -%10 mu, alim sonrasi uretim cikisi getirisi.", ""]
    # ---- A. ayrisma obekte daha mi sik?
    sat += ["## A. Obekte ayrisma tabandan daha mi sik? (pazar havuzu)", "", "| pazar | kaynak | n | birikim % | dagitim % | karisik % | CMF20 son ort | NVI obek % ort | A/D % ort | NVI>EMA255 % | fiyat obek % ort |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for pazar, _ in donemler_hepsi:
        for kay in ("obek", "taban"):
            x = OB[(OB.pazar == pazar) & (OB.kaynak == kay) & (OB.akis != "?")]
            if x.empty:
                continue
            sat.append(f"| {pazar} | {kay} | {len(x)} | %{100 * (x.akis == 'birikim').mean():.1f} | %{100 * (x.akis == 'dagitim').mean():.1f} | %{100 * (x.akis == 'karisik').mean():.1f} | "
                       f"{x.cmf_son.mean():+.3f} | {x.nvi_obek_pct.mean():+.2f} | {x.ad_obek.mean():+.2f} | %{100 * x.nvi_ustu.mean():.0f} | {x.fiyat_obek_pct.mean():+.2f} |")
    sat.append("")
    # ---- B. ayrisma -> alim / bozulma / 60g
    sat += ["## B. Ayrisan obekten sonra ne oluyor? (donem; obek ve TABAN ayri)", "",
            "| donem | kaynak | akis | n | alim % | bozulma % | ileri60 ort | ileri60 kazanan | once +10 % | ileri60 fark vs karisik (p) |", "|---|---|---|---|---|---|---|---|---|---|"]
    kayit_b: List[Dict[str, Any]] = []
    for pazar, ad, b, s_ in don_list:
        for kay in ("obek", "taban"):
            x = _don(OB[(OB.kaynak == kay) & (OB.akis != "?")], pazar, b, s_)
            if len(x) < ay.min_n:
                continue
            ref = x[x.akis == "karisik"]
            for ak in ("birikim", "karisik", "dagitim"):
                g = x[x.akis == ak]
                if len(g) < ay.min_n:
                    continue
                f = g.i60.mean() - ref.i60.mean() if len(ref) >= ay.min_n else np.nan
                p = _p_welch(g.i60.to_numpy(float), ref.i60.to_numpy(float)) if np.isfinite(f) else np.nan
                kayit_b.append({"donem": ad, "kaynak": kay, "akis": ak, "n": len(g), "alim": g.alim.mean(), "bozulma": g.bozulma.mean(), "i60": g.i60.mean(), "fark": f, "p": p})
                sat.append(f"| {ad} | {kay} | {ak} | {len(g)} | %{100 * g.alim.mean():.0f} | %{100 * g.bozulma.mean():.0f} | {g.i60.mean():+.2f} | %{100 * (g.ileri60_pct > 0).mean():.0f} | %{100 * g.once_yukari.mean():.0f} | "
                           + (f"{f:+.2f} ({p:.3f}) |" if np.isfinite(f) else "- |"))
    sat.append("")
    KB = pd.DataFrame(kayit_b)
    if len(KB):
        KB.to_csv(os.path.join(cikti, "col_kazanc_birikim_obek.csv"), index=False)
    # tek olcu kovalari: CMF20 son, NVI ustu, A/D -> alim orani ve ileri60 (obek, donem)
    sat += ["### Tek olcu: CMF20 son / NVI > EMA255 / A-D -> alim orani ve 60 gun ileri (obek, donem)", "",
            "| donem | olcu | kova | n | alim % | bozulma % | ileri60 ort | ileri60 kazanan |", "|---|---|---|---|---|---|---|---|"]
    for pazar, ad, b, s_ in don_list:
        x = _don(OB[OB.kaynak == "obek"], pazar, b, s_)
        if len(x) < ay.min_n:
            continue
        for olcu, kova, et in (("cmf_son", [-np.inf, -0.05, 0.05, np.inf], ["<-0.05", "-0.05-0.05", ">=0.05"]),
                               ("nvi_ustu", [-np.inf, 0.5, np.inf], ["altinda", "ustunde"]),
                               ("ad_obek", [-np.inf, -5, 5, np.inf], ["<-5", "-5-5", ">=5"]),
                               ("nvi_obek_pct", [-np.inf, 0, 2, np.inf], ["<0", "0-2", ">=2"])):
            kv = pd.cut(x[olcu].astype(float), kova, labels=et, right=False).astype(object)
            for k in et:
                g = x[kv == k]
                if len(g) >= ay.min_n:
                    sat.append(f"| {ad} | {olcu} | {k} | {len(g)} | %{100 * g.alim.mean():.0f} | %{100 * g.bozulma.mean():.0f} | {g.i60.mean():+.2f} | %{100 * (g.ileri60_pct > 0).mean():.0f} |")
    sat.append("")
    # ---- C. alim sonrasi getiri (uretim cikisi)
    sat += ["## C. Alim geldikten sonra uretim cikisiyla getiri: akis sinifina gore (obek islemleri; parantez TABAN)", "",
            "| donem | akis | n | ort | kazanan | fark vs donem | p | TABAN fark (p) |", "|---|---|---|---|---|---|---|---|"]
    kayit_c: List[Dict[str, Any]] = []
    for pazar, ad, b, s_ in don_list:
        x = _don(T[T.kaynak == "obek"], pazar, b, s_); tb = _don(T[T.kaynak == "taban"], pazar, b, s_)
        if len(x) < ay.min_n:
            continue
        for ak in ("birikim", "karisik", "dagitim"):
            g = x[x.akis == ak]; r = x[x.akis != ak]
            if len(g) < ay.min_n:
                continue
            f = g.g.mean() - x.g.mean(); p = _p_welch(g.g.to_numpy(float), r.g.to_numpy(float))
            tg = tb[tb.akis == ak]; tr_ = tb[tb.akis != ak]
            tf = tg.g.mean() - tb.g.mean() if len(tg) >= ay.min_n else np.nan
            tp = _p_welch(tg.g.to_numpy(float), tr_.g.to_numpy(float)) if np.isfinite(tf) else np.nan
            kayit_c.append({"donem": ad, "akis": ak, "n": len(g), "ort": g.g.mean(), "fark": f, "p": p, "taban_fark": tf})
            sat.append(f"| {ad} | {ak} | {len(g)} | {g.g.mean():+.2f} | %{100 * (g.getiri > 0).mean():.0f} | {f:+.2f} | {p:.3f} | " + (f"{tf:+.2f} ({tp:.3f}) |" if np.isfinite(tf) else "- |"))
    sat.append("")
    KC = pd.DataFrame(kayit_c)
    if len(KC):
        KC.to_csv(os.path.join(cikti, "col_kazanc_birikim_islem.csv"), index=False)
    sat.append("Not: tek olcu kovalari (cmf_son, cmf_obek, nvi_obek_pct, ad_obek, obv_obek, nvi_ustu, akis) ana taramaya (COL_KAZANC_rapor.md, K4 tutarlilik) da girdi; donem bazinda fark ve taban karsilastirmasi orada.")
    sat.append("")
    # ---- D. karar
    sat += ["## D. Okuma / karar", ""]
    if len(KB):
        bb = KB[(KB.kaynak == "obek") & (KB.akis == "birikim")]; dd = KB[(KB.kaynak == "obek") & (KB.akis == "dagitim")]
        for pazar, dl in donemler_hepsi:
            adlar = [ad for ad, _, _ in dl]
            b2 = bb[bb.donem.isin(adlar)]; d2 = dd[dd.donem.isin(adlar)]
            sat.append(f"- {pazar}: birikim obeklerinde ileri60 farki (vs karisik) {int((b2.fark > 0).sum())}/{len(b2)} donem arti, alim orani {100 * b2.alim.mean():.0f}% (karisik {100 * KB[(KB.kaynak == 'obek') & (KB.akis == 'karisik') & KB.donem.isin(adlar)].alim.mean():.0f}%); "
                       f"dagitim obekleri ileri60 farki {int((d2.fark < 0).sum())}/{len(d2)} donem eksi.")
    if len(KC):
        for pazar, dl in donemler_hepsi:
            adlar = [ad for ad, _, _ in dl]
            c2 = KC[(KC.akis == "birikim") & KC.donem.isin(adlar)]
            sat.append(f"- {pazar}: alim sonrasi birikim sinifi getiri farki {int((c2.fark > 0).sum())}/{len(c2)} donem arti (ort {c2.fark.mean():+.2f} puan); tabanda {int((c2.taban_fark > 0).sum())}/{int(c2.taban_fark.notna().sum())} arti.")
    sat += ["", "Kriter (CLAUDE.md): iz = her donemde ve her iki pazarda ayni yon, tabandan ayrisma, 1,3x. Birikim sinifi hem alim oranini hem ileri60'i hem alim sonrasi getiriyi her donemde yukari cekmiyorsa 'kurumsal birikim OHLCV'den okunmuyor' yazilir.", ""]
    metin = "\n".join(sat) + "\n"
    open(os.path.join(cikti, "COL_KAZANC_birikim.md"), "w", encoding="utf-8").write(metin)
    cklog.info("K8 birikim bitti (%.0f sn)", time.monotonic() - t0)
    return metin


# ------------------------------------------------------------------ calistirici
def _kazanc_pazar(ay: CKAyar, CD, CO, CY, veri: Dict[str, pd.DataFrame], pazar: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    isl, D, obk = ck_k2_islemler(ay, CO, CY, veri)
    T = ck_k3_cikis(ay, CY, isl, D)
    T = ck_k3_piyasa(ay, veri, T, pazar)
    T["pazar"] = pazar
    OB = pd.DataFrame(obk); OB["pazar"] = pazar
    return T, OB


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
    T, OB = _kazanc_pazar(ay, CD, CO, CY, veri, "BIST")
    donemler_hepsi: List[Tuple[str, Tuple]] = [("BIST", ay.donemler)]
    OZ = ck_k4_ozet(ay, CD, T, ay.donemler, "BIST")
    if ay.abd:
        try:
            if veri_abd is None:
                veri_abd = CD.cd_k1_abd(cay)
            Ta, OBa = _kazanc_pazar(ay, CD, CO, CY, veri_abd, "ABD")
            OZa = ck_k4_ozet(ay, CD, Ta, ay.donemler_abd, "ABD")
            T = pd.concat([T, Ta], ignore_index=True); OZ = pd.concat([OZ, OZa], ignore_index=True); OB = pd.concat([OB, OBa], ignore_index=True)
            donemler_hepsi.append(("ABD", ay.donemler_abd))
        except Exception as ex:
            cklog.error("ABD: %s", ex)
    T.to_csv(os.path.join(cikti, "col_kazanc_islemler.csv.gz"), index=False)
    OB.to_csv(os.path.join(cikti, "col_kazanc_obekler.csv.gz"), index=False)
    OZ.to_csv(os.path.join(cikti, "col_kazanc_kova.csv"), index=False)
    R = ck_k4_tutarlilik(ay, OZ)
    R.to_csv(os.path.join(cikti, "col_kazanc_tutarlilik.csv"), index=False)
    B = ck_k5_bilesik(ay, CD, T, R, donemler_hepsi)
    if len(B):
        B.to_csv(os.path.join(cikti, "col_kazanc_bilesik.csv"), index=False)
    metin = ck_k6_rapor(ay, T, OZ, R, B, cikti, donemler_hepsi)
    try:
        dog = ck_k7_dogrula(ay, CD, T, cikti, donemler_hepsi)
    except Exception as ex:
        cklog.error("K7: %s", ex); dog = f"K7 calismadi: {ex}"
    try:
        bir = ck_k8_birikim(ay, T, OB, cikti, donemler_hepsi)
    except Exception as ex:
        cklog.error("K8: %s", ex); bir = f"K8 calismadi: {ex}"
    cklog.info("BITTI %.0f sn -> %s", time.monotonic() - t0, cikti)
    return {"islemler": T, "obekler": OB, "kova": OZ, "tutarlilik": R, "bilesik": B, "rapor": metin, "dogrulama": dog, "birikim": bir, "cikti": cikti}


def col_kazanc_birikim(ay: Optional[CKAyar] = None) -> str:
    """Yalniz K8: kaydedilmis islem + obek dosyalarindan (veri indirmez)."""
    ay = ay or CKAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_kazanc")
    T = pd.read_csv(os.path.join(cikti, "col_kazanc_islemler.csv.gz"), parse_dates=["sinyal", "alim", "giris", "cikis"])
    OB = pd.read_csv(os.path.join(cikti, "col_kazanc_obekler.csv.gz"), parse_dates=["sinyal"])
    donemler_hepsi: List[Tuple[str, Tuple]] = [("BIST", ay.donemler)] + ([("ABD", ay.donemler_abd)] if (OB.pazar == "ABD").any() else [])
    return ck_k8_birikim(ay, T, OB, cikti, donemler_hepsi)


def col_kazanc_dogrula(ay: Optional[CKAyar] = None) -> str:
    """Yalniz K7: mevcut col_kazanc_islemler.csv.gz uzerinden dogrulama (veri indirmez)."""
    ay = ay or CKAyar()
    cikti = ay.cikti or os.path.join(ay.kok, "arastirma_cikti", "col_kazanc")
    CD, _, _ = _ck_mod()
    T = pd.read_csv(os.path.join(cikti, "col_kazanc_islemler.csv.gz"), parse_dates=["sinyal", "alim", "giris", "cikis"])
    for k in ("sinyal", "alim", "giris", "cikis"):
        T[k] = pd.to_datetime(T[k])
    donemler_hepsi: List[Tuple[str, Tuple]] = [("BIST", ay.donemler)] + ([("ABD", ay.donemler_abd)] if (T.pazar == "ABD").any() else [])
    return ck_k7_dogrula(ay, CD, T, cikti, donemler_hepsi)


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
    if len(sys.argv) > 1 and sys.argv[1] == "dogrula":
        print(col_kazanc_dogrula())
    elif len(sys.argv) > 1 and sys.argv[1] == "birikim":
        print(col_kazanc_birikim())
    else:
        R = col_kazanc()
        print(R["rapor"]); print(R["dogrulama"]); print(R["birikim"])
