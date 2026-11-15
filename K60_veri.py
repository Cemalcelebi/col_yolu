"""K60_veri — K60 VERİ HAZIRLIĞI, tek dosya (11 Kasım 2026; ana oturum iş tanımı, yol haritası bölüm 5). SİNYAL ÖLÇÜMÜ YOK, getiri istatistiği YOK.

Sorun: K59 temel veriye dayalı sinyalleri yalnız 66 ayda (2021-26) ölçebildi; SEC frames önbelleği 2020Q1-2026Q2, geniş evren fiyatları 2020'den.
K60 (KEŞİF 2016-2021 / DOĞRULAMA 2022-2023 / KASA 2024 - Ağu 2026) için temel veri 2009'dan, fiyat 2010'dan gerekir. Bu dosya yalnız veriyi
hazırlar: indirme planı, SEC XBRL frames indirici, Yahoo günlük fiyat indirici, denetim (sha256 manifesti, şirket sayıları) ve özet.

Komut:  python K60_veri.py plan           indirme planını yazar (arastirma_cikti/k60_veri/K60_VERI_PLANI.md + K60_SEC_ISTEK_LISTESI.csv); ağ yok
        K60_SEC_UA='...' python K60_veri.py indir_sec [--dizin evet] [--ek hayir]
                                          SEC frames -> /tmp/k60_secframes (saniyede en çok 8 istek, kaldığı yerden sürer). Kimlik satırı
                                          (User-Agent) YALNIZ K60_SEC_UA ortam değişkeninden okunur; değişken yoksa komut ÇALIŞMAZ (çıkış 2).
                                          Değer koda, günlüğe, manifeste, durum dosyasına yazılmaz (günlükte maskelenir).
        python K60_veri.py indir_fiyat    geniş ABD evreninin (K57-B evreni + V_ABD) Yahoo günlük fiyatları 2010-01-01'den -> /tmp/k60_fiyat
                                          (K57-B ile aynı uç ve tarayıcı kimliği; temettü / bölünme olayları saklanır; kaldığı yerden sürer)
        python K60_veri.py indir_fiyat --yenile kirpik   Yahoo'nun geçmişini eksik verdiği hisseleri yeniden ister (yalnız daha uzun yanıt yazılır)
        python K60_veri.py denetle        manifest sha256 doğrulaması + etiket x dönem şirket sayıları + fiyat kapsamı (K60_VERI_DENETIM.md)
        python K60_veri.py ozet           inenlerin özeti: yıllara göre fiyat paneli, uygun evren, bilinen yanlılıklar (K60_VERI_OZET.md)
Colab:  exec(open('K60_veri.py').read()); k60v_plan()
Veri:   K59 girdilerine DOKUNULMAZ (/tmp/secframes, /tmp/k57b_fiyat yalnız okunur; sha256'ları değişmez). Yeni önbellekler ayrı klasörlerde:
        /tmp/k60_secframes (K60_SECFRAMES ile değişir), /tmp/k60_fiyat (K60_FIYAT ile değişir). Ham SEC / fiyat verisi repoya konmaz.
        Kişisel e-posta / anahtar koda ve çıktılara yazılmaz.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K60V = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import ssl  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
import urllib.error  # noqa: E402
import urllib.parse  # noqa: E402
import urllib.request  # noqa: E402
from concurrent.futures import ThreadPoolExecutor, as_completed  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_K60V = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K60V not in sys.path:
    sys.path.insert(0, KOK_K60V)

import K57  # noqa: E402

K60V_SURUM = "K60_veri v1.0 (2026-11-11): K60 veri hazırlığı (SEC frames 2009-2026, Yahoo günlük fiyat 2010-2026); ölçüm yok"
K60V_UA_DEGISKEN = "K60_SEC_UA"
_K60V_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def k60v_maskele(s: Any) -> str:
    """Metinden e-posta biçimli her parçayı ve K60_SEC_UA değerinin kendisini siler (günlük ve dosya çıktıları için)."""
    s = str(s); ua = os.environ.get(K60V_UA_DEGISKEN, "")
    if ua and ua in s:
        s = s.replace(ua, "<K60_SEC_UA>")
    return _K60V_EPOSTA.sub("<e-posta>", s)


class _K60VGizle(logging.Filter):
    """Günlük süzgeci: her kayıt yazılmadan önce maskelenir (kimlik satırı / e-posta günlüğe düşmez)."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            ham = record.getMessage()
        except Exception:   # biçim hatası günlüğü durdurmasın
            ham = str(record.msg)
        record.msg = k60v_maskele(ham); record.args = ()
        return True


k60vlog = logging.getLogger("col.k60v")
if not k60vlog.handlers:
    _k60v_h = logging.StreamHandler(sys.stderr)
    _k60v_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s k60v: %(message)s", "%H:%M:%S"))
    _k60v_h.addFilter(_K60VGizle())
    k60vlog.addHandler(_k60v_h)
    k60vlog.addFilter(_K60VGizle())
    k60vlog.setLevel(logging.INFO)
    k60vlog.propagate = False

K60V_YOL = {
    "cikti": os.path.join(KOK_K60V, "arastirma_cikti", "k60_veri"),
    "frames": os.environ.get("K60_SECFRAMES", "/tmp/k60_secframes"),      # YENİ SEC frames önbelleği
    "fiyat": os.environ.get("K60_FIYAT", "/tmp/k60_fiyat"),               # YENİ Yahoo önbelleği
    "eski_frames": K57.K57_YOL["frames"],                                 # K59 girdisi: yalnız OKUNUR
    "eski_fiyat": K57.K57B_YOL["fiyat"],                                  # K59 girdisi: yalnız OKUNUR (burada hiç kullanılmaz)
    "veri": K57.K57_YOL["veri"],
    "evren_b1": os.path.join(K57.K57_YOL["cikti"], K57.K57B_DOSYA["b1_evren"]),
    "ca": K57.K57_YOL["ca"],
}
K60V_DOSYA = {"plan": "K60_VERI_PLANI.md", "liste": "K60_SEC_ISTEK_LISTESI.csv", "ozet": "K60_VERI_OZET.md", "denetim": "K60_VERI_DENETIM.md",
              "sec_sayim": "sec_sayim.csv", "fiyat_kapsam": "fiyat_kapsam.csv", "evren_ay": "evren_ay.csv",
              "manifest": "_manifest.json", "durum": "_durum.json", "gunluk": "_gunluk.log", "evren": "_evren.csv"}

K60V_ESIK: Dict[str, Any] = {
    "sec": {"url": "https://data.sec.gov/api/xbrl/frames/{tax}/{etiket}/{birim}/{donem}.json",
            "ceyrek": ("2009Q1", "2026Q2"), "yil": (2009, 2025),            # K60'ın istediği tam aralık
            "mevcut_ceyrek": ("2020Q1", "2026Q2"), "mevcut_yil": (2020, 2025),   # K57 / K59 önbelleğinde olan bölüm (7 etiket)
            "hiz_ust": 8.0, "hiz_pay_sn": 0.005, "is_parcacigi": 4, "deneme": 3, "zaman_asimi": 90, "geri_cekil": 5.0, "ret_kod": [403, 407]},
    "dizin": {"url": "https://www.sec.gov/Archives/edgar/full-index/{yil}/QTR{c}/master.gz", "ceyrek": ("2009Q1", "2026Q3"),
              "form": ["10-K", "10-Q", "10-K/A", "10-Q/A", "10-KT", "10-QT", "10-K405", "20-F", "40-F"]},
    "yahoo": dict(K57.K57B_ESIK["yahoo"], bas="2010-01-01", bit="2026-11-12", kes="2026-08-31", zaman_asimi=40, ret_kod=[407],
                  kirpik_gun=10),
    "uygunluk": {"fiyat_min": 2.0, "likit_min": 1.0e6, "likit_gun": 20, "likit_min_gun": 15, "gecmis_gun": 252, "ileri_tasima": 5,
                 "tur": ["EQUITY"], "takvim_pay": 0.20},
    "donem": {"KEŞİF": ("2016-01", "2021-12"), "DOĞRULAMA": ("2022-01", "2023-12"), "KASA": ("2024-01", "2026-08")},
    "yedek_bilgi_gun": 90,
    "boyut_mb": {"an": 0.60, "ceyrek": 0.35, "yil": 0.55, "dizin": 8.0},   # önbellek yoksa kullanılan kaba ortalamalar
}

# (grup, taksonomi, etiket, birim, tür, hangi sinyaller için, not). tür: 'an' = çeyrek sonu anlık (CYyyyyQnI); 'sure' = çeyreklik (CYyyyyQn)
# + yıllık (CYyyyy); 'yil' = YALNIZ yıllık. Grup A = K57 / K59'un kullandığı etiketler (2020+ bölümü eski önbellekte), B = yeni bilanço ve
# gelir tablosu etiketleri, C = nakit akış kalemleri (yalnız yıllık güvenilir), EK = iş tanımındaki listede olmayan, alt ajanın gerekçeli eki.
K60V_ETIKET: List[Tuple[str, str, str, str, str, str, str]] = (
    [("A", "us-gaap", t, "USD", "sure", "REV_SURP, satış ivmesi, GP_A payı", "gelir etiketi (üçünden biri dolu olur)") for t in K57.K57_ABD_GELIR]
    + [("A", "us-gaap", "NetIncomeLoss", "USD", "sure", "ROE_TTM, ROA_Q, SUE_SRW, EP, ACCRUALS", "")]
    + [("A", "us-gaap", "StockholdersEquity", "USD", "an", "ROE_TTM, BM", ""),
       ("A", "us-gaap", "Liabilities", "USD", "an", "kaldıraç (X2), F_SCORE", ""),
       ("A", "us-gaap", "LiabilitiesAndStockholdersEquity", "USD", "an", "toplam varlık yedeği", "Assets ile aynı sayı (bilanço eşitliği)"),
       ("A", "dei", "EntityCommonStockSharesOutstanding", "shares", "an", "NSI_1Y, piyasa değeri (BM, EP, CFP, küçüklük)",
        "kapak sayfası pay sayısı; eski önbellekte YOK, tam aralık iner; tarih çeyrek sonu değil kapak günüdür"),
       ("B", "us-gaap", "Assets", "USD", "an", "ASSET_G, ROA_Q, GP_A, ACCRUALS, F_SCORE", ""),
       ("B", "us-gaap", "AssetsCurrent", "USD", "an", "F_SCORE (cari oran)", "banka / sigorta bildirmez"),
       ("B", "us-gaap", "LiabilitiesCurrent", "USD", "an", "F_SCORE (cari oran)", "banka / sigorta bildirmez"),
       ("B", "us-gaap", "CashAndCashEquivalentsAtCarryingValue", "USD", "an", "RUNWAY", ""),
       ("B", "us-gaap", "LongTermDebt", "USD", "an", "F_SCORE (kaldıraç)", "LongTermDebtNoncurrent ile dönüşümlü"),
       ("B", "us-gaap", "LongTermDebtNoncurrent", "USD", "an", "F_SCORE (kaldıraç)", "LongTermDebt ile dönüşümlü"),
       ("B", "us-gaap", "GrossProfit", "USD", "sure", "GP_A, F_SCORE (brüt marj)", "yoksa gelir - maliyet"),
       ("B", "us-gaap", "CostOfRevenue", "USD", "sure", "GP_A", "CostOfGoodsAndServicesSold ile dönüşümlü"),
       ("B", "us-gaap", "CostOfGoodsAndServicesSold", "USD", "sure", "GP_A", "CostOfRevenue ile dönüşümlü"),
       ("B", "us-gaap", "OperatingIncomeLoss", "USD", "sure", "kârlılık ailesi (ikinci dalga)", ""),
       ("B", "us-gaap", "ResearchAndDevelopmentExpense", "USD", "sure", "kârlılık / yatırım ailesi (ikinci dalga)", ""),
       ("B", "us-gaap", "IncomeTaxExpenseBenefit", "USD", "sure", "kârlılık ailesi (ikinci dalga)", ""),
       ("B", "us-gaap", "DepreciationDepletionAndAmortization", "USD", "sure", "ACCRUALS (bilanço yöntemi), nakit kâr",
        "çoğu şirkette nakit akış tablosu kalemi: ÇEYREKLİK EKSİK, YILLIK güvenilir"),
       ("C", "us-gaap", "NetCashProvidedByUsedInOperatingActivities", "USD", "yil", "CFP, ACCRUALS, F_SCORE, RUNWAY", "YALNIZ YILLIK"),
       ("C", "us-gaap", "PaymentsToAcquirePropertyPlantAndEquipment", "USD", "yil", "yatırım ailesi", "YALNIZ YILLIK"),
       ("C", "us-gaap", "PaymentsForRepurchaseOfCommonStock", "USD", "yil", "NET_PAYOUT_YLD", "YALNIZ YILLIK"),
       ("C", "us-gaap", "ProceedsFromIssuanceOfCommonStock", "USD", "yil", "NET_PAYOUT_YLD", "YALNIZ YILLIK"),
       ("EK", "us-gaap", "PaymentsOfDividends", "USD", "yil", "NET_PAYOUT_YLD (envanter satır 48 temettü ister)", "YALNIZ YILLIK"),
       ("EK", "us-gaap", "PaymentsOfDividendsCommonStock", "USD", "yil", "NET_PAYOUT_YLD", "PaymentsOfDividends ile dönüşümlü; YALNIZ YILLIK"),
       ("EK", "us-gaap", "CommonStockSharesOutstanding", "shares", "an", "NSI_1Y, piyasa değeri (yedek)",
        "bilanço günü pay sayısı; kapak sayısı olmayan / çok sınıflı şirketler için yedek"),
       ("EK", "us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding", "shares", "sure", "NSI_1Y, piyasa değeri (yedek)",
        "ağırlıklı ortalama pay; çok sınıflı şirketlerde tek boyutsuz pay sayısı çoğunlukla budur")])


class K60VHata(RuntimeError):
    """K60_veri: beklenen, açıklaması olan durma (eksik girdi, eksik kimlik, bozuk önbellek)."""


class K60VKimlikYok(K60VHata):
    """K60_SEC_UA tanımlı değil: SEC indirmesi başlamaz."""


def _k60v_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _k60v_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or K60V_YOL["cikti"], K60V_DOSYA[ad])


def _bn(x: Any) -> str:
    """Tam sayı -> binlik ayraçlı Türkçe yazım (1.234); sayı değilse '—'."""
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "—"
        return f"{int(round(float(x))):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "—"


def _on(x: Any, n: int = 1) -> str:
    """Ondalıklı sayı -> Türkçe yazım (virgül)."""
    try:
        return f"{float(x):.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "—"


def _k60v_yaz(yol: str, metin: str) -> str:
    """Metin dosyası (maskeli, atomik)."""
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol + ".yarim", "w", encoding="utf-8") as f:
        f.write(k60v_maskele(metin))
    os.replace(yol + ".yarim", yol)
    return yol


# ---------------------------------------------------------------- 1) İSTEK LİSTELERİ (ağ yok)
def _k60v_ceyrekler(a: str, b: str) -> List[Tuple[int, int]]:
    return [(p.year, p.quarter) for p in pd.period_range(a, b, freq="Q")]


def k60v_donemler(tur: str) -> List[str]:
    """Bir etiket türünün K60 için istenen bütün dönemleri."""
    S = K60V_ESIK["sec"]
    c = [f"CY{y}Q{q}" for y, q in _k60v_ceyrekler(*S["ceyrek"])]
    yl = [f"CY{y}" for y in range(S["yil"][0], S["yil"][1] + 1)]
    if tur == "an":
        return [x + "I" for x in c]
    if tur == "sure":
        return c + yl
    if tur == "yil":
        return yl
    raise K60VHata(f"bilinmeyen etiket türü: {tur}")


def _k60v_donem_turu(donem: str) -> str:
    return "an" if donem.endswith("I") else ("yil" if re.fullmatch(r"CY\d{4}", donem) else "ceyrek")


def _k60v_eski_yol(tax: str, etiket: str, donem: str, eski: Optional[str]) -> Optional[str]:
    """K57 / K59 önbelleğinde (yalnız okunur) bu çerçeve var mı? Ad kuralı K57 ile aynı: us-gaap_<etiket>_<dönem>.json."""
    if not eski:
        return None
    y = os.path.join(eski, f"{tax}_{etiket}_{donem}.json")
    return y if os.path.exists(y) and os.path.getsize(y) >= 2 else None


def k60v_sec_listesi(ek: bool = True, eski_klasor: Optional[str] = None) -> List[Dict[str, Any]]:
    """K60'ın istediği bütün SEC frames çerçeveleri (sıra sabit). Her satır: grup, tax, etiket, birim, tur, donem, url, dosya,
    mevcut (eski önbellekteki yol ya da None). 'mevcut' olanlar İNDİRİLMEZ; eski önbellek yoksa aynı çerçeve yeni klasöre iner."""
    eski = K60V_YOL["eski_frames"] if eski_klasor is None else eski_klasor
    out: List[Dict[str, Any]] = []; gorulen = set()
    for grup, tax, etiket, birim, tur, icin, nt in K60V_ETIKET:
        if grup == "EK" and not ek:
            continue
        for donem in k60v_donemler(tur):
            ad = f"{tax}_{etiket}_{donem}.json"
            if ad in gorulen:
                raise K60VHata(f"istek listesinde yinelenen çerçeve: {ad}")
            gorulen.add(ad)
            out.append({"grup": grup, "tax": tax, "etiket": etiket, "birim": birim, "tur": tur, "donem": donem, "ad": f"{etiket}/{donem}",
                        "url": K60V_ESIK["sec"]["url"].format(tax=tax, etiket=etiket, birim=birim, donem=donem), "dosya": ad,
                        "mevcut": _k60v_eski_yol(tax, etiket, donem, eski), "icin": icin, "not": nt})
    return out


def k60v_dizin_listesi() -> List[Dict[str, Any]]:
    """EDGAR çeyreklik başvuru dizini (master.gz): CIK | şirket | form | başvuru günü | dosya. İsteğe bağlı (indir_sec --dizin evet);
    frames'te olmayan özgün başvuru gününü (10-Q / 10-K) verir."""
    D = K60V_ESIK["dizin"]
    return [{"grup": "DIZIN", "tax": "edgar", "etiket": "master", "birim": "", "tur": "dizin", "donem": f"{y}Q{q}", "ad": f"dizin/{y}Q{q}",
             "url": D["url"].format(yil=y, c=q), "dosya": f"edgar_master_{y}Q{q}.gz", "mevcut": None, "icin": "bilgi tarihi (filed)", "not": ""}
            for y, q in _k60v_ceyrekler(*D["ceyrek"])]


# ---------------------------------------------------------------- 2) MANİFEST (sha256) + HIZ SINIRI
def k60v_sha(ham: bytes) -> str:
    return hashlib.sha256(ham).hexdigest()


def k60v_dosya_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


class K60VManifest:
    """Önbellek klasörünün manifesti: dosya adı -> sha256, bayt, durum ('tamam' / 'yok_404'), zaman. Alt çizgiyle başlayan dosyalar (durum,
    günlük, manifestin kendisi) girmez. Klasör özeti = ada göre sıralı 'ad:sha256' satırlarının sha256'sı (K59 _k59_klasor_sha ile aynı)."""

    def __init__(self, klasor: str):
        self.klasor = klasor; self.yol = os.path.join(klasor, K60V_DOSYA["manifest"]); self._kilit = threading.Lock()
        self.d: Dict[str, Dict[str, Any]] = {}
        os.makedirs(klasor, exist_ok=True)
        if os.path.exists(self.yol):
            try:
                with open(self.yol, encoding="utf-8") as f:
                    self.d = dict(json.load(f).get("dosyalar") or {})
            except (OSError, ValueError) as ex:
                k60vlog.warning("manifest okunamadı (%s): diskteki dosyalardan yeniden kurulacak", ex)

    def var(self, ad: str, yok_isaret: bytes = b"") -> bool:
        """Dosya diskte ve geçerli mi? Diskte olup manifestte olmayan dosya (yarıda kesilen koşu) özeti alınarak manifeste eklenir."""
        y = os.path.join(self.klasor, ad)
        if not os.path.exists(y) or os.path.getsize(y) < 2:
            return False
        with self._kilit:
            if ad in self.d and self.d[ad].get("bayt") == os.path.getsize(y):
                return True
        with open(y, "rb") as f:
            ham = f.read()
        self._kayit(ad, ham, "yok_404" if yok_isaret and ham == yok_isaret else "tamam")
        return True

    def _kayit(self, ad: str, ham: bytes, durum: str) -> None:
        with self._kilit:
            self.d[ad] = {"sha256": k60v_sha(ham), "bayt": len(ham), "durum": durum, "utc": _k60v_simdi()}

    def dosya_yaz(self, ad: str, ham: bytes, durum: str) -> None:
        """Atomik yazım (önce .yarim) + manifest kaydı."""
        y = os.path.join(self.klasor, ad)
        with open(y + ".yarim", "wb") as f:
            f.write(ham)
        os.replace(y + ".yarim", y)
        self._kayit(ad, ham, durum)

    def ozet_sha(self) -> str:
        h = hashlib.sha256()
        with self._kilit:
            for ad in sorted(self.d):
                h.update(f"{ad}:{self.d[ad]['sha256']}\n".encode("utf-8"))
        return h.hexdigest()

    def kaydet(self) -> str:
        oz = self.ozet_sha()
        with self._kilit:
            govde = {"surum": K60V_SURUM, "guncelleme_utc": _k60v_simdi(), "dosya_sayisi": len(self.d), "klasor_ozet_sha256": oz,
                     "ozet_kurali": "ada göre sıralı 'ad:sha256' satırlarının sha256'sı", "dosyalar": {a: self.d[a] for a in sorted(self.d)}}
            with open(self.yol + ".yarim", "w", encoding="utf-8") as f:
                json.dump(govde, f, ensure_ascii=False, indent=0)
            os.replace(self.yol + ".yarim", self.yol)
        return oz


def k60v_manifest_dogrula(klasor: str) -> Dict[str, Any]:
    """Manifestteki her dosyanın sha256'sı diskten yeniden hesaplanır. Dönen: dosya sayısı, klasör özeti, farklı / eksik / fazla dosyalar."""
    M = K60VManifest(klasor); farkli, eksik = [], []
    for ad, k in sorted(M.d.items()):
        y = os.path.join(klasor, ad)
        if not os.path.exists(y):
            eksik.append(ad)
        elif k60v_dosya_sha(y) != k.get("sha256"):
            farkli.append(ad)
    fazla = sorted(f for f in os.listdir(klasor) if not f.startswith("_") and not f.endswith(".yarim") and f not in M.d)
    return {"klasor": klasor, "dosya": len(M.d), "tamam": sum(1 for k in M.d.values() if k.get("durum") == "tamam"),
            "yok_404": sum(1 for k in M.d.values() if k.get("durum") == "yok_404"), "bayt": int(sum(k.get("bayt", 0) for k in M.d.values())),
            "klasor_ozet_sha256": M.ozet_sha(), "farkli": farkli, "eksik": eksik, "fazla": fazla,
            "saglam": not (farkli or eksik or fazla)}


class K60VHizSiniri:
    """Bütün iş parçacıkları için ortak hız sınırı: art arda iki istek başlangıcı arasında en az 1 / hız + pay saniye. hiz, üst sınırı
    (saniyede 8) aşamaz. Bekleme kilit altında yapılır; böylece gerçek başlangıç anları arasındaki aralık korunur."""

    def __init__(self, hiz: float, zaman: Callable[[], float] = time.monotonic, uyu: Callable[[float], None] = time.sleep):
        ust = float(K60V_ESIK["sec"]["hiz_ust"])
        if not (hiz and hiz > 0):
            raise K60VHata(f"hız pozitif olmalı: {hiz}")
        if hiz > ust:
            k60vlog.warning("istenen hız %.1f / sn üst sınırı aşıyor; %.0f / sn'ye indirildi", hiz, ust)
        self.hiz = min(float(hiz), ust); self.aralik = 1.0 / self.hiz + float(K60V_ESIK["sec"]["hiz_pay_sn"])
        self._zaman, self._uyu, self._kilit, self._son = zaman, uyu, threading.Lock(), None

    def bekle(self) -> float:
        with self._kilit:
            if self._son is not None:
                while True:
                    kalan = self._son + self.aralik - self._zaman()
                    if kalan <= 0:
                        break
                    self._uyu(kalan)
            self._son = self._zaman()
            return self._son


# ---------------------------------------------------------------- 3) ORTAK İNDİRME MOTORU
_K60V_CTX: Dict[str, ssl.SSLContext] = {}


def _k60v_getir(url: str, basliklar: Dict[str, str], zaman_asimi: float) -> Tuple[int, bytes]:
    """Tek HTTPS isteği -> (durum kodu, gövde). HTTP hata kodu istisna değil kod olarak döner; ağ hatası istisna olarak yükselir."""
    if "ctx" not in _K60V_CTX:
        _K60V_CTX["ctx"] = ssl.create_default_context(cafile=K60V_YOL["ca"]) if os.path.exists(K60V_YOL["ca"]) else ssl.create_default_context()
    req = urllib.request.Request(url, headers=basliklar)
    try:
        with urllib.request.urlopen(req, context=_K60V_CTX["ctx"], timeout=zaman_asimi) as r:
            ham = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                ham = gzip.decompress(ham)
            return int(r.status), ham
    except urllib.error.HTTPError as e:
        return int(e.code), b""


def _k60v_json_mu(_is: Dict[str, Any], ham: bytes) -> bool:
    try:
        return isinstance(json.loads(ham), dict)
    except ValueError:
        return False


def _k60v_sec_gecerli(is_: Dict[str, Any], ham: bytes) -> bool:
    """Frames yanıtı 'data' listesi olan JSON; dizin yanıtı gzip (ya da düz metin) master dizini olmalı."""
    if is_.get("tur") == "dizin":
        try:
            bas = gzip.decompress(ham)[:4000] if ham[:2] == b"\x1f\x8b" else ham[:4000]
        except (OSError, EOFError):
            return False
        return b"CIK|Company Name|Form Type|Date Filed" in bas
    try:
        J = json.loads(ham)
    except ValueError:
        return False
    return isinstance(J, dict) and isinstance(J.get("data"), list)


def _k60v_tek(is_: Dict[str, Any], getir: Callable, basliklar: Dict[str, str], P: Dict[str, Any], hizci: Optional[K60VHizSiniri],
              dur: threading.Event, uyu: Callable[[float], None], gecerli: Callable) -> Tuple[str, Optional[bytes]]:
    """Tek iş: ('tamam', ham) / ('yok', None) (404) / ('ret', None) (durdurucu kod) / ('engel', None) / ('hata', None) / ('durdu', None)."""
    son = "hata"
    for deneme in range(int(P["deneme"])):
        if dur.is_set():
            return "durdu", None
        if hizci is not None:
            hizci.bekle()
        try:
            kod, ham = getir(is_["url"], basliklar, P["zaman_asimi"])
        except (urllib.error.URLError, TimeoutError, ValueError, OSError, EOFError) as e:
            son = "hata"; k60vlog.debug("%s: %s (deneme %d)", is_["ad"], str(e)[:120], deneme + 1); uyu(2.0 * (deneme + 1)); continue
        if kod == 200:
            if gecerli(is_, ham):
                return "tamam", ham
            son = "hata"; k60vlog.debug("%s: yanıt geçersiz (deneme %d)", is_["ad"], deneme + 1); uyu(2.0 * (deneme + 1)); continue
        if kod == 404:
            return "yok", None
        if kod in P["ret_kod"]:
            return "ret", None
        if kod in (401, 403, 429):
            son = "engel"; uyu(float(P["geri_cekil"]) * 2 ** deneme)
        else:
            son = "hata"; k60vlog.debug("%s: HTTP %s (deneme %d)", is_["ad"], kod, deneme + 1); uyu(2.0 * (deneme + 1))
    return son, None


def _k60v_gunluk_dosyasi(klasor: str) -> logging.Handler:
    h = logging.FileHandler(os.path.join(klasor, K60V_DOSYA["gunluk"]), encoding="utf-8")
    h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S"))
    h.addFilter(_K60VGizle())
    k60vlog.addHandler(h)
    return h


def _k60v_calistir(komut: str, isler: List[Dict[str, Any]], klasor: str, getir: Callable, basliklar: Dict[str, str], P: Dict[str, Any],
                   hizci: Optional[K60VHizSiniri], uyu: Callable[[float], None], gecerli: Callable, yok_isaret: bytes) -> Dict[str, Any]:
    """Kaldığı yerden süren indirme: diskte geçerli dosyası olan iş atlanır; her başarılı dosya atomik yazılır ve sha256'sı manifeste girer.
    Durdurucu kod (P['ret_kod']) ya da art arda P['engel_ardisik'] başarısızlık gelirse kalan işler bırakılır. Durum _durum.json'a yazılır
    (kimlik satırı / e-posta İÇERMEZ)."""
    os.makedirs(klasor, exist_ok=True)
    for f in os.listdir(klasor):
        if f.endswith(".yarim"):
            os.remove(os.path.join(klasor, f))
    gh = _k60v_gunluk_dosyasi(klasor); M = K60VManifest(klasor); dyol = os.path.join(klasor, K60V_DOSYA["durum"])
    try:
        with open(dyol, encoding="utf-8") as f:
            eski = json.load(f)
    except (OSError, ValueError):
        eski = {}
    eksik = [i for i in isler if not M.var(i["dosya"], yok_isaret)]
    durum: Dict[str, Any] = {"komut": komut, "surum": K60V_SURUM, "istenen": len(isler), "onbellek": len(isler) - len(eksik), "indirilen": 0,
                             "yok_404": 0, "engel": 0, "hata": 0, "ret": 0, "durdu": 0, "durum": "tamam", "inemeyen": [],
                             "ilk_indirme_utc": eski.get("ilk_indirme_utc") or (_k60v_simdi() if eksik else None)}
    dur = threading.Event(); kilit = threading.Lock(); ardisik = 0; t0 = time.time()
    k60vlog.info("%s: %d iş, %d önbellekte, %d indirilecek -> %s", komut, len(isler), durum["onbellek"], len(eksik), klasor)

    def say(i: Dict[str, Any], d: str) -> None:
        """Sonucu sayar; ret ya da art arda başarısızlıkta 'dur' işaretini HEMEN (işi yapan iş parçacığında) kaldırır."""
        nonlocal ardisik
        with kilit:
            durum[{"tamam": "indirilen", "yok": "yok_404"}.get(d, d)] += 1
            if d in ("engel", "hata", "ret"):
                durum["inemeyen"].append(i["ad"]); ardisik += 1
            elif d in ("tamam", "yok"):
                ardisik = 0
            if d == "ret" and not dur.is_set():
                dur.set(); durum["durum"] = "reddedildi (403 / 407): indirme durdu; aynı komut kaldığı yerden sürer"
                k60vlog.error("%s: %s (%s)", komut, durum["durum"], i["ad"])
            elif P.get("engel_ardisik") and ardisik >= int(P["engel_ardisik"]) and not dur.is_set():
                dur.set(); durum["durum"] = f"engellendi ({ardisik} ardışık iş inemedi): indirme durdu; aynı komut kaldığı yerden sürer"
                k60vlog.error("%s: %s", komut, durum["durum"])

    def calis(i: Dict[str, Any]) -> None:
        try:
            d, ham = _k60v_tek(i, getir, basliklar, P, hizci, dur, uyu, gecerli)
            if d == "tamam":
                M.dosya_yaz(i["dosya"], ham, "tamam")
            elif d == "yok":
                M.dosya_yaz(i["dosya"], yok_isaret, "yok_404")
        except Exception as e:   # tek iş beklenmedik hata verirse ötekiler sürer
            d = "hata"; k60vlog.warning("%s: iş hatası %s: %s", komut, i["ad"], str(e)[:160])
        say(i, d)
        if P.get("bekle") and d != "durdu":
            uyu(float(P["bekle"]))
    try:
        with ThreadPoolExecutor(max_workers=int(P["is_parcacigi"])) as ex:
            for k, fu in enumerate(as_completed([ex.submit(calis, i) for i in eksik]), 1):
                fu.result()
                if k % 200 == 0:
                    M.kaydet()
                    k60vlog.info("%s: %d / %d (%.0f sn) %s", komut, k, len(eksik), time.time() - t0,
                                 {a: durum[a] for a in ("indirilen", "yok_404", "engel", "hata")})
    finally:
        if durum["durum"] == "tamam" and (durum["engel"] or durum["hata"] or durum["durdu"]):
            durum["durum"] = "eksik (aynı komut kaldığı yerden sürer)"
        durum.update({"son_utc": _k60v_simdi(), "sure_sn": round(time.time() - t0, 1), "manifest_sha256": M.kaydet(), "manifest_dosya": len(M.d)})
        with open(dyol + ".yarim", "w", encoding="utf-8") as f:
            f.write(k60v_maskele(json.dumps(durum, ensure_ascii=False, indent=1)))
        os.replace(dyol + ".yarim", dyol)
        k60vlog.info("%s bitti: %s", komut, {a: v for a, v in durum.items() if a != "inemeyen"})
        k60vlog.removeHandler(gh); gh.close()
    return durum


# ---------------------------------------------------------------- 4) SEC FRAMES İNDİRME
def k60v_sec_ua() -> str:
    """SEC kimlik satırı YALNIZ K60_SEC_UA ortam değişkeninden okunur; yoksa K60VKimlikYok. Değer hiçbir yere yazılmaz."""
    ua = (os.environ.get(K60V_UA_DEGISKEN) or "").strip()
    if not ua:
        raise K60VKimlikYok(f"{K60V_UA_DEGISKEN} ortam değişkeni tanımlı değil: SEC indirmesi başlamaz. Kullanım: "
                            f"{K60V_UA_DEGISKEN}='<ad> <iletişim adresi>' python K60_veri.py indir_sec")
    if not _K60V_EPOSTA.search(ua):
        k60vlog.warning("%s içinde iletişim adresi görünmüyor; SEC adil erişim kuralı ad + iletişim adresi ister", K60V_UA_DEGISKEN)
    return ua


def k60v_sec_indir(hiz: Optional[float] = None, ek: bool = True, dizin: bool = False, adet: Optional[int] = None,
                   getir: Optional[Callable] = None, klasor: Optional[str] = None, eski_klasor: Optional[str] = None,
                   uyu: Callable[[float], None] = time.sleep, zaman: Callable[[], float] = time.monotonic) -> Dict[str, Any]:
    """SEC XBRL frames (+ isteğe bağlı EDGAR başvuru dizini) -> K60V_YOL['frames']. Saniyede en çok 8 istek (ortak sınır), 3 deneme, gzip.
    404 = o etiket / dönem yok ('{}' işareti, K57 ile aynı); 403 / 407 = ret, indirme durur. Eski önbellekte (K59 girdisi) olan çerçeve
    yeniden indirilmez ve o klasöre yazılmaz. getir / uyu / zaman yalnız testler içindir."""
    ua = k60v_sec_ua(); S = K60V_ESIK["sec"]; klasor = klasor or K60V_YOL["frames"]
    if os.path.abspath(klasor) == os.path.abspath(K60V_YOL["eski_frames"] if eski_klasor is None else eski_klasor):
        raise K60VHata(f"K60 frames önbelleği K59 girdisi olan {klasor} klasörüne yazılamaz")
    hizci = K60VHizSiniri(S["hiz_ust"] if hiz is None else float(hiz), zaman, uyu)
    isler = [r for r in k60v_sec_listesi(ek, eski_klasor) if not r["mevcut"]] + (k60v_dizin_listesi() if dizin else [])
    if adet is not None:
        isler = isler[:int(adet)]
    k60vlog.info("SEC: kimlik satırı %s ortam değişkeninden alındı (günlüğe yazılmaz); hız <= %.0f istek / sn", K60V_UA_DEGISKEN, hizci.hiz)
    P = {"deneme": S["deneme"], "zaman_asimi": S["zaman_asimi"], "geri_cekil": S["geri_cekil"], "ret_kod": S["ret_kod"],
         "is_parcacigi": S["is_parcacigi"], "engel_ardisik": 40}
    return _k60v_calistir("indir_sec", isler, klasor, getir or _k60v_getir, {"User-Agent": ua, "Accept-Encoding": "gzip, deflate"}, P, hizci,
                          uyu, _k60v_sec_gecerli, b"{}")


# ---------------------------------------------------------------- 5) YAHOO GÜNLÜK FİYAT İNDİRME
def k60v_evren() -> pd.DataFrame:
    """Geniş ABD evreni sembolleri: K57-B evren tablosu (repo: evren_b1.csv; frames'te geliri + kârı + özkaynağı olan, borsa kodlu CIK'ler)
    + V_ABD sembolleri (varsa). Yalnız bugün kodu olanlar (yaşayanlar)."""
    kay: Dict[str, List[str]] = {}
    if os.path.exists(K60V_YOL["evren_b1"]):
        for s in pd.read_csv(K60V_YOL["evren_b1"], dtype=str).sembol.dropna():
            kay.setdefault(str(s).strip().upper(), []).append("b1")
    else:
        k60vlog.warning("K57-B evren tablosu yok: %s", K60V_YOL["evren_b1"])
    y = os.path.join(K60V_YOL["veri"], "V_ABD.pkl")
    if os.path.exists(y):
        try:
            with open(y, "rb") as f:
                for s in pickle.load(f):
                    kay.setdefault(str(s).strip().upper(), []).append("vabd")
        except Exception as ex:   # bozuk / uyumsuz pickle evreni durdurmasın
            k60vlog.warning("V_ABD okunamadı (%s): evren yalnız K57-B tablosundan", ex)
    else:
        k60vlog.warning("V_ABD.pkl yok (%s): evren yalnız K57-B tablosundan", y)
    if not kay:
        raise K60VHata("evren boş: ne K57-B evren tablosu ne V_ABD var")
    return pd.DataFrame([{"sembol": s, "kaynak": "+".join(dict.fromkeys(k))} for s, k in sorted(kay.items())])


def _k60v_yahoo_url(T: str) -> str:
    Y = K60V_ESIK["yahoo"]
    p1 = int(pd.Timestamp(Y["bas"], tz="UTC").timestamp()); p2 = int(pd.Timestamp(Y["bit"], tz="UTC").timestamp())
    return Y["url"].format(T=urllib.parse.quote(T, safe="")) + f"?period1={p1}&period2={p2}&interval=1d&events=div%2Csplits&includeAdjustedClose=true"


def _k60v_fiyat_adi(T: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", T) + ".json"


def k60v_fiyat_indir(semboller: Optional[List[str]] = None, adet: Optional[int] = None, getir: Optional[Callable] = None,
                     klasor: Optional[str] = None, uyu: Callable[[float], None] = time.sleep) -> Dict[str, Any]:
    """Yahoo chart API günlük fiyatları (K57-B ile aynı uç, tarayıcı kimliği, iş parçacığı ve bekleme düzeni), 2010-01-01'den.
    Hisse başına ham JSON (temettü / bölünme olayları dahil) -> K60V_YOL['fiyat']; 404 -> {"yok": 404} işareti; kaldığı yerden sürer."""
    Y = K60V_ESIK["yahoo"]; klasor = klasor or K60V_YOL["fiyat"]
    if os.path.abspath(klasor) == os.path.abspath(K60V_YOL["eski_fiyat"]):
        raise K60VHata(f"K60 fiyat önbelleği K59 girdisi olan {klasor} klasörüne yazılamaz")
    if semboller is None:
        U = k60v_evren()
    else:
        U = pd.DataFrame({"sembol": list(dict.fromkeys(str(s).strip().upper() for s in semboller)), "kaynak": "elle"})
    os.makedirs(klasor, exist_ok=True)
    U.to_csv(os.path.join(klasor, K60V_DOSYA["evren"]), index=False)
    isler = [{"ad": s, "url": _k60v_yahoo_url(s), "dosya": _k60v_fiyat_adi(s), "tur": "fiyat"} for s in U.sembol]
    if adet is not None:
        isler = isler[:int(adet)]
    P = {"deneme": Y["deneme"], "zaman_asimi": Y["zaman_asimi"], "geri_cekil": Y["geri_cekil"], "ret_kod": Y["ret_kod"],
         "is_parcacigi": Y["is_parcacigi"], "engel_ardisik": Y["engel_ardisik"], "bekle": Y["bekle"]}
    return _k60v_calistir("indir_fiyat", isler, klasor, getir or _k60v_getir, {"User-Agent": K57.K57B_YAHOO_UA, "Accept": "application/json"},
                          P, None, uyu, _k60v_json_mu, b'{"yok": 404}')


def _k60v_bar_say(ham: bytes) -> int:
    """Ham Yahoo yanıtındaki gün (zaman damgası) sayısı; okunamıyorsa -1."""
    try:
        res = ((json.loads(ham).get("chart") or {}).get("result") or [None])[0]
        return len((res or {}).get("timestamp") or [])
    except (ValueError, AttributeError, TypeError):
        return -1


def k60v_fiyat_yenile(semboller: Optional[List[str]] = None, getir: Optional[Callable] = None, klasor: Optional[str] = None,
                      uyu: Callable[[float], None] = time.sleep) -> Dict[str, Any]:
    """Kırpık / boş gelen hisseleri yeniden ister (Yahoo geçmişi bazen geçici olarak eksik verir). Yeni yanıt eskisinden DAHA ÇOK gün
    içeriyorsa dosya ve manifest kaydı değişir; değilse eski dosya aynen kalır (veri kaybı olmaz). semboller verilmezse kapsam taramasından
    'kırpık' ve 'veri yok' olanlar alınır."""
    Y = K60V_ESIK["yahoo"]; klasor = klasor or K60V_YOL["fiyat"]
    if os.path.abspath(klasor) == os.path.abspath(K60V_YOL["eski_fiyat"]):
        raise K60VHata(f"K60 fiyat önbelleği K59 girdisi olan {klasor} klasörüne yazılamaz")
    if semboller is None:
        Kp = k60v_fiyat_tara(klasor, uygunluk=False)["kapsam"]
        semboller = Kp[Kp.kirpik | Kp.durum.str.startswith("veri yok")].sembol.tolist()
    M = K60VManifest(klasor); dur = threading.Event(); out: Dict[str, Any] = {"denenen": 0, "iyilesen": [], "ayni": [], "inemeyen": []}
    P = {"deneme": Y["deneme"], "zaman_asimi": Y["zaman_asimi"], "geri_cekil": Y["geri_cekil"], "ret_kod": Y["ret_kod"]}
    for s in semboller:
        ad = _k60v_fiyat_adi(s); y = os.path.join(klasor, ad); out["denenen"] += 1
        eski_n = -1
        if os.path.exists(y):
            with open(y, "rb") as f:
                eski_n = _k60v_bar_say(f.read())
        d, ham = _k60v_tek({"ad": s, "url": _k60v_yahoo_url(s), "dosya": ad}, getir or _k60v_getir,
                           {"User-Agent": K57.K57B_YAHOO_UA, "Accept": "application/json"}, P, None, dur, uyu, _k60v_json_mu)
        if d != "tamam":
            out["inemeyen"].append(s)
        elif _k60v_bar_say(ham) > eski_n:
            M.dosya_yaz(ad, ham, "tamam"); out["iyilesen"].append(s)
        else:
            out["ayni"].append(s)
        uyu(float(Y["bekle"]))
    out["manifest_sha256"] = M.kaydet()
    k60vlog.info("fiyat yenileme: %d denendi, %d iyileşti, %d aynı, %d inemedi", out["denenen"], len(out["iyilesen"]), len(out["ayni"]), len(out["inemeyen"]))
    return out


# ---------------------------------------------------------------- 6) OKUYUCULAR
def k60v_yahoo_oku(yol: str, kes: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], str]:
    """Önbellek JSON -> {'gun', 'kapanis' (bölünme düzeltmeli, temettüsüz), 'duzeltilmis' (temettü de düzeltilmiş), 'hacim', 'bolunme'
    ((tarih, oran) ya da None), 'temettu' (olay sayısı), 'tur', 'ilk_islem'}; (None, neden). Günler borsa saat dilimine göre; kes sonrası atılır.
    Temizlik K57 k57b_yahoo_oku ile aynı (OHLC dolu, High >= Low, Close > 0); tür ve en az gün süzgeci BURADA uygulanmaz.
    'kirpik' = Yahoo'nun verdiği ilk gün, hissenin ilk işlem gününden (ya da istek başlangıcından) kirpik_gun günden fazla sonra: geçmiş eksik."""
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
    meta = res.get("meta") or {}; tz = meta.get("exchangeTimezoneName") or "America/New_York"

    def gun(ts: Any) -> pd.DatetimeIndex:
        return pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    ilk = meta.get("firstTradeDate"); ilk_islem = gun([int(ilk)])[0] if isinstance(ilk, (int, float)) else pd.NaT
    beklenen = max(ilk_islem, pd.Timestamp(K60V_ESIK["yahoo"]["bas"])) if pd.notna(ilk_islem) else pd.Timestamp(K60V_ESIK["yahoo"]["bas"])
    kirpik = bool((gun([res["timestamp"][0]])[0] - beklenen).days > int(K60V_ESIK["yahoo"]["kirpik_gun"]))
    q = ((res.get("indicators") or {}).get("quote") or [{}])[0]
    try:
        d = pd.DataFrame({"o": q.get("open"), "h": q.get("high"), "l": q.get("low"), "c": q.get("close"), "v": q.get("volume")},
                         index=gun(res["timestamp"]), dtype=float)
    except (ValueError, TypeError):
        return None, "okunamadı (seri boyu)"
    adj = (((res.get("indicators") or {}).get("adjclose") or [{}])[0] or {}).get("adjclose")
    d["a"] = np.asarray(pd.Series(adj, dtype=float), float) if adj is not None and len(adj) == len(d) else d.c.to_numpy(float)
    d = d[~d.index.duplicated(keep="last")].dropna(subset=["o", "h", "l", "c"]).sort_index()
    d = d[(d.h >= d.l) & (d.c > 0)]
    if kes is not None:
        d = d[d.index <= pd.Timestamp(kes)]
    if not len(d):
        return None, "veri yok (kırpık)" if kirpik else "veri yok"
    olay = res.get("events") or {}; bol = []
    for v in (olay.get("splits") or {}).values():
        try:
            pay, payda, t = float(v["numerator"]), float(v["denominator"]), int(v["date"])
        except (KeyError, TypeError, ValueError):
            continue
        if pay > 0 and payda > 0 and pay != payda:
            bol.append((gun([t])[0].to_datetime64().astype("datetime64[ns]"), pay / payda))
    bol.sort(key=lambda x: x[0])
    return {"gun": d.index, "kapanis": d.c.to_numpy(float), "duzeltilmis": d.a.to_numpy(float), "hacim": d.v.fillna(0.0).to_numpy(float),
            "bolunme": (np.array([x[0] for x in bol], "datetime64[ns]"), np.array([x[1] for x in bol], float)) if bol else None,
            "temettu": len(olay.get("dividends") or {}), "tur": meta.get("instrumentType"), "ilk_islem": ilk_islem, "kirpik": kirpik}, "fiyat"


def k60v_bolunme_carpan(bol: Optional[Tuple[np.ndarray, np.ndarray]], t: np.ndarray) -> np.ndarray:
    """Her t için, tarihi t'den SONRA olan bölünme oranlarının çarpımı (K59 k59_bolunme_carpan ile aynı kural).
    Yahoo kapanışı (bölünme düzeltmeli) x çarpan = o gün ekranda görülen fiyat."""
    t = np.asarray(t, "datetime64[ns]"); out = np.ones(t.shape)
    if bol is None or not len(bol[0]):
        return out
    d, r = bol
    sonek = np.r_[np.cumprod(r[::-1])[::-1], 1.0]
    out[:] = sonek[np.searchsorted(d, t, side="right")]
    return out


def k60v_gunluk_bayrak(o: Dict[str, Any], U: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Hissenin her işlem günü için uygunluk bitleri (yalnız o gün ve öncesi bilgi): 1 = en az gecmis_gun gün geçmiş, 2 = o günkü fiyat >=
    fiyat_min, 4 = likit_gun günlük medyan işlem değeri (kapanış x hacim) >= likit_min. K59 k59_panel uygunluğuyla aynı eşikler."""
    U = U or K60V_ESIK["uygunluk"]; c = o["kapanis"]
    fiyat = c * k60v_bolunme_carpan(o["bolunme"], o["gun"].to_numpy("datetime64[ns]"))
    tl = pd.Series(c * o["hacim"]).rolling(int(U["likit_gun"]), min_periods=int(U["likit_min_gun"])).median().to_numpy(float)
    gec = np.arange(1, len(c) + 1) >= int(U["gecmis_gun"])
    return (gec.astype(np.uint8) + 2 * (fiyat >= float(U["fiyat_min"])).astype(np.uint8)
            + 4 * (np.nan_to_num(tl, nan=-1.0) >= float(U["likit_min"])).astype(np.uint8)).astype(np.uint8)


# ---------------------------------------------------------------- 7) FİYAT TARAMASI: KAPSAM + UYGUN EVREN (getiri HESAPLANMAZ)
def k60v_fiyat_tara(klasor: Optional[str] = None, uygunluk: bool = True) -> Dict[str, Any]:
    """Fiyat önbelleğini tarar. 'kapsam': hisse başına durum, tür, ilk / son gün, gün sayısı, bölünme ve temettü olay sayısı.
    uygunluk=True ise ayrıca 'ay' (her ay sonu: işlem gören, geçmişi yeten, fiyatı yeten, likit, uygun hisse sayısı) ve 'yil' (yıl özeti).
    Uygun = tür EQUITY + 252 gün geçmiş + o günkü fiyat >= 2 $ + 20 gün medyan işlem değeri >= 1 milyon $. Getiri hesaplanmaz."""
    klasor = klasor or K60V_YOL["fiyat"]; Y = K60V_ESIK["yahoo"]; Uy = K60V_ESIK["uygunluk"]
    if not os.path.isdir(klasor):
        raise K60VHata(f"fiyat önbelleği yok: {klasor} (önce `python K60_veri.py indir_fiyat`)")
    ey = os.path.join(klasor, K60V_DOSYA["evren"])
    if os.path.exists(ey):
        E = pd.read_csv(ey, dtype=str)
    else:
        E = pd.DataFrame({"sembol": sorted(f[:-5] for f in os.listdir(klasor) if f.endswith(".json") and not f.startswith("_")), "kaynak": "?"})
    sat: List[Dict[str, Any]] = []; saklanan: List[Tuple[np.ndarray, np.ndarray]] = []; gun_say: Dict[int, int] = {}
    yil_seri: Dict[int, int] = {}; yil_gun: Dict[int, int] = {}; yil_tam: Dict[int, int] = {}
    for r in E.itertuples():
        y = os.path.join(klasor, _k60v_fiyat_adi(r.sembol))
        if not os.path.exists(y):
            sat.append({"sembol": r.sembol, "kaynak": r.kaynak, "durum": "inmedi"}); continue
        o, dr = k60v_yahoo_oku(y, Y["kes"])
        if o is None:
            sat.append({"sembol": r.sembol, "kaynak": r.kaynak, "durum": dr}); continue
        g = o["gun"]
        sat.append({"sembol": r.sembol, "kaynak": r.kaynak, "durum": "fiyat", "tur": o["tur"], "ilk": g[0].date(), "son": g[-1].date(),
                    "gun": len(g), "bolunme": 0 if o["bolunme"] is None else len(o["bolunme"][0]), "temettu": o["temettu"],
                    "ilk_islem": o["ilk_islem"].date() if pd.notna(o["ilk_islem"]) else None, "kirpik": o["kirpik"]})
        yy, ns = np.unique(g.year.to_numpy(), return_counts=True)
        for a, n in zip(yy.tolist(), ns.tolist()):
            yil_seri[a] = yil_seri.get(a, 0) + 1; yil_gun[a] = yil_gun.get(a, 0) + n; yil_tam[a] = yil_tam.get(a, 0) + (n >= 200)
        if uygunluk and o["tur"] in Uy["tur"]:
            gd = g.to_numpy("datetime64[D]").astype(np.int32)
            for x in gd.tolist():
                gun_say[x] = gun_say.get(x, 0) + 1
            saklanan.append((gd, k60v_gunluk_bayrak(o, Uy)))
    K = pd.DataFrame(sat, columns=["sembol", "kaynak", "durum", "tur", "ilk", "son", "gun", "bolunme", "temettu", "ilk_islem", "kirpik"])
    K["kirpik"] = K.kirpik.fillna(False).astype(bool) | K.durum.eq("veri yok (kırpık)")
    out: Dict[str, Any] = {"kapsam": K, "klasor": klasor, "ay": None, "yil": None}
    Yl = pd.DataFrame({"yil": sorted(yil_seri)})
    Yl["seri"] = [yil_seri[a] for a in Yl.yil]; Yl["tam_yil_seri"] = [yil_tam[a] for a in Yl.yil]; Yl["hisse_gun"] = [yil_gun[a] for a in Yl.yil]
    if uygunluk and saklanan:
        tum = np.array(sorted(gun_say), np.int32); say = np.array([gun_say[x] for x in tum.tolist()])
        tak = tum[say >= max(1.0, float(Uy["takvim_pay"]) * float(np.median(say)))]       # borsa takvimi: yeterince hissenin işlem gördüğü günler
        tg = tak.astype("datetime64[D]"); ayk = tg.astype("datetime64[M]")
        son = np.r_[ayk[1:] != ayk[:-1], True]; me = tak[son]; me_p = np.flatnonzero(son)
        n = len(me); A = {k: np.zeros(n, int) for k in ("islem", "gecmis", "fiyat", "likit", "uygun")}
        for gd, b in saklanan:
            p = np.searchsorted(gd, me, side="right") - 1; var = p >= 0; pc = np.clip(p, 0, None)
            taze = var & (me_p - (np.searchsorted(tak, gd[pc], side="right") - 1) <= int(Uy["ileri_tasima"]))
            bb = b[pc]
            A["islem"] += taze; A["gecmis"] += taze & ((bb & 1) > 0); A["fiyat"] += taze & ((bb & 2) > 0); A["likit"] += taze & ((bb & 4) > 0)
            A["uygun"] += taze & (bb == 7)
        Ay = pd.DataFrame({"ay_sonu": pd.to_datetime(me.astype("datetime64[D]")), **A})
        Ay["yil"] = Ay.ay_sonu.dt.year
        G = Ay.groupby("yil").agg(ay=("uygun", "size"), uygun_ort=("uygun", "mean"), uygun_min=("uygun", "min"), uygun_maks=("uygun", "max"),
                                  uygun_yil_sonu=("uygun", "last"), islem_yil_sonu=("islem", "last"), gecmis_yil_sonu=("gecmis", "last"),
                                  fiyat_yil_sonu=("fiyat", "last"), likit_yil_sonu=("likit", "last")).reset_index()
        Yl = Yl.merge(G, on="yil", how="left"); out["ay"] = Ay.drop(columns="yil")
    out["yil"] = Yl
    return out


# ---------------------------------------------------------------- 8) SEC DENETİMİ: ETİKET x DÖNEM ŞİRKET SAYILARI, 'filed' ALANI
def k60v_frame_say(yol: str) -> Dict[str, Any]:
    """Bir frames dosyası: durum ('tamam' / 'yok_404' / 'bozuk'), satır, ayrı şirket (CIK) sayısı, veri alanları, 'filed' alanı var mı."""
    try:
        with open(yol, encoding="utf-8") as f:
            J = json.load(f)
    except (OSError, ValueError):
        return {"durum": "bozuk", "satir": 0, "sirket": 0, "alanlar": "", "filed_var": False}
    veri = J.get("data") if isinstance(J, dict) else None
    if not veri:
        return {"durum": "yok_404" if J == {} else "bos", "satir": 0, "sirket": 0, "alanlar": "", "filed_var": False}
    alan = set()
    for d in veri[:200]:
        alan |= set(d) if isinstance(d, dict) else set()
    return {"durum": "tamam", "satir": len(veri), "sirket": len({d.get("cik") for d in veri if isinstance(d, dict)}),
            "alanlar": "|".join(sorted(alan)), "filed_var": "filed" in alan}


def k60v_dizin_say(yol: str) -> Dict[str, Any]:
    """EDGAR master dizini: toplam başvuru ve 10-K / 10-Q ailesi başvuru sayısı, ayrı CIK sayısı."""
    try:
        with open(yol, "rb") as f:
            ham = f.read()
        metin = (gzip.decompress(ham) if ham[:2] == b"\x1f\x8b" else ham).decode("latin-1")
    except (OSError, EOFError):
        return {"durum": "bozuk", "satir": 0, "sirket": 0, "alanlar": "", "filed_var": False}
    form = set(K60V_ESIK["dizin"]["form"]); n = 0; cik = set(); top = 0
    for s in metin.splitlines():
        p = s.split("|")
        if len(p) == 5 and p[0].isdigit():
            top += 1
            if p[2] in form:
                n += 1; cik.add(p[0])
    return {"durum": "tamam" if top else "bos", "satir": n, "sirket": len(cik), "alanlar": f"CIK|Company Name|Form Type|Date Filed|Filename ({top} başvuru)",
            "filed_var": bool(top)}


def k60v_sec_denetle(klasor: Optional[str] = None, eski_klasor: Optional[str] = None, ek: bool = True) -> Dict[str, Any]:
    """Her (etiket, dönem) için şirket sayısı: kaynak 'k60' (yeni önbellek) ya da 'eski' (K59 girdisi, yalnız okunur) ya da 'inmedi'.
    Ayrıca yeni önbelleğin manifest doğrulaması. Dönen: {'sayim': DataFrame, 'manifest': {...} | None}."""
    klasor = klasor or K60V_YOL["frames"]; sat = []
    for r in k60v_sec_listesi(ek, eski_klasor) + k60v_dizin_listesi():
        y = os.path.join(klasor, r["dosya"])
        if os.path.exists(y) and os.path.getsize(y) >= 2:
            kaynak, yol = "k60", y
        elif r["mevcut"]:
            kaynak, yol = "eski", r["mevcut"]
        else:
            if r["tur"] != "dizin":
                sat.append({"grup": r["grup"], "tax": r["tax"], "etiket": r["etiket"], "donem": r["donem"], "kaynak": "inmedi", "durum": "inmedi"})
            continue
        s = k60v_dizin_say(yol) if r["tur"] == "dizin" else k60v_frame_say(yol)
        sat.append({"grup": r["grup"], "tax": r["tax"], "etiket": r["etiket"], "donem": r["donem"], "kaynak": kaynak, "bayt": os.path.getsize(yol), **s})
    Sy = pd.DataFrame(sat, columns=["grup", "tax", "etiket", "donem", "kaynak", "durum", "satir", "sirket", "bayt", "alanlar", "filed_var"])
    man = k60v_manifest_dogrula(klasor) if os.path.isdir(klasor) and os.path.exists(os.path.join(klasor, K60V_DOSYA["manifest"])) else None
    return {"sayim": Sy, "manifest": man, "klasor": klasor}


def k60v_filed_bulgusu(Sy: pd.DataFrame) -> Dict[str, Any]:
    """Frames dosyalarında 'filed' (başvuru günü) alanı var mı? Eski çeyrekler (<= 2019) ve yeni çeyrekler ayrı sayılır."""
    F = Sy[(Sy.durum == "tamam") & (Sy.grup != "DIZIN")].copy()
    F["yil"] = F.donem.str.slice(2, 6).astype(int) if len(F) else []
    eski, yeni = F[F.yil <= 2019], F[F.yil >= 2020]
    alan = sorted({a for x in F.alanlar.dropna().unique() for a in str(x).split("|") if a})
    return {"eski_dosya": len(eski), "eski_filed": int(eski.filed_var.sum()) if len(eski) else 0, "yeni_dosya": len(yeni),
            "yeni_filed": int(yeni.filed_var.sum()) if len(yeni) else 0, "alanlar": alan,
            "dizin_dosya": int(((Sy.grup == "DIZIN") & (Sy.durum == "tamam")).sum())}


# ---------------------------------------------------------------- 9) PLAN
def _k60v_boyut_olc(eski: Optional[str]) -> Tuple[Dict[str, float], str]:
    """Çerçeve başına ortalama boyut (MB): eski önbellek varsa ondan ölçülür, yoksa K60V_ESIK['boyut_mb']."""
    B = dict(K60V_ESIK["boyut_mb"]); top: Dict[str, List[int]] = {"an": [], "ceyrek": [], "yil": []}
    if eski and os.path.isdir(eski):
        for f in os.listdir(eski):
            m = re.fullmatch(r"[\w-]+_(CY\d{4}(?:Q\d)?I?)\.json", f)
            if m and os.path.getsize(os.path.join(eski, f)) > 2000:     # '404 yok' işaretleri ve boş çerçeveler ortalamaya girmez
                top[_k60v_donem_turu(m.group(1))].append(os.path.getsize(os.path.join(eski, f)))
    olc = {k: float(np.mean(v)) / 1e6 for k, v in top.items() if len(v) >= 5}
    B.update(olc)
    return B, (f"eski önbellekten ölçüldü ({sum(len(v) for v in top.values())} dosya)" if olc else "kaba varsayım (eski önbellek yok)")


def k60v_plan_tablo(ek: bool = True, dizin: bool = False, eski_klasor: Optional[str] = None, klasor: Optional[str] = None) -> Dict[str, Any]:
    """Plan sayıları: etiket başına dönem aralığı ve istek sayısı; toplam istek, tahmini boyut ve süre. Ağ kullanılmaz."""
    eski = K60V_YOL["eski_frames"] if eski_klasor is None else eski_klasor; klasor = klasor or K60V_YOL["frames"]
    L = pd.DataFrame(k60v_sec_listesi(ek, eski))
    L["dtur"] = L.donem.map(_k60v_donem_turu); L["mevcut_mu"] = L.mevcut.notna()
    L["inmis"] = [os.path.exists(os.path.join(klasor, d)) and os.path.getsize(os.path.join(klasor, d)) >= 2 for d in L.dosya]
    B, bnot = _k60v_boyut_olc(eski)
    L["mb"] = L.dtur.map(B)
    ist = L[~L.mevcut_mu]
    D = pd.DataFrame(k60v_dizin_listesi()) if dizin else pd.DataFrame(columns=L.columns)
    n = len(ist) + len(D); hiz = float(K60V_ESIK["sec"]["hiz_ust"]); aralik = 1.0 / hiz + float(K60V_ESIK["sec"]["hiz_pay_sn"])
    mb = float(ist.mb.sum()) + len(D) * B["dizin"]
    sat = []
    for (grup, tax, etiket), g in L.groupby(["grup", "tax", "etiket"], sort=False):
        c = g[g.dtur != "yil"]; yl = g[g.dtur == "yil"]
        sat.append({"grup": grup, "tax": tax, "etiket": etiket, "birim": g.birim.iloc[0], "tur": g.tur.iloc[0],
                    "ceyrek": f"{c.donem.iloc[0]} .. {c.donem.iloc[-1]} ({len(c)})" if len(c) else "—",
                    "yil": f"{yl.donem.iloc[0]} .. {yl.donem.iloc[-1]} ({len(yl)})" if len(yl) else "—",
                    "toplam": len(g), "eski_onbellekte": int(g.mevcut_mu.sum()), "istek": int((~g.mevcut_mu).sum()),
                    "inmis": int((g.inmis & ~g.mevcut_mu).sum()), "icin": g.icin.iloc[0], "not": g["not"].iloc[0]})
    return {"liste": L, "dizin": D, "etiket": pd.DataFrame(sat), "istek": n, "frames_istek": len(ist), "dizin_istek": len(D),
            "eski_onbellekte": int(L.mevcut_mu.sum()), "toplam_cerceve": len(L), "kalan": int((~ist.inmis).sum()) + len(D),
            "mb": mb, "boyut_notu": bnot, "boyut": B, "sure_alt_dk": n * aralik / 60.0, "sure_ust_dk": 3.0 * n * aralik / 60.0,
            "grup_istek": ist.groupby("grup").size().to_dict(), "eski": eski, "klasor": klasor, "ek": ek}


def k60v_plan_metin(P: Dict[str, Any]) -> str:
    S = K60V_ESIK["sec"]; Y = K60V_ESIK["yahoo"]; T = P["etiket"]; g = P["grup_istek"]
    satir = "\n".join(f"| {r.grup} | {r.tax} | {r.etiket} | {r.birim} | {r.ceyrek} | {r.yil} | {r.eski_onbellekte} | {r.istek} | {r.icin} | {r['not']} |"
                      for _, r in T.iterrows())
    try:
        nsem = len(k60v_evren())
    except K60VHata:
        nsem = 0
    return f"""# K60 veri planı (yalnız veri hazırlığı; sinyal ölçümü yok)

Yazım zamanı: {_k60v_simdi()}. {K60V_SURUM}. Üreten: `python K60_veri.py plan`. Ağ kullanılmadı.

## 1. Neden
K59 temel veriye dayalı sinyalleri 66 ayda ölçebildi (frames önbelleği 2020Q1–2026Q2, geniş evren fiyatı 2020'den). 68 ayda rastgele sinyal
t ≈ 3'e ulaşabiliyor. K60 üç dönemli (KEŞİF 2016–2021, DOĞRULAMA 2022–2023, KASA 2024 – Ağu 2026); KEŞİF için temel veri en geç 2014'ten,
yıllık büyüme ve 8 çeyreklik sürpriz ölçüleri için daha da geriden gerekir. Plan: temel veri 2009Q1'den, fiyat 2010-01-01'den.

## 2. SEC XBRL frames: istek listesi
Uç: `{S['url']}`. Dönem adı: `CYyyyyQn` = çeyreklik süre (yaklaşık 91 gün), `CYyyyyQnI` = çeyrek sonu anlık değer, `CYyyyy` = yıllık süre.
Tam liste (her satır bir istek, adresi ve hedef dosyasıyla): `{K60V_DOSYA['liste']}`.

| grup | taksonomi | etiket | birim | çeyrek dönemleri (adet) | yıllık dönemler (adet) | eski önbellekte | istek | hangi sinyal için | not |
|---|---|---|---|---|---|---|---|---|---|
{satir}

- **A** = K57 / K59'un kullandığı etiketler. 2020Q1–2026Q2 çeyrekleri ve 2020–2025 yılları eski önbellekte (`{P['eski']}`, K59 girdisi) durur:
  yeniden indirilmez, o klasöre yazılmaz (K59 veri sha256'ları değişmez). İnen bölüm: 2009Q1–2019Q4 (44 çeyrek) ve süreli etiketlerde
  2009–2019 yılları (11). `dei/EntityCommonStockSharesOutstanding` eski önbellekte hiç yok: tam aralık (70 çeyrek sonu) iner.
  Eski önbellek o gün yerinde değilse aynı çerçeveler de yeni klasöre iner (komut kendisi bakar).
- **B** = ilk 30 sinyalin istediği yeni bilanço ve gelir tablosu etiketleri, 2009Q1–2026Q2.
- **C** = nakit akış kalemleri, YALNIZ yıllık çerçeve (2009–2025).
- **EK** = iş tanımındaki listede OLMAYAN, alt ajanın eklediği dört etiket (`--ek hayir` ile çıkarılır): temettü ödemesi (NET_PAYOUT_YLD envanterde
  temettüyü de ister) ve iki yedek pay sayısı (kapak sayfası pay sayısı çok sınıflı şirketlerde boyutlu bildirilir, frames'e girmez).

Sayım: K60'ın istediği toplam çerçeve {_bn(P['toplam_cerceve'])}; eski önbellekte {_bn(P['eski_onbellekte'])}; **indirilecek {_bn(P['frames_istek'])} istek**
(A {_bn(g.get('A', 0))}, B {_bn(g.get('B', 0))}, C {_bn(g.get('C', 0))}, EK {_bn(g.get('EK', 0))}){' + EDGAR dizini ' + _bn(P['dizin_istek']) + ' istek' if P['dizin_istek'] else ''}.
Bu klasörde şu an inmiş olan: {_bn(P['istek'] - P['kalan'])}; kalan: {_bn(P['kalan'])}.

### Hangi kalem hangi sıklıkta güvenilir
- **Anlık (bilanço) kalemleri** — özkaynak, yükümlülük, varlık, dönen varlık, kısa vadeli yükümlülük, nakit, uzun vadeli borç, pay sayısı:
  her çeyrek sonu güvenilir.
- **Gelir tablosu kalemleri** — gelir, net kâr, brüt kâr, satışların maliyeti, faaliyet kârı, Ar-Ge, vergi: 1.–3. çeyrek çeyreklik çerçevede
  gelir. **4. çeyrek çoğu şirkette ayrı bildirilmez**; yıllık çerçeveden türetilir (yıl − ilk üç çeyrek; K57 `k57_abd_temel_tablo` kuralı).
  Bu yüzden süreli her etiket için yıllık çerçeve de iner.
- **YALNIZ YILLIK güvenilir** — faaliyet nakit akışı, yatırım harcaması, hisse geri alımı, hisse ihraç geliri, temettü ödemesi (grup C ve EK),
  ayrıca amortisman (`DepreciationDepletionAndAmortization`; çeyreklik çerçevesi de iner ama eksiktir). Neden: şirketler nakit akış tablosunu
  yılbaşından bugüne (3, 6, 9 ay) bildirir; frames yalnız ~91 günlük dönemi "çeyrek" sayar, 6 ve 9 aylık değerler hiçbir çerçeveye girmez.
  Çeyreklik nakit akışı gerekiyorsa (ör. RUNWAY'in çeyreklik sürümü) kaynak SEC finansal tablo veri setleridir (envanter bölüm C satır 2);
  bu planda yok. Yıllık değer, mali yıl bittikten sonraki 10-K ile bilinir.
- Pay sayısı: `dei` kapak sayısının tarihi çeyrek sonu değil kapak günüdür (çeyrek sonundan haftalar sonra); frames en yakın çeyreğe yazar.

### İstek sayısı, boyut, süre
| kalem | değer |
|---|---|
| istek sayısı | {_bn(P['istek'])} (frames {_bn(P['frames_istek'])}{', dizin ' + _bn(P['dizin_istek']) if P['dizin_istek'] else ''}) |
| hız sınırı | saniyede en çok {_on(S['hiz_ust'], 0)} istek (SEC sınırı 10); bütün iş parçacıkları tek sayaçtan geçer, istekler arası en az {_on(1000 * (1 / S['hiz_ust'] + S['hiz_pay_sn']), 0)} ms |
| tahmini boyut | ~{_on(P['mb'] / 1000, 2)} GB ({P['boyut_notu']}; anlık {_on(P['boyut']['an'], 2)} MB, çeyreklik {_on(P['boyut']['ceyrek'], 2)} MB, yıllık {_on(P['boyut']['yil'], 2)} MB / çerçeve). 2009–2011 çerçeveleri daha küçük olacağı için üst tahmindir |
| tahmini süre | en az {_on(P['sure_alt_dk'])} dk (hız sınırının izin verdiği); beklenen {_on(P['sure_alt_dk'], 0)}–{_on(P['sure_ust_dk'], 0)} dk (aktarım hızına bağlı) |
| hedef klasör | `{P['klasor']}` (yeni; `K60_SECFRAMES` ile değişir) |
| kaldığı yerden | diskte geçerli dosyası olan çerçeve yeniden istenmez; yarım dosya (`.yarim`) silinir; her dosyanın sha256'sı `_manifest.json`'da |
| 404 | o etiket o dönemde hiç bildirilmemiş (ör. `RevenueFromContractWithCustomerExcludingAssessedTax` 2017 öncesi): `{{}}` işareti yazılır, hata değildir |
| 403 / 407 | SEC ya da ağ geçidi reddi: indirme hemen durur; aynı komut sonra kaldığı yerden sürer |

Komut (ana oturum çalıştırır; kimlik satırı yalnız ortam değişkeninden okunur, hiçbir dosyaya ve günlüğe yazılmaz):

    {K60V_UA_DEGISKEN}='<ad> <iletişim adresi>' python K60_veri.py indir_sec

Sonra: `python K60_veri.py denetle` (manifest sha256 + etiket x dönem şirket sayıları) ve `python K60_veri.py ozet`.

### İsteğe bağlı: EDGAR başvuru dizini (`indir_sec --dizin evet`)
Frames yanıtında başvuru günü (`filed`) alanı YOKTUR (alanlar: accn, cik, entityName, loc, start, end, val) ve `accn` özgün başvuruyu değil o
değeri EN SON bildiren başvuruyu gösterir. Bilgi tarihi için iki yol var: (a) yedek kural: çeyrek sonu + {K60V_ESIK['yedek_bilgi_gun']} gün; (b) EDGAR çeyreklik
dizini (`{K60V_ESIK['dizin']['url']}`; {len(k60v_dizin_listesi())} dosya, 2009Q1–2026Q3, dosya başına ~{_on(K60V_ESIK['boyut_mb']['dizin'], 0)} MB, toplam ~{_on(len(k60v_dizin_listesi()) * K60V_ESIK['boyut_mb']['dizin'] / 1000)} GB) her şirketin her 10-Q / 10-K
başvurusunun gününü verir; K57 `_k57_abd_bilgi_tarihleri` kuralı (çeyrek sonundan sonraki ilk 10-Q / 10-K) bununla 2009'a uzatılabilir.
Dizin varsayılan olarak İNMEZ (iş tanımında yoktu); öneri: `--dizin evet` ile indirilmesi. Aynı kimlik satırı ve hız sınırı kullanılır.

## 3. Yahoo günlük fiyat
| kalem | değer |
|---|---|
| uç | `{Y['url']}` (K57-B ile aynı; tarayıcı kimliği, `events=div,splits`, `includeAdjustedClose=true`) |
| aralık | {Y['bas']} .. {Y['bit']} (okuyucular {Y['kes']}'de keser; bölünme olayları indirme gününe kadar alınır ki o günkü fiyat doğru kurulsun) |
| evren | {_bn(nsem)} sembol: K57-B geniş evren tablosu (`evren_b1.csv`) + V_ABD sembolleri; yalnız bugün kodu olanlar |
| istek | sembol başına 1; {Y['is_parcacigi']} iş parçacığı, istekler arası {_on(Y['bekle'])} sn, {Y['deneme']} deneme; art arda {Y['engel_ardisik']} başarısızlıkta durur |
| hedef klasör | `{K60V_YOL['fiyat']}` (yeni; `K60_FIYAT` ile değişir). `{K60V_YOL['eski_fiyat']}` (K59 girdisi) okunmaz, yazılmaz |
| tahmini boyut / süre | ~{_on(nsem * 0.29 / 1000)} GB; ~{_on(nsem / 210, 0)}–{_on(nsem / 110, 0)} dk (11 Kasım koşusunda ölçülen: 1,36 GB, 23 dk) |
| e-posta | gerekmez |

Komut: `python K60_veri.py indir_fiyat`

## 4. Bu planın kapsamadıkları
- Batan şirketler (yaşayanlar evreni; EVREN_SECENEKLERI.md). Çeyreklik nakit akışı (SEC finansal tablo veri setleri). İçeriden işlem, 13F,
  açığa satış, analist verisi (envanter bölüm C satır 3–10). Ham SEC ve fiyat verisi repoya konmaz; türetilmiş tabloların `islenmis-veri`
  dalına konması ana oturumun / Cemal'in kararıdır.
"""


def k60v_plan(cikti: Optional[str] = None, ek: bool = True, dizin: bool = False) -> str:
    """Planı yazar: K60_VERI_PLANI.md + K60_SEC_ISTEK_LISTESI.csv (tam istek listesi). Ağ kullanılmaz."""
    P = k60v_plan_tablo(ek, dizin)
    L = pd.concat([P["liste"], P["dizin"]], ignore_index=True) if len(P["dizin"]) else P["liste"]
    L = L.assign(durum=np.where(L.mevcut.notna(), "eski onbellekte (indirilmez)", "indirilecek"))
    os.makedirs(cikti or K60V_YOL["cikti"], exist_ok=True)
    L[["grup", "tax", "etiket", "birim", "donem", "durum", "url", "dosya"]].to_csv(_k60v_yol("liste", cikti), index=False)
    yol = _k60v_yaz(_k60v_yol("plan", cikti), k60v_plan_metin(P))
    k60vlog.info("plan: %s (%d istek, ~%.2f GB, en az %.1f dk)", yol, P["istek"], P["mb"] / 1000, P["sure_alt_dk"])
    return yol


# ---------------------------------------------------------------- 10) DENETİM + ÖZET RAPORLARI
def _k60v_durum_oku(klasor: str) -> Dict[str, Any]:
    try:
        with open(os.path.join(klasor, K60V_DOSYA["durum"]), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _k60v_manifest_satir(ad: str, m: Optional[Dict[str, Any]]) -> str:
    if m is None:
        return f"- {ad}: manifest yok (indirme yapılmamış)"
    sorun = "" if m["saglam"] else f" SORUN: sha256 farklı {len(m['farkli'])}, eksik {len(m['eksik'])}, manifest dışı {len(m['fazla'])}"
    return (f"- {ad}: `{m['klasor']}`; {_bn(m['dosya'])} dosya ({_bn(m['tamam'])} veri, {_bn(m['yok_404'])} '404 yok' işareti), "
            f"{_on(m['bayt'] / 1e9, 2)} GB; klasör özeti sha256 `{m['klasor_ozet_sha256']}`; diskle karşılaştırma: {'AYNI' if m['saglam'] else 'FARKLI'}.{sorun}")


def _k60v_sec_yil_tablo(Sy: pd.DataFrame) -> str:
    """Etiket x yıl: çeyreklik / anlık çerçevelerde yılın çeyrek ortalaması şirket sayısı; yalnız yıllık etiketlerde yıllık çerçeve."""
    F = Sy[(Sy.grup != "DIZIN") & Sy.durum.isin(["tamam", "yok_404", "bos"])].copy()
    if not len(F):
        return "(SEC çerçevesi yok)"
    F["yil"] = F.donem.str.slice(2, 6).astype(int); F["dtur"] = F.donem.map(_k60v_donem_turu); F["sirket"] = F.sirket.fillna(0)
    yillar = sorted(F.yil.unique()); out = ["| etiket | çerçeve | " + " | ".join(str(y)[2:] for y in yillar) + " |", "|---|---|" + "---|" * len(yillar)]
    for etiket, g in F.groupby("etiket", sort=False):
        for dt, ad in (("an", "çeyrek sonu"), ("ceyrek", "çeyreklik"), ("yil", "yıllık")):
            h = g[g.dtur == dt]
            if len(h):
                o = h.groupby("yil").sirket.mean()
                out.append(f"| {etiket} | {ad} | " + " | ".join(_bn(o.get(y)) if y in o.index else "·" for y in yillar) + " |")
    return "\n".join(out)


def k60v_denetle(cikti: Optional[str] = None, ek: bool = True) -> Dict[str, Any]:
    """Denetim: (1) iki yeni önbelleğin manifest sha256 doğrulaması, (2) SEC etiket x dönem şirket sayıları (sec_sayim.csv), (3) fiyat kapsamı
    (fiyat_kapsam.csv). K60_VERI_DENETIM.md yazılır. Hiçbir önbellek değiştirilmez; getiri hesaplanmaz."""
    cikti = cikti or K60V_YOL["cikti"]; os.makedirs(cikti, exist_ok=True)
    R = k60v_sec_denetle(ek=ek); Sy = R["sayim"]; Sy.to_csv(_k60v_yol("sec_sayim", cikti), index=False)
    fm = None; K = None
    if os.path.isdir(K60V_YOL["fiyat"]):
        fm = k60v_manifest_dogrula(K60V_YOL["fiyat"]) if os.path.exists(os.path.join(K60V_YOL["fiyat"], K60V_DOSYA["manifest"])) else None
        K = k60v_fiyat_tara(uygunluk=False)["kapsam"]; K.to_csv(_k60v_yol("fiyat_kapsam", cikti), index=False)
    fb = k60v_filed_bulgusu(Sy); kay = Sy.kaynak.value_counts().to_dict(); drm = Sy[Sy.kaynak == "k60"].durum.value_counts().to_dict()
    fk = "(fiyat önbelleği yok)" if K is None else (", ".join(f"{a} {_bn(n)}" for a, n in K.durum.value_counts().items())
                                                     + f"; kırpık seri {_bn(int(K.kirpik.sum()))}")
    metin = f"""# K60 veri denetimi

Yazım zamanı: {_k60v_simdi()}. Üreten: `python K60_veri.py denetle`. Önbellekler değiştirilmedi; getiri hesaplanmadı.

## 1. Manifest (sha256)
{_k60v_manifest_satir('SEC frames (yeni)', R['manifest'])}
{_k60v_manifest_satir('Yahoo fiyat (yeni)', fm)}
Klasör özeti kuralı: ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı (K59 ön kaydındaki kuralla aynı; K60 ön kaydına bu değerler girer).

## 2. SEC çerçeveleri
İstenen {_bn(int((Sy.grup != 'DIZIN').sum()))} çerçeve: yeni önbellekte {_bn(kay.get('k60', 0))}, eski önbellekte (K59 girdisi, yalnız okundu) {_bn(kay.get('eski', 0))}, inmemiş {_bn(kay.get('inmedi', 0))}.
Yeni önbellekteki durumlar: {drm or '—'}. 'filed' alanı: eski çeyreklerde (≤ 2019) {fb['eski_filed']} / {fb['eski_dosya']} dosyada, 2020+ çeyreklerde {fb['yeni_filed']} / {fb['yeni_dosya']} dosyada var.
Görülen veri alanları: {', '.join(fb['alanlar']) or '—'}. EDGAR dizin dosyası: {fb['dizin_dosya']}.

Şirket sayısı (ayrı CIK), etiket x yıl; çeyreklik ve çeyrek sonu çerçevelerde yılın ortalaması (· = çerçeve yok / inmedi). Dönem dönem ayrıntı: `{K60V_DOSYA['sec_sayim']}`.

{_k60v_sec_yil_tablo(Sy)}

## 3. Yahoo fiyat kapsamı
Hisse durumu: {fk}. Ayrıntı: `{K60V_DOSYA['fiyat_kapsam']}`.
"""
    yol = _k60v_yaz(_k60v_yol("denetim", cikti), metin)
    k60vlog.info("denetim: %s | SEC %s | fiyat %s", yol, kay, fk)
    return {"yol": yol, "sec_manifest": R["manifest"], "fiyat_manifest": fm, "sayim": Sy, "kapsam": K, "filed": fb}


def _k60v_b1_kayip(K: pd.DataFrame) -> List[str]:
    """K57-B evren tablosunda durumu 'fiyat' olup yeni önbellekte fiyat serisi olmayan semboller (Yahoo'nun sonradan geçmişini sildiği hisseler)."""
    try:
        B = pd.read_csv(K60V_YOL["evren_b1"], dtype=str)
    except (OSError, ValueError):
        return []
    eski = set(B[B.durum == "fiyat"].sembol)
    return sorted(set(K[K.durum != "fiyat"].sembol) & eski)


def _k60v_ilk_dagilim(K: pd.DataFrame) -> str:
    F = K[K.durum == "fiyat"].copy()
    if not len(F):
        return "(fiyat serisi yok)"
    ilk = pd.to_datetime(F.ilk); bas = pd.Timestamp(K60V_ESIK["yahoo"]["bas"]) + pd.Timedelta(days=7)
    sat = [f"| {K60V_ESIK['yahoo']['bas'][:4]} başı (tam geçmiş) | {_bn(int((ilk <= bas).sum()))} | {_on(100 * float((ilk <= bas).mean()))} |"]
    kalan = ilk[ilk > bas]
    for y, n in kalan.dt.year.value_counts().sort_index().items():
        sat.append(f"| {y} içinde | {_bn(n)} | {_on(100 * n / len(F))} |")
    return "| ilk fiyat günü | hisse | % |\n|---|---|---|\n" + "\n".join(sat)


def k60v_ozet(cikti: Optional[str] = None, ek: bool = True) -> str:
    """Özet: inenler, yıllara göre fiyat paneli ve uygun evren, bilinen yanlılıklar, 'filed' bulgusu. K60_VERI_OZET.md + evren_ay.csv."""
    cikti = cikti or K60V_YOL["cikti"]; os.makedirs(cikti, exist_ok=True); Uy = K60V_ESIK["uygunluk"]; Y = K60V_ESIK["yahoo"]
    R = k60v_sec_denetle(ek=ek); Sy = R["sayim"]; fb = k60v_filed_bulgusu(Sy); kay = Sy[Sy.grup != "DIZIN"].kaynak.value_counts().to_dict()
    sd = _k60v_durum_oku(K60V_YOL["frames"]); fd = _k60v_durum_oku(K60V_YOL["fiyat"])
    if os.path.isdir(K60V_YOL["fiyat"]):
        T = k60v_fiyat_tara(uygunluk=True); K = T["kapsam"]; Yl = T["yil"]
        K.to_csv(_k60v_yol("fiyat_kapsam", cikti), index=False)
        if T["ay"] is not None:
            T["ay"].to_csv(_k60v_yol("evren_ay", cikti), index=False)
        fm = k60v_manifest_dogrula(K60V_YOL["fiyat"]) if os.path.exists(os.path.join(K60V_YOL["fiyat"], K60V_DOSYA["manifest"])) else None
        F = K[K.durum == "fiyat"]; drm = K.durum.value_counts().to_dict(); kr = K[K.kirpik]
        tur = F.tur.fillna("?").value_counts().to_dict()
        fiyat_ozet = (f"{_bn(len(K))} sembol istendi; fiyat serisi olan {_bn(len(F))} (tür: {', '.join(f'{a} {_bn(n)}' for a, n in tur.items())}); "
                      f"durumlar: {', '.join(f'{a} {_bn(n)}' for a, n in drm.items())}. Bölünmesi olan {_bn(int((F.bolunme > 0).sum()))}, "
                      f"temettü olayı olan {_bn(int((F.temettu > 0).sum()))} hisse. İndirme: {fd.get('ilk_indirme_utc', '—')} → {fd.get('son_utc', '—')}, "
                      f"son durum '{fd.get('durum', '—')}', inemeyen {_bn(len(fd.get('inemeyen', []) or []))}.\n"
                      f"Durumların anlamı: 'fiyat' = {Y['kes']} ve öncesinde en az bir günü var; 'yok' = Yahoo bu kodu tanımıyor (404); 'veri yok' = "
                      f"Yahoo kodu tanıyor ama {Y['kes']} ve öncesi için hiç gün vermiyor.\n"
                      f"**Kırpık seri: {_bn(len(kr))} hisse** (Yahoo'nun verdiği ilk gün, hissenin ilk işlem gününden {Y['kirpik_gun']} günden fazla sonra; geçmiş Yahoo "
                      f"tarafında eksik; bunlardan {_bn(int((kr.durum == 'fiyat').sum()))} hissenin kısa da olsa serisi var): {', '.join(kr.sembol.tolist()) or '—'}. "
                      "Yeniden deneme: `python K60_veri.py indir_fiyat --yenile kirpik` (yalnız daha uzun gelen yanıt eskisinin yerine geçer).\n"
                      f"K57-B evren tablosunda (K59 girdisi, 9 Kasım) fiyat serisi olup burada serisi olmayanlar: {', '.join(_k60v_b1_kayip(K)) or '—'} "
                      "(bu hisselerin 2020+ serisi eski önbellekte durur; K60 paneli isterse oradan tamamlar).")
        if "uygun_ort" in Yl:
            ytab = ("| yıl | fiyat serisi olan | tam yıl (≥ 200 gün) | hisse-gün | uygun evren: ay sonu ort. | en az | en çok | yıl sonu uygun | yıl sonu: işlem gören | geçmişi yeten | fiyat ≥ 2 $ | likit ≥ 1 mn $ |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
                    + "\n".join(f"| {int(r.yil)} | {_bn(r.seri)} | {_bn(r.tam_yil_seri)} | {_bn(r.hisse_gun)} | {_bn(r.uygun_ort)} | {_bn(r.uygun_min)} | {_bn(r.uygun_maks)} | "
                                f"{_bn(r.uygun_yil_sonu)} | {_bn(r.islem_yil_sonu)} | {_bn(r.gecmis_yil_sonu)} | {_bn(r.fiyat_yil_sonu)} | {_bn(r.likit_yil_sonu)} |"
                                for r in Yl.itertuples()))
            Ay = T["ay"].assign(ay=T["ay"].ay_sonu.dt.strftime("%Y-%m"))
            dtab = "\n".join(f"| {ad} | {a} .. {b} | {_bn(len(g))} | {_bn(g.uygun.mean())} | {_bn(g.uygun.min())} | {_bn(g.uygun.max())} |"
                             for ad, (a, b) in K60V_ESIK["donem"].items() for g in [Ay[(Ay.ay >= a) & (Ay.ay <= b)]] if len(g))
            dtab = "| dönem | aylar | ay sayısı | uygun evren ort. | en az | en çok |\n|---|---|---|---|---|---|\n" + dtab
        else:
            ytab = "| yıl | fiyat serisi olan | tam yıl (≥ 200 gün) | hisse-gün |\n|---|---|---|---|\n" + "\n".join(
                f"| {int(r.yil)} | {_bn(r.seri)} | {_bn(r.tam_yil_seri)} | {_bn(r.hisse_gun)} |" for r in Yl.itertuples())
            dtab = "(uygun evren hesaplanamadı)"
        ilk_tab = _k60v_ilk_dagilim(K)
    else:
        fm = None; fiyat_ozet = f"Fiyat önbelleği yok (`{K60V_YOL['fiyat']}`): önce `python K60_veri.py indir_fiyat`."; ytab = dtab = ilk_tab = "(fiyat yok)"
    if kay.get("k60", 0):
        sec_ozet = (f"Yeni önbellekte {_bn(kay.get('k60', 0))} çerçeve, eski önbellekte {_bn(kay.get('eski', 0))}, inmemiş {_bn(kay.get('inmedi', 0))}. "
                    f"İndirme: {sd.get('ilk_indirme_utc', '—')} → {sd.get('son_utc', '—')}, son durum '{sd.get('durum', '—')}'.")
    else:
        sec_ozet = (f"SEC indirmesi HENÜZ YAPILMADI (yeni önbellek boş). Eski önbellekte (K59 girdisi) {_bn(kay.get('eski', 0))} çerçeve var; inecek "
                    f"{_bn(kay.get('inmedi', 0))} çerçeve için komut: `{K60V_UA_DEGISKEN}='<ad> <iletişim adresi>' python K60_veri.py indir_sec`.")
    if fb["eski_dosya"]:
        filed = (f"Eski çeyreklerde (≤ 2019) incelenen {fb['eski_dosya']} dosyanın {fb['eski_filed']}'inde, 2020+ çeyreklerde {fb['yeni_dosya']} dosyanın "
                 f"{fb['yeni_filed']}'inde `filed` alanı var.")
    else:
        filed = (f"Eski çeyrekler henüz inmedi; eldeki 2020+ çerçevelerde ({fb['yeni_dosya']} dosya) `filed` alanı olan dosya sayısı {fb['yeni_filed']}. "
                 "Uç ve yanıt şeması bütün dönemlerde aynıdır; indirmeden sonra `denetle` / `ozet` eski çeyrekleri de sayar.")
    yok = fb["eski_filed"] + fb["yeni_filed"] == 0
    metin = f"""# K60 veri özeti (indirmelerden sonra elde ne var)

Yazım zamanı: {_k60v_simdi()}. Üreten: `python K60_veri.py ozet`. Yalnız sayım: sinyal ölçülmedi, getiri istatistiği hesaplanmadı.

## 1. Fiyat (Yahoo, günlük, {Y['bas']} .. {Y['kes']})
{fiyat_ozet}
{_k60v_manifest_satir('Manifest', fm)}

### İlk fiyat gününe göre dağılım
{ilk_tab}

### Yıllara göre fiyat paneli ve uygun evren
Uygun evren kuralı (K59 ile aynı eşikler; her ay sonunda, yalnız o gün ve öncesi bilgiyle): tür {', '.join(Uy['tur'])}; en az {Uy['gecmis_gun']} işlem günü geçmiş;
o günkü fiyat (bölünmeler geri alınmış kapanış) ≥ {_on(Uy['fiyat_min'], 0)} $; son {Uy['likit_gun']} günün medyan işlem değeri ≥ {_on(Uy['likit_min'] / 1e6, 0)} milyon $; son {Uy['ileri_tasima']} işlem gününde fiyatı var.

{ytab}

### K60 dönemlerinde uygun evren
{dtab}

Not: {Uy['gecmis_gun']} gün geçmiş şartı yüzünden fiyatı 2010 başında başlayan hisseler ilk kez 2010'un son ay sonunda uygun olur; 2010'un ilk on bir ayında uygun
evren 0'dır (2010 satırının ortalaması bu yüzden düşüktür). 12 aylık momentum gibi ölçüler KEŞİF başlangıcı (2016) için fazlasıyla geçmişe sahiptir.

## 2. Temel veri (SEC XBRL frames)
{sec_ozet}
{_k60v_manifest_satir('Manifest', R['manifest'])}
Etiket x dönem şirket sayıları: `python K60_veri.py denetle` → `{K60V_DOSYA['denetim']}` ve `{K60V_DOSYA['sec_sayim']}`.

## 3. Bilinen yanlılıklar ve sınırlar
1. **Yalnız yaşayanlar.** Evren, Kasım 2026'da borsa kodu olan şirketlerdir (K57-B evren tablosu + V_ABD). Borsadan çıkan (iflas, birleşme) hiçbir
   şirket yok; Yahoo çıkanların fiyatını vermez. Geriye gidildikçe evren küçülür ve "16 yıl hayatta kalmış" şirketlere yaslanır (yukarıdaki
   tabloda 2011 ile 2026 arasındaki fark bunun ölçüsüdür). Getiriler yukarı yanlıdır; en açık aileler küçüklük, düşük fiyat, sıkıntı (EVREN_SECENEKLERI bölüm 4).
2. **Frames son bildirilen değeri verir.** Bir çeyreğin değeri sonradan düzeltildiyse (yeniden sunum, sınıflama değişikliği) çerçevede düzeltilmiş
   hali durur; o gün bilinen sayı değildir. `accn` alanı da değeri EN SON bildiren başvurudur (çoğu kez bir yıl sonraki karşılaştırmalı tablo).
3. **Başvuru günü (`filed`).** {filed}
   {'Frames yanıtında `filed` alanı YOK (alanlar: ' + ', '.join(fb['alanlar']) + '). ' if yok else ''}2021+ için bilgi tarihi SEC finansal özütlerinden (`/tmp/secfs`, K57 `_k57_abd_bilgi_tarihleri`) geliyor; 2020 ve öncesi için
   özüt yok. **Yedek kural: bilgi tarihi = çeyrek sonu + {K60V_ESIK['yedek_bilgi_gun']} gün** (10-Q yasal süresi 40–45 gün, 10-K 60–90 gün; +{K60V_ESIK['yedek_bilgi_gun']} gün çeyrek raporları için tutucudur, küçük
   şirketlerin yıllık raporu için sınırdadır; geç başvuranlarda (NT 10-K / 10-Q) geleceğe bakma riski kalır). Daha iyisi: EDGAR çeyreklik başvuru
   dizini (`indir_sec --dizin evet`; şu an {fb['dizin_dosya']} dizin dosyası var) her 10-Q / 10-K'nın gerçek gününü verir.
4. **XBRL'e geçiş takvimi.** XBRL zorunluluğu kademeli geldi: en büyük şirketler 2009 ortası, öteki büyükler 2010 ortası, küçük şirketler 2011 ortasından
   sonra biten dönemler. 2009–2011 çerçevelerinde küçük şirketler yoktur; temel veride tam kapsam fiilen 2011Q2'den, yıllık büyüme ölçülerinde 2012'den başlar.
5. **Nakit akış kalemleri yalnız yıllık** (plan bölüm 2). Çeyreklik OCF, yatırım harcaması, geri alım, ihraç bu veriyle kurulamaz.
6. **Pay sayısı.** Kapak sayfası pay sayısının tarihi çeyrek sonu değildir; çok sınıflı şirketlerde boyutlu bildirildiği için çerçevede olmayabilir
   (yedekler: bilanço pay sayısı, ağırlıklı ortalama pay). Bölünme düzeltmesi Yahoo bölünme olaylarıyla yapılır.
7. **CIK → borsa kodu eşlemesi bugünkü.** `company_tickers.json` bugünün kodunu verir; kod değiştirmiş şirketin eski fiyatı Yahoo'da yeni kod altında
   durur (sorun yok), ama yeniden kullanılmış kodlarda (K54: 9 örnek) fiyat ile temel veri farklı şirketlere ait olabilir.
8. **Yahoo fiyatı.** `close` bölünme düzeltmeli, `adjclose` temettü de düzeltilmiş; düzeltme katsayıları indirme günündeki haliyledir. Tekil hatalı
   günler (sıfır hacim, uç fiyat) temizlenmedi; K59'daki "en büyük tek hisse getirisi" denetimi K60'ta da gerekir. Yahoo bazı hisselerin geçmişini
   geçici olarak eksik verir (yukarıdaki "kırpık seri" listesi; 11 Kasım'da ROKU gibi büyük hisseler de vardı); liste her indirmede yeniden bakılmalıdır.
9. **Fon krizi kesimi.** Okuyucular fiyatı {Y['kes']}'de keser (KASA dönemi Ağustos 2026'da biter).
"""
    yol = _k60v_yaz(_k60v_yol("ozet", cikti), metin)
    k60vlog.info("özet: %s", yol)
    return yol


def _cakisma_kontrol_k60v(_once=_CK_ONCE_K60V, _dosya="K60_veri.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K60V", "_CK_KAYIT", "_cakisma_kontrol_k60v", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "gzip", "hashlib", "json", "logging", "pickle", "re", "ssl", "threading", "time", "urllib", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "ThreadPoolExecutor", "as_completed", "K57", "_dt")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k60v()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=K60V_SURUM)
    ap.add_argument("komut", choices=["plan", "indir_sec", "indir_fiyat", "denetle", "ozet"])
    ap.add_argument("--cikti", default=None, help="çıktı klasörü (varsayılan arastirma_cikti/k60_veri)")
    ap.add_argument("--ek", choices=["evet", "hayir"], default="evet", help="EK grubu etiketleri (temettü, yedek pay sayıları)")
    ap.add_argument("--dizin", choices=["evet", "hayir"], default="hayir", help="EDGAR başvuru dizinini de indir / plana kat")
    ap.add_argument("--hiz", type=float, default=None, help="SEC istek hızı (saniyede; üst sınır 8)")
    ap.add_argument("--adet", type=int, default=None, help="yalnız ilk N iş (deneme için)")
    ap.add_argument("--yenile", choices=["kirpik"], default=None, help="indir_fiyat: kırpık / boş gelen hisseleri yeniden iste")
    a = ap.parse_args()
    try:
        if a.komut == "plan":
            y_ = k60v_plan(a.cikti, ek=a.ek == "evet", dizin=a.dizin == "evet")
            with open(y_, encoding="utf-8") as f_:
                print(f_.read())
        elif a.komut == "indir_sec":
            d_ = k60v_sec_indir(hiz=a.hiz, ek=a.ek == "evet", dizin=a.dizin == "evet", adet=a.adet)
            print(json.dumps({k_: v_ for k_, v_ in d_.items() if k_ != "inemeyen"}, ensure_ascii=False, indent=1))
            sys.exit(0 if d_["durum"] == "tamam" else 3)
        elif a.komut == "indir_fiyat" and a.yenile:
            print(json.dumps(k60v_fiyat_yenile(), ensure_ascii=False, indent=1))
        elif a.komut == "indir_fiyat":
            d_ = k60v_fiyat_indir(adet=a.adet)
            print(json.dumps({k_: v_ for k_, v_ in d_.items() if k_ != "inemeyen"}, ensure_ascii=False, indent=1))
            sys.exit(0 if d_["durum"] == "tamam" else 3)
        elif a.komut == "denetle":
            r_ = k60v_denetle(a.cikti, ek=a.ek == "evet")
            for ad_, m_ in (("SEC frames", r_["sec_manifest"]), ("Yahoo fiyat", r_["fiyat_manifest"])):
                print(_k60v_manifest_satir(ad_, m_))
            print(r_["yol"])
        else:
            print(k60v_ozet(a.cikti, ek=a.ek == "evet"))
    except K60VKimlikYok as ex:
        k60vlog.error("%s", ex); sys.exit(2)
    except K60VHata as ex:
        k60vlog.error("%s", ex); sys.exit(1)
