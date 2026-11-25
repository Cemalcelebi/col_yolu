"""UC_IZ2 — ÜÇ FİYAT DIŞI İZ (sektör rüzgârı R, bilanço tepkisi B, içeriden alım İ) AYNI BİLANÇO OLAYINDA, ABD 2016-22 (25 Kasım 2026).

İş tanımı: arastirma_cikti/uc_iz2/UC_IZ2_IS_TANIMI.md (commit b325107; ana model). Ç225 (UC_IZ) ÖLÇÜLEMEDİ çıktı: B ve İ verisi 2022'den
başlıyordu. Bu iş SEC Form 4 (2015Q4-2022Q4) ve 8-K Item 2.02 (2015-10..2022-12) verisini indirip üç izi aynı bilanço olayında ölçer.
Keşif ölçümü (açık veri, kesik 2022-12-31). KASA AÇILMAZ; 2023+ fiyat ölçüm koduna girmez (kod en büyük tarihi assert eder).

VERİ
  V1 fiyat: TEZGAH2_VERI V_ABD2.pkl (/root/.kasa/ham/veri3) -> 2022-12-31 kesikli açık kopya (uc2_acik_kopya; UC_IZ.uc_kes ile aynı mekanik
     kesik + KASA.kasa_kapisi) -> OS.os_veri / C2.c2_panel22_al (CETVEL2 v2.2, kova sınırları cetvel2_esik_v2.2.json).
  V2 Form 4: SEC Insider Transactions Data Sets 2015q4..2022q4 (FON_IZI.FI_K30 url), A1 = FON_IZI.fi_k30_alimlar AYNEN (Form 4, kod P,
     edinme A, bildirim değeri = adet x fiyat toplamı) + değer >= FI_K30['kucuk'] (10.000 $); BİLGİ TARİHİ = FILING_DATE; ihraççı CIK
     (ISSUERCIK) SUBMISSION.tsv'den aynı erişim numarasıyla eklenir.
  V3 8-K 2.02: data.sec.gov/submissions/CIK##########.json (+ dönemle örtüşen ek sayfalar), form '8-K', items içinde '2.02',
     acceptanceDateTime (UTC 'Z' -> America/New_York). OLAY GÜNÜ t: kabul saati 16:00'dan önce ise o gün (işlem günü değilse sonraki işlem günü), 16:00 ve
     sonrası ise sonraki işlem günü. Aynı CIK'de son TUTULAN olaydan <= 20 takvim günü sonraki 2.02 atılır.
  V4 sembol -> CIK: SEC company_tickers.json (indirme günü) ile panel sembolü (Yahoo, '.' -> '-'); CIK kalıcı kimlik (bilanço ve Form 4
     CIK ile bağlanır; ticker değişimi / yeniden kullanımı etkilemez). Eşlenemeyen sembol / olay sayısı raporda.
  SEC User-Agent YALNIZ /root/.sec_ua dosyasından okunur; içeriği hiçbir çıktıya, loga, dosyaya yazılmaz. Saniyede en çok 8 istek
  (aralık 0,15 sn), 429 / 403 / 5xx'te artan bekleme ile yeniden dene. Ham SEC dosyaları repo DIŞI: /root/.kasa/ham/sec2016.

OLAY VE İZLER (UC2_ESIK; sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
  E1 bilanço günü t (P2 evreni ABD hissesi), giriş t + 1 açılış; aynı hissede bir bilanço = bir olay.
  B  EAR_t / ATRP20_{t-1} >= +1,0; EAR_t = (C_t / C_{t-1} - 1) - aynı gün aynı kova (CETVEL2 KV satırı t) eşlerinin medyan günlük getirisi
     (aynı gün E1 olayı olan hisseler hariç, >= 5 eş); ATRP20_{t-1} = son 20 geçerli barın TR ortalaması / C (t-1'de). BİLGİ: B- <= -1,0.
  İ  (t - 90, t] takvim aralığında FILING_DATE'li >= 1 A1 alımı (ihraççı CIK).
  R  KART_TUR2.k2_d9_durum -> D9_YENIDEN.d9_satir 'c' (KT10 aynen) t günü.
  N = R + B + İ.  E2 (BİLGİ): KT02 dip olayı (UC_IZ.uc_dip_ham) + gerçek B (son 15 geçerli barda E1 günü ve o gün B) + gerçek İ.
ÖLÇÜ: R15 (karar), R60 (karar), R30 (bilgi); CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı kova, >= 5 eş, aynı gün E1 olayları dışı);
  FARK, SIRA, ÜST10 / ALT10; taban UC_IZ.uc_taban (formül) ve UC_IZ.uc_plasebo (200 tohum); hücre UC_IZ.uc_hucre (C2.c2_hucre +
  MU.mu_sira_boot + MU.mu_hukum); karar UC_IZ.uc_iz_karar / uc_birlikte mantığı (iki ufukta ayrı). Hücreler ABD d1619 / d2022.

Komut:  python UC_IZ2.py sec_form4        Form 4 zip indir (2015q4..2022q4) -> A1 tablosu + 2022 sağlaması (k30_alim.pkl)
        python UC_IZ2.py sec_8k           company_tickers + submissions indir -> 8-K 2.02 tablosu
        python UC_IZ2.py acik             V_ABD2 / V_AVR2 -> 2022-12-31 kesikli açık kopya (/tmp/uc_iz2/acik)
        python UC_IZ2.py hazirla          olaylar + bayraklar + R60 güç eğrisi + getirisiz sayım + doğrulamalar -> uc_iz2_hazirlik.json
        python UC_IZ2.py kos              kapı (kontrol + ön kayıt sha + commit) -> ölçüm -> satır / sonuç
        python UC_IZ2.py sha              kod / eşik sha
Colab:  exec(open('UC_IZ2.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Mevcut modüller (UC_IZ, CETVEL2, KART_TUR2, FON_IZI, MACD_UYUM, OLCU_SINAMA, KASA) DEĞİŞTİRİLMEZ; içe alınır. Komisyon yok.
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_UC2 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402
import zipfile  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_UC2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_UC2 not in sys.path:
    sys.path.insert(0, KOK_UC2)

u2log = logging.getLogger("col.uc_iz2")
if not u2log.handlers:
    _u2_h = logging.StreamHandler(sys.stderr)
    _u2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s uc_iz2: %(message)s", "%H:%M:%S"))
    u2log.addHandler(_u2_h)
    u2log.setLevel(logging.INFO)
    u2log.propagate = False


class UC2Hata(RuntimeError):
    """Durdurucu hata: veri yok, SEC erişimi, sağlama tutmadı, kesik aşımı, kontrol / ön kayıt kapısı, ikinci koşu."""


UC2_SURUM = "UC_IZ2 v1.0 (2026-11-25): R (KT10) + B (8-K 2.02 tepkisi) + İ (Form 4 A1) bilanço olayında; ABD 2016-22; R15 + R60 karar"
_HAM = os.environ.get("UC2_HAM", "/root/.kasa/ham/sec2016")
UC2_YOL = {"cikti": os.path.join(KOK_UC2, "arastirma_cikti", "uc_iz2"), "kod": os.path.join(KOK_UC2, "UC_IZ2.py"),
           "ham": _HAM, "form345": os.path.join(_HAM, "form345"), "sub": os.path.join(_HAM, "sub"),
           "veri3": os.environ.get("UC2_VERI3", "/root/.kasa/ham/veri3"), "acik": os.environ.get("UC2_ACIK", "/tmp/uc_iz2/acik"),
           "gecici": os.environ.get("UC2_GECICI", "/tmp/uc_iz2"), "veri2": os.environ.get("UC2_VERI2", "/tmp/veri2"),
           "veri_eski": os.environ.get("UC2_VERI_ESKI", "/tmp/veri"), "ua": "/root/.sec_ua",
           "ct_yedek": "/tmp/iv/secfs/company_tickers.json", "k55": "/tmp/iv/k55"}
UC2_DOSYA = {"onkayit": "UC2_IZ2_ON_KAYIT.md", "rapor": "UC_IZ2_RAPOR.md", "sonuc": "uc_iz2_sonuc.json", "hazirlik": "uc_iz2_hazirlik.json",
             "veri_json": "uc_iz2_veri.json", "satir": "uc_iz2_satir.csv.gz", "a1": "form4_a1.pkl", "k8": "k8_202.pkl",
             "ct": "company_tickers.json", "olay": "olay.pkl"}
UC2_DOSYA["onkayit"] = "UC_IZ2_ON_KAYIT.md"
UC2_KESIK = pd.Timestamp("2022-12-31")

UC2_SEC: Dict[str, Any] = {
    "form4_url": "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{c}_form345.zip",
    "ceyrekler": ["2015q4"] + [f"{y}q{q}" for y in range(2016, 2023) for q in range(1, 5)],
    "sub_url": "https://data.sec.gov/submissions/CIK{cik:010d}.json",
    "sub_ek_url": "https://data.sec.gov/submissions/{ad}",
    "ticker_url": "https://www.sec.gov/files/company_tickers.json",
    "aralik_sn": 0.15,                      # <= 6,7 istek / sn (sınır 8)
    "deneme": 6, "bekle_sn": [5, 15, 45, 90, 180, 300],
    "sub_pencere": ["2015-09-01", "2023-01-31"],   # ek sayfa bu aralıkla örtüşüyorsa indirilir
}

UC2_ESIK: Dict[str, Any] = {
    "surum": "UC2-1.0",
    "pazar": "ABD",
    "donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
    "ufuk_karar": [15, 60], "ufuk_bilgi": [30],
    "es_min": 5,
    "veri_bas": "2012-01-01",   # ölçüm kopyası başlangıcı (bellek); en uzun pencere D9 500 bar; 2016 öncesi >= 4 yıl ısınma
    "veri": "TEZGAH2 V_ABD2.pkl (yfinance auto_adjust, indirme 2026-11-25) -> tarih <= 2022-12-31 VE >= veri_bas (ölçüm); 2000.. (T2 21 sınaması)",
    "olay": {"form": "8-K", "madde": "2.02", "kabul_sinir_saat": "16:00:00", "saat_dilimi": "acceptanceDateTime UTC ('Z'; AAPL 16:30 ET duyuruları 20:30 / 21:30 Z, yaz / kış saati) -> America/New_York",
             "tekrar_gun": 20, "tekrar_kural": "aynı CIK'de son TUTULAN olay gününden <= 20 takvim günü sonraki olay atılır",
             "aralik": ["2015-10-01", "2022-12-31"], "tekil": "aynı hissede aynı gün tek olay; CETVEL2 c2_olay tekil 1 (giriş günü tekrarı yok)",
             "evren": "TEZGAH2 P2 havuzu (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1) VE CETVEL2 v2.2 havuzu (c2_olay tekil 1; giriş günü d'de)",
             "takvim": "birleşik takvim (bütün hisselerin geçerli barları): t = D0'a eşit ya da sonraki ilk takvim günü; hisse t'de geçerli bar "
                       "değilse olay düşer (huni)",
             "cok_sinif": "aynı CIK'e birden çok panel sembolü (sınıf hisseleri) eşlenirse olay yalnız en çok geçerli barı olan sembolde (eşitlikte "
                          "alfabetik ilk); bütün sınıf sembolleri o gün eş / B eşi dışında",
             "dislama": "eş (R_H, giriş günü d) ve B eşi (t günü): o gün E1 olayı olan bütün CIK'lerin bütün panel sembolleri (P2 / havuz süzgecinden "
                        "önceki E1 listesi)"},
    "B": {"esik": 1.0, "bilgi_eksi": -1.0, "atr_gun": 20, "es_min": 5,
          "tanim": "EAR_t = (C_t / C_t-1 - 1) - medyan(aynı gün, aynı CETVEL2 kova satırı t, hisse ve o günkü E1 hisseleri hariç, günlük getiri); "
                   "B = EAR_t / ATRP20_t-1 >= 1,0; ATRP20 = son 20 geçerli barın TR (önceki kapanışla) SMA'sı / C, t-1 (önceki geçerli bar); "
                   "EAR / ATRP hesaplanamayan olay (eş < 5, kova yok, t'de geçerli bar yok) ÖLÇÜM DIŞI (huni sayımı)"},
    "I": {"gun": 90, "kucuk": 10_000, "tanim": "(t - 90 takvim günü, t] aralığında FILING_DATE'li >= 1 A1 (Form 4, P, A, >= 10.000 $), ihraççı CIK"},
    "R": {"tanim": "KART_TUR2.k2_d9_durum(Vd, 'ABD', K2_ESIK['d9_olay_bas']) -> D9_YENIDEN.d9_satir 'c' olay günü t (KT10 aynen)"},
    "E2": {"pencere_bar": 15, "tanim": "UC_IZ.uc_dip_ham KT02 olayı; gerçek B = son 15 geçerli barda (t dahil) B = 1 olan E1 günü; gerçek İ = "
                                       "(t - 90, t] A1; R = KT10 'c'; yalnız BİLGİ (Ç225 kıyas satırı)"},
    "ust_pay": 0.90, "alt_pay": 0.10,
    "taban": "UC_IZ.uc_taban (formül) ve UC_IZ.uc_plasebo AYNEN (UC_ESIK: 200 tohum, kök 25112026, aynı gün aynı kova rastgele üye, E1 hariç)",
    "plasebo_tohum": 200,
    "n_min": 30, "guc_esik": 0.80, "bh_q": 0.10,
    "iz": ["R", "B", "I"],
    "guc": {"r15": "cetvel2_guc_v2.2.json ABD x hücre x 15 (aynen)", "r30": "cetvel2_guc_v2.2.json ABD x hücre x 30 (bilgi)",
            "r60": "cetvel2_guc_v2.2.json'da H = 60 YOK -> aynı yöntem (C2.c2_hazirlik22: DS ANA olayları c2_ds_olay_acik_v2.2, c2_olay tekil 60, "
                   "c2_es, C2.c2_guc_egri, tohum_ek pazar 0 x hücre) bu panelde hazırlıkta hesaplanır; sha ön kayıtta", "delta": 0.02},
    "karar_kurali": (
        "Her ufuk (R60, R15) ayrı: YÖN TUTARLI(iz) <=> iki karar hücresinin (ABD d1619, ABD d2022) ikisinde de FARK(iz var) > 0 VE "
        "FARK(var) - FARK(yok) > 0 VE (ÜST10 - taban_formül) > 0 VE (ÜST10 - taban_plasebo) > 0. TUTAR <=> ayrıca iki hücrede c2 hükmü "
        "(C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç) TUTAR. Aksi: iki hücrede de iz-var n >= 30 ve güç >= 0,80 ise TUTMADI, "
        "değilse ÖLÇÜLEMEDİ. BİRLİKTE ARTIYOR <=> iki hücrede FARK(N=0) < FARK(N=1) < FARK(N>=2) VE N>=2 FARK boot alt > 0 en az bir hücrede, "
        "ötekinde FARK > 0. KASA ADAYI (yalnız öneri; kasa açılmaz) <=> aynı ufukta en az iki iz YÖN TUTARLI VE BİRLİKTE ARTIYOR. BH q 0,10, "
        "aile = (R, B, İ, N>=2) x (R60, R15) = 8; p = iki hücrenin en büyük permütasyon p'si (n < 30 hücre p = 1). AVRUPA: SEC verisi yok -> "
        "'AVRUPA VERİSİ YOK', karar en fazla ABD-ADAY. Evren bugün yaşayanlar (K7): sonuç yukarı yanlı."),
}


# ================================================================ 0) YARDIMCI
def _u2_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _u2_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def uc2_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or UC2_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _u2_json(o: Any) -> Any:
    import UC_IZ as U
    return U._uc_json(o)


def _u2_jyaz(yol: str, J: Any) -> None:
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol + ".tmp", "w", encoding="utf-8") as f:
        json.dump(_u2_json(J), f, ensure_ascii=False, indent=1)
    os.replace(yol + ".tmp", yol)


def _u2_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_UC2, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as ex:   # git yoksa kapı düşer (fail-closed çağıranda)
        u2log.warning("git çalışmadı: %s", ex)
        return ""


def _u2_pkl_yaz(yol: str, X: Any) -> str:
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol + ".tmp", "wb") as f:
        pickle.dump(X, f, protocol=4)
    os.replace(yol + ".tmp", yol)
    return _u2_sha(yol)


# ================================================================ 1) SEC ERİŞİMİ (User-Agent yalnız /root/.sec_ua; içerik hiçbir yere yazılmaz)
def _u2_ua() -> str:
    try:
        s = open(UC2_YOL["ua"], encoding="utf-8").read().strip()
    except OSError as ex:
        raise UC2Hata(f"SEC User-Agent dosyası okunamadı ({ex.strerror})") from None
    if not s or "@" not in s or "\n" in s:
        raise UC2Hata("SEC User-Agent dosyası geçersiz (tek satır, iletişim adresi içermeli)")
    return s


_U2_SON = [0.0]
_U2_SAY = {"istek": 0, "yeniden": 0, "404": 0}


def uc2_sec_get(url: str, ua: str) -> Optional[bytes]:
    """Hız sınırlı GET (aralık >= 0,15 sn; <= 6,7 istek / sn). 404 -> None. 429 / 403 / 5xx / ağ hatası -> artan bekleme ile yeniden dene.
    Hata mesajlarında User-Agent geçmez."""
    S = UC2_SEC
    for dnm in range(int(S["deneme"])):
        bekle = S["aralik_sn"] - (time.monotonic() - _U2_SON[0])
        if bekle > 0:
            time.sleep(bekle)
        _U2_SON[0] = time.monotonic(); _U2_SAY["istek"] += 1
        try:
            rq = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip, deflate"})
            with urllib.request.urlopen(rq, timeout=120) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                return raw
        except urllib.error.HTTPError as ex:
            if ex.code == 404:
                _U2_SAY["404"] += 1
                return None
            neden = f"HTTP {ex.code}"
        except Exception as ex:   # ağ / zaman aşımı: yeniden dene
            neden = type(ex).__name__
        _U2_SAY["yeniden"] += 1
        b = S["bekle_sn"][min(dnm, len(S["bekle_sn"]) - 1)]
        u2log.warning("SEC %s: %s -> %d sn bekle (deneme %d)", url.rsplit("/", 1)[-1], neden, b, dnm + 1)
        time.sleep(b)
    raise UC2Hata(f"SEC erişilemedi: {url.rsplit('/', 1)[-1]} ({S['deneme']} deneme)")


# ================================================================ 2) FORM 4 (V2)
def uc2_form4_indir() -> List[str]:
    """2015q4..2022q4 form345 zip (var olan ve açılabilen atlanır). Döner dosya yolları (çeyrek sırasıyla)."""
    ua = _u2_ua(); os.makedirs(UC2_YOL["form345"], exist_ok=True); out = []
    for c in UC2_SEC["ceyrekler"]:
        yol = os.path.join(UC2_YOL["form345"], f"{c}_form345.zip")
        if os.path.exists(yol) and os.path.getsize(yol) > 0:
            try:
                zipfile.ZipFile(yol).namelist(); out.append(yol); continue
            except zipfile.BadZipFile:
                u2log.warning("%s bozuk, yeniden indirilecek", os.path.basename(yol))
        raw = uc2_sec_get(UC2_SEC["form4_url"].format(c=c), ua)
        if raw is None:
            raise UC2Hata(f"Form 4 çeyreği yok (404): {c}")
        with open(yol + ".tmp", "wb") as f:
            f.write(raw)
        zipfile.ZipFile(yol + ".tmp").namelist()
        os.replace(yol + ".tmp", yol); out.append(yol)
        u2log.info("Form 4 %s: %.1f MB", c, len(raw) / 1e6)
    return out


def uc2_issuer_cik(dosyalar: List[str]) -> pd.DataFrame:
    """SUBMISSION.tsv: erişim no -> ihraççı CIK (ilk görülen; fi_k30_alimlar'ın drop_duplicates sırasıyla aynı)."""
    parca = []
    for yol in dosyalar:
        z = zipfile.ZipFile(yol)
        S = pd.read_csv(z.open("SUBMISSION.tsv"), sep="\t", usecols=["ACCESSION_NUMBER", "ISSUERCIK"], dtype=str)
        parca.append(S)
    S = pd.concat(parca, ignore_index=True).drop_duplicates("ACCESSION_NUMBER")
    S["issuer_cik"] = pd.to_numeric(S.ISSUERCIK, errors="coerce").astype("Int64")
    return S[["ACCESSION_NUMBER", "issuer_cik"]]


def uc2_form4_a1(dosyalar: List[str]) -> pd.DataFrame:
    """A1 = FON_IZI.fi_k30_alimlar AYNEN + değer >= FI_K30['kucuk'] + ihraççı CIK. Bilgi tarihi D = FILING_DATE."""
    import FON_IZI as FI
    X = FI.fi_k30_alimlar(dosyalar, FI.FI_K30)
    X = X[X.deger >= FI.FI_K30["kucuk"]].copy()
    X = X.merge(uc2_issuer_cik(dosyalar), on="ACCESSION_NUMBER", how="left", validate="one_to_one")
    X["D"] = pd.to_datetime(X.D).dt.normalize()
    return X.sort_values(["D", "ACCESSION_NUMBER"], kind="mergesort").reset_index(drop=True)


def uc2_k30_saglama(dosyalar: List[str], tohum: int = 2611) -> Dict[str, Any]:
    """V2 sağlaması: 2022 çeyreklerinden fi_k30_alimlar + fon_izi_k30 süzgeci (V_ABD evreni, değer >= 10 bin $, giriş günü var) = islenmis-veri
    k30_alim.pkl 2022 satırları (satır sayısı, erişim no kümesi, rastgele 5 satır alan alan)."""
    import FON_IZI as FI
    f22 = [y for y in dosyalar if os.path.basename(y).startswith("2022")]
    X = FI.fi_k30_alimlar(f22, FI.FI_K30)
    Va = pd.read_pickle(os.path.join(UC2_YOL["veri_eski"], "V_ABD.pkl"))
    X = X[X.sembol.isin(Va) & (X.deger >= FI.FI_K30["kucuk"])].copy()
    ok = []
    for r in X.itertuples():
        ix = Va[r.sembol].index; j = int(ix.searchsorted(r.D, side="right"))
        ok.append(1 <= j < len(ix))
    X = X[np.asarray(ok, bool)]
    X = X[X.D.dt.year == 2022]
    K = pd.read_pickle(os.path.join(UC2_YOL["veri2"], "k30_alim.pkl")); K = K[pd.to_datetime(K.D).dt.year == 2022]
    a, b = set(X.ACCESSION_NUMBER), set(K.ACCESSION_NUMBER)
    rng = np.random.default_rng(tohum); sec = sorted(a & b)
    sec = [sec[i] for i in rng.choice(len(sec), size=min(5, len(sec)), replace=False)] if sec else []
    ornek = []
    for acc in sec:
        x = X[X.ACCESSION_NUMBER == acc].iloc[0]; k = K[K.ACCESSION_NUMBER == acc].iloc[0]
        es = {c: (str(x[c]) == str(k[c])) if c != "D" else pd.Timestamp(x[c]) == pd.Timestamp(k[c]) for c in ("sembol", "D", "cik", "rol")}
        es["deger"] = bool(abs(float(x.deger) - float(k.deger)) < 1e-6)
        ornek.append({"acc": acc, "sembol": str(x.sembol), "D": str(pd.Timestamp(x.D).date()), "deger_yeni": float(x.deger),
                      "deger_k30": float(k.deger), "rol": str(x.rol), "esit": es, "tumu": all(es.values())})
    J = {"yeni_2022": int(len(X)), "k30_2022": int(len(K)), "ortak": len(a & b), "yalniz_yeni": len(a - b), "yalniz_k30": len(b - a),
         "ornek5": ornek}
    J["tuttu"] = bool(J["yeni_2022"] == J["k30_2022"] and not (a ^ b) and all(o["tumu"] for o in ornek) and len(ornek) == 5)
    return J


def uc2_sec_form4() -> Dict[str, Any]:
    t0 = time.time()
    dos = uc2_form4_indir()
    A = uc2_form4_a1(dos)
    if A.D.max() > UC2_KESIK:
        A = A[A.D <= UC2_KESIK].copy()
    sag = uc2_k30_saglama(dos)
    sha = _u2_pkl_yaz(os.path.join(UC2_YOL["ham"], UC2_DOSYA["a1"]), A)
    J = {"zaman": _u2_simdi(), "ceyrek": len(dos), "zip": {os.path.basename(y): {"mb": round(os.path.getsize(y) / 1e6, 2), "sha256": _u2_sha(y)}
                                                           for y in dos},
         "a1_satir": int(len(A)), "a1_ilk": str(A.D.min().date()), "a1_son": str(A.D.max().date()), "a1_ihracci": int(A.issuer_cik.nunique()),
         "a1_ihracci_cik_yok": int(A.issuer_cik.isna().sum()), "a1_yil": {str(k): int(v) for k, v in A.groupby(A.D.dt.year).size().items()},
         "a1_pkl_sha": sha, "saglama_k30_2022": sag, "istek": dict(_U2_SAY), "sure_sn": round(time.time() - t0)}
    _u2_veri_json_guncelle({"form4": J})
    if not sag["tuttu"]:
        raise UC2Hata(f"V2 sağlaması TUTMADI: {json.dumps(_u2_json({k: v for k, v in sag.items() if k != 'ornek5'}))}")
    u2log.info("Form 4: %d çeyrek, A1 %d satır (%s..%s), sağlama TUTTU (%d / %d)", len(dos), len(A), J["a1_ilk"], J["a1_son"],
               sag["yeni_2022"], sag["k30_2022"])
    return J


def _u2_veri_json_guncelle(ek: Dict[str, Any]) -> None:
    yol = os.path.join(UC2_YOL["cikti"], UC2_DOSYA["veri_json"])
    J = json.load(open(yol, encoding="utf-8")) if os.path.exists(yol) else {"surum": UC2_SURUM}
    J.update(ek)
    _u2_jyaz(yol, J)


# ================================================================ 3) 8-K 2.02 (V3) ve SEMBOL -> CIK (V4)
def uc2_sembol_norm(s: str) -> str:
    return str(s).strip().upper().replace(".", "-")


def uc2_company_tickers() -> Tuple[Dict[str, int], str]:
    """SEC company_tickers.json (bugün indirilir; olmazsa islenmis-veri secfs yedeği). Döner {sembol (normalize): CIK}, kaynak."""
    yol = os.path.join(UC2_YOL["ham"], UC2_DOSYA["ct"]); kaynak = "sec_bugun"
    if not os.path.exists(yol):
        raw = uc2_sec_get(UC2_SEC["ticker_url"], _u2_ua())
        if raw is not None:
            os.makedirs(UC2_YOL["ham"], exist_ok=True)
            open(yol, "wb").write(raw)
    if not os.path.exists(yol):
        yol = UC2_YOL["ct_yedek"]; kaynak = "islenmis_veri_secfs"
    J = json.load(open(yol, encoding="utf-8"))
    m: Dict[str, int] = {}
    for v in J.values():
        k = uc2_sembol_norm(v["ticker"])
        m.setdefault(k, int(v["cik_str"]))
    return m, kaynak


def uc2_sub_indir(ciks: List[int]) -> Dict[str, Any]:
    """Her CIK için submissions JSON (ana + dönemle örtüşen ek sayfalar) -> <ham>/sub/CIK##########.json.gz (var olan atlanır)."""
    ua = _u2_ua(); os.makedirs(UC2_YOL["sub"], exist_ok=True)
    a, b = (pd.Timestamp(x) for x in UC2_SEC["sub_pencere"]); say = {"cik": len(ciks), "var": 0, "indirildi": 0, "yok_404": 0, "ek_sayfa": 0}
    t0 = time.time()
    for n, c in enumerate(ciks, 1):
        yol = os.path.join(UC2_YOL["sub"], f"CIK{int(c):010d}.json.gz")
        if os.path.exists(yol):
            say["var"] += 1; continue
        raw = uc2_sec_get(UC2_SEC["sub_url"].format(cik=int(c)), ua)
        if raw is None:
            say["yok_404"] += 1
            with gzip.open(yol + ".tmp", "wt", encoding="utf-8") as f:
                json.dump({"cik": int(c), "yok": True}, f)
            os.replace(yol + ".tmp", yol); continue
        d = json.loads(raw); ek = []
        for fx in d.get("filings", {}).get("files", []) or []:
            try:
                fa, fb = pd.Timestamp(fx.get("filingFrom")), pd.Timestamp(fx.get("filingTo"))
            except Exception:   # tarih yoksa güvenli yol: indir
                fa, fb = a, b
            if fb < a or fa > b:
                continue
            r2 = uc2_sec_get(UC2_SEC["sub_ek_url"].format(ad=fx["name"]), ua)
            if r2 is not None:
                ek.append({"ad": fx["name"], "veri": json.loads(r2)}); say["ek_sayfa"] += 1
        with gzip.open(yol + ".tmp", "wt", encoding="utf-8") as f:
            json.dump({"cik": int(c), "ana": d, "ek": ek}, f)
        os.replace(yol + ".tmp", yol); say["indirildi"] += 1
        if n % 250 == 0:
            u2log.info("submissions %d / %d (indirilen %d, ek %d, %.0f sn)", n, len(ciks), say["indirildi"], say["ek_sayfa"], time.time() - t0)
    return say


def _u2_dosyalar_satir(f: Dict[str, Any]) -> pd.DataFrame:
    n = len(f.get("form", []))
    kol = {k: f.get(k, [None] * n) for k in ("accessionNumber", "filingDate", "acceptanceDateTime", "form", "items", "reportDate")}
    return pd.DataFrame(kol)


def uc2_k8_tablo(ciks: List[int]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Kayıtlı submissions dosyalarından 8-K ve 8-K/A satırları (madde 2.02 içerenler) + şirket bilgisi."""
    sat, bilgi, yok = [], {}, 0
    for c in ciks:
        yol = os.path.join(UC2_YOL["sub"], f"CIK{int(c):010d}.json.gz")
        if not os.path.exists(yol):
            yok += 1; continue
        J = json.load(gzip.open(yol, "rt", encoding="utf-8"))
        if J.get("yok"):
            yok += 1; continue
        d = J["ana"]; bilgi[int(c)] = {"ad": d.get("name"), "tickers": d.get("tickers"), "sic": d.get("sic")}
        parcalar = [_u2_dosyalar_satir(d.get("filings", {}).get("recent", {}))] + [_u2_dosyalar_satir(e["veri"]) for e in J.get("ek", [])]
        X = pd.concat(parcalar, ignore_index=True)
        X = X[X.form.isin(["8-K", "8-K/A"]) & X["items"].fillna("").astype(str).str.contains("2.02", regex=False)]
        if len(X):
            sat.append(X.assign(cik=int(c)))
    K = pd.concat(sat, ignore_index=True).drop_duplicates("accessionNumber") if sat else pd.DataFrame(
        columns=["accessionNumber", "filingDate", "acceptanceDateTime", "form", "items", "reportDate", "cik"])
    return K.reset_index(drop=True), {"cik_dosya_yok_ya_da_404": yok, "sirket_bilgi": len(bilgi)}


def uc2_semboller() -> Tuple[List[str], str]:
    """CIK listesi için ABD sembolleri: açık kopya V_ABD.pkl varsa onun sembolleri, yoksa V_ABD2.pkl, yoksa TEZGAH2 evren2_ABD_ham.csv."""
    for yol, ad in ((os.path.join(UC2_YOL["acik"], "V_ABD.pkl"), "acik_V_ABD"), (os.path.join(UC2_YOL["veri3"], "V_ABD2.pkl"), "V_ABD2")):
        if os.path.exists(yol):
            return sorted(str(k) for k in pd.read_pickle(yol)), ad
    yol = os.path.join(UC2_YOL["veri3"], "evren2_ABD_ham.csv")
    if not os.path.exists(yol):
        raise UC2Hata("sembol listesi yok (V_ABD / V_ABD2 / evren2_ABD_ham.csv)")
    return sorted(pd.read_csv(yol, keep_default_na=False, dtype=str).yahoo.astype(str)), "evren2_ABD_ham"


def uc2_sec_8k(semboller: Optional[List[str]] = None) -> Dict[str, Any]:
    """V3 / V4: sembol -> CIK (company_tickers), submissions indir, 8-K 2.02 tablosu -> <ham>/k8_202.pkl."""
    t0 = time.time()
    if semboller is None:
        semboller, kay = uc2_semboller()
    else:
        kay = "verilen"
    m, ct_kaynak = uc2_company_tickers()
    eslesen = {s: m[uc2_sembol_norm(s)] for s in semboller if uc2_sembol_norm(s) in m}
    ciks = sorted(set(eslesen.values()))
    say = uc2_sub_indir(ciks)
    K, kb = uc2_k8_tablo(ciks)
    sha = _u2_pkl_yaz(os.path.join(UC2_YOL["ham"], UC2_DOSYA["k8"]), {"K": K, "sembol_cik": eslesen, "ct_kaynak": ct_kaynak})
    J = {"zaman": _u2_simdi(), "sembol_kaynak": kay, "sembol": len(semboller), "sembol_cik_eslesen": len(eslesen),
         "sembol_eslenmeyen": len(semboller) - len(eslesen), "cik": len(ciks), "ct_kaynak": ct_kaynak, "indirme": say, **kb,
         "k8_202_satir": int(len(K)), "k8_202_8K": int((K.form == "8-K").sum()), "k8_202_8KA": int((K.form == "8-K/A").sum()),
         "k8_pkl_sha": sha, "istek": dict(_U2_SAY), "sure_sn": round(time.time() - t0)}
    _u2_veri_json_guncelle({"k8": J})
    u2log.info("8-K: %d sembol, %d CIK, 2.02 satır %d (%.0f sn)", len(semboller), len(ciks), len(K), time.time() - t0)
    return J


# ================================================================ 4) AÇIK KOPYA (V1; 2022-12-31 kesik, mekanik denetim)
def uc2_kes_fiyat(V: Dict[str, pd.DataFrame], kesik: pd.Timestamp = UC2_KESIK, bas: Optional[str] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, int]]:
    """UC_IZ.uc_kes mekaniği fiyat sözlüğünde: tarih <= kesik (ve >= bas) satırlar; kesik sonrası satır kalırsa DURUR. Boş kalan sembol düşer."""
    out: Dict[str, pd.DataFrame] = {}; say = {"sembol": len(V), "bos": 0, "atilan_satir": 0}
    b = pd.Timestamp(bas) if bas else None
    for s, d in V.items():
        ix = pd.DatetimeIndex(d.index)
        m = ix <= kesik
        if b is not None:
            m &= ix >= b
        x = d[m]
        say["atilan_satir"] += int((ix > kesik).sum())
        if not len(x):
            say["bos"] += 1; continue
        if pd.DatetimeIndex(x.index).max() > kesik:
            raise UC2Hata(f"{s}: kesik sonrası satır kaldı -> DURDU")
        out[s] = x
    return out, say


def uc2_kesik_kapi(veri: Optional[str] = None, dosyalar: Tuple[str, ...] = ("V_ABD.pkl",)) -> Dict[str, Any]:
    """KASA.kasa_kapisi (açık kesik 2022-12-31): dosyalardaki en geç tarih kesiği aşarsa DURUR (fail-closed)."""
    import KASA as KS
    v = veri or UC2_YOL["acik"]
    try:
        return KS.kasa_kapisi([os.path.join(v, f) for f in dosyalar], str(UC2_KESIK.date()))
    except KS.KasaHata as ex:
        raise UC2Hata(f"kesik kapısı KAPALI: {ex}") from ex


def uc2_acik_kopya() -> Dict[str, Any]:
    """V_ABD2 / V_AVR2 (TEZGAH2) -> (a) acik_tam: 2000..2022-12-31 (TEZGAH2_DOGRULAMA 21 sınaması) (b) acik: veri_bas..2022-12-31 (ölçüm; ABD)."""
    J: Dict[str, Any] = {"zaman": _u2_simdi()}
    tam = UC2_YOL["acik"] + "_tam"
    for p in ("ABD", "AVR"):
        kay = os.path.join(UC2_YOL["veri3"], f"V_{p}2.pkl")
        if not os.path.exists(kay):
            raise UC2Hata(f"TEZGAH2 verisi yok: {kay}")
        V = pd.read_pickle(kay)
        W, s1 = uc2_kes_fiyat(V)
        os.makedirs(tam, exist_ok=True); sha_t = _u2_pkl_yaz(os.path.join(tam, f"V_{p}.pkl"), W)
        J[p] = {"kaynak_sha": _u2_sha(kay), "kaynak_sembol": len(V), "tam": {**s1, "yazilan": len(W), "sha": sha_t,
                "ilk": str(min(d.index.min() for d in W.values()).date()), "son": str(max(d.index.max() for d in W.values()).date())}}
        if p == "ABD":
            W2, s2 = uc2_kes_fiyat(V, bas=UC2_ESIK["veri_bas"])
            os.makedirs(UC2_YOL["acik"], exist_ok=True); sha_a = _u2_pkl_yaz(os.path.join(UC2_YOL["acik"], "V_ABD.pkl"), W2)
            J[p]["acik"] = {**s2, "yazilan": len(W2), "sha": sha_a, "ilk": str(min(d.index.min() for d in W2.values()).date()),
                            "son": str(max(d.index.max() for d in W2.values()).date())}
            del W2
        del V, W
    J["kapi_tam"] = uc2_kesik_kapi(tam, ("V_ABD.pkl", "V_AVR.pkl"))
    J["kapi_acik"] = uc2_kesik_kapi(UC2_YOL["acik"])
    _u2_veri_json_guncelle({"acik_kopya": J})
    return J


def uc2_t2_dogrulama(veri: Optional[str] = None) -> Dict[str, Any]:
    """TEZGAH2_DOGRULAMA 21 ana hükmü 2022-12-31 kesikli açık kopyada yeniden (T2 / TD fonksiyonları AYNEN; KASA 2 kapısı yerine uc2 kesik
    kapısı). Hücre d3 = 2016-01..2022-12 (veri kesiği). Orijinal (tezgah2_dogrulama.json) seçim tablosu ile yan yana."""
    import gc
    import OLCU_SINAMA as OS
    import TEZGAH2_DOGRULAMA as T2
    import TEZGAH_DOGRULAMA as TD
    v = veri or (UC2_YOL["acik"] + "_tam")
    kp = uc2_kesik_kapi(v, ("V_ABD.pkl", "V_AVR.pkl"))
    HZ = json.load(open(os.path.join(T2.T2_YOL["cikti"], T2.T2_DOSYA["hazirlik"]), encoding="utf-8"))
    R, _ = TD.td_ref_yukle(T2.T2_YOL["ref_td"]); fx = T2.t2_eurusd_ay()
    S: Dict[str, pd.Series] = {}; nt: Dict[str, Any] = {}
    for p in ("ABD", "AVR"):
        Vd = OS.os_veri(p, v); Pn = OS.os_panel(Vd, HZ["sinir"][p]); M = T2.t2_havuz(Pn, Vd)
        Z = TD.td_kesit(Pn, Vd, fx if p == "AVR" else None)
        dd = Z.d.to_numpy(np.int64); jj = Z.j.to_numpy(np.int64)
        for hv in T2.T2_HAVUZ:
            Z[hv] = M[hv][dd, jj]
        nt[p] = {"hisse": len(Vd["V"]), "en_gec": str(max(d.index.max() for d in Vd["V"].values()).date()), "kesit_satir": int(len(Z))}
        S.update(T2.t2_seriler(Z, p))
        del Z, Vd, Pn, M; gc.collect()
    K = T2.t2_karsilastir(S, R); SEC = T2.t2_secim(K)
    O = json.load(open(os.path.join(T2.T2_YOL["cikti"], T2.T2_DOSYA["json"]), encoding="utf-8"))["secim"]
    tablo = {hv: {"dogru": SEC["tablo"][hv]["dogru"], "n": SEC["tablo"][hv]["n"],
                  "dusen": [(x["kod"], x["donem"], x["hukum"], x.get("pearson"), x.get("isaret")) for x in SEC["tablo"][hv]["dusen"]],
                  "orijinal_dogru": O["tablo"][hv]["dogru"], "orijinal_dusen": [(x["kod"], x["donem"], x["hukum"]) for x in O["tablo"][hv]["dusen"]]}
             for hv in T2.T2_HAVUZ}
    sec = SEC["secilen"]
    gecti = bool(tablo[sec]["dogru"] == tablo[sec]["n"] == 21 and sec == O["secilen"])
    J = {"zaman": _u2_simdi(), "kapi": kp, "veri_not": nt, "secilen": sec, "orijinal_secilen": O["secilen"], "yol": SEC["yol"], "tablo": tablo,
         "kural": "seçim kuralıyla seçilen havuz 21 / 21 DOĞRU ve orijinal seçimle aynı (orijinal: P1 21 / 21, P2 20 / 21 A1 d1 KISMEN)",
         "gecti": gecti, "ref_en_gec": max(str(x.index.max()) for x in R.values())}
    _u2_veri_json_guncelle({"t2_dogrulama": J})
    if not gecti:
        raise UC2Hata(f"TEZGAH2_DOGRULAMA 21 sınaması TUTMADI: seçilen {sec}, {tablo[sec]['dogru']} / {tablo[sec]['n']}")
    return J


# ================================================================ 5) E1 BİLANÇO OLAYLARI (getirisiz)
def uc2_kabul_d0(kabul_utc: Any) -> Tuple[pd.Series, pd.Series]:
    """acceptanceDateTime (UTC) -> New York yerel zaman ve D0 (takvim günü): yerel saat < 16:00:00 ise o gün, >= 16:00:00 ise ertesi gün."""
    ts = pd.to_datetime(pd.Series(kabul_utc), utc=True, errors="coerce").dt.tz_convert("America/New_York")
    sn = ts.dt.hour * 3600 + ts.dt.minute * 60 + ts.dt.second
    h, m, s = (int(x) for x in UC2_ESIK["olay"]["kabul_sinir_saat"].split(":"))
    once = sn < (h * 3600 + m * 60 + s)
    gun = ts.dt.tz_localize(None).dt.normalize()
    D0 = gun.where(once, gun + pd.Timedelta(days=1))
    return D0, ts


def uc2_olay_gunu(D0: Any, takvim: pd.DatetimeIndex) -> np.ndarray:
    """D0 -> birleşik takvimde D0'a eşit ya da sonraki ilk gün (yoksa NaT)."""
    tk = pd.DatetimeIndex(takvim).sort_values().values.astype("datetime64[ns]")
    d0 = pd.to_datetime(pd.Series(D0)).values.astype("datetime64[ns]")
    k = np.searchsorted(tk, d0, side="left")
    out = np.full(len(d0), np.datetime64("NaT", "ns"), dtype="datetime64[ns]")
    ok = (k < len(tk)) & ~np.isnat(d0)
    out[ok] = tk[k[ok]]
    return out


def uc2_tekrar_at(cik: np.ndarray, t: np.ndarray, gun: int) -> np.ndarray:
    """Aynı CIK'de t sırasıyla: son TUTULAN olaydan <= gun takvim günü sonraki olay atılır (aynı gün de atılır). Döner tut maskesi (girdi sırası)."""
    t = pd.to_datetime(pd.Series(t)).values.astype("datetime64[ns]"); cik = np.asarray(cik)
    o = np.lexsort((t, cik)); tut = np.zeros(len(t), bool); son: Dict[Any, np.datetime64] = {}
    for i in o:
        c = cik[i]
        if c not in son or (t[i] - son[c]) > np.timedelta64(int(gun), "D"):
            tut[i] = True; son[c] = t[i]
    return tut


def uc2_cik_sembol(sembol_cik: Dict[str, int], V: Dict[str, pd.DataFrame]) -> Tuple[Dict[int, str], Dict[int, List[str]]]:
    """CIK -> olay sembolü (en çok geçerli bar; eşitlikte alfabetik ilk) ve CIK -> bütün panel sembolleri (sınıf hisseleri; eş dışlaması)."""
    tum: Dict[int, List[str]] = {}
    for s, c in sembol_cik.items():
        if s in V:
            tum.setdefault(int(c), []).append(s)
    sec = {c: sorted(L, key=lambda s: (-len(V[s]), s))[0] for c, L in tum.items()}
    return sec, {c: sorted(L) for c, L in tum.items()}


def uc2_e1_ham(K8: pd.DataFrame, sembol_cik: Dict[str, int], Vd: Dict[str, Any], takvim: pd.DatetimeIndex) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """8-K 2.02 satırları -> E1 olayları (sembol, cik, tarih = t, kabul) ve dışlama listesi (aynı gün bütün sınıf hisseleri). Getirisiz."""
    E = UC2_ESIK["olay"]; say: Dict[str, Any] = {"k8_202_satir": int(len(K8))}
    K = K8[K8.form.astype(str) == E["form"]].copy()
    K = K[K["items"].fillna("").astype(str).map(lambda x: E["madde"] in [i.strip() for i in x.split(",")])]
    say["form_8K_madde_202"] = int(len(K))
    D0, ts = uc2_kabul_d0(K.acceptanceDateTime.to_numpy())
    K["D0"] = D0.to_numpy(); K["kabul_ny"] = ts.dt.strftime("%Y-%m-%d %H:%M:%S").to_numpy()
    say["kabul_yok"] = int(pd.isna(K.D0).sum()); K = K[pd.notna(K.D0)]
    sec, tum = uc2_cik_sembol(sembol_cik, Vd["V"])
    K["cik"] = K.cik.astype(int); K["sembol"] = K.cik.map(sec)
    say["cik_sembolsuz_satir"] = int(K.sembol.isna().sum()); K = K[K.sembol.notna()].copy()
    K["tarih"] = uc2_olay_gunu(K.D0, takvim)
    say["takvim_disi"] = int(pd.isna(K.tarih).sum()); K = K[pd.notna(K.tarih)].copy()
    a, b = pd.Timestamp(E["aralik"][0]), pd.Timestamp(E["aralik"][1])
    say["aralik_disi"] = int(((K.tarih < a) | (K.tarih > b)).sum())
    tut = uc2_tekrar_at(K.cik.to_numpy(), K.tarih.to_numpy(), int(E["tekrar_gun"]))
    say["tekrar_atilan_tum"] = int((~tut).sum()); K = K[tut].copy()
    K = K[(K.tarih >= a) & (K.tarih <= b)].copy()
    gec = np.array([pd.Timestamp(t) in Vd["V"][s].index for s, t in zip(K.sembol, K.tarih)], bool)
    say["olay_gunu_gecersiz_bar"] = int((~gec).sum()); K = K[gec].copy()
    if len(K) and (pd.to_datetime(K.D0) > pd.to_datetime(K.tarih)).any():
        raise UC2Hata("olay günü kabul gününden önce (geleceğe bakma denetimi) -> DURDU")
    K = K.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    EX = pd.DataFrame([(s2, t) for c, t in zip(K.cik, K.tarih) for s2 in tum.get(int(c), [])], columns=["sembol", "tarih"]).drop_duplicates()
    say.update({"e1": int(len(K)), "e1_cik": int(K.cik.nunique()), "e1_sembol": int(K.sembol.nunique()), "dislama_satir": int(len(EX)),
                "cok_sinif_cik": int(sum(len(v) > 1 for v in tum.values()))})
    kol = ["sembol", "cik", "tarih", "D0", "kabul_ny", "acceptanceDateTime", "accessionNumber", "filingDate", "items"]
    return K[kol], EX.reset_index(drop=True), say


# ================================================================ 6) İZLER (getirisiz: yalnız t'ye kadar bilgi)
def uc2_ret_atrp(Pb: Dict[str, Any], gun: int = 20) -> Tuple[np.ndarray, np.ndarray]:
    """Panel takviminde (C2 taban paneli) günlük getiri RET[t] = C_t / C_önceki geçerli - 1 (geçerli barda) ve ATRP{gun}_{t-1} (t'deki satırda,
    önceki geçerli barın ATR{gun} / C değeri; TR önceki kapanışla, SMA; POZITIF_KONTROL.pk_seri ile aynı formül, pencere {gun})."""
    P = Pb["P"]; idx = P["tarih"]; S = P["sembol"]; V = Pb["Vd"]["V"]
    RET = np.full((len(idx), len(S)), np.nan); ATP = np.full((len(idx), len(S)), np.nan)
    for j, s in enumerate(S):
        df = V[s]; pos = idx.get_indexer(df.index)
        if (pos < 0).any():
            raise UC2Hata(f"{s}: hisse takvimi panelde yok")
        H, L, C = (df[k].to_numpy(float) for k in ("High", "Low", "Close"))
        if len(C) < 2:
            continue
        pC = np.r_[np.nan, C[:-1]]
        TR = np.where(np.isfinite(pC), np.maximum(H, pC) - np.minimum(L, pC), H - L)
        a = pd.Series(TR).rolling(int(gun), min_periods=int(gun)).mean().to_numpy() / C
        with np.errstate(invalid="ignore", divide="ignore"):
            RET[pos[1:], j] = C[1:] / C[:-1] - 1
        ATP[pos[1:], j] = a[:-1]
    return RET, ATP


def uc2_b(E1: pd.DataFrame, Pb: Dict[str, Any], RET: np.ndarray, ATP: np.ndarray, EXg: pd.DataFrame) -> pd.DataFrame:
    """B: EAR_t = RET[t, j] - medyan(RET[t, eş]) (eş: KV[t] aynı kova, RET sonlu, hisse ve o gün E1 olan bütün sınıf hisseleri hariç, >= 5);
    BVAL = EAR / ATRP20_{t-1}; B = BVAL >= 1,0; Bm (bilgi) = BVAL <= -1,0. Hesaplanamayan -> NaN."""
    P = Pb["P"]; KV = Pb["KV"]; idx = P["tarih"]; kol = P["kol"]; me = int(UC2_ESIK["B"]["es_min"])
    n = len(E1); ear = np.full(n, np.nan); atp = np.full(n, np.nan); nes = np.zeros(n, int); kv = np.full(n, -1)
    dt = idx.get_indexer(pd.to_datetime(E1.tarih)); jj = np.array([kol.get(s, -1) for s in E1.sembol])
    exd = idx.get_indexer(pd.to_datetime(EXg.tarih)); exj = np.array([kol.get(s, -1) for s in EXg.sembol])
    exm = (exd >= 0) & (exj >= 0); ex_by_d: Dict[int, np.ndarray] = {}
    for d_, g in pd.Series(exj[exm]).groupby(exd[exm]):
        ex_by_d[int(d_)] = g.to_numpy(np.int64)
    ok_ev = (dt >= 0) & (jj >= 0)
    for d_ in np.unique(dt[ok_ev]):
        ii = np.flatnonzero(ok_ev & (dt == d_))
        kr = KV[d_]; rr = RET[d_]; m = (kr >= 0) & np.isfinite(rr)
        ex = ex_by_d.get(int(d_))
        if ex is not None:
            m[ex] = False
        for i in ii:
            k = int(kr[jj[i]]); kv[i] = k
            if k < 0 or not np.isfinite(rr[jj[i]]):
                continue
            pe = rr[m & (kr == k)]
            nes[i] = len(pe)
            if len(pe) >= me:
                ear[i] = rr[jj[i]] - float(np.median(pe))
            atp[i] = ATP[d_, jj[i]]
    with np.errstate(invalid="ignore", divide="ignore"):
        bv = np.where(np.isfinite(ear) & np.isfinite(atp) & (atp > 0), ear / atp, np.nan)
    out = pd.DataFrame({"ear": ear, "atrp20": atp, "bval": bv, "n_es_b": nes, "kova_t": kv}, index=E1.index)
    out["B"] = np.where(np.isfinite(bv), (bv >= float(UC2_ESIK["B"]["esik"])).astype(float), np.nan)
    out["Bm"] = np.where(np.isfinite(bv), (bv <= float(UC2_ESIK["B"]["bilgi_eksi"])).astype(float), np.nan)
    return out


def uc2_i(cik: np.ndarray, t: np.ndarray, A1: pd.DataFrame, gun: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """İ: (t - gun, t] takvim aralığında FILING_DATE'li A1 sayısı > 0 (ihraççı CIK). Döner bayrak, sayı, en son D (NaT). Yalnız D <= t."""
    g = int(gun or UC2_ESIK["I"]["gun"])
    A = A1.dropna(subset=["issuer_cik"])
    ev = {int(c): np.sort(x.D.values.astype("datetime64[ns]")) for c, x in A.groupby("issuer_cik")}
    t = pd.to_datetime(pd.Series(t)).values.astype("datetime64[ns]")
    bay = np.zeros(len(t), bool); say = np.zeros(len(t), int); son = np.full(len(t), np.datetime64("NaT", "ns"), dtype="datetime64[ns]")
    for k, (c, tt) in enumerate(zip(np.asarray(cik), t)):
        e = ev.get(int(c))
        if e is None or np.isnat(tt):
            continue
        hi = np.searchsorted(e, tt, side="right"); lo = np.searchsorted(e, tt - np.timedelta64(g, "D"), side="right")
        if hi > lo:
            bay[k] = True; say[k] = int(hi - lo); son[k] = e[hi - 1]
            if e[hi - 1] > tt:
                raise UC2Hata("İ bayrağı geleceği gördü")
    return bay, say, son


def uc2_r(X: pd.DataFrame, C: pd.DataFrame) -> np.ndarray:
    """R: (sembol, t) KT10 'c' satırında (D9 durumu t kapanışında, yalnız t'ye kadar fiyat)."""
    Cc = C[["sembol", "tarih"]].copy(); Cc["tarih"] = pd.to_datetime(Cc.tarih); Cc = Cc.drop_duplicates().assign(_r=1)
    Y = X[["sembol", "tarih"]].assign(tarih=lambda x: pd.to_datetime(x.tarih)).merge(Cc, on=["sembol", "tarih"], how="left")
    return Y._r.fillna(0).astype(int).to_numpy()


# ================================================================ 7) OLAY HAZIRLIĞI (E1 + izler + E2; getirisiz)
def _u2_a1() -> pd.DataFrame:
    import UC_IZ as U
    yol = os.path.join(UC2_YOL["ham"], UC2_DOSYA["a1"])
    if not os.path.exists(yol):
        raise UC2Hata(f"A1 tablosu yok: {yol} (önce sec_form4)")
    return U.uc_kes(pd.read_pickle(yol), "D", "Form 4 A1", UC2_KESIK)


def _u2_k8() -> Dict[str, Any]:
    yol = os.path.join(UC2_YOL["ham"], UC2_DOSYA["k8"])
    if not os.path.exists(yol):
        raise UC2Hata(f"8-K tablosu yok: {yol} (önce sec_8k)")
    return pd.read_pickle(yol)


def uc2_olaylar(veri: Optional[str] = None, islem: int = 4, e2: bool = True) -> Dict[str, Any]:
    """E1 olayları + R / B / İ / N bayrakları + P2 üyeliği (+ E2 KT02 olayları ve bayrakları). Getiri KULLANILMAZ (yalnız t'ye kadar fiyat)."""
    import gc
    import CETVEL2 as C2
    import D9_YENIDEN as D9
    import KART_TUR2 as KT2
    import OLCU_SINAMA as OS
    import UC_IZ as U
    t0 = time.time(); v = veri or UC2_YOL["acik"]
    kp = uc2_kesik_kapi(v)
    Vd = OS.os_veri(UC2_ESIK["pazar"], v)
    takvim = pd.DatetimeIndex(sorted(set().union(*[d.index for d in Vd["V"].values()])))
    if takvim.max() > UC2_KESIK:
        raise UC2Hata(f"KESİK AŞIMI: takvim {takvim.max().date()}")
    A1 = _u2_a1(); P8 = _u2_k8()
    m, ct_kay = uc2_company_tickers()
    sembol_cik = {s: m[uc2_sembol_norm(s)] for s in Vd["V"] if uc2_sembol_norm(s) in m}
    E1, EX, say = uc2_e1_ham(P8["K"], sembol_cik, Vd, takvim)
    say.update({"panel_sembol": len(Vd["V"]), "sembol_cik": len(sembol_cik), "sembol_cik_yok": len(Vd["V"]) - len(sembol_cik), "ct_kaynak": ct_kay})
    # R (KT10 'c') ve E2 (KT02) — UC_IZ.uc_dip_ham AYNEN
    if e2:
        Hd = U.uc_dip_ham(Vd, islem); C = Hd["C"]; K02 = Hd["K02"]; say["kt02"] = int(len(K02)); say["kt10_c"] = int(len(C))
        del Hd
    else:
        Dd = KT2.k2_d9_durum(Vd, UC2_ESIK["pazar"], KT2.K2_ESIK["d9_olay_bas"]); C = D9.d9_satir(Dd, "c")[["sembol", "tarih"]].copy(); K02 = None
        del Dd
    gc.collect()
    E1["R"] = uc2_r(E1, C)
    b, n, son = uc2_i(E1.cik.to_numpy(), E1.tarih.to_numpy(), A1)
    E1["I"] = b.astype(int); E1["i_say"] = n; E1["i_son"] = son
    # P2 (giriş günü, KART_TUR2 paneli)
    Pk, P2 = KT2.k2_panel(Vd, UC2_ESIK["pazar"]); P = KT2.k2_P(Pk, Vd, P2)
    Z, sp2 = KT2._k2_oc(E1[["sembol", "tarih"]], P, 1)
    k2 = set(zip(Z.sembol, pd.to_datetime(Z.tarih)))
    E1["p2"] = [(s, pd.Timestamp(t)) in k2 for s, t in zip(E1.sembol, E1.tarih)]
    say["p2_huni"] = sp2; say["p2"] = int(E1.p2.sum())
    del Pk, P2, P, Z; gc.collect()
    # B (CETVEL2 taban paneli: kova satırı t, günlük getiri, ATRP20)
    Pb = C2.c2_panel22_al(UC2_ESIK["pazar"], v, None)
    RET, ATP = uc2_ret_atrp(Pb, int(UC2_ESIK["B"]["atr_gun"]))
    Bd = uc2_b(E1, Pb, RET, ATP, EX)
    del RET, ATP; gc.collect()
    for c in Bd.columns:
        E1[c] = Bd[c].to_numpy()
    E1["N"] = np.where(np.isfinite(E1.B.to_numpy(float)), E1.R + np.nan_to_num(E1.B.to_numpy(float)) + E1.I, np.nan)
    say["b_hesaplanamayan"] = int(E1.B.isna().sum()); say["b_hesaplanamayan_p2"] = int((E1.B.isna() & E1.p2).sum())
    # E2 (bilgi): KT02 + gerçek B / İ / R
    X2 = None
    if K02 is not None:
        import GOZ_ETIKET as GE
        X2 = K02[["sembol", "tarih"]].copy(); X2["tarih"] = pd.to_datetime(X2.tarih)
        X2["cik"] = X2.sembol.map(sembol_cik)
        X2["R"] = uc2_r(X2, C)
        eb = E1[E1.B.to_numpy(float) == 1.0]; gB = {s: g.tarih.to_numpy() for s, g in eb.groupby("sembol")}
        X2["B"] = 0; X2["b_gun"] = pd.NaT
        for s, g in X2.groupby("sembol"):
            gi = GE.ge_hazir(Vd["V"][s]).index
            bb, ss = U.uc_pencere_bayrak(gi, g.tarih.to_numpy(), gB.get(s, np.array([], "datetime64[ns]")), int(UC2_ESIK["E2"]["pencere_bar"]))
            X2.loc[g.index, "B"] = bb.astype(int); X2.loc[g.index, "b_gun"] = ss
        okc = X2.cik.notna().to_numpy()
        bi = np.zeros(len(X2), bool); bi[okc], _, _ = uc2_i(X2.cik[okc].astype(int).to_numpy(), X2.tarih[okc].to_numpy(), A1)
        X2["I"] = bi.astype(int); X2["cik_yok"] = (~okc).astype(int)
        X2["N"] = X2.R + X2.B + X2.I
        say["e2"] = int(len(X2))
    # mekanik geleceğe bakma denetimi
    for c, ad in (("i_son", "İ"), ("D0", "kabul")):
        x = pd.to_datetime(E1[c])
        if (x > pd.to_datetime(E1.tarih)).any():
            raise UC2Hata(f"{ad} bilgi tarihi > t -> DURDU")
    say["sure_sn"] = round(time.time() - t0)
    u2log.info("olaylar: E1 %d (P2 %d), R %d, İ %d, B %d (%.0f sn)", len(E1), int(E1.p2.sum()), int(E1.R.sum()), int(E1.I.sum()),
               int(np.nansum(E1.B.to_numpy(float))), time.time() - t0)
    return {"E1": E1, "EX": EX, "K02": K02, "X2": X2, "say": say, "kapi": kp, "sembol_cik": sembol_cik}


# ================================================================ 8) ÖLÇÜM (ufuk başına; CETVEL2 v2.2)
UC2_KOL = ["sembol", "tarih", "cik", "R", "B", "I", "N", "Bm", "ear", "atrp20", "bval", "i_say", "accessionNumber", "kabul_ny"]


def uc2_analiz_olay(E1: pd.DataFrame) -> pd.DataFrame:
    """Analiz kümesi: P2 üyesi ve B hesaplanabilen E1 olayları."""
    return E1[E1.p2.astype(bool) & np.isfinite(E1.B.to_numpy(float))].reset_index(drop=True)


def uc2_olc_ufuk(X: pd.DataFrame, EX: pd.DataFrame, H: int, veri: Optional[str] = None, tekil: int = 1,
                 kol: Optional[List[str]] = None) -> Tuple[pd.DataFrame, Dict[str, Any], Dict[str, Any]]:
    """C2.c2_olay (tekil) + konum eşi C2.c2_es (dışlama: EX'in giriş günleri) + UC_IZ taban / ÜST-ALT. 'r15' sütunu R_H'yi taşır."""
    import CETVEL2 as C2
    import UC_IZ as U
    Pn = C2.c2_panel22_al(UC2_ESIK["pazar"], veri or UC2_YOL["acik"], int(H))
    kol = [c for c in (kol or UC2_KOL) if c in X.columns]
    S, say = C2.c2_olay(X[kol], Pn, int(tekil))
    Ex, _ = C2.c2_olay(EX[["sembol", "tarih"]], Pn, 1)
    exd = Ex.d.to_numpy(np.int64); exj = Ex.j.to_numpy(np.int64)
    e = C2.c2_es(Pn, S.d.to_numpy(np.int64), S.j.to_numpy(np.int64), S.r15.to_numpy(float), exd, exj, es_min=int(UC2_ESIK["es_min"]))
    S["es_r15"] = e["es_r15"]; S["n_es"] = e["n_es"]; S["sira"] = e["sira"]; S["fark"] = e["fark"]
    S["donem"] = U.uc_donem(S.giris)
    tu, ta = U.uc_taban(S.n_es.to_numpy(float), UC2_ESIK["ust_pay"], UC2_ESIK["alt_pay"])
    S["taban_ust10"] = np.where(np.isfinite(S.fark), tu, np.nan); S["taban_alt10"] = np.where(np.isfinite(S.fark), ta, np.nan)
    u, a = U.uc_ust_alt(S.sira.to_numpy(float), UC2_ESIK["ust_pay"], UC2_ESIK["alt_pay"])
    S["ust10"] = u; S["alt10"] = a; S["ufuk"] = int(H)
    return S, say, {"Pn": Pn, "exd": exd, "exj": exj}


def uc2_egri(H: int, hc: str, guc60: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Güç eğrisi: H 15 / 30 cetvel2_guc_v2.2.json (ABD x hücre); H 60 hazırlıkta hesaplanan (aynı yöntem)."""
    import CETVEL2 as C2
    if int(H) in (15, 30, 45):
        return C2._c2_egri22_al(UC2_ESIK["pazar"], hc, int(H), None)
    if guc60 is None:
        yol = os.path.join(UC2_YOL["cikti"], UC2_DOSYA["hazirlik"])
        guc60 = json.load(open(yol, encoding="utf-8"))["guc60"] if os.path.exists(yol) else None
    if not guc60:
        return None
    return guc60.get("egri", {}).get(hc) or guc60.get("egri", {}).get("acik")


def uc2_guc60(veri: Optional[str] = None) -> Dict[str, Any]:
    """R60 güç eğrisi: C2.c2_hazirlik22 yöntemi AYNEN (DS ANA olayları c2_ds_olay_acik_v2.2, c2_olay tekil 60, c2_es, c2_guc_egri; tohum_ek =
    pazar 0 x 100 + hücre x 10 + ufuk sırası 3). Yalnız FARK yayılımı (sigma(n)); ortalama kullanılmaz."""
    import CETVEL2 as C2
    Pn = C2.c2_panel22_al(UC2_ESIK["pazar"], veri or UC2_YOL["acik"], 60)
    X, say = C2.c2_olay(C2.c2_ds_olay22(UC2_ESIK["pazar"]), Pn, tekil_gun=60); X["donem"] = C2._c2_donem22(X.giris)
    e = C2.c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float))
    dn = X.donem.to_numpy(); eg = {}
    for hi, h in enumerate(C2.C2_ESIK22["guc"]["hucre"]):
        msk = np.isin(dn, C2.C2_HUCRE22) if h == "acik" else (dn == h)
        eg[h] = C2.c2_guc_egri(e["fark"][msk], tohum_ek=0 * 100 + hi * 10 + 3)
        eg[h]["n_olay_r"] = int((msk & np.isfinite(X.r15.to_numpy(float))).sum())
    return {"yontem": "C2.c2_hazirlik22 (H = 60)", "egri": eg, "huni": {k: v for k, v in say.items() if k != "donem"}}


def uc2_grup_maske(S: pd.DataFrame) -> Dict[str, np.ndarray]:
    R, B, I = (S[c].to_numpy(float) for c in ("R", "B", "I")); N = S.N.to_numpy(float)
    G = {"HEPSI": np.ones(len(S), bool)}
    for k, v in (("R", R), ("B", B), ("I", I)):
        G[f"{k}=1"] = v == 1; G[f"{k}=0"] = v == 0
    if "Bm" in S.columns:
        G["Bm=1"] = S.Bm.to_numpy(float) == 1
    for n_ in range(4):
        G[f"N={n_}"] = N == n_
    G["N>=2"] = N >= 2
    G["R∧B"] = (R == 1) & (B == 1); G["R∧I"] = (R == 1) & (I == 1); G["B∧I"] = (B == 1) & (I == 1)
    return G


def uc2_hucre(S: pd.DataFrame, m: np.ndarray, hc: str, tohum_ek: int, PL: Optional[Dict[str, Any]], egri: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """UC_IZ.uc_hucre ile AYNI hesap; tek fark güç eğrisi parametre (UC_IZ ufuk 15'e sabit). test_uc_iz2: H 15'te uc_hucre ile birebir."""
    import CETVEL2 as C2
    import MACD_UYUM as MU
    mm = m & (S.donem.to_numpy() == hc) & np.isfinite(S.fark.to_numpy(float))
    x = S[mm]; out: Dict[str, Any] = {"n": int(mm.sum())}
    if len(x) < 2:
        out.update({"hukum": "ÖLÇÜLEMEDİ", "fark": float(x.fark.mean()) if len(x) else np.nan})
        return out
    ay = pd.to_datetime(x.giris).dt.strftime("%Y-%m").to_numpy()
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15.to_numpy(float), x.sira.to_numpy(float), x.giris.to_numpy(), "+", tohum_ek=tohum_ek, egri=egri)
    c["sira_alt"], c["sira_ust"] = MU.mu_sira_boot(x.sira.to_numpy(float), ay, tohum_ek)
    c["plasebo_gecti"] = True       # plasebo HARİÇ hüküm (ön kayıt)
    hk, neden = MU.mu_hukum(c)
    du = x.ust10.to_numpy(float) - x.taban_ust10.to_numpy(float); da = x.alt10.to_numpy(float) - x.taban_alt10.to_numpy(float)
    ua, uu = MU.mu_sira_boot(du, ay, tohum_ek + 7); aa, au = MU.mu_sira_boot(da, ay, tohum_ek + 11)
    out.update({k: c.get(k) for k in ("fark", "med", "boot_alt", "boot_ust", "sira", "sira_alt", "l3o", "p", "guc", "r15_ort", "es_ort")})
    out.update({"hukum": hk, "neden": neden, "ust10": float(np.mean(x.ust10)), "alt10": float(np.mean(x.alt10)),
                "taban_ust_f": float(np.mean(x.taban_ust10)), "taban_alt_f": float(np.mean(x.taban_alt10)),
                "ust_eksi_taban": float(np.mean(du)), "ust_eksi_taban_alt": ua, "ust_eksi_taban_ust": uu,
                "alt_eksi_taban": float(np.mean(da)), "alt_eksi_taban_alt": aa, "alt_eksi_taban_ust": au,
                "n_es_med": float(np.median(x.n_es))})
    if PL is not None:
        U_ = PL["U"][mm]; A_ = PL["A"][mm]
        out["taban_ust_p"] = float(np.nanmean(np.nanmean(U_, axis=0))); out["taban_alt_p"] = float(np.nanmean(np.nanmean(A_, axis=0)))
        out["ust_eksi_taban_p"] = out["ust10"] - out["taban_ust_p"]; out["alt_eksi_taban_p"] = out["alt10"] - out["taban_alt_p"]
    yuk = x.es_r15.to_numpy(float) > 0
    out["fark_piy_yukari"] = float(np.mean(x.fark.to_numpy(float)[yuk])) if yuk.any() else np.nan
    out["fark_piy_asagi"] = float(np.mean(x.fark.to_numpy(float)[~yuk])) if (~yuk).any() else np.nan
    out["n_piy_yukari"] = int(yuk.sum())
    return out


def uc2_sayim(Sd: Dict[int, pd.DataFrame], guc60: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Getirisiz sayım: ufuk x hücre x grup eşli olay sayısı (R_H ölçülebilir ve >= 5 eş) + beklenen güç; R / B / İ örtüşmesi (phi). Getiri
    değeri OKUNMAZ (yalnız sonlu / sonsuz)."""
    import CETVEL2 as C2
    out: Dict[str, Any] = {}
    for H, S in Sd.items():
        ol = np.isfinite(S.fark.to_numpy(float)); G = uc2_grup_maske(S); o: Dict[str, Any] = {"olay_c2": int(len(S)), "esli": int(ol.sum())}
        for hc in UC2_ESIK["donem"]:
            m = ol & (S.donem.to_numpy() == hc); eg = uc2_egri(H, hc, guc60)
            o[hc] = {g: {"n": int((mk & m).sum()), "guc": C2.c2_guc(int((mk & m).sum()), eg) if (mk & m).sum() and eg else 0.0}
                     for g, mk in G.items()}
        o["dis"] = int((ol & (S.donem.to_numpy() == "dis")).sum())
        x = S[ol]
        ph = {}
        for a, b in (("R", "B"), ("R", "I"), ("B", "I")):
            ph[f"{a}_{b}_phi"] = float(np.corrcoef(x[a], x[b])[0, 1]) if len(x) > 2 and x[a].std() and x[b].std() else None
        o["ortusme"] = ph
        out[str(H)] = o
    return out


# ================================================================ 9) DOĞRULAMALAR (getirisiz)
def _u2_panel_fark_gun(Pa: Dict[str, Any], Pk: Dict[str, Any], son: pd.Timestamp) -> Tuple[set, Dict[str, int]]:
    """Tam (Pa) ve kesik (Pk) CETVEL2 taban panellerinde <= son günlerde KV / LQ / havuz (ok) farkı olan günler (ortak semboller) + yalnız tamda
    olup havuzda (KV >= 0) olan sembollerin günleri. Döner gün kümesi ve sayımlar."""
    ia, ik = Pa["P"]["tarih"], Pk["P"]["tarih"]; n = int(ik.searchsorted(son, side="right"))
    if not ia[:n].equals(ik[:n]):
        raise UC2Hata("prefix: panel takvimleri <= son günlerde aynı değil")
    ca = np.array([Pa["P"]["kol"][s] for s in Pk["P"]["sembol"]])
    fk = Pa["KV"][:n][:, ca] != Pk["KV"][:n]
    fl = Pa["LQ"][:n][:, ca] != Pk["LQ"][:n]
    fo = Pa["P"]["ok"][:n][:, ca] != Pk["P"]["ok"][:n]
    yalniz = np.array([j for s, j in Pa["P"]["kol"].items() if s not in Pk["P"]["kol"]], dtype=np.int64)
    fy = (Pa["KV"][:n][:, yalniz] >= 0) if len(yalniz) else np.zeros((n, 0), bool)
    g = fk.any(axis=1) | fy.any(axis=1)
    return set(pd.DatetimeIndex(ia[:n][g])), {"kv_hucre": int(fk.sum()), "lq_hucre": int(fl.sum()), "ok_hucre": int(fo.sum()),
                                              "yalniz_tam_havuz_hucre": int(fy.sum()), "fark_gun": int(g.sum()), "gun": n}


def uc2_prefix(O: Dict[str, Any], kesik: str = "2019-06-28") -> Dict[str, Any]:
    """K2 PREFIX: açık kopya kesik tarihinde kesilip diske yazılır, olaylar ve bayraklar baştan hesaplanır (E2 hariç); t <= kesik - 30 gün olan
    E1 olaylarında küme ve R / B / İ / P2 / BVAL karşılaştırılır. KATI: hepsi aynı. AYRIŞTIRMA: B / BVAL farkları yalnız CETVEL2 taban panelinin
    (OC.oc_veri min_bar 80 bütün seri süzgeci -> kesitsel likidite / havuz) KV satırının değiştiği günlerde mi (tam ve kesik panel karşılaştırılır).
    Geçme (hazırlıkta yazıldı, SAPMA S7): küme / R / İ / P2 birebir VE B / BVAL farkının hepsi panel farkı günlerinde VE B değişimi <= %0,1."""
    import CETVEL2 as C2
    k = pd.Timestamp(kesik); kl = os.path.join(UC2_YOL["gecici"], "acik_kes"); son = k - pd.Timedelta(days=30)
    Pa = C2.c2_panel22_al(UC2_ESIK["pazar"], UC2_YOL["acik"], None)
    V = pd.read_pickle(os.path.join(UC2_YOL["acik"], "V_ABD.pkl"))
    W, _ = uc2_kes_fiyat(V, kesik=k); del V
    os.makedirs(kl, exist_ok=True); _u2_pkl_yaz(os.path.join(kl, "V_ABD.pkl"), W); del W
    C2._C2_PN22.clear()
    try:
        import KASA as KS
        KS.kasa_kapisi([os.path.join(kl, "V_ABD.pkl")], kesik)
        Ok = uc2_olaylar(kl, e2=False)
        Pk = C2._C2_PN22[("baz", UC2_ESIK["pazar"])]
        gunler, pf = _u2_panel_fark_gun(Pa, Pk, son)
    finally:
        C2._C2_PN22.clear()
    del Pa
    kol = ["sembol", "tarih", "R", "B", "I", "p2", "bval", "Bm"]
    A = O["E1"][pd.to_datetime(O["E1"].tarih) <= son][kol].reset_index(drop=True)
    B = Ok["E1"][pd.to_datetime(Ok["E1"].tarih) <= son][kol].reset_index(drop=True)
    M = A.merge(B, on=["sembol", "tarih"], how="outer", suffixes=("_tam", "_kes"), indicator=True)
    ay = M[M._merge == "both"].copy()
    fark = {c: int((ay[f"{c}_tam"].fillna(-9) != ay[f"{c}_kes"].fillna(-9)).sum()) for c in ("R", "B", "I", "p2", "Bm")}
    bt, bk = ay.bval_tam.to_numpy(float), ay.bval_kes.to_numpy(float)
    bfm = (np.abs(bt - bk) > 1e-9) | (np.isnan(bt) != np.isnan(bk))
    bfm &= ~(np.isnan(bt) & np.isnan(bk))
    fark["bval_1e9"] = int(bfm.sum())
    bdeg = (ay.B_tam.fillna(-9) != ay.B_kes.fillna(-9)).to_numpy() | (ay.Bm_tam.fillna(-9) != ay.Bm_kes.fillna(-9)).to_numpy() | bfm
    gun_ok = pd.to_datetime(ay.tarih).isin(gunler).to_numpy()
    J = {"kesik": kesik, "son": str(son.date()), "tam": int(len(A)), "kesik_n": int(len(B)), "yalniz_tam": int((M._merge == "left_only").sum()),
         "yalniz_kesik": int((M._merge == "right_only").sum()), "fark": fark, "panel_fark": pf,
         "b_fark_panel_gununde": int((bdeg & gun_ok).sum()), "b_fark_panel_disi": int((bdeg & ~gun_ok).sum()),
         "b_degisim_pay": float(fark["B"] / max(len(ay), 1))}
    J["tuttu_kati"] = bool(J["yalniz_tam"] == 0 and J["yalniz_kesik"] == 0 and not any(fark.values()))
    J["tuttu"] = bool(J["yalniz_tam"] == 0 and J["yalniz_kesik"] == 0 and fark["R"] == 0 and fark["I"] == 0 and fark["p2"] == 0
                      and J["b_fark_panel_disi"] == 0 and J["b_degisim_pay"] <= 0.001)
    return J


def uc2_d3(O: Dict[str, Any], tohum: int = 3312) -> Dict[str, Any]:
    """K10: 10 rastgele A1 satırı ham zip'ten (NONDERIV_TRANS P / A toplamı, SUBMISSION alanları) yeniden; 10 rastgele E1 olayının ham
    submissions satırı (erişim no, kabul UTC, form, madde) ve hesaplanan NY saati / D0 / t (elle okunur)."""
    import UC_IZ as U  # noqa: F401  (çakışma kapısı sırası)
    rng = np.random.default_rng(tohum); A1 = _u2_a1(); out: Dict[str, Any] = {"A1": [], "E1": []}
    sec = A1.iloc[rng.choice(len(A1), size=10, replace=False)]
    zips = {f[:6]: os.path.join(UC2_YOL["form345"], f) for f in sorted(os.listdir(UC2_YOL["form345"])) if f.endswith("_form345.zip")}
    for r in sec.itertuples():
        q = f"{r.D.year}q{(r.D.month - 1) // 3 + 1}"; z = zipfile.ZipFile(zips[q])
        S = pd.read_csv(z.open("SUBMISSION.tsv"), sep="\t", dtype=str); S = S[S.ACCESSION_NUMBER == r.ACCESSION_NUMBER]
        T = pd.read_csv(z.open("NONDERIV_TRANS.tsv"), sep="\t", dtype=str, low_memory=False); T = T[T.ACCESSION_NUMBER == r.ACCESSION_NUMBER]
        T = T[(T.TRANS_CODE == "P") & (T.TRANS_ACQUIRED_DISP_CD == "A")]
        dg = float((pd.to_numeric(T.TRANS_SHARES, errors="coerce") * pd.to_numeric(T.TRANS_PRICEPERSHARE, errors="coerce")).sum())
        out["A1"].append({"acc": r.ACCESSION_NUMBER, "sembol": r.sembol, "D": str(r.D.date()), "deger": float(r.deger), "issuer_cik": int(r.issuer_cik),
                          "ham_filing_date": S.FILING_DATE.iloc[0] if len(S) else None, "ham_doc": S.DOCUMENT_TYPE.iloc[0] if len(S) else None,
                          "ham_issuer_cik": S.ISSUERCIK.iloc[0] if len(S) else None, "ham_sembol": S.ISSUERTRADINGSYMBOL.iloc[0] if len(S) else None,
                          "ham_deger": dg, "ham_satir_P": int(len(T)), "tutar": bool(len(S) and abs(dg - float(r.deger)) < 1e-6)})
    E1 = O["E1"]; sec = E1.iloc[rng.choice(len(E1), size=10, replace=False)]
    for r in sec.itertuples():
        out["E1"].append({"sembol": r.sembol, "cik": int(r.cik), "acc": r.accessionNumber, "kabul_utc": r.acceptanceDateTime, "kabul_ny": r.kabul_ny,
                          "filingDate": r.filingDate, "items": r.items, "D0": str(pd.Timestamp(r.D0).date()), "t": str(pd.Timestamp(r.tarih).date())})
    out["A1_tutar"] = int(sum(x["tutar"] for x in out["A1"]))
    return out


# ================================================================ 10) KOMUTLAR: hazırla / kapı / koş
UC2_E2_KOL = ["sembol", "tarih", "cik", "R", "B", "I", "N"]
UC2_KARAR_GRUP = ["R=1", "B=1", "I=1", "N>=2"]


def uc2_e2_ex(O: Dict[str, Any]) -> pd.DataFrame:
    return O["K02"][["sembol", "tarih"]].copy() if O.get("K02") is not None else pd.DataFrame(columns=["sembol", "tarih"])


def uc2_hazirla(islem: int = 4, prefix: bool = True, veri: Optional[str] = None) -> Dict[str, Any]:
    """Getirisiz: olaylar + bayraklar + R60 güç eğrisi + eşli olay sayımları + güç + D2 prefix + D3 -> olay.pkl + uc_iz2_hazirlik.json."""
    t0 = time.time(); v = veri or UC2_YOL["acik"]
    O = uc2_olaylar(v, islem, e2=True)
    X = uc2_analiz_olay(O["E1"])
    guc60 = uc2_guc60(v)
    Sd: Dict[int, pd.DataFrame] = {}; anahtar: Dict[int, pd.DataFrame] = {}; huni: Dict[str, Any] = {}
    for H in (15, 60, 30):
        S, say, _ = uc2_olc_ufuk(X, O["EX"], H, v)
        Sd[H] = S; anahtar[H] = S[["sembol", "tarih", "giris", "d", "j"]].copy(); huni[str(H)] = say
    sayim = uc2_sayim({15: Sd[15], 60: Sd[60]}, guc60)
    sayim30 = uc2_sayim({30: Sd[30]}, guc60)
    e2s: Dict[str, Any] = {}
    if O.get("X2") is not None:
        for H in (15, 60):
            S2, say2, _ = uc2_olc_ufuk(O["X2"], uc2_e2_ex(O), H, v, tekil=H, kol=UC2_E2_KOL)
            ol = np.isfinite(S2.fark.to_numpy(float))
            e2s[str(H)] = {"huni": say2, **{hc: {g: int((mk & ol & (S2.donem.to_numpy() == hc)).sum()) for g, mk in uc2_grup_maske(S2).items()}
                                           for hc in UC2_ESIK["donem"]}}
    d3 = uc2_d3(O)
    pre = uc2_prefix(O) if prefix else {"durum": "koşulmadı"}
    os.makedirs(UC2_YOL["gecici"], exist_ok=True)
    yol = os.path.join(UC2_YOL["gecici"], UC2_DOSYA["olay"])
    with open(yol + ".tmp", "wb") as f:
        pickle.dump({"E1": O["E1"], "EX": O["EX"], "K02": O["K02"], "X2": O["X2"], "anahtar": anahtar}, f, protocol=4)
    os.replace(yol + ".tmp", yol)
    E1 = O["E1"]
    J: Dict[str, Any] = {"surum": UC2_SURUM, "zaman": _u2_simdi(), "kapi": O["kapi"], "kod_sha": _u2_sha(UC2_YOL["kod"]), "esik_sha": uc2_esik_sha(),
                         "veri_sha": {"V_ABD.pkl (açık)": _u2_sha(os.path.join(v, "V_ABD.pkl")),
                                      UC2_DOSYA["a1"]: _u2_sha(os.path.join(UC2_YOL["ham"], UC2_DOSYA["a1"])),
                                      UC2_DOSYA["k8"]: _u2_sha(os.path.join(UC2_YOL["ham"], UC2_DOSYA["k8"]))},
                         "olay_say": O["say"], "huni_c2": huni, "analiz_olay": int(len(X)),
                         "e1_bayrak": {"R": int(E1.R.sum()), "I": int(E1.I.sum()), "B": int(np.nansum(E1.B.to_numpy(float))),
                                       "Bm": int(np.nansum(E1.Bm.to_numpy(float))), "p2": int(E1.p2.sum())},
                         "guc60": guc60, "sayim": sayim, "sayim30": sayim30, "e2_sayim": e2s, "D2_prefix": pre, "D3": d3,
                         "olay_pkl_sha": _u2_sha(yol), "sure_sn": round(time.time() - t0)}
    _u2_jyaz(os.path.join(UC2_YOL["cikti"], UC2_DOSYA["hazirlik"]), J)
    if prefix and not pre.get("tuttu"):
        raise UC2Hata(f"D2 PREFIX TUTMADI: {pre}")
    return J


def uc2_kapi(onkayit: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm kapısı: IZ_KARNE.ik_kontrol_kapisi + ön kayıttaki KOD_SHA / ESIK_SHA / HAZIRLIK_SHA = şimdiki + ön kayıt commit'li ve değişmemiş."""
    import IZ_KARNE as IK
    yol = onkayit or os.path.join(UC2_YOL["cikti"], UC2_DOSYA["onkayit"])
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise UC2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    beklenen = {"KOD_SHA": _u2_sha(UC2_YOL["kod"]), "ESIK_SHA": uc2_esik_sha(),
                "HAZIRLIK_SHA": _u2_sha(os.path.join(UC2_YOL["cikti"], UC2_DOSYA["hazirlik"]))}
    for ad, val in beklenen.items():
        if f"{ad}: {val}" not in metin:
            raise UC2Hata(f"ön kayıt kapısı: {ad} ön kayıtta yok ya da farklı (şimdiki {val[:12]}) -> DURDU")
    rel = os.path.relpath(yol, KOK_UC2)
    c = _u2_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise UC2Hata("ön kayıt commit'li değil -> DURDU")
    if _u2_git(["status", "--porcelain", "--", rel, os.path.relpath(UC2_YOL["kod"], KOK_UC2)]):
        raise UC2Hata("ön kayıt ya da kod çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **beklenen}


def _u2_p(c: Dict[str, Any]) -> float:
    v = c.get("p", np.nan)
    return float(v) if (v is not None and np.isfinite(v) and c.get("n", 0) >= UC2_ESIK["n_min"]) else 1.0


def uc2_kos(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Kapı -> olay.pkl (hazırlıktaki sha) -> ufuk başına ölçüm, plasebo, hücre, karar -> BH -> E2 bilgi -> satır / sonuç dosyaları."""
    import gc
    import CETVEL2 as C2
    import UC_IZ as U
    t0 = time.time(); bas = _u2_simdi(); v = veri or UC2_YOL["acik"]; cikti = cikti or UC2_YOL["cikti"]
    if os.path.exists(os.path.join(cikti, UC2_DOSYA["sonuc"])):
        raise UC2Hata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = uc2_kapi(os.path.join(cikti, UC2_DOSYA["onkayit"]))
    kp = uc2_kesik_kapi(v)
    Hz = json.load(open(os.path.join(cikti, UC2_DOSYA["hazirlik"]), encoding="utf-8"))
    yol = os.path.join(UC2_YOL["gecici"], UC2_DOSYA["olay"])
    if _u2_sha(yol) != Hz["olay_pkl_sha"]:
        raise UC2Hata("olay.pkl hazırlıktaki sha ile aynı değil -> DURDU")
    O = pd.read_pickle(yol); X = uc2_analiz_olay(O["E1"]); guc60 = Hz["guc60"]
    hucreler = list(UC2_ESIK["donem"]); R: Dict[str, Any] = {}; Ssat: Dict[int, pd.DataFrame] = {}
    for H in (15, 60, 30):
        S, say, ctx = uc2_olc_ufuk(X, O["EX"], H, v)
        if not S[["sembol", "tarih", "giris", "d", "j"]].reset_index(drop=True).equals(O["anahtar"][H].reset_index(drop=True)):
            raise UC2Hata(f"R{H}: olay anahtarları hazırlıktakiyle aynı değil -> DURDU")
        Pn = ctx["Pn"]; PL = U.uc_plasebo(Pn, S, ctx)
        S["plasebo_ust10"] = np.nanmean(PL["U"], axis=1); S["plasebo_alt10"] = np.nanmean(PL["A"], axis=1)
        Gm = uc2_grup_maske(S); Hc: Dict[str, Dict[str, Any]] = {}
        for gi, (g, m) in enumerate(Gm.items()):
            for hi, hc in enumerate(hucreler + ["dis"]):
                Hc[f"{g}|{hc}"] = uc2_hucre(S, m, hc, 600000 + H * 1000 + gi * 10 + hi, PL, uc2_egri(H, hc if hc != "dis" else "acik", guc60))
        if H in UC2_ESIK["ufuk_karar"]:
            for g in UC2_KARAR_GRUP:
                for hc in hucreler:
                    c = Hc[f"{g}|{hc}"]
                    if c.get("hukum") == "TUTAR":
                        mm = Gm[g] & (S.donem.to_numpy() == hc) & np.isfinite(S.fark.to_numpy(float))
                        pl = C2.c2_plasebo(Pn, S.d.to_numpy(np.int64)[mm], "+", uc2_egri(H, hc, guc60), tohum_ek=777, iki_yon_ayri=True)
                        c["c2_plasebo"] = {"fark_ort": pl["fark_ort"], "tutar_pay_arti": pl["tutar_pay_arti"], "gecti_arti": pl["gecti_arti"]}
            K = {iz: U.uc_iz_karar(Hc, iz) for iz in UC2_ESIK["iz"]}
            Bk = U.uc_birlikte(Hc)
            yt = [iz for iz in UC2_ESIK["iz"] if K[iz]["yon_tutarli"]]
            R[str(H)] = {"hucre": Hc, "iz_karar": K, "birlikte": Bk, "yon_tutarli": yt, "kasa_adayi": bool(len(yt) >= 2 and Bk["birlikte_artiyor"]),
                         "huni": say, "plasebo_aday_yok": PL["aday_yok"]}
        else:
            R[str(H)] = {"hucre": Hc, "huni": say, "plasebo_aday_yok": PL["aday_yok"], "durum": "BİLGİ"}
        Ssat[H] = S
        del PL; gc.collect()
        u2log.info("R%d bitti (%.0f sn)", H, time.time() - t0)
    aile = [(iz, H) for H in (60, 15) for iz in ["R", "B", "I", "N>=2"]]
    ps = [max(_u2_p(R[str(H)]["hucre"][f"{'N>=2' if iz == 'N>=2' else iz + '=1'}|{hc}"]) for hc in hucreler) for iz, H in aile]
    bh = C2.c2_bh(ps, UC2_ESIK["bh_q"])
    # E2 (bilgi)
    E2: Dict[str, Any] = {}
    if O.get("X2") is not None:
        for H in (15, 60):
            S2, say2, _ = uc2_olc_ufuk(O["X2"], uc2_e2_ex(O), H, v, tekil=H, kol=UC2_E2_KOL)
            G2 = uc2_grup_maske(S2)
            E2[str(H)] = {"huni": say2, "hucre": {f"{g}|{hc}": uc2_hucre(S2, m, hc, 700000 + H * 1000 + gi * 10 + hi, None, uc2_egri(H, hc, guc60))
                                                 for gi, (g, m) in enumerate(G2.items()) for hi, hc in enumerate(hucreler)
                                                 if g in ("HEPSI", "R=1", "B=1", "I=1", "N=0", "N=1", "N>=2")}}
    # satır dosyası (olay x iz bayrakları x R15 / R60 / R30 / eş)
    taban = ["sembol", "cik", "tarih", "giris", "donem", "R", "B", "I", "N", "Bm", "ear", "atrp20", "bval", "i_say", "accessionNumber", "kabul_ny"]
    ol = ["r15", "es_r15", "n_es", "sira", "fark", "taban_ust10", "taban_alt10", "ust10", "alt10", "plasebo_ust10", "plasebo_alt10"]
    Z = Ssat[15][[c for c in taban if c in Ssat[15].columns] + ol].rename(columns={c: f"{c}_15" for c in ol})
    for H in (60, 30):
        Y = Ssat[H][["sembol", "tarih"] + ol].rename(columns={c: f"{c}_{H}" for c in ol})
        Z = Z.merge(Y, on=["sembol", "tarih"], how="outer", validate="one_to_one")
    Z = Z.rename(columns={"r15_15": "R15", "r15_60": "R60", "r15_30": "R30", "es_r15_15": "es_R15", "es_r15_60": "es_R60", "es_r15_30": "es_R30"})
    en_gec = max(pd.to_datetime(Z.giris).max(), pd.to_datetime(Z.tarih).max())
    if en_gec > UC2_KESIK:
        raise UC2Hata(f"KESİK AŞIMI: {en_gec}")
    for c in ("tarih", "giris"):
        Z[c] = pd.to_datetime(Z[c]).dt.strftime("%Y-%m-%d")
    Z = Z.sort_values(["tarih", "sembol"], kind="mergesort").reset_index(drop=True)
    tmp = os.path.join(UC2_YOL["gecici"], UC2_DOSYA["satir"])
    Z.to_csv(tmp, index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.10g")
    boy = os.path.getsize(tmp); hedef = cikti if boy <= 5_000_000 else UC2_YOL["ham"]
    ys = os.path.join(hedef, UC2_DOSYA["satir"]); os.makedirs(hedef, exist_ok=True); os.replace(tmp, ys)
    J = {"surum": UC2_SURUM, "baslangic": bas, "bitis": _u2_simdi(), "sure_sn": round(time.time() - t0), "kapi": G0, "kesik_kapi": kp,
         "analiz_olay": int(len(X)), "ufuk": R, "bh": {"aile": [f"{iz}|R{H}" for iz, H in aile], "p": ps, "gecti": bh}, "e2_bilgi": E2,
         "avrupa": "AVRUPA VERİSİ YOK (SEC Form 4 / 8-K yalnız ABD); karar en fazla ABD-ADAY",
         "kasa_adayi": {str(H): R[str(H)]["kasa_adayi"] for H in UC2_ESIK["ufuk_karar"]},
         "satir": {"yol": ys, "sha": _u2_sha(ys), "boy": boy, "satir": int(len(Z))}, "en_gec": str(en_gec.date())}
    _u2_jyaz(os.path.join(cikti, UC2_DOSYA["sonuc"]), J)
    u2log.info("bitti: kasa adayı %s (%.0f sn)", J["kasa_adayi"], time.time() - t0)
    return J


# ================================================================ 11) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_uc2(_once=_CK_ONCE_UC2, _dosya="UC_IZ2.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_UC2",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_uc2()


def _uc2_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="UC_IZ2: üç iz aynı bilanço olayında (ABD 2016-22)")
    ap.add_argument("komut", choices=["sec_form4", "sec_8k", "acik", "t2", "hazirla", "kos", "sha"])
    ap.add_argument("--islem", type=int, default=4); ap.add_argument("--prefix_yok", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps({"KOD_SHA": _u2_sha(UC2_YOL["kod"]), "ESIK_SHA": uc2_esik_sha()}, indent=1))
        elif a.komut == "sec_form4":
            J = uc2_sec_form4(); print(json.dumps(_u2_json({k: v for k, v in J.items() if k != "zip"}), ensure_ascii=False)[:4000])
        elif a.komut == "sec_8k":
            print(json.dumps(_u2_json(uc2_sec_8k()), ensure_ascii=False)[:4000])
        elif a.komut == "acik":
            print(json.dumps(_u2_json(uc2_acik_kopya()), ensure_ascii=False)[:4000])
        elif a.komut == "t2":
            J = uc2_t2_dogrulama(); print(json.dumps(_u2_json({k: J[k] for k in ("secilen", "tablo", "gecti")}), ensure_ascii=False)[:6000])
        elif a.komut == "hazirla":
            J = uc2_hazirla(a.islem, prefix=not a.prefix_yok)
            print(json.dumps(_u2_json({k: J[k] for k in ("olay_say", "e1_bayrak", "analiz_olay", "D2_prefix")}), ensure_ascii=False)[:6000])
        else:
            J = uc2_kos()
            print(json.dumps(_u2_json({"kasa_adayi": J["kasa_adayi"], "bh": J["bh"],
                                       "karar": {H: {iz: r["iz_karar"][iz]["karar"] for iz in UC2_ESIK["iz"]} for H, r in J["ufuk"].items()
                                                 if "iz_karar" in r}}), ensure_ascii=False)[:6000])
    except UC2Hata as ex:
        u2log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_uc2_ana())
