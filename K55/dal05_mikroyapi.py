"""D05 — Piyasa mikro yapısı, yalnız günlük OHLCV (emir akışı / gün içi veri YOK; vekiller açıkça işaretli). D05-S09 kontrol değişkeni (hücre değil)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .dal_ortak import C_, PENCERE_KISA, PENCERE_ORTA, fitiller, getiri, hacim, islem_degeri, mp, rs
from .hucreler import kaydet


def s01_kapanis_konumu(p: int):
    def f(d):
        _, _, rng = fitiller(d); k = (C_(d) - d.Low.astype(float)) / rng.replace(0, np.nan); return rs(p, k).mean()
    return f


def s02_govde(p: int):
    def f(d):
        _, _, rng = fitiller(d); g = (C_(d) - d.Open.astype(float)) / rng.replace(0, np.nan); return rs(p, g).mean()
    return f


def s03_aralik_orani(p: int):
    def f(d):
        a = (d.High.astype(float) - d.Low.astype(float)) / C_(d); return np.log(rs(p, a).mean() / rs(120, a).mean())
    return f


def s04_orta_ustu_payi(p: int):
    def f(d):
        ust = (C_(d) > (d.High.astype(float) + d.Low.astype(float)) / 2).astype(float); return rs(p, ust).mean()
    return f


def s05_bosluk_net(p: int):
    def f(d):
        O = d.Open.astype(float); C = C_(d); g = O / C.shift(1) - 1; yuk = (g > 0.02).astype(float); asa = (g < -0.02).astype(float); return rs(p, yuk - asa).sum()
    return f


def s06_fiyat_etkisi(d: pd.DataFrame, w: int = 60) -> pd.Series:
    a = getiri(d).abs(); ld = np.log(islem_degeri(d).replace(0, np.nan)); cov = rs(w, a).cov(ld); var = rs(w, ld).var(ddof=0); return cov / var.replace(0, np.nan)


def s07_hacimli_gun_devam(p: int):
    def f(d):
        V = hacim(d); med = rs(20, V.shift(1)).median(); r = getiri(d); ol = (V > 1.5 * med); dev = (np.sign(r) * np.sign(r.shift(-1)))  # yüksek hacimli gün: > 1,5 × 20 gün medyan; ertesi gün çifti bir gün kaydırılır
        dev = dev.shift(1).where(ol.shift(1).fillna(False)); return dev.rolling(p, min_periods=3).mean()                                               # t günü: t−1'e kadar bilinen çiftler
    return f


def s08_isaretli_hacim_payi(p: int):
    def f(d):
        V = hacim(d); s = np.sign(C_(d) - d.Open.astype(float)); return rs(p, V * s).sum() / rs(p, V).sum().replace(0, np.nan)
    return f


def s10_gun_ici_donus_payi(p: int):
    def f(d):
        O = d.Open.astype(float); C = C_(d); donus = (np.sign(O - C.shift(1)) * np.sign(C - O) < 0).astype(float); return rs(p, donus).mean()
    return f


def kaydet_hucreler() -> None:
    kaydet("D05-S01", "D05", "Kapanış gün içi nerede? ((C−L)/(H−L), p gün ortalama)", +1, fabrika=s01_kapanis_konumu, pencereler=PENCERE_KISA)
    kaydet("D05-S02", "D05", "Gövde yönü ve payı ((C−O)/(H−L), p gün)", +1, fabrika=s02_govde, pencereler=PENCERE_KISA)
    kaydet("D05-S03", "D05", "Gün içi aralık (p / 120 gün)", -1, fabrika=s03_aralik_orani, pencereler=PENCERE_KISA, not_="K51 imza aralık tabanlı; oran")
    kaydet("D05-S04", "D05", "Kapanışa doğru davranış VEKİLİ (C > (H+L)/2 günlerin payı, p gün)", +1, fabrika=s04_orta_ustu_payi, pencereler=PENCERE_KISA, not_="VEKİL (gün içi veri yok)")
    kaydet("D05-S05", "D05", "Boşluklar (p günde yukarı − aşağı %2 açılış boşluğu sayısı)", +1, fabrika=s05_bosluk_net, pencereler=PENCERE_ORTA)
    kaydet("D05-S06", "D05", "Fiyat etkisi VEKİLİ (60 gün |getiri| ~ log işlem değeri eğimi; Kyle λ benzeri)", -1, fonk=s06_fiyat_etkisi, not_="VEKİL; D02-S03 ile korelasyon denetimi")
    kaydet("D05-S07", "D05", "Yüksek hacimli güne (> 1,5 × medyan) ertesi gün tepki (devam = +1; p gün ortalama, bir gün gecikmeli)", +1, fabrika=s07_hacimli_gun_devam, pencereler=PENCERE_ORTA)
    kaydet("D05-S08", "D05", "Alış–satış dengesizliği VEKİLİ (işaretli hacim payı, p gün)", +1, fabrika=s08_isaretli_hacim_payi, pencereler=PENCERE_KISA, not_="VEKİL; OBV vekil denetimi")
    kaydet("D05-S10", "D05", "Gün içi tersine dönüş payı (açılış yönü ≠ kapanış yönü, p gün)", +1, fabrika=s10_gun_ici_donus_payi, pencereler=PENCERE_KISA)
