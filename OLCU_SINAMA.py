"""OLCU_SINAMA — ÖLÇÜ SINAMASI: hangi 15-60 mum ölçüsü bilinen etkiyi (kontrol kartlarını) görüyor? Tek dosya (22 Kasım 2026).

İş tanımı: arastirma_cikti/olcu_sinama/OLCU_SINAMA_IS_TANIMI.md (bölüm 0-6). Bu iş iz aramaz; ÖLÇÜ seçer. Yalnız AÇIK veri (/tmp/kasa/acik;
KASA açık kesik 2023-12-31); her ölçümden önce KASA.kasa_kapisi.

PANEL (nedensel; KENAR_ETKISI_DENETIM.md'deki iki geleceğe bakma düzeltildi):
  (a) min_bar süzgeci YOK: hisse evrene KENDİ 80. geçerli barından SONRA girer (d gününden önceki geçerli bar sayısı >= 80);
  (b) bölünme şüphesi yalnız d-1'e kadarki barlarla: sıçramanın kalıcılığı (10 bar sonrası) henüz bilinmiyorsa (son 10 barda aday sıçrama)
      hisse-gün havuz DIŞI; kalıcılığı bilinen şüpheli gün [d-61, d-1] penceresindeyse havuz dışı (ORTAK_CETVEL ANA kuralı).
  Geçerli bar (H>L, V>0, O/H/L/C>0), açılış H-L kırpması (DS), likidite alt %20 dışlama (evrendeki hisseler kesitinde), giriş t+1 açılış:
  ORTAK_CETVEL / CETVEL2 ile aynı. EVREN PREFIX TESTİ: veri 2022-06-30 ve 2023-12-29'da kesilir; sinyal / havuz günü <= 2022-05-31 olan
  bütün hisse-günlerde havuz, kova ve olay kümeleri BİREBİR aynı olmalı (fark 0); tutmazsa koşu DURUR.
KONTROL KARTLARI (ay sonu, ABD + AVR; d1 2016-19, d2 2020-23): MOM 12-1 (üst onda +, alt onda -), STREV 21 gün (alt onda +, üst onda -),
  HIGH52 (kapanış / 252 gün en yüksek High; üst onda +); PLASEBO (rastgele etiket 200 tohum) ve YAPAY İZ (sürüklenme, 20 tohum).
ADAY ÖLÇÜLER (E0 = t+1 açılış; H 15 / 30 / 60; eş = aynı giriş günü, aynı pazar, aynı kova, olay kümesi dışı, >= 5 eş; KV1 / KV2):
  O1 R_H farkı, O2 sıra - 0,5, O3a T5_H / O3b T10_H dokunma payı farkı, O4 oynaklık ölçekli asimetri, O5 +-1,5 ATRP önce-hedef payı farkı.
SEÇİM KURALI (önceden yazılı; OS_ESIK['secim']).

Komut:  python OLCU_SINAMA.py hazirlik   kova sınırları (2016-22 havuzu, getirisiz) + evren prefix testi -> os_sinir.json, os_prefix.json
        python OLCU_SINAMA.py onkayit    OLCU_SINAMA_ON_KAYIT.md (kontrol tablosu, bölüm 2-5 aynen, sınırlar, sha'lar, KASA kesik)
        python OLCU_SINAMA.py kos [--islem 4]  kapılar (KASA, ön kayıt git + sha + kontrol) -> ölçüm -> olcu_sinama.json + satır dosyaları + rapor
        python OLCU_SINAMA.py rapor      OLCU_SINAMA_RAPOR.md (json'dan)
Colab:  exec(open('OLCU_SINAMA.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Komisyon / kayma YOK. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; STREV alt onda yukarı yanlı görünür) — raporda yazılır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_OS = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_OS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_OS not in sys.path:
    sys.path.insert(0, KOK_OS)

import ORTAK_CETVEL as OC  # noqa: E402  (yalnız oc_veri / oc_veri_hazirla; mühürlü cetvel DEĞİŞTİRİLMEZ)

oslog = logging.getLogger("col.olcu_sinama")
if not oslog.handlers:
    _os_h = logging.StreamHandler(sys.stderr)
    _os_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s olcu_sinama: %(message)s", "%H:%M:%S"))
    oslog.addHandler(_os_h)
    oslog.setLevel(logging.INFO)
    oslog.propagate = False

OS_SURUM = "OLCU_SINAMA v1.0 (2026-11-22)"
OS_YOL = {"cikti": os.path.join(KOK_OS, "arastirma_cikti", "olcu_sinama"), "veri": os.environ.get("OS_VERI", "/tmp/kasa/acik"),
          "kod": os.path.join(KOK_OS, "OLCU_SINAMA.py"), "is_tanimi": os.path.join(KOK_OS, "arastirma_cikti", "olcu_sinama", "OLCU_SINAMA_IS_TANIMI.md"),
          "kasa_dizin": os.environ.get("KASA_DIZIN", "/tmp/kasa")}
OS_DOSYA = {"onkayit": "OLCU_SINAMA_ON_KAYIT.md", "rapor": "OLCU_SINAMA_RAPOR.md", "json": "olcu_sinama.json", "sinir": "os_sinir.json",
            "prefix": "os_prefix.json", "kart": "os_kart_olay_{p}_H{h}.csv.gz", "plasebo": "os_plasebo.csv.gz", "yapay": "os_yapay.csv.gz",
            "klasik": "os_klasik.csv", "kart_hucre": "os_kart_hucre.csv"}

OS_OLCU = ["O1", "O2", "O3a", "O3b", "O4", "O5"]
OS_OLCU_KAYNAK = {"O1": "R", "O2": "R", "O3a": "T5", "O3b": "T10", "O4": "A", "O5": "O5"}
OS_KAYNAK = ["R", "T5", "T10", "A", "O5"]
OS_KOVA = ["KV1", "KV2"]
OS_BACAK = {"MOM+": ("MOM", "ust", "+"), "MOM-": ("MOM", "alt", "-"), "STREV+": ("STREV", "alt", "+"), "STREV-": ("STREV", "ust", "-"),
            "HIGH52+": ("HIGH52", "ust", "+")}
OS_KOVA_K = 36   # anahtar çarpanı (KV1 36 kova, KV2 30 kova)

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
OS_ESIK: Dict[str, Any] = {
    "surum": "OS1.0",
    "veri": {"klasor": "/tmp/kasa/acik (= /tmp/veri = /tmp/veri2); başka fiyat kaynağı YOK", "kesik_tarih": "2023-12-31",
             "pazar": ["ABD", "AVR"], "bist": "kapsam dışı (iş tanımı bölüm 3: ABD ve AVR)",
             "yukle": "OC.oc_veri(pazar, E: min_bar 1, abd_ek_aktif False; k34 YOK) = geçerli bar süzgeci (O/H/L/C > 0 sonlu, H > L, V > 0), ABD "
                      "evren dışı (ETF / fon) listesi; ardından DS açılış kırpması (Open H-L dışındaysa [L, H]'ye kırpılır)",
             "kapi": "KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl) + KASA_DURUM.json açık kesik = kesik_tarih değilse DURUR"},
    "evren": {"gec_bar": 80, "tanim": "hisse d gününde evrende <=> hissenin d'den ÖNCEKİ geçerli bar sayısı >= 80 (min_bar süzgeci yok; veri "
                                      "sonuna kadarki bar sayısı kullanılmaz)"},
    "bolunme": {"esik": 0.25, "geri_gun": 10, "geri_pay": 0.5, "oranlar": [1.5, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25, 30, 40, 50, 100],
                "oran_tol": 0.04, "pencere": 61,
                "tanim": "aday sıçrama (hissenin kendi geçerli kapanışları, bar i): |C_i / C_{i-1} - 1| > 0,25 VE önceki 10 bar düz (|ln C_{i-1} / "
                         "C_{max(0, i-11)}| < 0,5 |ln r_i|) VE |ln r_i| bir bölünme oranının ln'ine +-0,04 yakın (yalnız geçmiş). KALICILIK "
                         "(|ln C_{i+10} / C_{i-1}| >= 0,5 |ln r_i|) ancak bar i+10 d'den önceyse bilinir. Havuz dışı günler: kalıcı aday için "
                         "birleşik takvimde [p_i + 1, max(p_i + 61, p_{i+10})], kalıcı olmayan için [p_i + 1, p_{i+10}] (bekleme: kalıcılık "
                         "bilinene kadar), i+10 veri sonunu aşıyorsa veri sonuna kadar (p = birleşik takvim konumu)"},
    "likidite": {"gun": 20, "min_gun": 10, "alt_kesik": 0.20,
                 "tanim": "C x V (x Kur, EUR) önceki 20 birleşik takvim gününün medyanı (shift 1, en az 10 gün); alt %20 kesiti = d günü evrende, "
                          "geçerli barı ve sonlu likiditesi olan hisseler"},
    "havuz": {"mom": 60, "mom_kova": 5, "likit_kova": 3, "min_havuz": 30,
              "tanim": "ok = d günü geçerli bar VE evrende VE momentum60 (C(d-1) / C(d-61) - 1, birleşik takvim, 5 gün ileri taşıma) sonlu VE "
                       "likidite sonlu VE alt %20 dışı VE bölünme dışı; havuzda >= 30 hisse varsa 5 momentum x 3 likidite (qcut, rank first); "
                       "likidite üçlüsü LQ3 = H % 3 (ORTAK_CETVEL ile aynı)"},
    "giris": {"azami_bosluk": 10, "tanim": "t'den sonraki ilk geçerli bar (hissenin kendi takvimi) AÇILIŞI E0; t ile giriş arası <= 10 birleşik "
                                           "takvim günü; giriş günü havuzda (ok ve H >= 0)"},
    "kova": {"donem": ["2016-01-01", "2022-12-31"], "atrp_gun": 14, "f15_gun": 120, "atrp_q": [1 / 3, 2 / 3], "f15_q": [0.25, 0.50, 0.75],
             "atrp_onda": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
             "KV1": "ATRP tercili x 12 + LQ3 x 4 + F15 çeyreği (CETVEL2 kovası; 36)", "KV2": "ATRP ondalığı x 3 + LQ3 (30; F15 yok)",
             "tanim": "ATRP_t = ort TR [t-13, t] / C_t (TR önceki kapanışla; ilk bar H-L), F15_t = (C_t - min) / (max - min) son 120 geçerli "
                      "kapanış; t = hissenin d'den önceki son geçerli barı. Sınırlar pazar başına havuz hisse-günlerinden (giriş 2016-22, ok VE "
                      "H >= 0 VE ATRP sonlu (KV1 için F15 de)) numpy quantile (doğrusal), getirisiz; os_sinir.json ve ön kayıtta sayı olarak; "
                      "2023 ve prefix testinde aynı sayılar"},
    "es": {"min": 5, "tanim": "aynı giriş günü d, aynı pazar, aynı kova (KV1 ya da KV2), havuzda, o ölçüde ölçülebilir; aynı bacağın o gün olay "
                              "kümesindeki (tekilleştirme ÖNCESİ bütün ondalık üyeleri) hisseler ve olayın kendisi çıkarılır; en az 5 eş"},
    "ufuk": [15, 30, 60], "pencere_kat": 2,
    "olcu": {"R": "R_H = H. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 2H birleşik takvim satırında H geçerli bar "
                  "yoksa ölçülmez (CETVEL2 v2.2 c2_rh ile aynı)",
             "O1": "R_H - eş ortalaması R_H", "O2": "SIRA - 0,5; SIRA = (#eş R_H < olay + 0,5 #eş R_H = olay) / #eş",
             "O3a": "T5_H = H bar içinde maks High >= E0 x 1,05 (olay 0/1 - eş payı)", "O3b": "T10_H = H bar içinde maks High >= E0 x 1,10 (olay - eş payı)",
             "O4": "A_H = [(maks High - E0) - (E0 - min Low)] / (E0 x ATRP14(t)); olay - eş ortalaması (ATRP sonlu ve > 0 değilse ölçülmez)",
             "O5": "+1,5 x ATRP14(t) x E0 hedefi (High >=) -1,5 x ATRP14(t) x E0 stop'tan (Low <=) önce H bar içinde; aynı barda ikisi = stop; "
                   "hiçbiri = 0; olay - eş payı",
             "bar": "H bar = giriş barı dahil H geçerli bar (High / Low giriş barının açılış sonrası)"},
    "hedef": {"T5": 0.05, "T10": 0.10, "o5_kat": 1.5},
    "donem": {"d1": ["2016-01-01", "2019-12-31"], "d2": ["2020-01-01", "2023-12-31"], "tarih": "giriş günü"},
    "kart": {"onda": 0.10, "ay_sonu": "t = birleşik takvimde ayın son günü; hissenin t'de geçerli barı olmalı (kendi bar indeksi k)",
             "MOM": "C_{k-21} / C_{k-252} - 1 (k >= 252)", "STREV": "C_k / C_{k-21} - 1 (k >= 21)",
             "HIGH52": "C_k / maks High_{k-251..k} (k >= 251)",
             "sira": "aynı t kesitinde, giriş günü havuzda olan (ok ve H >= 0) ve değeri sonlu hisseler arasında yüzde sıra (sembol sırasıyla "
                     "rank first, pct): üst onda > 0,90; alt onda <= 0,10",
             "bacak": {"MOM+": "MOM üst onda (+)", "MOM-": "MOM alt onda (-)", "STREV+": "STREV alt onda (+)", "STREV-": "STREV üst onda (-)",
                       "HIGH52+": "HIGH52 üst onda (+)"},
             "tekil": "bacak x H başına: aynı hissede olaylar giriş günü sırasıyla, birleşik takvimde >= H gün arayla (CETVEL2 v2.2: tekil = H); "
                      "eş dışlama kümesi tekilleştirme öncesi bütün bacak üyeleri"},
    "boot": {"B": 2000, "tohum": 2261, "alt": 0.025, "ust": 0.975, "birim": "giriş ayı (ay toplamı ve sayısı yeniden örneklenir)"},
    "perm": {"R": 10000, "tohum": 2263, "tanim": "ay kümeli işaret permütasyonu; yön + / - tek yönlü"},
    "hucre": {"n_min": 30,
              "tutar": "TUTAR(+) = n >= 30 VE ort fark > 0 VE boot alt > 0 VE L3O(+) > 0; TUTAR(-) = n >= 30 VE ort fark < 0 VE boot üst < 0 "
                       "VE L3O(-) < 0. L3O(+) = beklenen + için en olumlu 3 ay (çıkınca ortalamayı en çok düşüren) çıkınca ortalama; L3O(-) "
                       "tersi. Hücre = pazar x dönem (d1 / d2)"},
    "plasebo": {"tohum_sayi": 200, "tohum": 2264, "pay": 0.10, "fark_sd_oran": 0.03, "tutar_pay": 0.07,
                "tanim": "rastgele etiket: her ay sonu giriş günü (t'den sonraki ilk birleşik takvim günü) havuzundan (ok, H >= 0) yerine koymadan "
                         "%10 (round) rastgele hisse = olay; eş dışlama = çekilen küme; aynı ölçü / kova / H cetveli; 200 tohum. GEÇER (hücre) = "
                         "|200 tohum ortalama fark| < 0,03 x SD (SD = hücrenin bütün tohumlardaki olay başı farklarının standart sapması) VE "
                         "TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7 (yön başına)"},
    "yapay": {"delta": [0.0, 0.01, 0.02, 0.03, 0.05], "n": [100, 300, 1000], "tohum_sayi": 20, "tohum": 2265, "n_azami_pay": 2 / 3,
              "karar_delta": 0.02, "karar_pay": 0.80,
              "tanim": "hücrenin ay sonu giriş günleri havuzundan (ok, H >= 0, R_H sonlu, KV1 >= 0, KV2 >= 0) yerine koymadan n hisse-gün; yol "
                       "sürüklemesi: k. geçerli bar (k = 0 giriş barı) High / Low / Close x (1 + delta (k+1) / H), E0 ve ATRP değişmez (POZITIF_KONTROL "
                       "pk_surukle); bütün ölçüler sürüklenmiş yoldan yeniden; eşler dokunulmaz; eş dışlama = çekilen küme; yakalama = TUTAR(+). "
                       "n > 2/3 havuz ise ölçülmez"},
    "secim": {"i": "PLASEBO: ABD ve AVR'nin dört hücresinde (d1, d2) plasebo GEÇER",
              "ii": "YAPAY İZ: +%2 sürüklenmede dört hücrenin her birinde n <= 1000 olan bir n'de yakalama >= %80; n* = dört hücrede >= %80'e "
                    "ulaşan en küçük n'lerin en büyüğü",
              "iii": "OYNAKLIK ÖDÜLÜ YOK: MOM- ve STREV- bacakları ABD / AVR dört hücrenin hiçbirinde TUTAR(+) değil",
              "iv": "BİLİNEN ETKİYİ GÖRÜR: MOM+, STREV+ ya da HIGH52+ bacaklarından en az biri ABD d1 VE ABD d2'de TUTAR(+) (AVR bilgi)",
              "sira": "(1) küçük H önce (15 < 30 < 60); (2) daha çok kontrol kartı bacağı gören (beş bacaktan ABD d1 ve d2'de beklenen yönde TUTAR "
                      "olanların sayısı); (3) daha küçük n*; (4) EK BERABERLİK BOZUCU (sonuç görülmeden, iş tanımında yok): basit ölçü önce "
                      "O1 < O3a < O3b < O2 < O5 < O4, sonra KV2 < KV1",
              "hicbiri": "'bu evren ve eş kurulumunda 15-60 mum ölçüsü bilinen etkiyi göremiyor' + klasik portföy tanısı"},
    "prefix": {"kisa": "2022-06-30", "uzun": "2023-12-29", "son": "2022-05-31",
               "tanim": "iki kesikte panel + kartlar; havuz / sinyal günü <= 2022-05-31 olan bütün hisse-günlerde ok, H (5x3), KV1, KV2 ve bütün "
                        "bacak x H olay kümeleri (sembol, tarih, giriş) birebir; fark 0 beklenir, değilse DURUR"},
    "klasik": {"H": [21, 63], "tanim": "eşsiz ham kesit: ay sonu kart ondalıkları (tekilsiz, havuz evreni), giriş E0, R_H (2H satır kuralı); ay başına "
                                        "eşit ağırlıklı üst onda - alt onda (STREV: alt - üst) ortalama farkı; hücre ortalaması ve Newey-West t "
                                        "(gecikme ceil(H / 21))"},
    "yeniden": {"hucre": [["MOM+", "ABD", "d2", "O1", "KV1", 15], ["STREV+", "ABD", "d1", "O3a", "KV2", 30], ["HIGH52+", "AVR", "d2", "O5", "KV1", 60]],
                "olay": 30, "tohum": 2266,
                "tanim": "üç hücre satır dosyasından düz pandas (n, ort fark); 30 olayın R / T5 / T10 / A / O5 ölçüsü ham pkl'den düz döngüyle; tutmazsa "
                         "koşu TUTMADI"},
}

OS_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı kova (KV1 ATRP x LQ3 x F15 / KV2 ATRP ondalığı x LQ3), bütün havuz, aynı geometri (aynı "
                   "E0, aynı H, aynı ölçü tanımı olay ve eşte); bacak üyeleri ve olay eş dışı; >= 5 eş (os_es); taban rastgele olay sağlaması = "
                   "plasebo 200 tohum (os_plasebo); mekanik üstünlük: O4 / O5 ATRP ölçekli, kova ATRP ile kurulu (oynaklık ödülü şartı iii)"),
    "K2": ("EVET", "evren = kendi 80. geçerli barından sonra (min_bar yok); bölünme kalıcılığı yalnız d-1'e kadar (bilinmiyorsa havuz dışı); "
                   "momentum / likidite / ATRP / F15 d-1'e kadar; kart değerleri t'de; EVREN PREFIX TESTİ (2022-06-30 vs 2023-12-29; <= 2022-05-31 "
                   "ok / H / KV1 / KV2 / olay kümeleri fark 0, os_prefix.json; tutmazsa DURUR); KASA kapısı kesik 2023-12-31"),
    "K3": ("EVET", "OC.oc_veri_hazirla (O/H/L/C > 0 sonlu, H > L, V > 0) + açılış kırpması; ölçüler yalnız geçerli barlar (kendi takvimi); "
                   "kart sinyali t'de geçerli bar ister"),
    "K4": ("EVET", "bacak x H başına aynı hissede >= H birleşik takvim günü arayla tek olay (örtüşmeyen H bar); n = ölçülen olay; boot / "
                   "permütasyon birimi giriş ayı; medyan farkı tabloda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (<= 10 gün boşluk); eşler aynı gün açılışı; test 'giriş'"),
    "K6": ("EVET", "V_*.pkl tek kip (fi_k1_veri düzeltilmiş; KASA bayt bayt bölünmüş açık kısım); ölçüler oran / ATRP ölçekli (birimsiz); "
                   "likidite günlük kesit sırası, AVR x Kur; bölünme şüphesi (nedensel) havuz dışı"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD, V_AVR; batanlar yok): getiriler yukarı yanlı, STREV alt onda yukarı yanlı görünür; "
                   "raporda yazılı; yanlılık olay ve eşte aynı evrende"),
    "K8": ("EVET", "iki alt dönem (d1 2016-19, d2 2020-23) x iki pazar ayrı hücre; n < 30 TUTMAZ; plasebo 200 tohum, yapay iz 20 tohum x 3 n x "
                   "5 delta; seçim kuralı dört şartın hepsi (çoklu karşılaştırma şart birleşimiyle; BH yok, yazılı)"),
    "K9": ("EVET", "OLCU_SINAMA_ON_KAYIT.md: OS_ESIK sha, OLCU_SINAMA.py sha + kod commit, kova sınırları (sayı), prefix sonucu, OC / CETVEL2 / "
                   "KASA / veri sha'ları, KASA açık kesik; os_kapi ön kaydın git'te işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; sıra kod "
                   "commit -> ön kayıt commit -> koşu; seçim kuralı iş tanımından (df0a499) aynen"),
    "K10": ("UYGULANMAZ", "haber / KAP / SEC ayrıştırması yok; yalnız OHLCV açık pkl; kart sinyalleri fiyattan"),
    "K11": ("EVET", "os_yeniden: üç hücre satır dosyasından düz pandas; 30 olayın ölçüleri ham pkl'den düz döngüyle; tutmazsa koşu TUTMADI"),
    "K12": ("EVET", "ölçü seçimi; 'iz' iddiası yok; fark, boot, p, tutar ayrı; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_os; test); OC / CETVEL2 / KASA / kart / kasa / defter dosyalarına dokunulmadı; e-posta / "
                    "anahtar taraması (_os_yaz); indirme yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçü sınaması"),
}


class OSHata(RuntimeError):
    """Durdurucu hata: veri yok, kasa / ön kayıt kapısı kapalı, prefix tutmuyor, yeniden üretim tutmadı."""


# ================================================================ 0) ORTAK
_OS_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_OS_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|sifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def _os_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _os_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def os_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(OS_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def os_kod_sha(yol: Optional[str] = None) -> str:
    return _os_sha_dosya(yol or OS_YOL["kod"])


def _os_yol(ad: str, cikti: Optional[str] = None, **kw: Any) -> str:
    return os.path.join(cikti or OS_YOL["cikti"], OS_DOSYA.get(ad, ad).format(**kw))


def _os_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return [_os_json(x) for x in o.tolist()]
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(pd.Timestamp(o).date())
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return str(o)


def _os_temizle(o: Any) -> Any:
    """json için NaN -> None (iç içe)."""
    if isinstance(o, dict):
        return {str(k): _os_temizle(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_os_temizle(v) for v in o]
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return o


def _os_yaz(yol: str, metin: str, ad: str = "dosya") -> str:
    """Metin dosyası yazar; e-posta / anahtar deseni varsa DURUR (K13)."""
    if _OS_EPOSTA.search(metin) or _OS_ANAHTAR.search(metin):
        raise OSHata(f"{ad}: e-posta / anahtar deseni bulundu, yazılmadı ({yol})")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    oslog.info("%s yazıldı: %s", ad, yol)
    return yol


def _os_tohum(*parca: Any) -> int:
    return zlib.crc32("|".join(str(p) for p in parca).encode("utf-8")) & 0x7FFFFFFF


def _os_donem(g: Any) -> np.ndarray:
    g = pd.to_datetime(pd.Series(g)).to_numpy()
    out = np.full(len(g), "dis", dtype=object)
    for ad, ab in OS_ESIK["donem"].items():
        if ad == "tarih":
            continue
        a, b = ab
        out[(g >= np.datetime64(pd.Timestamp(a))) & (g <= np.datetime64(pd.Timestamp(b)))] = ad
    return out


def _os_git_islenmis(yol: str) -> Dict[str, str]:
    kl, ad = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    try:
        r = subprocess.run(["git", "-C", kl, "log", "-1", "--format=%H %cI", "--", ad], capture_output=True, text=True, timeout=60)
        d = subprocess.run(["git", "-C", kl, "status", "--porcelain", "--", ad], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as ex:
        raise OSHata(f"git çalıştırılamadı ({ex}); {yol} işlenmiş mi doğrulanamadı")
    if r.returncode != 0 or not r.stdout.strip():
        raise OSHata(f"git'e işlenmemiş: {yol} (önce commit)")
    if d.returncode != 0 or d.stdout.strip():
        raise OSHata(f"git'e işlendikten sonra değişmiş: {yol} ({d.stdout.strip() or d.stderr.strip()})")
    h, z = r.stdout.strip().split(" ", 1)
    return {"commit": h, "commit_zamani": z}


# ================================================================ 1) VERİ
def os_veri(pazar: str, klasor: Optional[str] = None, kesik: Optional[Any] = None) -> Dict[str, Any]:
    """OC.oc_veri (min_bar 1: süzgeç yok; k34 yok; evren dışı listesi) + açılış kırpması + isteğe bağlı bellek içi kesik (prefix testi)."""
    if pazar not in OS_ESIK["veri"]["pazar"]:
        raise OSHata(f"bilinmeyen pazar {pazar}")
    klasor = klasor or OS_YOL["veri"]
    if not os.path.exists(os.path.join(klasor, f"V_{pazar}.pkl")):
        raise OSHata(f"veri yok: {klasor}/V_{pazar}.pkl (indirme / worktree YASAK)")
    E1 = copy.deepcopy(OC.OC_ESIK); E1["veri"]["min_bar"] = 1; E1["veri"]["abd_ek_aktif"] = False
    Vd = OC.oc_veri(pazar, E=E1, klasor=klasor, veri2="/nonexistent_os_k34_yok")
    k = pd.Timestamp(kesik) if kesik is not None else None
    V = {}; n_kirp = 0
    for s, d in Vd["V"].items():
        if k is not None:
            d = d[d.index <= k]
            if not len(d):
                continue
        bad = ((d.Open > d.High) | (d.Open < d.Low)).to_numpy()
        if bad.any():
            d = d.copy(); d.loc[bad, "Open"] = np.clip(d.Open.to_numpy(float), d.Low.to_numpy(float), d.High.to_numpy(float))[bad]
            n_kirp += int(bad.sum())
        V[s] = d
    Vd["V"] = V
    Vd["gecersiz"] = {s: (g[g <= k] if k is not None else g) for s, g in Vd["gecersiz"].items() if s in V}
    Vd["not"].append(f"açılış H-L dışı kırpılan bar: {n_kirp}; min_bar süzgeci YOK (evren kendi 80. barından sonra); k34 yok")
    Vd["kesik"] = str(k.date()) if k is not None else None
    oslog.info("%s veri: %d hisse%s", pazar, len(V), f" (kesik {k.date()})" if k is not None else "")
    return Vd


# ================================================================ 2) BÖLÜNME (nedensel)
def os_bolunme_aday(C: np.ndarray, E: Dict[str, Any] = OS_ESIK) -> Tuple[np.ndarray, np.ndarray]:
    """Hissenin kendi kapanışlarında aday sıçrama barları (yalnız geçmiş şartlar) ve kalıcılık (bar i+10 varsa 1/0, yoksa -1 = bilinmiyor)."""
    B = E["bolunme"]; n = len(C); aday, kal = [], []
    if n < 2:
        return np.array([], int), np.array([], int)
    with np.errstate(all="ignore"):
        r = np.r_[np.nan, np.log(C[1:] / C[:-1])]
        cand = np.where(np.abs(np.r_[np.nan, C[1:] / C[:-1] - 1]) > B["esik"])[0]
    for i in cand:
        lr = abs(r[i])
        once = max(0, i - 1 - B["geri_gun"])
        duz_once = abs(math.log(C[i - 1] / C[once])) < B["geri_pay"] * lr
        if not (duz_once and any(abs(lr - math.log(k)) < B["oran_tol"] for k in B["oranlar"])):
            continue
        j = i + B["geri_gun"]
        aday.append(int(i))
        kal.append(-1 if j > n - 1 else int(abs(math.log(C[j] / C[i - 1])) >= B["geri_pay"] * lr))
    return np.array(aday, int), np.array(kal, int)


def os_bolunme_disi(pos: np.ndarray, C: np.ndarray, n: int, E: Dict[str, Any] = OS_ESIK) -> np.ndarray:
    """Birleşik takvimde (n gün) bu hisse için bölünme nedeniyle havuz dışı günler (bool, nedensel)."""
    out = np.zeros(n, bool)
    a, k = os_bolunme_aday(C, E)
    g, w = E["bolunme"]["geri_gun"], E["bolunme"]["pencere"]
    for i, kk in zip(a, k):
        p = int(pos[i])
        if kk < 0:
            out[p + 1:] = True
            continue
        q = int(pos[i + g])
        son = max(p + w, q) if kk == 1 else q
        out[p + 1:min(n, son + 1)] = True
    return out


# ================================================================ 3) PANEL
def _os_atrp_f15(df: pd.DataFrame, E: Dict[str, Any] = OS_ESIK) -> Tuple[np.ndarray, np.ndarray]:
    H, L, C = (df[k].to_numpy(float) for k in ("High", "Low", "Close"))
    pC = np.r_[np.nan, C[:-1]]
    TR = np.where(np.isfinite(pC), np.maximum(H, pC) - np.minimum(L, pC), H - L)
    ag = int(E["kova"]["atrp_gun"]); fg = int(E["kova"]["f15_gun"])
    atrp = pd.Series(TR).rolling(ag, min_periods=ag).mean().to_numpy() / C
    c = pd.Series(C); lo = c.rolling(fg, min_periods=fg).min(); hi = c.rolling(fg, min_periods=fg).max()
    with np.errstate(invalid="ignore", divide="ignore"):
        f15 = ((c - lo) / (hi - lo)).where(hi > lo).to_numpy(float)
    return atrp, f15


def os_kova_sinir(Pn: Dict[str, Any], E: Dict[str, Any] = OS_ESIK) -> Dict[str, Any]:
    """Giriş 2016-22 havuz hisse-günlerinden ATRP tercil / ondalık ve F15 çeyrek sınırları (getirisiz)."""
    idx = Pn["tarih"]; a0, b0 = E["kova"]["donem"]
    sat = ((idx >= pd.Timestamp(a0)) & (idx <= pd.Timestamp(b0)))[:, None]
    m2 = Pn["ok"] & (Pn["H"] >= 0) & np.isfinite(Pn["ATRP"]) & sat
    m1 = m2 & np.isfinite(Pn["F15"])
    a1, f1, a2 = Pn["ATRP"][m1], Pn["F15"][m1], Pn["ATRP"][m2]
    if len(a1) < 1000 or len(a2) < 1000:
        raise OSHata(f"{Pn['pazar']}: 2016-22 havuzunda kova sınırı için yeterli hisse-gün yok ({len(a1)} / {len(a2)})")
    K = E["kova"]
    return {"KV1_ATRP": [float(np.quantile(a1, q)) for q in K["atrp_q"]], "KV1_F15": [float(np.quantile(f1, q)) for q in K["f15_q"]],
            "KV2_ATRP": [float(np.quantile(a2, q)) for q in K["atrp_onda"]], "n_KV1": int(len(a1)), "n_KV2": int(len(a2))}


def os_kova(Pn: Dict[str, Any], sinir: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    A, F, LQ = Pn["ATRP"], Pn["F15"], Pn["LQ3"]
    pool = Pn["ok"] & (Pn["H"] >= 0)
    t1, t2 = sinir["KV1_ATRP"]; q1, q2, q3 = sinir["KV1_F15"]
    with np.errstate(invalid="ignore"):
        at = np.where(A <= t1, 0, np.where(A <= t2, 1, 2))
        fq = np.where(F <= q1, 0, np.where(F <= q2, 1, np.where(F <= q3, 2, 3)))
        dec = np.searchsorted(np.asarray(sinir["KV2_ATRP"], float), np.where(np.isfinite(A), A, 0.0), side="left")
    KV1 = np.where(pool & np.isfinite(A) & np.isfinite(F) & (LQ >= 0), at * 12 + LQ * 4 + fq, -1)
    KV2 = np.where(pool & np.isfinite(A) & (LQ >= 0), dec * 3 + LQ, -1)
    return KV1.astype(np.int64), KV2.astype(np.int64)


def os_panel(Vd: Dict[str, Any], sinir: Optional[Dict[str, Any]] = None, E: Dict[str, Any] = OS_ESIK) -> Dict[str, Any]:
    """Nedensel panel: birleşik takvim (bütün geçerli barların birleşimi) x hisse. Döner: tablolar, havuz (ok), H, LQ3, ATRP(t), F15(t), KV1, KV2,
    hissenin kendi bar deposu (ölçüler için)."""
    t0 = time.time()
    V = Vd["V"]; S = sorted(V)
    if not S:
        raise OSHata("panel: boş veri")
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    n, u = len(idx), len(S)
    Hv = E["havuz"]; Lk = E["likidite"]

    def tablo(kol):
        return pd.DataFrame({s: V[s][kol] for s in S}).reindex(idx).to_numpy(float)
    Op, Cl = tablo("Open"), tablo("Close")
    Tl = pd.DataFrame({s: V[s].Close * V[s].Volume * V[s].Kur for s in S}).reindex(idx)
    Cf = pd.DataFrame(Cl).ffill(limit=5).to_numpy()
    M = np.full((n, u), np.nan)
    if n > Hv["mom"] + 1:
        with np.errstate(all="ignore"):
            M[Hv["mom"] + 1:] = Cf[Hv["mom"]:-1] / Cf[:-Hv["mom"] - 1] - 1
    Lq = Tl.rolling(Lk["gun"], min_periods=Lk["min_gun"]).median().shift(1).to_numpy()
    gec = np.isfinite(Op) & (Op > 0)
    nbar = np.vstack([np.zeros((1, u)), np.cumsum(gec, axis=0)[:-1]])       # d'den önceki geçerli bar sayısı
    evren = nbar >= E["evren"]["gec_bar"]
    # hissenin kendi bar deposu + nedensel bölünme
    sup = np.zeros((n, u), bool); ATRP = np.full((n, u), np.nan); F15 = np.full((n, u), np.nan); EIX = np.full((n, u), -1, np.int64)
    off = np.zeros(u + 1, np.int64); O_l, H_l, L_l, C_l, AP_l, P_l = [], [], [], [], [], []
    for j, s in enumerate(S):
        df = V[s]; pos = idx.get_indexer(df.index)
        if (pos < 0).any():
            raise OSHata(f"{s}: hisse takvimi panelde yok")
        C = df.Close.to_numpy(float)
        sup[:, j] = os_bolunme_disi(pos, C, n, E)
        atrp, f15 = _os_atrp_f15(df, E)
        m = len(pos)
        if m > 1:
            ATRP[pos[1:], j] = atrp[:-1]; F15[pos[1:], j] = f15[:-1]
        EIX[pos, j] = np.arange(m)
        ap = np.r_[np.nan, atrp[:-1]]
        O_l.append(df.Open.to_numpy(float)); H_l.append(df.High.to_numpy(float)); L_l.append(df.Low.to_numpy(float)); C_l.append(C)
        AP_l.append(ap); P_l.append(pos.astype(np.int64)); off[j + 1] = off[j] + m
    dep = {"O": np.concatenate(O_l), "H": np.concatenate(H_l), "L": np.concatenate(L_l), "C": np.concatenate(C_l), "AP": np.concatenate(AP_l),
           "POS": np.concatenate(P_l), "off": off, "m": np.diff(off)}
    taban = gec & np.isfinite(Lq) & evren
    lik_alt = np.zeros((n, u), bool)
    for d in range(n):
        g = taban[d]
        if g.sum() < 2:
            continue
        q = np.quantile(Lq[d, g], Lk["alt_kesik"])
        lik_alt[d] = g & (Lq[d] < q)
    ok = gec & evren & np.isfinite(M) & np.isfinite(Lq) & ~sup & ~lik_alt
    Hc = np.full((n, u), -1, np.int64)
    for d in range(n):
        g = ok[d]
        if g.sum() < Hv["min_havuz"]:
            continue
        mq = pd.qcut(pd.Series(M[d, g]).rank(method="first"), Hv["mom_kova"], labels=False).to_numpy()
        lq = pd.qcut(pd.Series(Lq[d, g]).rank(method="first"), Hv["likit_kova"], labels=False).to_numpy()
        Hc[d, g] = mq * Hv["likit_kova"] + lq
    Pn = {"pazar": Vd.get("pazar", "?"), "tarih": idx, "sembol": S, "kol": {s: i for i, s in enumerate(S)}, "Op": Op, "Cl": Cl, "M": M, "Lq": Lq,
          "gec": gec, "evren": evren, "sup": sup, "lik_alt": lik_alt, "ok": ok, "H": Hc, "LQ3": np.where(Hc >= 0, Hc % 3, -1), "ATRP": ATRP,
          "F15": F15, "EIX": EIX, "dep": dep, "kesik": Vd.get("kesik"), "not": list(Vd.get("not", []))}
    if sinir is None:
        sinir = os_kova_sinir(Pn, E)
    Pn["sinir"] = sinir
    Pn["KV1"], Pn["KV2"] = os_kova(Pn, sinir)
    oslog.info("%s panel: %d gün x %d hisse, havuz %d hisse-gün, KV1 %d, KV2 %d (%.0f sn)", Pn["pazar"], n, u, int((ok & (Hc >= 0)).sum()),
               int((Pn["KV1"] >= 0).sum()), int((Pn["KV2"] >= 0).sum()), time.time() - t0)
    return Pn


# ================================================================ 4) ÖLÇÜLER
def os_olcu_hesap(dep: Dict[str, np.ndarray], jj: np.ndarray, ee: np.ndarray, H: int, delta: float = 0.0,
                  E: Dict[str, Any] = OS_ESIK, parca: int = 100000) -> Dict[str, np.ndarray]:
    """Olaylar (hisse j, kendi bar indeksi e = giriş barı) için R / T5 / T10 / A / O5 (H bar, 2H satır kuralı); delta > 0 ise yol sürüklemesi
    (k. geçerli bar x (1 + delta (k+1) / H); E0 ve ATRP değişmez). Ölçülemeyen NaN."""
    jj = np.asarray(jj, np.int64); ee = np.asarray(ee, np.int64); N = len(jj); H = int(H)
    out = {k: np.full(N, np.nan) for k in OS_KAYNAK}
    if N == 0:
        return out
    m = dep["m"][jj]; Rz = int(E["pencere_kat"]) * H; hd = E["hedef"]
    val = (ee >= 0) & (ee + H - 1 < m)
    g_all = dep["off"][jj] + ee
    val[val] &= (dep["POS"][g_all[val] + H - 1] - dep["POS"][g_all[val]]) <= Rz - 1
    vi = np.flatnonzero(val)
    f = 1.0 + float(delta) * (np.arange(H) + 1) / H
    for a in range(0, len(vi), parca):
        ii = vi[a:a + parca]; g = g_all[ii]; W = g[:, None] + np.arange(H)[None, :]
        Hw = dep["H"][W] * f; Lw = dep["L"][W] * f
        E0 = dep["O"][g]; atr = dep["AP"][g]; cH = dep["C"][g + H - 1] * (1.0 + float(delta))
        mx = Hw.max(1); mn = Lw.min(1)
        out["R"][ii] = cH / E0 - 1.0
        out["T5"][ii] = (mx >= E0 * (1.0 + hd["T5"])).astype(float)
        out["T10"][ii] = (mx >= E0 * (1.0 + hd["T10"])).astype(float)
        aok = np.isfinite(atr) & (atr > 0)
        with np.errstate(invalid="ignore", divide="ignore"):
            A = ((mx - E0) - (E0 - mn)) / (E0 * atr)
            up = E0 * (1.0 + hd["o5_kat"] * atr); dn = E0 * (1.0 - hd["o5_kat"] * atr)
            hu = Hw >= up[:, None]; hdn = Lw <= dn[:, None]
        ku = np.where(hu.any(1), hu.argmax(1), H); kd = np.where(hdn.any(1), hdn.argmax(1), H)
        o5 = ((ku < H) & (ku < kd)).astype(float)
        out["A"][ii] = np.where(aok, A, np.nan); out["O5"][ii] = np.where(aok, o5, np.nan)
    return out


def os_olcu_matris(Pn: Dict[str, Any], H: int) -> Dict[str, np.ndarray]:
    """Bütün hisse-günler için ölçü matrisleri (giriş günü d x hisse)."""
    dep = Pn["dep"]; u = len(Pn["sembol"]); n = len(Pn["tarih"])
    jj = np.repeat(np.arange(u), dep["m"]); ee = np.concatenate([np.arange(k) for k in dep["m"]])
    o = os_olcu_hesap(dep, jj, ee, H)
    X = {}
    for k in OS_KAYNAK:
        Mx = np.full((n, u), np.nan); Mx[dep["POS"], jj] = o[k]; X[k] = Mx
    return X


# ================================================================ 5) EŞ HAVUZU (CETVEL2 c2_es algoritması, genel ölçü / kova)
def os_havuz(X: np.ndarray, KV: np.ndarray) -> Dict[str, Any]:
    pm = (KV >= 0) & np.isfinite(X)
    dd, jj = np.nonzero(pm)
    key = dd.astype(np.int64) * OS_KOVA_K + KV[dd, jj].astype(np.int64); r = X[dd, jj]
    o = np.lexsort((r, key)); dd, jj, key, r = dd[o], jj[o], key[o], r[o]
    uv = np.unique(r); rk = np.searchsorted(uv, r).astype(np.int64); M = np.int64(2 * len(uv) + 2)
    code = key * M + 2 * rk + 1
    if len(code) > 1 and not (np.diff(code) >= 0).all():
        raise OSHata("havuz kodu sıralı değil")
    pix = np.full(KV.shape, -1, np.int64); pix[dd, jj] = np.arange(len(dd))
    return {"KV": KV, "key": key, "r": r, "uv": uv, "M": M, "code": code, "cs": np.r_[0.0, np.cumsum(r)], "pix": pix}


def os_es(hv: Dict[str, Any], d: np.ndarray, j: np.ndarray, x: np.ndarray, exc_d: Optional[np.ndarray] = None,
          exc_j: Optional[np.ndarray] = None, es_min: Optional[int] = None) -> Dict[str, np.ndarray]:
    """Eş ortalaması / SIRA / sayı. Eş = aynı (d, kova) havuzu eksi dışlananlar (exc ∪ olayların kendisi). x olayın (sürüklenmiş olabilir) değeri."""
    d = np.asarray(d, np.int64); j = np.asarray(j, np.int64); x = np.asarray(x, float); ne = len(d)
    me = int(es_min or OS_ESIK["es"]["min"]); K = OS_KOVA_K
    out = {"es": np.full(ne, np.nan), "sira": np.full(ne, np.nan), "n_es": np.zeros(ne)}
    if ne == 0:
        return out
    kv = hv["KV"][d, j].astype(np.int64); key = d * K + kv
    hk, code, cs, uv, M = hv["key"], hv["code"], hv["cs"], hv["uv"], hv["M"]
    lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right")
    N = (hi - lo).astype(float); Ssum = cs[hi] - cs[lo]
    xf = np.where(np.isfinite(x), x, 0.0)
    gl = np.searchsorted(uv, xf, "left").astype(np.int64); gr = np.searchsorted(uv, xf, "right").astype(np.int64)
    less = (np.searchsorted(code, key * M + 2 * gl + 1, "left") - lo).astype(float)
    le = (np.searchsorted(code, key * M + 2 * gr + 1, "left") - lo).astype(float)
    eq = le - less
    ed = d if exc_d is None else np.r_[np.asarray(exc_d, np.int64), d]
    ej = j if exc_j is None else np.r_[np.asarray(exc_j, np.int64), j]
    pp = hv["pix"][ed, ej]; pp = np.unique(pp[pp >= 0])
    if len(pp):
        xk = hk[pp]; xr = hv["r"][pp]; o = np.argsort(xk, kind="stable"); xk, xr = xk[o], xr[o]
        a = np.searchsorted(xk, key, "left"); b = np.searchsorted(xk, key, "right"); c = b - a
        tot = int(c.sum())
        if tot:
            ii = np.repeat(np.arange(ne), c)
            kk = np.arange(tot) - np.repeat(np.cumsum(c) - c, c) + np.repeat(a, c)
            rr = xr[kk]; xi = xf[ii]
            N -= np.bincount(ii, minlength=ne); Ssum -= np.bincount(ii, weights=rr, minlength=ne)
            less -= np.bincount(ii, weights=(rr < xi).astype(float), minlength=ne)
            eq -= np.bincount(ii, weights=(rr == xi).astype(float), minlength=ne)
    ok = (kv >= 0) & np.isfinite(x) & (N >= me)
    with np.errstate(invalid="ignore", divide="ignore"):
        es = Ssum / N; sira = (less + 0.5 * eq) / N
    out["es"] = np.where(ok, es, np.nan); out["sira"] = np.where(ok, sira, np.nan); out["n_es"] = np.where(kv >= 0, N, 0.0)
    return out


def os_fark(olcu: str, x: np.ndarray, e: Dict[str, np.ndarray]) -> np.ndarray:
    """Ölçü farkı: O2 = SIRA - 0,5; öteki = x - eş ortalaması."""
    if olcu == "O2":
        return e["sira"] - 0.5
    return x - e["es"]


# ================================================================ 6) HÜCRE İSTATİSTİĞİ
def os_hucre(f: np.ndarray, ay: np.ndarray, yon: str = "+", tohum_ek: int = 0, perm: bool = False, B: Optional[int] = None) -> Dict[str, Any]:
    """f: olay başı fark; ay: giriş ayı kodu. n, ort, medyan, sd, ay kümeli boot %95, L3O(+/-), p (isteğe bağlı), TUTAR(+), TUTAR(-)."""
    f = np.asarray(f, float); ay = np.asarray(ay); m = np.isfinite(f); f, ay = f[m], ay[m]; n = int(len(f))
    c: Dict[str, Any] = {"n": n, "fark": np.nan, "med": np.nan, "sd": np.nan, "boot_alt": np.nan, "boot_ust": np.nan, "l3o_p": np.nan,
                         "l3o_n": np.nan, "p": np.nan, "ay": 0, "tutar_p": False, "tutar_n": False}
    if n == 0:
        return c
    c.update({"fark": float(f.mean()), "med": float(np.median(f)), "sd": float(f.std(ddof=1)) if n > 1 else np.nan})
    ua, inv = np.unique(ay, return_inverse=True); K = len(ua); c["ay"] = int(K)
    s = np.bincount(inv, weights=f, minlength=K); nn = np.bincount(inv, minlength=K).astype(float)
    Bb = int(B or OS_ESIK["boot"]["B"]); rng = np.random.default_rng([int(OS_ESIK["boot"]["tohum"]), int(tohum_ek) % (2 ** 31)])
    W = rng.multinomial(K, np.full(K, 1.0 / K), size=Bb).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        mb = (W @ s) / (W @ nn)
    mb = mb[np.isfinite(mb)]
    if len(mb):
        c["boot_alt"] = float(np.quantile(mb, OS_ESIK["boot"]["alt"])); c["boot_ust"] = float(np.quantile(mb, OS_ESIK["boot"]["ust"]))
    if K > 3:
        with np.errstate(invalid="ignore", divide="ignore"):
            tek = (s.sum() - s) / (nn.sum() - nn)
        tek = np.where(np.isfinite(tek), tek, np.nan)
        op = np.argsort(np.where(np.isfinite(tek), tek, np.inf), kind="stable")[:3]
        on = np.argsort(np.where(np.isfinite(tek), -tek, np.inf), kind="stable")[:3]
        kp = np.ones(K, bool); kp[op] = False; kn = np.ones(K, bool); kn[on] = False
        c["l3o_p"] = float(s[kp].sum() / nn[kp].sum()); c["l3o_n"] = float(s[kn].sum() / nn[kn].sum())
    if perm:
        R = int(OS_ESIK["perm"]["R"]); rp = np.random.default_rng([int(OS_ESIK["perm"]["tohum"]), int(tohum_ek) % (2 ** 31)])
        eps = rp.choice(np.array([-1.0, 1.0]), size=(R, K)); T = s.sum() / n; Ts = (eps @ s) / n
        k = int((Ts >= T - 1e-15).sum()) if yon == "+" else int((Ts <= T + 1e-15).sum()) if yon == "-" else int((np.abs(Ts) >= abs(T) - 1e-15).sum())
        c["p"] = float((1 + k) / (R + 1))
    nm = OS_ESIK["hucre"]["n_min"]
    c["tutar_p"] = bool(n >= nm and c["fark"] > 0 and np.isfinite(c["boot_alt"]) and c["boot_alt"] > 0 and np.isfinite(c["l3o_p"]) and c["l3o_p"] > 0)
    c["tutar_n"] = bool(n >= nm and c["fark"] < 0 and np.isfinite(c["boot_ust"]) and c["boot_ust"] < 0 and np.isfinite(c["l3o_n"]) and c["l3o_n"] < 0)
    return c


def _os_ay(Pn: Dict[str, Any], d: np.ndarray) -> np.ndarray:
    t = Pn["tarih"][np.asarray(d, np.int64)]
    return (t.year * 12 + t.month).to_numpy() if hasattr(t, "year") else np.array([], int)


# ================================================================ 7) KONTROL KARTLARI
def os_ay_sonu(Pn: Dict[str, Any]) -> Tuple[pd.DatetimeIndex, np.ndarray]:
    """Birleşik takvimde ay sonu günleri ve her birinin ertesi birleşik takvim günü indeksi (plasebo / yapay iz günleri)."""
    idx = Pn["tarih"]
    ays = pd.DatetimeIndex(pd.Series(idx, index=idx).groupby(idx.to_period("M")).max().to_numpy())
    dt = idx.searchsorted(ays, side="right")
    return ays, dt


def os_kart_sinyal(Pn: Dict[str, Any], E: Dict[str, Any] = OS_ESIK) -> pd.DataFrame:
    """Ay sonu adayları: sembol, j, tarih t, k, giriş d, MOM / STREV / HIGH52, havuzda (ok, H >= 0), ondalık bacak bayrakları."""
    dep = Pn["dep"]; idx = Pn["tarih"]; S = Pn["sembol"]; ays, _ = os_ay_sonu(Pn)
    aypos = idx.get_indexer(ays); bos = int(E["giris"]["azami_bosluk"]); sat = []
    for j, s in enumerate(S):
        a, b = dep["off"][j], dep["off"][j + 1]; pos = dep["POS"][a:b]; C = dep["C"][a:b]; Hh = dep["H"][a:b]; m = b - a
        k = np.flatnonzero(np.isin(pos, aypos))
        k = k[k + 1 < m]
        if not len(k):
            continue
        d = pos[k + 1]; dt = pos[k] + 1
        k = k[(d - dt + 1) <= bos]; d = pos[k + 1]
        if not len(k):
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            mom = np.where(k >= 252, C[np.maximum(k - 21, 0)] / C[np.maximum(k - 252, 0)] - 1, np.nan)
            st = np.where(k >= 21, C[k] / C[np.maximum(k - 21, 0)] - 1, np.nan)
            hmax = pd.Series(Hh).rolling(252, min_periods=252).max().to_numpy()
            h52 = np.where(k >= 251, C[k] / hmax[k], np.nan)
        sat.append(pd.DataFrame({"sembol": s, "j": j, "tarih": idx[pos[k]], "k": k, "d": d, "MOM": mom, "STREV": st, "HIGH52": h52}))
    X = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=["sembol", "j", "tarih", "k", "d", "MOM", "STREV", "HIGH52"])
    X["havuz"] = Pn["ok"][X.d.to_numpy(np.int64), X.j.to_numpy(np.int64)] & (Pn["H"][X.d.to_numpy(np.int64), X.j.to_numpy(np.int64)] >= 0)
    X = X.sort_values(["tarih", "sembol"], kind="mergesort").reset_index(drop=True)
    q = float(E["kart"]["onda"])
    for kart in ("MOM", "STREV", "HIGH52"):
        g = X.havuz & np.isfinite(X[kart])
        rk = X[kart].where(g).groupby(X.tarih).rank(method="first", pct=True)
        X[f"{kart}_ust"] = (rk > 1 - q).fillna(False).to_numpy(bool)
        X[f"{kart}_alt"] = (rk <= q).fillna(False).to_numpy(bool)
    return X


def os_tekil(X: pd.DataFrame, H: int) -> np.ndarray:
    """Aynı hissede giriş günü sırasıyla >= H birleşik takvim günü arayla ilk olay (bool, X sırasına göre)."""
    if not len(X):
        return np.zeros(0, bool)
    o = np.lexsort((X.d.to_numpy(np.int64), X.sembol.astype(str).to_numpy()))
    s = X.sembol.astype(str).to_numpy()[o]; d = X.d.to_numpy(np.int64)[o]; tut = np.zeros(len(X), bool); son: Dict[str, int] = {}
    for i, (ss, dd) in enumerate(zip(s, d)):
        if ss not in son or dd - son[ss] >= H:
            tut[o[i]] = True; son[ss] = dd
    return tut


def os_bacak_olay(X: pd.DataFrame, bacak: str, H: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Bacak üyeleri (tekil öncesi; eş dışlama kümesi) ve tekil olaylar."""
    kart, uc, _ = OS_BACAK[bacak]
    U = X[X[f"{kart}_{uc}"].to_numpy(bool)].reset_index(drop=True)
    return U, U[os_tekil(U, H)].reset_index(drop=True)


# ================================================================ 8) PREFIX TESTİ
def os_prefix(Pk: Dict[str, Any], Pu: Dict[str, Any], son: Optional[str] = None) -> Dict[str, Any]:
    """Kısa (Pk) ve uzun (Pu) kesik panelleri: havuz / sinyal günü <= son olan hisse-günlerde ok, H, KV1, KV2, ATRP, F15 ve olay kümeleri."""
    son_t = pd.Timestamp(son or OS_ESIK["prefix"]["son"])
    ik, iu = Pk["tarih"], Pu["tarih"]
    nk = int(ik.searchsorted(son_t, side="right"))
    if not ik[:nk].equals(iu[:nk]):
        return {"tutar": False, "neden": "birleşik takvim öneki farklı", "fark": {}}
    cu = [Pu["kol"].get(s, -1) for s in Pk["sembol"]]
    yeni = [s for s in Pu["sembol"] if s not in Pk["kol"]]
    fark: Dict[str, int] = {}
    cu_a = np.array(cu)
    if (cu_a < 0).any():
        return {"tutar": False, "neden": "kısa veride olup uzunda olmayan sembol", "fark": {}}
    for k in ("ok", "H", "KV1", "KV2", "sup", "lik_alt", "evren"):
        a = Pk[k][:nk]; b = Pu[k][:nk][:, cu_a]
        fark[k] = int((a != b).sum())
        if yeni:   # uzunda olup kısada olmayan hisseler: önekte havuzda OLMAMALI
            yb = Pu[k][:nk][:, [Pu["kol"][s] for s in yeni]]
            fark[k + "_yeni"] = int((yb != (False if Pu[k].dtype == bool else -1)).sum()) if k in ("ok", "H", "KV1", "KV2") else 0
    for k in ("ATRP", "F15", "Lq", "M"):
        a = Pk[k][:nk]; b = Pu[k][:nk][:, cu_a]; na, nb = np.isnan(a), np.isnan(b)
        fark[k] = int((na != nb).sum() + (~np.isclose(a[~na & ~nb], b[~na & ~nb], rtol=1e-12, atol=0)).sum())
    Xk, Xu = os_kart_sinyal(Pk), os_kart_sinyal(Pu)
    olay: Dict[str, Any] = {}
    for b in OS_BACAK:
        for H in OS_ESIK["ufuk"]:
            _, Tk = os_bacak_olay(Xk, b, H); _, Tu = os_bacak_olay(Xu, b, H)
            sk = set(zip(Tk.sembol[Tk.tarih <= son_t], Tk.tarih[Tk.tarih <= son_t], Pk["tarih"][Tk.d[Tk.tarih <= son_t].to_numpy(np.int64)]))
            su = set(zip(Tu.sembol[Tu.tarih <= son_t], Tu.tarih[Tu.tarih <= son_t], Pu["tarih"][Tu.d[Tu.tarih <= son_t].to_numpy(np.int64)]))
            olay[f"{b}_H{H}"] = {"n_kisa": len(sk), "n_uzun": len(su), "fark": len(sk ^ su)}
    toplam = sum(v for v in fark.values()) + sum(v["fark"] for v in olay.values())
    return {"tutar": toplam == 0, "son": str(son_t.date()), "n_gun": nk, "n_hisse_kisa": len(Pk["sembol"]), "n_hisse_uzun": len(Pu["sembol"]),
            "yeni_hisse": len(yeni), "fark": fark, "olay": olay, "toplam_fark": int(toplam),
            "havuz_kisa": int((Pk["ok"][:nk] & (Pk["H"][:nk] >= 0)).sum())}


# ================================================================ 9) HAZIRLIK (getirisiz) ve ÖN KAYIT
def os_hazirlik(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Kova sınırları (açık veri 2016-22 havuzu) + evren prefix testi (iki kesik). Getiri kullanmaz."""
    c = cikti or OS_YOL["cikti"]; sinir, pre = {}, {}
    os_kasa_kapi(veri)
    for p in OS_ESIK["veri"]["pazar"]:
        Vu = os_veri(p, veri)
        Pu = os_panel(Vu); sinir[p] = Pu["sinir"]
        Vk = os_veri(p, veri, kesik=OS_ESIK["prefix"]["kisa"])
        Pk = os_panel(Vk, sinir[p])
        pr = os_prefix(Pk, Pu); pre[p] = pr
        oslog.info("%s prefix: %s (toplam fark %s)", p, "TUTTU" if pr["tutar"] else "TUTMADI", pr.get("toplam_fark"))
        del Pu, Pk, Vu, Vk
    _os_yaz(_os_yol("sinir", c), json.dumps(_os_temizle({"surum": OS_SURUM, "esik_sha": os_esik_sha(), "sinir": sinir}), ensure_ascii=False,
                                            indent=1, default=_os_json), "kova sınırları")
    _os_yaz(_os_yol("prefix", c), json.dumps(_os_temizle({"surum": OS_SURUM, "prefix": pre}), ensure_ascii=False, indent=1, default=_os_json),
            "prefix")
    bozuk = [p for p, r in pre.items() if not r["tutar"]]
    if bozuk:
        raise OSHata(f"EVREN PREFIX TESTİ TUTMADI: {bozuk} -> DURDU ({_os_yol('prefix', c)})")
    return {"sinir": sinir, "prefix": pre}


def os_kasa_kapi(veri: Optional[str] = None) -> Dict[str, Any]:
    import KASA as _KS
    v = veri or OS_YOL["veri"]
    try:
        dur = _KS._durum_oku(OS_YOL["kasa_dizin"])
    except Exception as ex:   # kasa durumu okunamazsa ölçüm başlamaz (fail-closed)
        raise OSHata(f"KASA durumu okunamadı: {type(ex).__name__}: {ex}") from ex
    if pd.Timestamp(dur["acik_kesik"]) != pd.Timestamp(OS_ESIK["veri"]["kesik_tarih"]):
        raise OSHata(f"KASA açık kesik {dur['acik_kesik']} != {OS_ESIK['veri']['kesik_tarih']} -> DURDU")
    try:
        r = _KS.kasa_kapisi([os.path.join(v, f"V_{p}.pkl") for p in OS_ESIK["veri"]["pazar"]], cikti=OS_YOL["kasa_dizin"])
    except Exception as ex:
        raise OSHata(f"KASA kapısı KAPALI: {ex}") from ex
    return r


def os_sha_simdi(veri: Optional[str] = None) -> Dict[str, str]:
    v = veri or OS_YOL["veri"]
    out = {"OS_ESIK_SHA": os_esik_sha(), "OS_KOD_SHA": os_kod_sha(), "OC_KOD_SHA": _os_sha_dosya(os.path.join(KOK_OS, "ORTAK_CETVEL.py")),
           "CETVEL2_KOD_SHA": _os_sha_dosya(os.path.join(KOK_OS, "CETVEL2.py")), "KASA_KOD_SHA": _os_sha_dosya(os.path.join(KOK_OS, "KASA.py")),
           "IS_TANIMI_SHA": _os_sha_dosya(OS_YOL["is_tanimi"])}
    for p in OS_ESIK["veri"]["pazar"]:
        out[f"V_{p}_SHA"] = _os_sha_dosya(os.path.join(v, f"V_{p}.pkl"))
    out["KASA_DURUM_SHA"] = _os_sha_dosya(os.path.join(OS_YOL["kasa_dizin"], "acik", "KASA_DURUM.json"))
    for k in ("sinir", "prefix"):
        y = _os_yol(k)
        if os.path.exists(y):
            out[f"{k.upper()}_JSON_SHA"] = _os_sha_dosya(y)
    return out


def _os_is_tanimi_bolum(bas: str = "## 2.", son: str = "## 6.") -> str:
    t = open(OS_YOL["is_tanimi"], encoding="utf-8").read()
    a = t.find(bas); b = t.find(son)
    if a < 0 or b < 0:
        raise OSHata("iş tanımı bölüm 2-5 bulunamadı")
    return t[a:b].rstrip()


def os_onkayit_metni(veri: Optional[str] = None) -> str:
    sh = os_sha_simdi(veri)
    S = json.load(open(_os_yol("sinir"), encoding="utf-8")); Pr = json.load(open(_os_yol("prefix"), encoding="utf-8"))
    kod_git = _os_git_islenmis(OS_YOL["kod"])
    L = [f"# ÖLÇÜ SINAMASI — ÖN KAYIT ({_os_simdi()})", "",
         f"Sürüm: {OS_SURUM}. İş tanımı: arastirma_cikti/olcu_sinama/OLCU_SINAMA_IS_TANIMI.md (sha {sh['IS_TANIMI_SHA']}).",
         f"Kod: OLCU_SINAMA.py git {kod_git['commit']} {kod_git['commit_zamani']}. Bu dosya koşudan ÖNCE commit edilir; os_kapi git kaydını, değişmemişliği, "
         "sha'ları ve kontrol tablosunu denetler.", "",
         "## SHA", "", "| Ad | sha256 |", "|---|---|"]
    for k, v in sh.items():
        L.append(f"| {k} | `{v}` |")
    L += ["", f"OS_ESIK_SHA: `{sh['OS_ESIK_SHA']}`", f"OS_KOD_SHA: `{sh['OS_KOD_SHA']}`", "",
          f"KASA açık kesik: {OS_ESIK['veri']['kesik_tarih']} (KASA_DURUM.json; veri yalnız /tmp/kasa/acik). Pazarlar: ABD, AVR (BIST kapsam dışı).", "",
          "## Kova sınırları (giriş 2016-22 havuz hisse-günleri, getirisiz; sayı)", "",
          "| Pazar | KV1 ATRP tercil | KV1 F15 çeyrek | KV2 ATRP ondalık | n KV1 / KV2 |", "|---|---|---|---|---|"]
    for p, s in S["sinir"].items():
        L.append(f"| {p} | {', '.join(f'{x:.6f}' for x in s['KV1_ATRP'])} | {', '.join(f'{x:.6f}' for x in s['KV1_F15'])} | "
                 f"{', '.join(f'{x:.6f}' for x in s['KV2_ATRP'])} | {s['n_KV1']} / {s['n_KV2']} |")
    L += ["", "## Evren prefix testi (hazırlık; getirisiz; koşuda yeniden yapılmaz, os_prefix.json sha'sı yukarıda)", "",
          "| Pazar | sonuç | gün (<= 2022-05-31) | havuz hisse-gün | hisse kısa / uzun | toplam fark | ok / H / KV1 / KV2 farkı | olay kümesi farkı |", "|---|---|---|---|---|---|---|---|"]
    for p, r in Pr["prefix"].items():
        f = r["fark"]
        L.append(f"| {p} | {'TUTTU' if r['tutar'] else 'TUTMADI'} | {r['n_gun']} | {r['havuz_kisa']} | {r['n_hisse_kisa']} / {r['n_hisse_uzun']} | "
                 f"{r['toplam_fark']} | {f.get('ok')} / {f.get('H')} / {f.get('KV1')} / {f.get('KV2')} | {sum(v['fark'] for v in r['olay'].values())} |")
    L += ["", "## Bölüm 2-5 (iş tanımından AYNEN)", "", _os_is_tanimi_bolum(), "",
          "## İşlemsel tanımlar (sonuç görülmeden; OS_ESIK tam metni aşağıda)", "",
          "- O3 iki aday olarak ölçülür: O3a = T5_H, O3b = T10_H (iş tanımı 'T10_H (ve T5_H)').",
          "- Kart sırası: aynı ay sonu t kesitinde, giriş günü havuzda olan ve değeri sonlu hisseler; üst onda > 0,90, alt onda <= 0,10 (pct rank first, sembol sırası).",
          "- Eş dışlama ('olay kümesi dışı'): aynı bacağın tekilleştirme ÖNCESİ bütün ondalık üyeleri ve olayın kendisi.",
          "- Tekil: bacak x H başına >= H birleşik takvim günü (CETVEL2 v2.2 tekil = H).",
          "- Plasebo olayları: ay sonu giriş günü havuzundan %10 rastgele; GEÇER = |ort fark| < 0,03 SD VE TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7.",
          "- Yapay iz: ay sonu giriş günleri havuzundan n hisse-gün (R_H, KV1, KV2 var); yol sürüklemesi; yakalama = TUTAR(+); n* tanımı OS_ESIK['secim']['ii'].",
          "- Seçim şartı (iii) 'hiçbir hücre' = ABD ve AVR dört hücre; (iv) aynı bacak ABD d1 VE d2.",
          "- Ek beraberlik bozucu (4) iş tanımında yok, sonuç görülmeden eklendi: O1 < O3a < O3b < O2 < O5 < O4, KV2 < KV1.",
          "- Klasik portföy tanısı her durumda hesaplanır (seçimde kullanılmaz; 'hiçbiri geçmezse' tanısı olarak raporlanır).",
          "", "## OS_ESIK (mühürlü; sha yukarıda)", "", "```json", json.dumps(OS_ESIK, ensure_ascii=False, indent=1, default=str), "```", "",
          "## KONTROL LİSTESİ", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    try:
        import IZ_KARNE as _IK
        adlar = {k["kod"]: k.get("ad", k.get("madde", k["kod"])) for k in _IK.IK_KONTROL}
    except Exception as ex:   # ad yoksa yalnız kod basılır; kapı yine IZ_KARNE ile denetlenir
        oslog.warning("IZ_KARNE adları okunamadı: %s", ex); adlar = {}
    for k, (y, kn) in OS_KONTROL.items():
        L.append(f"| {k} | {adlar.get(k, k)} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(L) + "\n"


def os_onkayit_yaz(veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _os_yol("onkayit")
    if os.path.exists(yol) and not uzerine:
        raise OSHata(f"ön kayıt zaten var: {yol} (--uzerine-yaz)")
    return _os_yaz(yol, os_onkayit_metni(veri), "ön kayıt")


def os_kapi(onkayit: Optional[str] = None, git: bool = True, kontrol: bool = True, veri: Optional[str] = None) -> Dict[str, Any]:
    """Koşu kapısı: KASA + ön kayıt git'te işlenmiş / değişmemiş + OS_ESIK / kod / sınır / prefix sha eşit + ik_kontrol_kapisi."""
    yol = onkayit or _os_yol("onkayit")
    if not os.path.exists(yol):
        raise OSHata(f"ön kayıt yok: {yol}")
    kasa = os_kasa_kapi(veri)
    metin = open(yol, encoding="utf-8").read()
    sh = os_sha_simdi(veri); bozuk = []
    for k in ("OS_ESIK_SHA", "OS_KOD_SHA", "SINIR_JSON_SHA", "PREFIX_JSON_SHA", "V_ABD_SHA", "V_AVR_SHA"):
        m = re.search(rf"\|\s*{k}\s*\|\s*`([0-9a-f]{{64}})`", metin)
        if not m or m.group(1) != sh.get(k):
            bozuk.append(k)
    if bozuk:
        raise OSHata(f"ön kayıt sha tutmuyor: {bozuk} -> DURDU")
    g = _os_git_islenmis(yol) if git else {"commit": "-", "commit_zamani": "-"}
    kk = None
    if kontrol:
        import IZ_KARNE as _IK
        kk = _IK.ik_kontrol_kapisi(yol)
    return {"onkayit": yol, "git": g, "kasa": kasa, "sha": sh, "kontrol": bool(kk["gecti"]) if kk else None}


# ================================================================ 10) GÖREV (pazar x H): kartlar, plasebo, yapay iz
_OS_IS: Dict[str, Any] = {}


def _os_kart_gorev(Pn: Dict[str, Any], X: pd.DataFrame, H: int, Ms: Dict[str, np.ndarray]) -> Tuple[List[Dict[str, Any]], pd.DataFrame]:
    """Bütün bacaklar: olay satırları (ölçü + eş) ve hücre istatistikleri."""
    p = Pn["pazar"]; hucre, satir = [], []
    bac: Dict[str, Tuple[pd.DataFrame, pd.DataFrame]] = {b: os_bacak_olay(X, b, H) for b in OS_BACAK}
    for b, (U, T) in bac.items():
        d = T.d.to_numpy(np.int64); j = T.j.to_numpy(np.int64)
        R = pd.DataFrame({"pazar": p, "H": H, "bacak": b, "sembol": T.sembol.to_numpy(), "tarih": T.tarih.dt.strftime("%Y-%m-%d").to_numpy(),
                          "giris": Pn["tarih"][d].strftime("%Y-%m-%d"), "d": d, "j": j, "donem": _os_donem(Pn["tarih"][d]),
                          "deger": T[OS_BACAK[b][0]].to_numpy(float), "E0": Pn["Op"][d, j], "atrp": Pn["ATRP"][d, j]})
        for k in OS_KAYNAK:
            R[k] = Ms[k][d, j]
        satir.append((b, R, U))
    for kv in OS_KOVA:
        KV = Pn[kv]
        for k in OS_KAYNAK:
            hv = os_havuz(Ms[k], KV)
            for b, R, U in satir:
                ed, ej = U.d.to_numpy(np.int64), U.j.to_numpy(np.int64)
                e = os_es(hv, R.d.to_numpy(np.int64), R.j.to_numpy(np.int64), R[k].to_numpy(float), ed, ej)
                R[f"{kv}_kova"] = KV[R.d.to_numpy(np.int64), R.j.to_numpy(np.int64)]
                R[f"{kv}_es_{k}"] = e["es"]; R[f"{kv}_n_{k}"] = e["n_es"]
                if k == "R":
                    R[f"{kv}_sira"] = e["sira"]
            del hv
    for b, R, U in satir:
        yon = OS_BACAK[b][2]; ay = _os_ay(Pn, R.d.to_numpy(np.int64))
        for kv in OS_KOVA:
            for o in OS_OLCU:
                k = OS_OLCU_KAYNAK[o]
                f = (R[f"{kv}_sira"] - 0.5).to_numpy(float) if o == "O2" else (R[k] - R[f"{kv}_es_{k}"]).to_numpy(float)
                for dn in OS_ESIK["donem"]:
                    if dn == "tarih":
                        continue
                    m = (R.donem.to_numpy() == dn)
                    c = os_hucre(f[m], ay[m], yon, tohum_ek=_os_tohum("kart", p, H, b, kv, o, dn), perm=True)
                    hucre.append({"pazar": p, "H": H, "bacak": b, "yon": yon, "kova": kv, "olcu": o, "donem": dn, **c,
                                  "tutar": c["tutar_p"] if yon == "+" else c["tutar_n"], "ters": c["tutar_n"] if yon == "+" else c["tutar_p"]})
    return hucre, pd.concat([R for _, R, _ in satir], ignore_index=True)


def _os_cekim_gun(Pn: Dict[str, Any]) -> np.ndarray:
    _, dt = os_ay_sonu(Pn)
    return np.unique(dt[(dt > 0) & (dt < len(Pn["tarih"]))])


def _os_plasebo_gorev(Pn: Dict[str, Any], H: int, Ms: Dict[str, np.ndarray], T: Optional[int] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Rastgele etiket: ay sonu giriş günü havuzundan %10; 200 tohum; ölçü x kova x hücre."""
    Pl = OS_ESIK["plasebo"]; T = int(T or Pl["tohum_sayi"]); p = Pn["pazar"]
    gun = _os_cekim_gun(Pn); pool = Pn["ok"] & (Pn["H"] >= 0)
    cek = []
    for t in range(T):
        rng = np.random.default_rng([int(Pl["tohum"]), _os_tohum(p, H), t]); dd, jj = [], []
        for g in gun:
            js = np.flatnonzero(pool[g])
            k = int(round(Pl["pay"] * len(js)))
            if k <= 0:
                continue
            sec = rng.choice(js, size=k, replace=False); dd.append(np.full(k, g)); jj.append(sec)
        cek.append((np.concatenate(dd).astype(np.int64), np.concatenate(jj).astype(np.int64)))
    sat, sdt = [], []
    for kv in OS_KOVA:
        for k in OS_KAYNAK:
            hv = os_havuz(Ms[k], Pn[kv])
            for o in [o for o in OS_OLCU if OS_OLCU_KAYNAK[o] == k]:
                acc = {dn: [0.0, 0.0, 0] for dn in ("d1", "d2")}
                for t, (dd, jj) in enumerate(cek):
                    x = Ms[k][dd, jj]; e = os_es(hv, dd, jj, x, dd, jj); f = os_fark(o, x, e)
                    dn_ = _os_donem(Pn["tarih"][dd]); ay = _os_ay(Pn, dd)
                    for dn in ("d1", "d2"):
                        m = dn_ == dn
                        c = os_hucre(f[m], ay[m], "+", tohum_ek=_os_tohum("plasebo", p, H, kv, o, dn, t))
                        ff = f[m][np.isfinite(f[m])]
                        acc[dn][0] += float(ff.sum()); acc[dn][1] += float((ff ** 2).sum()); acc[dn][2] += int(len(ff))
                        sat.append({"pazar": p, "H": H, "kova": kv, "olcu": o, "donem": dn, "tohum": t, "n": c["n"], "fark": c["fark"],
                                    "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"], "tutar_p": c["tutar_p"], "tutar_n": c["tutar_n"]})
                for dn, (s1, s2, nn) in acc.items():
                    sd = math.sqrt(max(s2 / nn - (s1 / nn) ** 2, 0.0) * nn / max(nn - 1, 1)) if nn > 1 else float("nan")
                    sdt.append({"pazar": p, "H": H, "kova": kv, "olcu": o, "donem": dn, "sd": sd, "n_toplam": nn})
            del hv
    return sat, sdt


def _os_yapay_gorev(Pn: Dict[str, Any], H: int, Ms: Dict[str, np.ndarray]) -> List[Dict[str, Any]]:
    """Yapay iz: hücre başına n hisse-gün (yerine koymadan), yol sürüklemesi, yakalama = TUTAR(+)."""
    Y = OS_ESIK["yapay"]; p = Pn["pazar"]; gun = _os_cekim_gun(Pn); dep = Pn["dep"]
    pool = Pn["ok"] & (Pn["H"] >= 0) & np.isfinite(Ms["R"]) & (Pn["KV1"] >= 0) & (Pn["KV2"] >= 0)
    gm = np.zeros(len(Pn["tarih"]), bool); gm[gun] = True
    dd0, jj0 = np.nonzero(pool & gm[:, None])
    dn0 = _os_donem(Pn["tarih"][dd0])
    hv = {(kv, k): os_havuz(Ms[k], Pn[kv]) for kv in OS_KOVA for k in OS_KAYNAK}
    sat = []
    for dn in ("d1", "d2"):
        ci = np.flatnonzero(dn0 == dn); Nh = len(ci)
        for n in Y["n"]:
            if n > Y["n_azami_pay"] * Nh:
                for dl in Y["delta"]:
                    for kv in OS_KOVA:
                        for o in OS_OLCU:
                            sat.append({"pazar": p, "H": H, "donem": dn, "n_hedef": n, "delta": dl, "kova": kv, "olcu": o, "tohum": -1,
                                        "olculmedi": True, "havuz": Nh})
                continue
            for t in range(int(Y["tohum_sayi"])):
                rng = np.random.default_rng([int(Y["tohum"]), _os_tohum(p, H, dn, n), t])
                sec = ci[rng.choice(Nh, size=n, replace=False)]; dd, jj = dd0[sec], jj0[sec]
                ee = Pn["EIX"][dd, jj]; ay = _os_ay(Pn, dd)
                for dl in Y["delta"]:
                    xo = os_olcu_hesap(dep, jj, ee, H, dl)
                    for kv in OS_KOVA:
                        for o in OS_OLCU:
                            k = OS_OLCU_KAYNAK[o]; x = xo[k]
                            e = os_es(hv[(kv, k)], dd, jj, x, dd, jj); f = os_fark(o, x, e)
                            c = os_hucre(f, ay, "+", tohum_ek=_os_tohum("yapay", p, H, dn, n, dl, kv, o, t))
                            sat.append({"pazar": p, "H": H, "donem": dn, "n_hedef": n, "delta": dl, "kova": kv, "olcu": o, "tohum": t,
                                        "olculmedi": False, "havuz": Nh, "n": c["n"], "fark": c["fark"], "yakala": c["tutar_p"],
                                        "ters": c["tutar_n"]})
    del hv
    return sat


def _os_gorev(is_: Tuple[str, int]) -> Dict[str, Any]:
    p, H = is_; t0 = time.time()
    Pn = _OS_IS["P"][p]; X = _OS_IS["X"][p]
    try:
        Ms = os_olcu_matris(Pn, H)
        hucre, satir = _os_kart_gorev(Pn, X, H, Ms)
        oslog.info("%s H%d kartlar tamam (%.0f sn)", p, H, time.time() - t0)
        pl, sd = _os_plasebo_gorev(Pn, H, Ms, _OS_IS.get("plasebo_T"))
        oslog.info("%s H%d plasebo tamam (%.0f sn)", p, H, time.time() - t0)
        ya = _os_yapay_gorev(Pn, H, Ms)
        oslog.info("%s H%d yapay iz tamam (%.0f sn)", p, H, time.time() - t0)
    except Exception as ex:
        oslog.exception("%s H%d görev hatası", p, H)
        raise OSHata(f"{p} H{H} görev hatası: {type(ex).__name__}: {ex}") from ex
    return {"pazar": p, "H": H, "hucre": hucre, "satir": satir, "plasebo": pl, "plasebo_sd": sd, "yapay": ya, "sure": time.time() - t0}


# ================================================================ 11) KLASİK PORTFÖY (eşsiz ham kesit)
def os_klasik(Pn: Dict[str, Any], X: pd.DataFrame) -> List[Dict[str, Any]]:
    dep = Pn["dep"]; p = Pn["pazar"]; out = []
    Xh = X[X.havuz].reset_index(drop=True)
    e1 = Pn["EIX"][Xh.d.to_numpy(np.int64), Xh.j.to_numpy(np.int64)]
    for H in OS_ESIK["klasik"]["H"]:
        r = os_olcu_hesap(dep, Xh.j.to_numpy(np.int64), e1, H)["R"]
        Z = Xh.assign(r=r, ay=Xh.tarih.dt.to_period("M"), donem=_os_donem(Pn["tarih"][Xh.d.to_numpy(np.int64)]))
        for kart, (a, b) in {"MOM": ("ust", "alt"), "STREV": ("alt", "ust"), "HIGH52": ("ust", "alt")}.items():
            ga = Z[Z[f"{kart}_{a}"]].groupby("ay").r.mean(); gb = Z[Z[f"{kart}_{b}"]].groupby("ay").r.mean()
            sp = (ga - gb).dropna()
            dmap = Z.groupby("ay").donem.first()
            for dn in ("d1", "d2"):
                s = sp[dmap.reindex(sp.index).to_numpy() == dn].to_numpy(float)
                L = int(math.ceil(H / 21)); nw = _os_nw_t(s, L)
                out.append({"pazar": p, "H": H, "kart": kart, "bacak": f"{a}-{b}", "donem": dn, "ay": int(len(s)),
                            "ort": float(s.mean()) if len(s) else np.nan, "nw_t": nw, "pozitif_ay": float((s > 0).mean()) if len(s) else np.nan})
    return out


def _os_nw_t(s: np.ndarray, L: int) -> float:
    s = np.asarray(s, float); n = len(s)
    if n < 3:
        return float("nan")
    e = s - s.mean(); v = (e @ e) / n
    for l in range(1, min(L, n - 1) + 1):
        w = 1 - l / (L + 1); v += 2 * w * (e[l:] @ e[:-l]) / n
    return float(s.mean() / math.sqrt(v / n)) if v > 0 else float("nan")


# ================================================================ 12) SEÇİM
def os_secim(hucre: pd.DataFrame, plo: pd.DataFrame, yo: pd.DataFrame) -> Dict[str, Any]:
    """Önceden yazılı seçim kuralı (OS_ESIK['secim']) -> üçlü başına şartlar ve sıralama."""
    sat = []
    sira_olcu = {o: i for i, o in enumerate(["O1", "O3a", "O3b", "O2", "O5", "O4"])}; sira_kova = {"KV2": 0, "KV1": 1}
    for H in OS_ESIK["ufuk"]:
        for kv in OS_KOVA:
            for o in OS_OLCU:
                # (i) plasebo
                pp = plo[(plo.H == H) & (plo.kova == kv) & (plo.olcu == o)]
                i_ok = len(pp) == 4 and bool(pp.gecti.all())
                i_neden = "; ".join(f"{r.pazar} {r.donem}: |fark| {abs(r.fark_ort):.4f} vs 0,03 SD {0.03 * r.sd:.4f}, + {r.pay_p:.0%}, - {r.pay_n:.0%}"
                                    for r in pp.itertuples() if not r.gecti)
                # (ii) yapay iz
                yy = yo[(yo.H == H) & (yo.kova == kv) & (yo.olcu == o) & (yo.delta == OS_ESIK["yapay"]["karar_delta"])]
                nmin = []; ii_ok = True
                for p in OS_ESIK["veri"]["pazar"]:
                    for dn in ("d1", "d2"):
                        g = yy[(yy.pazar == p) & (yy.donem == dn) & (yy.yakala_pay >= OS_ESIK["yapay"]["karar_pay"])]
                        if not len(g):
                            ii_ok = False; nmin.append(None)
                        else:
                            nmin.append(int(g.n_hedef.min()))
                nstar = max(nmin) if ii_ok else None
                # (iii), (iv)
                hh = hucre[(hucre.H == H) & (hucre.kova == kv) & (hucre.olcu == o)]
                ters = hh[hh.bacak.isin(["MOM-", "STREV-"]) & hh.tutar_p.astype(bool)]
                iii_ok = len(ters) == 0
                gor = []
                for b in OS_BACAK:
                    a = hh[(hh.bacak == b) & (hh.pazar == "ABD")]
                    if len(a) == 2 and bool(a.tutar.astype(bool).all()):
                        gor.append(b)
                iv_ok = any(b in gor for b in ("MOM+", "STREV+", "HIGH52+"))
                sat.append({"H": H, "kova": kv, "olcu": o, "i_plasebo": i_ok, "i_neden": i_neden, "ii_yapay": ii_ok, "n_star": nstar,
                            "ii_nmin": nmin, "iii_oynaklik": iii_ok, "iii_neden": "; ".join(f"{r.bacak} {r.pazar} {r.donem}" for r in ters.itertuples()),
                            "iv_bilinen": iv_ok, "goren_bacak": gor, "n_goren": len(gor),
                            "gecer": bool(i_ok and ii_ok and iii_ok and iv_ok),
                            "dusen": [s for s, v in (("i", i_ok), ("ii", ii_ok), ("iii", iii_ok), ("iv", iv_ok)) if not v],
                            "_s4": (sira_olcu[o], sira_kova[kv])})
    S = pd.DataFrame(sat)
    G = S[S.gecer].copy()
    if len(G):
        G["_k"] = list(zip(G.H, -G.n_goren, G.n_star.fillna(10 ** 9), G._s4))
        G = G.sort_values("_k", kind="mergesort")
    birinci = G.iloc[0][["H", "kova", "olcu"]].to_dict() if len(G) else None
    return {"tablo": S.drop(columns=["_s4"]).to_dict("records"), "gecen": G.drop(columns=["_s4", "_k"], errors="ignore").to_dict("records"),
            "birinci": birinci, "hicbiri": not len(G)}


# ================================================================ 13) YENİDEN ÜRETİM
def os_yeniden(J: Dict[str, Any], veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Üç hücre satır dosyasından düz pandas; 30 olayın ölçüleri ham pkl'den düz döngüyle (bağımsız kod yolu)."""
    c = cikti or OS_YOL["cikti"]; v = veri or OS_YOL["veri"]; Yr = OS_ESIK["yeniden"]; out = {"hucre": [], "olay": [], "tutar": True}
    hc = pd.DataFrame(J["kart_hucre"])
    for b, p, dn, o, kv, H in Yr["hucre"]:
        R = pd.read_csv(_os_yol("kart", c, p=p, h=H))
        R = R[(R.bacak == b) & (R.donem == dn)]
        k = OS_OLCU_KAYNAK[o]
        f = (R[f"{kv}_sira"] - 0.5) if o == "O2" else (R[k] - R[f"{kv}_es_{k}"])
        f = f.dropna()
        ref = hc[(hc.bacak == b) & (hc.pazar == p) & (hc.donem == dn) & (hc.olcu == o) & (hc.kova == kv) & (hc.H == H)].iloc[0]
        ok = int(len(f)) == int(ref.n) and abs(float(f.mean()) - float(ref.fark)) < 1e-9
        out["hucre"].append({"hucre": f"{b} {p} {dn} {o} {kv} H{H}", "n": int(len(f)), "fark": float(f.mean()), "json_n": int(ref.n),
                             "json_fark": float(ref.fark), "tutar": bool(ok)})
        out["tutar"] &= bool(ok)
    rng = np.random.default_rng(int(Yr["tohum"])); ham: Dict[str, Any] = {}
    secim = []
    for p in OS_ESIK["veri"]["pazar"]:
        for H in OS_ESIK["ufuk"]:
            R = pd.read_csv(_os_yol("kart", c, p=p, h=H))
            R = R[np.isfinite(R[OS_KAYNAK]).all(axis=1)]
            secim.append(R.iloc[rng.choice(len(R), size=5, replace=False)])
    S = pd.concat(secim, ignore_index=True)
    hd = OS_ESIK["hedef"]
    for r in S.itertuples():
        if r.pazar not in ham:
            x = pd.read_pickle(os.path.join(v, f"V_{r.pazar}.pkl")); ham[r.pazar] = x["veri"] if isinstance(x, dict) and "veri" in x else x
        d = ham[r.pazar][r.sembol].copy()
        d.index = pd.DatetimeIndex(d.index).normalize()
        d = d[~d.index.duplicated(keep="last")].sort_index()
        d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)]
        rows = list(d.itertuples())
        gi = [i for i, z in enumerate(rows) if z.Index == pd.Timestamp(r.giris)][0]
        # ATRP(t): t = gi - 1; ATR14 TR önceki kapanışla
        trs = []
        for i in range(gi - 14, gi):
            z = rows[i]; pc = rows[i - 1].Close if i - 1 >= 0 else None
            trs.append((max(z.High, pc) - min(z.Low, pc)) if pc is not None else (z.High - z.Low))
        atrp = (sum(trs) / 14.0) / rows[gi - 1].Close
        z0 = rows[gi]; E0 = min(max(z0.Open, z0.Low), z0.High)
        H = int(r.H); mx, mn = -1e300, 1e300; up, dn = E0 * (1 + hd["o5_kat"] * atrp), E0 * (1 - hd["o5_kat"] * atrp); o5 = None
        for k in range(H):
            z = rows[gi + k]; mx = max(mx, z.High); mn = min(mn, z.Low)
            if o5 is None:
                if z.Low <= dn:
                    o5 = 0.0
                elif z.High >= up:
                    o5 = 1.0
        o5 = 0.0 if o5 is None else o5
        rr = rows[gi + H - 1].Close / E0 - 1
        el = {"R": rr, "T5": float(mx >= E0 * (1 + hd["T5"])), "T10": float(mx >= E0 * (1 + hd["T10"])),
              "A": ((mx - E0) - (E0 - mn)) / (E0 * atrp), "O5": o5}
        ok = all(abs(el[k] - getattr(r, k)) < 1e-9 for k in OS_KAYNAK)
        out["olay"].append({"pazar": r.pazar, "H": H, "sembol": r.sembol, "giris": r.giris, **{k: el[k] for k in OS_KAYNAK},
                            **{f"satir_{k}": getattr(r, k) for k in OS_KAYNAK}, "tutar": bool(ok)})
        out["tutar"] &= bool(ok)
    out["olay_tutan"] = int(sum(o["tutar"] for o in out["olay"])); out["olay_n"] = len(out["olay"])
    return out


# ================================================================ 14) KOŞU
def os_kos(veri: Optional[str] = None, cikti: Optional[str] = None, islem: int = 4, git: bool = True, kontrol: bool = True,
           plasebo_T: Optional[int] = None) -> Dict[str, Any]:
    c = cikti or OS_YOL["cikti"]; t0 = time.time(); bas = _os_simdi()
    K = os_kapi(git=git, kontrol=kontrol, veri=veri)
    oslog.info("kapılar AÇIK (ön kayıt %s)", K["git"]["commit"][:12])
    S = json.load(open(_os_yol("sinir", c), encoding="utf-8"))["sinir"]
    _OS_IS["P"], _OS_IS["X"] = {}, {}
    _OS_IS["plasebo_T"] = plasebo_T
    klasik = []
    for p in OS_ESIK["veri"]["pazar"]:
        P = os_panel(os_veri(p, veri), S[p])
        if P["sinir"] != S[p]:
            raise OSHata(f"{p}: sınır uyuşmuyor")
        X = os_kart_sinyal(P)
        _OS_IS["P"][p], _OS_IS["X"][p] = P, X
        klasik += os_klasik(P, X)
    isler = [(p, H) for H in sorted(OS_ESIK["ufuk"], reverse=True) for p in OS_ESIK["veri"]["pazar"]]
    if islem > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as pool:
            sonuc = pool.map(_os_gorev, isler, chunksize=1)
    else:
        sonuc = [_os_gorev(x) for x in isler]
    hucre = pd.DataFrame([h for s in sonuc for h in s["hucre"]])
    pl = pd.DataFrame([h for s in sonuc for h in s["plasebo"]]); sd = pd.DataFrame([h for s in sonuc for h in s["plasebo_sd"]])
    ya = pd.DataFrame([h for s in sonuc for h in s["yapay"]])
    # plasebo özeti
    g = pl.groupby(["pazar", "H", "kova", "olcu", "donem"])
    plo = g.agg(fark_ort=("fark", "mean"), pay_p=("tutar_p", "mean"), pay_n=("tutar_n", "mean"), n_ort=("n", "mean"), tohum=("tohum", "nunique")).reset_index()
    plo = plo.merge(sd, on=["pazar", "H", "kova", "olcu", "donem"], how="left")
    Pl = OS_ESIK["plasebo"]
    plo["gecti"] = (plo.fark_ort.abs() < Pl["fark_sd_oran"] * plo.sd) & (plo.pay_p <= Pl["tutar_pay"]) & (plo.pay_n <= Pl["tutar_pay"])
    yo = ya[~ya.olculmedi.astype(bool)].groupby(["pazar", "H", "donem", "n_hedef", "delta", "kova", "olcu"]).agg(
        yakala_pay=("yakala", "mean"), ters_pay=("ters", "mean"), n_ort=("n", "mean"), fark_ort=("fark", "mean"), havuz=("havuz", "first")).reset_index()
    sec = os_secim(hucre, plo, yo)
    # satır dosyaları
    os.makedirs(c, exist_ok=True)
    for s in sonuc:
        s["satir"].to_csv(_os_yol("kart", c, p=s["pazar"], h=s["H"]), index=False, compression={"method": "gzip", "mtime": 0})
    pl.to_csv(_os_yol("plasebo", c), index=False, compression={"method": "gzip", "mtime": 0})
    ya.to_csv(_os_yol("yapay", c), index=False, compression={"method": "gzip", "mtime": 0})
    pd.DataFrame(klasik).to_csv(_os_yol("klasik", c), index=False)
    hucre.to_csv(_os_yol("kart_hucre", c), index=False)
    J = {"surum": OS_SURUM, "esik_sha": os_esik_sha(), "kapi": K, "bas": bas, "son": _os_simdi(), "sure_sn": time.time() - t0,
         "kart_hucre": hucre.to_dict("records"), "plasebo": plo.to_dict("records"), "yapay": yo.to_dict("records"), "secim": sec,
         "klasik": klasik, "prefix": json.load(open(_os_yol("prefix", c), encoding="utf-8"))["prefix"], "sinir": S,
         "gorev_sure": {f"{s['pazar']}_H{s['H']}": s["sure"] for s in sonuc},
         "huni": {p: {"panel_gun": len(_OS_IS["P"][p]["tarih"]), "hisse": len(_OS_IS["P"][p]["sembol"]),
                      "havuz_hisse_gun": int((_OS_IS["P"][p]["ok"] & (_OS_IS["P"][p]["H"] >= 0)).sum()),
                      "ay_sonu_aday": int(len(_OS_IS["X"][p])), "ay_sonu_havuz": int(_OS_IS["X"][p].havuz.sum()),
                      "not": _OS_IS["P"][p]["not"]} for p in _OS_IS["P"]}}
    J["yeniden"] = os_yeniden(J, veri, c)
    import KASA as _KS
    eg = {}
    for p in OS_ESIK["veri"]["pazar"]:
        for H in OS_ESIK["ufuk"]:
            y = _os_yol("kart", c, p=p, h=H)
            R = pd.read_csv(y, usecols=["giris", "tarih", "R"])
            eg[os.path.basename(y)] = {"en_gec_tarih": str(_KS.ks_en_gec_tarih(y).date()), "son_sinyal": str(R.tarih.max()),
                                       "son_olculen_giris": str(R.giris[np.isfinite(R.R)].max())}
    J["en_gec"] = eg
    J["son"] = _os_simdi(); J["sure_sn"] = time.time() - t0
    _os_yaz(_os_yol("json", c), json.dumps(_os_temizle(J), ensure_ascii=False, indent=1, default=_os_json), "sonuç json")
    _os_yaz(_os_yol("rapor", c), os_rapor(J), "rapor")
    if not J["yeniden"]["tutar"]:
        raise OSHata("YENİDEN ÜRETİM TUTMADI (json ve rapor yazıldı; sonuç geçersiz)")
    return J


# ================================================================ 15) RAPOR
def _y(x: Any, n: int = 2, yuzde: bool = True) -> str:
    try:
        x = float(x)
    except (TypeError, ValueError):
        return "-"
    if not math.isfinite(x):
        return "-"
    return (f"{100 * x:+.{n}f}" if yuzde else f"{x:+.{n}f}").replace(".", ",")


def os_rapor(J: Optional[Dict[str, Any]] = None, cikti: Optional[str] = None) -> str:
    c = cikti or OS_YOL["cikti"]
    if J is None:
        J = json.load(open(_os_yol("json", c), encoding="utf-8"))
    H_ = pd.DataFrame(J["kart_hucre"]); S = J["secim"]; St = pd.DataFrame(S["tablo"])
    L = [f"# ÖLÇÜ SINAMASI — RAPOR ({J['son']})", "",
         f"{OS_SURUM}. Ön kayıt {J['kapi']['onkayit'].split('/')[-1]} (git {J['kapi']['git']['commit']} {J['kapi']['git']['commit_zamani']}); koşu {J['bas']} .. "
         f"{J['son']} ({J['sure_sn']:.0f} sn). Veri yalnız KASA açık kısmı (kesik {OS_ESIK['veri']['kesik_tarih']}). Evren bugün işlem gören hisseler "
         "(hayatta kalma: getiriler yukarı, STREV alt onda yukarı yanlı görünür). Komisyon yok. Fark birimi: O1 / O3 / O5 yüzde puan, O2 sıra "
         "puanı (x100), O4 ATRP birimi (x100 gösterilmez, ham).", "",
         "## 1. TEK SAYFA ÖZET", ""]
    if S["hicbiri"]:
        L.append("**Hiçbir (ölçü, kova, H) üçlüsü dört şartı birlikte geçmedi: bu evren ve eş kurulumunda 15-60 mum ölçüsü bilinen etkiyi göremiyor.**")
    else:
        b = S["birinci"]
        L.append(f"**GEÇEN üçlü sayısı: {len(S['gecen'])}. Seçim kuralına göre BİRİNCİ: {b['olcu']} / {b['kova']} / H {b['H']}.**")
        L += ["", "| sıra | ölçü | kova | H | gören bacaklar (ABD d1 + d2) | n* |", "|---|---|---|---|---|---|"]
        for i, g in enumerate(S["gecen"], 1):
            L.append(f"| {i} | {g['olcu']} | {g['kova']} | {g['H']} | {', '.join(g['goren_bacak'])} | {g['n_star']} |")
    L += ["", "Şart başına geçen üçlü sayısı (36 üçlü): " + ", ".join(f"({k}) {int(St[c_].sum())}" for k, c_ in
                                                              (("i", "i_plasebo"), ("ii", "ii_yapay"), ("iii", "iii_oynaklik"), ("iv", "iv_bilinen"))), "",
          "| H | kova | ölçü | (i) plasebo | (ii) yapay +%2 (n* / hücre n_min) | (iii) oynaklık ödülü yok | (iv) bilinen etki (ABD d1+d2 gören) | GEÇER | düşen |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in St.itertuples():
        L.append(f"| {r.H} | {r.kova} | {r.olcu} | {'E' if r.i_plasebo else 'H'} | {'E' if r.ii_yapay else 'H'} ({r.n_star if r.n_star else '-'} / "
                 f"{'/'.join(str(x) if x else '-' for x in r.ii_nmin)}) | {'E' if r.iii_oynaklik else 'H: ' + r.iii_neden} | "
                 f"{'E' if r.iv_bilinen else 'H'} ({', '.join(r.goren_bacak) or '-'}) | {'**GEÇER**' if r.gecer else '-'} | {','.join(r.dusen) or '-'} |")
    # 2. kart tablosu
    L += ["", "## 2. KONTROL KARTI TABLOSU (fark [boot %95], p, TUTAR; ABD iki dönem karar, AVR bilgi)", "",
          "Hücre biçimi: fark [alt; üst] p · T = beklenen yönde TUTAR, X = ters yönde TUTAR. n = ölçülen olay.", ""]
    for H in OS_ESIK["ufuk"]:
        for kv in OS_KOVA:
            L += [f"### H {H} · {kv}", "", "| bacak | ölçü | ABD d1 | ABD d2 | AVR d1 | AVR d2 |", "|---|---|---|---|---|---|"]
            for b in OS_BACAK:
                for o in OS_OLCU:
                    hs = []
                    for p in OS_ESIK["veri"]["pazar"]:
                        for dn in ("d1", "d2"):
                            g = H_[(H_.H == H) & (H_.kova == kv) & (H_.bacak == b) & (H_.olcu == o) & (H_.pazar == p) & (H_.donem == dn)]
                            if not len(g):
                                hs.append("-"); continue
                            r = g.iloc[0]; yz = o != "O4"
                            tag = " **T**" if r.tutar else (" X" if r.ters else "")
                            hs.append(f"{_y(r.fark, 2, yz)} [{_y(r.boot_alt, 2, yz)}; {_y(r.boot_ust, 2, yz)}] p {r.p:.3f} n {int(r.n)}{tag}")
                    L.append(f"| {b} | {o} | " + " | ".join(hs) + " |")
            L.append("")
    # 3. plasebo ve yapay iz
    Po = pd.DataFrame(J["plasebo"])
    L += ["## 3. PLASEBO (200 tohum) ve YAPAY İZ (20 tohum)", "", "### Plasebo: |ort fark| / (0,03 SD) · TUTAR(+) payı · TUTAR(-) payı · GEÇER", "",
          "| H | kova | ölçü | ABD d1 | ABD d2 | AVR d1 | AVR d2 |", "|---|---|---|---|---|---|---|"]
    for H in OS_ESIK["ufuk"]:
        for kv in OS_KOVA:
            for o in OS_OLCU:
                hs = []
                for p in OS_ESIK["veri"]["pazar"]:
                    for dn in ("d1", "d2"):
                        g = Po[(Po.H == H) & (Po.kova == kv) & (Po.olcu == o) & (Po.pazar == p) & (Po.donem == dn)]
                        if not len(g):
                            hs.append("-"); continue
                        r = g.iloc[0]
                        hs.append(f"{abs(r.fark_ort) / (0.03 * r.sd):.2f} · {r.pay_p:.1%} · {r.pay_n:.1%} · {'E' if r.gecti else '**H**'}".replace(".", ","))
                L.append(f"| {H} | {kv} | {o} | " + " | ".join(hs) + " |")
    Yo = pd.DataFrame(J["yapay"])
    L += ["", "### Yapay iz: yakalama payı (TUTAR(+)), n = 100 / 300 / 1000", ""]
    for dl in OS_ESIK["yapay"]["delta"]:
        L += [f"**delta {dl:+.0%}**", "", "| H | kova | ölçü | ABD d1 | ABD d2 | AVR d1 | AVR d2 |", "|---|---|---|---|---|---|---|"]
        for H in OS_ESIK["ufuk"]:
            for kv in OS_KOVA:
                for o in OS_OLCU:
                    hs = []
                    for p in OS_ESIK["veri"]["pazar"]:
                        for dn in ("d1", "d2"):
                            g = Yo[(Yo.H == H) & (Yo.kova == kv) & (Yo.olcu == o) & (Yo.pazar == p) & (Yo.donem == dn) & (Yo.delta == dl)]
                            hs.append(" / ".join(f"{int(round(100 * g[g.n_hedef == n].yakala_pay.iloc[0]))}" if len(g[g.n_hedef == n]) else "-"
                                                 for n in OS_ESIK["yapay"]["n"]))
                    L.append(f"| {H} | {kv} | {o} | " + " | ".join(hs) + " |")
        L.append("")
    # 4. prefix
    L += ["## 4. EVREN PREFIX TESTİ (2022-06-30 vs 2023-12-29; havuz / sinyal günü <= 2022-05-31)", "",
          "| Pazar | sonuç | gün | havuz hisse-gün | toplam fark | ok | H | KV1 | KV2 | sup | lik_alt | evren | ATRP | F15 | olay kümeleri (15 küme) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p, r in J["prefix"].items():
        f = r["fark"]
        L.append(f"| {p} | {'TUTTU' if r['tutar'] else 'TUTMADI'} | {r['n_gun']} | {r['havuz_kisa']} | {r['toplam_fark']} | {f['ok']} | {f['H']} | {f['KV1']} | "
                 f"{f['KV2']} | {f['sup']} | {f['lik_alt']} | {f['evren']} | {f['ATRP']} | {f['F15']} | "
                 f"{sum(v['fark'] for v in r['olay'].values())} fark / {sum(v['n_kisa'] for v in r['olay'].values())} olay |")
    # 5. klasik
    Kl = pd.DataFrame(J["klasik"])
    L += ["", "## 5. KLASİK PORTFÖY TANISI (eşsiz ham kesit; ay başına üst - alt onda eşit ağırlıklı R_H farkı; Newey-West t)", "",
          "| kart | bacak | H | ABD d1 | ABD d2 | AVR d1 | AVR d2 |", "|---|---|---|---|---|---|---|"]
    for kart in ("MOM", "STREV", "HIGH52"):
        for H in OS_ESIK["klasik"]["H"]:
            hs = []
            for p in OS_ESIK["veri"]["pazar"]:
                for dn in ("d1", "d2"):
                    g = Kl[(Kl.kart == kart) & (Kl.H == H) & (Kl.pazar == p) & (Kl.donem == dn)]
                    hs.append(f"{_y(g.ort.iloc[0])} (t {g.nw_t.iloc[0]:.2f}, {int(g.ay.iloc[0])} ay)".replace(".", ",") if len(g) else "-")
            L.append(f"| {kart} | {Kl[Kl.kart == kart].bacak.iloc[0]} | {H} | " + " | ".join(hs) + " |")
    # 6. yeniden üretim
    Yr = J["yeniden"]
    L += ["", f"## 6. YENİDEN ÜRETİM: {'TUTTU' if Yr['tutar'] else 'TUTMADI'}", "", "| hücre | n (satır) | fark (satır) | n (json) | fark (json) | tutar |",
          "|---|---|---|---|---|---|"]
    for h in Yr["hucre"]:
        L.append(f"| {h['hucre']} | {h['n']} | {h['fark']:.6f} | {h['json_n']} | {h['json_fark']:.6f} | {'E' if h['tutar'] else 'H'} |")
    L += ["", f"30 olayın ham pkl'den düz döngüyle ölçüleri (R, T5, T10, A, O5): {Yr['olay_tutan']} / {Yr['olay_n']} birebir (< 1e-9).", ""]
    for o in Yr["olay"][:6]:
        L.append(f"- {o['pazar']} H{o['H']} {o['sembol']} {o['giris']}: R {o['R']:.5f} / satır {o['satir_R']:.5f}; A {o['A']:.4f} / {o['satir_A']:.4f}; "
                 f"O5 {o['O5']:.0f} / {o['satir_O5']:.0f}")
    # 7. en geç tarih
    L += ["", "## 7. EN GEÇ TARİH", ""]
    for k, v in J["en_gec"].items():
        L.append(f"- {k}: dosyadaki en geç tarih {v['en_gec_tarih']}; son sinyal {v['son_sinyal']}; ölçülen son giriş {v['son_olculen_giris']}")
    L += [f"- KASA kapısı: {J['kapi']['kasa']}", "", "## HUNİ", ""]
    for p, h in J["huni"].items():
        L.append(f"- {p}: {h['hisse']} hisse, {h['panel_gun']} gün, havuz {h['havuz_hisse_gun']} hisse-gün, ay sonu aday {h['ay_sonu_aday']} "
                 f"(havuzda {h['ay_sonu_havuz']})")
    nmin = H_.groupby(["pazar", "H", "bacak", "donem"]).n.max().reset_index()
    L += ["", "Olay sayısı (ölçülen, en çok; bacak x pazar x dönem x H): " + "; ".join(f"{r.bacak} {r.pazar} {r.donem} H{r.H} {int(r.n)}"
                                                                                  for r in nmin[nmin.bacak == "MOM+"].itertuples()), ""]
    return "\n".join(L) + "\n"


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_os(_once=_CK_ONCE_OS, _dosya="OLCU_SINAMA.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_OS", "_CK_KAYIT", "_cakisma_kontrol_os", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "copy", "_dt", "zlib",
           "annotations", "Any", "Dict", "List", "Optional", "Tuple", "OC")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_os()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=OS_SURUM)
    ap.add_argument("komut", choices=["hazirlik", "onkayit", "kos", "rapor", "sha", "kapi"])
    ap.add_argument("--islem", type=int, default=4)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    try:
        if a.komut == "hazirlik":
            R_ = os_hazirlik(a.veri)
            print(json.dumps(_os_temizle({"sinir": R_["sinir"], "prefix": {p: {"tutar": r["tutar"], "toplam_fark": r["toplam_fark"]}
                                                                            for p, r in R_["prefix"].items()}}), ensure_ascii=False, indent=1))
        elif a.komut == "onkayit":
            print(os_onkayit_yaz(a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kapi":
            print(json.dumps(_os_temizle(os_kapi(veri=a.veri)), ensure_ascii=False, indent=1, default=_os_json))
        elif a.komut == "kos":
            J_ = os_kos(a.veri, islem=a.islem)
            print(json.dumps(_os_temizle({"birinci": J_["secim"]["birinci"], "gecen": len(J_["secim"]["gecen"]),
                                          "yeniden": J_["yeniden"]["tutar"]}), ensure_ascii=False, indent=1, default=_os_json))
        elif a.komut == "rapor":
            print(_os_yaz(_os_yol("rapor"), os_rapor(), "rapor"))
        else:
            print(json.dumps(os_sha_simdi(a.veri), indent=1))
    except OSHata as ex:
        oslog.error("%s", ex); sys.exit(1)
