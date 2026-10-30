"""K55 hücre kayıt defteri. Kimlik -> tanım. Değişken fonksiyonu OHLCV tablosu alır, aynı uzunlukta Series döndürür ve YALNIZ o gün ve öncesine bakar
(sizinti.kesme_testi ile zorunlu doğrulama; test_k55 bütün kayıtlı hücreleri sentetik seride sınar). Tanım sonradan değişmez; yeni tanım = yeni kimlik.

Tanım alanları: dal, soru, yon (+1 üst beşte bir sinyal, −1 alt), fabrika (pencere p -> fonk(d)) ya da fonk (pencere yok), pencereler (varyantlar;
(None,) = tek), panel_fonk (kesitsel bileşik: P -> Series; D10), yontemler (A / B / C; kesitsel bileşikte C yok), not_, veri (hangi dal modülü).
Faz 1 dalları (D01-D06, D10) dal modülleri içinde kaydedilir (dal01_fiyat.py …); faz1.py önce bu modülleri ek verilerle (SPY, IWM, sektör sepetleri)
kurar. Faz 0'da yalnız D01-S01 (iskele) kayıtlıdır.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import pandas as pd

HUCRELER: Dict[str, Dict[str, Any]] = {}


def kaydet(kimlik: str, dal: str, soru: str, yon: int, fonk: Optional[Callable[[pd.DataFrame], pd.Series]] = None, fabrika: Optional[Callable[[int], Callable]] = None,
           pencereler: Tuple[Optional[int], ...] = (None,), panel_fonk: Optional[Callable] = None, yontemler: Tuple[str, ...] = ("A", "B", "C"), not_: str = "") -> None:
    if kimlik in HUCRELER:
        raise KeyError(f"hücre kimliği zaten kayıtlı (tanım değişmez; yeni kimlik aç): {kimlik}")
    if fonk is None and fabrika is None and panel_fonk is None:
        raise ValueError(f"{kimlik}: fonk, fabrika ya da panel_fonk gerekli")
    if fabrika is not None and fonk is None and panel_fonk is None:
        fonk = fabrika(pencereler[0] if pencereler and pencereler[0] is not None else 20)
    HUCRELER[kimlik] = {"dal": dal, "soru": soru, "yon": yon, "fonk": fonk, "fabrika": fabrika, "pencereler": tuple(pencereler), "panel_fonk": panel_fonk, "yontemler": tuple(yontemler), "not": not_}


def temizle(dal: Optional[str] = None) -> None:
    """Test / yeniden kurulum için kayıtları siler (dal verilirse yalnız o dal)."""
    for k in [k for k, v in HUCRELER.items() if dal is None or v["dal"] == dal]:
        HUCRELER.pop(k)


# ---------------------------------------------------------------- D01-S01 (Faz 0 iskelesi; aynı tanım dal01_fiyat.py'de de kayıtlı olur)
def d01_s01_dip_band_gun(d: pd.DataFrame, pencere: int = 250, bant: float = 0.03) -> pd.Series:
    """Son 250 günde, o günkü 250 günlük dibin (kayan en düşük) ±%3 bandında kapanan gün sayısı (geriye bakar: her gün kendi bandını kullanır)."""
    C = d.Close.astype(float); L = d.Low.astype(float); dip = L.rolling(pencere, min_periods=pencere // 2).min()
    bandda = (C <= dip * (1 + bant)).astype(float); bandda[dip.isna()] = np.nan
    return bandda.rolling(pencere, min_periods=pencere // 2).sum()


kaydet("D01-S01", "D01", "Dip ne kadar sürede oluştu? (250 günde dip bandında geçirilen gün)", +1, d01_s01_dip_band_gun)
