"""CETVEL2 — düzeltilmiş 15 mum cetveli (21 Kasım 2026; iş tanımı arastirma_cikti/cetvel2/CETVEL2_IS_TANIMI.md bölüm 2-3).

NEDEN: Ç203 pozitif kontrol (POZITIF_KONTROL_RAPOR.md): eski 15 bar cetveli h5 (+%5 stop = dip x 0,98'den önce) oynaklığı ödüllendiriyor
(momentum alt ondası h5'te +5,3 puan), AVR sınama DS içi eş geometrisi plaseboda +2,2 puan, n <= 100 kör, dar stop büyük kazananları kesiyor.

CETVEL2 (sabit; ön kayıt CETVEL2_ON_KAYIT.md):
  Girdi: olay listesi (pazar, sembol, tarih = sinyal günü t, isteğe bağlı F_* bayrakları). Fiyat: DUSUS_SONRASI.ds_veri (= OC.oc_veri, k34
  yüklenmez, açılış H-L kırpması) + OC.oc_panel (geçerli bar, havuz, likidite, tekil).
  Giriş E0 = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla). KARAR ÖLÇÜSÜ R15 = 15. geçerli bar kapanışı / E0 - 1 (giriş barı 1.;
  stop YOK; 30 takvim satırında 15 geçerli bar yoksa ölçülmez; kriz kesiği 31.08.2026).
  EŞ (konum eşli, bütün evren): aynı giriş günü, aynı pazar, aynı KOVA = ATRP(14) tercili x likidite üçlüsü (OC H % 3) x F15 (120 gün konumu,
  t dahil) çeyreği; havuzda (OC), R15'i ölçülebilir; aynı denemenin (hipotez) o günkü olay hisseleri ve olayın kendisi eş kümesinden çıkar;
  en az 5 eş yoksa olay 'eşsiz'. ATRP tercil ve F15 çeyrek sınırları EĞİTİM (2016-22) havuz hisse-günlerinden pazar başına SAYI olarak
  (cetvel2_esik.json; ön kayıtta yazılı).
  FARK = R15 - ort R15(eş); SIRA = olayın eş dağılımındaki yüzdeliği (küçük + 0,5 eşit). Hücre (pazar x dönem): n, ort / medyan FARK, ort SIRA,
  ay kümeli boot %95 (YH.yh_d3_boot_l3o, B 2000), ay kümeli işaret permütasyon p (DS.ds_perm_p, R 10000), L3O, güç (cetvel2_guc.json eğrisi).
  HÜCRE TUTAR / PLASEBO KAPISI / ETİKET / BH: C2_ESIK.

Komut:  python CETVEL2.py onkayit [--islem 4]   kova sınırları + güç eğrisi + prefix -> cetvel2_esik.json, cetvel2_guc.json, CETVEL2_ON_KAYIT.md
        python CETVEL2.py kos [--islem 4]       kapı -> pozitif kontrol v2 (A yapay iz, B momentum / PEAD, C plasebo kapısı) -> CETVEL2_POZITIF_KONTROL.md
        python CETVEL2.py rapor                 cetvel2_pozitif_kontrol.json -> CETVEL2_POZITIF_KONTROL.md
        python CETVEL2.py sha                   kod / eşik / girdi sha'ları
        python CETVEL2.py onkayit22 | kos22 [--islem 4] | rapor22 | sha22 | regresyon21    v2.2 (H = 15 / 30 / 45; KART_TUR1_IS_TANIMI.md ADIM K1)
Kütüphane (ADIM H):  import CETVEL2 as C2; R = C2.c2_olc(olaylar, hipotez)  (bkz. c2_olc belge dizesi)
Kütüphane (ADIM K2): R = C2.c2_olc22(olaylar, hipotez, ufuk=30, donem={...})  (v2.2; bkz. c2_olc22 belge dizesi)
Colab:  exec(open('CETVEL2.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (islenmis-veri). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı).
YAPI_HEDEF / DUSUS_SONRASI / ORTAK_CETVEL / POZITIF_KONTROL DEĞİŞTİRİLMEZ; içe alınır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_C2 = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_C2 = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_C2 not in sys.path:
    sys.path.insert(0, KOK_C2)

import DUSUS_SONRASI as DS  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import POZITIF_KONTROL as PK  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

c2log = logging.getLogger("col.cetvel2")
if not c2log.handlers:
    _c2_h = logging.StreamHandler(sys.stderr)
    _c2_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s cetvel2: %(message)s", "%H:%M:%S"))
    c2log.addHandler(_c2_h)
    c2log.setLevel(logging.INFO)
    c2log.propagate = False

C2_SURUM = "CETVEL2 v2.1 (2026-11-21): R15 konum eşli fark (bütün evren), plasebo kapısı (200 tohum), güç eğrisi; pozitif kontrol v2"
C2_ETIKET_SURUM = os.environ.get("C2_SURUM_ETIKET", "_v2.1")  # '' = v2.0 (ilk ön kayıt / koşu, silinmez); '_v2.1' = düzeltilmiş ön kayıt
C2_YOL = {"cikti": os.path.join(KOK_C2, "arastirma_cikti", "cetvel2"), "veri": os.environ.get("C2_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_C2, "CETVEL2.py"),
          "ds_olay": os.path.join(KOK_C2, "arastirma_cikti", "dusus_sonrasi", "ds_olay.csv.gz"),
          "pk_b": os.path.join(KOK_C2, "arastirma_cikti", "pozitif_kontrol", "pk_b_olay.csv.gz"),
          "pk_json": os.path.join(KOK_C2, "arastirma_cikti", "pozitif_kontrol", "pozitif_kontrol.json"),
          "pk_kod": os.path.join(KOK_C2, "POZITIF_KONTROL.py")}


def _c2_dosya(e: Optional[str] = None) -> Dict[str, str]:
    e = C2_ETIKET_SURUM if e is None else e
    return {"onkayit": f"CETVEL2_ON_KAYIT{e}.md", "esik": f"cetvel2_esik{e}.json", "guc": f"cetvel2_guc{e}.json",
            "prefix": f"cetvel2_prefix{e}.json", "json": f"cetvel2_pozitif_kontrol{e}.json", "rapor": f"CETVEL2_POZITIF_KONTROL{e}.md",
            "a_satir": f"c2_a_hucre{e}.csv.gz", "b_satir": f"c2_b_olay{e}.csv.gz", "c_satir": f"c2_c_plasebo{e}.csv"}


C2_PAZAR = ["ABD", "AVR", "BIST"]
C2_KARAR = ["ABD", "AVR"]
C2_HUCRE = ["egitim", "sinama"]
C2_KOVA_SAYI = 36          # 3 ATRP x 3 likidite x 4 F15

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
C2_ESIK: Dict[str, Any] = {
    "surum": "C2.1",
    "duzeltme_v21": "v2.0 pozitif kontrolü (CETVEL2_POZITIF_KONTROL.md) KUSUR verdi: (iii) A RAST delta 0 ABD eğitim n 1000 3 / 20 "
                    "tohum. Neden (yalnız sıfır verisiyle, 100 tohumlu tanı): cetvel hafif gevşek (sıfırda yakalama %1-7, ort ~%3,5; nominal %2,5) "
                    "ve 20 tohumlu kapılar kaba: plasebo kapısı (<= %7 = en çok 1 / 20) doğru ayarlı hücrede bile ~%9-15 şansla düşer, (iii) tek "
                    "(n) hücresinde > %10 (>= 3 / 20) 32 denemede şansla tetiklenir. DÜZELTME: plasebo tohum 20 -> 200 (eşikler AYNI); (iii) n >= "
                    "100 tohumları birleşik (80 tohum-hücre) > %10. R15, eş, kova, TUTAR, güç, etiket DEĞİŞMEDİ",
    "veri": "DUSUS_SONRASI.ds_veri (OC.oc_veri, evren dışı listesi, k34 YÜKLENMEZ, açılış H-L kırpması) + OC.oc_panel (kip 'gecmis'): geçerli bar "
            "(O/H/L/C > 0, H > L, V > 0), havuz (momentum / likidite bilinir, alt %20 likidite dışı, geçmiş bölünme şüphesi dışı), kriz kesiği "
            "31.08.2026",
    "giris": "OC.oc_olay_hazirla: t'den sonraki ilk geçerli bar AÇILIŞI E0 (t ile giriş arası <= 10 takvim günü; giriş günü havuzda)",
    "tekil_gun": 15,
    "tekil": "aynı hissede olaylar giriş günü sırasıyla, birleşik takvimde >= 15 işlem günü arayla (OC tekil kuralı, tekil_gun 15 = ufuk; olay "
             "kümesi bütün bayraklar için aynı)",
    "ufuk": 15, "pencere_azami": 30,
    "r15": "R15 = 15. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 30 birleşik takvim satırında 15 geçerli bar "
           "yoksa NaN (POZITIF_KONTROL.pk_r15 ile aynı; stop YOK)",
    "donem": {"egitim": ["2016-01-01", "2022-12-31"], "sinama": ["2023-01-01", "2026-08-31"], "tarih": "giriş günü; ambargo yok (kova sınırları "
                                                                                                        "getirisiz havuz dağılımından)"},
    "kova": {"atrp_gun": 14, "atrp_q": [1 / 3, 2 / 3], "f15_gun": 120, "f15_q": [0.25, 0.50, 0.75],
             "tanim": "kova = ATRP tercili x 3 + likidite üçlüsü, x 4 + F15 çeyreği (36 kova). ATRP_t = ort TR [t-13, t] / C_t (PK.pk_seri; DS ile "
                      "aynı), d gününde hissenin d'den önceki son geçerli barı (t) değeri. F15_t = (C_t - min C) / (max C - min C), t dahil son 120 "
                      "geçerli kapanış (YH.yh_f15_panel; d'den önceki son geçerli bar). Likidite üçlüsü = OC.oc_panel H % 3 (giriş günü havuz kesitinde "
                      "önceki 20 gün medyan C x V (x Kur) sırası; para birimi enflasyonu yüzünden sabit TL / $ sınırı kullanılmaz: günlük kesit "
                      "üçlüsü, sınırlar her gün havuzun 1/3 ve 2/3'ü). ATRP tercil ve F15 çeyrek SINIRLARI pazar başına EĞİTİM (giriş 2016-22) "
                      "havuz hisse-günlerinden (OC ok VE H >= 0 VE ATRP / F15 sonlu; getirisiz) numpy quantile (doğrusal); sayı olarak "
                      "cetvel2_esik.json ve ön kayıtta; sınama aynı sayılarla. F15 kovası: f <= q1 -> 0, <= q2 -> 1, <= q3 -> 2, değilse 3"},
    "es_min": 5,
    "es": "aynı giriş günü d, aynı pazar, aynı kova; havuzda (OC ok, H >= 0), R15'i ölçülebilir; aynı denemenin (hipotez bayrağı 1 olan) o gün "
          "olay olan hisseleri ve olayın kendisi çıkarılır; en az 5 eş (yoksa 'eşsiz', ölçülmez, sayısı yazılır)",
    "fark": "FARK = R15(olay) - ort R15(eş); SIRA = (#eş R15 < olay + 0,5 #eş = olay) / #eş",
    "boot": {"B": 2000, "alt": 0.025, "ust": 0.975, "tohum": 2111, "birim": "giriş ayı (YH.yh_d3_boot_l3o; L3O = en olumlu 3 ay çıkınca)"},
    "perm": {"R": 10000, "tohum": 2113, "tanim": "DS.ds_perm_p (ay kümeli işaret permütasyonu); yön '+' / '-' tek yönlü, '?' iki yönlü"},
    "guc": {"delta": 0.02, "z": 1.959963984540054, "esik": 0.80, "n": [30, 100, 300, 1000, 3000], "R": 1000, "tohum": 2112,
            "tanim": "pazar x dönem hücre sigma eğrisi: DS ANA olaylarının (ds_olay.csv.gz; tek tek eşlenmiş, deneme = olayın kendisi) FARK'ından n "
                     "olay yerine koymadan R kez (n <= N / 2), sigma(n) = std(ort FARK); ln sigma = a + b ln n en küçük kareler; güç(n) = "
                     "Phi(delta / sigma(n) - z); delta = +0,02 (R15 +2 puan getiri). Güç < 0,80 hücre ÖLÇÜLEMEDİ. Getiri ortalaması "
                     "kullanılmaz (yalnız yayılım)"},
    "hucre": {"n_min": 30, "sira": 0.50,
              "tutar": "n >= 30 VE güç >= 0,80 VE ort FARK > 0 VE boot alt > 0 VE ort SIRA > 0,50 VE L3O > 0 (beklenen yön '-' ise: FARK < 0 VE "
                       "boot üst < 0 VE SIRA < 0,50 VE L3O(-) < 0; '?' iki yönden biri)"},
    "plasebo": {"tohum_sayi": 200, "tohum": 2114, "fark_mutlak": 0.005, "tutar_pay": 0.07,
                "tanim": "hücrenin ölçülen her olayı yerine AYNI GİRİŞ GÜNÜ havuzdan rastgele bir hisse (gün içinde yerine koymadan; R15 "
                         "ölçülebilir, kovası var) -> aynı cetvel (eşler, en az 5, boot, SIRA, L3O, güç) -> 200 tohum (v2.1; v2.0 20). KAPI GEÇER = |200 "
                         "tohum ortalama FARK| < 0,005 (0,5 puan) VE TUTAR payı (hipotezin yönünde; '?' iki yön) <= %7. Geçmeyen hücre KARAR VERMEZ "
                         "(BİLGİ); nedeni yazılır"},
    "etiket": {"tanim": "karar hücreleri ABD x {eğitim, sınama}, AVR x {eğitim, sınama}; sıra: (1) ÇELİŞKİLİ = bir karar pazarında eğitim ve "
                        "sınama boot aralıkları sıfırın zıt taraflarında (ayrık); (2) ÖLÇÜLEMEDİ = bir karar hücresinde n < 30 ya da güç < 0,80; "
                        "(3) KATKI+ = dört karar hücresi plasebo kapısını geçer VE beklenen yönde TUTAR ('-' yönlü hipotezde 'TUTAR' ters "
                        "işaretlerle; '?' hipotezde dördü aynı yönde); KATKI− = dört hücre ters yönde TUTAR; (4) SORGULA = öteki durumlar (bazı "
                        "hücreler tutar ya da plasebo kapısı düşen karar hücresi var ya da hiçbiri tutmadı; sayı yanında yazılır). KATKI± "
                        "yalnız BH geçerse; geçmezse 'SORGULA (BH)'. BIST BİLGİ",
               "bh": {"q": 0.10, "p": "hipotez p = max(p ABD sınama, p AVR sınama) (önceden yazılı yön; n < 30 hücrede p = 1); m = c2_olc'ye verilen "
                                      "hipotez sayısı (ya da m_bh)"}},
    "bilgi": {"h5": "eski cetvel: YH.yh_sim, stop0 = hat x 0,98 (hat = son 20 geçerli bar en düşük Low, t dahil), +%5 kapanışla stop'tan önce "
                    "(h5 / st5 / h10)",
              "atr": "ATR stop kolu: stop0 = E0 - 2 x ATR14(t), +%5 stop'tan önce, 15 bar (h5_atr / st5_atr)",
              "r60": "OC.oc_esli r60 eşli fark (aynı gün, aynı momentum beşliği x likidite üçlüsü)", "r15_med": "hücre R15 medyanı"},
    "A": {"pazar": ["ABD", "AVR", "BIST"], "karar_pazar": ["ABD", "AVR"], "n": [30, 100, 300, 1000, "yari"],
          "delta": [0.0, 0.01, 0.02, 0.03, 0.05], "tohum_sayi": 20, "tohum": 2121, "n_azami_pay": 2 / 3,
          "olay": "DS ANA olayları (ds_olay.csv.gz: pazar, sembol, tarih; c2_olay ile giriş + kova + R15); havuz = hücrede R15 ölçülebilir ve tek "
                  "başına (deneme = kendisi) >= 5 eşi olan olaylar; her tohum x n x hücre havuzdan yerine koymadan n 'tutan' (yari = havuzun "
                  "yarısı; n > 2/3 havuz ise ölçülmez)",
          "taban": {"DS": "tutan = seçilen DS olayları (delta 0 = DS olaylarının kendi konum eşli FARK'ı; saf sıfır değil)",
                    "RAST": "tutan = her seçilen DS olayının giriş gününde havuzdan rastgele hisse (gün içinde yerine koymadan; c2_plasebo ile aynı "
                            "çekiliş); delta 0 = SAF PLASEBO"},
          "surukleme": "tutan olayın R15'i (1 + R15) x (1 + delta) - 1 (15. barda +delta doğrusal sürüklenmenin kapanış etkisi; E0 değişmez); eşler "
                       "dokunulmaz (deneme = tutan küme)",
          "yakala": "hücre TUTAR şartları güç HARİÇ (n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0); ayrıca güç dahil TUTAR ve p (tek "
                    "yönlü '+') < 0,05 bilgi"},
    "B": {"kaynak": "POZITIF_KONTROL pk_b_olay.csv.gz (aynı ANA olaylar: B1 momentum 12-1 ay sonu ABD + AVR, B2 PEAD ABD; U üst onda, A alt onda) "
                    "ve pozitif_kontrol.json h5 FARK'ı (yan yana)",
          "hipotez": {"B1U": ["U", "+"], "B1A": ["A", "-"], "B2U": ["U", "+"], "B2A": ["A", "-"]},
          "pazar": {"B1": ["ABD", "AVR"], "B2": ["ABD"]}, "karar_pazar": ["ABD"], "bilgi_pazar": ["AVR"]},
    "C": {"n": ["tam", 100, 300], "tohum": 2131,
          "tanim": "plasebo kapısı her pazar x dönem hücresinde DS ANA olay günleriyle (tam n ve n 100 / 300 rastgele alt küme günleri) ve B "
                   "hücrelerinde (c2_olc); AVR sınama tanısı: günlük havuz büyüklüğü, eş sayısı, eşsiz payı, dolu kova sayısı"},
    "sonuc_kurali": {
        "KUSUR": "(i) B1A (momentum alt onda) ABD eğitim ya da sınama hücresinde R15 FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı ABD "
                 "eğitim / sınama DS hücrelerinden (tam n) birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR "
                 "hücresinde n >= 100 tohumları BİRLEŞİK (100 / 300 / 1000 / yarı x 20 tohum) > %10 (v2.1; v2.0 tek n hücresi). KUSUR -> nedeni "
                 "yazılır, cetvel düzeltilir, ön kayıt v2.2, yeniden koşu (en çok 2 tur)",
        "EVET": "KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin her birinde bir n'de >= %80 yakalama VE B'de bir + etki (B1U ya da "
                "B2U) ABD eğitim ve sınamada FARK > 0 ve en az birinde boot alt > 0 VE bir - etki (B1A ya da B2A) ABD eğitim ve sınamada FARK < 0",
        "KISMEN": "KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)",
        "HAYIR": "KUSUR var (iki düzeltme turundan sonra da)"},
    "yeniden_uretim": {"elle_r15": 50, "elle_es": 5, "tohum": 2141,
                       "tanim": "c2_b_olay satır dosyasından iki hücre (B1U ABD sınama, B1A ABD eğitim) ortalama FARK / SIRA düz pandas ile; 50 olayın "
                                "R15'i ham veriden düz döngüyle; 5 olayın eş ortalaması bütün evren üzerinde düz döngüyle (kova elle)"},
}

C2_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü x F15 çeyreği), bütün evren havuzu, aynı geometri "
                   "(R15 stop'suz, aynı E0 kuralı); aynı denemenin o günkü olayları ve olayın kendisi eş dışı; en az 5 eş (c2_es); taban rastgele olay "
                   "sağlaması = plasebo kapısı (aynı gün rastgele havuz hissesi, 20 tohum; c2_plasebo); mekanik üstünlük: stop / hedef yok, R15 "
                   "olay ve eşte aynı tanım (h5'in oynaklık ödülü yok)"),
    "K2": ("EVET", "kova girdileri (ATRP_t, F15_t, likidite) giriş gününden ÖNCEKİ son geçerli barda; c2_prefix: her pazarda 30 rastgele olayda veri "
                   "t'de kesilince ATRP / F15 / hat aynı (rtol 1e-9; cetvel2_prefix.json, tutmazsa DURUR); kova sınırları eğitim havuzundan getirisiz; "
                   "R15 yalnız giriş açılışından sonrası"),
    "K3": ("EVET", "OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması; R15 yalnız geçerli barlar (hissenin kendi takvimi); "
                   "sinyal günü geçersiz bar ise olay düşer (oc_olay_hazirla)"),
    "K4": ("EVET", "olaylar aynı hissede >= 15 işlem günü arayla (tekil_gun 15 = ufuk; örtüşmeyen 15 bar); n = ölçülen olay; boot / permütasyon "
                   "birimi giriş ayı; medyan FARK raporda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (oc_olay_hazirla d; R15 paydası P['Op'][d, j]); eşler aynı gün açılışı"),
    "K6": ("EVET", "V_*.pkl tek kip (fi_k1_veri düzeltilmiş); R15 / ATRP / F15 oran (birimsiz); likidite üçlüsü günlük kesit sırası (TL enflasyonu "
                   "etkisiz; AVR x Kur); geçmiş bölünme şüphesi havuz dışı (OC)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST); yanlılık hem olaya hem eşe; raporda yazılır"),
    "K8": ("EVET", "eğitim 2016-22 / sınama 2023-01 .. 2026-08 ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç eğrisi (delta +2 puan, %80) ile n yeterliliği; "
                   "BH q 0,10 (m sabit); A: 20 tohum x 5 n x 5 delta"),
    "K9": ("EVET", "CETVEL2_ON_KAYIT_v2.1.md (v2.0 CETVEL2_ON_KAYIT.md silinmedi; düzeltme C2_ESIK['duzeltme_v21']): C2_ESIK sha, CETVEL2.py sha, kova sınırları (sayı), güç eğrisi, DS / YH / OC / PK sha'ları, girdi dosyası "
                   "sha'ları; c2_kapi ön kaydın git'te işlenmiş ve değişmemiş olduğunu + ik_kontrol_kapisi'ni denetler; sıra kod commit -> ön kayıt "
                   "commit -> koşu; tasarım iş tanımından (ca5d2a8) sonuç görülmeden"),
    "K10": ("UYGULANMAZ", "ham haber / KAP / SEC ayrıştırması yok; olay kümeleri önceki koşuların satır dosyalarından (ds_olay.csv.gz, "
                          "pk_b_olay.csv.gz) okunur, sayıları huni'de karşılaştırılır"),
    "K11": ("EVET", "c2_yeniden: B1U ABD sınama ve B1A ABD eğitim hücreleri satır dosyasından düz pandas; 50 olayın R15'i ham veriden düz döngüyle; "
                    "5 olayın eş ortalaması bütün evren üzerinde düz döngüyle (kova elle); tutmazsa koşu TUTMADI"),
    "K12": ("EVET", "bu iş cetvel sınaması; 'iz' iddiası yok; FARK, SIRA, p, yakalama payı ayrı; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_c2; c2_ / C2_ önekleri dışında ezme DURUR; test); DS / YH / OC / PK değişmedi (sha ön kayıtta); "
                    "defter dosyalarına dokunulmadı; e-posta / anahtar taraması (YH._yh_yaz); dış servis yok; kod değişirse 'çalışma zamanını "
                    "yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; cetvel sınaması"),
}


class C2Hata(RuntimeError):
    """Durdurucu hata: veri yok, mühür / sha tutmuyor, prefix tutmuyor, yeniden üretim tutmadı."""


# ================================================================ 0) ORTAK
def _c2_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def c2_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(C2_ESIK if E is None else E)


def _c2_yol(ad: str, cikti: Optional[str] = None, e: Optional[str] = None) -> str:
    return os.path.join(cikti or C2_YOL["cikti"], _c2_dosya(e).get(ad, ad))


def _c2_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _c2_donem(g: Any) -> np.ndarray:
    g = pd.to_datetime(pd.Series(g)); Dn = C2_ESIK["donem"]
    eg = (g >= Dn["egitim"][0]) & (g <= Dn["egitim"][1]); sn = (g >= Dn["sinama"][0]) & (g <= Dn["sinama"][1])
    return np.where(eg, "egitim", np.where(sn, "sinama", "dis"))


def _c2_phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


# ================================================================ 1) VERİ ve PANEL
def c2_veri(pazar: str, veri: Optional[str] = None) -> Dict[str, Any]:
    """DUSUS_SONRASI.ds_veri (OC.oc_veri + açılış kırpması; k34 yüklenmez)."""
    if pazar not in C2_PAZAR:
        raise C2Hata(f"bilinmeyen pazar {pazar}")
    return DS.ds_veri(pazar, veri or C2_YOL["veri"])


def c2_kova_sinir(Pn: Dict[str, Any]) -> Dict[str, Any]:
    """Eğitim (giriş 2016-22) havuz hisse-günlerinden ATRP tercil ve F15 çeyrek sınırları (getirisiz)."""
    P = Pn["P"]; Dn = C2_ESIK["donem"]["egitim"]; idx = P["tarih"]
    sat = (idx >= pd.Timestamp(Dn[0])) & (idx <= pd.Timestamp(Dn[1]))
    m = P["ok"] & (P["H"] >= 0) & np.isfinite(Pn["ATRP"]) & np.isfinite(Pn["F15"]) & sat[:, None]
    a = Pn["ATRP"][m]; f = Pn["F15"][m]
    if len(a) < 1000:
        raise C2Hata(f"{P['pazar']}: eğitim havuzunda kova sınırı için yeterli hisse-gün yok ({len(a)})")
    K = C2_ESIK["kova"]
    return {"ATRP": [float(np.quantile(a, q)) for q in K["atrp_q"]], "F15": [float(np.quantile(f, q)) for q in K["f15_q"]],
            "n_hisse_gun": int(len(a)), "lq_tanim": "OC H % 3 (günlük kesit)"}


def c2_kova(ATRP: np.ndarray, LQ: np.ndarray, F15: np.ndarray, sinir: Dict[str, Any]) -> np.ndarray:
    """ATRP tercili x 12 + likidite üçlüsü x 4 + F15 çeyreği; eksik -> -1."""
    t1, t2 = sinir["ATRP"]; q1, q2, q3 = sinir["F15"]
    a = np.asarray(ATRP, float); f = np.asarray(F15, float); lq = np.asarray(LQ, int)
    with np.errstate(invalid="ignore"):
        at = np.where(a <= t1, 0, np.where(a <= t2, 1, 2))
        fq = np.where(f <= q1, 0, np.where(f <= q2, 1, np.where(f <= q3, 2, 3)))
    ok = np.isfinite(a) & np.isfinite(f) & (lq >= 0)
    return np.where(ok, at * 12 + lq * 4 + fq, -1)


def c2_panel(Vd: Dict[str, Any], sinir: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """OC paneli + R15 / ATRP / ATR / hat / F15 matrisleri (giriş günü d x hisse) + kova + eş havuzu dizileri.
    ATRP / ATR / hat d'de = hissenin d'den önceki son geçerli barındaki (t) değer; F15 YH.yh_f15_panel."""
    t0 = time.time()
    P = OC.oc_panel(Vd); idx = P["tarih"]; S = P["sembol"]; n, u = len(idx), len(S)
    Cl = YH.yh_kapanis(P, Vd)
    uf, Rz = int(C2_ESIK["ufuk"]), int(C2_ESIK["pencere_azami"])
    R15 = np.full((n, u), np.nan); AT = np.full((n, u), np.nan); ATR = np.full((n, u), np.nan); HAT = np.full((n, u), np.nan)
    for j, s in enumerate(S):
        df = Vd["V"][s]; pos = idx.get_indexer(df.index)
        if (pos < 0).any():
            raise C2Hata(f"{s}: hisse takvimi panelde yok")
        O = df.Open.to_numpy(float); C = df.Close.to_numpy(float); m = len(pos); k = uf - 1
        if m > k:
            e = np.arange(m - k); f = e + k; ok = (pos[f] - pos[e]) <= Rz - 1
            with np.errstate(invalid="ignore", divide="ignore"):
                R15[pos[e[ok]], j] = C[f[ok]] / O[e[ok]] - 1
        atrp, hat = PK.pk_seri(df)
        a = atrp.to_numpy(float); h = hat.to_numpy(float)
        if m > 1:
            AT[pos[1:], j] = a[:-1]; ATR[pos[1:], j] = a[:-1] * C[:-1]; HAT[pos[1:], j] = h[:-1]
    F15 = YH.yh_f15_panel(P, Vd)
    LQ = np.where(P["H"] >= 0, P["H"] % 3, -1)
    Pn = {"pazar": P["pazar"], "P": P, "Cl": Cl, "R15": R15, "ATRP": AT, "ATR": ATR, "HAT": HAT, "F15": F15, "LQ": LQ, "Vd": Vd}
    if sinir is None:
        sinir = c2_kova_sinir(Pn)
    Pn["sinir"] = sinir
    KV = c2_kova(AT, LQ, F15, sinir); KV[~(P["ok"] & (P["H"] >= 0))] = -1
    Pn["KV"] = KV
    _c2_havuz(Pn)
    c2log.info("%s panel: %d gün x %d hisse, havuz (R15 + kova) %d hisse-gün (%.0f sn)", P["pazar"], n, u, len(Pn["h_r"]), time.time() - t0)
    return Pn


def _c2_havuz(Pn: Dict[str, Any]) -> None:
    """Eş havuzu: (gün, kova) anahtarı ve R15'e göre sıralı düz diziler; tam sayı kodla kesin sıra / eşitlik sayımı."""
    KV, R15 = Pn["KV"], Pn["R15"]; K = C2_KOVA_SAYI
    pm = (KV >= 0) & np.isfinite(R15)
    dd, jj = np.nonzero(pm)
    key = dd.astype(np.int64) * K + KV[dd, jj].astype(np.int64); r = R15[dd, jj]
    o = np.lexsort((r, key))
    dd, jj, key, r = dd[o], jj[o], key[o], r[o]
    uv = np.unique(r); rk = np.searchsorted(uv, r).astype(np.int64); M = np.int64(2 * len(uv) + 2)
    code = key * M + 2 * rk + 1
    if len(code) > 1 and not (np.diff(code) >= 0).all():
        raise C2Hata("havuz kodu sıralı değil")
    pix = np.full(KV.shape, -1, np.int64); pix[dd, jj] = np.arange(len(dd))
    Pn.update({"h_d": dd, "h_j": jj, "h_key": key, "h_r": r, "h_uv": uv, "h_M": M, "h_code": code,
               "h_cs": np.r_[0.0, np.cumsum(r)], "h_pix": pix})


_C2_PN: Dict[str, Dict[str, Any]] = {}


def c2_panel_al(pazar: str, veri: Optional[str] = None, sinir: Optional[Dict[str, Any]] = None, onbellek: bool = True) -> Dict[str, Any]:
    """Panel önbelleği (pazar başına). sinir verilmezse cetvel2_esik.json (varsa) kullanılır, yoksa eğitimden hesaplanır."""
    if onbellek and pazar in _C2_PN and (sinir is None or _C2_PN[pazar]["sinir"] == sinir):
        return _C2_PN[pazar]
    if sinir is None:
        yol = _c2_yol("esik")
        if os.path.exists(yol):
            sinir = json.load(open(yol, encoding="utf-8"))["sinir"].get(pazar)
    Pn = c2_panel(c2_veri(pazar, veri), sinir)
    if onbellek:
        _C2_PN[pazar] = Pn
    return Pn


# ================================================================ 2) OLAY ve EŞ
def c2_olay(olaylar: pd.DataFrame, Pn: Dict[str, Any], tekil_gun: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Olay listesi (sembol, tarih, [F_* ...]) -> OC.oc_olay_hazirla (giriş, havuz, tekil) + donem, kova, R15, ATRP, F15, hat, ATR.
    Girdideki öteki sütunlar (bayraklar) (sembol, tarih) ile geri eklenir."""
    P = Pn["P"]
    E1 = json.loads(json.dumps(OC.OC_ESIK)); E1["olay"]["tekil_gun"] = int(tekil_gun or C2_ESIK["tekil_gun"])
    ol = olaylar.copy(); ol["tarih"] = pd.to_datetime(ol["tarih"]).dt.normalize(); ol["sembol"] = ol["sembol"].astype(str)
    dup = int(ol.duplicated(["sembol", "tarih"]).sum())
    if dup:
        c2log.warning("%s: girdide %d tekrar (sembol, tarih) satırı; ilki tutulur", Pn["pazar"], dup)
        ol = ol.drop_duplicates(["sembol", "tarih"], keep="first")
    X, say = OC.oc_olay_hazirla(ol.assign(pazar=Pn["pazar"])[["sembol", "tarih", "pazar"]], P, E1)
    ek = [c for c in ol.columns if c not in ("sembol", "tarih", "pazar", "giris", "d", "j", "hucre", "donem")]
    X = X.merge(ol[["sembol", "tarih"] + ek], on=["sembol", "tarih"], how="left", validate="one_to_one")
    d = X.d.to_numpy(int); j = X.j.to_numpy(int)
    X["pazar"] = Pn["pazar"]; X["donem"] = _c2_donem(X.giris)
    X["kova"] = Pn["KV"][d, j]; X["atrp"] = Pn["ATRP"][d, j]; X["f15"] = Pn["F15"][d, j]; X["lq3"] = Pn["LQ"][d, j]
    X["hat"] = Pn["HAT"][d, j]; X["atr"] = Pn["ATR"][d, j]; X["E0"] = P["Op"][d, j]; X["r15"] = Pn["R15"][d, j]
    say = {**say, "olcum_r15": int(np.isfinite(X.r15).sum()), "kova_yok": int((X.kova < 0).sum()),
           "donem": {k: int(v) for k, v in pd.Series(X.donem).value_counts().items()}}
    return X.reset_index(drop=True), say


def c2_es(Pn: Dict[str, Any], d: np.ndarray, j: np.ndarray, x: np.ndarray, exc_d: Optional[np.ndarray] = None,
          exc_j: Optional[np.ndarray] = None, es_min: Optional[int] = None) -> Dict[str, np.ndarray]:
    """Konum eşli eş istatistikleri. d, j: olay giriş günü / hisse; x: olayın R15'i (sürüklenmiş olabilir). Eş kümesi = aynı (d, kova) havuzu
    eksi dışlananlar (deneme kümesi exc ∪ olayların kendisi). Döner: es_r15 (ort), n_es, sira, fark (eşsiz -> NaN)."""
    d = np.asarray(d, np.int64); j = np.asarray(j, np.int64); x = np.asarray(x, float); ne = len(d)
    me = int(es_min or C2_ESIK["es_min"]); K = C2_KOVA_SAYI
    out = {k: np.full(ne, np.nan) for k in ("es_r15", "sira", "fark")}; out["n_es"] = np.zeros(ne)
    if ne == 0:
        return out
    kv = Pn["KV"][d, j].astype(np.int64)
    key = d * K + kv
    hk, code, cs, uv, M = Pn["h_key"], Pn["h_code"], Pn["h_cs"], Pn["h_uv"], Pn["h_M"]
    lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right")
    N = (hi - lo).astype(float); Ssum = cs[hi] - cs[lo]
    xf = np.where(np.isfinite(x), x, 0.0)
    gl = np.searchsorted(uv, xf, "left").astype(np.int64); gr = np.searchsorted(uv, xf, "right").astype(np.int64)
    less = (np.searchsorted(code, key * M + 2 * gl + 1, "left") - lo).astype(float)
    le = (np.searchsorted(code, key * M + 2 * gr + 1, "left") - lo).astype(float)
    eq = le - less
    # dışlananlar: deneme kümesi ∪ olayların kendisi, havuzda olanlar, tekil
    ed = d if exc_d is None else np.r_[np.asarray(exc_d, np.int64), d]
    ej = j if exc_j is None else np.r_[np.asarray(exc_j, np.int64), j]
    pp = Pn["h_pix"][ed, ej]; pp = np.unique(pp[pp >= 0])
    if len(pp):
        xk = hk[pp]; xr = Pn["h_r"][pp]; o = np.argsort(xk, kind="stable"); xk, xr = xk[o], xr[o]
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
    out["es_r15"] = np.where(ok, es, np.nan); out["sira"] = np.where(ok, sira, np.nan)
    out["fark"] = np.where(ok, x - es, np.nan); out["n_es"] = np.where(kv >= 0, N, 0.0)
    return out


# ================================================================ 3) GÜÇ, HÜCRE, PLASEBO
def c2_guc_egri(fark: np.ndarray, tohum_ek: int = 0) -> Dict[str, Any]:
    """Hücre tabanı FARK'larından sigma(n) eğrisi: n <= N / 2 noktalarında yerine koymadan R kez ortalama; ln sigma = a + b ln n."""
    G = C2_ESIK["guc"]; f = np.asarray(fark, float); f = f[np.isfinite(f)]; N = len(f)
    rng = np.random.default_rng([int(G["tohum"]), int(tohum_ek)]); tab = []
    for n in G["n"]:
        if n > N / 2:
            continue
        mr = np.array([f[rng.choice(N, n, replace=False)].mean() for _ in range(int(G["R"]))])
        tab.append({"n": int(n), "sigma": float(mr.std(ddof=1))})
    if not tab:
        sd = float(np.std(f, ddof=1)) if N > 2 else float("nan")
        return {"N": N, "sd": sd, "tablo": [], "a": math.log(sd) if sd and np.isfinite(sd) and sd > 0 else float("nan"), "b": -0.5,
                "not": "N / 2 < 30: sigma = sd / kök n varsayımı"}
    if len(tab) == 1:
        b = -0.5; a = math.log(tab[0]["sigma"]) - b * math.log(tab[0]["n"])
    else:
        lx = np.log([t["n"] for t in tab]); ly = np.log([t["sigma"] for t in tab]); b, a = np.polyfit(lx, ly, 1); a, b = float(a), float(b)
    return {"N": N, "sd": float(np.std(f, ddof=1)), "tablo": tab, "a": a, "b": b}


def c2_guc(n: int, egri: Optional[Dict[str, Any]], delta: Optional[float] = None) -> float:
    """güç(n) = Phi(delta / sigma(n) - z); sigma(n) = exp(a + b ln n). Eğri yoksa NaN."""
    G = C2_ESIK["guc"]; dl = float(G["delta"] if delta is None else delta)
    if not egri or n <= 0 or not np.isfinite(egri.get("a", np.nan)):
        return float("nan")
    sg = math.exp(float(egri["a"]) + float(egri["b"]) * math.log(n))
    return _c2_phi(dl / sg - float(G["z"])) if sg > 0 else float("nan")


def _c2_l3o_neg(g: pd.DataFrame, tohum_ek: int) -> float:
    gn = pd.DataFrame({"h5": -g.h5.to_numpy(float), "es_h5": -g.es_h5.to_numpy(float), "giris": g.giris.to_numpy()})
    b = YH.yh_d3_boot_l3o(gn, gn.assign(h5=gn.es_h5), C2_ESIK, tohum_ek=tohum_ek)
    return -float(b["l3o"]) if np.isfinite(b["l3o"]) else float("nan")


def c2_hucre(r15: np.ndarray, es: np.ndarray, sira: np.ndarray, giris: Any, yon: str, tohum_ek: int = 0,
             egri: Optional[Dict[str, Any]] = None, perm: bool = True, l3o_neg: Optional[bool] = None) -> Dict[str, Any]:
    """Bir hücre: n, ort / medyan FARK, ort SIRA, boot %95, L3O (+ ve -), p (yön), güç, TUTAR (beklenen yön) ve TERS."""
    g = pd.DataFrame({"h5": np.asarray(r15, float), "es_h5": np.asarray(es, float), "sira": np.asarray(sira, float),
                      "giris": pd.to_datetime(np.asarray(giris))})
    g = g[np.isfinite(g.h5) & np.isfinite(g.es_h5)]
    n = int(len(g)); H = C2_ESIK["hucre"]
    c: Dict[str, Any] = {"n": n, "fark": np.nan, "med": np.nan, "sira": np.nan, "boot_alt": np.nan, "boot_ust": np.nan, "l3o": np.nan,
                         "l3o_neg": np.nan, "p": np.nan, "guc": c2_guc(n, egri) if egri else np.nan, "r15_ort": np.nan, "r15_med": np.nan,
                         "es_ort": np.nan, "ay": 0}
    if n == 0:
        c.update({"tutar_p": False, "tutar_n": False, "tutar": False, "ters": False, "yakala": False})
        return c
    f = (g.h5 - g.es_h5).to_numpy(float)
    c.update({"fark": float(f.mean()), "med": float(np.median(f)), "sira": float(g.sira.mean()), "r15_ort": float(g.h5.mean()),
              "r15_med": float(g.h5.median()), "es_ort": float(g.es_h5.mean()), "ay": int(g.giris.dt.strftime("%Y-%m").nunique())})
    b = YH.yh_d3_boot_l3o(g, g.assign(h5=g.es_h5), C2_ESIK, tohum_ek=tohum_ek)     # Xa: h5 - es_h5 = FARK; Xk: 0 (DS / PK ile aynı)
    c.update({"boot_alt": b["boot_alt"], "boot_ust": b["boot_ust"], "l3o": b["l3o"]})
    if l3o_neg is None:
        l3o_neg = yon in ("-", "?")
    if l3o_neg:
        c["l3o_neg"] = _c2_l3o_neg(g, tohum_ek)
    if perm:
        c["p"] = DS.ds_perm_p(g, yon if yon in ("+", "-") else "?", int(C2_ESIK["perm"]["R"]), int(C2_ESIK["perm"]["tohum"]) + int(tohum_ek))
    gucok = bool(np.isfinite(c["guc"]) and c["guc"] >= float(C2_ESIK["guc"]["esik"])) if egri else True
    yp = bool(n >= H["n_min"] and c["fark"] > 0 and np.isfinite(c["boot_alt"]) and c["boot_alt"] > 0 and c["sira"] > H["sira"]
              and np.isfinite(c["l3o"]) and c["l3o"] > 0)
    yn = bool(n >= H["n_min"] and c["fark"] < 0 and np.isfinite(c["boot_ust"]) and c["boot_ust"] < 0 and c["sira"] < H["sira"]
              and np.isfinite(c["l3o_neg"]) and c["l3o_neg"] < 0)
    c["yakala_p"], c["yakala_n"] = yp, yn
    c["tutar_p"], c["tutar_n"] = yp and gucok, yn and gucok
    if yon == "+":
        c["tutar"], c["ters"], c["yakala"] = c["tutar_p"], c["tutar_n"], yp
    elif yon == "-":
        c["tutar"], c["ters"], c["yakala"] = c["tutar_n"], c["tutar_p"], yn
    else:
        c["tutar"], c["ters"], c["yakala"] = c["tutar_p"] or c["tutar_n"], False, yp or yn
    return c


def c2_rastgele(Pn: Dict[str, Any], d: np.ndarray, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    """Her olay günü için havuzdan (R15 + kova) rastgele hisse; aynı gün içinde yerine koymadan. Döner (d, j) (havuzu boş gün düşer)."""
    d = np.asarray(d, np.int64); K = C2_KOVA_SAYI; hk = Pn["h_key"]
    gun, say = np.unique(d, return_counts=True)
    lo = np.searchsorted(hk, gun * K, "left"); hi = np.searchsorted(hk, (gun + 1) * K, "left")
    od, oj = [], []
    for g_, k_, a, b in zip(gun, say, lo, hi):
        m = int(b - a)
        if m <= 0:
            continue
        sec = a + rng.choice(m, size=min(int(k_), m), replace=False)
        od.append(Pn["h_d"][sec]); oj.append(Pn["h_j"][sec])
    if not od:
        return np.array([], np.int64), np.array([], np.int64)
    return np.concatenate(od).astype(np.int64), np.concatenate(oj).astype(np.int64)


def c2_plasebo(Pn: Dict[str, Any], d: np.ndarray, yon: str, egri: Optional[Dict[str, Any]], tohum_ek: int = 0,
               tohum_sayi: Optional[int] = None, iki_yon_ayri: bool = False) -> Dict[str, Any]:
    """Plasebo kapısı: olay günleriyle (aynı gün) rastgele havuz hisseleri, 20 tohum, aynı cetvel. Döner ortalama FARK, tutar payı, geçti.
    iki_yon_ayri (v2.2, H286 / Ç204 hata v): '?' hipotezde tutar payı eşiği iki yön için AYRI (+ payı <= %7 VE - payı <= %7); v2.1 (False)
    '?' için birleşik (+ ya da -) payı %7 ile karşılaştırır. '+' / '-' hipotezde ikisi aynı."""
    Pl = C2_ESIK["plasebo"]; T = int(tohum_sayi or Pl["tohum_sayi"]); sat = []
    idx = Pn["P"]["tarih"]
    for t in range(T):
        rng = np.random.default_rng([int(Pl["tohum"]), int(tohum_ek) % (2 ** 31), t])
        rd, rj = c2_rastgele(Pn, d, rng)
        x = Pn["R15"][rd, rj]
        e = c2_es(Pn, rd, rj, x, rd, rj)
        c = c2_hucre(x, e["es_r15"], e["sira"], idx[rd], yon, tohum_ek=900000 + t, egri=egri, perm=False, l3o_neg=True)
        sat.append({"tohum": t, "n": c["n"], "fark": c["fark"], "sira": c["sira"], "tutar": bool(c["tutar"]), "yakala": bool(c["yakala"]),
                    "tutar_p": bool(c["tutar_p"]), "tutar_n": bool(c["tutar_n"]), "yakala_p": bool(c.get("yakala_p", False)),
                    "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"]})
    S = pd.DataFrame(sat)
    fo = float(S.fark.mean()) if len(S) else np.nan; tp = float(S.tutar.mean()) if len(S) else np.nan
    gec = bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_mutlak"]) and np.isfinite(tp) and tp <= float(Pl["tutar_pay"]))
    if iki_yon_ayri and yon == "?":
        gec = bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_mutlak"]) and len(S) and S.tutar_p.mean() <= float(Pl["tutar_pay"])
                   and S.tutar_n.mean() <= float(Pl["tutar_pay"]))
    return {"fark_ort": fo, "fark_sd": float(S.fark.std(ddof=1)) if len(S) > 1 else np.nan, "tutar_pay": tp,
            "tutar_pay_arti": float(S.tutar_p.mean()) if len(S) else np.nan, "tutar_pay_eksi": float(S.tutar_n.mean()) if len(S) else np.nan,
            "gecti_arti": bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_mutlak"]) and len(S) and S.tutar_p.mean() <= float(Pl["tutar_pay"])),
            "gecti_eksi": bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_mutlak"]) and len(S) and S.tutar_n.mean() <= float(Pl["tutar_pay"])),
            "yakala_pay": float(S.yakala.mean()) if len(S) else np.nan, "n_ort": float(S.n.mean()) if len(S) else np.nan, "gecti": gec,
            "tohum": sat}


# ================================================================ 4) ETİKET ve BH
def c2_bh(p: List[float], q: Optional[float] = None) -> List[bool]:
    return YH._yh_bh(list(p), float(q if q is not None else C2_ESIK["etiket"]["bh"]["q"]))


def c2_etiket(h: Dict[str, Dict[str, Dict[str, Any]]], yon: str, karar: Optional[List[str]] = None,
              hucreler: Optional[List[str]] = None) -> Dict[str, Any]:
    """h[pazar][hücre] -> hücre sözlüğü (c2_hucre + 'plasebo_gecti'). Ham etiket (BH öncesi) ve gerekçe.
    hucreler (v2.2): karar hücre adları (varsayılan C2_HUCRE = eğitim / sınama); ÇELİŞKİLİ ilk ve son hücreyi karşılaştırır."""
    karar = karar or C2_KARAR
    hl = list(hucreler) if hucreler else C2_HUCRE
    H_ = [(p, k, h.get(p, {}).get(k)) for p in karar for k in hl]

    def poz(c):
        return c is not None and np.isfinite(c.get("boot_alt", np.nan)) and c["boot_alt"] > 0

    def neg(c):
        return c is not None and np.isfinite(c.get("boot_ust", np.nan)) and c["boot_ust"] < 0
    for p in karar:
        a, b = h.get(p, {}).get(hl[0]), h.get(p, {}).get(hl[-1])
        if (poz(a) and neg(b)) or (neg(a) and poz(b)):
            return {"etiket": "ÇELİŞKİLİ", "neden": (f"{p} eğitim / sınama boot aralıkları sıfırın zıt tarafında" if hucreler is None else
                                                    f"{p} {hl[0]} / {hl[-1]} boot aralıkları sıfırın zıt tarafında")}
    eksik = [f"{p} {k}" for p, k, c in H_ if c is None or c["n"] < C2_ESIK["hucre"]["n_min"]
             or not (np.isfinite(c.get("guc", np.nan)) and c["guc"] >= C2_ESIK["guc"]["esik"])]
    if eksik:
        return {"etiket": "ÖLÇÜLEMEDİ", "neden": "n < 30 ya da güç < 0,80: " + ", ".join(eksik)}
    kapi = [f"{p} {k}" for p, k, c in H_ if not c.get("plasebo_gecti", False)]
    tp = [bool(c["tutar_p"]) for _, _, c in H_]; tn = [bool(c["tutar_n"]) for _, _, c in H_]
    if not kapi:
        if yon in ("+", "?") and all(tp):
            return {"etiket": "KATKI+", "neden": "dört karar hücresi + yönde TUTAR, plasebo kapısı geçti"}
        if yon in ("-", "?") and all(tn):
            return {"etiket": "KATKI−", "neden": "dört karar hücresi - yönde TUTAR, plasebo kapısı geçti"}
        if yon == "+" and all(tn):
            return {"etiket": "KATKI− (ters)", "neden": "beklenen + ama dört hücre - yönde TUTAR"}
        if yon == "-" and all(tp):
            return {"etiket": "KATKI+ (ters)", "neden": "beklenen - ama dört hücre + yönde TUTAR"}
    nt = sum(bool(c["tutar"]) for _, _, c in H_)
    ne = f"{nt} / 4 karar hücresi beklenen yönde TUTAR" + (f"; plasebo kapısı düşen: {', '.join(kapi)}" if kapi else "")
    return {"etiket": "SORGULA", "neden": ne}


# ================================================================ 5) BİLGİ SÜTUNLARI (eski h5, ATR stop, r60)
def c2_bilgi(Pn: Dict[str, Any], X: pd.DataFrame) -> pd.DataFrame:
    """h5 / st5 / h10 (stop0 = hat x 0,98), h5_atr / st5_atr (stop0 = E0 - 2 ATR14(t)), r60 / esli_r60 (OC.oc_esli). Yalnız olay satırları."""
    P = Pn["P"]; Rz = int(YH.YH_ESIK["olcu"]["pencere_azami"]); out = pd.DataFrame(index=X.index)
    d = X.d.to_numpy(int); j = X.j.to_numpy(int); E0 = P["Op"][d, j]
    for c in ("h5", "st5", "h10", "h5_atr", "st5_atr", "r60", "esli_r60"):
        out[c] = np.nan
    if not len(X):
        return out
    hc = float(YH.YH_ESIK["olcu"]["stop0"]["hat_carpan"])
    for i0 in range(0, len(X), 20000):
        sl = slice(i0, i0 + 20000); dd, jj = d[sl], j[sl]
        Cr, Hr, Lr = PK._pk_pencere(Pn["Cl"], dd, jj, Rz), PK._pk_pencere(P["Hi"], dd, jj, Rz), PK._pk_pencere(P["Lo"], dd, jj, Rz)
        e0 = E0[sl]
        for ad, st in (("", X.hat.to_numpy(float)[sl] * hc), ("_atr", e0 - 2.0 * X.atr.to_numpy(float)[sl])):
            okk = np.isfinite(st) & np.isfinite(e0) & (st < e0) & (st > 0)
            st2 = np.where(okk, st, e0 * 0.5)
            S = YH.yh_sim(Cr, Hr, Lr, e0, st2, 1)
            out.iloc[sl, out.columns.get_loc("h5" + ad)] = np.where(okk, S["h5"], np.nan)
            out.iloc[sl, out.columns.get_loc("st5" + ad)] = np.where(okk, S["st5"], np.nan)
            if ad == "":
                out.iloc[sl, out.columns.get_loc("h10")] = np.where(okk, S["h10"], np.nan)
    try:
        Xo = OC.oc_esli(P, X[["sembol", "tarih", "giris", "d", "j"]].reset_index(drop=True))
        out["r60"] = Xo.r60.to_numpy(float); out["esli_r60"] = Xo.esli_r60.to_numpy(float)
    except Exception as ex:   # r60 yalnız bilgi; hata olursa NaN kalır ve loglanır
        c2log.warning("%s r60 bilgi sütunu hesaplanamadı: %s", Pn["pazar"], ex)
    return out


# ================================================================ 6) ANA ÖLÇÜM (ADIM H arayüzü)
def _c2_egri_al(pazar: str, hucre: str, guc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if guc is None:
        yol = _c2_yol("guc")
        if not os.path.exists(yol):
            return None
        guc = json.load(open(yol, encoding="utf-8"))
    return guc.get("egri", {}).get(pazar, {}).get(hucre)


def c2_olc(olaylar: pd.DataFrame, hipotez: Dict[str, Dict[str, Any]], veri: Optional[str] = None, plasebo: bool = True, bilgi: bool = True,
           m_bh: Optional[int] = None, tohum0: int = 0, guc: Optional[Dict[str, Any]] = None, tekil_gun: Optional[int] = None,
           karar: Optional[List[str]] = None, ufuk: Optional[int] = None, donem: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
    """ADIM H ARAYÜZÜ (v2.1; ufuk verilirse v2.2, bkz. c2_olc22 belge dizesi).
    olaylar: DataFrame[pazar, sembol, tarih (sinyal günü t), F_<...> bayrak sütunları (1 / 0 / NaN)]. Pazarlar ABD / AVR / BIST.
    hipotez: {kod: {'bayrak': 'F_x' ya da None (bütün olaylar), 'yon': '+' / '-' / '?'}}.
    Döner {'satir': olay satırları (pazar, sembol, tarih, giris, d, j, donem, kova, atrp, f15, lq3, hat, atr, E0, r15, bilgi sütunları h5 / st5 /
           h10 / h5_atr / st5_atr / r60 / esli_r60, bayraklar, her kod için es_r15_<kod>, n_es_<kod>, sira_<kod>, fark_<kod>),
           'hucre': DataFrame[kod, yon, pazar, hucre, n, n_bayrak, n_essiz, fark, med, sira, boot_alt, boot_ust, l3o, l3o_neg, p, guc, tutar,
                    ters, yakala, r15_ort, r15_med, es_ort, plasebo_fark, plasebo_tutar_pay, plasebo_gecti, durum, h5, st5, h5_atr, st5_atr,
                    r60_fark],
           'etiket': DataFrame[kod, yon, etiket_ham, neden, p_bh, bh_gecti, etiket], 'say': huni}.
    Eşler: aynı denemenin (kod) bayrağı 1 olan o günkü olay hisseleri eş dışı. Kova sınırları cetvel2_esik.json, güç cetvel2_guc.json.
    v2.2 (ufuk = 15 / 30 / 45): R_H = H. geçerli bar kapanışı / E0 - 1 ('r15' sütunu R_H'yi taşır; 'ufuk' sütunu eklenir), pencere 2H satır,
    tekil H, kova sınırları / güç cetvel2_esik_v2.2.json / cetvel2_guc_v2.2.json, hücreler donem sözlüğünden (varsayılan C2_ESIK22 d1619 /
    d2022), plasebo '?' yön başına; ufuk None iken davranış v2.1 ile bayt bayt aynı."""
    t0 = time.time(); karar = karar or C2_KARAR
    v22 = ufuk is not None
    if v22:
        ufuk = int(ufuk)
        if ufuk not in C2_ESIK22["ufuklar"]:
            raise C2Hata(f"ufuk {ufuk} tanımsız (v2.2: {C2_ESIK22['ufuklar']})")
        Dn22 = dict(donem or C2_ESIK22["donem"]); hucreler = list(Dn22)
        tekil_gun = int(tekil_gun or ufuk)
    else:
        Dn22, hucreler = None, C2_HUCRE
    for c in ("pazar", "sembol", "tarih"):
        if c not in olaylar.columns:
            raise C2Hata(f"olay listesinde '{c}' sütunu yok")
    for k, h in hipotez.items():
        if h.get("yon") not in ("+", "-", "?"):
            raise C2Hata(f"{k}: yön '+' / '-' / '?' olmalı")
        if h.get("bayrak") is not None and h["bayrak"] not in olaylar.columns:
            raise C2Hata(f"{k}: bayrak sütunu {h['bayrak']} yok")
    satirlar, hucre, say = [], [], {}
    for pi, pazar in enumerate(sorted(olaylar.pazar.astype(str).unique())):
        Pn = c2_panel22_al(pazar, veri, ufuk) if v22 else c2_panel_al(pazar, veri)
        X, sy = c2_olay(olaylar[olaylar.pazar.astype(str) == pazar].drop(columns=["pazar"]), Pn, tekil_gun)
        if v22:
            X["donem"] = _c2_donem22(X.giris, Dn22); X["ufuk"] = ufuk
            sy["donem"] = {k: int(v) for k, v in pd.Series(X.donem).value_counts().items()}
        say[pazar] = sy
        if bilgi:
            X = pd.concat([X, c2_bilgi(Pn, X)], axis=1)
        d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64); x = X.r15.to_numpy(float); idx = Pn["P"]["tarih"]
        for ki, (kod, h) in enumerate(hipotez.items()):
            F = np.ones(len(X)) if h.get("bayrak") is None else pd.to_numeric(X[h["bayrak"]], errors="coerce").to_numpy(float)
            m = F == 1
            e = c2_es(Pn, d[m], j[m], x[m], d[m], j[m])
            for c_ in ("es_r15", "n_es", "sira", "fark"):
                v = np.full(len(X), np.nan); v[m] = e[c_]; X[f"{c_}_{kod}"] = v
            for hi, hc in enumerate(hucreler):
                mm = m & (X.donem.to_numpy() == hc)
                tek = (int(tohum0) * 100000 + ki * 1000 + pi * 100 + hi) if v22 else (int(tohum0) * 1000 + ki * 20 + pi * 4 + hi)
                egri = _c2_egri22_al(pazar, hc, ufuk, guc) if v22 else _c2_egri_al(pazar, hc, guc)
                c = c2_hucre(x[mm], X[f"es_r15_{kod}"].to_numpy(float)[mm], X[f"sira_{kod}"].to_numpy(float)[mm], X.giris.to_numpy()[mm],
                             h["yon"], tohum_ek=tek, egri=egri)
                ol = mm & np.isfinite(X[f"fark_{kod}"].to_numpy(float))
                r = {"kod": kod, "yon": h["yon"], "pazar": pazar, "hucre": hc, **({"ufuk": ufuk} if v22 else {}), "n_bayrak": int(mm.sum()),
                     "n_r15": int((mm & np.isfinite(x)).sum()), "n_essiz": int((mm & np.isfinite(x) & ~ol).sum()),
                     **{k_: v_ for k_, v_ in c.items()}}
                if bilgi:
                    for b_ in ("h5", "st5", "h5_atr", "st5_atr"):
                        r[b_] = float(np.nanmean(X[b_].to_numpy(float)[ol])) if ol.any() else np.nan
                    rf = (X.r60 - X.esli_r60).to_numpy(float)[ol]
                    r["r60_fark"] = float(np.nanmean(rf)) if np.isfinite(rf).any() else np.nan
                if plasebo and c["n"] > 0:
                    pl = c2_plasebo(Pn, d[ol], h["yon"], egri, tohum_ek=tek, iki_yon_ayri=v22)
                    r.update({"plasebo_fark": pl["fark_ort"], "plasebo_tutar_pay": pl["tutar_pay"], "plasebo_gecti": pl["gecti"]})
                else:
                    r.update({"plasebo_fark": np.nan, "plasebo_tutar_pay": np.nan, "plasebo_gecti": False})
                r["durum"] = ("BİLGİ (pazar)" if pazar not in karar else ("KARAR" if r["plasebo_gecti"] else "BİLGİ (plasebo kapısı)"))
                hucre.append(r)
        satirlar.append(X)
    S = pd.concat(satirlar, ignore_index=True) if satirlar else pd.DataFrame()
    Hc = pd.DataFrame(hucre)
    et = []
    for kod, h in hipotez.items():
        hh: Dict[str, Dict[str, Dict[str, Any]]] = {}
        for r in hucre:
            if r["kod"] == kod:
                hh.setdefault(r["pazar"], {})[r["hucre"]] = r
        e = c2_etiket(hh, h["yon"], karar, hucreler if v22 else None)
        ps = []
        for p in karar:
            for hc in (hucreler if v22 else ["sinama"]):       # v2.2: p = en büyük p (karar pazarları x bütün hücreler)
                c = hh.get(p, {}).get(hc)
                ps.append(1.0 if (c is None or c["n"] < C2_ESIK["hucre"]["n_min"] or not np.isfinite(c.get("p", np.nan))) else float(c["p"]))
        et.append({"kod": kod, "yon": h["yon"], **({"ufuk": ufuk} if v22 else {}), "etiket_ham": e["etiket"], "neden": e["neden"],
                   "p_bh": max(ps) if ps else 1.0})
    Et = pd.DataFrame(et)
    if len(Et):
        m = int(m_bh or len(Et))
        p = list(Et.p_bh.to_numpy(float)) + [1.0] * max(0, m - len(Et))
        Et["bh_gecti"] = c2_bh(p)[:len(Et)]
        Et["etiket"] = [e if (not e.startswith("KATKI") or b) else "SORGULA (BH)" for e, b in zip(Et.etiket_ham, Et.bh_gecti)]
        Et["m_bh"] = m
    c2log.info("c2_olc: %d olay satırı, %d hücre, %d hipotez (%.0f sn)", len(S), len(Hc), len(Et), time.time() - t0)
    return {"satir": S, "hucre": Hc, "etiket": Et, "say": say}


def c2_rapor_tablo(R: Dict[str, Any], baslik: str = "CETVEL2 ölçümü") -> str:
    """c2_olc çıktısından kısa markdown (hücre tablosu + etiket)."""
    s = [f"## {baslik}", "", "| kod | yön | pazar | hücre | n | eşsiz | FARK [boot %95] | medyan | SIRA | L3O | p | güç | plasebo FARK / tutar payı | "
         "kapı | TUTAR | durum | h5 | r60 fark |", "|" + "---|" * 18]
    for r in R["hucre"].to_dict("records"):
        s.append(f"| {r['kod']} | {r['yon']} | {r['pazar']} | {r['hucre']} | {r['n']} | {r.get('n_essiz', 0)} | {_c2_y(r['fark'], 2)} "
                 f"[{_c2_y(r['boot_alt'], 2)}, {_c2_y(r['boot_ust'], 2)}] | {_c2_y(r['med'], 2)} | {_c2_s(r['sira'])} | "
                 f"{_c2_y(r['l3o'] if r['yon'] != '-' else r['l3o_neg'], 2)} | {_c2_s(r['p'], 4)} | {_c2_s(r['guc'], 2)} | "
                 f"{_c2_y(r.get('plasebo_fark'), 2)} / {_c2_y(r.get('plasebo_tutar_pay'), 0, False)} | {'geçti' if r.get('plasebo_gecti') else 'DÜŞTÜ'} | "
                 f"{'TUTAR' if r['tutar'] else ('ters' if r['ters'] else '-')} | {r['durum']} | {_c2_y(r.get('h5'), 1, False)} | "
                 f"{_c2_y(r.get('r60_fark'), 2)} |")
    s += ["", "| kod | yön | etiket (ham) | gerekçe | p (BH) | BH | etiket |", "|---|---|---|---|---|---|---|"]
    for r in R["etiket"].to_dict("records"):
        s.append(f"| {r['kod']} | {r['yon']} | {r['etiket_ham']} | {r['neden']} | {_c2_s(r['p_bh'], 4)} | {'geçti' if r['bh_gecti'] else '-'} | "
                 f"{r['etiket']} |")
    return "\n".join(s) + "\n"


def _c2_y(x: Any, n: int = 1, isaret: bool = True) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    return (f"{100 * v:+.{n}f}" if isaret else f"{100 * v:.{n}f}").replace(".", ",")


def _c2_s(x: Any, n: int = 3) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    return "-" if not np.isfinite(v) else f"{v:.{n}f}".replace(".", ",")


# ================================================================ 7) PREFIX (K2)
def c2_prefix(Pn: Dict[str, Any], X: pd.DataFrame, n: int = 30, tohum: int = 2151) -> Dict[str, Any]:
    """Rastgele n olayda veri t'de kesilince ATRP_t / F15_t / hat_t / ATR_t panel değerine eşit mi (rtol 1e-9)."""
    Vd = Pn["Vd"]; A = X[(X.kova >= 0)].reset_index(drop=True); k = int(C2_ESIK["kova"]["f15_gun"])
    rng = np.random.default_rng([int(tohum), C2_PAZAR.index(Pn["pazar"])])
    sec = rng.choice(len(A), size=min(n, len(A)), replace=False) if len(A) else []
    sonuc, bozuk = [], 0
    for i in sec:
        r = A.iloc[int(i)]; s = r.sembol; df = Vd["V"][s]
        dk = df[df.index < pd.Timestamp(r.giris)]          # giriş gününden önceki son geçerli bar = bilgi anı
        atrp, hat = PK.pk_seri(dk)
        c = dk.Close.astype(float); lo = c.iloc[-k:].min(); hi = c.iloc[-k:].max()
        f15 = float((c.iloc[-1] - lo) / (hi - lo)) if len(c) >= k and hi > lo else np.nan
        yeni = {"atrp": float(atrp.iloc[-1]), "hat": float(hat.iloc[-1]), "f15": f15, "atr": float(atrp.iloc[-1] * c.iloc[-1])}
        fark = [kk for kk, v in yeni.items() if not np.isclose(v, float(r[kk]), rtol=1e-9, atol=1e-12, equal_nan=True)]
        bozuk += bool(fark); sonuc.append({"sembol": s, "tarih": str(pd.Timestamp(r.tarih).date()), "tut": not fark, "fark": fark})
    return {"pazar": Pn["pazar"], "n": len(sonuc), "bozuk": bozuk, "olay": sonuc}


# ================================================================ 8) POZİTİF KONTROL v2: A (yapay iz)
_C2_A: Dict[str, Any] = {}


def c2_ds_olay(pazar: str, yol: Optional[str] = None) -> pd.DataFrame:
    """DS ANA olayları (ds_olay.csv.gz: DUSUS_SONRASI koşusunun ölçülen ANA kümesi)."""
    yol = yol or C2_YOL["ds_olay"]
    if not os.path.exists(yol):
        raise C2Hata(f"DS olay dosyası yok: {yol}")
    X = pd.read_csv(yol, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"])
    return X[X.pazar == pazar][["sembol", "tarih"]].reset_index(drop=True)


def c2_a_hazirla(pazar: str, veri: Optional[str] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    Pn = c2_panel_al(pazar, veri)
    X, say = c2_olay(c2_ds_olay(pazar, ds_yol), Pn)
    e = c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float))
    X["fark0"] = e["fark"]; X["n_es0"] = e["n_es"]
    return {"Pn": Pn, "X": X, "say": say}


def _c2_a_isci(is_: Tuple[str, int, Any]) -> List[Dict[str, Any]]:
    pazar, ti, nk = is_
    G = _C2_A[pazar]; Pn, X = G["Pn"], G["X"]; Ea = C2_ESIK["A"]; idx = Pn["P"]["tarih"]; out = []
    guc = G.get("guc")
    for hi, h in enumerate(C2_HUCRE):
        havuz = np.flatnonzero((X.donem.to_numpy() == h) & np.isfinite(X.fark0.to_numpy(float)))
        n = len(havuz) // 2 if nk == "yari" else int(nk)
        if n < 1 or n > Ea["n_azami_pay"] * len(havuz):
            out.append({"pazar": pazar, "tohum": ti, "n_hedef": str(nk), "hucre": h, "taban": "-", "delta": np.nan, "n": 0}); continue
        rng = np.random.default_rng([int(Ea["tohum"]), int(ti), Ea["n"].index(nk), C2_PAZAR.index(pazar), hi])
        sec = np.sort(rng.choice(havuz, size=n, replace=False))
        d0 = X.d.to_numpy(np.int64)[sec]; j0 = X.j.to_numpy(np.int64)[sec]; r0 = X.r15.to_numpy(float)[sec]
        rd, rj = c2_rastgele(Pn, d0, rng); rr = Pn["R15"][rd, rj]
        egri = (guc or {}).get("egri", {}).get(pazar, {}).get(h)
        for tb, (dd, jj, rv) in (("DS", (d0, j0, r0)), ("RAST", (rd, rj, rr))):
            for di, de in enumerate(Ea["delta"]):
                x = (1.0 + rv) * (1.0 + float(de)) - 1.0
                e = c2_es(Pn, dd, jj, x, dd, jj)
                tek = 300000 + ti * 1000 + Ea["n"].index(nk) * 100 + hi * 50 + (0 if tb == "DS" else 25) + di
                c = c2_hucre(x, e["es_r15"], e["sira"], idx[dd], "+", tohum_ek=tek, egri=egri, l3o_neg=False)
                out.append({"pazar": pazar, "tohum": ti, "n_hedef": str(nk), "hucre": h, "taban": tb, "delta": float(de), "n": c["n"],
                            "fark": c["fark"], "med": c["med"], "sira": c["sira"], "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"],
                            "l3o": c["l3o"], "p": c["p"], "guc": c["guc"], "yakala": bool(c["yakala_p"]), "tutar": bool(c["tutar_p"]),
                            "yakala_p05": bool(c["yakala_p"] and np.isfinite(c["p"]) and c["p"] < 0.05)})
    return out


def c2_a_kos(islem: int = 1, veri: Optional[str] = None, guc: Optional[Dict[str, Any]] = None, tohum_sayi: Optional[int] = None,
             pazarlar: Optional[List[str]] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    global _C2_A
    Ea = C2_ESIK["A"]; pazarlar = pazarlar or Ea["pazar"]; T = int(tohum_sayi or Ea["tohum_sayi"]); say = {}
    for p in pazarlar:
        _C2_A[p] = c2_a_hazirla(p, veri, ds_yol); _C2_A[p]["guc"] = guc
        X = _C2_A[p]["X"]
        say[p] = {**_C2_A[p]["say"], "havuz": {h: int(((X.donem == h) & np.isfinite(X.fark0)).sum()) for h in C2_HUCRE},
                  "essiz": {h: int(((X.donem == h) & np.isfinite(X.r15) & ~np.isfinite(X.fark0)).sum()) for h in C2_HUCRE},
                  "n_es_medyan": {h: float(np.nanmedian(X.n_es0[(X.donem == h) & np.isfinite(X.r15)])) if ((X.donem == h) & np.isfinite(X.r15)).any()
                                  else np.nan for h in C2_HUCRE}}
    isler = [(p, ti, nk) for p in pazarlar for ti in range(T) for nk in Ea["n"]]
    t0 = time.time()
    if islem > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as hv:
            R = hv.map(_c2_a_isci, isler, chunksize=1)
    else:
        R = [_c2_a_isci(x) for x in isler]
    S = pd.DataFrame([r for x in R for r in x])
    c2log.info("A ızgara: %d satır (%.0f sn)", len(S), time.time() - t0)
    return {"satir": S, "say": say}


def c2_a_ozet(S: pd.DataFrame) -> Dict[str, Any]:
    g = S[S.n > 0].copy()
    tab = g.groupby(["pazar", "hucre", "taban", "n_hedef", "delta"]).agg(
        yakala=("yakala", "mean"), tutar=("tutar", "mean"), yakala_p05=("yakala_p05", "mean"), n=("n", "mean"), fark=("fark", "mean"),
        fark_sd=("fark", "std"), guc=("guc", "mean"), tohum=("tohum", "count")).reset_index()
    dort = []
    for (tb, nk, de), x in g[g.pazar.isin(C2_ESIK["A"]["karar_pazar"])].groupby(["taban", "n_hedef", "delta"]):
        k = x.groupby("tohum").agg(hep=("yakala", "all"), say=("yakala", "size"))
        k = k[k.say == 4]
        dort.append({"taban": tb, "n_hedef": nk, "delta": de, "dort_hucre": float(k.hep.mean()) if len(k) else np.nan, "tohum": int(len(k))})
    return {"tablo": tab.to_dict("records"), "dort": dort}


# ================================================================ 9) POZİTİF KONTROL v2: B (momentum, PEAD) ve C (plasebo kapısı)
def c2_b_kos(veri: Optional[str] = None, pk_b: Optional[str] = None, pk_json: Optional[str] = None,
             guc: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """POZITIF_KONTROL B olay kümeleri (aynı ANA olaylar) CETVEL2 ile; h5 FARK (PK json) yan yana."""
    yol = pk_b or C2_YOL["pk_b"]
    if not os.path.exists(yol):
        raise C2Hata(f"PK B satır dosyası yok: {yol}")
    B = pd.read_csv(yol, usecols=["kod", "pazar", "sembol", "tarih", "giris", "donem", "U", "A"], parse_dates=["tarih", "giris"])
    Eb = C2_ESIK["B"]; out: Dict[str, Any] = {"hucre": [], "etiket": [], "say": {}, "satir": []}
    for ad in ("B1", "B2"):
        for pazar in Eb["pazar"][ad]:
            g = B[(B.kod == ad) & (B.pazar == pazar)].copy()
            if not len(g):
                continue
            g["F_U"] = g.U.astype(bool).astype(float); g["F_A"] = g.A.astype(bool).astype(float)
            hip = {f"{ad}U": {"bayrak": "F_U", "yon": "+"}, f"{ad}A": {"bayrak": "F_A", "yon": "-"}}
            R = c2_olc(g.assign(pazar=pazar)[["pazar", "sembol", "tarih", "F_U", "F_A", "giris"]].rename(columns={"giris": "pk_giris"}), hip,
                       veri=veri, m_bh=2, tohum0=10 + (ad == "B2") * 5 + C2_PAZAR.index(pazar), guc=guc,
                       karar=Eb["karar_pazar"] if pazar in Eb["karar_pazar"] else [pazar])
            S = R["satir"]
            uy = int((pd.to_datetime(S.pk_giris) == pd.to_datetime(S.giris)).sum())
            out["say"][f"{ad}_{pazar}"] = {**R["say"][pazar], "girdi_pk": int(len(g)), "giris_ayni": uy}
            h = R["hucre"].assign(bilgi=pazar in Eb["bilgi_pazar"]); out["hucre"].append(h)
            out["etiket"].append(R["etiket"].assign(pazar=pazar))
            S = S.assign(kod=ad); out["satir"].append(S)
    out["hucre"] = pd.concat(out["hucre"], ignore_index=True); out["etiket"] = pd.concat(out["etiket"], ignore_index=True)
    out["satir"] = pd.concat(out["satir"], ignore_index=True)
    pj = pk_json or C2_YOL["pk_json"]
    if os.path.exists(pj):
        J = json.load(open(pj, encoding="utf-8")); pkb = {(r["kod"], r["pazar"], r["hucre"]): r for r in J["B"]["sonuc"]}
        for c in ("h5_fark_pk", "h5_alt_pk", "h5_ust_pk", "h5_p_pk", "r15_fark_pk", "r15_alt_pk", "r15_ust_pk", "n_pk"):
            out["hucre"][c] = np.nan
        for i, r in out["hucre"].iterrows():
            q = pkb.get((r["kod"], r["pazar"], r["hucre"]))
            if q:
                out["hucre"].loc[i, ["h5_fark_pk", "h5_alt_pk", "h5_ust_pk", "h5_p_pk", "n_pk"]] = [q["h5"].get("fark"), q["h5"].get("boot_alt"),
                                                                                                   q["h5"].get("boot_ust"), q["h5"].get("p"),
                                                                                                   q["h5"].get("n")]
                out["hucre"].loc[i, ["r15_fark_pk", "r15_alt_pk", "r15_ust_pk"]] = [q["r15"].get("fark"), q["r15"].get("boot_alt"), q["r15"].get("boot_ust")]
    return out


def c2_c_kos(veri: Optional[str] = None, guc: Optional[Dict[str, Any]] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    """Plasebo kapısı: her pazar x dönem DS ANA olay günleriyle (tam n, n 100 / 300 alt küme) + tanı (havuz, eş sayısı, eşsiz, dolu kova)."""
    Ec = C2_ESIK["C"]; sat, tani = [], []
    for pi, pazar in enumerate(C2_PAZAR):
        G = _C2_A.get(pazar) or c2_a_hazirla(pazar, veri, ds_yol)
        Pn, X = G["Pn"], G["X"]; P = Pn["P"]; idx = P["tarih"]
        for hi, h in enumerate(C2_HUCRE):
            m = (X.donem.to_numpy() == h) & np.isfinite(X.fark0.to_numpy(float))
            d_all = X.d.to_numpy(np.int64)[m]
            egri = (guc or {}).get("egri", {}).get(pazar, {}).get(h)
            for ni, nk in enumerate(Ec["n"]):
                if nk == "tam":
                    dsec = d_all
                else:
                    if int(nk) > len(d_all):
                        continue
                    rng = np.random.default_rng([int(Ec["tohum"]), pi, hi, ni]); dsec = np.sort(rng.choice(d_all, size=int(nk), replace=False))
                pl = c2_plasebo(Pn, dsec, "+", egri, tohum_ek=700000 + pi * 100 + hi * 10 + ni)
                sat.append({"pazar": pazar, "hucre": h, "n_hedef": str(nk), "n": pl["n_ort"], "fark_ort": pl["fark_ort"], "fark_sd": pl["fark_sd"],
                            "tutar_pay_arti": pl["tutar_pay_arti"], "tutar_pay_eksi": pl["tutar_pay_eksi"], "yakala_pay_arti": pl["yakala_pay"],
                            "gecti_arti": pl["gecti_arti"], "gecti_eksi": pl["gecti_eksi"],
                            "gecti": bool(pl["gecti_arti"] and pl["gecti_eksi"]), "karar": pazar in C2_KARAR})
            # tanı
            gm = (pd.Series(_c2_donem(idx)) == h).to_numpy()
            hv = (P["ok"] & (P["H"] >= 0))[gm].sum(1); rv = ((Pn["KV"] >= 0) & np.isfinite(Pn["R15"]))[gm].sum(1)
            dolu = np.array([len(np.unique(Pn["KV"][dd][(Pn["KV"][dd] >= 0) & np.isfinite(Pn["R15"][dd])])) for dd in np.flatnonzero(gm)])
            mr = (X.donem.to_numpy() == h) & np.isfinite(X.r15.to_numpy(float))
            tani.append({"pazar": pazar, "hucre": h, "gun": int(gm.sum()), "havuz_gun_medyan": float(np.median(hv)) if len(hv) else np.nan,
                         "r15_kova_gun_medyan": float(np.median(rv)) if len(rv) else np.nan,
                         "dolu_kova_medyan": float(np.median(dolu)) if len(dolu) else np.nan,
                         "olay_r15": int(mr.sum()), "essiz_pay": float((~np.isfinite(X.fark0.to_numpy(float)[mr])).mean()) if mr.any() else np.nan,
                         "n_es_medyan": float(np.nanmedian(X.n_es0.to_numpy(float)[mr])) if mr.any() else np.nan,
                         "n_es_p10": float(np.nanquantile(X.n_es0.to_numpy(float)[mr], 0.10)) if mr.any() else np.nan,
                         "olay_gun_sayi": int(len(np.unique(X.d.to_numpy()[mr]))),
                         "fark0_ort": float(np.nanmean(X.fark0.to_numpy(float)[mr])) if mr.any() else np.nan,
                         "r15_ort_havuz": float(np.nanmean(np.where((Pn["KV"] >= 0), Pn["R15"], np.nan)[gm])) if gm.any() else np.nan})
    return {"satir": pd.DataFrame(sat), "tani": pd.DataFrame(tani)}


# ================================================================ 10) YENİDEN ÜRETİM (K11)
def c2_yeniden(B: Dict[str, Any], veri: Optional[str] = None) -> Dict[str, Any]:
    """(1) B1U ABD sınama ve B1A ABD eğitim hücre ort FARK / SIRA satır dosyasından düz pandas; (2) 50 olayın R15'i ham veriden düz döngü;
    (3) 5 olayın eş ortalaması bütün evrende düz döngüyle (kova elle: ATRP / F15 ham seriden, likidite panel H % 3)."""
    Y = C2_ESIK["yeniden_uretim"]; out: Dict[str, Any] = {"hucre": [], "r15_bozuk": [], "es_bozuk": []}
    S = B["satir"]; Hc = B["hucre"]
    for kod, hc in (("B1U", "sinama"), ("B1A", "egitim")):
        g = S[(S.kod == kod[:2]) & (S.pazar == "ABD") & (S.donem == hc)]
        f = g[f"fark_{kod}"].dropna(); sr = g.loc[f.index, f"sira_{kod}"]
        q = Hc[(Hc.kod == kod) & (Hc.pazar == "ABD") & (Hc.hucre == hc)].iloc[0]
        out["hucre"].append({"kod": kod, "hucre": hc, "n_duz": int(len(f)), "fark_duz": float(f.mean()), "sira_duz": float(sr.mean()),
                             "n": int(q["n"]), "fark": float(q["fark"]), "sira": float(q["sira"]),
                             "esit": bool(len(f) == int(q["n"]) and abs(f.mean() - q["fark"]) < 1e-12 and abs(sr.mean() - q["sira"]) < 1e-12)})
    Pn = c2_panel_al("ABD", veri); V = Pn["Vd"]["V"]; P = Pn["P"]; idx = P["tarih"]
    g = S[(S.kod == "B1") & (S.pazar == "ABD") & np.isfinite(S.r15)].reset_index(drop=True)
    rng = np.random.default_rng(int(Y["tohum"]))
    for i in rng.choice(len(g), size=min(int(Y["elle_r15"]), len(g)), replace=False):
        r = g.iloc[int(i)]; df = V[r.sembol]; ix = list(df.index); k = ix.index(pd.Timestamp(r.giris))
        if k + 14 < len(ix) and idx.get_loc(ix[k + 14]) - idx.get_loc(ix[k]) <= 29:
            v = df.Close.iloc[k + 14] / df.Open.iloc[k] - 1
        else:
            v = float("nan")
        if not np.isclose(v, r.r15, rtol=1e-10, atol=1e-12, equal_nan=True):
            out["r15_bozuk"].append({"sembol": r.sembol, "giris": str(r.giris), "duz": v, "kod": r.r15})
    sn = P["sembol"]; sin = Pn["sinir"]; kf = int(C2_ESIK["kova"]["f15_gun"])
    gU = g[np.isfinite(g["fark_B1U"])].reset_index(drop=True)
    for i in rng.choice(len(gU), size=min(int(Y["elle_es"]), len(gU)), replace=False):
        r = gU.iloc[int(i)]; gd = pd.Timestamp(r.giris); dd = idx.get_loc(gU.loc[int(i), "giris"])
        ayni_gun_U = set(S[(S.kod == "B1") & (S.pazar == "ABD") & (pd.to_datetime(S.giris) == gd) & (S.F_U == 1)].sembol)

        def kova_elle(s):
            df = V[s]
            if gd not in df.index:
                return -1, np.nan
            jj = P["kol"][s]
            if not (P["ok"][dd, jj] and P["H"][dd, jj] >= 0):
                return -1, np.nan
            once = df[df.index < gd]
            if len(once) < 15:
                return -1, np.nan
            H_, L_, C_ = once.High.to_numpy(float), once.Low.to_numpy(float), once.Close.to_numpy(float)
            tr = [H_[0] - L_[0]] + [max(H_[t], C_[t - 1]) - min(L_[t], C_[t - 1]) for t in range(1, len(C_))]
            atrp = float(np.mean(tr[-14:]) / C_[-1])
            if len(C_) < kf:
                return -1, np.nan
            w = C_[-kf:]; f15 = (C_[-1] - w.min()) / (w.max() - w.min()) if w.max() > w.min() else np.nan
            if not np.isfinite(f15):
                return -1, np.nan
            at = 0 if atrp <= sin["ATRP"][0] else (1 if atrp <= sin["ATRP"][1] else 2)
            fq = 0 if f15 <= sin["F15"][0] else (1 if f15 <= sin["F15"][1] else (2 if f15 <= sin["F15"][2] else 3))
            k_ = list(df.index).index(gd); ix = list(df.index)
            if k_ + 14 >= len(ix) or idx.get_loc(ix[k_ + 14]) - idx.get_loc(ix[k_]) > 29:
                return -1, np.nan
            return at * 12 + int(P["H"][dd, jj] % 3) * 4 + fq, float(df.Close.iloc[k_ + 14] / df.Open.iloc[k_] - 1)
        k0, _ = kova_elle(r.sembol); vals = []
        for s in sn:
            if s == r.sembol or s in ayni_gun_U:
                continue
            k1, v1 = kova_elle(s)
            if k1 == k0 and k1 >= 0 and np.isfinite(v1):
                vals.append(v1)
        es = float(np.mean(vals)) if len(vals) >= C2_ESIK["es_min"] else float("nan")
        if not (k0 == int(r.kova) and np.isclose(es, r["es_r15_B1U"], rtol=1e-6, atol=1e-10, equal_nan=True) and len(vals) == int(r["n_es_B1U"])):
            out["es_bozuk"].append({"sembol": r.sembol, "giris": str(r.giris), "kova_elle": k0, "kova": int(r.kova), "es_duz": es,
                                    "es_kod": float(r["es_r15_B1U"]), "n_duz": len(vals), "n_kod": int(r["n_es_B1U"])})
    out["tuttu"] = bool(all(h["esit"] for h in out["hucre"]) and not out["r15_bozuk"] and not out["es_bozuk"])
    return out


# ================================================================ 11) ÖN KAYIT, KAPI, KOŞU
def c2_sha_simdi(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, str]:
    v = veri or C2_YOL["veri"]; c = cikti or C2_YOL["cikti"]
    out = {"C2_ESIK_SHA": c2_esik_sha(), "C2_KOD_SHA": _c2_sha(C2_YOL["kod"]), "PK_KOD_SHA": _c2_sha(C2_YOL["pk_kod"])}
    ds = DS.ds_sha_simdi(veri=v)
    for k in ("DS_KOD_SHA", "YH_KOD_SHA", "OC_KOD_SHA", "DS_ESIK_SHA", "YH_ESIK_SHA", "OC_ESIK_SHA", "V_ABD_SHA", "V_AVR_SHA", "V_BIST_SHA"):
        out[k] = ds[k]
    for k, y in (("DS_OLAY_SHA", C2_YOL["ds_olay"]), ("PK_B_OLAY_SHA", C2_YOL["pk_b"]), ("PK_JSON_SHA", C2_YOL["pk_json"]),
                 ("C2_ESIK_JSON_SHA", _c2_yol("esik", c)), ("C2_GUC_JSON_SHA", _c2_yol("guc", c)), ("C2_PREFIX_SHA", _c2_yol("prefix", c))):
        out[k] = _c2_sha(y) if os.path.exists(y) else "-"
    return out


def c2_hazirlik(veri: Optional[str] = None, cikti: Optional[str] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt girdileri (getirisiz ya da yalnız yayılım): kova sınırları (eğitim havuzu), güç eğrisi (DS ANA FARK sigma), prefix."""
    c = cikti or C2_YOL["cikti"]; sinir, egri, pre = {}, {}, {}
    for pi, p in enumerate(C2_PAZAR):
        Pn = c2_panel(c2_veri(p, veri)); _C2_PN[p] = Pn; sinir[p] = Pn["sinir"]
        X, say = c2_olay(c2_ds_olay(p, ds_yol), Pn)
        e = c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float))
        egri[p] = {}
        for hi, h in enumerate(C2_HUCRE):
            egri[p][h] = c2_guc_egri(e["fark"][X.donem.to_numpy() == h], tohum_ek=pi * 10 + hi)
            egri[p][h]["n_olay_r15"] = int(((X.donem == h) & np.isfinite(X.r15)).sum())
        pr = c2_prefix(Pn, X)
        if pr["bozuk"]:
            raise C2Hata(f"{p}: prefix TUTMADI ({pr['bozuk']} / {pr['n']}): {[o for o in pr['olay'] if not o['tut']][:3]}")
        pre[p] = pr
    os.makedirs(c, exist_ok=True)
    YH._yh_yaz(_c2_yol("esik", c), json.dumps({"surum": C2_SURUM, "sinir": sinir}, ensure_ascii=False, indent=1, default=YH._yh_json), "C2 eşik")
    YH._yh_yaz(_c2_yol("guc", c), json.dumps({"surum": C2_SURUM, "delta": C2_ESIK["guc"]["delta"], "egri": egri}, ensure_ascii=False, indent=1,
                                             default=YH._yh_json), "C2 güç")
    YH._yh_yaz(_c2_yol("prefix", c), json.dumps(pre, ensure_ascii=False, indent=1, default=YH._yh_json), "C2 prefix")
    return {"sinir": sinir, "egri": egri, "prefix": pre}


def c2_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False, ds_yol: Optional[str] = None,
                   onceki: Optional[str] = None, duzeltme: Optional[str] = None) -> str:
    c = cikti or C2_YOL["cikti"]; yol = _c2_yol("onkayit", c)
    if os.path.exists(yol) and not uzerine:
        raise C2Hata(f"ön kayıt zaten var: {yol}")
    Hz = c2_hazirlik(veri, c, ds_yol); sha = c2_sha_simdi(veri, c)
    s = [f"# CETVEL2 — ÖN KAYIT{(' ' + C2_ETIKET_SURUM.strip('_')) if C2_ETIKET_SURUM else ''} ({_c2_simdi()})", "",
         C2_SURUM + ". Bu dosya pozitif kontrol koşusundan ÖNCE yazıldı ve git'e işlendi; c2_kapi C2_ESIK / kod / girdi sha'larını, git kaydını ve "
         "IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Kova sınırları getirisiz havuz dağılımından, güç eğrisi yalnız "
         "FARK yayılımından (ortalama kullanılmaz) hesaplandı; hiçbir hücre FARK'ı / p'si bu dosya yazılırken hesaplanmadı.", ""]
    if onceki:
        s += [f"ÖNCEKİ SÜRÜM: {onceki} (silinmedi). DÜZELTME: {duzeltme or '-'}", ""]
    s += [f"- {k}: `{v}`" for k, v in sha.items()]
    s += ["", "## 1. CETVEL2 TANIMI (iş tanımı bölüm 2, AYNEN; ana model ön kaydı, commit ca5d2a8)", ""]
    try:
        it = open(os.path.join(KOK_C2, "arastirma_cikti", "cetvel2", "CETVEL2_IS_TANIMI.md"), encoding="utf-8").read()
        m = re.search(r"## 2\. CETVEL2 TANIMI.*?\n(.*?)\n## 3\.", it, flags=re.S)
        s += [m.group(1).strip() if m else "(iş tanımı bölüm 2 bulunamadı)"]
    except OSError as ex:
        raise C2Hata(f"iş tanımı okunamadı: {ex}") from ex
    s += ["", "## 2. UYGULAMA AYRINTILARI (C2_ESIK; sha yukarıda)", ""]

    def dz(d, on=""):
        for k, v in d.items():
            if isinstance(v, dict):
                s.append(f"- {on}{k}:"); dz(v, on + "  ")
            else:
                s.append(f"- {on}{k}: {v}")
    dz(C2_ESIK)
    s += ["", "## 3. EĞİTİM DÖNEMİNDE SABİTLENEN KOVA SINIRLARI (sayı; cetvel2_esik.json)", "",
          "| pazar | ATRP t1 | ATRP t2 | F15 q1 | F15 q2 | F15 q3 | eğitim havuz hisse-gün | likidite |", "|---|---|---|---|---|---|---|---|"]
    for p, v in Hz["sinir"].items():
        s.append(f"| {p} | {v['ATRP'][0]:.6f} | {v['ATRP'][1]:.6f} | {v['F15'][0]:.6f} | {v['F15'][1]:.6f} | {v['F15'][2]:.6f} | {v['n_hisse_gun']} | "
                 f"{v['lq_tanim']} |")
    s += ["", "## 4. GÜÇ EĞRİSİ (cetvel2_guc.json; delta +0,02 R15; sigma(n) = exp(a + b ln n); güç = Phi(delta / sigma - 1,96))", "",
          "| pazar | dönem | N (DS ANA, eşli) | sd (olay) | a | b | n = 30 | 100 | 300 | 1000 | 3000 | güç >= 0,80 için en küçük n |", "|" + "---|" * 12]
    for p, hh in Hz["egri"].items():
        for h, e in hh.items():
            gg = [c2_guc(n, e) for n in (30, 100, 300, 1000, 3000)]
            nmin = next((n for n in range(30, 200001, 10) if c2_guc(n, e) >= 0.80), None)
            s.append(f"| {p} | {h} | {e['N']} | {_c2_s(e['sd'], 4)} | {_c2_s(e['a'], 4)} | {_c2_s(e['b'], 4)} | " + " | ".join(_c2_s(x, 2) for x in gg)
                     + f" | {nmin if nmin else '> 200000'} |")
    s += ["", "## 5. PREFIX (K2; cetvel2_prefix.json)", ""]
    for p, v in Hz["prefix"].items():
        s.append(f"- {p}: {v['n']} olay, bozuk {v['bozuk']}")
    s += ["", "## 6. PLASEBO KAPISI EŞİKLERİ", "", f"- |ortalama FARK| < {C2_ESIK['plasebo']['fark_mutlak']} (0,5 puan) VE TUTAR payı <= "
          f"{C2_ESIK['plasebo']['tutar_pay']} ({C2_ESIK['plasebo']['tohum_sayi']} tohum); geçmeyen hücre KARAR VERMEZ.",
          "", "## 7. ÖNCEDEN YAZILI SONUÇ KURALI (pozitif kontrol v2)", ""]
    s += [f"- {k}: {v}" for k, v in C2_ESIK["sonuc_kurali"].items()]
    s += ["", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "",
          "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    try:
        import IZ_KARNE as IK
        ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    except Exception:   # IZ_KARNE yoksa madde adı yazılmaz; kapı yine kodları okur
        ad = {}
    for k, (y, kn) in C2_KONTROL.items():
        s.append(f"| {k} | {ad.get(k, k)} | {y} | {kn} |")
    metin = "\n".join(s) + "\n"
    YH._yh_yaz(yol, metin, "C2 ön kayıt")
    return yol


def c2_kapi(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    c = cikti or C2_YOL["cikti"]; yol = _c2_yol("onkayit", c)
    if not os.path.exists(yol):
        raise C2Hata(f"ön kayıt yok: {yol} (python CETVEL2.py onkayit)")
    metin = open(yol, encoding="utf-8").read(); simdi = c2_sha_simdi(veri, c)
    for k, v in simdi.items():
        m = re.search(rf"(?<![A-Z0-9_]){k}:\s*`([0-9a-f]{{64}}|-)`", metin)
        if not m or m.group(1) != v:
            raise C2Hata(f"{k} ön kayıttakiyle aynı değil -> koşu DURDU")
    out: Dict[str, Any] = {"sha": simdi}
    if git:
        try:
            dosyalar = [yol, _c2_yol("esik", c), _c2_yol("guc", c), _c2_yol("prefix", c), C2_YOL["kod"]]
            st = subprocess.run(["git", "status", "--porcelain"] + dosyalar, cwd=KOK_C2, capture_output=True, text=True, check=True).stdout.strip()
            lg = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_C2, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as ex:
            raise C2Hata(f"git denetimi yapılamadı: {ex}") from ex
        if st or not lg:
            raise C2Hata(f"ön kayıt / kod git'e işlenmemiş ya da değişmiş ({st or 'kayıt yok'}) -> koşu DURDU")
        out["git_onkayit"] = lg
    if kontrol:
        import IZ_KARNE as IK
        out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
    c2log.info("c2_kapi AÇIK (%s)", yol)
    return out


def _c2_jsonla(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _c2_jsonla(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)):
        return [_c2_jsonla(v) for v in o]
    if isinstance(o, pd.DataFrame):
        return _c2_jsonla(o.to_dict("records"))
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.datetime, _dt.date)):
        return str(o)
    return o


def c2_sonuc(J: Dict[str, Any]) -> Dict[str, Any]:
    """Önceden yazılı sonuç kuralı (C2_ESIK['sonuc_kurali'])."""
    Bh = pd.DataFrame(J["B"]["hucre"]); Ct = pd.DataFrame(J["C"]["satir"]); At = pd.DataFrame(J["A"]["ozet"]["tablo"])
    for k in ("fark", "boot_alt", "boot_ust"):
        Bh[k] = pd.to_numeric(Bh[k], errors="coerce")
    for k in ("yakala", "delta"):
        At[k] = pd.to_numeric(At[k], errors="coerce")
    kusur, eksik = [], []

    def h(kod, hc):
        q = Bh[(Bh.kod == kod) & (Bh.pazar == "ABD") & (Bh.hucre == hc)]
        return q.iloc[0] if len(q) else None
    for hc in C2_HUCRE:
        q = h("B1A", hc)
        if q is not None and q["fark"] > 0 and q["boot_alt"] > 0:
            kusur.append(f"momentum alt onda ABD {hc} R15 FARK > 0 ve boot alt > 0 ({_c2_y(q['fark'], 2)})")
        c = Ct[(Ct.pazar == "ABD") & (Ct.hucre == hc) & (Ct.n_hedef == "tam")]
        if len(c) and not bool(c.iloc[0]["gecti"]):
            kusur.append(f"plasebo kapısı ABD {hc} (tam n) düştü")
    r0 = At[(At.taban == "RAST") & (At.delta == 0.0) & At.pazar.isin(C2_KARAR) & At.n_hedef.isin(["100", "300", "1000", "yari"])].copy()
    r0["tohum"] = pd.to_numeric(r0["tohum"], errors="coerce")
    for (p_, hc_), x_ in r0.groupby(["pazar", "hucre"]):
        bp = float((x_.yakala * x_.tohum).sum() / x_.tohum.sum()) if x_.tohum.sum() > 0 else np.nan
        if np.isfinite(bp) and bp > 0.10:
            kusur.append(f"A RAST delta 0 yakalama {p_} {hc_} (n >= 100 birleşik, {int(x_.tohum.sum())} tohum-hücre): %{100 * bp:.1f}")
    a2 = At[(At.taban == "RAST") & (np.isclose(At.delta, 0.02)) & At.pazar.isin(C2_KARAR)]
    a_ok = all(((a2.pazar == p) & (a2.hucre == hc) & (a2.yakala >= 0.80)).any() for p in C2_KARAR for hc in C2_HUCRE)
    if not a_ok:
        eksik.append("A RAST delta +%2'de dört karar hücresinin birinde hiçbir n'de >= %80 yakalama yok")

    def arti(kod):
        q = [h(kod, hc) for hc in C2_HUCRE]
        return all(x is not None and x["fark"] > 0 for x in q) and any(x["boot_alt"] > 0 for x in q)

    def eksi(kod):
        q = [h(kod, hc) for hc in C2_HUCRE]
        return all(x is not None and x["fark"] < 0 for x in q)
    if not (arti("B1U") or arti("B2U")):
        eksik.append("B1U / B2U ABD iki hücrede FARK > 0 ve birinde boot alt > 0 değil")
    if not (eksi("B1A") or eksi("B2A")):
        eksik.append("B1A / B2A ABD iki hücrede FARK < 0 değil")
    karar = "HAYIR (KUSUR)" if kusur else ("EVET" if not eksik else "KISMEN")
    return {"karar": karar, "kusur": kusur, "eksik": eksik}


def c2_kos(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True, kontrol: bool = True,
           tohum_sayi: Optional[int] = None) -> Dict[str, Any]:
    c = cikti or C2_YOL["cikti"]; t0 = time.time()
    if os.path.exists(_c2_yol("json", c)):
        raise C2Hata(f"sonuç zaten var: {_c2_yol('json', c)} (ikinci koşu DURUR)")
    kapi = c2_kapi(c, veri, git, kontrol); bas = _c2_simdi()
    guc = json.load(open(_c2_yol("guc", c), encoding="utf-8")); esik = json.load(open(_c2_yol("esik", c), encoding="utf-8"))
    for p in C2_PAZAR:
        c2_panel_al(p, veri, esik["sinir"][p])
    J: Dict[str, Any] = {"surum": C2_SURUM, "kapi": kapi, "baslangic": bas}
    Ra = c2_a_kos(islem, veri, guc, tohum_sayi)
    Ra["satir"].to_csv(_c2_yol("a_satir", c), index=False, compression="gzip")
    J["A"] = {"say": Ra["say"], "ozet": c2_a_ozet(Ra["satir"])}
    Rb = c2_b_kos(veri, guc=guc)
    kol = [k for k in Rb["satir"].columns if k not in ("_esler",)]
    Rb["satir"][kol].to_csv(_c2_yol("b_satir", c), index=False, compression="gzip")
    J["B"] = {"hucre": Rb["hucre"], "etiket": Rb["etiket"], "say": Rb["say"]}
    Rc = c2_c_kos(veri, guc)
    Rc["satir"].to_csv(_c2_yol("c_satir", c), index=False)
    J["C"] = {"satir": Rc["satir"], "tani": Rc["tani"]}
    Bs = pd.read_csv(_c2_yol("b_satir", c), parse_dates=["giris", "tarih"])
    J["yeniden"] = c2_yeniden({"satir": Bs, "hucre": Rb["hucre"]}, veri)
    J["sonuc"] = c2_sonuc(_c2_jsonla(J))
    J["bitis"] = _c2_simdi(); J["sure_sn"] = round(time.time() - t0, 1)
    YH._yh_yaz(_c2_yol("json", c), json.dumps(_c2_jsonla(J), ensure_ascii=False, indent=1, default=YH._yh_json), "C2 json")
    J["rapor"] = c2_rapor(c)
    if not J["yeniden"]["tuttu"]:
        raise C2Hata(f"yeniden üretim TUTMADI: {J['yeniden']}")
    return J


# ================================================================ 12) RAPOR
def c2_rapor(cikti: Optional[str] = None) -> str:
    c = cikti or C2_YOL["cikti"]; J = json.load(open(_c2_yol("json", c), encoding="utf-8"))
    on = _c2_yol("onkayit", c); g = J["kapi"].get("git_onkayit", "-")
    s = [f"# CETVEL2 — POZİTİF KONTROL v2 ({J['bitis']})", "",
         f"{J['surum']}. Ön kayıt {os.path.basename(on)} (git {g}); koşu {J['baslangic']} .. {J['bitis']} ({J['sure_sn']} sn). R15 = 15. geçerli "
         "bar kapanışı / giriş açılışı - 1 (stop yok); FARK = R15 - konum eşli eş ortalaması (aynı gün, aynı ATRP x likidite x F15 kovası, bütün "
         "evren, en az 5 eş); puan = yüzde puan getiri. Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma).", "",
         f"**SONUÇ (önceden yazılı kural): {J['sonuc']['karar']}**", ""]
    for k in J["sonuc"]["kusur"]:
        s.append(f"- KUSUR: {k}")
    for k in J["sonuc"]["eksik"]:
        s.append(f"- eksik: {k}")
    # A
    T = pd.DataFrame(J["A"]["ozet"]["tablo"])
    s += ["", "## 1. A — YAPAY İZ: yakalama payı (20 tohum; yakalama = n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0; güç hariç)", "",
          "Sürüklenme: tutan olayın R15'i (1 + R15)(1 + delta) - 1. Taban DS = seçilen DS ANA olayları (delta 0 = DS olaylarının kendi konum eşli "
          "FARK'ı); taban RAST = aynı günlerde rastgele havuz hissesi (delta 0 = saf plasebo). Hücre: yakalama payı (güç dahil TUTAR payı) / "
          "ortalama ölçülen n / ortalama FARK (puan)."]
    nk_sira = ["30", "100", "300", "1000", "yari"]
    for tb in ("RAST", "DS"):
        for p in C2_ESIK["A"]["pazar"]:
            for h in C2_HUCRE:
                x = T[(T.pazar == p) & (T.hucre == h) & (T.taban == tb)]
                if not len(x):
                    continue
                hv = J["A"]["say"].get(p, {}).get("havuz", {}).get(h, "-")
                s += ["", f"**{tb} — {p} {h}** (havuz {hv})", "", "| n | " + " | ".join(f"delta {'+' if d else ''}{int(round(100 * d))}%"
                                                                                       for d in C2_ESIK["A"]["delta"]) + " |",
                      "|---|" + "---|" * len(C2_ESIK["A"]["delta"])]
                for nk in nk_sira:
                    row = [nk]
                    for de in C2_ESIK["A"]["delta"]:
                        q = x[(x.n_hedef == nk) & np.isclose(x.delta, de)]
                        row.append("-" if not len(q) else f"**%{100 * q.iloc[0].yakala:.0f}** (%{100 * q.iloc[0].tutar:.0f}) / "
                                                          f"{q.iloc[0].n:.0f} / {_c2_y(q.iloc[0].fark, 2)}")
                    s.append("| " + " | ".join(row) + " |")
    D4 = pd.DataFrame(J["A"]["ozet"]["dort"])
    if len(D4):
        s += ["", "Dört karar hücresi (ABD + AVR x eğitim + sınama) AYNI tohumda birlikte yakalama payı:", "",
              "| taban | n | " + " | ".join(f"delta {int(round(100 * d))}%" for d in C2_ESIK["A"]["delta"]) + " |", "|---|---|" + "---|" * 5]
        for tb in ("RAST", "DS"):
            for nk in nk_sira:
                row = [tb, nk]
                for de in C2_ESIK["A"]["delta"]:
                    q = D4[(D4.taban == tb) & (D4.n_hedef == nk) & np.isclose(D4.delta, de)]
                    row.append("-" if not len(q) or not np.isfinite(q.iloc[0].dort_hucre) else f"%{100 * q.iloc[0].dort_hucre:.0f}")
                s.append("| " + " | ".join(row) + " |")
    s += ["", "En küçük (delta, n) ile >= %80 yakalama (RAST tabanı):", ""]
    for p in C2_ESIK["A"]["pazar"]:
        for h in C2_HUCRE:
            x = T[(T.pazar == p) & (T.hucre == h) & (T.taban == "RAST") & (T.yakala >= 0.80) & (T.delta > 0)]
            if len(x):
                x = x.assign(nn=x.n.astype(float)).sort_values(["delta", "nn"])
                s.append(f"- {p} {h}: " + "; ".join(f"delta +%{100 * de:.0f} için n >= {x[np.isclose(x.delta, de)].nn.min():.0f}"
                                                   for de in sorted(x.delta.unique())))
            else:
                s.append(f"- {p} {h}: hiçbir (delta, n)'de >= %80 yok")
    # B
    B = pd.DataFrame(J["B"]["hucre"])
    s += ["", "## 2. B — BİLİNEN İZ: R15 (CETVEL2) ile h5 (eski cetvel, POZITIF_KONTROL) yan yana", "",
          "Aynı ANA olaylar (pk_b_olay.csv.gz). R15 FARK puan getiri, konum eşli bütün evren eşleri; h5 FARK puan olasılık (PK: DS kovası, orta "
          "eşler). p = ay kümeli işaret permütasyonu, önceden yazılı yön (U +, A -). [alt, üst] = ay kümeli boot %95.", "",
          "| kod | pazar | hücre | n | R15 FARK [alt, üst] | medyan | SIRA | L3O | p (R15) | güç | plasebo FARK / tutar | kapı | TUTAR | "
          "h5 FARK PK [alt, üst] | p (h5) | eski r15 FARK PK [alt, üst] | h5 (olay) | r60 fark |", "|" + "---|" * 18]
    for r in B.to_dict("records"):
        s.append(f"| {r['kod']} | {r['pazar']}{' (bilgi)' if r.get('bilgi') else ''} | {r['hucre']} | {r['n']} | {_c2_y(r['fark'], 2)} "
                 f"[{_c2_y(r['boot_alt'], 2)}, {_c2_y(r['boot_ust'], 2)}] | {_c2_y(r['med'], 2)} | {_c2_s(r['sira'])} | "
                 f"{_c2_y(r['l3o'] if r['yon'] == '+' else r['l3o_neg'], 2)} | {_c2_s(r['p'], 4)} | {_c2_s(r['guc'], 2)} | "
                 f"{_c2_y(r['plasebo_fark'], 2)} / %{100 * (r['plasebo_tutar_pay'] or 0):.0f} | {'geçti' if r['plasebo_gecti'] else 'DÜŞTÜ'} | "
                 f"{'TUTAR' if r['tutar'] else ('ters' if r['ters'] else '-')} | {_c2_y(r.get('h5_fark_pk'), 1)} [{_c2_y(r.get('h5_alt_pk'), 1)}, "
                 f"{_c2_y(r.get('h5_ust_pk'), 1)}] | {_c2_s(r.get('h5_p_pk'), 4)} | {_c2_y(r.get('r15_fark_pk'), 2)} [{_c2_y(r.get('r15_alt_pk'), 2)}, "
                 f"{_c2_y(r.get('r15_ust_pk'), 2)}] | {_c2_y(r.get('h5'), 1, False)} | {_c2_y(r.get('r60_fark'), 2)} |")
    s += ["", "Huni (B): " + "; ".join(f"{k}: girdi {v.get('girdi_pk')}, olay {v.get('girdi')} -> tekil sonrası R15 ölçülen {v.get('olcum_r15')}, "
                                       f"giriş PK ile aynı {v.get('giris_ayni')}, kova yok {v.get('kova_yok')}" for k, v in J["B"]["say"].items())]
    E = pd.DataFrame(J["B"]["etiket"])
    if len(E):
        s += ["", "| kod | pazar | etiket (ham) | gerekçe | etiket |", "|---|---|---|---|---|"]
        for r in E.to_dict("records"):
            s.append(f"| {r['kod']} | {r['pazar']} | {r['etiket_ham']} | {r['neden']} | {r['etiket']} |")
    # C
    C = pd.DataFrame(J["C"]["satir"]); Tn = pd.DataFrame(J["C"]["tani"])
    s += ["", f"## 3. C — PLASEBO KAPISI (aynı gün rastgele havuz hissesi, {C2_ESIK['plasebo']['tohum_sayi']} tohum; geçer = |ort FARK| < 0,5 puan "
          "VE TUTAR payı <= %7)", "",
          "| pazar | hücre | n | ort FARK (puan) | sd (tohumlar) | TUTAR payı + / - | yakalama payı + (güç hariç) | geçti | karar hücresi |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in C.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['hucre']} | {r['n_hedef']} ({r['n']:.0f}) | {_c2_y(r['fark_ort'], 2)} | {_c2_y(r['fark_sd'], 2, False)} | "
                 f"%{100 * r['tutar_pay_arti']:.0f} / %{100 * r['tutar_pay_eksi']:.0f} | %{100 * r['yakala_pay_arti']:.0f} | "
                 f"{'EVET' if r['gecti'] else 'HAYIR'} | {'karar' if r['karar'] else 'bilgi'} |")
    r0 = T[(T.taban == "RAST") & np.isclose(T.delta, 0.0) & T.n_hedef.isin(["100", "300", "1000", "yari"])]
    s += ["", "A RAST delta 0 (saf plasebo) yakalama payı, n >= 100 birleşik (sonuç kuralı iii): " + "; ".join(
        f"{p} {h} %{100 * float((x.yakala * x.tohum).sum() / x.tohum.sum()):.1f}" for (p, h), x in r0.groupby(["pazar", "hucre"]))]
    s += ["", "Tanı (AVR sınama sapması için; eski cetvelde AVR sınama plasebo +2,2 puan):", "",
          "| pazar | hücre | gün | havuz / gün (medyan) | R15 + kova / gün | dolu kova / gün | DS olay (R15) | eşsiz payı | eş sayısı medyan / p10 | "
          "olay günü | DS FARK0 ort | havuz R15 ort |", "|" + "---|" * 12]
    for r in Tn.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['hucre']} | {r['gun']} | {_c2_s(r['havuz_gun_medyan'], 0)} | {_c2_s(r['r15_kova_gun_medyan'], 0)} | "
                 f"{_c2_s(r['dolu_kova_medyan'], 0)} | {r['olay_r15']} | %{100 * (r['essiz_pay'] or 0):.1f} | {_c2_s(r['n_es_medyan'], 0)} / "
                 f"{_c2_s(r['n_es_p10'], 0)} | {r['olay_gun_sayi']} | {_c2_y(r['fark0_ort'], 2)} | {_c2_y(r['r15_ort_havuz'], 2)} |")
    Yd = J["yeniden"]
    s += ["", "## 4. YENİDEN ÜRETİM (K11)", "", f"Durum: {'TUTTU' if Yd['tuttu'] else 'TUTMADI'}"]
    for h in Yd["hucre"]:
        s.append(f"- {h['kod']} ABD {h['hucre']}: düz pandas n {h['n_duz']}, FARK {_c2_y(h['fark_duz'], 4)}, SIRA {_c2_s(h['sira_duz'], 6)} | kod n "
                 f"{h['n']}, FARK {_c2_y(h['fark'], 4)}, SIRA {_c2_s(h['sira'], 6)} -> {'eşit' if h['esit'] else 'FARKLI'}")
    s.append(f"- 50 olay R15 düz döngü: bozuk {len(Yd['r15_bozuk'])}; 5 olay eş ortalaması bütün evren düz döngü: bozuk {len(Yd['es_bozuk'])}")
    s += ["", "## 5. NOTLAR", "", "- Evren bugün işlem gören hisseler: hayatta kalma yanlılığı olaya ve eşe aynı biçimde etki eder.",
          "- Bu iş cetvel sınamasıdır; 'iz' iddiası yoktur. Etiketler (B) yalnız cetvelin davranışını gösterir."]
    metin = "\n".join(s) + "\n"
    YH._yh_yaz(_c2_yol("rapor", c), metin, "C2 rapor")
    return metin


# ================================================================ 13) v2.2: UFUK H = 15 / 30 / 45, YÖN BAŞINA PLASEBO, AÇIK VERİ (KASA)
# İş tanımı arastirma_cikti/kart/KART_TUR1_IS_TANIMI.md bölüm 2 (ADIM K1). v2.1 fonksiyonları ve C2_ESIK DEĞİŞMEDİ: v2.2 yalnız bu bölümdeki
# sözlük / fonksiyonlarla ve c2_olc(..., ufuk=H) ile çalışır; ufuk verilmeyen her çağrı v2.1 ile bayt bayt aynıdır (c2_regresyon21).
C2_E22 = "_v2.2"
C2_SURUM22 = ("CETVEL2 v2.2 (2026-11-21): R_H (H = 15 / 30 / 45) konum eşli fark (bütün evren), iki yönlü plasebo eşiği yön başına, açık veri "
              "(KASA <= 2022-12-31); pozitif kontrol v2.2")
C2_HUCRE22 = ["d1619", "d2022"]

# ---------------------------------------------------------------- MÜHÜRLÜ v2.2 AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
C2_ESIK22: Dict[str, Any] = {
    "surum": "C2.2",
    "taban": "C2_ESIK (v2.1; sha ön kayıtta) AYNEN: giriş E0 (t'den sonraki ilk geçerli bar açılışı), eş (aynı giriş günü, aynı pazar, aynı kova "
             "= ATRP tercili x likidite üçlüsü x F15 çeyreği, bütün evren, aynı denemenin o günkü olayları ve olayın kendisi dışı, en az 5), "
             "FARK / SIRA, boot (ay kümeli, B 2000), perm (ay kümeli işaret, R 10000), hücre TUTAR şartları (n >= 30, güç >= 0,80, FARK yönlü, "
             "boot ucu, SIRA, L3O), plasebo (200 tohum, |ort FARK| < 0,005, TUTAR payı <= %7), güç (delta +0,02, %80), BH q 0,10. Yalnız bu "
             "sözlüktekiler eklendi / değişti",
    "ufuklar": [15, 30, 45], "karar_ufuk": [15, 30], "bilgi_ufuk": [45],
    "r_h": "R_H = H. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 2H birleşik takvim satırında H geçerli bar yoksa "
           "NaN (H = 15: v2.1 R15 ile aynı, 30 satır); stop YOK. Matris c2_rh; olay satırında 'r15' sütunu R_H'yi taşır, 'ufuk' sütunu H",
    "pencere_kat": 2,
    "tekil": "aynı hissede olaylar giriş günü sırasıyla birleşik takvimde >= H işlem günü arayla (OC tekil kuralı, tekil_gun = H)",
    "es": "v2.1 ile aynı; eş havuzu ufuk başına (havuzda, kovası var, R_H ölçülebilir)",
    "donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
    "donem_not": "hücre = pazar x dönem (giriş günü); 2023 sonrası KASA'da mühürlü, bu sürümde görülmez",
    "kova_donem": ["2016-01-01", "2022-12-31"],
    "kova": "v2.1 tanımı (c2_kova_sinir: ATRP tercil ve F15 çeyrek sınırları, havuz hisse-günleri, getirisiz) AÇIK VERİDEN (giriş 2016-22) yeniden "
            "sabitlenir; sayılar cetvel2_esik_v2.2.json ve ön kayıtta (v2.1 sayıları yan yana)",
    "veri": {"klasor": "/tmp/kasa/acik (= /tmp/veri = /tmp/veri2); başka fiyat kaynağı YOK", "kesik_tarih": "2022-12-31",
             "kesik": "KASA açık kesik 2022-12-31 (veri sonu 2022-12-30); H. barı veri sonunu aşan olay ölçülmez (R_H NaN, eş havuzu da)",
             "kapi": "KASA.kasa_kapisi(V_ABD / V_AVR / V_BIST + açık DS olay kopyası) her koşudan önce; KASA_DURUM.json açık kesik = kesik_tarih "
                     "değilse DURUR; çıktı satır dosyalarının en geç tarihi (KASA.ks_en_gec_tarih) raporda"},
    "plasebo_iki_yon": "'?' hipotezde plasebo kapısı: |200 tohum ort FARK| < 0,005 VE + yönde TUTAR payı <= %7 VE - yönde TUTAR payı <= %7 (yön "
                       "başına ayrı; v2.1'de iki yönün birleşik payı %7 ile karşılaştırılıyordu: H286 / Ç204 hata v). '+' / '-' hipotezde v2.1 "
                       "ile aynı (hipotezin yönündeki pay)",
    "guc": {"hucre": ["d1619", "d2022", "acik"],
            "tanim": "v2.1 tanımı (DS ANA olaylarının konum eşli FARK yayılımı, sigma(n) = exp(a + b ln n), güç = Phi(0,02 / sigma - 1,96), %80) "
                     "pazar x hücre x H; 'acik' = 2016-22 bütün açık olaylar; c2_olc(ufuk = H) adı eğride olmayan hücrede (ör. KASA blok "
                     "birikimi) 'acik' eğrisini kullanır. Getiri ortalaması kullanılmaz"},
    "A": {"pazar": ["ABD", "AVR", "BIST"], "karar_pazar": ["ABD", "AVR"], "n": [30, 100, 300, 1000],
          "delta": [0.0, 0.01, 0.02, 0.03, 0.05], "tohum_sayi": 20, "tohum": 2221, "n_azami_pay": 2 / 3,
          "olay": "DS ANA olayları (ds_olay.csv.gz; tarih <= açık kesik süzülmüş kopya c2_ds_olay_acik_v2.2.csv.gz; c2_olay tekil H); havuz = hücrede "
                  "R_H ölçülebilir ve tek başına (deneme = kendisi) >= 5 eşi olan olaylar; her tohum x n x hücre x H havuzdan yerine koymadan n "
                  "'tutan' (n > 2/3 havuz ise ölçülmez)",
          "taban": "DS = seçilen DS olayları; RAST = her seçilen olayın giriş gününde havuzdan rastgele hisse (c2_rastgele; delta 0 = saf plasebo)",
          "surukleme": "tutan olayın R_H'si (1 + R_H)(1 + delta) - 1 (E0 değişmez); eşler dokunulmaz",
          "yakala": "hücre TUTAR şartları güç HARİÇ (n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0); güç dahil TUTAR ve p < 0,05 bilgi"},
    "B": {"pazar": ["ABD", "AVR"], "karar_pazar": ["ABD"], "hipotez": {"B1U": ["U", "+"], "B1A": ["A", "-"]},
          "olay": "12-1 momentum: POZITIF_KONTROL.pk_b_sinyal_mom + pk_b_kur AÇIK VERİDEN yeniden üretilir (ay sonu t, MOM = C(t-21) / C(t-252) - 1, "
                  "havuz sonrası aynı t kesitinde sıra: üst onda U, alt onda A; ANA = U ya da A, aynı hissede >= 15 bar arayla ilk); c2_olc "
                  "(ufuk = H, tekil H; eş = bütün evren, aynı gün aynı kova, aynı denemenin o günkü olayları dışı)",
          "pead": "B2 PEAD: sec_ozet (8-K madde 2.02) olay verisi açık klasörde (/tmp/kasa/acik) YOK -> 'VERİ YOK', atlanır (internete çıkılmaz)",
          "b1u_kural": "üst onda (+): ABD iki dönemde FARK > 0 ve en az birinde boot alt > 0",
          "b1a_kural": "alt onda (-): 0'ı kesmesi yeter = ABD iki dönemde boot alt <= 0 (FARK > 0 VE boot alt > 0 = KUSUR)"},
    "C": {"n": ["tam", 100, 300], "tohum": 2231,
          "tanim": "plasebo kapısı her pazar x dönem x H hücresinde DS ANA olay günleriyle (tam n ve n 100 / 300 rastgele alt küme günleri), 200 "
                   "tohum, '+' ve '-' payları ayrı; geçti = |ort FARK| < 0,005 VE + payı <= %7 VE - payı <= %7; tanı: havuz, eş, eşsiz, dolu kova"},
    "r45_kurali": "R45 KARAR ufkuna ancak şu ikisi birlikte tutarsa girer: (i) plasebo kapısı H = 45'te ABD ve AVR hücrelerinde geçer (C, tam n, "
                  "d1619 ve d2022, dört hücre); (ii) momentum üst onda (B1U) ABD'de iki alt dönemde de R45 FARK boot alt ucu > 0 iken R30'da "
                  "en az birinde değil (boot alt <= 0; yani 45 mum 30'un göremediğini görüyor). Tutmazsa R45 yalnız BİLGİ sütunu. R15 ve R30 "
                  "her durumda KARAR ufku",
    "sonuc_kurali": {
        "tanim": "her H için ayrı ('cetvel H mumda doğru şeye duyarlı mı')",
        "KUSUR": "(i) B1A ABD d1619 ya da d2022 hücresinde FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı (C, tam n) ABD d1619 / d2022 "
                 "hücrelerinden birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR hücresinde n 100 / "
                 "300 / 1000 tohumları birleşik > %10",
        "EVET": "KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin (ABD / AVR x d1619 / d2022) her birinde bir n'de >= %80 "
                "yakalama VE B1U ABD iki dönemde FARK > 0 ve en az birinde boot alt > 0",
        "KISMEN": "KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)",
        "HAYIR": "KUSUR var"},
    "yeniden_uretim": {"hucre": [["B1U", "ABD", "d2022", 30], ["B1A", "ABD", "d1619", 15], ["B1U", "AVR", "d1619", 45]],
                       "elle_rh": 20, "elle_es": 5, "elle_es_ufuk": 30, "tohum": 2241,
                       "tanim": "c2_b_olay_v2.2 satır dosyasından üç hücre (yukarıdaki) n / ort FARK / ort SIRA düz pandas; her H için 20 B1 ABD "
                                "olayının R_H'si ham veriden düz döngüyle; 5 B1U ABD olayının (H = 30) eş ortalaması bütün evren üzerinde düz "
                                "döngüyle (kova elle)"},
    "regresyon_v21": {"giris_son": "2022-10-31", "hucre": [["B1U", "ABD"], ["B1A", "ABD"], ["B1U", "AVR"]],
                      "tanim": "v2.1 çağrısı (ufuk yok, cetvel2_esik_v2.1.json kova sınırları) açık veride, pk_b_olay.csv.gz B1 ANA olaylarıyla (tarih "
                               "<= açık kesik); giriş <= 2022-10-31 olaylarında giris / kova / E0 / R15 / eş ortalaması / eş sayısı / SIRA / FARK "
                               "c2_b_olay_v2.1.csv.gz ile BİREBİR (rtol 1e-12); üç eğitim hücresinin bu olay alt kümesinde n / ort FARK / ort SIRA "
                               "eşit (< 1e-12)"},
}

C2_KONTROL22: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü x F15 çeyreği), bütün evren havuzu, aynı "
                   "geometri (R_H stop'suz, aynı E0, aynı H); aynı denemenin o günkü olayları ve olayın kendisi eş dışı; en az 5 eş (c2_es); taban "
                   "rastgele olay sağlaması = plasebo kapısı 200 tohum (c2_plasebo; '?' yön başına); mekanik üstünlük yok: stop / hedef yok, R_H "
                   "olay ve eşte aynı"),
    "K2": ("EVET", "kova girdileri giriş gününden ÖNCEKİ son geçerli barda; c2_prefix her pazarda 30 olayda veri t'de kesilince ATRP / F15 / hat "
                   "aynı (cetvel2_prefix_v2.2.json; tutmazsa DURUR); kova sınırları getirisiz; R_H yalnız giriş açılışından sonrası; veri KASA açık "
                   "kesik 2022-12-31 (kasa_kapisi her koşudan önce; satır dosyası en geç tarihi raporda); momentum olayları açık veriden yeniden"),
    "K3": ("EVET", "OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması; R_H yalnız geçerli barlar (hissenin kendi takvimi); "
                   "sinyal günü geçersiz bar ise olay düşer"),
    "K4": ("EVET", "olaylar aynı hissede >= H işlem günü arayla (tekil_gun = H; örtüşmeyen H bar); n = ölçülen olay; boot / permütasyon birimi "
                   "giriş ayı; medyan FARK raporda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (oc_olay_hazirla d; R_H paydası P['Op'][d, j]); eşler aynı gün açılışı"),
    "K6": ("EVET", "V_*.pkl tek kip (açık kısım, KASA bayt bayt bölünmüş); R_H / ATRP / F15 oran (birimsiz); likidite günlük kesit sırası; "
                   "geçmiş bölünme şüphesi havuz dışı (OC)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST 581); kesikten sonra doğan semboller açık kısımda yok; "
                   "yanlılık olaya ve eşe aynı; raporda yazılı"),
    "K8": ("EVET", "iki alt dönem (2016-19, 2020-22) ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç eğrisi pazar x dönem x H; A 20 tohum x 4 n x 5 delta x 3 "
                   "H; plasebo 200 tohum; R45 kuralı ve sonuç kuralı önceden yazılı"),
    "K9": ("EVET", "CETVEL2_ON_KAYIT_v2.2.md: C2_ESIK22 sha, C2_ESIK (v2.1) sha, CETVEL2.py sha + kod commit, kova sınırları (sayı), güç eğrisi, "
                   "R45 kuralı, DS / YH / OC / PK / KASA sha'ları, veri ve açık DS olay kopyası sha'ları, KASA açık kesik; c2_kapi22 git kaydı + "
                   "değişmemiş + ik_kontrol_kapisi; sıra kod commit -> ön kayıt commit -> koşu"),
    "K10": ("UYGULANMAZ", "ham haber / KAP / SEC ayrıştırması yok; DS olayları repo satır dosyasından (açık kesiğe süzülmüş kopya), momentum "
                          "açık fiyattan; PEAD VERİ YOK"),
    "K11": ("EVET", "c2_yeniden22: üç hücre satır dosyasından düz pandas; 3 x 20 olayın R_H'si ham veriden düz döngü; 5 olayın eş ortalaması "
                    "bütün evren düz döngü (kova elle); c2_regresyon21: v2.1 çağrısı satır dosyasıyla birebir; tutmazsa koşu TUTMADI"),
    "K12": ("EVET", "cetvel sınaması; 'iz' iddiası yok; FARK, SIRA, p, yakalama payı ayrı; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_c2; test); DS / YH / OC / PK / KASA ve defter dosyalarına dokunulmadı (sha ön kayıtta); "
                    "e-posta / anahtar taraması (YH._yh_yaz); dış servis / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; cetvel sınaması"),
}


def c2_esik22_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(C2_ESIK22 if E is None else E)


def _c2_donem22(g: Any, Dn: Optional[Dict[str, List[str]]] = None) -> np.ndarray:
    """Giriş günü -> hücre adı (sözlük sırasıyla ilk eşleşen; hiçbiri değilse 'dis')."""
    Dn = Dn or C2_ESIK22["donem"]; g = pd.to_datetime(pd.Series(g)).to_numpy()
    out = np.full(len(g), "dis", dtype=object)
    for ad, (a, b) in Dn.items():
        m = (g >= np.datetime64(pd.Timestamp(a))) & (g <= np.datetime64(pd.Timestamp(b))) & (out == "dis")
        out[m] = ad
    return out


def c2_rh(P: Dict[str, Any], Vd: Dict[str, Any], H: int, Rz: int) -> np.ndarray:
    """R_H matrisi (giriş günü d x hisse): H. geçerli bar kapanışı / giriş açılışı - 1; Rz birleşik takvim satırında H geçerli bar yoksa NaN."""
    idx = P["tarih"]; S = P["sembol"]; R = np.full((len(idx), len(S)), np.nan); k = int(H) - 1
    for j, s in enumerate(S):
        df = Vd["V"][s]; pos = idx.get_indexer(df.index)
        if (pos < 0).any():
            raise C2Hata(f"{s}: hisse takvimi panelde yok")
        O = df.Open.to_numpy(float); C = df.Close.to_numpy(float); m = len(pos)
        if m > k:
            e = np.arange(m - k); f = e + k; ok = (pos[f] - pos[e]) <= int(Rz) - 1
            with np.errstate(invalid="ignore", divide="ignore"):
                R[pos[e[ok]], j] = C[f[ok]] / O[e[ok]] - 1
    return R


def c2_panel_h(Pb: Dict[str, Any], H: int) -> Dict[str, Any]:
    """Taban panelden (c2_panel; kova / ATRP / F15 ortak) ufuk H paneli: 'R15' anahtarı R_H, eş havuzu R_H ile yeniden. Taban değişmez."""
    H = int(H); Rz = int(C2_ESIK22["pencere_kat"]) * H
    R = c2_rh(Pb["P"], Pb["Vd"], H, Rz)
    if H == int(C2_ESIK["ufuk"]) and Rz == int(C2_ESIK["pencere_azami"]):
        na, nb = np.isnan(R), np.isnan(Pb["R15"])
        if not (np.array_equal(na, nb) and np.array_equal(R[~na], Pb["R15"][~na])):
            raise C2Hata(f"{Pb['pazar']}: R_15 (c2_rh) v2.1 R15 matrisiyle aynı değil")
    Pn = dict(Pb); Pn["R15"] = R; Pn["ufuk"] = H; Pn["pencere"] = Rz
    _c2_havuz(Pn)
    c2log.info("%s ufuk %d paneli: havuz (R_H + kova) %d hisse-gün", Pb["pazar"], H, len(Pn["h_r"]))
    return Pn


_C2_PN22: Dict[Any, Dict[str, Any]] = {}


def c2_panel22_al(pazar: str, veri: Optional[str] = None, ufuk: Optional[int] = 15, sinir: Optional[Dict[str, Any]] = None,
                  onbellek: bool = True) -> Dict[str, Any]:
    """v2.2 panel önbelleği: taban (pazar; kova sınırları cetvel2_esik_v2.2.json, yoksa açık veriden) ve ufuk paneli (pazar, H)."""
    kb = ("baz", pazar)
    if onbellek and kb in _C2_PN22 and (sinir is None or _C2_PN22[kb]["sinir"] == sinir):
        Pb = _C2_PN22[kb]
    else:
        if sinir is None:
            yol = _c2_yol("esik", None, C2_E22)
            if os.path.exists(yol):
                sinir = json.load(open(yol, encoding="utf-8"))["sinir"].get(pazar)
        Pb = c2_panel(c2_veri(pazar, veri), sinir)
        if onbellek:
            for k in [k for k in _C2_PN22 if k[0] == pazar]:
                _C2_PN22.pop(k)
            _C2_PN22[kb] = Pb
    if ufuk is None:
        return Pb
    k = (pazar, int(ufuk))
    if onbellek and k in _C2_PN22 and _C2_PN22[k]["sinir"] == Pb["sinir"]:
        return _C2_PN22[k]
    Pn = c2_panel_h(Pb, int(ufuk))
    if onbellek:
        _C2_PN22[k] = Pn
    return Pn


def _c2_egri22_al(pazar: str, hucre: str, ufuk: int, guc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if guc is None:
        yol = _c2_yol("guc", None, C2_E22)
        if not os.path.exists(yol):
            return None
        guc = json.load(open(yol, encoding="utf-8"))
    eg = guc.get("egri", {}).get(pazar, {})
    e = eg.get(hucre) or eg.get("acik") or {}
    return e.get(str(int(ufuk)))


def c2_olc22(olaylar: pd.DataFrame, hipotez: Dict[str, Dict[str, Any]], ufuk: int, donem: Optional[Dict[str, List[str]]] = None,
             **kw: Any) -> Dict[str, Any]:
    """ADIM K2 ARAYÜZÜ (v2.2). c2_olc(olaylar, hipotez, ufuk = H, donem = {hücre adı: [başlangıç, bitiş]} (giriş günü), **kw).
    olaylar: DataFrame[pazar, sembol, tarih (sinyal günü t), F_<...> bayrakları (1 / 0 / NaN)]; hipotez: {kod: {'bayrak': 'F_x' | None, 'yon':
    '+' / '-' / '?'}}; ufuk 15 / 30 / 45. Hücre: pazar x donem; güç eğrisi (cetvel2_guc_v2.2.json) hücre adında yoksa 'acik' (2016-22). kw:
    veri, plasebo, bilgi, m_bh, tohum0, guc, tekil_gun (varsayılan H), karar (varsayılan ABD / AVR). Döner c2_olc sözlüğü ('hucre' ve 'etiket'
    'ufuk' sütunlu; etiket p_bh = karar pazarları x bütün hücrelerde en büyük p)."""
    return c2_olc(olaylar, hipotez, ufuk=ufuk, donem=donem, **kw)


# ---------------------------------------------------------------- olay kümeleri (yalnız açık veri)
def _c2_kesik22(kasa_dizin: Optional[str] = None) -> pd.Timestamp:
    """KASA_DURUM.json açık kesiği; C2_ESIK22 kesik_tarih'ten farklıysa DURUR."""
    import KASA as _KS
    try:
        k = pd.Timestamp(_KS._durum_oku(kasa_dizin or _KS.KS_YOL["dizin"])["acik_kesik"])
    except Exception as ex:   # kasa durumu okunamazsa ölçüm başlamaz (fail-closed)
        raise C2Hata(f"KASA durumu okunamadı: {type(ex).__name__}: {ex}") from ex
    if k != pd.Timestamp(C2_ESIK22["veri"]["kesik_tarih"]):
        raise C2Hata(f"KASA açık kesik {k.date()} != ön kayıttaki {C2_ESIK22['veri']['kesik_tarih']} -> DURDU")
    return k


def c2_ds_acik22(cikti: Optional[str] = None, kaynak: Optional[str] = None, kesik: Optional[Any] = None) -> str:
    """ds_olay.csv.gz -> tarih <= açık kesik süzülmüş kopya (c2_ds_olay_acik_v2.2.csv.gz; sıralı, gzip mtime 0 = aynı girdiyle aynı bayt)."""
    src = kaynak or C2_YOL["ds_olay"]; k = pd.Timestamp(kesik or C2_ESIK22["veri"]["kesik_tarih"])
    if not os.path.exists(src):
        raise C2Hata(f"DS olay dosyası yok: {src}")
    X = pd.read_csv(src, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"])
    X = X[X.tarih <= k].sort_values(["pazar", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    X["tarih"] = X.tarih.dt.strftime("%Y-%m-%d")
    yol = os.path.join(cikti or C2_YOL["cikti"], f"c2_ds_olay_acik{C2_E22}.csv.gz")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    X.to_csv(yol, index=False, compression={"method": "gzip", "mtime": 0})
    return yol


def c2_ds_olay22(pazar: str, yol: Optional[str] = None) -> pd.DataFrame:
    yol = yol or os.path.join(C2_YOL["cikti"], f"c2_ds_olay_acik{C2_E22}.csv.gz")
    if not os.path.exists(yol):
        raise C2Hata(f"açık DS olay kopyası yok: {yol} (c2_ds_acik22)")
    X = pd.read_csv(yol, parse_dates=["tarih"])
    if len(X) and X.tarih.max() > pd.Timestamp(C2_ESIK22["veri"]["kesik_tarih"]):
        raise C2Hata(f"açık DS olay kopyasında kesik sonrası tarih var ({X.tarih.max().date()}) -> DURDU")
    return X[X.pazar == pazar][["sembol", "tarih"]].reset_index(drop=True)


def c2_mom22(pazar: str, veri: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """12-1 momentum ANA olayları AÇIK VERİDEN (POZITIF_KONTROL.pk_b_sinyal_mom + pk_b_kur; v2.1 pk_b_olay ile aynı tanım)."""
    Pb = c2_panel22_al(pazar, veri, None); Vd, P = Pb["Vd"], Pb["P"]
    sg = PK.pk_b_sinyal_mom(Vd, P)
    seri = {s: PK.pk_seri(Vd["V"][s]) for s in P["sembol"]}
    X, _, say = PK.pk_b_kur("B1", Vd, P, sg, seri, None)
    A = X[X.ana].copy()
    O = pd.DataFrame({"sembol": A.sembol.astype(str).to_numpy(), "tarih": pd.to_datetime(A.tarih).to_numpy(),
                      "F_U": A.U.astype(bool).astype(float).to_numpy(), "F_A": A.A.astype(bool).astype(float).to_numpy()})
    O = O.sort_values(["sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    sy = {"sinyal": int(len(sg)), "ana": int(len(O)), "U": int(O.F_U.sum()), "A": int(O.F_A.sum()),
          "son_tarih": str(O.tarih.max().date()) if len(O) else "-", "pk": {k: v for k, v in say.items() if k in ("girdi", "olay_havuz", "U", "A", "ana")}}
    return O, sy


# ---------------------------------------------------------------- ön kayıt girdileri (getirisiz ya da yalnız yayılım)
def c2_hazirlik22(veri: Optional[str] = None, cikti: Optional[str] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    """Kova sınırları (açık veri 2016-22), güç eğrisi (DS ANA FARK sigma; pazar x hücre x H), prefix. Kesik denetimi dahil."""
    c = cikti or C2_YOL["cikti"]; sinir, egri, pre, huni = {}, {}, {}, {}
    if C2_ESIK22["kova_donem"] != C2_ESIK["donem"]["egitim"]:
        raise C2Hata("kova dönemi v2.1 eğitim dönemiyle aynı değil")
    U = [int(h) for h in C2_ESIK22["ufuklar"]]; GH = list(C2_ESIK22["guc"]["hucre"])
    for pi, p in enumerate(C2_PAZAR):
        Pb = c2_panel(c2_veri(p, veri)); _C2_PN22[("baz", p)] = Pb; sinir[p] = Pb["sinir"]
        egri[p] = {h: {} for h in GH}; huni[p] = {}
        for ui, H in enumerate(U):
            Pn = c2_panel22_al(p, veri, H)
            X, say = c2_olay(c2_ds_olay22(p, ds_yol), Pn, tekil_gun=H); X["donem"] = _c2_donem22(X.giris)
            e = c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float))
            dn = X.donem.to_numpy()
            for hi, h in enumerate(GH):
                msk = np.isin(dn, C2_HUCRE22) if h == "acik" else (dn == h)
                egri[p][h][str(H)] = c2_guc_egri(e["fark"][msk], tohum_ek=pi * 100 + hi * 10 + ui)
                egri[p][h][str(H)]["n_olay_r"] = int((msk & np.isfinite(X.r15.to_numpy(float))).sum())
            huni[p][str(H)] = {**{k: v for k, v in say.items() if k != "donem"}, "donem": {k: int(v) for k, v in pd.Series(dn).value_counts().items()},
                               "olcum_rh": int(np.isfinite(X.r15).sum()), "esli": int(np.isfinite(e["fark"]).sum()),
                               "son_giris_olculen": str(pd.Timestamp(X.giris[np.isfinite(X.r15)].max()).date()) if np.isfinite(X.r15).any() else "-"}
            if H == int(C2_ESIK["ufuk"]):
                pr = c2_prefix(Pn, X)
                if pr["bozuk"]:
                    raise C2Hata(f"{p}: prefix TUTMADI ({pr['bozuk']} / {pr['n']}): {[o for o in pr['olay'] if not o['tut']][:3]}")
                pre[p] = pr
    os.makedirs(c, exist_ok=True)
    YH._yh_yaz(_c2_yol("esik", c, C2_E22), json.dumps({"surum": C2_SURUM22, "sinir": sinir}, ensure_ascii=False, indent=1, default=YH._yh_json),
               "C2 v2.2 eşik")
    YH._yh_yaz(_c2_yol("guc", c, C2_E22), json.dumps({"surum": C2_SURUM22, "delta": C2_ESIK["guc"]["delta"], "egri": egri, "huni": huni},
                                                     ensure_ascii=False, indent=1, default=YH._yh_json), "C2 v2.2 güç")
    YH._yh_yaz(_c2_yol("prefix", c, C2_E22), json.dumps(pre, ensure_ascii=False, indent=1, default=YH._yh_json), "C2 v2.2 prefix")
    return {"sinir": sinir, "egri": egri, "prefix": pre, "huni": huni}


def _c2_git_son(yol: str) -> str:
    try:
        return subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_C2, capture_output=True, text=True,
                              check=True).stdout.strip() or "-"
    except (OSError, subprocess.CalledProcessError):
        return "-"


def c2_sha22_simdi(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, str]:
    v = veri or C2_YOL["veri"]; c = cikti or C2_YOL["cikti"]
    import KASA as _KS
    out = {"C2_ESIK22_SHA": c2_esik22_sha(), "C2_ESIK_SHA": c2_esik_sha(), "C2_KOD_SHA": _c2_sha(C2_YOL["kod"]),
           "PK_KOD_SHA": _c2_sha(C2_YOL["pk_kod"]), "KASA_KOD_SHA": _c2_sha(os.path.join(KOK_C2, "KASA.py"))}
    ds = DS.ds_sha_simdi(veri=v)
    for k in ("DS_KOD_SHA", "YH_KOD_SHA", "OC_KOD_SHA", "DS_ESIK_SHA", "YH_ESIK_SHA", "OC_ESIK_SHA", "V_ABD_SHA", "V_AVR_SHA", "V_BIST_SHA"):
        out[k] = ds[k]
    kd = os.path.join(_KS.KS_YOL["dizin"], "acik", _KS.KS_DURUM_AD)
    for k, y in (("KASA_DURUM_SHA", kd), ("DS_OLAY_SHA", C2_YOL["ds_olay"]), ("C2_DS_ACIK22_SHA", os.path.join(c, f"c2_ds_olay_acik{C2_E22}.csv.gz")),
                 ("C2_ESIK22_JSON_SHA", _c2_yol("esik", c, C2_E22)), ("C2_GUC22_JSON_SHA", _c2_yol("guc", c, C2_E22)),
                 ("C2_PREFIX22_SHA", _c2_yol("prefix", c, C2_E22)), ("C2_ESIK21_JSON_SHA", _c2_yol("esik", c, "_v2.1")),
                 ("PK_B_OLAY_SHA", C2_YOL["pk_b"]), ("C2_B21_SATIR_SHA", _c2_yol("b_satir", c, "_v2.1"))):
        out[k] = _c2_sha(y) if os.path.exists(y) else "-"
    return out


def c2_onkayit22_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False, ds_kaynak: Optional[str] = None,
                     kasa: bool = True) -> str:
    c = cikti or C2_YOL["cikti"]; yol = _c2_yol("onkayit", c, C2_E22)
    if os.path.exists(yol) and not uzerine:
        raise C2Hata(f"ön kayıt zaten var: {yol}")
    import KASA as _KS
    v = veri or C2_YOL["veri"]
    if kasa:
        kes = _c2_kesik22(); c2_kasa22(veri)
        durum = _KS._durum_oku(_KS.KS_YOL["dizin"])
    else:   # yalnız sentetik test
        kes = pd.Timestamp(C2_ESIK22["veri"]["kesik_tarih"]); durum = {"muhur_id": "TEST (kasa kapısı atlandı)", "acilan": []}
    dsy = c2_ds_acik22(c, ds_kaynak)
    if kasa:
        c2_kasa22(veri, [dsy])
    Hz = c2_hazirlik22(veri, c, dsy); sha = c2_sha22_simdi(veri, c)
    s = [f"# CETVEL2 — ÖN KAYIT v2.2 ({_c2_simdi()})", "",
         C2_SURUM22 + ". Bu dosya pozitif kontrol v2.2 koşusundan ÖNCE yazıldı ve git'e işlendi; c2_kapi22 C2_ESIK22 / kod / girdi sha'larını, git "
         "kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Kova sınırları getirisiz havuz dağılımından, güç eğrisi "
         "yalnız FARK yayılımından (ortalama kullanılmaz); hiçbir hücre FARK'ı / p'si bu dosya yazılırken hesaplanmadı.", "",
         f"KASA: açık kesik {kes.date()} (KASA_DURUM.json: mühür {durum.get('muhur_id', '-')}, açılan blok {durum.get('acilan', [])}); veri "
         f"klasörü {v} (= /tmp/kasa/acik); kasa_kapisi V_ABD / V_AVR / V_BIST ve açık DS olay kopyası için geçti.", "",
         f"Kod commit (CETVEL2.py son git kaydı): `{_c2_git_son(C2_YOL['kod'])}`", ""]
    s += [f"- {k}: `{x}`" for k, x in sha.items()]
    s += ["", "## 1. İŞ TANIMI (KART_TUR1_IS_TANIMI.md bölüm 2, AYNEN)", ""]
    try:
        it = open(os.path.join(KOK_C2, "arastirma_cikti", "kart", "KART_TUR1_IS_TANIMI.md"), encoding="utf-8").read()
        m = re.search(r"## 2\. ADIM K1.*?\n(.*?)\n## 3\.", it, flags=re.S)
        s += [m.group(1).strip() if m else "(iş tanımı bölüm 2 bulunamadı)"]
    except OSError as ex:
        raise C2Hata(f"iş tanımı okunamadı: {ex}") from ex
    s += ["", "## 2. v2.2 AYRINTILARI (C2_ESIK22; sha yukarıda; v2.1 C2_ESIK aynen, CETVEL2_ON_KAYIT_v2.1.md)", ""]

    def dz(d, on=""):
        for k, x in d.items():
            if isinstance(x, dict):
                s.append(f"- {on}{k}:"); dz(x, on + "  ")
            else:
                s.append(f"- {on}{k}: {x}")
    dz(C2_ESIK22)
    s21 = {}
    try:
        s21 = json.load(open(_c2_yol("esik", c, "_v2.1"), encoding="utf-8"))["sinir"]
    except (OSError, ValueError, KeyError):
        pass
    s += ["", "## 3. AÇIK VERİDE (giriş 2016-22) SABİTLENEN KOVA SINIRLARI (sayı; cetvel2_esik_v2.2.json; v2.1 sayıları yan yana)", "",
          "| pazar | sürüm | ATRP t1 | ATRP t2 | F15 q1 | F15 q2 | F15 q3 | havuz hisse-gün |", "|---|---|---|---|---|---|---|---|"]
    for p, x in Hz["sinir"].items():
        s.append(f"| {p} | v2.2 | {x['ATRP'][0]:.6f} | {x['ATRP'][1]:.6f} | {x['F15'][0]:.6f} | {x['F15'][1]:.6f} | {x['F15'][2]:.6f} | {x['n_hisse_gun']} |")
        if p in s21:
            y = s21[p]
            s.append(f"| {p} | v2.1 | {y['ATRP'][0]:.6f} | {y['ATRP'][1]:.6f} | {y['F15'][0]:.6f} | {y['F15'][1]:.6f} | {y['F15'][2]:.6f} | {y['n_hisse_gun']} |")
    s += ["", "## 4. GÜÇ EĞRİSİ (cetvel2_guc_v2.2.json; delta +0,02 R_H; sigma(n) = exp(a + b ln n); güç = Phi(delta / sigma - 1,96))", "",
          "| pazar | hücre | H | N (DS ANA, eşli) | sd (olay) | a | b | n = 30 | 100 | 300 | 1000 | 3000 | güç >= 0,80 için en küçük n |",
          "|" + "---|" * 13]
    for p, hh in Hz["egri"].items():
        for h, eh in hh.items():
            for H, e in eh.items():
                gg = [c2_guc(n, e) for n in (30, 100, 300, 1000, 3000)]
                nmin = next((n for n in range(30, 200001, 10) if c2_guc(n, e) >= 0.80), None)
                s.append(f"| {p} | {h} | {H} | {e['N']} | {_c2_s(e['sd'], 4)} | {_c2_s(e['a'], 4)} | {_c2_s(e['b'], 4)} | "
                         + " | ".join(_c2_s(x, 2) for x in gg) + f" | {nmin if nmin else '> 200000'} |")
    s += ["", "Huni (DS ANA olayları, açık kopya; H başına tekil H): " + "; ".join(
        f"{p} H{H}: girdi {v_.get('girdi')}, ölçülen R_H {v_.get('olcum_rh')}, eşli {v_.get('esli')}, son ölçülen giriş {v_.get('son_giris_olculen')}"
        for p, hh in Hz["huni"].items() for H, v_ in hh.items())]
    s += ["", "## 5. PREFIX (K2; cetvel2_prefix_v2.2.json)", ""]
    for p, x in Hz["prefix"].items():
        s.append(f"- {p}: {x['n']} olay, bozuk {x['bozuk']}")
    s += ["", "## 6. R45 KURALI (önceden yazılı)", "", "- " + C2_ESIK22["r45_kurali"],
          "", "## 7. PLASEBO KAPISI (v2.2)", "", "- " + C2_ESIK22["plasebo_iki_yon"],
          "", "## 8. ÖNCEDEN YAZILI SONUÇ KURALI (pozitif kontrol v2.2; her H ayrı)", ""]
    s += [f"- {k}: {x}" for k, x in C2_ESIK22["sonuc_kurali"].items()]
    s += ["", "## 9. B2 PEAD", "", "- " + C2_ESIK22["B"]["pead"],
          "", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "",
          "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    try:
        import IZ_KARNE as IK
        ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    except Exception:   # IZ_KARNE yoksa madde adı yazılmaz; kapı yine kodları okur
        ad = {}
    for k, (y, kn) in C2_KONTROL22.items():
        s.append(f"| {k} | {ad.get(k, k)} | {y} | {kn} |")
    YH._yh_yaz(yol, "\n".join(s) + "\n", "C2 v2.2 ön kayıt")
    return yol


def c2_kapi22(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    c = cikti or C2_YOL["cikti"]; yol = _c2_yol("onkayit", c, C2_E22)
    if not os.path.exists(yol):
        raise C2Hata(f"ön kayıt yok: {yol} (python CETVEL2.py onkayit22)")
    metin = open(yol, encoding="utf-8").read(); simdi = c2_sha22_simdi(veri, c)
    for k, x in simdi.items():
        m = re.search(rf"(?<![A-Z0-9_]){k}:\s*`([0-9a-f]{{64}}|-)`", metin)
        if not m or m.group(1) != x:
            raise C2Hata(f"{k} ön kayıttakiyle aynı değil -> koşu DURDU")
    out: Dict[str, Any] = {"sha": simdi}
    if git:
        try:
            dosyalar = [yol, _c2_yol("esik", c, C2_E22), _c2_yol("guc", c, C2_E22), _c2_yol("prefix", c, C2_E22), C2_YOL["kod"],
                        os.path.join(c, f"c2_ds_olay_acik{C2_E22}.csv.gz")]
            st = subprocess.run(["git", "status", "--porcelain"] + dosyalar, cwd=KOK_C2, capture_output=True, text=True, check=True).stdout.strip()
            lg = subprocess.run(["git", "log", "-1", "--format=%H %cI", "--", yol], cwd=KOK_C2, capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as ex:
            raise C2Hata(f"git denetimi yapılamadı: {ex}") from ex
        if st or not lg:
            raise C2Hata(f"ön kayıt / kod git'e işlenmemiş ya da değişmiş ({st or 'kayıt yok'}) -> koşu DURDU")
        out["git_onkayit"] = lg; out["git_kod"] = _c2_git_son(C2_YOL["kod"])
    if kontrol:
        import IZ_KARNE as IK
        out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
    c2log.info("c2_kapi22 AÇIK (%s)", yol)
    return out


# ---------------------------------------------------------------- A: yapay iz (H başına)
_C2_A22: Dict[Tuple[str, int], Dict[str, Any]] = {}


def c2_a22_hazirla(pazar: str, H: int, veri: Optional[str] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    Pn = c2_panel22_al(pazar, veri, H)
    X, say = c2_olay(c2_ds_olay22(pazar, ds_yol), Pn, tekil_gun=int(H)); X["donem"] = _c2_donem22(X.giris)
    e = c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float))
    X["fark0"] = e["fark"]; X["n_es0"] = e["n_es"]
    return {"Pn": Pn, "X": X, "say": say}


def _c2_a22_isci(is_: Tuple[str, int, int, Any]) -> List[Dict[str, Any]]:
    pazar, H, ti, nk = is_
    G = _C2_A22[(pazar, H)]; Pn, X = G["Pn"], G["X"]; Ea = C2_ESIK22["A"]; idx = Pn["P"]["tarih"]; out = []
    guc = G.get("guc"); ui = C2_ESIK22["ufuklar"].index(H)
    for hi, h in enumerate(C2_HUCRE22):
        havuz = np.flatnonzero((X.donem.to_numpy() == h) & np.isfinite(X.fark0.to_numpy(float)))
        n = int(nk)
        if n < 1 or n > Ea["n_azami_pay"] * len(havuz):
            out.append({"pazar": pazar, "ufuk": H, "tohum": ti, "n_hedef": str(nk), "hucre": h, "taban": "-", "delta": np.nan, "n": 0}); continue
        rng = np.random.default_rng([int(Ea["tohum"]), int(ti), Ea["n"].index(nk), C2_PAZAR.index(pazar), hi, ui])
        sec = np.sort(rng.choice(havuz, size=n, replace=False))
        d0 = X.d.to_numpy(np.int64)[sec]; j0 = X.j.to_numpy(np.int64)[sec]; r0 = X.r15.to_numpy(float)[sec]
        rd, rj = c2_rastgele(Pn, d0, rng); rr = Pn["R15"][rd, rj]
        egri = _c2_egri22_al(pazar, h, H, guc) if guc is not None else None
        for tb, (dd, jj, rv) in (("DS", (d0, j0, r0)), ("RAST", (rd, rj, rr))):
            for di, de in enumerate(Ea["delta"]):
                x = (1.0 + rv) * (1.0 + float(de)) - 1.0
                e = c2_es(Pn, dd, jj, x, dd, jj)
                tek = 400000 + ui * 100000 + ti * 1000 + Ea["n"].index(nk) * 100 + hi * 50 + (0 if tb == "DS" else 25) + di
                c = c2_hucre(x, e["es_r15"], e["sira"], idx[dd], "+", tohum_ek=tek, egri=egri, l3o_neg=False)
                out.append({"pazar": pazar, "ufuk": H, "tohum": ti, "n_hedef": str(nk), "hucre": h, "taban": tb, "delta": float(de), "n": c["n"],
                            "fark": c["fark"], "med": c["med"], "sira": c["sira"], "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"],
                            "l3o": c["l3o"], "p": c["p"], "guc": c["guc"], "yakala": bool(c["yakala_p"]), "tutar": bool(c["tutar_p"]),
                            "yakala_p05": bool(c["yakala_p"] and np.isfinite(c["p"]) and c["p"] < 0.05)})
    return out


def _c2_havuz_kos(f: Callable, isler: List[Any], islem: int) -> List[Any]:
    if islem > 1 and len(isler) > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as hv:
            return hv.map(f, isler, chunksize=1)
    return [f(x) for x in isler]


def c2_a22_kos(islem: int = 1, veri: Optional[str] = None, guc: Optional[Dict[str, Any]] = None, tohum_sayi: Optional[int] = None,
               pazarlar: Optional[List[str]] = None, ufuklar: Optional[List[int]] = None, ds_yol: Optional[str] = None) -> Dict[str, Any]:
    Ea = C2_ESIK22["A"]; pazarlar = pazarlar or Ea["pazar"]; ufuklar = [int(u) for u in (ufuklar or C2_ESIK22["ufuklar"])]
    T = int(tohum_sayi or Ea["tohum_sayi"]); say: Dict[str, Any] = {}
    for p in pazarlar:
        for H in ufuklar:
            G = c2_a22_hazirla(p, H, veri, ds_yol); G["guc"] = guc; _C2_A22[(p, H)] = G; X = G["X"]
            say[f"{p}_{H}"] = {**{k: v for k, v in G["say"].items() if k != "donem"},
                               "havuz": {h: int(((X.donem == h) & np.isfinite(X.fark0)).sum()) for h in C2_HUCRE22},
                               "essiz": {h: int(((X.donem == h) & np.isfinite(X.r15) & ~np.isfinite(X.fark0)).sum()) for h in C2_HUCRE22},
                               "son_giris": str(pd.Timestamp(X.giris[np.isfinite(X.r15)].max()).date()) if np.isfinite(X.r15).any() else "-"}
    isler = [(p, H, ti, nk) for p in pazarlar for H in ufuklar for ti in range(T) for nk in Ea["n"]]
    t0 = time.time()
    R = _c2_havuz_kos(_c2_a22_isci, isler, islem)
    S = pd.DataFrame([r for x in R for r in x])
    c2log.info("A v2.2 ızgara: %d satır (%.0f sn)", len(S), time.time() - t0)
    return {"satir": S, "say": say}


def c2_a22_ozet(S: pd.DataFrame) -> Dict[str, Any]:
    S = S.copy()
    for c in ("fark", "med", "sira", "boot_alt", "boot_ust", "l3o", "p", "guc", "yakala", "tutar", "yakala_p05"):
        if c not in S.columns:      # hiçbir hücre ölçülemediyse (n > 2/3 havuz) sütun yok
            S[c] = np.nan if c not in ("yakala", "tutar", "yakala_p05") else False
    g = S[S.n > 0].copy()
    tab = g.groupby(["ufuk", "pazar", "hucre", "taban", "n_hedef", "delta"]).agg(
        yakala=("yakala", "mean"), tutar=("tutar", "mean"), yakala_p05=("yakala_p05", "mean"), n=("n", "mean"), fark=("fark", "mean"),
        fark_sd=("fark", "std"), guc=("guc", "mean"), tohum=("tohum", "count")).reset_index()
    dort = []
    for (H, tb, nk, de), x in g[g.pazar.isin(C2_ESIK22["A"]["karar_pazar"])].groupby(["ufuk", "taban", "n_hedef", "delta"]):
        k = x.groupby("tohum").agg(hep=("yakala", "all"), say=("yakala", "size"))
        k = k[k.say == 4]
        dort.append({"ufuk": int(H), "taban": tb, "n_hedef": nk, "delta": de, "dort_hucre": float(k.hep.mean()) if len(k) else np.nan,
                     "tohum": int(len(k))})
    return {"tablo": tab.to_dict("records"), "dort": dort}


# ---------------------------------------------------------------- B: momentum (H başına), C: plasebo kapısı (H başına)
_C2_B22: Dict[str, Any] = {}


def _c2_b22_isci(is_: Tuple[str, int]) -> Dict[str, Any]:
    pazar, H = is_
    Eb = C2_ESIK22["B"]; ev = _C2_B22["olay"][pazar]; guc = _C2_B22.get("guc")
    hip = {k: {"bayrak": f"F_{v[0]}", "yon": v[1]} for k, v in Eb["hipotez"].items()}
    R = c2_olc(ev.assign(pazar=pazar)[["pazar", "sembol", "tarih", "F_U", "F_A"]], hip, veri=_C2_B22.get("veri"), plasebo=True, bilgi=False,
               m_bh=2, tohum0=10 + C2_PAZAR.index(pazar) * 3 + C2_ESIK22["ufuklar"].index(H), guc=guc,
               karar=Eb["karar_pazar"] if pazar in Eb["karar_pazar"] else [pazar], ufuk=H)
    return {"hucre": R["hucre"].assign(bilgi=pazar not in Eb["karar_pazar"]), "etiket": R["etiket"].assign(pazar=pazar),
            "satir": R["satir"].assign(kod="B1"), "say": {f"B1_{pazar}_{H}": R["say"][pazar]}}


def c2_b22_kos(islem: int = 1, veri: Optional[str] = None, guc: Optional[Dict[str, Any]] = None,
               ufuklar: Optional[List[int]] = None) -> Dict[str, Any]:
    Eb = C2_ESIK22["B"]; ufuklar = [int(u) for u in (ufuklar or C2_ESIK22["ufuklar"])]
    _C2_B22.clear(); _C2_B22.update({"olay": {}, "guc": guc, "veri": veri}); say: Dict[str, Any] = {"pead": Eb["pead"]}
    for p in Eb["pazar"]:
        O, sy = c2_mom22(p, veri); _C2_B22["olay"][p] = O; say[f"mom_{p}"] = sy
        for H in ufuklar:
            c2_panel22_al(p, veri, H)        # çatallanmadan önce önbellekte
    R = _c2_havuz_kos(_c2_b22_isci, [(p, H) for p in Eb["pazar"] for H in ufuklar], islem)
    out = {"hucre": pd.concat([r["hucre"] for r in R], ignore_index=True), "etiket": pd.concat([r["etiket"] for r in R], ignore_index=True),
           "satir": pd.concat([r["satir"] for r in R], ignore_index=True), "say": say}
    for r in R:
        out["say"].update(r["say"])
    return out


def _c2_c22_isci(is_: Tuple[str, int, int, str]) -> Dict[str, Any]:
    pazar, H, hi, h = is_
    Ec = C2_ESIK22["C"]; G = _C2_A22[(pazar, H)]; Pn, X = G["Pn"], G["X"]; P = Pn["P"]; idx = P["tarih"]; pi = C2_PAZAR.index(pazar)
    ui = C2_ESIK22["ufuklar"].index(H); guc = G.get("guc")
    m = (X.donem.to_numpy() == h) & np.isfinite(X.fark0.to_numpy(float)); d_all = X.d.to_numpy(np.int64)[m]
    egri = _c2_egri22_al(pazar, h, H, guc) if guc is not None else None
    sat = []
    for ni, nk in enumerate(Ec["n"]):
        if nk == "tam":
            dsec = d_all
        else:
            if int(nk) > len(d_all):
                continue
            rng = np.random.default_rng([int(Ec["tohum"]), pi, hi, ni, ui]); dsec = np.sort(rng.choice(d_all, size=int(nk), replace=False))
        if not len(dsec):
            continue
        pl = c2_plasebo(Pn, dsec, "?", egri, tohum_ek=800000 + ui * 10000 + pi * 100 + hi * 10 + ni, iki_yon_ayri=True)
        sat.append({"pazar": pazar, "ufuk": H, "hucre": h, "n_hedef": str(nk), "n": pl["n_ort"], "fark_ort": pl["fark_ort"], "fark_sd": pl["fark_sd"],
                    "tutar_pay_arti": pl["tutar_pay_arti"], "tutar_pay_eksi": pl["tutar_pay_eksi"], "tutar_pay_iki": pl["tutar_pay"],
                    "yakala_pay": pl["yakala_pay"], "gecti_arti": pl["gecti_arti"], "gecti_eksi": pl["gecti_eksi"], "gecti": pl["gecti"],
                    "karar": pazar in C2_KARAR})
    gm = (pd.Series(_c2_donem22(idx)) == h).to_numpy()
    hv = (P["ok"] & (P["H"] >= 0))[gm].sum(1); rv = ((Pn["KV"] >= 0) & np.isfinite(Pn["R15"]))[gm].sum(1)
    dolu = np.array([len(np.unique(Pn["KV"][dd][(Pn["KV"][dd] >= 0) & np.isfinite(Pn["R15"][dd])])) for dd in np.flatnonzero(gm)])
    mr = (X.donem.to_numpy() == h) & np.isfinite(X.r15.to_numpy(float))
    tani = {"pazar": pazar, "ufuk": H, "hucre": h, "gun": int(gm.sum()), "havuz_gun_medyan": float(np.median(hv)) if len(hv) else np.nan,
            "rh_kova_gun_medyan": float(np.median(rv)) if len(rv) else np.nan, "dolu_kova_medyan": float(np.median(dolu)) if len(dolu) else np.nan,
            "olay_rh": int(mr.sum()), "essiz_pay": float((~np.isfinite(X.fark0.to_numpy(float)[mr])).mean()) if mr.any() else np.nan,
            "n_es_medyan": float(np.nanmedian(X.n_es0.to_numpy(float)[mr])) if mr.any() else np.nan,
            "fark0_ort": float(np.nanmean(X.fark0.to_numpy(float)[mr])) if mr.any() else np.nan}
    return {"satir": sat, "tani": tani}


def c2_c22_kos(islem: int = 1, ufuklar: Optional[List[int]] = None) -> Dict[str, Any]:
    ufuklar = [int(u) for u in (ufuklar or C2_ESIK22["ufuklar"])]
    isler = [(p, H, hi, h) for p in C2_PAZAR for H in ufuklar for hi, h in enumerate(C2_HUCRE22) if (p, H) in _C2_A22]
    R = _c2_havuz_kos(_c2_c22_isci, isler, islem)
    return {"satir": pd.DataFrame([s for r in R for s in r["satir"]]), "tani": pd.DataFrame([r["tani"] for r in R])}


# ---------------------------------------------------------------- sonuç, R45, yeniden üretim, v2.1 regresyonu
def c2_sonuc22(J: Dict[str, Any]) -> Dict[str, Any]:
    """Önceden yazılı sonuç kuralı (C2_ESIK22['sonuc_kurali']) her H için."""
    Bh = pd.DataFrame(J["B"]["hucre"]); Ct = pd.DataFrame(J["C"]["satir"]); At = pd.DataFrame(J["A"]["ozet"]["tablo"])
    for k in ("fark", "boot_alt", "boot_ust"):
        Bh[k] = pd.to_numeric(Bh[k], errors="coerce")
    for k in ("yakala", "delta", "tohum", "ufuk"):
        At[k] = pd.to_numeric(At[k], errors="coerce") if k in At.columns else np.nan
    for k in ("pazar", "hucre", "taban", "n_hedef"):
        if k not in At.columns:
            At[k] = ""
    out = {}
    for H in [int(u) for u in C2_ESIK22["ufuklar"]]:
        kusur, eksik = [], []

        def h(kod, hc):
            q = Bh[(Bh.kod == kod) & (Bh.pazar == "ABD") & (Bh.hucre == hc) & (Bh.ufuk == H)]
            return q.iloc[0] if len(q) else None
        for hc in C2_HUCRE22:
            q = h("B1A", hc)
            if q is not None and q["fark"] > 0 and q["boot_alt"] > 0:
                kusur.append(f"momentum alt onda ABD {hc} R{H} FARK > 0 ve boot alt > 0 ({_c2_y(q['fark'], 2)})")
            c = Ct[(Ct.pazar == "ABD") & (Ct.hucre == hc) & (Ct.n_hedef == "tam") & (Ct.ufuk == H)]
            if len(c) and not bool(c.iloc[0]["gecti"]):
                kusur.append(f"plasebo kapısı ABD {hc} R{H} (tam n) düştü")
        r0 = At[(At.ufuk == H) & (At.taban == "RAST") & (At.delta == 0.0) & At.pazar.isin(C2_KARAR) & At.n_hedef.isin(["100", "300", "1000"])]
        for (p_, hc_), x_ in r0.groupby(["pazar", "hucre"]):
            bp = float((x_.yakala * x_.tohum).sum() / x_.tohum.sum()) if x_.tohum.sum() > 0 else np.nan
            if np.isfinite(bp) and bp > 0.10:
                kusur.append(f"A RAST delta 0 yakalama {p_} {hc_} R{H} (n >= 100 birleşik): %{100 * bp:.1f}")
        a2 = At[(At.ufuk == H) & (At.taban == "RAST") & np.isclose(At.delta, 0.02) & At.pazar.isin(C2_KARAR)]
        if not all(((a2.pazar == p) & (a2.hucre == hc) & (a2.yakala >= 0.80)).any() for p in C2_KARAR for hc in C2_HUCRE22):
            eksik.append(f"A RAST delta +%2 R{H}: dört karar hücresinin birinde hiçbir n'de >= %80 yakalama yok")
        q = [h("B1U", hc) for hc in C2_HUCRE22]
        if not (all(x is not None and x["fark"] > 0 for x in q) and any(x is not None and x["boot_alt"] > 0 for x in q)):
            eksik.append(f"B1U ABD R{H}: iki dönemde FARK > 0 ve birinde boot alt > 0 değil")
        out[str(H)] = {"karar": "HAYIR (KUSUR)" if kusur else ("EVET" if not eksik else "KISMEN"), "kusur": kusur, "eksik": eksik}
    return out


def c2_r45(J: Dict[str, Any]) -> Dict[str, Any]:
    """R45 KURALI (C2_ESIK22['r45_kurali'])."""
    Bh = pd.DataFrame(J["B"]["hucre"]); Ct = pd.DataFrame(J["C"]["satir"])
    Bh["boot_alt"] = pd.to_numeric(Bh["boot_alt"], errors="coerce")
    c45 = Ct[(Ct.ufuk == 45) & (Ct.n_hedef == "tam") & Ct.pazar.isin(["ABD", "AVR"])]
    i_det = {f"{r['pazar']} {r['hucre']}": bool(r["gecti"]) for r in c45.to_dict("records")}
    i_ok = len(i_det) == 4 and all(i_det.values())

    def ba(H, hc):
        q = Bh[(Bh.kod == "B1U") & (Bh.pazar == "ABD") & (Bh.hucre == hc) & (Bh.ufuk == H)]
        return float(q.iloc[0]["boot_alt"]) if len(q) else float("nan")
    b45 = {hc: ba(45, hc) for hc in C2_HUCRE22}; b30 = {hc: ba(30, hc) for hc in C2_HUCRE22}
    ii_ok = all(np.isfinite(v) and v > 0 for v in b45.values()) and any(not (np.isfinite(v) and v > 0) for v in b30.values())
    karar = "KARAR" if (i_ok and ii_ok) else "BİLGİ"
    ger = (f"(i) plasebo H45 ABD / AVR tam n: {i_det} -> {'TUTTU' if i_ok else 'TUTMADI'}; (ii) B1U ABD boot alt R45 "
           f"{ {k: round(v, 5) for k, v in b45.items()} }, R30 { {k: round(v, 5) for k, v in b30.items()} } -> {'TUTTU' if ii_ok else 'TUTMADI'}")
    return {"karar": karar, "i": i_ok, "ii": ii_ok, "i_detay": i_det, "b45": b45, "b30": b30, "gerekce": ger}


def c2_yeniden22(Bs: pd.DataFrame, Hc: pd.DataFrame, veri: Optional[str] = None) -> Dict[str, Any]:
    """(1) üç hücre satır dosyasından düz pandas; (2) her H için 20 B1 ABD olayının R_H'si ham veriden düz döngü; (3) 5 B1U ABD olayının (H 30)
    eş ortalaması bütün evrende düz döngü (kova elle)."""
    Y = C2_ESIK22["yeniden_uretim"]; out: Dict[str, Any] = {"hucre": [], "rh_bozuk": [], "rh_n": 0, "es_bozuk": [], "es_n": 0}
    for kod, pz, hc, H in Y["hucre"]:
        g = Bs[(Bs.pazar == pz) & (Bs.ufuk == H) & (Bs.donem == hc)]
        f = g[f"fark_{kod}"].dropna(); sr = g.loc[f.index, f"sira_{kod}"]
        q = Hc[(Hc.kod == kod) & (Hc.pazar == pz) & (Hc.hucre == hc) & (Hc.ufuk == H)].iloc[0]
        out["hucre"].append({"kod": kod, "pazar": pz, "hucre": hc, "ufuk": H, "n_duz": int(len(f)), "fark_duz": float(f.mean()),
                             "sira_duz": float(sr.mean()), "n": int(q["n"]), "fark": float(q["fark"]), "sira": float(q["sira"]),
                             "esit": bool(len(f) == int(q["n"]) and abs(f.mean() - q["fark"]) < 1e-12 and abs(sr.mean() - q["sira"]) < 1e-12)})
    rng = np.random.default_rng(int(Y["tohum"]))
    Pb = c2_panel22_al("ABD", veri, None); V = Pb["Vd"]["V"]; idx = Pb["P"]["tarih"]
    for H in [int(u) for u in C2_ESIK22["ufuklar"]]:
        g = Bs[(Bs.pazar == "ABD") & (Bs.ufuk == H) & np.isfinite(Bs.r15)].reset_index(drop=True)
        Rz = int(C2_ESIK22["pencere_kat"]) * H
        for i in rng.choice(len(g), size=min(int(Y["elle_rh"]), len(g)), replace=False):
            r = g.iloc[int(i)]; df = V[r.sembol]; ix = list(df.index); k = ix.index(pd.Timestamp(r.giris))
            if k + H - 1 < len(ix) and idx.get_loc(ix[k + H - 1]) - idx.get_loc(ix[k]) <= Rz - 1:
                v = df.Close.iloc[k + H - 1] / df.Open.iloc[k] - 1
            else:
                v = float("nan")
            out["rh_n"] += 1
            if not np.isclose(v, r.r15, rtol=1e-10, atol=1e-12, equal_nan=True):
                out["rh_bozuk"].append({"sembol": r.sembol, "giris": str(r.giris), "ufuk": H, "duz": v, "kod": r.r15})
    H = int(Y["elle_es_ufuk"]); Rz = int(C2_ESIK22["pencere_kat"]) * H
    Pn = c2_panel22_al("ABD", veri, H); P = Pn["P"]; sn = P["sembol"]; sin = Pn["sinir"]; kf = int(C2_ESIK["kova"]["f15_gun"])
    g = Bs[(Bs.pazar == "ABD") & (Bs.ufuk == H)]
    gU = g[np.isfinite(g["fark_B1U"])].reset_index(drop=True)
    for i in rng.choice(len(gU), size=min(int(Y["elle_es"]), len(gU)), replace=False):
        r = gU.iloc[int(i)]; gd = pd.Timestamp(r.giris); dd = idx.get_loc(gd)
        ayni_gun_U = set(g[(pd.to_datetime(g.giris) == gd) & (g.F_U == 1)].sembol)

        def kova_elle(s):
            df = V[s]
            if gd not in df.index:
                return -1, np.nan
            jj = P["kol"][s]
            if not (P["ok"][dd, jj] and P["H"][dd, jj] >= 0):
                return -1, np.nan
            once = df[df.index < gd]
            if len(once) < 15:
                return -1, np.nan
            H_, L_, C_ = once.High.to_numpy(float), once.Low.to_numpy(float), once.Close.to_numpy(float)
            tr = [H_[0] - L_[0]] + [max(H_[t], C_[t - 1]) - min(L_[t], C_[t - 1]) for t in range(1, len(C_))]
            atrp = float(np.mean(tr[-14:]) / C_[-1])
            if len(C_) < kf:
                return -1, np.nan
            w = C_[-kf:]; f15 = (C_[-1] - w.min()) / (w.max() - w.min()) if w.max() > w.min() else np.nan
            if not np.isfinite(f15):
                return -1, np.nan
            at = 0 if atrp <= sin["ATRP"][0] else (1 if atrp <= sin["ATRP"][1] else 2)
            fq = 0 if f15 <= sin["F15"][0] else (1 if f15 <= sin["F15"][1] else (2 if f15 <= sin["F15"][2] else 3))
            ix = list(df.index); k_ = ix.index(gd)
            if k_ + H - 1 >= len(ix) or idx.get_loc(ix[k_ + H - 1]) - idx.get_loc(ix[k_]) > Rz - 1:
                return -1, np.nan
            return at * 12 + int(P["H"][dd, jj] % 3) * 4 + fq, float(df.Close.iloc[k_ + H - 1] / df.Open.iloc[k_] - 1)
        k0, _ = kova_elle(r.sembol); vals = []
        for s in sn:
            if s == r.sembol or s in ayni_gun_U:
                continue
            k1, v1 = kova_elle(s)
            if k1 == k0 and k1 >= 0 and np.isfinite(v1):
                vals.append(v1)
        es = float(np.mean(vals)) if len(vals) >= C2_ESIK["es_min"] else float("nan")
        out["es_n"] += 1
        if not (k0 == int(r.kova) and np.isclose(es, r["es_r15_B1U"], rtol=1e-6, atol=1e-10, equal_nan=True) and len(vals) == int(r["n_es_B1U"])):
            out["es_bozuk"].append({"sembol": r.sembol, "giris": str(r.giris), "kova_elle": k0, "kova": int(r.kova), "es_duz": es,
                                    "es_kod": float(r["es_r15_B1U"]), "n_duz": len(vals), "n_kod": int(r["n_es_B1U"])})
    out["tuttu"] = bool(all(h["esit"] for h in out["hucre"]) and not out["rh_bozuk"] and not out["es_bozuk"])
    return out


def c2_regresyon21(veri: Optional[str] = None, pk_b: Optional[str] = None, b21: Optional[str] = None, esik21: Optional[str] = None,
                   giris_son: Optional[str] = None) -> Dict[str, Any]:
    """v2.1 çağrısı (ufuk yok) açık veride = c2_b_olay_v2.1 satırları (giriş <= giris_son) BİREBİR mi. Kova sınırları v2.1 eşik dosyasından."""
    Rg = C2_ESIK22["regresyon_v21"]; gs = pd.Timestamp(giris_son or Rg["giris_son"]); kes = pd.Timestamp(C2_ESIK22["veri"]["kesik_tarih"])
    pk_b = pk_b or C2_YOL["pk_b"]; b21 = b21 or _c2_yol("b_satir", None, "_v2.1"); esik21 = esik21 or _c2_yol("esik", None, "_v2.1")
    for y in (pk_b, b21, esik21):
        if not os.path.exists(y):
            raise C2Hata(f"regresyon girdisi yok: {y}")
    sin21 = json.load(open(esik21, encoding="utf-8"))["sinir"]
    PB = pd.read_csv(pk_b, usecols=["kod", "pazar", "sembol", "tarih", "giris", "U", "A"], parse_dates=["tarih", "giris"])
    PB = PB[(PB.kod == "B1") & (PB.tarih <= kes)]
    B21 = pd.read_csv(b21, parse_dates=["tarih", "giris"])
    kol = ["giris", "kova", "E0", "r15", "es_r15_B1U", "n_es_B1U", "sira_B1U", "fark_B1U", "es_r15_B1A", "n_es_B1A", "sira_B1A", "fark_B1A"]
    out: Dict[str, Any] = {"olay": {}, "hucre": [], "giris_son": str(gs.date())}
    yeni: Dict[str, pd.DataFrame] = {}
    eski_pn = dict(_C2_PN)
    try:
        for pazar in ("ABD", "AVR"):
            _C2_PN.pop(pazar, None)
            c2_panel_al(pazar, veri, sin21[pazar])
            g = PB[PB.pazar == pazar].copy(); g["F_U"] = g.U.astype(bool).astype(float); g["F_A"] = g.A.astype(bool).astype(float)
            R = c2_olc(g.assign(pazar=pazar)[["pazar", "sembol", "tarih", "F_U", "F_A", "giris"]].rename(columns={"giris": "pk_giris"}),
                       {"B1U": {"bayrak": "F_U", "yon": "+"}, "B1A": {"bayrak": "F_A", "yon": "-"}}, veri=veri, plasebo=False, bilgi=False,
                       m_bh=2, guc={"egri": {}}, karar=[pazar])
            S = R["satir"]; yeni[pazar] = S
            O = B21[(B21.kod == "B1") & (B21.pazar == pazar) & (B21.giris <= gs)]
            M = O[["sembol", "tarih"] + kol].merge(S[["sembol", "tarih"] + kol], on=["sembol", "tarih"], how="left", suffixes=("_21", "_yeni"),
                                                     validate="one_to_one")
            res = {"olay_21": int(len(O)), "eslesen": int(M["E0_yeni"].notna().sum()), "kolon": {}}
            for c in kol:
                a, b = M[f"{c}_21"], M[f"{c}_yeni"]
                if c == "giris":
                    ok = (pd.to_datetime(a) == pd.to_datetime(b)).to_numpy()
                else:
                    a = a.to_numpy(float); b = b.to_numpy(float)
                    ok = np.isclose(a, b, rtol=1e-12, atol=0, equal_nan=True)
                res["kolon"][c] = {"esit": int(ok.sum()), "farkli": int((~ok).sum())}
            res["tuttu"] = bool(res["eslesen"] == res["olay_21"] and all(v["farkli"] == 0 for v in res["kolon"].values()))
            out["olay"][pazar] = res
    finally:
        _C2_PN.clear(); _C2_PN.update(eski_pn)
    for kod, pz in Rg["hucre"]:
        O = B21[(B21.kod == "B1") & (B21.pazar == pz) & (B21.giris <= gs) & (B21.donem == "egitim")]
        S = yeni[pz]; S = S[(S.giris <= gs) & (S.donem == "egitim")]
        f0 = O[f"fark_{kod}"].dropna(); s0 = O.loc[f0.index, f"sira_{kod}"]
        f1 = S[f"fark_{kod}"].dropna(); s1 = S.loc[f1.index, f"sira_{kod}"]
        out["hucre"].append({"kod": kod, "pazar": pz, "n_21": int(len(f0)), "fark_21": float(f0.mean()), "sira_21": float(s0.mean()),
                             "n_yeni": int(len(f1)), "fark_yeni": float(f1.mean()), "sira_yeni": float(s1.mean()),
                             "esit": bool(len(f0) == len(f1) and abs(f0.mean() - f1.mean()) < 1e-12 and abs(s0.mean() - s1.mean()) < 1e-12)})
    out["tuttu"] = bool(all(v["tuttu"] for v in out["olay"].values()) and all(h["esit"] for h in out["hucre"]))
    return out


# ---------------------------------------------------------------- koşu ve rapor
def c2_kasa22(veri: Optional[str] = None, dosyalar: Optional[List[str]] = None) -> Dict[str, Any]:
    """Ölçümden önce KASA kapısı (V_* + verilen dosyalar); açık kesik C2_ESIK22 ile aynı olmalı."""
    import KASA as _KS
    _c2_kesik22()
    v = veri or C2_YOL["veri"]
    try:
        return _KS.kasa_kapisi([os.path.join(v, f"V_{p}.pkl") for p in C2_PAZAR] + list(dosyalar or []))
    except _KS.KasaHata as ex:
        raise C2Hata(f"KASA kapısı KAPALI: {ex}") from ex


def c2_kos22(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True, kontrol: bool = True, kasa: bool = True,
             tohum_sayi: Optional[int] = None, regresyon: bool = True) -> Dict[str, Any]:
    c = cikti or C2_YOL["cikti"]; t0 = time.time()
    if os.path.exists(_c2_yol("json", c, C2_E22)):
        raise C2Hata(f"sonuç zaten var: {_c2_yol('json', c, C2_E22)} (ikinci koşu DURUR)")
    kapi = c2_kapi22(c, veri, git, kontrol); bas = _c2_simdi()
    dsy = os.path.join(c, f"c2_ds_olay_acik{C2_E22}.csv.gz")
    kk = c2_kasa22(veri, [dsy]) if kasa else {"not": "kasa kapısı atlandı (test)"}
    guc = json.load(open(_c2_yol("guc", c, C2_E22), encoding="utf-8")); esik = json.load(open(_c2_yol("esik", c, C2_E22), encoding="utf-8"))
    for p in C2_PAZAR:
        c2_panel22_al(p, veri, None, esik["sinir"][p])
        for H in C2_ESIK22["ufuklar"]:
            c2_panel22_al(p, veri, H)
    J: Dict[str, Any] = {"surum": C2_SURUM22, "kapi": kapi, "kasa": kk, "baslangic": bas}
    Ra = c2_a22_kos(islem, veri, guc, tohum_sayi, ds_yol=dsy)
    Ra["satir"].to_csv(_c2_yol("a_satir", c, C2_E22), index=False, compression={"method": "gzip", "mtime": 0})
    J["A"] = {"say": Ra["say"], "ozet": c2_a22_ozet(Ra["satir"])}
    Rc = c2_c22_kos(islem)
    Rc["satir"].to_csv(_c2_yol("c_satir", c, C2_E22), index=False)
    J["C"] = {"satir": Rc["satir"], "tani": Rc["tani"]}
    Rb = c2_b22_kos(islem, veri, guc)
    Rb["satir"].to_csv(_c2_yol("b_satir", c, C2_E22), index=False, compression={"method": "gzip", "mtime": 0})
    J["B"] = {"hucre": Rb["hucre"], "etiket": Rb["etiket"], "say": Rb["say"]}
    Bs = pd.read_csv(_c2_yol("b_satir", c, C2_E22), parse_dates=["giris", "tarih"])
    J["yeniden"] = c2_yeniden22(Bs, Rb["hucre"], veri)
    J["regresyon21"] = c2_regresyon21(veri) if regresyon else {"tuttu": True, "not": "atlandı (test)"}
    Jj = _c2_jsonla(J)
    J["sonuc"] = c2_sonuc22(Jj); J["r45"] = c2_r45(Jj)
    import KASA as _KS
    J["en_gec"] = {}
    for ad in ("b_satir",):
        t = _KS.ks_en_gec_tarih(_c2_yol(ad, c, C2_E22)); J["en_gec"][os.path.basename(_c2_yol(ad, c, C2_E22))] = str(t.date()) if t is not None else "-"
    t = _KS.ks_en_gec_tarih(dsy); J["en_gec"][os.path.basename(dsy)] = str(t.date()) if t is not None else "-"
    J["en_gec"]["olculen_son_giris"] = {str(H): str(pd.Timestamp(Bs[(Bs.ufuk == H) & np.isfinite(Bs.r15)].giris.max()).date())
                                        for H in C2_ESIK22["ufuklar"] if ((Bs.ufuk == H) & np.isfinite(Bs.r15)).any()}
    kes = pd.Timestamp(C2_ESIK22["veri"]["kesik_tarih"])
    asan = [k for k, v in J["en_gec"].items() if isinstance(v, str) and v != "-" and pd.Timestamp(v) > kes]
    J["bitis"] = _c2_simdi(); J["sure_sn"] = round(time.time() - t0, 1)
    YH._yh_yaz(_c2_yol("json", c, C2_E22), json.dumps(_c2_jsonla(J), ensure_ascii=False, indent=1, default=YH._yh_json), "C2 v2.2 json")
    J["rapor"] = c2_rapor22(c)
    if asan:
        raise C2Hata(f"KESİK AŞIMI çıktı dosyasında: {asan}")
    if not J["yeniden"]["tuttu"]:
        raise C2Hata(f"yeniden üretim TUTMADI: {J['yeniden']}")
    if not J["regresyon21"]["tuttu"]:
        raise C2Hata(f"v2.1 regresyonu TUTMADI: {J['regresyon21']}")
    return J


def c2_rapor22(cikti: Optional[str] = None) -> str:
    c = cikti or C2_YOL["cikti"]; J = json.load(open(_c2_yol("json", c, C2_E22), encoding="utf-8"))
    on = _c2_yol("onkayit", c, C2_E22); g = J["kapi"].get("git_onkayit", "-")
    U = [int(u) for u in C2_ESIK22["ufuklar"]]
    s = [f"# CETVEL2 — POZİTİF KONTROL v2.2 ({J['bitis']})", "",
         f"{J['surum']}. Ön kayıt {os.path.basename(on)} (git {g}); kod git {J['kapi'].get('git_kod', '-')}; koşu {J['baslangic']} .. {J['bitis']} "
         f"({J['sure_sn']} sn). R_H = H. geçerli bar kapanışı / giriş açılışı - 1 (stop yok); FARK = R_H - konum eşli eş ortalaması (aynı gün, aynı "
         "ATRP x likidite x F15 kovası, bütün evren, en az 5 eş); puan = yüzde puan getiri. Hücre = pazar x dönem (d1619 = giriş 2016-19, d2022 = "
         "2020-22). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma). Veri yalnız KASA açık kısmı.", "",
         f"KASA: kesik {J['kasa'].get('kesik', '-')}; kapı dosyaları en geç: {J['kasa'].get('dosya', {})}. Çıktı en geç tarihleri: {J['en_gec']}.", "",
         "## 0. SONUÇ (önceden yazılı kural, H başına) ve R45 KARARI", "", "| H | sonuç | KUSUR | eksik |", "|---|---|---|---|"]
    for H in U:
        r = J["sonuc"][str(H)]
        s.append(f"| {H} | **{r['karar']}** | {'; '.join(r['kusur']) or '-'} | {'; '.join(r['eksik']) or '-'} |")
    s += ["", f"**R45: {J['r45']['karar']}** — {J['r45']['gerekce']}", ""]
    T = pd.DataFrame(J["A"]["ozet"]["tablo"])
    s += ["## 1. A — YAPAY İZ: yakalama payı (20 tohum; yakalama = n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0; güç hariç)", "",
          "Sürüklenme (1 + R_H)(1 + delta) - 1. Taban RAST = aynı günlerde rastgele havuz hissesi (delta 0 = saf plasebo); DS = seçilen DS ANA "
          "olayları. Hücre: yakalama payı (güç dahil TUTAR payı) / ortalama ölçülen n / ortalama FARK (puan)."]
    nk_sira = [str(n) for n in C2_ESIK22["A"]["n"]]
    for H in U:
        for p in C2_ESIK22["A"]["pazar"]:
            for h in C2_HUCRE22:
                x = T[(T.ufuk == H) & (T.pazar == p) & (T.hucre == h) & (T.taban == "RAST")]
                if not len(x):
                    continue
                hv = J["A"]["say"].get(f"{p}_{H}", {}).get("havuz", {}).get(h, "-")
                s += ["", f"**R{H} RAST — {p} {h}** (havuz {hv})", "", "| n | " + " | ".join(
                    f"delta {'+' if d else ''}{int(round(100 * d))}%" for d in C2_ESIK22["A"]["delta"]) + " |", "|---|" + "---|" * len(C2_ESIK22["A"]["delta"])]
                for nk in nk_sira:
                    row = [nk]
                    for de in C2_ESIK22["A"]["delta"]:
                        q = x[(x.n_hedef.astype(str) == nk) & np.isclose(x.delta, de)]
                        row.append("-" if not len(q) else f"**%{100 * q.iloc[0].yakala:.0f}** (%{100 * q.iloc[0].tutar:.0f}) / "
                                                          f"{q.iloc[0].n:.0f} / {_c2_y(q.iloc[0].fark, 2)}")
                    s.append("| " + " | ".join(row) + " |")
    s += ["", "En küçük (delta, n) ile >= %80 yakalama (RAST tabanı), H başına:", ""]
    for H in U:
        for p in C2_ESIK22["A"]["pazar"]:
            for h in C2_HUCRE22:
                x = T[(T.ufuk == H) & (T.pazar == p) & (T.hucre == h) & (T.taban == "RAST") & (T.yakala >= 0.80) & (T.delta > 0)]
                if len(x):
                    x = x.assign(nn=x.n.astype(float))
                    s.append(f"- R{H} {p} {h}: " + "; ".join(f"delta +%{100 * de:.0f} için n >= {x[np.isclose(x.delta, de)].nn.min():.0f}"
                                                            for de in sorted(x.delta.unique())))
                else:
                    s.append(f"- R{H} {p} {h}: hiçbir (delta, n)'de >= %80 yok")
    s += ["", "DS tabanı (seçilen DS ANA olaylarının kendi FARK'ı; delta 0 ve +%2, n 300): " + "; ".join(
        f"R{H} {p} {h}: d0 %{100 * q0.iloc[0].yakala:.0f} ({_c2_y(q0.iloc[0].fark, 2)}), d+2 %{100 * q2.iloc[0].yakala:.0f}"
        for H in U for p in C2_ESIK22["A"]["pazar"] for h in C2_HUCRE22
        for q0 in [T[(T.ufuk == H) & (T.pazar == p) & (T.hucre == h) & (T.taban == "DS") & (T.n_hedef.astype(str) == "300") & np.isclose(T.delta, 0)]]
        for q2 in [T[(T.ufuk == H) & (T.pazar == p) & (T.hucre == h) & (T.taban == "DS") & (T.n_hedef.astype(str) == "300") & np.isclose(T.delta, 0.02)]]
        if len(q0) and len(q2))]
    B = pd.DataFrame(J["B"]["hucre"])
    s += ["", "## 2. B — BİLİNEN İZ: 12-1 momentum (açık veriden yeniden üretilen ANA olaylar)", "",
          "U = üst onda (+), A = alt onda (-; 0'ı kesmesi yeter). p = ay kümeli işaret permütasyonu (önceden yazılı yön). [alt, üst] = ay kümeli "
          "boot %95. PEAD (B2): " + C2_ESIK22["B"]["pead"], "",
          "| kod | pazar | H | hücre | n | FARK [alt, üst] | medyan | SIRA | L3O | p | güç | plasebo FARK / tutar (+/-) | kapı | TUTAR |", "|" + "---|" * 14]
    for r in sorted(B.to_dict("records"), key=lambda r: (r["kod"], r["pazar"], r["ufuk"], r["hucre"])):
        s.append(f"| {r['kod']} | {r['pazar']}{' (bilgi)' if r.get('bilgi') else ''} | {r['ufuk']} | {r['hucre']} | {r['n']} | {_c2_y(r['fark'], 2)} "
                 f"[{_c2_y(r['boot_alt'], 2)}, {_c2_y(r['boot_ust'], 2)}] | {_c2_y(r['med'], 2)} | {_c2_s(r['sira'])} | "
                 f"{_c2_y(r['l3o'] if r['yon'] == '+' else r['l3o_neg'], 2)} | {_c2_s(r['p'], 4)} | {_c2_s(r['guc'], 2)} | "
                 f"{_c2_y(r['plasebo_fark'], 2)} / %{100 * (r['plasebo_tutar_pay'] or 0):.0f} | {'geçti' if r['plasebo_gecti'] else 'DÜŞTÜ'} | "
                 f"{'TUTAR' if r['tutar'] else ('ters' if r['ters'] else '-')} |")
    s += ["", "Huni (B): " + "; ".join(f"{k}: {v}" for k, v in J["B"]["say"].items() if k.startswith("mom_"))]
    s += ["", "Olay sayımı (c2_olc, tekil H): " + "; ".join(f"{k}: girdi {v.get('girdi')}, tekil düşen {v.get('tekil')}, R_H ölçülen "
                                                          f"{v.get('olcum_r15')}, dönem {v.get('donem')}"
                                                          for k, v in J["B"]["say"].items() if k.startswith("B1_"))]
    C = pd.DataFrame(J["C"]["satir"]); Tn = pd.DataFrame(J["C"]["tani"])
    s += ["", f"## 3. C — PLASEBO KAPISI (aynı gün rastgele havuz hissesi, {C2_ESIK['plasebo']['tohum_sayi']} tohum; geçer = |ort FARK| < 0,5 "
          "puan VE + payı <= %7 VE - payı <= %7)", "",
          "| pazar | H | hücre | n | ort FARK (puan) | sd (tohumlar) | TUTAR payı + / - / iki yön birleşik | geçti | karar pazarı |", "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(C.to_dict("records"), key=lambda r: (r["pazar"], r["ufuk"], r["hucre"], str(r["n_hedef"]))):
        s.append(f"| {r['pazar']} | {r['ufuk']} | {r['hucre']} | {r['n_hedef']} ({r['n']:.0f}) | {_c2_y(r['fark_ort'], 2)} | {_c2_y(r['fark_sd'], 2, False)} | "
                 f"%{100 * r['tutar_pay_arti']:.1f} / %{100 * r['tutar_pay_eksi']:.1f} / %{100 * r['tutar_pay_iki']:.1f} | "
                 f"{'EVET' if r['gecti'] else 'HAYIR'} | {'karar' if r['karar'] else 'bilgi'} |")
    r0 = T[(T.taban == "RAST") & np.isclose(T.delta, 0.0) & T.n_hedef.astype(str).isin(["100", "300", "1000"])]
    s += ["", "A RAST delta 0 (saf plasebo) yakalama payı, n >= 100 birleşik (sonuç kuralı iii): " + "; ".join(
        f"R{H} {p} {h} %{100 * float((x.yakala * x.tohum).sum() / x.tohum.sum()):.1f}" for (H, p, h), x in r0.groupby(["ufuk", "pazar", "hucre"]))]
    s += ["", "Tanı:", "", "| pazar | H | hücre | gün | havuz / gün | R_H + kova / gün | dolu kova / gün | DS olay (R_H) | eşsiz payı | eş sayısı medyan | "
          "DS FARK0 ort |", "|" + "---|" * 11]
    for r in Tn.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['ufuk']} | {r['hucre']} | {r['gun']} | {_c2_s(r['havuz_gun_medyan'], 0)} | {_c2_s(r['rh_kova_gun_medyan'], 0)} | "
                 f"{_c2_s(r['dolu_kova_medyan'], 0)} | {r['olay_rh']} | %{100 * (r['essiz_pay'] or 0):.1f} | {_c2_s(r['n_es_medyan'], 0)} | "
                 f"{_c2_y(r['fark0_ort'], 2)} |")
    Yd = J["yeniden"]; Rg = J["regresyon21"]
    s += ["", "## 4. YENİDEN ÜRETİM (K11)", "", f"Durum: {'TUTTU' if Yd['tuttu'] else 'TUTMADI'}"]
    for h in Yd["hucre"]:
        s.append(f"- {h['kod']} {h['pazar']} {h['hucre']} R{h['ufuk']}: düz pandas n {h['n_duz']}, FARK {_c2_y(h['fark_duz'], 4)}, SIRA "
                 f"{_c2_s(h['sira_duz'], 6)} | kod n {h['n']}, FARK {_c2_y(h['fark'], 4)}, SIRA {_c2_s(h['sira'], 6)} -> {'eşit' if h['esit'] else 'FARKLI'}")
    s.append(f"- {Yd['rh_n']} olay R_H düz döngü (H 15 / 30 / 45): bozuk {len(Yd['rh_bozuk'])}; {Yd['es_n']} olay eş ortalaması bütün evren düz "
             f"döngü (H 30): bozuk {len(Yd['es_bozuk'])}")
    s += ["", "## 5. v2.1 REGRESYONU (ufuk verilmeyen çağrı = v2.1)", "", f"Durum: {'TUTTU' if Rg.get('tuttu') else 'TUTMADI'} (giriş <= "
          f"{Rg.get('giris_son', '-')}; kova sınırları cetvel2_esik_v2.1.json)"]
    for p, r in Rg.get("olay", {}).items():
        s.append(f"- {p}: v2.1 olay {r['olay_21']}, eşleşen {r['eslesen']}; farklı sütun değeri: "
                 + ", ".join(f"{k} {v['farkli']}" for k, v in r["kolon"].items()))
    for h in Rg.get("hucre", []):
        s.append(f"- {h['kod']} {h['pazar']} eğitim (giriş <= {Rg.get('giris_son')}): v2.1 n {h['n_21']}, FARK {_c2_y(h['fark_21'], 4)}, SIRA "
                 f"{_c2_s(h['sira_21'], 6)} | yeni n {h['n_yeni']}, FARK {_c2_y(h['fark_yeni'], 4)}, SIRA {_c2_s(h['sira_yeni'], 6)} -> "
                 f"{'eşit' if h['esit'] else 'FARKLI'}")
    s += ["", "## 6. NOTLAR", "", "- Evren bugün işlem gören hisseler: hayatta kalma yanlılığı olaya ve eşe aynı biçimde etki eder.",
          "- Bu iş cetvel sınamasıdır; 'iz' iddiası yoktur. B etiketleri yalnız cetvelin davranışını gösterir.",
          "- 2023 sonrası KASA'da mühürlü; bu rapordaki bütün hücreler açık veri (2016-22)."]
    metin = "\n".join(s) + "\n"
    YH._yh_yaz(_c2_yol("rapor", c, C2_E22), metin, "C2 v2.2 rapor")
    return metin


def _cakisma_kontrol_c2(_once=_CK_ONCE_C2, _dosya="CETVEL2.py"):
    """Çakışma kapısı: bu dosya bellekteki c2_ / C2_ / _c2 öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_C2", "_CK_KAYIT", "_cakisma_kontrol_c2", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "subprocess", "_dt", "annotations", "math",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "OC", "YH", "DS", "PK")
    onek = ("c2_", "C2_", "_c2", "C2Hata", "c2log", "_C2", "KOK_C2")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_c2()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=C2_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha", "onkayit22", "kos22", "rapor22", "sha22", "regresyon21"])
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--onceki", default=None)
    ap.add_argument("--duzeltme", default=None)
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(c2_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz, onceki=a.onceki, duzeltme=a.duzeltme))
        elif a.komut == "kos":
            R_ = c2_kos(a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "rapor":
            print(c2_rapor(a.cikti))
        elif a.komut == "onkayit22":
            print(c2_onkayit22_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos22":
            R_ = c2_kos22(a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "rapor22":
            print(c2_rapor22(a.cikti))
        elif a.komut == "sha22":
            print(json.dumps(c2_sha22_simdi(a.veri, a.cikti), indent=1))
        elif a.komut == "regresyon21":
            print(json.dumps(_c2_jsonla(c2_regresyon21(a.veri)), ensure_ascii=False, indent=1))
        else:
            print(json.dumps(c2_sha_simdi(a.veri, a.cikti), indent=1))
    except (C2Hata, DS.DSHata, OC.OCHata, PK.PKHata) as ex:
        c2log.error("%s", ex); sys.exit(1)
