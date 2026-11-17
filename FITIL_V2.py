"""FITIL_V2 — S+ v2 'TAM GİRİLİR' (Cemal, 17 Kasım 2026: 'kod bu kurallar eşiğinde tam girilir dediklerini, sonrasının verisini görmeden
seç; kodu beni test ettiğin gibi test et'). Tek dosya; FITIL_OBEK (Ç187 fitil ölçüleri) ve ORTAK_CETVEL v1.0'ı yalnız İMPORT eder.

Tanım (iş tanımı §2; her gün t yalnız t ve öncesi; geçerli bar H > L, V > 0; W = son 10 geçerli bar):
  (1) ŞEKİL       ASIM >= a VE ALTYOK >= b (S+ 0,20 / 0,50; gevşek 0,10 / 0,40)
  (2) SAVUNMA     HAT = min(Low, W); düz: (max(L, W) - HAT) / medyan(R, W) <= duz (1,0 / 1,5 / kapalı); sağlam: W kapanışları HAT x (1 - tol)
                  üstünde VE HAT >= önceki 30 geçerli barın en düşük Low'u x (1 - tol) VE C_t >= HAT (tol 0,02 / 0,03)
  (3) DÖNÜM       1 - C_t / (W'den önceki 60 geçerli barın en yüksek kapanışı) >= dusus (0,10 / 0,15 / 0,20)
  (4) YOL ALMAMIŞ C_t <= HAT x (1 + yol) (0,05 / 0,10) VE C_t < max(High, W)
  (5) TEPEDE DEĞİL C_t <= 120 geçerli bar en yüksek kapanışı x 0,85
  TAM = (1)-(5). Bilgi satırları: S1 = (1), S12 = (1)+(2), S123 = (1)+(2)+(3).

İş tanımı: arastirma_cikti/fitil_v2/FITIL_V2_IS_TANIMI.md (koşudan önce git'e işlendi).
Komut:  python FITIL_V2.py tasarim [--veri K]                    AŞAMA 1: etiketli set x 72 noktalı ızgara -> TASARIM.md (GETİRİSİZ)
        python FITIL_V2.py onkayit [--veri K] [--uzerine-yaz]    ON_KAYIT.md (mühür, sha'lar, OLAY SAYIMI getirisiz, kontrol listesi)
        python FITIL_V2.py kos [--veri K] [--gitsiz]             AŞAMA 2: ORTAK CETVEL ölçümü -> sonuc.json + RAPOR.md (kapılar)
        python FITIL_V2.py korset [--veri K] [--gitsiz]          KÖR SET 2: FITIL_V2_KOR_SET.pdf + kor2_anahtar.json (gizli)
        python FITIL_V2.py olc --cevap "1:E,2:H,..."             Cemal'in kör set 2 yanıtı -> uyum (anahtar ve sonuc.json'a eklenir)
        python FITIL_V2.py olc --cevap-dosya kor2_cevap_cemal.json   aynı, yanıt dosyasından ('-' = yanıtsız, paylardan çıkar)
        python FITIL_V2.py rapor [--ek DOSYA]                    sonuc.json -> RAPOR.md
Colab:  exec(open('FITIL_V2.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Komisyon / kayma yok. Evren bugün işlem gören hisseler: hayatta kalma yanlılığı (getiriler yukarı, -%50 olasılığı aşağı yanlı).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_FV = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402
import warnings  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_FV = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_FV not in sys.path:
    sys.path.insert(0, KOK_FV)

import ORTAK_CETVEL as OC  # noqa: E402
import FITIL_OBEK as FO  # noqa: E402

fvlog = logging.getLogger("col.fitil_v2")
if not fvlog.handlers:
    _fv_h = logging.StreamHandler(sys.stderr)
    _fv_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s fitil_v2: %(message)s", "%H:%M:%S"))
    fvlog.addHandler(_fv_h)
    fvlog.setLevel(logging.INFO)
    fvlog.propagate = False

FV_SURUM = "FITIL_V2 v1.0 (2026-11-17): S+ v2 'TAM GİRİLİR' (şekil + savunma hattı + dönüm + yol almamış + tepede değil), ORTAK CETVEL v1.0 ile"
FV_YOL = {"cikti": os.path.join(KOK_FV, "arastirma_cikti", "fitil_v2"), "kod": os.path.join(KOK_FV, "FITIL_V2.py"),
          "is_tanimi": os.path.join(KOK_FV, "arastirma_cikti", "fitil_v2", "FITIL_V2_IS_TANIMI.md"),
          "kor_anahtar": os.path.join(KOK_FV, "arastirma_cikti", "fitil_obek", "kor_anahtar.json"),
          "kor_cevap": os.path.join(KOK_FV, "arastirma_cikti", "fitil_obek", "kor_cevap_cemal.json"),
          "veri": os.environ.get("OC_VERI", "/tmp/veri"), "veri2": os.environ.get("OC_VERI2", "/tmp/veri2"),
          "satir": os.environ.get("FV_SATIR", "/tmp/fitil_v2")}
FV_DOSYA = {"tasarim": "TASARIM.md", "onkayit": "ON_KAYIT.md", "sonuc": "sonuc.json", "rapor": "RAPOR.md", "pdf": "FITIL_V2_KOR_SET.pdf",
            "anahtar": "kor2_anahtar.json"}

FV_SART = ["s1", "s2", "s3", "s4", "s5"]
FV_SART_AD = {"s1": "(1) şekil", "s2": "(2) savunma hattı", "s3": "(3) dönüm", "s4": "(4) yol almamış", "s5": "(5) tepede değil"}

# ================================================================ MÜHÜRLÜ TANIM (ızgara önceden; sonuç görüldükten sonra DEĞİŞMEZ)
V2_ESIK: Dict[str, Any] = {
    "surum": "1.0",
    "bar": "geçerli bar (OC.oc_veri temiz: O/H/L/C > 0, H > L, V > 0; FO.fo_bar ayrıca süzer); R = H - L; alt / üst fitil payı FO.fo_bar",
    "k": 10,
    "pencere": "W = t dahil son 10 geçerli bar (rolling, yalnız t'ye kadar). ASIM = ort(üst) - ort(alt), ALTYOK = alt < 0,10 bar payı (FO.fo_pencere)",
    "sabit": {"hat_onceki": 30, "dusus_onceki": 60, "tepe_gun": 120, "tepe_esik": 0.15, "stop_carpan": 0.98, "kirilim_ufuk": 60},
    "tanim": {
        "s1": "ŞEKİL: ASIM >= a VE ALTYOK >= b",
        "s2": "SAVUNMA HATTI: HAT = min(Low, W); düz = (max(Low, W) - HAT) / medyan(R, W) <= duz (kapalı ise şart yok); sağlam = min(Close, W) >= "
              "HAT x (1 - tol) (tanım gereği doğru) VE HAT >= min(Low, W'den önceki 30 geçerli bar) x (1 - tol) VE C_t >= HAT",
        "s3": "DÖNÜM: 1 - C_t / max(Close, W'den önceki 60 geçerli bar) >= dusus",
        "s4": "YOL ALMAMIŞ: C_t <= HAT x (1 + yol) VE C_t <= max(High, W \\ {t}) (t HARİÇ önceki 9 pencere barının en yüksek High'ı: bugün "
              "pencere tepesini kapanışla kırmamış; SAPMA-1, ana model kararı 17 Kas)",
        "s5": "TEPEDE DEĞİL: C_t <= max(Close, t dahil son 120 geçerli bar) x (1 - 0,15)",
        "tam": "TAM GİRİLİR = (1) VE (2) VE (3) VE (4) VE (5); tanımsız ölçü (yetersiz geçmiş) = şart tutmaz",
        "cikis_bilgi": "HAT x 0,98 altı kapanış = STOP (K8); max(High, W) üstü kapanış = KIRILIM; t+1 .. t+60 geçerli barda hangisi önce"},
    "izgara": {"sekil": {"S+": [0.20, 0.50], "gevsek": [0.10, 0.40]}, "duz": [1.0, 1.5, None], "hatTol": [0.02, 0.03],
               "dusus": [0.10, 0.15, 0.20], "yol": [0.05, 0.10]},
    "sadelik": "Eşit puanda en sade nokta (sözlük sırası, önceden yazıldı): (i) düz şartı kapalı > 1,5 > 1,0 (şart yok / daha az bağlayıcı); "
               "(ii) şekil S+ (Ç187 tanımı, yeni sayı yok) > gevşek; (iii) hatTol 0,02 (stop marjı ile aynı sayı) > 0,03; (iv) dusus 0,10 > "
               "0,15 > 0,20 (en az bağlayıcı); (v) yol 0,10 > 0,05 (daha az bağlayıcı)",
    "puan": "PUAN = (E-GİRİŞ sayfalarında sayfa günü TAM) + (3 örnek aralıkta en az bir TAM günü) + (NEGATİF sayfalarda sayfa günü TAM YOK) + "
            "(NEGATİF aralıklarda hiç TAM günü yok) + (E-ŞEKİL sayfalarında sayfa günü (1) VAR VE TAM YOK); en çok 7 + 3 + 10 + 2 + 12 = 34",
    "etiket": {
        "kaynak": "kor_anahtar.json (sayfa -> pazar / sembol / tarih / grup; r20 / r60 alanları OKUNMAZ) + kor_cevap_cemal.json (E / H / B ve not)",
        "sayfa_gunu": "pencere son günü = sayfa tarihi (t); ölçü yalnız o gün",
        "E_GIRIS": [3, 9, 6, 22, 16, 17, 26],
        "E_SEKIL": "Cemal'in E dediği öteki sayfalar",
        "NEG_SAYFA": "Cemal'in H dediği sayfalar + S- (grup SM) sayfalarında E demedikleri",
        "ornek_poz": [{"ad": "TEHOL", "pazar": "BIST", "bas": "2025-05-06", "son": "2025-05-28"},
                      {"ad": "BINBN", "pazar": "BIST", "bas": "2024-12-23", "son": "2025-01-13"},
                      {"ad": "PAPIL", "pazar": "BIST", "bas": "2025-11-14", "son": "2025-11-26"}],
        "neg_aralik": [{"ad": "TEHOL", "pazar": "BIST", "bas": "2024-12-01", "son": "2025-02-28", "not": "Ara 2024 - Şub 2025 yükseliş bacağı"},
                       {"ad": "DGXX", "pazar": "ABD", "bas": "2026-10-01", "son": "2026-11-13", "not": "Eki-Kas 2026",
                        "kaynak": "V_ABD / oc_veri 31.08.2026'da keser: yalnız etiket için yfinance (auto_adjust=False, 2024-01-01 .. 2026-11-13; "
                                  "16 Kas yarım bar alınmaz); ölçüme girmez"}]},
    "baglam": {"gun": 250, "dip_konum": 0.25, "tepe_konum": 0.75, "dip_tepeden": 0.15,
               "tanim": "EK (Cemal, 17 Kas; ön kayıttan önce, sonuç görülmeden): KONUM = (C_t - min(Low, t dahil 250 geçerli bar)) / (max(High, 250) - "
                        "min(Low, 250)); DİP = KONUM <= 0,25 VE C_t <= max(Close, 120 geçerli bar) x (1 - 0,15); TEPE = KONUM >= 0,75; ORTA = ikisi "
                        "de değil (yolun ortası); 250 bar yoksa TANIMSIZ (hiçbir sınıfa girmez). Eşikler sabit, ızgaraya girmez"},
    "satirlar": {"TAM_DIP": "TAM GİRİLİR VE bağlam DİP [ANA] (Cemal: 'dipte risk alınır, stop bellidir')",
                 "TAM": "TAM GİRİLİR = (1)-(5), bağlam fark etmez [bilgi]",
                 "TAM_ORTA": "TAM VE bağlam ORTA [bilgi] (Cemal: 'yolun ortasında güven olmaz')",
                 "TAM_TEPE": "TAM VE bağlam TEPE [bilgi]",
                 "S1": "(1) şekil tek başına (= Ç187 S+ seçilen şekil eşiğiyle) [bilgi]",
                 "S12": "(1) + (2) [bilgi]", "S123": "(1) + (2) + (3) [bilgi]",
                 "SM_TEPE": "AYNA: bağlam TEPE VE S- (FITIL_OBEK ters öbek: ASIM <= -0,20 VE USTYOK >= 0,50) = 'ÇIK' [bilgi; kaçınma, beklenen yön -]"},
    "ana": ["TAM_DIP"],
    "yon": {"TAM_DIP": "+", "TAM": "+", "TAM_ORTA": "+", "TAM_TEPE": "+", "S1": "+", "S12": "+", "S123": "+", "SM_TEPE": "-"},
    "olay": "DURUM GÜNLERİ: şartın t kapanışında doğru olduğu her geçerli bar OC.oc_olc'a verilir; giriş t'den sonraki ilk geçerli açılış; "
            "tekilleştirme 60 gün (cetvel: ilk durum günü tutulur)",
    "karar": {"ana": "TAM_DIP satırı ORTAK CETVEL v1.0: hücre TUTAR = dört şart + iki yarı > 0 (oc_hucre); durum oc_hucre_durum; genel etiket "
                     "FO.fo_etiket(+) = OC.oc_etiket ve cetvelin 'İZ DEĞİL'i 'DESTEKLENMEDİ' (Ç187 ile aynı): İZ (dört karar hücresi ABD / AVR x "
                     "2023 / 2024-26 TUTAR) / EMARE (en az biri) / ÖLÇÜLEMEDİ (güç yetersiz) / DESTEKLENMEDİ (güç yeterli, tutmadı). BIST bilgi; "
                     "2016-22 keşif bilgi",
              "bilgi": "TAM, TAM_ORTA, TAM_TEPE, S1, S12, S123 (beklenen yön +, cetvel TUTAR) ve SM_TEPE (beklenen yön -, AYNA kaçınma şartı "
                       "FO.fo_kacinma: n >= 30, ort < 0 ve üst uç < 0, sıra < 0,50, portföy < p10, iki yarı < 0; etiket FO.fo_etiket(-)); 7 satır x 4 "
                       "karar hücresi = 28 test; p = beklenen yönde ay kümeli bootstrap (FO.fo_p); Benjamini-Hochberg q 0,10; n < 30 hücre teste girmez",
              "olasilik": "olasılık tablosu (P +%100 / -%50 eş ve taban katları, 250 gün) cetvelden aynen; etiket SEÇİCİ / PİYANGO / YOK",
              "kirilim": "bilgi: cetvel olaylarında (tekil) t+1 .. t+60 geçerli barda önce KIRILIM (C > max(High, W)) mı STOP (C < HAT x 0,98) mı; "
                         "pazar x dönem payları; 60 bar yoksa ÖLÇÜLMEZ"},
    "gelecek_denetimi": {"n": 40, "tohum": 1711,
                         "tanim": "kos: her pazarda rastgele 40 TAM_DIP durum gününde seri t'de kesilip ölçüler yeniden hesaplanır; TAM_DIP ve bağlam aynı olmalı; "
                                  "tutmazsa koşu DURUR"},
    "kor2": {"tohum": 1717, "bas": "2016-01-01", "son": "2026-08-31", "once": 120, "pencere": 10,
             "grup": {"TAM": {"BIST": 15, "ABD": 15}, "DEGIL": {"BIST": 5, "ABD": 5}},
             "tanim": "TAM grubu: kodun TAM_DIP (TAM GİRİLİR + bağlam DİP) dediği durum günlerinden rastgele (her hisse setin tamamında bir kez); "
                      "DEĞİL grubu: (1) şekil VAR ama TAM_DIP YOK günlerinden rastgele (anahtarda düşüren şart ve bağlam); sayfa = t'de biten 10 mum "
                      "+ öncesi 120 mum (EK, Cemal 17 Kas: bağlam görünsün), sonrası yok, adsız, tarihsiz; sıra karışık (tohum)",
             "soru": "E = tam girilir (son mumda stoplu girerdim) · H = girmem · B = belirsiz",
             "karar": "TAM sayfalarında E payı >= 0,60 VE TAM - DEĞİL E payı farkı >= 0,30 -> 'GÖZLE UYUMLU'; TAM E payı < 0,40 -> 'GÖZLE UYUMSUZ'; "
                      "aksi 'KISMİ'. Fisher kesin p bilgi. Sonuç (r20 / r60 / önce kırılım-stop) yalnız bilgi; n küçük, bulgu değil"},
    "veri": "OC.oc_veri (cetvel): V_BIST / V_ABD / V_AVR; ABD k34_yahoo varsa eklenir, yoksa yalnız V_ABD (raporda yazılır)",
}

# Tasarım sınamasının seçtiği nokta (TASARIM.md 'SECIM_JSON' satırıyla AYNI olmalı; onkayit / kos / test denetler). None = tasarım koşulmadı.
V2_SECIM: Optional[Dict[str, Any]] = {"no": "N30", "sekil": "S+", "duz": None, "hatTol": 0.02, "dusus": 0.20, "yol": 0.10}

FV_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, "
                   "aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: (3) "
                   "dönüm (60 bar tepeden >= %10-20 düşmüş) ve (5) tepede değil sinyali düşük 60 gün momentumlu hisselere iter; eşler aynı "
                   "momentum beşliğinden olduğu için bu fark eşlenir; kısa vadeli dönüş / oynaklık eşlenmez (raporda sınır)"),
    "K2": ("EVET", "bütün ölçüler rolling geriye (fv_olcu: W, önceki 30 / 60 / 120 / 250 bar t'de biter; bağlam KONUM t dahil 250 bar); etiket seti Cemal'in t'de biten sayfaları; "
                   "kos fv_gelecek_denetimi her pazarda 40 TAM_DIP gününde (bağlam dahil) seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma' "
                   "(rastgele seride kesme = tam seri, bütün günler); tasarımda getiri / r20 / r60 hiç okunmadı (anahtarın r alanları atlanır)"),
    "K3": ("EVET", "OC.oc_veri temiz barlar (H>L, V>0, fiyat > 0; geçersiz bar atılır, pencereye girmez) + FO.fo_bar ikinci süzgeç; DGXX etiketi "
                   "yfinance'ta 16 Kas (seans içi yarım bar) alınmaz ve aynı süzgeçten geçer"),
    "K4": ("EVET", "durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir (ilk gün); n bağımsız olay; hücrede "
                   "medyan da yazılır; ön kayıt OLAY SAYIMI durum günü ve tekil olayı ayrı verir"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter; kör set r20 / r60 de t+1 açılışından"),
    "K6": ("EVET", "tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); bütün şartlar oran (fitil payı, HAT'a göre %, tepeye göre %), birimden "
                   "bağımsız; bölünme şüphesi cetvelde geçmiş pencerede havuz dışı; DGXX etiketi ham (auto_adjust=False), yalnız etiket"),
    "K7": ("EVET", "evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı, -%50 olasılığı "
                   "aşağı yanlı' notu; (3) dönüm ve (5) tepede değil düşmüş hisseleri seçtiği için hayatta kalma yanlılığı bu işte daha büyük olabilir"),
    "K8": ("EVET", "3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; "
                   "tasarım seti küçük (19 + 10 sayfa + 5 aralık): eşik seçimi bulgu değil, yalnız tanım kalibrasyonu; olay sayımı getirisiz"),
    "K9": ("EVET", "V2_ESIK sha + V2_SECIM + FITIL_V2.py sha + TASARIM.md sha + kör anahtar / cevap sha + cetvel üç sha + veri sha bu dosyada; "
                   "ızgara (72 nokta) ve sadelik sırası tasarımdan önce kodda yazılı; iş tanımı git'te (22d7e50); kos ik_kontrol_kapisi + "
                   "OC.oc_kapi + fv_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz"),
    "K10": ("UYGULANMAZ", "metin / KAP ayrıştırma yok; yalnız OHLCV; etiket sayfaları kor_anahtar.json'dan (sembol / tarih) mekanik; 3 sayfa "
                          "(PAPIL No 3, LIDER No 26, EPLAS No 41) ham V_BIST'ten bağımsız kodla yeniden hesaplandı: ASIM / ALTYOK / HAT / düşüş / "
                          "yol / tepe / düz TASARIM tablosuyla aynı"),
    "K11": ("EVET", "ana olay satırları /tmp/fitil_v2/olay_TAM_DIP.csv.gz (bağlam ve kırılım sütunlu); rapor >= 2 hücreyi bağımsız kodla yeniden üretir (ana model denetimi); "
                    "tasarım tablosu her etiketin ölçü değerlerini yazar (elle yeniden hesaplanabilir)"),
    "K12": ("EVET", "etiketler yalnız FO.fo_etiket / oc_etiket kuralıyla; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı "
                    "(komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok; kör set sorusu 'tam girilir mi', alım tavsiyesi değil"),
    "K13": ("EVET", "çakışma kapısı _cakisma_kontrol_fv; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar "
                    "taraması testte ve her yazımda; ücretli veri yok; commit / push ana modelin"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; tanım ölçümü ve kör set (kapalı konu 'tek göstergeye göre alım' açılmaz)"),
}


class FVHata(RuntimeError):
    """Durdurucu hata: ön kayıt yok / sha tutmuyor / kapı / tasarım seçimi tutmuyor / geleceğe bakma denetimi / veri yok."""


# ================================================================ 0) ORTAK
_FV_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_FV_ANAHTAR = re.compile(r"(api[_-]?key|token|secret|password|şifre)\s*[=:]\s*['\"][^'\"]{8,}", re.I)


def _fv_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _fv_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _fv_sha_obj(o: Any) -> str:
    return hashlib.sha256(json.dumps(o, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")).hexdigest()


def fv_esik_sha() -> str:
    """Mühür: tanım + ızgara + seçilen nokta birlikte."""
    return _fv_sha_obj({"esik": V2_ESIK, "secim": V2_SECIM})


def _fv_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or FV_YOL["cikti"], FV_DOSYA[ad])


def _fv_sizinti(metin: str, ad: str) -> None:
    if _FV_EPOSTA.search(metin) or _FV_ANAHTAR.search(metin):
        raise FVHata(f"{ad}: e-posta / anahtar biçimli parça var")


def _fv_yaz(yol: str, metin: str, ad: str) -> None:
    _fv_sizinti(metin, ad)
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)


def _yz(x: Any, n: int = 1) -> str:
    return FO._yz(x, n)


def _sy(x: Any, n: int = 2) -> str:
    return FO._sy(x, n)


# ================================================================ 1) ÖLÇÜLER ve KURAL (yalnız t'ye kadar)
_FV_OLCU_KOL = ["ASIM", "ALTYOK", "USTYOK", "KONUM", "HAT", "LMAXW", "MEDR", "DUZ", "CMINW", "HMAXW", "HMAXW9", "ONC30", "MAXC60", "DUSUS", "YOL", "MAXC120", "TEPE", "C"]


def fv_olcu(df: pd.DataFrame) -> pd.DataFrame:
    """Temiz barlar -> geçerli bar indeksinde ölçüler (hepsi t dahil geriye): ASIM, ALTYOK, HAT, DUZ, ONC30, DUSUS, YOL, TEPE, HMAXW, ..."""
    E = V2_ESIK; k = E["k"]; Sb = E["sabit"]
    B = FO.fo_bar(df)
    if not len(B):
        return pd.DataFrame(columns=_FV_OLCU_KOL, index=B.index, dtype=float)
    d = df.loc[B.index, ["High", "Low", "Close"]].astype(float)
    L, H, C = d.Low, d.High, d.Close
    P = FO.fo_pencere(B, k)
    M = pd.DataFrame(index=B.index)
    M["ASIM"] = P.ASIM; M["ALTYOK"] = P.ALTYOK; M["USTYOK"] = P.USTYOK
    Bg = E["baglam"]["gun"]
    with np.errstate(all="ignore"):
        lo = L.rolling(Bg, min_periods=Bg).min(); hi = H.rolling(Bg, min_periods=Bg).max()
        M["KONUM"] = (C - lo) / (hi - lo)
    M["HAT"] = L.rolling(k, min_periods=k).min()
    M["LMAXW"] = L.rolling(k, min_periods=k).max()
    M["MEDR"] = B.R.rolling(k, min_periods=k).median()
    with np.errstate(all="ignore"):
        M["DUZ"] = (M.LMAXW - M.HAT) / M.MEDR
        M["CMINW"] = C.rolling(k, min_periods=k).min()
        M["HMAXW"] = H.rolling(k, min_periods=k).max()
        M["HMAXW9"] = H.shift(1).rolling(k - 1, min_periods=k - 1).max()
        M["ONC30"] = L.shift(k).rolling(Sb["hat_onceki"], min_periods=Sb["hat_onceki"]).min()
        M["MAXC60"] = C.shift(k).rolling(Sb["dusus_onceki"], min_periods=Sb["dusus_onceki"]).max()
        M["DUSUS"] = 1 - C / M.MAXC60
        M["YOL"] = C / M.HAT - 1
        M["MAXC120"] = C.rolling(Sb["tepe_gun"], min_periods=Sb["tepe_gun"]).max()
        M["TEPE"] = 1 - C / M.MAXC120
    M["C"] = C
    return M[_FV_OLCU_KOL]


def fv_prm(secim: Dict[str, Any]) -> Dict[str, Any]:
    """Izgara noktası -> sayısal eşikler."""
    a, b = V2_ESIK["izgara"]["sekil"][secim["sekil"]]
    return {"asim": a, "altyok": b, "duz": secim["duz"], "hatTol": secim["hatTol"], "dusus": secim["dusus"], "yol": secim["yol"]}


def fv_kural(M: pd.DataFrame, secim: Dict[str, Any]) -> pd.DataFrame:
    """Ölçüler + ızgara noktası -> şart bayrakları s1..s5, alt şartlar, TAM ve bilgi satırları (NaN = tutmaz)."""
    p = fv_prm(secim); Sb = V2_ESIK["sabit"]
    with np.errstate(invalid="ignore"):
        s1 = (M.ASIM >= p["asim"]) & (M.ALTYOK >= p["altyok"])
        duz = pd.Series(True, index=M.index) if p["duz"] is None else (M.DUZ <= p["duz"])
        tol = p["hatTol"]
        hat_w = M.CMINW >= M.HAT * (1 - tol)
        hat_dip = M.HAT >= M.ONC30 * (1 - tol)
        hat_ust = M.C >= M.HAT
        s2 = duz & hat_w & hat_dip & hat_ust & M.HAT.notna()
        s3 = M.DUSUS >= p["dusus"]
        s4 = (M.C <= M.HAT * (1 + p["yol"])) & (M.C <= M.HMAXW9)
        s5 = M.C <= M.MAXC120 * (1 - Sb["tepe_esik"])
    Z = pd.DataFrame({"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s2_duz": duz & M.DUZ.notna() if p["duz"] is not None else M.HAT.notna(),
                      "s2_yenidip": ~hat_dip, "s4_hat": M.C <= M.HAT * (1 + p["yol"]), "s4_tepe": M.C <= M.HMAXW9,
                      "s2_tanimsiz": M.ONC30.isna(), "s3_tanimsiz": M.MAXC60.isna(), "s5_tanimsiz": M.MAXC120.isna()},
                     index=M.index).fillna(False)
    Z = Z.astype(bool)
    Z["TAM"] = Z.s1 & Z.s2 & Z.s3 & Z.s4 & Z.s5
    Z["S1"] = Z.s1
    Z["S12"] = Z.s1 & Z.s2
    Z["S123"] = Z.s1 & Z.s2 & Z.s3
    Bg = V2_ESIK["baglam"]; Fe = FO.FO_ESIK["s_eksi"]
    with np.errstate(invalid="ignore"):
        dip = ((M.KONUM <= Bg["dip_konum"]) & (M.C <= M.MAXC120 * (1 - Bg["dip_tepeden"]))).fillna(False).astype(bool)
        tepe = (M.KONUM >= Bg["tepe_konum"]).fillna(False).astype(bool)
        sm = ((M.ASIM <= Fe["asim_max"]) & (M.USTYOK >= Fe["ustyok_min"])).fillna(False).astype(bool)
    orta = M.KONUM.notna() & M.MAXC120.notna() & ~dip & ~tepe
    Z["DIP"] = dip; Z["TEPE_B"] = tepe; Z["ORTA"] = orta.astype(bool)
    Z["TAM_DIP"] = Z.TAM & dip; Z["TAM_ORTA"] = Z.TAM & Z.ORTA; Z["TAM_TEPE"] = Z.TAM & tepe
    Z["SM"] = sm; Z["SM_TEPE"] = sm & tepe
    return Z


def fv_baglam(z: pd.Series) -> str:
    return "DİP" if bool(z["DIP"]) else "TEPE" if bool(z["TEPE_B"]) else "ORTA" if bool(z["ORTA"]) else "TANIMSIZ"


def fv_dusuren(z: pd.Series) -> List[str]:
    """Bir günün tutmayan şartları (alt nedenle)."""
    out = []
    for s in FV_SART:
        if bool(z[s]):
            continue
        if s in ("s2", "s3", "s5") and bool(z.get(f"{s}_tanimsiz", False)):
            out.append(FV_SART_AD[s].split(" ")[0] + " geçmiş yetersiz (ölçü tanımsız)")
        elif s == "s2":
            ek = [n for n, f in (("düz değil", not bool(z["s2_duz"])), ("yeni dip / hat kırık", bool(z["s2_yenidip"]))) if f]
            out.append("(2)" + (" " + ", ".join(ek) if ek else ""))
        elif s == "s4":
            ek = [n for n, f in (("hattan uzak", not bool(z["s4_hat"])), ("pencere tepesini kırmış", not bool(z["s4_tepe"]))) if f]
            out.append("(4)" + (" " + ", ".join(ek) if ek else ""))
        else:
            out.append(FV_SART_AD[s].split(" ")[0])
    return out


def fv_hisse(df: pd.DataFrame, secim: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    M = fv_olcu(df)
    return M, fv_kural(M, secim)


# ================================================================ 2) IZGARA ve TASARIM SINAMASI (getirisiz)
def fv_izgara() -> List[Dict[str, Any]]:
    """72 nokta (önceden yazılı sırayla) ve sadelik anahtarı."""
    G = V2_ESIK["izgara"]; out = []
    for sk, dz, ht, ds, yl in itertools.product(list(G["sekil"]), G["duz"], G["hatTol"], G["dusus"], G["yol"]):
        out.append({"sekil": sk, "duz": dz, "hatTol": ht, "dusus": ds, "yol": yl})
    for i, n in enumerate(out):
        n["no"] = f"N{i + 1:02d}"
    return out


def fv_sadelik(n: Dict[str, Any]) -> Tuple[int, int, int, int, int]:
    """Küçük = daha sade (V2_ESIK 'sadelik')."""
    dz = {None: 0, 1.5: 1, 1.0: 2}[n["duz"]]
    return (dz, 0 if n["sekil"] == "S+" else 1, 0 if n["hatTol"] == 0.02 else 1, {0.10: 0, 0.15: 1, 0.20: 2}[n["dusus"]],
            0 if n["yol"] == 0.10 else 1)


def fv_etiket_seti(anahtar_yol: Optional[str] = None, cevap_yol: Optional[str] = None) -> List[Dict[str, Any]]:
    """Etiketli set: sayfalar (r20 / r60 OKUNMAZ) + örnek aralıklar. Sınıf: E-GIRIS / E-SEKIL / NEG (sayfa), ORNEK+ / NEG-ARALIK (aralık)."""
    A = json.load(open(anahtar_yol or FV_YOL["kor_anahtar"], encoding="utf-8"))
    Cv = json.load(open(cevap_yol or FV_YOL["kor_cevap"], encoding="utf-8"))
    E = V2_ESIK["etiket"]; eg = set(E["E_GIRIS"]); out = []
    for s in A["sayfalar"]:
        no = int(s["no"]); c = Cv["cevap"][str(no)]
        if c == "E":
            sinif = "E-GIRIS" if no in eg else "E-SEKIL"
        elif c == "H" or s["grup"] == "SM":
            sinif = "NEG"
        else:
            continue
        out.append({"ad": f"s{no}", "tur": "sayfa", "sinif": sinif, "no": no, "pazar": s["pazar"], "sembol": s["sembol"], "tarih": s["tarih"],
                    "grup": s["grup"], "cevap": c, "not": Cv.get("not", {}).get(str(no), "")})
    for o in E["ornek_poz"]:
        out.append({"ad": f"{o['ad']} {o['bas']}..{o['son']}", "tur": "aralik", "sinif": "ORNEK+", "pazar": o["pazar"], "sembol": o["ad"],
                    "bas": o["bas"], "son": o["son"]})
    for o in E["neg_aralik"]:
        out.append({"ad": f"{o['ad']} {o['bas']}..{o['son']}", "tur": "aralik", "sinif": "NEG-ARALIK", "pazar": o["pazar"], "sembol": o["ad"],
                    "bas": o["bas"], "son": o["son"], "not": o.get("not", "")})
    eg_bul = {e["no"] for e in out if e["sinif"] == "E-GIRIS"}
    if eg_bul != eg:
        raise FVHata(f"E-GİRİŞ sayfaları Cemal'in E cevaplarında değil: {sorted(eg - eg_bul)}")
    return out


def _fv_dgxx() -> Optional[pd.DataFrame]:
    """DGXX (yalnız NEGATİF etiket): yfinance, auto_adjust=False; 16 Kas yarım bar atılır; geçerli bar süzgeci."""
    try:
        import yfinance as yf
        d = yf.download("DGXX", start="2024-01-01", end="2026-11-14", progress=False, auto_adjust=False)
    except Exception as ex:   # ağ / paket yoksa etiket 'veri yok' yazılır
        fvlog.warning("DGXX indirilemedi: %s", ex); return None
    if d is None or not len(d):
        return None
    if isinstance(d.columns, pd.MultiIndex):
        d.columns = d.columns.get_level_values(0)
    d = d[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    d.index = pd.DatetimeIndex(d.index).tz_localize(None).normalize()
    d = d[d.index < pd.Timestamp("2026-11-16")]
    ok = np.isfinite(d).all(axis=1) & (d.High > d.Low) & (d.Volume > 0) & (d.Close > 0) & (d.Open > 0) & (d.Low > 0)
    return d[ok]


def fv_etiket_veri(et: List[Dict[str, Any]], veri: Optional[str] = None,
                   getir: Optional[Callable[[str, str], Optional[pd.DataFrame]]] = None) -> Dict[Tuple[str, str], Optional[pd.DataFrame]]:
    """(pazar, sembol) -> temiz veri. getir verilirse (test) onu kullanır."""
    gerek = sorted({(e["pazar"], e["sembol"]) for e in et})
    out: Dict[Tuple[str, str], Optional[pd.DataFrame]] = {}
    if getir is not None:
        return {k: getir(*k) for k in gerek}
    for p in sorted({p for p, _ in gerek}):
        Vd = OC.oc_veri(p, klasor=veri or FV_YOL["veri"], veri2=FV_YOL["veri2"])
        for pz, s in gerek:
            if pz == p:
                out[(pz, s)] = Vd["V"].get(s)
        del Vd
    if ("ABD", "DGXX") in out:
        out[("ABD", "DGXX")] = _fv_dgxx()
    return out


def fv_etiket_degerlendir(e: Dict[str, Any], M: Optional[pd.DataFrame], secim: Dict[str, Any]) -> Dict[str, Any]:
    """Bir etiket x bir nokta: doğru mu, şart bayrakları, düşüren."""
    r: Dict[str, Any] = {"ad": e["ad"], "sinif": e["sinif"]}
    if M is None or not len(M):
        r.update({"veri": False, "dogru": e["sinif"] in ("NEG", "NEG-ARALIK"), "not": "veri yok"}); return r
    Z = fv_kural(M, secim); r["veri"] = True
    if e["tur"] == "sayfa":
        t = pd.Timestamp(e["tarih"])
        if t not in Z.index:
            r.update({"dogru": e["sinif"] == "NEG", "not": "sayfa günü veride yok"}); return r
        z = Z.loc[t]
        r.update({k: bool(z[k]) for k in FV_SART + ["TAM"]})
        r["dusuren"] = fv_dusuren(z); r["baglam"] = fv_baglam(z); r["TAM_DIP"] = bool(z["TAM_DIP"])
        r["olcu"] = {k: (None if not np.isfinite(M.loc[t, k]) else round(float(M.loc[t, k]), 3)) for k in
                     ("ASIM", "ALTYOK", "DUZ", "DUSUS", "YOL", "TEPE", "KONUM")}
        hd = M.loc[t, "HAT"] / M.loc[t, "ONC30"] - 1 if np.isfinite(M.loc[t, "ONC30"]) else np.nan
        r["olcu"]["HAT_ONC30"] = None if not np.isfinite(hd) else round(float(hd), 3)
        if e["sinif"] == "E-GIRIS":
            r["dogru"] = r["TAM"]
        elif e["sinif"] == "E-SEKIL":
            r["dogru"] = r["s1"] and not r["TAM"]
        else:
            r["dogru"] = not r["TAM"]
        return r
    m = (Z.index >= pd.Timestamp(e["bas"])) & (Z.index <= pd.Timestamp(e["son"]))
    Zw = Z[m]
    r["gun"] = int(len(Zw)); r["TAM_gun"] = [str(t.date()) for t in Zw.index[Zw.TAM.to_numpy(bool)]]
    r["sart_gun"] = {s: int(Zw[s].sum()) for s in FV_SART}
    r["baglam_gun"] = pd.Series([fv_baglam(Zw.iloc[i]) for i in range(len(Zw))]).value_counts().to_dict() if len(Zw) else {}
    r["baglam_TAM"] = pd.Series([fv_baglam(Zw.loc[t]) for t in Zw.index[Zw.TAM.to_numpy(bool)]]).value_counts().to_dict() if Zw.TAM.any() else {}
    r["TAM_DIP_gun"] = int(Zw.TAM_DIP.sum())
    if len(Zw):
        say = Zw[FV_SART].sum(axis=1).to_numpy()
        j = int(np.argmax(say)); r["en_yakin"] = str(Zw.index[j].date()); r["dusuren"] = fv_dusuren(Zw.iloc[j])
    else:
        r["dusuren"] = ["aralıkta bar yok"]
    r["dogru"] = (len(r["TAM_gun"]) > 0) if e["sinif"] == "ORNEK+" else (len(r["TAM_gun"]) == 0)
    return r


def fv_puan(R: List[Dict[str, Any]]) -> Dict[str, int]:
    """Bir noktanın etiket sonuçları -> puan bileşenleri."""
    def say(s):
        return int(sum(1 for r in R if r["sinif"] == s and r["dogru"]))
    out = {"yakalanan_E_GIRIS": say("E-GIRIS"), "yakalanan_ORNEK": say("ORNEK+"), "elenen_NEG": say("NEG"), "elenen_NEG_ARALIK": say("NEG-ARALIK"),
           "sekil_E_SEKIL": say("E-SEKIL")}
    out["puan"] = int(sum(out.values()))
    out["en_cok"] = int(len(R))
    return out


def fv_secim_yap(sonuc: List[Dict[str, Any]]) -> Dict[str, Any]:
    """En yüksek puan; eşitlikte en sade (fv_sadelik sözlük sırası)."""
    en = max(s["puan"]["puan"] for s in sonuc)
    aday = [s for s in sonuc if s["puan"]["puan"] == en]
    aday.sort(key=lambda s: fv_sadelik(s["nokta"]))
    return {"nokta": {k: v for k, v in aday[0]["nokta"].items()}, "puan": aday[0]["puan"], "esit_sayisi": len(aday),
            "esitler": [a["nokta"]["no"] for a in aday]}


def fv_tasarim(veri: Optional[str] = None, getir: Optional[Callable[[str, str], Optional[pd.DataFrame]]] = None,
               anahtar_yol: Optional[str] = None, cevap_yol: Optional[str] = None) -> Dict[str, Any]:
    """AŞAMA 1: etiket seti x 72 nokta; puan, seçim, seçilen noktada tablo. GETİRİ HESAPLANMAZ / OKUNMAZ."""
    et = fv_etiket_seti(anahtar_yol, cevap_yol)
    VV = fv_etiket_veri(et, veri, getir)
    MM = {k: (fv_olcu(d) if d is not None and len(d) else None) for k, d in VV.items()}
    sonuc = []
    for n in fv_izgara():
        R = [fv_etiket_degerlendir(e, MM[(e["pazar"], e["sembol"])], n) for e in et]
        sonuc.append({"nokta": n, "puan": fv_puan(R), "R": R})
    sec = fv_secim_yap(sonuc)
    secR = next(s["R"] for s in sonuc if s["nokta"]["no"] == sec["nokta"]["no"])
    veri_not = {f"{p} {s}": ("yok" if d is None else f"{len(d)} bar, {d.index[0].date()} .. {d.index[-1].date()}") for (p, s), d in VV.items()}
    return {"etiket": et, "sonuc": sonuc, "secim": sec, "secim_R": secR, "veri_not": veri_not}


def _fv_secim_json(n: Dict[str, Any]) -> str:
    return json.dumps({k: n[k] for k in ("no", "sekil", "duz", "hatTol", "dusus", "yol")}, sort_keys=True, ensure_ascii=False)


def _fv_nokta_metin(n: Dict[str, Any]) -> str:
    a, b = V2_ESIK["izgara"]["sekil"][n["sekil"]]
    return (f"{n['no']}: şekil {n['sekil']} (ASIM >= {a:.2f}, ALTYOK >= {b:.2f}), düz {'kapalı' if n['duz'] is None else n['duz']}, "
            f"hatTol {n['hatTol']}, düşüş >= {n['dusus']}, yol <= {n['yol']}").replace(".", ",")


def _fv_tf(x: Any) -> str:
    return "-" if x is None else ("✓" if x else "·")


def fv_tasarim_metni(T: Dict[str, Any]) -> str:
    sec = T["secim"]; n = sec["nokta"]; S = T["sonuc"]; R = T["secim_R"]
    pu = [s["puan"]["puan"] for s in S]
    s = ["# FITIL_V2 — TASARIM SINAMASI (AŞAMA 1; getirisiz)", "", FV_SURUM, "",
         f"- ZAMAN (UTC): `{_fv_simdi()}`", f"- TASARIM_KOD_SHA: `{_fv_sha_dosya(FV_YOL['kod'])}`",
         f"- KOR_ANAHTAR_SHA: `{_fv_sha_dosya(FV_YOL['kor_anahtar'])}` (yalnız sayfa / pazar / sembol / tarih / grup okundu; r20 / r60 OKUNMADI)",
         f"- KOR_CEVAP_SHA: `{_fv_sha_dosya(FV_YOL['kor_cevap'])}`", "",
         "Bu sınama hiçbir getiri / eş farkı / sonraki fiyat hesaplamadı ve okumadı; yalnız Cemal'in t'de biten sayfaları ve örnek aralıkları "
         "üzerinde şartların doğru / yanlış olduğu sayıldı. Izgara (72 nokta), puan ve eşitlik bozma (sadelik) kuralı koşudan önce kodda yazılıydı.", "",
         "## Etiket seti", "",
         f"- E-GİRİŞ (POZİTİF, sayfa günü TAM beklenir): sayfa {', '.join(str(e['no']) for e in T['etiket'] if e['sinif'] == 'E-GIRIS')}",
         f"- E-ŞEKİL ((1) VAR ama TAM YOK beklenir): sayfa {', '.join(str(e['no']) for e in T['etiket'] if e['sinif'] == 'E-SEKIL')}",
         f"- NEGATİF sayfa (TAM YOK beklenir; H + S- sayfalarında E olmayan): {', '.join(str(e['no']) for e in T['etiket'] if e['sinif'] == 'NEG')}",
         "- ÖRNEK+ (aralıkta en az bir TAM günü): " + "; ".join(e["ad"] for e in T["etiket"] if e["sinif"] == "ORNEK+"),
         "- NEGATİF aralık (hiç TAM günü yok): " + "; ".join(e["ad"] for e in T["etiket"] if e["sinif"] == "NEG-ARALIK"),
         f"- Puan: {V2_ESIK['puan']}.", f"- Eşitlik: {V2_ESIK['sadelik']}.", "",
         "Veri: " + "; ".join(f"{k}: {v}" for k, v in T["veri_not"].items()), "",
         "## SEÇİLEN NOKTA", "", f"**{_fv_nokta_metin(n)}**", "",
         f"Puan {sec['puan']['puan']} / {sec['puan']['en_cok']}: E-GİRİŞ {sec['puan']['yakalanan_E_GIRIS']} / 7, örnek {sec['puan']['yakalanan_ORNEK']} / 3, "
         f"NEGATİF sayfa elenen {sec['puan']['elenen_NEG']} / 10, NEGATİF aralık elenen {sec['puan']['elenen_NEG_ARALIK']} / 2, E-ŞEKİL (1) var TAM yok "
         f"{sec['puan']['sekil_E_SEKIL']} / 12. Aynı puanlı nokta sayısı {sec['esit_sayisi']} ({', '.join(sec['esitler'])}); sadelik sırasıyla ilki seçildi.", "",
         f"SECIM_JSON: `{_fv_secim_json(n)}`", "",
         "## ETİKET x SEÇİLEN NOKTA (✓ şart tuttu, · tutmadı; sayfa günü t)", "",
         "| Etiket | Sınıf | Cemal | (1) | (2) | (3) | (4) | (5) | TAM | doğru mu | düşüren şart | BAĞLAM (konum 250) | TAM_DIP | ASIM / ALTYOK | düz | HAT / önceki 30 dip | düşüş (60 bar tepesinden) | yol (C / HAT) | 120 bar tepesinden aşağı |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    etd = {e["ad"]: e for e in T["etiket"]}
    for r in sorted(R, key=lambda r: (["E-GIRIS", "ORNEK+", "E-SEKIL", "NEG", "NEG-ARALIK"].index(r["sinif"]), etd[r["ad"]].get("no", 0))):
        e = etd[r["ad"]]
        if not r.get("veri", True) or "not" in r and e["tur"] == "sayfa":
            s.append(f"| {r['ad']} | {r['sinif']} | {e.get('cevap', '-')} | - | - | - | - | - | - | {'EVET' if r['dogru'] else 'HAYIR'} | {r.get('not')} | | | | | | | | |")
            continue
        if e["tur"] == "sayfa":
            o = r["olcu"]
            s.append(f"| {e['pazar']} No {e['no']} ({e['grup']}) | {r['sinif']} | {e['cevap']}: {e['not'][:70].replace('|', '/')} | "
                     + " | ".join(_fv_tf(r[k]) for k in FV_SART) + f" | {'TAM' if r['TAM'] else '·'} | {'EVET' if r['dogru'] else 'HAYIR'} | "
                     f"{', '.join(r['dusuren']) or '-'} | {r['baglam']} ({_sy(o['KONUM'])}) | {'✓' if r['TAM_DIP'] else '·'} | {_sy(o['ASIM'])} / {_sy(o['ALTYOK'])} | {_sy(o['DUZ'])} | {_yz(o['HAT_ONC30'])} | "
                     f"{_yz(o['DUSUS'])} | {_yz(o['YOL'])} | {_yz(o['TEPE'])} |")
        else:
            sg = r.get("sart_gun", {})
            s.append(f"| {e['ad']} | {r['sinif']} | - | " + " | ".join(f"{sg.get(k, 0)}/{r['gun']}" for k in FV_SART)
                     + f" | {len(r['TAM_gun'])} gün | {'EVET' if r['dogru'] else 'HAYIR'} | "
                     + (f"TAM günleri: {', '.join(r['TAM_gun'][:8])}" if r["TAM_gun"] else f"en yakın gün {r.get('en_yakin')}: {', '.join(r['dusuren'])}")
                     + f" | aralık günleri {', '.join(f'{k} {v}' for k, v in r.get('baglam_gun', {}).items())}; TAM günleri "
                     + (', '.join(f'{k} {v}' for k, v in r.get('baglam_TAM', {}).items()) or '-')
                     + f" | {r.get('TAM_DIP_gun', 0)} gün | | | | | | |")
    bz = [(etd[r["ad"]], r) for r in R if r["sinif"] in ("E-GIRIS", "ORNEK+")]
    s += ["", "BAĞLAM (EK, sonuç görülmeden; ızgaraya ve puana girmez): " + V2_ESIK["baglam"]["tanim"] + ".",
          "E-GİRİŞ sayfaları ve 3 örneğin bağlamı: " + "; ".join(
              (f"No {e['no']} {r.get('baglam', '-')}" if e["tur"] == "sayfa" else
               f"{e['sembol']} TAM günleri {', '.join(f'{k} {v}' for k, v in r.get('baglam_TAM', {}).items()) or 'yok'} (aralık: "
               f"{', '.join(f'{k} {v}' for k, v in r.get('baglam_gun', {}).items())})") for e, r in bz) + ".",
          f"Seçilen noktada TAM_DIP (ana satır) etiket setinde: E-GİRİŞ {sum(1 for e, r in bz if e['tur'] == 'sayfa' and r.get('TAM_DIP'))} / 7, "
          f"örnek aralıkta TAM_DIP günü olan {sum(1 for e, r in bz if e['tur'] == 'aralik' and r.get('TAM_DIP_gun', 0) > 0)} / 3, NEGATİF sayfada TAM_DIP "
          f"{sum(1 for r in R if r['sinif'] == 'NEG' and r.get('TAM_DIP'))} / 10, E-ŞEKİL sayfada TAM_DIP {sum(1 for r in R if r['sinif'] == 'E-SEKIL' and r.get('TAM_DIP'))} / 12 (bilgi).",
          "", "Aralık satırlarında (1)-(5) sütunu = şartın tuttuğu gün / aralıktaki gün; TAM yoksa 'en yakın gün' en çok şartın tuttuğu ilk gündür.", "",
          "## IZGARA ÖZETİ (72 nokta)", "",
          f"- Puan dağılımı: en düşük {min(pu)}, medyan {int(np.median(pu))}, en yüksek {max(pu)}; en yüksek puanlı nokta sayısı {sec['esit_sayisi']}.",
          "- Bileşen tavanları (her bileşenin 72 noktadaki en yüksek değeri): " + ", ".join(
              f"{k} {max(x['puan'][k] for x in S)}" for k in ("yakalanan_E_GIRIS", "yakalanan_ORNEK", "elenen_NEG", "elenen_NEG_ARALIK", "sekil_E_SEKIL")),
          "", "| Nokta | şekil | düz | hatTol | düşüş | yol | E-GİRİŞ /7 | örnek /3 | NEG sayfa /10 | NEG aralık /2 | E-ŞEKİL /12 | PUAN |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in sorted(S, key=lambda x: (-x["puan"]["puan"], fv_sadelik(x["nokta"]))):
        q = x["nokta"]; p = x["puan"]
        s.append(f"| {q['no']}{' **SEÇİLEN**' if q['no'] == n['no'] else ''} | {q['sekil']} | {'kapalı' if q['duz'] is None else q['duz']} | {q['hatTol']} | "
                 f"{q['dusus']} | {q['yol']} | {p['yakalanan_E_GIRIS']} | {p['yakalanan_ORNEK']} | {p['elenen_NEG']} | {p['elenen_NEG_ARALIK']} | "
                 f"{p['sekil_E_SEKIL']} | {p['puan']} |")
    s += ["", "## SINIR", "",
          "- Etiket seti küçük (7 E-GİRİŞ + 3 örnek pozitif, 12 E-ŞEKİL, 10 + 2 negatif) ve sayfalar Ç187 S+ / S- seçiminden geldi: eşik seçimi tanımın "
          "Cemal'in gözüne uydurulmasıdır, bulgu değildir; ölçüm AŞAMA 2'de etiket setinin dışındaki bütün evrende ve önceden yazılı kuralla yapılır.",
          "- Cemal'in E-GİRİŞ notları (dönüm / akümülasyon / stoplu girilir) savunma hattı ve düşüş bağlamı ister; E-ŞEKİL notları (yol almış / hat "
          "kırık / aşağı) TAM'ın eleyeceği durumlardır. Tablodaki düşüren şart sütunu bunun ne kadar tuttuğunu gösterir.", ""]
    return "\n".join(s)


def fv_tasarim_yaz(cikti: Optional[str] = None, veri: Optional[str] = None) -> Dict[str, Any]:
    if os.path.exists(_fv_yol("onkayit", cikti)):
        raise FVHata("ON_KAYIT.md var: tasarım ön kayıttan sonra yeniden yazılmaz (SAPMA)")
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    T = fv_tasarim(veri)
    _fv_yaz(_fv_yol("tasarim", cikti), fv_tasarim_metni(T), "tasarım")
    fvlog.info("TASARIM.md yazıldı; seçilen %s puan %d", T["secim"]["nokta"]["no"], T["secim"]["puan"]["puan"])
    return T


def fv_tasarim_secim_oku(yol: Optional[str] = None) -> Dict[str, Any]:
    yol = yol or _fv_yol("tasarim")
    if not os.path.exists(yol):
        raise FVHata(f"TASARIM.md yok ({yol}): önce `python FITIL_V2.py tasarim`")
    m = re.search(r"SECIM_JSON:\s*`(\{[^`]+\})`", open(yol, encoding="utf-8").read())
    if not m:
        raise FVHata("TASARIM.md'de SECIM_JSON satırı yok")
    return json.loads(m.group(1))


def fv_secim_denetle(yol: Optional[str] = None) -> Dict[str, Any]:
    """V2_SECIM kodda yazılı ve TASARIM.md seçimiyle aynı olmalı."""
    if V2_SECIM is None:
        raise FVHata("V2_SECIM yok: tasarım seçimi koda yazılmadan ön kayıt / koşu yapılmaz")
    t = fv_tasarim_secim_oku(yol)
    k = json.loads(_fv_secim_json(V2_SECIM))
    if t != k:
        raise FVHata(f"V2_SECIM ({k}) TASARIM.md seçimiyle ({t}) aynı değil: SAPMA")
    if not any(all(n[a] == V2_SECIM[a] for a in ("sekil", "duz", "hatTol", "dusus", "yol")) and n["no"] == V2_SECIM["no"] for n in fv_izgara()):
        raise FVHata("V2_SECIM ızgarada yok")
    return t


# ================================================================ 3) EVREN SİNYALLERİ ve SAYIM (getirisiz)
def fv_sinyaller(Vd: Dict[str, Any], pazar: str, secim: Optional[Dict[str, Any]] = None, kirilim: bool = False,
                 hy: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """oc_veri -> durum günleri DataFrame[sembol, tarih, pazar, satir] (+ kirilim / tavan / hat ve s1..s5). hy verilirse hisse-yıl sayımı doldurulur."""
    secim = secim or V2_SECIM
    if secim is None:
        raise FVHata("seçim yok")
    V = Vd["V"]; evb = Vd.get("evren_bas", {}); sat = []
    for s in sorted(V):
        M, Z = fv_hisse(V[s], secim)
        if not len(M):
            continue
        tanimli = M[["ASIM", "DUZ", "ONC30", "MAXC60", "MAXC120", "KONUM"]].notna().all(axis=1)
        if s in evb:
            ev = M.index >= pd.Timestamp(evb[s]); Z = Z[ev]; tanimli = tanimli[ev]; M = M[ev]
        if hy is not None:
            dn = OC._oc_donem(pd.Series(M.index[tanimli.to_numpy(bool)]), OC.OC_ESIK)
            for d_, c_ in pd.Series(dn).value_counts().items():
                if d_:
                    hy.setdefault("bar", {}).setdefault(d_, 0); hy["bar"][d_] += int(c_)
            yil = pd.Series(M.index[tanimli.to_numpy(bool)].year).value_counts()
            for y_, c_ in yil.items():
                if c_ >= 60:
                    hy.setdefault("hisse_yil", {}).setdefault(int(y_), 0); hy["hisse_yil"][int(y_)] += 1
                    if Z.TAM_DIP[tanimli.to_numpy(bool) & (M.index.year == y_)].any():
                        hy.setdefault("tam_yil", {}).setdefault(int(y_), 0); hy["tam_yil"][int(y_)] += 1
        for ad in V2_ESIK["satirlar"]:
            m = Z[ad].to_numpy(bool)
            if not m.any():
                continue
            g = Z.index[m]
            x = pd.DataFrame({"sembol": s, "tarih": g, "pazar": pazar, "satir": ad,
                              "baglam": np.where(Z.DIP.to_numpy(bool)[m], "DİP", np.where(Z.TEPE_B.to_numpy(bool)[m], "TEPE",
                                                 np.where(Z.ORTA.to_numpy(bool)[m], "ORTA", "TANIMSIZ")))})
            if kirilim:
                x["kirilim"] = fv_kirilim_seri(V[s], M, g)
                x["tavan"] = M.loc[g, "HMAXW"].to_numpy(float); x["hat"] = M.loc[g, "HAT"].to_numpy(float)
            sat.append(x)
    if not sat:
        return pd.DataFrame(columns=["sembol", "tarih", "pazar", "satir"])
    X = pd.concat(sat, ignore_index=True)
    X["tarih"] = pd.to_datetime(X.tarih)
    return X.sort_values(["satir", "sembol", "tarih"]).reset_index(drop=True)


def fv_kirilim(C: np.ndarray, i: int, tavan: float, hat: float, ufuk: Optional[int] = None, carpan: Optional[float] = None) -> str:
    """t = i. geçerli bar; t+1 .. t+ufuk kapanışlarında ilk C > tavan (KIRILIM) / C < hat x carpan (STOP); aynı gün yok (kapanış tek);
    hiçbiri -> YOK; bar yetmezse ÖLÇÜLMEZ."""
    Sb = V2_ESIK["sabit"]; ufuk = ufuk or Sb["kirilim_ufuk"]; carpan = carpan or Sb["stop_carpan"]
    if not (np.isfinite(tavan) and np.isfinite(hat)) or i + ufuk >= len(C):
        return "OLCULMEZ"
    w = C[i + 1:i + 1 + ufuk]
    u = np.flatnonzero(w > tavan); a = np.flatnonzero(w < hat * carpan)
    u0 = u[0] if len(u) else 10 ** 9; a0 = a[0] if len(a) else 10 ** 9
    if u0 < a0:
        return "KIRILIM"
    if a0 < u0:
        return "STOP"
    return "YOK"


def fv_kirilim_seri(df: pd.DataFrame, M: pd.DataFrame, gunler: pd.DatetimeIndex) -> List[str]:
    C = M.C.to_numpy(float); ix = M.index
    return [fv_kirilim(C, int(ix.get_loc(t)), float(M.loc[t, "HMAXW"]), float(M.loc[t, "HAT"])) for t in gunler]


def fv_sayim(X: pd.DataFrame, P: Dict[str, Any], hy: Dict[str, Any]) -> Dict[str, Any]:
    """GETİRİSİZ: durum günü (sinyal tarihi dönemi) ve cetvel sonrası tekil olay (giriş dönemi); TAM için hisse-yıl oranları."""
    out: Dict[str, Any] = {}
    for sat in V2_ESIK["satirlar"]:
        x = X[X.satir == sat][["sembol", "tarih", "pazar"]]
        Y, say = OC.oc_olay_hazirla(x, P)
        dg = pd.Series(OC._oc_donem(x.tarih, OC.OC_ESIK)).value_counts().to_dict() if len(x) else {}
        ol = Y.donem.value_counts().to_dict() if len(Y) else {}
        xb = X[X.satir == sat]
        out[sat] = {"durum_gunu": {k: int(v) for k, v in dg.items() if k}, "olay": {k: int(v) for k, v in ol.items() if k},
                    "dusme": {k: int(v) for k, v in say.items()}, "hisse": int(x.sembol.nunique()) if len(x) else 0,
                    "baglam": {k: int(v) for k, v in xb.baglam.value_counts().items()} if len(xb) and "baglam" in xb else {}}
    out["hisse_yil"] = {"bar": hy.get("bar", {}), "hisse_yil": {str(k): v for k, v in sorted(hy.get("hisse_yil", {}).items())},
                        "tam_yil": {str(k): v for k, v in sorted(hy.get("tam_yil", {}).items())}}
    return out


# ================================================================ 4) ÖN KAYIT
def fv_kontrol_tablosu() -> str:
    import IZ_KARNE as IK
    sat = ["## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
           "|---|---|---|---|"]
    for k in IK.IK_KONTROL:
        y, kn = FV_KONTROL.get(k["kod"], ("", ""))
        sat.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn.replace('|', '/')} |")
    return "\n".join(sat)


def _fv_is_tanimi_git() -> Dict[str, str]:
    try:
        return OC._oc_git_islenmis(FV_YOL["is_tanimi"])
    except OC.OCHata as ex:
        raise FVHata(f"iş tanımı git kapısı: {ex}")


def _fv_say_tablo(say: Dict[str, Dict[str, Any]]) -> List[str]:
    s = ["| Satır | Pazar | hisse | durum günü 2016-22 / 2023 / 2024-26 | OLAY (tekil, giriş dönemi) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |",
         "|---|---|---|---|---|---|---|"]
    for sat in V2_ESIK["satirlar"]:
        for p, c in say.items():
            v = c[sat]; dg = v["durum_gunu"]; ol = v["olay"]
            s.append(f"| {sat} | {p} | {v['hisse']} | {dg.get('2016-22', 0)} / {dg.get('2023', 0)} / {dg.get('2024-26', 0)} | {ol.get('2016-22', 0)} / "
                     f"{ol.get('2023', 0)} / {ol.get('2024-26', 0)} | {v['dusme'].get('tekil', 0)} | {v['dusme'].get('havuz_disi', 0)} |")
    s += ["", "### Bağlam dağılımı (durum günü; DİP / ORTA / TEPE / TANIMSIZ)", "", "| Satır | Pazar | DİP | ORTA | TEPE | TANIMSIZ |", "|---|---|---|---|---|---|"]
    for sat in ("TAM", "S1", "S12", "S123"):
        for p, c in say.items():
            b = c[sat].get("baglam", {})
            s.append(f"| {sat} | {p} | {b.get('DİP', 0)} | {b.get('ORTA', 0)} | {b.get('TEPE', 0)} | {b.get('TANIMSIZ', 0)} |")
    s += ["", "### Çöl nadir mi? (TAM_DIP = ana satır; hisse-yıl)", "",
          "| Pazar | dönem | ölçülebilir hisse-gün | hisse-yıl (/ 252) | TAM_DIP durum günü | TAM_DIP olay (tekil) | durum günü / hisse-yıl | olay / hisse-yıl |",
          "|---|---|---|---|---|---|---|---|"]
    for p, c in say.items():
        b = c["hisse_yil"]["bar"]
        for d in ("2016-22", "2023", "2024-26"):
            hyil = b.get(d, 0) / 252; dg = c["TAM_DIP"]["durum_gunu"].get(d, 0); ol = c["TAM_DIP"]["olay"].get(d, 0)
            s.append(f"| {p} | {d} | {b.get(d, 0)} | {hyil:.0f} | {dg} | {ol} | {(dg / hyil if hyil else float('nan')):.3f} | "
                     f"{(ol / hyil if hyil else float('nan')):.3f} |".replace(".", ","))
    s += ["", "| Pazar | takvim yılı: ölçülebilir hisse-yıl (>= 60 ölçülebilir gün) / en az bir TAM_DIP günü olan / pay |", "|---|---|"]
    for p, c in say.items():
        h = c["hisse_yil"]["hisse_yil"]; t = c["hisse_yil"]["tam_yil"]
        s.append(f"| {p} | " + "; ".join(f"{y}: {h[y]} / {t.get(y, 0)} / {100 * t.get(y, 0) / h[y]:.1f}%".replace(".", ",") for y in h) + " |")
    return s


def fv_onkayit_metni(say: Dict[str, Any], vsha: Dict[str, str], notlar: Dict[str, List[str]], git_it: Dict[str, str]) -> str:
    E = V2_ESIK; n = V2_SECIM; p = fv_prm(n)
    s = ["# FITIL_V2 — ÖN KAYIT (S+ v2 'TAM GİRİLİR')", "", FV_SURUM, "",
         f"- V2_ESIK_SHA: `{fv_esik_sha()}` (V2_ESIK + V2_SECIM)", f"- V2_KOD_SHA: `{_fv_sha_dosya(FV_YOL['kod'])}`",
         f"- IS_TANIMI_SHA: `{_fv_sha_dosya(FV_YOL['is_tanimi'])}` (git {git_it.get('commit', '-')[:10]}, {git_it.get('commit_zamani', '-')})",
         f"- TASARIM_SHA: `{_fv_sha_dosya(_fv_yol('tasarim'))}`",
         f"- KOR_ANAHTAR_SHA: `{_fv_sha_dosya(FV_YOL['kor_anahtar'])}`", f"- KOR_CEVAP_SHA: `{_fv_sha_dosya(FV_YOL['kor_cevap'])}`",
         f"- SECIM_JSON: `{_fv_secim_json(n)}`",
         f"- ZAMAN (UTC): `{_fv_simdi()}`", "",
         "Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı ve okunmadı (yalnız olay sayımı, getirisiz). `kos` kontrol "
         "listesi, cetvel üç sha'sı, V2_ESIK / kod / tasarım / iş tanımı sha'sı ve bu dosyanın git kaydı tutmazsa durur. Eşikler sonuç görülünce değişmez.", "",
         "## Cetvel mühür satırları (ORTAK_CETVEL; aynen)", "", OC.oc_kapi_satirlari(), "",
         "## Tanım ve SEÇİLEN eşikler (tasarım sınaması, TASARIM.md)", "",
         f"- Bar: {E['bar']}.", f"- Pencere: {E['pencere']}.",
         f"- Seçilen nokta: {_fv_nokta_metin(n)}.",
         f"- (1) ŞEKİL: ASIM >= {p['asim']:.2f} VE ALTYOK >= {p['altyok']:.2f}.",
         f"- (2) SAVUNMA HATTI: {E['tanim']['s2']}; duz = {'kapalı' if p['duz'] is None else p['duz']}, tol = {p['hatTol']}.",
         f"- (3) DÖNÜM: {E['tanim']['s3']}; dusus = {p['dusus']}.",
         f"- (4) YOL ALMAMIŞ: {E['tanim']['s4']}; yol = {p['yol']}.",
         f"- (5) TEPEDE DEĞİL: {E['tanim']['s5']}.", f"- {E['tanim']['tam']}.", f"- BAĞLAM: {E['baglam']['tanim']}.", f"- Çıkış bilgisi: {E['tanim']['cikis_bilgi']}.", "",
         "Satırlar:", ""] + [f"- {k}: {v}" for k, v in E["satirlar"].items()] + ["",
         f"- Olay: {E['olay']}.", "",
         "## Karar kuralı (önceden yazılı)", "", f"- ANA: {E['karar']['ana']}.", f"- BİLGİ: {E['karar']['bilgi']}.",
         f"- Olasılık: {E['karar']['olasilik']}.", f"- Kırılım / stop: {E['karar']['kirilim']}.",
         f"- Geleceğe bakma denetimi: {E['gelecek_denetimi']['tanim']}.", "",
         "## KÖR SET 2 (önceden yazılı)", "", f"- {E['kor2']['tanim']}.",
         f"- Grup: TAM BIST {E['kor2']['grup']['TAM']['BIST']} + ABD {E['kor2']['grup']['TAM']['ABD']}; DEĞİL BIST {E['kor2']['grup']['DEGIL']['BIST']} + "
         f"ABD {E['kor2']['grup']['DEGIL']['ABD']}; tarih {E['kor2']['bas']} .. {E['kor2']['son']}; tohum {E['kor2']['tohum']}.",
         f"- Soru: {E['kor2']['soru']}.", f"- Karar: {E['kor2']['karar']}.", "",
         "## Veri", ""] + [f"- V_{q}.pkl sha256: `{v}`" for q, v in vsha.items()] + \
        [f"- {q} oc_veri notu: {'; '.join(x)}" for q, x in notlar.items()] + ["",
         "## OLAY SAYIMI (getirisiz; durum günü sinyal tarihine, olay giriş tarihine göre dönem)", ""] + _fv_say_tablo(say) + ["",
         "Kural: hücre n < 30 ise ÖLÇÜLEMEDİ; güç yetersizse DESTEKLENMEDİ denmez.", "",
         "## SAPMA / sınır (sonuç görülmeden yazıldı)", "",
         "- SAPMA-1 (ana model kararı, 17 Kas; tasarımdan önce, getiri görülmeden): iş tanımı §2 (4)'teki 'C_t < max(High, W)' W t'yi içerdiği için "
         "neredeyse boştu (yalnız C_t = H_t = pencere tepesi iken düşer; alt ajan HATA 1). Yeni kural: C_t <= max(High, W \\ {t}) (t hariç önceki 9 "
         "pencere barı). İlk yarı aynı. TASARIM aynı 72 noktalı ızgara ve aynı mekanik seçim kuralıyla yeniden koşuldu; bu ön kayıt onun üzerine yazıldı.",
         "- SÜREÇ NOTU (alt ajan HATA 4): AŞAMA 1 keşfinde kor_anahtar.json'un ilk ~4 KB'si `head` ile okunurken ilk ~11 sayfanın r20 / r60 değerleri "
         "ekrana geldi. Tasarım kodu bu alanları okumaz (test 'etiketlerde r20 / r60 alanı yok'); eşik seçimi önceden yazılı mekanik puan + sadelik "
         "kuralıyla yapıldı. Yine de AŞAMA 1 getiri yasağına süreç ihlalidir.",
         "- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD'dir (oc_veri notunda).",
         "- Tasarım seti küçük ve Ç187 S+ / S- sayfalarından geldi; seçilen eşik tanım kalibrasyonudur, bulgu değildir.",
         "- (3) ve (5) düşmüş hisseleri seçer: hayatta kalma yanlılığı (bugün işlem görenler) bu satırda getiriyi yukarı itebilir; kısa vadeli dönüş "
         "eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler).",
         "- ON_KAYIT.md'yi alt ajan git'e işleyemez: ana model işler; `kos` git kaydını ister (--gitsiz yalnız SAPMA olarak yazılır).", "",
         fv_kontrol_tablosu(), "",
         "## Test", "", "`python test_fitil_v2.py` (sentetik: ölçüler elle, her şart tek tek düşürülür, geleceğe bakma kesme testi, ızgara 72 / sadelik, "
         "etiket seti sayıları, puan, kırılım / stop, kör cevap ayrıştırma / karar, kapı, e-posta / anahtar taraması, kör sayfa ad / tarih sızıntısı).", ""]
    return "\n".join(s)


def fv_onkayit_yaz(cikti: Optional[str] = None, veri: Optional[str] = None, uzerine: bool = False) -> str:
    yol = _fv_yol("onkayit", cikti)
    if os.path.exists(yol):
        try:
            OC._oc_git_islenmis(yol)
            raise FVHata(f"ön kayıt git'e işlenmiş ({yol}); üzerine yazılmaz")
        except OC.OCHata:
            if not uzerine:
                raise FVHata(f"ön kayıt var ({yol}); git'e işlenmemişse --uzerine-yaz")
    if os.path.exists(_fv_yol("sonuc", cikti)):
        raise FVHata("sonuc.json var: ölçüm koşulmuş, ön kayıt yeniden yazılamaz (SAPMA)")
    fv_secim_denetle(_fv_yol("tasarim", cikti))
    git_it = _fv_is_tanimi_git()
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    say, vsha, notlar = {}, {}, {}
    for p in OC.OC_ESIK["pazar"]:
        vsha[p] = _fv_sha_dosya(os.path.join(veri or FV_YOL["veri"], f"V_{p}.pkl"))
        Vd = OC.oc_veri(p, klasor=veri or FV_YOL["veri"], veri2=FV_YOL["veri2"]); notlar[p] = list(Vd.get("not", []))
        hy: Dict[str, Any] = {}
        X = fv_sinyaller(Vd, p, hy=hy); P = OC.oc_panel(Vd)
        say[p] = fv_sayim(X, P, hy)
        fvlog.info("%s: durum günü %s", p, X.satir.value_counts().to_dict() if len(X) else {})
        del Vd, P, X
    metin = fv_onkayit_metni(say, vsha, notlar, git_it)
    _fv_yaz(yol, metin, "ön kayıt")
    fvlog.info("ön kayıt yazıldı: %s", yol)
    return yol


_FV_DESEN = {"esik": r"V2_ESIK_SHA:\s*`([0-9a-f]{64})`", "kod": r"V2_KOD_SHA:\s*`([0-9a-f]{64})`", "is_tanimi": r"IS_TANIMI_SHA:\s*`([0-9a-f]{64})`",
             "tasarim": r"TASARIM_SHA:\s*`([0-9a-f]{64})`", "kor_anahtar": r"KOR_ANAHTAR_SHA:\s*`([0-9a-f]{64})`",
             "kor_cevap": r"KOR_CEVAP_SHA:\s*`([0-9a-f]{64})`"}


def fv_onkayit_dogrula(yol: Optional[str] = None, git: bool = True, cikti: Optional[str] = None) -> Dict[str, Any]:
    yol = yol or _fv_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise FVHata(f"ön kayıt yok ({yol}): önce `python FITIL_V2.py onkayit`")
    metin = open(yol, encoding="utf-8").read(); b = {}
    for ad, desen in _FV_DESEN.items():
        m = re.search(desen, metin)
        if not m:
            raise FVHata(f"ön kayıt bozuk: '{ad}' satırı yok")
        b[ad] = m.group(1)
    simdi = {"esik": fv_esik_sha(), "kod": _fv_sha_dosya(FV_YOL["kod"]), "is_tanimi": _fv_sha_dosya(FV_YOL["is_tanimi"]),
             "tasarim": _fv_sha_dosya(_fv_yol("tasarim", cikti or os.path.dirname(yol))), "kor_anahtar": _fv_sha_dosya(FV_YOL["kor_anahtar"]),
             "kor_cevap": _fv_sha_dosya(FV_YOL["kor_cevap"])}
    for ad in simdi:
        if b[ad] != simdi[ad]:
            raise FVHata(f"{ad} sha tutmuyor (ön kayıt {b[ad][:12]}…, şimdi {simdi[ad][:12]}…): koşu DURDU (SAPMA)")
    fv_secim_denetle(_fv_yol("tasarim", cikti or os.path.dirname(yol)))
    out: Dict[str, Any] = {"yol": yol, **b, "onkayit_sha": _fv_sha_dosya(yol),
                           "onkayit_yazim_utc": re.search(r"ZAMAN \(UTC\):\s*`([^`]+)`", metin).group(1)}
    out["git_is_tanimi"] = _fv_is_tanimi_git()
    try:
        out["git_onkayit"] = OC._oc_git_islenmis(yol)
    except OC.OCHata as ex:
        if git:
            raise FVHata(f"{ex} (ana model ön kaydı işlemeli; alt ajan --gitsiz ile koşarsa SAPMA)")
        out["git_onkayit"] = f"İŞLENMEDİ (gitsiz koşu; ön kayıt sha {out['onkayit_sha'][:12]}…, yazım {out['onkayit_yazim_utc']})"
    return out


def fv_kapi(cikti: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    yol = _fv_yol("onkayit", cikti)
    if kontrol:
        import IZ_KARNE as IK
        try:
            IK.ik_kontrol_kapisi(yol)
        except RuntimeError as ex:
            raise FVHata(str(ex))
    try:
        kapi = OC.oc_kapi(yol, git=git, kontrol=kontrol)
    except OC.OCHata as ex:
        raise FVHata(f"oc_kapi: {ex}")
    ok = fv_onkayit_dogrula(yol, git=git, cikti=cikti)
    ok["oc_kapi"] = {k: v for k, v in kapi.items() if k != "kontrol"}
    return ok


# ================================================================ 5) KOŞU (AŞAMA 2)
def fv_gelecek_denetimi(Vd: Dict[str, Any], X: pd.DataFrame, pazar: str) -> int:
    G = V2_ESIK["gelecek_denetimi"]; rng = np.random.default_rng(G["tohum"]); V = Vd["V"]; n = 0
    Xt = X[X.satir.isin(V2_ESIK["ana"])]
    if not len(Xt):
        return 0
    for r in Xt.iloc[rng.choice(len(Xt), min(G["n"], len(Xt)), replace=False)].itertuples():
        t = pd.Timestamp(r.tarih)
        _, Z = fv_hisse(V[r.sembol][V[r.sembol].index <= t], V2_SECIM)
        if not len(Z) or Z.index[-1] != t or not bool(Z[r.satir].iloc[-1]) or fv_baglam(Z.iloc[-1]) != r.baglam:
            raise FVHata(f"geleceğe bakma denetimi tutmadı: {pazar} {r.sembol} {t.date()}")
        n += 1
    return n


def fv_satir_sonuc(S: Dict[str, Any], yon: str = "+") -> Dict[str, Any]:
    """Satır sonucu (beklenen yön): hücreler + durum, etiket (Ç187 ile aynı: FO.fo_etiket), olasılık, karar hücrelerinde p."""
    J = FO._fo_json_S(S); T = S["hucre"]; J["yon"] = yon
    if not len(T):
        J["etiket"] = {"genel": "VERİ YOK"}; J["p"] = {}
        return J
    J["etiket"] = FO.fo_etiket(T, yon)
    for h in J["hucre"]:
        h["durum_yon"], h["guc_yon"] = FO.fo_durum(h, yon)
    Ol = S["olay"]; J["p"] = {}
    for p in OC.OC_ESIK["karar_pazar"]:
        for d in OC.OC_ESIK["karar_donem"]:
            x = Ol[(Ol.pazar == p) & (Ol.donem == d)] if len(Ol) else Ol
            J["p"][f"{p} {d}"] = FO.fo_p(x.fark.to_numpy(float), x.giris, yon) if len(x) else np.nan
    return J


def fv_kirilim_ozet(Ol: pd.DataFrame) -> List[Dict[str, Any]]:
    out = []
    if not len(Ol) or "kirilim" not in Ol:
        return out
    for (p, d), g in Ol.groupby(["pazar", "donem"]):
        k = g.kirilim.value_counts().to_dict(); olc = int(sum(v for a, v in k.items() if a in ("KIRILIM", "STOP", "YOK")))
        out.append({"pazar": p, "donem": d, "n": int(len(g)), "olculen": olc, **{a: int(k.get(a, 0)) for a in ("KIRILIM", "STOP", "YOK", "OLCULMEZ")},
                    "kirilim_payi": (k.get("KIRILIM", 0) / olc) if olc else None, "stop_payi": (k.get("STOP", 0) / olc) if olc else None})
    return out


def fv_kos(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    t_bas = time.time(); warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or FV_YOL["cikti"]
    if os.path.exists(_fv_yol("sonuc", cikti)):
        raise FVHata("sonuc.json var: ölçüm bir kez koşulur")
    ok = fv_kapi(cikti, git=git, kontrol=kontrol)
    kos_zaman = _fv_simdi()
    if ok["onkayit_yazim_utc"] > kos_zaman:
        raise FVHata("ön kayıt zamanı koşu zamanından sonra")
    os.makedirs(FV_YOL["satir"], exist_ok=True)
    sonuc: Dict[str, Any] = {"surum": FV_SURUM, "onkayit": ok, "kos_zaman_utc": kos_zaman, "v2_esik_sha": fv_esik_sha(), "secim": V2_SECIM,
                             "gelecek_denetimi": {}, "veri_not": {}, "satir": {}, "kirilim": {}}
    Xs, PN = [], {}
    for p in OC.OC_ESIK["pazar"]:
        Vd = OC.oc_veri(p, klasor=veri or FV_YOL["veri"], veri2=FV_YOL["veri2"])
        sonuc["veri_not"][p] = list(Vd.get("not", [])) + [f"hisse {len(Vd['V'])}"]
        X = fv_sinyaller(Vd, p, kirilim=True)
        sonuc["gelecek_denetimi"][p] = fv_gelecek_denetimi(Vd, X, p)
        fvlog.info("%s: durum %d; geleceğe bakma denetimi TUTTU (%d)", p, len(X), sonuc["gelecek_denetimi"][p])
        PN[p] = OC.oc_panel(Vd); Xs.append(X)
        del Vd
    X = pd.concat(Xs, ignore_index=True)
    for sat in V2_ESIK["satirlar"]:
        Xa = X[X.satir == sat]
        S = FO.fo_olc_satir(Xa, PN)
        sonuc["satir"][sat] = fv_satir_sonuc(S, V2_ESIK["yon"][sat])
        Ol = S["olay"].copy()
        if len(Ol):
            km = Xa.drop_duplicates(["pazar", "sembol", "tarih"]).set_index(["pazar", "sembol", "tarih"])
            Ol["kirilim"] = [km.kirilim.get((r.pazar, r.sembol, pd.Timestamp(r.tarih)), "OLCULMEZ") for r in Ol.itertuples()]
            Ol["baglam"] = [km.baglam.get((r.pazar, r.sembol, pd.Timestamp(r.tarih)), "-") for r in Ol.itertuples()]
            Ol.insert(0, "satir", sat)
            Ol.to_csv(os.path.join(FV_YOL["satir"], f"olay_{sat}.csv.gz"), index=False)
        sonuc["kirilim"][sat] = fv_kirilim_ozet(Ol)
        fvlog.info("%s: %s %.0f sn", sat, sonuc["satir"][sat]["etiket"].get("genel"), time.time() - t_bas)
    anahtar, pler = [], []
    for sat in V2_ESIK["satirlar"]:
        if sat in V2_ESIK["ana"]:
            continue
        for h, pv in sonuc["satir"][sat].get("p", {}).items():
            anahtar.append((sat, h)); pler.append(pv)
    gec = FO.fo_bh(pler, 0.10)
    sonuc["bh"] = [{"satir": a, "hucre": h, "p": p, "bh_q10": g} for (a, h), p, g in zip(anahtar, pler, gec)]
    sonuc["sure_sn"] = round(time.time() - t_bas, 1)
    _fv_yaz(_fv_yol("sonuc", cikti), json.dumps(sonuc, ensure_ascii=False, indent=1, default=str), "sonuç")
    return {"sonuc": sonuc, "rapor": fv_rapor(cikti)}


# ================================================================ 6) KÖR SET 2
def fv_kor_sec(X: pd.DataFrame, Vlen: Dict[Tuple[str, str], int]) -> List[Dict[str, Any]]:
    """X: durum günleri (satir TAM / DEGIL); Vlen: (pazar, sembol) -> {tarih: geçerli bar sırası}. Önceden yazılı seçim (tohum)."""
    K = V2_ESIK["kor2"]; rng = np.random.default_rng(K["tohum"]); kul: set = set(); sec = []
    X = X[(X.tarih >= pd.Timestamp(K["bas"])) & (X.tarih <= pd.Timestamp(K["son"]))]
    for grup in ("TAM", "DEGIL"):
        for pz in ("BIST", "ABD"):
            n = K["grup"][grup][pz]
            h = X[(X.satir == grup) & (X.pazar == pz)].reset_index(drop=True)
            if len(h):
                gec = np.array([Vlen[(pz, s)].get(pd.Timestamp(t), -1) + 1 >= K["once"] + K["pencere"] for s, t in zip(h.sembol, h.tarih)])
                h = h[gec].reset_index(drop=True)
            k = 0
            for i in rng.permutation(len(h)):
                if k >= n:
                    break
                r = h.iloc[int(i)]
                if r.sembol in kul:
                    continue
                kul.add(r.sembol); k += 1
                sec.append({"grup": grup, "pazar": pz, "sembol": str(r.sembol), "tarih": str(pd.Timestamp(r.tarih).date()),
                            "dusuren": r.get("dusuren", "") if grup == "DEGIL" else "", "baglam": r.get("baglam", "")})
            if k < n:
                raise FVHata(f"kör set 2: {grup} {pz} için yeterli aday yok ({k} < {n})")
    sira = rng.permutation(len(sec))
    return [dict(sec[int(i)], no=j + 1) for j, i in enumerate(sira)]


def fv_kor_sonuc(d: pd.DataFrame, M: pd.DataFrame, t: pd.Timestamp) -> Dict[str, Any]:
    """Anahtar için (PDF'te YOK): r20 / r60 (t+1 açılış, 19 / 59 geçerli bar sonra kapanış) ve önce kırılım / stop."""
    i = int(M.index.get_loc(t)); dd = d.loc[M.index]; O, C = dd.Open.to_numpy(float), dd.Close.to_numpy(float); out: Dict[str, Any] = {}
    for ad, h in (("r20", 20), ("r60", 60)):
        out[ad] = float(C[i + h] / O[i + 1] - 1) if i + h < len(C) else None
    out["once"] = fv_kirilim(C, i, float(M.loc[t, "HMAXW"]), float(M.loc[t, "HAT"]))
    return out


def fv_kor_sayfa(d: pd.DataFrame, t: pd.Timestamp, no: int):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import FITIL_KOR as FK
    K = V2_ESIK["kor2"]; i = int(d.index.get_loc(pd.Timestamp(t)))
    w = d.iloc[i - K["once"] - K["pencere"] + 1:i + 1]
    if len(w) != K["once"] + K["pencere"] or w.index[-1] != pd.Timestamp(t):
        raise FVHata(f"kör sayfa {no}: pencere eksik")
    ref = float(w.Close.iloc[K["once"] - 1])
    fig = plt.figure(figsize=(11.69, 8.27))
    ax = fig.add_axes([0.07, 0.30, 0.90, 0.58]); axh = fig.add_axes([0.07, 0.10, 0.90, 0.17])
    FK.fk_kor_ciz(ax, axh, w, K["pencere"], ref)
    fig.text(0.07, 0.94, f"No {no}", fontsize=22, weight="bold", color=FK.FK_CIZIM["baslik"])
    fig.text(0.30, 0.945, "gri zemin = son 10 mum (sağ kenar = karar günü; sonrası gösterilmez)", fontsize=10, color="#555555")
    fig.text(0.07, 0.04, "Yanıt: " + K["soru"], fontsize=10, color="#333333")
    return fig


def fv_korset(cikti: Optional[str] = None, veri: Optional[str] = None, git: bool = True, kontrol: bool = True) -> Dict[str, Any]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import FITIL_KOR as FK
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    cikti = cikti or FV_YOL["cikti"]; ok = fv_kapi(cikti, git, kontrol)
    if os.path.exists(_fv_yol("anahtar", cikti)):
        raise FVHata("kor2_anahtar.json var: kör set 2 bir kez üretilir (tohum sabit)")
    Xs, VV, MM, Vlen = [], {}, {}, {}
    for p in ("BIST", "ABD"):
        Vd = OC.oc_veri(p, klasor=veri or FV_YOL["veri"], veri2=FV_YOL["veri2"])
        for s in sorted(Vd["V"]):
            M, Z = fv_hisse(Vd["V"][s], V2_SECIM)
            if not len(M):
                continue
            g1 = Z.index[Z.TAM_DIP.to_numpy(bool)]; g2 = Z.index[(Z.s1 & ~Z.TAM_DIP).to_numpy(bool)]
            if len(g1):
                Xs.append(pd.DataFrame({"sembol": s, "tarih": g1, "pazar": p, "satir": "TAM", "dusuren": "", "baglam": "DİP"}))
            if len(g2):
                Xs.append(pd.DataFrame({"sembol": s, "tarih": g2, "pazar": p, "satir": "DEGIL",
                                        "dusuren": ["; ".join(fv_dusuren(Z.loc[t]) or ["bağlam DİP değil"]) for t in g2],
                                        "baglam": [fv_baglam(Z.loc[t]) for t in g2]}))
            VV[(p, s)] = Vd["V"][s].loc[M.index]; MM[(p, s)] = M
            Vlen[(p, s)] = {t: i for i, t in enumerate(M.index)}
        del Vd
    X = pd.concat(Xs, ignore_index=True)
    sec = fv_kor_sec(X, Vlen)
    for e in sec:
        e.update(fv_kor_sonuc(VV[(e["pazar"], e["sembol"])], MM[(e["pazar"], e["sembol"])], pd.Timestamp(e["tarih"])))
    yol = _fv_yol("pdf", cikti); sayfa = 0
    with PdfPages(yol) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        fig.text(0.07, 0.92, f"S+ v2 'TAM GİRİLİR' — KÖR SET 2 ({len(sec)} grafik)", fontsize=18, weight="bold", color=FK.FK_CIZIM["baslik"])
        for k_, s_ in enumerate([
                f"No 1 .. No {len(sec)}: her grafik gri zeminde son 10 mum (sağ kenar = karar günü) + öncesi {V2_ESIK['kor2']['once']} mum. SONRASI YOK.",
                "Hisse adı, tarih, pazar ve fiyat rakamı yok; fiyat ekseni oransal (gri zeminden önceki son kapanış = %0); hacim altta.",
                "Soru: bu son mumda (stoplu) TAM GİRİLİR mi? " + K_SORU() + ".",
                f"Yanıt biçimi: 1:E, 2:H, 3:B, ... ({len(sec)} numaranın hepsi). Anahtar ayrı dosyada; sen işaretlemeden açılmaz.",
                "Bu set şunu ölçer: kodun 'tam girilir' dediği günler senin gözündeki giriş mi (sonuç / getiri bu sette yok)."]):
            fig.text(0.07, 0.84 - k_ * 0.05, s_, fontsize=11, va="top")
        pdf.savefig(fig); plt.close(fig); sayfa += 1
        for e in sorted(sec, key=lambda z: z["no"]):
            fig = fv_kor_sayfa(VV[(e["pazar"], e["sembol"])], pd.Timestamp(e["tarih"]), e["no"])
            m = " ".join(FK._fk_metinler(fig))
            if e["sembol"] in m or e["tarih"][:4] in m:
                raise FVHata(f"kör sayfa {e['no']}: ad / tarih sızıntısı")
            pdf.savefig(fig); plt.close(fig); sayfa += 1
    anahtar = {"surum": FV_SURUM, "uyari": "GİZLİ: Cemal işaretlemeden açılmaz; PDF'te bu bilgiler yok", "onkayit": ok, "v2_esik_sha": fv_esik_sha(),
               "pdf_sha": _fv_sha_dosya(yol), "pdf_sayfa": sayfa, "kor_sayfa_ofset": 1, "sayfalar": sorted(sec, key=lambda z: z["no"])}
    _fv_yaz(_fv_yol("anahtar", cikti), json.dumps(anahtar, ensure_ascii=False, indent=1, default=str), "anahtar")
    fvlog.info("kör set 2: %s (%d sayfa), anahtar yazıldı", yol, sayfa)
    return {"pdf": yol, "sayfa": sayfa}


def K_SORU() -> str:
    return V2_ESIK["kor2"]["soru"]


FV_YANITSIZ = "-"


def fv_cevap_ayristir(metin: str, n: int = 40, eksik_izin: bool = False) -> Dict[int, str]:
    """'1:E,2:H,3:B,4:-' -> {no: E/H/B/-}. '-' = yanıtsız sayfa. eksik_izin=True ise yazılmayan numaralar da '-' (yanıtsız) sayılır;
    aksi halde eksik numara durdurur (eski davranış)."""
    out: Dict[int, str] = {}
    for parca in re.split(r"[,;\s]+", metin.strip()):
        if not parca:
            continue
        m = re.fullmatch(r"(\d{1,3})\s*[:=]\s*([EeHhBb-])", parca)
        if not m:
            raise FVHata(f"yanıt parçası okunamadı: '{parca}' (biçim 1:E,2:H,3:B,4:-)")
        k = int(m.group(1))
        if not 1 <= k <= n:
            raise FVHata(f"numara {k} 1..{n} dışında")
        if k in out:
            raise FVHata(f"numara {k} iki kez")
        out[k] = m.group(2).upper()
    eksik = [k for k in range(1, n + 1) if k not in out]
    if eksik and not eksik_izin:
        raise FVHata(f"yanıtı olmayan numara: {eksik} (yanıtsız sayfa için '{FV_YANITSIZ}' yaz ya da eksik_izin=True)")
    for k in eksik:
        out[k] = FV_YANITSIZ
    if eksik:
        fvlog.info("kör yanıt: %d numara yazılmamış, yanıtsız sayıldı: %s", len(eksik), eksik)
    return dict(sorted(out.items()))


FV_TUR = ("açık", "çıkarım", "yanıtsız")


def fv_cevap_dosya_oku(yol: str, n: int = 40, eksik_izin: bool = False) -> Tuple[Dict[int, str], Dict[int, str], str]:
    """Ana modelin yazıya döktüğü yanıt dosyası ('yanit' -> no -> {etiket, tur, ...}) -> (etiket, tur, dosya sha).
    Denetim: numara 1..n, etiket E/H/B/-, tur açık/çıkarım/yanıtsız, '-' <-> 'yanıtsız' tutarlı; eksik numara eksik_izin ile yanıtsız."""
    if not os.path.exists(yol):
        raise FVHata(f"yanıt dosyası yok: {yol}")
    try:
        J = json.load(open(yol, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise FVHata(f"yanıt dosyası okunamadı: {yol}: {ex}")
    Y = J.get("yanit") if isinstance(J, dict) else None
    if not isinstance(Y, dict) or not Y:
        raise FVHata(f"yanıt dosyasında 'yanit' sözlüğü yok: {yol}")
    parca, tur = [], {}
    for k, v in Y.items():
        if not (isinstance(v, dict) and str(k).isdigit()):
            raise FVHata(f"yanıt dosyası satırı bozuk: {k}")
        et, tr = str(v.get("etiket", "")).strip().upper(), str(v.get("tur", "")).strip()
        if et not in ("E", "H", "B", FV_YANITSIZ):
            raise FVHata(f"yanıt {k}: etiket '{et}' E/H/B/- değil")
        if tr not in FV_TUR:
            raise FVHata(f"yanıt {k}: tur '{tr}' {FV_TUR} dışında")
        if (et == FV_YANITSIZ) != (tr == "yanıtsız"):
            raise FVHata(f"yanıt {k}: etiket '{et}' ile tur '{tr}' çelişiyor")
        parca.append(f"{int(k)}:{et}"); tur[int(k)] = tr
    c = fv_cevap_ayristir(",".join(parca), n, eksik_izin=eksik_izin)
    for k, v in c.items():
        tur.setdefault(k, "yanıtsız")
    return c, dict(sorted(tur.items())), _fv_sha_dosya(yol)


def fv_kor_karar(tam_e: Optional[float], degil_e: Optional[float]) -> str:
    if tam_e is None:
        return "ÖLÇÜLEMEDİ"
    if tam_e >= 0.60 and degil_e is not None and tam_e - degil_e >= 0.30:
        return "GÖZLE UYUMLU"
    if tam_e < 0.40:
        return "GÖZLE UYUMSUZ"
    return "KISMİ"


def fv_olc(cevap: Optional[str] = None, cikti: Optional[str] = None, cevap_dosya: Optional[str] = None,
           eksik_izin: bool = False) -> Dict[str, Any]:
    """Kör set 2 uyumu. Yanıt ya metin (--cevap) ya dosya (--cevap-dosya). Yanıtsız ('-') sayfalar paylardan ÇIKAR (n = yanıtlı);
    karar kuralı (fv_kor_karar) değişmez, yalnız yanıtlı sayfalarla hesaplanır."""
    import FITIL_KOR as FK
    if (cevap is None) == (cevap_dosya is None):
        raise FVHata("yanıt için --cevap ya da --cevap-dosya'dan yalnız biri verilmeli")
    ya = _fv_yol("anahtar", cikti)
    A = json.load(open(ya, encoding="utf-8")); S = A["sayfalar"]
    if cevap_dosya is not None:
        c, tur, csha = fv_cevap_dosya_oku(cevap_dosya, len(S), eksik_izin=eksik_izin)
    else:
        c, tur, csha = fv_cevap_ayristir(cevap, len(S), eksik_izin=eksik_izin), None, None
    if sorted(c) != sorted(int(e["no"]) for e in S):
        raise FVHata("yanıt numaraları anahtar sayfalarıyla aynı değil")
    yanitsiz = [k for k, v in sorted(c.items()) if v == FV_YANITSIZ]

    def pay(grp):
        y = [c[e["no"]] for e in S if grp(e)]; x = [v for v in y if v != FV_YANITSIZ]
        e_, h_, b_ = x.count("E"), x.count("H"), x.count("B")
        return {"n": len(x), "E": e_, "H": h_, "B": b_, "E_payi": e_ / len(x) if x else None, "E_payi_B_haric": e_ / (e_ + h_) if (e_ + h_) else None,
                "yanitsiz": len(y) - len(x), "n_toplam": len(y)}
    out = {"cevap": {str(k): v for k, v in sorted(c.items())}, "TAM": pay(lambda e: e["grup"] == "TAM"), "DEGIL": pay(lambda e: e["grup"] == "DEGIL"),
           "TAM_BIST": pay(lambda e: e["grup"] == "TAM" and e["pazar"] == "BIST"), "TAM_ABD": pay(lambda e: e["grup"] == "TAM" and e["pazar"] == "ABD")}
    out["n_toplam"] = len(c); out["n_yanitli"] = len(c) - len(yanitsiz); out["n_yanitsiz"] = len(yanitsiz); out["yanitsiz"] = yanitsiz
    out["kaynak"] = {"cevap_dosya": os.path.relpath(cevap_dosya, KOK_FV) if cevap_dosya else None, "cevap_dosya_sha": csha, "eksik_izin": eksik_izin}
    if tur is not None:
        out["tur_cevap"] = {str(k): v for k, v in tur.items()}
        out["tur"] = {tr: {g: pay(lambda e, tr=tr, g=g: e["grup"] == g and tur[e["no"]] == tr) for g in ("TAM", "DEGIL")}
                      for tr in ("açık", "çıkarım")}
    else:
        out["tur"] = None
    out["capraz"] = {etk: {g: sum(1 for e in S if e["grup"] == g and c[e["no"]] == etk) for g in ("TAM", "DEGIL")} for etk in ("E", "H", "B", FV_YANITSIZ)}
    t, d = out["TAM"], out["DEGIL"]
    out["fisher"] = FK.fk_fisher(t["E"], t["n"] - t["E"], d["E"], d["n"] - d["E"])
    out["karar"] = fv_kor_karar(t["E_payi"], d["E_payi"]); out["kural"] = V2_ESIK["kor2"]["karar"]
    def bilgi(grup):
        bil = {}
        for etk in ("E", "H", "B"):   # yanıtsız ('-') sayfalar dışarıda
            x = [e for e in S if e["grup"] == grup and c[e["no"]] == etk]
            r20 = [e["r20"] for e in x if e.get("r20") is not None]; r60 = [e["r60"] for e in x if e.get("r60") is not None]
            on = [e["once"] for e in x if e.get("once") in ("KIRILIM", "STOP", "YOK")]
            bil[etk] = {"n": len(x), "r20_medyan": float(np.median(r20)) if r20 else None, "r60_medyan": float(np.median(r60)) if r60 else None,
                        "kirilim_payi": (on.count("KIRILIM") / len(on)) if on else None, "stop_payi": (on.count("STOP") / len(on)) if on else None,
                        "n_once_olculen": len(on)}
        return bil
    out["sonuc_bilgi"] = bilgi("TAM")   # TAM grubu = TAM_DIP günleri
    out["sonuc_bilgi_DEGIL"] = bilgi("DEGIL")
    A["olc"] = out
    _fv_yaz(ya, json.dumps(A, ensure_ascii=False, indent=1, default=str), "anahtar")
    ys = _fv_yol("sonuc", cikti)
    if os.path.exists(ys):
        J = json.load(open(ys, encoding="utf-8")); J["kor2"] = out
        _fv_yaz(ys, json.dumps(J, ensure_ascii=False, indent=1, default=str), "sonuç")
    return out


# ================================================================ 7) RAPOR
def _fv_hucre_sat(sat: str, h: Dict[str, Any], yon: str = "+") -> str:
    n = int(h.get("n") or 0)
    if not n:
        return f"| {sat} | {h['pazar']} | {h['donem']} | {'K' if h.get('karar_hucre') else 'b'} | 0 | - | - | - | - | - | - | - | {h.get('durum_yon')} |"
    if yon == "+":
        dort = "".join("E" if h.get(k) else "h" for k in ("s_n", "s_fark", "s_sira", "s_port", "s_yari"))
    else:
        K = OC.OC_ESIK["hucre_karar"]
        sb = [n >= K["n_esik"], h["ort_fark"] < 0 and h["ust95"] < 0, h["sira"] < K["sira_esik"], h["portfoy"] < h["portfoy_esli_p10"],
              (h.get("yari1_fark") or 0) < 0 and (h.get("yari2_fark") or 0) < 0]
        dort = "".join("E" if b else "h" for b in sb)
    port = f"{_yz(h['portfoy'], 0)} / p90 {_yz(h['portfoy_esli_p90'], 0)} / p10 {_yz(h['portfoy_esli_p10'], 0)}"
    return (f"| {sat} | {h['pazar']} | {h['donem']} | {'K' if h.get('karar_hucre') else 'b'} | {n} | {_yz(h['ort_fark'])} [{_yz(h['alt95'])}, "
            f"{_yz(h['ust95'])}] | {_yz(h['medyan_fark'])} | {_sy(h['sira'])} | {port} | {_yz(h.get('yari1_fark'))} / {_yz(h.get('yari2_fark'))} | "
            f"{dort} | {_sy(100 * float(h.get('guc_yon') or 0), 0)}% | {h.get('durum_yon')} |")


def fv_rapor(cikti: Optional[str] = None, ek: Optional[str] = None) -> str:
    J = json.load(open(_fv_yol("sonuc", cikti), encoding="utf-8"))
    E = V2_ESIK; SA = J["satir"]; on = J["onkayit"]
    git_on = on.get("git_onkayit")
    git_on = git_on if isinstance(git_on, str) else (git_on or {}).get("commit", "-")[:10]
    s = ["# FITIL_V2 — RAPOR (S+ v2 'TAM GİRİLİR', ORTAK CETVEL v1.0)", "",
         f"Ön kayıt yazım {on.get('onkayit_yazim_utc')} (sha {on.get('onkayit_sha', '')[:12]}…; git {git_on}); iş tanımı git "
         f"{on['git_is_tanimi']['commit'][:10]}; koşu {J['kos_zaman_utc']}; süre {J.get('sure_sn')} sn. Geleceğe bakma denetimi: "
         + ", ".join(f"{p} {v} TAM günü TUTTU" for p, v in J["gelecek_denetimi"].items()) + ".", "", "## ÖZET", ""]
    ana = E["ana"][0]; e = SA[ana]["etiket"]
    s.append(f"- {E['satirlar'][ana]}: KARAR **{e.get('genel')}**; olasılık etiketi {e.get('olasilik')}.")
    par = []
    for h in SA[ana]["hucre"]:
        if h["donem"] != "2016-22":
            par.append(f"{h['pazar']} {h['donem']}: n {int(h.get('n') or 0)}, eş farkı {_yz(h.get('ort_fark'))} [{_yz(h.get('alt95'))}, "
                       f"{_yz(h.get('ust95'))}] -> {h.get('durum_yon')}")
    s += ["  - " + "; ".join(par), "- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı momentum x likidite kovasındaki öteki "
          "hisselerin ortalaması. Hayatta kalma: evren bugün işlem görenler; getiriler yukarı, -%50 olasılığı aşağı yanlı. Komisyon yok.", "",
          "## TANIM ve eşikler", "", f"- Seçilen nokta: {_fv_nokta_metin(J['secim'])}.", f"- BAĞLAM: {E['baglam']['tanim']}."] + \
         [f"- {FV_SART_AD[k]}: {E['tanim'][k]}." for k in FV_SART] + [f"- {E['tanim']['tam']}.", "",
          "## TASARIM sonucu", "", "TASARIM.md (etiket x şart tablosu, 72 noktalı ızgara).", "",
          "## OLAY SAYIMI (cetvel düşmeleri)", "",
          "| Satır | Pazar | girdi (durum günü) | havuz dışı | tekil düşen | r60 ölçülemedi | eş < 3 |", "|---|---|---|---|---|---|---|"]
    for sat in E["satirlar"]:
        for p, c in SA[sat]["sayim"].items():
            s.append(f"| {sat} | {p} | {c.get('girdi')} | {c.get('havuz_disi')} | {c.get('tekil')} | {c.get('r60_olculemedi')} | {c.get('es_az')} |")
    s += ["", "## HÜCRE TABLOSU (r60 eşli fark; şart: n / fark+aralık / sıra / portföy / iki yarı; E = tuttu, h = tutmadı)", "",
          "| Satır | Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / p90 / p10 | yarı1 / yarı2 | şart (beklenen yön) | güç (δ 5) | durum |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for sat in E["satirlar"]:
        for h in SA[sat]["hucre"]:
            s.append(_fv_hucre_sat(sat, h, E["yon"][sat]))
    s += ["", "## OLASILIK TABLOSU (250 gün dokunma; eş katı karar, taban katı bilgi)", "",
          "| Satır | Pazar | Dönem | n250 | P(+%100) olay / eş | kat eş [%95] | kat taban | P(-%50) olay / eş | kat eş [%95] | kat taban | etiket |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sat in E["satirlar"]:
        for r in SA[sat]["olasilik"]:
            s.append(f"| {sat} | {r['pazar']} | {r['donem']} | {r.get('n250', 0)} | {_yz(r.get('up100_es_p_olay'))} / {_yz(r.get('up100_es_p_ref'))} | "
                     f"{_sy(r.get('up100_es_kat'))} [{_sy(r.get('up100_es_alt'))}, {_sy(r.get('up100_es_ust'))}] | {_sy(r.get('up100_tb_kat'))} | "
                     f"{_yz(r.get('dn50_es_p_olay'))} / {_yz(r.get('dn50_es_p_ref'))} | {_sy(r.get('dn50_es_kat'))} [{_sy(r.get('dn50_es_alt'))}, "
                     f"{_sy(r.get('dn50_es_ust'))}] | {_sy(r.get('dn50_tb_kat'))} | {r.get('etiket')} |")
    s += ["", "## KIRILIM / STOP ORANLARI (tekil olaylar; t+1 .. t+60 geçerli bar, önce hangisi)", "",
          "| Satır | Pazar | Dönem | n | ölçülen | KIRILIM | STOP | YOK | ÖLÇÜLMEZ | kırılım payı | stop payı |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for sat in E["satirlar"]:
        for r in J["kirilim"].get(sat, []):
            s.append(f"| {sat} | {r['pazar']} | {r['donem']} | {r['n']} | {r['olculen']} | {r['KIRILIM']} | {r['STOP']} | {r['YOK']} | {r['OLCULMEZ']} | "
                     f"{_yz(r['kirilim_payi'], 0)} | {_yz(r['stop_payi'], 0)} |")
    s += ["", "## KARAR (önceden yazılı etiket kuralı)", "", f"- Kural: {E['karar']['ana']}."]
    for sat in E["satirlar"]:
        e = SA[sat]["etiket"]
        s.append(f"- {sat}{' (ANA)' if sat in E['ana'] else ' (bilgi)'} [yön {E['yon'][sat]}]: **{e.get('genel')}** (cetvel genel: {e.get('genel_cetvel')}); karar hücreleri: "
                 + ", ".join(f"{k} {v}" for k, v in e.get("karar_hucre", {}).items()))
    s.append(f"- Bilgi satırları BH q 0,10: {sum(1 for r in J.get('bh', []) if r['bh_q10'])} / "
             f"{sum(1 for r in J.get('bh', []) if r['p'] is not None and r['p'] == r['p'])} test geçti.")
    s += ["", "## KÖR SET 2", ""]
    k2 = J.get("kor2")
    if k2:
        s.append(f"- Karar: **{k2['karar']}** ({k2['kural']}). TAM E {k2['TAM']['E']} / {k2['TAM']['n']}, DEĞİL E {k2['DEGIL']['E']} / {k2['DEGIL']['n']}; "
                 f"Fisher p {_sy(k2['fisher'], 3)}.")
        if "n_yanitli" in k2:
            s += _fv_rapor_kor2_ek(k2)
    else:
        s.append("- Cemal'in yanıtı bekleniyor (`python FITIL_V2.py olc --cevap ...`).")
    s += ["", "## VERİ ve SINIRLAR", ""] + [f"- {p}: {'; '.join(n)}" for p, n in J["veri_not"].items()] + [
          "- Hayatta kalma: evren bugün işlem gören hisseler; (3) / (5) düşmüş hisseleri seçtiği için yanlılık bu satırda büyüyebilir.",
          "- Komisyon / kayma yok; 31.08.2026 sonrası fiyat yok.", ""]
    onm = _fv_yol("onkayit", cikti)
    if os.path.exists(onm):
        m = open(onm, encoding="utf-8").read(); i = m.find("## KONTROL LİSTESİ")
        if i >= 0:
            s += [m[i:].split("\n## Test")[0].rstrip(), ""]
    if ek and os.path.exists(ek):
        s += [open(ek, encoding="utf-8").read().rstrip(), ""]
    metin = "\n".join(s)
    _fv_yaz(_fv_yol("rapor", cikti), metin, "rapor")
    return metin


def _fv_rapor_kor2_ek(k2: Dict[str, Any]) -> List[str]:
    """KÖR SET 2 ek satırları: yanıtlı / yanıtsız, açık / çıkarım kırılımı, çapraz tablo, etiket başına sonuç bilgisi (n küçük; bulgu değil)."""
    def ehb(p): return f"E {p['E']} / H {p['H']} / B {p['B']} (n {p['n']}; E payı {_yz(p['E_payi'], 0)})"
    s = [f"- Yanıtlı sayfa (n_yanitli) {k2['n_yanitli']} / {k2['n_toplam']}; yanıtsız {k2['n_yanitsiz']} (paylardan çıkarıldı): "
         f"{', '.join(str(k) for k in k2['yanitsiz']) or '-'}.",
         f"- TAM: {ehb(k2['TAM'])}; DEĞİL: {ehb(k2['DEGIL'])}; TAM BIST: {ehb(k2['TAM_BIST'])}; TAM ABD: {ehb(k2['TAM_ABD'])}."]
    if k2.get("tur"):
        s += ["", "| Yanıt türü | TAM E / H / B (n) | DEĞİL E / H / B (n) |", "|---|---|---|"]
        for tr, g in k2["tur"].items():
            s.append(f"| {tr} | {g['TAM']['E']} / {g['TAM']['H']} / {g['TAM']['B']} ({g['TAM']['n']}) | "
                     f"{g['DEGIL']['E']} / {g['DEGIL']['H']} / {g['DEGIL']['B']} ({g['DEGIL']['n']}) |")
    s += ["", "| Cemal etiketi | TAM | DEĞİL |", "|---|---|---|"]
    for etk, g in k2["capraz"].items():
        s.append(f"| {'yanıtsız (-)' if etk == FV_YANITSIZ else etk} | {g['TAM']} | {g['DEGIL']} |")
    s += ["", "| Grup | Cemal etiketi | n | r20 medyan | r60 medyan | önce KIRILIM payı | önce STOP payı |", "|---|---|---|---|---|---|---|"]
    for grp, ad in (("TAM", "sonuc_bilgi"), ("DEĞİL", "sonuc_bilgi_DEGIL")):
        for etk, b in (k2.get(ad) or {}).items():
            s.append(f"| {grp} | {etk} | {b['n']} | {_yz(b['r20_medyan'])} | {_yz(b['r60_medyan'])} | {_yz(b['kirilim_payi'], 0)} | {_yz(b['stop_payi'], 0)} |")
    s.append("- Okuma: sonuç sütunları (r20 / r60 / önce kırılım-stop) yalnız bilgi; etiket başına n küçük, bulgu değil.")
    return s


# ================================================================ 8) ÇAKIŞMA KAPISI
def _cakisma_kontrol_fv(_once=_CK_ONCE_FV, _dosya="FITIL_V2.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_FV", "_CK_KAYIT", "_cakisma_kontrol_fv", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "hashlib", "warnings", "_dt", "OC", "FO", "itertools", "math",
           "annotations", "Any", "Callable", "Dict", "List", "Optional", "Tuple", "_yz", "_sy")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_fv()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=FV_SURUM)
    ap.add_argument("komut", choices=["tasarim", "onkayit", "kos", "korset", "olc", "rapor"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--veri", default=None)
    ap.add_argument("--ek", default=None)
    ap.add_argument("--cevap", default=None)
    ap.add_argument("--cevap-dosya", default=None, help="kör set 2 yanıt json'u ('yanit' -> no -> {etiket E/H/B/-, tur})")
    ap.add_argument("--eksik-izin", action="store_true", help="yazılmayan yanıt numaraları yanıtsız ('-') sayılır")
    ap.add_argument("--uzerine-yaz", action="store_true")
    ap.add_argument("--gitsiz", action="store_true", help="ön kayıt git'e işlenmemişse SAPMA olarak yazıp koş")
    a = ap.parse_args()
    try:
        if a.komut == "tasarim":
            T_ = fv_tasarim_yaz(a.cikti, a.veri)
            print(json.dumps({"secim": T_["secim"]}, ensure_ascii=False, indent=1, default=str))
        elif a.komut == "onkayit":
            print(fv_onkayit_yaz(a.cikti, a.veri, uzerine=a.uzerine_yaz))
        elif a.komut == "kos":
            R_ = fv_kos(a.cikti, a.veri, git=not a.gitsiz)
            print(R_["rapor"].split("## TANIM")[0])
        elif a.komut == "korset":
            print(fv_korset(a.cikti, a.veri, git=not a.gitsiz))
        elif a.komut == "olc":
            if bool(a.cevap) == bool(a.cevap_dosya):
                raise FVHata("--cevap ya da --cevap-dosya'dan yalnız biri gerekli")
            print(json.dumps(fv_olc(a.cevap, a.cikti, cevap_dosya=a.cevap_dosya, eksik_izin=a.eksik_izin), ensure_ascii=False, indent=1, default=str))
        else:
            print(fv_rapor(a.cikti, a.ek))
    except (FVHata, OC.OCHata) as ex:
        fvlog.error("%s", ex); sys.exit(1)
