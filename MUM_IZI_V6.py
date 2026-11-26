"""MUM_IZI_V6 — MUM_IZI EK 9: v6 = v5M ∧ küçük mum (K*) ∧ muntazam dizilim (D*) ∧ net Bollinger daralması (BB*) (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI9_IS_TANIMI.md (commit fd454da; ana model). Cemal MUM_IZI8_ONAY'ı işaretledi (24'ün 2'si BENZİYOR: v5M geçersiz)
ve yazdı: "Mumlar küçük olmalı, dizilim muntazam olmalı, Bollinger daralması net olmalı." Bu iş ETİKETLERİ KULLANIR. v5M yapısı aynen kalır; her yeni sözcük
için 4 önceden yazılı aday ölçü (K1-K4, D1-D4, BB1-BB4); eşik tek kuralla (EVET sayfalarının ve ölçülebiliyorsa şablonun EN KÖTÜ değeri, %5 pay); puan =
reddedilen HAYIR payı; sözcük başına en yüksek puanlı tek aday; puan < 0,15 -> o sözcükte kapı yok; v6 HAYIR'ların yarısından azını reddediyorsa DUR.
GETİRİ / SONRASI YOK. Eski kodlar değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz. Ön kayıttan (MUM_IZI9_ON_KAYIT.md) sonra kural değişmez.

Komut:  python MUM_IZI_V6.py aday       etiket kümesi + 12 aday tablosu + seçim (mum_izi9_aday.json / .csv)
        python MUM_IZI_V6.py sentetik   v6 sentetiği (mum_izi9_sentetik.json)
        python MUM_IZI_V6.py onkayit    MUM_IZI9_ON_KAYIT.md
        python MUM_IZI_V6.py tarama     kapı -> evren taraması, sayım, onay seçimi (mum_izi9_tarama.json)
        python MUM_IZI_V6.py onay       MUM_IZI9_ONAY.pdf + mum_izi9_onay_anahtar.json + mum_izi9_sonuc.json
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_V6 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_V6 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_V6 not in sys.path:
    sys.path.insert(0, KOK_V6)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V3 as V3  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V4 as V4  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V5 as V5  # noqa: E402  (DEĞİŞTİRİLMEZ)

v6log = logging.getLogger("col.mum_izi_v6")
if not v6log.handlers:
    _v6_h = logging.StreamHandler(sys.stderr)
    _v6_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_v6: %(message)s", "%H:%M:%S"))
    v6log.addHandler(_v6_h)
    v6log.setLevel(logging.INFO)
    v6log.propagate = False


class V6Hata(RuntimeError):
    """Durdurucu hata: seçim / kapı / mühür / veri / kesik."""


V6_SURUM = "MUM_IZI_V6 v1.0 (2026-11-26): v6 = v5M ∧ K* ∧ D* ∧ BB* (Cemal: küçük mum, muntazam dizilim, net Bollinger daralması)"
V5M = "R4+M"
V6_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_V6, "MUM_IZI_V6.py"), "gecici": "/tmp/mum_izi/v6",
          "isaret8": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi8_onay.json"), "anahtar8": os.path.join(MI.MI_YOL["cikti"], "mum_izi8_onay_anahtar.json"),
          "aday8": os.path.join(MI.MI_YOL["cikti"], "mum_izi8_aday.csv"), "isaret6": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi6_etiket.json"),
          "anahtar6": os.path.join(MI.MI_YOL["cikti"], "mum_izi6_anahtar.json"), "anahtar4": os.path.join(MI.MI_YOL["cikti"], "mum_izi4_onay_anahtar.json")}
V6_DOSYA = {"onkayit": "MUM_IZI9_ON_KAYIT.md", "rapor": "MUM_IZI9_RAPOR.md", "sonuc": "mum_izi9_sonuc.json", "aday": "mum_izi9_aday.json",
            "aday_csv": "mum_izi9_aday.csv", "sentetik": "mum_izi9_sentetik.json", "tarama": "mum_izi9_tarama.json", "onay": "MUM_IZI9_ONAY.pdf",
            "anahtar": "mum_izi9_onay_anahtar.json"}
# aday: (sözcük, yön 'kucuk' = küçük iyi / 'buyuk' = büyük iyi / 'ikili', şablonda ölçülür mü)
ADAY: Dict[str, Tuple[str, str, bool]] = {
    "K1": ("K", "kucuk", True), "K2": ("K", "kucuk", True), "K3": ("K", "kucuk", False), "K4": ("K", "kucuk", True),
    "D1": ("D", "kucuk", True), "D2": ("D", "buyuk", True), "D3": ("D", "buyuk", True), "D4": ("D", "kucuk", True),
    "BB1": ("BB", "kucuk", True), "BB2": ("BB", "kucuk", True), "BB3": ("BB", "kucuk", False), "BB4": ("BB", "ikili", True)}

V6_ESIK: Dict[str, Any] = {
    "surum": "V6-1.0",
    "taban": "v5M = MUM_IZI_V5 'R4+M' (Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ M) aynen; k = çıkış mumu (pencerenin ilk SMA üstü kapanışı); tırmanış = k+1..m-1",
    "olcu": {"K1": "bölgedeki (bütün mumlar) en büyük gövde |C - O| / (üst bant - SMA) (b birimi)",
             "K2": "medyan mum boyu (H - L) / bant genişliği (üst bant - alt bant), bölgenin bütün mumları",
             "K3": "bölgenin medyan mum boyu / bölgeden önceki 60 barın medyan mum boyu (en az 20 bar; şablonda ölçülemez -> şablon şartından muaf)",
             "K4": "çıkış mumunun gövdesi |C_k - O_k| / (üst bant_k - SMA_k)",
             "D1": "çıkış + tırmanışta (i = k..m-1) en büyük kapanış adımı |C_i - C_i-1| / (üst bant_i - SMA_i)",
             "D2": "bölgede ardışık mum örtüşmesi ortalaması (MI 'ortusme': ortak aralık / küçük mum boyu)",
             "D3": "tırmanış kapanışlarının (fiyat) sıra numarasına doğrusal uyumu R²",
             "D4": "tırmanışta mum boyu (H - L) değişkenliği: std (ddof 0) / ortalama",
             "BB1": "bölge içi en dar bant genişliği / bölgenin ilk 3 mumundaki ortalama bant genişliği",
             "BB2": "bölge içi en dar bant genişliği / [max(19, bölge başı - 20), bölge sonu] aralığındaki en geniş bant genişliği (şablonda yalnız görüntüdeki "
                    "20 mum)",
             "BB3": "en dar noktadaki (bant genişliği / SMA) değerinin o güne kadarki son 120 bardaki (geçerli, en az 20) yüzdeliği (değer <= o gün payı; "
                    "şablonda ölçülemez -> muaf)",
             "BB4": "en dar noktanın bölge içindeki yeri (sıra / (m - 1)) 0,25-0,90 arasında (ikili)"},
    "yon": {a: v[1] for a, v in ADAY.items()},
    "esik_kurali": "eşik = EVET sayfalarının ve (ölçülebiliyorsa) şablonun EN KÖTÜ değeri, %5 payla gevşetilir: 'küçük iyi' -> en büyük x 1,05; 'büyük iyi' -> en "
                   "küçük x 0,95; ikili (BB4) ancak bütün EVET ve şablon sağlıyorsa aday. Bir EVET sayfasında ölçü tanımsızsa (geçmiş yetersiz) aday GEÇERSİZ",
    "pay": 0.05,
    "puan": "eşikle reddedilen HAYIR sayfası payı (tanımsız ölçü = reddedildi); sözcük başına en yüksek puanlı TEK aday (eşitlikte listedeki ilk); puan < 0,15 "
            "-> o sözcükte kapı YOK",
    "puan_en_az": 0.15,
    "dur": "v6 (v5M ∧ seçilen kapılar) HAYIR sayfalarının yarısından azını reddediyorsa DUR (PDF yok)", "dur_pay": 0.5,
    "etiket": "EVET = Cemal'in BENZİYOR dediği v5M sayfaları: MUM_IZI8_ONAY 'EVET' + önceki 61 etikette v5M VAR olup EVET; HAYIR = MUM_IZI8_ONAY 'HAYIR' + önceki 61'de "
              "v5M VAR olup HAYIR; IKISI / YOK / BELIRSIZ karar dışı. Pencere: MUM_IZI8 sayfalarında anahtardaki (son, m) ve k; önceki 61'de sayfanın kendi penceresi",
    "kural": "bir son, uzunluklardan (16-24) birinde pencere v5M VAR VE seçilen kapıların hepsini geçiyorsa v6 VAR; kapı ölçüsü tanımsızsa geçmez",
    "sentetik": {"kok": 25112091, "tohum": 200, "gurultu": [0.0, 0.1, 0.2], "baglam": ["dip", "yatay"], "uretec": ["blok", "ry"], "tol": 3,
                 "negatif": {"n1": "fitilsiz büyük gövde (MV n1)", "n2": "fitiller ters (MV n2)", "n5": "aynı mumlar yatay yol (MV p1)",
                             "n8": "tek dev mumla çıkış: çıkış mumu açılışı önceki kapanış, gövdesi şablonun en büyük gövdesinin KAT katı; sonraki mumlar aynı fazla "
                                   "kadar yukarı. 'Sentetik bantta ölçülerek kurulur': KAT 6 / 9 / 13,5 / 20 sırayla denenir (aynı tohum), gömülü pencerenin kendi "
                                   "k'sındaki gövde >= 1,2 b olan ilk KAT alınır (hiçbiri değilse 20) (kendi ölçüsü: çıkış gövdesi >= 1,2 b)",
                             "n9": "daralmasız: kalıbın önündeki 25 barda fiyat hareketleri ve mum boyları 3 kat (oynak dönem; gömme birimi de büyür): kendi ölçüsü "
                                   "BB* (yoksa BB1) eşiği bozuluyor mu",
                             "n10": "dağınık: aynı kapanış yolu, her mumun boyu (O / H / L kapanışa göre) U(0,5, 3) katla çarpılır (tohumla): kendi ölçüsü D* (yoksa D4)"},
                 "kendi_olcu": {"n1": "B (v5)", "n2": "M", "n5": "T", "n8": "çıkış gövdesi >= 1,2 (b)", "n9": "BB*", "n10": "D*"},
                 "dogrulama": "gömülü pencerenin kendisinde (sentetik bant), pencerenin kendi k'sıyla; tohumların >= %80'inde ihlal -> GEÇERLİ, yoksa sayılmaz",
                 "gecerli_pay": 0.80, "n9": {"bar": 25, "kat": 3.0}, "n8_kat": [6.0, 9.0, 13.5, 20.0], "n10": [0.5, 3.0], "yanlis": {"seri": 200, "n": 1000},
                 "kabul_olcutu": "%10 gürültüde pozitif VAR >= %40; geçerli negatiflerde VAR <= %10 (bütün gürültüler); rastgele seride tekil VAR <= 0,5 / 1.000 bar",
                 "esik": {"poz": 0.40, "neg": 0.10, "rastgele": 0.5}},
    "tarama": {"gunluk": ["2016-01-01", "2022-12-31"], "haftalik": ["2001-01-01", "2022-12-31"], "evren": "MUM_IZI8 ile aynı (ETIKET2 P2 / BIST maskeleri)",
               "tekil": "< 15 mum zinciri, en yüksek v1 S'li hiza", "sayim": "v6 VAR (evren içi ve hepsi) pazar x dilim; v5M sayısına oranı (MUM_IZI8 taraması)"},
    "onay": {"tohum": 25112093, "gunluk": 12, "haftalik": 12, "bist_tavan": 4, "en_az": 8,
             "secim": "evren içi tekil v6 VAR olaylarından RASTGELE; önce haftalık sonra günlük; hisse başına bir; önceki üç setin (MUM_IZI4 / 6 / 8) hisseleri "
                      "hariç; BIST dilim başına <= 4; dilimde 12'den az varsa hepsi; toplam < 8 -> DUR",
             "sayfa": "MUM_IZI8_ONAY düzeni + yeni üç sayı (küçük mum, dizilim, daralma)", "esik": "24'ün >= 19'u ✓"},
}

V6_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşik EVET'lerden, puan HAYIR'lardan (iç örnek; ezber riski raporda); negatifler kendi ölçüsünde doğrulanır; rastgele seri tabanı; getiri yok"),
    "K2": ("EVET", "bütün ölçüler pencere sonuna kadarki veriyle (K3 önceki 60 bar, BB2 önceki 20 bar, BB3 o güne kadarki 120 bar); test: seri t'de kesilince aynı; "
                   "veri <= 2022-12-31 + KASA"),
    "K3": ("EVET", "geçerli bar; haftalıkta eksik haftalı pencere atılır; BIST medyan üstü; ABD / AVR P2"),
    "K4": ("EVET", "tekil < 15 mum (en yüksek v1 S); etiketlerde her sayfa bir kez (tekrar sayfaları dışarıda)"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok"),
    "K6": ("EVET", "ölçüler oransal / b birimi"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; yalnız sayım ve görsel onay"),
    "K8": ("EVET", "EVET 6 / HAYIR 18 civarı (raporda doğrulanır): çok küçük; eşikler EVET'lere oturtuldu, gerçek sınama yeni PDF"),
    "K9": ("EVET", "MUM_IZI9_ON_KAYIT.md: KOD9, ESIK9, ADAY9, SENTETIK9 sha + eski kod sha'ları; v6_kapi tarama öncesi"),
    "K10": ("EVET", "etiket şeması v4_etiket_oku ile (bilinmeyen değer DUR); MUM_IZI8 sayfalarında anahtardaki k ile yeniden hesaplanan k aynı ve v5M VAR (denetim)"),
    "K11": ("EVET", "v6_olcu_duz: tek pencerede 12 ölçü düz döngüyle; etiket sayfalarında vektörlü / döngü aynı"),
    "K12": ("EVET", "seçim önceden yazılı kuralla; 'iz' sözü yok; iç örnek uyarısı"),
    "K13": ("EVET", "çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _v6_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or V6_YOL["cikti"], V6_DOSYA[ad])


def v6_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or V6_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


# ================================================================ 1) ÖLÇÜLER
def v6_olcu(O, H, L, C, BU, BO, BA, s: int, e: int, k: int, sablon: bool = False) -> Dict[str, float]:
    """Seri bağlamında pencere [s, e] (k = pencere içi çıkış mumu sırası) için 12 aday ölçü. sablon True: diziler yalnız şablonun mumları
    (K3 / BB3 tanımsız; BB2 yalnız görüntüdeki mumlarla)."""
    O, H, L, C, BU, BO, BA = (np.asarray(x, float) for x in (O, H, L, C, BU, BO, BA)); m = e - s + 1; sl = slice(s, e + 1)
    hw = BU - BO; W = BU - BA; rg = H - L; out = {a: float("nan") for a in ADAY}
    if not (0 < k < m) or not np.all(hw[sl] > 0):
        return out
    out["K1"] = float(np.max(np.abs(C[sl] - O[sl]) / hw[sl]))
    out["K2"] = float(np.median(rg[sl] / W[sl]))
    if not sablon:
        i0 = max(0, s - 60)
        if s - i0 >= 20:
            ref = float(np.median(rg[i0:s]))
            out["K3"] = float(np.median(rg[sl]) / ref) if ref > 0 else float("nan")
    kk = s + k; out["K4"] = float(abs(C[kk] - O[kk]) / hw[kk])
    i = np.arange(kk, e + 1); out["D1"] = float(np.max(np.abs(C[i] - C[i - 1]) / hw[i]))
    Hs, Ls = H[sl], L[sl]; r = np.maximum(Hs - Ls, 1e-12)
    out["D2"] = float(np.mean(np.maximum(np.minimum(Hs[1:], Hs[:-1]) - np.maximum(Ls[1:], Ls[:-1]), 0.0) / np.minimum(r[1:], r[:-1])))
    t = np.arange(kk + 1, e + 1)
    if len(t) >= 3:
        y = C[t]; x = np.arange(len(t), dtype=float); xc = x - x.mean(); yc = y - y.mean(); den = (xc ** 2).sum() * (yc ** 2).sum()
        out["D3"] = float((xc * yc).sum() ** 2 / den) if den > 0 else 0.0
        rt = rg[t]; out["D4"] = float(rt.std() / rt.mean()) if rt.mean() > 0 else float("nan")
    Wr = W[sl]; jn = int(np.argmin(Wr)); out["BB1"] = float(Wr.min() / Wr[:3].mean())
    a0 = s if sablon else max(19, s - 20); out["BB2"] = float(Wr.min() / np.max(W[a0:e + 1]))
    if not sablon:
        g = s + jn; rel = W / np.where(BO != 0, BO, np.nan); h = rel[max(0, g - 119):g + 1]; h = h[np.isfinite(h)]
        if len(h) >= 20:
            out["BB3"] = float(np.mean(h <= rel[g]))
    out["BB4"] = float(0.25 <= jn / (m - 1) <= 0.90)
    return out


def v6_olcu_duz(O, H, L, C, BU, BO, BA, s: int, e: int, k: int, sablon: bool = False) -> Dict[str, float]:
    """K11: aynı ölçüler düz döngüyle."""
    m = e - s + 1; out = {a: float("nan") for a in ADAY}; kk = s + k
    hw = [BU[j] - BO[j] for j in range(len(C))]; W = [BU[j] - BA[j] for j in range(len(C))]; rg = [H[j] - L[j] for j in range(len(C))]
    if not (0 < k < m) or any(hw[j] <= 0 for j in range(s, e + 1)):
        return out
    out["K1"] = max(abs(C[j] - O[j]) / hw[j] for j in range(s, e + 1))
    out["K2"] = float(np.median([rg[j] / W[j] for j in range(s, e + 1)]))
    if not sablon and s - max(0, s - 60) >= 20:
        out["K3"] = float(np.median(rg[s:e + 1]) / np.median(rg[max(0, s - 60):s]))
    out["K4"] = abs(C[kk] - O[kk]) / hw[kk]
    out["D1"] = max(abs(C[j] - C[j - 1]) / hw[j] for j in range(kk, e + 1))
    ov = []
    for j in range(s + 1, e + 1):
        ov.append(max(min(H[j], H[j - 1]) - max(L[j], L[j - 1]), 0.0) / min(max(H[j] - L[j], 1e-12), max(H[j - 1] - L[j - 1], 1e-12)))
    out["D2"] = sum(ov) / len(ov)
    t = list(range(kk + 1, e + 1))
    if len(t) >= 3:
        y = [C[j] for j in t]; n = len(y); mx = (n - 1) / 2; my = sum(y) / n
        sxy = sum((i - mx) * (y[i] - my) for i in range(n)); sxx = sum((i - mx) ** 2 for i in range(n)); syy = sum((v - my) ** 2 for v in y)
        out["D3"] = sxy * sxy / (sxx * syy) if sxx * syy > 0 else 0.0
        r_ = [rg[j] for j in t]; mu = sum(r_) / n; out["D4"] = (sum((v - mu) ** 2 for v in r_) / n) ** 0.5 / mu
    Wr = W[s:e + 1]; jn = min(range(m), key=lambda j: (Wr[j], j)); out["BB1"] = Wr[jn] / (sum(Wr[:3]) / 3)
    a0 = s if sablon else max(19, s - 20); out["BB2"] = Wr[jn] / max(W[a0:e + 1])
    if not sablon:
        g = s + jn; h = [W[j] / BO[j] for j in range(max(0, g - 119), g + 1) if BO[j] != 0 and np.isfinite(W[j] / BO[j])]
        if len(h) >= 20:
            out["BB3"] = sum(1 for v in h if v <= W[g] / BO[g]) / len(h)
    out["BB4"] = float(0.25 <= jn / (m - 1) <= 0.90)
    return out


def v6_gec(o: Dict[str, float], kapi: Dict[str, Dict[str, Any]]) -> Dict[str, bool]:
    """Seçilen kapılar: {sözcük: {'aday', 'esik', 'yon'}} -> geçti mi (tanımsız -> geçmez)."""
    out = {}
    for soz, g in kapi.items():
        v = o.get(g["aday"], float("nan"))
        if not np.isfinite(v):
            out[soz] = False
        elif g["yon"] == "kucuk":
            out[soz] = bool(v <= g["esik"])
        elif g["yon"] == "buyuk":
            out[soz] = bool(v >= g["esik"])
        else:
            out[soz] = bool(v >= 0.5)
    return out


# ================================================================ 2) SERİ TARAMASI
def v6_tara_seri(O, H, L, C, kapi: Dict[str, Dict[str, Any]], bosluk: Optional[np.ndarray] = None, sonlar: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Her son: v5M ve v6 VAR (16-24), v6 VAR pencerelerinde en yüksek v1 S, uzunluğu, k'sı ve ölçüleri (sözlük)."""
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C)); T_ = len(C); BU, BO, BA = MI.mi_bant(C); s0 = 19
    bc = np.r_[0, np.cumsum(bosluk.astype(np.int64))] if bosluk is not None else None
    out = {"v5M": np.zeros(T_, bool), "VAR": np.zeros(T_, bool), "S": np.full(T_, np.nan), "m": np.zeros(T_, np.int64), "k": np.full(T_, -1, np.int64), "olcu": {}}
    for m in V5.V5_ESIK["uzunluklar"]:
        e = np.arange(s0 + m - 1, T_)
        if sonlar is not None:
            e = np.intersect1d(e, np.asarray(sonlar, np.int64))
        if bc is not None and len(e):
            e = e[(bc[e + 1] - bc[e - m + 2]) == 0]
        if not len(e):
            continue
        idx = (e - m + 1)[:, None] + np.arange(m)[None, :]
        P = V5.v5_parcalar(O[idx], H[idx], L[idx], C[idx], BU[idx], BO[idx]); on = V5.v5_kural(P, V5M)
        out["v5M"][e[on]] = True
        for j in np.flatnonzero(on):
            ee = int(e[j]); ss = ee - m + 1; kk = int(P["k"][j]); o = v6_olcu(O, H, L, C, BU, BO, BA, ss, ee, kk)
            if not all(v6_gec(o, kapi).values()):
                continue
            Sv = float(MI.mi_S_pencere(O[None, ss:ee + 1], H[None, ss:ee + 1], L[None, ss:ee + 1], C[None, ss:ee + 1], BU[None, ss:ee + 1], BO[None, ss:ee + 1],
                                       BA[None, ss:ee + 1], V5._v5_sab())[0])
            if not out["VAR"][ee] or Sv > out["S"][ee]:
                out["S"][ee] = Sv; out["m"][ee] = m; out["k"][ee] = kk; out["olcu"][ee] = o
            out["VAR"][ee] = True
    return out


# ================================================================ 3) ETİKET KÜMESİ, ADAY TABLOSU, SEÇİM
def v6_etiketler() -> pd.DataFrame:
    """EVET / HAYIR: MUM_IZI8_ONAY sayfaları (karar verilenler) + önceki 61'de v5M VAR olanlar. Bilgi için önceki 61'in tamamı ve MUM_IZI8 kararsızları da döner
    ('kume' sütunu)."""
    E8 = V4.v4_etiket_oku(V6_YOL["isaret8"]); A8 = {int(r["sayfa"]): r for r in json.load(open(V6_YOL["anahtar8"], encoding="utf-8"))["sayfalar"]}
    rows = []
    for pg, r in sorted(A8.items()):
        lab, t = E8.get(pg, (None, "eksik"))
        rows.append({"set": "set3", "sayfa": pg, "zaman": r["zaman"], "pazar": r["pazar"], "sembol": r["sembol"], "tarih": r["tarih"], "m": int(r["m"]), "k_anahtar": int(r["k"]),
                     "isaret": t, "cemal": lab, "v5M_onceki": True})
    T = pd.read_csv(V6_YOL["aday8"]); X61 = V5.v5_etiketler()
    X61 = X61.merge(T[["set", "sayfa", V5M]].rename(columns={V5M: "v5m_csv"}), on=["set", "sayfa"], how="left", validate="one_to_one")
    for r in X61.itertuples():
        rows.append({"set": r.set, "sayfa": int(r.sayfa), "zaman": r.zaman, "pazar": r.pazar, "sembol": r.sembol, "tarih": r.tarih, "m": int(r.m), "k_anahtar": -1,
                     "isaret": "EVET" if int(r.cemal) == 1 else "HAYIR", "cemal": int(r.cemal), "v5M_onceki": bool(r.v5m_csv)})
    X = pd.DataFrame(rows)
    X["kume"] = np.where(X.v5M_onceki & X.cemal.notna(), "karar", "bilgi")
    return X


def v6_aday(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V6_YOL["cikti"]; X = v6_etiketler(); Vc: Dict[Any, Any] = {}; rows = []
    for r in X.itertuples():
        W = V3.v3_pencere(r.zaman, r.pazar, r.sembol, r.tarih, int(r.m), Vc); d = W["d"]; t = W["t"]; m = int(r.m); s = t - m + 1
        O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); BU, BO, BA = MI.mi_bant(C)
        P = V5.v5_parcalar(*(x[None, s:t + 1] for x in (O, H, L, C, BU, BO))); k = int(P["k"][0]); v5m = bool(V5.v5_kural(P, V5M)[0])
        if r.set == "set3" and (k != int(r.k_anahtar) or not v5m):
            raise V6Hata(f"K10: MUM_IZI8 sayfa {r.sayfa} v5M / k anahtarla uyuşmuyor")
        if r.set != "set3" and v5m != bool(r.v5M_onceki):
            raise V6Hata(f"K10: {r.set} sayfa {r.sayfa} v5M mum_izi8_aday.csv ile uyuşmuyor")
        o = v6_olcu(O, H, L, C, BU, BO, BA, s, t, k) if k > 0 else {a: float("nan") for a in ADAY}
        if k > 0:
            od = v6_olcu_duz(list(O), list(H), list(L), list(C), list(BU), list(BO), list(BA), s, t, k)
            for a in ADAY:
                if not ((np.isnan(o[a]) and np.isnan(od[a])) or abs(o[a] - od[a]) < 1e-9):
                    raise V6Hata(f"K11: {a} düz döngü farklı ({r.set} {r.sayfa})")
        rows.append({**{c: getattr(r, c) for c in ("set", "sayfa", "zaman", "pazar", "isaret", "cemal", "kume")}, "k": k, "v5M": v5m, **o})
    T = pd.DataFrame(rows)
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]; Ps = V5.v5_parcalar(*(a[x] for x in ("O", "H", "L", "C", "BU", "BO"))); ks = int(Ps["k"][0])
    sab = v6_olcu(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], 0, len(a["C"]) - 1, ks, sablon=True)
    K = T[T.kume == "karar"]; ev = K[K.cemal == 1]; ha = K[K.cemal == 0]; tab: Dict[str, Any] = {}; pay = V6_ESIK["pay"]
    for ad, (soz, yon, sab_olc) in ADAY.items():
        e = ev[ad].to_numpy(float); h = ha[ad].to_numpy(float); sv = sab[ad] if sab_olc else float("nan")
        satir = {"sozcuk": soz, "yon": yon, "evet_min": float(np.nanmin(e)) if np.isfinite(e).any() else None, "evet_max": float(np.nanmax(e)) if np.isfinite(e).any() else None,
                 "hayir_medyan": float(np.nanmedian(h)) if np.isfinite(h).any() else None, "sablon": None if not np.isfinite(sv) else float(sv), "evet_tanimsiz": int((~np.isfinite(e)).sum())}
        tum = np.r_[e, [sv] if sab_olc else []]
        if (~np.isfinite(e)).any() or (sab_olc and not np.isfinite(sv)):
            satir.update({"gecerli": False, "neden": "EVET / şablon ölçüsü tanımsız", "esik": None, "puan": None}); tab[ad] = satir; continue
        if yon == "ikili":
            if not np.all(tum >= 0.5):
                satir.update({"gecerli": False, "neden": "bütün EVET ve şablon sağlamıyor", "esik": None, "puan": None}); tab[ad] = satir; continue
            esik = 0.5; red = ~(np.nan_to_num(h, nan=0.0) >= 0.5)
        elif yon == "kucuk":
            esik = float(np.max(tum) * (1 + pay)); red = ~(np.nan_to_num(h, nan=np.inf) <= esik)
        else:
            esik = float(np.min(tum) * (1 - pay)); red = ~(np.nan_to_num(h, nan=-np.inf) >= esik)
        satir.update({"gecerli": True, "esik": esik, "puan": float(red.mean()) if len(h) else None, "red_n": int(red.sum())}); tab[ad] = satir
    kapi: Dict[str, Dict[str, Any]] = {}; sec = {}
    for soz in ("K", "D", "BB"):
        ad_l = [a for a, v in ADAY.items() if v[0] == soz and tab[a]["gecerli"]]
        if not ad_l:
            sec[soz] = {"aday": None, "neden": "geçerli aday yok"}; continue
        en = max(ad_l, key=lambda a: (tab[a]["puan"], -list(ADAY).index(a)))
        if tab[en]["puan"] < V6_ESIK["puan_en_az"]:
            sec[soz] = {"aday": None, "neden": f"en iyi {en} puanı {tab[en]['puan']:.3f} < 0,15: kapı yok"}; continue
        kapi[soz] = {"aday": en, "esik": tab[en]["esik"], "yon": ADAY[en][1]}; sec[soz] = {"aday": en, "puan": tab[en]["puan"], "esik": tab[en]["esik"]}
    for i, r in T.iterrows():
        g = v6_gec({a: r[a] for a in ADAY}, kapi)
        for soz in ("K", "D", "BB"):
            T.loc[i, f"g_{soz}"] = g.get(soz, True)
        T.loc[i, "v6"] = bool(r["v5M"] and all(g.values()))
    T["v6"] = T.v6.astype(bool)
    K = T[T.kume == "karar"]; ha = K[K.cemal == 0]; ev = K[K.cemal == 1]
    ortak = float((~ha.v6).mean()) if len(ha) else None
    durum = "DUR" if (ortak is None or ortak < V6_ESIK["dur_pay"]) else "SEÇİLDİ"
    bilgi = {}
    for st, g in T.groupby("set"):
        bilgi[st] = {"n": int(len(g)), "v5M_VAR": int(g.v5M.sum()), "v6_VAR": int(g.v6.sum()), "v6_VAR_isaret": g[g.v6].isaret.value_counts().to_dict(),
                     "v5M_VAR_isaret": g[g.v5M].isaret.value_counts().to_dict()}
    T.to_csv(_v6_yol("aday_csv", cikti), index=False, float_format="%.5f")
    J = {"surum": V6_SURUM, "etiket": {"EVET": int(len(ev)), "HAYIR": int(len(ha)), "EVET_kaynak": ev.set.value_counts().to_dict(), "HAYIR_kaynak": ha.set.value_counts().to_dict(),
                                       "set3_isaret": T[T.set == "set3"].isaret.value_counts().to_dict()},
         "sablon": {"k": ks, **{a: (None if not np.isfinite(v) else float(v)) for a, v in sab.items()}}, "tablo": tab, "secim": sec, "kapi": kapi,
         "v6_hayir_red": ortak, "v6_evet_gecer": float(ev.v6.mean()) if len(ev) else None, "durum": durum, "bilgi": bilgi, "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_v6_yol("aday", cikti), J, "aday 9")
    return J


def v6_kapi_yukle(cikti: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    J = json.load(open(_v6_yol("aday", cikti), encoding="utf-8"))
    if J["durum"] != "SEÇİLDİ":
        raise V6Hata(f"seçim DUR: v6 HAYIR'ların {J['v6_hayir_red']} kadarını reddediyor (< 0,5)")
    return J["kapi"]


# ================================================================ 4) SENTETİK
_V6_SENT: Dict[str, Any] = {}


def v6_n9_seri(rng, havuz, ohlc, uretec: str, baglam: str, gurultu: float) -> Dict[str, Any]:
    """n9 daralmasız: v3_seri gibi, ama gömmeden önce [p-25, p) barlarında kapanış hareketleri ve mum boyları 3 kat."""
    Sn = MI.MI_ESIK["sentetik"]; p = int(Sn["seri_on"]); N9 = V6_ESIK["sentetik"]["n9"]
    esn = float(rng.uniform(*Sn["esneme"])); olc = float(math.exp(rng.uniform(math.log(Sn["olcek"][0]), math.log(Sn["olcek"][1]))))
    n = p + int(round(20 * Sn["esneme"][1])) + 1 + int(Sn["seri_son"])
    lO, lH, lL, lC = MI.mi_uret(rng, n, havuz, uretec); MI.mi_baglam_uygula(lO, lH, lL, lC, p, baglam)
    a = p - int(N9["bar"]); kat = float(N9["kat"]); taban = lC[a - 1]
    yC = taban + kat * (lC[a:p] - taban); yO = yC + kat * (lO[a:p] - lC[a:p]); yH = yC + kat * (lH[a:p] - lC[a:p]); yL = yC + kat * (lL[a:p] - lC[a:p])
    kay = yC[-1] - lC[p - 1]
    lO[a:p], lH[a:p], lL[a:p], lC[a:p] = yO, yH, yL, yC
    for x in (lO, lH, lL, lC):
        x[p:] += kay
    Le = MI.mi_gom(rng, lO, lH, lL, lC, p, {"ohlc": ohlc}, gurultu, olc, esn)
    return {"O": np.exp(lO), "H": np.exp(lH), "L": np.exp(lL), "C": np.exp(lC), "e": p + Le - 1}


def v6_karsi(rng: Optional[np.random.Generator] = None, n8_kat: Optional[float] = None) -> Dict[str, Dict[str, np.ndarray]]:
    s = MI.mi_sablon_yukle()["tam"]; a = s["ohlc"]; O, H, L, C = (np.asarray(a[x], float) for x in ("O", "H", "L", "C"))
    k = 10; K = MV.mv_karsi_ornek(s); out = {"n1": K["n1"], "n2": K["n2"], "n5": K["p1"]}
    kat = float(n8_kat if n8_kat is not None else V6_ESIK["sentetik"]["n8_kat"][0])
    gmax = float(np.max(np.abs(C - O))); yeni = C[k - 1] + kat * gmax; faz = yeni - C[k]
    O8, H8, L8, C8 = O.copy(), H.copy(), L.copy(), C.copy()
    O8[k] = C[k - 1]; C8[k] = yeni; H8[k] = yeni + (H[k] - max(O[k], C[k])); L8[k] = C[k - 1] - (min(O[k], C[k]) - L[k])
    for x, y in ((O8, O), (H8, H), (L8, L), (C8, C)):
        x[k + 1:] = y[k + 1:] + faz
    out["n8"] = {"O": O8, "H": H8, "L": L8, "C": C8}
    if rng is not None:
        f = rng.uniform(*V6_ESIK["sentetik"]["n10"], size=len(C))
        out["n10"] = {"O": C + f * (O - C), "H": C + f * (H - C), "L": C + f * (L - C), "C": C.copy()}
    return out


def _v6_kendi(tur: str, P: Dict[str, np.ndarray], o: Dict[str, float], kapi: Dict[str, Dict[str, Any]], tab: Dict[str, Any]) -> bool:
    if tur == "n1":
        return not bool(P["ham_B"][0])
    if tur == "n2":
        return not bool(P["ham_M"][0])
    if tur == "n5":
        return not bool(P["ham_T"][0])
    if tur == "n8":
        v = float(P["d_cikis_govde"][0]); return np.isfinite(v) and v >= 1.2
    soz, yedek = ("BB", "BB1") if tur == "n9" else ("D", "D4")
    g = kapi.get(soz) or {"aday": yedek, "esik": tab[yedek]["esik"], "yon": ADAY[yedek][1]}
    return not v6_gec(o, {soz: g})[soz]


def _v6_sent_isci(arg: Tuple[str, int, int, int, int, float]) -> Dict[str, Any]:
    tur, ti, ui, bi, t, gr = arg; Sn = V6_ESIK["sentetik"]; G = _V6_SENT
    rng = np.random.default_rng([int(Sn["kok"]), ti, ui, bi, int(round(gr * 100)), t])
    if tur == "n9":
        X = v6_n9_seri(rng, G["havuz"], G["ohlc"]["poz"], Sn["uretec"][ui], Sn["baglam"][bi], float(gr))
    elif tur == "n8":
        for kat in Sn["n8_kat"]:                                   # sentetik bantta ölçülerek kurulur (aynı tohum)
            rng = np.random.default_rng([int(Sn["kok"]), ti, ui, bi, int(round(gr * 100)), t])
            X = V3.v3_seri(rng, G["havuz"], G["n8"][kat], Sn["uretec"][ui], Sn["baglam"][bi], float(gr))
            e_ = int(X["e"]); m_ = e_ - int(MI.MI_ESIK["sentetik"]["seri_on"]) + 1; BU_, BO_, _ = MI.mi_bant(X["C"])
            P_ = V5.v5_parcalar(*(x[None, e_ - m_ + 1:e_ + 1] for x in (X["O"], X["H"], X["L"], X["C"], BU_, BO_)))
            if np.isfinite(P_["d_cikis_govde"][0]) and P_["d_cikis_govde"][0] >= 1.2:
                break
    else:
        oh = v6_karsi(rng)["n10"] if tur == "n10" else G["ohlc"][tur]
        X = V3.v3_seri(rng, G["havuz"], oh, Sn["uretec"][ui], Sn["baglam"][bi], float(gr))
    e = int(X["e"]); m = e - int(MI.MI_ESIK["sentetik"]["seri_on"]) + 1; tol = int(Sn["tol"])
    R = v6_tara_seri(X["O"], X["H"], X["L"], X["C"], G["kapi"], sonlar=np.arange(e - tol, e + tol + 1))
    BU, BO, BA = MI.mi_bant(X["C"]); s = e - m + 1
    P = V5.v5_parcalar(*(x[None, s:e + 1] for x in (X["O"], X["H"], X["L"], X["C"], BU, BO))); k = int(P["k"][0])
    o = v6_olcu(X["O"], X["H"], X["L"], X["C"], BU, BO, BA, s, e, k) if k > 0 else {a: float("nan") for a in ADAY}
    kendi = None if tur == "poz" else (_v6_kendi(tur, P, o, G["kapi"], G["tab"]) if (k > 0 or tur in ("n1", "n2", "n5")) else True)
    return {"tur": tur, "uretec": Sn["uretec"][ui], "baglam": Sn["baglam"][bi], "gurultu": gr, "VAR": bool(R["VAR"][e - tol:e + tol + 1].any()),
            "v5M": bool(R["v5M"][e - tol:e + tol + 1].any()), "kendi_ihlal": kendi}


def _v6_yanlis_isci(arg: Tuple[int, int]) -> Tuple[int, int]:
    ui, t = arg; Sn = V6_ESIK["sentetik"]; rng = np.random.default_rng([int(Sn["kok"]), 99, ui, t])
    lO, lH, lL, lC = MI.mi_uret(rng, int(Sn["yanlis"]["n"]) + 60, _V6_SENT["havuz"], Sn["uretec"][ui])
    R = v6_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC), _V6_SENT["kapi"])
    return int(len(lC) - 34), int(len(V5.v5_tekil(np.flatnonzero(R["VAR"]), R["S"])))


def v6_sentetik(cikti: Optional[str] = None, islem: int = 4) -> Dict[str, Any]:
    import multiprocessing as mp
    t0 = time.time(); cikti = cikti or V6_YOL["cikti"]; Sn = V6_ESIK["sentetik"]; kapi = v6_kapi_yukle(cikti)
    AJ = json.load(open(_v6_yol("aday", cikti), encoding="utf-8")); a = MI.mi_sablon_yukle()["tam"]; K = v6_karsi()
    ohlc = {"poz": {x: a["ohlc"][x] for x in ("O", "H", "L", "C")}, "n1": K["n1"], "n2": K["n2"], "n5": K["n5"], "n8": K["n8"], "n9": None, "n10": None}
    _V6_SENT.clear(); _V6_SENT.update({"havuz": pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"])), "ohlc": ohlc, "kapi": kapi, "tab": AJ["tablo"],
                                       "n8": {kat: v6_karsi(n8_kat=kat)["n8"] for kat in Sn["n8_kat"]}})
    turler = list(ohlc)
    isler = [(tur, ti, ui, bi, t, gr) for ti, tur in enumerate(turler) for ui in range(len(Sn["uretec"])) for bi in range(len(Sn["baglam"]))
             for gr in Sn["gurultu"] for t in range(int(Sn["tohum"]))]
    try:
        with mp.get_context("fork").Pool(islem) as pool:
            R = list(pool.imap(_v6_sent_isci, isler, chunksize=32))
            Y = list(pool.imap(_v6_yanlis_isci, [(ui, t) for ui in range(len(Sn["uretec"])) for t in range(int(Sn["yanlis"]["seri"]))], chunksize=8))
    finally:
        _V6_SENT.clear()
    D = pd.DataFrame(R); out: Dict[str, Any] = {"surum": V6_SURUM, "kapi": kapi}
    for tur, g in D.groupby("tur", sort=False):
        o = {"VAR": float(g.VAR.mean()), "v5M": float(g.v5M.mean()), "n": int(len(g)), "gurultu": {f"{x:.1f}": float(h.VAR.mean()) for x, h in g.groupby("gurultu")},
             "baglam": {x: float(h.VAR.mean()) for x, h in g.groupby("baglam")}}
        if tur != "poz":
            o["kendi_olcu"] = Sn["kendi_olcu"][tur]; o["kendi_ihlal_payi"] = float(g.kendi_ihlal.astype(float).mean())
            o["gecerli"] = bool(o["kendi_ihlal_payi"] >= Sn["gecerli_pay"])
        out[tur] = o
    T = int(Sn["yanlis"]["seri"]); out["rastgele"] = {}
    for ui, ur in enumerate(Sn["uretec"]):
        nb = int(sum(y[0] for y in Y[ui * T:(ui + 1) * T])); tk = int(sum(y[1] for y in Y[ui * T:(ui + 1) * T]))
        out["rastgele"][ur] = {"n_bar": nb, "tekil": tk, "VAR_1000": 1000.0 * tk / max(nb, 1)}
    es = Sn["esik"]; neg = [t for t in turler if t != "poz"]
    out["olcut"] = {"poz_g10": bool(out["poz"]["gurultu"]["0.1"] >= es["poz"]),
                    "neg": {n: (bool(out[n]["VAR"] <= es["neg"]) if out[n]["gecerli"] else "geçersiz kurgu (sayılmaz)") for n in neg},
                    "rastgele": {k: bool(v["VAR_1000"] <= es["rastgele"]) for k, v in out["rastgele"].items()}}
    out["olcut"]["gecti"] = bool(out["olcut"]["poz_g10"] and all(v is True for v in out["olcut"]["neg"].values() if not isinstance(v, str))
                                 and all(out["olcut"]["rastgele"].values()))
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_v6_yol("sentetik", cikti), out, "sentetik 9")
    return out


# ================================================================ 5) KAPI ve ÖN KAYIT
def v6_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD9_SHA": MI._mi_sha(V6_YOL["kod"]), "ESIK9_SHA": v6_esik_sha(), "ADAY9_SHA": MI._mi_sha(_v6_yol("aday", cikti)),
            "SENTETIK9_SHA": MI._mi_sha(_v6_yol("sentetik", cikti)), "V5_KOD_SHA": MI._mi_sha(V5.V5_YOL["kod"]), "V4_KOD_SHA": MI._mi_sha(V4.V4_YOL["kod"]),
            "V3_KOD_SHA": MI._mi_sha(V3.V3_YOL["kod"]), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]),
            "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"]), "E6_KOD_SHA": MI._mi_sha(os.path.join(KOK_V6, "MUM_IZI_ETIKET2.py")),
            "ISARET8_SHA": MI._mi_sha(V6_YOL["isaret8"])}


def v6_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or V6_YOL["cikti"]; yol = _v6_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise V6Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = v6_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise V6Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_V6); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise V6Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_V6.py", "MUM_IZI_V5.py", "MUM_IZI_V4.py", "MUM_IZI_V3.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py",
                   "MUM_IZI_ETIKET2.py", os.path.relpath(_v6_yol("aday", cikti), KOK_V6), os.path.relpath(_v6_yol("sentetik", cikti), KOK_V6)]):
        raise V6Hata("ön kayıt / kod / aday / sentetik çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def v6_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or V6_YOL["cikti"]; y = _v6_yol("onkayit", cikti)
    if os.path.exists(y):
        raise V6Hata("ön kayıt zaten var")
    sh = v6_sha_simdi(cikti); AJ = json.load(open(_v6_yol("aday", cikti), encoding="utf-8")); SJ = json.load(open(_v6_yol("sentetik", cikti), encoding="utf-8"))
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}; f = V5._v5_f
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in V6_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_V6.py"])
    tb = ["| aday | yön | EVET min-maks | HAYIR medyan | şablon | eşik | reddedilen HAYIR payı |", "|---|---|---|---|---|---|---|"]
    for a, v in AJ["tablo"].items():
        tb.append(f"| {a} | {v['yon']} | {f(v['evet_min'])}..{f(v['evet_max'])} | {f(v['hayir_medyan'])} | {f(v['sablon'])} | "
                  f"{f(v['esik']) if v['gecerli'] else 'aday değil: ' + v['neden']} | {f(v['puan'], 2)} |")
    neg = [t for t in SJ if t.startswith("n") and isinstance(SJ[t], dict) and "kendi_olcu" in SJ[t]]
    s = [f"# MUM_IZI9 ÖN KAYIT ({MI._mi_simdi()})", "",
         "v6 = v5M ∧ K* ∧ D* ∧ BB* (Cemal: 'Mumlar küçük olmalı, dizilim muntazam olmalı, Bollinger daralması net olmalı'). Aday ölçüler ve eşik kuralı iş tanımında; "
         "eşikler etiketlere (iç örnek) oturtuldu. Bu dosya evren taramasından ve PDF'ten ÖNCE commit edilir; sonra kural değişmez.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_V6.py commit'i: {kc or 'yok'}", "",
         f"## Etiket kümesi: {json.dumps(AJ['etiket'], ensure_ascii=False)}", "", "## Aday tablosu", "", *tb, "",
         f"- Seçim: {json.dumps(AJ['secim'], ensure_ascii=False)}", f"- v6 kapıları: {json.dumps(AJ['kapi'], ensure_ascii=False)}",
         f"- v6'nın birlikte reddettiği HAYIR payı: {f(AJ['v6_hayir_red'], 3)}; EVET'lerin geçen payı: {f(AJ['v6_evet_gecer'], 3)}; durum: {AJ['durum']}",
         f"- Bilgi (set bazında v5M / v6 VAR ve Cemal'in yanıtı): {json.dumps(AJ['bilgi'], ensure_ascii=False)}", f"- Şablon ölçüleri: {json.dumps(AJ['sablon'], ensure_ascii=False)}", "",
         "## Sentetik (v6)", "", f"- pozitif VAR: {SJ['poz']['gurultu']} (bağlam {SJ['poz']['baglam']}; v5M {SJ['poz']['v5M']:.3f})",
         *[f"- {n}: kendi ölçüsü {SJ[n]['kendi_olcu']} ihlal payı {100 * SJ[n]['kendi_ihlal_payi']:.1f} % -> {'GEÇERLİ' if SJ[n]['gecerli'] else 'KURGU GEÇERSİZ'}; "
           f"VAR {100 * SJ[n]['VAR']:.1f} %" for n in neg],
         f"- rastgele: {SJ['rastgele']}", f"- KABUL ÖLÇÜTÜ: {'GEÇTİ' if SJ['olcut']['gecti'] else 'GEÇMEDİ'} {json.dumps(SJ['olcut'], ensure_ascii=False)}", "",
         "## Kural ve eşikler (V6_ESIK; sha yukarıda)", "", "```", json.dumps(V6_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 9")


# ================================================================ 6) EVREN TARAMASI ve ONAY SEÇİMİ
_V6_ISCI: Dict[str, Any] = {}


def _v6_isci(s: str) -> Dict[str, Any]:
    import MUM_IZI_ETIKET2 as E6
    G = _V6_ISCI; d = G["V"][s]; z = G["zaman"]; p = G["pazar"]; uc = G["uc"]; ix = d.index
    R = v6_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), G["kapi"], d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None)
    ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1])); e = V5.v5_tekil(np.flatnonzero(R["VAR"] & ara), R["S"])
    if p in ("ABD", "AVR"):
        ev = np.zeros(len(e), bool)
        for (a, b), P in G["P"]:
            j = np.flatnonzero((ix[e] >= pd.Timestamp(a)) & (ix[e] <= pd.Timestamp(b)))
            if len(j):
                ev[j] = E6.e6_p2_maske(P, s, ix[e][j])
    else:
        dv = (d.Close * d.Volume).to_numpy(float)[e]; med = G["med"].reindex(E6._e6_anahtar(ix[e], z)).to_numpy(float); ev = np.isfinite(med) & (dv > med)
    return {"sembol": s, "n_bar": int(ara.sum()), "olay": [{"t": int(t), "tarih": str(ix[t].date()), "m": int(R["m"][t]), "k": int(R["k"][t]), "S": float(R["S"][t]),
                                                            "evren": bool(v), "olcu": R["olcu"][int(t)]} for t, v in zip(e, ev)]}


def v6_tarama(cikti: Optional[str] = None, islem: int = 3) -> Dict[str, Any]:
    import multiprocessing as mp
    import KASA as KS
    import MUM_IZI_ETIKET2 as E6
    t0 = time.time(); cikti = cikti or V6_YOL["cikti"]
    if os.path.exists(_v6_yol("tarama", cikti)):
        raise V6Hata("tarama zaten var")
    G0 = v6_kapi(cikti); kapi = v6_kapi_yukle(cikti)
    yol = [os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + \
          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")]
    kasa = KS.kasa_kapisi(yol, "2022-12-31"); olay: List[Dict[str, Any]] = []; say: Dict[str, Any] = {}
    J8 = json.load(open(os.path.join(V6_YOL["cikti"], "mum_izi8_tarama.json"), encoding="utf-8"))["sayim"][V5M]
    for z in ("gunluk", "haftalik"):
        uc = V6_ESIK["tarama"][z]
        for p in ("ABD", "AVR", "BIST"):
            V = MV.mv_veri(z, p); Ps = []; med = None
            if p in ("ABD", "AVR"):
                Ps = [(ara, E6.e6_p2_hazirla(p, kl)) for ara, kl in E6.e6_parcalar(z, p)]
            else:
                med = E6.e6_bist_medyan(V, z)
            _V6_ISCI.clear(); _V6_ISCI.update({"V": V, "zaman": z, "pazar": p, "P": Ps, "med": med, "uc": uc, "kapi": kapi})
            try:
                with mp.get_context("fork").Pool(islem) as pool:
                    R = list(pool.imap(_v6_isci, sorted(V), chunksize=16))
            finally:
                _V6_ISCI.clear()
            ol = [dict(o, sembol=r["sembol"], zaman=z, pazar=p) for r in R for o in r["olay"]]; olay += ol
            nb = int(sum(r["n_bar"] for r in R)); yil = nb / (252.0 if z == "gunluk" else 52.0); ne = int(sum(o["evren"] for o in ol)); v8 = J8[f"{z}|{p}"]
            say[f"{z}|{p}"] = {"hisse": len(R), "hisse_yil": round(yil, 1), "olay": len(ol), "olay_evren": ne, "v5M_olay": v8["olay"], "v5M_olay_evren": v8["olay_evren"],
                               "v5M_orani": (len(ol) / v8["olay"]) if v8["olay"] else None, "v5M_orani_evren": (ne / v8["olay_evren"]) if v8["olay_evren"] else None,
                               "evren_hisse_yil_basina": (ne / yil) if yil else None}
            del V, Ps, med; gc.collect()
            v6log.info("%s %s: %s (%.0f sn)", z, p, say[f"{z}|{p}"], time.time() - t0)
    if olay and max(pd.Timestamp(o["tarih"]) for o in olay) > MI.MI_KESIK:
        raise V6Hata("KESİK AŞIMI")
    haric = set()
    for k_ in ("anahtar4", "anahtar6", "anahtar8"):
        haric |= {r["sembol"] for r in json.load(open(V6_YOL[k_], encoding="utf-8"))["sayfalar"]}
    sec = v6_onay_secim(olay, haric)
    os.makedirs(V6_YOL["gecici"], exist_ok=True); hp = os.path.join(V6_YOL["gecici"], "tarama_ham.json")
    MI._mi_jyaz(hp, {"olay": olay, "secim": sec}, "tarama ham 9")
    J = {"surum": V6_SURUM, "kapi_secim": kapi, "kapi": G0, "kasa": kasa, "sayim": say, "ham_sha": MI._mi_sha(hp), "n_secim": len(sec),
         "secim_sayim": {"zaman": pd.Series([r["zaman"] for r in sec], dtype=object).value_counts().to_dict(),
                         "pazar": pd.Series([r["pazar"] for r in sec], dtype=object).value_counts().to_dict()},
         "uygun_olay": {z: int(sum(1 for o in olay if o["zaman"] == z and o["evren"] and o["sembol"] not in haric)) for z in ("gunluk", "haftalik")},
         "onay_durum": "DUR (v6 uygun bölge < 8)" if len(sec) < V6_ESIK["onay"]["en_az"] else "HAZIR", "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_v6_yol("tarama", cikti), J, "tarama 9")
    return J


def v6_onay_secim(olay: List[Dict[str, Any]], haric: set) -> List[Dict[str, Any]]:
    G = V6_ESIK["onay"]; rng = np.random.default_rng(G["tohum"]); sec: List[Dict[str, Any]] = []; gor = set(haric)
    for z in ("haftalik", "gunluk"):
        h = sorted([o for o in olay if o["zaman"] == z and o["evren"]], key=lambda o: (o["sembol"], o["tarih"])); n = 0; bist = 0
        for i in rng.permutation(len(h)):
            o = h[int(i)]
            if o["sembol"] in gor or (o["pazar"] == "BIST" and bist >= G["bist_tavan"]):
                continue
            sec.append(o); gor.add(o["sembol"]); n += 1; bist += int(o["pazar"] == "BIST")
            if n >= G[z]:
                break
    p = rng.permutation(len(sec))
    return [dict(sec[i], sayfa=j + 3) for j, i in enumerate(p)]


# ================================================================ 7) ONAY PDF
_V6_AD = {"K1": "en büyük gövde", "K2": "mum boyu / bant", "K3": "mum boyu / önceki 60 bar", "K4": "çıkış mumu gövdesi", "D1": "en büyük kapanış adımı",
          "D2": "mum örtüşmesi", "D3": "tırmanış doğrusallığı", "D4": "mum boyu değişkenliği", "BB1": "en dar bant / ilk 3 mum", "BB2": "en dar / en geniş bant",
          "BB3": "daralma yüzdeliği (120 bar)", "BB4": "en dar nokta bölgenin ortasında"}
_V6_SOZ = {"K": "küçük mum", "D": "dizilim", "BB": "daralma"}


def _v6_uc_sayi(o: Dict[str, float], kapi: Dict[str, Dict[str, Any]]) -> str:
    p = []
    for soz in ("K", "D", "BB"):
        g = kapi.get(soz)
        if not g:
            p.append(f"{_V6_SOZ[soz]}: kapı yok"); continue
        v = o.get(g["aday"]); isr = "<=" if g["yon"] == "kucuk" else ">="
        p.append(f"{_V6_SOZ[soz]}: {_V6_AD[g['aday']]} {v:.2f} ({isr} {g['esik']:.2f})" if g["yon"] != "ikili" else f"{_V6_SOZ[soz]}: {_V6_AD[g['aday']]} "
                 f"{'evet' if v >= 0.5 else 'hayır'}")
    return V5._v5_virgul("\n".join(p))


def v6_onay(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or V6_YOL["cikti"]; y = _v6_yol("onay", cikti); ya = _v6_yol("anahtar", cikti)
    if os.path.exists(y) or os.path.exists(ya):
        raise V6Hata("PDF / anahtar zaten var")
    JT = json.load(open(_v6_yol("tarama", cikti), encoding="utf-8")); hp = os.path.join(V6_YOL["gecici"], "tarama_ham.json")
    if MI._mi_sha(hp) != JT["ham_sha"]:
        raise V6Hata("tarama ham dosyası değişmiş")
    if JT["onay_durum"] != "HAZIR":
        raise V6Hata(f"onay seti: {JT['onay_durum']}")
    sec = json.load(open(hp, encoding="utf-8"))["secim"]; kapi = JT["kapi_secim"]
    AJ = json.load(open(_v6_yol("aday", cikti), encoding="utf-8")); SJ = json.load(open(_v6_yol("sentetik", cikti), encoding="utf-8"))
    a = MV.mv_sablon()["tam"]["ohlc"]; A5 = json.load(open(os.path.join(V6_YOL["cikti"], "mum_izi8_aday.json"), encoding="utf-8")); sb5 = A5["sablon"]
    once = int(MV.MV_ESIK["onay"]["once"]); Vc: Dict[Any, Any] = {}; nz = {z: sum(1 for r in sec if r["zaman"] == z) for z in ("gunluk", "haftalik")}
    T9 = pd.read_csv(_v6_yol("aday_csv", cikti)); h3 = T9[(T9.set == "set3") & (T9.isaret == "HAYIR")]; e3 = T9[(T9.set == "set3") & (T9.isaret == "EVET")]
    sb = AJ["sablon"]
    with PdfPages(y, metadata={"Title": "MUM_IZI9 onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "KOD NASIL TESPİT EDİYOR (v6)", fontsize=17, weight="bold")
        sat = ["Eski kural aynen: mavi gel-git, yeşil okla SMA'yı aşan mum, turuncu düzenli tırmanış, bandın içinden; küçük gövde, az alt fitil, uzun üst fitil."]
        for soz, cum in (("K", "Mumlar küçük"), ("D", "Dizilim muntazam"), ("BB", "Bollinger daralması net")):
            g = kapi.get(soz)
            sat.append(f"{cum}: " + (f"{_V6_AD[g['aday']]} {'<=' if g['yon'] == 'kucuk' else '>='} {g['esik']:.2f}" if g and g["yon"] != "ikili"
                                     else (f"{_V6_AD[g['aday']]}" if g else "ölçü senin işaretlerini ayırmadı, kapı konmadı")))
        sat.append(f"Senin işaretlerinle: v5M'nin {len(h3)} 'benzemiyor' sayfasından {int((~h3.v6.astype(bool)).sum())}'ini artık eliyor; 'benziyor' dediğin "
                   f"{len(e3)} sayfanın {int(e3.v6.astype(bool).sum())}'i kalıyor.")
        if not SJ["olcut"]["gecti"]:
            sat.append("Uyarı: kodun sentetik sınavı ölçütü GEÇMEDİ.")
        fig.text(0.06, 0.89, V5._v5_virgul("\n\n".join(sat)), fontsize=12, va="top", wrap=True)
        fig.text(0.06, 0.16, f"Sonraki sayfa: senin kalıbında kodun okuması. Sonra {len(sec)} rastgele bölge (haftalık {nz['haftalik']}, günlük {nz['gunluk']}).\n"
                 "Benziyorsa ✓, benzemiyorsa × kutusuna X koy; yanlış okunan parçayı daire içine al.\n"
                 f"{len(sec)} sayfanın en az %80'i ✓ ise tespit geçerli sayılır.", fontsize=11, va="top", wrap=True)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.08, 0.38, 0.86, 0.52])
        MV._mv_ciz(ax, a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın: kodun okuması")
        V5._v5_okuma_ciz(ax, 0, int(sb5["k"]), len(a["C"]), np.asarray(a["L"], float), np.asarray(a["H"], float))
        ms = (f"mum yapısı: gövde {sb5['d_m1']:.2f} · alt fitil {sb5['d_m2']:.2f} · üst fitil {sb5['d_m3']:.2f} · üst / alt {sb5['d_m4']:.1f}")
        def _sb(g):
            v = sb.get(g["aday"])
            if v is None:
                return "(şablonda ölçülemez)"
            if g["yon"] == "ikili":
                return "evet" if v >= 0.5 else "hayır"
            return f"{v:.2f} ({'<=' if g['yon'] == 'kucuk' else '>='} {g['esik']:.2f})"
        uc = "\n".join(f"{_V6_SOZ[soz]}: {_V6_AD[g['aday']]} " + _sb(g) for soz, g in kapi.items())
        fig.text(0.08, 0.33, V5._v5_virgul(ms + "\n" + uc), fontsize=11, va="top")
        fig.text(0.08, 0.95, "Mavi = gel-git kısmı, yeşil ok = SMA'yı aşan mum, turuncu = tırmanış kısmı", fontsize=12, weight="bold")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["sayfa"]):
            kk = (r["zaman"], r["pazar"])
            if kk not in Vc:
                Vc[kk] = MV.mv_veri(*kk)
            d = Vc[kk][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); i0 = max(0, t - m + 1 - once)
            Ofull, Hfull, Lfull, Cfull = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); BU, BO, BA = MI.mi_bant(Cfull); sl = slice(i0, t + 1)
            P = V5.v5_parcalar(*(x[None, t - m + 1:t + 1] for x in (Ofull, Hfull, Lfull, Cfull, BU, BO)))
            o = v6_olcu(Ofull, Hfull, Lfull, Cfull, BU, BO, BA, t - m + 1, t, int(r["k"]))
            if int(P["k"][0]) != int(r["k"]) or not bool(V5.v5_kural(P, V5M)[0]) or not all(v6_gec(o, kapi).values()):
                raise V6Hata(f"sayfa {r['sayfa']}: okuma tarama ile uyuşmuyor")
            fig = plt.figure(figsize=(8.3, 11.7))
            MV._mv_ciz(fig.add_axes([0.04, 0.66, 0.26, 0.22]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
            ax = fig.add_axes([0.34, 0.44, 0.63, 0.48]); L_, H_ = Lfull[sl], Hfull[sl]
            MV._mv_ciz(ax, Ofull[sl], H_, L_, Cfull[sl], BU[sl], BO[sl], BA[sl], None, f"Sayfa {r['sayfa']}: kodun okuması ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            V5._v5_okuma_ciz(ax, t - m + 1 - i0, int(r["k"]), m, L_, H_)
            fig.text(0.34, 0.425, V5._v5_m_metin(P), fontsize=9.5)
            fig.text(0.34, 0.415, _v6_uc_sayi(o, kapi), fontsize=9.5, va="top")
            fig.text(0.04, 0.6, "Mavi = gel-git\nYeşil ok = SMA'yı\naşan mum\nTuruncu = tırmanış\nMor = Bollinger 20\nve SMA20 (kesik)\nSağ kenar = bölge sonu\n(sonrası yok)",
                     fontsize=9.5, va="top")
            ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.22]); ax2.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
                ax2.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax2.transAxes))
                ax2.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax2.transAxes)
            fig.text(0.1, 0.34, "Yanlış okunan parçayı daire içine al.", fontsize=12)
            pdf.savefig(fig); plt.close(fig)
    MI._mi_jyaz(ya, {"not": "MÜHÜRLÜ: sayfa -> hisse / tarih / m / k / v1 S / ölçüler; PDF'e girmez", "kapi": kapi, "sayfalar": sec}, "anahtar 9")
    J = {"surum": V6_SURUM, "kapi": kapi, "aday": AJ, "sentetik": SJ, "tarama": {k: JT[k] for k in ("sayim", "n_secim", "secim_sayim", "uygun_olay", "kasa")},
         "pdf_sha": MI._mi_sha(y), "anahtar_sha": MI._mi_sha(ya)}
    MI._mi_jyaz(_v6_yol("sonuc", cikti), J, "sonuç 9")
    return y


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_v6(_once=_CK_ONCE_V6, _dosya="MUM_IZI_V6.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_V6",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_v6()


def _v6_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_V6")
    ap.add_argument("komut", choices=["aday", "sentetik", "onkayit", "tarama", "onay"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "aday":
            J = v6_aday(); print(json.dumps(MI._mi_json({k: J[k] for k in ("etiket", "secim", "kapi", "v6_hayir_red", "durum")}), ensure_ascii=False))
        elif a.komut == "sentetik":
            J = v6_sentetik(); print(json.dumps(MI._mi_json(J["olcut"]), ensure_ascii=False))
        elif a.komut == "onkayit":
            print(v6_onkayit_yaz())
        elif a.komut == "tarama":
            J = v6_tarama(); print(json.dumps(MI._mi_json(J["sayim"]), ensure_ascii=False))
        elif a.komut == "onay":
            print(v6_onay())
    except V6Hata as ex:
        v6log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_v6_ana())
