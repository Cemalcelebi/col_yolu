"""MUM_IZI2 — MUM_IZI EK 2: İKİNCİ GRAFİK (ENSRI) PARMAK İZİ VE İLK İZLE ORTAK NOKTALAR (25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI2_IS_TANIMI.md (commit ec169de; ana model). Cemal (25 Kas 13:00, ORNEK2_ENSRI_25Kas.jpg): "Buradaki
parmak izini çıkar; yukarıda önce verdiğim parmak izi ile bütün ortak noktaları metrik olarak yaz."

MUM_IZI.py DEĞİŞMEZ: ölçüler (MI.MI_OZELLIK, MI.mi_ozellik), bant (MI.mi_bant), konum (MI.mi_konum_seri), tekil (MI._mi_tekil), sonrası
(MI.mi_sonrasi: P2 + CETVEL2 v2.2 eş + plasebo + pencere-dibi stop'lu +%5) ve veri yükleyicisi (MI.mi_veri) içe alınır. Görüntü düzeni farklı
olduğu için (fiyat paneli satırları, mum aralığı ~78 px, iki bant çizgisi, TL ekseni) sayısallaştırma burada parametreli yazıldı.
2022-12-31 sonrası gerçek fiyat OKUNMAZ (ENSRI 2024-25 dahil): ENSRI yalnız görüntüden. KASA açılmaz.

Komut:  python MUM_IZI2.py sayisallastir   görüntü -> mum_izi2_mumlar.csv, mum_izi2_sayisal.json, bindirme + elle doğrulama PNG
        python MUM_IZI2.py onkayit         MUM_IZI2_ON_KAYIT.md
        python MUM_IZI2.py kos             kapı -> yüzdelik dağılımları -> karşılaştırma -> şans tabanı -> birleşik kural (bilgi)
                                           -> mum_izi2_karsilastirma.csv, mum_izi2_sonuc.json, mum_izi2_birlesik_olay.csv.gz
        python MUM_IZI2.py gorsel          MUM_IZI2_GORSEL.pdf
        python MUM_IZI2.py rapor           MUM_IZI2_RAPOR.md
        python MUM_IZI2.py sha
Colab:  exec(open('MUM_IZI.py').read()); exec(open('MUM_IZI2.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MI2 = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv2  # noqa: E402

KOK_MI2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MI2 not in sys.path:
    sys.path.insert(0, KOK_MI2)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; yalnız çağrılır)

mi2log = logging.getLogger("col.mum_izi2")
if not mi2log.handlers:
    _mi2_h = logging.StreamHandler(sys.stderr)
    _mi2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi2: %(message)s", "%H:%M:%S"))
    mi2log.addHandler(_mi2_h)
    mi2log.setLevel(logging.INFO)
    mi2log.propagate = False


class MI2Hata(RuntimeError):
    """Durdurucu hata: görüntü / kalibrasyon / kapı / veri / kesik."""


MI2_SURUM = "MUM_IZI2 v1.0 (2026-11-25): ENSRI parmak izi + MUM_IZI tam iziyle ortak noktalar (yüzdelik) + şans tabanı + birleşik kural (bilgi)"
MI2_YOL = {"cikti": MI.MI_YOL["cikti"], "kod": os.path.join(KOK_MI2, "MUM_IZI2.py"), "kod1": MI.MI_YOL["kod"],
           "goruntu": os.path.join(MI.MI_YOL["cikti"], "ORNEK2_ENSRI_25Kas.jpg"), "acik": MI.MI_YOL["acik"], "gecici": "/tmp/mum_izi/iz2"}
MI2_DOSYA = {"mumlar": "mum_izi2_mumlar.csv", "sayisal": "mum_izi2_sayisal.json", "bindirme": "mum_izi2_bindirme.png",
             "elle": "mum_izi2_elle_dogrulama.png", "onkayit": "MUM_IZI2_ON_KAYIT.md", "karsilastirma": "mum_izi2_karsilastirma.csv",
             "sonuc": "mum_izi2_sonuc.json", "birlesik": "mum_izi2_birlesik_olay.csv.gz", "rapor": "MUM_IZI2_RAPOR.md", "pdf": "MUM_IZI2_GORSEL.pdf"}

# ================================================================ MÜHÜRLÜ AYAR (sha ön kayıtta; ortak nokta hesabından sonra DEĞİŞMEZ)
MI2_ESIK: Dict[str, Any] = {
    "surum": "MI2-1.0",
    "goruntu": {
        "boyut": [1080, 2400], "fiyat_satir": [440, 1312], "grafik_sag": 918, "etiket_sutun": [940, 1080], "aralik": [50, 110],
        "govde_min_genislik": 30, "govde_yari": 10, "govde_satir_min": 4, "fitil_yari": 3, "fitil_bosluk": 2, "bant_yari": [14, 30],
        "bant_renk": "|R-G| <= 10, 8 <= B-R <= 26, 150 <= R <= 215 (lavanta, ilk görüntüdekinden koyu çekirdek); koşu <= 10 px; mum merkezi +-6 px dışı",
        "renk": "gövde / fitil / doji maskeleri MI.mi_maskeler ile AYNI",
        "etiket": "sağ sütundaki fiyat etiketi satırları (koyu piksel, max(R,G,B) < 170); yüksekliği < 25 px olan (panel üstünde kesik ₺7,00) "
                  "dışarıda; kalan etiketler yukarıdan aşağı ₺6,50, ₺6,00, ..., ₺0,50 (değerler görüntüden göz okumasıyla; 0,50 adım); TL = a + b "
                  "satır en küçük kareler; artık (TL ve piksel) yazılır; ızgara noktalı satırlarıyla sağlama",
        "kesik": "mum gövdesinin ızgara merkezine göre beklenen genişliği grafik sağ / sol kenarını aşıyorsa 'kenarda kırpık' (gövde üst / alt ve "
                 "fitil ölçülebiliyorsa ölçüye girer)"},
    "bant": {"orta": "SMA20 çizgisi görünmüyor -> orta = (üst + alt) / 2 (TÜRETİLDİ)",
             "gorunmeyen_alt": "alt bant çizgisi fiyat panelinin tabanının ALTINDA kalan mumlar: iki senaryo. E = görünür ilk 4 mumun alt bant "
                               "değerinden doğrusal ekstrapolasyon; T = panel tabanının TL değeri (alt bandın en yüksek olabileceği yer). Bir ölçünün "
                               "ORTAK sınıfı iki senaryoda aynı değilse BELİRSİZ: sayıma ve birleşik kurala girmez. Ana değer E"},
    "olcu": "MI.MI_OZELLIK 35 ölçü AYNEN (iş tanımı '33' diyor; MUM_IZI'de 35 ölçü + 3 bağlam ölçüsü var; bağlam ölçüleri ENSRI'de bölge öncesi "
            "olmadığı için dışarıda)",
    "dagilim": {"pazar": ["ABD", "AVR", "BIST"], "veri": "MUM_IZI açık kopya (/tmp/mum_izi/acik, <= 2022-12-30), MI.mi_veri yükleyicisi",
                "tarama": ["2016-01-01", "2022-12-31"], "n": 20000, "L": [20, 12], "tohum": {"20": 25112031, "12": 25112032},
                "tanim": "geçerli (hisse, pencere sonu e) çiftleri üç pazar birleşik havuz: e tarama aralığında, pencere başı bandın tanımlı olduğu "
                         "ilk bardan (19) sonra; havuzdan yerine koymadan düzgün 20.000; ölçüler MI.mi_ozellik + MI.mi_bant (SMA20, 2 std)",
                "yuzdelik": "p = (#{x < v} + 0,5 #{x = v}) / N"},
    "ortak": {"yuksek": 0.75, "dusuk": 0.25, "guclu_yuksek": 0.90, "guclu_dusuk": 0.10,
              "sinif": "GÜÇLÜ ORTAK: p1, p2 >= 0,90 ya da ikisi <= 0,10; ORTAK: ikisi >= 0,75 ya da ikisi <= 0,25 (güçlü değil); ZIT: biri >= 0,75 "
                       "öteki <= 0,25; AYRI: kalan; BELİRSİZ: bant senaryosuna göre sınıf değişiyor. p1 = iz 1 (MUM_IZI tam şablonu, L 20) L 20 "
                       "dağılımında; p2 = iz 2 (ENSRI, L 12) L 12 dağılımında"},
    "S": "iz 2'ye iz 1 şablonu: MUM_IZI pencere uzunlukları 16..24 (esneme +-%20); L 12 bu aralıkta değilse 'S UYGULANAMAZ' ve ölçü uzaklığı "
         "bileşeni D_oz (MI.mi_mesafe ölçü kısmı, kalibrasyon sd'si) ile D_oz / tau_oz verilir; ayrıca rastgele L 12 dağılım pencerelerinin iz 1'e "
         "D_oz değerleri içinde iz 2'nin yüzdeliği",
    "sans": {"cift": 5000, "tohum": {"20": 25112033, "12": 25112034},
             "tanim": "aynı havuzdan bağımsız 5.000 L 20 ve 5.000 L 12 pencere, sırayla eşlenir (5.000 çift); her çiftte aynı yüzdelik ve sınıf "
                      "kuralıyla (aynı ölçü kümesi: BELİRSİZ ölçüler dışarıda) GÜÇLÜ ORTAK, ORTAK (güçlü dahil) ve ZIT sayısı; ortalama, %95 üst "
                      "sınır (0,95 yüzdelik) ve iki izin sayısına eşit ya da büyük çift payı. 'Ortak nokta çok' sözü yalnız iki izin ORTAK sayısı "
                      "%95 üst sınırı AŞARSA"},
    "birlesik": {"L": [12, 20], "tekil": 15,
                 "kural": "GÜÇLÜ ORTAK + ORTAK ölçülerin HEPSİ aynı uçta: YÜKSEK -> ölçü >= q_L(0,75), DÜŞÜK -> ölçü <= q_L(0,25); q_L = q_12 + "
                          "(q_20 - q_12) (L - 12) / 8 (L 12 ve L 20 dağılımlarının yüzdelikleri arasında doğrusal); pencere sonu t'de L = 12..20'den "
                          "en az biri kuralı taşırsa olay, m = en kısa uygun L; aynı hissede 15 geçerli bar tekil; tarama 2016-22 ABD / AVR / BIST",
                 "sonrasi": "MI.mi_sonrasi AYNEN: ABD / AVR P2 + CETVEL2 v2.2 konum eşi, R15 eşli fark, +%5 (stop = pencere en düşük Low x 0,98) vs "
                            "20 eş, plasebo 200 tohum (karar pazarı, 'hepsi'); konum MI.mi_konum_seri; n < 30 hücre 'örneklem yetersiz'",
                 "etiket": "EZBER RİSKLİ (iki örnekten türetildi); karar etiketi VERİLMEZ, kasa açılmaz"},
}

MI2_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "ortak nokta tabanı = şans tabanı SAYIYLA (5.000 rastgele L20 / L12 pencere çifti, aynı kural, ortalama ve %95 üst sınır); "
                   "birleşik kural sonrası MI.mi_sonrasi: CETVEL2 v2.2 konum eşi (aynı gün aynı kova >= 5 eş), +%5 eşi aynı geometri, plasebo 200 tohum"),
    "K2": ("EVET", "ENSRI yalnız görüntüden (2024-25 gerçek fiyat OKUNMAZ); dağılım / şans / birleşik kural açık kopya <= 2022-12-30 (KASA kapısı "
                   "MI.mi_kasa_kapi); pencere ölçüleri yalnız t'ye kadarki barlar (MI.mi_bant / mi_ozellik prefix testli); birleşik olayda prefix "
                   "denetimi (mi2_prefix, 30 olay)"),
    "K3": ("EVET", "MI.mi_veri geçerli bar süzgeci (H > L, V > 0); sayısallaştırmada her bölge mumu H >= max(O,C), L <= min(O,C) denetimi"),
    "K4": ("EVET", "birleşik kural olayları aynı hissede 15 geçerli bar tekil (MI._mi_tekil) + C2.c2_olay tekil 15; dağılım pencereleri tekilsiz "
                   "(yüzdelik tabanı, olay değil)"),
    "K5": ("EVET", "giriş t + 1 açılış (MI.mi_sonrasi -> OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1"),
    "K6": ("EVET", "ENSRI TL ekseni doğrusal kalibrasyon (13 etiket, artık yazılır); ölçüler ölçek bağımsız (oran, mum boyu birimi); gerçek veri "
                   "TEZGAH2 bölünme düzeltmeli açık kopya"),
    "K7": ("EVET", "açık kopya bugün işlem gören hisseler (ABD 4.450, AVR 572, BIST 475): sonrası yukarı yanlı, olay ve eş aynı evren; ENSRI tek "
                   "hisse, halka arz sonrası kısa geçmiş (bant 12 aylık mumla)"),
    "K8": ("EVET", "birleşik kural hücreleri pazar x dönem (d1619 / d2022); n < 30 'örneklem yetersiz'; iki örnekten türetilen kural EZBER RİSKLİ; "
                   "karar etiketi yok"),
    "K9": ("EVET", "MUM_IZI2_ON_KAYIT.md: KOD2_SHA, ESIK2_SHA, SAYISAL2_SHA, MI_KOD_SHA, dağılım tohumları; ön kayıt commit'i ortak nokta "
                   "hesabından ÖNCE; mi2_kapi kontrol kapısı + sha + git denetler"),
    "K10": ("EVET", "bindirme PNG (12 mum) + 3 rastgele mumun yakın plan elle doğrulama PNG'si; mum sayısı ve renk dizisi elle sayımla "
                    "(test_mum_izi2); TL kalibrasyon artığı ve ızgara satırı sağlaması"),
    "K11": ("EVET", "mi2_yeniden: iki ölçünün (ust_fitil, kapanis_egim) iz 2 değeri düz döngüyle; iki ölçünün yüzdeliği dağılım dosyasından düz "
                    "pandas ile; birleşik kural 10 olayda kuralın düz yeniden denetimi"),
    "K12": ("EVET", "'ortak nokta çok' sözü yalnız şans tabanı aşılırsa; birleşik kural EZBER RİSKLİ, karar yok; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_mi2); MUM_IZI.py ve defter / UC_IZ2 dosyaları değişmez; yalnız kendi yolları git add"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; benzerlik / ortak nokta ölçümü"),
}


# ================================================================ 0) YARDIMCI
def _mi2_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MI2_YOL["cikti"], MI2_DOSYA[ad])


def mi2_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MI2_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def mi2_sinif(p1: float, p2: float) -> str:
    O = MI2_ESIK["ortak"]
    if (p1 >= O["guclu_yuksek"] and p2 >= O["guclu_yuksek"]) or (p1 <= O["guclu_dusuk"] and p2 <= O["guclu_dusuk"]):
        return "GÜÇLÜ ORTAK"
    if (p1 >= O["yuksek"] and p2 >= O["yuksek"]) or (p1 <= O["dusuk"] and p2 <= O["dusuk"]):
        return "ORTAK"
    if (p1 >= O["yuksek"] and p2 <= O["dusuk"]) or (p1 <= O["dusuk"] and p2 >= O["yuksek"]):
        return "ZIT"
    return "AYRI"


def mi2_yuzdelik(dagilim: np.ndarray, v: float) -> float:
    x = np.asarray(dagilim, float)
    return float(((x < v).sum() + 0.5 * (x == v).sum()) / len(x))


def mi2_yuzdelik_coklu(dagilim: np.ndarray, v: np.ndarray) -> np.ndarray:
    """p = (#< + 0,5 #=) / N, vektörlü (sıralı dağılımda arama)."""
    x = np.sort(np.asarray(dagilim, float)); v = np.asarray(v, float)
    lo = np.searchsorted(x, v, "left"); hi = np.searchsorted(x, v, "right")
    return (lo + 0.5 * (hi - lo)) / len(x)


# ================================================================ 1) SAYISALLAŞTIRMA
def mi2_goruntu_oku(yol: Optional[str] = None) -> np.ndarray:
    from PIL import Image
    y = yol or MI2_YOL["goruntu"]
    if not os.path.exists(y):
        raise MI2Hata(f"görüntü yok: {y}")
    im = np.asarray(Image.open(y).convert("RGB")).astype(np.int32)
    if list(im.shape[:2][::-1]) != MI2_ESIK["goruntu"]["boyut"]:
        raise MI2Hata(f"görüntü boyutu {im.shape[1]}x{im.shape[0]}")
    return im


def mi2_bant_maske(im: np.ndarray) -> np.ndarray:
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (np.abs(R - G) <= 10) & (B - R >= 8) & (B - R <= 26) & (R >= 150) & (R <= 215)


def mi2_kalibrasyon(im: np.ndarray) -> Dict[str, Any]:
    """Fiyat etiketi satırları -> TL = a + b satır (en küçük kareler); artık; ızgara noktalı satırlarıyla sağlama."""
    Gg = MI2_ESIK["goruntu"]; c0, c1 = Gg["etiket_sutun"]; y0, y1 = Gg["fiyat_satir"]
    koyu = im[:, c0:c1].max(2) < 170
    sat = [(a, b) for a, b in MI._mi_kosu(koyu[y0 - 20:y1 + 20].any(1)) if b - a + 1 >= 25]
    mer = np.array([(a + b) / 2.0 + y0 - 20 for a, b in sat])
    if len(mer) < 4:
        raise MI2Hata(f"kalibrasyon: en az 4 etiket gerekli ({len(mer)})")
    deger = 6.50 - 0.50 * np.arange(len(mer))
    b, a = np.polyfit(mer, deger, 1)
    art = deger - (a + b * mer)
    # ızgara: grafik sütunlarında nötr gri noktalı satırlar
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    gri = (np.abs(R - G) < 6) & (np.abs(B - R) < 8) & (R < 215) & (R > 120)
    gs = np.flatnonzero(gri[y0:y1, 0:Gg["grafik_sag"] - 20].sum(1) > 40) + y0
    izg = [float(np.mean([r for r in gs if abs(r - m) <= 4])) if any(abs(r - m) <= 4 for r in gs) else float("nan") for m in mer]
    return {"a": float(a), "b": float(b), "etiket_satir": mer.tolist(), "etiket_tl": deger.tolist(), "artik_tl": art.tolist(),
            "artik_tl_max": float(np.abs(art).max()), "artik_px_max": float(np.abs(art).max() / abs(b)), "izgara_satir": izg,
            "izgara_fark_px_max": float(np.nanmax(np.abs(np.array(izg) - mer))), "px_tl": float(1 / abs(b)),
            "taban_tl": float(a + b * y1), "kesik_etiket": int(sum(1 for a_, b_ in MI._mi_kosu(koyu[y0 - 20:y1 + 20].any(1)) if b_ - a_ + 1 < 25))}


def mi2_izgara(M: Dict[str, np.ndarray]) -> Tuple[float, float, List[float]]:
    Gg = MI2_ESIK["goruntu"]; y0, y1 = Gg["fiyat_satir"]
    renkli = (M["yesil"] | M["kirmizi"])[y0:y1].sum(0) > 0
    oz = [(a, b) for a, b in MI._mi_kosu(renkli) if b - a + 1 >= Gg["govde_min_genislik"]]
    gen = np.median([b - a + 1 for a, b in oz])
    tam = [(a, b) for a, b in oz if b - a + 1 >= gen - 3]                 # kenarda kırpık gövde ızgara uydurmasına girmez
    mer = np.array([(a + b) / 2.0 for a, b in tam])
    df = np.diff(mer); lo, hi = Gg["aralik"]; b0 = float(np.median(df[(df > lo) & (df < hi)]))
    k = np.round((mer - mer[0]) / b0)
    b, a = np.polyfit(k, mer, 1)
    if np.abs(mer - (a + b * k)).max() > 3.0:
        raise MI2Hata("ızgara artığı büyük")
    return float(a), float(b), mer.tolist()


def mi2_mum(M: Dict[str, np.ndarray], xc: float) -> Optional[Dict[str, Any]]:
    """MI.mi_mum ile aynı mantık (gövde / doji çizgisi / fitil koşusu), ENSRI panel satırlarıyla."""
    Gg = MI2_ESIK["goruntu"]; y0, y1 = Gg["fiyat_satir"]; W = min(M["yesil"].shape[1], Gg["grafik_sag"])
    x = int(round(xc)); hy = Gg["govde_yari"]
    c0, c1 = max(0, x - hy), min(W, x + hy + 1)
    if c1 - c0 < 3:
        return None
    gs = M["yesil"][y0:y1, c0:c1].sum(1); rs = M["kirmizi"][y0:y1, c0:c1].sum(1)
    sat = np.flatnonzero((gs + rs) >= Gg["govde_satir_min"]); doji = False
    if len(sat):
        ust, alt = int(sat.min() + y0), int(sat.max() + y0); renk = "Y" if gs.sum() > rs.sum() else "K"
    else:
        cols = [c for c in list(range(x - 11, x - 3)) + list(range(x + 4, x + 12)) if 0 <= c < W]
        gl = M["yesil_acik"][y0:y1, cols].sum(1); rl = M["kirmizi_acik"][y0:y1, cols].sum(1)
        tik = np.flatnonzero((gl + rl) >= 3)
        if not len(tik):
            return None
        ust, alt = int(tik.min() + y0), int(tik.max() + y0); renk = "Y" if gl.sum() > rl.sum() else "K"; doji = True
    fy = Gg["fitil_yari"]; w0, w1 = max(0, x - fy), min(W, x + fy + 1)
    ink = (M["fitil"][:, w0:w1] | M["yesil"][:, w0:w1] | M["kirmizi"][:, w0:w1] | M["yesil_acik"][:, w0:w1] | M["kirmizi_acik"][:, w0:w1]).any(1)

    def uzat(bas: int, adim: int) -> int:
        y = bas; son = bas; bos = 0
        while y0 < y < y1 - 1:
            y += adim
            if ink[y]:
                son = y; bos = 0
            else:
                bos += 1
                if bos > Gg["fitil_bosluk"]:
                    break
        return son
    return {"x": float(xc), "renk": renk, "doji_cizgi": doji, "govde_ust": ust, "govde_alt": alt, "fitil_ust": uzat(ust, -1), "fitil_alt": uzat(alt, 1)}


def mi2_bant_izle(im: np.ndarray, merkezler: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """Üst ve alt bant çizgisi sütun sütun (gözlenmeyen NaN); MI._mi_bant_izle mantığı, iki çizgi."""
    Gg = MI2_ESIK["goruntu"]; y0, y1 = Gg["fiyat_satir"]; W = Gg["grafik_sag"]; tol = 6
    from scipy.ndimage import binary_closing
    Bm = binary_closing(mi2_bant_maske(im), structure=np.ones((3, 1), bool)); yasak = np.zeros(W, bool)   # 1 px dikey boşluk kapanır
    for xc in merkezler:
        a_, b_ = int(round(xc)) - 6, int(round(xc)) + 7
        if b_ > 0 and a_ < W:
            yasak[max(0, a_):min(W, b_)] = True
    mer = [[] if yasak[x] else [(a + b) / 2.0 + y0 for a, b in MI._mi_kosu(Bm[y0:y1, x]) if 1 <= b - a <= 10] for x in range(W)]
    ref = [x for x in range(W) if len(mer[x]) == 2]
    if not ref:
        raise MI2Hata("bant: iki çizginin göründüğü sütun yok")
    x0 = ref[len(ref) // 2]
    U = np.full(W, np.nan); Lo = np.full(W, np.nan); U[x0], Lo[x0] = mer[x0]
    for yon in (1, -1):
        onc = list(mer[x0]); sx = [x0, x0]; x = x0 + yon
        while 0 <= x < W:
            for li, arr in enumerate((U, Lo)):
                if mer[x]:
                    c = np.array(mer[x]); k = int(np.argmin(np.abs(c - onc[li])))
                    if abs(c[k] - onc[li]) <= tol + 0.4 * abs(x - sx[li] - yon):
                        arr[x] = c[k]; onc[li] = float(c[k]); sx[li] = x
            x += yon
    return U, Lo


def _mi2_bant_x(arr: np.ndarray, xc: float) -> float:
    a, b = MI2_ESIK["goruntu"]["bant_yari"]
    xs = [x for x in range(int(xc - b), int(xc + b) + 1) if 0 <= x < len(arr) and abs(x - xc) >= a and np.isfinite(arr[x])]
    if len(xs) < 4:
        return float("nan")
    return float(np.polyval(np.polyfit(np.array(xs, float), arr[xs], 1), xc))


def mi2_sayisallastir(yol: Optional[str] = None) -> Dict[str, Any]:
    im = mi2_goruntu_oku(yol); M = MI.mi_maskeler(im); Gg = MI2_ESIK["goruntu"]
    K = mi2_kalibrasyon(im)
    a, b, mer = mi2_izgara(M)
    W = Gg["grafik_sag"]
    kmin = int(math.ceil((0 - a) / b - 0.5)); kmax = int(math.floor((W - 1 - a) / b + 0.5))
    kmin = max(kmin, int(math.ceil((0 - a) / b)))                     # merkezi görüntü dışında kalan ızgara noktası yok
    U, Lo = mi2_bant_izle(im, [a + b * k for k in range(kmin, kmax + 1)])
    sat = []
    for k in range(kmin, kmax + 1):
        xc = a + b * k
        m = mi2_mum(M, xc)
        if m is None:
            continue
        yari = (Gg["govde_yari"] + 13)
        m["kenar"] = "SAG_KIRPIK" if xc + yari > W - 1 else ("SOL_KIRPIK" if xc - yari < 0 else "")
        m["k"] = k
        m["bant_ust"] = _mi2_bant_x(U, xc); m["bant_alt"] = _mi2_bant_x(Lo, xc)
        sat.append(m)
    T = pd.DataFrame(sat).sort_values("k").reset_index(drop=True)
    T["i"] = np.arange(1, len(T) + 1)
    tl = lambda r: K["a"] + K["b"] * np.asarray(r, float)  # noqa: E731
    yes = T.renk == "Y"; doj = T.doji_cizgi.astype(bool); orta = (T.govde_ust + T.govde_alt) / 2
    T["O"] = np.where(doj, tl(orta), np.where(yes, tl(T.govde_alt), tl(T.govde_ust)))
    T["C"] = np.where(doj, tl(orta), np.where(yes, tl(T.govde_ust), tl(T.govde_alt)))
    T["H"] = tl(T.fitil_ust); T["L"] = tl(T.fitil_alt); T["BU"] = tl(T.bant_ust)
    # alt bant: görünür -> ölçülen; panel altında -> E (ilk 4 görünür mumdan doğrusal) ve T (panel tabanı)
    gor = np.isfinite(T.bant_alt.to_numpy(float))
    T["alt_gorunur"] = gor
    BA = tl(T.bant_alt.to_numpy(float))
    ix = np.flatnonzero(gor)[:4]
    if len(ix) < 2:
        raise MI2Hata("alt bant: ekstrapolasyon için görünür mum yetersiz")
    p = np.polyfit(T.i.to_numpy(float)[ix], BA[ix], 1)
    T["BA_E"] = np.where(gor, BA, np.polyval(p, T.i.to_numpy(float)))
    T["BA_T"] = np.where(gor, BA, K["taban_tl"])
    T["BO_E"] = (T.BU + T.BA_E) / 2; T["BO_T"] = (T.BU + T.BA_T) / 2
    if T[["O", "H", "L", "C", "BU"]].isna().any().any():
        raise MI2Hata("eksik ölçü (fitil / üst bant)")
    if ((T.H < T[["O", "C"]].max(axis=1) - 1e-9) | (T.L > T[["O", "C"]].min(axis=1) + 1e-9)).any():
        raise MI2Hata("mum H / L gövdeyi kapsamıyor")
    return {"tablo": T, "kalibrasyon": K, "izgara": {"a": a, "b": b, "govde_merkez": mer}, "n": int(len(T)),
            "renk_dizisi": "".join(T.renk), "goruntu_sha": MI._mi_sha(yol or MI2_YOL["goruntu"]),
            "alt_gorunmeyen": T.i[~gor].astype(int).tolist(), "ekstrapolasyon": {"egim_tl_mum": float(p[0]), "kesisim": float(p[1]), "mumlar": T.i[ix].astype(int).tolist()}}


def mi2_ozellik(T: pd.DataFrame, senaryo: str = "E") -> Dict[str, float]:
    F = MI.mi_ozellik(*(T[c].to_numpy(float) for c in ("O", "H", "L", "C", "BU")), T[f"BO_{senaryo}"].to_numpy(float), T[f"BA_{senaryo}"].to_numpy(float))
    return {k: float(v[0]) for k, v in F.items()}


def mi2_bindirme_png(D: Dict[str, Any], yol: Optional[str] = None) -> str:
    from PIL import Image, ImageDraw
    im = Image.open(MI2_YOL["goruntu"]).convert("RGB"); dr = ImageDraw.Draw(im); K = D["kalibrasyon"]
    for r in D["tablo"].itertuples():
        x = float(r.x)
        dr.rectangle([x - 26, r.govde_ust - 1, x + 26, r.govde_alt + 1], outline=(0, 70, 255), width=2)
        dr.line([x + 30, r.fitil_ust, x + 30, r.fitil_alt], fill=(0, 0, 0), width=2)
        dr.line([x + 26, r.fitil_ust, x + 34, r.fitil_ust], fill=(0, 0, 0), width=2); dr.line([x + 26, r.fitil_alt, x + 34, r.fitil_alt], fill=(0, 0, 0), width=2)
        for v in (r.bant_ust, r.bant_alt):
            if np.isfinite(v):
                dr.ellipse([x - 5, v - 5, x + 5, v + 5], outline=(200, 0, 200), width=2)
        if not r.alt_gorunur:
            ye = (r.BA_E - K["a"]) / K["b"]
            dr.text((x - 10, min(ye, 1290)), "E", fill=(200, 0, 200))
        dr.text((x - 6, r.fitil_ust - 28), f"{int(r.i)}" + ("k" if r.kenar else ""), fill=(0, 70, 255))
    for yy, tl_ in zip(K["etiket_satir"], K["etiket_tl"]):
        dr.line([925, yy, 945, yy], fill=(255, 0, 0), width=2)
    y = yol or _mi2_yol("bindirme"); im.save(y)
    return y


def mi2_elle_png(D: Dict[str, Any], yol: Optional[str] = None, tohum: int = 2518) -> Dict[str, Any]:
    from PIL import Image
    T = D["tablo"]; rng = np.random.default_rng(tohum); sec = sorted(rng.choice(len(T), size=3, replace=False).tolist())
    ham = Image.open(MI2_YOL["goruntu"]).convert("RGB")
    tmp = os.path.join(MI2_YOL["gecici"], "bindirme2_tam.png"); os.makedirs(MI2_YOL["gecici"], exist_ok=True)
    mi2_bindirme_png(D, tmp); bnd = Image.open(tmp).convert("RGB")
    parca, bilgi = [], []
    for i in sec:
        r = T.iloc[i]; x = int(r.x); y0 = int(min(r.fitil_ust, r.bant_ust) - 40); y1 = int(r.fitil_alt + 60)
        kut = (max(0, x - 50), max(0, y0), min(1080, x + 50), min(2400, y1))
        a = ham.crop(kut).resize(((kut[2] - kut[0]) * 2, (kut[3] - kut[1]) * 2), Image.NEAREST); b = bnd.crop(kut).resize(a.size, Image.NEAREST)
        c = Image.new("RGB", (a.size[0] * 2 + 10, a.size[1]), (255, 255, 255)); c.paste(a, (0, 0)); c.paste(b, (a.size[0] + 10, 0)); parca.append(c)
        bilgi.append({"i": int(r.i), "renk": r.renk, "doji_cizgi": bool(r.doji_cizgi), "govde_ust": int(r.govde_ust), "govde_alt": int(r.govde_alt),
                      "fitil_ust": int(r.fitil_ust), "fitil_alt": int(r.fitil_alt), "O": round(float(r.O), 3), "H": round(float(r.H), 3),
                      "L": round(float(r.L), 3), "C": round(float(r.C), 3)})
    Wt = sum(p.size[0] for p in parca) + 20 * (len(parca) - 1); Ht = max(p.size[1] for p in parca)
    out = Image.new("RGB", (Wt, Ht), (255, 255, 255)); x = 0
    for p in parca:
        out.paste(p, (x, 0)); x += p.size[0] + 20
    y = yol or _mi2_yol("elle"); out.save(y)
    return {"png": y, "mumlar": bilgi}


def mi2_sayisallastir_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or MI2_YOL["cikti"]
    D = mi2_sayisallastir(); T = D["tablo"]
    T.to_csv(_mi2_yol("mumlar", cikti), index=False, float_format="%.10g")
    FE = mi2_ozellik(T, "E"); FT = mi2_ozellik(T, "T")
    mi2_bindirme_png(D, _mi2_yol("bindirme", cikti))
    J = {"surum": MI2_SURUM, "goruntu_sha": D["goruntu_sha"], "n": D["n"], "renk_dizisi": D["renk_dizisi"], "kalibrasyon": D["kalibrasyon"],
         "izgara": D["izgara"], "alt_gorunmeyen": D["alt_gorunmeyen"], "ekstrapolasyon": D["ekstrapolasyon"],
         "kenar": {int(r.i): r.kenar for r in T.itertuples() if r.kenar}, "F_E": FE, "F_T": FT,
         "elle": mi2_elle_png(D, _mi2_yol("elle", cikti)),
         "notlar": ["Üstte 'Piyasa Fiyatı ₺2,23' yazıyor, mumlar ~₺4 düzeyinde: çelişki yalnız not edildi (neden aranmadı, veriye bakılmadı).",
                    "Orta bant (SMA20) çizgisi görünmüyor: orta = (üst + alt) / 2 TÜRETİLDİ.",
                    "Mum aralığı AYLIK varsayıldı ('5Y' görünüm, yıl etiketleri arası ~3 mum); 12 mum ~ 1 yıl; bant 20 mumdan kısa geçmişle çizilmiş olabilir."]}
    MI._mi_jyaz(_mi2_yol("sayisal", cikti), J, "sayısal 2")
    mi2log.info("ENSRI: %d mum (%s), kalibrasyon artığı %.4f TL, alt bant görünmeyen %s", D["n"], D["renk_dizisi"], D["kalibrasyon"]["artik_tl_max"],
                D["alt_gorunmeyen"])
    return J


# ================================================================ 2) DAĞILIM, KARŞILAŞTIRMA, ŞANS
def mi2_veri_hepsi(acik: Optional[str] = None) -> Dict[str, Dict[str, pd.DataFrame]]:
    acik = acik or MI2_YOL["acik"]; out = {}
    for p in MI2_ESIK["dagilim"]["pazar"]:
        V = MI.mi_veri(p, acik)["V"]
        en_gec = max(d.index.max() for d in V.values())
        if en_gec > MI.MI_KESIK:
            raise MI2Hata(f"{p}: KESİK AŞIMI {en_gec.date()}")
        out[p] = {s: d for s, d in V.items() if len(d) >= 40}
    return out


def _mi2_uclar(V: Dict[str, Dict[str, pd.DataFrame]], L: int) -> Tuple[List[Tuple[str, str]], np.ndarray, List[np.ndarray]]:
    """Her (pazar, hisse) için geçerli pencere sonu indeksleri (tarama aralığı, pencere başı >= 19)."""
    bas, son = (pd.Timestamp(x) for x in MI2_ESIK["dagilim"]["tarama"]); anah, say, uc = [], [], []
    for p in MI2_ESIK["dagilim"]["pazar"]:
        for s in sorted(V[p]):
            ix = V[p][s].index
            e = np.flatnonzero((ix >= bas) & (ix <= son)); e = e[e - L + 1 >= 19]
            anah.append((p, s)); say.append(len(e)); uc.append(e)
    return anah, np.array(say, np.int64), uc


def _mi2_pencere_oz(d: pd.DataFrame, e: np.ndarray, L: int) -> Dict[str, np.ndarray]:
    O, H, Lw, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    BU, BO, BA = MI.mi_bant(C)
    a = e - L + 1
    idx = a[:, None] + np.arange(L)[None, :]
    return MI.mi_ozellik(O[idx], H[idx], Lw[idx], C[idx], BU[idx], BO[idx], BA[idx])


def mi2_orneklem(V: Dict[str, Dict[str, pd.DataFrame]], L: int, n: int, tohum: int) -> pd.DataFrame:
    """Birleşik havuzdan yerine koymadan düzgün n pencere -> ölçü tablosu (+ pazar, sembol, tarih)."""
    anah, say, uc = _mi2_uclar(V, L)
    top = int(say.sum()); rng = np.random.default_rng(tohum)
    g = np.sort(rng.choice(top, size=min(n, top), replace=False))
    sinir = np.r_[0, np.cumsum(say)]
    hisse = np.searchsorted(sinir, g, side="right") - 1
    parca = []
    for h in np.unique(hisse):
        p, s = anah[h]; yer = g[hisse == h] - sinir[h]; e = uc[h][yer]
        F = _mi2_pencere_oz(V[p][s], e, L)
        df = pd.DataFrame({k: v for k, v in F.items()}); df["pazar"] = p; df["sembol"] = s; df["tarih"] = V[p][s].index[e]
        parca.append(df)
    out = pd.concat(parca, ignore_index=True)
    out.attrs["havuz"] = top
    return out


def mi2_karsilastir(F1: Dict[str, float], FE: Dict[str, float], FT: Dict[str, float], D20: pd.DataFrame, D12: pd.DataFrame) -> pd.DataFrame:
    sat = []
    for k, acik, grup in MI.MI_OZELLIK:
        p1 = mi2_yuzdelik(D20[k].to_numpy(), F1[k]); p2e = mi2_yuzdelik(D12[k].to_numpy(), FE[k]); p2t = mi2_yuzdelik(D12[k].to_numpy(), FT[k])
        se, st = mi2_sinif(p1, p2e), mi2_sinif(p1, p2t)
        sat.append({"olcu": k, "aciklama": acik, "grup": grup, "iz1": F1[k], "iz2": FE[k], "iz2_T": FT[k], "p1": p1, "p2": p2e, "p2_T": p2t,
                    "sinif_E": se, "sinif_T": st, "sinif": se if se == st else "BELİRSİZ",
                    "uc": ("YÜKSEK" if p1 >= 0.5 else "DÜŞÜK") if se == st and se in ("GÜÇLÜ ORTAK", "ORTAK") else ""})
    return pd.DataFrame(sat)


def mi2_say(K: pd.DataFrame) -> Dict[str, int]:
    v = K.sinif.value_counts()
    return {"GUCLU": int(v.get("GÜÇLÜ ORTAK", 0)), "ORTAK_DAHIL": int(v.get("GÜÇLÜ ORTAK", 0) + v.get("ORTAK", 0)), "ORTAK_YALNIZ": int(v.get("ORTAK", 0)),
            "ZIT": int(v.get("ZIT", 0)), "AYRI": int(v.get("AYRI", 0)), "BELIRSIZ": int(v.get("BELİRSİZ", 0)), "olcu": int(len(K))}


def mi2_sans(V: Dict[str, Dict[str, pd.DataFrame]], D20: pd.DataFrame, D12: pd.DataFrame, olculer: List[str], gozlenen: Dict[str, int]) -> Dict[str, Any]:
    S = MI2_ESIK["sans"]; n = int(S["cift"])
    A = mi2_orneklem(V, 20, n, S["tohum"]["20"]); B = mi2_orneklem(V, 12, n, S["tohum"]["12"])
    rng = np.random.default_rng(S["tohum"]["20"] + 7)
    A = A.iloc[rng.permutation(len(A))].reset_index(drop=True); B = B.iloc[rng.permutation(len(B))].reset_index(drop=True)
    m = min(len(A), len(B)); O = MI2_ESIK["ortak"]
    g = np.zeros(m, int); o = np.zeros(m, int); z = np.zeros(m, int)
    for k in olculer:
        p1 = mi2_yuzdelik_coklu(D20[k].to_numpy(), A[k].to_numpy()[:m]); p2 = mi2_yuzdelik_coklu(D12[k].to_numpy(), B[k].to_numpy()[:m])
        gu = ((p1 >= O["guclu_yuksek"]) & (p2 >= O["guclu_yuksek"])) | ((p1 <= O["guclu_dusuk"]) & (p2 <= O["guclu_dusuk"]))
        orr = ((p1 >= O["yuksek"]) & (p2 >= O["yuksek"])) | ((p1 <= O["dusuk"]) & (p2 <= O["dusuk"]))
        zt = ((p1 >= O["yuksek"]) & (p2 <= O["dusuk"])) | ((p1 <= O["dusuk"]) & (p2 >= O["yuksek"]))
        g += gu; o += orr; z += zt
    def oz(x: np.ndarray, gz: int) -> Dict[str, float]:
        return {"ort": float(x.mean()), "sd": float(x.std()), "ust95": float(np.quantile(x, 0.95)), "ust99": float(np.quantile(x, 0.99)),
                "gozlenen": int(gz), "pay_ge_gozlenen": float((x >= gz).mean())}
    return {"cift": int(m), "olcu_sayisi": len(olculer), "ORTAK_DAHIL": oz(o, gozlenen["ORTAK_DAHIL"]), "GUCLU": oz(g, gozlenen["GUCLU"]),
            "ZIT": oz(z, gozlenen["ZIT"]), "hist_ortak": np.bincount(o, minlength=len(olculer) + 1).tolist()}


def mi2_S(F2: Dict[str, float], D12: pd.DataFrame) -> Dict[str, Any]:
    sab = MI.mi_sablon_yukle()["tam"]
    alt = MI.MI_ESIK["benzerlik"]["ozellik_alt"]; sd = sab["sd"]
    if 12 >= min(sab["uzunluklar"]):
        raise MI2Hata("beklenmeyen: L 12 şablon uzunlukları içinde")
    d = math.sqrt(sum(((F2[k] - sab["F"][k]) / sd[k]) ** 2 for k in alt) / len(alt))
    dr = np.sqrt(np.mean([((D12[k].to_numpy() - sab["F"][k]) / sd[k]) ** 2 for k in alt], axis=0))
    return {"S": "UYGULANAMAZ", "neden": f"iz 2 L = 12, iz 1 şablon pencereleri {sab['uzunluklar']} (esneme +-%20) dışında", "D_oz": d,
            "D_oz_tau": d / sab["tau"][2], "tau_oz": sab["tau"][2], "rastgele_L12_D_oz_yuzdelik": mi2_yuzdelik(dr, d),
            "rastgele_L12_D_oz_medyan": float(np.median(dr))}


# ================================================================ 3) BİRLEŞİK KURAL (BİLGİ)
def mi2_kural(K: pd.DataFrame, D20: pd.DataFrame, D12: pd.DataFrame) -> List[Dict[str, Any]]:
    O = MI2_ESIK["ortak"]; out = []
    for r in K[K.sinif.isin(["GÜÇLÜ ORTAK", "ORTAK"])].itertuples():
        q = O["yuksek"] if r.uc == "YÜKSEK" else O["dusuk"]
        out.append({"olcu": r.olcu, "uc": r.uc, "q12": float(np.quantile(D12[r.olcu].to_numpy(), q)), "q20": float(np.quantile(D20[r.olcu].to_numpy(), q))})
    return out


def _mi2_kural_esik(k: Dict[str, Any], L: int) -> float:
    return k["q12"] + (k["q20"] - k["q12"]) * (L - 12) / 8.0


_MI2_ISCI: Dict[str, Any] = {}


def _mi2_kural_hisse(s: str) -> Tuple[str, List[Dict[str, Any]], int]:
    d = _MI2_ISCI["V"][s]; kural = _MI2_ISCI["kural"]; bas, son = _MI2_ISCI["bas"], _MI2_ISCI["son"]
    O, H, Lw, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); ix = d.index; n = len(C)
    BU, BO, BA = MI.mi_bant(C)
    ara = np.flatnonzero((ix >= bas) & (ix <= son)); m_sec = np.full(n, 0, np.int64)
    for L in range(int(MI2_ESIK["birlesik"]["L"][0]), int(MI2_ESIK["birlesik"]["L"][1]) + 1):
        e = ara[ara - L + 1 >= 19]
        if not len(e):
            continue
        idx = (e - L + 1)[:, None] + np.arange(L)[None, :]
        F = MI.mi_ozellik(O[idx], H[idx], Lw[idx], C[idx], BU[idx], BO[idx], BA[idx])
        ok = np.ones(len(e), bool)
        for k in kural:
            th = _mi2_kural_esik(k, L)
            ok &= (F[k["olcu"]] >= th) if k["uc"] == "YÜKSEK" else (F[k["olcu"]] <= th)
        yeni = e[ok & (m_sec[e] == 0)]
        m_sec[yeni] = L
    t = np.flatnonzero(m_sec > 0)
    t = MI._mi_tekil(t, int(MI2_ESIK["birlesik"]["tekil"])) if len(t) else t
    kon = MI.mi_konum_seri(C, t) if len(t) else []
    ol = [{"sablon": "birlesik", "tarih": ix[tt], "S": 1.0, "m": int(m_sec[tt]), "pencere_bas": ix[tt - m_sec[tt] + 1],
           "pencere_min_low": float(Lw[tt - m_sec[tt] + 1:tt + 1].min()), "C_t": float(C[tt]), "konum": kk, "bar_no": int(tt), "sembol": s}
          for tt, kk in zip(t, kon)]
    return s, ol, int(len(ara))


def mi2_kural_tara(V: Dict[str, pd.DataFrame], kural: List[Dict[str, Any]], pazar: str, islem: int = 3) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    import multiprocessing as mp
    _MI2_ISCI.clear(); _MI2_ISCI.update({"V": V, "kural": kural, "bas": pd.Timestamp(MI2_ESIK["dagilim"]["tarama"][0]),
                                         "son": pd.Timestamp(MI2_ESIK["dagilim"]["tarama"][1])})
    semb = sorted(V); t0 = time.time()
    try:
        if islem > 1 and "fork" in mp.get_all_start_methods():
            with mp.get_context("fork").Pool(islem) as pool:
                sonuc = list(pool.imap(_mi2_kural_hisse, semb, chunksize=16))
        else:
            sonuc = [_mi2_kural_hisse(s) for s in semb]
    finally:
        _MI2_ISCI.clear()
    ol = [r for _, o, _ in sonuc for r in o]; nbar = int(sum(x for _, _, x in sonuc))
    X = pd.DataFrame(ol)
    if len(X):
        X["pazar"] = pazar
    mi2log.info("%s birleşik kural taraması: %d hisse, olay %d (%.0f sn)", pazar, len(semb), len(X), time.time() - t0)
    return X, {"hisse": len(semb), "gun": nbar, "olay": int(len(X)), "olay_1000": 1000.0 * len(X) / max(nbar, 1)}


def mi2_prefix(V: Dict[str, pd.DataFrame], X: pd.DataFrame, kural: List[Dict[str, Any]], n: int = 30) -> Dict[str, Any]:
    """K2: veri t'de kesilince t'deki kural kararı ve m aynı."""
    if not len(X):
        return {"n": 0, "tuttu": True}
    rng = np.random.default_rng(2519); sec = X.iloc[rng.choice(len(X), size=min(n, len(X)), replace=False)]; bozuk = 0
    for r in sec.itertuples():
        d = V[r.sembol]; dk = d[d.index <= r.tarih]
        O, H, Lw, C = (dk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); BU, BO, BA = MI.mi_bant(C); t = len(C) - 1; m0 = 0
        for L in range(12, 21):
            if t - L + 1 < 19:
                continue
            sl = slice(t - L + 1, t + 1)
            F = MI.mi_ozellik(O[sl], H[sl], Lw[sl], C[sl], BU[sl], BO[sl], BA[sl])
            if all(((F[k["olcu"]][0] >= _mi2_kural_esik(k, L)) if k["uc"] == "YÜKSEK" else (F[k["olcu"]][0] <= _mi2_kural_esik(k, L))) for k in kural):
                m0 = L; break
        bozuk += int(m0 != int(r.m))
    if bozuk:
        raise MI2Hata(f"PREFIX TUTMADI: {bozuk} olay")
    return {"n": int(len(sec)), "bozuk": 0, "tuttu": True}


# ================================================================ 4) KAPI ve ÖN KAYIT
def mi2_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    return {"KOD2_SHA": MI._mi_sha(MI2_YOL["kod"]), "ESIK2_SHA": mi2_esik_sha(), "SAYISAL2_SHA": MI._mi_sha(_mi2_yol("sayisal", cikti)),
            "MI_KOD_SHA": MI._mi_sha(MI2_YOL["kod1"])}


def mi2_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK
    cikti = cikti or MI2_YOL["cikti"]; yol = _mi2_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise MI2Hata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read(); bek = mi2_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise MI2Hata(f"ön kayıt kapısı: {ad} farklı (şimdiki {v[:12]}) -> DURDU")
    rel = os.path.relpath(yol, KOK_MI2)
    c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise MI2Hata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "MUM_IZI2.py", "MUM_IZI.py", os.path.relpath(_mi2_yol("sayisal", cikti), KOK_MI2)]):
        raise MI2Hata("ön kayıt / kod / sayısal json çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


def mi2_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    return "\n".join(["| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"] +
                     [f"| {k} | {ad.get(k, k)} | {y} | {kn} |" for k, (y, kn) in MI2_KONTROL.items()])


def mi2_onkayit_yaz(cikti: Optional[str] = None) -> str:
    cikti = cikti or MI2_YOL["cikti"]; y = _mi2_yol("onkayit", cikti)
    if os.path.exists(y):
        raise MI2Hata("ön kayıt zaten var")
    sh = mi2_sha_simdi(cikti); SJ = json.load(open(_mi2_yol("sayisal", cikti), encoding="utf-8"))
    kc = MI._mi_git(["log", "-1", "--format=%H %cI", "--", "MUM_IZI2.py"])
    s = [f"# MUM_IZI2 ÖN KAYIT ({MI._mi_simdi()})", "",
         "Ortak nokta hesabı (yüzdelik dağılımları, karşılaştırma, şans tabanı, birleşik kural) bu dosya commit edildikten SONRA koşar (`mi2_kapi`).",
         "Bu ana kadar yalnız ENSRI görüntüsü sayısallaştırıldı; açık veride hiçbir pencere ölçülmedi.", "", "## Mühürler", "",
         f"KOD2_SHA: {sh['KOD2_SHA']}", f"ESIK2_SHA: {sh['ESIK2_SHA']}", f"SAYISAL2_SHA: {sh['SAYISAL2_SHA']}", f"MI_KOD_SHA: {sh['MI_KOD_SHA']}", "",
         f"- MUM_IZI2.py commit'i: {kc or 'yok'}", f"- Görüntü sha: {SJ['goruntu_sha']}", "",
         "## Sayısallaştırma (görüntüden)", "",
         f"- {SJ['n']} mum, renk {SJ['renk_dizisi']}; kenarda kırpık: {SJ['kenar'] or 'yok'}; alt bandı panel altında kalan mumlar {SJ['alt_gorunmeyen']} "
         f"(E: ilk 4 görünür mumdan doğrusal, eğim {SJ['ekstrapolasyon']['egim_tl_mum']:.3f} TL / mum; T: panel tabanı {SJ['kalibrasyon']['taban_tl']:.3f} TL)",
         f"- TL kalibrasyonu: {len(SJ['kalibrasyon']['etiket_satir'])} etiket, TL = {SJ['kalibrasyon']['a']:.5f} + {SJ['kalibrasyon']['b']:.7f} x satır; en büyük artık "
         f"{SJ['kalibrasyon']['artik_tl_max']:.4f} TL ({SJ['kalibrasyon']['artik_px_max']:.2f} px); ızgara satırı farkı en çok {SJ['kalibrasyon']['izgara_fark_px_max']:.1f} px",
         "- Notlar: " + " ".join(SJ["notlar"]), "",
         "## Yüzdelik dağılımı nasıl kuruldu (ölçümden önce yazıldı)", "", "```", json.dumps(MI2_ESIK["dagilim"], ensure_ascii=False, indent=1), "```", "",
         "## Ortak nokta, şans tabanı, S, birleşik kural (sabit; sonuca göre oynanmaz)", "", "```",
         json.dumps({k: MI2_ESIK[k] for k in ("ortak", "S", "sans", "birlesik", "bant", "olcu")}, ensure_ascii=False, indent=1), "```", "",
         "## Tohumlar", "", f"- dağılım L20 {MI2_ESIK['dagilim']['tohum']['20']}, L12 {MI2_ESIK['dagilim']['tohum']['12']}; şans L20 "
         f"{MI2_ESIK['sans']['tohum']['20']}, L12 {MI2_ESIK['sans']['tohum']['12']} (çift eşleme permütasyonu {MI2_ESIK['sans']['tohum']['20'] + 7}); "
         "elle doğrulama 2518; prefix 2519; birleşik plasebo / eş MUM_IZI tohumları (MI_ESIK['gercek'])", "",
         "## KONTROL LİSTESİ", "", mi2_kontrol_tablosu(), "", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(y, "\n".join(s), "ön kayıt 2")


# ================================================================ 5) KOŞU
def mi2_kos(cikti: Optional[str] = None, acik: Optional[str] = None, kuru: bool = False, plasebo_tohum: Optional[int] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or MI2_YOL["cikti"]; acik = acik or MI2_YOL["acik"]
    if os.path.exists(_mi2_yol("sonuc", cikti)) and not kuru:
        raise MI2Hata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = {"kuru": True} if kuru else mi2_kapi(cikti)
    kasa = MI.mi_kasa_kapi(acik) if not kuru else {"kuru": True}
    SJ = json.load(open(_mi2_yol("sayisal", MI2_YOL["cikti"]), encoding="utf-8"))
    F1 = MI.mi_sablon_yukle()["tam"]["F"]
    V = mi2_veri_hepsi(acik)
    Dg = MI2_ESIK["dagilim"]
    D20 = mi2_orneklem(V, 20, Dg["n"], Dg["tohum"]["20"]); D12 = mi2_orneklem(V, 12, Dg["n"], Dg["tohum"]["12"])
    os.makedirs(MI2_YOL["gecici"], exist_ok=True)
    D20.to_pickle(os.path.join(MI2_YOL["gecici"], "dagilim_L20.pkl")); D12.to_pickle(os.path.join(MI2_YOL["gecici"], "dagilim_L12.pkl"))
    K = mi2_karsilastir(F1, SJ["F_E"], SJ["F_T"], D20, D12)
    K.to_csv(_mi2_yol("karsilastirma", cikti), index=False, float_format="%.5f")
    say = mi2_say(K)
    olc = K[K.sinif != "BELİRSİZ"].olcu.tolist()
    sans = mi2_sans(V, D20, D12, olc, say)
    Sb = mi2_S(SJ["F_E"], D12)
    kural = mi2_kural(K, D20, D12)
    J: Dict[str, Any] = {"surum": MI2_SURUM, "kapi": G0, "kasa": kasa, "dagilim": {"L20": {"n": len(D20), "havuz": D20.attrs.get("havuz"),
                                                                                         "pazar": D20.pazar.value_counts().to_dict()},
                                                                                 "L12": {"n": len(D12), "havuz": D12.attrs.get("havuz"),
                                                                                         "pazar": D12.pazar.value_counts().to_dict()}},
                         "dagilim_sha": {k: MI._mi_sha(os.path.join(MI2_YOL["gecici"], f"dagilim_{k}.pkl")) for k in ("L20", "L12")},
                         "sayim": say, "sans": sans, "S": Sb, "kural": kural, "birlesik": {}, "hucre": {}, "prefix": {}}
    olay = []
    if kural:
        for p in MI2_ESIK["dagilim"]["pazar"]:
            X, ist = mi2_kural_tara(V[p], kural, p)
            J["birlesik"][p] = ist
            J["prefix"][p] = mi2_prefix(V[p], X, kural)
            if len(X):
                Vd = MI.mi_veri(p, acik)
                A, info = MI.mi_sonrasi(X, Vd, p, {"birlesik": None}, acik, plasebo=True, tohum_sayi=plasebo_tohum)
                J["hucre"].update(info.pop("hucre", {})); p2t = info.pop("p2_tablo", None); J["birlesik"][p]["info"] = info
                X2 = X.copy(); X2["tarih"] = pd.to_datetime(X2.tarih)
                if len(A):
                    A2 = A.copy(); A2["tarih"] = pd.to_datetime(A2.tarih)
                    ek = [c for c in A2.columns if c not in X2.columns or c in ("sembol", "tarih", "sablon")]
                    X2 = X2.merge(A2[ek], on=["sembol", "tarih", "sablon"], how="left", validate="one_to_one")
                if p2t is not None and len(p2t):
                    X2 = X2.merge(p2t.assign(tarih=pd.to_datetime(p2t.tarih)), on=["sembol", "tarih", "sablon"], how="left", validate="one_to_one")
                olay.append(X2)
                kv = X.konum.value_counts(); n = len(X)
                J["birlesik"][p]["konum"] = {**{k: int(kv.get(k, 0)) for k in ("TEPE", "DIP", "ORTA", "KISA")},
                                             "tepe_pay": float(kv.get("TEPE", 0) / n), "baska_pay": float((kv.get("DIP", 0) + kv.get("ORTA", 0)) / n)}
                del Vd
            gc.collect()
    Ol = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame()
    if len(Ol):
        for c in ("tarih", "pencere_bas", "giris"):
            if c in Ol.columns:
                Ol[c] = pd.to_datetime(Ol[c]).dt.strftime("%Y-%m-%d")
        eg = pd.to_datetime(Ol.tarih).max()
        if eg > MI.MI_KESIK:
            raise MI2Hata(f"KESİK AŞIMI {eg}")
        kol = ["pazar", "sembol", "tarih", "m", "pencere_bas", "pencere_min_low", "C_t", "konum", "p2", "giris", "donem", "kova", "r15", "es_r15",
               "n_es", "sira", "fark", "h5", "st5", "h5_es"]
        Ol = Ol[[c for c in kol if c in Ol.columns]]
        Ol.to_csv(_mi2_yol("birlesik", cikti), index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.10g")
        J["birlesik_satir_sha"] = MI._mi_sha(_mi2_yol("birlesik", cikti))
    J["yeniden"] = mi2_yeniden(K, D20, D12, SJ, V, Ol, kural)
    J["sure_sn"] = round(time.time() - t0); J["bitis"] = MI._mi_simdi()
    MI._mi_jyaz(_mi2_yol("sonuc", cikti), J, "sonuç 2")
    mi2log.info("kos bitti: ortak %s, şans %.2f (ust95 %.1f), kural %d ölçü (%.0f sn)", say, sans["ORTAK_DAHIL"]["ort"], sans["ORTAK_DAHIL"]["ust95"],
                len(kural), time.time() - t0)
    return J


def mi2_yeniden(K: pd.DataFrame, D20: pd.DataFrame, D12: pd.DataFrame, SJ: Dict[str, Any], V: Dict[str, Any], Ol: pd.DataFrame,
                kural: List[Dict[str, Any]]) -> Dict[str, Any]:
    """K11: iz 2'nin iki ölçüsü düz döngüyle; iki yüzdelik düz pandas; birleşik olaylarda 10 olayda kural düz denetimi."""
    T = pd.read_csv(_mi2_yol("mumlar"))
    O_, H_, L_, C_ = (T[c].tolist() for c in ("O", "H", "L", "C")); m = len(C_)
    rg = [max(H_[i] - L_[i], 1e-12) for i in range(m)]; u = sum(rg) / m
    ust = sum(max(H_[i] - max(O_[i], C_[i]), 0) / rg[i] for i in range(m)) / m
    xm = (m - 1) / 2; cm = sum(c / u for c in C_) / m
    eg = sum((i - xm) * (C_[i] / u - cm) for i in range(m)) / sum((i - xm) ** 2 for i in range(m))
    out = {"ust_fitil": {"duz": ust, "kod": SJ["F_E"]["ust_fitil"]}, "kapanis_egim": {"duz": eg, "kod": SJ["F_E"]["kapanis_egim"]}}
    for k in ("ust_fitil", "pB_son"):
        r = K[K.olcu == k].iloc[0]
        p1 = float(((D20[k] < r.iz1).sum() + 0.5 * (D20[k] == r.iz1).sum()) / len(D20))
        p2 = float(((D12[k] < r.iz2).sum() + 0.5 * (D12[k] == r.iz2).sum()) / len(D12))
        out[f"p_{k}"] = {"duz": [p1, p2], "kod": [float(r.p1), float(r.p2)]}
    ok = all(abs(v["duz"] - v["kod"]) < 1e-6 for k, v in out.items() if not k.startswith("p_")) and \
        all(max(abs(a - b) for a, b in zip(v["duz"], v["kod"])) < 1e-12 for k, v in out.items() if k.startswith("p_"))
    if len(Ol) and kural:
        x = Ol.sample(n=min(10, len(Ol)), random_state=2520); hata = 0
        for r in x.itertuples():
            d = V[r.pazar][r.sembol]; t = int(d.index.get_loc(pd.Timestamp(r.tarih))); Lm = int(r.m)
            C = d.Close.to_numpy(float); sl = slice(t - Lm + 1, t + 1); BU, BO, BA = MI.mi_bant(C)
            F = MI.mi_ozellik(d.Open.to_numpy(float)[sl], d.High.to_numpy(float)[sl], d.Low.to_numpy(float)[sl], C[sl], BU[sl], BO[sl], BA[sl])
            for k in kural:
                th = _mi2_kural_esik(k, Lm); v = float(F[k["olcu"]][0])
                hata += int(not (v >= th if k["uc"] == "YÜKSEK" else v <= th))
        out["kural_10_olay_ihlal"] = hata; ok = ok and hata == 0
    out["tuttu"] = bool(ok)
    return out


# ================================================================ 6) GÖRSEL ve RAPOR
def mi2_gorsel(cikti: Optional[str] = None, acik: Optional[str] = None) -> str:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from PIL import Image
    cikti = cikti or MI2_YOL["cikti"]; acik = acik or MI2_YOL["acik"]
    J = json.load(open(_mi2_yol("sonuc", cikti), encoding="utf-8")); SJ = json.load(open(_mi2_yol("sayisal", cikti), encoding="utf-8"))
    K = pd.read_csv(_mi2_yol("karsilastirma", cikti)); T2 = pd.read_csv(_mi2_yol("mumlar", cikti))
    T1 = pd.read_csv(MI._mi_yol("mumlar")); B1 = T1[T1.sinif == "BOLGE"].reset_index(drop=True)
    y = _mi2_yol("pdf", cikti)
    with PdfPages(y, metadata={"Title": "MUM_IZI2", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(11.7, 8.3))
        for k, (img, bas) in enumerate(((MI.MI_YOL["goruntu"], "iz 1: Cemal'in ilk grafiği (4 saatlik)"), (_mi2_yol("bindirme", cikti), "iz 2: ENSRI (aylık) + kodun gördüğü"))):
            ax = fig.add_axes([0.01 + 0.25 * k, 0.05, 0.24, 0.88]); ax.imshow(Image.open(img)); ax.axis("off"); ax.set_title(bas, fontsize=8)
        for k, (B, bas, ba) in enumerate(((B1, "iz 1: 20 mum (piksel)", "BA"), (T2, "iz 2: 12 mum (TL; alt bant E senaryosu)", "BA_E"))):
            ax = fig.add_axes([0.53, 0.55 - 0.47 * k, 0.45, 0.38])
            MI._mi_mum_ciz(ax, B.O.to_numpy(), B.H.to_numpy(), B.L.to_numpy(), B.C.to_numpy())
            xx = np.arange(len(B)); ax.plot(xx, B.BU.to_numpy(), color="#9e8fd6"); ax.plot(xx, B[ba].to_numpy(), color="#9e8fd6")
            ax.plot(xx, (B.BU.to_numpy() + B[ba].to_numpy()) / 2, color="#9e8fd6", linestyle="--")
            ax.set_title(bas, fontsize=8); ax.tick_params(labelsize=6)
            if k == 1:
                ax.set_ylim(min(B.L.min(), 1.5), B.BU.max() * 1.05)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.93]); ax.axis("off")
        sat = [[r.olcu, r.aciklama[:52], f"{r.iz1:.2f}", f"{r.iz2:.2f}", f"{r.p1:.2f}", f"{r.p2:.2f}", r.sinif] for r in K.itertuples()]
        tb = ax.table(cellText=sat, colLabels=["ölçü", "düz dil", "iz 1", "iz 2", "p1", "p2", "sınıf"], loc="upper center", cellLoc="left",
                      colWidths=[0.17, 0.47, 0.07, 0.07, 0.06, 0.06, 0.13])
        tb.auto_set_font_size(False); tb.set_fontsize(6.2)
        for (rr, cc), cell in tb.get_celld().items():
            if rr > 0 and cc == 6:
                v = sat[rr - 1][6]
                cell.set_facecolor({"GÜÇLÜ ORTAK": "#a6d96a", "ORTAK": "#d9ef8b", "ZIT": "#fdae61", "BELİRSİZ": "#e0e0e0"}.get(v, "white"))
        s = J["sayim"]
        ax.set_title(f"ORTAK NOKTALAR: GÜÇLÜ ORTAK {s['GUCLU']}, ORTAK (güçlü dahil) {s['ORTAK_DAHIL']}, ZIT {s['ZIT']}, AYRI {s['AYRI']}, BELİRSİZ {s['BELIRSIZ']}\n"
                     "p = açık verideki rastgele pencerelerin yüzde kaçının altında (0 en düşük, 1 en yüksek)", fontsize=8.5)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(11.7, 8.3)); a1 = fig.add_axes([0.06, 0.55, 0.4, 0.38])
        h = np.array(J["sans"]["hist_ortak"]); a1.bar(np.arange(len(h)), h / h.sum(), color="#9e9ac8")
        a1.axvline(J["sayim"]["ORTAK_DAHIL"], color="#d73027", linewidth=2, label=f"iki iz: {J['sayim']['ORTAK_DAHIL']}")
        a1.axvline(J["sans"]["ORTAK_DAHIL"]["ust95"], color="#333333", linestyle="--", label=f"rastgele %95 üst: {J['sans']['ORTAK_DAHIL']['ust95']:.0f}")
        a1.set_title(f"Şans tabanı: rastgele {J['sans']['cift']} pencere çiftinde ORTAK sayısı (ort {J['sans']['ORTAK_DAHIL']['ort']:.2f})", fontsize=8)
        a1.legend(fontsize=7); a1.tick_params(labelsize=7)
        a2 = fig.add_axes([0.5, 0.05, 0.48, 0.9]); a2.axis("off")
        txt = [f"S: {J['S']['S']} ({J['S']['neden']}); ölçü uzaklığı D_oz {J['S']['D_oz']:.2f} (tau {J['S']['tau_oz']:.2f}); rastgele L12 pencerelerin "
               f"%{100 * J['S']['rastgele_L12_D_oz_yuzdelik']:.0f}'i iz 1'e daha yakın", "",
               "BİRLEŞİK KURAL (BİLGİ, EZBER RİSKLİ): " + (", ".join(f"{k['olcu']} {k['uc']}" for k in J["kural"]) or "kural yok (ortak ölçü yok)")]
        for p, v in J["birlesik"].items():
            txt.append(f"{p}: {v['olay']} olay ({v['olay_1000']:.2f} / 1.000 gün), tepede %{100 * v.get('konum', {}).get('tepe_pay', float('nan')):.0f}")
        for k_, c in J["hucre"].items():
            pl = c.get("plasebo") or {}
            if k_.split("|")[2] != "hepsi":
                continue
            pls = f"%{100 * pl['tutar_pay']:.0f}" if pl.get("tutar_pay") is not None else "-"
            txt.append(f"{k_}: n {c.get('n')}, R15 eşli fark {100 * c['fark']:+.2f} puan, +%5 %{100 * c['h5']:.0f} / eş %{100 * c['h5_es']:.0f}, "
                       f"plasebo TUTAR {pls}" if c.get("n", 0) >= 30 and c.get("fark") is not None else f"{k_}: n {c.get('n')} (örneklem yetersiz)")
        import textwrap
        a2.text(0, 1, "\n".join(textwrap.fill(t, 95) if t else t for t in txt), fontsize=6.8, va="top")
        pdf.savefig(fig); plt.close(fig)
        if os.path.exists(_mi2_yol("birlesik", cikti)):
            Ol = pd.read_csv(_mi2_yol("birlesik", cikti)); Ol = Ol[pd.to_datetime(Ol.tarih) <= MI.MI_KESIK - pd.Timedelta(days=30)]
            if len(Ol):
                x = Ol.sample(n=min(8, len(Ol)), random_state=2521); Vc: Dict[str, Any] = {}
                for i0 in range(0, len(x), 4):
                    fig, axs = plt.subplots(2, 2, figsize=(11.7, 8.3)); axs = axs.ravel()
                    for k_, r in enumerate(x.iloc[i0:i0 + 4].itertuples()):
                        if r.pazar not in Vc:
                            Vc[r.pazar] = MI.mi_veri(r.pazar, acik)["V"]
                        r15 = f"{100 * r.r15:+.1f}%" if pd.notna(getattr(r, "r15", np.nan)) else "-"
                        MI.mi_olay_ciz(axs[k_], Vc[r.pazar][r.sembol], r, f"birleşik kural | rastgele | {r.pazar} {r.sembol} {r.tarih} | {r.m} mum | {r.konum}\nR15 {r15}")
                    for k_ in range(len(x.iloc[i0:i0 + 4]), 4):
                        axs[k_].axis("off")
                    fig.suptitle("BİRLEŞİK KURAL eşleşmeleri (rastgele 8; EZBER RİSKLİ, bilgi)", fontsize=9)
                    fig.tight_layout(rect=[0, 0, 1, 0.96]); pdf.savefig(fig); plt.close(fig)
    return y


def mi2_rapor(cikti: Optional[str] = None) -> str:
    cikti = cikti or MI2_YOL["cikti"]
    J = json.load(open(_mi2_yol("sonuc", cikti), encoding="utf-8")); SJ = json.load(open(_mi2_yol("sayisal", cikti), encoding="utf-8"))
    K = pd.read_csv(_mi2_yol("karsilastirma", cikti)); s = J["sayim"]; sn = J["sans"]
    L = [f"# MUM_IZI2 RAPOR ({MI._mi_simdi()})", "", f"Sürüm: {MI2_SURUM}", "", "## SAYISALLAŞTIRMA", "",
         f"- {SJ['n']} mum, renk {SJ['renk_dizisi']}, kenar: {SJ['kenar']}; alt bandı görünmeyen mumlar {SJ['alt_gorunmeyen']}",
         f"- TL = {SJ['kalibrasyon']['a']:.4f} + {SJ['kalibrasyon']['b']:.6f} x satır ({len(SJ['kalibrasyon']['etiket_satir'])} etiket); en büyük artık "
         f"{SJ['kalibrasyon']['artik_tl_max']:.4f} TL = {SJ['kalibrasyon']['artik_px_max']:.2f} px; ızgara farkı {SJ['kalibrasyon']['izgara_fark_px_max']:.1f} px",
         f"- Elle doğrulama: {SJ['elle']['mumlar']}", "", "## ORTAK NOKTALAR", "",
         f"GÜÇLÜ ORTAK {s['GUCLU']}, ORTAK (güçlü dahil) {s['ORTAK_DAHIL']}, ZIT {s['ZIT']}, AYRI {s['AYRI']}, BELİRSİZ {s['BELIRSIZ']} (toplam {s['olcu']} ölçü)", "",
         "| ölçü | düz dil | iz 1 | iz 2 | p1 | p2 | sınıf |", "|---|---|---|---|---|---|---|"]
    for r in K.itertuples():
        L.append(f"| {r.olcu} | {r.aciklama} | {r.iz1:.3f} | {r.iz2:.3f} | {r.p1:.3f} | {r.p2:.3f} | {r.sinif}{' (' + r.uc + ')' if isinstance(r.uc, str) and r.uc else ''} |")
    L += ["", f"S: {J['S']}", "", "## ŞANS TABANI", "",
          f"- {sn['cift']} rastgele çift, {sn['olcu_sayisi']} ölçü: ORTAK (güçlü dahil) ort {sn['ORTAK_DAHIL']['ort']:.2f}, %95 üst {sn['ORTAK_DAHIL']['ust95']:.0f}, "
          f"iki iz {sn['ORTAK_DAHIL']['gozlenen']} (rastgele çiftlerin %{100 * sn['ORTAK_DAHIL']['pay_ge_gozlenen']:.1f}'i >= bu sayı)",
          f"- GÜÇLÜ ORTAK ort {sn['GUCLU']['ort']:.2f}, %95 üst {sn['GUCLU']['ust95']:.0f}, iki iz {sn['GUCLU']['gozlenen']} (pay %{100 * sn['GUCLU']['pay_ge_gozlenen']:.1f})",
          f"- ZIT ort {sn['ZIT']['ort']:.2f}, %95 üst {sn['ZIT']['ust95']:.0f}, iki iz {sn['ZIT']['gozlenen']}", "",
          "## BİRLEŞİK KURAL (BİLGİ, EZBER RİSKLİ)", "", f"Kural: {J['kural']}", ""]
    for p, v in J["birlesik"].items():
        L.append(f"- {p}: {v['olay']} olay / {v['gun']} gün ({v['olay_1000']:.2f} / 1.000), konum {v.get('konum')}, prefix {J['prefix'].get(p)}")
    L += ["", "| hücre | n | R15 eşli fark | boot %95 | SIRA | güç | +%5 olay | +%5 eş | plasebo fark / TUTAR payı | C2 hüküm (bilgi) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in J["hucre"].items():
        pl = c.get("plasebo") or {}
        L.append(f"| {k} | {c.get('n')} | {MI._p(c.get('fark'), 2)} | {MI._p(c.get('boot_alt'), 2)}..{MI._p(c.get('boot_ust'), 2)} | {MI._s(c.get('sira'), 3)} | "
                 f"{MI._s(c.get('guc'))} | {MI._p(c.get('h5'), 0)} | {MI._p(c.get('h5_es'), 0)} | {MI._p(pl.get('fark_ort'), 2)} / {MI._p(pl.get('tutar_pay'), 0)} | "
                 f"{c.get('hukum') if c.get('n', 0) >= 30 else 'örneklem yetersiz'} |")
    L += ["", f"Yeniden üretim (K11): {J['yeniden']}", f"Kapı: {J['kapi']}", f"KASA: {J['kasa']}", ""]
    return MI._mi_yaz(_mi2_yol("rapor", cikti), "\n".join(L), "rapor 2")


# ================================================================ 7) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_mi2(_once=_CK_ONCE_MI2, _dosya="MUM_IZI2.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_MI2",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_mi2()


def _mi2_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI2: ENSRI parmak izi ve ortak noktalar")
    ap.add_argument("komut", choices=["sayisallastir", "onkayit", "kos", "gorsel", "rapor", "sha"])
    ap.add_argument("--plasebo_tohum", type=int, default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps(mi2_sha_simdi() if os.path.exists(_mi2_yol("sayisal")) else {"KOD2_SHA": MI._mi_sha(MI2_YOL["kod"]), "ESIK2_SHA": mi2_esik_sha()}, indent=1))
        elif a.komut == "sayisallastir":
            J = mi2_sayisallastir_kos()
            print(json.dumps(MI._mi_json({k: J[k] for k in ("n", "renk_dizisi", "kenar", "alt_gorunmeyen")}), ensure_ascii=False))
        elif a.komut == "onkayit":
            print(mi2_onkayit_yaz())
        elif a.komut == "kos":
            J = mi2_kos(plasebo_tohum=a.plasebo_tohum)
            print(json.dumps(MI._mi_json({k: J[k] for k in ("sayim", "S", "kural", "yeniden")}), ensure_ascii=False)[:4000])
        elif a.komut == "gorsel":
            print(mi2_gorsel())
        elif a.komut == "rapor":
            print(mi2_rapor())
    except MI2Hata as ex:
        mi2log.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_mi2_ana())
