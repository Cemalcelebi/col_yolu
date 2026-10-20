# =====================================================================
#  GH_GUNLUK — GitHub Actions gunluk calistirici   (2026-10-19, v1)
#
#  AMAC
#    Cemal telefondayken (Colab'a basmadan) her is gunu aksami:
#      BASLAT.py  ->  gun()   zincirini GitHub'in bulutunda calistirmak,
#    raporu rapor/ klasorune yazmak. Colab'daki davranis DEGISMEZ:
#    BASLAT.py, COL_v1.py, takip.py ve digerlerine dokunulmaz.
#
#  NASIL
#    Is akisi (.github/workflows/gunluk_col_tarama.yml) once
#        /content/drive/MyDrive/col_tarayici  ->  repo koku
#    sembolik baglantisini kurar. Boylece kodlardaki sabit Drive yollari
#    oldugu gibi calisir. Bu dosya o baglantiyi denetler, BASLAT.py'yi
#    Colab'daki gibi exec eder, gun()'u calistirir ve ciktiyi yakalar.
#
#  KURALLAR (KURAL_MOTORU: her adim ayri, her adim kendi hatasini raporlar)
#    K0  Ortam    : Drive yolu var ve repo kokune cikiyor olmali, yoksa DUR.
#    K1  Onbellek : veri_1d_turkey.pkl ciplak sozluk ise {'kayit','veri'}
#                   kabina sarilir (col_atilim_TEK.onbellek_oku yalniz bu
#                   bicimi okur; aksi halde her gun 10 yil bastan iner).
#    K2  Kurulum  : BASLAT.py exec — cikti rapor/kurulum_log.txt'ye.
#    K3  Gunluk   : gun() — cikti raporun govdesi.
#    K4  Rapor    : rapor/son_rapor.txt + rapor/YYYY-MM-DD.txt (TR tarihi).
#    Herhangi bir adim duserse rapor 'HATA' basligi ve hata izi ile yine
#    yazilir, program 1 koduyla cikar (is akisi kirmizi gorunur).
# =====================================================================
from __future__ import annotations

import contextlib
import datetime as dt
import io
import logging
import os
import pickle
import sys
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple

SURUM = "GH_GUNLUK v1 (2026-10-19)"
DRIVE_K = "/content/drive/MyDrive/col_tarayici"
KOK = os.path.dirname(os.path.abspath(__file__))
RAPOR_KLASOR = os.path.join(KOK, "rapor")
VERI_PKL = "veri_1d_turkey.pkl"
GEREKLI_DOSYALAR = ["BASLAT.py", "col_atilim_TEK.py", "COL_v1.py", "takip.py", "veri_koru.py", "bolunme_onar.py"]
ONERILEN_GIRDILER = ["v1_final_BIST.csv", "kirilim_sonrasi_w.csv", "yeni_BIST_2023.csv",
                     "temel_duz.csv", "cds_2022.csv", "sektor_BIST.csv"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                    datefmt="%H:%M:%S", stream=sys.stderr)
log = logging.getLogger("col.gh")


def tr_simdi() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=3)


class Tee(io.TextIOBase):
    """Yazilani hem ekrana (Actions logu) hem bellege yazar."""

    def __init__(self, ekran) -> None:
        self.ekran = ekran
        self.tampon = io.StringIO()

    def write(self, s: str) -> int:  # type: ignore[override]
        try:
            self.ekran.write(s)
        except Exception:
            pass
        return self.tampon.write(s)

    def flush(self) -> None:  # type: ignore[override]
        try:
            self.ekran.flush()
        except Exception:
            pass

    def metin(self) -> str:
        return self.tampon.getvalue()


# --------------------------------------------------------------- KURALLAR
def k0_ortam() -> List[str]:
    """Drive yolu taklidi ve gerekli dosyalar. Donus: uyarilar (eksik oneriler)."""
    if not os.path.isdir(DRIVE_K):
        raise RuntimeError(f"K0: {DRIVE_K} yok. Is akisindaki 'Drive yolunu taklit et' adimi calismamis.")
    if os.path.realpath(DRIVE_K) != os.path.realpath(KOK):
        raise RuntimeError(f"K0: {DRIVE_K} -> {os.path.realpath(DRIVE_K)}; beklenen repo koku {KOK}.")
    eksik = [f for f in GEREKLI_DOSYALAR if not os.path.exists(os.path.join(KOK, f))]
    if eksik:
        raise RuntimeError(f"K0: gerekli dosya yok: {', '.join(eksik)}")
    uyari = [f for f in ONERILEN_GIRDILER if not os.path.exists(os.path.join(KOK, f))]
    for f in uyari:
        log.warning("K0: girdi yok: %s (BASLAT yerine yeniden hesaplar ya da o kismi atlar)", f)
    if os.getcwd() != KOK:
        os.chdir(KOK)   # col_atilim_TEK Colab disinda onbellegi '.' klasorunde arar
    log.info("K0 tamam: Drive yolu -> %s", KOK)
    return uyari


def k1_onbellek_bicimi() -> str:
    """Ciplak {sembol: df} sozlugunu {'kayit','veri'} kabina sarar. Donus: durum metni."""
    yol = os.path.join(KOK, VERI_PKL)
    if not os.path.exists(yol):
        log.info("K1: onbellek yok — ilk calisma, tum veri indirilecek (10-20 dk)")
        return "yok (ilk indirme)"
    try:
        with open(yol, "rb") as f:
            p = pickle.load(f)
    except Exception as e:
        log.warning("K1: onbellek okunamadi (%s) — silinip bastan indirilecek", e)
        os.remove(yol)
        return f"bozuk, silindi ({type(e).__name__})"
    if isinstance(p, dict) and "veri" in p:
        return f"hazir ({len(p.get('veri') or {})} hisse)"
    if isinstance(p, dict) and p:
        tmp = yol + ".gh.tmp"
        with open(tmp, "wb") as f:
            pickle.dump({"kayit": str(tr_simdi()), "veri": p}, f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, yol)
        log.info("K1: ciplak onbellek kabina sarildi (%d hisse)", len(p))
        return f"sarildi ({len(p)} hisse)"
    log.warning("K1: onbellek bos/taninmayan bicim — silindi")
    os.remove(yol)
    return "taninmadi, silindi"


def k2_kurulum(G: Dict[str, Any]) -> str:
    """BASLAT.py'yi Colab'daki gibi exec eder. Donus: kurulum ciktisi."""
    kod = open(os.path.join(KOK, "BASLAT.py"), encoding="utf-8").read()
    tee = Tee(sys.stdout)
    t0 = time.monotonic()
    try:
        with contextlib.redirect_stdout(tee):
            exec(compile(kod, os.path.join(DRIVE_K, "BASLAT.py"), "exec"), G)
    finally:
        log.info("K2: BASLAT %.0f sn", time.monotonic() - t0)
    for ad in ("gun", "VERI"):
        if ad not in G:
            raise RuntimeError(f"K2: BASLAT sonrasi '{ad}' tanimli degil — zincir yarida kaldi")
    if not G["VERI"]:
        raise RuntimeError("K2: VERI bos — veri indirilemedi (Yahoo erisimi / hiz siniri?)")
    return tee.metin()


def k3_gunluk(G: Dict[str, Any]) -> Tuple[str, Dict[str, int]]:
    """gun() calistirir. Donus: (ekran ciktisi, ozet sayilar)."""
    tee = Tee(sys.stdout)
    with contextlib.redirect_stdout(tee):
        A, P, Kp = G["gun"]()
    return tee.metin(), {"aday": len(A), "pozisyon": len(P), "kapanan": len(Kp)}


def k4_rapor(baslik: List[str], govde: str, kurulum: Optional[str]) -> List[str]:
    os.makedirs(RAPOR_KLASOR, exist_ok=True)
    metin = "\n".join(baslik) + "\n" + "=" * 60 + "\n" + govde.rstrip() + "\n"
    yollar = [os.path.join(RAPOR_KLASOR, "son_rapor.txt"),
              os.path.join(RAPOR_KLASOR, f"{tr_simdi():%Y-%m-%d}.txt")]
    for y in yollar:
        tmp = y + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(metin)
        os.replace(tmp, y)
    if kurulum is not None:
        with open(os.path.join(RAPOR_KLASOR, "kurulum_log.txt"), "w", encoding="utf-8") as f:
            f.write(kurulum)
    return yollar


# --------------------------------------------------------------- ANA
def calistir() -> int:
    t0 = time.monotonic()
    basla = tr_simdi()
    baslik = [f"COL GUNLUK RAPOR — {basla:%Y-%m-%d %H:%M} (TR)", f"Calistirici: {SURUM} | GitHub Actions"]
    kurulum: Optional[str] = None
    try:
        uyari = k0_ortam()
        baslik.append(f"Onbellek: {k1_onbellek_bicimi()}")
        if uyari:
            baslik.append(f"Eksik girdi: {', '.join(uyari)}")
        G: Dict[str, Any] = {"__name__": "__main__", "__file__": os.path.join(DRIVE_K, "BASLAT.py")}
        kurulum = k2_kurulum(G)
        veri = G["VERI"]
        son_bar = max(df.index[-1] for df in veri.values() if len(df)).date()
        govde, ozet = k3_gunluk(G)
        baslik.append(f"Veri: {len(veri)} hisse | son bar {son_bar}")
        baslik.append(f"Ozet: aday {ozet['aday']} | pozisyon {ozet['pozisyon']} | kapanan {ozet['kapanan']} "
                      f"| sure {time.monotonic() - t0:.0f} sn")
        if son_bar < basla.date() and basla.weekday() < 5:
            baslik.append(f"UYARI: bugunun bari yok (son bar {son_bar}). Yahoo gecikmis olabilir.")
        yollar = k4_rapor(baslik, govde, kurulum)
        log.info("Rapor yazildi: %s", ", ".join(os.path.relpath(y, KOK) for y in yollar))
        return 0
    except Exception as e:
        iz = traceback.format_exc()
        log.error("CALISMA DUSTU: %s", e)
        baslik.insert(0, "HATA — tarama tamamlanamadi")
        try:
            k4_rapor(baslik, f"Hata: {type(e).__name__}: {e}\n\n{iz}", kurulum)
        except Exception as e2:
            log.error("Hata raporu da yazilamadi: %s", e2)
        return 1


if __name__ == "__main__":
    sys.exit(calistir())
