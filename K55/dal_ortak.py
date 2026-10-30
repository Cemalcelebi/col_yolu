"""K55 dal modülleri için ortak yardımcılar: güvenli kayan pencereler, getiri, fitil ölçüleri, ek veriler (SPY, IWM, sektör sepetleri) ve
kesitsel panel yardımcıları. Bütün fonksiyonlar yalnız o gün ve öncesine bakar (kesme testi her hücrede zorunlu).
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

import numpy as np
import pandas as pd

EK: Dict[str, Any] = {}        # faz1.ek_kur ile doldurulur: "SPY", "IWM" (Close Series), "sektor_getiri" (sektör -> günlük getiri Series), "lider_getiri", "sektor_of"
PENCERE_KISA = (5, 10, 20, 40, 60)
PENCERE_ORTA = (20, 40, 60)


def mp(w: int) -> int:
    return max(2, w // 2)


def C_(d: pd.DataFrame) -> pd.Series:
    return d.Close.astype(float)


def getiri(d: pd.DataFrame) -> pd.Series:
    return C_(d).pct_change(fill_method=None)


def log_getiri(d: pd.DataFrame) -> pd.Series:
    C = C_(d); return np.log(C / C.shift(1))


def aralik(d: pd.DataFrame) -> pd.Series:
    """Gün aralığı (H−L) / önceki kapanış (Cemal'in 'küçük mum'u: fitiller dahil)."""
    return (d.High.astype(float) - d.Low.astype(float)).clip(lower=0) / C_(d).shift(1)


def fitiller(d: pd.DataFrame):
    O = d.Open.astype(float); H = d.High.astype(float); L = d.Low.astype(float); C = d.Close.astype(float); rng = (H - L).clip(lower=0)
    ust = (H - np.maximum(O, C)).clip(lower=0); alt = (np.minimum(O, C) - L).clip(lower=0)
    return ust, alt, rng


def hacim(d: pd.DataFrame) -> pd.Series:
    return d.Volume.astype(float).clip(lower=0)


def islem_degeri(d: pd.DataFrame) -> pd.Series:
    return C_(d) * hacim(d)


def rs(w: int, x: pd.Series) -> pd.Series:
    return x.rolling(w, min_periods=mp(w))


def egim(logC: pd.Series, w: int) -> pd.Series:
    """w günlük ortalama günlük log eğim."""
    return (logC - logC.shift(w)) / w


def z_skor(x: pd.Series, w: int) -> pd.Series:
    mu = rs(w, x.shift(1)).mean(); sd = rs(w, x.shift(1)).std(ddof=0)
    return (x - mu) / sd.replace(0, np.nan)


def run_uzunlugu(bayrak: pd.Series) -> pd.Series:
    """True bayrağının ardışık gün sayısı (o gün dahil); False -> 0; NaN -> NaN."""
    b = bayrak.astype(float); out = np.full(len(b), np.nan); say = 0.0
    v = b.to_numpy()
    for i in range(len(v)):
        if np.isnan(v[i]):
            say = 0.0; out[i] = np.nan
        elif v[i] > 0:
            say += 1; out[i] = say
        else:
            say = 0.0; out[i] = 0.0
    return pd.Series(out, index=bayrak.index)


def gun_once(bayrak: pd.Series) -> pd.Series:
    """Son True'dan bu yana geçen gün (o gün True ise 0; hiç yoksa NaN)."""
    v = bayrak.fillna(False).to_numpy(bool); out = np.full(len(v), np.nan); son = -1
    for i in range(len(v)):
        if v[i]:
            son = i
        out[i] = (i - son) if son >= 0 else np.nan
    return pd.Series(out, index=bayrak.index)


def gini(x: np.ndarray) -> float:
    x = np.sort(np.asarray(x, float)); x = x[np.isfinite(x)]
    if len(x) < 2 or x.sum() <= 0:
        return np.nan
    n = len(x); return float((2 * np.sum((np.arange(1, n + 1)) * x) / (n * x.sum())) - (n + 1) / n)


def kayan_uygula(x: pd.Series, w: int, f: Callable[[np.ndarray], float]) -> pd.Series:
    """Saf python kayan uygulama (gini, entropi gibi); min_periods = w // 2."""
    v = x.to_numpy(float); out = np.full(len(v), np.nan)
    for i in range(len(v)):
        a = v[max(0, i - w + 1): i + 1]
        if len(a) >= mp(w):
            out[i] = f(a)
    return pd.Series(out, index=x.index)


def hizala(seri: Optional[pd.Series], idx: pd.Index) -> pd.Series:
    """Ek seriyi (SPY, sektör) hissenin tarihlerine hizalar (ileri doldurma yok: eksik gün NaN)."""
    if seri is None:
        return pd.Series(np.nan, index=idx)
    s = seri.copy(); s.index = pd.DatetimeIndex(s.index).normalize(); return s.reindex(pd.DatetimeIndex(idx).normalize()).set_axis(idx)


def sektor_adi(d: pd.DataFrame) -> Optional[str]:
    """Hissenin sektörü (faz1 ek_kur hisse tablolarına 'sektor' attr'ı yazar; yoksa None)."""
    return d.attrs.get("sektor") if hasattr(d, "attrs") else None
