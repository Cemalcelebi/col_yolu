"""KASA — mühürlü veri blokları ile ileri test aracı, tek dosya (21 Kasım 2026; iş tanımı arastirma_cikti/kasa/KASA_IS_TANIMI.md).

Cemal (21 Kas 2026): "veriyi aylık / 3 aylık gruplara böl, şifreli olsun, şifre sende olsun; alt model eski veriyle test etsin, sonrası
elinde olmasın; sızma olmaz." + "bunu kullanmak istiyorum."

DÜZEN
  kur       X25519 anahtar çifti. AÇIK anahtar arastirma_cikti/kasa/kasa_acik_anahtar.pem (repoya girer; mühürlemeye yeter). GİZLİ anahtar
            yalnız --gizli (ya da KASA_GIZLI) ile verilen yola yazılır: repo / scratchpad / kasa dizini DIŞI, chmod 600, varsa üzerine yazılmaz.
            Gizli yol hiçbir çıktıya, loga, manifeste, deftere yazılmaz. Bu dosyada varsayılan gizli yol YOKTUR.
  muhurle   --kesik T: kaynak V_*.pkl dosyalarından tarih <= T satırlar AYNI BİÇİMDE <cikti>/acik/<dosya>.pkl'ye (alt modele verilen tek veri);
            T'den sonraki satırlar takvim çeyreği (ya da ay) bloklarına bölünür, her blok açık anahtarla şifrelenir
            (<cikti>/muhurlu/<dosya>_<blok>.kasa). Manifest (arastirma_cikti/kasa/KASA_MANIFEST.json): blok, satır, sembol, tarih aralığı,
            şifreli dosya sha256, düz metin sha256, açık kısım sha256; getiri / fiyat İÇERMEZ.  --ekle: bugünden sonra gelen yeni veri,
            manifestteki son tarihten sonraki satırlar yeni bloklar olarak doğrudan mühürlenir (açık kısma dokunulmaz).
  ac        --blok B --hipotez H --onkayit Y: KASA_GIZLI zorunlu. KAPI: (1) ön kayıt git'e işlenmiş ve değişmemiş, IZ_KARNE kontrol tablosu dolu;
            (2) ön kayıtta 'KASA_HIPOTEZ: H' ve en az bir 'KASA_KOD: <yol> <sha256>' satırı; kod dosyası şimdi aynı sha'da ve git'e işlenmiş;
            (3) (mühür, blok, hipotez) KASA_DEFTERI'nde daha önce açılmamış (tek kullanım); (4) bloklar sırayla açılır (aradaki atlanamaz).
            Başka bir hipotez için zaten açılmış bloğu yeni hipotez ancak ön kaydı o bloğun İLK açılışından ÖNCE işlenmişse kullanabilir
            (o zaman veri değişmez, yalnız defter satırı yazılır); sonra yazılmış ön kayıt kör değildir, durur.
            Açınca blok <cikti>/acik/ verisine eklenir ve arastirma_cikti/kasa/KASA_DEFTERI.md'ye satır yazılır (UTC, mühür, blok, hipotez,
            ön kayıt, ön kayıt commit, kod sha, açan, tür). Defter ana model tarafından commit edilir.
  denetim   <pkl / csv ...> [--kesik T]: dosyalardaki en geç tarihi bulur; açık kesikten (varsayılan <cikti>/acik/KASA_DURUM.json) büyükse
            HATA ile durur (çıkış kodu 2). Ölçüm modülleri koşudan önce kasa_kapisi(veri_yolu, kesik) çağırır.
  durum     açık kesik, mühürlü bloklar, defter özeti.
  say       --kesik T: şifrelemeden kuru sayım (dosya x blok satır / sembol / tarih aralığı tablosu).

ŞİFRELEME: hibrit ECIES. Her blok için geçici X25519 anahtarı, alıcı açık anahtarla ECDH, HKDF-SHA256 (RFC 5869), AES-256-GCM (cryptography
kütüphanesi; başlık AAD). cryptography yoksa openssl CLI: aynı X25519 + HKDF, AES-256-CBC + HMAC-SHA256 (şifrele-sonra-MAC).
Anahtar PEM biçimleri (PKCS8 / SPKI) iki yolda ortaktır. KASA_PAROLA ortam değişkeni varsa gizli anahtar PEM'i parolayla şifrelenir.

SINIR: kasa fiziksel engel değil SÜREÇ KAPISIDIR. Aynı fiyatlar islenmis-veri dalında ve Yahoo'da açık durur; alt modele yalnız
<cikti>/acik verilir + denetim komutu + tek kullanım defteri. Gerçek kör veri bugünden sonra gelen veridir (muhurle --ekle).

Komut:  python KASA.py kur --gizli <yol>          python KASA.py muhurle --kesik 2025-12-31 --cikti /tmp/kasa
        python KASA.py ac --blok 2026Q1 --hipotez <kod> --onkayit <yol>
        python KASA.py denetim /tmp/kasa/acik/V_ABD.pkl         python KASA.py durum         python KASA.py say --kesik 2025-12-31
Colab:  exec(open('KASA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Test:   python test_kasa.py (yalnız sentetik veri)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_KS = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import getpass  # noqa: E402
import hashlib  # noqa: E402
import hmac  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import struct  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_KS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_KS not in sys.path:
    sys.path.insert(0, KOK_KS)

kslog = logging.getLogger("col.kasa")
if not kslog.handlers:
    _ks_h = logging.StreamHandler(sys.stderr)
    _ks_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kasa: %(message)s", "%H:%M:%S"))
    kslog.addHandler(_ks_h)
    kslog.setLevel(logging.INFO)
    kslog.propagate = False

KASA_SURUM = "KASA v1 (21 Kasım 2026)"
KS_CIKTI = os.path.join(KOK_KS, "arastirma_cikti", "kasa")
KS_YOL = {
    "acik_anahtar": os.path.join(KS_CIKTI, "kasa_acik_anahtar.pem"),
    "manifest": os.path.join(KS_CIKTI, "KASA_MANIFEST.json"),
    "defter": os.path.join(KS_CIKTI, "KASA_DEFTERI.md"),
    "kaynak": "/tmp/veri",
    "dizin": os.environ.get("KASA_DIZIN", "/tmp/kasa"),
}
KS_DOSYALAR = ("V_ABD.pkl", "V_AVR.pkl", "V_BIST.pkl")
KS_BLOK_TIP = {"ceyrek": "Q", "ay": "M"}
KS_MAGIC = b"KASA1"
KS_ALG_GCM = "X25519-HKDF-SHA256-AES256GCM"
KS_ALG_CBC = "X25519-HKDF-SHA256-AES256CBC-HMACSHA256"
KS_DURUM_AD = "KASA_DURUM.json"
KS_DEFTER_BASLIK = ["UTC", "Mühür", "Blok", "Hipotez", "Ön kayıt", "Ön kayıt commit", "Kod sha", "Açan", "Tür"]
KS_TARIH_AD = re.compile(r"(tarih|date|gun|gün|zaman|time|giris|giriş|cikis|çıkış|^t$|^dt$)", re.I)
KS_ISO = re.compile(r"^\s*\d{4}-\d{2}-\d{2}")


class KasaHata(RuntimeError):
    """KASA kapısı ya da işlemi durdu (açıklama mesajda; gizli anahtar yolu mesajda GEÇMEZ)."""


# ================================================================ 0) YARDIMCILAR
def _utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha_bayt(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    try:
        with open(yol, "rb") as f:
            for parca in iter(lambda: f.read(1 << 20), b""):
                h.update(parca)
    except OSError as ex:
        raise KasaHata(f"dosya okunamadı: {os.path.basename(yol)} ({ex.strerror})")
    return h.hexdigest()


def _atomik_yaz(yol: str, veri: bytes, kip: int = 0o644) -> None:
    kl = os.path.dirname(os.path.abspath(yol)) or "."
    os.makedirs(kl, exist_ok=True)
    fd, gec = tempfile.mkstemp(prefix=".kasa_", dir=kl)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(veri); f.flush(); os.fsync(f.fileno())
        os.chmod(gec, kip)
        os.replace(gec, yol)
    except BaseException:
        try:
            os.unlink(gec)
        except OSError:
            pass
        raise


def _json_yaz(yol: str, obj: Any) -> None:
    _atomik_yaz(yol, (json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode("utf-8"))


def _json_oku(yol: str, ad: str) -> Any:
    if not os.path.exists(yol):
        raise KasaHata(f"{ad} yok: {yol}")
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as ex:
        raise KasaHata(f"{ad} okunamadı ({yol}): {ex}")


def _ts(x: Any) -> pd.Timestamp:
    try:
        t = pd.Timestamp(x)
    except (ValueError, TypeError) as ex:
        raise KasaHata(f"tarih anlaşılmadı: {x!r} ({ex})")
    if t is pd.NaT or pd.isna(t):
        raise KasaHata(f"tarih anlaşılmadı: {x!r}")
    if t.tzinfo is not None:
        t = t.tz_convert(None)
    return t.normalize()


def _gun(t: pd.Timestamp) -> str:
    return pd.Timestamp(t).strftime("%Y-%m-%d")


def _git(args: List[str], kl: str) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["git", "-C", kl] + args, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise KasaHata(f"git çalıştırılamadı ({ex})")


def _git_islenmis(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı. Döner: commit, commit zamanı (UTC ISO)."""
    if not os.path.exists(yol):
        raise KasaHata(f"dosya yok: {yol}")
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    r = _git(["log", "-1", "--format=%H %ct", "--", ad], kl)
    if r.returncode != 0 or not r.stdout.strip():
        raise KasaHata(f"git'e işlenmemiş: {yol} (önce commit)")
    d = _git(["status", "--porcelain", "--", ad], kl)
    if d.returncode != 0 or d.stdout.strip():
        raise KasaHata(f"git'e işlendikten sonra değişmiş: {yol} ({(d.stdout or d.stderr).strip()})")
    h, z = r.stdout.strip().split(" ", 1)
    zt = _dt.datetime.fromtimestamp(int(z), _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"commit": h, "commit_utc": zt}


def _git_kok(yol: str) -> str:
    r = _git(["rev-parse", "--show-toplevel"], os.path.dirname(os.path.abspath(yol)))
    if r.returncode != 0 or not r.stdout.strip():
        raise KasaHata(f"git deposu bulunamadı: {yol}")
    return r.stdout.strip()


def _icinde(yol: str, kok: str) -> bool:
    a, k = os.path.realpath(yol), os.path.realpath(kok)
    try:
        return os.path.commonpath([a, k]) == k
    except ValueError:
        return False


# ================================================================ 1) GİZLİ ANAHTAR YOLU
def _gizli_yol_ortam() -> str:
    """Gizli anahtar yolu YALNIZ KASA_GIZLI ortam değişkeninden (varsayılan yok). Yol hiçbir mesaja yazılmaz."""
    y = os.environ.get("KASA_GIZLI", "").strip()
    if not y:
        raise KasaHata("KASA_GIZLI ortam değişkeni yok: gizli anahtar yolu yalnız buradan okunur (varsayılan yol yoktur)")
    return y


def _gizli_yol_denetle(yol: str, yeni: bool, yasak_kokler: Optional[List[str]] = None) -> None:
    """Gizli anahtar repo, scratchpad (/tmp/claude-*), kasa dizini ya da çıktı klasörü İÇİNDE olamaz. Mesajlarda yol geçmez."""
    yasak = [KOK_KS, KS_CIKTI, KS_YOL["dizin"]] + list(yasak_kokler or [])
    if any(_icinde(yol, k) for k in yasak if k):
        raise KasaHata("gizli anahtar yolu repo / kasa dizini / çıktı klasörü içinde olamaz (yol gizli; mesajda yazılmaz)")
    if "/tmp/claude-" in os.path.realpath(yol) or "/scratchpad" in os.path.realpath(yol):
        raise KasaHata("gizli anahtar yolu scratchpad içinde olamaz (yol gizli; mesajda yazılmaz)")
    if yeni:
        if os.path.exists(yol):
            raise KasaHata("gizli anahtar dosyası zaten var; üzerine yazılmaz (yol gizli; mesajda yazılmaz)")
        if not os.path.isdir(os.path.dirname(os.path.abspath(yol))):
            raise KasaHata("gizli anahtarın klasörü yok; önce klasörü kur (chmod 700 önerilir)")
    else:
        if not os.path.isfile(yol):
            raise KasaHata("KASA_GIZLI'nin gösterdiği gizli anahtar dosyası yok (yol gizli; mesajda yazılmaz)")
        kip = os.stat(yol).st_mode & 0o077
        if kip:
            raise KasaHata("gizli anahtar dosyası başkalarınca okunabilir (chmod 600 gerekir)")


# ================================================================ 2) ŞİFRELEME (X25519 + HKDF + AES)
def _arka_sec(arka: Optional[str] = None) -> str:
    arka = arka or os.environ.get("KASA_ARKA", "").strip() or None
    if arka in (None, "", "otomatik"):
        try:
            import cryptography  # noqa: F401
            return "cryptography"
        except ImportError:
            arka = "openssl"
    if arka == "cryptography":
        try:
            import cryptography  # noqa: F401
        except ImportError:
            raise KasaHata("cryptography kütüphanesi yok (KASA_ARKA=openssl kullan)")
        return arka
    if arka == "openssl":
        if not shutil.which("openssl"):
            raise KasaHata("openssl CLI yok ve cryptography kütüphanesi yok: şifreleme yapılamaz")
        return arka
    raise KasaHata(f"bilinmeyen şifreleme arka ucu: {arka}")


def _hkdf(ikm: bytes, tuz: bytes, bilgi: bytes, uzunluk: int) -> bytes:
    """RFC 5869 HKDF-SHA256."""
    prk = hmac.new(tuz or b"\x00" * 32, ikm, hashlib.sha256).digest()
    out, t, i = b"", b"", 1
    while len(out) < uzunluk:
        t = hmac.new(prk, t + bilgi + bytes([i]), hashlib.sha256).digest()
        out += t; i += 1
    return out[:uzunluk]


def _ossl(args: List[str], girdi: Optional[bytes] = None, ad: str = "openssl") -> bytes:
    try:
        r = subprocess.run(["openssl"] + args, input=girdi, capture_output=True, timeout=600, env=dict(os.environ))
    except (OSError, subprocess.SubprocessError) as ex:
        raise KasaHata(f"{ad}: openssl çalıştırılamadı ({ex})")
    if r.returncode != 0:
        hata = r.stderr.decode("utf-8", "replace").strip().splitlines()
        son = hata[-1] if hata else str(r.returncode)
        for x in args + [os.environ.get("KASA_GIZLI", "")]:   # dosya yolları (gizli anahtar dahil) hata mesajına sızmaz
            if x and os.sep in x:
                son = son.replace(x, "<yol>").replace(os.path.basename(x), "<dosya>")
        raise KasaHata(f"{ad}: openssl hata verdi ({son})")
    return r.stdout


def _parola_cr() -> Optional[bytes]:
    p = os.environ.get("KASA_PAROLA")
    return p.encode("utf-8") if p else None


def ks_anahtar_uret(arka: Optional[str] = None) -> Tuple[bytes, bytes]:
    """(gizli PEM PKCS8, açık PEM SPKI). KASA_PAROLA varsa gizli PEM parolayla şifreli."""
    arka = _arka_sec(arka)
    if arka == "cryptography":
        from cryptography.hazmat.primitives import serialization as S
        from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
        g = X25519PrivateKey.generate(); p = _parola_cr()
        sif = S.BestAvailableEncryption(p) if p else S.NoEncryption()
        gizli = g.private_bytes(S.Encoding.PEM, S.PrivateFormat.PKCS8, sif)
        acik = g.public_key().public_bytes(S.Encoding.PEM, S.PublicFormat.SubjectPublicKeyInfo)
        return gizli, acik
    ek = ["-aes-256-cbc", "-pass", "env:KASA_PAROLA"] if os.environ.get("KASA_PAROLA") else []
    gizli = _ossl(["genpkey", "-algorithm", "X25519"] + ek, ad="anahtar üretimi")
    with tempfile.TemporaryDirectory(prefix="kasa_") as td:
        gy = os.path.join(td, "g.pem")
        fd = os.open(gy, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(gizli)
        acik = _ossl(["pkey", "-in", gy, "-pubout"] + (["-passin", "env:KASA_PAROLA"] if ek else []), ad="açık anahtar")
    return gizli, acik


def _acik_der(acik_pem: bytes) -> bytes:
    try:
        from cryptography.hazmat.primitives import serialization as S
        k = S.load_pem_public_key(acik_pem)
        return k.public_bytes(S.Encoding.DER, S.PublicFormat.SubjectPublicKeyInfo)
    except ImportError:
        return _ossl(["pkey", "-pubin", "-outform", "DER"], girdi=acik_pem, ad="açık anahtar")
    except ValueError as ex:
        raise KasaHata(f"açık anahtar okunamadı: {ex}")


def ks_parmak_izi(acik_pem: bytes) -> str:
    """Açık anahtar parmak izi = sha256(DER SPKI)."""
    return _sha_bayt(_acik_der(acik_pem))


def _der_pem(der: bytes) -> bytes:
    import base64
    b = base64.encodebytes(der).replace(b"\n", b"")
    satir = b"\n".join(b[i:i + 64] for i in range(0, len(b), 64))
    return b"-----BEGIN PUBLIC KEY-----\n" + satir + b"\n-----END PUBLIC KEY-----\n"


def _gizli_acik_der(gizli_yol: str, arka: str) -> bytes:
    if arka == "cryptography":
        from cryptography.hazmat.primitives import serialization as S
        try:
            with open(gizli_yol, "rb") as f:
                g = S.load_pem_private_key(f.read(), password=_parola_cr())
        except (ValueError, TypeError) as ex:
            raise KasaHata(f"gizli anahtar okunamadı (parola? KASA_PAROLA): {type(ex).__name__}")
        except OSError as ex:
            raise KasaHata(f"gizli anahtar okunamadı ({ex.strerror})")
        return g.public_key().public_bytes(S.Encoding.DER, S.PublicFormat.SubjectPublicKeyInfo)
    ek = ["-passin", "env:KASA_PAROLA"] if os.environ.get("KASA_PAROLA") else ["-passin", "pass:"]
    return _ossl(["pkey", "-in", gizli_yol, "-pubout", "-outform", "DER"] + ek, ad="gizli anahtar")


def _ossl_derive(inkey_yol: str, peer_pem: bytes, parola: bool) -> bytes:
    with tempfile.TemporaryDirectory(prefix="kasa_") as td:
        py = os.path.join(td, "peer.pem")
        with open(py, "wb") as f:
            f.write(peer_pem)
        ek = ["-passin", "env:KASA_PAROLA"] if parola else []
        return _ossl(["pkeyutl", "-derive", "-inkey", inkey_yol, "-peerkey", py] + ek, ad="ECDH")


def _paket(baslik: Dict[str, Any]) -> bytes:
    hb = json.dumps(baslik, sort_keys=True, ensure_ascii=True).encode("ascii")
    return KS_MAGIC + struct.pack(">I", len(hb)) + hb


def _paket_coz(blob: bytes) -> Tuple[Dict[str, Any], bytes, bytes]:
    if len(blob) < 9 or blob[:5] != KS_MAGIC:
        raise KasaHata("kasa dosyası biçimi tanınmadı (KASA1 imzası yok)")
    n = struct.unpack(">I", blob[5:9])[0]
    on = blob[:9 + n]
    try:
        baslik = json.loads(blob[9:9 + n].decode("ascii"))
    except (UnicodeDecodeError, ValueError) as ex:
        raise KasaHata(f"kasa başlığı bozuk: {ex}")
    return baslik, on, blob[9 + n:]


def ks_sifrele(veri: bytes, acik_pem: bytes, ust: Dict[str, Any], arka: Optional[str] = None) -> bytes:
    """Hibrit ECIES: geçici X25519 + ECDH + HKDF-SHA256 + AES-256-GCM (cryptography) / AES-256-CBC+HMAC (openssl). Başlık AAD / MAC'e girer."""
    arka = _arka_sec(arka)
    alici_der = _acik_der(acik_pem)
    if arka == "cryptography":
        from cryptography.hazmat.primitives import serialization as S
        from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
        alici = S.load_der_public_key(alici_der)
        gec = X25519PrivateKey.generate()
        ortak = gec.exchange(alici)
        gec_der = gec.public_key().public_bytes(S.Encoding.DER, S.PublicFormat.SubjectPublicKeyInfo)
        baslik = dict(ust, alg=KS_ALG_GCM, gecici=gec_der.hex(), nonce=os.urandom(12).hex())
        anahtar = _hkdf(ortak, hashlib.sha256(gec_der + alici_der).digest(), b"KASA-v1|" + KS_ALG_GCM.encode(), 32)
        on = _paket(baslik)
        return on + AESGCM(anahtar).encrypt(bytes.fromhex(baslik["nonce"]), veri, on)
    with tempfile.TemporaryDirectory(prefix="kasa_") as td:
        gy = os.path.join(td, "e.pem")
        pem = _ossl(["genpkey", "-algorithm", "X25519"], ad="geçici anahtar")
        fd = os.open(gy, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as f:
            f.write(pem)
        gec_der = _ossl(["pkey", "-in", gy, "-pubout", "-outform", "DER"], ad="geçici anahtar")
        ortak = _ossl_derive(gy, _der_pem(alici_der), parola=False)
    iv = os.urandom(16)
    baslik = dict(ust, alg=KS_ALG_CBC, gecici=gec_der.hex(), iv=iv.hex())
    km = _hkdf(ortak, hashlib.sha256(gec_der + alici_der).digest(), b"KASA-v1|" + KS_ALG_CBC.encode(), 64)
    sif = _ossl(["enc", "-aes-256-cbc", "-K", km[:32].hex(), "-iv", iv.hex()], girdi=veri, ad="AES-CBC")
    on = _paket(baslik)
    etiket = hmac.new(km[32:], on + sif, hashlib.sha256).digest()
    return on + sif + etiket


def ks_coz(blob: bytes, gizli_yol: str, arka: Optional[str] = None) -> Tuple[Dict[str, Any], bytes]:
    """Kasa paketini gizli anahtarla çözer. Bütünlük (GCM etiketi / HMAC) tutmazsa KasaHata."""
    arka = _arka_sec(arka)
    baslik, on, govde = _paket_coz(blob)
    try:
        gec_der = bytes.fromhex(baslik["gecici"])
    except (KeyError, ValueError):
        raise KasaHata("kasa başlığında geçici anahtar yok")
    alici_der = _gizli_acik_der(gizli_yol, arka)
    tuz = hashlib.sha256(gec_der + alici_der).digest()
    alg = baslik.get("alg")
    if arka == "cryptography":
        from cryptography.hazmat.primitives import serialization as S
        try:
            with open(gizli_yol, "rb") as f:
                g = S.load_pem_private_key(f.read(), password=_parola_cr())
        except (ValueError, TypeError, OSError) as ex:
            raise KasaHata(f"gizli anahtar okunamadı: {type(ex).__name__}")
        ortak = g.exchange(S.load_der_public_key(gec_der))
    else:
        ortak = _ossl_derive(gizli_yol, _der_pem(gec_der), parola=bool(os.environ.get("KASA_PAROLA")))
    if alg == KS_ALG_GCM:
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            from cryptography.exceptions import InvalidTag
        except ImportError:
            raise KasaHata("bu blok AES-GCM ile mühürlü; çözmek için cryptography kütüphanesi gerekir")
        anahtar = _hkdf(ortak, tuz, b"KASA-v1|" + KS_ALG_GCM.encode(), 32)
        try:
            return baslik, AESGCM(anahtar).decrypt(bytes.fromhex(baslik["nonce"]), govde, on)
        except InvalidTag:
            raise KasaHata("blok çözülemedi: yanlış anahtar ya da bozulmuş / değiştirilmiş dosya (GCM etiketi tutmadı)")
    if alg == KS_ALG_CBC:
        if len(govde) < 32:
            raise KasaHata("kasa gövdesi kısa")
        km = _hkdf(ortak, tuz, b"KASA-v1|" + KS_ALG_CBC.encode(), 64)
        sif, etiket = govde[:-32], govde[-32:]
        if not hmac.compare_digest(hmac.new(km[32:], on + sif, hashlib.sha256).digest(), etiket):
            raise KasaHata("blok çözülemedi: yanlış anahtar ya da bozulmuş / değiştirilmiş dosya (HMAC tutmadı)")
        return baslik, _ossl(["enc", "-d", "-aes-256-cbc", "-K", km[:32].hex(), "-iv", baslik["iv"]], girdi=sif, ad="AES-CBC çöz")
    raise KasaHata(f"bilinmeyen kasa algoritması: {alg}")


# ================================================================ 3) VERİ BÖLME
def _dosya_adlari(dosyalar: List[str]) -> List[str]:
    """--dosya yalnız kaynak klasördeki DOSYA ADI olabilir (yol değil): açık kısım <cikti>/acik/<ad> olarak yazılır, kaynağın üzerine asla."""
    for ad in dosyalar:
        if not ad or os.path.basename(ad) != ad or ad in (".", "..") or not ad.endswith(".pkl"):
            raise KasaHata(f"--dosya yalnız klasördeki .pkl dosya adı olabilir (yol değil): {ad!r}")
    if len(set(dosyalar)) != len(dosyalar):
        raise KasaHata(f"--dosya tekrarlı: {dosyalar}")
    return list(dosyalar)


def _sozluk_yukle(yol: str) -> Tuple[Dict[str, pd.DataFrame], List[str]]:
    """V_*.pkl -> ({sembol: DataFrame}, atlanan üst anahtarlar). {'veri': {...}} sarmalı açılır; DataFrame olmayan değer varsa durur."""
    if not os.path.exists(yol):
        raise KasaHata(f"kaynak yok: {yol}")
    try:
        ham = pd.read_pickle(yol)
    except Exception as ex:   # bozuk pickle: hangi dosya olduğu söylenir
        raise KasaHata(f"kaynak okunamadı ({yol}): {type(ex).__name__}: {ex}")
    atla: List[str] = []
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        atla = sorted(str(k) for k in ham if k != "veri")
        ham = ham["veri"]
    if not isinstance(ham, dict):
        raise KasaHata(f"{os.path.basename(yol)}: beklenen {{sembol: DataFrame}} sözlüğü değil ({type(ham).__name__})")
    kotu = [str(k) for k, v in ham.items() if not isinstance(v, pd.DataFrame)]
    if kotu:
        raise KasaHata(f"{os.path.basename(yol)}: DataFrame olmayan değerler var ({kotu[:5]}); fail-closed")
    return ham, atla


def _gun_ix(d: pd.DataFrame) -> pd.DatetimeIndex:
    try:
        ix = pd.DatetimeIndex(d.index)
    except (TypeError, ValueError) as ex:
        raise KasaHata(f"tarih dizini değil: {ex}")
    if ix.tz is not None:
        ix = ix.tz_convert(None)
    return ix.normalize()


def _blok_ad(per: pd.Period, tip: str) -> str:
    return f"{per.year}Q{per.quarter}" if tip == "ceyrek" else f"{per.year}-{per.month:02d}"


def ks_bol(V: Dict[str, pd.DataFrame], kesik: Any, tip: str = "ceyrek", taban: Optional[Any] = None
           ) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Dict[str, pd.DataFrame]], Dict[str, int]]:
    """V'yi böler: (açık {sembol: tarih <= kesik}, bloklar {blok_ad: {sembol: satırlar}}, sayaç).
    taban verilirse (muhurle --ekle) yalnız tarih > taban satırlar bloklara girer; açık kısım boş döner.
    Her seri önce tarihe göre kararlı sıralanır (birleşim özgünle eşit olsun diye). Kesikten önce satırı olmayan sembol açık kısma GİRMEZ."""
    if tip not in KS_BLOK_TIP:
        raise KasaHata(f"blok tipi ceyrek | ay olmalı: {tip}")
    k = _ts(kesik if taban is None else taban)
    acik: Dict[str, pd.DataFrame] = {}; bloklar: Dict[str, Dict[str, pd.DataFrame]] = {}
    say = {"sirasiz": 0, "bos": 0}
    for s, d in V.items():
        if len(d) == 0:
            say["bos"] += 1; continue
        ix = _gun_ix(d)
        if not ix.is_monotonic_increasing:
            say["sirasiz"] += 1
            sira = np.argsort(ix.values, kind="mergesort"); d = d.iloc[sira]; ix = ix[sira]
        m = np.asarray(ix <= k)
        if taban is None and m.any():
            acik[s] = d.iloc[np.flatnonzero(m)]
        if (~m).any():
            sonra = np.flatnonzero(~m)
            per = ix[sonra].to_period(KS_BLOK_TIP[tip])
            for p in pd.unique(per):
                sec = sonra[np.asarray(per == p)]
                bloklar.setdefault(_blok_ad(p, tip), {})[s] = d.iloc[sec]
    return acik, bloklar, say


def _blok_sira(ad: str) -> Tuple[int, int, int]:
    """'2026Q1' / '2026Q1-2' / '2026-01' / '2026-01-2' -> sıralama anahtarı (yıl, ay başı, parça)."""
    m = re.fullmatch(r"(\d{4})Q([1-4])(?:-(\d+))?", ad)
    if m:
        return int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, int(m.group(3) or 1)
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d+))?", ad)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)
    raise KasaHata(f"blok adı tanınmadı: {ad}")


def _per_bitis(ad: str, tip: str) -> pd.Timestamp:
    y, a, _ = _blok_sira(ad)
    p = pd.Period(year=y, month=a, freq="M")
    p = p.asfreq("Q") if tip == "ceyrek" else p
    return pd.Timestamp(p.end_time).normalize()


def _satir(sozluk: Dict[str, pd.DataFrame]) -> int:
    return int(sum(len(v) for v in sozluk.values()))


def _aralik(sozluk: Dict[str, pd.DataFrame]) -> Tuple[Optional[str], Optional[str]]:
    ilk = [ _gun_ix(v).min() for v in sozluk.values() if len(v)]
    son = [_gun_ix(v).max() for v in sozluk.values() if len(v)]
    return (_gun(min(ilk)) if ilk else None, _gun(max(son)) if son else None)


def ks_say(kesik: Any, tip: str = "ceyrek", kaynak: Optional[str] = None, dosyalar: Optional[List[str]] = None) -> pd.DataFrame:
    """Kuru sayım (şifreleme YOK, hiçbir dosya yazılmaz): dosya x blok -> satır, sembol, ilk, son; 'ACIK' satırı açık kısım."""
    kaynak = kaynak or KS_YOL["kaynak"]; dosyalar = _dosya_adlari(list(dosyalar or KS_DOSYALAR)); sat = []
    for ad in dosyalar:
        V, _ = _sozluk_yukle(os.path.join(kaynak, ad))
        acik, bloklar, sy = ks_bol(V, kesik, tip)
        i, s = _aralik(acik)
        sat.append({"dosya": ad, "blok": "ACIK", "satir": _satir(acik), "sembol": len(acik), "ilk": i, "son": s,
                    "kaynak_sembol": len(V), "sirasiz": sy["sirasiz"]})
        for b in sorted(bloklar, key=_blok_sira):
            i, s = _aralik(bloklar[b])
            sat.append({"dosya": ad, "blok": b, "satir": _satir(bloklar[b]), "sembol": len(bloklar[b]), "ilk": i, "son": s,
                        "kaynak_sembol": len(V), "sirasiz": sy["sirasiz"]})
        kslog.info("kuru sayım %s: açık %d satır, %d blok", ad, _satir(acik), len(bloklar))
    return pd.DataFrame(sat)


def ks_say_md(T: pd.DataFrame) -> str:
    s = ["| Dosya | Blok | Satır | Sembol | İlk | Son |", "|---|---|---:|---:|---|---|"]
    for r in T.itertuples():
        s.append(f"| {r.dosya} | {r.blok} | {r.satir:,} | {r.sembol:,} | {r.ilk or '-'} | {r.son or '-'} |".replace(",", "."))
    return "\n".join(s)


# ================================================================ 4) MÜHÜRLE
def _pickle_bayt(obj: Any) -> bytes:
    b = io.BytesIO(); pickle.dump(obj, b, protocol=pickle.HIGHEST_PROTOCOL); return b.getvalue()


def _acik_yaz(yol: str, V: Dict[str, pd.DataFrame]) -> str:
    b = _pickle_bayt(V); _atomik_yaz(yol, b); return _sha_bayt(b)


def ks_muhurle(kesik: Any, cikti: Optional[str] = None, tip: str = "ceyrek", kaynak: Optional[str] = None,
               dosyalar: Optional[List[str]] = None, acik_anahtar: Optional[str] = None, manifest: Optional[str] = None,
               uzerine: bool = False, arka: Optional[str] = None) -> Dict[str, Any]:
    """İlk mühür: açık kısım (<cikti>/acik) + şifreli bloklar (<cikti>/muhurlu) + manifest. Gizli anahtar GEREKMEZ."""
    cikti = cikti or KS_YOL["dizin"]; kaynak = kaynak or KS_YOL["kaynak"]; dosyalar = _dosya_adlari(list(dosyalar or KS_DOSYALAR))
    acik_anahtar = acik_anahtar or KS_YOL["acik_anahtar"]; manifest = manifest or KS_YOL["manifest"]
    k = _ts(kesik); arka = _arka_sec(arka)
    if not os.path.exists(acik_anahtar):
        raise KasaHata(f"açık anahtar yok: {acik_anahtar} (önce `python KASA.py kur`)")
    acik_pem = open(acik_anahtar, "rb").read(); iz = ks_parmak_izi(acik_pem)
    a_dir, m_dir = os.path.join(cikti, "acik"), os.path.join(cikti, "muhurlu")
    if not uzerine:
        if os.path.exists(manifest):
            raise KasaHata(f"manifest zaten var ({manifest}); yeni kasa için --uzerine, yeni veri için --ekle")
        for d in (a_dir, m_dir):
            if os.path.isdir(d) and os.listdir(d):
                raise KasaHata(f"{d} boş değil; --uzerine olmadan yazılmaz")
    else:
        for d in (a_dir, m_dir):
            if os.path.isdir(d):
                shutil.rmtree(d)
    os.makedirs(a_dir, exist_ok=True); os.makedirs(m_dir, exist_ok=True)
    simdi = _utc(); muhur_id = _sha_bayt(f"{_gun(k)}|{iz}|{simdi}".encode())[:16]
    M: Dict[str, Any] = {"surum": KASA_SURUM, "muhur_id": muhur_id, "olusturma_utc": simdi, "kesik": _gun(k), "blok_tipi": tip,
                         "acik_anahtar_sha256": iz, "kaynak_klasor": kaynak, "dosyalar": {}, "bloklar": [], "ekler": [],
                         "not": "Manifest getiri / fiyat içermez: yalnız satır, sembol, tarih aralığı ve sha256."}
    hazir: Dict[str, Tuple[Dict[str, pd.DataFrame], Dict[str, Dict[str, pd.DataFrame]], str]] = {}
    kaynak_son = None
    for ad in dosyalar:
        V, atla = _sozluk_yukle(os.path.join(kaynak, ad))
        acik, bloklar, sy = ks_bol(V, k, tip)
        _, son = _aralik(V)
        kaynak_son = max(kaynak_son, son) if kaynak_son and son else (son or kaynak_son)
        hazir[ad] = (acik, bloklar, son)
        M["dosyalar"][ad] = {"kaynak_sembol": len(V), "kaynak_satir": _satir(V), "kaynak_son": son, "atlanan_ust_anahtar": atla,
                             "sirasiz_seri": sy["sirasiz"], "bos_seri": sy["bos"]}
    if not kaynak_son or _ts(kaynak_son) <= k:
        raise KasaHata(f"kesik {_gun(k)} kaynaktaki en geç tarihten ({kaynak_son}) büyük ya da eşit: mühürlenecek blok yok")
    blok_son: Dict[str, str] = {}
    for ad, (_, bloklar, _) in hazir.items():
        for b, sz in bloklar.items():
            s = _aralik(sz)[1]
            blok_son[b] = max(blok_son.get(b, s), s)
    for ad, (acik, bloklar, son) in hazir.items():
        yol = os.path.join(a_dir, ad)
        sha = _acik_yaz(yol, acik)
        i, s = _aralik(acik)
        M["dosyalar"][ad].update({"acik_sha256": sha, "acik_satir": _satir(acik), "acik_sembol": len(acik), "acik_ilk": i, "acik_son": s})
        for b in sorted(bloklar, key=_blok_sira):
            M["bloklar"].append(_blok_muhurle(ad, b, bloklar[b], tip, acik_pem, m_dir, arka, blok_son[b], kaynak_son))
        kslog.info("%s: açık %d satır / %d sembol; %d blok mühürlendi", ad, _satir(acik), len(acik), len(bloklar))
    M["son_tarih"] = max(x["bitis"] for x in M["bloklar"])
    _json_yaz(manifest, M)
    _json_yaz(os.path.join(a_dir, KS_DURUM_AD), {"muhur_id": muhur_id, "kesik_ilk": _gun(k), "acik_kesik": _gun(k), "acilan": [],
                                                 "guncelleme_utc": simdi})
    kslog.info("mühür %s tamam: kesik %s, %d blok kaydı, manifest %s", muhur_id, _gun(k), len(M["bloklar"]), manifest)
    return M


def _blok_muhurle(ad: str, b: str, sz: Dict[str, pd.DataFrame], tip: str, acik_pem: bytes, m_dir: str, arka: str,
                  b_son: str, kaynak_son: str, baslangic: Optional[str] = None) -> Dict[str, Any]:
    duz = _pickle_bayt(sz)
    i, s = _aralik(sz)
    per_son = _per_bitis(b, tip)
    bitis = _gun(per_son) if _ts(kaynak_son) >= per_son else b_son
    stem = os.path.splitext(ad)[0]
    blob = ks_sifrele(duz, acik_pem, {"dosya": ad, "blok": b, "surum": KASA_SURUM}, arka)
    kyol = os.path.join(m_dir, f"{stem}_{b}.kasa")
    if os.path.exists(kyol):
        raise KasaHata(f"kasa dosyası zaten var: {kyol}")
    _atomik_yaz(kyol, blob, 0o644)
    return {"dosya": ad, "blok": b, "sira": list(_blok_sira(b)), "satir": _satir(sz), "sembol": len(sz), "ilk": i, "son": s,
            "baslangic": baslangic, "bitis": bitis, "kasa_dosya": os.path.basename(kyol), "sha256": _sha_bayt(blob),
            "duz_sha256": _sha_bayt(duz), "alg": json.loads(blob[9:9 + struct.unpack(">I", blob[5:9])[0]])["alg"]}


def ks_muhurle_ekle(cikti: Optional[str] = None, kaynak: Optional[str] = None, dosyalar: Optional[List[str]] = None,
                    acik_anahtar: Optional[str] = None, manifest: Optional[str] = None, arka: Optional[str] = None) -> Dict[str, Any]:
    """Yeni veri: manifestteki son tarihten (bütün dosyalarda ortak) sonraki satırlar yeni bloklar olarak mühürlenir.
    Dönem zaten mühürlüyse blok adı parça ekiyle (2026Q4-2) verilir. Açık kısma ve eski bloklara dokunulmaz."""
    cikti = cikti or KS_YOL["dizin"]; kaynak = kaynak or KS_YOL["kaynak"]
    acik_anahtar = acik_anahtar or KS_YOL["acik_anahtar"]; manifest = manifest or KS_YOL["manifest"]
    M = _json_oku(manifest, "manifest"); arka = _arka_sec(arka); tip = M["blok_tipi"]
    dosyalar = _dosya_adlari(list(dosyalar or M["dosyalar"].keys()))
    acik_pem = open(acik_anahtar, "rb").read()
    if ks_parmak_izi(acik_pem) != M["acik_anahtar_sha256"]:
        raise KasaHata("açık anahtar manifestteki parmak iziyle aynı değil")
    taban = _ts(M["son_tarih"]); m_dir = os.path.join(cikti, "muhurlu"); os.makedirs(m_dir, exist_ok=True)
    mevcut = {x["blok"] for x in M["bloklar"]}
    hazir = {}; sonlar: Dict[str, Optional[str]] = {}; kaynak_son = None; kayip = {}
    for ad in dosyalar:
        V, _ = _sozluk_yukle(os.path.join(kaynak, ad))
        _, bl, _ = ks_bol(V, None, tip, taban=taban)
        eski_son = M["dosyalar"].get(ad, {}).get("kaynak_son")
        if eski_son:
            kayip[ad] = int(sum(int(((_gun_ix(v) > _ts(eski_son)) & (_gun_ix(v) <= taban)).sum()) for v in V.values() if len(v)))
        _, son = _aralik(V)
        kaynak_son = max(kaynak_son, son) if kaynak_son and son else (son or kaynak_son)
        hazir[ad] = bl; sonlar[ad] = son
    if not kaynak_son or _ts(kaynak_son) <= taban:
        raise KasaHata(f"yeni veri yok: kaynaktaki en geç tarih {kaynak_son}, mühürlü son tarih {_gun(taban)}")
    ad_esle: Dict[str, str] = {}
    for bl in hazir.values():
        for b in bl:
            if b in ad_esle:
                continue
            ad_n, parca = b, 1
            while ad_n in mevcut:
                parca += 1; ad_n = f"{b}-{parca}"
            ad_esle[b] = ad_n
    blok_son: Dict[str, str] = {}
    for bl in hazir.values():
        for b, sz in bl.items():
            s = _aralik(sz)[1]; blok_son[b] = max(blok_son.get(b, s), s)
    yeni = []
    for ad, bl in hazir.items():
        for b in sorted(bl, key=_blok_sira):
            yeni.append(_blok_muhurle(ad, ad_esle[b], bl[b], tip, acik_pem, m_dir, arka, blok_son[b], kaynak_son,
                                      baslangic=_gun(taban + pd.Timedelta(days=1))))
    M["bloklar"].extend(yeni)
    M["son_tarih"] = max(x["bitis"] for x in M["bloklar"])
    for ad in dosyalar:
        M["dosyalar"].setdefault(ad, {})["kaynak_son"] = max(M["dosyalar"][ad].get("kaynak_son") or "", sonlar.get(ad) or "") or None
    M["ekler"].append({"utc": _utc(), "taban": _gun(taban), "yeni_blok": sorted({x["blok"] for x in yeni}, key=_blok_sira),
                       "satir": int(sum(x["satir"] for x in yeni)), "taban_oncesi_kayip_satir": kayip})
    _json_yaz(manifest, M)
    if any(kayip.values()):
        kslog.warning("ekle: mühürlü son tarihten önce kalan ama önceki mühürde olmayan satırlar mühürlenmedi: %s", kayip)
    kslog.info("ekle tamam: %d yeni blok kaydı (%s)", len(yeni), ", ".join(sorted({x['blok'] for x in yeni}, key=_blok_sira)))
    return M


# ================================================================ 5) DEFTER ve ÖN KAYIT KAPISI
def _defter_oku(yol: str) -> List[Dict[str, str]]:
    if not os.path.exists(yol):
        return []
    out = []
    for satir in open(yol, encoding="utf-8").read().splitlines():
        if not satir.startswith("| ") or satir.startswith("| UTC") or set(satir) <= set("|-: "):
            continue
        h = [x.strip() for x in satir.strip().strip("|").split("|")]
        if len(h) == len(KS_DEFTER_BASLIK):
            out.append(dict(zip(KS_DEFTER_BASLIK, h)))
    return out


def _defter_ekle(yol: str, kayit: Dict[str, str]) -> None:
    if not os.path.exists(yol):
        bas = ["# KASA DEFTERİ (tek kullanım kaydı; `python KASA.py ac` yazar, elle düzenlenmez)", "",
               "Her satır bir (mühür, blok, hipotez) açılışıdır. Aynı çift ikinci kez açılamaz; bloklar sırayla açılır.", "",
               "| " + " | ".join(KS_DEFTER_BASLIK) + " |", "|" + "---|" * len(KS_DEFTER_BASLIK)]
        _atomik_yaz(yol, ("\n".join(bas) + "\n").encode("utf-8"))
    sat = "| " + " | ".join(str(kayit.get(k, "")).replace("|", "/").replace("\n", " ") for k in KS_DEFTER_BASLIK) + " |\n"
    with open(yol, "a", encoding="utf-8") as f:
        f.write(sat); f.flush(); os.fsync(f.fileno())


_KS_HIP = re.compile(r"^\s*KASA_HIPOTEZ:\s*`?([A-Za-z0-9_.\-]+)`?\s*$", re.M)
_KS_KOD = re.compile(r"^\s*KASA_KOD:\s*`?([^\s`]+)`?\s+`?([0-9a-f]{64})`?\s*$", re.M)


def ks_onkayit_kapi(onkayit: str, hipotez: str, kontrol: bool = True) -> Dict[str, Any]:
    """Ön kayıt kapısı: git'e işlenmiş + değişmemiş; KASA_HIPOTEZ == hipotez; KASA_KOD satırlarındaki her kod dosyası şimdi aynı sha'da
    ve git'e işlenmiş; IZ_KARNE kontrol tablosu dolu (kontrol=True)."""
    if not re.fullmatch(r"[A-Za-z0-9_.\-]{1,64}", hipotez or ""):
        raise KasaHata(f"hipotez kodu geçersiz: {hipotez!r} (harf, rakam, _ . -; en çok 64)")
    g = _git_islenmis(onkayit)
    metin = open(onkayit, encoding="utf-8").read()
    h = _KS_HIP.findall(metin)
    if h != [hipotez]:
        raise KasaHata(f"ön kayıtta tek 'KASA_HIPOTEZ: {hipotez}' satırı yok (bulunan {h})")
    kodlar = _KS_KOD.findall(metin)
    if not kodlar:
        raise KasaHata("ön kayıtta 'KASA_KOD: <yol> <sha256>' satırı yok (kod sha zorunlu)")
    kok = _git_kok(onkayit); kd = []
    for yol, sha in kodlar:
        tam = yol if os.path.isabs(yol) else os.path.join(kok, yol)
        if not os.path.isfile(tam):
            raise KasaHata(f"ön kayıttaki kod dosyası yok: {yol}")
        simdi = _sha_dosya(tam)
        if simdi != sha:
            raise KasaHata(f"kod sha tutmuyor: {yol} ön kayıt {sha[:12]}…, şimdi {simdi[:12]}… (kod ön kayıttan sonra değişmiş)")
        _git_islenmis(tam)
        kd.append({"yol": yol, "sha256": sha})
    out = {"onkayit": os.path.relpath(os.path.abspath(onkayit), kok), "commit": g["commit"], "commit_utc": g["commit_utc"], "kod": kd}
    if kontrol:
        import IZ_KARNE as IK
        try:
            IK.ik_kontrol_kapisi(onkayit)
        except RuntimeError as ex:
            raise KasaHata(str(ex))
        out["kontrol"] = True
    return out


def _acan() -> str:
    a = os.environ.get("KASA_ACAN", "").strip()
    if a:
        return a
    r = _git(["config", "user.name"], KOK_KS)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    try:
        return getpass.getuser()
    except Exception:   # kullanıcı adı alınamazsa defter yine yazılır
        return "bilinmiyor"


# ================================================================ 6) AÇ
def _durum_oku(cikti: str) -> Dict[str, Any]:
    return _json_oku(os.path.join(cikti, "acik", KS_DURUM_AD), "açık kısım durumu (KASA_DURUM.json)")


def _blok_listesi(M: Dict[str, Any]) -> List[str]:
    return sorted({x["blok"] for x in M["bloklar"]}, key=_blok_sira)


def ks_ac(blok: str, hipotez: str, onkayit: str, cikti: Optional[str] = None, manifest: Optional[str] = None,
          defter: Optional[str] = None, kontrol: bool = True, arka: Optional[str] = None) -> Dict[str, Any]:
    """Bloğu açar (KASA_GIZLI zorunlu). Kapı geçmezse KasaHata; açık veriye hiçbir şey yazılmaz."""
    cikti = cikti or KS_YOL["dizin"]; manifest = manifest or KS_YOL["manifest"]; defter = defter or KS_YOL["defter"]
    gizli = _gizli_yol_ortam()
    M = _json_oku(manifest, "manifest"); D = _durum_oku(cikti)
    if D.get("muhur_id") != M["muhur_id"]:
        raise KasaHata(f"açık kısım başka bir mühüre ait ({D.get('muhur_id')} != {M['muhur_id']}); /tmp kasası yeniden kurulmalı")
    sira = _blok_listesi(M)
    if blok not in sira:
        raise KasaHata(f"blok mühürlü değil: {blok} (mühürlü: {', '.join(sira)})")
    satirlar = [r for r in _defter_oku(defter) if r["Mühür"] == M["muhur_id"]]
    if any(r["Blok"] == blok and r["Hipotez"] == hipotez for r in satirlar):
        raise KasaHata(f"({blok}, {hipotez}) daha önce açıldı: tek kullanım; ikinci açma DURDU")
    acilan_defter = sorted({r["Blok"] for r in satirlar}, key=_blok_sira)
    acilan = list(D.get("acilan", []))
    if acilan != acilan_defter:
        raise KasaHata(f"açık kısım defterle tutarsız (durum {acilan}, defter {acilan_defter}); /tmp kasası eski ya da defter commit "
                       "edilmemiş: önce tutarlılığı sağla")
    G = ks_onkayit_kapi(onkayit, hipotez, kontrol=kontrol)
    _gizli_yol_denetle(gizli, yeni=False)
    arka = _arka_sec(arka)
    if _sha_bayt(_gizli_acik_der(gizli, arka)) != M["acik_anahtar_sha256"]:
        raise KasaHata("gizli anahtar bu mühürün açık anahtarıyla eşleşmiyor")
    kayit = {"UTC": _utc(), "Mühür": M["muhur_id"], "Blok": blok, "Hipotez": hipotez, "Ön kayıt": G["onkayit"],
             "Ön kayıt commit": f"{G['commit'][:12]} ({G['commit_utc']})", "Kod sha": ",".join(k["sha256"][:12] for k in G["kod"]),
             "Açan": _acan()}
    if blok in acilan:
        ilk = min((r["UTC"] for r in satirlar if r["Blok"] == blok), default=None)
        if ilk is None or not G["commit_utc"] < ilk:
            raise KasaHata(f"{blok} başka hipotez için {ilk} tarihinde açıldı; bu ön kayıt ({G['commit_utc']}) açılıştan sonra işlenmiş: "
                           "kör değil, DURDU")
        kayit["Tür"] = "kayıt (veri zaten açık; ön kayıt ilk açılıştan önce)"
        _defter_ekle(defter, kayit)
        kslog.info("%s / %s: blok zaten açık, defter satırı yazıldı", blok, hipotez)
        return {"blok": blok, "hipotez": hipotez, "tur": "kayit", "acik_kesik": D["acik_kesik"]}
    beklenen = sira[len(acilan)] if len(acilan) < len(sira) else None
    if blok != beklenen:
        raise KasaHata(f"sıra atlama: açılacak sıradaki blok {beklenen}, istenen {blok}; aradaki blok atlanamaz")
    girdiler = [x for x in M["bloklar"] if x["blok"] == blok]
    a_dir, m_dir = os.path.join(cikti, "acik"), os.path.join(cikti, "muhurlu")
    yeni_V: Dict[str, Tuple[Dict[str, pd.DataFrame], int]] = {}
    for x in girdiler:
        kyol = os.path.join(m_dir, x["kasa_dosya"])
        if _sha_dosya(kyol) != x["sha256"]:
            raise KasaHata(f"kasa dosyası manifestle aynı değil: {x['kasa_dosya']} (değiştirilmiş?)")
        with open(kyol, "rb") as f:
            baslik, duz = ks_coz(f.read(), gizli, arka)
        if baslik.get("blok") != blok or baslik.get("dosya") != x["dosya"] or _sha_bayt(duz) != x["duz_sha256"]:
            raise KasaHata(f"çözülen blok manifestle tutmuyor: {x['kasa_dosya']}")
        sz = pickle.loads(duz)
        if _satir(sz) != x["satir"]:
            raise KasaHata(f"satır sayısı tutmuyor: {x['kasa_dosya']}")
        ay = os.path.join(a_dir, x["dosya"])
        V = yeni_V[x["dosya"]][0] if x["dosya"] in yeni_V else (_sozluk_yukle(ay)[0] if os.path.exists(ay) else {})
        n0 = _satir(V)
        for s, d in sz.items():
            V[s] = pd.concat([V[s], d]) if s in V else d
        yeni_V[x["dosya"]] = (V, n0 + x["satir"])
    for ad, (V, n) in yeni_V.items():
        if _satir(V) != n:
            raise KasaHata(f"birleşim satır sayısı tutmuyor: {ad}")
    for ad, (V, _) in yeni_V.items():   # hepsi hazır; şimdi yaz
        _acik_yaz(os.path.join(a_dir, ad), V)
    bitis = max(x["bitis"] for x in girdiler)
    D.update({"acik_kesik": bitis, "acilan": acilan + [blok], "guncelleme_utc": _utc()})
    _json_yaz(os.path.join(a_dir, KS_DURUM_AD), D)
    kayit["Tür"] = "açılış"
    _defter_ekle(defter, kayit)
    kslog.info("%s açıldı (%s): %d dosya, açık kesik %s", blok, hipotez, len(yeni_V), bitis)
    return {"blok": blok, "hipotez": hipotez, "tur": "acilis", "acik_kesik": bitis, "dosya": sorted(yeni_V)}


# ================================================================ 7) DENETİM KAPISI
def _tarih_max_cerceve(d: Any) -> Optional[pd.Timestamp]:
    best: List[pd.Timestamp] = []
    if isinstance(d, (pd.DataFrame, pd.Series)):
        if isinstance(d.index, pd.DatetimeIndex) and len(d.index):
            best.append(_gun_ix(d).max())
        elif isinstance(d.index, pd.MultiIndex):
            for i in range(d.index.nlevels):
                lv = d.index.get_level_values(i)
                if isinstance(lv, pd.DatetimeIndex) and len(lv):
                    best.append(_gun_ix(pd.DataFrame(index=lv)).max())
        if isinstance(d, pd.DataFrame):
            for c in d.columns:
                col = d[c]
                if pd.api.types.is_datetime64_any_dtype(col):
                    v = pd.to_datetime(col, errors="coerce")
                elif (col.dtype == object or pd.api.types.is_string_dtype(col)) and (KS_TARIH_AD.search(str(c)) or (
                        len(col.dropna()) and col.dropna().astype(str).head(50).str.match(KS_ISO).all())):
                    s = col.dropna().astype(str)
                    s = s[s.str.match(KS_ISO)]
                    v = pd.to_datetime(s.str.slice(0, 10), errors="coerce", format="%Y-%m-%d")
                else:
                    continue
                v = v.dropna()
                if len(v):
                    t = pd.Timestamp(v.max())
                    best.append((t.tz_convert(None) if t.tzinfo else t).normalize())
    return max(best) if best else None


def ks_en_gec_tarih(yol: str) -> Optional[pd.Timestamp]:
    """pkl (DataFrame / Series / iç içe sözlük-liste) ya da csv(.gz) dosyasındaki en geç tarih. Bulunamazsa None."""
    if not os.path.exists(yol):
        raise KasaHata(f"dosya yok: {yol}")
    alt = yol.lower()
    try:
        if alt.endswith((".csv", ".csv.gz", ".txt")):
            obj: Any = pd.read_csv(yol, low_memory=False)
        elif alt.endswith((".pkl", ".pickle", ".pkl.gz")):
            obj = pd.read_pickle(yol)
        elif alt.endswith(".parquet"):
            obj = pd.read_parquet(yol)
        else:
            raise KasaHata(f"tanınmayan dosya türü: {yol} (pkl / csv / parquet)")
    except KasaHata:
        raise
    except Exception as ex:   # okunamayan dosya kapıyı geçemez (fail-closed)
        raise KasaHata(f"okunamadı ({yol}): {type(ex).__name__}: {ex}")
    tum: List[pd.Timestamp] = []
    yigin: List[Tuple[Any, int]] = [(obj, 0)]
    while yigin:
        o, der = yigin.pop()
        if isinstance(o, (pd.DataFrame, pd.Series)):
            t = _tarih_max_cerceve(o)
            if t is not None:
                tum.append(t)
        elif isinstance(o, dict) and der < 4:
            yigin.extend((v, der + 1) for v in o.values())
        elif isinstance(o, (list, tuple)) and der < 4:
            yigin.extend((v, der + 1) for v in o)
        elif isinstance(o, (pd.Timestamp, _dt.date, np.datetime64)):
            tum.append(_ts(o))
    return max(tum) if tum else None


def kasa_kapisi(veri_yolu: Any, kesik: Optional[Any] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm modülleri koşudan önce çağırır. Verilen dosya(lar)daki en geç tarih açık kesikten büyükse KasaHata (ölçüm başlamaz).
    kesik verilmezse <cikti>/acik/KASA_DURUM.json'daki açık kesik. Tarih bulunamayan dosya kapıyı GEÇEMEZ (fail-closed)."""
    yollar = [veri_yolu] if isinstance(veri_yolu, (str, os.PathLike)) else list(veri_yolu)
    if not yollar:
        raise KasaHata("denetlenecek dosya verilmedi")
    k = _ts(kesik) if kesik is not None else _ts(_durum_oku(cikti or KS_YOL["dizin"])["acik_kesik"])
    sonuc = {"kesik": _gun(k), "dosya": {}}
    asan = []
    for y in yollar:
        t = ks_en_gec_tarih(str(y))
        if t is None:
            raise KasaHata(f"tarih bulunamadı: {y} (kapı fail-closed; tarih sütunu / dizini olmayan dosya denetlenemez)")
        sonuc["dosya"][str(y)] = _gun(t)
        if t > k:
            asan.append(f"{y}: en geç {_gun(t)} > açık kesik {_gun(k)}")
    if asan:
        raise KasaHata("KESİK AŞIMI (geleceğe bakma): " + "; ".join(asan))
    kslog.info("kasa kapısı AÇIK: %d dosya, en geç %s <= kesik %s", len(yollar), max(sonuc["dosya"].values()), _gun(k))
    return sonuc


# ================================================================ 8) DURUM
def ks_durum(cikti: Optional[str] = None, manifest: Optional[str] = None, defter: Optional[str] = None) -> str:
    cikti = cikti or KS_YOL["dizin"]; manifest = manifest or KS_YOL["manifest"]; defter = defter or KS_YOL["defter"]
    s = [f"# KASA DURUMU ({KASA_SURUM})", ""]
    if not os.path.exists(manifest):
        return "\n".join(s + [f"Manifest yok ({manifest}): kasa kurulmamış. `python KASA.py kur` + `muhurle`."])
    M = _json_oku(manifest, "manifest")
    try:
        D = _durum_oku(cikti); acik_kesik = D["acik_kesik"]; acilan = D.get("acilan", [])
        dn = "" if D.get("muhur_id") == M["muhur_id"] else " (UYARI: açık kısım başka mühüre ait)"
    except KasaHata as ex:
        acik_kesik, acilan, dn = "?", [], f" (açık kısım okunamadı: {ex})"
    s += [f"- Mühür: {M['muhur_id']} ({M['olusturma_utc']}), ilk kesik {M['kesik']}, blok tipi {M['blok_tipi']}",
          f"- Açık kesik: {acik_kesik}{dn}", f"- Açık anahtar parmak izi: {M['acik_anahtar_sha256'][:16]}…",
          f"- Kasa dizini: {cikti}", "", "| Blok | Bitiş | Satır | Dosya | Durum |", "|---|---|---:|---|---|"]
    for b in _blok_listesi(M):
        g = [x for x in M["bloklar"] if x["blok"] == b]
        s.append(f"| {b} | {max(x['bitis'] for x in g)} | {sum(x['satir'] for x in g):,} | "
                 f"{', '.join(os.path.splitext(x['dosya'])[0] for x in g)} | {'AÇIK' if b in acilan else 'mühürlü'} |".replace(",", "."))
    satirlar = [r for r in _defter_oku(defter) if r["Mühür"] == M["muhur_id"]]
    s += ["", f"Defter: {len(satirlar)} satır (bu mühür)."]
    for r in satirlar[-10:]:
        s.append(f"- {r['UTC']} {r['Blok']} {r['Hipotez']} {r['Tür']} (ön kayıt {r['Ön kayıt commit']})")
    return "\n".join(s)


# ================================================================ 9) KUR
def ks_kur(gizli: str, acik_anahtar: Optional[str] = None, uzerine: bool = False, arka: Optional[str] = None) -> Dict[str, str]:
    """Anahtar çifti. Gizli: O_EXCL + 0600, yalnız verilen yola; dönüşte / logda yol YOK. Açık: repo içi PEM."""
    acik_anahtar = acik_anahtar or KS_YOL["acik_anahtar"]
    if not gizli:
        raise KasaHata("gizli anahtar yolu verilmedi (--gizli ya da KASA_GIZLI); varsayılan yol yoktur")
    if os.path.exists(acik_anahtar) and not uzerine:
        raise KasaHata(f"açık anahtar zaten var ({acik_anahtar}); yeni anahtar eski mühürleri açılamaz kılar: bilerek ise --uzerine")
    _gizli_yol_denetle(gizli, yeni=True, yasak_kokler=[os.path.dirname(os.path.abspath(acik_anahtar))])
    g_pem, a_pem = ks_anahtar_uret(arka)
    fd = os.open(gizli, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(g_pem); f.flush(); os.fsync(f.fileno())
        os.chmod(gizli, 0o600)
    except BaseException:
        try:
            os.unlink(gizli)
        except OSError:
            pass
        raise
    _atomik_yaz(acik_anahtar, a_pem)
    iz = ks_parmak_izi(a_pem)
    kslog.info("anahtar çifti kuruldu: açık %s (parmak izi %s…); gizli anahtar verilen yola yazıldı (0600)", acik_anahtar, iz[:16])
    return {"acik_anahtar": acik_anahtar, "parmak_izi": iz, "arka": _arka_sec(arka)}


# ================================================================ 10) ÇAKIŞMA KAPISI
def _cakisma_kontrol_ks(_once=_CK_ONCE_KS, _dosya="KASA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_KS", "_CK_KAYIT", "_cakisma_kontrol_ks", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "hmac", "io", "pickle", "shutil", "struct", "subprocess",
           "tempfile", "getpass", "_dt", "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ks()


def _ks_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=KASA_SURUM)
    alt = ap.add_subparsers(dest="komut", required=True)
    p = alt.add_parser("kur"); p.add_argument("--gizli", default=None); p.add_argument("--acik-anahtar", default=None)
    p.add_argument("--uzerine", action="store_true"); p.add_argument("--arka", default=None)
    p = alt.add_parser("muhurle"); p.add_argument("--kesik", default=None); p.add_argument("--cikti", default=None)
    p.add_argument("--blok", default="ceyrek", choices=list(KS_BLOK_TIP)); p.add_argument("--kaynak", default=None)
    p.add_argument("--dosya", action="append", default=None); p.add_argument("--acik-anahtar", default=None)
    p.add_argument("--manifest", default=None); p.add_argument("--uzerine", action="store_true"); p.add_argument("--ekle", action="store_true")
    p.add_argument("--arka", default=None)
    p = alt.add_parser("ac"); p.add_argument("--blok", required=True); p.add_argument("--hipotez", required=True)
    p.add_argument("--onkayit", required=True); p.add_argument("--cikti", default=None); p.add_argument("--manifest", default=None)
    p.add_argument("--defter", default=None); p.add_argument("--arka", default=None)
    p = alt.add_parser("denetim"); p.add_argument("yol", nargs="+"); p.add_argument("--kesik", default=None); p.add_argument("--cikti", default=None)
    p = alt.add_parser("durum"); p.add_argument("--cikti", default=None); p.add_argument("--manifest", default=None)
    p.add_argument("--defter", default=None)
    p = alt.add_parser("say"); p.add_argument("--kesik", required=True); p.add_argument("--blok", default="ceyrek", choices=list(KS_BLOK_TIP))
    p.add_argument("--kaynak", default=None); p.add_argument("--dosya", action="append", default=None)
    a = ap.parse_args(argv)
    cikti = getattr(a, "cikti", None) or KS_YOL["dizin"]
    if a.komut in ("muhurle", "ac") and os.path.isdir(cikti):
        fh = logging.FileHandler(os.path.join(cikti, "kasa.log"), encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kasa: %(message)s")); kslog.addHandler(fh)
    try:
        if a.komut == "kur":
            gz = a.gizli or os.environ.get("KASA_GIZLI", "").strip()
            r = ks_kur(gz, a.acik_anahtar, a.uzerine, a.arka)
            print(f"KUR TAMAM: açık anahtar {r['acik_anahtar']}, parmak izi {r['parmak_izi']}, arka uç {r['arka']}. "
                  "Gizli anahtar verilen yolda (0600); yolu KASA_GIZLI ortam değişkeninde tut.")
        elif a.komut == "muhurle":
            if a.ekle:
                M = ks_muhurle_ekle(a.cikti, a.kaynak, a.dosya, a.acik_anahtar, a.manifest, a.arka)
            else:
                if not a.kesik:
                    raise KasaHata("--kesik zorunlu (ya da --ekle)")
                M = ks_muhurle(a.kesik, a.cikti, a.blok, a.kaynak, a.dosya, a.acik_anahtar, a.manifest, a.uzerine, a.arka)
            print(f"MÜHÜR TAMAM: {M['muhur_id']}, kesik {M['kesik']}, {len(_blok_listesi(M))} blok ({', '.join(_blok_listesi(M))}), "
                  f"son tarih {M['son_tarih']}")
        elif a.komut == "ac":
            r = ks_ac(a.blok, a.hipotez, a.onkayit, a.cikti, a.manifest, a.defter, arka=a.arka)
            print(f"AÇ TAMAM: {r['blok']} / {r['hipotez']} ({r['tur']}), açık kesik {r['acik_kesik']}. Defteri commit et.")
        elif a.komut == "denetim":
            r = kasa_kapisi(a.yol, a.kesik, a.cikti)
            print(f"DENETİM GEÇTİ: kesik {r['kesik']}; " + "; ".join(f"{os.path.basename(k)} en geç {v}" for k, v in r["dosya"].items()))
        elif a.komut == "durum":
            print(ks_durum(a.cikti, a.manifest, a.defter))
        else:
            print(ks_say_md(ks_say(a.kesik, a.blok, a.kaynak, a.dosya)))
    except KasaHata as ex:
        kslog.error("%s", ex)
        print(f"HATA: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_ks_ana())
