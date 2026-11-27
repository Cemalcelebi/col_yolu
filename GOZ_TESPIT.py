"""GOZ_TESPIT — kodun 'aynı' dediği bölge Cemal'in gözünün gördüğü bölge mi: kitaplıktan çok ölçülü PARMAK İZİ, üç dedektör, rastgele kontrollü
KÖR ONAY SETİ (27 Kasım 2026).

İş tanımı: arastirma_cikti/goz_tespit/GT_IS_TANIMI.md (ana model). Bu iş YALNIZ TESPİT içindir: hiçbir bölgenin sonrası / getirisi hesaplanmaz, çizilmez.
  ADIM A (parmak): Cemal'in çöl kitaplığındaki bölgelerin (COL_SKOR6.CS_KITAPLIK; verisi olanlar) 40 ölçüsü, BIST 2016-22 aynı uzunluk sınıfı (L* = 20 / 40 / 80)
         pencerelerinin dağılımında yüzdelik sıra; ölçü başına medyan sıra + tutarlılık; İMZA ölçüleri; mum izi ✓ / ✗ AUC bilgi tablosu.
  ADIM B (dedektor): D1 ESKİ PUAN (COL_SKOR6 PUAN_ESIT üst %10), D2 İMZA (imza ölçülerinin hepsi kitaplığın tarafında ve gevşek %20 sınırı içinde),
         D3 EN YAKIN KOMŞU (standart imza uzayında her çölün en yakın penceresi); BIST ve ABD havuzunda kaç pencere seçtikleri.
  ADIM C (onay): 30 sayfa (D1 6, D2 8, D3 6, RASTGELE 6, KİTAPLIK 4; tohum 2715 karışık sıra), geçmişli + yüzde eksenli sayfa, üç kutu (✓ çöl / K kısmen /
         × değil); mühürlü anahtar (sayfa -> kol, pazar, sembol, tarih, puan) PDF'e girmez.
Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır: COL_SKOR6 (F1..F6, PUAN_ESIT, kitaplık listesi, yüzdelik), MUM_IZI_UC (12 ölçü, kilitli pay), YUKSELIS_ONCESI
(fiyat ölçüleri, pazar endeksi, kesit sırası), MUM_IZI_HAKEM (geçmişli sayfa grafiği, yüzde ekseni, sınır), MUM_IZI / MUM_IZI_V2 (veri, bant, mum çizimi, yazma).
Aday havuzu verisi <= 2022-12-31 (assert); kitaplık bölgeleri (BIST 2024-26) yalnız ölçü ve çizim için, bölge bitişinde KESİLEREK okunur (assert).

Komut:  python GOZ_TESPIT.py olcu       kitaplık + BIST / ABD / AVR pencere ölçüleri + mum izi bölgeleri (ham: /root/.kasa/ham/goz_tespit)
        python GOZ_TESPIT.py parmak     ADIM A -> GT_PARMAK_IZI.md + gt_parmak.json
        python GOZ_TESPIT.py dedektor   ADIM B (kapı: GT_PARMAK_IZI.md commit + push) -> GT_DEDEKTOR.md + gt_dedektor.json
        python GOZ_TESPIT.py onay       ADIM C (kapı: GT_DEDEKTOR.md commit + push + kontrol tablosu) -> GT_ONAY.pdf + GT_onay_anahtar.json (mühürlü)
        python GOZ_TESPIT.py rapor      GT_RAPOR.md + gt_sonuc.json
        python GOZ_TESPIT.py sha        kod / eşik sha
        python GOZ_TESPIT.py k2esles    ÇÖL-K2 (EK 5): goz2 GT3 (32) + GT4 (20) sayfalarının beş şartı gt_k2 ile birebir mi
        python GOZ_TESPIT.py k2olay     ÇÖL-K2 olay listesi (getirisiz; K2 / YMSB / Y) -> gt5_olay.json + /root/.kasa/ham/goz_tespit/k2/
        python GOZ_TESPIT.py k2olc      ÇÖL-K2 sonrası (kapı: GT5_ON_KAYIT.md commit + push + kontrol listesi; bir kez) -> gt5_sonuc.json, gt5_ozet.json
        python GOZ_TESPIT.py k2kirsay   ÇÖL-K2 KIRILIM (EK 6): getirisiz sayım (bölge, izleme kesik, Kontrol 1 pencere) -> gt6_sayim.json
        python GOZ_TESPIT.py k2kirolc   ÇÖL-K2 KIRILIM yön + kırılım sonrası (kapı: GT6_ON_KAYIT.md commit + push + kontrol listesi; bir kez) -> gt6_ozet.json
Colab:  exec(open('GOZ_TESPIT.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_GT = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_GT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_GT not in sys.path:
    sys.path.insert(0, KOK_GT)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; veri, bant, yazma, sha)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ; açık kopya yolu, mum çizimi)
import COL_SKOR6 as CS  # noqa: E402  (DEĞİŞTİRİLMEZ; F1..F6, PUAN_ESIT, kitaplık, yüzdelik)
import MUM_IZI_UC as UC  # noqa: E402  (DEĞİŞTİRİLMEZ; 12 ölçü, kilitli pay)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; fiyat ölçüleri, endeks, kesit sırası)
import MUM_IZI_HAKEM as HK  # noqa: E402  (DEĞİŞTİRİLMEZ; geçmişli sayfa grafiği)

gtlog = logging.getLogger("col.goz_tespit")
if not gtlog.handlers:
    _gt_h = logging.StreamHandler(sys.stderr)
    _gt_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s goz_tespit: %(message)s", "%H:%M:%S"))
    gtlog.addHandler(_gt_h)
    gtlog.setLevel(logging.INFO)
    gtlog.propagate = False


class GTHata(RuntimeError):
    """Durdurucu hata: kapı / kesik / geleceğe bakma / şema / sıra uyuşmazlığı."""


GT_SURUM = "GOZ_TESPIT v1.0 (2026-11-27): kitaplık parmak izi + üç dedektör + kör onay seti (yalnız tespit; getiri yok)"
GT_YOL = {"cikti": os.path.join(KOK_GT, "arastirma_cikti", "goz_tespit"), "kod": os.path.join(KOK_GT, "GOZ_TESPIT.py"),
          "ham": os.environ.get("GT_HAM", "/root/.kasa/ham/goz_tespit"), "acik": MV.MV_YOL["gunluk"], "tam_bist": "/tmp/veri",
          "mumizi": os.path.join(KOK_GT, "arastirma_cikti", "mum_izi", "mum_izi23_olay.csv")}
GT_DOSYA = {"parmak_md": "GT_PARMAK_IZI.md", "parmak": "gt_parmak.json", "dedektor_md": "GT_DEDEKTOR.md", "dedektor": "gt_dedektor.json",
            "pdf": "GT_ONAY.pdf", "anahtar": "GT_onay_anahtar.json", "rapor": "GT_RAPOR.md", "sonuc": "gt_sonuc.json"}
GT_KESIK = pd.Timestamp("2022-12-31")
GT_PAZAR = ("BIST", "ABD", "AVR")          # AVR yalnız mum izi bilgi tablosu için (havuz BIST + ABD)
GT_HAVUZ_PAZAR = ("BIST", "ABD")
GT_L = (20, 40, 80)

# ================================================================ ÖLÇÜLER (40; tanımlar mevcut modüllerden AYNEN, ek bölge içi 7 ölçü burada)
GT_OLCU: List[Tuple[str, str, str]] = [
    ("F1", "COL_SKOR6", "doji oranı (gövde / boy < 0,40 mum payı)"),
    ("F2", "COL_SKOR6", "Bollinger genişliği daralması"),
    ("F3", "COL_SKOR6", "daralmanın başladığı genişlik (BBW başı / 0,6)"),
    ("F4", "COL_SKOR6", "fiyat sıkışması (1 - aralık / orta)"),
    ("F5", "COL_SKOR6", "sol bacak düşüşü (önceki 30 bar tepesinden bölge dibine)"),
    ("F6", "COL_SKOR6", "hacim azalması (1 - bölge / önceki 200 bar)"),
    ("BOY_YUZDE_ORAN", "MUM_IZI_UC", "mum boyu (%) / önceki 120 barın mum boyu"),
    ("BOY_GRAFIK_ORAN", "MUM_IZI_UC", "mum boyu (fiyat) / önceki 120 bar"),
    ("BOY_MUTLAK", "MUM_IZI_UC", "mum boyu medyanı (% fiyat)"),
    ("GOVDE_ORAN", "MUM_IZI_UC", "gövde (%) / önceki 120 bar"),
    ("GOVDE_BOY", "MUM_IZI_UC", "gövde / mum boyu medyanı"),
    ("UST_FITIL", "MUM_IZI_UC", "üst fitil / mum boyu medyanı"),
    ("ALT_FITIL", "MUM_IZI_UC", "alt fitil / mum boyu medyanı"),
    ("UST_ALT_PAY", "MUM_IZI_UC", "üst fitili alttan uzun mum payı"),
    ("SON_UST_FITIL", "MUM_IZI_UC", "son üçte birde üst fitil medyanı"),
    ("DARALMA", "MUM_IZI_UC", "bant genişliği bitiş / başlangıç - 1"),
    ("BANT_SON", "MUM_IZI_UC", "son üçte birde banttaki yerin 0,85'e yakınlığı (-|bc - 0,85|)"),
    ("ONCEKI_DUSUS", "MUM_IZI_UC", "bölge dibi / önceki 60 bar tepesi - 1 (%)"),
    ("MIKRO", "YUKSELIS_ONCESI", "son 60 barda art arda >= 3 yükselen kapanış serisi sayısı"),
    ("RS_UZAK", "YUKSELIS_ONCESI", "göreli güç / son 60 bar en yüksek göreli güç - 1"),
    ("OYN_SIRA", "YUKSELIS_ONCESI", "60 günlük oynaklığın aynı gün pazar içi sırası"),
    ("MA_KOD", "YUKSELIS_ONCESI", "SMA20 / 50 / 200 dizilim kodu (0 aşağı .. 3 yukarı)"),
    ("MA_EGIM_DEG", "YUKSELIS_ONCESI", "SMA20 eğiminin 10 barlık değişimi"),
    ("ZIRVE_BAR", "YUKSELIS_ONCESI", "250 bar zirvesinden bu yana bar"),
    ("ZIRVE_DUSUS", "YUKSELIS_ONCESI", "kapanış / 250 bar zirvesi - 1"),
    ("DIP_BAR", "YUKSELIS_ONCESI", "zirveden sonraki dipten bu yana bar"),
    ("DIP_HIZ", "YUKSELIS_ONCESI", "dipten toparlanma hızı (% / bar)"),
    ("CLV10", "YUKSELIS_ONCESI", "son 10 barda kapanışın mum içindeki yeri"),
    ("YUKSELEN_DIP", "YUKSELIS_ONCESI", "art arda yükselen yerel dip sayısı"),
    ("MOM_12_1", "YUKSELIS_ONCESI", "12-1 ay momentumu"),
    ("F15", "YUKSELIS_ONCESI", "15 barlık geçmiş getiri"),
    ("KONUM120", "YUKSELIS_ONCESI", "son 120 kapanış aralığında konum"),
    ("ATRP20", "YUKSELIS_ONCESI", "ATR20 / kapanış"),
    ("DIP_YER", "EK", "bölge dibinin bölgedeki yeri (0 = ilk bar, 1 = son bar)"),
    ("DIP_DOKUNMA", "EK", "dip savunması: dipten en çok 0,5 ATR yukarıda kapanan bar payı"),
    ("SON_KONUM", "EK", "bölge sonu kapanışının bölge aralığındaki yeri"),
    ("BOLGE_L", "EK", "bölge uzunluğu (bar)"),
    ("YUK_KAPANIS", "EK", "bölge içi yükselen kapanış payı"),
    ("HACIM_ORAN", "EK", "bölge hacmi / önceki 200 bar hacmi"),
    ("HACIM_SON5", "EK", "bölge sonu 5 barın hacmi / bölge ortalaması"),
]
GT_OLCU_AD = [a for a, _, _ in GT_OLCU]
GT_UC_AD = list(UC.UC_OLCU_AD)
GT_YO_AD = [a for a, k, _ in GT_OLCU if k == "YUKSELIS_ONCESI"]
GT_EK_AD = [a for a, k, _ in GT_OLCU if k == "EK"]
GT_IMZA_DISI = {"BOLGE_L": "karşılaştırma evreninde sabit (= L*): sırası anlamsız; imzaya girmez (bilgi)"}

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (iş tanımındaki sayılar; sonuçtan sonra DEĞİŞMEZ)
GT_ESIK: Dict[str, Any] = {
    "surum": "GT-1.0",
    "tohum": 2715,
    "evren": {"tanim": "pencere sonu t = hissenin kendi geçerli bar indeksi k, k % 5 == 0 (COL_SKOR6 örneklemesi); pencere sonu tarihi 2016-01-01 .. "
                       "2022-12-31; s = t - L + 1 >= 30; COL_SKOR6 kilitli pay <= 0,20; PUAN_ESIT sonlu (COL_SKOR6.cs_dag_maske ile aynı); her ölçünün sırası "
                       "aynı L'deki evren pencerelerinden o ölçüsü sonlu olanlara göre ((küçük + 0,5 eşit) / n; COL_SKOR6.cs_yuzdelik)",
              "bas": "2016-01-01", "son": "2022-12-31", "adim": 5, "sol": 30, "kilitli": 0.20},
    "havuz": {"tanim": "evren + s >= 120 (MUM_IZI_UC ölçüleri ve 120 barlık uzak görünüm) + pencerede açılış = kapanış (gövdesiz, fiyat adımına yapışmış) bar "
                       "payı <= 0,30 + PUAN_ESIT ve bütün imza ölçüleri sonlu + kitaplık bölgeleri ve aynı hissede onlarla örtüşen pencereler çıkar + Cemal'e "
                       "daha önce gösterilmiş mum izi bölgeleriyle (mum_izi23_olay.csv; aynı pazar / hisse, takvim örtüşmesi) örtüşen pencereler çıkar",
              "on_bar": 120, "govdesiz": 0.30},
    "imza": {"tutarlilik": 0.75, "taraf_ust": 0.70, "taraf_alt": 0.30, "medyan_ust": 0.75, "medyan_alt": 0.25, "rho": 0.80, "n_oran": 0.75,
             "tanim": "TUTARLILIK = medyanın tarafında (>= 0,70 ya da <= 0,30) kalan bölge payı (ölçüsü olan bölgeler); İMZA <=> tutarlılık >= 0,75 VE medyan "
                      "sıra >= 0,75 ya da <= 0,25 VE ölçüsü olan bölge >= %75 (16'da 12); sıra ilişkisi (evren Spearman, üç L'nin en büyük |rho|'su) > 0,80 "
                      "çiftlerden tutarlılığı düşük olan atılır (eşitlikte medyanı 0,5'ten uzak olan kalır)"},
    "D1": {"ust": 0.90, "tanim": "PUAN_ESIT'in kendi pazarı ve L'deki evren sırası >= 0,90 (üst %10); sıralama = bu sıra (eşitlikte ham puan)"},
    "D2": {"gevsek": 0.20, "taraf": 0.50,
           "tanim": "her imza ölçüsünde kitaplık yönüne çevrilmiş sıra (DÜŞÜK yönlüde 1 - sıra) >= maks(0,50; kitaplık yönlü sıralarının alttan "
                    "(n - ceil(0,8 n)). değeri) (16'da 13 çölün sağladığı sınır); sıralama = yönlü imza sıralarının ortalaması"},
    "D3": {"tanim": "standart imza uzayı: z = Φ⁻¹(yönlü sıra, [0,001; 0,999] kırpık); uzaklık = ortak sonlu boyutlarda karekök ortalama kare fark; her kitaplık "
                    "çölünün aynı L* sınıfında, kendisinden farklı hissedeki en yakın havuz penceresi (pazar başına; çöller sırayla, daha önce seçilen hisse "
                    "atlanır); sıralama = uzaklık (küçük önce)"},
    "tekil": {"bar": 40, "tanim": "her dedektörde aynı hissede pencere sonları arasında < 40 bar olan pencerelerden yalnız en yüksek sıralı olan kalır "
                                  "(L = 20 / 40 / 80 dahil; açgözlü, sıra büyükten küçüğe)"},
    "kol": {"D1": 6, "D2": 8, "D3": 6, "RASTGELE": 6, "KITAPLIK": 4},
    "kol_pazar": {"D1": {"BIST": 3, "ABD": 3}, "D2": {"BIST": 4, "ABD": 4}, "D3": {"BIST": 3, "ABD": 3}, "RASTGELE": {"BIST": 3, "ABD": 3},
                  "KITAPLIK": {"BIST": 4}},
    "secim": {"tanim": "dedektör sayfaları her dedektörün tekilleştirilmiş sıralamasının EN ÜSTÜNDEN (pazar başına kol_pazar kadar); bütün sette her hisse en "
                       "çok bir kez; sıra KITAPLIK (rng ile 4 çöl) -> D1 -> D2 -> D3 -> RASTGELE; bir kolun penceresi önceki kolda seçildiyse / hissesi "
                       "kullanıldıysa sıradaki alınır; D2'de bir pazarda yeterli pencere yoksa öteki pazarın D2 sıralamasından tamamlanır, yine eksikse eksik "
                       "kalır (RASTGELE'ye eklenmez); RASTGELE: pazar başına 3 pencere, L'leri o pazarın dedektör sayfalarının L'lerinden rng ile çekilir "
                       "(yerine koymadan), pencere aynı havuzdan o L'de rng ile tekdüze; tek rng np.random.default_rng(2715), çağrı sırası sabit; en son 30 "
                       "sayfanın sırası aynı rng ile karıştırılır"},
    "sayfa": {"uzak_onceki": 120, "uzak_en_az": 40, "yakin_onceki": 10, "boy": [8.3, 14.5],
              "kutu": ["✓  çöl", "K  kısmen", "×  değil"],
              "tanim": "üst uzak görünüm: bölgeden önceki en çok 120 bar + bölge (turuncu kutu); alt yakın görünüm: önceki 10 bar + bölgenin tamamı; ikisinde sağda "
                       "yüzde ekseni (0 = bölgenin son kapanışı), Bollinger 20 + SMA20, MUM_IZI_HAKEM sınır / kırpma kuralı (HK_ESIK_OLCEK); hisse / tarih / "
                       "fiyat / kol / SONRASI yok (seri bölge sonunda kesilir: assert)"},
    "kapak": ("Bu sette 30 bölge var. Bir kısmını kod senin çöllerine benzetip seçti, bir kısmı rastgele, bir kısmı başka yolla. Hangisi olduğu yazmıyor. "
              "Soru tek: bu bölge senin çöl dediğin şey mi? Sonrası yok."),
    "kapak_ek": "Her sayfada bir kutuyu işaretle: ✓ çöl, K kısmen, × değil.",
    "sayim": {"tutuyor_pay": 0.70, "fark": 0.40,
              "tanim": "işaretlerden sonra ana model sayar: kol başına ✓ payı ve ✓ + K payı; RASTGELE kolun ✓ payı taban; 'KOD GÖZÜ TUTUYOR' <=> bir dedektörün ✓ "
                       "payı >= 0,70 VE RASTGELE ✓ payından en az 40 puan yüksek; KİTAPLIK sayfalarında ✓ sayısı (4'te kaç); sayılar küçük: 'ilk tur'"},
    "kesik": "havuz ve evren verisi en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi; assert); kitaplık serisi bölge bitişinde kesilir (assert)",
    "pazar_olcu": "RS_UZAK pazar endeksi ve OYN_SIRA kesiti: YO formülleri, küme = o gün geçerli barı olan pazarın BÜTÜN hisseleri (BIST'te P2 yok; ABD / AVR "
                  "de aynı kural, tutarlılık için); kitaplıkta endeks ve kesit, bütün BIST serileri bölge bitişinde kesilerek kurulur",
}

# ================================================================ ANA MODELİN EK KURALI (27 Kas 2026; ADIM A tablosu görüldükten SONRA, Cemal'in işaretlerinden
# ve onay setinden ÖNCE yazıldı). GT_ESIK'e girmez (onun sha'sı ADIM A ile mühürlü); ayrı sha ile dedektör json'una ve anahtara yazılır.
GT_EK_KURAL: Dict[str, Any] = {
    "surum": "GT-EK-1 (2026-11-27)",
    "sapma": "SAPMA: iş tanımındaki imza kuralı hiç ölçü seçmedi; ana modelin ek kuralı",
    "D2": {"ad": "YAKIN İMZA", "medyan_ust": 0.75, "medyan_alt": 0.25, "tutarlilik": 0.55, "karsi_en_cok": 1, "n_en_az": 12, "rho": 0.80,
           "tanim": "yakın imza ölçüsü <=> medyan sıra >= %75 ya da <= %25 VE tutarlılık >= %55 VE karşı uçta (yön YÜKSEK ise <= %30'da; DÜŞÜK ise >= %70'te) "
                    "en çok 1 bölge VE ölçüsü olan bölge >= 12; sonra |rho| > 0,80 çiftlerinden tutarlılığı düşük olan atılır (eşitlikte karşı uçta az bölgesi "
                    "olan kalır); kalan ölçülerin her birinde pencere kitaplığın tarafında ve kitaplık değerlerinin en gevşek %20'lik sınırının içinde "
                    "(iş tanımındaki D2 sınırı aynen); sıralama = bu ölçülerin kitaplık yönündeki evren yüzdelik sıralarının ortalaması"},
    "D3": {"ad": "EN YAKIN KOMŞU (sıra uzayı)", "tutarlilik": 0.50, "rho": 0.80, "ortak_en_az": 8, "haric": ["BOLGE_L", "PUAN_ESIT"], "col_basina": 20,
           "tanim": "tutarlılığı >= %50 olan ölçüler (BOLGE_L ve PUAN_ESIT hariç), |rho| > 0,80 budamasından sonra; her ölçü evren yüzdelik sırasına çevrilir; "
                    "uzaklık = ortak (boş olmayan) ölçülerde ortalama mutlak sıra farkı, en az 8 ortak ölçü; kitaplıktaki her çölün (aynı L* sınıfında, farklı "
                    "hisseden) en yakın komşusu; set için 6 sayfa = komşu uzaklığı en küçük 6 çölün komşuları (farklı çöllerden, farklı hisselerden)"},
    "uygulama": "D3 aday tablosu pazar başına her çölün en yakın 20 farklı hisseli komşusunu uzaklık sırasıyla tutar; onay seçimi kol_pazar'a göre (BIST 3, "
                "ABD 3) bu sıradan alır, bütün D3 kolunda her çöl ve her hisse en çok bir kez (bir çölün en yakın komşusunun hissesi zaten kullanılmışsa "
                "o çölün sıradaki komşusu); budama eşitliğinde (D3) medyanı 0,5'ten uzak olan kalır.",
}


def gt_ek_sha() -> str:
    return hashlib.sha256(json.dumps(GT_EK_KURAL, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


GT_YORUM = [
    "Kitaplık: COL_SKOR6.CS_KITAPLIK (20 bölge); tam BIST verisinde (/tmp/veri) sembolü olanlar ölçülür (COL_SKOR6 kitaplık.json ile aynı 16 bölge beklenir); "
    "veri yoksa sayısı yazılır, tutarlılık eşiği aynı oranla (%75) uygulanır.",
    "Bölge ölçüleri bölgenin kendi bar sayısıyla (COL_SKOR6'nın kitaplık kuralı); MUM_IZI_UC ölçüleri uzunluk parametreli (uc_olcu(m)) olduğu için bölgenin kendi "
    "uzunluğuyla; YUKSELIS_ONCESI ölçüleri bölge son barında (tanımları sabit geri bakışlı); karşılaştırma dağılımı bölgeye en yakın L* (20 / 40 / 80; eşitlikte "
    "küçük) sınıfının pencereleridir (COL_SKOR6 kuralı).",
    "MUM_IZI_UC ölçüleri bölgeden önce 120 bar ister (tanım AYNEN); daha kısa geçmişli bölgede (BINBN 50, KTLEV 63 bar) bu 12 ölçü boştur; MOM_12_1 / ZIRVE / DIP "
    "ölçüleri 250+ bar ister. Ölçüsü olmayan bölge o ölçünün tutarlılık paydasına girmez; imza için ölçüsü olan bölge >= %75 şartı aranır.",
    "RS_UZAK ve OYN_SIRA pazar düzeyi bilgi ister: YO'nun P2 havuzu yerine o gün geçerli barı olan bütün hisseler (BIST'te P2 yok; üç pazarda aynı kural).",
    "BANT_SON MUM_IZI_UC'deki tanımıyla (-|bc - 0,85|: banda yakınlık); ham konum bilgi olarak tutulmaz.",
    "DIP_DOKUNMA: dip = bölgenin en düşük L'si; ATR = bölge son barındaki ATR20 (YO ATRP20 x kapanış); C_i <= dip + 0,5 ATR olan bölge barlarının payı.",
    "DIP_YER: bölgenin en düşük L'sinin (ilk görülen) bar sırası / (n - 1); 'dip ilk üçte birde' <=> DIP_YER <= 1/3 (raporda sayılır).",
    "HACIM_ORAN = ort V(bölge) / ort V(bölgeden önceki en çok 200 bar; en az 20) (F6'nın kırpılmamış ham oranı); HACIM_SON5 = son 5 bar / bölge ortalaması.",
    "BOLGE_L evrende sabittir (= L*); sırası anlamsız olduğu için imzaya girmez, bilgi olarak yazılır.",
    "Spearman ilişkisi BIST evreninde her L için ayrı (en çok 200.000 pencere, sabit tohumlu alt örnek), üç L'nin en büyük |rho|'su kullanılır.",
    "Mum izi bilgi tablosu: mum_izi23_olay.csv günlük satırlar, sinif EVET (✓) / HAYIR (✗) (KISMEN dışarıda); ölçüler aynı fonksiyonlarla, sıralar kendi pazarının "
    "L = 20 evreninde (bölgeler 16-24 bar); AUC = P(✓ sırası > ✗ sırası) + 0,5 P(eşit). Getiri sütunları OKUNMAZ.",
    "D2 sınırı sıra uzayında: BIST'te ham değer sınırıyla aynı; ABD'de pazarın kendi evren sırası (ham değerler pazarlar arasında karşılaştırılamaz).",
    "D3'te kitaplık çölünün boş ölçüsü (kısa geçmiş) uzaklığa girmez (ortak sonlu boyutlar); komşu çölün L* sınıfından seçilir.",
    "Havuzdan ayrıca Cemal'e daha önce gösterilmiş mum izi bölgeleriyle örtüşen pencereler çıkarılır (körlük); kitaplık 2024-26, havuz <= 2022: örtüşme beklenmez, "
    "kural yine uygulanır ve sayılır.",
    "Sayfa: MUM_IZI_HAKEM geçmişli sayfanın grafik fonksiyonu (_hk_grafik_gecmis) ve sınır / yüzde ekseni kuralları içe alınır; sayfa fonksiyonu bu modülde "
    "(kutu yazıları '✓ çöl / K kısmen / × değil'; 'Senin kalıbın' mum izi şablonu ve mum boyu satırı bu sette YOK: kalıp Cemal'in kendi çölü, sayfada ölçü "
    "ipucu verilmez); yakın görünümde önceki 10 bar (iş tanımı).",
    "Kitaplık sayfaları tam BIST verisinden (2024-26) bölge bitişinde kesilerek çizilir; tarih / hisse yok.",
]


# ================================================================ 0) YARDIMCI
def _gt_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or GT_YOL["cikti"], GT_DOSYA[ad])


def _gt_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or GT_YOL["ham"], ad)


def gt_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or GT_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def gt_kod_sha() -> str:
    return MI._mi_sha(GT_YOL["kod"])


def gt_json_sha(J: Any) -> str:
    return hashlib.sha256(json.dumps(MI._mi_json(J), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _gt_git(args: List[str]) -> str:
    r = subprocess.run(["git", "-C", KOK_GT] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise GTHata(f"git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def gt_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str) -> pd.Timestamp:
    mx = max((d.index.max() for d in V.values() if len(d)), default=pd.Timestamp("1900-01-01"))
    if not mx <= GT_KESIK:
        raise GTHata(f"KESİK: {ad} en büyük tarih {mx.date()} > {GT_KESIK.date()}")
    return mx


def gt_yuzdelik(x: np.ndarray, dag: np.ndarray) -> np.ndarray:
    """(küçük + 0,5 eşit) / n (COL_SKOR6.cs_yuzdelik ile aynı; vektör). dag sıralı ve sonlu."""
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    if not len(dag):
        return out
    lo = np.searchsorted(dag, x, "left"); hi = np.searchsorted(dag, x, "right")
    ok = np.isfinite(x); out[ok] = (lo[ok] + 0.5 * (hi[ok] - lo[ok])) / len(dag)
    return out


def gt_Lyildiz(n: int) -> int:
    """Bölgeye en yakın L* (eşitlikte küçük; COL_SKOR6 kuralı)."""
    return int(min(GT_L, key=lambda L: (abs(int(n) - L), L)))


# ================================================================ 1) ÖLÇÜLER (yalnız s..t ve öncesi barlar)
def gt_on(d: pd.DataFrame, Lp: np.ndarray) -> Dict[str, Any]:
    """Bir hissenin pencereden bağımsız ön dizileri. d yalnız kullanılacak son bara kadar verilir (çağıran keser)."""
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    return {"O": O, "H": H, "L": L, "C": C, "V": V, "cV": np.r_[0.0, np.cumsum(V)], "CS": CS.cs_dizi(O, H, L, C, V), "UC": UC.uc_bar(O, H, L, C),
            "YO": YO.yo_hisse_ozellik(O, H, L, C, np.asarray(Lp, float)), "n": len(C)}


def gt_ek_olcu(P: Dict[str, Any], s: np.ndarray, t: np.ndarray) -> Dict[str, np.ndarray]:
    """Ek bölge içi 7 ölçü (GT_YORUM tanımları); pencereler [s_i, t_i], s >= 1; aynı uzunluklar gruplanır."""
    s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); N = len(s)
    out = {a: np.full(N, np.nan) for a in GT_EK_AD}
    ok = (s >= 1) & (t >= s) & (t < P["n"])
    H, L, C, V, cV, at = P["H"], P["L"], P["C"], P["V"], P["cV"], P["YO"]["ATRP20"]
    for m in np.unique((t - s + 1)[ok]):
        m = int(m); j = np.flatnonzero(ok & (t - s + 1 == m)); ss, tt = s[j], t[j]
        W = ss[:, None] + np.arange(m)[None, :]
        Lw = L[W]; Hw = H[W]; Cw = C[W]
        mnL = Lw.min(1); mxH = Hw.max(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            out["DIP_YER"][j] = np.argmin(Lw, 1) / (m - 1) if m > 1 else np.nan
            atr = at[tt] * C[tt]
            dd = (Cw <= (mnL + 0.5 * atr)[:, None]).mean(1); dd[~np.isfinite(atr)] = np.nan; out["DIP_DOKUNMA"][j] = dd
            out["SON_KONUM"][j] = np.where(mxH > mnL, (C[tt] - mnL) / (mxH - mnL), np.nan)
            out["BOLGE_L"][j] = float(m)
            out["YUK_KAPANIS"][j] = (Cw > C[W - 1]).mean(1)
            a0 = np.maximum(0, ss - 200); cnt = ss - a0
            vw = (cV[tt + 1] - cV[ss]) / m; vp = (cV[ss] - cV[a0]) / np.maximum(cnt, 1)
            out["HACIM_ORAN"][j] = np.where((cnt >= 20) & (vp > 0), vw / np.where(vp > 0, vp, 1.0), np.nan)
            if m >= 5:
                v5 = (cV[tt + 1] - cV[tt - 4]) / 5.0
                out["HACIM_SON5"][j] = np.where(vw > 0, v5 / np.where(vw > 0, vw, 1.0), np.nan)
    for a in out:
        out[a] = np.where(np.isfinite(out[a]), out[a], np.nan)
    return out


def gt_olcu(P: Dict[str, Any], s: Any, t: Any) -> Dict[str, np.ndarray]:
    """40 ölçü + PUAN_ESIT + govdesiz_pay + _oyn60 (OYN_SIRA kesiti çağıranda). Ölçü yalnız t_i'ye kadarki barlardan (test: t + 1 sonrası bozulunca aynı)."""
    s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); N = len(s)
    out: Dict[str, np.ndarray] = {a: np.full(N, np.nan) for a in GT_OLCU_AD + ["PUAN_ESIT", "govdesiz_pay", "_oyn60"]}
    if not N:
        return out
    if (t >= P["n"]).any() or (t < s).any():
        raise GTHata("gt_olcu: pencere seri dışında")
    o = CS.cs_olcu(P["CS"], s, t)
    for a in CS.CS_F + ["PUAN_ESIT"]:
        out[a] = np.asarray(o[a], float)
    m_ = t - s + 1; u = s - int(UC.UC_ESIK["pencere"]["onceki"]) >= 0
    for m in np.unique(m_[u]):
        j = np.flatnonzero(u & (m_ == m)); ou = UC.uc_olcu(P["UC"], t[j], int(m))
        for a in GT_UC_AD + ["govdesiz_pay"]:
            out[a][j] = ou[a]
    Y = P["YO"]
    for a in GT_YO_AD:
        if a != "OYN_SIRA":
            out[a] = np.asarray(Y[a], float)[t]
    out["_oyn60"] = np.asarray(Y["_oyn60"], float)[t]
    out.update(gt_ek_olcu(P, s, t))
    return out


# ================================================================ 2) PAZAR DÜZEYİ (endeks, oynaklık kesiti)
def gt_pazar(Vd: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Takvim, kapanış matrisi, pazar endeksi L (YO.yo_endeks; küme = o gün geçerli barı olan bütün hisseler)."""
    S = sorted(Vd); idx = pd.DatetimeIndex(sorted(set().union(*[Vd[s].index for s in S if len(Vd[s])])))
    Cl = np.full((len(idx), len(S)), np.nan); pos = {}
    for j, s in enumerate(S):
        d = Vd[s]; p = idx.get_indexer(d.index)
        if (p < 0).any():
            raise GTHata(f"takvim: {s} tarihi takvimde yok")
        Cl[p, j] = d.Close.to_numpy(float); pos[s] = p
    Lx, _ = YO.yo_endeks(Cl, np.isfinite(Cl))
    return {"idx": idx, "S": S, "pos": pos, "L": Lx}


def gt_oyn_sira(deger: np.ndarray, satir: np.ndarray, MAT: np.ndarray) -> np.ndarray:
    return YO.yo_kesit_sira(np.asarray(deger, float), np.asarray(satir, np.int64), MAT, np.isfinite(MAT))


# ================================================================ 3) KİTAPLIK (bölge bitişinde KESİLİR)
def gt_kitaplik_bolge(V: Dict[str, pd.DataFrame], G: Dict[str, pd.DatetimeIndex], sem: str, bas: str, bit: str) -> Dict[str, Any]:
    """Tek kitaplık bölgesi. Bütün BIST serileri bölge bitişinde kesilir (endeks + kesit + hissenin kendisi); 40 ölçü + PUAN_ESIT + kilitli payı."""
    bas_t = pd.Timestamp(bas); bit_t = pd.Timestamp(bit)
    d0 = V.get(sem)
    if d0 is None:
        return {"durum": "veri yok", "neden": "sembol tam BIST panelinde yok", "bar": 0}
    Vk = {s: d[d.index <= bit_t] for s, d in V.items()}
    Vk = {s: d for s, d in Vk.items() if len(d)}
    assert all(d.index.max() <= bit_t for d in Vk.values()), "kitaplık: bölge bitişinden sonraki bar okundu"
    x = Vk.get(sem)
    ix = np.flatnonzero((x.index >= bas_t) & (x.index <= bit_t)) if x is not None else np.array([], int)
    if len(ix) < 2:
        return {"durum": "veri yok", "neden": "bölge kapsanmıyor (geçerli bar < 2)", "bar": int(len(ix))}
    s, t = int(ix[0]), int(ix[-1])
    if s < int(GT_ESIK["evren"]["sol"]):
        return {"durum": "veri yok", "neden": f"bölgeden önce {s} bar (< 30)", "bar": int(t - s + 1)}
    assert t == len(x) - 1 and x.index[t] <= bit_t
    M = gt_pazar(Vk); p_sem = M["pos"][sem]
    P = gt_on(x, M["L"][p_sem]); o = gt_olcu(P, [s], [t])
    MAT = np.full((len(M["idx"]), len(M["S"])), np.nan)
    for j, ss in enumerate(M["S"]):
        dd = Vk[ss]; Y = YO.yo_hisse_ozellik(*(dd[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), M["L"][M["pos"][ss]])
        MAT[M["pos"][ss], j] = Y["_oyn60"]
    o["OYN_SIRA"] = gt_oyn_sira(o["_oyn60"], [p_sem[t]], MAT)
    g = G.get(sem); g = pd.DatetimeIndex(g)[pd.DatetimeIndex(g) <= bit_t] if g is not None else pd.DatetimeIndex([])
    kp = float(UC.uc_kilitli_pay(g, x.index, [x.index[s]], [x.index[t]])[0])
    n = t - s + 1
    r = {"durum": "tamam", "bar": int(n), "L": gt_Lyildiz(n), "ilk": str(x.index[s].date()), "son": str(x.index[t].date()), "kilitli_pay": kp,
         "s": s, "t": t, "onceki_bar": s}
    for a in GT_OLCU_AD + ["PUAN_ESIT", "govdesiz_pay"]:
        v = float(o[a][0]); r[a] = v if np.isfinite(v) else None
    return r


def gt_kitaplik(tam: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    tam = tam or MI.mi_veri("BIST", GT_YOL["tam_bist"])
    V = tam["V"]; G = tam.get("gecersiz", {}); sat = []
    for i, (sem, bas, bit) in enumerate(CS.CS_KITAPLIK):
        r = gt_kitaplik_bolge(V, G, sem, bas, bit)
        sat.append({"no": i + 1, "sembol": sem, "bas": bas, "bit": bit, **r})
        gtlog.info("kitaplık %d %s: %s", i + 1, sem, r["durum"])
    return sat


# ================================================================ 4) PENCERE PANELİ (BIST / ABD / AVR; <= 2022)
def gt_pencere_pazar(pazar: str, Vd: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Her hissede pencere sonu t (k % 5 == 0; tarih 2016-22), L = 20 / 40 / 80: 40 ölçü + PUAN_ESIT + kilitli + gövdesiz payı + OYN_SIRA."""
    t0 = time.time(); E = GT_ESIK["evren"]
    Vd = Vd or MI.mi_veri(pazar, GT_YOL["acik"])
    gt_kesik_kapi(Vd["V"], f"açık {pazar}")
    V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}; Gc = Vd.get("gecersiz", {})
    M = gt_pazar(V); MAT = np.full((len(M["idx"]), len(M["S"])), np.nan); parca = []
    b0, b1 = pd.Timestamp(E["bas"]), pd.Timestamp(E["son"])
    for j, sem in enumerate(M["S"]):
        d = V[sem]; p = M["pos"][sem]; P = gt_on(d, M["L"][p]); MAT[p, j] = P["YO"]["_oyn60"]
        tt = np.arange(0, len(d), int(E["adim"]), dtype=np.int64); dt = d.index[tt]; tt = tt[(dt >= b0) & (dt <= b1)]
        if not len(tt):
            continue
        gec = pd.DatetimeIndex(Gc.get(sem)) if Gc.get(sem) is not None else pd.DatetimeIndex([])
        for L in GT_L:
            s = tt - L + 1; k = s >= 1
            if not k.any():
                continue
            s1, t1 = s[k], tt[k]; o = gt_olcu(P, s1, t1)
            X = {a: np.asarray(o[a], np.float32) for a in GT_OLCU_AD + ["PUAN_ESIT", "govdesiz_pay", "_oyn60"]}
            X.update({"sembol": np.full(len(t1), sem, object), "j": np.full(len(t1), j, np.int32), "L": np.full(len(t1), L, np.int16),
                      "s": s1.astype(np.int32), "t": t1.astype(np.int32), "t_row": p[t1].astype(np.int32),
                      "KIL": UC.uc_kilitli_pay(gec, d.index, d.index[s1], d.index[t1]).astype(np.float32)})
            parca.append(pd.DataFrame(X))
    X = pd.concat(parca, ignore_index=True); del parca; gc.collect()
    X["OYN_SIRA"] = gt_oyn_sira(X["_oyn60"].to_numpy(float), X.t_row.to_numpy(), MAT).astype(np.float32)
    X["tarih"] = M["idx"][X.t_row.to_numpy()]
    X["bas_tarih"] = _gt_bas_tarih(X, V)
    X["pazar"] = pazar
    if not (X.tarih.max() <= GT_KESIK):
        raise GTHata(f"KESİK: {pazar} pencere tarihi > 2022-12-31")
    gtlog.info("%s: %d pencere (%d hisse, %.0f sn)", pazar, len(X), len(M["S"]), time.time() - t0)
    return X


def _gt_bas_tarih(X: pd.DataFrame, V: Dict[str, pd.DataFrame]) -> pd.DatetimeIndex:
    out = np.empty(len(X), "datetime64[ns]")
    for sem, ii in X.groupby("sembol").indices.items():
        out[ii] = V[sem].index.values[X.s.to_numpy()[ii]]
    return pd.DatetimeIndex(out)


def gt_evren_maske(X: pd.DataFrame) -> np.ndarray:
    """Karşılaştırma evreni (COL_SKOR6.cs_dag_maske ile aynı kural)."""
    E = GT_ESIK["evren"]
    return ((X.tarih >= pd.Timestamp(E["bas"])) & (X.tarih <= pd.Timestamp(E["son"]))).to_numpy(bool) & (X.s.to_numpy() >= int(E["sol"])) & \
        ~(X.KIL.to_numpy(float) > float(E["kilitli"])) & np.isfinite(X.PUAN_ESIT.to_numpy(float))


def gt_dagilim(X: pd.DataFrame) -> Dict[int, Dict[str, np.ndarray]]:
    m = gt_evren_maske(X); out = {}
    for L in GT_L:
        g = X[m & (X.L.to_numpy() == L)]
        out[L] = {}
        for a in GT_OLCU_AD + ["PUAN_ESIT"]:
            v = g[a].to_numpy(float); out[L][a] = np.sort(v[np.isfinite(v)])
    return out


def gt_sira_ekle(X: pd.DataFrame, dag: Dict[int, Dict[str, np.ndarray]], olcu: List[str]) -> pd.DataFrame:
    for a in olcu:
        r = np.full(len(X), np.nan)
        for L in GT_L:
            ii = np.flatnonzero(X.L.to_numpy() == L); r[ii] = gt_yuzdelik(X[a].to_numpy(float)[ii], dag[L][a])
        X[f"{a}_r"] = r.astype(np.float32)
    return X


# ================================================================ 5) MUM İZİ BÖLGELERİ (bilgi; getiri sütunları okunmaz)
GT_MI_SUTUN = ["set", "sayfa", "sinif", "zaman", "pazar", "sembol", "bolge_bas", "bolge_son", "m"]


def gt_mumizi_oku(yol: Optional[str] = None) -> pd.DataFrame:
    d = pd.read_csv(yol or GT_YOL["mumizi"], usecols=GT_MI_SUTUN)
    return d[(d.zaman == "gunluk") & d.sinif.isin(["EVET", "HAYIR"])].reset_index(drop=True)


def gt_mumizi_olcu(Vd: Dict[str, Any], pazar: str, R: pd.DataFrame) -> pd.DataFrame:
    V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}; M = gt_pazar(V)
    MAT = np.full((len(M["idx"]), len(M["S"])), np.nan); Pc: Dict[str, Any] = {}
    for j, sem in enumerate(M["S"]):
        d = V[sem]; Y = YO.yo_hisse_ozellik(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), M["L"][M["pos"][sem]])
        MAT[M["pos"][sem], j] = Y["_oyn60"]
    sat = []
    for r in R[R.pazar == pazar].itertuples():
        d = V.get(r.sembol)
        if d is None:
            sat.append({"sembol": r.sembol, "bolge_son": r.bolge_son, "sinif": r.sinif, "durum": "seri yok"}); continue
        b, e = pd.Timestamp(r.bolge_bas), pd.Timestamp(r.bolge_son)
        x = d[d.index <= e]; ix = np.flatnonzero((x.index >= b) & (x.index <= e))
        if len(ix) < 2:
            sat.append({"sembol": r.sembol, "bolge_son": r.bolge_son, "sinif": r.sinif, "durum": "bölge yok"}); continue
        s, t = int(ix[0]), int(ix[-1]); P = gt_on(x, M["L"][M["pos"][r.sembol][:len(x)]]); o = gt_olcu(P, [s], [t])
        o["OYN_SIRA"] = gt_oyn_sira(o["_oyn60"], [M["pos"][r.sembol][t]], MAT)
        sat.append({"sembol": r.sembol, "bolge_son": r.bolge_son, "sinif": r.sinif, "durum": "tamam", "pazar": pazar, "set": r.set, "bar": t - s + 1,
                    "m": int(r.m), **{a: float(o[a][0]) for a in GT_OLCU_AD + ["PUAN_ESIT"]}})
    return pd.DataFrame(sat)


# ================================================================ 6) OLCU KOMUTU
def gt_olcu_kos(ham: Optional[str] = None) -> Dict[str, Any]:
    ham = ham or GT_YOL["ham"]; os.makedirs(ham, exist_ok=True); out: Dict[str, Any] = {}
    KT = gt_kitaplik(); MI._mi_jyaz(_gt_ham("kitaplik_olcu.json", ham), KT, "kitaplık ölçü"); out["kitaplik"] = sum(r["durum"] == "tamam" for r in KT)
    R = gt_mumizi_oku(); MZ = []
    for p in GT_PAZAR:
        Vd = MI.mi_veri(p, GT_YOL["acik"])
        X = gt_pencere_pazar(p, Vd)
        with open(_gt_ham(f"pencere_{p}.pkl", ham), "wb") as f:
            pickle.dump(X, f, protocol=4)
        out[p] = int(len(X))
        if p == "BIST":
            out["K11_cs"] = gt_cs_sagla(X)
        MZ.append(gt_mumizi_olcu(Vd, p, R)); del X, Vd; gc.collect()
    Z = pd.concat(MZ, ignore_index=True); Z.to_csv(_gt_ham("mumizi_olcu.csv", ham), index=False); out["mumizi"] = int((Z.durum == "tamam").sum())
    out["sha"] = {a: MI._mi_sha(_gt_ham(a, ham)) for a in ["kitaplik_olcu.json", "mumizi_olcu.csv"] + [f"pencere_{p}.pkl" for p in GT_PAZAR]}
    MI._mi_jyaz(_gt_ham("olcu_ozet.json", ham), out, "ölçü özeti")
    return out


def gt_yukle(pazar: str, ham: Optional[str] = None) -> pd.DataFrame:
    with open(_gt_ham(f"pencere_{pazar}.pkl", ham), "rb") as f:
        return pickle.load(f)


def gt_cs_sagla(X: pd.DataFrame, ham: Optional[str] = None, n: int = 20000) -> Dict[str, Any]:
    """K11: BIST F1..F6 / PUAN_ESIT COL_SKOR6 pencere panelinden (pencere_BIST.pkl) bağımsız olarak birebir mi (aynı sembol, aynı t, aynı L)."""
    Y = CS.cs_yukle("BIST", CS.CS_YOL["ham"] if ham is None else ham)
    rng = np.random.default_rng(GT_ESIK["tohum"]); ii = rng.choice(len(X), min(n, len(X)), replace=False); en = 0.0; k = 0
    Yi = Y.set_index(["sembol", "t"])
    for L in GT_L:
        g = X.iloc[ii]; g = g[g.L.to_numpy() == L]
        key = list(zip(g.sembol, g.t.astype(int)))
        h = Yi.reindex(key)
        for a in CS.CS_F + ["PUAN_ESIT"]:
            u = g[a].to_numpy(float); v = h[f"{a}_{L}"].to_numpy(float); f = np.isfinite(u) & np.isfinite(v)
            k += int(f.sum()); en = max(en, float(np.max(np.abs(u[f] - v[f]))) if f.any() else 0.0)
            if (np.isfinite(u) != np.isfinite(v)).sum() > 0:
                raise GTHata(f"K11: {a} L{L} sonluluk COL_SKOR6 ile farklı")
    if en > 1e-4:
        raise GTHata(f"K11: F1..F6 COL_SKOR6 panelinden farklı (en büyük fark {en})")
    return {"karsilastirilan": k, "en_buyuk_fark": en}


# ================================================================ 7) ADIM A — PARMAK İZİ
def gt_tutarlilik(r: np.ndarray) -> Dict[str, Any]:
    E = GT_ESIK["imza"]; r = np.asarray([x for x in r if x is not None and np.isfinite(x)], float); n = len(r)
    if not n:
        return {"n": 0, "medyan": None, "ust": 0, "alt": 0, "yon": "-", "tut": None, "tut_k": 0}
    med = float(np.median(r)); ust = int((r >= E["taraf_ust"]).sum()); alt = int((r <= E["taraf_alt"]).sum())
    if med >= 0.5:
        yon, k = "YÜKSEK", ust
    else:
        yon, k = "DÜŞÜK", alt
    return {"n": n, "medyan": med, "ust": ust, "alt": alt, "yon": yon, "tut": k / n, "tut_k": k}


def gt_imza_aday(T: Dict[str, Any], n_bolge: int) -> bool:
    E = GT_ESIK["imza"]
    if T["n"] < math.ceil(E["n_oran"] * n_bolge) or T["tut"] is None:
        return False
    return T["tut"] >= E["tutarlilik"] and (T["medyan"] >= E["medyan_ust"] or T["medyan"] <= E["medyan_alt"])


def gt_spearman(X: pd.DataFrame, olcu: List[str]) -> Dict[str, Dict[str, float]]:
    """Evren (BIST) Spearman; her L ayrı, en büyük |rho|."""
    m = gt_evren_maske(X); R: Dict[str, Dict[str, float]] = {a: {b: 0.0 for b in olcu} for a in olcu}
    rng = np.random.default_rng(GT_ESIK["tohum"])
    for L in GT_L:
        g = X.loc[m & (X.L.to_numpy() == L), olcu]
        if len(g) > 200000:
            g = g.iloc[np.sort(rng.choice(len(g), 200000, replace=False))]
        C = g.rank().corr(method="pearson")
        for a in olcu:
            for b in olcu:
                v = C.loc[a, b]
                if np.isfinite(v) and abs(v) > abs(R[a][b]):
                    R[a][b] = float(v)
    return R


def gt_imza_sec(TT: Dict[str, Dict[str, Any]], n_bolge: int, R: Dict[str, Dict[str, float]]) -> Tuple[List[str], List[Dict[str, Any]]]:
    E = GT_ESIK["imza"]
    aday = [a for a in GT_OLCU_AD if a not in GT_IMZA_DISI and gt_imza_aday(TT[a], n_bolge)]
    aday.sort(key=lambda a: (-TT[a]["tut"], -abs(TT[a]["medyan"] - 0.5), GT_OLCU_AD.index(a)))
    kal: List[str] = []; atilan: List[Dict[str, Any]] = []
    for a in aday:
        cak = [b for b in kal if abs(R[a][b]) > E["rho"]]
        if cak:
            atilan.append({"olcu": a, "nedeni": cak[0], "rho": R[a][cak[0]]})
        else:
            kal.append(a)
    return kal, atilan


def _gt_budama(aday: List[str], R: Dict[str, Dict[str, float]], esik: float) -> Tuple[List[str], List[Dict[str, Any]]]:
    """aday önceden sıralı (önce kalacak olan önde); |rho| > esik olan sonraki ölçü atılır."""
    kal: List[str] = []; atilan: List[Dict[str, Any]] = []
    for a in aday:
        cak = [b for b in kal if abs(R[a][b]) > esik]
        if cak:
            atilan.append({"olcu": a, "nedeni": cak[0], "rho": R[a][cak[0]]})
        else:
            kal.append(a)
    return kal, atilan


def gt_karsi(T: Dict[str, Any]) -> int:
    """Kitaplık yönünün karşı ucundaki bölge sayısı (YÜKSEK -> <= 0,30; DÜŞÜK -> >= 0,70)."""
    return int(T["alt"] if T["yon"] == "YÜKSEK" else T["ust"])


def gt_yakin_imza(TT: Dict[str, Dict[str, Any]], R: Dict[str, Dict[str, float]]) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """EK KURAL D2 'YAKIN İMZA' ölçüleri (GT_EK_KURAL['D2'])."""
    E = GT_EK_KURAL["D2"]
    aday = [a for a in GT_OLCU_AD if a not in GT_IMZA_DISI and TT[a]["tut"] is not None and TT[a]["n"] >= E["n_en_az"]
            and (TT[a]["medyan"] >= E["medyan_ust"] or TT[a]["medyan"] <= E["medyan_alt"]) and TT[a]["tut"] >= E["tutarlilik"]
            and gt_karsi(TT[a]) <= E["karsi_en_cok"]]
    aday.sort(key=lambda a: (-TT[a]["tut"], gt_karsi(TT[a]), -abs(TT[a]["medyan"] - 0.5), GT_OLCU_AD.index(a)))
    kal, atilan = _gt_budama(aday, R, E["rho"])
    return kal, atilan, aday


def gt_d3_olcu_sec(TT: Dict[str, Dict[str, Any]], R: Dict[str, Dict[str, float]]) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """EK KURAL D3 ölçüleri: tutarlılık >= 0,50 (BOLGE_L / PUAN_ESIT hariç), |rho| > 0,80 budaması."""
    E = GT_EK_KURAL["D3"]
    aday = [a for a in GT_OLCU_AD if a not in E["haric"] and a not in GT_IMZA_DISI and TT[a]["tut"] is not None and TT[a]["tut"] >= E["tutarlilik"]]
    aday.sort(key=lambda a: (-TT[a]["tut"], -abs(TT[a]["medyan"] - 0.5), GT_OLCU_AD.index(a)))
    kal, atilan = _gt_budama(aday, R, E["rho"])
    return kal, atilan, aday


def gt_d3_uzak(Rp: np.ndarray, rk: np.ndarray, en_az: int) -> np.ndarray:
    """Ortak sonlu ölçülerde ortalama mutlak sıra farkı; ortak ölçü < en_az ise inf."""
    D = np.abs(Rp - rk[None, :]); f = np.isfinite(D); k = f.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        u = np.where(f, D, 0.0).sum(1) / np.maximum(k, 1)
    return np.where(k >= en_az, u, np.inf)


def gt_auc(x: np.ndarray, y: np.ndarray) -> Optional[float]:
    """AUC = P(x > y) + 0,5 P(x = y) (x: ✓, y: ✗)."""
    x = np.asarray(x, float); y = np.asarray(y, float); x = x[np.isfinite(x)]; y = y[np.isfinite(y)]
    if not len(x) or not len(y):
        return None
    g = (x[:, None] > y[None, :]).sum() + 0.5 * (x[:, None] == y[None, :]).sum()
    return float(g / (len(x) * len(y)))


def gt_parmak(ham: Optional[str] = None) -> Dict[str, Any]:
    KT = json.load(open(_gt_ham("kitaplik_olcu.json", ham), encoding="utf-8"))
    XB = gt_yukle("BIST", ham); dagB = gt_dagilim(XB)
    ok = [r for r in KT if r["durum"] == "tamam"]; nb = len(ok)
    for r in ok:
        r["sira"] = {a: (float(gt_yuzdelik([r[a]], dagB[r["L"]][a])[0]) if r.get(a) is not None else None) for a in GT_OLCU_AD + ["PUAN_ESIT"]}
    TT = {a: gt_tutarlilik([r["sira"][a] for r in ok]) for a in GT_OLCU_AD + ["PUAN_ESIT"]}
    R = gt_spearman(XB, [a for a in GT_OLCU_AD if a not in GT_IMZA_DISI])
    imza, atilan = gt_imza_sec(TT, nb, R)
    # mum izi bilgi tablosu (kendi pazarının L = 20 evreninde sıra)
    Z = pd.read_csv(_gt_ham("mumizi_olcu.csv", ham)); Z = Z[Z.durum == "tamam"].copy(); AUC: Dict[str, Any] = {}
    for p in GT_PAZAR:
        dag = dagB if p == "BIST" else gt_dagilim(gt_yukle(p, ham))
        ii = np.flatnonzero(Z.pazar.to_numpy() == p)
        for a in GT_OLCU_AD:
            L_ = np.array([gt_Lyildiz(b) for b in Z.bar.to_numpy()[ii]])
            v = np.full(len(ii), np.nan)
            for L in GT_L:
                k = L_ == L
                v[k] = gt_yuzdelik(Z[a].to_numpy(float)[ii][k], dag[L][a])
            Z.loc[Z.index[ii], f"{a}_r"] = v
        gc.collect()
    ev = Z.sinif.to_numpy() == "EVET"; hy = Z.sinif.to_numpy() == "HAYIR"
    for a in GT_OLCU_AD:
        AUC[a] = {"auc": gt_auc(Z[f"{a}_r"].to_numpy(float)[ev], Z[f"{a}_r"].to_numpy(float)[hy]),
                  "n_evet": int(np.isfinite(Z[f"{a}_r"].to_numpy(float)[ev]).sum()), "n_hayir": int(np.isfinite(Z[f"{a}_r"].to_numpy(float)[hy]).sum()),
                  "med_evet": _nmed(Z[f"{a}_r"].to_numpy(float)[ev]), "med_hayir": _nmed(Z[f"{a}_r"].to_numpy(float)[hy])}
    ayni = []
    for a in imza:
        au = AUC[a]["auc"]
        if au is None:
            ayni.append({"olcu": a, "ayni": None}); continue
        ayni.append({"olcu": a, "auc": au, "ayni": bool((au > 0.5) if TT[a]["yon"] == "YÜKSEK" else (au < 0.5))})
    # BİLGİ: imzaya en yakın ama geçemeyen 5 ölçü (gt_rapor ile aynı sıralama) mum izi ✓'lerinde de kitaplık yönünde mi
    yak5 = sorted([a for a in GT_OLCU_AD if a not in imza and a not in GT_IMZA_DISI and TT[a]["tut"] is not None],
                  key=lambda a: (-TT[a]["tut"], -abs(TT[a]["medyan"] - 0.5)))[:5]
    yakin_ayni = [{"olcu": a, "yon": TT[a]["yon"], "auc": AUC[a]["auc"],
                   "ayni": (None if AUC[a]["auc"] is None else bool((AUC[a]["auc"] > 0.5) if TT[a]["yon"] == "YÜKSEK" else (AUC[a]["auc"] < 0.5)))}
                  for a in yak5]
    J = {"surum": GT_SURUM, "kod_sha": gt_kod_sha(), "esik_sha": gt_esik_sha(), "bolge_n": nb, "bolge_toplam": len(KT),
         "veri_yok": [{"no": r["no"], "sembol": r["sembol"], "neden": r.get("neden")} for r in KT if r["durum"] != "tamam"],
         "dagilim_n": {str(L): int(len(dagB[L]["PUAN_ESIT"])) for L in GT_L},
         "bolge": [{k: r[k] for k in ("no", "sembol", "bas", "bit", "bar", "L", "onceki_bar", "kilitli_pay")} | {"sira": r["sira"]} for r in ok],
         "tutarlilik": TT, "imza": imza, "imza_yon": {a: TT[a]["yon"] for a in imza}, "imza_atilan_rho": atilan,
         "rho_imza": {a: {b: R[a][b] for b in imza} for a in imza}, "rho": R,
         "mumizi": {"n_evet": int(ev.sum()), "n_hayir": int(hy.sum()), "pazar": Z.groupby(["pazar", "sinif"]).size().to_dict(), "auc": AUC,
                    "imza_ayni_uc": ayni, "yakin_ayni_uc": yakin_ayni},
         "dip_ilk_ucte_bir": int(sum(1 for r in ok if r.get("DIP_YER") is not None and r["DIP_YER"] <= 1 / 3)),
         "dip_yer_n": int(sum(1 for r in ok if r.get("DIP_YER") is not None))}
    J["mumizi"]["pazar"] = {f"{k[0]}|{k[1]}": int(v) for k, v in J["mumizi"]["pazar"].items()}
    return J


def _nmed(v: np.ndarray) -> Optional[float]:
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    return float(np.median(v)) if len(v) else None


def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    return (f"%{100 * x:.0f}" if yuzde else f"{x:.{n}f}").replace(".", ",")


def _n(x: Any) -> str:
    return f"{int(x):,}".replace(",", ".")


_GT_ACIK = {a: d for a, _, d in GT_OLCU}


def gt_parmak_md(J: Dict[str, Any], ozet: Optional[str] = None) -> str:
    nb = J["bolge_n"]; TT = J["tutarlilik"]; imza = J["imza"]
    S = [f"# GT_PARMAK_IZI — Cemal'in çöl kitaplığının çok ölçülü parmak izi (ADIM A; yalnız tespit, getiri yok)", "",
         f"Kod: GOZ_TESPIT.py (sha {J['kod_sha'][:12]}); eşik sözlüğü sha {J['esik_sha'][:12]}. Kitaplık: COL_SKOR6.CS_KITAPLIK {J['bolge_toplam']} bölge; "
         f"verisi olan **{nb}** (veri yok: {', '.join(r['sembol'] for r in J['veri_yok'])}). Karşılaştırma evreni: BIST 2016-22 pencereleri (L* = 20 / 40 / 80; "
         f"n = {', '.join(f'L{k} {v:,}'.replace(',', '.') for k, v in J['dagilim_n'].items())}). Sıra = evrendeki yüzdelik ((küçük + 0,5 eşit) / n).", ""]
    S += ["## 1. ÖZET: Cemal'in çöllerinin ortak yanı", "", ozet or "(özet: ölçüm sonrası ana metin)", ""]
    S += ["## 2. İMZA ÖLÇÜLERİ", "",
          f"Kural (önceden): tutarlılık (medyan tarafında >= %70 / <= %30 kalan bölge payı) >= %75, medyan sıra >= %75 ya da <= %25, ölçüsü olan bölge >= "
          f"{math.ceil(0.75 * nb)} / {nb}; |rho| > 0,80 çiftlerden tutarlılığı düşük olan atılır.", "",
          "| imza ölçüsü | ne ölçer | yön | medyan sıra | tutarlılık |", "|---|---|---|---|---|"]
    for a in imza:
        T = TT[a]; S.append(f"| {a} | {_GT_ACIK[a]} | {T['yon']} | {_f(T['medyan'], yuzde=True)} | {T['tut_k']}/{T['n']} ({_f(T['tut'], yuzde=True)}) |")
    if not imza:
        S.append("| (yok) | | | | |")
    if J["imza_atilan_rho"]:
        S += ["", "İlişki yüzünden atılan imza adayları: " + "; ".join(f"{x['olcu']} ({x['nedeni']} ile rho {_f(x['rho'])})" for x in J["imza_atilan_rho"])]
    if imza:
        S += ["", "İmza ölçüleri arası evren Spearman (en büyük |rho|, üç L): " + "; ".join(
            f"{a}-{b} {_f(J['rho_imza'][a][b])}" for i, a in enumerate(imza) for b in imza[i + 1:])]
    S += ["", "## 3. Ölçü başına medyan sıra ve tutarlılık (40 ölçü + PUAN_ESIT bilgi)", "",
          "| ölçü | kaynak | ne ölçer | n | medyan sıra | >= %70 | <= %30 | yön | tutarlılık | imza |", "|---|---|---|---|---|---|---|---|---|---|"]
    kay = {a: k for a, k, _ in GT_OLCU}
    for a in GT_OLCU_AD + ["PUAN_ESIT"]:
        T = TT[a]
        im = "İMZA" if a in imza else ("rho ile atıldı" if any(x["olcu"] == a for x in J["imza_atilan_rho"]) else
                                       ("bilgi" if a in GT_IMZA_DISI or a == "PUAN_ESIT" else ""))
        S.append(f"| {a} | {kay.get(a, 'COL_SKOR6')} | {_GT_ACIK.get(a, 'altı ölçü eşit puan (D1)')} | {T['n']} | {_f(T['medyan'], yuzde=True)} | {T['ust']} | "
                 f"{T['alt']} | {T['yon']} | {_f(T['tut'], yuzde=True)} | {im} |")
    S += ["", f"Dibin yeri: {J['dip_ilk_ucte_bir']} / {J['dip_yer_n']} bölgede bölge dibi ilk üçte birde (DIP_YER <= 1/3).", "",
          "## 4. Bölge x ölçü yüzdelik sıra tablosu (%; '-' = ölçü yok: kısa geçmiş)", ""]
    B = J["bolge"]
    S.append("| ölçü | " + " | ".join(f"{r['no']} {r['sembol']}" for r in B) + " |")
    S.append("|---|" + "---|" * len(B))
    S.append("| bar / L* | " + " | ".join(f"{r['bar']}/{r['L']}" for r in B) + " |")
    for a in GT_OLCU_AD + ["PUAN_ESIT"]:
        S.append(f"| {a} | " + " | ".join(_f(r["sira"][a], yuzde=True) for r in B) + " |")
    M = J["mumizi"]
    S += ["", "## 5. BİLGİ: mum izi ✓ / ✗ (Cemal'in BENZİYOR / BENZEMİYOR dediği günlük bölgeler; mum_izi23_olay.csv)", "",
          f"✓ (EVET) {M['n_evet']}, ✗ (HAYIR) {M['n_hayir']} bölge ({', '.join(f'{k} {v}' for k, v in sorted(M['pazar'].items()))}); sıralar kendi pazarının L = 20 "
          "evreninde; AUC = P(✓ sırası > ✗ sırası). Küçük örneklem: bilgi, bulgu değil.", "",
          "| ölçü | AUC | ✓ medyan sıra | ✗ medyan sıra | n ✓ / ✗ | çöl imzası mı |", "|---|---|---|---|---|---|"]
    srt = sorted(GT_OLCU_AD, key=lambda a: -abs((M["auc"][a]["auc"] if M["auc"][a]["auc"] is not None else 0.5) - 0.5))
    for a in srt:
        u = M["auc"][a]
        S.append(f"| {a} | {_f(u['auc'])} | {_f(u['med_evet'], yuzde=True)} | {_f(u['med_hayir'], yuzde=True)} | {u['n_evet']} / {u['n_hayir']} | "
                 f"{('İMZA ' + TT[a]['yon']) if a in imza else ''} |")
    ay = [x for x in M["imza_ayni_uc"] if x["ayni"] is not None]
    S += ["", f"Çöl imza ölçüleri mum izi ✓'lerinde de aynı uçta mı (AUC kitaplık yönünde > 0,5): {sum(x['ayni'] for x in ay)} / {len(ay)} "
          f"({'; '.join(x['olcu'] + ' ' + ('evet' if x['ayni'] else 'hayır') + ' ' + _f(x['auc']) for x in ay)}).", ""]
    ya = [x for x in M.get("yakin_ayni_uc", []) if x["ayni"] is not None]
    if ya:
        S += [f"İmzaya en yakın ama geçemeyen 5 ölçü (bilgi) mum izi ✓'lerinde kitaplık yönünde mi: {sum(x['ayni'] for x in ya)} / {len(ya)} "
              f"({'; '.join(x['olcu'] + ' ' + x['yon'] + ' ' + ('evet' if x['ayni'] else 'hayır') + ' AUC ' + _f(x['auc']) for x in ya)}).", ""]
    S += ["## 6. Yorum noktaları", ""] + [f"- {y}" for y in GT_YORUM] + [""]
    return "\n".join(S)


# ================================================================ 8) ADIM B — DEDEKTÖRLER
def gt_kapi_commit(yol: str, ad: str) -> str:
    """yol commit edilmiş, çalışma kopyası HEAD ile aynı ve uzak dalda (push) olmalı."""
    rel = os.path.relpath(yol, KOK_GT)
    if not os.path.exists(yol):
        raise GTHata(f"kapı: {ad} yok ({rel})")
    c = _gt_git(["log", "-1", "--format=%H", "--", rel])
    if not c:
        raise GTHata(f"kapı: {ad} commit edilmemiş")
    if _gt_git(["status", "--porcelain", "--", rel]):
        raise GTHata(f"kapı: {ad} commit'ten sonra değişmiş")
    if not _gt_git(["branch", "-r", "--contains", c]):
        raise GTHata(f"kapı: {ad} commit'i ({c[:10]}) push edilmemiş")
    return c


def gt_yonlu(r: np.ndarray, yon: str) -> np.ndarray:
    r = np.asarray(r, float)
    return r if yon == "YÜKSEK" else 1.0 - r


def gt_d2_sinir(kit_r: List[Optional[float]], yon: str) -> Dict[str, Any]:
    """Kitaplık yönlü sıralarının 16'da 13 çölün sağladığı alt sınırı: sıralı (artan) dizide (n - ceil(0,8 n)). eleman; taraf şartıyla birleşik."""
    E = GT_ESIK["D2"]; q = np.sort(gt_yonlu(np.array([x for x in kit_r if x is not None and np.isfinite(x)], float), yon))
    n = len(q); k = int(math.ceil((1 - E["gevsek"]) * n)); b = float(q[n - k]) if n else float("nan")
    return {"n": n, "k": k, "sinir_kitaplik": b, "sinir": max(float(E["taraf"]), b)}


def gt_tekil(df: pd.DataFrame, skor: str, artan: bool = False) -> pd.DataFrame:
    """Aynı hissede pencere sonları arası < 40 bar olanlardan yalnız en iyi sıralı (açgözlü)."""
    w = int(GT_ESIK["tekil"]["bar"])
    if not len(df):
        return df
    g = df.sort_values([skor, "sembol", "t", "L"], ascending=[artan, True, True, True], kind="mergesort")
    tut = np.zeros(len(g), bool); son: Dict[str, List[int]] = {}
    for i, (sem, t) in enumerate(zip(g.sembol.to_numpy(), g.t.to_numpy())):
        k = son.setdefault(sem, [])
        if all(abs(int(t) - x) >= w for x in k):
            k.append(int(t)); tut[i] = True
    return g[tut]


def gt_ortusme(X: pd.DataFrame, bolgeler: pd.DataFrame) -> np.ndarray:
    """X penceresi (sembol, bas_tarih, tarih) aynı hissede bir bölgeyle (sembol, bas, son) takvimde örtüşüyor mu."""
    m = np.zeros(len(X), bool)
    if not len(bolgeler):
        return m
    gi = X.groupby("sembol").indices
    for r in bolgeler.itertuples():
        ii = gi.get(r.sembol)
        if ii is None:
            continue
        b, e = pd.Timestamp(r.bas), pd.Timestamp(r.son)
        m[ii] |= (X.bas_tarih.to_numpy()[ii] <= np.datetime64(e)) & (X.tarih.to_numpy()[ii] >= np.datetime64(b))
    return m


def gt_haric_bolgeler(pazar: str, KT: List[Dict[str, Any]]) -> pd.DataFrame:
    sat = []
    if pazar == "BIST":
        sat += [{"sembol": r["sembol"], "bas": r["bas"], "son": r["bit"], "kaynak": "kitaplik"} for r in KT]
    d = pd.read_csv(GT_YOL["mumizi"], usecols=["pazar", "sembol", "bolge_bas", "bolge_son"])
    d = d[d.pazar == pazar]
    sat += [{"sembol": s, "bas": b, "son": e, "kaynak": "mumizi"} for s, b, e in zip(d.sembol, d.bolge_bas, d.bolge_son)]
    return pd.DataFrame(sat, columns=["sembol", "bas", "son", "kaynak"])


def gt_havuz_maske(X: pd.DataFrame, imza: List[str], haric: pd.DataFrame) -> Tuple[np.ndarray, Dict[str, int]]:
    H = GT_ESIK["havuz"]; say: Dict[str, int] = {"pencere": int(len(X))}
    m = gt_evren_maske(X); say["evren"] = int(m.sum())
    m &= X.s.to_numpy() >= int(H["on_bar"]); say["on_bar_120"] = int(m.sum())
    m &= ~(X.govdesiz_pay.to_numpy(float) > float(H["govdesiz"])); say["govdesiz_ok"] = int(m.sum())
    for a in imza:
        m &= np.isfinite(X[a].to_numpy(float))
    say["imza_sonlu"] = int(m.sum())
    for k in ("kitaplik", "mumizi"):
        o = gt_ortusme(X, haric[haric.kaynak == k]); say[f"{k}_ortusen"] = int((m & o).sum()); m &= ~o
    say["havuz"] = int(m.sum()); say["havuz_hisse"] = int(X.sembol[m].nunique())
    return m, say


def gt_d3_z(r: np.ndarray) -> np.ndarray:
    from scipy.stats import norm
    return norm.ppf(np.clip(np.asarray(r, float), 0.001, 0.999))


def gt_dedektor_hesap(J: Dict[str, Any], ham: Optional[str] = None) -> Dict[str, Any]:
    """D1 (iş tanımı) + D2 'YAKIN İMZA' ve D3 'EN YAKIN KOMŞU (sıra uzayı)' (GT_EK_KURAL; iş tanımının imza kuralı ölçü seçmediğinde ana modelin ek kuralı)."""
    TT = J["tutarlilik"]; R = J["rho"]; B = J["bolge"]
    imza = list(J["imza"])
    if imza:
        d2o = imza; d2_atilan: List[Dict[str, Any]] = []; d2_aday = imza; d2_kaynak = "iş tanımı imza"
    else:
        d2o, d2_atilan, d2_aday = gt_yakin_imza(TT, R); d2_kaynak = "EK KURAL yakın imza"
    d3o, d3_atilan, d3_aday = gt_d3_olcu_sec(TT, R)
    yon = {a: TT[a]["yon"] for a in set(d2o) | set(d3o)}
    KT = json.load(open(_gt_ham("kitaplik_olcu.json", ham), encoding="utf-8"))
    sin = {a: gt_d2_sinir([r["sira"][a] for r in B], yon[a]) for a in d2o}
    E3 = GT_EK_KURAL["D3"]
    kit = []
    for r in B:
        q = {a: (float(gt_yonlu([r["sira"][a]], yon[a])[0]) if r["sira"][a] is not None else None) for a in d2o}
        gec = all(q[a] is not None and q[a] >= sin[a]["sinir"] for a in d2o) if d2o else False
        kit.append({"no": r["no"], "sembol": r["sembol"], "L": r["L"], "D1": (r["sira"]["PUAN_ESIT"] or 0) >= GT_ESIK["D1"]["ust"], "D2": gec,
                    "D2_sagladigi": sum(1 for a in d2o if q[a] is not None and q[a] >= sin[a]["sinir"]),
                    "r3": [(r["sira"][a] if r["sira"][a] is not None else np.nan) for a in d3o]})
    out: Dict[str, Any] = {"imza": imza, "d2_olcu": d2o, "d2_kaynak": d2_kaynak, "d2_aday": d2_aday, "d2_atilan_rho": d2_atilan,
                           "d3_olcu": d3o, "d3_aday": d3_aday, "d3_atilan_rho": d3_atilan, "imza_yon": yon, "d2_sinir": sin, "kitaplik": kit,
                           "ek_kural_sha": gt_ek_sha(), "pazar": {}, "aday": {}}
    for p in GT_HAVUZ_PAZAR:
        X = gt_yukle(p, ham); dag = gt_dagilim(X); X = gt_sira_ekle(X, dag, sorted(set(d2o) | set(d3o)) + ["PUAN_ESIT"])
        hm, say = gt_havuz_maske(X, d2o, gt_haric_bolgeler(p, KT))
        g = X[hm].copy(); del X; gc.collect()
        # D1
        d1 = g[g.PUAN_ESIT_r.to_numpy(float) >= GT_ESIK["D1"]["ust"]].copy(); d1["skor"] = d1.PUAN_ESIT_r.astype(float) + 1e-9 * d1.PUAN_ESIT.astype(float) / 100
        d1t = gt_tekil(d1, "skor")
        # D2
        Q = np.stack([gt_yonlu(g[f"{a}_r"].to_numpy(float), yon[a]) for a in d2o], 1) if d2o else np.zeros((len(g), 0))
        kos = np.stack([Q[:, i] >= sin[a]["sinir"] for i, a in enumerate(d2o)], 1) if d2o else np.zeros((len(g), 0), bool)
        k_say = kos.sum(1)
        d2m = kos.all(1) if d2o else np.zeros(len(g), bool)
        d2 = g[d2m].copy(); d2["skor"] = Q[d2m].mean(1) if d2o else np.zeros(0); d2t = gt_tekil(d2, "skor")
        # D3 (sıra uzayı, ortalama mutlak fark)
        Rp = np.stack([g[f"{a}_r"].to_numpy(float) for a in d3o], 1) if d3o else np.zeros((len(g), 0)); d3s = []; d3_en = {}
        Lg = g.L.to_numpy(); Sg = g.sembol.to_numpy()
        for kr in kit:
            rk = np.asarray(kr["r3"], float)
            if np.isfinite(rk).sum() < E3["ortak_en_az"]:
                d3_en[str(kr["no"])] = None; continue
            ii = np.flatnonzero((Lg == kr["L"]) & (Sg != kr["sembol"]))
            dist = gt_d3_uzak(Rp[ii], rk, int(E3["ortak_en_az"]))
            k = min(len(ii), 5000); o = np.argpartition(dist, k - 1)[:k] if k < len(ii) else np.arange(len(ii))
            o = o[np.lexsort((o, dist[o]))]; gor: set = set()
            for q_ in o:
                if not np.isfinite(dist[q_]) or len(gor) >= int(E3["col_basina"]):
                    break
                sem = Sg[ii[q_]]
                if sem in gor:
                    continue
                gor.add(sem); rr = g.iloc[ii[q_]].copy(); rr["skor"] = float(dist[q_]); rr["kitaplik_no"] = kr["no"]; rr["komsu_sira"] = len(gor); d3s.append(rr)
            d3_en[str(kr["no"])] = next((float(x["skor"]) for x in d3s if x["kitaplik_no"] == kr["no"]), None)
        d3 = pd.DataFrame(d3s)
        out["pazar"][p] = {"say": say, "D1_ham": int(len(d1)), "D1": int(len(d1t)), "D2_ham": int(d2m.sum()), "D2": int(len(d2t)),
                           "D3": int(sum(v is not None for v in d3_en.values())), "D3_en_yakin": d3_en,
                           "D1_pay": len(d1) / max(len(g), 1), "D2_pay": int(d2m.sum()) / max(len(g), 1),
                           "D2_kosul_pay": {a: float(kos[:, i].mean()) for i, a in enumerate(d2o)},
                           "D2_kac_kosul": {str(k): int((k_say == k).sum()) for k in range(len(d2o) + 1)},
                           "havuz_L": {str(L): int((g.L.to_numpy() == L).sum()) for L in GT_L},
                           "D2_L": {str(L): int((d2t.L.to_numpy() == L).sum()) for L in GT_L} if len(d2t) else {},
                           "D1_L": {str(L): int((d1t.L.to_numpy() == L).sum()) for L in GT_L}}
        kol = ["sembol", "t", "s", "L", "tarih", "bas_tarih", "PUAN_ESIT", "PUAN_ESIT_r", "skor"]
        kol2 = kol + [f"{a}_r" for a in d2o]; kol3 = kol + [f"{a}_r" for a in d3o] + ["kitaplik_no", "komsu_sira"]
        out["aday"][p] = {"D1": d1t[kol].head(200), "D2": d2t[kol2].head(200),
                          "D3": d3[kol3].sort_values(["skor", "kitaplik_no"], kind="mergesort").reset_index(drop=True) if len(d3) else pd.DataFrame(columns=kol3),
                          "havuz": g[["sembol", "t", "s", "L", "tarih", "bas_tarih", "PUAN_ESIT", "PUAN_ESIT_r"]].reset_index(drop=True)}
        del g; gc.collect()
    for k in kit:
        k.pop("r3", None)
    return out


def gt_dedektor_md(J: Dict[str, Any], D: Dict[str, Any], c_parmak: str, ksha: str) -> str:
    imza = D["d2_olcu"]; yon = D["imza_yon"]; E = GT_ESIK; EK = GT_EK_KURAL
    S = ["# GT_DEDEKTOR — üç dedektör (ADIM B; ADIM A'dan sonra, Cemal'in işaretlerinden ve onay setinden ÖNCE sabitlendi)", "",
         f"Parmak izi commit'i: {c_parmak[:10]}; GOZ_TESPIT.py sha {gt_kod_sha()[:12]}; eşik sözlüğü sha {gt_esik_sha()[:12]}; dedektör json sha {ksha[:12]}. "
         "Getiri / sonrası hesaplanmadı.", "",
         "## 1. Tanımlar (kesin)", "",
         f"- HAVUZ: {E['havuz']['tanim']}. Evren: {E['evren']['tanim']}.",
         f"- D1 ESKİ PUAN: {E['D1']['tanim']}.",
         f"- İŞ TANIMINDAKİ D2 İMZA: {E['D2']['tanim']}. İş tanımı imza ölçüleri ({len(D['imza'])}): " + (", ".join(D["imza"]) or "YOK") + ".",
         f"- İŞ TANIMINDAKİ D3: {E['D3']['tanim']}." + ("" if D["imza"] else " İmza uzayı boş olduğu için tanımsız."), "",
         f"## 1a. {EK['sapma']}", "",
         "Ana modelin ek kuralı ADIM A tablosu görüldükten SONRA, Cemal'in işaretlerinden ve onay setinden ÖNCE yazıldı; imza kuralının sonucu değişmedi "
         f"(imza = {'yok' if not D['imza'] else ', '.join(D['imza'])}). Ek kural sha {D['ek_kural_sha'][:12]} ({EK['surum']}).", "",
         f"- D2 {EK['D2']['ad']} (D2'nin yerine): {EK['D2']['tanim']}.",
         f"- D3 {EK['D3']['ad']} (imza uzayının yerine): {EK['D3']['tanim']}.",
         f"- Uygulama ayrıntısı: {EK['uygulama']}", "",
         f"D2 ölçü adayları (budama öncesi): {', '.join(D['d2_aday']) or 'yok'}; budamada atılan: " +
         ("; ".join(f"{x['olcu']} ({x['nedeni']} ile rho {_f(x['rho'])})" for x in D["d2_atilan_rho"]) or "yok") +
         f"; KALAN D2 ölçüleri ({len(imza)}): " + (", ".join(f"{a} ({yon[a]})" for a in imza) or "YOK") + ".", "",
         f"D3 ölçü adayları (tutarlılık >= %50): {', '.join(D['d3_aday']) or 'yok'}; budamada atılan: " +
         ("; ".join(f"{x['olcu']} ({x['nedeni']} ile rho {_f(x['rho'])})" for x in D["d3_atilan_rho"]) or "yok") +
         f"; KALAN D3 ölçüleri ({len(D['d3_olcu'])}): {', '.join(D['d3_olcu']) or 'YOK'}.", "",
         f"- TEKİLLEŞTİRME: {E['tekil']['tanim']}.", "",
         "## 2. D2 kesim değerleri (yönlü sıra uzayında; kitaplıktan)", "",
         "| imza ölçüsü | yön | ölçüsü olan çöl | 13/16 kuralı (k) | kitaplık sınırı | uygulanan sınır (maks 0,50) |", "|---|---|---|---|---|---|"]
    for a in imza:
        s = D["d2_sinir"][a]
        S.append(f"| {a} | {yon[a]} | {s['n']} | {s['k']} | {_f(s['sinir_kitaplik'], 3)} | {_f(s['sinir'], 3)} |")
    S += ["", "Yönlü sıra: YÜKSEK yönlüde evren sırası, DÜŞÜK yönlüde 1 - sıra. Ham değer karşılığı BIST'te aynı yüzdelikteki değerdir.", "",
          "## 3. Havuz ve seçilen pencere sayıları", "", "| | BIST | ABD |", "|---|---|---|"]
    P = D["pazar"]
    for k, ad in (("pencere", "bütün pencereler (L x pencere sonu)"), ("evren", "evren (ön şart, kilitli değil)"), ("on_bar_120", "+ önceki >= 120 bar"),
                  ("govdesiz_ok", "+ gövdesiz bar payı <= %30"), ("imza_sonlu", "+ PUAN ve imza ölçüleri sonlu"), ("kitaplik_ortusen", "- kitaplıkla örtüşen"),
                  ("mumizi_ortusen", "- mum izi bölgeleriyle örtüşen"), ("havuz", "HAVUZ (pencere)"), ("havuz_hisse", "havuz hisse sayısı")):
        S.append(f"| {ad} | {P['BIST']['say'][k]:,} | {P['ABD']['say'][k]:,} |".replace(",", "."))
    for k, ad in (("D1", "D1 seçilen (ham / tekil)"), ("D2", "D2 seçilen (ham / tekil)")):
        S.append(f"| {ad} | {P['BIST'][k + '_ham']:,} / {P['BIST'][k]:,} | {P['ABD'][k + '_ham']:,} / {P['ABD'][k]:,} |".replace(",", "."))
    for k in ("D1", "D2"):
        S.append(f"| {k} havuzun yüzde kaçı (ham) | {_f(100 * P['BIST'][k + '_pay'], 2)} | {_f(100 * P['ABD'][k + '_pay'], 2)} |")
    S.append(f"| D3 komşusu bulunan çöl (en az 8 ortak ölçü) | {P['BIST']['D3']} | {P['ABD']['D3']} |")
    S += ["", "D3: çöl başına en yakın komşu uzaklığı (ortalama mutlak sıra farkı; küçük = yakın):", "", "| çöl | BIST | ABD |", "|---|---|---|"]
    for k in D["kitaplik"]:
        S.append(f"| {k['no']} {k['sembol']} | {_f(P['BIST']['D3_en_yakin'].get(str(k['no'])), 3)} | {_f(P['ABD']['D3_en_yakin'].get(str(k['no'])), 3)} |")
    S += ["", "## 4. D2 imza koşullarının havuzda sağlanma payı", "", "| koşul | BIST | ABD |", "|---|---|---|"]
    for a in imza:
        S.append(f"| {a} ({yon[a]}) | {_f(100 * P['BIST']['D2_kosul_pay'][a], 1)} % | {_f(100 * P['ABD']['D2_kosul_pay'][a], 1)} % |")
    S += ["", "Kaç koşulu birden sağlayan pencere (havuz):", "", "| sağlanan koşul | BIST | ABD |", "|---|---|---|"]
    for k in range(len(imza) + 1):
        S.append(f"| {k} / {len(imza)} | {P['BIST']['D2_kac_kosul'][str(k)]:,} | {P['ABD']['D2_kac_kosul'][str(k)]:,} |".replace(",", "."))
    kit = D["kitaplik"]
    S += ["", "## 5. Kitaplığın kendisi (örneklem içi yakalama; bölgeler kuralı kurdu, bu bir sağlama, bulgu değil)", "",
          f"- D1 (PUAN_ESIT sırası >= 0,90): {sum(k['D1'] for k in kit)} / {len(kit)} çöl.",
          f"- D2 (bütün imza koşulları): {sum(k['D2'] for k in kit)} / {len(kit)} çöl; koşul başına sağlayan çöl: " +
          ", ".join(f"{a} {sum(1 for r in J['bolge'] if r['sira'][a] is not None and gt_yonlu([r['sira'][a]], yon[a])[0] >= D['d2_sinir'][a]['sinir'])}"
                    for a in imza) + ".",
          "- Çöl başına sağlanan D2 koşulu: " + ", ".join(f"{k['no']} {k['sembol']} {k['D2_sagladigi']}/{len(imza)}" for k in kit) + ".", "",
          "## 6. Yorum gerektiren noktalar (ana modele)", ""]
    S += [f"- {y}" for y in GT_YORUM[11:]]
    if not D["imza"]:
        S += [f"- {EK['sapma']} (bkz. 1a). D2 / D3 ek kuralla kuruldu; kitaplığın D2'yi geçmesi örneklem içidir (kural kitaplıktan kuruldu)."]
    S += ["- D1'de sınır 'en yüksek puanlılar' için pazar ve L içinde üst %10 seçildi (Ç262 dilimi); sayfalar sıralamanın en üstünden alınır.",
          "- D2 'kitaplığın tarafı' = yönlü sıra >= 0,50; 'gevşek %20 sınırı' = kitaplık yönlü sıralarının 16'da 13'ünün sağladığı en büyük alt sınır; ikisinin büyüğü.",
          "- Dedektör sayfaları sıralamanın en üstünden: kod en çok benzettiğini gösterir; bütün seçilen kümeyi temsil etmez (rapor bunu yazar).",
          "- Onay setinde her hisse bir kez; kol ve pazar sayıları sabit (GT_ESIK['kol_pazar']); D2 bir pazarda yetmezse öteki pazardan tamamlanır, yine eksikse eksik kalır.", ""]
    S += ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; ölçüm yok: getiri hesaplanmaz)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    for k, (y, kn) in GT_KONTROL.items():
        S.append(f"| {k} | {GT_KONTROL_AD[k]} | {y} | {kn} |")
    S.append("")
    return "\n".join(S)


GT_KONTROL_AD = {"K1": "kontrol grubu", "K2": "geleceğe bakma", "K3": "geçerli bar", "K4": "tekilleştirme", "K5": "giriş fiyatı", "K6": "veri birimi",
                 "K7": "hayatta kalma", "K8": "örneklem ve dönem", "K9": "ön kayıt", "K10": "ayrıştırma", "K11": "yeniden üretim", "K12": "ifade",
                 "K13": "süreç", "K14": "boyut (gerçek para)"}
GT_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban oran = RASTGELE kol (aynı havuz, aynı L dağılımı, aynı sayfa çizimi); kitaplık 4 sayfa Cemal'in tekrar tutarlılığı; getiri karşılaştırması yok"),
    "K2": ("EVET", "ölçüler yalnız s..t ve öncesi (test: t + 1 sonrası bozulunca aynı); kitaplıkta bütün BIST serileri bölge bitişinde kesilir (assert); havuz <= 2022-12-31 (assert)"),
    "K3": ("EVET", "MI.mi_veri geçerli bar; kilitli pay > 0,20 ve gövdesiz (O = C) bar payı > 0,30 pencere havuzdan atılır"),
    "K4": ("EVET", "her dedektörde aynı hissede < 40 bar pencere sonlarından tek pencere; onay setinde her hisse bir kez"),
    "K5": ("UYGULANMAZ", "giriş / getiri yok: yalnız tespit (sayfada bölge sonrası çizilmez)"),
    "K6": ("EVET", "ölçüler oransal / sıra; ABD ve BIST kendi evren sırasıyla; açık kopya bölünme düzeltmeli"),
    "K7": ("EVET", "evren bugün yaşayan hisseler; tespit sorusunda etkisi küçük, raporda yazılı"),
    "K8": ("EVET", "kitaplık 16 bölge: 'tespit' (bulgu değil); onay kol başına 6-8 sayfa: 'ilk tur', en iyi kol 24 sayfayla yinelenir"),
    "K9": ("EVET", "GT_ESIK sha + kod sha bu dosyada; GT_PARMAK_IZI.md commit + push dedektörden önce, GT_DEDEKTOR.md commit + push onay setinden önce (gt_kapi_commit)"),
    "K10": ("EVET", "F1..F6 COL_SKOR6 pencere paneliyle birebir (gt_cs_sagla); kitaplık PUAN sırası COL_SKOR6 kitaplik.json ile karşılaştırıldı; ek ölçüler elle örnekli test"),
    "K11": ("EVET", "rapordan önce >= 2 hücre (kitaplık sırası, D2 kesimi) ham dosyalardan bağımsız kısa kodla yeniden üretilir (GT_RAPOR)"),
    "K12": ("EVET", "'imza' yalnız önceden yazılı kuralla; kitaplık yakalaması örneklem içi diye yazılır; 'kod gözü tutuyor' yalnız işaret sayımından sonra"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_gt); yasak dosyalara dokunulmaz; yalnız kendi yolları commit; MI._mi_yaz sızıntı taraması; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil"),
}


# ================================================================ 9) ADIM C — ONAY SETİ
def gt_sayfa(fig, d: pd.DataFrame, s: int, t: int, sayfa: int, kutu: Optional[List[str]] = None) -> Dict[str, Any]:
    """Geçmişli onay sayfası: üst uzak (önceki <= 120 bar + bölge), alt yakın (önceki 10 bar + bölge), üç kutu. Yalnız d[:t + 1] (assert); sonrası yok."""
    from matplotlib.patches import Rectangle
    G = dict(HK.HK_ESIK_OLCEK); P = GT_ESIK["sayfa"]; s = int(s); t = int(t)
    # Çok derin düşüşlü pencerede (önceki fiyat son kapanışın onlarca katı) HK adım listesi (en çok %500) 8 çizgiyi aşar: yalnız bu sayfa için büyük adımlar eklenir.
    G["adim"] = list(G["adim"]) + [1000, 2000, 2500, 5000, 10000, 20000, 50000, 100000]
    if not (0 <= s <= t < len(d)):
        raise GTHata(f"sayfa: geçersiz bölge (s={s}, t={t}, n={len(d)})")
    dg = d.iloc[:t + 1]
    O_, H_, L_, C_ = (dg[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    assert len(C_) == t + 1, "geleceğe bakma kapısı: bölge sonundan sonraki bar sayfaya girdi"
    BU, BO, BA = MI.mi_bant(C_); ref = float(C_[t])
    nu = min(int(P["uzak_onceki"]), s)
    if nu < int(P["uzak_en_az"]):
        raise GTHata(f"sayfa: bölgeden önce {nu} bar (< {P['uzak_en_az']})")
    iu = s - nu; slu = slice(iu, t + 1); ku = (s - iu, t - iu)
    iy = max(0, s - int(P["yakin_onceki"])); sly = slice(iy, t + 1); ky = (s - iy, t - iy)
    assert slu.stop == sly.stop == t + 1 == len(C_), "geleceğe bakma kapısı: pencere bölge sonunu aşıyor"
    fig.text(0.05, 0.968, "Üst: bölgenin gerisi (önceki 120 mum) + bölge.   Alt: yakından bölge (önceki 10 mum + bölge).\n"
             "Turuncu kutu = bölge; sağ kenar = bölgenin sonu (sonrası gösterilmiyor).\nMor = Bollinger 20 ve SMA20 (kesik).   "
             "Sağdaki eksen: bölgenin son kapanışına göre yüzde (0 = son kapanış).\n▲ / ▼ = çerçeveden taşan fitil kesildi (mor işaret: bant kesildi).",
             fontsize=9.6, va="top", linespacing=1.45)
    axu = fig.add_axes([0.04, 0.565, 0.83, 0.30])
    ou = HK._hk_grafik_gecmis(axu, O_[slu], H_[slu], L_[slu], C_[slu], BU[slu], BO[slu], BA[slu], ku, ref, G, True, f"Sayfa {sayfa}: bölgenin gerisi ve bölge (günlük mum)")
    axy = fig.add_axes([0.04, 0.185, 0.83, 0.315])
    oy = HK._hk_grafik_gecmis(axy, O_[sly], H_[sly], L_[sly], C_[sly], BU[sly], BO[sly], BA[sly], ky, ref, G, False, "Yakından: bölge")
    axk = fig.add_axes([0.04, 0.02, 0.92, 0.11]); axk.axis("off")
    for xx, txt in zip((0.0, 0.345, 0.69), P["kutu"]):
        axk.add_patch(Rectangle((xx, 0.05), 0.31, 0.9, fill=False, linewidth=3, transform=axk.transAxes))
        axk.text(xx + 0.155, 0.5, txt, ha="center", va="center", fontsize=21, transform=axk.transAxes)
    if kutu:                                                            # isteğe bağlı kutu yazıları (ör. dört kutu: ✓ / K / E erken / ×); verilmezse üstteki üç kutu aynen
        for p_ in list(axk.patches): p_.remove()
        for t_ in list(axk.texts): t_.remove()
        nk = len(kutu); bosluk = 0.035; gen = (1.0 - (nk - 1) * bosluk) / nk
        for i_, txt in enumerate(kutu):
            xx = i_ * (gen + bosluk)
            axk.add_patch(Rectangle((xx, 0.05), gen, 0.9, fill=False, linewidth=3, transform=axk.transAxes))
            axk.text(xx + gen / 2, 0.5, txt, ha="center", va="center", fontsize=21 if nk <= 3 else 16.5, transform=axk.transAxes)
    return {"uzak_onceki_bar": int(nu), "yakin_onceki_bar": int(s - iy), "uzak": ou, "yakin": oy, "son_bar_index": int(t), "seri_uzunluk_kullanilan": int(len(dg))}


def gt_pdf(yol: str, sayfalar: List[Dict[str, Any]], seri: Any, kapak: Optional[str] = None, kutu: Optional[List[str]] = None) -> Dict[str, Any]:
    """sayfalar: [{'sayfa', 'pazar', 'sembol', 's', 't', 'kaynak'}]; seri(pazar, sembol, kaynak) -> DataFrame. Belirlenimci (metadata tarihsiz)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    boy = tuple(float(x) for x in GT_ESIK["sayfa"]["boy"]); olc = []
    kapak = kapak or (GT_ESIK["kapak"] + "\n\n" + GT_ESIK["kapak_ek"])
    try:
        with PdfPages(yol, metadata={"Title": "GT onay", "Author": None, "Creator": None, "Producer": None, "CreationDate": None, "ModDate": None}) as pdf:
            fig = plt.figure(figsize=boy); fig.text(0.06, 0.955, "ÇÖL ONAY SETİ", fontsize=17, weight="bold")
            fig.text(0.06, 0.915, kapak, fontsize=13.5, va="top", wrap=True, linespacing=1.5)
            pdf.savefig(fig); plt.close(fig)
            for r in sorted(sayfalar, key=lambda r: r["sayfa"]):
                d = seri(r["pazar"], r["sembol"], r["kaynak"])
                fig = plt.figure(figsize=boy); o = gt_sayfa(fig, d, r["s"], r["t"], r["sayfa"], kutu=kutu); pdf.savefig(fig); plt.close(fig)
                olc.append(dict(o, sayfa=r["sayfa"]))
    except Exception:
        if os.path.exists(yol):
            os.remove(yol)
        raise
    return {"sha": MI._mi_sha(yol), "olc": olc}


def gt_onay_sec(A: Dict[str, Dict[str, pd.DataFrame]], kit: List[Dict[str, Any]], tohum: Optional[int] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """A[pazar][kol] sıralı aday tabloları (D1 / D2 / D3 / havuz); kit = verisi olan kitaplık bölgeleri (s, t, sembol, no). Sayfa listesi + sayım."""
    rng = np.random.default_rng(GT_ESIK["tohum"] if tohum is None else tohum); KP = GT_ESIK["kol_pazar"]
    kul: set = set(); kul_kit: set = set(); sec: List[Dict[str, Any]] = []; eksik: Dict[str, int] = {}; tasinan: Dict[str, int] = {}
    uygun_kit = [k for k in kit if k["s"] >= int(GT_ESIK["sayfa"]["uzak_en_az"])]
    for i in sorted(rng.choice(len(uygun_kit), KP["KITAPLIK"]["BIST"], replace=False).tolist()):
        k = uygun_kit[i]; kul.add(("BIST", k["sembol"]))
        sec.append({"kol": "KITAPLIK", "pazar": "BIST", "sembol": k["sembol"], "s": int(k["s"]), "t": int(k["t"]), "L": int(k["bar"]), "kaynak": "tam",
                    "kitaplik_no": int(k["no"]), "bas": k["ilk"], "son": k["son"]})

    def al(p: str, kol: str, n: int) -> int:
        T = A[p][kol]; kc = 0
        for r in T.itertuples():
            if kc >= n:
                break
            if (p, r.sembol) in kul:
                continue
            kno = getattr(r, "kitaplik_no", None) if kol == "D3" else None
            if kno is not None and pd.notna(kno):
                if int(kno) in kul_kit:                                   # EK KURAL D3: her çöl en çok bir kez
                    continue
                kul_kit.add(int(kno))
            kul.add((p, r.sembol)); kc += 1
            e = {"kol": kol, "pazar": p, "sembol": r.sembol, "s": int(r.s), "t": int(r.t), "L": int(r.L), "kaynak": "acik", "bas": str(pd.Timestamp(r.bas_tarih).date()),
                 "son": str(pd.Timestamp(r.tarih).date()), "PUAN_ESIT": float(r.PUAN_ESIT), "PUAN_ESIT_r": float(r.PUAN_ESIT_r), "skor": float(r.skor)}
            if hasattr(r, "kitaplik_no") and pd.notna(getattr(r, "kitaplik_no")):
                e["kitaplik_no"] = int(r.kitaplik_no)
            sec.append(e)
        return kc

    for kol in ("D1", "D2", "D3"):
        for p in GT_HAVUZ_PAZAR:
            n = KP[kol][p]; k = al(p, kol, n)
            if k < n:
                eksik[f"{kol}|{p}"] = n - k
        if kol == "D2":
            for p in GT_HAVUZ_PAZAR:
                q = [x for x in GT_HAVUZ_PAZAR if x != p][0]; ek = eksik.get(f"D2|{p}", 0)
                if ek:
                    k = al(q, "D2", ek); tasinan[f"D2|{p}->{q}"] = k; eksik[f"D2|{p}"] = ek - k
    for p in GT_HAVUZ_PAZAR:
        Ls = [x["L"] for x in sec if x["pazar"] == p and x["kol"] in ("D1", "D2", "D3")] or list(GT_L)
        n = KP["RASTGELE"][p]; Lc = rng.choice(np.asarray(Ls), n, replace=len(Ls) < n).tolist()
        H = A[p]["havuz"]
        for L in Lc:
            ii = np.flatnonzero((H.L.to_numpy() == L) & ~np.isin(H.sembol.to_numpy(), [s for (pp, s) in kul if pp == p]))
            if not len(ii):
                eksik[f"RASTGELE|{p}"] = eksik.get(f"RASTGELE|{p}", 0) + 1; continue
            r = H.iloc[int(rng.choice(ii))]; kul.add((p, r.sembol))
            sec.append({"kol": "RASTGELE", "pazar": p, "sembol": r.sembol, "s": int(r.s), "t": int(r.t), "L": int(r.L), "kaynak": "acik",
                        "bas": str(pd.Timestamp(r.bas_tarih).date()), "son": str(pd.Timestamp(r.tarih).date()), "PUAN_ESIT": float(r.PUAN_ESIT),
                        "PUAN_ESIT_r": float(r.PUAN_ESIT_r)})
    sira = rng.permutation(len(sec))
    for k, i in enumerate(sira):
        sec[int(i)]["sayfa"] = k + 1
    sec.sort(key=lambda r: r["sayfa"])
    say = {"kol": {k: sum(r["kol"] == k for r in sec) for k in GT_ESIK["kol"]}, "pazar": {p: sum(r["pazar"] == p for r in sec) for p in GT_HAVUZ_PAZAR},
           "eksik": {k: v for k, v in eksik.items() if v}, "tasinan": tasinan, "toplam": len(sec)}
    return sec, say


def gt_pdf_metin(yol: str) -> str:
    r = subprocess.run(["pdftotext", "-layout", yol, "-"], capture_output=True, text=True)
    if r.returncode != 0:
        raise GTHata(f"pdftotext: {r.stderr[:200]}")
    return r.stdout


GT_YASAK_METIN = ["D1", "D2", "D3", "RASTGELE", "KİTAPLIK", "KITAPLIK", "rastgele kol", "imza", "puan"]


def gt_pdf_denetim(yol: str, semboller: List[str]) -> Dict[str, Any]:
    """PDF metninde kol / hisse / tarih yok (DUR)."""
    m = gt_pdf_metin(yol); ust = m.upper(); bul = []
    for sem in set(semboller):
        if re.search(r"(?<![A-Z0-9])" + re.escape(sem.upper()) + r"(?![A-Z0-9])", ust):
            bul.append(f"hisse:{sem}")
    for y in GT_YASAK_METIN:
        if re.search(r"(?<![A-Za-zİı0-9])" + re.escape(y) + r"(?![A-Za-zİı0-9])", m):
            bul.append(f"kol:{y}")
    if re.search(r"\b(19|20)\d{2}[-./]\d{1,2}", m) or re.search(r"\b\d{1,2}[./]\d{1,2}[./](19|20)\d{2}\b", m):
        bul.append("tarih")
    if bul:
        raise GTHata(f"PDF metninde yasak bilgi: {bul[:10]}")
    return {"karakter": len(m), "temiz": True}


def gt_onay(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    import IZ_KARNE as IK  # yalnız okuma (kontrol kapısı)
    cikti = cikti or GT_YOL["cikti"]
    y = _gt_yol("pdf", cikti); ya = _gt_yol("anahtar", cikti)
    if os.path.exists(y) or os.path.exists(ya):
        raise GTHata("onay: GT_ONAY.pdf / anahtar zaten var (ikinci koşu durur)")
    c_ded = gt_kapi_commit(_gt_yol("dedektor_md", cikti), "GT_DEDEKTOR.md"); c_par = gt_kapi_commit(_gt_yol("parmak_md", cikti), "GT_PARMAK_IZI.md")
    IK.ik_kontrol_kapisi(_gt_yol("dedektor_md", cikti))
    DJ = json.load(open(_gt_yol("dedektor", cikti), encoding="utf-8"))
    if DJ.get("esik_sha") != gt_esik_sha():
        raise GTHata("onay: eşik sözlüğü dedektör json'undaki sha ile aynı değil")
    with open(_gt_ham("dedektor_aday.pkl", ham), "rb") as f:
        A = pickle.load(f)
    if MI._mi_sha(_gt_ham("dedektor_aday.pkl", ham)) != DJ["aday_sha"]:
        raise GTHata("onay: aday dosyası dedektör json'undaki sha ile aynı değil")
    KT = json.load(open(_gt_ham("kitaplik_olcu.json", ham), encoding="utf-8")); kit = [r for r in KT if r["durum"] == "tamam"]
    sec, say = gt_onay_sec(A, kit)
    Vc: Dict[Any, Any] = {}
    sira: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for x in sorted(sec, key=lambda q: q["sayfa"]):
        sira.setdefault((x["pazar"], x["sembol"]), []).append(x)

    def seri(p: str, sem: str, kaynak: str) -> pd.DataFrame:
        if (p, kaynak) not in Vc:
            Vc[(p, kaynak)] = MI.mi_veri(p, GT_YOL["tam_bist"] if kaynak == "tam" else GT_YOL["acik"])["V"]
            if kaynak == "acik":
                gt_kesik_kapi(Vc[(p, kaynak)], f"onay {p}")
        d = Vc[(p, kaynak)][sem]
        # gt_pdf sayfaları sayfa sırasıyla ve her sayfa için bir kez çağırır: aynı hissenin iki bölgesi (kitaplıkta TEHOL) sırayla eşlenir;
        # yanlış eşleşme aşağıdaki tarih kapısında durur.
        r = sira[(p, sem)].pop(0)
        if r["kaynak"] != kaynak:
            raise GTHata(f"onay: sayfa kaynağı uyuşmuyor ({p} sayfa {r['sayfa']})")
        if kaynak == "tam":
            d = d[d.index <= pd.Timestamp(next(k["bit"] for k in kit if k["no"] == r["kitaplik_no"]))]
        if str(d.index[r["t"]].date()) != r["son"] or str(d.index[r["s"]].date()) != r["bas"]:
            raise GTHata(f"onay: bölge tarihleri seriyle uyuşmuyor ({p} sayfa {r['sayfa']})")
        return d

    kapak = GT_ESIK["kapak"].replace("Bu sette 30 bölge var.", f"Bu sette {len(sec)} bölge var.") + "\n\n" + GT_ESIK["kapak_ek"]
    P = gt_pdf(y, sec, seri, kapak=kapak)
    gt_pdf_denetim(y, [r["sembol"] for r in sec])
    K = {"not": "MÜHÜRLÜ: sayfa -> kol / pazar / sembol / bölge tarihleri / puanlar; PDF'e girmez; işaretler gelmeden açılmaz", "surum": GT_SURUM,
         "kod_sha": gt_kod_sha(), "esik_sha": gt_esik_sha(), "tohum": GT_ESIK["tohum"], "ek_kural_sha": gt_ek_sha(), "parmak_commit": c_par, "dedektor_commit": c_ded,
         "dedektor_json_sha": MI._mi_sha(_gt_yol("dedektor", cikti)), "pdf": os.path.basename(y), "pdf_sha": P["sha"], "say": say,
         "sayfalar": [dict(r, uzak_onceki_bar=o["uzak_onceki_bar"]) for r, o in zip(sec, P["olc"])]}
    MI._mi_jyaz(ya, K, "onay anahtar")
    return {"pdf": y, "pdf_sha": P["sha"], "anahtar": ya, "anahtar_sha": MI._mi_sha(ya), "say": say, "sayfa_sayisi": len(sec) + 1,
            "olc": [{"sayfa": o["sayfa"], "uzak_onceki_bar": o["uzak_onceki_bar"], "son_bar_index": o["son_bar_index"],
                     "seri_uzunluk_kullanilan": o["seri_uzunluk_kullanilan"]} for o in P["olc"]]}

def gt_rapor(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """GT_RAPOR.md + gt_sonuc.json (parmak / dedektör json'ları ve anahtarın YALNIZ toplamlarından; kol-sayfa / hisse-sayfa eşlemesi yazılmaz)."""
    cikti = cikti or GT_YOL["cikti"]
    J = json.load(open(_gt_yol("parmak", cikti), encoding="utf-8")); D = json.load(open(_gt_yol("dedektor", cikti), encoding="utf-8"))
    K = json.load(open(_gt_yol("anahtar", cikti), encoding="utf-8"))
    if MI._mi_sha(_gt_yol("pdf", cikti)) != K["pdf_sha"]:
        raise GTHata("rapor: GT_ONAY.pdf anahtardaki sha ile aynı değil")
    ek_y = _gt_ham("rapor_ek.json", ham); EK = json.load(open(ek_y, encoding="utf-8")) if os.path.exists(ek_y) else {}
    TT = J["tutarlilik"]; imza = J["imza"]; P = D["pazar"]; kit = D["kitaplik"]
    yak = sorted([a for a in GT_OLCU_AD if a not in imza and a not in GT_IMZA_DISI and TT[a]["tut"] is not None],
                 key=lambda a: (-TT[a]["tut"], -abs(TT[a]["medyan"] - 0.5)))[:5]
    auc = sorted([(a, v["auc"]) for a, v in J["mumizi"]["auc"].items() if v["auc"] is not None], key=lambda x: -abs(x[1] - 0.5))[:5]
    ay = [x for x in J["mumizi"]["imza_ayni_uc"] if x["ayni"] is not None]
    R = {"surum": GT_SURUM, "kod_sha": gt_kod_sha(), "esik_sha": gt_esik_sha(), "parmak_commit": K["parmak_commit"], "dedektor_commit": K["dedektor_commit"],
         "pdf_sha": K["pdf_sha"], "anahtar_sha": MI._mi_sha(_gt_yol("anahtar", cikti)), "sayfa": K["say"]["toplam"], "kol": K["say"]["kol"],
         "pazar": K["say"]["pazar"], "eksik": K["say"]["eksik"], "tasinan": K["say"]["tasinan"],
         "parmak": {"olcu_n": len(GT_OLCU_AD), "bolge_n": J["bolge_n"], "imza": [{"olcu": a, "yon": TT[a]["yon"], "medyan": TT[a]["medyan"],
                                                                                  "tut_k": TT[a]["tut_k"], "n": TT[a]["n"]} for a in imza],
                    "yakin": [{"olcu": a, "yon": TT[a]["yon"], "medyan": TT[a]["medyan"], "tut_k": TT[a]["tut_k"], "n": TT[a]["n"]} for a in yak],
                    "ilginc": {a: {"medyan": TT[a]["medyan"], "tut_k": TT[a]["tut_k"], "n": TT[a]["n"]} for a in
                               ("F1", "BOY_YUZDE_ORAN", "BOY_MUTLAK", "UST_FITIL", "SON_UST_FITIL", "F6", "HACIM_ORAN", "HACIM_SON5") if a in TT}},
         "mumizi": {"auc_ilk5": auc, "imza_ayni": sum(x["ayni"] for x in ay), "imza_n": len(ay)},
         "dedektor": {p: {k: P[p][k] for k in ("D1_ham", "D1", "D1_pay", "D2_ham", "D2", "D2_pay", "D3")} | {"havuz": P[p]["say"]["havuz"]} for p in P},
         "kitaplik_D1": sum(k["D1"] for k in kit), "kitaplik_D2": sum(k["D2"] for k in kit), "kitaplik_n": len(kit), "d2_kosul": len(D.get("d2_olcu", D["imza"])), "d2_olcu": D.get("d2_olcu", D["imza"]),
         "d3_olcu": D.get("d3_olcu", []), "ek_kural_sha": D.get("ek_kural_sha"),
         "sayim_kurali": GT_ESIK["sayim"]["tanim"], "hata": EK.get("hata", []), "sapma": EK.get("sapma", []), "yeniden": EK.get("yeniden", [])}
    S = ["# GT_RAPOR — GOZ_TESPIT: parmak izi, dedektörler, kör onay seti (yalnız tespit; getiri / sonrası yok)", "",
         f"Kod sha {R['kod_sha'][:12]}, eşik sha {R['esik_sha'][:12]}; parmak izi commit {R['parmak_commit'][:10]} -> dedektör commit {R['dedektor_commit'][:10]} -> "
         f"onay seti (PDF sha {R['pdf_sha'][:12]}, anahtar sha {R['anahtar_sha'][:12]}).", "",
         "## SONUÇ", "",
         f"- PARMAK İZİ: {len(GT_OLCU_AD)} ölçü, {J['bolge_n']} kitaplık bölgesi. İMZA ölçüleri ({len(imza)}): " +
         ("; ".join(f"{x['olcu']} {x['yon']} (medyan sıra {_f(x['medyan'], yuzde=True)}, {x['tut_k']}/{x['n']})" for x in R["parmak"]["imza"]) or "YOK") + ".",
         "- İmzaya en yakın ama geçemeyen: " + "; ".join(f"{x['olcu']} {x['yon']} ({_f(x['medyan'], yuzde=True)}, {x['tut_k']}/{x['n']})" for x in R["parmak"]["yakin"]) + ".",
         "- Ayırmayan / zayıf ilginç ölçüler: " + "; ".join(f"{a} medyan {_f(v['medyan'], yuzde=True)} ({v['tut_k']}/{v['n']})" for a, v in R["parmak"]["ilginc"].items()) + ".",
         f"- Mum izi ✓ / ✗ (bilgi): en yüksek |AUC - 0,5| beş ölçü: " + "; ".join(f"{a} {_f(u)}" for a, u in auc) +
         f". Çöl imzaları mum izi ✓'lerinde aynı uçta: {R['mumizi']['imza_ayni']} / {R['mumizi']['imza_n']}.",
         f"- DEDEKTÖRLER (havuz BIST {_n(P['BIST']['say']['havuz'])} / ABD {_n(P['ABD']['say']['havuz'])} pencere): " + "; ".join(
             f"{k} BIST {_n(P['BIST'][k + '_ham'])} (%{_f(100 * P['BIST'][k + '_pay'], 2)}; tekil {_n(P['BIST'][k])}), ABD {_n(P['ABD'][k + '_ham'])} "
             f"(%{_f(100 * P['ABD'][k + '_pay'], 2)}; tekil {_n(P['ABD'][k])})" for k in ("D1", "D2")) +
         f"; D3 (komşusu bulunan çöl) BIST {P['BIST']['D3']}, ABD {P['ABD']['D3']}. D2'nin {R['d2_kosul']} koşulu var ({', '.join(R['d2_olcu']) or 'yok'}"
         f"{'; iş tanımı imzası yok, EK KURAL yakın imza' if not imza else ''}); D3 ölçüleri ({len(R['d3_olcu'])}): {', '.join(R['d3_olcu'])}.",
         f"- Kitaplığın kendi yakalaması (örneklem içi): D1 üst %10'unda {R['kitaplik_D1']} / {len(kit)}; D2'yi geçen {R['kitaplik_D2']} / {len(kit)}.",
         f"- ONAY SETİ: {R['sayfa']} bölge sayfası + kapak; kol sayıları {R['kol']}; pazar {R['pazar']}; eksik {R['eksik'] or 'yok'}; taşınan {R['tasinan'] or 'yok'}. "
         "Kol / hisse / tarih PDF'te yok (pdftotext denetimi); eşleme yalnız mühürlü anahtarda.",
         f"- Sayım kuralı (işaretlerden sonra, önceden): {GT_ESIK['sayim']['tanim']}.", "",
         "Okuma: dedektör sayfaları her dedektörün sıralamasının en üstünden alındı (kodun en çok benzettiği); seçilen kümenin tamamını temsil etmez. Kol başına 6-8 "
         "sayfa: sonuç 'ilk tur'; tutarsa en iyi kol 24 sayfayla yinelenir. Kitaplık imzası kitaplığın kendisinden kuruldu: D2'nin kitaplığı yakalaması örneklem içidir.", "",
         "## KONTROL LİSTESİ", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    S += [f"| {k} | {GT_KONTROL_AD[k]} | {y} | {kn} |" for k, (y, kn) in GT_KONTROL.items()]
    S += ["", "## YENİDEN ÜRETİM (K11)", ""] + ([f"- {x}" for x in R["yeniden"]] or ["- (yok)"])
    S += ["", "## HATA", ""] + ([f"- HATA: {x}" for x in R["hata"]] or ["- (bulunan hata yok)"])
    S += ["", "## SAPMA", ""] + ([f"- {x}" for x in R["sapma"]] or ["- (iş tanımından sapma yok)"])
    S += ["", "## ÖNERİLEN DEFTER SATIRLARI (ana model işler)", ""] + [f"- {x}" for x in EK.get("defter", [])] + [""]
    MI._mi_jyaz(_gt_yol("sonuc", cikti), R, "gt sonuç")
    MI._mi_yaz(_gt_yol("rapor", cikti), "\n".join(S), "gt rapor")
    return R


# ================================================================ 10) KOMUTLAR
def gt_parmak_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or GT_YOL["cikti"]
    J = gt_parmak(ham)
    oz = _gt_ham("ozet_A.txt", ham); ozet = open(oz, encoding="utf-8").read().strip() if os.path.exists(oz) else None
    MI._mi_jyaz(_gt_yol("parmak", cikti), J, "parmak izi json")
    MI._mi_yaz(_gt_yol("parmak_md", cikti), gt_parmak_md(J, ozet), "parmak izi md")
    return J


def gt_dedektor_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or GT_YOL["cikti"]
    c_par = gt_kapi_commit(_gt_yol("parmak_md", cikti), "GT_PARMAK_IZI.md")
    J = json.load(open(_gt_yol("parmak", cikti), encoding="utf-8"))
    if J.get("esik_sha") != gt_esik_sha():
        raise GTHata("dedektör: eşik sözlüğü parmak izi json'undaki sha ile aynı değil")
    D = gt_dedektor_hesap(J, ham)
    with open(_gt_ham("dedektor_aday.pkl", ham), "wb") as f:
        pickle.dump(D["aday"], f, protocol=4)
    DJ = {k: v for k, v in D.items() if k != "aday"}
    DJ.update({"surum": GT_SURUM, "kod_sha": gt_kod_sha(), "esik_sha": gt_esik_sha(), "parmak_commit": c_par,
               "aday_sha": MI._mi_sha(_gt_ham("dedektor_aday.pkl", ham))})
    for k in DJ["kitaplik"]:
        k.pop("z", None)
    MI._mi_jyaz(_gt_yol("dedektor", cikti), DJ, "dedektör json")
    MI._mi_yaz(_gt_yol("dedektor_md", cikti), gt_dedektor_md(J, D, c_par, MI._mi_sha(_gt_yol("dedektor", cikti))), "dedektör md")
    return DJ


# ================================================================ 11) ÇÖL-K2 (EK 5, 27 Kas 2026; iş tanımı GT5_IS_TANIMI.md)
# Beş şart ana modelin denetim araçlarından (goz2/cetvel.py goz_olcu, goz2/parabol.py dip_parabol / dip_parabol_var, goz2/k2.py k2) AYNEN alındı; eşikler
# goz2/k2.py K2 sözlüğü + goz2/dip_parabol_kural.json (seçilen basamak r2 0,60; yükseliş 0,25). Hiçbir şart bölge sonundan (t) sonraki barı okumaz.
# Sonuçlar 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)' diye okunur.
GT_K2: Dict[str, Any] = {
    "Y": {"KUTU_ORAN": 0.22, "KUTU_YER": 0.35, "TEPE_KAT": 2.0},
    "M": {"BOY_ORAN": 0.80, "GOV_ORAN": 0.80},
    "S": {"taban_pay": 0.25, "ayri_bar": 3, "dokunus": 3, "yayilim": 0.25},
    "B": {"dipten_bar": 5, "once": 20},
    "Z": {"bolum_pay": 3, "bolum_en_az": 10, "tepe_x": [-1.0, 0.5], "son_bar": 3, "yuksek_dip": 0.05, "r2": 0.60, "yukselis": 0.25},
    "uzak": 120, "uzak_en_az": 40,
    "tanim": {"Y": "YER: kutu yüksekliği / uzak görünüm (önceki 120 bar + bölge) yüksekliği <= 0,22 VE kutu ortası uzak görünümün alt %35'inde VE önceki 120 barın "
                   "tepesi / kutu tavanı >= 2",
              "M": "KÜÇÜK MUM: bölge medyan mum boyu (H - L) / önceki 120 bar medyanı <= 0,80 VE medyan gövde |C - O| oranı <= 0,80",
              "S": "DİP SAVUNMASI: dibi kutunun alt %25'ine dokunan barlar; aralarında >= 3 bar olanlar ayrı dokunuş; >= 3 ayrı dokunuş VE ilk-son dokunuş arası >= "
                   "bölge uzunluğunun %25'i",
              "B": "DERİN DİP BİTTİ: bölge + önceki 20 barın en derin dibi bölge sonundan en az 5 bar geride",
              "Z": "DİP PARABOLÜ: bölgenin son üçte biri (en az 10 bar) mum DİPLERİNE ikinci derece eğri: kavis > 0, sonda eğim > 0, eğrinin dibi x in [-1; 0,5], "
                   "son 3 barın dibi bölümün en derin dibinin üstünde, son üçte birin dibi bölüm aralığının >= %5 üstünde, r2 >= 0,60, yükseliş >= 0,25"},
    "kaynak": "goz2/k2.py K2 + goz2/dip_parabol_kural.json (AYNEN; test_goz_tespit: sözlük ve sayılar goz2 ile birebir)",
}
GT_K2_OLAY: Dict[str, Any] = {
    "bas": "2016-01-01", "son": "2022-12-31", "s_min": 120, "kilitli": 0.20, "govdesiz": 0.30, "tekil": 40, "kollar": ["K2", "YMSB", "Y"],
    "pazar": ["ABD", "AVR", "BIST"],
    "tanim": "evren = GOZ_TESPIT pencere paneli (L = 20 / 40 / 80; t % 5 == 0), pencere sonu tarihi 2016-01-01 .. 2022-12-31, s >= 120, kilitli pay <= 0,20, "
             "gövdesiz bar payı <= 0,30; kollar: K2 = beş şart, YMSB = parabolsüz dört şart (Y, M, S, B), Y = yalnız yer; tekilleştirme kol ve hisse başına: "
             "pencereler (t, L) artan sırada; bir pencere, aynı kolda tutulan son pencerenin sonundan >= 40 bar sonra bitiyorsa tutulur (ilk görülen; 'en iyi' "
             "değil); hücre = giriş tarihine (t + 1 barı) göre MUM_IZI_HAVUZ dönemi",
}
GT_K2_OLC: Dict[str, Any] = {
    "ufuk": 15, "stop_carpan": 0.98, "taban_m": 20, "t1_en_az": 30, "hedef": [0.05, 0.10], "uc": 0.20, "boot": {"B": 2000, "tohum": 5}, "besli": 5,
    "hucre_karar": ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"], "hucre_bilgi": ["BIST|d1619", "BIST|d2022"], "ana": "K2",
    "karar": {"n": 30, "besli_arti": 4, "kat5": 1.0},
    "tanim": {"giris": "olay penceresi sonu t; giriş = t + 1 barı açılışı (MUM_IZI_HAVUZ.hv25_olc_dizi; geçerli bar takvimi)",
              "R15": "t + 15 barı kapanışı / giriş - 1; R5 (bilgi) = t + 5 barı kapanışı / giriş - 1",
              "stop": "olay: bölge [s, t] dibi x 0,98 (hv25_olc_dizi m = L); taban günü: o günün önceki 20 bar (t - 19 .. t) dibi x 0,98",
              "HEDEF": "giriş barından 15. bara kadar High >= giriş x 1,05 (1,10) stop'tan (Low <= stop) ÖNCE; aynı barda ikisi = stop (hv25_olc_dizi aynen)",
              "uygun": "MUM_IZI_HAVUZ.hv25_uygun: t + 15 veride ve tarihi <= 2022-12-31, giriş tarihi dönemde, giriş > 0 VE giriş > stop; olay da aynı kuralla "
                       "(m = L) ölçülür, değilse durum KESIK / DIS / STOP_ALTI",
              "T1": "aynı hissenin aynı dönemdeki (giriş tarihine göre) BÜTÜN uygun günlerinin (m = 20) R15 ortalaması; uygun gün < 30 ise T1_YOK (olay ölçülmez)",
              "taban": "aynı hisse-dönemin bütün uygun günlerinde aynı kuralla hesaplanan HEDEF5 / HEDEF10 payı ve R15 < -%20 / > +%20 payı; hücre tabanı = "
                       "olaylar üzerinden ortalama",
              "TF15": "R15 - T1 (olay başına); hücrede ortalama + ay kümeli bootstrap %95 (giriş ayı; 2.000; np.random.default_rng(5) her kol x hücrede "
                      "yeniden; KISA_UFUK.ku_boot)",
              "medyan_fark": "medyan(R15) - medyan(T1) (olaylar üzerinden)",
              "besli": "ATRP20 (pencere paneli, t günü) beşlikleri: sınırlar o pazar x dönemin evren pencerelerinin (pencere tarihi dönemde) %20/40/60/80'i "
                       "(getirisiz, olay aşamasında yazılır); beşlik başına TF15 ortalaması; artı beşlik = olayı olan ve TF15 ortalaması > 0",
              "karar": "hücre TUTAR <=> n >= 30 VE TF15 GA alt ucu > 0 VE medyan fark > 0 VE artı beşlik >= 4 VE HEDEF5 katı (pay / taban) > 1; n < 30 "
                       "ÖLÇÜLEMEDİ; aksi TUTMAZ; EMARE (yaşayan evren) <=> ANA kol (K2) dört karar hücresinin dördü TUTAR; BIST bilgi"},
}
GT_K2_DOSYA = {"olay_json": "gt5_olay.json", "onkayit": "GT5_ON_KAYIT.md", "sonuc": "gt5_sonuc.json", "ozet": "gt5_ozet.json", "rapor_tablo": "GT5_RAPOR_TABLO.md",
               "olay_pkl": "k2/k2_olay.pkl", "aday_pkl": "k2/k2_aday.pkl", "getiri_pkl": "k2/k2_getiri.pkl"}
GT_K2_BASLIK = "DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)"
GT_K2_K7 = ("K7 UYARISI: evren bugün yaşayan hisseler; yer şartı en az 2 kat düşmüş hisseleri seçtiği için batanların yokluğu sonucu YUKARI yanlı yapar "
            "(Ç263 dersi); T1 aynı hisseden olduğu için yanlılık farkta kısmen düşer, kalkmaz; artı sonuç en fazla 'EMARE (yaşayan evren)'; batanlar dahil "
            "veriyle sınama Aralık'ta.")


def gt_k2_esik_sha() -> str:
    return hashlib.sha256(json.dumps({"K2": GT_K2, "OLAY": GT_K2_OLAY, "OLC": GT_K2_OLC}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _gt_k2_yol(ad: str, cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    if ad.endswith("_pkl"):
        return os.path.join(ham or GT_YOL["ham"], GT_K2_DOSYA[ad])
    return os.path.join(cikti or GT_YOL["cikti"], GT_K2_DOSYA[ad])


def gt_goz_olcu(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, s: int, t: int, uzak: Optional[int] = None) -> Optional[Dict[str, float]]:
    """Göz cetveli (goz2/cetvel.py goz_olcu AYNEN): bölge [s, t], uzak görünüm = önceki `uzak` bar + bölge; yalnız t'ye kadar okunur."""
    uzak = int(GT_K2["uzak"] if uzak is None else uzak)
    iu = max(0, s - uzak); Hb, Lb, Cb, Ob = H[s:t + 1], L[s:t + 1], C[s:t + 1], O[s:t + 1]; Ho, Lo = H[iu:s], L[iu:s]
    if len(Ho) < int(GT_K2["uzak_en_az"]):
        return None
    ust = float(Hb.max()); alt = float(Lb.min()); kutu = ust - alt
    gust = float(max(Ho.max(), ust)); galt = float(min(Lo.min(), alt)); ga = gust - galt
    boyb = np.median(Hb - Lb); boyo = np.median((H[iu:s] - L[iu:s]))
    govb = np.median(np.abs(Cb - Ob)); govo = np.median(np.abs(C[iu:s] - O[iu:s]))
    n = len(Cb); x = np.arange(n); egim = np.polyfit(x, Cb, 1)[0] * (n - 1) / kutu if kutu > 0 and n > 2 else np.nan
    ipk = int(np.argmax(Ho)); dip_once = float(Lo[ipk:].min()) if ipk < len(Lo) else alt
    return dict(KUTU_ORAN=kutu / ga if ga > 0 else np.nan, KUTU_YER=((ust + alt) / 2 - galt) / ga if ga > 0 else np.nan, TEPE_KAT=float(Ho.max()) / ust,
                DUSUS=alt / float(Ho.max()) - 1, TEPE_UZAK=len(Ho) - ipk, ONCE_DIP=dip_once / alt - 1, EGIM=float(egim),
                SON_YER=(Cb[-1] - alt) / kutu if kutu > 0 else np.nan, BOY_ORAN=boyb / boyo if boyo > 0 else np.nan,
                GOV_ORAN=govb / govo if govo > 0 else np.nan, EN_BUYUK=float((Hb - Lb).max() / kutu) if kutu > 0 else np.nan, KUTU_YUZDE=kutu / alt)


def gt_dip_parabol(H: np.ndarray, L: np.ndarray, s: int, t: int, K: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, float]]:
    """Bölgenin son bölümündeki mum DİPLERİNE ikinci derece eğri (goz2/parabol.py dip_parabol AYNEN; K varsayılanı GT_K2['Z'])."""
    K = K or GT_K2["Z"]
    n_b = t - s + 1; n = min(n_b, max(int(K["bolum_en_az"]), n_b // int(K["bolum_pay"]))); i0 = t - n + 1
    Ls = L[i0:t + 1]; ar = float(H[i0:t + 1].max() - Ls.min())
    if n < 8 or ar <= 0:
        return None
    x = np.linspace(-1.0, 1.0, n); yn = (Ls - Ls.mean()) / ar; a, b, c = np.polyfit(x, yn, 2); f = a * x * x + b * x + c
    ss = float(((yn - yn.mean()) ** 2).sum()); r2 = 1.0 - float(((yn - f) ** 2).sum()) / ss if ss > 0 else 0.0
    tx = -b / (2 * a) if abs(a) > 1e-12 else np.nan; dx = float(np.clip(tx, -1, 1)) if np.isfinite(tx) else 1.0
    yuk = float((a + b + c) - (a * dx * dx + b * dx + c)) if a > 0 else 0.0; k3 = max(3, n // 3)
    return dict(a=float(a), tepe_x=float(tx), son_egim=float(2 * a + b), yukselis=yuk, r2=r2, n=n, dip_yer=int(np.argmin(Ls)),
                son_dip=float((Ls[-int(K["son_bar"]):].min() - Ls.min()) / ar), son_ucte_dip=float((Ls[-k3:].min() - Ls.min()) / ar))


def gt_dip_parabol_var(p: Optional[Dict[str, float]], K: Optional[Dict[str, Any]] = None) -> bool:
    """Dipler yukarı açılan parabol çiziyor (goz2/parabol.py dip_parabol_var AYNEN)."""
    K = K or GT_K2["Z"]
    return bool(p and p["a"] > 0 and p["son_egim"] > 0 and K["tepe_x"][0] <= p["tepe_x"] <= K["tepe_x"][1] and p["son_dip"] > 0
                and p["son_ucte_dip"] >= K["yuksek_dip"] and p["r2"] >= K["r2"] and p["yukselis"] >= K["yukselis"])


def gt_k2_savunma(Lb: np.ndarray, Hb: np.ndarray, K: Optional[Dict[str, Any]] = None) -> Tuple[bool, int]:
    """Dip savunması (goz2/k2.py AYNEN): kutunun alt taban_pay'ına dokunan barlar; aralarında >= ayri_bar olanlar ayrı dokunuş."""
    K = K or GT_K2["S"]; n = len(Lb); dip = float(Lb.min()); kutu = float(Hb.max() - dip)
    idx = np.where(Lb <= dip + K["taban_pay"] * kutu)[0]; ay: List[int] = []
    for i in idx:
        if not ay or i - ay[-1] >= K["ayri_bar"]:
            ay.append(int(i))
    return bool(len(ay) >= K["dokunus"] and (ay[-1] - ay[0]) >= K["yayilim"] * n), len(ay)


def gt_k2_dip_bitti(L: np.ndarray, s: int, t: int, K: Optional[Dict[str, Any]] = None) -> bool:
    """Derin dip bitti (goz2/k2.py AYNEN): bölge + önceki `once` barın en derin dibi bölge sonundan en az `dipten_bar` bar geride."""
    K = K or GT_K2["B"]; i0 = max(0, s - K["once"])
    return bool((t - (i0 + int(np.argmin(L[i0:t + 1])))) >= K["dipten_bar"])


def gt_k2(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, s: int, t: int) -> Optional[Dict[str, int]]:
    """ÇÖL-K2 beş şart (goz2/k2.py k2 AYNEN): Y yer, M küçük mum, S dip savunması, B derin dip bitti, Z dip parabolü; K2 = beşi, YMSB = parabolsüz dördü."""
    o = gt_goz_olcu(O, H, L, C, s, t)
    if not o:
        return None
    Hb, Lb = H[s:t + 1], L[s:t + 1]; Y, M = GT_K2["Y"], GT_K2["M"]
    y = o["KUTU_ORAN"] <= Y["KUTU_ORAN"] and o["KUTU_YER"] <= Y["KUTU_YER"] and o["TEPE_KAT"] >= Y["TEPE_KAT"]
    m = o["BOY_ORAN"] <= M["BOY_ORAN"] and o["GOV_ORAN"] <= M["GOV_ORAN"]
    sv, nd = gt_k2_savunma(Lb, Hb)
    b = gt_k2_dip_bitti(L, s, t)
    z = gt_dip_parabol_var(gt_dip_parabol(H, L, s, t))
    return dict(Y=int(y), M=int(m), S=int(sv), B=int(b), Z=int(z), dokunus=nd, K2=int(y and m and sv and b and z), YMSB=int(y and m and sv and b))


def gt_k2_yer_vek(H: np.ndarray, L: np.ndarray, s: np.ndarray, t: np.ndarray) -> np.ndarray:
    """YER şartı vektörle (gt_goz_olcu ile aynı aritmetik; ön eleme). s, t aynı uzunluklu pencereler (t - s sabit olmak zorunda değil)."""
    s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); out = np.zeros(len(s), bool); u = int(GT_K2["uzak"]); Y = GT_K2["Y"]
    for Lw in np.unique(t - s + 1):
        k = np.where(t - s + 1 == Lw)[0]; ss, tt = s[k], t[k]; tam = ss >= u
        if tam.any():
            ks = k[tam]; s1 = ss[tam]
            ust = np.lib.stride_tricks.sliding_window_view(H, int(Lw)).max(1)[s1]; alt = np.lib.stride_tricks.sliding_window_view(L, int(Lw)).min(1)[s1]
            homx = np.lib.stride_tricks.sliding_window_view(H, u).max(1)[s1 - u]; lomn = np.lib.stride_tricks.sliding_window_view(L, u).min(1)[s1 - u]
            kutu = ust - alt; gust = np.maximum(homx, ust); galt = np.minimum(lomn, alt); ga = gust - galt
            with np.errstate(invalid="ignore", divide="ignore"):
                ko = np.where(ga > 0, kutu / ga, np.nan); ky = np.where(ga > 0, ((ust + alt) / 2 - galt) / ga, np.nan); tk = homx / ust
            out[ks] = (ko <= Y["KUTU_ORAN"]) & (ky <= Y["KUTU_YER"]) & (tk >= Y["TEPE_KAT"])
        for j in k[~tam]:                                              # kısa geçmiş: tek tek (gt_goz_olcu)
            o = gt_goz_olcu(np.zeros(len(H)), H, L, np.zeros(len(H)), int(s[j]), int(t[j]))
            out[j] = bool(o and o["KUTU_ORAN"] <= Y["KUTU_ORAN"] and o["KUTU_YER"] <= Y["KUTU_YER"] and o["TEPE_KAT"] >= Y["TEPE_KAT"])
    return out


def gt_k2_tekil(df: pd.DataFrame, bar: Optional[int] = None) -> pd.DataFrame:
    """Hisse başına (t, L) artan sırada açgözlü: son tutulan pencerenin sonundan >= bar sonra biten pencere tutulur (ilk görülen)."""
    bar = int(GT_K2_OLAY["tekil"] if bar is None else bar); tut = []
    for _, g in df.sort_values(["sembol", "t", "L"], kind="mergesort").groupby("sembol", sort=True):
        son = None
        for i, tt in zip(g.index, g.t.to_numpy()):
            if son is None or int(tt) - son >= bar:
                tut.append(i); son = int(tt)
    return df.loc[tut].sort_values(["sembol", "t"], kind="mergesort")


def gt_k2_evren(P: pd.DataFrame) -> pd.DataFrame:
    E = GT_K2_OLAY; tr = pd.to_datetime(P["tarih"])
    m = (tr >= pd.Timestamp(E["bas"])) & (tr <= pd.Timestamp(E["son"])) & (P.s >= int(E["s_min"])) & (P.KIL <= float(E["kilitli"])) & \
        (P.govdesiz_pay <= float(E["govdesiz"]))
    return P.loc[m.to_numpy(bool), ["sembol", "L", "s", "t", "tarih", "ATRP20"]].assign(tarih=tr[m.to_numpy(bool)])


def gt_k2_aday_pazar(pazar: str, P: pd.DataFrame, V: Dict[str, pd.DataFrame], denetim: int = 300) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Bir pazarın evren pencerelerinde YER ön elemesi (vektör) + YER'i geçenlerde beş şart (gt_k2). Getirisiz. Denetim: YER'i geçmeyenlerden
    rastgele `denetim` pencerede gt_k2 YER = 0 olmalı; geçenlerin hepsinde gt_k2 YER = 1 olmalı (aksi GTHata)."""
    t0 = time.time(); gt_kesik_kapi(V, f"k2 {pazar}"); R = []; hata = 0; red = []
    for sem, g in P.groupby("sembol", sort=True):
        d = V.get(sem)
        if d is None:
            raise GTHata(f"K10: {pazar} {sem}: pencere panelinde var, seride yok")
        s = g.s.to_numpy(np.int64); t = g.t.to_numpy(np.int64)
        if t.max() >= len(d) or (d.index[t] != pd.DatetimeIndex(g.tarih)).any():
            raise GTHata(f"K10: {pazar} {sem}: pencere t indeksi ile seri tarihi uyuşmuyor")
        O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        y = gt_k2_yer_vek(H, L, s, t)
        for i in np.where(y)[0]:
            try:
                o = gt_k2(O[:t[i] + 1], H[:t[i] + 1], L[:t[i] + 1], C[:t[i] + 1], int(s[i]), int(t[i]))   # t sonrası verilmez
            except Exception as ex:  # noqa: BLE001
                hata += 1; gtlog.warning("k2 %s %s t=%d: %s", pazar, sem, int(t[i]), ex); continue
            if not o or o["Y"] != 1:
                raise GTHata(f"K10: {pazar} {sem} t={int(t[i])}: YER vektör = 1, gt_k2 YER = {o and o['Y']}")
            r = g.iloc[int(i)]; R.append({"pazar": pazar, "sembol": sem, "L": int(r.L), "s": int(r.s), "t": int(r.t), "tarih": r.tarih,
                                           "ATRP20": float(r.ATRP20), **o})
        red.extend((sem, int(s[i]), int(t[i])) for i in np.where(~y)[0][:: max(1, int((~y).sum()) // 3 + 1)])
    rng = np.random.default_rng(5)
    for j in rng.permutation(len(red))[:denetim]:
        sem, s_, t_ = red[int(j)]; d = V[sem]; o = gt_k2(*(d[c].to_numpy(float)[:t_ + 1] for c in ("Open", "High", "Low", "Close")), s_, t_)
        if o and o["Y"] != 0:
            raise GTHata(f"K10: {pazar} {sem} t={t_}: YER vektör = 0, gt_k2 YER = 1")
    A = pd.DataFrame(R)
    gtlog.info("k2 %s: evren %d pencere, YER %d, K2 %d (%.0f sn; hata %d)", pazar, len(P), len(A), int(A.K2.sum()) if len(A) else 0, time.time() - t0, hata)
    return A, {"evren": int(len(P)), "evren_hisse": int(P.sembol.nunique()), "yer_pencere": int(len(A)), "hata": hata, "denetim_red": int(min(denetim, len(red)))}


def gt_k2_besli_sinir(P: pd.DataFrame) -> Dict[str, List[float]]:
    """ATRP20 beşlik sınırları: dönem (pencere tarihi) başına evren pencerelerinin %20/40/60/80'i (getirisiz)."""
    import MUM_IZI_HAVUZ as HV
    out = {}
    for dn in ("d1619", "d2022"):
        a, b = HV.HV_ESIK["hucre"]["donem"][dn]; x = P.ATRP20[(P.tarih >= pd.Timestamp(a)) & (P.tarih <= pd.Timestamp(b))].to_numpy(float)
        x = x[np.isfinite(x)]; out[dn] = [float(v) for v in np.quantile(x, [0.2, 0.4, 0.6, 0.8])] if len(x) else []
    return out


def gt_k2_olay_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """k2olay: üç kol için olay listesi (getirisiz) -> k2/k2_aday.pkl, k2/k2_olay.pkl, gt5_olay.json (sayımlar, beşlik sınırları, sha)."""
    import MUM_IZI_HAVUZ as HV
    os.makedirs(os.path.dirname(_gt_k2_yol("olay_pkl", ham=ham)), exist_ok=True)
    AD, OL, J = [], [], {"surum": GT_SURUM + " + ÇÖL-K2 (EK 5)", "baslik": GT_K2_BASLIK, "kod_sha": gt_kod_sha(), "k2_esik_sha": gt_k2_esik_sha(),
                         "pazar": {}, "besli_sinir": {}, "sayim": {}}
    for p in GT_K2_OLAY["pazar"]:
        Vd = MI.mi_veri(p, GT_YOL["acik"]); V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}
        P = gt_k2_evren(gt_yukle(p, ham)); J["besli_sinir"][p] = gt_k2_besli_sinir(P)
        A, ist = gt_k2_aday_pazar(p, P, V); J["pazar"][p] = ist
        if len(A):
            A["giris_tarih"] = [V[s].index[t + 1] if t + 1 < len(V[s]) else pd.NaT for s, t in zip(A.sembol, A.t)]
            A["hucre"] = [HV.hv_hucre_ad(g, p) if pd.notna(g) else f"{p}|yok" for g in A.giris_tarih]
            A["son15_tarih"] = [V[s].index[t + 15] if t + 15 < len(V[s]) else pd.NaT for s, t in zip(A.sembol, A.t)]
            AD.append(A)
            for kol in GT_K2_OLAY["kollar"]:
                T = gt_k2_tekil(A[A[kol] == 1]).assign(kol=kol); OL.append(T)
        del Vd, V, P; gc.collect()
    AD = pd.concat(AD, ignore_index=True); OL = pd.concat(OL, ignore_index=True)
    if not (pd.to_datetime(OL.tarih).max() <= GT_KESIK):
        raise GTHata("KESİK: olay tarihi > 2022-12-31")
    for ad, X in (("aday_pkl", AD), ("olay_pkl", OL)):
        with open(_gt_k2_yol(ad, ham=ham), "wb") as f:
            pickle.dump(X, f, protocol=4)
    J["olay_sha"] = MI._mi_sha(_gt_k2_yol("olay_pkl", ham=ham)); J["aday_sha"] = MI._mi_sha(_gt_k2_yol("aday_pkl", ham=ham))
    J["sayim"] = gt_k2_sayim(OL); J["aday_sart"] = {p: {k: int(AD[AD.pazar == p][k].sum()) for k in ("Y", "M", "S", "B", "Z", "YMSB", "K2")}
                                                   for p in GT_K2_OLAY["pazar"]}
    MI._mi_jyaz(_gt_k2_yol("olay_json", cikti), J, "gt5 olay json")
    return J


def gt_k2_sayim(OL: pd.DataFrame) -> Dict[str, Any]:
    """Getirisiz sayım: kol x hücre (giriş tarihine göre) olay ve hisse; 15. bar kesik sonrası olanlar ayrıca; L dağılımı."""
    out: Dict[str, Any] = {}
    for kol, g in OL.groupby("kol"):
        o = {}
        for h, gg in g.groupby("hucre"):
            kes = gg.son15_tarih.isna() | (pd.to_datetime(gg.son15_tarih) > GT_KESIK)
            o[h] = {"olay": int(len(gg)), "hisse": int(gg.sembol.nunique()), "kesik15": int(kes.sum()),
                    "L": {str(int(k)): int(v) for k, v in gg.L.value_counts().sort_index().items()}}
        out[kol] = o
    return out


# ---------------------------------------------------------------- İŞ B: sonrası (ön kayıttan SONRA; bir kez)
_GT_K2_DURUM = {"kapi": False}


def gt_k2_taban(A: Dict[str, Any], dn: str) -> Optional[Dict[str, float]]:
    """Aynı hisse, aynı dönem, bütün uygun günler (m = 20): T1 (R15 ortalaması), medyan R15, HEDEF5 / HEDEF10 payı, R15 < -%20 / > +%20 payı."""
    import MUM_IZI_HAVUZ as HV
    if not _GT_K2_DURUM["kapi"]:
        raise GTHata("sonrası: kapı açılmadan getiri hesaplanmaz")
    a, b = HV.HV_ESIK["hucre"]["donem"][dn]; m = int(GT_K2_OLC["taban_m"])
    tu = HV.hv25_uygun(A, m, [], a, b, GT_KESIK)
    if len(tu) < int(GT_K2_OLC["t1_en_az"]):
        return None
    o = HV.hv25_olc_dizi(A, tu, m); R = o["R15"]; u = float(GT_K2_OLC["uc"])
    return {"T1": float(R.mean()), "T1_med": float(np.median(R)), "tb5": float(o["d5"].mean()), "tb10": float(o["d10"].mean()),
            "tbalt": float((R < -u).mean()), "tbust": float((R > u).mean()), "t1_n": int(len(tu))}


def gt_k2_olay_olc(A: Dict[str, Any], t: np.ndarray, Lw: np.ndarray, giris_dn: List[Optional[str]]) -> pd.DataFrame:
    """Olay başına durum ve sonrası: hv25_uygun (m = L) üyeliği, hv25_olc_dizi (E0, stop, R15, d5, d10), R5 (bilgi)."""
    import MUM_IZI_HAVUZ as HV
    if not _GT_K2_DURUM["kapi"]:
        raise GTHata("sonrası: kapı açılmadan getiri hesaplanmaz")
    U = int(GT_K2_OLC["ufuk"]); n = int(A["n"]); rows = []
    for tt, L_, dn in zip(np.asarray(t, np.int64), np.asarray(Lw, np.int64), giris_dn):
        r = {"durum": "", "E0": np.nan, "stop": np.nan, "R15": np.nan, "R5": np.nan, "d5": np.nan, "d10": np.nan}
        if tt + U >= n or A["tarih"][tt + U] > GT_KESIK:
            r["durum"] = "KESIK"
        elif dn is None:
            r["durum"] = "DIS"
        else:
            a, b = HV.HV_ESIK["hucre"]["donem"][dn]
            if int(tt) not in set(HV.hv25_uygun(A, int(L_), [], a, b, GT_KESIK).tolist()):
                r["durum"] = "STOP_ALTI"
            else:
                o = HV.hv25_olc_dizi(A, np.array([tt]), int(L_))
                r.update({"durum": "TAMAM", "E0": float(o["E0"][0]), "stop": float(o["stop"][0]), "R15": float(o["R15"][0]), "d5": float(o["d5"][0]),
                          "d10": float(o["d10"][0]), "R5": float(A["DC"][A["ei"][tt + 5]] / o["E0"][0] - 1)})
        rows.append(r)
    return pd.DataFrame(rows)


def gt_k2_boot(x: np.ndarray, ay: np.ndarray) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama: KISA_UFUK.ku_boot; ağırlık matrisi np.random.default_rng(5) (her çağrıda yeniden), B = 2.000."""
    import KISA_UFUK as KU
    u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = np.random.default_rng(int(GT_K2_OLC["boot"]["tohum"])).multinomial(K, np.full(K, 1.0 / K), size=int(GT_K2_OLC["boot"]["B"])).astype(float)
    return KU.ku_boot(np.asarray(x, float), k, W)


def gt_k2_besli(atr: np.ndarray, sinir: List[float]) -> np.ndarray:
    """ATRP20 beşliği 1..5 (sınıra eşit değer alt beşliğe: searchsorted left); sınır yoksa 0."""
    if not sinir:
        return np.zeros(len(atr), int)
    return np.searchsorted(np.asarray(sinir, float), np.asarray(atr, float), side="left") + 1


def gt_k2_hucre(g: pd.DataFrame) -> Dict[str, Any]:
    """Bir kol x hücre satırı (yalnız TAMAM olaylar)."""
    o: Dict[str, Any] = {"n": int(len(g)), "hisse": int(g.sembol.nunique()) if len(g) else 0}
    if not len(g):
        return o
    R = g.R15.to_numpy(float); TF = R - g.T1.to_numpy(float); ay = pd.to_datetime(g.giris_tarih).dt.strftime("%Y-%m").to_numpy()
    o["ay"] = int(len(np.unique(ay))); o["TF15"] = gt_k2_boot(TF, ay); o["R15_ort"] = float(R.mean()); o["T1_ort"] = float(g.T1.mean())
    o["medyan_fark"] = float(np.median(R) - np.median(g.T1.to_numpy(float))); o["TF15_medyan"] = float(np.median(TF)); o["R5_ort"] = float(g.R5.mean())
    for x in ("5", "10"):
        d = float(g[f"d{x}"].mean()); tb = float(g[f"tb{x}"].mean()); o[f"HEDEF{x}"] = d; o[f"taban{x}"] = tb; o[f"kat{x}"] = d / tb if tb > 0 else None
    u = float(GT_K2_OLC["uc"])
    o["alt20"] = float((R < -u).mean()); o["taban_alt20"] = float(g.tbalt.mean()); o["ust20"] = float((R > u).mean()); o["taban_ust20"] = float(g.tbust.mean())
    bs = {}
    for q in range(1, int(GT_K2_OLC["besli"]) + 1):
        m = g.besli.to_numpy() == q; bs[str(q)] = {"n": int(m.sum()), "TF15": float(TF[m].mean()) if m.any() else None}
    o["besli"] = bs; o["besli_arti"] = int(sum(1 for v in bs.values() if v["n"] > 0 and v["TF15"] > 0))
    return o


def gt_k2_karar(o: Dict[str, Any]) -> str:
    K = GT_K2_OLC["karar"]
    if o.get("n", 0) < int(K["n"]):
        return "ÖLÇÜLEMEDİ"
    tf = o["TF15"]; kat = o.get("kat5")
    ok = tf.get("alt") is not None and tf["alt"] > 0 and o["medyan_fark"] > 0 and o["besli_arti"] >= int(K["besli_arti"]) and kat is not None and kat > float(K["kat5"])
    return "TUTAR" if ok else "TUTMAZ"


def gt_k2_olc_hesap(OL: pd.DataFrame, sinir: Dict[str, Dict[str, List[float]]], ham: Optional[str] = None) -> pd.DataFrame:
    """Bütün olaylar: durum, sonrası, T1 ve tabanlar, beşlik. Seri tarihi pencere tarihiyle assert edilir."""
    import MUM_IZI_HAVUZ as HV
    parca = []
    for p in GT_K2_OLAY["pazar"]:
        Op = OL[OL.pazar == p]
        if not len(Op):
            continue
        Vd = MI.mi_veri(p, GT_YOL["acik"]); V = Vd["V"]; gt_kesik_kapi(V, f"k2 sonrası {p}")
        for sem, g in Op.groupby("sembol", sort=True):
            A = HV.hv25_dizi(V[sem], None); t = g.t.to_numpy(np.int64)
            if (A["tarih"][t] != pd.DatetimeIndex(g.tarih)).any():
                raise GTHata(f"K10: {p} {sem}: olay t tarihi seriyle uyuşmuyor")
            dn = [h.split("|")[1] if h.split("|")[1] in ("d1619", "d2022") else None for h in g.hucre]
            Y = gt_k2_olay_olc(A, t, g.L.to_numpy(np.int64), dn).set_index(g.index)
            TB = {d_: gt_k2_taban(A, d_) for d_ in set(x for x in dn if x)}
            for c in ("T1", "T1_med", "tb5", "tb10", "tbalt", "tbust", "t1_n"):
                Y[c] = [TB[d_][c] if d_ and TB.get(d_) else np.nan for d_ in dn]
            Y.loc[(Y.durum == "TAMAM") & ~np.isfinite(Y.T1.to_numpy(float)), "durum"] = "T1_YOK"
            Y["besli"] = [int(gt_k2_besli([a_], sinir[p].get(d_, []))[0]) if d_ else 0 for a_, d_ in zip(g.ATRP20, dn)]
            parca.append(pd.concat([g, Y], axis=1))
        del Vd, V; gc.collect()
    return pd.concat(parca)


def gt_k2_tablo(G: pd.DataFrame) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    T = G[G.durum == "TAMAM"]
    for kol in GT_K2_OLAY["kollar"]:
        out[kol] = {}
        for h in GT_K2_OLC["hucre_karar"] + GT_K2_OLC["hucre_bilgi"]:
            o = gt_k2_hucre(T[(T.kol == kol) & (T.hucre == h)]); o["karar"] = gt_k2_karar(o)
            o["durum"] = {k: int(v) for k, v in G[(G.kol == kol) & (G.hucre == h)].durum.value_counts().items()}; out[kol][h] = o
    ana = [out[GT_K2_OLC["ana"]][h]["karar"] for h in GT_K2_OLC["hucre_karar"]]
    out["_karar"] = {"ana_kol": GT_K2_OLC["ana"], "hucre": dict(zip(GT_K2_OLC["hucre_karar"], ana)),
                     "sonuc": "EMARE (yaşayan evren)" if all(k == "TUTAR" for k in ana) else "EMARE DEĞİL (dört karar hücresinin dördü tutmadı)"}
    return out


def gt_k2_olc_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """k2olc: kapılar (ön kayıt commit + push, kontrol listesi, olay sha, kod sha, ikinci koşu yok) -> sonrası -> gt5_sonuc.json, gt5_ozet.json, tablo md."""
    if os.path.exists(_gt_k2_yol("sonuc", cikti)):
        raise GTHata("gt5_sonuc.json zaten var (ikinci koşu DURUR)")
    c_on = gt_kapi_commit(_gt_k2_yol("onkayit", cikti), "GT5_ON_KAYIT.md")
    import IZ_KARNE as IK
    kk = IK.ik_kontrol_kapisi(_gt_k2_yol("onkayit", cikti))
    J = json.load(open(_gt_k2_yol("olay_json", cikti), encoding="utf-8"))
    if MI._mi_sha(_gt_k2_yol("olay_pkl", ham=ham)) != J["olay_sha"]:
        raise GTHata("olay dosyası ön kayıttaki sha ile aynı değil")
    if J["kod_sha"] != gt_kod_sha() or J["k2_esik_sha"] != gt_k2_esik_sha():
        raise GTHata("kod / eşik sha olay aşamasından sonra değişmiş (SAPMA)")
    on = open(_gt_k2_yol("onkayit", cikti), encoding="utf-8").read()
    if J["kod_sha"] not in on or J["olay_sha"] not in on:
        raise GTHata("ön kayıtta kod sha / olay sha yazılı değil")
    _GT_K2_DURUM["kapi"] = True; bas = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        OL = pickle.load(open(_gt_k2_yol("olay_pkl", ham=ham), "rb"))
        G = gt_k2_olc_hesap(OL, J["besli_sinir"], ham)
    finally:
        _GT_K2_DURUM["kapi"] = False
    with open(_gt_k2_yol("getiri_pkl", ham=ham), "wb") as f:
        pickle.dump(G, f, protocol=4)
    TB = gt_k2_tablo(G)
    S = {"baslik": GT_K2_BASLIK, "k7": GT_K2_K7, "baslangic": bas, "onkayit_commit": c_on, "kontrol_kapisi": kk["gecti"], "kod_sha": gt_kod_sha(),
         "k2_esik_sha": gt_k2_esik_sha(), "olay_sha": J["olay_sha"], "getiri_sha": MI._mi_sha(_gt_k2_yol("getiri_pkl", ham=ham)), "tablo": TB}
    MI._mi_jyaz(_gt_k2_yol("sonuc", cikti), S, "gt5 sonuç")
    Z = {"baslik": GT_K2_BASLIK, "karar": TB["_karar"], "satir": [
        {"kol": kol, "hucre": h, "n": o["n"], "hisse": o["hisse"], "TF15": (o.get("TF15") or {}).get("ort"), "TF15_alt": (o.get("TF15") or {}).get("alt"),
         "TF15_ust": (o.get("TF15") or {}).get("ust"), "medyan_fark": o.get("medyan_fark"), "HEDEF5": o.get("HEDEF5"), "taban5": o.get("taban5"),
         "kat5": o.get("kat5"), "HEDEF10": o.get("HEDEF10"), "taban10": o.get("taban10"), "alt20": o.get("alt20"), "taban_alt20": o.get("taban_alt20"),
         "ust20": o.get("ust20"), "taban_ust20": o.get("taban_ust20"), "besli_arti": o.get("besli_arti"), "karar": o["karar"]}
        for kol in GT_K2_OLAY["kollar"] for h, o in TB[kol].items()]}
    MI._mi_jyaz(_gt_k2_yol("ozet", cikti), Z, "gt5 özet")
    MI._mi_yaz(_gt_k2_yol("rapor_tablo", cikti), gt_k2_tablo_md(TB), "gt5 tablo md")
    return Z


def gt_k2_tablo_md(TB: Dict[str, Any]) -> str:
    def y(v: Any, n: int = 1) -> str:
        return "—" if v is None or (isinstance(v, float) and not np.isfinite(v)) else f"{100 * v:.{n}f}"
    L_ = [f"## {GT_K2_BASLIK}", "", GT_K2_K7, "",
          "| kol | hücre | n | hisse | TF15 % [GA] | medyan fark % | HEDEF5 / taban / kat | HEDEF10 / taban | R15<-20% / taban | R15>+20% / taban | artı beşlik | karar |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for kol in GT_K2_OLAY["kollar"]:
        for h, o in TB[kol].items():
            tf = o.get("TF15") or {}; ks = "—" if o.get("kat5") is None else f"{o['kat5']:.2f}"
            L_.append(f"| {kol} | {h} | {o['n']} | {o['hisse']} | {y(tf.get('ort'), 2)} [{y(tf.get('alt'), 2)}; {y(tf.get('ust'), 2)}] | "
                      f"{y(o.get('medyan_fark'), 2)} | {y(o.get('HEDEF5'))} / {y(o.get('taban5'))} / "
                      f"{ks} | {y(o.get('HEDEF10'))} / {y(o.get('taban10'))} | "
                      f"{y(o.get('alt20'))} / {y(o.get('taban_alt20'))} | {y(o.get('ust20'))} / {y(o.get('taban_ust20'))} | {o.get('besli_arti', '—')} | {o['karar']} |")
    L_ += ["", "Oynaklık (ATRP20) beşlikleri içinde TF15 % (n):", "", "| kol | hücre | B1 | B2 | B3 | B4 | B5 |", "|---|---|---|---|---|---|---|"]
    for kol in GT_K2_OLAY["kollar"]:
        for h, o in TB[kol].items():
            if "besli" in o:
                L_.append(f"| {kol} | {h} | " + " | ".join(f"{y(v['TF15'], 2)} ({v['n']})" for v in o["besli"].values()) + " |")
    k = TB["_karar"]; L_ += ["", f"KARAR KURALI (ANA kol {k['ana_kol']}): " + "; ".join(f"{h} {v}" for h, v in k["hucre"].items()) + f" -> {k['sonuc']}", ""]
    return "\n".join(L_)


def gt_k2_goz2_esles() -> Dict[str, Any]:
    """goz2/k2_onkayit.json'daki GT3 (32) ve GT4 (20) sayfalarının beş şartı GOZ_TESPIT gt_k2 ile yeniden (k2.py hes() ile aynı veri ve kesik)."""
    D = os.path.join(GT_YOL["cikti"], "goz2"); KJ = json.load(open(os.path.join(D, "k2_onkayit.json"), encoding="utf-8")); VV: Dict[Tuple[str, str], Any] = {}

    def veri(p: str, kaynak: str) -> Dict[str, pd.DataFrame]:
        if (p, kaynak) not in VV:
            VV[(p, kaynak)] = MI.mi_veri(p, GT_YOL["tam_bist"] if kaynak == "tam" else GT_YOL["acik"])["V"]
        return VV[(p, kaynak)]

    def hes(r: Dict[str, Any], bit: Optional[str] = None) -> Optional[Dict[str, int]]:
        d = veri(r["pazar"], r.get("kaynak", "acik"))[r["sembol"]]
        if bit:
            d = d[d.index <= pd.Timestamp(bit)]
        return gt_k2(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), int(r["s"]), int(r["t"]))
    J3 = json.load(open(os.path.join(D, "gt3_secim.json"), encoding="utf-8")); A4 = json.load(open(os.path.join(D, "dip_anahtar.json"), encoding="utf-8"))
    out: Dict[str, Any] = {}
    for ad, sayfa, bek, bit in (("GT3", J3["sayfalar"], KJ["GT3"], lambda r: J3["kit_bit"][str(r["kitaplik_no"])] if r["kaynak"] == "tam" else None),
                                ("GT4", A4, KJ["GT4"], lambda r: None)):
        B = {r["sayfa"]: r for r in bek}; ayni = 0; fark = []
        for r in sayfa:
            no = r.get("sayfa", r.get("no")); o = hes(r, bit(r)); e = B[no]
            if all(int(o[k]) == int(e[k]) for k in ("Y", "M", "S", "B", "Z", "K2", "YMSB", "dokunus")):
                ayni += 1
            else:
                fark.append(no)
        out[ad] = {"sayfa": len(sayfa), "ayni": ayni, "fark": fark}
    return out


# ================================================================ 12) ÇÖL-K2 KIRILIM (EK 6, 27 Kas 2026; iş tanımı GT6_IS_TANIMI.md)
# Dondurulmuş ÇÖL-K2 olayları (k2/k2_olay.pkl; GT5 ön kayıt sha) üzerinde (A) YÖN: bölge tavanı mı önce kırılıyor, dibi mi (Kontrol 1: aynı hisse, aynı
# dönem, aynı L, Y'yi sağlamayan havuz pencereleri) ve (B) KIRILIM SONRASI: tavan kırılımından sonraki açılışla girişte 15 bar (Kontrol 2: aynı hissenin
# aynı dönemdeki sıradan tavan kırılımları). Şart / eşik / olay değişmez. Yön ve sonrası SONUÇ ölçüsüdür: k2kirsay yalnız getirisiz sayım yapar.
GT_K2K: Dict[str, Any] = {
    "izleme": 20, "ufuk": 15, "tekil": 15, "k1_en_az": 5, "k2_en_az": 5, "hedef": [0.05, 0.10], "uc": 0.20, "boot": {"B": 2000, "tohum": 6},
    "besli": 5, "besli_en_az": 20, "besli_pay": 0.75, "besli_sart_en_az": 2, "karar": {"yon_n": 50, "kir_n": 30},
    "hucre_karar": ["ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"], "hucre_bilgi": ["BIST|d1619", "BIST|d2022"], "ana": "K2",
    "emare_hucre": ["ABD|d1619", "ABD|d2022"],
    "olay_sha": "e0ef464c8159b1f403ba03537352e939ea699b3a2a5c6148366485eae99cbf55",
    "tanim": {
        "bolge": "bölge [s, t] (olay dosyası); TAVAN = bölgedeki en yüksek High, DİP = en düşük Low",
        "izleme": "t'den sonraki 20 geçerli bar (High > Low); 20. barın tarihi > 2022-12-31 ya da veri yetmiyorsa KESIK (sayım dışı; kırılım önce gelse de)",
        "yon": "YUKARI = izlemede Close > TAVAN olan ilk bar b, AŞAĞI = Close < DİP olan ilk bar; hangisi önce; 20 barda hiçbiri yoksa KIRILMADI; Close ile "
               "ikisi aynı barda olamaz (TAVAN >= DİP); fitil delmesi kırılım sayılmaz",
        "kontrol1": "aynı hisse, aynı dönem (t + 1 barı tarihine göre), aynı L, evren şartları aynı (gt_k2_evren), gt_k2_yer_vek YER = 0 havuz pencereleri; "
                    "KESIK olmayanlarda aynı YÖN kuralı; taban = hisse-dönem-L içinde YUKARI payı (en az 5 pencere; azsa olay A'dan düşer, sayılır)",
        "fark_yon": "olay başına 1[YUKARI] - taban; hücre ortalaması + ay kümeli bootstrap %95 (t + 1 ayı; 2.000; np.random.default_rng(6) her ölçüde yeniden)",
        "giris": "yalnız YUKARI önce: giriş = b + 1 barı açılışı (MUM_IZI_HAVUZ.hv25_olc_dizi karar barı b); R15 = b + 15 barı kapanışı / giriş - 1 "
                 "(giriş barı 1. bar; KISA_UFUK / GT5 ile aynı); b + 15 barı tarihi > 2022-12-31 ya da veride yoksa KESIK",
        "simetrik": "b + 1 .. b + 15 barlarında High >= giriş x 1,05 mi önce, Low <= giriş x 0,95 mi; aynı barda ikisi = BELİRSİZ (o ölçünün hem payından hem "
                    "paydasından çıkar); hiçbiri = YOK (paydada kalır); %10 için aynısı; stop yok",
        "kontrol2": "Kontrol 1 pencerelerinden YUKARI önce gelenlerin b günleri, hisse başına tekil (b artan; < 15 bar arayla gelen sonrakiler düşer), dönem = "
                    "giriş (b + 1) tarihine göre; aynı giriş / R15 / simetrik kuralı; T1k = hisse-dönem içinde KESIK olmayan kırılımların R15 ortalaması "
                    "(en az 5; azsa olay B'den düşer, sayılır); tabanlar (simetrik +%5 / +%10 payı, R15 < -%20 / > +%20 payı) aynı kırılımlardan",
        "tekil": "olay kırılımları kol + hisse başına b artan; önceki tutulandan < 15 bar sonra gelen düşer (Kontrol 2 ile aynı kural)",
        "hucre": "olayın hücresi olay dosyasındaki 'hucre' (giriş t + 1 tarihine göre; dondurulmuş); T1k ve Kontrol 1 aynı dönemden",
        "T1": "bilgi: GT5 / Ç271 ile aynı T1 (gt_k2_taban; aynı hisse-dönemin bütün uygun günleri, m = 20)",
        "besli": "olayın ATRP20 beşliği (gt5_olay.json besli_sinir, dondurulmuş); yalnız >= 20 olaylı beşliklerde TFk15 ortalaması",
        "karar_yon": "YÖN hücresi TUTAR <=> Kontrol 1 tabanı olan bölge >= 50 VE fark GA alt ucu > 0; bölge < 50 ÖLÇÜLEMEDİ; aksi TUTMAZ",
        "karar_kir": "KIRILIM SONRASI hücresi TUTAR <=> n giriş >= 30 VE TFk15 GA alt ucu > 0 VE medyan(R15) - medyan(T1k) > 0 VE simetrik +%5 farkının GA alt "
                     "ucu > 0 VE >= 20 olaylı beşliklerin en az %75'inde TFk15 > 0 (böyle beşlik 2'den azsa bu şart aranmaz); n < 30 ÖLÇÜLEMEDİ; aksi TUTMAZ",
        "kosullu_bilgi": "BİLGİ (karara girmez): kırılan bölgeler içinde YUKARI payı (yukarı / (yukarı + aşağı)) ve Kontrol 1'in aynı oranı; dar kutu iki "
                         "yönde de kırılımı artırdığı için (mekanik) yukarı önce payının yanında okunur",
        "emare": "her tablo için ayrı: EMARE (yaşayan evren) <=> ANA kol (K2) ABD 2016-19 VE ABD 2020-22 hücrelerinde o tablo TUTAR; iki tablo ayrı yazılır"},
}
GT_K2K_DOSYA = {"sayim": "gt6_sayim.json", "onkayit": "GT6_ON_KAYIT.md", "ozet": "gt6_ozet.json", "gt5_onkayit": "GT5_ON_KAYIT.md",
                "yon_pkl": "k2/k2k_yon.pkl", "kir_pkl": "k2/k2k_kir.pkl", "kon_pkl": "k2/k2k_kontrol.pkl", "konkir_pkl": "k2/k2k_kontrol_kir.pkl"}
_GT_K2K_DURUM = {"kapi": False}


def gt_k2k_esik_sha() -> str:
    return hashlib.sha256(json.dumps(GT_K2K, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _gt_k2k_yol(ad: str, cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    if ad.endswith("_pkl"):
        return os.path.join(ham or GT_YOL["ham"], GT_K2K_DOSYA[ad])
    return os.path.join(cikti or GT_YOL["cikti"], GT_K2K_DOSYA[ad])


def gt_k2k_izleme(H: np.ndarray, L: np.ndarray, tarih: pd.DatetimeIndex, t: np.ndarray, izleme: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """İzleme penceresi: her t için sonraki `izleme` geçerli barın (High > Low) indeksleri (satır başına). Dönen (IX, kesik): IX[i] = indeksler (kesikte -1),
    kesik[i] = 20. bar veride yok ya da tarihi > 2022-12-31. Getirisiz (yalnız takvim)."""
    izleme = int(GT_K2K["izleme"] if izleme is None else izleme); t = np.asarray(t, np.int64)
    vi = np.where((np.asarray(H, float) > np.asarray(L, float)))[0]; pos = np.searchsorted(vi, t, side="right")
    kes = pos + izleme > len(vi); IX = np.full((len(t), izleme), -1, np.int64)
    ok = ~kes
    if ok.any():
        IX[ok] = vi[pos[ok][:, None] + np.arange(izleme)[None, :]]
        son = pd.DatetimeIndex(tarih)[IX[ok, -1]]; kes[np.where(ok)[0][son > GT_KESIK]] = True
    IX[kes] = -1
    return IX, kes


def gt_k2k_tavan_dip(H: np.ndarray, L: np.ndarray, s: np.ndarray, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Bölge [s, t] TAVAN (en yüksek High) ve DİP (en düşük Low); yalnız s..t okunur."""
    s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); TV = np.full(len(s), np.nan); DP = np.full(len(s), np.nan)
    for Lw in np.unique(t - s + 1):
        k = np.where(t - s + 1 == Lw)[0]
        TV[k] = np.lib.stride_tricks.sliding_window_view(H, int(Lw)).max(1)[s[k]]; DP[k] = np.lib.stride_tricks.sliding_window_view(L, int(Lw)).min(1)[s[k]]
    return TV, DP


GT_K2K_YON = {1: "YUKARI", -1: "ASAGI", 0: "KIRILMADI", -9: "KESIK"}


def gt_k2k_yon(H: np.ndarray, L: np.ndarray, C: np.ndarray, tarih: pd.DatetimeIndex, s: np.ndarray, t: np.ndarray,
               izleme: Optional[int] = None) -> Dict[str, np.ndarray]:
    """YÖN kuralı (vektör): yon 1 / -1 / 0 / -9 (YUKARI / AŞAĞI / KIRILMADI / KESIK), b = kırılım barı indeksi (yoksa -1), k = kırılım izlemenin kaçıncı
    geçerli barı (1..20; yoksa 0), TAVAN, DİP. Kırılım kararı b barında yalnız b'ye kadar okunur; izleme penceresinden sonrası hiç okunmaz."""
    s = np.asarray(s, np.int64); t = np.asarray(t, np.int64); TV, DP = gt_k2k_tavan_dip(H, L, s, t); IX, kes = gt_k2k_izleme(H, L, tarih, t, izleme)
    n = len(t); yon = np.full(n, -9, np.int64); b = np.full(n, -1, np.int64); k = np.zeros(n, np.int64); ok = ~kes
    if ok.any():
        Cw = np.asarray(C, float)[IX[ok]]; up = Cw > TV[ok][:, None]; dn = Cw < DP[ok][:, None]; BIG = 10 ** 9
        ku = np.where(up.any(1), up.argmax(1), BIG); kd = np.where(dn.any(1), dn.argmax(1), BIG)
        y = np.where((ku == BIG) & (kd == BIG), 0, np.where(ku < kd, 1, -1)); y = np.where((ku == kd) & (ku < BIG), 0, y)   # aynı bar olanaksız (TAVAN >= DİP)
        kk = np.where(y == 1, ku, np.where(y == -1, kd, -1)); io = np.where(ok)[0]
        yon[io] = y; k[io] = np.where(kk >= 0, kk + 1, 0); b[io] = np.where(kk >= 0, IX[io, np.maximum(kk, 0)], -1)
    return {"yon": yon, "b": b, "k": k, "TAVAN": TV, "DIP": DP}


def gt_k2k_simetrik(DH: np.ndarray, DL: np.ndarray, g0: np.ndarray, e15: np.ndarray, E0: np.ndarray, x: float) -> np.ndarray:
    """Simetrik ilk dokunuş: g0..e15 barlarında High >= E0 (1 + x) mi önce (1), Low <= E0 (1 - x) mi (-1); aynı barda ikisi 2 (BELİRSİZ); hiçbiri 0.
    e15'ten sonrası okunmaz."""
    g0 = np.asarray(g0, np.int64); e15 = np.asarray(e15, np.int64); E0 = np.asarray(E0, float); out = np.zeros(len(g0), np.int64)
    if not len(g0):
        return out
    Lm = int((e15 - g0).max()) + 1; ix = g0[:, None] + np.arange(Lm)[None, :]; val = ix <= e15[:, None]; ix = np.minimum(ix, len(DH) - 1)
    up = val & (DH[ix] >= (E0 * (1 + x))[:, None]); dn = val & (DL[ix] <= (E0 * (1 - x))[:, None]); BIG = 10 ** 9
    ku = np.where(up.any(1), up.argmax(1), BIG); kd = np.where(dn.any(1), dn.argmax(1), BIG)
    out[(ku < kd)] = 1; out[(kd < ku)] = -1; out[(ku == kd) & (ku < BIG)] = 2
    return out


def gt_k2k_tekil(b: np.ndarray, bar: Optional[int] = None) -> np.ndarray:
    """Kırılım günleri (bir hisse + kol): b artan; önceki tutulandan < bar sonra gelen düşer. Tutulan b'ler (artan, tekil)."""
    bar = int(GT_K2K["tekil"] if bar is None else bar); tut: List[int] = []
    for x in np.unique(np.asarray(b, np.int64)):
        if not tut or int(x) - tut[-1] >= bar:
            tut.append(int(x))
    return np.asarray(tut, np.int64)


def gt_k2k_giris(A: Dict[str, Any], b: np.ndarray) -> Dict[str, np.ndarray]:
    """Kırılım barları b için giriş ve 15 bar: KESIK (b + 15 veride yok / tarihi > 2022-12-31 / giriş geçersiz) ya da E0 = b + 1 açılışı, R15
    (MUM_IZI_HAVUZ.hv25_olc_dizi, karar barı b; stop'lu ölçüleri kullanılmaz), simetrik +%5 / +%10 (gt_k2k_simetrik)."""
    import MUM_IZI_HAVUZ as HV
    b = np.asarray(b, np.int64); U = int(GT_K2K["ufuk"]); n = int(A["n"]); m = len(b)
    out = {"kesik": np.ones(m, bool), "E0": np.full(m, np.nan), "R15": np.full(m, np.nan), "s5": np.zeros(m, np.int64), "s10": np.zeros(m, np.int64),
           "giris_tarih": np.full(m, np.datetime64("NaT"), "datetime64[ns]")}
    if not m:
        return out
    ok = (b >= 0) & (b + U < n)
    ok[ok] = A["tarih"][b[ok] + U] <= GT_KESIK
    if ok.any():
        o = HV.hv25_olc_dizi(A, b[ok], 1); E0 = o["E0"]; fin = np.isfinite(E0) & (E0 > 0); io = np.where(ok)[0]; ok[io[~fin]] = False; io = io[fin]
        out["E0"][io] = E0[fin]; out["R15"][io] = o["R15"][fin]
        for x, ad in zip(GT_K2K["hedef"], ("s5", "s10")):
            out[ad][io] = gt_k2k_simetrik(A["DH"], A["DL"], o["g0"][fin], o["e15"][fin], E0[fin], float(x))
        out["giris_tarih"][io] = pd.DatetimeIndex(A["giris_tarih"][b[io] + 1]).to_numpy()
    out["kesik"] = ~ok
    return out


def gt_k2k_donem(tarih: Any) -> Optional[str]:
    import MUM_IZI_HAVUZ as HV
    if pd.isna(tarih):
        return None
    h = HV.hv_hucre_ad(tarih, "X").split("|")[1]
    return h if h in ("d1619", "d2022") else None


def gt_k2k_donem_vek(tarih: pd.DatetimeIndex, i: np.ndarray) -> np.ndarray:
    """tarih[i] dönemi (d1619 / d2022 / None; i veride yoksa None); gt_k2k_donem ile aynı sınırlar (vektör)."""
    import MUM_IZI_HAVUZ as HV
    i = np.asarray(i, np.int64); out = np.full(len(i), None, object); ok = i < len(tarih)
    if ok.any():
        g = pd.DatetimeIndex(tarih)[i[ok]]; r = np.full(ok.sum(), None, object)
        for dn in ("d1619", "d2022"):
            a, b = HV.HV_ESIK["hucre"]["donem"][dn]; r[(g >= pd.Timestamp(a)) & (g <= pd.Timestamp(b))] = dn
        out[ok] = r
    return out


def gt_k2k_pazar(p: str, OL: pd.DataFrame, V: Dict[str, pd.DataFrame], P: pd.DataFrame, AD: pd.DataFrame, olc: bool) -> Dict[str, Any]:
    """Bir pazar: evren pencerelerinde YER (vektör; k2_aday ile aynı küme, assert), Kontrol 1 pencereleri (YER = 0), izleme KESIK bayrağı. olc=False:
    yalnız getirisiz sayım (pencere / kesik); olc=True (kapı açık): olay ve kontrol YÖN'ü, kontrol kırılımları ve giriş ölçüleri."""
    if olc and not _GT_K2K_DURUM["kapi"]:
        raise GTHata("kırılım: kapı açılmadan yön / getiri hesaplanmaz")
    import MUM_IZI_HAVUZ as HV
    gt_kesik_kapi(V, f"k2k {p}"); OLp = OL[OL.pazar == p]; ADp = AD[AD.pazar == p]
    ad_set: Dict[str, set] = {}
    for a_, b_, c_ in zip(ADp.sembol, ADp.L.astype(int), ADp.t.astype(int)):
        ad_set.setdefault(a_, set()).add((int(b_), int(c_)))
    EV, KP, KK, KS = [], [], [], {}
    for sem, g in P.groupby("sembol", sort=True):
        d = V.get(sem)
        if d is None:
            raise GTHata(f"K10: {p} {sem}: pencere panelinde var, seride yok")
        H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close")); tar = d.index
        if not (H > L).all():
            raise GTHata(f"K3: {p} {sem}: seride High <= Low bar var")
        s = g.s.to_numpy(np.int64); t = g.t.to_numpy(np.int64); Lw = g.L.to_numpy(np.int64)
        if t.max() >= len(d) or (tar[t] != pd.DatetimeIndex(g.tarih)).any():
            raise GTHata(f"K10: {p} {sem}: pencere t indeksi ile seri tarihi uyuşmuyor")
        y = gt_k2_yer_vek(H, L, s, t)
        if set(zip(Lw[y].tolist(), t[y].tolist())) != ad_set.get(sem, set()):
            raise GTHata(f"K10: {p} {sem}: YER = 1 kümesi k2_aday ile aynı değil")
        k = ~y; sk, tk, Lk = s[k], t[k], Lw[k]
        dn = gt_k2k_donem_vek(tar, tk + 1)
        _, kes = gt_k2k_izleme(H, L, tar, tk)
        KP.append(pd.DataFrame({"sembol": sem, "L": Lk, "t": tk, "donem": dn, "kesik": kes}))
        Oe = OLp[OLp.sembol == sem]
        if olc:
            A = HV.hv25_dizi(d, None)
            m = (~kes) & np.array([x is not None for x in dn], bool)
            Yk = gt_k2k_yon(H, L, C, tar, sk[m], tk[m])
            KP[-1] = KP[-1].assign(yon=-9, b=-1); KP[-1].loc[np.where(m)[0], "yon"] = Yk["yon"]; KP[-1].loc[np.where(m)[0], "b"] = Yk["b"]
            bk = gt_k2k_tekil(Yk["b"][Yk["yon"] == 1]); Gk = gt_k2k_giris(A, bk)
            KK.append(pd.DataFrame({"sembol": sem, "b": bk, "kesik": Gk["kesik"], "giris_tarih": Gk["giris_tarih"], "E0": Gk["E0"], "R15": Gk["R15"],
                                    "s5": Gk["s5"], "s10": Gk["s10"]}))
            if len(Oe):
                if (tar[Oe.t.to_numpy(np.int64)] != pd.DatetimeIndex(Oe.tarih)).any():
                    raise GTHata(f"K10: {p} {sem}: olay t tarihi seriyle uyuşmuyor")
                Ye = gt_k2k_yon(H, L, C, tar, Oe.s.to_numpy(np.int64), Oe.t.to_numpy(np.int64))
                X = Oe.assign(yon=Ye["yon"], b=Ye["b"], kbar=Ye["k"], TAVAN=Ye["TAVAN"], DIP=Ye["DIP"])
                dns = sorted(set(h.split("|")[1] for h in X.hucre if h.split("|")[1] in ("d1619", "d2022")))
                TB = {d_: gt_k2_taban(A, d_) for d_ in dns}
                X["T1"] = [TB[h.split("|")[1]]["T1"] if TB.get(h.split("|")[1]) else np.nan for h in X.hucre]
                EV.append(X)
        else:
            if len(Oe):
                _, ke = gt_k2k_izleme(H, L, tar, Oe.t.to_numpy(np.int64)); EV.append(Oe.assign(kesik=ke))
    KP = pd.concat(KP, ignore_index=True); KP["pazar"] = p
    out = {"kontrol": KP, "olay": pd.concat(EV) if EV else OLp.iloc[:0]}
    if olc:
        KK = pd.concat(KK, ignore_index=True) if KK else pd.DataFrame(columns=["sembol", "b", "kesik", "giris_tarih", "E0", "R15", "s5", "s10"])
        KK["pazar"] = p; KK["donem"] = [gt_k2k_donem(x) for x in KK.giris_tarih]; out["kontrol_kir"] = KK
    return out


def _gt_k2k_k1_sayi(KP: pd.DataFrame) -> pd.DataFrame:
    """Kontrol 1 KESIK olmayan pencere adedi (pazar, sembol, dönem, L)."""
    x = KP[(~KP.kesik) & KP.donem.notna()]
    return x.groupby(["pazar", "sembol", "donem", "L"]).size().rename("k1_n").reset_index()


def gt_k2k_sayim_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """k2kirsay: GETİRİSİZ sayım (yön / getiri hesaplanmaz): kol x hücre bölge, izleme KESIK, Kontrol 1 tabanı olan bölge (>= 5 KESIK olmayan pencere),
    Kontrol 1 pencere adetleri (pazar x dönem x L), olayların ATRP20 beşlik dağılımı -> gt6_sayim.json."""
    OL, AD, sinir = _gt_k2k_girdi(cikti, ham); EVs, KPs = [], []
    for p in GT_K2_OLAY["pazar"]:
        Vd = MI.mi_veri(p, GT_YOL["acik"]); V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}; P = gt_k2_evren(gt_yukle(p, ham))
        R = gt_k2k_pazar(p, OL, V, P, AD, olc=False); EVs.append(R["olay"]); KPs.append(R["kontrol"]); del Vd, V, P; gc.collect()
    EV = pd.concat(EVs); KP = pd.concat(KPs, ignore_index=True); K1 = _gt_k2k_k1_sayi(KP)
    EV["donem"] = [h.split("|")[1] for h in EV.hucre]
    EV = EV.merge(K1, how="left", on=["pazar", "sembol", "donem", "L"]); EV["k1_n"] = EV.k1_n.fillna(0).astype(int)
    J: Dict[str, Any] = {"baslik": GT_K2_BASLIK, "surum": GT_SURUM + " + ÇÖL-K2 KIRILIM (EK 6)", "kod_sha": gt_kod_sha(), "k2k_esik_sha": gt_k2k_esik_sha(),
                         "k2_esik_sha": gt_k2_esik_sha(), "olay_sha": MI._mi_sha(_gt_k2_yol("olay_pkl", ham=ham)), "not": "GETİRİSİZ: yön / kırılım / getiri yok",
                         "olay": {}, "kontrol1": {}}
    for kol in GT_K2_OLAY["kollar"]:
        J["olay"][kol] = {}
        for h in GT_K2K["hucre_karar"] + GT_K2K["hucre_bilgi"]:
            g = EV[(EV.kol == kol) & (EV.hucre == h)]; nk = g[~g.kesik]; dn = h.split("|")[1]; p = h.split("|")[0]
            bs = gt_k2_besli(nk.ATRP20.to_numpy(float), sinir[p].get(dn, []))
            J["olay"][kol][h] = {"bolge": int(len(g)), "kesik": int(g.kesik.sum()), "bolge_net": int(len(nk)), "hisse": int(nk.sembol.nunique()),
                                 "k1_tabanli": int((nk.k1_n >= int(GT_K2K["k1_en_az"])).sum()), "k1_duser": int((nk.k1_n < int(GT_K2K["k1_en_az"])).sum()),
                                 "besli": {str(q): int((bs == q).sum()) for q in range(1, 6)}}
    for (p, dn, Lw), g in KP[KP.donem.notna()].groupby(["pazar", "donem", "L"]):
        J["kontrol1"].setdefault(f"{p}|{dn}", {})[str(int(Lw))] = {"pencere": int(len(g)), "kesik": int(g.kesik.sum()), "net": int((~g.kesik).sum()),
                                                                     "hisse": int(g[~g.kesik].sembol.nunique())}
    MI._mi_jyaz(_gt_k2k_yol("sayim", cikti), J, "gt6 sayım json")
    return J


def _gt_k2k_girdi(cikti: Optional[str] = None, ham: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Dondurulmuş girdiler: olay dosyası (sha = GT5 ön kayıttaki; assert), aday dosyası (sha gt5_olay.json; assert), beşlik sınırları (gt5_olay.json)."""
    J5 = json.load(open(_gt_k2_yol("olay_json", cikti), encoding="utf-8")); on5 = open(_gt_k2k_yol("gt5_onkayit", cikti), encoding="utf-8").read()
    sh = MI._mi_sha(_gt_k2_yol("olay_pkl", ham=ham))
    if sh != GT_K2K["olay_sha"] or sh != J5["olay_sha"] or GT_K2K["olay_sha"] not in on5:
        raise GTHata("olay dosyası sha GT5 ön kayıttakiyle aynı değil")
    if MI._mi_sha(_gt_k2_yol("aday_pkl", ham=ham)) != J5["aday_sha"]:
        raise GTHata("aday dosyası sha gt5_olay.json ile aynı değil")
    OL = pickle.load(open(_gt_k2_yol("olay_pkl", ham=ham), "rb")); AD = pickle.load(open(_gt_k2_yol("aday_pkl", ham=ham), "rb"))
    if not (pd.to_datetime(OL.tarih).max() <= GT_KESIK):
        raise GTHata("KESİK: olay tarihi > 2022-12-31")
    OL = OL[OL.hucre.isin(GT_K2K["hucre_karar"] + GT_K2K["hucre_bilgi"])].copy()
    return OL, AD, J5["besli_sinir"]


def gt_k2k_boot(x: np.ndarray, ay: np.ndarray) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama: KISA_UFUK.ku_boot; ağırlıklar np.random.default_rng(6) (her çağrıda yeniden), B = 2.000. Sonlu olmayanlar çıkar."""
    import KISA_UFUK as KU
    x = np.asarray(x, float); f = np.isfinite(x); x = x[f]; ay = np.asarray(ay, str)[f]
    if len(x) < 2:
        return {"n": int(len(x)), "ort": float(x.mean()) if len(x) else None, "medyan": None, "alt": None, "ust": None, "p": None}
    u, k = np.unique(ay, return_inverse=True); K = len(u)
    W = np.random.default_rng(int(GT_K2K["boot"]["tohum"])).multinomial(K, np.full(K, 1.0 / K), size=int(GT_K2K["boot"]["B"])).astype(float)
    return KU.ku_boot(x, k, W)


def gt_k2k_taban1(EV: pd.DataFrame, KP: pd.DataFrame) -> pd.DataFrame:
    """Kontrol 1 tabanı: hisse-dönem-L içinde KESIK olmayan pencerelerde YUKARI payı (en az k1_en_az pencere)."""
    x = KP[(~KP.kesik) & KP.donem.notna()]
    T = x.groupby(["pazar", "sembol", "donem", "L"]).agg(k1_n=("yon", "size"), k1_yuk=("yon", lambda v: float((v == 1).mean())),
                                                        k1_asg=("yon", lambda v: float((v == -1).mean())),
                                                        k1_kos=("yon", lambda v: float((v == 1).sum() / (v != 0).sum()) if (v != 0).any() else np.nan)).reset_index()
    E = EV.copy(); E["donem"] = [h.split("|")[1] for h in E.hucre]
    E = E.merge(T, how="left", on=["pazar", "sembol", "donem", "L"]); E["k1_n"] = E.k1_n.fillna(0).astype(int)
    E.loc[E.k1_n < int(GT_K2K["k1_en_az"]), ["k1_yuk", "k1_asg", "k1_kos"]] = np.nan
    return E


def _gt_k2k_pay(v: np.ndarray) -> Tuple[float, float, int]:
    """Simetrik kod dizisinden (1 / -1 / 0 / 2): (üst önce payı, alt önce payı, belirsiz sayısı); payda belirsizsiz."""
    v = np.asarray(v, np.int64); m = v != 2
    return (float((v[m] == 1).mean()) if m.any() else np.nan, float((v[m] == -1).mean()) if m.any() else np.nan, int((~m).sum()))


def gt_k2k_taban2(KR: pd.DataFrame) -> pd.DataFrame:
    """Kontrol 2 tabanı: hisse-dönem içinde KESIK olmayan sıradan kırılımlar: T1k, medyan, simetrik +%5 / +%10 üst önce payı, R15 < -%20 / > +%20 payı."""
    u = float(GT_K2K["uc"]); x = KR[(~KR.kesik) & KR.donem.notna()]; rows = []
    for (p, sem, dn), g in x.groupby(["pazar", "sembol", "donem"]):
        R = g.R15.to_numpy(float); a5 = _gt_k2k_pay(g.s5.to_numpy()); a10 = _gt_k2k_pay(g.s10.to_numpy())
        rows.append({"pazar": p, "sembol": sem, "donem": dn, "k2_n": int(len(g)), "T1k": float(R.mean()), "tb_s5": a5[0], "tb_s5_alt": a5[1],
                     "tb_s10": a10[0], "tb_s10_alt": a10[1], "tb_alt20": float((R < -u).mean()), "tb_ust20": float((R > u).mean())})
    return pd.DataFrame(rows, columns=["pazar", "sembol", "donem", "k2_n", "T1k", "tb_s5", "tb_s5_alt", "tb_s10", "tb_s10_alt", "tb_alt20", "tb_ust20"])


def gt_k2k_kir_olay(E: pd.DataFrame, V: Dict[str, Dict[str, pd.DataFrame]], T2: pd.DataFrame, sinir: Dict[str, Any]) -> pd.DataFrame:
    """Olay kırılımları (YUKARI önce, KESIK olmayan izleme): kol + hisse tekil (15 bar), giriş ölçüleri, T1k ve tabanlar, beşlik, durum
    (TAMAM / KESIK / T1K_AZ / TEKIL_DUSTU)."""
    import MUM_IZI_HAVUZ as HV
    if not _GT_K2K_DURUM["kapi"]:
        raise GTHata("kırılım: kapı açılmadan getiri hesaplanmaz")
    X = E[E.yon == 1].copy(); parca = []
    for (p, sem), g in X.groupby(["pazar", "sembol"], sort=True):
        A = HV.hv25_dizi(V[p][sem], None)
        for kol, gg in g.groupby("kol"):
            tut = set(gt_k2k_tekil(gg.b.to_numpy(np.int64)).tolist()); gg = gg.sort_values("b").copy(); ilk = ~gg.b.duplicated()
            gg["tekil"] = [bool(bb in tut and i_) for bb, i_ in zip(gg.b, ilk)]
            Gi = gt_k2k_giris(A, gg.b.to_numpy(np.int64))
            for c in ("kesik", "E0", "R15", "s5", "s10", "giris_tarih"):
                gg["kir_kesik" if c == "kesik" else c] = Gi[c]
            parca.append(gg)
    K = pd.concat(parca) if parca else X.assign(tekil=False, kir_kesik=True)
    K = K.merge(T2, how="left", on=["pazar", "sembol", "donem"]); K["k2_n"] = K.k2_n.fillna(0).astype(int)
    K["durum"] = np.where(~K.tekil, "TEKIL_DUSTU", np.where(K.kir_kesik, "KESIK", np.where(K.k2_n < int(GT_K2K["k2_en_az"]), "T1K_AZ", "TAMAM")))
    K["besli"] = [int(gt_k2_besli([a_], sinir[p_].get(d_, []))[0]) for a_, p_, d_ in zip(K.ATRP20, K.pazar, K.donem)]
    return K


def gt_k2k_hucre_yon(g: pd.DataFrame) -> Dict[str, Any]:
    """TABLO A satırı: g = bir kol x hücrenin KESIK olmayan olayları."""
    o: Dict[str, Any] = {"bolge_net": int(len(g))}; a = g[np.isfinite(g.k1_yuk.to_numpy(float))]; o["n"] = int(len(a)); o["k1_duser"] = int(len(g) - len(a))
    o["hisse"] = int(a.sembol.nunique()) if len(a) else 0
    if not len(a):
        return o
    y = a.yon.to_numpy(); ay = pd.to_datetime(a.giris_tarih).dt.strftime("%Y-%m").to_numpy()
    o.update({"yukari": float((y == 1).mean()), "asagi": float((y == -1).mean()), "kirilmadi": float((y == 0).mean()), "taban": float(a.k1_yuk.mean()),
              "taban_asagi": float(a.k1_asg.mean()), "fark": gt_k2k_boot((y == 1).astype(float) - a.k1_yuk.to_numpy(float), ay),
              "kbar_med_yukari": float(np.median(a.kbar[y == 1])) if (y == 1).any() else None,
              "kbar_med_asagi": float(np.median(a.kbar[y == -1])) if (y == -1).any() else None,
              "adet": {"yukari": int((y == 1).sum()), "asagi": int((y == -1).sum()), "kirilmadi": int((y == 0).sum())}})
    kb = (y != 0) & np.isfinite(a.k1_kos.to_numpy(float))                 # BİLGİ (kutu genişliğinden bağımsıza yakın): kırılanlar içinde yukarı payı
    o["kosullu"] = {"n": int(kb.sum()), "pay": float((y[kb] == 1).mean()) if kb.any() else None,
                    "taban": float(a.k1_kos.to_numpy(float)[kb].mean()) if kb.any() else None,
                    "fark": gt_k2k_boot((y[kb] == 1).astype(float) - a.k1_kos.to_numpy(float)[kb], ay[kb])}
    return o


def gt_k2k_karar_yon(o: Dict[str, Any]) -> str:
    if o.get("n", 0) < int(GT_K2K["karar"]["yon_n"]):
        return "ÖLÇÜLEMEDİ"
    f = o.get("fark") or {}
    return "TUTAR" if f.get("alt") is not None and f["alt"] > 0 else "TUTMAZ"


def gt_k2k_hucre_kir(g: pd.DataFrame, durum: Dict[str, int]) -> Dict[str, Any]:
    """TABLO B satırı: g = bir kol x hücrenin TAMAM olay kırılımları."""
    o: Dict[str, Any] = {"n": int(len(g)), "hisse": int(g.sembol.nunique()) if len(g) else 0, "durum": durum}
    if not len(g):
        return o
    R = g.R15.to_numpy(float); T1k = g.T1k.to_numpy(float); TF = R - T1k; ay = pd.to_datetime(g.giris_tarih).dt.strftime("%Y-%m").to_numpy(); u = float(GT_K2K["uc"])
    o.update({"TFk15": gt_k2k_boot(TF, ay), "medyan_fark": float(np.median(R) - np.median(T1k)), "TFk15_medyan": float(np.median(TF)),
              "R15_ort": float(R.mean()), "T1k_ort": float(T1k.mean()), "R15_T1": float(np.nanmean(R - g.T1.to_numpy(float))),
              "alt20": float((R < -u).mean()), "taban_alt20": float(g.tb_alt20.mean()), "ust20": float((R > u).mean()), "taban_ust20": float(g.tb_ust20.mean())})
    for ad in ("s5", "s10"):
        v = g[ad].to_numpy(np.int64); m = (v != 2) & np.isfinite(g[f"tb_{ad}"].to_numpy(float))
        x = (v[m] == 1).astype(float) - g[f"tb_{ad}"].to_numpy(float)[m]
        o[ad] = {"n": int(m.sum()), "belirsiz": int((v == 2).sum()), "pay": float((v[m] == 1).mean()) if m.any() else None,
                 "pay_alt": float((v[m] == -1).mean()) if m.any() else None, "taban": float(g[f"tb_{ad}"].to_numpy(float)[m].mean()) if m.any() else None,
                 "taban_alt": float(np.nanmean(g[f"tb_{ad}_alt"].to_numpy(float)[m])) if m.any() else None, "fark": gt_k2k_boot(x, ay[m])}
    bs = {}
    for q in range(1, int(GT_K2K["besli"]) + 1):
        m = g.besli.to_numpy() == q; bs[str(q)] = {"n": int(m.sum()), "TFk15": float(TF[m].mean()) if m.any() else None}
    buyuk = [v for v in bs.values() if v["n"] >= int(GT_K2K["besli_en_az"])]
    o["besli"] = bs; o["besli_buyuk"] = len(buyuk); o["besli_arti"] = int(sum(1 for v in buyuk if v["TFk15"] > 0))
    return o


def gt_k2k_karar_kir(o: Dict[str, Any]) -> str:
    if o.get("n", 0) < int(GT_K2K["karar"]["kir_n"]):
        return "ÖLÇÜLEMEDİ"
    tf = o["TFk15"]; f5 = (o.get("s5") or {}).get("fark") or {}
    bes = True if o["besli_buyuk"] < int(GT_K2K["besli_sart_en_az"]) else o["besli_arti"] >= float(GT_K2K["besli_pay"]) * o["besli_buyuk"]
    ok = (tf.get("alt") is not None and tf["alt"] > 0 and o["medyan_fark"] > 0 and f5.get("alt") is not None and f5["alt"] > 0 and bes)
    return "TUTAR" if ok else "TUTMAZ"


def gt_k2k_tablo(E: pd.DataFrame, K: pd.DataFrame) -> Dict[str, Any]:
    """İki tablo (kol x hücre) + karar. E: bütün olaylar (yon, k1_yuk); K: olay kırılımları (durum)."""
    out: Dict[str, Any] = {"A": {}, "B": {}}
    for kol in GT_K2_OLAY["kollar"]:
        out["A"][kol] = {}; out["B"][kol] = {}
        for h in GT_K2K["hucre_karar"] + GT_K2K["hucre_bilgi"]:
            g = E[(E.kol == kol) & (E.hucre == h)]; oa = gt_k2k_hucre_yon(g[g.yon != -9]); oa["bolge"] = int(len(g)); oa["kesik"] = int((g.yon == -9).sum())
            oa["karar"] = gt_k2k_karar_yon(oa); out["A"][kol][h] = oa
            gk = K[(K.kol == kol) & (K.hucre == h)]
            ob = gt_k2k_hucre_kir(gk[gk.durum == "TAMAM"], {k: int(v) for k, v in gk.durum.value_counts().items()}); ob["karar"] = gt_k2k_karar_kir(ob)
            out["B"][kol][h] = ob
    ana = GT_K2K["ana"]; em = GT_K2K["emare_hucre"]
    for tb in ("A", "B"):
        kk = [out[tb][ana][h]["karar"] for h in em]
        out[f"_karar_{tb}"] = {"ana_kol": ana, "hucre": dict(zip(em, kk)), "karar_hucre": {h: out[tb][ana][h]["karar"] for h in GT_K2K["hucre_karar"]},
                               "sonuc": "EMARE (yaşayan evren)" if all(k == "TUTAR" for k in kk) else "EMARE DEĞİL"}
    return out


def gt_k2k_olc_kos(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """k2kirolc: kapılar (GT6_ON_KAYIT.md commit + push, kontrol listesi, olay sha, kod / eşik sha ön kayıtta ve sayımla aynı, ikinci koşu yok) -> yön +
    kırılım sonrası -> satır dosyaları (k2/k2k_*.pkl) + gt6_ozet.json."""
    if os.path.exists(_gt_k2k_yol("ozet", cikti)):
        raise GTHata("gt6_ozet.json zaten var (ikinci koşu DURUR)")
    c_on = gt_kapi_commit(_gt_k2k_yol("onkayit", cikti), "GT6_ON_KAYIT.md")
    import IZ_KARNE as IK
    kk = IK.ik_kontrol_kapisi(_gt_k2k_yol("onkayit", cikti))
    SJ = json.load(open(_gt_k2k_yol("sayim", cikti), encoding="utf-8")); on = open(_gt_k2k_yol("onkayit", cikti), encoding="utf-8").read()
    if SJ["kod_sha"] != gt_kod_sha() or SJ["k2k_esik_sha"] != gt_k2k_esik_sha():
        raise GTHata("kod / eşik sha sayımdan sonra değişmiş (SAPMA)")
    for x in (gt_kod_sha(), gt_k2k_esik_sha(), GT_K2K["olay_sha"]):
        if x not in on:
            raise GTHata(f"ön kayıtta sha yazılı değil: {x[:12]}")
    OL, AD, sinir = _gt_k2k_girdi(cikti, ham)
    _GT_K2K_DURUM["kapi"] = True; _GT_K2_DURUM["kapi"] = True; bas = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    try:
        EVs, KPs, KKs, VV = [], [], [], {}
        for p in GT_K2_OLAY["pazar"]:
            Vd = MI.mi_veri(p, GT_YOL["acik"]); V = {s: d for s, d in Vd["V"].items() if len(d) >= 2}; P = gt_k2_evren(gt_yukle(p, ham))
            R = gt_k2k_pazar(p, OL, V, P, AD, olc=True); EVs.append(R["olay"]); KPs.append(R["kontrol"]); KKs.append(R["kontrol_kir"])
            VV[p] = {s: V[s] for s in set(OL[OL.pazar == p].sembol)}; del Vd, V, P; gc.collect()
        KP = pd.concat(KPs, ignore_index=True); KR = pd.concat(KKs, ignore_index=True)
        E = gt_k2k_taban1(pd.concat(EVs), KP); T2 = gt_k2k_taban2(KR); K = gt_k2k_kir_olay(E, VV, T2, sinir)
    finally:
        _GT_K2K_DURUM["kapi"] = False; _GT_K2_DURUM["kapi"] = False
    for ad, X in (("yon_pkl", E), ("kir_pkl", K), ("kon_pkl", KP[["pazar", "sembol", "L", "t", "donem", "kesik", "yon", "b"]]), ("konkir_pkl", KR)):
        with open(_gt_k2k_yol(ad, ham=ham), "wb") as f:
            pickle.dump(X, f, protocol=4)
    TB = gt_k2k_tablo(E, K)
    kon = {f"{p}|{dn}": {"k1_pencere_net": int(((KP.pazar == p) & (KP.donem == dn) & ~KP.kesik).sum()),
                         "k1_yukari_pay": float((KP[(KP.pazar == p) & (KP.donem == dn) & ~KP.kesik].yon == 1).mean()),
                         "k2_kirilim": int(((KR.pazar == p) & (KR.donem == dn)).sum()), "k2_kirilim_net": int(((KR.pazar == p) & (KR.donem == dn) & ~KR.kesik).sum())}
           for p in GT_K2_OLAY["pazar"] for dn in ("d1619", "d2022")}
    Z = {"baslik": GT_K2_BASLIK, "k7": GT_K2_K7, "baslangic_utc": bas, "onkayit_commit": c_on, "kontrol_kapisi": kk["gecti"], "kod_sha": gt_kod_sha(),
         "k2k_esik_sha": gt_k2k_esik_sha(), "olay_sha": GT_K2K["olay_sha"], "satir_sha": {ad: MI._mi_sha(_gt_k2k_yol(ad, ham=ham)) for ad in
                                                                                         ("yon_pkl", "kir_pkl", "kon_pkl", "konkir_pkl")},
         "kontrol": kon, "tablo": TB, "tablo_md": gt_k2k_tablo_md(TB)}
    MI._mi_jyaz(_gt_k2k_yol("ozet", cikti), Z, "gt6 özet")
    return Z


def gt_k2k_tablo_md(TB: Dict[str, Any]) -> str:
    def y(v: Any, n: int = 1) -> str:
        return "—" if v is None or (isinstance(v, float) and not np.isfinite(v)) else f"{100 * v:.{n}f}"

    def ga(b: Optional[Dict[str, Any]], n: int = 1) -> str:
        b = b or {}
        return f"{y(b.get('ort'), n)} [{y(b.get('alt'), n)}; {y(b.get('ust'), n)}]"
    L_ = [f"## {GT_K2_BASLIK}", "", GT_K2_K7, "", "### TABLO A — YÖN (Kontrol 1: aynı hisse-dönem-L, YER'i sağlamayan pencereler)", "",
          "| kol | hücre | bölge (kesik) | n tabanlı | yukarı / aşağı / kırılmadı % | taban yukarı / aşağı % | fark % [GA] | bar med. yukarı / aşağı | "
          "bilgi: kırılanda yukarı % / taban / fark [GA] | karar |", "|---|---|---|---|---|---|---|---|---|---|"]
    for kol in GT_K2_OLAY["kollar"]:
        for h, o in TB["A"][kol].items():
            L_.append(f"| {kol} | {h} | {o['bolge']} ({o['kesik']}) | {o['n']} | {y(o.get('yukari'))} / {y(o.get('asagi'))} / {y(o.get('kirilmadi'))} | "
                      f"{y(o.get('taban'))} / {y(o.get('taban_asagi'))} | {ga(o.get('fark'))} | {o.get('kbar_med_yukari', '—')} / "
                      f"{o.get('kbar_med_asagi', '—')} | {y((o.get('kosullu') or {}).get('pay'))} / {y((o.get('kosullu') or {}).get('taban'))} / "
                      f"{ga((o.get('kosullu') or {}).get('fark'))} | {o['karar']} |")
    L_ += ["", "### TABLO B — KIRILIM SONRASI (Kontrol 2: aynı hisse-dönemin sıradan tavan kırılımları; giriş b + 1 açılışı; 15 bar)", "",
           "| kol | hücre | n | TFk15 % [GA] | medyan fark % | +5 önce % / taban / fark [GA] | +10 önce % / taban | -5 önce % / taban | R15<-20 % / taban | "
           "R15>+20 % / taban | beşlik artı / büyük | R15-T1 % | karar |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for kol in GT_K2_OLAY["kollar"]:
        for h, o in TB["B"][kol].items():
            s5 = o.get("s5") or {}; s10 = o.get("s10") or {}
            L_.append(f"| {kol} | {h} | {o['n']} | {ga(o.get('TFk15'), 2)} | {y(o.get('medyan_fark'), 2)} | {y(s5.get('pay'))} / {y(s5.get('taban'))} / "
                      f"{ga(s5.get('fark'))} | {y(s10.get('pay'))} / {y(s10.get('taban'))} | {y(s5.get('pay_alt'))} / {y(s5.get('taban_alt'))} | "
                      f"{y(o.get('alt20'))} / {y(o.get('taban_alt20'))} | {y(o.get('ust20'))} / {y(o.get('taban_ust20'))} | {o.get('besli_arti', '—')} / "
                      f"{o.get('besli_buyuk', '—')} | {y(o.get('R15_T1'), 2)} | {o['karar']} |")
    L_ += ["", "ATRP20 beşlikleri içinde TFk15 % (n):", "", "| kol | hücre | B1 | B2 | B3 | B4 | B5 |", "|---|---|---|---|---|---|---|"]
    for kol in GT_K2_OLAY["kollar"]:
        for h, o in TB["B"][kol].items():
            if "besli" in o:
                L_.append(f"| {kol} | {h} | " + " | ".join(f"{y(v['TFk15'], 2)} ({v['n']})" for v in o["besli"].values()) + " |")
    for tb, ad in (("A", "YÖN"), ("B", "KIRILIM SONRASI")):
        k = TB[f"_karar_{tb}"]
        L_ += ["", f"KARAR {ad} (ANA kol {k['ana_kol']}; ABD iki dönem): " + "; ".join(f"{h} {v}" for h, v in k["hucre"].items()) + f" -> {k['sonuc']}; "
               "karar hücreleri: " + "; ".join(f"{h} {v}" for h, v in k["karar_hucre"].items())]
    return "\n".join(L_) + "\n"


def gt_sha_simdi() -> Dict[str, str]:
    return {"GT_KOD_SHA": gt_kod_sha(), "GT_ESIK_SHA": gt_esik_sha()}


def _cakisma_kontrol_gt(_once=_CK_ONCE_GT, _dosya="GOZ_TESPIT.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_GT",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_gt()


def _gt_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="GOZ_TESPIT")
    ap.add_argument("komut", choices=["olcu", "parmak", "dedektor", "onay", "rapor", "sha", "k2esles", "k2olay", "k2olc", "k2kirsay", "k2kirolc"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "olcu":
            print(json.dumps(MI._mi_json(gt_olcu_kos()), ensure_ascii=False, indent=1))
        elif a.komut == "parmak":
            J = gt_parmak_kos(); print(json.dumps(MI._mi_json({"imza": J["imza"], "yon": J["imza_yon"]}), ensure_ascii=False, indent=1))
        elif a.komut == "dedektor":
            D = gt_dedektor_kos(); print(json.dumps(MI._mi_json(D["pazar"]), ensure_ascii=False, indent=1)[:4000])
        elif a.komut == "onay":
            print(json.dumps(MI._mi_json(gt_onay()), ensure_ascii=False, indent=1)[:3000])
        elif a.komut == "rapor":
            print(json.dumps(MI._mi_json(gt_rapor()), ensure_ascii=False, indent=1)[:3000])
        elif a.komut == "sha":
            print(json.dumps(gt_sha_simdi(), indent=1))
        elif a.komut == "k2esles":
            print(json.dumps(MI._mi_json(gt_k2_goz2_esles()), ensure_ascii=False, indent=1))
        elif a.komut == "k2olay":
            J = gt_k2_olay_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("pazar", "sayim", "aday_sart", "olay_sha", "kod_sha")}), ensure_ascii=False, indent=1))
        elif a.komut == "k2olc":
            print(json.dumps(MI._mi_json(gt_k2_olc_kos()["karar"]), ensure_ascii=False, indent=1))
        elif a.komut == "k2kirsay":
            J = gt_k2k_sayim_kos(); print(json.dumps(MI._mi_json({k: J[k] for k in ("olay", "kod_sha", "k2k_esik_sha")}), ensure_ascii=False, indent=1)[:6000])
        elif a.komut == "k2kirolc":
            Z = gt_k2k_olc_kos(); print(Z["tablo_md"])
    except GTHata as ex:
        gtlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_gt_ana())
