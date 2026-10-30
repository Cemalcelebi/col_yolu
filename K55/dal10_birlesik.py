"""D10 — Değişkenlerin birlikte davranışı (K55_PLAN D10-S01 … S10). Korelasyon değil; sıra, gecikme, birlikte oluşma, koşullu etki.
Kesitsel bileşikler panel fonksiyonu olarak (A ve B; C uygulanmaz): x = min(gün içi yüzdelik(x1), gün içi yüzdelik(x2)) (iki koşul birlikte yüksek).
Bileşenler öteki dalların hücre sütunlarından alınır (faz1 önce D01-D06'yı hesaplar). D10-S05 (temel) ve S07 (içeriden alım) Faz 2 verisi ister;
D10-S06 = D04-S09 aynı değişken; D10-S08 dallanma şablonunda (koşullu etki: KEŞİF hücreleri × likidite / büyüklük) — burada hücre değil."""
from __future__ import annotations

from typing import Callable, Dict, List

import numpy as np
import pandas as pd

from .dal_ortak import C_, EK, PENCERE_ORTA, aralik, fitiller, getiri, hacim, hizala, mp, rs, sektor_adi
from .hucreler import kaydet


def _pct(P: pd.DataFrame, kol: str, isaret: int = 1) -> pd.Series:
    """Likit satırlarda gün içi yüzdelik (isaret −1: ters)."""
    x = P[kol] * isaret; q = x.where(P.likit).groupby(P.tarih).rank(pct=True); return q


def birlesik(kollar: List[tuple]):
    """kollar: [(sütun, işaret), …] -> x = min(yüzdelik_i)."""
    def f(P: pd.DataFrame) -> pd.Series:
        qs = [_pct(P, k, s) for k, s in kollar if k in P]
        if len(qs) < len(kollar):
            return pd.Series(np.nan, index=P.index)
        return pd.concat(qs, axis=1).min(axis=1)
    return f


def s01_fiyat_duserken_hacim(P: pd.DataFrame) -> pd.Series:
    r20 = P.close / P.groupby("sembol").close.shift(20) - 1; P2 = P.assign(_r20=r20); return birlesik([("_r20", -1), ("D02-S02", -1)])(P2)


def s02_vol_duserken_rs(P: pd.DataFrame) -> pd.Series:
    return birlesik([("D03-S01", -1), ("D06-S01", 1)])(P)


def s03_piyasa_duserken_yatay(P: pd.DataFrame) -> pd.Series:
    return birlesik([("D06-S02", 1), ("D01-S06", 1)])(P)


def s04_hareketsizlik_hacim_yapisi(P: pd.DataFrame) -> pd.Series:
    g = P["D02-S05"]; dg = g - g.groupby(P.sembol).shift(20); P2 = P.assign(_dg=dg); return birlesik([("D04-S08", 1), ("_dg", -1)])(P2)


def s09_lider_takipci(d: pd.DataFrame) -> pd.Series:
    """Sektör liderlerinin (işlem değeri üst üçte bir, önceki yıl) 20 gün getirisi; hissenin kendi 20 gün getirisi çıkarılmış (lider önde mi)."""
    lg = EK.get("lider_getiri", {}); s = sektor_adi(d); L = hizala(lg.get(s), d.index) if (s and s in lg) else pd.Series(np.nan, index=d.index)
    return rs(20, np.log1p(L)).sum() - rs(20, np.log1p(getiri(d))).sum()


def s10_cok_degiskenli_sapma(d: pd.DataFrame, w: int = 250) -> pd.Series:
    """D01-D06 türü 8 temel ölçünün (aralık20, vol20, alt fitil20, aşağı hacim payı20, kapanış konumu20, 20 gün getiri, hacim20 / hacim120, |getiri| otokor20)
    hissenin kendi w gün geçmişine göre standartlaştırılmış uzaklığı (köşegen Mahalanobis); makine öğrenmesi değil, anomali."""
    r = getiri(d); V = hacim(d); ust, alt, rng = fitiller(d); C = C_(d)
    oz = pd.concat([rs(20, aralik(d)).median(), rs(20, r).std(ddof=0), rs(20, alt / rng.replace(0, np.nan)).mean(), rs(20, V.where(r < 0, 0.0)).sum() / rs(20, V).sum().replace(0, np.nan),
                    rs(20, (C - d.Low.astype(float)) / rng.replace(0, np.nan)).mean(), C / C.shift(20) - 1, rs(20, V).mean() / rs(120, V).mean().replace(0, np.nan), rs(20, r.abs()).corr(r.abs().shift(1))], axis=1)
    mu = oz.shift(1).rolling(w, min_periods=w // 2).mean(); sd = oz.shift(1).rolling(w, min_periods=w // 2).std(ddof=0)
    z = (oz - mu) / sd.replace(0, np.nan); return np.sqrt((z ** 2).sum(axis=1, min_count=4) / z.notna().sum(axis=1).replace(0, np.nan))


def kaydet_hucreler() -> None:
    kaydet("D10-S01", "D10", "Fiyat düşerken hacim farklı (r20 düşük VE aşağı gün hacim payı düşük)", +1, panel_fonk=s01_fiyat_duserken_hacim, yontemler=("A", "B"), not_="kesitsel bileşik; D02-S02 (20) gerekli")
    kaydet("D10-S02", "D10", "Vol düşerken göreli güç yükseliyor (D03-S01 düşük VE D06-S01 yüksek)", +1, panel_fonk=s02_vol_duserken_rs, yontemler=("A", "B"), not_="kesitsel bileşik")
    kaydet("D10-S03", "D10", "Piyasa düşerken hisse yatay (D06-S02 yüksek VE dar alan süresi uzun)", +1, panel_fonk=s03_piyasa_duserken_yatay, yontemler=("A", "B"), not_="kesitsel bileşik")
    kaydet("D10-S04", "D10", "Uzun hareketsizlik + hacim yapısı değişimi (D04-S08 uzun VE Gini 20 gün düşüşü)", +1, panel_fonk=s04_hareketsizlik_hacim_yapisi, yontemler=("A", "B"), not_="kesitsel bileşik")
    kaydet("D10-S09", "D10", "Lider–takipçi gecikmesi (sektör liderleri 20 gün getirisi − hisse 20 gün getirisi)", +1, fonk=s09_lider_takipci, not_="liderler: önceki yıl işlem değeri üst üçte bir (Ç111 hisse düzeyi)")
    kaydet("D10-S10", "D10", "Çok değişkenli sapma (8 temel ölçünün kendi 250 gün geçmişine köşegen Mahalanobis uzaklığı)", +1, fonk=s10_cok_degiskenli_sapma, not_="makine öğrenmesi değil; anomali")
