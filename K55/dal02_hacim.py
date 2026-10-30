"""D02 — Hacim ve işlem akışı (K55_PLAN D02-S01 … S10). CMF / OBV / MFI yeniden adlandırılmaz; vekil denetimi 2.7. Hepsi geriye bakar."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, PENCERE_KISA, PENCERE_ORTA, getiri, gini, hacim, islem_degeri, kayan_uygula, mp, rs, z_skor
from .hucreler import kaydet


def s01_hacim_onculugu(p: int):
    def f(d):
        V = hacim(d); C = C_(d); oran = np.log(rs(p, V).mean() / rs(120, V).mean().replace(0, np.nan)); rp = (C / C.shift(p) - 1).abs()
        return oran / (1 + rp / 0.03)                                       # hacim değişimi, fiyat hareketi büyüdükçe cezalanır (fiyattan önce hacim)
    return f


def s02_asagi_gun_hacim_payi(p: int):
    def f(d):
        V = hacim(d); r = getiri(d); asagi = V.where(r < 0, 0.0); return rs(p, asagi).sum() / rs(p, V).sum().replace(0, np.nan)
    return f


def s03_amihud_degisimi(p: int):
    def f(d):
        am = getiri(d).abs() / islem_degeri(d).replace(0, np.nan); return np.log(rs(p, am).mean() / rs(120, am).mean())
    return f


def s04_yukari_asagi_medyan_hacim(p: int):
    def f(d):
        V = hacim(d); r = getiri(d); q = max(2, p // 4); return V.where(r > 0).rolling(p, min_periods=q).median() / V.where(r < 0).rolling(p, min_periods=q).median().replace(0, np.nan)
    return f


def s05_hacim_gini(p: int):
    def f(d):
        return kayan_uygula(hacim(d), p, gini)
    return f


def s06_olagan_disi_hacim_kumesi(p: int):
    def f(d):
        V = hacim(d); med = rs(20, V.shift(1)).median(); ol = (V > 2 * med).astype(float); ol[med.isna()] = np.nan; return rs(p, ol).sum()
    return f


def s07_emilim(p: int):
    def f(d):
        V = hacim(d); C = C_(d); z = (rs(p, V).mean() - rs(120, V.shift(1)).mean()) / rs(120, V.shift(1)).std(ddof=0).replace(0, np.nan)
        rp = (C / C.shift(p) - 1).abs(); return z / (1 + rp / 0.03)       # hacim artıyor, fiyat ilerlemiyor
    return f


def s08_satici_tukenmesi(p: int):
    def f(d):
        V = hacim(d); C = C_(d); z = (rs(p, V).mean() - rs(120, V.shift(1)).mean()) / rs(120, V.shift(1)).std(ddof=0).replace(0, np.nan)
        rp = C / C.shift(p) - 1; sd = rs(120, getiri(d)).std(ddof=0) * np.sqrt(p); return -z + rp.clip(upper=0) / sd.replace(0, np.nan)   # hacim azalıyor, fiyat düşmüyor
    return f


def s09_hacim_vol_korelasyonu(p: int):
    def f(d):
        V = hacim(d); a = getiri(d).abs(); return rs(p, a).corr(V) - rs(120, a).corr(V)
    return f


def s10_islem_degeri_yuzdelik_degisimi(p: int):
    """Kesitsel: işlem değeri (20 gün medyan) evren içi yüzdeliğinin p gün değişimi (panel fonksiyonu)."""
    def f(P: pd.DataFrame) -> pd.Series:
        L = P.likit; q = P.loc[L].groupby("tarih").dv20.rank(pct=True); q = q.reindex(P.index)
        once = q.groupby(P.sembol).shift(p); return q - once
    return f


def kaydet_hucreler() -> None:
    kaydet("D02-S01", "D02", "Hacim fiyattan önce mi değişiyor? (p / 120 gün hacim oranı, fiyat hareketi cezalı)", +1, fabrika=s01_hacim_onculugu, pencereler=PENCERE_KISA)
    kaydet("D02-S02", "D02", "Aşağı günlerin hacim payı (p gün; düşük = satıcı zayıf)", -1, fabrika=s02_asagi_gun_hacim_payi, pencereler=PENCERE_KISA, not_="OBV / CMF vekil denetimi")
    kaydet("D02-S03", "D02", "Aynı hacme fiyat tepkisi değişiyor mu? (Amihud p / 120)", -1, fabrika=s03_amihud_degisimi, pencereler=PENCERE_KISA, not_="bilinen ölçü (Amihud), değişimi")
    kaydet("D02-S04", "D02", "Yukarı / aşağı gün medyan hacim oranı (p gün)", +1, fabrika=s04_yukari_asagi_medyan_hacim, pencereler=PENCERE_ORTA)
    kaydet("D02-S05", "D02", "Hacim zamana nasıl yayılmış? (p gün Gini; düşük = yayılmış)", -1, fabrika=s05_hacim_gini, pencereler=PENCERE_ORTA)
    kaydet("D02-S06", "D02", "Olağan dışı hacim günleri sayısı (p gün; > 2 × 20 gün medyan)", +1, fabrika=s06_olagan_disi_hacim_kumesi, pencereler=PENCERE_KISA)
    kaydet("D02-S07", "D02", "Emilim: hacim artıyor, fiyat ilerlemiyor (p gün)", +1, fabrika=s07_emilim, pencereler=PENCERE_KISA)
    kaydet("D02-S08", "D02", "Satıcı tükenmesi: hacim azalıyor, fiyat düşmüyor (p gün)", +1, fabrika=s08_satici_tukenmesi, pencereler=PENCERE_KISA, not_="K51 H-C hacim kuruması ile kısmen çakışır (koşullu biçim yeni)")
    kaydet("D02-S09", "D02", "Hacim–oynaklık bağı değişimi (p gün − 120 gün korelasyon)", +1, fabrika=s09_hacim_vol_korelasyonu, pencereler=PENCERE_ORTA)
    kaydet("D02-S10", "D02", "Evren içinde ilgi artıyor mu? (işlem değeri yüzdeliğinin p gün değişimi; kesitsel)", +1, panel_fonk=s10_islem_degeri_yuzdelik_degisimi(20), fabrika=s10_islem_degeri_yuzdelik_degisimi, pencereler=PENCERE_ORTA, yontemler=("A", "B"), not_="kesitsel bileşik: C uygulanmaz")
