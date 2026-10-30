"""K55 ortak ayarlar, sürüm, koşu kimliği, dönem kilidi ve olay sabitleri (ön kayıt: K55/ONKAYIT_K55.md).

Bu modül başka K55 modüllerine bağımlı değildir. COL_YOLU_ABD yalnız veri yükleme ve K51 ölçüleri için tembel yüklenir (eski dosya değişmez).
"""
from __future__ import annotations

import hashlib
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

K55_SURUM = "K55 v0.1 (2026-10-30, Faz 0: evren, veri kalitesi, ortak panel, olay tanımları, sızıntı testleri, hücre iskelesi A / B / C)"
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # repo kökü (K55/ klasörünün üstü)
log = logging.getLogger("k55")

# ---------------------------------------------------------------- kilitli sabitler (ONKAYIT_K55.md 2-4; değişiklik = yeni sürüm)
DONEM: Dict[str, Tuple[str, str]] = {"KESIF": ("2016-01-01", "2021-12-31"), "IC_DOGRULAMA": ("2022-01-01", "2023-12-31"), "BAGIMSIZ": ("2024-01-01", "2026-06-05")}
ILERI_BASLANGIC = "2026-09-01"
OLAY: Dict[str, Tuple[int, float]] = {"Y60": (60, 0.30), "Y120": (120, 0.50), "Y250": (250, 1.00)}      # ufuk (işlem günü), eşik (getiri)
PENCERE: Tuple[int, ...] = (5, 10, 20, 40, 60)
KRIZ = "2026-08-31"                 # fon krizi kesimi: fiyat serisi bu günde biter
ALIVE_SINIR = "2026-08-01"          # seri bu tarihten önce bitiyorsa 'erken bitti' (K51 / K54)
MIN_GUN = 260                       # seri başından itibaren ölçü için gereken gün
N_MIN = 30
BOOT = 2000
K_ES = 5                            # eşleşmiş kontrol sayısı
GUN_TOL = 10                        # eşleşmiş ileri yöntemde tarih toleransı (işlem günü)
DD_TOL = 0.10
PURGE_GUN = 60
EMBARGO_GUN = 10
FDR_Q = 0.10


@dataclass
class K55Ayar:
    veri: str = field(default_factory=lambda: os.environ.get("CY_VERI", "/content/drive/MyDrive/COLAB_VERILER/OUTPUT/COL_YOLU_ABD/veri"))
    cikti: str = field(default_factory=lambda: os.environ.get("K55_CIKTI", os.path.join(KOK, "arastirma_cikti", "k55_dallanma")))
    k54: str = field(default_factory=lambda: os.environ.get("K55_K54", os.path.join(KOK, "arastirma_cikti", "col_yolu_abd")))
    isci: int = field(default_factory=lambda: int(os.environ.get("CY_ISCI", "4")))
    tohum: int = 55
    ornek: Optional[int] = None          # None = tam evren; 50 = deneme koşusu


def cy():
    """COL_YOLU_ABD modülü (veri yükleme, K51 ölçüleri, likit eşiği). Eski dosya değiştirilmez; yalnız içe aktarılır."""
    if KOK not in sys.path:
        sys.path.insert(0, KOK)
    import COL_YOLU_ABD as C  # noqa: WPS433
    return C


def sha256_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_metin(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def git_commit(kok: str = KOK) -> str:
    try:
        return subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=20).stdout.strip() or "?"
    except Exception:
        return "?"


def onkayit_sha() -> str:
    """Kilit belgesinin sha256'sı (koşu kimliğine yazılır: hangi kilitle koşuldu)."""
    yol = os.path.join(KOK, "K55", "ONKAYIT_K55.md")
    return sha256_dosya(yol) if os.path.exists(yol) else ""


def kosu_kimligi(A: K55Ayar, evren_surum: str, paketler: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Tekrar üretilebilir koşu kimliği: zaman, kod sürümü, git commit, kilit sha, evren sürümü, veri paketi sha listesi, ayarlar."""
    return {"kimlik": f"K55-{time.strftime('%Y%m%d-%H%M%S')}-{git_commit()}", "kod_surum": K55_SURUM, "commit": git_commit(), "onkayit_sha": onkayit_sha(),
            "evren_surum": evren_surum, "veri_paketleri": paketler or {}, "ayar": {"veri": A.veri, "cikti": A.cikti, "isci": A.isci, "tohum": A.tohum, "ornek": A.ornek},
            "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}


def donem_etiketi(tarih: pd.Series) -> pd.Series:
    """Tarih -> KESIF / IC_DOGRULAMA / BAGIMSIZ / ILERI / DISI (kilitli sınırlar)."""
    t = pd.to_datetime(tarih); out = pd.Series("DISI", index=t.index, dtype=object)
    for ad, (a, b) in DONEM.items():
        out[(t >= a) & (t <= b)] = ad
    out[t >= ILERI_BASLANGIC] = "ILERI"
    return out


def gunluk_log() -> None:
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
