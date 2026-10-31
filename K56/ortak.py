"""K56 ortak: sürüm, yollar, çıktı yolu güvenliği, kaynak (K51-K55) okuma kaydı, koşu kimliği, ağ istemcisi (SEC / genel; boyut sınırı, önbellek).

Bağımsızlık: K51-K55 dosyaları DEĞİŞTİRİLMEZ. K55 paketinden yalnız saf yardımcılar (sha, dönem sınırları, istatistik) içe aktarılır ve
sha'ları koşu kimliğine yazılır. K51-K55 çıktılarının her okunuşu `kaynak_kaydi`na (yeniden kullanım kaydı) girer.
SEC: User-Agent'taki iletişim e-postası YALNIZ SEC_EPOSTA ortam değişkeninden okunur; koda, loga, çıktıya ve repoya yazılmaz.
"""
from __future__ import annotations

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

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if KOK not in sys.path:
    sys.path.insert(0, KOK)
from K55.ortak import DONEM as K55_DONEM, KRIZ, git_commit, sha256_dosya, sha256_metin  # noqa: E402  (salt okunur içe aktarma)

K56_SURUM = "K56 v0.1 (2026-10-30, Faz 0: etki envanteri, mekanizma hipotezleri, veri kaynakları, küçük örneklem erişim testi, seçim etkisi sentetik sınaması)"
log = logging.getLogger("k56")

DRIVE_OUTPUT = "/content/drive/MyDrive/COLAB_VERILER/OUTPUT"
CIKTI_ALT = "K56_MEKANIZMA"
REPO_CIKTI = os.path.join(KOK, "arastirma_cikti", "k56_mekanizma")
IZINLI_KOKLER: Tuple[str, ...] = (os.path.join(DRIVE_OUTPUT, CIKTI_ALT), REPO_CIKTI)
YASAK_KOKLER: Tuple[str, ...] = (os.path.join(KOK, "arastirma_cikti", "col_yolu_abd"), os.path.join(KOK, "arastirma_cikti", "k55_dallanma"),
                                 os.path.join(DRIVE_OUTPUT, "COL_YOLU_ABD"), os.path.join(DRIVE_OUTPUT, "K55"))
KOD_YOLLARI: Tuple[str, ...] = ("K56", "K56.py", "K55", "COL_YOLU_ABD.py", "FON_IZI.py")     # K56'nın çağırdığı K55 / COL_YOLU_ABD / FON_IZI kodu da kimliğe girer
BUYUK_INDIRME_SINIR = 64 * 1024 * 1024        # Faz 0: tek dosya en çok 64 MB (büyük veri indirme yok)
SEC_HIZ = 0.15                                # SEC adil erişim: saniyede en çok ~7 istek (sınır 10)

# Dönem politikası (ONKAYIT_K56 2): K55 dönem sınırları aynen; K56 mekanizma testleri KEŞİF 2016-21'de keşif-verisi YENİDEN KULLANIMI olarak
# işaretlenir; İÇ 2022-23 ve BAĞIMSIZ 2024-26 (K55'te açılmadı) Cemal'in kararı olmadan açılmaz.
DONEM = dict(K55_DONEM)


def _varsayilan_cikti() -> str:
    ek = os.environ.get("K56_CIKTI")
    if ek:
        return ek
    return os.path.join(DRIVE_OUTPUT, CIKTI_ALT) if os.path.isdir(DRIVE_OUTPUT) else REPO_CIKTI


def _ilk_var(*yollar: str) -> str:
    for y in yollar:
        if y and os.path.exists(y):
            return y
    return yollar[0]


@dataclass
class K56Ayar:
    cikti: str = field(default_factory=_varsayilan_cikti)
    abd: str = field(default_factory=lambda: os.environ.get("K56_ABD", _ilk_var(os.path.join(KOK, "arastirma_cikti", "col_yolu_abd"), os.path.join(DRIVE_OUTPUT, "COL_YOLU_ABD"))))
    k55: str = field(default_factory=lambda: os.environ.get("K56_K55", _ilk_var(os.path.join(KOK, "arastirma_cikti", "k55_dallanma", "tam_evren"), os.path.join(DRIVE_OUTPUT, "K55"))))
    veri: str = field(default_factory=lambda: os.environ.get("CY_VERI", os.path.join(DRIVE_OUTPUT, "COL_YOLU_ABD", "veri")))
    iv: str = field(default_factory=lambda: os.environ.get("K56_IV", "/tmp/iv"))          # islenmis-veri dalı (git worktree)
    onbellek: str = field(default_factory=lambda: os.environ.get("K56_ONBELLEK", os.path.join("/content/drive/MyDrive/COLAB_VERILER", "K56_onbellek") if os.path.isdir(DRIVE_OUTPUT) else os.path.join("/tmp", "k56_onbellek")))
    ag: bool = False                          # Faz 0 erişim testi dışında ağ kapalı
    ornek: int = 12
    tohum: int = 56


# ---------------------------------------------------------------- çıktı yolu ve kaynak kaydı
def cikti_dogrula(yol: str) -> str:
    """Çıktı yalnız K56 köklerine (Drive OUTPUT/K56_MEKANIZMA, repo arastirma_cikti/k56_mekanizma, K56_CIKTI_EK); K51-K55 çıktıları yasak."""
    gercek = os.path.realpath(os.path.abspath(yol)); izinli = [os.path.realpath(k) for k in IZINLI_KOKLER]
    ek = os.environ.get("K56_CIKTI_EK")
    if ek:
        izinli += [os.path.realpath(p) for p in ek.split(os.pathsep) if p]
    for y in YASAK_KOKLER:
        yr = os.path.realpath(y)
        if gercek == yr or gercek.startswith(yr + os.sep):
            raise PermissionError(f"çıkış yolu yasak (K51-K55 çıktıları değiştirilmez): {gercek}")
    if not any(gercek == k or gercek.startswith(k + os.sep) for k in izinli):
        raise PermissionError(f"çıkış yolu K56 kökleri altında değil: {gercek}; izinli: {izinli}")
    return gercek


class KaynakKaydi:
    """K51-K55 (ve işlenmiş veri) dosyalarının her okunuşu: yol, sha256, amaç. 'Eski sonuçların yeni araştırmada kullanımı' kaydıdır (ONKAYIT_K56 1)."""

    AMAC = ("envanter", "hipotez_uretimi", "orneklem_secimi", "veri", "kiyas")

    def __init__(self) -> None:
        self.kayit: List[Dict[str, str]] = []

    def oku(self, yol: str, amac: str, aciklama: str = "") -> str:
        if amac not in self.AMAC:
            raise ValueError(f"bilinmeyen amaç: {amac}")
        if not os.path.exists(yol):
            raise FileNotFoundError(f"kaynak yok: {yol}")
        sha = sha256_dosya(yol)
        if not any(k["yol"] == yol and k["amac"] == amac for k in self.kayit):
            self.kayit.append({"yol": os.path.relpath(yol, KOK) if yol.startswith(KOK) else yol, "sha256": sha, "amac": amac, "aciklama": aciklama})
        return yol

    def tablo(self) -> pd.DataFrame:
        return pd.DataFrame(self.kayit, columns=["yol", "sha256", "amac", "aciklama"])


# ---------------------------------------------------------------- koşu kimliği
def git_kirli(yollar: Tuple[str, ...] = KOD_YOLLARI) -> List[str]:
    try:
        r = subprocess.run(["git", "-C", KOK, "status", "--porcelain", "--", *yollar], capture_output=True, text=True, timeout=20)
        return [l[3:] for l in r.stdout.splitlines() if l.strip()]
    except Exception as ex:
        return [f"git durumu alınamadı: {ex}"]


def onkayit_sha() -> str:
    y = os.path.join(KOK, "K56", "ONKAYIT_K56.md")
    return sha256_dosya(y) if os.path.exists(y) else ""


def kod_sha() -> Dict[str, str]:
    out = {}
    kd = os.path.join(KOK, "K56")
    for f in sorted(os.listdir(kd)):
        if f.endswith(".py") or f.endswith(".md"):
            out[f"K56/{f}"] = sha256_dosya(os.path.join(kd, f))
    k55 = os.path.join(KOK, "K55")
    for g in ["K56.py", "COL_YOLU_ABD.py", "FON_IZI.py"] + [f"K55/{f}" for f in sorted(os.listdir(k55)) if f.endswith(".py")]:
        y = os.path.join(KOK, g)
        if os.path.exists(y):
            out[g] = sha256_dosya(y)
    return out


def kosu_kimligi(A: K56Ayar, faz: str) -> Dict[str, Any]:
    ok = onkayit_sha()
    if not ok:
        raise RuntimeError("ön kayıt (K56/ONKAYIT_K56.md) yok: kilit olmadan koşu yok")
    kirli = git_kirli()
    if kirli and os.environ.get("K56_KIRLI_IZIN") != "1":
        raise RuntimeError(f"commit'lenmemiş K56 kodu var: {kirli[:10]}; önce commit ya da K56_KIRLI_IZIN=1 (kimliğe KİRLİ yazılır)")
    c = git_commit()
    return {"kimlik": f"K56-{faz}-{time.strftime('%Y%m%d-%H%M%S')}-{c}" + ("-KIRLI" if kirli else ""), "surum": K56_SURUM, "commit": c, "git_kirli": kirli,
            "onkayit_sha": ok, "kod_sha": kod_sha(), "ayar": {"cikti": A.cikti, "abd": A.abd, "k55": A.k55, "veri": A.veri, "iv": A.iv, "ag": A.ag, "ornek": A.ornek, "tohum": A.tohum, "onbellek": A.onbellek},
            "python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}


def gunluk_log() -> None:
    if not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%H:%M:%S")


# ---------------------------------------------------------------- ağ istemcisi
class AgKapali(RuntimeError):
    pass


class Istemci:
    """Küçük HTTP istemcisi: ağ izni, boyut sınırı (BUYUK_INDIRME_SINIR), önbellek, yeniden deneme, SEC User-Agent (SEC_EPOSTA'dan), HTTP Range.
    Her istek `gunluk`e (url, durum, bayt, süre, hata) yazılır; e-posta hiçbir kayda girmez."""

    def __init__(self, A: K56Ayar, sinir: int = BUYUK_INDIRME_SINIR) -> None:
        self.A = A; self.sinir = sinir; self.gunluk: List[Dict[str, Any]] = []; self._son_sec = 0.0
        os.makedirs(A.onbellek, exist_ok=True)

    @staticmethod
    def sec_ua() -> str:
        e = os.environ.get("SEC_EPOSTA", "").strip()
        if "@" not in e:
            raise RuntimeError("SEC_EPOSTA ortam değişkeni yok: SEC adil erişim kuralı User-Agent'ta iletişim e-postası ister (koda yazılmaz)")
        return f"col_yolu-arastirma {e}"

    @staticmethod
    def sec_mi(url: str) -> bool:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or "").lower()
        return h == "sec.gov" or h.endswith(".sec.gov")

    def _basliklar(self, url: str, ek: Optional[Dict[str, str]]) -> Dict[str, str]:
        b = {"User-Agent": "col_yolu-arastirma", "Accept-Encoding": "gzip, deflate"}
        if self.sec_mi(url):
            b["User-Agent"] = self.sec_ua()
            gecen = time.time() - self._son_sec
            if gecen < SEC_HIZ:
                time.sleep(SEC_HIZ - gecen)
            self._son_sec = time.time()
        b.update(ek or {})
        return b

    def al(self, url: str, ad: Optional[str] = None, aralik: Optional[Tuple[int, int]] = None, sinir: Optional[int] = None, ek_baslik: Optional[Dict[str, str]] = None,
           yontem: str = "GET", govde: Optional[bytes] = None, deneme: int = 3) -> Tuple[int, bytes, Dict[str, str]]:
        """İstek: (durum, içerik, başlıklar). ad verilirse önbellekten okunur / yazılır. aralik=(a, b) bayt aralığı. Sınır aşılırsa durur."""
        if not self.A.ag:
            raise AgKapali(f"ağ kapalı (K56Ayar.ag=False): {url}")
        import requests
        sinir = sinir or self.sinir; yol = os.path.join(self.A.onbellek, ad) if ad else None
        if yol and os.path.exists(yol):
            veri = open(yol, "rb").read(); self.gunluk.append({"url": url, "yontem": yontem, "durum": "onbellek", "bayt": len(veri), "sn": 0.0, "hata": ""}); return 200, veri, {}
        bas = self._basliklar(url, ek_baslik)
        if aralik:
            bas["Range"] = f"bytes={aralik[0]}-{aralik[1]}"
        hata = ""
        for k in range(deneme):
            t0 = time.time()
            try:
                with requests.request(yontem, url, headers=bas, data=govde, stream=True, timeout=60, allow_redirects=not self.sec_mi(url)) as r:
                    if r.is_redirect and self.sec_mi(url):
                        yeni = requests.compat.urljoin(url, r.headers.get("Location", ""))
                        if not self.sec_mi(yeni):
                            raise RuntimeError(f"SEC isteği SEC dışına yönlendi ({yeni}); e-postalı başlık gönderilmedi")
                        url = yeni; continue
                    boy = int(r.headers.get("Content-Length", "0") or 0)
                    if boy and boy > sinir and r.status_code in (200, 206):
                        raise RuntimeError(f"boyut sınırı aşıldı: {boy} > {sinir} bayt ({url}); Faz 0'da büyük indirme yok")
                    parca = []; top = 0
                    for b in r.iter_content(1 << 16):
                        top += len(b); parca.append(b)
                        if top > sinir:
                            raise RuntimeError(f"boyut sınırı aşıldı (akış): > {sinir} bayt ({url})")
                    veri = b"".join(parca); durum = r.status_code; bh = dict(r.headers)
                self.gunluk.append({"url": url, "yontem": yontem + (" Range" if aralik else ""), "durum": durum, "bayt": len(veri), "sn": round(time.time() - t0, 2), "hata": ""})
                if durum in (429, 500, 502, 503, 504) and k < deneme - 1:
                    time.sleep(2 ** (k + 1)); continue
                if yol and durum == 200:
                    with open(yol, "wb") as f:
                        f.write(veri)
                return durum, veri, bh
            except RuntimeError:
                raise
            except Exception as ex:
                hata = f"{type(ex).__name__}: {str(ex)[:200]}"; self.gunluk.append({"url": url, "yontem": yontem, "durum": "hata", "bayt": 0, "sn": round(time.time() - t0, 2), "hata": hata})
                if k < deneme - 1:
                    time.sleep(2 ** (k + 1))
        return -1, b"", {"hata": hata}

    def bas(self, url: str, ek_baslik: Optional[Dict[str, str]] = None) -> Tuple[int, Dict[str, str]]:
        """HEAD isteği (boyut / varlık)."""
        if not self.A.ag:
            raise AgKapali(f"ağ kapalı: {url}")
        import requests
        t0 = time.time()
        try:
            r = requests.head(url, headers=self._basliklar(url, ek_baslik), timeout=30, allow_redirects=not self.sec_mi(url))
            self.gunluk.append({"url": url, "yontem": "HEAD", "durum": r.status_code, "bayt": 0, "dosya_boyu": int(r.headers.get("Content-Length", "0") or 0), "sn": round(time.time() - t0, 2), "hata": ""})
            return r.status_code, dict(r.headers)
        except Exception as ex:
            self.gunluk.append({"url": url, "yontem": "HEAD", "durum": "hata", "bayt": 0, "sn": round(time.time() - t0, 2), "hata": f"{type(ex).__name__}: {str(ex)[:200]}"})
            return -1, {}


def zip_icerik_listesi(ist: Istemci, url: str, ad: str) -> pd.DataFrame:
    """Büyük zip'i indirmeden içeriğini listeler: HTTP Range ile yalnız sondaki merkez dizin (son 256 KB) okunur. Dönüş: dosya, sıkıştırılmış, açık boy."""
    import struct
    durum, bas = ist.bas(url)
    toplam = int(bas.get("Content-Length", "0") or 0)
    if durum != 200 or not toplam:
        return pd.DataFrame({"hata": [f"HEAD {durum}"]})
    a = max(0, toplam - 262144); d, kuyruk, _ = ist.al(url, ad=ad + ".kuyruk", aralik=(a, toplam - 1), sinir=300000)
    if d not in (200, 206):
        return pd.DataFrame({"hata": [f"Range {d}"]})
    j = kuyruk.rfind(b"PK\x05\x06")
    if j < 0:
        return pd.DataFrame({"hata": ["merkez dizin sonu bulunamadı"]})
    cd_boy, cd_ofs = struct.unpack("<II", kuyruk[j + 12:j + 20]); bas_ofs = cd_ofs - a
    rows = []; k = bas_ofs
    while 0 <= k < j and kuyruk[k:k + 4] == b"PK\x01\x02":
        comp, unc = struct.unpack("<II", kuyruk[k + 20:k + 28]); nl, el, cl = struct.unpack("<HHH", kuyruk[k + 28:k + 34]); lofs = struct.unpack("<I", kuyruk[k + 42:k + 46])[0]
        rows.append({"dosya": kuyruk[k + 46:k + 46 + nl].decode("utf-8", "replace"), "sikistirilmis": comp, "acik": unc, "ofs": lofs}); k += 46 + nl + el + cl
    T = pd.DataFrame(rows); T.attrs["zip_boy"] = toplam
    return T


# ---------------------------------------------------------------- erişim testi satırı ve zip üye başı (kısmi okuma)
ERISIM_DURUM = ("GECTI", "KISMI", "BASARISIZ", "ATLANDI")


def erisim_satiri(modul: str, kaynak: str, test: str, durum: str, olcu: str = "", deger: Any = None, ayrinti: str = "", url: str = "") -> Dict[str, Any]:
    if durum not in ERISIM_DURUM:
        raise ValueError(durum)
    return {"modul": modul, "kaynak": kaynak, "test": test, "durum": durum, "olcu": olcu, "deger": deger, "ayrinti": ayrinti[:600], "url": url}


def zip_uye_bas(ist: "Istemci", url: str, uyeler: pd.DataFrame, uye: str, n_bayt: int, ad: str) -> bytes:
    """Zip içindeki bir üyenin ilk n_bayt sıkıştırılmış verisini HTTP Range ile alıp açar (kısmi; deflate akışı). Büyük dosyayı indirmeden
    ilk satırları okumak için. uyeler: zip_icerik_listesi çıktısı (yerel başlık konumu 'ofs' sütunu gerekir)."""
    import struct
    import zlib
    r = uyeler[uyeler.dosya.str.endswith(uye)]
    if not len(r) or "ofs" not in r:
        raise KeyError(f"zip üyesi yok: {uye}")
    ofs = int(r.ofs.iloc[0]); d, bas, _ = ist.al(url, ad=ad + ".lh", aralik=(ofs, ofs + 29), sinir=1000)
    if bas[:4] != b"PK\x03\x04":
        raise RuntimeError("yerel başlık okunamadı")
    nl, el = struct.unpack("<HH", bas[26:30]); veri_bas = ofs + 30 + nl + el
    d, parca, _ = ist.al(url, ad=ad + ".parca", aralik=(veri_bas, veri_bas + n_bayt - 1), sinir=n_bayt + 1000)
    return zlib.decompressobj(-15).decompress(parca)


# ---------------------------------------------------------------- dönem kapısı (ONKAYIT_K56 v1.2-B): BAĞIMSIZ kapalı
DONEM_SON = {"KESIF": "2021-12-31", "IC_DOGRULAMA": "2023-12-31", "BAGIMSIZ": "2026-06-05"}
BAGIMSIZ_KILIT = "K56_BAGIMSIZ_KILIT.json"


class DonemKapali(PermissionError):
    pass


def donem_kapisi(donem: str, D: Optional[pd.DataFrame] = None, h: Optional[int] = None, kilit_klasoru: Optional[str] = None) -> None:
    """KESIF ve IC_DOGRULAMA serbest; BAGIMSIZ yalnız kilit dosyası doğrulanır ve K56_BAGIMSIZ_AC=1 ise. D verilirse: satırların tarihi ve (h verilirse)
    etiket penceresinin son günü dönem sonunu aşamaz (sızıntı denetimi)."""
    if donem not in DONEM_SON:
        raise ValueError(f"bilinmeyen dönem: {donem}")
    if donem == "BAGIMSIZ":
        if os.environ.get("K56_BAGIMSIZ_AC") != "1":
            raise DonemKapali("BAĞIMSIZ dönem kapalı (Cemal kararı + K56_BAGIMSIZ_KILIT.json + K56_BAGIMSIZ_AC=1 gerekir)")
        bagimsiz_kilit_dogrula(kilit_klasoru)
    if D is not None and len(D):
        son = pd.Timestamp(DONEM_SON[donem])
        if (pd.to_datetime(D.tarih) > son).any():
            raise DonemKapali(f"{donem} dışına taşan satır var (son {son.date()})")
        if h is not None and f"bitis{h}" in D and (pd.to_datetime(D[f"bitis{h}"]) > son).any():
            raise DonemKapali(f"{donem}: etiket penceresi dönem sonunu aşan satır var (h={h})")


def kilit_icerigi(veri_tanimi: Dict[str, str]) -> Dict[str, Any]:
    """BAĞIMSIZ açılmadan önce sabitlenecek her şeyin sha256'sı: kod (K56 + kullanılan K55 modülleri), ön kayıt, hipotez kaydı, eşik sözlüğü, veri tanımları."""
    from . import mekanizma as M
    from K55.ortak import AYARLAR
    esik = {"K56": {"MEKANIK_ORAN": M.MEKANIK_ORAN, "KISMI_ORAN": M.KISMI_ORAN, "ANLAMSIZ_D": M.ANLAMSIZ_D, "SPEK_UYUM": M.SPEK_UYUM}, "K55": AYARLAR}
    try:
        from . import faz1_yerel as F1
        esik["K56_F1"] = F1.ESIKLER
    except Exception:
        pass
    return {"kod_sha": kod_sha(), "onkayit_sha": onkayit_sha(), "hipotez_sha": sha256_metin(M.hipotez_tablosu().drop(columns=["surum"]).to_csv(index=False)),
            "esik_sha": sha256_metin(json.dumps(esik, sort_keys=True, default=str)), "esikler": esik, "veri_tanimi": veri_tanimi}


def bagimsiz_kilit_dogrula(klasor: Optional[str]) -> None:
    y = os.path.join(klasor or REPO_CIKTI, BAGIMSIZ_KILIT)
    if not os.path.exists(y):
        raise DonemKapali(f"kilit dosyası yok: {y}")
    k = json.load(open(y, encoding="utf-8")); simdi = kilit_icerigi(k.get("veri_tanimi", {}))
    for a in ("kod_sha", "onkayit_sha", "hipotez_sha", "esik_sha"):
        if k.get(a) != simdi.get(a):
            raise DonemKapali(f"kilit tutmuyor: {a} değişmiş; BAĞIMSIZ açılamaz")
    vt = k.get("veri_tanimi", {}); yeni = veri_tanimi_hesapla(vt.get("panel_yol", ""), vt.get("olay_yol", ""), evren=True)   # açılış anında yeniden hesap
    for a in ("panel_sha", "olay_sha", "evren_surum"):
        if not vt.get(a) or vt.get(a) != yeni.get(a):
            raise DonemKapali(f"kilit tutmuyor: veri tanımı {a} değişmiş ya da hesaplanamadı; BAĞIMSIZ açılamaz")


def veri_tanimi_hesapla(panel_yol: str, olay_yol: str, evren: bool = True) -> Dict[str, str]:
    """BAĞIMSIZ kilidinin veri tanımı: panel ve olay tablosu sha256 + K55 evren sürümü (evren=True: K55 evren_kur ağ kapalı, ~3 dk)."""
    out = {"panel_yol": panel_yol, "olay_yol": olay_yol, "panel_sha": sha256_dosya(panel_yol) if os.path.exists(panel_yol) else "",
           "olay_sha": sha256_dosya(olay_yol) if os.path.exists(olay_yol) else "", "donem": "K55 DONEM (değişmedi)", "kesif_satirlari": "K55_VARYANTLAR KEŞİF ölçütü (125)"}
    if evren:
        from K55.evren import evren_kur
        from K55.ortak import K55Ayar, veri_sha
        A55 = K55Ayar(veri=K56Ayar().veri, cikti=os.path.dirname(os.path.dirname(panel_yol)) or "/tmp", k54=K56Ayar().abd, isci=1)
        out["evren_surum"] = evren_kur(A55, veri_sha(A55), network=False)["surum"]
    return out
