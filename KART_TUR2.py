"""KART_TUR2 — KART TURU 2: en basit fiyat-hacim kartları, GENİŞ TEZGÂH (TEZGAH2: ABD + AVR, 2000-2023 açık), P2 olay havuzu, R15 / R30
karar ufku, KASA 2 ile yürüyen ileri test (2024Q1 .. 2026Q4; karar bakışı 4., 8. ve 12. blokta). 22 Kasım 2026.

İş tanımı: arastirma_cikti/kart2/KART_TUR2_IS_TANIMI.md (ANA MODEL KARARLARI aynen K2_ESIK['kararlar']'da).

DÜZEN (aynı kod hem açık veride hem açılmış bloklarla çalışır):
  python KART_TUR2.py hazirla --veri /tmp/kasa2/acik [--islem 4]
      Açık veride (KASA 2 kesik 2023-12-31; blok açılmamış) bütün kart sinyallerini bir kez hesaplar -> /tmp/kart2_onbellek/ (repo dışı;
      sha'lar ön kayıtta), PREFIX TESTİ (veri 2022-06-30'da kesilince <= 2022-05-31 sinyal, bayrak, özellik ve P2 olay kümeleri BİREBİR;
      tutmazsa DURUR) ve GÜÇ EĞRİLERİ (yapay iz +0,5 / +1 / +2 puan, P2 havuzu) -> arastirma_cikti/kart2/k2_prefix.json, k2_guc.json.
  python KART_TUR2.py olc --veri /tmp/kasa2/acik --cikti <klasör> [--islem 4]
      Veri klasöründe ne varsa onunla bütün kartları ölçer. Hücreler 'acik_d1' (giriş 2001-07), 'acik_d2' (2008-15), 'acik_d3' (2016-23),
      açılmış her çeyrek ('2024Q1', ...) ve 'birikimli' (giriş >= 2024-01-01). Açık hücreler DONDURULMUŞTUR: giriş <= 2023-12-31 olan bir
      hisse-günün R_H'si yalnız H. barı da <= 2023-12-31 ise ölçülür (olay ve eş için aynı) -> açık tablo her koşuda bayt bayt aynı (yeniden
      üretim kapısı). Kapılar: KASA 2 (KASA_DURUM, mühür, V_*.pkl -> V_*2.pkl bağlantısı, KASA.kasa_kapisi en geç tarih <= açık kesik), blok
      açıkken ön kayıt (KASA.ks_onkayit_kapi 'KART_TUR2' + BAGIMLI_SHA + K2_ESIK_SHA + ACIK_TABLO_SHA + GUC_SHA + OLAY_ACIK_SHA), önbellek
      tutarlılığı, yeniden üretim (iki hücre satır dosyasından + açık hücreler kuru koşu tablosuyla birebir), çıktı en geç tarih <= kesik;
      aynı klasöre ikinci koşu DURUR. KARAR BAKIŞI yalnız açılmış blok sayısı 4, 8, 12 iken (Bonferroni: boot %98,33, BH q 0,10 / 3).
  python KART_TUR2.py onkayit        açık kuru koşu + hazırlık çıktılarından KART_TUR2_ON_KAYIT.md
  python KART_TUR2.py sha            kod / eşik / bağımlı dosya sha'ları
Kart bayrakları YALNIZ açık fiyat verisinden, mevcut modül fonksiyonlarıyla (YAPI_HEDEF, GOZ_ETIKET, DUSUS_SONRASI, BOFA_IZI, D9_YENIDEN,
OLCU_SINAMA, TEZGAH2_DOGRULAMA, KART_TUR1) yeniden hesaplanır; repo içindeki eski olay / sonuç dosyaları OKUNMAZ. Bu modüller DEĞİŞTİRİLMEZ.
Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
Colab: exec(open('KART_TUR2.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Test:  python test_kart_tur2.py (yalnız sentetik veri)
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_K2 = {k: id(v) for k, v in globals().items()}

import argparse  # noqa: E402
import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

KOK_K2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_K2 not in sys.path:
    sys.path.insert(0, KOK_K2)

import DUSUS_SONRASI as DS  # noqa: E402
import GOZ_ETIKET as GE  # noqa: E402
import KART_TUR1 as KT  # noqa: E402
import KASA as KS  # noqa: E402
import OLCU_SINAMA as OS  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import TEZGAH2_DOGRULAMA as T2  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

k2log = logging.getLogger("col.kart_tur2")
if not k2log.handlers:
    _k2_h = logging.StreamHandler(sys.stderr)
    _k2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s kart_tur2: %(message)s", "%H:%M:%S"))
    k2log.addHandler(_k2_h)
    k2log.setLevel(logging.INFO)
    k2log.propagate = False


class K2Hata(RuntimeError):
    """Durdurucu hata: kasa / ön kayıt kapısı, veri yok, prefix / önbellek / yeniden üretim tutmadı, sha tutmuyor, ikinci koşu, kesik aşımı."""


K2_SURUM = "KART_TUR2 v1.0 (2026-11-22): 14 kart (KT00 / KT13 kontrol + KT01-KT12), geniş tezgâh P2, R15 / R30 karar, KASA 2 yürüyen ileri test"
K2_HIPOTEZ = "KART_TUR2"
K2_YOL = {"cikti": os.path.join(KOK_K2, "arastirma_cikti", "kart2"), "kod": os.path.join(KOK_K2, "KART_TUR2.py"),
          "onkayit": os.path.join(KOK_K2, "arastirma_cikti", "kart2", "KART_TUR2_ON_KAYIT.md"),
          "is_tanimi": os.path.join(KOK_K2, "arastirma_cikti", "kart2", "KART_TUR2_IS_TANIMI.md"),
          "acik": os.path.join(KOK_K2, "arastirma_cikti", "kart2", "acik"),
          "prefix": os.path.join(KOK_K2, "arastirma_cikti", "kart2", "k2_prefix.json"),
          "guc": os.path.join(KOK_K2, "arastirma_cikti", "kart2", "k2_guc.json"),
          "hazirlik_t2": os.path.join(KOK_K2, "arastirma_cikti", "tezgah2", "tezgah2_hazirlik.json"),
          "manifest": os.path.join(KOK_K2, "arastirma_cikti", "kasa", "KASA2_MANIFEST.json"),
          "onbellek": os.environ.get("K2_ONBELLEK", "/tmp/kart2_onbellek"), "kasa_dizin": "/tmp/kasa2", "veri": "/tmp/kasa2/acik"}
K2_DOSYA = {"satir": "k2_satir.csv.gz", "hucre": "k2_hucre.csv", "karar": "k2_karar.csv", "huni": "k2_huni.json", "sonuc": "k2_sonuc.json",
            "meta": "k2_meta.json", "rapor": "KART_TUR2_SONUC.md"}
K2_BAGIMLI = ["KART_TUR1.py", "YAPI_HEDEF.py", "GOZ_ETIKET.py", "DUSUS_SONRASI.py", "BOFA_IZI.py", "D9_YENIDEN.py", "ORTAK_CETVEL.py",
              "OLCU_SINAMA.py", "TEZGAH2_DOGRULAMA.py", "TEZGAH_DOGRULAMA.py", "KASA.py", "S6_TABAN.py", "SIKISMA_YENIDEN.py", "CETVEL2.py",
              "POZITIF_KONTROL.py", "sektor_ABD.csv", os.path.join("arastirma_cikti", "tezgah2", "tezgah2_hazirlik.json"),
              os.path.join("arastirma_cikti", "kasa", "KASA2_MANIFEST.json"), os.path.join("arastirma_cikti", "k55_dallanma", "K55_EVREN_DISI.csv")]
K2_PAZAR = ["ABD", "AVR"]
K2_GRUP = ["Y1", "DS", "BOFA", "D9", "MOM", "STREV"]
K2_ACIK_SON = pd.Timestamp("2023-12-31")
K2_BLOK_BAS = pd.Timestamp("2024-01-01")

# ================================================================ MÜHÜRLÜ KART SÖZLÜĞÜ (sha ön kayıtta; sonuç görüldükten sonra DEĞİŞMEZ)
_Y11E = YH.YH_ESIK["denemeler"]["Y11"]["esik"]
_S10E = YH.YH_ESIK8["esik"]


def _kt1(kod: str, **ek: Any) -> Dict[str, Any]:
    v = {k: KT.KT_KART[kod][k] for k in ("yon", "cumle", "tanim", "esik", "kaynak")}
    v.update(ek)
    return v


K2_KART: Dict[str, Dict[str, Any]] = {
    "KT00": _kt1("KT00", grup="MOM", bayrak="F_KT00", pazar=["ABD", "AVR"], karar=False,
                 uyarlama="KART_TUR1 tanımı (12-1 momentum, ay sonu, üst onda) aynen; sıra P2 havuzunda (giriş günü d'de P2 ve değeri sonlu "
                          "hisseler, OS.os_kart_sinyal düzeni: t = ay sonu, d = hissenin sonraki geçerli barı, boşluk <= 10); KART_TUR1'in 'ANA = U "
                          "ya da A, 15 bar' kuralı yerine cetvel tekili (H); yalnız BİLGİ"),
    "KT01": _kt1("KT01", grup="Y1", bayrak="F_KT01", pazar=K2_PAZAR, karar=True,
                 uyarlama="S6 'al' -> OC.oc_olay_hazirla (giriş, P2 havuzu, 60 gün tekil) = Y1 OLAYI"),
    "KT02": _kt1("KT02", grup="Y1", bayrak="F_KT02", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş1"),
    "KT03": _kt1("KT03", grup="Y1", bayrak="F_KT03", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş3"),
    "KT04": _kt1("KT04", grup="Y1", bayrak="F_KT04", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş5"),
    "KT05": _kt1("KT05", grup="Y1", bayrak="F_KT05", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş4"),
    "KT06": _kt1("KT06", grup="Y1", bayrak="F_KT06", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş7"),
    "KT07": _kt1("KT07", grup="Y1", bayrak="F_KT07", pazar=K2_PAZAR, karar=True, uyarlama="Y1 olayı (P2) VE Ş1 VE Ş3 VE Ş5"),
    "KT08": _kt1("KT08", grup="DS", bayrak="F_KT08", pazar=K2_PAZAR, karar=True,
                 uyarlama="DS durum bayrağı DUSUS_SONRASI.ds_ozellik_hisse 's_ds' satırlarının satır satır kopyası (yalnız durum; özellik döngüsü "
                          "atlanır; eşitlik testte ve hazırlıkta örneklemle denetlenir) -> DS.ds_olay_kur (OC giriş, P2 havuzu, ANA 15 bar) VE "
                          "F15 <= 0,05 VE r5 <= -0,03 (KART_TUR1.kt_f15_r5)"),
    "KT09": _kt1("KT09", grup="BOFA", bayrak="F_KT09", pazar=["ABD", "AVR"], karar=True,
                 uyarlama="BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum aynen (kendi okuyucusu); kurulum günü -> OC.oc_olay_hazirla (giriş, P2, tekil 1; "
                          "60 bar ayrılık kurulum tanımında)"),
    "KT10": _kt1("KT10", grup="D9", bayrak="F_KT10", pazar=["ABD"], karar=True,
                 uyarlama="D9_YENIDEN.d9_durum hesabı (KART_TUR1.kt_d9_durum kopyası) aynen; tek fark dönem penceresi: D9_ESIK olay_bas "
                          "2015-06-01 D9 çalışmasının dönemi (kart tanımı değil) -> 2000-01-01; rüzgâr evreni = tezgâh evreni (OS.os_veri; k34 "
                          "kasada yok); d9_satir 'c' -> OC.oc_olay_hazirla (giriş, P2, tekil 1) -> cetvel tekili (H); AVR sektör listesi yok"),
    "KT11": {"grup": "Y1", "bayrak": "F_KT11", "yon": "+", "pazar": K2_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş9 U DİP (YAPI_HEDEF 5. tur Y11c tanımı) eşlerinden iyi",
             "tanim": "Y1 olayı VE Ş9: W = t'den önceki son 40 geçerli barın Low'u, L ≈ a x² + b x + c; F24 = a / ATR > 0 VE 0,20 <= F25 = x* / 39 "
                      "<= 0,75 VE F26 = R² >= 0,40 VE F27 >= 1,0 VE F28 >= 0,5 VE |F29| <= 5 (NaN tutmaz; YAPI_HEDEF Ş9 tanımı aynen)",
             "esik": f"YH_ESIK['denemeler']['Y11']['esik'] = {_Y11E}",
             "kaynak": "YAPI_HEDEF.yh_s9_ozellik (F24-F29, 6 anlamlı basamak) + yh_s9_sartlar['S9']",
             "uyarlama": "Y1 olayı (P2) VE Ş9; Y11 (Ş1 + Ş2 + Ş9) değil, iş tanımındaki 'Y1 ∧ Ş9' = Y11c kümesi"},
    "KT12": {"grup": "Y1", "bayrak": "F_KT12", "yon": "+", "pazar": K2_PAZAR, "karar": True,
             "cumle": "Y1 ∧ Ş10 MACD POZİTİF UYUMSUZLUK (YAPI_HEDEF 8. tur Y13) eşlerinden iyi",
             "tanim": "Y1 olayı VE Ş10: [t-60, t-1] içinde 5/5 salınım dipleri L1 < L2 (L1 <= L2 - 8); s65 = Low(L2) <= Low(L1) x 1,01 VE s66 = "
                      "MACD(L2) > MACD(L1) VE MACD(L2) < 0 (MACD 12/26/9, [t-250, t] barları; YAPI_HEDEF Ş10 tanımı aynen)",
             "esik": f"YH_ESIK8['esik'] F65_ust {_S10E['F65_ust']}, F66_alt_acik {_S10E['F66_alt_acik']}, F66m_ust_acik {_S10E['F66m_ust_acik']}",
             "kaynak": "YAPI_HEDEF.yh_s10_ozellik ('S10' bayrağı) = yh_s10_maske('Y13')",
             "uyarlama": "Y1 olayı (P2) VE S10 == 1"},
    "KT13": {"grup": "STREV", "bayrak": "F_KT13", "yon": "+", "pazar": ["ABD", "AVR"], "karar": False,
             "cumle": "KONTROL KARTI: kısa vadeli dönüş (son 21 gün getirisi alt onda) eşlerinden iyi. İz aramaz",
             "tanim": "ay sonu t, STREV = C_k / C_{k-21} - 1 (k >= 21; OLCU_SINAMA kart tanımı), giriş günü d'de P2 havuzunda ve değeri sonlu "
                      "hisseler arasında yüzde sıra <= 0,10 (alt onda)", "esik": "OS_ESIK['kart'] onda 0,10",
             "kaynak": "OLCU_SINAMA.os_kart_sinyal (STREV) + P2 sırası", "uyarlama": "yalnız BİLGİ; KT00 ile birlikte raporlanır"},
}

K2_ESIK: Dict[str, Any] = {
    "surum": "K2-1.0",
    "kararlar": (
        "(1) OLAY HAVUZU = P2 (`T2.t2_secili_panel(pazar, havuz='P2')`): tezgâh doğrulama kuralı piyasa serileri için P1'i seçti, ama kart ölçümü "
        "olay düzeyi 15-30 mum ortalamasıdır ve P1'in kuyruğu (R_15 > %300 olan 456 hisse-gün) ortalamayı anlamsız kılar; P2 36 hükmün 35'inde "
        "DOĞRU. Bu bir SAPMA notudur (kart sonucu görülmeden verildi). Eşler de yalnız P2 havuzundan. (2) ÖLÇÜ: R_H = H. geçerli bar kapanışı / "
        "t+1 açılış − 1, H = 15 ve 30 (karar); eş = aynı giriş günü, aynı pazar, OLCU_SINAMA KV1 kovası (ATRP tercili x likidite üçlüsü x F15 "
        "çeyreği; sınırlar tezgah2_hazirlik.json'daki sayılar), olay kümesi dışı, en az 5 eş; FARK = R_H − eş ortalaması; SIRA = eş dağılımındaki "
        "yüzdelik. Bilgi sütunları: medyan FARK, %1-%99 kırpılmış ortalama FARK, likidite üst yarı / alt yarı ayrı FARK. (3) HÜCRE TUTAR "
        "(beklenen yön +; − ise işaretler ters): n >= 30; ortalama FARK > 0 ve ay kümeli bootstrap (B 2000) alt ucu > 0; ortalama SIRA > 0,50 ve "
        "onun da boot alt ucu > 0,50; L3O (en iyi 3 ay çıkınca) FARK > 0; PLASEBO KAPISI (hücre, 200 tohum rastgele etiket: |ortalama FARK| < 0,5 "
        "puan ve yön başına tutar payı <= %7). (4) KARTLAR: KART_TUR1'deki tanımlar ve eşikler AYNEN (KT00 momentum yalnız bilgi; KT01 S6 taban "
        "kırılımı; KT02 dipte; KT03 dip savunulmuş; KT04 alt fitil az; KT05 küçük mum; KT06 gövdeli yakın tavan kırılımı; KT07 dip + savunma + "
        "alt fitil az; KT08 düşen bıçak (−); KT09 −%80 dip kurulumu; KT10 sektör rüzgârı yalnız sektörü bilinen ABD hisseleri) + üç yeni basit "
        "kart, tanımları mevcut kodda mühürlü: KT11 Y1 ∧ Ş9 U dip (YAPI_HEDEF Ş9 / Y11 eşikleri), KT12 Y1 ∧ Ş10 MACD pozitif uyumsuzluk (Y13 "
        "eşikleri), KT13 kısa vadeli dönüş kontrolü (son 21 gün getirisi alt onda, +; bilgi). Tanım koddan birebir alınamayan kart 'TANIM "
        "KURULAMADI' yazılır, uydurulmaz. Bayraklar yalnız açık fiyat verisinden hesaplanır; repo içindeki eski olay / sonuç dosyaları (2024+ "
        "satır içerir) OKUNMAZ. (5) YÜRÜYEN İLERİ TEST: KASA 2 blokları 2024Q1 .. 2026Q4 (12 blok) sırayla; her blok sonrası birikimli tablo "
        "(bilgi); KARAR BAKIŞI 4. blokta (2024 birikimli), 8. blokta ve 12. blokta; üç bakış için Bonferroni (boot güven düzeyi %98,33; p eşiği "
        "üçe bölünür). KART ETİKETİ (bakışta; karar hücreleri ABD ve AVR birikimli mühürlü dönem): İZ ADAYI = ABD ve AVR'de en az bir karar "
        "ufkunda TUTAR ve öteki ufukta aynı işaret ve açık verinin üç alt döneminin (2001-07, 2008-15, 2016-23) en az ikisinde aynı işaret, BH q "
        "0,10 (m = kart sayısı x 2 ufuk; KT00 / KT13 hariç); ABD-ADAY = yalnız ABD'de aynı şartlar (AVR güçsüz ya da veri yok); KATKI− = ters "
        "yönde aynı şartlar; ETKİ YOK = iki pazarda iki ufukta güç >= 0,80 (yapay iz eğrisinden, +1 puan için) ve boot aralığı tümüyle (−1, +1) "
        "puan içinde; ÖLÇÜLEMEDİ = güç yetersiz; SORGULA = geri kalan. KT00 / KT13 hükmü kartların etiketini DEĞİŞTİRMEZ (tezgâh korelasyonla "
        "doğrulandı); yalnız raporlanır."),
    "havuz": {"ad": "P2", "tanim": "TEZGAH2_DOGRULAMA T2_ESIK['havuz']['P2']: P1 (OS paneli ok VE H >= 0) VE d-1 kapanışı x Kur >= 2 USD (AVR 1 "
                                   "EUR) VE Lq (20 gün medyan işlem değeri, d-1'e kadar) >= 1 mn USD / EUR; panel = OS.os_veri + OS.os_panel(sinir = "
                                   "tezgah2_hazirlik.json) + T2.t2_havuz (= t2_secili_panel(pazar, havuz='P2') ile aynı hesap; KASA kapısı "
                                   "K2'nin kendi kapısı, çünkü t2_kasa_kapi açık kesiği 2023-12-31'e sabitler)"},
    "ufuk": {"karar": [15, 30], "pencere_kat": 2,
             "R": "R_H = giriş barından (giriş barı 1.) H. geçerli barın kapanışı / giriş barı açılışı E0 - 1; giriş satırından 2H birleşik takvim "
                  "satırında H geçerli bar yoksa ölçülmez (OS.os_olcu_hesap 'R' ile aynı; testte eşit)"},
    "es": {"kova": "KV1", "min": 5, "tanim": "aynı giriş günü d, aynı pazar, aynı KV1 kovası, P2 havuzunda, R_H ölçülebilir; aynı kartın o günkü "
                                              "olay kümesi (H tekilinden ÖNCE) ve olayın kendisi dışı; en az 5 eş (OS.os_havuz / OS.os_es)"},
    "tekil": {"Y1": "OC 60 gün (oc_olay_hazirla tekil_gun 60)", "DS": "ANA 15 bar (DS.ds_olay_kur)", "BOFA": "kurulum tanımında 60 bar",
              "D9": "yok (durum günleri)", "MOM": "yok (ay sonu)", "STREV": "yok (ay sonu)",
              "H": "sonra kart x H başına: aynı hissede birleşik takvimde >= H gün arayla ilk olay (OS.os_tekil kuralı); eş dışı küme tekil öncesi"},
    "hucre": {"acik_d1": ["2001-01-01", "2007-12-31"], "acik_d2": ["2008-01-01", "2015-12-31"], "acik_d3": ["2016-01-01", "2023-12-31"],
              "birikimli_bas": "2024-01-01", "acik_son": "2023-12-31",
              "tanim": "hücre = kart x pazar x H x giriş günü aralığı. acik_d1 / d2 / d3 (bilinen veri; DONDURULMUŞ: giriş <= 2023-12-31 olan "
                       "hisse-günün R_H'si H. barı > 2023-12-31 ise ölçülmez, olay ve eş için aynı -> 'acik_tasan'); açılmış her takvim çeyreği "
                       "(BİLGİ, plasebosuz, permütasyonsuz); 'birikimli' = giriş 2024-01-01 .. açık kesik (karar; plaseboyla). Fon krizi kesiği "
                       "31.08.2026 (OC.oc_veri_hazirla); H. barı veri sonunu aşan olay 'bekleyen' (sonraki blokta ölçülür), kriz kesiğini aşan "
                       "'kriz' (hiç ölçülmez)"},
    "boot": {"B": 2000, "tohum": 2291, "alt95": 0.025, "ust95": 0.975, "alt_bakis": 0.025 / 3, "ust_bakis": 1 - 0.025 / 3,
             "birim": "giriş ayı (ay toplamı ve sayısı yeniden örneklenir; FARK ve SIRA aynı ağırlıklarla)"},
    "perm": {"R": 10000, "tohum": 2292, "tanim": "ay kümeli işaret permütasyonu (FARK; beklenen yön ve ters yön tek yönlü p)"},
    "plasebo": {"tohum_sayi": 200, "tohum": 2293, "fark_esik": 0.005, "tutar_pay": 0.07,
                "tanim": "hücrenin her olayı için aynı giriş günü d'de P2 havuzundan (KV1 >= 0, R_H ölçülebilir) rastgele bir hisse (gün içinde "
                         "yerine koymadan); eş dışı küme = çekilen küme; aynı hücre kuralı; 200 tohum. GEÇER = |200 tohum ortalama FARK| < 0,005 VE "
                         "TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7. Plasebo hücreleri: açık alt dönemler (yalnız kuru koşuda; BİLGİ; açık tablo sha'lı) "
                         "ve birikimli (karar)"},
    "guc": {"delta": [0.005, 0.01, 0.02], "karar_delta": 0.01, "esik": 0.80, "tohum_sayi": 40, "tohum": 2294,
            "n": [30, 50, 100, 200, 300, 500, 1000, 2000, 5000],
            "pencere": {"1y": ["2023-01-01", "2023-12-31"], "2y": ["2022-01-01", "2023-12-31"], "3y": ["2021-01-01", "2023-12-31"],
                        "d1": ["2001-01-01", "2007-12-31"], "d2": ["2008-01-01", "2015-12-31"], "d3": ["2016-01-01", "2023-12-31"]},
            "bakis_pencere": {"1": "1y", "2": "2y", "3": "3y"},
            "tanim": "yapay iz: pencerenin P2 havuzundan (KV1 >= 0, R_H ölçülebilir; dondurulmuş R) yerine koymadan n hisse-gün; R_H + delta "
                     "(toplamsal: FARK tam delta kayar); eş dışı = çekilen küme; yakalama = hücre TUTAR(+) (plasebo hariç); 40 tohum. Pencere "
                     "1y / 2y / 3y bakış 1 / 2 / 3 için (boot %98,33), d1 / d2 / d3 açık alt dönemler için (boot %95). Gerçek kart olayları "
                     "aylara kümelenir; rastgele hisse-gün daha dağınıktır -> güç İYİMSER (rapor notu). Hücre gücü = eğrinin hücre n'inde "
                     "(log n doğrusal ara değer; n < 30 -> 0)"},
    "bakis": {"4": 1, "8": 2, "12": 3, "tanim": "KARAR BAKIŞI yalnız açılmış blok sayısı 4 (2024), 8 (2024-25) ve 12 (2024-26) iken; KASA_DURUM "
                                                  "'acilan' sırası 2024Q1'den kesintisiz; öteki blok sayılarında tablo BİLGİ (boot %95, BH q 0,10)"},
    "bh": {"q": 0.10, "q_bakis": 0.10 / 3,
           "tanim": "aile = karar kartları (KT01-KT12; KT00 / KT13 hariç) x karar ufku (15, 30) = 24 p. İki aile: (A) iki pazar p = karar "
                    "pazarlarının birikimli hücrelerinde en büyük ay kümeli permütasyon p (İZ ADAYI / KATKI−; KT10 yalnız ABD), (B) ABD p (ABD-ADAY "
                    "/ KATKI− yalnız ABD). Ters yön etiketi ters yön p'si ile ayrı BH"},
    "etiket": (
        "Karar hücresi c(k, H, P) = kart k, H in {15, 30}, P in {ABD, AVR} (KT10: yalnız ABD), birikimli. TUT(c) = hücre TUTAR (beklenen yönde, "
        "boot bakışta %98,33) VE plasebo GEÇER. İŞARET(c) = FARK beklenen işaretli. ALT(k, H, P) = acik_d1 / d2 / d3 hücrelerinden FARK'ı beklenen "
        "işaretli olanların sayısı. GÜÇLÜ(c) = n >= 30 VE güç(n; +1 puan; bakış penceresi) >= 0,80. İZ ADAYI <=> bir H1'de ABD ve AVR'de TUT VE "
        "öteki H2'de ABD ve AVR'de İŞARET VE ABD ve AVR'de ALT(k, H1) >= 2 VE (k, H1) BH (A) geçti. KATKI− <=> aynı şartlar ters yönde. ABD-ADAY "
        "<=> AVR veri yok (KT10) ya da AVR c(k, H1) GÜÇLÜ değil VE ABD'de aynı şartlar VE (k, H1) BH (B) geçti; ters yönde 'KATKI− (yalnız "
        "ABD)'. ETKİ YOK <=> bütün karar hücrelerinde GÜÇLÜ VE boot aralığı (bakış düzeyi) tümüyle (-0,01, +0,01) içinde. ÖLÇÜLEMEDİ <=> bir "
        "karar hücresi GÜÇLÜ değil. SORGULA <=> geri kalan. Sıra: İZ ADAYI, KATKI−, ABD-ADAY, KATKI− (yalnız ABD), ETKİ YOK, ÖLÇÜLEMEDİ, SORGULA. "
        "KONTROL (KT00, KT13; BH dışı, etiketleri değiştirmez): GÖRDÜ = bir H'de ABD ve AVR TUT; KISMEN = bir H'de ABD ve AVR İŞARET; aksi "
        "GÖRMEDİ. Bakış dışı bloklarda aynı hesap BİLGİ (boot %95, BH q 0,10)."),
    "prefix": {"kisa": "2022-06-30", "son": "2022-05-31",
               "tanim": "açık veri 2022-06-30'da kesilir: sinyal düzeyi (Y1 S6 sinyali + hat / tavan + F1-F29 + S10; DS durum günleri + f15 / r5; "
                        "BOFA kurulum; D9 'c' durum günleri) ve P2 olay düzeyi (kart x olay: sembol, tarih, giriş, d) <= 2022-05-31 olan BÜTÜN "
                        "satırlar tam açık veriyle hesaplananla BİREBİR (float tam eşit); değilse DURUR"},
    "onbellek": {"tanim": "açık kısım (<= 2023-12-31) sinyal tabloları /tmp/kart2_onbellek/sinyal_<pazar>.pkl; blok koşusunda Y1 özellikleri "
                          "yalnız yeni sinyaller (t > 2023-12-31) için hesaplanır; S6 taraması, DS, BOFA, D9 tüm seride yeniden yapılır ve "
                          "<= 2023-12-31 satırları önbellekle BİREBİR olmalı (değilse DURUR; tek istisna: BOFA kurulumu hissenin açık kısımdaki SON barındaysa açık veride "
                          "giriş barı olmadığı için dp_kurulum_tum yazmaz, blok açılınca yazılır: 'acik_son_bar' satırları ayrı sayılır); önbellek yoksa baştan hesaplanır ve tablo sha'sı "
                          "ön kayıttaki OLAY_ACIK_SHA ile aynı olmalı"},
    "yuvarlama": "Y1 özellikleri F1-F29 eşik karşılaştırmasından önce 6 anlamlı basamağa yuvarlanır (KART_TUR1 / YAPI_HEDEF dosya biçimi)",
    "d9_olay_bas": "2000-01-01",
    "ds_ornek": 200,
    "yeniden": [["KT01", "ABD", 15, "acik_d3"], ["KT08", "AVR", 30, "acik_d2"]],
    "veri": "yalnız --veri klasörü (KASA 2 açık kısmı): V_ABD.pkl -> V_ABD2.pkl, V_AVR.pkl -> V_AVR2.pkl; OS.os_veri (OC.oc_veri min_bar 1, k34 "
            "yok, evren dışı fon listesi, açılış H-L kırpması) bütün kartlar ve panel için; KT09 BOFA_IZI.dp_pkl_fiyat (kendi okuyucusu, aynı "
            "dosya). BIST bu turda yok",
}

K2_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı KV1 kovası (ATRP tercili x LQ3 x F15 çeyreği; sınırlar tezgah2_hazirlik.json), P2 "
                   "havuzu, aynı geometri (R_H stop'suz, aynı E0 / H); kartın o günkü olay kümesi ve olayın kendisi eş dışı, >= 5 eş (OS.os_es); "
                   "plasebo kapısı 200 tohum aynı gün rastgele P2 hissesi; KT00 / KT13 kontrol kartları; mekanik üstünlük yok (stop / hedef yok)"),
    "K2": ("EVET", "bayraklar yalnız t ve öncesi barlarla; PREFIX TESTİ (2022-06-30 kesik, <= 2022-05-31 sinyal + bayrak + özellik + P2 olay "
                   "kümeleri birebir; k2_prefix.json; tutmazsa DURUR); KASA 2 kapısı (en geç tarih <= açık kesik); açık hücreler dondurulmuş "
                   "(H. bar <= 2023-12-31); eski olay / sonuç dosyaları okunmaz; sektör ve evren listesi bugünkü (K7 / sınır)"),
    "K3": ("EVET", "OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0) + açılış kırpması; sinyal günü geçersiz bar ise "
                   "olay düşer (oc_olay_hazirla); R_H yalnız geçerli barlar, 2H satır kuralı"),
    "K4": ("EVET", "Y1 60 gün tekil (OC), DS ANA 15 bar, BOFA 60 bar ayrılık, sonra kart x H tekil (>= H gün); n = ölçülen olay; boot / "
                   "permütasyon birimi giriş ayı; medyan ve kırpılmış ortalama hücre tablosunda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla / os_kart_sinyal; boşluk <= 10 gün); eşler aynı gün açılışı"),
    "K6": ("EVET", "V_*2.pkl tek kip (auto_adjust; TEZGAH2_VERI); oranlar birimsiz; P2 fiyat / likidite eşiği Close x Kur (EUR); bölünme şüphesi "
                   "havuz dışı (OS nedensel kuralı); BOFA veri kırığı kuralı aynen"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok; ABD 2000 aktif = 2025'in %31'i); dipteki kartlarda (KT02, KT07, KT08, KT09) "
                   "yanlılık büyük; açık alt dönem işaretleri yukarı yanlı; raporda yazılı"),
    "K8": ("EVET", "hücre n >= 30 ve güç (yapay iz, +1 puan) >= 0,80 değilse ÖLÇÜLEMEDİ; güç tablosu (4 / 8 / 12 blokta beklenen n) ön kayıtta; "
                   "iki karar ufku + iki karar pazarı + üç açık alt dönem; BH q 0,10 (bakışta / 3) m 24; üç bakış Bonferroni"),
    "K9": ("EVET", "KART_TUR2_ON_KAYIT.md: K2_ESIK / K2_KART sha, KASA_KOD KART_TUR2.py sha, BAGIMLI_SHA tablosu, açık tablo / güç / prefix / "
                   "olay sha'ları, karar kuralı, bakış takvimi, güç tablosu; sıra kod commit -> açık kuru koşu -> ön kayıt commit -> (ana model) "
                   "blok aç -> olc; blok açıkken KASA.ks_onkayit_kapi + sha kapısı"),
    "K10": ("UYGULANMAZ", "ham haber / KAP / SEC ayrıştırması yok; yalnız OHLCV + sektor_ABD.csv"),
    "K11": ("EVET", "k2_yeniden: iki hücre (KT01 ABD R15 acik_d3, KT08 AVR R30 acik_d2) satır dosyasından düz pandas; blok koşusunda açık "
                    "hücreler kuru koşu tablosuyla birebir; tutmazsa DURUR"),
    "K12": ("EVET", "etiketler yalnız karar kuralıyla; açık veri 'bilinen veri' diye ayrı; sayı ve yorum ayrı cümle; 'iz' sözü yalnız kural geçerse"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_k2 (test); defter / yasak modüllere dokunulmadı (bağımlı sha tablosu); e-posta / anahtar "
                    "taraması (_k2_yaz); dış istek / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; kart ölçümü"),
}


# ================================================================ 0) ORTAK
def _k2_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _k2_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def k2_esik_sha() -> str:
    return YH.yh_esik_sha({"esik": K2_ESIK, "kart": K2_KART})


def _k2_tohum(*parca: Any) -> int:
    return zlib.crc32("|".join(str(p) for p in parca).encode("utf-8")) & 0x7FFFFFFF


def _k2_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _k2_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_k2_json(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        v = float(o)
        return v if np.isfinite(v) else None
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, pd.Timestamp):
        return str(o.date())
    if isinstance(o, _dt.date):
        return str(o)
    if isinstance(o, np.ndarray):
        return [_k2_json(v) for v in o.tolist()]
    return o


_K2_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_K2_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|şifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")


def _k2_yaz(yol: str, metin: str) -> str:
    """Atomik yaz + e-posta / anahtar sızıntı taraması (K13)."""
    if [m for m in _K2_EPOSTA.findall(metin) if m != "noreply@anthropic.com"]:
        raise K2Hata(f"{yol}: metinde e-posta biçimli dizi var -> yazılmadı")
    if _K2_ANAHTAR.search(metin):
        raise K2Hata(f"{yol}: metinde anahtar biçimli dizi var -> yazılmadı")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    tmp = yol + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(tmp, yol)
    return yol


def _k2_jyaz(yol: str, J: Any) -> str:
    return _k2_yaz(yol, json.dumps(_k2_json(J), ensure_ascii=False, indent=1))


def _k2_git(yol: str) -> str:
    try:
        return subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_K2, capture_output=True, text=True,
                              check=True).stdout.strip() or "-"
    except (OSError, subprocess.CalledProcessError):
        return "-"


def k2_bagimli_sha() -> Dict[str, str]:
    out = {}
    for y in K2_BAGIMLI:
        t = os.path.join(KOK_K2, y)
        out[y] = _k2_sha(t) if os.path.exists(t) else "-"
    return out


def k2_tablo_sha(X: pd.DataFrame) -> str:
    """Kanonik tablo sha'sı: (sembol, tarih) sıralı, tarih YYYY-MM-DD, float %.17g (yeniden üretim / önbellek kimliği)."""
    if not len(X):
        return hashlib.sha256(("|".join(map(str, X.columns))).encode()).hexdigest()
    Y = X.copy()
    for c in Y.columns:
        if pd.api.types.is_datetime64_any_dtype(Y[c]):
            Y[c] = pd.to_datetime(Y[c]).dt.strftime("%Y-%m-%d")
    Y = Y.sort_values([c for c in ("sembol", "tarih") if c in Y.columns], kind="mergesort").reset_index(drop=True)
    return hashlib.sha256(Y.to_csv(index=False, float_format="%.17g").encode("utf-8")).hexdigest()


def k2_sha_simdi() -> Dict[str, Any]:
    E = {"KART_TUR2.py": _k2_sha(K2_YOL["kod"]), "K2_ESIK_SHA": k2_esik_sha(), "YH_Y10_ESIK_SHA": YH.yh_esik_sha(KT._Y10),
         "YH_Y11_ESIK_SHA": YH.yh_esik_sha(YH.YH_ESIK["denemeler"]["Y11"]), "YH_ESIK8_SHA": YH.yh_esik_sha(YH.YH_ESIK8),
         "GE_OZELLIK_SHA": YH.yh_esik_sha(GE.GE_ESIK["ozellik"]), "DS_OLAY_SHA": YH.yh_esik_sha(DS.DS_ESIK["olay"]),
         "OC_ESIK_SHA": YH.yh_esik_sha(OC.OC_ESIK), "OS_ESIK_SHA": OS.os_esik_sha(), "T2_ESIK_SHA": T2.t2_esik_sha()}
    import BOFA_IZI as BI
    import D9_YENIDEN as D9
    E["DP_KURULUM_SHA"] = YH.yh_esik_sha(BI.DP_ESIK["kurulum"]); E["D9_PARAM_SHA"] = YH.yh_esik_sha(D9.D9_PARAM)
    return {"esik": E, "bagimli": k2_bagimli_sha()}


def _k2_havuz(f: Callable, isler: List[Any], islem: int) -> List[Any]:
    if islem > 1 and len(isler) > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(min(islem, len(isler))) as hv:
            return hv.map(f, isler)
    return [f(x) for x in isler]


def _r6(x: np.ndarray) -> np.ndarray:
    """6 anlamlı basamak ('%.6g' csv biçimi; KART_TUR1._r6 ile aynı)."""
    return np.array([float(f"{v:.6g}") if np.isfinite(v) else np.nan for v in np.asarray(x, float)])


def k2_ceyrek(t: Any) -> str:
    t = pd.Timestamp(t)
    return f"{t.year}Q{(t.month - 1) // 3 + 1}"


def k2_bloklar_beklenen(n: int) -> List[str]:
    out, y, q = [], 2024, 1
    for _ in range(n):
        out.append(f"{y}Q{q}"); q += 1
        if q > 4:
            q = 1; y += 1
    return out


def k2_hucre_adi(g: Any) -> np.ndarray:
    """giriş günü -> 'acik_d1' / 'acik_d2' / 'acik_d3' / 'blok' / 'dis'."""
    g = pd.to_datetime(pd.Series(g)).to_numpy()
    out = np.full(len(g), "dis", dtype=object)
    for ad in ("acik_d1", "acik_d2", "acik_d3"):
        a, b = K2_ESIK["hucre"][ad]
        out[(g >= np.datetime64(pd.Timestamp(a))) & (g <= np.datetime64(pd.Timestamp(b)))] = ad
    out[g >= np.datetime64(K2_BLOK_BAS)] = "blok"
    return out


# ================================================================ 1) KASA, DURUM
def k2_durum(veri: str) -> Dict[str, Any]:
    """--veri klasöründeki KASA_DURUM.json: mühür = KASA2 manifest, açılmış bloklar 2024Q1'den kesintisiz, bakış no."""
    yol = os.path.join(veri, KS.KS_DURUM_AD)
    if not os.path.exists(yol):
        raise K2Hata(f"KASA durum dosyası yok: {yol} (yalnız KASA 2 açık kısmı okunur)")
    D = json.load(open(yol, encoding="utf-8"))
    M = json.load(open(K2_YOL["manifest"], encoding="utf-8"))
    if D.get("muhur_id") != M.get("muhur_id"):
        raise K2Hata(f"açık kısım KASA 2 mühürüne ait değil ({D.get('muhur_id')} != {M.get('muhur_id')}) -> DURDU")
    kes = pd.Timestamp(D["acik_kesik"]); ac = list(D.get("acilan", []))
    if ac != k2_bloklar_beklenen(len(ac)):
        raise K2Hata(f"açılmış bloklar 2024Q1'den kesintisiz değil: {ac}")
    if not ac and kes != K2_ACIK_SON:
        raise K2Hata(f"blok açılmamış ama açık kesik {kes.date()} != {K2_ACIK_SON.date()}")
    if ac:
        son = pd.Period(ac[-1], freq="Q")
        if not (son.start_time.normalize() <= kes <= son.end_time.normalize()):
            raise K2Hata(f"açık kesik {kes.date()} son açılmış blok {ac[-1]} içinde değil")
    nb = len(ac)
    return {"kesik": kes, "acilan": ac, "blok_sayi": nb, "bakis_no": int(K2_ESIK["bakis"].get(str(nb), 0)),
            "muhur_id": D.get("muhur_id"), "durum_sha": _k2_sha(yol)}


def k2_kasa(veri: str, D: Dict[str, Any]) -> Dict[str, Any]:
    """V_<p>.pkl -> V_<p>2.pkl bağlantısı + KASA.kasa_kapisi (en geç tarih <= açık kesik)."""
    hisse = []
    for p in K2_PAZAR:
        y = os.path.join(veri, f"V_{p}.pkl"); y2 = os.path.join(veri, f"V_{p}2.pkl")
        if not os.path.exists(y2) or not os.path.exists(y) or os.path.realpath(y) != os.path.realpath(y2):
            raise K2Hata(f"{y} -> V_{p}2.pkl bağlantısı yok (başka veri okunabilir; indirme / worktree YASAK) -> DURDU")
        hisse.append(y2)
    try:
        return KS.kasa_kapisi(hisse, kesik=D["kesik"])
    except KS.KasaHata as ex:
        raise K2Hata(f"KASA 2 kapısı KAPALI: {ex}") from ex


def _k2_onkayit_sha(metin: str, ad: str) -> List[str]:
    return re.findall(rf"^\s*{ad}:\s*([0-9a-f]{{64}})\s*$", metin, flags=re.M)


def k2_onkayit_kapisi(onkayit: str) -> Dict[str, Any]:
    """Blok açıkken: KASA.ks_onkayit_kapi (git'e işlenmiş, değişmemiş, KASA_HIPOTEZ KART_TUR2, KASA_KOD sha'ları, kontrol tablosu) +
    BAGIMLI_SHA + K2_ESIK_SHA + ACIK_TABLO_SHA + GUC_SHA + PREFIX_SHA aynı."""
    try:
        G = KS.ks_onkayit_kapi(onkayit, K2_HIPOTEZ, kontrol=True)
    except KS.KasaHata as ex:
        raise K2Hata(f"ön kayıt kapısı KAPALI: {ex}") from ex
    metin = open(onkayit, encoding="utf-8").read()
    kayit = dict(re.findall(r"^\s*BAGIMLI_SHA:\s*(\S+)\s+([0-9a-f]{64}|-)\s*$", metin, flags=re.M))
    if not kayit:
        raise K2Hata("ön kayıtta BAGIMLI_SHA satırı yok")
    simdi = k2_bagimli_sha(); fark = [k for k, v in kayit.items() if simdi.get(k) != v]
    if fark:
        raise K2Hata(f"bağımlı dosya ön kayıttan sonra değişmiş: {fark} -> DURDU")
    if _k2_onkayit_sha(metin, "K2_ESIK_SHA") != [k2_esik_sha()]:
        raise K2Hata("K2_ESIK sha ön kayıttakiyle aynı değil -> DURDU")
    for ad, yol in (("ACIK_TABLO_SHA", os.path.join(K2_YOL["acik"], K2_DOSYA["hucre"])), ("GUC_SHA", K2_YOL["guc"]),
                    ("PREFIX_SHA", K2_YOL["prefix"])):
        if not os.path.exists(yol) or _k2_onkayit_sha(metin, ad) != [_k2_sha(yol)]:
            raise K2Hata(f"{ad} ön kayıttakiyle aynı değil ya da dosya yok ({yol}) -> DURDU")
    G["bagimli"] = len(kayit)
    G["olay_acik"] = dict(re.findall(r"^\s*OLAY_ACIK_SHA:\s*(\S+)\s+([0-9a-f]{64})\s*$", metin, flags=re.M))
    return G


# ================================================================ 2) SİNYALLER (yalnız açık fiyat verisinden; hisse başına nedensel)
_K2_IS: Dict[str, Any] = {}
_Y1_OZ = list(YH._Y10_OZ) + list(YH._Y11_OZ_S9)
_Y1_S10 = list(YH._YH_S10_OZ)
_Y1_BAYRAK = ["F_KT01", "F_KT02", "F_KT03", "F_KT04", "F_KT05", "F_KT06", "F_KT07", "F_KT11", "F_KT12"]


def _k2_y1_isci(semboller: List[str]) -> Dict[str, Any]:
    """Hisse başına: S6 taraması (YH.yh_s6_hisse; bütün seri) -> Y1 sinyalleri; özellikler (GE F1-F18, YH S7 F20-F23, S9 F24-F29, S10) yalnız
    t > kes_eski olan sinyaller için (kes_eski None ise hepsi). Döner: {'yeni': satırlar, 'eski': (sembol, tarih, hat, tavan) satırları}."""
    V = _K2_IS["V"]; kes = _K2_IS.get("kes_eski"); yeni, eski, hata = [], [], []
    for s in semboller:
        try:
            X, _ = YH.yh_s6_hisse(V[s])
            if not len(X):
                continue
            tl_all = pd.to_datetime(X.tarih)
            m_yeni = np.ones(len(X), bool) if kes is None else (tl_all > kes).to_numpy()
            for t, h0, tv0 in zip(tl_all[~m_yeni], X.hat.to_numpy(float)[~m_yeni], X.tavan.to_numpy(float)[~m_yeni]):
                eski.append({"sembol": s, "tarih": pd.Timestamp(t), "hat": float(h0), "tavan": float(tv0)})
            if not m_yeni.any():
                continue
            Xn = X[m_yeni]; tl = list(pd.to_datetime(Xn.tarih))
            d = GE.ge_hazir(V[s])
            Fs, Bs = GE.ge_ozellik_hisse(d, tl, hazir=True)
            S7 = YH.yh_s7_ozellik(d, tl, hazir=True); S9 = YH.yh_s9_ozellik(d, tl, hazir=True); S10 = YH.yh_s10_ozellik(d, tl, hazir=True)
            for k, (t, f, b, h0, tv0) in enumerate(zip(tl, Fs, Bs, Xn.hat.to_numpy(float), Xn.tavan.to_numpy(float))):
                ok = bool(abs(b["hat"] / h0 - 1) <= 1e-9 and (abs(b["tavan"] / tv0 - 1) <= 1e-9 if np.isfinite(tv0) else not np.isfinite(b["tavan"])))
                if not ok:
                    hata.append(f"{s} {t.date()} hat / tavan sinyalle aynı değil")
                yeni.append({"sembol": s, "tarih": pd.Timestamp(t), "hat": float(h0), "tavan": float(tv0), **f, **S7.iloc[k].to_dict(),
                             **S9.iloc[k].to_dict(), **S10.iloc[k].to_dict()})
        except Exception as ex:   # tek hisse bozuksa sayılır; sonda DURUR (sessiz düşme yok)
            hata.append(f"{s}: {type(ex).__name__}: {str(ex)[:160]}")
    return {"yeni": yeni, "eski": eski, "hata": hata}


def k2_y1_bayrak(F: pd.DataFrame) -> pd.DataFrame:
    """Y1 sinyal tablosu -> 6 anlamlı basamak + Ş1 / Ş3 / Ş4 / Ş5 / Ş7 / Ş9 / Ş10 -> F_KT01..07, F_KT11, F_KT12."""
    F = F.copy()
    for c in _Y1_OZ:
        F[c] = _r6(F[c].to_numpy(float)) if len(F) else F[c].astype(float)
    if not len(F):
        for c in _Y1_BAYRAK:
            F[c] = np.zeros(0)
        return F
    S = YH.yh_s9_sartlar(F)
    F["F_KT01"] = 1.0
    for kod, m in (("F_KT02", S["S1"]), ("F_KT03", S["S3"]), ("F_KT04", S["S5"]), ("F_KT05", S["S4"]), ("F_KT06", S["S7"]),
                   ("F_KT07", S["S1"] & S["S3"] & S["S5"]), ("F_KT11", S["S9"]), ("F_KT12", F["S10"].to_numpy(float) == 1.0)):
        F[kod] = np.asarray(m, bool).astype(float)
    return F


def k2_y1(V: Dict[str, pd.DataFrame], islem: int = 1, kes_eski: Optional[pd.Timestamp] = None) -> Dict[str, Any]:
    t0 = time.time(); S = sorted(V); k = max(1, islem * 6)
    dilim = [S[j::k] for j in range(k) if S[j::k]]
    _K2_IS.clear(); _K2_IS.update({"V": V, "kes_eski": kes_eski})
    try:
        R = _k2_havuz(_k2_y1_isci, dilim, islem)
    finally:
        _K2_IS.clear()
    hata = [h for r in R for h in r["hata"]]
    if hata:
        raise K2Hata(f"Y1: {len(hata)} hisse / olayda hata (ör. {hata[:3]}) -> DURDU")
    kol = ["sembol", "tarih", "hat", "tavan"] + _Y1_OZ + _Y1_S10
    Yn = pd.DataFrame([y for r in R for y in r["yeni"]])
    Yn = Yn.reindex(columns=kol) if len(Yn) else pd.DataFrame(columns=kol)
    Ye = pd.DataFrame([y for r in R for y in r["eski"]], columns=["sembol", "tarih", "hat", "tavan"])
    for X_ in (Yn, Ye):   # boş tabloda bile tür sabit (önbellekle birleşimde tarih datetime64 kalsın)
        X_["sembol"] = X_["sembol"].astype(str); X_["tarih"] = pd.to_datetime(X_["tarih"])
        for c in X_.columns[2:]:
            X_[c] = X_[c].astype(float)
    Yn = k2_y1_bayrak(Yn).sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    k2log.info("Y1: %d yeni (özellikli) + %d eski sinyal (%.0f sn)", len(Yn), len(Ye), time.time() - t0)
    return {"yeni": Yn, "eski": Ye.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)}


def k2_ds_durum_hisse(df: pd.DataFrame, pazar: str) -> np.ndarray:
    """DUSUS_SONRASI.ds_ozellik_hisse 's_ds' durum bayrağının satır satır kopyası (yalnız durum; özellik döngüsü yok)."""
    Eo = DS.DS_ESIK["olay"]; N = len(df)
    if N < Eo["pencere"]:
        return np.zeros(N, bool)
    C, V = df["Close"].to_numpy(float), df["Volume"].to_numpy(float)
    K = df["Kur"].to_numpy(float) if "Kur" in df else np.ones(N)
    c = pd.Series(C); w = Eo["pencere"]
    mx = c.rolling(w, min_periods=w).max().to_numpy(); mn = c.rolling(w, min_periods=w).min().to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        f15 = np.where(mx > mn, (C - mn) / (mx - mn), np.nan); dus = C / mx - 1
    liq = pd.Series(C * V * K).rolling(Eo["likit_gun"], min_periods=Eo["likit_gun"]).median().to_numpy()
    with np.errstate(invalid="ignore"):
        ds = (dus <= Eo["dusus"]) & (f15 <= Eo["f15"]) & (liq >= Eo["likit"][pazar])
        if pazar in Eo["fiyat_min"]:
            ds &= C >= Eo["fiyat_min"][pazar]
    return np.asarray(ds, bool)


def k2_ds(V: Dict[str, pd.DataFrame], pazar: str) -> pd.DataFrame:
    """Bütün DS durum günleri (sembol, tarih) + f15 / r5 (KART_TUR1.kt_f15_r5 formülü)."""
    t0 = time.time(); parca = []
    for s in sorted(V):
        df = V[s]; ds = k2_ds_durum_hisse(df, pazar)
        if not ds.any():
            continue
        tl = list(df.index[ds])
        f15, r5 = KT.kt_f15_r5(YH._yh_hazir(df), tl)
        parca.append(pd.DataFrame({"sembol": s, "tarih": pd.DatetimeIndex(tl), "f15": f15, "r5": r5}))
    X = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["sembol", "tarih", "f15", "r5"])
    k2log.info("DS %s: %d durum günü (%.0f sn)", pazar, len(X), time.time() - t0)
    return X.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)


def k2_ds_ornek_denetim(V: Dict[str, pd.DataFrame], pazar: str, n: int, tohum: int = 2295) -> Dict[str, Any]:
    """Kopya denetimi: rastgele n hissede k2_ds_durum_hisse == DS.ds_ozellik_hisse 's_ds' (bağlam / eşik gerekmez: durum bayrağı onlardan bağımsız)."""
    S = sorted(V); rng = np.random.default_rng([tohum, K2_PAZAR.index(pazar)])
    sec = sorted(S[i] for i in rng.choice(len(S), min(n, len(S)), replace=False))
    bag = DS.ds_baglam({"V": {s: V[s] for s in sec}, "pazar": pazar})   # bağlam yalnız özellikleri etkiler; durum bayrağı ondan bağımsız
    esit = 0
    for s in sec:
        a = k2_ds_durum_hisse(V[s], pazar)
        try:
            _, _, sds = DS.ds_ozellik_hisse(V[s], pazar, bag, s, None, None)
        except Exception as ex:   # denetim çalışamazsa kopya doğrulanmamış sayılır: DURUR (fail-closed)
            raise K2Hata(f"DS kopya denetimi çalışmadı: {pazar} {s}: {type(ex).__name__}: {ex}") from ex
        if not np.array_equal(a, sds.to_numpy(bool)):
            raise K2Hata(f"DS durum kopyası DUSUS_SONRASI ile aynı değil: {pazar} {s} -> DURDU")
        esit += 1
    return {"n": len(sec), "esit": esit, "durum_gunu": int(sum(k2_ds_durum_hisse(V[s], pazar).sum() for s in sec))}


def k2_bofa(veri: str, pazar: str, kesik: Optional[Any] = None) -> pd.DataFrame:
    """BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum (kendi okuyucusu); kesik verilirse seri bellekte kesilir (prefix testi)."""
    import BOFA_IZI as BI
    t0 = time.time()
    V, _ = BI.dp_pkl_fiyat(os.path.join(veri, f"V_{pazar}.pkl"), pazar)
    V = {s: d[d.index <= pd.Timestamp(OC.OC_ESIK["kriz"])] for s, d in V.items()}
    if kesik is not None:
        V = {s: d[d.index <= pd.Timestamp(kesik)] for s, d in V.items()}
        V = {s: d for s, d in V.items() if len(d) >= 20}
    X, _ = BI.dp_kurulum_tum(V, pazar)
    # dp_kurulum_tum son barı (giriş yok) yazmaz: açık kısmın son barındaki kurulum ancak blok açılınca yazılır -> önbellek denetiminde ayrı
    sb = {s: d.index[d.index <= K2_ACIK_SON].max() for s, d in V.items() if (d.index <= K2_ACIK_SON).any()}
    del V; gc.collect()
    O = pd.DataFrame({"sembol": X.sembol.astype(str), "tarih": pd.to_datetime(X.kurulum_gunu)})
    O["acik_son_bar"] = np.array([sb.get(s) == t for s, t in zip(O.sembol, O.tarih)], bool) if len(O) else np.zeros(0, bool)
    k2log.info("BOFA %s: %d kurulum (%.0f sn)", pazar, len(O), time.time() - t0)
    return O.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)


def k2_d9_durum(Vd: Dict[str, Any], pazar: str, olay_bas: str) -> pd.DataFrame:
    """KART_TUR1.kt_d9_durum (= D9_YENIDEN.d9_durum satır satır kopyası, kısa seri bilgi sütunu düzeltmesiyle) ile AYNI hesap; tek fark dönem
    penceresi olay_bas (D9 çalışmasının 2015-06-01 penceresi kart tanımı değildir). D9_YENIDEN / KART_TUR1 değiştirilmez."""
    import D9_YENIDEN as D9
    E = copy.deepcopy(D9.D9_ESIK); E["olay_bas"] = olay_bas
    P = E["param"]; V = Vd["V"]; sek = D9.d9_sektor(pazar, E)
    RP = D9.d9_ruzgar_panel(Vd, sek, P) if sek else None
    a, b = pd.Timestamp(E["olay_bas"]), pd.Timestamp(E["olay_son"])
    parca = []
    for s in sorted(V):
        x = V[s]
        U = D9.d9_uzun_seri(x, P, tuple(E["bilgi"]["sure_W"])[::-1])
        for c in ("bant250", "bant125"):
            if c not in U.columns:
                U[c] = np.nan
        tar = x.index
        if RP is not None:
            r = RP["tarih"].get_indexer(tar); j = RP["kol"][s]
            ruz = RP["ruz"][r, j]; sep = RP["sepet"][r, j]; rz = RP["ruzgar"][r, j]
        else:
            ruz = np.full(len(tar), np.nan); sep = ruz.copy(); rz = np.zeros(len(tar), bool)
        evb = Vd.get("evren_bas", {}).get(s)
        m = (U.D9.to_numpy() | rz) & (tar >= a) & (tar <= b)
        if evb is not None:
            m &= tar >= pd.Timestamp(evb)
        if not m.any():
            continue
        parca.append(pd.DataFrame({"sembol": s, "tarih": tar[m], "pazar": pazar, "D9": U.D9.to_numpy()[m], "uzun": U.uzun.to_numpy()[m],
                                   "sure": U.sure.to_numpy()[m], "ruz": ruz[m], "sepet": sep[m], "ruzgar": rz[m],
                                   "bant250": U.bant250.to_numpy()[m], "bant125": U.bant125.to_numpy()[m]}))
    D = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["sembol", "tarih", "pazar", "D9", "uzun", "sure", "ruz",
                                                                                "sepet", "ruzgar", "bant250", "bant125"])
    D["sektor_var"] = bool(sek)
    return D


def k2_d9(Vd: Dict[str, Any], pazar: str) -> pd.DataFrame:
    import D9_YENIDEN as D9
    t0 = time.time()
    if pazar != "ABD":
        return pd.DataFrame(columns=["sembol", "tarih", "ruz"])
    Dd = k2_d9_durum(Vd, pazar, K2_ESIK["d9_olay_bas"])
    Xc = D9.d9_satir(Dd, "c")
    O = pd.DataFrame({"sembol": Xc.sembol.astype(str), "tarih": pd.to_datetime(Xc.tarih), "ruz": Xc.ruz.astype(float)})
    k2log.info("D9 %s: %d durum, %d 'c' (%.0f sn)", pazar, len(Dd), len(O), time.time() - t0)
    return O.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)


def k2_sinyal_pazar(Vd: Dict[str, Any], pazar: str, veri: str, islem: int = 1, onbellek: Optional[Dict[str, Any]] = None,
                    bofa_kesik: Optional[Any] = None) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """Grup sinyal tabloları (Y1, DS, BOFA, D9). onbellek verilirse Y1 özellikleri yalnız t > önbellek kesiği için hesaplanır; bütün
    grupların <= kesik satırları önbellekle BİREBİR olmalı (değilse DURUR)."""
    V = Vd["V"]; info: Dict[str, Any] = {}
    kes = pd.Timestamp(onbellek["kesik"]) if onbellek else None
    R = k2_y1(V, islem, kes)
    if onbellek:
        Yc = onbellek["tablo"]["Y1"]
        a = Yc[["sembol", "tarih", "hat", "tavan"]].reset_index(drop=True); b = R["eski"].reset_index(drop=True)
        if len(a) != len(b) or k2_tablo_sha(a) != k2_tablo_sha(b):
            raise K2Hata(f"önbellek tutarsız: Y1 {pazar} <= {kes.date()} sinyalleri yeniden taramayla aynı değil ({len(a)} / {len(b)}) -> DURDU")
        Y1 = pd.concat([Yc, R["yeni"]], ignore_index=True).sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)
        info["Y1_onbellek"] = {"eski": int(len(a)), "yeni": int(len(R["yeni"]))}
    else:
        if len(R["eski"]):
            raise K2Hata("önbelleksiz koşuda eski satır olamaz")
        Y1 = R["yeni"]
    G = {"Y1": Y1, "DS": k2_ds(V, pazar), "D9": k2_d9(Vd, pazar), "BOFA": k2_bofa(veri, pazar, bofa_kesik)}
    if onbellek:
        for g in ("DS", "D9", "BOFA"):
            a = onbellek["tablo"][g]; b = G[g][G[g].tarih <= kes]
            if g == "BOFA":   # açık kısmın son barındaki kurulum açık veride yazılamaz (giriş barı yok); yalnız o satırlar fazladan olabilir
                if a.acik_son_bar.any():
                    raise K2Hata(f"önbellek tutarsız: BOFA {pazar} önbellekte açık son bar kurulumu var -> DURDU")
                info["BOFA_acik_son_bar"] = int(b.acik_son_bar.sum()); b = b[~b.acik_son_bar]
            if k2_tablo_sha(a) != k2_tablo_sha(b.reset_index(drop=True)):
                raise K2Hata(f"önbellek tutarsız: {g} {pazar} <= {kes.date()} satırları yeniden hesapla aynı değil ({len(a)} / {len(b)}) -> DURDU")
            info[f"{g}_onbellek"] = {"eski": int(len(a)), "yeni": int((G[g].tarih > kes).sum())}
    info["sayi"] = {g: int(len(x)) for g, x in G.items()}
    return G, info


# ================================================================ 3) ÖNBELLEK
def _k2_ob_yol(pazar: str, kl: Optional[str] = None) -> str:
    return os.path.join(kl or K2_YOL["onbellek"], f"sinyal_{pazar}.pkl")


def k2_onbellek_yaz(G: Dict[str, pd.DataFrame], pazar: str, kesik: pd.Timestamp, kl: Optional[str] = None) -> Dict[str, Any]:
    kl = kl or K2_YOL["onbellek"]; os.makedirs(kl, exist_ok=True)
    T = {g: x[x.tarih <= kesik].reset_index(drop=True) for g, x in G.items()}
    meta = {"pazar": pazar, "kesik": str(kesik.date()), "kod_sha": _k2_sha(K2_YOL["kod"]), "esik_sha": k2_esik_sha(),
            "tablo_sha": {g: k2_tablo_sha(x) for g, x in T.items()}, "satir": {g: int(len(x)) for g, x in T.items()}, "zaman": _k2_simdi()}
    yol = _k2_ob_yol(pazar, kl)
    pd.to_pickle({"meta": meta, "tablo": T}, yol + ".tmp"); os.replace(yol + ".tmp", yol)
    meta["dosya_sha"] = _k2_sha(yol)
    _k2_jyaz(os.path.join(kl, f"sinyal_{pazar}_meta.json"), meta)
    return meta


def k2_onbellek_oku(pazar: str, beklenen: Optional[Dict[str, str]] = None, kl: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Önbellek yoksa None. Varsa tablo sha'ları (ve verilmişse ön kayıttaki OLAY_ACIK_SHA'lar) tutmalı; tutmazsa DURUR."""
    yol = _k2_ob_yol(pazar, kl)
    if not os.path.exists(yol):
        return None
    O = pd.read_pickle(yol)
    for g, x in O["tablo"].items():
        s = k2_tablo_sha(x)
        if s != O["meta"]["tablo_sha"][g]:
            raise K2Hata(f"önbellek bozuk: {pazar} {g} tablo sha meta ile aynı değil -> DURDU")
        if beklenen is not None and beklenen.get(f"{pazar}|{g}") not in (None, s):
            raise K2Hata(f"önbellek ön kayıttaki OLAY_ACIK_SHA ile aynı değil: {pazar} {g} -> DURDU")
    return O["meta"] | {"tablo": O["tablo"]}


# ================================================================ 4) PANEL (P2) VE OLAYLAR
def k2_sinir() -> Dict[str, Any]:
    if not os.path.exists(K2_YOL["hazirlik_t2"]):
        raise K2Hata(f"tezgâh hazırlık json yok: {K2_YOL['hazirlik_t2']}")
    return json.load(open(K2_YOL["hazirlik_t2"], encoding="utf-8"))["sinir"]


def k2_panel(Vd: Dict[str, Any], pazar: str) -> Tuple[Dict[str, Any], np.ndarray]:
    """OS.os_panel (kova sınırları tezgâh hazırlığındaki sayılar) + T2.t2_havuz -> P2 (= T2.t2_secili_panel(pazar, havuz='P2') hesabı)."""
    t0 = time.time()
    Pn = OS.os_panel(Vd, k2_sinir()[pazar])
    M = T2.t2_havuz(Pn, Vd); P2 = M["P2"]; del M; gc.collect()
    k2log.info("%s panel + P2: %d gün x %d hisse, P2 %d hisse-gün (%.0f sn)", pazar, len(Pn["tarih"]), len(Pn["sembol"]), int(P2.sum()),
               time.time() - t0)
    return Pn, P2


def k2_P(Pn: Dict[str, Any], Vd: Dict[str, Any], P2: np.ndarray) -> Dict[str, Any]:
    """OC.oc_olay_hazirla / DS.ds_olay_kur için panel arayüzü: havuz = P2."""
    return {"pazar": Pn["pazar"], "tarih": Pn["tarih"], "kol": Pn["kol"], "gecersiz": Vd["gecersiz"],
            "Vidx": {s: Vd["V"][s].index for s in Pn["sembol"]}, "ok": P2, "H": np.where(P2, Pn["H"], -1), "kip": "p2"}


def _k2_oc(S: pd.DataFrame, P: Dict[str, Any], tekil: int) -> Tuple[pd.DataFrame, Dict[str, int]]:
    E = json.loads(json.dumps(OC.OC_ESIK)); E["olay"]["tekil_gun"] = int(tekil)
    return OC.oc_olay_hazirla(S[["sembol", "tarih"]].assign(pazar=P["pazar"]), P, E)


def k2_kart_sinyal(Pn: Dict[str, Any], P2: np.ndarray) -> pd.DataFrame:
    """OS.os_kart_sinyal (ay sonu, MOM / STREV değerleri, giriş d) + sıra P2 havuzunda (giriş günü d'de P2 ve değeri sonlu)."""
    X = OS.os_kart_sinyal(Pn)
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64)
    X["p2"] = P2[d, j] if len(X) else np.zeros(0, bool)
    q = float(OS.OS_ESIK["kart"]["onda"])
    for kart in ("MOM", "STREV"):
        g = X.p2 & np.isfinite(X[kart])
        rk = X[kart].where(g).groupby(X.tarih).rank(method="first", pct=True)
        X[f"{kart}_ust2"] = (rk > 1 - q).fillna(False).to_numpy(bool)
        X[f"{kart}_alt2"] = (rk <= q).fillna(False).to_numpy(bool)
    return X


def k2_olaylar(G: Dict[str, pd.DataFrame], Pn: Dict[str, Any], Vd: Dict[str, Any], P2: np.ndarray) -> Tuple[Dict[str, pd.DataFrame], Dict[str, Any]]:
    """Kart olay kümeleri (H tekilinden ÖNCE): kart -> DataFrame[sembol, tarih, giris, d, j] (+ bilgi sütunları). Huni sayımları."""
    P = k2_P(Pn, Vd, P2); pz = Pn["pazar"]; O: Dict[str, pd.DataFrame] = {}; say: Dict[str, Any] = {}
    kol = ["sembol", "tarih", "giris", "d", "j"]
    # Y1 (60 gün tekil)
    Z, sy = _k2_oc(G["Y1"], P, OC.OC_ESIK["olay"]["tekil_gun"])
    Z = Z.merge(G["Y1"][["sembol", "tarih"] + _Y1_BAYRAK], on=["sembol", "tarih"], how="left", validate="one_to_one")
    say["Y1"] = {"sinyal": int(len(G["Y1"])), **sy, "y1_olay": int(len(Z))}
    for k in [k for k, v in K2_KART.items() if v["grup"] == "Y1" and pz in v["pazar"]]:
        O[k] = Z[Z[K2_KART[k]["bayrak"]].to_numpy(float) == 1.0][kol].reset_index(drop=True)
    # DS (ANA 15 bar) -> KT08
    if "KT08" in K2_KART and pz in K2_KART["KT08"]["pazar"]:
        X, sy = DS.ds_olay_kur({"T": G["DS"]}, P)
        A = X[X.ana].copy()
        with np.errstate(invalid="ignore"):
            A["F_KT08"] = ((A.f15.to_numpy(float) <= 0.05) & (A.r5.to_numpy(float) <= -0.03)).astype(float)
        say["DS"] = {k: int(v) for k, v in sy.items()} | {"F_KT08": int(A.F_KT08.sum())}
        O["KT08"] = A[A.F_KT08 == 1.0][kol].reset_index(drop=True)
    # BOFA (KT09)
    if pz in K2_KART["KT09"]["pazar"]:
        Z, sy = _k2_oc(G["BOFA"], P, 1); say["BOFA"] = {"kurulum": int(len(G["BOFA"])), **sy}
        O["KT09"] = Z[kol].reset_index(drop=True)
    # D9 'c' (KT10; yalnız ABD)
    if pz in K2_KART["KT10"]["pazar"]:
        Z, sy = _k2_oc(G["D9"], P, 1); say["D9"] = {"c": int(len(G["D9"])), **sy}
        O["KT10"] = Z[kol].reset_index(drop=True)
    # MOM (KT00) / STREV (KT13): ay sonu, P2 sırası
    X = k2_kart_sinyal(Pn, P2)
    for k, c in (("KT00", "MOM_ust2"), ("KT13", "STREV_alt2")):
        Y = X[X[c]].copy()
        O[k] = pd.DataFrame({"sembol": Y.sembol.to_numpy(), "tarih": pd.to_datetime(Y.tarih).to_numpy(), "giris": Pn["tarih"][Y.d.to_numpy(np.int64)],
                             "d": Y.d.to_numpy(np.int64), "j": Y.j.to_numpy(np.int64)})
    say["MOM_STREV"] = {"ay_sonu_aday": int(len(X)), "p2": int(X.p2.sum()), "KT00": int(len(O["KT00"])), "KT13": int(len(O["KT13"]))}
    for k in O:
        O[k] = O[k].sort_values(["sembol", "d"], kind="mergesort").reset_index(drop=True)
        O[k]["tarih"] = pd.to_datetime(O[k]["tarih"]); O[k]["giris"] = pd.to_datetime(O[k]["giris"])
    return O, say


def k2_tekil(X: pd.DataFrame, H: int) -> np.ndarray:
    """Aynı hissede giriş günü sırasıyla >= H birleşik takvim günü arayla ilk olay (OS.os_tekil kuralı)."""
    return OS.os_tekil(X, H) if len(X) else np.zeros(0, bool)


# ================================================================ 5) ÖLÇÜ (R_H, eşler, hücre istatistiği)
def k2_rh(Pn: Dict[str, Any], H: int, dondur: Optional[pd.Timestamp] = K2_ACIK_SON) -> Tuple[np.ndarray, np.ndarray]:
    """R_H matrisi (giriş günü d x hisse; OS.os_olcu_hesap 'R' ile aynı) + çıkış günü indeksi. dondur: giriş <= dondur olup H. barı > dondur
    olan hisse-günler NaN (açık hücreler dondurulur; olay ve eş aynı matristen)."""
    dep = Pn["dep"]; u = len(Pn["sembol"]); n = len(Pn["tarih"]); H = int(H)
    m = dep["m"]; jj = np.repeat(np.arange(u), m); ee = np.concatenate([np.arange(k) for k in m]) if u else np.zeros(0, np.int64)
    g = dep["off"][jj] + ee
    val = ee + H - 1 < m[jj]
    gi = g[val]; gx = gi + H - 1
    ok = (dep["POS"][gx] - dep["POS"][gi]) <= int(K2_ESIK["ufuk"]["pencere_kat"]) * H - 1
    gi, gx = gi[ok], gx[ok]; ji = jj[val][ok]
    R = np.full((n, u), np.nan); X = np.full((n, u), -1, np.int64)
    R[dep["POS"][gi], ji] = dep["C"][gx] / dep["O"][gi] - 1.0
    X[dep["POS"][gi], ji] = dep["POS"][gx]
    if dondur is not None:
        nd = int(Pn["tarih"].searchsorted(pd.Timestamp(dondur), side="right"))     # giriş satırı < nd <=> giriş <= dondur
        R[:nd][X[:nd] >= nd] = np.nan
    return R, X


def k2_stat(f: np.ndarray, s: np.ndarray, ay: np.ndarray, tohum_ek: int, perm: bool = False) -> Dict[str, Any]:
    """Hücre istatistiği: n, FARK ort / medyan / %1-%99 kırpılmış / sd, SIRA ort, ay kümeli boot (FARK ve SIRA aynı ağırlık; %95 ve %98,33),
    L3O(+) / L3O(-), isteğe bağlı ay kümeli işaret permütasyonu p (+ / -)."""
    f = np.asarray(f, float); s = np.asarray(s, float); ay = np.asarray(ay)
    m = np.isfinite(f) & np.isfinite(s); f, s, ay = f[m], s[m], ay[m]; n = int(len(f))
    B = K2_ESIK["boot"]
    c: Dict[str, Any] = {"n": n, "ay": 0, "fark": np.nan, "med": np.nan, "kirp": np.nan, "sd": np.nan, "sira": np.nan,
                         "boot_alt95": np.nan, "boot_ust95": np.nan, "boot_alt98": np.nan, "boot_ust98": np.nan,
                         "sira_alt95": np.nan, "sira_ust95": np.nan, "sira_alt98": np.nan, "sira_ust98": np.nan,
                         "l3o_p": np.nan, "l3o_n": np.nan, "p_p": np.nan, "p_n": np.nan}
    if n == 0:
        return c
    q1, q99 = np.quantile(f, [0.01, 0.99]); kk = (f >= q1) & (f <= q99)
    c.update({"fark": float(f.mean()), "med": float(np.median(f)), "kirp": float(f[kk].mean()) if kk.any() else np.nan,
              "sd": float(f.std(ddof=1)) if n > 1 else np.nan, "sira": float(s.mean())})
    ua, inv = np.unique(ay, return_inverse=True); K = len(ua); c["ay"] = int(K)
    sf = np.bincount(inv, weights=f, minlength=K); ss = np.bincount(inv, weights=s, minlength=K); nn = np.bincount(inv, minlength=K).astype(float)
    rng = np.random.default_rng([int(B["tohum"]), int(tohum_ek) % (2 ** 31)])
    W = rng.multinomial(K, np.full(K, 1.0 / K), size=int(B["B"])).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        wn = W @ nn; mf = (W @ sf) / wn; ms = (W @ ss) / wn
    ok = np.isfinite(mf) & np.isfinite(ms); mf, ms = mf[ok], ms[ok]
    if len(mf):
        qq = [B["alt95"], B["ust95"], B["alt_bakis"], B["ust_bakis"]]
        a1, b1, a2, b2 = np.quantile(mf, qq); x1, y1, x2, y2 = np.quantile(ms, qq)
        c.update({"boot_alt95": float(a1), "boot_ust95": float(b1), "boot_alt98": float(a2), "boot_ust98": float(b2),
                  "sira_alt95": float(x1), "sira_ust95": float(y1), "sira_alt98": float(x2), "sira_ust98": float(y2)})
    if K > 3:
        with np.errstate(invalid="ignore", divide="ignore"):
            tek = (sf.sum() - sf) / (nn.sum() - nn)
        op = np.argsort(np.where(np.isfinite(tek), tek, np.inf), kind="stable")[:3]
        on = np.argsort(np.where(np.isfinite(tek), -tek, np.inf), kind="stable")[:3]
        kp = np.ones(K, bool); kp[op] = False; kn = np.ones(K, bool); kn[on] = False
        c["l3o_p"] = float(sf[kp].sum() / nn[kp].sum()); c["l3o_n"] = float(sf[kn].sum() / nn[kn].sum())
    if perm:
        Pm = K2_ESIK["perm"]; rp = np.random.default_rng([int(Pm["tohum"]), int(tohum_ek) % (2 ** 31)])
        eps = rp.choice(np.array([-1.0, 1.0]), size=(int(Pm["R"]), K)); T = sf.sum() / n; Ts = (eps @ sf) / n
        c["p_p"] = float((1 + int((Ts >= T - 1e-15).sum())) / (int(Pm["R"]) + 1))
        c["p_n"] = float((1 + int((Ts <= T + 1e-15).sum())) / (int(Pm["R"]) + 1))
    return c


def k2_tutar(c: Dict[str, Any], yon: str, bakis: bool) -> bool:
    """Hücre TUTAR (plasebo hariç) beklenen yönde: '+' -> n >= 30, FARK > 0, boot alt > 0, SIRA > 0,5, SIRA boot alt > 0,5, L3O(+) > 0;
    '-' -> tersi. bakis: boot %98,33, değilse %95."""
    nm = 30; L = "98" if bakis else "95"
    if c["n"] < nm or not np.isfinite(c["fark"]):
        return False
    if yon == "+":
        return bool(c["fark"] > 0 and c[f"boot_alt{L}"] > 0 and c["sira"] > 0.5 and c[f"sira_alt{L}"] > 0.5 and np.isfinite(c["l3o_p"])
                    and c["l3o_p"] > 0)
    return bool(c["fark"] < 0 and c[f"boot_ust{L}"] < 0 and c["sira"] < 0.5 and c[f"sira_ust{L}"] < 0.5 and np.isfinite(c["l3o_n"])
                and c["l3o_n"] < 0)


def _k2_ay(Pn: Dict[str, Any], d: np.ndarray) -> np.ndarray:
    t = Pn["tarih"][np.asarray(d, np.int64)]
    return (t.year * 12 + t.month).to_numpy() if len(t) else np.zeros(0, int)


class K2Havuz:
    """Bir pazar x H için eş havuzu (OS.os_havuz; KV = P2'de KV1, değilse -1), plasebo / yapay iz aday listeleri."""

    def __init__(self, Pn: Dict[str, Any], P2: np.ndarray, R: np.ndarray):
        self.Pn, self.R = Pn, R
        self.KV = np.where(P2, Pn["KV1"], -1).astype(np.int64)
        self.hv = OS.os_havuz(R, self.KV)
        pool = (self.KV >= 0) & np.isfinite(R)
        dd, jj = np.nonzero(pool)
        self.cd, self.cj = dd.astype(np.int64), jj.astype(np.int64)
        n = len(Pn["tarih"])
        self.bas = np.searchsorted(self.cd, np.arange(n), "left"); self.say = np.searchsorted(self.cd, np.arange(n), "right") - self.bas

    def es(self, d: np.ndarray, j: np.ndarray, x: np.ndarray, exc_d: np.ndarray, exc_j: np.ndarray) -> Dict[str, np.ndarray]:
        return OS.os_es(self.hv, d, j, x, exc_d, exc_j, int(K2_ESIK["es"]["min"]))

    def cek_gun(self, d: np.ndarray, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
        """Her olay günü için aynı gün havuzdan rastgele hisse (gün içinde yerine koymadan; havuz küçükse olay düşer)."""
        d = np.asarray(d, np.int64); sz = self.say[d]; ok = sz > 0; d = d[ok]; sz = sz[ok]
        j = self.cj[self.bas[d] + np.floor(rng.random(len(d)) * sz).astype(np.int64)]
        for _ in range(50):
            key = d * np.int64(1 << 20) + j
            _, ilk, cnt = np.unique(key, return_index=True, return_counts=True)
            if (cnt == 1).all():
                break
            tekrar = np.ones(len(d), bool); tekrar[ilk] = False
            j[tekrar] = self.cj[self.bas[d[tekrar]] + np.floor(rng.random(int(tekrar.sum())) * sz[tekrar]).astype(np.int64)]
        key = d * np.int64(1 << 20) + j
        _, ilk = np.unique(key, return_index=True)
        ilk = np.sort(ilk)
        return d[ilk], j[ilk]


def k2_plasebo(hv: K2Havuz, d: np.ndarray, bakis: bool, tohum_ad: str) -> Dict[str, Any]:
    """Hücre plasebo kapısı: 200 tohum, her olay günü için aynı gün rastgele P2 hissesi; ort FARK, TUTAR(+) / TUTAR(-) payı."""
    Pl = K2_ESIK["plasebo"]; T = int(Pl["tohum_sayi"]); fk, tp, tn = [], 0, 0
    if not len(d):
        return {"plasebo_fark": np.nan, "plasebo_pay_p": np.nan, "plasebo_pay_n": np.nan, "plasebo_gecti": False}
    for t in range(T):
        rng = np.random.default_rng([int(Pl["tohum"]), _k2_tohum(tohum_ad), t])
        dd, jj = hv.cek_gun(d, rng); x = hv.R[dd, jj]
        e = hv.es(dd, jj, x, dd, jj); f = x - e["es"]
        c = k2_stat(f, e["sira"], _k2_ay(hv.Pn, dd), _k2_tohum(tohum_ad, "pl", t))
        fk.append(c["fark"]); tp += int(k2_tutar(c, "+", bakis)); tn += int(k2_tutar(c, "-", bakis))
    fo = float(np.nanmean(fk)) if np.isfinite(fk).any() else np.nan
    pp, pn = tp / T, tn / T
    return {"plasebo_fark": fo, "plasebo_pay_p": pp, "plasebo_pay_n": pn,
            "plasebo_gecti": bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_esik"]) and pp <= float(Pl["tutar_pay"]) and pn <= float(Pl["tutar_pay"]))}


# ================================================================ 6) GÜÇ (yapay iz)
def k2_guc_egri(hv: K2Havuz, pazar: str, H: int) -> List[Dict[str, Any]]:
    """Pencere x n x delta: yakalama payı (TUTAR(+), plasebo hariç). Pencere 1y / 2y / 3y boot %98,33; d1 / d2 / d3 %95."""
    Gc = K2_ESIK["guc"]; idx = hv.Pn["tarih"]; out = []
    for pw, (a, b) in Gc["pencere"].items():
        bak = pw in ("1y", "2y", "3y")
        lo = int(idx.searchsorted(pd.Timestamp(a), "left")); hi = int(idx.searchsorted(pd.Timestamp(b), "right"))
        i0 = int(np.searchsorted(hv.cd, lo, "left")); i1 = int(np.searchsorted(hv.cd, hi, "left")); N = i1 - i0
        for n in Gc["n"]:
            if n > 2 * N // 3:
                continue
            yak = {dl: 0 for dl in Gc["delta"]}; ya0 = 0
            for t in range(int(Gc["tohum_sayi"])):
                rng = np.random.default_rng([int(Gc["tohum"]), _k2_tohum(pazar, H, pw, n), t])
                sec = i0 + rng.choice(N, size=n, replace=False); dd, jj = hv.cd[sec], hv.cj[sec]
                ay = _k2_ay(hv.Pn, dd); x0 = hv.R[dd, jj]
                for dl in [0.0] + list(Gc["delta"]):
                    x = x0 + dl; e = hv.es(dd, jj, x, dd, jj)
                    c = k2_stat(x - e["es"], e["sira"], ay, _k2_tohum(pazar, H, pw, n, t, dl))
                    if dl == 0.0:
                        ya0 += int(k2_tutar(c, "+", bak))
                    else:
                        yak[dl] += int(k2_tutar(c, "+", bak))
            T = int(Gc["tohum_sayi"])
            out.append({"pazar": pazar, "H": H, "pencere": pw, "n": n, "havuz": N, "yanlis_pozitif": ya0 / T,
                        **{f"guc_{dl}": yak[dl] / T for dl in Gc["delta"]}})
        k2log.info("güç %s H%d %s bitti", pazar, H, pw)
    return out


def k2_guc(egri: List[Dict[str, Any]], pazar: str, H: int, pencere: str, n: float, delta: Optional[float] = None) -> float:
    """Eğriden güç: log n doğrusal ara değer; n < 30 -> 0; en büyük n'den büyükse son değer."""
    dl = delta if delta is not None else K2_ESIK["guc"]["karar_delta"]
    E = sorted([r for r in egri if r["pazar"] == pazar and int(r["H"]) == int(H) and r["pencere"] == pencere], key=lambda r: r["n"])
    if not E or not np.isfinite(n) or n < 30:
        return 0.0
    xs = np.log([r["n"] for r in E]); ys = np.array([r[f"guc_{dl}"] for r in E], float)
    return float(np.interp(np.log(n), xs, ys))


# ================================================================ 7) PAZAR ÖLÇÜMÜ
def k2_olc_pazar(O: Dict[str, pd.DataFrame], Pn: Dict[str, Any], P2: np.ndarray, D: Dict[str, Any], egri: Optional[List[Dict[str, Any]]],
                 plasebo: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """Kart x H: olay satırları (R, eş, SIRA, FARK, durum) + hücre tablosu. D: k2_durum çıktısı."""
    pz = Pn["pazar"]; idx = Pn["tarih"]; n = len(idx); bak = D["bakis_no"] > 0
    with np.errstate(all="ignore"):
        Lq = Pn["Lq"]; medLq = np.array([np.nanmedian(Lq[d, P2[d]]) if P2[d].any() else np.nan for d in range(n)])
    son_veri = idx[-1]; kriz = pd.Timestamp(OC.OC_ESIK["kriz"])
    S_all, H_all, huni = [], [], {}
    for H in K2_ESIK["ufuk"]["karar"]:
        t0 = time.time()
        R, Xc = k2_rh(Pn, H)
        hv = K2Havuz(Pn, P2, R)
        for k, X in O.items():
            yon = K2_KART[k]["yon"]
            tek = k2_tekil(X, H); T = X[tek].reset_index(drop=True)
            d = T.d.to_numpy(np.int64); j = T.j.to_numpy(np.int64)
            x = R[d, j] if len(T) else np.zeros(0)
            e = hv.es(d, j, x, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64))
            hc = k2_hucre_adi(T.giris) if len(T) else np.zeros(0, object)
            cey = np.array([k2_ceyrek(g) for g in T.giris], dtype=object) if len(T) else np.zeros(0, object)
            m_j = Pn["dep"]["m"][j] if len(T) else np.zeros(0, int); ee = Pn["EIX"][d, j] if len(T) else np.zeros(0, int)
            sonu_asar = ee + H - 1 >= m_j                       # hissenin verisi H. bardan önce bitiyor (veri sonu)
            dondu = (Xc[d, j] >= 0) & ~np.isfinite(x) if len(T) else np.zeros(0, bool)   # ölçülebilirdi ama açık dondurması kesti
            dur = np.where(np.isfinite(x) & np.isfinite(e["es"]), "olculdu", np.where(np.isfinite(x), "essiz", "olculemez")).astype(object)
            dur[(~np.isfinite(x)) & sonu_asar] = "kriz" if son_veri >= kriz else "bekleyen"
            acik_g = (T.giris.to_numpy() <= np.datetime64(K2_ACIK_SON)) if len(T) else np.zeros(0, bool)
            dur[dondu | ((~np.isfinite(x)) & sonu_asar & acik_g)] = "acik_tasan"   # açık hücreden kalıcı olarak dışarıda (her koşuda aynı)
            S = pd.DataFrame({"kod": k, "pazar": pz, "ufuk": H, "sembol": T.sembol.to_numpy(), "tarih": T.tarih.to_numpy(), "giris": T.giris.to_numpy(),
                              "hucre": hc, "ceyrek": cey, "durum": dur, "R": x, "es": e["es"], "n_es": e["n_es"], "sira": e["sira"],
                              "fark": x - e["es"], "lq_ust": (Lq[d, j] >= medLq[d]) if len(T) else np.zeros(0, bool), "d": d, "j": j})
            S_all.append(S)
            hx = k2_hucre_adi(X.giris) if len(X) else np.zeros(0, object)
            huni[f"{k}|{pz}|H{H}"] = {"olay": int(len(X)), "tekil": int(len(T)), **{str(a): int(b) for a, b in zip(*np.unique(dur, return_counts=True))},
                                      "olay_hucre": {str(a): int(b) for a, b in zip(*np.unique(hx, return_counts=True))},
                                      "olculen_hucre": {str(a): int(b) for a, b in zip(*np.unique(hc[dur == "olculdu"], return_counts=True))}}
            ay = _k2_ay(Pn, d) if len(T) else np.zeros(0, int)
            hucreler = [("acik_d1", S.hucre == "acik_d1"), ("acik_d2", S.hucre == "acik_d2"), ("acik_d3", S.hucre == "acik_d3")]
            if D["blok_sayi"]:
                hucreler.append(("birikimli", S.hucre == "blok"))
                for q in D["acilan"]:
                    hucreler.append((q, (S.hucre == "blok") & (S.ceyrek == q)))
            for hn, mm in hucreler:
                mm = mm.to_numpy(bool); ol = mm & (S.durum.to_numpy() == "olculdu")
                karar_h = hn == "birikimli"; acik_h = hn.startswith("acik")
                c = k2_stat(S.fark.to_numpy(float)[ol], S.sira.to_numpy(float)[ol], ay[ol], _k2_tohum(k, pz, H, hn), perm=(karar_h or acik_h))
                bk = bak and karar_h
                r = {"kod": k, "yon": yon, "pazar": pz, "ufuk": H, "hucre": hn, "n_olay": int(mm.sum()),
                     "bekleyen": int((mm & (S.durum.to_numpy() == "bekleyen")).sum()), "kriz": int((mm & (S.durum.to_numpy() == "kriz")).sum()),
                     "essiz": int((mm & (S.durum.to_numpy() == "essiz")).sum()), "acik_tasan": int((mm & (S.durum.to_numpy() == "acik_tasan")).sum()),
                     **c, "bakis_duzey": bk}
                for ad, mq in (("lq_ust", ol & S.lq_ust.to_numpy(bool)), ("lq_alt", ol & ~S.lq_ust.to_numpy(bool))):
                    r[f"{ad}_n"] = int(mq.sum()); r[f"{ad}_fark"] = float(np.mean(S.fark.to_numpy(float)[mq])) if mq.any() else np.nan
                r["tutar_p"] = k2_tutar(c, "+", bk); r["tutar_n"] = k2_tutar(c, "-", bk)
                if plasebo and (karar_h or (acik_h and not D["blok_sayi"])):   # açık hücre plasebosu yalnız kuru koşuda (bilgi; tablo sha'lı)
                    r.update(k2_plasebo(hv, d[ol], bk, f"{k}|{pz}|{H}|{hn}"))
                else:
                    r.update({"plasebo_fark": np.nan, "plasebo_pay_p": np.nan, "plasebo_pay_n": np.nan, "plasebo_gecti": False})
                pw = ("d" + hn[-1]) if acik_h else K2_ESIK["guc"]["bakis_pencere"].get(str(max(1, min(3, (len(D["acilan"]) + 3) // 4))), "3y")
                r["guc_pencere"] = pw
                r["guc"] = k2_guc(egri, pz, H, pw, c["n"]) if egri else np.nan
                H_all.append(r)
        k2log.info("%s H%d ölçüm + plasebo (%.0f sn)", pz, H, time.time() - t0)
        del hv, R; gc.collect()
    S = pd.concat(S_all, ignore_index=True) if S_all else pd.DataFrame()
    return S, pd.DataFrame(H_all), huni


# ================================================================ 8) KARAR
def _k2_c(Hc: pd.DataFrame, kod: str, H: int, P: str, hucre: str) -> Optional[Dict[str, Any]]:
    x = Hc[(Hc.kod == kod) & (Hc.ufuk == H) & (Hc.pazar == P) & (Hc.hucre == hucre)]
    return x.iloc[0].to_dict() if len(x) else None


def _k2_bh(p: List[float], q: float) -> List[bool]:
    return YH._yh_bh(p, q)


def k2_karar(Hc: pd.DataFrame, D: Dict[str, Any]) -> pd.DataFrame:
    """Kart etiketleri (K2_ESIK['etiket'] aynen). Blok yoksa 'BİLGİ (blok yok)'. Bakış dışı 'BİLGİ (...)'."""
    U = K2_ESIK["ufuk"]["karar"]; bak = D["bakis_no"] > 0; q = K2_ESIK["bh"]["q_bakis"] if bak else K2_ESIK["bh"]["q"]
    G_ESIK = float(K2_ESIK["guc"]["esik"]); hb = "birikimli" if D["blok_sayi"] else None
    kartlar = [k for k, v in K2_KART.items() if v["karar"]]; sat = []
    if not hb:
        for k in K2_KART:
            sat.append({"kod": k, "etiket": "BİLGİ (blok yok; yalnız açık veri)", "neden": "", "bakis": 0, "bh_p": np.nan})
        return pd.DataFrame(sat)

    def kp(k: str) -> List[str]:
        return [p for p in K2_KART[k]["pazar"] if p in ("ABD", "AVR")]

    def tut(c: Optional[Dict[str, Any]], yon: str) -> bool:
        return bool(c is not None and (c["tutar_p"] if yon == "+" else c["tutar_n"]) and c["plasebo_gecti"])

    def isr(c: Optional[Dict[str, Any]], yon: str) -> bool:
        return bool(c is not None and np.isfinite(c["fark"]) and (c["fark"] > 0 if yon == "+" else c["fark"] < 0))

    def alt(k: str, H: int, P: str, yon: str) -> int:
        return sum(isr(_k2_c(Hc, k, H, P, h), yon) for h in ("acik_d1", "acik_d2", "acik_d3"))

    def guclu(c: Optional[Dict[str, Any]]) -> bool:
        return bool(c is not None and c["n"] >= 30 and np.isfinite(c.get("guc", np.nan)) and c["guc"] >= G_ESIK)

    def pv(c: Optional[Dict[str, Any]], yon: str) -> float:
        if c is None or c["n"] < 30:
            return 1.0
        v = c["p_p"] if yon == "+" else c["p_n"]
        return float(v) if np.isfinite(v) else 1.0

    ters = {"+": "-", "-": "+"}
    aile: Dict[str, Dict[Tuple[str, int], float]] = {"A+": {}, "A-": {}, "B+": {}, "B-": {}}
    for k in kartlar:
        y = K2_KART[k]["yon"]
        for H in U:
            cs = [_k2_c(Hc, k, H, P, hb) for P in kp(k)]
            aile["A+"][(k, H)] = max(pv(c, y) for c in cs); aile["A-"][(k, H)] = max(pv(c, ters[y]) for c in cs)
            ca = _k2_c(Hc, k, H, "ABD", hb)
            aile["B+"][(k, H)] = pv(ca, y); aile["B-"][(k, H)] = pv(ca, ters[y])
    BH = {}
    for a, dct in aile.items():
        ks = list(dct); b = _k2_bh([dct[x] for x in ks], q)
        BH[a] = {x: (bool(bb), dct[x]) for x, bb in zip(ks, b)}

    def sartlar(k: str, pazarlar: List[str], yon: str, ail: str) -> Tuple[bool, str, float]:
        for H1 in U:
            H2 = [h for h in U if h != H1][0]
            c1 = [_k2_c(Hc, k, H1, P, hb) for P in pazarlar]; c2 = [_k2_c(Hc, k, H2, P, hb) for P in pazarlar]
            t1 = all(tut(c, yon) for c in c1); t2 = all(isr(c, yon) for c in c2); t3 = all(alt(k, H1, P, yon) >= 2 for P in pazarlar)
            bg, p = BH[ail][(k, H1)]
            if t1 and t2 and t3 and bg:
                return True, f"R{H1} TUTAR ({', '.join(pazarlar)}), R{H2} işaret aynı, açık alt dönem >= 2/3, BH (q {q:.4f}) geçti (p {p:.4f})", p
        return False, "", np.nan

    for k in kartlar:
        y = K2_KART[k]["yon"]; KP = kp(k); et, neden, bp = None, [], np.nan
        if "ABD" in KP and "AVR" in KP:
            ok, ne, bp = sartlar(k, ["ABD", "AVR"], y, "A+")
            if ok:
                et = "İZ ADAYI"; neden.append(ne)
            if et is None:
                ok, ne, bp = sartlar(k, ["ABD", "AVR"], ters[y], "A-")
                if ok:
                    et = "KATKI−"; neden.append(ne)
        if et is None and "ABD" in KP:
            avr_guc = {H: ("AVR" in KP and guclu(_k2_c(Hc, k, H, "AVR", hb))) for H in U}
            for ters_m, ail, ad in ((False, "B+", "ABD-ADAY"), (True, "B-", "KATKI− (yalnız ABD)")):
                yy = ters[y] if ters_m else y
                for H1 in U:
                    if avr_guc[H1]:
                        continue
                    H2 = [h for h in U if h != H1][0]
                    c1 = _k2_c(Hc, k, H1, "ABD", hb); c2 = _k2_c(Hc, k, H2, "ABD", hb); bg, p = BH[ail][(k, H1)]
                    if tut(c1, yy) and isr(c2, yy) and alt(k, H1, "ABD", yy) >= 2 and bg:
                        et = ad; bp = p
                        neden.append(f"R{H1} ABD TUTAR, R{H2} işaret aynı, açık alt dönem >= 2/3, AVR {'veri yok' if 'AVR' not in KP else 'güçsüz'}, "
                                     f"BH (q {q:.4f}) geçti (p {p:.4f})")
                        break
                if et:
                    break
        cs = [(_k2_c(Hc, k, H, P, hb), H, P) for H in U for P in KP]
        L = "98" if bak else "95"
        if et is None:
            if all(guclu(c) and c[f"boot_alt{L}"] > -0.01 and c[f"boot_ust{L}"] < 0.01 for c, _, _ in cs):
                et = "ETKİ YOK"
            elif any(not guclu(c) for c, _, _ in cs):
                et = "ÖLÇÜLEMEDİ"
                neden.append("; ".join(f"{P} R{H} n {0 if c is None else int(c['n'])} güç {np.nan if c is None else c.get('guc', np.nan):.2f}"
                                       for c, H, P in cs if not guclu(c)))
            else:
                et = "SORGULA"
        neden.append("; ".join(f"{P} R{H} FARK {c['fark'] * 100:+.2f} [{c[f'boot_alt{L}'] * 100:+.2f}; {c[f'boot_ust{L}'] * 100:+.2f}] SIRA "
                               f"{c['sira']:.3f} n {int(c['n'])} TUT {tut(c, y)} plasebo {c['plasebo_gecti']}"
                               for c, H, P in cs if c is not None and np.isfinite(c["fark"])))
        sat.append({"kod": k, "etiket": et if bak else f"BİLGİ ({et})", "neden": " | ".join(x for x in neden if x), "bakis": D["bakis_no"], "bh_p": bp})
    for k in [k for k, v in K2_KART.items() if not v["karar"]]:
        y = K2_KART[k]["yon"]
        if any(all(tut(_k2_c(Hc, k, H, P, hb), y) for P in ("ABD", "AVR")) for H in U):
            et = "GÖRDÜ"
        elif any(all(isr(_k2_c(Hc, k, H, P, hb), y) for P in ("ABD", "AVR")) for H in U):
            et = "KISMEN"
        else:
            et = "GÖRMEDİ"
        sat.append({"kod": k, "etiket": f"KONTROL {et}" + ("" if bak else " (BİLGİ)"), "neden": "etiketleri değiştirmez (yalnız rapor)",
                    "bakis": D["bakis_no"], "bh_p": np.nan})
    return pd.DataFrame(sat)


# ================================================================ 9) YENİDEN ÜRETİM
def k2_yeniden(S: pd.DataFrame, Hc: pd.DataFrame, acik_tablo: Optional[str] = None) -> Dict[str, Any]:
    """K11: (a) iki hücre satır tablosundan düz pandas (n, ort FARK, ort SIRA); (b) acik_tablo verilirse açık hücreler (n, fark, sira, boot,
    plasebo) o tabloyla birebir (dondurulmuş açık veri)."""
    out, tut = [], True
    for kod, P, H, hc in K2_ESIK["yeniden"]:
        if P not in set(S.pazar):   # --pazar ile o pazar ölçülmediyse (deneme koşusu) hücre atlanır; tam koşuda iki hücre de denetlenir
            out.append({"hucre": f"{kod} {P} R{H} {hc}", "not": "pazar ölçülmedi"}); continue
        g = S[(S.kod == kod) & (S.pazar == P) & (S.ufuk == H) & (S.hucre == hc) & (S.durum == "olculdu")]
        n = int(len(g)); f = float((g.R - g.es).mean()) if n else np.nan; s = float(g.sira.mean()) if n else np.nan
        c = _k2_c(Hc, kod, H, P, hc)
        e = c is not None and n == int(c["n"]) and (n == 0 or (abs(f - c["fark"]) < 1e-12 and abs(s - c["sira"]) < 1e-12))
        tut &= bool(e)
        out.append({"hucre": f"{kod} {P} R{H} {hc}", "n": n, "fark": f, "sira": s, "esit": bool(e)})
    ak: Dict[str, Any] = {"yapildi": False}
    if acik_tablo:
        A = pd.read_csv(acik_tablo)
        A = A[A.hucre.astype(str).str.startswith("acik")]
        B = Hc[Hc.hucre.astype(str).str.startswith("acik")]
        M = A.merge(B, on=["kod", "pazar", "ufuk", "hucre"], how="outer", suffixes=("_a", "_b"), indicator=True)
        kol = ["n", "n_olay", "fark", "med", "sira", "boot_alt95", "boot_ust95", "boot_alt98", "sira_alt95", "l3o_p", "p_p"]
        bozuk = int((M._merge != "both").sum())
        for c in kol:
            a, b = M[c + "_a"].to_numpy(float), M[c + "_b"].to_numpy(float)
            bozuk += int((~((np.isnan(a) & np.isnan(b)) | (np.abs(a - b) <= 1e-12 * np.maximum(1, np.abs(a))))).sum())
        ak = {"yapildi": True, "hucre": int(len(M)), "fark": bozuk, "esit": bozuk == 0}
        tut &= bozuk == 0
    return {"tuttu": bool(tut), "hucre": out, "acik": ak}


# ================================================================ 10) ANA KOŞULAR
def _k2_veri(pazar: str, veri: str, kesik: Optional[Any] = None) -> Dict[str, Any]:
    try:
        return OS.os_veri(pazar, veri, kesik=kesik)
    except OS.OSHata as ex:
        raise K2Hata(f"veri okunamadı: {ex}") from ex


def k2_olc(veri: str, cikti: str, islem: int = 1, onkayit: Optional[str] = None, uzerine: bool = False,
           pazarlar: Optional[List[str]] = None, plasebo: bool = True) -> Dict[str, Any]:
    """Bütün kartlar, verilen klasördeki veriyle. Açık veride (blok yok) ön kayıt kapısı aranmaz; blok açıkken zorunlu."""
    t0 = time.time(); bas = _k2_simdi()
    veri = os.path.abspath(veri)
    os.makedirs(cikti, exist_ok=True)
    if os.path.exists(os.path.join(cikti, K2_DOSYA["karar"])) and not uzerine:
        raise K2Hata(f"sonuç zaten var: {os.path.join(cikti, K2_DOSYA['karar'])} (ikinci koşu DURUR; yeni klasör ver)")
    D = k2_durum(veri)
    kapi = k2_kasa(veri, D)
    blok = D["blok_sayi"] > 0
    G = k2_onkayit_kapisi(onkayit or K2_YOL["onkayit"]) if blok else {"not": "blok yok (açık veri kuru koşusu); ön kayıt kapısı aranmaz"}
    egri = None
    if os.path.exists(K2_YOL["guc"]):
        egri = json.load(open(K2_YOL["guc"], encoding="utf-8"))["egri"]
    elif blok:
        raise K2Hata(f"güç eğrisi yok: {K2_YOL['guc']} (önce 'hazirla')")
    pazarlar = pazarlar or K2_PAZAR
    S_all, H_all, huni, info = [], [], {}, {}
    for p in pazarlar:
        tp = time.time()
        ob = k2_onbellek_oku(p, G.get("olay_acik") if blok else None)
        if ob is None:
            k2log.warning("%s önbellek yok: sinyaller baştan hesaplanıyor (yavaş)", p)
        Vd = _k2_veri(p, veri)
        Gs, inf = k2_sinyal_pazar(Vd, p, veri, islem, ob)
        if ob is None and blok:
            for g, x in Gs.items():
                s = k2_tablo_sha(x[x.tarih <= K2_ACIK_SON].reset_index(drop=True))
                if G["olay_acik"].get(f"{p}|{g}") != s:
                    raise K2Hata(f"önbelleksiz yeniden hesap ön kayıttaki OLAY_ACIK_SHA ile aynı değil: {p} {g} -> DURDU")
        info[p] = inf
        Pn, P2 = k2_panel(Vd, p)
        O, say = k2_olaylar(Gs, Pn, Vd, P2)
        huni[p] = {"sinyal_donem": {g: {str(a): int(b) for a, b in zip(*np.unique(k2_hucre_adi(x.tarih), return_counts=True))} if len(x) else {}
                                    for g, x in Gs.items()}, "olay": say}
        del Gs; gc.collect()
        S, Hc, hn = k2_olc_pazar(O, Pn, P2, D, egri, plasebo)
        huni[p]["olcum"] = hn
        S_all.append(S.drop(columns=["d", "j"])); H_all.append(Hc)
        del O, Pn, P2, Vd; gc.collect()
        k2log.info("%s bitti (%.0f sn)", p, time.time() - tp)
    S = pd.concat(S_all, ignore_index=True); Hc = pd.concat(H_all, ignore_index=True)
    Kr = k2_karar(Hc, D)
    at = os.path.join(K2_YOL["acik"], K2_DOSYA["hucre"]) if blok else None
    yen = k2_yeniden(S, Hc, at)
    S = S.sort_values(["kod", "pazar", "ufuk", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    Hc = Hc.sort_values(["kod", "pazar", "ufuk", "hucre"], kind="mergesort").reset_index(drop=True)
    for c in ("tarih", "giris"):
        S[c] = pd.to_datetime(S[c]).dt.strftime("%Y-%m-%d")
    ys = os.path.join(cikti, K2_DOSYA["satir"]); S.to_csv(ys, index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.10g")
    yh = os.path.join(cikti, K2_DOSYA["hucre"]); Hc.to_csv(yh, index=False, float_format="%.12g")
    Kr.to_csv(os.path.join(cikti, K2_DOSYA["karar"]), index=False)
    _k2_jyaz(os.path.join(cikti, K2_DOSYA["huni"]), huni)
    ol = S[S.durum == "olculdu"]
    en_gec = {"satir_en_gec_giris": str(pd.to_datetime(S.giris).max().date()) if len(S) else "-",
              "olculen_son_giris": {str(H): str(pd.to_datetime(ol[ol.ufuk == H].giris).max().date()) for H in sorted(ol.ufuk.unique())}}
    asan = [v for v in [en_gec["satir_en_gec_giris"]] + list(en_gec["olculen_son_giris"].values()) if v != "-" and pd.Timestamp(v) > D["kesik"]]
    J = {"surum": K2_SURUM, "durum": {k: v for k, v in D.items() if k != "kesik"}, "kesik": str(D["kesik"].date()), "kasa": kapi,
         "onkayit_kapi": G, "yeniden": yen, "en_gec": en_gec, "onbellek": info, "sha": k2_sha_simdi(),
         "acik_tablo_sha": _k2_sha(yh) if not blok else None}
    _k2_jyaz(os.path.join(cikti, K2_DOSYA["sonuc"]), J)
    _k2_jyaz(os.path.join(cikti, K2_DOSYA["meta"]), {"baslangic": bas, "bitis": _k2_simdi(), "sure_sn": round(time.time() - t0, 1),
                                                    "islem": islem, "veri": veri})
    _k2_yaz(os.path.join(cikti, K2_DOSYA["rapor"]), k2_rapor_md(cikti))
    if asan:
        raise K2Hata(f"KESİK AŞIMI çıktı dosyasında: {asan}")
    if not yen["tuttu"]:
        raise K2Hata(f"yeniden üretim TUTMADI: {yen}")
    k2log.info("bitti: %d satır, %d hücre (%.0f sn)", len(S), len(Hc), time.time() - t0)
    return {"satir": S, "hucre": Hc, "karar": Kr, "sonuc": J, "huni": huni}


def _k2_olay_anahtar(O: Dict[str, pd.DataFrame], Pn: Dict[str, Any], son: pd.Timestamp) -> Dict[str, pd.DataFrame]:
    return {k: X[X.tarih <= son][["sembol", "tarih", "giris"]].reset_index(drop=True) for k, X in O.items()}


def k2_hazirla(veri: str, islem: int = 1, pazarlar: Optional[List[str]] = None, guc: bool = True) -> Dict[str, Any]:
    """Açık veride: (1) tam sinyaller -> önbellek; (2) tam panel -> P2 olay kümeleri; (3) güç eğrileri; (4) 2022-06-30 kesik sinyaller + panel
    -> <= 2022-05-31 PREFIX karşılaştırması (BİREBİR; değilse DURUR); DS kopya denetimi."""
    t0 = time.time(); D = k2_durum(veri)
    if D["blok_sayi"]:
        raise K2Hata("hazirla yalnız açık veride (blok açılmamışken) çalışır")
    kapi = k2_kasa(veri, D)
    Pr = K2_ESIK["prefix"]; son = pd.Timestamp(Pr["son"]); kisa = pd.Timestamp(Pr["kisa"])
    out: Dict[str, Any] = {"surum": K2_SURUM, "esik_sha": k2_esik_sha(), "kod_sha": _k2_sha(K2_YOL["kod"]), "kasa": kapi, "prefix": {},
                           "onbellek": {}, "ds_kopya": {}, "sure": {}}
    egri: List[Dict[str, Any]] = []
    for p in pazarlar or K2_PAZAR:
        tp = time.time()
        Vd = _k2_veri(p, veri)
        out["ds_kopya"][p] = k2_ds_ornek_denetim(Vd["V"], p, int(K2_ESIK["ds_ornek"]))
        Gs, _ = k2_sinyal_pazar(Vd, p, veri, islem, None)
        out["onbellek"][p] = k2_onbellek_yaz(Gs, p, K2_ACIK_SON)
        Pn, P2 = k2_panel(Vd, p)
        O, _ = k2_olaylar(Gs, Pn, Vd, P2)
        anah_tam = _k2_olay_anahtar(O, Pn, son)
        sig_tam = {g: x[x.tarih <= son].reset_index(drop=True) for g, x in Gs.items()}
        del O, Gs; gc.collect()
        if guc:
            for H in K2_ESIK["ufuk"]["karar"]:
                R, _ = k2_rh(Pn, H); hv = K2Havuz(Pn, P2, R)
                egri += k2_guc_egri(hv, p, H)
                del hv, R; gc.collect()
        del Pn, P2, Vd; gc.collect()
        out["sure"][f"{p}_tam"] = round(time.time() - tp)
        # kısa (kesik) veri
        tk = time.time()
        Vk = _k2_veri(p, veri, kesik=kisa)
        Gk, _ = k2_sinyal_pazar(Vk, p, veri, islem, None, bofa_kesik=kisa)
        Pk, P2k = k2_panel(Vk, p)
        Ok, _ = k2_olaylar(Gk, Pk, Vk, P2k)
        anah_k = _k2_olay_anahtar(Ok, Pk, son)
        sig_k = {g: x[x.tarih <= son].reset_index(drop=True) for g, x in Gk.items()}
        r: Dict[str, Any] = {"sinyal": {}, "olay": {}}
        for g in sig_tam:
            a, b = sig_tam[g], sig_k[g]
            r["sinyal"][g] = {"n_tam": int(len(a)), "n_kisa": int(len(b)), "esit": k2_tablo_sha(a) == k2_tablo_sha(b)}
        for k in anah_tam:
            a, b = anah_tam[k], anah_k.get(k, anah_tam[k].iloc[0:0])
            r["olay"][k] = {"n_tam": int(len(a)), "n_kisa": int(len(b)), "esit": k2_tablo_sha(a) == k2_tablo_sha(b)}
        r["tutar"] = all(v["esit"] for v in r["sinyal"].values()) and all(v["esit"] for v in r["olay"].values())
        out["prefix"][p] = r
        out["sure"][f"{p}_kisa"] = round(time.time() - tk)
        k2log.info("%s PREFIX: %s (%.0f sn)", p, "TUTTU" if r["tutar"] else "TUTMADI", time.time() - tp)
        del Vk, Gk, Pk, P2k, Ok; gc.collect()
    out["sure"]["toplam"] = round(time.time() - t0)
    out["zaman"] = _k2_simdi()
    _k2_jyaz(K2_YOL["prefix"], out)
    if guc:
        _k2_jyaz(K2_YOL["guc"], {"surum": K2_SURUM, "esik_sha": k2_esik_sha(), "tanim": K2_ESIK["guc"]["tanim"], "egri": egri})
    bozuk = [p for p, r in out["prefix"].items() if not r["tutar"]]
    if bozuk:
        raise K2Hata(f"PREFIX TESTİ TUTMADI: {bozuk} -> DURDU (k2_prefix.json)")
    return out


# ================================================================ 11) RAPOR
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


def k2_hucre_tablo(Hc: pd.DataFrame, hucre: str) -> List[str]:
    L = ["| Kart | Yön | Pazar | H | n olay | n | bekleyen | FARK puan [boot %95] | [%98,33] | medyan | kırpılmış | SIRA [boot alt] | L3O + / - | p + / - "
         "| lik. üst n / FARK | lik. alt n / FARK | plasebo ort / pay+ / pay- / geçti | güç (+1) | TUT+ / TUT- |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in Hc[Hc.hucre == hucre].itertuples(index=False):
        L.append(f"| {r.kod} | {r.yon} | {r.pazar} | {int(r.ufuk)} | {int(r.n_olay)} | {int(r.n)} | {int(r.bekleyen)} | {_y(r.fark)} [{_y(r.boot_alt95)}; "
                 f"{_y(r.boot_ust95)}] | [{_y(r.boot_alt98)}; {_y(r.boot_ust98)}] | {_y(r.med)} | {_y(r.kirp)} | {_s(r.sira, 3)} [{_s(r.sira_alt95, 3)}] | "
                 f"{_y(r.l3o_p)} / {_y(r.l3o_n)} | {_s(r.p_p, 4)} / {_s(r.p_n, 4)} | {int(r.lq_ust_n)} / {_y(r.lq_ust_fark)} | {int(r.lq_alt_n)} / "
                 f"{_y(r.lq_alt_fark)} | {_y(r.plasebo_fark)} / {_s(r.plasebo_pay_p)} / {_s(r.plasebo_pay_n)} / {r.plasebo_gecti} | {_s(r.guc)} | "
                 f"{r.tutar_p} / {r.tutar_n} |")
    return L


def k2_rapor_md(cikti: str) -> str:
    J = json.load(open(os.path.join(cikti, K2_DOSYA["sonuc"]), encoding="utf-8"))
    Hc = pd.read_csv(os.path.join(cikti, K2_DOSYA["hucre"])); Kr = pd.read_csv(os.path.join(cikti, K2_DOSYA["karar"]))
    huni = json.load(open(os.path.join(cikti, K2_DOSYA["huni"]), encoding="utf-8"))
    D = J["durum"]
    L = [f"# KART TURU 2 — sonuç (açık kesik {J['kesik']}, açılmış blok {D['blok_sayi']}: {', '.join(D['acilan']) or 'yok'})", "", K2_SURUM, "",
         f"Bakış: {('KARAR BAKIŞI ' + str(D['bakis_no'])) if D['bakis_no'] else ('YOK (açık veri kuru koşusu)' if not D['blok_sayi'] else 'BİLGİ')}. "
         f"KASA 2 kapısı: kesik {J['kasa']['kesik']}, dosyalar en geç {J['kasa']['dosya']}. Çıktı en geç: {J['en_gec']}.",
         f"Ön kayıt kapısı: {J['onkayit_kapi']}.",
         f"Yeniden üretim (K11): {'TUTTU' if J['yeniden']['tuttu'] else 'TUTMADI'} {J['yeniden']['hucre']}; açık tablo: {J['yeniden']['acik']}.",
         f"Önbellek: {J['onbellek']}.", "", "## Kart etiketleri", "", "| Kart | Etiket | Neden | BH p |", "|---|---|---|---|"]
    for r in Kr.itertuples(index=False):
        L.append(f"| {r.kod} | {r.etiket} | {str(r.neden) if isinstance(r.neden, str) else ''} | {_s(r.bh_p, 4)} |")
    L += ["", "## Huni", "", "```", json.dumps(huni, ensure_ascii=False, indent=1)[:15000], "```", ""]
    for h in ["acik_d1", "acik_d2", "acik_d3", "birikimli"] + list(D["acilan"]):
        if (Hc.hucre == h).any():
            L += [f"## Hücre: {h}", ""] + k2_hucre_tablo(Hc, h) + [""]
    L += ["FARK = R_H - eş ortalaması (yüzde puan); boot ay kümeli (B 2000); TUT+ / TUT- hücre şartları (plasebo hariç; boot düzeyi bakışta %98,33). "
          "Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok."]
    return "\n".join(L) + "\n"


# ================================================================ 12) ÖN KAYIT
def k2_guc_tablo(Hc: pd.DataFrame, egri: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Açık d3 (2016-23, 8 yıl) sıklığından 4 / 8 / 12 blokta beklenen n ve güç (+1 puan; bakış pencereleri 1y / 2y / 3y). Etkin yıl: 1, 2 ve
    2024-01-01 .. 2026-08-31 (kriz kesiği), eksi H / 252 (son H barın olayları ölçülmez)."""
    out = []
    etkin = {4: 1.0, 8: 2.0, 12: (pd.Timestamp(OC.OC_ESIK["kriz"]) - K2_BLOK_BAS).days / 365.25}
    for r in Hc[Hc.hucre == "acik_d3"].itertuples(index=False):
        oran = float(r.n) / 8.0; s = {"kod": r.kod, "pazar": r.pazar, "ufuk": int(r.ufuk), "n_d3": int(r.n)}
        for b, pw in ((4, "1y"), (8, "2y"), (12, "3y")):
            nb = oran * max(0.0, etkin[b] - int(r.ufuk) / 252.0)
            s[f"n{b}"] = int(round(nb)); s[f"guc{b}"] = k2_guc(egri, r.pazar, int(r.ufuk), pw, nb)
        out.append(s)
    return out


def k2_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    L = ["| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = K2_KONTROL[k["kod"]]
        L.append(f"| {k['kod']} | {k.get('madde', k.get('ad', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(L)


def k2_onkayit_metni() -> str:
    a = K2_YOL["acik"]
    J = json.load(open(os.path.join(a, K2_DOSYA["sonuc"]), encoding="utf-8"))
    Hc = pd.read_csv(os.path.join(a, K2_DOSYA["hucre"])); huni = json.load(open(os.path.join(a, K2_DOSYA["huni"]), encoding="utf-8"))
    PR = json.load(open(K2_YOL["prefix"], encoding="utf-8")); GJ = json.load(open(K2_YOL["guc"], encoding="utf-8")); egri = GJ["egri"]
    sha = k2_sha_simdi(); kod = sha["esik"]["KART_TUR2.py"]
    if J["sha"]["esik"]["KART_TUR2.py"] != kod or PR["kod_sha"] != kod:
        raise K2Hata("açık kuru koşu / hazırlık başka bir KART_TUR2.py sürümüyle yapılmış -> ön kayıt yazılmaz (yeniden koş)")
    if not all(r["tutar"] for r in PR["prefix"].values()):
        raise K2Hata("prefix testi tutmamış -> ön kayıt yazılmaz")
    L = ["# KART TURU 2 — ÖN KAYIT (donmuş kod; KASA 2 ile yürüyen ileri test, 2024Q1 .. 2026Q4)", "",
         f"Tarih: {_k2_simdi()}. İş tanımı: arastirma_cikti/kart2/KART_TUR2_IS_TANIMI.md (git {_k2_git(K2_YOL['is_tanimi'])}). Kod: KART_TUR2.py "
         f"(git {_k2_git(K2_YOL['kod'])}).", "",
         f"KASA_HIPOTEZ: {K2_HIPOTEZ}", f"KASA_KOD: KART_TUR2.py {kod}"]
    for y in ("KART_TUR1.py", "YAPI_HEDEF.py", "OLCU_SINAMA.py", "TEZGAH2_DOGRULAMA.py", "ORTAK_CETVEL.py", "DUSUS_SONRASI.py", "GOZ_ETIKET.py",
              "BOFA_IZI.py", "D9_YENIDEN.py", "KASA.py"):
        L.append(f"KASA_KOD: {y} {sha['bagimli'][y]}")
    L += [f"K2_ESIK_SHA: {sha['esik']['K2_ESIK_SHA']}", f"ACIK_TABLO_SHA: {_k2_sha(os.path.join(a, K2_DOSYA['hucre']))}",
          f"GUC_SHA: {_k2_sha(K2_YOL['guc'])}", f"PREFIX_SHA: {_k2_sha(K2_YOL['prefix'])}"]
    for p, m in PR["onbellek"].items():
        for g, s in m["tablo_sha"].items():
            L.append(f"OLAY_ACIK_SHA: {p}|{g} {s}")
    L += ["", "## 1. ANA MODEL KARARLARI (iş tanımından AYNEN)", "", K2_ESIK["kararlar"], "",
          "## 2. Kartlar (tanım ve eşik mevcut modüllerden; yeni eşik yok)", "",
          "| Kart | Yön | Pazar | Karar | Cümle | Tanım (t'de bilinen) | Eşik | Kaynak (modül.fonksiyon) | KART_TUR2 uyarlaması |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, v in K2_KART.items():
        L.append(f"| {k} | {v['yon']} | {', '.join(v['pazar'])} | {'karar' if v['karar'] else 'kontrol (bilgi)'} | {v['cumle']} | {v['tanim']} | "
                 f"{v['esik']} | {v['kaynak']} | {v.get('uyarlama', '')} |")
    L += ["", "Kurulamayan kart: yok (KT00-KT13 tanım ve eşikleri ilgili modül fonksiyonlarıyla birebir; KT10 AVR için sektör verisi yok -> en fazla "
          "ABD-ADAY; BIST bu turda yok).", "", "## 3. Eşik ve dosya sha'ları", "", "| Ad | sha256 |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sha["esik"].items()]
    L += ["", "Bağımlı dosyalar (olc blok açıkken bunların sha'sı aynı değilse DURUR):", ""]
    L += [f"BAGIMLI_SHA: {k} {v}" for k, v in sha["bagimli"].items()]
    L += ["", "Önbellek (repo dışı; /tmp/kart2_onbellek): " + "; ".join(f"{p}: dosya sha {m['dosya_sha']}, satır {m['satir']}"
                                                                         for p, m in PR["onbellek"].items()), "",
          "## 4. Ölçü, hücre, plasebo, güç, BH, Bonferroni (K2_ESIK; aynen)", "",
          f"Havuz: {K2_ESIK['havuz']['tanim']}", "", f"Ölçü: {K2_ESIK['ufuk']['R']}", "", f"Eş: {K2_ESIK['es']['tanim']}", "",
          f"Tekil: {K2_ESIK['tekil']}", "", f"Hücreler: {K2_ESIK['hucre']['tanim']}", "", f"Boot: {K2_ESIK['boot']}", "",
          f"Permütasyon: {K2_ESIK['perm']['tanim']} (R {K2_ESIK['perm']['R']})", "", f"Plasebo: {K2_ESIK['plasebo']['tanim']}", "",
          f"Güç: {K2_ESIK['guc']['tanim']}", "", f"BH: {K2_ESIK['bh']['tanim']} (q {K2_ESIK['bh']['q']}; bakışta {K2_ESIK['bh']['q_bakis']:.4f})", "",
          "## 5. Kart etiketi (işlemsel kural; ANA MODEL KARARI (5)'in kodu)", "", K2_ESIK["etiket"], "",
          "## 6. Kova sınırları (tezgah2_hazirlik.json; KV1 = ATRP tercili x 12 + LQ3 x 4 + F15 çeyreği)", "", "```json",
          json.dumps({p: {k: v for k, v in s.items() if k.startswith("KV1")} for p, s in k2_sinir().items()}, ensure_ascii=False), "```", "",
          "## 7. Bakış takvimi", "",
          "- Ana model blokları sırayla açar (2024Q1 ... 2026Q4); her bloktan sonra olc (BİLGİ, birikimli tablo).",
          "- KARAR BAKIŞI 1: 4. blok (2024Q1-Q4) açıkken; BAKIŞ 2: 8. blok (2024Q1-2025Q4); BAKIŞ 3: 12. blok (2024Q1-2026Q4; veri 31.08.2026'da "
          "kesik).", f"- {K2_ESIK['bakis']['tanim']}", "",
          "## 8. Güç tablosu (yapay iz eğrisi, P2 havuzu, +1 puan; beklenen n = açık 2016-23 sıklığı / 8 yıl x etkin yıl)", "",
          "| Kart | Pazar | H | n açık d3 | 4 blokta n | güç | 8 blokta n | güç | 12 blokta n | güç | karar verebilir (güç >= 0,80) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for g in k2_guc_tablo(Hc, egri):
        kv = [str(i + 1) for i, b in enumerate((4, 8, 12)) if g[f"n{b}"] >= 30 and g[f"guc{b}"] >= 0.80]
        L.append(f"| {g['kod']} | {g['pazar']} | {g['ufuk']} | {g['n_d3']} | {g['n4']} | {_s(g['guc4'])} | {g['n8']} | {_s(g['guc8'])} | "
                 f"{g['n12']} | {_s(g['guc12'])} | {('bakış ' + ', '.join(kv)) if kv else 'hiçbir bakışta'} |")
    L += ["", "Güç eğrisi (yakalama payı; pencere 1y / 2y / 3y boot %98,33, d1-d3 %95; yanlış pozitif = delta 0):", "",
          "| Pazar | H | Pencere | n | yanlış poz. | +0,5 | +1 | +2 |", "|---|---|---|---|---|---|---|---|"]
    for r in egri:
        L.append(f"| {r['pazar']} | {r['H']} | {r['pencere']} | {r['n']} | {_s(r['yanlis_pozitif'])} | {_s(r['guc_0.005'])} | {_s(r['guc_0.01'])} | "
                 f"{_s(r['guc_0.02'])} |")
    L += ["", "Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural); bu, sonuç görülmeden yazılmıştır. Rastgele hisse-gün kart "
          "olaylarından daha dağınık olduğu için güç İYİMSERDİR.", "",
          "## 9. Prefix testi ve DS kopya denetimi (hazırlık; k2_prefix.json)", "", "```json",
          json.dumps({"prefix": PR["prefix"], "ds_kopya": PR["ds_kopya"], "sure_sn": PR["sure"]}, ensure_ascii=False, indent=1), "```", "",
          "## 10. Açık veri kuru koşusu (2001-2023; BİLİNEN VERİ, karar değil)", "",
          f"Çıktı: arastirma_cikti/kart2/acik/. Kesik {J['kesik']}; KASA kapısı {J['kasa']['dosya']}; çıktı en geç {J['en_gec']}; yeniden üretim "
          f"{'TUTTU' if J['yeniden']['tuttu'] else 'TUTMADI'}.", "", "Huni:", "", "```", json.dumps(huni, ensure_ascii=False, indent=1)[:20000], "```", ""]
    for h in ("acik_d1", "acik_d2", "acik_d3"):
        L += [f"### {h}", ""] + k2_hucre_tablo(Hc, h) + [""]
    L += ["## 11. Ana modelin komutları (her blok için sırayla)", "", "```",
          "KASA_DIZIN=/tmp/kasa2 KASA_GIZLI=<gizli anahtar yolu> python KASA.py ac --blok 2024Q1 --hipotez KART_TUR2 "
          "--onkayit arastirma_cikti/kart2/KART_TUR2_ON_KAYIT.md --cikti /tmp/kasa2 --manifest arastirma_cikti/kasa/KASA2_MANIFEST.json",
          "nohup python KART_TUR2.py olc --veri /tmp/kasa2/acik --cikti arastirma_cikti/kart2/2024Q1 --islem 4 > /tmp/k2_2024Q1.log 2>&1 &", "```", "",
          "Sıradaki bloklar: 2024Q2, 2024Q3, 2024Q4 (BAKIŞ 1), 2025Q1 ... 2025Q4 (BAKIŞ 2), 2026Q1 ... 2026Q4 (BAKIŞ 3). Her olc'tan sonra "
          "arastirma_cikti/kasa/KASA_DEFTERI.md ve çıktı klasörü commit edilir. KART_TUR2.py ve bu ön kayıt bu commit'ten sonra DEĞİŞMEZ.", "",
          "## 12. KONTROL LİSTESİ", "", k2_kontrol_tablosu(), ""]
    return "\n".join(L) + "\n"


def k2_onkayit_yaz(uzerine: bool = False) -> str:
    yol = K2_YOL["onkayit"]
    if os.path.exists(yol) and not uzerine:
        raise K2Hata(f"ön kayıt zaten var: {yol}")
    _k2_yaz(yol, k2_onkayit_metni())
    import IZ_KARNE as IK
    IK.ik_kontrol_kapisi(yol)
    return yol


# ================================================================ 13) ÇAKIŞMA KAPISI
def _cakisma_kontrol_k2(_once=_CK_ONCE_K2, _dosya="KART_TUR2.py"):
    """Çakışma kapısı: bu dosya bellekteki k2_ / K2_ / _k2 öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_K2", "_CK_KAYIT", "_cakisma_kontrol_k2", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "subprocess", "_dt", "annotations", "copy", "argparse", "gc",
           "warnings", "zlib", "Any", "Callable", "Dict", "List", "Optional", "Tuple", "DS", "GE", "KT", "KS", "OS", "OC", "T2", "YH")
    onek = ("k2_", "K2_", "_k2", "K2Hata", "K2Havuz", "k2log", "_K2", "KOK_K2", "_Y11E", "_S10E", "_kt1", "_r6", "_y", "_s", "_Y1_")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_k2()

if __name__ == "__main__" and "get_ipython" not in globals():
    ap = argparse.ArgumentParser(description=K2_SURUM)
    ap.add_argument("komut", choices=["olc", "hazirla", "onkayit", "sha", "rapor"])
    ap.add_argument("--veri", default=os.environ.get("K2_VERI", K2_YOL["veri"]))
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
                raise K2Hata("--cikti zorunlu (ör. arastirma_cikti/kart2/2024Q1)")
            R_ = k2_olc(a.veri, a.cikti, a.islem, a.onkayit, a.uzerine_yaz, pazarlar=pz)
            print(R_["karar"].to_string())
        elif a.komut == "hazirla":
            R_ = k2_hazirla(a.veri, a.islem, pz)
            print(json.dumps(_k2_json({"prefix": R_["prefix"], "sure": R_["sure"]}), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(k2_onkayit_yaz(a.uzerine_yaz))
        elif a.komut == "rapor":
            print(k2_rapor_md(a.cikti))
        else:
            print(json.dumps(k2_sha_simdi(), indent=1))
    except (K2Hata, OS.OSHata, T2.T2Hata, DS.DSHata, OC.OCHata, YH.YHHata, GE.GEHata, KS.KasaHata, KT.KTHata) as ex:
        k2log.error("%s", ex); sys.exit(1)
