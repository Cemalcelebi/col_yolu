"""MUM_IZI_V5 — MUM_IZI EK 8: etiketlerden seçilen evre kuralı (v5) + 'kod nasıl tespit ediyor' onay PDF'i (26 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI8_IS_TANIMI.md (commit a67a77a; ana model). Cemal (26 Kas): "Yeni bir PDF gönder, nasıl tespit ediyor;
düzelmesi gerekir artık." Bu iş ETİKETLERİ KULLANIR (61 karar: set 1 + set 2; eşleme mum_izi7_sinama.csv). Parçalar sabit tanımlı (Y, G1, G2, T, I, B, F, S);
yalnız 8 aday kural (R1-R8); seçim kuralı önceden yazılı. Seçim iç örnektir (ezber riski); gerçek sınama Cemal'in yeni PDF'teki işaretleri.
GETİRİ / SONRASI YOK. Eski kodlar değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz. Ön kayıttan (MUM_IZI8_ON_KAYIT.md) sonra kural değişmez.

Komut:  python MUM_IZI_V5.py aday       61 etikette aday tablosu + seçim (mum_izi8_aday.json, mum_izi8_aday.csv)
        python MUM_IZI_V5.py sentetik   seçilen kural: pozitif + kendi ölçüsünde doğrulanmış negatifler + rastgele (mum_izi8_sentetik.json)
        python MUM_IZI_V5.py onkayit    MUM_IZI8_ON_KAYIT.md
        python MUM_IZI_V5.py tarama     kapı -> evren taraması, sayım, onay seçimi (mum_izi8_tarama.json)
        python MUM_IZI_V5.py onay       MUM_IZI8_ONAY.pdf + mum_izi8_onay_anahtar.json + mum_izi8_sonuc.json
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_V5 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import rankdata as _rank5  # noqa: E402

KOK_V5 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_V5 not in sys.path:
    sys.path.insert(0, KOK_V5)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V3 as V3  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V4 as V4  # noqa: E402  (DEĞİŞTİRİLMEZ)

v5log = logging.getLogger("col.mum_izi_v5")
if not v5log.handlers:
    _v5_h = logging.StreamHandler(sys.stderr)
    _v5_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_v5: %(message)s", "%H:%M:%S"))
    v5log.addHandler(_v5_h)
    v5log.setLevel(logging.INFO)
    v5log.propagate = False


class V5Hata(RuntimeError):
    """Durdurucu hata: seçim / kapı / mühür / veri / kesik."""


V5_SURUM = "MUM_IZI_V5 v1.0 (2026-11-26): etiketlerle seçilen evre kuralı (R1-R8 adayları), kodun okuması PDF'te"
V5_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_V5, "MUM_IZI_V5.py"), "gecici": "/tmp/mum_izi/v5",
          "etiket": os.path.join(MI.MI_YOL["cikti"], "mum_izi7_sinama.csv"), "anahtar1": os.path.join(MI.MI_YOL["cikti"], "mum_izi4_onay_anahtar.json"),
          "anahtar2": os.path.join(MI.MI_YOL["cikti"], "mum_izi6_anahtar.json"), "olcum6": os.path.join(MI.MI_YOL["cikti"], "mum_izi6_olcum.json")}
V5_DOSYA = {"onkayit": "MUM_IZI8_ON_KAYIT.md", "rapor": "MUM_IZI8_RAPOR.md", "sonuc": "mum_izi8_sonuc.json", "aday": "mum_izi8_aday.json",
            "aday_csv": "mum_izi8_aday.csv", "sentetik": "mum_izi8_sentetik.json", "sentetik_m": "mum_izi8_sentetik_v5m.json", "tarama": "mum_izi8_tarama.json", "onay": "MUM_IZI8_ONAY.pdf",
            "anahtar": "mum_izi8_onay_anahtar.json"}
PARCA = ["Y", "G1", "G2", "T", "I", "B", "F", "S", "M"]
DUZ_PARCA = ["Y", "G1", "G2", "T", "I", "B", "F", "M"]
KURAL: Dict[str, List[str]] = {"R1": ["Y", "G1", "G2"], "R2": ["Y", "G1", "G2", "S"], "R3": ["Y", "G1", "G2", "T"], "R4": ["Y", "G1", "G2", "T", "I"],
                               "R5": ["Y", "G1", "G2", "T", "B"], "R6": ["Y", "G1", "G2", "T", "I", "B"], "R7": ["Y", "G1", "G2", "T", "I", "B", "F"],
                               "R8": ["Y", "G1", "G2", "T", "I", "B", "S"]}

V5_ESIK: Dict[str, Any] = {
    "surum": "V5-1.0",
    "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20); Bollinger (20, 2), her mum kendi gününe kadarki barlarla; üst bant <= SMA olan pencere geçersiz",
    "uzunluklar": list(range(16, 25)),
    "parca": {"Y": "k = pencerede ilk SMA üstü kapanış (0'dan); 3 <= k <= floor(0,6 x m) ve çıkıştan sonra (k+1..m-1) en az 5 mum",
              "G1": "v4 E1 aynen: ön kısım (0..k-1) bC ortalaması <= -0,3 ve fiyat kapanış yönü (ön kısım içindeki çiftler) en az 2 kez değişiyor",
              "G2": "v4 E2 aynen: çıkış mumu yeşil (C > O), önceki kapanış bC < 0, çıkıştan sonraki kapanışların >= %80'i bC > 0",
              "T": "çıkıştan sonraki FİYAT kapanışlarının sıra numarasıyla Spearman korelasyonu (eşitlerde ortalama sıra) >= 0,5 ve pencerenin son kapanışı bC >= 0,6",
              "I": "çıkıştan sonraki kapanışların >= %60'ı bC <= 1,05",
              "B": "çıkıştan sonraki gövdelerin (|bC - bO|, bant yarı genişliği birimi) en büyüğü <= 0,9 ve medyanı <= 0,30",
              "F": "çıkıştan sonraki mumlarda üst fitili alt fitilinden uzun olanların payı >= %50",
              "S": "v1 benzerlik puanı (MI.mi_S_pencere, tam şablon, kalibre) >= 0,59",
              "M": "MUM YAPISI (Cemal 26 Kas, sözle kondu, etiketle seçilmedi; bölgenin BÜTÜN mumları): m1 ortalama gövde / mum boyu <= 0,45; m2 ortalama alt "
                   "fitil / mum boyu <= 0,25; m3 ortalama üst fitil / mum boyu >= 0,33; m4 toplam üst fitil / toplam alt fitil >= 1,5 (alt fitil toplamı 0 ise "
                   "sonsuz); M = dördü birden"},
    "esik": {"k_ust": 0.6, "en_az_sonra": 5, "G1_ort": -0.3, "G1_degisim": 2, "G2_ust": 0.80, "T_spearman": 0.5, "T_son": 0.6, "I_pay": 0.60, "I_ust": 1.05,
             "B_max": 0.9, "B_med": 0.30, "F_pay": 0.50, "S": 0.59, "m1": 0.45, "m2": 0.25, "m3": 0.33, "m4": 1.5},
    "kural": {k: " ∧ ".join(v) for k, v in KURAL.items()},
    "nihai": "v5M = seçilen aday kural ∧ M (Cemal'in kesin şartı; sözle kondu, etiketle seçilmedi); 61 etikette hem seçilen kural hem v5M raporlanır; "
             "EVET / HAYIR sayfalarında M ve m1-m4 geçme payları",
    "pencere_sonu": "bir son, uzunluklardan biri VAR ise VAR",
    "etiket": "61 karar etiketi (mum_izi7_sinama.csv: set, sayfa, zaman, cemal); pencere anahtarlardan (set 1 mum_izi4_onay_anahtar.json, set 2 mum_izi6_anahtar.json); "
              "sayfanın kendi penceresi (aynı m, aynı son)",
    "aday": {"olcu": "VAR, 2x2, isabet (VAR içinde EVET), yakalama (EVET içinde VAR), kappa + bootstrap %95 (sayfalar yerine koyarak, B 5000, tohum 25112081); "
                     "set 1 / set 2 ayrı", "B": 5000, "tohum": 25112081},
    "secim": {"kural": "61 etikette VAR >= 8 olan adaylar içinde en yüksek kappa; kappası en yüksekten 0,03'ten az geride olanlar arasında en az parçalı (eşit "
                       "parçada yüksek kappa); seçilenin kappası <= 0,20 ise (ya da uygun aday yoksa) DUR, PDF yok",
              "var_en_az": 8, "fark": 0.03, "kappa_en_az": 0.20,
              "capraz": "bilgi: aynı kural tek sette (VAR en az = tavan(8 x n_set / 61)) seçilir, öteki sette kappası yazılır"},
    "sentetik": {"kok": 25112082, "tohum": 200, "gurultu": [0.0, 0.1, 0.2], "baglam": ["dip", "yatay"], "uretec": ["blok", "ry"], "tol": 3,
                 "negatif": {"n1": "fitilsiz büyük gövde (MV n1)", "n2": "fitiller ters (MV n2; yalnız v5M sentetiğinde)", "n3": "mumlar 2 kat (MV n3)", "n5": "aynı mumlar yatay yol (MV p1)",
                             "n6": "V dönüş (MUM_IZI_V4.v4_karsi n6: tek yönlü iniş, gel-git yok)", "n7": "üst bandın dışından büyük mumlarla (V4 n7)",
                             "n8a": "kırmızı boşluklu çıkış (V4 n8a)", "n8b": "tek dev mumla çıkış (V4 n8b)"},
                 "kendi_olcu": {"n1": "B", "n2": "M", "n3": "B", "n5": "T", "n6": "G1", "n7": "I", "n8a": "G2", "n8b": "çıkış mumu gövdesi > 0,9 (b)"},
                 "dogrulama": "her negatifte gömülü pencerenin kendisinde (son = gerçek son, m = gömülü uzunluk; sentetik bantla) hedef koşul pencerenin kendi "
                              "k'sıyla (Y sınırları aranmadan) hesaplanır; k yoksa ihlal sayılır; tohumların >= %80'inde ihlal varsa negatif GEÇERLİ, yoksa "
                              "'negatif kurgusu geçersiz' (sayılmaz)", "gecerli_pay": 0.80,
                 "yanlis": {"seri": 200, "n": 1000},
                 "kabul_olcutu": "%10 gürültüde pozitif VAR (gerçek sonun +-3 barında, 16-24 uzunluk) >= %50 (iki bağlam x iki üretici); geçerli her negatifte VAR "
                                 "<= %10 (bütün gürültüler); rastgele seride tekil VAR <= 1 / 1.000 bar (iki üretici ayrı). Geçmezse yazılır, kural değişmez; "
                                 "PDF kapağında 'sentetik ölçütü geçmedi' yazar",
                 "esik": {"poz": 0.50, "neg": 0.10, "rastgele": 1.0}},
    "tarama": {"gunluk": ["2016-01-01", "2022-12-31"], "haftalik": ["2001-01-01", "2022-12-31"],
               "evren": "ABD / AVR P2 (MUM_IZI_ETIKET2.e6_p2_maske; günlük açık kopya, haftalık 2001-15 p1 / 2016-22 açık kopya), BIST işlem değeri aynı gün / "
                        "ISO haftası kesit medyanı üstü (olay sonu barında); geçerli bar; haftalıkta eksik haftalı pencere yok",
               "tekil": "aynı hissede VAR sonları < 15 mum zinciri = bir olay; olay = kümenin en yüksek v1 S'li hizası (uzunluklar içinde en yüksek S)",
               "sayim": "tekil v5 VAR olay sayısı pazar x zaman dilimi (evren içi ve hepsi); hisse-yıl başına sıklık = olay / (bar / 252 günlük, / 52 haftalık)"},
    "onay": {"tohum": 25112083, "gunluk": 12, "haftalik": 12, "bist_tavan": 4, "kural": "YALNIZ v5M VAR bölgeleri; bir dilimde 12'den az uygun olay varsa "
                                                                                     "hepsi (sayı yazılır); toplam < 8 ise DUR (PDF yok)", "en_az": 8,
             "secim": "evren içi tekil v5 VAR olaylarından RASTGELE (S'ye göre değil); hisse başına bir; önceki iki setin hisseleri hariç; BIST dilim başına <= 4; "
                      "önce haftalık sonra günlük; sayfa sırası tohumla karışık",
             "sayfa": "s1 KOD NASIL TESPİT EDİYOR (<= 8 satır, Cemal'in cümlesiyle + 61 işaretle uyum + tekrar uyumu); s2 Cemal'in kalıbı üstünde kodun okuması "
                      "(mavi gel-git şeridi, yeşil ok çıkış mumu, turuncu tırmanış şeridi; parça sayıları); s3-26 bölgeler: solda küçük 'Senin kalıbın', sağda bölge "
                      "(öncesi 15 mum, Bollinger 20 + SMA20, bölge sonunda kesik) ve üstünde kodun okuması (aynı renkler, yarı saydam, mumların arkasında); altta "
                      "✓ / × kutuları ve 'yanlış okunan parçayı daire içine al'; hisse / tarih / sonrası yok",
             "esik": "24'ün >= 19'u ✓ -> tespit GEÇERLİ"},
}

V5_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "aday tablosunda kappa bootstrap; negatifler sentetikte kendi ölçüsünde doğrulanıp sayılır; rastgele seri tabanı; getiri / eş yok"),
    "K2": ("EVET", "b her mumun kendi gününe kadarki bantla; v5_tara_seri sonu t olan pencerede <= t barları (test); veri <= 2022-12-31 + KASA kapısı (tarama)"),
    "K3": ("EVET", "MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır; BIST işlem değeri kesit medyanı üstü; ABD / AVR P2"),
    "K4": ("EVET", "tekil < 15 mum zincir, en yüksek v1 S; etiketlerde tekrar sayfaları zaten dışarıda (mum_izi7_sinama.csv)"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok"),
    "K6": ("EVET", "b birimi ölçek bağımsız; gövde sınırı bant yarı genişliğine göre"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; yalnız sayım ve görsel onay"),
    "K8": ("EVET", "61 etiket iç örnek (ezber riski raporda); çapraz set bilgisi; gerçek sınama yeni PDF işaretleri"),
    "K9": ("EVET", "MUM_IZI8_ON_KAYIT.md: KOD8, ESIK8, ADAY8, SENTETIK8 sha + eski kod sha'ları; v5_kapi (kontrol + sha + git) tarama öncesi"),
    "K10": ("EVET", "etiket eşlemesi mum_izi7_sinama.csv'den, sayı denetimi (61; 16 EVET); pencereler anahtarlardan; set 1'de v1 S anahtardaki S ile aynı"),
    "K11": ("EVET", "v5_duz: tek pencerede parçalar düz döngüyle; 61 sayfada vektörlü sonuçla aynı (fark -> DUR)"),
    "K12": ("EVET", "seçim yalnız önceden yazılı kuralla; 'iz' sözü yok; iç örnek uyarısı"),
    "K13": ("EVET", "çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _v5_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or V5_YOL["cikti"], V5_DOSYA[ad])


def v5_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or V5_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


_V5_SAB: Dict[str, Any] = {}


def _v5_sab() -> Dict[str, Any]:
    if not _V5_SAB:
        _V5_SAB["tam"] = MI.mi_sablon_yukle()["tam"]
    return _V5_SAB["tam"]


# ================================================================ 1) PARÇALAR (vektörlü)
_DEG = ["G1_ort", "G1_degisim", "G2_yesil", "G2_onceki", "G2_ust", "T_spearman", "T_son", "I_pay", "B_max", "B_med", "F_pay", "cikis_govde",
        "m1", "m2", "m3", "m4"]


def v5_liste(ad: str) -> List[str]:
    """Kural adı -> parça listesi: 'R1'..'R8' ya da '<aday>+M' (nihai v5M)."""
    if ad.endswith("+M"):
        return KURAL[ad[:-2]] + ["M"]
    return KURAL[ad]


def v5_parcalar(O, H, L, C, BU, BO, BA=None, S: bool = False, maske: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """(N, m) pencereler -> parça bayrakları (Y sınırlarıyla), ham değerler (pencerenin kendi k'sıyla; k >= 1 ve sonra >= 2 mum), k.
    S True ise v1 S yalnız 'maske' (verilmezse hepsi) pencerelerinde hesaplanır (öteki NaN)."""
    O, H, L, C, BU, BO = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BO)]
    N, m = C.shape; E = V5_ESIK["esik"]
    d = BU - BO; gec = (d > 0).all(1) & np.isfinite(d).all(1) & np.isfinite(C).all(1); dd = np.where(d > 0, d, 1.0)
    bO, bC = (O - BO) / dd, (C - BO) / dd
    pos = bC > 0; var_ = pos.any(1); k = np.where(var_, np.argmax(pos, 1), -1)
    Y = gec & var_ & (k >= 3) & (k <= math.floor(E["k_ust"] * m + 1e-9)) & (m - 1 - k >= E["en_az_sonra"])
    hesap = gec & var_ & (k >= 1) & (m - 1 - k >= 2)
    D = {a: np.full(N, np.nan) for a in _DEG}
    uw = H - np.maximum(O, C); lw = np.minimum(O, C) - L; rg = np.maximum(H - L, 1e-12)
    D["m1"] = np.where(gec, (np.abs(C - O) / rg).mean(1), np.nan); D["m2"] = np.where(gec, (lw / rg).mean(1), np.nan)
    D["m3"] = np.where(gec, (uw / rg).mean(1), np.nan); su = uw.sum(1); sl_ = lw.sum(1)
    D["m4"] = np.where(gec, np.where(sl_ > 0, su / np.where(sl_ > 0, sl_, 1.0), np.inf), np.nan)
    for kk in np.unique(k[hesap]):
        i = np.flatnonzero(hesap & (k == kk)); kk = int(kk)
        Ci, bCi, bOi = C[i], bC[i], bO[i]
        D["G1_ort"][i] = bCi[:, :kk].mean(1)
        yon = np.sign(np.diff(Ci[:, :kk], axis=1)); D["G1_degisim"][i] = (yon[:, 1:] * yon[:, :-1] < 0).sum(1) if kk >= 3 else 0
        D["G2_yesil"][i] = bCi[:, kk] - bOi[:, kk]; D["G2_onceki"][i] = bCi[:, kk - 1]; D["cikis_govde"][i] = np.abs(bCi[:, kk] - bOi[:, kk])
        po = slice(kk + 1, m); D["G2_ust"][i] = (bCi[:, po] > 0).mean(1)
        y = Ci[:, po]; r = _rank5(y, axis=1); x = np.arange(y.shape[1], dtype=float)
        rc = r - r.mean(1, keepdims=True); xc = x - x.mean(); den = np.sqrt((rc ** 2).sum(1) * (xc ** 2).sum())
        D["T_spearman"][i] = np.where(den > 0, (rc * xc).sum(1) / np.where(den > 0, den, 1.0), 0.0); D["T_son"][i] = bCi[:, m - 1]
        D["I_pay"][i] = (bCi[:, po] <= E["I_ust"]).mean(1)
        gv = np.abs(bCi[:, po] - bOi[:, po]); D["B_max"][i] = gv.max(1); D["B_med"][i] = np.median(gv, 1)
        D["F_pay"][i] = (uw[i][:, po] > lw[i][:, po]).mean(1)
    ham = {"G1": (D["G1_ort"] <= E["G1_ort"]) & (D["G1_degisim"] >= E["G1_degisim"]),
           "G2": (D["G2_yesil"] > 0) & (D["G2_onceki"] < 0) & (D["G2_ust"] >= E["G2_ust"]),
           "T": (D["T_spearman"] >= E["T_spearman"]) & (D["T_son"] >= E["T_son"]), "I": D["I_pay"] >= E["I_pay"],
           "B": (D["B_max"] <= E["B_max"]) & (D["B_med"] <= E["B_med"]), "F": D["F_pay"] >= E["F_pay"]}
    mm = {"m1": D["m1"] <= E["m1"], "m2": D["m2"] <= E["m2"], "m3": D["m3"] >= E["m3"], "m4": D["m4"] >= E["m4"]}
    ham["M"] = gec & mm["m1"] & mm["m2"] & mm["m3"] & mm["m4"]
    out: Dict[str, np.ndarray] = {"k": k, "gecerli": gec, "Y": Y, **{f"ham_{a}": v for a, v in ham.items()}, **{f"d_{a}": v for a, v in D.items()},
                                  **{f"g_{a}": v & gec for a, v in mm.items()}}
    for a, v in ham.items():
        out[a] = v & Y if a != "M" else v
    Sv = np.full(N, np.nan)
    if S:
        mk = np.ones(N, bool) if maske is None else np.asarray(maske, bool)
        if mk.any():
            BA_ = np.atleast_2d(np.asarray(BA, float))
            Sv[mk] = MI.mi_S_pencere(O[mk], H[mk], L[mk], C[mk], BU[mk], BO[mk], BA_[mk], _v5_sab())
    out["d_S"] = Sv; out["S"] = np.nan_to_num(Sv, nan=-1.0) >= E["S"]
    return out


def v5_kural(P: Dict[str, np.ndarray], ad: str) -> np.ndarray:
    return np.all(np.stack([P[p] for p in v5_liste(ad)]), 0)


def v5_duz(W: Dict[str, np.ndarray]) -> Dict[str, Any]:
    """K11: tek pencerede parçalar düz döngüyle (S hariç)."""
    O, H, L, C, BU, BO = (list(map(float, W[x])) for x in ("O", "H", "L", "C", "BU", "BO")); m = len(C); E = V5_ESIK["esik"]
    if any(BU[i] - BO[i] <= 0 for i in range(m)):
        return {p: False for p in DUZ_PARCA}
    rg = [max(H[i] - L[i], 1e-12) for i in range(m)]; ust = [H[i] - max(O[i], C[i]) for i in range(m)]; alt = [min(O[i], C[i]) - L[i] for i in range(m)]
    m4 = sum(ust) / sum(alt) if sum(alt) > 0 else float("inf")
    M = (sum(abs(C[i] - O[i]) / rg[i] for i in range(m)) / m <= E["m1"] and sum(alt[i] / rg[i] for i in range(m)) / m <= E["m2"]
         and sum(ust[i] / rg[i] for i in range(m)) / m >= E["m3"] and m4 >= E["m4"])
    bC = [(C[i] - BO[i]) / (BU[i] - BO[i]) for i in range(m)]; bO = [(O[i] - BO[i]) / (BU[i] - BO[i]) for i in range(m)]
    k = next((i for i in range(m) if bC[i] > 0), None)
    Y = k is not None and 3 <= k <= math.floor(E["k_ust"] * m + 1e-9) and m - 1 - k >= E["en_az_sonra"]
    if not Y:
        return {**{p: False for p in DUZ_PARCA}, "M": bool(M)}
    yon = [np.sign(C[j] - C[j - 1]) for j in range(1, k)]; dg = sum(1 for j in range(1, len(yon)) if yon[j] * yon[j - 1] < 0)
    G1 = sum(bC[:k]) / k <= E["G1_ort"] and dg >= E["G1_degisim"]
    po = list(range(k + 1, m)); n = len(po)
    G2 = C[k] > O[k] and bC[k - 1] < 0 and sum(1 for j in po if bC[j] > 0) / n >= E["G2_ust"]
    rk = _rank5([C[j] for j in po]); xs = list(range(n)); mr = sum(rk) / n; mx = sum(xs) / n
    den = (sum((rk[i] - mr) ** 2 for i in range(n)) * sum((xs[i] - mx) ** 2 for i in range(n))) ** 0.5
    sp = sum((rk[i] - mr) * (xs[i] - mx) for i in range(n)) / den if den > 0 else 0.0
    T = sp >= E["T_spearman"] and bC[m - 1] >= E["T_son"]
    I = sum(1 for j in po if bC[j] <= E["I_ust"]) / n >= E["I_pay"]
    gv = sorted(abs(bC[j] - bO[j]) for j in po); med = gv[n // 2] if n % 2 else (gv[n // 2 - 1] + gv[n // 2]) / 2
    B = gv[-1] <= E["B_max"] and med <= E["B_med"]
    F = sum(1 for j in po if (H[j] - max(O[j], C[j])) > (min(O[j], C[j]) - L[j])) / n >= E["F_pay"]
    return {"Y": True, "G1": bool(G1), "G2": bool(G2), "T": bool(T), "I": bool(I), "B": bool(B), "F": bool(F), "M": bool(M), "k": k}


# ================================================================ 2) SERİ TARAMASI
def v5_tara_seri(O, H, L, C, kural, bosluk: Optional[np.ndarray] = None, sonlar: Optional[np.ndarray] = None, S_hep: bool = False):
    """Her son: kural VAR (16-24'ten biri), VAR pencerelerinde en yüksek v1 S, uzunluğu ve k'sı (S kuralda yoksa S_hep True ise hesaplanır).
    kural bir ad ise tek çıktı, ad listesi ise {ad: çıktı} (parçalar bir kez hesaplanır)."""
    adlar = [kural] if isinstance(kural, str) else list(kural)
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C)); T_ = len(C); BU, BO, BA = MI.mi_bant(C); s0 = 19
    bc = np.r_[0, np.cumsum(bosluk.astype(np.int64))] if bosluk is not None else None
    outs = {ad: {"VAR": np.zeros(T_, bool), "S": np.full(T_, np.nan), "m": np.zeros(T_, np.int64), "k": np.full(T_, -1, np.int64)} for ad in adlar}
    for m in V5_ESIK["uzunluklar"]:
        e = np.arange(s0 + m - 1, T_)
        if sonlar is not None:
            e = np.intersect1d(e, np.asarray(sonlar, np.int64))
        if bc is not None and len(e):
            e = e[(bc[e + 1] - bc[e - m + 2]) == 0]
        if not len(e):
            continue
        idx = (e - m + 1)[:, None] + np.arange(m)[None, :]
        P = v5_parcalar(O[idx], H[idx], L[idx], C[idx], BU[idx], BO[idx])
        on = {ad: np.all(np.stack([P[p] for p in v5_liste(ad) if p != "S"]), 0) for ad in adlar}
        sgerek = {ad: "S" in v5_liste(ad) for ad in adlar}
        hes = np.zeros(len(e), bool)
        for ad in adlar:
            if sgerek[ad] or S_hep:
                hes |= on[ad]
        Sv = np.full(len(e), np.nan)
        if hes.any():
            j = np.flatnonzero(hes)
            Sv[j] = MI.mi_S_pencere(O[idx[j]], H[idx[j]], L[idx[j]], C[idx[j]], BU[idx[j]], BO[idx[j]], BA[idx[j]], _v5_sab())
        for ad in adlar:
            o = outs[ad]; sv_ad = Sv if (sgerek[ad] or S_hep) else np.where(on[ad], 0.0, np.nan)
            var = on[ad] & (np.nan_to_num(sv_ad, nan=-1.0) >= V5_ESIK["esik"]["S"]) if sgerek[ad] else on[ad]
            ee = e[var]; sv = sv_ad[var]
            iy = ~(sv <= o["S"][ee]) | ~o["VAR"][ee]
            o["S"][ee[iy]] = sv[iy]; o["m"][ee[iy]] = m; o["k"][ee[iy]] = P["k"][var][iy]; o["VAR"][ee] = True
    return outs[kural] if isinstance(kural, str) else outs


def v5_tekil(e: np.ndarray, S: np.ndarray, aralik: int = 15) -> np.ndarray:
    if not len(e):
        return np.asarray(e, np.int64)
    e = np.sort(np.asarray(e, np.int64)); kir = np.flatnonzero(np.diff(e) >= aralik) + 1
    return np.array([int(g[np.argmax(np.nan_to_num(S[g], nan=-9.0))]) for g in np.split(e, kir)], np.int64)


# ================================================================ 3) ADAY TABLOSU ve SEÇİM (61 etiket)
def v5_etiketler() -> pd.DataFrame:
    T = pd.read_csv(V5_YOL["etiket"]); T = T[T.cemal.notna()].copy(); T["cemal"] = T.cemal.astype(int)
    if len(T) != 61 or int(T.cemal.sum()) != 16:
        raise V5Hata(f"etiket sayısı beklenenden farklı: {len(T)} / EVET {int(T.cemal.sum())} (61 / 16)")
    A1 = {int(r["sayfa"]): r for r in json.load(open(V5_YOL["anahtar1"], encoding="utf-8"))["sayfalar"]}
    A2 = {int(r["sayfa"]): r for r in json.load(open(V5_YOL["anahtar2"], encoding="utf-8"))["sayfalar"]}
    rows = []
    for r in T.itertuples():
        a = (A1 if r.set == "set1" else A2)[int(r.sayfa)]
        if a["zaman"] != r.zaman:
            raise V5Hata(f"K10: zaman uyuşmuyor ({r.set} {r.sayfa})")
        rows.append({"set": r.set, "sayfa": int(r.sayfa), "zaman": a["zaman"], "pazar": a["pazar"], "sembol": a["sembol"], "tarih": a["tarih"], "m": int(a["m"]),
                     "cemal": int(r.cemal), "S_anahtar": a.get("S")})
    return pd.DataFrame(rows)


def _v5_ozet(var: np.ndarray, c: np.ndarray, B: int, tohum: int) -> Dict[str, Any]:
    var = np.asarray(var, int); c = np.asarray(c, int)
    o = {"n": int(len(c)), "evet": int(c.sum()), "VAR": int(var.sum()), "evet_var": int(((c == 1) & (var == 1)).sum()), "evet_yok": int(((c == 1) & (var == 0)).sum()),
         "hayir_var": int(((c == 0) & (var == 1)).sum()), "hayir_yok": int(((c == 0) & (var == 0)).sum())}
    o["isabet"] = o["evet_var"] / o["VAR"] if o["VAR"] else None; o["yakalama"] = o["evet_var"] / o["evet"] if o["evet"] else None
    k = V4.v4_kappa(var, c); o["kappa"] = None if not np.isfinite(k) else float(k)
    o.update(V4.v4_kappa_boot(var, c, B, tohum))
    return o


def v5_sec(tab: Dict[str, Dict[str, Any]], var_en_az: int) -> Dict[str, Any]:
    """Seçim kuralı: VAR >= var_en_az adaylar; en yüksek kappa; 0,03'ten az geride olanlar içinde en az parçalı (eşitse yüksek kappa); kappa <= 0,20 -> DUR."""
    S = V5_ESIK["secim"]
    uy = {a: v for a, v in tab.items() if v["VAR"] >= var_en_az and v["kappa"] is not None}
    if not uy:
        return {"secilen": None, "durum": "DUR", "neden": "VAR en az koşulunu sağlayan aday yok"}
    kmax = max(v["kappa"] for v in uy.values())
    yakin = [a for a, v in uy.items() if v["kappa"] > kmax - S["fark"] - 1e-12]
    sec = sorted(yakin, key=lambda a: (len(KURAL[a]), -uy[a]["kappa"], a))[0]
    if uy[sec]["kappa"] <= S["kappa_en_az"]:
        return {"secilen": None, "durum": "DUR", "neden": f"en iyi uygun adayın kappası {uy[sec]['kappa']:.3f} <= {S['kappa_en_az']}", "aday": sec}
    return {"secilen": sec, "durum": "SEÇİLDİ", "kappa": uy[sec]["kappa"], "kmax": kmax, "yakin": yakin, "uygun": sorted(uy)}


def v5_aday(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V5_YOL["cikti"]; X = v5_etiketler(); Vc: Dict[Any, Any] = {}; sab = _v5_sab(); rows = []
    for r in X.itertuples():
        W = V3.v3_pencere(r.zaman, r.pazar, r.sembol, r.tarih, int(r.m), Vc)
        P = v5_parcalar(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"], W["BA"], S=True); dz = v5_duz(W)
        for p in DUZ_PARCA:
            if bool(P[p][0]) != bool(dz[p]):
                raise V5Hata(f"K11: düz döngü farklı ({r.set} {r.sayfa} {p})")
        if r.set == "set1" and abs(float(P["d_S"][0]) - float(r.S_anahtar)) > 1e-4:
            raise V5Hata(f"K10: set 1 sayfa {r.sayfa} v1 S anahtardan farklı")
        rows.append({**r._asdict(), "k": int(P["k"][0]), **{p: bool(P[p][0]) for p in PARCA}, **{f"d_{a}": float(P[f"d_{a}"][0]) for a in _DEG + ["S"]},
                     **{f"g_{a}": bool(P[f"g_{a}"][0]) for a in ("m1", "m2", "m3", "m4")}, **{a: bool(v5_kural(P, a)[0]) for a in KURAL}})
    T = pd.DataFrame(rows).drop(columns=["Index"]); T.to_csv(_v5_yol("aday_csv", cikti), index=False, float_format="%.5f")
    A = V5_ESIK["aday"]; tab = {}
    for a in KURAL:
        tab[a] = {"parca": len(KURAL[a]), **_v5_ozet(T[a].to_numpy(), T.cemal.to_numpy(), A["B"], A["tohum"]),
                  "set1": _v5_ozet(T[T.set == "set1"][a].to_numpy(), T[T.set == "set1"].cemal.to_numpy(), A["B"], A["tohum"]),
                  "set2": _v5_ozet(T[T.set == "set2"][a].to_numpy(), T[T.set == "set2"].cemal.to_numpy(), A["B"], A["tohum"])}
        k1, k2 = tab[a]["set1"]["kappa"], tab[a]["set2"]["kappa"]
        tab[a]["iki_set_ayni_yon"] = None if (k1 is None or k2 is None) else bool(np.sign(k1) == np.sign(k2) and k1 != 0)
    sec = v5_sec(tab, V5_ESIK["secim"]["var_en_az"])
    nihai = None
    if sec["durum"] == "SEÇİLDİ":
        ad = f"{sec['secilen']}+M"; T[ad] = T[sec["secilen"]] & T["M"]
        nihai = {"ad": ad, "parcalar": v5_liste(ad), **_v5_ozet(T[ad].to_numpy(), T.cemal.to_numpy(), A["B"], A["tohum"]),
                 "set1": _v5_ozet(T[T.set == "set1"][ad].to_numpy(), T[T.set == "set1"].cemal.to_numpy(), A["B"], A["tohum"]),
                 "set2": _v5_ozet(T[T.set == "set2"][ad].to_numpy(), T[T.set == "set2"].cemal.to_numpy(), A["B"], A["tohum"])}
        T.to_csv(_v5_yol("aday_csv", cikti), index=False, float_format="%.5f")
    mgec = {a: {"evet": float(T[T.cemal == 1][c].mean()), "hayir": float(T[T.cemal == 0][c].mean())}
            for a, c in (("M", "M"), ("m1", "g_m1"), ("m2", "g_m2"), ("m3", "g_m3"), ("m4", "g_m4"))}
    mdeg = {a: {"evet_medyan": float(T[T.cemal == 1][f"d_{a}"].median()), "hayir_medyan": float(T[T.cemal == 0][f"d_{a}"].median())} for a in ("m1", "m2", "m3", "m4")}
    cap = {}
    for st, ot in (("set1", "set2"), ("set2", "set1")):
        n = int((T.set == st).sum()); en = int(math.ceil(V5_ESIK["secim"]["var_en_az"] * n / 61))
        s = v5_sec({a: tab[a][st] for a in KURAL}, en)
        cap[f"{st}_sec_{ot}_sina"] = {"var_en_az": en, "secilen": s["secilen"], "durum": s["durum"],
                                       "kappa_secim_seti": tab[s["secilen"]][st]["kappa"] if s["secilen"] else None,
                                       "kappa_obur_set": tab[s["secilen"]][ot]["kappa"] if s["secilen"] else None}
    sb = v5_parcalar(*(sab["ohlc"][x] for x in ("O", "H", "L", "C", "BU", "BO", "BA")), S=True)
    sablon = {"k": int(sb["k"][0]), **{p: bool(sb[p][0]) for p in PARCA}, **{f"d_{a}": float(sb[f"d_{a}"][0]) for a in _DEG + ["S"]},
              **{a: bool(v5_kural(sb, a)[0]) for a in KURAL}}
    if not sablon["M"]:
        raise V5Hata(f"ŞABLON M'DEN GEÇMEDİ: { {a: sablon['d_' + a] for a in ('m1', 'm2', 'm3', 'm4')} } -> DUR")
    J = {"surum": V5_SURUM, "n": int(len(T)), "evet": int(T.cemal.sum()), "tablo": tab, "secim": sec, "nihai": nihai, "M_gecme": mgec, "M_deger": mdeg,
         "capraz": cap, "sablon": sablon,
         "parca_gecme": {p: {"evet": float(T[T.cemal == 1][p].mean()), "hayir": float(T[T.cemal == 0][p].mean())} for p in PARCA}, "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_v5_yol("aday", cikti), J, "aday 8")
    return J


def v5_secilen(cikti: Optional[str] = None, nihai: bool = False) -> str:
    J = json.load(open(_v5_yol("aday", cikti), encoding="utf-8"))
    if J["secim"]["durum"] != "SEÇİLDİ":
        raise V5Hata(f"seçim DUR: {J['secim'].get('neden')}")
    return J["nihai"]["ad"] if nihai else J["secim"]["secilen"]


# ================================================================ 4) SENTETİK
_V5_SENT: Dict[str, Any] = {}


def _v5_kendi(tur: str, P: Dict[str, np.ndarray]) -> bool:
    """Negatifin kendi ölçüsü ihlal ediliyor mu (pencerenin kendi k'sıyla; Y sınırları aranmadan; k yoksa ihlal)."""
    E = V5_ESIK["esik"]; hedef = V5_ESIK["sentetik"]["kendi_olcu"][tur]
    if tur == "n8b":
        v = float(P["d_cikis_govde"][0]); return (not np.isfinite(v)) or v > E["B_max"]
    return not bool(P[f"ham_{hedef}"][0])


def _v5_sent_isci(arg: Tuple[str, int, int, int, int, float]) -> Dict[str, Any]:
    tur, ti, ui, bi, t, gr = arg; Sn = V5_ESIK["sentetik"]; G = _V5_SENT
    rng = np.random.default_rng([int(Sn["kok"]), ti, ui, bi, int(round(gr * 100)), t])
    X = V3.v3_seri(rng, G["havuz"], G["ohlc"][tur], Sn["uretec"][ui], Sn["baglam"][bi], float(gr))
    e = int(X["e"]); m = e - int(MI.MI_ESIK["sentetik"]["seri_on"]) + 1; tol = int(Sn["tol"])
    R = v5_tara_seri(X["O"], X["H"], X["L"], X["C"], G["kural"], sonlar=np.arange(e - tol, e + tol + 1))
    BU, BO, BA = MI.mi_bant(X["C"]); sl = slice(e - m + 1, e + 1)
    P = v5_parcalar(X["O"][sl], X["H"][sl], X["L"][sl], X["C"][sl], BU[sl], BO[sl])
    return {"tur": tur, "uretec": Sn["uretec"][ui], "baglam": Sn["baglam"][bi], "gurultu": gr, "VAR": bool(R["VAR"][e - tol:e + tol + 1].any()),
            "kendi_ihlal": _v5_kendi(tur, P) if tur != "poz" else None, "m": m, **{f"g_{p}": bool(P[p][0]) for p in DUZ_PARCA}}


def _v5_yanlis_isci(arg: Tuple[int, int]) -> Tuple[int, int]:
    ui, t = arg; Sn = V5_ESIK["sentetik"]; rng = np.random.default_rng([int(Sn["kok"]), 99, ui, t])
    lO, lH, lL, lC = MI.mi_uret(rng, int(Sn["yanlis"]["n"]) + 60, _V5_SENT["havuz"], Sn["uretec"][ui])
    R = v5_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC), _V5_SENT["kural"])
    n = int(len(lC) - 19 - 15); e = np.flatnonzero(R["VAR"])
    return n, int(len(v5_tekil(e, R["S"])))


def v5_sentetik(cikti: Optional[str] = None, islem: int = 4, nihai: bool = False) -> Dict[str, Any]:
    """nihai False: seçilen aday kural (mum_izi8_sentetik.json); True: v5M = seçilen ∧ M (mum_izi8_sentetik_v5m.json; ek negatif n2)."""
    import multiprocessing as mp
    t0 = time.time(); cikti = cikti or V5_YOL["cikti"]; Sn = V5_ESIK["sentetik"]; kural = v5_secilen(cikti, nihai)
    a = MI.mi_sablon_yukle()["tam"]; K = MV.mv_karsi_ornek(a); K4 = V4.v4_karsi()
    ohlc = {"poz": {x: a["ohlc"][x] for x in ("O", "H", "L", "C")}, "n1": K["n1"], **({"n2": K["n2"]} if nihai else {}), "n3": K["n3"], "n5": K["p1"], "n6": K4["n6"], "n7": K4["n7"], "n8a": K4["n8a"],
            "n8b": K4["n8b"]}
    _V5_SENT.clear(); _V5_SENT.update({"havuz": pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"])), "ohlc": ohlc, "kural": kural})
    turler = list(ohlc)
    isler = [(tur, ti, ui, bi, t, gr) for ti, tur in enumerate(turler) for ui in range(len(Sn["uretec"])) for bi in range(len(Sn["baglam"]))
             for gr in Sn["gurultu"] for t in range(int(Sn["tohum"]))]
    try:
        with mp.get_context("fork").Pool(islem) as pool:
            R = list(pool.imap(_v5_sent_isci, isler, chunksize=64))
            Y = list(pool.imap(_v5_yanlis_isci, [(ui, t) for ui in range(len(Sn["uretec"])) for t in range(int(Sn["yanlis"]["seri"]))], chunksize=8))
    finally:
        _V5_SENT.clear()
    D = pd.DataFrame(R); out: Dict[str, Any] = {"surum": V5_SURUM, "kural": kural, "parcalar": v5_liste(kural)}
    for tur, g in D.groupby("tur", sort=False):
        o = {"VAR": float(g.VAR.mean()), "n": int(len(g)), "gurultu": {f"{x:.1f}": float(h.VAR.mean()) for x, h in g.groupby("gurultu")},
             "baglam": {x: float(h.VAR.mean()) for x, h in g.groupby("baglam")}, "gomulu_pencere_parca": {p: float(g[f"g_{p}"].mean()) for p in DUZ_PARCA}}
        if tur != "poz":
            o["kendi_olcu"] = Sn["kendi_olcu"][tur]; o["kendi_ihlal_payi"] = float(g.kendi_ihlal.mean()); o["gecerli"] = bool(o["kendi_ihlal_payi"] >= Sn["gecerli_pay"])
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
    MI._mi_jyaz(_v5_yol("sentetik_m" if nihai else "sentetik", cikti), out, "sentetik 8")
    return out


# ================================================================ 5) KAPI ve ÖN KAYIT
def v5_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD8_SHA": MI._mi_sha(V5_YOL["kod"]), "ESIK8_SHA": v5_esik_sha(), "ADAY8_SHA": MI._mi_sha(_v5_yol("aday", cikti)),
            "SENTETIK8_SHA": MI._mi_sha(_v5_yol("sentetik", cikti)), "SENTETIK8M_SHA": MI._mi_sha(_v5_yol("sentetik_m", cikti)),
            "V4_KOD_SHA": MI._mi_sha(V4.V4_YOL["kod"]), "V3_KOD_SHA": MI._mi_sha(V3.V3_YOL["kod"]),
            "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]), "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]), "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"]),
            "E6_KOD_SHA": MI._mi_sha(os.path.join(KOK_V5, "MUM_IZI_ETIKET2.py")), "ETIKET_CSV_SHA": MI._mi_sha(V5_YOL["etiket"])}


def v5_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or V5_YOL["cikti"]; yol = _v5_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise V5Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = v5_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise V5Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_V5); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise V5Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_V5.py", "MUM_IZI_V4.py", "MUM_IZI_V3.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py",
                   "MUM_IZI_ETIKET2.py", os.path.relpath(_v5_yol("aday", cikti), KOK_V5), os.path.relpath(_v5_yol("sentetik", cikti), KOK_V5),
                   os.path.relpath(_v5_yol("sentetik_m", cikti), KOK_V5)]):
        raise V5Hata("ön kayıt / kod / aday / sentetik çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def _v5_f(x, n: int = 3) -> str:
    return "-" if x is None else f"{x:.{n}f}"


def _v5_sent_satir(SJ: Dict[str, Any]) -> List[str]:
    neg = [t for t in SJ if t.startswith("n") and isinstance(SJ[t], dict) and "kendi_olcu" in SJ[t]]
    return [f"- pozitif VAR: {SJ['poz']['gurultu']} (bağlam {SJ['poz']['baglam']}; gömülü pencerede parça geçme {SJ['poz']['gomulu_pencere_parca']})",
            *[f"- {n}: kendi ölçüsü {SJ[n]['kendi_olcu']} ihlal payı {100 * SJ[n]['kendi_ihlal_payi']:.1f} % -> {'GEÇERLİ' if SJ[n]['gecerli'] else 'KURGU GEÇERSİZ'}; "
              f"VAR {100 * SJ[n]['VAR']:.1f} %" for n in neg],
            f"- rastgele: {SJ['rastgele']}", f"- KABUL ÖLÇÜTÜ: {'GEÇTİ' if SJ['olcut']['gecti'] else 'GEÇMEDİ'} {json.dumps(SJ['olcut'], ensure_ascii=False)}"]


def v5_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or V5_YOL["cikti"]; y = _v5_yol("onkayit", cikti)
    if os.path.exists(y):
        raise V5Hata("ön kayıt zaten var")
    sh = v5_sha_simdi(cikti); AJ = json.load(open(_v5_yol("aday", cikti), encoding="utf-8")); SJ = json.load(open(_v5_yol("sentetik", cikti), encoding="utf-8"))
    SM = json.load(open(_v5_yol("sentetik_m", cikti), encoding="utf-8")); f = _v5_f
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in V5_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_V5.py"])
    tb = ["| kural | parça | VAR | EVET-VAR | isabet | yakalama | kappa (%95) | set 1 kappa | set 2 kappa |", "|---|---|---|---|---|---|---|---|---|"]
    sat = list(AJ["tablo"].items()) + ([(AJ["nihai"]["ad"] + " (v5M, nihai)", {**AJ["nihai"], "parca": len(AJ["nihai"]["parcalar"])})] if AJ.get("nihai") else [])
    for a, v in sat:
        tb.append(f"| {a} | {v['parca']} | {v['VAR']} | {v['evet_var']} | {f(v['isabet'], 2)} | {f(v['yakalama'], 2)} | {f(v['kappa'])} ({f(v['boot95'][0], 2)}..{f(v['boot95'][1], 2)}) | "
                  f"{f(v['set1']['kappa'])} | {f(v['set2']['kappa'])} |")
    sb = AJ["sablon"]
    s = [f"# MUM_IZI8 ÖN KAYIT ({MI._mi_simdi()})", "",
         "v5: etiketlerle (61 karar) önceden yazılı 8 aday arasından önceden yazılı seçim kuralıyla seçilen evre kuralı; NİHAİ KURAL v5M = seçilen kural ∧ M "
         "(Cemal'in 26 Kasım kesin şartı: küçük gövde, alt fitil az / yok, üst fitil uzun; sözle kondu, etiketle seçilmedi). Bu dosya evren taramasından ve PDF'ten "
         "ÖNCE commit edilir; sonra kural, eşik ve onay seçimi değişmez. Seçim iç örnektir (ezber riski); gerçek sınama Cemal'in MUM_IZI8_ONAY.pdf işaretleri.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_V5.py commit'i: {kc or 'yok'}", "",
         "## Aday tablosu (61 etiket; 16 EVET) + nihai v5M", "", *tb, "",
         f"- Seçim: {json.dumps(AJ['secim'], ensure_ascii=False)}", f"- Çapraz set (bilgi): {json.dumps(AJ['capraz'], ensure_ascii=False)}", "",
         "## M (mum yapısı) Cemal'in kendi işaretlerinde (geçme payı EVET / HAYIR; medyan değer EVET / HAYIR)", "",
         *[f"- {a}: geçme {100 * v['evet']:.0f} % / {100 * v['hayir']:.0f} %" + (f"; medyan {AJ['M_deger'][a]['evet_medyan']:.3f} / {AJ['M_deger'][a]['hayir_medyan']:.3f}"
                                                                                  if a in AJ["M_deger"] else "") for a, v in AJ["M_gecme"].items()],
         f"- Şablon M değerleri: m1 {sb['d_m1']:.3f} (<= 0,45), m2 {sb['d_m2']:.3f} (<= 0,25), m3 {sb['d_m3']:.3f} (>= 0,33), m4 {sb['d_m4']:.3f} (>= 1,5; toplam üst / "
         f"toplam alt fitil); M {sb['M']}. Şablon bütün parçalar: { {p: sb[p] for p in PARCA} }", "",
         f"## Sentetik: seçilen aday kural {SJ['kural']} = {' ∧ '.join(SJ['parcalar'])} (bilgi)", "", *_v5_sent_satir(SJ), "",
         f"## Sentetik: NİHAİ v5M {SM['kural']} = {' ∧ '.join(SM['parcalar'])}", "", *_v5_sent_satir(SM), "",
         "## Kural, eşikler, onay seçimi (V5_ESIK; sha yukarıda)", "", "```", json.dumps(V5_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 8")


# ================================================================ 6) EVREN TARAMASI ve ONAY SEÇİMİ
_V5_ISCI: Dict[str, Any] = {}


def _v5_isci(s: str) -> Dict[str, Any]:
    import MUM_IZI_ETIKET2 as E6
    G = _V5_ISCI; d = G["V"][s]; z = G["zaman"]; p = G["pazar"]; uc = G["uc"]; ix = d.index
    RR = v5_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), G["kurallar"], d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None,
                      S_hep=True)
    ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1])); out = {"sembol": s, "n_bar": int(ara.sum()), "olay": {}}
    for ad, R in RR.items():
        e = v5_tekil(np.flatnonzero(R["VAR"] & ara), R["S"])
        if p in ("ABD", "AVR"):
            ev = np.zeros(len(e), bool)
            for (a, b), P in G["P"]:
                j = np.flatnonzero((ix[e] >= pd.Timestamp(a)) & (ix[e] <= pd.Timestamp(b)))
                if len(j):
                    ev[j] = E6.e6_p2_maske(P, s, ix[e][j])
        else:
            dv = (d.Close * d.Volume).to_numpy(float)[e]; med = G["med"].reindex(E6._e6_anahtar(ix[e], z)).to_numpy(float); ev = np.isfinite(med) & (dv > med)
        out["olay"][ad] = [{"t": int(t), "tarih": str(ix[t].date()), "m": int(R["m"][t]), "k": int(R["k"][t]), "S": float(R["S"][t]), "evren": bool(v)}
                           for t, v in zip(e, ev)]
    return out


def v5_tarama(cikti: Optional[str] = None, islem: int = 3) -> Dict[str, Any]:
    import multiprocessing as mp
    import KASA as KS
    import MUM_IZI_ETIKET2 as E6
    t0 = time.time(); cikti = cikti or V5_YOL["cikti"]
    if os.path.exists(_v5_yol("tarama", cikti)):
        raise V5Hata("tarama zaten var")
    G0 = v5_kapi(cikti); kural = v5_secilen(cikti); nihai = v5_secilen(cikti, True); kurallar = [kural, nihai]
    yol = [os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + \
          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")]
    kasa = KS.kasa_kapisi(yol, "2022-12-31"); olay: Dict[str, List[Dict[str, Any]]] = {ad: [] for ad in kurallar}; say: Dict[str, Any] = {ad: {} for ad in kurallar}
    for z in ("gunluk", "haftalik"):
        uc = V5_ESIK["tarama"][z]
        for p in ("ABD", "AVR", "BIST"):
            V = MV.mv_veri(z, p); Ps = []; med = None
            if p in ("ABD", "AVR"):
                Ps = [(ara, E6.e6_p2_hazirla(p, kl)) for ara, kl in E6.e6_parcalar(z, p)]
            else:
                med = E6.e6_bist_medyan(V, z)
            _V5_ISCI.clear(); _V5_ISCI.update({"V": V, "zaman": z, "pazar": p, "P": Ps, "med": med, "uc": uc, "kurallar": kurallar})
            try:
                with mp.get_context("fork").Pool(islem) as pool:
                    R = list(pool.imap(_v5_isci, sorted(V), chunksize=16))
            finally:
                _V5_ISCI.clear()
            nb = int(sum(r["n_bar"] for r in R)); yil = nb / (252.0 if z == "gunluk" else 52.0)
            for ad in kurallar:
                ol = [dict(o, sembol=r["sembol"], zaman=z, pazar=p) for r in R for o in r["olay"][ad]]; olay[ad] += ol
                ne = int(sum(o["evren"] for o in ol))
                say[ad][f"{z}|{p}"] = {"hisse": len(R), "bar": nb, "hisse_yil": round(yil, 1), "olay": len(ol), "olay_evren": ne,
                                       "hisse_yil_basina": (len(ol) / yil) if yil else None, "evren_hisse_yil_basina": (ne / yil) if yil else None}
            del V, Ps, med; gc.collect()
            v5log.info("%s %s: %s (%.0f sn)", z, p, {ad: say[ad][f"{z}|{p}"]["olay"] for ad in kurallar}, time.time() - t0)
    for ad in kurallar:
        if olay[ad] and max(pd.Timestamp(o["tarih"]) for o in olay[ad]) > MI.MI_KESIK:
            raise V5Hata("KESİK AŞIMI")
    haric = {r["sembol"] for r in json.load(open(V5_YOL["anahtar1"], encoding="utf-8"))["sayfalar"]} | \
            {r["sembol"] for r in json.load(open(V5_YOL["anahtar2"], encoding="utf-8"))["sayfalar"]}
    sec = v5_onay_secim(olay[nihai], haric)
    os.makedirs(V5_YOL["gecici"], exist_ok=True); hp = os.path.join(V5_YOL["gecici"], "tarama_ham.json")
    MI._mi_jyaz(hp, {"olay": olay, "secim": sec}, "tarama ham 8")
    G = V5_ESIK["onay"]
    J = {"surum": V5_SURUM, "kural": kural, "nihai": nihai, "kapi": G0, "kasa": kasa, "sayim": say, "ham_sha": MI._mi_sha(hp), "n_secim": len(sec),
         "secim_sayim": {"zaman": pd.Series([r["zaman"] for r in sec], dtype=object).value_counts().to_dict(),
                         "pazar": pd.Series([r["pazar"] for r in sec], dtype=object).value_counts().to_dict()},
         "uygun_olay": {z: int(sum(1 for o in olay[nihai] if o["zaman"] == z and o["evren"] and o["sembol"] not in haric)) for z in ("gunluk", "haftalik")},
         "onay_durum": "DUR (v5M uygun bölge < 8)" if len(sec) < G["en_az"] else "HAZIR", "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_v5_yol("tarama", cikti), J, "tarama 8")
    return J


def v5_onay_secim(olay: List[Dict[str, Any]], haric: set) -> List[Dict[str, Any]]:
    """v5M olaylarından RASTGELE: önce haftalık sonra günlük; hisse başına bir; önceki setlerin hisseleri hariç; BIST dilim başına <= 4; az ise hepsi."""
    G = V5_ESIK["onay"]; rng = np.random.default_rng(G["tohum"]); sec: List[Dict[str, Any]] = []; gor = set(haric)
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
def _v5_okuma_ciz(ax, i0: int, k: int, m: int, L: np.ndarray, H: np.ndarray) -> None:
    """Pencere [i0, i0+m-1] (eksen koordinatında): mavi gel-git (0..k-1), yeşil ok çıkış mumu (k), turuncu tırmanış (k+1..m-1); mumların arkasında."""
    ax.axvspan(i0 - 0.5, i0 + k - 0.5, color="#4a90d9", alpha=0.18, zorder=0, linewidth=0)
    ax.axvspan(i0 + k + 0.5, i0 + m - 0.5, color="#ff8c1a", alpha=0.18, zorder=0, linewidth=0)
    x = i0 + k; lo = float(np.nanmin(L)); hi = float(np.nanmax(H)); yy = float(L[x]) if x < len(L) else lo
    ax.annotate("", xy=(x, yy - 0.01 * (hi - lo)), xytext=(x, yy - 0.16 * (hi - lo)), arrowprops=dict(arrowstyle="-|>", color="#1a9850", lw=2.5), zorder=5)
    ax.set_ylim(lo - 0.2 * (hi - lo), hi + 0.05 * (hi - lo))


def _v5_m_metin(P: Dict[str, Any], i: int = 0) -> str:
    g = lambda a: float(P[f"d_{a}"][i]) if not isinstance(P[f"d_{a}"], float) else float(P[f"d_{a}"])  # noqa: E731
    m4 = g("m4")
    return _v5_virgul(f"mum yapısı: gövde {g('m1'):.2f} · alt fitil {g('m2'):.2f} · üst fitil {g('m3'):.2f} · üst / alt "
                      f"{'∞' if not np.isfinite(m4) else f'{m4:.1f}'}")


def _v5_virgul(t: str) -> str:
    import re
    return re.sub(r"(\d)\.(\d)", r"\1,\2", t)


def _v5_cumle(kural: str) -> List[str]:
    c = {"Y": None, "G1": "1) Mavi: SMA'nın alt bandında bir-iki gel-git (kapanışlar alt bant tarafında, yön en az iki kez dönüyor).",
         "G2": "2) Yeşil ok: yeşil mumla SMA'yı aşıyor; sonraki kapanışların çoğu (%80) SMA'nın üstünde kalıyor.",
         "T": "3) Turuncu: fiyat sonra düzenli yükseliyor; son kapanış üst banda yakın.",
         "I": "4) Tırmanış bandın içinden: kapanışların çoğu üst bandı aşmıyor.",
         "B": "5) Küçük küçük mumlar: tırmanıştaki gövdeler banda göre küçük.",
         "F": "6) Tırmanış mumlarının yarısından çoğunda üst fitil alt fitilden uzun.",
         "S": "7) Eski benzerlik puanı da eşiği geçiyor.",
         "M": "Mum yapısı şartın (küçük gövde, alt fitil az, üst fitil uzun) zorunlu kapı."}
    return [c[p] for p in v5_liste(kural) if c.get(p)]


def v5_onay(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or V5_YOL["cikti"]; y = _v5_yol("onay", cikti); ya = _v5_yol("anahtar", cikti)
    if os.path.exists(y) or os.path.exists(ya):
        raise V5Hata("PDF / anahtar zaten var")
    JT = json.load(open(_v5_yol("tarama", cikti), encoding="utf-8")); hp = os.path.join(V5_YOL["gecici"], "tarama_ham.json")
    if MI._mi_sha(hp) != JT["ham_sha"]:
        raise V5Hata("tarama ham dosyası değişmiş")
    if JT["onay_durum"] != "HAZIR":
        raise V5Hata(f"onay seti: {JT['onay_durum']}")
    sec = json.load(open(hp, encoding="utf-8"))["secim"]; kural = JT["nihai"]
    AJ = json.load(open(_v5_yol("aday", cikti), encoding="utf-8")); SM = json.load(open(_v5_yol("sentetik_m", cikti), encoding="utf-8"))
    tk = json.load(open(V5_YOL["olcum6"], encoding="utf-8"))["T1"]; tb = AJ["nihai"]
    a = MV.mv_sablon()["tam"]["ohlc"]; sb = AJ["sablon"]; once = int(MV.MV_ESIK["onay"]["once"]); Vc: Dict[Any, Any] = {}
    nz = {z: sum(1 for r in sec if r["zaman"] == z) for z in ("gunluk", "haftalik")}
    with PdfPages(y, metadata={"Title": "MUM_IZI8 onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.95, "KOD NASIL TESPİT EDİYOR", fontsize=17, weight="bold")
        sat = _v5_cumle(kural)
        sat.append(f"Senin 61 işaretinle: benziyor dediğin {tb['evet']} sayfanın {tb['evet_var']}'ini buldu; 'var' dediği {tb['VAR']} sayfanın "
                   f"{tb['evet_var']}'ine sen de benziyor demiştin.")
        sat.append(f"Tekrar sayfalarında sen de {tk['n']}'de {tk['ayni']} aynı dedin.")
        if not SM["olcut"]["gecti"]:
            sat.append("Uyarı: kodun sentetik sınavı (kalıbı gömüp bulma, yanlışları reddetme) ölçütü GEÇMEDİ.")
        fig.text(0.06, 0.89, "\n\n".join(sat[:8]), fontsize=12, va="top", wrap=True)
        alt = (f"Sonraki sayfa: senin kalıbında kodun okuması. Sonra {len(sec)} rastgele bölge (haftalık {nz['haftalik']}, günlük {nz['gunluk']}); "
               "her birinde kodun okuması aynı renklerle.\nBenziyorsa ✓, benzemiyorsa × kutusuna X koy; yanlış okunan parçayı daire içine al.\n"
               f"{len(sec)} sayfanın en az %80'i ✓ ise tespit geçerli sayılır.")
        fig.text(0.06, 0.16, alt, fontsize=11, va="top", wrap=True)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.08, 0.38, 0.86, 0.52])
        MV._mv_ciz(ax, a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın: kodun okuması")
        _v5_okuma_ciz(ax, 0, int(sb["k"]), len(a["C"]), np.asarray(a["L"], float), np.asarray(a["H"], float))
        nt = {"G1": f"mavi gel-git: kapanış ort. {sb['d_G1_ort']:.2f} (<= -0,30), yön değişimi {int(sb['d_G1_degisim'])} (>= 2)",
              "G2": f"yeşil ok: yeşil mum, önceki kapanış {sb['d_G2_onceki']:.2f} (< 0), sonra SMA üstü %{100 * sb['d_G2_ust']:.0f} (>= %80)",
              "T": f"turuncu tırmanış: sıra korelasyonu {sb['d_T_spearman']:.2f} (>= 0,50), son kapanış {sb['d_T_son']:.2f} (>= 0,60)",
              "I": f"içeriden: kapanışların %{100 * sb['d_I_pay']:.0f}'i üst bandın içinde (>= %60)",
              "B": f"küçük mum: en büyük gövde {sb['d_B_max']:.2f} (<= 0,90), medyan {sb['d_B_med']:.2f} (<= 0,30) (bant yarı genişliği = 1)",
              "F": f"fitil: üst fitili uzun mum payı %{100 * sb['d_F_pay']:.0f} (>= %50)", "S": f"eski benzerlik puanı {sb['d_S']:.2f} (>= 0,59)",
              "M": f"mum yapısı (bütün mumlar): gövde {sb['d_m1']:.2f} (<= 0,45) · alt fitil {sb['d_m2']:.2f} (<= 0,25)\n"
                   f"      üst fitil {sb['d_m3']:.2f} (>= 0,33) · üst / alt {sb['d_m4']:.1f} (>= 1,5)"}
        fig.text(0.08, 0.33, _v5_virgul("\n".join(nt[p] for p in v5_liste(kural) if p in nt)), fontsize=10.5, va="top")
        fig.text(0.08, 0.95, "Mavi = gel-git kısmı, yeşil ok = SMA'yı aşan mum, turuncu = tırmanış kısmı", fontsize=12, weight="bold")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["sayfa"]):
            kk = (r["zaman"], r["pazar"])
            if kk not in Vc:
                Vc[kk] = MV.mv_veri(*kk)
            d = Vc[kk][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); i0 = max(0, t - m + 1 - once)
            BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
            O_, H_, L_, C_ = (d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close"))
            P = v5_parcalar(*(x[None, t - m + 1 - i0:] for x in (O_, H_, L_, C_, BU[sl], BO[sl])))
            if int(P["k"][0]) != int(r["k"]) or (not bool(v5_kural(P, kural)[0]) and "S" not in v5_liste(kural)):
                raise V5Hata(f"sayfa {r['sayfa']}: okuma tarama ile uyuşmuyor")
            fig = plt.figure(figsize=(8.3, 11.7))
            MV._mv_ciz(fig.add_axes([0.04, 0.66, 0.26, 0.22]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
            ax = fig.add_axes([0.34, 0.42, 0.63, 0.5])
            MV._mv_ciz(ax, O_, H_, L_, C_, BU[sl], BO[sl], BA[sl], None, f"Sayfa {r['sayfa']}: kodun okuması ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            _v5_okuma_ciz(ax, t - m + 1 - i0, int(r["k"]), m, L_, H_)
            fig.text(0.34, 0.405, _v5_m_metin(P), fontsize=10)
            fig.text(0.04, 0.6, "Mavi = gel-git\nYeşil ok = SMA'yı\naşan mum\nTuruncu = tırmanış\nMor = Bollinger 20\nve SMA20 (kesik)\nSağ kenar = bölge sonu\n(sonrası yok)",
                     fontsize=9.5, va="top")
            ax2 = fig.add_axes([0.1, 0.12, 0.8, 0.22]); ax2.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
                ax2.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax2.transAxes))
                ax2.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax2.transAxes)
            fig.text(0.1, 0.36, "Yanlış okunan parçayı daire içine al.", fontsize=12)
            pdf.savefig(fig); plt.close(fig)
    MI._mi_jyaz(ya, {"not": "MÜHÜRLÜ: sayfa -> hisse / tarih / m / k / v1 S; PDF'e girmez", "kural": kural, "sayfalar": sec}, "anahtar 8")
    J = {"surum": V5_SURUM, "kural": JT["kural"], "nihai": kural, "aday": {k: AJ[k] for k in ("tablo", "secim", "nihai", "M_gecme", "M_deger", "capraz", "sablon",
                                                                                           "parca_gecme")},
         "sentetik_secilen": json.load(open(_v5_yol("sentetik", cikti), encoding="utf-8")), "sentetik_v5m": SM,
         "tarama": {k: JT[k] for k in ("sayim", "n_secim", "secim_sayim", "uygun_olay", "kasa")}, "pdf_sha": MI._mi_sha(y), "anahtar_sha": MI._mi_sha(ya),
         "tekrar_uyumu": tk}
    MI._mi_jyaz(_v5_yol("sonuc", cikti), J, "sonuç 8")
    return y


# ================================================================ 8) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_v5(_once=_CK_ONCE_V5, _dosya="MUM_IZI_V5.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_V5",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_v5()


def _v5_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_V5")
    ap.add_argument("komut", choices=["aday", "sentetik", "sentetik_m", "onkayit", "tarama", "onay"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "aday":
            J = v5_aday(); print(json.dumps(MI._mi_json({k: J[k] for k in ("secim", "capraz")}), ensure_ascii=False))
        elif a.komut in ("sentetik", "sentetik_m"):
            J = v5_sentetik(nihai=a.komut == "sentetik_m"); print(json.dumps(MI._mi_json(J["olcut"]), ensure_ascii=False))
        elif a.komut == "onkayit":
            print(v5_onkayit_yaz())
        elif a.komut == "tarama":
            J = v5_tarama(); print(json.dumps(MI._mi_json(J["sayim"]), ensure_ascii=False))
        elif a.komut == "onay":
            print(v5_onay())
    except V5Hata as ex:
        v5log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_v5_ana())
