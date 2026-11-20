"""DUSUS_SONRASI — düşüş sonrası parmak izi: web + eleştiri havuzundan gelen 25 sınıf I hipotezin (DS01..DS28) tek ön kayıtla 15 bar
cetvelinde ölçümü (20 Kasım 2026; iş tanımı arastirma_cikti/dusus_sonrasi/DS_IS_TANIMI_2026-11-20.md bölüm 6, çerçeve DS_OLCUM_CERCEVE.md,
hipotez havuzu DS_ELESTIRI.md bölüm 3 / 5).

SORU: hisse son 120 geçerli barın en yüksek kapanışından en az %30 düşmüş ve 120 gün kapanış aralığının alt çeyreğinde (DS olayı). Giriş günü
t'de BİLİNEN hangi ölçü, sonraki 15 geçerli barda +%5 hedefinin stop'tan (hat x 0,98; hat = son 20 bar en düşük Low) ÖNCE görülmesini ayırt eder?
CETVEL: YAPI_HEDEF 15 bar makinesi AYNEN içe alınır (yh_sim, yh_getiri, yh_d1_hucre, yh_d3_boot_l3o, yh_d3_guc, yh_d3_etiket, _yh_bh; KOPYA YOK).
EŞ: aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü), DS kümesi İÇİNDE (o gün DS durumunda olan öteki hisseler),
özelliği TUTMAYAN ve 15 barı ölçülebilir hisseler; eşler OLAYIN d'si (stop uzaklığı) ile aynı kuralla ölçülür (aynı geometri); en az 3 eş.
FARK = ort h5(özellik tutan olay) - ort es_h5. 'DS dışı eş' (aynı gün, aynı kova, DS durumunda OLMAYAN havuz hisseleri) BİLGİ.
HÜCRE: pazar {ABD, AVR karar; BIST bilgi} x {eğitim 2016-22, sınama 2023-01 .. 2026-08 (eğitimin son girişinden 60 bar ambargo)}.
ETİKET: karne v3 (yh_d3_etiket; KATKI+ / KATKI− / SORGULA / ÖLÇÜLEMEDİ) + ÇELİŞKİLİ + BH q 0,10 (m = 25 sabit; p = ay kümeli işaret
permütasyonu, ABD ve AVR sınama p'lerinin büyüğü). Eğitim çeyrek / onda / beşlik eşikleri eğitim DS ANA olaylarından (getirisiz) ds_esik.json'a
SAYI olarak yazılır ve ön kayıtta mühürlenir. Sınıf II (ABD-olay, sec_ozet) ayrı BİLGİ tablosu, BH dışı.

Komut:  python DUSUS_SONRASI.py onkayit [--islem 4]   özellik (A + B geçişi) -> eşik -> prefix -> ds_esik.json, ds_prefix.json, DS_ON_KAYIT.md
        python DUSUS_SONRASI.py kos [--islem 4]       kapı (ik_kontrol_kapisi + sha + git) -> ölçüm -> ds_sonuc.json, ds_olay.csv.gz, DS_RAPOR.md
        python DUSUS_SONRASI.py rapor                 ds_sonuc.json -> DS_RAPOR.md
        python DUSUS_SONRASI.py sha                   kod / eşik / girdi sha'ları
Colab:  exec(open('DUSUS_SONRASI.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri);
        sınıf II: /tmp/k55/sec_ozet.json + sembol_cik.json (K55.veri_paket.ac('/tmp/iv/k55', '/tmp/k55')). k34_yahoo YÜKLENMEZ (V_ABD 1.411 hisse).
Komisyon / kayma YOK. Evren bugün işlem gören hisseler: hayatta kalma yanlılığı ((+) yönlü özellikler lehine, (−) yönlüler aleyhine).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_DS = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_DS = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_DS not in sys.path:
    sys.path.insert(0, KOK_DS)

import ORTAK_CETVEL as OC  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402
import S6_TABAN as S6  # noqa: E402

dslog = logging.getLogger("col.dusus_sonrasi")
if not dslog.handlers:
    _ds_h = logging.StreamHandler(sys.stderr)
    _ds_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s dusus_sonrasi: %(message)s", "%H:%M:%S"))
    dslog.addHandler(_ds_h)
    dslog.setLevel(logging.INFO)
    dslog.propagate = False

DS_SURUM = "DUSUS_SONRASI v1.0 (2026-11-20): 25 sınıf I hipotez (DS_ELESTIRI bölüm 5), 15 bar cetveli, DS içi eş, karne v3 + BH q 0,10"
DS_YOL = {"cikti": os.path.join(KOK_DS, "arastirma_cikti", "dusus_sonrasi"), "veri": os.environ.get("DS_VERI", "/tmp/veri"),
          "veri2_yok": "/tmp/_ds_k34_yuklenmez", "kod": os.path.join(KOK_DS, "DUSUS_SONRASI.py"),
          "yh_kod": os.path.join(KOK_DS, "YAPI_HEDEF.py"), "oc_kod": os.path.join(KOK_DS, "ORTAK_CETVEL.py"),
          "s6_kod": os.path.join(KOK_DS, "S6_TABAN.py"), "sektor": os.path.join(KOK_DS, "sektor_ABD.csv"),
          "k55": os.environ.get("DS_K55", "/tmp/k55")}
DS_DOSYA = {"onkayit": "DS_ON_KAYIT.md", "esik": "ds_esik.json", "prefix": "ds_prefix.json", "sonuc": "ds_sonuc.json",
            "olay": "ds_olay.csv.gz", "rapor": "DS_RAPOR.md", "cerceve": "DS_OLCUM_CERCEVE.md", "elestiri": "DS_ELESTIRI.md",
            "is_tanimi": "DS_IS_TANIMI_2026-11-20.md"}
DS_PAZAR = ["ABD", "AVR", "BIST"]
DS_KARAR = ["ABD", "AVR"]
DS_HUCRE = ["egitim", "sinama"]

# ================================================================ MÜHÜRLÜ EŞİK SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
DS_HIP: Dict[str, Dict[str, Any]] = {
    "DS01": {"sira": 1, "ad": "son 10 günde sona doğru hızlanan düşüş (içbükey yol)", "yon": "+", "iki": True,
             "tanim": "KONV10_t = (M - ort(C_t-9..t)) / M, M = (C_t-9 + C_t) / 2; 1 = KONV10 <= eğitim alt beşte bir sınırı (q20)",
             "esik": "KONV10_q20 (eğitim)", "kaynak": "Gulen-Woeppel JFQA (10 gün beşli, t 7,31)"},
    "DS04": {"sira": 2, "ad": "tek gün büyük düşüş sonrası sıçrama fazı", "yon": "+", "iki": True,
             "tanim": "son barlarda r_s = C_s / C_s-1 - 1 <= -0,15 ve t - s in [2, 23] (geçerli bar)", "esik": "-%15; [2, 23] (kaynak)",
             "kaynak": "Bulkowski dead-cat; Cox-Peterson JF 1994; Guo 2024 (İDDİA)"},
    "DS02": {"sira": 3, "ad": "düşük göreli devirli kaybeden", "yon": "+", "iki": True,
             "tanim": "DEVIR_t = ort(V_t-20..t) / medyan(V_t-251..t); 1 = DEVIR <= eğitim alt onda (q10)", "esik": "DEVIR_q10 (eğitim)",
             "kaynak": "Medhat-Schmeling RFS 2022; Lee-Swaminathan JF 2000"},
    "DS03": {"sira": 4, "ad": "sektörden (AVR / BIST: evrenden) bağımsız son ay düşüşü", "yon": "+", "iki": False,
             "tanim": "ART21_t = r21(hisse) - ort r21(sektör eşit ağırlık, sektor_ABD.csv, >= 5 hisse; yoksa evren); 1 = ART21 <= eğitim q10",
             "esik": "ART21_q10 (eğitim)", "kaynak": "Da-Liu-Schaumburg MS 2014"},
    "DS08": {"sira": 5, "ad": "Weinstein evre 4 (SMA150 düşüyor, fiyat altında)", "yon": "-", "iki": False,
             "tanim": "EGIM = SMA150_t / SMA150_t-20 - 1; 1 = EGIM < 0 VE C_t < SMA150_t", "esik": "işaret (kaynak)",
             "kaynak": "Weinstein; Bulkowski Stages (evre 4 alım n 127)"},
    "DS05": {"sira": 6, "ad": "satış doruğu barı (geniş aralık + hacim + dipten uzak kapanış)", "yon": "+", "iki": False,
             "tanim": "s in [t-59, t]: C_s < C_s-1 VE (H-L)_s / ATR20_s-1 >= q VE V_s >= 2 x SMA20(V)_s-1 VE CLV_s >= m",
             "esik": "2 x SMA20 (kaynak); q = ARALIK eğitim q75, m = CLV eğitim medyanı (t günü değerleri)", "kaynak": "Wyckoff; Huddart MS 2009"},
    "DS06": {"sira": 7, "ad": "Turtle Soup dip süpürme + kapanışla geri alma", "yon": "+", "iki": False,
             "tanim": "L_t < m20 = min(L_t-20..t-1), m20'nin yaşı >= 4 bar, C_t >= m20, (H-L)_t <= 3 x ATR14_t-1", "esik": "20 / 4 / 3 (kaynak)",
             "kaynak": "Connors-Raschke 1996"},
    "DS11": {"sira": 8, "ad": "kapanış 7 günün en düşüğü (Double 7 / H2)", "yon": "?", "iki": True,
             "tanim": "C_t <= min(C_t-6..t)", "esik": "7 gün (kaynak)", "kaynak": "Connors; KAZANANLAR H2"},
    "DS09": {"sira": 9, "ad": "RSI(2) aşırı satım", "yon": "+", "iki": True,
             "tanim": "RSI2_t <= 5 (Wilder, alfa 1/2)", "esik": "5 (kaynak)", "kaynak": "Connors / ChartSchool"},
    "DS14": {"sira": 10, "ad": "son alçalan onaylı tepenin kapanışla aşılması (CHoCH)", "yon": "+", "iki": False,
             "tanim": "son iki onaylı 6/6 tepe LH1 > LH2 (onay p + 6 <= t) VE C_t-1 <= LH2 < C_t", "esik": "işaret; pivot 6/6",
             "kaynak": "DeMark / Wyckoff / smc (İDDİA)"},
    "DS15": {"sira": 11, "ad": "busted aşağı kırılım (S6 tabanı)", "yon": "+", "iki": True,
             "tanim": "son S6 bölgesi s'de KIRILDI (S6 kuralı C_s < dip x (1 - kirTol)); min(L_s..t) >= 0,90 x kutu_alt; C_t > kutu_ust ilk kez",
             "esik": "%10 (kaynak)", "kaynak": "Bulkowski Busted"},
    "DS16": {"sira": 12, "ad": "Wyckoff ikinci test (DS05 doruğuna düşük hacim + dar aralıkla dönüş)", "yon": "+", "iki": False,
             "tanim": "son DS05 doruk barı s, u* = argmin L[s+5..t]: |L_u/L_s - 1| <= e VE V_u/V_s < q1 VE (H-L)_u/(H-L)_s < q2; doruk yoksa 0",
             "esik": "e, q1, q2 = eğitim medyanları", "kaynak": "Wyckoff ChartSchool"},
    "DS18": {"sira": 13, "ad": "evren endeksine göre göreli güç eğimi yukarı", "yon": "+", "iki": True,
             "tanim": "RS = C / E (evren eşit ağırlık); SMA22(RS)_t-1 > SMA22(RS)_t-2", "esik": "işaret (Bulkowski)", "kaynak": "Bulkowski RS"},
    "DS21": {"sira": 14, "ad": "düşüşün çoğu gece (boşluk) olmuş", "yon": "-", "iki": False,
             "tanim": "GECE_PAY = sum ln(O_i/C_i-1) / sum ln(C_i/C_i-1), i in [t-19, t], payda < 0; 1 = >= eğitim q75 (açılışı temizlenmiş bar penceredeyse NaN)",
             "esik": "GECE_q75 (eğitim)", "kaynak": "Miwa (QuantPedia); Lou-Polk-Skouras"},
    "DS22": {"sira": 15, "ad": "düşüşteki büyük aşağı günün kapanışla doldurulması", "yon": "+", "iki": False,
             "tanim": "i in [t-59, t-1]: r_i <= -2 x std20(r)_i-1; C_t >= C_i-1 ilk kez (C_i..t-1 < C_i-1)", "esik": "2 sigma (kaynak)",
             "kaynak": "tastylive"},
    "DS13": {"sira": 16, "ad": "TD Sequential setup 9", "yon": "+", "iki": False,
             "tanim": "C_i < C_i-4 art arda tam 9 bar, 9. bar = t (kesişim şartı yok)", "esik": "9 (kaynak)", "kaynak": "DeMark (MarketInOut)"},
    "DS12": {"sira": 17, "ad": "Elder Impulse kırmızıdan çıkış", "yon": "+", "iki": False,
             "tanim": "KIRMIZI_i = EMA13_i < EMA13_i-1 VE HIST_i < HIST_i-1 (MACD 12,26,9); KIRMIZI_t-1 VE değil KIRMIZI_t", "esik": "ikili (kaynak)",
             "kaynak": "Elder (ChartSchool)"},
    "DS19": {"sira": 18, "ad": "Bollinger %b W dip", "yon": "+", "iki": False,
             "tanim": "son iki onaylı 6/6 dip d1 < d2: %b_d1 <= 0 VE %b_d2 > 0 VE d2 - d1 in [Q1, Q3] VE L_d2 <= L_d1 x (1 + tol); BB(20,2)",
             "esik": "Q1 / Q3 = eğitim dip arası bar çeyrekleri; tol = eğitim medyan |L_d2/L_d1 - 1|", "kaynak": "bollingerbands.com"},
    "DS20": {"sira": 19, "ad": "alt bantta yürüme", "yon": "-", "iki": False,
             "tanim": "YURU = sayı(C_i < Alt_i), i in [t-9, t], BB(20,2); 1 = YURU >= eğitim q75", "esik": "YURU_q75 (eğitim)",
             "kaynak": "Bollinger kural 7-8"},
    "DS17": {"sira": 20, "ad": "piyasa aşağı günlerinde direnç", "yon": "+", "iki": False,
             "tanim": "DIRENC = ort(r_i - r_m,i | r_m,i < 0), i in [t-39, t], r_m evren eşit ağırlık; 1 = >= eğitim q75", "esik": "DIRENC_q75 (eğitim)",
             "kaynak": "Wyckoff alım testi 7"},
    "DS07": {"sira": 21, "ad": "smash day dönüşü", "yon": "+", "iki": False,
             "tanim": "C_t-1 < L_t-2 VE L_t-1 < min(L_t-9..t-2) VE H_t > H_t-1", "esik": "8 gün (kaynak)", "kaynak": "Larry Williams"},
    "DS28": {"sira": 22, "ad": "252 gün tepeden en az %60 derin", "yon": "?", "iki": True,
             "tanim": "C_t / max(C son 252 bar) - 1 <= -0,60", "esik": "-%60 (kaynak)", "kaynak": "Brandes; Mauboussin (ikincil)"},
    "DS10": {"sira": 23, "ad": "DV2 < 10", "yon": "+", "iki": True,
             "tanim": "DV2 = yüzdelik sıra(SMA2(C / ((H+L)/2) - 1), son 252 bar) x 100 < 10", "esik": "10; 252 (kaynak)", "kaynak": "Quantitativo (İDDİA)"},
    "DS23": {"sira": 24, "ad": "yukarıda +%5..+%10 bandında dolmamış 2 sigma aşağı gün", "yon": "+", "iki": False,
             "tanim": "i in [t-119, t]: r_i <= -2 x std20_i-1, C_i..t < C_i-1 (dolmamış), C_i-1 / C_t - 1 in (0,05; 0,10]", "esik": "2 sigma; bant",
             "kaynak": "tastylive; smc (İDDİA)"},
    "DS25": {"sira": 25, "ad": "dipten çapalı AVWAP testi", "yon": "+", "iki": False,
             "tanim": "AVWAP = son 120 bar en düşük L barından t'ye sum TP*V / sum V; C_t > AVWAP VE min(L_t-2..t) <= AVWAP x (1 + e)",
             "esik": "e = eğitim medyanı (C_t > AVWAP olaylarında min(L_t-2..t)/AVWAP - 1)", "kaynak": "MMT / takeprofitapp (İDDİA)"},
}
DS_HIP_SIRA = sorted(DS_HIP, key=lambda k: DS_HIP[k]["sira"])

DS_SINIF2: Dict[str, Dict[str, Any]] = {
    "DS47": {"ad": "5.02 sonrası ilk 2.02 tepkisi negatif (t = tepkiden sonraki ilk gün)", "yon": "+", "kaynak": "sec_ozet 8-K 5.02 / 2.02",
             "tanim": "8-K 5.02 başvurusu tarih(t) - 180 takvim günü içinde; sonraki ilk 2.02 bilgi barı i0; tepki = r(C_i0-2 -> C_i0+1) - r_evren < 0; t = i0 + 2"},
    "DS48": {"ad": "Form 144 [t-20, t-1]", "yon": "-", "kaynak": "sec_ozet form '144'", "tanim": "bilgi barı (başvuru + 1 işlem günü) in [t-20, t-1]",
             "not": "2023 öncesi kâğıt başvuru kapsamı eksik (DS_ELESTIRI HATA 10): eğitim hücresi yorumlanmaz"},
    "DS49": {"ad": "yeni pasif %5 ortak (SC 13G / SCHEDULE 13G, değişikliksiz) [t-60, t]", "yon": "+", "kaynak": "sec_ozet",
             "tanim": "bilgi barı in [t-60, t]; form 'SC 13G' ya da 'SCHEDULE 13G' (iki ad birlikte)"},
    "DS50": {"ad": "8-K 2.03 yeni borç [t-20, t]", "yon": "?", "kaynak": "sec_ozet 8-K madde", "tanim": "bilgi barı in [t-20, t]"},
    "DS51": {"ad": "8-K 2.04 borç hızlandırma [t-60, t]", "yon": "-", "kaynak": "sec_ozet 8-K madde", "tanim": "bilgi barı in [t-60, t]"},
    "DS52": {"ad": "8-K 1.02 sözleşme feshi [t-20, t]", "yon": "-", "kaynak": "sec_ozet 8-K madde", "tanim": "bilgi barı in [t-20, t]"},
    "DS53": {"ad": "8-K 3.03 ortak hakları değişimi [t-60, t]", "yon": "-", "kaynak": "sec_ozet 8-K madde", "tanim": "bilgi barı in [t-60, t]"},
}
DS_SINIF2_YOK = {"DS44": "VERİ YOK (Yahoo not günlüğü / bilanço takvimi k67: /tmp, kalıcı değil)",
                 "DS45": "VERİ YOK (k67 not düşürme günlüğü)",
                 "DS46": "bu koşuda kapsam dışı (Form 4 k30; ana model kararı: sınıf II yalnız sec_ozet)"}

DS_ESIK: Dict[str, Any] = {
    "surum": "DS1.0",
    "olay": {"dusus": -0.30, "pencere": 120, "f15": 0.25, "likit_gun": 20, "likit": {"ABD": 1.0e6, "AVR": 1.0e6, "BIST": 5.0e6},
             "fiyat_min": {"ABD": 2.0}, "tekil_bar": 15, "hat_gun": 20,
             "tanim": "hisse-gün t (geçerli bar; OC.oc_veri temiz veri): (a) C_t / max(C son 120 geçerli bar) - 1 <= -0,30; (b) F15_t = (C_t - min C) / "
                      "(max C - min C), son 120 kapanış t dahil, <= 0,25; (c) medyan(C x V x Kur, son 20 bar t dahil) >= 1 mn $ (ABD) / 1 mn EUR (AVR) / "
                      "5 mn TL (BIST); (d) ABD C_t >= 2 $; (e) giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla: havuz üyeliği, "
                      "alt %20 likidite dışı, geçmiş bölünme şüphesi dışı, giriş boşluğu <= 10 gün; tekil_gun = 1); kriz kesiği 31.08.2026 (15 bar "
                      "ölçülemeyen olay ölçülmez). ANA = aynı hissede ilk DS günü, sonraki >= 15 birleşik takvim günü sonra (BÜTÜN DS günleri eş havuzu)"},
    "acilis_temizlik": "O < L ya da O > H olan barlarda O = kırp(O, L, H) (bütün pazarlar; sayı huni'de); DS21 penceresinde kırpılmış bar varsa DS21 NaN",
    "kova": {"atrp_gun": 14, "q": [1 / 3, 2 / 3], "tanim": "kova = ATRP tercili (ATRP_t = ort TR [t-13, t] / C_t; tercil sınırları pazar başına eğitim DS "
                                                         "ANA olaylarından, ds_esik.json) x OC likidite üçlüsü (H[d] % 3; giriş günü kesiti)"},
    "olcu": {"cetvel": "YAPI_HEDEF YH_ESIK['olcu'] AYNEN (ufuk 15, hedef +%5 / +%10, stop0 = hat x 0,98, kilit / takip stopu); yh_sim ile olay ve eşler",
             "hat": "son 20 geçerli bar en düşük Low (t dahil)", "es_min": 3,
             "es": "aynı giriş günü d, aynı pazar, aynı kova, DS kümesi İÇİ (o gün DS durumunda ve OC havuzunda öteki hisseler), özelliği 0 (NaN değil), "
                   "15 barı ölçülebilir; eş stop'u = eş açılışı x (1 - d_olay); en az 3 eş",
             "ds_disi_es": "aynı gün, aynı kova, havuzda, DS durumunda OLMAYAN hisseler (bilgi)", "oc_es": "aynı gün aynı OC kovası (bilgi)"},
    "donem": {"egitim": ["2016-01-01", "2022-12-31"], "sinama": ["2023-01-01", "2026-08-31"], "ambargo_bar": 60,
              "tanim": "giriş tarihine göre; sınama girişi >= panel takviminde (son eğitim ANA girişi + 60 bar) (ds_esik.json 'ambargo')"},
    "esik_tanim": "eğitim (2016-22) DS ANA olaylarında (havuz + tekil sonrası, getirisiz) pazar başına numpy quantile (doğrusal); sınama aynı sayılarla",
    "n_min": 30, "n_kesin": 1000,
    "boot": {"B": 2000, "alt": 0.025, "ust": 0.975, "tohum": 2011, "birim": "giriş ayı"},
    "guc": {"delta": 0.05, "R": 1000, "tohum": 2012, "esik": 0.80, "z": 1.959963984540054,
            "tanim": "yh_d3_guc: hücre tabanından (bütün DS ANA olayları, h5 - es_h5_hepsi; es_h5_hepsi = özellik ayrımı olmadan DS içi eş ortalaması) n "
                     "olay yerine koymadan R kez; güç = Phi(delta / sigma - z); karar hücrelerinden birinde < 0,80 -> ÖLÇÜLEMEDİ"},
    "perm": {"R": 10000, "tohum": 2013,
             "tanim": "ay kümeli işaret permütasyonu: ay toplamı s_m = sum(h5 - es_h5); T = sum s_m / sum n_m; T* = sum e_m s_m / sum n_m, e_m = +-1; "
                      "tek yönlü '+': p = (1 + #{T* >= T}) / (R + 1); '-': T* <= T; iki yönlü (yön '?' ya da iki=True): |T*| >= |T|"},
    "bh": {"q": 0.10, "m": 25, "p_ds": "max(p ABD sınama, p AVR sınama) (kesişim-birleşim; iki pazar şartı); hücre n < 30 -> p = 1",
           "tanim": "YH._yh_bh, 25 p (DS_ELESTIRI bölüm 5 listesi, ANA kollar), q 0,10"},
    "etiket": "karne v3 (YH.yh_d3_etiket): karar hücreleri ABD eğitim / sınama, AVR eğitim / sınama; ÖLÇÜLEMEDİ = bir hücrede n < 30 ya da güç < 0,80; "
              "KATKI+ = her hücrede FARK > 0 VE boot %95 alt > 0 VE leave-3-out FARK > 0 VE st5 olay <= eş VE ATRP şartı (her karar pazarı x hücre x "
              "ATRP tercilinde FARK sonlu ve > 0); KATKI− = her hücrede FARK < 0 VE boot üst < 0; değilse SORGULA. ÇELİŞKİLİ (KATKI'dan önce): bir karar "
              "pazarında eğitim ve sınama boot aralıkları sıfırın ZIT taraflarında ya da ABD sınama ile AVR sınama zıt tarafta. SON ETİKET: KATKI+ / "
              "KATKI− yalnız BH (q 0,10, önceden yazılı yönlü p) geçerse; geçmezse 'SORGULA (BH)'. BIST ve sınıf II BİLGİ",
    "yeniden_uretim": [["DS01", "ABD", "sinama"], ["DS09", "AVR", "egitim"]],
    "elle_sim_n": 50, "elle_sim_tohum": 2014,
    "prefix": {"n": 30, "tohum": 2015, "rtol": 1e-9,
               "tanim": "pazar başına n rastgele DS ANA olayında bütün ham özellikler tam veride ve veri t'de kesilince (bağlam serileri de t'de kesilir) "
                        "yeniden hesaplanır; eşit olmalı (rtol 1e-9, NaN = NaN); tutmazsa DURUR"},
    "hipotez": {k: {kk: vv for kk, vv in v.items()} for k, v in DS_HIP.items()},
    "sinif2": {k: {kk: vv for kk, vv in v.items()} for k, v in DS_SINIF2.items()},
    "sinif2_yok": DS_SINIF2_YOK,
}

DS_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü), DS kümesi içi, özelliği tutmayan; eşler olayın stop "
                   "uzaklığı d ile aynı 15 bar kuralıyla (yh_sim, aynı giriş / çıkış geometrisi); mekanik üstünlük: DS30 / DS31 / DS34 havuzda elendi, "
                   "DS08 / DS20 / DS28 için tutan / tutmayan sayıları getirisiz huni'de; DS dışı eş ve OC eşi bilgi satırı"),
    "K2": ("EVET", "bütün ham özellikler yalnız [.., t] barlarından (pivotlar 6/6 onayı p + 6 <= t); ds_prefix.json pazar başına 30 olayda veri t'de "
                   "kesilince eşit (DURUR); sınıf II olaylar başvuru günü + 1 işlem günü <= t; eşikler eğitim olaylarından getirisiz; sektör sınıfı "
                   "bugünkü (DS03 notu); evren endeksi aynı gün getirilerinin ortalaması"),
    "K3": ("EVET", "OC.oc_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği; açılış H-L dışı bar kırpılır (sayı huni'de, DS21 NaN); 15 bar yalnız "
                   "geçerli barlarla (yh_sim); sinyal günü geçerli bar"),
    "K4": ("EVET", "ANA = hisse başına ilk DS günü, sonraki >= 15 birleşik takvim günü sonra (oc_olay_hazirla sonrası); n = ANA olay; bootstrap / "
                   "permütasyon birimi giriş ayı; ortalama yanında h5 / getiri medyanı raporda"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla d; YH.yh_sim satır 0); açılış stop'un altındaysa olay ölçülmez "
                   "(sayım)"),
    "K6": ("EVET", "V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur (EUR); geçmiş bölünme şüphesi [d-61, d-1] havuz "
                   "dışı (DS04 -%15 günleri bölünme hatası olamaz: OC sup_gecmis); AVR açılış temizliği"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST 581; k34 yüklenmez): (+) yönlü özellikler lehine, (−) yönlüler "
                   "aleyhine yanlı; DS içi eş FARK'ta kısmen götürür; raporda yazılır"),
    "K8": ("EVET", "ABD ve AVR ayrı, eğitim + sınama; n < 30 ÖLÇÜLEMEDİ ve olayları ds_sonuc.json 'kucuk' listesinde; güç < 0,80 ÖLÇÜLEMEDİ; BH q 0,10 "
                   "m = 25 sabit; aynı aileden (DS01 / DS09 / DS10 / DS11; DS05 / DS16) birden fazla geçen tek bulgu sayılır"),
    "K9": ("EVET", "DS_ON_KAYIT.md: DS_ESIK sha, ds_esik.json (eğitim eşikleri SAYI), ds_prefix.json, kod sha'ları, girdi sha'ları, getirisiz huni; "
                   "ds_kos kapısı sha + git (işlenmiş ve değişmemiş) + ik_kontrol_kapisi denetler, eşikleri yeniden hesaplayıp json ile eşitler; "
                   "ön kayıt commit'i koşudan önce; ikinci koşu DURUR"),
    "K10": ("EVET", "sınıf I yalnız OHLCV (UYGULANMAZ); sınıf II sec_ozet: form adları 'SC 13G' + 'SCHEDULE 13G' birlikte, 8-K madde kodu virgülle "
                    "ayrılmış alan, başvuru günü + 1 işlem günü; ham sec_ozet'ten 3 satır ön kayıtta elle gösterildi"),
    "K11": ("EVET", "ds_olay.csv.gz satır dosyası; DS_RAPOR.md YENİDEN ÜRETİM iki hücre (DS01 ABD sınama, DS09 AVR eğitim) düz pandas ile + 50 rastgele "
                    "olayın h5'i bağımsız döngüyle yeniden simüle; fark > 1e-12 DURUR"),
    "K12": ("EVET", "etiket yalnız karne v3 + BH kuralıyla; 'iz / emare / anlamlı' yazılmaz; FARK yüzde puan h5 (stop'tan önce +%5 payı), getiri "
                    "değil; sayı ve yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_ds; ds_ / DS_ önekli adlar dışında ezme DURUR; test_dusus_sonrasi); yasak defter dosyalarına ve "
                    "YAPI_HEDEF.py'ye dokunulmadı (git diff); e-posta / anahtar taraması (YH._yh_yaz); dış servis yok; kod değişti -> 'çalışma "
                    "zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


class DSHata(RuntimeError):
    """Durdurucu hata: veri yok, mühür / sha tutmuyor, prefix tutmadı, ikinci koşu, girdi bozuk."""


# ================================================================ 0) ORTAK
def _ds_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def ds_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(DS_ESIK if E is None else E)


def _ds_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or DS_YOL["cikti"], DS_DOSYA.get(ad, ad))


def _ds_json(o: Any) -> Any:
    return YH._yh_json(o)


def _ds_yaz(yol: str, metin: str, ad: str) -> None:
    YH._yh_yaz(yol, metin, ad)


def _ds_q(x: np.ndarray, q: float) -> float:
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return float(np.quantile(x, q)) if len(x) else float("nan")


def _ds_kay(x: np.ndarray, k: int) -> np.ndarray:
    return YH._yh_kaydir(np.asarray(x, float), k)


# ================================================================ 1) VERİ
def ds_veri(pazar: str, klasor: Optional[str] = None) -> Dict[str, Any]:
    """OC.oc_veri (evren dışı listesi uygulanır; k34 yüklenmez) + açılış temizliği. 'temiz': {sembol: kırpılan tarihler}."""
    Vd = OC.oc_veri(pazar, klasor=klasor or DS_YOL["veri"], veri2=DS_YOL["veri2_yok"])
    Vd["temiz"] = {}; n = 0
    for s, d in Vd["V"].items():
        bad = ((d.Open > d.High) | (d.Open < d.Low)).to_numpy()
        if bad.any():
            d = d.copy(); d.loc[bad, "Open"] = np.clip(d.Open.to_numpy(float), d.Low.to_numpy(float), d.High.to_numpy(float))[bad]
            Vd["V"][s] = d; Vd["temiz"][s] = pd.DatetimeIndex(d.index[bad]); n += int(bad.sum())
    Vd["temiz_n"] = n
    Vd["not"].append(f"açılış H-L dışı kırpılan bar: {n} ({len(Vd['temiz'])} hisse)")
    return Vd


def ds_baglam(Vd: Dict[str, Any]) -> Dict[str, Any]:
    """Evren eşit ağırlıklı günlük getiri rm (birleşik takvim), endeks E = cumprod(1 + rm), r21 referansı (ABD sektör / evren ortalaması).
    Hepsi aynı gün ve öncesi verisinden (K2)."""
    V = Vd["V"]; S = sorted(V)
    idx = pd.DatetimeIndex(sorted(set().union(*[V[s].index for s in S])))
    R = pd.DataFrame({s: V[s].Close.pct_change() for s in S}).reindex(idx)
    say = R.notna().sum(1)
    rm = R.mean(1).where(say >= 10)
    E = (1 + rm.fillna(0.0)).cumprod()
    R21 = pd.DataFrame({s: V[s].Close / V[s].Close.shift(21) - 1 for s in S}).reindex(idx)
    evren21 = R21.mean(1).where(R21.notna().sum(1) >= 5)
    ref = {s: evren21 for s in S}; sek_ad: Dict[str, str] = {}
    if Vd["pazar"] == "ABD" and os.path.exists(DS_YOL["sektor"]):
        sk = pd.read_csv(DS_YOL["sektor"]); sk["s"] = sk.sembol.astype(str).str.split(".").str[0]
        sk = sk[(sk.sektor.astype(str) != "BILINMIYOR") & sk.s.isin(S)].drop_duplicates("s")
        for sek, g in sk.groupby("sektor"):
            uy = list(g.s)
            m = R21[uy].mean(1).where(R21[uy].notna().sum(1) >= 5)
            m = m.where(m.notna(), evren21)
            for s in uy:
                ref[s] = m; sek_ad[s] = str(sek)
    return {"rm": rm, "E": E, "r21ref": ref, "sektor": sek_ad, "idx": idx}


# ================================================================ 2) ÖZELLİKLER (hisse başına; yalnız t ve öncesi)
_DS_HAM = ["f15", "dus", "liq", "atrp", "hat", "close", "konv10", "devir", "art21", "evre4", "dus04", "ds05", "aralik", "clv", "ts06", "sm07",
           "rsi2", "dv2", "c7", "elder", "td9", "choch", "busted", "ds16_var", "ds16_e", "ds16_v", "ds16_r", "direnc", "rsg", "pb1", "pb2", "gap19",
           "der19", "yuru", "gece", "dol22", "mik23", "av_up", "av_touch", "derin"]


def _ds_pivot(x: np.ndarray, k: int, yuksek: bool) -> np.ndarray:
    """6/6 pivot (k = 6): x_p sol k ve sağ k bardan KESİN büyük (yüksek) / küçük (alçak). Sağ pencere eksikse yanlış (onaylanmamış)."""
    s = pd.Series(x if yuksek else -x)
    sol = s.rolling(k, min_periods=k).max().shift(1)
    sag = s[::-1].rolling(k, min_periods=k).max()[::-1].shift(-1)
    with np.errstate(invalid="ignore"):
        return ((s > sol) & (s > sag)).to_numpy()


def _ds_s6_busted(df: pd.DataFrame, L: np.ndarray, C: np.ndarray) -> np.ndarray:
    """DS15: son S6 KIRILDI bölgesi; min L >= 0,90 x kutu_alt korunurken C > kutu_ust ilk kez. S6_TABAN (nedensel) içe alınır."""
    out = np.zeros(len(C))
    try:
        T = S6.s6_taban(YH._yh_hazir(df), None).reindex(df.index)
    except Exception as ex:   # S6 kısa / bozuk seride hata verebilir: özellik NaN
        dslog.debug("S6 hesaplanamadı: %s", ex)
        return np.full(len(C), np.nan)
    kir = T["kirildi"].fillna(False).to_numpy(bool); bid = T["bolge_id"].fillna(-1).to_numpy(int)
    ka = T["kutu_alt"].to_numpy(float); ku = T["kutu_ust"].to_numpy(float)
    aktif = False; Lb = Hb = mn = np.nan
    for i in range(len(C)):
        if kir[i] and bid[i] >= 0 and np.isfinite(ka[i]) and np.isfinite(ku[i]):
            aktif = True; Lb, Hb, mn = ka[i], ku[i], L[i]
            continue
        if aktif:
            mn = min(mn, L[i])
            if mn < 0.90 * Lb:
                aktif = False
            elif C[i] > Hb:
                out[i] = 1.0; aktif = False
    return out


def ds_ozellik_hisse(df: pd.DataFrame, pazar: str, bag: Dict[str, Any], sembol: str, esik: Optional[Dict[str, Any]] = None,
                     temiz: Optional[pd.DatetimeIndex] = None) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Bir hissenin DS günleri ve ham özellikleri (_DS_HAM). esik = pazarın eğitim eşikleri (DS05 q / m için; yoksa DS05 / DS16 NaN).
    Döner: (DS günleri tablosu, ATRP serisi (t), DS bayrağı serisi (t)). Her değer yalnız [.., t] barlarından."""
    Eo = DS_ESIK["olay"]; ix = df.index; N = len(df)
    bos = pd.DataFrame(columns=["sembol", "tarih"] + _DS_HAM)
    if N < Eo["pencere"]:          # DS (a) / (b) 120 bar ister; daha sıkı uzunluk şartı prefix'i bozar (veri sonuna bakar)
        return bos, pd.Series(np.nan, index=ix), pd.Series(False, index=ix)
    O, H, L, C, V = (df[k].to_numpy(float) for k in ("Open", "High", "Low", "Close", "Volume"))
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
    pC = _ds_kay(C, 1)
    TR = np.where(np.isfinite(pC), np.maximum(H, pC) - np.minimum(L, pC), H - L)
    atr14 = pd.Series(TR).rolling(14, min_periods=14).mean().to_numpy(); atr20 = pd.Series(TR).rolling(20, min_periods=20).mean().to_numpy()
    atrp = atr14 / C
    s_atrp = pd.Series(atrp, index=ix); s_ds = pd.Series(ds, index=ix)
    di = np.flatnonzero(ds)
    if not len(di):
        return bos, s_atrp, s_ds
    with np.errstate(invalid="ignore", divide="ignore"):
        r = C / pC - 1
        F: Dict[str, np.ndarray] = {"f15": f15, "dus": dus, "liq": liq, "atrp": atrp, "close": C}
        F["hat"] = pd.Series(L).rolling(Eo["hat_gun"], min_periods=Eo["hat_gun"]).min().to_numpy()
        M = (_ds_kay(C, 9) + C) / 2; F["konv10"] = (M - c.rolling(10, min_periods=10).mean().to_numpy()) / M
        sv = pd.Series(V)
        F["devir"] = sv.rolling(21, min_periods=21).mean().to_numpy() / sv.rolling(252, min_periods=252).median().to_numpy()
        ref = bag["r21ref"].get(sembol)
        r21 = C / _ds_kay(C, 21) - 1
        F["art21"] = r21 - (ref.reindex(ix).to_numpy(float) if ref is not None else np.nan)
        sma150 = c.rolling(150, min_periods=150).mean().to_numpy(); eg = sma150 / _ds_kay(sma150, 20) - 1
        F["evre4"] = np.where(np.isfinite(eg) & np.isfinite(sma150), ((eg < 0) & (C < sma150)).astype(float), np.nan)
        big = np.where(np.isfinite(r), (r <= -0.15).astype(float), 0.0)
        F["dus04"] = pd.Series(big).shift(2).rolling(22, min_periods=22).max().to_numpy()
        hl = H - L
        F["aralik"] = hl / _ds_kay(atr20, 1)
        F["clv"] = ((C - L) - (H - C)) / hl
        v20 = _ds_kay(sv.rolling(20, min_periods=20).mean().to_numpy(), 1)
        F["ds05"] = np.full(N, np.nan); doruk_son = np.full(N, -1)
        if esik is not None:
            cond = (C < pC) & (F["aralik"] >= esik["DS05_q"]) & (V >= 2 * v20) & (F["clv"] >= esik["DS05_m"])
            cond = np.where(np.isfinite(F["aralik"]) & np.isfinite(v20), cond, False)
            F["ds05"] = pd.Series(cond.astype(float)).rolling(60, min_periods=60).max().to_numpy()
            son = -1
            for i in range(N):
                if cond[i]:
                    son = i
                doruk_son[i] = son if (son >= 0 and i - son <= 59) else -1
        m20 = _ds_kay(pd.Series(L).rolling(8, min_periods=8).min().to_numpy(), 2)
        F["sm07"] = np.where(np.isfinite(m20) & np.isfinite(_ds_kay(L, 2)),
                             ((_ds_kay(C, 1) < _ds_kay(L, 2)) & (_ds_kay(L, 1) < m20) & (H > _ds_kay(H, 1))).astype(float), np.nan)
        dlt = np.r_[0.0, np.diff(C)]
        ag = pd.Series(np.maximum(dlt, 0)).ewm(alpha=0.5, adjust=False).mean().to_numpy()
        al_ = pd.Series(np.maximum(-dlt, 0)).ewm(alpha=0.5, adjust=False).mean().to_numpy()
        F["rsi2"] = np.where(al_ > 0, 100 - 100 / (1 + ag / np.where(al_ > 0, al_, 1)), 100.0)
        F["rsi2"][:3] = np.nan
        x2 = pd.Series(C / ((H + L) / 2) - 1).rolling(2, min_periods=2).mean()
        F["dv2"] = (x2.rolling(252, min_periods=252).rank(pct=True) * 100).to_numpy()
        F["c7"] = np.where(np.arange(N) >= 6, (C <= c.rolling(7, min_periods=7).min().to_numpy()).astype(float), np.nan)
        e13 = c.ewm(span=13, adjust=False).mean().to_numpy()
        macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
        hist = (macd - macd.ewm(span=9, adjust=False).mean()).to_numpy()
        kir = (e13 < _ds_kay(e13, 1)) & (hist < _ds_kay(hist, 1))
        F["elder"] = np.where(np.arange(N) >= 35, (np.r_[False, kir[:-1]] & ~kir).astype(float), np.nan)
        cd = np.where(np.isfinite(_ds_kay(C, 4)), C < _ds_kay(C, 4), False)
        cnt = np.zeros(N, int)
        for i in range(N):
            cnt[i] = (cnt[i - 1] + 1 if i else 1) if cd[i] else 0
        F["td9"] = np.where(np.arange(N) >= 12, (cnt == 9).astype(float), np.nan)
        sd20 = c.rolling(20, min_periods=20).std(ddof=0).to_numpy(); mid = c.rolling(20, min_periods=20).mean().to_numpy()
        alt = mid - 2 * sd20; ust = mid + 2 * sd20
        pb = (C - alt) / (ust - alt)
        below = np.where(np.isfinite(alt), (C < alt).astype(float), np.nan)
        F["yuru"] = pd.Series(below).rolling(10, min_periods=10).sum().to_numpy()
        lg = np.log(O / pC); lt = np.log(C / pC)
        sg = pd.Series(lg).rolling(20, min_periods=20).sum().to_numpy(); st_ = pd.Series(lt).rolling(20, min_periods=20).sum().to_numpy()
        gece = np.where(st_ < 0, sg / st_, np.nan)
        if temiz is not None and len(temiz):
            tm = ix.isin(temiz).astype(float)
            gece = np.where(pd.Series(tm).rolling(20, min_periods=1).max().to_numpy() > 0, np.nan, gece)
        F["gece"] = gece
        rm = bag["rm"].reindex(ix).to_numpy(float)
        mk = np.isfinite(rm) & (rm < 0) & np.isfinite(r)
        num = pd.Series(np.where(mk, r - rm, 0.0)).rolling(40, min_periods=40).sum().to_numpy()
        den = pd.Series(mk.astype(float)).rolling(40, min_periods=40).sum().to_numpy()
        F["direnc"] = np.where(den > 0, num / np.where(den > 0, den, 1), np.nan)
        RS = C / bag["E"].reindex(ix).to_numpy(float)
        s22 = pd.Series(RS).rolling(22, min_periods=22).mean().to_numpy()
        a1, a2 = _ds_kay(s22, 1), _ds_kay(s22, 2)
        F["rsg"] = np.where(np.isfinite(a1) & np.isfinite(a2), (a1 > a2).astype(float), np.nan)
        F["derin"] = C / c.rolling(252, min_periods=252).max().to_numpy() - 1
        sig = _ds_kay(pd.Series(r).rolling(20, min_periods=20).std().to_numpy(), 1)
        gapd = np.where(np.isfinite(sig) & np.isfinite(r), r <= -2 * sig, False)
    F["busted"] = _ds_s6_busted(df, L, C)
    ph = np.flatnonzero(_ds_pivot(H, 6, True)); pl = np.flatnonzero(_ds_pivot(L, 6, False)); gi = np.flatnonzero(gapd)
    tp = (H + L + C) / 3
    for k in ("ts06", "choch", "ds16_var", "ds16_e", "ds16_v", "ds16_r", "pb1", "pb2", "gap19", "der19", "dol22", "mik23", "av_up", "av_touch"):
        F[k] = np.full(N, np.nan)
    for t in di:
        # DS06 Turtle Soup
        if t >= 21 and np.isfinite(atr14[t - 1]):
            wl = L[t - 20:t]; m_ = wl.min(); pos = t - 20 + int(np.flatnonzero(wl == m_)[-1])
            F["ts06"][t] = float(L[t] < m_ and t - pos >= 4 and C[t] >= m_ and (H[t] - L[t]) <= 3 * atr14[t - 1])
        # DS14 CHoCH (onaylı tepe p + 6 <= t)
        k_ = np.searchsorted(ph, t - 6, side="right")
        if t >= 30:
            F["choch"][t] = float(k_ >= 2 and H[ph[k_ - 2]] > H[ph[k_ - 1]] and C[t - 1] <= H[ph[k_ - 1]] < C[t])
        # DS19 %b W dip (onaylı dip p + 6 <= t)
        k_ = np.searchsorted(pl, t - 6, side="right")
        if k_ >= 2:
            d1, d2 = pl[k_ - 2], pl[k_ - 1]
            F["pb1"][t], F["pb2"][t] = pb[d1], pb[d2]; F["gap19"][t] = d2 - d1; F["der19"][t] = L[d2] / L[d1] - 1
        # DS22 / DS23 aşağı 2 sigma günleri
        if t >= 80:
            a = gi[(gi >= t - 59) & (gi <= t - 1)]
            F["dol22"][t] = float(any(C[t] >= C[i - 1] and (C[i:t].max() < C[i - 1]) for i in a if i >= 1))
            b = gi[(gi >= t - 119) & (gi <= t)]
            F["mik23"][t] = float(any((C[i:t + 1].max() < C[i - 1]) and 0.05 < C[i - 1] / C[t] - 1 <= 0.10 for i in b if i >= 1))
        # DS25 AVWAP (dipten çapalı)
        if t >= 119:
            a0 = t - 119 + int(np.argmin(L[t - 119:t + 1])); vv = V[a0:t + 1].sum()
            if vv > 0:
                av = float((tp[a0:t + 1] * V[a0:t + 1]).sum() / vv)
                F["av_up"][t] = float(C[t] > av); F["av_touch"][t] = float(L[t - 2:t + 1].min() / av - 1)
        # DS16 ikinci test (DS05 doruğu; esik gerekli)
        if esik is not None and np.isfinite(F["ds05"][t]):
            s = doruk_son[t]
            if s >= 0 and t >= s + 5:
                u = s + 5 + int(np.argmin(L[s + 5:t + 1]))
                F["ds16_var"][t] = 1.0; F["ds16_e"][t] = abs(L[u] / L[s] - 1); F["ds16_v"][t] = V[u] / V[s]
                F["ds16_r"][t] = (H[u] - L[u]) / (H[s] - L[s])
            else:
                F["ds16_var"][t] = 0.0
    T = pd.DataFrame({k: np.asarray(F[k], float)[di] for k in _DS_HAM})
    T.insert(0, "tarih", ix[di]); T.insert(0, "sembol", sembol)
    return T, s_atrp, s_ds


_DS_IS: Dict[str, Any] = {}


def _ds_oz_isci(semboller: List[str]) -> List[Tuple[str, pd.DataFrame, pd.Series, pd.Series]]:
    Vd, bag, esik = _DS_IS["Vd"], _DS_IS["bag"], _DS_IS["esik"]; out = []
    for s in semboller:
        try:
            T, a, d = ds_ozellik_hisse(Vd["V"][s], Vd["pazar"], bag, s, esik, Vd["temiz"].get(s))
        except Exception as ex:
            raise DSHata(f"özellik hesaplanamadı {Vd['pazar']} {s}: {ex}") from ex
        out.append((s, T, a, d))
    return out


def ds_ozellik_pazar(Vd: Dict[str, Any], bag: Dict[str, Any], esik: Optional[Dict[str, Any]], islem: int = 1) -> Dict[str, Any]:
    """Pazarın bütün hisseleri: DS günleri tablosu + ATRP / DS bayrağı serileri (hissenin t'si)."""
    global _DS_IS
    S = sorted(Vd["V"]); _DS_IS = {"Vd": Vd, "bag": bag, "esik": esik}
    if islem > 1:
        import multiprocessing as mp
        parca = [list(p) for p in np.array_split(np.array(S, dtype=object), islem * 6) if len(p)]
        with mp.get_context("fork").Pool(islem) as hv:
            R = [x for y in hv.map(_ds_oz_isci, parca) for x in y]
    else:
        R = _ds_oz_isci(S)
    _DS_IS = {}
    tab = [x[1] for x in R if len(x[1])]
    T = pd.concat(tab, ignore_index=True) if tab else pd.DataFrame(columns=["sembol", "tarih"] + _DS_HAM)
    return {"T": T, "atrp": {x[0]: x[2] for x in R}, "ds": {x[0]: x[3] for x in R}}


# ================================================================ 3) OLAY KÜMESİ, ANA, KOVA, DÖNEM
def ds_olay_kur(Z: Dict[str, Any], P: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """DS günleri -> OC.oc_olay_hazirla (tekil_gun = 1: bütün DS günleri; giriş, havuz) -> ANA (15 gün tekil). Döner (tablo, sayım)."""
    T = Z["T"]
    E1 = json.loads(json.dumps(OC.OC_ESIK)); E1["olay"]["tekil_gun"] = 1
    ol = pd.DataFrame({"sembol": T.sembol, "tarih": pd.to_datetime(T.tarih), "pazar": P["pazar"]})
    X, say = OC.oc_olay_hazirla(ol, P, E1)
    X = X.merge(T.assign(tarih=pd.to_datetime(T.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
    X = X.sort_values(["sembol", "d"], kind="mergesort").reset_index(drop=True)
    ana = np.zeros(len(X), bool); son: Dict[str, int] = {}
    for i, (s, d) in enumerate(zip(X.sembol.to_numpy(), X.d.to_numpy(int))):
        if s not in son or d - son[s] >= DS_ESIK["olay"]["tekil_bar"]:
            ana[i] = True; son[s] = d
    X["ana"] = ana
    say.update({"ds_gun": int(len(T)), "havuz_gun": int(len(X)), "ana": int(ana.sum())})
    return X, say


def ds_donem(X: pd.DataFrame, P: Dict[str, Any], amb: Optional[str] = None) -> Tuple[np.ndarray, str]:
    """egitim / sinama / ambargo / dis. amb: sınama ilk izinli giriş günü (ds_esik.json); yoksa ANA eğitimden hesaplanır."""
    g = pd.to_datetime(X.giris); Dn = DS_ESIK["donem"]
    eg = (g >= Dn["egitim"][0]) & (g <= Dn["egitim"][1]); sn = (g >= Dn["sinama"][0]) & (g <= Dn["sinama"][1])
    if amb is None:
        son = pd.to_datetime(X.loc[eg & X.ana, "giris"]).max()
        if pd.isna(son):
            raise DSHata(f"{P.get('pazar', '?')}: eğitim döneminde DS ANA olayı yok (ambargo hesaplanamaz)")
        k = P["tarih"].get_loc(son) + DS_ESIK["donem"]["ambargo_bar"]
        amb = str(P["tarih"][min(k, len(P["tarih"]) - 1)].date())
    out = np.where(eg, "egitim", np.where(sn & (g >= pd.Timestamp(amb)), "sinama", np.where(sn, "ambargo", "dis")))
    return out, amb


def ds_esik_hesap(X: pd.DataFrame, asama: str = "A") -> Dict[str, float]:
    """Eğitim ANA olaylarından eşikler (getirisiz). asama 'A': DS05 / DS16 hariç; 'B': yalnız DS16 (DS05 q / m ile hesaplanmış ham)."""
    g = X[X.ana & (X.donem == "egitim")]
    if asama == "B":
        v = g[g.ds16_var == 1]
        return {"DS16_e": _ds_q(v.ds16_e, 0.5), "DS16_q1": _ds_q(v.ds16_v, 0.5), "DS16_q2": _ds_q(v.ds16_r, 0.5), "n_DS16": int(len(v))}
    q = DS_ESIK["kova"]["q"]
    return {"KONV10_q20": _ds_q(g.konv10, 0.20), "DEVIR_q10": _ds_q(g.devir, 0.10), "ART21_q10": _ds_q(g.art21, 0.10),
            "DIRENC_q75": _ds_q(g.direnc, 0.75), "YURU_q75": _ds_q(g.yuru, 0.75), "GECE_q75": _ds_q(g.gece, 0.75),
            "DS05_q": _ds_q(g.aralik, 0.75), "DS05_m": _ds_q(g.clv, 0.50),
            "DS19_Q1": _ds_q(g.gap19, 0.25), "DS19_Q3": _ds_q(g.gap19, 0.75), "DS19_tol": _ds_q(np.abs(g.der19), 0.50),
            "DS25_e": _ds_q(g.loc[g.av_up == 1, "av_touch"], 0.50),
            "ATRP_t1": _ds_q(g.atrp, q[0]), "ATRP_t2": _ds_q(g.atrp, q[1]), "n_egitim_ana": int(len(g))}


def _ds_b(cond: np.ndarray, var: np.ndarray) -> np.ndarray:
    """İkili özellik: var (ham değer sonlu) değilse NaN."""
    return np.where(var, np.asarray(cond, bool).astype(float), np.nan)


def ds_ikili(X: pd.DataFrame, e: Dict[str, float]) -> pd.DataFrame:
    """Ham sütunlar + pazar eşikleri -> F_DS01..F_DS28 (1 / 0 / NaN)."""
    f = lambda k: X[k].to_numpy(float)  # noqa: E731
    fin = lambda k: np.isfinite(f(k))  # noqa: E731
    with np.errstate(invalid="ignore"):
        B = {
            "DS01": _ds_b(f("konv10") <= e["KONV10_q20"], fin("konv10")),
            "DS02": _ds_b(f("devir") <= e["DEVIR_q10"], fin("devir")),
            "DS03": _ds_b(f("art21") <= e["ART21_q10"], fin("art21")),
            "DS04": _ds_b(f("dus04") == 1, fin("dus04")),
            "DS05": _ds_b(f("ds05") == 1, fin("ds05")),
            "DS06": _ds_b(f("ts06") == 1, fin("ts06")),
            "DS07": _ds_b(f("sm07") == 1, fin("sm07")),
            "DS08": _ds_b(f("evre4") == 1, fin("evre4")),
            "DS09": _ds_b(f("rsi2") <= 5, fin("rsi2")),
            "DS10": _ds_b(f("dv2") < 10, fin("dv2")),
            "DS11": _ds_b(f("c7") == 1, fin("c7")),
            "DS12": _ds_b(f("elder") == 1, fin("elder")),
            "DS13": _ds_b(f("td9") == 1, fin("td9")),
            "DS14": _ds_b(f("choch") == 1, fin("choch")),
            "DS15": _ds_b(f("busted") == 1, fin("busted")),
            "DS16": _ds_b((f("ds16_var") == 1) & (f("ds16_e") <= e["DS16_e"]) & (f("ds16_v") < e["DS16_q1"]) & (f("ds16_r") < e["DS16_q2"]),
                          fin("ds16_var")),
            "DS17": _ds_b(f("direnc") >= e["DIRENC_q75"], fin("direnc")),
            "DS18": _ds_b(f("rsg") == 1, fin("rsg")),
            "DS19": np.where(fin("pb1"), ((f("pb1") <= 0) & (f("pb2") > 0) & (f("gap19") >= e["DS19_Q1"]) & (f("gap19") <= e["DS19_Q3"])
                                          & (f("der19") <= e["DS19_tol"])).astype(float), np.where(np.isfinite(f("f15")), 0.0, np.nan)),
            "DS20": _ds_b(f("yuru") >= e["YURU_q75"], fin("yuru")),
            "DS21": _ds_b(f("gece") >= e["GECE_q75"], fin("gece")),
            "DS22": _ds_b(f("dol22") == 1, fin("dol22")),
            "DS23": _ds_b(f("mik23") == 1, fin("mik23")),
            "DS25": _ds_b((f("av_up") == 1) & (f("av_touch") <= e["DS25_e"]), fin("av_up")),
            "DS28": _ds_b(f("derin") <= -0.60, fin("derin")),
        }
    return pd.DataFrame({f"F_{k}": B[k] for k in DS_HIP_SIRA}, index=X.index)


def ds_kova(X: pd.DataFrame, e: Dict[str, float]) -> np.ndarray:
    a = X.atrp.to_numpy(float)
    at = np.where(np.isfinite(a), np.where(a <= e["ATRP_t1"], 0, np.where(a <= e["ATRP_t2"], 1, 2)), -1)
    lq = X.hucre.to_numpy(int) % 3
    return np.where((at >= 0) & (X.hucre.to_numpy(int) >= 0), at * 3 + lq, -1)


# ================================================================ 4) SINIF II (ABD-olay; sec_ozet; BİLGİ)
def ds_sec_yukle(k55: Optional[str] = None) -> Optional[Dict[str, Any]]:
    k55 = k55 or DS_YOL["k55"]
    y1, y2 = os.path.join(k55, "sec_ozet.json"), os.path.join(k55, "sembol_cik.json")
    if not (os.path.exists(y1) and os.path.exists(y2)):
        return None
    J = json.load(open(y1, encoding="utf-8")); SC = json.load(open(y2, encoding="utf-8"))
    return {"J": J, "SC": SC, "sha": OC._oc_sha_dosya(y1)}


def _ds_sec_olay(v: Dict[str, Any]) -> Dict[str, List[pd.Timestamp]]:
    out: Dict[str, List[pd.Timestamp]] = {k: [] for k in ("144", "13G", "2.03", "2.04", "1.02", "3.03", "5.02", "2.02")}
    for f, t, it in zip(v.get("form", []), v.get("date", []), v.get("items", [""] * len(v.get("form", [])))):
        try:
            tt = pd.Timestamp(t)
        except (ValueError, TypeError):
            continue
        if f == "144":
            out["144"].append(tt)
        elif f in ("SC 13G", "SCHEDULE 13G"):
            out["13G"].append(tt)
        elif f == "8-K" and it:
            ms = {m.strip() for m in str(it).split(",")}
            for m in ("2.03", "2.04", "1.02", "3.03", "5.02", "2.02"):
                if m in ms:
                    out[m].append(tt)
    return out


def ds_sinif2(X: pd.DataFrame, Vd: Dict[str, Any], bag: Dict[str, Any], sec: Optional[Dict[str, Any]]) -> pd.DataFrame:
    """ABD DS tablosu satırlarına F_DS47..F_DS53 (1 / 0; kapsam dışı hisse NaN). Bilgi barı = başvuru gününden SONRAKİ ilk geçerli bar."""
    kol = [f"F_{k}" for k in DS_SINIF2]
    out = pd.DataFrame(np.nan, index=X.index, columns=kol)
    if sec is None or not len(X):
        return out
    J, SC = sec["J"], sec["SC"]; rmE = bag["E"]
    for s, g in X.groupby("sembol"):
        cik = SC.get(s)
        if cik is None or str(cik) not in J:
            continue
        df = Vd["V"][s]; ix = df.index; C = df.Close.to_numpy(float); Ee = rmE.reindex(ix).to_numpy(float)
        ev = _ds_sec_olay(J[str(cik)])
        b = {k: np.sort(np.searchsorted(ix, pd.DatetimeIndex(v), side="right")) for k, v in ev.items()}
        ti = ix.get_indexer(pd.DatetimeIndex(g.tarih))

        def var(k: str, a: int, z: int) -> np.ndarray:
            x = b[k]
            return np.array([bool(((x >= t + a) & (x <= t + z)).any()) for t in ti], float)
        out.loc[g.index, "F_DS48"] = var("144", -20, -1)
        out.loc[g.index, "F_DS49"] = var("13G", -60, 0)
        out.loc[g.index, "F_DS50"] = var("2.03", -20, 0)
        out.loc[g.index, "F_DS51"] = var("2.04", -60, 0)
        out.loc[g.index, "F_DS52"] = var("1.02", -20, 0)
        out.loc[g.index, "F_DS53"] = var("3.03", -60, 0)
        # DS47: 5.02 sonrası ilk 2.02 (bilgi barı i0 = başvuru sonrası ilk bar - 1 değil: i0 = başvuru günü ya da sonraki ilk bar)
        hed = set()
        d502 = pd.DatetimeIndex(ev["5.02"]).sort_values(); d202 = pd.DatetimeIndex(ev["2.02"]).sort_values()
        for a in d502:
            sonra = d202[d202 > a]
            if not len(sonra):
                continue
            f2 = sonra[0]; i0 = int(np.searchsorted(ix, f2, side="left"))
            if i0 - 2 < 0 or i0 + 2 >= len(ix):
                continue
            with np.errstate(invalid="ignore", divide="ignore"):
                tep = (C[i0 + 1] / C[i0 - 2] - 1) - (Ee[i0 + 1] / Ee[i0 - 2] - 1)
            if np.isfinite(tep) and tep < 0 and (ix[i0 + 2] - a).days <= 180:
                hed.add(i0 + 2)
        out.loc[g.index, "F_DS47"] = np.array([float(t in hed) for t in ti])
    return out


# ================================================================ 5) ÖLÇÜM (yh_sim; olay + DS içi adaylar + DS dışı eş)
_DS_SIM: Dict[str, Any] = {}


def _ds_sim_isci(ev: np.ndarray) -> Dict[str, Any]:
    G = _DS_SIM; P, Cl = G["P"], G["Cl"]; Y = YH.YH_ESIK; R = int(Y["olcu"]["pencere_azami"]); me = int(DS_ESIK["olcu"]["es_min"])
    Op, Hi, Lo, ok, Hc = P["Op"], P["Hi"], P["Lo"], P["ok"], P["H"]
    X = G["X"]; dA, jA, kv, hat = X.d.to_numpy(int), X.j.to_numpy(int), X.kova.to_numpy(int), X.hat.to_numpy(float)
    DSg, KVg = G["DSg"], G["KVg"]; grp = G["grp"]; hc = float(Y["olcu"]["stop0"]["hat_carpan"])
    kol = ["dd", "olc", "h5", "h10", "st5", "h5H", "k5", "kst", "getiri", "cikis_bar", "cikis_tur", "dsd_h5", "dsd_h10", "dsd_st5", "dsd_n",
           "oc_h5", "oc_st5", "oc_n", "n_aday"]
    res = {k: [] for k in kol}; ce, cr, c5, c10, cst = [], [], [], [], []
    for e in ev:
        d, j, k = int(dA[e]), int(jA[e]), int(kv[e]); E0 = float(Op[d, j]); st0 = hat[e] * hc
        dd = 1 - st0 / E0 if (np.isfinite(E0) and E0 > 0 and np.isfinite(st0)) else np.nan
        sat = dict.fromkeys(kol, np.nan); sat["olc"] = False; sat["cikis_tur"] = ""; sat["dd"] = dd
        if not (np.isfinite(dd) and dd > 0) or k < 0:
            sat["cikis_tur"] = "giris_stop_otesi" if k >= 0 else "kova_yok"
            for kk in kol:
                res[kk].append(sat[kk])
            continue
        hv = np.flatnonzero(ok[d])
        Ek = Op[d, hv]; stk = Ek * (1 - dd); pj = int(np.searchsorted(hv, j)); stk[pj] = st0
        Sm = YH.yh_sim(YH._yh_pencere(Cl, d, R, hv), YH._yh_pencere(Hi, d, R, hv), YH._yh_pencere(Lo, d, R, hv), Ek, stk, 1, Y)
        olc = Sm["olc"]
        sat["olc"] = bool(olc[pj])
        if sat["olc"]:
            for kk in ("h5", "h10", "st5", "h5H"):
                sat[kk] = float(Sm[kk][pj])
            sat["k5"] = int(Sm["k5"][pj]); sat["kst"] = int(Sm["kst"][pj])
        # DS içi adaylar (aynı gün, aynı kova, olay hissesi hariç)
        rows = grp.get((d, k), np.array([], int)); rows = rows[jA[rows] != j]
        pos = np.searchsorted(hv, jA[rows]); sat["n_aday"] = int(len(rows))
        if len(rows):
            m = olc[pos]
            ce.append(np.full(len(rows), e)); cr.append(rows)
            c5.append(np.where(m, Sm["h5"][pos], np.nan)); c10.append(np.where(m, Sm["h10"][pos], np.nan)); cst.append(np.where(m, Sm["st5"][pos], np.nan))
        # DS dışı eş (bilgi)
        mm = olc & ~DSg[d, hv] & (KVg[d, hv] == k); mm[pj] = False; sat["dsd_n"] = int(mm.sum())
        if mm.sum() >= me:
            sat["dsd_h5"] = float(Sm["h5"][mm].mean()); sat["dsd_h10"] = float(Sm["h10"][mm].mean()); sat["dsd_st5"] = float(Sm["st5"][mm].mean())
        mo = olc & (Hc[d, hv] == Hc[d, j]); mo[pj] = False; sat["oc_n"] = int(mo.sum())
        if mo.sum() >= me:
            sat["oc_h5"] = float(Sm["h5"][mo].mean()); sat["oc_st5"] = float(Sm["st5"][mo].mean())
        s = P["sembol"][j]; A = G["arr"][s]
        gi = int(np.searchsorted(A[4], P["tarih"][d].value))
        if sat["olc"] and gi < len(A[4]) and A[4][gi] == P["tarih"][d].value:
            g_, b_, t_ = YH.yh_getiri(A[0], A[1], A[2], A[3], gi, E0, st0, 1, Y)
            sat["getiri"], sat["cikis_bar"], sat["cikis_tur"] = g_, b_, t_
        for kk in kol:
            res[kk].append(sat[kk])
    cat = lambda L_, dt: np.concatenate(L_) if L_ else np.array([], dt)  # noqa: E731
    return {"ev": ev, "res": res, "ce": cat(ce, int), "cr": cat(cr, int), "c5": cat(c5, float), "c10": cat(c10, float), "cst": cat(cst, float)}


def ds_olc(X: pd.DataFrame, P: Dict[str, Any], Vd: Dict[str, Any], Z: Dict[str, Any], islem: int = 1) -> Tuple[pd.DataFrame, Dict[str, np.ndarray]]:
    """X: bütün DS havuz günleri (kova, hat, ana). ANA olaylar ölçülür; adaylar = aynı gün aynı kova bütün DS günleri. Döner (ANA satırları, aday dizileri)."""
    global _DS_SIM
    idx = P["tarih"]; S = P["sembol"]; n, u = len(idx), len(S)
    DSg = pd.DataFrame({s: Z["ds"][s].shift(1).astype(float) for s in S}).reindex(idx).fillna(0).to_numpy(bool)
    AT = pd.DataFrame({s: Z["atrp"][s].shift(1) for s in S}).reindex(idx).to_numpy(float)
    e = Z["esik"]
    at = np.where(np.isfinite(AT), np.where(AT <= e["ATRP_t1"], 0, np.where(AT <= e["ATRP_t2"], 1, 2)), -1)
    KVg = np.where((at >= 0) & (P["H"] >= 0), at * 3 + P["H"] % 3, -1)
    grp: Dict[Tuple[int, int], np.ndarray] = {}
    kk = pd.DataFrame({"d": X.d.to_numpy(int), "k": X.kova.to_numpy(int)})
    for (d, k), g in kk[kk.k >= 0].groupby(["d", "k"]).groups.items():
        grp[(int(d), int(k))] = np.asarray(g, int)
    arr = {s: (Vd["V"][s].Open.to_numpy(float), Vd["V"][s].High.to_numpy(float), Vd["V"][s].Low.to_numpy(float), Vd["V"][s].Close.to_numpy(float),
               Vd["V"][s].index.values.astype("datetime64[ns]").astype(np.int64)) for s in S}
    _DS_SIM = {"P": P, "Cl": YH.yh_kapanis(P, Vd), "X": X, "DSg": DSg, "KVg": KVg, "grp": grp, "arr": arr}
    ev = np.flatnonzero(X.ana.to_numpy(bool) & np.isin(X.donem.to_numpy(object), ["egitim", "sinama"]))
    parca = [p for p in np.array_split(ev, max(1, islem * 8)) if len(p)]
    if islem > 1 and len(ev) > 200:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(islem) as hv:
            R = hv.map(_ds_sim_isci, parca)
    else:
        R = [_ds_sim_isci(p) for p in parca]
    _DS_SIM = {}
    A = X.iloc[ev].copy()
    for k in R[0]["res"]:
        A[k] = np.concatenate([np.asarray(r["res"][k], dtype=object if k == "cikis_tur" else float) for r in R])
    Cd = {k: np.concatenate([r[k] for r in R]) for k in ("ce", "cr", "c5", "c10", "cst")}
    return A, Cd


def ds_es_topla(A: pd.DataFrame, Cd: Dict[str, np.ndarray], Fall: pd.DataFrame, kod: str, me: int) -> Dict[str, np.ndarray]:
    """Özellik kod için her ANA olayın DS içi eş ortalaması: adayın F == 0 VE 15 bar ölçülebilir; en az me eş. Fall: X (bütün DS günleri) ikili tablo.
    Cd['ce'] = olayın X satır no'su; A.index = X satır no'su."""
    pos = pd.Index(A.index).get_indexer(Cd["ce"])
    Fc = Fall[f"F_{kod}"].to_numpy(float)[Cd["cr"]] if kod != "_hepsi" else np.zeros(len(Cd["cr"]))
    m = (Fc == 0) & np.isfinite(Cd["c5"]) & (pos >= 0)
    nA = len(A); cnt = np.bincount(pos[m], minlength=nA).astype(float)
    out = {"n_es": cnt}
    for ad, v in (("es_h5", Cd["c5"]), ("es_h10", Cd["c10"]), ("es_st5", Cd["cst"])):
        sm = np.bincount(pos[m], weights=v[m], minlength=nA)
        with np.errstate(invalid="ignore", divide="ignore"):
            out[ad] = np.where(cnt >= me, sm / np.where(cnt > 0, cnt, 1), np.nan)
    return out


# ================================================================ 6) HÜCRE, p, KARNE, BH
def ds_perm_p(X: pd.DataFrame, yon: str, R: int, tohum: int) -> float:
    """Ay kümeli işaret permütasyonu (X: h5, es_h5, giris)."""
    g = X[X.h5.notna() & X.es_h5.notna()]
    if not len(g):
        return float("nan")
    A = pd.DataFrame({"s": (g.h5 - g.es_h5).to_numpy(float), "n": 1.0,
                      "ay": pd.to_datetime(g.giris).dt.strftime("%Y-%m").to_numpy()}).groupby("ay")[["s", "n"]].sum()
    s = A.s.to_numpy(float); N = float(A.n.sum()); T = s.sum() / N
    rng = np.random.default_rng(int(tohum)); eps = rng.choice(np.array([-1.0, 1.0]), size=(int(R), len(s)))
    Ts = (eps @ s) / N
    if yon == "+":
        k = int((Ts >= T - 1e-15).sum())
    elif yon == "-":
        k = int((Ts <= T + 1e-15).sum())
    else:
        k = int((np.abs(Ts) >= abs(T) - 1e-15).sum())
    return float((1 + k) / (R + 1))


def _ds_p_yon(kod: str) -> str:
    h = DS_HIP.get(kod) or DS_SINIF2.get(kod) or {}
    return "?" if (h.get("iki") or h.get("yon") == "?") else h.get("yon", "?")


def ds_hucre(A: pd.DataFrame, es: Dict[str, np.ndarray], esH: Dict[str, np.ndarray], kod: str, pazar: str, hucre: str, tohum_ek: int) -> Dict[str, Any]:
    """Bir DS x pazar x hücre: n, FARK, stop, boot (ay kümeli; yh_d3_boot_l3o), L3O, güç (yh_d3_guc), p (permütasyon), ATRP tercil FARK'ları."""
    m0 = ((A.pazar == pazar) & (A.donem == hucre)).to_numpy()
    F = A[f"F_{kod}"].to_numpy(float)
    X = pd.DataFrame({"h5": A.h5.to_numpy(float), "es_h5": es["es_h5"], "st5": A.st5.to_numpy(float), "es_st5": es["es_st5"],
                      "giris": A.giris.to_numpy(), "kova": A.kova.to_numpy(int)}, index=A.index)
    sec = m0 & (F == 1); Xs = X[sec]
    c = YH.yh_d1_hucre(Xs); c["marjinal"] = c["fark"]
    c["n_tutan_ham"] = int(sec.sum()); c["n_tutmayan_ham"] = int((m0 & (F == 0)).sum())
    g = Xs[Xs.h5.notna() & Xs.es_h5.notna()]
    c["h5_med"] = float(np.median(g.h5)) if len(g) else np.nan
    c.update(YH.yh_d3_boot_l3o(g, g.assign(h5=g.es_h5), DS_ESIK, tohum_ek=tohum_ek))
    Tb = pd.DataFrame({"h5": A.h5.to_numpy(float), "es_h5": esH["es_h5"]}, index=A.index)[m0]
    c.update(YH.yh_d3_guc(Tb, c["n"], tohum_ek=tohum_ek, E=DS_ESIK))
    c["p"] = ds_perm_p(g, _ds_p_yon(kod), DS_ESIK["perm"]["R"], DS_ESIK["perm"]["tohum"] + tohum_ek) if c["n"] else np.nan
    c["atrp"] = {}
    for t in range(3):
        gt = g[(g.kova // 3) == t]
        c["atrp"][f"T{t}"] = {"n": int(len(gt)), "fark": float(gt.h5.mean() - gt.es_h5.mean()) if len(gt) else np.nan}
    if len(g):
        gt = A.loc[g.index]
        c["getiri_ort"] = float(np.nanmean(gt.getiri.to_numpy(float))); c["getiri_med"] = float(np.nanmedian(gt.getiri.to_numpy(float)))
        c["h10"] = float(np.nanmean(gt.h10.to_numpy(float))); c["es_h10"] = float(np.nanmean(es["es_h10"][A.index.get_indexer(g.index)]))
    return c


def ds_celiskili(c: Dict[str, Dict[str, Dict[str, Any]]]) -> bool:
    def poz(h):
        return np.isfinite(h.get("boot_alt", np.nan)) and h["boot_alt"] > 0

    def neg(h):
        return np.isfinite(h.get("boot_ust", np.nan)) and h["boot_ust"] < 0
    for p in DS_KARAR:
        a, b = c[p]["egitim"], c[p]["sinama"]
        if (poz(a) and neg(b)) or (neg(a) and poz(b)):
            return True
    a, b = c["ABD"]["sinama"], c["AVR"]["sinama"]
    return bool((poz(a) and neg(b)) or (neg(a) and poz(b)))


def ds_karne(A: pd.DataFrame, Cd: Dict[str, np.ndarray], Fall: pd.DataFrame, kodlar: List[str], pazarlar: List[str], tohum0: int = 0) -> List[Dict[str, Any]]:
    me = int(DS_ESIK["olcu"]["es_min"]); esH = ds_es_topla(A, Cd, Fall, "_hepsi", me); out = []
    for ki, kod in enumerate(kodlar):
        es = ds_es_topla(A, Cd, Fall, kod, me)
        c = {p: {h: ds_hucre(A, es, esH, kod, p, h, tohum0 + (ki * 10 + pi) * 2 + hi) for hi, h in enumerate(DS_HUCRE)}
             for pi, p in enumerate(pazarlar)}
        out.append({"kod": kod, "hucre": c})
    return out


def ds_etiketle(K: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Karne v3 (yh_d3_etiket) + ÇELİŞKİLİ + BH (m = 25)."""
    nmin = int(DS_ESIK["n_min"]); ps = []
    for x in K:
        c = x["hucre"]
        guc_ok = all(np.isfinite(c[p][h].get("guc", np.nan)) and c[p][h]["guc"] >= DS_ESIK["guc"]["esik"] for p in DS_KARAR for h in DS_HUCRE)
        atrp_ok = all(np.isfinite(c[p][h]["atrp"][t]["fark"]) and c[p][h]["atrp"][t]["fark"] > 0 for p in DS_KARAR for h in DS_HUCRE for t in c[p][h]["atrp"])
        x["guc_ok"], x["atrp_ok"] = guc_ok, atrp_ok
        x["etiket_kural"] = YH.yh_d3_etiket({p: c[p] for p in DS_KARAR}, DS_KARAR, True, atrp_ok, nmin, guc_ok)
        x["celiskili"] = ds_celiskili(c)
        pa, pv = c["ABD"]["sinama"], c["AVR"]["sinama"]
        x["p_ds"] = float(max(pa["p"] if pa["n"] >= nmin and np.isfinite(pa["p"]) else 1.0, pv["p"] if pv["n"] >= nmin and np.isfinite(pv["p"]) else 1.0))
        ps.append(x["p_ds"])
    if len(ps) != DS_ESIK["bh"]["m"]:
        raise DSHata(f"BH m = {DS_ESIK['bh']['m']} olmalı, {len(ps)} p var")
    bh = YH._yh_bh(ps, DS_ESIK["bh"]["q"])
    srt = np.argsort(ps, kind="stable"); m = len(ps)
    qv = np.empty(m); prev = 1.0
    for r in range(m - 1, -1, -1):
        i = srt[r]; prev = min(prev, ps[i] * m / (r + 1)); qv[i] = prev
    say: Dict[str, int] = {}
    for x, b, q in zip(K, bh, qv):
        x["bh"] = bool(b); x["q_bh"] = float(q); e = x["etiket_kural"]
        if e == "ÖLÇÜLEMEDİ":
            x["etiket"] = "ÖLÇÜLEMEDİ"
        elif x["celiskili"]:
            x["etiket"] = "ÇELİŞKİLİ"
        elif e in ("KATKI+", "KATKI−"):
            x["etiket"] = e if b else "SORGULA (BH)"
        else:
            x["etiket"] = "SORGULA"
        say[x["etiket"]] = say.get(x["etiket"], 0) + 1
    return {"sayim": say}


def ds_kume_kendisi(A: pd.DataFrame, Cd: Dict[str, np.ndarray], Fall: pd.DataFrame) -> List[Dict[str, Any]]:
    """BİLGİ: DS ANA olayı vs DS dışı eş (aynı gün aynı kova) ve vs OC eşi (aynı gün aynı OC kovası)."""
    out = []
    for p in DS_PAZAR:
        for hi, h in enumerate(DS_HUCRE):
            m = ((A.pazar == p) & (A.donem == h)).to_numpy()
            for ad, col, cst in (("DS dışı eş (ATRP x likidite)", "dsd_h5", "dsd_st5"), ("OC eşi (momentum x likidite)", "oc_h5", "oc_st5")):
                X = pd.DataFrame({"h5": A.h5, "es_h5": A[col], "st5": A.st5, "es_st5": A[cst], "giris": A.giris})[m]
                c = YH.yh_d1_hucre(X); g = X[X.h5.notna() & X.es_h5.notna()]
                c.update(YH.yh_d3_boot_l3o(g, g.assign(h5=g.es_h5), DS_ESIK, tohum_ek=900 + hi))
                out.append({"pazar": p, "hucre": h, "es": ad, **c})
    return out


def ds_olasilik(A: pd.DataFrame, P_: Dict[str, Dict[str, Any]], Fall: pd.DataFrame) -> Dict[str, Any]:
    """BİLGİ: OC olasılık (250 gün +%100 / -%50 dokunma, OC eşi KAT) ve r60 eşli fark; DS kümesi + özellik tutan / tutmayan (DS içi, havuzlu)."""
    parca = []
    for p in DS_PAZAR:
        Xp = A[A.pazar == p]
        if not len(Xp):
            continue
        Xo = OC.oc_olasilik_olay(P_[p], Xp[["sembol", "tarih", "giris", "d", "j"]].copy())
        Xr = OC.oc_esli(P_[p], Xp[["sembol", "tarih", "giris", "d", "j"]].copy())
        Xo["r60"] = Xr.r60.to_numpy(); Xo["esli_r60"] = Xr.esli_r60.to_numpy(); Xo.index = Xp.index
        parca.append(Xo)
    O = pd.concat(parca).reindex(A.index)
    don = OC._oc_donem(A.giris, OC.OC_ESIK)
    kume = []
    for p in DS_PAZAR:
        for dn in ("2016-22", "2023", "2024-26"):
            m = (A.pazar.to_numpy() == p) & (don == dn)
            if not m.any():
                continue
            ay = pd.to_datetime(A.giris[m]).dt.to_period("M").astype(str).to_numpy()
            r = {"pazar": p, "donem": dn}
            for k in ("up100", "dn50"):
                kk = OC.oc_kat(O[k].to_numpy(float)[m], O["es_" + k].to_numpy(float)[m], ay)
                r[k] = {"n": kk["n"], "p_olay": kk["p_olay"], "p_es": kk["p_ref"], "kat": kk["kat"], "alt": kk["alt"], "ust": kk["ust"]}
            fr = (O.r60 - O.esli_r60).to_numpy(float)[m]; fr = fr[np.isfinite(fr)]
            r["r60_esli_fark"] = {"n": int(len(fr)), "ort": float(fr.mean()) if len(fr) else np.nan, "med": float(np.median(fr)) if len(fr) else np.nan}
            kume.append(r)
    oz = []
    for kod in DS_HIP_SIRA:
        F = A[f"F_{kod}"].to_numpy(float)
        for p in DS_PAZAR:
            m = (A.pazar.to_numpy() == p) & (A.donem.to_numpy() == "sinama")
            r = {"kod": kod, "pazar": p}
            for ad, mm in (("tutan", m & (F == 1)), ("tutmayan", m & (F == 0))):
                u = O.up100.to_numpy(float)[mm]; dn_ = O.dn50.to_numpy(float)[mm]; fr = (O.r60 - O.esli_r60).to_numpy(float)[mm]
                r[ad] = {"n250": int(np.isfinite(u).sum()), "up100": float(np.nanmean(u)) if np.isfinite(u).any() else np.nan,
                         "dn50": float(np.nanmean(dn_)) if np.isfinite(dn_).any() else np.nan,
                         "r60_fark": float(np.nanmean(fr)) if np.isfinite(fr).any() else np.nan}
            oz.append(r)
    return {"kume": kume, "ozellik": oz, "satir": O[["up100", "dn50", "es_up100", "es_dn50", "r60", "esli_r60"]]}


# ================================================================ 7) ÖN KAYIT: eşikler, prefix, huni, sha
def ds_hazirla(pazar: str, islem: int = 1, esik_json: Optional[Dict[str, Any]] = None, veri: Optional[str] = None) -> Dict[str, Any]:
    """Veri -> bağlam -> panel -> özellik (esik_json yoksa A + B geçişi ile eşik hesaplanır) -> olay tablosu (ikili, kova, dönem)."""
    t0 = time.time()
    Vd = ds_veri(pazar, veri); bag = ds_baglam(Vd); P = OC.oc_panel(Vd)
    if esik_json is None:
        ZA = ds_ozellik_pazar(Vd, bag, None, islem)
        XA, say = ds_olay_kur(ZA, P); XA["donem"], amb = ds_donem(XA, P)
        eA = ds_esik_hesap(XA, "A")
        ZB = ds_ozellik_pazar(Vd, bag, eA, islem)
        X, say = ds_olay_kur(ZB, P); X["donem"], amb2 = ds_donem(X, P)
        if amb2 != amb or len(X) != len(XA):
            raise DSHata(f"{pazar}: A / B geçişi olay kümesi farklı ({len(XA)} / {len(X)}, {amb} / {amb2})")
        e = {**eA, **ds_esik_hesap(X, "B"), "ambargo": amb}
        Z = ZB
    else:
        e = esik_json[pazar]
        Z = ds_ozellik_pazar(Vd, bag, e, islem)
        X, say = ds_olay_kur(Z, P); X["donem"], _ = ds_donem(X, P, e["ambargo"])
    X["pazar"] = pazar
    X = pd.concat([X, ds_ikili(X, e)], axis=1)
    X["kova"] = ds_kova(X, e)
    say["temiz_acilis"] = int(Vd["temiz_n"]); say["hisse"] = len(Vd["V"]); say["sure_sn"] = round(time.time() - t0, 1)
    Z["esik"] = e
    dslog.info("%s: %d DS günü, %d havuz günü, %d ANA (%.0f sn)", pazar, say["ds_gun"], say["havuz_gun"], say["ana"], time.time() - t0)
    return {"pazar": pazar, "Vd": Vd, "bag": bag, "P": P, "Z": Z, "X": X, "esik": e, "say": say}


def ds_huni(H: Dict[str, Any]) -> Dict[str, Any]:
    """Getirisiz huni: DS günleri, ANA olay pazar x dönem, hipotez başına tutan ANA olay ve en az 3 özelliği tutmayan DS içi adayı olan tutan olay
    (15 bar ölçülebilirlik bakılmadan)."""
    X = H["X"]; A = X[X.ana]; me = int(DS_ESIK["olcu"]["es_min"])
    out: Dict[str, Any] = {"sayim": H["say"], "ana_donem": {k: int(v) for k, v in A.donem.value_counts().items()}}
    key = pd.Series(X.d.to_numpy(np.int64) * 16 + (X.kova.to_numpy(np.int64) + 1), index=X.index)
    oz: Dict[str, Any] = {}
    for kod in DS_HIP_SIRA:
        col = f"F_{kod}"; F = X[col].to_numpy(float)
        off = pd.Series((F == 0).astype(float), index=X.index).groupby(key).sum()
        r: Dict[str, Any] = {}
        for h in DS_HUCRE:
            a = A[A.donem == h]; fa = a[col].to_numpy(float)
            k0 = key.loc[a.index]; offn = off.reindex(k0.to_numpy()).to_numpy(float) - (fa == 0)
            r[h] = {"n": int(len(a)), "tutan": int((fa == 1).sum()), "tutmayan": int((fa == 0).sum()), "nan": int(np.isnan(fa).sum()),
                    "tutan_es3": int(((fa == 1) & (offn >= me) & (a.kova.to_numpy(int) >= 0)).sum())}
        oz[kod] = r
    out["hipotez"] = oz
    return out


def ds_prefix(H: Dict[str, Any], n: Optional[int] = None) -> Dict[str, Any]:
    """K2: rastgele n ANA olayında ham özellikler veri t'de kesilince aynı mı (bağlam serileri de t'de kesilir)."""
    Pf = DS_ESIK["prefix"]; n = n or int(Pf["n"]); X = H["X"]; A = X[X.ana].reset_index(drop=True)
    rng = np.random.default_rng([int(Pf["tohum"]), DS_PAZAR.index(H["pazar"])])
    sec = rng.choice(len(A), size=min(n, len(A)), replace=False) if len(A) else []
    Vd, bag, e = H["Vd"], H["bag"], H["esik"]; sonuc = []; bozuk = 0
    for i in sec:
        r = A.iloc[int(i)]; s = r.sembol; t = pd.Timestamp(r.tarih)
        df = Vd["V"][s]; dk = df.loc[:t]
        bk = {"rm": bag["rm"].loc[:t], "E": bag["E"].loc[:t], "r21ref": {s: bag["r21ref"][s].loc[:t]}}
        Tt, _, _ = ds_ozellik_hisse(dk, H["pazar"], bk, s, e, Vd["temiz"].get(s))
        Tf, _, _ = ds_ozellik_hisse(df, H["pazar"], bag, s, e, Vd["temiz"].get(s))
        a_ = Tt[pd.to_datetime(Tt.tarih) == t]; b_ = Tf[pd.to_datetime(Tf.tarih) == t]
        if len(a_) != 1 or len(b_) != 1:
            bozuk += 1; sonuc.append({"sembol": s, "tarih": str(t.date()), "tut": False, "neden": "satır yok"}); continue
        fark = [k for k in _DS_HAM if not (np.isclose(a_[k].iat[0], b_[k].iat[0], rtol=Pf["rtol"], atol=1e-12, equal_nan=True))]
        bozuk += bool(fark); sonuc.append({"sembol": s, "tarih": str(t.date()), "tut": not fark, "fark": fark})
    return {"pazar": H["pazar"], "n": len(sonuc), "bozuk": bozuk, "olay": sonuc}


def _ds_sha(yol: str) -> str:
    return OC._oc_sha_dosya(yol) if os.path.exists(yol) else "-"


def ds_sha_simdi(cikti: Optional[str] = None, veri: Optional[str] = None) -> Dict[str, str]:
    c = cikti or DS_YOL["cikti"]; v = veri or DS_YOL["veri"]
    out = {"DS_ESIK_SHA": ds_esik_sha(), "DS_KOD_SHA": _ds_sha(DS_YOL["kod"]), "YH_KOD_SHA": _ds_sha(DS_YOL["yh_kod"]),
           "YH_ESIK_SHA": YH.yh_esik_sha(), "OC_KOD_SHA": _ds_sha(DS_YOL["oc_kod"]), "OC_ESIK_SHA": OC.oc_esik_sha(), "S6_KOD_SHA": _ds_sha(DS_YOL["s6_kod"]),
           "DS_ESIK_JSON_SHA": _ds_sha(_ds_yol("esik", c)), "DS_PREFIX_SHA": _ds_sha(_ds_yol("prefix", c)),
           "CERCEVE_SHA": _ds_sha(_ds_yol("cerceve", c)), "ELESTIRI_SHA": _ds_sha(_ds_yol("elestiri", c)), "SEKTOR_SHA": _ds_sha(DS_YOL["sektor"])}
    for p in DS_PAZAR:
        out[f"V_{p}_SHA"] = _ds_sha(os.path.join(v, f"V_{p}.pkl"))
    return out


def _ds_git(yol: str) -> Dict[str, str]:
    try:
        r = subprocess.run(["git", "-C", KOK_DS, "log", "-1", "--format=%H %cI", "--", yol], capture_output=True, text=True, timeout=60)
        h = r.stdout.strip().split(" ", 1)
        return {"commit": h[0], "zaman": h[1]} if len(h) == 2 else {"commit": "-", "zaman": "-"}
    except (OSError, subprocess.SubprocessError):
        return {"commit": "-", "zaman": "-"}


def ds_kontrol_tablosu() -> str:
    try:
        import IZ_KARNE as IK
        ad = {k["kod"]: k.get("ad", k["kod"]) for k in IK.IK_KONTROL}
    except Exception:   # IZ_KARNE yüklenemezse madde adları kodla
        ad = {k: k for k in DS_KONTROL}
    s = ["| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    for k, (y, kn) in DS_KONTROL.items():
        s.append(f"| {k} | {ad.get(k, k)} | {y} | {kn} |")
    return "\n".join(s)


def _ds_sec_ornek(sec: Optional[Dict[str, Any]]) -> List[str]:
    """K10: ham sec_ozet'ten 3 satır (8-K madde alanı, 13G adı) elle gösterim."""
    if sec is None:
        return ["- sec_ozet yok: sınıf II VERİ YOK"]
    out = []; J = sec["J"]
    for cik in list(J)[:400]:
        v = J[cik]
        for f, t, it in zip(v["form"], v["date"], v.get("items", [""] * len(v["form"]))):
            if (f == "8-K" and "2.03" in str(it)) or f in ("SC 13G", "SCHEDULE 13G"):
                out.append(f"- CIK {cik} ({','.join(v.get('tickers', [])[:1])}): form '{f}', tarih {t}, madde '{it}'")
                break
        if len(out) >= 3:
            break
    return out


def ds_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False) -> str:
    c = cikti or DS_YOL["cikti"]; yol = _ds_yol("onkayit", c)
    if os.path.exists(yol) and not uzerine:
        raise DSHata(f"{yol} var (--uzerine-yaz olmadan yazılmaz)")
    H = {p: ds_hazirla(p, islem, None, veri) for p in DS_PAZAR}
    esik = {p: H[p]["esik"] for p in DS_PAZAR}
    pre = {p: ds_prefix(H[p]) for p in DS_PAZAR}
    if any(pre[p]["bozuk"] for p in DS_PAZAR):
        raise DSHata("prefix TUTMADI: " + json.dumps({p: [o for o in pre[p]["olay"] if not o["tut"]][:3] for p in DS_PAZAR}, ensure_ascii=False))
    huni = {p: ds_huni(H[p]) for p in DS_PAZAR}
    _ds_yaz(_ds_yol("esik", c), json.dumps(esik, ensure_ascii=False, indent=1, sort_keys=True, default=_ds_json), "DS eşik")
    _ds_yaz(_ds_yol("prefix", c), json.dumps(pre, ensure_ascii=False, indent=1, default=_ds_json), "DS prefix")
    sec = ds_sec_yukle()
    sha = ds_sha_simdi(c, veri); gi = _ds_git(os.path.join(c, DS_DOSYA["elestiri"])); gc = _ds_git(os.path.join(c, DS_DOSYA["cerceve"]))
    s = [f"# DÜŞÜŞ SONRASI — ÖN KAYIT (DS; 25 sınıf I hipotez, 15 bar cetveli; {_ds_simdi()[:10]})", "",
         f"{DS_SURUM}. Kodlayıcı alt ajan (KOL F). Bu dosya koşudan ÖNCE yazıldı ve git'e işlendi ('DS ön kayıt'); ds_kos kapısı aşağıdaki "
         "sha'ları, ds_esik.json eşitliğini, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Sınama verisinin "
         "SONUCU (h5 / st5 / getiri) bu dosya yazılırken hesaplanmadı: yalnız özellik değerleri, olay sayıları ve eğitim eşikleri (getirisiz).", ""]
    for k, v in sha.items():
        s.append(f"- {k}: `{v}`")
    s += [f"- GİRDİ MÜHRÜ: DS_ELESTIRI.md commit `{gi['commit']}` ({gi['zaman']}); DS_OLCUM_CERCEVE.md commit `{gc['commit']}` ({gc['zaman']})",
          f"- ZAMAN (UTC): `{_ds_simdi()}`", "",
          "## 1. SORU, OLAY, CETVEL, EŞ, HÜCRE (DS_ESIK; çerçeve DS_OLCUM_CERCEVE.md AYNEN)", "",
          f"- OLAY: {DS_ESIK['olay']['tanim']}.", f"- AÇILIŞ TEMİZLİĞİ: {DS_ESIK['acilis_temizlik']}.",
          f"- CETVEL: {DS_ESIK['olcu']['cetvel']}; hat = {DS_ESIK['olcu']['hat']}.", f"- EŞ: {DS_ESIK['olcu']['es']}.",
          f"- KOVA: {DS_ESIK['kova']['tanim']}.", f"- BİLGİ EŞLERİ: DS dışı eş = {DS_ESIK['olcu']['ds_disi_es']}; {DS_ESIK['olcu']['oc_es']}.",
          f"- DÖNEM: eğitim {DS_ESIK['donem']['egitim']}, sınama {DS_ESIK['donem']['sinama']}; {DS_ESIK['donem']['tanim']}. Ambargo (sınama ilk "
          f"izinli giriş): " + ", ".join(f"{p} {esik[p]['ambargo']}" for p in DS_PAZAR) + ".",
          f"- GÜÇ: {DS_ESIK['guc']['tanim']}.", f"- p: {DS_ESIK['perm']['tanim']}.", f"- BH: {DS_ESIK['bh']['tanim']}; p_DS = {DS_ESIK['bh']['p_ds']}.",
          f"- ETİKET: {DS_ESIK['etiket']}.", f"- YENİDEN ÜRETİM (önceden seçildi): {DS_ESIK['yeniden_uretim']} + {DS_ESIK['elle_sim_n']} rastgele olayın "
          "h5'i bağımsız döngüyle.", "- KARAR PAZARLARI ABD ve AVR; BIST BİLGİ. Sınıf II (ABD-olay) BİLGİ, BH dışı.", "",
          "## 2. HİPOTEZ TABLOSU (BH listesi, m = 25, DS_ELESTIRI bölüm 5 sırası; ANA kol)", "",
          "| sıra | DS | hipotez | tanım (t'de bilinir) | yön | p yönü | SABİT eşik | kaynak |", "|---|---|---|---|---|---|---|---|"]
    for k in DS_HIP_SIRA:
        h = DS_HIP[k]
        s.append(f"| {h['sira']} | {k} | {h['ad']} | {h['tanim']} | {h['yon']} | {'iki yönlü' if _ds_p_yon(k) == '?' else 'tek yönlü ' + _ds_p_yon(k)} | "
                 f"{h['esik']} | {h['kaynak']} |")
    s += ["", "## 3. EĞİTİM EŞİKLERİ (2016-22 DS ANA olaylarından, getirisiz; SAYI; ds_esik.json)", "",
          "| eşik | " + " | ".join(DS_PAZAR) + " |", "|---|" + "---|" * len(DS_PAZAR)]
    for k in [k for k in esik["ABD"] if k != "ambargo"]:
        s.append(f"| {k} | " + " | ".join(f"{esik[p][k]:.6g}" if isinstance(esik[p][k], float) else str(esik[p][k]) for p in DS_PAZAR) + " |")
    s += ["", "## 4. HUNİ (getirisiz)", ""]
    for p in DS_PAZAR:
        sy = huni[p]["sayim"]
        s.append(f"- **{p}**: hisse {sy['hisse']}; DS günü {sy['ds_gun']}; havuzdan geçen DS günü {sy['havuz_gun']} (düşen: likidite alt %20 "
                 f"{sy.get('likidite_alt20', 0)}, geçmiş bölünme {sy.get('bolunme_gecmis', 0)}, havuz dışı {sy.get('havuz_disi', 0)}, giriş yok / geç "
                 f"{sy.get('giris_yok', 0)} / {sy.get('giris_gec', 0)}); ANA olay {sy['ana']}; dönem " +
                 ", ".join(f"{k} {v}" for k, v in sorted(huni[p]['ana_donem'].items())) + f"; açılış kırpılan bar {sy['temiz_acilis']}.")
    s += ["", "Hipotez başına ANA olay (tutan / tutmayan / NaN; 'tutan_es3' = en az 3 özelliği tutmayan DS içi adayı olan tutan olay; 15 bar "
          "ölçülebilirliği bakılmadan):", "", "| DS | " + " | ".join(f"{p} {h}" for p in DS_PAZAR for h in DS_HUCRE) + " |",
          "|---|" + "---|" * (len(DS_PAZAR) * 2)]
    for k in DS_HIP_SIRA:
        s.append(f"| {k} | " + " | ".join(f"{huni[p]['hipotez'][k][h]['tutan']} / {huni[p]['hipotez'][k][h]['tutmayan']} / {huni[p]['hipotez'][k][h]['nan']}"
                                         f" (es3 {huni[p]['hipotez'][k][h]['tutan_es3']})" for p in DS_PAZAR for h in DS_HUCRE) + " |")
    s += ["", "## 5. SINIF II (ABD-olay, sec_ozet; BİLGİ tablosu, BH dışı)", ""]
    for k, h in DS_SINIF2.items():
        s.append(f"- {k} ({h['yon']}): {h['ad']}; {h['tanim']}" + (f" NOT: {h['not']}" if h.get("not") else ""))
    for k, v in DS_SINIF2_YOK.items():
        s.append(f"- {k}: {v}")
    s += ["", "K10 sec_ozet ham satır gösterimi (elle):"] + _ds_sec_ornek(sec)
    s += ["", "## 6. PREFIX (K2; ds_prefix.json)", ""]
    for p in DS_PAZAR:
        s.append(f"- {p}: {pre[p]['n']} olay, bozuk {pre[p]['bozuk']} ({len(_DS_HAM)} ham özellik, rtol {DS_ESIK['prefix']['rtol']}).")
    s += ["", "## 7. ÖNCEDEN YAZILI NOTLAR", "",
          "- DS01 / DS09 / DS10 / DS11 (son günlerin zayıflığı) ve DS05 / DS16 (aynı doruk barı) yüksek ilişkili beklenir: birden fazlası geçerse tek bulgu.",
          "- DS08 / DS20 / DS28: özellik DS olayında sık; tutmayan eş azlığı ÖLÇÜLEMEDİ üretebilir (huni yukarıda).",
          "- DS03 sektör sınıfı bugünkü (sektor_ABD.csv; K2 notu); AVR / BIST evren artığı.",
          "- Etiket KATKI+ olsa bile 'iz' denmez; ileri test (Mart 2027, kriz sonrası veri) gerekir.", "",
          "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", ds_kontrol_tablosu(), ""]
    metin = "\n".join(s)
    _ds_yaz(yol, metin, "DS ön kayıt")
    return yol


# ================================================================ 8) KOŞU
_DS_DESEN = {k: rf"(?<![A-Z0-9_]){k}:\s*`([0-9a-f]{{64}}|-)`" for k in ("DS_ESIK_SHA", "DS_KOD_SHA", "YH_KOD_SHA", "YH_ESIK_SHA", "OC_KOD_SHA", "OC_ESIK_SHA",
                                                       "S6_KOD_SHA", "DS_ESIK_JSON_SHA", "DS_PREFIX_SHA", "CERCEVE_SHA", "ELESTIRI_SHA", "SEKTOR_SHA",
                                                       "V_ABD_SHA", "V_AVR_SHA", "V_BIST_SHA")}


def ds_kapi(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    c = cikti or DS_YOL["cikti"]; yol = _ds_yol("onkayit", c)
    if not os.path.exists(yol):
        raise DSHata(f"ön kayıt yok: {yol}")
    if kontrol:
        import IZ_KARNE as IK
        IK.ik_kontrol_kapisi(yol)
    metin = open(yol, encoding="utf-8").read(); simdi = ds_sha_simdi(c, veri); tut = {}
    for k, d in _DS_DESEN.items():
        m = re.search(d, metin)
        if not m:
            raise DSHata(f"ön kayıtta {k} yok")
        if m.group(1) != simdi[k]:
            raise DSHata(f"{k} tutmuyor: ön kayıt {m.group(1)[:12]} / şimdi {simdi[k][:12]} -> DURDU")
        tut[k] = simdi[k]
    g = {}
    if git:
        for ad in ("onkayit", "esik", "prefix"):
            g[ad] = OC._oc_git_islenmis(_ds_yol(ad, c))
        g["kod"] = OC._oc_git_islenmis(DS_YOL["kod"])
    return {"sha": tut, "git": g, "zaman": _ds_simdi()}


def ds_elle_sim(A: pd.DataFrame, Vd_: Dict[str, Dict[str, Any]], n: int, tohum: int) -> Dict[str, Any]:
    """K11 bağımsız: olayın h5 / st5'i hissenin kendi geçerli barlarıyla düz döngü (yh_sim kullanılmaz). 15 bar, kapanış stop / hedef sırası."""
    Y = YH.YH_ESIK["olcu"]; St = Y["stop"]; g = A[A.olc.astype(bool)]
    rng = np.random.default_rng(int(tohum)); sec = g.iloc[rng.choice(len(g), size=min(n, len(g)), replace=False)] if len(g) else g
    bozuk = []
    for r in sec.itertuples():
        df = Vd_[r.pazar]["V"][r.sembol]; ix = df.index; k0 = ix.get_loc(pd.Timestamp(r.giris))
        O, C = df.Open.to_numpy(float), df.Close.to_numpy(float); E0 = O[k0]; stop = r.hat * Y["stop0"]["hat_carpan"]; tepe = -np.inf
        h5 = 0.0; st5 = 0.0; g5 = g10 = False
        for k in range(int(Y["ufuk"])):
            cc = C[k0 + k]
            if cc < stop:
                st5 = 0.0 if g5 else 1.0; break
            if not g5 and cc >= E0 * (1 + Y["hedef"][0]):
                g5 = True; h5 = 1.0
            if not g10 and cc >= E0 * (1 + Y["hedef"][1]):
                g10 = True
            if g5:
                stop = max(stop, E0 * (1 + St["kilit5"]))
            if g10:
                stop = max(stop, E0 * (1 + St["kilit10"]))
            tepe = max(tepe, cc); stop = max(stop, tepe * (1 - St["takip"]))
        if abs(h5 - float(r.h5)) > 1e-12 or abs(st5 - float(r.st5)) > 1e-12:
            bozuk.append({"pazar": r.pazar, "sembol": r.sembol, "giris": str(pd.Timestamp(r.giris).date()), "h5": [float(r.h5), h5], "st5": [float(r.st5), st5]})
    return {"n": int(len(sec)), "bozuk": bozuk}


def ds_yeniden(yol_olay: str, kod: str, pazar: str, hucre: str) -> Dict[str, Any]:
    """K11 bağımsız: ds_olay.csv.gz düz pandas sorgusu (ds_hucre / yh_d1_hucre kullanılmaz)."""
    O = pd.read_csv(yol_olay, dtype={"sembol": str}, low_memory=False)
    q = O[(O.pazar == pazar) & (O.donem == hucre) & (O[f"F_{kod}"] == 1)].dropna(subset=["h5", f"es_h5_{kod}"])
    return {"n": int(len(q)), "fark": float(q.h5.mean() - q[f"es_h5_{kod}"].mean()) if len(q) else float("nan")}


def ds_kos(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    c = cikti or DS_YOL["cikti"]; ys = _ds_yol("sonuc", c)
    if os.path.exists(ys):
        raise DSHata("ds_sonuc.json var: DS zaten ölçüldü (ikinci koşu yok; düzeltme ayrı commit + DÜZELTME notu)")
    t0 = time.time(); kp = ds_kapi(c, veri, git, kontrol)
    esik = json.load(open(_ds_yol("esik", c), encoding="utf-8"))
    H = {p: ds_hazirla(p, islem, esik, veri) for p in DS_PAZAR}
    # eşik eşitliği (D3 gibi): aynı kodla yeniden hesap = mühürlü json
    for p in DS_PAZAR:
        X = H[p]["X"]; yeni = {**ds_esik_hesap(X, "A"), **ds_esik_hesap(X, "B"), "ambargo": esik[p]["ambargo"]}
        if json.dumps(yeni, sort_keys=True, default=_ds_json) != json.dumps(esik[p], sort_keys=True, default=_ds_json):
            raise DSHata(f"{p}: eşikler yeniden hesapla ds_esik.json aynı değil -> DURDU")
    sec = ds_sec_yukle()
    A_l, F_l, C_l = [], {}, {}
    off = 0
    for p in DS_PAZAR:
        X = H[p]["X"]
        if p == "ABD":
            X = pd.concat([X, ds_sinif2(X, H[p]["Vd"], H[p]["bag"], sec)], axis=1)
        else:
            X = X.assign(**{f"F_{k}": np.nan for k in DS_SINIF2})
        X.index = np.arange(off, off + len(X)); H[p]["X"] = X
        A, Cd = ds_olc(X, H[p]["P"], H[p]["Vd"], H[p]["Z"], islem)
        Cd["cr"] = Cd["cr"] + off; Cd["ce"] = Cd["ce"] + off
        A_l.append(A); C_l[p] = Cd; off += len(X)
        dslog.info("%s ölçüldü: %d ANA (%.0f sn)", p, len(A), time.time() - t0)
    A = pd.concat(A_l)
    Fall = pd.concat([H[p]["X"][[f"F_{k}" for k in DS_HIP_SIRA + list(DS_SINIF2)]] for p in DS_PAZAR])
    Cd = {k: np.concatenate([C_l[p][k] for p in DS_PAZAR]) for k in C_l["ABD"]}
    K = ds_karne(A, Cd, Fall, DS_HIP_SIRA, DS_PAZAR)
    et = ds_etiketle(K)
    K2 = ds_karne(A, Cd, Fall, list(DS_SINIF2), ["ABD"], tohum0=5000)
    kume = ds_kume_kendisi(A, Cd, Fall)
    ola = ds_olasilik(A, {p: H[p]["P"] for p in DS_PAZAR}, Fall)
    # satır dosyası
    me = int(DS_ESIK["olcu"]["es_min"]); Sat = A[["pazar", "sembol", "tarih", "giris", "donem", "kova", "hucre", "atrp", "hat", "dd", "olc", "h5", "h10", "st5",
                                                  "h5H", "getiri", "cikis_bar", "cikis_tur", "n_aday", "dsd_h5", "dsd_st5", "dsd_n", "oc_h5", "oc_st5", "oc_n"]].copy()
    esH = ds_es_topla(A, Cd, Fall, "_hepsi", me); ek: Dict[str, np.ndarray] = {"es_h5_hepsi": esH["es_h5"]}
    for kod in DS_HIP_SIRA + list(DS_SINIF2):
        es = ds_es_topla(A, Cd, Fall, kod, me)
        ek[f"F_{kod}"] = A[f"F_{kod}"].to_numpy(float); ek[f"es_h5_{kod}"] = es["es_h5"]; ek[f"es_st5_{kod}"] = es["es_st5"]; ek[f"n_es_{kod}"] = es["n_es"]
    for k in ("up100", "dn50", "es_up100", "es_dn50", "r60", "esli_r60"):
        ek[k] = ola["satir"][k].to_numpy(float)
    Sat = pd.concat([Sat, pd.DataFrame(ek, index=Sat.index)], axis=1)
    Sat["tarih"] = pd.to_datetime(Sat.tarih).dt.strftime("%Y-%m-%d"); Sat["giris"] = pd.to_datetime(Sat.giris).dt.strftime("%Y-%m-%d")
    yo = _ds_yol("olay", c)
    Sat.round(6).to_csv(yo, index=False, compression="gzip")
    # yeniden üretim
    yu = []
    for kod, p, h in DS_ESIK["yeniden_uretim"]:
        r = [x for x in K if x["kod"] == kod][0]["hucre"][p][h]; b = ds_yeniden(yo, kod, p, h)
        tut = b["n"] == r["n"] and (abs(b["fark"] - r["fark"]) <= 1e-6 or (np.isnan(b["fark"]) and np.isnan(r["fark"])))
        if not tut:
            raise DSHata(f"yeniden üretim TUTMADI {kod} {p} {h}: {r['n']} / {r['fark']} vs {b['n']} / {b['fark']}")
        yu.append({"kod": kod, "pazar": p, "hucre": h, "kod_n": r["n"], "kod_fark": r["fark"], "yeni_n": b["n"], "yeni_fark": b["fark"], "durum": "TUTTU"})
    es_ = ds_elle_sim(A, {p: H[p]["Vd"] for p in DS_PAZAR}, int(DS_ESIK["elle_sim_n"]), int(DS_ESIK["elle_sim_tohum"]))
    if es_["bozuk"]:
        raise DSHata(f"elle simülasyon TUTMADI: {es_['bozuk'][:3]}")
    # n < 30 olay listesi (sınıf I karar hücreleri)
    kucuk = []
    for x in K:
        for p in DS_KARAR:
            for h in DS_HUCRE:
                if 0 < x["hucre"][p][h]["n"] < DS_ESIK["n_min"]:
                    es = ds_es_topla(A, Cd, Fall, x["kod"], me)
                    m = ((A.pazar == p) & (A.donem == h) & (A[f"F_{x['kod']}"] == 1)).to_numpy() & np.isfinite(es["es_h5"]) & np.isfinite(A.h5.to_numpy(float))
                    g = A[m]
                    kucuk.append({"kod": x["kod"], "pazar": p, "hucre": h, "olay": [{"sembol": r.sembol, "tarih": str(pd.Timestamp(r.tarih).date()),
                                                                                     "h5": float(r.h5), "st5": float(r.st5)} for r in g.itertuples()]})
    huni_olc = {p: {h: {"ana": int(((A.pazar == p) & (A.donem == h)).sum()), "olc": int(((A.pazar == p) & (A.donem == h) & A.olc.astype(bool)).sum()),
                        "giris_stop_otesi": int(((A.pazar == p) & (A.donem == h) & (A.cikis_tur == "giris_stop_otesi")).sum()),
                        "h5_ort": float(A.loc[(A.pazar == p) & (A.donem == h), "h5"].mean())} for h in DS_HUCRE} for p in DS_PAZAR}
    J = {"surum": DS_SURUM, "zaman_utc": _ds_simdi(), "sure_sn": round(time.time() - t0, 1), "kapi": kp, "esik_sha": ds_esik_sha(),
         "sayim": {p: H[p]["say"] for p in DS_PAZAR}, "huni_olc": huni_olc, "karne": K, "etiket_sayim": et["sayim"], "sinif2": K2,
         "sinif2_yok": DS_SINIF2_YOK, "kume": kume, "olasilik": {"kume": ola["kume"], "ozellik": ola["ozellik"]}, "yeniden_uretim": yu,
         "elle_sim": es_, "kucuk": kucuk, "sec_ozet_sha": sec["sha"] if sec else None, "olay_sha": OC._oc_sha_dosya(yo)}
    _ds_yaz(ys, json.dumps(J, ensure_ascii=False, indent=1, default=_ds_json), "DS sonuç")
    return {"json": J, "rapor": ds_rapor(c)}


# ================================================================ 9) RAPOR
def _p(x: Any, n: int = 1) -> str:
    return YH._yz(x, n)


def _s(x: Any, n: int = 2) -> str:
    return YH._sy(x, n)


def _fp(x: Any) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{100 * float(x):+.1f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def ds_rapor(cikti: Optional[str] = None) -> str:
    c = cikti or DS_YOL["cikti"]; J = json.load(open(_ds_yol("sonuc", c), encoding="utf-8"))
    K = J["karne"]; s = [f"# DÜŞÜŞ SONRASI — RAPOR (DS koşusu; {J['zaman_utc']})", "",
                         f"{J['surum']}. Ön kayıt DS_ON_KAYIT.md (commit `{J['kapi']['git'].get('onkayit', {}).get('commit', '-')}`, "
                         f"{J['kapi']['git'].get('onkayit', {}).get('commit_zamani', '-')}); kapı {J['kapi']['zaman']}; süre {J['sure_sn']} sn. "
                         "FARK = hedef payı farkı (yüzde puan; h5 = 15 barda +%5 stop'tan önce), getiri değil. Komisyon yok. Evren bugün işlem gören "
                         "hisseler (hayatta kalma: (+) yönlü özellikler lehine).", "", "## 0. ÖZET", ""]
    s.append("- Etiket dağılımı (25 hipotez): " + ", ".join(f"{k} {v}" for k, v in sorted(J["etiket_sayim"].items())) + ".")
    gec = [x for x in K if x["bh"]]
    s.append(f"- BH (q 0,10, m 25) geçen: {', '.join(x['kod'] for x in gec) if gec else 'yok'}.")
    yak = sorted(K, key=lambda x: x["p_ds"])[:5]
    s.append("- En küçük p_DS 5 hipotez: " + "; ".join(f"{x['kod']} p {_s(x['p_ds'], 4)} q {_s(x['q_bh'], 3)} ({x['etiket']})" for x in yak) + ".")
    s += ["", "## 1. HUNİ (ölçüm)", ""]
    for p, v in J["huni_olc"].items():
        sy = J["sayim"][p]
        s.append(f"- {p}: DS günü {sy['ds_gun']}, havuz {sy['havuz_gun']}, ANA {sy['ana']}; " +
                 "; ".join(f"{h}: ANA {v[h]['ana']}, ölçülen {v[h]['olc']}, açılış stop altı {v[h]['giris_stop_otesi']}, h5 ort {_p(v[h]['h5_ort'])}" for h in DS_HUCRE))
    s += ["", "## 2. SONUÇ TABLOSU (sınıf I; karar ABD + AVR, BIST bilgi)", "",
          "Hücre: n / FARK / stop olay-eş (puan). boot = sınama ay kümeli %95 [alt, üst]; güç = sınama; p = pazar sınama p'si (önceden yazılı yön).", "",
          "| DS | pazar | eğitim n / FARK / st olay-eş | sınama n / FARK / st olay-eş | sınama boot | güç e / s | p | p_DS / q | etiket |",
          "|---|---|---|---|---|---|---|---|---|"]
    for x in K:
        for p in DS_PAZAR:
            a, b = x["hucre"][p]["egitim"], x["hucre"][p]["sinama"]
            et = (f"**{x['etiket']}**" if p == "ABD" else "") if p in DS_KARAR else "BİLGİ"
            pq = f"{_s(x['p_ds'], 4)} / {_s(x['q_bh'], 3)}" if p == "ABD" else ""
            s.append(f"| {x['kod']} | {p} | {a['n']} / {_fp(a['fark'])} / {_p(a['st'], 0)}-{_p(a['es_st'], 0)} | {b['n']} / {_fp(b['fark'])} / "
                     f"{_p(b['st'], 0)}-{_p(b['es_st'], 0)} | [{_fp(b.get('boot_alt'))}, {_fp(b.get('boot_ust'))}] | {_s(a.get('guc'))} / {_s(b.get('guc'))} | "
                     f"{_s(b.get('p'), 4)} | {pq} | {et} |")
    s += ["", "Etiket kuralı: " + DS_ESIK["etiket"], "",
          "ATRP tercil FARK'ı (sınama; T0 / T1 / T2, puan) ve L3O (sınama):", "", "| DS | ABD T0 / T1 / T2 | AVR T0 / T1 / T2 | L3O ABD / AVR | ÇELİŞKİLİ | karne v3 |",
          "|---|---|---|---|---|---|"]
    for x in K:
        h = x["hucre"]
        s.append(f"| {x['kod']} | " + " / ".join(_fp(h['ABD']['sinama']['atrp'][t]['fark']) for t in ('T0', 'T1', 'T2')) + " | " +
                 " / ".join(_fp(h['AVR']['sinama']['atrp'][t]['fark']) for t in ('T0', 'T1', 'T2')) +
                 f" | {_fp(h['ABD']['sinama'].get('l3o'))} / {_fp(h['AVR']['sinama'].get('l3o'))} | {'EVET' if x['celiskili'] else '-'} | {x['etiket_kural']} |")
    s += ["", "## 3. DS KÜMESİNİN KENDİSİ (BİLGİ)", "", "| pazar | hücre | eş | n | h5 olay | h5 eş | FARK | boot [alt, üst] | st olay / eş |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in J["kume"]:
        s.append(f"| {r['pazar']} | {r['hucre']} | {r['es']} | {r['n']} | {_p(r['p_olay'])} | {_p(r['p_es'])} | {_fp(r['fark'])} | "
                 f"[{_fp(r.get('boot_alt'))}, {_fp(r.get('boot_ust'))}] | {_p(r['st'])} / {_p(r['es_st'])} |")
    s += ["", "## 4. SINIF II (ABD-olay, sec_ozet; BİLGİ, BH dışı)", "", "| DS | yön | eğitim n / FARK | sınama n / FARK | sınama boot | p (sınama) | not |",
          "|---|---|---|---|---|---|---|"]
    for x in J["sinif2"]:
        a, b = x["hucre"]["ABD"]["egitim"], x["hucre"]["ABD"]["sinama"]; h = DS_SINIF2[x["kod"]]
        s.append(f"| {x['kod']} | {h['yon']} | {a['n']} / {_fp(a['fark'])} | {b['n']} / {_fp(b['fark'])} | [{_fp(b.get('boot_alt'))}, {_fp(b.get('boot_ust'))}] | "
                 f"{_s(b.get('p'), 4)} | {h.get('not', '')} |")
    for k, v in J["sinif2_yok"].items():
        s.append(f"| {k} | - | - | - | - | - | {v} |")
    s += ["", "## 5. OLASILIK TABLOSU (BİLGİ; 250 gün +%100 / -%50 dokunma, OC eşi KAT; 60 gün r60 eşli fark)", "",
          "| pazar | dönem | n250 | P(+%100) olay / eş | KAT +%100 [alt, üst] | P(-%50) olay / eş | KAT -%50 [alt, üst] | r60 eşli fark ort / med |",
          "|---|---|---|---|---|---|---|---|"]
    for r in J["olasilik"]["kume"]:
        u, d = r["up100"], r["dn50"]
        s.append(f"| {r['pazar']} | {r['donem']} | {u['n']} | {_p(u['p_olay'])} / {_p(u['p_es'])} | {_s(u['kat'])} [{_s(u['alt'])}, {_s(u['ust'])}] | "
                 f"{_p(d['p_olay'])} / {_p(d['p_es'])} | {_s(d['kat'])} [{_s(d['alt'])}, {_s(d['ust'])}] | {_fp(r['r60_esli_fark']['ort'])} / "
                 f"{_fp(r['r60_esli_fark']['med'])} |")
    s += ["", "Özellik tutan / tutmayan (DS içi, sınama, havuzlu; aynı gün eşlemesi YOK, bilgi): P(+%100) ve P(-%50) oranları, r60 OC eşli fark ortalaması.", "",
          "| DS | ABD tutan +100 / -50 / r60 | ABD tutmayan | AVR tutan | AVR tutmayan |", "|---|---|---|---|---|"]
    oz = {(r["kod"], r["pazar"]): r for r in J["olasilik"]["ozellik"]}
    for k in DS_HIP_SIRA:
        f_ = lambda r: f"{_p(r['up100'])} / {_p(r['dn50'])} / {_fp(r['r60_fark'])} (n {r['n250']})"  # noqa: E731
        s.append(f"| {k} | {f_(oz[(k, 'ABD')]['tutan'])} | {f_(oz[(k, 'ABD')]['tutmayan'])} | {f_(oz[(k, 'AVR')]['tutan'])} | {f_(oz[(k, 'AVR')]['tutmayan'])} |")
    s += ["", "## 6. YENİDEN ÜRETİM (K11)", ""]
    for r in J["yeniden_uretim"]:
        s.append(f"- {r['kod']} {r['pazar']} {r['hucre']}: kod n {r['kod_n']} / FARK {_s(r['kod_fark'], 6)}; ds_olay.csv.gz düz pandas n {r['yeni_n']} / "
                 f"FARK {_s(r['yeni_fark'], 6)} -> {r['durum']}.")
    s.append(f"- Bağımsız döngüyle h5 / st5 yeniden simülasyonu: {J['elle_sim']['n']} rastgele olay, bozuk {len(J['elle_sim']['bozuk'])}.")
    s += ["", "## 7. n < 30 KARAR HÜCRELERİ (olaylar ds_sonuc.json 'kucuk')", ""]
    s.append("- " + ("; ".join(f"{k['kod']} {k['pazar']} {k['hucre']} n {len(k['olay'])}" for k in J["kucuk"]) or "yok") + ".")
    s += ["", "## HATA", "", "(ana model IK_HATA'ya işler; bu koşuda bulunanlar raporun sonuna alt ajan tarafından eklenir)", "",
          "## KONTROL LİSTESİ", "", ds_kontrol_tablosu(), "", "Kod değişti: Colab'da çalışma zamanını yeniden başlat.", ""]
    metin = "\n".join(s)
    _ds_yaz(_ds_yol("rapor", c), metin, "DS rapor")
    return metin


# ================================================================ ÇAKIŞMA KAPISI
def _cakisma_kontrol_ds(_once=_CK_ONCE_DS, _dosya="DUSUS_SONRASI.py"):
    """Çakışma kapısı: bu dosya bellekteki ds_ / DS_ / _ds öneki DIŞINDAKİ mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_DS", "_CK_KAYIT", "_cakisma_kontrol_ds", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "_dt", "annotations",
           "Any", "Dict", "List", "Optional", "Tuple", "OC", "YH", "S6")
    onek = ("ds_", "DS_", "_ds", "DSHata", "dslog", "_DS")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std and not k.startswith(onek))
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_ds()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=DS_SURUM)
    ap.add_argument("komut", choices=["onkayit", "kos", "rapor", "sha"])
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "onkayit":
            print(ds_onkayit_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = ds_kos(a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(R_["rapor"][:5000])
        elif a.komut == "rapor":
            print(ds_rapor(a.cikti))
        else:
            print(json.dumps(ds_sha_simdi(a.cikti, a.veri), indent=1))
    except (DSHata, OC.OCHata) as ex:
        dslog.error("%s", ex); sys.exit(1)
