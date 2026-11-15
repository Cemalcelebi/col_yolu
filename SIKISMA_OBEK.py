"""SIKISMA_OBEK — ÖBEK SIKIŞMASI (S5): Cemal'in üç grafikle düzelttiği tanım; tasarım sınaması + ileri ölçüm, tek dosya (15 Kasım 2026).

Kaynak (Cemal, 15 Kas 2026; FENER, CCOLA, ENJSA günlük): "mum dizilişleri bir öbek gibi yan yana sıkışmış, eğim yukarı olabilir; arada bir
zıplama mumu varsa görmezden gel; Bollinger daralması BÜTÜN bölgelerde şart; yükselişteki bölge sancılı değil dinlenme olmalı, aşağı taban
korunuyor; bölge dipte de olabilir (düşüş sonrası taban)."

S5 (SO_ESIK['S5']; ızgara SO_IZGARA tasarım sınamasında, seçilen değer ön kayıtta DONAR):
  pencere p bar (t-p+1..t). (a) mum: pencerenin en büyük 1 mumu (zıplama) çıkarılıp kalan (H-L)/C'lerin MEDYANI <= k_m x ATR250% (t-249..t ort
  TR/C_önceki); (b) öbek: 1 uç gün (en yüksek ya da en düşük kapanış; bandı en çok daraltan) hariç kapanış bandı max/min-1 <= bant (BIST / ABD,AVR);
  (c) eğim: pencere ln C doğrusal eğimi x p, -%2 .. +%10; (d) aşağı açılış (O < önceki C) payı <= %50; (e) BOLLINGER ŞART: BB(20, 2σ, ddof 0)
  genişliği 4σ20/SMA20 (t) önceki 250 günün (t-250..t-1) değerleri içindeki yüzdeliği (pay(önceki <= bugünkü)) <= bb; (f) uzunluk: 'p' = pencere
  yeter / '10' = (a)+(b)+(e) t'de biten en az 10 ardışık günde doğru.
  SINIF DİP: konum120 = (C - min C 120) / (max - min) <= 0,25 VE C / max C 120 - 1 <= -%10.
  SINIF YOL ÜSTÜ: C > SMA50 VE SMA50_t > SMA50_t-20 VE konum120 >= 0,60 VE taban korunuyor (pencere min C >= pencerenin ilk 5 günü min C x 0,99).
  S5 günü = (a)..(f) VE (DİP ya da YOL). Bölge = ardışık S5 günleri (arası < 20 gün olan parçalar aynı bölge); OLAY (karar günü) = bölgenin ilk
  günü (önceki 19 günde S5 günü yok); bölge sonu = son S5 günü (yalnız bilgi / 'bölge sonrası' ölçüsü). Sınıf = karar günündeki sınıf.
  Geçerli bar (H>L, V>0), likidite alt %20 dışarı, en az 290 geçerli bar, bölünme şüphesi YALNIZ geçmiş pencerede [t-260, t].
ÖLÇÜM: SIKISMA_CEMAL ile BİREBİR aynı sonuç tanımları ve kapılar (SC.sc_sonuc, SC.sc_olc_B, SC._sc_hucre_karar, SY.sy_es_ortalama,
  SY.sy_oran_boot, SY.sy_olc_C, OC.oc_olc): B1 / BH2 / B1k2 / BH2k2 / B0, KAT eş 1 (σ250 ondalığı x likidite üçlüsü) ve eş 2 (pencere ort TR/C /
  ATR250 20'liği x likidite üçlüsü), S5 dışı eşler; ilk büyük hareketin zamanı, yön payı; ORTAK_CETVEL 60 gün + olasılık tablosu; yönsüz stoplu
  kırılım işlemi. Hücreler BIST (bilgi), ABD, AVR x 2016-22 / 2023 / 2024-26; S5, S5_DIP, S5_YOL ayrı. Cemal'in sorusu için düz sayılar: karar
  gününden ve BÖLGE SONUNDAN sonraki 20 günde 'sıkışma mumunun 2x / 3x mumu' ve 'yıllık ATR'nin 2x / 3x' gelen bölgelerin payı (olay / eş).
Komut:  python SIKISMA_OBEK.py tasarim | onkayit | kos | rapor | liste
Colab:  exec(open('SIKISMA_OBEK.py').read()); so_kos()   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_*.pkl; ekran fiyatı /tmp/tavan/yahoo (TAVAN_SERISI.ts_fiyatlar). Satır verisi /tmp/sikisma_obek (repoya girmez).
Çıktı:  arastirma_cikti/sikisma_obek/ SIKISMA_OBEK_TASARIM.md, SIKISMA_OBEK_ON_KAYIT.md, sikisma_obek_sonuc.json, SIKISMA_OBEK_RAPOR.md,
        BOLGE_LISTESI_S5.md. Komisyon / kayma YOK. Evren bugünün listesi (hayatta kalma yanlılığı; yazılır).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_SO = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_SO = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_SO not in sys.path:
    sys.path.insert(0, KOK_SO)

import ORTAK_CETVEL as OC  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402
import SIKISMA_CEMAL as SC  # noqa: E402

solog = logging.getLogger("col.sikisma_obek")
if not solog.handlers:
    _so_h = logging.StreamHandler(sys.stderr)
    _so_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sikisma_obek: %(message)s", "%H:%M:%S"))
    solog.addHandler(_so_h)
    solog.setLevel(logging.INFO)
    solog.propagate = False

SO_SURUM = "SIKISMA_OBEK v1.0 (2026-11-15): öbek sıkışması S5 (öbek + zıplama hariç küçük mum + Bollinger şart; DİP / YOL ÜSTÜ sınıfı) -> büyük hareket"
SO_YOL = {"cikti": os.path.join(KOK_SO, "arastirma_cikti", "sikisma_obek"), "veri": os.environ.get("SO_VERI", "/tmp/veri"),
          "veri2": os.environ.get("OC_VERI2", "/tmp/veri2"), "satir": os.environ.get("SO_SATIR", "/tmp/sikisma_obek"),
          "kod": os.path.join(KOK_SO, "SIKISMA_OBEK.py"), "sc_kod": os.path.join(KOK_SO, "SIKISMA_CEMAL.py"),
          "sy_kod": os.path.join(KOK_SO, "SIKISMA_YENIDEN.py"), "yahoo": os.environ.get("SO_YAHOO", "/tmp/tavan/yahoo")}
SO_DOSYA = {"tasarim": "SIKISMA_OBEK_TASARIM.md", "tasarim_json": "sikisma_obek_tasarim.json", "onkayit": "SIKISMA_OBEK_ON_KAYIT.md",
            "sonuc": "sikisma_obek_sonuc.json", "rapor": "SIKISMA_OBEK_RAPOR.md", "liste": "BOLGE_LISTESI_S5.md", "denetim": "sikisma_obek_denetim.json"}
SO_PAZAR = ("BIST", "ABD", "AVR")

# TASARIM IZGARASI (iş tanımı; tasarım sınamasında yalnız bu kaba ızgarada ayar yapılır; getiri / sonuç ÖLÇÜLMEZ).
SO_IZGARA: Dict[str, Any] = {
    "p": [15, 20],
    "k_m": [0.65, 0.75, 0.85],
    "bant": [{"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, {"BIST": 0.10, "ABD": 0.08, "AVR": 0.08}],
    "bb": [0.15, 0.20, 0.25],
    "uzunluk": ["p", "10"],
    "orta": {"p": 15, "k_m": 0.75, "bant": 0, "bb": 0.20, "uzunluk": "p"},
    "secim_kurali": "(1) 7 örnek x 2 fiyat kaynağı (ekran / V_BIST) = 14 sınamanın hepsini tutan noktalar; yoksa en çok tutan noktalar. "
                    "(2) Aralarından EN SADE: orta noktadan (p 15, k_m 0,75, bant 8/6, bb 0,20, uzunluk 'p') farklı parametre sayısı en az. "
                    "(3) Eşitlikte sıra: p küçük, |k_m - 0,75| küçük, bant dar, |bb - 0,20| küçük, uzunluk 'p'; yine eşitse SIKI olan (k_m küçük, bb küçük).",
    "ornek_kurali": "SEÇMELİ tutar: karar günü (t) örnek aralığında [ilk, son] olan en az bir S5 günü VE o gün sınıf doğru. SEÇMEMELİ tutar: aralıkta "
                    "hiç S5 günü yok (sınıf ne olursa olsun). Aralıklar iş tanımındaki ekran-fiyat aralıkları (CCOLA seçmeli: 02.10-20.10.2025).",
}
SO_ORNEK: List[Dict[str, Any]] = [
    {"ad": "FENER-E", "sembol": "FENER", "ilk": "2025-10-14", "son": "2025-11-07", "beklenen": "DIP", "secmeli": True},
    {"ad": "CCOLA-E", "sembol": "CCOLA", "ilk": "2025-10-02", "son": "2025-10-20", "beklenen": "DIP", "secmeli": True},
    {"ad": "ENJSA-T", "sembol": "ENJSA", "ilk": "2025-07-10", "son": "2025-08-14", "beklenen": "YOL", "secmeli": True},
    {"ad": "FENER-A", "sembol": "FENER", "ilk": "2025-12-03", "son": "2025-12-16", "beklenen": "-", "secmeli": False},
    {"ad": "CCOLA-T", "sembol": "CCOLA", "ilk": "2025-07-29", "son": "2025-08-29", "beklenen": "-", "secmeli": False},
    {"ad": "ENJSA-O", "sembol": "ENJSA", "ilk": "2025-01-20", "son": "2025-02-14", "beklenen": "-", "secmeli": False},
    {"ad": "ENJSA-A", "sembol": "ENJSA", "ilk": "2025-12-30", "son": "2026-01-27", "beklenen": "-", "secmeli": False},
]

# ÖN KAYITTAKİ BÜTÜN SABİTLER (sonuç görüldükten sonra değişmez; mühür so_esik_sha). 'secilen' tasarım sınamasının sonucudur.
SO_ESIK: Dict[str, Any] = {
    "S5": {"secilen": {"p": 15, "k_m": 0.75, "bant": {"BIST": 0.08, "ABD": 0.06, "AVR": 0.06}, "bb": 0.20, "uzunluk": "p"},
           "atr_gun": 250, "zipla_cikar": 1, "uc_gun_cikar": 1, "egim": [-0.02, 0.10], "asagi_acilis_pay": 0.50,
           "bb_gun": 20, "bb_k": 2.0, "bb_ddof": 0, "bb_dagilim": 250, "uzunluk_gun": 10,
           "konum_gun": 120, "dip_konum": 0.25, "dip_dusus": -0.10, "yol_konum": 0.60, "sma_gun": 50, "sma_egim_gun": 20,
           "taban_ilk": 5, "taban_pay": 0.99, "ara": 20,
           "tanim": {"a": "pencerenin en büyük 1 (H-L)/C değeri çıkarılır; kalan p-1 değerin medyanı <= k_m x ATR250% (t-249..t ort TR/C_önceki)",
                     "b": "pencere kapanışlarından en yüksek YA DA en düşük 1 gün (bandı en çok daraltan) çıkarılır; max/min - 1 <= bant",
                     "c": "ln C ~ gün doğrusal eğimi (EKK) x p, [-%2, +%10] içinde",
                     "d": "pencerede O < önceki geçerli barın C'si olan günlerin payı <= %50",
                     "e": "BBW_t = 4 x std20(C, ddof 0) / SMA20(C); pay(BBW_t-250..t-1 <= BBW_t) <= bb",
                     "f": "'p': ek şart yok (pencere yeter); '10': (a)&(b)&(e) t'de biten en az 10 ardışık geçerli barda doğru",
                     "DIP": "konum120 = (C_t - min C t-119..t) / (max - min) <= 0,25 VE C_t / max C t-119..t - 1 <= -%10",
                     "YOL": "C_t > SMA50_t VE SMA50_t > SMA50_t-20 VE konum120 >= 0,60 VE min C (pencere) >= min C (pencerenin ilk 5 günü) x 0,99",
                     "olay": "S5 günü = (a)..(f) VE (DIP ya da YOL); olay = S5 günü ve önceki 19 barda S5 günü yok (bölge ilk günü = karar günü); "
                             "bölge sonu = 20 bardan kısa aralarla süren S5 günlerinin sonuncusu; sınıf = karar günü sınıfı"}},
    "gecmis_min": 290,
    "bolunme_gecmis": [-260, 0],
    "sonuc": {"ana": ["B1", "BH2"], "bilgi": ["B1k2", "BH2k2", "B0", "M2", "M3"],
              "tanim": {"B1": "SC / SY B1 aynen: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250%",
                        "BH2": "SC BH2 (SY B2) aynen: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
                        "B1k2": "t+1..t+20 içinde bir günün TR/C_önceki >= 2 x ATR250% (yıllık ATR'nin 2 katı)",
                        "BH2k2": "max_k |ln(C_t+k / C_t)| >= max(%15, 2 x σ250 x √20)",
                        "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x pencere ort TR/C_önceki (göreli; tanımsal, bilgi)",
                        "M2": "t+1..t+20 içinde bir günün (H-L)/C_önceki >= 2 x sıkışma mumu (t'deki (a) ölçüsü: zıplama hariç medyan mum) (Cemal'in sorusu)",
                        "M3": "aynı, 3 x sıkışma mumu"},
              "bolge_sonu": {"tanim": "olay bölgesinin SON günü e'den sonraki 20 günde A3 (= B1), A2 (= B1k2), M2, M3 (sıkışma mumu e'deki (a) ölçüsü); "
                                      "eş = e günü, aynı pazar, σ250 ondalığı x likidite üçlüsü (e günündeki hücre), uygun, e'de S5 günü değil. "
                                      "Bölge sonu bilgisi geleceğe aittir: yalnız BİLGİ (Cemal'in sorusu); karar ölçüsü değildir.",
                             "olcu": ["A3", "A2", "M3", "M2"]},
              "yon": {"B1": "ilk büyük günün kapanıştan kapanışa getirisinin işareti", "BH2": "eşiği ilk aşan günde ln(C_t+k/C_t) işareti"},
              "zaman": "ilk büyük günün t'den uzaklığı k (1..20); pencereler [1,5] [6,10] [11,15] [16,20]"},
    "es": {"es1": "aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (SY hucA), uygun, S5 günü değil",
           "es2": "aynı gün, aynı pazar, (pencere ort TR/C_önceki / ATR250) 20'liği x likidite üçlüsü, uygun, S5 günü değil (mekanik düşük oynaklık dengesi)",
           "oran_kova": 20, "min_es": 3, "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır"},
    "tanimlar": {"S5": "ev5 (iki sınıf birleşik)", "S5_DIP": "ev5 VE sınıf DİP", "S5_YOL": "ev5 VE sınıf YOL ÜSTÜ"},
    "uygun": "SY 'uygun' ile aynı (likidite alt %20 dışı, σ250 / ATR250 / likidite tanımlı, 20 gün gelecek barı var, dönem içinde) + en az 290 geçerli bar "
             "+ bölünme şüphesi [t-260, t] içinde yok (yalnız geçmiş)",
    "donem": [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]],
    "birlesik": {"2023+": ["2023", "2024-26"]},
    "karar_pazar": ["ABD", "AVR"], "karar_donem": ["2023", "2024-26"], "bilgi_pazar": ["BIST"],
    "bootstrap": "SY.sy_oran_boot: 2000 tekrar, ay kümeli (olay ayı), %95, tohum 1414 + crc32(etiket) % 1000",
    "karar": {"n_min": 30, "n_guc": 1000,
              "hucre": "SC ile aynı: KAT alt95 > 1 hem eş 1 hem eş 2'de ve n >= 30 (iki eş kümesinin küçük n'i) -> GEÇER; n < 30 -> ÖLÇÜLEMEDİ; n >= 1000 ve "
                       "eş 1 ya da eş 2 üst95 < 1 -> TERS; n >= 1000 ve geçmez -> TUTMADI; 30 <= n < 1000 ve geçmez -> ÖLÇÜLEMEDİ (güç)",
              "etiket": "her tanım (S5, S5_DIP, S5_YOL) ve ana sonuç (B1, BH2) için ayrı: dört karar hücresi (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) "
                        "GEÇER -> 'ÖBEK SIKIŞMASI BÜYÜK HAREKET HABERCİSİ'; en az biri GEÇER -> EMARE; hiçbiri geçmez ve dördü TUTMADI / TERS -> 'HABERCİ "
                        "DEĞİL' (dördü TERS ise '(TERS)'); aksi ÖLÇÜLEMEDİ. k2 / B0 / M2 / M3 / bölge sonu / BIST / 2016-22 bilgi."},
    "C": "SY.sy_olc_C aynen (10 gün bandı %1 taşma kapanışı -> ertesi açılış, stop öteki kenar, 20 bar; eş aynı t momentum beşliği x likidite üçlüsü, "
         "S5 dışı; FI_OLCUT dört şart); olay = S5 / S5_DIP / S5_YOL olayı. BİLGİ.",
    "OC": "ORTAK_CETVEL.oc_olc: S5, S5_DIP, S5_YOL olayları ayrı ayrı [sembol, tarih, pazar] (tarih = karar günü t); BİLGİ (yön tahmini yok).",
    "gelecek_denetimi_n": 40, "tohum": 1616,
    "liste": {"bas": "2025-01-01", "son": "2026-08-31", "rastgele_hisse": 7, "ardisik": 3, "en_iyi": 10, "tohum": 27, "pazar": "BIST", "sicrama": 0.11,
              "fiyat": "ekran fiyatı = Yahoo kapanış x sonraki bölünme çarpanı (TAVAN_SERISI.ts_fiyatlar); tespit Yahoo bölünme düzeltmeli oranlarla",
              "sicrama_tanim": "pencere başı .. bölge sonu + 20 gün içinde tek günde |C/C_önceki - 1| > %11 olan bölge 'bedelli / bölünme şüphesi': "
                               "en iyi / en kötü 10'a girmez, satırında işaretli"},
}

SO_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş 1 = aynı gün/pazar σ250 ondalığı x likidite üçlüsü (SY hucA), S5 günü değil; eş 2 = aynı gün (pencere ort TR/C / ATR250) 20'liği x "
                   "likidite üçlüsü, S5 dışı: sıkışmanın ATR250'yi düşürmesinden gelen mekanik üstünlüğü dengeler; aynı B tanımı eşlere; B0 ve M2/M3 "
                   "tanımsal göreli (bilgi); bölge sonu ölçüsünde eş e gününde aynı hücreden; 60 gün getiri ve plasebo yalnız OC.oc_olc; işlem eşleri SY.sy_olc_C"),
    "K2": ("EVET", "so_s5 yalnız t'ye kadar (ATR250 t-249..t, BBW yüzdeliği t-250..t-1 dağılımı, konum120 / SMA50 t'ye kadar, likidite t-1'e kadar); "
                   "olay = önceki 19 barda S5 yok (geçmiş); bölge sonu yalnız sonuç tarafında (bilgi); bölünme şüphesi yalnız [t-260, t]; kos'ta "
                   "so_gelecek_denetimi 40 olay/pazar seriyi t'de kesip aynı tespiti mekanik denetler; test kesme + gelecek bozma"),
    "K3": ("EVET", "SY.sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat sayılmaz); 'önceki C' önceki GEÇERLİ bar; günlük veri, kesik 31.08.2026"),
    "K4": ("EVET", "aynı hissede yeni S5 olayı bölge sonundan en az 20 bar sonra (önceki 19 barda S5 günü yok); n = olay (bölge) sayısı; OC kendi 60 gün "
                   "tekilleştirmesi; ay kümeli bootstrap; zaman medyan + %25-75"),
    "K5": ("EVET", "KAT olasılık ölçüsü (t kapanışı karar anı); 60 gün getiri OC: giriş t sonrası ilk geçerli açılış; işlem SY (C): kırılım kapanışı sonrası açılış"),
    "K6": ("EVET", "ölçüm tek kip: fi_k1_veri düzeltilmiş fiyat (V_*); tasarım ve liste ekran fiyatı ayrı (tespit Yahoo bölünme düzeltmeli oranla); mum ve ATR "
                   "yüzde; AVR likidite EUR (Kur); bölünme şüphesi SY.sy_bolunme_supheli; liste >%11 tek gün süzgeci (BIST marjı %10)"),
    "K7": ("EVET", "evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batanlar yok; raporda yazılı; büyük hareket olasılığı olay ve eşte birlikte etkilenir"),
    "K8": ("EVET", "3 pazar x 3 dönem x 3 tanım (S5, DİP, YOL); n < 30 ÖLÇÜLEMEDİ, 30-999 güç sınırlı ÖLÇÜLEMEDİ (HABERCİ DEĞİL yalnız n >= 1000); iki "
                   "doğrulama dönemi ayrı; ana sonuç 2 (B1, BH2) x 2 eş; k2 / B0 / M / bölge sonu / BIST bilgi; tasarım 7 örneğe göre ayarlandı (aşırı uyum "
                   "riski yazılı; ızgara kaba ve ön kayıtta)"),
    "K9": ("EVET", "tasarım sınaması (getirisiz) ön kayıttan ÖNCE commit; SO_ESIK sha mühür + SIKISMA_OBEK.py / SIKISMA_CEMAL.py / SIKISMA_YENIDEN.py sha + "
                   "OC üç satır ön kayıtta; olay sayımı getirisiz; commit + push sonra kos; kos OC.oc_kapi + kendi git / sha kapısı; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 bölge (7 tasarım örneği dahil) elle doğrulanır"),
    "K11": ("EVET", "2 hücre KAT /tmp/sikisma_obek satır CSV'sinden bağımsız kodla yeniden üretilir; 3 bölge ham veriden elle"),
    "K12": ("EVET", "'HABERCİ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı, 60 gün getiri ve işlem getirisi ayrı tablolarda; komisyon yok yazılır"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_so; yasak dosyalara dokunulmaz (git diff denetimi); e-posta taraması ön kayıt + testte; ücretli veri yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok)"),
}


class SOHata(RuntimeError):
    """Durdurucu hata (ön kayıt yok / mühür ya da kod sha tutmuyor / git'e işlenmemiş / veri yok / geleceğe bakma denetimi tutmadı)."""


_SO_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def _so_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def so_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or SO_ESIK, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def _so_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SO_YOL["cikti"], SO_DOSYA.get(ad, ad))


def _so_sc_E(p: int) -> Dict[str, Any]:
    """SC.sc_sonuc / SC.sc_olc_B için SC_ESIK kopyası (S4 pencere alanı S5 penceresiyle; dönem / birleşik / karar aynı)."""
    E = json.loads(json.dumps(SC.SC_ESIK, default=str))
    E["S4"]["pencere"] = [p]; E["S4"]["ana_pencere"] = p
    E["donem"] = SO_ESIK["donem"]; E["birlesik"] = SO_ESIK["birlesik"]; E["karar"] = SO_ESIK["karar"]
    return E


# ---------------------------------------------------------------- 1) S5 TESPİTİ (yalnız t'ye kadar)
def _so_kayan(x: np.ndarray, w: int) -> np.ndarray:
    """M[i] = x[i-w+1..i] (i < w-1 satırları NaN)."""
    n = len(x); out = np.full((n, w), np.nan)
    if n >= w:
        out[w - 1:] = np.lib.stride_tricks.sliding_window_view(x.astype(float), w)
    return out


def so_s5(d: pd.DataFrame, pazar: str, prm: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """d = SY.sy_veri_hazirla çıktısı (geçerli barlar). prm = {'p', 'k_m', 'bant' (pazar sözlüğü), 'bb', 'uzunluk'}; yoksa SO_ESIK secilen.
    Her bar t için S5 koşulları, sınıf ve tanı sütunları; yalnız t'ye kadarki barlar."""
    E = E or SO_ESIK; S = E["S5"]; prm = prm or S["secilen"]
    p = int(prm["p"])
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    n = len(C); Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = H[0] - L[0]
    atr = pd.Series(tr / Cp).rolling(S["atr_gun"], min_periods=S["atr_gun"]).mean().to_numpy()
    # (a) zıplama hariç medyan mum
    mum = (H - L) / C
    Wm = np.sort(_so_kayan(mum, p), axis=1)[:, :p - S["zipla_cikar"]]
    mmed = np.median(Wm, axis=1)
    # (b) 1 uç gün hariç kapanış bandı
    Wc = np.sort(_so_kayan(C, p), axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        obek = np.fmin(Wc[:, -2] / Wc[:, 0], Wc[:, -1] / Wc[:, 1]) - 1
        bant_tam = Wc[:, -1] / Wc[:, 0] - 1
    # (c) eğim
    x = np.arange(p, dtype=float); xm = x - x.mean()
    Wl = _so_kayan(np.log(C), p)
    egim = ((Wl - Wl.mean(axis=1, keepdims=True)) @ xm) / (xm @ xm) * p
    net = np.r_[np.full(p - 1, np.nan), C[p - 1:] / C[:n - p + 1] - 1] if n >= p else np.full(n, np.nan)
    # (d) aşağı açılış
    asg = (O < Cp).astype(float); asg[0] = np.nan
    asagi = pd.Series(asg).rolling(p, min_periods=p).mean().to_numpy()
    # (e) Bollinger yüzdeliği (önceki 250 gün)
    Cs = pd.Series(C)
    bbw = (2 * S["bb_k"] * Cs.rolling(S["bb_gun"], min_periods=S["bb_gun"]).std(ddof=S["bb_ddof"])
           / Cs.rolling(S["bb_gun"], min_periods=S["bb_gun"]).mean()).to_numpy()
    nb = S["bb_dagilim"]; bbp = np.full(n, np.nan)
    if n > nb:
        Wb = np.lib.stride_tricks.sliding_window_view(bbw, nb)[:n - nb]          # satır j: bbw[j..j+nb-1] = t-250..t-1, t = j+nb
        t_ = np.arange(nb, n)
        with np.errstate(invalid="ignore"):
            ok = np.isfinite(Wb).all(axis=1) & np.isfinite(bbw[t_])
            bbp[t_] = np.where(ok, (Wb <= bbw[t_][:, None]).mean(axis=1), np.nan)
    # trp (eş 2 ve B0): pencere ort TR/C_önceki
    trp = pd.Series(tr / Cp).rolling(p, min_periods=p).mean().to_numpy()
    # sınıf
    kg = S["konum_gun"]
    mx = Cs.rolling(kg, min_periods=kg).max().to_numpy(); mn = Cs.rolling(kg, min_periods=kg).min().to_numpy()
    sma = Cs.rolling(S["sma_gun"], min_periods=S["sma_gun"]).mean().to_numpy()
    sma_once = np.r_[np.full(S["sma_egim_gun"], np.nan), sma[:-S["sma_egim_gun"]]] if n > S["sma_egim_gun"] else np.full(n, np.nan)
    ilk5 = np.r_[np.full(p - 1, np.nan), pd.Series(C).rolling(S["taban_ilk"], min_periods=S["taban_ilk"]).min().to_numpy()[S["taban_ilk"] - 1:n - p + S["taban_ilk"]]] \
        if n >= p else np.full(n, np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        konum = (C - mn) / (mx - mn)
        dd = C / mx - 1
        ca = mmed <= prm["k_m"] * atr
        cb = obek <= prm["bant"][pazar]
        cc = (egim >= S["egim"][0]) & (egim <= S["egim"][1])
        cd = asagi <= S["asagi_acilis_pay"]
        ce = bbp <= prm["bb"]
        taban = Wc[:, 0] >= ilk5 * S["taban_pay"]
        dip = (konum <= S["dip_konum"]) & (dd <= S["dip_dusus"])
        yol = (C > sma) & (sma > sma_once) & (konum >= S["yol_konum"]) & taban
    run = SY._sy_kosu(ca & cb & ce)
    cf = np.ones(n, bool) if str(prm["uzunluk"]) == "p" else run >= S["uzunluk_gun"]
    gm = E["gecmis_min"]; ok_g = np.arange(n) >= gm
    cek = ca & cb & cc & cd & ce & cf & ok_g
    s5d = cek & dip; s5y = cek & yol; s5 = s5d | s5y
    ev = _so_olay(s5, S["ara"], gm)
    return pd.DataFrame({"mmed": mmed, "atr5": atr, "obek": obek, "bant_tam": bant_tam, "egim": egim, "net": net, "asagi": asagi, "bbw": bbw, "bbp": bbp,
                         "trp": trp, "konum": konum, "dd120": dd, "sma50": sma, "sma50_once": sma_once, "taban": taban,
                         "ca": ca, "cb": cb, "cc": cc, "cd": cd, "ce": ce, "cf": cf, "run5": run, "cek": cek, "dip": dip, "yol": yol,
                         "s5c": s5, "s5c_dip": s5d, "s5c_yol": s5y, "ev5": ev, "ev5_dip": ev & dip, "ev5_yol": ev & yol}, index=d.index)


def _so_olay(kosul: np.ndarray, ara: int, bas: int) -> np.ndarray:
    """Olay = koşul doğru VE önceki ara-1 barda koşul hiç doğru değil (bölgenin ilk günü; yeni bölge önceki bölgenin SONUNDAN en az `ara` bar sonra).
    Yalnız geçmişe bakar."""
    k = kosul.astype(bool); n = len(k)
    cs = np.r_[0, np.cumsum(k.astype(int))]
    i = np.arange(n); lo = np.clip(i - (ara - 1), 0, n)
    once = (cs[i] - cs[lo]) > 0
    return k & ~once & (i >= bas)


def so_bolge_sonu(ev: np.ndarray, kosul: np.ndarray, ara: int) -> np.ndarray:
    """Her olay barı i için bölgenin son S5 günü (indeks); olay olmayan barlarda -1. GELECEĞE AİT: yalnız sonuç / liste tarafında kullanılır."""
    k = kosul.astype(bool); n = len(k); out = np.full(n, -1, int)
    for i in np.where(ev)[0]:
        son = i; j = i + 1
        while j < n and j - son < ara:
            if k[j]:
                son = j
            j += 1
        out[i] = son
    return out


def so_gecmis(d: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """SY geçmiş özellikleri (ATR250, σ250, likidite, momentum, S1, 10 gün bandı) + S5 (seçilen parametreler)."""
    E = E or SO_ESIK
    G = SY.sy_gecmis(d, pazar, SY.SY_ESIK)
    X = so_s5(d, pazar, None, E)
    for c in X.columns:
        G[c] = X[c].to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        G["oran"] = X.trp.to_numpy() / G.atr.to_numpy()
    return G


# ---------------------------------------------------------------- 2) SONUÇLAR (t'den sonrası; yalnız kos)
def so_sonuc(d: pd.DataFrame, G: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """SC.sc_sonuc aynen (B1, BH2, B1k2, BH2k2, B0, yön, zaman, (C) işlem) + M2 / M3 (sıkışma mumunun 2x / 3x mumu) + bölge sonu indeksi."""
    E = E or SO_ESIK; h = SY.SY_ESIK["B"]["ufuk"]
    R = SC.sc_sonuc(d, G, _so_sc_E(int(E["S5"]["secilen"]["p"])))
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    Cp = np.r_[np.nan, C[:-1]]
    Mf = SY._sy_ileri((H - L) / Cp, h)
    mm = G.mmed.to_numpy(); gel = R.gel.to_numpy()
    with np.errstate(invalid="ignore"):
        R["M2"] = (Mf >= 2.0 * mm[:, None]).any(axis=1) & gel
        R["M3"] = (Mf >= 3.0 * mm[:, None]).any(axis=1) & gel
    R["bs_i"] = so_bolge_sonu(G.ev5.to_numpy(), G.s5c.to_numpy(), E["S5"]["ara"])
    return R


# ---------------------------------------------------------------- 3) PANEL
_SO_GECMIS_KOL = ["atr", "sig", "m10", "band", "s1c", "ev1", "liq", "mom", "vk", "mmed", "obek", "egim", "net", "asagi", "bbw", "bbp", "trp", "konum",
                  "dd120", "ca", "cb", "cc", "cd", "ce", "cf", "run5", "cek", "dip", "yol", "s5c", "s5c_dip", "s5c_yol", "ev5", "ev5_dip", "ev5_yol", "oran"]
_SO_SONUC_KOL = ["B1", "k1", "BH2", "kh", "B1k2", "BH2k2", "B0", "M2", "M3", "B1_up", "BH2_up", "f1", "f2", "f3", "f4", "h1", "h2", "h3", "h4",
                 "c_yon", "c_r", "c_giris", "c_cikis", "c_ilk20", "c_ilk10"]
_SO_BOOL = ["s1c", "ev1", "ca", "cb", "cc", "cd", "ce", "cf", "cek", "dip", "yol", "s5c", "s5c_dip", "s5c_yol", "ev5", "ev5_dip", "ev5_yol", "sup", "gel", "c_ok"]


def so_panel(V: Dict[str, pd.DataFrame], pazar: str, E: Optional[Dict[str, Any]] = None, sonuc: bool = True) -> pd.DataFrame:
    """Bütün hisse-günler: geçmiş özellikler, (sonuc=True) sonuçlar + bölge sonu tarihi, uygunluk, dönem, eş hücreleri (hucA, hucE2, hucC)."""
    E = E or SO_ESIK; SE = SY.SY_ESIK
    parca = []
    for s, d in V.items():
        try:
            G = so_gecmis(d, pazar, E)
            C = d.Close.to_numpy(float)
            sup = SY.sy_bolunme_supheli(C, SE)
            X = G[_SO_GECMIS_KOL].copy()
            X["sup"] = SY._sy_pencere_var(sup, *E["bolunme_gecmis"])
            X["gel"] = np.arange(len(d)) + SE["B"]["ufuk"] <= len(d) - 1
            X["c_ok"] = np.arange(len(d)) + SE["C"]["gelecek_bar"] <= len(d) - 1
            if sonuc:
                R = so_sonuc(d, G, E)
                for c in _SO_SONUC_KOL:
                    X[c] = R[c].to_numpy()
                bs = R.bs_i.to_numpy()
                X["bs_tarih"] = pd.NaT
                m = bs >= 0
                X.loc[m, "bs_tarih"] = d.index[bs[m]]
                X["bs_gun"] = np.where(m, bs - np.arange(len(d)), -1)
            X["sembol"] = s; X["tarih"] = d.index
            X = X[np.arange(len(d)) >= E["gecmis_min"]]
            parca.append(X)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (log'da)
            solog.warning("%s %s panel dışı: %s", pazar, s, ex)
    P = pd.concat(parca, ignore_index=True)
    for c in _SO_BOOL:
        if c in P:
            P[c] = P[c].fillna(False).astype(bool)
    P["pazar"] = pazar
    P["donem"] = SC._sc_donem(P.tarih, E)
    P["liq_pct"] = P.groupby("tarih").liq.rank(pct=True)
    temel = (P.donem != "") & np.isfinite(P.atr) & np.isfinite(P.sig) & np.isfinite(P.liq) & (P.liq_pct > SE["likidite"]["alt_kesik"]) \
        & (P.sig > 0) & (P.atr > 0)
    P["temel"] = temel
    P["uygun"] = temel & P.gel & ~P.sup
    P["uygun_c"] = P.uygun & P.c_ok & np.isfinite(P.mom)
    u = P.uygun
    g = P[u].groupby("tarih")
    for c in ("oyn", "lq3", "e2", "mom5"):
        P[c] = -1
    P.loc[u, "oyn"] = (np.ceil(g.sig.rank(pct=True, method="first") * SE["eslesme"]["oyn_kova"]) - 1).astype(int)
    P.loc[u, "lq3"] = (np.ceil(g.liq.rank(pct=True, method="first") * SE["likidite"]["kova"]) - 1).astype(int)
    uu = u & np.isfinite(P.oran)
    P.loc[uu, "e2"] = (np.ceil(P[uu].groupby("tarih").oran.rank(pct=True, method="first") * E["es"]["oran_kova"]) - 1).astype(int)
    uc = P.uygun_c
    P.loc[uc, "mom5"] = (np.ceil(P[uc].groupby("tarih").mom.rank(pct=True, method="first") * SE["eslesme"]["mom_kova"]) - 1).astype(int)
    P["hucA"] = P.oyn * 10 + P.lq3
    P["hucE2"] = np.where(P.e2 >= 0, P.e2 * 10 + P.lq3, -1)
    P["hucC"] = P.mom5 * 10 + P.lq3
    return P


def so_sayim(P: pd.DataFrame) -> Dict[str, Any]:
    """Olay SAYIMI (sonuç / getiri kullanmaz)."""
    D = [d[0] for d in SO_ESIK["donem"]]
    out: Dict[str, Any] = {}
    for ad, ev in (("S5", "ev5"), ("S5_DIP", "ev5_dip"), ("S5_YOL", "ev5_yol"), ("S1", "ev1")):
        x = P[P.uygun & P[ev]]
        out[ad] = {d: int((x.donem == d).sum()) for d in D}
    out["S5_gun_pay"] = {d: (float(P[P.uygun & (P.donem == d)].s5c.mean()) if (P.uygun & (P.donem == d)).any() else None) for d in D}
    out["hisse"] = int(P.sembol.nunique()); out["uygun_gun"] = int(P.uygun.sum())
    out["kosul_pay"] = {k: float(P.loc[P.uygun, k].mean()) for k in ("ca", "cb", "cc", "cd", "ce", "cf", "cek", "dip", "yol")}
    return out


# ---------------------------------------------------------------- 4) (A) KAT, bölge sonu, (B) ZAMAN, (C) İŞLEM
_SO_TANIM = [("S5", "ev5"), ("S5_DIP", "ev5_dip"), ("S5_YOL", "ev5_yol")]
_SO_EKSTRA = ["B1_up", "BH2_up", "f1", "f2", "f3", "f4", "h1", "h2", "h3", "h4"]


def so_olc_A(P: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """KAT tablosu: tanım (S5, S5_DIP, S5_YOL) x eş (es1, es2) x sonuç x dönem. SC.sc_olc_A ile aynı hesap (SY.sy_es_ortalama + SY.sy_oran_boot)."""
    E = E or SO_ESIK; pazar = P.pazar.iat[0]; sat = []; satir = {}
    deg = E["sonuc"]["ana"] + E["sonuc"]["bilgi"]
    donem = [d[0] for d in E["donem"]] + list(E["birlesik"])
    u = P.uygun
    for ad, ev in _SO_TANIM:
        olay = u & P[ev]
        for es, huc in (("es1", "hucA"), ("es2", "hucE2")):
            es_m = u & ~P.s5c & (P[huc] >= 0)
            X = SY.sy_es_ortalama(P, olay & (P[huc] >= 0), es_m, huc, deg + _SO_EKSTRA)
            X = X[X.es_n >= E["es"]["min_es"]]
            satir[f"{ad}_{es}"] = X
            for dn in donem:
                Y = X[X.donem.isin(E["birlesik"][dn])] if dn in E["birlesik"] else X[X.donem == dn]
                ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
                for b in deg:
                    kat, a95, u95 = SY.sy_oran_boot(Y[b].astype(float).to_numpy(), Y["es_" + b].to_numpy(), ay, SY.SY_ESIK,
                                                    zlib.crc32(f"{ad}|{es}|{dn}|{b}".encode()) % 1000)
                    sat.append({"pazar": pazar, "donem": dn, "sikisma": ad, "es": es, "olcu": b, "n": int(len(Y)),
                                "p_olay": float(Y[b].mean()) if len(Y) else np.nan, "p_es": float(Y["es_" + b].mean()) if len(Y) else np.nan,
                                "kat": kat, "alt95": a95, "ust95": u95, "es_n_medyan": float(Y.es_n.median()) if len(Y) else np.nan})
    for dn in [d[0] for d in E["donem"]]:
        U = P[u & (P.donem == dn)]
        for b in ("B1", "BH2"):
            sat.append({"pazar": pazar, "donem": dn, "sikisma": "TABAN_tum_gunler", "es": "-", "olcu": b, "n": int(len(U)),
                        "p_olay": float(U[b].mean()) if len(U) else np.nan})
    return pd.DataFrame(sat), satir


def so_olc_bolge_sonu(P: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Cemal'in sorusu (BİLGİ): olay bölgesinin son günü e'den sonraki 20 günde A3 (=B1 e'de), A2 (=B1k2), M3, M2; eş = e günü, aynı hücre (hucA e'de),
    uygun, e'de S5 günü değil. Dönem karar günü t'ye göre."""
    E = E or SO_ESIK; pazar = P.pazar.iat[0]
    ol = ["A3", "A2", "M3", "M2"]; kaynak = {"A3": "B1", "A2": "B1k2", "M3": "M3", "M2": "M2"}
    Pk = P[["sembol", "tarih", "uygun", "s5c", "hucA"] + list(kaynak.values())].rename(columns={"tarih": "bs_tarih", "uygun": "e_uygun", "s5c": "e_s5c",
                                                                                                  "hucA": "e_hucA", **{v: "e_" + k for k, v in kaynak.items()}})
    X = P.loc[P.uygun & P.ev5 & P.bs_tarih.notna(), ["pazar", "sembol", "tarih", "donem", "ev5_dip", "ev5_yol", "bs_tarih", "bs_gun"]].copy()
    X["bs_tarih"] = pd.to_datetime(X.bs_tarih)
    X = X.merge(Pk, on=["sembol", "bs_tarih"], how="left")
    X = X[X.e_uygun.fillna(False).astype(bool) & (X.e_hucA >= 0)]
    es_m = P.uygun & ~P.s5c & (P.hucA >= 0)
    Es = P.loc[es_m, ["tarih", "hucA"] + list(kaynak.values())].copy()
    for c in kaynak.values():
        Es[c] = Es[c].astype(float)
    g = Es.groupby(["tarih", "hucA"])[list(kaynak.values())].agg(["sum", "count"])
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    X = X.merge(g, left_on=["bs_tarih", "e_hucA"], right_index=True, how="left")
    for k, v in kaynak.items():
        X["es_" + k] = X[f"{v}_sum"] / X[f"{v}_count"]
        X[k] = X["e_" + k].astype(float)
    X["es_n"] = X[f"{kaynak['A3']}_count"].fillna(0).astype(int)
    X = X[X.es_n >= E["es"]["min_es"]].drop(columns=[c for c in X.columns if c.endswith(("_sum", "_count"))])
    sat = []
    for ad, m in (("S5", np.ones(len(X), bool)), ("S5_DIP", X.ev5_dip.astype(bool).to_numpy()), ("S5_YOL", X.ev5_yol.astype(bool).to_numpy())):
        for dn in [d[0] for d in E["donem"]] + list(E["birlesik"]):
            Y = X[m & (X.donem.isin(E["birlesik"][dn]) if dn in E["birlesik"] else X.donem == dn).to_numpy()]
            ay = Y.tarih.dt.to_period("M").astype(str).to_numpy()
            for b in ol:
                kat, a95, u95 = SY.sy_oran_boot(Y[b].to_numpy(), Y["es_" + b].to_numpy(), ay, SY.SY_ESIK, zlib.crc32(f"BS|{ad}|{dn}|{b}".encode()) % 1000)
                sat.append({"pazar": pazar, "donem": dn, "sikisma": ad, "olcu": b, "n": int(len(Y)), "p_olay": float(Y[b].mean()) if len(Y) else np.nan,
                            "p_es": float(Y["es_" + b].mean()) if len(Y) else np.nan, "kat": kat, "alt95": a95, "ust95": u95,
                            "bolge_gun_medyan": float(Y.bs_gun.median() + 1) if len(Y) else np.nan})
    return pd.DataFrame(sat), X


def so_olc_C(P: pd.DataFrame, ev: str = "ev5") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """SY.sy_olc_C aynen: olay = S5 (ya da sınıf) olayı, eş = S5 günü değil (SY kodu ev1 / s1c sütunlarını okur; bu çağrı için yeniden adlandırılır)."""
    Q = P[["pazar", "tarih", "donem", "sembol", "uygun_c", ev, "s5c", "hucC", "c_yon", "c_r", "c_giris", "c_cikis", "c_ilk20", "c_ilk10"]] \
        .rename(columns={ev: "ev1", "s5c": "s1c"})
    return SY.sy_olc_C(Q, SY.SY_ESIK)


# ---------------------------------------------------------------- 5) GELECEĞE BAKMA DENETİMİ (mekanik)
_SO_DENETIM_KOL = ["mmed", "obek", "egim", "asagi", "bbw", "bbp", "trp", "konum", "dd120", "run5", "cek", "dip", "yol", "s5c", "ev5", "oran",
                   "atr", "sig", "liq", "s1c", "ev1"]


def so_gelecek_denetimi(V: Dict[str, pd.DataFrame], X: pd.DataFrame, pazar: str, E: Optional[Dict[str, Any]] = None, n: Optional[int] = None) -> int:
    E = E or SO_ESIK; n = n or E["gelecek_denetimi_n"]
    rng = np.random.default_rng(E["tohum"])
    sec = X.iloc[rng.choice(len(X), min(n, len(X)), replace=False)] if len(X) else X
    for r in sec.itertuples():
        d = V[r.sembol]
        G1 = so_gecmis(d, pazar, E).loc[r.tarih, _SO_DENETIM_KOL]
        G2 = so_gecmis(d[d.index <= r.tarih], pazar, E).iloc[-1][_SO_DENETIM_KOL]
        a = pd.to_numeric(G1, errors="coerce").astype(float).to_numpy(); b = pd.to_numeric(G2, errors="coerce").astype(float).to_numpy()
        if not np.allclose(a, b, equal_nan=True, rtol=1e-9, atol=1e-12):
            raise SOHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {pd.Timestamp(r.tarih).date()}")
    return len(sec)


# ---------------------------------------------------------------- 6) TASARIM SINAMASI (getirisiz; ön kayıttan önce)
def _so_kaynaklar(semboller: List[str], veri: Optional[str] = None, yahoo: Optional[str] = None) -> Dict[str, Dict[str, pd.DataFrame]]:
    """{'ekran': {sembol: d}, 'V_BIST': {sembol: d}} (SY biçimi, geçerli bar)."""
    out: Dict[str, Dict[str, pd.DataFrame]] = {}
    try:
        import TAVAN_SERISI as TS
        S, _m = TS.ts_fiyatlar(yahoo or SO_YOL["yahoo"], semboller=semboller)
        out["ekran"] = {s: SC._sc_yahoo_sy(S[s]) for s in semboller if s in S}
    except Exception as ex:
        solog.warning("ekran fiyatı okunamadı: %s", ex)
    try:
        Vb = pd.read_pickle(os.path.join(veri or SO_YOL["veri"], "V_BIST.pkl"))
        Vb = Vb.get("veri", Vb) if isinstance(Vb, dict) and "veri" in Vb else Vb
        out["V_BIST"] = {s: SY.sy_veri_hazirla(Vb[s], SY.SY_ESIK) for s in semboller if s in Vb}
    except Exception as ex:
        solog.warning("V_BIST okunamadı: %s", ex)
    return out


def so_ornek_sina(X: pd.DataFrame, o: Dict[str, Any]) -> Dict[str, Any]:
    """Bir örnek aralığında S5 sonucu ve koşul tanısı (aralıkta en az bir gün doğru mu)."""
    Z = X.loc[o["ilk"]:o["son"]]
    s5 = Z.index[Z.s5c.to_numpy()]
    if o["secmeli"]:
        dogru = Z.s5c_dip if o["beklenen"] == "DIP" else Z.s5c_yol
        tut = bool(dogru.any())
    else:
        tut = not bool(Z.s5c.any())
    kos = {k: bool(Z[k].any()) for k in ("ca", "cb", "cc", "cd", "ce", "cf", "cek", "dip", "yol", "s5c")}
    # en çok koşulu birlikte sağlayan gün (tanı)
    sk = Z[["ca", "cb", "cc", "cd", "ce", "cf"]].sum(axis=1)
    en = Z.index[int(np.argmax(sk.to_numpy()))] if len(Z) else None
    return {"tutar": tut, "s5_gun": [str(t.date()) for t in s5], "ilk_s5": str(s5[0].date()) if len(s5) else "-",
            "sinif_ilk": ("DIP" if Z.s5c_dip.loc[s5[0]] else "YOL") if len(s5) else "-", "kosul": kos,
            "en_iyi_gun": str(en.date()) if en is not None else "-", "en_iyi_gun_kosul": {k: bool(Z.loc[en, k]) for k in ("ca", "cb", "cc", "cd", "ce", "cf", "dip", "yol")} if en is not None else {},
            "olcu": {k: SC._sc_temiz(float(Z.loc[en, k])) for k in ("mmed", "atr5", "obek", "egim", "asagi", "bbp", "konum", "dd120")} if en is not None else {}}


def so_tasarim(veri: Optional[str] = None, yahoo: Optional[str] = None, E: Optional[Dict[str, Any]] = None, cikti: Optional[str] = None,
               yaz: bool = True) -> Dict[str, Any]:
    """Izgaranın her noktasında 7 örneği iki fiyat kaynağında sınar (getiri / sonuç ÖLÇMEZ); seçim kuralıyla noktayı seçer; tablo yazar."""
    E = E or SO_ESIK; Z = SO_IZGARA
    K = _so_kaynaklar(sorted({o["sembol"] for o in SO_ORNEK}), veri, yahoo)
    if not K:
        raise SOHata("tasarım: fiyat kaynağı yok (ekran /tmp/tavan/yahoo ya da /tmp/veri/V_BIST.pkl)")
    noktalar = []
    for p, km, bi, bb, uz in itertools.product(Z["p"], Z["k_m"], range(len(Z["bant"])), Z["bb"], Z["uzunluk"]):
        prm = {"p": p, "k_m": km, "bant": Z["bant"][bi], "bb": bb, "uzunluk": uz}
        sonuc = {}
        for kay, D in K.items():
            Xs = {s: so_s5(d, "BIST", prm, E) for s, d in D.items()}
            for o in SO_ORNEK:
                sonuc[f"{o['ad']}|{kay}"] = so_ornek_sina(Xs[o["sembol"]], o) if o["sembol"] in Xs else {"tutar": False, "s5_gun": [], "kosul": {}}
        tutan = sum(v["tutar"] for v in sonuc.values())
        o_ = Z["orta"]
        fark = int(p != o_["p"]) + int(km != o_["k_m"]) + int(bi != o_["bant"]) + int(bb != o_["bb"]) + int(uz != o_["uzunluk"])
        noktalar.append({"p": p, "k_m": km, "bant_i": bi, "bant": Z["bant"][bi], "bb": bb, "uzunluk": uz, "tutan": tutan, "toplam": len(sonuc),
                         "fark": fark, "sira": (p, abs(km - 0.75), bi, abs(bb - 0.20), uz != "p", km, bb), "sonuc": sonuc})
    en_cok = max(n["tutan"] for n in noktalar)
    aday = [n for n in noktalar if n["tutan"] == en_cok]
    sec = sorted(aday, key=lambda n: (n["fark"], n["sira"]))[0]
    J = {"zaman_utc": _so_simdi(), "kaynak": list(K), "en_cok_tutan": en_cok, "toplam": sec["toplam"], "tam_tutan_nokta": sum(n["tutan"] == n["toplam"] for n in noktalar),
         "aday_nokta": len(aday), "nokta_sayisi": len(noktalar),
         "secilen": {"p": sec["p"], "k_m": sec["k_m"], "bant": sec["bant"], "bb": sec["bb"], "uzunluk": sec["uzunluk"]},
         "secilen_sonuc": sec["sonuc"],
         "noktalar": [{k: v for k, v in n.items() if k not in ("sonuc", "sira")} | {"kacan": [k for k, v in n["sonuc"].items() if not v["tutar"]]} for n in noktalar],
         "orta_sonuc": next(n["sonuc"] for n in noktalar if n["fark"] == 0)}
    if yaz:
        os.makedirs(cikti or SO_YOL["cikti"], exist_ok=True)
        SC._sc_json(_so_yol("tasarim_json", cikti), SC._sc_temiz(J))
        metin = so_tasarim_md(J)
        if _SO_EPOSTA.search(metin):
            raise SOHata("tasarım metninde e-posta biçimli parça var")
        with open(_so_yol("tasarim", cikti), "w", encoding="utf-8") as f:
            f.write(metin + "\n")
        solog.info("tasarım yazıldı: en çok tutan %d / %d; seçilen %s", en_cok, sec["toplam"], J["secilen"])
    return J


def _so_tasarim_tablo(sonuc: Dict[str, Any]) -> List[str]:
    s = ["| örnek | kaynak | beklenen | S5 sonucu | (a) mum | (b) öbek | (c) eğim | (d) aşağı açılış | (e) BB | (f) uzunluk | (a-f) hep | DİP | YOL | tutar | en iyi gün ölçüleri (mum/ATR, öbek, eğim, BB yüzdelik, konum120, 120 gün tepeden) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for o in SO_ORNEK:
        for kay in ("ekran", "V_BIST"):
            v = sonuc.get(f"{o['ad']}|{kay}")
            if v is None:
                continue
            k = v.get("kosul", {}); m = v.get("olcu", {})
            e = lambda b: "E" if b else "-"   # noqa: E731
            sn = (f"S5 {v['ilk_s5']} ({v['sinif_ilk']}), {len(v['s5_gun'])} gün") if v.get("s5_gun") else "S5 yok"
            ol = "-" if not m else (f"{(m['mmed'] or 0) / (m['atr5'] or np.nan):.2f}, %{(m['obek'] or 0) * 100:.1f}, %{(m['egim'] or 0) * 100:+.1f}, "
                                    f"{m['bbp'] if m['bbp'] is None else round(m['bbp'], 2)}, {m['konum'] if m['konum'] is None else round(m['konum'], 2)}, "
                                    f"%{(m['dd120'] or 0) * 100:+.0f} ({v['en_iyi_gun']})")
            s.append(f"| {o['ad']} {o['ilk'][5:]}..{o['son'][5:]} | {kay} | {'SEÇ ' + o['beklenen'] if o['secmeli'] else 'SEÇME'} | {sn} | "
                     + " | ".join(e(k.get(c)) for c in ("ca", "cb", "cc", "cd", "ce", "cf", "cek", "dip", "yol")) + f" | {'TUTTU' if v['tutar'] else 'KAÇTI'} | {ol} |")
    return s


def so_tasarim_md(J: Dict[str, Any]) -> str:
    Z = SO_IZGARA; S = SO_ESIK["S5"]
    s = ["# SIKISMA_OBEK (S5) — TASARIM SINAMASI (ön kayıttan ÖNCE; getiri / sonuç ölçülmedi)", "", SO_SURUM, "", f"- ZAMAN (UTC): `{J['zaman_utc']}`",
         f"- Fiyat kaynakları: {', '.join(J['kaynak'])} (ekran = Yahoo x bölünme çarpanı, tespit oranla; V_BIST = düzeltilmiş).",
         f"- Izgara: p {Z['p']}, k_m {Z['k_m']}, bant {', '.join('BIST %' + format(b['BIST'] * 100, '.0f') + ' / ABD-AVR %' + format(b['ABD'] * 100, '.0f') for b in Z['bant'])}, bb {Z['bb']}, "
         f"uzunluk {Z['uzunluk']} -> {J['nokta_sayisi']} nokta.",
         f"- Sabit (ızgara dışı): eğim {S['egim']}, aşağı açılış <= {S['asagi_acilis_pay']}, DİP konum120 <= {S['dip_konum']} ve tepeden <= {S['dip_dusus']}, "
         f"YOL konum120 >= {S['yol_konum']} + SMA50 üstü ve yükselen + taban (ilk {S['taban_ilk']} gün min x {S['taban_pay']}).",
         f"- Örnek kuralı: {Z['ornek_kurali']}", f"- Seçim kuralı: {Z['secim_kurali']}", "",
         f"## Sonuç: en çok tutan {J['en_cok_tutan']} / {J['toplam']} sınama; 14/14 tutan nokta {J['tam_tutan_nokta']}; aday {J['aday_nokta']} nokta", "",
         f"**SEÇİLEN:** p = {J['secilen']['p']}, k_m = {J['secilen']['k_m']}, bant BIST %{J['secilen']['bant']['BIST'] * 100:.0f} / ABD-AVR "
         f"%{J['secilen']['bant']['ABD'] * 100:.0f}, bb = {J['secilen']['bb']}, uzunluk '{J['secilen']['uzunluk']}'.", ""]
    kac = [k for k, v in J["secilen_sonuc"].items() if not v["tutar"]]
    s += [f"Seçilen noktada kaçan sınama: {', '.join(kac) if kac else 'YOK'}.", "", "## Tasarım sınaması tablosu (seçilen nokta; örnek x koşul: aralıkta en az bir gün sağlandı = E)", ""]
    s += _so_tasarim_tablo(J["secilen_sonuc"])
    s += ["", "## Orta nokta (p 15, k_m 0,75, bant 8/6, bb 0,20, 'p') tablosu (kıyas)", ""] + _so_tasarim_tablo(J["orta_sonuc"])
    s += ["", "## Bütün ızgara (tutan / 14; kaçan sınamalar)", "", "| p | k_m | bant (BIST/ABD) | bb | uzunluk | tutan | orta farkı | kaçan |", "|---|---|---|---|---|---|---|---|"]
    for n in J["noktalar"]:
        s.append(f"| {n['p']} | {n['k_m']} | {n['bant']['BIST']:.2f}/{n['bant']['ABD']:.2f} | {n['bb']} | {n['uzunluk']} | {n['tutan']} | {n['fark']} | {', '.join(n['kacan']) or '-'} |")
    s += ["", "Not: tasarım 7 örneğe göre ayarlandı (aşırı uyum riski): ızgara kaba ve önceden yazılı; ölçüm başka hisse / pazar / dönemlerde ileri sınamadır."]
    return "\n".join(s)


# ---------------------------------------------------------------- 7) ÖN KAYIT
_SO_DESEN = {"muhur": r"MÜHÜR \(SO_ESIK sha256\): `([0-9a-f]{64})`", "kod": r"KOD \(SIKISMA_OBEK\.py sha256\): `([0-9a-f]{64})`",
             "sc_kod": r"SC_KOD \(SIKISMA_CEMAL\.py sha256\): `([0-9a-f]{64})`", "sy_kod": r"SY_KOD \(SIKISMA_YENIDEN\.py sha256\): `([0-9a-f]{64})`",
             "zaman": r"ZAMAN \(UTC\): `([^`]+)`"}


def so_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = SO_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def so_onkayit_metni(sayim: Dict[str, Dict[str, Any]], veri_sha: Dict[str, str], tasarim: Dict[str, Any], tasarim_git: Dict[str, str],
                     E: Optional[Dict[str, Any]] = None) -> str:
    E = E or SO_ESIK; S = E["S5"]; T = S["tanim"]; sc = S["secilen"]
    s = ["# SIKISMA_OBEK (S5, öbek sıkışması) — ÖN KAYIT", "", SO_SURUM, "",
         f"- MÜHÜR (SO_ESIK sha256): `{so_esik_sha(E)}`", f"- KOD (SIKISMA_OBEK.py sha256): `{SY._sy_sha_dosya(SO_YOL['kod'])}`",
         f"- SC_KOD (SIKISMA_CEMAL.py sha256): `{SY._sy_sha_dosya(SO_YOL['sc_kod'])}`",
         f"- SY_KOD (SIKISMA_YENIDEN.py sha256): `{SY._sy_sha_dosya(SO_YOL['sy_kod'])}`", f"- ZAMAN (UTC): `{_so_simdi()}`",
         f"- Tasarım sınaması commit: `{tasarim_git.get('commit', '-')}` ({tasarim_git.get('commit_zamani', '-')}); SIKISMA_OBEK_TASARIM.md.",
         "- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` OC.oc_kapi (kontrol + cetvel sha + git) ve kendi kapısı (mühür, üç kod sha, "
         "git'e işlenmiş ve değişmemiş) geçmezse durur.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Soru", "Cemal'in üç grafikle düzelttiği öbek sıkışması (S5; DİP ve YOL ÜSTÜ sınıfı) bitince 20 günde hissenin olağan ölçüsüne göre büyük hareket "
         "(B1 tek gün, BH2 çok gün) eşlerden sık mı; ne zaman, hangi yöne; sıkışma mumunun 2x / 3x mumu ne sıklıkla geliyor. 60 gün getiri ve yönsüz işlem bilgi.", "",
         "## Tanım (SO_ESIK['S5']; seçilen ızgara noktası DONDU)", "",
         f"- Seçilen: p = {sc['p']}, k_m = {sc['k_m']}, bant BIST %{sc['bant']['BIST'] * 100:.0f} / ABD %{sc['bant']['ABD'] * 100:.0f} / AVR "
         f"%{sc['bant']['AVR'] * 100:.0f}, bb = {sc['bb']}, uzunluk '{sc['uzunluk']}'."]
    s += [f"- ({k}) {v}" for k, v in T.items()]
    s += [f"- Geçmiş: en az {E['gecmis_min']} geçerli bar. Uygunluk: {E['uygun']}.", f"- Bölünme şüphesi: SY.sy_bolunme_supheli ANA, pencere {E['bolunme_gecmis']} (yalnız geçmiş).",
          f"- Izgara (tasarımda ayarlandı): {json.dumps({k: v for k, v in SO_IZGARA.items() if k in ('p', 'k_m', 'bant', 'bb', 'uzunluk')}, ensure_ascii=False)}.",
          f"- Seçim kuralı: {SO_IZGARA['secim_kurali']}", "", "## Tasarım sınaması (ön kayıttan önce; getirisiz)", "",
          f"En çok tutan {tasarim['en_cok_tutan']} / {tasarim['toplam']} sınama (7 örnek x 2 fiyat kaynağı); 14/14 tutan nokta {tasarim['tam_tutan_nokta']}; "
          f"seçilen nokta yukarıda. Kaçan: {', '.join(k for k, v in tasarim['secilen_sonuc'].items() if not v['tutar']) or 'YOK'}.", ""]
    s += _so_tasarim_tablo(tasarim["secilen_sonuc"])
    s += ["", "## Sonuçlar (SIKISMA_CEMAL / SIKISMA_YENIDEN içe alınır)", ""]
    s += [f"- **{k}**: {v}" for k, v in E["sonuc"]["tanim"].items()]
    s += [f"- Bölge sonu (Cemal'in sorusu, BİLGİ): {E['sonuc']['bolge_sonu']['tanim']}",
          f"- Yön: B1 {E['sonuc']['yon']['B1']}; BH2 {E['sonuc']['yon']['BH2']}.", f"- Zaman: {E['sonuc']['zaman']}.",
          f"- Eş 1: {E['es']['es1']}.", f"- Eş 2: {E['es']['es2']}.", f"- {E['es']['olay_secimi']}; bootstrap {E['bootstrap']}.",
          f"- Tanımlar: {E['tanimlar']}.", f"- (C) 60 gün: {E['OC']}", f"- (C) işlem: {E['C']}",
          f"- Dönemler {E['donem']}; karar hücreleri ABD / AVR x 2023 / 2024-26; BIST ve 2016-22 bilgi.",
          f"- Hücre kararı: {E['karar']['hucre']}.", f"- Etiket: {E['karar']['etiket']}.", "",
          "## Eşik sözlüğü (SO_ESIK, kararlı JSON)", "", "```json", json.dumps(E, sort_keys=True, ensure_ascii=False, indent=1, default=str), "```", "",
          "## Veri", ""] + [f"- V_{p}.pkl sha256: `{h}`" for p, h in veri_sha.items()]
    D = [d[0] for d in E["donem"]]
    s += ["", "## Olay SAYIMI (sonuç / getiri hesaplanmadan; uygun hisse-gün)", "", "| Pazar | Tanım | 2016-22 | 2023 | 2024-26 |", "|---|---|---|---|---|"]
    for p, c in sayim.items():
        for k in ("S5", "S5_DIP", "S5_YOL", "S1"):
            s.append(f"| {p} | {k} | {c[k]['2016-22']} | {c[k]['2023']} | {c[k]['2024-26']} |")
    s += ["", "| Pazar | S5 günü payı (2016-22 / 2023 / 2024-26) | koşul payı (a / b / c / d / e / f / a-f / DİP / YOL) | hisse | uygun gün |", "|---|---|---|---|---|"]
    for p, c in sayim.items():
        s.append(f"| {p} | {' / '.join(SC._sc_yz(c['S5_gun_pay'][d], 2) for d in D)} | "
                 f"{' / '.join(SC._sc_yz(c['kosul_pay'][k]) for k in ('ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cek', 'dip', 'yol'))} | {c['hisse']} | {c['uygun_gun']} |")
    s += ["", "## Sınırlar (önceden)", "- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).",
          "- Tanım 7 BIST örneğine göre kaba ızgarada ayarlandı (aşırı uyum riski); ölçüm ABD / AVR ve öteki BIST hisselerinde ileri sınamadır.",
          "- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür.", "- Komisyon, kayma, açığa satış maliyeti yok.",
          "- BIST ölçümü düzeltilmiş fiyatla (V_BIST); liste ve tasarım ekran fiyatıyla da. BIST ±%10 sınırı B1'i kısar (BH2 ikinci ana ölçü).",
          "- Güç sınırlı hücreler (n < 1000) ÖLÇÜLEMEDİ yazılır, 'yok' denmez.", "", so_kontrol_tablosu(), ""]
    return "\n".join(s)


def so_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _so_yol("onkayit", cikti)
    if os.path.exists(yol):
        if not uzerine:
            raise SOHata(f"ön kayıt zaten var ({yol}); üzerine yazılmaz")
        try:
            SY._sy_git_islenmis(yol)
            raise SOHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except SY.SYHata as ex:
            if "işlenmemiş" not in str(ex):
                raise SOHata(str(ex))
    ty = _so_yol("tasarim_json", cikti)
    if not os.path.exists(ty):
        raise SOHata("tasarım sınaması yok: önce `python SIKISMA_OBEK.py tasarim` ve commit")
    try:
        tg = SY._sy_git_islenmis(ty)
    except SY.SYHata as ex:
        raise SOHata(f"tasarım sınaması git'e işlenmemiş / değişmiş: {ex}")
    TJ = json.load(open(ty, encoding="utf-8"))
    if json.dumps(TJ["secilen"], sort_keys=True) != json.dumps(SO_ESIK["S5"]["secilen"], sort_keys=True):
        raise SOHata(f"SO_ESIK secilen ({SO_ESIK['S5']['secilen']}) tasarımın seçtiği noktadan ({TJ['secilen']}) farklı")
    sayim, vsha = {}, {}
    for p in SO_PAZAR:
        vsha[p] = SY._sy_sha_dosya(os.path.join(veri or SO_YOL["veri"], f"V_{p}.pkl"))
        V = SY.sy_veri_yukle(p, SY.SY_ESIK, veri or SO_YOL["veri"])
        P = so_panel(V, p, SO_ESIK, sonuc=False)
        sayim[p] = so_sayim(P)
        solog.info("%s sayım: S5 %s DIP %s YOL %s", p, sayim[p]["S5"], sayim[p]["S5_DIP"], sayim[p]["S5_YOL"])
        del P, V
    metin = so_onkayit_metni(sayim, vsha, TJ, tg)
    if _SO_EPOSTA.search(metin):
        raise SOHata("ön kayıtta e-posta biçimli parça var")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    solog.info("ön kayıt yazıldı: %s", yol)
    return yol


def so_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, kod_sha: bool = True) -> Dict[str, Any]:
    yol = yol or _so_yol("onkayit")
    if not os.path.exists(yol):
        raise SOHata(f"ön kayıt yok ({yol}): önce `python SIKISMA_OBEK.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); oc = {}
    for ad, desen in _SO_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise SOHata(f"ön kayıt bozuk: '{ad}' yok")
        oc[ad] = m.group(1)
    if oc["muhur"] != so_esik_sha():
        raise SOHata("ön kayıt mührü tutmuyor: eşikler ön kayıttan sonra değişmiş, koşu durdu")
    if kod_sha:
        for ad, k in (("kod", "kod"), ("sc_kod", "sc_kod"), ("sy_kod", "sy_kod")):
            if oc[ad] != SY._sy_sha_dosya(SO_YOL[k]):
                raise SOHata(f"{os.path.basename(SO_YOL[k])} sha256 ön kayıttakinden farklı (SAPMA): koşu durdu")
    out = {"yol": yol, **oc}
    if git:
        try:
            out["git"] = SY._sy_git_islenmis(yol)
        except SY.SYHata as ex:
            raise SOHata(str(ex))
    return out


# ---------------------------------------------------------------- 8) KOŞU
def so_karar(TA: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    E = E or SO_ESIK; out: Dict[str, Any] = {}
    for ad, _ev in _SO_TANIM:
        out[ad] = {}
        for b in E["sonuc"]["ana"] + E["sonuc"]["bilgi"]:
            hucre = {}
            for p in E["karar_pazar"] + E["bilgi_pazar"]:
                for d in [x[0] for x in E["donem"]] + list(E["birlesik"]):
                    x = {es: TA[(TA.sikisma == ad) & (TA.es == es) & (TA.olcu == b) & (TA.pazar == p) & (TA.donem == d)] for es in ("es1", "es2")}
                    if not all(len(v) for v in x.values()):
                        hucre[f"{p} {d}"] = "ÖLÇÜLEMEDİ"; continue
                    r1, r2 = x["es1"].iloc[0], x["es2"].iloc[0]
                    hucre[f"{p} {d}"] = SC._sc_hucre_karar(int(min(r1.n, r2.n)), r1.alt95, r2.alt95, r1.ust95, r2.ust95, E)
            kh = [hucre.get(f"{p} {d}", "ÖLÇÜLEMEDİ") for p in E["karar_pazar"] for d in E["karar_donem"]]
            liste = ", ".join(f"{p} {d}={hucre[f'{p} {d}']}" for p in E["karar_pazar"] for d in E["karar_donem"])
            if all(v == "GEÇER" for v in kh):
                g = "ÖBEK SIKIŞMASI BÜYÜK HAREKET HABERCİSİ"
            elif any(v == "GEÇER" for v in kh):
                g = f"EMARE ({liste})"
            elif all(v in ("TUTMADI", "TERS") for v in kh):
                g = "HABERCİ DEĞİL" + (" (TERS: S5 sonrası büyük hareket eşlerden SEYREK)" if all(v == "TERS" for v in kh) else "")
            else:
                g = f"ÖLÇÜLEMEDİ ({liste})"
            out[ad][b] = {"etiket": g if b in E["sonuc"]["ana"] else "BİLGİ: " + g, "hucre": hucre}
    return out


def so_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True, pazarlar: Tuple[str, ...] = SO_PAZAR,
           satir: Optional[str] = None, oc_veri: bool = True) -> Dict[str, Any]:
    E = SO_ESIK; t0 = time.time()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    yol = _so_yol("onkayit", cikti)
    kapi = OC.oc_kapi(yol, git=git, kontrol=kontrol)
    ok = so_onkayit_dogrula(yol, git=git)
    kz = _so_simdi()
    satir = satir or SO_YOL["satir"]; os.makedirs(satir, exist_ok=True)
    A_, BS_, B_, C_, den, say = [], [], [], [], {}, {}
    oc_parca: Dict[str, List[Dict[str, Any]]] = {ad: [] for ad, _ in _SO_TANIM}
    Esc = _so_sc_E(int(E["S5"]["secilen"]["p"]))
    for p in pazarlar:
        V = SY.sy_veri_yukle(p, SY.SY_ESIK, veri or SO_YOL["veri"])
        P = so_panel(V, p, E, sonuc=True)
        say[p] = so_sayim(P)
        tA, satirlar = so_olc_A(P, E)
        tBS, XBS = so_olc_bolge_sonu(P, E)
        den[p] = {"gelecek_denetimi_olay": so_gelecek_denetimi(V, satirlar["S5_es1"], p, E)}
        for ad, ev in _SO_TANIM:
            for r in SC.sc_olc_B(satirlar[f"{ad}_es1"], Esc):
                B_.append({"sikisma": ad, **r})
            tC, XC = so_olc_C(P, ev)
            tC.insert(0, "sikisma", ad); C_.append(tC)
            XC.to_csv(os.path.join(satir, f"olay_C_{ad}_{p}.csv.gz"), index=False)
        A_.append(tA); BS_.append(tBS)
        for ad, X in satirlar.items():
            kol = [c for c in ["pazar", "sembol", "tarih", "donem", "hucA", "hucE2", "es_n", "B1", "BH2", "B1k2", "BH2k2", "B0", "M2", "M3", "k1", "kh",
                               "B1_up", "BH2_up", "es_B1", "es_BH2", "es_B1k2", "es_BH2k2", "es_B0", "es_M2", "es_M3", "es_B1_up", "es_BH2_up",
                               "mmed", "atr", "obek", "egim", "bbp", "konum", "dd120", "ev5_dip", "ev5_yol", "bs_tarih", "bs_gun"] if c in X.columns]
            X[kol].to_csv(os.path.join(satir, f"olay_{ad}_{p}.csv.gz"), index=False)
        XBS.to_csv(os.path.join(satir, f"bolge_sonu_{p}.csv.gz"), index=False)
        for es, huc in (("es1", "hucA"), ("es2", "hucE2")):
            m_ = P.uygun & ~P.s5c & (P[huc] >= 0)
            P.loc[m_, ["tarih", huc, "B1", "BH2"]].groupby(["tarih", huc]).agg(B1_t=("B1", "sum"), BH2_t=("BH2", "sum"), n=("B1", "size")) \
                .reset_index().to_csv(os.path.join(satir, f"es_{es}_{p}.csv.gz"), index=False)
        girdi = {}
        for ad, ev in _SO_TANIM:
            olay = P.loc[P[ev] & (P.donem != "") & ~P.sup, ["sembol", "tarih"]].copy(); olay["pazar"] = p
            olay.to_csv(os.path.join(satir, f"oc_girdi_{ad}_{p}.csv.gz"), index=False)
            girdi[ad] = olay.reset_index(drop=True)
        solog.info("%s panel bitti: S5 olay %d (%.0f sn)", p, int((P.uygun & P.ev5).sum()), time.time() - t0)
        del P
        if oc_veri:
            Vd = OC.oc_veri(p, klasor=veri or SO_YOL["veri"], veri2=SO_YOL["veri2"])
            for ad, _ev in _SO_TANIM:
                oc_parca[ad].append(OC.oc_olc(girdi[ad], {p: Vd}))
            del Vd
            OC._OC_PANEL_ONBELLEK.clear()
        del V
        solog.info("%s bitti (%.0f sn)", p, time.time() - t0)
    TA = pd.concat(A_, ignore_index=True); TBS = pd.concat(BS_, ignore_index=True); TC = pd.concat(C_, ignore_index=True)
    karar = so_karar(TA, E)
    J: Dict[str, Any] = {"surum": SO_SURUM, "onkayit": ok, "oc_kapi": {k: v for k, v in kapi.items() if k != "kontrol"}, "kos_zaman_utc": kz,
                         "muhur": so_esik_sha(), "secilen": E["S5"]["secilen"], "sayim": say,
                         "A": json.loads(TA.to_json(orient="records", force_ascii=False)), "BS": json.loads(TBS.to_json(orient="records", force_ascii=False)),
                         "B": B_, "C": json.loads(TC.to_json(orient="records", force_ascii=False)), "karar": karar, "denetim": den, "pazarlar": list(pazarlar)}
    if oc_veri:
        J["oc"] = {}
        for ad, parca in oc_parca.items():
            if not parca:
                continue
            S = SC._sc_birlestir(parca)
            S["olay"].to_csv(os.path.join(satir, f"oc_olay_{ad}.csv.gz"), index=False)
            J["oc"][ad] = {"hucre": json.loads(S["hucre"].to_json(orient="records", force_ascii=False)) if len(S["hucre"]) else [],
                           "olasilik": json.loads(S["olasilik"].to_json(orient="records", force_ascii=False)) if len(S["olasilik"]) else [],
                           "etiket": S["etiket"], "rapor": OC.oc_rapor(S, f"{ad} (öbek sıkışması) olayları — 60 gün eşli (BİLGİ)")}
    J["sure_sn"] = round(time.time() - t0, 1)
    SC._sc_json(_so_yol("sonuc", cikti), SC._sc_temiz(J))
    return {"sonuc": J, "rapor": so_rapor(cikti)}


# ---------------------------------------------------------------- 9) RAPOR
def so_rapor(cikti: Optional[str] = None) -> str:
    J = json.load(open(_so_yol("sonuc", cikti), encoding="utf-8"))
    E = SO_ESIK; A = pd.DataFrame(J["A"]); C = pd.DataFrame(J["C"]); B = pd.DataFrame(J["B"]); BS = pd.DataFrame(J["BS"])
    g = J["onkayit"].get("git", {}); D = [d[0] for d in E["donem"]]
    say = J["sayim"]; yz, s2 = SC._sc_yz, SC._sc_s

    def kat(p, d, b, es, sik="S5"):
        x = A[(A.pazar == p) & (A.donem == d) & (A.olcu == b) & (A.es == es) & (A.sikisma == sik)]
        return x.iloc[0] if len(x) else None

    def kt(r):
        return "-" if r is None or not r["n"] else f"{s2(r['kat'])} [{s2(r['alt95'])}, {s2(r['ust95'])}]"

    def bs(p, d, b, sik="S5"):
        x = BS[(BS.pazar == p) & (BS.donem == d) & (BS.olcu == b) & (BS.sikisma == sik)]
        return x.iloc[0] if len(x) else None

    sec = J["secilen"]
    s = ["# SIKISMA_OBEK (S5, öbek sıkışması) — RAPOR", "", f"{J['surum']}. Ön kayıt commit {str(g.get('commit', '-'))[:10]} ({g.get('commit_zamani', '-')}); "
         f"koşu {J['kos_zaman_utc']}; süre {J.get('sure_sn')} sn. Mühür `{J['muhur'][:16]}…`. Seçilen: p {sec['p']}, k_m {sec['k_m']}, bant BIST "
         f"%{sec['bant']['BIST'] * 100:.0f} / ABD-AVR %{sec['bant']['ABD'] * 100:.0f}, bb {sec['bb']}, uzunluk '{sec['uzunluk']}'.", "", "## DÜZ DİL ÖZET", ""]
    for p in J["pazarlar"]:
        c = say[p]
        s.append(f"- **{p}**: S5 bölgesi {c['S5']['2016-22']} / {c['S5']['2023']} / {c['S5']['2024-26']} (2016-22 / 2023 / 2024-26); DİP "
                 f"{c['S5_DIP']['2016-22']} / {c['S5_DIP']['2023']} / {c['S5_DIP']['2024-26']}; YOL ÜSTÜ {c['S5_YOL']['2016-22']} / {c['S5_YOL']['2023']} / "
                 f"{c['S5_YOL']['2024-26']}.")
    for ad, _ev in _SO_TANIM:
        for b in E["sonuc"]["ana"]:
            s.append(f"- **{ad} {b}**: **{J['karar'][ad][b]['etiket']}**.")
    s.append("- Cemal'in sorusu (2023+, bölge SONUNDAN sonraki 20 gün; olay % / eş %): " + "; ".join(
        f"{p}: sıkışma mumunun 2x {yz(bs(p, '2023+', 'M2')['p_olay'] if bs(p, '2023+', 'M2') is not None else None, 0)} / "
        f"{yz(bs(p, '2023+', 'M2')['p_es'] if bs(p, '2023+', 'M2') is not None else None, 0)}, 3x "
        f"{yz(bs(p, '2023+', 'M3')['p_olay'] if bs(p, '2023+', 'M3') is not None else None, 0)} / {yz(bs(p, '2023+', 'M3')['p_es'] if bs(p, '2023+', 'M3') is not None else None, 0)}; "
        f"yıllık ATR'nin 2x {yz(bs(p, '2023+', 'A2')['p_olay'] if bs(p, '2023+', 'A2') is not None else None, 0)} / "
        f"{yz(bs(p, '2023+', 'A2')['p_es'] if bs(p, '2023+', 'A2') is not None else None, 0)}, 3x "
        f"{yz(bs(p, '2023+', 'A3')['p_olay'] if bs(p, '2023+', 'A3') is not None else None, 0)} / {yz(bs(p, '2023+', 'A3')['p_es'] if bs(p, '2023+', 'A3') is not None else None, 0)}"
        for p in J["pazarlar"]) + ".")
    s += ["- Sayı ile yorum ayrı: KAT > 1 = S5'ten sonra 20 günde büyük hareket eşlerden SIK; < 1 = SEYREK. Eş 2 sıkışmanın kendi düşük oynaklığını "
          "dengeler (mekanik üstünlük kontrolü). Sıkışma mumuna göre ölçüler (M2 / M3, B0) tanım gereği eşlerden sık çıkar (göreli ölçü; bilgi).",
          "- 60 gün getiri / olasılık tablosu ve yönsüz işlem BİLGİDİR (yön tahmini yok).", "- Hayatta kalma: evren bugünün listesi; batanlar yok.", ""]
    for ad, _ev in _SO_TANIM:
        s += [f"## KAT tablosu — {ad} (karar günü t'den 20 gün; eş 1 / eş 2)", "",
              "| Pazar | Dönem | sonuç | n (eş1/eş2) | olay % | eş1 % | KAT eş 1 [%95] | eş2 % | KAT eş 2 [%95] | hücre |", "|---|---|---|---|---|---|---|---|---|---|"]
        for p in E["karar_pazar"] + E["bilgi_pazar"]:
            if p not in J["pazarlar"]:
                continue
            for d in D + list(E["birlesik"]):
                for b in E["sonuc"]["ana"] + E["sonuc"]["bilgi"]:
                    r1, r2 = kat(p, d, b, "es1", ad), kat(p, d, b, "es2", ad)
                    if r1 is None:
                        continue
                    s.append(f"| {p} | {d} | {b} | {int(r1['n'])}/{int(r2['n']) if r2 is not None else 0} | {yz(r1['p_olay'])} | {yz(r1['p_es'])} | {kt(r1)} | "
                             f"{yz(r2['p_es']) if r2 is not None else '-'} | {kt(r2)} | {J['karar'][ad][b]['hucre'].get(f'{p} {d}', '-')} |")
        s.append("")
    s += ["## Cemal'in sorusu — bölge SONUNDAN sonraki 20 gün (BİLGİ; eş = bölge sonu günü, aynı σ250 x likidite hücresi, S5 dışı)", "",
          "A3 = yıllık ATR'nin 3 katı mum (TR/C_önceki), A2 = 2 katı; M3 / M2 = sıkışma mumunun (zıplama hariç medyan, bölge sonu penceresi) 3 / 2 katı mum ((H-L)/C_önceki).", "",
          "| Pazar | Dönem | tanım | ölçü | n | olay % | eş % | KAT [%95] | bölge boyu medyan (gün) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in BS.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['donem']} | {r['sikisma']} | {r['olcu']} | {r['n']} | {yz(r['p_olay'])} | {yz(r['p_es'])} | {kt(r)} | {s2(r.get('bolge_gun_medyan'), 0)} |")
    s += ["", "## (B) Zaman ve yön (eş 1 satırları)", "",
          "| tanım | Pazar | Dönem | sonuç | n | büyük hareketli | ilk gün medyan [%25-%75] | yukarı payı (eş) | 1-5 / 6-10 / 11-15 / 16-20 olay % (eş %) |", "|---|---|---|---|---|---|---|---|---|"]
    for r in B.to_dict("records"):
        fw = "f" if r["olcu"] == "B1" else "h"
        pen = " / ".join(f"{yz(r.get(f'p_{fw}{w}'))} ({yz(r.get(f'es_p_{fw}{w}'))})" for w in range(1, 5))
        s.append(f"| {r['sikisma']} | {r['pazar']} | {r['donem']} | {r['olcu']} | {r['n']} | {r['n_olay']} | {s2(r.get('k_medyan'), 0)} [{s2(r.get('k_q25'), 0)}-{s2(r.get('k_q75'), 0)}] | "
                 f"{yz(r.get('yukari_pay'), 0)} ({yz(r.get('es_yukari_pay'), 0)}) | {pen} |")
    s += ["", "## (C) Yönsüz stoplu kırılım işlemi (SY (C) kuralı aynen; BİLGİ)", "",
          "| tanım | Pazar | Dönem | olay | işlem | işlem oranı | ort getiri | medyan | ort eş | ort fark [%95] | sıra | portföy / plasebo p90 | P(+%20 önce) / P(-%10 önce) (eş) | karar |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in C.to_dict("records"):
        s.append(f"| {r['sikisma']} | {r['pazar']} | {r['donem']} | {r['n_olay']} | {r['n']} | {yz(r.get('islem_orani'), 0)} | {yz(r.get('ort_r'))} | {yz(r.get('medyan_r'))} | "
                 f"{yz(r.get('ort_es_r'))} | {yz(r.get('ort_fark'))} [{yz(r.get('alt95'))}, {yz(r.get('ust95'))}] | {s2(r.get('sira'))} | "
                 f"{yz(r.get('portfoy'), 0)} / {yz(r.get('port_es_p90'), 0)} | {yz(r.get('p_ilk20'), 0)} / {yz(r.get('p_ilk10'), 0)} "
                 f"({yz(r.get('es_p_ilk20'), 0)} / {yz(r.get('es_p_ilk10'), 0)}) | {r.get('karar')} |")
    for ad, v in J.get("oc", {}).items():
        s += ["", v["rapor"]]
    s += ["", "## Geleceğe bakma denetimi (koşu içinde)", ""] + [f"- {p}: {v['gelecek_denetimi_olay']} olayda seri t'de kesildi, S5 / sınıf / ATR / likidite aynı (TUTTU)"
                                                               for p, v in J["denetim"].items()]
    dy = _so_yol("denetim", cikti)
    if os.path.exists(dy):
        Dn = json.load(open(dy, encoding="utf-8"))
        s += ["", "## Denetim (koşudan sonra, ayrı kod)", ""] + [f"- {x}" for x in Dn.get("satirlar", [])]
    s += ["", "## Sınırlar", "", "- Evren bugünün listesi (V_*.pkl; OC'de ABD + k34): batan / kottan çıkan yok; büyük hareket olasılığı olay ve eşte birlikte etkilenir, "
          "işlem getirisi yukarı yanlı.", "- Tanım 7 BIST örneğine göre kaba ızgarada ayarlandı (aşırı uyum riski); ABD / AVR ileri sınamadır.",
          "- Bilanço takvimi yok. Komisyon / kayma / açığa satış maliyeti yok.", "- BIST ±%10 fiyat sınırı tek günlük büyük mumu kısar; BIST bilgi.",
          "- Bölge sonu ölçüsü geleceğe ait bilgiyle (bölgenin bittiği gün) kurulur: karar ölçüsü değildir, Cemal'in sorusuna düz sayıdır.",
          "- 31.08.2026 sonrası fiyat yok (fon krizi kesiği)."]
    metin = "\n".join(s)
    if _SO_EPOSTA.search(metin):
        raise SOHata("raporda e-posta biçimli parça var")
    with open(_so_yol("rapor", cikti), "w", encoding="utf-8") as f:
        f.write(metin + "\n")
    return metin


# ---------------------------------------------------------------- 10) CEMAL'İN GÖZÜ İÇİN LİSTE (BIST, ekran fiyatı)
def _so_bolge_satir(s: str, d: pd.DataFrame, X: pd.DataFrame, i: int, e: int, p: int, sicrama: float) -> Dict[str, Any]:
    """Liste satırı (gösterim; ölçüm değil). i = karar günü, e = bölge sonu. Sonraki 20 gün bölge SONUNDAN."""
    C = d.Close.to_numpy(float); H = d.High.to_numpy(float); L = d.Low.to_numpy(float); ek = d.ekran.to_numpy(float)
    n = len(C); a = i - p + 1; b = min(n - 1, e + 20)
    Cp = np.r_[np.nan, C[:-1]]
    if e + 1 <= n - 1:
        rng_ = (H[e + 1:b + 1] - L[e + 1:b + 1]) / Cp[e + 1:b + 1]; j = int(np.argmax(rng_)); bm = float(rng_[j]); bt = d.index[e + 1 + j]
    else:
        bm, bt = float("nan"), None
    sik = float(X.mmed.iat[e]); atr = float(X.atr5.iat[e])
    gr = np.abs(C[max(a, 1):b + 1] / Cp[max(a, 1):b + 1] - 1)
    return {"hisse": s, "sinif": "DİP" if bool(X.s5c_dip.iat[i]) else "YOL", "pencere_bas": str(d.index[a].date()), "karar": str(d.index[i].date()),
            "bolge_son": str(d.index[e].date()), "bolge_gun": int(e - i + 1), "bant_alt": float(np.min(ek[a:e + 1])), "bant_ust": float(np.max(ek[a:e + 1])),
            "obek": float(X.obek.iat[i]), "sik_mum": sik, "bb_yuzdelik": float(X.bbp.iat[i]), "egim": float(X.egim.iat[i]), "konum": float(X.konum.iat[i]),
            "en_buyuk_mum": bm, "en_buyuk_tarih": str(bt.date()) if bt is not None else "-", "kat_sik": bm / sik if sik > 0 else float("nan"),
            "kat_atr": bm / atr if atr > 0 else float("nan"), "g20": float(C[b] / C[e] - 1) if b > e else float("nan"), "gun_sonra": int(b - e),
            "en_yuksek": float(np.max(H[e + 1:b + 1]) / C[e] - 1) if b > e else float("nan"),
            "en_dusuk": float(np.min(L[e + 1:b + 1]) / C[e] - 1) if b > e else float("nan"),
            "sicrama": bool(np.nanmax(gr) > sicrama) if len(gr) else False}


def _so_bolge_md(R: List[Dict[str, Any]], tur: bool = False) -> List[str]:
    s = ["| hisse | " + ("örnek | " if tur else "") + "sınıf | pencere_bas | karar (ilk gün) | bölge son | gün | bant_alt | bant_ust | öbek | sık mum | BB yüzdelik | eğim | konum120 | "
         "en büyük mum (tarih) | x sık mum | x ATR | g20 | en yüksek | en düşük |",
         "|---|" + ("---|" if tur else "") + "---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in R:
        f = lambda x, k=1: "-" if x is None or not math.isfinite(x) else f"%{x * 100:+.{k}f}"   # noqa: E731
        u = lambda x, k=1: "-" if x is None or not math.isfinite(x) else f"%{x * 100:.{k}f}"    # noqa: E731
        g20 = f(r["g20"]) + ("" if r["gun_sonra"] >= 20 else f" ({r['gun_sonra']} gün)")
        if r.get("sicrama"):
            g20 += " (>%11 gün: bedelli / bölünme şüphesi)"
        s.append(f"| {r['hisse']} | " + (f"{r.get('tur', '')} | " if tur else "") + f"{r['sinif']} | {r['pencere_bas']} | {r['karar']} | {r['bolge_son']} | {r['bolge_gun']} | "
                 f"{r['bant_alt']:.4g} | {r['bant_ust']:.4g} | {u(r['obek'])} | {u(r['sik_mum'])} | {r['bb_yuzdelik']:.2f} | {f(r['egim'])} | {r['konum']:.2f} | "
                 f"{u(r['en_buyuk_mum'])} ({r['en_buyuk_tarih']}) | {SC._sc_s(r['kat_sik'], 1)} | {SC._sc_s(r['kat_atr'], 1)} | {g20} | {f(r['en_yuksek'])} | {f(r['en_dusuk'])} |")
    return s


def so_liste(cikti: Optional[str] = None, yahoo: Optional[str] = None, E: Optional[Dict[str, Any]] = None) -> str:
    """BIST 2025-01..2026-08 S5 bölgeleri, ekran fiyatı: sayılar, rastgele 7 hisse x ardışık 3 bölge, bölge sonu + 20 gün en iyi / en kötü 10, 7 tasarım örneği."""
    E = E or SO_ESIK; Ls = E["liste"]; p = int(E["S5"]["secilen"]["p"])
    import TAVAN_SERISI as TS
    S, _m = TS.ts_fiyatlar(yahoo or SO_YOL["yahoo"])
    Dd, Xs, liq = {}, {}, []
    for s_, d0 in S.items():
        try:
            d = SC._sc_yahoo_sy(d0)
            if len(d) < E["gecmis_min"] + 25:
                continue
            G = SY.sy_gecmis(d, "BIST", SY.SY_ESIK); X = so_s5(d, "BIST", None, E)
            X["sup"] = SY._sy_pencere_var(SY.sy_bolunme_supheli(d.Close.to_numpy(float), SY.SY_ESIK), *E["bolunme_gecmis"])
            X["bs_i"] = so_bolge_sonu(X.ev5.to_numpy(), X.s5c.to_numpy(), E["S5"]["ara"])
            Dd[s_], Xs[s_] = d, X
            liq.append(pd.DataFrame({"sembol": s_, "tarih": d.index, "liq": G.liq.to_numpy()}))
        except Exception as ex:
            solog.warning("liste %s atlandı: %s", s_, ex)
    Lq = pd.concat(liq, ignore_index=True); Lq["pct"] = Lq.groupby("tarih").liq.rank(pct=True)
    Lq = Lq.set_index(["sembol", "tarih"]).pct
    R: List[Dict[str, Any]] = []
    for s_, X in Xs.items():
        d = Dd[s_]
        for i in np.where(X.ev5.to_numpy())[0]:
            t = d.index[i]
            if not (pd.Timestamp(Ls["bas"]) <= t <= pd.Timestamp(Ls["son"])) or X.sup.iat[i]:
                continue
            lp = Lq.get((s_, t), np.nan)
            if not (np.isfinite(lp) and lp > SY.SY_ESIK["likidite"]["alt_kesik"]):
                continue
            R.append(_so_bolge_satir(s_, d, X, int(i), int(X.bs_i.iat[i]), p, Ls["sicrama"]))
    Rd = pd.DataFrame(R)
    rng = np.random.default_rng(Ls["tohum"])
    adaylar = sorted(Rd.groupby("hisse").size().loc[lambda x: x >= Ls["ardisik"]].index) if len(Rd) else []
    sec = list(rng.choice(adaylar, min(Ls["rastgele_hisse"], len(adaylar)), replace=False)) if adaylar else []
    A_ = [r for h in sec for r in sorted([r for r in R if r["hisse"] == h], key=lambda r: r["karar"])[:Ls["ardisik"]]]
    tam = [r for r in R if r["gun_sonra"] >= 20 and not r["sicrama"]]
    iyi = sorted(tam, key=lambda r: -r["g20"])[:Ls["en_iyi"]]; kotu = sorted(tam, key=lambda r: r["g20"])[:Ls["en_iyi"]]
    # tasarım örnekleri: örnek aralığıyla kesişen bölgeler (yoksa 'S5 yok')
    T_ = []
    for o in SO_ORNEK:
        if o["sembol"] not in Xs:
            continue
        d, X = Dd[o["sembol"]], Xs[o["sembol"]]
        bul = False
        for i in np.where(X.ev5.to_numpy())[0]:
            e = int(X.bs_i.iat[i])
            if d.index[i] <= pd.Timestamp(o["son"]) and d.index[e] >= pd.Timestamp(o["ilk"]):
                r = _so_bolge_satir(o["sembol"], d, X, int(i), e, p, Ls["sicrama"]); r["tur"] = f"{o['ad']} ({'SEÇ' if o['secmeli'] else 'SEÇME'})"; T_.append(r); bul = True
        if not bul:
            T_.append({"hisse": o["sembol"], "tur": f"{o['ad']} ({'SEÇ' if o['secmeli'] else 'SEÇME'}) {o['ilk']}..{o['son']}: S5 BÖLGESİ YOK"})
    sinif = Rd.sinif.value_counts().to_dict() if len(Rd) else {}
    sc_ = E["S5"]["secilen"]
    s = ["# Öbek sıkışması (S5) bölgeleri (BIST, Ocak 2025 - Ağustos 2026) — Cemal'in kendi grafiğinde bakması için", "",
         f"Tanım (S5, p = {p}): (a) son {p} günün en büyük mumu çıkarılınca kalan mumların medyanı (H-L)/C <= {sc_['k_m']} x yıllık ortalama mum (ATR250); "
         f"(b) bir uç gün hariç kapanışlar %{sc_['bant']['BIST'] * 100:.0f} bant içinde (öbek); (c) eğim -%2 .. +%10; (d) aşağı açılış günleri <= yarı; "
         f"(e) Bollinger (20, 2σ) genişliği son 250 günün en dar %{sc_['bb'] * 100:.0f}'sinde (ŞART); "
         + ("(f) pencere yeter. " if str(sc_["uzunluk"]) == "p" else "(f) (a)+(b)+(e) en az 10 gündür. ")
         + "SINIF DİP: 120 günlük aralığın alt çeyreğinde ve tepeden en az %10 aşağıda. SINIF YOL ÜSTÜ: SMA50 üstünde, SMA50 yükseliyor, 120 günlük "
         "aralığın üst %40'ında, taban korunuyor (pencerenin dibi ilk 5 günün dibinin %1'den fazla altına inmiyor). Bölge = koşulun ilk sağlandığı "
         "gün (karar) .. son sağlandığı gün; aynı hissede yeni bölge en az 20 gün sonra. Likidite alt %20 dışarıda. Fiyatlar ekran fiyatı.",
         "Sütunlar: pencere_bas = karar gününün penceresinin ilk günü; gün = bölge boyu (karar .. bölge son, işlem günü); bant_alt / bant_ust = pencere_bas .. "
         "bölge son kapanış aralığı; öbek = karar günü bir uç gün hariç bant; sık mum = bölge sonundaki zıplama hariç medyan mum; eğim = karar günü pencere "
         "eğimi; en büyük mum = bölge SONUNDAN sonraki 20 günün en büyük mumu (gün aralığı / önceki kapanış); x sık mum / x ATR = bu mumun sıkışma mumuna / "
         "yıllık ortalama muma oranı; g20 / en yüksek / en düşük = bölge sonu kapanışına göre 20 gün.",
         f"**Sayı:** {len(R)} bölge ({len(set(r['hisse'] for r in R))} hisse); DİP {sinif.get('DİP', 0)}, YOL ÜSTÜ {sinif.get('YOL', 0)}. Bölge sonundan 20 günü "
         f"tamamlanan ve tek günde > %11 değişim olmayan {len(tam)} (>%11 olan {sum(1 for r in R if r['sicrama'])}: bedelli / bölünme şüphesi).", "",
         f"## A. Rastgele {len(sec)} hisse (tohum {Ls['tohum']}; en az {Ls['ardisik']} bölgesi olanlardan), her birinde ARDIŞIK ilk {Ls['ardisik']} bölge ({len(A_)} satır)", ""]
    s += _so_bolge_md(A_)
    s += ["", f"## B. Bölge sonundan 20 gün getirisi EN İYİ {len(iyi)} ({len(tam)} bölge içinde; >%11 günü olanlar dışarıda)", ""] + _so_bolge_md(iyi)
    s += ["", f"## C. EN KÖTÜ {len(kotu)}", ""] + _so_bolge_md(kotu)
    s += ["", "## D. 7 tasarım örneğinin satırları (örnek aralığıyla kesişen S5 bölgeleri)", ""]
    s += _so_bolge_md([r for r in T_ if "karar" in r], tur=True)
    s += [""] + [f"- {r['tur']}" for r in T_ if "karar" not in r]
    s += ["", "## E. Bütün bölgeler (sınıf, ilk - son gün)", "", "| hisse | sınıf | karar (ilk gün) | bölge son | gün |", "|---|---|---|---|---|"]
    s += [f"| {r['hisse']} | {r['sinif']} | {r['karar']} | {r['bolge_son']} | {r['bolge_gun']} |" for r in sorted(R, key=lambda r: (r["hisse"], r["karar"]))]
    s += ["", "Not: liste ölçüm değildir; Cemal'in gözle kıyası içindir. Hayatta kalma: yalnız bugün işlem gören hisseler."]
    metin = "\n".join(s)
    if _SO_EPOSTA.search(metin):
        raise SOHata("listede e-posta biçimli parça var")
    yol = _so_yol("liste", cikti)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin + "\n")
    solog.info("liste yazıldı: %s (%d bölge)", yol, len(R))
    return yol


# ---------------------------------------------------------------- 11) ÇAKIŞMA KAPISI
def _cakisma_kontrol_so(_once=_CK_ONCE_SO, _dosya="SIKISMA_OBEK.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_SO", "_CK_KAYIT", "_cakisma_kontrol_so", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "itertools", "zlib", "warnings", "_dt", "OC", "SY", "SC",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_so()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=SO_SURUM)
    ap.add_argument("komut", choices=["tasarim", "onkayit", "kos", "rapor", "liste"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true", help="onkayit: git'e İŞLENMEMİŞ ön kaydı yeniden yaz")
    a = ap.parse_args()
    try:
        if a.komut == "tasarim":
            J_ = so_tasarim(a.veri, cikti=a.cikti)
            print(json.dumps({k: J_[k] for k in ("en_cok_tutan", "toplam", "tam_tutan_nokta", "aday_nokta", "secilen")}, ensure_ascii=False))
        elif a.komut == "onkayit":
            print(so_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = so_kos(a.cikti, a.veri)
            print(json.dumps(SC._sc_temiz(R_["sonuc"]["karar"]), ensure_ascii=False, indent=1))
        elif a.komut == "liste":
            print(so_liste(a.cikti))
        else:
            print(so_rapor(a.cikti))
    except (SOHata, OC.OCHata) as ex:
        solog.error("%s", ex); sys.exit(1)
