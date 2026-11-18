"""YAPI_HEDEF — yapı kurallarının YENİ TEST STANDARDIYLA ilk ölçümü (17 Kasım 2026; iş tanımı arastirma_cikti/yapi_hedef/YAPI_HEDEF_IS_TANIMI.md).

Cemal (17 Kas akşam, 'testler bu şekilde devam etsin'): 60 gün testi yapı kuralları için kapandı. Kod oluşumu görür; giriş = kırılım mumu
(ölçümde t+1 açılış); HEDEF = +%5 (ve +%10) stop'tan ÖNCE, 15 geçerli bar içinde; stop geçici takip kuralı; çıkış = stop ya da yeni ters oluşum.
Bu modül beş yapı denemesini (Y1-Y5) aynı mekanik kuralla ölçer; eşler (aynı gün, aynı ORTAK_CETVEL kovası) ve plasebo (aynı hisse, rastgele gün)
AYNI kuralla ölçülür. Bütün eşikler YH_ESIK tek sözlüğündedir (sha256 ön kayıtta); karar kuralı ve etiket koşudan ÖNCE yazılıdır.

TANIM (ayrıntı YH_ESIK; her sinyal yalnız t ve öncesiyle; geçerli bar H > L, V > 0, O/H/L/C > 0):
  Olay hazırlığı ORTAK_CETVEL.oc_olay_hazirla (giriş = t'den sonraki ilk geçerli bar AÇILIŞI, havuz üyeliği, aynı hissede 60 gün tekil).
  stop0 = hat x 0,98 (yön +) ya da tavan x 1,02 (yön -); d = |1 - stop0 / giriş| (giriş stop'un ötesindeyse olay ölçülmez, sayımda).
  15 geçerli bar (giriş barı dahil, en çok 30 birleşik takvim günü içinde): bar k kapanışı önce stop ile (bir önceki barın sonundaki stop
  seviyesi) karşılaştırılır; kapanış stop'un ötesindeyse STOP (çıkış ertesi açılış); değilse hedefler (+%5 / +%10 kapanışla; bilgi: High ile)
  işaretlenir; sonra stop güncellenir: +%5 görüldüyse stop >= giriş x 1,02, +%10 görüldüyse >= giriş x 1,07, takip stop >= en yüksek kapanış x 0,93
  (yön - aynası). HEDEF5 = +%5 stop'tan önce; STOP5 = stop +%5'ten önce; ikisi de değilse YOK.
  EŞ: aynı giriş günü, aynı momentum beşliği x likidite üçlüsü (OC panel kovası), olay hissesi hariç, aynı d ile aynı kural (min 3 eş).
  TABAN: aynı gün bütün havuz (bilgi). PLASEBO: aynı hisse, aynı dönemde rastgele bir giriş günü (havuzda), aynı d, aynı kural (olay başına 1).
  KAT = Σ olay / Σ eş oranı (OC.oc_kat ile aynı ay kümeli bootstrap %95). Hücre TUTAR = n >= 30 VE KAT5 alt > 1 VE P(stop önce) olay < eş
  VE plasebo KAT5 alt > 1. Etiket: İZ / EMARE / DESTEKLENMEDİ / ÖLÇÜLEMEDİ (YH_ESIK['etiket']; 'iz değil' sözü yazılmaz).
DENEMELER: Y1 S6 TABAN AL · Y2 S+ v2 TAM_DIP · Y3 KAZAN + DÖNÜŞ · Y4 Y1 + KAĞIT HAFIZASI · Y5 DÜZ TAVAN SAT (yön -).

Komut:  python YAPI_HEDEF.py guc [--islem 4]           güç tablosu (ABD 2023-26 rastgele hisse-gün; guc_tablosu.json + GUC_TABLOSU.md)
        python YAPI_HEDEF.py onkayit [--islem 4]       ON_KAYIT.md (YH_ESIK tam metni, sha'lar, getirisiz olay sayımı, kontrol listesi)
        python YAPI_HEDEF.py kos [--deneme Y1,Y2] [--islem 4] [--gitsiz]   kapı -> ölçüm -> sonuc.json, olay_Y*.csv.gz, RAPOR.md
        python YAPI_HEDEF.py rapor                     sonuc.json -> RAPOR.md
        2. TUR (YAPI_HEDEF_2_IS_TANIMI.md; Y6 = Y1 + hat net + gerçek kırılım + stop <= %10 + büyük desen; Y7 = Y3 + kazan şartları + stop <= %10;
        Y8 = Y6 + patlamış yapı yok; Y8B bilgi):
        python YAPI_HEDEF.py onkayit2 [--islem 4]      ON_KAYIT_2.md (huni, getirisiz sayım, Y1-Y5 eşik mührü, kontrol listesi)
        python YAPI_HEDEF.py kos --deneme Y6,Y7,Y8 [--islem 4]   kapı (tur 2) -> ölçüm -> sonuc.json'a ekler, olay_Y6..Y8B.csv.gz, RAPOR_2.md
        python YAPI_HEDEF.py rapor2                    sonuc.json -> RAPOR_2.md (RAPOR.md'ye dokunmaz)
        3. TUR (YAPI_HEDEF_3_IS_TANIMI.md; Y9 = Y1 olayı + F15 <= 0,25 + F17 <= -0,20 düşüş sonrası dipte; Y9b = Y9 + F1 >= 3 + F11 >= 0,01;
        Y9c = F15 >= 0,75 tepede (iki yönlü etiket); Y9d orta bilgi; özellikler goz_etiket/ozellik_Y1.csv.gz; konum eşli KAT; etiket en fazla EMARE):
        python YAPI_HEDEF.py onkayit3 [--islem 4]      ON_KAYIT_3.md (§2 dürüstlük notu, bakılmış hücre işareti, huni, mühürler, kontrol listesi)
        python YAPI_HEDEF.py kos --deneme Y9,Y9b,Y9c,Y9d [--islem 4]   kapı (tur 3) -> ölçüm + konum eşli KAT + Y1 regresyonu -> RAPOR_3.md
        python YAPI_HEDEF.py rapor3                    sonuc.json -> RAPOR_3.md
Colab:  exec(open('YAPI_HEDEF.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_BIST.pkl, V_ABD.pkl, V_AVR.pkl (git worktree add /tmp/iv origin/islenmis-veri; python FON_IZI.py vpac /tmp/iv/veri /tmp/veri).
Komisyon / kayma YOK. Evren bugün işlem gören hisseler: hayatta kalma yanlılığı (hedef payı yukarı, stop payı aşağı yanlı okunmalı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_YH = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_YH = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_YH not in sys.path:
    sys.path.insert(0, KOK_YH)

import ORTAK_CETVEL as OC  # noqa: E402
import S6_TABAN as S6  # noqa: E402
import SIKISMA_YENIDEN as SY  # noqa: E402

yhlog = logging.getLogger("col.yapi_hedef")
if not yhlog.handlers:
    _yh_h = logging.StreamHandler(sys.stderr)
    _yh_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yapi_hedef: %(message)s", "%H:%M:%S"))
    yhlog.addHandler(_yh_h)
    yhlog.setLevel(logging.INFO)
    yhlog.propagate = False

YH_SURUM = "YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo"
YH_YOL = {"cikti": os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef"), "veri": os.environ.get("YH_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_YH, "YAPI_HEDEF.py"), "oc_kod": os.path.join(KOK_YH, "ORTAK_CETVEL.py"),
          "s6_kod": os.path.join(KOK_YH, "S6_TABAN.py"), "fv_kod": os.path.join(KOK_YH, "FITIL_V2.py"),
          "y2_olay": os.path.join(KOK_YH, "arastirma_cikti", "fitil_v2", "olay_TAM_DIP.csv.gz"),
          "is_tanimi": os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_IS_TANIMI.md"),
          "satir_buyuk": os.environ.get("YH_SATIR_BUYUK", "/tmp/yapi_hedef_satir")}
YH_DOSYA = {"onkayit": "ON_KAYIT.md", "sonuc": "sonuc.json", "rapor": "RAPOR.md", "guc_json": "guc_tablosu.json", "guc_md": "GUC_TABLOSU.md",
            "satir": "olay_{d}.csv.gz"}
YH_DENEMELER = ["Y1", "Y2", "Y3", "Y4", "Y5"]
YH_SATIR_AZAMI_MB = 5.0
# 2. tur (17 Kas 2026 akşam; arastirma_cikti/yapi_hedef/YAPI_HEDEF_2_IS_TANIMI.md; Cemal'in değerlendirmesi E1-E11). Y8B bilgi satırıdır (karar değil).
YH_DENEMELER_2 = ["Y6", "Y7", "Y8", "Y8B"]
# 3. tur (18 Kas 2026; arastirma_cikti/yapi_hedef/YAPI_HEDEF_3_IS_TANIMI.md; Cemal'in çöl tanımı: düşüş sonrası dipte). Y9d bilgi satırıdır.
YH_DENEMELER_3 = ["Y9", "Y9b", "Y9c", "Y9d"]
YH_DENEMELER_HEPSI = YH_DENEMELER + YH_DENEMELER_2 + YH_DENEMELER_3   # dizin (plasebo / denetim tohumu) Y1-Y8B için önceki turlarla aynı
YH_DOSYA.update({"onkayit2": "ON_KAYIT_2.md", "rapor2": "RAPOR_2.md"})
YH_YOL["is_tanimi2"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_2_IS_TANIMI.md")
YH_DOSYA.update({"onkayit3": "ON_KAYIT_3.md", "rapor3": "RAPOR_3.md"})
YH_YOL["is_tanimi3"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_3_IS_TANIMI.md")
YH_YOL["ozellik"] = os.environ.get("YH_OZELLIK", os.path.join(KOK_YH, "arastirma_cikti", "goz_etiket", "ozellik_Y1.csv.gz"))

# ================================================================ EŞİKLER (ön kayıtta mühürlü; sonuç görüldükten sonra DEĞİŞMEZ)
YH_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "kriz": "2026-08-31",
    "cetvel": "ORTAK_CETVEL v1.0: oc_veri (geçerli bar, kriz kesiği, ETF dışı), oc_panel (havuz 'gecmis': likidite alt %20 dışı, geçmiş bölünme "
              "şüphesi dışı, 5 momentum x 3 likidite kovası), oc_olay_hazirla (giriş t+1 açılış, 60 gün tekil), dönem = giriş günü",
    "olcu": {
        "ufuk": 15, "pencere_azami": 30,
        "ufuk_tanim": "giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü "
                      "içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural)",
        "hedef": [0.05, 0.10], "karar_hedef": 0.05, "karar_sutun": "kapanış (bilgi sütunu: High; yön -: Low)",
        "stop0": {"arti": "hat x 0,98", "eksi": "tavan x 1,02", "hat_carpan": 0.98, "tavan_carpan": 1.02},
        "d_tanim": "d = 1 - stop0 / giriş (yön +), stop0 / giriş - 1 (yön -); d <= 0 (giriş açılışı stop'un ötesinde) -> olay ölçülmez (sayım "
                   "'giris_stop_otesi'; karar giriş anında bilinir)",
        "stop": {"kilit5": 0.02, "kilit10": 0.07, "takip": 0.07,
                 "tanim": "bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse "
                          "+%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop "
                          "güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). "
                          "Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07)."},
        "olay_gosterge": {"h5": "+%5 kapanışla stop'tan önce, 15 barda", "h10": "+%10 kapanışla stop'tan önce, 15 barda",
                          "st5": "stop, +%5'ten önce, 15 barda (P(stop önce))", "h5H / h10H": "aynı, High ile (bilgi)"},
        "cikis_bilgi": {"zaman_tavani": 60, "ters_n": 10, "ters_n_aralik": [10, 30], "ters_bant": 0.06, "ters_kir": 0.02,
                        "tanim": "takip stoplu getiri (bilgi, yalnız olay): 60 geçerli bara kadar; çıkış = stop (ertesi açılış) YA DA yeni TERS "
                                 "OLUŞUM (yön +: girişten sonra oluşmuş son n barda bant max H / min L - 1 <= %6 ve kapanış < min L x 0,98; "
                                 "n 10..30 aralığında var olması n = 10'da var olmasına eşittir [bant n ile büyür, min L küçülür] -> n = 10; "
                                 "pencere giriş barından önceye taşmaz; çıkış ertesi açılış; yön -: kapanış > max H x 1,02) YA DA 60. bar kapanışı "
                                 "(zaman). Veri biterse son kapanış ('kesik'). Getiri = yön x (çıkış / giriş - 1); komisyon yok."},
    },
    "kontrol": {"min_es": 3, "es": "aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = "
                                   "giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı",
                "taban": "aynı gün bütün havuz (olay hissesi hariç, ölçülebilir), aynı d (bilgi)",
                "plasebo_tohum": 1717, "plasebo_deneme": 50,
                "plasebo": "olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; "
                           "aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j]"},
    "kat": {"bootstrap": 2000, "tohum": 27, "guven": [0.025, 0.975], "kume": "giriş ayı",
            "tanim": "KAT = Σ olay göstergesi / Σ eş oranı (ORTAK_CETVEL.oc_kat ile aynı; ay kümeli bootstrap 2000, tohum 27); p = bootstrap KAT <= 1 payı "
                     "(tek taraflı, bilgi; BH q = 0,10 karar hücrelerinde 5 deneme x 4 hücre, bilgi)"},
    "karar": {"n_esik": 30,
              "tanim": "hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş "
                       "(nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar)",
              "hucre_karar": [["ABD", "2023"], ["ABD", "2024-26"], ["AVR", "2023"], ["AVR", "2024-26"]],
              "hucre_bilgi": [["BIST", "2023"], ["BIST", "2024-26"], ["*", "2016-22"]]},
    "etiket": {"n_yeter": 1000, "guc_esik": 0.80, "kat_ref": 1.25,
               "hucre": "n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ",
               "guc_bak": "güç tablosunda (yön aynı) hücre n'inden küçük ya da eşit en büyük n satırı, d ızgarasının EN KÜÇÜK gücü (muhafazakâr)",
               "genel": "dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki "
                        "dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek "
                        "hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. "
                        "'İz değil' sözü yazılmaz."},
    "guc": {"n": [30, 100, 300, 1000, 3000], "kat_ref": [1.0, 1.25, 1.5], "d": [0.03, 0.06, 0.10], "yon": [1, -1], "tekrar": 200,
            "havuz": 6000, "tohum": 1477, "bas": "2023-01-01", "son": "2026-06-30", "pazar": "ABD",
            "tanim": "ABD giriş 2023-01-01 .. 2026-06-30 havuzda (ok, kova) rastgele hisse-gün (6.000, yerine koymadan); her biri için olay "
                     "göstergeleri, eş oranları (aynı gün aynı kova, min 3) ve plasebo (aynı hisse aynı dönem rastgele gün) gerçek fiyatla ve "
                     "sabit d ile hesaplanır. Tekrar: n olay çekilir; KAT_ref > 1 ise h5 = 0 olan olaylar q = (KAT_ref Σ eş - Σ h5) / (n - Σ h5) "
                     "olasılıkla h5 = 1 (st5 = 0) yapılır; hücre TUTAR kuralı (4 şart; bootstrap ay kümeli 2000, vektör) uygulanır; güç = TUTAR payı. "
                     "KAT_ref = 1,0 enjeksiyonsuz (yanlış pozitif payı)."},
    "gelecek_denetimi": {"n": 5, "tohum": 615,
                         "tanim": "her deneme x pazar rastgele 5 olay: hissenin verisi t'de kesilir, sinyal yeniden üretilir; t'de aynı sinyal ve "
                                  "aynı hat / stop0 çıkmalı (yoksa koşu DURUR)"},
    "denemeler": {
        "Y1": {"ad": "S6 TABAN AL", "yon": 1, "s6_prm": "S6_TABAN.S6_PRM varsayılan (v1.1)",
               "tanim": "S6_TABAN.s6_taban (SY.sy_veri_hazirla girdisi) 'al' günleri (AL ve AL_BOLGESIZ) = taban kırılım mumu (C_t > TAVAN(t-1)); "
                        "hat = bölge dibi: durum AL ise kutu_alt (açık bölgenin as-of t alt kenarı), AL_BOLGESIZ ise DİP(t-1) (bir önceki barın "
                        "taban penceresinin en düşük Low'u)"},
        "Y2": {"ad": "S+ v2 TAM_DIP", "yon": 1,
               "tanim": "arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz (sembol, pazar, tarih) olayları; hat = FITIL_V2.fv_olcu HAT (t dahil son 10 "
                        "geçerli barın en düşük Low'u; yeniden hesaplanır); giriş dosyadaki 'giris' ile aynı olmalı (sayım)"},
        "Y3": {"ad": "KAZAN + DÖNÜŞ", "yon": 1, "n": [20, 60], "sag": 5, "sag_carpan": 1.03, "baglam_gun": 120, "baglam_dusus": 0.15,
               "tanim": "t için pencere W = [t-n, t-1] (n geçerli bar, t hariç), n = 20..60: (a) Low serisine 2. derece en küçük kareler "
                        "uyumunun x^2 katsayısı a > 0; (b) sağ kenar dibi min L(son 5 bar of W) > orta üçte bir dibi min L(W[n//3 : 2n//3]) x 1,03; "
                        "(c) son kapanış C_{t-1} > dip + (tavan - dip) / 2, dip = min L(W), tavan = max H(W); (d) kırılım C_t > tavan. "
                        "(a)-(d) tutan EN BÜYÜK n seçilir; hat = dip(W). Bağlam: C_t <= max(C, t dahil son 120 geçerli bar) x 0,85"},
        "Y4": {"ad": "Y1 + KAĞIT HAFIZASI", "yon": 1, "gun": 250, "ufuk": 15, "hedef": 0.05, "esik": 0,
               "tanim": "Y1 olayı t, hafıza = (son 250 barda [t-250, t-1] AL ile biten S6 bölgelerinden (durum AL; a + 15 <= t, sonucu t'de "
                        "bilinen) a+1 .. a+15 kapanışlarından biri >= açılış(a+1) x 1,05 olanlar) - (son 250 barda KIRILDI ile biten bölgeler); "
                        "hafıza >= 0 -> Y4 (yalnız geçmiş, t'ye kadar)"},
        "Y5": {"ad": "DÜZ TAVAN SAT", "yon": -1, "n": [8, 70], "bant": 0.12, "net": 0.03, "tavanTol": 0.05, "konum_gun": 120, "konum": 0.75,
               "yuk_gun": 60, "yuk": 0.20, "sat": 0.98, "stop": 1.02,
               "tanim": "TAVAN(t-1): pencere W = [t-n, t-1], n = 8..70: bant max H / min L - 1 <= 0,12; net |C_{t-1} / C_{t-n} - 1| <= 0,03; "
                        "yüksekler düz (S6 dip savunmasının aynası): max H(ikinci yarı) <= max H(ilk yarı, n//2 bar) x 1,05; önceki yükseliş: "
                        "C_{t-n-1} / min C(son 60 bar, t-n-1 dahil) - 1 >= 0,20; tutan EN BÜYÜK n. Konum: (C_{t-1} - min C120) / (max C120 - min C120) "
                        ">= 0,75 (t-1 dahil 120 geçerli kapanış). SAT_t = C_t < min L(W) x 0,98. stop0 = max H(W) x 1,02; hedef -%5 / -%10 (yön -)"},
        # ---- 2. TUR (YAPI_HEDEF_2_IS_TANIMI.md §3; sonuç görülmeden sabit). Y1-Y5 girdileri yukarıda AYNEN (yh_esik_sha_tur1 = 1. tur mührü).
        "Y6": {"ad": "Y1 + HAT NET + GERÇEK KIRILIM + STOP YAKIN + BÜYÜK DESEN", "yon": 1, "tur": 2, "taban": "Y1",
               "hat_bant": 0.015, "dokunus_min": 3, "dokunus_egim": 0.99, "kir_pay": 0.01, "stop_uzak": 0.10,
               "buyuk_gun": 250, "buyuk_parca": 25, "buyuk_egim": -0.05, "e5b": {"hat_carpan": 0.98, "giris_carpan": 0.95},
               "tanim": "Y1 olayı t (S6 'al' günü; hat ve tavan Y1'deki gibi) + dört şart. BÖLGE = durum AL ise [kutu_sol_i(t), t-1] (açık S6 "
                        "bölgesinin as-of t kutusu, t hariç), AL_BOLGESIZ ise t-1 taban penceresi [bas_i(t-1), t-1]. (a) HAT NET (E2): bölgede "
                        "Low <= hat x 1,015 olan bar sayısı >= 3 VE son dokunuşun Low'u >= ilk dokunuşun Low'u x 0,99 (eğim aşağı değil); (b) GERÇEK "
                        "KIRILIM (E3): C_t > tavan x 1,01 (tavan = Y1 TAVAN(t-1)) VE (H_t - L_t) >= bölge içi (H - L) medyanı; (c) STOP UZAKLIĞI "
                        "(E5a): sinyalde C_t / hat - 1 <= 0,10 (ön eleme), ölçümde gerçek giriş (t+1 açılış) / hat - 1 <= 0,10 yeniden denetlenir, "
                        "aşan olay ölçülmez ve 'stop_uzak' sayımına düşer; (d) BÜYÜK DESEN ALÇALAN DEĞİL (E1): [t-250, t-1] 250 geçerli bar, ardışık "
                        "10 parça x 25 bar, her parçanın min Low'u; bu 10 noktaya doğru (en küçük kareler, x = 0..9); eğim = uyum(9) / uyum(0) - 1 "
                        ">= -0,05 (uyum(0) <= 0 ise şart tutmaz); t'den önce 250 geçerli bar yoksa (d) UYGULANMAZ (şart geçer, ek sütunda "
                        "'buyuk_desen=NA'). stop0 = hat x 0,98 (1. turla aynı). Bilgi (E5b): stop0b = max(hat x 0,98, giriş x 0,95) ile olay ve eş "
                        "(aynı gün aynı kova, aynı d_b) hedef / stop payları ayrı sütun (b_*); karar satırı değil"},
        "Y7": {"ad": "Y3 + KAZAN ŞARTLARI + STOP YAKIN", "yon": 1, "tur": 2, "taban": "Y3",
               "kenar": 1.05, "mum_k": 0.90, "atr_gun": 250, "atr_min": 120, "dip_bant": 0.015, "dokunus_min": 3, "stop_uzak": 0.10,
               "e5b": {"hat_carpan": 0.98, "giris_carpan": 0.95},
               "tanim": "Y3 olayı t (Y3'ün seçtiği EN BÜYÜK n ile pencere W = [t-n, t-1], hat = dip(W)) + dört şart, aynı W üzerinde (Y7 ⊆ Y3 "
                        "sinyalleri). Üçte birler: ilk = W[0 : n//3], orta = W[n//3 : 2n//3] (Y3'teki orta ile aynı), son = W[2n//3 : n]. (a) İKİ "
                        "KENAR: min L(ilk) >= min L(orta) x 1,05 VE min L(son) >= min L(orta) x 1,05; (b) DİPTE KÜÇÜK MUM: orta üçte birde mum boyu "
                        "(H - L) / C medyanı <= 0,90 x ATR250, ATR250 = pencereden ÖNCEKİ 250 geçerli barın ortalama TR / C_önceki'si (S6 refOnce "
                        "ile aynı birim; 250 yoksa en az 120 bar, 120 de yoksa şart tutmaz); (c) DİP SAVUNMASI: W'de Low <= dip(W) x 1,015 olan bar "
                        "sayısı >= 3; (d) E5a: sinyalde C_t / hat - 1 <= 0,10, ölçümde giriş / hat - 1 <= 0,10 (aşan 'stop_uzak'). Bilgi E5b Y6 gibi"},
        "Y8": {"ad": "Y6 + CEMAL HAFIZASI (patlamış yapı yok)", "yon": 1, "tur": 2, "taban": "Y6", "gun": 250, "stop_uzak": 0.10,
               "tanim": "Y6 olayı t ve [t-250, t-1] içinde durum KIRILDI ile biten S6 bölgesi (kapanış < dip x 0,98; S6 kirTol 0,02) YOK -> olay; "
                        "varsa düşer (yalnız geçmiş; Y4'teki KIRILDI sayımıyla aynı aralık)"},
        "Y8B": {"ad": "Y6 + patlamış yapı VAR (bilgi, aleyhte)", "yon": 1, "tur": 2, "taban": "Y6", "gun": 250, "stop_uzak": 0.10, "bilgi": True,
                "tanim": "Y8'in tersi: Y6 olayı ve [t-250, t-1] içinde KIRILDI ile biten S6 bölgesi >= 1 (karşılaştırma için bilgi satırı; etiket "
                         "yazılır ama karar değildir). `kos --deneme ...Y8` Y8B'yi kendiliğinden ekler"},
        # ---- 3. TUR (YAPI_HEDEF_3_IS_TANIMI.md §3; sonuç görülmeden sabit). Y1-Y8B girdileri yukarıda AYNEN (yh_esik_sha_tur2 = 2. tur mührü).
        "Y9": {"ad": "DÜŞÜŞ SONRASI DİPTE", "yon": 1, "tur": 3, "taban": "Y1", "F15_ust": 0.25, "F17_ust": -0.20,
               "tanim": "Y1 OLAYI (OC tekilleştirmesi sonrası; ozellik_Y1.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile eşlenir) VE "
                        "F15 <= 0,25 VE F17 <= -0,20. F15 = 120 gün konumu (C_t - min C) / (max C - min C), t DAHİL son 120 geçerli kapanış (GOZ_ETIKET "
                        "tanımı; C_t sinyal günü kapanışı, giriş t+1 açılış: karar anında bilinir); F17 = bölge öncesi 60 gün düşüş C(sol) / max(C, "
                        "[sol-60, sol-1]) - 1. Değerler dosyadan (6 anlamlı basamak) okunur; NaN şart tutmaz",
               "ozellik_prm": {"hat_bant": 0.015, "konum_gun": 120, "dusus_gun": 60,
                               "tanim": "GOZ_ETIKET GE_ESIK['ozellik'] ile aynı (F1 dokunuş bandı, F15 konum penceresi, F17 düşüş penceresi); yalnız "
                                        "geleceğe bakma (prefix) denetiminde yeniden hesap için"},
               "tur3_kural": {
                   "ceyrek": [0.25, 0.50, 0.75],
                   "ceyrek_tanim": "F15 çeyreği: Ç1 [0, 0,25], Ç2 (0,25, 0,50], Ç3 (0,50, 0,75), Ç4 [0,75, 1] (Y9 / Y9c sınırlarıyla aynı)",
                   "konum_es": "KONUM EŞLİ KAT (zorunlu bilgi satırı): eş = 1. turun eşi (aynı giriş günü, aynı OC kovası, havuzda, olay hissesi hariç, "
                               "15 barı ölçülebilir, AYNI d ve kural) VE eşin F15'i olayın F15 çeyreğinde; eşin F15'i = giriş gününden ÖNCEKİ son "
                               "geçerli barında (olayın t'siyle aynı bilgi anı) t dahil son 120 geçerli kapanışla aynı formül; en az 3 eş; KAT ve "
                               "ay kümeli %95 1. turla aynı (yh_kat). Olayın çeyreği dosyadaki F15'ten",
                   "konum_uyum_min": 0.99,
                   "konum_uyum": "olayların panelden hesaplanan F15 çeyreği dosyadaki çeyrekle >= %99 aynı olmalı (aynı formül denetimi), değilse koşu DURUR",
                   "regresyon": "Y9* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, "
                                "tb_h5, getiri sütunlarında eşit olmalı (göreli 1e-4; dosya 6 anlamlı basamak), değilse koşu DURUR; ayrıca pazar "
                                "başına ozellik dosyası (sembol, tarih) kümesi = şimdiki kodun Y1 olay kümesi",
                   "bakilmis": [["ABD", "2023"], ["ABD", "2024-26"], ["AVR", "2023"], ["AVR", "2024-26"]],
                   "dis_sinama": [["ABD", "2016-22"], ["AVR", "2016-22"]],
                   "bist_bilgi": [["BIST", "2016-22"], ["BIST", "2023"], ["BIST", "2024-26"]],
                   "ters": "hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1",
                   "etiket": "Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön "
                             "kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış "
                             "hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ "
                             "vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS "
                             "EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket "
                             "her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar"},},
        "Y9b": {"ad": "Y9 + HAT NET + GERÇEK KIRILIM", "yon": 1, "tur": 3, "taban": "Y9", "F15_ust": 0.25, "F17_ust": -0.20, "F1_min": 3,
                "F11_min": 0.01,
                "tanim": "Y9 olayı VE F1 >= 3 (bölgede Low <= hat x 1,015 dokunuş sayısı) VE F11 >= 0,01 (C_t / tavan - 1; Cemal E2 / E3 dip bağlamında)"},
        "Y9c": {"ad": "TEPEDE (şemsiye karşıtı)", "yon": 1, "tur": 3, "taban": "Y1", "F15_alt": 0.75, "iki_yonlu": True,
                "tanim": "Y1 olayı VE F15 >= 0,75. Yön + ile ölçülür (kodun yukarı kırılımı); beklenti yazılmaz; iki yönlü etiket (TERS EMARE kuralı)"},
        "Y9d": {"ad": "ORTA (bilgi)", "yon": 1, "tur": 3, "taban": "Y1", "F15_ara": [0.25, 0.75], "bilgi": True,
                "tanim": "Y1 olayı VE 0,25 < F15 < 0,75 (bilgi satırı; etiket yazılır, karar değildir)"},
    },
    "s6_prm": {k: v for k, v in S6.S6_PRM.items()},
}

YH_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = aynı giriş günü, aynı OC momentum beşliği x likidite üçlüsü kovası, olay hissesi hariç, AYNI giriş (t+1 açılış) / AYNI d "
                   "ile stop0 / aynı hedefler / aynı takip kuralı / aynı 15 bar (yh_sim tek fonksiyon); taban = aynı gün bütün havuz; plasebo = aynı "
                   "hisse rastgele gün aynı kural (hisse etkisi); mekanik üstünlük: d eşlere aynen verilir (stop uzaklığı farkı dışlandı), kırılım "
                   "mumunun kendisi (t) ölçüye girmez (giriş t+1 açılış); güç simülasyonu KAT_ref 1,0 = yanlış pozitif payı"),
    "K2": ("EVET", "sinyaller yalnız t ve öncesiyle (S6 durum makinesi nedensel; Y3 / Y5 pencereleri t-1'de biter, t yalnız kırılım kapanışı; Y4 "
                   "hafızası a + 15 <= t şartıyla); test_yapi_hedef 'geleceğe bakma' bütün günlerde kesik seri = tam seri; koşuda her deneme x pazar "
                   "5 rastgele olay kesik veriyle yeniden üretilir (yh_gelecek_denetimi, tutmazsa DURUR); hedef / stop yalnız giriş ve sonrası fiyatla"),
    "K3": ("EVET", "OC.oc_veri_hazirla + SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0 olmayan bar atılır; bütün pencereler geçerli bar dizisinde; 15 bar "
                   "ve takip yalnız geçerli bar; sinyal günü geçersiz bar olamaz (veriden atılmış)"),
    "K4": ("EVET", "OC.oc_olay_hazirla: aynı hissede 60 birleşik takvim gününde tek olay (deneme başına); n = bağımsız olay; hücre tablosunda "
                   "getiri ortalama + medyan"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC); eş ve plasebo da kendi giriş günlerinin açılışı; stop çıkışı ertesi açılış; "
                   "test 'giriş ertesi açılış'"),
    "K6": ("EVET", "tek kip V_*.pkl (fi_k1_veri düzeltilmiş fiyat); hedef / stop / d oran (birimden bağımsız); AVR yerel para, likidite kovası EUR "
                   "(OC Kur); bölünme şüphesi geçmiş penceresinde havuz dışı (OC); ileri 15 barda dışlama yok (OC kuralı: sonuca göre seçim olurdu)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD 1.411, k34 / Tiingo yok; V_AVR, V_BIST); batanlar yok -> hedef payı yukarı, stop payı "
                   "aşağı yanlı; eş ve plasebo aynı evrenden olduğu için KAT'ta yanlılık kısmen birbirini götürür; rapora yazılır"),
    "K8": ("EVET", "3 pazar x 3 dönem (2016-22 / 2023 / 2024-26); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80 (guc_tablosu.json); "
                   "iki yarı KAT (bilgi); 5 deneme x 4 karar hücresi BH q 0,10 (bilgi); küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "YH_ESIK sha256 + YAPI_HEDEF.py / ORTAK_CETVEL.py / S6_TABAN.py / FITIL_V2.py sha256 + güç tablosu sha256 + Y2 olay dosyası sha256 "
                   "ON_KAYIT.md'de; yh_kapi hepsini + ON_KAYIT ve kodun git'e işlenmiş / değişmemiş olmasını + IZ_KARNE.ik_kontrol_kapisi'ni "
                   "denetler; ön kayıt ayrı commit (ölçümden önce); eşik sonuca göre oynanmaz; sapma SAPMA-n olarak koşudan önce"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV; Y2 olay dosyası FITIL_V2 kos çıktısı (sha ön kayıtta, giriş günü OC ile "
                          "yeniden üretilir ve dosyadakiyle karşılaştırılır)"),
    "K11": ("EVET", "olay_Y*.csv.gz satır dosyaları (olay + eş + taban + plasebo göstergeleri); RAPOR.md 'YENİDEN ÜRETİM' bölümünde iki hücrenin "
                    "KAT'ı satır dosyasından 5 satırlık bağımsız komutla; test KAT = OC.oc_kat"),
    "K12": ("EVET", "etiketler yalnız YH_ESIK['etiket'] kuralıyla (İZ / EMARE / DESTEKLENMEDİ / ÖLÇÜLEMEDİ); 'iz değil' yazılmaz; hedef payı fiyat "
                    "dokunuşu, getiri komisyonsuz fiyat değişimi; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_yh; yasak defter dosyalarına dokunulmaz (git diff ile denetim); e-posta / anahtar taraması "
                    "(test + yazım öncesi _yh_sizinti); ücretli veri yok; push yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm (yapı kuralları hedef payı)"),
}


YH_KONTROL_2: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş / taban / plasebo 1. turla AYNI kod (yh_olay_olc, yh_sim): aynı giriş günü, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar; "
                   "yeni şartlar yalnız olay seçimini değiştirir; E5a stop uzaklığı şartı d'yi küçültür ama eşlere AYNI d verilir (mekanik stop farkı "
                   "dışlandı); E5b bilgi satırında da eşlere aynı d_b; Y8B (aleyhte) karşılaştırma satırı; güç tablosu 1. turunki (aynı kural)"),
    "K2": ("EVET", "Y6 bölgesi [sol, t-1] ve hat / tavan t ve öncesi (S6 durum makinesi nedensel); büyük desen [t-250, t-1]; Y7 W = [t-n, t-1], ATR "
                   "pencere öncesi; Y8 KIRILDI sayımı [t-250, t-1]; E5a ölçüm denetimi giriş açılışı (karar anında bilinir); test_yapi_hedef 'geleceğe "
                   "bakma' Y6 / Y7 / Y8 / Y8B kesik seri = tam seri; koşuda her deneme x pazar 5 rastgele olay kesik veriyle (yh_gelecek_denetimi, DURUR)"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (OC.oc_veri_hazirla + SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0); dokunuş / medyan mum / büyük desen / "
                   "ATR yalnız geçerli barlarda"),
    "K4": ("EVET", "OC.oc_olay_hazirla aynı hissede 60 takvim günü tekil (deneme başına); stop_uzak düşmesi tekilden SONRA (sayımda); n = bağımsız "
                   "olay; getiri ortalama + medyan"),
    "K5": ("EVET", "giriş t+1 açılışı (OC); E5a ölçümde gerçek giriş açılışıyla yeniden denetlenir (C_t ön elemesi yalnız sinyal günü bilgisi)"),
    "K6": ("EVET", "aynı V_*.pkl tek kip; bütün yeni şartlar oran (dokunuş bandı, kırılım payı, eğim, iki kenar, mum / ATR oran birimi); AVR yerel "
                   "para (oran birimden bağımsız)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo aynı evrenden; rapora yazılır"),
    "K8": ("EVET", "şartlar olay sayısını düşürür: huni ön kayıtta (getirisiz); n < 30 ÖLÇÜLEMEDİ, DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; "
                   "Y6 / Y7 / Y8 x 4 karar hücresi BH q 0,10 (bilgi, 1. tur BH'si ayrı); küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_2.md: YH_ESIK sha (yeni), ESIK_TUR1_SHA (Y6-Y8B çıkarılınca 1. tur mührü = ON_KAYIT.md ve güç tablosu sha'sı; Y1-Y5 "
                   "eşikleri değişmedi kanıtı), kod / OC / S6 / FV / güç / Y2 sha; yh_kapi(tur 2) hepsini + git kaydını + ik_kontrol_kapisi'ni "
                   "denetler; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler Cemal'in değerlendirmesinden (sonuç görülerek) yazıldı: bu ölçüm "
                   "bağımsız kanıt değil, ileri test gerekir (raporda)"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV"),
    "K11": ("EVET", "olay_Y6..Y8B.csv.gz satır dosyaları; RAPOR_2.md 'YENİDEN ÜRETİM' iki hücre bağımsız komutla; Y1 ABD 2023 regresyonu (n 2040, "
                    "KAT5 0,9752) yeni kodla yeniden üretildi"),
    "K12": ("EVET", "etiket yalnız YH_ESIK['etiket'] kuralıyla; Y8B 'bilgi' (karar değil); 'iz değil' yazılmaz; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ önekli); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar taraması; "
                    "push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


class YHHata(RuntimeError):
    """Durdurucu hata: mühür / kod sha'sı tutmuyor, ön kayıt işlenmemiş, veri yok, geleceğe bakma denetimi tutmadı, girdi bozuk."""


# ================================================================ 0) ORTAK
_YH_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_YH_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|şifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}")


def _yh_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _yh_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def yh_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    s = json.dumps(YH_ESIK if E is None else E, sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def yh_esik_sha_tur1(E: Optional[Dict[str, Any]] = None) -> str:
    """YH_ESIK'ten 2. tur denemeleri çıkarılınca sha: 1. tur mührüne (ON_KAYIT.md, güç tablosu) EŞİT olmalı (Y1-Y5 eşikleri değişmedi kanıtı)."""
    E = YH_ESIK if E is None else E
    E1 = dict(E); E1["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_2 + YH_DENEMELER_3}
    return yh_esik_sha(E1)


def yh_esik_sha_tur2(E: Optional[Dict[str, Any]] = None) -> str:
    """YH_ESIK'ten 3. tur denemeleri çıkarılınca sha: 2. tur mührüne (ON_KAYIT_2.md YH_ESIK_SHA) EŞİT olmalı (Y1-Y8B eşikleri değişmedi kanıtı)."""
    E = YH_ESIK if E is None else E
    E2 = dict(E); E2["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_3}
    return yh_esik_sha(E2)


def _yh_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or YH_YOL["cikti"], YH_DOSYA.get(ad, ad))


def _yh_sizinti(metin: str, ad: str) -> None:
    if _YH_EPOSTA.search(metin) or _YH_ANAHTAR.search(metin):
        raise YHHata(f"{ad}: e-posta / anahtar benzeri metin var; yazılmadı")


def _yh_yaz(yol: str, metin: str, ad: str) -> None:
    _yh_sizinti(metin, ad)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)


def _yz(x: Any, n: int = 1) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"%{100 * float(x):.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def _sy(x: Any, n: int = 2) -> str:
    try:
        return "-" if x is None or not np.isfinite(float(x)) else f"{float(x):.{n}f}".replace(".", ",")
    except (TypeError, ValueError):
        return "-"


def _yh_json(o: Any) -> Any:
    """json.dumps default: numpy sayıları / bool / Timestamp."""
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.datetime, _dt.date)):
        return str(o)
    return str(o)


def _yh_kaydir(x: np.ndarray, k: int) -> np.ndarray:
    """out[i] = x[i-k] (k >= 0; başta NaN)."""
    x = np.asarray(x, float)
    if k <= 0:
        return x.copy()
    if len(x) <= k:
        return np.full(len(x), np.nan)
    return np.r_[np.full(k, np.nan), x[:-k]]


def _yh_roll(x: np.ndarray, n: int, ne: str) -> np.ndarray:
    s = pd.Series(np.asarray(x, float))
    r = s.rolling(n, min_periods=n)
    return (r.max() if ne == "max" else r.min()).to_numpy()


def _yh_hazir(df: pd.DataFrame) -> pd.DataFrame:
    """SY.sy_veri_hazirla (geçerli bar, kriz kesiği); oc_veri çıktısında idempotent."""
    return SY.sy_veri_hazirla(df, SY.SY_ESIK)


# ================================================================ 1) SİNYALLER (hisse başına; yalnız t ve öncesi)
_SIG_KOL = ["tarih", "hat", "stop0", "yon", "n", "tavan", "ek"]


def _yh_bos() -> pd.DataFrame:
    return pd.DataFrame(columns=_SIG_KOL)


def yh_s6_hisse(df: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Y1 ve Y4 sinyalleri: S6 'al' günleri; hat = kutu_alt (AL) ya da DİP(t-1) (AL_BOLGESIZ); Y4 = hafıza >= 0."""
    d = _yh_hazir(df)
    P = S6.s6_prm(None)
    if len(d) < P["atrGun"] + 2:
        return _yh_bos(), _yh_bos()
    T = S6.s6_taban(d, None)
    ix = d.index; N = len(d)
    al = T["al"].to_numpy(bool)
    durum = T["durum"].to_numpy(object)
    dip_onc = _yh_kaydir(T["dip"].to_numpy(float), 1)
    tav_onc = _yh_kaydir(T["tavan"].to_numpy(float), 1)
    n_onc = _yh_kaydir(T["n"].to_numpy(float), 1)
    hat = np.where(durum == "AL", T["kutu_alt"].to_numpy(float), dip_onc)
    # Y4 hafıza (yalnız geçmiş)
    Y4 = E["denemeler"]["Y4"]; C = d.Close.to_numpy(float); O = d.Open.to_numpy(float)
    ALb = np.flatnonzero(durum == "AL"); KIRb = np.flatnonzero(durum == "KIRILDI")
    u = Y4["ufuk"]; out5 = np.zeros(len(ALb), bool); bil = ALb + u      # sonucu bil günü (a + 15) kapanışında bilinir
    for q, a in enumerate(ALb):
        if a + u < N:
            out5[q] = bool(np.nanmax(C[a + 1:a + u + 1]) >= O[a + 1] * (1 + Y4["hedef"]))
    gi = np.flatnonzero(al)
    haf = np.zeros(len(gi), int); hit = np.zeros(len(gi), int); kir = np.zeros(len(gi), int)
    for q, i in enumerate(gi):
        m = (ALb >= i - Y4["gun"]) & (bil <= i)
        hit[q] = int(out5[m].sum())
        kir[q] = int(((KIRb >= i - Y4["gun"]) & (KIRb <= i - 1)).sum())
        haf[q] = hit[q] - kir[q]
    if not len(gi):
        return _yh_bos(), _yh_bos()
    hc = E["olcu"]["stop0"]["hat_carpan"]
    X = pd.DataFrame({"tarih": ix[gi], "hat": hat[gi], "stop0": hat[gi] * hc, "yon": 1, "n": n_onc[gi], "tavan": tav_onc[gi],
                      "ek": [f"{durum[i]};haf={h};hit={a};kir={k}" for i, h, a, k in zip(gi, haf, hit, kir)]})
    X["hafiza"] = haf
    X = X[np.isfinite(X.hat.to_numpy(float)) & (X.hat.to_numpy(float) > 0)].reset_index(drop=True)
    X4 = X[X.hafiza >= Y4["esik"]].reset_index(drop=True)
    return X, X4


def _yh_kare_agirlik(n: int) -> np.ndarray:
    """Pencere [0..n-1] için ikinci derece en küçük kareler uyumunda x^2 katsayısını veren doğrusal ağırlıklar."""
    x = np.arange(n, dtype=float) - (n - 1) / 2.0
    A = np.vstack([np.ones(n), x, x * x]).T
    return np.linalg.pinv(A)[2]


def yh_y3_hisse(df: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Y3 KAZAN + DÖNÜŞ: pencere [t-n, t-1], n = 20..60, en büyük tutan n; hat = pencere dibi; bağlam 120 bar tepesinden >= %15 aşağı."""
    Y = E["denemeler"]["Y3"]; d = _yh_hazir(df); N = len(d)
    if N < max(Y["n"][1], Y["baglam_gun"]) + 2:
        return _yh_bos()
    L, H, C = d.Low.to_numpy(float), d.High.to_numpy(float), d.Close.to_numpy(float)
    sec_n = np.zeros(N, int); sec_hat = np.full(N, np.nan); sec_tav = np.full(N, np.nan)
    sag = _yh_kaydir(_yh_roll(L, Y["sag"], "min"), 1)            # min L[t-5 .. t-1]
    c_onc = _yh_kaydir(C, 1)
    for n in range(Y["n"][1], Y["n"][0] - 1, -1):
        w = _yh_kare_agirlik(n)
        a_son = np.full(N, np.nan)                                 # a[e] pencere e-n+1 .. e
        if N >= n:
            a_son[n - 1:] = np.lib.stride_tricks.sliding_window_view(L, n) @ w
        a = _yh_kaydir(a_son, 1)                                  # t için pencere t-n .. t-1
        tav = _yh_kaydir(_yh_roll(H, n, "max"), 1); dip = _yh_kaydir(_yh_roll(L, n, "min"), 1)
        m3 = 2 * n // 3 - n // 3
        orta_son = _yh_roll(L, m3, "min")                          # biter e
        orta = _yh_kaydir(orta_son, n - 2 * n // 3 + 1)            # e = t - n + 2n//3 - 1
        with np.errstate(invalid="ignore"):
            ok = (a > 0) & (sag > orta * Y["sag_carpan"]) & (c_onc > dip + (tav - dip) / 2.0) & (C > tav)
        yeni = ok & (sec_n == 0)
        sec_n[yeni] = n; sec_hat[yeni] = dip[yeni]; sec_tav[yeni] = tav[yeni]
    mx120 = _yh_roll(C, Y["baglam_gun"], "max")
    with np.errstate(invalid="ignore"):
        bag = C <= mx120 * (1 - Y["baglam_dusus"])
    g = np.flatnonzero((sec_n > 0) & bag & np.isfinite(sec_hat) & (sec_hat > 0))
    if not len(g):
        return _yh_bos()
    hc = E["olcu"]["stop0"]["hat_carpan"]
    return pd.DataFrame({"tarih": d.index[g], "hat": sec_hat[g], "stop0": sec_hat[g] * hc, "yon": 1, "n": sec_n[g], "tavan": sec_tav[g],
                         "ek": [f"tepe120={C[i] / mx120[i] - 1:.3f}" for i in g]})


def yh_y5_hisse(df: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Y5 DÜZ TAVAN SAT (yön -): TAVAN(t-1) pencere [t-n, t-1], n = 8..70 en büyük tutan; SAT_t = C_t < min L x 0,98; stop0 = max H x 1,02."""
    Y = E["denemeler"]["Y5"]; d = _yh_hazir(df); N = len(d)
    if N < Y["konum_gun"] + 2:
        return _yh_bos()
    L, H, C = d.Low.to_numpy(float), d.High.to_numpy(float), d.Close.to_numpy(float)
    sec_n = np.zeros(N, int); sec_dip = np.full(N, np.nan); sec_tav = np.full(N, np.nan)   # bitiş e (= t-1) dizinli
    mnC60 = _yh_roll(C, Y["yuk_gun"], "min")
    for n in range(Y["n"][1], Y["n"][0] - 1, -1):
        h = n // 2
        mxH = _yh_roll(H, n, "max"); mnL = _yh_roll(L, n, "min")
        cbas = _yh_kaydir(C, n - 1)
        H1 = _yh_kaydir(_yh_roll(H, h, "max"), n - h)               # ilk yarı [e-n+1, e-n+h]
        H2 = _yh_roll(H, n - h, "max")                              # ikinci yarı [e-n+h+1, e]
        yuk = _yh_kaydir(C, n) / _yh_kaydir(mnC60, n) - 1           # C[e-n] / min C[e-n-59 .. e-n] - 1
        with np.errstate(invalid="ignore", divide="ignore"):
            ok = (mxH / mnL - 1 <= Y["bant"]) & (np.abs(C / cbas - 1) <= Y["net"]) & (H2 <= H1 * (1 + Y["tavanTol"])) & (yuk >= Y["yuk"])
        yeni = ok & (sec_n == 0)
        sec_n[yeni] = n; sec_dip[yeni] = mnL[yeni]; sec_tav[yeni] = mxH[yeni]
    kg = Y["konum_gun"]
    mx = _yh_roll(C, kg, "max"); mn = _yh_roll(C, kg, "min")
    with np.errstate(invalid="ignore", divide="ignore"):
        konum = np.where(mx > mn, (C - mn) / (mx - mn), np.nan)
        zon = (sec_n > 0) & (konum >= Y["konum"])                   # e günü (t-1)
    zon_t = np.r_[False, zon[:-1]]
    dip_t = _yh_kaydir(sec_dip, 1); tav_t = _yh_kaydir(sec_tav, 1); n_t = _yh_kaydir(sec_n.astype(float), 1)
    with np.errstate(invalid="ignore"):
        sat = zon_t & (C < dip_t * Y["sat"])
    g = np.flatnonzero(sat & np.isfinite(tav_t) & (tav_t > 0))
    if not len(g):
        return _yh_bos()
    return pd.DataFrame({"tarih": d.index[g], "hat": dip_t[g], "stop0": tav_t[g] * Y["stop"], "yon": -1, "n": n_t[g], "tavan": tav_t[g],
                         "ek": [f"konum={konum[i - 1]:.2f}" for i in g]})


def yh_y2_hat(df: pd.DataFrame, tarihler: List[pd.Timestamp]) -> np.ndarray:
    """Y2 hattı: FITIL_V2.fv_olcu HAT (t dahil son 10 geçerli bar min Low)."""
    import FITIL_V2 as FV   # kütüphane olarak; kendi çakışma kapısını taşır
    M = FV.fv_olcu(_yh_hazir(df))
    return np.array([float(M.HAT.get(pd.Timestamp(t), np.nan)) for t in tarihler], float)


# ---------------------------------------------------------------- 1b) 2. TUR ŞARTLARI (saf yardımcılar; birim testli)
_Y6_BAYRAK = ["f_hat", "f_kir", "f_stop", "f_buyuk", "dokunus", "buyuk_egim", "kir250"]
_Y7_BAYRAK = ["f_kenar", "f_mum", "f_dok", "f_stop", "dokunus", "mum_atr"]


def yh_dokunus(Lz: np.ndarray, hat: float, bant: float, egim: float) -> Tuple[int, bool]:
    """E2 hat netliği: bölge Low'larında Low <= hat x (1 + bant) olan bar sayısı; eğim şartı: son dokunuş Low >= ilk dokunuş Low x egim.
    Döner (dokunuş sayısı, eğim şartı tuttu mu); dokunuş yoksa (0, False)."""
    Lz = np.asarray(Lz, float)
    if not (np.isfinite(hat) and hat > 0) or not len(Lz):
        return 0, False
    t = np.flatnonzero(Lz <= hat * (1 + bant))
    if not len(t):
        return 0, False
    return int(len(t)), bool(Lz[t[-1]] >= Lz[t[0]] * egim)


def yh_buyuk_egim(Lb: np.ndarray, parca: int) -> float:
    """E1 büyük desen: Lb = [t-G, t-1] Low'ları (G = parça x parça boyu). Ardışık parçaların min Low'larına doğru (x = 0..k-1);
    eğim = uyum(k-1) / uyum(0) - 1; uyum(0) <= 0 ya da eksik veri -> -inf (şart tutmaz)."""
    Lb = np.asarray(Lb, float)
    if len(Lb) % parca or len(Lb) < 2 * parca or not np.isfinite(Lb).all():
        return -np.inf
    m = Lb.reshape(-1, parca).min(1); x = np.arange(len(m), dtype=float)
    b, a = np.polyfit(x, m, 1)
    y0, y1 = a, a + b * (len(m) - 1)
    return float(y1 / y0 - 1) if y0 > 0 else -np.inf


def yh_iki_kenar(Lw: np.ndarray, kenar: float) -> Tuple[bool, float, float, float]:
    """E4 iki kenar: W üçte birleri (ilk W[:n//3], orta W[n//3:2n//3], son W[2n//3:]); ilk ve son dipleri >= orta dip x kenar."""
    Lw = np.asarray(Lw, float); n = len(Lw)
    if n < 3:
        return False, np.nan, np.nan, np.nan
    a, b = n // 3, 2 * n // 3
    i_, o_, s_ = float(Lw[:a].min()), float(Lw[a:b].min()), float(Lw[b:].min())
    return bool(i_ >= o_ * kenar and s_ >= o_ * kenar), i_, o_, s_


def _yh_trp(H: np.ndarray, L: np.ndarray, C: np.ndarray) -> np.ndarray:
    """TR / C_önceki (S6 ATR birimi); ilk bar NaN."""
    Cp = np.r_[np.nan, C[:-1]]
    with np.errstate(invalid="ignore", divide="ignore"):
        tr = (np.fmax(H, Cp) - np.fmin(L, Cp)) / Cp
    tr[0] = np.nan
    return tr


def yh_y6_bayrak(df: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Y1 sinyalleri + Y6 şart bayrakları (a hat net, b gerçek kırılım, c stop <= %10 ön eleme, d büyük desen) + kir250 (Y8 hafızası).
    Yalnız t ve öncesi. Y6 = dört bayrak; Y8 = Y6 ve kir250 = 0; Y8B = Y6 ve kir250 > 0."""
    X1, _ = yh_s6_hisse(df, E)
    kol = list(X1.columns) + _Y6_BAYRAK
    if not len(X1):
        return pd.DataFrame(columns=kol)
    Y = E["denemeler"]["Y6"]; G8 = E["denemeler"]["Y8"]["gun"]
    d = _yh_hazir(df); T = S6.s6_taban(d, None)
    L, H, C = d.Low.to_numpy(float), d.High.to_numpy(float), d.Close.to_numpy(float)
    durum = T["durum"].to_numpy(object); sol_al = T["kutu_sol_i"].to_numpy(float); bas = T["bas_i"].to_numpy(float)
    KIRb = np.flatnonzero(durum == "KIRILDI")
    pos = d.index.get_indexer(pd.to_datetime(X1.tarih))
    if (pos < 0).any():
        raise YHHata("Y6: Y1 sinyal günü veride yok")
    G = int(Y["buyuk_gun"]); fh, fk, fs, fb, dk, eg, kr, ekl = [], [], [], [], [], [], [], []
    for q, i in enumerate(pos):
        hat = float(X1.hat.iat[q]); tav = float(X1.tavan.iat[q])
        sol = sol_al[i] if durum[i] == "AL" else (bas[i - 1] if i >= 1 else np.nan)
        if np.isfinite(sol) and 0 <= int(sol) < i:
            z = slice(int(sol), i)
            n_dok, egim_ok = yh_dokunus(L[z], hat, Y["hat_bant"], Y["dokunus_egim"])
            med = float(np.median(H[z] - L[z]))
        else:
            n_dok, egim_ok, med = 0, False, np.inf
        a_ = bool(n_dok >= Y["dokunus_min"] and egim_ok)
        b_ = bool(np.isfinite(tav) and C[i] > tav * (1 + Y["kir_pay"]) and (H[i] - L[i]) >= med)
        c_ = bool(np.isfinite(hat) and hat > 0 and C[i] / hat - 1 <= Y["stop_uzak"])
        if i >= G:
            e_ = yh_buyuk_egim(L[i - G:i], int(Y["buyuk_parca"])); d_ = bool(e_ >= Y["buyuk_egim"]); bd = f"{e_:.3f}"
        else:
            e_ = np.nan; d_ = True; bd = "NA"
        k_ = int(((KIRb >= i - G8) & (KIRb <= i - 1)).sum())
        fh.append(a_); fk.append(b_); fs.append(c_); fb.append(d_); dk.append(n_dok); eg.append(e_); kr.append(k_)
        ekl.append(f"{X1.ek.iat[q]};dok={n_dok};buyuk_desen={bd};kir250={k_}")
    Z = X1.copy()
    Z["f_hat"], Z["f_kir"], Z["f_stop"], Z["f_buyuk"] = fh, fk, fs, fb
    Z["dokunus"], Z["buyuk_egim"], Z["kir250"] = dk, eg, kr
    Z["ek"] = ekl
    return Z


def yh_y7_bayrak(df: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Y3 sinyalleri + Y7 şart bayrakları (a iki kenar, b dipte küçük mum, c dip savunması, d stop <= %10 ön eleme), Y3'ün seçtiği W üzerinde."""
    X3 = yh_y3_hisse(df, E)
    kol = list(X3.columns) + _Y7_BAYRAK
    if not len(X3):
        return pd.DataFrame(columns=kol)
    Y = E["denemeler"]["Y7"]; d = _yh_hazir(df)
    L, H, C = d.Low.to_numpy(float), d.High.to_numpy(float), d.Close.to_numpy(float)
    trp = _yh_trp(H, L, C)
    with np.errstate(invalid="ignore", divide="ignore"):
        mum = (H - L) / C
    pos = d.index.get_indexer(pd.to_datetime(X3.tarih))
    if (pos < 0).any():
        raise YHHata("Y7: Y3 sinyal günü veride yok")
    fk, fm, fd, fs, dk, ma, ekl = [], [], [], [], [], [], []
    for q, i in enumerate(pos):
        n = int(X3.n.iat[q]); hat = float(X3.hat.iat[q]); w0 = i - n
        Lw = L[w0:i]
        k_ok, i_, o_, s_ = yh_iki_kenar(Lw, Y["kenar"])
        a3, b3 = n // 3, 2 * n // 3
        m_ = float(np.median(mum[w0 + a3:w0 + b3]))
        cnt = min(int(Y["atr_gun"]), w0 - 1)
        atr = float(np.mean(trp[w0 - cnt:w0])) if cnt >= int(Y["atr_min"]) else np.nan
        m_ok = bool(np.isfinite(atr) and atr > 0 and m_ <= Y["mum_k"] * atr)
        n_dok = int((Lw <= hat * (1 + Y["dip_bant"])).sum())
        d_ok = bool(n_dok >= Y["dokunus_min"])
        s_ok = bool(np.isfinite(hat) and hat > 0 and C[i] / hat - 1 <= Y["stop_uzak"])
        fk.append(k_ok); fm.append(m_ok); fd.append(d_ok); fs.append(s_ok); dk.append(n_dok)
        ma.append(m_ / atr if np.isfinite(atr) and atr > 0 else np.nan)
        ekl.append(f"{X3.ek.iat[q]};kenar={i_ / o_ - 1:.3f}/{s_ / o_ - 1:.3f};mum_atr={ma[-1]:.2f};dok={n_dok}")
    Z = X3.copy()
    Z["f_kenar"], Z["f_mum"], Z["f_dok"], Z["f_stop"] = fk, fm, fd, fs
    Z["dokunus"], Z["mum_atr"] = dk, ma
    Z["ek"] = ekl
    return Z


def yh_tur2_sec(F: pd.DataFrame, deneme: str) -> pd.DataFrame:
    """Bayraklı çerçeveden deneme sinyalleri (Y6 / Y8 / Y8B: yh_y6_bayrak; Y7: yh_y7_bayrak)."""
    if not len(F):
        return F.reset_index(drop=True)
    if deneme == "Y7":
        m = F.f_kenar.astype(bool) & F.f_mum.astype(bool) & F.f_dok.astype(bool) & F.f_stop.astype(bool)
    else:
        m = F.f_hat.astype(bool) & F.f_kir.astype(bool) & F.f_stop.astype(bool) & F.f_buyuk.astype(bool)
        if deneme == "Y8":
            m &= F.kir250.astype(int) == 0
        elif deneme == "Y8B":
            m &= F.kir250.astype(int) > 0
        elif deneme != "Y6":
            raise YHHata(f"2. tur deneme değil: {deneme}")
    return F[m.to_numpy(bool)].reset_index(drop=True)


def yh_hisse_sinyal(df: pd.DataFrame, deneme: str, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Tek hisse, tek deneme (Y2 hariç; Y2 olay dosyasından). Y9*: OC tekilleştirmesiz, özellikler yeniden hesaplanır (yh_y9_hisse)."""
    if deneme in YH_DENEMELER_3:
        return yh_y9_hisse(df, deneme, E)
    if deneme in ("Y6", "Y8", "Y8B"):
        return yh_tur2_sec(yh_y6_bayrak(df, E), deneme)
    if deneme == "Y7":
        return yh_tur2_sec(yh_y7_bayrak(df, E), deneme)
    if deneme in ("Y1", "Y4"):
        X1, X4 = yh_s6_hisse(df, E)
        return X1 if deneme == "Y1" else X4
    if deneme == "Y3":
        return yh_y3_hisse(df, E)
    if deneme == "Y5":
        return yh_y5_hisse(df, E)
    raise YHHata(f"hisse sinyali yok: {deneme}")


_YH_IS_V: Dict[str, pd.DataFrame] = {}


def _yh_sinyal_isci(is_: Tuple[List[str], Tuple[str, ...]]) -> Dict[str, List[pd.DataFrame]]:
    semboller, den = is_
    out: Dict[str, List[pd.DataFrame]] = {k: [] for k in den}
    for s in semboller:
        df = _YH_IS_V[s]
        try:
            if "Y1" in den or "Y4" in den:
                X1, X4 = yh_s6_hisse(df)
                for k, X in (("Y1", X1), ("Y4", X4)):
                    if k in den and len(X):
                        X = X.copy(); X.insert(0, "sembol", s); out[k].append(X)
            for k, f in (("Y3", yh_y3_hisse), ("Y5", yh_y5_hisse)):
                if k in den:
                    X = f(df)
                    if len(X):
                        X = X.copy(); X.insert(0, "sembol", s); out[k].append(X)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (sayımda log)
            yhlog.warning("sinyal %s atlandı: %s", s, ex)
    return out


def _yh_sinyal_isci2(is_: Tuple[List[str], Tuple[str, ...]]) -> Dict[str, List[pd.DataFrame]]:
    """2. tur işçisi: bayraklı çerçeveler (_Y6F: Y1 + Y6 bayrakları, _Y7F: Y3 + Y7 bayrakları)."""
    semboller, den = is_
    out: Dict[str, List[pd.DataFrame]] = {"_Y6F": [], "_Y7F": []}
    for s in semboller:
        df = _YH_IS_V[s]
        try:
            for k, f, gerek in (("_Y6F", yh_y6_bayrak, ("Y6", "Y8", "Y8B")), ("_Y7F", yh_y7_bayrak, ("Y7",))):
                if any(x in den for x in gerek):
                    X = f(df)
                    if len(X):
                        X = X.copy(); X.insert(0, "sembol", s); out[k].append(X)
        except Exception as ex:   # tek hisse bozuksa öteki hisseler sürer (sayımda log)
            yhlog.warning("sinyal (2. tur) %s atlandı: %s", s, ex)
    return out


def yh_sinyaller2(Vd: Dict[str, Any], pazar: str, denemeler: List[str], islem: int = 1, E: Dict[str, Any] = YH_ESIK) -> Dict[str, pd.DataFrame]:
    """2. tur: deneme sinyalleri + bayraklı çerçeveler '_Y6F' / '_Y7F' (huni için)."""
    global _YH_IS_V
    den = tuple(k for k in denemeler if k in YH_DENEMELER_2)
    if len(den) != len(denemeler):
        raise YHHata(f"yh_sinyaller2 yalnız 2. tur: {denemeler}")
    _YH_IS_V = Vd["V"]
    S = sorted(_YH_IS_V); parca = [S[i::max(1, islem * 4)] for i in range(max(1, islem * 4))]
    isler = [(p, den) for p in parca if p]
    try:
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as havuz:
                R = havuz.map(_yh_sinyal_isci2, isler)
        else:
            R = [_yh_sinyal_isci2(i) for i in isler]
    finally:
        _YH_IS_V = {}
    out: Dict[str, pd.DataFrame] = {}
    for k, kol in (("_Y6F", _Y6_BAYRAK), ("_Y7F", _Y7_BAYRAK)):
        parcalar = [x for r in R for x in r[k]]
        X = pd.concat(parcalar, ignore_index=True) if parcalar else pd.DataFrame(columns=["sembol"] + _SIG_KOL + kol)
        X["pazar"] = pazar
        out[k] = X.sort_values(["sembol", "tarih"]).reset_index(drop=True)
    for k in den:
        F = out["_Y7F"] if k == "Y7" else out["_Y6F"]
        out[k] = yh_tur2_sec(F, k)
    return out


def yh_sinyaller(Vd: Dict[str, Any], pazar: str, denemeler: List[str], islem: int = 1, E: Dict[str, Any] = YH_ESIK) -> Dict[str, pd.DataFrame]:
    """oc_veri -> deneme -> DataFrame[sembol, tarih, pazar, hat, stop0, yon, n, tavan, ek]. 2. tur denemeleri yh_sinyaller2'ye gider
    (çıktıda ayrıca '_Y6F' / '_Y7F' bayraklı çerçeveler)."""
    global _YH_IS_V
    den2 = [k for k in denemeler if k in YH_DENEMELER_2]
    if den2:
        kalan = [k for k in denemeler if k not in YH_DENEMELER_2]
        return {**(yh_sinyaller(Vd, pazar, kalan, islem, E) if kalan else {}), **yh_sinyaller2(Vd, pazar, den2, islem, E)}
    V = Vd["V"]; den = tuple(k for k in denemeler if k != "Y2")
    out: Dict[str, pd.DataFrame] = {}
    if den:
        _YH_IS_V = V
        S = sorted(V); parca = [S[i::max(1, islem * 4)] for i in range(max(1, islem * 4))]
        isler = [(p, den) for p in parca if p]
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as havuz:
                R = havuz.map(_yh_sinyal_isci, isler)
        else:
            R = [_yh_sinyal_isci(i) for i in isler]
        _YH_IS_V = {}
        for k in den:
            parcalar = [x for r in R for x in r[k]]
            X = pd.concat(parcalar, ignore_index=True) if parcalar else pd.DataFrame(columns=["sembol"] + _SIG_KOL)
            X["pazar"] = pazar
            out[k] = X.sort_values(["sembol", "tarih"]).reset_index(drop=True)
    if "Y2" in denemeler:
        out["Y2"] = yh_y2_sinyal(Vd, pazar)
    return out


def yh_y2_sinyal(Vd: Dict[str, Any], pazar: str, yol: Optional[str] = None) -> pd.DataFrame:
    yol = yol or YH_YOL["y2_olay"]
    if not os.path.exists(yol):
        raise YHHata(f"Y2 olay dosyası yok: {yol}")
    O = pd.read_csv(yol, parse_dates=["tarih", "giris"])
    O = O[O.pazar == pazar]
    sat = []
    for s, g in O.groupby("sembol"):
        if s not in Vd["V"]:
            continue
        hat = yh_y2_hat(Vd["V"][s], list(g.tarih))
        sat.append(pd.DataFrame({"sembol": s, "tarih": g.tarih.to_numpy(), "hat": hat, "stop0": hat * YH_ESIK["olcu"]["stop0"]["hat_carpan"],
                                 "yon": 1, "n": 10.0, "tavan": np.nan, "ek": "", "giris_dosya": g.giris.to_numpy()}))
    X = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame(columns=["sembol"] + _SIG_KOL + ["giris_dosya"])
    X["pazar"] = pazar
    return X.sort_values(["sembol", "tarih"]).reset_index(drop=True)


# ================================================================ 2) ÖLÇÜM ÇEKİRDEĞİ (olay, eş, taban, plasebo AYNI fonksiyon)
def _yh_sec(a: np.ndarray, b: np.ndarray, s: int) -> np.ndarray:
    """Yön s için stop'u 'sıkılaştıran' seçim: s = +1 max, s = -1 min."""
    return s * np.maximum(s * a, s * b)


def yh_sim(Cr: np.ndarray, Hr: np.ndarray, Lr: np.ndarray, E0: np.ndarray, stop0: np.ndarray, yon: int,
           Y: Dict[str, Any] = YH_ESIK) -> Dict[str, np.ndarray]:
    """Cr/Hr/Lr: (R, K) satır 0 = giriş günü (birleşik takvim; NaN = o hisse o gün geçerli bar yok). E0: giriş açılışı (K), stop0 (K).
    Döner: olc (15 bar ölçülebilir), h5, h10, st5, h5H, h10H (float 0/1, ölçülemeyen NaN), k5, kst (bar sırası; -1 yok)."""
    O = Y["olcu"]; St = O["stop"]; u = int(O["ufuk"]); s = int(yon)
    h5, h10 = O["hedef"]
    Cr = np.asarray(Cr, float); R, K = Cr.shape
    E0 = np.asarray(E0, float); stop = np.asarray(stop0, float).copy()
    valid = np.isfinite(Cr)
    olc = (valid.sum(0) >= u) & np.isfinite(E0) & (E0 > 0) & valid[0] & np.isfinite(stop)
    with np.errstate(invalid="ignore"):
        olc &= (s * (E0 - stop) > 0)
    T5 = E0 * (1 + s * h5); T10 = E0 * (1 + s * h10)
    K5 = E0 * (1 + s * St["kilit5"]); K10 = E0 * (1 + s * St["kilit10"])
    X = Hr if s > 0 else Lr
    k5 = np.full(K, -1); k10 = np.full(K, -1); kst = np.full(K, -1); k5H = np.full(K, -1); k10H = np.full(K, -1)
    ext = np.full(K, -np.inf); cnt = np.zeros(K, int); bitti = ~olc.copy()
    with np.errstate(invalid="ignore"):
        for r in range(R):
            v = valid[r] & ~bitti & (cnt < u)
            if v.any():
                c = Cr[r]
                st = v & (s * (c - stop) < 0)
                kst[st] = cnt[st]; bitti |= st
                g = v & ~st
                x = g & (k5 < 0) & (s * (c - T5) >= 0); k5[x] = cnt[x]
                x = g & (k10 < 0) & (s * (c - T10) >= 0); k10[x] = cnt[x]
                xx = np.asarray(X[r], float)
                x = g & (k5H < 0) & (s * (xx - T5) >= 0); k5H[x] = cnt[x]
                x = g & (k10H < 0) & (s * (xx - T10) >= 0); k10H[x] = cnt[x]
                lvl = np.where(g & (k5 >= 0), _yh_sec(stop, K5, s), stop)
                lvl = np.where(g & (k10 >= 0), _yh_sec(lvl, K10, s), lvl)
                ext = np.where(g, np.maximum(ext, s * c), ext)
                trail = (s * ext) * (1 - s * St["takip"])
                stop = np.where(g, _yh_sec(lvl, trail, s), stop)
            cnt += valid[r]
            if ((cnt >= u) | bitti).all():
                break

    def g_(b: np.ndarray) -> np.ndarray:
        return np.where(olc, b.astype(float), np.nan)
    return {"olc": olc, "h5": g_(k5 >= 0), "h10": g_(k10 >= 0), "st5": g_((kst >= 0) & (k5 < 0)), "h5H": g_(k5H >= 0), "h10H": g_(k10H >= 0),
            "k5": k5, "kst": kst}


def yh_getiri(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, gi: int, E0: float, stop0: float, yon: int,
              Y: Dict[str, Any] = YH_ESIK) -> Tuple[float, int, str]:
    """Takip stoplu getiri (bilgi): hissenin geçerli barları, giriş barı gi. Döner (getiri, çıkış barı (gi'ye göre), tür)."""
    O_ = Y["olcu"]; St = O_["stop"]; B = O_["cikis_bilgi"]; s = int(yon); N = len(C)
    if not (np.isfinite(E0) and E0 > 0 and np.isfinite(stop0)) or s * (E0 - stop0) <= 0:
        return np.nan, -1, "olculmez"
    stop = stop0; ext = -np.inf; g5 = g10 = False
    T5 = E0 * (1 + s * O_["hedef"][0]); T10 = E0 * (1 + s * O_["hedef"][1]); tn = B["ters_n"]
    for k in range(B["zaman_tavani"]):
        i = gi + k
        if i >= N:
            if k == 0:
                return np.nan, -1, "olculmez"
            return s * (C[i - 1] / E0 - 1), k - 1, "kesik"
        c = C[i]
        if s * (c - stop) < 0:
            if i + 1 < N:
                return s * (O[i + 1] / E0 - 1), k + 1, "stop"
            return s * (c / E0 - 1), k, "stop_kesik"
        if k >= tn:
            hh = float(np.max(H[i - tn:i])); ll = float(np.min(L[i - tn:i]))
            seviye = ll * (1 - B["ters_kir"]) if s > 0 else hh * (1 + B["ters_kir"])
            if hh / ll - 1 <= B["ters_bant"] and s * (c - seviye) < 0:
                if i + 1 < N:
                    return s * (O[i + 1] / E0 - 1), k + 1, "ters"
                return s * (c / E0 - 1), k, "ters_kesik"
        if s * (c - T5) >= 0:
            g5 = True
        if s * (c - T10) >= 0:
            g10 = True
        if g5:
            stop = float(_yh_sec(np.array(stop), np.array(E0 * (1 + s * St["kilit5"])), s))
        if g10:
            stop = float(_yh_sec(np.array(stop), np.array(E0 * (1 + s * St["kilit10"])), s))
        ext = max(ext, s * c)
        stop = float(_yh_sec(np.array(stop), np.array((s * ext) * (1 - s * St["takip"])), s))
    i = gi + B["zaman_tavani"] - 1
    return s * (C[i] / E0 - 1), B["zaman_tavani"] - 1, "zaman"


def yh_kapanis(P: Dict[str, Any], Vd: Dict[str, Any]) -> np.ndarray:
    """Panel takviminde Close tablosu (oc_panel Close döndürmez)."""
    V = Vd["V"]
    return pd.DataFrame({s: V[s]["Close"] for s in P["sembol"]}).reindex(P["tarih"]).to_numpy(float)


def _yh_pencere(A: np.ndarray, d: int, R: int, cols: Optional[np.ndarray] = None) -> np.ndarray:
    x = A[d:d + R] if cols is None else A[d:d + R][:, cols]
    if x.shape[0] < R:
        x = np.vstack([x, np.full((R - x.shape[0], x.shape[1]), np.nan)])
    return x


_YH_IS_P: Dict[str, Any] = {}


def _yh_olay_isci(is_: Tuple[pd.DataFrame, int, int]) -> pd.DataFrame:
    X, dno, pno = is_
    return yh_olay_olc(_YH_IS_P["P"], _YH_IS_P["Cl"], _YH_IS_P["Vd"], X, dno, pno)


def yh_olay_olc(P: Dict[str, Any], Cl: np.ndarray, Vd: Dict[str, Any], X: pd.DataFrame, dno: int, pno: int,
                Y: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """X: oc_olay_hazirla çıktısı + stop0, yon. Her olay: olay göstergeleri, eş / taban oranları (aynı d), plasebo, takip stoplu getiri."""
    O = Y["olcu"]; R = int(O["pencere_azami"]); Kc = Y["kontrol"]; me = Kc["min_es"]
    Op, Hi, Lo, Hc, ok = P["Op"], P["Hi"], P["Lo"], P["H"], P["ok"]
    idx = P["tarih"]; dn = OC._oc_donem(pd.Series(idx), OC.OC_ESIK)
    kol = ["dd", "E0", "olc", "h5", "h10", "st5", "h5H", "h10H", "k5", "kst", "es_h5", "es_h10", "es_st5", "es_h5H", "es_h10H", "n_es",
           "tb_h5", "tb_h10", "tb_st5", "n_tb", "pl_d", "pl_h5", "pl_h10", "pl_st5", "getiri", "cikis_bar", "cikis_tur"]
    out = {k: [] for k in kol}
    V = Vd["V"]; aday_onb: Dict[int, np.ndarray] = {}
    for r in X.itertuples(index=False):
        d, j, s = int(r.d), int(r.j), int(r.yon)
        E0 = float(Op[d, j]); st0 = float(r.stop0)
        dd = s * (1 - st0 / E0) if (np.isfinite(E0) and E0 > 0 and np.isfinite(st0)) else np.nan
        sat = dict.fromkeys(kol, np.nan); sat["dd"] = dd; sat["E0"] = E0; sat["olc"] = False; sat["cikis_tur"] = ""
        if not (np.isfinite(dd) and dd > 0):
            sat["cikis_tur"] = "giris_stop_otesi"
            for k in kol:
                out[k].append(sat[k])
            continue
        havuz = np.flatnonzero(ok[d])
        if not ok[d, j]:            # oc_olay_hazirla havuz üyeliğini zaten şart koşar; savunma
            havuz = np.r_[havuz, j]
        Ek = Op[d, havuz]; stk = Ek * (1 - s * dd)
        stk[havuz == j] = st0
        Sm = yh_sim(_yh_pencere(Cl, d, R, havuz), _yh_pencere(Hi, d, R, havuz), _yh_pencere(Lo, d, R, havuz), Ek, stk, s, Y)
        pj = int(np.flatnonzero(havuz == j)[0])
        sat["olc"] = bool(Sm["olc"][pj])
        if sat["olc"]:
            for k in ("h5", "h10", "st5", "h5H", "h10H"):
                sat[k] = float(Sm[k][pj])
            sat["k5"] = int(Sm["k5"][pj]); sat["kst"] = int(Sm["kst"][pj])
        diger = Sm["olc"].copy(); diger[pj] = False
        es = diger & (Hc[d, havuz] == Hc[d, j])
        sat["n_es"] = int(es.sum()); sat["n_tb"] = int(diger.sum())
        if es.sum() >= me:
            for k in ("h5", "h10", "st5", "h5H", "h10H"):
                sat["es_" + k] = float(np.mean(Sm[k][es]))
        if diger.sum() >= me:
            for k in ("h5", "h10", "st5"):
                sat["tb_" + k] = float(np.mean(Sm[k][diger]))
        # plasebo: aynı hisse, aynı dönem, havuzda, rastgele gün
        donem = dn[d]
        if donem and sat["olc"]:
            if j not in aday_onb:
                aday_onb[j] = np.flatnonzero(ok[:, j])
            ad = aday_onb[j]; ad = ad[(dn[ad] == donem) & (ad != d)]
            rng = np.random.default_rng([Kc["plasebo_tohum"], dno, pno, d, j])
            for _ in range(Kc["plasebo_deneme"]):
                if not len(ad):
                    break
                dp = int(ad[rng.integers(len(ad))])
                Ep = float(Op[dp, j])
                Sp = yh_sim(_yh_pencere(Cl, dp, R, np.array([j])), _yh_pencere(Hi, dp, R, np.array([j])), _yh_pencere(Lo, dp, R, np.array([j])),
                            np.array([Ep]), np.array([Ep * (1 - s * dd)]), s, Y)
                if Sp["olc"][0]:
                    sat["pl_d"] = dp
                    for k in ("h5", "h10", "st5"):
                        sat["pl_" + k] = float(Sp[k][0])
                    break
        # takip stoplu getiri (bilgi, hissenin kendi geçerli barları)
        sym = P["sembol"][j]; df = V[sym]
        try:
            gi = int(df.index.get_loc(idx[d]))
            g_, b_, t_ = yh_getiri(df.Open.to_numpy(float), df.High.to_numpy(float), df.Low.to_numpy(float), df.Close.to_numpy(float), gi, E0, st0, s, Y)
        except KeyError:
            g_, b_, t_ = np.nan, -1, "olculmez"
        sat["getiri"] = g_; sat["cikis_bar"] = b_; sat["cikis_tur"] = t_
        for k in kol:
            out[k].append(sat[k])
    Z = X.copy()
    for k in kol:
        Z[k] = out[k]
    return Z


def yh_olc_pazar(Vd: Dict[str, Any], P: Dict[str, Any], Cl: np.ndarray, sig: pd.DataFrame, deneme: str, pazar: str,
                 islem: int = 1, Y: Dict[str, Any] = YH_ESIK) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Sinyaller -> OC olay hazırlığı (giriş, havuz, tekil) -> ölçüm. Döner (olay satırları, sayım)."""
    global _YH_IS_P
    if not len(sig):
        return pd.DataFrame(), {"girdi": 0}
    sig = sig.copy(); sig["tarih"] = pd.to_datetime(sig.tarih)
    if sig.duplicated(["sembol", "tarih"]).any():
        raise YHHata(f"{deneme} {pazar}: aynı sembol-gün iki kez")
    X, say = OC.oc_olay_hazirla(sig[["sembol", "tarih", "pazar"]], P)
    if not len(X):
        return pd.DataFrame(), say
    ek_kol = [c for c in ["hat", "stop0", "yon", "n", "tavan", "ek", "hafiza", "giris_dosya"] if c in sig.columns]
    X = X.merge(sig[["sembol", "tarih"] + ek_kol], on=["sembol", "tarih"], how="left", validate="one_to_one")
    if "giris_dosya" in X:
        say["y2_giris_farkli"] = int((pd.to_datetime(X.giris_dosya) != pd.to_datetime(X.giris)).sum())
    su = Y["denemeler"].get(deneme, {}).get("stop_uzak")
    if su is not None:          # 2. tur E5a: gerçek giriş (t+1 açılış) / hat - 1 <= stop_uzak; aşan ölçülmez (karar giriş anında bilinir)
        E0x = P["Op"][X.d.to_numpy(int), X.j.to_numpy(int)]; hx = X.hat.to_numpy(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            uz = ~(E0x / hx - 1 <= float(su))
        say["stop_uzak"] = int(uz.sum()); X = X[~uz].reset_index(drop=True)
        if not len(X):
            return pd.DataFrame(), say
    dno = YH_DENEMELER_HEPSI.index(deneme) + 1; pno = OC.OC_ESIK["pazar"].index(pazar) + 1
    if islem > 1 and len(X) > 200:
        import multiprocessing as mp
        _YH_IS_P = {"P": P, "Cl": Cl, "Vd": Vd}
        parca = np.array_split(np.arange(len(X)), islem * 4)
        with mp.get_context("fork").Pool(islem) as havuz:
            R_ = havuz.map(_yh_olay_isci, [(X.iloc[p], dno, pno) for p in parca if len(p)])
        _YH_IS_P = {}
        Z = pd.concat(R_, ignore_index=True)
    else:
        Z = yh_olay_olc(P, Cl, Vd, X, dno, pno, Y)
    say["giris_stop_otesi"] = int((Z.cikis_tur == "giris_stop_otesi").sum())
    say["olc15_yok"] = int(((~Z.olc.astype(bool)) & (Z.cikis_tur != "giris_stop_otesi")).sum())
    say["es_az"] = int((Z.olc.astype(bool) & Z.es_h5.isna()).sum())
    say["plasebo_yok"] = int((Z.olc.astype(bool) & Z.pl_h5.isna()).sum())
    Z.insert(0, "pazar", pazar); Z.insert(0, "deneme", deneme)
    return Z, say


def yh_e5b_olc(P: Dict[str, Any], Cl: np.ndarray, Z: pd.DataFrame, Y: Dict[str, Any] = YH_ESIK, carp: Optional[Dict[str, float]] = None) -> pd.DataFrame:
    """BİLGİ (E5b, karar değil): stop0b = max(hat x 0,98, giriş x 0,95); olay ve eşler (aynı gün, aynı kova, aynı d_b) AYNI yh_sim kuralıyla.
    Z: yh_olay_olc çıktısı (hat, d, j, yon, E0). Ekler: b_dd, b_h5, b_h10, b_st5, b_es_h5, b_es_h10, b_es_st5, b_n_es."""
    carp = carp or {"hat_carpan": 0.98, "giris_carpan": 0.95}
    R = int(Y["olcu"]["pencere_azami"]); me = Y["kontrol"]["min_es"]
    Op, Hi, Lo, Hc, ok = P["Op"], P["Hi"], P["Lo"], P["H"], P["ok"]
    kol = ["b_dd", "b_h5", "b_h10", "b_st5", "b_es_h5", "b_es_h10", "b_es_st5", "b_n_es"]
    out = {k: [] for k in kol}
    for r in Z.itertuples(index=False):
        sat = dict.fromkeys(kol, np.nan)
        d, j, s = int(r.d), int(r.j), int(r.yon); E0 = float(r.E0); hat = float(r.hat)
        if bool(r.olc) and s == 1 and np.isfinite(E0) and E0 > 0 and np.isfinite(hat) and hat > 0:
            st0 = max(hat * carp["hat_carpan"], E0 * carp["giris_carpan"]); db = 1 - st0 / E0
            if db > 0:
                havuz = np.flatnonzero(ok[d])
                if not ok[d, j]:
                    havuz = np.r_[havuz, j]
                Ek = Op[d, havuz]; stk = Ek * (1 - db); stk[havuz == j] = st0
                Sm = yh_sim(_yh_pencere(Cl, d, R, havuz), _yh_pencere(Hi, d, R, havuz), _yh_pencere(Lo, d, R, havuz), Ek, stk, s, Y)
                pj = int(np.flatnonzero(havuz == j)[0]); sat["b_dd"] = db
                if Sm["olc"][pj]:
                    for k in ("h5", "h10", "st5"):
                        sat["b_" + k] = float(Sm[k][pj])
                es = Sm["olc"].copy(); es[pj] = False; es &= (Hc[d, havuz] == Hc[d, j]); sat["b_n_es"] = int(es.sum())
                if es.sum() >= me:
                    for k in ("h5", "h10", "st5"):
                        sat["b_es_" + k] = float(np.mean(Sm[k][es]))
        for k in kol:
            out[k].append(sat[k])
    Z = Z.copy()
    for k in kol:
        Z[k] = out[k]
    return Z


# ================================================================ 3) HÜCRE, KAT, ETİKET
def yh_kat(olay: np.ndarray, oran: np.ndarray, ay: np.ndarray, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, float]:
    """KAT = Σ olay / Σ oran; ay kümeli bootstrap (OC.oc_kat ile aynı algoritma ve rastgele sıra) + p = P(bootstrap KAT <= 1)."""
    Kt = Y["kat"]; olay = np.asarray(olay, float); oran = np.asarray(oran, float); ay = np.asarray(ay)
    g = np.isfinite(olay) & np.isfinite(oran)
    a, b, m = olay[g], oran[g], ay[g]
    out = {"n": int(g.sum()), "p_olay": float(a.mean()) if len(a) else np.nan, "p_ref": float(b.mean()) if len(b) else np.nan,
           "kat": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}
    if not len(a) or b.sum() <= 0:
        return out
    out["kat"] = float(a.sum() / b.sum())
    aylar = np.unique(m); ga = {x: a[m == x].sum() for x in aylar}; gb = {x: b[m == x].sum() for x in aylar}
    rng = np.random.default_rng(Kt["tohum"]); v = []
    for _ in range(Kt["bootstrap"]):
        sec = rng.choice(aylar, len(aylar), replace=True)
        pa = sum(ga[x] for x in sec); pb = sum(gb[x] for x in sec)
        v.append(pa / pb if pb > 0 else np.nan)
    v = np.array(v, float); v = v[np.isfinite(v)]
    if len(v):
        out["alt"] = float(np.quantile(v, Kt["guven"][0])); out["ust"] = float(np.quantile(v, Kt["guven"][1])); out["p"] = float((v <= 1).mean())
    return out


def yh_hucre(X: pd.DataFrame, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Bir hücrenin olay satırları -> KAT'lar, paylar, plasebo, karar şartları, bilgi (High, iki yarı, getiri)."""
    if not len(X):
        return {"n": 0, "tutar": False}
    g = X[X.h5.notna() & X.es_h5.notna()].sort_values("giris")
    ay = pd.to_datetime(g.giris).dt.to_period("M").astype(str).to_numpy() if len(g) else np.array([], dtype=object)
    out: Dict[str, Any] = {"n": int(len(g)), "n_ham": int(len(X)), "ay": int(len(np.unique(ay)))}
    for k in ("h5", "h10", "st5", "h5H", "h10H"):
        r = yh_kat(g[k].to_numpy(float), g["es_" + k].to_numpy(float), ay, Y)
        for a_, v in r.items():
            out[f"{k}_{a_}"] = v
    for k in ("h5", "h10", "st5"):
        r = yh_kat(g[k].to_numpy(float), g["tb_" + k].to_numpy(float), ay, Y)
        out[f"tb_{k}_p"] = r["p_ref"]; out[f"tb_{k}_kat"] = r["kat"]; out[f"tb_{k}_alt"] = r["alt"]; out[f"tb_{k}_ust"] = r["ust"]
    for k in ("h5", "h10", "st5"):
        r = yh_kat(g[k].to_numpy(float), g["pl_" + k].to_numpy(float), ay, Y)
        for a_, v in r.items():
            out[f"pl_{k}_{a_}"] = v
    yari = len(g) // 2
    for ad, x in (("yari1", g.iloc[:yari]), ("yari2", g.iloc[yari:])):
        out[f"{ad}_kat5"] = float(x.h5.sum() / x.es_h5.sum()) if len(x) and x.es_h5.sum() > 0 else np.nan
    gt = g.getiri.to_numpy(float); gt = gt[np.isfinite(gt)]
    out["getiri_ort"] = float(gt.mean()) if len(gt) else np.nan; out["getiri_med"] = float(np.median(gt)) if len(gt) else np.nan
    out["getiri_kazanan"] = float((gt > 0).mean()) if len(gt) else np.nan
    cb = g.cikis_bar.to_numpy(float); cb = cb[np.isfinite(cb) & (cb >= 0)]
    out["cikis_bar_ort"] = float(cb.mean()) if len(cb) else np.nan; out["cikis_bar_med"] = float(np.median(cb)) if len(cb) else np.nan
    out["cikis_tur"] = {str(k): int(v) for k, v in g.cikis_tur.value_counts().items()}
    out["dd_med"] = float(np.nanmedian(g.dd.to_numpy(float))) if len(g) else np.nan
    K = Y["karar"]
    out["s_n"] = bool(out["n"] >= K["n_esik"])
    out["s_kat"] = bool(np.isfinite(out.get("h5_alt", np.nan)) and out["h5_alt"] > 1)
    out["s_stop"] = bool(np.isfinite(out.get("st5_p_olay", np.nan)) and np.isfinite(out.get("st5_p_ref", np.nan)) and out["st5_p_olay"] < out["st5_p_ref"])
    out["s_plasebo"] = bool(np.isfinite(out.get("pl_h5_alt", np.nan)) and out["pl_h5_alt"] > 1)
    out["tutar"] = bool(out["s_n"] and out["s_kat"] and out["s_stop"] and out["s_plasebo"])
    return out


def yh_hucre_e5b(X: pd.DataFrame, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """BİLGİ: E5b stop varyantı hücre özeti (olay / eş, ay kümeli KAT)."""
    if not len(X) or "b_h5" not in X.columns:
        return {}
    g = X[X.b_h5.notna() & X.b_es_h5.notna()].sort_values("giris")
    ay = pd.to_datetime(g.giris).dt.to_period("M").astype(str).to_numpy() if len(g) else np.array([], dtype=object)
    out: Dict[str, Any] = {"b_n": int(len(g)), "b_dd_med": float(np.nanmedian(g.b_dd.to_numpy(float))) if len(g) else np.nan}
    for k in ("h5", "h10", "st5"):
        r = yh_kat(g["b_" + k].to_numpy(float), g["b_es_" + k].to_numpy(float), ay, Y)
        for a_, v in r.items():
            if a_ != "n":
                out[f"b_{k}_{a_}"] = v
    return out


def yh_guc_bak(n: int, yon: int, tablo: Optional[Dict[str, Any]], Y: Dict[str, Any] = YH_ESIK) -> float:
    """Güç: n'e küçük-eşit en büyük n satırı, KAT_ref 1,25, d ızgarasının en küçüğü (muhafazakâr). Tablo yok / n < 30 -> 0."""
    if not tablo or n < Y["karar"]["n_esik"]:
        return 0.0
    T = tablo.get("guc", {}).get(str(int(yon)), {})
    ns = sorted(int(k) for k in T if int(k) <= n)
    if not ns:
        return 0.0
    r = T[str(ns[-1])].get(f"{Y['etiket']['kat_ref']:.2f}", {})
    return float(min(r.values())) if r else 0.0


def yh_durum(h: Dict[str, Any], yon: int, tablo: Optional[Dict[str, Any]], Y: Dict[str, Any] = YH_ESIK) -> Tuple[str, float]:
    n = int(h.get("n", 0) or 0)
    if n < Y["karar"]["n_esik"]:
        return "ÖLÇÜLEMEDİ", 0.0
    g = yh_guc_bak(n, yon, tablo, Y)
    if h.get("tutar"):
        return "TUTAR", g
    if n >= Y["etiket"]["n_yeter"] or g >= Y["etiket"]["guc_esik"]:
        return "DESTEKLENMEDİ", g
    return "ÖLÇÜLEMEDİ", g


def yh_etiket(dur: Dict[Tuple[str, str], str], Y: Dict[str, Any] = YH_ESIK) -> str:
    """dur: (pazar, dönem) -> durum. Önceden yazılı genel etiket kuralı."""
    karar = [tuple(x) for x in Y["karar"]["hucre_karar"]]
    d = {k: dur.get(k) or "ÖLÇÜLEMEDİ" for k in karar}
    tut = [k for k in karar if d[k] == "TUTAR"]
    ad = ", ".join(f"{p} {q}" for p, q in tut)
    if len(tut) == 4:
        bist = all(dur.get(("BIST", q)) == "TUTAR" for q in ("2023", "2024-26"))
        return "İZ + BIST" if bist else "İZ"
    if len(tut) >= 2:
        return f"EMARE ({ad})"
    oteki = [k for k in karar if k not in tut]
    hepsi_des = all(d[k] == "DESTEKLENMEDİ" for k in oteki)
    if len(tut) == 1:
        return f"{'DESTEKLENMEDİ' if hepsi_des else 'ÖLÇÜLEMEDİ'} (tek hücre tuttu: {ad})"
    return "DESTEKLENMEDİ" if hepsi_des else "ÖLÇÜLEMEDİ"


def _yh_bh(p: List[float], q: float = 0.10) -> List[bool]:
    p = np.asarray(p, float); n = int(np.isfinite(p).sum()); out = np.zeros(len(p), bool)
    if not n:
        return out.tolist()
    o = np.argsort(np.where(np.isfinite(p), p, np.inf)); kmax = -1
    for r, i in enumerate(o[:n], 1):
        if p[i] <= q * r / n:
            kmax = r
    if kmax > 0:
        out[o[:kmax]] = True
    return out.tolist()


# ================================================================ 4) GÜÇ
def _yh_boot_alt(a_m: np.ndarray, b_m: np.ndarray, rng: np.random.Generator, B: int, q: float) -> float:
    M = len(a_m)
    if M == 0:
        return np.nan
    ix = rng.integers(0, M, size=(B, M))
    pa = a_m[ix].sum(1); pb = b_m[ix].sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        v = np.where(pb > 0, pa / pb, np.nan)
    v = v[np.isfinite(v)]
    return float(np.quantile(v, q)) if len(v) else np.nan


def yh_guc_havuz(P: Dict[str, Any], Cl: np.ndarray, Y: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Güç havuzu: rastgele hisse-gün x d x yön için olay / eş / plasebo göstergeleri (gerçek fiyat)."""
    G = Y["guc"]; R = int(Y["olcu"]["pencere_azami"]); me = Y["kontrol"]["min_es"]
    idx = P["tarih"]; dn = OC._oc_donem(pd.Series(idx), OC.OC_ESIK)
    a = idx.searchsorted(pd.Timestamp(G["bas"])); b = idx.searchsorted(pd.Timestamp(G["son"]), side="right")
    D, J = np.nonzero(P["ok"][a:b] & (P["H"][a:b] >= 0)); D = D + a
    rng = np.random.default_rng(G["tohum"])
    sec = rng.choice(len(D), min(G["havuz"], len(D)), replace=False)
    sat = []
    t0 = time.time()
    for q, i in enumerate(sec):
        d, j = int(D[i]), int(J[i])
        havuz = np.flatnonzero(P["ok"][d]); pj = int(np.flatnonzero(havuz == j)[0])
        Cr, Hr, Lr = _yh_pencere(Cl, d, R, havuz), _yh_pencere(P["Hi"], d, R, havuz), _yh_pencere(P["Lo"], d, R, havuz)
        Ek = P["Op"][d, havuz]
        es0 = P["H"][d, havuz] == P["H"][d, j]
        ad = np.flatnonzero(P["ok"][:, j]); ad = ad[(dn[ad] == dn[d]) & (ad != d)]
        for yon in G["yon"]:
            for dd in G["d"]:
                Sm = yh_sim(Cr, Hr, Lr, Ek, Ek * (1 - yon * dd), yon, Y)
                if not Sm["olc"][pj]:
                    continue
                es = es0 & Sm["olc"]; es[pj] = False
                if es.sum() < me:
                    continue
                r2 = np.random.default_rng([G["tohum"], q, int(dd * 1000), yon + 2]); pl = None
                for _ in range(Y["kontrol"]["plasebo_deneme"]):
                    if not len(ad):
                        break
                    dp = int(ad[r2.integers(len(ad))]); Ep = float(P["Op"][dp, j])
                    Sp = yh_sim(_yh_pencere(Cl, dp, R, np.array([j])), _yh_pencere(P["Hi"], dp, R, np.array([j])),
                                _yh_pencere(P["Lo"], dp, R, np.array([j])), np.array([Ep]), np.array([Ep * (1 - yon * dd)]), yon, Y)
                    if Sp["olc"][0]:
                        pl = float(Sp["h5"][0]); break
                if pl is None:
                    continue
                sat.append({"q": q, "d": d, "j": j, "ay": str(idx[d].to_period("M")), "yon": yon, "dd": dd, "h5": float(Sm["h5"][pj]),
                            "st5": float(Sm["st5"][pj]), "es_h5": float(np.mean(Sm["h5"][es])), "es_st5": float(np.mean(Sm["st5"][es])), "pl_h5": pl})
        if (q + 1) % 500 == 0:
            yhlog.info("güç havuzu %d / %d (%.0f sn)", q + 1, len(sec), time.time() - t0)
    return pd.DataFrame(sat)


def yh_guc_tekrar(Hv: pd.DataFrame, n: int, kat_ref: float, rng: np.random.Generator, Y: Dict[str, Any] = YH_ESIK) -> bool:
    """Bir güç tekrarı: n olay çek, KAT_ref enjekte et, dört şartlı TUTAR kuralı."""
    Kt = Y["kat"]
    x = Hv.iloc[rng.choice(len(Hv), n, replace=False)]
    h5 = x.h5.to_numpy(float).copy(); st5 = x.st5.to_numpy(float).copy()
    es5 = x.es_h5.to_numpy(float); esst = x.es_st5.to_numpy(float); pl = x.pl_h5.to_numpy(float)
    if kat_ref > 1.0:
        sh = h5.sum(); qq = (kat_ref * es5.sum() - sh) / max(n - sh, 1e-9); qq = min(max(qq, 0.0), 1.0)
        f = (h5 == 0) & (rng.random(n) < qq)
        h5[f] = 1.0; st5[f] = 0.0
    ay = x.ay.to_numpy(); aylar, inv = np.unique(ay, return_inverse=True)
    a_m = np.bincount(inv, weights=h5); b_m = np.bincount(inv, weights=es5); p_m = np.bincount(inv, weights=pl)
    alt = _yh_boot_alt(a_m, b_m, rng, Kt["bootstrap"], Kt["guven"][0])
    palt = _yh_boot_alt(a_m, p_m, rng, Kt["bootstrap"], Kt["guven"][0])
    return bool(n >= Y["karar"]["n_esik"] and np.isfinite(alt) and alt > 1 and st5.mean() < esst.mean() and np.isfinite(palt) and palt > 1)


def yh_guc_tablo(Hv: pd.DataFrame, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    G = Y["guc"]; T: Dict[str, Any] = {}
    for yon in G["yon"]:
        for n in G["n"]:
            for kr in G["kat_ref"]:
                for dd in G["d"]:
                    x = Hv[(Hv.yon == yon) & (Hv.dd == dd)]
                    if len(x) < n:
                        v = np.nan
                    else:
                        rng = np.random.default_rng([G["tohum"], yon + 2, n, int(kr * 100), int(dd * 1000)])
                        v = float(np.mean([yh_guc_tekrar(x, n, kr, rng, Y) for _ in range(G["tekrar"])]))
                    T.setdefault(str(yon), {}).setdefault(str(n), {}).setdefault(f"{kr:.2f}", {})[f"{dd:.2f}"] = v
    return T


def yh_guc(cikti: Optional[str] = None, veri: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    cikti = cikti or YH_YOL["cikti"]; t0 = time.time()
    Vd = OC.oc_veri(Y["guc"]["pazar"], klasor=veri or YH_YOL["veri"])
    P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
    Hv = yh_guc_havuz(P, Cl, Y)
    T = yh_guc_tablo(Hv, Y)
    ozet = {f"{yon}|{dd:.2f}": {"n": int(len(x)), "p_h5": float(x.h5.mean()), "p_es_h5": float(x.es_h5.mean()), "p_pl_h5": float(x.pl_h5.mean()),
                                 "p_st5": float(x.st5.mean()), "p_es_st5": float(x.es_st5.mean())}
            for (yon, dd), x in Hv.groupby(["yon", "dd"])}
    J = {"surum": YH_SURUM, "yh_esik_sha": yh_esik_sha(Y), "zaman_utc": _yh_simdi(), "havuz_ozet": ozet, "guc": T, "sure_sn": round(time.time() - t0, 1)}
    _yh_yaz(_yh_yol("guc_json", cikti), json.dumps(J, ensure_ascii=False, indent=1, sort_keys=True), "güç tablosu")
    _yh_yaz(_yh_yol("guc_md", cikti), yh_guc_md(J, Y), "güç md")
    return J


def yh_guc_md(J: Dict[str, Any], Y: Dict[str, Any] = YH_ESIK) -> str:
    G = Y["guc"]
    s = ["# YAPI_HEDEF — GÜÇ TABLOSU", "", f"Üreten: `python YAPI_HEDEF.py guc` ({J['surum']}); {J['zaman_utc']}; YH_ESIK_SHA `{J['yh_esik_sha']}`.", "",
         G["tanim"], "", "Havuz (rastgele hisse-gün; olay = rastgele gün, yani taban):", "",
         "| yön | d | n | P(+5 önce) olay | eş | plasebo | P(stop önce) olay | eş |", "|---|---|---|---|---|---|---|---|"]
    for k, v in sorted(J["havuz_ozet"].items()):
        yon, dd = k.split("|")
        s.append(f"| {yon} | {dd} | {v['n']} | {_yz(v['p_h5'])} | {_yz(v['p_es_h5'])} | {_yz(v['p_pl_h5'])} | {_yz(v['p_st5'])} | {_yz(v['p_es_st5'])} |")
    for yon in G["yon"]:
        s += ["", f"## Yön {'+' if yon > 0 else '-'}: güç (TUTAR payı); sütun KAT_ref / d", "",
              "| n | " + " | ".join(f"KAT {_sy(kr)} d {_yz(dd, 0)}" for kr in G["kat_ref"] for dd in G["d"]) + " |",
              "|---|" + "---|" * (len(G["kat_ref"]) * len(G["d"]))]
        for n in G["n"]:
            r = J["guc"][str(yon)][str(n)]
            s.append(f"| {n} | " + " | ".join(_yz(r[f'{kr:.2f}'][f'{dd:.2f}'], 0) for kr in G["kat_ref"] for dd in G["d"]) + " |")
    s += ["", "KAT_ref 1,00 sütunu yanlış pozitif payıdır (enjeksiyon yok). Etiket için KAT 1,25 sütunlarının EN KÜÇÜĞÜ kullanılır.", ""]
    return "\n".join(s)


# ================================================================ 5) ÖN KAYIT ve KAPI
_YH_KAPI_DESEN = {"esik": r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"YH_KOD_SHA:\s*`([0-9a-f]{64})`", "oc": r"OC_KOD_SHA:\s*`([0-9a-f]{64})`",
                  "s6": r"S6_KOD_SHA:\s*`([0-9a-f]{64})`", "fv": r"FV_KOD_SHA:\s*`([0-9a-f]{64})`", "guc": r"GUC_SHA:\s*`([0-9a-f]{64})`",
                  "y2": r"Y2_OLAY_SHA:\s*`([0-9a-f]{64})`", "zaman": r"ZAMAN \(UTC\):\s*`([^`]+)`"}


def yh_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    g = _yh_yol("guc_json", cikti)
    if not os.path.exists(g):
        raise YHHata(f"güç tablosu yok: {g} (önce `python YAPI_HEDEF.py guc`)")
    return {"esik": yh_esik_sha(), "kod": _yh_sha_dosya(YH_YOL["kod"]), "oc": _yh_sha_dosya(YH_YOL["oc_kod"]), "s6": _yh_sha_dosya(YH_YOL["s6_kod"]),
            "fv": _yh_sha_dosya(YH_YOL["fv_kod"]), "guc": _yh_sha_dosya(g), "y2": _yh_sha_dosya(YH_YOL["y2_olay"])}


def yh_kontrol_tablosu(tablo: Optional[Dict[str, Tuple[str, str]]] = None) -> str:
    import IZ_KARNE as IK
    tablo = YH_KONTROL if tablo is None else tablo
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = tablo.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def yh_sayim(veri: Optional[str] = None, islem: int = 1, denemeler: Optional[List[str]] = None) -> Dict[str, Any]:
    """GETİRİSİZ olay sayımı: sinyal günü (sinyal dönemi) ve OC sonrası tekil olay (giriş dönemi). Hedef / stop / eş HESAPLANMAZ."""
    denemeler = denemeler or YH_DENEMELER; out: Dict[str, Any] = {}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); P = OC.oc_panel(Vd)
        S = yh_sinyaller(Vd, p, denemeler, islem)
        for k, X in S.items():
            dg = pd.Series(OC._oc_donem(pd.to_datetime(X.tarih), OC.OC_ESIK)).value_counts().to_dict() if len(X) else {}
            Z, say = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P) if len(X) else (pd.DataFrame(), {})
            ol = Z.donem.value_counts().to_dict() if len(Z) else {}
            out.setdefault(k, {})[p] = {"sinyal": {a: int(b) for a, b in dg.items() if a}, "olay": {a: int(b) for a, b in ol.items() if a},
                                        "sayim": {a: int(b) for a, b in say.items()}, "hisse": int(X.sembol.nunique()) if len(X) else 0}
        yhlog.info("sayım %s tamam", p)
        del Vd, P
    return out


def yh_onkayit_metni(say: Dict[str, Any], sha: Dict[str, str], git_is: Dict[str, str], cikti: Optional[str] = None) -> str:
    J = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    if J["yh_esik_sha"] != yh_esik_sha():
        raise YHHata("güç tablosu bu YH_ESIK ile üretilmemiş: önce `python YAPI_HEDEF.py guc`")
    Y = YH_ESIK
    s = [f"# YAPI_HEDEF — ÖN KAYIT", "", YH_SURUM, "",
         f"- YH_ESIK_SHA: `{sha['esik']}`", f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)",
         f"- OC_CETVEL_SHA (bilgi): `{OC.oc_esik_sha()}`", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)", f"- FV_KOD_SHA: `{sha['fv']}` (FITIL_V2.py)",
         f"- GUC_SHA: `{sha['guc']}` ({YH_DOSYA['guc_json']})", f"- Y2_OLAY_SHA: `{sha['y2']}` (fitil_v2/olay_TAM_DIP.csv.gz)",
         f"- IS_TANIMI: git {git_is.get('commit', '?')[:10]}, {git_is.get('commit_zamani', '?')}",
         f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı. Hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri hesaplanmadı ve okunmadı (yalnız aşağıdaki "
         "getirisiz olay sayımı ve güç simülasyonu: rastgele hisse-gün, sinyal değil). `kos` kontrol listesini, yukarıdaki sha'ları ve bu dosyanın "
         "git kaydını denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez; zorunlu sapma SAPMA-n olarak koşudan ÖNCE buraya yazılır.", "",
         "## Ölçü (Cemal'in yeni test standardı; CLAUDE.md 'YENİ TEST STANDARDI', 'UFUK 15 MUM')", "",
         f"- Cetvel: {Y['cetvel']}.", f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- d: {Y['olcu']['d_tanim']}.",
         f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- Göstergeler: {json.dumps(Y['olcu']['olay_gosterge'], ensure_ascii=False)}.",
         f"- Takip stoplu getiri ve çıkış (bilgi): {Y['olcu']['cikis_bilgi']['tanim']}", "",
         "## Kontrol grupları (K1)", "", f"- EŞ: {Y['kontrol']['es']}.", f"- TABAN: {Y['kontrol']['taban']}.", f"- PLASEBO: {Y['kontrol']['plasebo']}.",
         f"- KAT: {Y['kat']['tanim']}.", "",
         "## Karar kuralı (önceden yazılı; DEĞİŞMEZ)", "", f"- {Y['karar']['tanim']}.", f"- Hücre durumu: {Y['etiket']['hucre']}.",
         f"- Güç bakışı: {Y['etiket']['guc_bak']}.", f"- Genel etiket (deneme başına): {Y['etiket']['genel']}",
         f"- Karar hücreleri: {', '.join(' '.join(x) for x in Y['karar']['hucre_karar'])}; bilgi: BIST 2023, BIST 2024-26, her pazarın 2016-22'si.", "",
         "## Denemeler (sonuç görülmeden sabit)", ""]
    for k in YH_DENEMELER:
        D = Y["denemeler"][k]
        s.append(f"- **{k} {D['ad']}** (yön {'+' if D['yon'] > 0 else '-'}): {D['tanim']}.")
    s += ["", f"S6 parametreleri (v1.1 varsayılan): `{json.dumps(Y['s6_prm'], sort_keys=True)}`", "",
          "## Getirisiz olay sayımı (sinyal günü, sinyal dönemi / OC sonrası tekil olay, giriş dönemi)", "",
          "| Deneme | Pazar | hisse | sinyal 2016-22 / 2023 / 2024-26 | olay 2016-22 / 2023 / 2024-26 | düşme (giriş yok / geç / havuz dışı / tekil) |",
          "|---|---|---|---|---|---|"]
    for k in YH_DENEMELER:
        for p in OC.OC_ESIK["pazar"]:
            x = say.get(k, {}).get(p)
            if not x:
                continue
            sg = " / ".join(str(x["sinyal"].get(q, 0)) for q in ("2016-22", "2023", "2024-26"))
            ol = " / ".join(str(x["olay"].get(q, 0)) for q in ("2016-22", "2023", "2024-26"))
            sy = x["sayim"]
            s.append(f"| {k} | {p} | {x['hisse']} | {sg} | {ol} | {sy.get('giris_yok', 0)} / {sy.get('giris_gec', 0)} / {sy.get('havuz_disi', 0)} / {sy.get('tekil', 0)} |")
    s += ["", "## Güç (gerçek ABD 2023-26 rastgele hisse-gün; dört şartlı hücre kuralı; ayrıntı GUC_TABLOSU.md)", ""]
    for yon in Y["guc"]["yon"]:
        s += [f"Yön {'+' if yon > 0 else '-'} (KAT_ref 1,25; d 3 / 6 / 10; etiket için en küçüğü):", "", "| n | d %3 | d %6 | d %10 | KAT 1,00 (yanlış pozitif, en büyük) |", "|---|---|---|---|---|"]
        for n in Y["guc"]["n"]:
            r = J["guc"][str(yon)][str(n)]
            fp = max(v for v in r["1.00"].values() if v == v) if any(v == v for v in r["1.00"].values()) else np.nan
            s.append(f"| {n} | " + " | ".join(_yz(r["1.25"][f"{dd:.2f}"], 0) for dd in Y["guc"]["d"]) + f" | {_yz(fp, 0)} |")
        s.append("")
    s += ["## Sınırlar (önceden)", "",
          "- Hayatta kalma: evren bugün işlem gören hisseler (ABD V_ABD 1.411; k34 / Tiingo yok); hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo "
          "aynı evrenden.", "- Komisyon / kayma yok; stop çıkışı ertesi açılış (boşluk riski içerir).",
          "- Takip stopu GEÇİCİ kural (Cemal: 'son kural değil'); getiri ve bar sayısı bilgi.",
          "- Y2 olayları FITIL_V2'nin tekilleştirilmiş olaylarıdır (aynı OC kuralı, aynı veri); yeniden OC'den geçirilir.", "",
          "## YH_ESIK (tam metin; mühürlü)", "", "```json", json.dumps(YH_ESIK, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
          yh_kontrol_tablosu(), "", "## SAPMALAR", "", "(yok)", "",
          "## Test", "", "`python test_yapi_hedef.py` (sentetik: sinyaller elle, geleceğe bakma kesme testi, yh_sim hedef / stop / takip / yön -, "
          "eş = aynı kural, plasebo, KAT = OC.oc_kat, etiket kuralı, kapı, uçtan uca kos, e-posta / anahtar taraması, çakışma kapısı).", ""]
    return "\n".join(s)


def _yh_git(yol: str) -> Dict[str, str]:
    try:
        return OC._oc_git_islenmis(yol)
    except OC.OCHata as ex:
        raise YHHata(str(ex))


def yh_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False) -> str:
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit", cikti)
    if os.path.exists(yol) and not uzerine:
        try:
            _yh_git(yol)
            raise YHHata(f"ön kayıt zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
        except YHHata as ex:
            if "zaten" in str(ex):
                raise
            raise YHHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(_yh_yol("sonuc", cikti)):
        raise YHHata("sonuc.json var: ön kayıt ölçümden sonra yazılamaz")
    sha = yh_sha_simdi(cikti)
    try:
        git_is = _yh_git(YH_YOL["is_tanimi"])
    except YHHata:
        git_is = {}
    say = yh_sayim(veri, islem)
    metin = yh_onkayit_metni(say, sha, git_is, cikti)
    _yh_yaz(yol, metin, "ön kayıt")
    return yol


# ---------------------------------------------------------------- 5b) 2. TUR ÖN KAYIT (ON_KAYIT_2.md)
_YH_DONEM3 = ("2016-22", "2023", "2024-26")


def yh_sayim2(veri: Optional[str] = None, islem: int = 1) -> Dict[str, Any]:
    """2. tur GETİRİSİZ sayım: huni (yh_huni) + deneme başına OC olayı ve E5a 'stop_uzak' (yalnız giriş açılışı; hedef / stop / eş YOK)."""
    out: Dict[str, Any] = {"huni": {}, "deneme": {}}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); P = OC.oc_panel(Vd)
        S = yh_sinyaller(Vd, p, YH_DENEMELER_2, islem)
        out["huni"][p] = yh_huni(S, P)
        for k in YH_DENEMELER_2:
            X = S[k]
            Z, say = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P) if len(X) else (pd.DataFrame(), {})
            su = YH_ESIK["denemeler"][k]["stop_uzak"]; uz = {}
            if len(Z):
                Z = Z.merge(X[["sembol", "tarih", "hat"]].assign(tarih=pd.to_datetime(X.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
                with np.errstate(invalid="ignore", divide="ignore"):
                    u = ~(P["Op"][Z.d.to_numpy(int), Z.j.to_numpy(int)] / Z.hat.to_numpy(float) - 1 <= su)
                uz = Z[u].donem.value_counts().to_dict(); Z = Z[~u]
            out["deneme"].setdefault(k, {})[p] = {"olay": {a: int(b) for a, b in (Z.donem.value_counts().to_dict() if len(Z) else {}).items() if a},
                                                  "stop_uzak": {a: int(b) for a, b in uz.items() if a}, "hisse": int(X.sembol.nunique()) if len(X) else 0,
                                                  "sayim": {a: int(b) for a, b in say.items()}}
        yhlog.info("sayım (2. tur) %s tamam", p)
        del Vd, P, S
    return out


def _yh_huni_md(huni: Dict[str, Any], deneme: str, olcum: Optional[Dict[str, Any]] = None) -> List[str]:
    """Huni tablosu: aşama x pazar (sinyal / olay 2023 / olay 2024-26); olcum verilirse son satır ölçülen n (h5 ve eş h5)."""
    pz = [p for p in OC.OC_ESIK["pazar"] if deneme in huni.get(p, {})]
    if not pz:
        return ["(huni yok)"]
    s = ["| Aşama | " + " | ".join(f"{p} sinyal (tümü) | {p} olay 2016-22 / 2023 / 2024-26" for p in pz) + " |", "|---|" + "---|---|" * len(pz)]
    for q, a in enumerate(huni[pz[0]][deneme]["asama"]):
        c = []
        for p in pz:
            x = huni[p][deneme]["asama"][q]
            c.append(f"{x['sinyal']} | " + " / ".join(str(x["olay_donem"].get(d, 0)) for d in _YH_DONEM3))
        s.append(f"| {a['ad']} | " + " | ".join(c) + " |")
    tek = []
    for p in pz:
        T = huni[p][deneme]
        tek.append(f"{p}: " + ", ".join(f"{k} {v}" for k, v in T["tek"].items()) + (f", kir250>0 {T['tek_kir250']}, büyük desen NA {T['buyuk_desen_NA']}"
                                                                                     if "tek_kir250" in T else ""))
    s += ["", "Tek başına düşürdüğü taban sinyali (şart tutmayan): " + "; ".join(tek) + "."]
    if olcum:
        s += ["", "Ölçülen n (OC tekil -> E5a giriş denetimi 'stop_uzak' -> 15 bar ve eş >= 3; karar n'i): " + "; ".join(
            f"{k}: " + ", ".join(f"{p} {q} {n}" for (p, q), n in v.items()) for k, v in olcum.items()) + "."]
    return s


def yh_onkayit2_metni(say: Dict[str, Any], sha: Dict[str, str], git1: Dict[str, str], git_is: Dict[str, str], t1: str) -> str:
    Y = YH_ESIK
    s = ["# YAPI_HEDEF — ÖN KAYIT 2 (2. tur: Y6 / Y7 / Y8 + Y8B bilgi)", "", YH_SURUM + "; 2. tur eklendi (YAPI_HEDEF_2_IS_TANIMI.md)", "",
         f"- YH_ESIK_SHA: `{sha['esik']}` (2. tur denemeleri dahil)",
         f"- ESIK_TUR1_SHA: `{t1}` (YH_ESIK'ten Y6-Y8B çıkarılınca; = ON_KAYIT.md YH_ESIK_SHA = güç tablosu yh_esik_sha: Y1-Y5 eşikleri AYNEN)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)",
         f"- FV_KOD_SHA: `{sha['fv']}` (FITIL_V2.py)", f"- GUC_SHA: `{sha['guc']}` ({YH_DOSYA['guc_json']}; 1. turun güç tablosu, aynı kural)",
         f"- Y2_OLAY_SHA: `{sha['y2']}` (değişmedi; 2. turda kullanılmaz)",
         f"- ON_KAYIT_1: git {git1.get('commit', '?')[:10]}, {git1.get('commit_zamani', '?')}",
         f"- IS_TANIMI_2: git {git_is.get('commit', '?')[:10]}, {git_is.get('commit_zamani', '?')}",
         f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "Bu dosya 2. tur ölçümünden ÖNCE yazıldı. Y6 / Y7 / Y8 / Y8B için hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri hesaplanmadı ve "
         "okunmadı (yalnız aşağıdaki getirisiz huni ve olay sayımı; E5a sayımı yalnız giriş açılışını kullanır). `kos --deneme Y6,Y7,Y8` bu dosyanın "
         "kontrol listesini, sha'larını, git kaydını ve Y1-Y5 eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.", "",
         "UYARI (K2 / K9 benzeri, önceden): Y6-Y8 şartları Cemal'in 17 Kas değerlendirmesinden (CEMAL_DEGERLENDIRME_2026-11-17.md E1-E11) "
         "yazıldı; o değerlendirme 1. tur örnek grafiklerinin SONUCU görülerek yapıldı (30 örnek). Bu yüzden bu ölçüm o 30 örneği de içeren "
         "veride yapılır ve tek başına bağımsız kanıt değildir; TUTAR çıkan hücre ileri testle (kriz sonrası veri) yeniden ölçülür.", "",
         "## Ölçü, kontrol grupları, karar kuralı", "",
         "1. turla AYNI (ON_KAYIT.md; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' bölümleri değişmedi, ESIK_TUR1_SHA kanıtı):",
         f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- EŞ: {Y['kontrol']['es']}.",
         f"- PLASEBO: {Y['kontrol']['plasebo']}.", f"- Karar: {Y['karar']['tanim']}.", f"- Hücre durumu: {Y['etiket']['hucre']}.",
         f"- Genel etiket (deneme başına): {Y['etiket']['genel']}", "- Y8B bilgi satırıdır: etiketi yazılır, karar değildir. BH (bilgi) yalnız Y6 / Y7 / Y8 x 4 karar hücresi "
         "(12 p; 1. turun BH'si ayrı ve korunur).", "",
         "## Denemeler (sonuç görülmeden sabit; YAPI_HEDEF_2_IS_TANIMI.md §3)", ""]
    for k in YH_DENEMELER_2:
        D = Y["denemeler"][k]
        s.append(f"- **{k} {D['ad']}**: {D['tanim']}.")
    s += ["", "## Yorumlar (iş tanımında açık bırakılan noktalar; koşudan önce sabit)", "",
          "- YORUM-1 (Y6 bölge): 'bölge içi' = durum AL ise açık S6 bölgesinin as-of t kutusu [kutu_sol_i(t), t-1] (hat = kutu_alt), AL_BOLGESIZ ise "
          "t-1 taban penceresi [bas_i(t-1), t-1] (hat = DİP(t-1)); kırılım günü t bölgeye girmez.",
          "- YORUM-2 (Y6 (b) tavan): Y1'in kırılım tavanı TAVAN(t-1) (C_t > TAVAN(t-1) Y1 tanımı); mum boyu mutlak H - L, bölge medyanı aynı birimde.",
          "- YORUM-3 (Y6 (d)): 250 bar = [t-250, t-1] (t hariç); 10 parça x 25; doğru en küçük kareler; eğim = uyum(son) / uyum(ilk) - 1.",
          "- YORUM-4 (Y7): şartlar Y3'ün seçtiği EN BÜYÜK n penceresinde sınanır (Y7 ⊆ Y3 sinyalleri; başka n aranmaz). ATR250 birimi TR / C_önceki "
          "(S6 refOnce), mum birimi (H - L) / C; ATR penceresi W'den önceki 250 geçerli bar (en az 120).",
          "- YORUM-5 (E5a): sinyalde C_t / hat ön elemesi, ölçümde gerçek giriş açılışıyla denetim; denetim OC tekilleştirmesinden SONRA (aşan olay "
          "düşer, aynı 60 günde başka olay yerine konmaz); 'stop_uzak' sayımı raporda.",
          "- YORUM-6 (Y8): 'patlamış yapı' = durum KIRILDI (bölgeli; KIRILDI_BOLGESIZ değil) [t-250, t-1] içinde; Y4'ün KIRILDI sayımıyla aynı.",
          "- YORUM-7 (E5b bilgi): stop0b = max(hat x 0,98, giriş x 0,95); olay ve eşler aynı d_b; plasebo yok; karar satırı değil.", "",
          "## Huni ve getirisiz olay sayımı (sinyal: sinyal günü; olay: OC tekil sonrası, giriş dönemi)", ""]
    for k in ("Y6", "Y7"):
        s += [f"### {k} hunisi", ""] + _yh_huni_md(say["huni"], k) + [""]
    s += ["| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 (E5a sonrası) | stop_uzak 2016-22 / 2023 / 2024-26 |", "|---|---|---|---|---|"]
    for k in YH_DENEMELER_2:
        for p in OC.OC_ESIK["pazar"]:
            x = say["deneme"].get(k, {}).get(p)
            if x:
                s.append(f"| {k} | {p} | {x['hisse']} | " + " / ".join(str(x["olay"].get(q, 0)) for q in _YH_DONEM3) + " | "
                         + " / ".join(str(x["stop_uzak"].get(q, 0)) for q in _YH_DONEM3) + " |")
    s += ["", "Güç: 1. turun güç tablosu (GUC_TABLOSU.md; aynı dört şartlı kural, ABD 2023-26 rastgele hisse-gün). Hücre n < 1.000 ve güç < %80 ise "
          "tutmayan hücre ÖLÇÜLEMEDİ yazılır (1. turla aynı).", "",
          "## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)", ""]
    try:
        tablo = json.load(open(_yh_yol("guc_json"), encoding="utf-8"))
    except (OSError, ValueError):
        tablo = None
    for k in YH_DENEMELER_2:
        if Y["denemeler"][k].get("bilgi"):
            continue
        hc = [(p, q, int(say["deneme"].get(k, {}).get(p, {}).get("olay", {}).get(q, 0))) for p, q in Y["karar"]["hucre_karar"]]
        gs = [yh_guc_bak(n, Y["denemeler"][k]["yon"], tablo) for _, _, n in hc]
        ifade = "; ".join(f"{p} {q} en çok {n} olay (güç {_yz(g, 0)})" for (p, q, n), g in zip(hc, gs))
        if all(n == 0 for _, _, n in hc):
            s.append(f"- {k}: karar hücrelerinde OLAY YOK ({ifade}). Ön eleme şartları birlikte hiç olay bırakmadı (huni son aşaması): {k} "
                     "ÖLÇÜLEMEDİ (n = 0) olur. Eşik değiştirilmedi (ön kayıt kuralı; değişiklik ana model kararıdır).")
        else:
            az = all(n < Y["etiket"]["n_yeter"] and g < Y["etiket"]["guc_esik"] for (_, _, n), g in zip(hc, gs))
            s.append(f"- {k}: {ifade}." + (" Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, "
                                          "ÖLÇÜLEMEDİ yazılır." if az else ""))
    s += ["- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer.", "",
          "## YH_ESIK 2. tur girdileri (tam metin; geri kalanı ON_KAYIT.md ile aynı)", "", "```json",
          json.dumps({k: Y["denemeler"][k] for k in YH_DENEMELER_2}, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
          yh_kontrol_tablosu(YH_KONTROL_2), "", "## SAPMALAR", "", "(yok)", "",
          "## Test", "", "`python test_yapi_hedef.py` (1. tur testleri aynen + 2. tur: hat dokunuş sayımı, kırılım payı, iki kenar, büyük desen eğimi, "
          "Y8 hafızası, Y6 / Y7 / Y8 / Y8B geleceğe bakma (prefix), ESIK_TUR1_SHA = 1. tur mührü, 2. tur uçtan uca kos + kapı).", ""]
    return "\n".join(s)


def yh_onkayit2_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_2.md: 1. tur ölçülmüş olmalı (sonuc.json Y1-Y5), 2. tur ölçülmemiş; Y1-Y5 eşik mührü tutmalı; huni taban aşaması = 1. tur girdisi."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit2", cikti)
    if os.path.exists(yol) and not uzerine:
        raise YHHata(f"ön kayıt 2 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if git and os.path.exists(yol):
        try:
            _yh_git(yol)
            raise YHHata(f"ön kayıt 2 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
        except YHHata as ex:
            if "zaten" in str(ex):
                raise
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("1. tur sonuc.json yok: 2. tur ön kaydı 1. tur ölçümünden sonra yazılır")
    J = json.load(open(sy, encoding="utf-8"))
    if [k for k in YH_DENEMELER_2 if k in J.get("deneme", {})]:
        raise YHHata("2. tur denemeleri zaten ölçülmüş: ön kayıt ölçümden sonra yazılamaz")
    t1 = yh_esik_sha_tur1()
    m1 = re.search(_YH_KAPI_DESEN["esik"], open(_yh_yol("onkayit", cikti), encoding="utf-8").read())
    gj = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    if not (m1 and m1.group(1) == t1 == gj.get("yh_esik_sha")):
        raise YHHata("Y1-Y5 eşik mührü tutmuyor (ON_KAYIT.md / güç tablosu / yh_esik_sha_tur1)")
    sha = yh_sha_simdi(cikti)
    git1 = _yh_git(_yh_yol("onkayit", cikti)) if git else {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi2"]) if git else {}
    except YHHata:
        git_is = {}
    say = yh_sayim2(veri, islem)
    for p in OC.OC_ESIK["pazar"]:                              # regresyon: huni taban aşaması = 1. turun sinyal girdisi
        for k, t in (("Y6", "Y1"), ("Y7", "Y3")):
            g1 = J.get("sayim", {}).get(t, {}).get(p, {}).get("girdi")
            g2 = say["huni"][p][k]["asama"][0]["sinyal"]
            if g1 is not None and int(g1) != int(g2):
                raise YHHata(f"regresyon: {p} {t} sinyal sayısı 1. turda {g1}, şimdi {g2} -> ön kayıt yazılmadı")
    _yh_yaz(yol, yh_onkayit2_metni(say, sha, git1, git_is, t1), "ön kayıt 2")
    return yol


def yh_kapi(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True, tur: int = 1) -> Dict[str, Any]:
    """Koşu kapısı: kontrol listesi + sha'lar + ön kayıt / kod / güç tablosu git'e işlenmiş ve değişmemiş.
    tur 2: ON_KAYIT_2.md; ayrıca ESIK_TUR1_SHA = yh_esik_sha_tur1() = ON_KAYIT.md YH_ESIK_SHA = güç tablosu yh_esik_sha (Y1-Y5 eşikleri aynen)."""
    yol = _yh_yol("onkayit" if tur == 1 else "onkayit2", cikti)
    if tur == 2:
        t1 = yh_esik_sha_tur1()
        m2 = re.search(r"ESIK_TUR1_SHA:\s*`([0-9a-f]{64})`", open(yol, encoding="utf-8").read()) if os.path.exists(yol) else None
        y1 = _yh_yol("onkayit", cikti)
        m1 = re.search(_YH_KAPI_DESEN["esik"], open(y1, encoding="utf-8").read()) if os.path.exists(y1) else None
        gj = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("guc_json", cikti)) else {}
        if not (m2 and m1 and m2.group(1) == t1 == m1.group(1) == gj.get("yh_esik_sha")):
            raise YHHata("2. tur kapısı: Y1-Y5 eşik mührü (ESIK_TUR1_SHA / ON_KAYIT.md / güç tablosu) tutmuyor -> koşu DURDU")
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt yok: {yol}")
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    metin = open(yol, encoding="utf-8").read(); bul = {}
    for ad, desen in _YH_KAPI_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise YHHata(f"ön kayıtta {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"]); out["git_guc"] = _yh_git(_yh_yol("guc_json", cikti))
    yhlog.info("yh_kapi AÇIK (%s)", yol)
    return out


# ================================================================ 6) KOŞU
def yh_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, deneme: str, pazar: str, Y: Dict[str, Any] = YH_ESIK) -> int:
    """Rastgele 5 olay: veri t'de kesilir; sinyal t'de aynı hat / stop0 ile yeniden çıkmalı."""
    G = Y["gelecek_denetimi"]
    if not len(X):
        return 0
    rng = np.random.default_rng([G["tohum"], YH_DENEMELER_HEPSI.index(deneme), OC.OC_ESIK["pazar"].index(pazar)])
    n = 0
    for r in X.iloc[rng.choice(len(X), min(G["n"], len(X)), replace=False)].itertuples():
        t = pd.Timestamp(r.tarih); df = Vd["V"][r.sembol]; kes = df[df.index <= t]
        if deneme == "Y2":
            h = yh_y2_hat(kes, [t])[0]
            ok = np.isfinite(h) and abs(h - float(r.hat)) <= 1e-9 * max(1.0, abs(h))
        elif deneme in YH_DENEMELER_3:       # 3. tur: Y1 sinyali kesik veride aynı + dört özellik kesik veriden yeniden = dosya (göreli 1e-5)
            X1, _ = yh_s6_hisse(kes, Y)
            z = X1[pd.to_datetime(X1.tarih) == t] if len(X1) else X1
            ok = len(z) == 1 and abs(float(z.stop0.iloc[0]) - float(r.stop0)) <= 1e-9 * max(1.0, abs(float(r.stop0))) and pd.Timestamp(X1.tarih.iloc[-1]) == t
            if ok:
                Fr = yh_y9_ozellik(kes, [t], Y).iloc[0][_Y9_OZ].to_numpy(float)
                ok = bool(np.allclose(Fr, np.array([getattr(r, c) for c in _Y9_OZ], float), rtol=1e-5, atol=1e-7, equal_nan=True))
        else:
            Z = yh_hisse_sinyal(kes, deneme, Y)
            z = Z[pd.to_datetime(Z.tarih) == t] if len(Z) else Z
            ok = len(z) == 1 and abs(float(z.stop0.iloc[0]) - float(r.stop0)) <= 1e-9 * max(1.0, abs(float(r.stop0))) and pd.Timestamp(Z.tarih.iloc[-1]) == t
        if not ok:
            raise YHHata(f"geleceğe bakma denetimi TUTMADI: {deneme} {pazar} {r.sembol} {t.date()}")
        n += 1
    return n


def yh_sonuc_deneme(Ol: pd.DataFrame, deneme: str, tablo: Optional[Dict[str, Any]], Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    yon = Y["denemeler"][deneme]["yon"]; H_ = []; dur = {}
    for p in OC.OC_ESIK["pazar"]:
        for q, _a, _b in OC.OC_ESIK["donem"]:
            x = Ol[(Ol.pazar == p) & (Ol.donem == q)] if len(Ol) else Ol
            h = yh_hucre(x, Y)
            if len(x) and "b_h5" in x.columns:      # 2. tur E5b bilgi sütunları (1. turda yok)
                h.update(yh_hucre_e5b(x, Y))
            durum, g = yh_durum(h, yon, tablo, Y)
            dur[(p, q)] = durum
            H_.append({"pazar": p, "donem": q, "karar_hucre": [p, q] in Y["karar"]["hucre_karar"], **h, "guc": g, "durum": durum})
    out = {"ad": Y["denemeler"][deneme]["ad"], "yon": yon, "hucre": H_, "etiket": yh_etiket(dur, Y)}
    if Y["denemeler"][deneme].get("bilgi"):
        out["bilgi"] = True
    return out


def yh_satir_yaz(Ol: pd.DataFrame, deneme: str, cikti: str) -> str:
    yol = os.path.join(cikti, YH_DOSYA["satir"].format(d=deneme))
    Ol.to_csv(yol, index=False, float_format="%.6g", compression="gzip")
    mb = os.path.getsize(yol) / 1e6
    if mb > YH_SATIR_AZAMI_MB:
        os.makedirs(YH_YOL["satir_buyuk"], exist_ok=True)
        hedef = os.path.join(YH_YOL["satir_buyuk"], os.path.basename(yol))
        os.replace(yol, hedef)
        yhlog.warning("%s %.1f MB > %.0f MB: repoya girmez, %s", deneme, mb, YH_SATIR_AZAMI_MB, hedef)
        return hedef
    return yol


def yh_kos(denemeler: Optional[List[str]] = None, cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1,
           git: bool = True, kontrol: bool = True, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]; denemeler = denemeler or YH_DENEMELER
    bilinmeyen = [k for k in denemeler if k not in YH_DENEMELER_HEPSI]
    if bilinmeyen:
        raise YHHata(f"bilinmeyen deneme: {bilinmeyen}")
    if any(k in YH_DENEMELER_3 for k in denemeler):        # 3. tur ayrı koşu (yh_kos3); önceki turların akışına dokunmaz
        return yh_kos3(list(denemeler), cikti, veri, islem, git, kontrol, Y)
    tur = 2 if any(k in YH_DENEMELER_2 for k in denemeler) else 1
    if tur == 2:
        if any(k not in YH_DENEMELER_2 for k in denemeler):
            raise YHHata(f"1. ve 2. tur denemeleri aynı koşuda olmaz: {denemeler}")
        if "Y8" in denemeler and "Y8B" not in denemeler:
            denemeler = list(denemeler) + ["Y8B"]          # Y8B bilgi satırı Y8 ile birlikte (ön kayıtta yazılı)
        denemeler = [k for k in YH_DENEMELER_2 if k in denemeler]
    sy = _yh_yol("sonuc", cikti)
    sonuc = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else None
    if sonuc is not None:
        tekrar = [k for k in denemeler if k in sonuc.get("deneme", {})]
        if tekrar:
            raise YHHata(f"bu denemeler zaten ölçüldü (ölçüm bir kez koşulur): {tekrar}")
    ok = yh_kapi(cikti, git=git, kontrol=kontrol, tur=tur)
    kos_zaman = _yh_simdi()
    if ok["onkayit_zaman"] > kos_zaman:
        raise YHHata("ön kayıt zamanı koşu zamanından sonra")
    tablo = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    if sonuc is None:
        sonuc = {"surum": YH_SURUM, "deneme": {}, "kos": [], "veri_not": {}, "gelecek_denetimi": {}, "sayim": {}}
    sonuc["kos"].append({"zaman_utc": kos_zaman, "kapi": ok, "denemeler": denemeler, "islem": islem})
    Ols: Dict[str, List[pd.DataFrame]] = {k: [] for k in denemeler}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
        S = yh_sinyaller(Vd, p, denemeler, islem, Y)
        if tur == 2:
            sonuc.setdefault("huni", {})[p] = yh_huni(S, P)
        for k in denemeler:
            X = S.get(k, pd.DataFrame())
            sonuc["gelecek_denetimi"].setdefault(k, {})[p] = yh_gelecek_denetimi(Vd, X, k, p, Y)
            Z, say = yh_olc_pazar(Vd, P, Cl, X, k, p, islem, Y)
            if len(Z) and Y["denemeler"][k].get("e5b"):
                Z = yh_e5b_olc(P, Cl, Z, Y, Y["denemeler"][k]["e5b"])
            sonuc["sayim"].setdefault(k, {})[p] = {a: int(b) for a, b in say.items()}
            if len(Z):
                Ols[k].append(Z)
            yhlog.info("%s %s: olay %d (%.0f sn)", k, p, len(Z), time.time() - t0)
        del Vd, P, Cl
    for k in denemeler:
        Ol = pd.concat(Ols[k], ignore_index=True) if Ols[k] else pd.DataFrame()
        sonuc["deneme"][k] = yh_sonuc_deneme(Ol, k, tablo, Y)
        if len(Ol):
            sonuc["deneme"][k]["satir_dosya"] = os.path.relpath(yh_satir_yaz(Ol, k, cikti), KOK_YH)
    # BH (bilgi): karar hücrelerinde KAT5 p, bütün ölçülen denemeler (2. tur ayrı aile: 'bh_tur2'; 1. turun 'bh'si korunur)
    anahtar, pler = [], []
    for k in (YH_DENEMELER if tur == 1 else [x for x in YH_DENEMELER_2 if not Y["denemeler"][x].get("bilgi")]):
        for h in sonuc["deneme"].get(k, {}).get("hucre", []):
            if h.get("karar_hucre"):
                anahtar.append((k, h["pazar"], h["donem"])); pler.append(h.get("h5_p", np.nan))
    sonuc["bh" if tur == 1 else "bh_tur2"] = [{"deneme": a, "pazar": b, "donem": c, "p": p, "bh_q10": g}
                                              for (a, b, c), p, g in zip(anahtar, pler, _yh_bh(pler, 0.10))]
    sonuc["sure_sn"] = round(sonuc.get("sure_sn", 0) + time.time() - t0, 1)
    _yh_yaz(sy, json.dumps(sonuc, ensure_ascii=False, indent=1, default=_yh_json), "sonuç")
    return {"sonuc": sonuc, "rapor": yh_rapor(cikti) if tur == 1 else yh_rapor2(cikti)}


def yh_huni(S: Dict[str, pd.DataFrame], P: Dict[str, Any]) -> Dict[str, Any]:
    """GETİRİSİZ huni: taban sinyalinden (Y1 / Y3) şartlar sırayla eklenince sinyal (sinyal dönemi) ve OC sonrası tekil olay (giriş dönemi)
    sayısı; ayrıca her şartın TEK BAŞINA düşürdüğü taban sinyali. Hedef / stop / eş HESAPLANMAZ."""
    def say(X: pd.DataFrame) -> Dict[str, Any]:
        if not len(X):
            return {"sinyal": 0, "sinyal_donem": {}, "olay_donem": {}}
        sg = pd.Series(OC._oc_donem(pd.to_datetime(X.tarih), OC.OC_ESIK)).value_counts().to_dict()
        Z, _ = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P)
        ol = Z.donem.value_counts().to_dict() if len(Z) else {}
        return {"sinyal": int(len(X)), "sinyal_donem": {a: int(b) for a, b in sg.items() if a}, "olay_donem": {a: int(b) for a, b in ol.items() if a}}
    out: Dict[str, Any] = {}
    F = S.get("_Y6F")
    if F is not None:
        b = {c: F[c].astype(bool).to_numpy() if len(F) else np.zeros(0, bool) for c in ("f_hat", "f_kir", "f_stop", "f_buyuk")}
        kir = F.kir250.astype(int).to_numpy() if len(F) else np.zeros(0, int)
        m = np.ones(len(F), bool); A = [{"ad": "Y1 (S6 AL)", **say(F)}]
        for c, ad in (("f_hat", "+ (a) hat net (>= 3 dokunuş, eğim)"), ("f_kir", "+ (b) gerçek kırılım (%1 + mum)"),
                      ("f_stop", "+ (c) stop <= %10 (C_t ön eleme)"), ("f_buyuk", "+ (d) büyük desen alçalan değil = Y6")):
            m = m & b[c]; A.append({"ad": ad, **say(F[m])})
        A.append({"ad": "Y6 + hafıza temiz = Y8", **say(F[m & (kir == 0)])})
        A.append({"ad": "Y6 + patlamış yapı var = Y8B (bilgi)", **say(F[m & (kir > 0)])})
        bna = int(F.buyuk_egim.isna().sum()) if len(F) else 0
        out["Y6"] = {"asama": A, "tek": {c: int((~b[c]).sum()) for c in b}, "tek_kir250": int((kir > 0).sum()), "buyuk_desen_NA": bna}
    F = S.get("_Y7F")
    if F is not None:
        b = {c: F[c].astype(bool).to_numpy() if len(F) else np.zeros(0, bool) for c in ("f_kenar", "f_mum", "f_dok", "f_stop")}
        m = np.ones(len(F), bool); A = [{"ad": "Y3 (KAZAN + DÖNÜŞ)", **say(F)}]
        for c, ad in (("f_kenar", "+ (a) iki kenar (%5)"), ("f_mum", "+ (b) dipte küçük mum (0,9 ATR)"), ("f_dok", "+ (c) dip savunması (>= 3)"),
                      ("f_stop", "+ (d) stop <= %10 (C_t ön eleme) = Y7")):
            m = m & b[c]; A.append({"ad": ad, **say(F[m])})
        out["Y7"] = {"asama": A, "tek": {c: int((~b[c]).sum()) for c in b}}
    return out


# ================================================================ 7) RAPOR
def yh_rapor(cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> str:
    cikti = cikti or YH_YOL["cikti"]
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    s = ["# YAPI_HEDEF — RAPOR", "", f"{J['surum']}. Koşu: " + "; ".join(f"{k['zaman_utc']} ({', '.join(k['denemeler'])})" for k in J["kos"]) +
         f". Ön kayıt: {J['kos'][0]['kapi'].get('onkayit_zaman', '?')} (git {J['kos'][0]['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}).", "",
         "## 1. ÖZET (etiket önceden yazılı kuralla)", "", "| Deneme | yön | ETİKET | karar hücreleri (ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26) |", "|---|---|---|---|"]
    for k in YH_DENEMELER:
        D = J["deneme"].get(k)
        if not D:
            continue
        kh = {(h["pazar"], h["donem"]): h for h in D["hucre"]}
        hc = " · ".join(f"{kh.get(tuple(x), {}).get('durum', '-')} (n {kh.get(tuple(x), {}).get('n', 0)}, KAT5 {_sy(kh.get(tuple(x), {}).get('h5_kat'))})"
                        for x in Y["karar"]["hucre_karar"])
        s.append(f"| {k} {D['ad']} | {'+' if D['yon'] > 0 else '-'} | **{D['etiket']}** | {hc} |")
    s += ["", f"Karar kuralı: {Y['karar']['tanim']}. Durum: {Y['etiket']['hucre']}.", "",
          "## 2. TANIM", "", f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- EŞ: {Y['kontrol']['es']}.",
          f"- PLASEBO: {Y['kontrol']['plasebo']}.", ""]
    for k in YH_DENEMELER:
        if k in J["deneme"]:
            D = Y["denemeler"][k]; s.append(f"- **{k} {D['ad']}**: {D['tanim']}.")
    s += ["", "## 3. OLAY SAYIMI", "", "| Deneme | Pazar | girdi | havuz dışı | tekil | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma denetimi |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in YH_DENEMELER:
        for p, x in J["sayim"].get(k, {}).items():
            s.append(f"| {k} | {p} | {x.get('girdi', 0)} | {x.get('havuz_disi', 0)} | {x.get('tekil', 0)} | {x.get('giris_stop_otesi', 0)} | {x.get('olc15_yok', 0)} | "
                     f"{x.get('es_az', 0)} | {x.get('plasebo_yok', 0)} | {J['gelecek_denetimi'].get(k, {}).get(p, '-')} TUTTU |")
    s += ["", "## 4. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95)", "",
          "| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop önce) olay / eş | plasebo P(+5) | plasebo KAT5 [%95] | şartlar n·kat·stop·plasebo | güç | DURUM |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in YH_DENEMELER:
        D = J["deneme"].get(k)
        if not D:
            continue
        for h in D["hucre"]:
            if not h.get("n"):
                s.append(f"| {k} | {h['pazar']} {h['donem']}{' (karar)' if h['karar_hucre'] else ''} | 0 | - | - | - | - | - | - | - | {h['durum']} |"); continue
            sart = "".join("✓" if h.get(a) else "·" for a in ("s_n", "s_kat", "s_stop", "s_plasebo"))
            s.append(f"| {k} | {h['pazar']} {h['donem']}{' (karar)' if h['karar_hucre'] else ''} | {h['n']} | {_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))} | "
                     f"{_sy(h.get('h5_kat'))} [{_sy(h.get('h5_alt'))}, {_sy(h.get('h5_ust'))}] | {_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))} | "
                     f"{_yz(h.get('pl_h5_p_ref'))} | {_sy(h.get('pl_h5_kat'))} [{_sy(h.get('pl_h5_alt'))}, {_sy(h.get('pl_h5_ust'))}] | {sart} | {_yz(h.get('guc'), 0)} | {h['durum']} |")
    s += ["", "## 5. OLASILIK TABLOSU (Cemal'in biçimi: olay / eş / taban; KAT = olay / eş [%95])", "",
          "| Deneme | Hücre | n | P(+5 önce) olay / eş / taban | KAT | P(+10 önce) olay / eş / taban | KAT | P(stop önce) olay / eş / taban | KAT |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in YH_DENEMELER:
        D = J["deneme"].get(k)
        if not D:
            continue
        for h in D["hucre"]:
            if not h.get("n"):
                continue
            c = []
            for g in ("h5", "h10", "st5"):
                c.append(f"{_yz(h.get(g + '_p_olay'))} / {_yz(h.get(g + '_p_ref'))} / {_yz(h.get('tb_' + g + '_p'))}")
                c.append(f"{_sy(h.get(g + '_kat'))} [{_sy(h.get(g + '_alt'))}, {_sy(h.get(g + '_ust'))}]")
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {h['n']} | " + " | ".join(c) + " |")
    s += ["", "## 6. BİLGİ: High ile hedef, iki yarı, takip stoplu getiri, çıkış", "",
          "| Deneme | Hücre | KAT5 High [%95] | KAT10 High | KAT5 yarı 1 / yarı 2 | getiri ort / medyan | kazanan | çıkış barı ort / med | çıkış türü | d medyan |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in YH_DENEMELER:
        D = J["deneme"].get(k)
        if not D:
            continue
        for h in D["hucre"]:
            if not h.get("n"):
                continue
            ct = ", ".join(f"{a} {b}" for a, b in sorted(h.get("cikis_tur", {}).items()))
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {_sy(h.get('h5H_kat'))} [{_sy(h.get('h5H_alt'))}, {_sy(h.get('h5H_ust'))}] | {_sy(h.get('h10H_kat'))} | "
                     f"{_sy(h.get('yari1_kat5'))} / {_sy(h.get('yari2_kat5'))} | {_yz(h.get('getiri_ort'))} / {_yz(h.get('getiri_med'))} | {_yz(h.get('getiri_kazanan'), 0)} | "
                     f"{_sy(h.get('cikis_bar_ort'), 1)} / {_sy(h.get('cikis_bar_med'), 0)} | {ct} | {_yz(h.get('dd_med'))} |")
    s += ["", "## 7. ÇOKLU KARŞILAŞTIRMA (bilgi; KAT5 bootstrap p, BH q 0,10, karar hücreleri)", "", "| Deneme | Hücre | p | BH geçer |", "|---|---|---|---|"]
    for b in J.get("bh", []):
        s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {_sy(b['p'], 3)} | {'evet' if b['bh_q10'] else 'hayır'} |")
    s += ["", "## 8. VERİ SINIRLARI", ""]
    for p, n_ in J.get("veri_not", {}).items():
        s.append(f"- {p}: " + "; ".join(n_))
    s += ["- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.",
          "- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı okunmalı (eş ve plasebo aynı evrenden).", "",
          "## 9. YENİDEN ÜRETİM (satır dosyasından iki hücre)", "", "```",
          "python - <<'EOF'", "import pandas as pd", "for d, p, q in [('Y1', 'ABD', '2023'), ('Y1', 'AVR', '2024-26')]:",
          "    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q) & x.h5.notna() & x.es_h5.notna()]",
          "    print(d, p, q, len(x), round(x.h5.sum() / x.es_h5.sum(), 4), round(x.st5.mean(), 4), round(x.es_st5.mean(), 4), round(x[x.pl_h5.notna()].h5.sum() / x.pl_h5.sum(), 4))",
          "EOF", "```", "",
          yh_kontrol_tablosu(), ""]
    metin = "\n".join(s)
    _yh_yaz(_yh_yol("rapor", cikti), metin, "rapor")
    return metin


def yh_rapor2(cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> str:
    """2. tur raporu (RAPOR_2.md): Y6 / Y7 / Y8 (+ Y8B bilgi), huni, hücre, olasılık, E5b, 1. turla yan yana. RAPOR.md'ye dokunmaz."""
    cikti = cikti or YH_YOL["cikti"]
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    den = [k for k in YH_DENEMELER_2 if k in J["deneme"]]
    if not den:
        raise YHHata("sonuc.json'da 2. tur denemesi yok")
    k2 = [k for k in J["kos"] if any(x in YH_DENEMELER_2 for x in k["denemeler"])][-1]
    kh = lambda D: {(h["pazar"], h["donem"]): h for h in D["hucre"]}  # noqa: E731
    s = ["# YAPI_HEDEF — RAPOR 2 (2. tur: Y6 / Y7 / Y8; Cemal'in değerlendirmesi E1-E7)", "",
         f"{J['surum']}. Koşu: {k2['zaman_utc']} ({', '.join(k2['denemeler'])}). Ön kayıt 2: {k2['kapi'].get('onkayit_zaman', '?')} "
         f"(git {k2['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}).", "",
         "## 1. SONUÇ (etiket önceden yazılı kuralla)", "",
         "| Deneme | ETİKET | karar hücreleri (ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26) |", "|---|---|---|"]
    for k in den:
        D = J["deneme"][k]; h_ = kh(D)
        hc = " · ".join(f"{h_.get(tuple(x), {}).get('durum', '-')} (n {h_.get(tuple(x), {}).get('n', 0)}, KAT5 {_sy(h_.get(tuple(x), {}).get('h5_kat'))})"
                        for x in Y["karar"]["hucre_karar"])
        s.append(f"| {k} {D['ad']}{' (BİLGİ, karar değil)' if D.get('bilgi') else ''} | **{D['etiket']}** | {hc} |")
    s += ["", f"Karar kuralı (1. turla aynı): {Y['karar']['tanim']}. Durum: {Y['etiket']['hucre']}.", "",
          "UYARI: şartlar Cemal'in 1. tur örnek grafiklerine (sonucu görülerek) yazdığı notlardan kuruldu; ölçüm bu örnekleri de içeren veride. "
          "TUTAR çıkan hücre bile ileri testle (kriz sonrası veri, aynı eşik) doğrulanmadan kural sayılmaz.", "",
          "## 2. 1. TURLA YAN YANA (karar hücreleri; P(+5 önce) olay / eş, KAT5, P(stop önce) olay / eş)", "",
          "| Hücre | " + " | ".join(x for x in ["Y1", "Y6", "Y8", "Y8B", "Y3", "Y7"] if x in J["deneme"]) + " |",
          "|---|" + "---|" * len([x for x in ["Y1", "Y6", "Y8", "Y8B", "Y3", "Y7"] if x in J["deneme"]])]
    for x in Y["karar"]["hucre_karar"] + Y["karar"]["hucre_bilgi"][:2]:
        c = []
        for k in ["Y1", "Y6", "Y8", "Y8B", "Y3", "Y7"]:
            if k not in J["deneme"]:
                continue
            h = kh(J["deneme"][k]).get(tuple(x), {})
            c.append(f"n {h.get('n', 0)}; {_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))}; KAT {_sy(h.get('h5_kat'))}; stop {_yz(h.get('st5_p_olay'))} / "
                     f"{_yz(h.get('st5_p_ref'))}")
        s.append(f"| {x[0]} {x[1]} | " + " | ".join(c) + " |")
    olcum = {}
    for k in den:
        olcum[k] = {(h["pazar"], h["donem"]): h.get("n", 0) for h in J["deneme"][k]["hucre"] if h["donem"] in ("2023", "2024-26")}
    s += ["", "## 3. HUNİ (taban sinyalinden şart şart; getirisiz)", ""]
    for k, alt in (("Y6", ["Y6", "Y8", "Y8B"]), ("Y7", ["Y7"])):
        if any(k in J.get("huni", {}).get(p, {}) for p in OC.OC_ESIK["pazar"]):
            s += [f"### {k} hunisi", ""] + _yh_huni_md(J["huni"], k, {a: olcum[a] for a in alt if a in olcum}) + [""]
    s += ["## 4. OLAY SAYIMI (ölçüm)", "",
          "| Deneme | Pazar | girdi | havuz dışı | tekil | stop_uzak (E5a giriş) | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma denetimi |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for p, x in J["sayim"].get(k, {}).items():
            s.append(f"| {k} | {p} | {x.get('girdi', 0)} | {x.get('havuz_disi', 0)} | {x.get('tekil', 0)} | {x.get('stop_uzak', 0)} | {x.get('giris_stop_otesi', 0)} | "
                     f"{x.get('olc15_yok', 0)} | {x.get('es_az', 0)} | {x.get('plasebo_yok', 0)} | {J['gelecek_denetimi'].get(k, {}).get(p, '-')} TUTTU |")
    s += ["", "## 5. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95)", "",
          "| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop önce) olay / eş | plasebo P(+5) | plasebo KAT5 [%95] | şartlar n·kat·stop·plasebo | güç | DURUM |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            et = f"{h['pazar']} {h['donem']}{' (karar)' if h['karar_hucre'] else ''}"
            if not h.get("n"):
                s.append(f"| {k} | {et} | 0 | - | - | - | - | - | - | - | {h['durum']} |"); continue
            sart = "".join("✓" if h.get(a) else "·" for a in ("s_n", "s_kat", "s_stop", "s_plasebo"))
            s.append(f"| {k} | {et} | {h['n']} | {_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))} | {_sy(h.get('h5_kat'))} [{_sy(h.get('h5_alt'))}, "
                     f"{_sy(h.get('h5_ust'))}] | {_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))} | {_yz(h.get('pl_h5_p_ref'))} | {_sy(h.get('pl_h5_kat'))} "
                     f"[{_sy(h.get('pl_h5_alt'))}, {_sy(h.get('pl_h5_ust'))}] | {sart} | {_yz(h.get('guc'), 0)} | {h['durum']} |")
    s += ["", "## 6. OLASILIK TABLOSU (Cemal'in biçimi: olay / eş / taban; KAT = olay / eş [%95])", "",
          "| Deneme | Hücre | n | P(+5 önce) olay / eş / taban | KAT | P(+10 önce) olay / eş / taban | KAT | P(stop önce) olay / eş / taban | KAT |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("n"):
                continue
            c = []
            for g in ("h5", "h10", "st5"):
                c.append(f"{_yz(h.get(g + '_p_olay'))} / {_yz(h.get(g + '_p_ref'))} / {_yz(h.get('tb_' + g + '_p'))}")
                c.append(f"{_sy(h.get(g + '_kat'))} [{_sy(h.get(g + '_alt'))}, {_sy(h.get(g + '_ust'))}]")
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {h['n']} | " + " | ".join(c) + " |")
    s += ["", "## 7. BİLGİ: E5b stop varyantı (stop0b = max(hat x 0,98, giriş x 0,95); olay / eş aynı d_b; karar değil)", "",
          "| Deneme | Hücre | n | d_b medyan | P(+5 önce) olay / eş | KAT5 [%95] | P(+10 önce) olay / eş | P(stop önce) olay / eş | KAT stop |", "|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("b_n"):
                continue
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {h['b_n']} | {_yz(h.get('b_dd_med'))} | {_yz(h.get('b_h5_p_olay'))} / {_yz(h.get('b_h5_p_ref'))} | "
                     f"{_sy(h.get('b_h5_kat'))} [{_sy(h.get('b_h5_alt'))}, {_sy(h.get('b_h5_ust'))}] | {_yz(h.get('b_h10_p_olay'))} / {_yz(h.get('b_h10_p_ref'))} | "
                     f"{_yz(h.get('b_st5_p_olay'))} / {_yz(h.get('b_st5_p_ref'))} | {_sy(h.get('b_st5_kat'))} |")
    s += ["", "## 8. BİLGİ: High ile hedef, iki yarı, takip stoplu getiri, çıkış", "",
          "| Deneme | Hücre | KAT5 High [%95] | KAT10 High | KAT5 yarı 1 / yarı 2 | getiri ort / medyan | kazanan | çıkış barı ort / med | çıkış türü | d medyan |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("n"):
                continue
            ct = ", ".join(f"{a} {b}" for a, b in sorted(h.get("cikis_tur", {}).items()))
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {_sy(h.get('h5H_kat'))} [{_sy(h.get('h5H_alt'))}, {_sy(h.get('h5H_ust'))}] | {_sy(h.get('h10H_kat'))} | "
                     f"{_sy(h.get('yari1_kat5'))} / {_sy(h.get('yari2_kat5'))} | {_yz(h.get('getiri_ort'))} / {_yz(h.get('getiri_med'))} | {_yz(h.get('getiri_kazanan'), 0)} | "
                     f"{_sy(h.get('cikis_bar_ort'), 1)} / {_sy(h.get('cikis_bar_med'), 0)} | {ct} | {_yz(h.get('dd_med'))} |")
    s += ["", "## 9. ÇOKLU KARŞILAŞTIRMA (bilgi; Y6 / Y7 / Y8 karar hücreleri KAT5 bootstrap p, BH q 0,10)", "", "| Deneme | Hücre | p | BH geçer |", "|---|---|---|---|"]
    for b in J.get("bh_tur2", []):
        s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {_sy(b['p'], 3)} | {'evet' if b['bh_q10'] else 'hayır'} |")
    s += ["", "## 10. VERİ SINIRLARI", ""]
    for p, n_ in J.get("veri_not", {}).items():
        s.append(f"- {p}: " + "; ".join(n_))
    s += ["- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.",
          "- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı (eş ve plasebo aynı evrenden).",
          "- Sonradan bilgi: şartlar 1. tur örneklerinin sonucu görülerek yazıldı (ön kayıt 2 UYARI).", "",
          "## 11. YENİDEN ÜRETİM (satır dosyasından iki hücre)", "", "```",
          "python - <<'EOF'", "import pandas as pd", "for d, p, q in [('Y6', 'ABD', '2024-26'), ('Y7', 'ABD', '2023')]:",
          "    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q) & x.h5.notna() & x.es_h5.notna()]",
          "    print(d, p, q, len(x), round(x.h5.sum() / x.es_h5.sum(), 4), round(x.st5.mean(), 4), round(x.es_st5.mean(), 4), round(x[x.pl_h5.notna()].h5.sum() / x.pl_h5.sum(), 4))",
          "EOF", "```", "", "Satır dosyası 5 MB'ı aşarsa scratch yolundadır (sonuc.json 'satir_dosya').", "",
          yh_kontrol_tablosu(YH_KONTROL_2), ""]
    metin = "\n".join(s)
    _yh_yaz(_yh_yol("rapor2", cikti), metin, "rapor 2")
    return metin


# ================================================================ 8) 3. TUR (Y9 / Y9b / Y9c / Y9d; YAPI_HEDEF_3_IS_TANIMI.md)
_Y9_OZ = ["F1", "F11", "F15", "F17"]
_YH_OZ_ONB: Dict[str, Any] = {}
_YH_DONEM_DIS = "2016-22"

YH_KONTROL_3: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / "
                   "takip / 15 bar); EK kontrol 'konum eşli KAT' (yh_konum_es_olc): aynı eşler VE eşin F15'i olayın çeyreğinde (dipte olmanın "
                   "momentum kovasıyla karışması ayrılır); eşlerin F15 dağılımı her hücrede raporlanır; güç tablosu 1. turunki (aynı kural)"),
    "K2": ("EVET", "F1 / F11 / F15 / F17 yalnız [.., t] (GOZ_ETIKET prefix denetimi + bu koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, "
                   "Y1 sinyali ve dört özellik yeniden hesaplanır, dosyayla göreli 1e-5 aynı olmalı, yoksa DURUR: yh_gelecek_denetimi); F15 C_t'yi "
                   "içerir (sinyal günü kapanışı, giriş t+1 açılış); eşin F15'i giriş gününden önceki son geçerli barında; hedef / stop yalnız giriş "
                   "ve sonrası"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (OC.oc_veri_hazirla + SY.sy_veri_hazirla); F15 paneli hissenin kendi geçerli kapanışlarıyla (120 bar)"),
    "K4": ("EVET", "Y9* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz "
                   "dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan"),
    "K5": ("EVET", "giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı"),
    "K6": ("EVET", "aynı V_*.pkl tek kip; F15 / F17 / F11 oran, F1 sayı (birimden bağımsız); AVR yerel para"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Y9) olaylarda batan hisse "
                   "eksikliği daha büyük olabilir (dipteki hissenin batma olasılığı yüksek) -> Y9 hedef payı ayrıca yukarı yanlı okunur; eş ve "
                   "plasebo aynı evrenden; rapora yazılır"),
    "K8": ("EVET", "huni ön kayıtta (getirisiz); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; iki yarı KAT (TERS kuralında "
                   "şart); Y9 / Y9b / Y9c x 4 karar hücresi BH q 0,10 (bilgi, ayrı aile 'bh_tur3'); bakılmış hücreler işaretli, etiket en fazla "
                   "EMARE; dış sınama 2016-22 ABD / AVR ayrı satır; BIST ayrı başlık; küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_3.md: YH_ESIK sha (yeni), ESIK_TUR2_SHA (= ON_KAYIT_2.md YH_ESIK_SHA: Y1-Y8B eşikleri aynen), ESIK_TUR1_SHA, kod / OC / "
                   "S6 / FV / güç / Y2 sha, OZELLIK_SHA (ozellik_Y1.csv.gz), Y1_OLAY_SHA (regresyon dosyası); yh_kapi(tur 3) hepsini + git "
                   "kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit, ölçüm ikinci commit; §2 dürüstlük notu aynen: ABD / AVR 2023 ve "
                   "2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldü (bakılmış), etiket en fazla EMARE"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve GOZ_ETIKET özellik dosyası (sha mühürlü; 5 olay / deneme x pazar "
                          "ham veriden yeniden hesaplanıp karşılaştırılır)"),
    "K11": ("EVET", "olay_Y9*.csv.gz satır dosyaları; RAPOR_3.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; Y1 regresyonu: "
                    "ölçülen her Y9* satırı olay_Y1.csv.gz satırına eşit (DURUR) ve Y1 ABD 2023 n 2040 KAT5 0,9752 sonuc.json'da aynen"),
    "K12": ("EVET", "etiket yalnız YH_ESIK Y9 'tur3_kural' ile (en fazla EMARE; TERS EMARE iki yönlü kural); Y9d 'bilgi'; 'iz değil' yazılmaz; sayı ve "
                    "yorum ayrı; bakılmış hücre sonuçları 'bağımsız kanıt' diye sunulmaz"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y9 önekli); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar "
                    "taraması; push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


def _yh_kural3(Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    return Y["denemeler"]["Y9"]["tur3_kural"]


def yh_ozellik_oku(yol: Optional[str] = None) -> pd.DataFrame:
    """ozellik_Y1.csv.gz (GOZ_ETIKET aşama A; pazar, sembol, tarih, durum, F1-F18) -> DataFrame. Yoksa / bozuksa YHHata (3. tur DURUR)."""
    yol = yol or YH_YOL["ozellik"]
    if not os.path.exists(yol):
        raise YHHata(f"özellik dosyası yok: {yol} (GOZ_ETIKET aşama A çıktısı; 3. tur DURDU)")
    sha = _yh_sha_dosya(yol)
    if _YH_OZ_ONB.get("yol") == yol and _YH_OZ_ONB.get("sha") == sha:
        return _YH_OZ_ONB["F"]
    try:
        F = pd.read_csv(yol, parse_dates=["tarih"])
    except Exception as ex:
        raise YHHata(f"özellik dosyası okunamadı: {yol}: {ex}")
    eksik = [c for c in ["pazar", "sembol", "tarih"] + _Y9_OZ if c not in F.columns]
    if eksik:
        raise YHHata(f"özellik dosyasında sütun yok: {eksik}")
    if F.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata("özellik dosyasında aynı (pazar, sembol, tarih) iki kez")
    _YH_OZ_ONB.clear(); _YH_OZ_ONB.update({"yol": yol, "sha": sha, "F": F})
    return F


def yh_y9_maske(F: pd.DataFrame, deneme: str, E: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    """Y9 / Y9b / Y9c / Y9d seçimi (F1, F11, F15, F17 sütunlu çerçeve). NaN şart tutmaz."""
    if deneme not in YH_DENEMELER_3:
        raise YHHata(f"3. tur deneme değil: {deneme}")
    D = E["denemeler"][deneme]
    if not len(F):
        return np.zeros(0, bool)
    f15 = F.F15.to_numpy(float)
    with np.errstate(invalid="ignore"):
        if deneme in ("Y9", "Y9b"):
            m = (f15 <= D["F15_ust"]) & (F.F17.to_numpy(float) <= D["F17_ust"])
            if deneme == "Y9b":
                m &= (F.F1.to_numpy(float) >= D["F1_min"]) & (F.F11.to_numpy(float) >= D["F11_min"])
        elif deneme == "Y9c":
            m = f15 >= D["F15_alt"]
        else:
            a, b = D["F15_ara"]; m = (f15 > a) & (f15 < b)
    return np.asarray(m, bool)


def yh_ceyrek(f: np.ndarray, Y: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    """F15 çeyreği: 0 = [0, 0,25], 1 = (0,25, 0,50], 2 = (0,50, 0,75), 3 = [0,75, 1]; NaN -> -1. Değer 9 ondalığa yuvarlanır (kayan nokta
    gürültüsü: tam 0,75 olan konum panelde 0,7499999999 çıkabilir; dosya 6 anlamlı basamak)."""
    c = _yh_kural3(Y)["ceyrek"]; f = np.round(np.asarray(f, float), 9); q = np.full(f.shape, -1, int)
    with np.errstate(invalid="ignore"):
        q[f <= c[0]] = 0
        q[(f > c[0]) & (f <= c[1])] = 1
        q[(f > c[1]) & (f < c[2])] = 2
        q[f >= c[2]] = 3
    return q


def yh_y9_ozellik(df: pd.DataFrame, tarihler: List[pd.Timestamp], E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """F1, F11, F15, F17 (GOZ_ETIKET.ge_ozellik_bar ile aynı formül) Y1 sinyal günleri için; t = i'de yalnız [0..i] okunur."""
    Pz = E["denemeler"]["Y9"]["ozellik_prm"]
    d = _yh_hazir(df); T = S6.s6_taban(d, None)
    durum = T["durum"].to_numpy(object); al = T["al"].to_numpy(bool)
    kal, ksol, bas = T["kutu_alt"].to_numpy(float), T["kutu_sol_i"].to_numpy(float), T["bas_i"].to_numpy(float)
    dip, tavan = T["dip"].to_numpy(float), T["tavan"].to_numpy(float)
    L, C = d.Low.to_numpy(float), d.Close.to_numpy(float)
    pos = d.index.get_indexer(pd.DatetimeIndex(pd.to_datetime(list(tarihler))))
    if (pos < 0).any():
        raise YHHata("Y9 özellik: sinyal günü veride yok")
    k, q = int(Pz["konum_gun"]), int(Pz["dusus_gun"]); sat = []
    for i in pos:
        if i < 1 or not al[i]:
            raise YHHata(f"Y9 özellik: bar {i} S6 'al' günü değil")
        if durum[i] == "AL":
            hat, sol = float(kal[i]), ksol[i]
        else:
            hat, sol = float(dip[i - 1]), bas[i - 1]
        tav = float(tavan[i - 1])
        if not (np.isfinite(sol) and 0 <= int(sol) < i and np.isfinite(hat) and hat > 0):
            raise YHHata(f"Y9 özellik: bar {i} bölge / hat tanımsız")
        sol = int(sol); Lz = L[sol:i]
        f1 = float(np.sum(Lz <= hat * (1 + Pz["hat_bant"])))
        f11 = float(C[i] / tav - 1) if np.isfinite(tav) and tav > 0 else np.nan
        c120 = C[max(0, i - k + 1):i + 1]; lo, hi = float(c120.min()), float(c120.max())
        f15 = float((C[i] - lo) / (hi - lo)) if len(c120) == k and hi > lo else np.nan
        f17 = float(C[sol] / np.max(C[sol - q:sol]) - 1) if sol >= q else np.nan
        sat.append({"F1": f1, "F11": f11, "F15": f15, "F17": f17})
    return pd.DataFrame(sat, columns=_Y9_OZ)


def yh_y9_hisse(df: pd.DataFrame, deneme: str, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Tek hisse Y9*: Y1 sinyalleri + yeniden hesaplanan özellikler + seçim. NOT: OC tekilleştirmesi YOK (pazar düzeyinde Y9* = Y1 OLAY alt
    kümesi, özellikler dosyadan); bu fonksiyon geleceğe bakma testi ve birim testler içindir."""
    X1, _ = yh_s6_hisse(df, E)
    if not len(X1):
        return pd.DataFrame(columns=list(X1.columns) + _Y9_OZ)
    Z = pd.concat([X1.reset_index(drop=True), yh_y9_ozellik(df, list(X1.tarih), E)], axis=1)
    return Z[yh_y9_maske(Z, deneme, E)].reset_index(drop=True)


def yh_sinyaller3(Vd: Dict[str, Any], pazar: str, denemeler: List[str], islem: int = 1, E: Dict[str, Any] = YH_ESIK,
                  P: Optional[Dict[str, Any]] = None, ozellik: Optional[str] = None) -> Dict[str, Any]:
    """3. tur: Y1 sinyalleri (1. tur kodu) ∩ özellik dosyası satırları (= Y1 OLAYLARI) -> '_Y9F' (bayraklı) + deneme alt kümeleri.
    Regresyon: pazarın özellik satırlarının hepsi Y1 sinyalinde olmalı; P verilirse özellik (sembol, tarih) kümesi = OC sonrası Y1 olay kümesi."""
    den = [k for k in denemeler if k in YH_DENEMELER_3]
    if len(den) != len(denemeler):
        raise YHHata(f"yh_sinyaller3 yalnız 3. tur: {denemeler}")
    S1 = yh_sinyaller(Vd, pazar, ["Y1"], islem, E)["Y1"].copy()
    S1["tarih"] = pd.to_datetime(S1.tarih)
    Fo = yh_ozellik_oku(ozellik)
    Fp = Fo[Fo.pazar == pazar][["sembol", "tarih"] + _Y9_OZ].copy()
    X = S1.merge(Fp, on=["sembol", "tarih"], how="inner", validate="one_to_one")
    rap: Dict[str, Any] = {"y1_sinyal": int(len(S1)), "ozellik_satir": int(len(Fp)), "eslesen": int(len(X))}
    if len(X) != len(Fp):
        raise YHHata(f"3. tur regresyon: {pazar} {len(Fp) - len(X)} özellik satırı şimdiki Y1 sinyallerinde yok -> DURDU")
    if P is not None and len(S1):
        Z, _ = OC.oc_olay_hazirla(S1[["sembol", "tarih", "pazar"]], P)
        k1 = set(zip(Z.sembol, pd.to_datetime(Z.tarih))); k2 = set(zip(Fp.sembol, Fp.tarih))
        rap["y1_olay"] = int(len(Z))
        if k1 != k2:
            raise YHHata(f"3. tur regresyon: {pazar} özellik kümesi ({len(k2)}) != Y1 olay kümesi ({len(k1)}) -> DURDU")
    out: Dict[str, Any] = {"_Y9F": X.sort_values(["sembol", "tarih"]).reset_index(drop=True), "_Y9R": rap}
    for k in den:
        out[k] = out["_Y9F"][yh_y9_maske(out["_Y9F"], k, E)].reset_index(drop=True)
    return out


def _yh_say_getirisiz(X: pd.DataFrame, P: Dict[str, Any]) -> Dict[str, Any]:
    if not len(X):
        return {"sinyal": 0, "sinyal_donem": {}, "olay_donem": {}}
    sg = pd.Series(OC._oc_donem(pd.to_datetime(X.tarih), OC.OC_ESIK)).value_counts().to_dict()
    Z, _ = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P)
    ol = Z.donem.value_counts().to_dict() if len(Z) else {}
    return {"sinyal": int(len(X)), "sinyal_donem": {a: int(b) for a, b in sg.items() if a}, "olay_donem": {a: int(b) for a, b in ol.items() if a}}


def yh_huni3(S: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """GETİRİSİZ huni: Y1 olayı -> F15 <= 0,25 -> F17 <= -0,20 (= Y9) -> F1 >= 3 -> F11 >= 0,01 (= Y9b); ayrıca Y9c, Y9d, NaN sayıları."""
    F = S["_Y9F"]; D, Db = E["denemeler"]["Y9"], E["denemeler"]["Y9b"]
    if not len(F):
        return {"Y9": {"asama": [], "tek": {}}}
    f15, f17, f1, f11 = (F[c].to_numpy(float) for c in ("F15", "F17", "F1", "F11"))
    with np.errstate(invalid="ignore"):
        m1 = f15 <= D["F15_ust"]; m2 = m1 & (f17 <= D["F17_ust"]); m3 = m2 & (f1 >= Db["F1_min"]); m4 = m3 & (f11 >= Db["F11_min"])
    A = [{"ad": "Y1 olayı (özellik satırı)", **_yh_say_getirisiz(F, P)},
         {"ad": "+ F15 <= 0,25 (dipte)", **_yh_say_getirisiz(F[m1], P)},
         {"ad": "+ F17 <= -0,20 (düşüş sonrası) = Y9", **_yh_say_getirisiz(F[m2], P)},
         {"ad": "+ F1 >= 3 (hat net)", **_yh_say_getirisiz(F[m3], P)},
         {"ad": "+ F11 >= 0,01 (gerçek kırılım) = Y9b", **_yh_say_getirisiz(F[m4], P)},
         {"ad": "(ayrı) F15 >= 0,75 TEPEDE = Y9c", **_yh_say_getirisiz(F[yh_y9_maske(F, "Y9c", E)], P)},
         {"ad": "(ayrı) 0,25 < F15 < 0,75 ORTA = Y9d", **_yh_say_getirisiz(F[yh_y9_maske(F, "Y9d", E)], P)}]
    with np.errstate(invalid="ignore"):
        tek = {"F15_NaN": int(np.isnan(f15).sum()), "F17_NaN (dipte)": int((m1 & np.isnan(f17)).sum()), "F17 > -0,20 (dipte)": int((m1 & (f17 > D["F17_ust"])).sum())}
    return {"Y9": {"asama": A, "tek": tek}}


def yh_f15_panel(P: Dict[str, Any], Vd: Dict[str, Any], E: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    """Panel takviminde (giriş günü d x hisse) F15: hissenin d'den ÖNCEKİ son geçerli barında, t dahil son 120 geçerli kapanışla
    (C_t - min) / (max - min); 120 bar yok ya da aralık 0 -> NaN. Olayın t'si = giriş gününden önceki son geçerli bar (aynı bilgi anı)."""
    k = int(E["denemeler"]["Y9"]["ozellik_prm"]["konum_gun"]); idx = P["tarih"]; S = P["sembol"]
    out = np.full((len(idx), len(S)), np.nan)
    for j, s in enumerate(S):
        c = Vd["V"][s]["Close"].astype(float)
        lo = c.rolling(k, min_periods=k).min(); hi = c.rolling(k, min_periods=k).max()
        with np.errstate(invalid="ignore", divide="ignore"):
            pz = ((c - lo) / (hi - lo)).where(hi > lo)
        a = pz.reindex(idx, method="ffill").to_numpy(float)
        out[1:, j] = a[:-1]
    return out


_YH_IS_K: Dict[str, Any] = {}


def _yh_konum_isci(Zp: pd.DataFrame) -> pd.DataFrame:
    return yh_konum_es_olc(_YH_IS_K["P"], _YH_IS_K["Cl"], Zp, _YH_IS_K["F15p"], 1, _YH_IS_K["Y"])


def yh_konum_es_olc(P: Dict[str, Any], Cl: np.ndarray, Z: pd.DataFrame, F15p: np.ndarray, islem: int = 1, Y: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """KONUM EŞLİ KAT girdisi: 1. turun eşleri (aynı gün, aynı kova, havuzda, ölçülebilir, aynı d) içinden F15'i olayın çeyreğinde olanlar,
    AYNI yh_sim kuralı. Ekler: q_olay (dosya F15), f15_panel / q_panel (panel; uyum denetimi), k_es_h5 / k_es_h10 / k_es_st5, k_n_es,
    es_f15_ort, es_f15_med, es_ayni_ceyrek (1. tur eşlerinin olayla aynı çeyrekte payı)."""
    global _YH_IS_K
    kol = ["q_olay", "f15_panel", "q_panel", "k_es_h5", "k_es_h10", "k_es_st5", "k_n_es", "es_f15_ort", "es_f15_med", "es_ayni_ceyrek"]
    if islem > 1 and len(Z) > 200:
        import multiprocessing as mp
        _YH_IS_K = {"P": P, "Cl": Cl, "F15p": F15p, "Y": Y}
        try:
            parca = np.array_split(np.arange(len(Z)), islem * 4)
            with mp.get_context("fork").Pool(islem) as havuz:
                R_ = havuz.map(_yh_konum_isci, [Z.iloc[p] for p in parca if len(p)])
        finally:
            _YH_IS_K = {}
        return pd.concat(R_, ignore_index=True)
    R = int(Y["olcu"]["pencere_azami"]); me = Y["kontrol"]["min_es"]
    Op, Hi, Lo, Hc, ok = P["Op"], P["Hi"], P["Lo"], P["H"], P["ok"]
    out = {k: [] for k in kol}
    qo_all = yh_ceyrek(Z.F15.to_numpy(float), Y)
    for q_, r in enumerate(Z.itertuples(index=False)):
        sat = dict.fromkeys(kol, np.nan); d, j, s = int(r.d), int(r.j), int(r.yon); qo = int(qo_all[q_])
        sat["q_olay"] = qo; sat["f15_panel"] = float(F15p[d, j]); sat["q_panel"] = int(yh_ceyrek(np.array([F15p[d, j]]), Y)[0])
        dd = float(r.dd) if np.isfinite(r.dd) else np.nan
        if bool(r.olc) and np.isfinite(dd) and dd > 0:
            havuz = np.flatnonzero(ok[d])
            if not ok[d, j]:
                havuz = np.r_[havuz, j]
            Ek = Op[d, havuz]; stk = Ek * (1 - s * dd); stk[havuz == j] = float(r.stop0)
            Sm = yh_sim(_yh_pencere(Cl, d, R, havuz), _yh_pencere(Hi, d, R, havuz), _yh_pencere(Lo, d, R, havuz), Ek, stk, s, Y)
            pj = int(np.flatnonzero(havuz == j)[0])
            es = Sm["olc"].copy(); es[pj] = False; es &= (Hc[d, havuz] == Hc[d, j])
            fq = F15p[d, havuz]; qq = yh_ceyrek(fq, Y)
            if es.sum():
                fe = fq[es]; fe = fe[np.isfinite(fe)]
                sat["es_f15_ort"] = float(fe.mean()) if len(fe) else np.nan
                sat["es_f15_med"] = float(np.median(fe)) if len(fe) else np.nan
                sat["es_ayni_ceyrek"] = float(np.mean(qq[es] == qo)) if qo >= 0 else np.nan
            ke = es & (qq == qo) & (qo >= 0)
            sat["k_n_es"] = int(ke.sum())
            if ke.sum() >= me:
                for k in ("h5", "h10", "st5"):
                    sat["k_es_" + k] = float(np.mean(Sm[k][ke]))
        for k in kol:
            out[k].append(sat[k])
    Z = Z.copy()
    for k in kol:
        Z[k] = out[k]
    return Z


_YH_REG_KOL = ["h5", "h10", "st5", "es_h5", "es_h10", "es_st5", "n_es", "tb_h5", "getiri"]


def yh_y1_regresyon(Z: pd.DataFrame, O1: pd.DataFrame) -> Dict[str, Any]:
    """Ölçülen Y9* satırları olay_Y1.csv.gz'deki aynı (pazar, sembol, tarih) satırına eşit olmalı (göreli 1e-4, NaN = NaN); değilse YHHata."""
    if not len(Z):
        return {"n": 0, "esit": True}
    a = Z[["pazar", "sembol", "tarih", "giris"] + _YH_REG_KOL].copy(); a["tarih"] = pd.to_datetime(a.tarih)
    m = a.merge(O1[["pazar", "sembol", "tarih", "giris"] + _YH_REG_KOL], on=["pazar", "sembol", "tarih"], how="left", suffixes=("", "_y1"),
                indicator=True, validate="one_to_one")
    yok = int((m._merge != "both").sum())
    if yok:
        raise YHHata(f"Y1 regresyonu: {yok} Y9* olayı olay_Y1.csv.gz'de yok -> DURDU")
    fark = {}
    if (pd.to_datetime(m.giris) != pd.to_datetime(m.giris_y1)).any():
        fark["giris"] = int((pd.to_datetime(m.giris) != pd.to_datetime(m.giris_y1)).sum())
    for c in _YH_REG_KOL:
        x = m[c].to_numpy(float); y = m[c + "_y1"].to_numpy(float)
        bad = ~(np.isclose(x, y, rtol=1e-4, atol=1e-6, equal_nan=True))
        if bad.any():
            fark[c] = int(bad.sum())
    if fark:
        raise YHHata(f"Y1 regresyonu TUTMADI (sütun: farklı satır) {fark} -> DURDU")
    return {"n": int(len(m)), "esit": True, "kol": _YH_REG_KOL}


def yh_hucre_konum(X: pd.DataFrame, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Hücre: konum eşli KAT (h5 / h10 / st5) + eşlerin F15 dağılımı (bilgi) + çeyrek uyumu."""
    out: Dict[str, Any] = {"k_n": 0}
    if not len(X) or "k_es_h5" not in X.columns:
        return out
    g = X[X.h5.notna() & X.k_es_h5.notna()].sort_values("giris")
    ay = pd.to_datetime(g.giris).dt.to_period("M").astype(str).to_numpy() if len(g) else np.array([], dtype=object)
    out["k_n"] = int(len(g))
    for k in ("h5", "h10", "st5"):
        r = yh_kat(g[k].to_numpy(float), g["k_es_" + k].to_numpy(float), ay, Y)
        for a_, v in r.items():
            if a_ != "n":
                out[f"k_{k}_{a_}"] = v
    gg = X[X.h5.notna() & X.es_h5.notna()]
    if len(gg):
        out["olay_f15_ort"] = float(np.nanmean(gg.F15.to_numpy(float)))
        out["es_f15_ort"] = float(np.nanmean(gg.es_f15_ort.to_numpy(float)))
        out["es_f15_med"] = float(np.nanmedian(gg.es_f15_med.to_numpy(float)))
        out["es_ayni_ceyrek"] = float(np.nanmean(gg.es_ayni_ceyrek.to_numpy(float)))
        qv = gg[gg.q_olay >= 0]
        out["ceyrek_uyum"] = float((qv.q_olay == qv.q_panel).mean()) if len(qv) else np.nan
        out["k_es_az"] = int((gg.k_es_h5.isna()).sum())
    return out


def yh_ters(h: Dict[str, Any], Y: Dict[str, Any] = YH_ESIK) -> bool:
    """Hücre TERS = n >= 30 VE KAT5 %95 üst uç < 1 VE iki yarı KAT5 < 1."""
    f = lambda x: x is not None and np.isfinite(x)  # noqa: E731
    return bool(h.get("n", 0) >= Y["karar"]["n_esik"] and f(h.get("h5_ust")) and h["h5_ust"] < 1 and f(h.get("yari1_kat5"))
                and h["yari1_kat5"] < 1 and f(h.get("yari2_kat5")) and h["yari2_kat5"] < 1)


def yh_etiket3(H_: List[Dict[str, Any]], kural: str, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """3. tur etiketi (YH_ESIK Y9 tur3_kural 'etiket'): en fazla EMARE (bakılmış hücreler); dış sınama; iki yönlü TERS EMARE."""
    K = _yh_kural3(Y); hk = {(h["pazar"], h["donem"]): h for h in H_}
    karar = [tuple(x) for x in Y["karar"]["hucre_karar"]]; dis = [tuple(x) for x in K["dis_sinama"]]
    tutan = [f"{p} {q}" for p, q in karar if hk.get((p, q), {}).get("tutar")]
    dis_tutar = all(hk.get(x, {}).get("tutar") for x in dis)
    ters_k = [f"{p} {q}" for p, q in karar if hk.get((p, q), {}).get("ters")]
    dis_ters = all(hk.get(x, {}).get("ters") for x in dis)
    if kural.startswith("İZ") or kural.startswith("EMARE"):
        et = "EMARE (dış sınama tuttu)" if dis_tutar else f"EMARE (bakılmış hücreler: {', '.join(tutan)})"
    else:
        et = kural
    if len(ters_k) >= 2:
        te = "TERS EMARE (dış sınama tuttu)" if dis_ters else f"TERS EMARE (bakılmış hücreler: {', '.join(ters_k)})"
    else:
        te = f"TERS YOK (TERS karar hücresi {len(ters_k)}" + (f": {ters_k[0]}" if ters_k else "") + ")"
    return {"etiket": et, "ters_etiket": te, "dis_sinama_tutar": bool(dis_tutar), "dis_sinama_ters": bool(dis_ters), "tutan_karar": tutan,
            "ters_karar": ters_k}


def yh_sonuc_deneme3(Ol: pd.DataFrame, deneme: str, tablo: Optional[Dict[str, Any]], Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """1. tur hücre / etiket kuralı (yh_sonuc_deneme) + konum eşli KAT + TERS + bakılmış / dış sınama işareti + 3. tur etiketi."""
    out = yh_sonuc_deneme(Ol, deneme, tablo, Y); K = _yh_kural3(Y)
    for h in out["hucre"]:
        x = Ol[(Ol.pazar == h["pazar"]) & (Ol.donem == h["donem"])] if len(Ol) else Ol
        h.update(yh_hucre_konum(x, Y))
        h["ters"] = yh_ters(h, Y)
        h["bakilmis"] = [h["pazar"], h["donem"]] in K["bakilmis"]
        h["dis_sinama"] = [h["pazar"], h["donem"]] in K["dis_sinama"]
    out["etiket_kural"] = out["etiket"]
    e3 = yh_etiket3(out["hucre"], out["etiket_kural"], Y)
    out.update(e3)
    return out


def yh_sayim3(veri: Optional[str] = None, islem: int = 1, ozellik: Optional[str] = None) -> Dict[str, Any]:
    """3. tur GETİRİSİZ sayım: huni + deneme başına OC olayı (dönem) + Y1 eşleşmesi. Hedef / stop / eş / konum eş HESAPLANMAZ."""
    out: Dict[str, Any] = {"huni": {}, "deneme": {}, "eslesme": {}}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); P = OC.oc_panel(Vd)
        S = yh_sinyaller3(Vd, p, YH_DENEMELER_3, islem, P=P, ozellik=ozellik)
        out["huni"][p] = yh_huni3(S, P); out["eslesme"][p] = S["_Y9R"]
        for k in YH_DENEMELER_3:
            X = S[k]
            Z, say = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P) if len(X) else (pd.DataFrame(), {})
            out["deneme"].setdefault(k, {})[p] = {"olay": {a: int(b) for a, b in (Z.donem.value_counts().to_dict() if len(Z) else {}).items() if a},
                                                  "hisse": int(X.sembol.nunique()) if len(X) else 0, "sayim": {a: int(b) for a, b in say.items()}}
        yhlog.info("sayım (3. tur) %s tamam", p)
        del Vd, P, S
    return out


def _yh_is_tanimi3_s2(yol: Optional[str] = None) -> str:
    """İş tanımı §2 (GEREKÇE ve DÜRÜSTLÜK NOTU) metni aynen; yoksa YHHata."""
    yol = yol or YH_YOL["is_tanimi3"]
    if not os.path.exists(yol):
        raise YHHata(f"3. tur iş tanımı yok: {yol}")
    m = re.search(r"(?ms)^## 2\. GEREKÇE ve DÜRÜSTLÜK NOTU[^\n]*\n(.*?)(?=^## 3\.)", open(yol, encoding="utf-8").read())
    if not m or not m.group(1).strip():
        raise YHHata("iş tanımında §2 dürüstlük notu bulunamadı")
    return m.group(1).strip()


def yh_onkayit3_metni(say: Dict[str, Any], sha: Dict[str, str], git2: Dict[str, str], git_is: Dict[str, str], t1: str, t2: str,
                      s2: str) -> str:
    Y = YH_ESIK; K = _yh_kural3(Y)
    s = ["# YAPI_HEDEF — ÖN KAYIT 3 (3. tur: Y9 / Y9b / Y9c + Y9d bilgi; konum eşli KAT)", "",
         YH_SURUM + "; 3. tur eklendi (YAPI_HEDEF_3_IS_TANIMI.md)", "",
         f"- YH_ESIK_SHA: `{sha['esik']}` (3. tur denemeleri dahil)",
         f"- ESIK_TUR2_SHA: `{t2}` (YH_ESIK'ten Y9-Y9d çıkarılınca; = ON_KAYIT_2.md YH_ESIK_SHA: Y1-Y8B eşikleri AYNEN)",
         f"- ESIK_TUR1_SHA: `{t1}` (Y6-Y9d çıkarılınca; = ON_KAYIT.md YH_ESIK_SHA = güç tablosu)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)",
         f"- FV_KOD_SHA: `{sha['fv']}` (FITIL_V2.py)", f"- GUC_SHA: `{sha['guc']}` ({YH_DOSYA['guc_json']}; 1. turun güç tablosu, aynı kural)",
         f"- Y2_OLAY_SHA: `{sha['y2']}` (değişmedi; 3. turda kullanılmaz)",
         f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)",
         f"- ON_KAYIT_2: git {git2.get('commit', '?')[:10]}, {git2.get('commit_zamani', '?')}",
         f"- IS_TANIMI_3: git {git_is.get('commit', '?')[:10]}, {git_is.get('commit_zamani', '?')}",
         f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "Bu dosya 3. tur ölçümünden ÖNCE yazıldı. Y9 / Y9b / Y9c / Y9d için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / "
         "konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni ve olay sayımı). `kos --deneme Y9,Y9b,Y9c,Y9d` bu dosyanın "
         "kontrol listesini, sha'larını, git kaydını ve Y1-Y8B eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.", "",
         "## GEREKÇE ve DÜRÜSTLÜK NOTU (iş tanımı §2, AYNEN)", "", s2, "",
         "## BAKILMIŞ HÜCRE İŞARETİ", "",
         "- BAKILMIŞ (ana modelin ön kayıtsız bakışı sonucu gördü): " + ", ".join(" ".join(x) for x in K["bakilmis"]) + ". Bu hücreler karar "
         "hücreleridir ama sonuçları bağımsız kanıt değildir; etiket EN FAZLA EMARE.",
         "- DIŞ SINAMA (ana model bakmadı): " + ", ".join(" ".join(x) for x in K["dis_sinama"]) + " (karar kuralıyla aynı 4 şart; ikisi de TUTAR -> "
         "'EMARE (dış sınama tuttu)').",
         "- BIST (bilgi, ayrı başlık; ana model bakmadı): " + ", ".join(" ".join(x) for x in K["bist_bilgi"]) + ".",
         "- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).", "",
         "## Ölçü, kontrol grupları, karar kuralı", "",
         "1. turla AYNI (ON_KAYIT.md; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi, ESIK_TUR1_SHA / ESIK_TUR2_SHA kanıtı):",
         f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- EŞ: {Y['kontrol']['es']}.",
         f"- PLASEBO: {Y['kontrol']['plasebo']}.", f"- Karar: {Y['karar']['tanim']}.", f"- Hücre durumu: {Y['etiket']['hucre']}.",
         f"- Kural etiketi (deneme başına): {Y['etiket']['genel']}", "",
         "## 3. tur ek kuralları (önceden yazılı; DEĞİŞMEZ)", "",
         f"- Etiket: {K['etiket']}.", f"- TERS: {K['ters']}.", f"- Konum eşli KAT: {K['konum_es']}.", f"- Çeyrek: {K['ceyrek_tanim']}.",
         f"- Konum uyumu: {K['konum_uyum']}.", f"- Regresyon: {K['regresyon']}.",
         "- Y9d bilgi satırıdır: etiketi yazılır, karar değildir. BH (bilgi) yalnız Y9 / Y9b / Y9c x 4 karar hücresi (12 p; ayrı aile 'bh_tur3').", "",
         "## Denemeler (sonuç görülmeden sabit; YAPI_HEDEF_3_IS_TANIMI.md §3)", ""]
    for k in YH_DENEMELER_3:
        D = Y["denemeler"][k]
        s.append(f"- **{k} {D['ad']}**: {D['tanim']}.")
    s += ["", "## Yorumlar (iş tanımında açık ya da çelişik noktalar; koşudan önce sabit)", "",
          "- YORUM-1 (F15 bilgi anı): iş tanımı §3 'son 120 barın aralığında kapanış konumu; t-1'e kadar' diyor, aynı cümle 'özellikler "
          "ozellik_Y1.csv.gz'den (t'ye kadar)' diyor; dosyadaki F15 (GOZ_ETIKET tanımı) C_t'yi ve t DAHİL son 120 kapanışı kullanır ve §2'deki "
          "bakış da bu dosyayla yapıldı. Dosya tanımı uygulanır. C_t sinyal günü kapanışıdır, giriş t+1 açılıştır: geleceğe bakma yok. (HATA "
          "listesinde iş tanımı tutarsızlığı olarak yazılır.)",
          "- YORUM-2 (Y1 OLAYI): Y9* = Y1 OLAY kümesinin (OC tekil, havuzda, giriş var) alt kümesi; özellik dosyası satırları = olay_Y1.csv.gz "
          "satırları (26.663). Y1 sinyali olup Y1 olayı olmayan günler (60 gün içinde önceki Y1 olayı) Y9'a giremez; böylece Y9 sayısı Y1 tekilinden "
          "türer (iş tanımı 'Y1 olayı VE ...').",
          "- YORUM-3 (sınırlar): F15 <= 0,25 ve F15 >= 0,75 kapalı, Y9d açık (0,25, 0,75); dosya değerleri 6 anlamlı basamak (eşik kenarında "
          "yuvarlama dosya değerine göre). NaN (F15: 120 bar yok / aralık 0; F17: bölge öncesi 60 bar yok) şart tutmaz.",
          "- YORUM-4 (konum eşi F15): eşin F15'i giriş gününden önceki son geçerli barında hesaplanır (olayın t'si de giriş gününden önceki son "
          "geçerli bar). Olayın çeyreği dosyadan; panelden hesaplanan olay çeyreği >= %99 aynı olmalı (formül denetimi). Çeyrek sınırında "
          "kayan nokta gürültüsü (tam 0,75 konum panelde 0,7499999999) için değer çeyreğe atanmadan önce 9 ondalığa yuvarlanır (yh_ceyrek).",
          "- YORUM-5 (dış sınama 'aynı yön + kural'): ABD 2016-22 VE AVR 2016-22 hücrelerinin ikisi de 1. turun 4 şartlı TUTAR kuralını sağlar. "
          "Tersi için ikisi de TERS. Tek hücre tutarsa 'dış sınama tutmadı' yazılır.",
          "- YORUM-6 (TERS iki yarı): 1. turun 'yari1_kat5 / yari2_kat5' bilgisi (hücre olayları giriş sırasına göre ikiye bölünür, Σ h5 / Σ eş h5).",
          "- YORUM-7 (Y9c TERS ve stop): TERS kuralı stop şartı içermez (iş tanımı: KAT5 üst uç < 1 ve iki yarı aynı yön); stop payları raporda "
          "bilgi olarak yazılır.", "",
          "## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)", ""]
    s += ["### Y9 hunisi", ""] + _yh_huni_md(say["huni"], "Y9") + [""]
    s += ["Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): " + "; ".join(
        f"{p}: Y1 sinyal {x.get('y1_sinyal')}, Y1 olay {x.get('y1_olay', '?')}, özellik {x.get('ozellik_satir')}, eşleşen {x.get('eslesen')}"
        for p, x in say["eslesme"].items()) + ".", "",
          "| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |", "|---|---|---|---|"]
    for k in YH_DENEMELER_3:
        for p in OC.OC_ESIK["pazar"]:
            x = say["deneme"].get(k, {}).get(p)
            if x:
                s.append(f"| {k} | {p} | {x['hisse']} | " + " / ".join(str(x["olay"].get(q, 0)) for q in _YH_DONEM3) + " |")
    s += ["", "## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)", ""]
    try:
        tablo = json.load(open(_yh_yol("guc_json"), encoding="utf-8"))
    except (OSError, ValueError):
        tablo = None
    for k in YH_DENEMELER_3:
        if Y["denemeler"][k].get("bilgi"):
            continue
        hc = [(p, q, int(say["deneme"].get(k, {}).get(p, {}).get("olay", {}).get(q, 0))) for p, q in Y["karar"]["hucre_karar"]]
        gs = [yh_guc_bak(n, Y["denemeler"][k]["yon"], tablo) for _, _, n in hc]
        ifade = "; ".join(f"{p} {q} en çok {n} olay (güç {_yz(g, 0)})" for (p, q, n), g in zip(hc, gs))
        az = all(n < Y["etiket"]["n_yeter"] and g < Y["etiket"]["guc_esik"] for (_, _, n), g in zip(hc, gs))
        s.append(f"- {k}: {ifade}." + (" Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ "
                                      "yazılır." if az else ""))
    s += ["- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay "
          "o satırdan düşer (k_n ayrı yazılır).",
          "- Hayatta kalma: dipteki (Y9) hissenin batma olasılığı yüksektir; evrende batan yok -> Y9 hedef payı ayrıca yukarı yanlı okunur.", "",
          "## YH_ESIK 3. tur girdileri (tam metin; geri kalanı ON_KAYIT.md / ON_KAYIT_2.md ile aynı)", "", "```json",
          json.dumps({k: Y["denemeler"][k] for k in YH_DENEMELER_3}, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
          yh_kontrol_tablosu(YH_KONTROL_3), "", "## SAPMALAR", "", "(yok)", "",
          "## Test", "", "`python test_yapi_hedef.py` (önceki turların testleri aynen + 3. tur: özellik birleştirme sembol + tarih (satır sırası "
          "karışık dosya), Y9 / Y9b / Y9c / Y9d seçimi, F1 / F11 / F15 / F17 = GOZ_ETIKET.ge_ozellik_bar, prefix (geleceğe bakma), F15 paneli = "
          "elle, konum eşli KAT elle = kod, TERS ve 3. tur etiketi, ESIK_TUR2_SHA = 2. tur mührü, 3. tur uçtan uca onkayit3 + kos + kapı, "
          "önceki turların sonuçları değişmez).", ""]
    return "\n".join(s)


def yh_onkayit3_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_3.md: 1. ve 2. tur ölçülmüş, 3. tur ölçülmemiş olmalı; Y1-Y8B eşik mührü tutmalı; özellik dosyası = Y1 olay kümesi."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit3", cikti)
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"ön kayıt 3 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"ön kayıt 3 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 3. tur ön kaydı önceki turların ölçümünden sonra yazılır")
    J = json.load(open(sy, encoding="utf-8"))
    if [k for k in YH_DENEMELER_3 if k in J.get("deneme", {})]:
        raise YHHata("3. tur denemeleri zaten ölçülmüş: ön kayıt ölçümden sonra yazılamaz")
    if "Y1" not in J.get("deneme", {}):
        raise YHHata("Y1 ölçülmemiş: 3. tur Y1 olaylarının alt kümesidir")
    t1, t2 = yh_esik_sha_tur1(), yh_esik_sha_tur2()
    m1 = re.search(_YH_KAPI_DESEN["esik"], open(_yh_yol("onkayit", cikti), encoding="utf-8").read())
    y2 = _yh_yol("onkayit2", cikti)
    m2 = re.search(_YH_KAPI_DESEN["esik"], open(y2, encoding="utf-8").read()) if os.path.exists(y2) else None
    gj = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    if not (m1 and m1.group(1) == t1 == gj.get("yh_esik_sha")):
        raise YHHata("Y1-Y5 eşik mührü tutmuyor (ON_KAYIT.md / güç tablosu / yh_esik_sha_tur1)")
    if not (m2 and m2.group(1) == t2):
        raise YHHata("Y1-Y8B eşik mührü tutmuyor (ON_KAYIT_2.md YH_ESIK_SHA / yh_esik_sha_tur2)")
    sha = yh_sha_simdi3(cikti)
    git2 = _yh_git(y2) if git else {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi3"]) if git else {}
    except YHHata:
        git_is = {}
    s2 = _yh_is_tanimi3_s2()
    say = yh_sayim3(veri, islem)
    for p in OC.OC_ESIK["pazar"]:                     # regresyon: Y1 olay sayısı = 1. turun girdi - havuz dışı - tekil - giriş yok / geç
        x = J.get("sayim", {}).get("Y1", {}).get(p)
        if x:
            n1 = int(x["girdi"]) - int(x.get("havuz_disi", 0)) - int(x.get("tekil", 0)) - int(x.get("giris_yok", 0)) - int(x.get("giris_gec", 0))
            if n1 != say["eslesme"][p].get("y1_olay", n1):
                raise YHHata(f"regresyon: {p} Y1 olay sayısı 1. turda {n1}, şimdi {say['eslesme'][p].get('y1_olay')} -> ön kayıt yazılmadı")
    _yh_yaz(yol, yh_onkayit3_metni(say, sha, git2, git_is, t1, t2, s2), "ön kayıt 3")
    return yol


def _yh_y1_satir_yolu(sonuc: Dict[str, Any], cikti: str) -> str:
    rel = sonuc.get("deneme", {}).get("Y1", {}).get("satir_dosya")
    adaylar = ([rel if os.path.isabs(rel) else os.path.join(KOK_YH, rel)] if rel else []) + [os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1"))]
    for a in adaylar:
        if os.path.exists(a):
            return a
    raise YHHata(f"Y1 satır dosyası yok ({adaylar}): regresyon yapılamaz -> DURDU")


def yh_sha_simdi3(cikti: Optional[str] = None) -> Dict[str, str]:
    """1. turun sha'ları + özellik dosyası + Y1 satır dosyası (regresyon)."""
    cikti = cikti or YH_YOL["cikti"]
    out = yh_sha_simdi(cikti)
    if not os.path.exists(YH_YOL["ozellik"]):
        raise YHHata(f"özellik dosyası yok: {YH_YOL['ozellik']}")
    out["ozellik"] = _yh_sha_dosya(YH_YOL["ozellik"])
    sy = _yh_yol("sonuc", cikti)
    J = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
    out["y1olay"] = _yh_sha_dosya(_yh_y1_satir_yolu(J, cikti))
    return out


def yh_kapi3(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """3. tur koşu kapısı: ON_KAYIT_3.md kontrol listesi + bütün sha'lar (özellik, Y1 satır dosyası dahil) + Y1-Y8B eşik mührü + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit3", cikti)
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt 3 yok: {yol}")
    metin = open(yol, encoding="utf-8").read()
    t1, t2 = yh_esik_sha_tur1(), yh_esik_sha_tur2()
    m_t1 = re.search(r"ESIK_TUR1_SHA:\s*`([0-9a-f]{64})`", metin); m_t2 = re.search(r"ESIK_TUR2_SHA:\s*`([0-9a-f]{64})`", metin)
    y1, y2 = _yh_yol("onkayit", cikti), _yh_yol("onkayit2", cikti)
    m1 = re.search(_YH_KAPI_DESEN["esik"], open(y1, encoding="utf-8").read()) if os.path.exists(y1) else None
    m2 = re.search(_YH_KAPI_DESEN["esik"], open(y2, encoding="utf-8").read()) if os.path.exists(y2) else None
    gj = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("guc_json", cikti)) else {}
    if not (m_t1 and m1 and m_t1.group(1) == t1 == m1.group(1) == gj.get("yh_esik_sha")):
        raise YHHata("3. tur kapısı: Y1-Y5 eşik mührü tutmuyor -> koşu DURDU")
    if not (m_t2 and m2 and m_t2.group(1) == t2 == m2.group(1)):
        raise YHHata("3. tur kapısı: Y1-Y8B eşik mührü (ESIK_TUR2_SHA / ON_KAYIT_2.md) tutmuyor -> koşu DURDU")
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    desen = dict(_YH_KAPI_DESEN); desen["ozellik"] = r"OZELLIK_SHA:\s*`([0-9a-f]{64})`"; desen["y1olay"] = r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`"
    bul = {}
    for ad, d_ in desen.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"ön kayıt 3'te {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi3(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"]); out["git_guc"] = _yh_git(_yh_yol("guc_json", cikti))
        out["git_ozellik"] = _yh_git(YH_YOL["ozellik"])
    yhlog.info("yh_kapi3 AÇIK (%s)", yol)
    return out


def yh_kos3(denemeler: List[str], cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True,
            kontrol: bool = True, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """3. tur koşusu: kapı -> Y1 sinyali ∩ özellik -> Y9* ölçüm (1. tur kodu) -> konum eşli KAT -> Y1 regresyonu -> sonuc.json / RAPOR_3.md."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]
    if any(k not in YH_DENEMELER_3 for k in denemeler):
        raise YHHata(f"3. tur denemeleri başka turla aynı koşuda olmaz: {denemeler}")
    denemeler = [k for k in YH_DENEMELER_3 if k in denemeler]
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 3. tur önceki turlardan sonra koşar")
    sonuc = json.load(open(sy, encoding="utf-8"))
    tekrar = [k for k in denemeler if k in sonuc.get("deneme", {})]
    if tekrar:
        raise YHHata(f"bu denemeler zaten ölçüldü (ölçüm bir kez koşulur): {tekrar}")
    ok = yh_kapi3(cikti, git=git, kontrol=kontrol)
    kos_zaman = _yh_simdi()
    if ok["onkayit_zaman"] > kos_zaman:
        raise YHHata("ön kayıt zamanı koşu zamanından sonra")
    tablo = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    O1 = pd.read_csv(_yh_y1_satir_yolu(sonuc, cikti), parse_dates=["tarih", "giris"])
    sonuc["kos"].append({"zaman_utc": kos_zaman, "kapi": ok, "denemeler": denemeler, "islem": islem})
    K = _yh_kural3(Y); Ols: Dict[str, List[pd.DataFrame]] = {k: [] for k in denemeler}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
        S = yh_sinyaller3(Vd, p, denemeler, islem, Y, P=P)
        sonuc.setdefault("huni3", {})[p] = yh_huni3(S, P, Y); sonuc.setdefault("y9_eslesme", {})[p] = S["_Y9R"]
        F15p = yh_f15_panel(P, Vd, Y)
        for k in denemeler:
            X = S.get(k, pd.DataFrame())
            sonuc["gelecek_denetimi"].setdefault(k, {})[p] = yh_gelecek_denetimi(Vd, X, k, p, Y)
            Z, say = yh_olc_pazar(Vd, P, Cl, X, k, p, islem, Y)
            dus = {a: int(say.get(a, 0)) for a in ("giris_yok", "giris_gec", "havuz_disi", "tekil")}
            if any(dus.values()):
                raise YHHata(f"{k} {p}: Y1 olay alt kümesi OC'de düştü {dus} (Y9 ⊆ Y1 olayı bozuk) -> DURDU")
            if len(Z):
                Z = Z.merge(X[["sembol", "tarih"] + _Y9_OZ].assign(tarih=pd.to_datetime(X.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
                Z = yh_konum_es_olc(P, Cl, Z, F15p, islem, Y)
                qv = Z[Z.q_olay >= 0]
                uy = float((qv.q_olay == qv.q_panel).mean()) if len(qv) else 1.0
                say["ceyrek_uyum_binde"] = int(round(uy * 1000))
                if uy < K["konum_uyum_min"]:
                    raise YHHata(f"{k} {p}: panel F15 çeyreği dosyayla yalnız %{uy * 100:.1f} aynı (< %99) -> DURDU")
                sonuc.setdefault("regresyon_y1", {}).setdefault(k, {})[p] = yh_y1_regresyon(Z, O1)
            sonuc["sayim"].setdefault(k, {})[p] = {a: int(b) for a, b in say.items()}
            if len(Z):
                Ols[k].append(Z)
            yhlog.info("%s %s: olay %d (%.0f sn)", k, p, len(Z), time.time() - t0)
        del Vd, P, Cl, F15p
    for k in denemeler:
        Ol = pd.concat(Ols[k], ignore_index=True) if Ols[k] else pd.DataFrame()
        sonuc["deneme"][k] = yh_sonuc_deneme3(Ol, k, tablo, Y)
        if len(Ol):
            sonuc["deneme"][k]["satir_dosya"] = os.path.relpath(yh_satir_yaz(Ol, k, cikti), KOK_YH)
    anahtar, pler = [], []
    for k in [x for x in YH_DENEMELER_3 if not Y["denemeler"][x].get("bilgi")]:
        for h in sonuc["deneme"].get(k, {}).get("hucre", []):
            if h.get("karar_hucre"):
                anahtar.append((k, h["pazar"], h["donem"])); pler.append(h.get("h5_p", np.nan))
    sonuc["bh_tur3"] = [{"deneme": a, "pazar": b, "donem": c, "p": p, "bh_q10": g} for (a, b, c), p, g in zip(anahtar, pler, _yh_bh(pler, 0.10))]
    sonuc["sure_sn"] = round(sonuc.get("sure_sn", 0) + time.time() - t0, 1)
    _yh_yaz(sy, json.dumps(sonuc, ensure_ascii=False, indent=1, default=_yh_json), "sonuç")
    return {"sonuc": sonuc, "rapor": yh_rapor3(cikti)}


def yh_rapor3(cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> str:
    """3. tur raporu (RAPOR_3.md): Y9 / Y9b / Y9c (+ Y9d bilgi), huni, hücre (bakılmış işaretli), konum eşli KAT, olasılık, dış sınama, BIST,
    iki yönlü etiket. RAPOR.md / RAPOR_2.md'ye dokunmaz."""
    cikti = cikti or YH_YOL["cikti"]
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    den = [k for k in YH_DENEMELER_3 if k in J["deneme"]]
    if not den:
        raise YHHata("sonuc.json'da 3. tur denemesi yok")
    K = _yh_kural3(Y)
    k3 = [k for k in J["kos"] if any(x in YH_DENEMELER_3 for x in k["denemeler"])][-1]
    kh = lambda D: {(h["pazar"], h["donem"]): h for h in D["hucre"]}  # noqa: E731

    def isaret(h: Dict[str, Any]) -> str:
        if h.get("bakilmis"):
            return "BAKILMIŞ"
        if h.get("dis_sinama"):
            return "DIŞ SINAMA"
        return "BIST bilgi" if h["pazar"] == "BIST" else "bilgi"
    s = ["# YAPI_HEDEF — RAPOR 3 (3. tur: Y9 düşüş sonrası dipte / Y9b / Y9c tepede / Y9d orta; konum eşli KAT)", "",
         f"{J['surum']}. Koşu: {k3['zaman_utc']} ({', '.join(k3['denemeler'])}). Ön kayıt 3: {k3['kapi'].get('onkayit_zaman', '?')} "
         f"(git {k3['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}).", "",
         "## 1. SONUÇ (etiket önceden yazılı kuralla; EN FAZLA EMARE: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ)", "",
         "| Deneme | ETİKET (3. tur) | kural etiketi | İKİ YÖNLÜ (TERS) | dış sınama ABD / AVR 2016-22 | karar hücreleri (ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26) |",
         "|---|---|---|---|---|---|"]
    for k in den:
        D = J["deneme"][k]; h_ = kh(D)
        hc = " · ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' / TERS' if h_.get(tuple(x), {}).get('ters') else ''} (n {h_.get(tuple(x), {}).get('n', 0)}, "
                        f"KAT5 {_sy(h_.get(tuple(x), {}).get('h5_kat'))})" for x in Y["karar"]["hucre_karar"])
        ds = " / ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' TERS' if h_.get(tuple(x), {}).get('ters') else ''}" for x in K["dis_sinama"])
        s.append(f"| {k} {D['ad']}{' (BİLGİ, karar değil)' if D.get('bilgi') else ''} | **{D['etiket']}** | {D.get('etiket_kural', '-')} | "
                 f"{D.get('ters_etiket', '-')} | {ds} | {hc} |")
    s += ["", f"3. tur etiket kuralı: {K['etiket']}.", f"TERS: {K['ters']}.", "",
          "DÜRÜSTLÜK: ABD / AVR 2023 ve 2024-26 hücrelerinin sonucu (F15 dip / tepe kırılımı) ön kayıttan önce ana modelin bakışında görüldü; bu "
          "hücreler bağımsız kanıt değildir. Bağımsız olan yalnız dış sınama (2016-22 ABD / AVR) ve BIST hücreleridir. Asıl karar Mart 2027 ileri "
          "testidir (kriz sonrası veri, aynı eşik).", "",
          "## 2. HUNİ (Y1 olayından şart şart; getirisiz)", ""]
    olcum = {k: {(h["pazar"], h["donem"]): h.get("n", 0) for h in J["deneme"][k]["hucre"] if h["donem"] in _YH_DONEM3} for k in den}
    s += _yh_huni_md(J.get("huni3", {}), "Y9", {a: olcum[a] for a in den})
    s += ["", "Y1 eşleşmesi: " + "; ".join(f"{p}: Y1 olay {x.get('y1_olay', '?')} = özellik satırı {x.get('ozellik_satir')} (eşleşen {x.get('eslesen')})"
                                           for p, x in J.get("y9_eslesme", {}).items()) + ".", "",
          "## 3. OLAY SAYIMI ve DENETİMLER", "",
          "| Deneme | Pazar | girdi | düşen (giriş / havuz / tekil) | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma (5 olay, özellik dahil) | F15 çeyrek uyumu | Y1 regresyonu (satır) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for p, x in J["sayim"].get(k, {}).items():
            rg = J.get("regresyon_y1", {}).get(k, {}).get(p, {})
            s.append(f"| {k} | {p} | {x.get('girdi', 0)} | {x.get('giris_yok', 0) + x.get('havuz_disi', 0) + x.get('tekil', 0)} | {x.get('giris_stop_otesi', 0)} | "
                     f"{x.get('olc15_yok', 0)} | {x.get('es_az', 0)} | {x.get('plasebo_yok', 0)} | {J['gelecek_denetimi'].get(k, {}).get(p, '-')} TUTTU | "
                     f"%{x.get('ceyrek_uyum_binde', 0) / 10:.1f} | {'EŞİT ' + str(rg.get('n')) if rg.get('esit') else '-'} |")
    s += ["", "## 4. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95; İŞARET: BAKILMIŞ / DIŞ SINAMA / BIST bilgi)", "",
          "| Deneme | Hücre | İŞARET | n | P(+5) olay / eş | KAT5 [%95] | P(stop önce) olay / eş | plasebo KAT5 [%95] | şartlar n·kat·stop·plasebo | güç | DURUM | TERS |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            et = f"{h['pazar']} {h['donem']}{' (karar)' if h['karar_hucre'] else ''}"
            if not h.get("n"):
                s.append(f"| {k} | {et} | {isaret(h)} | 0 | - | - | - | - | - | - | {h['durum']} | - |"); continue
            sart = "".join("✓" if h.get(a) else "·" for a in ("s_n", "s_kat", "s_stop", "s_plasebo"))
            s.append(f"| {k} | {et} | {isaret(h)} | {h['n']} | {_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))} | {_sy(h.get('h5_kat'))} "
                     f"[{_sy(h.get('h5_alt'))}, {_sy(h.get('h5_ust'))}] | {_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))} | {_sy(h.get('pl_h5_kat'))} "
                     f"[{_sy(h.get('pl_h5_alt'))}, {_sy(h.get('pl_h5_ust'))}] | {sart} | {_yz(h.get('guc'), 0)} | {h['durum']} | {'TERS' if h.get('ters') else '-'} |")
    s += ["", "## 5. KONUM EŞLİ KAT (zorunlu; eş = aynı gün, aynı kova VE F15 aynı çeyrek; eşlerin F15 dağılımı)", "",
          "Okuma: KAT5 (1. tur eşi) dipte olmanın momentum kovasıyla karışmasını ayırmaz; konum eşli KAT5 aynı çeyrekteki eşlerle karşılaştırır "
          "(S6 kırılımının konumdan bağımsız katkısı).", "",
          "| Deneme | Hücre | İŞARET | n (1. tur eş) | KAT5 (1. tur eş) | n (konum eş) | P(+5) olay / konum eş | KAT5 konum [%95] | P(stop önce) olay / konum eş | "
          "olay F15 ort | eş F15 ort / medyan | eşlerin olay çeyreğinde payı |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("n"):
                continue
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {isaret(h)} | {h['n']} | {_sy(h.get('h5_kat'))} | {h.get('k_n', 0)} | {_yz(h.get('k_h5_p_olay'))} / "
                     f"{_yz(h.get('k_h5_p_ref'))} | {_sy(h.get('k_h5_kat'))} [{_sy(h.get('k_h5_alt'))}, {_sy(h.get('k_h5_ust'))}] | {_yz(h.get('k_st5_p_olay'))} / "
                     f"{_yz(h.get('k_st5_p_ref'))} | {_sy(h.get('olay_f15_ort'))} | {_sy(h.get('es_f15_ort'))} / {_sy(h.get('es_f15_med'))} | {_yz(h.get('es_ayni_ceyrek'))} |")
    s += ["", "## 6. OLASILIK TABLOSU (Cemal'in biçimi: olay / eş / taban; KAT = olay / eş [%95])", "",
          "| Deneme | Hücre | İŞARET | n | P(+5 önce) olay / eş / taban | KAT | P(+10 önce) olay / eş / taban | KAT | P(stop önce) olay / eş / taban | KAT |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("n"):
                continue
            c = []
            for g in ("h5", "h10", "st5"):
                c.append(f"{_yz(h.get(g + '_p_olay'))} / {_yz(h.get(g + '_p_ref'))} / {_yz(h.get('tb_' + g + '_p'))}")
                c.append(f"{_sy(h.get(g + '_kat'))} [{_sy(h.get(g + '_alt'))}, {_sy(h.get(g + '_ust'))}]")
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {isaret(h)} | {h['n']} | " + " | ".join(c) + " |")

    def alt_tablo(hucreler: List[List[str]]) -> List[str]:
        t = ["| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop) olay / eş | plasebo KAT5 alt | konum KAT5 [%95] | yarı 1 / yarı 2 | DURUM | TERS |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
        for k in den:
            hk = kh(J["deneme"][k])
            for x in hucreler:
                h = hk.get(tuple(x), {})
                t.append(f"| {k} | {x[0]} {x[1]} | {h.get('n', 0)} | {_yz(h.get('h5_p_olay'))} / {_yz(h.get('h5_p_ref'))} | {_sy(h.get('h5_kat'))} "
                         f"[{_sy(h.get('h5_alt'))}, {_sy(h.get('h5_ust'))}] | {_yz(h.get('st5_p_olay'))} / {_yz(h.get('st5_p_ref'))} | {_sy(h.get('pl_h5_alt'))} | "
                         f"{_sy(h.get('k_h5_kat'))} [{_sy(h.get('k_h5_alt'))}, {_sy(h.get('k_h5_ust'))}] | {_sy(h.get('yari1_kat5'))} / {_sy(h.get('yari2_kat5'))} | "
                         f"{h.get('durum', '-')} | {'TERS' if h.get('ters') else '-'} |")
        return t
    s += ["", "## 7. DIŞ SINAMA (2016-22 ABD / AVR; ana model bakmadı)", ""] + alt_tablo(K["dis_sinama"])
    s += ["", "Dış sınama kararı: " + "; ".join(f"{k}: TUTAR {'evet' if J['deneme'][k].get('dis_sinama_tutar') else 'hayır'}, TERS "
                                                 f"{'evet' if J['deneme'][k].get('dis_sinama_ters') else 'hayır'}" for k in den) + "."]
    s += ["", "## 8. BIST (bilgi; ayrı başlık; karar değil)", ""] + alt_tablo(K["bist_bilgi"])
    s += ["", "## 9. İKİ YÖNLÜ ETİKET (TERS EMARE kuralı; karar hücreleri)", "", "| Deneme | Hücre | n | KAT5 [%95] | üst < 1 | yarı 1 / yarı 2 | TERS |",
          "|---|---|---|---|---|---|---|"]
    for k in den:
        hk = kh(J["deneme"][k])
        for x in Y["karar"]["hucre_karar"]:
            h = hk.get(tuple(x), {})
            u = h.get("h5_ust")
            s.append(f"| {k} | {x[0]} {x[1]} | {h.get('n', 0)} | {_sy(h.get('h5_kat'))} [{_sy(h.get('h5_alt'))}, {_sy(u)}] | "
                     f"{'evet' if (u is not None and u == u and u < 1) else 'hayır'} | {_sy(h.get('yari1_kat5'))} / {_sy(h.get('yari2_kat5'))} | "
                     f"{'TERS' if h.get('ters') else '-'} |")
        s.append(f"| {k} | **ters etiket** | | | | | **{J['deneme'][k].get('ters_etiket', '-')}** |")
    s += ["", "## 10. BİLGİ: High ile hedef, takip stoplu getiri, çıkış", "",
          "| Deneme | Hücre | KAT5 High [%95] | KAT10 High | getiri ort / medyan | kazanan | çıkış barı ort / med | çıkış türü | d medyan |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for h in J["deneme"][k]["hucre"]:
            if not h.get("n"):
                continue
            ct = ", ".join(f"{a} {b}" for a, b in sorted(h.get("cikis_tur", {}).items()))
            s.append(f"| {k} | {h['pazar']} {h['donem']} | {_sy(h.get('h5H_kat'))} [{_sy(h.get('h5H_alt'))}, {_sy(h.get('h5H_ust'))}] | {_sy(h.get('h10H_kat'))} | "
                     f"{_yz(h.get('getiri_ort'))} / {_yz(h.get('getiri_med'))} | {_yz(h.get('getiri_kazanan'), 0)} | {_sy(h.get('cikis_bar_ort'), 1)} / "
                     f"{_sy(h.get('cikis_bar_med'), 0)} | {ct} | {_yz(h.get('dd_med'))} |")
    s += ["", "## 11. ÇOKLU KARŞILAŞTIRMA (bilgi; Y9 / Y9b / Y9c karar hücreleri KAT5 bootstrap p = P(KAT <= 1), BH q 0,10)", "",
          "| Deneme | Hücre | p | BH geçer |", "|---|---|---|---|"]
    for b in J.get("bh_tur3", []):
        s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {_sy(b['p'], 3)} | {'evet' if b['bh_q10'] else 'hayır'} |")
    s += ["", "## 12. VERİ SINIRLARI", ""]
    for p, n_ in J.get("veri_not", {}).items():
        s.append(f"- {p}: " + "; ".join(n_))
    s += ["- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.",
          "- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı; DİPTE (Y9) olaylarda bu yanlılık daha "
          "büyük olabilir (eş ve plasebo aynı evrenden).",
          "- Sonradan bilgi: ABD / AVR 2023 ve 2024-26 hücreleri ön kayıttan önce görüldü (ön kayıt 3 §2 notu).",
          "- F15 bilgi anı t (C_t dahil; ön kayıt YORUM-1); eşin F15'i giriş gününden önceki son geçerli bar.", "",
          "## 13. YENİDEN ÜRETİM (satır dosyasından iki hücre; biri konum eşli)", "", "```",
          "python - <<'EOF'", "import pandas as pd",
          "for d, p, q in [('Y9', 'ABD', '2016-22'), ('Y9c', 'ABD', '2024-26')]:",
          "    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q)]",
          "    a = x[x.h5.notna() & x.es_h5.notna()]; b = x[x.h5.notna() & x.k_es_h5.notna()]",
          "    print(d, p, q, len(a), round(a.h5.sum() / a.es_h5.sum(), 4), round(a.st5.mean(), 4), round(a.es_st5.mean(), 4), len(b), round(b.h5.sum() / b.k_es_h5.sum(), 4))",
          "EOF", "```", "", "Satır dosyası 5 MB'ı aşarsa scratch yolundadır (sonuc.json 'satir_dosya').", "",
          yh_kontrol_tablosu(YH_KONTROL_3), ""]
    metin = "\n".join(s)
    _yh_yaz(_yh_yol("rapor3", cikti), metin, "rapor 3")
    return metin


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
def _cakisma_kontrol_yh(_once=_CK_ONCE_YH, _dosya="YAPI_HEDEF.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_YH", "_CK_KAYIT", "_cakisma_kontrol_yh", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "time", "re", "hashlib", "subprocess", "warnings", "_dt", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple", "OC", "S6", "SY", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_yh()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=YH_SURUM)
    ap.add_argument("komut", choices=["guc", "onkayit", "onkayit2", "onkayit3", "kos", "rapor", "rapor2", "rapor3", "sha"])
    ap.add_argument("--deneme", default=None)
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    a = ap.parse_args()
    try:
        if a.komut == "guc":
            J_ = yh_guc(a.cikti, a.veri); print(yh_guc_md(J_))
        elif a.komut == "onkayit":
            print(yh_onkayit_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz))
        elif a.komut == "onkayit2":
            print(yh_onkayit2_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "rapor2":
            print(yh_rapor2(a.cikti))
        elif a.komut == "onkayit3":
            print(yh_onkayit3_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "rapor3":
            print(yh_rapor3(a.cikti))
        elif a.komut == "kos":
            den_ = a.deneme.split(",") if a.deneme else None
            R_ = yh_kos(den_, a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "rapor":
            print(yh_rapor(a.cikti))
        else:
            print(json.dumps(yh_sha_simdi(a.cikti), indent=1))
    except YHHata as ex:
        yhlog.error("%s", ex); sys.exit(1)
