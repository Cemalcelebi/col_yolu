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
def gt_sayfa(fig, d: pd.DataFrame, s: int, t: int, sayfa: int) -> Dict[str, Any]:
    """Geçmişli onay sayfası: üst uzak (önceki <= 120 bar + bölge), alt yakın (önceki 10 bar + bölge), üç kutu. Yalnız d[:t + 1] (assert); sonrası yok."""
    from matplotlib.patches import Rectangle
    G = HK.HK_ESIK_OLCEK; P = GT_ESIK["sayfa"]; s = int(s); t = int(t)
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
    return {"uzak_onceki_bar": int(nu), "yakin_onceki_bar": int(s - iy), "uzak": ou, "yakin": oy, "son_bar_index": int(t), "seri_uzunluk_kullanilan": int(len(dg))}


def gt_pdf(yol: str, sayfalar: List[Dict[str, Any]], seri: Any, kapak: Optional[str] = None) -> Dict[str, Any]:
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
                fig = plt.figure(figsize=boy); o = gt_sayfa(fig, d, r["s"], r["t"], r["sayfa"]); pdf.savefig(fig); plt.close(fig)
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

    def seri(p: str, sem: str, kaynak: str) -> pd.DataFrame:
        if (p, kaynak) not in Vc:
            Vc[(p, kaynak)] = MI.mi_veri(p, GT_YOL["tam_bist"] if kaynak == "tam" else GT_YOL["acik"])["V"]
            if kaynak == "acik":
                gt_kesik_kapi(Vc[(p, kaynak)], f"onay {p}")
        d = Vc[(p, kaynak)][sem]
        r = next(x for x in sec if x["pazar"] == p and x["sembol"] == sem)
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
    ap.add_argument("komut", choices=["olcu", "parmak", "dedektor", "onay", "rapor", "sha"])
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
    except GTHata as ex:
        gtlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_gt_ana())
