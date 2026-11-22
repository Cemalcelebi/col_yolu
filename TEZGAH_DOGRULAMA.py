"""TEZGAH_DOGRULAMA — TEZGÂH DOĞRULAMA: bizim tezgâhın (veri + OLCU_SINAMA nedensel paneli + portföy hesabı) ürettiği AYLIK seriler,
dışarıda yayımlanmış referans serilerle ay ay karşılaştırılır. İz ARANMAZ; yalnız doğrulama (22 Kasım 2026).

İş tanımı: arastirma_cikti/tezgah_dogrulama/TEZGAH_DOGRULAMA_IS_TANIMI.md.
Veri: hisse fiyatı YALNIZ /tmp/kasa/acik (KASA açık kesik 2023-12-31); her hesaptan önce KASA.kasa_kapisi (hisse pkl + kesilmiş referans pkl).
Referans: Kenneth French veri kütüphanesi (ABD faktör / onluk dosyaları, Avrupa faktörleri; curl, repo dışı /tmp/claude-0/tezgah_ref/);
  erişilemezse yedek Yahoo fonları (SPY, RSP, IWM, MTUM, VLUE, USMV, VGK). Referanslar 2023-12'de kesilir (sonrası atılır).
  Ek: Yahoo (yfinance) 30 büyük ABD hissesinin günlük Close / Adj Close'u ve EURUSD=X (E2 veri kipi doğrulaması; AVR USD çevirimi), 2023-12-29'a kadar.
Panel: OLCU_SINAMA (OS.os_veri, OS.os_panel, OS.os_kart_sinyal, OS.os_olcu_hesap) İÇE ALINIR, kopyalanmaz.

Komut:  python TEZGAH_DOGRULAMA.py ref       referans indir + ayrıştır + 2023-12 kesiği -> /tmp/claude-0/tezgah_ref/ (ref_kesik.pkl, yahoo_kesik.pkl, ref_durum.json)
        python TEZGAH_DOGRULAMA.py onkayit   TEZGAH_DOGRULAMA_ON_KAYIT.md (kontrol tablosu, hüküm kuralı aynen, kaynak / erişim, sha'lar)
        python TEZGAH_DOGRULAMA.py kos       kapılar (KASA, ön kayıt git + sha + kontrol) -> seriler -> karşılaştırma -> json + rapor
        python TEZGAH_DOGRULAMA.py yeniden   yalnız yeniden üretim adımı (koşu json'u üzerinde; H-TD1 SAPMA kaydıyla)
        python TEZGAH_DOGRULAMA.py rapor     TEZGAH_DOGRULAMA_RAPOR.md (json'dan)
Colab:  exec(open('TEZGAH_DOGRULAMA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_TD = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_TD = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_TD not in sys.path:
    sys.path.insert(0, KOK_TD)

import OLCU_SINAMA as OS  # noqa: E402  (nedensel panel; DEĞİŞTİRİLMEZ, yalnız çağrılır)

tdlog = logging.getLogger("col.tezgah_dogrulama")
if not tdlog.handlers:
    _td_h = logging.StreamHandler(sys.stderr)
    _td_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s tezgah_dogrulama: %(message)s", "%H:%M:%S"))
    tdlog.addHandler(_td_h)
    tdlog.setLevel(logging.INFO)
    tdlog.propagate = False

TD_SURUM = "TEZGAH_DOGRULAMA v1.0 (2026-11-22)"
TD_YOL = {"cikti": os.path.join(KOK_TD, "arastirma_cikti", "tezgah_dogrulama"), "veri": os.environ.get("TD_VERI", "/tmp/kasa/acik"),
          "ref": os.environ.get("TD_REF", "/tmp/claude-0/tezgah_ref"), "kod": os.path.join(KOK_TD, "TEZGAH_DOGRULAMA.py"),
          "is_tanimi": os.path.join(KOK_TD, "arastirma_cikti", "tezgah_dogrulama", "TEZGAH_DOGRULAMA_IS_TANIMI.md"),
          "kasa_dizin": os.environ.get("KASA_DIZIN", "/tmp/kasa"),
          "os_sinir": os.path.join(KOK_TD, "arastirma_cikti", "olcu_sinama", "os_sinir.json")}
TD_DOSYA = {"onkayit": "TEZGAH_DOGRULAMA_ON_KAYIT.md", "rapor": "TEZGAH_DOGRULAMA_RAPOR.md", "json": "tezgah_dogrulama.json",
            "ref_kesik": "ref_kesik.pkl", "yahoo_kesik": "yahoo_kesik.pkl", "ref_durum": "ref_durum.json"}

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
TD_ESIK: Dict[str, Any] = {
    "surum": "TD1.0",
    "kesik": "2023-12-31", "yahoo_son": "2023-12-29",
    "pencere": {"karsilastirma": ["2016-01", "2023-12"], "ref_eski": ["2000-01", "2015-12"], "ref_yeni": ["2016-01", "2023-12"],
                "alt": {"d1": ["2016-01", "2019-12"], "d2": ["2020-01", "2023-12"]}, "tarih": "TUTMA ayı (getirinin ölçüldüğü ay)"},
    "french": {"kok": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/",
               "dosya": ["F-F_Research_Data_Factors_CSV.zip", "F-F_Momentum_Factor_CSV.zip", "F-F_ST_Reversal_Factor_CSV.zip",
                         "10_Portfolios_Prior_12_2_CSV.zip", "10_Portfolios_Prior_1_0_CSV.zip", "Europe_3_Factors_CSV.zip",
                         "Europe_Mom_Factor_CSV.zip"],
               "eksik": [-99.99, -999.0], "birim": "yüzde -> ondalık (/100); firma sayısı ham",
               "tanim": "ABD: CRSP (NYSE / AMEX / NASDAQ), onluklar NYSE kırılımıyla, Mom ve ST_Rev 2x3 (NYSE medyan büyüklük x 30/70 önceki "
                        "getiri) değer ağırlıklı; EW piyasa = Prior_12_2 eşit ağırlıklı onlukların firma sayısıyla ağırlıklı ortalaması (o ay "
                        "sıralamaya giren bütün hisselerin eşit ağırlıklı getirisi); Avrupa: 16 gelişmiş Avrupa ülkesi, USD"},
    "yedek": {"fon": ["SPY", "RSP", "IWM", "MTUM", "VLUE", "USMV", "VGK"], "kosul": "French dosyalarından biri bile açılmazsa o referans "
              "yerine fon vekili (MTUM - SPY momentum; RSP eşit ağırlıklı piyasa); French açıldıysa indirilmez"},
    "yahoo": {"hisse": ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "XOM", "JNJ", "PG", "V", "UNH", "HD", "CVX", "KO", "PEP",
                        "MRK", "WMT", "BAC", "CSCO", "INTC", "PFE", "T", "VZ", "DIS", "ORCL", "ABBV", "COST", "MCD", "NKE"],
              "e2_sayi": 20, "kur": "EURUSD=X", "bas": "2015-01-01",
              "tanim": "yfinance download(auto_adjust=False, günlük), Close ve Adj Close; E2 = listedeki sırayla bizim evrende olan ilk 20"},
    "bizim": {"panel": "OS.os_veri + OS.os_panel (kova sınırları olcu_sinama/os_sinir.json) + OS.os_kart_sinyal: ay sonu t = birleşik takvimde "
                       "ayın son günü, hissenin t'de geçerli barı; MOM = C_{k-21} / C_{k-252} - 1 (12-1), STREV = C_k / C_{k-21} - 1 (önceki ay); "
                       "havuz = giriş günü (t'den sonraki ilk geçerli bar) OS havuzunda (ok ve H >= 0)",
              "getiri": {"r": "AY KAPANIŞI: tutma ayı m+1'deki son geçerli kapanış / t kapanışı - 1 (French gibi kapanıştan kapanışa); AVR: kapanış "
                              "x Kur (EUR) x EURUSD (ay son kuru) = USD (French Avrupa USD)",
                         "r_os": "OS klasik kipi: t+1 açılış E0, 21. geçerli barın kapanışı / E0 - 1 (OS.os_olcu_hesap H 21; yerel para); bilgi"},
              "agirlik": {"EW": "eşit", "LQ": "Lq (OS paneli: C x V x Kur önceki 20 günün medyanı, t dahil) ile ağırlıklı = piyasa değeri yok, "
                                              "işlem değeri vekili"},
              "onluk": "t kesitinde maske VE sinyal sonlu hisseler arasında rank(first, pct) (sembol sırası); onluk = ceil(pct x 10); sıralama "
                       "getiriden ÖNCE (getirisi olmayan hisse sıralamada kalır, portföy ortalamasına girmez)",
              "iki_uc": "2x3: büyüklük = Lq maske kesiti medyanının üstü / altı; sinyal pct <= 0,30 alt, > 0,70 üst; altı portföy LQ ağırlıklı; "
                        "faktör = (küçük üst + büyük üst) / 2 - (küçük alt + büyük alt) / 2 (STREV: alt - üst); 'U30A30_EW' = eşit ağırlıklı "
                        "üst %30 - alt %30",
              "maske": {"havuz": "OS havuzu (birincil)", "tum": "havuz şartı yok (t'de geçerli bar, sinyal sonlu)",
                        "buyuk": "havuz VE t kesitinde Lq sırası ilk N (ABD 500, AVR 200)"},
              "buyuk_n": {"ABD": 500, "AVR": 200}},
    "karsilastir": {"olcu": "Pearson (hüküm) ve Spearman korelasyonu, eğim b (bizim = a + b x referans, EKK), işaret uyumu payı (aynı ay aynı "
                            "işaret; sıfır = uyumsuz), ortalama ve t (ort / (sd / kök n)) ikisi için; en çok ayrışan 10 ay = |bizim - referans| en büyük",
                    "n_min": 36},
    "hukum": {"metin": "TEZGÂH DOĞRU (o seri için) = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa serisi için korelasyon >= 0,90); "
                       "KISMEN = 0,40-0,70; UYUŞMUYOR = < 0,40 -> neden araştırılır (evren farkı: büyük-likit yaşayan hisseler; onluk tanımı; "
                       "ağırlık; veri hatası) ve tek tek sınanır (ör. yalnız en büyük 500 hisse; yalnız French'in değer ağırlıklı serisi).",
              "yorum": "korelasyon = Pearson; DOĞRU eşiği (0,70 / piyasa 0,90) geçilip işaret uyumu < %70 ise KISMEN; piyasa serisinde 0,40-0,90 "
                       "KISMEN; n < 36 ay ÖLÇÜLEMEDİ; onluk seviye serileri (D1..D10) piyasa benzeri sayılır (0,90)",
              "dogru": 0.70, "dogru_piyasa": 0.90, "isaret": 0.70, "kismen": 0.40},
    "teshis": "her ana çift için ÖNCEDEN yazılı ve hükümden bağımsız HER ZAMAN hesaplanan sürümler: (a) maske 'buyuk' (ABD ilk 500 / AVR ilk "
              "200 Lq); (b) maske 'tum'; (c) EW <-> LQ ve French EW <-> VW çaprazı; (d) OS kipi getiri r_os; (e) AVR EUR (kur çevirimsiz)",
    "sonuc": {"kural": "(1) ABD ana çiftlerinin (A1-A8) hepsi DOĞRU ise 'tezgâh yayımlanmış seriyi izliyor'; biri UYUŞMUYOR ise 'tezgâhta / "
                       "evrende fark var' (teşhis tablosuna bakılır); aksi 'kısmen izliyor'. (2) Dönem: French Mom ve ST_Rev 2016-23 ortalamasının "
                       "t'si |t| < 2 ise 'yayımlanmış veride de bu dönemde sıfırdan ayrışmıyor (dönemin gerçeği)'; t >= 2 iken bizimki < 2 ise "
                       "'evren farkı'. Tek cümle bu iki parçadan kurulur."},
    "e1": {"tanim": "ABD (AVR bilgi): hissenin ardışık iki geçerli barı (birleşik takvimde <= 5 gün arayla), gün t OS havuzunda (ok); gece = "
                    "O_t / C_{t-1} - 1, gün içi = C_t / O_t - 1 (O: OS açılış kırpması sonrası); gün başına kesit ortalaması (EW ve LQ), "
                    "yıl başına gün ortalaması (baz puan) ve yıllık toplam (%); beklenen: gece > 0, gün içi ~ 0 (bilgi)"},
    "e2": {"tanim": "20 hisse: bizim ay kapanışı getirisi (os_veri Close) ile Yahoo Adj Close ve Close ay sonu getirisi, 2016-01..2023-12; "
                    "Pearson >= 0,99 beklenir; ort fark (bizim - Adj) ~0 ise bizim kapanış temettü ayarlı, ~ -temettü verimi ise yalnız "
                    "bölünme ayarlı", "esik": 0.99},
    "yeniden": {"seri": ["ABD|tum|r|MOM|D10-D1|EW", "ABD|tum|r|PIYASA|-|EW"], "ay": ["2017-03", "2020-04", "2023-06"],
                "tanim": "ham V_ABD.pkl'den düz pandas (OC / OS kodu kullanmadan): geçerli bar süzgeci, K55 fon listesi dışı, birleşik takvim ay "
                         "sonu, MOM kendi bar indeksiyle, rank(first, pct) sembol sırası, ceil onluk, ay kapanışı getirisi; fark < 1e-9 TUTAR"},
}

TD_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("UYGULANMAZ", "iz / sinyal sınaması yok; doğrulama: bizim aylık portföy serileri = yayımlanmış referans serilerle ay ay; 'kontrol "
                         "grubu' yerine dış referans (French); eş kurulumu kullanılmaz"),
    "K2": ("EVET", "sıralama t kapanışında bilinenle (MOM C_{k-21}/C_{k-252}, STREV C_k/C_{k-21}, Lq t dahil önceki 20 gün); getiri t+1 "
                   "ayında; onluk sırası getiriden önce; KASA kapısı hisse pkl + referans kesik pkl (2023-12-31); referans 2023-12 sonrası atılır"),
    "K3": ("EVET", "OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0); ay sonu t'de geçerli bar şartı (os_kart_sinyal)"),
    "K4": ("UYGULANMAZ", "olay yok; ay başına bir portföy getirisi (aylık seri, n = ay); tekrar sayım yok"),
    "K5": ("EVET", "birincil getiri French ile aynı kip (ay kapanışından ay kapanışına); OS kipi (t+1 açılış) ayrıca r_os olarak raporlanır"),
    "K6": ("EVET", "V_*.pkl tek kip; E2 ile Yahoo Adj Close / Close'a karşı kip ölçülür; AVR Kur (yerel -> EUR) x EURUSD = USD (French "
                   "Avrupa USD); French yüzde -> ondalık, -99,99 / -999 eksik"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): seviye getirileri yukarı yanlı, alt onluklar (MOM alt, STREV alt) "
                   "yukarı yanlı -> MOM farkı aşağı, STREV farkı yukarı yanlı okunur; raporda yazılı; teşhis 'buyuk' maskesi"),
    "K8": ("EVET", "96 tutma ayı (MOM ABD ~90); n < 36 ay ÖLÇÜLEMEDİ; iki alt dönem (2016-19, 2020-23) ayrı; referans 2000-15 vs 2016-23"),
    "K9": ("EVET", "TD_ESIK sha + kod sha + git commit, referans dosya sha'ları ön kayıtta; sıra kod commit -> ön kayıt commit -> koşu; td_kapi "
                   "ön kaydın işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; hüküm kuralı iş tanımından aynen"),
    "K10": ("EVET", "French CSV ayrıştırma: bölüm başlığı + 6 haneli ay satırı; sütun sayısı başlıkla eşit; ham dosyadan rastgele 3 satır "
                    "elle (rapor) ve test_tezgah_dogrulama; yıllık (4 haneli) satırlar alınmaz"),
    "K11": ("EVET", "td_yeniden: iki seri x 3 ay ham pkl'den düz pandas (OC / OS kodu yok); French 3 satır ham metinden"),
    "K12": ("EVET", "iz iddiası yok; hüküm yalnız önceden yazılı eşikle; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_td; test); OS / OC / KASA / defter / kart / kasa / tezgah2 dosyalarına dokunulmadı; dış "
                    "istek yalnız French + Yahoo (kimlik yok, Tiingo yok); e-posta / anahtar taraması (_td_yaz)"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; tezgâh doğrulaması"),
}


class TDHata(RuntimeError):
    """Durdurucu hata: veri / referans yok, kasa / ön kayıt kapısı kapalı, ayrıştırma bozuk, yeniden üretim tutmadı."""


# ================================================================ 0) ORTAK
_TD_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_TD_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|sifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def _td_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def td_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(TD_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _td_yol(ad: str, kl: Optional[str] = None) -> str:
    if ad in ("ref_kesik", "yahoo_kesik", "ref_durum"):
        return os.path.join(kl or TD_YOL["ref"], TD_DOSYA[ad])
    return os.path.join(kl or TD_YOL["cikti"], TD_DOSYA.get(ad, ad))


def _td_yaz(yol: str, metin: str, ad: str = "dosya") -> str:
    """Metin dosyası yazar; e-posta / anahtar deseni varsa DURUR (K13)."""
    if _TD_EPOSTA.search(metin) or _TD_ANAHTAR.search(metin):
        raise TDHata(f"{ad}: e-posta / anahtar deseni bulundu, yazılmadı ({yol})")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    tdlog.info("%s yazıldı: %s", ad, yol)
    return yol


def _ay_ts(p: Any) -> pd.Timestamp:
    """Period / 'YYYY-MM' -> ay sonu gün (00:00; KASA kesik karşılaştırması için end_time değil)."""
    return pd.Period(p, "M").to_timestamp(how="start") + pd.offsets.MonthEnd(0)


def _per(a: str, b: str) -> Tuple[pd.Period, pd.Period]:
    return pd.Period(a, "M"), pd.Period(b, "M")


# ================================================================ 1) REFERANS: French ayrıştırma
def td_french_ayristir(metin: str) -> Dict[str, pd.DataFrame]:
    """French CSV metni -> {bölüm adı: DataFrame (PeriodIndex M, sütunlar)}. Yalnız 6 haneli (YYYYMM) aylık satırlar; yıllık satırlar atlanır.
    Bölüm adı: başlık satırından önceki son metin satırı ('' ise 'aylik'). Değerler HAM (yüzde); eksik kodlar NaN."""
    out: Dict[str, Dict[str, List[float]]] = {}; kolon: Dict[str, List[str]] = {}
    son_metin = ""; cur: Optional[str] = None; kol: Optional[List[str]] = None
    for satir in metin.splitlines():
        s = satir.strip()
        if not s:
            continue
        if s.startswith(","):
            kol = [c.strip() for c in s.split(",")[1:]]
            cur = son_metin or "aylik"
            if cur in out and kolon.get(cur) != kol:
                cur = f"{cur}#{len(out)}"
            out.setdefault(cur, {}); kolon[cur] = kol
            continue
        parca = [p.strip() for p in s.split(",")]
        if re.fullmatch(r"\d{6}", parca[0]):
            if kol is None or cur is None:
                continue
            if len(parca) - 1 != len(kol):
                raise TDHata(f"French ayrıştırma: '{cur}' bölümünde sütun sayısı {len(parca) - 1} != başlık {len(kol)} ({parca[0]})")
            out[cur][parca[0]] = [float(x) for x in parca[1:]]
        elif re.fullmatch(r"\d{4}", parca[0]):
            continue   # yıllık satır
        else:
            son_metin = s; kol = None; cur = None
    R: Dict[str, pd.DataFrame] = {}
    for ad, d in out.items():
        if not d:
            continue
        df = pd.DataFrame.from_dict(d, orient="index", columns=kolon[ad])
        df.index = pd.PeriodIndex([pd.Period(f"{k[:4]}-{k[4:]}", "M") for k in df.index], freq="M")
        df = df.sort_index()
        for e in TD_ESIK["french"]["eksik"]:
            df = df.mask(np.isclose(df, e))
        R[ad] = df
    return R


def _td_bolum(B: Dict[str, pd.DataFrame], *anahtar: str) -> pd.DataFrame:
    for ad, df in B.items():
        if all(a.lower() in ad.lower() for a in anahtar):
            return df
    raise TDHata(f"French bölümü bulunamadı: {anahtar} (bölümler: {list(B)[:8]})")


def td_french_seriler(zipler: Dict[str, bytes]) -> Tuple[Dict[str, pd.Series], Dict[str, Any]]:
    """İndirilmiş French zip baytları -> referans aylık seriler (ondalık, PeriodIndex) + ham satır örneği (yeniden üretim için)."""
    def oku(ad: str) -> Tuple[Dict[str, pd.DataFrame], str]:
        z = zipfile.ZipFile(io.BytesIO(zipler[ad]))
        uyeler = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(uyeler) != 1:
            raise TDHata(f"{ad}: zip içinde tek csv beklenir: {z.namelist()}")
        metin = z.read(uyeler[0]).decode("latin-1")
        return td_french_ayristir(metin), metin
    S: Dict[str, pd.Series] = {}; ham: Dict[str, str] = {}
    B, ham["ff3"] = oku("F-F_Research_Data_Factors_CSV.zip"); f = B[list(B)[0]]
    S["US_MKT"] = (f["Mkt-RF"] + f["RF"]) / 100; S["US_RF"] = f["RF"] / 100
    B, ham["mom"] = oku("F-F_Momentum_Factor_CSV.zip"); S["US_MOM"] = B[list(B)[0]]["Mom"] / 100
    B, ham["strev"] = oku("F-F_ST_Reversal_Factor_CSV.zip"); S["US_STREV"] = B[list(B)[0]]["ST_Rev"] / 100
    for dosya, kod, ters in (("10_Portfolios_Prior_12_2_CSV.zip", "P12", False), ("10_Portfolios_Prior_1_0_CSV.zip", "P1", True)):
        B, ham[kod] = oku(dosya)
        vw = _td_bolum(B, "Value Weight", "Monthly"); ew = _td_bolum(B, "Equal Weighted", "Monthly"); nf = _td_bolum(B, "Number of Firms")
        if vw.shape[1] != 10 or ew.shape[1] != 10 or nf.shape[1] != 10:
            raise TDHata(f"{dosya}: onluk sütun sayısı 10 değil")
        for i in range(10):
            S[f"US_{kod}_VW_D{i + 1}"] = vw.iloc[:, i] / 100; S[f"US_{kod}_EW_D{i + 1}"] = ew.iloc[:, i] / 100
        sp = (vw.iloc[:, 0] - vw.iloc[:, 9]) if ters else (vw.iloc[:, 9] - vw.iloc[:, 0])
        se = (ew.iloc[:, 0] - ew.iloc[:, 9]) if ters else (ew.iloc[:, 9] - ew.iloc[:, 0])
        S[f"US_{kod}_VW_FARK"] = sp / 100; S[f"US_{kod}_EW_FARK"] = se / 100
        if kod == "P12":
            n = nf.reindex(ew.index)
            S["US_EWMKT"] = (ew * n.to_numpy()).sum(axis=1, min_count=10) / n.sum(axis=1, min_count=10) / 100
    B, ham["eu3"] = oku("Europe_3_Factors_CSV.zip"); f = B[list(B)[0]]
    S["EU_MKT"] = (f["Mkt-RF"] + f["RF"]) / 100
    B, ham["eumom"] = oku("Europe_Mom_Factor_CSV.zip"); S["EU_WML"] = B[list(B)[0]]["WML"] / 100
    return S, ham


def _td_curl(url: str, hedef: str) -> Tuple[bool, str]:
    try:
        r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "180", "-o", hedef, url], capture_output=True, text=True, timeout=240)
    except (OSError, subprocess.SubprocessError) as ex:
        return False, f"{type(ex).__name__}: {ex}"
    if r.returncode != 0 or not os.path.exists(hedef) or os.path.getsize(hedef) < 500:
        return False, (r.stderr or f"kod {r.returncode}").strip()[:300]
    return True, "ok"


def _td_kes(S: Dict[str, pd.Series]) -> Dict[str, pd.Series]:
    son = pd.Period(TD_ESIK["kesik"][:7], "M")
    return {k: v[v.index <= son].dropna() for k, v in S.items()}


def td_yahoo_indir(semboller: List[str]) -> Dict[str, pd.DataFrame]:
    """yfinance günlük Close / Adj Close (auto_adjust=False), 2023-12-29'a kadar (end dışlayıcı 2023-12-30); sonrası atılır."""
    import yfinance as yf
    son = pd.Timestamp(TD_ESIK["yahoo_son"])
    d = yf.download(semboller, start=TD_ESIK["yahoo"]["bas"], end=str((son + pd.Timedelta(days=1)).date()), interval="1d",
                    auto_adjust=False, progress=False, group_by="column", threads=True)
    if d is None or not len(d):
        raise TDHata("Yahoo: boş yanıt")
    out = {}
    for k in ("Close", "Adj Close"):
        x = d[k] if k in d.columns.get_level_values(0) else None
        if x is None:
            raise TDHata(f"Yahoo: {k} yok")
        if isinstance(x, pd.Series):
            x = x.to_frame(semboller[0])
        x.index = pd.DatetimeIndex(x.index).tz_localize(None).normalize()
        out[k] = x[x.index <= son].astype(float)
    return out


def td_ref_indir(kl: Optional[str] = None) -> Dict[str, Any]:
    """French zipleri (curl) + Yahoo (hisse + EURUSD) -> kesilmiş pkl'ler + durum json. Açılmayan kaynak 'erişilemedi' yazılır, sayı uydurulmaz."""
    kl = kl or TD_YOL["ref"]; os.makedirs(kl, exist_ok=True)
    durum: Dict[str, Any] = {"zaman": _td_simdi(), "french": {}, "yahoo": {}, "yedek": None}
    zipler: Dict[str, bytes] = {}
    for ad in TD_ESIK["french"]["dosya"]:
        y = os.path.join(kl, ad); ok, msg = _td_curl(TD_ESIK["french"]["kok"] + ad, y)
        if ok:
            try:
                b = open(y, "rb").read(); zipfile.ZipFile(io.BytesIO(b)).testzip(); zipler[ad] = b
                durum["french"][ad] = {"durum": "açıldı", "bayt": len(b), "sha": OS._os_sha_dosya(y)}
            except Exception as ex:   # bozuk zip: erişilemedi say
                durum["french"][ad] = {"durum": f"erişilemedi (zip açılmadı: {type(ex).__name__})"}
        else:
            durum["french"][ad] = {"durum": f"erişilemedi ({msg})"}
    S: Dict[str, pd.Series] = {}
    if len(zipler) == len(TD_ESIK["french"]["dosya"]):
        S, ham = td_french_seriler(zipler)
        durum["french_ham_ornek"] = {k: v.splitlines()[:6] for k, v in ham.items()}
    else:
        durum["yedek"] = "French eksik -> yedek fonlar"
    Y: Dict[str, Any] = {}
    try:
        sem = list(TD_ESIK["yahoo"]["hisse"]) + [TD_ESIK["yahoo"]["kur"]] + (TD_ESIK["yedek"]["fon"] if durum["yedek"] else [])
        Y = td_yahoo_indir(sem)
        durum["yahoo"] = {"durum": "açıldı", "sembol": int(Y["Close"].notna().any().sum()), "en_gec": str(Y["Close"].index.max().date()),
                          "eksik": sorted(s for s in sem if s not in Y["Close"].columns or Y["Close"][s].notna().sum() == 0)}
    except Exception as ex:   # Yahoo açılmazsa E2 / AVR USD 'erişilemedi'
        durum["yahoo"] = {"durum": f"erişilemedi ({type(ex).__name__}: {str(ex)[:200]})"}
    if durum["yedek"] and Y:
        C = Y["Adj Close"]; ay = C.groupby(C.index.to_period("M")).last().pct_change()
        if {"MTUM", "SPY"} <= set(ay.columns):
            S["US_MOM"] = ay["MTUM"] - ay["SPY"]
        if "RSP" in ay.columns:
            S["US_EWMKT"] = ay["RSP"]
        if "SPY" in ay.columns:
            S["US_MKT"] = ay["SPY"]
        if "VGK" in ay.columns:
            S["EU_MKT"] = ay["VGK"]
    S = _td_kes(S)
    if not S:
        raise TDHata("hiçbir referans açılmadı")
    ref_df = pd.DataFrame({k: v for k, v in S.items()})
    ref_df.index = pd.DatetimeIndex([_ay_ts(p) for p in ref_df.index])
    pd.to_pickle({"ref": ref_df}, _td_yol("ref_kesik", kl))
    if Y:
        pd.to_pickle({k: v for k, v in Y.items()}, _td_yol("yahoo_kesik", kl))
    durum["ref_seri"] = {k: {"ilk": str(v.index.min()), "son": str(v.index.max()), "n": int(len(v))} for k, v in S.items()}
    durum["sha"] = {"ref_kesik": OS._os_sha_dosya(_td_yol("ref_kesik", kl))}
    if Y:
        durum["sha"]["yahoo_kesik"] = OS._os_sha_dosya(_td_yol("yahoo_kesik", kl))
    _td_yaz(_td_yol("ref_durum", kl), json.dumps(OS._os_temizle(durum), ensure_ascii=False, indent=1, default=OS._os_json), "referans durumu")
    return durum


def td_kasa_kapi(veri: Optional[str] = None, kl: Optional[str] = None) -> Dict[str, Any]:
    """KASA: hisse pkl'leri (OS kapısı: açık kesik = 2023-12-31) + kesilmiş referans / Yahoo pkl'leri kesiği aşmıyor."""
    import KASA as _KS
    r = OS.os_kasa_kapi(veri)
    ek = [p for p in (_td_yol("ref_kesik", kl), _td_yol("yahoo_kesik", kl)) if os.path.exists(p)]
    if not os.path.exists(_td_yol("ref_kesik", kl)):
        raise TDHata(f"referans kesik dosyası yok: {_td_yol('ref_kesik', kl)} (önce 'ref')")
    try:
        r2 = _KS.kasa_kapisi(ek, kesik=TD_ESIK["kesik"], cikti=TD_YOL["kasa_dizin"])
    except Exception as ex:
        raise TDHata(f"KASA kapısı (referans) KAPALI: {ex}") from ex
    return {"hisse": r, "referans": r2}


def td_ref_yukle(kl: Optional[str] = None) -> Tuple[Dict[str, pd.Series], Dict[str, pd.DataFrame]]:
    R = pd.read_pickle(_td_yol("ref_kesik", kl))["ref"]
    R.index = R.index.to_period("M")
    S = {k: R[k].dropna() for k in R.columns}
    Y = pd.read_pickle(_td_yol("yahoo_kesik", kl)) if os.path.exists(_td_yol("yahoo_kesik", kl)) else {}
    return S, Y


# ================================================================ 2) BİZİM SERİLER
def td_ay_kapanis(V: Dict[str, pd.DataFrame], kur: bool = True) -> pd.DataFrame:
    """Hisse başına ay son geçerli kapanışı (x Kur = EUR, kur=True) -> DataFrame [ay (Period) x sembol]."""
    sat = {}
    for s, d in V.items():
        c = d.Close * (d.Kur if kur and "Kur" in d.columns else 1.0)
        sat[s] = c.groupby(d.index.to_period("M")).last()
    C = pd.DataFrame(sat).sort_index()
    if len(C):
        C = C.reindex(pd.period_range(C.index.min(), C.index.max(), freq="M"))
    return C


def td_eurusd_ay(Y: Dict[str, pd.DataFrame]) -> Optional[pd.Series]:
    k = TD_ESIK["yahoo"]["kur"]
    if not Y or k not in Y.get("Close", pd.DataFrame()).columns:
        return None
    x = Y["Close"][k].dropna()
    return x.groupby(x.index.to_period("M")).last()


def td_kesit(Pn: Dict[str, Any], Vd: Dict[str, Any], fx: Optional[pd.Series]) -> pd.DataFrame:
    """Ay sonu kesiti: OS kart sinyalleri + Lq(t) + tutma ayı getirileri (r: ay kapanışı, USD / yerel; r_eur; r_os: OS kipi)."""
    X = OS.os_kart_sinyal(Pn)
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64)
    Z = X[["sembol", "j", "tarih", "k", "d", "MOM", "STREV", "havuz"]].copy()
    Z["ay"] = Z.tarih.dt.to_period("M")
    Z["Lq"] = Pn["Lq"][d, j]
    C = td_ay_kapanis(Vd["V"], kur=True)
    Rl = C.shift(-1) / C - 1                                                    # tutma ayı (m+1) getirisi, satır m
    if Pn["pazar"] == "AVR" and fx is not None:
        f = fx.reindex(C.index)
        Ru = (C.shift(-1).mul(f.shift(-1), axis=0)) / C.mul(f, axis=0) - 1
    else:
        Ru = Rl
    mi = pd.MultiIndex.from_arrays([Z.ay, Z.sembol])
    Z["r"] = Ru.stack(future_stack=True).reindex(mi).to_numpy(float)
    Z["r_eur"] = Rl.stack(future_stack=True).reindex(mi).to_numpy(float)
    e1 = Pn["EIX"][d, j]
    Z["r_os"] = OS.os_olcu_hesap(Pn["dep"], j, e1, 21)["R"]
    Z["tut"] = Z.ay + 1
    return Z


def _td_ort(g: pd.DataFrame, r: str, w: Optional[str]) -> float:
    g = g[np.isfinite(g[r].to_numpy(float))]
    if w is None:
        return float(g[r].mean()) if len(g) else np.nan
    g = g[np.isfinite(g[w].to_numpy(float)) & (g[w].to_numpy(float) > 0)]
    return float(np.average(g[r], weights=g[w])) if len(g) else np.nan


def td_maske(Z: pd.DataFrame, maske: str, pazar: str) -> np.ndarray:
    if maske == "tum":
        return np.ones(len(Z), bool)
    m = Z.havuz.to_numpy(bool)
    if maske == "havuz":
        return m
    if maske == "buyuk":
        N = TD_ESIK["bizim"]["buyuk_n"][pazar]
        lq = Z.Lq.where(m & np.isfinite(Z.Lq.to_numpy(float)))
        rk = lq.groupby(Z.ay).rank(method="first", ascending=False)
        return (rk <= N).fillna(False).to_numpy(bool)
    raise TDHata(f"bilinmeyen maske {maske}")


def td_portfoy(Z: pd.DataFrame, m: np.ndarray, sinyal: str, rkol: str) -> Dict[str, pd.Series]:
    """Onluk (D1..D10, EW ve LQ), onluk farkı, 2x3 faktör (LQ) ve U30A30_EW; anahtar 'D10-D1|EW' vb. İndeks = tutma ayı."""
    Y = Z[m & np.isfinite(Z[sinyal].to_numpy(float))].sort_values(["ay", "sembol"], kind="mergesort").copy()
    out: Dict[str, pd.Series] = {}
    if not len(Y):
        return out
    Y["pct"] = Y.groupby("ay")[sinyal].rank(method="first", pct=True)
    Y["onluk"] = np.clip(np.ceil(Y.pct * 10).astype(int), 1, 10)
    lqm = Y.groupby("ay").Lq.transform("median")
    Y["buyuk"] = Y.Lq > lqm
    Y["uc"] = np.where(Y.pct <= 0.30, "A", np.where(Y.pct > 0.70, "U", "O"))
    res: Dict[str, Dict[pd.Period, float]] = {}
    for ay, g in Y.groupby("ay", sort=True):
        t = ay + 1
        for w, wk in (("EW", None), ("LQ", "Lq")):
            for i in range(1, 11):
                res.setdefault(f"D{i}|{w}", {})[t] = _td_ort(g[g.onluk == i], rkol, wk)
        p6 = {(b, u): _td_ort(g[(g.buyuk == b) & (g.uc == u)], rkol, "Lq") for b in (False, True) for u in ("A", "U")}
        res.setdefault("2X3|LQ", {})[t] = 0.5 * (p6[(False, "U")] + p6[(True, "U")]) - 0.5 * (p6[(False, "A")] + p6[(True, "A")])
        res.setdefault("U30A30|EW", {})[t] = _td_ort(g[g.uc == "U"], rkol, None) - _td_ort(g[g.uc == "A"], rkol, None)
        res.setdefault("N", {})[t] = float(np.isfinite(g[rkol].to_numpy(float)).sum())
    for k, v in res.items():
        out[k] = pd.Series(v, dtype=float).sort_index()
    for w in ("EW", "LQ"):
        out[f"D10-D1|{w}"] = out[f"D10|{w}"] - out[f"D1|{w}"]
    return out


def td_piyasa(Z: pd.DataFrame, m: np.ndarray, rkol: str) -> Dict[str, pd.Series]:
    Y = Z[m]; res: Dict[str, Dict[pd.Period, float]] = {}
    for ay, g in Y.groupby("ay", sort=True):
        res.setdefault("EW", {})[ay + 1] = _td_ort(g, rkol, None)
        res.setdefault("LQ", {})[ay + 1] = _td_ort(g, rkol, "Lq")
        res.setdefault("N", {})[ay + 1] = float(np.isfinite(g[rkol].to_numpy(float)).sum())
    return {k: pd.Series(v, dtype=float).sort_index() for k, v in res.items()}


def td_bizim_seriler(Z: pd.DataFrame, pazar: str) -> Dict[str, pd.Series]:
    """Ad biçimi: 'PAZAR|maske|rkol|kart|portföy|ağırlık' (STREV farkları alt - üst = D1-D10 olarak çevrilir; 2x3 STREV = alt - üst)."""
    S: Dict[str, pd.Series] = {}
    rkoller = ["r", "r_os"] + (["r_eur"] if pazar == "AVR" else [])
    for maske in ("havuz", "tum", "buyuk"):
        m = td_maske(Z, maske, pazar)
        for rk in (rkoller if maske == "havuz" else ["r"]):
            for k, v in td_piyasa(Z, m, rk).items():
                S[f"{pazar}|{maske}|{rk}|PIYASA|-|{k}"] = v
            for kart in ("MOM", "STREV"):
                P = td_portfoy(Z, m, kart, rk)
                for k, v in P.items():
                    port, w = (k.split("|") + ["-"])[:2]
                    if kart == "STREV" and port in ("D10-D1", "2X3", "U30A30"):
                        v = -v
                        port = {"D10-D1": "D1-D10", "2X3": "2X3", "U30A30": "A30U30"}[port]
                    S[f"{pazar}|{maske}|{rk}|{kart}|{port}|{w}"] = v
    return S


# ================================================================ 3) KARŞILAŞTIRMA
def _td_t(x: np.ndarray) -> float:
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3 or x.std(ddof=1) == 0:
        return float("nan")
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def td_hukum(r: float, isaret: float, n: int, piyasa: bool) -> str:
    H = TD_ESIK["hukum"]
    if n < TD_ESIK["karsilastir"]["n_min"] or not np.isfinite(r):
        return "ÖLÇÜLEMEDİ"
    ust = H["dogru_piyasa"] if piyasa else H["dogru"]
    if r >= ust and isaret >= H["isaret"]:
        return "DOĞRU"
    if r >= H["kismen"]:
        return "KISMEN"
    return "UYUŞMUYOR"


def td_karsilastir(biz: pd.Series, ref: pd.Series, piyasa: bool, pencere: Optional[List[str]] = None) -> Dict[str, Any]:
    a, b = _per(*(pencere or TD_ESIK["pencere"]["karsilastirma"]))
    x = biz[(biz.index >= a) & (biz.index <= b)]; y = ref[(ref.index >= a) & (ref.index <= b)]
    D = pd.concat({"biz": x, "ref": y}, axis=1).dropna()
    n = len(D)
    if n < 3:
        return {"n": n, "hukum": "ÖLÇÜLEMEDİ"}
    pr = float(D.biz.corr(D.ref)); sp = float(D.biz.corr(D.ref, method="spearman"))
    vr = float(D.ref.var(ddof=1)); bb = float(D.biz.cov(D.ref) / vr) if vr > 0 else float("nan")
    aa = float(D.biz.mean() - bb * D.ref.mean()) if np.isfinite(bb) else float("nan")
    isr = float((np.sign(D.biz) == np.sign(D.ref)).where(D.ref != 0, False).mean())
    fark = (D.biz - D.ref)
    en = fark.abs().sort_values(ascending=False).head(10)
    ayr = [{"ay": str(p), "biz": float(D.biz[p]), "ref": float(D.ref[p]), "fark": float(fark[p])} for p in en.index]
    alt = {}
    for ad, (p, q) in TD_ESIK["pencere"]["alt"].items():
        Dd = D[(D.index >= pd.Period(p, "M")) & (D.index <= pd.Period(q, "M"))]
        alt[ad] = {"n": len(Dd), "pearson": float(Dd.biz.corr(Dd.ref)) if len(Dd) > 2 else float("nan"),
                   "biz_ort": float(Dd.biz.mean()) if len(Dd) else float("nan"), "ref_ort": float(Dd.ref.mean()) if len(Dd) else float("nan")}
    return {"n": n, "ilk": str(D.index.min()), "son": str(D.index.max()), "pearson": pr, "spearman": sp, "egim": bb, "kesen": aa,
            "isaret": isr, "biz_ort": float(D.biz.mean()), "biz_t": _td_t(D.biz.to_numpy()), "ref_ort": float(D.ref.mean()),
            "ref_t": _td_t(D.ref.to_numpy()), "alt": alt, "ayrisan": ayr, "piyasa": piyasa, "hukum": td_hukum(pr, isr, n, piyasa)}


# Ana çiftler (önceden yazılı): kod, bizim seri, referans, piyasa?, açıklama
TD_CIFT: List[Tuple[str, str, str, bool, str]] = [
    ("A1", "ABD|havuz|r|PIYASA|-|EW", "US_EWMKT", True, "ABD evren getirisi EW vs French EW piyasa (Prior_12_2 EW onlukları, firma ağırlıklı)"),
    ("A2", "ABD|havuz|r|PIYASA|-|LQ", "US_MKT", True, "ABD evren getirisi LQ vs French piyasa (Mkt-RF + RF, VW)"),
    ("A3", "ABD|havuz|r|MOM|D10-D1|EW", "US_P12_EW_FARK", False, "ABD MOM onluk üst - alt EW vs French Prior_12_2 EW Hi - Lo"),
    ("A4", "ABD|havuz|r|MOM|D10-D1|LQ", "US_P12_VW_FARK", False, "ABD MOM onluk üst - alt LQ vs French Prior_12_2 VW Hi - Lo"),
    ("A5", "ABD|havuz|r|MOM|2X3|LQ", "US_MOM", False, "ABD MOM 2x3 (üst 30 - alt 30) LQ vs French Mom"),
    ("A6", "ABD|havuz|r|STREV|D1-D10|EW", "US_P1_EW_FARK", False, "ABD STREV onluk alt - üst EW vs French Prior_1_0 EW Lo - Hi"),
    ("A7", "ABD|havuz|r|STREV|D1-D10|LQ", "US_P1_VW_FARK", False, "ABD STREV onluk alt - üst LQ vs French Prior_1_0 VW Lo - Hi"),
    ("A8", "ABD|havuz|r|STREV|2X3|LQ", "US_STREV", False, "ABD STREV 2x3 (alt 30 - üst 30) LQ vs French ST_Rev"),
    ("E1", "AVR|havuz|r|PIYASA|-|LQ", "EU_MKT", True, "AVR evren getirisi LQ (USD) vs French Avrupa piyasa (USD)"),
    ("E2", "AVR|havuz|r|PIYASA|-|EW", "EU_MKT", True, "AVR evren getirisi EW (USD) vs French Avrupa piyasa (USD)"),
    ("E3", "AVR|havuz|r|MOM|2X3|LQ", "EU_WML", False, "AVR MOM 2x3 LQ (USD) vs French Avrupa WML"),
    ("E4", "AVR|havuz|r|MOM|D10-D1|EW", "EU_WML", False, "AVR MOM onluk üst - alt EW (USD) vs French Avrupa WML"),
]


def td_cift_listesi(S: Dict[str, pd.Series]) -> List[Dict[str, Any]]:
    """Ana çiftler + önceden yazılı teşhis sürümleri + onluk seviyeleri (bilgi)."""
    L: List[Dict[str, Any]] = [{"kod": k, "biz": b, "ref": r, "piyasa": p, "aciklama": a, "tur": "ANA"} for k, b, r, p, a in TD_CIFT]
    for k, b, r, p, a in TD_CIFT:
        pz, mk, rk, kart, port, w = b.split("|")
        sur = [("buyuk", "r", w, r, "a: büyük"), ("tum", "r", w, r, "b: tüm")]
        if kart != "PIYASA" and pz == "ABD":
            karsi_w = "LQ" if w == "EW" else "EW"
            if port != "2X3":
                karsi_r = r.replace("_EW_", "_VW_") if "_EW_" in r else r.replace("_VW_", "_EW_")
                sur += [("havuz", "r", karsi_w, r, "c: ağırlık çapraz"), ("havuz", "r", w, karsi_r, "c: French çapraz")]
            else:
                sur += [("havuz", "r", "EW", r, "c: 2x3 yerine U30A30 EW")]
        if kart == "PIYASA" and pz == "ABD":
            sur += [("havuz", "r", "LQ" if w == "EW" else "EW", "US_MKT" if r == "US_EWMKT" else "US_EWMKT", "c: çapraz")]
        sur += [("havuz", "r_os", w, r, "d: OS kipi (t+1 açılış, 21 bar)")]
        if pz == "AVR":
            sur += [("havuz", "r_eur", w, r, "e: EUR (kur çevirimsiz)")]
        for i, (mk2, rk2, w2, r2, ac) in enumerate(sur):
            port2 = port
            if ac.startswith("c: 2x3"):
                port2 = "U30A30" if kart == "MOM" else "A30U30"
            L.append({"kod": f"{k}.{i + 1}", "biz": f"{pz}|{mk2}|{rk2}|{kart}|{port2}|{w2}", "ref": r2, "piyasa": p,
                      "aciklama": f"{a} [{ac}]", "tur": "TEŞHİS"})
    for kod, kart in (("P12", "MOM"), ("P1", "STREV")):
        for i in range(1, 11):
            for w, fw in (("EW", "EW"), ("LQ", "VW")):
                L.append({"kod": f"O.{kart}.D{i}.{w}", "biz": f"ABD|havuz|r|{kart}|D{i}|{w}", "ref": f"US_{kod}_{fw}_D{i}", "piyasa": True,
                          "aciklama": f"ABD {kart} onluk D{i} seviye {w} vs French {fw}", "tur": "BİLGİ"})
    return L


def td_ref_donem(R: Dict[str, pd.Series]) -> List[Dict[str, Any]]:
    """Referansın kendi dönem ortalamaları: 2000-15 vs 2016-23 (ort, t, n) ve 2016-19 / 2020-23."""
    out = []
    pen = {"2000-15": TD_ESIK["pencere"]["ref_eski"], "2016-23": TD_ESIK["pencere"]["ref_yeni"], **{f"{k}": v for k, v in TD_ESIK["pencere"]["alt"].items()}}
    for k in ("US_MOM", "US_P12_VW_FARK", "US_P12_EW_FARK", "US_STREV", "US_P1_VW_FARK", "US_P1_EW_FARK", "US_MKT", "US_EWMKT", "EU_WML", "EU_MKT"):
        if k not in R:
            out.append({"seri": k, "durum": "erişilemedi"}); continue
        s = R[k]; sat: Dict[str, Any] = {"seri": k}
        for ad, (a, b) in pen.items():
            x = s[(s.index >= pd.Period(a, "M")) & (s.index <= pd.Period(b, "M"))].to_numpy(float)
            sat[ad] = {"n": int(np.isfinite(x).sum()), "ort": float(np.nanmean(x)) if len(x) else float("nan"), "t": _td_t(x)}
        out.append(sat)
    return out


def td_sonuc(K: List[Dict[str, Any]], RD: List[Dict[str, Any]], S: Dict[str, pd.Series]) -> Dict[str, Any]:
    ana = [c for c in K if c["tur"] == "ANA" and c["kod"].startswith("A")]
    hk = [c["sonuc"]["hukum"] for c in ana]
    if all(h == "DOĞRU" for h in hk):
        p1 = "tezgâh (veri + panel + portföy hesabı) yayımlanmış ABD serilerini izliyor"
    elif any(h == "UYUŞMUYOR" for h in hk):
        p1 = "tezgâhta ya da evrende fark var (UYUŞMUYOR: " + ", ".join(c["kod"] for c in ana if c["sonuc"]["hukum"] == "UYUŞMUYOR") + ")"
    else:
        p1 = "tezgâh yayımlanmış ABD serilerini kısmen izliyor (DOĞRU olmayan: " + ", ".join(
            f"{c['kod']} {c['sonuc']['hukum']}" for c in ana if c["sonuc"]["hukum"] != "DOĞRU") + ")"
    rd = {r["seri"]: r for r in RD}
    p2 = []
    for ref, biz in (("US_MOM", "ABD|havuz|r|MOM|2X3|LQ"), ("US_STREV", "ABD|havuz|r|STREV|2X3|LQ")):
        if ref not in rd or "2016-23" not in rd[ref]:
            p2.append(f"{ref} erişilemedi"); continue
        t_ref = rd[ref]["2016-23"]["t"]
        b = S.get(biz); a_, b_ = _per(*TD_ESIK["pencere"]["ref_yeni"])
        t_biz = _td_t(b[(b.index >= a_) & (b.index <= b_)].to_numpy()) if b is not None else float("nan")
        if abs(t_ref) < 2:
            p2.append(f"{ref} 2016-23 yayımlanmış seride de sıfırdan ayrışmıyor (t {t_ref:+.2f}; bizim t {t_biz:+.2f}): dönemin gerçeği")
        elif abs(t_biz) < 2:
            p2.append(f"{ref} 2016-23 yayımlanmış seride ayrışıyor (t {t_ref:+.2f}) ama bizimki ayrışmıyor (t {t_biz:+.2f}): evren farkı")
        else:
            p2.append(f"{ref} 2016-23 hem yayımlanmış (t {t_ref:+.2f}) hem bizim seride (t {t_biz:+.2f}) ayrışıyor")
    return {"tezgah": p1, "donem": p2, "cumle": f"{p1}; " + "; ".join(p2) + "."}


# ================================================================ 4) EK DOĞRULAMALAR
def td_e1(Pn: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Gece / gün içi ayrışması (yıl başına; EW ve LQ kesit ortalaması)."""
    dep = Pn["dep"]; ok = Pn["ok"]; Lq = Pn["Lq"]; idx = Pn["tarih"]; n, u = ok.shape
    GN = np.full((n, u), np.nan); GI = np.full((n, u), np.nan)
    for j in range(u):
        a, b = dep["off"][j], dep["off"][j + 1]
        if b - a < 2:
            continue
        pos = dep["POS"][a:b]; O = dep["O"][a:b]; C = dep["C"][a:b]
        ar = np.diff(pos) <= 5
        p = pos[1:][ar]
        GN[p, j] = (O[1:] / C[:-1] - 1)[ar]; GI[p, j] = (C[1:] / O[1:] - 1)[ar]
    m = ok & np.isfinite(GN) & np.isfinite(GI)
    w = np.where(m & np.isfinite(Lq) & (Lq > 0), Lq, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        gn_ew = np.where(m, GN, 0).sum(1) / m.sum(1); gi_ew = np.where(m, GI, 0).sum(1) / m.sum(1)
        gn_lq = (np.where(m, GN, 0) * w).sum(1) / w.sum(1); gi_lq = (np.where(m, GI, 0) * w).sum(1) / w.sum(1)
    D = pd.DataFrame({"gn_ew": gn_ew, "gi_ew": gi_ew, "gn_lq": gn_lq, "gi_lq": gi_lq, "n": m.sum(1)}, index=idx)
    D = D[D.n >= 30]
    out = []
    for y, g in D.groupby(D.index.year):
        out.append({"yil": int(y), "gun": int(len(g)), "hisse_ort": float(g.n.mean()),
                    "gece_ew_bp": float(g.gn_ew.mean() * 1e4), "gunici_ew_bp": float(g.gi_ew.mean() * 1e4),
                    "gece_ew_yil_pct": float(g.gn_ew.sum() * 100), "gunici_ew_yil_pct": float(g.gi_ew.sum() * 100),
                    "gece_lq_bp": float(g.gn_lq.mean() * 1e4), "gunici_lq_bp": float(g.gi_lq.mean() * 1e4),
                    "gece_lq_yil_pct": float(g.gn_lq.sum() * 100), "gunici_lq_yil_pct": float(g.gi_lq.sum() * 100)})
    return out


def td_e2(V: Dict[str, pd.DataFrame], Y: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    if not Y:
        return {"durum": "erişilemedi (Yahoo)"}
    sec = [s for s in TD_ESIK["yahoo"]["hisse"] if s in V and s in Y["Adj Close"].columns and Y["Adj Close"][s].notna().sum() > 100]
    sec = sec[:TD_ESIK["yahoo"]["e2_sayi"]]
    a, b = _per(*TD_ESIK["pencere"]["karsilastirma"]); sat = []
    for s in sec:
        biz = V[s].Close.groupby(V[s].index.to_period("M")).last().pct_change()
        ya = Y["Adj Close"][s].dropna(); ya = ya.groupby(ya.index.to_period("M")).last().pct_change()
        yc = Y["Close"][s].dropna(); yc = yc.groupby(yc.index.to_period("M")).last().pct_change()
        D = pd.concat({"biz": biz, "adj": ya, "close": yc}, axis=1)
        D = D[(D.index >= a) & (D.index <= b)].dropna()
        if len(D) < 12:
            sat.append({"sembol": s, "n": len(D), "durum": "yetersiz"}); continue
        sat.append({"sembol": s, "n": len(D), "r_adj": float(D.biz.corr(D.adj)), "r_close": float(D.biz.corr(D.close)),
                    "fark_adj_bp": float((D.biz - D.adj).mean() * 1e4), "fark_close_bp": float((D.biz - D.close).mean() * 1e4),
                    "maks_fark_adj_pct": float((D.biz - D.adj).abs().max() * 100)})
    ra = [x["r_adj"] for x in sat if "r_adj" in x]
    return {"durum": "açıldı", "hisse": sat, "gecen": int(sum(r >= TD_ESIK["e2"]["esik"] for r in ra)), "n": len(ra),
            "min_r_adj": float(min(ra)) if ra else float("nan"), "med_fark_adj_bp": float(np.median([x["fark_adj_bp"] for x in sat if "r_adj" in x])) if ra else float("nan"),
            "med_fark_close_bp": float(np.median([x["fark_close_bp"] for x in sat if "r_adj" in x])) if ra else float("nan")}


# ================================================================ 5) YENİDEN ÜRETİM (düz pandas; OC / OS kodu yok)
def td_yeniden(J: Dict[str, Any], veri: Optional[str] = None) -> Dict[str, Any]:
    v = veri or TD_YOL["veri"]
    ham = pd.read_pickle(os.path.join(v, "V_ABD.pkl"))
    if isinstance(ham, dict) and "veri" in ham and isinstance(ham["veri"], dict):
        ham = ham["veri"]
    fon = set()
    y = os.path.join(KOK_TD, "arastirma_cikti", "k55_dallanma", "K55_EVREN_DISI.csv")
    if os.path.exists(y):
        t = pd.read_csv(y); t = t[t.kategori.astype(str) == "fon_evren_disi"] if "kategori" in t.columns else t
        fon = set(t.sembol.astype(str).str.upper())
    y2 = os.path.join(KOK_TD, "evren_disi_ABD.csv")
    if os.path.exists(y2):
        fon |= set(pd.read_csv(y2).sembol.astype(str).str.upper())
    temiz = {}
    for s, d in ham.items():
        if str(s).upper() in fon:
            continue
        d = d.copy()
        if isinstance(d.columns, pd.MultiIndex):
            d.columns = d.columns.get_level_values(0)
        d.index = pd.DatetimeIndex(d.index).tz_localize(None).normalize() if pd.DatetimeIndex(d.index).tz is not None else pd.DatetimeIndex(d.index).normalize()
        d = d[~d.index.duplicated(keep="last")].sort_index()
        d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)].dropna(subset=["Open", "High", "Low", "Close", "Volume"])
        if len(d):
            temiz[str(s)] = d
    tak = pd.DatetimeIndex(sorted(set().union(*[d.index for d in temiz.values()])))
    ay_sonu = pd.Series(tak, index=tak).groupby(tak.to_period("M")).max()
    sonuc = []
    seri = J["seriler"]
    for ay in TD_ESIK["yeniden"]["ay"]:
        p_tut = pd.Period(ay, "M"); p_f = p_tut - 1; t = ay_sonu[p_f]
        rows = []
        for s in sorted(temiz):
            d = temiz[s]
            if t not in d.index:
                continue
            k = d.index.get_loc(t)
            if k + 1 >= len(d) or tak.get_loc(d.index[k + 1]) - tak.get_loc(t) > 10:
                continue
            nxt = d[(d.index.to_period("M") == p_tut)]
            r = nxt.Close.iloc[-1] / d.Close.iloc[k] - 1 if len(nxt) else np.nan
            mom = d.Close.iloc[k - 21] / d.Close.iloc[k - 252] - 1 if k >= 252 else np.nan
            rows.append((s, mom, r))
        T = pd.DataFrame(rows, columns=["sembol", "MOM", "r"])
        piy = float(T.r.mean())
        Tm = T[np.isfinite(T.MOM)].copy()
        Tm["pct"] = Tm.MOM.rank(method="first", pct=True); Tm["onluk"] = np.clip(np.ceil(Tm.pct * 10).astype(int), 1, 10)
        fark = float(Tm[Tm.onluk == 10].r.mean() - Tm[Tm.onluk == 1].r.mean())
        for ad, deger in (("ABD|tum|r|MOM|D10-D1|EW", fark), ("ABD|tum|r|PIYASA|-|EW", piy)):
            kod = seri.get(ad, {}).get(str(p_tut))
            sonuc.append({"seri": ad, "ay": str(p_tut), "elle": deger, "kod": kod,
                          "tutar": bool(kod is not None and np.isfinite(deger) and abs(deger - kod) < 1e-9)})
    fr = td_french_elle(J)
    return {"satir": sonuc, "french": fr, "tutar": all(x["tutar"] for x in sonuc) and all(x["tutar"] for x in fr)}


# French ham satırlarından elle (ayrıştırıcı kullanılmadan): dosya, ay, ilk eşleşme (aylık VW bölümü önce gelir), hesap, seri
TD_FRENCH_ELLE: List[Tuple[str, str, str, str]] = [
    ("F-F_Momentum_Factor_CSV.zip", "202003", "c[0]", "US_MOM"),
    ("F-F_Research_Data_Factors_CSV.zip", "201811", "c[0] + c[3]", "US_MKT"),
    ("10_Portfolios_Prior_12_2_CSV.zip", "202106", "c[9] - c[0]", "US_P12_VW_FARK"),
    ("Europe_Mom_Factor_CSV.zip", "201912", "c[0]", "EU_WML"),
]


def td_french_elle(J: Dict[str, Any], kl: Optional[str] = None) -> List[Dict[str, Any]]:
    out = []
    for dosya, ay, hesap, seri in TD_FRENCH_ELLE:
        try:
            z = zipfile.ZipFile(os.path.join(kl or TD_YOL["ref"], dosya))
            metin = z.read([n for n in z.namelist() if n.lower().endswith(".csv")][0]).decode("latin-1")
            satir = next(s for s in metin.splitlines() if re.match(rf"^\s*{ay}\s*,", s))   # Avrupa dosyalarında '201912    ,2.45'
            c = [float(x) for x in satir.strip().split(",")[1:]]
            elle = {"c[0]": c[0], "c[0] + c[3]": c[0] + c[3] if len(c) > 3 else float("nan"), "c[9] - c[0]": c[9] - c[0] if len(c) > 9 else float("nan")}[hesap] / 100
            kod = J["ref_seriler"].get(seri, {}).get(f"{ay[:4]}-{ay[4:]}")
            out.append({"dosya": dosya, "satir": satir.strip()[:120], "hesap": hesap, "seri": seri, "ay": f"{ay[:4]}-{ay[4:]}", "elle": elle,
                        "kod": kod, "tutar": bool(kod is not None and abs(elle - kod) < 1e-12)})
        except Exception as ex:   # ham dosya okunamazsa satır TUTMADI olarak kalır
            out.append({"dosya": dosya, "ay": ay, "seri": seri, "hata": f"{type(ex).__name__}: {ex}", "tutar": False})
    return out


# ================================================================ 6) KAPI, ÖN KAYIT
def td_sha_simdi(veri: Optional[str] = None, kl: Optional[str] = None) -> Dict[str, str]:
    v = veri or TD_YOL["veri"]
    out = {"TD_ESIK_SHA": td_esik_sha(), "TD_KOD_SHA": OS._os_sha_dosya(TD_YOL["kod"]),
           "OS_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_TD, "OLCU_SINAMA.py")), "OC_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_TD, "ORTAK_CETVEL.py")),
           "KASA_KOD_SHA": OS._os_sha_dosya(os.path.join(KOK_TD, "KASA.py")), "IS_TANIMI_SHA": OS._os_sha_dosya(TD_YOL["is_tanimi"]),
           "OS_SINIR_SHA": OS._os_sha_dosya(TD_YOL["os_sinir"])}
    for p in ("ABD", "AVR"):
        out[f"V_{p}_SHA"] = OS._os_sha_dosya(os.path.join(v, f"V_{p}.pkl"))
    for k in ("ref_kesik", "yahoo_kesik"):
        y = _td_yol(k, kl)
        if os.path.exists(y):
            out[f"{k.upper()}_SHA"] = OS._os_sha_dosya(y)
    return out


def td_onkayit_metni(veri: Optional[str] = None, kl: Optional[str] = None) -> str:
    td_kasa_kapi(veri, kl)
    sh = td_sha_simdi(veri, kl); kod_git = OS._os_git_islenmis(TD_YOL["kod"])
    dur = json.load(open(_td_yol("ref_durum", kl), encoding="utf-8"))
    L = [f"# TEZGÂH DOĞRULAMA — ÖN KAYIT ({_td_simdi()})", "",
         f"Sürüm: {TD_SURUM}. İş tanımı: arastirma_cikti/tezgah_dogrulama/TEZGAH_DOGRULAMA_IS_TANIMI.md (sha {sh['IS_TANIMI_SHA']}).",
         f"Kod: TEZGAH_DOGRULAMA.py git {kod_git['commit']} {kod_git['commit_zamani']}. Bu dosya koşudan ÖNCE commit edilir; td_kapi git kaydını, "
         "değişmemişliği, sha'ları ve kontrol tablosunu denetler. İz aranmaz; yalnız doğrulama. Bizim seriler henüz HESAPLANMADI (referans "
         "indirildi ve ayrıştırıldı; bizim panel / portföy koşusu ön kayıttan sonra).", "",
         "## 1. HÜKÜM KURALI (iş tanımından AYNEN)", "", TD_ESIK["hukum"]["metin"], "",
         f"Yorum (kodda): {TD_ESIK['hukum']['yorum']}.", "",
         "## 2. SONUÇ KURALI (tek cümle)", "", TD_ESIK["sonuc"]["kural"], "",
         "## 3. ÇİFTLER (önceden yazılı)", "", "| kod | bizim seri | referans | piyasa | açıklama |", "|---|---|---|---|---|"]
    for k, b, r, p, a in TD_CIFT:
        L.append(f"| {k} | `{_ad(b)}` | `{r}` | {'E' if p else 'H'} | {a} |")
    L += ["", f"Teşhis sürümleri (her ana çift için, hükümden bağımsız hep hesaplanır): {TD_ESIK['teshis']}.",
          "Bilgi: ABD MOM ve STREV onluk seviyeleri D1..D10 (EW vs French EW, LQ vs French VW; piyasa eşiği).", "",
          "## 4. TANIMLAR (TD_ESIK)", "", "```json", json.dumps(TD_ESIK, ensure_ascii=False, indent=1), "```", "",
          "## 5. REFERANS KAYNAK VE ERİŞİM", "", f"İndirme zamanı {dur.get('zaman')}; yedek: {dur.get('yedek') or 'kullanılmadı (French açıldı)'}.", "",
          "| dosya | durum | bayt | sha256 |", "|---|---|---|---|"]
    for ad, d in dur["french"].items():
        L.append(f"| {ad} | {d.get('durum')} | {d.get('bayt', '-')} | `{d.get('sha', '-')}` |")
    L += ["", f"Yahoo (E2 hisseleri + EURUSD=X): {dur['yahoo'].get('durum')}; sembol {dur['yahoo'].get('sembol', '-')}; en geç "
          f"{dur['yahoo'].get('en_gec', '-')}; eksik {dur['yahoo'].get('eksik', '-')}.", "",
          "Referans serileri (kesik 2023-12): " + "; ".join(f"{k} {v['ilk']}..{v['son']}" for k, v in list(dur["ref_seri"].items())[:8]) + " ...", "",
          "## 6. SHA", "", "| ad | sha256 |", "|---|---|"]
    for k, v in sh.items():
        L.append(f"| {k} | `{v}` |")
    L += ["", "## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
          "|---|---|---|---|"]
    try:
        import IZ_KARNE as _IK
        adlar = {k["kod"]: k.get("madde", k.get("ad", "")) for k in _IK.IK_KONTROL}
    except Exception:   # IZ_KARNE okunamazsa ad boş kalır; kapı yine denetler
        adlar = {}
    for k, (y, kn) in TD_KONTROL.items():
        L.append(f"| {k} | {adlar.get(k, '')} | {y} | {kn} |")
    return "\n".join(L) + "\n"


def td_onkayit_yaz(veri: Optional[str] = None, uzerine: bool = False) -> str:
    y = _td_yol("onkayit")
    if os.path.exists(y) and not uzerine:
        raise TDHata(f"ön kayıt zaten var: {y} (--uzerine-yaz)")
    return _td_yaz(y, td_onkayit_metni(veri), "ön kayıt")


def td_kapi(onkayit: Optional[str] = None, git: bool = True, kontrol: bool = True, veri: Optional[str] = None) -> Dict[str, Any]:
    yol = onkayit or _td_yol("onkayit")
    if not os.path.exists(yol):
        raise TDHata(f"ön kayıt yok: {yol}")
    kasa = td_kasa_kapi(veri)
    metin = open(yol, encoding="utf-8").read(); sh = td_sha_simdi(veri); bozuk = []
    for k in ("TD_ESIK_SHA", "TD_KOD_SHA", "OS_KOD_SHA", "V_ABD_SHA", "V_AVR_SHA", "REF_KESIK_SHA", "YAHOO_KESIK_SHA", "OS_SINIR_SHA"):
        m = re.search(rf"\|\s*{k}\s*\|\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != sh.get(k):
            bozuk.append(k)
    if bozuk:
        raise TDHata(f"ön kayıt sha tutmuyor: {bozuk} -> DURDU")
    g = OS._os_git_islenmis(yol) if git else {"commit": "-", "commit_zamani": "-"}
    kk = None
    if kontrol:
        import IZ_KARNE as _IK
        kk = _IK.ik_kontrol_kapisi(yol)
    return {"onkayit": yol, "git": g, "kasa": kasa, "sha": sh, "kontrol": bool(kk["gecti"]) if kk else None}


# ================================================================ 7) KOŞU
def _td_seri_json(S: Dict[str, pd.Series]) -> Dict[str, Dict[str, float]]:
    return {k: {str(p): (float(x) if np.isfinite(x) else None) for p, x in v.items()} for k, v in S.items()}


def td_kos(veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t0 = time.time(); bas = _td_simdi()
    kp = td_kapi(git=git, kontrol=kontrol, veri=veri)
    R, Y = td_ref_yukle()
    fx = td_eurusd_ay(Y)
    sinir = json.load(open(TD_YOL["os_sinir"], encoding="utf-8"))["sinir"]
    S: Dict[str, pd.Series] = {}; E1: Dict[str, Any] = {}; E2: Dict[str, Any] = {}; en_gec: Dict[str, str] = {}; nt: Dict[str, Any] = {}
    for p in ("ABD", "AVR"):
        Vd = OS.os_veri(p, veri)
        en_gec[p] = str(max(d.index.max() for d in Vd["V"].values()).date())
        Pn = OS.os_panel(Vd, sinir[p])
        Z = td_kesit(Pn, Vd, fx if p == "AVR" else None)
        nt[p] = {"hisse": len(Vd["V"]), "kesit_satir": int(len(Z)), "havuz_satir": int(Z.havuz.sum()), "not": Vd.get("not", [])[-3:],
                 "fx": "EURUSD=X Yahoo ay son kuru" if (p == "AVR" and fx is not None) else ("YOK: AVR USD yerine EUR" if p == "AVR" else "-")}
        S.update(td_bizim_seriler(Z, p))
        E1[p] = td_e1(Pn)
        if p == "ABD":
            E2 = td_e2(Vd["V"], Y)
        del Pn, Z
        tdlog.info("%s seriler hazır (%.0f sn)", p, time.time() - t0)
    K = td_cift_listesi(S)
    for c in K:
        if c["biz"] not in S or c["ref"] not in R:
            c["sonuc"] = {"n": 0, "hukum": "ÖLÇÜLEMEDİ", "neden": "bizim seri yok" if c["biz"] not in S else "referans erişilemedi"}
        else:
            c["sonuc"] = td_karsilastir(S[c["biz"]], R[c["ref"]], c["piyasa"])
    RD = td_ref_donem(R)
    # bizim seri dönem ortalamaları (ana çiftler)
    BD = []
    for k, b, r, p_, a in TD_CIFT:
        s = S.get(b); sat = {"kod": k, "seri": b}
        for ad, (x, y) in {"2016-23": TD_ESIK["pencere"]["ref_yeni"], **TD_ESIK["pencere"]["alt"]}.items():
            v = s[(s.index >= pd.Period(x, "M")) & (s.index <= pd.Period(y, "M"))].to_numpy(float) if s is not None else np.array([])
            sat[ad] = {"n": int(np.isfinite(v).sum()), "ort": float(np.nanmean(v)) if np.isfinite(v).any() else float("nan"), "t": _td_t(v)}
        BD.append(sat)
    SON = td_sonuc(K, RD, S)
    J: Dict[str, Any] = {"surum": TD_SURUM, "esik_sha": td_esik_sha(), "kapi": OS._os_temizle({"git": kp["git"], "kontrol": kp["kontrol"], "sha": kp["sha"]}),
                         "bas": bas, "bit": None, "veri_not": nt, "en_gec": en_gec, "ciftler": K, "ref_donem": RD, "biz_donem": BD, "sonuc": SON,
                         "e1": E1, "e2": E2, "seriler": _td_seri_json({k: v for k, v in S.items() if not k.endswith("|N")}),
                         "seri_n": _td_seri_json({k: v for k, v in S.items() if k.endswith("|N") and "|havuz|r|" in k}),
                         "ref_seriler": _td_seri_json({k: v[v.index >= pd.Period("2000-01", "M")] for k, v in R.items()
                                                       if k in {c["ref"] for c in K}})}
    J["ref_en_gec"] = max(str(v.index.max()) for v in R.values())
    J["yeniden"] = td_yeniden(J, veri)
    durum = json.load(open(_td_yol("ref_durum"), encoding="utf-8"))
    J["french_ham_ornek"] = durum.get("french_ham_ornek", {}); J["ref_durum"] = {k: v for k, v in durum.items() if k != "french_ham_ornek"}
    J["bit"] = _td_simdi(); J["sure_sn"] = round(time.time() - t0)
    _td_yaz(_td_yol("json"), json.dumps(OS._os_temizle(J), ensure_ascii=False, default=OS._os_json), "json")
    if not J["yeniden"]["tutar"]:
        tdlog.error("YENİDEN ÜRETİM TUTMADI: %s", J["yeniden"])
    return J


# ================================================================ 8) RAPOR
def _p(x: Any, n: int = 2) -> str:
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "-"
    return f"{x:+.{n}f}".replace(".", ",")


def _ad(s: str) -> str:
    """Seri adı markdown tablosunda: '|' sütun ayırıcısıyla karışmasın."""
    return str(s).replace("|", " · ")


def _y(x: Any, n: int = 2) -> str:
    """ondalık getiri -> yüzde (işaretli)."""
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return "-"
    return f"{x * 100:+.{n}f}".replace(".", ",")


def td_rapor(J: Optional[Dict[str, Any]] = None) -> str:
    J = J or json.load(open(_td_yol("json"), encoding="utf-8"))
    K = J["ciftler"]; ana = [c for c in K if c["tur"] == "ANA"]
    L = [f"# TEZGÂH DOĞRULAMA — RAPOR ({J['bit']})", "",
         f"{J['surum']}. Ön kayıt TEZGAH_DOGRULAMA_ON_KAYIT.md (git {J['kapi']['git']['commit']} {J['kapi']['git']['commit_zamani']}); koşu "
         f"{J['bas']} .. {J['bit']} ({J['sure_sn']} sn). Hisse verisi yalnız KASA açık kısmı (kesik 2023-12-31); referans French veri "
         f"kütüphanesi ({'yedek: ' + J['ref_durum']['yedek'] if J['ref_durum'].get('yedek') else 'yedek kullanılmadı'}), 2023-12'de kesik.", "",
         "## 1. TEK SAYFA ÖZET", "",
         f"**Sonuç: {J['sonuc']['cumle']}**", ""] + [f"- {x}" for x in td_okuma(J)] + ["",
         "Seri başına hüküm (karşılaştırma penceresi: tutma ayı 2016-01..2023-12; kural: korelasyon >= 0,70 ve işaret uyumu >= %70 DOĞRU, "
         "piyasa serisinde korelasyon >= 0,90; 0,40-0,70 KISMEN; < 0,40 UYUŞMUYOR):", "",
         "| kod | seri | ay | Pearson | Spearman | işaret uyumu | eğim | hüküm |", "|---|---|---|---|---|---|---|---|"]
    for c in ana:
        s = c["sonuc"]
        L.append(f"| {c['kod']} | {c['aciklama']} | {s.get('n', 0)} | {_p(s.get('pearson'))} | {_p(s.get('spearman'))} | "
                 f"{'-' if s.get('isaret') is None else f'%{s['isaret'] * 100:.0f}'} | {_p(s.get('egim'))} | **{s['hukum']}** |")
    L += ["", "Referansın KENDİ dönem ortalamaları (aylık, %; t = ort / (sd / kök n)): 'bu dönemde yayımlanmış veride de zayıf mıydı?'", "",
          "| referans | 2000-15 ort (t) | 2016-23 ort (t) | 2016-19 ort (t) | 2020-23 ort (t) |", "|---|---|---|---|---|"]
    for r in J["ref_donem"]:
        if "2000-15" not in r:
            L.append(f"| {r['seri']} | erişilemedi | | | |"); continue
        L.append(f"| {r['seri']} | " + " | ".join(f"{_y(r[k]['ort'])} ({_p(r[k]['t'])}, n {r[k]['n']})" for k in ("2000-15", "2016-23", "d1", "d2")) + " |")
    L += ["", "Bizim ana serilerin aynı dönem ortalamaları:", "", "| kod | 2016-23 ort (t) | 2016-19 | 2020-23 |", "|---|---|---|---|"]
    for r in J["biz_donem"]:
        L.append(f"| {r['kod']} | " + " | ".join(f"{_y(r[k]['ort'])} ({_p(r[k]['t'])}, n {r[k]['n']})" for k in ("2016-23", "d1", "d2")) + " |")
    L += ["", "Okuma: evren bugün işlem gören hisselerdir (batan yok); bu, seviye getirilerini yukarı, alt onlukları (MOM alt, STREV alt) yukarı "
          "çeker: MOM farkı aşağı, STREV farkı yukarı yanlı okunur. Korelasyon (zamanlama) bu yanlılıktan az etkilenir; ortalama (seviye) çok etkilenir.", "",
          "## 2. BÜTÜN ÇİFTLER (ana + teşhis)", "",
          "| kod | tür | bizim | referans | ay | Pearson | Spearman | işaret | eğim | biz ort (t) | ref ort (t) | d1 r | d2 r | hüküm |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in K:
        if c["tur"] == "BİLGİ":
            continue
        s = c["sonuc"]; al = s.get("alt", {})
        L.append(f"| {c['kod']} | {c['tur']} | `{_ad(c['biz'])}` | `{c['ref']}` | {s.get('n', 0)} | {_p(s.get('pearson'))} | {_p(s.get('spearman'))} | "
                 f"{'-' if s.get('isaret') is None else f'%{s['isaret'] * 100:.0f}'} | {_p(s.get('egim'))} | {_y(s.get('biz_ort'))} ({_p(s.get('biz_t'))}) | "
                 f"{_y(s.get('ref_ort'))} ({_p(s.get('ref_t'))}) | {_p(al.get('d1', {}).get('pearson'))} | {_p(al.get('d2', {}).get('pearson'))} | {s['hukum']} |")
    L += ["", "### Onluk seviyeleri (bilgi; piyasa eşiği)", "", "| kod | ay | Pearson | işaret | eğim | biz ort | ref ort | hüküm |", "|---|---|---|---|---|---|---|---|"]
    for c in K:
        if c["tur"] != "BİLGİ":
            continue
        s = c["sonuc"]
        L.append(f"| {c['kod']} | {s.get('n', 0)} | {_p(s.get('pearson'))} | {'-' if s.get('isaret') is None else f'%{s['isaret'] * 100:.0f}'} | "
                 f"{_p(s.get('egim'))} | {_y(s.get('biz_ort'))} | {_y(s.get('ref_ort'))} | {s['hukum']} |")
    L += ["", "## 3. EN ÇOK AYRIŞAN 10 AY (ana çiftler; % puan)", ""]
    for c in ana:
        s = c["sonuc"]
        if not s.get("ayrisan"):
            continue
        L.append(f"- **{c['kod']}** ({c['aciklama']}): " + "; ".join(f"{a['ay']} biz {_y(a['biz'])} / ref {_y(a['ref'])}" for a in s["ayrisan"]))
    L += ["", "## 4. EK DOĞRULAMALAR", "", "### E1 gece / gün içi (gün ortalaması baz puan; yıllık toplam %)", "",
          "| pazar | yıl | gün | hisse | gece EW bp | gün içi EW bp | gece EW yıl % | gün içi EW yıl % | gece LQ bp | gün içi LQ bp | gece LQ yıl % | gün içi LQ yıl % |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p, rows in J["e1"].items():
        for r in rows:
            L.append(f"| {p} | {r['yil']} | {r['gun']} | {r['hisse_ort']:.0f} | {_p(r['gece_ew_bp'])} | {_p(r['gunici_ew_bp'])} | {_p(r['gece_ew_yil_pct'], 1)} | "
                     f"{_p(r['gunici_ew_yil_pct'], 1)} | {_p(r['gece_lq_bp'])} | {_p(r['gunici_lq_bp'])} | {_p(r['gece_lq_yil_pct'], 1)} | {_p(r['gunici_lq_yil_pct'], 1)} |")
    e2 = J["e2"]
    L += ["", "### E2 veri kipi (bizim ay sonu kapanış getirisi vs Yahoo Adj Close / Close; 2016-01..2023-12)", ""]
    if e2.get("durum") != "açıldı":
        L.append(f"E2: {e2.get('durum')}")
    else:
        L += [f"{e2['gecen']} / {e2['n']} hissede Pearson(bizim, Adj Close) >= 0,99; en düşük {_p(e2['min_r_adj'], 4)}; medyan aylık fark (bizim - Adj) "
              f"{_p(e2['med_fark_adj_bp'])} bp, (bizim - Close) {_p(e2['med_fark_close_bp'])} bp.", "",
              "| hisse | ay | r(Adj) | r(Close) | fark Adj bp | fark Close bp | maks |fark Adj| % |", "|---|---|---|---|---|---|---|"]
        for h in e2["hisse"]:
            if "r_adj" in h:
                L.append(f"| {h['sembol']} | {h['n']} | {h['r_adj']:.4f} | {h['r_close']:.4f} | {_p(h['fark_adj_bp'])} | {_p(h['fark_close_bp'])} | {h['maks_fark_adj_pct']:.2f} |")
    L += ["", "## 5. YENİDEN ÜRETİM: " + ("TUTTU" if J["yeniden"]["tutar"] else "TUTMADI"), "",
          "Ham V_ABD.pkl'den düz pandas (OC / OS kodu kullanılmadan):", "", "| seri | tutma ayı | elle | kod | tutar |", "|---|---|---|---|---|"]
    for r in J["yeniden"]["satir"]:
        L.append(f"| `{_ad(r['seri'])}` | {r['ay']} | {r['elle']:.10f} | {('-' if r['kod'] is None else f'{r['kod']:.10f}')} | {'E' if r['tutar'] else 'H'} |")
    L += ["", "French ham satırından elle (ayrıştırıcı kullanılmadan; değerler ondalık):", "", "| dosya | ay | ham satır | hesap | elle | kod | tutar |",
          "|---|---|---|---|---|---|---|"]
    for r in J["yeniden"].get("french", []):
        L.append(f"| {r['dosya']} | {r['ay']} | `{r.get('satir', r.get('hata', ''))}` | {r.get('hesap', '-')} | "
                 f"{('-' if r.get('elle') is None else f'{r['elle']:.6f}')} | {('-' if r.get('kod') is None else f'{r['kod']:.6f}')} | {'E' if r['tutar'] else 'H'} |")
    L += ["", "## 6. EN GEÇ TARİH", "", f"- hisse verisi en geç bar: {J['en_gec']}", f"- referans en geç ay: {J['ref_en_gec']}",
          f"- Yahoo en geç: {J['ref_durum'].get('yahoo', {}).get('en_gec', '-')}", "",
          "## 7. VERİ NOTU", ""]
    for p, v in J["veri_not"].items():
        L.append(f"- {p}: {v['hisse']} hisse, kesit satırı {v['kesit_satir']}, havuz satırı {v['havuz_satir']}; kur: {v['fx']}")
    L += ["", "## 8. HATA (koşu sırasında ve sonrasında bulunan; IK_HATA'ya ana model yazar)", ""]
    L += [f"- {h}" for h in (J.get("hata") or ["yok"])]
    L += ["", "## 9. KONTROL LİSTESİ (ön kayıttaki tablo aynen)", "", "| Kod | Yanıt | Kanıt |", "|---|---|---|"]
    L += [f"| {k} | {y} | {kn} |" for k, (y, kn) in TD_KONTROL.items()]
    return "\n".join(L) + "\n"


def td_okuma(J: Dict[str, Any]) -> List[str]:
    """Düz Türkçe tek sayfa maddeleri (sayılar json'dan; yorum cümlesi sayıdan ayrı)."""
    K = {c["kod"]: c for c in J["ciftler"]}; rd = {r["seri"]: r for r in J["ref_donem"]}
    def s(k: str) -> str:
        x = K[k]["sonuc"]
        return f"{x['hukum']} (korelasyon {_p(x.get('pearson'))}, işaret uyumu %{(x.get('isaret') or 0) * 100:.0f})"
    def r(k: str, d: str) -> str:
        x = rd.get(k, {}).get(d)
        return "-" if not x else f"ayda {_y(x['ort'])}% (t {_p(x['t'])})"
    return [f"Piyasa: ABD eşit ağırlıklı {s('A1')}, işlem değeri ağırlıklı {s('A2')}; Avrupa {s('E1')}.",
            f"Momentum (12-1): French Mom ile {s('A5')}; onluk farkı ağırlıklı {s('A4')}, eşit ağırlıklı {s('A3')}; Avrupa WML ile {s('E3')}.",
            f"Kısa vadeli dönüş: French ST_Rev ile {s('A8')}; onluk farkı ağırlıklı {s('A7')}, eşit ağırlıklı {s('A6')}.",
            f"Yayımlanmış ABD momentumu (French Mom): 2000-15 {r('US_MOM', '2000-15')}, 2016-23 {r('US_MOM', '2016-23')}. ST_Rev: 2000-15 "
            f"{r('US_STREV', '2000-15')}, 2016-23 {r('US_STREV', '2016-23')}. Avrupa WML: 2000-15 {r('EU_WML', '2000-15')}, 2016-23 {r('EU_WML', '2016-23')}.",
            f"Veri kipi (E2): {J['e2'].get('gecen', '-')} / {J['e2'].get('n', '-')} büyük hissede bizim aylık getiri = Yahoo ayarlı kapanış "
            f"(en düşük korelasyon {_p(J['e2'].get('min_r_adj'), 4)}; medyan fark {_p(J['e2'].get('med_fark_adj_bp'))} bp): fiyatlar temettü dahil ayarlı.",
            "Evren bugün yaşayan hisseler: batan hisseler yok, bu yüzden alt onluklar (kaybedenler) olduğundan iyi görünür; korelasyon (ay ay "
            "zamanlama) bundan az, ortalama (seviye) çok etkilenir."]


TD_HATA: List[str] = [
    "H-TD1 (doğrulama kodu, koşu 1): td_french_elle Avrupa dosyasında ay satırını 'YYYYMM,' önekiyle aradı; Avrupa dosyalarında ay kodundan "
    "sonra boşluk var ('201912    ,2.45') -> satır bulunamadı (StopIteration), yeniden üretim TUTMADI göründü (bizim 6 hücre ve French 3 "
    "satır tutmuştu). Ayrıştırıcı td_french_ayristir etkilenmedi (parçaları strip ediyor; EU_WML serisi doğru). Düzeltme: düzenli ifade "
    "'^\\s*YYYYMM\\s*,'. SAPMA: kod sha ön kayıttan farklı; ölçüm YENİDEN KOŞULMADI, yalnız yeniden üretim adımı 'yeniden' komutuyla "
    "koşu json'u üzerinde (KASA kapısından sonra) yeniden koşuldu; hükümler ve seriler koşu 1'in aynısı.",
    "H-TD2 (rapor üreteci, koşu 1): ilk rapor HATA / KONTROL LİSTESİ bölümlerini ve düz Türkçe özet maddelerini basmıyordu (iş tanımı "
    "istiyordu). Yalnız gösterim eklendi; sayılar json'dan, değişmedi.",
    "GÖZLEM (hata değil): 'tum' maskesinde (OS havuz süzgeci yok: likidite alt %20 ve bölünme şüpheli hisse-aylar dahil) STREV onluk farkı "
    "EW ayda +3,62% (A6.2, French ile korelasyon 0,30) — havuz dışı hisse-aylarda bayat / ayarsız fiyat sıçramaları alt-üst onluk farkını "
    "şişiriyor; havuz süzgeci bunu dışlıyor (A6: 0,74). Ayrıca araştırılmadı.",
]


def td_yeniden_kos(veri: Optional[str] = None) -> Dict[str, Any]:
    """Koşu json'u üzerinde YALNIZ yeniden üretim adımı (H-TD1 düzeltmesi; SAPMA kaydıyla). Ölçüm yeniden koşulmaz."""
    td_kasa_kapi(veri)
    J = json.load(open(_td_yol("json"), encoding="utf-8"))
    eski = J.get("yeniden")
    J["yeniden"] = td_yeniden(J, veri)
    J["yeniden_koşu1"] = eski
    J["sapma"] = {"zaman": _td_simdi(), "kod_sha": OS._os_sha_dosya(TD_YOL["kod"]),
                  "metin": "yeniden üretim adımı düzeltilmiş kodla json üzerinde yeniden koşuldu (H-TD1); ölçüm / seriler / hükümler koşu 1"}
    J["hata"] = list(TD_HATA)
    _td_yaz(_td_yol("json"), json.dumps(OS._os_temizle(J), ensure_ascii=False, default=OS._os_json), "json")
    return J


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_td(_once=_CK_ONCE_TD, _dosya="TEZGAH_DOGRULAMA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_TD", "_CK_KAYIT", "_cakisma_kontrol_td", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "copy", "_dt", "zipfile", "io",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "OS")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_td()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=TD_SURUM)
    ap.add_argument("komut", choices=["ref", "onkayit", "kos", "yeniden", "rapor", "sha", "kapi"])
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    try:
        if a.komut == "ref":
            print(json.dumps(OS._os_temizle({k: v for k, v in td_ref_indir().items() if k != "french_ham_ornek"}), ensure_ascii=False, indent=1,
                             default=OS._os_json))
        elif a.komut == "onkayit":
            print(td_onkayit_yaz(a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kapi":
            print(json.dumps(OS._os_temizle(td_kapi(veri=a.veri)), ensure_ascii=False, indent=1, default=OS._os_json))
        elif a.komut == "kos":
            J_ = td_kos(a.veri)
            print(_td_yaz(_td_yol("rapor"), td_rapor(J_), "rapor"))
            print(J_["sonuc"]["cumle"]); print("yeniden üretim:", J_["yeniden"]["tutar"])
        elif a.komut == "yeniden":
            J_ = td_yeniden_kos(a.veri)
            print(_td_yaz(_td_yol("rapor"), td_rapor(J_), "rapor")); print("yeniden üretim:", J_["yeniden"]["tutar"])
        elif a.komut == "rapor":
            print(_td_yaz(_td_yol("rapor"), td_rapor(), "rapor"))
        else:
            print(json.dumps(td_sha_simdi(a.veri), indent=1))
    except TDHata as ex:
        tdlog.error("%s", ex); sys.exit(1)
