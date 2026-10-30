"""D01 — Fiyat davranışı (K55_PLAN bölüm 4, D01-S01 … S10). Klasik gösterge yok; ham fiyat davranışından ölçüler. Hepsi geriye bakar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, PENCERE_KISA, PENCERE_ORTA, aralik, egim, fitiller, getiri, kayan_uygula, log_getiri, mp, rs, run_uzunlugu
from .hucreler import HUCRELER, d01_s01_dip_band_gun, kaydet


def s02_dusus_ivmesi(p: int):
    def f(d):
        lc = np.log(C_(d)); return egim(lc, p) - egim(lc.shift(p), p)          # son p gün eğimi − önceki p gün eğimi (düşüş yavaşlıyorsa > 0)
    return f


def s03_dip_testi(d: pd.DataFrame, w: int = 120, bant: float = 0.02) -> pd.Series:
    L = d.Low.astype(float); C = C_(d); dip = rs(w, L).min()
    test = ((L <= dip * (1 + bant)) & (C > dip)).astype(float); test[dip.isna()] = np.nan
    return rs(w, test).sum()


def s04_fitil_orani(p: int):
    def f(d):
        ust, alt, _ = fitiller(d); return rs(p, alt).sum() / rs(p, ust).sum().replace(0, np.nan)
    return f


def s05_getiri_asimetrisi(p: int):
    def f(d):
        r = getiri(d); return rs(p, r).skew()
    return f


def s06_dar_alan_suresi(d: pd.DataFrame) -> pd.Series:
    ar20 = rs(20, aralik(d)).median(); esik = rs(250, ar20).quantile(0.10)
    return run_uzunlugu((ar20 <= esik).where(esik.notna()))


def s07_mum_dizisi_entropi(p: int):
    def ent(a):
        u = np.mean(a > 0); return float(-(u * np.log2(u) + (1 - u) * np.log2(1 - u))) if 0 < u < 1 else 0.0
    def f(d):
        r = getiri(d); return kayan_uygula(r, p, ent)
    return f


def s08_sert_dusus_tepkisi(p: int):
    def f(d):
        C = C_(d).to_numpy(float); r = np.r_[np.nan, C[1:] / C[:-1] - 1]; out = np.full(len(C), np.nan)
        for i in range(p, len(C)):
            w = r[i - p + 1: i + 1]; j = int(np.nanargmin(w)) + i - p + 1
            if np.isfinite(r[j]) and r[j] < 0 and j >= 1:
                dus = C[j - 1] - C[j]; out[i] = (C[i] - C[j]) / dus if dus > 0 else np.nan          # düşüşün geri alınan payı (1 = tamamı)
        return pd.Series(out, index=d.index)
    return f


def s09_direnc_asinmasi(p: int):
    def f(d):
        H = d.High.astype(float); tepe = rs(p, H.shift(1)).max(); yakin = (H >= tepe * 0.97).astype(float); yakin[tepe.isna()] = np.nan
        return rs(p, yakin).sum()
    return f


def s10_ks_uzakligi(p: int, ref: int = 120):
    def f(d):
        r = log_getiri(d).to_numpy(float); n = len(r); out = np.full(n, np.nan)
        for i in range(p + ref, n):
            a = r[i - p + 1: i + 1]; b = r[i - p - ref + 1: i - p + 1]; a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
            if len(a) >= mp(p) and len(b) >= ref // 2:
                hep = np.sort(np.concatenate([a, b])); fa = np.searchsorted(np.sort(a), hep, side="right") / len(a); fb = np.searchsorted(np.sort(b), hep, side="right") / len(b)
                out[i] = float(np.max(np.abs(fa - fb)))
        return pd.Series(out, index=d.index)
    return f


def kaydet_hucreler() -> None:
    if "D01-S01" not in HUCRELER:
        kaydet("D01-S01", "D01", "Dip ne kadar sürede oluştu? (250 günde dip bandında geçirilen gün)", +1, d01_s01_dip_band_gun)
    kaydet("D01-S02", "D01", "Düşüş hızı değişiyor mu? (son p gün eğimi − önceki p gün eğimi)", +1, fabrika=s02_dusus_ivmesi, pencereler=PENCERE_KISA)
    kaydet("D01-S03", "D01", "Dip kaç kez test edilip savunuldu? (120 gün)", +1, fonk=s03_dip_testi)
    kaydet("D01-S04", "D01", "Alt fitiller büyüyor mu? (p gün alt / üst fitil)", +1, fabrika=s04_fitil_orani, pencereler=PENCERE_KISA)
    kaydet("D01-S05", "D01", "Getiri asimetrisi (p gün çarpıklık)", +1, fabrika=s05_getiri_asimetrisi, pencereler=PENCERE_ORTA)
    kaydet("D01-S06", "D01", "Dar alanda kalma süresi (20 gün aralığı 250 gün en düşük %10'unda ardışık gün)", +1, fonk=s06_dar_alan_suresi, not_="K51 imza ile vekil denetimi")
    kaydet("D01-S07", "D01", "Mum dizisinin düzeni (p gün yön dizisi entropisi; düşük = düzenli)", -1, fabrika=s07_mum_dizisi_entropi, pencereler=PENCERE_KISA)
    kaydet("D01-S08", "D01", "Son sert düşüşün geri alınan payı (p gün)", +1, fabrika=s08_sert_dusus_tepkisi, pencereler=PENCERE_ORTA)
    kaydet("D01-S09", "D01", "Direnç aşınması: p gün tepesine %3 yaklaşma sayısı", +1, fabrika=s09_direnc_asinmasi, pencereler=PENCERE_ORTA)
    kaydet("D01-S10", "D01", "Hisse kendi normalinden saptı mı? (son p gün getirisi vs önceki 120 gün, KS)", +1, fabrika=s10_ks_uzakligi, pencereler=PENCERE_ORTA)
