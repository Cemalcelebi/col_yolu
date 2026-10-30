"""K55 ortak ayarlar, sürüm, kilitli sabitler, dönem etiketleri, koşu kimliği ve çıktı yolu güvenliği (ön kayıt: K55/ONKAYIT_K55.md v1.2).

Bu modül başka K55 modüllerine bağımlı değildir. COL_YOLU_ABD yalnız veri yükleme ve K51 ölçüleri için tembel yüklenir (eski dosya değişmez,
içe aktarma yan etkisizdir; test_k55 bunu ağ kapalıyken ve çıktı dosyalarının sha256'sıyla sınar).
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

K55_SURUM = "K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi)"
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # repo kökü (K55/ klasörünün üstü)
log = logging.getLogger("k55")

# ---------------------------------------------------------------- kilitli sabitler (ONKAYIT_K55.md 2-4, v1.2; değişiklik = yeni sürüm + gerekçe)
DONEM: Dict[str, Tuple[str, str]] = {"KESIF": ("2016-01-01", "2021-12-31"), "IC_DOGRULAMA": ("2022-01-01", "2023-12-31"), "BAGIMSIZ": ("2024-01-01", "2026-06-05")}
ILERI_BASLANGIC = "2026-09-01"
OLAY: Dict[str, Tuple[int, float]] = {"Y60": (60, 0.30), "Y120": (120, 0.50), "Y250": (250, 1.00)}      # ufuk (işlem günü), eşik (getiri)
PENCERE: Tuple[int, ...] = (5, 10, 20, 40, 60)
KRIZ = "2026-08-31"                 # fon krizi kesimi: fiyat serisi bu günde biter
ALIVE_SINIR = "2026-08-01"          # seri bu tarihten önce bitiyorsa 'erken bitti' (K51 / K54)
MIN_GUN = 260                       # özellik hesaplama gereksinimi (ilk 260 satır özelliksiz); evrenden silme ölçütü DEĞİL
N_MIN = 30
BOOT = 2000
K_ES = 5                            # eşleşmiş kontrol sayısı
GUN_TOL = 10                        # eşleşmiş ileri yöntemde tarih toleransı (işlem günü)
DD_TOL = 0.10
PURGE_GUN = max(h for h, _ in OLAY.values())      # 250: en uzun etiket ufku; ufuk başına purge = kendi ufku (donem_etiketi_ufuk)
EMBARGO_GUN = 10                    # işlem günü; takvimde ~14 gün
EMBARGO_TAKVIM_GUN = 14
BLOK_GUN = 60                       # blok bootstrap: ardışık 60 işlem günü (ufukla aynı)
FDR_Q = 0.10                        # aile = (dal, yöntem) × KEŞİF; hücre içi Holm
A_D_ESIK = 0.20
A_AUC_ESIK = 0.06
B_FARK_ESIK = 0.05
C_LIFT_ESIK = 1.3
CUSUM_H = 4.0

AYARLAR: Dict[str, Any] = {"DONEM": DONEM, "ILERI_BASLANGIC": ILERI_BASLANGIC, "OLAY": OLAY, "PENCERE": PENCERE, "KRIZ": KRIZ, "ALIVE_SINIR": ALIVE_SINIR, "MIN_GUN": MIN_GUN,
                           "N_MIN": N_MIN, "BOOT": BOOT, "K_ES": K_ES, "GUN_TOL": GUN_TOL, "DD_TOL": DD_TOL, "PURGE_GUN": PURGE_GUN, "EMBARGO_GUN": EMBARGO_GUN,
                           "EMBARGO_TAKVIM_GUN": EMBARGO_TAKVIM_GUN, "BLOK_GUN": BLOK_GUN, "FDR_Q": FDR_Q, "A_D_ESIK": A_D_ESIK, "A_AUC_ESIK": A_AUC_ESIK,
                           "B_FARK_ESIK": B_FARK_ESIK, "C_LIFT_ESIK": C_LIFT_ESIK, "CUSUM_H": CUSUM_H}

DRIVE_OUTPUT = "/content/drive/MyDrive/COLAB_VERILER/OUTPUT"
IZINLI_KOKLER: Tuple[str, ...] = (DRIVE_OUTPUT, os.path.join(KOK, "arastirma_cikti", "k55_dallanma"))
YASAK_KOKLER: Tuple[str, ...] = (os.path.join(KOK, "arastirma_cikti", "col_yolu_abd"),)          # K51-K54 çıktıları: K55 asla buraya yazmaz
KOD_DOSYALARI_GORELI: Tuple[str, ...] = ("K55.py", "COL_YOLU_ABD.py", "evren_disi_ABD.csv", "K55/ONKAYIT_K55.md")


def _varsayilan_cikti() -> str:
    ek = os.environ.get("K55_CIKTI")
    if ek:
        return ek
    return os.path.join(DRIVE_OUTPUT, "K55") if os.path.isdir(DRIVE_OUTPUT) else os.path.join(KOK, "arastirma_cikti", "k55_dallanma")


@dataclass
class K55Ayar:
    veri: str = field(default_factory=lambda: os.environ.get("CY_VERI", os.path.join(DRIVE_OUTPUT, "COL_YOLU_ABD", "veri")))
    cikti: str = field(default_factory=_varsayilan_cikti)
    k54: str = field(default_factory=lambda: os.environ.get("K55_K54", os.path.join(KOK, "arastirma_cikti", "col_yolu_abd")))
    isci: int = field(default_factory=lambda: int(os.environ.get("CY_ISCI", "4")))
    tohum: int = 55
    ornek: Optional[int] = None          # None = tam evren; 50 = deneme koşusu


def cy():
    """COL_YOLU_ABD modülü (veri yükleme, K51 ölçüleri, likit eşiği). Eski dosya değiştirilmez; yalnız içe aktarılır (yan etkisiz)."""
    if KOK not in sys.path:
        sys.path.insert(0, KOK)
    import COL_YOLU_ABD as C  # noqa: WPS433
    return C


# ---------------------------------------------------------------- sha / git
def sha256_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_metin(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_klasor(yol: str, uzanti: str = ".csv") -> str:
    """Klasördeki dosyaların (ad + sha256) listesinin sha256'sı (Tiingo csv klasörü gibi)."""
    if not os.path.isdir(yol):
        return ""
    adlar = sorted(f for f in os.listdir(yol) if f.endswith(uzanti))
    return sha256_metin("\n".join(f"{a}:{sha256_dosya(os.path.join(yol, a))}" for a in adlar) + f"\n{len(adlar)}")


def git_commit(kok: str = KOK) -> str:
    try:
        return subprocess.run(["git", "-C", kok, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=20).stdout.strip() or "?"
    except Exception:
        return "?"


def git_kirli(kok: str = KOK, yollar: Tuple[str, ...] = ("K55", "K55.py", "COL_YOLU_ABD.py", "evren_disi_ABD.csv")) -> List[str]:
    """Verilen yollarda commit'lenmemiş (değişmiş ya da izlenmeyen) dosyalar."""
    try:
        r = subprocess.run(["git", "-C", kok, "status", "--porcelain", "--", *yollar], capture_output=True, text=True, timeout=20)
        return [l[3:] for l in r.stdout.splitlines() if l.strip()]
    except Exception as ex:
        return [f"git durumu alınamadı: {ex}"]


def onkayit_sha() -> str:
    """Kilit belgesinin sha256'sı; dosya yoksa boş (koşu durur)."""
    yol = os.path.join(KOK, "K55", "ONKAYIT_K55.md")
    return sha256_dosya(yol) if os.path.exists(yol) else ""


def ayar_sha() -> str:
    return sha256_metin(json.dumps(AYARLAR, sort_keys=True, ensure_ascii=False, default=str))


def kod_dosyalari() -> Dict[str, str]:
    """K55 modülleri + giriş + COL_YOLU_ABD + evren dışı listesi + kilit: ad -> sha256."""
    out = {}
    kd = os.path.join(KOK, "K55")
    for f in sorted(os.listdir(kd)):
        if f.endswith(".py"):
            out[f"K55/{f}"] = sha256_dosya(os.path.join(kd, f))
    for g in KOD_DOSYALARI_GORELI:
        y = os.path.join(KOK, g)
        if os.path.exists(y):
            out[g] = sha256_dosya(y)
    return out


def veri_dosyalari(A: K55Ayar) -> Dict[str, str]:
    """Zorunlu veri girdileri: ad -> yol (eksik olan koşuyu durdurur). Tiingo klasörü klasör sha'sıyla."""
    return {"V_ABD.pkl": os.path.join(A.veri, "V_ABD.pkl"), "k34_yahoo.pkl": os.path.join(A.veri, "k34_yahoo.pkl"), "k34_evren.csv": os.path.join(A.veri, "k34_evren.csv"),
            "endeks.pkl": os.path.join(A.veri, "endeks.pkl"), "tiingo/": os.path.join(A.veri, "tiingo"),
            "sektor_ABD.csv": next((p for p in (os.path.join(A.veri, "sektor_ABD.csv"), os.path.join(KOK, "sektor_ABD.csv")) if os.path.exists(p)), os.path.join(KOK, "sektor_ABD.csv")),
            "K54_SIRKET_DURUMU.csv": os.path.join(A.k54, "K54_SIRKET_DURUMU.csv"), "K54_EVREN_ESLESTIRME.csv": os.path.join(A.k54, "K54_EVREN_ESLESTIRME.csv")}


def veri_sha(A: K55Ayar) -> Dict[str, str]:
    out = {}
    for ad, yol in veri_dosyalari(A).items():
        if ad.endswith("/"):
            if not os.path.isdir(yol):
                raise FileNotFoundError(f"zorunlu veri klasörü yok: {ad} -> {yol}")
            out[ad] = sha256_klasor(yol)
        else:
            if not os.path.exists(yol):
                raise FileNotFoundError(f"zorunlu veri dosyası yok: {ad} -> {yol}")
            out[ad] = sha256_dosya(yol)
    return out


def cikti_dogrula(yol: str) -> str:
    """Çıkış yolu güvenliği: gerçek yola çözülür; izinli köklerden (Drive OUTPUT, repo arastirma_cikti/k55_dallanma, K55_CIKTI_EK) biri altında
    olmalı; K51-K54 çıktı klasörü yasak. Dönüş: çözülmüş yol."""
    gercek = os.path.realpath(os.path.abspath(yol)); izinli = [os.path.realpath(k) for k in IZINLI_KOKLER]
    ek = os.environ.get("K55_CIKTI_EK")
    if ek:
        izinli += [os.path.realpath(p) for p in ek.split(os.pathsep) if p]
    for y in YASAK_KOKLER:
        yr = os.path.realpath(y)
        if gercek == yr or gercek.startswith(yr + os.sep):
            raise PermissionError(f"çıkış yolu yasak (K51-K54 çıktıları değiştirilmez): {gercek}")
    if not any(gercek == k or gercek.startswith(k + os.sep) for k in izinli):
        raise PermissionError(f"çıkış yolu izinli kökler altında değil: {gercek}; izinli: {izinli}")
    return gercek


def kosu_kimligi(A: K55Ayar, evren_surum: str, paketler: Optional[Dict[str, str]] = None, veri: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Tekrar üretilebilir koşu kimliği (v1.2): zaman, kod sürümü, commit, git kirlilik denetimi, kilit sha (boşsa durur), yapılandırma sha,
    kod dosyaları sha, veri dosyaları sha (zorunlu), evren sürümü, veri paketleri, ayarlar."""
    ok_sha = onkayit_sha()
    if not ok_sha:
        raise RuntimeError("ön kayıt (K55/ONKAYIT_K55.md) bulunamadı: kilit olmadan koşu yok")
    kirli = git_kirli()
    if kirli and os.environ.get("K55_KIRLI_IZIN") != "1":
        raise RuntimeError(f"git çalışma ağacında commit'lenmemiş kod / ayar dosyası var (koşu commit'e bağlanamaz): {kirli[:10]}; "
                           "önce commit'le ya da K55_KIRLI_IZIN=1 ile (kimliğe KİRLİ yazılır) geç")
    vs = veri if veri is not None else veri_sha(A)
    return {"kimlik": f"K55-{time.strftime('%Y%m%d-%H%M%S')}-{git_commit()}" + ("-KIRLI" if kirli else ""), "kod_surum": K55_SURUM, "commit": git_commit(), "git_kirli": kirli,
            "onkayit_sha": ok_sha, "ayar_sha": ayar_sha(), "ayarlar": AYARLAR, "kod_sha": kod_dosyalari(), "veri_sha": vs, "evren_surum": evren_surum, "veri_paketleri": paketler or {},
            "ayar": {"veri": A.veri, "cikti": A.cikti, "k54": A.k54, "isci": A.isci, "tohum": A.tohum, "ornek": A.ornek},
            "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}


# ---------------------------------------------------------------- dönem etiketleri (v1.2: gün sonu, saat dilimi, NaT; purge / embargo)
def _tarih_normalize(tarih: Any) -> pd.Series:
    t = pd.to_datetime(pd.Series(tarih), errors="coerce")
    if getattr(t.dt, "tz", None) is not None:
        t = t.dt.tz_localize(None)                                      # saat dilimli damga -> yerel takvim günü
    return t.dt.normalize()


def donem_etiketi(tarih: Any) -> pd.Series:
    """Tarih -> KESIF / IC_DOGRULAMA / BAGIMSIZ / ILERI / DISI. Bitiş günü bütün gün dahil; NaT -> DISI."""
    t = _tarih_normalize(tarih); out = pd.Series("DISI", index=t.index, dtype=object)
    for ad, (a, b) in DONEM.items():
        out[(t >= pd.Timestamp(a)) & (t <= pd.Timestamp(b))] = ad
    out[t >= pd.Timestamp(ILERI_BASLANGIC)] = "ILERI"; out[t.isna()] = "DISI"
    return out


def donem_etiketi_ufuk(tarih: Any, bitis: Any) -> pd.Series:
    """Sinyal / olay için dönem (purge + embargo): t0 dönemi; etiket penceresinin son günü (bitis) aynı dönemde bitmiyorsa PURGE; t0 dönem
    başlangıcını izleyen EMBARGO_TAKVIM_GUN içindeyse EMBARGO; bitis NaT (pencere tanımsız) -> TANIMSIZ."""
    t = _tarih_normalize(tarih); b = _tarih_normalize(bitis); out = donem_etiketi(t)
    for ad, (a, s) in DONEM.items():
        m = out == ad
        out[m & b.isna()] = "TANIMSIZ"
        out[m & b.notna() & (b > pd.Timestamp(s))] = "PURGE"
        out[m & (t < pd.Timestamp(a) + pd.Timedelta(days=EMBARGO_TAKVIM_GUN))] = "EMBARGO"
    return out


def gunluk_log() -> None:
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")
