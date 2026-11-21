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
Kütüphane (ADIM H):  import CETVEL2 as C2; R = C2.c2_olc(olaylar, hipotez)  (bkz. c2_olc belge dizesi)
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

C2_SURUM = "CETVEL2 v2.0 (2026-11-21): R15 konum eşli fark (bütün evren), plasebo kapısı, güç eğrisi; pozitif kontrol v2"
C2_ETIKET_SURUM = os.environ.get("C2_SURUM_ETIKET", "")      # '' = v2.0; '_v2.1' = düzeltilmiş ön kayıt (eski dosyalar silinmez)
C2_YOL = {"cikti": os.path.join(KOK_C2, "arastirma_cikti", "cetvel2"), "veri": os.environ.get("C2_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_C2, "CETVEL2.py"),
          "ds_olay": os.path.join(KOK_C2, "arastirma_cikti", "dusus_sonrasi", "ds_olay.csv.gz"),
          "pk_b": os.path.join(KOK_C2, "arastirma_cikti", "pozitif_kontrol", "pk_b_olay.csv.gz"),
          "pk_json": os.path.join(KOK_C2, "arastirma_cikti", "pozitif_kontrol", "pozitif_kontrol.json"),
          "pk_kod": os.path.join(KOK_C2, "POZITIF_KONTROL.py")}


def _c2_dosya() -> Dict[str, str]:
    e = C2_ETIKET_SURUM
    return {"onkayit": f"CETVEL2_ON_KAYIT{e}.md", "esik": f"cetvel2_esik{e}.json", "guc": f"cetvel2_guc{e}.json",
            "prefix": f"cetvel2_prefix{e}.json", "json": f"cetvel2_pozitif_kontrol{e}.json", "rapor": f"CETVEL2_POZITIF_KONTROL{e}.md",
            "a_satir": f"c2_a_hucre{e}.csv.gz", "b_satir": f"c2_b_olay{e}.csv.gz", "c_satir": f"c2_c_plasebo{e}.csv"}


C2_PAZAR = ["ABD", "AVR", "BIST"]
C2_KARAR = ["ABD", "AVR"]
C2_HUCRE = ["egitim", "sinama"]
C2_KOVA_SAYI = 36          # 3 ATRP x 3 likidite x 4 F15

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
C2_ESIK: Dict[str, Any] = {
    "surum": "C2.0",
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
    "plasebo": {"tohum_sayi": 20, "tohum": 2114, "fark_mutlak": 0.005, "tutar_pay": 0.07,
                "tanim": "hücrenin ölçülen her olayı yerine AYNI GİRİŞ GÜNÜ havuzdan rastgele bir hisse (gün içinde yerine koymadan; R15 "
                         "ölçülebilir, kovası var) -> aynı cetvel (eşler, en az 5, boot, p, SIRA, L3O, güç) -> 20 tohum. KAPI GEÇER = |20 tohum "
                         "ortalama FARK| < 0,005 (0,5 puan) VE TUTAR payı (hipotezin yönünde; '?' iki yön) <= %7. Geçmeyen hücre KARAR VERMEZ "
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
                 "hücresinde n >= 100'de > %10. KUSUR -> nedeni yazılır, cetvel düzeltilir, ön kayıt v2.1, yeniden koşu (en çok 2 tur)",
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
    "K9": ("EVET", "CETVEL2_ON_KAYIT.md: C2_ESIK sha, CETVEL2.py sha, kova sınırları (sayı), güç eğrisi, DS / YH / OC / PK sha'ları, girdi dosyası "
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


def _c2_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or C2_YOL["cikti"], _c2_dosya().get(ad, ad))


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
               tohum_sayi: Optional[int] = None) -> Dict[str, Any]:
    """Plasebo kapısı: olay günleriyle (aynı gün) rastgele havuz hisseleri, 20 tohum, aynı cetvel. Döner ortalama FARK, tutar payı, geçti."""
    Pl = C2_ESIK["plasebo"]; T = int(tohum_sayi or Pl["tohum_sayi"]); sat = []
    idx = Pn["P"]["tarih"]
    for t in range(T):
        rng = np.random.default_rng([int(Pl["tohum"]), int(tohum_ek) % (2 ** 31), t])
        rd, rj = c2_rastgele(Pn, d, rng)
        x = Pn["R15"][rd, rj]
        e = c2_es(Pn, rd, rj, x, rd, rj)
        c = c2_hucre(x, e["es_r15"], e["sira"], idx[rd], yon, tohum_ek=900000 + t, egri=egri, perm=False)
        sat.append({"tohum": t, "n": c["n"], "fark": c["fark"], "sira": c["sira"], "tutar": bool(c["tutar"]), "yakala": bool(c["yakala"]),
                    "boot_alt": c["boot_alt"], "boot_ust": c["boot_ust"]})
    S = pd.DataFrame(sat)
    fo = float(S.fark.mean()) if len(S) else np.nan; tp = float(S.tutar.mean()) if len(S) else np.nan
    gec = bool(np.isfinite(fo) and abs(fo) < float(Pl["fark_mutlak"]) and np.isfinite(tp) and tp <= float(Pl["tutar_pay"]))
    return {"fark_ort": fo, "fark_sd": float(S.fark.std(ddof=1)) if len(S) > 1 else np.nan, "tutar_pay": tp,
            "yakala_pay": float(S.yakala.mean()) if len(S) else np.nan, "n_ort": float(S.n.mean()) if len(S) else np.nan, "gecti": gec,
            "tohum": sat}


# ================================================================ 4) ETİKET ve BH
def c2_bh(p: List[float], q: Optional[float] = None) -> List[bool]:
    return YH._yh_bh(list(p), float(q if q is not None else C2_ESIK["etiket"]["bh"]["q"]))


def c2_etiket(h: Dict[str, Dict[str, Dict[str, Any]]], yon: str, karar: Optional[List[str]] = None) -> Dict[str, Any]:
    """h[pazar][hücre] -> hücre sözlüğü (c2_hucre + 'plasebo_gecti'). Ham etiket (BH öncesi) ve gerekçe."""
    karar = karar or C2_KARAR
    H_ = [(p, k, h.get(p, {}).get(k)) for p in karar for k in C2_HUCRE]

    def poz(c):
        return c is not None and np.isfinite(c.get("boot_alt", np.nan)) and c["boot_alt"] > 0

    def neg(c):
        return c is not None and np.isfinite(c.get("boot_ust", np.nan)) and c["boot_ust"] < 0
    for p in karar:
        a, b = h.get(p, {}).get("egitim"), h.get(p, {}).get("sinama")
        if (poz(a) and neg(b)) or (neg(a) and poz(b)):
            return {"etiket": "ÇELİŞKİLİ", "neden": f"{p} eğitim / sınama boot aralıkları sıfırın zıt tarafında"}
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
           karar: Optional[List[str]] = None) -> Dict[str, Any]:
    """ADIM H ARAYÜZÜ.
    olaylar: DataFrame[pazar, sembol, tarih (sinyal günü t), F_<...> bayrak sütunları (1 / 0 / NaN)]. Pazarlar ABD / AVR / BIST.
    hipotez: {kod: {'bayrak': 'F_x' ya da None (bütün olaylar), 'yon': '+' / '-' / '?'}}.
    Döner {'satir': olay satırları (pazar, sembol, tarih, giris, d, j, donem, kova, atrp, f15, lq3, hat, atr, E0, r15, bilgi sütunları h5 / st5 /
           h10 / h5_atr / st5_atr / r60 / esli_r60, bayraklar, her kod için es_r15_<kod>, n_es_<kod>, sira_<kod>, fark_<kod>),
           'hucre': DataFrame[kod, yon, pazar, hucre, n, n_bayrak, n_essiz, fark, med, sira, boot_alt, boot_ust, l3o, l3o_neg, p, guc, tutar,
                    ters, yakala, r15_ort, r15_med, es_ort, plasebo_fark, plasebo_tutar_pay, plasebo_gecti, durum, h5, st5, h5_atr, st5_atr,
                    r60_fark],
           'etiket': DataFrame[kod, yon, etiket_ham, neden, p_bh, bh_gecti, etiket], 'say': huni}.
    Eşler: aynı denemenin (kod) bayrağı 1 olan o günkü olay hisseleri eş dışı. Kova sınırları cetvel2_esik.json, güç cetvel2_guc.json."""
    t0 = time.time(); karar = karar or C2_KARAR
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
        Pn = c2_panel_al(pazar, veri)
        X, sy = c2_olay(olaylar[olaylar.pazar.astype(str) == pazar].drop(columns=["pazar"]), Pn, tekil_gun)
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
            for hi, hc in enumerate(C2_HUCRE):
                mm = m & (X.donem.to_numpy() == hc)
                tek = int(tohum0) * 1000 + ki * 20 + pi * 4 + hi
                egri = _c2_egri_al(pazar, hc, guc)
                c = c2_hucre(x[mm], X[f"es_r15_{kod}"].to_numpy(float)[mm], X[f"sira_{kod}"].to_numpy(float)[mm], X.giris.to_numpy()[mm],
                             h["yon"], tohum_ek=tek, egri=egri)
                ol = mm & np.isfinite(X[f"fark_{kod}"].to_numpy(float))
                r = {"kod": kod, "yon": h["yon"], "pazar": pazar, "hucre": hc, "n_bayrak": int(mm.sum()),
                     "n_r15": int((mm & np.isfinite(x)).sum()), "n_essiz": int((mm & np.isfinite(x) & ~ol).sum()),
                     **{k_: v_ for k_, v_ in c.items()}}
                if bilgi:
                    for b_ in ("h5", "st5", "h5_atr", "st5_atr"):
                        r[b_] = float(np.nanmean(X[b_].to_numpy(float)[ol])) if ol.any() else np.nan
                    rf = (X.r60 - X.esli_r60).to_numpy(float)[ol]
                    r["r60_fark"] = float(np.nanmean(rf)) if np.isfinite(rf).any() else np.nan
                if plasebo and c["n"] > 0:
                    pl = c2_plasebo(Pn, d[ol], h["yon"], egri, tohum_ek=tek)
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
        e = c2_etiket(hh, h["yon"], karar)
        ps = []
        for p in karar:
            c = hh.get(p, {}).get("sinama")
            ps.append(1.0 if (c is None or c["n"] < C2_ESIK["hucre"]["n_min"] or not np.isfinite(c.get("p", np.nan))) else float(c["p"]))
        et.append({"kod": kod, "yon": h["yon"], "etiket_ham": e["etiket"], "neden": e["neden"], "p_bh": max(ps) if ps else 1.0})
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
                pn_ = c2_plasebo(Pn, dsec, "-", egri, tohum_ek=700000 + pi * 100 + hi * 10 + ni)
                sat.append({"pazar": pazar, "hucre": h, "n_hedef": str(nk), "n": pl["n_ort"], "fark_ort": pl["fark_ort"], "fark_sd": pl["fark_sd"],
                            "tutar_pay_arti": pl["tutar_pay"], "tutar_pay_eksi": pn_["tutar_pay"], "yakala_pay_arti": pl["yakala_pay"],
                            "gecti_arti": pl["gecti"], "gecti_eksi": pn_["gecti"],
                            "gecti": bool(pl["gecti"] and pn_["gecti"]), "karar": pazar in C2_KARAR})
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
    r0 = At[(At.taban == "RAST") & (At.delta == 0.0) & At.pazar.isin(C2_KARAR) & At.n_hedef.isin(["100", "300", "1000", "yari"])]
    for r in r0.itertuples():
        if r.yakala > 0.10:
            kusur.append(f"A RAST delta 0 yakalama {r.pazar} {r.hucre} n {r.n_hedef}: %{100 * r.yakala:.0f}")
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
    s += ["", "## 3. C — PLASEBO KAPISI (aynı gün rastgele havuz hissesi, 20 tohum; geçer = |ort FARK| < 0,5 puan VE TUTAR payı <= %7)", "",
          "| pazar | hücre | n | ort FARK (puan) | sd (tohumlar) | TUTAR payı + / - | yakalama payı + (güç hariç) | geçti | karar hücresi |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in C.to_dict("records"):
        s.append(f"| {r['pazar']} | {r['hucre']} | {r['n_hedef']} ({r['n']:.0f}) | {_c2_y(r['fark_ort'], 2)} | {_c2_y(r['fark_sd'], 2, False)} | "
                 f"%{100 * r['tutar_pay_arti']:.0f} / %{100 * r['tutar_pay_eksi']:.0f} | %{100 * r['yakala_pay_arti']:.0f} | "
                 f"{'EVET' if r['gecti'] else 'HAYIR'} | {'karar' if r['karar'] else 'bilgi'} |")
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
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
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
        else:
            print(json.dumps(c2_sha_simdi(a.veri, a.cikti), indent=1))
    except (C2Hata, DS.DSHata, OC.OCHata, PK.PKHata) as ex:
        c2log.error("%s", ex); sys.exit(1)
