"""VDYT_GRAFIK — VDYT grafik arşivini küçük bir 'grafik girdi paketi'nden YENİDEN ÜRETİR (12 Kasım 2026; Cemal: grafikler Drive'a 3 MB parçalarla
yüklenmeyecek, Colab'da yeniden üretilecek; başarılı ve başarısız örneklerin ikisi de).

SINIR: VDYT.py'yi, ön kaydını (VDYT_ON_KAYIT.md §13 grafik seçim kuralı) ve sonuç dosyalarını DEĞİŞTİRMEZ. `paket` seçimi VDYT'nin kendi fonksiyonunu
(VDYT.vdyt_grafik) çağırarak yapar: çizim fonksiyonu (VDYT.vdyt_grafik_ciz) koşu süresince bir 'yakalayıcı' ile değiştirilir, VDYT'nin seçtiği her örneğin
çizim girdisi (fiyat penceresi, bölge, karar günü, savunma hattı, olay günleri, başlık, dosya adı) olduğu gibi kaydedilir; asıl fonksiyon sonra geri konur.
Aday listesi özeti için grup tanımları bir KONTROL KOPYASIYLA yeniden kurulur ve VDYT'nin seçimiyle birebir karşılaştırılır; ayrışırsa paket kurulmaz.
`ciz` VDYT.py'ye BAĞIMLI DEĞİLDİR (Colab'da yalnız numpy / pandas / matplotlib): VDYT.vdyt_grafik_ciz ile AYNI görsel sözleşmeyi paketten çizer.

Komut:  python VDYT_GRAFIK.py paket [--asama wf|kasa|hepsi]       (yalnız VDYT ara tablolarının ve fiyatların olduğu konteynerde)
            -> arastirma_cikti/vdyt/paket/vdyt_grafik_paket_<aşama>.tar ve /tmp/vdyt_paket/ (tar: manifest.json + ornek / olay / bar .csv.gz)
        python VDYT_GRAFIK.py dogrula [--girdi YOL]                  manifest sha256 + şema + iç tutarlılık; bozuksa durur
        python VDYT_GRAFIK.py ciz [--asama wf|kasa|hepsi] [--girdi YOL] [--cikti KLASOR] [--ozgun]
            -> <cikti>/<aşama>/ (doluysa <aşama>/<YYYYMMDD_HHMMSS>/): her örnek için _tam.png ve _sinyal.png, grup başına temas_<pazar>_<grup>.png,
               grafik_dizini.md, vdyt_grafik_log.txt. Mevcut dosyanın üstüne YAZMAZ. --ozgun: VDYT'nin özgün başlıkları, ek etiket yok (denetim için).
        python VDYT_GRAFIK.py karsilastir --girdi YENI_KLASOR --eski ESKI_KLASOR   dosya listesi + piksel karşılaştırması (yerel denetim)
Colab:  !python /content/drive/MyDrive/col_tarayici/VDYT_GRAFIK.py ciz --asama hepsi
        varsayılan girdi /content/drive/MyDrive/COLAB_VERILER/OUTPUT/VDYT/vdyt_grafik_paket*.tar, çıktı .../OUTPUT/VDYT/grafik/<aşama>/
SİNYAL GÜNÜ grafiği: yalnız karar gününe kadarki mumlar ve olaylar; genişleme, yön, sonuç, grup adı ÇİZİLMEZ / YAZILMAZ (bar ve olay tabloları çizimden
önce karar gününde kesilir). Dosya adı VDYT'nin adıdır (grup adını içerir; arşiv sırası için).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_VDYT_GRAFIK = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import inspect  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import tarfile  # noqa: E402
import tempfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_VG = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

vglog = logging.getLogger("col.vdyt_grafik")
if not vglog.handlers:
    _vg_h = logging.StreamHandler(sys.stderr)
    _vg_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s vdyt_grafik: %(message)s", "%H:%M:%S"))
    vglog.addHandler(_vg_h)
    vglog.setLevel(logging.INFO)
    vglog.propagate = False

VG_SURUM = "VDYT_GRAFIK v1.0 (2026-11-12): VDYT grafik arşivi için girdi paketi (paket) + bağımsız yeniden çizim (ciz) + doğrulama + karşılaştırma"
VG_COLAB_KOK = "/content/drive/MyDrive/COLAB_VERILER/OUTPUT/VDYT"
VG_YOL: Dict[str, str] = {
    "vdyt_py": os.environ.get("VDYT_GRAFIK_VDYT", os.path.join(KOK_VG, "VDYT.py")),
    "sonuc": os.path.join(KOK_VG, "arastirma_cikti", "vdyt"),
    "paket_repo": os.path.join(KOK_VG, "arastirma_cikti", "vdyt", "paket"),
    "paket_tmp": "/tmp/vdyt_paket",
    "eski_png": os.path.join(KOK_VG, "arastirma_cikti", "vdyt", "grafik"),
    "yerel_cikti": os.path.join(KOK_VG, "arastirma_cikti", "vdyt", "grafik_yeniden"),
    "colab_girdi": VG_COLAB_KOK,
    "colab_cikti": os.path.join(VG_COLAB_KOK, "grafik"),
}
VG_ASAMA = ("wf", "kasa")
VG_GRUPLAR = ("BASARILI", "BASARISIZ", "HABERLI", "HABERSIZ", "HATLI", "HATSIZ")
VG_PAZARLAR = ("BIST_K62", "BIST", "ABD")           # dosya adı ayrıştırmada uzun önek önce
VG_PAKET_AD = "vdyt_grafik_paket_{asama}.tar"
VG_SEMA: Dict[str, List[str]] = {
    "ornek.csv.gz": ["oid", "asama", "pazar", "grup", "no", "sembol", "bolge", "satir", "tanim", "model", "ufuk", "t", "karar_tarih", "yas", "bas",
                     "tespit", "gen_bas", "bit", "bit_tur", "bas_tarih", "tespit_tarih", "gen_bas_tarih", "bit_tarih", "a0", "son_tam", "lo_t", "hi_t",
                     "lo", "hi", "sv_hat_var", "sv_seviye", "sv_taban", "sv_kirilma", "Y1", "Y2", "haberli", "habersiz", "p", "esik", "y", "y20", "sonuc",
                     "baslik_tam_vdyt", "baslik_sinyal_vdyt", "dosya_tam", "dosya_sinyal"],
    "olay.csv.gz": ["oid", "sira", "i", "olay_tarih", "tur", "kat", "onceden", "yas_olayda"],
    "bar.csv.gz": ["oid", "i", "tarih", "o", "h", "l", "c", "v"],
}
VG_YON = {1.0: "YUKARI", -1.0: "AŞAĞI", 0.0: "BELİRSİZ"}
_VG_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")


class VgHata(RuntimeError):
    """VDYT_GRAFIK durdurucu hatası (paket yok / bozuk / şema dışı, VDYT sürümü ön kayıttaki değil, seçim kontrol kopyasıyla ayrışıyor, üzerine yazma)."""


# ---------------------------------------------------------------- 0) ORTAK YARDIMCILAR
def _vg_sha_bayt(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def vg_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def _vg_csv_gz(df: pd.DataFrame) -> bytes:
    """Belirlenimci gzip'li CSV (mtime=0; float'lar Python repr ile, round_trip okunur)."""
    return gzip.compress(df.to_csv(index=False, lineterminator="\n").encode("utf-8"), compresslevel=9, mtime=0)


_VG_METIN = ("oid", "asama", "pazar", "grup", "sembol", "tanim", "model", "karar_tarih", "bas_tarih", "tespit_tarih", "gen_bas_tarih", "bit_tarih",
             "sv_taban", "sonuc", "baslik_tam_vdyt", "baslik_sinyal_vdyt", "dosya_tam", "dosya_sinyal", "olay_tarih", "tur", "kat", "onceden", "tarih")


def _vg_csv_oku(b: bytes) -> pd.DataFrame:
    """Paket CSV'si: metin sütunları metin kalır ('NA', 'NAN', 'TRUE' gibi semboller NaN / bool olmaz); yalnız boş hücre NaN; float'lar bit bit aynı."""
    ham = gzip.decompress(b); bas = ham.split(b"\n", 1)[0].decode("utf-8").split(",")
    return pd.read_csv(io.BytesIO(ham), float_precision="round_trip", keep_default_na=False, na_values=[""],
                       dtype={k: str for k in _VG_METIN if k in bas})


def _vg_tar_bayt(uyeler: Dict[str, bytes]) -> bytes:
    """Belirlenimci tar (sıralı üyeler, mtime / uid / gid = 0)."""
    tb = io.BytesIO()
    with tarfile.open(fileobj=tb, mode="w", format=tarfile.USTAR_FORMAT) as tf:
        for ad in sorted(uyeler):
            ti = tarfile.TarInfo(ad); ti.size = len(uyeler[ad]); ti.mtime = 0; ti.mode = 0o644; ti.uid = ti.gid = 0; ti.uname = ti.gname = ""
            tf.addfile(ti, io.BytesIO(uyeler[ad]))
    return tb.getvalue()


def _vg_tar_oku(yol: str) -> Dict[str, bytes]:
    try:
        with tarfile.open(yol, mode="r:") as tf:
            out = {}
            for m in tf.getmembers():
                if not m.isfile() or "/" in m.name or m.name.startswith("."):
                    raise VgHata(f"{os.path.basename(yol)}: beklenmeyen tar üyesi {m.name!r}")
                f = tf.extractfile(m)
                out[m.name] = f.read() if f is not None else b""
            return out
    except (tarfile.TarError, EOFError, OSError) as ex:
        raise VgHata(f"{os.path.basename(yol)}: paket okunamadı ({type(ex).__name__}: {ex})") from ex


def _vg_yaz_yeni(yol: str, veri: bytes) -> str:
    """Dosyayı YALNIZ yoksa yazar ('xb'); varsa ve bayt bayt aynıysa dokunmaz; farklıysa durur (üzerine yazma yok)."""
    if os.path.exists(yol):
        with open(yol, "rb") as f:
            if f.read() == veri:
                vglog.info("zaten var, bayt bayt aynı: %s", yol); return yol
        raise VgHata(f"{yol} zaten var ve içeriği farklı; üzerine yazılmadı (eskisini taşıyın ya da başka klasör verin)")
    os.makedirs(os.path.dirname(yol) or ".", exist_ok=True)
    with open(yol, "xb") as f:
        f.write(veri)
    return yol


def _vg_git(args: List[str]) -> str:
    try:
        r = subprocess.run(["git", "-C", KOK_VG] + args, capture_output=True, text=True, timeout=60)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def _vg_tarih(x: Any) -> str:
    try:
        return "" if x is None or pd.isna(x) else str(pd.Timestamp(x).date())
    except (TypeError, ValueError):
        return str(x)


def _vg_f(x: Any) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return float("nan")
    return v


def _vg_yon(y1: Any) -> str:
    v = _vg_f(y1)
    return VG_YON.get(v, "?") if np.isfinite(v) else "?"


def vg_sonuc_metni(y: Any, Y1: Any, ufuk: int = 10) -> str:
    """Sonuç etiketi (yalnız TAM grafik ve dizin): y = karar gününden sonra 'ufuk' işlem günü içinde genişleme (1) / yok (0) / belirsiz (NaN)."""
    v = _vg_f(y)
    if not np.isfinite(v):
        g = f"{ufuk} gün içinde genişleme BELİRSİZ (sansür)"
    elif v >= 0.5:
        g = f"{ufuk} gün içinde GENİŞLEDİ"
    else:
        g = f"{ufuk} gün içinde GENİŞLEMEDİ"
    return f"{g}; bölge sonu yönü {_vg_yon(Y1)}"


# ---------------------------------------------------------------- 1) PAKET (yalnız VDYT ara tablolarının olduğu konteynerde)
def vg_vdyt_yukle(yol: Optional[str] = None) -> Any:
    """VDYT.py'yi ayrı modül olarak yükler ve sürümünü denetler: VDYT.py sha256 == ön kayıttaki KOD_SHA256 == sonuç dosyalarındaki kod; eşik mührü aynı.
    Tutmazsa VgHata (yanlış dosya / değişmiş kod ile paket kurulmaz)."""
    yol = yol or VG_YOL["vdyt_py"]
    if not os.path.exists(yol):
        raise VgHata(f"VDYT.py yok: {yol} (paket yalnız VDYT'nin koştuğu konteynerde kurulur; çizim için gerekmez)")
    spec = importlib.util.spec_from_file_location("VDYT_vg_kaynak", yol)
    if spec is None or spec.loader is None:
        raise VgHata(f"VDYT.py yüklenemedi: {yol}")
    V = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(V)
    except Exception as ex:  # noqa: BLE001 — yükleme hatası tek nedenle raporlanır
        raise VgHata(f"VDYT.py yüklenirken hata: {type(ex).__name__}: {ex}") from ex
    oc = V._vdyt_onkayit_oku(V._vdyt_yol("onkayit"))
    kod, esik = V.vdyt_kod_sha(), V.vdyt_esik_sha()
    if oc["kod"] != kod or oc["esik"] != esik:
        raise VgHata(f"VDYT.py / eşikler ön kayıttakiyle aynı değil (kod {kod[:12]} / {str(oc['kod'])[:12]}, eşik {esik[:12]} / {str(oc['esik'])[:12]}); paket kurulmadı")
    return V


def vg_yakala(V: Any, asama: str, pz: str, F: Dict[str, Any]) -> List[Dict[str, Any]]:
    """VDYT.vdyt_grafik'i (ön kayıtlı seçim kuralı) bir pazar için ÇAĞIRIR; çizim fonksiyonunu yakalayıcıyla değiştirir (dosya yazılmaz), her çağrının
    bağımsız değişkenlerini döndürür. Asıl fonksiyon her durumda geri konur."""
    asil = V.vdyt_grafik_ciz; imza = inspect.signature(asil); kayit: List[Dict[str, Any]] = []

    def yakalayici(*a: Any, **k: Any) -> str:
        ba = imza.bind(*a, **k); ba.apply_defaults(); kayit.append(dict(ba.arguments)); return str(ba.arguments["yol"])
    V.vdyt_grafik_ciz = yakalayici
    try:
        with tempfile.TemporaryDirectory() as td:
            V.vdyt_grafik(asama, td, [pz], None, {pz: F})
            if any(os.scandir(td)):
                raise VgHata("yakalama sırasında VDYT dosya yazdı (beklenmiyor)")
    finally:
        V.vdyt_grafik_ciz = asil
    return kayit


def vg_adaylar(V: Any, asama: str, pz: str) -> Dict[str, Any]:
    """KONTROL KOPYASI (yalnız aday listesi özeti ve çapraz denetim için): VDYT.vdyt_grafik'teki grup tanımları ve tohumlu seçim, aynı tablolar ve aynı
    VDYT yardımcılarıyla. Seçimin asıl kaynağı vg_yakala'dır; bu kopya onunla birebir aynı çıkmazsa paket kurulmaz."""
    E = V.VDYT_ESIK; ara = os.path.join(V.VDYT_YOL["ara"], asama); an = E["ana_tanim"]; hh = int(E["ana_ufuk"])
    _bas, son, _y = V._vdyt_donem(asama, E); ts = pd.Timestamp(son)
    yk, yp, yb = (os.path.join(ara, f) for f in (f"karar_{pz}_{an}.csv.gz", f"tahmin_m1_{pz}_{an}_y{hh}.csv.gz", f"bolge_{pz}_{an}.csv.gz"))
    yo = os.path.join(ara, f"olay_eslesme_{pz}_{an}.csv.gz")
    for x in (yk, yp, yb):
        if not os.path.exists(x):
            raise VgHata(f"VDYT ara tablosu yok: {x}")
    Kd = pd.read_csv(yk, parse_dates=["tarih", "y1_son"]); Pd = pd.read_csv(yp, parse_dates=["tarih"]); Bd = pd.read_csv(yb, parse_dates=["bas_tarih", "bit_tarih", "y1_son"])
    Od = pd.read_csv(yo, parse_dates=["olay_tarih"]) if os.path.exists(yo) else pd.DataFrame()
    P1 = Pd.merge(Kd[["satir", "bolge"]], on="satir", how="left")
    son_dp = Kd[Kd.Y1.isin([1, -1]) & (Kd.y1_son <= ts)].sort_values("yas").groupby(["sembol", "bolge"]).tail(1)
    Bg = Bd.assign(bolge=Bd.groupby("sembol").cumcount())
    Bg = Bg[(Bg.bit_tur == V.BITIS_GEN) & Bg.uygun.astype(bool) & (Bg.y1_son <= ts)]
    gruplar = {"BASARILI": P1[(P1.p_M_TAM >= P1.esik90_M_TAM) & (P1.y == 1)][["sembol", "bolge", "satir"]],
               "BASARISIZ": P1[(P1.p_M_TAM >= P1.esik90_M_TAM) & (P1.y == 0)][["sembol", "bolge", "satir"]],
               "HABERLI": Bg[Bg.haberli == 1][["sembol", "bolge"]], "HABERSIZ": Bg[Bg.habersiz == 1][["sembol", "bolge"]],
               "HATLI": son_dp[son_dp.sv_hat_var == 1][["sembol", "bolge", "satir"]], "HATSIZ": son_dp[son_dp.sv_hat_var == 0][["sembol", "bolge", "satir"]]}
    sec: Dict[str, Dict[str, Any]] = {}
    for g, A in gruplar.items():
        A = A.sort_values(["sembol", "bolge"]).reset_index(drop=True)
        liste = "\n".join(f"{r.sembol}|{int(r.bolge)}|{int(r.satir) if 'satir' in A and pd.notna(r.satir) else ''}" for r in A.itertuples())
        if len(A):
            rng = np.random.default_rng(V._vdyt_tohum(E["grafik"]["tohum"], pz, g))
            ix = np.sort(rng.choice(len(A), size=min(int(E["grafik"]["grup_n"]), len(A)), replace=False))
        else:
            ix = np.array([], int)
        sec[g] = {"n": int(len(A)), "sha256": _vg_sha_bayt(liste.encode("utf-8")), "sira": [int(i) for i in ix],
                  "secilen": [{"sembol": str(A.iloc[i].sembol), "bolge": int(A.iloc[i].bolge),
                               "satir": (int(A.iloc[i].satir) if "satir" in A and pd.notna(A.iloc[i].satir) else None)} for i in ix]}
    return {"sec": sec, "Kd": Kd, "Pd": Pd, "Bd": Bd, "Od": Od, "dosya": {os.path.basename(x): x for x in (yk, yp, yb, yo) if os.path.exists(x)}}


def _vg_ad_coz(ad: str) -> Tuple[str, str, int, str, str]:
    """VDYT dosya adı '<pazar>_<grup>_<no>_<sembol>_<tam|sinyal>.png' -> (pazar, grup, no, sembol, tür)."""
    k = os.path.basename(ad)
    if not k.endswith(".png"):
        raise VgHata(f"beklenmeyen grafik adı: {ad}")
    k = k[:-4]
    pz = next((p for p in VG_PAZARLAR if k.startswith(p + "_")), None)
    if pz is None:
        raise VgHata(f"grafik adında pazar yok: {ad}")
    k = k[len(pz) + 1:]; g = next((x for x in VG_GRUPLAR if k.startswith(x + "_")), None)
    if g is None:
        raise VgHata(f"grafik adında grup yok: {ad}")
    k = k[len(g) + 1:]; no, _, k = k.partition("_"); s, _, tur = k.rpartition("_")
    if not no.isdigit() or tur not in ("tam", "sinyal") or not s:
        raise VgHata(f"grafik adı çözülemedi: {ad}")
    return pz, g, int(no), s, tur


def vg_paket_kur(asama: str, V: Any, pazarlar: Optional[List[str]] = None, F_ver: Optional[Dict[str, Dict[str, Any]]] = None
                 ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Bir aşamanın paket tablolarını kurar: (ornek, olay, bar, meta). Seçim ve çizim girdisi VDYT'den yakalanır; kontrol kopyasıyla birebir denetlenir."""
    if asama not in VG_ASAMA:
        raise VgHata(f"bilinmeyen aşama: {asama}")
    E = V.VDYT_ESIK; Gr = E["grafik"]; on_bar, son_bar = int(Gr["on_bar"]), int(Gr["son_bar"]); hh = int(E["ana_ufuk"])
    O_sat: List[Dict[str, Any]] = []; Ol_par: List[pd.DataFrame] = []; B_par: List[pd.DataFrame] = []
    meta: Dict[str, Any] = {"adaylar": {}, "ara": {}, "fiyat": {}}
    for pz in pazarlar or list(E["karar_pazari"]):
        K = vg_adaylar(V, asama, pz); Kd, Pd, Bd, Od = K["Kd"], K["Pd"], K["Bd"], K["Od"]
        for ad, y in sorted(K["dosya"].items()):
            meta["ara"][ad] = {"sha256": vg_sha_dosya(y), "boy": os.path.getsize(y)}
        F = (F_ver or {}).get(pz) or V.vdyt_fiyat_yukle(pz, E)
        meta["fiyat"][pz] = {"kaynak": str(F.get("kaynak")), "kaynak_sha": F.get("kaynak_sha") or (vg_sha_dosya(F["kaynak"]) if os.path.isfile(str(F.get("kaynak"))) else "")}
        kayit = vg_yakala(V, asama, pz, F)
        cift: Dict[Tuple[str, int], Dict[str, Any]] = {}
        for c in kayit:
            pz_, g, no, s, tur = _vg_ad_coz(c["yol"])
            if pz_ != pz:
                raise VgHata(f"yakalanan grafik başka pazara ait: {c['yol']}")
            x = cift.setdefault((g, no), {"sembol": s}); x[tur] = c
            if x["sembol"] != s:
                raise VgHata(f"{pz} {g} #{no}: tam / sinyal sembolü farklı")
        for g in VG_GRUPLAR:
            S = K["sec"].get(g, {"n": 0, "sha256": _vg_sha_bayt(b""), "sira": [], "secilen": []})
            meta["adaylar"][f"{pz}/{g}"] = {"n": S["n"], "sha256": S["sha256"], "secilen_sira": S["sira"], "cizilen": 0}
            for no, sc in enumerate(S["secilen"], start=1):
                x = cift.pop((g, no), None)
                if x is None:
                    if sc["sembol"] in F["S"]:
                        raise VgHata(f"{pz} {g} #{no}: kontrol kopyası {sc['sembol']} seçti, VDYT çizmedi")
                    vglog.warning("%s %s #%d %s: fiyat yok, VDYT de çizmedi", pz, g, no, sc["sembol"]); continue
                if "tam" not in x or "sinyal" not in x:
                    raise VgHata(f"{pz} {g} #{no}: tam ya da sinyal çağrısı eksik")
                ct, cs = x["tam"], x["sinyal"]; s = x["sembol"]
                if s != sc["sembol"]:
                    raise VgHata(f"{pz} {g} #{no}: VDYT {s} seçti, kontrol kopyası {sc['sembol']}")
                if ct["sadece_gecmis"] or not cs["sadece_gecmis"]:
                    raise VgHata(f"{pz} {g} #{no}: tam / sinyal bayrağı ters")
                d = ct["d"]; b = ct["b"]; t = int(ct["t"]); hat = _vg_f(ct["hat"]); og = [int(v) for v in ct["olaylar"]]
                if int(cs["t"]) != t or not (np.isnan(hat) and np.isnan(_vg_f(cs["hat"])) or hat == _vg_f(cs["hat"])) \
                        or [int(v) for v in cs["olaylar"]] != [v for v in og if v <= t] or cs["d"] is not d:
                    raise VgHata(f"{pz} {g} #{no}: sinyal çağrısı tam çağrıyla tutarsız")
                bolge = int(sc["bolge"]); Bs = Bd[Bd.sembol == s].reset_index(drop=True)
                br = Bs.iloc[bolge]
                if int(br.bas) != int(b["bas"]) or int(br.bit) != int(b["bit"]):
                    raise VgHata(f"{pz} {g} #{no} {s}: bölge eşleşmedi")
                bas, bit, gen_bas = int(b["bas"]), int(b["bit"]), int(b["gen_bas"])
                a0 = max(0, bas - on_bar); e = min(len(d) - 1, bit + son_bar)
                if not (a0 <= bas <= t <= e and bit <= len(d) - 1):
                    raise VgHata(f"{pz} {g} #{no} {s}: karar günü pencere dışında (a0 {a0}, bas {bas}, t {t}, e {e})")
                if sc["satir"] is not None:
                    kr = Kd[Kd.satir == int(sc["satir"])]
                else:
                    kr = Kd[(Kd.sembol == s) & (Kd.bolge == bolge) & (Kd.t == t)]
                kr = kr.iloc[0] if len(kr) else None
                if kr is not None and int(kr.t) != t:
                    raise VgHata(f"{pz} {g} #{no} {s}: karar satırı t'si farklı")
                satir = int(kr.satir) if kr is not None else None
                pr = Pd[Pd.satir == satir] if satir is not None else Pd.iloc[0:0]
                p = float(pr.iloc[0].p_M_TAM) if len(pr) else float("nan"); es = float(pr.iloc[0].esik90_M_TAM) if len(pr) else float("nan")
                yv = float(kr[f"y{hh}"]) if kr is not None else float("nan")
                if len(pr) and pd.notna(pr.iloc[0].y) and float(pr.iloc[0].y) != yv:
                    raise VgHata(f"{pz} {g} #{no} {s}: tahmin y ile karar y{hh} farklı")
                X = d.iloc[a0: e + 1]; ix = np.arange(a0, e + 1)
                oid = f"{asama}|{pz}|{g}|{no}"
                B_par.append(pd.DataFrame({"oid": oid, "i": ix, "tarih": [str(z.date()) for z in X.index], "o": X.o.to_numpy(float), "h": X.h.to_numpy(float),
                                           "l": X.l.to_numpy(float), "c": X.c.to_numpy(float), "v": X.v.to_numpy(float)}))
                Ob = Od[(Od.sembol == s) & (Od.bolge == bolge)] if len(Od) else pd.DataFrame(columns=["olay_tarih"])
                oi = [int(v) for v in np.searchsorted(d.index, Ob.olay_tarih.values)] if len(Ob) else []
                if oi != og:
                    raise VgHata(f"{pz} {g} #{no} {s}: olay günleri VDYT'nin çizdiğiyle aynı değil")
                if len(Ob):
                    Ol_par.append(pd.DataFrame({"oid": oid, "sira": np.arange(len(Ob)), "i": oi, "olay_tarih": [_vg_tarih(z) for z in Ob.olay_tarih],
                                                "tur": Ob.tur.astype(str).to_numpy(), "kat": Ob.kat.astype(str).to_numpy(),
                                                "onceden": Ob.onceden.astype(str).to_numpy(), "yas_olayda": Ob.yas_olayda.to_numpy()}))
                cc = d.c.to_numpy(float)
                O_sat.append({"oid": oid, "asama": asama, "pazar": pz, "grup": g, "no": no, "sembol": s, "bolge": bolge, "satir": satir,
                              "tanim": E["ana_tanim"], "model": "M_TAM", "ufuk": hh, "t": t, "karar_tarih": str(d.index[t].date()), "yas": t - bas + 1,
                              "bas": bas, "tespit": int(b["tespit"]), "gen_bas": gen_bas, "bit": bit, "bit_tur": int(b["bit_tur"]),
                              "bas_tarih": str(d.index[bas].date()), "tespit_tarih": str(d.index[int(b["tespit"])].date()),
                              "gen_bas_tarih": str(d.index[gen_bas].date()) if gen_bas >= 0 else "", "bit_tarih": str(d.index[bit].date()),
                              "a0": a0, "son_tam": e, "lo_t": float(cc[bas: t + 1].min()), "hi_t": float(cc[bas: t + 1].max()),
                              "lo": float(cc[bas: bit + 1].min()), "hi": float(cc[bas: bit + 1].max()),
                              "sv_hat_var": _vg_f(kr.sv_hat_var) if kr is not None else float("nan"), "sv_seviye": hat,
                              "sv_taban": E["savunma"]["ana_taban"], "sv_kirilma": _vg_f(kr.sv_kirilma) if kr is not None else float("nan"),
                              "Y1": _vg_f(b.get("Y1")), "Y2": _vg_f(b.get("Y2")), "haberli": _vg_f(b.get("haberli")), "habersiz": _vg_f(b.get("habersiz")),
                              "p": p, "esik": es, "y": yv, "y20": _vg_f(kr.y20) if kr is not None else float("nan"),
                              "sonuc": vg_sonuc_metni(yv, b.get("Y1"), hh), "baslik_tam_vdyt": str(ct["baslik"]), "baslik_sinyal_vdyt": str(cs["baslik"]),
                              "dosya_tam": os.path.basename(ct["yol"]), "dosya_sinyal": os.path.basename(cs["yol"])})
                meta["adaylar"][f"{pz}/{g}"]["cizilen"] += 1
        if cift:
            raise VgHata(f"{pz}: VDYT'nin çizdiği ama kontrol kopyasında olmayan örnekler: {sorted(cift)}")
    O = pd.DataFrame(O_sat, columns=VG_SEMA["ornek.csv.gz"])
    Ol = pd.concat(Ol_par, ignore_index=True) if Ol_par else pd.DataFrame(columns=VG_SEMA["olay.csv.gz"])
    B = pd.concat(B_par, ignore_index=True) if B_par else pd.DataFrame(columns=VG_SEMA["bar.csv.gz"])
    return O, Ol[VG_SEMA["olay.csv.gz"]], B[VG_SEMA["bar.csv.gz"]], meta


def vg_paket_yaz(asama: str, O: pd.DataFrame, Ol: pd.DataFrame, B: pd.DataFrame, meta: Dict[str, Any], hedefler: List[str]) -> List[str]:
    """Paketi (tar: manifest.json + ornek / olay / bar .csv.gz) her hedef klasöre yazar; üzerine yazmaz. Manifest her üyenin sha256'sını taşır."""
    for ad, df in (("ornek.csv.gz", O), ("olay.csv.gz", Ol), ("bar.csv.gz", B)):
        eks = [k for k in VG_SEMA[ad] if k not in df.columns]
        if eks:
            raise VgHata(f"{ad}: şema sütunları eksik {eks}")
    uyeler = {"ornek.csv.gz": _vg_csv_gz(O[VG_SEMA["ornek.csv.gz"]]), "olay.csv.gz": _vg_csv_gz(Ol[VG_SEMA["olay.csv.gz"]]),
              "bar.csv.gz": _vg_csv_gz(B[VG_SEMA["bar.csv.gz"]])}
    sayim = {"ornek": int(len(O)), "png": int(2 * len(O)), "olay": int(len(Ol)), "bar": int(len(B))}
    for (pz, g), n in O.groupby(["pazar", "grup"]).size().items():
        sayim[f"{pz}/{g}"] = int(n)
    man = dict(meta); man.update({"paket": "VDYT_GRAFIK", "surum": VG_SURUM, "asama": asama, "sema": VG_SEMA, "sayim": sayim,
                                  "dosyalar": {ad: {"sha256": _vg_sha_bayt(v), "boy": len(v),
                                                    "satir": int({"ornek.csv.gz": len(O), "olay.csv.gz": len(Ol), "bar.csv.gz": len(B)}[ad])}
                                               for ad, v in uyeler.items()}})
    mj = json.dumps(man, ensure_ascii=False, indent=1, sort_keys=True, default=str)
    if _VG_EPOSTA.search(mj):
        raise VgHata("manifest içinde e-posta biçimli parça var; paket yazılmadı")
    uyeler["manifest.json"] = mj.encode("utf-8")
    tb = _vg_tar_bayt(uyeler); ad = VG_PAKET_AD.format(asama=asama)
    return [_vg_yaz_yeni(os.path.join(h, ad), tb) for h in hedefler]


def vg_paket(asama: str = "hepsi", hedefler: Optional[List[str]] = None, pazarlar: Optional[List[str]] = None) -> List[str]:
    """`paket` komutu: VDYT'yi yükler (sürüm denetimi), her aşama için paketi kurar ve yazar. Fiyatlar pazar başına bir kez yüklenir."""
    V = vg_vdyt_yukle(); E = V.VDYT_ESIK; hedefler = hedefler or [VG_YOL["paket_repo"], VG_YOL["paket_tmp"]]
    asamalar = list(VG_ASAMA) if asama == "hepsi" else [asama]
    oc = V._vdyt_onkayit_oku(V._vdyt_yol("onkayit")); yaz: List[str] = []
    pzl = pazarlar or list(E["karar_pazari"])
    tablolar: Dict[str, List[Any]] = {a: [[], [], [], {"adaylar": {}, "ara": {}, "fiyat": {}}] for a in asamalar}
    for pz in pzl:                                    # fiyat bir kez (ABD önbelleği büyük); her aşama aynı fiyatla
        F = V.vdyt_fiyat_yukle(pz, E)
        for a in asamalar:
            O, Ol, B, m = vg_paket_kur(a, V, [pz], {pz: F})
            T = tablolar[a]; T[0].append(O); T[1].append(Ol); T[2].append(B)
            for k in ("adaylar", "ara", "fiyat"):
                T[3][k].update(m[k])
        del F
    for a in asamalar:
        sy = os.path.join(VG_YOL["sonuc"], f"vdyt_sonuc_{a}.json")
        if not os.path.exists(sy):
            raise VgHata(f"VDYT sonuç dosyası yok: {sy}")
        with open(sy, encoding="utf-8") as f:
            SJ = json.load(f)
        ok = SJ.get("onkayit") or {}
        if ok.get("kod") != V.vdyt_kod_sha() or ok.get("esik") != V.vdyt_esik_sha():
            raise VgHata(f"{os.path.basename(sy)}: sonuç dosyasındaki kod / eşik mührü bugünkü VDYT.py ile aynı değil")
        eski = os.path.join(VG_YOL["eski_png"], a)
        png = sorted(glob.glob(os.path.join(eski, "*.png")))
        h = hashlib.sha256()
        for y in png:
            h.update(f"{os.path.basename(y)}|{vg_sha_dosya(y)}\n".encode())
        O, Ol, B, m = (pd.concat(tablolar[a][0], ignore_index=True), pd.concat(tablolar[a][1], ignore_index=True),
                       pd.concat(tablolar[a][2], ignore_index=True), tablolar[a][3])
        m.update({"vdyt": {"kod_sha256": V.vdyt_kod_sha(), "esik_sha256": V.vdyt_esik_sha(), "onkayit_zaman": oc["zaman"],
                           "onkayit_dosya_sha256": ok.get("dosya_sha256"), "onkayit_commit": (ok.get("git_onkayit") or {}).get("commit"),
                           "kod_commit": (ok.get("git_kod") or {}).get("commit"), "on_kayit_bolum": "VDYT_ON_KAYIT.md §13 (grafik seçim kuralı)"},
                  "kaynak_sonuc": {"ad": os.path.basename(sy), "sha256": vg_sha_dosya(sy)},
                  "vdyt_png": {"klasor": os.path.relpath(eski, KOK_VG), "n": len(png), "liste_sha256": h.hexdigest()},
                  "secim": {"kural": "VDYT.vdyt_grafik çağrıldı (ön kayıt §13); çizim girdisi yakalandı; grup tanımları kontrol kopyasıyla birebir denetlendi",
                            "tohum": int(E["grafik"]["tohum"]), "grup_n": int(E["grafik"]["grup_n"]), "gruplar": list(E["grafik"]["gruplar"]),
                            "tanim": E["ana_tanim"], "model": "M_TAM", "ufuk": int(E["ana_ufuk"]), "pazarlar": pzl},
                  "cizim": {"dpi": int(E["grafik"]["dpi"]), "on_bar": int(E["grafik"]["on_bar"]), "son_bar": int(E["grafik"]["son_bar"]),
                            "boyut": [12, 6.5], "oran": [3.2, 1]},
                  "vdyt_grafik_kod_sha256": vg_sha_dosya(os.path.abspath(__file__)) if "__file__" in globals() else "",
                  "vdyt_grafik_commit": _vg_git(["log", "-1", "--format=%H", "--", "VDYT_GRAFIK.py"])})
        yaz += vg_paket_yaz(a, O, Ol, B, m, hedefler)
        vglog.info("paket %s: %d örnek, %d bar, %d olay -> %s", a, len(O), len(B), len(Ol), ", ".join(yaz[-len(hedefler):]))
    return yaz


# ---------------------------------------------------------------- 2) DOĞRULAMA (çizimden önce; bozuk paket çizilmez)
def vg_dogrula_bayt(uyeler: Dict[str, bytes], ad: str = "paket") -> Tuple[Dict[str, Any], pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Manifest sha256 / boy / satır, şema ve iç tutarlılık denetimi. Tutmazsa VgHata. Döner: (manifest, ornek, olay, bar)."""
    if "manifest.json" not in uyeler:
        raise VgHata(f"{ad}: manifest.json yok")
    try:
        man = json.loads(uyeler["manifest.json"].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as ex:
        raise VgHata(f"{ad}: manifest okunamadı ({ex})") from ex
    D = man.get("dosyalar") or {}
    if set(D) != set(VG_SEMA) or set(uyeler) != set(VG_SEMA) | {"manifest.json"}:
        raise VgHata(f"{ad}: paket üyeleri beklenenden farklı ({sorted(uyeler)})")
    for k, m in D.items():
        if len(uyeler[k]) != int(m["boy"]) or _vg_sha_bayt(uyeler[k]) != m["sha256"]:
            raise VgHata(f"{ad}: {k} sha256 / boy manifestle tutmuyor (paket bozulmuş); ÇİZİLMEDİ")
    try:
        T = {k: _vg_csv_oku(uyeler[k]) for k in VG_SEMA}
    except (OSError, ValueError, EOFError, pd.errors.ParserError) as ex:
        raise VgHata(f"{ad}: tablo okunamadı ({type(ex).__name__}: {ex})") from ex
    for k, kol in VG_SEMA.items():
        eks = [c for c in kol if c not in T[k].columns]
        if eks:
            raise VgHata(f"{ad}: {k} şema sütunları eksik {eks}")
        if len(T[k]) != int(D[k]["satir"]):
            raise VgHata(f"{ad}: {k} satır sayısı manifestle tutmuyor")
    O, Ol, B = T["ornek.csv.gz"], T["olay.csv.gz"], T["bar.csv.gz"]
    if O.oid.duplicated().any():
        raise VgHata(f"{ad}: yinelenen örnek kimliği")
    if not set(O.grup).issubset(VG_GRUPLAR) or (O.asama != man.get("asama")).any():
        raise VgHata(f"{ad}: bilinmeyen grup ya da aşama")
    for c in ("o", "h", "l", "c", "v"):
        if not np.isfinite(B[c].to_numpy(float)).all():
            raise VgHata(f"{ad}: bar tablosunda sonlu olmayan {c}")
    Bg = dict(tuple(B.groupby("oid", sort=False)))
    for r in O.itertuples():
        X = Bg.get(r.oid)
        if X is None:
            raise VgHata(f"{ad}: {r.oid} için bar yok")
        i = X.i.to_numpy(int)
        if i[0] != int(r.a0) or i[-1] != int(r.son_tam) or not np.array_equal(i, np.arange(i[0], i[-1] + 1)):
            raise VgHata(f"{ad}: {r.oid} bar penceresi kesintili ya da a0 / son_tam ile tutmuyor")
        if not (int(r.a0) <= int(r.bas) <= int(r.t) <= int(r.son_tam)) or int(r.bit) > int(r.son_tam):
            raise VgHata(f"{ad}: {r.oid} bas / t / bit pencere dışında")
        if str(X.tarih.iloc[int(r.t) - i[0]]) != str(r.karar_tarih):
            raise VgHata(f"{ad}: {r.oid} karar günü tarihi bar tablosuyla tutmuyor")
        if (X.h.to_numpy() < np.maximum(X.o, X.c).to_numpy() - 1e-12).any() or (X.l.to_numpy() > np.minimum(X.o, X.c).to_numpy() + 1e-12).any():
            raise VgHata(f"{ad}: {r.oid} H / L tutarsız")
        if r.grup in ("BASARILI", "BASARISIZ"):
            if not (np.isfinite(r.p) and np.isfinite(r.esik) and r.p >= r.esik and r.y == (1.0 if r.grup == "BASARILI" else 0.0)):
                raise VgHata(f"{ad}: {r.oid} {r.grup} tanımı tutmuyor (p >= eşik ve y)")
    if len(Ol) and not set(Ol.oid).issubset(set(O.oid)):
        raise VgHata(f"{ad}: olay tablosunda bilinmeyen örnek")
    say = O.groupby(["pazar", "grup"]).size()
    for (pz, g), n in say.items():
        if int((man.get("sayim") or {}).get(f"{pz}/{g}", -1)) != int(n):
            raise VgHata(f"{ad}: {pz}/{g} örnek sayısı manifestle tutmuyor")
    return man, O, Ol, B


def vg_dogrula(yol: str) -> Dict[str, Any]:
    """Tek paket dosyasını doğrular; özet döndürür."""
    man, O, Ol, B = vg_dogrula_bayt(_vg_tar_oku(yol), os.path.basename(yol))
    return {"yol": yol, "sha256": vg_sha_dosya(yol), "boy": os.path.getsize(yol), "asama": man["asama"], "ornek": len(O), "bar": len(B), "olay": len(Ol),
            "sayim": man.get("sayim"), "vdyt_kod": (man.get("vdyt") or {}).get("kod_sha256"), "esik": (man.get("vdyt") or {}).get("esik_sha256")}


def vg_paket_bul(girdi: Optional[str] = None) -> List[str]:
    """Girdi: paket dosyası, klasör (içindeki vdyt_grafik_paket*.tar) ya da glob. Varsayılan: Colab'da OUTPUT/VDYT, yerelde arastirma_cikti/vdyt/paket."""
    if girdi is None:
        girdi = VG_YOL["colab_girdi"] if os.path.isdir("/content/drive/MyDrive") else VG_YOL["paket_repo"]
    if os.path.isfile(girdi):
        return [girdi]
    if os.path.isdir(girdi):
        L = sorted(glob.glob(os.path.join(girdi, "vdyt_grafik_paket*.tar")))
    else:
        L = sorted(glob.glob(girdi))
    if not L:
        raise VgHata(f"paket bulunamadı: {girdi} (beklenen: vdyt_grafik_paket_wf.tar / vdyt_grafik_paket_kasa.tar)")
    return L


# ---------------------------------------------------------------- 3) ÇİZİM (VDYT.vdyt_grafik_ciz ile aynı görsel sözleşme; VDYT.py gerekmez)
def _vg_plt() -> Any:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as ex:
        raise VgHata(f"çizim için matplotlib gerekli ({ex}); Colab'da kurulu, burada `pip install matplotlib`") from ex
    return plt


def _vg_mum(ax: Any, X: pd.DataFrame, x0: int) -> None:
    """Mum (gövde + fitil; yeşil yükselen, kırmızı düşen); VDYT.vdyt_mum_ciz ile aynı."""
    from matplotlib.patches import Rectangle
    for i, r in enumerate(X.itertuples()):
        x = x0 + i; yuk = r.c >= r.o; renk = "#1a9850" if yuk else "#d73027"
        ax.vlines(x, r.l, r.h, color=renk, linewidth=0.8)
        ax.add_patch(Rectangle((x - 0.3, min(r.o, r.c)), 0.6, max(abs(r.c - r.o), 1e-9), facecolor=renk, edgecolor=renk))


def vg_baslik(o: Dict[str, Any], sinyal: bool, ozgun: bool) -> str:
    """Başlık. ozgun=True: VDYT'nin özgün başlığı. Değilse TAM: pazar / grup / no / sembol / karar günü / yaş / olasılık / sonuç; SİNYAL: pazar / no /
    sembol / karar günü / yaş / olasılık (o gün bilinen); grup adı ve sonuç YOK."""
    if ozgun:
        return str(o["baslik_sinyal_vdyt"] if sinyal else o["baslik_tam_vdyt"])
    p, es = _vg_f(o.get("p")), _vg_f(o.get("esik"))
    pm = f"model olasılığı p = {p:.3f} (eğitim %90 eşiği {es:.3f})" if np.isfinite(p) else "model olasılığı yok (eğitim satırı)"
    ust = f"{o['pazar']} #{int(o['no'])} — {o['sembol']} — karar günü {o['karar_tarih']} (yaş {int(o['yas'])})"
    if sinyal:
        return f"{ust} — YALNIZ O GÜNE KADARKİ MUMLAR\n{pm}"
    return f"{o['pazar']} {o['grup']} #{int(o['no'])} — {o['sembol']} — karar günü {o['karar_tarih']} (yaş {int(o['yas'])})\n{pm} — sonuç: {o['sonuc']}"


def vg_sekil(o: Dict[str, Any], B: pd.DataFrame, Ol: pd.DataFrame, cz: Dict[str, Any], sinyal: bool, ozgun: bool = False) -> Any:
    """Bir örneğin şekli (kaydetmeden). SİNYAL: bar ve olay tabloları önce karar gününde KESİLİR; bölge bitişi, genişleme, yön ve sonuç kullanılmaz."""
    plt = _vg_plt()
    bas, t = int(o["bas"]), int(o["t"]); on_bar, son_bar = int(cz["on_bar"]), int(cz["son_bar"])
    B = B.sort_values("i"); Ol = Ol.sort_values("sira") if len(Ol) else Ol
    if sinyal:
        B = B[B.i <= t]; Ol = Ol[Ol.i <= t] if len(Ol) else Ol
        bit = gen_bas = None; Y1 = None
    else:
        bit, gen_bas, Y1 = int(o["bit"]), int(o["gen_bas"]), _vg_f(o.get("Y1"))
    a = max(0, bas - on_bar); son = t if sinyal else min(int(B.i.max()), bit + son_bar)
    X = B[(B.i >= a) & (B.i <= son)]
    if len(X) != son - a + 1 or (len(X) and int(X.i.iloc[0]) != a):
        raise VgHata(f"{o['oid']}: çizim penceresi barları eksik ({len(X)} / {son - a + 1})")
    fig, (ax, av) = plt.subplots(2, 1, figsize=tuple(cz.get("boyut", [12, 6.5])), sharex=True, gridspec_kw={"height_ratios": list(cz.get("oran", [3.2, 1]))})
    _vg_mum(ax, X, a)
    ax.axvspan(bas - 0.5, min(t if sinyal else bit, son) + 0.5, color="#4575b4", alpha=0.08, label="sıkışma")
    hat = _vg_f(o.get("sv_seviye"))
    if np.isfinite(hat):
        ax.hlines(hat, bas, min(t, son), color="#542788", linestyle="--", linewidth=1.2, label="savunma hattı (t'ye kadar)")
    ciz_olay = Ol[(Ol.i >= a) & (Ol.i <= son)] if len(Ol) else Ol
    for g in (ciz_olay.i.to_numpy(int) if len(ciz_olay) else []):
        ax.axvline(int(g), color="#fdae61", linestyle=":", linewidth=1.2)
    ax.axvline(t, color="black", linewidth=0.8, alpha=0.6, label="karar günü")
    if not sinyal and gen_bas is not None and gen_bas >= 0:
        ax.axvline(gen_bas, color="#d73027" if Y1 == -1 else "#1a9850", linewidth=1.5, label="genişleme başlangıcı")
        yon = VG_YON.get(Y1, "?") if Y1 is not None and np.isfinite(Y1) else "?"
        ax.annotate(yon, (gen_bas, float(X.h.max())), fontsize=10, color="black")
    av.bar(np.arange(a, son + 1), X.v.to_numpy(), color=["#1a9850" if c >= op else "#d73027" for c, op in zip(X.c, X.o)], width=0.7)
    ax.set_title(vg_baslik(o, sinyal, ozgun), fontsize=10); ax.legend(loc="upper left", fontsize=7); av.set_ylabel("hacim", fontsize=8)
    if not ozgun and len(ciz_olay):
        for (gi, tur), _x in ciz_olay.groupby(["i", "tur"], sort=True):
            ax.text(int(gi), 0.01, str(tur).replace("BIST_", "").replace("ABD_", "").replace("MAKRO_", ""), transform=ax.get_xaxis_transform(),
                    rotation=90, fontsize=6, color="#b35806", va="bottom", ha="right")
    tarih = dict(zip(X.i.to_numpy(int), X.tarih.astype(str)))
    tick = np.linspace(a, son, min(8, son - a + 1)).astype(int); av.set_xticks(tick); av.set_xticklabels([tarih[int(i)] for i in tick], fontsize=7, rotation=20)
    fig.tight_layout()
    return fig


def _vg_png_yaz(fig: Any, yol: str, dpi: int) -> str:
    plt = _vg_plt(); tb = io.BytesIO()
    try:
        fig.savefig(tb, format="png", dpi=dpi)
    finally:
        plt.close(fig)
    try:
        with open(yol, "xb") as f:                     # üzerine yazma yok
            f.write(tb.getvalue())
    except FileExistsError as ex:
        raise VgHata(f"{yol} zaten var; üzerine yazılmadı") from ex
    return yol


def vg_cikti_klasoru(kok: str, asama: str) -> str:
    """<kok>/<aşama>/; varsa ve doluysa <kok>/<aşama>/<YYYYMMDD_HHMMSS>[_n]/ (mevcut dosyaya dokunulmaz)."""
    yol = os.path.join(kok, asama)
    if os.path.isdir(yol) and os.listdir(yol):
        dmg = _dt.datetime.now().strftime("%Y%m%d_%H%M%S"); y2 = os.path.join(yol, dmg); n = 2
        while os.path.exists(y2):
            y2 = os.path.join(yol, f"{dmg}_{n}"); n += 1
        os.makedirs(y2); return y2
    os.makedirs(yol, exist_ok=True)
    return yol


def vg_temas(O: pd.DataFrame, klasor: str, asama: str, dpi: int = 100) -> List[str]:
    """Grup başına temas sayfası: üst sıra SİNYAL GÜNÜ, alt sıra TAM (aynı örnek aynı sütunda); altında sembol / karar günü / p / sonuç."""
    plt = _vg_plt(); import matplotlib.image as mpimg
    out = []
    for (pz, g), A in O.sort_values(["pazar", "grup", "no"]).groupby(["pazar", "grup"], sort=False):
        n = len(A); fig, axs = plt.subplots(2, max(n, 1), figsize=(4.2 * max(n, 1), 5.6), squeeze=False)
        for j, r in enumerate(A.itertuples()):
            for k, (ad, et) in enumerate(((r.dosya_sinyal, "sinyal günü"), (r.dosya_tam, "tam"))):
                ax = axs[k][j]; ax.axis("off"); y = os.path.join(klasor, ad)
                if os.path.exists(y):
                    ax.imshow(mpimg.imread(y))
                p = _vg_f(r.p); ps = f"p={p:.2f}" if np.isfinite(p) else "p yok"
                ax.set_title(f"#{int(r.no)} {r.sembol} {r.karar_tarih} {ps} ({et})" + ("" if k == 0 else f"\n{r.sonuc}"), fontsize=7)
        fig.suptitle(f"VDYT {asama} — {pz} {g} — üst: sinyal günü (yalnız o güne kadarki mumlar), alt: tam", fontsize=10)
        fig.tight_layout(); out.append(_vg_png_yaz(fig, os.path.join(klasor, f"temas_{pz}_{g}.png"), dpi))
    return out


def vg_dizin_md(O: pd.DataFrame, man: Dict[str, Any], paket_sha: str, klasor: str, hatalar: List[str]) -> str:
    v = man.get("vdyt") or {}
    L = [f"# VDYT grafik dizini — aşama {man.get('asama')}\n\n",
         f"Paket sha256 {paket_sha}; VDYT KOD_SHA256 {v.get('kod_sha256')}; ESIK_SHA256 {v.get('esik_sha256')}; ön kayıt commit {v.get('onkayit_commit')}; "
         f"seçim kuralı {v.get('on_kayit_bolum')}; tohum {(man.get('secim') or {}).get('tohum')}.\n\n",
         "BAŞARILI = Motor 1 (M_TAM) test satırı p >= eğitim %90 eşiği ve 10 gün içinde genişleme VAR (y = 1); BAŞARISIZ = aynı eşik, genişleme YOK (y = 0). "
         "HABERLİ / HABERSİZ = genişlemeden önce olay var / yok; HATLI / HATSIZ = genişlemeden önceki son karar noktasında savunma hattı var / yok.\n\n",
         "SİNYAL GÜNÜ grafiği yalnız karar gününe kadarki mumları ve olayları gösterir; genişleme, yön, sonuç ve grup adı grafikte yoktur (dosya adında grup "
         "arşiv sırası için vardır).\n\n",
         "| pazar | grup | no | sembol | karar günü | yaş | p | eşik | y10 | yön | sonuç | tam | sinyal |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"]
    for r in O.sort_values(["pazar", "grup", "no"]).itertuples():
        p, es, y = _vg_f(r.p), _vg_f(r.esik), _vg_f(r.y)
        L.append(f"| {r.pazar} | {r.grup} | {int(r.no)} | {r.sembol} | {r.karar_tarih} | {int(r.yas)} | {p:.3f} | {es:.3f} | "
                 f"{'' if not np.isfinite(y) else int(y)} | {_vg_yon(r.Y1)} | {r.sonuc} | {r.dosya_tam} | {r.dosya_sinyal} |\n".replace(" nan ", " - "))
    L.append(f"\nTemas sayfaları: temas_<pazar>_<grup>.png. Çizim hataları: {len(hatalar)}" + ("".join(f"\n- {h}" for h in hatalar) if hatalar else "") + "\n")
    y = os.path.join(klasor, "grafik_dizini.md"); m = "".join(L)
    with open(y, "x", encoding="utf-8") as f:
        f.write(m)
    return y


def vg_ciz(asama: str = "hepsi", girdi: Optional[str] = None, cikti: Optional[str] = None, ozgun: bool = False, temas: bool = True) -> Dict[str, Any]:
    """`ciz` komutu: paketleri bulur, HEPSİNİ önce doğrular (biri bozuksa hiçbir şey çizilmez), sonra her aşamayı yeni / boş bir klasöre çizer."""
    yollar = vg_paket_bul(girdi); P: Dict[str, Tuple[str, str, Dict[str, Any], pd.DataFrame, pd.DataFrame, pd.DataFrame]] = {}
    for y in yollar:
        man, O, Ol, B = vg_dogrula_bayt(_vg_tar_oku(y), os.path.basename(y)); a = man["asama"]; sh = vg_sha_dosya(y)
        if asama != "hepsi" and a != asama:
            continue
        if a in P:
            if P[a][1] == sh:
                continue
            raise VgHata(f"aşama {a} için birden fazla farklı paket: {P[a][0]} ve {y}")
        P[a] = (y, sh, man, O, Ol, B)
    if not P:
        raise VgHata(f"aşama {asama} için paket yok ({yollar})")
    if cikti is None:
        cikti = VG_YOL["colab_cikti"] if os.path.isdir("/content/drive/MyDrive") else VG_YOL["yerel_cikti"]
    out: Dict[str, Any] = {}
    for a in sorted(P):
        y, sh, man, O, Ol, B = P[a]; cz = man.get("cizim") or {"dpi": 150, "on_bar": 40, "son_bar": 30}; dpi = int(cz.get("dpi", 150))
        kl = vg_cikti_klasoru(cikti, a)
        fh = logging.FileHandler(os.path.join(kl, "vdyt_grafik_log.txt"), encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s")); vglog.addHandler(fh)
        try:
            vglog.info("%s: paket %s (sha256 %s), %d örnek -> %s (ozgun=%s)", a, y, sh[:16], len(O), kl, ozgun)
            Bg = dict(tuple(B.groupby("oid", sort=False))); Og = dict(tuple(Ol.groupby("oid", sort=False))) if len(Ol) else {}
            bos = pd.DataFrame(columns=VG_SEMA["olay.csv.gz"]); yazilan: List[str] = []; hatalar: List[str] = []
            for o in O.to_dict("records"):
                for sinyal in (False, True):
                    ad = o["dosya_sinyal"] if sinyal else o["dosya_tam"]
                    try:
                        fig = vg_sekil(o, Bg[o["oid"]], Og.get(o["oid"], bos), cz, sinyal, ozgun)
                        yazilan.append(_vg_png_yaz(fig, os.path.join(kl, ad), dpi))
                    except (VgHata, OSError, ValueError, KeyError) as ex:
                        hatalar.append(f"{ad}: {type(ex).__name__}: {ex}"); vglog.error("%s: %s", ad, ex)
            tm = vg_temas(O, kl, a) if temas else []
            dz = vg_dizin_md(O, man, sh, kl, hatalar)
            say = {g: int((O.grup == g).sum()) for g in VG_GRUPLAR}
            vglog.info("%s: %d PNG, %d temas sayfası, %d hata; grup sayıları %s", a, len(yazilan), len(tm), len(hatalar), say)
            out[a] = {"klasor": kl, "png": yazilan, "temas": tm, "dizin": dz, "hata": hatalar, "paket": y, "paket_sha256": sh, "grup": say}
        finally:
            vglog.removeHandler(fh); fh.close()
    return out


# ---------------------------------------------------------------- 4) KARŞILAŞTIRMA (yerel denetim: yeniden çizilen PNG'ler ile VDYT'nin PNG'leri)
def vg_karsilastir(yeni: str, eski: str) -> Dict[str, Any]:
    """Dosya adı listesi (pazar_grup_no_sembol_tür) birebir aynı mı; her ortak PNG için boyut, bayt sha256 ve piksel farkı."""
    import matplotlib.image as mpimg
    A = {os.path.basename(x) for x in glob.glob(os.path.join(yeni, "*.png")) if not os.path.basename(x).startswith("temas_")}
    Bs = {os.path.basename(x) for x in glob.glob(os.path.join(eski, "*.png"))}
    ortak = sorted(A & Bs); bayt = piksel = 0; fark: List[Dict[str, Any]] = []
    for ad in ortak:
        ya, yb = os.path.join(yeni, ad), os.path.join(eski, ad)
        if vg_sha_dosya(ya) == vg_sha_dosya(yb):
            bayt += 1; piksel += 1; continue
        ia, ib = mpimg.imread(ya), mpimg.imread(yb)
        if ia.shape != ib.shape:
            fark.append({"ad": ad, "neden": f"boyut {ia.shape} / {ib.shape}"}); continue
        d = np.abs(ia.astype(float) - ib.astype(float)).max(axis=-1)
        if (d == 0).all():
            piksel += 1
        else:
            fark.append({"ad": ad, "farkli_piksel": int((d > 0).sum()), "pay": float((d > 0).mean()), "en_buyuk": float(d.max())})
    return {"yeni_n": len(A), "eski_n": len(Bs), "liste_ayni": A == Bs, "yalniz_yeni": sorted(A - Bs), "yalniz_eski": sorted(Bs - A),
            "ortak": len(ortak), "bayt_ayni": bayt, "piksel_ayni": piksel, "fark": fark}


def _cakisma_kontrol_vdyt_grafik(_once=_CK_ONCE_VDYT_GRAFIK, _dosya="VDYT_GRAFIK.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_VDYT_GRAFIK", "_CK_KAYIT", "_cakisma_kontrol_vdyt_grafik", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "glob", "gzip", "subprocess", "tarfile", "tempfile", "inspect", "io", "importlib",
           "_dt", "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_vdyt_grafik()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=VG_SURUM)
    ap.add_argument("komut", choices=["paket", "dogrula", "ciz", "karsilastir"])
    ap.add_argument("--asama", default="hepsi", choices=["wf", "kasa", "hepsi"])
    ap.add_argument("--girdi", default=None, help="paket dosyası / klasörü / glob (karsilastir: yeni PNG klasörü)")
    ap.add_argument("--cikti", default=None, help="çıktı kök klasörü (paket: hedef klasör)")
    ap.add_argument("--eski", default=None, help="karsilastir: VDYT'nin PNG klasörü")
    ap.add_argument("--pazar", action="append", default=None)
    ap.add_argument("--ozgun", action="store_true", help="VDYT'nin özgün başlıkları, ek etiket yok (piksel denetimi için)")
    ap.add_argument("--temas_yok", action="store_true")
    a_ = ap.parse_args()
    try:
        if a_.komut == "paket":
            print("\n".join(vg_paket(a_.asama, [a_.cikti] if a_.cikti else None, a_.pazar)))
        elif a_.komut == "dogrula":
            for y_ in vg_paket_bul(a_.girdi):
                print(json.dumps(vg_dogrula(y_), ensure_ascii=False, default=str))
        elif a_.komut == "ciz":
            R_ = vg_ciz(a_.asama, a_.girdi, a_.cikti, a_.ozgun, not a_.temas_yok)
            for k_, v_ in R_.items():
                print(f"{k_}: {len(v_['png'])} PNG, {len(v_['temas'])} temas, {len(v_['hata'])} hata -> {v_['klasor']}")
            if any(v_["hata"] for v_ in R_.values()):
                sys.exit(2)
        else:
            if not a_.girdi or not a_.eski:
                raise VgHata("karsilastir: --girdi (yeni klasör) ve --eski (VDYT PNG klasörü) gerekli")
            print(json.dumps(vg_karsilastir(a_.girdi, a_.eski), ensure_ascii=False, indent=1))
    except (VgHata, FileNotFoundError, OSError) as ex:
        vglog.error("%s", ex); sys.exit(1)
