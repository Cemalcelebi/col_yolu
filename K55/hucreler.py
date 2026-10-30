"""K55 hücre kayıt defteri: kimlik -> {dal, soru, yon, pencereli, fonk}. Değişken fonksiyonu OHLCV tablosu alır, aynı uzunlukta Series döndürür ve
YALNIZ o gün ve öncesine bakar (sizinti.kesme_testi ile zorunlu doğrulama). Tanım sonradan değişmez; yeni tanım = yeni kimlik (ör. D01-S01b).

Faz 0: yalnız D01-S01 (pipeline iskelesi) + sızıntı kontrol değişkenleri (sizinti.py). Faz 1'de dal modülleri (dal01_fiyat.py …) buraya kaydolur.
"""
from __future__ import annotations

from typing import Any, Callable, Dict

import numpy as np
import pandas as pd

HUCRELER: Dict[str, Dict[str, Any]] = {}


def kaydet(kimlik: str, dal: str, soru: str, yon: int, fonk: Callable[[pd.DataFrame], pd.Series], pencereli: bool = False) -> None:
    if kimlik in HUCRELER:
        raise KeyError(f"hücre kimliği zaten kayıtlı (tanım değişmez; yeni kimlik aç): {kimlik}")
    HUCRELER[kimlik] = {"dal": dal, "soru": soru, "yon": yon, "fonk": fonk, "pencereli": pencereli}


# ---------------------------------------------------------------- D01-S01 (Faz 0 iskelesi; dal01_fiyat.py Faz 1'de taşır)
def d01_s01_dip_band_gun(d: pd.DataFrame, pencere: int = 250, bant: float = 0.03) -> pd.Series:
    """Son 250 günde, o günkü 250 günlük dibin (kayan en düşük) ±%3 bandında kapanan gün sayısı (geriye bakar: her gün kendi bandını kullanır)."""
    C = d.Close.astype(float); L = d.Low.astype(float); dip = L.rolling(pencere, min_periods=pencere // 2).min()
    bandda = (C <= dip * (1 + bant)).astype(float); bandda[dip.isna()] = np.nan
    return bandda.rolling(pencere, min_periods=pencere // 2).sum()


kaydet("D01-S01", "D01", "Dip ne kadar sürede oluştu? (250 günde dip bandında geçirilen gün)", +1, d01_s01_dip_band_gun)
