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
        4. TUR (YAPI_HEDEF_IS_TANIMI_4.md; S7 'Cemal bölge seçici': Y10 = Y1 olayı + Ş1 dipte + Ş2 hat net + Ş3 dip savunulmuş + Ş4 küçük mum +
        Ş5 kısa alt fitil + Ş6 kazan sağ kenarı + Ş7 yakın tavan gövdeli kırılım + Ş8 yol almamış; Y10b = Y10 + F14 >= 0; Y10c = Ş2-Ş8 bilgi):
        python YAPI_HEDEF.py s7ozellik                 F20-F23 (ham fiyat, [t-15, t]) -> ozellik_Y1_s7.csv.gz + denetim json (prefix)
        python YAPI_HEDEF.py onkayit4 [--islem 4]      ON_KAYIT_4.md (S7 tanımı aynen, huni Ş1..Ş8, mühür zinciri, kontrol listesi)
        python YAPI_HEDEF.py kos --deneme Y10,Y10b,Y10c [--islem 4]   kapı (tur 4) -> ölçüm + konum eşli KAT + Y1 regresyonu + Cemal uyumu
                                                       + TUR 4 örneklem sayımı (kuru; tur ac koşulmaz) -> RAPOR_4.md
        python YAPI_HEDEF.py rapor4                    sonuc.json -> RAPOR_4.md
        5. TUR (YAPI_HEDEF_IS_TANIMI_5.md; Ş9 U dip + parabolik devam: Y11 = Y1 olayı + Ş1 + Ş2 + Ş9; Y11b = Y10 şartları, Ş6 yerine Ş9;
        Y11c = Y1 + Ş9 bilgi):
        python YAPI_HEDEF.py s9ozellik                 F24-F29 (ham fiyat, [t-291, t-1]) -> ozellik_Y1_s9.csv.gz + denetim json (prefix)
        python YAPI_HEDEF.py tasarim5                  tasarım kontrolü (No 38 geçmemeli; TUR 2 kazan sayfaları >= 3 / 4) -> tasarim5.json
        python YAPI_HEDEF.py onkayit5 [--islem 4]      ON_KAYIT_5.md (Ş9 tanımı aynen, tasarım kaydı, huni, mühür zinciri, kontrol listesi)
        python YAPI_HEDEF.py kos --deneme Y11,Y11b,Y11c [--islem 4]   kapı (tur 5) -> ölçüm + konum eşli KAT + Y1 regresyonu + Cemal uyumu
                                                       + TUR 4 kuru sayım (T1.5) + İLERLEME -> RAPOR_5.md
        python YAPI_HEDEF.py rapor5                    sonuc.json -> RAPOR_5.md
        6. TUR (YAPI_HEDEF_IS_TANIMI_6.md; GRUPLAR G1 trend içi raf / G2 düşüş sonrası dip (+ G2u U dip) / G3 rastgele; FİLTRE KARNESİ; MAHKEME):
        python YAPI_HEDEF.py onkayit6                  ON_KAYIT_6.md + grup6_G3.csv (getirisiz: grup sayıları, karne hunisi, mühürler, kontrol listesi)
        python YAPI_HEDEF.py grup6 [--islem 4]         kapı (tur 6) -> Y1 ölçümü + konum eşli KAT + regresyon + tutarlılık -> grup6.json, olay_G6.csv.gz
        python YAPI_HEDEF.py filtrekarne               FILTRE_KARNE.md + filtre_karne.json (yürüyen sınama; her yeni filtrede aynı komut)
        python YAPI_HEDEF.py mahkeme --pazar ABD --sembol X --tarih YYYY-MM-DD [--json yol]   tek olay mahkemesi (düz metin)
        python YAPI_HEDEF.py mahkeme --liste dosya.csv [--md yol]   toplu (no, pazar, sembol, tarih); md'de sembol / tarih yok
        python YAPI_HEDEF.py mahkeme --s7 | --tur4     S7_MAHKEME.md (50 olay) | tur/4/TUR_4_MAHKEME.md (40 kör sayfa)
        python YAPI_HEDEF.py rapor6                    grup6.json + karne + mahkeme özetleri -> RAPOR_6.md
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
# 4. tur (18 Kas 2026; arastirma_cikti/yapi_hedef/YAPI_HEDEF_IS_TANIMI_4.md; S7 Cemal bölge seçicisi). Y10c bilgi satırıdır.
YH_DENEMELER_4 = ["Y10", "Y10b", "Y10c"]
# 5. tur (19 Kas 2026; arastirma_cikti/yapi_hedef/YAPI_HEDEF_IS_TANIMI_5.md; Ş9 U dip + parabolik devam). Y11c bilgi satırıdır.
YH_DENEMELER_5 = ["Y11", "Y11b", "Y11c"]
YH_DENEMELER_HEPSI = YH_DENEMELER + YH_DENEMELER_2 + YH_DENEMELER_3 + YH_DENEMELER_4 + YH_DENEMELER_5   # dizin (plasebo / denetim tohumu) Y1-Y10c için önceki turlarla aynı
YH_DOSYA.update({"onkayit2": "ON_KAYIT_2.md", "rapor2": "RAPOR_2.md"})
YH_YOL["is_tanimi2"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_2_IS_TANIMI.md")
YH_DOSYA.update({"onkayit3": "ON_KAYIT_3.md", "rapor3": "RAPOR_3.md"})
YH_YOL["is_tanimi3"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_3_IS_TANIMI.md")
YH_YOL["ozellik"] = os.environ.get("YH_OZELLIK", os.path.join(KOK_YH, "arastirma_cikti", "goz_etiket", "ozellik_Y1.csv.gz"))
YH_DOSYA.update({"onkayit4": "ON_KAYIT_4.md", "rapor4": "RAPOR_4.md", "s7_denetim": "ozellik_Y1_s7_denetim.json"})
YH_YOL["is_tanimi4"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_IS_TANIMI_4.md")
YH_YOL["ozellik_s7"] = os.environ.get("YH_OZELLIK_S7", os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "ozellik_Y1_s7.csv.gz"))
YH_YOL["ge_kod"] = os.path.join(KOK_YH, "GOZ_ETIKET.py")
YH_YOL["ge_cikti"] = os.path.join(KOK_YH, "arastirma_cikti", "goz_etiket")

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
        # ---- 4. TUR (YAPI_HEDEF_IS_TANIMI_4.md §2; S7 'Cemal bölge seçici'; sonuç görülmeden sabit). Y1-Y9d girdileri yukarıda AYNEN
        # (yh_esik_sha_tur3 = 3. tur mührü ON_KAYIT_3.md YH_ESIK_SHA).
        "Y10": {"ad": "S7 ÇEKİRDEK (Cemal bölge seçici)", "yon": 1, "tur": 4, "taban": "Y1",
                "sartlar": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"],
                "esik": {"F15_ust": 0.25, "F17_ust": -0.20, "F1_min": 3, "F2_min": -0.01, "F3_ust": 0.90, "F4_ust": 0.25, "F20_min": 0.0,
                         "F22_alt_acik": 0.0, "F22a_ust_acik": 0.0, "F23_min": 0.50, "F18_ust": 0.20},
                "sart_tanim": {
                    "S1": "DİPTE (C6 / VD3; Y9 ile aynı): F15 <= 0,25 VE F17 <= -0,20",
                    "S2": "HAT NET (C1; Y9b ile aynı): F1 >= 3",
                    "S3": "DİP SAVUNULMUŞ (C2): F2 >= -0,01 (son dokunuş dibi ilk dokunuştan en çok %1 aşağıda; dokunuş yoksa F2 NaN = tutmaz)",
                    "S4": "MUMLAR KÜÇÜK (C3): F3 <= 0,90 (bölge medyan mum boyu / ATR250; parmak P1.1 eşiğiyle aynı)",
                    "S5": "ALT FİTİL KISA (C4): F4 <= 0,25 (bölge medyan alt fitil payı)",
                    "S6": "KAZAN SAĞ KENARI DÖNMÜŞ (VD6 / VD9 şart 1): F20 = min Low[t-5..t-1] / min Low[t-15..t-6] - 1 >= 0 (geçerli bar "
                          "sayımı; t'den önce 15 geçerli bar yoksa NaN = tutmaz)",
                    "S7": "YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM (VD5 / VD8 / C5): F21 = max High[t-15..t-1]; F22 = C_t / F21 - 1 > 0 VE "
                          "F22a = O_t / F21 - 1 < 0 (açılış tavanın altında; boşluklu açılış O_t >= F21 elenir) VE F23 = |C_t - O_t| / "
                          "(H_t - L_t) >= 0,50 (H_t = L_t ise NaN = tutmaz)",
                    "S8": "YOL ALMAMIŞ (C10 / C11 / VD2): F18 <= 0,20"},
                "s7_prm": {"sag": 5, "sol": 15, "tavan_gun": 15, "bilgi_azami_gun": 250,
                           "tanim": "F20-F23 (ve F22a) ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal "
                                    "günü (geçerli bar sırası i); yalnız [t-15, t] barları okunur (prefix: [t-250, t] kesiti ve t'de kesik veri "
                                    "aynı değeri vermeli); dosya ozellik_Y1_s7.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak)"},
                "tanim": "Y1 OLAYI (ozellik_Y1.csv.gz + ozellik_Y1_s7.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile) VE Ş1-Ş8 "
                         "hepsi (her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir",
                "tur4_kural": {
                    "etiket": "3. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket, bakılmış hücreler ABD / AVR 2023 ve 2024-26 "
                              "-> etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS "
                              "iki yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Bakılmış gerekçesi: Y10 / Y10b Y9'un alt kümesi, Y9 "
                              "hücreleri 3. turda görüldü; Y10c Y1'in alt kümesi, Y1 hücreleri 1. turda görüldü. Bağımsız kanıt dış sınama "
                              "ve BIST",
                    "bh": "Y10 / Y10b x 4 karar hücresi (8 p) BH q 0,10 (aile 'bh_tur4'); Y10c bilgi",
                    "regresyon": "Y10* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, "
                                 "es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y9d eşikleri AYNEN "
                                 "(yh_esik_sha_tur3 = ON_KAYIT_3.md YH_ESIK_SHA)",
                    "huni": "Y1 -> +Ş1 -> +Ş2 -> ... -> +Ş8 (= Y10) -> +F14 >= 0 (= Y10b); ayrıca Y10c (Ş2-Ş8); getirisiz, ön kayıtta"}},
        "Y10b": {"ad": "S7 + BÜYÜK RESİM", "yon": 1, "tur": 4, "taban": "Y10", "F14_min": 0.0,
                 "tanim": "Y10 olayı VE F14 >= 0 (250 bar dip noktaları eğimi aşağı değil; VD9 şart 3; F14 NaN = tutmaz)"},
        "Y10c": {"ad": "ŞEKİL KURALLARI, KONUMSUZ (bilgi)", "yon": 1, "tur": 4, "taban": "Y1", "bilgi": True,
                 "sartlar": ["S2", "S3", "S4", "S5", "S6", "S7", "S8"],
                 "tanim": "Y1 olayı VE Ş2-Ş8 (Ş1 yok): Cemal'in şekil kuralları tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi "
                          "satırı, karar değil"},
        # ---- 5. TUR (YAPI_HEDEF_IS_TANIMI_5.md §2-§3; Ş9 'U DİP + PARABOLİK DEVAM'; tasarım kontrolünden sonra ön kayıtta kilitli). Y1-Y10c
        # girdileri yukarıda AYNEN (yh_esik_sha_tur4 = 4. tur mührü ON_KAYIT_4.md YH_ESIK_SHA).
        "Y11": {"ad": "U DİP ÇEKİRDEK", "yon": 1, "tur": 5, "taban": "Y1", "sartlar": ["S1", "S2", "S9"],
                "esik": {"F24_alt_acik": 0.0, "F25_alt": 0.20, "F25_ust": 0.75, "F26_min": 0.40, "F27_min": 1.0, "F28_min": 0.5, "F29_mutlak_ust": 5.0},
                "sart_tanim": {
                    "S9": "U DİP + PARABOLİK DEVAM (K47 / K40): W = t'den önceki son 40 geçerli barın Low'u (x = 0..39, x = 39 -> t-1); "
                          "L ≈ a x² + b x + c (en küçük kareler); F24 = a / ATR > 0 VE 0,20 <= F25 = x* / 39 <= 0,75 (x* = -b / 2a) VE "
                          "F26 = R² >= 0,40 VE F27 = (uyum(0) - uyum(x*)) / ATR >= 1,0 VE F28 = (uyum(39) - uyum(x*)) / ATR >= 0,5 VE "
                          "|F29| = |argmin(L) - x*| <= 5 (x* pencere dışındaysa uyum(min(max(x*, 0), 39)); a <= 0 ise F25 / F27 / F28 / F29 "
                          "NaN; 40 bar ya da ATR yoksa NaN = tutmaz)"},
                "s9_prm": {"pencere": 40, "atr_gun": 250, "atr_min": 120, "bilgi_azami_gun": 291,
                           "tanim": "F24-F29 ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal günü (geçerli "
                                    "bar sırası i); W = Low[i-40 .. i-1]; ATR = GOZ_ETIKET F3 ATR250 tanımı (öncesi): w0 = i-40, cnt = min(250, "
                                    "w0-1), ATR_göreli = ort(TR / C_önceki, [w0-cnt, w0-1]) (cnt < 120 -> NaN); fiyat birimine pencerenin "
                                    "ortalama kapanışıyla çevrilir: ATR = ATR_göreli x ort(Close[i-40 .. i-1]); yalnız [i-291, i-1] barları "
                                    "okunur (t barı girmez); dosya ozellik_Y1_s9.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak)"},
                "tanim": "Y1 OLAYI VE Ş1 DİPTE VE Ş2 HAT NET VE Ş9 U DİP (az şart: n korunsun; her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile "
                         "AYNI; yalnız olay kümesi değişir",
                "tur5_kural": {
                    "etiket": "3. / 4. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket; ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> "
                              "etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS iki "
                              "yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Y11 / Y11b Y9'un alt kümesi (Ş1 = Y9 şartı): dış sınama "
                              "ve BIST hücreleri 'kısmen bakılmış (Y9 alt kümesi)' yazılır, 'bağımsız' denmez (4. tur H-c dersi)",
                    "bh": "Y11 / Y11b x 4 karar hücresi BH q 0,10 (aile 'bh_tur5'); BH yalnız n >= 30 hücreler arasında hesaplanır ve basılır "
                          "(4. tur H-d dersi); n < 30 hücre 'BH dışı (n < 30)'; Y11c bilgi",
                    "regresyon": "Y11* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, "
                                 "es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y10c eşikleri AYNEN "
                                 "(yh_esik_sha_tur4 = ON_KAYIT_4.md YH_ESIK_SHA)",
                    "huni": "Y1 -> +Ş1 -> +Ş2 -> +Ş9 (= Y11); Y10 (Ş1-Ş8) -> Ş6 çıkar -> +Ş9 (= Y11b); Y1 -> +Ş9 (= Y11c); pazar x dönem; "
                            "getirisiz, ön kayıtta"}},
        "Y11b": {"ad": "S7 v2 (Ş6 yerine Ş9)", "yon": 1, "tur": 5, "taban": "Y1", "sartlar": ["S1", "S2", "S3", "S4", "S5", "S9", "S7", "S8"],
                 "tanim": "Y1 olayı VE Y10'un sekiz şartı, Ş6 yerine Ş9: Ş1, Ş2, Ş3, Ş4, Ş5, Ş9, Ş7, Ş8 (eşikler Y10 / Y11 ile AYNI)"},
        "Y11c": {"ad": "Ş9 TEK BAŞINA (bilgi, konumsuz)", "yon": 1, "tur": 5, "taban": "Y1", "bilgi": True, "sartlar": ["S9"],
                 "tanim": "Y1 olayı VE Ş9 (Ş1 yok): U dip şekli tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil"},
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
    E1 = dict(E); E1["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_2 + YH_DENEMELER_3 + YH_DENEMELER_4 + YH_DENEMELER_5}
    return yh_esik_sha(E1)


def yh_esik_sha_tur2(E: Optional[Dict[str, Any]] = None) -> str:
    """YH_ESIK'ten 3. tur denemeleri çıkarılınca sha: 2. tur mührüne (ON_KAYIT_2.md YH_ESIK_SHA) EŞİT olmalı (Y1-Y8B eşikleri değişmedi kanıtı)."""
    E = YH_ESIK if E is None else E
    E2 = dict(E); E2["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_3 + YH_DENEMELER_4 + YH_DENEMELER_5}
    return yh_esik_sha(E2)


def yh_esik_sha_tur3(E: Optional[Dict[str, Any]] = None) -> str:
    """YH_ESIK'ten 4. tur denemeleri çıkarılınca sha: 3. tur mührüne (ON_KAYIT_3.md YH_ESIK_SHA) EŞİT olmalı (Y1-Y9d eşikleri değişmedi kanıtı)."""
    E = YH_ESIK if E is None else E
    E3 = dict(E); E3["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_4 + YH_DENEMELER_5}
    return yh_esik_sha(E3)


def yh_esik_sha_tur4(E: Optional[Dict[str, Any]] = None) -> str:
    """YH_ESIK'ten 5. tur denemeleri çıkarılınca sha: 4. tur mührüne (ON_KAYIT_4.md YH_ESIK_SHA) EŞİT olmalı (Y1-Y10c eşikleri değişmedi kanıtı)."""
    E = YH_ESIK if E is None else E
    E4 = dict(E); E4["denemeler"] = {k: v for k, v in E["denemeler"].items() if k not in YH_DENEMELER_5}
    return yh_esik_sha(E4)


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
    if any(k in YH_DENEMELER_5 for k in denemeler):        # 5. tur ayrı koşu (yh_kos5); önceki turların akışına dokunmaz
        return yh_kos5(list(denemeler), cikti, veri, islem, git, kontrol, Y)
    if any(k in YH_DENEMELER_4 for k in denemeler):        # 4. tur ayrı koşu (yh_kos4); önceki turların akışına dokunmaz
        return yh_kos4(list(denemeler), cikti, veri, islem, git, kontrol, Y)
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


# ================================================================ 9) 4. TUR (S7 'Cemal bölge seçici': Y10 / Y10b / Y10c; YAPI_HEDEF_IS_TANIMI_4.md)
_Y10_OZ_A = ["F1", "F2", "F3", "F4", "F11", "F14", "F15", "F17", "F18"]      # goz_etiket/ozellik_Y1.csv.gz (GOZ_ETIKET F1-F18 tanımı)
_Y10_OZ_S7 = ["F20", "F21", "F22", "F22a", "F23"]                             # yapi_hedef/ozellik_Y1_s7.csv.gz (yh_s7_ozellik)
_Y10_OZ = _Y10_OZ_A + _Y10_OZ_S7
_YH_SART = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]
_YH_OZ4_ONB: Dict[str, Any] = {}

YH_KONTROL_4: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / "
                   "takip / 15 bar); hat ve stop0 Y1 ile aynı (yalnız olay kümesi değişir); konum eşli KAT (yh_konum_es_olc, 3. tur kodu): eşin "
                   "F15'i olayın çeyreğinde (Ş1 dipte şartı momentum kovasıyla karışmasın); plasebo aynı hisse rastgele gün; güç tablosu 1. turunki"),
    "K2": ("EVET", "F1-F18 GOZ_ETIKET dosyasından (yalnız [.., t]; aşama A prefix denetimi); F20-F23 yalnız [t-15, t] (yh_s7_ozellik; dosya "
                   "üretiminde pazar başına 25 rastgele olay t'de kesik veriyle ve [t-250, t] kesitiyle yeniden = tam: denetim json); koşuda her deneme "
                   "x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 yeniden = dosya, yoksa "
                   "DURUR (yh_gelecek4); C_t / O_t sinyal günü (giriş t+1 açılış); eşin F15'i giriş gününden önceki son geçerli bar"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); F20 / F21 pencereleri "
                   "geçerli bar sayımıyla; H_t = L_t bar veride yok (F23 NaN tutmaz)"),
    "K4": ("EVET", "Y10* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz "
                   "dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan"),
    "K5": ("EVET", "giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); Ş7 O_t / C_t sinyal günü (t) değerleri, giriş "
                   "değil; regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı"),
    "K6": ("EVET", "aynı V_*.pkl tek kip; F2 / F3 / F4 / F11 / F14 / F15 / F17 / F18 / F20 / F22 / F22a / F23 oran, F1 sayı, F21 fiyat (yalnız "
                   "aynı hissenin C_t / O_t ile oranda kullanılır); AVR yerel para"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Ş1) olaylarda batan hisse "
                   "eksikliği daha büyük olabilir -> Y10 / Y10b hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır"),
    "K8": ("EVET", "huni ön kayıtta (getirisiz, Ş1..Ş8 adım adım, pazar x dönem); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç "
                   "%80; Y10 / Y10b x 4 karar hücresi BH q 0,10 (aile 'bh_tur4'); Y10c bilgi; bakılmış hücreler işaretli, etiket en fazla "
                   "EMARE; dış sınama 2016-22 ABD / AVR ayrı satır; BIST ayrı başlık; küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_4.md: YH_ESIK sha (yeni), ESIK_TUR3_SHA (= ON_KAYIT_3.md YH_ESIK_SHA: Y1-Y9d eşikleri aynen), ESIK_TUR2_SHA, "
                   "ESIK_TUR1_SHA, kod / OC / S6 / FV / GE kod / güç / Y2 sha, OZELLIK_SHA, S7_OZELLIK_SHA, Y1_OLAY_SHA; yh_kapi4 hepsini + git "
                   "kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler iş tanımı §2 AYNEN"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve özellik dosyaları (sha mühürlü; deneme x pazar 5 olay ham "
                          "veriden yeniden hesaplanıp karşılaştırılır); Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ)"),
    "K11": ("EVET", "olay_Y10*.csv.gz satır dosyaları; RAPOR_4.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; Y1 "
                    "regresyonu: ölçülen her Y10* satırı olay_Y1.csv.gz satırına eşit (DURUR); Y1 ABD 2023 n 2040 KAT5 0,9752 sonuc.json'da aynen"),
    "K12": ("EVET", "etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS EMARE iki yönlü kural); Y10c 'bilgi'; Cemal uyum tablosu 'bilgi' "
                    "(n küçük); 'iz değil' yazılmaz; sayı ve yorum ayrı; bakılmış hücre sonuçları 'bağımsız kanıt' diye sunulmaz"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y10 önekli); yasak defter dosyalarına ve tur/1-3 klasörlerine dokunulmadı "
                    "(git diff); e-posta / anahtar taraması (_yh_yaz); push yok; tur ac --no 4 KOŞULMADI (yalnız kuru örneklem sayımı); kod "
                    "değişti -> Colab'da 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


def yh_s7_bar(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, i: int, E: Dict[str, Any] = YH_ESIK) -> Dict[str, float]:
    """t = i (geçerli bar sırası) için F20, F21, F22, F22a, F23; yalnız [i-15, i] okunur. 15 bar yoksa F20 / F21 / F22 / F22a NaN."""
    Pz = E["denemeler"]["Y10"]["s7_prm"]; sag, sol, tg = int(Pz["sag"]), int(Pz["sol"]), int(Pz["tavan_gun"])
    out = {k: np.nan for k in _Y10_OZ_S7}
    if i >= sol:
        a = float(np.min(L[i - sag:i])); b = float(np.min(L[i - sol:i - sag]))
        out["F20"] = a / b - 1 if b > 0 else np.nan
    if i >= tg:
        f21 = float(np.max(H[i - tg:i]))
        if f21 > 0:
            out["F21"] = f21; out["F22"] = float(C[i] / f21 - 1); out["F22a"] = float(O[i] / f21 - 1)
    r = float(H[i] - L[i])
    out["F23"] = float(abs(C[i] - O[i]) / r) if r > 0 else np.nan
    return out


def yh_s7_ozellik(df: pd.DataFrame, tarihler: List[pd.Timestamp], hazir: bool = False, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Bir hissenin sinyal günleri için F20-F23 (+ F22a); veri _yh_hazir (geçerli bar, kriz kesiği). Gün veride yoksa YHHata."""
    d = df if hazir else _yh_hazir(df)
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
    pos = d.index.get_indexer(pd.DatetimeIndex(pd.to_datetime(list(tarihler))))
    if (pos < 0).any():
        raise YHHata("S7 özellik: sinyal günü geçerli bar değil")
    return pd.DataFrame([yh_s7_bar(O, H, L, C, int(i), E) for i in pos], columns=_Y10_OZ_S7)


def yh_s7_ozellik_yaz(veri: Optional[str] = None, cikti: Optional[str] = None, ozellik: Optional[str] = None, denetim_n: int = 25,
                      tohum: int = 1810, E: Dict[str, Any] = YH_ESIK, yol: Optional[str] = None) -> Dict[str, Any]:
    """Bütün Y1 olayları (ozellik_Y1.csv.gz anahtarları) -> ozellik_Y1_s7.csv.gz (pazar, sembol, tarih, F20-F23, F22a; 6 anlamlı basamak) +
    ozellik_Y1_s7_denetim.json. Prefix denetimi: pazar başına denetim_n rastgele olay t'de kesik veriyle ve [t-250, t] kesitiyle = tam; değilse DURUR."""
    cikti = cikti or YH_YOL["cikti"]; yol = yol or YH_YOL["ozellik_s7"]
    yo = ozellik or YH_YOL["ozellik"]
    if not os.path.exists(yo):
        raise YHHata(f"özellik dosyası yok: {yo} (GOZ_ETIKET aşama A çıktısı; S7 DURDU)")
    Fo = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"], dtype={"sembol": str, "pazar": str})
    if Fo.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata("özellik dosyasında aynı (pazar, sembol, tarih) iki kez")
    sat, den = [], {"surum": YH_SURUM, "esik_s7_sha": yh_esik_sha(E["denemeler"]["Y10"]["s7_prm"]), "ozellik_sha": _yh_sha_dosya(yo),
                    "pazar": {}}
    for p in OC.OC_ESIK["pazar"]:
        Fp = Fo[Fo.pazar == p]
        if not len(Fp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); n0 = len(sat); hz: Dict[str, pd.DataFrame] = {}
        for s, g in Fp.groupby("sembol", sort=True):
            if s not in Vd["V"]:
                raise YHHata(f"S7 özellik: {p} {s} veride yok")
            hz[s] = _yh_hazir(Vd["V"][s])
            R = yh_s7_ozellik(hz[s], list(g.tarih), hazir=True, E=E)
            for t, r in zip(g.tarih, R.itertuples(index=False)):
                sat.append({"pazar": p, "sembol": s, "tarih": pd.Timestamp(t), **r._asdict()})
        Xp = pd.DataFrame(sat[n0:])
        rng = np.random.default_rng([tohum, OC.OC_ESIK["pazar"].index(p)]); ok = 0
        for q in rng.choice(len(Xp), min(denetim_n, len(Xp)), replace=False):
            r = Xp.iloc[int(q)]; t = pd.Timestamp(r.tarih); d = hz[r.sembol]; i = int(d.index.get_loc(t))
            kes = Vd["V"][r.sembol]; kes = kes[kes.index <= t]
            a = yh_s7_ozellik(kes, [t], E=E).iloc[0].to_numpy(float)
            b = yh_s7_ozellik(d.iloc[max(0, i - int(E["denemeler"]["Y10"]["s7_prm"]["bilgi_azami_gun"])):i + 1], [t], hazir=True, E=E).iloc[0].to_numpy(float)
            c = r[_Y10_OZ_S7].to_numpy(float)
            if not (np.allclose(a, c, rtol=1e-12, atol=0, equal_nan=True) and np.allclose(b, c, rtol=1e-12, atol=0, equal_nan=True)):
                raise YHHata(f"S7 prefix denetimi TUTMADI: {p} {r.sembol} {t.date()} -> DURDU")
            ok += 1
        den["pazar"][p] = {"olay": int(len(Xp)), "prefix_tuttu": ok, "nan": {k: int(Xp[k].isna().sum()) for k in _Y10_OZ_S7}}
        yhlog.info("S7 özellik %s: %d olay, prefix %d tuttu", p, len(Xp), ok)
        del Vd, hz
    X = pd.DataFrame(sat, columns=["pazar", "sembol", "tarih"] + _Y10_OZ_S7)
    if len(X) != len(Fo):
        raise YHHata(f"S7 özellik: satır {len(X)} != özellik dosyası {len(Fo)}")
    X.to_csv(yol, index=False, float_format="%.6g", compression="gzip", date_format="%Y-%m-%d")
    den["satir"] = int(len(X)); den["sha"] = _yh_sha_dosya(yol)
    _yh_yaz(os.path.join(cikti, YH_DOSYA["s7_denetim"]), json.dumps(den, ensure_ascii=False, indent=1, default=_yh_json), "S7 denetim")
    return {"yol": yol, **den}


def yh_ozellik4_oku(ozellik: Optional[str] = None, ozellik_s7: Optional[str] = None) -> pd.DataFrame:
    """ozellik_Y1.csv.gz (F1-F18) + ozellik_Y1_s7.csv.gz (F20-F23, F22a) -> (pazar, sembol, tarih) + _Y10_OZ. Anahtar kümeleri aynı olmalı."""
    ya = ozellik or YH_YOL["ozellik"]; ys = ozellik_s7 or YH_YOL["ozellik_s7"]
    for y in (ya, ys):
        if not os.path.exists(y):
            raise YHHata(f"özellik dosyası yok: {y} (4. tur DURDU; S7 için `python YAPI_HEDEF.py s7ozellik`)")
    anahtar = (ya, _yh_sha_dosya(ya), ys, _yh_sha_dosya(ys))
    if _YH_OZ4_ONB.get("anahtar") == anahtar:
        return _YH_OZ4_ONB["F"]
    try:
        A = pd.read_csv(ya, parse_dates=["tarih"], dtype={"sembol": str}); B = pd.read_csv(ys, parse_dates=["tarih"], dtype={"sembol": str})
    except Exception as ex:
        raise YHHata(f"özellik dosyası okunamadı: {ex}")
    for X_, kol, ad in ((A, _Y10_OZ_A, ya), (B, _Y10_OZ_S7, ys)):
        eksik = [c for c in ["pazar", "sembol", "tarih"] + kol if c not in X_.columns]
        if eksik:
            raise YHHata(f"{ad}: sütun yok {eksik}")
        if X_.duplicated(["pazar", "sembol", "tarih"]).any():
            raise YHHata(f"{ad}: aynı (pazar, sembol, tarih) iki kez")
    F = A[["pazar", "sembol", "tarih"] + _Y10_OZ_A].merge(B[["pazar", "sembol", "tarih"] + _Y10_OZ_S7], on=["pazar", "sembol", "tarih"], how="outer",
                                                           validate="one_to_one", indicator=True)
    if (F._merge != "both").any():
        raise YHHata(f"4. tur: F1-F18 ve S7 dosyalarının anahtarları farklı ({int((F._merge != 'both').sum())} satır) -> DURDU")
    F = F.drop(columns="_merge")
    _YH_OZ4_ONB.clear(); _YH_OZ4_ONB.update({"anahtar": anahtar, "F": F})
    return F


def yh_s7_sartlar(F: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> Dict[str, np.ndarray]:
    """Ş1-Ş8 ve F14 (Y10b) bayrakları (NaN tutmaz). F: _Y10_OZ sütunlu çerçeve."""
    T = E["denemeler"]["Y10"]["esik"]; Tb = E["denemeler"]["Y10b"]
    g = lambda c: F[c].to_numpy(float)  # noqa: E731
    with np.errstate(invalid="ignore"):
        out = {"S1": (g("F15") <= T["F15_ust"]) & (g("F17") <= T["F17_ust"]),
               "S2": g("F1") >= T["F1_min"],
               "S3": g("F2") >= T["F2_min"],
               "S4": g("F3") <= T["F3_ust"],
               "S5": g("F4") <= T["F4_ust"],
               "S6": g("F20") >= T["F20_min"],
               "S7": (g("F22") > T["F22_alt_acik"]) & (g("F22a") < T["F22a_ust_acik"]) & (g("F23") >= T["F23_min"]),
               "S8": g("F18") <= T["F18_ust"],
               "F14": g("F14") >= Tb["F14_min"]}
    return {k: np.asarray(v, bool) for k, v in out.items()}


def yh_y10_maske(F: pd.DataFrame, deneme: str, E: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    """Y10 = Ş1-Ş8; Y10b = Y10 + F14 >= 0; Y10c = Ş2-Ş8 (bilgi)."""
    if deneme not in YH_DENEMELER_4:
        raise YHHata(f"4. tur deneme değil: {deneme}")
    if not len(F):
        return np.zeros(0, bool)
    S = yh_s7_sartlar(F, E)
    D = E["denemeler"]["Y10c" if deneme == "Y10c" else "Y10"]
    m = np.ones(len(F), bool)
    for k in D["sartlar"]:
        m &= S[k]
    if deneme == "Y10b":
        m &= S["F14"]
    return m


def yh_sinyaller4(Vd: Dict[str, Any], pazar: str, denemeler: List[str], islem: int = 1, E: Dict[str, Any] = YH_ESIK,
                  P: Optional[Dict[str, Any]] = None, ozellik: Optional[str] = None, ozellik_s7: Optional[str] = None) -> Dict[str, Any]:
    """4. tur: Y1 sinyalleri (1. tur kodu) ∩ özellik satırları (= Y1 OLAYLARI) -> '_Y10F' + deneme alt kümeleri. Regresyon 3. turdaki gibi."""
    den = [k for k in denemeler if k in YH_DENEMELER_4]
    if len(den) != len(denemeler):
        raise YHHata(f"yh_sinyaller4 yalnız 4. tur: {denemeler}")
    S1 = yh_sinyaller(Vd, pazar, ["Y1"], islem, E)["Y1"].copy()
    S1["tarih"] = pd.to_datetime(S1.tarih); S1["sembol"] = S1.sembol.astype(str)
    Fo = yh_ozellik4_oku(ozellik, ozellik_s7)
    Fp = Fo[Fo.pazar == pazar][["sembol", "tarih"] + _Y10_OZ].copy()
    X = S1.merge(Fp, on=["sembol", "tarih"], how="inner", validate="one_to_one")
    rap: Dict[str, Any] = {"y1_sinyal": int(len(S1)), "ozellik_satir": int(len(Fp)), "eslesen": int(len(X))}
    if len(X) != len(Fp):
        raise YHHata(f"4. tur regresyon: {pazar} {len(Fp) - len(X)} özellik satırı şimdiki Y1 sinyallerinde yok -> DURDU")
    if P is not None and len(S1):
        Z, _ = OC.oc_olay_hazirla(S1[["sembol", "tarih", "pazar"]], P)
        k1 = set(zip(Z.sembol.astype(str), pd.to_datetime(Z.tarih))); k2 = set(zip(Fp.sembol, Fp.tarih))
        rap["y1_olay"] = int(len(Z))
        if k1 != k2:
            raise YHHata(f"4. tur regresyon: {pazar} özellik kümesi ({len(k2)}) != Y1 olay kümesi ({len(k1)}) -> DURDU")
    out: Dict[str, Any] = {"_Y10F": X.sort_values(["sembol", "tarih"]).reset_index(drop=True), "_Y10R": rap}
    for k in den:
        out[k] = out["_Y10F"][yh_y10_maske(out["_Y10F"], k, E)].reset_index(drop=True)
    return out


def yh_huni4(S: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """GETİRİSİZ huni: Y1 olayı -> +Ş1 -> ... -> +Ş8 (= Y10) -> +F14 (= Y10b); ayrıca Y10c; her şartın Y1'den TEK BAŞINA düşürdüğü olay."""
    F = S["_Y10F"]
    if not len(F):
        return {"Y10": {"asama": [], "tek": {}}}
    Sb = yh_s7_sartlar(F, E); D = E["denemeler"]["Y10"]["sart_tanim"]
    A = [{"ad": "Y1 olayı (özellik satırı)", **_yh_say_getirisiz(F, P)}]; m = np.ones(len(F), bool)
    for k in _YH_SART:
        m = m & Sb[k]
        A.append({"ad": f"+ Ş{k[1:]} {D[k].split(' (')[0].split(':')[0]}" + (" = Y10" if k == "S8" else ""), **_yh_say_getirisiz(F[m], P)})
    A.append({"ad": "+ F14 >= 0 (büyük resim) = Y10b", **_yh_say_getirisiz(F[m & Sb["F14"]], P)})
    A.append({"ad": "(ayrı) Ş2-Ş8, Ş1 yok = Y10c (bilgi)", **_yh_say_getirisiz(F[yh_y10_maske(F, "Y10c", E)], P)})
    tek = {f"Ş{k[1:]} tutmayan": int((~Sb[k]).sum()) for k in _YH_SART}
    tek["F14 < 0 / NaN"] = int((~Sb["F14"]).sum())
    tek.update({f"{c} NaN": int(F[c].isna().sum()) for c in ("F2", "F3", "F14", "F20", "F21", "F23")})
    return {"Y10": {"asama": A, "tek": tek}}


def yh_sayim4(veri: Optional[str] = None, islem: int = 1, ozellik: Optional[str] = None, ozellik_s7: Optional[str] = None) -> Dict[str, Any]:
    """4. tur GETİRİSİZ sayım: huni + deneme başına OC olayı (dönem) + Y1 eşleşmesi. Hedef / stop / eş / konum eş HESAPLANMAZ."""
    out: Dict[str, Any] = {"huni": {}, "deneme": {}, "eslesme": {}}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); P = OC.oc_panel(Vd)
        S = yh_sinyaller4(Vd, p, YH_DENEMELER_4, islem, P=P, ozellik=ozellik, ozellik_s7=ozellik_s7)
        out["huni"][p] = yh_huni4(S, P); out["eslesme"][p] = S["_Y10R"]
        for k in YH_DENEMELER_4:
            X = S[k]
            Z, say = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P) if len(X) else (pd.DataFrame(), {})
            out["deneme"].setdefault(k, {})[p] = {"olay": {a: int(b) for a, b in (Z.donem.value_counts().to_dict() if len(Z) else {}).items() if a},
                                                  "hisse": int(X.sembol.nunique()) if len(X) else 0, "sayim": {a: int(b) for a, b in say.items()}}
        yhlog.info("sayım (4. tur) %s tamam", p)
        del Vd, P, S
    return out


def yh_sha_simdi4(cikti: Optional[str] = None) -> Dict[str, str]:
    """3. turun sha'ları + S7 özellik dosyası + GOZ_ETIKET kodu (F1-F18 geleceğe bakma yeniden hesabı ve TUR 4 örneklemi)."""
    out = yh_sha_simdi3(cikti)
    if not os.path.exists(YH_YOL["ozellik_s7"]):
        raise YHHata(f"S7 özellik dosyası yok: {YH_YOL['ozellik_s7']}")
    out["s7ozellik"] = _yh_sha_dosya(YH_YOL["ozellik_s7"]); out["gekod"] = _yh_sha_dosya(YH_YOL["ge_kod"])
    return out


_YH_KAPI_DESEN4 = {**_YH_KAPI_DESEN, "ozellik": r"OZELLIK_SHA:\s*`([0-9a-f]{64})`", "y1olay": r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`",
                   "s7ozellik": r"S7_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "gekod": r"GE_KOD_SHA:\s*`([0-9a-f]{64})`"}


def _yh_muhur_zinciri(cikti: str, metin: str) -> Dict[str, str]:
    """ESIK_TUR1/2/3_SHA (ön kayıt 4 metni) = yh_esik_sha_tur1/2/3() = ON_KAYIT.md / ON_KAYIT_2.md / ON_KAYIT_3.md YH_ESIK_SHA (+ güç tablosu)."""
    t = {1: yh_esik_sha_tur1(), 2: yh_esik_sha_tur2(), 3: yh_esik_sha_tur3()}
    dosya = {1: "onkayit", 2: "onkayit2", 3: "onkayit3"}
    for n in (1, 2, 3):
        y = _yh_yol(dosya[n], cikti)
        m = re.search(_YH_KAPI_DESEN["esik"], open(y, encoding="utf-8").read()) if os.path.exists(y) else None
        mm = re.search(rf"ESIK_TUR{n}_SHA:\s*`([0-9a-f]{{64}})`", metin) if metin else None
        if not (m and m.group(1) == t[n] and (metin is None or (mm and mm.group(1) == t[n]))):
            raise YHHata(f"4. tur: Y1-{['', 'Y5', 'Y8B', 'Y9d'][n]} eşik mührü (ESIK_TUR{n}_SHA / {YH_DOSYA[dosya[n]]}) tutmuyor -> DURDU")
    gj = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("guc_json", cikti)) else {}
    if gj.get("yh_esik_sha") != t[1]:
        raise YHHata("4. tur: güç tablosu Y1-Y5 mührü tutmuyor -> DURDU")
    return {f"t{n}": v for n, v in t.items()}


def _yh_is_tanimi4_s2(yol: Optional[str] = None) -> str:
    """İş tanımı 4 §2 (S7 TANIMI) metni aynen; yoksa YHHata."""
    yol = yol or YH_YOL["is_tanimi4"]
    if not os.path.exists(yol):
        raise YHHata(f"4. tur iş tanımı yok: {yol}")
    m = re.search(r"(?ms)^## 2\. S7 TANIMI[^\n]*\n(.*?)(?=^## 3\.)", open(yol, encoding="utf-8").read())
    if not m or not m.group(1).strip():
        raise YHHata("iş tanımı 4'te §2 S7 TANIMI bulunamadı")
    return m.group(1).strip()


def yh_onkayit4_metni(say: Dict[str, Any], sha: Dict[str, str], t: Dict[str, str], git3: Dict[str, str], git_is: Dict[str, str],
                      s2: str, s7den: Dict[str, Any]) -> str:
    Y = YH_ESIK; K = _yh_kural3(Y); D = Y["denemeler"]["Y10"]
    s = ["# YAPI_HEDEF — ÖN KAYIT 4 (4. tur: S7 'Cemal bölge seçici' Y10 / Y10b + Y10c bilgi; TUR 4 örneklemi hazırlığı)", "",
         YH_SURUM + "; 4. tur eklendi (YAPI_HEDEF_IS_TANIMI_4.md)", "",
         f"- YH_ESIK_SHA: `{sha['esik']}` (4. tur denemeleri dahil)",
         f"- ESIK_TUR3_SHA: `{t['t3']}` (YH_ESIK'ten Y10-Y10c çıkarılınca; = ON_KAYIT_3.md YH_ESIK_SHA: Y1-Y9d eşikleri AYNEN)",
         f"- ESIK_TUR2_SHA: `{t['t2']}` (= ON_KAYIT_2.md YH_ESIK_SHA)", f"- ESIK_TUR1_SHA: `{t['t1']}` (= ON_KAYIT.md YH_ESIK_SHA = güç tablosu)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)",
         f"- FV_KOD_SHA: `{sha['fv']}` (FITIL_V2.py)", f"- GE_KOD_SHA: `{sha['gekod']}` (GOZ_ETIKET.py; F1-F18 yeniden hesabı, T1.4 örneklemi)",
         f"- GUC_SHA: `{sha['guc']}` ({YH_DOSYA['guc_json']}; 1. turun güç tablosu, aynı kural)",
         f"- Y2_OLAY_SHA: `{sha['y2']}` (değişmedi; 4. turda kullanılmaz)", f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)",
         f"- S7_OZELLIK_SHA: `{sha['s7ozellik']}` (yapi_hedef/ozellik_Y1_s7.csv.gz; F20-F23, F22a)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)",
         f"- ON_KAYIT_3: git {git3.get('commit', '?')[:10]}, {git3.get('commit_zamani', '?')}",
         f"- IS_TANIMI_4: git {git_is.get('commit', '?')[:10]}, {git_is.get('commit_zamani', '?')}",
         f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "Bu dosya 4. tur ölçümünden ÖNCE yazıldı. Y10 / Y10b / Y10c için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / "
         "konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni ve olay sayımı; S7 özellik dosyası yalnız fiyat [t-15, t]). "
         "`kos --deneme Y10,Y10b,Y10c` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y9d eşik mührünü denetler; biri tutmazsa durur. "
         "Eşikler sonuç görüldükten sonra değişmez.", "",
         "## S7 TANIMI (iş tanımı 4 §2, AYNEN)", "", s2, "",
         "## BAKILMIŞ HÜCRE İŞARETİ", "",
         "- BAKILMIŞ: " + ", ".join(" ".join(x) for x in K["bakilmis"]) + ". Y10 / Y10b Y9'un alt kümesi; Y9 hücreleri 3. turda görüldü (Y10c Y1'in alt "
         "kümesi; Y1 hücreleri 1. turda görüldü). Bu hücreler karar hücreleridir ama sonuçları bağımsız kanıt değildir; etiket EN FAZLA EMARE.",
         "- DIŞ SINAMA (bağımsız kanıt): " + ", ".join(" ".join(x) for x in K["dis_sinama"]) + " (karar kuralıyla aynı 4 şart; ikisi de TUTAR -> "
         "'EMARE (dış sınama tuttu)'). NOT: Y9 dış sınama hücreleri (2016-22) 3. tur raporunda görüldü; Y10 / Y10b bunların alt kümesidir.",
         "- BIST (bilgi, ayrı başlık): " + ", ".join(" ".join(x) for x in K["bist_bilgi"]) + ".",
         "- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).", "",
         "## Ölçü, kontrol grupları, karar kuralı (1. ve 3. turla AYNI; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi)", "",
         f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- EŞ: {Y['kontrol']['es']}.",
         f"- PLASEBO: {Y['kontrol']['plasebo']}.", f"- Karar: {Y['karar']['tanim']}.", f"- Hücre durumu: {Y['etiket']['hucre']}.",
         f"- Kural etiketi (deneme başına): {Y['etiket']['genel']}", f"- 3. tur ek kuralları (4. turda AYNEN): etiket: {K['etiket']}.",
         f"- TERS: {K['ters']}.", f"- Konum eşli KAT: {K['konum_es']}.", f"- Çeyrek: {K['ceyrek_tanim']}.", f"- Konum uyumu: {K['konum_uyum']}.", "",
         "## 4. tur kuralları (önceden yazılı; DEĞİŞMEZ)", "",
         f"- Etiket: {D['tur4_kural']['etiket']}.", f"- Çoklu karşılaştırma: {D['tur4_kural']['bh']}.", f"- Regresyon: {D['tur4_kural']['regresyon']}.",
         f"- Huni: {D['tur4_kural']['huni']}.", f"- S7 özellikleri: {D['s7_prm']['tanim']}.", "",
         "## Denemeler (sonuç görülmeden sabit; iş tanımı 4 §2)", ""]
    for k in YH_DENEMELER_4:
        s.append(f"- **{k} {Y['denemeler'][k]['ad']}**: {Y['denemeler'][k]['tanim']}.")
    s += ["", "Şartlar (YH_ESIK Y10 'sart_tanim'; eşikler 'esik'):", ""] + [f"- Ş{k[1:]}: {D['sart_tanim'][k]}." for k in _YH_SART] + [
        "", "## Yorumlar (iş tanımında açık noktalar; koşudan önce sabit)", "",
        "- YORUM-1 (Ş7 açılış): O_t < F21 dosyada F22a = O_t / F21 - 1 < 0 olarak tutulur (6 anlamlı basamak; O_t = F21 -> F22a = 0 -> elenir).",
        "- YORUM-2 (F20 / F21 penceresi): t'den önceki 15 GEÇERLİ bar [t-15, t-1]; sağ = [t-5, t-1], sol = [t-15, t-6]; 15 geçerli bar yoksa NaN "
        "(şart tutmaz). Bölge (S6) ile ilgisi yok; yalnız son 15 bar.",
        "- YORUM-3 (F2 NaN): F2 dokunuş yoksa NaN; Ş2 (F1 >= 3) tutan olayda F2 tanımlıdır. Y10c'de Ş2 de şart olduğundan aynı.",
        "- YORUM-4 (Y10c bakılmış): Y10c Y1'in alt kümesidir, Y1 hücreleri 1. turda görüldü; bilgi satırıdır, 3. tur etiketi aynı kuralla yazılır.",
        "- YORUM-5 (Cemal uyumu §4): hakem setinde yalnız KÖR yarı (Cemal OLUR / OLMAZ / BELİRSİZ verdi); AÇIK yarıda yanıt modelin kararına "
        "DOĞRU / YANLIŞ olduğu için dışarıda. TUR 1 / TUR 2 bütün sayfalar. Bu bölüm h5 okumaz; Fisher OLUR / OLMAZ x S7 tutar (BELİRSİZ ayrı).",
        "- YORUM-6 (TUR 4 örneklemi): GOZ_ETIKET T1.4 olay dosyası olay_Y10.csv.gz (yalnız kimlik sütunları; ölçüm koşusunun çıktısı, sonuç "
        "sütunu okunmaz); uygun = deneme Y10, dönem 2023 / 2024-26, giriş <= kriz - 30 gün, gösterilmemiş olay / hisse. `tur ac --no 4` "
        "KOŞULMAZ; yalnız kuru örneklem (dosya yazmadan) ve uygun olay sayıları.", "",
        "## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)", "", "### Y10 hunisi", ""]
    s += _yh_huni_md(say["huni"], "Y10") + [""]
    s += ["Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): " + "; ".join(
        f"{p}: Y1 sinyal {x.get('y1_sinyal')}, Y1 olay {x.get('y1_olay', '?')}, özellik {x.get('ozellik_satir')}, eşleşen {x.get('eslesen')}"
        for p, x in say["eslesme"].items()) + ".", "",
          "S7 özellik dosyası denetimi: " + "; ".join(f"{p}: {x['olay']} olay, prefix {x['prefix_tuttu']} TUTTU, NaN " + ", ".join(f"{a} {b}" for a, b in x["nan"].items())
                                                      for p, x in s7den.get("pazar", {}).items()) + ".", "",
          "| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |", "|---|---|---|---|"]
    for k in YH_DENEMELER_4:
        for p in OC.OC_ESIK["pazar"]:
            x = say["deneme"].get(k, {}).get(p)
            if x:
                s.append(f"| {k} | {p} | {x['hisse']} | " + " / ".join(str(x["olay"].get(q, 0)) for q in _YH_DONEM3) + " |")
    s += ["", "## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)", ""]
    try:
        tablo = json.load(open(_yh_yol("guc_json"), encoding="utf-8"))
    except (OSError, ValueError):
        tablo = None
    for k in YH_DENEMELER_4:
        hc = [(p, q, int(say["deneme"].get(k, {}).get(p, {}).get("olay", {}).get(q, 0))) for p, q in Y["karar"]["hucre_karar"]]
        gs = [yh_guc_bak(n, Y["denemeler"][k]["yon"], tablo) for _, _, n in hc]
        ifade = "; ".join(f"{p} {q} en çok {n} olay (güç {_yz(g, 0)}{', n < 30 -> ÖLÇÜLEMEDİ (n)' if n < Y['karar']['n_esik'] else ''})" for (p, q, n), g in zip(hc, gs))
        az = all(n < Y["etiket"]["n_yeter"] and g < Y["etiket"]["guc_esik"] for (_, _, n), g in zip(hc, gs))
        s.append(f"- {k}{' (bilgi)' if Y['denemeler'][k].get('bilgi') else ''}: {ifade}." + (
            " Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır." if az else ""))
    s += ["- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay "
          "o satırdan düşer (k_n ayrı yazılır).",
          "- Hayatta kalma: dipteki (Ş1) hissenin batma olasılığı yüksektir; evrende batan yok -> Y10 / Y10b hedef payı ayrıca yukarı yanlı okunur.", "",
          "## YH_ESIK 4. tur girdileri (tam metin; geri kalanı ON_KAYIT.md / ON_KAYIT_2.md / ON_KAYIT_3.md ile aynı)", "", "```json",
          json.dumps({k: Y["denemeler"][k] for k in YH_DENEMELER_4}, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
          yh_kontrol_tablosu(YH_KONTROL_4), "", "## SAPMALAR", "", "(yok)", "",
          "## Test", "", "`python test_yapi_hedef.py` (önceki turların testleri aynen + 4. tur: F20-F23 yapay vakalar, prefix değişmezliği, Ş7 "
          "boşluklu açılış elenir, şart sınırları ve NaN, Y10 / Y10b / Y10c seçimi, ESIK_TUR3_SHA = 3. tur mührü, uçtan uca onkayit4 + kos + kapı "
          "+ Y1 regresyonu, önceki turların sonuçları değişmez); `python test_goz_etiket.py` (T1.4, tavan_kaynak, TUR 1-3 çıktıları değişmedi "
          "kapısı).", ""]
    return "\n".join(s)


def yh_onkayit4_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_4.md: 1-3. turlar ölçülmüş, 4. tur ölçülmemiş olmalı; Y1-Y9d eşik mührü tutmalı; özellik dosyaları = Y1 olay kümesi."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit4", cikti)
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"ön kayıt 4 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"ön kayıt 4 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 4. tur ön kaydı önceki turların ölçümünden sonra yazılır")
    J = json.load(open(sy, encoding="utf-8"))
    if [k for k in YH_DENEMELER_4 if k in J.get("deneme", {})]:
        raise YHHata("4. tur denemeleri zaten ölçülmüş: ön kayıt ölçümden sonra yazılamaz")
    if "Y1" not in J.get("deneme", {}) or "Y9" not in J.get("deneme", {}):
        raise YHHata("Y1 / Y9 ölçülmemiş: 4. tur 3. turdan sonra gelir")
    t = _yh_muhur_zinciri(cikti, None)
    sha = yh_sha_simdi4(cikti)
    git3 = _yh_git(_yh_yol("onkayit3", cikti)) if git else {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi4"]) if git else {}
    except YHHata:
        git_is = {}
    s2 = _yh_is_tanimi4_s2()
    yd = os.path.join(cikti, YH_DOSYA["s7_denetim"])
    s7den = json.load(open(yd, encoding="utf-8")) if os.path.exists(yd) else {}
    if s7den.get("sha") != sha["s7ozellik"]:
        raise YHHata("S7 denetim dosyası S7 özellik dosyasıyla eşleşmiyor (önce `python YAPI_HEDEF.py s7ozellik`)")
    say = yh_sayim4(veri, islem)
    for p in OC.OC_ESIK["pazar"]:
        x = J.get("sayim", {}).get("Y1", {}).get(p)
        if x:
            n1 = int(x["girdi"]) - int(x.get("havuz_disi", 0)) - int(x.get("tekil", 0)) - int(x.get("giris_yok", 0)) - int(x.get("giris_gec", 0))
            if n1 != say["eslesme"][p].get("y1_olay", n1):
                raise YHHata(f"regresyon: {p} Y1 olay sayısı 1. turda {n1}, şimdi {say['eslesme'][p].get('y1_olay')} -> ön kayıt yazılmadı")
    _yh_yaz(yol, yh_onkayit4_metni(say, sha, t, git3, git_is, s2, s7den), "ön kayıt 4")
    return yol


def yh_kapi4(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """4. tur koşu kapısı: ON_KAYIT_4.md kontrol listesi + bütün sha'lar + Y1-Y9d eşik mührü zinciri + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit4", cikti)
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt 4 yok: {yol}")
    metin = open(yol, encoding="utf-8").read()
    _yh_muhur_zinciri(cikti, metin)
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in _YH_KAPI_DESEN4.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"ön kayıt 4'te {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi4(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"]); out["git_guc"] = _yh_git(_yh_yol("guc_json", cikti))
        out["git_ozellik"] = _yh_git(YH_YOL["ozellik"]); out["git_s7"] = _yh_git(YH_YOL["ozellik_s7"]); out["git_ge"] = _yh_git(YH_YOL["ge_kod"])
    yhlog.info("yh_kapi4 AÇIK (%s)", yol)
    return out


def yh_gelecek4(Vd: Dict[str, Any], X: pd.DataFrame, deneme: str, pazar: str, Y: Dict[str, Any] = YH_ESIK) -> int:
    """Rastgele 5 olay: veri t'de kesilir; Y1 sinyali (aynı stop0, son sinyal t) + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 kesik
    veriden yeniden = dosya (göreli 1e-5); değilse YHHata."""
    import GOZ_ETIKET as GE
    G = Y["gelecek_denetimi"]
    if not len(X):
        return 0
    rng = np.random.default_rng([G["tohum"], YH_DENEMELER_HEPSI.index(deneme), OC.OC_ESIK["pazar"].index(pazar)])
    n = 0
    for r in X.iloc[rng.choice(len(X), min(G["n"], len(X)), replace=False)].itertuples():
        t = pd.Timestamp(r.tarih); df = Vd["V"][r.sembol]; kes = df[df.index <= t]
        X1, _ = yh_s6_hisse(kes, Y)
        z = X1[pd.to_datetime(X1.tarih) == t] if len(X1) else X1
        ok = len(z) == 1 and abs(float(z.stop0.iloc[0]) - float(r.stop0)) <= 1e-9 * max(1.0, abs(float(r.stop0))) and pd.Timestamp(X1.tarih.iloc[-1]) == t
        if ok:
            Fs, _ = GE.ge_ozellik_hisse(kes, [t])
            a = np.array([Fs[0][c] for c in _Y10_OZ_A], float)
            b = yh_s7_ozellik(kes, [t], E=Y).iloc[0].to_numpy(float)
            ok = bool(np.allclose(np.r_[a, b], np.array([getattr(r, c) for c in _Y10_OZ], float), rtol=1e-5, atol=1e-7, equal_nan=True))
        if not ok:
            raise YHHata(f"geleceğe bakma denetimi TUTMADI: {deneme} {pazar} {r.sembol} {t.date()}")
        n += 1
    return n


def _yh_cemal_norm(v: Any) -> Optional[str]:
    if isinstance(v, dict):
        v = v.get("cevap", v.get("B"))
    if v is None:
        return None
    s = str(v).strip().upper().translate(str.maketrans({"İ": "I", "Ş": "S", "Ğ": "G", "Ü": "U", "Ö": "O", "Ç": "C"}))
    return {"OLUR": "OLUR", "✓": "OLUR", "✔": "OLUR", "V": "OLUR", "OLMAZ": "OLMAZ", "X": "OLMAZ", "✗": "OLMAZ", "BELIRSIZ": "BELİRSİZ",
            "?": "BELİRSİZ"}.get(s)


def yh_cemal_sayfalar(ge_cikti: Optional[str] = None) -> pd.DataFrame:
    """Cemal'in etiketlediği sayfalar (hakem KÖR yarı + TUR 1 + TUR 2) -> DataFrame[set, sayfa, pazar, sembol, tarih, cemal]. Sonuç sütunu yok."""
    gc = ge_cikti or YH_YOL["ge_cikti"]; sat = []
    yk = lambda *a: os.path.join(gc, *a)  # noqa: E731
    try:
        A0 = json.load(open(yk("anahtar.json"), encoding="utf-8"))["olay"]; Hk = json.load(open(yk("hakem_anahtar.json"), encoding="utf-8"))["sayfa"]
        Ch = json.load(open(yk("hakem_cevap_cemal_duz.json"), encoding="utf-8"))
    except (OSError, ValueError, KeyError) as ex:
        raise YHHata(f"Cemal hakem dosyaları okunamadı: {ex}")
    for k, v in Hk.items():
        if v.get("yari") != "KÖR" or k not in Ch:
            continue
        o = A0[str(v["no"])]
        sat.append({"set": "hakem (KÖR)", "sayfa": int(k), "pazar": o["pazar"], "sembol": str(o["sembol"]), "tarih": pd.Timestamp(o["tarih"]),
                    "cemal": _yh_cemal_norm(Ch[k])})
    for n in (1, 2):
        try:
            A = json.load(open(yk("tur", str(n), f"tur_{n}_anahtar.json"), encoding="utf-8"))["sayfa"]
            C = json.load(open(yk("tur", str(n), f"tur_{n}_cemal.json"), encoding="utf-8"))
        except (OSError, ValueError, KeyError) as ex:
            raise YHHata(f"TUR {n} Cemal dosyaları okunamadı: {ex}")
        C = C.get("cevap", C) if isinstance(C, dict) else C
        for k, v in C.items():
            o = A[str(k)]
            sat.append({"set": f"TUR {n}", "sayfa": int(k), "pazar": o["pazar"], "sembol": str(o["sembol"]), "tarih": pd.Timestamp(o["tarih"]),
                        "cemal": _yh_cemal_norm(v)})
    return pd.DataFrame(sat)


def yh_cemal_uyum4(F: Optional[pd.DataFrame] = None, ge_cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """§4 CEMAL'İN GÖZÜYLE UYUM (bilgi; h5 OKUNMAZ): sayfa başına Ş1-Ş8 / F14 -> Cemal OLUR / OLMAZ / BELİRSİZ x (tutar / tutmaz) + şart başına
    Cemal OLUR payı + Fisher (OLUR / OLMAZ x tutar, iki yönlü)."""
    from scipy.stats import fisher_exact
    F = yh_ozellik4_oku() if F is None else F
    D = yh_cemal_sayfalar(ge_cikti)
    M = D.merge(F, on=["pazar", "sembol", "tarih"], how="left", validate="many_to_one", indicator=True)
    if (M._merge != "both").any():
        raise YHHata(f"Cemal sayfaları özellik dosyasında yok: {int((M._merge != 'both').sum())}")
    Sb = yh_s7_sartlar(M, Y)
    bay = {**{k: Sb[k] for k in _YH_SART + ["F14"]}, **{k: yh_y10_maske(M, k, Y) for k in YH_DENEMELER_4}}
    out: Dict[str, Any] = {"n": int(len(M)), "set": {k: int(v) for k, v in M.set.value_counts().items()},
                           "cemal": {k: int(v) for k, v in M.cemal.fillna("yanıtsız").value_counts().items()}, "tablo": [], "sart": []}
    for st in ["hepsi"] + sorted(M.set.unique()):
        g = (M.set == st).to_numpy() if st != "hepsi" else np.ones(len(M), bool)
        for k in YH_DENEMELER_4:
            b = bay[k]; c = M.cemal.to_numpy(object)
            r = {"set": st, "deneme": k}
            for cl in ("OLUR", "OLMAZ", "BELİRSİZ"):
                r[f"{cl}_tutar"] = int((g & b & (c == cl)).sum()); r[f"{cl}_tutmaz"] = int((g & ~b & (c == cl)).sum())
            tb = [[r["OLUR_tutar"], r["OLUR_tutmaz"]], [r["OLMAZ_tutar"], r["OLMAZ_tutmaz"]]]
            r["fisher_p"] = float(fisher_exact(tb)[1]) if sum(map(sum, tb)) else np.nan
            out["tablo"].append(r)
    c = M.cemal.to_numpy(object); karar = np.isin(c, ["OLUR", "OLMAZ"])
    for k in _YH_SART + ["F14"]:
        b = bay[k]
        a1, a0 = int((b & (c == "OLUR")).sum()), int((b & (c == "OLMAZ")).sum()); z1, z0 = int((~b & (c == "OLUR")).sum()), int((~b & (c == "OLMAZ")).sum())
        out["sart"].append({"sart": k, "tutar": int(b.sum()), "tutar_karar": int((b & karar).sum()), "olur_pay_tutar": a1 / (a1 + a0) if a1 + a0 else np.nan,
                            "tutmaz_karar": int((~b & karar).sum()), "olur_pay_tutmaz": z1 / (z1 + z0) if z1 + z0 else np.nan,
                            "fisher_p": float(fisher_exact([[a1, z1], [a0, z0]])[1]) if a1 + a0 + z1 + z0 else np.nan})
    return out


def yh_tur4_orneklem_bilgi(satir_yol: str) -> Dict[str, Any]:
    """TUR 4 hazırlığı (GOZ_ETIKET T1.4; DOSYA YAZMADAN): uygun olay (deneme Y10, dönem 2023 / 2024-26, giriş <= kriz - 30) ve gösterilmemiş
    olay / hisse sayıları (pazar x dönem) + ge_tur_orneklem(4) kuru koşusu (kota doldu mu). Yalnız kimlik sütunları okunur."""
    import GOZ_ETIKET as GE
    E = GE.ge_tur_esik(4)
    X = GE.ge_olay_oku(GE.GE_KIMLIK_KOL, satir_yol); X["sembol"] = X.sembol.astype(str)
    olay_g, hisse_g = GE.ge_tur_gosterilen(4)
    sinir = pd.Timestamp(GE.GE_ESIK["kriz"]) - pd.Timedelta(days=int(E["giris_kriz_pay_gun"]))
    U = X[(X.deneme == E["deneme"]) & X.donem.isin(list(E["donem"])) & (X.giris <= sinir)].copy()
    U["goster"] = [(p, s, str(t.date())) in olay_g or (p, s) in hisse_g for p, s, t in zip(U.pazar, U.sembol, U.tarih)]
    out: Dict[str, Any] = {"surum": E["surum"], "kota": {p: int(k) for p, k in E["katman"]}, "uygun": {}, "gosterilmemis": {}, "hisse_gosterilmemis": {}}
    for p in OC.OC_ESIK["pazar"]:
        for q in E["donem"]:
            x = U[(U.pazar == p) & (U.donem == q)]
            out["uygun"][f"{p} {q}"] = int(len(x)); out["gosterilmemis"][f"{p} {q}"] = int((~x.goster).sum())
        out["hisse_gosterilmemis"][p] = int(U[(U.pazar == p) & ~U.goster].sembol.nunique())
    try:
        S = GE.ge_tur_orneklem(4, satir_yol, None, E)
        out["kuru"] = {"durum": "KOTA DOLDU", "n": int(len(S)), "dagilim": {f"{a} {b}": int(v) for (a, b), v in S.groupby(["pazar", "donem"]).size().items()}}
    except GE.GEHata as ex:
        out["kuru"] = {"durum": "DURDU (kota dolmadı; kota düşürülmez, ana model karar verir)", "neden": str(ex)}
    return out


def yh_kos4(denemeler: List[str], cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True,
            kontrol: bool = True, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """4. tur koşusu: kapı -> Y1 sinyali ∩ özellikler -> Y10* ölçüm (1. tur kodu) -> konum eşli KAT -> Y1 regresyonu -> Cemal uyumu ->
    TUR 4 örneklem bilgisi -> sonuc.json / RAPOR_4.md."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]
    if any(k not in YH_DENEMELER_4 for k in denemeler):
        raise YHHata(f"4. tur denemeleri başka turla aynı koşuda olmaz: {denemeler}")
    denemeler = [k for k in YH_DENEMELER_4 if k in denemeler]
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 4. tur önceki turlardan sonra koşar")
    sonuc = json.load(open(sy, encoding="utf-8"))
    tekrar = [k for k in denemeler if k in sonuc.get("deneme", {})]
    if tekrar:
        raise YHHata(f"bu denemeler zaten ölçüldü (ölçüm bir kez koşulur): {tekrar}")
    ok = yh_kapi4(cikti, git=git, kontrol=kontrol)
    kos_zaman = _yh_simdi()
    if ok["onkayit_zaman"] > kos_zaman:
        raise YHHata("ön kayıt zamanı koşu zamanından sonra")
    tablo = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    O1 = pd.read_csv(_yh_y1_satir_yolu(sonuc, cikti), parse_dates=["tarih", "giris"], dtype={"sembol": str})
    sonuc["kos"].append({"zaman_utc": kos_zaman, "kapi": ok, "denemeler": denemeler, "islem": islem})
    K = _yh_kural3(Y); Ols: Dict[str, List[pd.DataFrame]] = {k: [] for k in denemeler}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
        S = yh_sinyaller4(Vd, p, denemeler, islem, Y, P=P)
        sonuc.setdefault("huni4", {})[p] = yh_huni4(S, P, Y); sonuc.setdefault("y10_eslesme", {})[p] = S["_Y10R"]
        F15p = yh_f15_panel(P, Vd, Y)
        for k in denemeler:
            X = S.get(k, pd.DataFrame())
            sonuc["gelecek_denetimi"].setdefault(k, {})[p] = yh_gelecek4(Vd, X, k, p, Y)
            Z, say = yh_olc_pazar(Vd, P, Cl, X, k, p, islem, Y)
            dus = {a: int(say.get(a, 0)) for a in ("giris_yok", "giris_gec", "havuz_disi", "tekil")}
            if any(dus.values()):
                raise YHHata(f"{k} {p}: Y1 olay alt kümesi OC'de düştü {dus} (Y10 ⊆ Y1 olayı bozuk) -> DURDU")
            if len(Z):
                Z = Z.merge(X[["sembol", "tarih"] + _Y10_OZ].assign(tarih=pd.to_datetime(X.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
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
        sonuc["deneme"][k]["tur"] = 4
        if len(Ol):
            sonuc["deneme"][k]["satir_dosya"] = os.path.relpath(yh_satir_yaz(Ol, k, cikti), KOK_YH)
    anahtar, pler = [], []
    for k in [x for x in YH_DENEMELER_4 if not Y["denemeler"][x].get("bilgi")]:
        for h in sonuc["deneme"].get(k, {}).get("hucre", []):
            if h.get("karar_hucre"):
                anahtar.append((k, h["pazar"], h["donem"])); pler.append(h.get("h5_p", np.nan))
    sonuc["bh_tur4"] = [{"deneme": a, "pazar": b, "donem": c, "p": p, "bh_q10": g} for (a, b, c), p, g in zip(anahtar, pler, _yh_bh(pler, 0.10))]
    gercek = os.path.abspath(cikti) == os.path.abspath(os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef"))
    sonuc["cemal_uyum_tur4"] = yh_cemal_uyum4(None, None, Y) if gercek else {"not": "test / başka çıktı klasörü: hesaplanmadı"}
    sd = sonuc["deneme"].get("Y10", {}).get("satir_dosya")
    if sd and gercek:
        sonuc["tur4_orneklem"] = yh_tur4_orneklem_bilgi(sd if os.path.isabs(sd) else os.path.join(KOK_YH, sd))
    sonuc.setdefault("hata_tur4", [])
    sonuc["sure_sn"] = round(sonuc.get("sure_sn", 0) + time.time() - t0, 1)
    _yh_yaz(sy, json.dumps(sonuc, ensure_ascii=False, indent=1, default=_yh_json), "sonuç")
    return {"sonuc": sonuc, "rapor": yh_rapor4(cikti)}


def yh_rapor4(cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> str:
    """4. tur raporu (RAPOR_4.md): Y10 / Y10b (+ Y10c bilgi), huni, hücre (bakılmış işaretli), konum eşli KAT, olasılık, dış sınama, BIST,
    iki yönlü etiket, Cemal uyumu (§4), TUR 4 örneklemi. RAPOR / RAPOR_2 / RAPOR_3'e dokunmaz."""
    cikti = cikti or YH_YOL["cikti"]
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    den = [k for k in YH_DENEMELER_4 if k in J["deneme"]]
    if not den:
        raise YHHata("sonuc.json'da 4. tur denemesi yok")
    K = _yh_kural3(Y)
    k4 = [k for k in J["kos"] if any(x in YH_DENEMELER_4 for x in k["denemeler"])][-1]
    kh = lambda D: {(h["pazar"], h["donem"]): h for h in D["hucre"]}  # noqa: E731

    def isaret(h: Dict[str, Any]) -> str:
        if h.get("bakilmis"):
            return "BAKILMIŞ"
        if h.get("dis_sinama"):
            return "DIŞ SINAMA"
        return "BIST bilgi" if h["pazar"] == "BIST" else "bilgi"
    s = ["# YAPI_HEDEF — RAPOR 4 (4. tur: S7 'Cemal bölge seçici' Y10 / Y10b + Y10c bilgi; konum eşli KAT; TUR 4 örneklemi)", "",
         f"{J['surum']}. Koşu: {k4['zaman_utc']} ({', '.join(k4['denemeler'])}). Ön kayıt 4: {k4['kapi'].get('onkayit_zaman', '?')} "
         f"(git {k4['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}).", "",
         "## 1. SONUÇ (etiket önceden yazılı kuralla; EN FAZLA EMARE: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ)", "",
         "| Deneme | ETİKET (4. tur = 3. tur kuralı) | kural etiketi | İKİ YÖNLÜ (TERS) | dış sınama ABD / AVR 2016-22 | karar hücreleri: durum (n, KAT5, konum eşli KAT5 [n], plasebo KAT5) — ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26 |",
         "|---|---|---|---|---|---|"]
    for k in den:
        D = J["deneme"][k]; h_ = kh(D)
        hc = " · ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' / TERS' if h_.get(tuple(x), {}).get('ters') else ''} (n {h_.get(tuple(x), {}).get('n', 0)}, "
                        f"KAT5 {_sy(h_.get(tuple(x), {}).get('h5_kat'))}, konum {_sy(h_.get(tuple(x), {}).get('k_h5_kat'))} [{h_.get(tuple(x), {}).get('k_n', 0)}], "
                        f"plasebo {_sy(h_.get(tuple(x), {}).get('pl_h5_kat'))})" for x in Y["karar"]["hucre_karar"])
        ds = " / ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' TERS' if h_.get(tuple(x), {}).get('ters') else ''}" for x in K["dis_sinama"])
        s.append(f"| {k} {D['ad']}{' (BİLGİ, karar değil)' if D.get('bilgi') else ''} | **{D['etiket']}** | {D.get('etiket_kural', '-')} | "
                 f"{D.get('ters_etiket', '-')} | {ds} | {hc} |")
    s += ["", f"Etiket kuralı (3. tur, AYNEN): {K['etiket']}.", f"TERS: {K['ters']}.", "",
          "DÜRÜSTLÜK: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ (Y10 / Y10b Y9'un alt kümesi; Y9 hücreleri 3. turda görüldü); bağımsız olan dış "
          "sınama (2016-22 ABD / AVR) ve BIST hücreleridir. Asıl karar Mart 2027 ileri testidir (kriz sonrası veri, aynı eşik).", "",
          "## 2. HUNİ (Y1 olayından şart şart; getirisiz)", ""]
    olcum = {k: {(h["pazar"], h["donem"]): h.get("n", 0) for h in J["deneme"][k]["hucre"] if h["donem"] in _YH_DONEM3} for k in den}
    s += _yh_huni_md(J.get("huni4", {}), "Y10", {a: olcum[a] for a in den})
    s += ["", "Y1 eşleşmesi: " + "; ".join(f"{p}: Y1 olay {x.get('y1_olay', '?')} = özellik satırı {x.get('ozellik_satir')} (eşleşen {x.get('eslesen')})"
                                           for p, x in J.get("y10_eslesme", {}).items()) + ".", "",
          "## 3. OLAY SAYIMI ve DENETİMLER", "",
          "| Deneme | Pazar | girdi | düşen (giriş / havuz / tekil) | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma (5 olay, F1-F23) | F15 çeyrek uyumu | Y1 regresyonu (satır) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for p, x in J["sayim"].get(k, {}).items():
            rg = J.get("regresyon_y1", {}).get(k, {}).get(p, {})
            s.append(f"| {k} | {p} | {x.get('girdi', 0)} | {x.get('giris_yok', 0) + x.get('havuz_disi', 0) + x.get('tekil', 0)} | {x.get('giris_stop_otesi', 0)} | "
                     f"{x.get('olc15_yok', 0)} | {x.get('es_az', 0)} | {x.get('plasebo_yok', 0)} | {J['gelecek_denetimi'].get(k, {}).get(p, '-')} TUTTU | "
                     f"{'%' + format(x.get('ceyrek_uyum_binde', 0) / 10, '.1f') if 'ceyrek_uyum_binde' in x else '-'} | {'EŞİT ' + str(rg.get('n')) if rg.get('esit') else '-'} |")
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
    s += ["", "## 7. DIŞ SINAMA (2016-22 ABD / AVR)", ""] + alt_tablo(K["dis_sinama"])
    s += ["", "Dış sınama kararı: " + "; ".join(f"{k}: TUTAR {'evet' if J['deneme'][k].get('dis_sinama_tutar') else 'hayır'}, TERS "
                                                 f"{'evet' if J['deneme'][k].get('dis_sinama_ters') else 'hayır'}" for k in den) + "."]
    s += ["", "## 8. BIST (bilgi; ayrı başlık; karar değil)", ""] + alt_tablo(K["bist_bilgi"])
    s += ["", "## 9. İKİ YÖNLÜ ETİKET (TERS EMARE kuralı; karar hücreleri)", "", "| Deneme | Hücre | n | KAT5 [%95] | üst < 1 | yarı 1 / yarı 2 | TERS |",
          "|---|---|---|---|---|---|---|"]
    for k in den:
        hk = kh(J["deneme"][k])
        for x in Y["karar"]["hucre_karar"]:
            h = hk.get(tuple(x), {}); u = h.get("h5_ust")
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
    s += ["", "## 11. ÇOKLU KARŞILAŞTIRMA (bilgi; Y10 / Y10b karar hücreleri KAT5 bootstrap p = P(KAT <= 1), BH q 0,10; aile 'bh_tur4')", "",
          "| Deneme | Hücre | p | BH geçer |", "|---|---|---|---|"]
    for b in J.get("bh_tur4", []):
        s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {_sy(b['p'], 3)} | {'evet' if b['bh_q10'] else 'hayır'} |")
    U = J.get("cemal_uyum_tur4", {})
    s += ["", "## 12. CEMAL'İN GÖZÜYLE UYUM (bilgi; ölçümden bağımsız, sonuç h5 OKUNMAZ; yalnız etiket ve özellik)", "",
          f"Sayfa: {U.get('n', 0)} (" + ", ".join(f"{a} {b}" for a, b in U.get("set", {}).items()) + "); Cemal: " + ", ".join(f"{a} {b}" for a, b in U.get("cemal", {}).items())
          + ". Hakem setinde yalnız KÖR yarı (AÇIK yarı yanıtı modelin kararına DOĞRU / YANLIŞ). n küçük: Fisher p bilgi.", "",
          "| Küme | Deneme | OLUR: tutar / tutmaz | OLMAZ: tutar / tutmaz | BELİRSİZ: tutar / tutmaz | tutanlarda OLUR payı | tutmayanlarda OLUR payı | Fisher p (OLUR / OLMAZ x tutar) |",
          "|---|---|---|---|---|---|---|---|"]
    for r in U.get("tablo", []):
        a1, a0, z1, z0 = r["OLUR_tutar"], r["OLMAZ_tutar"], r["OLUR_tutmaz"], r["OLMAZ_tutmaz"]
        s.append(f"| {r['set']} | {r['deneme']} | {a1} / {z1} | {a0} / {z0} | {r['BELİRSİZ_tutar']} / {r['BELİRSİZ_tutmaz']} | "
                 f"{_yz(a1 / (a1 + a0)) if a1 + a0 else '-'} ({a1}/{a1 + a0}) | {_yz(z1 / (z1 + z0)) if z1 + z0 else '-'} ({z1}/{z1 + z0}) | {_sy(r['fisher_p'], 3)} |")
    s += ["", "Şart başına (bütün sayfalar; OLUR payı = OLUR / (OLUR + OLMAZ)):", "",
          "| Şart | tutan sayfa | tutanlarda karar (OLUR+OLMAZ) / OLUR payı | tutmayanlarda karar / OLUR payı | Fisher p |", "|---|---|---|---|---|"]
    for r in U.get("sart", []):
        ad = r["sart"] if r["sart"] == "F14" else f"Ş{r['sart'][1:]}"
        s.append(f"| {ad} | {r['tutar']} | {r['tutar_karar']} / {_yz(r['olur_pay_tutar'])} | {r['tutmaz_karar']} / {_yz(r['olur_pay_tutmaz'])} | {_sy(r['fisher_p'], 3)} |")
    T4 = J.get("tur4_orneklem", {})
    s += ["", "## 13. TUR 4 ÖRNEKLEMİ (GOZ_ETIKET T1.4; `tur ac --no 4` KOŞULMADI; yalnız sayım ve kuru örneklem, dosya yazılmadı)", ""]
    if T4:
        s += [f"Sürüm {T4.get('surum')}; kota " + ", ".join(f"{a} {b}" for a, b in T4.get("kota", {}).items()) + ".", "",
              "| Pazar x dönem | uygun Y10 olayı (giriş <= kriz - 30 g) | gösterilmemiş |", "|---|---|---|"]
        for a, b in T4.get("uygun", {}).items():
            s.append(f"| {a} | {b} | {T4.get('gosterilmemis', {}).get(a, 0)} |")
        s += ["", "Gösterilmemiş hisse (pazar başına, turda hisse en çok 1): " + ", ".join(f"{a} {b}" for a, b in T4.get("hisse_gosterilmemis", {}).items()) + ".",
              f"Kuru örneklem: {T4.get('kuru', {}).get('durum', '-')}" + (f" ({T4['kuru'].get('neden')})" if T4.get("kuru", {}).get("neden") else "")
              + (f"; dağılım " + ", ".join(f"{a} {b}" for a, b in T4["kuru"].get("dagilim", {}).items()) if T4.get("kuru", {}).get("dagilim") else "") + "."]
    else:
        s.append("(hesaplanmadı)")
    s += ["", "## 14. VERİ SINIRLARI", ""]
    for p, n_ in J.get("veri_not", {}).items():
        s.append(f"- {p}: " + "; ".join(n_))
    s += ["- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.",
          "- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı; DİPTE (Ş1) olaylarda bu yanlılık daha "
          "büyük olabilir (eş ve plasebo aynı evrenden).",
          "- Sonradan bilgi: ABD / AVR 2023 ve 2024-26 hücreleri bakılmış (Y9 3. turda görüldü); Cemal'in kuralları (C1-C13, VD) hakem / tur "
          "sayfalarına bakılarak yazıldı (bölüm 12'deki sayfalar).", "",
          "## 15. YENİDEN ÜRETİM (satır dosyasından iki hücre; biri konum eşli)", "", "```",
          "python - <<'EOF'", "import pandas as pd",
          "for d, p, q in [('Y10c', 'ABD', '2024-26'), ('Y10', 'ABD', '2016-22')]:",
          "    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q)]",
          "    a = x[x.h5.notna() & x.es_h5.notna()]; b = x[x.h5.notna() & x.k_es_h5.notna()]",
          "    print(d, p, q, len(a), round(a.h5.sum() / a.es_h5.sum(), 4), round(a.st5.mean(), 4), round(a.es_st5.mean(), 4), len(b), round(b.h5.sum() / b.k_es_h5.sum(), 4))",
          "EOF", "```", "", "Satır dosyası 5 MB'ı aşarsa scratch yolundadır (sonuc.json 'satir_dosya').", "",
          yh_kontrol_tablosu(YH_KONTROL_4), "", "## HATA", ""]
    hl = J.get("hata_tur4", [])
    s += [f"- {x}" for x in hl] if hl else ["(yok)"]
    metin = "\n".join(s) + "\n"
    _yh_yaz(_yh_yol("rapor4", cikti), metin, "rapor 4")
    return metin


# ================================================================ 10) 5. TUR (Ş9 'U DİP + PARABOLİK DEVAM': Y11 / Y11b / Y11c; YAPI_HEDEF_IS_TANIMI_5.md)
_Y11_OZ_S9 = ["F24", "F25", "F26", "F27", "F28", "F29"]                         # yapi_hedef/ozellik_Y1_s9.csv.gz (yh_s9_ozellik)
_Y11_OZ = _Y10_OZ + _Y11_OZ_S9
_YH_SART5 = _YH_SART + ["S9"]
_YH_OZ5_ONB: Dict[str, Any] = {}
_YH_TASARIM_TUR2 = [1, 3, 11, 22]          # Cemal'in TUR 2'de OLUR deyip kazan çizdiği sayfalar (iş tanımı 5 §2 (b))
_YH_TASARIM_NO = 38                         # S7 PDF'i No 38 (AVR 2016-22, s7_bolge_pdf sırasıyla AVR listesinden 7. olay; (a))
YH_DOSYA.update({"onkayit5": "ON_KAYIT_5.md", "rapor5": "RAPOR_5.md", "s9_denetim": "ozellik_Y1_s9_denetim.json", "tasarim5": "tasarim5.json"})
YH_YOL["is_tanimi5"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_IS_TANIMI_5.md")
YH_YOL["ozellik_s9"] = os.environ.get("YH_OZELLIK_S9", os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "ozellik_Y1_s9.csv.gz"))
YH_YOL["s7_pdf_kod"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "s7_bolge_pdf.py")

YH_KONTROL_5: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / "
                   "takip / 15 bar); hat ve stop0 Y1 ile aynı (yalnız olay kümesi değişir); konum eşli KAT (yh_konum_es_olc): eşin F15'i olayın "
                   "çeyreğinde (Ş1 dipte şartı momentum kovasıyla karışmasın); plasebo aynı hisse rastgele gün; güç tablosu 1. turunki"),
    "K2": ("EVET", "F1-F23 4. turun mühürlü dosyalarından; F24-F29 yalnız [t-291, t-1] (yh_s9_ozellik; t barı girmez; dosya üretiminde pazar "
                   "başına 25 rastgele olay t'de kesik veriyle ve [t-291, t] kesitiyle yeniden = tam: denetim json); koşuda her deneme x pazar 5 "
                   "rastgele olay: veri t'de kesilir, Y1 sinyali + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 + F24-F29 yeniden = dosya, yoksa "
                   "DURUR (yh_gelecek5); giriş t+1 açılış; eşin F15'i giriş gününden önceki son geçerli bar"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); Ş9 penceresi (40) ve ATR "
                   "(250, en az 120) geçerli bar sayımıyla; 40 bar ya da ATR yoksa NaN = tutmaz"),
    "K4": ("EVET", "Y11* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz "
                   "dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan"),
    "K5": ("EVET", "giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); Ş9 yalnız t'den önceki Low'lar; regresyon: ölçülen "
                   "satırlar olay_Y1.csv.gz ile aynı"),
    "K6": ("EVET", "aynı V_*.pkl tek kip; F24 / F27 / F28 fiyat farkı / ATR (ATR = göreli ATR250 x pencerenin ortalama kapanışı: birimsiz), F25 / "
                   "F26 oran, F29 bar; AVR yerel para (birimden bağımsız)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Ş1) olaylarda batan hisse "
                   "eksikliği daha büyük olabilir -> Y11 / Y11b hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır"),
    "K8": ("EVET", "huni ön kayıtta (getirisiz, Y1 -> Ş1 -> Ş2 -> Ş9; Y10 -> Ş6 çıkar -> Ş9; Y1 -> Ş9; pazar x dönem); n < 30 ÖLÇÜLEMEDİ; "
                   "DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; Y11 / Y11b x 4 karar hücresi BH q 0,10 yalnız n >= 30 hücreler (aile "
                   "'bh_tur5'); Y11c bilgi; bakılmış hücreler işaretli, etiket en fazla EMARE; dış sınama / BIST 'kısmen bakılmış (Y9 alt kümesi)'; "
                   "küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_5.md: YH_ESIK sha (yeni), ESIK_TUR4_SHA (= ON_KAYIT_4.md YH_ESIK_SHA: Y1-Y10c eşikleri aynen), ESIK_TUR3/2/1_SHA, "
                   "kod / OC / S6 / FV / GE kod / güç / Y2 sha, OZELLIK_SHA, S7_OZELLIK_SHA, S9_OZELLIK_SHA, TASARIM5_SHA, Y1_OLAY_SHA; yh_kapi5 "
                   "hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; tasarım kontrolü (No 38 + TUR 2 kazan sayfaları) ön kayıttan ÖNCE, h5 / "
                   "st5 / getiri okunmadan, bir kez; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler iş tanımı §2 (tasarım ayarı dışında) AYNEN"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve özellik dosyaları (sha mühürlü; deneme x pazar 5 olay ham "
                          "veriden yeniden hesaplanıp karşılaştırılır); Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ)"),
    "K11": ("EVET", "olay_Y11*.csv.gz satır dosyaları; RAPOR_5.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; İLERLEME tablosu "
                    "satır dosyalarından yeniden hesaplanır ve sonuc.json hücreleriyle karşılaştırılır; Y1 regresyonu: ölçülen her Y11* satırı "
                    "olay_Y1.csv.gz satırına eşit (DURUR)"),
    "K12": ("EVET", "etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS EMARE iki yönlü kural); Y11c 'bilgi'; Cemal uyum tablosu 'bilgi' "
                    "(n küçük); 'iz değil' yazılmaz; 'bağımsız' sözü yerine 'kısmen bakılmış (Y9 alt kümesi)'; sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y11 önekli); yasak defter dosyalarına ve tur/1-3 klasörlerine dokunulmadı "
                    "(git diff); e-posta / anahtar taraması (_yh_yaz); push yok; `tur ac --no 4` KOŞULMADI (yalnız T1.5 kuru örneklem sayımı); kod "
                    "değişti -> Colab'da 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


def yh_s9_bar(H: np.ndarray, L: np.ndarray, C: np.ndarray, i: int, E: Dict[str, Any] = YH_ESIK) -> Dict[str, float]:
    """t = i (geçerli bar sırası) için F24-F29; yalnız [i-291, i-1] okunur (t barı girmez). 40 bar ya da ATR (>= 120 bar) yoksa NaN."""
    Pz = E["denemeler"]["Y11"]["s9_prm"]; n = int(Pz["pencere"])
    out = {k: np.nan for k in _Y11_OZ_S9}
    if i < n:
        return out
    w0 = i - n
    cnt = min(int(Pz["atr_gun"]), w0 - 1)
    if cnt < int(Pz["atr_min"]):
        return out
    trp = _yh_trp(H[w0 - cnt - 1:w0], L[w0 - cnt - 1:w0], C[w0 - cnt - 1:w0])[1:]
    atr_g = float(np.mean(trp))
    Lw = np.asarray(L[w0:i], float); Cw = np.asarray(C[w0:i], float)
    atr = atr_g * float(np.mean(Cw))
    if not (np.isfinite(atr) and atr > 0) or not np.isfinite(Lw).all():
        return out
    x = np.arange(n, dtype=float)
    a, b, c = (float(v) for v in np.polyfit(x, Lw, 2))
    u = lambda z: a * z * z + b * z + c  # noqa: E731
    ss_tot = float(np.sum((Lw - Lw.mean()) ** 2)); ss_res = float(np.sum((Lw - u(x)) ** 2))
    out["F24"] = a / atr
    out["F26"] = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    if a > 0:
        xs = -b / (2.0 * a); xc = min(max(xs, 0.0), float(n - 1))
        out["F25"] = xs / float(n - 1)
        out["F27"] = (u(0.0) - u(xc)) / atr
        out["F28"] = (u(float(n - 1)) - u(xc)) / atr
        out["F29"] = float(int(np.argmin(Lw))) - xs
    return out


def yh_s9_ozellik(df: pd.DataFrame, tarihler: List[pd.Timestamp], hazir: bool = False, E: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """Bir hissenin sinyal günleri için F24-F29; veri _yh_hazir (geçerli bar, kriz kesiği). Gün veride yoksa YHHata."""
    d = df if hazir else _yh_hazir(df)
    H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    pos = d.index.get_indexer(pd.DatetimeIndex(pd.to_datetime(list(tarihler))))
    if (pos < 0).any():
        raise YHHata("S9 özellik: sinyal günü geçerli bar değil")
    return pd.DataFrame([yh_s9_bar(H, L, C, int(i), E) for i in pos], columns=_Y11_OZ_S9)


def yh_s9_ozellik_yaz(veri: Optional[str] = None, cikti: Optional[str] = None, ozellik: Optional[str] = None, denetim_n: int = 25,
                      tohum: int = 1911, E: Dict[str, Any] = YH_ESIK, yol: Optional[str] = None) -> Dict[str, Any]:
    """Bütün Y1 olayları (ozellik_Y1.csv.gz anahtarları) -> ozellik_Y1_s9.csv.gz (pazar, sembol, tarih, F24-F29; 6 anlamlı basamak) +
    ozellik_Y1_s9_denetim.json. Prefix denetimi: pazar başına denetim_n rastgele olay t'de kesik veriyle ve [t-291, t] kesitiyle = tam; değilse DURUR."""
    cikti = cikti or YH_YOL["cikti"]; yol = yol or YH_YOL["ozellik_s9"]
    yo = ozellik or YH_YOL["ozellik"]
    if not os.path.exists(yo):
        raise YHHata(f"özellik dosyası yok: {yo} (GOZ_ETIKET aşama A çıktısı; S9 DURDU)")
    Fo = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"], dtype={"sembol": str, "pazar": str})
    if Fo.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata("özellik dosyasında aynı (pazar, sembol, tarih) iki kez")
    Pz = E["denemeler"]["Y11"]["s9_prm"]
    sat, den = [], {"surum": YH_SURUM, "esik_s9_sha": yh_esik_sha(Pz), "ozellik_sha": _yh_sha_dosya(yo), "pazar": {}}
    for p in OC.OC_ESIK["pazar"]:
        Fp = Fo[Fo.pazar == p]
        if not len(Fp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); n0 = len(sat); hz: Dict[str, pd.DataFrame] = {}
        for s, g in Fp.groupby("sembol", sort=True):
            if s not in Vd["V"]:
                raise YHHata(f"S9 özellik: {p} {s} veride yok")
            hz[s] = _yh_hazir(Vd["V"][s])
            R = yh_s9_ozellik(hz[s], list(g.tarih), hazir=True, E=E)
            for t, r in zip(g.tarih, R.itertuples(index=False)):
                sat.append({"pazar": p, "sembol": s, "tarih": pd.Timestamp(t), **r._asdict()})
        Xp = pd.DataFrame(sat[n0:])
        rng = np.random.default_rng([tohum, OC.OC_ESIK["pazar"].index(p)]); ok = 0
        for q in rng.choice(len(Xp), min(denetim_n, len(Xp)), replace=False):
            r = Xp.iloc[int(q)]; t = pd.Timestamp(r.tarih); d = hz[r.sembol]; i = int(d.index.get_loc(t))
            kes = Vd["V"][r.sembol]; kes = kes[kes.index <= t]
            a = yh_s9_ozellik(kes, [t], E=E).iloc[0].to_numpy(float)
            b = yh_s9_ozellik(d.iloc[max(0, i - int(Pz["bilgi_azami_gun"])):i + 1], [t], hazir=True, E=E).iloc[0].to_numpy(float)
            c = r[_Y11_OZ_S9].to_numpy(float)
            if not (np.allclose(a, c, rtol=1e-9, atol=1e-12, equal_nan=True) and np.allclose(b, c, rtol=1e-9, atol=1e-12, equal_nan=True)):
                raise YHHata(f"S9 prefix denetimi TUTMADI: {p} {r.sembol} {t.date()} -> DURDU")
            ok += 1
        den["pazar"][p] = {"olay": int(len(Xp)), "prefix_tuttu": ok, "nan": {k: int(Xp[k].isna().sum()) for k in _Y11_OZ_S9}}
        yhlog.info("S9 özellik %s: %d olay, prefix %d tuttu", p, len(Xp), ok)
        del Vd, hz
    X = pd.DataFrame(sat, columns=["pazar", "sembol", "tarih"] + _Y11_OZ_S9)
    if len(X) != len(Fo):
        raise YHHata(f"S9 özellik: satır {len(X)} != özellik dosyası {len(Fo)}")
    X.to_csv(yol, index=False, float_format="%.6g", compression="gzip", date_format="%Y-%m-%d")
    den["satir"] = int(len(X)); den["sha"] = _yh_sha_dosya(yol)
    _yh_yaz(os.path.join(cikti, YH_DOSYA["s9_denetim"]), json.dumps(den, ensure_ascii=False, indent=1, default=_yh_json), "S9 denetim")
    return {"yol": yol, **den}


def yh_ozellik5_oku(ozellik: Optional[str] = None, ozellik_s7: Optional[str] = None, ozellik_s9: Optional[str] = None) -> pd.DataFrame:
    """yh_ozellik4_oku (F1-F23) + ozellik_Y1_s9.csv.gz (F24-F29) -> (pazar, sembol, tarih) + _Y11_OZ. Anahtar kümeleri aynı olmalı."""
    y9 = ozellik_s9 or YH_YOL["ozellik_s9"]
    if not os.path.exists(y9):
        raise YHHata(f"S9 özellik dosyası yok: {y9} (5. tur DURDU; `python YAPI_HEDEF.py s9ozellik`)")
    A = yh_ozellik4_oku(ozellik, ozellik_s7)
    anahtar = (id(A), y9, _yh_sha_dosya(y9))
    if _YH_OZ5_ONB.get("anahtar") == anahtar:
        return _YH_OZ5_ONB["F"]
    try:
        B = pd.read_csv(y9, parse_dates=["tarih"], dtype={"sembol": str})
    except Exception as ex:
        raise YHHata(f"S9 özellik dosyası okunamadı: {ex}")
    eksik = [c for c in ["pazar", "sembol", "tarih"] + _Y11_OZ_S9 if c not in B.columns]
    if eksik:
        raise YHHata(f"{y9}: sütun yok {eksik}")
    if B.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata(f"{y9}: aynı (pazar, sembol, tarih) iki kez")
    F = A.merge(B[["pazar", "sembol", "tarih"] + _Y11_OZ_S9], on=["pazar", "sembol", "tarih"], how="outer", validate="one_to_one", indicator=True)
    if (F._merge != "both").any():
        raise YHHata(f"5. tur: F1-F23 ve S9 dosyalarının anahtarları farklı ({int((F._merge != 'both').sum())} satır) -> DURDU")
    F = F.drop(columns="_merge")
    _YH_OZ5_ONB.clear(); _YH_OZ5_ONB.update({"anahtar": anahtar, "F": F})
    return F


def yh_s9_alt(F: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> Dict[str, np.ndarray]:
    """Ş9'un altı alt şartı (NaN tutmaz): a F24 > 0, b 0,20 <= F25 <= 0,75, c F26 >= 0,40, d F27 >= 1, e F28 >= 0,5, f |F29| <= 5."""
    T = E["denemeler"]["Y11"]["esik"]
    g = lambda c: F[c].to_numpy(float)  # noqa: E731
    with np.errstate(invalid="ignore"):
        out = {"a": g("F24") > T["F24_alt_acik"], "b": (g("F25") >= T["F25_alt"]) & (g("F25") <= T["F25_ust"]), "c": g("F26") >= T["F26_min"],
               "d": g("F27") >= T["F27_min"], "e": g("F28") >= T["F28_min"], "f": np.abs(g("F29")) <= T["F29_mutlak_ust"]}
    return {k: np.asarray(v, bool) for k, v in out.items()}


def yh_s9_sartlar(F: pd.DataFrame, E: Dict[str, Any] = YH_ESIK) -> Dict[str, np.ndarray]:
    """Ş1-Ş8, F14 (yh_s7_sartlar) + Ş9 (altı alt şartın hepsi)."""
    gerek = ["F1", "F2", "F3", "F4", "F14", "F15", "F17", "F18", "F20", "F22", "F22a", "F23"]      # yh_s7_sartlar'ın okuduğu sütunlar
    out = yh_s7_sartlar(F, E) if all(c in F.columns for c in gerek) else {}
    A = yh_s9_alt(F, E); m = np.ones(len(F), bool)
    for v in A.values():
        m &= v
    out["S9"] = m
    return out


def yh_y11_maske(F: pd.DataFrame, deneme: str, E: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    """Y11 = Ş1 + Ş2 + Ş9; Y11b = Ş1-Ş5 + Ş9 + Ş7 + Ş8 (Ş6 yerine Ş9); Y11c = Ş9 (bilgi)."""
    if deneme not in YH_DENEMELER_5:
        raise YHHata(f"5. tur deneme değil: {deneme}")
    if not len(F):
        return np.zeros(0, bool)
    S = yh_s9_sartlar(F, E); m = np.ones(len(F), bool)
    for k in E["denemeler"][deneme]["sartlar"]:
        m &= S[k]
    return m


def yh_sinyaller5(Vd: Dict[str, Any], pazar: str, denemeler: List[str], islem: int = 1, E: Dict[str, Any] = YH_ESIK,
                  P: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """5. tur: Y1 sinyalleri (1. tur kodu) ∩ özellik satırları (= Y1 OLAYLARI) -> '_Y11F' + deneme alt kümeleri. Regresyon 4. turdaki gibi."""
    den = [k for k in denemeler if k in YH_DENEMELER_5]
    if len(den) != len(denemeler):
        raise YHHata(f"yh_sinyaller5 yalnız 5. tur: {denemeler}")
    S1 = yh_sinyaller(Vd, pazar, ["Y1"], islem, E)["Y1"].copy()
    S1["tarih"] = pd.to_datetime(S1.tarih); S1["sembol"] = S1.sembol.astype(str)
    Fo = yh_ozellik5_oku()
    Fp = Fo[Fo.pazar == pazar][["sembol", "tarih"] + _Y11_OZ].copy()
    X = S1.merge(Fp, on=["sembol", "tarih"], how="inner", validate="one_to_one")
    rap: Dict[str, Any] = {"y1_sinyal": int(len(S1)), "ozellik_satir": int(len(Fp)), "eslesen": int(len(X))}
    if len(X) != len(Fp):
        raise YHHata(f"5. tur regresyon: {pazar} {len(Fp) - len(X)} özellik satırı şimdiki Y1 sinyallerinde yok -> DURDU")
    if P is not None and len(S1):
        Z, _ = OC.oc_olay_hazirla(S1[["sembol", "tarih", "pazar"]], P)
        k1 = set(zip(Z.sembol.astype(str), pd.to_datetime(Z.tarih))); k2 = set(zip(Fp.sembol, Fp.tarih))
        rap["y1_olay"] = int(len(Z))
        if k1 != k2:
            raise YHHata(f"5. tur regresyon: {pazar} özellik kümesi ({len(k2)}) != Y1 olay kümesi ({len(k1)}) -> DURDU")
    out: Dict[str, Any] = {"_Y11F": X.sort_values(["sembol", "tarih"]).reset_index(drop=True), "_Y11R": rap}
    for k in den:
        out[k] = out["_Y11F"][yh_y11_maske(out["_Y11F"], k, E)].reset_index(drop=True)
    return out


def yh_huni5(S: Dict[str, Any], P: Dict[str, Any], E: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """GETİRİSİZ huni: Y1 -> +Ş1 -> +Ş2 -> +Ş9 (= Y11); Y10 -> Ş6 çıkar -> +Ş9 (= Y11b); Y1 -> +Ş9 (= Y11c); Ş9 alt şartlarının tek başına
    düşürdüğü olay; NaN sayıları."""
    F = S["_Y11F"]
    if not len(F):
        return {"Y11": {"asama": [], "tek": {}}}
    Sb = yh_s9_sartlar(F, E); Al = yh_s9_alt(F, E)
    m1 = Sb["S1"]; m2 = m1 & Sb["S2"]
    y10 = np.ones(len(F), bool)
    for k in _YH_SART:
        y10 &= Sb[k]
    y10_6 = np.ones(len(F), bool)
    for k in [x for x in _YH_SART if x != "S6"]:
        y10_6 &= Sb[k]
    A = [{"ad": "Y1 olayı (özellik satırı)", **_yh_say_getirisiz(F, P)},
         {"ad": "+ Ş1 DİPTE", **_yh_say_getirisiz(F[m1], P)},
         {"ad": "+ Ş2 HAT NET", **_yh_say_getirisiz(F[m2], P)},
         {"ad": "+ Ş9 U DİP = Y11", **_yh_say_getirisiz(F[m2 & Sb["S9"]], P)},
         {"ad": "(ayrı) Y10 = Ş1-Ş8", **_yh_say_getirisiz(F[y10], P)},
         {"ad": "(ayrı) Y10, Ş6 çıkar (Ş1-Ş5, Ş7, Ş8)", **_yh_say_getirisiz(F[y10_6], P)},
         {"ad": "(ayrı) + Ş9 = Y11b", **_yh_say_getirisiz(F[y10_6 & Sb["S9"]], P)},
         {"ad": "(ayrı) Y1 + Ş9 = Y11c (bilgi)", **_yh_say_getirisiz(F[Sb["S9"]], P)}]
    ad = {"a": "F24 <= 0 / NaN", "b": "F25 [0,20, 0,75] dışı / NaN", "c": "F26 < 0,40 / NaN", "d": "F27 < 1 / NaN", "e": "F28 < 0,5 / NaN",
          "f": "|F29| > 5 / NaN"}
    tek = {"Ş9 tutmayan": int((~Sb["S9"]).sum())}
    tek.update({ad[k]: int((~v).sum()) for k, v in Al.items()})
    tek.update({f"{c} NaN": int(F[c].isna().sum()) for c in _Y11_OZ_S9})
    return {"Y11": {"asama": A, "tek": tek}}


def yh_sayim5(veri: Optional[str] = None, islem: int = 1) -> Dict[str, Any]:
    """5. tur GETİRİSİZ sayım: huni + deneme başına OC olayı (dönem) + Y1 eşleşmesi. Hedef / stop / eş / konum eş HESAPLANMAZ."""
    out: Dict[str, Any] = {"huni": {}, "deneme": {}, "eslesme": {}}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"]); P = OC.oc_panel(Vd)
        S = yh_sinyaller5(Vd, p, YH_DENEMELER_5, islem, P=P)
        out["huni"][p] = yh_huni5(S, P); out["eslesme"][p] = S["_Y11R"]
        for k in YH_DENEMELER_5:
            X = S[k]
            Z, say = OC.oc_olay_hazirla(X[["sembol", "tarih", "pazar"]], P) if len(X) else (pd.DataFrame(), {})
            out["deneme"].setdefault(k, {})[p] = {"olay": {a: int(b) for a, b in (Z.donem.value_counts().to_dict() if len(Z) else {}).items() if a},
                                                  "hisse": int(X.sembol.nunique()) if len(X) else 0, "sayim": {a: int(b) for a, b in say.items()}}
        yhlog.info("sayım (5. tur) %s tamam", p)
        del Vd, P, S
    return out


def _yh_s7b_modul():
    """s7_bolge_pdf (S7 PDF'inin olay sırası; yalnız okunur)."""
    k = os.path.dirname(YH_YOL["s7_pdf_kod"])
    if k not in sys.path:
        sys.path.insert(0, k)
    try:
        import s7_bolge_pdf as S7B
    except Exception as ex:
        raise YHHata(f"s7_bolge_pdf yüklenemedi: {ex}")
    return S7B


def yh_s7pdf_olaylar() -> pd.DataFrame:
    """S7 PDF'inin 50 olayı, PDF'teki sırayla (s7_bolge_pdf.s7b_olaylar, tohum 104; No = sıra) -> YALNIZ kimlik sütunları [no, pazar, sembol,
    tarih] (sonuç sütunları döndürülmez)."""
    S7B = _yh_s7b_modul()
    S = S7B.s7b_olaylar(S7B.S7B_AYAR["tohum"])
    K = S[["pazar", "sembol", "tarih"]].copy().reset_index(drop=True)
    K.insert(0, "no", np.arange(1, len(K) + 1)); K["sembol"] = K.sembol.astype(str); K["tarih"] = pd.to_datetime(K.tarih)
    del S
    return K


def _yh_s9_ham(pazar: str, sembol: str, tarih: pd.Timestamp, veri: Optional[str], Vc: Dict[str, Any], E: Dict[str, Any] = YH_ESIK) -> np.ndarray:
    if pazar not in Vc:
        Vc[pazar] = OC.oc_veri(pazar, klasor=veri or YH_YOL["veri"])
    return yh_s9_ozellik(Vc[pazar]["V"][sembol], [pd.Timestamp(tarih)], E=E).iloc[0].to_numpy(float)


def yh_tasarim5(cikti: Optional[str] = None, veri: Optional[str] = None, E: Dict[str, Any] = YH_ESIK, git: bool = True,
                ge_cikti: Optional[str] = None) -> Dict[str, Any]:
    """TASARIM KONTROLÜ (iş tanımı 5 §2; sonuç OKUMADAN, ön kayıttan ÖNCE): (a) S7 PDF'i No 38 Ş9'u GEÇMEMELİ; (b) TUR 2 sayfaları 1, 3, 11, 22
    en az 3 / 4 GEÇMELİ. h5 / st5 / getiri okunmaz (yalnız kimlik + F24-F29). Kayıt tasarim5.json'a eklenir; en çok 2 kayıt (ilk + tek ayar)."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_DOSYA["tasarim5"])
    yo5 = _yh_yol("onkayit5", cikti)
    if os.path.exists(yo5):
        raise YHHata("ON_KAYIT_5.md var: tasarım kontrolü ön kayıttan ÖNCE yapılır (eşik kilitli)")
    eski = json.load(open(yol, encoding="utf-8")) if os.path.exists(yol) else {"kayit": []}
    if len(eski["kayit"]) >= 2:
        raise YHHata("tasarım kontrolü iki kez koştu (ilk + tek ayar hakkı): eşik kilitli -> DURDU")
    if eski["kayit"]:
        T0, T1 = eski["kayit"][-1]["esik"], E["denemeler"]["Y11"]["esik"]
        fark = {k for k in set(T0) | set(T1) if T0.get(k) != T1.get(k)}
        if not fark or not fark <= {"F26_min", "F25_alt"}:
            raise YHHata(f"ayar yalnız F26_min / F25_alt olabilir (değişen: {sorted(fark)})")
        if not (0.30 <= T1["F26_min"] <= 0.50 and 0.15 <= T1["F25_alt"] <= 0.25):
            raise YHHata("ayar aralık dışı (F26 0,30..0,50; F25 alt 0,15..0,25)")
    K = yh_s7pdf_olaylar()
    r38 = K[K.no == _YH_TASARIM_NO]
    avr = K[K.pazar == "AVR"].no.tolist()
    if len(r38) != 1 or r38.pazar.iloc[0] != "AVR" or avr.index(_YH_TASARIM_NO) + 1 != 7:
        raise YHHata("No 38 S7 PDF sırasında AVR listesinin 7. olayı değil -> DURDU")
    gc = ge_cikti or YH_YOL["ge_cikti"]
    try:
        A2 = json.load(open(os.path.join(gc, "tur", "2", "tur_2_anahtar.json"), encoding="utf-8"))["sayfa"]
    except (OSError, ValueError, KeyError) as ex:
        raise YHHata(f"TUR 2 anahtarı okunamadı: {ex}")
    sat = [{"kume": "a", "ad": f"S7 PDF No {_YH_TASARIM_NO} (AVR 2016-22, AVR 7.)", "pazar": "AVR", "sembol": str(r38.sembol.iloc[0]),
            "tarih": pd.Timestamp(r38.tarih.iloc[0])}]
    for s in _YH_TASARIM_TUR2:
        o = A2[str(s)]
        sat.append({"kume": "b", "ad": f"TUR 2 sayfa {s}", "pazar": o["pazar"], "sembol": str(o["sembol"]), "tarih": pd.Timestamp(o["tarih"])})
    D = pd.DataFrame(sat)
    F = yh_ozellik5_oku()
    M = D.merge(F[["pazar", "sembol", "tarih"] + _Y11_OZ_S9], on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    Vc: Dict[str, Any] = {}
    for q, r in M.iterrows():
        ham = _yh_s9_ham(r.pazar, r.sembol, r.tarih, veri, Vc, E)
        if r[_Y11_OZ_S9].isna().all() and not np.isnan(ham).all():
            M.loc[q, _Y11_OZ_S9] = ham                                            # dosyada yoksa ham fiyattan (Y1 olayı değilse)
        elif not np.allclose(ham, r[_Y11_OZ_S9].to_numpy(float), rtol=1e-5, atol=1e-7, equal_nan=True):
            raise YHHata(f"tasarım: {r.ad} F24-F29 dosya ile ham fiyat farklı -> DURDU")
    del Vc
    Al = yh_s9_alt(M, E); S9 = yh_s9_sartlar(M, E)["S9"]
    satir = []
    for q, r in M.iterrows():
        satir.append({"kume": r.kume, "ad": r.ad, **{k: (None if not np.isfinite(r[k]) else float(r[k])) for k in _Y11_OZ_S9},
                      "alt": {k: bool(v[q]) for k, v in Al.items()}, "S9": bool(S9[q])})
    a_gecti = not bool(S9[0]); b_n = int(S9[1:].sum())
    kayit = {"zaman": _yh_simdi(), "esik": dict(E["denemeler"]["Y11"]["esik"]), "esik_sha": yh_esik_sha(E["denemeler"]["Y11"]["esik"]),
             "satir": satir, "a_no38_gecmedi": a_gecti, "b_tur2_gecen": b_n, "tuttu": bool(a_gecti and b_n >= 3),
             "ozellik_s9_sha": _yh_sha_dosya(YH_YOL["ozellik_s9"]), "okunan": "yalnız kimlik (pazar, sembol, tarih) + F24-F29; h5 / st5 / getiri okunmadı"}
    eski["kayit"].append(kayit)
    eski["not"] = "iş tanımı 5 §2 tasarım kontrolü; en çok 2 kayıt (ilk + tek ayar: F26_min 0,30..0,50, F25_alt 0,15..0,25)"
    _yh_yaz(yol, json.dumps(eski, ensure_ascii=False, indent=1, default=_yh_json), "tasarım 5")
    return eski


def yh_tasarim5_karar(gerekce: str, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Tasarım kontrolü TUTMADI ve izinli tek ayar (F26_min / F25_alt) sonucu değiştiremiyorsa: ayar KULLANILMADI kararı ve gerekçesi
    tasarim5.json'a yazılır (eşik iş tanımındaki gibi kilitlenir). Ön kayıttan sonra yazılamaz; tek kayıtta ve TUTMAYAN kayıtta geçerli."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_DOSYA["tasarim5"])
    if os.path.exists(_yh_yol("onkayit5", cikti)):
        raise YHHata("ON_KAYIT_5.md var: tasarım kararı ön kayıttan ÖNCE yazılır")
    if not os.path.exists(yol):
        raise YHHata("tasarım kaydı yok")
    T = json.load(open(yol, encoding="utf-8"))
    if T["kayit"][-1]["tuttu"] or len(T["kayit"]) != 1:
        raise YHHata("ayar-kullanılmadı kararı yalnız tek ve TUTMAYAN tasarım kaydında yazılır")
    if not gerekce.strip():
        raise YHHata("gerekçe boş")
    T["ayar_kullanilmadi_gerekce"] = gerekce.strip()
    _yh_yaz(yol, json.dumps(T, ensure_ascii=False, indent=1, default=_yh_json), "tasarım 5 karar")
    return T


def yh_sha_simdi5(cikti: Optional[str] = None) -> Dict[str, str]:
    """4. turun sha'ları + S9 özellik dosyası + tasarım kaydı + s7_bolge_pdf kodu (No 38 sırası)."""
    cikti = cikti or YH_YOL["cikti"]
    out = yh_sha_simdi4(cikti)
    if not os.path.exists(YH_YOL["ozellik_s9"]):
        raise YHHata(f"S9 özellik dosyası yok: {YH_YOL['ozellik_s9']}")
    out["s9ozellik"] = _yh_sha_dosya(YH_YOL["ozellik_s9"])
    yt = os.path.join(cikti, YH_DOSYA["tasarim5"])
    out["tasarim"] = _yh_sha_dosya(yt) if os.path.exists(yt) else "0" * 64
    out["s7pdfkod"] = _yh_sha_dosya(YH_YOL["s7_pdf_kod"])
    return out


_YH_KAPI_DESEN5 = {**_YH_KAPI_DESEN4, "s9ozellik": r"S9_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "tasarim": r"TASARIM5_SHA:\s*`([0-9a-f]{64})`",
                   "s7pdfkod": r"S7PDF_KOD_SHA:\s*`([0-9a-f]{64})`"}


def _yh_muhur_zinciri5(cikti: str, metin: Optional[str]) -> Dict[str, str]:
    """ESIK_TUR1..3 (4. turun zinciri) + ESIK_TUR4_SHA = yh_esik_sha_tur4() = ON_KAYIT_4.md YH_ESIK_SHA."""
    t = _yh_muhur_zinciri(cikti, metin)
    t4 = yh_esik_sha_tur4(); y = _yh_yol("onkayit4", cikti)
    m = re.search(_YH_KAPI_DESEN["esik"], open(y, encoding="utf-8").read()) if os.path.exists(y) else None
    mm = re.search(r"ESIK_TUR4_SHA:\s*`([0-9a-f]{64})`", metin) if metin else None
    if not (m and m.group(1) == t4 and (metin is None or (mm and mm.group(1) == t4))):
        raise YHHata("5. tur: Y1-Y10c eşik mührü (ESIK_TUR4_SHA / ON_KAYIT_4.md) tutmuyor -> DURDU")
    t["t4"] = t4
    return t


def _yh_is_tanimi5_s2(yol: Optional[str] = None) -> str:
    """İş tanımı 5 §2 (Ş9 TANIMI) metni aynen; yoksa YHHata."""
    yol = yol or YH_YOL["is_tanimi5"]
    if not os.path.exists(yol):
        raise YHHata(f"5. tur iş tanımı yok: {yol}")
    m = re.search(r"(?ms)^## 2\. Ş9 TANIMI[^\n]*\n(.*?)(?=^## 3\.)", open(yol, encoding="utf-8").read())
    if not m or not m.group(1).strip():
        raise YHHata("iş tanımı 5'te §2 Ş9 TANIMI bulunamadı")
    return m.group(1).strip()


def _yh_tasarim_md(T: Dict[str, Any]) -> List[str]:
    s = []
    for n, k in enumerate(T.get("kayit", []), 1):
        e = k["esik"]
        s += [f"Kayıt {n} ({k['zaman']}; eşik F25 [{e['F25_alt']}, {e['F25_ust']}], F26 >= {e['F26_min']}, F27 >= {e['F27_min']}, F28 >= {e['F28_min']}, "
              f"|F29| <= {e['F29_mutlak_ust']}): (a) No 38 Ş9'u {'GEÇMEDİ (istenen)' if k['a_no38_gecmedi'] else 'GEÇTİ (istenmeyen)'}; (b) TUR 2 kazan "
              f"sayfaları {k['b_tur2_gecen']} / 4 geçti (en az 3 istenir) -> {'TUTTU' if k['tuttu'] else 'TUTMADI'}.", "",
              "| Olay | F24 a/ATR | F25 x*/39 | F26 R² | F27 sol derinlik | F28 sağ kalkış | F29 argmin - x* | alt şartlar a·b·c·d·e·f | Ş9 |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in k["satir"]:
            s.append(f"| {r['ad']} | " + " | ".join(_sy(r[c], 3) for c in _Y11_OZ_S9) + " | " + "".join("✓" if r["alt"][a] else "·" for a in "abcdef")
                     + f" | {'TUTAR' if r['S9'] else 'tutmaz'} |")
        s.append("")
    return s


def yh_onkayit5_metni(say: Dict[str, Any], sha: Dict[str, str], t: Dict[str, str], git4: Dict[str, str], git_is: Dict[str, str],
                      s2: str, s9den: Dict[str, Any], T: Dict[str, Any]) -> str:
    Y = YH_ESIK; K = _yh_kural3(Y); D = Y["denemeler"]["Y11"]
    s = ["# YAPI_HEDEF — ÖN KAYIT 5 (5. tur: Ş9 'U DİP + PARABOLİK DEVAM' Y11 / Y11b + Y11c bilgi; TUR 4 kuru sayım T1.5)", "",
         YH_SURUM + "; 5. tur eklendi (YAPI_HEDEF_IS_TANIMI_5.md)", "",
         f"- YH_ESIK_SHA: `{sha['esik']}` (5. tur denemeleri dahil)",
         f"- ESIK_TUR4_SHA: `{t['t4']}` (YH_ESIK'ten Y11-Y11c çıkarılınca; = ON_KAYIT_4.md YH_ESIK_SHA: Y1-Y10c eşikleri AYNEN)",
         f"- ESIK_TUR3_SHA: `{t['t3']}` (= ON_KAYIT_3.md YH_ESIK_SHA)", f"- ESIK_TUR2_SHA: `{t['t2']}` (= ON_KAYIT_2.md YH_ESIK_SHA)",
         f"- ESIK_TUR1_SHA: `{t['t1']}` (= ON_KAYIT.md YH_ESIK_SHA = güç tablosu)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)",
         f"- FV_KOD_SHA: `{sha['fv']}` (FITIL_V2.py)", f"- GE_KOD_SHA: `{sha['gekod']}` (GOZ_ETIKET.py; F1-F18 yeniden hesabı, T1.5 örneklemi)",
         f"- GUC_SHA: `{sha['guc']}` ({YH_DOSYA['guc_json']}; 1. turun güç tablosu, aynı kural)",
         f"- Y2_OLAY_SHA: `{sha['y2']}` (değişmedi; 5. turda kullanılmaz)", f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)",
         f"- S7_OZELLIK_SHA: `{sha['s7ozellik']}` (yapi_hedef/ozellik_Y1_s7.csv.gz; F20-F23, F22a; 4. turdaki dosya)",
         f"- S9_OZELLIK_SHA: `{sha['s9ozellik']}` (yapi_hedef/ozellik_Y1_s9.csv.gz; F24-F29)",
         f"- TASARIM5_SHA: `{sha['tasarim']}` (yapi_hedef/tasarim5.json; tasarım kontrolü kaydı)",
         f"- S7PDF_KOD_SHA: `{sha['s7pdfkod']}` (yapi_hedef/s7_bolge_pdf.py; No 38 sırası, §5 50 olay)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)",
         f"- ON_KAYIT_4: git {git4.get('commit', '?')[:10]}, {git4.get('commit_zamani', '?')}",
         f"- IS_TANIMI_5: git {git_is.get('commit', '?')[:10]}, {git_is.get('commit_zamani', '?')}",
         f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "Bu dosya 5. tur ölçümünden ÖNCE yazıldı. Y11 / Y11b / Y11c için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / "
         "konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni, olay sayımı ve tasarım kontrolü; S9 özellik dosyası yalnız "
         "fiyat [t-291, t-1]). `kos --deneme Y11,Y11b,Y11c` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y10c eşik mührünü "
         "denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.", "",
         "## Ş9 TANIMI (iş tanımı 5 §2, AYNEN)", "", s2, "",
         "## TASARIM KONTROLÜ (sonuç OKUMADAN, ön kayıttan ÖNCE; h5 / st5 / getiri okunmadı)", ""]
    s += _yh_tasarim_md(T)
    son = T["kayit"][-1]
    s += [f"SONUÇ: {'TUTTU' if son['tuttu'] else 'TUTMADI'} ({len(T['kayit'])} kayıt; " + ("AYAR YAPILMADI" if len(T["kayit"]) == 1 else
          "TEK AYAR KULLANILDI: " + ", ".join(f"{k} {T['kayit'][0]['esik'][k]} -> {son['esik'][k]}" for k in ("F26_min", "F25_alt")
                                              if T["kayit"][0]["esik"][k] != son["esik"][k])) + "). Eşik bundan sonra KİLİTLİ.", ""]
    if len(T["kayit"]) > 1 and T.get("gerekce"):
        s += [f"Ayar gerekçesi: {T['gerekce']}", ""]
    if T.get("ayar_kullanilmadi_gerekce"):
        s += [f"AYAR KULLANILMADI — gerekçe: {T['ayar_kullanilmadi_gerekce']}", ""]
    s += ["## BAKILMIŞ HÜCRE İŞARETİ", "",
          "- BAKILMIŞ: " + ", ".join(" ".join(x) for x in K["bakilmis"]) + ". Y11 / Y11b Y9'un alt kümesi (Ş1 = Y9 şartı); Y9 hücreleri 3. turda "
          "görüldü (Y11c Y1'in alt kümesi; Y1 hücreleri 1. turda görüldü). Etiket EN FAZLA EMARE.",
          "- DIŞ SINAMA: " + ", ".join(" ".join(x) for x in K["dis_sinama"]) + " — kısmen bakılmış (Y9 alt kümesi; Y9 dış sınama hücreleri 3. tur "
          "raporunda görüldü); 'bağımsız' denmez (4. tur H-c dersi). Karar kuralıyla aynı 4 şart; ikisi de TUTAR -> 'EMARE (dış sınama tuttu)'.",
          "- BIST (bilgi, ayrı başlık): " + ", ".join(" ".join(x) for x in K["bist_bilgi"]) + " — kısmen bakılmış (Y9 alt kümesi).",
          "- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).", "",
          "## Ölçü, kontrol grupları, karar kuralı (1., 3. ve 4. turla AYNI; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi)", "",
          f"- Ufuk: {Y['olcu']['ufuk_tanim']}.", f"- Stop / hedef: {Y['olcu']['stop']['tanim']}", f"- EŞ: {Y['kontrol']['es']}.",
          f"- PLASEBO: {Y['kontrol']['plasebo']}.", f"- Karar: {Y['karar']['tanim']}.", f"- Hücre durumu: {Y['etiket']['hucre']}.",
          f"- Kural etiketi (deneme başına): {Y['etiket']['genel']}", f"- 3. tur ek kuralları (5. turda AYNEN): etiket: {K['etiket']}.",
          f"- TERS: {K['ters']}.", f"- Konum eşli KAT: {K['konum_es']}.", f"- Çeyrek: {K['ceyrek_tanim']}.", f"- Konum uyumu: {K['konum_uyum']}.", "",
          "## 5. tur kuralları (önceden yazılı; DEĞİŞMEZ)", "",
          f"- Etiket: {D['tur5_kural']['etiket']}.", f"- Çoklu karşılaştırma: {D['tur5_kural']['bh']}.", f"- Regresyon: {D['tur5_kural']['regresyon']}.",
          f"- Huni: {D['tur5_kural']['huni']}.", f"- S9 özellikleri: {D['s9_prm']['tanim']}.", "",
          "## Denemeler (sonuç görülmeden sabit; iş tanımı 5 §3)", ""]
    for k in YH_DENEMELER_5:
        s.append(f"- **{k} {Y['denemeler'][k]['ad']}**: {Y['denemeler'][k]['tanim']} (şartlar: " +
                 ", ".join(f"Ş{x[1:]}" for x in Y["denemeler"][k]["sartlar"]) + ").")
    s += ["", "Şartlar: Ş1-Ş8 = 4. tur (YH_ESIK Y10 'sart_tanim', eşikler AYNEN); Ş9:", "", f"- Ş9: {D['sart_tanim']['S9']}.",
          f"- Ş9 eşikleri (kilitli): {json.dumps(D['esik'], ensure_ascii=False, sort_keys=True)}.", "",
          "## Yorumlar (iş tanımında açık noktalar; koşudan önce sabit)", "",
          "- YORUM-1 (ATR birimi): GOZ_ETIKET F3'ün ATR250'si göreli (ort(TR / C_önceki)); Ş9'un F24 / F27 / F28'i fiyat farkı olduğundan göreli ATR "
          "pencerenin ortalama kapanışıyla fiyat birimine çevrilir (ATR = ATR_göreli x ort(Close[t-40..t-1])). ATR barları F3'teki gibi "
          "pencereden ÖNCE: [w0 - min(250, w0 - 1), w0 - 1], w0 = t-40; 120 bardan azsa NaN.",
          "- YORUM-2 (a <= 0): x* tanımsız -> F25, F27, F28, F29 NaN (F24 > 0 şartı zaten tutmaz).",
          "- YORUM-3 (argmin): eşit en düşük Low'larda ilki (np.argmin).",
          "- YORUM-4 (t barı): Ş9 yalnız t'den önceki 40 Low'u okur; t (sinyal) barı girmez; giriş t+1 açılış.",
          "- YORUM-5 (No 38): s7_bolge_pdf.s7b_olaylar(104) sırası (PDF'teki No); betik olay dosyasının 'ölçülemeyen olay yok' kapısını kendi "
          "içinde koşar, tasarım yalnız kimlik sütunlarını alır (sonuç sütunu döndürülmez / yazdırılmaz).",
          "- YORUM-6 (TUR 4 kuru sayım): GOZ_ETIKET T1.5 = T1.4, deneme Y11, olay dosyası olay_Y11.csv.gz (yalnız kimlik sütunları); "
          "ge_tur_esik(>= 5) -> T1.5; ge_tur_esik(4) T1.4 olarak DEĞİŞMEDİ (TUR 4'ün hangi sürümle açılacağı ana modelin kararı); kuru sayım "
          "tur no 4 (gösterilen = 300 + hakem + TUR 1-3) ve T1.5 ile, dosya yazmadan. `tur ac --no 4` KOŞULMAZ.",
          "- YORUM-7 (Cemal uyumu §5): 4. tur §4 gibi (hakem KÖR 19 + TUR 1 + TUR 2 = 79 sayfa); ayrıca S7 PDF'inin 50 olayında Ş9 tutan sayısı "
          "(bilgi; No 38 dahil) koşuda hesaplanır (tasarım kontrolünde yalnız No 38 bakıldı).", "",
          "## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)", "", "### Y11 hunisi", ""]
    s += _yh_huni_md(say["huni"], "Y11") + [""]
    s += ["Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): " + "; ".join(
        f"{p}: Y1 sinyal {x.get('y1_sinyal')}, Y1 olay {x.get('y1_olay', '?')}, özellik {x.get('ozellik_satir')}, eşleşen {x.get('eslesen')}"
        for p, x in say["eslesme"].items()) + ".", "",
          "S9 özellik dosyası denetimi: " + "; ".join(f"{p}: {x['olay']} olay, prefix {x['prefix_tuttu']} TUTTU, NaN " + ", ".join(f"{a} {b}" for a, b in x["nan"].items())
                                                      for p, x in s9den.get("pazar", {}).items()) + ".", "",
          "| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |", "|---|---|---|---|"]
    for k in YH_DENEMELER_5:
        for p in OC.OC_ESIK["pazar"]:
            x = say["deneme"].get(k, {}).get(p)
            if x:
                s.append(f"| {k} | {p} | {x['hisse']} | " + " / ".join(str(x["olay"].get(q, 0)) for q in _YH_DONEM3) + " |")
    s += ["", "## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)", ""]
    try:
        tablo = json.load(open(_yh_yol("guc_json"), encoding="utf-8"))
    except (OSError, ValueError):
        tablo = None
    for k in YH_DENEMELER_5:
        hc = [(p, q, int(say["deneme"].get(k, {}).get(p, {}).get("olay", {}).get(q, 0))) for p, q in Y["karar"]["hucre_karar"]]
        gs = [yh_guc_bak(n, Y["denemeler"][k]["yon"], tablo) for _, _, n in hc]
        ifade = "; ".join(f"{p} {q} en çok {n} olay (güç {_yz(g, 0)}{', n < 30 -> ÖLÇÜLEMEDİ (n)' if n < Y['karar']['n_esik'] else ''})" for (p, q, n), g in zip(hc, gs))
        az = all(n < Y["etiket"]["n_yeter"] and g < Y["etiket"]["guc_esik"] for (_, _, n), g in zip(hc, gs))
        s.append(f"- {k}{' (bilgi)' if Y['denemeler'][k].get('bilgi') else ''}: {ifade}." + (
            " Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır." if az else ""))
    s += ["- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay "
          "o satırdan düşer (k_n ayrı yazılır).",
          "- BH (aile 'bh_tur5') yalnız n >= 30 karar hücreleri arasında; n < 30 hücre 'BH dışı'.",
          "- Hayatta kalma: dipteki (Ş1) hissenin batma olasılığı yüksektir; evrende batan yok -> Y11 / Y11b hedef payı ayrıca yukarı yanlı okunur.", "",
          "## YH_ESIK 5. tur girdileri (tam metin; geri kalanı ON_KAYIT.md .. ON_KAYIT_4.md ile aynı)", "", "```json",
          json.dumps({k: Y["denemeler"][k] for k in YH_DENEMELER_5}, ensure_ascii=False, indent=1, sort_keys=True, default=str), "```", "",
          yh_kontrol_tablosu(YH_KONTROL_5), "", "## SAPMALAR", "",
          ("- SAPMA-1: tasarım kontrolü TUTMADI (a No 38 " + ("geçmedi" if son["a_no38_gecmedi"] else "GEÇTİ") + f", b TUR 2 {son['b_tur2_gecen']} / 4); "
           "izinli tek ayar " + ("KULLANILMADI (gerekçe yukarıda)" if len(T["kayit"]) == 1 else "kullanıldı") + "; iş tanımı §2 gereği eşik kilitlendi, "
           "ölçüm bu eşikle koşar; ölçüm sonucu tasarım kontrolünü değiştirmez.") if not son["tuttu"] else "(yok)", "",
          "## Test", "", "`python test_yapi_hedef.py` (önceki turların testleri aynen + 5. tur: F24-F29 yapay vakalar (tam parabol geçer, alçalan "
          "zincir geçmez, düz taban F27 < 1 geçmez, şemsiye a < 0 geçmez), prefix değişmezliği, Y11 / Y11b / Y11c seçimi, ESIK_TUR4_SHA = 4. tur "
          "mührü, uçtan uca s9ozellik + onkayit5 + kos + kapı + Y1 regresyonu, önceki turların sonuçları değişmez); `python test_goz_etiket.py` "
          "(T1.5; TUR 1-3 kapısı).", ""]
    return "\n".join(s)


def yh_onkayit5_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_5.md: 1-4. turlar ölçülmüş, 5. tur ölçülmemiş; Y1-Y10c eşik mührü tutmalı; tasarım kontrolü yapılmış ve TUTMUŞ olmalı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit5", cikti)
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"ön kayıt 5 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"ön kayıt 5 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 5. tur ön kaydı önceki turların ölçümünden sonra yazılır")
    J = json.load(open(sy, encoding="utf-8"))
    if [k for k in YH_DENEMELER_5 if k in J.get("deneme", {})]:
        raise YHHata("5. tur denemeleri zaten ölçülmüş: ön kayıt ölçümden sonra yazılamaz")
    if "Y10" not in J.get("deneme", {}):
        raise YHHata("Y10 ölçülmemiş: 5. tur 4. turdan sonra gelir")
    yt = os.path.join(cikti, YH_DOSYA["tasarim5"])
    if not os.path.exists(yt):
        raise YHHata("tasarım kontrolü yapılmamış (`python YAPI_HEDEF.py tasarim5`) -> ön kayıt yazılmaz")
    T = json.load(open(yt, encoding="utf-8")); son = T["kayit"][-1]
    if son["esik"] != YH_ESIK["denemeler"]["Y11"]["esik"]:
        raise YHHata("tasarım kaydının eşiği şimdiki YH_ESIK Y11 eşiği değil -> DURDU")
    if not son["tuttu"] and not T.get("ayar_kullanilmadi_gerekce"):
        raise YHHata("tasarım kontrolü TUTMADI ve ayar kararı yazılmamış (yh_tasarim5_karar): ön kayıt yazılmaz")
    t = _yh_muhur_zinciri5(cikti, None)
    sha = yh_sha_simdi5(cikti)
    if son.get("ozellik_s9_sha") != sha["s9ozellik"]:
        raise YHHata("tasarım kaydı başka S9 özellik dosyasıyla yapılmış -> DURDU")
    git4 = _yh_git(_yh_yol("onkayit4", cikti)) if git else {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi5"]) if git else {}
    except YHHata:
        git_is = {}
    s2 = _yh_is_tanimi5_s2()
    yd = os.path.join(cikti, YH_DOSYA["s9_denetim"])
    s9den = json.load(open(yd, encoding="utf-8")) if os.path.exists(yd) else {}
    if s9den.get("sha") != sha["s9ozellik"]:
        raise YHHata("S9 denetim dosyası S9 özellik dosyasıyla eşleşmiyor (önce `python YAPI_HEDEF.py s9ozellik`)")
    say = yh_sayim5(veri, islem)
    for p in OC.OC_ESIK["pazar"]:
        x = J.get("sayim", {}).get("Y1", {}).get(p)
        if x:
            n1 = int(x["girdi"]) - int(x.get("havuz_disi", 0)) - int(x.get("tekil", 0)) - int(x.get("giris_yok", 0)) - int(x.get("giris_gec", 0))
            if n1 != say["eslesme"][p].get("y1_olay", n1):
                raise YHHata(f"regresyon: {p} Y1 olay sayısı 1. turda {n1}, şimdi {say['eslesme'][p].get('y1_olay')} -> ön kayıt yazılmadı")
    _yh_yaz(yol, yh_onkayit5_metni(say, sha, t, git4, git_is, s2, s9den, T), "ön kayıt 5")
    return yol


def yh_kapi5(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """5. tur koşu kapısı: ON_KAYIT_5.md kontrol listesi + bütün sha'lar + Y1-Y10c eşik mührü zinciri + tasarım kaydı + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit5", cikti)
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt 5 yok: {yol}")
    metin = open(yol, encoding="utf-8").read()
    _yh_muhur_zinciri5(cikti, metin)
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in _YH_KAPI_DESEN5.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"ön kayıt 5'te {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi5(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    T = json.load(open(os.path.join(cikti, YH_DOSYA["tasarim5"]), encoding="utf-8"))
    if (not T["kayit"][-1]["tuttu"] and not T.get("ayar_kullanilmadi_gerekce")) or T["kayit"][-1]["esik"] != YH_ESIK["denemeler"]["Y11"]["esik"]:
        raise YHHata("tasarım kaydı tutmuyor / eşik farklı -> koşu DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"]); out["git_guc"] = _yh_git(_yh_yol("guc_json", cikti))
        out["git_ozellik"] = _yh_git(YH_YOL["ozellik"]); out["git_s7"] = _yh_git(YH_YOL["ozellik_s7"]); out["git_s9"] = _yh_git(YH_YOL["ozellik_s9"])
        out["git_ge"] = _yh_git(YH_YOL["ge_kod"]); out["git_tasarim"] = _yh_git(os.path.join(cikti, YH_DOSYA["tasarim5"]))
    yhlog.info("yh_kapi5 AÇIK (%s)", yol)
    return out


def yh_gelecek5(Vd: Dict[str, Any], X: pd.DataFrame, deneme: str, pazar: str, Y: Dict[str, Any] = YH_ESIK) -> int:
    """Rastgele 5 olay: veri t'de kesilir; Y1 sinyali (aynı stop0, son sinyal t) + F1-F18 + F20-F23 + F24-F29 kesik veriden yeniden = dosya
    (göreli 1e-5); değilse YHHata."""
    import GOZ_ETIKET as GE
    G = Y["gelecek_denetimi"]
    if not len(X):
        return 0
    rng = np.random.default_rng([G["tohum"], YH_DENEMELER_HEPSI.index(deneme), OC.OC_ESIK["pazar"].index(pazar)])
    n = 0
    for r in X.iloc[rng.choice(len(X), min(G["n"], len(X)), replace=False)].itertuples():
        t = pd.Timestamp(r.tarih); df = Vd["V"][r.sembol]; kes = df[df.index <= t]
        X1, _ = yh_s6_hisse(kes, Y)
        z = X1[pd.to_datetime(X1.tarih) == t] if len(X1) else X1
        ok = len(z) == 1 and abs(float(z.stop0.iloc[0]) - float(r.stop0)) <= 1e-9 * max(1.0, abs(float(r.stop0))) and pd.Timestamp(X1.tarih.iloc[-1]) == t
        if ok:
            Fs, _ = GE.ge_ozellik_hisse(kes, [t])
            a = np.array([Fs[0][c] for c in _Y10_OZ_A], float)
            b = yh_s7_ozellik(kes, [t], E=Y).iloc[0].to_numpy(float)
            c = yh_s9_ozellik(kes, [t], E=Y).iloc[0].to_numpy(float)
            ok = bool(np.allclose(np.r_[a, b, c], np.array([getattr(r, k) for k in _Y11_OZ], float), rtol=1e-5, atol=1e-7, equal_nan=True))
        if not ok:
            raise YHHata(f"geleceğe bakma denetimi TUTMADI: {deneme} {pazar} {r.sembol} {t.date()}")
        n += 1
    return n


def yh_cemal_uyum5(F: Optional[pd.DataFrame] = None, ge_cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """§5 CEMAL'İN GÖZÜYLE UYUM (bilgi; h5 OKUNMAZ): sayfa başına Ş1-Ş9 / F14 / Y11* -> Cemal OLUR / OLMAZ / BELİRSİZ x (tutar / tutmaz) +
    şart başına Cemal OLUR payı + Fisher; ayrıca S7 PDF'inin 50 olayında Ş9 tutan (No 38 dahil)."""
    from scipy.stats import fisher_exact
    F = yh_ozellik5_oku() if F is None else F
    D = yh_cemal_sayfalar(ge_cikti)
    M = D.merge(F, on=["pazar", "sembol", "tarih"], how="left", validate="many_to_one", indicator=True)
    if (M._merge != "both").any():
        raise YHHata(f"Cemal sayfaları özellik dosyasında yok: {int((M._merge != 'both').sum())}")
    Sb = yh_s9_sartlar(M, Y)
    bay = {**{k: Sb[k] for k in _YH_SART5 + ["F14"]}, **{k: yh_y11_maske(M, k, Y) for k in YH_DENEMELER_5}}
    out: Dict[str, Any] = {"n": int(len(M)), "set": {k: int(v) for k, v in M.set.value_counts().items()},
                           "cemal": {k: int(v) for k, v in M.cemal.fillna("yanıtsız").value_counts().items()}, "tablo": [], "sart": []}
    c = M.cemal.to_numpy(object)
    for st in ["hepsi"] + sorted(M.set.unique()):
        g = (M.set == st).to_numpy() if st != "hepsi" else np.ones(len(M), bool)
        for k in YH_DENEMELER_5:
            b = bay[k]; r = {"set": st, "deneme": k}
            for cl in ("OLUR", "OLMAZ", "BELİRSİZ"):
                r[f"{cl}_tutar"] = int((g & b & (c == cl)).sum()); r[f"{cl}_tutmaz"] = int((g & ~b & (c == cl)).sum())
            tb = [[r["OLUR_tutar"], r["OLUR_tutmaz"]], [r["OLMAZ_tutar"], r["OLMAZ_tutmaz"]]]
            r["fisher_p"] = float(fisher_exact(tb)[1]) if sum(map(sum, tb)) else np.nan
            out["tablo"].append(r)
    for k in _YH_SART5 + ["F14"]:
        b = bay[k]
        a1, a0 = int((b & (c == "OLUR")).sum()), int((b & (c == "OLMAZ")).sum()); z1, z0 = int((~b & (c == "OLUR")).sum()), int((~b & (c == "OLMAZ")).sum())
        kr = np.isin(c, ["OLUR", "OLMAZ"])
        out["sart"].append({"sart": k, "tutar": int(b.sum()), "tutar_karar": int((b & kr).sum()), "olur_pay_tutar": a1 / (a1 + a0) if a1 + a0 else np.nan,
                            "tutmaz_karar": int((~b & kr).sum()), "olur_pay_tutmaz": z1 / (z1 + z0) if z1 + z0 else np.nan,
                            "fisher_p": float(fisher_exact([[a1, z1], [a0, z0]])[1]) if a1 + a0 + z1 + z0 else np.nan})
    K = yh_s7pdf_olaylar()
    Mk = K.merge(F[["pazar", "sembol", "tarih"] + _Y11_OZ_S9], on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    s9 = yh_s9_sartlar(Mk, Y)["S9"]
    out["s7pdf"] = {"n": int(len(Mk)), "s9_tutan": int(s9.sum()),
                    "pazar": {p: [int((Mk.pazar == p).sum()), int((s9 & (Mk.pazar == p).to_numpy()).sum())] for p in OC.OC_ESIK["pazar"]},
                    "tutan_no": [int(x) for x in Mk.no[s9]], "no38_s9": bool(s9[(Mk.no == _YH_TASARIM_NO).to_numpy()].any()),
                    "nan": int(Mk[_Y11_OZ_S9].isna().all(axis=1).sum())}
    return out


def yh_tur5_orneklem_bilgi(satir_yol: str) -> Dict[str, Any]:
    """TUR 4 kuru sayımı T1.5 ile (GOZ_ETIKET; DOSYA YAZMADAN): uygun olay (deneme Y11, dönem 2023 / 2024-26, giriş <= kriz - 30) ve
    gösterilmemiş olay / hisse sayıları (pazar x dönem; gösterilen = 300 + hakem + TUR 1-3) + ge_tur_orneklem(4, E = T1.5) kuru koşusu."""
    import GOZ_ETIKET as GE
    E = GE.ge_tur_esik(5)
    if E.get("deneme") != "Y11":
        raise YHHata("GOZ_ETIKET T1.5 deneme Y11 değil")
    X = GE.ge_olay_oku(GE.GE_KIMLIK_KOL, satir_yol); X["sembol"] = X.sembol.astype(str)
    olay_g, hisse_g = GE.ge_tur_gosterilen(4)
    sinir = pd.Timestamp(GE.GE_ESIK["kriz"]) - pd.Timedelta(days=int(E["giris_kriz_pay_gun"]))
    U = X[(X.deneme == E["deneme"]) & X.donem.isin(list(E["donem"])) & (X.giris <= sinir)].copy()
    U["goster"] = [(p, s, str(t.date())) in olay_g or (p, s) in hisse_g for p, s, t in zip(U.pazar, U.sembol, U.tarih)]
    out: Dict[str, Any] = {"surum": E["surum"], "tur_no": 4, "kota": {p: int(k) for p, k in E["katman"]}, "uygun": {}, "gosterilmemis": {},
                           "hisse_gosterilmemis": {}}
    for p in OC.OC_ESIK["pazar"]:
        for q in E["donem"]:
            x = U[(U.pazar == p) & (U.donem == q)]
            out["uygun"][f"{p} {q}"] = int(len(x)); out["gosterilmemis"][f"{p} {q}"] = int((~x.goster).sum())
        out["hisse_gosterilmemis"][p] = int(U[(U.pazar == p) & ~U.goster].sembol.nunique())
    try:
        S = GE.ge_tur_orneklem(4, satir_yol, None, E)
        out["kuru"] = {"durum": "KOTA DOLDU", "n": int(len(S)), "dagilim": {f"{a} {b}": int(v) for (a, b), v in S.groupby(["pazar", "donem"]).size().items()}}
    except GE.GEHata as ex:
        out["kuru"] = {"durum": "DURDU (kota dolmadı; kota düşürülmez, ana model karar verir)", "neden": str(ex)}
    return out


_YH_ILERLEME = ["Y1", "Y9", "Y9b", "Y10", "Y11", "Y11b"]


def yh_ilerleme5(J: Dict[str, Any], cikti: str) -> Dict[str, Any]:
    """İLERLEME tablosu: Y1, Y9, Y9b, Y10, Y11, Y11b için hücre başına n ve P(+5) olay / eş SATIR DOSYALARINDAN (h5 ve es_h5 ölçülebilir);
    sonuc.json hücresiyle (n, h5_p_olay, h5_p_ref) karşılaştırılır (yeniden üretim)."""
    out: Dict[str, Any] = {"deneme": {}, "uyum": True, "uyumsuz": []}
    for d in _YH_ILERLEME:
        D = J.get("deneme", {}).get(d)
        if not D:
            continue
        rel = D.get("satir_dosya")
        yol = (rel if os.path.isabs(rel) else os.path.join(KOK_YH, rel)) if rel else os.path.join(cikti, YH_DOSYA["satir"].format(d=d))
        if not os.path.exists(yol):
            out["deneme"][d] = {"yok": yol}; continue
        x = pd.read_csv(yol, usecols=["pazar", "donem", "h5", "es_h5"], dtype={"donem": str})
        hk = {(h["pazar"], h["donem"]): h for h in D["hucre"]}; R = {}
        for p in OC.OC_ESIK["pazar"]:
            for q in _YH_DONEM3:
                a = x[(x.pazar == p) & (x.donem == q) & x.h5.notna() & x.es_h5.notna()]
                r = {"n": int(len(a)), "p_olay": float(a.h5.mean()) if len(a) else np.nan, "p_es": float(a.es_h5.mean()) if len(a) else np.nan}
                h = hk.get((p, q), {})
                ok = r["n"] == int(h.get("n", 0) or 0) and (not r["n"] or (abs(r["p_olay"] - h["h5_p_olay"]) < 1e-4 and abs(r["p_es"] - h["h5_p_ref"]) < 1e-4))
                if not ok:
                    out["uyum"] = False; out["uyumsuz"].append(f"{d} {p} {q}")
                R[f"{p} {q}"] = r
        out["deneme"][d] = R
    return out


def yh_kos5(denemeler: List[str], cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True,
            kontrol: bool = True, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """5. tur koşusu: kapı -> Y1 sinyali ∩ özellikler -> Y11* ölçüm (1. tur kodu) -> konum eşli KAT -> Y1 regresyonu -> BH (n >= 30) -> Cemal
    uyumu + S7 PDF 50 olay Ş9 -> TUR 4 kuru sayım (T1.5) -> İLERLEME -> sonuc.json / RAPOR_5.md."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]
    if any(k not in YH_DENEMELER_5 for k in denemeler):
        raise YHHata(f"5. tur denemeleri başka turla aynı koşuda olmaz: {denemeler}")
    denemeler = [k for k in YH_DENEMELER_5 if k in denemeler]
    sy = _yh_yol("sonuc", cikti)
    if not os.path.exists(sy):
        raise YHHata("sonuc.json yok: 5. tur önceki turlardan sonra koşar")
    sonuc = json.load(open(sy, encoding="utf-8"))
    tekrar = [k for k in denemeler if k in sonuc.get("deneme", {})]
    if tekrar:
        raise YHHata(f"bu denemeler zaten ölçüldü (ölçüm bir kez koşulur): {tekrar}")
    ok = yh_kapi5(cikti, git=git, kontrol=kontrol)
    kos_zaman = _yh_simdi()
    if ok["onkayit_zaman"] > kos_zaman:
        raise YHHata("ön kayıt zamanı koşu zamanından sonra")
    tablo = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    O1 = pd.read_csv(_yh_y1_satir_yolu(sonuc, cikti), parse_dates=["tarih", "giris"], dtype={"sembol": str})
    sonuc["kos"].append({"zaman_utc": kos_zaman, "kapi": ok, "denemeler": denemeler, "islem": islem})
    K = _yh_kural3(Y); Ols: Dict[str, List[pd.DataFrame]] = {k: [] for k in denemeler}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
        S = yh_sinyaller5(Vd, p, denemeler, islem, Y, P=P)
        sonuc.setdefault("huni5", {})[p] = yh_huni5(S, P, Y); sonuc.setdefault("y11_eslesme", {})[p] = S["_Y11R"]
        F15p = yh_f15_panel(P, Vd, Y)
        for k in denemeler:
            X = S.get(k, pd.DataFrame())
            sonuc["gelecek_denetimi"].setdefault(k, {})[p] = yh_gelecek5(Vd, X, k, p, Y)
            Z, say = yh_olc_pazar(Vd, P, Cl, X, k, p, islem, Y)
            dus = {a: int(say.get(a, 0)) for a in ("giris_yok", "giris_gec", "havuz_disi", "tekil")}
            if any(dus.values()):
                raise YHHata(f"{k} {p}: Y1 olay alt kümesi OC'de düştü {dus} (Y11 ⊆ Y1 olayı bozuk) -> DURDU")
            if len(Z):
                Z = Z.merge(X[["sembol", "tarih"] + _Y11_OZ].assign(tarih=pd.to_datetime(X.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
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
        sonuc["deneme"][k]["tur"] = 5
        if len(Ol):
            sonuc["deneme"][k]["satir_dosya"] = os.path.relpath(yh_satir_yaz(Ol, k, cikti), KOK_YH)
    anahtar, pler, dis = [], [], []
    for k in [x for x in YH_DENEMELER_5 if not Y["denemeler"][x].get("bilgi")]:
        for h in sonuc["deneme"].get(k, {}).get("hucre", []):
            if h.get("karar_hucre"):
                if int(h.get("n", 0) or 0) >= Y["karar"]["n_esik"]:
                    anahtar.append((k, h["pazar"], h["donem"])); pler.append(h.get("h5_p", np.nan))
                else:
                    dis.append({"deneme": k, "pazar": h["pazar"], "donem": h["donem"], "n": int(h.get("n", 0) or 0), "not": "BH dışı (n < 30)"})
    sonuc["bh_tur5"] = [{"deneme": a, "pazar": b, "donem": c, "p": p, "bh_q10": g} for (a, b, c), p, g in zip(anahtar, pler, _yh_bh(pler, 0.10))] + dis
    gercek = os.path.abspath(cikti) == os.path.abspath(os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef"))
    sonuc["cemal_uyum_tur5"] = yh_cemal_uyum5(None, None, Y) if gercek else {"not": "test / başka çıktı klasörü: hesaplanmadı"}
    sd = sonuc["deneme"].get("Y11", {}).get("satir_dosya")
    if sd and gercek:
        sonuc["tur5_orneklem"] = yh_tur5_orneklem_bilgi(sd if os.path.isabs(sd) else os.path.join(KOK_YH, sd))
    sonuc["ilerleme5"] = yh_ilerleme5(sonuc, cikti)
    sonuc.setdefault("hata_tur5", [])
    if not sonuc["ilerleme5"]["uyum"]:
        sonuc["hata_tur5"].append("İLERLEME: satır dosyasından yeniden hesap sonuc.json hücresiyle tutmadı: " + ", ".join(sonuc["ilerleme5"]["uyumsuz"]))
    sonuc["sure_sn"] = round(sonuc.get("sure_sn", 0) + time.time() - t0, 1)
    _yh_yaz(sy, json.dumps(sonuc, ensure_ascii=False, indent=1, default=_yh_json), "sonuç")
    return {"sonuc": sonuc, "rapor": yh_rapor5(cikti)}


def yh_rapor5(cikti: Optional[str] = None, Y: Dict[str, Any] = YH_ESIK) -> str:
    """5. tur raporu (RAPOR_5.md): 4. tur biçimi + tasarım kontrolü + İLERLEME; RAPOR .. RAPOR_4'e dokunmaz."""
    cikti = cikti or YH_YOL["cikti"]
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    den = [k for k in YH_DENEMELER_5 if k in J["deneme"]]
    if not den:
        raise YHHata("sonuc.json'da 5. tur denemesi yok")
    K = _yh_kural3(Y)
    k5 = [k for k in J["kos"] if any(x in YH_DENEMELER_5 for x in k["denemeler"])][-1]
    kh = lambda D: {(h["pazar"], h["donem"]): h for h in D["hucre"]}  # noqa: E731
    KB = "kısmen bakılmış (Y9 alt kümesi)"

    def isaret(h: Dict[str, Any]) -> str:
        if h.get("bakilmis"):
            return "BAKILMIŞ"
        if h.get("dis_sinama"):
            return f"DIŞ SINAMA, {KB}"
        return f"BIST bilgi, {KB}" if h["pazar"] == "BIST" else "bilgi"
    s = ["# YAPI_HEDEF — RAPOR 5 (5. tur: Ş9 'U DİP + PARABOLİK DEVAM' Y11 / Y11b + Y11c bilgi; konum eşli KAT; TUR 4 kuru sayım T1.5)", "",
         f"{J['surum']}. Koşu: {k5['zaman_utc']} ({', '.join(k5['denemeler'])}). Ön kayıt 5: {k5['kapi'].get('onkayit_zaman', '?')} "
         f"(git {k5['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}).", "",
         "## 1. SONUÇ (etiket önceden yazılı kuralla; EN FAZLA EMARE: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ)", "",
         "| Deneme | ETİKET (5. tur = 3. tur kuralı) | kural etiketi | İKİ YÖNLÜ (TERS) | dış sınama ABD / AVR 2016-22 | karar hücreleri: durum (n, KAT5, konum eşli KAT5 [n], plasebo KAT5) — ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26 |",
         "|---|---|---|---|---|---|"]
    for k in den:
        D = J["deneme"][k]; h_ = kh(D)
        hc = " · ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' / TERS' if h_.get(tuple(x), {}).get('ters') else ''} (n {h_.get(tuple(x), {}).get('n', 0)}, "
                        f"KAT5 {_sy(h_.get(tuple(x), {}).get('h5_kat'))}, konum {_sy(h_.get(tuple(x), {}).get('k_h5_kat'))} [{h_.get(tuple(x), {}).get('k_n', 0)}], "
                        f"plasebo {_sy(h_.get(tuple(x), {}).get('pl_h5_kat'))})" for x in Y["karar"]["hucre_karar"])
        ds = " / ".join(f"{h_.get(tuple(x), {}).get('durum', '-')}{' TERS' if h_.get(tuple(x), {}).get('ters') else ''}" for x in K["dis_sinama"])
        s.append(f"| {k} {D['ad']}{' (BİLGİ, karar değil)' if D.get('bilgi') else ''} | **{D['etiket']}** | {D.get('etiket_kural', '-')} | "
                 f"{D.get('ters_etiket', '-')} | {ds} | {hc} |")
    s += ["", f"Etiket kuralı (3. tur, AYNEN): {K['etiket']}.", f"TERS: {K['ters']}.", "",
          f"DÜRÜSTLÜK: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ (Y11 / Y11b Y9'un alt kümesi; Y9 hücreleri 3. turda görüldü). Dış sınama (2016-22 "
          f"ABD / AVR) ve BIST hücreleri {KB}: Y9'un 2016-22 ve BIST hücreleri 3. tur raporunda görüldü. Asıl karar Mart 2027 ileri testidir "
          "(kriz sonrası veri, aynı eşik).", ""]
    T = json.load(open(os.path.join(cikti, YH_DOSYA["tasarim5"]), encoding="utf-8")) if os.path.exists(os.path.join(cikti, YH_DOSYA["tasarim5"])) else {}
    s += ["## 2. TASARIM KONTROLÜ (ön kayıttan ÖNCE, sonuç okunmadan; tasarim5.json)", ""]
    if T.get("kayit"):
        son = T["kayit"][-1]
        s += _yh_tasarim_md(T)
        if T.get("ayar_kullanilmadi_gerekce"):
            s += [f"AYAR KULLANILMADI — gerekçe: {T['ayar_kullanilmadi_gerekce']}", ""]
        s += [f"Özet: No 38 Ş9'u {'GEÇMEDİ' if son['a_no38_gecmedi'] else 'GEÇTİ'}; TUR 2 kazan sayfaları {son['b_tur2_gecen']} / 4 geçti; ayar "
              + ("YAPILMADI" if len(T["kayit"]) == 1 else "YAPILDI (tek hak: " + ", ".join(
                  f"{a} {T['kayit'][0]['esik'][a]} -> {son['esik'][a]}" for a in ("F26_min", "F25_alt") if T["kayit"][0]["esik"][a] != son["esik"][a]) + ")") + ".", ""]
    else:
        s += ["(tasarım kaydı yok)", ""]
    s += ["## 3. HUNİ (getirisiz)", ""]
    olcum = {k: {(h["pazar"], h["donem"]): h.get("n", 0) for h in J["deneme"][k]["hucre"] if h["donem"] in _YH_DONEM3} for k in den}
    s += _yh_huni_md(J.get("huni5", {}), "Y11", {a: olcum[a] for a in den})
    s += ["", "Y1 eşleşmesi: " + "; ".join(f"{p}: Y1 olay {x.get('y1_olay', '?')} = özellik satırı {x.get('ozellik_satir')} (eşleşen {x.get('eslesen')})"
                                           for p, x in J.get("y11_eslesme", {}).items()) + ".", "",
          "## 4. OLAY SAYIMI ve DENETİMLER", "",
          "| Deneme | Pazar | girdi | düşen (giriş / havuz / tekil) | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma (5 olay, F1-F29) | F15 çeyrek uyumu | Y1 regresyonu (satır) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in den:
        for p, x in J["sayim"].get(k, {}).items():
            rg = J.get("regresyon_y1", {}).get(k, {}).get(p, {})
            s.append(f"| {k} | {p} | {x.get('girdi', 0)} | {x.get('giris_yok', 0) + x.get('havuz_disi', 0) + x.get('tekil', 0)} | {x.get('giris_stop_otesi', 0)} | "
                     f"{x.get('olc15_yok', 0)} | {x.get('es_az', 0)} | {x.get('plasebo_yok', 0)} | {J['gelecek_denetimi'].get(k, {}).get(p, '-')} TUTTU | "
                     f"{'%' + format(x.get('ceyrek_uyum_binde', 0) / 10, '.1f') if 'ceyrek_uyum_binde' in x else '-'} | {'EŞİT ' + str(rg.get('n')) if rg.get('esit') else '-'} |")
    s += ["", "## 5. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95)", "",
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
    s += ["", "## 6. KONUM EŞLİ KAT (zorunlu; eş = aynı gün, aynı kova VE F15 aynı çeyrek)", "",
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
    s += ["", "## 7. OLASILIK TABLOSU (olay / eş / taban; KAT = olay / eş [%95])", "",
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
    s += ["", f"## 8. DIŞ SINAMA (2016-22 ABD / AVR; {KB})", ""] + alt_tablo(K["dis_sinama"])
    s += ["", "Dış sınama kararı: " + "; ".join(f"{k}: TUTAR {'evet' if J['deneme'][k].get('dis_sinama_tutar') else 'hayır'}, TERS "
                                                 f"{'evet' if J['deneme'][k].get('dis_sinama_ters') else 'hayır'}" for k in den) + "."]
    s += ["", f"## 9. BIST (bilgi; ayrı başlık; karar değil; {KB})", ""] + alt_tablo(K["bist_bilgi"])
    s += ["", "## 10. İKİ YÖNLÜ ETİKET (TERS EMARE kuralı; karar hücreleri)", "", "| Deneme | Hücre | n | KAT5 [%95] | üst < 1 | yarı 1 / yarı 2 | TERS |",
          "|---|---|---|---|---|---|---|"]
    for k in den:
        hk = kh(J["deneme"][k])
        for x in Y["karar"]["hucre_karar"]:
            h = hk.get(tuple(x), {}); u = h.get("h5_ust")
            s.append(f"| {k} | {x[0]} {x[1]} | {h.get('n', 0)} | {_sy(h.get('h5_kat'))} [{_sy(h.get('h5_alt'))}, {_sy(u)}] | "
                     f"{'evet' if (u is not None and u == u and u < 1) else 'hayır'} | {_sy(h.get('yari1_kat5'))} / {_sy(h.get('yari2_kat5'))} | "
                     f"{'TERS' if h.get('ters') else '-'} |")
        s.append(f"| {k} | **ters etiket** | | | | | **{J['deneme'][k].get('ters_etiket', '-')}** |")
    s += ["", "## 11. BİLGİ: High ile hedef, takip stoplu getiri, çıkış", "",
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
    s += ["", "## 12. ÇOKLU KARŞILAŞTIRMA (bilgi; Y11 / Y11b karar hücreleri KAT5 bootstrap p = P(KAT <= 1), BH q 0,10 YALNIZ n >= 30 hücreler; aile 'bh_tur5')", "",
          "| Deneme | Hücre | n | p | BH geçer |", "|---|---|---|---|---|"]
    nh = {(k, h["pazar"], h["donem"]): h.get("n", 0) for k in den for h in J["deneme"][k]["hucre"]}
    for b in J.get("bh_tur5", []):
        if "p" in b:
            s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {nh.get((b['deneme'], b['pazar'], b['donem']), '-')} | {_sy(b['p'], 3)} | {'evet' if b['bh_q10'] else 'hayır'} |")
        else:
            s.append(f"| {b['deneme']} | {b['pazar']} {b['donem']} | {b['n']} | - | {b['not']} |")
    U = J.get("cemal_uyum_tur5", {})
    s += ["", "## 13. CEMAL'İN GÖZÜYLE UYUM (bilgi; ölçümden bağımsız, sonuç h5 OKUNMAZ; yalnız etiket ve özellik)", "",
          f"Sayfa: {U.get('n', 0)} (" + ", ".join(f"{a} {b}" for a, b in U.get("set", {}).items()) + "); Cemal: " + ", ".join(f"{a} {b}" for a, b in U.get("cemal", {}).items())
          + ". Hakem setinde yalnız KÖR yarı. n küçük: Fisher p bilgi.", "",
          "| Küme | Deneme | OLUR: tutar / tutmaz | OLMAZ: tutar / tutmaz | BELİRSİZ: tutar / tutmaz | tutanlarda OLUR payı | tutmayanlarda OLUR payı | Fisher p (OLUR / OLMAZ x tutar) |",
          "|---|---|---|---|---|---|---|---|"]
    for r in U.get("tablo", []):
        a1, a0, z1, z0 = r["OLUR_tutar"], r["OLMAZ_tutar"], r["OLUR_tutmaz"], r["OLMAZ_tutmaz"]
        s.append(f"| {r['set']} | {r['deneme']} | {a1} / {z1} | {a0} / {z0} | {r['BELİRSİZ_tutar']} / {r['BELİRSİZ_tutmaz']} | "
                 f"{_yz(a1 / (a1 + a0)) if a1 + a0 else '-'} ({a1}/{a1 + a0}) | {_yz(z1 / (z1 + z0)) if z1 + z0 else '-'} ({z1}/{z1 + z0}) | {_sy(r['fisher_p'], 3)} |")
    s += ["", "Şart başına (bütün sayfalar; OLUR payı = OLUR / (OLUR + OLMAZ)):", "",
          "| Şart | tutan sayfa | tutanlarda karar (OLUR+OLMAZ) / OLUR payı | tutmayanlarda karar / OLUR payı | Fisher p |", "|---|---|---|---|---|"]
    for r in U.get("sart", []):
        ad = r["sart"] if r["sart"] == "F14" else f"Ş{r['sart'][1:]}"
        s.append(f"| {ad} | {r['tutar']} | {r['tutar_karar']} / {_yz(r['olur_pay_tutar'])} | {r['tutmaz_karar']} / {_yz(r['olur_pay_tutmaz'])} | {_sy(r['fisher_p'], 3)} |")
    P7 = U.get("s7pdf", {})
    if P7:
        s += ["", f"S7 PDF'inin {P7['n']} olayında Ş9 tutan: {P7['s9_tutan']} (" + ", ".join(f"{a} {b[1]} / {b[0]}" for a, b in P7["pazar"].items())
              + f"); No 38 Ş9 {'TUTAR' if P7['no38_s9'] else 'tutmaz'}; tutan No: {', '.join(map(str, P7['tutan_no'])) or '-'}; F24-F29 hepsi NaN olay {P7['nan']}."]
    T5 = J.get("tur5_orneklem", {})
    s += ["", "## 14. TUR 4 KURU SAYIM (GOZ_ETIKET T1.5 = T1.4, deneme Y11; `tur ac --no 4` KOŞULMADI; dosya yazılmadı)", ""]
    if T5:
        s += [f"Sürüm {T5.get('surum')} (tur no {T5.get('tur_no')}); kota " + ", ".join(f"{a} {b}" for a, b in T5.get("kota", {}).items()) + ".", "",
              "| Pazar x dönem | uygun Y11 olayı (giriş <= kriz - 30 g) | gösterilmemiş |", "|---|---|---|"]
        for a, b in T5.get("uygun", {}).items():
            s.append(f"| {a} | {b} | {T5.get('gosterilmemis', {}).get(a, 0)} |")
        s += ["", "Gösterilmemiş hisse (pazar başına, turda hisse en çok 1): " + ", ".join(f"{a} {b}" for a, b in T5.get("hisse_gosterilmemis", {}).items()) + ".",
              f"Kuru örneklem: {T5.get('kuru', {}).get('durum', '-')}" + (f" ({T5['kuru'].get('neden')})" if T5.get("kuru", {}).get("neden") else "")
              + (f"; dağılım " + ", ".join(f"{a} {b}" for a, b in T5["kuru"].get("dagilim", {}).items()) if T5.get("kuru", {}).get("dagilim") else "") + "."]
    else:
        s.append("(hesaplanmadı)")
    IL = J.get("ilerleme5", {})
    s += ["", "## 15. İLERLEME (satır dosyalarından; hücre başına n ve P(+5) olay / eş; h5 ve eş h5 ölçülebilir olaylar)", ""]
    if IL.get("deneme"):
        hd = [f"{p} {q}" for p in OC.OC_ESIK["pazar"] for q in _YH_DONEM3]
        s += ["| Deneme | " + " | ".join(hd) + " |", "|---|" + "---|" * len(hd)]
        for d in _YH_ILERLEME:
            R = IL["deneme"].get(d)
            if not R or "yok" in R:
                s.append(f"| {d} | " + " | ".join("-" for _ in hd) + " |"); continue
            s.append(f"| {d} | " + " | ".join(f"{R[x]['n']}: {_yz(R[x]['p_olay'])} / {_yz(R[x]['p_es'])}" if R[x]["n"] else "0" for x in hd) + " |")
        s += ["", f"Satır dosyasından yeniden hesap = sonuc.json hücresi (n, P olay, P eş): {'TUTTU (hepsi)' if IL.get('uyum') else 'TUTMADI: ' + ', '.join(IL.get('uyumsuz', []))}."]
    s += ["", "## 16. VERİ SINIRLARI", ""]
    for p, n_ in J.get("veri_not", {}).items():
        s.append(f"- {p}: " + "; ".join(n_))
    s += ["- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.",
          "- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı; DİPTE (Ş1) olaylarda bu yanlılık daha "
          "büyük olabilir (eş ve plasebo aynı evrenden).",
          "- Sonradan bilgi: Ş9 Cemal'in S7 PDF'i No 38 ve TUR 2 sayfalarına bakılarak yazıldı; ABD / AVR 2023 ve 2024-26 bakılmış; 2016-22 ve BIST "
          f"{KB}.", "",
          "## 17. YENİDEN ÜRETİM (satır dosyasından iki hücre; biri konum eşli)", "", "```",
          "python - <<'EOF'", "import pandas as pd",
          "for d, p, q in [('Y11c', 'ABD', '2024-26'), ('Y11', 'ABD', '2016-22')]:",
          "    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q)]",
          "    a = x[x.h5.notna() & x.es_h5.notna()]; b = x[x.h5.notna() & x.k_es_h5.notna()]",
          "    print(d, p, q, len(a), round(a.h5.sum() / a.es_h5.sum(), 4), round(a.st5.mean(), 4), round(a.es_st5.mean(), 4), len(b), round(b.h5.sum() / b.k_es_h5.sum(), 4))",
          "EOF", "```", "", "Satır dosyası 5 MB'ı aşarsa scratch yolundadır (sonuc.json 'satir_dosya').", "",
          yh_kontrol_tablosu(YH_KONTROL_5), "", "## HATA", ""]
    hl = J.get("hata_tur5", [])
    s += [f"- {x}" for x in hl] if hl else ["(yok)"]
    metin = "\n".join(s) + "\n"
    _yh_yaz(_yh_yol("rapor5", cikti), metin, "rapor 5")
    return metin


# ================================================================ 6. TUR (YAPI_HEDEF_IS_TANIMI_6.md): GRUPLAR + FİLTRE KARNESİ + MAHKEME
# Cemal (19 Kas 2026): (1) trend içi raf / düşüş sonrası dip / rastgele gruplarından hangisi daha çok hedefe ulaşır; (2) dersler filtre olur,
# her filtre yürüyen sınamayla karnelenir, kötü çıkan son filtre SORGULA'ya düşer; (3) MAHKEME: seçilen bölge her kurala uyuyor mu, öncesindeki
# bölge neden seçilmedi. YH_ESIK (Y1-Y11c) DEĞİŞMEZ (ON_KAYIT_5.md YH_ESIK_SHA); 6. turun eşikleri ayrı sözlükte (YH_ESIK6), ön kayıtta mühürlü.
YH_DOSYA.update({"onkayit6": "ON_KAYIT_6.md", "rapor6": "RAPOR_6.md", "grup6": "grup6.json", "g3": "grup6_G3.csv", "olay_g6": "olay_G6.csv.gz",
                 "karne_md": "FILTRE_KARNE.md", "karne_json": "filtre_karne.json", "s7_mahkeme": "S7_MAHKEME.md", "s7_mahkeme_json": "s7_mahkeme.json"})
YH_YOL["is_tanimi6"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_IS_TANIMI_6.md")
YH_YOL["tur4_anahtar"] = os.path.join(YH_YOL["ge_cikti"], "tur", "4", "tur_4_anahtar.json")
YH_YOL["tur4_mahkeme"] = os.path.join(YH_YOL["ge_cikti"], "tur", "4", "TUR_4_MAHKEME.md")
_YH_GRUP6 = ["G0", "G1", "G2", "G2u", "G3"]
_YH_KURAL6 = ["S1", "S2", "S3", "S4", "S5", "S6", "S9", "S7", "S8", "F14", "C8", "C13"]
_YH_KURAL6_AD = {"S1": "Ş1 dipte", "S2": "Ş2 hat net", "S3": "Ş3 dip savunulmuş", "S4": "Ş4 küçük mum", "S5": "Ş5 alt fitil kısa",
                 "S6": "Ş6 kazan dönüş", "S9": "Ş9 U dip", "S7": "Ş7 yakın tavan gövdeli kırılım", "S8": "Ş8 yol almamış", "F14": "F14 büyük resim",
                 "C8": "C8 kağıt hafızası", "C13": "C13 dev mum yok"}
_YH_G6_KOL = ["deneme", "pazar", "sembol", "tarih", "giris", "donem", "hucre", "d", "j", "dd", "olc", "h5", "h10", "st5", "h5H", "h10H", "es_h5",
              "es_h10", "es_st5", "es_h5H", "es_h10H", "n_es", "tb_h5", "tb_h10", "tb_st5", "pl_h5", "pl_h10", "pl_st5", "getiri", "cikis_bar",
              "cikis_tur", "F14", "F15", "F17", "q_olay", "q_panel", "k_es_h5", "k_es_h10", "k_es_st5", "k_n_es", "es_f15_ort", "es_f15_med",
              "es_ayni_ceyrek"] + _YH_GRUP6

YH_ESIK6: Dict[str, Any] = {
    "surum": "6.0",
    "taban": "YH_ESIK (Y1-Y11c, ölçü cetveli, karar ve etiket kuralı) AYNEN; yh_esik_sha() = ON_KAYIT_5.md YH_ESIK_SHA olmalı (kapı)",
    "grup": {
        "G0": {"ad": "BÜTÜN Y1 (taban)", "tanim": "bütün Y1 OLAYLARI (olay_Y1.csv.gz satırları = özellik dosyası satırları)"},
        "G1": {"ad": "TREND İÇİ RAF", "F14_min": 0.0, "F15_min": 0.50, "tanim": "Y1 olayı VE F14 >= 0 VE F15 >= 0,50 (NaN tutmaz)"},
        "G2": {"ad": "DÜŞÜŞ SONRASI DİP", "F15_ust": 0.25, "F17_ust": -0.20, "tanim": "Y1 olayı VE Ş1 (F15 <= 0,25 VE F17 <= -0,20) = Y9 kümesi"},
        "G2u": {"ad": "DİP + U", "tanim": "G2 VE Ş9 (YH_ESIK Y11 eşikleri, altı alt şart; NaN tutmaz)"},
        "G3": {"ad": "RASTGELE", "tohum": 106,
               "tanim": "her (pazar, dönem) hücresinde Y1 OLAY satırlarından (olay_Y1.csv.gz; dönem = giriş günü dönemi) yerine koymadan G2'nin aynı "
                        "hücredeki OLAY satırı sayısı kadar; satırlar (sembol, tarih) sırasında; rng = default_rng([106, pazar no, dönem no]); G2 0 "
                        "ise 0; G2 olaylarını da içerebilir; örneklem ön kayıtta grup6_G3.csv (sha) ile mühürlü (getirisiz: yalnız kimlik + dönem)"}},
    "olcu": "1. tur 15 bar cetveli AYNEN: olay ölçümü = Y1 ölçümü (yh_olc_pazar deneme 'Y1'; eş / taban / plasebo tohumu Y1'inki; satırlar "
            "olay_Y1.csv.gz ile regresyon, plasebo dahil) -> grup satırları Y1 satırlarının alt kümesi; hücre: yh_hucre (h5 / h10 / st5 olay, eş, "
            "KAT5 ay kümeli %95, plasebo) + yh_hucre_konum (konum eşli KAT, yh_konum_es_olc); hücre kuralı ve durum (yh_durum, güç tablosu 1. tur) "
            "ve etiket 3. tur kuralı (yh_etiket + yh_etiket3: ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> en fazla EMARE; dış sınama ABD / AVR 2016-22; "
            "TERS iki yönlü); hücreler ABD / AVR / BIST x 2016-22 / 2023 / 2024-26",
    "fark": {"ciftler": [["G2", "G1"], ["G2", "G3"]], "bootstrap": 2000, "tohum": 66, "guven": [0.025, 0.975],
             "tanim": "FARK = P(+%5) olay (G2) - P(+%5) olay (Gx), ölçülen olaylar (h5 ve eş h5 var: yh_hucre n'i); %95 aralık: iki grupta AYRI "
                      "ay kümeli bootstrap (giriş ayı, yerine koyarak, 2000, rng [66, pazar no, dönem no, çift no]); BİLGİ (karar kuralı yok)"},
    "tutarlilik": "G2 (pazar, sembol, tarih) kümesi = olay_Y9.csv.gz kümesi VE h5 / h10 / st5 / es_h5 / es_st5 / n_es / tb_h5 / getiri / k_es_h5 / "
                  "k_es_st5 / k_n_es eşit (göreli 1e-4, NaN = NaN); G0 ∩ F15 >= 0,75 kümesi = olay_Y9c.csv.gz kümesi (aynı sütunlar); değilse DUR",
    "gelecek": "her grup x pazar: yh_gelecek5 (5 rastgele olay; veri t'de kesilir; Y1 sinyali + F1-F29 kesik veriden = dosya; değilse DUR)",
    "karne": {
        "sira": ["S1", "S2", "S3", "S4", "S5", "S6", "S9", "S7", "S8", "F14"],
        "kollar": {"S7": ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "F14"], "U": ["S1", "S2", "S3", "S4", "S5", "S9", "S7", "S8", "F14"]},
        "donem": {"egitim": ["2016-22"], "sinama": ["2023", "2024-26"]},
        "n_min": 30, "pazar": ["ABD", "AVR", "BIST", "ABD+AVR"], "karar_pazar": "ABD+AVR",
        "tanim": "Huni Y1 (adım 0) -> + filtre (kol sırasıyla; Ş1-Ş5 iki kolda ortak). Her adım x pazar x dönem: n = ölçülen olay (h5 ve eş h5 var), "
                 "P olay = ort h5, P eş = ort es_h5, FARK = P olay - P eş, MARJİNAL = FARK(adım) - FARK(önceki adım). EĞİTİM 2016-22, SINAMA 2023-26 "
                 "(2023 + 2024-26); tersi (eğitim 2023-26, sınama 2016-22) aynı iki sayıyı kullandığı için etiket simetriktir",
        "etiket": "KATKI+ = marjinal > 0 iki dönemde VE adım n >= 30 iki dönemde; KATKI− = marjinal < 0 iki dönemde VE n >= 30 iki dönemde; "
                  "değilse SORGULA (dönemler çelişiyor ya da n < 30)",
        "tek_cikarma": "TAM kol kümesi (kolun bütün filtreleri) ve her filtre tek tek çıkarılınca: DELTA = FARK(tam - f) - FARK(tam), iki dönem; "
                       "DELTA > 0 iki dönemde (n >= 30 iki dönemde) -> ZARAR VERİYOR; DELTA < 0 iki dönemde -> YARARLI; değilse BELİRSİZ",
        "sorgula": "SORGULANACAK FİLTRELER: karar pazarı satırlarında (ABD+AVR) etiketi SORGULA ya da KATKI− olan (filtre, kol) çiftleri, kolda en son "
                   "eklenenden geriye; ayrıca tek-çıkarmada ZARAR VERİYOR olanlar"},
    "mahkeme": {
        "gun": 250, "c13_carp": 4.0, "c13_gun": 250, "s9_kaydir": [5, 120, 5], "kurallar": list(_YH_KURAL6),
        "girdi": "(pazar, sembol, t) Y1 olayı; veri t'de KESİLİR (t sonrası okunmaz); adaylar [t-250, t-1] içinde; her kural değeri yalnız kendi "
                 "gününe kadarki veriyle (adayın günü t_k'dan öncesi okunur: F3 ATR250, F14 250 bar, F17 60 gün; sonrası okunmaz)",
        "kural": "Ş1 F15 <= 0,25 VE F17 <= -0,20; Ş2 F1 >= 3; Ş3 F2 >= -0,01; Ş4 F3 <= 0,90; Ş5 F4 <= 0,25; Ş6 F20 >= 0; Ş9 altı alt şart (Y11); "
                 "Ş7 F22 > 0 VE F22a < 0 VE F23 >= 0,50; Ş8 F18 <= 0,20; F14 >= 0; C8 F16 = 0 (son 250 barda KIRILDI bölge sayısı); C13 max |C_k / "
                 "C_k-1 - 1| (son 250 bar, k = t-249..t) <= 4 x ATR250 (ort TR / C_önceki, aynı 250 bar; 250 bar yoksa NaN = tutmaz). NaN = ✗",
        "puan": "PUAN = ✓ sayısı / 12 kural",
        "aday_a": "S6 (s6_taban, kesik veri) bölgeleri, seçilenin bölgesi hariç, son barı [t-250, t-1] içinde ve bitişi t'ye kadar bilinen: AL "
                  "(t_k = al günü; bölge = GE bölgesi), KIRILDI (t_k = kırılma günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = TAVAN(t_k-1)), "
                  "ZAMAN AŞIMI / sönme (t_k = kutunun son günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = kutu_ust(t_k))",
        "aday_b": "Ş9 çanak: t_k = t-5, t-10, ..., t-120; Ş9 t_k'da TUTARSA aday; bölge = Ş9 penceresi [t_k-40, t_k-1], hat = min Low, tavan = max "
                  "High[t_k-15, t_k-1]",
        "ozellik": "F1-F18 = GOZ_ETIKET.ge_ozellik_bar (aday için bölge sahte 'AL' olarak verilir; F16 gerçek durum dizisinden), F20-F23 = yh_s7_bar, "
                   "F24-F29 = yh_s9_bar (t_k'da)",
        "karar": "seçilenin puanı >= en iyi önceki adayın puanı -> SEÇİM TUTARLI; değilse ÖNCEKİ BÖLGE DAHA UYGUN (en iyi aday: en yüksek puan, "
                 "eşitlikte en yakın); önceki aday yoksa SEÇİM TUTARLI (önceki aday yok). Ayrıca seçilen bölge tam puan değilse eksik kurallar",
        "kapi": "prefix: her adayın kural değerleri veri t_k'da kesilince aynı (göreli 1e-9); seçilen bölgenin F1-F29 + F16 değerleri özellik "
                "dosyalarıyla aynı (göreli 1e-5); toplu md'lerde sembol / tarih sızıntısı 0"},
}

YH_KONTROL_6: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "gruplar Y1 olay satırlarının alt kümesi; eş / taban / plasebo 1. tur kodu (yh_olc_pazar 'Y1' -> yh_olay_olc, yh_sim; aynı gün, "
                   "aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); konum eşli KAT (yh_konum_es_olc: eşin F15'i olayın çeyreğinde: G1 / G2 "
                   "konum farkı momentum kovasıyla karışmasın); G3 rastgele grup aynı hücre, aynı n (G2 ile); karne FARK = olay - eş (aynı gün aynı kova)"),
    "K2": ("EVET", "grup tanımları F14 / F15 / F17 / Ş9 mühürlü özellik dosyalarından (yalnız [.., t]); koşuda her grup x pazar 5 olay veri t'de "
                   "kesilerek yeniden (yh_gelecek5, DURUR); mahkeme veriyi t'de keser, her aday yalnız t_k'ya kadar (prefix kapısı: t_k'da kesik "
                   "veri = aynı değer); G3 örneklemi yalnız kimlik + dönem ile, ön kayıtta mühürlü"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); mahkeme pencereleri geçerli "
                   "bar sayımıyla; C13 ATR250 geçerli barlarla"),
    "K4": ("EVET", "Y1 olayları OC 60 gün tekil; yh_olc_pazar'da hiçbir olay düşmemeli (DURUR); n = bağımsız olay; grup hücrelerinde getiri "
                   "ortalama + medyan (yh_hucre); mahkeme adayları bölge başına bir kez (S6 bölge kimliği)"),
    "K5": ("EVET", "giriş t+1 açılışı (OC); Y1 regresyonu: ölçülen her satır olay_Y1.csv.gz satırına eşit (plasebo dahil), DURUR"),
    "K6": ("EVET", "aynı V_*.pkl tek kip; bütün ölçüler oran / sayı (birimden bağımsız); AVR yerel para; mahkeme çıktısında fiyat seviyesi yok"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; G2 (dipte) gruplarında batan hisse "
                   "eksikliği daha büyük olabilir -> G2 - G1 farkı yukarı yanlı okunur; rapora yazılır"),
    "K8": ("EVET", "grup x hücre n (ölçülen) tabloda; n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; ABD / AVR 2023 ve 2024-26 "
                   "BAKILMIŞ (Y1 ve Y9 hücreleri önceki turlarda görüldü; G1 / G2u / G3 Y1 alt kümesi) -> etiket en fazla EMARE; karne n < 30 SORGULA; "
                   "grup farkı bootstrap %95 (bilgi); küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_6.md: YH_ESIK6_SHA, YH_ESIK_SHA (= ON_KAYIT_5.md: Y1-Y11c aynen), kod / OC / S6 / GE fonksiyon / özellik / Y1-Y9-Y9c "
                   "olay / güç / G3 / s7_bolge_pdf sha + git; yh_kapi6 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit "
                   "(A koşusundan önce), ölçüm ikinci commit; B / C yeni eşik seçmez (B raporlama, C getirisiz); eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve mühürlü özellik dosyaları; TUR 4 anahtarı yalnız okunur (sayfa -> "
                          "kimlik), sha md'ye yazılır"),
    "K11": ("EVET", "olay_G6.csv.gz satır dosyası (grup bayraklı); RAPOR_6.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli) bağımsız komutla; "
                    "tutarlılık kapısı G2 = olay_Y9, G0 ∩ F15 >= 0,75 = olay_Y9c; karne olay_Y1 + özellik dosyalarından yeniden üretilebilir"),
    "K12": ("EVET", "etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS iki yönlü); grup farkı ve karne 'bilgi'; 'iz değil' yazılmaz; mahkeme "
                    "kararı kural uyumu (getiri değil); sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ / _YH_ önekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, tur/1-5 içeriklerine "
                    "dokunulmadı (git diff; TUR 4 anahtarı yalnız okundu); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da "
                    "'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm ve kural denetimi"),
}


def yh_esik6_sha(E6: Optional[Dict[str, Any]] = None) -> str:
    return yh_esik_sha(YH_ESIK6 if E6 is None else E6)


def _yh_ge_fn_sha() -> str:
    """GOZ_ETIKET'in F1-F18 fonksiyonlarının (ge_s6, ge_bolge, ge_ozellik_bar, GE_ESIK 'ozellik') kaynak sha'sı: dosyanın başka yerleri başka
    ajanca değişebilir; 6. tur yalnız bu fonksiyonlara dayanır."""
    import inspect
    import GOZ_ETIKET as GE
    s = "".join(inspect.getsource(f) for f in (GE.ge_s6, GE.ge_bolge, GE.ge_ozellik_bar))
    s += json.dumps(GE.GE_ESIK["ozellik"], sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- A) GRUPLAR
def yh_grup6_maske(F: pd.DataFrame, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, np.ndarray]:
    """G0 / G1 / G2 / G2u bayrakları (F14, F15, F17, F24-F29 sütunlu çerçeve; NaN tutmaz). G3 örneklemle (yh_grup6_g3)."""
    G = E6["grup"]; g = lambda c: F[c].to_numpy(float)  # noqa: E731
    with np.errstate(invalid="ignore"):
        g1 = (g("F14") >= G["G1"]["F14_min"]) & (g("F15") >= G["G1"]["F15_min"])
        g2 = (g("F15") <= G["G2"]["F15_ust"]) & (g("F17") <= G["G2"]["F17_ust"])
    s9 = np.ones(len(F), bool)
    for v in yh_s9_alt(F, Y).values():
        s9 &= v
    return {"G0": np.ones(len(F), bool), "G1": np.asarray(g1, bool), "G2": np.asarray(g2, bool), "G2u": np.asarray(g2, bool) & s9}


def yh_g6_taban(olay_y1: Optional[str] = None) -> pd.DataFrame:
    """GETİRİSİZ taban: olay_Y1.csv.gz'den YALNIZ kimlik + dönem (pazar, sembol, tarih, donem) ∩ özellik dosyaları (F1-F29) + grup bayrakları."""
    yo = olay_y1 or os.path.join(YH_YOL["cikti"], YH_DOSYA["satir"].format(d="Y1"))
    if not os.path.exists(yo):
        raise YHHata(f"olay_Y1 yok: {yo}")
    K = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih", "donem"], parse_dates=["tarih"], dtype={"sembol": str})
    F = yh_ozellik5_oku()
    M = K.merge(F, on=["pazar", "sembol", "tarih"], how="outer", validate="one_to_one", indicator=True)
    if (M._merge != "both").any():
        raise YHHata(f"6. tur: olay_Y1 ve özellik anahtarları farklı ({int((M._merge != 'both').sum())} satır) -> DURDU")
    M = M.drop(columns="_merge").sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    for k, v in yh_grup6_maske(M).items():
        M[k] = v
    return M


def yh_grup6_g3(M: pd.DataFrame, E6: Dict[str, Any] = YH_ESIK6) -> pd.DataFrame:
    """G3 örneklemi (getirisiz): her (pazar, dönem) hücresinde G2 olay sayısı kadar Y1 olayı, yerine koymadan, tohum [106, pazar no, dönem no]."""
    t = int(E6["grup"]["G3"]["tohum"]); dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]; out = []
    for pi, p in enumerate(OC.OC_ESIK["pazar"]):
        for qi, q in enumerate(dn):
            X = M[(M.pazar == p) & (M.donem == q)].sort_values(["sembol", "tarih"]).reset_index(drop=True)
            n = int(X.G2.sum())
            if n <= 0 or not len(X):
                continue
            sec = np.random.default_rng([t, pi, qi]).choice(len(X), n, replace=False)
            out.append(X.iloc[np.sort(sec)][["pazar", "sembol", "tarih", "donem"]])
    G3 = pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["pazar", "sembol", "tarih", "donem"])
    return G3.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)


def yh_grup6_g3_yaz(cikti: Optional[str] = None, olay_y1: Optional[str] = None) -> Tuple[str, pd.DataFrame]:
    cikti = cikti or YH_YOL["cikti"]; M = yh_g6_taban(olay_y1); G3 = yh_grup6_g3(M)
    yol = os.path.join(cikti, YH_DOSYA["g3"])
    _yh_yaz(yol, G3.assign(tarih=pd.to_datetime(G3.tarih).dt.strftime("%Y-%m-%d")).to_csv(index=False), "G3 örneklemi")
    return yol, M


def yh_grup6_say(M: pd.DataFrame, G3: pd.DataFrame) -> Dict[str, Any]:
    """Getirisiz grup sayımı: grup x pazar x dönem olay satırı sayısı (ölçülebilirlik bilinmez)."""
    k3 = set(zip(G3.pazar, G3.sembol.astype(str), pd.to_datetime(G3.tarih)))
    M = M.copy(); M["G3"] = [x in k3 for x in zip(M.pazar, M.sembol.astype(str), pd.to_datetime(M.tarih))]
    out: Dict[str, Any] = {}
    for g in _YH_GRUP6:
        out[g] = {f"{p}|{q}": int(((M.pazar == p) & (M.donem == q) & M[g]).sum()) for p in OC.OC_ESIK["pazar"] for q, _a, _b in OC.OC_ESIK["donem"]}
    return out


def yh_karne_huni_say(M: pd.DataFrame, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Getirisiz karne hunisi: kol x adım x pazar x (eğitim / sınama) olay satırı sayısı."""
    Kn = E6["karne"]; S = yh_s9_sartlar(M, Y); out: Dict[str, Any] = {}
    for kol, sira in Kn["kollar"].items():
        m = np.ones(len(M), bool); ad = []
        for f in ["Y1"] + sira:
            if f != "Y1":
                m = m & S[f]
            r = {}
            for pz in Kn["pazar"]:
                pm = M.pazar.isin(pz.split("+")).to_numpy()
                for dk, dl in Kn["donem"].items():
                    r[f"{pz}|{dk}"] = int((m & pm & M.donem.isin(dl).to_numpy()).sum())
            ad.append({"filtre": f, **r})
        out[kol] = ad
    return out


def _yh_ay_boot(h: np.ndarray, ay: np.ndarray, B: int, rng: np.random.Generator) -> np.ndarray:
    """Ay kümeli bootstrap: aylar yerine koyarak çekilir; P = Σ h / Σ n."""
    aylar, inv = np.unique(ay, return_inverse=True)
    sh = np.bincount(inv, weights=h, minlength=len(aylar)); sn = np.bincount(inv, minlength=len(aylar)).astype(float)
    sec = rng.integers(0, len(aylar), size=(B, len(aylar)))
    with np.errstate(invalid="ignore", divide="ignore"):
        return sh[sec].sum(1) / sn[sec].sum(1)


def yh_grup6_fark(A: pd.DataFrame, B_: pd.DataFrame, tohum: List[int], E6: Dict[str, Any] = YH_ESIK6) -> Dict[str, Any]:
    """FARK = P(h5) A - P(h5) B (ölçülen olaylar); iki grupta ayrı ay kümeli bootstrap %95."""
    F = E6["fark"]
    a = A[A.h5.notna() & A.es_h5.notna()]; b = B_[B_.h5.notna() & B_.es_h5.notna()]
    out = {"n_a": int(len(a)), "n_b": int(len(b)), "p_a": float(a.h5.mean()) if len(a) else np.nan, "p_b": float(b.h5.mean()) if len(b) else np.nan,
           "fark": np.nan, "alt": np.nan, "ust": np.nan}
    if not len(a) or not len(b):
        return out
    out["fark"] = out["p_a"] - out["p_b"]
    rng = np.random.default_rng([int(F["tohum"])] + list(tohum))
    ay = lambda x: pd.to_datetime(x.giris).dt.to_period("M").astype(str).to_numpy()  # noqa: E731
    va = _yh_ay_boot(a.h5.to_numpy(float), ay(a), int(F["bootstrap"]), rng); vb = _yh_ay_boot(b.h5.to_numpy(float), ay(b), int(F["bootstrap"]), rng)
    v = va - vb; v = v[np.isfinite(v)]
    if len(v):
        out["alt"] = float(np.quantile(v, F["guven"][0])); out["ust"] = float(np.quantile(v, F["guven"][1]))
    return out


def yh_grup6_sonuc(Ol: pd.DataFrame, grup: str, tablo: Optional[Dict[str, Any]], E6: Dict[str, Any] = YH_ESIK6,
                   Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Bir grubun hücreleri: yh_hucre + yh_hucre_konum + durum + TERS + bakılmış / dış sınama + 3. tur etiketi (yön +)."""
    K = _yh_kural3(Y); H_ = []; dur = {}
    for p in OC.OC_ESIK["pazar"]:
        for q, _a, _b in OC.OC_ESIK["donem"]:
            x = Ol[(Ol.pazar == p) & (Ol.donem == q)] if len(Ol) else Ol
            h = yh_hucre(x, Y); h.update(yh_hucre_konum(x, Y))
            durum, g = yh_durum(h, 1, tablo, Y); dur[(p, q)] = durum
            H_.append({"pazar": p, "donem": q, "karar_hucre": [p, q] in Y["karar"]["hucre_karar"], **h, "guc": g, "durum": durum,
                       "ters": yh_ters(h, Y), "bakilmis": [p, q] in K["bakilmis"], "dis_sinama": [p, q] in K["dis_sinama"]})
    out = {"ad": E6["grup"][grup]["ad"], "yon": 1, "hucre": H_, "etiket_kural": yh_etiket(dur, Y)}
    out.update(yh_etiket3(H_, out["etiket_kural"], Y))
    return out


_YH_TUT_KOL = ["h5", "h10", "st5", "es_h5", "es_st5", "n_es", "tb_h5", "getiri", "k_es_h5", "k_es_st5", "k_n_es"]


def yh_grup6_tutarlilik(Ol: pd.DataFrame, cikti: str) -> Dict[str, Any]:
    """G2 = olay_Y9 kümesi ve satırları; G0 ∩ F15 >= 0,75 = olay_Y9c kümesi ve satırları. Değilse YHHata."""
    out = {}
    for ad, dosya, m in (("G2=Y9", "Y9", Ol.G2.to_numpy(bool)), ("F15>=0,75=Y9c", "Y9c", Ol.F15.to_numpy(float) >= 0.75)):
        yol = os.path.join(cikti, YH_DOSYA["satir"].format(d=dosya))
        if not os.path.exists(yol):
            sy = _yh_yol("sonuc", cikti); J = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
            rel = J.get("deneme", {}).get(dosya, {}).get("satir_dosya")
            yol = (rel if os.path.isabs(rel) else os.path.join(KOK_YH, rel)) if rel else yol
        if not os.path.exists(yol):
            raise YHHata(f"tutarlılık kapısı: {dosya} satır dosyası yok -> DURDU")
        R = pd.read_csv(yol, parse_dates=["tarih"], dtype={"sembol": str})
        a = Ol[m][["pazar", "sembol", "tarih"] + _YH_TUT_KOL].copy(); a["tarih"] = pd.to_datetime(a.tarih); a["sembol"] = a.sembol.astype(str)
        J_ = a.merge(R[["pazar", "sembol", "tarih"] + _YH_TUT_KOL], on=["pazar", "sembol", "tarih"], how="outer", suffixes=("", "_r"),
                     indicator=True, validate="one_to_one")
        fark = {"yalniz_grup": int((J_._merge == "left_only").sum()), "yalniz_dosya": int((J_._merge == "right_only").sum())}
        B = J_[J_._merge == "both"]
        for c in _YH_TUT_KOL:
            bad = ~np.isclose(B[c].to_numpy(float), B[c + "_r"].to_numpy(float), rtol=1e-4, atol=1e-6, equal_nan=True)
            if bad.any():
                fark[c] = int(bad.sum())
        if any(fark.values()):
            raise YHHata(f"tutarlılık kapısı {ad} TUTMADI: {fark} -> DURDU")
        out[ad] = {"n": int(len(B)), "esit": True}
    return out


# ---------------------------------------------------------------- ÖN KAYIT / KAPI
def yh_sha_simdi6(cikti: Optional[str] = None) -> Dict[str, str]:
    cikti = cikti or YH_YOL["cikti"]
    out = {"esik6": yh_esik6_sha(), "esik": yh_esik_sha(), "kod": _yh_sha_dosya(YH_YOL["kod"]), "oc": _yh_sha_dosya(YH_YOL["oc_kod"]),
           "s6": _yh_sha_dosya(YH_YOL["s6_kod"]), "gefn": _yh_ge_fn_sha(), "guc": _yh_sha_dosya(_yh_yol("guc_json", cikti))}
    for ad, yol in (("ozellik", YH_YOL["ozellik"]), ("s7ozellik", YH_YOL["ozellik_s7"]), ("s9ozellik", YH_YOL["ozellik_s9"]),
                    ("g3", os.path.join(cikti, YH_DOSYA["g3"])), ("s7pdfkod", YH_YOL["s7_pdf_kod"])):
        if not os.path.exists(yol):
            raise YHHata(f"6. tur: dosya yok: {yol}")
        out[ad] = _yh_sha_dosya(yol)
    sy = _yh_yol("sonuc", cikti); J = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
    out["y1olay"] = _yh_sha_dosya(_yh_y1_satir_yolu(J, cikti))
    for d in ("Y9", "Y9c"):
        yol = os.path.join(cikti, YH_DOSYA["satir"].format(d=d))
        rel = J.get("deneme", {}).get(d, {}).get("satir_dosya")
        if not os.path.exists(yol) and rel:
            yol = rel if os.path.isabs(rel) else os.path.join(KOK_YH, rel)
        out[d.lower() + "olay"] = _yh_sha_dosya(yol) if os.path.exists(yol) else "0" * 64
    return out


_YH_KAPI_DESEN6 = {"esik6": r"YH_ESIK6_SHA:\s*`([0-9a-f]{64})`", "esik": r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"YH_KOD_SHA:\s*`([0-9a-f]{64})`",
                   "oc": r"OC_KOD_SHA:\s*`([0-9a-f]{64})`", "s6": r"S6_KOD_SHA:\s*`([0-9a-f]{64})`", "gefn": r"GE_FN_SHA:\s*`([0-9a-f]{64})`",
                   "guc": r"GUC_SHA:\s*`([0-9a-f]{64})`", "ozellik": r"OZELLIK_SHA:\s*`([0-9a-f]{64})`",
                   "s7ozellik": r"S7_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "s9ozellik": r"S9_OZELLIK_SHA:\s*`([0-9a-f]{64})`",
                   "g3": r"G3_SHA:\s*`([0-9a-f]{64})`", "s7pdfkod": r"S7PDF_KOD_SHA:\s*`([0-9a-f]{64})`", "y1olay": r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`",
                   "y9olay": r"Y9_OLAY_SHA:\s*`([0-9a-f]{64})`", "y9colay": r"Y9C_OLAY_SHA:\s*`([0-9a-f]{64})`"}


def _yh_esik_tur5_kontrol(cikti: str) -> str:
    """yh_esik_sha() = ON_KAYIT_5.md YH_ESIK_SHA (Y1-Y11c eşikleri, cetvel ve etiket kuralı AYNEN). Değilse YHHata."""
    y = _yh_yol("onkayit5", cikti)
    m = re.search(_YH_KAPI_DESEN["esik"], open(y, encoding="utf-8").read()) if os.path.exists(y) else None
    if not (m and m.group(1) == yh_esik_sha()):
        raise YHHata("6. tur: YH_ESIK ON_KAYIT_5.md mührüyle aynı değil (Y1-Y11c eşikleri değişmiş) -> DURDU")
    return m.group(1)


def _yh_is_tanimi6_bolum(harf: str, yol: Optional[str] = None) -> str:
    yol = yol or YH_YOL["is_tanimi6"]
    if not os.path.exists(yol):
        raise YHHata(f"6. tur iş tanımı yok: {yol}")
    m = re.search(rf"(?ms)^## {harf}\. [^\n]*\n(.*?)(?=^## |\Z)", open(yol, encoding="utf-8").read())
    if not m or not m.group(1).strip():
        raise YHHata(f"iş tanımı 6'da §{harf} bulunamadı")
    return m.group(1).strip()


def yh_onkayit6_metni(say: Dict[str, Any], huni: Dict[str, Any], sha: Dict[str, str], git5: Dict[str, str], git_is: Dict[str, str],
                      E6: Dict[str, Any] = YH_ESIK6) -> str:
    dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]; pz = OC.OC_ESIK["pazar"]
    s = ["# YAPI_HEDEF — ÖN KAYIT 6 (6. tur: GRUPLAR G1 / G2 / G2u / G3 + FİLTRE KARNESİ + MAHKEME)", "",
         f"{YH_SURUM}; 6. tur eklendi (YAPI_HEDEF_IS_TANIMI_6.md)", "",
         f"- YH_ESIK6_SHA: `{sha['esik6']}` (6. tur eşikleri: gruplar, fark, karne, mahkeme)",
         f"- YH_ESIK_SHA: `{sha['esik']}` (= ON_KAYIT_5.md YH_ESIK_SHA: Y1-Y11c, cetvel, karar ve etiket kuralı AYNEN)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)",
         f"- OC_KOD_SHA: `{sha['oc']}` (ORTAK_CETVEL.py)", f"- S6_KOD_SHA: `{sha['s6']}` (S6_TABAN.py)",
         f"- GE_FN_SHA: `{sha['gefn']}` (GOZ_ETIKET ge_s6 + ge_bolge + ge_ozellik_bar + GE_ESIK 'ozellik' kaynak metni; dosyanın geri kalanı başka "
         "ajanca değişebilir, 6. tur yalnız bunlara dayanır)",
         f"- GUC_SHA: `{sha['guc']}` (guc_tablosu.json, 1. tur)", f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)",
         f"- S7_OZELLIK_SHA: `{sha['s7ozellik']}` (ozellik_Y1_s7.csv.gz; F20-F23)", f"- S9_OZELLIK_SHA: `{sha['s9ozellik']}` (ozellik_Y1_s9.csv.gz; F24-F29)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (olay_Y1.csv.gz; regresyon)", f"- Y9_OLAY_SHA: `{sha['y9olay']}` (olay_Y9.csv.gz; tutarlılık kapısı)",
         f"- Y9C_OLAY_SHA: `{sha['y9colay']}` (olay_Y9c.csv.gz; tutarlılık kapısı)",
         f"- G3_SHA: `{sha['g3']}` (grup6_G3.csv; rastgele grup örneklemi, getirisiz)",
         f"- S7PDF_KOD_SHA: `{sha['s7pdfkod']}` (s7_bolge_pdf.py; mahkeme 50 olay sırası)"]
    if git5:
        s.append(f"- ON_KAYIT_5: git {git5.get('commit', '?')[:10]}, {git5.get('zaman', '?')}")
    if git_is:
        s.append(f"- IS_TANIMI_6: git {git_is.get('commit', '?')[:10]}, {git_is.get('zaman', '?')}")
    s += [f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
          "Bu dosya 6. tur A ölçümünden ÖNCE yazıldı. Gruplar için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / konum eşli "
          "oran hesaplamadı ve okumadı: aşağıdaki sayılar yalnız olay_Y1.csv.gz'nin kimlik + dönem sütunları ve mühürlü özellik dosyalarından "
          "(getirisiz). `python YAPI_HEDEF.py grup6` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y11c mührünü denetler; biri "
          "tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez. B (filtre karnesi) getiri okur ama eşik seçmez (raporlama); C (mahkeme) "
          "getirisizdir.", "",
          "## İŞ TANIMI 6 §A / §B / §C (AYNEN)", "", "### A", _yh_is_tanimi6_bolum("A"), "", "### B", _yh_is_tanimi6_bolum("B"), "", "### C",
          _yh_is_tanimi6_bolum("C"), "",
          "## TANIMLAR ve EŞİKLER (YH_ESIK6; uygulama kararları dahil)", ""]
    for g in ("G0", "G1", "G2", "G2u", "G3"):
        s.append(f"- {g} {E6['grup'][g]['ad']}: {E6['grup'][g]['tanim']}.")
    s += [f"- ÖLÇÜ: {E6['olcu']}.", f"- GRUP FARKI: {E6['fark']['tanim']}.", f"- TUTARLILIK KAPISI: {E6['tutarlilik']}.",
          f"- GELECEĞE BAKMA: {E6['gelecek']}.", f"- KARNE: {E6['karne']['tanim']}.", f"- KARNE ETİKETİ: {E6['karne']['etiket']}.",
          f"- TEK-ÇIKARMA: {E6['karne']['tek_cikarma']}.", f"- {E6['karne']['sorgula']}.",
          f"- KARNE KOLLARI: S7 = {' -> '.join(E6['karne']['kollar']['S7'])}; U = {' -> '.join(E6['karne']['kollar']['U'])}; pazarlar "
          f"{', '.join(E6['karne']['pazar'])} (karar pazarı {E6['karne']['karar_pazar']}).",
          f"- MAHKEME GİRDİ: {E6['mahkeme']['girdi']}.", f"- MAHKEME KURALLARI (12): {E6['mahkeme']['kural']}.", f"- {E6['mahkeme']['puan']}.",
          f"- ÖNCEKİ ADAYLAR (a): {E6['mahkeme']['aday_a']}.", f"- ÖNCEKİ ADAYLAR (b): {E6['mahkeme']['aday_b']}.",
          f"- ÖZELLİK HESABI: {E6['mahkeme']['ozellik']}.", f"- KARAR: {E6['mahkeme']['karar']}.", f"- MAHKEME KAPILARI: {E6['mahkeme']['kapi']}.", "",
          "UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden önce yazıldı): (1) 'yalnız [t-250, t] barları' = adaylar [t-250, t-1] içinde; her "
          "kural değeri kendi gününe kadarki veriyle (öncesi okunabilir: F3 ATR250 / F14 250 bar / F17 60 gün; sonrası okunmaz); (2) Ş9 adaylarının "
          "bölgesi Ş9 penceresidir (bölge kuralları Ş2-Ş5 / F17 / F18 için bir bölge gerekir); (3) karne karar satırı ABD+AVR birleşik (karar "
          "pazarları), ABD / AVR / BIST ayrı satırlar bilgi; (4) G3 olay satırı sayısıyla eşlenir (ölçülebilirlik sonra bilinir); (5) grup "
          "plasebosu Y1'in plasebosudur (deneme tohumu 'Y1'); (6) KATKI etiketi 'tersi' yönünde aynıdır (iki dönem sayısı simetrik).", "",
          "## GRUP OLAY SAYILARI (getirisiz; olay satırı = Y1 olayı, ölçülebilirlik bilinmez)", "",
          "| Grup | " + " | ".join(f"{p} {q}" for p in pz for q in dn) + " | toplam |", "|---|" + "---|" * (len(pz) * len(dn) + 1)]
    for g in _YH_GRUP6:
        v = say[g]; s.append(f"| {g} {E6['grup'][g]['ad']} | " + " | ".join(str(v[f'{p}|{q}']) for p in pz for q in dn) + f" | {sum(v.values())} |")
    s += ["", "## KARNE HUNİSİ (getirisiz; olay satırı; eğitim 2016-22 / sınama 2023-26)", ""]
    for kol, adim in huni.items():
        kk = list(adim[0].keys())[1:]
        s += [f"Kol {kol}:", "", "| Adım | " + " | ".join(k.replace("|", " ") for k in kk) + " |", "|---|" + "---|" * len(kk)]
        for r in adim:
            s.append(f"| {r['filtre']} | " + " | ".join(str(r[k]) for k in kk) + " |")
        s.append("")
    s += [yh_kontrol_tablosu(YH_KONTROL_6), ""]
    return "\n".join(s) + "\n"


def yh_onkayit6_yaz(cikti: Optional[str] = None, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_6.md + grup6_G3.csv (getirisiz). 5. tur ölçülmüş olmalı, 6. tur ölçülmemiş; YH_ESIK = ON_KAYIT_5 mührü."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit6", cikti)
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"ön kayıt 6 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"ön kayıt 6 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(os.path.join(cikti, YH_DOSYA["grup6"])):
        raise YHHata("grup6.json var: 6. tur ölçülmüş; ön kayıt ölçümden sonra yazılamaz")
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("sonuc", cikti)) else {}
    if "Y11" not in J.get("deneme", {}):
        raise YHHata("Y11 ölçülmemiş: 6. tur 5. turdan sonra gelir")
    _yh_esik_tur5_kontrol(cikti)
    _gy, M = yh_grup6_g3_yaz(cikti, _yh_y1_satir_yolu(J, cikti))
    G3 = pd.read_csv(os.path.join(cikti, YH_DOSYA["g3"]), parse_dates=["tarih"], dtype={"sembol": str})
    say = yh_grup6_say(M, G3); huni = yh_karne_huni_say(M)
    for p in OC.OC_ESIK["pazar"]:
        for q, _a, _b in OC.OC_ESIK["donem"]:
            if say["G3"][f"{p}|{q}"] != say["G2"][f"{p}|{q}"]:
                raise YHHata(f"G3 n != G2 n ({p} {q}) -> DURDU")
    sha = yh_sha_simdi6(cikti)
    git5 = _yh_git(_yh_yol("onkayit5", cikti)) if git else {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi6"]) if git else {}
    except YHHata:
        git_is = {}
    _yh_yaz(yol, yh_onkayit6_metni(say, huni, sha, git5, git_is), "ön kayıt 6")
    return yol


def yh_kapi6(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """6. tur A koşu kapısı: ON_KAYIT_6.md kontrol listesi + bütün sha'lar + YH_ESIK = ON_KAYIT_5 mührü + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit6", cikti)
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt 6 yok: {yol}")
    metin = open(yol, encoding="utf-8").read()
    _yh_esik_tur5_kontrol(cikti)
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in {**_YH_KAPI_DESEN6, "zaman": _YH_KAPI_DESEN["zaman"]}.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"ön kayıt 6'da {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi6(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"]); out["git_g3"] = _yh_git(os.path.join(cikti, YH_DOSYA["g3"]))
        out["git_ozellik"] = _yh_git(YH_YOL["ozellik"]); out["git_s7"] = _yh_git(YH_YOL["ozellik_s7"]); out["git_s9"] = _yh_git(YH_YOL["ozellik_s9"])
    yhlog.info("yh_kapi6 AÇIK (%s)", yol)
    return out


# ---------------------------------------------------------------- A) KOŞU
def yh_kos6(cikti: Optional[str] = None, veri: Optional[str] = None, islem: int = 1, git: bool = True, kontrol: bool = True,
            E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """6. tur A: kapı -> pazar başına Y1 ölçümü (1. tur kodu) + konum eşli KAT + Y1 regresyonu (plasebo dahil) + grup bayrakları + geleceğe
    bakma -> tutarlılık kapısı -> grup x hücre sonuçları + grup farkları -> grup6.json, olay_G6.csv.gz. Bir kez koşar."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]; gy = os.path.join(cikti, YH_DOSYA["grup6"])
    if os.path.exists(gy):
        raise YHHata("grup6.json var: 6. tur A ölçümü bir kez koşulur")
    ok = yh_kapi6(cikti, git=git, kontrol=kontrol)
    kos_zaman = _yh_simdi()
    if ok["onkayit_zaman"] > kos_zaman:
        raise YHHata("ön kayıt zamanı koşu zamanından sonra")
    sonuc = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8"))
    tablo = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8"))
    O1 = pd.read_csv(_yh_y1_satir_yolu(sonuc, cikti), parse_dates=["tarih", "giris"], dtype={"sembol": str})
    G3 = pd.read_csv(os.path.join(cikti, YH_DOSYA["g3"]), parse_dates=["tarih"], dtype={"sembol": str})
    k3 = set(zip(G3.pazar, G3.sembol.astype(str), pd.to_datetime(G3.tarih)))
    K = _yh_kural3(Y); R: Dict[str, Any] = {"surum": YH_SURUM, "esik6_sha": yh_esik6_sha(E6), "kos": {"zaman_utc": kos_zaman, "kapi": ok, "islem": islem},
                                            "sayim": {}, "regresyon_y1": {}, "gelecek_denetimi": {}, "ceyrek_uyum_binde": {}, "veri_not": {}}
    parca = []
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        R["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        P = OC.oc_panel(Vd); Cl = yh_kapanis(P, Vd)
        S = yh_sinyaller5(Vd, p, ["Y11"], islem, Y, P=P); X = S["_Y11F"]
        Z, say = yh_olc_pazar(Vd, P, Cl, X, "Y1", p, islem, Y)
        dus = {a: int(say.get(a, 0)) for a in ("giris_yok", "giris_gec", "havuz_disi", "tekil")}
        if any(dus.values()):
            raise YHHata(f"6. tur {p}: Y1 olayı OC'de düştü {dus} -> DURDU")
        Z = Z.merge(X[["sembol", "tarih"] + _Y11_OZ].assign(tarih=pd.to_datetime(X.tarih)), on=["sembol", "tarih"], how="left", validate="one_to_one")
        Z = yh_konum_es_olc(P, Cl, Z, yh_f15_panel(P, Vd, Y), islem, Y)
        qv = Z[Z.q_olay >= 0]; uy = float((qv.q_olay == qv.q_panel).mean()) if len(qv) else 1.0
        R["ceyrek_uyum_binde"][p] = int(round(uy * 1000))
        if uy < K["konum_uyum_min"]:
            raise YHHata(f"6. tur {p}: panel F15 çeyreği dosyayla yalnız %{uy * 100:.1f} aynı (< %99) -> DURDU")
        R["regresyon_y1"][p] = yh_y1_regresyon(Z, O1)
        a_ = Z[["sembol", "tarih", "pl_h5", "pl_st5"]].assign(tarih=pd.to_datetime(Z.tarih)).merge(
            O1[O1.pazar == p][["sembol", "tarih", "pl_h5", "pl_st5"]], on=["sembol", "tarih"], suffixes=("", "_y1"), validate="one_to_one")
        plb = int(sum((~np.isclose(a_[c].to_numpy(float), a_[c + "_y1"].to_numpy(float), equal_nan=True)).sum() for c in ("pl_h5", "pl_st5")))
        if plb or len(a_) != len(Z):
            raise YHHata(f"6. tur {p}: plasebo regresyonu tutmadı ({plb} fark) -> DURDU")
        R["regresyon_y1"][p]["plasebo_esit"] = True
        for k, v in yh_grup6_maske(Z, E6, Y).items():
            Z[k] = v
        Z["G3"] = [(p, str(s_), pd.Timestamp(t_)) in k3 for s_, t_ in zip(Z.sembol, Z.tarih)]
        R["gelecek_denetimi"][p] = {g: yh_gelecek5(Vd, Z[Z[g]], "Y1", p, Y) for g in ("G1", "G2", "G2u", "G3")}
        R["sayim"][p] = {a: int(b) for a, b in say.items()}
        parca.append(Z)
        yhlog.info("6. tur %s: olay %d (%.0f sn)", p, len(Z), time.time() - t0)
        del Vd, P, Cl, S
    Ol = pd.concat(parca, ignore_index=True)
    if int(Ol.G3.sum()) != len(G3):
        raise YHHata(f"G3 örneklemi ({len(G3)}) ölçülen satırlarda {int(Ol.G3.sum())} -> DURDU")
    R["tutarlilik"] = yh_grup6_tutarlilik(Ol, cikti)
    R["grup"] = {g: yh_grup6_sonuc(Ol[Ol[g]], g, tablo, E6, Y) for g in _YH_GRUP6}
    R["fark"] = {}
    for ci, (a, b) in enumerate(E6["fark"]["ciftler"]):
        for pi, p in enumerate(OC.OC_ESIK["pazar"]):
            for qi, (q, _a, _b) in enumerate(OC.OC_ESIK["donem"]):
                x = Ol[(Ol.pazar == p) & (Ol.donem == q)]
                R["fark"][f"{a}-{b}|{p}|{q}"] = yh_grup6_fark(x[x[a]], x[x[b]], [pi, qi, ci], E6)
    Ol["deneme"] = "G6"
    yo = os.path.join(cikti, YH_DOSYA["olay_g6"])
    Ol[_YH_G6_KOL].to_csv(yo, index=False, float_format="%.6g", compression="gzip")
    R["satir_dosya"] = os.path.relpath(yo, KOK_YH); R["satir_sha"] = _yh_sha_dosya(yo)
    R["sure_sn"] = round(time.time() - t0, 1)
    _yh_yaz(gy, json.dumps(R, ensure_ascii=False, indent=1, default=_yh_json), "grup 6")
    return R


# ---------------------------------------------------------------- B) FİLTRE KARNESİ
def _yh_karne_hucre(X: pd.DataFrame) -> Dict[str, Any]:
    g = X[X.h5.notna() & X.es_h5.notna()]
    n = int(len(g))
    po = float(g.h5.mean()) if n else np.nan; pe = float(g.es_h5.mean()) if n else np.nan
    return {"n": n, "p_olay": po, "p_es": pe, "fark": po - pe if n else np.nan}


def _yh_karne_etiket(ma: float, mb: float, na: int, nb: int, nmin: int) -> str:
    if na >= nmin and nb >= nmin and np.isfinite(ma) and np.isfinite(mb):
        if ma > 0 and mb > 0:
            return "KATKI+"
        if ma < 0 and mb < 0:
            return "KATKI−"
    return "SORGULA"


def yh_filtre_karne(cikti: Optional[str] = None, olay_y1: Optional[str] = None, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK,
                    yaz: bool = True) -> Dict[str, Any]:
    """FİLTRE KARNESİ (sızıntısız yürüyen sınama; raporlama, eşik seçmez): olay_Y1.csv.gz (h5, es_h5) + özellik dosyaları -> her kol x adım x pazar
    x dönem n / P olay / P eş / FARK / MARJİNAL + etiket; tek-çıkarma; SORGULANACAK FİLTRELER. FILTRE_KARNE.md + filtre_karne.json."""
    cikti = cikti or YH_YOL["cikti"]; Kn = E6["karne"]
    sy = _yh_yol("sonuc", cikti); J = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
    yo = olay_y1 or _yh_y1_satir_yolu(J, cikti)
    O = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih", "donem", "h5", "es_h5"], parse_dates=["tarih"], dtype={"sembol": str})
    F = yh_ozellik5_oku()
    M = O.merge(F, on=["pazar", "sembol", "tarih"], how="inner", validate="one_to_one")
    if len(M) != len(O) or len(M) != len(F):
        raise YHHata(f"karne: olay_Y1 ({len(O)}) ve özellik ({len(F)}) eşleşmesi {len(M)} -> DURDU")
    S = yh_s9_sartlar(M, Y); dk = list(Kn["donem"].items())
    pm = {pz: M.pazar.isin(pz.split("+")).to_numpy() for pz in Kn["pazar"]}
    dm = {a: M.donem.isin(b).to_numpy() for a, b in dk}

    def hucre(m: np.ndarray, pz: str) -> Dict[str, Any]:
        return {a: _yh_karne_hucre(M[m & pm[pz] & dm[a]]) for a, _b in dk}

    tablo, tek = [], []
    for kol, sira in Kn["kollar"].items():
        m = np.ones(len(M), bool); onc = {pz: hucre(m, pz) for pz in Kn["pazar"]}
        for pz in Kn["pazar"]:
            tablo.append({"kol": kol, "adim": 0, "filtre": "Y1", "pazar": pz, **{a: {**onc[pz][a], "marjinal": np.nan} for a, _b in dk}, "etiket": "-"})
        for ai, f in enumerate(sira, 1):
            m = m & S[f]
            for pz in Kn["pazar"]:
                h = hucre(m, pz)
                for a, _b in dk:
                    h[a]["marjinal"] = h[a]["fark"] - onc[pz][a]["fark"] if np.isfinite(h[a]["fark"]) and np.isfinite(onc[pz][a]["fark"]) else np.nan
                (a1, _), (a2, _) = dk
                et = _yh_karne_etiket(h[a1]["marjinal"], h[a2]["marjinal"], h[a1]["n"], h[a2]["n"], int(Kn["n_min"]))
                tablo.append({"kol": kol, "adim": ai, "filtre": f, "pazar": pz, **h, "etiket": et}); onc[pz] = h
        tam = np.ones(len(M), bool)
        for f in sira:
            tam &= S[f]
        for f in sira:
            m_ = np.ones(len(M), bool)
            for g_ in sira:
                if g_ != f:
                    m_ &= S[g_]
            for pz in Kn["pazar"]:
                ht = hucre(tam, pz); hc = hucre(m_, pz); r = {"kol": kol, "filtre": f, "pazar": pz}
                for a, _b in dk:
                    r[a] = {"n_tam": ht[a]["n"], "fark_tam": ht[a]["fark"], "n_cikar": hc[a]["n"], "fark_cikar": hc[a]["fark"],
                            "delta": hc[a]["fark"] - ht[a]["fark"] if np.isfinite(hc[a]["fark"]) and np.isfinite(ht[a]["fark"]) else np.nan}
                (a1, _), (a2, _) = dk
                ok_n = all(r[a]["n_tam"] >= Kn["n_min"] and r[a]["n_cikar"] >= Kn["n_min"] for a in (a1, a2))
                d1, d2 = r[a1]["delta"], r[a2]["delta"]
                r["etiket"] = ("ZARAR VERİYOR" if ok_n and d1 > 0 and d2 > 0 else "YARARLI" if ok_n and d1 < 0 and d2 < 0 else "BELİRSİZ")
                tek.append(r)
    kp = Kn["karar_pazar"]; sor = []
    for kol, sira in Kn["kollar"].items():
        for f in reversed(sira):
            r = [x for x in tablo if x["kol"] == kol and x["filtre"] == f and x["pazar"] == kp][0]
            if r["etiket"] in ("SORGULA", "KATKI−"):
                sor.append(f"{_YH_KURAL6_AD.get(f, f)} [{kol} kolu, {r['etiket']}]")
        for f in reversed(sira):
            r = [x for x in tek if x["kol"] == kol and x["filtre"] == f and x["pazar"] == kp][0]
            if r["etiket"] == "ZARAR VERİYOR":
                sor.append(f"{_YH_KURAL6_AD.get(f, f)} [{kol} kolu, tek-çıkarma: ZARAR VERİYOR]")
    out = {"surum": YH_SURUM, "zaman_utc": _yh_simdi(), "esik6_sha": yh_esik6_sha(E6), "olay_y1_sha": _yh_sha_dosya(yo),
           "ozellik_sha": [_yh_sha_dosya(YH_YOL[k]) for k in ("ozellik", "ozellik_s7", "ozellik_s9")], "tablo": tablo, "tek_cikarma": tek,
           "sorgulanacak": sor}
    if yaz:
        _yh_yaz(os.path.join(cikti, YH_DOSYA["karne_json"]), json.dumps(out, ensure_ascii=False, indent=1, default=_yh_json), "karne json")
        _yh_yaz(os.path.join(cikti, YH_DOSYA["karne_md"]), yh_filtre_karne_md(out, E6), "karne md")
    return out


def yh_filtre_karne_md(R: Dict[str, Any], E6: Dict[str, Any] = YH_ESIK6) -> str:
    Kn = E6["karne"]; a1, a2 = list(Kn["donem"])
    yz = lambda x: "-" if x is None or not np.isfinite(float(x)) else f"{100 * float(x):+.1f}".replace(".", ",")  # noqa: E731
    s = ["# FİLTRE KARNESİ (yürüyen sınama; YAPI_HEDEF 6. tur §B)", "",
         f"{R['surum']}. Üretim: {R['zaman_utc']}. Komut: `python YAPI_HEDEF.py filtrekarne` (her yeni ders / filtre eklendiğinde AYNI komutla yenilenir). "
         "Girdi: olay_Y1.csv.gz (h5, es_h5) + özellik dosyaları (F1-F29). Eşik seçmez; raporlamadır.", "",
         f"Tanım: {Kn['tanim']}. Etiket: {Kn['etiket']}. Değerler yüzde puan (FARK = P olay - P eş). Eğitim = {', '.join(Kn['donem'][a1])}; "
         f"sınama = {', '.join(Kn['donem'][a2])}.", "",
         "**SORGULANACAK FİLTRELER: " + ("; ".join(R["sorgulanacak"]) if R["sorgulanacak"] else "yok") + "**", "",
         f"## 1. Karar pazarı ({Kn['karar_pazar']})", ""]

    def tablo(pz: str) -> List[str]:
        t = ["| Filtre | Kol | eğitim n | eğitim P olay / P eş | eğitim FARK | eğitim MARJİNAL | sınama n | sınama P olay / P eş | sınama FARK | "
             "sınama MARJİNAL | etiket |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in R["tablo"]:
            if r["pazar"] != pz:
                continue
            t.append(f"| {_YH_KURAL6_AD.get(r['filtre'], r['filtre'])} | {r['kol']} | {r[a1]['n']} | {_yz(r[a1]['p_olay'])} / {_yz(r[a1]['p_es'])} | "
                     f"{yz(r[a1]['fark'])} | {yz(r[a1]['marjinal'])} | {r[a2]['n']} | {_yz(r[a2]['p_olay'])} / {_yz(r[a2]['p_es'])} | "
                     f"{yz(r[a2]['fark'])} | {yz(r[a2]['marjinal'])} | {r['etiket']} |")
        return t

    def tek(pz: str) -> List[str]:
        t = ["| Çıkarılan filtre | Kol | eğitim n tam / çıkarılmış | eğitim FARK tam -> çıkarılmış (DELTA) | sınama n tam / çıkarılmış | "
             "sınama FARK tam -> çıkarılmış (DELTA) | etiket |", "|---|---|---|---|---|---|---|"]
        for r in R["tek_cikarma"]:
            if r["pazar"] != pz:
                continue
            t.append(f"| {_YH_KURAL6_AD.get(r['filtre'], r['filtre'])} | {r['kol']} | {r[a1]['n_tam']} / {r[a1]['n_cikar']} | {yz(r[a1]['fark_tam'])} -> "
                     f"{yz(r[a1]['fark_cikar'])} ({yz(r[a1]['delta'])}) | {r[a2]['n_tam']} / {r[a2]['n_cikar']} | {yz(r[a2]['fark_tam'])} -> "
                     f"{yz(r[a2]['fark_cikar'])} ({yz(r[a2]['delta'])}) | {r['etiket']} |")
        return t

    s += tablo(Kn["karar_pazar"]) + ["", f"### TEK-ÇIKARMA ({Kn['karar_pazar']}): {Kn['tek_cikarma']}", ""] + tek(Kn["karar_pazar"]) + [""]
    for pz in [x for x in Kn["pazar"] if x != Kn["karar_pazar"]]:
        s += [f"## {pz} (bilgi)", ""] + tablo(pz) + ["", f"Tek-çıkarma ({pz}):", ""] + tek(pz) + [""]
    s += ["Not: evren bugün işlem gören hisseler (hayatta kalma yanlılığı: P olay ve P eş yukarı yanlı; FARK'ta kısmen birbirini götürür). ABD / AVR "
          "2023-26 hücreleri önceki turlarda görüldü (bakılmış); karne kural seçmez, sorgulanacak filtreleri işaretler.", ""]
    return "\n".join(s) + "\n"


# ---------------------------------------------------------------- C) MAHKEME
def _yh_c13(H: np.ndarray, L: np.ndarray, C: np.ndarray, i: int, gun: int) -> float:
    """C13 ölçüsü: max |C_k / C_k-1 - 1| / ATR250, k = i-gun+1 .. i; ATR250 = ort TR / C_önceki aynı barlar. i < gun ise NaN."""
    if i < gun:
        return np.nan
    a = i - gun
    Cs, Hs, Ls = C[a:i + 1], H[a:i + 1], L[a:i + 1]
    r = np.abs(Cs[1:] / Cs[:-1] - 1.0); trp = _yh_trp(Hs, Ls, Cs)[1:]
    atr = float(np.mean(trp))
    return float(np.max(r) / atr) if np.isfinite(atr) and atr > 0 else np.nan


def yh_m_ozellik(d: pd.DataFrame, T: Dict[str, np.ndarray], i: int, bolge: Optional[Dict[str, float]] = None, E6: Dict[str, Any] = YH_ESIK6,
                 Y: Dict[str, Any] = YH_ESIK) -> Dict[str, float]:
    """t = i (geçerli bar) için F1-F18 (GOZ_ETIKET.ge_ozellik_bar), F20-F23 (yh_s7_bar), F24-F29 (yh_s9_bar), C13. bolge None: S6 'al' günü (GE
    bölgesi); değilse {sol, hat, ust, tavan} sahte 'AL' bölgesi olarak verilir (F16 gerçek durum dizisinden). Yalnız [.., i] okunur."""
    import GOZ_ETIKET as GE
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    T2 = T
    if bolge is not None:
        T2 = {k: v.copy() for k, v in T.items()}
        T2["al"][i] = True; T2["durum"][i] = "AL"; T2["kutu_alt"][i] = float(bolge["hat"]); T2["kutu_sol_i"][i] = float(bolge["sol"])
        T2["kutu_ust"][i] = float(bolge["ust"])
        if i >= 1:
            T2["tavan"][i - 1] = float(bolge["tavan"])
    F = dict(GE.ge_ozellik_bar(O, H, L, C, V, T2, int(i)))
    F.update(yh_s7_bar(O, H, L, C, int(i), Y)); F.update(yh_s9_bar(H, L, C, int(i), Y))
    F["C13"] = _yh_c13(H, L, C, int(i), int(E6["mahkeme"]["c13_gun"]))
    return F


def yh_m_kurallar(F: Dict[str, float], E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, bool]:
    """12 kural ✓ / ✗ (NaN = ✗)."""
    X = pd.DataFrame([{k: F.get(k, np.nan) for k in _Y11_OZ + ["F16", "C13"]}])
    S = yh_s9_sartlar(X, Y)
    out = {k: bool(S[k][0]) for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S9", "S7", "S8", "F14")}
    f16, c13 = F.get("F16", np.nan), F.get("C13", np.nan)
    out["C8"] = bool(np.isfinite(f16) and f16 == 0)
    out["C13"] = bool(np.isfinite(c13) and c13 <= float(E6["mahkeme"]["c13_carp"]))
    return {k: out[k] for k in _YH_KURAL6}


def _yh_m_deger(k: str, F: Dict[str, float]) -> Tuple[str, str]:
    """Kuralın ölçülen değeri ve eşiği (metin)."""
    f = lambda c, n=2: _sy(F.get(c), n)  # noqa: E731
    return {"S1": (f"F15 {f('F15')}, F17 {_yz(F.get('F17'))}", "F15 <= 0,25 VE F17 <= -%20"), "S2": (f"F1 {f('F1', 0)}", ">= 3"),
            "S3": (f"F2 {_yz(F.get('F2'))}", ">= -%1"), "S4": (f"F3 {f('F3')}", "<= 0,90"), "S5": (f"F4 {f('F4')}", "<= 0,25"),
            "S6": (f"F20 {_yz(F.get('F20'))}", ">= %0"),
            "S9": (f"a/ATR {f('F24', 3)}, x* {f('F25')}, R² {f('F26')}, sol {f('F27')}, sağ {f('F28')}, argmin-x* {f('F29', 1)}",
                   "a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5"),
            "S7": (f"F22 {_yz(F.get('F22'))}, F22a {_yz(F.get('F22a'))}, F23 {f('F23')}", "F22 > 0 VE F22a < 0 VE F23 >= 0,50"),
            "S8": (f"F18 {_yz(F.get('F18'))}", "<= %20"), "F14": (f"F14 {_yz(F.get('F14'))}", ">= %0"),
            "C8": (f"F16 {f('F16', 0)}", "= 0"), "C13": (f"en büyük günlük getiri / ATR {f('C13', 1)}", "<= 4")}[k]


def yh_mahkeme_hisse(df: pd.DataFrame, t: pd.Timestamp, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK,
                     prefix: bool = True) -> Dict[str, Any]:
    """Bir Y1 olayının mahkemesi (getirisiz). Veri t'de kesilir. Döner: seçilen (değer + kural + puan), adaylar, en iyi aday, karar."""
    t = pd.Timestamp(t); Mh = E6["mahkeme"]
    d = _yh_hazir(df); d = d[d.index <= t]
    if not len(d) or d.index[-1] != t:
        raise YHHata(f"mahkeme: {t.date()} geçerli bar değil")
    i = len(d) - 1
    T6 = S6.s6_taban(d, None)
    T = {"durum": T6["durum"].to_numpy(object), "kutu_sol_i": T6["kutu_sol_i"].to_numpy(float), "kutu_alt": T6["kutu_alt"].to_numpy(float),
         "kutu_ust": T6["kutu_ust"].to_numpy(float), "bas_i": T6["bas_i"].to_numpy(float), "dip": T6["dip"].to_numpy(float),
         "tavan": T6["tavan"].to_numpy(float), "al": T6["al"].to_numpy(bool)}
    if not T["al"][i]:
        raise YHHata(f"mahkeme: {t.date()} S6 'al' günü değil (Y1 olayı değil)")
    Fs = yh_m_ozellik(d, T, i, None, E6, Y); Ks = yh_m_kurallar(Fs, E6, Y)
    sec = {"bar": 0, "tur": str(T["durum"][i]), "F": Fs, "kural": Ks, "puan": int(sum(Ks.values()))}
    bid = T6["bolge_id"].to_numpy(int); al = T["al"]; kir = T6["kirildi"].to_numpy(bool); H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
    lo = i - int(Mh["gun"]); ad: List[Dict[str, Any]] = []
    for rid in np.unique(bid[:i][bid[:i] >= 0]):
        if bid[i] >= 0 and rid == bid[i]:
            continue
        sag = int(np.flatnonzero(bid[:i] == rid)[-1])
        if sag < lo or sag > i - 1:
            continue
        sol = T["kutu_sol_i"][sag]
        if not np.isfinite(sol) or int(sol) >= sag:
            continue
        if al[sag]:
            tur, bol = "AL", None
        elif kir[sag]:
            tur, bol = "KIRILDI", {"sol": int(sol), "hat": T["kutu_alt"][sag], "ust": T["kutu_ust"][sag], "tavan": T["tavan"][sag - 1]}
        else:
            tur, bol = "ZAMAN AŞIMI", {"sol": int(sol), "hat": T["kutu_alt"][sag], "ust": T["kutu_ust"][sag], "tavan": T["kutu_ust"][sag]}
        ad.append({"tk": sag, "tur": tur, "bolge": bol})
    a0, a1, ad_ = (int(x) for x in Mh["s9_kaydir"])
    for k in range(a0, a1 + 1, ad_):
        tk = i - k
        if tk < 41:
            continue
        s9 = yh_s9_bar(H, L, C, tk, Y)
        if all(yh_s9_alt(pd.DataFrame([s9]), Y)[x][0] for x in "abcdef"):
            ad.append({"tk": tk, "tur": "Ş9 ÇANAK", "bolge": {"sol": tk - 40, "hat": float(np.min(L[tk - 40:tk])), "ust": float(np.max(H[tk - 40:tk])),
                                                               "tavan": float(np.max(H[tk - 15:tk]))}})
    adaylar = []
    for a in ad:
        if a["bolge"] is not None and not (np.isfinite(a["bolge"]["hat"]) and a["bolge"]["hat"] > 0):
            continue
        Fa = yh_m_ozellik(d, T, a["tk"], a["bolge"], E6, Y)
        if prefix:                                         # bilgi yalnız adayın gününe kadar: veri t_k'da kesilince aynı değer
            dk = d.iloc[:a["tk"] + 1]; T6k = S6.s6_taban(dk, None)
            Tk = {"durum": T6k["durum"].to_numpy(object), "kutu_sol_i": T6k["kutu_sol_i"].to_numpy(float), "kutu_alt": T6k["kutu_alt"].to_numpy(float),
                  "kutu_ust": T6k["kutu_ust"].to_numpy(float), "bas_i": T6k["bas_i"].to_numpy(float), "dip": T6k["dip"].to_numpy(float),
                  "tavan": T6k["tavan"].to_numpy(float), "al": T6k["al"].to_numpy(bool)}
            Fb = yh_m_ozellik(dk, Tk, a["tk"], a["bolge"], E6, Y)
            ka = sorted(Fa)
            if not np.allclose(np.array([Fa[x] for x in ka], float), np.array([Fb[x] for x in ka], float), rtol=1e-9, atol=1e-12, equal_nan=True):
                raise YHHata(f"mahkeme prefix kapısı TUTMADI: aday bar -{i - a['tk']} ({a['tur']}) -> DURDU")
        Ka = yh_m_kurallar(Fa, E6, Y)
        adaylar.append({"bar": -(i - a["tk"]), "tur": a["tur"], "F": Fa, "kural": Ka, "puan": int(sum(Ka.values()))})
    return {"secilen": sec, "adaylar": sorted(adaylar, key=lambda x: x["bar"]), **yh_m_karar(sec, adaylar)}


def yh_m_karar(sec: Dict[str, Any], adaylar: List[Dict[str, Any]]) -> Dict[str, Any]:
    """KARAR: seçilenin puanı >= en iyi önceki adayın puanı -> SEÇİM TUTARLI; değilse ÖNCEKİ BÖLGE DAHA UYGUN (en iyi aday: en yüksek puan,
    eşitlikte en yakın = en büyük bar). sec / aday: {'bar', 'tur', 'kural': {kural: bool}, 'puan'}."""
    en = max(adaylar, key=lambda x: (x["puan"], x["bar"])) if adaylar else None
    nk = len(_YH_KURAL6); Ks = sec["kural"]
    eks_s = [k for k in _YH_KURAL6 if not Ks[k]]
    if en is None:
        karar = "SEÇİM TUTARLI (önceki aday yok)"
    elif sec["puan"] >= en["puan"]:
        karar = f"SEÇİM TUTARLI (seçilen {sec['puan']}/{nk} >= en iyi önceki aday {en['puan']}/{nk}, bar {en['bar']})"
    else:
        eks_a = [k for k in _YH_KURAL6 if not en["kural"][k]]
        karar = (f"ÖNCEKİ BÖLGE DAHA UYGUN: bar {en['bar']} ({en['tur']}), puan {en['puan']}/{nk} vs seçilen {sec['puan']}/{nk}; seçilenin tutmadığı "
                 f"kurallar: {', '.join(_YH_KURAL6_AD[k] for k in eks_s) or 'yok'}; önceki adayın tutmadığı: "
                 f"{', '.join(_YH_KURAL6_AD[k] for k in eks_a) or 'yok'}")
    return {"en_iyi": en, "karar": karar, "onceki_daha_uygun": bool(en is not None and en["puan"] > sec["puan"]), "tam_puan": not eks_s,
            "eksik": eks_s, "kural_sayisi": nk}


def yh_mahkeme_regresyon(M: Dict[str, Any], pazar: str, sembol: str, t: pd.Timestamp, Fdos: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Seçilen bölgenin F1-F29 + F16 değerleri özellik dosyalarıyla aynı mı (göreli 1e-5). Dosyada yoksa 'dosyada yok'."""
    Fd = yh_ozellik5_oku() if Fdos is None else Fdos
    if "F16" not in Fd.columns:
        F0 = yh_ozellik_oku()
        Fd = Fd.merge(F0[["pazar", "sembol", "tarih", "F16"]].assign(sembol=F0.sembol.astype(str)), on=["pazar", "sembol", "tarih"], how="left")
    r = Fd[(Fd.pazar == pazar) & (Fd.sembol.astype(str) == str(sembol)) & (pd.to_datetime(Fd.tarih) == pd.Timestamp(t))]
    if len(r) != 1:
        return {"durum": "dosyada yok"}
    kol = _Y11_OZ + (["F16"] if "F16" in r.columns else [])
    a = np.array([M["secilen"]["F"][k] for k in kol], float); b = r[kol].iloc[0].to_numpy(float)
    bad = [k for k, x, y in zip(kol, a, b) if not np.isclose(x, y, rtol=1e-5, atol=1e-7, equal_nan=True)]
    if bad:
        raise YHHata(f"mahkeme regresyonu TUTMADI ({pazar} olay): {bad} -> DURDU")
    return {"durum": "eşit", "n_kol": len(kol)}


def yh_mahkeme_metin(M: Dict[str, Any], baslik: str) -> str:
    nk = M["kural_sayisi"]; sec = M["secilen"]
    s = [f"### {baslik}", "", f"**KARAR: {M['karar']}**", "",
         f"Seçilen bölge (bar 0, {sec['tur']}): puan {sec['puan']}/{nk}; her kurala uyuyor mu: "
         + ("EVET" if M["tam_puan"] else "HAYIR (eksik: " + ", ".join(_YH_KURAL6_AD[k] for k in M["eksik"]) + ")"), "",
         "| Kural | seçilen | değer | eşik |" + (" en iyi önceki aday |" if M["en_iyi"] else ""), "|---|---|---|---|" + ("---|" if M["en_iyi"] else "")]
    for k in _YH_KURAL6:
        v, e = _yh_m_deger(k, sec["F"])
        ek = ""
        if M["en_iyi"]:
            va, _ = _yh_m_deger(k, M["en_iyi"]["F"]); ek = f" {'✓' if M['en_iyi']['kural'][k] else '✗'} {va} |"
        s.append(f"| {_YH_KURAL6_AD[k]} | {'✓' if sec['kural'][k] else '✗'} | {v} | {e} |{ek}")
    s += ["", f"Önceki adaylar ({len(M['adaylar'])}; [t-250, t-1]): "
          + ("; ".join(f"bar {a['bar']} {a['tur']} {a['puan']}/{nk}" for a in M["adaylar"]) if M["adaylar"] else "yok"), ""]
    return "\n".join(s)


def yh_mahkeme(pazar: str, sembol: str, tarih: Any, veri: Optional[str] = None, Vc: Optional[Dict[str, Any]] = None,
               E6: Dict[str, Any] = YH_ESIK6) -> Dict[str, Any]:
    Vc = {} if Vc is None else Vc
    if pazar not in Vc:
        Vc[pazar] = OC.oc_veri(pazar, klasor=veri or YH_YOL["veri"])
    if sembol not in Vc[pazar]["V"]:
        raise YHHata(f"mahkeme: {pazar} {sembol} veride yok")
    M = yh_mahkeme_hisse(Vc[pazar]["V"][sembol], pd.Timestamp(tarih), E6)
    M["regresyon"] = yh_mahkeme_regresyon(M, pazar, sembol, pd.Timestamp(tarih))
    return M


def _yh_m_json(M: Dict[str, Any]) -> Dict[str, Any]:
    j = lambda F: {k: (None if not np.isfinite(float(v)) else float(v)) for k, v in F.items()}  # noqa: E731
    return {"karar": M["karar"], "onceki_daha_uygun": M["onceki_daha_uygun"], "tam_puan": M["tam_puan"], "eksik": M["eksik"],
            "secilen": {**{k: v for k, v in M["secilen"].items() if k != "F"}, "F": j(M["secilen"]["F"])},
            "adaylar": [{**{k: v for k, v in a.items() if k != "F"}, "F": j(a["F"])} for a in M["adaylar"]],
            "en_iyi_bar": M["en_iyi"]["bar"] if M["en_iyi"] else None, "regresyon": M.get("regresyon", {})}


def yh_mahkeme_toplu(L: pd.DataFrame, md_yol: str, baslik: str, json_yol: Optional[str] = None, veri: Optional[str] = None,
                     ek_not: str = "", E6: Dict[str, Any] = YH_ESIK6) -> Dict[str, Any]:
    """Toplu mahkeme: L = [no, pazar, sembol, tarih]. Md / json'da yalnız No (sembol / tarih YOK); sızıntı denetimi (DURUR)."""
    Vc: Dict[str, Any] = {}; R = []; Fd = yh_ozellik5_oku()
    F0 = yh_ozellik_oku(); Fd = Fd.merge(F0[["pazar", "sembol", "tarih", "F16"]].assign(sembol=F0.sembol.astype(str)), on=["pazar", "sembol", "tarih"], how="left")
    for r in L.itertuples(index=False):
        try:
            if r.pazar not in Vc:
                Vc[r.pazar] = OC.oc_veri(r.pazar, klasor=veri or YH_YOL["veri"])
            if str(r.sembol) not in Vc[r.pazar]["V"]:
                raise YHHata("veride yok: hisse yok")
            M = yh_mahkeme_hisse(Vc[r.pazar]["V"][str(r.sembol)], pd.Timestamp(r.tarih), E6)
            M["regresyon"] = yh_mahkeme_regresyon(M, r.pazar, str(r.sembol), pd.Timestamp(r.tarih), Fd)
            R.append({"no": int(r.no), "pazar": r.pazar, "M": M})
        except YHHata as ex:
            if "TUTMADI" in str(ex):
                raise
            m_ = str(ex)
            neden = ("Y1 olayı değil (S6 'al' günü değil)" if "'al' günü değil" in m_ else "geçerli bar değil" if "geçerli bar değil" in m_
                     else "veride hisse yok" if "veride yok" in m_ else "hesaplanamadı")
            R.append({"no": int(r.no), "pazar": r.pazar, "M": None, "hata": neden})
    ok = [x for x in R if x["M"] is not None]; nk = len(_YH_KURAL6)
    once = [x for x in ok if x["M"]["onceki_daha_uygun"]]
    eks: Dict[str, int] = {}
    for x in ok:
        for k in x["M"]["eksik"]:
            eks[k] = eks.get(k, 0) + 1
    eks_s = sorted(eks.items(), key=lambda z: -z[1])
    oz = {"n": len(R), "mahkeme": len(ok), "onceki_daha_uygun": len(once), "tam_puan": sum(x["M"]["tam_puan"] for x in ok),
          "eksik_sikligi": {_YH_KURAL6_AD[k]: v for k, v in eks_s}, "hata": [{"no": x["no"], "hata": x["hata"]} for x in R if x["M"] is None],
          "regresyon_esit": sum(1 for x in ok if x["M"]["regresyon"].get("durum") == "eşit")}
    s = [f"# {baslik}", "", f"{YH_SURUM}; 6. tur §C MAHKEME (getirisiz: h5 / stop / getiri OKUNMADI). Üretim: {_yh_simdi()}. {ek_not}".strip(), "",
         "Kurallar (12; NaN = ✗): " + E6["mahkeme"]["kural"] + ".", "", "Önceki adaylar: (a) " + E6["mahkeme"]["aday_a"] + "; (b) " + E6["mahkeme"]["aday_b"] + ".",
         "", "## ÖZET", "",
         f"- Olay {oz['n']}; mahkeme kurulan {oz['mahkeme']}; ÖNCEKİ BÖLGE DAHA UYGUN: **{oz['onceki_daha_uygun']}** / {oz['mahkeme']}; seçilen bölge "
         f"her kurala uyuyor: {oz['tam_puan']} / {oz['mahkeme']}; seçilen bölge özellik dosyasıyla eşit: {oz['regresyon_esit']} / {oz['mahkeme']}.",
         "- En sık eksik kurallar (seçilen bölgede): " + (", ".join(f"{_YH_KURAL6_AD[k]} {v}" for k, v in eks_s) or "yok") + ".",
         "- Mahkeme kurulamayan: " + ("; ".join(f"No {h['no']}: {h['hata']}" for h in oz["hata"]) or "yok") + ".", "",
         "| No | Pazar | seçilen puan | önceki aday sayısı | en iyi önceki aday (bar, tür, puan) | karar |", "|---|---|---|---|---|---|"]
    for x in R:
        if x["M"] is None:
            s.append(f"| {x['no']} | {x['pazar']} | - | - | - | mahkeme yok ({x['hata']}) |"); continue
        M = x["M"]; e = M["en_iyi"]
        s.append(f"| {x['no']} | {x['pazar']} | {M['secilen']['puan']}/{nk} | {len(M['adaylar'])} | "
                 + (f"bar {e['bar']}, {e['tur']}, {e['puan']}/{nk}" if e else "-") + f" | {'ÖNCEKİ BÖLGE DAHA UYGUN' if M['onceki_daha_uygun'] else 'SEÇİM TUTARLI'} |")
    s += ["", "## OLAY SAYFALARI", ""]
    for x in ok:
        s += [yh_mahkeme_metin(x["M"], f"No {x['no']} ({x['pazar']})"), ""]
    metin = "\n".join(s) + "\n"
    kim = set(L.sembol.astype(str)); tar = {pd.Timestamp(z).strftime("%Y-%m-%d") for z in L.tarih}
    tok = set(re.findall(r"[A-Za-z0-9][A-Za-z0-9.\-]*", metin))
    siz = sorted((kim & tok) | {z for z in tar if z in metin})
    if siz:
        raise YHHata(f"toplu mahkeme: sembol / tarih sızıntısı {len(siz)} -> yazılmadı")
    _yh_yaz(md_yol, metin, "mahkeme md")
    J = {"surum": YH_SURUM, "esik6_sha": yh_esik6_sha(E6), "ozet": oz, "olay": [{"no": x["no"], "pazar": x["pazar"],
                                                                                   **(_yh_m_json(x["M"]) if x["M"] else {"hata": x["hata"]})} for x in R]}
    if json_yol:
        _yh_yaz(json_yol, json.dumps(J, ensure_ascii=False, indent=1, default=_yh_json), "mahkeme json")
    oz["sizinti"] = 0
    return {"ozet": oz, "md": md_yol, "json": json_yol}


def yh_mahkeme_s7(cikti: Optional[str] = None, veri: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or YH_YOL["cikti"]
    return yh_mahkeme_toplu(yh_s7pdf_olaylar(), os.path.join(cikti, YH_DOSYA["s7_mahkeme"]), "S7 MAHKEME (S7 PDF'i 50 olay; No = PDF sırası)",
                            os.path.join(cikti, YH_DOSYA["s7_mahkeme_json"]), veri)


def yh_mahkeme_tur4(veri: Optional[str] = None, yol: Optional[str] = None) -> Dict[str, Any]:
    """TUR 4 anahtarı (yalnız okunur) -> TUR_4_MAHKEME.md (sayfa no; sembol / tarih yok; SONUÇ YOK: kör). Anahtar yoksa {'atlandi': ...}."""
    ya = YH_YOL["tur4_anahtar"]
    if not os.path.exists(ya):
        return {"atlandi": "tur_4_anahtar.json yok (TUR 4 hazır değil)"}
    A = json.load(open(ya, encoding="utf-8"))["sayfa"]
    L = pd.DataFrame([{"no": int(k), "pazar": v["pazar"], "sembol": str(v["sembol"]), "tarih": pd.Timestamp(v["tarih"])} for k, v in A.items()])
    L = L.sort_values("no").reset_index(drop=True)
    return yh_mahkeme_toplu(L, yol or YH_YOL["tur4_mahkeme"], "TUR 4 MAHKEME (40 kör sayfa; sayfa No; SONUÇ YOK)", None, veri,
                            ek_not=f"Kör: sonuç (h5) okunmadı ve yazılmadı. TUR 4 anahtar sha: {_yh_sha_dosya(ya)[:16]}…")


# ---------------------------------------------------------------- D) RAPOR
YH_DOSYA.update({"tur4_mahkeme_ozet": "tur4_mahkeme_ozet.json", "hata6": "hata6.json"})


def yh_rapor6(cikti: Optional[str] = None, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> str:
    """RAPOR_6.md: A olasılık tablosu + grup farkları; B karne özeti; C mahkeme özetleri; yeniden üretim; HATA; KONTROL LİSTESİ."""
    cikti = cikti or YH_YOL["cikti"]; gy = os.path.join(cikti, YH_DOSYA["grup6"])
    if not os.path.exists(gy):
        raise YHHata("grup6.json yok: önce `python YAPI_HEDEF.py grup6`")
    R = json.load(open(gy, encoding="utf-8"))
    kp = lambda h: "BAKILMIŞ" if h.get("bakilmis") else ("dış sınama" if h.get("dis_sinama") else ("BIST bilgi" if h["pazar"] == "BIST" else ""))  # noqa: E731
    s = ["# YAPI_HEDEF — RAPOR 6 (GRUPLAR + FİLTRE KARNESİ + MAHKEME)", "",
         f"{R['surum']}. A koşusu: {R['kos']['zaman_utc']}; ön kayıt 6: {R['kos']['kapi'].get('onkayit_zaman', '?')} (git "
         f"{R['kos']['kapi'].get('git_onkayit', {}).get('commit', '?')[:10]}). Süre {R.get('sure_sn', '?')} sn.", "",
         "## A. GRUPLAR — SONUÇ (etiket 3. tur kuralı; ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> en fazla EMARE)", "",
         "| Grup | ETİKET | kural etiketi | İKİ YÖNLÜ (TERS) | karar hücreleri: durum (n, KAT5, konum KAT5) |", "|---|---|---|---|---|"]
    for g in _YH_GRUP6:
        D = R["grup"][g]; hk = {(h["pazar"], h["donem"]): h for h in D["hucre"]}
        hc = " · ".join(f"{p} {q}: {hk[(p, q)]['durum']} ({hk[(p, q)].get('n', 0)}, {_sy(hk[(p, q)].get('h5_kat'))}, {_sy(hk[(p, q)].get('k_h5_kat'))})"
                        for p, q in Y["karar"]["hucre_karar"])
        s.append(f"| {g} {D['ad']} | **{D['etiket']}** | {D['etiket_kural']} | {D['ters_etiket']} | {hc} |")
    s += ["", "### OLASILIK TABLOSU (Cemal biçimi; 15 bar, +%5 kapanışla stop'tan önce; eş = aynı gün aynı OC kovası, aynı d)", "",
          "| Grup | Hücre | n | +%5 payı | eş payı | KAT (%95) | konum eşli KAT [n] | stop payı (olay / eş) | plasebo KAT | durum | not |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for g in _YH_GRUP6:
        for h in R["grup"][g]["hucre"]:
            if not h.get("n"):
                s.append(f"| {g} | {h['pazar']} {h['donem']} | 0 | - | - | - | - | - | - | {h['durum']} | {kp(h)} |"); continue
            s.append(f"| {g} | {h['pazar']} {h['donem']} | {h['n']} | {_yz(h.get('h5_p_olay'))} | {_yz(h.get('h5_p_ref'))} | {_sy(h.get('h5_kat'))} "
                     f"({_sy(h.get('h5_alt'))}-{_sy(h.get('h5_ust'))}) | {_sy(h.get('k_h5_kat'))} [{h.get('k_n', 0)}] | {_yz(h.get('st5_p_olay'))} / "
                     f"{_yz(h.get('st5_p_ref'))} | {_sy(h.get('pl_h5_kat'))} | {h['durum']}{' TERS' if h.get('ters') else ''} | {kp(h)} |")
    s += ["", "### GRUP FARKLARI (P(+%5) olay; bilgi; iki grupta ayrı ay kümeli bootstrap %95)", "",
          "| Fark | Hücre | n (G2 / öteki) | P G2 | P öteki | FARK (%95) |", "|---|---|---|---|---|---|"]
    for k, v in R["fark"].items():
        a, p, q = k.split("|")
        yp = lambda x: "-" if x is None or not np.isfinite(float(x)) else f"{100 * float(x):+.1f}".replace(".", ",")  # noqa: E731
        s.append(f"| {a} | {p} {q} | {v['n_a']} / {v['n_b']} | {_yz(v['p_a'])} | {_yz(v['p_b'])} | {yp(v['fark'])} ({yp(v['alt'])} .. {yp(v['ust'])}) |")
    s += ["", "### DENETİMLER", "",
          "- Tutarlılık kapısı: " + "; ".join(f"{a}: n {b['n']} {'EŞİT' if b['esit'] else 'FARKLI'}" for a, b in R["tutarlilik"].items()) + ".",
          "- Y1 regresyonu (ölçülen satır = olay_Y1, plasebo dahil): " + "; ".join(f"{p}: n {v['n']}, {'eşit' if v['esit'] and v.get('plasebo_esit') else 'FARKLI'}"
                                                                             for p, v in R["regresyon_y1"].items()) + ".",
          "- Geleceğe bakma (grup x pazar 5 olay, F1-F29 kesik veriden): " + "; ".join(f"{p}: " + ", ".join(f"{g} {n}" for g, n in v.items())
                                                                                     for p, v in R["gelecek_denetimi"].items()) + ".",
          "- F15 çeyrek uyumu (binde): " + ", ".join(f"{p} {v}" for p, v in R["ceyrek_uyum_binde"].items()) + ".",
          "- K7: evren bugün işlem gören hisseler; G2 (dipte) batan hisse eksikliği daha büyük olabilir -> G2 payları ve G2 - G1 farkı yukarı yanlı.", ""]
    kj = os.path.join(cikti, YH_DOSYA["karne_json"])
    s += ["## B. FİLTRE KARNESİ (FILTRE_KARNE.md; `python YAPI_HEDEF.py filtrekarne`)", ""]
    if os.path.exists(kj):
        Kj = json.load(open(kj, encoding="utf-8")); Kn = E6["karne"]; a1, a2 = list(Kn["donem"])
        yp = lambda x: "-" if x is None or not np.isfinite(float(x)) else f"{100 * float(x):+.1f}".replace(".", ",")  # noqa: E731
        s += ["**SORGULANACAK FİLTRELER: " + ("; ".join(Kj["sorgulanacak"]) or "yok") + "**", "",
              f"Karar pazarı {Kn['karar_pazar']} (eğitim 2016-22 / sınama 2023-26; FARK ve MARJİNAL yüzde puan):", "",
              "| Filtre | Kol | eğitim n / FARK / MARJ | sınama n / FARK / MARJ | etiket |", "|---|---|---|---|---|"]
        for r in Kj["tablo"]:
            if r["pazar"] == Kn["karar_pazar"]:
                s.append(f"| {_YH_KURAL6_AD.get(r['filtre'], r['filtre'])} | {r['kol']} | {r[a1]['n']} / {yp(r[a1]['fark'])} / {yp(r[a1].get('marjinal'))} | "
                         f"{r[a2]['n']} / {yp(r[a2]['fark'])} / {yp(r[a2].get('marjinal'))} | {r['etiket']} |")
        s += ["", "Tek-çıkarma (ABD+AVR; DELTA = FARK(tam - f) - FARK(tam)): " + "; ".join(
            f"{r['kol']} {_YH_KURAL6_AD.get(r['filtre'], r['filtre'])} {yp(r[a1]['delta'])} / {yp(r[a2]['delta'])} {r['etiket']}"
            for r in Kj["tek_cikarma"] if r["pazar"] == Kn["karar_pazar"]) + ".", ""]
    else:
        s += ["(filtre_karne.json yok)", ""]
    s += ["## C. MAHKEME (getirisiz)", ""]
    for ad, yol in (("S7 PDF 50 olay (S7_MAHKEME.md)", os.path.join(cikti, YH_DOSYA["s7_mahkeme_json"])),
                    ("TUR 4 40 kör sayfa (tur/4/TUR_4_MAHKEME.md)", os.path.join(cikti, YH_DOSYA["tur4_mahkeme_ozet"]))):
        if os.path.exists(yol):
            o = json.load(open(yol, encoding="utf-8")); o = o.get("ozet", o)
            if o.get("atlandi"):
                s.append(f"- {ad}: ATLANDI ({o['atlandi']})."); continue
            s.append(f"- {ad}: mahkeme {o['mahkeme']} / {o['n']}; ÖNCEKİ BÖLGE DAHA UYGUN **{o['onceki_daha_uygun']}**; seçilen her kurala uyuyor "
                     f"{o['tam_puan']}; özellik dosyasıyla eşit {o['regresyon_esit']}; en sık eksik: "
                     + ", ".join(f"{k} {v}" for k, v in list(o["eksik_sikligi"].items())[:6]) + "; kurulamayan "
                     + (", ".join(f"No {h['no']}" for h in o["hata"]) or "yok") + "; sızıntı 0.")
        else:
            s.append(f"- {ad}: koşulmadı.")
    s += ["", "## YENİDEN ÜRETİM (satır dosyasından bağımsız komut; K11)", "", "```bash", "python - <<'EOF'", "import pandas as pd",
          "x = pd.read_csv('arastirma_cikti/yapi_hedef/olay_G6.csv.gz')",
          "for g, p, q in (('G2', 'ABD', '2016-22'), ('G1', 'AVR', '2024-26')):",
          "    a = x[x[g] & (x.pazar == p) & (x.donem == q) & x.h5.notna() & x.es_h5.notna()]; b = a[a.k_es_h5.notna()]",
          "    print(g, p, q, len(a), round(a.h5.mean(), 4), round(a.es_h5.mean(), 4), round(a.h5.sum() / a.es_h5.sum(), 4), len(b), round(b.h5.sum() / b.k_es_h5.sum(), 4))",
          "EOF", "```", ""]
    for g, p, q in (("G2", "ABD", "2016-22"), ("G1", "AVR", "2024-26")):
        h = [x for x in R["grup"][g]["hucre"] if x["pazar"] == p and x["donem"] == q][0]
        s.append(f"- grup6.json {g} {p} {q}: n {h.get('n')}, P olay {_sy(h.get('h5_p_olay'), 4)}, P eş {_sy(h.get('h5_p_ref'), 4)}, KAT5 {_sy(h.get('h5_kat'), 4)}, "
                 f"konum n {h.get('k_n')}, konum KAT5 {_sy(h.get('k_h5_kat'), 4)}.")
    hy = os.path.join(cikti, YH_DOSYA["hata6"]); hl = json.load(open(hy, encoding="utf-8")) if os.path.exists(hy) else []
    s += ["", yh_kontrol_tablosu(YH_KONTROL_6), "", "## HATA", ""] + ([f"- {x}" for x in hl] if hl else ["(yok)"])
    s += ["", "Colab: kod değişti -> çalışma zamanını yeniden başlat; `exec(open('YAPI_HEDEF.py').read())`.", ""]
    metin = "\n".join(s) + "\n"
    _yh_yaz(_yh_yol("rapor6", cikti), metin, "rapor 6")
    return metin


# ================================================================ ÇAKIŞMA KAPISI ve KOMUT
# ================================================================ 7. TUR — PUAN (YAPI_HEDEF_IS_TANIMI_7.md)
# Bütün Y1 bölgelerini F1-F29 ile puanlama; sızıntısız öğrenme (A: 2016-22 -> 2023-26, B: tersi, C: yürüyen yıllık); M1 lojistik + M2
# HistGradientBoosting SABİT ayarlarla (hiperparametre arama yok); 20 plasebo (y karıştırılmış); dilim tabloları; TUTAR; Y12 seçicisi.
YH_DOSYA.update({"onkayit7": "ON_KAYIT_7.md", "rapor7": "RAPOR_7.md", "puan7": "puan_Y1.csv.gz", "olay_y12": "olay_Y12.csv.gz",
                 "puan7_json": "puan7.json"})
YH_YOL["is_tanimi7"] = os.path.join(KOK_YH, "arastirma_cikti", "yapi_hedef", "YAPI_HEDEF_IS_TANIMI_7.md")
YH_YOL["parmak_p11"] = os.environ.get("YH_PARMAK_P11", os.path.join(KOK_YH, "arastirma_cikti", "goz_etiket", "parmak_Y1_p11.csv.gz"))
_YH_OZ7 = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19",
           "F20", "F21", "F22", "F22a", "F23", "F24", "F25", "F26", "F27", "F28", "F29"]
_YH_PZ7 = ["ABD", "AVR", "BIST"]
_YH_DILIM7 = ["tumu", "ust20", "ust10", "ust5", "alt20"]
_YH_DILIM7_AD = {"tumu": "tümü", "ust20": "üst %20", "ust10": "üst %10", "ust5": "üst %5", "alt20": "alt %20"}
_YH_OZ7_SART = {"F15": "Ş1", "F17": "Ş1", "F1": "Ş2", "F2": "Ş3", "F3": "Ş4", "F4": "Ş5", "F20": "Ş6", "F22": "Ş7", "F22a": "Ş7", "F23": "Ş7",
                "F18": "Ş8", "F24": "Ş9", "F25": "Ş9", "F26": "Ş9", "F27": "Ş9", "F28": "Ş9", "F29": "Ş9", "F14": "F14 büyük resim",
                "F16": "C8 kağıt hafızası"}

YH_ESIK7: Dict[str, Any] = {
    "surum": "7.0",
    "taban": "YH_ESIK (Y1-Y11c, 15 bar cetveli, karar ve etiket kuralı) AYNEN; yh_esik_sha() = ON_KAYIT_5.md YH_ESIK_SHA (kapı)",
    "satir": "olay_G6.csv.gz (26.663 Y1 olayı = olay_Y1.csv.gz satırları + konum eşi sütunları; h5 / es_h5 / st5 / es_st5 / n_es / tb_h5 / "
             "getiri / pl_h5 olay_Y1 ile eşit olmalı, değilse DUR); özellikler (pazar, sembol, tarih) ile 1:1 birleşir (eksik / fazla satır DUR)",
    "olcu_satir": "ölçülen satır = h5 ve es_h5 var (yh_hucre n'i); eğitim yalnız ölçülen satırlar; dilimler ölçülen sınama satırlarında",
    "ozellik": list(_YH_OZ7),
    "ozellik_not": "F1-F18 (goz_etiket/ozellik_Y1), F19 (parmak_Y1_p11), F20-F23 (s7; F21 fiyat seviyesidir: iş tanımı listesinde olduğu için "
                   "alındı, birimli), F24-F29 (s9); pazar, dönem, eş kovası (momentum x likidite) ÖZELLİK DEĞİL",
    "nan": "NaN -> eğitim kümesinin medyanı (eğitimde hepsi NaN ise 0); ayrıca NaN bayrağı sütunu (0/1) şu özellikler için (tam tabloda NaN'ı "
           "olanlar; getirisiz): F2, F14, F25, F27, F28, F29; başka bir özellikte NaN çıkarsa DUR",
    "nan_bayrak": ["F2", "F14", "F25", "F27", "F28", "F29"],
    "hedef": "h5 (15 geçerli barda kapanış +%5 stop'tan önce; 1. tur cetveli)",
    "hedef2": "y2 = h5 - es_h5 > 0 (eşini geçti mi; BİLGİ: yalnız A / B, birleşik, M1 / M2; AUC ve üst %20 payı)",
    "tarih": "satır tarihi = giris (giriş günü; dönem = giriş günü dönemi)",
    "yon": {"A": {"egitim": ["2016-22"], "sinama": ["2023", "2024-26"]}, "B": {"egitim": ["2023", "2024-26"], "sinama": ["2016-22"]},
            "C": {"ilk_sinama_yili": 2019, "son_sinama_yili": 2026,
                  "tanim": "her takvim yılı Y (giriş yılı, 2019..2026) için eğitim = giriş yılı < Y olan ölçülen satırlar, sınama = giriş yılı Y"}},
    "tampon_gun": 60,
    "tampon": "eğitim satırlarından sınama satırlarının (bütün olay satırları, ölçülemeyenler dahil) herhangi birine giriş tarihi farkı <= 60 "
              "takvim günü olanlar ATILIR (purge); SIZINTI KAPISI: her model eğitiminden önce min |giris_sinama - giris_egitim| > 60 gün, "
              "değilse YHHata (DURUR); hisse düzeyinde ek tampon yok (eş günlük)",
    "M1": {"ad": "lojistik regresyon", "olcek": "StandardScaler (eğitim kümesinde)", "C": 1.0, "ceza": "L2 (sklearn varsayılanı)",
           "solver": "lbfgs", "max_iter": 5000},
    "M2": {"ad": "HistGradientBoostingClassifier", "max_depth": 3, "learning_rate": 0.05, "max_iter": 300, "early_stopping": True,
           "validation_fraction": 0.2, "n_iter_no_change": 10, "scoring": "loss", "random_state": 7,
           "not": "erken durdurma doğrulaması eğitim içi %20 (sklearn tabakalı rastgele bölme, random_state 7)"},
    "modeller": ["M1", "M2"],
    "mod": {"birlesik": "ABD + AVR + BIST tek model", "pazar": "pazar başına ayrı model (eğitim ve sınama o pazarın satırları)"},
    "plasebo": {"tohum": 107, "tekrar": 20, "yuzde": 0.95,
                "tanim": "aynı model, aynı bölünme; eğitim y'si karıştırılır: rng = default_rng([107, tekrar, kat no, pazar no (birleşik 0; ABD 1, "
                         "AVR 2, BIST 3)]).permutation(y); sınama puanları aynı dilim kuralıyla; hücre x dilim başına 20 P(+5) değeri; plasebo "
                         "%95 = np.quantile(20 değer, 0,95) (doğrusal); gerçek > plasebo %95 -> 'plasebo üstü'"},
    "dilim": {"ust5": 0.05, "ust10": 0.10, "ust20": 0.20, "alt20": 0.20,
              "tanim": "dilim grubu içinde (A / B: pazar x sınama dönemi; C: pazar x sınama yılı, sonra dönem hücrelerine toplanır) ölçülen "
                       "satırların puanıyla: üst %q = puan >= np.quantile(puan, 1 - q); alt %20 = puan <= np.quantile(puan, 0,20); tümü = hücre"},
    "olcu": "dilim x hücre (pazar x sınama dönemi): yh_hucre (n, P(+5) olay, P eş = es_h5 ort, KAT5 = Σh5 / Σes_h5 ay kümeli bootstrap %95 "
            "(YH_ESIK kat: 2000, tohum 27), stop payı st5 olay / eş, iki yarı) + yh_hucre_konum (konum eşli KAT, F15 çeyreği); AUC (bilgi, tümü "
            "satırında), kalibrasyon 10 kutu (puan çeyrek kutuları: ort tahmin vs ort h5; bilgi)",
    "tutar": "hücre üst %20 diliminde: n >= 30 VE KAT5 %95 alt ucu > 1 VE üst %20 P(+5) > plasebo %95 VE stop payı (st5 olay) <= eş stop payı "
             "(es_st5 ort)",
    "etiket": "hücre durumu yh_durum (n < 30 ÖLÇÜLEMEDİ; TUTAR; n >= 1.000 ya da güç >= %80 -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ; güç "
              "tablosu 1. tur) -> yh_etiket (karar hücreleri ABD / AVR 2023 ve 2024-26) -> yh_etiket3 (3. tur: BAKILMIŞ hücreler (Y1 hücreleri "
              "önceki turlarda görüldü) -> en fazla EMARE; dış sınama ABD / AVR 2016-22; TERS iki yönlü). Hücreler: 2023 ve 2024-26 yön A'dan, "
              "2016-22 yön B'den (bağımsız sınama). ANA ETİKET = M2 birleşik; M1 birleşik, M1 / M2 pazar başı BİLGİ (çoklu karşılaştırma). Yön C "
              "BİLGİ (TUTAR bayrakları yazılır, etiket yok)",
    "tavan": "üst %5 diliminde P(+5) ('her seçilen yukarı çıksın' tavanı) her hücre için yazılır",
    "onem": {"model": "M2 birleşik, yön A ve B", "scoring": "roc_auc", "n_repeats": 5, "random_state": 7,
             "tanim": "sklearn permutation_importance sınama kümesinin ölçülen satırlarında (bilgi); Ş1-Ş9 / F14 / C8 eşlemesi yazılır"},
    "kalibrasyon_kutu": 10,
    "y12": {"model": "M2", "mod": "birlesik", "esik_yuzde": 0.80,
            "tanim": "Y12 PUAN seçicisi: eşik = eğitim kümesinin (purge sonrası, ölçülen) kendi puanlarının 0,80 çeyreği (eğitimden sabit); "
                     "A modeliyle 2023 ve 2024-26 sınama olayları (bütün olay satırları; n = ölçülen), B modeliyle 2016-22; aynı 15 bar cetveli; "
                     "İLERLEME tablosuna 'Y12 PUAN' satırı; TUR 6 havuzu adayı (karar Cemal'in)"},
    "mahkeme_bag": "BİLGİ: yön A M2 birleşik sınama satırlarında 12 kural puanı (yh_m_kurallar ile aynı kurallar: Ş1-Ş9, F14, C8 (F16 = 0) "
                   "özellik dosyalarından; C13 veriden _yh_c13 (son 250 bar, t'ye kadar)); üst %20 ortalaması vs alt %20 vs tümü, pazar başına",
    "tekrar_uretim": "RAPOR_7 'YENİDEN ÜRETİM': iki hücre (ABD 2023 üst %20 yön A M2 birleşik; AVR 2016-22 üst %20 yön B M2 birleşik) "
                     "puan_Y1.csv.gz + olay_G6.csv.gz'den bağımsız pandas koduyla (dilim yeniden, n / P olay / P eş) = puan7.json",
}

YH_KONTROL_7: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban = aynı satırın eşi (es_h5: aynı giriş günü, aynı momentum x likidite kovası, aynı d / hedef / takip / 15 bar; 1. tur "
                   "kodu, olay_G6 = olay_Y1 regresyonu DURUR) ve konum eşli KAT (F15 çeyreği); model plasebosu (y karıştırılmış, 20 tekrar, aynı "
                   "bölünme ve dilim kuralı) üst dilimin mekanik üstünlüğünü (model esnekliği / dilim seçimi) dışlar; dilim hücre içinde (pazar x "
                   "dönem) sıralanır: pazar / dönem taban farkı puana girmez; eş kovası özellik değil"),
    "K2": ("EVET", "özellikler mühürlü dosyalardan (F1-F29 yalnız [.., t]; önceki turlarda prefix denetimleri: ozellik_denetim, parmak_denetim_p11, "
                   "s7 / s9 denetim json); pazar / dönem özellik değil; NaN medyanı ve ölçekleme yalnız eğitim kümesinden; SIZINTI KAPISI her "
                   "eğitimde min |giris_sinama - giris_egitim| > 60 gün (hedef penceresi 15 bar <= 30 takvim günü + giriş), değilse DURUR (test: "
                   "ihlal eden bölünme durur); Y12 eşiği eğitim puanlarından; C13 yalnız t'ye kadar"),
    "K3": ("EVET", "satırlar 1. tur Y1 ölçümü (_yh_hazir: H > L, V > 0, kriz kesiği; 15 geçerli bar / 30 takvim günü); bu tur yeni bar ölçmez"),
    "K4": ("EVET", "Y1 olayları OC 60 gün tekil (1. tur); n = bağımsız olay; dilim hücrelerinde getiri ortalama + medyan (yh_hucre); yürüyen "
                   "yılda her olay bir kez sınanır"),
    "K5": ("EVET", "giriş t+1 açılışı (1. tur cetveli; olay_G6 = olay_Y1 regresyonu)"),
    "K6": ("EVET", "ölçüler oran / sayı; F21 fiyat seviyesi (birimli, pazara göre farklı para): iş tanımı F20-F23 dediği için alındı, ön kayıtta "
                   "yazılı; dilim pazar hücresi içinde; AVR yerel para"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; rapora yazılır"),
    "K8": ("EVET", "dilim x hücre n tabloda; n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; iki yön + yürüyen; karar hücreleri "
                   "BAKILMIŞ -> en fazla EMARE; ANA = M2 birleşik, öteki üç model / mod BİLGİ (çoklu karşılaştırma); küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "ON_KAYIT_7.md: YH_ESIK7_SHA (model ayarları, eşikler, tohumlar, tampon), YH_ESIK_SHA (= ON_KAYIT_5), kod / özellik / olay / "
                   "güç sha, sklearn sürümü, getirisiz sayımlar; yh_kapi7 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i "
                   "koşudan önce; hiperparametre arama yok; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız mühürlü özellik ve olay dosyaları (+ C13 için OHLCV)"),
    "K11": ("EVET", "puan_Y1.csv.gz (puan + dilim) + olay_Y12.csv.gz + puan7.json; RAPOR_7 'YENİDEN ÜRETİM' iki hücre bağımsız pandas koduyla; "
                    "İLERLEME satırları satır dosyalarından"),
    "K12": ("EVET", "etiket yalnız 3. tur kuralıyla (en fazla EMARE); AUC / kalibrasyon / önem / mahkeme bağı / y2 'bilgi'; 'iz değil' yazılmaz; "
                    "sayı ve yorum ayrı"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_ / YH_ / _YH_ önekli, 7 ekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, tur/* "
                    "içeriklerine dokunulmadı (git diff); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını "
                    "yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm"),
}


def yh_esik7_sha(E7: Optional[Dict[str, Any]] = None) -> str:
    return yh_esik_sha(YH_ESIK7 if E7 is None else E7)


def _yh_sklearn_surum() -> str:
    try:
        import sklearn
        return str(sklearn.__version__)
    except ImportError:
        raise YHHata("7. tur: scikit-learn kurulu değil (`pip install scikit-learn`) -> DURDU")


# ---------------------------------------------------------------- veri
def yh_veri7(cikti: Optional[str] = None, E7: Dict[str, Any] = YH_ESIK7) -> pd.DataFrame:
    """olay_G6.csv.gz (ölçüm sütunları; = olay_Y1 regresyonu) + F1-F29 (dört özellik dosyası, 1:1). Satır sırası (pazar, sembol, tarih)."""
    cikti = cikti or YH_YOL["cikti"]; k = ["pazar", "sembol", "tarih"]
    gy = os.path.join(cikti, YH_DOSYA["olay_g6"])
    if not os.path.exists(gy):
        raise YHHata(f"7. tur: {gy} yok (6. tur çıktısı) -> DURDU")
    J = json.load(open(_yh_yol("sonuc", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("sonuc", cikti)) else {}
    G = pd.read_csv(gy, parse_dates=["tarih", "giris"], dtype={"sembol": str, "donem": str})
    O = pd.read_csv(_yh_y1_satir_yolu(J, cikti), parse_dates=["tarih"], dtype={"sembol": str, "donem": str})
    if len(G) != len(O) or G.duplicated(k).any():
        raise YHHata(f"7. tur: olay_G6 ({len(G)}) ve olay_Y1 ({len(O)}) satır sayısı farklı ya da tekrar var -> DURDU")
    R = G[k + ["donem"]].merge(O[k + ["donem", "h5", "es_h5", "st5", "es_st5", "n_es", "tb_h5", "getiri", "pl_h5"]], on=k, how="left",
                               suffixes=("", "_y1"), validate="one_to_one")
    if R.h5.isna().sum() != G.h5.isna().sum() or (R.donem != R.donem_y1).any():
        raise YHHata("7. tur: olay_G6 anahtarları olay_Y1 ile aynı değil -> DURDU")
    Gs = G.set_index(k).loc[pd.MultiIndex.from_frame(R[k])].reset_index()
    for c in ("h5", "es_h5", "st5", "es_st5", "n_es", "tb_h5", "getiri", "pl_h5"):
        a, b = Gs[c].to_numpy(float), R[c].to_numpy(float)
        ok = (np.isnan(a) & np.isnan(b)) | (np.abs(a - b) <= 1e-9 * np.maximum(1.0, np.abs(b)))
        if not ok.all():
            raise YHHata(f"7. tur: olay_G6 {c} olay_Y1 ile eşit değil ({int((~ok).sum())} satır) -> DURDU")
    F = None
    for yol, kol in ((YH_YOL["ozellik"], _YH_OZ7[:18]), (YH_YOL["parmak_p11"], ["F19"]), (YH_YOL["ozellik_s7"], _Y10_OZ_S7),
                     (YH_YOL["ozellik_s9"], _Y11_OZ_S9)):
        if not os.path.exists(yol):
            raise YHHata(f"7. tur: özellik dosyası yok: {yol} -> DURDU")
        try:
            B = pd.read_csv(yol, parse_dates=["tarih"], dtype={"sembol": str})
        except Exception as ex:
            raise YHHata(f"7. tur: özellik dosyası okunamadı: {yol}: {ex}")
        eksik = [c for c in k + kol if c not in B.columns]
        if eksik or B.duplicated(k).any():
            raise YHHata(f"7. tur: {yol}: sütun yok {eksik} ya da aynı (pazar, sembol, tarih) iki kez -> DURDU")
        if F is None:
            F = B[k + kol]; continue
        F = F.merge(B[k + kol], on=k, how="outer", validate="one_to_one", indicator=True)
        if (F._merge != "both").any():
            raise YHHata(f"7. tur: {yol} anahtarları öteki özellik dosyalarından farklı ({int((F._merge != 'both').sum())} satır) -> DURDU")
        F = F.drop(columns="_merge")
    D = G.drop(columns=[c for c in G.columns if c in _YH_OZ7]).merge(F[k + _YH_OZ7], on=k, how="outer", validate="one_to_one", indicator=True)
    if (D._merge != "both").any():
        raise YHHata(f"7. tur: olay ve özellik anahtarları farklı ({int((D._merge != 'both').sum())} satır) -> DURDU")
    D = D.drop(columns="_merge").sort_values(k).reset_index(drop=True)
    Gk = G.set_index(k).loc[pd.MultiIndex.from_frame(D[k])]
    for c in ("F14", "F15", "F17"):
        if c in Gk.columns:
            a, b = Gk[c].to_numpy(float), D[c].to_numpy(float)
            if not ((np.isnan(a) & np.isnan(b)) | (np.abs(a - b) <= 1e-9 * np.maximum(1.0, np.abs(b)))).all():
                raise YHHata(f"7. tur: olay_G6 {c} özellik dosyasıyla eşit değil -> DURDU")
    nanli = [c for c in _YH_OZ7 if D[c].isna().any()]
    fazla = [c for c in nanli if c not in E7["nan_bayrak"]]
    if fazla:
        raise YHHata(f"7. tur: ön kayıtta NaN bayrağı olmayan özellikte NaN var: {fazla} -> DURDU")
    D["olcu"] = D.h5.notna() & D.es_h5.notna()
    D["yil"] = D.giris.dt.year.astype(int)
    return D


def _yh_matris7(Dtr: pd.DataFrame, Dte: pd.DataFrame, E7: Dict[str, Any] = YH_ESIK7) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """Özellik matrisi: medyan (eğitimden) + NaN bayrakları. Ad listesi döner."""
    oz = E7["ozellik"]; med = Dtr[oz].median()
    med = med.fillna(0.0)
    ad = list(oz) + [f"nan_{c}" for c in E7["nan_bayrak"]]

    def m(D: pd.DataFrame) -> np.ndarray:
        X = D[oz].astype(float)
        B = np.column_stack([D[c].isna().to_numpy(float) for c in E7["nan_bayrak"]]) if E7["nan_bayrak"] else np.zeros((len(D), 0))
        return np.column_stack([X.fillna(med).to_numpy(float), B])
    return m(Dtr), m(Dte), ad


def _yh_yakin_gun(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """b'nin her elemanı için a'daki en yakın tarihe uzaklık (gün). a boşsa inf."""
    a = np.sort(np.asarray(a, "datetime64[D]").astype(np.int64)); b = np.asarray(b, "datetime64[D]").astype(np.int64)
    if not len(a):
        return np.full(len(b), np.inf)
    i = np.searchsorted(a, b)
    sol = np.abs(b - a[np.clip(i - 1, 0, len(a) - 1)]); sag = np.abs(a[np.clip(i, 0, len(a) - 1)] - b)
    return np.minimum(sol, sag).astype(float)


def yh_sizinti_kapisi(g_egitim: Any, g_sinama: Any, tampon: int = 60) -> int:
    """SIZINTI KAPISI: min |giris_sinama - giris_egitim| > tampon gün olmalı; değilse YHHata (koşu DURUR). En küçük uzaklığı döner."""
    a = np.asarray(pd.to_datetime(pd.Series(g_egitim)).to_numpy(), "datetime64[D]")
    b = np.asarray(pd.to_datetime(pd.Series(g_sinama)).to_numpy(), "datetime64[D]")
    if not len(a) or not len(b):
        raise YHHata("SIZINTI KAPISI: eğitim ya da sınama kümesi boş -> DURDU")
    mn = float(np.min(_yh_yakin_gun(a, b)))
    if not mn > tampon:
        raise YHHata(f"SIZINTI KAPISI: sınama satırı eğitim satırına {mn:.0f} gün yakın (tampon {tampon}) -> DURDU")
    return int(mn)


def yh_tampon7(g_egitim: Any, g_sinama: Any, tampon: int = 60) -> np.ndarray:
    """Eğitimde tutulacak satırlar: her sınama tarihine uzaklığı > tampon gün olanlar (purge)."""
    a = np.asarray(pd.to_datetime(pd.Series(g_sinama)).to_numpy(), "datetime64[D]")
    b = np.asarray(pd.to_datetime(pd.Series(g_egitim)).to_numpy(), "datetime64[D]")
    return _yh_yakin_gun(a, b) > tampon


def yh_bolunme7(D: pd.DataFrame, yon: str, E7: Dict[str, Any] = YH_ESIK7) -> List[Dict[str, Any]]:
    """Katlar: {ad, kat, te (bool, bütün sınama olay satırları), tr_ham (dönem kuralı, ölçülen), tr (purge sonrası), purge, grup (dilim grubu sütunu)}."""
    tp = int(E7["tampon_gun"]); out = []
    if yon in ("A", "B"):
        Y_ = E7["yon"][yon]
        katlar = [(yon, D.donem.isin(Y_["sinama"]).to_numpy(), D.donem.isin(Y_["egitim"]).to_numpy())]
        grup = "donem"
    elif yon == "C":
        C_ = E7["yon"]["C"]; katlar = []
        for y in range(int(C_["ilk_sinama_yili"]), int(C_["son_sinama_yili"]) + 1):
            katlar.append((f"C{y}", (D.yil == y).to_numpy(), (D.yil < y).to_numpy()))
        grup = "yil"
    else:
        raise YHHata(f"yön bilinmiyor: {yon}")
    for no, (ad, te, trh) in enumerate(katlar, start=1):
        trh = trh & D.olcu.to_numpy()
        keep = np.zeros(len(D), bool)
        if te.any() and trh.any():
            keep[trh] = yh_tampon7(D.giris[trh], D.giris[te], tp)
        out.append({"ad": ad, "kat": no, "te": te, "tr_ham": trh, "tr": keep, "purge": int(trh.sum() - keep.sum()), "grup": grup})
    return out


# ---------------------------------------------------------------- model
def yh_model7(ad: str, E7: Dict[str, Any] = YH_ESIK7):
    """Sabit ayarlı model (hiperparametre arama yok)."""
    _yh_sklearn_surum()
    if ad == "M1":
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        M = E7["M1"]
        return Pipeline([("olcek", StandardScaler()), ("lr", LogisticRegression(C=float(M["C"]), solver=M["solver"], max_iter=int(M["max_iter"])))])
    if ad == "M2":
        from sklearn.ensemble import HistGradientBoostingClassifier
        M = E7["M2"]
        return HistGradientBoostingClassifier(max_depth=int(M["max_depth"]), learning_rate=float(M["learning_rate"]), max_iter=int(M["max_iter"]),
                                              early_stopping=bool(M["early_stopping"]), validation_fraction=float(M["validation_fraction"]),
                                              n_iter_no_change=int(M["n_iter_no_change"]), scoring=M["scoring"], random_state=int(M["random_state"]))
    raise YHHata(f"model bilinmiyor: {ad}")


def yh_plasebo_y7(y: np.ndarray, tekrar: int, kat: int, pazar_no: int, E7: Dict[str, Any] = YH_ESIK7) -> np.ndarray:
    """Plasebo hedefi: eğitim y'sinin karıştırılmışı (aynı çokluk); tohum [107, tekrar, kat, pazar no]."""
    return np.random.default_rng([int(E7["plasebo"]["tohum"]), int(tekrar), int(kat), int(pazar_no)]).permutation(np.asarray(y))


def yh_egit_tahmin7(D: pd.DataFrame, tr: np.ndarray, te: np.ndarray, model: str, y_sutun: str = "h5", plasebo: Optional[Tuple[int, int, int]] = None,
                    E7: Dict[str, Any] = YH_ESIK7, don_model: bool = False) -> Dict[str, Any]:
    """Bir eğitim: SIZINTI KAPISI -> matris (eğitim medyanı) -> fit -> sınama ve eğitim puanları (P(y=1))."""
    from sklearn.exceptions import ConvergenceWarning
    tm = yh_sizinti_kapisi(D.giris[tr], D.giris[te], int(E7["tampon_gun"]))
    Dtr, Dte = D[tr], D[te]
    Xtr, Xte, ad = _yh_matris7(Dtr, Dte, E7)
    if y_sutun == "y2":
        y = (Dtr.h5.to_numpy(float) - Dtr.es_h5.to_numpy(float) > 0).astype(int)
    else:
        y = (Dtr[y_sutun].to_numpy(float) > 0.5).astype(int)
    if plasebo is not None:
        y = yh_plasebo_y7(y, *plasebo, E7=E7)
    if len(np.unique(y)) < 2:
        raise YHHata("7. tur: eğitim hedefinde tek sınıf -> DURDU")
    M = yh_model7(model, E7)
    with warnings.catch_warnings(record=True) as W:
        warnings.simplefilter("always", ConvergenceWarning)
        M.fit(Xtr, y)
    out = {"p_te": M.predict_proba(Xte)[:, 1], "p_tr": M.predict_proba(Xtr)[:, 1], "min_gun": tm, "n_tr": int(tr.sum()), "n_te": int(te.sum()),
           "yakinsama_uyari": int(sum(issubclass(w.category, ConvergenceWarning) for w in W)), "ad": ad}
    if model == "M2":
        out["n_iter"] = int(M.n_iter_)
    if don_model:
        out["model"] = M; out["Xte"] = Xte
    return out


# ---------------------------------------------------------------- dilim
def yh_dilim7(puan: np.ndarray, grup: np.ndarray, E7: Dict[str, Any] = YH_ESIK7) -> Dict[str, np.ndarray]:
    """Grup içi dilim maskeleri (yalnız verilen satırlar; NaN puan hiçbir dilime girmez, 'tumu' hariç)."""
    p = np.asarray(puan, float); g = np.asarray(grup); Dl = E7["dilim"]
    out = {k: np.zeros(len(p), bool) for k in _YH_DILIM7}
    out["tumu"][:] = True
    for gv in pd.unique(g):
        m = (g == gv) & np.isfinite(p)
        if not m.any():
            continue
        x = p[m]
        for k in ("ust5", "ust10", "ust20"):
            out[k][m] = x >= np.quantile(x, 1.0 - float(Dl[k]))
        out["alt20"][m] = x <= np.quantile(x, float(Dl["alt20"]))
    return out


def _yh_dilim_etiket7(Dm: Dict[str, np.ndarray]) -> np.ndarray:
    e = np.full(len(Dm["tumu"]), "orta", dtype=object)
    e[Dm["alt20"]] = "alt20"; e[Dm["ust20"]] = "ust20"; e[Dm["ust10"]] = "ust10"; e[Dm["ust5"]] = "ust5"
    return e


def yh_plasebo_pay7(h5: np.ndarray, PL: np.ndarray, grup: np.ndarray, hucre: np.ndarray, E7: Dict[str, Any] = YH_ESIK7) -> Dict[str, Dict[str, List[float]]]:
    """Plasebo puanları (tekrar x satır) -> hücre x dilim başına P(+5) listesi."""
    out: Dict[str, Dict[str, List[float]]] = {}
    for r in range(PL.shape[0]):
        Dm = yh_dilim7(PL[r], grup, E7)
        for hv in pd.unique(hucre):
            hm = hucre == hv
            for k in _YH_DILIM7:
                m = hm & Dm[k]
                out.setdefault(str(hv), {}).setdefault(k, []).append(float(h5[m].mean()) if m.any() else np.nan)
    return out


def _yh_auc(y: np.ndarray, p: np.ndarray) -> float:
    from sklearn.metrics import roc_auc_score
    y = np.asarray(y, float); p = np.asarray(p, float); g = np.isfinite(y) & np.isfinite(p)
    return float(roc_auc_score(y[g], p[g])) if g.sum() > 1 and len(np.unique(y[g])) == 2 else np.nan


def yh_kalibrasyon7(y: np.ndarray, p: np.ndarray, kutu: int = 10) -> List[Dict[str, Any]]:
    q = pd.qcut(pd.Series(p), kutu, labels=False, duplicates="drop")
    out = []
    for b in sorted(q.dropna().unique()):
        m = (q == b).to_numpy()
        out.append({"kutu": int(b) + 1, "n": int(m.sum()), "tahmin": float(np.mean(p[m])), "gercek": float(np.mean(y[m]))})
    return out


def yh_tutar7(h: Dict[str, Any], pl95: float, Y: Dict[str, Any] = YH_ESIK) -> Dict[str, bool]:
    """Üst %20 hücre şartları (YH_ESIK7 'tutar')."""
    f = lambda x: x is not None and np.isfinite(x)  # noqa: E731
    s = {"s_n": bool(int(h.get("n", 0) or 0) >= Y["karar"]["n_esik"]),
         "s_kat": bool(f(h.get("h5_alt")) and h["h5_alt"] > 1),
         "s_plasebo7": bool(f(h.get("h5_p_olay")) and f(pl95) and h["h5_p_olay"] > pl95),
         "s_stop7": bool(f(h.get("st5_p_olay")) and f(h.get("st5_p_ref")) and h["st5_p_olay"] <= h["st5_p_ref"])}
    s["tutar"] = bool(all(s.values()))
    return s


def yh_dilim_tablo7(D: pd.DataFrame, puan: np.ndarray, PL: Optional[np.ndarray], grup_sutun: str, E7: Dict[str, Any] = YH_ESIK7,
                    Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Sınama satırları (puan sonlu ve ölçülen) -> hücre (pazar x dönem) x dilim tablosu + plasebo + AUC + kalibrasyon."""
    m = np.isfinite(puan) & D.olcu.to_numpy()
    X = D[m].copy(); p = puan[m]; X["puan"] = p
    grup = (X.pazar + "|" + X[grup_sutun].astype(str)).to_numpy(); hucre = (X.pazar + "|" + X.donem.astype(str)).to_numpy()
    Dm = yh_dilim7(p, grup, E7)
    h5 = X.h5.to_numpy(float)
    PLp = yh_plasebo_pay7(h5, PL[:, m], grup, hucre, E7) if PL is not None and PL.shape[0] else {}
    satir = []
    for hv in sorted(pd.unique(hucre)):
        pz, dn = hv.split("|"); hm = hucre == hv
        for k in _YH_DILIM7:
            sm = hm & Dm[k]; xs = X[sm]
            h = yh_hucre(xs, Y); h.update(yh_hucre_konum(xs, Y))
            r = {"pazar": pz, "donem": dn, "dilim": k, **{a: h.get(a) for a in ("n", "ay", "h5_p_olay", "h5_p_ref", "h5_kat", "h5_alt", "h5_ust",
                                                                                  "st5_p_olay", "st5_p_ref", "k_h5_kat", "k_h5_alt", "k_h5_ust",
                                                                                  "yari1_kat5", "yari2_kat5", "getiri_ort", "getiri_med", "pl_h5_alt")}}
            pl = PLp.get(hv, {}).get(k, [])
            plf = np.array([v for v in pl if np.isfinite(v)], float)
            r["pl_ort"] = float(plf.mean()) if len(plf) else np.nan
            r["pl95"] = float(np.quantile(plf, float(E7["plasebo"]["yuzde"]))) if len(plf) else np.nan
            r["pl_max"] = float(plf.max()) if len(plf) else np.nan
            r["pl_ustu"] = bool(np.isfinite(r["pl95"]) and np.isfinite(r["h5_p_olay"] if r["h5_p_olay"] is not None else np.nan)
                                and r["h5_p_olay"] > r["pl95"])
            if k == "tumu":
                r["auc"] = _yh_auc(xs.h5.to_numpy(float), xs.puan.to_numpy(float))
            if k == "ust20":
                r.update(yh_tutar7(h, r["pl95"], Y)); r["ters"] = yh_ters(h, Y); r["_h"] = h
            satir.append(r)
    return {"satir": satir, "auc": _yh_auc(h5, p), "kalibrasyon": yh_kalibrasyon7(h5, p, int(E7["kalibrasyon_kutu"])),
            "dilim_etiket": pd.Series(_yh_dilim_etiket7(Dm), index=X.index)}


def yh_etiket7(satir_A: List[Dict[str, Any]], satir_B: List[Dict[str, Any]], tablo: Optional[Dict[str, Any]], Y: Dict[str, Any] = YH_ESIK) -> Dict[str, Any]:
    """Hücreler: 2023 / 2024-26 yön A'nın üst %20'si, 2016-22 yön B'nin üst %20'si -> yh_durum + yh_etiket + yh_etiket3."""
    K = _yh_kural3(Y); H_ = []; dur = {}
    for r in [x for x in satir_A if x["dilim"] == "ust20" and x["donem"] in ("2023", "2024-26")] + \
             [x for x in satir_B if x["dilim"] == "ust20" and x["donem"] == "2016-22"]:
        h = dict(r["_h"]); h["tutar"] = bool(r["tutar"])
        durum, g = yh_durum(h, 1, tablo, Y)
        dur[(r["pazar"], r["donem"])] = durum
        H_.append({"pazar": r["pazar"], "donem": r["donem"], "tutar": bool(r["tutar"]), "ters": bool(r["ters"]), "durum": durum, "guc": g,
                   "bakilmis": [r["pazar"], r["donem"]] in K["bakilmis"], "dis_sinama": [r["pazar"], r["donem"]] in K["dis_sinama"]})
    kural = yh_etiket(dur, Y)
    e3 = yh_etiket3(H_, kural, Y)
    return {"etiket_kural": kural, **e3, "hucre": H_}


# ---------------------------------------------------------------- mahkeme bağı (C13 + 12 kural; getirisiz)
def yh_c13_7(D: pd.DataFrame, veri: Optional[str] = None, E6: Dict[str, Any] = YH_ESIK6) -> np.ndarray:
    """Her satır için C13 ölçüsü (_yh_c13, yalnız [t-250, t] geçerli barlar). Veri yoksa / tarih geçerli bar değilse NaN."""
    out = np.full(len(D), np.nan); gun = int(E6["mahkeme"]["c13_gun"])
    for pz in _YH_PZ7:
        idx = np.where(D.pazar.to_numpy() == pz)[0]
        if not len(idx):
            continue
        try:
            Vd = OC.oc_veri(pz, klasor=veri or YH_YOL["veri"])
        except Exception as ex:      # veri yoksa bilgi satırı atlanır
            yhlog.warning("C13: %s verisi okunamadı (%s); NaN", pz, ex); continue
        sub = D.iloc[idx]
        for s, grp in sub.groupby("sembol"):
            if s not in Vd["V"]:
                continue
            d = _yh_hazir(Vd["V"][s])
            H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
            pos = d.index.get_indexer(pd.DatetimeIndex(grp.tarih))
            for j, i in zip(grp.index, pos):
                if i >= 0:
                    out[int(j)] = _yh_c13(H, L, C, int(i), gun)
    return out


def yh_kural12_7(D: pd.DataFrame, c13: np.ndarray, E6: Dict[str, Any] = YH_ESIK6, Y: Dict[str, Any] = YH_ESIK) -> pd.DataFrame:
    """12 kural ✓ (yh_m_kurallar ile aynı eşikler; vektör) + puan."""
    S = yh_s9_sartlar(D, Y)
    R = pd.DataFrame({k: np.asarray(S[k], bool) for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S9", "S7", "S8", "F14")}, index=D.index)
    f16 = D.F16.to_numpy(float)
    R["C8"] = np.isfinite(f16) & (f16 == 0)
    R["C13"] = np.isfinite(c13) & (c13 <= float(E6["mahkeme"]["c13_carp"]))
    R = R[_YH_KURAL6]; R["puan12"] = R.sum(axis=1).astype(int)
    return R


# ---------------------------------------------------------------- sayım / ön kayıt / kapı
def yh_sayim7(D: pd.DataFrame, E7: Dict[str, Any] = YH_ESIK7) -> Dict[str, Any]:
    """GETİRİSİZ sayımlar: kat başına eğitim (ölçülen) / purge / sınama olay sayısı, en küçük uzaklık; pazar başına. Hedef değeri okunmaz."""
    out: Dict[str, Any] = {"satir": int(len(D)), "olcu": int(D.olcu.sum()), "nan_oran": {c: float(D[c].isna().mean()) for c in E7["ozellik"]},
                           "kat": []}
    for yon in ("A", "B", "C"):
        for k in yh_bolunme7(D, yon, E7):
            r = {"yon": yon, "ad": k["ad"], "egitim_ham": int(k["tr_ham"].sum()), "purge": k["purge"], "egitim": int(k["tr"].sum()),
                 "sinama_olay": int(k["te"].sum()), "sinama_olcu": int((k["te"] & D.olcu.to_numpy()).sum())}
            r["min_gun"] = int(np.min(_yh_yakin_gun(D.giris[k["tr"]].to_numpy(), D.giris[k["te"]].to_numpy()))) if k["tr"].any() and k["te"].any() else None
            for pz in _YH_PZ7:
                pm = (D.pazar == pz).to_numpy()
                r[f"egitim_{pz}"] = int((k["tr"] & pm).sum()); r[f"sinama_{pz}"] = int((k["te"] & pm & D.olcu.to_numpy()).sum())
            out["kat"].append(r)
    return out


def yh_sha_simdi7(cikti: Optional[str] = None) -> Dict[str, str]:
    cikti = cikti or YH_YOL["cikti"]
    out = {"esik7": yh_esik7_sha(), "esik": yh_esik_sha(), "kod": _yh_sha_dosya(YH_YOL["kod"]), "guc": _yh_sha_dosya(_yh_yol("guc_json", cikti))}
    for ad, yol in (("ozellik", YH_YOL["ozellik"]), ("parmak", YH_YOL["parmak_p11"]), ("s7ozellik", YH_YOL["ozellik_s7"]),
                    ("s9ozellik", YH_YOL["ozellik_s9"]), ("g6olay", os.path.join(cikti, YH_DOSYA["olay_g6"]))):
        if not os.path.exists(yol):
            raise YHHata(f"7. tur: dosya yok: {yol}")
        out[ad] = _yh_sha_dosya(yol)
    sy = _yh_yol("sonuc", cikti); J = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
    out["y1olay"] = _yh_sha_dosya(_yh_y1_satir_yolu(J, cikti))
    return out


_YH_KAPI_DESEN7 = {"esik7": r"YH_ESIK7_SHA:\s*`([0-9a-f]{64})`", "esik": r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"YH_KOD_SHA:\s*`([0-9a-f]{64})`",
                   "guc": r"GUC_SHA:\s*`([0-9a-f]{64})`", "ozellik": r"OZELLIK_SHA:\s*`([0-9a-f]{64})`", "parmak": r"PARMAK_SHA:\s*`([0-9a-f]{64})`",
                   "s7ozellik": r"S7_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "s9ozellik": r"S9_OZELLIK_SHA:\s*`([0-9a-f]{64})`",
                   "g6olay": r"G6_OLAY_SHA:\s*`([0-9a-f]{64})`", "y1olay": r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`"}


def _yh_is_tanimi7_bolum(no: int, yol: Optional[str] = None) -> str:
    yol = yol or YH_YOL["is_tanimi7"]
    if not os.path.exists(yol):
        raise YHHata(f"7. tur iş tanımı yok: {yol}")
    m = re.search(rf"(?ms)^## {no}\. [^\n]*\n(.*?)(?=^## |\Z)", open(yol, encoding="utf-8").read())
    if not m or not m.group(1).strip():
        raise YHHata(f"iş tanımı 7'de §{no} bulunamadı")
    return m.group(1).strip()


def yh_onkayit7_metni(say: Dict[str, Any], sha: Dict[str, str], skl: str, git6: Dict[str, str], git_is: Dict[str, str],
                      E7: Dict[str, Any] = YH_ESIK7) -> str:
    s = ["# YAPI_HEDEF — ÖN KAYIT 7 (7. tur: PUAN — bütün Y1 bölgelerini puanlama, sızıntısız öğrenme, Y12)", "",
         f"{YH_SURUM}; 7. tur eklendi (YAPI_HEDEF_IS_TANIMI_7.md)", "",
         f"- YH_ESIK7_SHA: `{sha['esik7']}` (7. tur: özellikler, NaN, yönler, tampon, model ayarları, plasebo, dilim, TUTAR, etiket, Y12)",
         f"- YH_ESIK_SHA: `{sha['esik']}` (= ON_KAYIT_5.md YH_ESIK_SHA: Y1-Y11c, cetvel, karar ve etiket kuralı AYNEN)",
         f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)", f"- GUC_SHA: `{sha['guc']}` (guc_tablosu.json, 1. tur)",
         f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)",
         f"- PARMAK_SHA: `{sha['parmak']}` (goz_etiket/parmak_Y1_p11.csv.gz; F19)",
         f"- S7_OZELLIK_SHA: `{sha['s7ozellik']}` (ozellik_Y1_s7.csv.gz; F20-F23)", f"- S9_OZELLIK_SHA: `{sha['s9ozellik']}` (ozellik_Y1_s9.csv.gz; F24-F29)",
         f"- G6_OLAY_SHA: `{sha['g6olay']}` (olay_G6.csv.gz; ölçüm satırları + konum eşi)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (olay_Y1.csv.gz; regresyon)",
         f"- SKLEARN: `{skl}` (numpy {np.__version__}, pandas {pd.__version__})"]
    if git6:
        s.append(f"- ON_KAYIT_6: git {git6.get('commit', '?')[:10]}, {git6.get('zaman', '?')}")
    if git_is:
        s.append(f"- IS_TANIMI_7: git {git_is.get('commit', '?')[:10]}, {git_is.get('zaman', '?')}")
    s += [f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
          "Bu dosya 7. tur koşusundan ÖNCE yazıldı. Alt ajan hiçbir model eğitmedi, hiçbir puan / dilim / hedef payı / eş oranı / plasebo / AUC "
          "hesaplamadı ve okumadı: aşağıdaki sayılar yalnız satır kimlikleri, giriş tarihleri, ölçülebilirlik bayrağı ve özellik NaN oranlarıdır "
          "(getirisiz). `python YAPI_HEDEF.py puan7` bu dosyanın kontrol listesini, sha'larını, sklearn sürümünü ve git kaydını denetler; biri "
          "tutmazsa durur. Model ayarları ve eşikler sonuç görüldükten sonra değişmez (hiperparametre arama yok).", "",
          "## İŞ TANIMI 7 §1-§4 (AYNEN)", ""]
    for no in (1, 2, 3, 4):
        s += [f"### §{no}", _yh_is_tanimi7_bolum(no), ""]
    s += ["## TANIMLAR, MODEL AYARLARI ve EŞİKLER (YH_ESIK7; uygulama kararları dahil)", "",
          f"- SATIRLAR: {E7['satir']}; {E7['olcu_satir']}.", f"- ÖZELLİKLER ({len(E7['ozellik'])}): {', '.join(E7['ozellik'])}; {E7['ozellik_not']}.",
          f"- NaN: {E7['nan']}.", f"- HEDEF: {E7['hedef']}; ikincil: {E7['hedef2']}.", f"- TARİH: {E7['tarih']}.",
          f"- YÖN A: eğitim {', '.join(E7['yon']['A']['egitim'])} -> sınama {', '.join(E7['yon']['A']['sinama'])}; YÖN B: eğitim "
          f"{', '.join(E7['yon']['B']['egitim'])} -> sınama {', '.join(E7['yon']['B']['sinama'])}; YÖN C: {E7['yon']['C']['tanim']}.",
          f"- TAMPON ({E7['tampon_gun']} gün): {E7['tampon']}.",
          f"- M1: {json.dumps(E7['M1'], ensure_ascii=False, sort_keys=True)}.", f"- M2: {json.dumps(E7['M2'], ensure_ascii=False, sort_keys=True)}.",
          f"- MODLAR: birleşik = {E7['mod']['birlesik']}; pazar = {E7['mod']['pazar']}.",
          f"- PLASEBO: {E7['plasebo']['tanim']}.", f"- DİLİM: {E7['dilim']['tanim']}.", f"- ÖLÇÜ: {E7['olcu']}.", f"- TUTAR: {E7['tutar']}.",
          f"- ETİKET: {E7['etiket']}.", f"- TAVAN: {E7['tavan']}.", f"- ÖNEM: {E7['onem']['tanim']} (n_repeats {E7['onem']['n_repeats']}, "
          f"random_state {E7['onem']['random_state']}, {E7['onem']['scoring']}; {E7['onem']['model']}).",
          f"- Y12: {E7['y12']['tanim']}.", f"- MAHKEME BAĞI: {E7['mahkeme_bag']}.", f"- YENİDEN ÜRETİM: {E7['tekrar_uretim']}.", "",
          "UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden önce yazıldı): (1) §3 dilimleri sınama hücresi içinde sıralanır (değerlendirme); "
          "§4 Y12 eşiği eğitim kümesinden sabitlenir (karar kuralı); (2) tampon eğitim tarafında uygulanır (sınama hücreleri eksiksiz kalır); B'de "
          "eğitim sınamadan SONRA olduğu için tampon simetriktir (en yakın tarih uzaklığı); (3) 'plasebo %95'in üstünde' = gerçek üst %20 P(+5) > "
          "20 plasebo değerinin 0,95 çeyreği; (4) 'stop payı eşten büyük değil' = st5 olay <= es_st5 ort (1. tur yh_hucre'nin kesin küçük "
          "şartından farklı: iş tanımı sözü); (5) ANA etiket M2 birleşik (Y12 de bu modelden); öteki üç model / mod bilgi; (6) yürüyen (C) dilimleri "
          "pazar x yıl içinde, dönem hücrelerine toplanarak raporlanır (2016-22 hücresi C'de yalnız 2019-22); (7) F21 fiyat seviyesi listede olduğu "
          "için alındı (birimli; K6 notu).", "",
          "## GETİRİSİZ SAYIMLAR (satır kimliği + giriş tarihi + ölçülebilirlik; hedef değeri okunmadı)", "",
          f"Satır {say['satir']}, ölçülen {say['olcu']}. Özellik NaN oranları: " +
          ", ".join(f"{c} {_yz(v)}" for c, v in say["nan_oran"].items() if v > 0) + " (öteki özelliklerde NaN yok).", "",
          "| Yön / kat | eğitim (ölçülen, ham) | purge | eğitim | sınama olay | sınama ölçülen | min uzaklık (gün) | eğitim ABD / AVR / BIST | "
          "sınama ölçülen ABD / AVR / BIST |", "|---|---|---|---|---|---|---|---|---|"]
    for r in say["kat"]:
        s.append(f"| {r['ad']} | {r['egitim_ham']} | {r['purge']} | {r['egitim']} | {r['sinama_olay']} | {r['sinama_olcu']} | {r['min_gun']} | "
                 f"{r['egitim_ABD']} / {r['egitim_AVR']} / {r['egitim_BIST']} | {r['sinama_ABD']} / {r['sinama_AVR']} / {r['sinama_BIST']} |")
    s += ["", f"Eğitim sayısı (model x mod x kat x (1 gerçek + {E7['plasebo']['tekrar']} plasebo)): "
          f"{2 * (len(say['kat'])) * (1 + 3) * (1 + int(E7['plasebo']['tekrar']))}.", "", yh_kontrol_tablosu(YH_KONTROL_7), ""]
    return "\n".join(s) + "\n"


def yh_onkayit7_yaz(cikti: Optional[str] = None, uzerine: bool = False, git: bool = True) -> str:
    """ON_KAYIT_7.md (getirisiz). 6. tur ölçülmüş olmalı (olay_G6), 7. tur ölçülmemiş; YH_ESIK = ON_KAYIT_5 mührü."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit7", cikti)
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"ön kayıt 7 zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"ön kayıt 7 var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(os.path.join(cikti, YH_DOSYA["puan7_json"])):
        raise YHHata("puan7.json var: 7. tur ölçülmüş; ön kayıt ölçümden sonra yazılamaz")
    _yh_esik_tur5_kontrol(cikti)
    skl = _yh_sklearn_surum()
    D = yh_veri7(cikti)
    say = yh_sayim7(D)
    sha = yh_sha_simdi7(cikti)
    git6 = {}
    if git:
        try:
            git6 = _yh_git(_yh_yol("onkayit6", cikti))
        except YHHata:
            git6 = {}
    try:
        git_is = _yh_git(YH_YOL["is_tanimi7"]) if git else {}
    except YHHata:
        git_is = {}
    _yh_yaz(yol, yh_onkayit7_metni(say, sha, skl, git6, git_is), "ön kayıt 7")
    return yol


def yh_kapi7(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """7. tur koşu kapısı: ON_KAYIT_7.md kontrol listesi + sha'lar + sklearn sürümü + YH_ESIK = ON_KAYIT_5 mührü + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = _yh_yol("onkayit7", cikti)
    if not os.path.exists(yol):
        raise YHHata(f"ön kayıt 7 yok: {yol}")
    metin = open(yol, encoding="utf-8").read()
    _yh_esik_tur5_kontrol(cikti)
    out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in {**_YH_KAPI_DESEN7, "zaman": _YH_KAPI_DESEN["zaman"], "skl": r"SKLEARN:\s*`([^`]+)`"}.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"ön kayıt 7'de {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = yh_sha_simdi7(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    if bul["skl"] != _yh_sklearn_surum():
        raise YHHata(f"sklearn sürümü ön kayıttan farklı ({bul['skl']} -> {_yh_sklearn_surum()}) -> DURDU")
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]; out["sklearn"] = bul["skl"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"])
    yhlog.info("yh_kapi7 AÇIK (%s)", yol)
    return out


# ---------------------------------------------------------------- koşu
def yh_puan_hesap7(D: pd.DataFrame, E7: Dict[str, Any] = YH_ESIK7, yonler: Tuple[str, ...] = ("A", "B", "C"),
                   modeller: Tuple[str, ...] = ("M1", "M2"), modlar: Tuple[str, ...] = ("birlesik", "pazar"), tekrar: Optional[int] = None,
                   y2: bool = True) -> Dict[str, Any]:
    """Bütün eğitimler. Döner: puan[(yon, mod, model)] (satır dizisi, sınama dışı NaN), plasebo[(…)] (tekrar x satır), kat bilgisi, Y12 eşikleri,
    y2 puanları."""
    T = int(E7["plasebo"]["tekrar"] if tekrar is None else tekrar); n = len(D)
    P: Dict[Tuple[str, str, str], np.ndarray] = {}; PL: Dict[Tuple[str, str, str], np.ndarray] = {}; bilgi: List[Dict[str, Any]] = []
    esik12: Dict[str, float] = {}; P2: Dict[Tuple[str, str], np.ndarray] = {}
    pz_no = {"ABD": 1, "AVR": 2, "BIST": 3}
    for yon in yonler:
        katlar = yh_bolunme7(D, yon, E7)
        for mod in modlar:
            for model in modeller:
                key = (yon, mod, model); P[key] = np.full(n, np.nan); PL[key] = np.full((T, n), np.nan)
                for k in katlar:
                    parca = [("birlesik", 0, np.ones(n, bool))] if mod == "birlesik" else [(p, pz_no[p], (D.pazar == p).to_numpy()) for p in _YH_PZ7]
                    for pad, pno, pm in parca:
                        tr, te = k["tr"] & pm, k["te"] & pm
                        if not tr.any() or not te.any():
                            continue
                        R = yh_egit_tahmin7(D, tr, te, model, "h5", None, E7)
                        P[key][te] = R["p_te"]
                        bilgi.append({"yon": yon, "mod": mod, "model": model, "kat": k["ad"], "parca": pad, "n_tr": R["n_tr"], "n_te": R["n_te"],
                                      "min_gun": R["min_gun"], "n_iter": R.get("n_iter"), "yakinsama_uyari": R["yakinsama_uyari"]})
                        if yon in ("A", "B") and mod == E7["y12"]["mod"] and model == E7["y12"]["model"]:
                            esik12[yon] = float(np.quantile(R["p_tr"], float(E7["y12"]["esik_yuzde"])))
                        for r in range(T):
                            Rp = yh_egit_tahmin7(D, tr, te, model, "h5", (r, k["kat"], pno), E7)
                            PL[key][r, te] = Rp["p_te"]
                        if y2 and yon in ("A", "B") and mod == "birlesik":
                            P2.setdefault((yon, model), np.full(n, np.nan))[te] = yh_egit_tahmin7(D, tr, te, model, "y2", None, E7)["p_te"]
                yhlog.info("7. tur: %s %s %s bitti", yon, mod, model)
    return {"puan": P, "plasebo": PL, "bilgi": bilgi, "esik12": esik12, "puan_y2": P2, "tekrar": T}


def yh_onem7(D: pd.DataFrame, yon: str, E7: Dict[str, Any] = YH_ESIK7) -> List[Dict[str, Any]]:
    """M2 birleşik permütasyon önemi (sınama kümesinin ölçülen satırları; roc_auc; bilgi)."""
    from sklearn.inspection import permutation_importance
    k = yh_bolunme7(D, yon, E7)[0]; te = k["te"] & D.olcu.to_numpy()
    R = yh_egit_tahmin7(D, k["tr"], te, "M2", "h5", None, E7, don_model=True)
    y = (D.h5[te].to_numpy(float) > 0.5).astype(int)
    O = E7["onem"]
    I = permutation_importance(R["model"], R["Xte"], y, scoring=O["scoring"], n_repeats=int(O["n_repeats"]), random_state=int(O["random_state"]))
    out = [{"ozellik": a, "onem": float(I.importances_mean[i]), "std": float(I.importances_std[i]),
            "sart": _YH_OZ7_SART.get(a.replace("nan_", ""), "-") + (" (NaN bayrağı)" if a.startswith("nan_") else "")} for i, a in enumerate(R["ad"])]
    return sorted(out, key=lambda r: -r["onem"])


def _yh_satir_temiz7(S: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [{k: v for k, v in r.items() if k != "_h"} for r in S]


def yh_kos7(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True, E7: Dict[str, Any] = YH_ESIK7,
            Y: Dict[str, Any] = YH_ESIK, tekrar: Optional[int] = None, c13: bool = True) -> Dict[str, Any]:
    """7. tur: kapı -> veri -> bütün eğitimler (gerçek + plasebo) -> dilim tabloları, etiket, Y12, önem, mahkeme bağı -> puan_Y1.csv.gz,
    olay_Y12.csv.gz, puan7.json, sonuc.json 'puan7' özeti, RAPOR_7.md. Bir kez koşar."""
    t0 = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or YH_YOL["cikti"]; jy = os.path.join(cikti, YH_DOSYA["puan7_json"])
    if os.path.exists(jy):
        raise YHHata(f"7. tur zaten koştu ({jy}); ikinci koşu yok")
    kapi = yh_kapi7(cikti, git=git, kontrol=kontrol)
    D = yh_veri7(cikti, E7)
    gt = json.load(open(_yh_yol("guc_json", cikti), encoding="utf-8")) if os.path.exists(_yh_yol("guc_json", cikti)) else None
    H = yh_puan_hesap7(D, E7, tekrar=tekrar)
    grup = {"A": "donem", "B": "donem", "C": "yil"}
    TB: Dict[str, Any] = {}; dil: Dict[str, pd.Series] = {}
    for key, p in H["puan"].items():
        R = yh_dilim_tablo7(D, p, H["plasebo"][key], grup[key[0]], E7, Y)
        TB["|".join(key)] = R
        if key[1] == "birlesik":
            dil["|".join(key)] = R["dilim_etiket"]
    ET = {}
    for mod in ("birlesik", "pazar"):
        for model in ("M1", "M2"):
            ET[f"{mod}|{model}"] = yh_etiket7(TB[f"A|{mod}|{model}"]["satir"], TB[f"B|{mod}|{model}"]["satir"], gt, Y)
    # Y12
    pA, pB = H["puan"][("A", "birlesik", "M2")], H["puan"][("B", "birlesik", "M2")]
    selA = np.isfinite(pA) & (pA >= H["esik12"]["A"]); selB = np.isfinite(pB) & (pB >= H["esik12"]["B"])
    Y12 = D[selA | selB].copy(); Y12["deneme"] = "Y12"
    Y12["yon"] = np.where(selA[selA | selB], "A", "B"); Y12["puan"] = np.where(selA[selA | selB], pA[selA | selB], pB[selA | selB])
    Y12["esik"] = np.where(Y12.yon == "A", H["esik12"]["A"], H["esik12"]["B"])
    y12h = []
    for pz in _YH_PZ7:
        for dn in _YH_DONEM3:
            x = Y12[(Y12.pazar == pz) & (Y12.donem == dn)]
            h = yh_hucre(x, Y); h.update(yh_hucre_konum(x, Y))
            hd = (D.pazar == pz) & (D.donem == dn) & D.olcu
            y12h.append({"pazar": pz, "donem": dn, "olay": int(len(x)), "sinama_olcu": int(hd.sum()),
                         "pay_secilen": float(len(x[x.olcu]) / hd.sum()) if hd.sum() else np.nan,
                         **{a: h.get(a) for a in ("n", "h5_p_olay", "h5_p_ref", "h5_kat", "h5_alt", "h5_ust", "st5_p_olay", "st5_p_ref", "k_h5_kat",
                                                  "k_h5_alt", "tutar", "getiri_ort", "getiri_med")}})
    # y2 (bilgi)
    Y2 = {}
    for (yon, model), p in H["puan_y2"].items():
        m = np.isfinite(p) & D.olcu.to_numpy(); X = D[m]; y2v = (X.h5.to_numpy(float) - X.es_h5.to_numpy(float) > 0).astype(float)
        Dm = yh_dilim7(p[m], (X.pazar + "|" + X.donem).to_numpy(), E7)
        Y2[f"{yon}|{model}"] = {"auc": _yh_auc(y2v, p[m]), "tumu_pay": float(y2v.mean()), "ust20_pay": float(y2v[Dm["ust20"]].mean()),
                                "ust20_fark": float((X.h5.to_numpy(float) - X.es_h5.to_numpy(float))[Dm["ust20"]].mean()),
                                "tumu_fark": float((X.h5.to_numpy(float) - X.es_h5.to_numpy(float)).mean())}
    ONEM = {y: yh_onem7(D, y, E7) for y in ("A", "B")}
    # mahkeme bağı
    MB: Dict[str, Any] = {"yapildi": False}
    if c13:
        cv = yh_c13_7(D, veri)
        K12 = yh_kural12_7(D, cv)
        de = dil["A|birlesik|M2"]; MB = {"yapildi": True, "c13_nan": int(np.isnan(cv).sum()), "pazar": {}}
        for pz in _YH_PZ7 + ["hepsi"]:
            idx = de.index if pz == "hepsi" else de.index[D.loc[de.index, "pazar"] == pz]
            e = de.loc[idx]; R_ = {}
            for nm, m in (("ust20", e.isin(["ust20", "ust10", "ust5"])), ("alt20", e == "alt20"), ("tumu", pd.Series(True, index=e.index))):
                ii = e.index[m.to_numpy()]
                R_[nm] = {"n": int(len(ii)), "puan_ort": float(K12.loc[ii, "puan12"].mean()) if len(ii) else np.nan,
                          "kural": {k: float(K12.loc[ii, k].mean()) if len(ii) else np.nan for k in _YH_KURAL6}}
            MB["pazar"][pz] = R_
        D["puan12"] = K12["puan12"]; D["c13"] = cv
    # dosyalar
    pu = D[["pazar", "sembol", "tarih", "giris", "donem"]].copy()
    for yon in ("A", "B", "C"):
        pu[f"puan_{yon}"] = H["puan"][(yon, "birlesik", "M2")]; pu[f"puan_{yon}_M1"] = H["puan"][(yon, "birlesik", "M1")]
        pu[f"dilim_{yon}"] = ""
        de = dil[f"{yon}|birlesik|M2"]; pu.loc[de.index, f"dilim_{yon}"] = de.to_numpy()
    if "puan12" in D.columns:
        pu["puan12"] = D["puan12"]
    pu["tarih"] = pu.tarih.dt.strftime("%Y-%m-%d"); pu["giris"] = pu.giris.dt.strftime("%Y-%m-%d")
    py = os.path.join(cikti, YH_DOSYA["puan7"]); pu.to_csv(py, index=False, compression="gzip", float_format="%.6g")
    oy = os.path.join(cikti, YH_DOSYA["olay_y12"]); Y12w = Y12.copy()
    Y12w["tarih"] = Y12w.tarih.dt.strftime("%Y-%m-%d"); Y12w["giris"] = Y12w.giris.dt.strftime("%Y-%m-%d")
    Y12w.drop(columns=[c for c in _YH_OZ7 if c in Y12w.columns]).to_csv(oy, index=False, compression="gzip")
    J7 = {"surum": YH_SURUM, "tur": 7, "zaman_utc": _yh_simdi(), "kapi": kapi, "esik7_sha": yh_esik7_sha(E7), "sklearn": _yh_sklearn_surum(),
          "tekrar": H["tekrar"], "bilgi": H["bilgi"], "esik12": H["esik12"],
          "tablo": {k: {"satir": _yh_satir_temiz7(v["satir"]), "auc": v["auc"], "kalibrasyon": v["kalibrasyon"]} for k, v in TB.items()},
          "etiket": ET, "y12": y12h, "y12_n": int(len(Y12)), "y2": Y2, "onem": ONEM, "mahkeme_bag": MB,
          "dosya": {"puan": os.path.relpath(py, KOK_YH), "olay_y12": os.path.relpath(oy, KOK_YH)}, "sure_sn": round(time.time() - t0, 1)}
    _yh_yaz(jy, json.dumps(J7, ensure_ascii=False, indent=1, default=_yh_json), "puan7")
    sy = _yh_yol("sonuc", cikti)
    if os.path.exists(sy):
        S_ = json.load(open(sy, encoding="utf-8"))
        S_["puan7"] = {"dosya": os.path.relpath(jy, KOK_YH), "ana_etiket": ET["birlesik|M2"]["etiket"], "etiket_kural": ET["birlesik|M2"]["etiket_kural"],
                       "y12_n": int(len(Y12)), "esik12": H["esik12"], "esik7_sha": yh_esik7_sha(E7)}
        _yh_yaz(sy, json.dumps(S_, ensure_ascii=False, indent=1, default=_yh_json), "sonuç")
    rapor = yh_rapor7(cikti)
    yhlog.info("7. tur bitti (%.0f sn)", time.time() - t0)
    return {"json": J7, "rapor": rapor}


# ---------------------------------------------------------------- rapor
def _yh_kat_metin7(r: Dict[str, Any]) -> str:
    if not r or not r.get("n"):
        return "0"
    return (f"{r['n']}: {_yz(r['h5_p_olay'])} / {_yz(r['h5_p_ref'])}, KAT {_sy(r['h5_kat'])} [{_sy(r['h5_alt'])}; {_sy(r['h5_ust'])}]")


def yh_yeniden_uret7(cikti: str, yon: str, pazar: str, donem: str) -> Dict[str, Any]:
    """BAĞIMSIZ yeniden üretim (pandas): puan_Y1.csv.gz (M2 birleşik puanı) + olay_G6.csv.gz -> üst %20 dilimi n / P olay / P eş."""
    pu = pd.read_csv(os.path.join(cikti, YH_DOSYA["puan7"]), dtype={"sembol": str})
    g6 = pd.read_csv(os.path.join(cikti, YH_DOSYA["olay_g6"]), usecols=["pazar", "sembol", "tarih", "h5", "es_h5"], dtype={"sembol": str})
    x = pu.merge(g6, on=["pazar", "sembol", "tarih"], how="inner")
    x = x[(x.pazar == pazar) & (x.donem.astype(str) == donem) & x[f"puan_{yon}"].notna() & x.h5.notna() & x.es_h5.notna()]
    esik = x[f"puan_{yon}"].quantile(0.80)          # pandas doğrusal çeyrek (np.quantile ile aynı varsayılan)
    u = x[x[f"puan_{yon}"] >= esik]
    return {"n": int(len(u)), "p_olay": float(u.h5.mean()), "p_es": float(u.es_h5.mean()), "dilim_dosya_n": int((x[f"dilim_{yon}"].isin(["ust20", "ust10", "ust5"])).sum())}


def yh_rapor7(cikti: Optional[str] = None, E7: Dict[str, Any] = YH_ESIK7, Y: Dict[str, Any] = YH_ESIK) -> str:
    cikti = cikti or YH_YOL["cikti"]; jy = os.path.join(cikti, YH_DOSYA["puan7_json"])
    if not os.path.exists(jy):
        raise YHHata("puan7.json yok: önce `python YAPI_HEDEF.py puan7`")
    J = json.load(open(jy, encoding="utf-8")); TB = J["tablo"]
    hucreler = [(p, q) for p in _YH_PZ7 for q in _YH_DONEM3]

    def bul(key: str, p: str, q: str, d: str) -> Dict[str, Any]:
        for r in TB.get(key, {}).get("satir", []):
            if r["pazar"] == p and r["donem"] == q and r["dilim"] == d:
                return r
        return {}
    E_ = J["etiket"]["birlesik|M2"]
    s = ["# YAPI_HEDEF — RAPOR 7 (PUAN: bütün Y1 bölgelerini puanlama, sızıntısız öğrenme, Y12)", "",
         f"{J['surum']}; koşu {J['zaman_utc']}; sklearn {J['sklearn']}; plasebo tekrar {J['tekrar']}; süre {J['sure_sn']} sn", "",
         f"Ön kayıt: ON_KAYIT_7.md (zaman {J['kapi'].get('onkayit_zaman')}; git {J['kapi'].get('git_onkayit', {}).get('commit', '-')[:10]}); "
         f"YH_ESIK7_SHA `{J['esik7_sha']}`.", "",
         "## 1. ANA ETİKET (M2 birleşik; hücreler: 2023 / 2024-26 yön A, 2016-22 yön B)", "",
         f"- ETİKET: **{E_['etiket']}** (hücre kuralı: {E_['etiket_kural']}); {E_['ters_etiket']}", "",
         "| Hücre | durum | TUTAR | BAKILMIŞ | DIŞ SINAMA |", "|---|---|---|---|---|"]
    for h in E_["hucre"]:
        s.append(f"| {h['pazar']} {h['donem']} | {h['durum']} | {'evet' if h['tutar'] else 'hayır'} | {'evet' if h['bakilmis'] else '-'} | "
                 f"{'evet' if h['dis_sinama'] else '-'} |")
    s += ["", "BİLGİ etiketleri: " + "; ".join(f"{k.replace('|', ' ')}: {v['etiket']}" for k, v in J["etiket"].items() if k != "birlesik|M2"), "",
          "## 2. ÖZET (M2 birleşik): P(+5) olay / eş, KAT5 [%95]", "",
          "| Yön | Hücre | tümü | üst %20 | üst %10 | üst %5 (tavan) | alt %20 | plasebo %95 (üst %20) | TUTAR |", "|---|---|---|---|---|---|---|---|---|"]
    for yon in ("A", "B", "C"):
        key = f"{yon}|birlesik|M2"
        for p, q in hucreler:
            u = bul(key, p, q, "ust20")
            if not u:
                continue
            s.append(f"| {yon} | {p} {q} | {_yh_kat_metin7(bul(key, p, q, 'tumu'))} | {_yh_kat_metin7(u)} | {_yh_kat_metin7(bul(key, p, q, 'ust10'))} | "
                     f"{_yh_kat_metin7(bul(key, p, q, 'ust5'))} | {_yh_kat_metin7(bul(key, p, q, 'alt20'))} | {_yz(u.get('pl95'))} | "
                     f"{'TUTAR' if u.get('tutar') else '-'} |")
    s += ["", "## 3. DİLİM TABLOLARI (bütün modeller; üst %20 satırı; n: P olay / P eş, KAT5 [%95]; stop olay / eş; konum KAT; plasebo ort / %95; şartlar)", ""]
    for key in sorted(TB):
        s += [f"### {key.replace('|', ' ')} (AUC sınama {_sy(TB[key]['auc'], 3)})", "",
              "| Hücre | üst %20 | stop olay / eş | konum KAT [%95] | plasebo ort / %95 | n>=30 | KAT>1 | plasebo | stop | TUTAR | AUC hücre |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for p, q in hucreler:
            u = bul(key, p, q, "ust20"); t_ = bul(key, p, q, "tumu")
            if not u:
                continue
            e = lambda b: "✓" if b else "✗"  # noqa: E731
            s.append(f"| {p} {q} | {_yh_kat_metin7(u)} | {_yz(u.get('st5_p_olay'))} / {_yz(u.get('st5_p_ref'))} | {_sy(u.get('k_h5_kat'))} "
                     f"[{_sy(u.get('k_h5_alt'))}; {_sy(u.get('k_h5_ust'))}] | {_yz(u.get('pl_ort'))} / {_yz(u.get('pl95'))} | {e(u.get('s_n'))} | "
                     f"{e(u.get('s_kat'))} | {e(u.get('s_plasebo7'))} | {e(u.get('s_stop7'))} | {'TUTAR' if u.get('tutar') else '-'} | {_sy(t_.get('auc'), 3)} |")
        s.append("")
    s += [f"## 4. PLASEBO (M2 birleşik; dilim başına gerçek P(+5) vs {J['tekrar']} plasebo: ort / %95 / en büyük)", "",
          "| Yön | Hücre | üst %20 gerçek / pl ort / %95 / max | üst %10 | üst %5 |", "|---|---|---|---|---|"]
    for yon in ("A", "B", "C"):
        key = f"{yon}|birlesik|M2"
        for p, q in hucreler:
            cell = []
            for d in ("ust20", "ust10", "ust5"):
                r = bul(key, p, q, d)
                cell.append(f"{_yz(r.get('h5_p_olay'))} / {_yz(r.get('pl_ort'))} / {_yz(r.get('pl95'))} / {_yz(r.get('pl_max'))}" if r else "-")
            if any(c != "-" for c in cell):
                s.append(f"| {yon} | {p} {q} | " + " | ".join(cell) + " |")
    s += ["", "## 5. AUC ve KALİBRASYON (bilgi)", "", "| Model | AUC (sınama, bütün) |", "|---|---|"]
    for key in sorted(TB):
        s.append(f"| {key.replace('|', ' ')} | {_sy(TB[key]['auc'], 3)} |")
    for key in ("A|birlesik|M1", "A|birlesik|M2", "B|birlesik|M1", "B|birlesik|M2"):
        if key in TB:
            s += ["", f"Kalibrasyon {key.replace('|', ' ')}: " + "; ".join(f"{k['kutu']}: {_yz(k['tahmin'])} -> {_yz(k['gercek'])} (n {k['n']})"
                                                                         for k in TB[key]["kalibrasyon"])]
    s += ["", "## 6. ÖZELLİK ÖNEMİ (M2 birleşik, permütasyon, sınama AUC düşüşü; bilgi)", ""]
    for yon in ("A", "B"):
        s += [f"Yön {yon} (ilk 8):", "", "| Sıra | Özellik | önem (AUC düşüşü) | std | Cemal kuralı |", "|---|---|---|---|---|"]
        for i, r in enumerate(J["onem"][yon][:8], start=1):
            s.append(f"| {i} | {r['ozellik']} | {_sy(r['onem'], 4)} | {_sy(r['std'], 4)} | {r['sart']} |")
        s.append("")
    s += ["## 7. Y12 PUAN SEÇİCİSİ (M2 birleşik; eşik eğitimden: üst %20 eğitim puanı)", "",
          f"Eşik A {_sy(J['esik12'].get('A'), 4)}, B {_sy(J['esik12'].get('B'), 4)}; seçilen olay {J['y12_n']} (olay_Y12.csv.gz).", "",
          "| Hücre | yön | seçilen olay | ölçülen n | seçilen pay | P olay / P eş | KAT5 [%95] | stop olay / eş | konum KAT [%95] | getiri ort / med |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in J["y12"]:
        s.append(f"| {r['pazar']} {r['donem']} | {'B' if r['donem'] == '2016-22' else 'A'} | {r['olay']} | {r.get('n', 0)} | {_yz(r.get('pay_secilen'))} | "
                 f"{_yz(r.get('h5_p_olay'))} / {_yz(r.get('h5_p_ref'))} | {_sy(r.get('h5_kat'))} [{_sy(r.get('h5_alt'))}; {_sy(r.get('h5_ust'))}] | "
                 f"{_yz(r.get('st5_p_olay'))} / {_yz(r.get('st5_p_ref'))} | {_sy(r.get('k_h5_kat'))} [{_sy(r.get('k_h5_alt'))}] | "
                 f"{_yz(r.get('getiri_ort'))} / {_yz(r.get('getiri_med'))} |")
    sy = _yh_yol("sonuc", cikti); S_ = json.load(open(sy, encoding="utf-8")) if os.path.exists(sy) else {}
    IL = S_.get("ilerleme5", {}).get("deneme", {})
    s += ["", "## 8. İLERLEME (hücre başına n: P(+5) olay / eş; Y12 PUAN: 2016-22 yön B, 2023 / 2024-26 yön A)", "",
          "| Deneme | " + " | ".join(f"{p} {q}" for p, q in hucreler) + " |", "|---|" + "---|" * len(hucreler)]
    for d, R in IL.items():
        if isinstance(R, dict) and "yok" not in R:
            s.append(f"| {d} | " + " | ".join((f"{R[f'{p} {q}']['n']}: {_yz(R[f'{p} {q}']['p_olay'])} / {_yz(R[f'{p} {q}']['p_es'])}"
                                               if R.get(f"{p} {q}", {}).get("n") else "0") for p, q in hucreler) + " |")
    y12k = {(r["pazar"], r["donem"]): r for r in J["y12"]}
    s.append("| Y12 PUAN | " + " | ".join((f"{y12k[(p, q)]['n']}: {_yz(y12k[(p, q)]['h5_p_olay'])} / {_yz(y12k[(p, q)]['h5_p_ref'])}"
                                            if y12k.get((p, q), {}).get("n") else "0") for p, q in hucreler) + " |")
    MB = J["mahkeme_bag"]
    s += ["", "## 9. MAHKEME BAĞI (bilgi; yön A M2 birleşik sınama; 12 kural puanı ortalaması)", ""]
    if MB.get("yapildi"):
        s += [f"C13 hesaplanamayan satır: {MB['c13_nan']}.", "", "| Pazar | üst %20 n / puan | alt %20 n / puan | tümü n / puan |", "|---|---|---|---|"]
        for pz, R in MB["pazar"].items():
            s.append(f"| {pz} | {R['ust20']['n']} / {_sy(R['ust20']['puan_ort'])} | {R['alt20']['n']} / {_sy(R['alt20']['puan_ort'])} | "
                     f"{R['tumu']['n']} / {_sy(R['tumu']['puan_ort'])} |")
        R = MB["pazar"]["hepsi"]
        s += ["", "Kural ✓ oranı (hepsi) üst %20 / alt %20: " + "; ".join(f"{_YH_KURAL6_AD[k]} {_yz(R['ust20']['kural'][k])} / {_yz(R['alt20']['kural'][k])}"
                                                                          for k in _YH_KURAL6)]
    else:
        s.append("yapılmadı (veri yok)")
    s += ["", "## 10. İKİNCİL HEDEF y2 = h5 - es_h5 > 0 (bilgi; birleşik)", "", "| Yön model | AUC | y2 payı tümü / üst %20 | ort (h5 - es_h5) tümü / üst %20 |",
          "|---|---|---|---|"]
    for k, v in sorted(J["y2"].items()):
        s.append(f"| {k.replace('|', ' ')} | {_sy(v['auc'], 3)} | {_yz(v['tumu_pay'])} / {_yz(v['ust20_pay'])} | {_yz(v['tumu_fark'])} / {_yz(v['ust20_fark'])} |")
    s += ["", "## 11. SIZINTI KAPISI ve EĞİTİMLER", ""]
    bi = pd.DataFrame(J["bilgi"])
    if len(bi):
        s += [f"Eğitim (gerçek) sayısı {len(bi)}; her eğitimde min |giris_sinama - giris_egitim| en küçüğü {int(bi.min_gun.min())} gün (> "
              f"{E7['tampon_gun']}: kapı GEÇTİ); M1 yakınsama uyarısı {int(bi.yakinsama_uyari.sum())}; M2 ağaç sayısı (erken durdurma) medyan "
              f"{_sy(bi.n_iter.dropna().median(), 0)}, aralık {_sy(bi.n_iter.dropna().min(), 0)}-{_sy(bi.n_iter.dropna().max(), 0)}.", ""]
    s += ["## 12. YENİDEN ÜRETİM (bağımsız pandas kodu: puan_Y1.csv.gz + olay_G6.csv.gz)", ""]
    for yon, p, q in (("A", "ABD", "2023"), ("B", "AVR", "2016-22")):
        try:
            Rr = yh_yeniden_uret7(cikti, yon, p, q); u = bul(f"{yon}|birlesik|M2", p, q, "ust20")
            ok = Rr["n"] == u.get("n") and abs(Rr["p_olay"] - u["h5_p_olay"]) < 1e-9 and abs(Rr["p_es"] - u["h5_p_ref"]) < 1e-9
            s.append(f"- {yon} {p} {q} üst %20: yeniden n {Rr['n']}, P {_yz(Rr['p_olay'], 2)} / eş {_yz(Rr['p_es'], 2)}; puan7.json n {u.get('n')}, "
                     f"P {_yz(u.get('h5_p_olay'), 2)} / eş {_yz(u.get('h5_p_ref'), 2)}; dosyadaki dilim etiketi n {Rr['dilim_dosya_n']} -> "
                     f"{'TUTTU' if ok and Rr['dilim_dosya_n'] == Rr['n'] else 'TUTMADI'}")
        except Exception as ex:  # rapor yazılır, sorun görünür kalır
            s.append(f"- {yon} {p} {q}: yeniden üretim hatası: {ex}")
    s += ["", "## 13. VERİ SINIRLARI", "", "- Evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı.",
          "- F21 fiyat seviyesidir (pazara göre farklı para); iş tanımı listesinde olduğu için alındı.",
          "- Karar hücreleri (ABD / AVR 2023, 2024-26) Y1 hücresi olarak önceki turlarda görüldü (BAKILMIŞ): etiket en fazla EMARE.",
          "- Fon krizi kesiği 31.08.2026 (1. tur cetveli).", "",
          "## 14. COLAB", "", "YAPI_HEDEF.py değişti: Colab'da 'çalışma zamanını yeniden başlat'. Koşu: `python YAPI_HEDEF.py puan7` (bir kez), rapor: "
          "`python YAPI_HEDEF.py rapor7`.", ""]
    oy = _yh_yol("onkayit7", cikti)
    if os.path.exists(oy):
        m = re.search(r"(?ms)^## KONTROL LİSTESİ.*?(?=^## |\Z)", open(oy, encoding="utf-8").read())
        if m:
            s += [m.group(0).strip(), ""]
    hy = os.path.join(cikti, "hata7.json")
    H_ = json.load(open(hy, encoding="utf-8")) if os.path.exists(hy) else []
    s += ["## HATA", ""] + ([f"- {h}" for h in H_] if H_ else ["(yok)"]) + [""]
    metin = "\n".join(s) + "\n"
    _yh_yaz(_yh_yol("rapor7", cikti), metin, "rapor 7")
    return metin



# ================================================================ DEVİR 1 (2026-11-19): web / hakem adayları F30-F42 süzgeç karnesi
# Kodlayıcı alt ajan; iş tanımı: workflow DEVİR 1 (W1-W6 web adayları, E1 ÖNCEKİ BÖLGE süzgeci CD15, E2 TOPARLANMA HIZI CD17).
# Yalnız ekleme: Y1-Y12 eşikleri (YH_ESIK / YH_ESIK6 / YH_ESIK7) ve önceki tur fonksiyonları değişmez (regresyon kapısı yh_d1_kapi).
_YH_D1_OZ = ["F30", "F31", "F32", "F33", "F34", "F35", "F36", "F37", "F38", "F39", "F40", "F41", "F42"]
_YH_D1_BAR = ["F30", "F31", "F32", "F33", "F34", "F35", "F36", "F37", "F38", "F41", "F42"]
_YH_D1_MAH = ["F39", "F40"]
YH_D1_DOSYA = {"ozellik": "ozellik_Y1_d1.csv.gz", "denetim": "ozellik_Y1_d1_denetim.json", "esik": "devir1_esik.json",
               "onkayit": "DEVIR_1_ON_KAYIT.md", "sonuc": "devir1_sonuc.json", "rapor": "DEVIR_1_RAPOR.md", "hata": "devir1_hata.json"}

YH_ESIK_D1: Dict[str, Any] = {
    "surum": "D1.0",
    "taban": "YH_ESIK (Y1-Y11c; ON_KAYIT_5 mührü), YH_ESIK6 (ON_KAYIT_6), YH_ESIK7 (Y12; ON_KAYIT_7) AYNEN; ölçü satırları olay_Y1.csv.gz (sha)",
    "pencere": {"onceki": 60, "onceki_min": 40, "bolge_min_cs": 10, "bolge_min": 15, "er_kisa": 10, "mdd_gun": 30, "hiz_gun": 250,
                "hiz_hedef": 0.10, "hiz_hedef2": 0.05, "hiz_esik": 15},
    "ozellik": {
        "F30": "W1 Corwin-Schultz spread oranı: ort S (bölge [sol, t-1] içi iki-gün çiftleri, >= 10 çift) / ort S (önceki pencere [sol-60, sol-1] "
               "içi çiftler, >= 40 bar); S = 2(e^a - 1)/(1 + e^a), a = (sqrt(2b) - sqrt(b))/k - sqrt(g/k), k = 3 - 2 sqrt2, b = ln(H_j/L_j)^2 + "
               "ln(H_j+1/L_j+1)^2, g = ln(max H / min L)^2; gece düzeltmesi: C_j < L_j+1 ise j+1'in H ve L'si (L_j+1 - C_j) kadar aşağı, C_j > "
               "H_j+1 ise (C_j - H_j+1) kadar yukarı; S < 0 -> 0; önceki ort S = 0 ise NaN",
        "F31": "W2 B gün-içi birikim = prod(C_j/O_j) - 1, j = [sol, t-1] (>= 15 bar)",
        "F32": "W2 D = A - B; A gece birikim = prod(O_j/C_j-1) - 1, j = [sol, t-1]",
        "F33": "W3 Amihud oranı: ort(|C_j/C_j-1 - 1| / (C_j V_j)) bölge [sol, t-1] (>= 15) / aynısı önceki [sol-60, sol-1] (>= 40); önceki ort 0 "
               "ise NaN (günlük oranların ortalaması)",
        "F34": "W4 sıfır getiri payı farkı: pay(C_j == C_j-1) bölge [sol, t-1] (>= 15) - aynısı önceki [sol-60, sol-1] (>= 40)",
        "F35": "W5 ER_bölge = |C_t-1 - C_sol-1| / sum |C_k - C_k-1|, k = sol..t-1 (n = bölge boyu, >= 15); payda 0 -> NaN",
        "F36": "W5 ER_10 = |C_t-1 - C_t-11| / sum |C_k - C_k-1|, k = t-10..t-1; payda 0 -> NaN",
        "F37": "W6 R/MDD: P = ln C, pencere [t-30, t-1]; MDD = max(koşan tepe - P); tau* = ilk en derin nokta; R = P_t-1 - P_tau*; MDD = 0 -> NaN",
        "F38": "W6 R (log toparlanma, aynı pencere; bilgi)",
        "F39": "E1 mahkeme BAYRAK: 1 = yh_mahkeme_hisse 'ÖNCEKİ BÖLGE DAHA UYGUN' (max aday puanı > seçilen puanı), 0 = değil; mahkeme hatası NaN",
        "F40": "E1 PUAN_FARK = puan(seçilen) - max puan(aday); aday yoksa NaN (bilgi)",
        "F41": "E2 HIZ: j* = ilk argmin Low [t-250, sol-1]; HIZ = ilk m (j* < m <= sol-1) Close_m >= Low_j* x 1,10 için m - j* (geçerli bar); "
               "ulaşmadı = inf (UL); t'den önce 250 geçerli bar yoksa ya da sol <= t-250 ise NaN",
        "F42": "E2 HIZ +%5 varyantı (bilgi; süzgece girmez)"},
    "ceyrek": {"alt": 0.25, "ust": 0.75, "yon1": ["2016-22"], "yon2": ["2023", "2024-26"],
               "tanim": "kaynakta eşik olmayan adaylar için q25 / q75 PAZAR içinde, bütün Y1 olaylarının (KOL-A tabanı) sonlu özellik değerlerinden "
                        "(getirisiz; inf ve NaN dışarıda); YÖN 1 eşiği eğitim 2016-22 olaylarından, YÖN 2 (ters yürüyen sınama) eşiği 2023-26 "
                        "olaylarından; KOL-B aynı eşikleri kullanır; eşikler devir1_esik.json'da ön kayıtta mühürlü"},
    "aday": {
        "W1":   {"kaynak": "W1", "yon": "ana", "kural": [["F30", "<", 1.0], ["F30", "<=", "q25"]], "ad": "W1 CS spread daraldı (oran < 1 ve alt çeyrek)"},
        "W1t":  {"kaynak": "W1", "yon": "ters", "kural": [["F30", ">=", "q75"]], "ad": "W1 ters: spread genişledi (üst çeyrek)"},
        "W2":   {"kaynak": "W2", "yon": "ana", "kural": [["F31", ">", 0.0], ["F31", ">=", "q75"]], "ad": "W2 gün-içi birikim B > 0 ve üst çeyrek"},
        "W2t":  {"kaynak": "W2", "yon": "ters", "kural": [["F31", "<=", "q25"]], "ad": "W2 ters: B alt çeyrek"},
        "W2D":  {"kaynak": "W2", "yon": "ana", "kural": [["F32", ">=", "q75"]], "ad": "W2 D = gece - gün-içi üst çeyrek"},
        "W2Dt": {"kaynak": "W2", "yon": "ters", "kural": [["F32", "<=", "q25"]], "ad": "W2 ters: D alt çeyrek"},
        "W3":   {"kaynak": "W3", "yon": "ana", "kural": [["F33", "<", 1.0], ["F33", "<=", "q25"]], "ad": "W3 Amihud düştü (oran < 1 ve alt çeyrek)"},
        "W3t":  {"kaynak": "W3", "yon": "ters", "kural": [["F33", ">=", "q75"]], "ad": "W3 ters: Amihud üst çeyrek"},
        "W4":   {"kaynak": "W4", "yon": "ana", "kural": [["F34", "<", 0.0], ["F34", "<=", "q25"]], "ad": "W4 sıfır getiri payı düştü (< 0 ve alt çeyrek)"},
        "W4t":  {"kaynak": "W4", "yon": "ters", "kural": [["F34", ">", 0.0], ["F34", ">=", "q75"]], "ad": "W4 ters: sıfır getiri payı arttı (> 0 ve üst çeyrek; q75 = 0 olan pazarda dejenere olmasın)"},
        "W5a":  {"kaynak": "W5", "yon": "ana", "kural": [["F35", "<=", "q25"]], "ad": "W5a ER_bölge alt çeyrek (yerinde sayma)"},
        "W5b":  {"kaynak": "W5", "yon": "ana", "kural": [["F36", ">=", "q75"]], "ad": "W5b ER_10 üst çeyrek (çıkış)"},
        "W6":   {"kaynak": "W6", "yon": "ana", "kural": [["F37", ">=", "q75"]], "ad": "W6 R/MDD üst çeyrek (dipten toparlanmış)"},
        "W6t":  {"kaynak": "W6", "yon": "ters", "kural": [["F37", "<=", "q25"]], "ad": "W6 ters: R/MDD alt çeyrek"},
        "E1":   {"kaynak": "E1", "yon": "ana", "kural": [["F39", "==", 0.0]], "ad": "E1 ÖNCEKİ BÖLGE süzgeci (bayrak 0 kalır)"},
        "E1t":  {"kaynak": "E1", "yon": "ters", "kural": [["F39", "==", 1.0]], "ad": "E1 ters: bayrak 1 (önceki bölge daha uygun)"},
        "E2":   {"kaynak": "E2", "yon": "ana", "kural": [["F41", "<=", 15.0]], "ad": "E2 HIZLI toparlanma hafızası (HIZ <= 15 bar)"},
        "E2t":  {"kaynak": "E2", "yon": "ters", "kural": [["F41", ">", 15.0]], "ad": "E2 ters: YAVAŞ (> 15) ya da UL"}},
    "kol": {"A": "Y1 (bütün olay_Y1.csv.gz satırları)", "B": "Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; YH_ESIK6 G2; olay_Y9.csv.gz ile küme eşitliği)"},
    "donem": {"egitim": ["2016-22"], "sinama": ["2023", "2024-26"]},
    "pazar": ["ABD+AVR", "ABD", "AVR", "BIST"], "karar_pazar": "ABD+AVR", "n_min": 30,
    "olcu": "1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): hücre = (aday süzgeci VE kol tabanı) x pazar x dönem; "
            "n = h5 ve es_h5 olan olay; P olay = ort h5, P eş = ort es_h5 (aynı gün aynı OC kovası eşleri), FARK = P olay - P eş; MARJİNAL = "
            "FARK(süzgeçli) - FARK(kol tabanı, aynı pazar x dönem); stop: ort st5 (olay) / ort es_st5 (eş)",
    "etiket": "YÖN 1 (eşik 2016-22): eğitim hücresi 2016-22, sınama 2023-26; YÖN 2 (eşik 2023-26): sınama hücresi 2016-22. KATKI+ = (eğitim, sınama, "
              "YÖN 2 sınama) üçünde n >= 30 VE FARK > 0 VE MARJİNAL > 0, ayrıca eğitim ve sınamada st5 olay <= es_st5 eş (eş payından stop payı "
              "büyük değil); KATKI− = üçünde n >= 30 VE MARJİNAL < 0; değilse SORGULA. Karar pazarı ABD+AVR; ABD / AVR / BIST bilgi",
    "mahkeme": {"prefix_n": 3, "hata_azami_oran": 0.01},
    "prefix": {"n": 25, "tohum": 1119},
    "coklu": "18 aday x 2 kol = 36 karne satırı: BH uygulanmaz (ikili, iki dönem + ters yön kuralı); şansla KATKI+ olasılığı rapora yazılır",
    "yeniden_uretim": [["W1", "A", "ABD+AVR", "sinama"], ["E2", "B", "ABD+AVR", "egitim"]],
}

YH_KONTROL_D1: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "olay ve eş olay_Y1.csv.gz'den (yh_olay_olc: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar "
                   "takip geometrisi); FARK = P olay - P eş aynı satırlarda; MARJİNAL kol tabanına göre (Y1 / Y9) aynı pazar x dönem; mekanik üstünlük: "
                   "F30 / F33 / F34 aralık ve hacim ölçüleri F3 / F13 ile ilişkili -> Spearman tablosu ön kayıtta (getirisiz); E1 / E2 sabit eşik"),
    "K2": ("EVET", "F30-F38 ve F41-F42 yalnız [.., t-1] barları (yh_d1_bar t barını okumaz); sol = GOZ_ETIKET.ge_bolge (S6 nedensel); F39-F40 "
                   "yh_mahkeme_hisse veriyi t'de keser; yh_devir_ozellik_yaz pazar başına 25 rastgele olayda veri t'de kesilince aynı değer (DURUR) ve "
                   "t - sol = F8 (ozellik_Y1) bütün satırlarda (DURUR); çeyrek eşikleri getirisiz, ön kayıtta mühürlü"),
    "K3": ("EVET", "aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); pencereler "
                   "geçerli bar sayımıyla; geçersiz bar veri dizisinde yok (CS çiftleri geçerli komşu barlar)"),
    "K4": ("EVET", "Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç olay düşürmez, yalnız seçer; hücrede ort "
                   "yanında P olay / P eş ayrı"),
    "K5": ("EVET", "giriş t+1 açılışı (olay_Y1 E0 / OC); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA)"),
    "K6": ("EVET", "aynı V_*.pkl tek kip (Yahoo düzeltilmiş); bütün yeni ölçüler oran / pay / log / bar sayısı (birimsiz; Amihud oranı para birimini "
                   "götürür); F34 hisse kendi öncesine göre fark (tick düzeyi hisseler arası kullanılmaz); AVR yerel para"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batanlar yok): P olay ve P eş yukarı yanlı, FARK'ta kısmen götürür; dipte (KOL-B) daha büyük "
                   "olabilir; rapora yazılır"),
    "K8": ("EVET", "hücre n < 30 SORGULA (ölçülemedi); iki dönem + ters yön aynı yön şartı; 36 karne satırı BH yok (ikili kural) -> şans KATKI+ notu; "
                   "ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış) -> KATKI+ en fazla EMARE düzeyi, iz denmez; küçük n bulgu değil"),
    "K9": ("EVET", "DEVIR_1_ON_KAYIT.md: YH_ESIK_D1_SHA, YH_ESIK / 6 / 7 sha (= ON_KAYIT_5 / 6 / 7), kod / özellik / eşik json / olay_Y1 / olay_Y9 "
                   "sha + getirisiz huni; yh_d1_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i ('DEVİR 1 ön kayıt') "
                   "koşudan önce; eşik sonuca göre oynanmaz; ikinci koşu DURUR"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları"),
    "K11": ("EVET", "devir1_sonuc.json + ozellik_Y1_d1.csv.gz + olay_Y1.csv.gz; DEVIR_1_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (W1 A ABD+AVR sınama, "
                    "E2 B ABD+AVR eğitim) ayrı kodla (_yh_d1_yeniden: düz pandas sorgusu) yeniden üretilir; fark > 1e-12 ise DURUR"),
    "K12": ("EVET", "etiket yalnız karne kuralı (KATKI+ / KATKI− / SORGULA); 'iz / emare' denmez; FARK yüzde puan, yorum ayrı cümle; fiyat değişimi "
                    "ile gerçekleşen getiri ayrımı: h5 hedef payı (stop'tan önce +%5), getiri değil"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_d1_ / yh_devir_ / YH_ESIK_D1 / _YH_D1 önekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, "
                    "üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da "
                    "'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi"),
}


def yh_esik_d1_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return yh_esik_sha(YH_ESIK_D1 if E is None else E)


def _yh_d1_cs(H: np.ndarray, L: np.ndarray, C: np.ndarray, a: int, b: int) -> Tuple[float, int]:
    """Corwin-Schultz (2012) iki-gün çifti spread tahmini; barlar [a, b) içindeki (j, j+1) çiftleri. Döner: (ort S, çift sayısı)."""
    if b - a < 2:
        return np.nan, 0
    h0, l0, c0 = H[a:b - 1], L[a:b - 1], C[a:b - 1]
    h1, l1 = H[a + 1:b].astype(float).copy(), L[a + 1:b].astype(float).copy()
    dn = c0 < l1; s = np.where(dn, l1 - c0, 0.0); h1 = h1 - s; l1 = l1 - s
    up = c0 > h1; s = np.where(up, c0 - h1, 0.0); h1 = h1 + s; l1 = l1 + s
    ok = (l0 > 0) & (l1 > 0) & (h0 > 0) & (h1 > 0)
    if not ok.any():
        return np.nan, 0
    h0, l0, h1, l1 = h0[ok], l0[ok], h1[ok], l1[ok]
    beta = np.log(h0 / l0) ** 2 + np.log(h1 / l1) ** 2
    gamma = np.log(np.maximum(h0, h1) / np.minimum(l0, l1)) ** 2
    k = 3.0 - 2.0 * math.sqrt(2.0)
    alpha = (np.sqrt(2.0 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
    S = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))
    S = np.maximum(S, 0.0)
    return float(np.mean(S)), int(len(S))


def yh_d1_bar(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray, i: int, sol: int,
              E: Dict[str, Any] = YH_ESIK_D1) -> Dict[str, float]:
    """t = i (geçerli bar sırası), bölge [sol, i-1] için F30-F38, F41, F42. Yalnız [0, i-1] okunur (t barı girmez)."""
    P = E["pencere"]; out = {k: np.nan for k in _YH_D1_BAR}
    O, H, L, C, V = (np.asarray(x[:i], float) for x in (O, H, L, C, V))        # t barı ve sonrası kesilir
    nb = i - sol
    if not (0 < sol < i):
        return out
    ob = int(P["onceki"]); omin = int(P["onceki_min"]); bmin = int(P["bolge_min"]); a0 = max(1, sol - ob); no = sol - a0
    # F30 Corwin-Schultz
    sb, kb = _yh_d1_cs(H, L, C, sol, i); so, ko = _yh_d1_cs(H, L, C, a0, sol)
    if kb >= int(P["bolge_min_cs"]) and no >= omin and np.isfinite(so) and so > 0 and np.isfinite(sb):
        out["F30"] = sb / so
    # F31 / F32 gece / gün-içi
    if nb >= bmin:
        j = np.arange(sol, i)
        B = float(np.prod(C[j] / O[j]) - 1.0); A = float(np.prod(O[j] / C[j - 1]) - 1.0)
        out["F31"] = B; out["F32"] = A - B
    # F33 Amihud, F34 sıfır getiri
    if nb >= bmin and no >= omin:
        jb = np.arange(sol, i); jo = np.arange(a0, sol)
        il = lambda jj: np.abs(C[jj] / C[jj - 1] - 1.0) / (C[jj] * V[jj])  # noqa: E731
        mo = float(np.mean(il(jo)))
        if mo > 0:
            out["F33"] = float(np.mean(il(jb))) / mo
        out["F34"] = float(np.mean(C[jb] == C[jb - 1])) - float(np.mean(C[jo] == C[jo - 1]))
    # F35 / F36 Kaufman ER
    if nb >= bmin:
        dz = float(np.sum(np.abs(np.diff(C[sol - 1:i]))))
        if dz > 0:
            out["F35"] = abs(C[i - 1] - C[sol - 1]) / dz
    k10 = int(P["er_kisa"])
    if i >= k10 + 1:
        dz = float(np.sum(np.abs(np.diff(C[i - k10 - 1:i]))))
        if dz > 0:
            out["F36"] = abs(C[i - 1] - C[i - k10 - 1]) / dz
    # F37 / F38 Choi MDD / R
    m = int(P["mdd_gun"])
    if i >= m:
        Pl = np.log(C[i - m:i]); dd = np.maximum.accumulate(Pl) - Pl; mdd = float(dd.max()); tau = int(np.argmax(dd))
        R = float(Pl[-1] - Pl[tau]); out["F38"] = R
        if mdd > 0:
            out["F37"] = R / mdd
    # F41 / F42 toparlanma hızı
    g = int(P["hiz_gun"]); lo = i - g
    if lo >= 0 and sol - lo >= 1:
        js = lo + int(np.argmin(L[lo:sol]))
        for kol, hd in (("F41", P["hiz_hedef"]), ("F42", P["hiz_hedef2"])):
            hit = np.flatnonzero(C[js + 1:sol] >= L[js] * (1.0 + float(hd)))
            out[kol] = float(hit[0] + 1) if len(hit) else float("inf")
    return out


def yh_d1_mahkeme(d: pd.DataFrame, t: pd.Timestamp) -> Dict[str, float]:
    """F39 (ÖNCEKİ BÖLGE bayrağı) ve F40 (PUAN_FARK); yh_mahkeme_hisse (veri t'de kesilir; prefix kapısı ayrı denetlenir)."""
    M = yh_mahkeme_hisse(d, t, prefix=False)
    en = M["en_iyi"]
    return {"F39": 1.0 if M["onceki_daha_uygun"] else 0.0, "F40": float(M["secilen"]["puan"] - en["puan"]) if en is not None else np.nan}


def yh_devir_ozellik(df: pd.DataFrame, tarihler: List[pd.Timestamp], hazir: bool = False, mahkeme: bool = True,
                     E: Dict[str, Any] = YH_ESIK_D1) -> pd.DataFrame:
    """Bir hissenin Y1 günleri için F30-F42 (+ _sol, _hata). Veri _yh_hazir; sol = GOZ_ETIKET.ge_bolge (S6 nedensel). Gün veride yoksa YHHata."""
    import GOZ_ETIKET as GE
    d = df if hazir else _yh_hazir(df)
    T = GE.ge_s6(d)
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    pos = d.index.get_indexer(pd.DatetimeIndex(pd.to_datetime(list(tarihler))))
    if (pos < 0).any():
        raise YHHata("DEVİR 1 özellik: sinyal günü geçerli bar değil")
    sat = []
    for t, i in zip(pd.to_datetime(list(tarihler)), pos):
        i = int(i)
        try:
            sol = int(GE.ge_bolge(T, i)["sol"])
        except Exception as ex:
            raise YHHata(f"DEVİR 1 özellik: bölge tanımsız ({t.date()}): {ex}")
        r = yh_d1_bar(O, H, L, C, V, i, sol, E); r["_sol"] = float(i - sol); r["_hata"] = ""
        if mahkeme:
            try:
                r.update(yh_d1_mahkeme(d.iloc[:i + 1], t))
            except Exception as ex:          # tek olay bozuksa NaN; sayılır, oran eşiği aşılırsa yazıcı DURUR
                r.update({"F39": np.nan, "F40": np.nan}); r["_hata"] = f"mahkeme: {ex}"[:200]
        else:
            r.update({"F39": np.nan, "F40": np.nan})
        sat.append(r)
    return pd.DataFrame(sat, columns=_YH_D1_OZ + ["_sol", "_hata"])


_YH_D1_IS_V: Dict[str, pd.DataFrame] = {}


def _yh_d1_isci(is_: Tuple[str, List[pd.Timestamp]]) -> List[Dict[str, Any]]:
    s, tl = is_
    try:
        R = yh_devir_ozellik(_YH_D1_IS_V[s], tl)
        return [{"sembol": s, "tarih": pd.Timestamp(t), **r} for t, r in zip(tl, R.to_dict("records"))]
    except Exception as ex:
        return [{"sembol": s, "tarih": pd.Timestamp(t), **{k: np.nan for k in _YH_D1_OZ}, "_sol": np.nan, "_hata": f"hisse: {ex}"[:200]} for t in tl]


def yh_devir_ozellik_yaz(veri: Optional[str] = None, cikti: Optional[str] = None, islem: int = 1, denetim_n: Optional[int] = None,
                         E: Dict[str, Any] = YH_ESIK_D1, olay_y1: Optional[str] = None, ozellik: Optional[str] = None) -> Dict[str, Any]:
    """Bütün Y1 olayları (olay_Y1.csv.gz anahtarları) -> ozellik_Y1_d1.csv.gz (F30-F42) + denetim json. Kapılar: t - sol = F8 (ozellik_Y1) bütün
    satırlarda; pazar başına denetim_n rastgele olay veri t'de kesilince aynı değer (F39 / F40 dahil); bir pazar için 3 olayda mahkeme prefix=True;
    hisse hatası ya da mahkeme hata oranı > %1 -> DURUR."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D1_DOSYA["ozellik"])
    yo = olay_y1 or os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1"))
    yf = ozellik or YH_YOL["ozellik"]
    for y in (yo, yf):
        if not os.path.exists(y):
            raise YHHata(f"DEVİR 1: dosya yok: {y}")
    K = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"], dtype={"sembol": str, "pazar": str})
    if K.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata("olay_Y1'de aynı (pazar, sembol, tarih) iki kez")
    F8 = pd.read_csv(yf, usecols=["pazar", "sembol", "tarih", "F8"], parse_dates=["tarih"], dtype={"sembol": str, "pazar": str})
    dn = int(E["prefix"]["n"] if denetim_n is None else denetim_n); sat: List[Dict[str, Any]] = []
    den: Dict[str, Any] = {"surum": YH_SURUM, "esik_d1_sha": yh_esik_d1_sha(E), "olay_y1_sha": _yh_sha_dosya(yo), "pazar": {}}
    for pi, p in enumerate(OC.OC_ESIK["pazar"]):
        Kp = K[K.pazar == p]
        if not len(Kp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        eksik = sorted(set(Kp.sembol) - set(Vd["V"]))
        if eksik:
            raise YHHata(f"DEVİR 1 özellik: {p} veride olmayan sembol {eksik[:5]}")
        isler = [(s, list(g.tarih)) for s, g in Kp.groupby("sembol", sort=True)]
        _YH_D1_IS_V.clear(); _YH_D1_IS_V.update({s: _yh_hazir(Vd["V"][s]) for s, _ in isler})
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as pool:
                parca = pool.map(_yh_d1_isci, isler, chunksize=4)
        else:
            parca = [_yh_d1_isci(x) for x in isler]
        Xp = pd.DataFrame([r for pr in parca for r in pr]); Xp.insert(0, "pazar", p)
        hh = Xp[Xp._hata.str.startswith("hisse")]
        if len(hh):
            raise YHHata(f"DEVİR 1 özellik: {p} hisse hatası {len(hh)} satır, ilk: {hh._hata.iloc[0]} -> DURDU")
        mh = int(Xp._hata.str.startswith("mahkeme").sum())
        if mh > E["mahkeme"]["hata_azami_oran"] * len(Xp):
            raise YHHata(f"DEVİR 1 özellik: {p} mahkeme hatası {mh} / {len(Xp)} (> %{100 * E['mahkeme']['hata_azami_oran']:.0f}) -> DURDU")
        Z = Xp.merge(F8[F8.pazar == p], on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
        bad = ~np.isclose(Z._sol.to_numpy(float), Z.F8.to_numpy(float), rtol=0, atol=1e-9)
        if bad.any():
            raise YHHata(f"DEVİR 1 özellik: {p} t - sol != F8 ({int(bad.sum())} satır) -> DURDU")
        rng = np.random.default_rng([int(E["prefix"]["tohum"]), pi]); ok = 0; okm = 0
        for qi, q in enumerate(rng.choice(len(Xp), min(dn, len(Xp)), replace=False)):
            r = Xp.iloc[int(q)]; t = pd.Timestamp(r.tarih)
            kes = Vd["V"][r.sembol]; kes = kes[kes.index <= t]
            a = yh_devir_ozellik(kes, [t]).iloc[0][_YH_D1_OZ].to_numpy(float)
            c = r[_YH_D1_OZ].to_numpy(float)
            if not np.allclose(a, c, rtol=1e-9, atol=1e-12, equal_nan=True):
                raise YHHata(f"DEVİR 1 prefix denetimi TUTMADI: {p} {r.sembol} {t.date()} -> DURDU")
            ok += 1
            if qi < int(E["mahkeme"]["prefix_n"]):
                yh_mahkeme_hisse(kes, t, prefix=True); okm += 1        # aday değerleri t_k'da kesilince aynı (değilse YHHata)
        den["pazar"][p] = {"olay": int(len(Xp)), "prefix_tuttu": ok, "mahkeme_prefix_tuttu": okm, "mahkeme_hata": mh,
                           "nan": {k: int(Xp[k].isna().sum()) for k in _YH_D1_OZ}, "inf": {k: int(np.isinf(Xp[k].to_numpy(float)).sum()) for k in ("F41", "F42")}}
        yhlog.info("DEVİR 1 özellik %s: %d olay, prefix %d tuttu, mahkeme hata %d", p, len(Xp), ok, mh)
        sat.extend(Xp.to_dict("records")); _YH_D1_IS_V.clear(); del Vd
    X = pd.DataFrame(sat)[["pazar", "sembol", "tarih"] + _YH_D1_OZ]
    if len(X) != len(K):
        raise YHHata(f"DEVİR 1 özellik: satır {len(X)} != olay_Y1 {len(K)}")
    X = X.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    X.to_csv(yol, index=False, float_format="%.10g", compression="gzip", date_format="%Y-%m-%d")
    den["satir"] = int(len(X)); den["sha"] = _yh_sha_dosya(yol)
    _yh_yaz(os.path.join(cikti, YH_D1_DOSYA["denetim"]), json.dumps(den, ensure_ascii=False, indent=1, default=_yh_json), "DEVİR 1 denetim")
    return {"yol": yol, **den}


def yh_d1_taban(cikti: Optional[str] = None, getiri: bool = False) -> pd.DataFrame:
    """olay_Y1 (kimlik + dönem; getiri=True ise h5 / es_h5 / st5 / es_st5) ∩ ozellik_Y1_d1 ∩ ozellik_Y1 (F15, F17) + KOL-B bayrağı."""
    cikti = cikti or YH_YOL["cikti"]
    yo = os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1")); yd = os.path.join(cikti, YH_D1_DOSYA["ozellik"])
    for y in (yo, yd, YH_YOL["ozellik"]):
        if not os.path.exists(y):
            raise YHHata(f"DEVİR 1: dosya yok: {y}")
    kol = ["pazar", "sembol", "tarih", "donem"] + (["h5", "es_h5", "st5", "es_st5"] if getiri else [])
    K = pd.read_csv(yo, usecols=kol, parse_dates=["tarih"], dtype={"sembol": str})
    D = pd.read_csv(yd, parse_dates=["tarih"], dtype={"sembol": str})
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F15", "F17"], parse_dates=["tarih"], dtype={"sembol": str})
    M = K.merge(D, on=["pazar", "sembol", "tarih"], how="outer", validate="one_to_one", indicator=True)
    if (M._merge != "both").any():
        raise YHHata(f"DEVİR 1: olay_Y1 ve ozellik_Y1_d1 anahtarları farklı ({int((M._merge != 'both').sum())}) -> DURDU")
    M = M.drop(columns="_merge").merge(G, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    g2 = YH_ESIK6["grup"]["G2"]
    with np.errstate(invalid="ignore"):
        M["kolB"] = (M.F15.to_numpy(float) <= g2["F15_ust"]) & (M.F17.to_numpy(float) <= g2["F17_ust"])
    M["kolA"] = True
    return M.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)


def yh_d1_esik(M: pd.DataFrame, E: Dict[str, Any] = YH_ESIK_D1) -> Dict[str, Any]:
    """Çeyrek eşikleri (getirisiz): yön x pazar x özellik -> {q25, q75}; bütün Y1 olaylarının sonlu değerleri."""
    Q = E["ceyrek"]; kol = sorted({k[0] for a in E["aday"].values() for k in a["kural"] if k[2] in ("q25", "q75")})
    out: Dict[str, Any] = {}
    for yon in ("yon1", "yon2"):
        out[yon] = {}
        for p in OC.OC_ESIK["pazar"]:
            X = M[(M.pazar == p) & M.donem.isin(Q[yon])]; out[yon][p] = {}
            for c in kol:
                v = X[c].to_numpy(float); v = v[np.isfinite(v)]
                out[yon][p][c] = {"q25": float(np.quantile(v, Q["alt"])) if len(v) else np.nan,
                                  "q75": float(np.quantile(v, Q["ust"])) if len(v) else np.nan, "n": int(len(v))}
    return out


_YH_D1_OP = {"<": np.less, "<=": np.less_equal, ">": np.greater, ">=": np.greater_equal, "==": np.equal}


def yh_d1_maske(M: pd.DataFrame, aday: str, esik: Dict[str, Any], yon: str, E: Dict[str, Any] = YH_ESIK_D1) -> np.ndarray:
    """Aday süzgeci (NaN tutmaz; inf yalnız sayısal karşılaştırmayla: F41 UL = inf -> '<= 15' tutmaz, '> 15' tutar)."""
    m = np.zeros(len(M), bool)
    for p in OC.OC_ESIK["pazar"]:
        pm = (M.pazar == p).to_numpy()
        if not pm.any():
            continue
        mp_ = np.ones(int(pm.sum()), bool)
        for c, op, v in E["aday"][aday]["kural"]:
            x = M.loc[pm, c].to_numpy(float)
            th = float(esik[yon][p][c][v]) if isinstance(v, str) else float(v)
            with np.errstate(invalid="ignore"):
                mp_ &= ~np.isnan(x) & _YH_D1_OP[op](x, th)
        m[pm] = mp_
    return m


def yh_d1_huni(M: pd.DataFrame, esik: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D1) -> Dict[str, Any]:
    """Getirisiz huni: aday x kol x pazar x dönem olay satırı sayısı (YÖN 1 eşikleri) + taban satırları."""
    dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]; out: Dict[str, Any] = {}
    for kol in ("A", "B"):
        km = M[f"kol{kol}"].to_numpy(bool)
        out[f"taban|{kol}"] = {f"{p}|{q}": int((km & (M.pazar == p).to_numpy() & (M.donem == q).to_numpy()).sum())
                               for p in OC.OC_ESIK["pazar"] for q in dn}
        for a in E["aday"]:
            am = yh_d1_maske(M, a, esik, "yon1", E) & km
            out[f"{a}|{kol}"] = {f"{p}|{q}": int((am & (M.pazar == p).to_numpy() & (M.donem == q).to_numpy()).sum())
                                 for p in OC.OC_ESIK["pazar"] for q in dn}
    return out


def yh_d1_spearman(M: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Getirisiz mekanik ilişki tablosu (K1): F30-F41 ile F3 / F10 / F13 / F15 Spearman (bütün Y1, sonlu satırlar)."""
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F3", "F10", "F13"], parse_dates=["tarih"], dtype={"sembol": str})
    X = M.merge(G, on=["pazar", "sembol", "tarih"], how="left")
    out: Dict[str, Dict[str, float]] = {}
    for c in ["F30", "F31", "F32", "F33", "F34", "F35", "F36", "F37", "F41"]:
        out[c] = {}
        for r in ("F3", "F10", "F13", "F15"):
            Z = X[[c, r]].replace([np.inf, -np.inf], np.nan).dropna()
            out[c][r] = float(Z[c].rank().corr(Z[r].rank())) if len(Z) > 30 else np.nan
    return out


def _yh_d1_sha(cikti: str) -> Dict[str, str]:
    out = {"esik_d1": yh_esik_d1_sha(), "esik": yh_esik_sha(), "esik6": yh_esik6_sha(), "esik7": yh_esik7_sha(), "kod": _yh_sha_dosya(YH_YOL["kod"])}
    for ad, yol in (("ozellik_d1", os.path.join(cikti, YH_D1_DOSYA["ozellik"])), ("esik_json", os.path.join(cikti, YH_D1_DOSYA["esik"])),
                    ("y1olay", os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1"))), ("y9olay", os.path.join(cikti, YH_DOSYA["satir"].format(d="Y9"))),
                    ("ozellik", YH_YOL["ozellik"])):
        if not os.path.exists(yol):
            raise YHHata(f"DEVİR 1: dosya yok: {yol}")
        out[ad] = _yh_sha_dosya(yol)
    return out


_YH_D1_DESEN = {"esik_d1": r"YH_ESIK_D1_SHA:\s*`([0-9a-f]{64})`", "esik": r"YH_ESIK_SHA:\s*`([0-9a-f]{64})`", "esik6": r"YH_ESIK6_SHA:\s*`([0-9a-f]{64})`",
                "esik7": r"YH_ESIK7_SHA:\s*`([0-9a-f]{64})`", "kod": r"YH_KOD_SHA:\s*`([0-9a-f]{64})`",
                "ozellik_d1": r"D1_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "esik_json": r"D1_ESIK_JSON_SHA:\s*`([0-9a-f]{64})`",
                "y1olay": r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`", "y9olay": r"Y9_OLAY_SHA:\s*`([0-9a-f]{64})`",
                "ozellik": r"(?<![A-Z0-9_])OZELLIK_SHA:\s*`([0-9a-f]{64})`"}   # düzeltme: D1_OZELLIK_SHA satırını yakalamasın


def _yh_d1_regresyon(cikti: str, M: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Regresyon kapısı: YH_ESIK / 6 / 7 sha = ON_KAYIT_5 / 6 / 7 mührü (Y1-Y12 eşikleri değişmedi); KOL-B kümesi = olay_Y9.csv.gz kümesi."""
    out = {}
    for ad, dosya, fn, desen in (("esik", "ON_KAYIT_5.md", yh_esik_sha, _YH_KAPI_DESEN["esik"]), ("esik6", "ON_KAYIT_6.md", yh_esik6_sha, _YH_D1_DESEN["esik6"]),
                                 ("esik7", "ON_KAYIT_7.md", yh_esik7_sha, _YH_D1_DESEN["esik7"])):
        y = os.path.join(cikti, dosya)
        mm = re.search(desen, open(y, encoding="utf-8").read()) if os.path.exists(y) else None
        if not (mm and mm.group(1) == fn()):
            raise YHHata(f"DEVİR 1 regresyon: {ad} {dosya} mührüyle aynı değil (Y1-Y12 eşikleri değişmiş) -> DURDU")
        out[ad] = mm.group(1)
    if M is not None:
        y9 = os.path.join(cikti, YH_DOSYA["satir"].format(d="Y9"))
        K9 = pd.read_csv(y9, usecols=["pazar", "sembol", "tarih"], parse_dates=["tarih"], dtype={"sembol": str})
        a = set(zip(K9.pazar, K9.sembol, K9.tarih)); B = M[M.kolB]; b = set(zip(B.pazar, B.sembol, B.tarih))
        if a != b:
            raise YHHata(f"DEVİR 1 regresyon: KOL-B kümesi olay_Y9 kümesiyle aynı değil ({len(a)} / {len(b)}) -> DURDU")
        out["kolB_n"] = len(b)
    return out


def yh_d1_onkayit_metni(huni: Dict[str, Any], esik: Dict[str, Any], spm: Dict[str, Any], sha: Dict[str, str], den: Dict[str, Any],
                        E: Dict[str, Any] = YH_ESIK_D1) -> str:
    dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]
    s = ["# YAPI_HEDEF — DEVİR 1 ÖN KAYIT (web / hakem adayları F30-F42, süzgeç karnesi; 2026-11-19)", "",
         f"{YH_SURUM}; DEVİR 1 eklendi (yh_devir_ozellik, yh_devir_kos). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar "
         "yalnız satır kimliği, dönem ve özellik dağılımıdır (getirisiz: h5 / es_h5 / st5 okunmadı).", "",
         f"- YH_ESIK_D1_SHA: `{sha['esik_d1']}` (DEVİR 1: tanımlar, pencereler, aday kuralları, kol, dönem, etiket)",
         f"- YH_ESIK_SHA: `{sha['esik']}` (= ON_KAYIT_5.md: Y1-Y11c AYNEN)", f"- YH_ESIK6_SHA: `{sha['esik6']}` (= ON_KAYIT_6.md)",
         f"- YH_ESIK7_SHA: `{sha['esik7']}` (= ON_KAYIT_7.md; Y12)", f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)",
         f"- D1_OZELLIK_SHA: `{sha['ozellik_d1']}` (ozellik_Y1_d1.csv.gz; F30-F42)", f"- D1_ESIK_JSON_SHA: `{sha['esik_json']}` (devir1_esik.json; çeyrekler)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (olay_Y1.csv.gz; ölçü satırları)", f"- Y9_OLAY_SHA: `{sha['y9olay']}` (olay_Y9.csv.gz; KOL-B regresyonu)",
         f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F8 / F15 / F17)", f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "## 1. ADAYLAR, F-KODLARI, TANIM, PENCERE, SABİT EŞİK", "",
         f"Pencereler: {json.dumps(E['pencere'], ensure_ascii=False)}. Bölge = Y1 olayının S6 bölgesi [sol, t-1] (GOZ_ETIKET.ge_bolge; t - sol = F8).", ""]
    for k, v in E["ozellik"].items():
        s.append(f"- **{k}**: {v}.")
    s += ["", f"Çeyrek kuralı: {E['ceyrek']['tanim']}.", "", "| Aday | Kaynak | Yön | Süzgeç kuralı | Ad |", "|---|---|---|---|---|"]
    for a, v in E["aday"].items():
        s.append(f"| {a} | {v['kaynak']} | {v['yon']} | {' VE '.join(f'{c} {o} {x}' for c, o, x in v['kural'])} | {v['ad']} |")
    s += ["", "### Çeyrek eşikleri (devir1_esik.json; YÖN 1 = 2016-22, YÖN 2 = 2023-26; pazar içi, bütün Y1 olayları)", "",
          "| Özellik | Pazar | YÖN 1 q25 / q75 (n) | YÖN 2 q25 / q75 (n) |", "|---|---|---|---|"]
    for c in sorted(esik["yon1"]["ABD"]):
        for p in OC.OC_ESIK["pazar"]:
            a1, a2 = esik["yon1"][p][c], esik["yon2"][p][c]
            s.append(f"| {c} | {p} | {a1['q25']:.6g} / {a1['q75']:.6g} ({a1['n']}) | {a2['q25']:.6g} / {a2['q75']:.6g} ({a2['n']}) |")
    s += ["", "## 2. ÖLÇÜ, KOLLAR, ETİKET", "", f"- KOLLAR: A = {E['kol']['A']}; B = {E['kol']['B']}.", f"- ÖLÇÜ: {E['olcu']}.",
          f"- ETİKET: {E['etiket']}.", f"- ÇOKLU KARŞILAŞTIRMA: {E['coklu']}.",
          f"- YENİDEN ÜRETİM hücreleri: {'; '.join(' / '.join(x) for x in E['yeniden_uretim'])}.",
          "- REGRESYON KAPISI: YH_ESIK / 6 / 7 sha = ON_KAYIT_5 / 6 / 7 mührü; KOL-B kümesi = olay_Y9.csv.gz kümesi; t - sol = F8; değilse DURUR.", "",
          "## 3. GETİRİSİZ HUNİ (Y1 olayı -> aday tutan olay sayısı; YÖN 1 eşikleri; pazar x dönem)", "",
          "| Satır | Kol | " + " | ".join(f"{p} {q}" for p in OC.OC_ESIK["pazar"] for q in dn) + " |",
          "|---|---|" + "---|" * (len(OC.OC_ESIK["pazar"]) * len(dn))]
    for kol in ("A", "B"):
        for a in ["taban"] + list(E["aday"]):
            r = huni[f"{a}|{kol}"]
            s.append(f"| {a} | {kol} | " + " | ".join(str(r[f'{p}|{q}']) for p in OC.OC_ESIK["pazar"] for q in dn) + " |")
    s += ["", "## 4. ÖZELLİK DENETİMİ (getirisiz)", "", "| Pazar | olay | prefix tuttu | mahkeme prefix | mahkeme hata | NaN (F30..F42) | inf F41 / F42 |",
          "|---|---|---|---|---|---|---|"]
    for p, v in den.get("pazar", {}).items():
        s.append(f"| {p} | {v['olay']} | {v['prefix_tuttu']} | {v['mahkeme_prefix_tuttu']} | {v['mahkeme_hata']} | "
                 f"{', '.join(f'{k} {n}' for k, n in v['nan'].items() if n)} | {v['inf']['F41']} / {v['inf']['F42']} |")
    s += ["", "### Mekanik ilişki (K1; Spearman, bütün Y1, getirisiz)", "", "| Özellik | F3 mum boyu | F10 bölge net | F13 kırılım hacmi | F15 konum |",
          "|---|---|---|---|---|"]
    for c, v in spm.items():
        s.append(f"| {c} | " + " | ".join("-" if not np.isfinite(v[r]) else f"{v[r]:+.2f}" for r in ("F3", "F10", "F13", "F15")) + " |")
    s += ["", "Uygulama yorumları (ölçümden önce): (1) CS çiftleri geçerli barlar dizisinde komşu (geçersiz bar atılmış; ABD'de nadir); (2) W2'de "
          "gece = O_j / C_j-1 - 1 düzeltilmiş fiyatla (temettü günü geceye düşer); (3) E1 seçilen bölge puanı 12 kural (YH_ESIK6 mahkeme), prefix=False "
          "ile hesaplanır, prefix=True pazar başına 3 olayda denetlenir; (4) E2 UL = inf (HIZLI değil, YAVAŞ sınıfına girer); (5) W5'te iki hücre "
          "(W5a, W5b) ayrı karne satırıdır, ters yön yok; (6) KATKI+ ters yön şartı E1 / E2'de (sabit eşik) YÖN 2 sınama hücresi = eğitim hücresi "
          "olur (aynı sayı).", "", yh_kontrol_tablosu(YH_KONTROL_D1), ""]
    return "\n".join(s) + "\n"


def yh_d1_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False, git: bool = True) -> str:
    """DEVIR_1_ON_KAYIT.md + devir1_esik.json (getirisiz). Özellik dosyası yazılmış, DEVİR 1 ölçülmemiş olmalı."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D1_DOSYA["onkayit"])
    if os.path.exists(os.path.join(cikti, YH_D1_DOSYA["sonuc"])):
        raise YHHata("devir1_sonuc.json var: DEVİR 1 ölçülmüş; ön kayıt ölçümden sonra yazılamaz")
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"DEVİR 1 ön kaydı zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"DEVİR 1 ön kaydı var ({yol}); git'e işlenmemişse --uzerine-yaz")
    M = yh_d1_taban(cikti, getiri=False)
    _yh_d1_regresyon(cikti, M)
    esik = yh_d1_esik(M)
    _yh_yaz(os.path.join(cikti, YH_D1_DOSYA["esik"]), json.dumps({"esik_d1_sha": yh_esik_d1_sha(), **esik}, ensure_ascii=False, indent=1,
                                                                default=_yh_json), "DEVİR 1 eşik")
    yd = os.path.join(cikti, YH_D1_DOSYA["denetim"]); den = json.load(open(yd, encoding="utf-8")) if os.path.exists(yd) else {}
    _yh_yaz(yol, yh_d1_onkayit_metni(yh_d1_huni(M, esik), esik, yh_d1_spearman(M), _yh_d1_sha(cikti), den), "DEVİR 1 ön kayıt")
    return yol


def yh_d1_kapi(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """DEVİR 1 koşu kapısı: kontrol listesi (ik_kontrol_kapisi) + sha'lar + regresyon + eşik json yeniden hesap + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D1_DOSYA["onkayit"])
    if not os.path.exists(yol):
        raise YHHata(f"DEVİR 1 ön kaydı yok: {yol}")
    metin = open(yol, encoding="utf-8").read(); out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in {**_YH_D1_DESEN, "zaman": _YH_KAPI_DESEN["zaman"]}.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"DEVİR 1 ön kaydında {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = _yh_d1_sha(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["regresyon"] = _yh_d1_regresyon(cikti)
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"])
    yhlog.info("yh_d1_kapi AÇIK (%s)", yol)
    return out


def yh_d1_hucre(X: pd.DataFrame) -> Dict[str, Any]:
    g = X[X.h5.notna() & X.es_h5.notna()]; n = int(len(g))
    if not n:
        return {"n": 0, "p_olay": np.nan, "p_es": np.nan, "fark": np.nan, "st": np.nan, "es_st": np.nan}
    po, pe = float(g.h5.mean()), float(g.es_h5.mean())
    return {"n": n, "p_olay": po, "p_es": pe, "fark": po - pe, "st": float(g.st5.mean()), "es_st": float(g.es_st5.mean())}


def yh_d1_etiket(c: Dict[str, Dict[str, Any]], nmin: int) -> str:
    """c: {'egitim', 'sinama', 'ters'} -> hücre (fark, marjinal, n, st, es_st). Kural YH_ESIK_D1['etiket']."""
    ks = ("egitim", "sinama", "ters")
    ok_n = all(c[k]["n"] >= nmin and np.isfinite(c[k]["fark"]) and np.isfinite(c[k]["marjinal"]) for k in ks)
    if ok_n and all(c[k]["fark"] > 0 and c[k]["marjinal"] > 0 for k in ks) and all(c[k]["st"] <= c[k]["es_st"] for k in ("egitim", "sinama")):
        return "KATKI+"
    if ok_n and all(c[k]["marjinal"] < 0 for k in ks):
        return "KATKI−"
    return "SORGULA"


def yh_d1_karne(M: pd.DataFrame, esik: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D1) -> List[Dict[str, Any]]:
    """Karne satırları: aday x kol x pazar; hücreler eğitim / sınama (YÖN 1) ve ters (YÖN 2 sınama = 2016-22)."""
    Dn = E["donem"]; dm = {"egitim": M.donem.isin(Dn["egitim"]).to_numpy(), "sinama": M.donem.isin(Dn["sinama"]).to_numpy()}
    dm["ters"] = dm["egitim"]; out = []
    for kol in ("A", "B"):
        km = M[f"kol{kol}"].to_numpy(bool)
        for pz in E["pazar"]:
            pm = M.pazar.isin(pz.split("+")).to_numpy()
            tb = {k: yh_d1_hucre(M[km & pm & dm[k]]) for k in ("egitim", "sinama", "ters")}
            out.append({"aday": "taban", "kol": kol, "pazar": pz, **{k: {**v, "marjinal": np.nan} for k, v in tb.items()}, "etiket": "-"})
            for a in E["aday"]:
                m1 = yh_d1_maske(M, a, esik, "yon1", E); m2 = yh_d1_maske(M, a, esik, "yon2", E)
                c = {"egitim": yh_d1_hucre(M[km & pm & dm["egitim"] & m1]), "sinama": yh_d1_hucre(M[km & pm & dm["sinama"] & m1]),
                     "ters": yh_d1_hucre(M[km & pm & dm["ters"] & m2])}
                for k in c:
                    c[k]["marjinal"] = c[k]["fark"] - tb[k]["fark"] if c[k]["n"] and tb[k]["n"] else np.nan
                out.append({"aday": a, "kol": kol, "pazar": pz, **c, "etiket": yh_d1_etiket(c, int(E["n_min"]))})
    return out


def _yh_d1_yeniden(cikti: str, aday: str, kol: str, pazar: str, hucre: str, E: Dict[str, Any] = YH_ESIK_D1) -> Dict[str, Any]:
    """Bağımsız yeniden üretim (K11): ham csv'ler + eşik json, düz pandas sorgusu (yh_d1_maske / yh_d1_hucre kullanılmaz)."""
    O = pd.read_csv(os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1")), dtype={"sembol": str})
    D = pd.read_csv(os.path.join(cikti, YH_D1_DOSYA["ozellik"]), dtype={"sembol": str})
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F15", "F17"], dtype={"sembol": str})
    Q = json.load(open(os.path.join(cikti, YH_D1_DOSYA["esik"]), encoding="utf-8"))
    X = O.merge(D, on=["pazar", "sembol", "tarih"]).merge(G, on=["pazar", "sembol", "tarih"], how="left")
    X = X[X.pazar.isin(pazar.split("+"))]
    if kol == "B":
        X = X.query("F15 <= 0.25 and F17 <= -0.20")
    yon = "yon2" if hucre == "ters" else "yon1"
    X = X[X.donem.isin(E["donem"]["egitim"] if hucre in ("egitim", "ters") else E["donem"]["sinama"])]
    parca = []
    for p, g in X.groupby("pazar"):
        for c, op, v in E["aday"][aday]["kural"]:
            th = Q[yon][p][c][v] if isinstance(v, str) else v
            g = g.query(f"{c} {op} {th!r}")
        parca.append(g)
    X = pd.concat(parca) if parca else X.iloc[:0]
    X = X.dropna(subset=["h5", "es_h5"])
    return {"n": int(len(X)), "fark": float(X.h5.mean() - X.es_h5.mean()) if len(X) else np.nan}


def yh_devir_kos(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True, E: Dict[str, Any] = YH_ESIK_D1) -> Dict[str, Any]:
    """DEVİR 1 koşusu: kapı -> karne (iki kol, iki yön) -> yeniden üretim -> devir1_sonuc.json + DEVIR_1_RAPOR.md. İkinci koşu DURUR."""
    cikti = cikti or YH_YOL["cikti"]; ys = os.path.join(cikti, YH_D1_DOSYA["sonuc"])
    if os.path.exists(ys):
        raise YHHata("devir1_sonuc.json var: DEVİR 1 zaten ölçüldü (ikinci koşu yok)")
    kp = yh_d1_kapi(cikti, git=git, kontrol=kontrol)
    M = yh_d1_taban(cikti, getiri=True)
    _yh_d1_regresyon(cikti, M)
    esik = json.load(open(os.path.join(cikti, YH_D1_DOSYA["esik"]), encoding="utf-8"))
    yeni = yh_d1_esik(M[["pazar", "sembol", "tarih", "donem"] + _YH_D1_OZ], E)
    if json.dumps(yeni, sort_keys=True, default=_yh_json) != json.dumps({k: esik[k] for k in ("yon1", "yon2")}, sort_keys=True, default=_yh_json):
        raise YHHata("DEVİR 1: eşik json yeniden hesapla aynı değil -> DURDU")
    K = yh_d1_karne(M, esik, E)
    yu = []
    for a, kol, pz, h in E["yeniden_uretim"]:
        r = [x for x in K if x["aday"] == a and x["kol"] == kol and x["pazar"] == pz][0][h]
        b = _yh_d1_yeniden(cikti, a, kol, pz, h, E)
        tut = b["n"] == r["n"] and (np.isclose(b["fark"], r["fark"], rtol=0, atol=1e-12) or (np.isnan(b["fark"]) and np.isnan(r["fark"])))
        if not tut:
            raise YHHata(f"DEVİR 1 yeniden üretim TUTMADI: {a} {kol} {pz} {h}: {r['n']} / {r['fark']} vs {b['n']} / {b['fark']} -> DURDU")
        yu.append({"aday": a, "kol": kol, "pazar": pz, "hucre": h, "kod_n": r["n"], "kod_fark": r["fark"], "yeni_n": b["n"], "yeni_fark": b["fark"],
                   "durum": "TUTTU"})
    J = {"surum": YH_SURUM, "zaman_utc": _yh_simdi(), "kapi": {k: v for k, v in kp.items() if k != "yol"}, "karne": K, "yeniden_uretim": yu,
         "esik_d1_sha": yh_esik_d1_sha(E)}
    _yh_yaz(ys, json.dumps(J, ensure_ascii=False, indent=1, default=_yh_json), "DEVİR 1 sonuç")
    return {"json": J, "rapor": yh_devir_rapor(cikti, E)}


def yh_devir_rapor(cikti: Optional[str] = None, E: Dict[str, Any] = YH_ESIK_D1) -> str:
    """DEVIR_1_RAPOR.md (devir1_sonuc.json + isteğe bağlı devir1_hata.json)."""
    cikti = cikti or YH_YOL["cikti"]; ys = os.path.join(cikti, YH_D1_DOSYA["sonuc"])
    if not os.path.exists(ys):
        raise YHHata("devir1_sonuc.json yok: önce `python YAPI_HEDEF.py devir1kos`")
    J = json.load(open(ys, encoding="utf-8")); K = J["karne"]
    yh_ = os.path.join(cikti, YH_D1_DOSYA["hata"]); H_ = json.load(open(yh_, encoding="utf-8")) if os.path.exists(yh_) else []
    pc = lambda x: "-" if x is None or not np.isfinite(float(x)) else f"{100 * float(x):+.1f}".replace(".", ",")  # noqa: E731
    pp = lambda x: "-" if x is None or not np.isfinite(float(x)) else f"%{100 * float(x):.1f}".replace(".", ",")  # noqa: E731
    kp = E["karar_pazar"]
    sat = [x for x in K if x["pazar"] == kp and x["aday"] != "taban"]
    say = {e: sum(1 for x in sat if x["etiket"] == e) for e in ("KATKI+", "KATKI−", "SORGULA")}
    s = ["# YAPI_HEDEF — DEVİR 1 RAPORU (web / hakem adayları F30-F42, süzgeç karnesi)", "",
         f"{J['surum']}. Koşu: {J['zaman_utc']}. Ön kayıt: DEVIR_1_ON_KAYIT.md ({J['kapi'].get('onkayit_zaman', '?')}"
         f"{', git ' + J['kapi']['git_onkayit'].get('commit', '?')[:10] if J['kapi'].get('git_onkayit') else ''}). Komut: `python YAPI_HEDEF.py devir1kos`.", "",
         f"**SONUÇ (karar pazarı {kp}, 36 satır): KATKI+ {say['KATKI+']}, KATKI− {say['KATKI−']}, SORGULA {say['SORGULA']}.** "
         "KATKI+ olanlar: " + (", ".join(f"{x['aday']} (kol {x['kol']})" for x in sat if x["etiket"] == "KATKI+") or "yok") + ".", "",
         f"Ölçü: {E['olcu']}. Etiket: {E['etiket']}. Değerler yüzde puan; P = 15 barda +%5 hedefin stop'tan önce görülme payı.", "",
         f"## 1. Karne ({kp})", "",
         "| Aday | Kol | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters yön sınama n / FARK (MARJ) | stop olay / eş (eğitim; sınama) | etiket |",
         "|---|---|---|---|---|---|---|"]

    def satir(x: Dict[str, Any]) -> str:
        e, si, te = x["egitim"], x["sinama"], x["ters"]
        return (f"| {x['aday']} | {x['kol']} | {e['n']} / {pc(e['fark'])} ({pc(e['marjinal'])}) | {si['n']} / {pc(si['fark'])} ({pc(si['marjinal'])}) | "
                f"{te['n']} / {pc(te['fark'])} ({pc(te['marjinal'])}) | {pp(e['st'])} / {pp(e['es_st'])}; {pp(si['st'])} / {pp(si['es_st'])} | {x['etiket']} |")
    for kol in ("A", "B"):
        for x in K:
            if x["pazar"] == kp and x["kol"] == kol:
                s.append(satir(x))
    for pz in [p for p in E["pazar"] if p != kp]:
        s += ["", f"## {pz} (bilgi)", "", "| Aday | Kol | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters yön sınama n / FARK (MARJ) | "
              "stop olay / eş (eğitim; sınama) | etiket |", "|---|---|---|---|---|---|---|"]
        s += [satir(x) for x in K if x["pazar"] == pz]
    s += ["", "## YENİDEN ÜRETİM (K11; _yh_d1_yeniden: ham csv + eşik json, düz pandas sorgusu)", "",
          "| Aday | Kol | Pazar | Hücre | kod n / FARK | yeniden n / FARK | durum |", "|---|---|---|---|---|---|---|"]
    for r in J["yeniden_uretim"]:
        s.append(f"| {r['aday']} | {r['kol']} | {r['pazar']} | {r['hucre']} | {r['kod_n']} / {pc(r['kod_fark'])} | {r['yeni_n']} / {pc(r['yeni_fark'])} | "
                 f"{r['durum']} |")
    s += ["", "## Notlar", "", "- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı): P olay ve P eş yukarı yanlı; FARK'ta kısmen götürür; KOL-B "
          "(dipte) daha büyük olabilir.", "- ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış): KATKI+ en fazla EMARE düzeyi okunur, iz değildir.",
          f"- {E['coklu']}.", "- Kod değişti: Colab'da çalışma zamanını yeniden başlat.", "", "## HATA", ""]
    s += [f"- {h}" for h in H_] if H_ else ["- (koşuda hata kaydı yok; alt ajan raporu devir1_hata.json'a yazar)"]
    s += ["", yh_kontrol_tablosu(YH_KONTROL_D1), ""]
    metin = "\n".join(s) + "\n"
    _yh_yaz(os.path.join(cikti, YH_D1_DOSYA["rapor"]), metin, "DEVİR 1 rapor")
    return metin


# ================================================================ DEVİR 2 (2026-11-19): karne v2 (60 bar ambargo, ABD / AVR ayrı, bootstrap, L3O, K1 tabaka)
# Kodlayıcı alt ajan; iş tanımı: workflow DEVİR 2 (Y2_* web entegrasyon adayları F43-F64 + DEVİR 1 YENİDEN W1 / W2 / W2D, devir1_esik.json AYNEN).
# Yalnız ekleme: Y1-Y12 eşikleri ve DEVİR 1 (YH_ESIK_D1, devir1_esik.json, ozellik_Y1_d1.csv.gz) değişmez (regresyon kapısı yh_d2_kapi).
# Not: DEVİR 1 F30-F42 kodlarını kullandı (ozellik_Y1_d1); DEVİR 2 yeni ölçüleri çakışmasın diye F43'ten başlar. Ad: yh_devir2_* (yh_devir_ozellik /
# yh_devir_kos DEVİR 1'e ait; üzerine yazılmaz).
_YH_D2_OZ = ["F43", "F44", "F45", "F46", "F47", "F48", "F49", "F50", "F51", "F52", "F53", "F54", "F55", "F56", "F57", "F58", "F59", "F60",
             "F61", "F62", "F63", "F64"]
_YH_D2_BAR = [k for k in _YH_D2_OZ if k not in ("F53", "F54")]          # hisse içi (prefix denetimi); F53 / F54 kesit (aynı gün evren)
YH_D2_DOSYA = {"ozellik": "ozellik_Y1_d2.csv.gz", "denetim": "ozellik_Y1_d2_denetim.json", "esik": "devir2_esik.json",
               "onkayit": "DEVIR_2_ON_KAYIT.md", "sonuc": "devir2_sonuc.json", "rapor": "DEVIR_2_RAPOR.md", "hata": "devir2_hata.json"}

YH_ESIK_D2: Dict[str, Any] = {
    "surum": "D2.0",
    "taban": "YH_ESIK / YH_ESIK6 / YH_ESIK7 AYNEN (ON_KAYIT_5 / 6 / 7 mührü); DEVİR 1 YH_ESIK_D1 + devir1_esik.json + ozellik_Y1_d1.csv.gz AYNEN; "
             "ölçü satırları olay_Y1.csv.gz (sha)",
    "pencere": {"pp": 10, "sma_kisa": 10, "sma_uzun": 50, "kutu": 20, "kutu_gecmis": 252, "kutu_min": 200, "pivot": 6, "rvol": 14, "rvol_min": 10,
                "atr": 14, "atr_min_oran": 0.01, "kesit_ilk": 20, "nr7": 7, "nr4": 4, "trend": 20, "vcp_gun": 120, "vcp_atr_kat": 1.5,
                "vcp_oran": 0.70, "vcp_ilk": 10.0, "vcp_ilk_kucuk": 5.0, "vcp_son": 15.0, "vcp_bar": 5, "vcp_hacim": 50},
    "ozellik": {
        "F43": "Y2_PP pocket pivot (filtresiz, ana): 1 eğer C_t > C_t-1 ve V_t > max{V_i: i in [t-10, t-1], C_i < C_i-1} (kesin büyük); C_t <= C_t-1 "
               "ise 0; yukarı gün ama pencerede düşüş günü yoksa NaN; t-11'den geçmiş yoksa NaN",
        "F44": "Y2_PPR = V_t / max(düşüş günü V, [t-10, t-1]) (sürekli; düşüş günü yoksa NaN; yukarı gün şartı YOK)",
        "F45": "Y2_PP LuxAlgo filtreli (bilgi): F43 = 1 VE C_t > SMA50_t VE L_t <= max(SMA10_t, 1,02 x SMA50_t) VE C_t > SMA10_t; SMA50 için 50 bar yoksa NaN",
        "F46": "Y2_YUZDELIK: P_s = (max H - min L) / min L, kutu [s-19, s]; F46 = (#{P_s < P_t} + 0,5 x #{P_s = P_t}) / M, s in [t-251, t] "
               "(t dahil, s-19 >= 0); M < 200 ise NaN",
        "F47": "Y2_KAYMA = |C_t - C_t-19| / (max H - min L) (kutu [t-19, t])",
        "F48": "Y2_ARALIK_CV = std(H-L) / ort(H-L), kutu [t-19, t] (ddof 0)",
        "F49": "Y2_TEK_GUN_PAYI = max(H-L) / (max H - min L), kutu [t-19, t]",
        "F50": "Y2_DUZ_TAVAN: pivot tepe j = H_j = max H[j-6, j+6] ve H_j > max H[j-6, j-1]; onaylı pivot j + 6 <= t; bölge pivotları j in [sol, t-6]; "
               "a, c = son iki onaylı pivot (a önce); 1 eğer |a - c| <= ort(H-L)[idx a .. idx c] VE C_t-1 <= max(a, c); ikiden az pivot ise 0",
        "F51": "Y2_TAVAN_FARK = |a - c| / ort(H-L)[idx a .. idx c] (sürekli; ikiden az pivot NaN)",
        "F52": "Y2_RVOL14: R_t = V_t / ort(V_t-14..t-1) (geçerli bar; t < 14 ise NaN; ort 0 ise NaN)",
        "F53": "Y2_KESIT_SIRA: aynı tarih, aynı pazar evreninde (V_<pazar>.pkl o gün geçerli barı olan hisseler; evren_bas sonrası) ATR14/C > %1 "
               "olanlar içinde R_t'ye göre azalan sıra (1 = en yüksek; eşitlik 'min'); olay hissesi ATR filtresini geçmezse NaN",
        "F54": "Y2_KESIT_YUZDE: R_t'nin aynı gün aynı pazar bütün evren içindeki yüzdelik sırası (ortalama sıra / sayı; bilgi)",
        "F55": "Y2_ATRP = ort(TR_j, j in [t-13, t]) / C_t; TR_j = max(H_j, C_j-1) - min(L_j, C_j-1); t < 14 ise NaN",
        "F56": "Y2_NR7 (t-1): R_i = H_i - L_i; 1 eğer R_t-1 = min(R_t-7..t-1) (eşitlik dahil); t < 8 ise NaN",
        "F57": "Y2_IDNR4 (t-1): 1 eğer R_t-1 = min(R_t-4..t-1) VE H_t-1 < H_t-2 VE L_t-1 > L_t-2",
        "F58": "Y2_ONCEKI_TREND_ASAGI = 1 eğer C_t-1 < C_t-21 (bilgi tabakası; t < 21 ise NaN)",
        "F59": "Y2_NR7 (t; bilgi): 1 eğer R_t = min(R_t-6..t)",
        "F60": "Y2_VCP (kaynak, ilk derinlik >= %10): ZigZag (H / L, dönüş eşiği 1,5 x ATR14_j) pencere [t-120, t-1]; yalnız ONAYLI pivotlar (dönüş "
               "görülen; son açık salınım girmez); daralmalar = ardışık (tepe -> sonraki dip) çiftleri, penceredeki EN YÜKSEK tepe pivotundan başlar; "
               "d_k = 100 (H_k - L_k) / H_k; 1 eğer n >= 2 VE d_1 >= 10 VE her d_k+1 <= 0,70 d_k VE her daralma (dip idx - tepe idx) >= 5 bar VE "
               "d_n <= 15 VE ort V[son daralma] < ort V[t-50, t-1]; değilse 0; t-120 < 14 ise NaN",
        "F61": "Y2_VCP5 (bilgi): F60 ile aynı, ilk derinlik >= %5",
        "F62": "Y2_VCP_ORAN = d_n / d_1 (n >= 2; değilse NaN)",
        "F63": "Y2_VCP_N = daralma sayısı n (bilgi)",
        "F64": "Y2_KIRILIM_HACMI = V_t / ort V[t-50, t-1] (bilgi; kaynakta alım şartı >= 1,5)"},
    "ceyrek": {"alt": 0.25, "ust": 0.75, "yon1": ["2016-22"], "yon2": ["2023", "2024-26"],
               "tanim": "kaynakta eşik olmayan adaylar (F44 q75, F47 / F48 / F49 q25, F52 q75) için PAZAR içinde bütün Y1 olaylarının sonlu "
                        "değerlerinden (getirisiz); YÖN 1 eğitim 2016-22, YÖN 2 (ters yürüyen, BİLGİ) 2023-26; KOL-B aynı eşikler; devir2_esik.json"},
    "d1_esik": "W1 / W2 / W2D (DEVİR 1 YENİDEN) eşikleri devir1_esik.json'dan AYNEN (esik_d1_sha = YH_ESIK_D1 sha; yeni eşik seçilmez)",
    "aday": {
        "PP":    {"kaynak": "Y2_PP_HACIM", "tur": "ana", "kural": [["F43", "==", 1.0]], "ad": "Pocket pivot (filtresiz): yukarı gün hacmi > son 10 gün en büyük düşüş günü hacmi", "kapali": True},
        "PPq":   {"kaynak": "Y2_PP_HACIM", "tur": "bilgi", "kural": [["F44", ">=", "q75"]], "ad": "PPR üst çeyrek"},
        "PPb":   {"kaynak": "Y2_PP_HACIM", "tur": "bilgi", "kural": [["F45", "==", 1.0]], "ad": "Pocket pivot LuxAlgo filtreli"},
        "PPt":   {"kaynak": "Y2_PP_HACIM", "tur": "ters", "kural": [["F43", "==", 0.0]], "ad": "ters: pocket pivot değil"},
        "AY":    {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "ana", "kural": [["F46", "<=", 0.10]], "ad": "20 günlük kutu yüzdeliği <= %10 (nadir sıkışma)"},
        "AYK":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "ana", "kural": [["F47", "<=", "q25"]], "ad": "KAYMA alt çeyrek (yatay kutu)"},
        "AY5":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "bilgi", "kural": [["F46", "<=", 0.05]], "ad": "yüzdelik <= %5"},
        "AY2":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "bilgi", "kural": [["F46", "<=", 0.02]], "ad": "yüzdelik <= %2"},
        "AYKK":  {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "bilgi", "kural": [["F46", "<=", 0.10], ["F47", "<=", "q25"]], "ad": "nadir VE yatay"},
        "AYC":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "bilgi", "kural": [["F48", "<=", "q25"]], "ad": "aralık CV alt çeyrek"},
        "AYT":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "bilgi", "kural": [["F49", "<=", "q25"]], "ad": "tek gün payı alt çeyrek"},
        "AYt":   {"kaynak": "Y2_ARALIK_YUZDELIK_KAYMA", "tur": "ters", "kural": [["F46", ">=", 0.90]], "ad": "ters: yüzdelik >= %90 (geniş kutu)"},
        "DT":    {"kaynak": "Y2_DUZ_TAVAN_ABL", "tur": "ana", "kural": [["F50", "==", 1.0]], "ad": "düz tavan: son iki pivot tepe farkı <= 1 x ort(H-L)"},
        "DT05":  {"kaynak": "Y2_DUZ_TAVAN_ABL", "tur": "bilgi", "kural": [["F51", "<=", 0.5]], "ad": "tavan farkı <= 0,5 x ort(H-L)"},
        "DT2":   {"kaynak": "Y2_DUZ_TAVAN_ABL", "tur": "bilgi", "kural": [["F51", "<=", 2.0]], "ad": "tavan farkı <= 2 x ort(H-L)"},
        "DTt":   {"kaynak": "Y2_DUZ_TAVAN_ABL", "tur": "ters", "kural": [["F50", "==", 0.0]], "ad": "ters: düz tavan yok"},
        "RV":    {"kaynak": "Y2_RVOL14_KESIT", "tur": "ana", "kural": [["F52", ">=", 1.0], ["F53", "<=", 20.0], ["F55", ">", 0.01]],
                  "ad": "RVOL14 >= 1 VE günün ilk 20'si (ATR/C > %1 evreninde)", "kapali": True},
        "RVq":   {"kaynak": "Y2_RVOL14_KESIT", "tur": "bilgi", "kural": [["F52", ">=", "q75"]], "ad": "RVOL14 üst çeyrek"},
        "RVt":   {"kaynak": "Y2_RVOL14_KESIT", "tur": "ters", "kural": [["F52", "<", 1.0]], "ad": "ters: RVOL14 < 1"},
        "NR7":   {"kaynak": "Y2_NR7_IDNR4", "tur": "ana", "kural": [["F56", "==", 1.0]], "ad": "kırılım öncesi bar NR7"},
        "NR7a":  {"kaynak": "Y2_NR7_IDNR4", "tur": "bilgi", "kural": [["F56", "==", 1.0], ["F58", "==", 1.0]], "ad": "NR7 VE önceki trend aşağı"},
        "NR7y":  {"kaynak": "Y2_NR7_IDNR4", "tur": "bilgi", "kural": [["F56", "==", 1.0], ["F58", "==", 0.0]], "ad": "NR7 VE önceki trend yukarı"},
        "IDNR4": {"kaynak": "Y2_NR7_IDNR4", "tur": "bilgi", "kural": [["F57", "==", 1.0]], "ad": "kırılım öncesi bar ID/NR4"},
        "NR7t":  {"kaynak": "Y2_NR7_IDNR4", "tur": "ters", "kural": [["F56", "==", 0.0]], "ad": "ters: NR7 değil"},
        "VCP":   {"kaynak": "Y2_VCP_ORAN", "tur": "ana", "kural": [["F60", "==", 1.0]], "ad": "VCP (kaynak eşikleri; ilk derinlik >= %10)"},
        "VCP5":  {"kaynak": "Y2_VCP_ORAN", "tur": "bilgi", "kural": [["F61", "==", 1.0]], "ad": "VCP ilk derinlik >= %5 (küçük yapı)"},
        "VCPt":  {"kaynak": "Y2_VCP_ORAN", "tur": "ters", "kural": [["F60", "==", 0.0]], "ad": "ters: VCP değil"},
        "W1":    {"kaynak": "DEVİR 1 YENİDEN W1", "tur": "ana", "kural": [["F30", "<", 1.0], ["F30", "<=", "q25"]], "esik": "d1", "ad": "DEVİR 1 YENİDEN: CS spread daraldı"},
        "W1t":   {"kaynak": "DEVİR 1 YENİDEN W1", "tur": "ters", "kural": [["F30", ">=", "q75"]], "esik": "d1", "ad": "ters: spread üst çeyrek"},
        "W2":    {"kaynak": "DEVİR 1 YENİDEN W2", "tur": "ana", "kural": [["F31", ">", 0.0], ["F31", ">=", "q75"]], "esik": "d1", "ad": "DEVİR 1 YENİDEN: gün-içi birikim B > 0 ve üst çeyrek"},
        "W2t":   {"kaynak": "DEVİR 1 YENİDEN W2", "tur": "ters", "kural": [["F31", "<=", "q25"]], "esik": "d1", "ad": "ters: B alt çeyrek"},
        "W2D":   {"kaynak": "DEVİR 1 YENİDEN W2", "tur": "ana", "kural": [["F32", ">=", "q75"]], "esik": "d1", "ad": "DEVİR 1 YENİDEN: D = gece - gün-içi üst çeyrek"},
        "W2Dt":  {"kaynak": "DEVİR 1 YENİDEN W2", "tur": "ters", "kural": [["F32", "<=", "q25"]], "esik": "d1", "ad": "ters: D alt çeyrek"}},
    "kol": {"A": "Y1 (bütün olay_Y1.csv.gz satırları)", "B": "Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; olay_Y9.csv.gz ile küme eşitliği)"},
    "donem": {"egitim": ["2016-22"], "sinama": ["2023", "2024-26"]},
    "ambargo": {"bar": 60, "tanim": "pazar takvimi = V_<pazar>.pkl geçerli barlarının birleşimi; YÖN 1: sınama (2023-26) olayı giriş sırası - eğitim "
                                    "(2016-22) son giriş sırası >= 60 bar; YÖN 2 (BİLGİ): eğitim (2023-26) ilk giriş sırası - sınama (2016-22) olayı "
                                    "giriş sırası >= 60 bar; kol tabanı aynı ambargoyla"},
    "pazar": ["ABD+AVR", "ABD", "AVR", "BIST"], "karar_pazar": ["ABD", "AVR"], "n_min": 30,
    "boot": {"B": 2000, "q": 0.025, "tohum": 1120, "birim": "giriş ayı (YYYY-MM)"},
    "l3o": "hücrede tek tek çıkarıldığında MARJ'ı en çok düşüren 3 ay birlikte çıkarılır; kalan MARJ > 0 olmalı",
    "tabaka": {"oz": ["F10", "F15", "F7"], "q": [1 / 3, 2 / 3],
               "tanim": "tercil sınırları pazar içinde 2016-22 bütün Y1 olaylarından (getirisiz; ozellik_Y1.csv.gz); her ana aday için MARJ (aday VE kol "
                        "VE tabaka) - (kol VE tabaka) ABD+AVR havuzunda eğitim ve sınama hücrelerinde; n >= 30 olan bir tabakada MARJ <= 0 ise "
                        "KATKI+ -> SORGULA ('K1 tabaka')"},
    "olcu": "1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): n = h5 ve es_h5 olan olay; FARK = ort h5 - ort es_h5 "
            "(aynı gün aynı OC kovası eşleri); MARJ = FARK(aday VE kol) - FARK(kol), aynı pazar x hücre (aynı ambargo); stop: ort st5 / ort es_st5",
    "etiket": "KARNE v2 (yalnız 'ana' adaylar): KATKI+ = ABD ve AVR AYRI AYRI, eğitim (2016-22) ve sınama (2023-26, ambargolu) dört hücrenin her "
              "birinde n >= 30 VE FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; "
              "ayrıca K1 tabaka şartı; KATKI− = dört hücrede n >= 30 VE MARJ < 0; değilse SORGULA. Ters yön (YÖN 2) hücresi ve 'bilgi' / 'ters' "
              "adaylar yalnız BİLGİ (bağımsız sayılmaz). BIST ve ABD+AVR bilgi (tabaka hariç)",
    "kapali": "PP ve RV 'giriş zamanlaması / onay / hacim' kapalı konusuna dokunur (COL_OZET): sonuç yapı ölçüsü olarak raporlanır; KATKI+ çıksa bile "
              "üretime / kurala girmeden ana model ve Cemal onayı gerekir",
    "prefix": {"n": 25, "tohum": 1219},
    "coklu": "10 ana aday x 2 kol = 20 karar satırı: BH uygulanmaz (dört hücre + bootstrap + L3O + tabaka ikili kuralı); şansla KATKI+ notu raporda",
    "yeniden_uretim": [["AY", "A", "ABD", "sinama"], ["W2", "B", "AVR", "egitim"]],
}

YH_KONTROL_D2: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "olay ve eş olay_Y1.csv.gz'den (aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar takip "
                   "geometrisi); MARJ kol tabanına göre (Y1 / Y9) aynı pazar x hücre x ambargo; K1 TABAKALI koşulur: her ana aday MARJ'ı F10, F15, F7 "
                   "tercil tabakalarında (sınırlar devir2_esik.json, 2016-22 getirisiz) ölçülür, n >= 30 tabakada MARJ <= 0 -> SORGULA; mekanik ilişki "
                   "Spearman tablosu (F3 / F10 / F13 / F15) ön kayıtta; RV kesit sırası aynı gün eşlerinden bağımsız değil (eşler aynı günün hisseleri) -> raporda"),
    "K2": ("EVET", "F43-F64 yalnız [.., t] barları (t = sinyal günü kapanışı, giriş t+1 açılış); pivot onayı j+6 <= t; ZigZag yalnız onaylı pivot; "
                   "yh_d2_bar dizileri t+1'de keser; yh_devir2_ozellik_yaz pazar başına 25 rastgele olayda veri t'de kesilince aynı değer (DURUR) ve "
                   "panel R (kesit) = olay R (DURUR); kesit evreni o günün geçerli barları (evren_bas sonrası); eşikler getirisiz, ön kayıtta mühürlü"),
    "K3": ("EVET", "geçerli bar süzgeci _yh_hazir (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); pencereler geçerli bar sayımıyla; kesit "
                   "evreninde o gün geçerli barı olmayan hisse yok; hacim 0 bar veri dizisinde yok"),
    "K4": ("EVET", "Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç yalnız seçer; FARK ortalama, P olay / P eş ayrı"),
    "K5": ("EVET", "giriş t+1 açılışı (olay_Y1 E0); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA)"),
    "K6": ("EVET", "aynı V_*.pkl tek kip (Yahoo düzeltilmiş); yeni ölçüler oran / pay / sıra / ikili (birimsiz); AVR yerel para ama hepsi hisse içi "
                   "oran; RV kesit sırası oranla (birimden bağımsız)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (batanlar yok): P olay ve P eş yukarı yanlı, FARK'ta kısmen götürür; kesit evreni de bugünün "
                   "listesi (geçmiş günlerin batan hisseleri sırada yok) -> RV ilk-20 sırası yanlı; rapora yazılır"),
    "K8": ("EVET", "hücre n < 30 SORGULA (ölçülemedi); ABD ve AVR ayrı, eğitim + sınama dört hücre aynı yön şartı; 20 karar satırı BH yok -> şans notu; "
                   "ABD / AVR 2023-26 önceki turlarda görüldü (bakılmış) -> KATKI+ en fazla EMARE düzeyi; küçük n bulgu değil"),
    "K9": ("EVET", "DEVIR_2_ON_KAYIT.md: YH_ESIK_D2_SHA, YH_ESIK / 6 / 7 / D1 sha, kod / özellik d2 / eşik json d2 / d1 özellik / d1 eşik json / "
                   "olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d2_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i "
                   "('DEVİR 2 ön kayıt') koşudan önce; eşik sonuca göre oynanmaz; ikinci koşu DURUR"),
    "K10": ("UYGULANMAZ", "haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları"),
    "K11": ("EVET", "devir2_sonuc.json + ozellik_Y1_d2.csv.gz + olay_Y1.csv.gz; DEVIR_2_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (AY A ABD sınama, W2 B "
                    "AVR eğitim) ayrı kodla (_yh_d2_yeniden: düz pandas sorgusu + kendi ambargo hesabı) yeniden üretilir; fark > 1e-12 ise DURUR"),
    "K12": ("EVET", "etiket yalnız karne v2 kuralı (KATKI+ / KATKI− / SORGULA / BİLGİ); 'iz / emare' denmez; FARK yüzde puan; h5 hedef payı (stop'tan "
                    "önce +%5), getiri değil; sayı ile yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı korundu (yeni adlar yh_d2_ / yh_devir2_ / YH_ESIK_D2 / _YH_D2 önekli; DEVİR 1 adları ezilmez); yasak defter "
                    "dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; "
                    "kod değişti -> Colab'da 'çalışma zamanını yeniden başlat'; PP / RV kapalı konuya dokunur -> raporda onay notu"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi"),
}


def yh_esik_d2_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return yh_esik_sha(YH_ESIK_D2 if E is None else E)


def _yh_d2_zigzag(H: np.ndarray, L: np.ndarray, atr: np.ndarray, a: int, b: int, kat: float) -> List[Tuple[str, int, float]]:
    """ZigZag (H / L) barlar [a, b] (b dahil); dönüş eşiği kat x atr[j]. Yalnız ONAYLI pivotlar döner (dönüş görülen): [(tür 'H'/'L', idx, fiyat)].
    Pivot j'nin onayı j'den sonraki bir bar k <= b'de; k > b bilgisi kullanılmaz."""
    piv: List[Tuple[str, int, float]] = []
    if b - a < 2:
        return piv
    mod = 0; hi, hi_i, lo, lo_i = H[a], a, L[a], a
    for j in range(a + 1, b + 1):
        th = kat * atr[j]
        if not np.isfinite(th):
            continue
        if mod >= 0 and H[j] > hi:
            hi, hi_i = H[j], j
        if mod <= 0 and L[j] < lo:
            lo, lo_i = L[j], j
        if mod == 0:
            if hi - L[j] >= th and hi_i < j:
                piv.append(("H", hi_i, float(hi))); mod = -1; lo, lo_i = L[j], j
            elif H[j] - lo >= th and lo_i < j:
                piv.append(("L", lo_i, float(lo))); mod = 1; hi, hi_i = H[j], j
        elif mod == 1:
            if hi - L[j] >= th:
                piv.append(("H", hi_i, float(hi))); mod = -1; lo, lo_i = L[j], j
        else:
            if H[j] - lo >= th:
                piv.append(("L", lo_i, float(lo))); mod = 1; hi, hi_i = H[j], j
    return piv


def yh_d2_vcp(H: np.ndarray, L: np.ndarray, V: np.ndarray, atr: np.ndarray, i: int, E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, float]:
    """F60-F63 (VCP); pencere [i-120, i-1], ATR dizisi nedensel (atr[j] yalnız <= j)."""
    P = E["pencere"]; out = {"F60": np.nan, "F61": np.nan, "F62": np.nan, "F63": np.nan}
    a = i - int(P["vcp_gun"]); b = i - 1
    if a < int(P["atr"]) or i - int(P["vcp_hacim"]) < 0:
        return out
    piv = _yh_d2_zigzag(H, L, atr, a, b, float(P["vcp_atr_kat"]))
    tep = [k for k, p in enumerate(piv) if p[0] == "H"]
    d: List[float] = []; bar: List[int] = []; vol_ok = False
    if tep:
        k0 = max(tep, key=lambda k: (piv[k][2], -k))          # en yüksek tepe (eşitlikte ilk)
        k = k0
        while k + 1 < len(piv):
            if piv[k][0] == "H" and piv[k + 1][0] == "L":
                hh, hi_i = piv[k][2], piv[k][1]; ll, lo_i = piv[k + 1][2], piv[k + 1][1]
                d.append(100.0 * (hh - ll) / hh); bar.append(lo_i - hi_i)
                last = (hi_i, lo_i)
            k += 1
        if d:
            vol_ok = bool(np.mean(V[last[0]:last[1] + 1]) < np.mean(V[i - int(P["vcp_hacim"]):i]))
    n = len(d); out["F63"] = float(n)
    if n >= 2:
        out["F62"] = d[-1] / d[0]
    base = (n >= 2 and all(d[k + 1] <= float(P["vcp_oran"]) * d[k] for k in range(n - 1)) and all(x >= int(P["vcp_bar"]) for x in bar)
            and d[-1] <= float(P["vcp_son"]) and vol_ok)
    out["F60"] = 1.0 if base and d[0] >= float(P["vcp_ilk"]) else 0.0
    out["F61"] = 1.0 if base and d[0] >= float(P["vcp_ilk_kucuk"]) else 0.0
    return out


def _yh_d2_atr(H: np.ndarray, L: np.ndarray, C: np.ndarray, k: int) -> np.ndarray:
    """ATR_k (basit ortalama TR, [j-k+1, j]); TR_j = max(H_j, C_j-1) - min(L_j, C_j-1); j < k NaN. Nedensel."""
    Cp = np.r_[np.nan, C[:-1]]
    tr = np.fmax(H, Cp) - np.fmin(L, Cp); tr[0] = np.nan
    out = np.full(len(H), np.nan)
    if len(H) > k:
        cs = np.cumsum(np.r_[0.0, np.nan_to_num(tr)])
        j = np.arange(k, len(H)); out[j] = (cs[j + 1] - cs[j + 1 - k]) / k
    return out


def yh_d2_bar(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray, i: int, sol: int,
              E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, float]:
    """t = i (geçerli bar sırası), bölge [sol, i-1]: F43-F52, F55-F64. Yalnız [0, i] okunur (t+1 ve sonrası kesilir)."""
    P = E["pencere"]; out = {k: np.nan for k in _YH_D2_BAR}
    O, H, L, C, V = (np.asarray(x[:i + 1], float) for x in (O, H, L, C, V))
    R = H - L
    # PP (F43-F45)
    w = int(P["pp"])
    if i >= w + 1:
        jj = np.arange(i - w, i); dn = C[jj] < C[jj - 1]
        mx = float(V[jj][dn].max()) if dn.any() else np.nan
        out["F44"] = V[i] / mx if np.isfinite(mx) and mx > 0 else np.nan
        if not C[i] > C[i - 1]:
            out["F43"] = 0.0
        elif np.isfinite(mx):
            out["F43"] = 1.0 if V[i] > mx else 0.0
        su, sk = int(P["sma_uzun"]), int(P["sma_kisa"])
        if i >= su - 1 and np.isfinite(out["F43"]):
            s50 = float(np.mean(C[i - su + 1:i + 1])); s10 = float(np.mean(C[i - sk + 1:i + 1]))
            out["F45"] = 1.0 if (out["F43"] == 1.0 and C[i] > s50 and L[i] <= max(s10, 1.02 * s50) and C[i] > s10) else 0.0
    # kutu (F46-F49)
    N = int(P["kutu"]); G = int(P["kutu_gecmis"])
    if i >= N - 1:
        a = i - N + 1; mh, ml = float(H[a:i + 1].max()), float(L[a:i + 1].min()); kb = mh - ml
        if kb > 0:
            out["F47"] = abs(C[i] - C[a]) / kb; out["F49"] = float(R[a:i + 1].max()) / kb
        mr = float(R[a:i + 1].mean())
        if mr > 0:
            out["F48"] = float(R[a:i + 1].std()) / mr
        s0 = max(N - 1, i - G + 1)
        if i - s0 + 1 >= int(P["kutu_min"]):
            from numpy.lib.stride_tricks import sliding_window_view as _sw
            hh = _sw(H[s0 - N + 1:i + 1], N).max(axis=1); ll = _sw(L[s0 - N + 1:i + 1], N).min(axis=1)
            Pb = (hh - ll) / ll; pt = Pb[-1]
            out["F46"] = (float(np.sum(Pb < pt)) + 0.5 * float(np.sum(Pb == pt))) / len(Pb)
    # düz tavan (F50 / F51)
    pv = int(P["pivot"])
    if 0 < sol <= i:
        piv = []
        for j in range(max(sol, pv), i - pv + 1):
            hj = H[j]
            if hj >= H[j - pv:j + pv + 1].max() and hj > H[j - pv:j].max():
                piv.append(j)
        if len(piv) >= 2:
            ja, jc = piv[-2], piv[-1]; a_, c_ = H[ja], H[jc]; mr = float(R[ja:jc + 1].mean())
            out["F51"] = abs(a_ - c_) / mr if mr > 0 else np.nan
            out["F50"] = 1.0 if (np.isfinite(out["F51"]) and out["F51"] <= 1.0 and C[i - 1] <= max(a_, c_)) else 0.0
        else:
            out["F50"] = 0.0
    # RVOL / ATR (F52, F55)
    rv = int(P["rvol"])
    if i >= rv:
        m = float(np.mean(V[i - rv:i]))
        out["F52"] = V[i] / m if m > 0 else np.nan
    atr = _yh_d2_atr(H, L, C, int(P["atr"]))
    if np.isfinite(atr[i]):
        out["F55"] = atr[i] / C[i]
    # NR7 / IDNR4 (F56-F59)
    n7, n4 = int(P["nr7"]), int(P["nr4"])
    if i >= n7 + 1:
        out["F56"] = 1.0 if R[i - 1] <= R[i - n7:i].min() else 0.0
        out["F57"] = 1.0 if (R[i - 1] <= R[i - n4:i].min() and H[i - 1] < H[i - 2] and L[i - 1] > L[i - 2]) else 0.0
        out["F59"] = 1.0 if R[i] <= R[i - n7 + 1:i + 1].min() else 0.0
    tr_ = int(P["trend"])
    if i >= tr_ + 1:
        out["F58"] = 1.0 if C[i - 1] < C[i - 1 - tr_] else 0.0
    # VCP (F60-F63), kırılım hacmi (F64)
    out.update(yh_d2_vcp(H, L, V, atr, i, E))
    hv = int(P["vcp_hacim"])
    if i >= hv:
        m = float(np.mean(V[i - hv:i]))
        out["F64"] = V[i] / m if m > 0 else np.nan
    return out


def yh_devir2_ozellik(df: pd.DataFrame, tarihler: List[pd.Timestamp], sol_geri: List[float], hazir: bool = False,
                      E: Dict[str, Any] = YH_ESIK_D2) -> pd.DataFrame:
    """Bir hissenin Y1 günleri için F43-F52, F55-F64 (hisse içi). sol = i - F8 (ozellik_Y1 F8 = t - sol; DEVİR 1'de bütün satırlarda doğrulandı).
    Gün veride yoksa YHHata."""
    d = df if hazir else _yh_hazir(df)
    O, H, L, C, V = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
    pos = d.index.get_indexer(pd.DatetimeIndex(pd.to_datetime(list(tarihler))))
    if (pos < 0).any():
        raise YHHata("DEVİR 2 özellik: sinyal günü geçerli bar değil")
    sat = []
    for i, g in zip(pos, sol_geri):
        i = int(i); sol = i - int(g) if np.isfinite(g) else -1
        sat.append(yh_d2_bar(O, H, L, C, V, i, sol, E))
    return pd.DataFrame(sat, columns=_YH_D2_BAR)


def yh_d2_kesit(Vh: Dict[str, pd.DataFrame], evren_bas: Dict[str, pd.Timestamp], E: Dict[str, Any] = YH_ESIK_D2) -> pd.DataFrame:
    """Pazar paneli: her hisse-gün için R (RVOL14) ve ATR14/C (nedensel, geçerli bar), sonra aynı gün kesit: sira (ATR/C > %1 evreni, azalan,
    'min') ve yuzde (bütün evren, ortalama sıra / sayı). Döner: uzun tablo (sembol, tarih, R, atrp, sira, yuzde)."""
    P = E["pencere"]; rv = int(P["rvol"]); parca = []
    for s, d in Vh.items():
        V = d.Volume.to_numpy(float); H, L, C = (d[c].to_numpy(float) for c in ("High", "Low", "Close"))
        m = pd.Series(V).shift(1).rolling(rv, min_periods=rv).mean().to_numpy()
        with np.errstate(invalid="ignore", divide="ignore"):
            R = np.where(m > 0, V / m, np.nan)
        atrp = _yh_d2_atr(H, L, C, int(P["atr"])) / C
        X = pd.DataFrame({"sembol": s, "tarih": d.index, "R": R, "atrp": atrp})
        b = evren_bas.get(s)
        if b is not None:
            X = X[X.tarih >= pd.Timestamp(b)]
        parca.append(X)
    K = pd.concat(parca, ignore_index=True)
    K = K[np.isfinite(K.R.to_numpy(float))]
    K["yuzde"] = K.groupby("tarih").R.rank(method="average", pct=True)
    f = K.atrp.to_numpy(float) > float(P["atr_min_oran"])
    K["sira"] = np.nan
    K.loc[f, "sira"] = K[f].groupby("tarih").R.rank(method="min", ascending=False)
    return K


_YH_D2_IS_V: Dict[str, pd.DataFrame] = {}


def _yh_d2_isci(is_: Tuple[str, List[pd.Timestamp], List[float]]) -> List[Dict[str, Any]]:
    s, tl, gl = is_
    try:
        R = yh_devir2_ozellik(_YH_D2_IS_V[s], tl, gl, hazir=True)
        return [{"sembol": s, "tarih": pd.Timestamp(t), **r, "_hata": ""} for t, r in zip(tl, R.to_dict("records"))]
    except Exception as ex:
        return [{"sembol": s, "tarih": pd.Timestamp(t), **{k: np.nan for k in _YH_D2_BAR}, "_hata": f"hisse: {ex}"[:200]} for t in tl]


def yh_d2_ambargo_tarih(takvim: pd.DatetimeIndex, g_egitim1: pd.Series, g_egitim2: pd.Series, bar: int) -> Dict[str, str]:
    """YÖN 1: sınama ilk izinli giriş = takvim[sıra(son eğitim girişi) + bar]; YÖN 2: sınama son izinli giriş = takvim[sıra(ilk eğitim girişi) - bar]."""
    T = pd.DatetimeIndex(sorted(set(pd.DatetimeIndex(takvim))))
    s1 = pd.Timestamp(pd.to_datetime(g_egitim1).max()); s2 = pd.Timestamp(pd.to_datetime(g_egitim2).min())
    i1 = int(T.searchsorted(s1)); i2 = int(T.searchsorted(s2))
    if i1 >= len(T) or T[i1] != s1 or i2 >= len(T) or T[i2] != s2:
        raise YHHata("DEVİR 2 ambargo: eğitim giriş günü pazar takviminde yok -> DURDU")
    if i1 + bar >= len(T) or i2 - bar < 0:
        raise YHHata("DEVİR 2 ambargo: takvim yetmiyor -> DURDU")
    return {"yon1_son_egitim_giris": str(s1.date()), "yon1_sinama_ilk_izinli": str(T[i1 + bar].date()),
            "yon2_ilk_egitim_giris": str(s2.date()), "yon2_sinama_son_izinli": str(T[i2 - bar].date())}


def yh_devir2_ozellik_yaz(veri: Optional[str] = None, cikti: Optional[str] = None, islem: int = 1, denetim_n: Optional[int] = None,
                          E: Dict[str, Any] = YH_ESIK_D2, olay_y1: Optional[str] = None, ozellik: Optional[str] = None) -> Dict[str, Any]:
    """Bütün Y1 olayları -> ozellik_Y1_d2.csv.gz (F43-F64) + denetim json (prefix, panel R = olay R, ambargo tarihleri; getirisiz).
    Kapılar: hisse hatası -> DURUR; pazar başına denetim_n rastgele olay veri t'de kesilince aynı (DURUR); kesit paneli R = olay F52 (DURUR)."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D2_DOSYA["ozellik"])
    yo = olay_y1 or os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1"))
    yf = ozellik or YH_YOL["ozellik"]
    for y in (yo, yf):
        if not os.path.exists(y):
            raise YHHata(f"DEVİR 2: dosya yok: {y}")
    K = pd.read_csv(yo, usecols=["pazar", "sembol", "tarih", "giris", "donem"], parse_dates=["tarih", "giris"], dtype={"sembol": str, "pazar": str})
    if K.duplicated(["pazar", "sembol", "tarih"]).any():
        raise YHHata("olay_Y1'de aynı (pazar, sembol, tarih) iki kez")
    F8 = pd.read_csv(yf, usecols=["pazar", "sembol", "tarih", "F8"], parse_dates=["tarih"], dtype={"sembol": str, "pazar": str})
    K = K.merge(F8, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    dn = int(E["prefix"]["n"] if denetim_n is None else denetim_n); sat: List[Dict[str, Any]] = []
    den: Dict[str, Any] = {"surum": YH_SURUM, "esik_d2_sha": yh_esik_d2_sha(E), "olay_y1_sha": _yh_sha_dosya(yo), "pazar": {}, "ambargo": {}}
    for pi, p in enumerate(OC.OC_ESIK["pazar"]):
        Kp = K[K.pazar == p]
        if not len(Kp):
            continue
        Vd = OC.oc_veri(p, klasor=veri or YH_YOL["veri"])
        eksik = sorted(set(Kp.sembol) - set(Vd["V"]))
        if eksik:
            raise YHHata(f"DEVİR 2 özellik: {p} veride olmayan sembol {eksik[:5]}")
        Vh = {s: _yh_hazir(d) for s, d in Vd["V"].items()}
        takvim = pd.DatetimeIndex(sorted(set().union(*[set(d.index) for d in Vh.values()])))
        den["ambargo"][p] = yh_d2_ambargo_tarih(takvim, Kp.giris[Kp.donem.isin(E["donem"]["egitim"])],
                                                Kp.giris[Kp.donem.isin(E["donem"]["sinama"])], int(E["ambargo"]["bar"]))
        isler = [(s, list(g.tarih), list(g.F8.to_numpy(float))) for s, g in Kp.groupby("sembol", sort=True)]
        _YH_D2_IS_V.clear(); _YH_D2_IS_V.update({s: Vh[s] for s, _a, _b in isler})
        if islem > 1:
            import multiprocessing as mp
            with mp.get_context("fork").Pool(islem) as pool:
                parca = pool.map(_yh_d2_isci, isler, chunksize=4)
        else:
            parca = [_yh_d2_isci(x) for x in isler]
        Xp = pd.DataFrame([r for pr in parca for r in pr]); Xp.insert(0, "pazar", p)
        hh = Xp[Xp._hata.str.startswith("hisse")]
        if len(hh):
            raise YHHata(f"DEVİR 2 özellik: {p} hisse hatası {len(hh)} satır, ilk: {hh._hata.iloc[0]} -> DURDU")
        Ks = yh_d2_kesit(Vh, Vd.get("evren_bas", {}), E)
        Z = Xp.merge(Ks[["sembol", "tarih", "R", "sira", "yuzde"]], on=["sembol", "tarih"], how="left", validate="one_to_one")
        a_, b_ = Z.F52.to_numpy(float), Z.R.to_numpy(float)
        bad = ~(np.isclose(a_, b_, rtol=1e-9, atol=1e-12) | (np.isnan(a_) & np.isnan(b_)))
        if bad.any():
            raise YHHata(f"DEVİR 2 özellik: {p} panel R != olay F52 ({int(bad.sum())} satır) -> DURDU")
        Z["F53"] = np.where(Z.F55.to_numpy(float) > float(E["pencere"]["atr_min_oran"]), Z.sira.to_numpy(float), np.nan)
        Z["F54"] = Z.yuzde.to_numpy(float)
        Xp = Z.drop(columns=["R", "sira", "yuzde"])
        rng = np.random.default_rng([int(E["prefix"]["tohum"]), pi]); ok = 0
        for q in rng.choice(len(Xp), min(dn, len(Xp)), replace=False):
            r = Xp.iloc[int(q)]; t = pd.Timestamp(r.tarih); g = float(Kp[(Kp.sembol == r.sembol) & (Kp.tarih == t)].F8.iloc[0])
            kes = Vd["V"][r.sembol]; kes = kes[kes.index <= t]
            a = yh_devir2_ozellik(kes, [t], [g]).iloc[0][_YH_D2_BAR].to_numpy(float)
            c = r[_YH_D2_BAR].to_numpy(float)
            if not np.allclose(a, c, rtol=1e-9, atol=1e-12, equal_nan=True):
                raise YHHata(f"DEVİR 2 prefix denetimi TUTMADI: {p} {r.sembol} {t.date()} -> DURDU")
            ok += 1
        den["pazar"][p] = {"olay": int(len(Xp)), "prefix_tuttu": ok, "kesit_hisse_gun": int(len(Ks)), "takvim_bar": int(len(takvim)),
                           "nan": {k: int(Xp[k].isna().sum()) for k in _YH_D2_OZ}}
        yhlog.info("DEVİR 2 özellik %s: %d olay, prefix %d tuttu", p, len(Xp), ok)
        sat.extend(Xp.to_dict("records")); _YH_D2_IS_V.clear(); del Vd, Vh, Ks
    X = pd.DataFrame(sat)[["pazar", "sembol", "tarih"] + _YH_D2_OZ]
    if len(X) != len(K):
        raise YHHata(f"DEVİR 2 özellik: satır {len(X)} != olay_Y1 {len(K)}")
    X = X.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)
    X.to_csv(yol, index=False, float_format="%.10g", compression="gzip", date_format="%Y-%m-%d")
    den["satir"] = int(len(X)); den["sha"] = _yh_sha_dosya(yol)
    _yh_yaz(os.path.join(cikti, YH_D2_DOSYA["denetim"]), json.dumps(den, ensure_ascii=False, indent=1, default=_yh_json), "DEVİR 2 denetim")
    return {"yol": yol, **den}


def yh_d2_taban(cikti: Optional[str] = None, getiri: bool = False) -> pd.DataFrame:
    """olay_Y1 (kimlik + dönem + giriş; getiri=True ise h5 / es_h5 / st5 / es_st5) ∩ ozellik_Y1_d2 ∩ ozellik_Y1_d1 (F30-F32) ∩ ozellik_Y1
    (F7 / F10 / F15 / F17) + kolA / kolB."""
    cikti = cikti or YH_YOL["cikti"]
    yo = os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1")); y2 = os.path.join(cikti, YH_D2_DOSYA["ozellik"])
    y1 = os.path.join(cikti, YH_D1_DOSYA["ozellik"])
    for y in (yo, y2, y1, YH_YOL["ozellik"]):
        if not os.path.exists(y):
            raise YHHata(f"DEVİR 2: dosya yok: {y}")
    kol = ["pazar", "sembol", "tarih", "giris", "donem"] + (["h5", "es_h5", "st5", "es_st5"] if getiri else [])
    K = pd.read_csv(yo, usecols=kol, parse_dates=["tarih", "giris"], dtype={"sembol": str})
    D = pd.read_csv(y2, parse_dates=["tarih"], dtype={"sembol": str})
    D1 = pd.read_csv(y1, usecols=["pazar", "sembol", "tarih", "F30", "F31", "F32"], parse_dates=["tarih"], dtype={"sembol": str})
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F7", "F10", "F15", "F17"], parse_dates=["tarih"], dtype={"sembol": str})
    M = K.merge(D, on=["pazar", "sembol", "tarih"], how="outer", validate="one_to_one", indicator=True)
    if (M._merge != "both").any():
        raise YHHata(f"DEVİR 2: olay_Y1 ve ozellik_Y1_d2 anahtarları farklı ({int((M._merge != 'both').sum())}) -> DURDU")
    M = M.drop(columns="_merge").merge(D1, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    M = M.merge(G, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
    g2 = YH_ESIK6["grup"]["G2"]
    with np.errstate(invalid="ignore"):
        M["kolB"] = (M.F15.to_numpy(float) <= g2["F15_ust"]) & (M.F17.to_numpy(float) <= g2["F17_ust"])
    M["kolA"] = True
    return M.sort_values(["pazar", "sembol", "tarih"]).reset_index(drop=True)


def yh_d2_esik(M: pd.DataFrame, amb: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, Any]:
    """Getirisiz eşik sözlüğü: çeyrekler (yön x pazar x özellik; yalnız d2 adayları), tabaka tercilleri (2016-22), ambargo tarihleri."""
    Q = E["ceyrek"]; kol = sorted({k[0] for a in E["aday"].values() if a.get("esik") != "d1" for k in a["kural"] if k[2] in ("q25", "q75")})
    out: Dict[str, Any] = {"yon1": {}, "yon2": {}, "tabaka": {}, "ambargo": amb}
    for yon in ("yon1", "yon2"):
        for p in OC.OC_ESIK["pazar"]:
            X = M[(M.pazar == p) & M.donem.isin(Q[yon])]; out[yon][p] = {}
            for c in kol:
                v = X[c].to_numpy(float); v = v[np.isfinite(v)]
                out[yon][p][c] = {"q25": float(np.quantile(v, Q["alt"])) if len(v) else np.nan,
                                  "q75": float(np.quantile(v, Q["ust"])) if len(v) else np.nan, "n": int(len(v))}
    T = E["tabaka"]
    for p in OC.OC_ESIK["pazar"]:
        X = M[(M.pazar == p) & M.donem.isin(E["donem"]["egitim"])]; out["tabaka"][p] = {}
        for c in T["oz"]:
            v = X[c].to_numpy(float); v = v[np.isfinite(v)]
            out["tabaka"][p][c] = [float(np.quantile(v, q)) for q in T["q"]] if len(v) else [np.nan, np.nan]
    return out


def yh_d2_eski_esik_oku(cikti: str) -> Dict[str, Any]:
    """devir1_esik.json (DEVİR 1 YENİDEN eşikleri) AYNEN; esik_d1_sha = YH_ESIK_D1 sha değilse DURUR."""
    y = os.path.join(cikti, YH_D1_DOSYA["esik"])
    if not os.path.exists(y):
        raise YHHata(f"DEVİR 2: devir1_esik.json yok: {y}")
    Q = json.load(open(y, encoding="utf-8"))
    if Q.get("esik_d1_sha") != yh_esik_d1_sha():
        raise YHHata("DEVİR 2: devir1_esik.json esik_d1_sha YH_ESIK_D1 ile aynı değil (DEVİR 1 eşikleri değişmiş) -> DURDU")
    return Q


def yh_d2_maske(M: pd.DataFrame, aday: str, esik: Dict[str, Any], esik_d1: Dict[str, Any], yon: str, E: Dict[str, Any] = YH_ESIK_D2) -> np.ndarray:
    """Aday süzgeci (NaN tutmaz). 'q25' / 'q75' eşikleri: aday 'esik' = 'd1' ise devir1_esik.json, değilse devir2_esik.json (aynı yön, aynı pazar)."""
    A = E["aday"][aday]; Q = esik_d1 if A.get("esik") == "d1" else esik
    m = np.zeros(len(M), bool)
    for p in OC.OC_ESIK["pazar"]:
        pm = (M.pazar == p).to_numpy()
        if not pm.any():
            continue
        mp_ = np.ones(int(pm.sum()), bool)
        for c, op, v in A["kural"]:
            x = M.loc[pm, c].to_numpy(float)
            th = float(Q[yon][p][c][v]) if isinstance(v, str) else float(v)
            with np.errstate(invalid="ignore"):
                mp_ &= ~np.isnan(x) & _YH_D1_OP[op](x, th)
        m[pm] = mp_
    return m


def yh_d2_hucre_maske(M: pd.DataFrame, esik: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, np.ndarray]:
    """Hücre maskeleri (pazar başına ambargo tarihleriyle): egitim (2016-22), sinama (2023-26 VE giriş >= YÖN 1 ilk izinli), ters (2016-22 VE giriş
    <= YÖN 2 son izinli; BİLGİ)."""
    Dn = E["donem"]; g = pd.to_datetime(M.giris).to_numpy("datetime64[D]")
    eg = M.donem.isin(Dn["egitim"]).to_numpy(); si = M.donem.isin(Dn["sinama"]).to_numpy()
    s_ok = np.zeros(len(M), bool); t_ok = np.zeros(len(M), bool)
    for p, a in esik["ambargo"].items():
        pm = (M.pazar == p).to_numpy()
        s_ok |= pm & (g >= np.datetime64(a["yon1_sinama_ilk_izinli"])); t_ok |= pm & (g <= np.datetime64(a["yon2_sinama_son_izinli"]))
    return {"egitim": eg, "sinama": si & s_ok, "ters": eg & t_ok}


def yh_d2_huni(M: pd.DataFrame, esik: Dict[str, Any], esik_d1: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, Any]:
    """Getirisiz huni: aday x kol x pazar x dönem (YÖN 1 eşikleri) + sınama ambargo sonrası (amb) + taban."""
    dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]; hm = yh_d2_hucre_maske(M, esik, E); out: Dict[str, Any] = {}
    for kol in ("A", "B"):
        km = M[f"kol{kol}"].to_numpy(bool)
        for a in ["taban"] + list(E["aday"]):
            am = km & (yh_d2_maske(M, a, esik, esik_d1, "yon1", E) if a != "taban" else True)
            r = {f"{p}|{q}": int((am & (M.pazar == p).to_numpy() & (M.donem == q).to_numpy()).sum()) for p in OC.OC_ESIK["pazar"] for q in dn}
            r.update({f"{p}|amb": int((am & (M.pazar == p).to_numpy() & hm["sinama"]).sum()) for p in OC.OC_ESIK["pazar"]})
            out[f"{a}|{kol}"] = r
    return out


def yh_d2_spearman(M: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """Getirisiz mekanik ilişki (K1): F44, F46-F49, F51, F52, F54, F55, F62, F64 ile F3 / F10 / F13 / F15 Spearman (bütün Y1)."""
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F3", "F13"], parse_dates=["tarih"], dtype={"sembol": str})
    X = M.merge(G, on=["pazar", "sembol", "tarih"], how="left"); out: Dict[str, Dict[str, float]] = {}
    for c in ["F44", "F46", "F47", "F48", "F49", "F51", "F52", "F54", "F55", "F62", "F64"]:
        out[c] = {}
        for r in ("F3", "F10", "F13", "F15"):
            Z = X[[c, r]].replace([np.inf, -np.inf], np.nan).dropna()
            out[c][r] = float(Z[c].rank().corr(Z[r].rank())) if len(Z) > 30 else np.nan
    return out


def _yh_d2_sha(cikti: str) -> Dict[str, str]:
    out = {"esik_d2": yh_esik_d2_sha(), "esik_d1": yh_esik_d1_sha(), "esik": yh_esik_sha(), "esik6": yh_esik6_sha(), "esik7": yh_esik7_sha(),
           "kod": _yh_sha_dosya(YH_YOL["kod"])}
    for ad, yol in (("ozellik_d2", os.path.join(cikti, YH_D2_DOSYA["ozellik"])), ("esik_json_d2", os.path.join(cikti, YH_D2_DOSYA["esik"])),
                    ("ozellik_d1", os.path.join(cikti, YH_D1_DOSYA["ozellik"])), ("esik_json_d1", os.path.join(cikti, YH_D1_DOSYA["esik"])),
                    ("y1olay", os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1"))), ("y9olay", os.path.join(cikti, YH_DOSYA["satir"].format(d="Y9"))),
                    ("ozellik", YH_YOL["ozellik"])):
        if not os.path.exists(yol):
            raise YHHata(f"DEVİR 2: dosya yok: {yol}")
        out[ad] = _yh_sha_dosya(yol)
    return out


_YH_D2_DESEN = {"esik_d2": r"YH_ESIK_D2_SHA:\s*`([0-9a-f]{64})`", "esik_d1": r"YH_ESIK_D1_SHA:\s*`([0-9a-f]{64})`",
                "esik": r"(?<![A-Z0-9_])YH_ESIK_SHA:\s*`([0-9a-f]{64})`", "esik6": r"YH_ESIK6_SHA:\s*`([0-9a-f]{64})`",
                "esik7": r"YH_ESIK7_SHA:\s*`([0-9a-f]{64})`", "kod": r"YH_KOD_SHA:\s*`([0-9a-f]{64})`",
                "ozellik_d2": r"D2_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "esik_json_d2": r"D2_ESIK_JSON_SHA:\s*`([0-9a-f]{64})`",
                "ozellik_d1": r"D1_OZELLIK_SHA:\s*`([0-9a-f]{64})`", "esik_json_d1": r"D1_ESIK_JSON_SHA:\s*`([0-9a-f]{64})`",
                "y1olay": r"Y1_OLAY_SHA:\s*`([0-9a-f]{64})`", "y9olay": r"Y9_OLAY_SHA:\s*`([0-9a-f]{64})`",
                "ozellik": r"(?<![A-Z0-9_])OZELLIK_SHA:\s*`([0-9a-f]{64})`", "zaman": _YH_KAPI_DESEN["zaman"]}


def _yh_d2_regresyon(cikti: str, M: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """Regresyon kapısı: DEVİR 1 kapısı (YH_ESIK / 6 / 7 = ON_KAYIT_5 / 6 / 7; KOL-B = olay_Y9) + YH_ESIK_D1 = DEVIR_1_ON_KAYIT mührü +
    devir1_esik.json sha = DEVIR_1_ON_KAYIT mührü (DEVİR 1 YENİDEN eşikleri aynı)."""
    out = _yh_d1_regresyon(cikti, M)
    y = os.path.join(cikti, YH_D1_DOSYA["onkayit"]); metin = open(y, encoding="utf-8").read() if os.path.exists(y) else ""
    m1 = re.search(_YH_D1_DESEN["esik_d1"], metin); m2 = re.search(_YH_D1_DESEN["esik_json"], metin)
    if not (m1 and m1.group(1) == yh_esik_d1_sha()):
        raise YHHata("DEVİR 2 regresyon: YH_ESIK_D1 DEVIR_1_ON_KAYIT mührüyle aynı değil -> DURDU")
    if not (m2 and m2.group(1) == _yh_sha_dosya(os.path.join(cikti, YH_D1_DOSYA["esik"]))):
        raise YHHata("DEVİR 2 regresyon: devir1_esik.json DEVIR_1_ON_KAYIT mührüyle aynı değil -> DURDU")
    out["esik_d1"] = m1.group(1); out["esik_json_d1"] = m2.group(1)
    return out


def yh_d2_onkayit_metni(huni: Dict[str, Any], esik: Dict[str, Any], esik_d1: Dict[str, Any], spm: Dict[str, Any], sha: Dict[str, str],
                        den: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D2) -> str:
    dn = [q for q, _a, _b in OC.OC_ESIK["donem"]]; pz = OC.OC_ESIK["pazar"]
    s = ["# YAPI_HEDEF — DEVİR 2 ÖN KAYIT (karne v2; Y2 web entegrasyon adayları F43-F64 + DEVİR 1 YENİDEN W1 / W2 / W2D; 2026-11-19)", "",
         f"{YH_SURUM}; DEVİR 2 eklendi (yh_devir2_ozellik, yh_devir2_kos). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar "
         "yalnız satır kimliği, dönem, giriş tarihi ve özellik dağılımıdır (getirisiz: h5 / es_h5 / st5 okunmadı).", "",
         f"- YH_ESIK_D2_SHA: `{sha['esik_d2']}` (DEVİR 2: tanımlar, pencereler, aday kuralları, kol, dönem, ambargo, bootstrap, L3O, tabaka, etiket)",
         f"- YH_ESIK_D1_SHA: `{sha['esik_d1']}` (= DEVIR_1_ON_KAYIT.md; W1 / W2 / W2D tanım ve eşik kuralı AYNEN)",
         f"- YH_ESIK_SHA: `{sha['esik']}` (= ON_KAYIT_5.md: Y1-Y11c AYNEN)", f"- YH_ESIK6_SHA: `{sha['esik6']}` (= ON_KAYIT_6.md)",
         f"- YH_ESIK7_SHA: `{sha['esik7']}` (= ON_KAYIT_7.md; Y12)", f"- YH_KOD_SHA: `{sha['kod']}` (YAPI_HEDEF.py)",
         f"- D2_OZELLIK_SHA: `{sha['ozellik_d2']}` (ozellik_Y1_d2.csv.gz; F43-F64)",
         f"- D2_ESIK_JSON_SHA: `{sha['esik_json_d2']}` (devir2_esik.json; çeyrekler, tabaka tercilleri, ambargo tarihleri)",
         f"- D1_OZELLIK_SHA: `{sha['ozellik_d1']}` (ozellik_Y1_d1.csv.gz; F30-F32 DEVİR 1 YENİDEN)",
         f"- D1_ESIK_JSON_SHA: `{sha['esik_json_d1']}` (devir1_esik.json; = DEVIR_1_ON_KAYIT mührü, yeni eşik seçilmedi)",
         f"- Y1_OLAY_SHA: `{sha['y1olay']}` (olay_Y1.csv.gz; ölçü satırları)", f"- Y9_OLAY_SHA: `{sha['y9olay']}` (olay_Y9.csv.gz; KOL-B regresyonu)",
         f"- OZELLIK_SHA: `{sha['ozellik']}` (goz_etiket/ozellik_Y1.csv.gz; F7 / F8 / F10 / F15 / F17)", f"- ZAMAN (UTC): `{_yh_simdi()}`", "",
         "## 1. ADAYLAR, F-KODLARI, TANIM, PENCERE, SABİT EŞİK", "",
         "F-kodları F43'ten başlar: F30-F42 DEVİR 1'in (ozellik_Y1_d1.csv.gz) kodlarıdır; DEVİR 1 YENİDEN adayları F30 / F31 / F32'yi aynen kullanır.",
         f"Pencereler: {json.dumps(E['pencere'], ensure_ascii=False)}. t = Y1 sinyal günü (kırılım mumu; kapanışı biliniyor), giriş t+1 açılış; "
         "bölge [sol, t-1], sol = t - F8.", ""]
    for k, v in E["ozellik"].items():
        s.append(f"- **{k}**: {v}.")
    s += ["", f"Çeyrek kuralı: {E['ceyrek']['tanim']}. {E['d1_esik']}.", "",
          "| Aday | Kaynak | Tür | Süzgeç kuralı | Eşik kaynağı | Ad |", "|---|---|---|---|---|---|"]
    for a, v in E["aday"].items():
        s.append(f"| {a} | {v['kaynak']} | {v['tur']}{' (KAPALI KONU)' if v.get('kapali') else ''} | "
                 f"{' VE '.join(f'{c} {o} {x}' for c, o, x in v['kural'])} | {'devir1_esik.json' if v.get('esik') == 'd1' else 'sabit / devir2_esik.json'} | {v['ad']} |")
    s += ["", "### Çeyrek eşikleri (devir2_esik.json; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi; pazar içi, bütün Y1 olayları)", "",
          "| Özellik | Pazar | YÖN 1 q25 / q75 (n) | YÖN 2 q25 / q75 (n) |", "|---|---|---|---|"]
    for c in sorted(esik["yon1"]["ABD"]):
        for p in pz:
            a1, a2 = esik["yon1"][p][c], esik["yon2"][p][c]
            s.append(f"| {c} | {p} | {a1['q25']:.6g} / {a1['q75']:.6g} ({a1['n']}) | {a2['q25']:.6g} / {a2['q75']:.6g} ({a2['n']}) |")
    s += ["", "### DEVİR 1 YENİDEN eşikleri (devir1_esik.json AYNEN)", "", "| Özellik | Pazar | YÖN 1 q25 / q75 | YÖN 2 q25 / q75 |", "|---|---|---|---|"]
    for c in ("F30", "F31", "F32"):
        for p in pz:
            a1, a2 = esik_d1["yon1"][p][c], esik_d1["yon2"][p][c]
            s.append(f"| {c} | {p} | {a1['q25']:.6g} / {a1['q75']:.6g} | {a2['q25']:.6g} / {a2['q75']:.6g} |")
    s += ["", "### K1 tabaka tercil sınırları (2016-22, pazar içi; getirisiz)", "", "| Pazar | F10 t33 / t67 | F15 t33 / t67 | F7 t33 / t67 |", "|---|---|---|---|"]
    for p in pz:
        T = esik["tabaka"][p]
        s.append(f"| {p} | " + " | ".join(f"{T[c][0]:.4g} / {T[c][1]:.4g}" for c in E["tabaka"]["oz"]) + " |")
    s += ["", f"### Ambargo ({E['ambargo']['bar']} bar; {E['ambargo']['tanim']})", "",
          "| Pazar | YÖN 1 eğitim son giriş | YÖN 1 sınama ilk izinli | YÖN 2 eğitim ilk giriş | YÖN 2 sınama son izinli |", "|---|---|---|---|---|"]
    for p in pz:
        a = esik["ambargo"][p]
        s.append(f"| {p} | {a['yon1_son_egitim_giris']} | {a['yon1_sinama_ilk_izinli']} | {a['yon2_ilk_egitim_giris']} | {a['yon2_sinama_son_izinli']} |")
    s += ["", "## 2. ÖLÇÜ, KOLLAR, KARNE v2", "", f"- KOLLAR: A = {E['kol']['A']}; B = {E['kol']['B']}.", f"- ÖLÇÜ: {E['olcu']}.",
          f"- KARNE v2 ETİKET: {E['etiket']}.", f"- BOOTSTRAP: {json.dumps(E['boot'], ensure_ascii=False)}; MARJ her örneklemde (aday ve kol tabanı aynı "
          "aylarla) yeniden hesaplanır.", f"- LEAVE-3-OUT: {E['l3o']}.", f"- K1 TABAKA: {E['tabaka']['tanim']}.", f"- KAPALI KONU: {E['kapali']}.",
          f"- ÇOKLU KARŞILAŞTIRMA: {E['coklu']}.", f"- YENİDEN ÜRETİM hücreleri: {'; '.join(' / '.join(x) for x in E['yeniden_uretim'])}.",
          "- REGRESYON KAPISI: YH_ESIK / 6 / 7 sha = ON_KAYIT_5 / 6 / 7; YH_ESIK_D1 ve devir1_esik.json = DEVIR_1_ON_KAYIT mührü; KOL-B = olay_Y9 "
          "kümesi; eşik json yeniden hesapla aynı; değilse DURUR.", "",
          "## 3. GETİRİSİZ HUNİ (Y1 olayı -> aday tutan olay sayısı; YÖN 1 eşikleri; pazar x dönem; 'amb' = sınama ambargo sonrası)", "",
          "| Satır | Kol | " + " | ".join(f"{p} {q}" for p in pz for q in dn + ["amb"]) + " |", "|---|---|" + "---|" * (len(pz) * (len(dn) + 1))]
    for kol in ("A", "B"):
        for a in ["taban"] + list(E["aday"]):
            r = huni[f"{a}|{kol}"]
            s.append(f"| {a} | {kol} | " + " | ".join(str(r[f'{p}|{q}']) for p in pz for q in dn + ["amb"]) + " |")
    s += ["", "## 4. ÖZELLİK DENETİMİ (getirisiz)", "", "| Pazar | olay | prefix tuttu | kesit hisse-gün | takvim bar | NaN (F43..F64) |", "|---|---|---|---|---|---|"]
    for p, v in den.get("pazar", {}).items():
        s.append(f"| {p} | {v['olay']} | {v['prefix_tuttu']} | {v['kesit_hisse_gun']} | {v['takvim_bar']} | "
                 f"{', '.join(f'{k} {n}' for k, n in v['nan'].items() if n)} |")
    s += ["", "### Mekanik ilişki (K1; Spearman, bütün Y1, getirisiz)", "", "| Özellik | F3 mum boyu | F10 bölge net | F13 kırılım hacmi | F15 konum |",
          "|---|---|---|---|---|"]
    for c, v in spm.items():
        s.append(f"| {c} | " + " | ".join("-" if not np.isfinite(v[r]) else f"{v[r]:+.2f}" for r in ("F3", "F10", "F13", "F15")) + " |")
    s += ["", "Uygulama yorumları (ölçümden önce): (1) t barı (sinyal günü) girdidir; DEVİR 1'den farklı olarak PP / kutu / RVOL / NR7_t t'yi okur, "
          "NR7 karar hücresi t-1 barıdır; (2) PP'de yukarı gün ama 10 günde düşüş günü yoksa NaN (süzgeç tutmaz); (3) DÜZ TAVAN'da ikiden az onaylı "
          "pivot = 0 (düz tavan yok), 6 bar onay gecikmesi yüzünden son 6 barın tepeleri sayılmaz (küçük 3-5 günlük yapıyı geç yakalar; karnede not); "
          "(4) VCP daralmaları penceredeki en yüksek tepeden başlar, son açık salınım girmez; (5) RV kesit evreni bugün işlem gören hisseler (K7), ilk-20 "
          "pazar büyüklüğüne göre farklı seçicilik (ABD ~1.400, AVR / BIST ~580 hisse); (6) KATKI+ dört hücre + bootstrap + L3O + tabaka şartları "
          "birlikte; ters yön hücresi yalnız bilgi.", "", yh_kontrol_tablosu(YH_KONTROL_D2), ""]
    return "\n".join(s) + "\n"


def yh_d2_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False, git: bool = True) -> str:
    """DEVIR_2_ON_KAYIT.md + devir2_esik.json (getirisiz). Özellik dosyası yazılmış, DEVİR 2 ölçülmemiş olmalı."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D2_DOSYA["onkayit"])
    if os.path.exists(os.path.join(cikti, YH_D2_DOSYA["sonuc"])):
        raise YHHata("devir2_sonuc.json var: DEVİR 2 ölçülmüş; ön kayıt ölçümden sonra yazılamaz")
    if os.path.exists(yol):
        if git:
            try:
                _yh_git(yol)
                raise YHHata(f"DEVİR 2 ön kaydı zaten git'e işlenmiş ({yol}); üzerine yazılmaz")
            except YHHata as ex:
                if "zaten" in str(ex):
                    raise
        if not uzerine:
            raise YHHata(f"DEVİR 2 ön kaydı var ({yol}); git'e işlenmemişse --uzerine-yaz")
    M = yh_d2_taban(cikti, getiri=False)
    _yh_d2_regresyon(cikti, M)
    yd = os.path.join(cikti, YH_D2_DOSYA["denetim"])
    if not os.path.exists(yd):
        raise YHHata("DEVİR 2: özellik denetim json yok (önce devir2ozellik)")
    den = json.load(open(yd, encoding="utf-8"))
    if den.get("sha") != _yh_sha_dosya(os.path.join(cikti, YH_D2_DOSYA["ozellik"])):
        raise YHHata("DEVİR 2: özellik dosyası denetim json'daki sha ile aynı değil -> DURDU")
    esik = yh_d2_esik(M, den["ambargo"]); esik_d1 = yh_d2_eski_esik_oku(cikti)
    _yh_yaz(os.path.join(cikti, YH_D2_DOSYA["esik"]), json.dumps({"esik_d2_sha": yh_esik_d2_sha(), **esik}, ensure_ascii=False, indent=1,
                                                                default=_yh_json), "DEVİR 2 eşik")
    _yh_yaz(yol, yh_d2_onkayit_metni(yh_d2_huni(M, esik, esik_d1), esik, esik_d1, yh_d2_spearman(M), _yh_d2_sha(cikti), den), "DEVİR 2 ön kayıt")
    return yol


def yh_d2_kapi(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    """DEVİR 2 koşu kapısı: kontrol listesi (ik_kontrol_kapisi) + sha'lar + regresyon + git kaydı."""
    cikti = cikti or YH_YOL["cikti"]; yol = os.path.join(cikti, YH_D2_DOSYA["onkayit"])
    if not os.path.exists(yol):
        raise YHHata(f"DEVİR 2 ön kaydı yok: {yol}")
    metin = open(yol, encoding="utf-8").read(); out: Dict[str, Any] = {"yol": yol}
    if kontrol:
        import IZ_KARNE as IK
        try:
            out["kontrol"] = IK.ik_kontrol_kapisi(yol)["gecti"]
        except RuntimeError as ex:
            raise YHHata(str(ex))
    bul = {}
    for ad, d_ in _YH_D2_DESEN.items():
        m = re.search(d_, metin)
        if not m:
            raise YHHata(f"DEVİR 2 ön kaydında {ad} satırı yok")
        bul[ad] = m.group(1)
    simdi = _yh_d2_sha(cikti)
    for ad, v in simdi.items():
        if bul[ad] != v:
            raise YHHata(f"{ad} sha tutmuyor: ön kayıt {bul[ad][:12]}…, şimdi {v[:12]}… -> koşu DURDU")
    out["regresyon"] = _yh_d2_regresyon(cikti)
    out["sha"] = simdi; out["onkayit_zaman"] = bul["zaman"]
    if git:
        out["git_onkayit"] = _yh_git(yol); out["git_kod"] = _yh_git(YH_YOL["kod"])
    yhlog.info("yh_d2_kapi AÇIK (%s)", yol)
    return out


def _yh_d2_ay_top(X: pd.DataFrame) -> pd.DataFrame:
    g = X[X.h5.notna() & X.es_h5.notna()]
    return pd.DataFrame({"s": (g.h5 - g.es_h5).to_numpy(float), "n": 1.0, "ay": pd.to_datetime(g.giris).dt.strftime("%Y-%m").to_numpy()}).groupby("ay")[["s", "n"]].sum()


def yh_d2_boot_l3o(Xa: pd.DataFrame, Xk: pd.DataFrame, E: Dict[str, Any] = YH_ESIK_D2, tohum_ek: int = 0) -> Dict[str, float]:
    """MARJ = FARK(aday) - FARK(kol) için ay kümeli bootstrap %95 alt ucu ve leave-3-out MARJ. Ay birimi kol tabanının ayları (aday ⊂ kol)."""
    A = _yh_d2_ay_top(Xa); K_ = _yh_d2_ay_top(Xk)
    if not len(A) or not len(K_):
        return {"boot_alt": np.nan, "l3o": np.nan}
    A = A.reindex(K_.index, fill_value=0.0)
    sa, na, sk, nk = (x.to_numpy(float) for x in (A.s, A.n, K_.s, K_.n))
    B = int(E["boot"]["B"]); rng = np.random.default_rng([int(E["boot"]["tohum"]), int(tohum_ek)])
    W = rng.multinomial(len(sk), np.full(len(sk), 1.0 / len(sk)), size=B).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        mb = (W @ sa) / (W @ na) - (W @ sk) / (W @ nk)
    mb = mb[np.isfinite(mb)]
    alt = float(np.quantile(mb, float(E["boot"]["q"]))) if len(mb) else np.nan
    with np.errstate(invalid="ignore", divide="ignore"):
        tek = (sa.sum() - sa) / (na.sum() - na) - (sk.sum() - sk) / (nk.sum() - nk)
    tek = np.where(np.isfinite(tek), tek, np.inf)
    cik = np.argsort(tek, kind="stable")[:3]; keep = np.ones(len(sk), bool); keep[cik] = False
    l3o = float(sa[keep].sum() / na[keep].sum() - sk[keep].sum() / nk[keep].sum()) if na[keep].sum() > 0 and nk[keep].sum() > 0 else np.nan
    return {"boot_alt": alt, "l3o": l3o}


def yh_d2_etiket(c: Dict[str, Dict[str, Dict[str, Any]]], tabaka_ok: bool, nmin: int, karar: List[str]) -> str:
    """c[pazar][hücre] (egitim / sinama) -> {n, fark, marjinal, boot_alt, l3o, st, es_st}. Kural YH_ESIK_D2['etiket']."""
    H_ = [c[p][k] for p in karar for k in ("egitim", "sinama")]
    ok_n = all(h["n"] >= nmin and np.isfinite(h["fark"]) and np.isfinite(h["marjinal"]) for h in H_)
    if ok_n and all(h["fark"] > 0 and h["marjinal"] > 0 and np.isfinite(h["boot_alt"]) and h["boot_alt"] > 0 and np.isfinite(h["l3o"])
                    and h["l3o"] > 0 and h["st"] <= h["es_st"] for h in H_):
        return "KATKI+" if tabaka_ok else "SORGULA"
    if ok_n and all(h["marjinal"] < 0 for h in H_):
        return "KATKI−"
    return "SORGULA"


def yh_d2_karne(M: pd.DataFrame, esik: Dict[str, Any], esik_d1: Dict[str, Any], E: Dict[str, Any] = YH_ESIK_D2) -> List[Dict[str, Any]]:
    """Karne v2 satırları: aday x kol x pazar; hücreler egitim / sinama (YÖN 1, ambargolu) ve ters (YÖN 2, ambargolu, BİLGİ); bootstrap ve L3O
    eğitim / sınama hücrelerinde; K1 tabaka ABD+AVR eğitim ve sınama."""
    hm = yh_d2_hucre_maske(M, esik, E); nmin = int(E["n_min"]); out = []
    Tb = E["tabaka"]
    tab: Dict[str, Dict[str, np.ndarray]] = {}
    for c in Tb["oz"]:
        x = M[c].to_numpy(float); lab = np.full(len(M), -1)
        for p in OC.OC_ESIK["pazar"]:
            pm = (M.pazar == p).to_numpy(); a, b = esik["tabaka"][p][c]
            with np.errstate(invalid="ignore"):
                lab[pm & (x <= a)] = 0; lab[pm & (x > a) & (x <= b)] = 1; lab[pm & (x > b)] = 2
        tab[c] = {f"T{k}": lab == k for k in range(3)}
    for ko, kol in enumerate(("A", "B")):
        km = M[f"kol{kol}"].to_numpy(bool)
        for pi, pz in enumerate(E["pazar"]):
            pm = M.pazar.isin(pz.split("+")).to_numpy()
            tb = {k: yh_d1_hucre(M[km & pm & hm[k]]) for k in ("egitim", "sinama", "ters")}
            out.append({"aday": "taban", "kol": kol, "pazar": pz, "tur": "taban", **{k: {**v, "marjinal": np.nan} for k, v in tb.items()}, "etiket": "-"})
            for ai, (a, A) in enumerate(E["aday"].items()):
                m1 = yh_d2_maske(M, a, esik, esik_d1, "yon1", E); m2 = yh_d2_maske(M, a, esik, esik_d1, "yon2", E)
                c = {"egitim": yh_d1_hucre(M[km & pm & hm["egitim"] & m1]), "sinama": yh_d1_hucre(M[km & pm & hm["sinama"] & m1]),
                     "ters": yh_d1_hucre(M[km & pm & hm["ters"] & m2])}
                for k in c:
                    c[k]["marjinal"] = c[k]["fark"] - tb[k]["fark"] if c[k]["n"] and tb[k]["n"] else np.nan
                for hi, k in enumerate(("egitim", "sinama")):
                    c[k].update(yh_d2_boot_l3o(M[km & pm & hm[k] & m1], M[km & pm & hm[k]], E, tohum_ek=((ko * 10 + pi) * 100 + ai) * 2 + hi))
                out.append({"aday": a, "kol": kol, "pazar": pz, "tur": A["tur"], **c, "etiket": "?"})
    # K1 tabaka (ABD+AVR) + etiket
    for x in out:
        if x["aday"] == "taban":
            continue
        km = M[f"kol{x['kol']}"].to_numpy(bool); pm = M.pazar.isin(["ABD", "AVR"]).to_numpy()
        m1 = yh_d2_maske(M, x["aday"], esik, esik_d1, "yon1", E); T = {}; tok = True
        if x["pazar"] == "ABD+AVR" or x["pazar"] in E["karar_pazar"]:
            for c_ in Tb["oz"]:
                for tk, tm in tab[c_].items():
                    for k in ("egitim", "sinama"):
                        h = yh_d1_hucre(M[km & pm & hm[k] & m1 & tm]); hb = yh_d1_hucre(M[km & pm & hm[k] & tm])
                        mj = h["fark"] - hb["fark"] if h["n"] and hb["n"] else np.nan
                        T[f"{c_}|{tk}|{k}"] = {"n": h["n"], "marjinal": mj}
                        if h["n"] >= nmin and np.isfinite(mj) and mj <= 0:
                            tok = False
        x["tabaka"] = T; x["tabaka_ok"] = tok
    idx = {(x["aday"], x["kol"], x["pazar"]): x for x in out}
    for x in out:
        if x["aday"] == "taban":
            continue
        c = {p: idx[(x["aday"], x["kol"], p)] for p in E["karar_pazar"]}
        e = yh_d2_etiket(c, idx[(x["aday"], x["kol"], "ABD")]["tabaka_ok"], nmin, E["karar_pazar"])
        x["etiket_kural"] = e
        x["etiket"] = e if x["tur"] == "ana" else f"BİLGİ ({e})"
    return out


def _yh_d2_yeniden(cikti: str, aday: str, kol: str, pazar: str, hucre: str, E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, Any]:
    """Bağımsız yeniden üretim (K11): ham csv'ler + eşik json'ları, düz pandas sorgusu; ambargo ozellik denetim json'undaki takvim bilgisinden değil,
    eşik json'undaki tarihten (yh_d2_maske / yh_d2_hucre_maske / yh_d1_hucre kullanılmaz)."""
    O = pd.read_csv(os.path.join(cikti, YH_DOSYA["satir"].format(d="Y1")), dtype={"sembol": str})
    D = pd.read_csv(os.path.join(cikti, YH_D2_DOSYA["ozellik"]), dtype={"sembol": str})
    D1 = pd.read_csv(os.path.join(cikti, YH_D1_DOSYA["ozellik"]), usecols=["pazar", "sembol", "tarih", "F30", "F31", "F32"], dtype={"sembol": str})
    G = pd.read_csv(YH_YOL["ozellik"], usecols=["pazar", "sembol", "tarih", "F15", "F17"], dtype={"sembol": str})
    Q2 = json.load(open(os.path.join(cikti, YH_D2_DOSYA["esik"]), encoding="utf-8"))
    Q1 = json.load(open(os.path.join(cikti, YH_D1_DOSYA["esik"]), encoding="utf-8"))
    X = O.merge(D, on=["pazar", "sembol", "tarih"]).merge(D1, on=["pazar", "sembol", "tarih"]).merge(G, on=["pazar", "sembol", "tarih"], how="left")
    X = X[X.pazar.isin(pazar.split("+"))]
    if kol == "B":
        X = X.query("F15 <= 0.25 and F17 <= -0.20")
    yon = "yon2" if hucre == "ters" else "yon1"
    parca = []
    for p, g in X.groupby("pazar"):
        am = Q2["ambargo"][p]
        if hucre == "egitim":
            g = g[g.donem == "2016-22"]
        elif hucre == "sinama":
            g = g[g.donem.isin(["2023", "2024-26"]) & (g.giris >= am["yon1_sinama_ilk_izinli"])]
        else:
            g = g[(g.donem == "2016-22") & (g.giris <= am["yon2_sinama_son_izinli"])]
        Q = Q1 if E["aday"][aday].get("esik") == "d1" else Q2
        for c, op, v in E["aday"][aday]["kural"]:
            th = Q[yon][p][c][v] if isinstance(v, str) else v
            g = g.query(f"{c} {op} {th!r}")
        parca.append(g)
    X = pd.concat(parca) if parca else X.iloc[:0]
    X = X.dropna(subset=["h5", "es_h5"])
    return {"n": int(len(X)), "fark": float(X.h5.mean() - X.es_h5.mean()) if len(X) else np.nan}


def yh_devir2_kos(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True, E: Dict[str, Any] = YH_ESIK_D2) -> Dict[str, Any]:
    """DEVİR 2 koşusu: kapı -> karne v2 (iki kol, ambargo, bootstrap, L3O, tabaka) -> yeniden üretim -> devir2_sonuc.json + DEVIR_2_RAPOR.md.
    İkinci koşu DURUR."""
    cikti = cikti or YH_YOL["cikti"]; ys = os.path.join(cikti, YH_D2_DOSYA["sonuc"])
    if os.path.exists(ys):
        raise YHHata("devir2_sonuc.json var: DEVİR 2 zaten ölçüldü (ikinci koşu yok)")
    kp = yh_d2_kapi(cikti, git=git, kontrol=kontrol)
    M = yh_d2_taban(cikti, getiri=True)
    _yh_d2_regresyon(cikti, M)
    esik = json.load(open(os.path.join(cikti, YH_D2_DOSYA["esik"]), encoding="utf-8")); esik_d1 = yh_d2_eski_esik_oku(cikti)
    yeni = yh_d2_esik(M[[c for c in M.columns if c not in ("h5", "es_h5", "st5", "es_st5")]], esik["ambargo"], E)
    if json.dumps(yeni, sort_keys=True, default=_yh_json) != json.dumps({k: esik[k] for k in yeni}, sort_keys=True, default=_yh_json):
        raise YHHata("DEVİR 2: eşik json yeniden hesapla aynı değil -> DURDU")
    K = yh_d2_karne(M, esik, esik_d1, E)
    yu = []
    for a, kol, pz, h in E["yeniden_uretim"]:
        r = [x for x in K if x["aday"] == a and x["kol"] == kol and x["pazar"] == pz][0][h]
        b = _yh_d2_yeniden(cikti, a, kol, pz, h, E)
        tut = b["n"] == r["n"] and (np.isclose(b["fark"], r["fark"], rtol=0, atol=1e-12) or (np.isnan(b["fark"]) and np.isnan(r["fark"])))
        if not tut:
            raise YHHata(f"DEVİR 2 yeniden üretim TUTMADI: {a} {kol} {pz} {h}: {r['n']} / {r['fark']} vs {b['n']} / {b['fark']} -> DURDU")
        yu.append({"aday": a, "kol": kol, "pazar": pz, "hucre": h, "kod_n": r["n"], "kod_fark": r["fark"], "yeni_n": b["n"], "yeni_fark": b["fark"],
                   "durum": "TUTTU"})
    J = {"surum": YH_SURUM, "zaman_utc": _yh_simdi(), "kapi": {k: v for k, v in kp.items() if k != "yol"}, "karne": K, "yeniden_uretim": yu,
         "esik_d2_sha": yh_esik_d2_sha(E)}
    _yh_yaz(ys, json.dumps(J, ensure_ascii=False, indent=1, default=_yh_json), "DEVİR 2 sonuç")
    return {"json": J, "rapor": yh_devir2_rapor(cikti, E)}


def yh_devir2_rapor(cikti: Optional[str] = None, E: Dict[str, Any] = YH_ESIK_D2) -> str:
    """DEVIR_2_RAPOR.md (devir2_sonuc.json + isteğe bağlı devir2_hata.json)."""
    cikti = cikti or YH_YOL["cikti"]; ys = os.path.join(cikti, YH_D2_DOSYA["sonuc"])
    if not os.path.exists(ys):
        raise YHHata("devir2_sonuc.json yok: önce `python YAPI_HEDEF.py devir2kos`")
    J = json.load(open(ys, encoding="utf-8")); K = J["karne"]
    yh_ = os.path.join(cikti, YH_D2_DOSYA["hata"]); H_ = json.load(open(yh_, encoding="utf-8")) if os.path.exists(yh_) else []
    fn = lambda x: x is not None and np.isfinite(float(x))  # noqa: E731
    pc = lambda x: f"{100 * float(x):+.1f}".replace(".", ",") if fn(x) else "-"  # noqa: E731
    pp = lambda x: f"%{100 * float(x):.1f}".replace(".", ",") if fn(x) else "-"  # noqa: E731
    ana = [x for x in K if x["pazar"] == "ABD" and x["tur"] == "ana"]
    say = {e: sum(1 for x in ana if x["etiket"] == e) for e in ("KATKI+", "KATKI−", "SORGULA")}
    s = ["# YAPI_HEDEF — DEVİR 2 RAPORU (karne v2: Y2 web entegrasyon adayları F43-F64 + DEVİR 1 YENİDEN W1 / W2 / W2D)", "",
         f"{J['surum']}. Koşu: {J['zaman_utc']}. Ön kayıt: DEVIR_2_ON_KAYIT.md ({J['kapi'].get('onkayit_zaman', '?')}"
         f"{', git ' + J['kapi']['git_onkayit'].get('commit', '?')[:10] if J['kapi'].get('git_onkayit') else ''}). Komut: `python YAPI_HEDEF.py devir2kos`.", "",
         f"**SONUÇ (karar: ABD ve AVR ayrı ayrı; {len(ana)} ana satır = 10 aday x 2 kol): KATKI+ {say['KATKI+']}, KATKI− {say['KATKI−']}, "
         f"SORGULA {say['SORGULA']}.** KATKI+ olanlar: " + (", ".join(f"{x['aday']} (kol {x['kol']})" for x in ana if x["etiket"] == "KATKI+") or "yok") + ".", "",
         f"Ölçü: {E['olcu']}. Etiket: {E['etiket']}. Değerler yüzde puan; P = 15 barda +%5 hedefin stop'tan önce görülme payı. {E['kapali']}.", "",
         "## 1. Karar tablosu (ana adaylar; her hücre ABD | AVR)", "",
         "| Aday | Kol | eğitim n / FARK (MARJ; boot alt; L3O) ABD | AVR | sınama n / FARK (MARJ; boot alt; L3O) ABD | AVR | stop olay / eş (eğitim; sınama) ABD | AVR | tabaka | etiket |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    idx = {(x["aday"], x["kol"], x["pazar"]): x for x in K}

    def hc(h: Dict[str, Any], tam: bool = True) -> str:
        r = f"{h['n']} / {pc(h['fark'])} ({pc(h['marjinal'])}"
        return r + (f"; {pc(h.get('boot_alt'))}; {pc(h.get('l3o'))})" if tam else ")")

    def st(x: Dict[str, Any]) -> str:
        return f"{pp(x['egitim']['st'])} / {pp(x['egitim']['es_st'])}; {pp(x['sinama']['st'])} / {pp(x['sinama']['es_st'])}"
    for kol in ("A", "B"):
        for a, A in E["aday"].items():
            if A["tur"] != "ana":
                continue
            u, v = idx[(a, kol, "ABD")], idx[(a, kol, "AVR")]
            s.append(f"| {a} | {kol} | {hc(u['egitim'])} | {hc(v['egitim'])} | {hc(u['sinama'])} | {hc(v['sinama'])} | {st(u)} | {st(v)} | "
                     f"{'tuttu' if u.get('tabaka_ok') else 'İŞARET DEĞİŞTİ'} | {u['etiket']} |")
    s += ["", "## 2. İstenen tablo biçimi (aday | kol | eğitim n / fark | sınama n / fark | stop olay / eş | etiket); pazar ABD+AVR havuzu bilgi, etiket "
          "ABD / AVR kuralından", "", "| Aday | Kol | Tür | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters yön n / FARK (MARJ; BİLGİ) | stop olay / eş "
          "(eğitim; sınama) | etiket |", "|---|---|---|---|---|---|---|---|"]
    for kol in ("A", "B"):
        for a, A in E["aday"].items():
            x = idx[(a, kol, "ABD+AVR")]; e = idx[(a, kol, "ABD")]["etiket"]
            s.append(f"| {a} | {kol} | {A['tur']} | {hc(x['egitim'], False)} | {hc(x['sinama'], False)} | {hc(x['ters'], False)} | {st(x)} | {e} |")
        tb = idx[("taban", kol, "ABD+AVR")]
        s.append(f"| taban | {kol} | - | {tb['egitim']['n']} / {pc(tb['egitim']['fark'])} | {tb['sinama']['n']} / {pc(tb['sinama']['fark'])} | "
                 f"{tb['ters']['n']} / {pc(tb['ters']['fark'])} | {st(tb)} | - |")
    s += ["", "## 3. K1 tabaka (ABD+AVR; ana adaylar; MARJ yüzde puan, n; tabaka T0 / T1 / T2 = alt / orta / üst tercil)", "",
          "| Aday | Kol | " + " | ".join(f"{c} {t} {k[:3]}" for c in E["tabaka"]["oz"] for t in ("T0", "T1", "T2") for k in ("egitim", "sinama")) + " |",
          "|---|---|" + "---|" * 18]
    for kol in ("A", "B"):
        for a, A in E["aday"].items():
            if A["tur"] != "ana":
                continue
            T = idx[(a, kol, "ABD")]["tabaka"]
            s.append(f"| {a} | {kol} | " + " | ".join(f"{pc(T[f'{c}|{t}|{k}']['marjinal'])} ({T[f'{c}|{t}|{k}']['n']})" for c in E["tabaka"]["oz"]
                                                       for t in ("T0", "T1", "T2") for k in ("egitim", "sinama")) + " |")
    for pz in ("BIST",):
        s += ["", f"## {pz} (bilgi)", "", "| Aday | Kol | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters n / FARK (MARJ) | stop olay / eş |",
              "|---|---|---|---|---|---|"]
        s += [f"| {x['aday']} | {x['kol']} | {hc(x['egitim'], False)} | {hc(x['sinama'], False)} | {hc(x['ters'], False)} | {st(x)} |"
              for x in K if x["pazar"] == pz and x["tur"] in ("ana", "taban")]
    s += ["", "## YENİDEN ÜRETİM (K11; _yh_d2_yeniden: ham csv + eşik json'ları, düz pandas sorgusu)", "",
          "| Aday | Kol | Pazar | Hücre | kod n / FARK | yeniden n / FARK | durum |", "|---|---|---|---|---|---|---|"]
    for r in J["yeniden_uretim"]:
        s.append(f"| {r['aday']} | {r['kol']} | {r['pazar']} | {r['hucre']} | {r['kod_n']} / {pc(r['kod_fark'])} | {r['yeni_n']} / {pc(r['yeni_fark'])} | "
                 f"{r['durum']} |")
    s += ["", "## Notlar", "", "- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı): P olay ve P eş yukarı yanlı; FARK'ta kısmen götürür; RV kesit "
          "sırası da bugünün evreniyle.", "- ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış): KATKI+ en fazla EMARE düzeyi okunur, iz değildir.",
          f"- {E['coklu']}.", "- DÜZ TAVAN 6 bar onay gecikmesi: 3-5 günlük küçük yapıyı geç yakalar (son 6 barın tepeleri sayılmaz).",
          "- Kod değişti: Colab'da çalışma zamanını yeniden başlat.", "", "## HATA", ""]
    s += [f"- {h}" for h in H_] if H_ else ["- (koşuda hata kaydı yok)"]
    s += ["", yh_kontrol_tablosu(YH_KONTROL_D2), ""]
    metin = "\n".join(s) + "\n"
    _yh_yaz(os.path.join(cikti, YH_D2_DOSYA["rapor"]), metin, "DEVİR 2 rapor")
    return metin


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
    ap.add_argument("komut", choices=["guc", "onkayit", "onkayit2", "onkayit3", "s7ozellik", "onkayit4", "kos", "rapor", "rapor2", "rapor3", "rapor4",
                                      "sha", "s9ozellik", "tasarim5", "onkayit5", "rapor5", "onkayit6", "grup6", "filtrekarne", "mahkeme", "rapor6",
                                      "onkayit7", "puan7", "rapor7", "devir1ozellik", "devir1onkayit", "devir1kos",
                                      "devir1rapor", "devir2ozellik", "devir2onkayit", "devir2kos", "devir2rapor"])
    ap.add_argument("--deneme", default=None)
    ap.add_argument("--islem", type=int, default=1)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--gitsiz", action="store_true")
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--pazar", default=None)
    ap.add_argument("--sembol", default=None)
    ap.add_argument("--tarih", default=None)
    ap.add_argument("--liste", default=None, help="mahkeme: toplu liste csv (no, pazar, sembol, tarih)")
    ap.add_argument("--md", default=None, help="mahkeme --liste: çıktı md yolu")
    ap.add_argument("--json", default=None, help="mahkeme: json çıktı yolu")
    ap.add_argument("--s7", action="store_true", help="mahkeme: S7 PDF'i 50 olay -> S7_MAHKEME.md")
    ap.add_argument("--tur4", action="store_true", help="mahkeme: TUR 4 40 sayfa -> tur/4/TUR_4_MAHKEME.md")
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
        elif a.komut == "s7ozellik":
            R_ = yh_s7_ozellik_yaz(a.veri); print(json.dumps({k: v for k, v in R_.items()}, ensure_ascii=False, indent=1, default=_yh_json))
        elif a.komut == "onkayit4":
            print(yh_onkayit4_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "rapor4":
            print(yh_rapor4(a.cikti))
        elif a.komut == "s9ozellik":
            R_ = yh_s9_ozellik_yaz(a.veri); print(json.dumps({k: v for k, v in R_.items()}, ensure_ascii=False, indent=1, default=_yh_json))
        elif a.komut == "tasarim5":
            print(json.dumps(yh_tasarim5(a.cikti, a.veri, git=not a.gitsiz), ensure_ascii=False, indent=1, default=_yh_json))
        elif a.komut == "onkayit5":
            print(yh_onkayit5_yaz(a.cikti, a.veri, a.islem, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "rapor5":
            print(yh_rapor5(a.cikti))
        elif a.komut == "onkayit6":
            print(yh_onkayit6_yaz(a.cikti, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "grup6":
            R_ = yh_kos6(a.cikti, a.veri, a.islem, git=not a.gitsiz)
            print(yh_rapor6(a.cikti)[:6000])
        elif a.komut == "rapor6":
            print(yh_rapor6(a.cikti))
        elif a.komut == "onkayit7":
            print(yh_onkayit7_yaz(a.cikti, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "puan7":
            R_ = yh_kos7(a.cikti, a.veri, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "rapor7":
            print(yh_rapor7(a.cikti))
        elif a.komut == "devir1ozellik":
            R_ = yh_devir_ozellik_yaz(a.veri, a.cikti, a.islem); print(json.dumps({k: v for k, v in R_.items()}, ensure_ascii=False, indent=1, default=_yh_json))
        elif a.komut == "devir1onkayit":
            print(yh_d1_onkayit_yaz(a.cikti, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "devir1kos":
            R_ = yh_devir_kos(a.cikti, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "devir1rapor":
            print(yh_devir_rapor(a.cikti))
        elif a.komut == "devir2ozellik":
            R_ = yh_devir2_ozellik_yaz(a.veri, a.cikti, a.islem); print(json.dumps({k: v for k, v in R_.items()}, ensure_ascii=False, indent=1, default=_yh_json))
        elif a.komut == "devir2onkayit":
            print(yh_d2_onkayit_yaz(a.cikti, uzerine=a.uzerine_yaz, git=not a.gitsiz))
        elif a.komut == "devir2kos":
            R_ = yh_devir2_kos(a.cikti, git=not a.gitsiz)
            print(R_["rapor"][:6000])
        elif a.komut == "devir2rapor":
            print(yh_devir2_rapor(a.cikti))
        elif a.komut == "filtrekarne":
            R_ = yh_filtre_karne(a.cikti); print("SORGULANACAK FİLTRELER: " + ("; ".join(R_["sorgulanacak"]) or "yok"))
        elif a.komut == "mahkeme":
            if a.s7:
                print(json.dumps(yh_mahkeme_s7(a.cikti, a.veri)["ozet"], ensure_ascii=False, indent=1, default=_yh_json))
            elif a.tur4:
                R_ = yh_mahkeme_tur4(a.veri); oz_ = R_.get("ozet", R_)
                _yh_yaz(os.path.join(a.cikti or YH_YOL["cikti"], YH_DOSYA["tur4_mahkeme_ozet"]),
                        json.dumps(oz_, ensure_ascii=False, indent=1, default=_yh_json), "TUR 4 mahkeme özeti")
                print(json.dumps(oz_, ensure_ascii=False, indent=1, default=_yh_json))
            elif a.liste:
                L_ = pd.read_csv(a.liste, dtype={"sembol": str}, parse_dates=["tarih"])
                if "no" not in L_.columns:
                    L_.insert(0, "no", np.arange(1, len(L_) + 1))
                md_ = a.md or os.path.join(a.cikti or YH_YOL["cikti"], "MAHKEME_liste.md")
                print(json.dumps(yh_mahkeme_toplu(L_, md_, "MAHKEME (liste)", a.json, a.veri)["ozet"], ensure_ascii=False, indent=1, default=_yh_json))
            else:
                if not (a.pazar and a.sembol and a.tarih):
                    raise YHHata("mahkeme: --pazar --sembol --tarih (ya da --liste / --s7 / --tur4) gerekli")
                M_ = yh_mahkeme(a.pazar, a.sembol, a.tarih, a.veri)
                print(yh_mahkeme_metin(M_, f"MAHKEME {a.pazar} {a.sembol} {a.tarih}"))
                if a.json:
                    _yh_yaz(a.json, json.dumps(_yh_m_json(M_), ensure_ascii=False, indent=1, default=_yh_json), "mahkeme json")
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
