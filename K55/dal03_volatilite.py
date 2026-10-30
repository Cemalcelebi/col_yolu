"""D03 — Volatilite ve risk rejimi (K55_PLAN D03-S01 … S10). Bollinger kullanılmaz; D03-S07 (VIX) KAPALI, kaydedilmez. Hepsi geriye bakar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, PENCERE_KISA, PENCERE_ORTA, aralik, getiri, mp, rs, run_uzunlugu
from .hucreler import kaydet


def _vol(d, w):
    return rs(w, getiri(d)).std(ddof=0)


def s01_vol_orani(p: int):
    def f(d):
        return _vol(d, p) / _vol(d, 250).replace(0, np.nan)
    return f


def s02_yari_varyans_orani(p: int):
    def f(d):
        r = getiri(d); asagi = rs(p, (r.clip(upper=0)) ** 2).mean(); yukari = rs(p, (r.clip(lower=0)) ** 2).mean(); return asagi / yukari.replace(0, np.nan)
    return f


def s03_mutlak_getiri_otokor(p: int):
    def f(d):
        a = getiri(d).abs(); return rs(p, a).corr(a.shift(1))
    return f


def s04_daralma_hizi(d: pd.DataFrame) -> pd.Series:
    v20 = _vol(d, 20); return run_uzunlugu((v20 < v20.shift(1)).where(v20.notna() & v20.shift(1).notna()))


def s05_vol_fiyat_onculuk(d: pd.DataFrame, w: int = 60, g: int = 5) -> pd.Series:
    ar = aralik(d); a = getiri(d).abs(); return rs(w, ar.shift(g)).corr(a) - rs(w, ar).corr(a.shift(g))     # aralık değişimi |getiri|den önce mi


def s06_verimlilik(p: int):
    def f(d):
        H = d.High.astype(float); L = d.Low.astype(float); C = C_(d); tr = pd.concat([H - L, (H - C.shift(1)).abs(), (L - C.shift(1)).abs()], axis=1).max(axis=1)
        net = (C - C.shift(p)).abs(); return rs(p, tr).sum() / net.replace(0, np.nan)                        # yol / net hareket (büyük = verimsiz)
    return f


def s08_bosluk_vol_katkisi(p: int):
    def f(d):
        O = d.Open.astype(float); C = C_(d); g = np.log(O / C.shift(1)); r = np.log(C / C.shift(1)); return rs(p, g).var(ddof=0) / rs(p, r).var(ddof=0).replace(0, np.nan)
    return f


def s09_uzun_dusuk_vol(d: pd.DataFrame) -> pd.Series:
    v20 = _vol(d, 20); yuzde = v20.rolling(250, min_periods=125).apply(lambda a: (a[:-1] < a[-1]).mean() if len(a) > 1 else np.nan, raw=True)
    return run_uzunlugu((yuzde < 0.10).where(yuzde.notna()))


def s10_asagi_vol_degisimi(d: pd.DataFrame) -> pd.Series:
    r = getiri(d); a60 = rs(60, (r.clip(upper=0)) ** 2).mean(); a120 = rs(120, (r.clip(upper=0)) ** 2).mean(); return a60 / a120.replace(0, np.nan)


def kaydet_hucreler() -> None:
    kaydet("D03-S01", "D03", "Kısa vol uzun vole göre nerede? (vol p / vol 250)", -1, fabrika=s01_vol_orani, pencereler=PENCERE_KISA, not_="vol60 K51 kontrolü; oran yeni; BB kullanılmaz")
    kaydet("D03-S02", "D03", "Aşağı / yukarı yarı-varyans oranı (p gün; düşük = aşağı sakin)", -1, fabrika=s02_yari_varyans_orani, pencereler=PENCERE_ORTA)
    kaydet("D03-S03", "D03", "Vol kümelenmesi (|getiri| 1. gecikme otokorelasyonu, p gün)", +1, fabrika=s03_mutlak_getiri_otokor, pencereler=(40, 60))
    kaydet("D03-S04", "D03", "Daralma hızı (vol20 ardışık kaç gündür düşüyor)", +1, fonk=s04_daralma_hizi)
    kaydet("D03-S05", "D03", "Aralık değişimi |getiri|den önce mi? (60 gün, ±5 gün öncü-gecikme farkı)", +1, fonk=s05_vol_fiyat_onculuk, yontemler=("A", "C"))
    kaydet("D03-S06", "D03", "Hareket verimliliği (p gün gerçek aralık toplamı / net hareket; düşük = verimli)", -1, fabrika=s06_verimlilik, pencereler=PENCERE_KISA)
    kaydet("D03-S08", "D03", "Boşluk volatilitesi payı (p gün açılış boşluğu varyansı / kapanış varyansı)", +1, fabrika=s08_bosluk_vol_katkisi, pencereler=PENCERE_ORTA)
    kaydet("D03-S09", "D03", "Uzun düşük vol süresi (vol20 250 gün yüzdeliği < 10 ardışık gün)", +1, fonk=s09_uzun_dusuk_vol)
    kaydet("D03-S10", "D03", "Aşağı vol zamanla azalıyor mu? (aşağı yarı-varyans 60 / 120)", -1, fonk=s10_asagi_vol_degisimi)
