"""KART_TUR1 — KART TURU 1: en basit fiyat-hacim kartları, CETVEL2 v2.2 (R15 / R30 karar, R45 bilgi), KASA ile yürüyen ileri test
(21 Kasım 2026; iş tanımı arastirma_cikti/kart/KART_TUR1_IS_TANIMI.md bölüm 3, ADIM K2).

Cemal (21 Kas): "kartlar en basitten başlasın; ölçü 15 ve 30 mum ikisi olsun, yararı varsa 45 de olsun." ANA MODEL KARARI (ADIM K1,
CETVEL2_POZITIF_KONTROL_v2.2.md): KARAR ufukları R15 ve R30; R45 yalnız BİLGİ.

DÜZEN (aynı kod hem açık veride hem ileride açılmış bloklarla çalışır):
  python KART_TUR1.py olc --veri <klasör> --cikti <klasör> [--islem 4]
      <klasör> = KASA açık kısmı (/tmp/kasa/acik; içinde V_ABD / V_AVR / V_BIST / k34_yahoo .pkl ve KASA_DURUM.json). Kod klasörde ne varsa onu
      okur; açık kesik ve açılmış bloklar KASA_DURUM.json'dan, blok (çeyrek) sınırları tarihten türetilir. Önce KASA.kasa_kapisi (veri en geç
      tarihi <= açık kesik); kesik 2022-12-31'den sonraysa ön kayıt kapısı (KASA.ks_onkayit_kapi 'KART_TUR1' + bağımlı kod sha'ları) zorunlu.
      Hücreler: 'acik' (giriş 2016-01-01 .. 2022-12-31), açılmış her çeyrek ('2023Q1', ...; BİLGİ, plasebosuz) ve 'birikimli' (2023-01-01 ..
      açık kesik). KARAR BAKIŞI yalnız 4. blok (2023Q1-Q4) ve 8. blok (2023Q1-2024Q4) açıkken; öteki blok sayılarında tablo BİLGİ'dir.
  python KART_TUR1.py onkayit [--cikti arastirma_cikti/kart]      açık-veri çıktısından (acik/) ön kayıt metni (KART_TUR1_ON_KAYIT.md)
  python KART_TUR1.py regresyon --veri <açık klasör>                bayrak regresyonu: yalnız giriş <= 2022-12-30 satırlarında eski olay /
                                                                     özellik dosyalarıyla anahtar ve bayrak eşitliği (BİLGİ; olc'de KULLANILMAZ)
  python KART_TUR1.py sha                                           kod / eşik sha'ları
Kartların bayrakları YALNIZ açık fiyat verisinden, mevcut modül fonksiyonlarıyla yeniden hesaplanır (YAPI_HEDEF, GOZ_ETIKET, DUSUS_SONRASI,
BOFA_IZI, D9_YENIDEN, CETVEL2 / POZITIF_KONTROL); repo içindeki eski olay / özellik / sonuç dosyaları olc'de OKUNMAZ.
CETVEL2.py, YAPI_HEDEF.py, GOZ_ETIKET.py, DUSUS_SONRASI.py, BOFA_IZI.py, D9_YENIDEN.py, ORTAK_CETVEL.py, POZITIF_KONTROL.py, KASA.py
DEĞİŞTİRİLMEZ; içe alınır. Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
Colab: exec(open('KART_TUR1.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Test:  python test_kart_tur1.py (yalnız sentetik veri)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_KT = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

KOK_KT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_KT not in sys.path:
    sys.path.insert(0, KOK_KT)

import CETVEL2 as C2  # noqa: E402
import DUSUS_SONRASI as DS  # noqa: E402
import GOZ_ETIKET as GE  # noqa: E402
import KASA as KS  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import POZITIF_KONTROL as PK  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

ktlog = logging.getLogger("col.kart_tur1")
if not ktlog.handlers:
    _kt_h = logging.StreamHandler(sys.stderr)
    _kt_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kart_tur1: %(message)s", "%H:%M:%S"))
    ktlog.addHandler(_kt_h)
    ktlog.setLevel(logging.INFO)
    ktlog.propagate = False


class KTHata(RuntimeError):
    """Durdurucu hata: kasa / ön kayıt kapısı, veri yok, prefix tutmadı, sha tutmuyor, ikinci koşu, kesik aşımı."""


KT_SURUM = "KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test"
KT_HIPOTEZ = "KART_TUR1"
KT_YOL = {"cikti": os.path.join(KOK_KT, "arastirma_cikti", "kart"), "kod": os.path.join(KOK_KT, "KART_TUR1.py"),
          "onkayit": os.path.join(KOK_KT, "arastirma_cikti", "kart", "KART_TUR1_ON_KAYIT.md"),
          "is_tanimi": os.path.join(KOK_KT, "arastirma_cikti", "kart", "KART_TUR1_IS_TANIMI.md")}
KT_DOSYA = {"satir": "kt_satir.csv.gz", "hucre": "kt_hucre.csv", "karar": "kt_karar.csv", "huni": "kt_huni.json", "sonuc": "kt_sonuc.json",
            "prefix": "kt_prefix.json", "meta": "kt_meta.json", "rapor": "KART_TUR1_SONUC.md"}
KT_BAGIMLI = ["CETVEL2.py", "YAPI_HEDEF.py", "GOZ_ETIKET.py", "DUSUS_SONRASI.py", "BOFA_IZI.py", "D9_YENIDEN.py", "ORTAK_CETVEL.py",
              "POZITIF_KONTROL.py", "KASA.py", "S6_TABAN.py", "SIKISMA_YENIDEN.py", "sektor_ABD.csv", "evren_disi_ABD.csv",
              os.path.join("arastirma_cikti", "col_yolu_abd", "k34_evren.csv"),
              os.path.join("arastirma_cikti", "cetvel2", "cetvel2_esik_v2.2.json"), os.path.join("arastirma_cikti", "cetvel2", "cetvel2_guc_v2.2.json")]
KT_GRUP = ["MOM", "Y1", "DS", "BOFA", "D9"]
KT_PAZAR = ["ABD", "AVR", "BIST"]

# ================================================================ MÜHÜRLÜ KART SÖZLÜĞÜ (sha ön kayıtta; sonuç görüldükten sonra DEĞİŞMEZ)
_Y10 = YH.YH_ESIK["denemeler"]["Y10"]["esik"]
KT_KART: Dict[str, Dict[str, Any]] = {
    "KT00": {"grup": "MOM", "bayrak": "F_U", "yon": "+", "pazar": ["ABD", "AVR"], "karar": False,
             "cumle": "KONTROL KARTI: 12-1 momentum üst ondaki hisse (ay sonu, bütün evren) eşlerinden iyi. İz aramaz; kasada cetvelin bilinen "
                      "etkiyi görüp görmediğini sınar",
             "tanim": "ay sonu t, MOM = C(t-21) / C(t-252) - 1, OC havuzu sonrası aynı t kesitinde sıra: üst onda U (POZITIF_KONTROL.pk_b_sinyal_mom "
                      "+ pk_b_kur; ANA = U ya da A, aynı hissede >= 15 bar arayla ilk)",
             "esik": "üst onda (CETVEL2 v2.2 pozitif kontrol B1U ile AYNI tanım)", "kaynak": "CETVEL2.c2_mom22 -> POZITIF_KONTROL.pk_b_sinyal_mom, pk_b_kur"},
    "KT01": {"grup": "Y1", "bayrak": "F_KT01", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "S6 taban kırılımı (YAPI_HEDEF Y1 olayı) eşlerinden iyi",
             "tanim": "S6 'al' günü (S6_TABAN.s6_taban; hat = kutu_alt (AL) ya da DİP(t-1) (AL_BOLGESIZ), hat > 0) -> OC.oc_olay_hazirla (giriş, "
                      "havuz, 60 gün tekil) = Y1 OLAYI", "esik": "S6 parametreleri (S6.s6_prm) + OC_ESIK olay (tekil 60)",
             "kaynak": "YAPI_HEDEF.yh_sinyaller(['Y1']) -> yh_s6_hisse; ORTAK_CETVEL.oc_olay_hazirla"},
    "KT02": {"grup": "Y1", "bayrak": "F_KT02", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş1 DİPTE eşlerinden iyi", "tanim": "Y1 olayı VE F15 <= 0,25 VE F17 <= -0,20",
             "esik": f"F15_ust {_Y10['F15_ust']}, F17_ust {_Y10['F17_ust']} (YH_ESIK Y10 esik)", "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S1']; "
             "F15 / F17 GOZ_ETIKET.ge_ozellik_hisse"},
    "KT03": {"grup": "Y1", "bayrak": "F_KT03", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş3 DİP SAVUNULMUŞ eşlerinden iyi", "tanim": "Y1 olayı VE F2 >= -0,01 (son dokunuş dibi / ilk dokunuş dibi - 1; "
             "dokunuş yoksa NaN = tutmaz)", "esik": f"F2_min {_Y10['F2_min']}", "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S3']; F2 GOZ_ETIKET"},
    "KT04": {"grup": "Y1", "bayrak": "F_KT04", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş5 ALT FİTİL AZ eşlerinden iyi", "tanim": "Y1 olayı VE F4 <= 0,25 (bölge medyan alt fitil payı)",
             "esik": f"F4_ust {_Y10['F4_ust']}", "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S5']; F4 GOZ_ETIKET"},
    "KT05": {"grup": "Y1", "bayrak": "F_KT05", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş4 KÜÇÜK MUM eşlerinden iyi", "tanim": "Y1 olayı VE F3 <= 0,90 (bölge medyan mum boyu / ATR250)",
             "esik": f"F3_ust {_Y10['F3_ust']}", "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S4']; F3 GOZ_ETIKET"},
    "KT06": {"grup": "Y1", "bayrak": "F_KT06", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş7 GÖVDELİ YAKIN TAVAN KIRILIMI eşlerinden iyi",
             "tanim": "Y1 olayı VE F22 = C_t / F21 - 1 > 0 VE F22a = O_t / F21 - 1 < 0 VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (F21 = max "
                      "High[t-15 .. t-1])", "esik": f"F22 > {_Y10['F22_alt_acik']}, F22a < {_Y10['F22a_ust_acik']}, F23_min {_Y10['F23_min']}",
             "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S7']; F20-F23 YAPI_HEDEF.yh_s7_ozellik"},
    "KT07": {"grup": "Y1", "bayrak": "F_KT07", "yon": "+", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Cemal'in son dersi: Y1 ∧ Ş1 ∧ Ş3 ∧ Ş5 (dip + savunma + alt fitil az) eşlerinden iyi",
             "tanim": "Y1 olayı VE Ş1 VE Ş3 VE Ş5 (eşikler KT02 / KT03 / KT04 ile aynı)", "esik": "KT02 + KT03 + KT04",
             "kaynak": "YAPI_HEDEF.yh_s7_sartlar['S1'] & ['S3'] & ['S5']"},
    "KT08": {"grup": "DS", "bayrak": "F_KT08", "yon": "-", "pazar": KT_PAZAR, "karar": True,
             "cumle": "Düşen bıçak (kural defteri K50 / KAZANANLAR H2): düşüş sonrası dipte, 120 günün tam dibine son 5 günde düşerek gelen hisse "
                      "eşlerinden kötü",
             "tanim": "DS ANA olayı (DUSUS_SONRASI: C_t / max C son 120 - 1 <= -0,30, F15 <= 0,25, likidite, ABD C >= 2 $; OC giriş / havuz; ANA "
                      "15 bar tekil) VE F15_t <= 0,05 VE r5 = C_t / C_t-5 - 1 <= -0,03 (geçerli barlar; arastirma_cikti/canli/kazananlar.kz_ozellik "
                      "tanımı)", "esik": "F15 <= 0,05; r5 <= -0,03 (K50 kaydı, KURAL_DEFTERI_TASLAK.md; KAZANANLAR_2026-10-22 H2)",
             "kaynak": "DUSUS_SONRASI.ds_ozellik_pazar + ds_olay_kur (ana); F15 / r5 = kazananlar.kz_ozellik formülü (testte birebir)"},
    "KT09": {"grup": "BOFA", "bayrak": "F_KT09", "yon": "+", "pazar": ["ABD", "AVR"], "karar": True,
             "cumle": "−%80 dip kurulumu (Ç173b): tepeden >= %80 düşmüş, son 10 günde yeni dip yapmamış, dipten <= 1,5 kat uzaktaki hisse "
                      "eşlerinden iyi",
             "tanim": "D1 C_t / max(C[t-250 .. t-1]) - 1 <= -0,80 (en az 200 bar, veri kırığından sonra) VE D2 min(C[t-9 .. t]) > min(C[t-59 .. "
                      "t-10]) VE D3 C_t <= 1,50 x min(C[t-59 .. t-10]); aynı hissede ilk kurulum günü, sonraki >= 60 bar sonra",
             "esik": "BOFA_IZI.DP_ESIK['kurulum'] (dusus -0,80, tepe 250 / 200, dip 60 / 10, dipten 1,50, ayri 60, kırık ABD / AVR [-0,6667, 2,0])",
             "kaynak": "BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum (Ç173 'dosya' BOFA_IZI.py diponkayit / dipkos); BIST verisi Yahoo önbelleği "
                       "(TAVAN_SERISI) kasada yok -> BIST VERİ YOK"},
    "KT10": {"grup": "D9", "bayrak": "F_KT10", "yon": "+", "pazar": ["ABD"], "karar": True,
             "cumle": "Sektör rüzgârı ABD (Ç181c): alt sektörü piyasadan >= 10 puan iyi giden (rüzgârlı) ve uzun çölde OLMAYAN hisse eşlerinden iyi",
             "tanim": "RÜZGÂR VE D9 DEĞİL (D9_YENIDEN.d9_satir 'c'): ruz = sepet (alt sektörün öteki >= 4 üyesi, 60 bar getiri eşit ağırlık) - "
                      "piyasa (taze hisselerin 60 bar getiri medyanı) >= 0,10 VE sepet > 0; D9 uzun çöl değil; durum günleri (sektör ABD "
                      "'endustri', sektor_ABD.csv)",
             "esik": "D9_YENIDEN.D9_PARAM (RUZ_GERI 60, RUZ_ESIK 0,10, RUZ_MIN_UYE 4, RUZ_MUTLAK 0, RUZ_BAYAT 5; UZUN_W 250, UZUN_BANT 1,50, "
                     "UZUN_MUM 0,04, UZUN_KONUM 0,5)",
             "kaynak": "D9_YENIDEN.d9_durum + d9_satir('c') (Ç181 'dosya' D9_YENIDEN.py); AVR sektör listesi yok -> AVRUPA VERİSİ YOK, karar en "
                       "fazla ABD-ADAY (CLAUDE.md olay ölçüleri kuralı)"},
}

KT_ESIK: Dict[str, Any] = {
    "surum": "KT1.0",
    "cetvel": "CETVEL2 v2.2 (C2.c2_olc22; C2_ESIK22 sha ön kayıtta): R_H = H. geçerli bar kapanışı / t+1 açılış - 1 (stop yok), konum eşli "
              "fark (aynı giriş günü, aynı pazar, aynı ATRP x likidite x F15 kovası, bütün evren, aynı kartın o günkü olayları ve olayın "
              "kendisi eş dışı, en az 5 eş), tekil H, ay kümeli boot (B 2000), ay kümeli işaret permütasyonu (R 10000), L3O, güç eğrisi "
              "(cetvel2_guc_v2.2.json; hücre adı eğride yoksa 'acik'), plasebo kapısı 200 tohum (|ort FARK| < 0,005 VE TUTAR payı <= %7, "
              "hipotez yönünde)",
    "kartlar": {k: {kk: vv for kk, vv in v.items()} for k, v in KT_KART.items()},
    "ufuk": {"karar": [15, 30], "bilgi": [45], "plasebo": [15, 30],
             "not": "ADIM K1 ana model kararı: R45 kuralı tutmadı (plasebo AVR 2020-22 %15, momentum R45'te de 0'dan ayrışmıyor) -> R45 BİLGİ, "
                    "plasebosuz"},
    "hucre": {"acik": ["2016-01-01", "2022-12-31"], "blok_bas": "2023-01-01",
              "tanim": "hücre = pazar x giriş günü aralığı: 'acik' (2016-22, bilinen veri), açılmış her takvim çeyreği ('2023Q1' ...; BİLGİ, "
                       "plasebosuz, permütasyonsuz) ve 'birikimli' (2023-01-01 .. açık kesik; plaseboyla). Fon krizi kesiği 31.08.2026 (OC); "
                       "H. barı veri sonunu aşan olay ölçülmez, 'bekleyen' sayısı yazılır (sonraki blok açılınca ölçülür)"},
    "bakis": {"4": "BAKIŞ 1: 2023Q1-2023Q4 birikimli", "8": "BAKIŞ 2: 2023Q1-2024Q4 birikimli",
              "tanim": "KARAR BAKIŞI yalnız açılmış blok sayısı 4 ve 8 iken (KASA_DURUM 'acilan' sırası 2023Q1'den kesintisiz); öteki blok "
                       "sayılarında birikimli tablo BİLGİ (boot %95, BH q 0,10); 8'den sonra karar yok (bilgi)"},
    "bonferroni": {"boot_alt": 0.0125, "boot_ust": 0.9875, "bh_q": 0.05,
                   "tanim": "iki bakış için Bonferroni: bakış hücrelerinde boot aralığı %97,5 (alt 0,0125 / üst 0,9875 yüzdelik; aynı ay kümeli "
                            "boot, B 2000) ve BH q 0,10 / 2 = 0,05"},
    "bh": {"q": 0.10, "m": 20,
           "tanim": "aile = karar kartları (KT01-KT10; KT00 hariç) x karar ufku (15, 30) = 10 x 2 = 20 p; kart x ufuk p = karar pazarlarının "
                    "birikimli hücrelerinde en büyük ay kümeli permütasyon p (beklenen yönde; ters yön etiketi için ters yön p'si ayrı BH)"},
    "karar_kurali": (
        "Karar hücresi c(k, H, P) = kart k, karar ufku H in {15, 30}, karar pazarı P in {ABD, AVR} (KT10: yalnız ABD), birikimli hücre. "
        "GÜÇLÜ(c) = n >= 30 VE güç >= 0,80; KAPI(c) = plasebo kapısı geçti. T+(c) = GÜÇLÜ VE KAPI VE FARK > 0 VE boot alt > 0 VE SIRA > 0,50 "
        "VE L3O > 0; T-(c) = GÜÇLÜ VE KAPI VE FARK < 0 VE boot üst < 0 VE SIRA < 0,50 VE L3O(-) < 0 (boot bakışta %97,5). Yönü '+' olan kartta "
        "TUTAR = T+, TERS = T-; '-' kartta TUTAR = T-, TERS = T+. KART TUTAR <=> bir H1 karar ufkunda bütün karar pazarlarında TUTAR(c(k, H1, P)) "
        "VE öteki karar ufkunda (H2) bütün karar pazarlarında birikimli FARK beklenen işaretli VE açık veri (2016-22) hücresinde (H1) bütün karar "
        "pazarlarında FARK beklenen işaretli VE (k, H1) BH geçti (bakışta q 0,05, m 20). KATKI− <=> aynı şartlar ters yönde (TERS, ters "
        "işaretler, ters p ile BH). İkisi de değilse: bir karar hücresinde (iki ufuk, karar pazarları) GÜÇLÜ değil ya da KAPI düşmüşse "
        "ÖLÇÜLEMEDİ (neden yazılır); aksi 'İZ DEĞİL (bu ufuklarda, güç eğrisindeki en küçük yakalanır etki için)'. KT10 (AVR verisi yok): "
        "TUTAR -> 'ABD-ADAY', KATKI− -> 'ABD-ADAY (−)'. KONTROL KARTI KT00 (BH dışı): GÖRDÜ = bir karar ufkunda ABD ve AVR birikimli T+; "
        "KISMEN = bir karar ufkunda ABD ve AVR birikimli FARK > 0; aksi GÖRMEDİ. KT00 GÖRMEDİ ise tur 'cetvel / ufuk yetersiz' diye raporlanır "
        "ve 'İZ DEĞİL' etiketleri 'ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)' olur. Bakış dışı bloklarda aynı hesap BİLGİ (boot %95, "
        "BH q 0,10)."),
    "prefix": {"n": 8, "tohum": 2251, "rtol": 1e-9,
               "tanim": "kart grubu x pazar başına 8 rastgele olay: veri t'de kesilince bayrak girdileri aynı (Y1: S6 sinyali + F1-F18 + F20-F23; MOM: "
                        "o günün bütün MOM değerleri; DS: DS durumu + F15 + r5; BOFA: kurulum; D9: D9_YENIDEN.d9_gelecek_denetimi). Tutmazsa DURUR"},
    "tohum": {"MOM": 100, "Y1": 101, "DS": 108, "BOFA": 109, "D9": 110, "ceyrek": 2261, "bakis_boot": 2271},
    "yuvarlama": "Y1 özellikleri (F1-F23) eşik karşılaştırmasından önce 6 anlamlı basamağa yuvarlanır (ozellik_Y1*.csv.gz '%.6g' biçimi; "
                 "YAPI_HEDEF 4. tur bayrakları bu değerlerle kuruldu)",
    "veri": "yalnız --veri klasörü (KASA açık kısmı): V_ABD / V_AVR / V_BIST (+ ABD için k34_yahoo); Y1 tabanı OC.oc_veri k34'SÜZ (orijinal YAPI_HEDEF "
            "Y1 evreni; açık veride olay kümesi olay_Y1 ile birebir), D9 (KT10) OC.oc_veri k34 DAHİL (orijinal D9_YENIDEN evreni); cetvel paneli CETVEL2 (DS.ds_veri, k34 yok); BOFA BOFA_IZI.dp_pkl_fiyat",
}

KT_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = CETVEL2 v2.2 c2_es: aynı giriş günü, aynı pazar, aynı ATRP x likidite x F15 kovası, bütün evren, aynı geometri (R_H "
                   "stop'suz); kartın o günkü olayları ve olayın kendisi eş dışı; plasebo kapısı 200 tohum aynı gün rastgele hisse (c2_plasebo); "
                   "KT00 momentum kontrol kartı cetvelin bilinen etkiyi gördüğünü sınar; mekanik üstünlük yok (stop / hedef yok)"),
    "K2": ("EVET", "bayraklar yalnız t ve öncesi barlarla; kt_prefix her grup x pazarda 8 olayda veri t'de kesilince aynı (kt_prefix.json; "
                   "tutmazsa DURUR); KASA.kasa_kapisi veri en geç tarihi <= açık kesik; çıktı en geç tarihleri kt_meta.json; eski olay / özellik "
                   "dosyaları olc'de okunmaz; evren / sektör listesi bugünkü (K7 / sınır)"),
    "K3": ("EVET", "OC.oc_veri_hazirla + YH._yh_hazir (H > L, V > 0, fiyat > 0); sinyal günü geçersiz bar ise olay düşer (oc_olay_hazirla); R_H "
                   "yalnız geçerli barlar"),
    "K4": ("EVET", "Y1 60 gün tekil (OC), DS ANA 15 bar tekil, BOFA 60 bar ayrı olay, MOM 15 bar ANA; cetvel tekil H (15 / 30 / 45); n = "
                   "ölçülen olay; boot / permütasyon birimi giriş ayı; medyan FARK hücre tablosunda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla; R_H paydası); eşler aynı gün açılışı"),
    "K6": ("EVET", "V_*.pkl tek kip (fi_k1_veri düzeltilmiş; KASA bayt bayt bölünmüş); oranlar birimsiz; likidite günlük kesit sırası (AVR x "
                   "Kur); BOFA veri kırığı kuralı (ABD / AVR 1/3 - 3 kat) aynen; geçmiş bölünme şüphesi havuz dışı (OC)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (KT10 rüzgâr hesabında + ABD k34 nakdi biten, kesikten önce doğanlar); batan yok; dipteki kartlarda "
                   "(KT02, KT07, KT08, KT09) yanlılık daha büyük; raporda yazılı"),
    "K8": ("EVET", "hücre başına n >= 30 ve güç >= 0,80 yoksa ÖLÇÜLEMEDİ; güç tablosu (4 / 8 blokta beklenen n) ön kayıtta; iki karar ufku + "
                   "iki karar pazarı + açık veri işareti; BH q 0,10 (bakışta 0,05) m 20; iki bakış Bonferroni"),
    "K9": ("EVET", "KART_TUR1_ON_KAYIT.md: KT_KART / KT_ESIK sha, KART_TUR1.py ve CETVEL2.py KASA_KOD sha'sı, bağımlı kod sha tablosu, karar "
                   "kuralı, bakış takvimi, güç tablosu; sıra kod commit -> açık kuru koşu -> ön kayıt commit -> (ana model) blok aç -> olc; "
                   "olc kesik > 2022-12-31 iken KASA.ks_onkayit_kapi + bağımlı sha denetimi"),
    "K10": ("UYGULANMAZ", "ham haber / KAP / SEC ayrıştırması yok; yalnız OHLCV + sektor_ABD.csv; eski olay dosyaları yalnız 'regresyon' "
                          "komutunda (giriş <= 2022-12-30 satırları) karşılaştırma için okunur"),
    "K11": ("EVET", "kt_yeniden: iki hücre (KT01 ABD acik R15, KT08 AVR acik R30) satır dosyasından düz pandas ile n / ort FARK / ort SIRA; "
                    "kt_satir.csv.gz'den bağımsız yeniden üretim; tutmazsa DURUR"),
    "K12": ("EVET", "etiketler yalnız karar kuralıyla; açık veri sonuçları 'bilinen veri' diye ayrı; sayı ve yorum ayrı cümle; 'iz' sözü yalnız "
                    "kural geçerse"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_kt (test); defter / üretim / yasak modüllere dokunulmadı (bağımlı sha tablosu); e-posta / "
                    "anahtar taraması (_kt_yaz); dış servis / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; kart ölçümü"),
}


# ================================================================ 0) ORTAK
def _kt_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _kt_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def kt_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(KT_ESIK if E is None else E)


def _kt_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _kt_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_kt_json(v) for v in o]
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if np.isfinite(v) else None
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(o.date()) if isinstance(o, pd.Timestamp) else str(o)
    if isinstance(o, np.ndarray):
        return [_kt_json(v) for v in o.tolist()]
    return o


_KT_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_KT_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|şifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")


def _kt_yaz(yol: str, metin: str) -> None:
    """Atomik yaz + e-posta / anahtar sızıntı taraması (K13)."""
    if [m for m in _KT_EPOSTA.findall(metin) if m != "noreply@anthropic.com"]:
        raise KTHata(f"{yol}: metinde e-posta biçimli dizi var -> yazılmadı")
    if _KT_ANAHTAR.search(metin):
        raise KTHata(f"{yol}: metinde anahtar biçimli dizi var -> yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    tmp = yol + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(tmp, yol)


def _kt_git(yol: str) -> str:
    try:
        return subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_KT, capture_output=True, text=True,
                              check=True).stdout.strip() or "-"
    except (OSError, subprocess.CalledProcessError):
        return "-"


def kt_bagimli_sha() -> Dict[str, str]:
    out = {}
    for y in KT_BAGIMLI:
        t = os.path.join(KOK_KT, y)
        out[y] = _kt_sha(t) if os.path.exists(t) else "-"
    return out


def kt_sha_simdi() -> Dict[str, Any]:
    E = {"KART_TUR1.py": _kt_sha(KT_YOL["kod"]), "KT_ESIK_SHA": kt_esik_sha(), "KT_KART_SHA": YH.yh_esik_sha(KT_KART),
         "C2_ESIK22_SHA": C2.c2_esik22_sha(), "C2_ESIK_SHA": C2.c2_esik_sha(), "YH_Y10_ESIK_SHA": YH.yh_esik_sha(_Y10),
         "GE_OZELLIK_SHA": YH.yh_esik_sha(GE.GE_ESIK["ozellik"]), "DS_OLAY_SHA": YH.yh_esik_sha(DS.DS_ESIK["olay"])}
    import BOFA_IZI as BI
    import D9_YENIDEN as D9
    E["DP_KURULUM_SHA"] = YH.yh_esik_sha(BI.DP_ESIK["kurulum"]); E["D9_PARAM_SHA"] = YH.yh_esik_sha(D9.D9_PARAM)
    E["OC_ESIK_SHA"] = YH.yh_esik_sha(OC.OC_ESIK)
    return {"esik": E, "bagimli": kt_bagimli_sha()}


def _kt_havuz(f: Callable, isler: List[Any], islem: int) -> List[Any]:
    if islem > 1 and len(isler) > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(min(islem, len(isler))) as hv:
            return hv.map(f, isler)
    return [f(x) for x in isler]


def _r6(x: np.ndarray) -> np.ndarray:
    """6 anlamlı basamak ('%.6g' csv biçimi)."""
    return np.array([float(f"{v:.6g}") if np.isfinite(v) else np.nan for v in np.asarray(x, float)])


# ================================================================ 1) KASA, DURUM, BLOKLAR
def kt_ceyrek(t: Any) -> str:
    t = pd.Timestamp(t)
    return f"{t.year}Q{(t.month - 1) // 3 + 1}"


def kt_bloklar_beklenen(n: int) -> List[str]:
    out, y, q = [], 2023, 1
    for _ in range(n):
        out.append(f"{y}Q{q}"); q += 1
        if q > 4:
            q = 1; y += 1
    return out


def kt_durum(veri: str) -> Dict[str, Any]:
    """--veri klasöründeki KASA_DURUM.json: açık kesik, açılmış bloklar (2023Q1'den kesintisiz sıra), bakış no."""
    yol = os.path.join(veri, KS.KS_DURUM_AD)
    if not os.path.exists(yol):
        raise KTHata(f"KASA durum dosyası yok: {yol} (yalnız KASA açık kısmı okunur)")
    D = json.load(open(yol, encoding="utf-8"))
    kes = pd.Timestamp(D["acik_kesik"]); ac = list(D.get("acilan", []))
    if ac != kt_bloklar_beklenen(len(ac)):
        raise KTHata(f"açılmış bloklar 2023Q1'den kesintisiz değil: {ac}")
    if not ac and kes != pd.Timestamp(KT_ESIK["hucre"]["acik"][1]):
        raise KTHata(f"blok açılmamış ama açık kesik {kes.date()} != {KT_ESIK['hucre']['acik'][1]}")
    if ac:
        son = pd.Period(ac[-1].replace("Q", "Q"), freq="Q")
        if not (son.start_time.normalize() <= kes <= son.end_time.normalize()):
            raise KTHata(f"açık kesik {kes.date()} son açılmış blok {ac[-1]} içinde değil")
    nb = len(ac)
    bk = KT_ESIK["bakis"].get(str(nb))
    return {"kesik": kes, "acilan": ac, "blok_sayi": nb, "bakis": bk, "bakis_no": (1 if nb == 4 else 2 if nb == 8 else 0),
            "muhur_id": D.get("muhur_id"), "durum_sha": _kt_sha(yol)}


def kt_k34_yok() -> str:
    """k34 yüklenmeyen veri2 yolu (DUSUS_SONRASI kuralı); klasörde k34 varsa DURUR (yanlışlıkla okunmasın)."""
    y = DS.DS_YOL["veri2_yok"]
    if os.path.exists(os.path.join(y, "k34_yahoo.pkl")):
        raise KTHata(f"{y} içinde k34_yahoo.pkl var: Y1 evreni k34'süz olmalı -> DURDU")
    return y


def kt_veri_dosyalari(veri: str) -> List[str]:
    yy = [os.path.join(veri, f"V_{p}.pkl") for p in KT_PAZAR] + [os.path.join(veri, "k34_yahoo.pkl")]
    eks = [y for y in yy if not os.path.exists(y)]
    if eks:
        raise KTHata(f"veri dosyası yok: {eks} (yalnız KASA açık kısmı; indirme / worktree YASAK)")
    return yy


def kt_kasa(veri: str, D: Dict[str, Any]) -> Dict[str, Any]:
    """KASA.kasa_kapisi: bütün veri dosyalarının en geç tarihi <= açık kesik (KASA_DURUM)."""
    try:
        return KS.kasa_kapisi(kt_veri_dosyalari(veri), kesik=D["kesik"])
    except KS.KasaHata as ex:
        raise KTHata(f"KASA kapısı KAPALI: {ex}") from ex


def kt_hucreler(D: Dict[str, Any]) -> Dict[str, List[str]]:
    """c2_olc22 donem sözlüğü: 'acik' + (blok varsa) 'birikimli'. Çeyrekler ayrıca (kt_ceyrek_hucre)."""
    Dn = {"acik": list(KT_ESIK["hucre"]["acik"])}
    if D["blok_sayi"]:
        Dn["birikimli"] = [KT_ESIK["hucre"]["blok_bas"], str(D["kesik"].date())]
    return Dn


def kt_onkayit_kapisi(onkayit: str) -> Dict[str, Any]:
    """Blok açıkken: KASA.ks_onkayit_kapi (git'e işlenmiş, değişmemiş, KASA_HIPOTEZ KART_TUR1, KASA_KOD sha'ları, kontrol tablosu) + bağımlı
    kod / eşik dosyası sha'ları ön kayıttakiyle aynı."""
    try:
        G = KS.ks_onkayit_kapi(onkayit, KT_HIPOTEZ, kontrol=True)
    except KS.KasaHata as ex:
        raise KTHata(f"ön kayıt kapısı KAPALI: {ex}") from ex
    metin = open(onkayit, encoding="utf-8").read()
    kayit = dict(re.findall(r"^\s*BAGIMLI_SHA:\s*(\S+)\s+([0-9a-f]{64}|-)\s*$", metin, flags=re.M))
    if not kayit:
        raise KTHata("ön kayıtta BAGIMLI_SHA satırı yok")
    simdi = kt_bagimli_sha(); fark = [k for k, v in kayit.items() if simdi.get(k) != v]
    if fark:
        raise KTHata(f"bağımlı dosya ön kayıttan sonra değişmiş: {fark} -> DURDU (sonuç bu kodla üretilmez)")
    es = re.findall(r"^\s*KT_ESIK_SHA:\s*([0-9a-f]{64})\s*$", metin, flags=re.M)
    if es != [kt_esik_sha()]:
        raise KTHata("KT_ESIK sha ön kayıttakiyle aynı değil -> DURDU")
    G["bagimli"] = len(kayit)
    return G


# ================================================================ 2) OLAY KÜMELERİ VE BAYRAKLAR (yalnız açık fiyat verisinden)
_KT_IS: Dict[str, Any] = {}


def _kt_y1_isci(semboller: List[Tuple[str, List[pd.Timestamp], List[float], List[float]]]) -> List[Dict[str, Any]]:
    V = _KT_IS["V"]; out = []
    for s, tl, hl, tvl in semboller:
        try:
            d = GE.ge_hazir(V[s])
            Fs, Bs = GE.ge_ozellik_hisse(d, tl, hazir=True)
            S7 = YH.yh_s7_ozellik(d, tl, hazir=True)
            for k, (t, f, b, h0, tv0) in enumerate(zip(tl, Fs, Bs, hl, tvl)):
                ok = bool(abs(b["hat"] / h0 - 1) <= 1e-9 and (abs(b["tavan"] / tv0 - 1) <= 1e-9 if np.isfinite(tv0) else not np.isfinite(b["tavan"])))
                out.append({"sembol": s, "tarih": t, **f, **S7.iloc[k].to_dict(), "_ok": ok, "_hata": ""})
        except Exception as ex:   # tek hisse bozuksa sayılır; sonda DURUR
            for t in tl:
                out.append({"sembol": s, "tarih": t, "_ok": False, "_hata": f"{type(ex).__name__}: {str(ex)[:160]}"})
    return out


def kt_y1(Vo: Dict[str, Any], Po: Dict[str, Any], pazar: str, islem: int = 1) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Y1 olayları (S6 'al' -> OC 60 gün tekil) + F1-F18 (GOZ_ETIKET) + F20-F23 (YAPI_HEDEF S7) -> Ş1 / Ş3 / Ş4 / Ş5 / Ş7 bayrakları."""
    t0 = time.time()
    S1 = YH.yh_sinyaller(Vo, pazar, ["Y1"], islem)["Y1"].copy()
    S1["tarih"] = pd.to_datetime(S1.tarih); S1["sembol"] = S1.sembol.astype(str)
    Z, say = OC.oc_olay_hazirla(S1[["sembol", "tarih", "pazar"]], Po)
    Z = Z.merge(S1[["sembol", "tarih", "hat", "tavan"]], on=["sembol", "tarih"], how="left", validate="one_to_one")
    isler = [(s, list(pd.to_datetime(g.tarih)), list(g.hat.astype(float)), list(g.tavan.astype(float))) for s, g in Z.groupby("sembol", sort=True)]
    k = max(1, islem * 4); dilim = [isler[j::k] for j in range(k) if isler[j::k]]
    _KT_IS["V"] = Vo["V"]
    try:
        R = _kt_havuz(_kt_y1_isci, dilim, islem)
    finally:
        _KT_IS.clear()
    F = pd.DataFrame([y for r in R for y in r])
    if len(F):
        hata = F[F["_hata"].astype(str) != ""]
        if len(hata):
            raise KTHata(f"Y1 {pazar}: {len(hata)} olayda özellik hesaplanamadı (ör. {hata.sembol.iat[0]}: {hata['_hata'].iat[0]})")
        if not F["_ok"].all():
            raise KTHata(f"Y1 {pazar}: {int((~F['_ok']).sum())} olayda hat / tavan sinyalle aynı değil -> DURDU")
    kol = list(YH._Y10_OZ)
    X = Z[["sembol", "tarih"]].merge(F[["sembol", "tarih"] + kol], on=["sembol", "tarih"], how="left", validate="one_to_one") if len(F) else \
        Z[["sembol", "tarih"]].assign(**{c: np.nan for c in kol})
    for c in kol:
        X[c] = _r6(X[c].to_numpy(float))
    S = YH.yh_s7_sartlar(X) if len(X) else {k_: np.zeros(0, bool) for k_ in ("S1", "S3", "S4", "S5", "S7")}
    X["F_KT01"] = 1.0
    for kod, m in (("F_KT02", S["S1"]), ("F_KT03", S["S3"]), ("F_KT04", S["S5"]), ("F_KT05", S["S4"]), ("F_KT06", S["S7"]),
                   ("F_KT07", S["S1"] & S["S3"] & S["S5"])):
        X[kod] = np.asarray(m, bool).astype(float)
    X.insert(0, "pazar", pazar)
    say = {"sinyal": int(len(S1)), **{k_: int(v) for k_, v in say.items()}, "y1_olay": int(len(X)),
           **{c: int(X[c].sum()) for c in ("F_KT02", "F_KT03", "F_KT04", "F_KT05", "F_KT06", "F_KT07")}, "sure_sn": round(time.time() - t0, 1)}
    ktlog.info("Y1 %s: %d sinyal, %d olay (%.0f sn)", pazar, len(S1), len(X), time.time() - t0)
    return X.sort_values(["sembol", "tarih"]).reset_index(drop=True), {"S1": S1, "say": say}


def kt_mom(pazar: str, veri: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    O, sy = C2.c2_mom22(pazar, veri)
    O = O.copy(); O.insert(0, "pazar", pazar)
    return O, sy


def kt_f15_r5(d: pd.DataFrame, tarihler: List[pd.Timestamp]) -> Tuple[np.ndarray, np.ndarray]:
    """kazananlar.kz_ozellik F15 / r5 formülü (YH._yh_hazir barları; t dahil son 120 kapanış; r5 = C_t / C_t-5 - 1)."""
    C = d.Close.to_numpy(float); pos = d.index.get_indexer(pd.DatetimeIndex(tarihler))
    if (pos < 0).any():
        raise KTHata("F15 / r5: olay günü geçerli bar değil")
    f15 = np.full(len(pos), np.nan); r5 = np.full(len(pos), np.nan)
    for q, i in enumerate(pos):
        c = C[max(0, i - 119):i + 1]
        if len(c) == 120 and c.max() > c.min():
            f15[q] = (C[i] - c.min()) / (c.max() - c.min())
        if i >= 5:
            r5[q] = C[i] / C[i - 5] - 1
    return f15, r5


def kt_ds(Pb: Dict[str, Any], pazar: str, islem: int = 1) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """DS ANA olayları (DUSUS_SONRASI.ds_ozellik_pazar + ds_olay_kur) + KT08 bayrağı (F15 <= 0,05 VE r5 <= -0,03)."""
    t0 = time.time(); Vd, P = Pb["Vd"], Pb["P"]
    bag = DS.ds_baglam(Vd)
    Z = DS.ds_ozellik_pazar(Vd, bag, None, islem)
    X, say = DS.ds_olay_kur(Z, P)
    A = X[X.ana][["sembol", "tarih"]].copy(); A["tarih"] = pd.to_datetime(A.tarih)
    f15 = np.full(len(A), np.nan); r5 = np.full(len(A), np.nan)
    for s, g in A.groupby("sembol", sort=True):
        a, b = kt_f15_r5(YH._yh_hazir(Vd["V"][s]), list(g.tarih))
        f15[A.index.get_indexer(g.index)] = a; r5[A.index.get_indexer(g.index)] = b
    A["f15"] = f15; A["r5"] = r5
    with np.errstate(invalid="ignore"):
        A["F_KT08"] = ((A.f15.to_numpy(float) <= 0.05) & (A.r5.to_numpy(float) <= -0.03)).astype(float)
    A.insert(0, "pazar", pazar)
    sy = {k: int(v) for k, v in say.items()}; sy.update({"ana": int(len(A)), "F_KT08": int(A.F_KT08.sum()), "sure_sn": round(time.time() - t0, 1)})
    ktlog.info("DS %s: %d ANA, KT08 %d (%.0f sn)", pazar, len(A), int(A.F_KT08.sum()), time.time() - t0)
    return A.sort_values(["sembol", "tarih"]).reset_index(drop=True), {"say": sy, "Vd": Vd, "bag": bag}


def kt_bofa(pazar: str, veri: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    import BOFA_IZI as BI
    V, info = BI.dp_pkl_fiyat(os.path.join(veri, f"V_{pazar}.pkl"), pazar)
    X, _ = BI.dp_kurulum_tum(V, pazar)
    O = pd.DataFrame({"pazar": pazar, "sembol": X.sembol.astype(str), "tarih": pd.to_datetime(X.kurulum_gunu), "F_KT09": 1.0})
    return O.sort_values(["sembol", "tarih"]).reset_index(drop=True), {"say": {"hisse": int(info["hisse"]), "kurulum": int(len(O)),
                                                                               "son": info.get("son")}, "V": V}


def kt_d9(Vo: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    import D9_YENIDEN as D9
    t0 = time.time()
    Dd = D9.d9_durum(Vo, "ABD")
    Xc = D9.d9_satir(Dd, "c")
    O = pd.DataFrame({"pazar": "ABD", "sembol": Xc.sembol.astype(str), "tarih": pd.to_datetime(Xc.tarih), "F_KT10": 1.0})
    ktlog.info("D9 ABD: %d durum, %d rüzgâr-D9 değil (%.0f sn)", len(Dd), len(O), time.time() - t0)
    return O.sort_values(["sembol", "tarih"]).reset_index(drop=True), {"say": {"durum": int(len(Dd)), "c": int(len(O)),
                                                                               "sure_sn": round(time.time() - t0, 1)}, "Xc": Xc}


# ================================================================ 3) PREFIX (geleceğe bakma) DENETİMİ
def kt_prefix(grup: str, pazar: str, X: pd.DataFrame, ek: Dict[str, Any], n: Optional[int] = None) -> Dict[str, Any]:
    """Grup x pazar: rastgele n olayda veri t'de kesilince bayrak girdileri aynı. Tutmazsa KTHata."""
    Pr = KT_ESIK["prefix"]; n = int(n or Pr["n"])
    if not len(X):
        return {"n": 0, "tuttu": 0}
    rng = np.random.default_rng([int(Pr["tohum"]), KT_GRUP.index(grup), KT_PAZAR.index(pazar)])
    sec = X.iloc[np.sort(rng.choice(len(X), min(n, len(X)), replace=False))]
    ok = 0
    if grup == "D9":
        import D9_YENIDEN as D9
        Xc = ek["Xc"]; m = Xc.set_index(["sembol", "tarih"]).index.isin(list(zip(sec.sembol, sec.tarih)))
        try:
            ok = D9.d9_gelecek_denetimi(ek["Vo"], Xc[m].reset_index(drop=True), "ABD", len(sec), int(Pr["tohum"]))
        except D9.D9Hata as ex:
            raise KTHata(f"prefix TUTMADI (D9): {ex}") from ex
        return {"n": int(len(sec)), "tuttu": int(ok)}
    for r in sec.itertuples(index=False):
        s, t = str(r.sembol), pd.Timestamp(r.tarih)
        if grup == "Y1":
            df = ek["Vo"]["V"][s]; kes = df[df.index <= t]
            X1, _ = YH.yh_s6_hisse(kes)
            z = X1[pd.to_datetime(X1.tarih) == t] if len(X1) else X1
            tut = len(z) == 1 and pd.Timestamp(X1.tarih.iloc[-1]) == t
            if tut:
                d = GE.ge_hazir(kes); Fs, _ = GE.ge_ozellik_hisse(d, [t], hazir=True); S7 = YH.yh_s7_ozellik(d, [t], hazir=True).iloc[0].to_dict()
                a = _r6(np.array([{**Fs[0], **S7}[c] for c in YH._Y10_OZ], float))
                b = np.array([getattr(r, c) for c in YH._Y10_OZ], float)
                tut = bool(np.allclose(a, b, rtol=float(Pr["rtol"]), atol=0, equal_nan=True))
        elif grup == "MOM":
            Vd = ek["Vd"]; Pt = ek["P"]["tarih"]
            def _mom(V_: Dict[str, pd.DataFrame]) -> Dict[str, float]:
                o = {}
                for s_, df_ in V_.items():
                    i = df_.index.searchsorted(t, side="right") - 1
                    if i >= 252 and df_.index[i] == t:
                        o[s_] = float(df_.Close.iat[i - 21] / df_.Close.iat[i - 252] - 1)
                return o
            tam = _mom(Vd["V"]); kesik = _mom({s_: d_[d_.index <= t] for s_, d_ in Vd["V"].items()})
            tut = t in Pt and set(tam) == set(kesik) and all(abs(tam[k] - kesik[k]) <= 1e-12 * max(1.0, abs(tam[k])) for k in tam)
        elif grup == "DS":
            df = ek["Vd"]["V"][s]; kes = df[df.index <= t]
            _, _, sds = DS.ds_ozellik_hisse(kes, pazar, ek["bag"], s, None, ek["Vd"]["temiz"].get(s))
            a, b = kt_f15_r5(YH._yh_hazir(kes), [t])
            tut = bool(sds.iloc[-1]) and kes.index[-1] == t and np.allclose([a[0], b[0]], [r.f15, r.r5], rtol=float(Pr["rtol"]), atol=0, equal_nan=True)
        elif grup == "BOFA":
            import BOFA_IZI as BI
            df = ek["V"][s]; c = df.Close[df.index <= t].to_numpy(float)
            Zs = BI.dp_kurulum_seri(c, pazar)
            tut = bool(Zs["kurulum"][-1])
        else:
            raise KTHata(f"bilinmeyen grup {grup}")
        if not tut:
            raise KTHata(f"prefix TUTMADI: {grup} {pazar} {s} {t.date()} -> DURDU (geleceğe bakma şüphesi)")
        ok += 1
    return {"n": int(len(sec)), "tuttu": int(ok)}


# ================================================================ 4) ÖLÇÜM (CETVEL2 v2.2)
def kt_hipotez(grup: str) -> Dict[str, Dict[str, Any]]:
    return {k: {"bayrak": v["bayrak"], "yon": v["yon"]} for k, v in KT_KART.items() if v["grup"] == grup}


_KT_OLC: Dict[str, Any] = {}


def _kt_olc_isci(is_: Tuple[str, str, int]) -> Dict[str, Any]:
    """(grup, pazar, H) -> c2_olc22 (acik + birikimli; plasebo yalnız karar ufkunda) + çeyrek hücreleri + bekleyen sayısı."""
    grup, pazar, H = is_
    O = _KT_OLC["olay"][(grup, pazar)]; veri = _KT_OLC["veri"]; Dn = _KT_OLC["donem"]; D = _KT_OLC["durum"]
    hip = kt_hipotez(grup); pl = H in KT_ESIK["ufuk"]["plasebo"]
    kol = ["pazar", "sembol", "tarih"] + [v["bayrak"] for v in hip.values()]
    R = C2.c2_olc22(O[kol], hip, ufuk=H, donem=Dn, veri=veri, plasebo=pl, bilgi=False, m_bh=len(hip),
                    tohum0=int(KT_ESIK["tohum"][grup]) * 10 + KT_PAZAR.index(pazar), karar=["ABD", "AVR"])
    S = R["satir"]; Hc = R["hucre"].copy()
    Pn = C2.c2_panel22_al(pazar, veri, H); nP = len(Pn["P"]["tarih"]); egri = C2._c2_egri22_al(pazar, "acik", H, None)
    hc_ = []
    S = S.assign(ceyrek=[kt_ceyrek(g) for g in pd.to_datetime(S.giris)]) if len(S) else S.assign(ceyrek=[])
    for ki, (kod, h) in enumerate(hip.items()):
        m = pd.to_numeric(S[h["bayrak"]], errors="coerce").to_numpy(float) == 1 if len(S) else np.zeros(0, bool)
        r15 = S.r15.to_numpy(float) if len(S) else np.zeros(0)
        bek = m & ~np.isfinite(r15) & (S.d.to_numpy(int) + 2 * H - 1 > nP - 1) if len(S) else m
        for hc in list(Dn) + D["acilan"]:
            if hc in Dn:
                mm = m & (S.donem.to_numpy() == hc)
            else:
                mm = m & (S.ceyrek.to_numpy() == hc)
            if hc not in Dn:
                c = C2.c2_hucre(r15[mm], S[f"es_r15_{kod}"].to_numpy(float)[mm], S[f"sira_{kod}"].to_numpy(float)[mm], S.giris.to_numpy()[mm],
                                h["yon"], tohum_ek=int(KT_ESIK["tohum"]["ceyrek"]) + ki * 100 + H,
                                egri=egri, perm=False)
                ol = mm & np.isfinite(S[f"fark_{kod}"].to_numpy(float))
                r = {"kod": kod, "yon": h["yon"], "pazar": pazar, "hucre": hc, "ufuk": H, "n_bayrak": int(mm.sum()),
                     "n_r15": int((mm & np.isfinite(r15)).sum()), "n_essiz": int((mm & np.isfinite(r15) & ~ol).sum()), **c,
                     "plasebo_fark": np.nan, "plasebo_tutar_pay": np.nan, "plasebo_gecti": False, "durum": "BİLGİ (çeyrek)"}
                hc_.append(r)
            if hc in Dn:
                sel = (Hc.kod == kod) & (Hc.hucre == hc)
                if not sel.any():
                    raise KTHata(f"c2_olc22 hücresi yok: {grup} {pazar} R{H} {kod} {hc}")
                Hc.loc[sel, "bekleyen"] = int((mm & bek).sum())
            else:
                hc_[-1]["bekleyen"] = int((mm & bek).sum())
    Hc = pd.concat([Hc, pd.DataFrame(hc_)], ignore_index=True) if hc_ else Hc
    Hc["grup"] = grup
    keep = ["pazar", "sembol", "tarih", "giris", "d", "j", "donem", "ceyrek", "ufuk", "kova", "f15", "atrp", "E0", "r15"] + \
           [c for k in hip for c in (hip[k]["bayrak"], f"es_r15_{k}", f"n_es_{k}", f"sira_{k}", f"fark_{k}")]
    S = S[[c for c in keep if c in S.columns]].assign(grup=grup) if len(S) else S
    return {"hucre": Hc, "satir": S, "say": R["say"].get(pazar, {})}


def kt_bakis_hucre(Hc: pd.DataFrame, S: pd.DataFrame, bakis: bool) -> pd.DataFrame:
    """Birikimli (ve acik) karar hücrelerine bakış boot'u (%97,5 bakışta, %95 bilgi) ve ters yön p'si; T+ / T- yeniden."""
    Hc = Hc.copy()
    E = copy.deepcopy(C2.C2_ESIK)
    if bakis:
        E["boot"]["alt"] = KT_ESIK["bonferroni"]["boot_alt"]; E["boot"]["ust"] = KT_ESIK["bonferroni"]["boot_ust"]
    for c in ("boot_alt_k", "boot_ust_k", "p_ters", "Tp", "Tn"):
        Hc[c] = np.nan if c.startswith(("boot", "p_")) else False
    G = float(C2.C2_ESIK["guc"]["esik"]); nmin = int(C2.C2_ESIK["hucre"]["n_min"])
    for i, r in Hc.iterrows():
        if r.hucre not in ("acik", "birikimli"):
            continue
        g = S[(S.grup == r.grup) & (S.pazar == r.pazar) & (S.ufuk == r.ufuk) & (S.donem == r.hucre)]
        b_ = KT_KART[r.kod]["bayrak"]
        g = g[pd.to_numeric(g[b_], errors="coerce") == 1]
        g = pd.DataFrame({"h5": g.r15.to_numpy(float), "es_h5": g[f"es_r15_{r.kod}"].to_numpy(float), "giris": pd.to_datetime(g.giris)})
        g = g[np.isfinite(g.h5) & np.isfinite(g.es_h5)]
        if not len(g):
            continue
        tek = int(KT_ESIK["tohum"]["bakis_boot"]) + KT_PAZAR.index(r.pazar) * 1000 + int(r.ufuk) * 10 + list(KT_KART).index(r.kod) * 100000
        b = YH.yh_d3_boot_l3o(g, g.assign(h5=g.es_h5), E, tohum_ek=tek)
        Hc.at[i, "boot_alt_k"] = b["boot_alt"]; Hc.at[i, "boot_ust_k"] = b["boot_ust"]
        ters = "-" if r.yon == "+" else "+"
        Hc.at[i, "p_ters"] = DS.ds_perm_p(g, ters, int(C2.C2_ESIK["perm"]["R"]), int(C2.C2_ESIK["perm"]["tohum"]) + 7)
        guclu = bool(r.n >= nmin and np.isfinite(r.guc) and r.guc >= G); kapi = bool(r.plasebo_gecti)
        Hc.at[i, "Tp"] = bool(guclu and kapi and r.fark > 0 and b["boot_alt"] > 0 and r.sira > 0.5 and np.isfinite(r.l3o) and r.l3o > 0)
        l3n = r.l3o_neg if np.isfinite(r.l3o_neg) else C2._c2_l3o_neg(g.assign(sira=np.nan), tek)
        Hc.at[i, "l3o_neg"] = l3n
        Hc.at[i, "Tn"] = bool(guclu and kapi and r.fark < 0 and b["boot_ust"] < 0 and r.sira < 0.5 and np.isfinite(l3n) and l3n < 0)
    return Hc


def _kt_c(Hc: pd.DataFrame, kod: str, H: int, P: str, hucre: str) -> Optional[Dict[str, Any]]:
    x = Hc[(Hc.kod == kod) & (Hc.ufuk == H) & (Hc.pazar == P) & (Hc.hucre == hucre)]
    return x.iloc[0].to_dict() if len(x) else None


def kt_karar(Hc: pd.DataFrame, D: Dict[str, Any]) -> pd.DataFrame:
    """Kart etiketleri (karar kuralı aynen; bakış dışı BİLGİ). Hc kt_bakis_hucre çıktısı."""
    bak = D["bakis_no"] in (1, 2); q = KT_ESIK["bonferroni"]["bh_q"] if bak else KT_ESIK["bh"]["q"]
    U = KT_ESIK["ufuk"]["karar"]; G = float(C2.C2_ESIK["guc"]["esik"]); nmin = int(C2.C2_ESIK["hucre"]["n_min"])
    hb = "birikimli" if D["blok_sayi"] else None
    kartlar = [k for k, v in KT_KART.items() if v["karar"]]
    pk, pt, sat = [], [], []
    for k in kartlar:
        KP = KT_KART[k]["pazar"]; KP = [p for p in KP if p in ("ABD", "AVR")]
        for H in U:
            ps = [(_kt_c(Hc, k, H, P, hb) if hb else None) for P in KP]
            pk.append(max([float(c["p"]) if c and c["n"] >= nmin and np.isfinite(c.get("p", np.nan)) else 1.0 for c in ps] or [1.0]))
            pt.append(max([float(c["p_ters"]) if c and c["n"] >= nmin and np.isfinite(c.get("p_ters", np.nan)) else 1.0 for c in ps] or [1.0]))
    m = int(KT_ESIK["bh"]["m"])
    bh = YH._yh_bh(pk + [1.0] * max(0, m - len(pk)), q)[:len(pk)]; bht = YH._yh_bh(pt + [1.0] * max(0, m - len(pt)), q)[:len(pt)]
    BH = {(k, H): (bh[i], bht[i], pk[i], pt[i]) for i, (k, H) in enumerate([(k, H) for k in kartlar for H in U])}
    # KT00
    k0 = "GÖRMEDİ"; n0 = "blok yok (yalnız açık veri)"
    if hb:
        cs = {H: [_kt_c(Hc, "KT00", H, P, hb) for P in ("ABD", "AVR")] for H in U}
        if any(all(c and bool(c["Tp"]) for c in cs[H]) for H in U):
            k0 = "GÖRDÜ"
        elif any(all(c and np.isfinite(c["fark"]) and c["fark"] > 0 for c in cs[H]) for H in U):
            k0 = "KISMEN"
        n0 = "; ".join(f"R{H}: " + ", ".join(f"{P} FARK {c['fark'] * 100:+.2f} boot [{c['boot_alt_k'] * 100:+.2f}; {c['boot_ust_k'] * 100:+.2f}] "
                                                 f"n {int(c['n'])} T+ {bool(c['Tp'])}" if c and np.isfinite(c.get("fark", np.nan)) else f"{P} -"
                                                 for P, c in zip(("ABD", "AVR"), cs[H])) for H in U)
    sat.append({"kod": "KT00", "etiket": ("KONTROL " + k0) if hb else "KONTROL (blok yok)", "neden": n0, "bakis": D["bakis_no"], "bh_p": np.nan,
                "bh_gecti": np.nan})
    for k in kartlar:
        v = KT_KART[k]; KP = [p for p in v["pazar"] if p in ("ABD", "AVR")]; yon = v["yon"]
        if not hb:
            sat.append({"kod": k, "etiket": "BİLGİ (blok yok; yalnız açık veri)", "neden": "", "bakis": 0, "bh_p": np.nan, "bh_gecti": np.nan})
            continue
        sg = (lambda f: f > 0) if yon == "+" else (lambda f: f < 0)
        sgt = (lambda f: f < 0) if yon == "+" else (lambda f: f > 0)
        sonuc, neden, bhp, bhg = None, [], np.nan, np.nan
        for ters in (False, True):
            for H1 in U:
                H2 = [h for h in U if h != H1][0]
                c1 = [_kt_c(Hc, k, H1, P, hb) for P in KP]; c2_ = [_kt_c(Hc, k, H2, P, hb) for P in KP]; ca = [_kt_c(Hc, k, H1, P, "acik") for P in KP]
                key = ("Tn" if yon == "+" else "Tp") if ters else ("Tp" if yon == "+" else "Tn")
                s_ = sgt if ters else sg
                t1 = all(c is not None and bool(c[key]) for c in c1)
                t2 = all(c is not None and np.isfinite(c["fark"]) and s_(c["fark"]) for c in c2_)
                t3 = all(c is not None and np.isfinite(c["fark"]) and s_(c["fark"]) for c in ca)
                b = BH[(k, H1)]; bg = b[1] if ters else b[0]
                if t1 and t2 and t3 and bg:
                    sonuc = ("KATKI−" if ters else "TUTAR") if k != "KT10" else ("ABD-ADAY (−)" if ters else "ABD-ADAY")
                    neden.append(f"R{H1} {'ters ' if ters else ''}TUTAR ({', '.join(KP)}), R{H2} işaret aynı, açık veri işareti aynı, BH (q {q}) geçti")
                    bhp, bhg = (b[3] if ters else b[2]), True
                    break
                if t1 and t2 and t3 and not bg:
                    neden.append(f"R{H1} {'ters ' if ters else ''}şartlar tuttu ama BH (q {q}) geçmedi (p {(b[3] if ters else b[2]):.4f})")
            if sonuc:
                break
        if not sonuc:
            eks = []
            for H in U:
                for P in KP:
                    c = _kt_c(Hc, k, H, P, hb)
                    if c is None or c["n"] < nmin or not (np.isfinite(c.get("guc", np.nan)) and c["guc"] >= G):
                        eks.append(f"{P} R{H} n {0 if c is None else int(c['n'])} güç {np.nan if c is None else c.get('guc', np.nan):.2f}")
                    elif not bool(c["plasebo_gecti"]):
                        eks.append(f"{P} R{H} plasebo kapısı düştü (ort {c['plasebo_fark'] * 100:+.2f} puan, pay {c['plasebo_tutar_pay']:.2f})")
            if eks:
                sonuc = "ÖLÇÜLEMEDİ"; neden.append("; ".join(eks))
            else:
                sonuc = ("ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)" if k0 == "GÖRMEDİ"
                         else "İZ DEĞİL (bu ufuklarda, güç eğrisindeki en küçük yakalanır etki için)")
                ds_ = [f"{P} R{H} FARK {c['fark'] * 100:+.2f} [{c['boot_alt_k'] * 100:+.2f}; {c['boot_ust_k'] * 100:+.2f}]"
                       for H in U for P in KP for c in [_kt_c(Hc, k, H, P, hb)] if c]
                neden.append("; ".join(ds_))
        if not bak:
            sonuc = f"BİLGİ ({sonuc})"
        sat.append({"kod": k, "etiket": sonuc, "neden": " | ".join(neden), "bakis": D["bakis_no"], "bh_p": bhp, "bh_gecti": bhg})
    return pd.DataFrame(sat)


def kt_yeniden(S: pd.DataFrame, Hc: pd.DataFrame) -> Dict[str, Any]:
    """K11: iki hücre satır dosyasından düz pandas ile (n, ort FARK, ort SIRA)."""
    out, tut = [], True
    for kod, P, H, hc in (("KT01", "ABD", 15, "acik"), ("KT08", "AVR", 30, "acik")):
        b = KT_KART[kod]["bayrak"]; g = S[(S.pazar == P) & (S.ufuk == H) & (S.donem == hc)]
        if b not in g.columns:
            out.append({"hucre": f"{kod} {P} R{H} {hc}", "not": "satır yok"}); continue
        g = g[(pd.to_numeric(g[b], errors="coerce") == 1) & np.isfinite(g[f"fark_{kod}"].astype(float))]
        n = int(len(g)); f = float((g.r15 - g[f"es_r15_{kod}"]).mean()) if n else np.nan; s = float(g[f"sira_{kod}"].mean()) if n else np.nan
        c = _kt_c(Hc, kod, H, P, hc)
        e = c is not None and n == int(c["n"]) and (n == 0 or (abs(f - c["fark"]) < 1e-12 and abs(s - c["sira"]) < 1e-12))
        tut &= bool(e)
        out.append({"hucre": f"{kod} {P} R{H} {hc}", "n": n, "fark": f, "sira": s, "esit": bool(e)})
    return {"tuttu": bool(tut), "hucre": out}


def kt_olc(veri: str, cikti: str, islem: int = 1, onkayit: Optional[str] = None, uzerine: bool = False,
           prefix_n: Optional[int] = None, pazarlar: Optional[List[str]] = None) -> Dict[str, Any]:
    """Bütün kartlar, verilen klasördeki veriyle. Açık veride (blok yok) ön kayıt kapısı aranmaz; blok açıkken zorunlu."""
    t0 = time.time(); bas = _kt_simdi()
    veri = os.path.realpath(veri); os.makedirs(cikti, exist_ok=True)
    if os.path.exists(os.path.join(cikti, KT_DOSYA["karar"])) and not uzerine:
        raise KTHata(f"sonuç zaten var: {os.path.join(cikti, KT_DOSYA['karar'])} (ikinci koşu DURUR; yeni klasör ver)")
    D = kt_durum(veri)
    kapi = kt_kasa(veri, D)
    G = kt_onkayit_kapisi(onkayit or KT_YOL["onkayit"]) if D["blok_sayi"] else {"not": "blok yok (açık veri kuru koşusu); ön kayıt kapısı aranmaz"}
    Dn = kt_hucreler(D)
    pazarlar = pazarlar or KT_PAZAR
    olay: Dict[Tuple[str, str], pd.DataFrame] = {}; huni: Dict[str, Any] = {}; pre: Dict[str, Any] = {}; S_all, H_all = [], []
    for p in pazarlar:
        tp = time.time(); huni[p] = {}
        # (a) OC evreni: Y1 k34'süz (orijinal YAPI_HEDEF Y1 koşusu; regresyonda birebir), D9 ABD k34 dahil (orijinal D9_YENIDEN koşusu)
        Vo = OC.oc_veri(p, klasor=veri, veri2=kt_k34_yok()); Po = OC.oc_panel(Vo)
        X, ey = kt_y1(Vo, Po, p, islem); olay[("Y1", p)] = X; huni[p]["Y1"] = ey["say"]
        pre[f"Y1|{p}"] = kt_prefix("Y1", p, X, {"Vo": Vo}, prefix_n)
        del Vo, Po
        if p == "ABD":
            Vo = OC.oc_veri(p, klasor=veri, veri2=veri)
            Xd, ed = kt_d9(Vo); olay[("D9", p)] = Xd; huni[p]["D9"] = ed["say"]
            pre[f"D9|{p}"] = kt_prefix("D9", p, Xd, {"Vo": Vo, "Xc": ed["Xc"]}, prefix_n)
            del Vo
        # (b) cetvel evreni (CETVEL2 / DS.ds_veri): MOM, DS; BOFA kendi okuyucusu
        Pb = C2.c2_panel22_al(p, veri, None)
        if p in ("ABD", "AVR"):
            Xm, em = kt_mom(p, veri); olay[("MOM", p)] = Xm; huni[p]["MOM"] = em
            pre[f"MOM|{p}"] = kt_prefix("MOM", p, Xm[Xm.F_U == 1], {"Vd": Pb["Vd"], "P": Pb["P"]}, prefix_n)
            Xb, eb = kt_bofa(p, veri); olay[("BOFA", p)] = Xb; huni[p]["BOFA"] = eb["say"]
            pre[f"BOFA|{p}"] = kt_prefix("BOFA", p, Xb, {"V": eb["V"]}, prefix_n)
        Xs, es = kt_ds(Pb, p, islem); olay[("DS", p)] = Xs; huni[p]["DS"] = es["say"]
        pre[f"DS|{p}"] = kt_prefix("DS", p, Xs[Xs.F_KT08 == 1] if (Xs.F_KT08 == 1).any() else Xs, {"Vd": es["Vd"], "bag": es["bag"]}, prefix_n)
        # (c) ölçüm: grup x H (fork; paneller önbellekte)
        for H in KT_ESIK["ufuk"]["karar"] + KT_ESIK["ufuk"]["bilgi"]:
            C2.c2_panel22_al(p, veri, H)
        _KT_OLC.clear(); _KT_OLC.update({"olay": olay, "veri": veri, "donem": Dn, "durum": D})
        isler = [(g, p, H) for g in KT_GRUP if (g, p) in olay for H in KT_ESIK["ufuk"]["karar"] + KT_ESIK["ufuk"]["bilgi"]]
        R = _kt_havuz(_kt_olc_isci, isler, islem)
        for (g, _, H), r in zip(isler, R):
            S_all.append(r["satir"]); H_all.append(r["hucre"]); huni[p].setdefault("cetvel", {})[f"{g}|{H}"] = r["say"]
        for k in [k for k in C2._C2_PN22 if k[0] in (p, "baz") and (k[1] == p or k[0] == p)]:
            C2._C2_PN22.pop(k, None)
        ktlog.info("%s bitti (%.0f sn)", p, time.time() - tp)
    S = pd.concat([s for s in S_all if len(s)], ignore_index=True)
    Hc = pd.concat(H_all, ignore_index=True)
    Hc = kt_bakis_hucre(Hc, S, D["bakis_no"] in (1, 2))
    Kr = kt_karar(Hc, D)
    yen = kt_yeniden(S, Hc)
    # yaz (aynı girdiyle aynı bayt: sıralı, gzip mtime 0, zaman damgası yalnız meta'da)
    S = S.sort_values(["grup", "pazar", "ufuk", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    Hc = Hc.sort_values(["kod", "pazar", "ufuk", "hucre"], kind="mergesort").reset_index(drop=True)
    for c in ("tarih", "giris"):
        S[c] = pd.to_datetime(S[c]).dt.strftime("%Y-%m-%d")
    ys = os.path.join(cikti, KT_DOSYA["satir"]); S.to_csv(ys, index=False, compression={"method": "gzip", "mtime": 0})
    yh = os.path.join(cikti, KT_DOSYA["hucre"]); Hc.drop(columns=[c for c in ("tohum",) if c in Hc.columns]).to_csv(yh, index=False)
    yk = os.path.join(cikti, KT_DOSYA["karar"]); Kr.to_csv(yk, index=False)
    _kt_yaz(os.path.join(cikti, KT_DOSYA["huni"]), json.dumps(_kt_json(huni), ensure_ascii=False, indent=1))
    _kt_yaz(os.path.join(cikti, KT_DOSYA["prefix"]), json.dumps(_kt_json(pre), ensure_ascii=False, indent=1))
    en_gec = {os.path.basename(ys): str(KS.ks_en_gec_tarih(ys).date()),
              "olculen_son_giris": {str(H): str(pd.to_datetime(S[(S.ufuk == H) & np.isfinite(S.r15.astype(float))].giris).max().date())
                                    for H in sorted(S.ufuk.unique()) if ((S.ufuk == H) & np.isfinite(S.r15.astype(float))).any()}}
    asan = [k for k, v in [(os.path.basename(ys), en_gec[os.path.basename(ys)])] + list(en_gec["olculen_son_giris"].items())
            if pd.Timestamp(v) > D["kesik"]]
    J = {"surum": KT_SURUM, "durum": {k: v for k, v in D.items() if k != "kesik"}, "kesik": str(D["kesik"].date()), "hucreler": Dn,
         "kasa": kapi, "onkayit_kapi": G, "yeniden": yen, "en_gec": en_gec, "sha": kt_sha_simdi()}
    _kt_yaz(os.path.join(cikti, KT_DOSYA["sonuc"]), json.dumps(_kt_json(J), ensure_ascii=False, indent=1))
    _kt_yaz(os.path.join(cikti, KT_DOSYA["meta"]), json.dumps(_kt_json({"baslangic": bas, "bitis": _kt_simdi(), "sure_sn": round(time.time() - t0, 1),
                                                                         "islem": islem, "veri": veri}), ensure_ascii=False, indent=1))
    _kt_yaz(os.path.join(cikti, KT_DOSYA["rapor"]), kt_rapor_md(cikti))
    if asan:
        raise KTHata(f"KESİK AŞIMI çıktı dosyasında: {asan}")
    if not yen["tuttu"]:
        raise KTHata(f"yeniden üretim TUTMADI: {yen}")
    ktlog.info("bitti: %d satır, %d hücre (%.0f sn)", len(S), len(Hc), time.time() - t0)
    return {"satir": S, "hucre": Hc, "karar": Kr, "sonuc": J, "huni": huni}


# ================================================================ 5) RAPOR
def _y(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v * 100:+.{n}f}"


def _s(x: Any, n: int = 2) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:.{n}f}"


def kt_hucre_tablo(Hc: pd.DataFrame, hucre: str) -> List[str]:
    L = ["| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    X = Hc[Hc.hucre == hucre]
    for r in X.itertuples(index=False):
        ba = getattr(r, "boot_alt_k", np.nan); bu = getattr(r, "boot_ust_k", np.nan)
        if not np.isfinite(ba if isinstance(ba, float) else np.nan):
            ba, bu = r.boot_alt, r.boot_ust
        L.append(f"| {r.kod} | {r.yon} | {r.pazar} | {int(r.ufuk)} | {int(r.n_bayrak)} | {int(r.n)} | {int(r.n_essiz)} | "
                 f"{int(getattr(r, 'bekleyen', 0) or 0)} | {_y(r.fark)} [{_y(ba)}; {_y(bu)}] | {_y(r.med)} | {_s(r.sira, 3)} | {_y(r.l3o)} | "
                 f"{_s(r.p, 4)} | {_s(r.guc)} | {_y(r.plasebo_fark)} / {_s(r.plasebo_tutar_pay)} / {r.plasebo_gecti} | "
                 f"{getattr(r, 'Tp', '-')} / {getattr(r, 'Tn', '-')} |")
    return L


def kt_rapor_md(cikti: str) -> str:
    J = json.load(open(os.path.join(cikti, KT_DOSYA["sonuc"]), encoding="utf-8"))
    Hc = pd.read_csv(os.path.join(cikti, KT_DOSYA["hucre"])); Kr = pd.read_csv(os.path.join(cikti, KT_DOSYA["karar"]))
    huni = json.load(open(os.path.join(cikti, KT_DOSYA["huni"]), encoding="utf-8"))
    pre = json.load(open(os.path.join(cikti, KT_DOSYA["prefix"]), encoding="utf-8"))
    D = J["durum"]
    L = [f"# KART TURU 1 — sonuç (açık kesik {J['kesik']}, açılmış blok {D['blok_sayi']}: {', '.join(D['acilan']) or 'yok'})", "",
         KT_SURUM, "",
         f"Bakış: {D['bakis'] or ('YOK (açık veri kuru koşusu)' if not D['blok_sayi'] else 'BİLGİ (karar bakışı değil)')}. "
         f"KASA kapısı: kesik {J['kasa']['kesik']}, dosyalar en geç {J['kasa']['dosya']}. Çıktı en geç tarih: {J['en_gec']}.",
         f"Ön kayıt kapısı: {J['onkayit_kapi']}.", f"Yeniden üretim (K11): {'TUTTU' if J['yeniden']['tuttu'] else 'TUTMADI'} {J['yeniden']['hucre']}.",
         "Prefix (K2): " + ", ".join(f"{k} {v['tuttu']}/{v['n']}" for k, v in pre.items()) + ".", "",
         "## Kart etiketleri", "", "| Kart | Etiket | Neden | BH p |", "|---|---|---|---|"]
    for r in Kr.itertuples(index=False):
        L.append(f"| {r.kod} | {r.etiket} | {str(r.neden) if isinstance(r.neden, str) else ''} | {_s(r.bh_p, 4)} |")
    L += ["", "## Huni (olay sayıları; getirisiz)", "", "```", json.dumps(huni, ensure_ascii=False, indent=1)[:12000], "```", ""]
    for h in ["acik", "birikimli"] + list(D["acilan"]):
        if (Hc.hucre == h).any():
            L += [f"## Hücre: {h}", ""] + kt_hucre_tablo(Hc, h) + [""]
    L += ["FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. "
          "Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok."]
    return "\n".join(L) + "\n"


# ================================================================ 6) REGRESYON (eski dosyalar; YALNIZ giriş <= 2022-12-30 satırları; BİLGİ)
def kt_regresyon(veri: str, islem: int = 1, pazarlar: Optional[List[str]] = None) -> Dict[str, Any]:
    """Açık veride yeniden hesaplanan Y1 olayları / Ş bayrakları ve DS ANA olayları, eski dosyaların giriş <= 2022-12-30 satırlarıyla."""
    yh = os.path.join(KOK_KT, "arastirma_cikti", "yapi_hedef"); ge = os.path.join(KOK_KT, "arastirma_cikti", "goz_etiket")
    kes = pd.Timestamp("2022-12-30"); out: Dict[str, Any] = {}
    O1 = pd.read_csv(os.path.join(yh, "olay_Y1.csv.gz"), usecols=["deneme", "pazar", "sembol", "tarih", "giris"], parse_dates=["tarih", "giris"])
    O1 = O1[(O1.deneme == "Y1") & (O1.giris <= kes)]
    Fa = pd.read_csv(os.path.join(ge, "ozellik_Y1.csv.gz"), parse_dates=["tarih"], dtype={"sembol": str})
    Fs = pd.read_csv(os.path.join(yh, "ozellik_Y1_s7.csv.gz"), parse_dates=["tarih"], dtype={"sembol": str})
    Fo = Fa.merge(Fs, on=["pazar", "sembol", "tarih"], how="inner")
    Dso = pd.read_csv(os.path.join(KOK_KT, "arastirma_cikti", "dusus_sonrasi", "ds_olay.csv.gz"), usecols=["pazar", "sembol", "tarih", "giris"],
                      parse_dates=["tarih", "giris"])
    Dso = Dso[Dso.giris <= kes]
    for p in pazarlar or KT_PAZAR:
        Vo = OC.oc_veri(p, klasor=veri, veri2=kt_k34_yok()); Po = OC.oc_panel(Vo)
        X, ey = kt_y1(Vo, Po, p, islem); del Vo, Po
        oo = O1[O1.pazar == p]; b = set(zip(oo.sembol.astype(str), oo.tarih))
        Zg = X  # kt_y1 çıktısı zaten OC.oc_olay_hazirla sonrası (giriş sütunu yok -> yeniden hazırla)
        Pz = OC.oc_panel(OC.oc_veri(p, klasor=veri, veri2=kt_k34_yok()))
        Zg, _ = OC.oc_olay_hazirla(X[["sembol", "tarih"]].assign(pazar=p), Pz); del Pz
        a2 = set(zip(Zg[pd.to_datetime(Zg.giris) <= kes].sembol, pd.to_datetime(Zg[pd.to_datetime(Zg.giris) <= kes].tarih)))
        r = {"y1_yeni_giris_kesik": len(a2), "y1_eski": len(b), "kesisim": len(a2 & b), "yalniz_yeni": sorted(f"{s} {t.date()}" for s, t in a2 - b)[:20],
             "yalniz_eski": sorted(f"{s} {t.date()}" for s, t in b - a2)[:20],
             "yalniz_yeni_yil": {str(k): int(v) for k, v in pd.Series([t.year for _, t in a2 - b], dtype=int).value_counts().sort_index().items()}}
        M = X.merge(Fo[Fo.pazar == p], on=["sembol", "tarih"], how="inner", suffixes=("", "_e"))
        M = M[M.set_index(["sembol", "tarih"]).index.isin(list(a2 & b))]
        Me = pd.DataFrame({c: M[c + "_e"].to_numpy(float) for c in YH._Y10_OZ})
        Se = YH.yh_s7_sartlar(Me)
        fl = {"F_KT02": Se["S1"], "F_KT03": Se["S3"], "F_KT04": Se["S5"], "F_KT05": Se["S4"], "F_KT06": Se["S7"],
              "F_KT07": Se["S1"] & Se["S3"] & Se["S5"]}
        r["bayrak_karsilastirilan"] = int(len(M))
        r["bayrak_farkli"] = {k: int((M[k].to_numpy(float).astype(bool) != np.asarray(v, bool)).sum()) for k, v in fl.items()}
        r["ozellik_max_goreli_fark"] = {c: float(np.nanmax(np.abs(M[c].to_numpy(float) - M[c + "_e"].to_numpy(float)) /
                                                       np.maximum(1e-12, np.abs(M[c + "_e"].to_numpy(float))))) if len(M) else np.nan
                                        for c in YH._Y10_OZ if c + "_e" in M.columns}
        Pb = C2.c2_panel22_al(p, veri, None)
        Xs, _ = kt_ds(Pb, p, islem)
        Zd, _ = OC.oc_olay_hazirla(Xs[["sembol", "tarih"]].assign(pazar=p), Pb["P"], {**json.loads(json.dumps(OC.OC_ESIK)),
                                                                                      "olay": {**OC.OC_ESIK["olay"], "tekil_gun": 1}})
        c1 = set(zip(Zd[pd.to_datetime(Zd.giris) <= kes].sembol, pd.to_datetime(Zd[pd.to_datetime(Zd.giris) <= kes].tarih)))
        dd = Dso[Dso.pazar == p]; c2_ = set(zip(dd.sembol.astype(str), dd.tarih))
        r["ds"] = {"yeni": len(c1), "eski": len(c2_), "kesisim": len(c1 & c2_), "yalniz_yeni": sorted(f"{s} {t.date()}" for s, t in c1 - c2_)[:10],
                   "yalniz_eski": sorted(f"{s} {t.date()}" for s, t in c2_ - c1)[:10],
                   "yalniz_yeni_yil": {str(k): int(v) for k, v in pd.Series([t.year for _, t in c1 - c2_], dtype=int).value_counts().sort_index().items()}}
        for k in [k for k in C2._C2_PN22 if p in k]:
            C2._C2_PN22.pop(k, None)
        out[p] = r; ktlog.info("regresyon %s: %s", p, {k: v for k, v in r.items() if not isinstance(v, (list, dict))})
    return out


# ================================================================ 7) ÖN KAYIT
def kt_guc_tablo(Hc: pd.DataFrame) -> List[Dict[str, Any]]:
    """Açık veri sıklığından 4 / 8 blokta beklenen n (ölçülen n / 7 yıl x 1 / 2 yıl) ve güç (cetvel2_guc_v2.2 'acik' eğrisi)."""
    out = []
    for r in Hc[Hc.hucre == "acik"].itertuples(index=False):
        yil = 7.0; eg = C2._c2_egri22_al(r.pazar, "acik", int(r.ufuk), None)
        n4 = int(round(r.n / yil)); n8 = int(round(2 * r.n / yil))
        out.append({"kod": r.kod, "pazar": r.pazar, "ufuk": int(r.ufuk), "n_acik": int(r.n), "n4": n4, "guc4": C2.c2_guc(n4, eg) if n4 > 0 else 0.0,
                    "n8": n8, "guc8": C2.c2_guc(n8, eg) if n8 > 0 else 0.0})
    return out


def kt_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    L = ["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = KT_KONTROL[k["kod"]]
        L.append(f"| {k['kod']} | {k['ad'] if 'ad' in k else k.get('madde', '')} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(L)


def kt_onkayit_metni(cikti: Optional[str] = None, acik: Optional[str] = None) -> str:
    c = cikti or KT_YOL["cikti"]; a = acik or os.path.join(c, "acik")
    J = json.load(open(os.path.join(a, KT_DOSYA["sonuc"]), encoding="utf-8"))
    Hc = pd.read_csv(os.path.join(a, KT_DOSYA["hucre"])); huni = json.load(open(os.path.join(a, KT_DOSYA["huni"]), encoding="utf-8"))
    pre = json.load(open(os.path.join(a, KT_DOSYA["prefix"]), encoding="utf-8"))
    sha = kt_sha_simdi(); kod_sha = sha["esik"]["KART_TUR1.py"]; c2sha = sha["bagimli"]["CETVEL2.py"]
    if J["sha"]["esik"]["KART_TUR1.py"] != kod_sha:
        raise KTHata("açık kuru koşu başka bir KART_TUR1.py sürümüyle yapılmış -> ön kayıt yazılmaz (kuru koşuyu yeniden yap)")
    L = ["# KART TURU 1 — ÖN KAYIT (donmuş kod; KASA ile yürüyen ileri test)", "",
         f"Tarih: {_kt_simdi()}. İş tanımı: arastirma_cikti/kart/KART_TUR1_IS_TANIMI.md (git {_kt_git(KT_YOL['is_tanimi'])}). Kod: KART_TUR1.py "
         f"(git {_kt_git(KT_YOL['kod'])}). ADIM K1 kararı: R15 ve R30 KARAR, R45 BİLGİ (CETVEL2_POZITIF_KONTROL_v2.2.md).", "",
         f"KASA_HIPOTEZ: {KT_HIPOTEZ}", f"KASA_KOD: KART_TUR1.py {kod_sha}", f"KASA_KOD: CETVEL2.py {c2sha}", f"KT_ESIK_SHA: {sha['esik']['KT_ESIK_SHA']}", "",
         "## 1. Kartlar (tanım ve eşik mevcut modüllerden; yeni eşik yok)", "",
         "| Kart | Yön | Pazar (karar) | Cümle | Tanım (t'de bilinen) | Eşik | Kaynak (modül.fonksiyon) |", "|---|---|---|---|---|---|---|"]
    for k, v in KT_KART.items():
        L.append(f"| {k} | {v['yon']} | {', '.join(v['pazar'])}{'' if v['karar'] else ' (kontrol)'} | {v['cumle']} | {v['tanim']} | {v['esik']} | {v['kaynak']} |")
    L += ["", "Kurulamayan kart: yok (KT09 ve KT10 tanım / eşikleri ilgili modül fonksiyonlarıyla birebir; KT09 BIST ve KT10 AVR için veri yok, "
          "yukarıda yazılı).", "", "## 2. Eşik sha'ları", "", "| Ad | sha256 |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sha["esik"].items()]
    L += ["", "Bağımlı dosyalar (olc blok açıkken bunların sha'sı aynı değilse DURUR):", ""]
    L += [f"BAGIMLI_SHA: {k} {v}" for k, v in sha["bagimli"].items()]
    L += ["", "## 3. Karar kuralı (aynen)", "", KT_ESIK["karar_kurali"], "", f"Cetvel: {KT_ESIK['cetvel']}", "",
          f"Ufuk: {KT_ESIK['ufuk']}", "", f"Hücreler: {KT_ESIK['hucre']['tanim']}", "", f"BH: {KT_ESIK['bh']['tanim']}", "",
          f"Bonferroni: {KT_ESIK['bonferroni']['tanim']}", "", "## 4. Bakış takvimi", "", f"- {KT_ESIK['bakis']['4']}: ana model 2023Q1, 2023Q2, "
          "2023Q3, 2023Q4 bloklarını sırayla açar; her bloktan sonra olc (BİLGİ); 4. bloktan sonraki olc KARAR BAKIŞI 1.",
          f"- {KT_ESIK['bakis']['8']}: 2024Q1-Q4 açılınca 8. bloktan sonraki olc KARAR BAKIŞI 2.", f"- {KT_ESIK['bakis']['tanim']}", "",
          "## 5. Güç tablosu (açık veri sıklığından; 4 blok = 1 yıl, 8 blok = 2 yıl; güç cetvel2_guc_v2.2 'acik' eğrisi, delta +2 puan)", "",
          "| Kart | Pazar | H | n açık (2016-22) | 4 blokta n | güç | 8 blokta n | güç |", "|---|---|---|---|---|---|---|---|"]
    for g in kt_guc_tablo(Hc):
        L.append(f"| {g['kod']} | {g['pazar']} | {g['ufuk']} | {g['n_acik']} | {g['n4']} | {_s(g['guc4'])} | {g['n8']} | {_s(g['guc8'])} |")
    L += ["", "Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural); bu, sonuç görülmeden yazılmıştır.", "",
          "## 6. Açık veri kuru koşusu (2016-22; BİLİNEN VERİ, karar değil)", "",
          f"Çıktı: arastirma_cikti/kart/acik/ (kt_hucre.csv, kt_satir.csv.gz, kt_huni.json, kt_prefix.json). Kesik {J['kesik']}; KASA kapısı "
          f"{J['kasa']['dosya']}; çıktı en geç {J['en_gec']}; yeniden üretim {'TUTTU' if J['yeniden']['tuttu'] else 'TUTMADI'}; prefix "
          + ", ".join(f"{k} {v['tuttu']}/{v['n']}" for k, v in pre.items()) + ".", "", "Huni:", "", "```", json.dumps(huni, ensure_ascii=False, indent=1)[:9000], "```", ""]
    L += kt_hucre_tablo(Hc, "acik")
    L += ["", "## 7. Ana modelin komutları (blok açtıktan sonra)", "",
          "Her blok için (sırayla 2023Q1 ... ; 'KASA_GIZLI' ana modelin ortamında):", "", "```",
          "KASA_GIZLI=<yol> python KASA.py ac --blok 2023Q1 --hipotez KART_TUR1 --onkayit arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md",
          "python KART_TUR1.py olc --veri /tmp/kasa/acik --cikti arastirma_cikti/kart/2023Q1 --islem 4", "```", "",
          "Beklenen çıktı (her blok klasöründe): kt_karar.csv (kart etiketleri; 4. ve 8. blokta KARAR, öteki BİLGİ), kt_hucre.csv (kart x ufuk x "
          "pazar x hücre), kt_satir.csv.gz, kt_huni.json, kt_prefix.json, kt_sonuc.json, kt_meta.json, KART_TUR1_SONUC.md. Ardından "
          "arastirma_cikti/kasa/KASA_DEFTERI.md ve çıktı klasörü commit edilir. KART_TUR1.py ve bu ön kayıt bu commit'ten sonra DEĞİŞMEZ.", "",
          "## 8. KONTROL LİSTESİ", "", kt_kontrol_tablosu(), ""]
    return "\n".join(L) + "\n"


def kt_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    yol = os.path.join(cikti or KT_YOL["cikti"], "KART_TUR1_ON_KAYIT.md")
    if os.path.exists(yol) and not uzerine:
        raise KTHata(f"ön kayıt zaten var: {yol}")
    _kt_yaz(yol, kt_onkayit_metni(cikti))
    import IZ_KARNE as IK
    IK.ik_kontrol_kapisi(yol)
    return yol


# ================================================================ 8) ÇAKIŞMA KAPISI
def _cakisma_kontrol_kt(_once=_CK_ONCE_KT, _dosya="KART_TUR1.py"):
    """Çakışma kapısı: bu dosya bellekteki kt_ / KT_ / _kt öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_KT", "_CK_KAYIT", "_cakisma_kontrol_kt", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "subprocess", "_dt", "annotations", "copy", "argparse",
           "warnings", "Any", "Callable", "Dict", "List", "Optional", "Tuple", "C2", "DS", "GE", "KS", "OC", "PK", "YH")
    onek = ("kt_", "KT_", "_kt", "KTHata", "ktlog", "_KT", "KOK_KT", "_Y10", "_r6", "_y", "_s")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_kt()

if __name__ == "__main__" and "get_ipython" not in globals():
    ap = argparse.ArgumentParser(description=KT_SURUM)
    ap.add_argument("komut", choices=["olc", "onkayit", "regresyon", "sha", "rapor"])
    ap.add_argument("--veri", default=os.environ.get("KT_VERI", "/tmp/kasa/acik"))
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--onkayit", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--pazar", default=None)
    a = ap.parse_args()
    try:
        pz = a.pazar.split(",") if a.pazar else None
        if a.komut == "olc":
            if not a.cikti:
                raise KTHata("--cikti zorunlu (ör. arastirma_cikti/kart/2023Q1)")
            R_ = kt_olc(a.veri, a.cikti, a.islem, a.onkayit, a.uzerine_yaz, pazarlar=pz)
            print(R_["karar"].to_string())
        elif a.komut == "onkayit":
            print(kt_onkayit_yaz(a.cikti, a.uzerine_yaz))
        elif a.komut == "regresyon":
            R_ = kt_regresyon(a.veri, a.islem, pz)
            yol = os.path.join(a.cikti or KT_YOL["cikti"], "kt_regresyon.json")
            _kt_yaz(yol, json.dumps(_kt_json(R_), ensure_ascii=False, indent=1)); print(yol)
        elif a.komut == "rapor":
            print(kt_rapor_md(a.cikti))
        else:
            print(json.dumps(kt_sha_simdi(), indent=1))
    except (KTHata, C2.C2Hata, DS.DSHata, OC.OCHata, PK.PKHata, YH.YHHata, GE.GEHata, KS.KasaHata) as ex:
        ktlog.error("%s", ex); sys.exit(1)
