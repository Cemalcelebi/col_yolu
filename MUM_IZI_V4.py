"""MUM_IZI_V4 — MUM_IZI EK 7: Cemal'in kapak notundan EVRE KURALI (v4), sentetik, mühürlü etiketlerle sınama, (yalnız UYUMLU ise) evren sayımı ve onay seti
(25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI7_IS_TANIMI.md (commit 2e79fa3; ana model). Cemal'in notu (etiket seti 2 kapağı, ana model okuması): "SMA'nın alt
bandında bir-iki gel-git (yükseliş-düşüş şeklinde); sonrasında yeşil mumla SMA'nın orta bandını aşarak çıkış; ama üst banda İÇERİDEN, boncuk gibi küçük
küçük mumlarla düzenli tırmanış; ve mumların çoğunda üst fitil uzun."

Dört parça (b = (fiyat - SMA20) / (üst bant - SMA20); her mum kendi gününe kadarki bantla; bölge 16-24 mum):
  E1 alt bantta gel-git, E2 yeşil mumla orta bandı aşma (kalıcı), E3 üst banda içeriden boncuk gibi düzenli tırmanış, E4 çoğu mumda uzun üst fitil.
  v4 VAR <=> E1 ve E2 ve E3 ve E4; PUAN4 = parçaların dereceli puanlarının EN KÜÇÜĞÜ (telafi yok). Eşik sayıları iş tanımında SABİT.

MÜHÜR: etiket dosyaları, işaretli PDF'ler, mum_izi6 olc çıktıları ve mum_izi5_sinama.csv ön kayıt (MUM_IZI7_ON_KAYIT.md) commit edilene kadar açılmaz;
sınamadan sonra tanım değişmez (fikir = 'ÖNERİ'). GETİRİ / SONRASI YOK. Eski kodlar değişmez (içe alınır). Veri <= 2022-12-31; KASA açılmaz.

Komut:  python MUM_IZI_V4.py sablon      şablonun dört parçadaki değerleri (geçmezse DUR)
        python MUM_IZI_V4.py sentetik    B: pozitif + n1-n8 + rastgele (mum_izi7_sentetik.json)
        python MUM_IZI_V4.py onkayit     MUM_IZI7_ON_KAYIT.md
        python MUM_IZI_V4.py sinama      C: kapı -> etiketler -> kappa / AUC / parça düşüşleri (mum_izi7_sinama.csv, mum_izi7_sonuc.json)
        python MUM_IZI_V4.py tarama      D (yalnız C hükmü UYUMLU): evren sayımı + onay seçimi (mum_izi7_tarama.json)
        python MUM_IZI_V4.py onay        D: MUM_IZI7_ONAY.pdf + mum_izi7_onay_anahtar.json
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_V4 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv4  # noqa: E402
from scipy.stats import rankdata as _rank4  # noqa: E402

KOK_V4 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_V4 not in sys.path:
    sys.path.insert(0, KOK_V4)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_HAFTALIK as MH  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ)
import MUM_IZI_V3 as V3  # noqa: E402  (DEĞİŞTİRİLMEZ)

v4log = logging.getLogger("col.mum_izi_v4")
if not v4log.handlers:
    _v4_h = logging.StreamHandler(sys.stderr)
    _v4_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi_v4: %(message)s", "%H:%M:%S"))
    v4log.addHandler(_v4_h)
    v4log.setLevel(logging.INFO)
    v4log.propagate = False


class V4Hata(RuntimeError):
    """Durdurucu hata: şablon / kapı / mühür / veri / kesik."""


V4_SURUM = "MUM_IZI_V4 v1.0 (2026-11-25): evre kuralı E1-E4 (Cemal'in kapak notu), PUAN4 = en küçük parça puanı"
V4_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_V4, "MUM_IZI_V4.py"), "gecici": "/tmp/mum_izi/v4",
          "isaret1": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi4_onay.json"), "anahtar1": os.path.join(MI.MI_YOL["cikti"], "mum_izi4_onay_anahtar.json"),
          "isaret2": os.path.join(MI.MI_YOL["cikti"], "cemal_mum_izi6_etiket.json"), "anahtar2": os.path.join(MI.MI_YOL["cikti"], "mum_izi6_anahtar.json")}
V4_DOSYA = {"onkayit": "MUM_IZI7_ON_KAYIT.md", "rapor": "MUM_IZI7_RAPOR.md", "sonuc": "mum_izi7_sonuc.json", "sinama": "mum_izi7_sinama.csv",
            "sentetik": "mum_izi7_sentetik.json", "sablon": "mum_izi7_sablon.json", "tarama": "mum_izi7_tarama.json", "onay": "MUM_IZI7_ONAY.pdf",
            "anahtar": "mum_izi7_onay_anahtar.json"}

V4_ESIK: Dict[str, Any] = {
    "surum": "V4-1.0",
    "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20); Bollinger (20, 2; std ddof 0), her mum kendi gününe kadarki barlarla (MI.mi_bant); şablonda "
                 "bantlar görüntüden; üst bant <= SMA olan pencere geçersiz",
    "uzunluklar": [16, 17, 18, 19, 20, 21, 22, 23, 24],
    "yapi": "k = pencerede kapanışı SMA'nın üstünde (bC > 0) olan İLK mumun sırası (0'dan). Ön kısım = 0..k-1, çıkış mumu = k, tırmanış kısmı = k+1..m-1. "
            "Yapı koşulu: böyle bir mum var, 3 <= k <= floor(m / 2) (ön kısım en az 3, en çok bölgenin yarısı), tırmanış kısmı >= 5 mum. Yapı yoksa E1-E3 "
            "YOK ve puanları 0",
    "E1": {"tanim": "ön kısımda bC ortalaması <= -0,3 VE kapanış yönü (sign(C_j - C_j-1), ön kısım içindeki ardışık çiftler) en az 2 kez değişiyor "
                    "(ardışık iki yön çarpımı < 0)", "bC_ort": -0.3, "degisim": 2},
    "E2": {"tanim": "çıkış mumu k yeşil (C > O); önceki kapanış SMA altında (bC_k-1 < 0); tırmanış kısmında kapanışların >= %80'i SMA üstünde (bC > 0)",
           "ust_pay": 0.80},
    "E3": {"tanim": "tırmanış kısmı (k+1..m-1): (a) bölgenin son 3 mumu hariç bu kısmın kapanışlarının >= %80'i 0 < bC <= 1,05; (b) gövde |bC - bO| medyanı "
                    "<= şablonun tırmanış kısmındaki medyanın 1,5 katı VE en büyük gövde <= şablondakinin 1,5 katı; (c) bC'nin sıraya göre Spearman "
                    "korelasyonu (eşitlerde ortalama sıra) >= 0,6 VE bölgenin son kapanışı bC >= 0,6; (d) tırmanış kısmı içindeki ardışık mum çiftlerinin "
                    "örtüşmesi (ortak aralık / küçük mum boyu; MI 'ortusme' tanımı) ortalaması >= şablonun aynı ortalamasının 0,75 katı",
           "icerden_pay": 0.80, "icerden_ust": 1.05, "muaf_son": 3, "govde_kat": 1.5, "spearman": 0.6, "son_bC": 0.6, "ortusme_kat": 0.75},
    "E4": {"tanim": "bölgenin bütün mumlarında uzun üst fitil = üst fitil >= mum boyunun %30'u VE üst fitil > alt fitil; bu mumların payı >= %50",
           "fitil_oran": 0.30, "pay": 0.50},
    "kural": "v4 VAR <=> E1 ve E2 ve E3 ve E4 (ikili koşullar); bir pencere sonunda 16-24 uzunluklarından biri VAR ise o son VAR",
    "puan": {"tanim": "her alt koşul için g = 0,5 + (x - eşik) / (2 s) ('>=' koşulu) ya da 0,5 + (eşik - x) / (2 s) ('<=' koşulu), [0, 1]'e kırpılır; parça "
                      "puanı = alt koşulların en küçüğü; PUAN4 = dört parça puanının en küçüğü (telafi yok); yapı yoksa E1-E3 puanı 0. Eşikte g = 0,5. "
                      "Bir pencere sonunun PUAN4'ü uzunluklar içinde en büyüğü",
             "s": {"E1_bC_ort": 0.3, "E1_degisim": 1.0, "E2_yesil": 0.1, "E2_onceki": 0.1, "E2_ust_pay": 0.2, "E3_icerden": 0.2, "E3_govde_med": 0.5,
                   "E3_govde_max": 0.5, "E3_spearman": 0.4, "E3_son_bC": 0.4, "E3_ortusme": 0.25, "E4_pay": 0.25},
             "not": "E2_yesil x = bC_k - bO_k (eşik 0); E2_onceki x = bC_k-1 (<= 0); ikili VAR kesin eşitsizlik kullandığı için eşitlikte (ölçü sıfır) PUAN4 0,5 "
                    "iken VAR YOK olabilir"},
    "tekil": "aynı hissede VAR sonları birbirine < 15 mum olan zincir = bir olay; olay = kümenin en yüksek PUAN4'lü hizası",
    "sentetik": {"kok": 25112071, "tohum": 200, "gurultu": [0.0, 0.1, 0.2], "baglam": ["dip", "yatay"], "uretec": ["blok", "ry"], "tol": 3,
                 "negatif": {"n1": "fitilsiz büyük gövde (MV n1)", "n2": "fitiller ters (MV n2)", "n3": "mumlar 2 kat (MV n3)", "n5": "aynı mumlar yatay yol (MV p1)",
                             "n6": "V dönüş: ön kısım kapanışları şablonun ilk kapanışından ön kısmın en düşük kapanışına doğrusal (tek yönlü iniş, gel-git yok), "
                                   "sonra 10 mumda şablonun son kapanışına doğrusal sert yükseliş; mum biçimleri şablonun",
                             "n7": "üst bandın dışından yürüyüş: mum 0-10 şablon; 11-19 kapanışları mum başına şablon tırmanışının ortalama adımının 3 katıyla "
                                   "yükselir, mumlar kapanış çevresinde 2 kat",
                             "n8a": "SMA'yı kırmızı mumlu boşlukla aşma: mum 10 kırmızı, açılış kapanışın gövde boyu kadar üstünde (önceki kapanıştan boşluk)",
                             "n8b": "SMA'yı tek dev mumla aşma: mum 10 yeşil, açılış = önceki kapanış, gövde = şablonun en büyük gövdesinin 4 katı; sonraki mumlar "
                                    "aynı fazla kadar yukarı kayar"},
                 "yanlis": {"seri": 200, "n": 1000},
                 "kabul_olcutu": "%10 gürültüde pozitif VAR payı (gerçek sonun +-3 barında VAR) >= %60 (iki bağlam x iki üretici birleşik); her negatifte VAR "
                                 "payı <= %5 (bütün gürültüler birleşik; n8a ve n8b ayrı ayrı); rastgele seride tekil VAR <= 0,3 / 1.000 bar (iki üretici ayrı). "
                                 "Geçmezse yazılır; tanım değişmez",
                 "tani": "her negatif ve pozitif için hangi parçanın kaç kez düştüğü (gerçek son +-3 bar, en yüksek PUAN4'lü pencere) yazılır"},
    "sinama": {"set1": "cemal_mum_izi4_onay.json 'isaret' (EVET / HAYIR) + mum_izi4_onay_anahtar.json (24 sayfa)",
               "set2": "cemal_mum_izi6_etiket.json 'isaret' EVET / HAYIR (IKISI / YOK / BELIRSIZ karar dışı) + mum_izi6_anahtar.json; katman 'T' (tekrar) "
                       "sayfaları set 2'de sayılmaz",
               "pencere": "sayfadaki bölgenin kendisi (aynı uzunluk m, aynı son); v4 VAR / YOK ve PUAN4 o pencerede",
               "kappa": "Cohen kappa (v4 VAR ile Cemal EVET); bootstrap %95 (sayfalar yerine koyarak, B 5000, tohum 25112072; kappa tanımsız örnekler atılır, "
                        "sayısı yazılır); uyum payı; 2x2",
               "auc": "PUAN4 AUC = P(PUAN4 EVET > PUAN4 HAYIR) + 0,5 eşit; bootstrap %95 (grup içi, B 5000, tohum 25112072); tam permütasyon p",
               "ayri": "set 1, set 2, birleşik; günlük / haftalık ayrı (bilgi)",
               "dusus": "Cemal EVET / v4 YOK sayfalarında hangi parça (yapı, E1, E2, E3 ve alt koşulları, E4) kaç kez düştü; Cemal HAYIR / v4 VAR sayısı",
               "bilgi_esnek": "bilgi (hüküm dışı): aynı sayfanın son +-3 barında biten 16-24 uzunluklu pencerelerde en yüksek PUAN4 ve VAR",
               "hukum": "birleşik: v4 VAR sayısı < 5 -> 'kural çok dar: ÖLÇÜLEMEDİ' (AUC yine yazılır); kappa >= 0,60 VE alt uç >= 0,40 -> UYUMLU; değilse "
                        "kappa >= 0,40 -> KISMEN; kappa < 0,40 -> UYUMSUZ",
               "esik": {"var_en_az": 5, "uyumlu": 0.60, "alt_uc": 0.40, "kismen": 0.40}, "B": 5000, "tohum": 25112072},
    "tarama": {"yalniz": "C hükmü UYUMLU", "gunluk": ["2016-01-01", "2022-12-31"], "haftalik": ["2001-01-01", "2022-12-31"],
               "evren": "ABD / AVR P2 (MUM_IZI_ETIKET2.e6_p2_maske; günlük açık kopya, haftalık 2001-15 p1 / 2016-22 açık kopya), BIST işlem değeri aynı gün / "
                        "ISO haftası kesit medyanı üstü; olay sonu barında",
               "sayim": "tekil v4 VAR olay sayısı pazar x zaman dilimi (evren içi ve hepsi)",
               "onay": {"tohum": 25112073, "gunluk": 12, "haftalik": 12, "secim": "evren içi tekil VAR olaylarından RASTGELE; hisse başına bir; önceki iki setin "
                                                                                   "hisseleri hariç; sayfa sırası karışık", "esik": "24'ün >= 19'u ✓"}},
}

V4_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "negatifler sentetikte sayıyla (n1, n2, n3, n5, n6, n7, n8a, n8b + rastgele seri), kabul ölçütü önceden; sınamada kappa bootstrap ve AUC "
                   "permütasyonu; getiri / eş yok"),
    "K2": ("EVET", "b her mumun kendi gününe kadarki bantla; v4_tara_seri sonu t olan pencerede yalnız <= t barları kullanır (test: seri t'de kesilince aynı); "
                   "veri <= 2022-12-31 + KASA kapısı (tarama); etiketler ön kayıt commit'inden sonra açılır"),
    "K3": ("EVET", "MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (V3 kuralı); BIST işlem değeri kesit medyanı üstü; ABD / AVR P2"),
    "K4": ("EVET", "tekil: < 15 mum zincir = bir olay, en yüksek PUAN4; sınamada tekrar sayfaları set 2'de sayılmaz (çift sayım yok)"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok"),
    "K6": ("EVET", "b birimi ölçek bağımsız; örtüşme ve fitil oranları oransal"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; sayım ve görsel onay (getiri yok)"),
    "K8": ("EVET", "set 1 24 + set 2 (tekrar hariç) karar sayfaları; v4 VAR < 5 ise ÖLÇÜLEMEDİ; aralıklar raporda"),
    "K9": ("EVET", "MUM_IZI7_ON_KAYIT.md: KOD7_SHA, ESIK7_SHA, SABLON7_SHA, SENTETIK7_SHA + eski kod sha'ları; v4_kapi (kontrol + sha + git) sınama ve tarama "
                   "öncesi"),
    "K10": ("EVET", "sayfa pencereleri anahtarlardan (hisse / son / m / zaman); set 1 sayfalarında v1 S anahtardaki S ile aynı (denetim); etiket şeması "
                    "('isaret' EVET / HAYIR / YOK / IKISI / BELIRSIZ) bilinmeyen değerde DUR"),
    "K11": ("EVET", "v4_duz: tek pencerede E1-E4 ve PUAN4 düz döngüyle yeniden; test ve sınamada vektörlü sonuçla aynı"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı kappa eşikleriyle; commit mesajında etiket-sayfa eşlemesi yok; 'iz' sözü yok"),
    "K13": ("EVET", "çakışma kapısı; eski kodlar / defterler / UC_IZ2 / başka ajanın mum_izi6 olc dosyaları değişmez, git add edilmez"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 0) YARDIMCI
def _v4_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or V4_YOL["cikti"], V4_DOSYA[ad])


def v4_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or V4_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _g_ge(x, esik: float, s: float):
    return np.clip(0.5 + (np.asarray(x, float) - esik) / (2 * s), 0.0, 1.0)


def _g_le(x, esik: float, s: float):
    return np.clip(0.5 + (esik - np.asarray(x, float)) / (2 * s), 0.0, 1.0)


_V4_ALT = ["E1_bC_ort", "E1_degisim", "E2_yesil", "E2_onceki", "E2_ust_pay", "E3_icerden", "E3_govde_med", "E3_govde_max", "E3_spearman", "E3_son_bC",
           "E3_ortusme", "E4_pay"]


# ================================================================ 1) v4 KURALI (vektörlü)
def v4_pencereler(O, H, L, C, BU, BO, ref: Optional[Dict[str, float]] = None) -> Dict[str, np.ndarray]:
    """(N, m) pencereler -> VAR, PUAN4, parça bayrakları / puanları, alt koşul değerleri. ref: şablonun tırmanış kısmı gövde medyanı / en büyüğü / örtüşmesi."""
    O, H, L, C, BU, BO = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BO)]
    N, m = C.shape; ref = ref or V4_REF; E = V4_ESIK; s = E["puan"]["s"]
    d = BU - BO; gec = (d > 0).all(1) & np.isfinite(d).all(1) & np.isfinite(C).all(1); dd = np.where(d > 0, d, 1.0)
    bO, bC = (O - BO) / dd, (C - BO) / dd
    pos = bC > 0; var_ = pos.any(1); k = np.where(var_, np.argmax(pos, 1), -1)
    yapi = gec & var_ & (k >= 3) & (k <= m // 2) & (m - 1 - k >= 5)
    deg = {a: np.full(N, np.nan) for a in _V4_ALT}; gp = {a: np.zeros(N) for a in _V4_ALT}
    for kk in np.unique(k[yapi]):
        i = np.flatnonzero(yapi & (k == kk)); kk = int(kk)
        Ci, Oi, Hi, Li, bCi, bOi = C[i], O[i], H[i], L[i], bC[i], bO[i]
        deg["E1_bC_ort"][i] = bCi[:, :kk].mean(1)
        yon = np.sign(np.diff(Ci[:, :kk], axis=1)); deg["E1_degisim"][i] = (yon[:, 1:] * yon[:, :-1] < 0).sum(1)
        deg["E2_yesil"][i] = bCi[:, kk] - bOi[:, kk]; deg["E2_onceki"][i] = bCi[:, kk - 1]
        po = slice(kk + 1, m); deg["E2_ust_pay"][i] = (bCi[:, po] > 0).mean(1)
        ev = slice(kk + 1, m - int(E["E3"]["muaf_son"]))
        deg["E3_icerden"][i] = ((bCi[:, ev] > 0) & (bCi[:, ev] <= E["E3"]["icerden_ust"])).mean(1)
        gv = np.abs(bCi[:, po] - bOi[:, po]); deg["E3_govde_med"][i] = np.median(gv, 1) / ref["govde_med"]; deg["E3_govde_max"][i] = gv.max(1) / ref["govde_max"]
        y = bCi[:, po]; r = _rank4(y, axis=1); x = np.arange(y.shape[1], dtype=float)
        rc = r - r.mean(1, keepdims=True); xc = x - x.mean(); den = np.sqrt((rc ** 2).sum(1) * (xc ** 2).sum())
        deg["E3_spearman"][i] = np.where(den > 0, (rc * xc).sum(1) / np.where(den > 0, den, 1.0), 0.0)
        deg["E3_son_bC"][i] = bCi[:, m - 1]
        Hp, Lp = Hi[:, kk + 1:], Li[:, kk + 1:]; rg = np.maximum(Hp - Lp, 1e-12)
        ort = np.maximum(np.minimum(Hp[:, 1:], Hp[:, :-1]) - np.maximum(Lp[:, 1:], Lp[:, :-1]), 0.0) / np.minimum(rg[:, 1:], rg[:, :-1])
        deg["E3_ortusme"][i] = ort.mean(1) / ref["ortusme"]
    rgt = np.maximum(H - L, 1e-12); uw = H - np.maximum(O, C); lw = np.minimum(O, C) - L
    deg["E4_pay"] = np.where(gec, ((uw >= E["E4"]["fitil_oran"] * rgt) & (uw > lw)).mean(1), np.nan)
    b = {"E1_bC_ort": deg["E1_bC_ort"] <= E["E1"]["bC_ort"], "E1_degisim": deg["E1_degisim"] >= E["E1"]["degisim"], "E2_yesil": deg["E2_yesil"] > 0,
         "E2_onceki": deg["E2_onceki"] < 0, "E2_ust_pay": deg["E2_ust_pay"] >= E["E2"]["ust_pay"], "E3_icerden": deg["E3_icerden"] >= E["E3"]["icerden_pay"],
         "E3_govde_med": deg["E3_govde_med"] <= E["E3"]["govde_kat"], "E3_govde_max": deg["E3_govde_max"] <= E["E3"]["govde_kat"],
         "E3_spearman": deg["E3_spearman"] >= E["E3"]["spearman"], "E3_son_bC": deg["E3_son_bC"] >= E["E3"]["son_bC"],
         "E3_ortusme": deg["E3_ortusme"] >= E["E3"]["ortusme_kat"], "E4_pay": deg["E4_pay"] >= E["E4"]["pay"]}
    for a in _V4_ALT:
        b[a] = np.nan_to_num(b[a].astype(float), nan=0.0).astype(bool) & (yapi if not a.startswith("E4") else gec)
    gp["E1_bC_ort"] = _g_le(deg["E1_bC_ort"], E["E1"]["bC_ort"], s["E1_bC_ort"]); gp["E1_degisim"] = _g_ge(deg["E1_degisim"], E["E1"]["degisim"], s["E1_degisim"])
    gp["E2_yesil"] = _g_ge(deg["E2_yesil"], 0.0, s["E2_yesil"]); gp["E2_onceki"] = _g_le(deg["E2_onceki"], 0.0, s["E2_onceki"])
    gp["E2_ust_pay"] = _g_ge(deg["E2_ust_pay"], E["E2"]["ust_pay"], s["E2_ust_pay"]); gp["E3_icerden"] = _g_ge(deg["E3_icerden"], E["E3"]["icerden_pay"], s["E3_icerden"])
    gp["E3_govde_med"] = _g_le(deg["E3_govde_med"], E["E3"]["govde_kat"], s["E3_govde_med"])
    gp["E3_govde_max"] = _g_le(deg["E3_govde_max"], E["E3"]["govde_kat"], s["E3_govde_max"])
    gp["E3_spearman"] = _g_ge(deg["E3_spearman"], E["E3"]["spearman"], s["E3_spearman"]); gp["E3_son_bC"] = _g_ge(deg["E3_son_bC"], E["E3"]["son_bC"], s["E3_son_bC"])
    gp["E3_ortusme"] = _g_ge(deg["E3_ortusme"], E["E3"]["ortusme_kat"], s["E3_ortusme"]); gp["E4_pay"] = _g_ge(deg["E4_pay"], E["E4"]["pay"], s["E4_pay"])
    for a in _V4_ALT:
        gp[a] = np.where(np.isfinite(gp[a]), gp[a], 0.0)
    P = {e: np.min(np.stack([gp[a] for a in _V4_ALT if a.startswith(e)]), 0) for e in ("E1", "E2", "E3", "E4")}
    F = {e: np.all(np.stack([b[a] for a in _V4_ALT if a.startswith(e)]), 0) for e in ("E1", "E2", "E3", "E4")}
    VAR = F["E1"] & F["E2"] & F["E3"] & F["E4"]; PUAN = np.min(np.stack([P[e] for e in ("E1", "E2", "E3", "E4")]), 0)
    return {"VAR": VAR, "PUAN4": PUAN, "yapi": yapi, "gecerli": gec, "k": k, **{f"{e}": F[e] for e in F}, **{f"p_{e}": P[e] for e in P},
            **{f"d_{a}": deg[a] for a in _V4_ALT}, **{f"b_{a}": b[a] for a in _V4_ALT}}


def _v4_ref_hesap() -> Dict[str, float]:
    """Şablonun tırmanış kısmı referansları (k şablonun kendi yapısından)."""
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]; O, H, L, C, BU, BO = (np.asarray(a[x], float) for x in ("O", "H", "L", "C", "BU", "BO"))
    bC = (C - BO) / (BU - BO); bO = (O - BO) / (BU - BO); k = int(np.argmax(bC > 0)); m = len(C)
    gv = np.abs(bC - bO)[k + 1:]; Hp, Lp = H[k + 1:], L[k + 1:]; rg = Hp - Lp
    ort = np.maximum(np.minimum(Hp[1:], Hp[:-1]) - np.maximum(Lp[1:], Lp[:-1]), 0.0) / np.minimum(rg[1:], rg[:-1])
    return {"k": k, "m": m, "govde_med": float(np.median(gv)), "govde_max": float(gv.max()), "ortusme": float(ort.mean())}


V4_REF: Dict[str, float] = _v4_ref_hesap()


def v4_sablon_denetim() -> Dict[str, Any]:
    """Şablon dört parçadan geçmeli; geçmezse DUR (eşik değişmez)."""
    a = MI.mi_sablon_yukle(kalibre=False)["tam"]["ohlc"]
    R = v4_pencereler(a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"])
    out = {"ref": V4_REF, "k": int(R["k"][0]), "VAR": bool(R["VAR"][0]), "PUAN4": float(R["PUAN4"][0]), **{e: bool(R[e][0]) for e in ("E1", "E2", "E3", "E4")},
           **{f"p_{e}": float(R[f"p_{e}"][0]) for e in ("E1", "E2", "E3", "E4")}, "deger": {x: float(R[f"d_{x}"][0]) for x in _V4_ALT},
           "alt_gecti": {x: bool(R[f"b_{x}"][0]) for x in _V4_ALT}}
    if not out["VAR"]:
        raise V4Hata(f"ŞABLON GEÇMEDİ: {[x for x, v in out['alt_gecti'].items() if not v]} -> DUR (eşik değiştirilmez; ana model karar verir)")
    return out


def v4_duz(W: Dict[str, np.ndarray]) -> Dict[str, Any]:
    """K11: tek pencerede E1-E4 düz döngüyle (vektörsüz)."""
    O, H, L, C, BU, BO = (list(map(float, W[x])) for x in ("O", "H", "L", "C", "BU", "BO")); m = len(C); E = V4_ESIK; ref = V4_REF
    if any(BU[i] - BO[i] <= 0 for i in range(m)):
        return {"VAR": False}
    bC = [(C[i] - BO[i]) / (BU[i] - BO[i]) for i in range(m)]; bO = [(O[i] - BO[i]) / (BU[i] - BO[i]) for i in range(m)]
    k = next((i for i in range(m) if bC[i] > 0), None)
    uz = 0
    for i in range(m):
        r = max(H[i] - L[i], 1e-12); u = H[i] - max(O[i], C[i]); lo = min(O[i], C[i]) - L[i]
        uz += 1 if (u >= E["E4"]["fitil_oran"] * r and u > lo) else 0
    e4 = uz / m >= E["E4"]["pay"]
    if k is None or k < 3 or k > m // 2 or m - 1 - k < 5:
        return {"VAR": False, "E4": e4, "yapi": False}
    ort_bc = sum(bC[:k]) / k; yon = [np.sign(C[j] - C[j - 1]) for j in range(1, k)]; dg = sum(1 for j in range(1, len(yon)) if yon[j] * yon[j - 1] < 0)
    e1 = ort_bc <= E["E1"]["bC_ort"] and dg >= E["E1"]["degisim"]
    po = list(range(k + 1, m)); e2 = C[k] > O[k] and bC[k] - bO[k] > 0 and bC[k - 1] < 0 and sum(1 for j in po if bC[j] > 0) / len(po) >= E["E2"]["ust_pay"]
    ev = [j for j in po if j <= m - 1 - E["E3"]["muaf_son"]]; ic = sum(1 for j in ev if 0 < bC[j] <= E["E3"]["icerden_ust"]) / len(ev)
    gv = sorted(abs(bC[j] - bO[j]) for j in po); n = len(gv); med = gv[n // 2] if n % 2 else (gv[n // 2 - 1] + gv[n // 2]) / 2
    rk = _rank4([bC[j] for j in po]); xs = list(range(n)); mr = sum(rk) / n; mx = sum(xs) / n
    sp = sum((rk[i] - mr) * (xs[i] - mx) for i in range(n)) / ((sum((rk[i] - mr) ** 2 for i in range(n)) * sum((xs[i] - mx) ** 2 for i in range(n))) ** 0.5)
    ov = []
    for j in range(k + 2, m):
        a_ = max(min(H[j], H[j - 1]) - max(L[j], L[j - 1]), 0.0); ov.append(a_ / min(max(H[j] - L[j], 1e-12), max(H[j - 1] - L[j - 1], 1e-12)))
    e3 = (ic >= E["E3"]["icerden_pay"] and med / ref["govde_med"] <= E["E3"]["govde_kat"] and gv[-1] / ref["govde_max"] <= E["E3"]["govde_kat"]
          and sp >= E["E3"]["spearman"] and bC[m - 1] >= E["E3"]["son_bC"] and (sum(ov) / len(ov)) / ref["ortusme"] >= E["E3"]["ortusme_kat"])
    return {"VAR": bool(e1 and e2 and e3 and e4), "E1": bool(e1), "E2": bool(e2), "E3": bool(e3), "E4": bool(e4), "yapi": True, "k": k}


# ================================================================ 2) SERİ TARAMASI
def v4_tara_seri(O, H, L, C, bosluk: Optional[np.ndarray] = None, sonlar: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Her pencere sonu (ya da yalnız 'sonlar'): uzunluklar içinde VAR (herhangi), en yüksek PUAN4 ve uzunluğu, o penceredeki parça bayrakları."""
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C)); T = len(C); BU, BO, _ = MI.mi_bant(C); s0 = 19
    bc = np.r_[0, np.cumsum(bosluk.astype(np.int64))] if bosluk is not None else None
    out = {"VAR": np.zeros(T, bool), "PUAN4": np.full(T, np.nan), "m": np.zeros(T, np.int64)}
    for e_ in ("E1", "E2", "E3", "E4", "yapi"):
        out[e_] = np.zeros(T, bool)
    for m in V4_ESIK["uzunluklar"]:
        e = np.arange(s0 + m - 1, T)
        if sonlar is not None:
            e = np.intersect1d(e, np.asarray(sonlar, np.int64))
        if not len(e):
            continue
        if bc is not None:
            e = e[(bc[e + 1] - bc[e - m + 2]) == 0]
            if not len(e):
                continue
        idx = (e - m + 1)[:, None] + np.arange(m)[None, :]
        R = v4_pencereler(O[idx], H[idx], L[idx], C[idx], BU[idx], BO[idx])
        out["VAR"][e] |= R["VAR"]
        iy = ~(R["PUAN4"] <= out["PUAN4"][e]) & np.isfinite(R["PUAN4"])
        ee = e[iy]; out["PUAN4"][ee] = R["PUAN4"][iy]; out["m"][ee] = m
        for e_ in ("E1", "E2", "E3", "E4", "yapi"):
            out[e_][ee] = R[e_][iy]
    return out


def v4_tekil(e: np.ndarray, puan: np.ndarray, aralik: int = 15) -> np.ndarray:
    """Sıralı VAR sonları: ardışık fark < aralik zinciri bir küme; kümenin en yüksek PUAN4'lü sonu."""
    if not len(e):
        return np.asarray(e, np.int64)
    e = np.sort(np.asarray(e, np.int64)); kir = np.flatnonzero(np.diff(e) >= aralik) + 1
    return np.array([int(g[np.argmax(puan[g])]) for g in np.split(e, kir)], np.int64)


# ================================================================ 3) SENTETİK (B)
def v4_karsi() -> Dict[str, Dict[str, np.ndarray]]:
    s = MI.mi_sablon_yukle()["tam"]; a = s["ohlc"]; O, H, L, C = (np.asarray(a[x], float) for x in ("O", "H", "L", "C"))
    k = int(V4_REF["k"]); m = len(C); K = MV.mv_karsi_ornek(s); out = {"n1": K["n1"], "n2": K["n2"], "n3": K["n3"], "n5": K["p1"]}

    def bicim(Cn):
        return {"O": Cn + (O - C), "H": Cn + (H - C), "L": Cn + (L - C), "C": Cn.copy()}
    dip = float(C[:k].min()); Cn = np.r_[np.linspace(C[0], dip, k), np.linspace(dip, C[-1], m - k + 1)[1:]]
    out["n6"] = bicim(Cn)
    adim = float(np.mean(np.diff(C[k:]))); C7 = C.copy(); C7[k + 1:] = C[k] + 3 * adim * np.arange(1, m - k)
    out["n7"] = {"O": C7 + 2 * (O - C), "H": C7 + 2 * (H - C), "L": C7 + 2 * (L - C), "C": C7}
    O8 = O.copy(); H8 = H.copy(); L8 = L.copy(); gb = abs(C[k] - O[k]); uw = H[k] - max(O[k], C[k]); lw = min(O[k], C[k]) - L[k]
    O8[k] = C[k] + gb; H8[k] = O8[k] + uw; L8[k] = C[k] - lw
    out["n8a"] = {"O": O8, "H": H8, "L": L8, "C": C.copy()}
    gmax = float(np.max(np.abs(C - O))); C9 = C.copy(); O9 = O.copy(); H9 = H.copy(); L9 = L.copy()
    yeni = C[k - 1] + 4 * gmax; faz = yeni - C[k]; O9[k] = C[k - 1]; C9[k] = yeni; H9[k] = yeni + (H[k] - max(O[k], C[k])); L9[k] = C[k - 1] - (min(O[k], C[k]) - L[k])
    for x, y in ((O9, O), (H9, H), (L9, L), (C9, C)):
        x[k + 1:] = y[k + 1:] + faz
    out["n8b"] = {"O": O9, "H": H9, "L": L9, "C": C9}
    return out


def _v4_sent_isci(arg: Tuple[str, int, int, int, int, float, int]) -> Dict[str, Any]:
    tur, ti, ui, bi, t, gr, _ = arg; Sn = V4_ESIK["sentetik"]; G = _V4_SENT
    rng = np.random.default_rng([int(Sn["kok"]), ti, ui, bi, int(round(gr * 100)), t])
    X = V3.v3_seri(rng, G["havuz"], G["ohlc"][tur], Sn["uretec"][ui], Sn["baglam"][bi], float(gr))
    tol = int(Sn["tol"]); son = np.arange(X["e"] - tol, X["e"] + tol + 1)
    R = v4_tara_seri(X["O"], X["H"], X["L"], X["C"], sonlar=son)
    j = son[np.nanargmax(np.where(np.isfinite(R["PUAN4"][son]), R["PUAN4"][son], -1))]
    return {"tur": tur, "uretec": Sn["uretec"][ui], "baglam": Sn["baglam"][bi], "gurultu": gr, "VAR": bool(R["VAR"][son].any()),
            "PUAN4": float(np.nanmax(R["PUAN4"][son])) if np.isfinite(R["PUAN4"][son]).any() else 0.0,
            **{e: bool(R[e][j]) for e in ("yapi", "E1", "E2", "E3", "E4")}}


def _v4_yanlis_isci(arg: Tuple[int, int]) -> Tuple[int, int]:
    ui, t = arg; Sn = V4_ESIK["sentetik"]; rng = np.random.default_rng([int(Sn["kok"]), 99, ui, t])
    lO, lH, lL, lC = MI.mi_uret(rng, int(Sn["yanlis"]["n"]) + 60, _V4_SENT["havuz"], Sn["uretec"][ui])
    R = v4_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC))
    n = int(np.isfinite(R["PUAN4"]).sum()); e = np.flatnonzero(R["VAR"])
    return n, int(len(v4_tekil(e, np.nan_to_num(R["PUAN4"], nan=-1))))


_V4_SENT: Dict[str, Any] = {}


def v4_sentetik(cikti: Optional[str] = None, islem: int = 4) -> Dict[str, Any]:
    import multiprocessing as mp
    t0 = time.time(); cikti = cikti or V4_YOL["cikti"]; Sn = V4_ESIK["sentetik"]
    a = MI.mi_sablon_yukle()["tam"]["ohlc"]; K = v4_karsi(); ohlc = {"poz": {x: a[x] for x in ("O", "H", "L", "C")}, **{n: K[n] for n in K}}
    _V4_SENT.clear(); _V4_SENT.update({"havuz": pd.read_pickle(os.path.join(MI.MI_YOL["gecici"], MI.MI_DOSYA["havuz"])), "ohlc": ohlc})
    turler = ["poz", "n1", "n2", "n3", "n5", "n6", "n7", "n8a", "n8b"]
    isler = [(tur, ti, ui, bi, t, gr, 0) for ti, tur in enumerate(turler) for ui in range(len(Sn["uretec"])) for bi in range(len(Sn["baglam"]))
             for gr in Sn["gurultu"] for t in range(int(Sn["tohum"]))]
    try:
        with mp.get_context("fork").Pool(islem) as pool:
            R = list(pool.imap(_v4_sent_isci, isler, chunksize=64))
            Y = list(pool.imap(_v4_yanlis_isci, [(ui, t) for ui in range(len(Sn["uretec"])) for t in range(int(Sn["yanlis"]["seri"]))], chunksize=8))
    finally:
        _V4_SENT.clear()
    D = pd.DataFrame(R); out: Dict[str, Any] = {"surum": V4_SURUM}
    for tur, g in D.groupby("tur", sort=False):
        out[tur] = {"VAR": float(g.VAR.mean()), "n": int(len(g)), "PUAN4_med": float(g.PUAN4.median()),
                    "gurultu": {f"{x:.1f}": float(h.VAR.mean()) for x, h in g.groupby("gurultu")}, "baglam": {x: float(h.VAR.mean()) for x, h in g.groupby("baglam")},
                    "uretec": {x: float(h.VAR.mean()) for x, h in g.groupby("uretec")},
                    "parca_gecti": {e: float(g[e].mean()) for e in ("yapi", "E1", "E2", "E3", "E4")}}
    ny = len(Sn["uretec"]); T = int(Sn["yanlis"]["seri"])
    out["rastgele"] = {Sn["uretec"][ui]: {"n_bar": int(sum(y[0] for y in Y[ui * T:(ui + 1) * T])), "tekil": int(sum(y[1] for y in Y[ui * T:(ui + 1) * T]))}
                       for ui in range(ny)}
    for v in out["rastgele"].values():
        v["VAR_1000"] = 1000.0 * v["tekil"] / max(v["n_bar"], 1)
    neg = ["n1", "n2", "n3", "n5", "n6", "n7", "n8a", "n8b"]
    out["olcut"] = {"poz_g10_ge_60": bool(out["poz"]["gurultu"]["0.1"] >= 0.60), "neg_le_5": {n: bool(out[n]["VAR"] <= 0.05) for n in neg},
                    "rastgele_le_03": {k: bool(v["VAR_1000"] <= 0.3) for k, v in out["rastgele"].items()}}
    out["olcut"]["gecti"] = out["olcut"]["poz_g10_ge_60"] and all(out["olcut"]["neg_le_5"].values()) and all(out["olcut"]["rastgele_le_03"].values())
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_v4_yol("sentetik", cikti), out, "sentetik 7")
    return out


# ================================================================ 4) KAPI ve ÖN KAYIT
def v4_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD7_SHA": MI._mi_sha(V4_YOL["kod"]), "ESIK7_SHA": v4_esik_sha(), "SABLON7_SHA": MI._mi_sha(_v4_yol("sablon", cikti)),
            "SENTETIK7_SHA": MI._mi_sha(_v4_yol("sentetik", cikti)), "V3_KOD_SHA": MI._mi_sha(V3.V3_YOL["kod"]), "MI_KOD_SHA": MI._mi_sha(MI.MI_YOL["kod"]),
            "MH_KOD_SHA": MI._mi_sha(MH.MH_YOL["kod"]), "MV_KOD_SHA": MI._mi_sha(MV.MV_YOL["kod"]),
            "E6_KOD_SHA": MI._mi_sha(os.path.join(KOK_V4, "MUM_IZI_ETIKET2.py"))}


def v4_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or V4_YOL["cikti"]; yol = _v4_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise V4Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = v4_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise V4Hata(f"ön kayıt kapısı: {ad} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_V4); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise V4Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI_V4.py", "MUM_IZI_V3.py", "MUM_IZI.py", "MUM_IZI_HAFTALIK.py", "MUM_IZI_V2.py", "MUM_IZI_ETIKET2.py",
                   os.path.relpath(_v4_yol("sablon", cikti), KOK_V4), os.path.relpath(_v4_yol("sentetik", cikti), KOK_V4)]):
        raise V4Hata("ön kayıt / kod / şablon / sentetik çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def v4_onkayit_yaz(cikti: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or V4_YOL["cikti"]; y = _v4_yol("onkayit", cikti)
    if os.path.exists(y):
        raise V4Hata("ön kayıt zaten var")
    sh = v4_sha_simdi(cikti); SB = json.load(open(_v4_yol("sablon", cikti), encoding="utf-8")); SJ = json.load(open(_v4_yol("sentetik", cikti), encoding="utf-8"))
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    kt = "\n".join(["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"] + [f"| {k} | {ad.get(k, k)} | {a} | {b} |" for k, (a, b) in V4_KONTROL.items()])
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI_V4.py"])
    neg = ["n1", "n2", "n3", "n5", "n6", "n7", "n8a", "n8b"]
    s = [f"# MUM_IZI7 ÖN KAYIT ({MI._mi_simdi()})", "",
         "v4 yalnız Cemal'in kapak notundan, şablonun kendi mumlarından ve sentetikten kuruldu. Etiket dosyaları (set 1, set 2), işaretli PDF'ler, mum_izi6 "
         "olc çıktıları ve mum_izi5_sinama.csv bu dosya commit edilene kadar AÇILMADI. Sınama (C) bu commit'ten sonra; sonra tanım değişmez.", "",
         "## Mühürler", "", *[f"{k}: {v}" for k, v in sh.items()], "", f"- MUM_IZI_V4.py commit'i: {kc or 'yok'}", "",
         "## Şablonun dört parçadaki değerleri (mum_izi7_sablon.json)", "",
         f"- Yapı: k = {SB['k']} (ilk SMA üstü kapanış; ön kısım {SB['k']} mum = floor(20 / 2) SINIRDA), tırmanış kısmı {20 - 1 - SB['k']} mum.",
         f"- Değerler: {json.dumps({k: round(v, 4) for k, v in SB['deger'].items()}, ensure_ascii=False)}",
         f"- Parçalar: E1 {SB['E1']}, E2 {SB['E2']}, E3 {SB['E3']}, E4 {SB['E4']}; VAR {SB['VAR']}; parça puanları "
         f"{ {e: round(SB['p_' + e], 3) for e in ('E1', 'E2', 'E3', 'E4')} }; PUAN4 {SB['PUAN4']:.3f}",
         f"- Referanslar (tırmanış kısmı): gövde medyanı {SB['ref']['govde_med']:.4f}, en büyük gövde {SB['ref']['govde_max']:.4f} (b birimi), ardışık örtüşme "
         f"{SB['ref']['ortusme']:.4f}.",
         "- Sınırdaki değerler: E4 uzun üst fitil payı şablonda tam %50 (10 / 20; eşik %50): şablon geçiyor ama sınırda (PUAN4 0,5). k = 10 = floor(m / 2) sınırda.", "",
         "## v4 tanımı (V4_ESIK; sha yukarıda)", "", "```", json.dumps(V4_ESIK, ensure_ascii=False, indent=1), "```", "",
         "## Sentetik (B; etiketlerden bağımsız)", "",
         f"- pozitif VAR payı: {SJ['poz']['gurultu']} (bağlam {SJ['poz']['baglam']}; parça geçme payları {SJ['poz']['parca_gecti']})",
         *[f"- {n}: VAR {100 * SJ[n]['VAR']:.1f} % (parça geçme payları {SJ[n]['parca_gecti']})" for n in neg],
         f"- rastgele: {SJ['rastgele']}", f"- KABUL ÖLÇÜTÜ: {'GEÇTİ' if SJ['olcut']['gecti'] else 'GEÇMEDİ'} {SJ['olcut']}", "",
         "## KONTROL LİSTESİ", "", kt, "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 7")


# ================================================================ 5) ETİKETLERLE SINAMA (C)
_V4_DEGER = {"EVET": 1, "HAYIR": 0, "YOK": None, "IKISI": None, "BELIRSIZ": None}


def v4_etiket_oku(yol: str) -> Dict[int, Tuple[Optional[int], str]]:
    """{"sayfalar": {"<no>": {"isaret": EVET | HAYIR | YOK | IKISI | BELIRSIZ, ...}}}; başka değer -> DUR."""
    J = json.load(open(yol, encoding="utf-8"))
    if not isinstance(J, dict) or not isinstance(J.get("sayfalar"), dict):
        raise V4Hata(f"etiket şeması: 'sayfalar' sözlüğü yok ({os.path.basename(yol)})")
    out = {}
    for k, v in J["sayfalar"].items():
        if not str(k).strip().isdigit() or not isinstance(v, dict) or "isaret" not in v:
            raise V4Hata(f"etiket şeması: sayfa {k!r}")
        t = str(v["isaret"]).strip().replace("İ", "I").replace("ı", "I").upper()
        if t not in _V4_DEGER:
            raise V4Hata(f"etiket şeması: sayfa {k} bilinmeyen değer {v['isaret']!r}")
        out[int(k)] = (_V4_DEGER[t], t)
    return out


def v4_kappa(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, int); b = np.asarray(b, int); n = len(a)
    if n == 0:
        return float("nan")
    po = float((a == b).mean()); pa = a.mean(); pb = b.mean(); pe = pa * pb + (1 - pa) * (1 - pb)
    return float("nan") if pe >= 1 - 1e-12 else (po - pe) / (1 - pe)


def v4_kappa_boot(a: np.ndarray, b: np.ndarray, B: int, tohum: int) -> Dict[str, Any]:
    rng = np.random.default_rng(tohum); n = len(a); v = []
    for _ in range(B):
        i = rng.integers(0, n, n); v.append(v4_kappa(a[i], b[i]))
    v = np.array(v); f = np.isfinite(v)
    return {"boot95": [float(np.quantile(v[f], 0.025)), float(np.quantile(v[f], 0.975))] if f.any() else [None, None], "atilan": int((~f).sum())}


def _v4_auc_ozet(puan: np.ndarray, y: np.ndarray, B: int, tohum: int) -> Dict[str, Any]:
    import MUM_IZI_ETIKET2 as E6
    x = -np.asarray(puan, float); y = np.asarray(y, int)
    if y.sum() < 1 or (1 - y).sum() < 1:
        return {"auc": None}
    lo, hi = V3.v3_boot(x, y, B, tohum) if min(y.sum(), (1 - y).sum()) >= 2 else (None, None)
    return {"auc": float(V3.v3_auc(x[y == 1], x[y == 0])), "boot95": [lo, hi], "p": E6.e6_perm_p(x, y)}


def _v4_ozet(X: pd.DataFrame, B: int, tohum: int) -> Dict[str, Any]:
    a = X.v4.astype(int).to_numpy(); c = X.cemal.astype(int).to_numpy()
    out = {"n": int(len(X)), "cemal_evet": int(c.sum()), "v4_var": int(a.sum()),
           "tablo": {"evet_var": int(((c == 1) & (a == 1)).sum()), "evet_yok": int(((c == 1) & (a == 0)).sum()), "hayir_var": int(((c == 0) & (a == 1)).sum()),
                     "hayir_yok": int(((c == 0) & (a == 0)).sum())}, "uyum": float((a == c).mean()) if len(X) else None, "kappa": v4_kappa(a, c)}
    out.update(v4_kappa_boot(a, c, B, tohum) if len(X) else {})
    out["puan4_auc"] = _v4_auc_ozet(X.PUAN4.to_numpy(), c, B, tohum) if len(X) else None
    return out


def v4_sinama(cikti: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or V4_YOL["cikti"]
    if os.path.exists(_v4_yol("sonuc", cikti)):
        raise V4Hata("sonuç zaten var")
    G0 = v4_kapi(cikti); Sm = V4_ESIK["sinama"]; B = int(Sm["B"]); tb = int(Sm["tohum"])
    E1 = v4_etiket_oku(V4_YOL["isaret1"]); E2 = v4_etiket_oku(V4_YOL["isaret2"])
    A1 = json.load(open(V4_YOL["anahtar1"], encoding="utf-8"))["sayfalar"]; A2 = json.load(open(V4_YOL["anahtar2"], encoding="utf-8"))["sayfalar"]
    git = {k: MI._mi_git(["log", "-1", "--format=%H %cI", "--", os.path.relpath(V4_YOL[k], KOK_V4)]) for k in ("isaret1", "isaret2", "anahtar2")}
    sab1 = MI.mi_sablon_yukle()["tam"]; Vc: Dict[Any, Any] = {}; rows = []; sayim = {"set1": {}, "set2": {}}
    for st, A, E in (("set1", A1, E1), ("set2", A2, E2)):
        for r in A:
            pg = int(r["sayfa"]); lab, t = E.get(pg, (None, "eksik")); sayim[st][t] = sayim[st].get(t, 0) + 1
            if st == "set2" and r.get("katman") == "T":
                continue
            W = V3.v3_pencere(r["zaman"], r["pazar"], r["sembol"], r["tarih"], int(r["m"]), Vc)
            R = v4_pencereler(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"]); dz = v4_duz(W)
            if bool(dz["VAR"]) != bool(R["VAR"][0]):
                raise V4Hata(f"K11: düz döngü farklı ({st} sayfa {pg})")
            if st == "set1":
                S1 = MV.mv_S_bilesen(sab1, {k: W[k] for k in ("O", "H", "L", "C", "BU", "BO", "BA")})
                if abs(S1["S"] - float(r["S"])) > 1e-4:
                    raise V4Hata(f"K10: set 1 sayfa {pg} penceresi anahtarla uyuşmuyor")
            d = W["d"]; t_ = W["t"]; son = np.arange(t_ - 3, t_ + 4); son = son[(son >= 0) & (son < len(d))]
            Re = v4_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None, son)
            rows.append({"set": st, "sayfa": pg, "zaman": r["zaman"], "isaret": t, "cemal": lab, "v4": bool(R["VAR"][0]), "PUAN4": float(R["PUAN4"][0]),
                         "yapi": bool(R["yapi"][0]), "k": int(R["k"][0]), **{e: bool(R[e][0]) for e in ("E1", "E2", "E3", "E4")},
                         **{f"p_{e}": float(R[f"p_{e}"][0]) for e in ("E1", "E2", "E3", "E4")}, **{f"g_{a}": bool(R[f"b_{a}"][0]) for a in _V4_ALT},
                         **{f"d_{a}": float(R[f"d_{a}"][0]) for a in _V4_ALT},
                         "esnek_VAR": bool(Re["VAR"][son].any()), "esnek_PUAN4": float(np.nanmax(Re["PUAN4"][son])) if np.isfinite(Re["PUAN4"][son]).any() else 0.0})
    T = pd.DataFrame(rows); T.to_csv(_v4_yol("sinama", cikti), index=False, float_format="%.5f")
    K = T[T.cemal.notna()].copy(); K["cemal"] = K.cemal.astype(int); out: Dict[str, Any] = {"surum": V4_SURUM, "kapi": G0, "etiket_git": git, "etiket_sayim": sayim}
    for ad, g in (("birlesik", K), ("set1", K[K.set == "set1"]), ("set2", K[K.set == "set2"]), ("gunluk", K[K.zaman == "gunluk"]), ("haftalik", K[K.zaman == "haftalik"])):
        out[ad] = _v4_ozet(g, B, tb)
    ey = K[(K.cemal == 1) & ~K.v4]
    out["evet_yok_dusus"] = {"n": int(len(ey)), "yapi": int((~ey.yapi).sum()), **{e: int((~ey[e]).sum()) for e in ("E1", "E2", "E3", "E4")},
                             "alt": {a: int((~ey[f"g_{a}"]).sum()) for a in _V4_ALT}}
    out["hayir_var"] = int(((K.cemal == 0) & K.v4).sum())
    es = Sm["esik"]; bk = out["birlesik"]; kp = bk["kappa"]; lo = bk.get("boot95", [None])[0]
    if bk["v4_var"] < es["var_en_az"]:
        hk = "ÖLÇÜLEMEDİ (kural çok dar)"
    elif kp is not None and np.isfinite(kp) and kp >= es["uyumlu"] and lo is not None and lo >= es["alt_uc"]:
        hk = "UYUMLU"
    elif kp is not None and np.isfinite(kp) and kp >= es["kismen"]:
        hk = "KISMEN"
    else:
        hk = "UYUMSUZ"
    out["hukum"] = hk
    out["esnek_bilgi"] = {"VAR": int(K.esnek_VAR.sum()), "kappa": v4_kappa(K.esnek_VAR.astype(int).to_numpy(), K.cemal.to_numpy()),
                          "auc": _v4_auc_ozet(K.esnek_PUAN4.to_numpy(), K.cemal.to_numpy(), B, tb)}
    out["sure_sn"] = round(time.time() - t0)
    MI._mi_jyaz(_v4_yol("sonuc", cikti), {"sinama": out}, "sonuç 7")
    v4log.info("sınama: kappa %s, hüküm %s", kp, hk)
    return out


# ================================================================ 6) EVREN SAYIMI ve ONAY (D; yalnız UYUMLU)
_V4_ISCI: Dict[str, Any] = {}


def _v4_isci(s: str) -> Dict[str, Any]:
    import MUM_IZI_ETIKET2 as E6
    G = _V4_ISCI; d = G["V"][s]; z = G["zaman"]; p = G["pazar"]; uc = G["uc"]; ix = d.index
    R = v4_tara_seri(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), d.bosluk.to_numpy(bool) if "bosluk" in d.columns else None)
    ara = (ix >= pd.Timestamp(uc[0])) & (ix <= pd.Timestamp(uc[1])); e = np.flatnonzero(R["VAR"] & ara)
    e = v4_tekil(e, np.nan_to_num(R["PUAN4"], nan=-1))
    if p in ("ABD", "AVR"):
        ev = np.zeros(len(e), bool)
        for (a, b), P in G["P"]:
            j = np.flatnonzero((ix[e] >= pd.Timestamp(a)) & (ix[e] <= pd.Timestamp(b)))
            if len(j):
                ev[j] = E6.e6_p2_maske(P, s, ix[e][j])
    else:
        dv = (d.Close * d.Volume).to_numpy(float)[e]; med = G["med"].reindex(E6._e6_anahtar(ix[e], z)).to_numpy(float); ev = np.isfinite(med) & (dv > med)
    return {"sembol": s, "n_bar": int(ara.sum()), "olay": [{"t": int(t), "tarih": str(ix[t].date()), "m": int(R["m"][t]), "PUAN4": float(R["PUAN4"][t]),
                                                            "evren": bool(v)} for t, v in zip(e, ev)]}


def v4_tarama(cikti: Optional[str] = None, islem: int = 3) -> Dict[str, Any]:
    import multiprocessing as mp
    import KASA as KS
    import MUM_IZI_ETIKET2 as E6
    t0 = time.time(); cikti = cikti or V4_YOL["cikti"]
    J0 = json.load(open(_v4_yol("sonuc", cikti), encoding="utf-8"))["sinama"]
    if J0["hukum"] != "UYUMLU":
        raise V4Hata(f"C hükmü {J0['hukum']}: D yapılmaz")
    G0 = v4_kapi(cikti)
    yol = [os.path.join(MV.MV_YOL["gunluk"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + \
          [os.path.join(MV.MV_YOL["haftalik"], f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")] + [os.path.join(MH.MH_YOL["p1"], f"V_{p}.pkl") for p in ("ABD", "AVR")]
    kasa = KS.kasa_kapisi(yol, "2022-12-31"); olay = []; say = {}
    for z in ("gunluk", "haftalik"):
        uc = V4_ESIK["tarama"][z]
        for p in ("ABD", "AVR", "BIST"):
            V = MV.mv_veri(z, p); Ps = []; med = None
            if p in ("ABD", "AVR"):
                Ps = [(ara, E6.e6_p2_hazirla(p, kl)) for ara, kl in E6.e6_parcalar(z, p)]
            else:
                med = E6.e6_bist_medyan(V, z)
            _V4_ISCI.clear(); _V4_ISCI.update({"V": V, "zaman": z, "pazar": p, "P": Ps, "med": med, "uc": uc})
            try:
                with mp.get_context("fork").Pool(islem) as pool:
                    R = list(pool.imap(_v4_isci, sorted(V), chunksize=16))
            finally:
                _V4_ISCI.clear()
            ol = [dict(o, sembol=r["sembol"], zaman=z, pazar=p) for r in R for o in r["olay"]]; olay += ol
            say[f"{z}|{p}"] = {"hisse": len(R), "bar": int(sum(r["n_bar"] for r in R)), "olay": len(ol), "olay_evren": int(sum(o["evren"] for o in ol))}
            del V, Ps, med; gc.collect()
            v4log.info("%s %s: %s (%.0f sn)", z, p, say[f"{z}|{p}"], time.time() - t0)
    if olay and max(pd.Timestamp(o["tarih"]) for o in olay) > MI.MI_KESIK:
        raise V4Hata("KESİK AŞIMI")
    haric = {r["sembol"] for r in json.load(open(V4_YOL["anahtar1"], encoding="utf-8"))["sayfalar"]} | \
            {r["sembol"] for r in json.load(open(V4_YOL["anahtar2"], encoding="utf-8"))["sayfalar"]}
    G = V4_ESIK["tarama"]["onay"]; rng = np.random.default_rng(G["tohum"]); sec = []; gor = set(haric)
    for z in ("gunluk", "haftalik"):
        h = sorted([o for o in olay if o["zaman"] == z and o["evren"]], key=lambda o: (o["sembol"], o["tarih"]))
        for i in rng.permutation(len(h)):
            o = h[int(i)]
            if o["sembol"] in gor:
                continue
            sec.append(o); gor.add(o["sembol"])
            if sum(1 for x in sec if x["zaman"] == z) >= G[z]:
                break
    p = rng.permutation(len(sec)); sec = [dict(sec[i], sayfa=j + 2) for j, i in enumerate(p)]
    os.makedirs(V4_YOL["gecici"], exist_ok=True); MI._mi_jyaz(os.path.join(V4_YOL["gecici"], "tarama_ham.json"), {"olay": olay, "secim": sec}, "tarama ham 7")
    J = {"surum": V4_SURUM, "kapi": G0, "kasa": kasa, "sayim": say, "ham_sha": MI._mi_sha(os.path.join(V4_YOL["gecici"], "tarama_ham.json")),
         "n_secim": len(sec), "sure_sn": round(time.time() - t0)}
    MI._mi_jyaz(_v4_yol("tarama", cikti), J, "tarama 7")
    return J


def v4_onay(cikti: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.patches import Rectangle
    cikti = cikti or V4_YOL["cikti"]; JT = json.load(open(_v4_yol("tarama", cikti), encoding="utf-8")); hp = os.path.join(V4_YOL["gecici"], "tarama_ham.json")
    if MI._mi_sha(hp) != JT["ham_sha"]:
        raise V4Hata("tarama ham dosyası değişmiş")
    sec = json.load(open(hp, encoding="utf-8"))["secim"]; a = MV.mv_sablon()["tam"]["ohlc"]; Vc: Dict[Any, Any] = {}; y = _v4_yol("onay", cikti)
    once = int(MV.MV_ESIK["onay"]["once"])
    with PdfPages(y, metadata={"Title": "MUM_IZI7 onay", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); fig.text(0.06, 0.94, "SENİN TARİFİNLE BULUNAN BÖLGELER", fontsize=15, weight="bold")
        fig.text(0.06, 0.88, "Kod senin kapak notunu dört parçaya çevirdi: alt bantta gel-git, yeşil mumla orta bandı aşma, üst banda içeriden boncuk gibi "
                 f"küçük mumlarla düzenli tırmanış, çoğu mumda uzun üst fitil. Sonraki {len(sec)} sayfa bu dört parçayı birlikte taşıyan RASTGELE bölgeler "
                 "(hisse / tarih / sonrası yok). Her sayfada benziyorsa ✓, benzemiyorsa × kutusuna X koy. 24'ün 19'u ✓ ise tespit geçerli sayılır.",
                 fontsize=12, va="top", wrap=True)
        MV._mv_ciz(fig.add_axes([0.25, 0.2, 0.5, 0.35]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
        pdf.savefig(fig); plt.close(fig)
        for r in sorted(sec, key=lambda r: r["sayfa"]):
            k = (r["zaman"], r["pazar"])
            if k not in Vc:
                Vc[k] = MV.mv_veri(*k)
            d = Vc[k][r["sembol"]]; t = d.index.get_loc(pd.Timestamp(r["tarih"])); m = int(r["m"]); i0 = max(0, t - m + 1 - once)
            BU, BO, BA = MI.mi_bant(d.Close.to_numpy(float)); sl = slice(i0, t + 1)
            fig = plt.figure(figsize=(8.3, 11.7))
            MV._mv_ciz(fig.add_axes([0.04, 0.6, 0.3, 0.28]), a["O"], a["H"], a["L"], a["C"], a["BU"], a["BO"], a["BA"], None, "Senin kalıbın")
            MV._mv_ciz(fig.add_axes([0.38, 0.45, 0.58, 0.45]), *(d[c].to_numpy(float)[sl] for c in ("Open", "High", "Low", "Close")), BU[sl], BO[sl], BA[sl],
                       (t - m + 1 - i0, t - i0), f"Sayfa {r['sayfa']}: bulunan bölge ({'haftalık' if r['zaman'] == 'haftalik' else 'günlük'} mum)")
            ax = fig.add_axes([0.1, 0.12, 0.8, 0.22]); ax.axis("off")
            for xx, txt in ((0.0, "✓  benziyor"), (0.55, "✗  benzemiyor")):
                ax.add_patch(Rectangle((xx, 0.1), 0.42, 0.8, fill=False, linewidth=3, transform=ax.transAxes))
                ax.text(xx + 0.21, 0.5, txt, ha="center", va="center", fontsize=22, transform=ax.transAxes)
            fig.text(0.04, 0.4, "Turuncu kutu = bölge; sağ kenar = bölgenin sonu (sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).", fontsize=9)
            pdf.savefig(fig); plt.close(fig)
    MI._mi_jyaz(_v4_yol("anahtar", cikti), {"not": "MÜHÜRLÜ: sayfa -> hisse / tarih / PUAN4; PDF'e girmez", "sayfalar": sec}, "anahtar 7")
    return y


# ================================================================ 7) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_v4(_once=_CK_ONCE_V4, _dosya="MUM_IZI_V4.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_V4",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_v4()


def _v4_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI_V4")
    ap.add_argument("komut", choices=["sablon", "sentetik", "onkayit", "sinama", "tarama", "onay"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "sablon":
            J = v4_sablon_denetim(); MI._mi_jyaz(_v4_yol("sablon"), J, "şablon 7"); print(json.dumps(MI._mi_json(J), ensure_ascii=False))
        elif a.komut == "sentetik":
            J = v4_sentetik(); print(json.dumps(MI._mi_json(J), ensure_ascii=False)[:4000])
        elif a.komut == "onkayit":
            print(v4_onkayit_yaz())
        elif a.komut == "sinama":
            J = v4_sinama(); print(json.dumps(MI._mi_json({k: J[k] for k in ("birlesik", "set1", "set2", "hukum")}), ensure_ascii=False)[:4000])
        elif a.komut == "tarama":
            J = v4_tarama(); print(json.dumps(MI._mi_json(J["sayim"]), ensure_ascii=False))
        elif a.komut == "onay":
            print(v4_onay())
    except V4Hata as ex:
        v4log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_v4_ana())
