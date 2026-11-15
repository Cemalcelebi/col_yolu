"""TAVAN_SERISI — çökmüş BIST hissesinde art arda tavan serisi: canlı tarama + geçmiş taban oranlar (13 Kasım 2026). Tek dosya.

Soru (Cemal, 13 Kasım 2026): fon krizinde (31.08.2026 sonrası) çok sert düşmüş (100'ler / 1000'ler TL'den ~1 TL'ye) hisselerin bir kısmı son günlerde
art arda tavan yapıyor (TEHOL, PEKER = PEKGY). (1) Bugün hangileri kaç gündür tavan gidiyor? (2) Geçmişte çökmüş bir hissede tavan serisi
başladığında, k. tavandan sonra katılmak ne getirmiş, ne kaybettirmiş; rastgele mi?

İŞ 1  CANLI (`canli`): evren ÇÖKMÜŞ = 1 Haz - 31 Ağu 2026 en yüksek kapanıştan 1 Eyl 2026 sonrası en düşük kapanışa düşüş >= %80. Ardışık tavan,
      son 20 günde tavan, kilitli tavan, hacim oranı, fon payı (K25 KAP fon raporları, kriz öncesi). Ölçüm değil, tarama (getiri yok).
İŞ 2  GEÇMİŞ (`onkayit` -> commit -> `kos`): BIST 2016 - 31.08.2026, seri öncesi kapanış 250 günlük en yüksekten >= %80 aşağıda (ÇÖKMÜŞ) iken
      k. ardışık tavan (k = 1, 2, 3, 4, 5, 6, 8, 10); giriş k. tavandan sonraki ilk işlem günü açılışı; kontrol aynı gün aynı derinlik
      kovasında çökmüş olup seri boyunca tavan yapmayan hisseler; karar cümlesi TS_ESIK['karar']'da (sha256 mührü ön kayıtta).
      Eylül - Kasım 2026 olayları yalnız BİLGİ (fon krizi; ayrı tablo, karara girmez).

Veri: Yahoo chart API günlük OHLCV (K60_veri.k60v_fiyat_indir; aynı uç, tarayıcı kimliği, kaldığı yerden sürme, sha256 manifesti), 2015-01-01'den,
      evren V_BIST.pkl sembolleri ∪ dol.pkl kodları (.IS). Fiyat bölünme (bedelsiz) düzeltmeli, temettüsüz; ekran fiyatı = Yahoo x sonraki
      bölünmeler çarpanı (K60_veri.k60v_bolunme_carpan) -> tavan fiyat adımı kuralı. V_BIST.pkl çapraz denetim için okunur.
      Fon payı: /tmp/veri/G.pkl + oran.pkl + dol.pkl, FON_IZI.fi_k25_pay_tablo (aynı hesap). Veri / pkl / csv repoya girmez.

Komut:  python TAVAN_SERISI.py indir            Yahoo fiyatları -> /tmp/tavan/yahoo (kaldığı yerden; TS_YAHOO_KLASOR ile değişir)
        python TAVAN_SERISI.py canli [--yenile]  İŞ 1: /tmp/tavan/canli_cokmus.csv + arastirma_cikti/tavan_serisi/CANLI_<tarih>.md
                                                (--yenile: canlı tablo için son günleri ayrı klasöre yeniden indirir)
        python TAVAN_SERISI.py onkayit          İŞ 2 ön kaydı (eşik mührü, kod / veri sha256; varsa üzerine yazmaz)
        python TAVAN_SERISI.py kos [--sapma G]  ön kayıt git'te ve mühür tutuyorsa ölçüm -> tavan_sonuc.json + TAVAN_RAPOR.md
        python TAVAN_SERISI.py rapor            raporu sonuç JSON'undan yeniden yazar
        python TAVAN_SERISI.py hacim onkayit    HACİM (Cemal'in itirazı: devasa hacim barı H1, dipte hacim H2, taban fiyat H3) ön kaydı
        python TAVAN_SERISI.py hacim kos [--sapma G]  mühür kapısı -> hacim_sonuc.json + HACIM_RAPOR.md + /tmp/tavan/grafik/*.png
        python TAVAN_SERISI.py hacim rapor      hacim raporunu sonuç JSON'undan yeniden yazar
Colab:  exec(open('TAVAN_SERISI.py').read())  (K60_veri.py, K57.py, FON_IZI.py aynı klasörde)
SINIR:  IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md'ye dokunmaz. Ağ yalnız `indir` / `canli --yenile`. Tiingo yok,
        e-posta / anahtar yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_TS = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_TS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_TS not in sys.path:
    sys.path.insert(0, KOK_TS)
import K60_veri as K60V  # noqa: E402  (Yahoo indirici + bölünme çarpanı; DEĞİŞTİRİLMEZ)

tslog = logging.getLogger("col.tavan_serisi")
if not tslog.handlers:
    _ts_h = logging.StreamHandler(sys.stderr)
    _ts_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tavan: %(message)s", "%H:%M:%S"))
    tslog.addHandler(_ts_h)
    tslog.setLevel(logging.INFO)
    tslog.propagate = False

TS_ETIKET = "tavan_serisi_20261113"
TS_SURUM = "TAVAN_SERISI v1.0 (tavan_serisi_20261113): çökmüş BIST hissesinde art arda tavan; canlı tarama + geçmiş taban oranlar (ön kayıtlı)"

TS_YOL: Dict[str, str] = {
    "cikti": os.environ.get("TS_CIKTI", os.path.join(KOK_TS, "arastirma_cikti", "tavan_serisi")),
    "is": os.environ.get("TS_IS", "/tmp/tavan"),
    "yahoo": os.environ.get("TS_YAHOO_KLASOR", "/tmp/tavan/yahoo"),
    "yahoo_canli": os.environ.get("TS_YAHOO_CANLI", "/tmp/tavan/yahoo_canli"),
    "veri": os.environ.get("TS_VERI", "/tmp/veri"),
}
TS_DOSYA: Dict[str, str] = {"onkayit": "TAVAN_ON_KAYIT.md", "sonuc": "tavan_sonuc.json", "rapor": "TAVAN_RAPOR.md",
                            "canli_csv": "canli_cokmus.csv", "olay": "tavan_olaylar.csv.gz"}
_TS_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")

# BIST pay piyasası fiyat adımları (alt sınır TL, adım TL): tavan fiyatı = önceki kapanış x 1,10, adıma AŞAĞI yuvarlanır.
TS_ADIM: List[Tuple[float, float]] = [(0.0, 0.01), (20.0, 0.02), (50.0, 0.05), (100.0, 0.10), (250.0, 0.25), (500.0, 0.50),
                                      (1000.0, 1.00), (2500.0, 2.50)]

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256 mührü ön kayıtta; sonuç görüldükten sonra değişmez)
TS_ESIK: Dict[str, Any] = {
    "surum_etiket": TS_ETIKET,
    "veri": {"kaynak": "Yahoo chart API v8 günlük (K60_veri.k60v_fiyat_indir, değiştirilmeden; yalnız bas / bit bu iş için)",
             "bas": "2015-01-01", "bit": "2026-11-14", "evren": "V_BIST.pkl sembolleri ∪ dol.pkl kodları, Yahoo kodu SEMBOL.IS",
             "fiyat": "Yahoo quote OHLC (bölünme / bedelsiz düzeltmeli, temettüsüz); O/H/L tutarsızsa H = max(O,H,C), L = min(O,L,C)",
             "ekran": "ekran fiyatı = Yahoo fiyatı x tarihi o günden SONRA olan bölünme oranlarının çarpımı (K60_veri.k60v_bolunme_carpan)",
             "takvim": "hafta içi ve en az 10 hissenin işlem gördüğü günler; her hisse kendi barlarıyla (durdurma günleri atlanır)"},
    "tavan": {"rejim": [["2000-01-01", "2020-03-12", 0.20], ["2020-03-13", "2099-12-31", 0.10]], "esik_kat": 0.95, "ust_kat": 1.05,
              "rejim_kaynak": "BIST günlük fiyat marjı 12.03.2020'ye kadar ±%20, 13.03.2020'den ±%10 (veride: 2016-19 tavan kümesi +%19,5-20,5, "
                              "+%9,5-10,5 günü yılda ~200; 12.03.2020'de 134 gün <= -%19, 13.03.2020'den sonra yok; Mart 2020'den +%9,5-10,5 yılda 3.500+)",
              "tanim": "marj m (o günün rejimi); tavan günü <=> r = C_t / C_t-1 - 1 >= min(0,95 m ; adim_tavan - 1e-9) VE r <= 1,05 m; adim_tavan = "
                       "(ekran C_t-1 x (1 + m) BIST fiyat adımına aşağı yuvarlanmış) / ekran C_t-1 - 1. m = %10 için eşik iş tanımındaki +%9,5 aynen; "
                       "1-2 TL'de adım yuvarlaması gerçek tavanı %9,5'in altına indirdiği için (1,38 -> 1,51 = +%9,42) o günlerde gerçek tavan fiyatı "
                       "kullanılır; r > 1,05 m marjla olamaz -> tavan sayılmaz. 2016 - 12.03.2020 (±%20 rejimi) +%9,5 günü tavan DEĞİLDİR (eşik +%19)",
              "kirik": 0.25, "kirik_tanim": "|r| > 0,25 = VERİ KIRIĞI (düzeltilmemiş bedelsiz / bedelli, uzun durdurma sonrası baz fiyat, Yahoo hatası): "
                                            "tavan değildir, seriyi keser ve 250 gün tepesi kırıktan sonra yeniden başlar",
              "kilitli": "kilitli tavan günü = tavan VE O = H = C (göreli tolerans 1e-6); tam kilitli = ayrıca L = H",
              "tol": 1e-6},
    "canli": {"tepe": ["2026-06-01", "2026-08-31"], "dip_bas": "2026-09-01", "dusus": -0.80, "gun20": 20, "hacim_med": 20, "hacim5": 5,
              "fon": "kriz öncesi fon payı = bilinme tarihi <= 31.08.2026 olan son KAP fon raporu ayındaki pay (FON_IZI.fi_k25_pay_tablo); "
                     "ayrıca 2026 Oca-Ağu en yüksek pay",
              "gun_ici": "son bar bugünün tarihi ve saat < 15:10 UTC (18:10 TR) ise 'gün içi' yazılır; ardışık tavan hem 'dünkü kapanışla kesin' "
                         "hem 'bugün dahil (gün içi)' verilir"},
    "olay": {"donem": ["2016-01-01", "2026-08-31"], "kriz": "2026-08-31", "bilgi": ["2026-09-01", None],
             "k": [1, 2, 3, 4, 5, 6, 8, 10],
             "cokmus": {"esik": -0.80, "pencere": 250, "en_az": 250,
                        "tanim": "derinlik = seri ilk tavanından ÖNCEKİ günün kapanışı / (kendi son 250 barının en yüksek kapanışı) - 1; 250 bar kırıktan "
                                 "sonra dolmalı (yoksa tanımsız: ne ÇÖKMÜŞ ne ÇÖKMEMİŞ). ÇÖKMÜŞ <=> derinlik <= -0,80; ÇÖKMEMİŞ <=> > -0,80"},
             "seri": "ardışık tavan günleri (kendi barları) bir seri; k. tavan günü t = seri başı + k - 1; aynı serinin her k'sı ayrı satır; "
                     "seri uzunluğu L; ertesi gün tavan <=> L > k",
             "giris": "t'den sonraki ilk kendi barı e'nin açılışı O_e; e'de hacim 0 / O yok -> dışarıda (sayılır)",
             "dolum_belirsiz": "e günü tavan VE O_e = H_e = L_e (tam kilitli tavan; alıcı sırada kalır): işaretlenir; ana sonuç yine O_e'den, "
                               "'yalnız dolum belirsiz olmayanlar' ayrı satır",
             "ufuk": [5, 20, 60, 120],
             "getiri": "r_h = C(e + h - 1) / O_e - 1 (e = 1. gün; takvim satırı, durdurmada son kapanış ileri taşınır); h penceresi kriz kesiğini "
                       "(31.08.2026) aşan olay o ufukta ölçülmez",
             "dokunma": {"yukari": 1.0, "asagi": -0.5,
                         "tanim": "P(+%100, 60g) <=> max H[e..e+59] >= 2 O_e; P(-%50, 60g) <=> min L[e..e+59] <= 0,5 O_e; P(-%50, 120g) aynı 120 barda"},
             "ana_n": "ana tablo n'i = 60 gün penceresi kesik içinde tamamlanan olaylar"},
    "kontrol": {"kova": [-0.80, -0.85, -0.90],
                "kova_tanim": "derinlik kovası: (-0,85, -0,80], (-0,90, -0,85], <= -0,90 (sabit)",
                "tanim": "her ÇÖKMÜŞ olay için: aynı referans gününde (olay hissesinin seri öncesi günü) ÇÖKMÜŞ ve aynı derinlik kovasında olan, seri "
                         "başından k. tavan gününe kadar (dahil) hiç tavan yapmamış, giriş günü e'de işlem gören (O var, hacim > 0) bütün öteki hisseler; "
                         "girişleri aynı gün O_e; ölçüler aynı. Kontrol değeri = kontrol hisselerinin ortalaması (oran ölçülerde ortalama oran)",
                "fark": "olay başına fark = olay r60 - kontrol ortalama r60; kontrolü olmayan olay farkta dışarıda (sayılır)"},
    "bootstrap": {"B": 2000, "tohum": 20261113, "kume": "hisse (olayları hisseleriyle birlikte çekilir)", "guven": [2.5, 97.5],
                  "olcu": "medyan fark ve ortalama fark (60 gün)"},
    "donem": {"2016-19": ["2016-01-01", "2019-12-31"], "2020-22": ["2020-01-01", "2022-12-31"], "2023-26.08": ["2023-01-01", "2026-08-31"],
              "tanim": "dönem = k. tavan gününün tarihi"},
    "karar": {"n_min": 30, "p50_kat": 1.2, "donem_min": 2, "donem_n_min": 10,
              "metin": "her k için: 'k. tavandan sonra katılmak kontrolden iyi' <=> n >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt "
                       "uç > 0 VE P(-%50, 60g) <= 1,2 x kontrolün P(-%50, 60g) VE üç dönemin en az ikisinde dönem medyan farkı > 0 (n >= 10 olan "
                       "dönemler; n < 10 dönem 'yön yok' sayılır); değilse 'kumar: beklenen değer kontrolden iyi değil'. n < 30 -> 'örneklem "
                       "yetersiz'. 8 ayrı k sınanır: tek k'nın geçmesi çoklu deneme şansı olabilir, raporda yazılır.",
              "karsilastirma": "ÇÖKMEMİŞ hisselerde k. tavan: aynı ölçüler BİLGİ (kontrolsüz)"},
    "duyarlilik": {"esik": [-0.60, -0.70], "kova": "e, e + (-1 - e) / 3, e + 2 (-1 - e) / 3 (ana -0,80 için iş tanımındaki sabit kovalar)",
                   "not": "BİLGİ, karara girmez: ÇÖKMÜŞ eşiği gevşetilince aynı ölçüler (ana n küçükse yön bilgisi için)"},
    "yanlilik": "evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker); Yahoo BIST geçmişinde "
                "eksik bedelsiz düzeltmesi kırık kuralıyla ayıklanır; işlem maliyeti yok",
}


class TsHata(RuntimeError):
    """TAVAN_SERISI'ne özgü durdurucu hata (veri yok, ön kayıt yok / değişmiş / git'e işlenmemiş, mühür / kod sha256 tutmuyor)."""


# ---------------------------------------------------------------- 0) YARDIMCILAR
def _ts_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _ts_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or TS_YOL["cikti"], TS_DOSYA.get(ad, ad))


def _ts_yaz(yol: str, metin: str) -> str:
    if _TS_EPOSTA.search(metin):
        raise TsHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _ts_kayit(x: Any) -> Any:
    if isinstance(x, pd.DataFrame):
        return [_ts_kayit(r) for r in x.to_dict(orient="records")]
    if isinstance(x, dict):
        return {str(k): _ts_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_ts_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer, np.bool_)):
        x = x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    if isinstance(x, pd.Timestamp):
        return str(x.date())
    if isinstance(x, _dt.date):
        return str(x)
    return x


def _ts_json(yol: str, obj: Any) -> str:
    return _ts_yaz(yol, json.dumps(_ts_kayit(obj), ensure_ascii=False, indent=1, sort_keys=True, default=str))


def _ts_json_oku(yol: str) -> Any:
    try:
        with open(yol, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as ex:
        raise TsHata(f"{yol} okunamadı ({type(ex).__name__}: {ex})") from ex


def ts_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def ts_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: TS_ESIK + TS_ADIM (sıralı JSON)."""
    s = json.dumps({"TS": E or TS_ESIK, "ADIM": TS_ADIM}, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def ts_kod_sha(yol: Optional[str] = None) -> str:
    return ts_sha_dosya(yol or os.path.join(KOK_TS, "TAVAN_SERISI.py"))


def ts_git_durum(yol: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve çalışma kopyası HEAD ile aynı mı? Değilse TsHata. Döner son commit ve zamanı."""
    kl = os.path.dirname(os.path.abspath(yol)); ad = os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "ls-files", "--error-unmatch", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise TsHata(f"{ad} git'e işlenmemiş (ön kayıt önce commit edilmeli)")
        r = subprocess.run(["git", "-C", kl, "diff", "--quiet", "HEAD", "--", ad], capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            raise TsHata(f"{ad} işlenmiş sürümden farklı (commit sonrası değişmiş)")
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H|%cI", "--", ad], capture_output=True, text=True, timeout=30)
        h, z = (r.stdout.strip().split("|") + [""])[:2]
        if not h:
            raise TsHata(f"{ad}: git geçmişi yok")
        return {"commit": h, "commit_zamani": z}
    except (OSError, subprocess.SubprocessError) as ex:
        raise TsHata(f"git denetimi yapılamadı ({type(ex).__name__}: {ex})") from ex


# ---------------------------------------------------------------- 1) VERİ
def ts_evren(veri: Optional[str] = None) -> List[str]:
    """V_BIST.pkl sembolleri ∪ dol.pkl kodları (sıralı)."""
    veri = veri or TS_YOL["veri"]; s: set = set()
    for ad in ("V_BIST.pkl", "dol.pkl"):
        y = os.path.join(veri, ad)
        try:
            with open(y, "rb") as f:
                o = pickle.load(f)
        except (OSError, pickle.UnpicklingError, EOFError) as ex:
            tslog.warning("%s okunamadı (%s); evrene katılmadı", y, type(ex).__name__); continue
        s |= set(o.keys()) if isinstance(o, dict) else set(o["kod"].astype(str))
    if not s:
        raise TsHata(f"evren boş: {veri} içinde V_BIST.pkl / dol.pkl yok")
    return sorted(str(x).strip().upper() for x in s)


def ts_indir(semboller: Optional[List[str]] = None, klasor: Optional[str] = None, bit: Optional[str] = None,
             bas: Optional[str] = None) -> Dict[str, Any]:
    """K60_veri.k60v_fiyat_indir'i bu işin tarih aralığıyla çağırır (K60V_ESIK geçici olarak değişir, sonra eski hâline döner)."""
    semboller = semboller or ts_evren(); klasor = klasor or TS_YOL["yahoo"]
    Y = K60V.K60V_ESIK["yahoo"]; eski = {k: Y[k] for k in ("bas", "bit")}
    try:
        Y["bas"] = bas or TS_ESIK["veri"]["bas"]; Y["bit"] = bit or TS_ESIK["veri"]["bit"]
        return K60V.k60v_fiyat_indir(semboller=[s + ".IS" for s in semboller], klasor=klasor)
    finally:
        Y.update(eski)


def ts_adim(p: np.ndarray) -> np.ndarray:
    """Ekran fiyatı için BIST fiyat adımı."""
    p = np.asarray(p, float); out = np.full(p.shape, TS_ADIM[0][1])
    for alt, a in TS_ADIM:
        out = np.where(p >= alt, a, out)
    return out


def ts_yahoo_oku(yol: str) -> Tuple[Optional[pd.DataFrame], str]:
    """Önbellek JSON -> DataFrame(o, h, l, c, v, carpan) (günler İstanbul saatine göre, bölünme düzeltmeli) ya da (None, neden).
    Temizlik K60_veri.k60v_yahoo_oku ile aynı (OHLC dolu, C > 0); O/H/L tutarsızlığı onarılır (H = max, L = min)."""
    try:
        with open(yol, encoding="utf-8") as f:
            J = json.load(f)
    except (OSError, ValueError) as ex:
        return None, f"okunamadı ({type(ex).__name__})"
    if not isinstance(J, dict):
        return None, "okunamadı (biçim)"
    if "yok" in J:
        return None, "yok"
    res = ((J.get("chart") or {}).get("result") or [None])[0]
    if not res or not res.get("timestamp"):
        return None, "veri yok"
    tz = (res.get("meta") or {}).get("exchangeTimezoneName") or "Europe/Istanbul"
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    try:
        gun = pd.to_datetime(res["timestamp"], unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
        d = pd.DataFrame({"o": q.get("open"), "h": q.get("high"), "l": q.get("low"), "c": q.get("close"), "v": q.get("volume")},
                         index=gun, dtype=float)
    except (ValueError, TypeError):
        return None, "okunamadı (seri boyu)"
    d = d[~d.index.duplicated(keep="last")].dropna(subset=["o", "h", "l", "c"]).sort_index()
    d = d[(d.c > 0) & (d.o > 0) & (d.index.dayofweek < 5)]
    if not len(d):
        return None, "veri yok"
    d["h"] = d[["o", "h", "c"]].max(axis=1); d["l"] = d[["o", "l", "c"]].min(axis=1); d["v"] = d.v.fillna(0.0)
    bol = []
    for v in ((res.get("events") or {}).get("splits") or {}).values():
        try:
            pay, payda, t = float(v["numerator"]), float(v["denominator"]), int(v["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if pay > 0 and payda > 0 and pay != payda:
            g = pd.to_datetime([t], unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()[0]
            bol.append((g.to_datetime64().astype("datetime64[ns]"), pay / payda))
    bol.sort(key=lambda x: x[0])
    B = (np.array([x[0] for x in bol], "datetime64[ns]"), np.array([x[1] for x in bol], float)) if bol else None
    d["carpan"] = K60V.k60v_bolunme_carpan(B, d.index.to_numpy("datetime64[ns]"))
    return d, "fiyat"


def ts_fiyatlar(klasor: Optional[str] = None, semboller: Optional[List[str]] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """Önbellekteki bütün hisseler -> {sembol: DataFrame}; kapsam sayımı (inemeyen / veri yok)."""
    klasor = klasor or TS_YOL["yahoo"]
    if not os.path.isdir(klasor):
        raise TsHata(f"fiyat önbelleği yok: {klasor} (önce `python TAVAN_SERISI.py indir`)")
    semboller = semboller or ts_evren(); S: Dict[str, pd.DataFrame] = {}; eksik: Dict[str, str] = {}
    for s in semboller:
        y = os.path.join(klasor, K60V._k60v_fiyat_adi(s + ".IS"))
        if not os.path.exists(y):
            eksik[s] = "inmedi"; continue
        d, neden = ts_yahoo_oku(y)
        if d is None:
            eksik[s] = neden
        else:
            S[s] = d
    tslog.info("fiyat: %d hisse okundu, %d eksik (%s)", len(S), len(eksik), klasor)
    if not S:
        raise TsHata(f"{klasor}: okunabilen fiyat yok")
    man = os.path.join(klasor, K60V.K60V_DOSYA["manifest"])
    return S, {"okunan": len(S), "eksik": eksik, "manifest_sha256": ts_sha_dosya(man) if os.path.exists(man) else None,
               "son_tarih": str(max(d.index[-1] for d in S.values()).date())}


# ---------------------------------------------------------------- 2) TAVAN VE SERİ
def ts_marj(gun: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Her gün için BIST günlük fiyat marjı (TS_ESIK['tavan']['rejim']); rejim dışı gün NaN."""
    out = np.full(len(gun), np.nan)
    for a, b, m in (E or TS_ESIK)["tavan"]["rejim"]:
        out[(gun >= pd.Timestamp(a)) & (gun <= pd.Timestamp(b))] = float(m)
    return out


def ts_tavan(d: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her bar için r, eşik, tavan, kırık, kilitli, tam_kilitli, seri sayacı (o güne kadar ardışık tavan), derinlik (250 bar tepe, kırıktan sonra)."""
    E = E or TS_ESIK; T = E["tavan"]; C = E["olay"]["cokmus"]; tol = float(T["tol"])
    c = d.c.to_numpy(float); o = d.o.to_numpy(float); h = d.h.to_numpy(float); lo = d.l.to_numpy(float)
    car = d["carpan"].to_numpy(float) if "carpan" in d else np.ones(len(d))
    r = np.r_[np.nan, c[1:] / c[:-1] - 1.0]
    p0 = np.r_[np.nan, c[:-1] * car[:-1]]
    marj = ts_marj(d.index, E)
    with np.errstate(invalid="ignore", divide="ignore"):
        adim = ts_adim(np.nan_to_num(p0, nan=1.0))
        tf = np.floor(p0 * (1.0 + marj) / adim + 1e-9) * adim
        esik = np.minimum(T["esik_kat"] * marj, tf / p0 - 1.0 - 1e-9)
        tavan = (r >= esik - tol) & (r <= T["ust_kat"] * marj + tol)
        kirik = np.abs(r) > T["kirik"]
        es = lambda a, b: np.abs(a - b) <= tol * np.maximum(np.abs(b), 1e-12)  # noqa: E731
        kil = tavan & es(o, h) & es(c, h)
        tam = kil & es(lo, h)
    tavan = np.nan_to_num(tavan, nan=0).astype(bool); kirik = np.nan_to_num(kirik, nan=0).astype(bool)
    sayac = np.zeros(len(c), int)
    for i in range(len(c)):
        sayac[i] = (sayac[i - 1] + 1 if i else 1) if tavan[i] else 0
    seg = np.cumsum(kirik)
    tepe = pd.Series(c).groupby(seg).transform(lambda x: x.rolling(int(C["pencere"]), min_periods=int(C["en_az"])).max()).to_numpy(float)
    return pd.DataFrame({"r": r, "esik": esik, "tavan": tavan, "kirik": kirik, "kilitli": kil, "tam_kilitli": tam, "sayac": sayac,
                         "derinlik": c / tepe - 1.0}, index=d.index)


def ts_seriler(d: pd.DataFrame, X: pd.DataFrame) -> pd.DataFrame:
    """Ardışık tavan serileri: bas_i, son_i (kendi bar sırası), uzunluk, ref derinlik (seri öncesi gün)."""
    t = X.tavan.to_numpy(bool); sat = []
    i = 0; n = len(t)
    while i < n:
        if t[i]:
            j = i
            while j + 1 < n and t[j + 1]:
                j += 1
            sat.append({"bas_i": i, "son_i": j, "L": j - i + 1, "bas": d.index[i], "ref_derinlik": X.derinlik.iloc[i - 1] if i > 0 else np.nan,
                        "ref_tarih": d.index[i - 1] if i > 0 else pd.NaT})
            i = j + 1
        else:
            i += 1
    return pd.DataFrame(sat, columns=["bas_i", "son_i", "L", "bas", "ref_derinlik", "ref_tarih"])


# ---------------------------------------------------------------- 3) İŞ 1: CANLI TARAMA
def ts_fon_pay(veri: Optional[str] = None, kriz: str = "2026-08-31") -> pd.DataFrame:
    """Hisse başına kriz öncesi KAP raporlu fon payı (FON_IZI.fi_k25_pay_tablo ile aynı hesap). Veri yoksa boş tablo + uyarı."""
    veri = veri or TS_YOL["veri"]
    try:
        import FON_IZI as FI  # noqa: WPS433  (yalnız fi_k25_pay_tablo; DEĞİŞTİRİLMEZ)
        G = pd.read_pickle(os.path.join(veri, "G.pkl")); oran = pd.read_pickle(os.path.join(veri, "oran.pkl"))
        dol = pd.read_pickle(os.path.join(veri, "dol.pkl"))
        M = FI.fi_k25_pay_tablo(G, oran, dol)
    except (OSError, ImportError, KeyError, ValueError, pickle.UnpicklingError, EOFError) as ex:
        tslog.warning("fon payı tablosu kurulamadı (%s: %s); fon sütunları boş", type(ex).__name__, ex)
        return pd.DataFrame(columns=["sembol", "fon_pay_kriz_oncesi", "fon_pay_ay", "fon_sayisi", "fon_pay_max_2026"])
    k = pd.Timestamp(kriz); M = M[M.bil <= k + pd.Timedelta(hours=23, minutes=59)]
    son = M.sort_values(["kod", "ay", "bil"]).groupby("kod").tail(1)
    y26 = M[M.ay >= 2026 * 12].groupby("kod").pay.max().rename("fon_pay_max_2026")
    out = son[["kod", "pay", "ay", "fon"]].rename(columns={"kod": "sembol", "pay": "fon_pay_kriz_oncesi", "fon": "fon_sayisi"})
    out["fon_pay_ay"] = [f"{a // 12}-{a % 12 + 1:02d}" for a in out.ay]
    return out.drop(columns="ay").merge(y26, left_on="sembol", right_index=True, how="left")


def ts_gun_ici(son_tarih: pd.Timestamp, simdi: Optional[_dt.datetime] = None) -> bool:
    simdi = simdi or _dt.datetime.now(_dt.timezone.utc)
    return son_tarih.date() == simdi.date() and (simdi.hour, simdi.minute) < (15, 10)


def ts_canli_tablo(S: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None, fon: Optional[pd.DataFrame] = None,
                   simdi: Optional[_dt.datetime] = None) -> pd.DataFrame:
    """İŞ 1: her hisse için kriz düşüşü, dip, dipten kat, ardışık tavan (dünkü kapanışla kesin + bugün dahil), son 20 günde tavan, kilitli, hacim."""
    E = E or TS_ESIK; Cn = E["canli"]; t1, t2 = (pd.Timestamp(x) for x in Cn["tepe"]); db = pd.Timestamp(Cn["dip_bas"])
    sat = []
    for s, d in S.items():
        try:
            X = ts_tavan(d, E)
            a = d.loc[t1:t2]; b = d.loc[db:]
            if not len(a) or not len(b):
                sat.append({"sembol": s, "durum": "kriz dönemi verisi yok"}); continue
            tepe_t = a.c.idxmax(); dip_t = b.c.idxmin(); tepe = float(a.c.max()); dip = float(b.c.min())
            kirik_arada = bool(X.kirik.loc[tepe_t:].any())
            n = len(d); son = d.index[-1]; gi = ts_gun_ici(son, simdi)
            say_bugun = int(X.sayac.iloc[-1]); say_dun = int(X.sayac.iloc[-2]) if n > 1 else 0
            kesin = say_dun if gi else say_bugun
            v = d.v.to_numpy(float); vmed = float(np.median(v[max(0, n - 1 - Cn["hacim_med"]):n - 1])) if n > 1 else np.nan
            car = float(d["carpan"].iloc[-1])
            sat.append({"sembol": s, "durum": "tamam", "tepe": tepe * float(d["carpan"].loc[tepe_t]), "tepe_tarih": tepe_t.date(),
                        "dip": dip * float(d["carpan"].loc[dip_t]), "dip_tarih": dip_t.date(), "dusus": dip / tepe - 1.0,
                        "bugun": float(d.c.iloc[-1]) * car, "bugun_tarih": son.date(), "gun_ici": gi, "dipten_kat": float(d.c.iloc[-1]) / dip,
                        "ardisik_tavan_kesin": kesin, "bugun_tavan": bool(X.tavan.iloc[-1]), "ardisik_tavan_bugun_dahil": say_bugun,
                        "tavan_20g": int(X.tavan.iloc[-Cn["gun20"]:].sum()), "son_r": float(X.r.iloc[-1]),
                        "kilitli_son": bool(X.kilitli.iloc[-1]), "tam_kilitli_son": bool(X.tam_kilitli.iloc[-1]),
                        "kilitli_seri_gun": int(X.kilitli.iloc[n - say_bugun:].sum()) if say_bugun else 0,
                        "hacim_son": float(v[-1]), "hacim_oran_20med": float(v[-1] / vmed) if vmed and vmed > 0 else np.nan,
                        "hacim_5g_ort": float(np.mean(v[-Cn["hacim5"]:])), "hacim_5g_tl_ort": float(np.mean((d.c * d["carpan"] * d.v).iloc[-Cn["hacim5"]:])),
                        "kirik_tepe_sonrasi": kirik_arada, "carpan_son": car,
                        "kirik_tarih": X.index[X.kirik & (X.index >= tepe_t)][-1].date() if kirik_arada else None,
                        "kirik_r": float(X.r[X.kirik & (X.index >= tepe_t)].iloc[-1]) if kirik_arada else np.nan,
                        "cokmus": bool(dip / tepe - 1.0 <= Cn["dusus"]) and not kirik_arada})
        except (ValueError, KeyError, IndexError, TypeError, ZeroDivisionError) as ex:
            tslog.warning("%s canlı ölçülemedi (%s: %s)", s, type(ex).__name__, ex)
            sat.append({"sembol": s, "durum": f"hata: {type(ex).__name__}"})
    T = pd.DataFrame(sat)
    for c in ("ardisik_tavan_kesin", "ardisik_tavan_bugun_dahil", "tavan_20g", "kilitli_seri_gun"):
        if c in T:
            T[c] = T[c].astype("Int64")
    if fon is not None and len(fon):
        T = T.merge(fon, on="sembol", how="left")
    return T


def ts_vbist_denetim(S: Dict[str, pd.DataFrame], veri: Optional[str] = None) -> Dict[str, Any]:
    """V_BIST.pkl ile Yahoo kapanışlarının ortak günlerdeki uyumu (son 60 ortak gün; ölçek farkı oran medyanıyla giderilir)."""
    try:
        V = pd.read_pickle(os.path.join(veri or TS_YOL["veri"], "V_BIST.pkl"))
    except (OSError, pickle.UnpicklingError, EOFError) as ex:
        return {"durum": f"V_BIST okunamadı ({type(ex).__name__})"}
    fark, n, son = [], 0, None
    for s, d in S.items():
        v = V.get(s)
        if v is None or "Close" not in v:
            continue
        son = max(son, v.index.max()) if son is not None else v.index.max()
        j = d.c.to_frame().join(v.Close.rename("vb"), how="inner").dropna().iloc[-60:]
        if len(j) < 10:
            continue
        q = j.vb / j.c; n += 1
        fark.append(float(((q / q.median() - 1).abs() > 0.02).mean()))
    return {"hisse": n, "v_bist_son": str(son.date()) if son is not None else None,
            "uyumsuz_gun_pay_medyan": float(np.median(fark)) if fark else None,
            "uyumsuz_hisse_%5_ustu": int(sum(f > 0.05 for f in fark))}


def _f(x: Any, n: int = 2) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else f"{x:,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _y(x: Any, n: int = 0) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if not np.isfinite(x) else f"%{_f(100 * x, n)}"


def ts_canli_md(T: pd.DataFrame, K: Dict[str, Any], D: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or TS_ESIK; ev = T[T.get("cokmus", False) == True].copy()  # noqa: E712
    son = K["son_tarih"]; gi = bool(ev.gun_ici.any()) if len(ev) else False
    sr = ev[ev.ardisik_tavan_bugun_dahil > 0].sort_values(["ardisik_tavan_bugun_dahil", "dipten_kat"], ascending=False)
    L = [f"# Çökmüş BIST hisseleri: tavan serisi taraması ({son})", "",
         f"{TS_SURUM}. Üretim {_ts_simdi()}. Veri: Yahoo günlük ({K['okunan']} hisse okundu, {len(K['eksik'])} eksik); son bar {son}"
         + (" **GÜN İÇİ** (BIST kapanmadan alındı; bugünün tavanı kesin değil)" if gi else "") + ".",
         "",
         f"Evren ÇÖKMÜŞ: 1 Haz - 31 Ağu 2026 en yüksek kapanıştan 1 Eyl 2026 sonrası en düşük kapanışa düşüş <= %-80 ve arada veri kırığı (|günlük| > %25) "
         f"yok. **{len(ev)} hisse** ÇÖKMÜŞ; bunlardan **{len(sr)} hisse** bugün tavan serisinde, {int((ev.tavan_20g > 0).sum())} hisse son 20 günde en az bir "
         "tavan yaptı. "
         "Tavan günü: kapanış / önceki kapanış - 1 >= %9,5 (1-2 TL'de fiyat adımı yuvarlaması gerçek tavanı %9,5'in altına indirdiğinde gerçek tavan "
         "fiyatı) ve <= %10,5 (BIST ±%10 marjı). Fiyatlar ekran fiyatı (bedelsiz düzeltmesi geri alınmış).", "",
         "## 1. Bugün tavan serisinde olanlar (seri uzunluğuna göre)", "",
         "| sembol | kriz öncesi tepe (tarih) | dip (tarih) | düşüş | bugün | dipten kat | ardışık tavan (dünkü kapanışla kesin) | bugün dahil"
         + (" (gün içi)" if gi else "") + " | 20 günde tavan | bugün kilitli mi | hacim / 20g medyan | 5g ort. hacim (TL) | fon payı (kriz öncesi) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sr.itertuples():
        kil = "TAM KİLİTLİ" if r.tam_kilitli_son else ("kilitli (O=H=C)" if r.kilitli_son else ("tavan, kilitsiz" if r.bugun_tavan else "—"))
        L.append(f"| {r.sembol} | {_f(r.tepe)} ({r.tepe_tarih}) | {_f(r.dip)} ({r.dip_tarih}) | {_y(r.dusus)} | {_f(r.bugun)} | {_f(r.dipten_kat)} | "
                 f"{r.ardisik_tavan_kesin} | {r.ardisik_tavan_bugun_dahil} | {r.tavan_20g} | {kil} | {_f(r.hacim_oran_20med)} | "
                 f"{_f(r.hacim_5g_tl_ort / 1e6, 1)} mn | {_y(getattr(r, 'fon_pay_kriz_oncesi', np.nan), 1)} |")
    if not len(sr):
        L.append("| (yok) |  |  |  |  |  |  |  |  |  |  |  |  |")
    L += ["", "Kilitli: açılış = en yüksek = kapanış (alıcı sırada; satıcı yok). Tam kilitli: gün boyu tek fiyat (en düşük = en yüksek). Hacim oranı "
          "düşükse tahta sığ; yüksekse el değiştirme var.", "",
          "## 2. TEHOL ve PEKER", ""]
    for s, ad in (("TEHOL", "TEHOL"), ("PEKGY", "PEKER (borsa kodu PEKGY, Peker GYO; PEKER.IS Yahoo'da yok)")):
        r = T[T.sembol == s]
        if not len(r):
            L.append(f"- {ad}: fiyat verisi yok."); continue
        r = r.iloc[0]
        if r.get("durum") != "tamam":
            L.append(f"- {ad}: {r.get('durum')}"); continue
        neden = "ÇÖKMÜŞ evreninde" if r.cokmus else ("evrende değil: veri kırığı" if r.kirik_tepe_sonrasi else f"evrende değil: düşüş {_y(r.dusus)} (> %-80)")
        L.append(f"- {ad}: {neden}. Tepe {_f(r.tepe)} ({r.tepe_tarih}) -> dip {_f(r.dip)} ({r.dip_tarih}) = {_y(r.dusus)}; bugün {_f(r.bugun)} "
                 f"(dipten {_f(r.dipten_kat)} kat); ardışık tavan {r.ardisik_tavan_kesin} (kesin) / {r.ardisik_tavan_bugun_dahil} (bugün dahil); "
                 f"son 20 günde {r.tavan_20g} tavan; seri içinde kilitli gün {r.kilitli_seri_gun}; bugün hacim / 20g medyan {_f(r.hacim_oran_20med)}; "
                 f"kriz öncesi fon payı {_y(r.get('fon_pay_kriz_oncesi', np.nan), 1)} ({r.get('fon_pay_ay', '—')}), 2026 en yüksek "
                 f"{_y(r.get('fon_pay_max_2026', np.nan), 1)}.")
    nt = ev[ev.ardisik_tavan_bugun_dahil == 0].sort_values("dusus")
    L += ["", f"## 3. Çökmüş ama bugün tavan serisinde olmayanlar ({len(nt)} hisse)", "",
          f"Düşüş medyanı {_y(nt.dusus.median())}; dipten kat medyanı {_f(nt.dipten_kat.median())}; son 20 günde en az bir tavan yapan "
          f"{int((nt.tavan_20g > 0).sum())}; bugün dipte (dipten kat < 1,05) {int((nt.dipten_kat < 1.05).sum())}.", "",
          "| sembol | düşüş | bugün | dipten kat | 20 günde tavan | fon payı (kriz öncesi) |", "|---|---|---|---|---|---|"]
    for r in nt.itertuples():
        L.append(f"| {r.sembol} | {_y(r.dusus)} | {_f(r.bugun)} | {_f(r.dipten_kat)} | {r.tavan_20g} | {_y(getattr(r, 'fon_pay_kriz_oncesi', np.nan), 1)} |")
    kir = T[(T.get("kirik_tepe_sonrasi", False) == True) & (T.dusus <= E["canli"]["dusus"])]  # noqa: E712
    L += ["", "## 4. Notlar", "",
          "- Veri kırığı nedeniyle evrene alınmayan (düşüş <= %-80 görünüyor ama tepeden sonra |günlük| > %25 olan gün var: düzeltilmemiş bedelsiz ya "
          "da işlem durdurma sonrası baz fiyatla açılış; elle bakılmalı): "
          + ("; ".join(f"{r.sembol} ({r.kirik_tarih}: {_y(r.kirik_r)}; düşüş {_y(r.dusus)}, bugün {_f(r.bugun)})" for r in kir.itertuples())
             if len(kir) else "yok") + ".",
          f"- İnemeyen / verisi olmayan sembol: {len(K['eksik'])} ({', '.join(sorted(K['eksik'])[:40])}{' ...' if len(K['eksik']) > 40 else ''}).",
          f"- V_BIST.pkl çapraz denetimi (son 60 ortak gün): {D}.",
          "- Bu tablo tarama, öneri değildir; geçmişte bu durumun ne getirdiği TAVAN_RAPOR.md'de (ön kayıtlı ölçüm). Fon krizi sonrası olaylar testlere girmez.",
          "- Ham tablo: /tmp/tavan/canli_cokmus.csv (repoda değil)."]
    return "\n".join(L) + "\n"


def ts_canli(yenile: bool = False, E: Optional[Dict[str, Any]] = None, kl: Optional[str] = None) -> Dict[str, Any]:
    """İŞ 1 uçtan uca: (isteğe bağlı yeniden indirme) -> tablo -> csv + md."""
    E = E or TS_ESIK; klasor = TS_YOL["yahoo"]
    if yenile:
        klasor = TS_YOL["yahoo_canli"] + "_" + _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d_%H%M")
        tslog.info("canlı yenileme -> %s", klasor)
        ts_indir(klasor=klasor, bas="2026-01-01", bit=(pd.Timestamp.utcnow().normalize() + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
    S, K = ts_fiyatlar(klasor)
    T = ts_canli_tablo(S, E, ts_fon_pay())
    D = ts_vbist_denetim(S)
    os.makedirs(TS_YOL["is"], exist_ok=True)
    yc = os.path.join(TS_YOL["is"], TS_DOSYA["canli_csv"]); T.to_csv(yc, index=False)
    ym = _ts_yaz(os.path.join(kl or TS_YOL["cikti"], f"CANLI_{K['son_tarih']}.md"), ts_canli_md(T, K, D, E))
    ev = T[T.get("cokmus", False) == True]  # noqa: E712
    tslog.info("canlı: %d çökmüş, %d tavan serisinde -> %s", len(ev), int((ev.ardisik_tavan_bugun_dahil > 0).sum()), ym)
    return {"csv": yc, "md": ym, "T": T, "kapsam": K, "denetim": D}


# ---------------------------------------------------------------- 4) İŞ 2: PANEL VE OLAYLAR
def ts_panel(S: Dict[str, pd.DataFrame], kes: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Takvim x hisse panelleri (O, H, L, C ileri taşınmış, V, tavan, derinlik) + hisse başına tavan tablosu ve seriler. kes sonrası atılır."""
    E = E or TS_ESIK; Sx: Dict[str, pd.DataFrame] = {}; Xs: Dict[str, pd.DataFrame] = {}; Rs: Dict[str, pd.DataFrame] = {}
    for s, d in S.items():
        if kes is not None:
            d = d[d.index <= pd.Timestamp(kes)]
        if len(d) < 2:
            continue
        X = ts_tavan(d, E); Sx[s] = d; Xs[s] = X; Rs[s] = ts_seriler(d, X)
    if not Sx:
        raise TsHata("panel boş")
    say = pd.Series(np.concatenate([d.index.to_numpy() for d in Sx.values()])).value_counts()
    takvim = pd.DatetimeIndex(sorted(say[say >= 10].index))
    sym = sorted(Sx)

    def pan(f) -> pd.DataFrame:
        return pd.DataFrame({s: f(s) for s in sym}).reindex(takvim)
    P = {"takvim": takvim, "sym": sym, "O": pan(lambda s: Sx[s].o), "H": pan(lambda s: Sx[s].h), "L": pan(lambda s: Sx[s].l),
         "C": pan(lambda s: Sx[s].c), "V": pan(lambda s: Sx[s].v), "T": pan(lambda s: Xs[s].tavan.astype(float)).fillna(0.0) > 0,
         "D": pan(lambda s: Xs[s].derinlik), "S": Sx, "X": Xs, "R": Rs}
    P["Cf"] = P["C"].ffill()
    return P


def ts_ufuk_panelleri(P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Her (giriş satırı, hisse) için r_h, P(+%100 60g), P(-%50 60g), P(-%50 120g); pencere takvim sonunu aşarsa NaN."""
    E = E or TS_ESIK; O = P["O"].to_numpy(float); Cf = P["Cf"].to_numpy(float); n = O.shape[0]; out: Dict[str, np.ndarray] = {}
    for h in E["olay"]["ufuk"]:
        R = np.full(O.shape, np.nan)
        if h - 1 < n:
            R[: n - h + 1] = Cf[h - 1:] / O[: n - h + 1] - 1.0
        out[f"r{h}"] = R
    up, dn = E["olay"]["dokunma"]["yukari"], E["olay"]["dokunma"]["asagi"]
    for ad, pan, h, f in (("up100_60", "H", 60, "max"), ("dn50_60", "L", 60, "min"), ("dn50_120", "L", 120, "min")):
        A = P[pan].iloc[::-1].rolling(h, min_periods=1)
        A = (A.max() if f == "max" else A.min()).iloc[::-1].to_numpy(float)
        with np.errstate(invalid="ignore"):
            Z = (A >= O * (1 + up)) if f == "max" else (A <= O * (1 + dn))
        Z = Z.astype(float); Z[np.isnan(O) | np.isnan(A)] = np.nan
        if h - 1 < n:
            Z[n - h + 1:] = np.nan
        else:
            Z[:] = np.nan
        out[ad] = Z
    return out


def ts_kova(dr: float, E: Optional[Dict[str, Any]] = None) -> int:
    """Derinlik kovası: 0 = (-0,85, -0,80], 1 = (-0,90, -0,85], 2 = <= -0,90; ÇÖKMÜŞ değilse -1."""
    k = (E or TS_ESIK)["kontrol"]["kova"]
    if not np.isfinite(dr) or dr > k[0]:
        return -1
    return 0 if dr > k[1] else (1 if dr > k[2] else 2)


def ts_olaylar(P: Dict[str, Any], U: Dict[str, np.ndarray], bas: str, bit: Optional[str], kontrol: bool = True,
               E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Olay satırları (seri x k): k. tavan günü t bas..bit arasında; giriş, dolum, ufuk ölçüleri, kontrol ortalamaları."""
    E = E or TS_ESIK; tak = P["takvim"]; ix = {t: i for i, t in enumerate(tak)}; sym = P["sym"]; sj = {s: j for j, s in enumerate(sym)}
    b0 = pd.Timestamp(bas); b1 = pd.Timestamp(bit) if bit else tak[-1]
    O = P["O"].to_numpy(float); V = P["V"].to_numpy(float); D = P["D"].to_numpy(float)
    Tc = np.vstack([np.zeros((1, len(sym))), np.cumsum(P["T"].to_numpy(float), axis=0)])   # Tc[i] = satır < i tavan sayısı
    kovaP = np.full(D.shape, -1, np.int8)
    kk = E["kontrol"]["kova"]
    with np.errstate(invalid="ignore"):
        kovaP[D <= kk[0]] = 0; kovaP[D <= kk[1]] = 1; kovaP[D <= kk[2]] = 2
    ks = E["olay"]["k"]; olcu = [f"r{h}" for h in E["olay"]["ufuk"]] + ["up100_60", "dn50_60", "dn50_120"]; sat = []
    for s in sym:
        d = P["S"][s]; X = P["X"][s]; R = P["R"][s]; j = sj[s]; di = d.index
        for sr in R.itertuples():
            for k in ks:
                if sr.L < k:
                    break
                ti = sr.bas_i + k - 1; t = di[ti]
                if t < b0 or t > b1:
                    continue
                ei = ti + 1
                rec = {"sembol": s, "seri_bas": sr.bas, "k": k, "t": t, "L": int(sr.L), "ref_tarih": sr.ref_tarih,
                       "ref_derinlik": float(sr.ref_derinlik) if np.isfinite(sr.ref_derinlik) else np.nan}
                rec["sinif"] = ("tanimsiz" if not np.isfinite(rec["ref_derinlik"]) else
                                ("COKMUS" if rec["ref_derinlik"] <= E["olay"]["cokmus"]["esik"] else "COKMEMIS"))
                rec["kova"] = ts_kova(rec["ref_derinlik"], E)
                rec["seri_acik"] = bool(sr.son_i == len(di) - 1)
                rec["ertesi_tavan"] = (bool(sr.L > k) if ei < len(di) else np.nan)
                if ei >= len(di):
                    rec["durum"] = "giris yok (veri sonu)"; sat.append(rec); continue
                e = di[ei]; r = ix.get(e)
                rec["e"] = e
                if r is None or not np.isfinite(O[r, j]) or not V[r, j] > 0:
                    rec["durum"] = "giris yok (islem yok)"; sat.append(rec); continue
                rec["durum"] = "tamam"; rec["giris"] = float(O[r, j])
                rec["dolum_belirsiz"] = bool(X.tam_kilitli.iloc[ei])
                rec["kilitli_t"] = bool(X.kilitli.iloc[ti])
                for m in olcu:
                    rec[m] = float(U[m][r, j])
                if kontrol and rec["sinif"] == "COKMUS" and pd.notna(sr.ref_tarih) and sr.ref_tarih in ix and t in ix:
                    rr = ix[sr.ref_tarih]; r0 = ix[sr.bas]; rt = ix[t]
                    m = (kovaP[rr] == rec["kova"]) & ((Tc[rt + 1] - Tc[r0]) == 0) & np.isfinite(O[r]) & (V[r] > 0)
                    m[j] = False
                    rec["n_kontrol"] = int(m.sum())
                    for mm in olcu:
                        v = U[mm][r, m]; v = v[np.isfinite(v)]
                        rec[f"k_{mm}"] = float(v.mean()) if len(v) else np.nan
                elif kontrol:
                    rec["n_kontrol"] = 0
                sat.append(rec)
    Ev = pd.DataFrame(sat)
    if len(Ev):
        Ev["donem"] = [ts_donem(t, E) for t in Ev.t]
    return Ev


def ts_donem(t: pd.Timestamp, E: Optional[Dict[str, Any]] = None) -> str:
    for ad, ab in (E or TS_ESIK)["donem"].items():
        if ad == "tanim":
            continue
        a, b = ab
        if pd.Timestamp(a) <= t <= pd.Timestamp(b):
            return ad
    return "dışı"


# ---------------------------------------------------------------- 5) İSTATİSTİK VE KARAR
def ts_boot(x: np.ndarray, g: np.ndarray, f, E: Optional[Dict[str, Any]] = None) -> List[float]:
    """Hisse kümeli bootstrap %95 aralığı (f = np.median / np.mean)."""
    E = E or TS_ESIK; Bt = E["bootstrap"]; ok = np.isfinite(x); x = x[ok]; g = g[ok]
    if len(x) < 2:
        return [np.nan, np.nan]
    u, inv = np.unique(g, return_inverse=True); idx = [np.flatnonzero(inv == i) for i in range(len(u))]
    rng = np.random.default_rng(int(Bt["tohum"])); st = np.empty(int(Bt["B"]))
    for b in range(len(st)):
        sec = rng.integers(0, len(u), len(u))
        st[b] = f(x[np.concatenate([idx[i] for i in sec])])
    return [float(np.percentile(st, Bt["guven"][0])), float(np.percentile(st, Bt["guven"][1]))]


def _q(x: pd.Series) -> Dict[str, Any]:
    x = pd.to_numeric(x, errors="coerce").dropna()
    if not len(x):
        return {"n": 0, "med": np.nan, "ort": np.nan, "q25": np.nan, "q75": np.nan}
    return {"n": int(len(x)), "med": float(x.median()), "ort": float(x.mean()), "q25": float(x.quantile(0.25)), "q75": float(x.quantile(0.75))}


def ts_ozet_k(Ek: pd.DataFrame, kontrol: bool = True, E: Optional[Dict[str, Any]] = None, boot: bool = True) -> Dict[str, Any]:
    """Bir k'nın olay kümesi (giriş 'tamam') için bütün ölçüler."""
    E = E or TS_ESIK; A = Ek[Ek.durum == "tamam"]; W = A[A.r60.notna()]
    o: Dict[str, Any] = {"n_olay": int(len(Ek)), "n_giris": int(len(A)), "n": int(len(W)), "n_hisse": int(W.sembol.nunique()),
                         "dolum_belirsiz_pay": float(W.dolum_belirsiz.mean()) if len(W) else np.nan}
    et = pd.to_numeric(Ek.ertesi_tavan, errors="coerce").dropna()
    o["p_ertesi_tavan"] = float(et.mean()) if len(et) else np.nan; o["n_ertesi"] = int(len(et))
    Lk = Ek.L.to_numpy(float); kk = int(Ek.k.iloc[0]) if len(Ek) else 0
    o["seri"] = {"medyan_L": float(np.median(Lk)) if len(Lk) else np.nan,
                 **{f"P(L>={kk + a})": float((Lk >= kk + a).mean()) if len(Lk) else np.nan for a in (1, 2, 3, 5)},
                 "acik_seri": int(Ek.seri_acik.sum())}
    for h in E["olay"]["ufuk"]:
        o[f"r{h}"] = _q(A[f"r{h}"])
    for m in ("up100_60", "dn50_60", "dn50_120"):
        x = pd.to_numeric(A[m], errors="coerce").dropna(); o[m] = float(x.mean()) if len(x) else np.nan; o[f"n_{m}"] = int(len(x))
    if kontrol and "k_r60" in W:
        F = W[W.k_r60.notna()]
        fark = (F.r60 - F.k_r60).to_numpy(float); g = F.sembol.to_numpy()
        o["n_fark"] = int(len(F)); o["kontrolsuz"] = int(len(W) - len(F)); o["n_kontrol_medyan"] = float(F.n_kontrol.median()) if len(F) else np.nan
        o["fark_med"] = float(np.median(fark)) if len(fark) else np.nan; o["fark_ort"] = float(np.mean(fark)) if len(fark) else np.nan
        o["fark_med_ci"] = ts_boot(fark, g, np.median, E) if boot else [np.nan, np.nan]
        o["fark_ort_ci"] = ts_boot(fark, g, np.mean, E) if boot else [np.nan, np.nan]
        o["k_r60_med_ort"] = float(F.k_r60.median()) if len(F) else np.nan
        for m in ("up100_60", "dn50_60", "dn50_120"):
            Fm = A[A[f"k_{m}"].notna() & A[m].notna()]
            o[f"k_{m}"] = float(Fm[f"k_{m}"].mean()) if len(Fm) else np.nan
            o[f"o_{m}_eslesik"] = float(Fm[m].mean()) if len(Fm) else np.nan
        o["p50_kat"] = (o["o_dn50_60_eslesik"] / o["k_dn50_60"]) if o.get("k_dn50_60") and o["k_dn50_60"] > 0 else np.nan
        o["p100_kat"] = (o["o_up100_60_eslesik"] / o["k_up100_60"]) if o.get("k_up100_60") and o["k_up100_60"] > 0 else np.nan
        o["donem"] = {}
        for dn in [x for x in E["donem"] if x != "tanim"]:
            Fd = F[F.donem == dn]; fd = (Fd.r60 - Fd.k_r60).to_numpy(float)
            Ad = A[(A.donem == dn) & A.dn50_60.notna()]
            o["donem"][dn] = {"n": int(len(Fd)), "fark_med": float(np.median(fd)) if len(fd) else np.nan,
                              "r60_med": float(Fd.r60.median()) if len(Fd) else np.nan,
                              "up100_60": float(Ad.up100_60.mean()) if len(Ad) else np.nan, "dn50_60": float(Ad.dn50_60.mean()) if len(Ad) else np.nan,
                              "k_dn50_60": float(Ad.k_dn50_60.mean()) if len(Ad) and "k_dn50_60" in Ad else np.nan}
    return o


def ts_karar(o: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Önceden yazılı karar cümlesi (TS_ESIK['karar'])."""
    Kr = (E or TS_ESIK)["karar"]; n = o.get("n_fark", 0)
    if n < Kr["n_min"]:
        return {"karar": "örneklem yetersiz", "sartlar": {"n": n}}
    yon = [d["fark_med"] > 0 for d in o["donem"].values() if d["n"] >= Kr["donem_n_min"] and np.isfinite(d["fark_med"])]
    s = {"medyan_fark>0": bool(o["fark_med"] > 0), "alt_uc>0": bool(np.isfinite(o["fark_med_ci"][0]) and o["fark_med_ci"][0] > 0),
         "P50<=1,2xkontrol": bool(np.isfinite(o["p50_kat"]) and o["p50_kat"] <= Kr["p50_kat"]) if np.isfinite(o.get("k_dn50_60", np.nan)) else False,
         "donem>=2": bool(sum(yon) >= Kr["donem_min"])}
    return {"karar": "KONTROLDEN İYİ" if all(s.values()) else "KUMAR: beklenen değer kontrolden iyi değil", "sartlar": s,
            "donem_pozitif": int(sum(yon)), "donem_olculen": len(yon)}


def ts_esik_gevsek(e: float, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Duyarlılık için ÇÖKMÜŞ eşiği e olan TS_ESIK kopyası (kovalar e'den -1'e üç eşit dilim)."""
    import copy
    E2 = copy.deepcopy(E or TS_ESIK); a = (-1.0 - e) / 3.0
    E2["olay"]["cokmus"]["esik"] = float(e); E2["kontrol"]["kova"] = [float(e), float(e + a), float(e + 2 * a)]
    return E2


# ---------------------------------------------------------------- 6) ÖN KAYIT VE KAPI
def ts_sayim(P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt için yalnız tanım sayımı (sonuç yok): hisse, takvim, ÇÖKMÜŞ seri sayısı (k = 1), sınıf dağılımı."""
    E = E or TS_ESIK; b0 = pd.Timestamp(E["olay"]["donem"][0]); b1 = pd.Timestamp(E["olay"]["donem"][1]); c = E["olay"]["cokmus"]["esik"]
    n_c = n_n = n_t = 0; hs = set()
    for s, R in P["R"].items():
        R = R[(R.bas >= b0) & (R.bas <= b1)]
        n_c += int((R.ref_derinlik <= c).sum()); n_n += int((R.ref_derinlik > c).sum()); n_t += int(R.ref_derinlik.isna().sum())
        hs |= {s} if (R.ref_derinlik <= c).any() else set()
    return {"hisse": len(P["sym"]), "takvim_bas": str(P["takvim"][0].date()), "takvim_son": str(P["takvim"][-1].date()),
            "seri_cokmus": n_c, "seri_cokmemis": n_n, "seri_tanimsiz": n_t, "cokmus_seri_hisse": len(hs)}


def ts_onkayit_metin(zaman: str, sayim: Dict[str, Any], K: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or TS_ESIK
    return "\n".join([
        "# TAVAN SERİSİ ÖN KAYDI (ölçümden önce)", "",
        f"{TS_SURUM}. Yazılma {zaman}. Bu dosya git'e işlenmeden `python TAVAN_SERISI.py kos` çalışmaz (mühür kapısı).", "",
        "## Soru", "",
        "Çökmüş (seri öncesi kapanış 250 günlük en yüksekten >= %80 aşağıda) BIST hissesinde art arda tavan serisinin k. gününden sonra katılmak "
        "(ertesi gün açılış) ne getirmiş, ne kaybettirmiş; aynı gün aynı derinlikte çökmüş ama tavan yapmayan hisselerden iyi mi?", "",
        "## Tanımlar ve eşikler (TS_ESIK, değişmez)", "",
        "```json", json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
        "Fiyat adımları (TS_ADIM): " + json.dumps(TS_ADIM), "",
        "## Karar cümlesi (önceden yazılı)", "", E["karar"]["metin"], "",
        "Ölçülecekler (k = 1, 2, 3, 4, 5, 6, 8, 10): P(ertesi gün de tavan); seri uzunluğu dağılımı (k'ya koşullu); getiri 5 / 20 / 60 / 120 gün (medyan, "
        "ortalama, %25 / %75); P(60 günde +%100'e dokunma), P(60 günde -%50'ye dokunma), P(120 günde -%50); kontrole göre fark ve hisse kümeli "
        "bootstrap %95 aralık; dönem kırılımı 2016-19 / 2020-22 / 2023-26.08; 'yalnız dolum belirsiz olmayanlar' ayrı satır; ÇÖKMEMİŞ hisselerde "
        "k. tavan (BİLGİ); Eylül - Kasım 2026 olayları ayrı BİLGİ tablosu (karara girmez).", "",
        "## Veri ve tanım sayımı (sonuç içermez)", "",
        f"- Fiyat: {K['okunan']} hisse okundu, {len(K['eksik'])} eksik ({', '.join(sorted(K['eksik']))}); son tarih {K['son_tarih']}; "
        f"manifest sha256 {K['manifest_sha256']}.",
        f"- Test paneli (kesik {E['olay']['kriz']}): {json.dumps(sayim, ensure_ascii=False)}", "",
        "## Ön kayıttan önce görülenler (sonuç değil)", "",
        "- Günlük getiri dağılımı yıllara göre (BIST fiyat marjı rejimini bulmak için: 12.03.2020'ye kadar ±%20). Bu yüzden 2016 - 12.03.2020 tavan eşiği "
        "+%19 (iş tanımındaki +%9,5 o dönemde tavan değildir).",
        "- Tanım denetimi için k'ya göre ÇÖKMÜŞ olay sayıları (k = 1: 134, 2: 47, 3: 19, 4: 7, 5: 6, 6: 4, 8: 2, 10: 1; 40 hisse). n küçük: k >= 3 büyük "
        "olasılıkla 'örneklem yetersiz' çıkar. Bu yüzden ÇÖKMÜŞ eşiği -%60 / -%70 duyarlılığı BİLGİ olarak eklendi (karar ana tanımda kalır). "
        "Getiri, dokunma oranı, kontrol farkı görülmedi.",
        "- Canlı tarama (İŞ 1) bugünkü durumu gösterir, getiri içermez.", "",
        "## Bilinen yanlılıklar", "", E["yanlilik"], "",
        f"ESIK_SHA256: {ts_esik_sha(E)}",
        f"KOD_SHA256: {ts_kod_sha()}",
        f"VERI_MANIFEST_SHA256: {K['manifest_sha256']}", ""])


def ts_onkayit(kl: Optional[str] = None) -> str:
    y = _ts_yol("onkayit", kl)
    if os.path.exists(y):
        raise TsHata(f"ön kayıt zaten var, üzerine yazılmaz: {y}")
    S, K = ts_fiyatlar()
    P = ts_panel(S, kes=TS_ESIK["olay"]["kriz"])
    return _ts_yaz(y, ts_onkayit_metin(_ts_simdi(), ts_sayim(P), K))


def ts_onkayit_oku(yol: str) -> Dict[str, str]:
    try:
        with open(yol, encoding="utf-8") as f:
            t = f.read()
    except OSError as ex:
        raise TsHata(f"ön kayıt okunamadı: {ex}") from ex
    out = {}
    for k in ("ESIK_SHA256", "KOD_SHA256", "VERI_MANIFEST_SHA256"):
        m = re.search(rf"^{k}: ([0-9a-f]{{64}}|None)$", t, re.M)
        if not m:
            raise TsHata(f"ön kayıtta {k} yok")
        out[k] = m.group(1)
    return out


def ts_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
            manifest: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt mühür kapısı: ön kayıt var + git'e işlenmiş ve değişmemiş + ESIK sha tutar + veri manifesti tutar + KOD sha tutar (ya da sapma)."""
    E = E or TS_ESIK; y = _ts_yol("onkayit", kl)
    if not os.path.exists(y):
        raise TsHata("ön kayıt yok: önce `python TAVAN_SERISI.py onkayit` ve commit")
    O = ts_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        out["onkayit_git"] = ts_git_durum(y)
    if O["ESIK_SHA256"] != ts_esik_sha(E):
        raise TsHata("eşik mührü tutmuyor (TS_ESIK ön kayıttan sonra değişmiş)")
    if manifest is not None and O["VERI_MANIFEST_SHA256"] != manifest:
        raise TsHata("veri manifesti ön kayıttakiyle aynı değil (fiyat önbelleği değişmiş)")
    ks = ts_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise TsHata("TAVAN_SERISI.py ön kayıttan sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]
    return out


# ---------------------------------------------------------------- 7) KOŞU VE RAPOR
def ts_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
           S: Optional[Dict[str, pd.DataFrame]] = None, K: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or TS_ESIK
    if S is None:
        S, K = ts_fiyatlar()
    Kp = ts_kapi(kl, git, sapma, E, manifest=(K or {}).get("manifest_sha256"))
    t0 = _ts_simdi(); tslog.info("kapı geçti (mühür %s)", Kp["esik_sha256"][:12])
    P = ts_panel(S, kes=E["olay"]["kriz"], E=E); U = ts_ufuk_panelleri(P, E)
    Ev = ts_olaylar(P, U, E["olay"]["donem"][0], E["olay"]["donem"][1], True, E)
    tslog.info("test olayları: %d satır", len(Ev))
    sonuc: Dict[str, Any] = {"surum": TS_SURUM, "baslangic": t0, "kapi": Kp, "kapsam": {k: v for k, v in (K or {}).items() if k != "eksik"},
                             "eksik": (K or {}).get("eksik"), "sayim": ts_sayim(P, E), "cokmus": {}, "cokmus_kilitsiz": {}, "cokmemis": {}, "karar": {}}
    for k in E["olay"]["k"]:
        Ck = Ev[(Ev.k == k) & (Ev.sinif == "COKMUS")]
        if len(Ck):
            o = ts_ozet_k(Ck, True, E); sonuc["cokmus"][k] = o; sonuc["karar"][k] = ts_karar(o, E)
            Kk = Ck[~Ck.dolum_belirsiz.fillna(False).astype(bool)]
            if len(Kk):
                ok = ts_ozet_k(Kk, True, E); sonuc["cokmus_kilitsiz"][k] = ok; ok["karar"] = ts_karar(ok, E)["karar"]
        Nk = Ev[(Ev.k == k) & (Ev.sinif == "COKMEMIS")]
        if len(Nk):
            sonuc["cokmemis"][k] = ts_ozet_k(Nk, False, E, boot=False)
        tslog.info("k=%d: çökmüş %d, çökmemiş %d", k, len(Ck), len(Nk))
    sonuc["duyarlilik"] = {}
    for e in E["duyarlilik"]["esik"]:
        E2 = ts_esik_gevsek(e, E); Ev2 = ts_olaylar(P, U, E["olay"]["donem"][0], E["olay"]["donem"][1], True, E2); dd = {}
        for k in E["olay"]["k"]:
            Ck = Ev2[(Ev2.k == k) & (Ev2.sinif == "COKMUS")]
            if len(Ck):
                o = ts_ozet_k(Ck, True, E2); o["karar"] = ts_karar(o, E2)["karar"]; dd[k] = o
        sonuc["duyarlilik"][f"{e:.2f}"] = dd
        tslog.info("duyarlılık %.2f: %s", e, {k: v["n"] for k, v in dd.items()})
    # BİLGİ: Eylül - Kasım 2026 (kriz sonrası; tam veri, gün içi son bar atılır)
    son = max(d.index[-1] for d in S.values())
    kesB = (son - pd.Timedelta(days=1)) if ts_gun_ici(son) else son
    PB = ts_panel(S, kes=str(kesB.date()), E=E); UB = ts_ufuk_panelleri(PB, E)
    EB = ts_olaylar(PB, UB, E["olay"]["bilgi"][0], None, False, E)
    sonuc["bilgi"] = {"kes": str(kesB.date()), "k": {}}
    for k in E["olay"]["k"]:
        Bk = EB[(EB.k == k) & (EB.sinif == "COKMUS")] if len(EB) else EB
        if len(Bk):
            et = pd.to_numeric(Bk.ertesi_tavan, errors="coerce").dropna()
            sonuc["bilgi"]["k"][k] = {"n": int(len(Bk)), "hisse": int(Bk.sembol.nunique()), "p_ertesi_tavan": float(et.mean()) if len(et) else np.nan,
                                      "n_ertesi": int(len(et)), "acik_seri": int(Bk.seri_acik.sum()), "r5": _q(Bk.get("r5", pd.Series(dtype=float))),
                                      "semboller": sorted(Bk.sembol.unique().tolist())[:40]}
    sonuc["bitis"] = _ts_simdi()
    os.makedirs(TS_YOL["is"], exist_ok=True)
    Ev.to_csv(os.path.join(TS_YOL["is"], TS_DOSYA["olay"]), index=False)
    if len(EB):
        EB.to_csv(os.path.join(TS_YOL["is"], "tavan_olaylar_bilgi.csv.gz"), index=False)
    _ts_json(_ts_yol("sonuc", kl), sonuc); _ts_yaz(_ts_yol("rapor", kl), ts_rapor_md(_ts_kayit(sonuc), E))
    return sonuc


def _g(o: Dict[str, Any], *ks: Any) -> Any:
    for k in ks:
        if not isinstance(o, dict):
            return None
        o = o.get(str(k), o.get(k)) if isinstance(k, (int, str)) else None
    return o


def _ar(a: Any) -> str:
    try:
        return f"[{_f(100 * a[0], 1)}, {_f(100 * a[1], 1)}]"
    except (TypeError, IndexError, ValueError):
        return "—"


def ts_rapor_md(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    """Tek sayfa düz Türkçe rapor (sonuç JSON'undan)."""
    E = E or TS_ESIK; ks = [str(k) for k in E["olay"]["k"]]; C = S.get("cokmus", {}); Kr = S.get("karar", {})
    kap = S.get("kapi", {})
    gecen = [k for k in ks if _g(Kr, k, "karar") == "KONTROLDEN İYİ"]
    kumar = [k for k in ks if str(_g(Kr, k, "karar") or "").startswith("KUMAR")]
    yetersiz = [k for k in ks if _g(Kr, k, "karar") == "örneklem yetersiz"]
    dz = []
    for e, dd in S.get("duyarlilik", {}).items():
        ol = [(k, o) for k, o in dd.items() if o.get("n_fark", 0) >= E["karar"]["n_min"]]
        neg = [k for k, o in ol if o.get("fark_med_ci") and o["fark_med_ci"][1] is not None and o["fark_med_ci"][1] < 0]
        dz.append(f"eşik {_y(float(e))}: n >= 30 olan k = {', '.join(k for k, _ in ol) or 'yok'}; bunlardan medyan farkın %95 aralığı tamamen 0'ın altında "
                  f"olan: {', '.join(neg) or 'yok'}")
    L = ["# Çökmüş hissede art arda tavan: k. tavandan sonra katılmak (BIST 2016 - Ağu 2026)", "",
         f"Ön kayıt {kap.get('onkayit_git', {}).get('commit', '—')[:7]} ({kap.get('onkayit_git', {}).get('commit_zamani', '—')}), mühür "
         f"{str(kap.get('esik_sha256', '—'))[:12]}" + (f"; SAPMA: {kap.get('sapma')}" if kap.get("sapma") else "") + ".", "",
         "## Sonuç", "",
         ("**Hiçbir k'da 'kontrolden iyi' değil.**" if not gecen else
          f"**'Kontrolden iyi' çıkan k: {', '.join(gecen)}** (8 k sınandı; tek k'nın geçmesi çoklu deneme şansı olabilir).")
         + (f" KUMAR (beklenen değer kontrolden iyi değil): k = {', '.join(kumar)}." if kumar else "")
         + (f" Örneklem yetersiz (n < 30, karar yok): k = {', '.join(yetersiz)}." if yetersiz else ""), "",
         "Duyarlılık (BİLGİ, karara girmez): " + ("; ".join(dz) if dz else "yok") + ".", "",
         "Düz dille:"] + [f"- Çökmüş hissede {k}. tavandan sonraki gün açılıştan katılan ({C[k]['n']} olay, {C[k]['n_hisse']} hisse): ertesi gün de tavan "
                          f"{_y(C[k]['p_ertesi_tavan'])}; 60 günde medyan {_y(C[k]['r60']['med'])}; +%100'e ulaşan {_y(C[k]['up100_60'])}, -%50'ye düşen "
                          f"{_y(C[k]['dn50_60'])} (120 günde {_y(C[k]['dn50_120'])}); tavan yapmayan eş çökmüşlere göre medyan fark {_y(C[k].get('fark_med'), 1)}."
                          for k in ks[:3] if C.get(k)] + \
        ([f"- Çökmemiş hissede aynı durum (BİLGİ): 1. tavandan sonra 60 günde medyan {_y(S['cokmemis']['1']['r60']['med'])}, +%100 "
          f"{_y(S['cokmemis']['1']['up100_60'])}, -%50 {_y(S['cokmemis']['1']['dn50_60'])}."] if S.get("cokmemis", {}).get("1") else []) + \
        ([f"- Fon krizi sonrası (Eylül - Kasım 2026, BİLGİ): çökmüş hissede 1. tavandan sonra ertesi gün de tavan "
          f"{_y(_g(S, 'bilgi', 'k', '1', 'p_ertesi_tavan'))}, 3. tavandan sonra {_y(_g(S, 'bilgi', 'k', '3', 'p_ertesi_tavan'))} (geçmişte "
          f"{_y(_g(C, '1', 'p_ertesi_tavan'))} / {_y(_g(C, '3', 'p_ertesi_tavan'))}): seriler bu dönemde daha uzun; sonucu henüz bilinmiyor."]
         if _g(S, "bilgi", "k", "1") else []) + ["",
         "## Olasılık tablosu (ÇÖKMÜŞ hisse, giriş k. tavandan sonraki gün açılış)", "",
         "| k | n (hisse) | ertesi gün de tavan | 60g medyan getiri | 60g'de +%100'e dokunma | 60g'de -%50'ye dokunma | 120g'de -%50 | kontrol 60g -%50 | "
         "medyan fark (60g) | %95 aralık | karar |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in ks:
        o = C.get(k)
        if not o:
            L.append(f"| {k} | 0 | — | — | — | — | — | — | — | — | olay yok |"); continue
        L.append(f"| {k} | {o['n']} ({o['n_hisse']}) | {_y(o['p_ertesi_tavan'])} | {_y(o['r60']['med'])} | {_y(o['up100_60'])} | {_y(o['dn50_60'])} | "
                 f"{_y(o['dn50_120'])} | {_y(o.get('k_dn50_60'))} | {_y(o.get('fark_med'), 1)} | {_ar(o.get('fark_med_ci'))} | {_g(Kr, k, 'karar') or '—'} |")
    L += ["", "Kontrol kapsamı: " + "; ".join(f"k={k}: farkı ölçülen {C[k].get('n_fark', 0)}, kontrolsüz {C[k].get('kontrolsuz', 0)}, olay başına kontrol "
                                               f"hissesi medyanı {_f(C[k].get('n_kontrol_medyan'), 0)}" for k in ks if C.get(k)) + "."]
    L += ["", "Fark = olayın 60 gün getirisi - aynı gün, aynı derinlik kovasında çökmüş ama seri boyunca tavan yapmamış hisselerin ortalaması; aralık hisse "
          "kümeli bootstrap. 'Ertesi gün de tavan' bütün olaylardan; getiriler 60 gün penceresi 31.08.2026'dan önce biten olaylardan.", "",
          "## Getiri dağılımı ve seri uzunluğu", "",
          "| k | 5g medyan | 20g medyan | 60g medyan (ort.) [%25, %75] | 120g medyan | seri en az k+1 | k+3 | k+5 | dolum belirsiz payı | kontrol 60g medyan |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in ks:
        o = C.get(k)
        if not o:
            continue
        sr = o["seri"]; ki = int(k)
        L.append(f"| {k} | {_y(o['r5']['med'])} | {_y(o['r20']['med'])} | {_y(o['r60']['med'])} ({_y(o['r60']['ort'])}) [{_y(o['r60']['q25'])}, "
                 f"{_y(o['r60']['q75'])}] | {_y(o['r120']['med'])} (n {o['r120']['n']}) | {_y(sr.get(f'P(L>={ki + 1})'))} | {_y(sr.get(f'P(L>={ki + 3})'))} | "
                 f"{_y(sr.get(f'P(L>={ki + 5})'))} | {_y(o['dolum_belirsiz_pay'])} | {_y(o.get('k_r60_med_ort'))} |")
    L += ["", "## Dönemler (60g medyan fark; P(-%50) olay / kontrol)", "", "| k | 2016-19 | 2020-22 | 2023-26.08 | yön tutan dönem |", "|---|---|---|---|---|"]
    for k in ks:
        o = C.get(k)
        if not o:
            continue
        hc = []
        for dn in ("2016-19", "2020-22", "2023-26.08"):
            d = o.get("donem", {}).get(dn, {})
            hc.append(f"n {d.get('n', 0)}: {_y(d.get('fark_med'), 1)}; {_y(d.get('dn50_60'))} / {_y(d.get('k_dn50_60'))}")
        dp, dol = _g(Kr, k, "donem_pozitif"), _g(Kr, k, "donem_olculen")
        L.append(f"| {k} | " + " | ".join(hc) + (f" | {dp} / {dol} |" if dp is not None else " | — (n < 30) |"))
    L += ["", "## Yalnız dolum belirsiz olmayan girişler (giriş günü tam kilitli tavan değil)", "",
          "| k | n | 60g medyan | +%100 | -%50 | medyan fark [%95] | karar |", "|---|---|---|---|---|---|---|"]
    for k in ks:
        o = S.get("cokmus_kilitsiz", {}).get(k)
        if o:
            L.append(f"| {k} | {o['n']} | {_y(o['r60']['med'])} | {_y(o['up100_60'])} | {_y(o['dn50_60'])} | {_y(o.get('fark_med'), 1)} "
                     f"{_ar(o.get('fark_med_ci'))} | {o.get('karar', '—')} |")
    L += ["", "## Karşılaştırma: ÇÖKMEMİŞ hissede k. tavan (BİLGİ, kontrolsüz)", "",
          "| k | n | ertesi gün tavan | 60g medyan | +%100 | -%50 |", "|---|---|---|---|---|---|"]
    for k in ks:
        o = S.get("cokmemis", {}).get(k)
        if o:
            L.append(f"| {k} | {o['n']} | {_y(o['p_ertesi_tavan'])} | {_y(o['r60']['med'])} | {_y(o['up100_60'])} | {_y(o['dn50_60'])} |")
    L += ["", "## Duyarlılık: ÇÖKMÜŞ eşiği gevşek (BİLGİ, karara girmez)", "",
          "| eşik | k | n (hisse) | ertesi gün tavan | 60g medyan | +%100 | -%50 (kontrol) | medyan fark [%95] | kural sonucu |", "|---|---|---|---|---|---|---|---|---|"]
    for e, dd in S.get("duyarlilik", {}).items():
        for k in ks:
            o = dd.get(k)
            if o:
                L.append(f"| {_y(float(e))} | {k} | {o['n']} ({o['n_hisse']}) | {_y(o['p_ertesi_tavan'])} | {_y(o['r60']['med'])} | {_y(o['up100_60'])} | "
                         f"{_y(o['dn50_60'])} ({_y(o.get('k_dn50_60'))}) | {_y(o.get('fark_med'), 1)} {_ar(o.get('fark_med_ci'))} | {o.get('karar', '—')} |")
    B = S.get("bilgi", {})
    L += ["", f"## BİLGİ: fon krizi sonrası (Eylül 2026 - {B.get('kes', '—')}) çökmüş hissede k. tavan (karara girmez)", "",
          "| k | olay (hisse) | ertesi gün de tavan | seri hâlâ açık | 5g medyan (n) |", "|---|---|---|---|---|"]
    for k in ks:
        o = B.get("k", {}).get(k)
        if o:
            L.append(f"| {k} | {o['n']} ({o['hisse']}) | {_y(o['p_ertesi_tavan'])} (n {o['n_ertesi']}) | {o['acik_seri']} | "
                     f"{_y(_g(o, 'r5', 'med'))} ({_g(o, 'r5', 'n')}) |")
    L += ["", "## Tanım ve sınırlar", "",
          "- ÇÖKMÜŞ: seri ilk tavanından önceki gün kapanışı, kendi son 250 barının en yüksek kapanışından en az %80 aşağıda. Tavan: 13.03.2020'den "
          "(BIST ±%10) günlük >= %9,5 (1-2 TL'de fiyat adımına göre gerçek tavan) ve <= %10,5; 12.03.2020'ye kadar (BIST ±%20) >= %19 ve <= %21; "
          "|günlük| > %25 veri kırığı.",
          "- Kontrol: aynı referans günü, aynı derinlik kovası ((-%85, -%80], (-%90, -%85], <= -%90), seri boyunca tavansız, giriş günü işlem gören hisseler.",
          f"- Yanlılık: {E['yanlilik']}.",
          f"- Karar cümlesi (önceden yazılı): {E['karar']['metin']}"]
    return "\n".join(L) + "\n"


def ts_rapor(kl: Optional[str] = None) -> str:
    S = _ts_json_oku(_ts_yol("sonuc", kl))
    return _ts_yaz(_ts_yol("rapor", kl), ts_rapor_md(S))


# ---------------------------------------------------------------- 8) HACİM ALT KOMUTU (Cemal'in itirazı, 13.11.2026; ön kayıt HACIM_ON_KAYIT.md)
# H1 devasa hacim barı (çökmüş + hacim >= k x 20 gün medyanı + tavan), H2 dipte tavansız hacim (birikim), H3 taban fiyat ('1 liradan nereye düşer').
# Okuma (ts_fiyatlar / ts_yahoo_oku), tavan (ts_tavan: marj rejimi + fiyat adımı), derinlik, takvim paneli (ts_panel), kova (ts_kova / ts_esik_gevsek),
# bootstrap (ts_boot), dönem (ts_donem), git / mühür okuma (ts_git_durum / ts_onkayit_oku) YENİDEN KULLANILIR; yukarıdaki kod değişmedi.
TH_ETIKET = "tavan_hacim_20261113"
TH_SURUM = ("TAVAN_SERISI hacim v1.0 (tavan_hacim_20261113): çökmüş BIST hissesinde devasa hacim barı (H1), dipte tavansız hacim (H2), "
            "taban fiyat (H3); ön kayıtlı")
TH_DOSYA: Dict[str, str] = {"onkayit": "HACIM_ON_KAYIT.md", "sonuc": "hacim_sonuc.json", "rapor": "HACIM_RAPOR.md", "olay": "hacim_olaylar.csv.gz",
                            "bilgi": "hacim_olaylar_bilgi.csv.gz", "h3": "hacim_h3.csv.gz", "grafik": "grafik"}
TH_IZLE: List[str] = ["TEHOL", "PEKGY", "IEYHO", "DSTKF", "OZATD", "TRHOL"]

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (mühür: th_esik_sha; sonuç görüldükten sonra değişmez)
TH_ESIK: Dict[str, Any] = {
    "surum_etiket": TH_ETIKET,
    "veri": "TAVAN_SERISI ile aynı Yahoo günlük önbellek (/tmp/tavan/yahoo, ts_fiyatlar); tavan = ts_tavan (TS_ESIK['tavan']: BIST marjı 12.03.2020'ye "
            "kadar ±%20, 13.03.2020'den ±%10; 1-2 TL'de fiyat adımı; |günlük| > %25 veri kırığı); derinlik = ts_tavan (kendi son 250 barının en yüksek "
            "kapanışı, kırıktan sonra yeniden dolar); takvim = ts_panel (en az 10 hisse); hacim = Yahoo adet (bölünme düzeltmeli)",
    "donem": ["2016-01-01", "2026-08-31"], "kriz": "2026-08-31", "bilgi_bas": "2026-09-01",
    "cokmus": {"esik": -0.80, "duyarlilik": [-0.70, -0.60],
               "tanim": "derinlik = olay gününden ÖNCEKİ kendi barının kapanışı / o barın son 250 barlık en yüksek kapanışı - 1 (ts_tavan 'derinlik' bir "
                        "bar geri); ÇÖKMÜŞ <=> derinlik <= eşik; tanımsızsa olay değil, kontrol değil"},
    "hacim": {"pencere": 20, "kat": 10.0, "duyarlilik": [5.0, 20.0, 50.0], "kontrol_ust": 3.0,
              "tanim": "hacim oranı = t günü hacmi / t'den önceki 20 kendi barının hacim medyanı; önceki 20 bar yoksa ya da medyan <= 0 ise tanımsız"},
    "hip": {"H1": {"getiri": "tavan", "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü tavan (ts_tavan; 13.03.2020'den >= +%9,5, öncesi >= +%19)"},
            "H1b": {"getiri": [0.05, 0.25], "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü kapanış getirisi >= +%5 (ve <= %25: kırık değil)"},
            "H2": {"getiri": [-0.05, 0.05], "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü kapanış getirisi -%5 .. +%5 (dipte birikim, tavansız)"}},
    "tekil": {"gun": 20, "tanim": "aynı hisse ve aynı hücre (hipotez x derinlik eşiği x hacim katı) için bir olaydan sonraki 20 kendi barı içinde yeni olay "
                                  "sayılmaz (kronolojik, açgözlü); iki giriş türü aynı olayları kullanır"},
    "giris": {"a": "ANA: t'den sonraki ilk kendi barı e'nin açılışı O_e; O yok / hacim 0 -> 'giriş yok' (sayılır); e tam kilitli tavansa 'dolum belirsiz' "
                   "işareti (sonuç yine O_e'den)",
              "b": "t kapanışı C_t; t kilitli tavan (ts_tavan 'kilitli': O = H = C) ise 'alınamaz' (sayılır, ölçülmez)"},
    "olcu": {"ufuk": [5, 20, 60], "dok": [["up61_20", 20, 0.61], ["up100_60", 60, 1.0], ["dn50_60", 60, -0.5]],
             "yaris": {"ufuk": 60, "yukari": 0.5, "asagi": -0.25},
             "tanim": "giriş a satırı e: pencere e .. e+h-1, r_h = C(e+h-1) / O_e - 1; giriş b satırı t: pencere t+1 .. t+h, r_h = C(t+h) / C_t - 1 (iki "
                      "girişte aynı son gün; takvim satırı, durdurmada son kapanış ileri taşınır). Dokunma: pencerede max H >= giriş x (1 + eşik) ya da "
                      "min L <= giriş x (1 + eşik). +%61 = Cemal'in '5 tavan' (1,1^5 = 1,61). Yarış: 60 bar içinde ilk H >= 1,5 giriş mi ilk L <= 0,75 "
                      "giriş mi; aynı gün ikisi 'aynı gün', hiçbiri 'yok'. Pencere kesiği (31.08.2026) aşan ölçü yok; pencerede veri kırığı "
                      "(|günlük| > %25) varsa o ölçü yok (sayısı yazılır). En kötü %10: r60'ın 10. yüzdeliği ve en kötü %10 olayın ortalaması"},
    "kontrol": {"kova_ana": [-0.80, -0.85, -0.90],
                "tanim": "her ÇÖKMÜŞ olay için: aynı t gününde aynı derinlik kovasında (ana -0,80: (-0,85, -0,80], (-0,90, -0,85], <= -0,90; -0,70 / "
                         "-0,60'ta eşikten -1'e üç eşit dilim, ts_esik_gevsek), t günü hacim oranı tanımlı ve < 3 olan, giriş satırında işlem gören "
                         "(a: O var ve hacim > 0; b: C_t var) bütün öteki hisseler; aynı giriş türüyle aynı ölçüler; kontrol değeri = kontrol hisselerinin "
                         "ortalaması (oranlarda ortalama oran)",
                "fark": "olay başına fark = olay r60 - kontrol ortalama r60; kontrolü olmayan olay farkta dışarıda (sayılır)"},
    "bootstrap": {"B": 2000, "tohum": 20261113, "kume": "hisse (olaylar hisseleriyle birlikte çekilir)", "guven": [2.5, 97.5]},
    "donem_kirilim": {"2016-19": ["2016-01-01", "2019-12-31"], "2020-22": ["2020-01-01", "2022-12-31"], "2023-26.08": ["2023-01-01", "2026-08-31"],
                      "tanim": "dönem = olay günü t (H3'te ay başı günü)"},
    "karar": {"n_min": 30, "p61_kat": 1.5, "p50_kat": 1.2, "donem_min": 2, "donem_n_min": 10, "ana": "H1|-0.80|10|a", "ikincil": "H2|-0.80|10|a",
              "metin": "H1 ANA (ÇÖKMÜŞ -%80, hacim >= 10x, tavan, giriş a) 'İZ ADAYI (BIST)' <=> n (60 gün farkı ölçülen olay) >= 30 VE medyan 60 gün "
                       "fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(+%61, 20g) olay >= 1,5 x kontrol (kontrol 0 ise olay > 0 yeter) VE "
                       "P(-%50, 60g) olay <= 1,2 x kontrol (kontrol 0 ise olay da 0 olmalı) VE üç dönemin (2016-19 / 2020-22 / 2023-26.08; n >= 10 "
                       "olanlar) en az ikisinde dönem medyan farkı > 0. Değilse 'KANIT YOK' ve tutmayan şartlar yazılır (n < 30: 'örneklem yetersiz', "
                       "yine KANIT YOK). H2 ANA (hacim >= 10x, -%5..+%5, giriş a) aynı cümleyle İKİNCİL. Öteki hücreler (derinlik -%70 / -%60, kat "
                       "5 / 20 / 50, H1b, giriş b) BİLGİ: kural sonucu yazılır, kararı değiştirmez; kaç hücrenin geçtiği çoklu deneme olarak yazılır. "
                       "H3 için yalnız sayı, karar yok."},
    "h3": {"ay": "her hisse-ay: ayın ilk kendi işlem günü t (2016-01 .. kesik); ÇÖKMÜŞ <=> C_t / kendi son 250 barının en yüksek kapanışı - 1 <= -0,80 "
                 "(ts_tavan 'derinlik', aynı gün)",
           "kova": [[0.0, 1.0], [1.0, 2.0], [2.0, 5.0], [5.0, None]],
           "fiyat": "ekran fiyatı = Yahoo kapanış x sonraki bölünmeler çarpanı (o gün tahtada görünen fiyat)",
           "giris": "C_t; pencere t+1 .. t+h", "ufuk": [60, 120, 250],
           "olcu": "P(-%50'ye dokunma) 60 / 120 / 250 gün; en düşük nokta = min L[t+1 .. t+250] / C_t - 1 (medyan, %10, %25); BİLGİ: P(+%100, 250g), "
                   "r250 medyan; karşılaştırma: aynı şart 2 TL ve üstü çökmüşler; ayrıca ÇÖKMEMİŞ 2 TL altı (BİLGİ); dönem kırılımı; hisse kümeli %95 "
                   "aralık (oranlar). Karar yok."},
    "grafik": {"tohum": 20261113, "adet": 3, "iyi": "H1 ANA, giriş a, r60 > 0", "kotu": "H1 ANA, giriş a, r60 <= 0", "once": 120, "sonra": 60,
               "tanim": "iyi ve kötü gruplarından (sembol, tarih) sırasıyla dizilip tohumlu rastgele 3'er olay; PNG /tmp/tavan/grafik (repoya girmez)"},
    "bilgi": "Eylül 2026 - son bar olayları (H1 / H2 ana tanım, giriş a; kontrol yok) ayrı tablo, karara girmez; sonuç penceresi tamamlanmamış ölçü 'açık'; "
             "son bar gün içiyse işaretlenir; bugüne kadar: son kapanış / giriş, girişten sonra en yüksek ve en düşük. İzlenen hisseler (TEHOL, PEKGY, "
             "IEYHO, DSTKF, OZATD, TRHOL): son 10 barın getirisi, hacim oranı, derinliği, H1 / H2 koşul işaretleri",
    "yanlilik": "evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker, özellikle H3'te "
                "-%50 olasılığını AŞAĞI); işlem maliyeti yok; kilitli tavanda giriş a'nın dolumu belirsiz; olaylar takvimde örtüşebilir (aynı gün "
                "birden çok hisse), aralık hisse kümeli",
}


def th_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Hacim ön kayıt mührü: TH_ESIK + yeniden kullanılan TS tanımları (tavan, kova, fiyat adımı)."""
    s = json.dumps({"TH": E or TH_ESIK, "ADIM": TS_ADIM, "TAVAN": TS_ESIK["tavan"], "KOVA": TS_ESIK["kontrol"]["kova"], "COKMUS_TS": TS_ESIK["olay"]["cokmus"]},
                   sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _th_yol(ad: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or TS_YOL["cikti"], TH_DOSYA.get(ad, ad))


def th_kova_listesi(e: float) -> List[float]:
    """Derinlik eşiğine göre kontrol kovaları: -0,80'de TS sabit kovaları, öteki eşiklerde ts_esik_gevsek."""
    return list(TS_ESIK["kontrol"]["kova"]) if abs(e - TS_ESIK["kontrol"]["kova"][0]) < 1e-12 else ts_esik_gevsek(e)["kontrol"]["kova"]


def th_hacim_oran(v: np.ndarray, n: int = 20) -> np.ndarray:
    """Kendi barlarında hacim oranı: v_t / medyan(v_{t-n} .. v_{t-1}); n bar yoksa ya da medyan <= 0 ise NaN."""
    v = np.asarray(v, float)
    med = pd.Series(v).shift(1).rolling(int(n), min_periods=int(n)).median().to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = v / med
    out[~(med > 0)] = np.nan
    return out


def th_hisse_ek(d: pd.DataFrame, X: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Kendi barlarında: hacim oranı (HO), önceki barın derinliği (DO), ekran kapanışı, ts_tavan sütunları."""
    E = E or TH_ESIK
    return pd.DataFrame({"HO": th_hacim_oran(d.v.to_numpy(float), E["hacim"]["pencere"]), "DO": X.derinlik.shift(1).to_numpy(float),
                         "der": X.derinlik.to_numpy(float), "r": X.r.to_numpy(float), "tavan": X.tavan.to_numpy(bool),
                         "kilitli": X.kilitli.to_numpy(bool), "tam_kilitli": X.tam_kilitli.to_numpy(bool), "kirik": X.kirik.to_numpy(bool),
                         "ekran": (d.c * d["carpan"]).to_numpy(float), "carpan": d["carpan"].to_numpy(float)}, index=d.index)


def th_panel(S: Dict[str, pd.DataFrame], kes: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """ts_panel + hacim ekleri: HO / DO / KR panelleri ve hisse başına ek tablo (P['Y'])."""
    E = E or TH_ESIK; P = ts_panel(S, kes=kes, E=TS_ESIK); tak = P["takvim"]; Y: Dict[str, pd.DataFrame] = {}
    for s in P["sym"]:
        Y[s] = th_hisse_ek(P["S"][s], P["X"][s], E)
    P["Y"] = Y
    P["HO"] = pd.DataFrame({s: Y[s].HO for s in P["sym"]}).reindex(tak)
    P["DO"] = pd.DataFrame({s: Y[s].DO for s in P["sym"]}).reindex(tak)
    P["KR"] = pd.DataFrame({s: Y[s].kirik.astype(float) for s in P["sym"]}).reindex(tak).fillna(0.0)
    return P


def _th_ileri(A: np.ndarray, h: int, f: str, kay: int) -> np.ndarray:
    """out[i] = f(A[i+kay .. i+kay+h-1]) (NaN atlanır; f = max / min / sum); pencere takvim sonunu aşarsa NaN."""
    n = A.shape[0]; R = pd.DataFrame(A[::-1]).rolling(int(h), min_periods=1)
    R = (R.max() if f == "max" else (R.min() if f == "min" else R.sum())).to_numpy(float)[::-1]
    out = np.full(A.shape, np.nan); m = n - kay - h + 1
    if m > 0:
        out[:m] = R[kay:kay + m]
    return out


def th_olcu_panelleri(P: Dict[str, Any], mod: str, ufuk: List[int], dok: List[List[Any]], yaris: Optional[Dict[str, Any]] = None,
                      dip: Optional[List[int]] = None) -> Dict[str, np.ndarray]:
    """Her (satır, hisse) girişi için sonuç panelleri. mod 'a': giriş O[i] (hacim > 0), pencere i .. i+h-1; mod 'b': giriş C[i], pencere i+1 .. i+h.
    r{h}, dokunma (ad 'up..' max H >= B(1+e), 'dn..' min L <= B(1+e)), dip{h} = min L / B - 1, yarış (y_up / y_dn / y_ayni / y_yok), kir{h} işareti.
    Pencere eksikse ya da içinde veri kırığı varsa NaN."""
    kay = 0 if mod == "a" else 1
    O = P["O"].to_numpy(float); C = P["C"].to_numpy(float); V = P["V"].to_numpy(float); Cf = P["Cf"].to_numpy(float)
    H = P["H"].to_numpy(float); L = P["L"].to_numpy(float); KR = P["KR"].to_numpy(float); n = O.shape[0]
    with np.errstate(invalid="ignore"):
        B = np.where(np.isfinite(O) & (V > 0), O, np.nan) if mod == "a" else np.where(np.isfinite(C), C, np.nan)
    out: Dict[str, np.ndarray] = {"B": B}
    hs = sorted(set(list(ufuk) + [int(x[1]) for x in dok] + list(dip or []) + ([int(yaris["ufuk"])] if yaris else [])))
    kir = {h: _th_ileri(KR, h, "sum", kay) > 0 for h in hs}
    for h in hs:
        out[f"kir{h}"] = kir[h].astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        for h in ufuk:
            R = np.full(O.shape, np.nan); m = n - kay - h + 1
            if m > 0:
                R[:m] = Cf[kay + h - 1:kay + h - 1 + m] / B[:m] - 1.0
            R[kir[h]] = np.nan; out[f"r{h}"] = R
        for ad, h, e in dok:
            up = str(ad).startswith("up"); A = _th_ileri(H if up else L, int(h), "max" if up else "min", kay)
            Z = ((A >= B * (1 + e)) if up else (A <= B * (1 + e))).astype(float)
            Z[~np.isfinite(A) | ~np.isfinite(B) | kir[int(h)]] = np.nan; out[ad] = Z
        for h in dip or []:
            A = _th_ileri(L, int(h), "min", kay); Z = A / B - 1.0; Z[kir[int(h)]] = np.nan; out[f"dip{h}"] = Z
        if yaris:
            h = int(yaris["ufuk"]); m = n - kay - h + 1
            iu = np.full(O.shape, np.inf); idn = np.full(O.shape, np.inf)
            for k in range(h - 1, -1, -1):        # geriye doğru: en küçük k kalır
                if m <= 0:
                    break
                Hk = H[kay + k:kay + k + m]; Lk = L[kay + k:kay + k + m]
                iu[:m][Hk >= B[:m] * (1 + yaris["yukari"])] = k
                idn[:m][Lk <= B[:m] * (1 + yaris["asagi"])] = k
            gec = np.zeros(O.shape, bool)
            if m > 0:
                gec[:m] = True
            gec &= np.isfinite(B) & ~kir[h]
            for ad, z in (("y_up", iu < idn), ("y_dn", idn < iu), ("y_ayni", (iu == idn) & np.isfinite(iu)), ("y_yok", ~np.isfinite(iu) & ~np.isfinite(idn))):
                Z = z.astype(float); Z[~gec] = np.nan; out[ad] = Z
    return out


def th_olcu_listesi(E: Optional[Dict[str, Any]] = None) -> List[str]:
    E = E or TH_ESIK
    return [f"r{h}" for h in E["olcu"]["ufuk"]] + [x[0] for x in E["olcu"]["dok"]] + ["y_up", "y_dn", "y_ayni", "y_yok"]


def th_olaylar(P: Dict[str, Any], hip: str, esik: float, kat: float, mod: str, bas: str, bit: Optional[str], M: Optional[Dict[str, np.ndarray]] = None,
               kontrol: bool = True, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Bir hücrenin olayları (hipotez, derinlik eşiği, hacim katı, giriş türü). M = th_olcu_panelleri(P, mod, ...) verilirse ölçüler ve kontrol."""
    E = E or TH_ESIK; tak = P["takvim"]; ix = {t: i for i, t in enumerate(tak)}; sym = P["sym"]; sj = {s: j for j, s in enumerate(sym)}
    b0 = pd.Timestamp(bas); b1 = pd.Timestamp(bit) if bit else tak[-1]; g = E["hip"][hip]["getiri"]; tek = int(E["tekil"]["gun"])
    kv = th_kova_listesi(esik); olcu = th_olcu_listesi(E); kust = float(E["hacim"]["kontrol_ust"])
    DOp = P["DO"].to_numpy(float); HOp = P["HO"].to_numpy(float); O = P["O"].to_numpy(float); V = P["V"].to_numpy(float); C = P["C"].to_numpy(float)
    sat = []
    for s in sym:
        Y = P["Y"][s]; j = sj[s]; di = Y.index
        with np.errstate(invalid="ignore"):
            m = (Y.DO.to_numpy() <= esik) & (Y.HO.to_numpy() >= kat) & (di >= b0) & (di <= b1)
            r = Y.r.to_numpy()
            m &= Y.tavan.to_numpy() if g == "tavan" else ((r >= g[0]) & (r <= g[1]) & ~Y.kirik.to_numpy())
        son = -10 ** 9
        for i in np.flatnonzero(m):
            if i - son <= tek:
                continue
            son = i; t = di[i]
            rec = {"sembol": s, "t": t, "hip": hip, "esik": esik, "kat": kat, "mod": mod, "derinlik": float(Y.DO.iloc[i]),
                   "kova": ts_kova(float(Y.DO.iloc[i]), {"kontrol": {"kova": kv}}), "hacim_oran": float(Y.HO.iloc[i]), "r_t": float(r[i]),
                   "tavan_t": bool(Y.tavan.iloc[i]), "kilitli_t": bool(Y.kilitli.iloc[i]), "ekran_t": float(Y.ekran.iloc[i]), "donem": ts_donem(t, {"donem": E["donem_kirilim"]})}
            rt = ix.get(t)
            if rt is None:
                rec["durum"] = "takvim dışı"; sat.append(rec); continue
            if mod == "a":
                if i + 1 >= len(di):
                    rec["durum"] = "giris yok (veri sonu)"; sat.append(rec); continue
                e = di[i + 1]; row = ix.get(e); rec["e"] = e
                if row is None or not np.isfinite(O[row, j]) or not V[row, j] > 0:
                    rec["durum"] = "giris yok (islem yok)"; sat.append(rec); continue
                rec["giris"] = float(O[row, j]); rec["dolum_belirsiz"] = bool(Y.tam_kilitli.iloc[i + 1])
                rec["giris_ekran"] = rec["giris"] * float(Y.carpan.iloc[i + 1])
            else:
                if bool(Y.kilitli.iloc[i]):
                    rec["durum"] = "alinamaz (kilitli)"; sat.append(rec); continue
                row = rt; rec["e"] = t; rec["giris"] = float(C[row, j]); rec["dolum_belirsiz"] = False; rec["giris_ekran"] = float(Y.ekran.iloc[i])
            rec["durum"] = "tamam"; rec["row"] = int(row)
            if M is not None:
                for mm in olcu:
                    rec[mm] = float(M[mm][row, j])
                rec["kir60"] = bool(M["kir60"][row, j] > 0) if np.isfinite(M["kir60"][row, j]) else np.nan
                if kontrol:
                    with np.errstate(invalid="ignore"):
                        d = DOp[rt]; kp = np.full(len(sym), -1)
                        kp[d <= kv[0]] = 0; kp[d <= kv[1]] = 1; kp[d <= kv[2]] = 2
                        km = (kp == rec["kova"]) & np.isfinite(HOp[rt]) & (HOp[rt] < kust)
                        km &= (np.isfinite(O[row]) & (V[row] > 0)) if mod == "a" else np.isfinite(C[rt])
                    km[j] = False; rec["n_kontrol"] = int(km.sum())
                    for mm in olcu:
                        v = M[mm][row, km]; v = v[np.isfinite(v)]
                        rec[f"k_{mm}"] = float(v.mean()) if len(v) else np.nan
            sat.append(rec)
    return pd.DataFrame(sat)


def _th_oran(x: Any) -> Tuple[float, int]:
    x = pd.to_numeric(pd.Series(x), errors="coerce").dropna()
    return (float(x.mean()) if len(x) else np.nan), int(len(x))


def _th_kat(o: float, k: float) -> float:
    if not (np.isfinite(o) and np.isfinite(k)):
        return np.nan
    if k > 0:
        return o / k
    return np.inf if o > 0 else np.nan


def th_ozet(Ev: pd.DataFrame, kontrol: bool = True, E: Optional[Dict[str, Any]] = None, boot: bool = True) -> Dict[str, Any]:
    """Bir hücrenin bütün ölçüleri (olasılık tablosu satırı)."""
    E = E or TH_ESIK
    if not len(Ev):
        return {"n_olay": 0, "n": 0, "n_fark": 0}
    A = Ev[Ev.durum == "tamam"]; W = A[A.r60.notna()] if "r60" in A else A.iloc[:0]
    o: Dict[str, Any] = {"n_olay": int(len(Ev)), "n_giris": int(len(A)), "n_alinamaz": int((Ev.durum == "alinamaz (kilitli)").sum()),
                         "n_giris_yok": int(Ev.durum.str.startswith("giris yok").sum()), "n": int(len(W)), "n_hisse": int(W.sembol.nunique()),
                         "n_kirikli": int(pd.to_numeric(A.get("kir60"), errors="coerce").fillna(0).astype(bool).sum()) if "kir60" in A else 0,
                         "dolum_belirsiz_pay": float(W.dolum_belirsiz.mean()) if len(W) else np.nan}
    for h in E["olcu"]["ufuk"]:
        o[f"r{h}"] = _q(A[f"r{h}"]) if f"r{h}" in A else _q(pd.Series(dtype=float))
    x = pd.to_numeric(W.r60, errors="coerce").dropna().sort_values() if len(W) else pd.Series(dtype=float)
    o["r60_p10"] = float(x.quantile(0.10)) if len(x) else np.nan
    o["r60_kotu10_ort"] = float(x.iloc[:max(1, int(np.ceil(0.10 * len(x))))].mean()) if len(x) else np.nan
    for m in [d[0] for d in E["olcu"]["dok"]] + ["y_up", "y_dn", "y_ayni", "y_yok"]:
        o[m], o[f"n_{m}"] = _th_oran(A[m]) if m in A else (np.nan, 0)
    if kontrol and "k_r60" in W:
        F = W[W.k_r60.notna()]; fark = (F.r60 - F.k_r60).to_numpy(float); gg = F.sembol.to_numpy()
        o["n_fark"] = int(len(F)); o["kontrolsuz"] = int(len(W) - len(F)); o["n_kontrol_medyan"] = float(F.n_kontrol.median()) if len(F) else np.nan
        o["fark_med"] = float(np.median(fark)) if len(fark) else np.nan; o["fark_ort"] = float(np.mean(fark)) if len(fark) else np.nan
        o["fark_med_ci"] = ts_boot(fark, gg, np.median, E) if boot else [np.nan, np.nan]
        o["fark_ort_ci"] = ts_boot(fark, gg, np.mean, E) if boot else [np.nan, np.nan]
        o["k_r60_med"] = float(F.k_r60.median()) if len(F) else np.nan; o["k_r60_ort"] = float(F.k_r60.mean()) if len(F) else np.nan
        for m in [d[0] for d in E["olcu"]["dok"]] + ["y_up", "y_dn"]:
            Fm = A[A[f"k_{m}"].notna() & A[m].notna()]
            o[f"o_{m}"] = float(Fm[m].mean()) if len(Fm) else np.nan; o[f"k_{m}"] = float(Fm[f"k_{m}"].mean()) if len(Fm) else np.nan
            o[f"n_e_{m}"] = int(len(Fm)); o[f"kat_{m}"] = _th_kat(o[f"o_{m}"], o[f"k_{m}"])
        o["donem"] = {}
        for dn in [x for x in E["donem_kirilim"] if x != "tanim"]:
            Fd = F[F.donem == dn]; fd = (Fd.r60 - Fd.k_r60).to_numpy(float); Ad = A[A.donem == dn]
            o["donem"][dn] = {"n": int(len(Fd)), "fark_med": float(np.median(fd)) if len(fd) else np.nan,
                              "r60_med": float(Fd.r60.median()) if len(Fd) else np.nan,
                              "up61_20": _th_oran(Ad.up61_20)[0], "k_up61_20": _th_oran(Ad.k_up61_20)[0],
                              "dn50_60": _th_oran(Ad.dn50_60)[0], "k_dn50_60": _th_oran(Ad.k_dn50_60)[0]}
    else:
        o["n_fark"] = 0
    return o


def th_karar(o: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Önceden yazılı karar cümlesi (TH_ESIK['karar']); tutmayan şartlar listelenir."""
    Kr = (E or TH_ESIK)["karar"]; n = int(o.get("n_fark", 0) or 0)
    if n < Kr["n_min"]:
        return {"karar": "KANIT YOK (örneklem yetersiz)", "sartlar": {"n>=30": False}, "tutmayan": [f"n = {n} < {Kr['n_min']}"]}
    yon = [d["fark_med"] > 0 for d in o["donem"].values() if d["n"] >= Kr["donem_n_min"] and np.isfinite(d["fark_med"])]
    o61, k61 = o.get("o_up61_20", np.nan), o.get("k_up61_20", np.nan); o50, k50 = o.get("o_dn50_60", np.nan), o.get("k_dn50_60", np.nan)
    p61 = bool(np.isfinite(o61) and np.isfinite(k61) and ((o61 >= Kr["p61_kat"] * k61) if k61 > 0 else o61 > 0))
    p50 = bool(np.isfinite(o50) and np.isfinite(k50) and ((o50 <= Kr["p50_kat"] * k50) if k50 > 0 else o50 == 0))
    ci = o.get("fark_med_ci") or [np.nan, np.nan]
    s = {"n>=30": True, "medyan_fark>0": bool(o["fark_med"] > 0), "alt_uc>0": bool(ci[0] is not None and np.isfinite(ci[0]) and ci[0] > 0),
         "P61>=1,5xkontrol": p61, "P50<=1,2xkontrol": p50, "donem>=2": bool(sum(yon) >= Kr["donem_min"])}
    return {"karar": "İZ ADAYI (BIST)" if all(s.values()) else "KANIT YOK", "sartlar": s, "tutmayan": [k for k, v in s.items() if not v],
            "donem_pozitif": int(sum(yon)), "donem_olculen": len(yon)}


def th_hucreler(E: Optional[Dict[str, Any]] = None) -> List[Tuple[str, float, float, str]]:
    """Ölçülecek bütün hücreler (ana önce): H1 / H1b / H2 x derinlik x kat x giriş."""
    E = E or TH_ESIK; es = [E["cokmus"]["esik"]] + list(E["cokmus"]["duyarlilik"]); ks = [E["hacim"]["kat"]] + list(E["hacim"]["duyarlilik"])
    return [(h, e, k, m) for h in ("H1", "H2", "H1b") for e in es for k in ks for m in ("a", "b")]


def th_anahtar(h: str, e: float, k: float, m: str) -> str:
    return f"{h}|{e:.2f}|{k:g}|{m}"


def th_h3(P: Dict[str, Any], M3: Dict[str, np.ndarray], E: Optional[Dict[str, Any]] = None, bas: Optional[str] = None,
          bit: Optional[str] = None) -> pd.DataFrame:
    """H3: hisse-ay satırları (ayın ilk kendi işlem günü; derinlik aynı gün; ekran fiyatı) + giriş C_t'den ölçüler."""
    E = E or TH_ESIK; ix = {t: i for i, t in enumerate(P["takvim"])}; b0 = pd.Timestamp(bas or E["donem"][0]); b1 = pd.Timestamp(bit or E["donem"][1])
    ad = [k for k in M3 if k.startswith(("r", "dn", "up", "dip"))]; sat = []
    for j, s in enumerate(P["sym"]):
        Y = P["Y"][s]; Y = Y[(Y.index >= b0) & (Y.index <= b1)]
        if not len(Y):
            continue
        ilk = Y[~Y.index.to_period("M").duplicated()]
        for t, y in ilk.iterrows():
            if not np.isfinite(y.der):
                continue
            row = ix.get(t)
            if row is None:
                continue
            rec = {"sembol": s, "t": t, "ekran": float(y.ekran), "derinlik": float(y.der), "cokmus": bool(y.der <= E["cokmus"]["esik"]),
                   "donem": ts_donem(t, {"donem": E["donem_kirilim"]})}
            for k in ad:
                rec[k] = float(M3[k][row, j])
            sat.append(rec)
    D = pd.DataFrame(sat)
    if len(D):
        D["kova"] = [th_h3_kova(p, E) for p in D.ekran]
    return D


def th_h3_kova(p: float, E: Optional[Dict[str, Any]] = None) -> str:
    for a, b in (E or TH_ESIK)["h3"]["kova"]:
        if p >= a and (b is None or p < b):
            return f"{_f(a, 0)}+ TL" if b is None else f"{_f(a, 0)}-{_f(b, 0)} TL"
    return "—"


def th_h3_ozet(D: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """H3 özet: fiyat kovalarına göre (çökmüş), < 1 TL / < 2 TL / >= 2 TL toplamları, çökmemiş < 2 TL (BİLGİ), dönem kırılımı."""
    E = E or TH_ESIK; out: Dict[str, Any] = {"kova": {}, "toplam": {}, "donem": {}}

    def oz(X: pd.DataFrame) -> Dict[str, Any]:
        r: Dict[str, Any] = {"n": int(len(X)), "n_hisse": int(X.sembol.nunique()) if len(X) else 0}
        for h in E["h3"]["ufuk"]:
            x = X[f"dn50_{h}"].dropna() if len(X) else pd.Series(dtype=float); r[f"dn50_{h}"] = float(x.mean()) if len(x) else np.nan
            r[f"n_dn50_{h}"] = int(len(x))
        x = X.dropna(subset=["dn50_120"]) if len(X) else X
        r["dn50_120_ci"] = ts_boot(x.dn50_120.to_numpy(float), x.sembol.to_numpy(), np.mean, E) if len(x) > 1 else [np.nan, np.nan]
        dp = X.dip250.dropna() if len(X) else pd.Series(dtype=float)
        r["dip250"] = {"n": int(len(dp)), "med": float(dp.median()) if len(dp) else np.nan, "p10": float(dp.quantile(0.1)) if len(dp) else np.nan,
                       "p25": float(dp.quantile(0.25)) if len(dp) else np.nan, "p75": float(dp.quantile(0.75)) if len(dp) else np.nan}
        u = X.up100_250.dropna() if len(X) else pd.Series(dtype=float); r["up100_250"] = float(u.mean()) if len(u) else np.nan
        q = X.r250.dropna() if len(X) else pd.Series(dtype=float); r["r250_med"] = float(q.median()) if len(q) else np.nan
        return r
    if not len(D):
        return out
    Cc = D[D.cokmus]
    for kv in [th_h3_kova(a, E) for a, _ in E["h3"]["kova"]]:
        out["kova"][kv] = oz(Cc[Cc.kova == kv])
    out["toplam"] = {"çökmüş < 1 TL": oz(Cc[Cc.ekran < 1]), "çökmüş < 2 TL": oz(Cc[Cc.ekran < 2]), "çökmüş >= 2 TL": oz(Cc[Cc.ekran >= 2]),
                     "çökmemiş < 2 TL (BİLGİ)": oz(D[~D.cokmus & (D.ekran < 2)]), "bütün hisse-aylar (BİLGİ)": oz(D)}
    for dn in [x for x in E["donem_kirilim"] if x != "tanim"]:
        a = Cc[(Cc.donem == dn) & (Cc.ekran < 2)].dn50_120.dropna(); b = Cc[(Cc.donem == dn) & (Cc.ekran >= 2)].dn50_120.dropna()
        out["donem"][dn] = {"lt2_n": int(len(a)), "lt2_dn50_120": float(a.mean()) if len(a) else np.nan,
                            "ge2_n": int(len(b)), "ge2_dn50_120": float(b.mean()) if len(b) else np.nan}
    return out


def th_izlenen(P: Dict[str, Any], E: Optional[Dict[str, Any]] = None, son_n: int = 10, gun_ici: bool = False) -> Dict[str, Any]:
    """İzlenen hisselerin son barları: tarih, ekran, getiri, tavan / kilitli, hacim oranı, önceki derinlik, H1 / H2 koşulları (tekil kuralı yok)."""
    E = E or TH_ESIK; out: Dict[str, Any] = {}; e0 = E["cokmus"]["esik"]; k0 = E["hacim"]["kat"]; g2 = E["hip"]["H2"]["getiri"]
    son = max(P["Y"][s].index[-1] for s in P["sym"])
    for s in TH_IZLE:
        Y = P["Y"].get(s)
        if Y is None:
            out[s] = "veri yok"; continue
        sat = []
        for t, y in Y.iloc[-son_n:].iterrows():
            c = bool(np.isfinite(y.DO) and y.DO <= e0 and np.isfinite(y.HO) and y.HO >= k0)
            sat.append({"t": t, "ekran": y.ekran, "r": y.r, "tavan": bool(y.tavan), "kilitli": bool(y.kilitli), "hacim_oran": y.HO, "derinlik": y.DO,
                        "H1": bool(c and y.tavan), "H2": bool(c and g2[0] <= y.r <= g2[1]), "gun_ici": bool(gun_ici and t == son)})
        out[s] = sat
    return out


def th_bilgi(S: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Fon krizi sonrası (Eylül 2026 - son bar) H1 / H2 ana tanım olayları (giriş a, kontrol yok) + izlenen hisseler. Karara girmez."""
    E = E or TH_ESIK; son = max(d.index[-1] for d in S.values()); gi = ts_gun_ici(son)
    P = th_panel(S, kes=None, E=E); o = E["olcu"]
    M = th_olcu_panelleri(P, "a", o["ufuk"], o["dok"], o["yaris"])
    H = P["H"].to_numpy(float); L = P["L"].to_numpy(float); Cf = P["Cf"].to_numpy(float); sj = {s: j for j, s in enumerate(P["sym"])}
    parca = []
    for hip in ("H1", "H2"):
        Ev = th_olaylar(P, hip, E["cokmus"]["esik"], E["hacim"]["kat"], "a", E["bilgi_bas"], None, M, False, E)
        if not len(Ev):
            continue
        for c in ("son_getiri", "en_yuksek", "en_dusuk", "gun"):
            Ev[c] = np.nan
        for i, r in Ev[Ev.durum == "tamam"].iterrows():
            j = sj[r.sembol]; rw = int(r.row)
            Ev.loc[i, "son_getiri"] = Cf[-1, j] / r.giris - 1; Ev.loc[i, "en_yuksek"] = np.nanmax(H[rw:, j]) / r.giris - 1
            Ev.loc[i, "en_dusuk"] = np.nanmin(L[rw:, j]) / r.giris - 1; Ev.loc[i, "gun"] = len(P["takvim"]) - rw
        Ev["t_gun_ici"] = [bool(gi and t == son) for t in Ev.t]
        parca.append(Ev)
    B = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame()
    return {"son_bar": str(son.date()), "gun_ici": bool(gi), "izlenen": th_izlenen(P, E, gun_ici=gi)}, B


def th_grafik(Ev: pd.DataFrame, S: Dict[str, pd.DataFrame], E: Optional[Dict[str, Any]] = None, klasor: Optional[str] = None) -> List[str]:
    """H1 ana (giriş a) olaylarından iyi (r60 > 0) ve kötü (r60 <= 0) gruplardan tohumlu rastgele 3'er grafik (PNG, repoya girmez)."""
    E = E or TH_ESIK; G = E["grafik"]; klasor = klasor or os.path.join(TS_YOL["is"], TH_DOSYA["grafik"])
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as ex:
        tslog.warning("matplotlib yok (%s); grafik çizilmedi", ex); return []
    os.makedirs(klasor, exist_ok=True)
    W = Ev[(Ev.durum == "tamam") & Ev.r60.notna()].sort_values(["sembol", "t"]).reset_index(drop=True)
    rng = np.random.default_rng(int(G["tohum"])); yollar = []
    for grup, Wg in (("iyi", W[W.r60 > 0]), ("kotu", W[W.r60 <= 0])):
        if not len(Wg):
            continue
        sec = sorted(rng.choice(len(Wg), size=min(int(G["adet"]), len(Wg)), replace=False))
        for n_, k in enumerate(sec, 1):
            r = Wg.iloc[k]; d = S[r.sembol]; i = d.index.get_loc(r.t); a = max(0, i - int(G["once"])); b = min(len(d), i + int(G["sonra"]) + 2)
            x = d.iloc[a:b]; car = x["carpan"]; xs = np.arange(len(x)); it = i - a
            try:
                fig, (ax, av) = plt.subplots(2, 1, figsize=(10, 6.2), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
                ax.vlines(xs, x.l * car, x.h * car, color="#9aa3ad", lw=1.0)
                ax.plot(xs, x.c * car, color="#1f4e79", lw=1.6, label="kapanış (ekran fiyatı)")
                ax.axvline(it, color="#c0392b", lw=1.2, ls="--", label="olay günü (hacim barı)")
                gx = r.giris_ekran
                for yv, ls, lab in ((gx, "-", "giriş (ertesi gün açılış)"), (gx * 1.61, ":", "+%61 (5 tavan)"), (gx * 0.5, ":", "-%50")):
                    ax.axhline(yv, color="#555555", lw=0.9, ls=ls, label=lab)
                if it + 60 < len(x):
                    ax.axvline(it + 60, color="#888888", lw=0.8, ls="-.", label="60. gün")
                ax.set_ylabel("TL"); ax.grid(alpha=0.25); ax.legend(loc="upper right", fontsize=8, frameon=False)
                ax.set_title(f"{r.sembol}  {pd.Timestamp(r.t).date()}  hacim {r.hacim_oran:.0f}x  derinlik {100 * r.derinlik:.0f}%  "
                             f"60 gün {100 * r.r60:+.0f}%  ({'iyi giden' if grup == 'iyi' else 'kötü giden'})", fontsize=11)
                av.bar(xs, x.v, color=np.where(xs == it, "#c0392b", "#7f8c8d"), width=0.8)
                av.set_ylabel("hacim (adet)"); av.grid(alpha=0.25)
                tick = list(range(0, len(x), 20)); av.set_xticks(tick); av.set_xticklabels([str(x.index[t].date()) for t in tick], rotation=30, fontsize=8)
                fig.tight_layout()
                y = os.path.join(klasor, f"H1_{grup}_{n_}_{r.sembol}_{pd.Timestamp(r.t).date()}.png"); fig.savefig(y, dpi=110); plt.close(fig)
                yollar.append(y)
            except (ValueError, KeyError, IndexError, TypeError) as ex:
                tslog.warning("grafik çizilemedi %s (%s)", r.sembol, ex)
    return yollar


def th_sayim(P: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Ön kayıt için yalnız tanım sayımı (sonuç yok): hücre başına olay sayısı (giriş durumu dahil), H3 hisse-ay sayıları."""
    E = E or TH_ESIK; out: Dict[str, Any] = {"hisse": len(P["sym"]), "takvim": [str(P["takvim"][0].date()), str(P["takvim"][-1].date())], "hucre": {}}
    for h, e, k, m in th_hucreler(E):
        Ev = th_olaylar(P, h, e, k, m, E["donem"][0], E["donem"][1], None, False, E)
        out["hucre"][th_anahtar(h, e, k, m)] = {"olay": int(len(Ev)), "giris": int((Ev.durum == "tamam").sum()) if len(Ev) else 0,
                                                "hisse": int(Ev.sembol.nunique()) if len(Ev) else 0}
    return out


def th_onkayit_metin(zaman: str, sayim: Dict[str, Any], K: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or TH_ESIK; a = sayim["hucre"]; an = E["karar"]["ana"]; ik = E["karar"]["ikincil"]
    return "\n".join([
        "# TAVAN SERİSİ / HACİM ÖN KAYDI (ölçümden önce)", "",
        f"{TH_SURUM}. Yazılma {zaman}. Bu dosya git'e işlenmeden `python TAVAN_SERISI.py hacim kos` çalışmaz (mühür kapısı).", "",
        "## Soru (Cemal, 13 Kasım 2026)", "",
        "'Hepsi kumar değil. TEHOL'de devasa hacimli bir alım barı var; 1 liradaki hisseyi böyle hacim zıplatır; 1 liradan daha nereye düşer; 5 tavan = %61.' "
        "H1: çökmüş hissede devasa hacimli tavan barından sonra katılmak, aynı gün aynı derinlikte hacimsiz çökmüşlerden iyi mi? H2: dipte tavansız "
        "devasa hacim (birikim) aynı soruda. H3: 1 / 2 TL altındaki çökmüş hisse sonraki 60 / 120 / 250 günde yine de -%50'ye düşüyor mu?", "",
        "## Tanımlar ve eşikler (TH_ESIK, değişmez)", "",
        "```json", json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
        "Yeniden kullanılan TAVAN_SERISI tanımları (mühre dahil): tavan " + json.dumps(TS_ESIK["tavan"]["rejim"]) + ", kontrol kovaları "
        + json.dumps(TS_ESIK["kontrol"]["kova"]) + ", fiyat adımları " + json.dumps(TS_ADIM) + ".", "",
        "## Karar cümlesi (önceden yazılı)", "", E["karar"]["metin"], "",
        "Ölçülecekler (her hücre): n (hisse), P(20 günde +%61'e dokunma), P(60 günde +%100), P(60 günde -%50), önce +%50 mi önce -%25 mi (60 gün), 5 / 20 / "
        "60 gün getiri medyan ve ortalama, en kötü %10, kontrol ve fark (hisse kümeli bootstrap %95), dönem kırılımı 2016-19 / 2020-22 / 2023-26.08. "
        "Fon krizi sonrası olaylar ayrı BİLGİ tablosu. Grafik: H1 ana tanımdan iyi / kötü gruplarından tohumlu 3'er örnek.", "",
        "## Veri ve tanım sayımı (sonuç içermez)", "",
        f"- Fiyat: {K['okunan']} hisse okundu, {len(K['eksik'])} eksik; son tarih {K['son_tarih']}; manifest sha256 {K['manifest_sha256']}.",
        f"- Test paneli (kesik {E['kriz']}): {sayim['hisse']} hisse, takvim {sayim['takvim'][0]} - {sayim['takvim'][1]}.",
        f"- ANA hücre {an}: {a[an]['olay']} olay ({a[an]['hisse']} hisse), girişi olan {a[an]['giris']}. İKİNCİL {ik}: {a[ik]['olay']} olay "
        f"({a[ik]['hisse']} hisse), girişi olan {a[ik]['giris']}.",
        "- Bütün hücreler (olay / girişi olan / hisse): " + "; ".join(f"{k}: {v['olay']} / {v['giris']} / {v['hisse']}" for k, v in a.items()) + ".", "",
        "## Ön kayıttan önce görülenler (sonuç değil)", "",
        "- TAVAN_RAPOR.md (aynı gün, ön kayıtlı): çökmüş hissede 1. tavandan sonra katılmak kontrolden iyi değil (k=1 KUMAR), k >= 2 örneklem az. Hacim "
        "koşulu o ölçümde yoktu.",
        "- İzlenen altı hissenin (TEHOL, PEKGY, IEYHO, DSTKF, OZATD, TRHOL) son 10 barının getiri / hacim oranı / derinliği (tanım denetimi; ör. TEHOL "
        "05.11.2026 hacim oranı ~4.300x, 09.11.2026 tavan + ~580x). Kilitli taban dizisinden çıkışta 20 gün medyan hacmi çok küçük olduğundan oranlar "
        "yüzlerce / binlerce kat çıkabiliyor: tanım bu hâliyle ölçülür, eşik değişmez.",
        "- Yahoo hacminin bölünme düzeltmeli olduğu (bölünme günlerinde 20 gün medyan hacim oranı ~1; ör. AEFES 10:1 2025-06-26: 0,91) denetlendi.",
        "- Olay sayıları (yukarıda). Getiri, dokunma oranı, kontrol farkı görülmedi.", "",
        "## Bilinen yanlılıklar", "", E["yanlilik"], "",
        f"ESIK_SHA256: {th_esik_sha(E)}",
        f"KOD_SHA256: {ts_kod_sha()}",
        f"VERI_MANIFEST_SHA256: {K['manifest_sha256']}", ""])


def th_onkayit(kl: Optional[str] = None) -> str:
    y = _th_yol("onkayit", kl)
    if os.path.exists(y):
        raise TsHata(f"hacim ön kaydı zaten var, üzerine yazılmaz: {y}")
    S, K = ts_fiyatlar(); P = th_panel(S, kes=TH_ESIK["kriz"])
    return _ts_yaz(y, th_onkayit_metin(_ts_simdi(), th_sayim(P), K))


def th_kapi(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
            manifest: Optional[str] = None) -> Dict[str, Any]:
    """Hacim ön kayıt mühür kapısı: ön kayıt var + git'e işlenmiş ve değişmemiş + eşik mührü + veri manifesti + kod sha256 (ya da sapma gerekçesi)."""
    E = E or TH_ESIK; y = _th_yol("onkayit", kl)
    if not os.path.exists(y):
        raise TsHata("hacim ön kaydı yok: önce `python TAVAN_SERISI.py hacim onkayit` ve commit")
    O = ts_onkayit_oku(y); out: Dict[str, Any] = {"onkayit": y}
    if git:
        out["onkayit_git"] = ts_git_durum(y)
    if O["ESIK_SHA256"] != th_esik_sha(E):
        raise TsHata("hacim eşik mührü tutmuyor (TH_ESIK ön kayıttan sonra değişmiş)")
    if manifest is not None and O["VERI_MANIFEST_SHA256"] != manifest:
        raise TsHata("veri manifesti hacim ön kaydındakiyle aynı değil (fiyat önbelleği değişmiş)")
    ks = ts_kod_sha(); out["kod_sha256"] = ks; out["kod_ayni"] = ks == O["KOD_SHA256"]
    if not out["kod_ayni"]:
        if not sapma:
            raise TsHata("TAVAN_SERISI.py hacim ön kaydından sonra değişmiş: yalnız `--sapma GEREKCE` ile koşar (gerekçe sonuca yazılır)")
        out["sapma"] = sapma
    out["esik_sha256"] = O["ESIK_SHA256"]
    return out


def th_kos(kl: Optional[str] = None, git: bool = True, sapma: Optional[str] = None, E: Optional[Dict[str, Any]] = None,
           S: Optional[Dict[str, pd.DataFrame]] = None, K: Optional[Dict[str, Any]] = None, grafik: bool = True) -> Dict[str, Any]:
    """Hacim ölçümü uçtan uca: kapı -> H1 / H1b / H2 hücreleri -> H3 -> kriz sonrası BİLGİ -> grafik -> JSON + rapor."""
    E = E or TH_ESIK
    if S is None:
        S, K = ts_fiyatlar()
    Kp = th_kapi(kl, git, sapma, E, manifest=(K or {}).get("manifest_sha256"))
    t0 = _ts_simdi(); tslog.info("hacim kapısı geçti (mühür %s)", Kp["esik_sha256"][:12])
    P = th_panel(S, kes=E["kriz"], E=E); o = E["olcu"]
    M = {m: th_olcu_panelleri(P, m, o["ufuk"], o["dok"], o["yaris"]) for m in ("a", "b")}
    sonuc: Dict[str, Any] = {"surum": TH_SURUM, "baslangic": t0, "kapi": Kp, "kapsam": {k: v for k, v in (K or {}).items() if k != "eksik"},
                             "hucre": {}, "karar": {}}
    parca = []
    for h, e, k, m in th_hucreler(E):
        an = th_anahtar(h, e, k, m)
        Ev = th_olaylar(P, h, e, k, m, E["donem"][0], E["donem"][1], M[m], True, E)
        oz = th_ozet(Ev, True, E); oz["kural"] = th_karar(oz, E); sonuc["hucre"][an] = oz
        if len(Ev):
            parca.append(Ev.assign(hucre=an))
        tslog.info("%s: olay %d, n %d, fark n %d -> %s", an, oz.get("n_olay", 0), oz.get("n", 0), oz.get("n_fark", 0), oz["kural"]["karar"])
    Kr = E["karar"]
    sonuc["karar"] = {"H1_ana": {"hucre": Kr["ana"], **sonuc["hucre"][Kr["ana"]]["kural"]},
                      "H2_ikincil": {"hucre": Kr["ikincil"], **sonuc["hucre"][Kr["ikincil"]]["kural"]},
                      "gecen_hucre": sorted(a for a, v in sonuc["hucre"].items() if v["kural"]["karar"].startswith("İZ")),
                      "olculen_hucre": int(sum(1 for v in sonuc["hucre"].values() if v.get("n_fark", 0) >= Kr["n_min"])), "hucre_sayisi": len(sonuc["hucre"])}
    EvT = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame()
    # H3
    M3 = th_olcu_panelleri(P, "b", E["h3"]["ufuk"], [[f"dn50_{h}", h, -0.5] for h in E["h3"]["ufuk"]] + [["up100_250", 250, 1.0]], None, [250])
    D3 = th_h3(P, M3, E); sonuc["h3"] = th_h3_ozet(D3, E)
    tslog.info("H3: %d hisse-ay (%d çökmüş)", len(D3), int(D3.cokmus.sum()) if len(D3) else 0)
    # BİLGİ: kriz sonrası
    bi, B = th_bilgi(S, E); sonuc["bilgi"] = bi
    sonuc["bilgi"]["olay"] = [{k: r.get(k) for k in ("hip", "sembol", "t", "t_gun_ici", "derinlik", "hacim_oran", "r_t", "kilitli_t", "ekran_t", "durum",
                                                      "e", "giris_ekran", "dolum_belirsiz", "r5", "r20", "r60", "up61_20", "dn50_60", "son_getiri",
                                                      "en_yuksek", "en_dusuk", "gun")} for r in B.to_dict("records")] if len(B) else []
    # grafik
    ana = EvT[EvT.hucre == Kr["ana"]] if len(EvT) else EvT
    sonuc["grafik"] = th_grafik(ana, S, E) if grafik and len(ana) else []
    sonuc["bitis"] = _ts_simdi()
    os.makedirs(TS_YOL["is"], exist_ok=True)
    if len(EvT):
        EvT.to_csv(os.path.join(TS_YOL["is"], TH_DOSYA["olay"]), index=False)
    if len(B):
        B.to_csv(os.path.join(TS_YOL["is"], TH_DOSYA["bilgi"]), index=False)
    if len(D3):
        D3.to_csv(os.path.join(TS_YOL["is"], TH_DOSYA["h3"]), index=False)
    _ts_json(_th_yol("sonuc", kl), sonuc); _ts_yaz(_th_yol("rapor", kl), th_rapor_md(_ts_kayit(sonuc), E))
    return sonuc


def _th_ok(o: Any, k: str) -> str:
    """Oran hücresi: bütün olaylarda oran (kontrolü olan olaylarda eşleşik olay / kontrol)."""
    return f"{_y(_g(o, k))} ({_y(_g(o, 'o_' + k))} / {_y(_g(o, 'k_' + k))})"


def th_rapor_md(S: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> str:
    """Tek sayfa düz Türkçe rapor (sonuç JSON'undan)."""
    E = E or TH_ESIK; Hc = S.get("hucre", {}); Kr = S.get("karar", {}); kap = S.get("kapi", {}); an = E["karar"]["ana"]; ik = E["karar"]["ikincil"]
    A = Hc.get(an, {}); I = Hc.get(ik, {}); ka = Kr.get("H1_ana", {}); ki = Kr.get("H2_ikincil", {})

    def kural(o: Dict[str, Any]) -> str:
        k = o.get("kural", {})
        return k.get("karar", "—") + (f" (tutmayan: {', '.join(k.get('tutmayan', []))})" if k.get("tutmayan") else "")

    def satir(ad: str, o: Dict[str, Any]) -> str:
        if not o or not o.get("n_olay"):
            return f"| {ad} | 0 | — | — | — | — | — | — | — | — | olay yok |"
        return (f"| {ad} | {o['n']} ({o['n_hisse']}) | {_th_ok(o, 'up61_20')} | {_th_ok(o, 'up100_60')} | {_th_ok(o, 'dn50_60')} | "
                f"{_y(o.get('y_up'))} / {_y(o.get('y_dn'))} | {_y(_g(o, 'r60', 'med'))} ({_y(_g(o, 'r60', 'ort'))}) | {_y(o.get('r60_p10'))} | "
                f"{_y(o.get('k_r60_med'))} | {_y(o.get('fark_med'), 1)} {_ar(o.get('fark_med_ci'))} | {kural(o)} |")
    bas = ("| tanım | n (hisse) | +%61 / 20g: olay (eşleşik olay / kontrol) | +%100 / 60g: olay (eş. olay / kontrol) | -%50 / 60g: olay (eş. olay / "
           "kontrol) | önce +%50 / önce -%25 | "
           "60g medyan (ort.) | en kötü %10 (60g) | kontrol 60g medyan | medyan fark [%95] | kural |")
    ayr = "|---|---|---|---|---|---|---|---|---|---|---|"
    L = ["# Çökmüş hissede devasa hacim barı: Cemal'in hipotezleri (BIST 2016 - Ağu 2026)", "",
         f"Ön kayıt {str(_g(kap, 'onkayit_git', 'commit') or '—')[:7]} ({_g(kap, 'onkayit_git', 'commit_zamani') or '—'}), mühür "
         f"{str(kap.get('esik_sha256', '—'))[:12]}" + (f"; SAPMA: {kap.get('sapma')}" if kap.get("sapma") else "") + ".", "",
         "## Sonuç", "",
         f"**H1 (çökmüş -%80 + hacim >= 10x + tavan, ertesi gün açılış): {ka.get('karar', '—')}**"
         + (f" (tutmayan şart: {', '.join(ka.get('tutmayan', []))})" if ka.get("tutmayan") else "") + ". "
         f"H2 (dipte tavansız hacim, ikincil): {ki.get('karar', '—')}" + (f" (tutmayan: {', '.join(ki.get('tutmayan', []))})" if ki.get("tutmayan") else "")
         + f". BİLGİ hücrelerinden kuralı geçen: {', '.join(Kr.get('gecen_hucre', [])) or 'yok'} ({Kr.get('hucre_sayisi', 0)} hücre ölçüldü; "
         f"n >= 30 olan {Kr.get('olculen_hucre', 0)}, bunlardan medyan farkın %95 aralığı tamamen 0'ın altında olan "
         f"{sum(1 for v in Hc.values() if v.get('n_fark', 0) >= E['karar']['n_min'] and (v.get('fark_med_ci') or [None, None])[1] is not None and v['fark_med_ci'][1] < 0)}, "
         f"tamamen 0'ın üstünde olan "
         f"{sum(1 for v in Hc.values() if v.get('n_fark', 0) >= E['karar']['n_min'] and (v.get('fark_med_ci') or [None, None])[0] is not None and v['fark_med_ci'][0] > 0)}).",
         "", "Düz dille:"]
    if A.get("n"):
        L += [f"- Çökmüş hissede hacmi 20 günlük medyanın 10 katı olan tavan günü ({A['n']} olay, {A['n_hisse']} hisse; aynı gün kontrolü olan "
              f"{A.get('n_fark', 0)}), ertesi gün açılıştan alan: 20 günde +%61'e (Cemal'in 5 tavanı) ulaşan {_y(A.get('up61_20'))}; 60 günde +%100 "
              f"{_y(A.get('up100_60'))}; 60 günde -%50 {_y(A.get('dn50_60'))}; 60 gün medyan getiri {_y(_g(A, 'r60', 'med'))}; önce +%50 mi önce -%25 mi: "
              f"{_y(A.get('y_up'))} / {_y(A.get('y_dn'))}. Kontrolü olan olaylarda medyan fark {_y(A.get('fark_med'), 1)} {_ar(A.get('fark_med_ci'))}: "
              "örneklem karar için çok küçük."]
    gen = sorted([(v.get("n_fark", 0), a) for a, v in Hc.items() if a.startswith("H1|") and a.endswith("|a")], reverse=True)
    if gen and gen[0][0]:
        g_ = Hc[gen[0][1]]; h_, e_, k_, _m = gen[0][1].split("|")
        L += [f"- En geniş H1 hücresi (BİLGİ: derinlik {_y(float(e_))}, hacim >= {k_}x, tavan; {g_['n']} olay, {g_['n_hisse']} hisse): 20 günde +%61 "
              f"{_y(g_.get('o_up61_20'))}, kontrol {_y(g_.get('k_up61_20'))} (kat {_f(g_.get('kat_up61_20'))}); 60 günde -%50 {_y(g_.get('o_dn50_60'))}, "
              f"kontrol {_y(g_.get('k_dn50_60'))}; 60 gün medyan {_y(_g(g_, 'r60', 'med'))}, kontrol {_y(g_.get('k_r60_med'))}; medyan fark "
              f"{_y(g_.get('fark_med'), 1)} {_ar(g_.get('fark_med_ci'))}. Yani hacimli tavan büyük sıçrama biletini artırıyor ama tipik sonucu "
              "hacimsiz eşlerinden kötü."]
    if I.get("n"):
        L += [f"- Dipte tavansız hacim (H2, {I['n']} olay): 60 gün medyan {_y(_g(I, 'r60', 'med'))}, kontrol {_y(I.get('k_r60_med'))}; medyan fark "
              f"{_y(I.get('fark_med'), 1)} {_ar(I.get('fark_med_ci'))}; -%50 {_y(I.get('o_dn50_60'))} (kontrol {_y(I.get('k_dn50_60'))})."]
    h3 = S.get("h3", {}).get("toplam", {})
    if h3:
        a1, a2, a3 = h3.get("çökmüş < 1 TL", {}), h3.get("çökmüş < 2 TL", {}), h3.get("çökmüş >= 2 TL", {})
        L += [f"- '1 liradan nereye düşer' (H3): çökmüş ve 1 TL altı hisse-ayların {_y(a1.get('dn50_120'))}'i sonraki 120 günde yine -%50'ye düştü "
              f"(250 günde {_y(a1.get('dn50_250'))}); 2 TL altı {_y(a2.get('dn50_120'))} / {_y(a2.get('dn50_250'))}; 2 TL ve üstü çökmüşler "
              f"{_y(a3.get('dn50_120'))} / {_y(a3.get('dn50_250'))}. 250 günde en düşük noktanın medyanı: 1 TL altı {_y(_g(a1, 'dip250', 'med'))}, "
              f"2 TL üstü {_y(_g(a3, 'dip250', 'med'))}."]
    L += ["", "## H1: devasa hacimli tavan barı (ÇÖKMÜŞ -%80, giriş ertesi gün açılış)", "", bas, ayr]
    for h, nm in (("H1", "tavan"), ("H1b", "+%5 ve üstü")):
        for k in [E["hacim"]["kat"]] + list(E["hacim"]["duyarlilik"]):
            ad = th_anahtar(h, E["cokmus"]["esik"], k, "a")
            L.append(satir(f"{h} {nm}, hacim >= {_f(k, 0)}x" + (" **ANA**" if ad == an else ""), Hc.get(ad, {})))
    L += ["", "'olay / kontrol': kontrol = aynı gün, aynı derinlik kovasında çökmüş, o gün hacmi 20 gün medyanının 3 katından az hisseler (oranlar "
          "kontrolü olan olaylarda eşleşik). Fark = olay 60g getirisi - kontrol ortalaması; aralık hisse kümeli bootstrap.", "",
          "## H1 ANA ve H2 dönemler (60g medyan fark; +%61 olay / kontrol; -%50 olay / kontrol)", "",
          "| hücre | 2016-19 | 2020-22 | 2023-26.08 | yön tutan dönem |", "|---|---|---|---|---|"]
    for ad, kk in ((an, ka), (ik, ki)):
        o = Hc.get(ad, {}); hc = []
        for dn in ("2016-19", "2020-22", "2023-26.08"):
            d = _g(o, "donem", dn) or {}
            hc.append(f"n {d.get('n', 0)}: {_y(d.get('fark_med'), 1)}; {_y(d.get('up61_20'))} / {_y(d.get('k_up61_20'))}; "
                      f"{_y(d.get('dn50_60'))} / {_y(d.get('k_dn50_60'))}")
        L.append(f"| {ad} | " + " | ".join(hc) + f" | {kk.get('donem_pozitif', '—')} / {kk.get('donem_olculen', '—')} |")
    L += ["", "## H2: dipte tavansız devasa hacim (getiri -%5..+%5; ÇÖKMÜŞ -%80, giriş ertesi gün açılış)", "", bas, ayr]
    for k in [E["hacim"]["kat"]] + list(E["hacim"]["duyarlilik"]):
        ad = th_anahtar("H2", E["cokmus"]["esik"], k, "a")
        L.append(satir(f"H2 hacim >= {_f(k, 0)}x" + (" **İKİNCİL**" if ad == ik else ""), Hc.get(ad, {})))
    L += ["", "## H3: taban fiyat ('1 liradan nereye düşer'); çökmüş hisse-ay, giriş ay başı kapanış", "",
          "| fiyat kovası | hisse-ay (hisse) | 60g'de -%50 | 120g'de -%50 [%95] | 250g'de -%50 | 250g en düşük nokta: medyan [%10, %25] | 250g'de +%100 | 250g medyan getiri |",
          "|---|---|---|---|---|---|---|---|"]
    for nm, o in list(S.get("h3", {}).get("kova", {}).items()) + list(h3.items()):
        L.append(f"| {nm} | {o.get('n', 0)} ({o.get('n_hisse', 0)}) | {_y(o.get('dn50_60'))} | {_y(o.get('dn50_120'))} {_ar(o.get('dn50_120_ci'))} | "
                 f"{_y(o.get('dn50_250'))} | {_y(_g(o, 'dip250', 'med'))} [{_y(_g(o, 'dip250', 'p10'))}, {_y(_g(o, 'dip250', 'p25'))}] | "
                 f"{_y(o.get('up100_250'))} | {_y(o.get('r250_med'))} |")
    L += ["", "H3 dönemler (çökmüş, 120g'de -%50; 2 TL altı / 2 TL ve üstü): " + "; ".join(
        f"{dn}: {_y(d.get('lt2_dn50_120'))} (n {d.get('lt2_n')}) / {_y(d.get('ge2_dn50_120'))} (n {d.get('ge2_n')})" for dn, d in S.get("h3", {}).get("donem", {}).items())
        + ". Karar yok (ön kayıt).", ""]
    B = S.get("bilgi", {})
    L += [f"## BİLGİ: fon krizi sonrası (Eylül 2026 - {B.get('son_bar', '—')}{', son bar GÜN İÇİ' if B.get('gun_ici') else ''}) H1 / H2 ana tanım olayları "
          "(karara girmez)", "",
          "| hip | sembol | olay günü | hacim oranı | derinlik | o gün | giriş (ekran) | 5g | 20g | 60g | +%61 / 20g | bugüne: son / en yüksek / en düşük (gün) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def ac(x: Any) -> str:
        return "açık" if x is None or (isinstance(x, float) and not np.isfinite(x)) else _y(x)
    for r in sorted(B.get("olay", []), key=lambda r: (str(r.get("t")), r.get("sembol"))):
        gir = (f"{_f(r.get('giris_ekran'))}" + (" (dolum belirsiz)" if r.get("dolum_belirsiz") else "")) if r.get("durum") == "tamam" else "henüz yok"
        L.append(f"| {r.get('hip')} | {r.get('sembol')} | {r.get('t')}{' (gün içi)' if r.get('t_gun_ici') else ''} | {_f(r.get('hacim_oran'), 0)}x | "
                 f"{_y(r.get('derinlik'))} | {_y(r.get('r_t'), 1)}{' kilitli' if r.get('kilitli_t') else ''} | {gir} | {ac(r.get('r5'))} | {ac(r.get('r20'))} | "
                 f"{ac(r.get('r60'))} | {ac(r.get('up61_20'))} | " + (f"{_y(r.get('son_getiri'))} / {_y(r.get('en_yuksek'))} / {_y(r.get('en_dusuk'))} "
                                                                      f"({_f(r.get('gun'), 0)})" if r.get("durum") == "tamam" else "—") + " |")
    if not B.get("olay"):
        L.append("| (yok) |  |  |  |  |  |  |  |  |  |  |  |")
    L += ["", "İzlenen hisseler, son barlar (tarih: ekran fiyatı, günlük getiri, hacim / 20g medyan; T = tavan, K = kilitli; H1 / H2 = ana tanım koşulu o gün "
          "tutuyor, 20 gün tekil kuralı uygulanmadan):", ""]
    for s, sat in B.get("izlenen", {}).items():
        if isinstance(sat, str):
            L.append(f"- {s}: {sat}"); continue
        L.append(f"- {s} (derinlik {_y(sat[-1].get('derinlik'))}): " + "; ".join(
            f"{str(x['t'])[5:]}{' gün içi' if x.get('gun_ici') else ''}: {_f(x['ekran'])}, {_y(x['r'], 1)}, {_f(x['hacim_oran'], 0)}x"
            + (" T" if x["tavan"] else "") + ("K" if x["kilitli"] else "") + (" H1" if x["H1"] else "") + (" H2" if x["H2"] else "") for x in sat))
    if S.get("grafik"):
        L += ["", "Grafikler (repoda değil): " + ", ".join(S["grafik"]) + "."]
    L += ["", "## Ek: bütün hücreler (BİLGİ; kural sonucu kararı değiştirmez)", "",
          "| hücre (hip, derinlik, kat, giriş) | olay / girişi olan / alınamaz | n (hisse) | +%61 / 20g: olay (eş. olay / kontrol) | -%50 / 60g: olay (eş. olay / "
          "kontrol) | 60g medyan | medyan fark [%95] | kural |",
          "|---|---|---|---|---|---|---|---|"]
    for ad, o in Hc.items():
        L.append(f"| {ad} | {o.get('n_olay', 0)} / {o.get('n_giris', 0)} / {o.get('n_alinamaz', 0)} | {o.get('n', 0)} ({o.get('n_hisse', 0)}) | "
                 f"{_th_ok(o, 'up61_20')} | {_th_ok(o, 'dn50_60')} | {_y(_g(o, 'r60', 'med'))} | {_y(o.get('fark_med'), 1)} {_ar(o.get('fark_med_ci'))} | "
                 f"{_g(o, 'kural', 'karar') or '—'} |")
    L += ["", "## Tanım ve sınırlar", "",
          "- ÇÖKMÜŞ: olaydan önceki gün kapanışı kendi son 250 barının en yüksek kapanışından en az %80 aşağıda (duyarlılık %70, %60). Hacim oranı: o "
          "günün hacmi / önceki 20 günün medyan hacmi. Tavan: TAVAN_SERISI tanımı (13.03.2020'den >= +%9,5, öncesi >= +%19; 1-2 TL'de fiyat adımı). "
          "Aynı hissede 20 gün içinde tek olay.",
          "- Giriş a: ertesi gün açılış (ana). Giriş b: olay günü kapanışı, olay günü kilitli tavansa alınamaz. Pencerede veri kırığı (|günlük| > %25) "
          "olan ölçü dışarıda.",
          f"- Yanlılık: {E['yanlilik']}.",
          f"- Karar cümlesi (önceden yazılı): {E['karar']['metin']}"]
    return "\n".join(L) + "\n"


def th_rapor(kl: Optional[str] = None) -> str:
    S = _ts_json_oku(_th_yol("sonuc", kl))
    return _ts_yaz(_th_yol("rapor", kl), th_rapor_md(S))


def _cakisma_kontrol_ts(_once=_CK_ONCE_TS, _dosya="TAVAN_SERISI.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_TS", "_CK_KAYIT", "_cakisma_kontrol_ts", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "re", "hashlib", "pickle", "subprocess", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "K60V", "_f", "_ar", "_g", "_q", "_y")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ts()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=TS_SURUM)
    ap.add_argument("komut", choices=["indir", "canli", "onkayit", "kos", "rapor", "hacim"])
    ap.add_argument("alt", nargs="?", default="kos", choices=["onkayit", "kos", "rapor"], help="hacim: onkayit / kos / rapor")
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--yenile", action="store_true", help="canli: son günleri ayrı klasöre yeniden indir")
    ap.add_argument("--sapma", default=None, help="kos: ön kayıttan sonra kod değiştiyse gerekçe (sonuca yazılır)")
    a_ = ap.parse_args()
    try:
        if a_.komut == "indir":
            print(json.dumps(_ts_kayit(ts_indir()), ensure_ascii=False))
        elif a_.komut == "canli":
            c_ = ts_canli(a_.yenile, kl=a_.cikti); print(c_["csv"]); print(c_["md"])
        elif a_.komut == "onkayit":
            y_ = ts_onkayit(a_.cikti); print(y_, "mühür", ts_esik_sha(), "kod", ts_kod_sha(), "dosya", ts_sha_dosya(y_))
        elif a_.komut == "kos":
            s_ = ts_kos(a_.cikti, sapma=a_.sapma)
            print(json.dumps({k: v["karar"] for k, v in s_["karar"].items()}, ensure_ascii=False)); print(_ts_yol("rapor", a_.cikti))
        elif a_.komut == "hacim":
            if a_.alt == "onkayit":
                y_ = th_onkayit(a_.cikti); print(y_, "mühür", th_esik_sha(), "kod", ts_kod_sha(), "dosya", ts_sha_dosya(y_))
            elif a_.alt == "kos":
                s_ = th_kos(a_.cikti, sapma=a_.sapma); print(json.dumps(_ts_kayit(s_["karar"]), ensure_ascii=False)); print(_th_yol("rapor", a_.cikti))
            else:
                print(th_rapor(a_.cikti))
        else:
            print(ts_rapor(a_.cikti))
    except (TsHata, K60V.K60VHata, FileNotFoundError) as ex:
        tslog.error("%s", ex); sys.exit(1)
