"""K67 — BİLANÇO SONRASI ANALİST REVİZYONLARI: sonraki getiriyi ve çöl sinyalini açıklıyor mu? (tek dosya; 12 Kasım 2026; ana oturum iş tanımı;
ön kayıt arastirma_cikti/col_dis_bilgi/K67_ON_KAYIT.md).

Soru (Cemal): bilanço sonrasında analistlerin EPS ve hedef fiyat tahminlerindeki değişim (yukarı / aşağı revizyon yapan analist sayısı, net revizyon oranı,
revizyon büyüklüğü, görüş birliği / ayrışma, revizyonun bilanço sürpriziyle aynı ya da ters yönde olması) sonraki getiriyi açıklıyor mu, çöl sinyaline ek bilgi
taşıyor mu? Veri yoksa tahmin ÜRETİLMEZ; hangi sağlayıcıda hangi tarihsel alanın eksik olduğu yazılır.
  Olay      ABD bilanço açıklaması (Yahoo bilanço takvimi; Nasdaq takvimi 2022-12 -> çapraz denetim). r0 = açıklamaya tepki veren ilk işlem günü (açılış öncesi /
            gün içi / saat yok: açıklama günü ya da sonraki ilk işlem günü; kapanış sonrası: sonraki işlem günü). Karar günü d = r0'dan itibaren 5. işlem günü
            (d = r0 + 4) kapanışı; giriş d+1 açılışı. Revizyon penceresi = [açıklama anı, d kapanışı (16:00 ET)]. Aynı hissede 60 işlem gününde tek olay.
  Değişken  Yahoo analist not günlüğü (yfinance upgrades_downgrades): N_UP, N_DOWN, NET, BUYUKLUK, AYRISMA (hedef fiyat + tavsiye), YON_UYUM (NET işareti x
            analist EPS sürprizi işareti). EPS TAHMİN REVİZYONU: VERİ YOK (ücretsiz tarihsel kaynak yok; vekil üretilmez).
  S1        bilanço olaylarında değişkenin ÜST / ALT üçte biri (geçmiş 365 gün olay içi sıra) x FI_OLCUT 60 + 20 gün; ÜST - ALT; tepki (EAR) üçte biri içinde
            katmanlı ÜST - ALT ('ek katkı'; karar istatistiği).
  S2        K24 çöl olayları (K64.k64_olay_k24; K64.py DEĞİŞMEZ) içinde, son 60 işlem gününde karar günü olan bilanço olayının NET'i: çöl içi ÜST / ALT üçte biri.
FON_IZI.py, K60.py, K64.py MODÜL olarak içe alınır; DEĞİŞMEZ. SEC'e istek atılmaz. Servise kayıt / anahtar yok.

Komut:  python K67.py indir       yalnız VERİ: Yahoo not günlüğü + bilanço takvimi (önbellek /tmp/k67_yahoo; kaldığı yerden sürer; kibar hız)
        python -I K67.py kapsam   yalnız SAYIM (olay, değişken kapsamı, üçte bir grupları, çöl x revizyon); getiri HESAPLANMAZ
        python K67.py onkayit     ön kaydı yazar (ölçümden ÖNCE; mühür + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I K67.py kos      mühür + veri sha256 + ön kayıt git'e işlenmiş ve değişmemiş -> ölçüm + rapor
        python K67.py rapor       K67_RAPOR.md'yi çıktılardan yeniden yazar
Colab:  exec(open('K67.py').read()); k67_kos()
Veri:   /tmp/veri/V_ABD.pkl (islenmis-veri dalı), /tmp/pead/liste_abd.csv.gz (K28 Nasdaq takvimi), /tmp/k67_yahoo (Yahoo; repoya konmaz).
        Kişisel e-posta / anahtar yok. Çıktılar arastirma_cikti/col_dis_bilgi/.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K67 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K67 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K67 not in sys.path:
    sys.path.insert(0, KOK_K67)

import FON_IZI as FI  # noqa: E402
import K60  # noqa: E402
import K64  # noqa: E402

k67log = logging.getLogger("col.k67")
if not k67log.handlers:
    _k67_h = logging.StreamHandler(sys.stderr)
    _k67_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k67: %(message)s", "%H:%M:%S"))
    k67log.addHandler(_k67_h)
    k67log.setLevel(logging.INFO)
    k67log.propagate = False

K67_SURUM = "K67 v1.0 (2026-11-12): bilanço sonrası analist revizyonları (Yahoo not günlüğü) x FI_OLCUT; S1 bilanço olayları, S2 çöl etkileşimi"
K67_YOL = {"cikti": os.path.join(KOK_K67, "arastirma_cikti", "col_dis_bilgi"), "veri": os.environ.get("K67_VERI", "/tmp/veri"),
           "yahoo": os.environ.get("K67_YAHOO", "/tmp/k67_yahoo"), "pead": os.environ.get("K67_PEAD", "/tmp/pead")}
K67_DOSYA = {"onkayit": "K67_ON_KAYIT.md", "kapsam": "k67_kapsam.csv", "kapsam_ozet": "k67_kapsam_ozet.json", "indir_ozet": "k67_indir_ozet.json",
             "olay": "k67_olaylar.csv.gz", "s1": "k67_s1.csv", "fark": "k67_s1_fark.csv", "s2": "k67_s2.csv", "karar": "k67_karar.csv", "meta": "k67_meta.json",
             "rapor": "K67_RAPOR.md"}
_K67_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_K67_ET = "America/New_York"

# İndirme ayarları (mühre GİRMEZ: veri içeriği sha256 ile mühürlenir). Kibar hız: istekler arası bekleme; 429'da geri çekil ve yavaşla; kimlik değiştirme YOK.
K67_INDIR: Dict[str, Any] = {"bekle": 1.2, "bekle_tavan": 12.0, "yavasla": 1.5, "geri_cekil": [60, 120, 300, 600, 900], "ardisik_dur": 6, "zaman_asimi": 40,
                             "takvim_boyut": 100, "not_modul": "upgradeDowngradeHistory"}
_K67_QS_URL = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}"
_K67_TAKVIM_URL = "https://finance.yahoo.com/calendar/earnings?symbol={}&offset=0&size={}"

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı ön kayıtta; sonradan değişmez)
_K67_DEGISKEN: List[Tuple[str, str, str]] = [
    ("N_UP", "S", "pencerede revizyon yönü YUKARI olan kurum sayısı (kurum başına tek yön; yön kuralı §3). En az 1 kurum kaydı olan olaylarda tanımlı"),
    ("N_DOWN", "S", "pencerede revizyon yönü AŞAĞI olan kurum sayısı. En az 1 kurum kaydı olan olaylarda tanımlı"),
    ("NET", "S", "(N_UP - N_DOWN) / (N_UP + N_DOWN + N_AYNI); payda (yön sınıfı olan kurum) >= 2. Yeni kapsama (init) paydaya girmez"),
    ("BUYUKLUK", "S", "kurum başına hedef değişim oranlarının medyanı; oran = penceredeki SON kaydın hedefi / pencerenin İLK kaydının önceki hedefi - 1; en az 2 oran"),
    ("AYRISMA", "S", "kurum başına hedef değişim oranlarının standart sapması (ddof = 1); en az 3 oran"),
    ("YON_UYUM", "K", "NET işareti x analist EPS sürprizi işareti (sürpriz yoksa tepki EAR): AO (sürpriz +, NET +), TO (sürpriz +, NET -), TU (sürpriz -, NET +), "
     "AU (sürpriz -, NET -), NOTR (NET = 0 ya da sürpriz = 0), YOK (NET ya da sürpriz yok). Karşıtlıklar: YU_POZ = AO - TO, YU_NEG = TU - AU"),
]

K67_ESIK: Dict[str, Any] = {
    "kriz": "2026-08-31",
    "donem": [["2017-2021", "2017-01-01", "2021-12-31"], ["2022-2026", "2022-01-01", "2026-12-31"], ["2023-2026", "2023-01-01", "2026-12-31"]],
    "bagimsiz": ["2017-2021", "2022-2026"],
    "pazar": "ABD",
    "olay": {"kaynak": "YAHOO_TAKVIM", "capraz": "NASDAQ_K28", "ilk_tarih": "2016-06-01", "kapanis_saat": 16, "karar_gun": 5, "tekil_gun": 60, "r0_azami_gun": 7,
             "saat_yok": "12 AM (Yahoo 'at 12 AM' = saat bildirilmemiş): açılış öncesi gibi (r0 = açıklama günü ya da sonraki ilk işlem günü)"},
    "rev": {"min_net": 2, "min_buyukluk": 2, "min_ayrisma": 3, "oran_sinir": [1.0 / 3.0, 3.0], "tarih_yalniz": "gün sonu 23:59:59 ET sayılır",
            "hedef_eylem": {"Raises": 1, "Lowers": -1}, "tavsiye_eylem": {"up": 1, "down": -1}, "baslangic": ["init"]},
    "surpriz": {"birincil": "YAHOO_SURPRIZ", "yedek": ["NASDAQ_SURPRIZ", "EAR"], "ear": "C(b) / C(a) - 1 - aynı pencerede bütün hisselerin medyanı; a = açıklama gününden "
                "önceki son işlem günü, b = açıklama gününden sonraki ilk işlem günü (FON_IZI.fi_k28_olaylar tanımı)"},
    "sira": {"ust": 2.0 / 3.0, "alt": 1.0 / 3.0, "ic_gun": 365, "ic_min": 30},
    "s1": {"n_esik": 30, "bootstrap": 2000, "tohum": 67001, "guven": [2.5, 97.5], "gecerli_pay": 0.90, "katman_min": 10},
    "s2": {"pencere": 60, "tohum": 67002},
    "ek_ufuk": 20,
    "maliyet": {"ABD": 0.0020},
    "coklu": {"bh_q": 0.10},
    "degisken": [{"kod": k, "tur": t, "tanim": d} for k, t, d in _K67_DEGISKEN],
    "karsitlik": {"YU_POZ": ["AO", "TO"], "YU_NEG": ["TU", "AU"]},
    "aile": ["N_UP", "N_DOWN", "NET", "BUYUKLUK", "AYRISMA", "YU_POZ", "YU_NEG", "COL_NET"],
}


class K67Hata(RuntimeError):
    """K67'ye özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, veri eksik ya da farklı, çıktı yok)."""


def _k67_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K67_YOL["cikti"], K67_DOSYA.get(ad, ad))


def _k67_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def k67_kodlar(E: Optional[Dict[str, Any]] = None, tur: Optional[str] = None) -> List[str]:
    return [d["kod"] for d in (E or K67_ESIK)["degisken"] if tur is None or d["tur"] == tur]


# ---------------------------------------------------------------- 1) İNDİRME (ağ yalnız burada; yalnız Yahoo; kibar hız)
class _K67Sinir(RuntimeError):
    """Yahoo hız sınırı (429) ya da geçici ağ hatası: geri çekil, yavaşla, yeniden dene."""


def _k67_yf_oturum() -> Any:
    """yfinance oturumu (çerez + crumb yfinance tarafından yönetilir; kimlik değiştirilmez)."""
    try:
        from yfinance.data import YfData
    except ImportError as ex:   # paket yoksa indirme yapılamaz
        raise K67Hata(f"yfinance yok ({ex}): pip install yfinance")
    return YfData()


def _k67_getir_not(oturum: Any, sembol: str) -> Tuple[str, bytes]:
    """Bir hissenin analist not günlüğü (quoteSummary upgradeDowngradeHistory; ham JSON). Döner: (durum, gövde). durum: 'tamam' | 'yok' (Yahoo veri yok)."""
    try:
        r = oturum.get(_K67_QS_URL.format(sembol), params={"modules": K67_INDIR["not_modul"], "corsDomain": "finance.yahoo.com", "formatted": "false",
                                                           "symbol": sembol}, timeout=K67_INDIR["zaman_asimi"])
    except Exception as ex:   # yfinance 429'u istisna olarak da atabilir; ağ hatası geçicidir
        raise _K67Sinir(f"{type(ex).__name__}: {str(ex)[:120]}")
    if r.status_code == 429 or (r.status_code >= 500):
        raise _K67Sinir(f"HTTP {r.status_code}")
    if r.status_code == 404:
        return "yok", r.content
    if r.status_code != 200:
        raise _K67Sinir(f"HTTP {r.status_code}")
    try:
        json.loads(r.content)
    except ValueError:
        raise _K67Sinir("JSON değil")
    return "tamam", r.content


def _k67_getir_takvim(oturum: Any, sembol: str) -> Tuple[str, bytes]:
    """Bir hissenin Yahoo bilanço takvimi sayfasındaki tablo (ham <table> HTML'i; en çok takvim_boyut satır). durum: 'tamam' | 'yok' (tablo yok)."""
    try:
        r = oturum.get(_K67_TAKVIM_URL.format(sembol, K67_INDIR["takvim_boyut"]), timeout=K67_INDIR["zaman_asimi"])
    except Exception as ex:
        raise _K67Sinir(f"{type(ex).__name__}: {str(ex)[:120]}")
    if r.status_code == 429 or r.status_code >= 500:
        raise _K67Sinir(f"HTTP {r.status_code}")
    if r.status_code == 404:
        return "yok", b""
    if r.status_code != 200:
        raise _K67Sinir(f"HTTP {r.status_code}")
    m = re.search(rb"<table.*?</table>", r.content, re.S)
    return ("tamam", m.group(0)) if m else ("yok", b"")


def _k67_yaz_gz(yol: str, govde: bytes) -> None:
    os.makedirs(os.path.dirname(yol), exist_ok=True); gecici = yol + ".gecici"
    with open(gecici, "wb") as ham, gzip.GzipFile(fileobj=ham, mode="wb", compresslevel=6, mtime=0, filename="") as f:
        f.write(govde)
    os.replace(gecici, yol)


def k67_indir(semboller: List[str], klasor: Optional[str] = None, getir_not: Optional[Callable[[Any, str], Tuple[str, bytes]]] = None,
              getir_takvim: Optional[Callable[[Any, str], Tuple[str, bytes]]] = None, oturum: Any = None, uyu: Callable[[float], None] = time.sleep) -> Dict[str, Any]:
    """Yahoo not günlüğü + bilanço takvimi önbelleği: klasor/not/<S>.json.gz, klasor/takvim/<S>.html.gz, klasor/durum.csv (sembol, tur, durum, zaman_utc).
    Kaldığı yerden sürer (önbellekte olan yeniden istenmez). 429 / geçici hata: geri_cekil süresi kadar bekle, beklemeyi 'yavasla' katı artır (tavan
    bekle_tavan); ardisik_dur kez üst üste hata -> durur (sonra yeniden çalıştırılır). getir_* ve oturum testler içindir (sahte indirici, ağ yok)."""
    I = K67_INDIR; kl = klasor or K67_YOL["yahoo"]; os.makedirs(kl, exist_ok=True); dy = os.path.join(kl, "durum.csv")
    D = pd.read_csv(dy, dtype=str) if os.path.exists(dy) else pd.DataFrame(columns=["sembol", "tur", "durum", "zaman_utc"])
    bitti = set(zip(D.sembol, D.tur)); getir = {"not": getir_not or _k67_getir_not, "takvim": getir_takvim or _k67_getir_takvim}
    uzanti = {"not": "json.gz", "takvim": "html.gz"}; yeni: List[Dict[str, str]] = []; bekle = float(I["bekle"]); ardisik = 0; sinir = 0; sayac = {"tamam": 0, "yok": 0}
    if oturum is None and (getir_not is None or getir_takvim is None):
        oturum = _k67_yf_oturum()
    t0 = time.time()

    def kaydet() -> None:
        nonlocal D, yeni
        if yeni:
            D = pd.concat([D, pd.DataFrame(yeni)], ignore_index=True); yeni = []
            g = dy + ".gecici"; D.to_csv(g, index=False); os.replace(g, dy)

    try:
        for i, s in enumerate(semboller):
            for tur in ("not", "takvim"):
                if (s, tur) in bitti:
                    continue
                deneme = 0
                while True:
                    try:
                        durum, govde = getir[tur](oturum, s); ardisik = 0; break
                    except _K67Sinir as ex:
                        ardisik += 1; sinir += 1
                        if ardisik >= I["ardisik_dur"]:
                            kaydet()
                            raise K67Hata(f"Yahoo üst üste {ardisik} kez hata verdi (son: {ex}); durdu. Önbellek korunuyor, sonra yeniden çalıştırın")
                        w = I["geri_cekil"][min(deneme, len(I["geri_cekil"]) - 1)]; bekle = min(bekle * I["yavasla"], I["bekle_tavan"]); deneme += 1
                        k67log.warning("%s %s: %s -> %d sn geri çekil, istekler arası bekleme %.1f sn", s, tur, ex, w, bekle); uyu(w)
                if durum == "tamam":
                    _k67_yaz_gz(os.path.join(kl, tur, f"{s}.{uzanti[tur]}"), govde)
                sayac[durum] = sayac.get(durum, 0) + 1; bitti.add((s, tur)); yeni.append({"sembol": s, "tur": tur, "durum": durum, "zaman_utc": _k67_simdi()})
                uyu(bekle)
            if (i + 1) % 25 == 0:
                kaydet(); k67log.info("indir: %d / %d hisse (%.0f sn; bekleme %.1f sn; 429/hata %d)", i + 1, len(semboller), time.time() - t0, bekle, sinir)
    finally:
        kaydet()
    return {"hisse": len(semboller), "yeni": sayac, "sinir_hatasi": sinir, "son_bekleme_sn": bekle, "sure_sn": round(time.time() - t0), "durum_dosyasi": dy}


def k67_indir_semboller(klasor: Optional[str] = None) -> List[str]:
    """V_ABD.pkl'deki semboller (fiyat dosyası yalnız sembol listesi için okunur)."""
    import pickle
    yol = os.path.join(klasor or K67_YOL["veri"], "V_ABD.pkl")
    if not os.path.exists(yol):
        raise K67Hata(f"fiyat verisi yok: {yol} (islenmis-veri dalı: python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
    with open(yol, "rb") as f:
        V = pickle.load(f)
    if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
        V = V["veri"]
    return sorted(str(s) for s in V)


# ---------------------------------------------------------------- 2) OKUYUCULAR (yalnız önbellek; ağ yok)
def k67_not_ayristir(govde: bytes, sembol: str) -> pd.DataFrame:
    """Ham quoteSummary JSON -> not kayıtları. Sütunlar: sembol, zaman_utc (epoch sn), kurum, eylem, yeni_tav, eski_tav, hedef_eylem, hedef, eski_hedef.
    Hedef 0 ya da yok -> NaN (Yahoo 'yok' yerine 0 yazar)."""
    try:
        J = json.loads(govde)
        res = (J.get("quoteSummary") or {}).get("result") or []
        H = ((res[0] if res else {}) or {}).get("upgradeDowngradeHistory", {}).get("history") or []
    except (ValueError, AttributeError, TypeError) as ex:
        raise K67Hata(f"{sembol}: not günlüğü JSON'u ayrıştırılamadı ({ex})")

    def fiyat(x: Any) -> float:
        try:
            v = float(x)
        except (TypeError, ValueError):
            return np.nan
        return v if np.isfinite(v) and v > 0 else np.nan
    sat = []
    for h in H:
        try:
            ep = int(h.get("epochGradeDate"))
        except (TypeError, ValueError):
            continue
        sat.append({"sembol": sembol, "zaman_utc": ep, "kurum": str(h.get("firm") or "").strip(), "eylem": str(h.get("action") or "").strip().lower(),
                    "yeni_tav": str(h.get("toGrade") or ""), "eski_tav": str(h.get("fromGrade") or ""), "hedef_eylem": str(h.get("priceTargetAction") or ""),
                    "hedef": fiyat(h.get("currentPriceTarget")), "eski_hedef": fiyat(h.get("priorPriceTarget"))})
    return pd.DataFrame(sat, columns=["sembol", "zaman_utc", "kurum", "eylem", "yeni_tav", "eski_tav", "hedef_eylem", "hedef", "eski_hedef"])


def k67_not_et(N: pd.DataFrame) -> pd.DataFrame:
    """Kayıtlara ET (America/New_York, saat dilimsiz) yayım anı 'et' ve 'tarih_yalniz' eklenir. Saat bilgisi olmayan kayıt (epoch tam UTC gece yarısı) gün
    sonu 23:59:59 ET sayılır (karar günü d'de yayımlanmışsa pencereye GİRMEZ: geleceğe bakmaya karşı tutucu)."""
    N = N.copy(); z = pd.to_numeric(N.zaman_utc, errors="coerce").astype("int64"); N["tarih_yalniz"] = (z % 86400) == 0
    et = pd.to_datetime(z, unit="s", utc=True).dt.tz_convert(_K67_ET).dt.tz_localize(None)
    gun = pd.to_datetime(z, unit="s").dt.normalize() + pd.Timedelta(hours=23, minutes=59, seconds=59)
    N["et"] = np.where(N.tarih_yalniz, gun, et).astype("datetime64[ns]")
    return N


def k67_not_oku(klasor: Optional[str] = None, semboller: Optional[List[str]] = None) -> pd.DataFrame:
    """Önbellekteki bütün not günlükleri (birebir aynı kayıtlar tekilleştirilir) + ET zamanı."""
    kl = os.path.join(klasor or K67_YOL["yahoo"], "not"); sat = []
    if not os.path.isdir(kl):
        raise K67Hata(f"not günlüğü önbelleği yok: {kl} (önce `python K67.py indir`)")
    for y in sorted(glob.glob(os.path.join(kl, "*.json.gz"))):
        s = os.path.basename(y)[:-len(".json.gz")]
        if semboller is not None and s not in semboller:
            continue
        with gzip.open(y, "rb") as f:
            sat.append(k67_not_ayristir(f.read(), s))
    N = pd.concat(sat, ignore_index=True) if sat else k67_not_ayristir(b"{}", "")
    N = N.drop_duplicates(["sembol", "zaman_utc", "kurum", "eylem", "yeni_tav", "eski_tav", "hedef_eylem", "hedef", "eski_hedef"]).reset_index(drop=True)
    return k67_not_et(N)


_K67_TARIH = re.compile(r"\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})(?:\s+at\s+(\d{1,2})\s*([AP]M))?")


def k67_takvim_ayristir(html: bytes, sembol: str) -> pd.DataFrame:
    """Yahoo bilanço takvimi tablosu (ham HTML) -> sembol, tarih (gün), saat (ET saat 0-23; yoksa -1), an (ET; saat yoksa gün başı), eps_tahmin, eps_gercek,
    surpriz (%). Yahoo saatleri ET'dir (EST / EDT); dakika yok."""
    bos = pd.DataFrame(columns=["sembol", "tarih", "saat", "an", "eps_tahmin", "eps_gercek", "surpriz"])
    if not html:
        return bos
    try:
        T = pd.read_html(io.StringIO(html.decode("utf-8", "replace")), na_values=["-"])[0]
    except (ValueError, IndexError) as ex:
        k67log.warning("%s takvim tablosu okunamadı: %s", sembol, ex)
        return bos
    kol = {c: re.sub(r"\s+", "", str(c)).lower() for c in T.columns}; T = T.rename(columns=kol)
    if "earningsdate" not in T:
        raise K67Hata(f"{sembol}: takvim tablosunda 'Earnings Date' sütunu yok ({list(kol.values())})")
    sat = []
    for r in T.to_dict("records"):
        m = _K67_TARIH.match(str(r.get("earningsdate") or ""))
        if not m:
            continue
        try:
            g = pd.Timestamp(_dt.datetime.strptime(re.sub(r"\s+", " ", m.group(1)), "%B %d, %Y"))
        except ValueError:
            continue
        sa = -1
        if m.group(2):
            sa = int(m.group(2)) % 12 + (12 if m.group(3) == "PM" else 0)
        sat.append({"sembol": sembol, "tarih": g, "saat": sa, "an": g + pd.Timedelta(hours=max(sa, 0)),
                    "eps_tahmin": pd.to_numeric(r.get("epsestimate"), errors="coerce"), "eps_gercek": pd.to_numeric(r.get("reportedeps"), errors="coerce"),
                    "surpriz": pd.to_numeric(r.get("surprise(%)"), errors="coerce")})
    return pd.DataFrame(sat, columns=bos.columns) if sat else bos


def k67_takvim_oku(klasor: Optional[str] = None, semboller: Optional[List[str]] = None) -> pd.DataFrame:
    """Önbellekteki bütün bilanço takvimleri. Aynı hisse-gün birden çok satırsa sürprizi dolu olan ilk satır tutulur."""
    kl = os.path.join(klasor or K67_YOL["yahoo"], "takvim"); sat = []
    if not os.path.isdir(kl):
        raise K67Hata(f"bilanço takvimi önbelleği yok: {kl} (önce `python K67.py indir`)")
    for y in sorted(glob.glob(os.path.join(kl, "*.html.gz"))):
        s = os.path.basename(y)[:-len(".html.gz")]
        if semboller is not None and s not in semboller:
            continue
        with gzip.open(y, "rb") as f:
            sat.append(k67_takvim_ayristir(f.read(), s))
    T = pd.concat([x for x in sat if len(x)], ignore_index=True) if any(len(x) for x in sat) else k67_takvim_ayristir(b"", "")
    if len(T):
        T = T.assign(_d=T.surpriz.notna()).sort_values(["sembol", "tarih", "_d"], ascending=[True, True, False], kind="stable")
        T = T.drop_duplicates(["sembol", "tarih"]).drop(columns="_d").reset_index(drop=True)
    for c in ("eps_tahmin", "eps_gercek", "surpriz"):
        T[c] = pd.to_numeric(T[c], errors="coerce")
    T["saat"] = pd.to_numeric(T["saat"], errors="coerce").fillna(-1).astype(int)
    return T


def k67_nasdaq_oku(yol: Optional[str] = None) -> pd.DataFrame:
    """K28 Nasdaq takvimi (FON_IZI.fi_k28_liste_abd çıktısı): sembol, tarih, surpriz (%). Saat alanı %99 'time-not-supplied' olduğu için kullanılmaz."""
    yol = yol or os.path.join(K67_YOL["pead"], "liste_abd.csv.gz")
    if not os.path.exists(yol):
        raise K67Hata(f"Nasdaq takvimi yok: {yol} (FON_IZI.fi_k28_liste_abd)")
    Q = pd.read_csv(yol, dtype={"sembol": str}); Q = Q[Q.sembol.notna()].copy()
    Q["tarih"] = pd.to_datetime(Q.tarih); Q["surpriz"] = pd.to_numeric(Q.surpriz, errors="coerce")
    Q = Q.assign(_d=Q.surpriz.notna()).sort_values(["sembol", "tarih", "_d"], ascending=[True, True, False], kind="stable").drop_duplicates(["sembol", "tarih"])
    return Q[["sembol", "tarih", "surpriz"]].reset_index(drop=True)


def k67_klasor_sha(klasor: str, alt: Tuple[str, ...] = ("not", "takvim")) -> Tuple[str, int]:
    """Önbellek içeriğinin sha256'sı (göreli yol + dosya baytları, sıralı) ve dosya sayısı. gzip başlığı sabit (mtime 0, ad yok): aynı içerik -> aynı özet."""
    h = hashlib.sha256(); n = 0
    for a in alt:
        for y in sorted(glob.glob(os.path.join(klasor, a, "*"))):
            if y.endswith(".gecici"):
                continue
            h.update(f"{a}/{os.path.basename(y)}\n".encode())
            with open(y, "rb") as f:
                h.update(hashlib.sha256(f.read()).digest())
            n += 1
    if not n:
        raise K67Hata(f"önbellek boş: {klasor}")
    return h.hexdigest(), n


# ---------------------------------------------------------------- 3) OLAYLAR (bilanço açıklamaları; yalnız d ve öncesi bilgi)
def k67_takvim_matris(V: Dict[str, pd.DataFrame]) -> Tuple[pd.DatetimeIndex, pd.DataFrame]:
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in V])))
    return idx, pd.DataFrame({s: V[s].Close for s in sorted(V)}).reindex(idx)


def k67_ear(sembol: str, gun: pd.Timestamp, idx: pd.DatetimeIndex, C: pd.DataFrame, onbellek: Optional[Dict[Tuple[int, int], float]] = None) -> Tuple[float, int, int]:
    """K28 tepkisi (FON_IZI.fi_k28_olaylar tanımı): a = açıklama gününden önceki son işlem günü, b = sonraki ilk işlem günü (birleşik takvim); EAR = C(b) / C(a)
    - 1 - aynı pencerede bütün hisselerin medyan getirisi. Döner (ear, a, b konumları); hesaplanamazsa ear NaN."""
    a = int(idx.searchsorted(pd.Timestamp(gun))) - 1; b = int(idx.searchsorted(pd.Timestamp(gun), side="right"))
    if a < 0 or b >= len(idx) or sembol not in C:
        return np.nan, a, b
    c0, c1 = C.iat[a, C.columns.get_loc(sembol)], C.iat[b, C.columns.get_loc(sembol)]
    if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
        return np.nan, a, b
    key = (a, b)
    if onbellek is not None and key in onbellek:
        p = onbellek[key]
    else:
        p = float((C.iloc[b] / C.iloc[a] - 1).median())
        if onbellek is not None:
            onbellek[key] = p
    return float(c1 / c0 - 1 - p), a, b


def k67_olaylar(T: pd.DataFrame, V: Dict[str, pd.DataFrame], Q: Optional[pd.DataFrame] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Bilanço olayları (yalnız fiyatı olan hisseler; ilk_tarih <= açıklama günü <= kriz). Her olay için: r0 (tepki veren ilk işlem günü; hissenin kendi işlem
    günleri), d = r0 + (karar_gun - 1), giris = d + 1 (yoksa NaT), revizyon penceresi [pencere_bas, pencere_son] (ET), tepki EAR, sürprizler (Yahoo; Nasdaq
    ±1 gün eşleşme), seçilen sürpriz ve kaynağı, tekil (aynı hissede r0'lar arası tekil_gun işlem günü; ilk olay)."""
    E = E or K67_ESIK; O = E["olay"]; kriz = pd.Timestamp(E["kriz"]); ilk = pd.Timestamp(O["ilk_tarih"]); kg = int(O["karar_gun"]); ks = int(O["kapanis_saat"])
    idx, C = k67_takvim_matris(V); onb: Dict[Tuple[int, int], float] = {}; sat = []
    T = T[(T.tarih >= ilk) & (T.tarih <= kriz) & T.sembol.isin(list(V))] if len(T) else T
    for s, g in (T.groupby("sembol", sort=True) if len(T) else []):
        dix = V[s].index; n = len(dix); pos_l = []
        for r in g.sort_values("tarih", kind="stable").itertuples():
            amc = bool(r.saat >= ks); p = int(dix.searchsorted(r.tarih, side="right" if amc else "left"))
            if p >= n or (dix[p] - r.tarih).days > int(O["r0_azami_gun"]):
                continue
            dp = p + kg - 1
            if dp >= n:
                continue
            ear, a, b = k67_ear(s, r.tarih, idx, C, onb)
            bas = r.an if int(r.saat) > 0 else r.tarih
            sat.append({"sembol": s, "tarih": r.tarih, "saat": int(r.saat), "amc": amc, "an": r.an, "r0": dix[p], "d": dix[dp],
                        "giris": dix[dp + 1] if dp + 1 < n else pd.NaT, "pencere_bas": bas, "pencere_son": dix[dp] + pd.Timedelta(hours=ks),
                        "ear": ear, "ear_b": idx[b] if 0 <= b < len(idx) else pd.NaT, "surpriz_yahoo": r.surpriz, "eps_tahmin": r.eps_tahmin, "eps_gercek": r.eps_gercek,
                        "_r0p": p})
            pos_l.append(p)
    kol = ["sembol", "tarih", "saat", "amc", "an", "r0", "d", "giris", "pencere_bas", "pencere_son", "ear", "ear_b", "surpriz_yahoo", "eps_tahmin", "eps_gercek", "_r0p"]
    X = pd.DataFrame(sat, columns=kol)
    X["tekil"] = False
    for s, g in X.groupby("sembol", sort=False):
        g = g.sort_values(["_r0p", "tarih"], kind="stable")
        X.loc[g.index[K64.k64_tekil(g._r0p.to_numpy(), int(O["tekil_gun"]))], "tekil"] = True
    X["surpriz_nasdaq"] = np.nan; X["nasdaq_tarih"] = pd.NaT
    if Q is not None and len(Q) and len(X):
        L = X[["sembol", "tarih"]].reset_index().sort_values("tarih"); R = Q.rename(columns={"tarih": "nasdaq_tarih", "surpriz": "sn"}).sort_values("nasdaq_tarih")
        M = pd.merge_asof(L, R.assign(_t=R.nasdaq_tarih), left_on="tarih", right_on="_t", by="sembol", direction="nearest", tolerance=pd.Timedelta(days=1))
        M = M.set_index("index").reindex(X.index); X["surpriz_nasdaq"] = M.sn.to_numpy(float); X["nasdaq_tarih"] = M.nasdaq_tarih.to_numpy()
    sy, sn = X.surpriz_yahoo.to_numpy(float), X.surpriz_nasdaq.to_numpy(float)
    X["surpriz"] = np.where(np.isfinite(sy), sy, np.where(np.isfinite(sn), sn, X.ear.to_numpy(float)))
    X["surpriz_kaynak"] = np.where(np.isfinite(sy), "YAHOO", np.where(np.isfinite(sn), "NASDAQ", np.where(np.isfinite(X.ear.to_numpy(float)), "EAR", "YOK")))
    return X.drop(columns="_r0p").sort_values(["sembol", "tarih"], kind="stable").reset_index(drop=True)


# ---------------------------------------------------------------- 4) DEĞİŞKENLER (pencere içindeki not günlüğü kayıtları; yalnız <= d kapanışı)
def k67_kurum_yon(K: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[str, float, bool]:
    """Bir kurumun penceredeki kayıtları (zaman sıralı) -> (yön 'UP' | 'DOWN' | 'AYNI' | 'BASLA', hedef değişim oranı (yoksa NaN), aykırı mı).
    ORAN = son kaydın (hedefi olan) hedefi / ilk kaydın (önceki hedefi olan) önceki hedefi - 1; (1 + oran) [1/3, 3] dışındaysa aykırı (olası bölünme / hata):
    oran NaN. YÖN: oran sonlu ve != 0 -> işareti; değilse hedef eylemleri (Raises +1 / Lowers -1) toplamının işareti; değilse tavsiye eylemleri (up +1 /
    down -1) toplamının işareti; değilse bütün kayıtlar 'init' ise BASLA (yeni kapsama), aksi AYNI."""
    R = (E or K67_ESIK)["rev"]; eh, h = K.eski_hedef.to_numpy(float), K.hedef.to_numpy(float); oran = np.nan; aykiri = False
    i0 = np.flatnonzero(np.isfinite(eh))
    if len(i0):
        i1 = np.flatnonzero(np.isfinite(h) & (np.arange(len(h)) >= i0[0]))
        if len(i1):
            oran = float(h[i1[-1]] / eh[i0[0]] - 1)
            lo, hi = R["oran_sinir"]
            if not (lo <= 1 + oran <= hi):
                oran = np.nan; aykiri = True
    if np.isfinite(oran) and oran != 0:
        return ("UP" if oran > 0 else "DOWN"), oran, aykiri
    he = int(sum(R["hedef_eylem"].get(x, 0) for x in K.hedef_eylem))
    if he:
        return ("UP" if he > 0 else "DOWN"), oran, aykiri
    te = int(sum(R["tavsiye_eylem"].get(x, 0) for x in K.eylem))
    if te:
        return ("UP" if te > 0 else "DOWN"), oran, aykiri
    if len(K) and all(x in R["baslangic"] for x in K.eylem):
        return "BASLA", oran, aykiri
    return "AYNI", oran, aykiri


def k67_pencere_degiskenleri(W: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Bir olayın pencere kayıtları -> değişkenler (§3). Kurum adı boş olan kayıt kendi başına bir kurum sayılmaz (atlanır)."""
    R = (E or K67_ESIK)["rev"]; out: Dict[str, Any] = {"n_kayit": int(len(W)), "n_kurum": 0, "N_AYNI": 0, "N_BASLA": 0, "n_oran": 0, "n_aykiri": 0}
    yon: Dict[str, int] = {"UP": 0, "DOWN": 0, "AYNI": 0, "BASLA": 0}; oran: List[float] = []
    W = W[W.kurum.astype(str).str.len() > 0]
    for _k, K in W.groupby("kurum", sort=True):
        y, o, a = k67_kurum_yon(K.sort_values("et", kind="stable"), E); yon[y] += 1; out["n_aykiri"] += int(a)
        if np.isfinite(o):
            oran.append(o)
    nk = sum(yon.values()); out["n_kurum"] = nk; out["N_AYNI"] = yon["AYNI"]; out["N_BASLA"] = yon["BASLA"]; out["n_oran"] = len(oran)
    out["N_UP"] = float(yon["UP"]) if nk >= 1 else np.nan; out["N_DOWN"] = float(yon["DOWN"]) if nk >= 1 else np.nan
    payda = yon["UP"] + yon["DOWN"] + yon["AYNI"]
    out["NET"] = float((yon["UP"] - yon["DOWN"]) / payda) if payda >= int(R["min_net"]) else np.nan
    v = np.asarray(oran, float)
    out["BUYUKLUK"] = float(np.median(v)) if len(v) >= int(R["min_buyukluk"]) else np.nan
    out["AYRISMA"] = float(np.std(v, ddof=1)) if len(v) >= int(R["min_ayrisma"]) else np.nan
    return out


def k67_yon_uyum(net: float, surpriz: float) -> str:
    """YON_UYUM kategorisi: AO, TO, TU, AU, NOTR, YOK (§3)."""
    if not (np.isfinite(net) and np.isfinite(surpriz)):
        return "YOK"
    if net == 0 or surpriz == 0:
        return "NOTR"
    if surpriz > 0:
        return "AO" if net > 0 else "TO"
    return "TU" if net > 0 else "AU"


def k67_degiskenler(X: pd.DataFrame, N: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Olaylara pencere değişkenleri: yalnız pencere_bas <= et <= pencere_son kayıtları (et = ET yayım anı; tarih-yalnız kayıt gün sonu sayılır). 'gecmis' =
    hissenin pencere sonuna kadar en az bir kaydı var mı (kapsama); 'kapsama' = pencerede en az bir kurum kaydı."""
    E = E or K67_ESIK; X = X.copy().reset_index(drop=True); kol = ["n_kayit", "n_kurum", "N_UP", "N_DOWN", "N_AYNI", "N_BASLA", "n_oran", "n_aykiri", "NET",
                                                                  "BUYUKLUK", "AYRISMA"]
    sat: List[Dict[str, Any]] = [{} for _ in range(len(X))]; gecmis = np.zeros(len(X), bool)
    G = {s: g.sort_values("et", kind="stable").reset_index(drop=True) for s, g in N.groupby("sembol", sort=False)} if len(N) else {}
    for s, ix in (X.groupby("sembol", sort=False).groups.items() if len(X) else []):
        g = G.get(s)
        for i in ix:
            if g is None or not len(g):
                sat[i] = k67_pencere_degiskenleri(N.iloc[:0], E); continue
            t = g.et.to_numpy("datetime64[ns]"); a = int(np.searchsorted(t, np.datetime64(X.at[i, "pencere_bas"], "ns"), "left"))
            b = int(np.searchsorted(t, np.datetime64(X.at[i, "pencere_son"], "ns"), "right")); gecmis[i] = b > 0
            sat[i] = k67_pencere_degiskenleri(g.iloc[a:b], E)
    D = pd.DataFrame(sat, columns=kol, index=X.index)
    for c in kol:
        X[c] = D[c].to_numpy(float)
    X["gecmis"] = gecmis; X["kapsama"] = X.n_kurum.fillna(0).to_numpy(float) >= 1
    X["YON_UYUM"] = [k67_yon_uyum(n, s) for n, s in zip(X.NET.to_numpy(float), X.surpriz.to_numpy(float))]
    return X


def k67_siralar(X: pd.DataFrame, E: Optional[Dict[str, Any]] = None, gun_kol: str = "d", ek: Tuple[str, ...] = ("ear",)) -> pd.DataFrame:
    """Sürekli değişkenler (ve EAR) için OLAY İÇİ sıra (K64.k64_ic_sira: karar günü [g - ic_gun, g] aralığındaki tekil olaylar, kendisi ve aynı gün dahil; en az
    ic_min; geleceğe bakmaz) -> <kod>_ic ve <kod>_grup (UST / ORTA / ALT / ''). Tekil olmayan olaylarda sıra yok."""
    E = E or K67_ESIK; S = E["sira"]; X = X.copy(); m = X.tekil.to_numpy(bool) if len(X) else np.zeros(0, bool)
    for k in k67_kodlar(E, "S") + list(ek):
        X[k + "_ic"] = np.nan
        if m.any():
            X.loc[m, k + "_ic"] = K64.k64_ic_sira(pd.DatetimeIndex(X[gun_kol]).to_numpy("datetime64[D]")[m], X[k].to_numpy(float)[m], S["ic_gun"], S["ic_min"])
        X[k + "_grup"] = K64.k64_grup(X[k + "_ic"].to_numpy(float), {"sira": S})
    return X


def k67_col_olaylar(V: Dict[str, pd.DataFrame], X: pd.DataFrame, E: Optional[Dict[str, Any]] = None, col: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """S2: K24 çöl olayları (K64.k64_olay_k24; tekil, girişi olan) + son s2.pencere işlem gününde (sinyal t dahil, hissenin kendi işlem günleri) karar günü d
    olan EN SON tekil bilanço olayının değişkenleri (d <= t: bilgi sinyal gününde biliniyor). NET'in çöl içi sırası (K64.k64_ic_sira, sinyal günü) -> NET_ic,
    NET_grup."""
    E = E or K67_ESIK; w = int(E["s2"]["pencere"]); S = E["sira"]
    C0 = K64.k64_olay_k24(V) if col is None else col
    C0 = C0[C0.tekil & C0.giris.notna()].reset_index(drop=True) if len(C0) else C0
    B = X[X.tekil] if len(X) else X; Bg = {s: g.sort_values("d", kind="stable") for s, g in B.groupby("sembol", sort=False)} if len(B) else {}
    al = ["tarih", "d", "NET", "N_UP", "N_DOWN", "BUYUKLUK", "AYRISMA", "n_kurum", "ear", "surpriz", "YON_UYUM"]; sat = []
    for r in C0.itertuples():
        dix = V[r.sembol].index; t = int(dix.get_loc(pd.Timestamp(r.sinyal))); g = Bg.get(r.sembol); row = {"sembol": r.sembol, "sinyal": r.sinyal, "giris": r.giris}
        if g is not None and len(g):
            dp = dix.get_indexer(pd.DatetimeIndex(g.d)); ok = (dp >= 0) & (dp <= t) & (dp >= t - w + 1)
            if ok.any():
                h = g.iloc[np.flatnonzero(ok)[-1]]; row.update({"b_" + k: h[k] for k in al}); row["bilanco"] = True
        sat.append(row)
    Y = pd.DataFrame(sat)
    for k in ["b_" + k for k in al] + ["bilanco"]:
        if k not in Y:
            Y[k] = np.nan if k != "bilanco" else False
    Y["bilanco"] = Y.bilanco.fillna(False).astype(bool) if len(Y) else Y.bilanco
    Y["NET_ic"] = K64.k64_ic_sira(pd.DatetimeIndex(Y.sinyal).to_numpy("datetime64[D]"), Y.b_NET.to_numpy(float), S["ic_gun"], S["ic_min"]) if len(Y) else []
    Y["NET_grup"] = K64.k64_grup(Y.NET_ic.to_numpy(float), {"sira": S}) if len(Y) else []
    return Y


# ---------------------------------------------------------------- 5) GİRDİ, HAZIRLIK, KAPSAM (yalnız SAYIM)
def k67_girdi(E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """GERÇEK girdi (yalnız önbellek; ağ yok): V (V_ABD; fon krizi kesiği), T (Yahoo takvim), N (Yahoo not günlüğü), Q (Nasdaq K28)."""
    E = E or K67_ESIK; V = K64.k64_fiyat_yukle("ABD", K67_YOL["veri"], {**K64.K64_ESIK, "kriz": E["kriz"]}); S = sorted(V)
    return {"V": V, "T": k67_takvim_oku(None, S), "N": k67_not_oku(None, S), "Q": k67_nasdaq_oku()}


def k67_hazirla(g: Dict[str, Any], E: Optional[Dict[str, Any]] = None, col: Optional[pd.DataFrame] = None, s2: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Olaylar -> değişkenler -> sıralar; S2 çöl olayları. Getiri HESAPLANMAZ."""
    E = E or K67_ESIK; X = k67_olaylar(g["T"], g["V"], g.get("Q"), E); X = k67_degiskenler(X, g["N"], E); X = k67_siralar(X, E)
    Y = k67_col_olaylar(g["V"], X, E, col if col is not None else g.get("col")) if s2 else pd.DataFrame()
    return X, Y


def _k67_pencere(X: pd.DataFrame, takvim: pd.DatetimeIndex, giris_kol: str = "giris") -> np.ndarray:
    """Olayın 60 günlük ölçüm penceresi kesikten önce bitiyor mu (FI_OLCUT ufku; birleşik takvim)."""
    if not len(X):
        return np.zeros(0, bool)
    gi = takvim.get_indexer(pd.DatetimeIndex(X[giris_kol])); return (gi >= 0) & (gi + int(FI.FI_OLCUT["ufuk"]) - 1 <= len(takvim) - 1)


def k67_veri_ozeti(g: Dict[str, Any]) -> Dict[str, Any]:
    """İndirme / kaynak özeti (yalnız SAYI): not günlüğü yıl yıl kayıt / hisse / alan doluluğu; takvim yıl yıl olay / sürpriz doluluğu / saat türü; Nasdaq
    örtüşmesi (±1 gün) ve sürpriz işaret uyumu."""
    V, T, N, Q = g["V"], g["T"], g["N"], g["Q"]; S = set(V); o: Dict[str, Any] = {"hisse_fiyat": len(V)}
    dy = os.path.join(K67_YOL["yahoo"], "durum.csv")
    if os.path.exists(dy):
        D = pd.read_csv(dy, dtype=str); o["durum"] = {f"{a}_{b}": int(n) for (a, b), n in D.groupby(["tur", "durum"]).size().items()}
        z = pd.to_datetime(D.zaman_utc.str.replace(" UTC", ""), errors="coerce"); o["cekim_ilk_utc"] = str(z.min()); o["cekim_son_utc"] = str(z.max())
    y = N.et.dt.year if len(N) else pd.Series(dtype=int)
    o["not"] = {"hisse_kayitli": int(N.sembol.nunique()), "kayit": int(len(N)), "ilk": str(N.et.min()) if len(N) else None, "son": str(N.et.max()) if len(N) else None,
                "tarih_yalniz_pay": float(N.tarih_yalniz.mean()) if len(N) else None,
                "yil": {int(k): {"kayit": int(len(v)), "hisse": int(v.sembol.nunique()), "hedef_dolu": round(float(v.hedef.notna().mean()), 4),
                                 "eski_hedef_dolu": round(float(v.eski_hedef.notna().mean()), 4), "up": int((v.eylem == "up").sum()), "down": int((v.eylem == "down").sum()),
                                 "init": int((v.eylem == "init").sum())} for k, v in N.groupby(y)} if len(N) else {}}
    Tt = T[T.sembol.isin(S)] if len(T) else T; yt = Tt.tarih.dt.year if len(Tt) else pd.Series(dtype=int)
    sinif = np.where(Tt.saat >= 16, "kapanis_sonrasi", np.where(Tt.saat >= 1, "acilis_oncesi_gun_ici", "saat_yok")) if len(Tt) else np.array([])
    o["takvim"] = {"hisse": int(Tt.sembol.nunique()) if len(Tt) else 0, "satir": int(len(Tt)), "ilk": str(Tt.tarih.min().date()) if len(Tt) else None,
                   "son": str(Tt.tarih.max().date()) if len(Tt) else None, "saat": {k: int(v) for k, v in pd.Series(sinif).value_counts().items()},
                   "yil": {int(k): {"satir": int(len(v)), "hisse": int(v.sembol.nunique()), "surpriz_dolu": round(float(v.surpriz.notna().mean()), 4),
                                    "eps_tahmin_dolu": round(float(v.eps_tahmin.notna().mean()), 4)} for k, v in Tt.groupby(yt)} if len(Tt) else {}}
    Qs = Q[Q.sembol.isin(S) & (Q.tarih <= pd.Timestamp(K67_ESIK["kriz"]))] if len(Q) else Q
    if len(Qs) and len(Tt):
        Ty = Tt[(Tt.tarih >= Qs.tarih.min()) & (Tt.tarih <= Qs.tarih.max())]
        L = Qs.sort_values("tarih"); R = Ty.rename(columns={"tarih": "yt", "surpriz": "ys"})[["sembol", "yt", "ys"]].sort_values("yt")
        M = pd.merge_asof(L, R.assign(_t=R.yt), left_on="tarih", right_on="_t", by="sembol", direction="nearest", tolerance=pd.Timedelta(days=1))
        L2 = Ty.sort_values("tarih"); R2 = Qs.rename(columns={"tarih": "qt"})[["sembol", "qt"]].sort_values("qt")
        M2 = pd.merge_asof(L2, R2.assign(_t=R2.qt), left_on="tarih", right_on="_t", by="sembol", direction="nearest", tolerance=pd.Timedelta(days=1))
        b = M.yt.notna() & M.surpriz.notna() & M.ys.notna() & (M.surpriz != 0) & (M.ys != 0)
        o["nasdaq"] = {"satir": int(len(Qs)), "ilk": str(Qs.tarih.min().date()), "son": str(Qs.tarih.max().date()), "yahoo_eslesen_pay": round(float(M.yt.notna().mean()), 4),
                       "ayni_gun_pay": round(float((M.yt == M.tarih).mean()), 4), "yahoo_satir_ortusme": int(len(Ty)),
                       "yahoo_nasdaqta_bulunan_pay": round(float(M2.qt.notna().mean()), 4) if len(M2) else None,
                       "surpriz_isaret_uyum": round(float((np.sign(M.surpriz[b]) == np.sign(M.ys[b])).mean()), 4) if b.any() else None, "surpriz_karsilastirilan": int(b.sum())}
    return o


def k67_kapsam(cikti: Optional[str] = None, girdi: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """KAPSAM: yalnız SAYIM. Dönem başına: olay (ham / tekil / pencere), revizyonu olan olay oranı, değişken kapsamı ve ÜST / ORTA / ALT, katmanlı (EAR üçte biri)
    gruplar, YON_UYUM kategorileri, sürpriz kaynağı, S2 çöl x revizyon. Getiri, eşli fark, FI_OLCUT paneli HESAPLANMAZ."""
    E = E or K67_ESIK; sentetik = girdi is not None; t0 = time.time(); g = girdi if sentetik else k67_girdi(E)
    X, Y = k67_hazirla(g, E); tak, _C = k67_takvim_matris(g["V"]); X["pencere"] = _k67_pencere(X, tak) & X.tekil.to_numpy(bool)
    Y["pencere"] = _k67_pencere(Y, tak) if len(Y) else []
    sat: List[Dict[str, Any]] = []; oz: Dict[str, Any] = {"zaman": _k67_simdi(), "surum": K67_SURUM, "muhur": k67_esik_sha(E)}
    if not sentetik:
        oz["veri"] = k67_veri_ozeti(g)
    oz["olay_yil"] = {int(k): {"ham": int(len(v)), "tekil": int(v.tekil.sum()), "pencere": int(v.pencere.sum()), "kapsama": int((v.pencere & v.kapsama).sum()),
                               "NET": int((v.pencere & v.NET.notna()).sum())} for k, v in X.groupby(X.d.dt.year)} if len(X) else {}
    for dn, a, b in E["donem"]:
        gi = pd.to_datetime(X.giris)
        md = ((gi >= a) & (gi <= b)).to_numpy() if len(X) else np.zeros(0, bool); tk = md & X.tekil.to_numpy(bool); pn = md & X.pencere.to_numpy(bool)
        kim = {"kume": "S1", "donem": dn}
        sat.append({**kim, "degisken": "(olay)", "n_ham": int(md.sum()), "n_tekil": int(tk.sum()), "n_pencere": int(pn.sum()),
                    "n_kapsama": int((pn & X.kapsama.to_numpy(bool)).sum()), "n_gecmis": int((pn & X.gecmis.to_numpy(bool)).sum()),
                    "kapsama_pay": float((pn & X.kapsama.to_numpy(bool)).sum() / max(int(pn.sum()), 1)),
                    "n_ear": int((pn & np.isfinite(X.ear.to_numpy(float))).sum()),
                    **{f"surpriz_{k}": int((pn & (X.surpriz_kaynak == k).to_numpy()).sum()) for k in ("YAHOO", "NASDAQ", "EAR", "YOK")}})
        ek = X.ear_grup.to_numpy(str) if len(X) else np.array([], str)
        for k in k67_kodlar(E, "S"):
            gr = X[k + "_grup"].to_numpy(str) if len(X) else np.array([], str); v = np.isfinite(X[k].to_numpy(float)) if len(X) else md
            row = {**kim, "degisken": k, "n_deger": int((pn & v).sum()), "n_ust": int((pn & (gr == "UST")).sum()), "n_orta": int((pn & (gr == "ORTA")).sum()),
                   "n_alt": int((pn & (gr == "ALT")).sum()), "n_ust_k": int((pn & (gr == "UST") & (ek != "")).sum()), "n_alt_k": int((pn & (gr == "ALT") & (ek != "")).sum())}
            for e in ("UST", "ORTA", "ALT"):
                row[f"ust_{e}"] = int((pn & (gr == "UST") & (ek == e)).sum()); row[f"alt_{e}"] = int((pn & (gr == "ALT") & (ek == e)).sum())
            sat.append(row)
        yu = X.YON_UYUM.to_numpy(str) if len(X) else np.array([], str)
        sat.append({**kim, "degisken": "YON_UYUM", **{f"n_{c}": int((pn & (yu == c)).sum()) for c in ("AO", "TO", "TU", "AU", "NOTR", "YOK")},
                    **{f"n_{c}_k": int((pn & (yu == c) & (ek != "")).sum()) for c in ("AO", "TO", "TU", "AU")}})
        if len(Y):
            gy = pd.to_datetime(Y.giris); my = ((gy >= a) & (gy <= b)).to_numpy() & Y.pencere.to_numpy(bool); ng = Y.NET_grup.to_numpy(str)
            sat.append({"kume": "S2", "donem": dn, "degisken": "COL_NET", "n_pencere": int(my.sum()), "n_bilanco": int((my & Y.bilanco.to_numpy(bool)).sum()),
                        "n_deger": int((my & np.isfinite(Y.b_NET.to_numpy(float))).sum()), "n_ust": int((my & (ng == "UST")).sum()),
                        "n_orta": int((my & (ng == "ORTA")).sum()), "n_alt": int((my & (ng == "ALT")).sum())})
    K = pd.DataFrame(sat); cik = cikti or K67_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    K.to_csv(_k67_yol("kapsam", cikti), index=False); K60._k60_json_yaz(_k67_yol("kapsam_ozet", cikti), oz)
    k67log.info("kapsam: %d olay, %d çöl olayı (%.0f sn)", len(X), len(Y), time.time() - t0)
    return K


# ---------------------------------------------------------------- 6) MÜHÜR VE VERİ ÖZETLERİ
def _k67_bagimli() -> Dict[str, Any]:
    """Mühre giren dış tanımlar: FI_OLCUT (cetvel), FI_K24 (çöl kuralı), K64 olay ayarları (tekilleştirme, K24 başlangıcı)."""
    return {"FI_OLCUT": FI.FI_OLCUT, "FI_K24": FI.FI_K24, "K64_olay": K64.K64_ESIK["olay"], "K64_kriz": K64.K64_ESIK["kriz"]}


def k67_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: K67_ESIK (değişken tanımları dahil) + dış tanımlar; biri değişirse koşu durur."""
    s = json.dumps({"K67_ESIK": E or K67_ESIK, "bagimli": _k67_bagimli()}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def k67_veri_sha() -> Dict[str, Tuple[str, int]]:
    """Koşunun okuyacağı verinin ve içe alınan kodun sha256'ları: ad -> (sha256, dosya sayısı). Eksik dosyada durur."""
    sha = K60._k60_sha; out: Dict[str, Tuple[str, int]] = {}
    for ad, y in (("V_ABD.pkl", os.path.join(K67_YOL["veri"], "V_ABD.pkl")), ("liste_abd.csv.gz", os.path.join(K67_YOL["pead"], "liste_abd.csv.gz"))):
        if not os.path.exists(y):
            raise K67Hata(f"veri yok: {y}")
        out[ad] = (sha(y), 1)
    out["k67_yahoo"] = k67_klasor_sha(K67_YOL["yahoo"])
    for a in ("FON_IZI.py", "K60.py", "K64.py"):
        y = os.path.join(KOK_K67, a)
        if not os.path.exists(y):
            raise K67Hata(f"içe alınan kod dosyası yok: {y}")
        out[a] = (sha(y), 1)
    return out


# ---------------------------------------------------------------- 7) CETVEL: FI_OLCUT (K64 yardımcılarıyla, aynen) + katmanlı ÜST - ALT
def k67_katmanli_fark(fu: np.ndarray, ayu: np.ndarray, ku: np.ndarray, fa: np.ndarray, aya: np.ndarray, ka: np.ndarray, B: int, tohum: int, guven: List[float],
                      gecerli_pay: float = 0.9, katman_min: int = 10) -> Dict[str, float]:
    """Katmanlı (EAR üçte biri içinde) ÜST - ALT: katman k'da d_k = ort(ÜST_k) - ort(ALT_k), ağırlık w_k = n_u n_a / (n_u + n_a) (Mantel-Haenszel tipi);
    tahmin = Σ w_k d_k / Σ w_k. Yalnız iki grubu da >= katman_min olan katmanlar (tam örneklemde seçilir, çekilişte sabit) girer. Ay kümeli bootstrap: aylar
    (iki grubun ortak ay kümesi) yerine koyarak çekilir; çekilişte bir grubu boş kalan katman o çekilişte düşer; hiç katman kalmayan çekiliş geçersiz.
    Döner: nokta, alt, ust, sd, p_ust = 1 - Φ(nokta / sd), p_alt, gecerli, n_ust, n_alt (giren katmanlarda), katman (giren katman sayısı)."""
    fu, fa = np.asarray(fu, float), np.asarray(fa, float); ku, ka = np.asarray(ku).astype(str), np.asarray(ka).astype(str); ayu, aya = np.asarray(ayu), np.asarray(aya)
    out: Dict[str, float] = {k: np.nan for k in ("nokta", "alt", "ust", "sd", "p_ust", "p_alt")}; out.update({"gecerli": 0, "n_ust": 0, "n_alt": 0, "katman": 0})
    giren = [k for k in sorted(set(ku) | set(ka)) if (ku == k).sum() >= int(katman_min) and (ka == k).sum() >= int(katman_min)]
    if not giren:
        return out
    mu, ma = np.isin(ku, giren), np.isin(ka, giren); fu, ayu, ku, fa, aya, ka = fu[mu], ayu[mu], ku[mu], fa[ma], aya[ma], ka[ma]
    out.update({"n_ust": int(len(fu)), "n_alt": int(len(fa)), "katman": len(giren)})
    kat = {k: i for i, k in enumerate(giren)}; K = len(giren)
    aylar, ters = np.unique(np.r_[ayu.astype(str), aya.astype(str)], return_inverse=True); M = len(aylar); iu, ia = ters[:len(fu)], ters[len(fu):]
    S = np.zeros((M, K, 2)); C = np.zeros((M, K, 2))
    np.add.at(S, (iu, [kat[k] for k in ku], 0), fu); np.add.at(C, (iu, [kat[k] for k in ku], 0), 1.0)
    np.add.at(S, (ia, [kat[k] for k in ka], 1), fa); np.add.at(C, (ia, [kat[k] for k in ka], 1), 1.0)

    def tahmin(Ss: np.ndarray, Cs: np.ndarray) -> np.ndarray:
        c0, c1 = Cs[..., 0], Cs[..., 1]; ok = (c0 > 0) & (c1 > 0)
        with np.errstate(invalid="ignore", divide="ignore"):
            d = np.where(ok, Ss[..., 0] / np.maximum(c0, 1) - Ss[..., 1] / np.maximum(c1, 1), 0.0); w = np.where(ok, c0 * c1 / np.maximum(c0 + c1, 1), 0.0)
            return np.where(w.sum(axis=-1) > 0, (w * d).sum(axis=-1) / np.maximum(w.sum(axis=-1), 1e-300), np.nan)
    out["nokta"] = float(tahmin(S.sum(axis=0), C.sum(axis=0)))
    sec = np.random.default_rng(int(tohum)).integers(0, M, (int(B), M)); v = tahmin(S[sec].sum(axis=1), C[sec].sum(axis=1)); gec = np.isfinite(v)
    out["gecerli"] = int(gec.sum())
    if gec.sum() >= gecerli_pay * int(B) and gec.sum() > 1:
        w = v[gec]; out["alt"], out["ust"] = (float(x) for x in np.percentile(w, guven)); sd = float(w.std(ddof=1)); out["sd"] = sd
        if sd > 0:
            out["p_ust"] = float(K60._k60_norm_p(out["nokta"] / sd)); out["p_alt"] = float(K60._k60_norm_p(-out["nokta"] / sd))
    return out


def _k67_fark_satiri(X: pd.DataFrame, mu: np.ndarray, ma: np.ndarray, ay: np.ndarray, Hu: Dict[str, Any], Ha: Dict[str, Any], temel: Dict[str, Any],
                     E: Dict[str, Any], katmanli: bool = True) -> Dict[str, Any]:
    """Bir karşıtlığın (ÜST rolü mu, ALT rolü ma) ölçüleri: ham ÜST - ALT (K64.k64_grup_farki), katmanlı ÜST - ALT (EAR üçte biri; S1 karar istatistiği), 20
    gün sürümleri, 'ek katkı' kuralı. katmanli = False (S2): karar istatistiği ham fark, kural K64.k64_ek_katki (ÜST > temel ve aralık; K64 §4)."""
    S1 = E["s1"]; f = X.fark.to_numpy(float); f20 = X.fark20.to_numpy(float); v20 = np.isfinite(f20)
    gf = lambda a, b, x: K64.k64_grup_farki(x[a], ay[a], x[b], ay[b], S1["bootstrap"], S1["tohum"], S1["guven"], S1["gecerli_pay"])  # noqa: E731
    ham = gf(mu, ma, f); ham20 = gf(mu & v20, ma & v20, f20)
    out = {"n_ust": int(Hu.get("n", 0)), "n_alt": int(Ha.get("n", 0)), "n_temel": int(temel.get("n", 0)), "ort_ust": Hu.get("ort_fark", np.nan),
           "ort_alt": Ha.get("ort_fark", np.nan), "ort_temel": temel.get("ort_fark", np.nan), "nokta": ham["nokta"], "alt": ham["alt"], "ust": ham["ust"],
           "p_ham_ust": ham["p_ust"], "p_ham_alt": ham["p_alt"], "nokta20": ham20["nokta"], "alt20": ham20["alt"], "ust20": ham20["ust"],
           "tutar_UST": bool(Hu.get("tutar", False)), "tutar_ALT": bool(Ha.get("tutar", False)), "tutar_net_UST": bool(Hu.get("tutar_net", False)),
           "tutar_net_ALT": bool(Ha.get("tutar_net", False))}
    if katmanli:
        ke = X.ear_grup.to_numpy(str); kv = ke != ""
        kf = lambda a, b, x: k67_katmanli_fark(x[a], ay[a], ke[a], x[b], ay[b], ke[b], S1["bootstrap"], S1["tohum"], S1["guven"], S1["gecerli_pay"], S1["katman_min"])  # noqa: E731
        k = kf(mu & kv, ma & kv, f); k20 = kf(mu & kv & v20, ma & kv & v20, f20)
        out.update({"k_nokta": k["nokta"], "k_alt": k["alt"], "k_ust": k["ust"], "k_sd": k["sd"], "k_p_ust": k["p_ust"], "k_p_alt": k["p_alt"], "k_n_ust": k["n_ust"],
                    "k_n_alt": k["n_alt"], "k_katman": k["katman"], "k_gecerli": k["gecerli"], "k_nokta20": k20["nokta"], "k_alt20": k20["alt"], "k_ust20": k20["ust"]})
        olc = bool(k["n_ust"] >= S1["n_esik"] and k["n_alt"] >= S1["n_esik"] and np.isfinite(k["alt"]) and np.isfinite(k["ust"]))
        out.update({"olculebilir": olc, "ek_UST": bool(olc and k["alt"] > 0 and np.nan_to_num(ham["nokta"]) > 0),
                    "ek_ALT": bool(olc and k["ust"] < 0 and np.nan_to_num(ham["nokta"]) < 0)})
    else:
        e = K64.k64_ek_katki(out["n_ust"], out["n_alt"], out["ort_ust"], out["ort_alt"], out["ort_temel"], ham["alt"], ham["ust"], S1["n_esik"])
        out.update({"k_nokta": ham["nokta"], "k_alt": ham["alt"], "k_ust": ham["ust"], "k_sd": ham["sd"], "k_p_ust": ham["p_ust"], "k_p_alt": ham["p_alt"],
                    "k_n_ust": out["n_ust"], "k_n_alt": out["n_alt"], "k_katman": 0, "k_gecerli": ham["gecerli"], "k_nokta20": ham20["nokta"], "k_alt20": ham20["alt"],
                    "k_ust20": ham20["ust"], "olculebilir": e["olculebilir"], "ek_UST": e["UST"], "ek_ALT": e["ALT"]})
    return out


def _k67_ay(X: pd.DataFrame) -> np.ndarray:
    return pd.to_datetime(X.giris).dt.to_period("M").astype(str).to_numpy() if len(X) else np.array([], str)


def k67_s1(X: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """S1: ölçülmüş tekil bilanço olayları -> (hücre tablosu, karşıtlık tablosu). Hücreler: dönem x değişken x grup (TEMEL, KAYIT_VAR / KAYIT_YOK, KAPSAM,
    UST, ORTA, ALT; YON_UYUM kategorileri). UST / ALT ve karşıtlık grupları FI_OLCUT tam hücresiyle (K64.k64_hucre), ötekiler hafif ölçüyle."""
    E = E or K67_ESIK; c = float(E["maliyet"]["ABD"]); sat: List[Dict[str, Any]] = []; frk: List[Dict[str, Any]] = []
    if not len(X):
        return pd.DataFrame(), pd.DataFrame()
    X = X.reset_index(drop=True); ay = _k67_ay(X); gi = pd.to_datetime(X.giris); yu = X.YON_UYUM.to_numpy(str); kap = X.kapsama.to_numpy(bool)
    for dn, a, b in E["donem"]:
        md = ((gi >= a) & (gi <= b) & X.fark.notna()).to_numpy(); kim0 = {"kume": "S1", "donem": dn}
        temel = K64.k64_hucre(X[md], c) if md.any() else {"n": 0}
        sat.append({**kim0, "degisken": "", "grup": "TEMEL", **temel})
        for ad, m in (("KAYIT_VAR", md & kap), ("KAYIT_YOK", md & ~kap)):
            sat.append({**kim0, "degisken": "", "grup": ad, **(K64.k64_hafif(X[m]) if m.any() else {"n": 0})})
        for k in k67_kodlar(E, "S"):
            g = X[k + "_grup"].to_numpy(str); kim = {**kim0, "degisken": k}; H: Dict[str, Dict[str, Any]] = {}
            for ad, m in (("KAPSAM", md & (g != "")), ("UST", md & (g == "UST")), ("ORTA", md & (g == "ORTA")), ("ALT", md & (g == "ALT"))):
                H[ad] = (K64.k64_hucre(X[m], c) if ad in ("UST", "ALT") else K64.k64_hafif(X[m])) if m.any() else {"n": 0}
                sat.append({**kim, "grup": ad, **H[ad]})
            frk.append({**kim, **_k67_fark_satiri(X, md & (g == "UST"), md & (g == "ALT"), ay, H["UST"], H["ALT"], temel, E)})
        for cat in ("AO", "TO", "TU", "AU", "NOTR", "YOK"):
            m = md & (yu == cat)
            sat.append({**kim0, "degisken": "YON_UYUM", "grup": cat, **((K64.k64_hucre(X[m], c) if cat in ("AO", "TO", "TU", "AU") else K64.k64_hafif(X[m]))
                                                                        if m.any() else {"n": 0})})
        for kod, (u, al) in E["karsitlik"].items():
            mu, ma = md & (yu == u), md & (yu == al)
            Hu = K64.k64_hucre(X[mu], c) if mu.any() else {"n": 0}; Ha = K64.k64_hucre(X[ma], c) if ma.any() else {"n": 0}
            frk.append({**kim0, "degisken": kod, **_k67_fark_satiri(X, mu, ma, ay, Hu, Ha, temel, E)})
    return pd.DataFrame(sat), pd.DataFrame(frk)


def k67_s2(Y: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """S2: ölçülmüş K24 çöl olayları -> (hücre tablosu, COL_NET karşıtlığı). Hücreler: TEMEL (bütün çöl olayları), BILANCO_VAR / BILANCO_YOK, KAPSAM (NET
    sırası olan), UST, ORTA, ALT (NET çöl içi sırası). Karar istatistiği ham ÜST - ALT; kural K64.k64_ek_katki (K64 §4)."""
    E = E or K67_ESIK; c = float(E["maliyet"]["ABD"]); sat: List[Dict[str, Any]] = []; frk: List[Dict[str, Any]] = []
    if not len(Y):
        return pd.DataFrame(), pd.DataFrame()
    Y = Y.reset_index(drop=True); ay = _k67_ay(Y); gi = pd.to_datetime(Y.giris); g = Y.NET_grup.to_numpy(str); bl = Y.bilanco.to_numpy(bool)
    for dn, a, b in E["donem"]:
        md = ((gi >= a) & (gi <= b) & Y.fark.notna()).to_numpy(); kim = {"kume": "S2", "donem": dn, "degisken": "COL_NET"}
        temel = K64.k64_hucre(Y[md], c) if md.any() else {"n": 0}; sat.append({**kim, "grup": "TEMEL", **temel}); H: Dict[str, Dict[str, Any]] = {}
        for ad, m in (("BILANCO_VAR", md & bl), ("BILANCO_YOK", md & ~bl), ("KAPSAM", md & (g != "")), ("UST", md & (g == "UST")), ("ORTA", md & (g == "ORTA")),
                      ("ALT", md & (g == "ALT"))):
            H[ad] = (K64.k64_hucre(Y[m], c) if ad in ("UST", "ALT") else K64.k64_hafif(Y[m])) if m.any() else {"n": 0}
            sat.append({**kim, "grup": ad, **H[ad]})
        frk.append({**kim, **_k67_fark_satiri(Y, md & (g == "UST"), md & (g == "ALT"), ay, H["UST"], H["ALT"], temel, E, katmanli=False)})
    return pd.DataFrame(sat), pd.DataFrame(frk)


def k67_karar(Fk: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Karar tablosu (değişken x yön). BH %10 ailesi = ölçülebilen bütün (aile değişkeni x yön x bağımsız dönem) hipotezleri (p = k_p_ust / k_p_alt; S1'de katmanlı,
    S2'de ham). 'ADAY' <=> iki bağımsız dönemde de o yönde 'ek katkı VAR' ve BH'den geçiyor; bağımsız dönemlerden biri ölçülemiyorsa 'ÖLÇÜLEMEZ'; aksi 'İZ DEĞİL'.
    İŞARET: ölçülebilen bütün hücrelerde (üç dönem) karar istatistiğinin işareti yönle aynı olmalı; değilse aday düşer. Genel karar en fazla 'ABD-ADAY' (Avrupa
    ve BIST verisi yok)."""
    E = E or K67_ESIK; q = E["coklu"]["bh_q"]; bag = list(E["bagimsiz"]); aile = list(E["aile"])
    if not len(Fk):
        return pd.DataFrame()
    A = Fk[Fk.degisken.isin(aile)]; hip = []
    for r in A.to_dict("records"):
        for yon in ("UST", "ALT"):
            olc = bool(r["olculebilir"])
            hip.append({"degisken": r["degisken"], "yon": yon, "donem": r["donem"], "olculebilir": olc, "ek": bool(r[f"ek_{yon}"]),
                        "p": float(r["k_p_ust" if yon == "UST" else "k_p_alt"]) if olc else np.nan, "nokta": float(r["k_nokta"]) if pd.notna(r["k_nokta"]) else np.nan,
                        "tutar": bool(r[f"tutar_{yon}"]), "tutar_net": bool(r[f"tutar_net_{yon}"])})
    Hp = pd.DataFrame(hip)
    if not len(Hp):
        return pd.DataFrame()
    am = (Hp.donem.isin(bag) & Hp.olculebilir).to_numpy(); Hp["bh"] = False; Hp["bonferroni"] = False; m = int(am.sum())
    if m:
        Hp.loc[am, "bh"] = K60.k60_bh(Hp.p.to_numpy(float)[am], q); Hp.loc[am, "bonferroni"] = Hp.p.to_numpy(float)[am] * m <= q
    out = []
    for (k, yon), g in Hp.groupby(["degisken", "yon"], sort=False):
        isa = 1.0 if yon == "UST" else -1.0; olc = g[g.olculebilir]; gp = g.set_index("donem"); b = [gp.loc[d] for d in bag if d in gp.index]
        tutarli = bool(len(olc) and (np.sign(olc.nokta.to_numpy(float)) == isa).all())
        if len(b) < len(bag) or not all(bool(x.olculebilir) for x in b):
            pk = "ÖLÇÜLEMEZ"
        elif all(bool(x.ek) and bool(x.bh) for x in b):
            pk = "ADAY"
        else:
            pk = "İZ DEĞİL"
        karar = ("ABD-ADAY (İZ için Avrupa verisi yok; BIST VERİSİ YOK)" if pk == "ADAY" and tutarli else
                 "ÖLÇÜLEMEZ (bağımsız dönem hücresinde n < 30)" if pk == "ÖLÇÜLEMEZ" else "İZ DEĞİL")
        out.append({"degisken": k, "yon": yon, "aile_m": m, "abd": pk, "isaret_tutarli": tutarli, "karar": karar,
                    "ek": "/".join("E" if (d in gp.index and bool(gp.loc[d].ek)) else "h" for d, _a, _b in E["donem"]),
                    "bh": "/".join("E" if (d in gp.index and bool(gp.loc[d].bh)) else "h" for d in bag),
                    "bonferroni": "/".join("E" if (d in gp.index and bool(gp.loc[d].bonferroni)) else "h" for d in bag),
                    "p": "/".join(f"{float(gp.loc[d].p):.4f}" if (d in gp.index and np.isfinite(float(gp.loc[d].p))) else "—" for d in bag),
                    "dort_sart": bool(len(gp) == len(E["donem"]) and gp.tutar.astype(bool).all()),
                    "dort_sart_net": bool(len(gp) == len(E["donem"]) and gp.tutar_net.astype(bool).all())})
    return pd.DataFrame(out)


# ---------------------------------------------------------------- 8) ÖN KAYIT
def _k67_y(x: Any, n: int = 1) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return ("%" + f"{100 * v:.{n}f}".replace(".", ",")) if np.isfinite(v) else "—"


def k67_kapsam_notu(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """Kapsam sayımının ön kayıt metnine giren özeti (yalnız SAYI). Mühre girmez (eşik değil)."""
    E = E or K67_ESIK; yk, yo = _k67_yol("kapsam", cikti), _k67_yol("kapsam_ozet", cikti)
    if not (os.path.exists(yk) and os.path.exists(yo)):
        return "Kapsam sayımı henüz koşulmadı (`python -I K67.py kapsam`)."
    K = pd.read_csv(yk); O = K60._k60_json_oku(yo); V = O.get("veri", {}); par = [f"Kapsam sayımı ({O.get('zaman', '?')}; `python -I K67.py kapsam`; yalnız SAYI: "
                                                                                    "getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).\n"]
    if V:
        nt, tk, nq = V.get("not", {}), V.get("takvim", {}), V.get("nasdaq", {})
        par.append(f"- Fiyat evreni V_ABD: {V.get('hisse_fiyat')} hisse. Yahoo çekimi {V.get('cekim_ilk_utc')} .. {V.get('cekim_son_utc')} UTC; istek durumları {V.get('durum')}.")
        par.append(f"- Not günlüğü: {nt.get('kayit')} kayıt, {nt.get('hisse_kayitli')} hisse; ilk {nt.get('ilk')}, son {nt.get('son')} (ET); saat bilgisi olmayan kayıt payı "
                   f"{_k67_y(nt.get('tarih_yalniz_pay'), 2)}.")
        par.append(f"- Yahoo bilanço takvimi: {tk.get('satir')} satır, {tk.get('hisse')} hisse; {tk.get('ilk')} .. {tk.get('son')}; saat türü {tk.get('saat')}.")
        if nq:
            par.append(f"- Nasdaq K28 takvimi (çapraz denetim): {nq.get('satir')} satır ({nq.get('ilk')} .. {nq.get('son')}); Yahoo'da ±1 günde bulunan pay "
                       f"{_k67_y(nq.get('yahoo_eslesen_pay'))} (aynı gün {_k67_y(nq.get('ayni_gun_pay'))}); aynı aralıktaki Yahoo satırlarının Nasdaq'ta bulunan payı "
                       f"{_k67_y(nq.get('yahoo_nasdaqta_bulunan_pay'))}; analist sürprizinin işaret uyumu {_k67_y(nq.get('surpriz_isaret_uyum'))} "
                       f"({nq.get('surpriz_karsilastirilan')} çift).")
        par.append("\n**Not günlüğü yıl yıl** (kayıt / hisse / yeni hedef dolu / önceki hedef dolu / tavsiye yükseltme / düşürme / yeni kapsama)\n\n| yıl | kayıt | hisse | hedef | önceki hedef | up | down | init |\n|---|---|---|---|---|---|---|---|")
        for y, v in sorted(nt.get("yil", {}).items(), key=lambda x: int(x[0])):
            par.append(f"| {y} | {v['kayit']} | {v['hisse']} | {_k67_y(v['hedef_dolu'])} | {_k67_y(v['eski_hedef_dolu'])} | {v['up']} | {v['down']} | {v['init']} |")
        par.append("\n**Yahoo bilanço takvimi yıl yıl** (satır / hisse / analist sürprizi dolu / EPS tahmini dolu)\n\n| yıl | satır | hisse | sürpriz | EPS tahmini |\n|---|---|---|---|---|")
        for y, v in sorted(tk.get("yil", {}).items(), key=lambda x: int(x[0])):
            if int(y) >= 2015:
                par.append(f"| {y} | {v['satir']} | {v['hisse']} | {_k67_y(v['surpriz_dolu'])} | {_k67_y(v['eps_tahmin_dolu'])} |")
    oy = O.get("olay_yil", {})
    if oy:
        par.append("\n**Bilanço olayları yıl yıl (karar günü d'nin yılı)** (ham / tekil / pencere = girişi var ve 60 günlük penceresi 31.08.2026'dan önce biten tekil / "
                   "pencerede en az bir kurum kaydı / NET tanımlı)\n\n| yıl | ham | tekil | pencere | revizyon kaydı var | NET tanımlı |\n|---|---|---|---|---|---|")
        for y, v in sorted(oy.items(), key=lambda x: int(x[0])):
            par.append(f"| {y} | {v['ham']} | {v['tekil']} | {v['pencere']} | {v['kapsama']} ({_k67_y(v['kapsama'] / max(v['pencere'], 1))}) | {v['NET']} |")
    A = K[(K.kume == "S1") & (K.degisken == "(olay)")]
    par.append("\n**S1 olayları (giriş dönemine göre)**\n\n| dönem | ham | tekil | pencere | revizyon kaydı var (pay) | hissenin geçmiş kaydı var | EAR var | sürpriz kaynağı Yahoo / Nasdaq / EAR / yok |\n"
               "|---|---|---|---|---|---|---|---|")
    for r in A.itertuples():
        par.append(f"| {r.donem} | {int(r.n_ham)} | {int(r.n_tekil)} | {int(r.n_pencere)} | {int(r.n_kapsama)} ({_k67_y(r.kapsama_pay)}) | {int(r.n_gecmis)} | {int(r.n_ear)} | "
                   f"{int(r.surpriz_YAHOO)} / {int(r.surpriz_NASDAQ)} / {int(r.surpriz_EAR)} / {int(r.surpriz_YOK)} |")
    par.append("\n**S1 değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; hücre = değer / ÜST / ORTA / ALT; köşeli parantez = EAR katmanı olan ÜST / ALT, "
               "katmanlı karar istatistiğine girecek olanlar)\n\n| değişken | " + " | ".join(d[0] for d in E["donem"]) + " |\n|---|" + "---|" * len(E["donem"]))
    for k in k67_kodlar(E, "S"):
        h = []
        for d in E["donem"]:
            x = K[(K.kume == "S1") & (K.degisken == k) & (K.donem == d[0])]
            h.append("—" if not len(x) else f"{int(x.n_deger.iloc[0])} / {int(x.n_ust.iloc[0])} / {int(x.n_orta.iloc[0])} / {int(x.n_alt.iloc[0])} "
                                            f"[{int(x.n_ust_k.iloc[0])} / {int(x.n_alt_k.iloc[0])}]")
        par.append(f"| {k} | " + " | ".join(h) + " |")
    par.append("\n**Katman (EAR üçte biri) x grup** (ÜST grubu UST / ORTA / ALT katmanında; ALT grubu aynı; pencereli tekil olaylar)\n\n| değişken | dönem | ÜST: EAR üst / orta / alt | ALT: EAR üst / orta / alt |\n|---|---|---|---|")
    for k in k67_kodlar(E, "S"):
        for d in E["donem"]:
            x = K[(K.kume == "S1") & (K.degisken == k) & (K.donem == d[0])]
            if len(x):
                x = x.iloc[0]
                par.append(f"| {k} | {d[0]} | {int(x.ust_UST)} / {int(x.ust_ORTA)} / {int(x.ust_ALT)} | {int(x.alt_UST)} / {int(x.alt_ORTA)} / {int(x.alt_ALT)} |")
    par.append("\n**YON_UYUM kategorileri** (AO / TO / TU / AU / NOTR / YOK; köşeli parantez = EAR katmanı olan AO / TO / TU / AU)\n\n| dönem | sayılar | katmanlı |\n|---|---|---|")
    for r in K[(K.kume == "S1") & (K.degisken == "YON_UYUM")].itertuples():
        par.append(f"| {r.donem} | {int(r.n_AO)} / {int(r.n_TO)} / {int(r.n_TU)} / {int(r.n_AU)} / {int(r.n_NOTR)} / {int(r.n_YOK)} | "
                   f"[{int(r.n_AO_k)} / {int(r.n_TO_k)} / {int(r.n_TU_k)} / {int(r.n_AU_k)}] |")
    S2 = K[K.kume == "S2"]
    if len(S2):
        par.append("\n**S2 çöl x revizyon** (K24 tekil çöl olayları, pencereli; son 60 işlem gününde bilanço karar günü olan; NET tanımlı; NET çöl içi ÜST / ORTA / ALT)\n\n"
                   "| dönem | çöl olayı | bilanço var | NET var | ÜST / ORTA / ALT |\n|---|---|---|---|---|")
        for r in S2.itertuples():
            par.append(f"| {r.donem} | {int(r.n_pencere)} | {int(r.n_bilanco)} | {int(r.n_deger)} | {int(r.n_ust)} / {int(r.n_orta)} / {int(r.n_alt)} |")
    az = []
    for k in k67_kodlar(E, "S"):
        for d in E["bagimsiz"]:
            x = K[(K.kume == "S1") & (K.degisken == k) & (K.donem == d)]
            if len(x) and (int(x.n_ust_k.iloc[0]) < E["s1"]["n_esik"] or int(x.n_alt_k.iloc[0]) < E["s1"]["n_esik"]):
                az.append(f"{k} {d}")
    for kod, (u, a) in E["karsitlik"].items():
        for d in E["bagimsiz"]:
            x = K[(K.kume == "S1") & (K.degisken == "YON_UYUM") & (K.donem == d)]
            if len(x) and (int(x[f"n_{u}_k"].iloc[0]) < E["s1"]["n_esik"] or int(x[f"n_{a}_k"].iloc[0]) < E["s1"]["n_esik"]):
                az.append(f"{kod} {d}")
    for d in E["bagimsiz"]:
        x = S2[S2.donem == d]
        if len(x) and (int(x.n_ust.iloc[0]) < E["s1"]["n_esik"] or int(x.n_alt.iloc[0]) < E["s1"]["n_esik"]):
            az.append(f"COL_NET {d}")
    par.append(f"\nBağımsız dönemlerde grubu n < {E['s1']['n_esik']} olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak; ölçülebilen olay daha az olabilir) hücreler: "
               + ("; ".join(az) if az else "yok") + ".")
    return "\n".join(par)


def k67_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: str, E: Optional[Dict[str, Any]] = None) -> str:
    E = E or K67_ESIK; O = E["olay"]; R = E["rev"]; S = E["sira"]; S1 = E["s1"]; FO = FI.FI_OLCUT
    vs = "\n".join(f"- {k}: sha256 {v[0]} ({v[1]} dosya)" for k, v in veri_sha.items()) or "- (veri dosyası bulunamadı)"
    dg = "\n".join(f"| {d['kod']} | {'sürekli' if d['tur'] == 'S' else 'kategorik'} | {d['tanim']} |" for d in E["degisken"])
    dn = ", ".join(f"{a} ({b} .. {c})" for a, b, c in E["donem"])
    return f"""# K67 — BİLANÇO SONRASI ANALİST REVİZYONLARI: ÖN KAYIT (ölçümden ÖNCE)

{K67_SURUM}
Yazım zamanı: {zaman}
ESIK_SHA256: {k67_esik_sha(E)}

Bu dosya gerçek veride revizyona bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `indir` ve `kapsam` sayımı koşuldu: §15). `python -I K67.py kos`
bu dosya git'e işlenmeden, işlendikten sonra değişmişse, mühür ya da veri sha256'ları tutmazsa çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
{vs}
k67_yahoo = /tmp/k67_yahoo içindeki not/*.json.gz + takvim/*.html.gz (göreli yol + dosya sha256, sıralı; gzip başlığı sabit). Önbellek repoya konmaz.

## 0. Soru (Cemal'in isteği, aynen)
"Bilanço sonrasında analistlerin EPS ve hedef fiyat tahminlerinde meydana gelen değişimleri ölç: yukarı revizyon yapan analist sayısı, aşağı revizyon yapan analist
sayısı, net revizyon oranı, revizyonların büyüklüğü, analistlerin görüş birliği veya ayrışması, revizyonun bilanço sürpriziyle aynı veya ters yönde olması. Veri yoksa
tahmin üretme; hangi veri sağlayıcısında hangi tarihsel alanın eksik olduğunu belirt."
İki soru: (S1) bu ölçüler bilanço olaylarında sonraki 60 (ve 20) günlük eşli farkı açıklıyor mu, bilanço sürprizini (tepki) kontrol ettikten sonra da? (S2) çöl
sinyaline ek bilgi taşıyorlar mı?

## 1. Veri kaynakları: hangi sağlayıcıda hangi tarihsel alan VAR / YOK
| alan | sağlayıcı | durum (bu işte) | tarihsel derinlik | not |
|---|---|---|---|---|
| hedef fiyat değişimi (kurum, önceki / yeni hedef, yayım anı) | Yahoo not günlüğü (quoteSummary upgradeDowngradeHistory; yfinance upgrades_downgrades) | **VAR, kullanılıyor** | 2012 -> bugün (§15 yıl tablosu) | ücretsiz; resmî olmayan uç; 'bugünkü' görüntü (çekim günü §15); geçmiş kayıtların sonradan eklenip değiştirilmediği doğrulanamaz |
| tavsiye değişimi (up / down / main / reit / init; önceki / yeni not) | Yahoo not günlüğü | **VAR, kullanılıyor** | aynı | önceki tavsiye alanı yıllara göre boş olabilir (K51: 2020-22 %20-25 dolu); eylem alanı her kayıtta dolu |
| analist KİŞİ kimliği | Yahoo | **YOK** | — | yalnız kurum adı; 'analist sayısı' = KURUM sayısı |
| EPS tahmini, analist bazında tarih damgalı seri | Yahoo | **YOK** | — | Yahoo'da yalnız güncel anlık görüntü (earningsTrend / epsRevisions: şimdi, 7 / 30 / 60 / 90 gün önce; yukarı / aşağı revizyon sayısı 7 / 30 gün); geçmiş görüntü saklanmıyor |
| EPS konsensüs revizyonu (çeyreklik donmuş görüntü: 7 / 30 / 60 / 90 gün önceki ortalama, 7 ve 30 günde yukarı / aşağı revizyon sayısı, analist sayısı, en yüksek / en düşük) | Alpha Vantage EARNINGS_ESTIMATES | **VERİ YOK (bu işte)** | 2017-06 -> (K63, demo anahtar IBM) | ücretsiz katman anahtar + günde 25 istek (1.411 hisse = 57 gün); kayıt / anahtar yasak. Ücretli seçenek: 49,99 $ / ay (75 istek / dk, ~1 saatte iner). Görüntünün alındığı gün dosyada YOK (sızıntı riski ayrıca sınanmalı) |
| aynı yapıda EPS revizyon görüntüsü | EODHD Fundamentals 'Earnings Trend' | **VERİ YOK (bu işte)** | 2017-06 -> (demo AAPL) | 59,99 $ / ay |
| analist bazında EPS / gelir tahmini tam geçmişi (nokta-zaman) | I/B/E/S (LSEG / WRDS), FactSet, Bloomberg, Capital IQ | **VERİ YOK** | 1976 -> | kurumsal; bireysel erişim yok |
| gelir (satış) tahmini revizyonu | Yahoo / ücretsiz | **YOK** | — | Alpha Vantage / EODHD görüntüsünde revenue_estimate var (ücretli yol) |
| bilanço açıklama günü + saati (ET; saat çözünürlüğü) | Yahoo bilanço takvimi (finance.yahoo.com/calendar/earnings?symbol=) | **VAR, olay kaynağı** | 25 yıla kadar (100 satır) | saat 'at 4 PM' biçiminde (dakika yok) |
| analist EPS sürprizi (tahmin, gerçekleşen, sürpriz %) | Yahoo bilanço takvimi | **VAR, birincil sürpriz** | §15 | eski yıllarda EPS tahmini boş, sürpriz dolu olabilir |
| bilanço günü + analist sürprizi | Nasdaq takvimi (K28; FON_IZI.fi_k28_liste_abd) | **VAR, çapraz denetim + yedek sürpriz** | 2022-12-01 -> 2026-10 | 2017-2021 YOK (SAPMA §14); saat alanı %99 'time-not-supplied' |
| BIST hedef fiyat / tavsiye / EPS revizyonu | İş Yatırım (güncel, 54 hisse), KAP (analist yok), Matriks (bulunamadı) | **BIST VERİSİ YOK** | — | K63; ABD bulgusu BIST'e GENELLENMEZ |
| Avrupa analist not günlüğü | Yahoo (denenmedi) | **AVRUPA VERİSİ YOK** | — | karar en fazla ABD-ADAY |

## 2. Olay (ABD bilanço açıklaması)
- Kaynak: Yahoo bilanço takvimi (tüm dönem; tek kaynak, iki bağımsız dönemde aynı). Evren: V_ABD.pkl (1.411 hisse; FON_IZI.fi_k1_veri; K64 ile aynı yükleyici
  K64.k64_fiyat_yukle, fon krizi kesiği {E['kriz']}). Açıklama günü {O['ilk_tarih']} .. {E['kriz']}.
- r0 = açıklamaya tepki veren ilk işlem günü (hissenin kendi işlem günleri): saat >= {O['kapanis_saat']}:00 ET (kapanış sonrası) -> açıklama gününden SONRAKİ ilk işlem günü;
  aksi (açılış öncesi, gün içi, saat yok = 'at 12 AM') -> açıklama günü ya da sonraki ilk işlem günü. r0 açıklama gününden {O['r0_azami_gun']} takvim gününden uzaksa olay yok (hisse işlem görmüyor).
- KARAR GÜNÜ d = r0'dan itibaren {O['karar_gun']}. işlem günü (d = r0 + {O['karar_gun'] - 1}) KAPANIŞI. GİRİŞ = d'den sonraki ilk işlem günü AÇILIŞI (FI_OLCUT girişi).
- REVİZYON PENCERESİ = [açıklama anı, d günü {O['kapanis_saat']}:00 ET]. Açıklama anı = takvimdeki saat (ET); saat yoksa açıklama günü 00:00 ET. Not kaydının yayım anı (epoch, UTC ->
  America/New_York) pencere içinde olmalı. Saat bilgisi olmayan kayıt (epoch tam UTC gece yarısı) {R['tarih_yalniz']} (d günündeyse pencereye girmez).
- TEKİLLEŞTİRME: aynı hissede r0'lar arası {O['tekil_gun']} işlem gününden yakın olay tek olaydır; son TUTULAN olaydan en az {O['tekil_gun']} işlem günü sonra gelen ilk olay tutulur
  (K64.k64_tekil). Aynı hisse-gün birden çok takvim satırı -> sürprizi dolu olan ilk satır.
- Dönem ataması GİRİŞ gününe göre: {dn}. Bağımsız dönemler: {', '.join(E['bagimsiz'])}; 2023-2026 örtüşür (bilgi; BH ailesine girmez).

## 3. Değişkenler (yalnız revizyon penceresindeki kayıtlar; hepsi <= d kapanışı)
KURUM YÖNÜ (bir kurumun penceredeki kayıtları zaman sırasıyla): ORAN = penceredeki son (hedefi olan) kaydın hedefi / pencerenin ilk (önceki hedefi olan) kaydının önceki
hedefi - 1; (1 + ORAN) [{R['oran_sinir'][0]:.4f}, {R['oran_sinir'][1]:.1f}] dışındaysa AYKIRI (olası bölünme / veri hatası; oran yok sayılır). YÖN: ORAN sonlu ve != 0 ise işareti;
değilse hedef eylemleri toplamı ({json.dumps(R['hedef_eylem'])}) işareti; değilse tavsiye eylemleri toplamı ({json.dumps(R['tavsiye_eylem'])}) işareti; değilse bütün kayıtlar
{R['baslangic']} ise BASLA (yeni kapsama; NET paydasına girmez), aksi AYNI. Hedef fiyat yönü tavsiye yönünden önce gelir (çelişkide hedef). Yahoo hedef 0 = yok.
Kurum adı boş kayıt sayılmaz. AYNI yönlü bir kurumun oranı 0 ise (hedefini korumuş) BUYUKLUK ve AYRISMA'ya 0 olarak girer.

| kod | tür | tanım |
|---|---|---|
{dg}

KAPSAMA sınıfı (bilgi): pencerede hiç kurum kaydı olmayan olay KAYIT_YOK; değişkenler NaN (sıfır sayılmaz). 'Hissenin geçmiş kaydı' = pencere sonuna kadar en az bir kayıt.
EPS REVİZYONU: VERİ YOK (§1). Vekil (fiyat tepkisinden, hedef fiyattan EPS türetme vb.) ÜRETİLMEZ.

## 4. Bilanço sürprizi ve tepki
- SÜRPRİZ (YON_UYUM için): Yahoo analist EPS sürprizi % (birincil); yoksa Nasdaq K28 sürprizi (aynı hisse, ±1 gün); yoksa tepki EAR. Kaynak olay başına kaydedilir.
- TEPKİ EAR (katman için; K28 tanımı): {E['surpriz']['ear']}. b <= d her zaman (geleceğe bakmaz).

## 5. Sıra ve gruplar (geleceğe bakmaz)
- OLAY İÇİ SIRA (K64.k64_ic_sira, aynen): olayın değeri, karar günü g için [g - {S['ic_gun']} gün, g] aralığındaki tekil bilanço olaylarının (kendisi ve aynı gün dahil) değerleri
  içinde (küçük + 0,5 x eşit) / n; n >= {S['ic_min']}. ÜST = sıra >= 2/3, ALT = sıra <= 1/3, ORTA arası (K64.k64_grup). Eşit değerler (sayımlarda sık) ortalama sıra alır.
- EAR aynı kuralla üçte bire ayrılır (KATMAN: UST / ORTA / ALT).
- S2'de NET'in ÇÖL İÇİ sırası: aynı kural, çöl olaylarının sinyal günleri üzerinden (K64 §4 'İÇ' sırası).

## 6. S1 — bilanço olaylarında revizyon (asıl soru)
- Örneklem: tekil, girişi olan, FI_OLCUT ile ölçülebilen bilanço olayları. Temel = dönemdeki bütün olaylar.
- Her sürekli değişken (N_UP, N_DOWN, NET, BUYUKLUK, AYRISMA): ÜST ve ALT üçte birin FI_OLCUT hücresi (60 gün; ek 20 gün), ham ÜST - ALT (K64.k64_grup_farki: ay kümeli
  bootstrap, {S1['bootstrap']} çekiliş, tohum {S1['tohum']}, %{S1['guven'][0]}-%{S1['guven'][1]}) ve **KATMANLI ÜST - ALT** (karar istatistiği; 'ek katkı' = sürpriz kontrolü): EAR üçte biri
  içinde ort(ÜST) - ort(ALT), ağırlık n_u n_a / (n_u + n_a); iki grubu da >= {S1['katman_min']} olan katmanlar; aynı ay kümeli bootstrap (aynı tohum). p = 1 - Φ(nokta / sd).
- YON_UYUM: kategori hücreleri (AO, TO, TU, AU tam; NOTR, YOK hafif) ve iki karşıtlık: YU_POZ = AO - TO (olumlu sürprizde revizyonun yukarı olması),
  YU_NEG = TU - AU (olumsuz sürprizde revizyonun yukarı olması); aynı katmanlı istatistik.
- KAYIT_VAR / KAYIT_YOK (bilgi; karara girmez).
- 'EK KATKI VAR (ÜST yönü)' <=> katmanlı n_ÜST >= {S1['n_esik']} ve n_ALT >= {S1['n_esik']}, katmanlı aralık var, katmanlı %95 alt sınır > 0 VE ham ÜST - ALT > 0.
  ALT yönü ayna (katmanlı üst sınır < 0 ve ham < 0).

## 7. S2 — çöl etkileşimi
- Olay: K24 çöl sinyali (K64.k64_olay_k24, DEĞİŞTİRİLMEDEN; FI_K24 eşikleri; tekil, girişi olan). Çöl olayının sinyal günü t'ye kadar son {E['s2']['pencere']} işlem gününde
  (t dahil) karar günü d olan EN SON tekil bilanço olayının değişkenleri alınır (d <= t: bilgi sinyal gününde biliniyor). Yoksa BILANCO_YOK.
- Değişken: NET (COL_NET); çöl içi sıra (§5) ile ÜST / ALT. Karar istatistiği HAM ÜST - ALT; kural K64.k64_ek_katki (K64 §4): ÜST grubunun ortalama eşli farkı > temel
  (bütün çöl olayları) VE %95 alt sınır > 0; ALT ayna. Katmanlama yok (çöl örneklemi küçük).

## 8. Cetvel (FI_OLCUT, aynen)
{json.dumps(FO, ensure_ascii=False)}. Olay başına r60 = giriş açılışından 60. gün kapanışına; eşli fark = r60 - aynı giriş günü, aynı 60 gün momentum beşliği x likidite
üçlüsündeki öteki hisselerin ortalaması (FI.fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre; K64.k64_olc / k64_hucre ile). Hücre dört şartı: n >= 30, %95 alt > 0,
sıra > 0,50, slot portföyü > 200 eşli rastgele portföyün %90'ı. Ek ufuk {E['ek_ufuk']} gün (aynı yöntem). Maliyet: ABD gidiş-dönüş {E['maliyet']['ABD'] * 1e4:.0f} bp (her olayın
getirisinden ve eşli farkından düşülür; rastgele eş portföyler maliyetsiz: tutucu). Fon krizi: 60 günlük penceresi {E['kriz']}'i aşan olay ölçülmez.

## 9. Karar
- Aile değişkenleri: {', '.join(E['aile'])}. Her biri İKİ YÖNDE (ÜST daha iyi / ALT daha iyi).
- Pazar kararı (ABD): 'ADAY' <=> iki bağımsız dönemin İKİSİNDE de o yönde 'ek katkı VAR' ve BH'den geçiyor. Bağımsız dönemlerden biri ölçülemiyorsa (n < {S1['n_esik']} ya da aralık yok)
  'ÖLÇÜLEMEZ'. Aksi 'İZ DEĞİL'.
- İŞARET: ölçülebilen bütün dönem hücrelerinde (2023-2026 dahil) karar istatistiğinin işareti yönle aynı olmalı; bir hücrede dönerse aday düşer -> İZ DEĞİL.
- Genel karar en fazla **ABD-ADAY** (İZ için Avrupa verisi yok; BIST VERİSİ YOK). Grup hücresinin FI_OLCUT dört şartı (brüt / net) bilgi olarak yazılır.

## 10. Çoklu test
BH q = %{100 * E['coklu']['bh_q']:.0f}; aile = ölçülebilen bütün (aile değişkeni x yön x bağımsız dönem) hipotezleri: en çok {len(E['aile'])} x 2 x {len(E['bagimsiz'])} = {len(E['aile']) * 2 * len(E['bagimsiz'])}.
Bonferroni bilgi olarak yazılır. 2023-2026 ve 20 gün sonuçları aileye girmez.

## 11. Güç
K58 (FI_OLCUT plasebo): δ = +%2 etkiyi tek hücrenin dört şartı n = 30 / 100 / 300 / 1000 / 3000'de %4 / %8 / %11 / %13 / %21 olasılıkla görür; cetvel yalnız büyük etkiyi
görür. ÜST - ALT için kaba saptanabilir en küçük etki ≈ 2,8 x σ x √(1/n_ÜST + 1/n_ALT); σ (60 gün tek hisse eşli fark standart sapması) VARSAYIM ≈ 0,25 (ölçülmedi) ->
n 1.000 / 1.000: ≈ %3,1; n 300 / 300: ≈ %5,7; ay kümelemesi bunu büyütür. Gerçek yarı genişlik koşuda raporlanır. 'İZ DEĞİL' = 'etki yok' değildir, 'bu cetvelle görülmedi'dir.

## 12. Geleceğe bakma
- Değişkenler yalnız yayım anı <= d günü 16:00 ET olan kayıtlarla; tarih-yalnız kayıt gün sonu sayılır. Giriş d+1 açılışı. EAR penceresi b <= d.
- Sıralar yalnız geçmiş 365 gün (ve aynı gün) olaylarıyla; katman da öyle.
- S2: bilanço karar günü d <= çöl sinyal günü t; giriş t'den sonraki ilk işlem günü (K64).
- Yahoo not günlüğü 'bugünkü' görüntüdür: geçmiş kayıtların sonradan eklenmiş / tarihinin düzeltilmiş / silinmiş olabileceği DOĞRULANAMAZ (geriye dönük yazım
  riski). Hedef fiyatlar kayıt anındaki değerdir; bölünme düzeltmesi yapılıp yapılmadığı belgelenmemiştir (AYKIRI kuralı §3).
- Yahoo bilanço takviminde geçmiş sürprizler sonradan düzeltilmiş olabilir (beyan).

## 13. Yanlılık
- YAŞAYAN yanlılığı: V_ABD bugün işlem gören hisseler; borsadan çıkanlar yok. Not günlüğü de bugünkü sembollerle çekildi (sembol değiştiren şirketin eski kayıtları
  eksik olabilir).
- Kapsama yanlılığı: analist kapsamı büyük / likit hissede yoğun; N_UP / N_DOWN kurum sayısıyla ölçeklenir (büyüklük etkisi). Eşli fark likidite üçlüsünü ve momentum
  beşlisini eşler; tam büyüklük kontrolü değildir (beyan).
- Kurum = 'analist' (kişi kimliği yok). Aynı kurumun aynı penceredeki birden çok kaydı tek yön sayılır.

## 14. SAPMA / BOŞLUK (iş tanımına göre)
- SAPMA 1 (olay kaynağı): iş tanımı 'Nasdaq takvimi' diyordu; Nasdaq K28 takvimi yalnız 2022-12-01'den başlıyor -> 2017-2021 bağımsız dönemi için bilanço günü YOK.
  Bu yüzden olay kaynağı iki dönemde de aynı olsun diye Yahoo bilanço takvimi (saat + analist sürprizi dahil) seçildi; Nasdaq çapraz denetim ve yedek sürpriz (§15
  örtüşme sayıları).
- SAPMA 2 (sürpriz): birincil sürpriz Yahoo (Nasdaq 2017-2021'de yok); EAR yalnız yedek ve katman.
- SAPMA 3 (karar günü): 'açıklamadan sonraki 5. işlem günü' = r0 + 4 (r0 tepki veren ilk gün = 1. gün) olarak sabitlendi.
- BOŞLUK: EPS tahmin revizyonu (analist bazında ya da konsensüs) VERİ YOK; gelir tahmini revizyonu VERİ YOK; BIST VERİSİ YOK; AVRUPA VERİSİ YOK; analist kişi kimliği YOK.

## 15. Kapsam (yalnız sayım; getiri yok)
{kapsam}

## 16. Koşu
1. `python K67.py indir`  (yapıldı; önbellek /tmp/k67_yahoo, sha256 yukarıda)
2. `python -I K67.py kapsam`  (yapıldı; sayılar §15)
3. ana oturum bu ön kaydı denetler ve git'e işler
4. `python -I K67.py kos` -> k67_olaylar.csv.gz, k67_s1.csv, k67_s1_fark.csv, k67_s2.csv, k67_karar.csv, k67_meta.json, K67_RAPOR.md
5. `python K67.py rapor` -> raporu çıktılardan yeniden yazar

## 17. Değişmezlik
K67_ESIK ya da içe alınan tanımlar (FI_OLCUT, FI_K24, K64 olay ayarları) değişirse ESIK_SHA256 değişir ve koşu durur. Veri (V_ABD.pkl, liste_abd.csv.gz, Yahoo önbelleği)
ya da içe alınan kod (FON_IZI.py, K60.py, K64.py) değişirse sha256 tutmaz ve koşu durur.
"""


def _k67_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    m = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", metin, re.M); z = re.search(r"^Yazım zamanı: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", metin, re.M)
    veri = {a: (h, int(n)) for a, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}) \((\d+) dosya\)$", metin, re.M)}
    return {"sha": m.group(1) if m else None, "zaman_utc": z.group(1) if z else "", "veri": veri}


def k67_onkayit(cikti: Optional[str] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ: mühür aynıysa yolu döndürür, değilse durur. veri_sha None ise veri özetleri hesaplanır (eksikse durur)."""
    yol = _k67_yol("onkayit", cikti); os.makedirs(os.path.dirname(yol), exist_ok=True)
    if os.path.exists(yol):
        mevcut = _k67_onkayit_oku(yol)["sha"]
        if mevcut != k67_esik_sha():
            raise K67Hata(f"ön kayıt zaten var ve mühür farklı ({mevcut} != {k67_esik_sha()}): eşikler ön kayıttan sonra değişmiş")
        k67log.info("ön kayıt zaten var (mühür aynı): %s", yol)
        return yol
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    metin = k67_onkayit_metin(zaman, k67_veri_sha() if veri_sha is None else veri_sha, k67_kapsam_notu(cikti))
    if _K67_EPOSTA.search(metin):
        raise K67Hata("ön kayıt metninde e-posta biçimli parça var; yazılmadı")
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    k67log.info("ön kayıt yazıldı: %s (mühür %s)", yol, k67_esik_sha()[:12])
    return yol


def k67_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = False, git: bool = False) -> Dict[str, Any]:
    """Mühür (her zaman), veri sha256'ları (veri=True) ve git'e işlenmişlik + işlendikten sonra değişmemişlik (git=True) doğrulanır; biri tutmazsa K67Hata."""
    yol = _k67_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise K67Hata(f"ön kayıt yok ({yol}): önce `python K67.py onkayit`")
    oc = _k67_onkayit_oku(yol)
    if oc["sha"] != k67_esik_sha():
        raise K67Hata(f"ön kayıt mührü tutmuyor ({oc['sha']} != {k67_esik_sha()}): eşikler ön kayıttan sonra değişmiş, koşu durdu")
    out = {"yol": yol, "sha": oc["sha"], "zaman_utc": oc["zaman_utc"], "dosya_sha256": K60._k60_sha(yol), "veri": oc["veri"]}
    if veri:
        simdi = k67_veri_sha()
        fark = sorted(k for k in set(simdi) | set(oc["veri"]) if tuple(simdi.get(k) or ()) != tuple(oc["veri"].get(k) or ()))
        if fark:
            raise K67Hata(f"veri / içe alınan kod ön kayıttakiyle aynı değil (sha256 ya da dosya sayısı farklı): {fark}; koşu durdu")
    if git:
        try:
            out["git"] = K60._k60_git_islenmis(yol, "K67 ön kaydı")
        except K60.K60Hata as ex:
            raise K67Hata(str(ex))
    return out


# ---------------------------------------------------------------- 9) KOŞU
def k67_kos(cikti: Optional[str] = None, git_sart: bool = True, girdi: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Tek koşu: ön kayıt (mühür + git) -> [gerçek veride veri sha256] -> olaylar -> değişkenler -> FI_OLCUT -> S1, S2 -> karar -> çıktılar + rapor. girdi / E
    yalnız testler içindir (sentetik girdi: veri sha256 doğrulaması atlanır; ön kayıt doğrulaması yine şarttır; girdi['col'] verilirse çöl olayları ondan)."""
    Ek = E or K67_ESIK; sentetik = girdi is not None; t0 = time.time()
    oc = k67_onkayit_dogrula(cikti, veri=not sentetik, git=git_sart)
    meta: Dict[str, Any] = {"surum": K67_SURUM, "onkayit": oc, "sentetik": sentetik, "kos_baslangic": _k67_simdi(), "isolated": bool(sys.flags.isolated),
                            "k67_kod_sha256": K60._k60_sha(os.path.join(KOK_K67, "K67.py")) if os.path.exists(os.path.join(KOK_K67, "K67.py")) else None,
                            "surumler": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__}}
    g = girdi if sentetik else k67_girdi(Ek); V = g["V"]
    X, Y = k67_hazirla(g, Ek); P = FI.fi_olcut_panel(V); P20 = FI.fi_olcut_panel(V, {**FI.FI_OLCUT, "ufuk": int(Ek["ek_ufuk"])})
    Xm = X[X.tekil & X.giris.notna()].reset_index(drop=True)
    Xm = K64.k64_olc(P, P20, Xm) if len(Xm) else Xm.assign(r60=np.nan, esli_r60=np.nan, sira=np.nan, fark=np.nan, r20=np.nan, fark20=np.nan)
    Ym = Y[Y.giris.notna()].reset_index(drop=True) if len(Y) else Y
    Ym = K64.k64_olc(P, P20, Ym) if len(Ym) else Ym.assign(r60=np.nan, esli_r60=np.nan, sira=np.nan, fark=np.nan, r20=np.nan, fark20=np.nan)
    S1, F1 = k67_s1(Xm, Ek); S2, F2 = k67_s2(Ym, Ek); Fk = pd.concat([F1, F2], ignore_index=True); Kr = k67_karar(Fk, Ek)
    meta["olay"] = {"bilanco_ham": int(len(X)), "bilanco_tekil": int(X.tekil.sum()) if len(X) else 0, "bilanco_olculen": int(Xm.fark.notna().sum()) if len(Xm) else 0,
                    "col": int(len(Y)), "col_olculen": int(Ym.fark.notna().sum()) if len(Ym) else 0}
    cik = cikti or K67_YOL["cikti"]; os.makedirs(cik, exist_ok=True)
    Xm.drop(columns=[c for c in ("_esler",) if c in Xm]).to_csv(_k67_yol("olay", cikti), index=False)
    pd.concat([S1, S2], ignore_index=True).to_csv(_k67_yol("s1", cikti), index=False); Fk.to_csv(_k67_yol("fark", cikti), index=False)
    Ym.drop(columns=[c for c in ("_esler",) if c in Ym]).to_csv(_k67_yol("s2", cikti), index=False); Kr.to_csv(_k67_yol("karar", cikti), index=False)
    meta["kos_bitis"] = _k67_simdi(); meta["sure_sn"] = round(time.time() - t0)
    with open(_k67_yol("meta", cikti), "w", encoding="utf-8") as f:
        json.dump(K60._k60_yuvarla(meta, 12), f, ensure_ascii=False, indent=1, default=str)
    return {"s1": S1, "s2": S2, "fark": Fk, "karar": Kr, "meta": meta, "rapor": k67_rapor(cikti, Ek)}


# ---------------------------------------------------------------- 10) RAPOR
def _k67_f(r: Dict[str, Any], k: str) -> float:
    try:
        v = r.get(k)
        return float(v) if v is not None and pd.notna(v) else np.nan
    except (TypeError, ValueError):
        return np.nan


def _k67_tam(x: Any) -> int:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 0
    return int(v) if np.isfinite(v) else 0


def _k67_evet(x: Any) -> bool:
    return str(x).strip().lower() in ("true", "1", "1.0")


def k67_rapor(cikti: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """K67_RAPOR.md'yi çıktı dosyalarından yazar: karar tablosu, temel, her değişkenin ÜST / ALT hücreleri (60 / 20 gün, ortalama / medyan, eşli fark, aralık,
    maliyet sonrası), ham ve katmanlı ÜST - ALT, YON_UYUM kategorileri, S2."""
    E = E or K67_ESIK; yol = {k: _k67_yol(k, cikti) for k in ("s1", "fark", "karar", "meta")}
    if not all(os.path.exists(y) for y in yol.values()):
        raise K67Hata(f"K67 çıktıları yok ({yol['s1']}): önce `python -I K67.py kos`")
    oku = lambda y: pd.read_csv(y) if os.path.getsize(y) > 2 else pd.DataFrame()  # noqa: E731
    S1, Fk, Kr = oku(yol["s1"]), oku(yol["fark"]), oku(yol["karar"])
    with open(yol["meta"], encoding="utf-8") as f:
        m = json.load(f)
    if len(S1):
        S1["degisken"] = S1["degisken"].fillna("")
    oc = m.get("onkayit", {})
    par = [f"# K67 — bilanço sonrası analist revizyonları: RAPOR\n\n{K67_SURUM}. Ön kayıt K67_ON_KAYIT.md (mühür {str(oc.get('sha'))[:12]}, dosya sha256 "
           f"{str(oc.get('dosya_sha256'))[:12]}, git {str((oc.get('git') or {}).get('commit', ''))[:7]}); koşu {m.get('kos_baslangic')} -> {m.get('kos_bitis')} ({m.get('sure_sn')} sn). "
           f"Olaylar: {json.dumps(m.get('olay', {}), ensure_ascii=False)}.\n",
           "EPS tahmin revizyonu: VERİ YOK (ücretsiz tarihsel kaynak yok; ücretli: Alpha Vantage 49,99 $ / ay, EODHD 59,99 $ / ay; kurumsal I/B/E/S). BIST VERİSİ YOK. "
           "AVRUPA VERİSİ YOK. Karar en fazla ABD-ADAY.\n"]
    if len(Kr):
        par.append("## Karar tablosu\n| değişken | yön | karar | ABD | ek katkı (3 dönem) | BH (bağımsız) | p (bağımsız) | işaret tutarlı | grup dört şart (brüt / net) |\n"
                   "|---|---|---|---|---|---|---|---|---|")
        for r in Kr.to_dict("records"):
            par.append(f"| {r['degisken']} | {'ÜST' if r['yon'] == 'UST' else 'ALT'} | {r['karar']} | {r['abd']} | {r['ek']} | {r['bh']} | {r['p']} | "
                       f"{'evet' if _k67_evet(r['isaret_tutarli']) else 'hayır'} | {'evet' if _k67_evet(r['dort_sart']) else 'hayır'} / {'evet' if _k67_evet(r['dort_sart_net']) else 'hayır'} |")
        par.append(f"\nBH ailesi m = {int(Kr.aile_m.iloc[0])}; q = %{100 * E['coklu']['bh_q']:.0f}.\n")
    hd = ("| küme | dönem | değişken | grup | n | ort. r60 | medyan r60 | ort. r20 | ort. eşli fark [%95] | medyan eşli fark | ort. eşli fark 20 g | net eşli fark | dört şart (brüt / net) |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    par.append("## Hücreler (temel, kapsama, gruplar)\n" + hd)
    for r in (S1.to_dict("records") if len(S1) else []):
        if r.get("grup") in ("ORTA",):
            continue
        n = _k67_tam(_k67_f(r, "n"))
        par.append(f"| {r['kume']} | {r['donem']} | {r['degisken'] or '—'} | {r['grup']} | {n} | {_k67_y(_k67_f(r, 'ort_r60'))} | {_k67_y(_k67_f(r, 'medyan_r60'))} | "
                   f"{_k67_y(_k67_f(r, 'ort_r20'))} | {_k67_y(_k67_f(r, 'ort_fark'))} [{_k67_y(_k67_f(r, 'alt95'))}; {_k67_y(_k67_f(r, 'ust95'))}] | {_k67_y(_k67_f(r, 'medyan_fark'))} | "
                   f"{_k67_y(_k67_f(r, 'ort_fark20'))} | {_k67_y(_k67_f(r, 'ort_fark_net'))} | "
                   f"{'tutar' if _k67_evet(r.get('tutar')) else 'tutmaz'} / {'tutar' if _k67_evet(r.get('tutar_net')) else 'tutmaz'} |")
    par.append("\n## ÜST - ALT (ham ve katmanlı; S2'de karar istatistiği ham)\n| değişken | dönem | n ÜST / ALT | ham ÜST - ALT [%95] | katmanlı [%95] (katman, n) | temel | 20 g ham / katmanlı | "
               "ölçülebilir | ek katkı |\n|---|---|---|---|---|---|---|---|---|")
    for r in (Fk.to_dict("records") if len(Fk) else []):
        ek = "ÖLÇÜLEMEZ" if not _k67_evet(r["olculebilir"]) else ("VAR (ÜST)" if _k67_evet(r["ek_UST"]) else ("VAR (ALT)" if _k67_evet(r["ek_ALT"]) else "yok"))
        par.append(f"| {r['degisken']} | {r['donem']} | {_k67_tam(_k67_f(r, 'n_ust'))} / {_k67_tam(_k67_f(r, 'n_alt'))} | {_k67_y(_k67_f(r, 'nokta'))} [{_k67_y(_k67_f(r, 'alt'))}; "
                   f"{_k67_y(_k67_f(r, 'ust'))}] | {_k67_y(_k67_f(r, 'k_nokta'))} [{_k67_y(_k67_f(r, 'k_alt'))}; {_k67_y(_k67_f(r, 'k_ust'))}] ({_k67_tam(_k67_f(r, 'k_katman'))}, "
                   f"{_k67_tam(_k67_f(r, 'k_n_ust'))} / {_k67_tam(_k67_f(r, 'k_n_alt'))}) | {_k67_y(_k67_f(r, 'ort_temel'))} | {_k67_y(_k67_f(r, 'nokta20'))} / {_k67_y(_k67_f(r, 'k_nokta20'))} | "
                   f"{'evet' if _k67_evet(r['olculebilir']) else 'hayır'} | {ek} |")
    par.append("\n## Sınırlar\nYahoo not günlüğü bugünkü görüntü (geriye dönük yazım doğrulanamaz); yaşayan yanlılığı (V_ABD bugünkü liste); 'analist' = kurum; EPS revizyonu VERİ YOK; "
               "'ÖLÇÜLEMEZ' = n < 30 (az veri), 'İZ DEĞİL' değildir. Ayrıntı K67_ON_KAYIT.md §12-§14.\n")
    metin = "\n".join(par); y = _k67_yol("rapor", cikti)
    if _K67_EPOSTA.search(metin):
        raise K67Hata("rapor metninde e-posta biçimli parça var; yazılmadı")
    with open(y, "w", encoding="utf-8") as f:
        f.write(metin)
    k67log.info("rapor: %s", y)
    return y


def _cakisma_kontrol_k67(_once=_CK_ONCE_K67, _dosya="K67.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K67", "_CK_KAYIT", "_cakisma_kontrol_k67", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "io", "gzip", "glob", "hashlib", "_dt", "annotations", "Any", "Callable", "Dict", "List",
           "Optional", "Tuple", "FI", "K60", "K64")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k67()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K67_SURUM)
    ap.add_argument("komut", choices=["onkayit", "indir", "kapsam", "kos", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--sinir", type=int, default=0, help="indir: yalnız ilk N sembol (pilot)")
    a_ = ap.parse_args()
    try:
        if a_.komut == "indir":
            S_ = k67_indir_semboller(); S_ = S_[:a_.sinir] if a_.sinir else S_
            R_ = k67_indir(S_); K60._k60_json_yaz(_k67_yol("indir_ozet", a_.cikti), {**R_, "zaman": _k67_simdi(), "surum": K67_SURUM})
            print(json.dumps(R_, ensure_ascii=False))
        elif a_.komut == "onkayit":
            y_ = k67_onkayit(a_.cikti); print(y_, "mühür", k67_esik_sha(), "dosya sha256", K60._k60_sha(y_))
        elif a_.komut == "kapsam":
            K_ = k67_kapsam(a_.cikti); print(K_.to_string(index=False)); print(_k67_yol("kapsam", a_.cikti))
        elif a_.komut == "kos":
            R_ = k67_kos(a_.cikti); print("K67 bitti:", json.dumps({"sure_sn": R_["meta"]["sure_sn"], "olay": R_["meta"]["olay"]}, ensure_ascii=False, default=str))
            print(R_["karar"].to_string(index=False) if len(R_["karar"]) else "(karar tablosu boş)"); print(R_["rapor"])
        else:
            print(k67_rapor(a_.cikti))
    except (K67Hata, K60.K60Hata, FileNotFoundError) as ex:
        k67log.error("%s", ex); sys.exit(1)
