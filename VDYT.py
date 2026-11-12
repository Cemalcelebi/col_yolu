"""VDYT — VOLATİLİTE DENGE VE YÖN TAHMİNİ. Tek dosya, ayrı araştırma motoru (12 Kasım 2026; Cemal'in iş tanımı, ana oturum tasarım kararları).

Soru: uzun süreli volatilite sıkışmaları (1) ne zaman biter, (2) bitiş olasılığı yaşla nasıl değişir (hazard), (3) bitişten önce / sırasında hangi olaylar
etkili, (4) bitişin yönü, (5) hisseye özgü süre mi, piyasa rejimi mi, haber / bilanço mu daha açıklayıcı. Nihai soru: süre + kendi geçmişi + olay takvimi +
savunma hattı birlikte, genişlemenin ne zaman ve hangi yöne olacağını BASİT PİYASA KONTROLLERİNDEN daha iyi tahmin ediyor mu (zaman sıralı walk-forward + KASA).

SINIR: VDYT, Çöl Yolu'nu, IZ_KARNE karar ölçütlerini ve mevcut kodları DEĞİŞTİRMEZ; onlardan bir şey içe almaz. İçindeki hacim ve mum şekli değişkenleri
(Çöl Yolu'nda kapalı konular) YALNIZ bu motorda ölçülür, Çöl Yolu kararlarına bağlanmaz. VDYT sonucu doğrulanmış sinyal değildir.

Komut:  python VDYT.py envanter     veri envanteri + eksikler (VDYT_VERI_ENVANTERI.md, VDYT_EKSIKLER.md); ağ yok, getiri yok
        python VDYT.py makro        resmi makro TARİH listesi (FOMC: federalreserve.gov, PPK: tcmb.gov.tr) -> vdyt_makro_takvim.json; içerik / sürpriz yok
        python -I VDYT.py kapsam    YALNIZ SAYIM (sıkışma bölgesi, süre dağılımı, karar noktası, olay eşleşme, hisse geçmişi yeterliliği); getiri / genişleme
                                    oranı / yön / model başarısı HESAPLANMAZ
        python VDYT.py onkayit      ön kaydı yazar (ölçümden ÖNCE; eşik mührü + kod sha256 + veri sha256 + kapsam; varsa üzerine yazmaz)
        python -I VDYT.py kos [--asama wf|kasa]   ön kayıt + VDYT.py git'e işlenmiş, değişmemiş, mühür / kod / veri sha256 tutuyorsa ölçüm; yoksa REDDEDER.
                                    'kasa' yalnız 'wf' bittikten sonra ve BİR KEZ açılır.
        python VDYT.py grafik       önceden tanımlı kuralla seçilen örneklerin grafikleri (kos çıktısından)
        python VDYT.py rapor        raporları çıktılardan yeniden yazar
Colab:  exec(open('VDYT.py').read()); vdyt_kapsam()
Veri:   yalnız yerel, daha önce inmiş veri (ayrıntı VDYT_VERI_ENVANTERI.md). Ağ yalnız `makro` komutunda (federalreserve.gov, tcmb.gov.tr). SEC'e istek yok;
        e-posta / anahtar / kişisel bilgi yok. Çıktılar arastirma_cikti/vdyt/ (raporlar), büyük tablolar /tmp/vdyt (VDYT_ARA ile değişir).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_VDYT = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import gzip  # noqa: E402
import hashlib  # noqa: E402
import html as _html  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Callable, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_VDYT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

vdytlog = logging.getLogger("col.vdyt")
if not vdytlog.handlers:
    _vdyt_h = logging.StreamHandler(sys.stderr)
    _vdyt_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s vdyt: %(message)s", "%H:%M:%S"))
    vdytlog.addHandler(_vdyt_h)
    vdytlog.setLevel(logging.INFO)
    vdytlog.propagate = False

VDYT_SURUM = "VDYT v1.0 (2026-11-12): Faz 1 (envanter, ön kayıt, kod + sentetik test, kapsam sayımı); ölçüm Faz 2'de, ön kayıt git'e işlendikten sonra"

VDYT_YOL: Dict[str, str] = {
    "cikti": os.environ.get("VDYT_CIKTI", os.path.join(KOK_VDYT, "arastirma_cikti", "vdyt")),
    "ara": os.environ.get("VDYT_ARA", "/tmp/vdyt"),
    "v_bist": os.environ.get("VDYT_V_BIST", "/tmp/veri/V_BIST.pkl"),
    "v_abd": os.environ.get("VDYT_V_ABD", "/tmp/veri/V_ABD.pkl"),
    "k60_fiyat": os.environ.get("VDYT_K60_FIYAT", "/tmp/k60_fiyat"),
    "k62": os.environ.get("VDYT_K62", "/tmp/k62_veri"),
    "k58_yahoo": os.environ.get("VDYT_K58_YAHOO", "/tmp/k58_yahoo"),
    "pead": os.environ.get("VDYT_PEAD", "/tmp/pead"),
    "kap_iceriden": os.environ.get("VDYT_KAPIC", "/tmp/iv/kap_iceriden"),
    "fon_G": os.environ.get("VDYT_FON_G", "/tmp/veri/G.pkl"),
    "edgar": os.environ.get("VDYT_EDGAR", "/tmp/k60_secframes"),
    "ticker": os.environ.get("VDYT_TICKER", "/tmp/iv/secfs/company_tickers.json"),
    "sic": os.environ.get("VDYT_SIC", "/tmp/iv/k35/k35_sic.csv"),
    "surucu": os.environ.get("VDYT_SURUCU", "/tmp/iv/k36/surucu.pkl"),
    "sektor_bist": os.path.join(KOK_VDYT, "sektor_BIST.csv"),
    "sektor_abd": os.path.join(KOK_VDYT, "sektor_ABD.csv"),
    "k34": os.environ.get("VDYT_K34", "/tmp/veri2/k34_yahoo.pkl"),
    "k66_finra": os.environ.get("VDYT_FINRA", "/tmp/k66_finra"),
    "kapfon_dal": "origin/kapfon-veri",
    "makro": os.environ.get("VDYT_MAKRO", os.path.join(KOK_VDYT, "arastirma_cikti", "vdyt", "vdyt_makro_takvim.json")),
}
VDYT_DOSYA: Dict[str, str] = {
    "envanter": "VDYT_VERI_ENVANTERI.md", "eksik": "VDYT_EKSIKLER.md", "onkayit": "VDYT_ON_KAYIT.md", "kapsam": "vdyt_kapsam.json",
    "kapsam_md": "VDYT_KAPSAM.md", "meta": "vdyt_meta.json", "kasa": "vdyt_kasa_acildi.json", "rapor": "VDYT_RAPOR.md",
    "parametre": "vdyt_parametre_kaydi.json", "hata": "VDYT_HATA_VE_EKSIK.md", "grafik": "grafik",
}
_VDYT_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.(com|net|org|edu|gov|io|tr)\b")
_VDYT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# ---------------------------------------------------------------- ÖN KAYITLI EŞİKLER (sha256'sı ön kayıtta; sonuç görüldükten sonra değişmez)
VDYT_ESIK: Dict[str, Any] = {
    "kesik": "2026-08-31",                        # fon krizi kesiği (CLAUDE.md, FI_OLCUT 'kriz'): fiyat bu günde kesilir, pencereyi aşan karar ölçülmez
    "pazar": {
        "BIST": {"kaynak": "V_BIST (islenmis-veri; OHLCV, bölünme düzeltmeli; yaşayan 581)", "bas": "2015-06-01", "maliyet": 0.0030,
                 "uygunluk": {"gecmis_gun": 252, "likit_gun": 20, "likit_pct": 0.20}},
        "ABD": {"kaynak": "k60_fiyat (Yahoo günlük OHLCV 2010+, 4.678 hisse; yaşayan)", "bas": "2010-01-01", "maliyet": 0.0010,
                "uygunluk": {"gecmis_gun": 252, "likit_gun": 20, "likit_min": 1.0e6, "fiyat_min": 2.0, "tur": ["EQUITY"]}},
        "BIST_K62": {"kaynak": "K62 İş Yatırım günlük kapanış 2008+ (kotasyondan çıkanlar dahil; açılış / yüksek / düşük YOK)", "bas": "2008-01-01",
                     "rol": "yanlılık kontrolü: yalnız kapanış tanımları (T2, T3, T4) ve RV genişlemesi; karar pazarı değil"},
    },
    "karar_pazari": ["BIST", "ABD"],
    "bar": {"hacim_sifir_at": True, "hl_duzelt": True, "bosluk_takvim_gun": 15},
    "olcu": {"atr_n": 14, "rv_n": 20, "bb_n": 20, "bb_k": 2.0, "gecmis_n": 250, "gecmis_min": 200, "bant_n": 20, "rv_kisa": 5,
             "hacim_kisa": 20, "hacim_uzun": 250, "mum_n": 10, "sma": [20, 50, 200], "egim_n": 10, "ret": [20, 60]},
    "tanim": {
        "T1": {"ad": "ATR oranı", "olcu": "natr_oran", "esik": [0.70, 0.60, 0.80], "veri": "OHLC",
               "tarif": "NATR14(t) / medyan(NATR14[t-250..t-1]) <= eşik; NATR14 = 14 günlük ortalama gerçek aralık / kapanış"},
        "T2": {"ad": "Gerçekleşen volatilite yüzdeliği", "olcu": "rv_yuzde", "esik": [0.20, 0.10, 0.30], "veri": "kapanış",
               "tarif": "RV20(t) (20 günlük log getiri std) hissenin kendi [t-250..t-1] RV20 değerleri içinde yüzdelik <= eşik"},
        "T3": {"ad": "Bollinger genişliği yüzdeliği", "olcu": "bbw_yuzde", "esik": [0.20, 0.10, 0.30], "veri": "kapanış",
               "tarif": "BBW20 = 4 x std(C,20) / SMA20; kendi [t-250..t-1] BBW20 değerleri içinde yüzdelik <= eşik"},
        "T4": {"ad": "Dar bant (kapanış)", "olcu": "bant", "esik": [3.5, 2.5, 4.5], "veri": "kapanış",
               "tarif": "(max C - min C) / ort C (son 20 kapanış) / sigma_ref <= eşik; sigma_ref = medyan(RV20[t-250..t-1]) (günlük sigma birimi)"},
        "T5": {"ad": "Bileşik", "en_az": 3, "veri": "OHLC", "tarif": "T1-T4'ün ANA eşiklerinden en az 3'ü aynı gün sağlanır"},
    },
    "ana_tanim": "T1",
    "bolge": {"min_gun": 10, "sonme_gun": 5, "ref_max": 60, "ref_min": 8},
    "genisleme": {"turler": ["TR", "RV"], "ana_tur": "TR", "k": [2.0, 1.5, 2.5], "ana_k": 2.0, "tr_pencere": 3, "rv_pencere": 5,
                  "tarif": {"TR": "ort(TRn[t-2..t]) >= k x medyan(TRn, bölgenin t-3'e kadarki son 60 günü); TRn = gerçek aralık / önceki kapanış",
                            "RV": "std(log getiri[t-4..t]) >= k x std(bölgenin t-5'e kadarki son 60 günlük log getirisi)"}},
    "duyarlilik": {"esik_alt": True, "k_alt_tanim": "T1", "rv_tanim": "T1"},
    "yon": {"Y1_ufuk": 20, "Y2_ufuk": 10},
    "karar_yas": [10, 20, 40, 60, 90, 120],
    "yas_kova": [[10, 19], [20, 39], [40, 59], [60, 89], [90, 119], [120, 100000]],
    "ufuk": [5, 10, 20], "ana_ufuk": 10, "getiri_ufuk": [5, 10, 20, 60], "mfe_ufuk": 20,
    "hisse_gecmis": {"min_bolge": 3, "buzme": 5},
    "rejim": {"tertil": [1.0 / 3.0, 2.0 / 3.0], "sektor_min": 5},
    "savunma": {"tolerans_tr": 0.5, "alt_dilim": 1.0 / 3.0, "min_temas": 3, "min_aralik": 5, "tabanlar": ["govde", "fitil", "kapanis"],
                "ana_taban": "govde", "blok": 5, "blok_max": 12},
    "olay": {"pencere_e1": [[-20, -11], [-10, -6], [-5, -1], [0, 0], [1, 5], [6, 10], [11, 20]],
             "pencere_e2": [[0, 0], [1, 5], [6, 10], [11, 20]],
             "on_artis_gun": 5, "on_artis_esik": 1.5, "haberli": [-5, 1], "habersiz": [-10, 1], "makro_haberli": [-1, 0],
             "esleme": {"yas_tol": 2, "kontrol_n": 5, "aday_n": 40, "tohum": 20261112},
             "emtia_soku_z": 3.0, "emtia_gecmis": 250, "bist_seans_bitis": "18:00", "rakip": "sektörün çeyrekteki ilk bilanço günü (raporlayan hariç)"},
    "wf": {"kesif_yillar": [2019, 2020, 2021, 2022, 2023], "kasa_yillar": [2024, 2025, 2026], "kasa": ["2024-01-01", "2026-08-31"],
           "etiket_tam": True, "kural": "her test yılı Y için eğitim = karar günü + ufuk (işlem günü) < 1 Ocak Y olan bütün satırlar (genişleyen pencere, yıllık yeniden eğitim)"},
    "model": {"ridge": 1.0, "tur": 25, "tol": 1e-8, "winsor": [0.01, 0.99], "min_egitim": 200},
    "temel": {"G_T0": ["ay"], "G_T1": ["yas_kova", "ay"], "kucuk_hucre": 20, "Y_B0": 0.5, "Y_B1": "pazar_60g_yon"},
    "basari": {"bootstrap": 2000, "tohum": 20261112, "guven": [2.5, 97.5], "kume": "hisse",
               "kural": "BASİTTEN İYİ <=> (WF test yılları toplamında VE KASA'da) Brier skill > 0 VE hisse kümeli bootstrap %95 alt sınırı > 0; BIST ve ABD AYRI; "
                        "yön motorunda ayrıca dengeli doğruluk farkı ve log loss skill aynı şartla"},
    "coklu": {"bh_q": 0.10, "plasebo_olay_tekrar": 100, "plasebo_bolge_tekrar": 5, "tohum": 20261113},
    "portfoy": {"yuva": 10, "tut": 20, "esik_pct": 0.90, "rol": "yalnız bilgi"},
    "grafik": {"dpi": 150, "grup_n": 5, "tohum": 20261114, "on_bar": 40, "son_bar": 30,
               "gruplar": ["BASARILI", "BASARISIZ", "HABERLI", "HABERSIZ", "HATLI", "HATSIZ"]},
    "donem_kapsam": [["2010-2015", "2010-01-01", "2015-12-31"], ["2016-2018", "2016-01-01", "2018-12-31"],
                     ["2019-2023 (WF test)", "2019-01-01", "2023-12-31"], ["2024-2026 (KASA)", "2024-01-01", "2026-08-31"]],
}

# Olay kategorileri: kod -> (pazar, kategori, ad, kaynak, önceden bilinir mi, bilgi tarihi kuralı)
VDYT_OLAY_TUR: Dict[str, Dict[str, Any]] = {
    "BIST_BILANCO": {"pazar": "BIST", "kat": "A", "ad": "bilanço (KAP Finansal Rapor, hisse-yıl-dönemin ilk raporu)", "kaynak": "/tmp/k62_veri/kap (2009-06+)",
                     "onceden": True, "bilgi": "KAP yayın saati: < 18:00 ise o işlem günü, >= 18:00 ya da tatil ise sonraki işlem günü"},
    "BIST_TEMETTU": {"pazar": "BIST", "kat": "A", "ad": "hak kullanım (temettü / bölünme) günü, K62 ham / düzeltilmiş kapanış oranı değişimi", "kaynak": "/tmp/k62_veri/fiyat",
                     "onceden": True, "bilgi": "hak kullanım günü (duyuru günü bilinmiyor; özellikte yalnız o gün ve sonrası)"},
    "BIST_SERMAYE": {"pazar": "BIST", "kat": "B", "ad": "ödenmiş sermaye değişimi (bedelli / bedelsiz), K62 sermaye alanı", "kaynak": "/tmp/k62_veri/fiyat",
                     "onceden": False, "bilgi": "sermayenin değiştiği gün (karar / duyuru günü bilinmiyor)"},
    "BIST_ICERIDEN_ALIM": {"pazar": "BIST", "kat": "B", "ad": "içeriden net alım bildirimi (KAP Pay Alım Satım)", "kaynak": "kap_iceriden (2022-07+)",
                           "onceden": False, "bilgi": "KAP yayın saati kuralı"},
    "BIST_ICERIDEN_SATIM": {"pazar": "BIST", "kat": "B", "ad": "içeriden net satım bildirimi (KAP Pay Alım Satım)", "kaynak": "kap_iceriden (2022-07+)",
                            "onceden": False, "bilgi": "KAP yayın saati kuralı"},
    "BIST_FON_GIRIS": {"pazar": "BIST", "kat": "B", "ad": "fon portföyüne giriş bildirimi (KAP fon raporu; fonun önceki raporunda yok)", "kaynak": "G.pkl (2023-01+)",
                       "onceden": False, "bilgi": "rapor yayın saati (bilinme) KAP kuralı"},
    "ABD_BILANCO": {"pazar": "ABD", "kat": "A", "ad": "bilanço günü: 2022-12+ Nasdaq takvimi; öncesi 10-Q / 10-K başvuru günü (VEKİL)", "kaynak": "pead/liste_abd + EDGAR",
                    "onceden": True, "bilgi": "Nasdaq: o gün (saat çoğunlukla verilmemiş); EDGAR: başvuru günü (özellikte ertesi işlem günü)"},
    "ABD_TEMETTU": {"pazar": "ABD", "kat": "A", "ad": "temettü / bölünme hak kullanım günü (Yahoo olayları)", "kaynak": "k60_fiyat events",
                    "onceden": True, "bilgi": "hak kullanım günü"},
    "ABD_VEKALET": {"pazar": "ABD", "kat": "A", "ad": "DEF 14A vekâlet bildirimi (genel kurul yaklaşıyor)", "kaynak": "EDGAR", "onceden": True,
                    "bilgi": "başvuru günü; özellikte ertesi işlem günü"},
    "ABD_8K": {"pazar": "ABD", "kat": "B", "ad": "8-K (madde kodu YOK; bilanço günü +-3 iş günü dışındakiler)", "kaynak": "EDGAR", "onceden": False,
               "bilgi": "başvuru günü; özellikte ertesi işlem günü"},
    "ABD_SERMAYE": {"pazar": "ABD", "kat": "B", "ad": "pay arzı / raf kaydı (S-1, S-3, S-3ASR, 424B1, 424B3, 424B4, 424B5; 424B2 hariç)", "kaynak": "EDGAR", "onceden": False, "bilgi": "başvuru günü"},
    "ABD_13D": {"pazar": "ABD", "kat": "B", "ad": "SC 13D / 13D/A (aktivist / büyük ortak)", "kaynak": "EDGAR", "onceden": False, "bilgi": "başvuru günü"},
    "ABD_BIRLESME": {"pazar": "ABD", "kat": "B", "ad": "birleşme / ihale teklifi (425, SC TO-T, SC 14D9, DEFM14A, PREM14A)", "kaynak": "EDGAR", "onceden": False,
                     "bilgi": "başvuru günü"},
    "ABD_GECIKME": {"pazar": "ABD", "kat": "B", "ad": "NT 10-K / NT 10-Q (rapor gecikmesi)", "kaynak": "EDGAR", "onceden": False, "bilgi": "başvuru günü"},
    "BIST_RAKIP": {"pazar": "BIST", "kat": "C", "ad": "rakip bilançosu: sektörün çeyrekteki ilk bilanço günü", "kaynak": "KAP FR + sektor_BIST.csv",
                   "onceden": True, "bilgi": "rakibin KAP yayın saati kuralı"},
    "ABD_RAKIP": {"pazar": "ABD", "kat": "C", "ad": "rakip bilançosu: SIC grubunun çeyrekteki ilk bilanço günü", "kaynak": "ABD_BILANCO + k35_sic",
                  "onceden": True, "bilgi": "rakibin bilanço günü"},
    "MAKRO_FOMC": {"pazar": "*", "kat": "C", "ad": "FOMC karar günü (planlı toplantılar)", "kaynak": "federalreserve.gov", "onceden": True,
                   "bilgi": "ABD: o gün (14:00 ET); BIST: sonraki işlem günü"},
    "MAKRO_PPK": {"pazar": "*", "kat": "C", "ad": "TCMB PPK karar günü", "kaynak": "tcmb.gov.tr", "onceden": True, "bilgi": "BIST ve ABD: o gün (14:00 TR)"},
    "MAKRO_EMTIA": {"pazar": "*", "kat": "C", "ad": "emtia / kur / faiz şoku (|log getiri| >= 3 x kendi 250 gün std'si; GC, SI, CL, HG, ZW, HRC, ALI, USDTRY, TNX)",
                    "kaynak": "k36 surucu.pkl", "onceden": False, "bilgi": "BIST: ertesi işlem günü; ABD: o gün; özellikte ertesi gün"},
}
VDYT_EDGAR_FORM: Dict[str, List[str]] = {
    "ABD_BILANCO_EDGAR": ["10-Q", "10-K", "10-K405", "10-KT", "10-QT"],
    "ABD_VEKALET": ["DEF 14A"],
    "ABD_8K": ["8-K"],
    "ABD_SERMAYE": ["S-1", "S-3", "S-3ASR", "424B1", "424B3", "424B4", "424B5"],     # 424B2 dışarıda: bankaların yapılandırılmış ürün / borç senedi akışı
    "ABD_13D": ["SC 13D", "SC 13D/A", "SCHEDULE 13D", "SCHEDULE 13D/A"],
    "ABD_BIRLESME": ["425", "SC TO-T", "SC TO-T/A", "SC 14D9", "SC14D9C", "DEFM14A", "PREM14A"],
    "ABD_GECIKME": ["NT 10-K", "NT 10-Q"],
}

# Özellik grupları (Motor 1 genişleme, Motor 2 yön; ikisi aynı tam kümeyi kullanır, gruplar çıkarma (ablasyon) için)
VDYT_OZELLIK: Dict[str, List[str]] = {
    "SURE": ["yas_log", "yk_20", "yk_40", "yk_60", "yk_90", "yk_120"],
    "HISSE": ["hs_oran", "hs_yetersiz", "hs_gen_pay"],
    "REJIM": ["rj_pazar", "rj_sektor"],
    "VOL": ["v_natr_oran", "v_rv_yuzde", "v_bbw_yuzde", "v_bant", "v_rv5_rv20", "v_tr_son3"],
    "HACIM": ["h_hacim_oran", "h_hacim_son5", "h_yukselen_hacim"],
    "MUM": ["m_govde_aralik", "m_govde_gecmis", "m_fitil_ust", "m_fitil_alt", "m_kapanis_konum"],
    "FIYAT": ["f_sma20", "f_sma50", "f_sma200", "f_sma50_egim", "f_ret20", "f_ret60", "f_likidite", "f_bolge_konum"],
    "OLAY": ["o_bilanco_gun", "o_bilanco_yok", "o_bilanco_son", "o_makro_10", "o_olay_son5", "o_olay_son20", "o_olay_tepki"],
    "HAT": ["sv_hat_var", "sv_temas", "sv_korunma", "sv_kirilma", "sv_fitil_ihlal", "sv_mesafe", "sv_son_test", "sv_hacim_test",
            "sv_yukselen_dip", "sv_alcalan_tepe"],
    "PAZAR": ["p_pazar_ret60", "p_sektor_ret20"],
}
VDYT_SURE_MODEL: Dict[str, List[str]] = {          # Bölüm 4: süre yaklaşımları (A-D) ve tam motor
    "A_ORTAK": ["SURE"], "B_HISSE": ["SURE", "HISSE"], "C_REJIM": ["SURE", "REJIM"], "D_ADAPTIF": ["SURE", "HISSE", "REJIM"],
    "M_TAM": list(VDYT_OZELLIK),
}


class VdytHata(RuntimeError):
    """VDYT'ye özgü durdurucu hata (ön kayıt yok / değişmiş / git'e işlenmemiş, kod ya da veri sha256 farklı, veri eksik, KASA zaten açılmış)."""


# ---------------------------------------------------------------- 0) ORTAK YARDIMCILAR
def _vdyt_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _vdyt_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or VDYT_YOL["cikti"], VDYT_DOSYA.get(ad, ad))


def _vdyt_ara(ad: str) -> str:
    os.makedirs(VDYT_YOL["ara"], exist_ok=True)
    return os.path.join(VDYT_YOL["ara"], ad)


def vdyt_sha_dosya(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for p in iter(lambda: f.read(1 << 20), b""):
            h.update(p)
    return h.hexdigest()


def vdyt_sha_klasor(yol: str, desen: str = "*") -> Tuple[str, int]:
    """Klasör özeti: sıralı (ad, boy, sha256) listesinin sha256'sı ve dosya sayısı. Yoksa ('YOK', 0)."""
    if not os.path.isdir(yol):
        return "YOK", 0
    h = hashlib.sha256(); n = 0
    for f in sorted(glob.glob(os.path.join(yol, desen))):
        if os.path.isfile(f):
            h.update(f"{os.path.basename(f)}|{os.path.getsize(f)}|{vdyt_sha_dosya(f)}\n".encode()); n += 1
    return h.hexdigest(), n


def vdyt_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    """Ön kayıt mührü: VDYT_ESIK + olay türleri + EDGAR form listesi + özellik grupları + süre modelleri (hepsi sıralı JSON)."""
    s = json.dumps({"ESIK": E or VDYT_ESIK, "OLAY": VDYT_OLAY_TUR, "EDGAR": VDYT_EDGAR_FORM, "OZELLIK": VDYT_OZELLIK, "SURE_MODEL": VDYT_SURE_MODEL},
                   sort_keys=True, default=str, ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def vdyt_kod_sha(yol: Optional[str] = None) -> str:
    return vdyt_sha_dosya(yol or os.path.join(KOK_VDYT, "VDYT.py"))


def _vdyt_yaz(yol: str, metin: str) -> str:
    if _VDYT_EPOSTA.search(metin):
        raise VdytHata(f"{os.path.basename(yol)}: metinde e-posta biçimli parça var; yazılmadı")
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "w", encoding="utf-8") as f:
        f.write(metin)
    return yol


def _vdyt_pickle_oku(yol: str) -> Any:
    with open(yol, "rb") as f:
        return pickle.load(f)


def _vdyt_jsongz_oku(yol: str) -> Any:
    with gzip.open(yol, "rt", encoding="utf-8") as f:
        return json.load(f)


def _vdyt_json_oku(yol: str) -> Any:
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


def _vdyt_json(yol: str, obj: Any) -> str:
    return _vdyt_yaz(yol, json.dumps(obj, ensure_ascii=False, indent=1, default=str, sort_keys=True))


def _t(x: Any, n: int = 0) -> str:
    """Türkçe sayı biçimi (binlik nokta, ondalık virgül)."""
    try:
        if x is None or (isinstance(x, float) and not np.isfinite(x)):
            return "-"
        s = f"{float(x):,.{n}f}"
        return s.replace(",", "_").replace(".", ",").replace("_", ".")
    except (TypeError, ValueError):
        return str(x)


# ---------------------------------------------------------------- 1) FİYAT VERİSİ
def vdyt_bar_temizle(d: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """OHLCV temizliği (ön kayıtlı): eksik OHLC ve kapanış <= 0 satırları atılır; hacim <= 0 (işlemsiz gün) atılır; H = max(O,H,C), L = min(O,L,C).
    Sütunlar: o, h, l, c, v; tarih indeksi sıralı ve tekil."""
    B = (E or VDYT_ESIK)["bar"]
    d = d.rename(columns={"Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"})[["o", "h", "l", "c", "v"]].astype(float)
    d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d.dropna(subset=["o", "h", "l", "c"])
    d = d[d.c > 0]
    if B["hacim_sifir_at"]:
        d = d[d.v.fillna(0) > 0]
    if B["hl_duzelt"]:
        d = d.assign(h=np.maximum.reduce([d.o.to_numpy(), d.h.to_numpy(), d.c.to_numpy()]), l=np.minimum.reduce([d.o.to_numpy(), d.l.to_numpy(), d.c.to_numpy()]))
    return d


def _vdyt_kes(d: pd.DataFrame, bas: str, E: Dict[str, Any]) -> pd.DataFrame:
    return d[(d.index >= pd.Timestamp(bas)) & (d.index <= pd.Timestamp(E["kesik"]))]


def vdyt_yahoo_oku(yol: str) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
    """K60 Yahoo önbellek JSON'u -> (OHLCV DataFrame, meta: tur, temettu günleri, bolunme günleri). Günler borsa saat dilimine göre."""
    try:
        with open(yol, encoding="utf-8") as f:
            J = json.load(f)
    except (OSError, ValueError) as ex:
        return None, {"durum": f"okunamadı ({type(ex).__name__})"}
    if not isinstance(J, dict) or "yok" in J:
        return None, {"durum": "yok"}
    r = ((J.get("chart") or {}).get("result") or [None])[0]
    if not r or not r.get("timestamp"):
        return None, {"durum": "veri yok"}
    meta = r.get("meta") or {}; tz = meta.get("exchangeTimezoneName") or "America/New_York"

    def gun(ts: Any) -> pd.DatetimeIndex:
        return pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    try:
        d = pd.DataFrame({"Open": q.get("open"), "High": q.get("high"), "Low": q.get("low"), "Close": q.get("close"), "Volume": q.get("volume")},
                         index=gun(r["timestamp"]), dtype=float)
    except (ValueError, TypeError):
        return None, {"durum": "okunamadı (seri boyu)"}
    ev = r.get("events") or {}
    tem = sorted(gun([int(v["date"])])[0] for v in (ev.get("dividends") or {}).values() if isinstance(v, dict) and "date" in v)
    bol = []
    for v in (ev.get("splits") or {}).values():
        try:
            pay, payda = float(v["numerator"]), float(v["denominator"])
        except (KeyError, TypeError, ValueError):
            continue
        if pay > 0 and payda > 0 and pay != payda:
            bol.append((gun([int(v["date"])])[0], pay / payda))
    bol.sort(key=lambda x: x[0])
    return d, {"durum": "fiyat", "tur": meta.get("instrumentType"), "temettu": tem, "bolunme": bol}


def vdyt_bolunme_carpan(bol: List[Tuple[pd.Timestamp, float]], gunler: pd.DatetimeIndex) -> np.ndarray:
    """Her gün için tarihi o günden SONRA olan bölünme oranlarının çarpımı: Yahoo kapanışı (bölünme düzeltmeli) x çarpan = o gün ekranda görülen fiyat."""
    out = np.ones(len(gunler))
    if not bol:
        return out
    d = np.array([x[0].to_datetime64() for x in bol], "datetime64[ns]"); r = np.array([x[1] for x in bol], float)
    sonek = np.r_[np.cumprod(r[::-1])[::-1], 1.0]
    return sonek[np.searchsorted(d, gunler.to_numpy("datetime64[ns]"), side="right")]


def vdyt_fiyat_yukle(pazar: str, E: Optional[Dict[str, Any]] = None, onbellek: bool = True) -> Dict[str, Any]:
    """Pazarın temizlenmiş fiyatları: {'S': {sembol: DataFrame(o,h,l,c,v)}, 'meta': {sembol: {...}}, 'kaynak_sha': ...}.
    BIST = V_BIST.pkl; ABD = k60_fiyat (Yahoo JSON; ilk okumada /tmp/vdyt önbelleğine yazılır, kaynak klasör özeti değişirse yeniden okunur);
    BIST_K62 = K62 kapanış (o = h = l = c; yalnız kapanış tanımları kullanılabilir). Fiyat kesik gününde kesilir."""
    E = E or VDYT_ESIK; P = E["pazar"][pazar]
    if pazar == "BIST":
        if not os.path.exists(VDYT_YOL["v_bist"]):
            raise VdytHata(f"BIST fiyatı yok: {VDYT_YOL['v_bist']} (islenmis-veri dalı: python FON_IZI.py vpac /tmp/iv/veri /tmp/veri)")
        V = _vdyt_pickle_oku(VDYT_YOL["v_bist"])
        S = {s: _vdyt_kes(vdyt_bar_temizle(d, E), P["bas"], E) for s, d in V.items()}
        return {"S": {s: d for s, d in S.items() if len(d)}, "meta": {s: {"tur": "EQUITY"} for s in S}, "kaynak": VDYT_YOL["v_bist"]}
    if pazar == "ABD":
        kl = VDYT_YOL["k60_fiyat"]
        if not os.path.isdir(kl):
            raise VdytHata(f"ABD fiyatı yok: {kl} (K60_veri.py indir_fiyat)")
        ozet = vdyt_sha_klasor(kl, "*.json")[0]; ob = _vdyt_ara("fiyat_ABD.pkl")
        if onbellek and os.path.exists(ob):
            try:
                X = _vdyt_pickle_oku(ob)
                if X.get("kaynak_sha") == ozet:
                    return X
            except (OSError, pickle.UnpicklingError, EOFError) as ex:
                vdytlog.warning("ABD fiyat önbelleği okunamadı (%s); yeniden okunuyor", ex)
        S, M = {}, {}
        for f in sorted(glob.glob(os.path.join(kl, "*.json"))):
            s = os.path.basename(f)[:-5]
            if s.startswith("_"):
                continue
            d, m = vdyt_yahoo_oku(f); M[s] = m
            if d is None:
                continue
            d = _vdyt_kes(vdyt_bar_temizle(d, E), P["bas"], E)
            if len(d):
                S[s] = d
        X = {"S": S, "meta": M, "kaynak": kl, "kaynak_sha": ozet}
        if onbellek:
            with open(ob, "wb") as f:
                pickle.dump(X, f, protocol=pickle.HIGHEST_PROTOCOL)
        return X
    if pazar == "BIST_K62":
        S, M = {}, {}
        for f in sorted(glob.glob(os.path.join(VDYT_YOL["k62"], "fiyat", "*.csv.gz"))):
            s = os.path.basename(f)[:-7]
            try:
                d = pd.read_csv(f)
            except (OSError, ValueError, pd.errors.EmptyDataError):
                continue
            if not len(d):
                continue
            d.index = pd.to_datetime(d.tarih.astype(str).str[:10]); d = d[~d.index.duplicated(keep="last")].sort_index()
            c = d.kapanis.astype(float)
            X = pd.DataFrame({"Open": c, "High": c, "Low": c, "Close": c, "Volume": d.hacim_tl.astype(float) / c.where(c > 0)})
            X = _vdyt_kes(vdyt_bar_temizle(X, E), P["bas"], E)
            if len(X):
                S[s] = X; M[s] = {"son": X.index[-1], "ham_oran": (d.ham / d.kapanis).reindex(X.index), "sermaye": d.sermaye.reindex(X.index)}
        return {"S": S, "meta": M, "kaynak": VDYT_YOL["k62"]}
    raise VdytHata(f"bilinmeyen pazar: {pazar}")


def vdyt_endeks(pazar: str, E: Optional[Dict[str, Any]] = None) -> Optional[pd.DataFrame]:
    """Piyasa endeksi (rejim ve pazar yönü için): BIST = XU100.IS, ABD = SPY (k58 Yahoo önbelleği, günlük). Yoksa None (rejim eşit ağırlıklı medyandan)."""
    E = E or VDYT_ESIK; ad = {"BIST": "XU100.IS", "BIST_K62": "XU100.IS", "ABD": "SPY"}.get(pazar)
    y = os.path.join(VDYT_YOL["k58_yahoo"], f"{ad}.json")
    if not ad or not os.path.exists(y):
        return None
    d, _m = vdyt_yahoo_oku(y)
    if d is None:
        return None
    d = d.rename(columns={"Open": "o", "High": "h", "Low": "l", "Close": "c", "Volume": "v"})
    d = d.dropna(subset=["c"]); d = d[d.c > 0]
    return d[d.index <= pd.Timestamp(E["kesik"])]


# ---------------------------------------------------------------- 2) GÜNLÜK ÖLÇÜLER (her değer yalnız o gün ve öncesi barlardan)
def vdyt_yuzde_gecmis(x: np.ndarray, n: int, n_min: int) -> np.ndarray:
    """x[t]'nin x[t-n..t-1] içindeki yüzdeliği: (küçük sayısı + 0,5 x eşit sayısı) / geçerli sayısı; geçerli < n_min ya da x[t] NaN ise NaN."""
    x = np.asarray(x, float); out = np.full(len(x), np.nan)
    if len(x) <= n:
        return out
    W = np.lib.stride_tricks.sliding_window_view(x, n)[:-1]; cur = x[n:]
    gec = ~np.isnan(W); kuc = (W < cur[:, None]) & gec; esit = (W == cur[:, None]) & gec
    ng = gec.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        p = (kuc.sum(1) + 0.5 * esit.sum(1)) / ng
    p[(ng < n_min) | np.isnan(cur)] = np.nan
    out[n:] = p
    return out


def vdyt_olculer(d: pd.DataFrame, E: Optional[Dict[str, Any]] = None) -> Dict[str, np.ndarray]:
    """Bir hissenin günlük ölçüleri (ön kayıtlı tanımlar; hepsi geriye bakar). d: o, h, l, c, v sütunlu, tarih sıralı."""
    E = E or VDYT_ESIK; O = E["olcu"]; gn, gm = int(O["gecmis_n"]), int(O["gecmis_min"])
    o, h, l, c, v = (d[k].to_numpy(float) for k in ("o", "h", "l", "c", "v"))
    n = len(c); cp = np.r_[np.nan, c[:-1]]
    with np.errstate(invalid="ignore", divide="ignore"):
        tr = np.nanmax(np.vstack([h - l, np.abs(h - cp), np.abs(l - cp)]), axis=0); tr[0] = h[0] - l[0]
        trn = tr / np.where(np.isnan(cp), c, cp)
        S = lambda a: pd.Series(a)   # noqa: E731
        atr = S(tr).rolling(int(O["atr_n"]), min_periods=int(O["atr_n"])).mean().to_numpy()
        natr = atr / c
        natr_ref = S(natr).rolling(gn, min_periods=gm).median().shift(1).to_numpy()
        lr = np.log(c / cp)
        rv = S(lr).rolling(int(O["rv_n"]), min_periods=int(O["rv_n"])).std(ddof=1).to_numpy()
        ort = S(c).rolling(int(O["bb_n"]), min_periods=int(O["bb_n"])).mean().to_numpy()
        bbw = 2.0 * float(O["bb_k"]) * S(c).rolling(int(O["bb_n"]), min_periods=int(O["bb_n"])).std(ddof=0).to_numpy() / ort
        bn = int(O["bant_n"])
        sig_ref = S(rv).rolling(gn, min_periods=gm).median().shift(1).to_numpy()
        bant = (S(c).rolling(bn, min_periods=bn).max().to_numpy() - S(c).rolling(bn, min_periods=bn).min().to_numpy()) \
            / S(c).rolling(bn, min_periods=bn).mean().to_numpy() / sig_ref
        rv5 = S(lr).rolling(int(O["rv_kisa"]), min_periods=int(O["rv_kisa"])).std(ddof=1).to_numpy()
        hk, hu = int(O["hacim_kisa"]), int(O["hacim_uzun"])
        hacim_oran = S(v).rolling(hk, min_periods=hk).median().to_numpy() / S(v).rolling(hu, min_periods=gm).median().to_numpy()
        rng = np.where(h - l > 0, h - l, np.nan); govde = np.abs(c - o); mn = int(O["mum_n"])
        R = lambda a, k=mn: S(a).rolling(k, min_periods=max(3, k // 2)).mean().to_numpy()   # noqa: E731
        govde_aralik = R(govde / rng); fitil_ust = R((h - np.maximum(o, c)) / rng); fitil_alt = R((np.minimum(o, c) - l) / rng)
        kap_konum = R((c - l) / rng)
        govde_gecmis = R(govde / c) / S(govde / c).rolling(gn, min_periods=gm).mean().to_numpy()
        sma = {k: S(c).rolling(k, min_periods=k).mean().to_numpy() for k in O["sma"]}
        deger = c * v
        deger20 = S(deger).rolling(int(E["pazar"]["BIST"]["uygunluk"]["likit_gun"]), min_periods=10).median().to_numpy()
        yuk = np.where(lr > 0, v, 0.0)
        yuk_hacim = S(yuk).rolling(hk, min_periods=hk).sum().to_numpy() / S(v).rolling(hk, min_periods=hk).sum().to_numpy()
        ret = {k: np.log(c / np.r_[np.full(k, np.nan), c[:-k]]) if n > k else np.full(n, np.nan) for k in O["ret"]}
        egim_n = int(O["egim_n"]); s50 = sma[50]
        out = {"tr": tr, "trn": trn, "atr": atr, "natr": natr, "natr_oran": natr / natr_ref, "lr": lr, "rv": rv,
               "rv_yuzde": vdyt_yuzde_gecmis(rv, gn, gm), "bbw": bbw, "bbw_yuzde": vdyt_yuzde_gecmis(bbw, gn, gm), "bant": bant,
               "rv5_rv20": rv5 / rv, "hacim_oran": hacim_oran, "govde_aralik": govde_aralik, "govde_gecmis": govde_gecmis,
               "fitil_ust": fitil_ust, "fitil_alt": fitil_alt, "kap_konum": kap_konum, "yuk_hacim": yuk_hacim,
               "sma20": np.log(c / sma[20]), "sma50": np.log(c / sma[50]), "sma200": np.log(c / sma[200]),
               "sma50_egim": np.log(s50 / np.r_[np.full(egim_n, np.nan), s50[:-egim_n]]) if n > egim_n else np.full(n, np.nan),
               "ret20": ret[20], "ret60": ret[60], "likidite": np.log(deger20), "deger20": deger20, "bar_no": np.arange(1, n + 1, dtype=float)}
    return out


def vdyt_durum(Ol: Dict[str, np.ndarray], tanim: str, esik_idx: int = 0, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Günlük 'sıkışık' durumu (bool). T1-T4: ölçü <= eşik (NaN -> False). T5: T1-T4 ANA eşiklerinden en az 'en_az' tanesi."""
    E = E or VDYT_ESIK; T = E["tanim"][tanim]
    if tanim == "T5":
        say = sum(vdyt_durum(Ol, k, 0, E).astype(int) for k in ("T1", "T2", "T3", "T4"))
        return say >= int(T["en_az"])
    x = Ol[T["olcu"]]
    with np.errstate(invalid="ignore"):
        return np.nan_to_num(x, nan=np.inf) <= float(T["esik"][esik_idx])


# ---------------------------------------------------------------- 3) SIKIŞMA BÖLGELERİ (başlangıç / bitiş kuralı)
BITIS_GEN, BITIS_SONME, BITIS_SANSUR = 1, 2, 3
BITIS_AD = {BITIS_GEN: "GENISLEME", BITIS_SONME: "SONME", BITIS_SANSUR: "SANSUR"}


def vdyt_kopuk(gun: pd.DatetimeIndex, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """kopuk[i] = i. bar ile önceki bar arasında bosluk_takvim_gun'den fazla takvim günü var (işlem durması / veri boşluğu)."""
    g = np.asarray(gun.to_numpy("datetime64[D]"), "datetime64[D]").astype(np.int64)
    k = np.zeros(len(g), bool)
    if len(g) > 1:
        k[1:] = np.diff(g) > int((E or VDYT_ESIK)["bar"]["bosluk_takvim_gun"])
    return k


def vdyt_kosu(durum: np.ndarray, kopuk: np.ndarray) -> np.ndarray:
    """Her gün için o güne kadar kesintisiz 'sıkışık' gün sayısı (kopuk günde sayım yeniden başlar)."""
    n = len(durum); idx = np.arange(n)
    r = np.where(~durum, idx, -1)
    r = np.maximum(r, np.where(kopuk, idx - 1, -1))
    son = np.maximum.accumulate(r) if n else r
    return np.where(durum, idx - son, 0)


def vdyt_genisleme_mi(i: int, bas: int, trn: np.ndarray, lr: np.ndarray, k: float, tur: str, E: Dict[str, Any]) -> bool:
    """i. gün genişleme günü mü (yalnız i ve öncesi). TR: ort(TRn[i-2..i]) >= k x medyan(TRn[bas..i-3] son ref_max); RV: std(lr[i-4..i]) >= k x
    std(lr[bas+1..i-5] son ref_max). Referans gün sayısı < ref_min ise hayır."""
    B = E["bolge"]; G = E["genisleme"]; rm, rn = int(B["ref_max"]), int(B["ref_min"])
    if tur == "TR":
        w = int(G["tr_pencere"]); son = i - w
        ref = trn[max(bas, son - rm + 1): son + 1]
        if len(ref) < rn or i - w + 1 < 0:
            return False
        x = trn[i - w + 1: i + 1]
        if np.isnan(x).any() or np.isnan(ref).any():
            return False
        return bool(x.mean() >= k * float(np.median(ref)))
    w = int(G["rv_pencere"]); son = i - w
    ref = lr[max(bas + 1, son - rm + 1): son + 1]
    if len(ref) < max(rn, 3) or i - w + 1 < 1:
        return False
    x = lr[i - w + 1: i + 1]
    if np.isnan(x).any() or np.isnan(ref).any():
        return False
    s_ref = float(np.std(ref, ddof=1))
    return bool(s_ref > 0 and float(np.std(x, ddof=1)) >= k * s_ref)


def vdyt_bolgeler(durum: np.ndarray, trn: np.ndarray, lr: np.ndarray, kopuk: np.ndarray, k: float, tur: str,
                  E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Sıkışma bölgeleri (ön kayıtlı kural). Açılış: 'sıkışık' durum min_gun gün kesintisiz -> bas = koşunun ilk günü, tespit = bas + min_gun - 1
    (bölge ancak tespit gününün kapanışında bilinir). Bitiş (tespit gününden SONRA, ilk gerçekleşen): GENİŞLEME (vdyt_genisleme_mi) ya da
    SÖNME (durum sonme_gun gün üst üste yanlış; bitiş = o gün) ya da SANSÜR (veri sonu, kesik ya da boşluk; bitiş = son bar).
    Bir bölge kapandıktan sonra yeni koşu sayımı ertesi günden başlar. Döner (m, 5) int dizi: bas, tespit, bit, bit_tur, gen_bas
    (gen_bas = genişleme penceresinin ilk günü; GENİŞLEME değilse -1)."""
    E = E or VDYT_ESIK; m = int(E["bolge"]["min_gun"]); sg = int(E["bolge"]["sonme_gun"])
    w = int(E["genisleme"]["tr_pencere"] if tur == "TR" else E["genisleme"]["rv_pencere"])
    n = len(durum); kosu = vdyt_kosu(durum, kopuk); aday = np.flatnonzero(kosu >= m); out = []
    j = -1
    while True:
        p = int(np.searchsorted(aday, j + m))
        if p >= len(aday):
            break
        i0 = int(aday[p]); bas = i0 - m + 1; yanlis = 0; kapandi = False; i = i0 + 1
        while i < n:
            if kopuk[i]:
                out.append((bas, i0, i - 1, BITIS_SANSUR, -1)); j = i - 1; kapandi = True; break
            if vdyt_genisleme_mi(i, bas, trn, lr, k, tur, E):
                out.append((bas, i0, i, BITIS_GEN, i - w + 1)); j = i; kapandi = True; break
            if not durum[i]:
                yanlis += 1
                if yanlis >= sg:
                    out.append((bas, i0, i, BITIS_SONME, -1)); j = i; kapandi = True; break
            else:
                yanlis = 0
            i += 1
        if not kapandi:
            out.append((bas, i0, n - 1, BITIS_SANSUR, -1)); break
    return np.array(out, dtype=np.int64).reshape(-1, 5)


def vdyt_yon(c: np.ndarray, bolge: np.ndarray, E: Optional[Dict[str, Any]] = None) -> Tuple[np.ndarray, np.ndarray]:
    """GENİŞLEME ile biten bölgelerin yönü. Y1 (ana): bölge kapanış aralığı [Lo, Hi] = bas..gen_bas-1 kapanışları; gen_bas'tan başlayıp bit + Y1_ufuk'a
    kadar ilk kapanış > Hi ise +1, < Lo ise -1, hiçbiri ise 0 (BELİRSİZ); pencere veri sonunu aşıp karar çıkmazsa NaN. Y2: sign(ln(C[bit+Y2_ufuk] /
    C[gen_bas-1])), veri yoksa NaN. Genişleme değilse ikisi NaN."""
    E = E or VDYT_ESIK; u1, u2 = int(E["yon"]["Y1_ufuk"]), int(E["yon"]["Y2_ufuk"]); n = len(c)
    y1 = np.full(len(bolge), np.nan); y2 = np.full(len(bolge), np.nan)
    for r, (bas, _tes, bit, tur, gb) in enumerate(bolge):
        if tur != BITIS_GEN or gb <= bas:
            continue
        lo, hi = float(np.min(c[bas:gb])), float(np.max(c[bas:gb])); son = bit + u1; karar = np.nan
        for j in range(gb, min(n - 1, son) + 1):
            if c[j] > hi:
                karar = 1.0; break
            if c[j] < lo:
                karar = -1.0; break
        if np.isnan(karar) and son <= n - 1:
            karar = 0.0
        y1[r] = karar
        if bit + u2 <= n - 1:
            y2[r] = float(np.sign(np.log(c[bit + u2] / c[gb - 1])))
    return y1, y2


def vdyt_karar_noktalari(bolge: np.ndarray, n: int, E: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Karar noktaları: her bölge ve her karar yaşı a için t = bas + a - 1; t >= tespit ve bölge t'nin kapanışında hâlâ açık (t < bit) ise satır.
    Etiket y_h (h ufku): GENİŞLEME ve t < bit <= t + h -> 1; bit > t + h ya da SÖNME ile t + h içinde bitti -> 0; SANSÜR t + h içinde ya da t + h > son bar
    -> NaN (ölçülmez). 'yas' = a."""
    E = E or VDYT_ESIK; sat = []
    for r, (bas, tes, bit, tur, _gb) in enumerate(bolge):
        for a in E["karar_yas"]:
            t = bas + int(a) - 1
            if t < tes or t >= bit:
                continue
            row = {"bolge": r, "yas": int(a), "t": int(t)}
            for h in E["ufuk"]:
                if t + h > n - 1:
                    row[f"y{h}"] = np.nan
                elif bit <= t + h:
                    row[f"y{h}"] = 1.0 if tur == BITIS_GEN else (0.0 if tur == BITIS_SONME else np.nan)
                else:
                    row[f"y{h}"] = 0.0
            sat.append(row)
    cols = ["bolge", "yas", "t"] + [f"y{h}" for h in E["ufuk"]]
    return pd.DataFrame(sat, columns=cols)


def vdyt_yas_kova(yas: Any, E: Optional[Dict[str, Any]] = None) -> np.ndarray:
    K = (E or VDYT_ESIK)["yas_kova"]; y = np.asarray(yas, float); out = np.full(y.shape, -1, int)
    for i, (a, b) in enumerate(K):
        out[(y >= a) & (y <= b)] = i
    return out


# ---------------------------------------------------------------- 4) SAVUNMA HATTI (yalnız bas..t mumları)
def vdyt_savunma(o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray, v: np.ndarray, tr: np.ndarray, atr: np.ndarray, bas: int, t: int,
                 taban: str = "govde", E: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """Savunma hattı, YALNIZ bas..t barlarıyla (t'den sonraki hiçbir bar okunmaz). Taban dizisi b: govde = min(O,C), fitil = L, kapanis = C.
    tol = tolerans_tr x medyan(TR[bas..t]). Aday seviyeler: b değerlerinden bölge aralığının [min L, max H] alt_dilim'inde kalanlar. Temas(p) = |b - p| <= tol
    olan bar sayısı; p* = en çok temaslı (eşitlikte en düşük). Hat VAR <=> temas >= min_temas ve ilk / son temas arası >= min_aralik bar.
    Çıktılar: hat_var, temas, korunma (t - ilk temas), kirilma (ilk temastan sonra kapanış < p* - tol oldu mu), fitil_ihlal (L < p* - tol ama kapanış >= p* - tol
    sayısı), mesafe ((C_t - p*) / ATR_t), son_test (t - son temas), hacim_test (temas barlarının ort. hacmi / bölge medyan hacmi), yukselen_dip / alcalan_tepe
    (5'lik blok diplerinin / tepelerinin bar başına eğimi / ATR, son blok_max blok, en az 3 blok; işaretli 0/1), seviye."""
    E = E or VDYT_ESIK; S = E["savunma"]; sl = slice(bas, t + 1)
    oo, hh, ll, cc, vv = o[sl], h[sl], l[sl], c[sl], v[sl]
    b = {"govde": np.minimum(oo, cc), "fitil": ll, "kapanis": cc}[taban]
    tol = float(S["tolerans_tr"]) * float(np.nanmedian(tr[sl])); lo, hi = float(np.min(ll)), float(np.max(hh))
    out = {k: 0.0 for k in ("hat_var", "temas", "korunma", "kirilma", "fitil_ihlal", "mesafe", "son_test", "hacim_test", "yukselen_dip", "alcalan_tepe")}
    out["seviye"] = np.nan
    a_ = float(atr[t]) if np.isfinite(atr[t]) and atr[t] > 0 else np.nan
    sinir = lo + (hi - lo) * float(S["alt_dilim"]); aday = np.flatnonzero(b <= sinir)
    if len(aday) and tol > 0:
        sb = np.sort(b); p_ = b[aday]
        temas = np.searchsorted(sb, p_ + tol, side="right") - np.searchsorted(sb, p_ - tol, side="left")
        en = int(np.max(temas)); p = float(np.min(p_[temas == en]))
        tj = np.flatnonzero(np.abs(b - p) <= tol); ilk, son = int(tj[0]), int(tj[-1]); m = len(cc) - 1
        out.update({"temas": float(len(tj)), "seviye": p, "korunma": float(m - ilk), "son_test": float(m - son)})
        out["hat_var"] = float(len(tj) >= int(S["min_temas"]) and (son - ilk) >= int(S["min_aralik"]))
        sonra = slice(ilk + 1, m + 1)
        out["kirilma"] = float(np.any(cc[sonra] < p - tol))
        out["fitil_ihlal"] = float(np.sum((ll[sonra] < p - tol) & (cc[sonra] >= p - tol)))
        out["mesafe"] = (float(cc[-1]) - p) / a_ if np.isfinite(a_) else 0.0
        mv = float(np.median(vv)); out["hacim_test"] = float(np.mean(vv[tj]) / mv) if mv > 0 else 1.0
    bk = int(S["blok"]); nb = len(cc) // bk
    if nb >= 3:
        nb = min(nb, int(S["blok_max"])); kes = len(cc) - nb * bk
        dip = ll[kes:].reshape(nb, bk).min(1); tepe = hh[kes:].reshape(nb, bk).max(1); x = np.arange(nb) * bk
        if np.isfinite(a_):
            out["yukselen_dip"] = float(np.polyfit(x, dip, 1)[0] / a_ > 0)
            out["alcalan_tepe"] = float(np.polyfit(x, tepe, 1)[0] / a_ < 0)
    return out


# ---------------------------------------------------------------- 5) OLAYLAR (yalnız yerel veri; makro tarih listesi `makro` komutuyla iner)
OLAY_SUTUN = ["pazar", "sembol", "tur", "kat", "onceden", "g0_tarih", "bilgi_tarih", "kaynak", "ek"]


def _vdyt_kap_g0(zaman: pd.Series, E: Dict[str, Any]) -> Tuple[pd.Series, pd.Series]:
    """KAP yayın zamanı -> (g0 takvim günü, bilgi takvim günü): saat < seans bitişi ise o gün, değilse ertesi takvim günü (işlem gününe hizalama sonra)."""
    sb = pd.Timestamp("2000-01-01 " + E["olay"]["bist_seans_bitis"]).time()
    z = pd.to_datetime(zaman, errors="coerce"); gun = z.dt.normalize()
    sonra = z.dt.time >= sb
    g0 = gun + pd.to_timedelta(sonra.astype(int), unit="D")
    return g0, g0


def vdyt_olay_bist(semboller: Optional[List[str]] = None, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """BIST olayları: bilanço (KAP FR 2009+), hak kullanım ve sermaye değişimi (K62 fiyat), içeriden alım / satım (KAP 2022-07+), fon girişi (G.pkl 2023-01+),
    rakip bilançosu (sektörün çeyrekteki ilk bilanço günü). Döner (olay tablosu, kaynak notları)."""
    E = E or VDYT_ESIK; parca, not_ = [], {}
    # (a) KAP Finansal Rapor
    sat = []
    for f in sorted(glob.glob(os.path.join(VDYT_YOL["k62"], "kap", "*.json.gz"))):
        try:
            J = _vdyt_jsongz_oku(f)
        except (OSError, ValueError) as ex:
            vdytlog.warning("KAP dosyası okunamadı %s: %s", f, ex); continue
        for j in J:
            if (j.get("subject") or "").strip() == "Finansal Rapor" and j.get("disclosureClass") == "FR":
                for kod in str(j.get("stockCodes") or "").split(","):
                    if kod.strip():
                        sat.append((kod.strip(), j.get("publishDate"), j.get("year"), j.get("period"), j.get("disclosureIndex")))
    F = pd.DataFrame(sat, columns=["sembol", "yayin", "yil", "donem", "indeks"])
    F["zaman"] = pd.to_datetime(F.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce")
    F = F.dropna(subset=["zaman"]).sort_values("zaman").drop_duplicates(["sembol", "yil", "donem"], keep="first")
    not_["BIST_BILANCO"] = {"ham_kayit": len(sat), "ilk_rapor": len(F), "ilk": str(F.zaman.min()), "son": str(F.zaman.max())}
    g0, bi = _vdyt_kap_g0(F.zaman, E)
    parca.append(pd.DataFrame({"pazar": "BIST", "sembol": F.sembol.values, "tur": "BIST_BILANCO", "kat": "A", "onceden": True, "g0_tarih": g0.values,
                               "bilgi_tarih": bi.values, "kaynak": "KAP FR", "ek": (F.yil.astype(str) + "/" + F.donem.astype(str)).values}))
    # (b) K62 hak kullanım (ham / düzeltilmiş oranı değişimi) ve sermaye değişimi
    tem, ser = [], []
    for f in sorted(glob.glob(os.path.join(VDYT_YOL["k62"], "fiyat", "*.csv.gz"))):
        s = os.path.basename(f)[:-7]
        try:
            d = pd.read_csv(f, usecols=["tarih", "kapanis", "ham", "sermaye"])
        except (OSError, ValueError, pd.errors.EmptyDataError):
            continue
        if len(d) < 2:
            continue
        t = pd.to_datetime(d.tarih.astype(str).str[:10]); oran = (d.ham / d.kapanis).to_numpy(float); sm = d.sermaye.to_numpy(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            do = np.abs(np.diff(np.log(oran))) > 0.002
            ds = np.abs(np.diff(sm)) > 0.5
        for i in np.flatnonzero(ds) + 1:
            ser.append((s, t.iloc[i]))
        for i in np.flatnonzero(do & ~ds) + 1:
            tem.append((s, t.iloc[i]))
    for ad, L in (("BIST_TEMETTU", tem), ("BIST_SERMAYE", ser)):
        X = pd.DataFrame(L, columns=["sembol", "t"])
        not_[ad] = {"olay": len(X), "ilk": str(X.t.min()) if len(X) else None, "son": str(X.t.max()) if len(X) else None}
        T = VDYT_OLAY_TUR[ad]
        parca.append(pd.DataFrame({"pazar": "BIST", "sembol": X.sembol.values, "tur": ad, "kat": T["kat"], "onceden": T["onceden"], "g0_tarih": X.t.values,
                                   "bilgi_tarih": X.t.values, "kaynak": "K62 fiyat", "ek": ""}))
    # (c) içeriden alım / satım bildirimleri (FON_IZI fi_k27 ile aynı: aracı kurum / portföy hariç; net = gün sonu - gün başı, yoksa alım - satım)
    kl = VDYT_YOL["kap_iceriden"]; yl, yi = os.path.join(kl, "liste.csv.gz"), os.path.join(kl, "islem.csv.gz")
    if os.path.exists(yl) and os.path.exists(yi):
        L = pd.read_csv(yl); I = pd.read_csv(yi)
        haric = r"MENKUL DE[ĞG]ER|YATIRIM MENKUL|PORTF[ÖO]Y Y[ÖO]NET|B[ÜU]Y[ÜU]KŞEH|MENKUL KIYMET"
        L = L[~L.unvan.astype(str).str.upper().str.contains(haric, regex=True)]
        I = I.assign(_net=np.where(np.isfinite(I.son) & np.isfinite(I.bas), I.son - I.bas, I.alim.fillna(0) - I.satim.fillna(0)))
        G_ = I.groupby("indeks")._net.sum()
        B = L.merge(G_.rename("net"), left_on="indeks", right_index=True)
        B["sembol"] = B.ilgili.where(B.ilgili.notna() & (B.ilgili.astype(str).str.len() > 0), B.kod).astype(str).str.split(",").str[0].str.strip()
        B["zaman"] = pd.to_datetime(B.yayin, format="%d.%m.%Y %H:%M:%S", errors="coerce"); B = B.dropna(subset=["zaman"])
        for ad, m in (("BIST_ICERIDEN_ALIM", B.net > 0), ("BIST_ICERIDEN_SATIM", B.net < 0)):
            X = B[m]; g0, bi = _vdyt_kap_g0(X.zaman, E); not_[ad] = {"bildirim": int(len(X))}
            parca.append(pd.DataFrame({"pazar": "BIST", "sembol": X.sembol.values, "tur": ad, "kat": "B", "onceden": False, "g0_tarih": g0.values,
                                       "bilgi_tarih": bi.values, "kaynak": "KAP Pay Alım Satım", "ek": X.indeks.astype(str).values}))
        not_["ICERIDEN_LISTE"] = {"liste": int(len(pd.read_csv(yl))), "haric_sonrasi": int(len(L)), "ayristirilan_bildirim": int(I.indeks.nunique())}
    else:
        not_["BIST_ICERIDEN"] = "EKSİK (kap_iceriden yok: git worktree add /tmp/iv origin/islenmis-veri)"
    # (d) fon girişi (fonun önceki raporunda olmayan hisse, nominal > 0)
    if os.path.exists(VDYT_YOL["fon_G"]):
        G = _vdyt_pickle_oku(VDYT_YOL["fon_G"]); G = G[G.nominal > 0]
        R = G[["fon", "indeks", "bilinme"]].drop_duplicates().sort_values(["fon", "bilinme"])
        R["onceki"] = R.groupby("fon").indeks.shift(1)
        pos = set(zip(G.fon, G.indeks, G.kod)); gir = []
        for r in G.merge(R[["fon", "indeks", "onceki"]], on=["fon", "indeks"]).itertuples():
            if pd.notna(r.onceki) and (r.fon, int(r.onceki), r.kod) not in pos:
                gir.append((r.kod, r.bilinme, r.fon))
        X = pd.DataFrame(gir, columns=["sembol", "zaman", "fon"]).sort_values("zaman").drop_duplicates(["sembol", "fon", "zaman"])
        g0, bi = _vdyt_kap_g0(X.zaman, E); not_["BIST_FON_GIRIS"] = {"giris": int(len(X)), "rapor": int(G.indeks.nunique())}
        parca.append(pd.DataFrame({"pazar": "BIST", "sembol": X.sembol.values, "tur": "BIST_FON_GIRIS", "kat": "B", "onceden": False, "g0_tarih": g0.values,
                                   "bilgi_tarih": bi.values, "kaynak": "KAP fon raporu (G.pkl)", "ek": X.fon.values}))
    Ev = pd.concat(parca, ignore_index=True)
    # (e) rakip bilançosu
    sek = vdyt_sektor("BIST"); Bl = Ev[Ev.tur == "BIST_BILANCO"].assign(sektor=lambda x: x.sembol.map(sek)).dropna(subset=["sektor"])
    Bl = Bl.assign(ceyrek=pd.to_datetime(Bl.g0_tarih).dt.to_period("Q").astype(str))
    ilk = Bl.sort_values("g0_tarih").drop_duplicates(["sektor", "ceyrek"], keep="first"); uyeler: Dict[str, List[str]] = {}
    for s_, g_ in sek.items():
        uyeler.setdefault(g_, []).append(s_)
    rk = [(u, r.g0_tarih, r.bilgi_tarih, r.sembol) for r in ilk.itertuples() for u in uyeler.get(r.sektor, []) if u != r.sembol]
    X = pd.DataFrame(rk, columns=["sembol", "g0", "bi", "kim"]); not_["BIST_RAKIP"] = {"sektor_ceyrek": int(len(ilk)), "olay": int(len(X))}
    Ev = pd.concat([Ev, pd.DataFrame({"pazar": "BIST", "sembol": X.sembol.values, "tur": "BIST_RAKIP", "kat": "C", "onceden": True, "g0_tarih": X.g0.values,
                                      "bilgi_tarih": X.bi.values, "kaynak": "KAP FR + sektor_BIST", "ek": X.kim.values})], ignore_index=True)
    if semboller is not None:
        Ev = Ev[Ev.sembol.isin(set(semboller))]
    Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    return Ev[OLAY_SUTUN].reset_index(drop=True), not_


def vdyt_cik_ticker() -> Dict[int, List[str]]:
    """SEC company_tickers.json (bugünkü kodlar) -> {cik: [kodlar]}. Kodu değişmiş / kotasyondan çıkmış şirketler eşlenmez (beyan)."""
    if not os.path.exists(VDYT_YOL["ticker"]):
        return {}
    J = _vdyt_json_oku(VDYT_YOL["ticker"]); out: Dict[int, List[str]] = {}
    for v in J.values():
        try:
            out.setdefault(int(v["cik_str"]), []).append(str(v["ticker"]).upper().replace(".", "-"))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def vdyt_edgar(semboller: Optional[List[str]] = None, onbellek: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """EDGAR üç aylık ana dizinleri (2009Q1+) -> seçili form türleri (VDYT_EDGAR_FORM) x bugünkü kod eşlemesi. Döner (cik, sembol, form, tarih, grup)."""
    kl = VDYT_YOL["edgar"]; dosyalar = sorted(glob.glob(os.path.join(kl, "edgar_master_*.gz")))
    if not dosyalar:
        return pd.DataFrame(columns=["cik", "sembol", "form", "tarih", "grup"]), {"durum": "EKSİK (EDGAR dizini yok)"}
    anahtar = hashlib.sha256(("|".join(f"{os.path.basename(f)}:{os.path.getsize(f)}" for f in dosyalar)
                              + json.dumps(VDYT_EDGAR_FORM, sort_keys=True)).encode()).hexdigest()[:16]
    ob = _vdyt_ara(f"edgar_{anahtar}.pkl")
    if onbellek and os.path.exists(ob):
        X, not_ = _vdyt_pickle_oku(ob)
    else:
        grup = {f: g for g, L in VDYT_EDGAR_FORM.items() for f in L}; parca = []; satir = 0
        for f in dosyalar:
            D = pd.read_csv(f, sep="|", skiprows=11, header=None, names=["cik", "ad", "form", "tarih", "dosya"], dtype=str, on_bad_lines="skip")
            satir += len(D); D = D[D.form.isin(grup)]
            parca.append(D[["cik", "form", "tarih"]])
        X = pd.concat(parca, ignore_index=True); X["cik"] = pd.to_numeric(X.cik, errors="coerce"); X = X.dropna(subset=["cik"])
        X["cik"] = X.cik.astype(np.int64); X["tarih"] = pd.to_datetime(X.tarih, errors="coerce"); X = X.dropna(subset=["tarih"])
        X["grup"] = X.form.map(grup)
        ct = vdyt_cik_ticker(); Y = X[X.cik.isin(ct)]
        Y = Y.assign(sembol=Y.cik.map(ct)).explode("sembol")
        not_ = {"dosya": len(dosyalar), "satir": int(satir), "secili_form": int(len(X)), "kodla_eslenen": int(len(Y)), "ilk": str(X.tarih.min()),
                "son": str(X.tarih.max()), "cik_ticker": len(ct)}
        X = Y[["cik", "sembol", "form", "tarih", "grup"]].reset_index(drop=True)
        if onbellek:
            with open(ob, "wb") as f:
                pickle.dump((X, not_), f, protocol=pickle.HIGHEST_PROTOCOL)
    if semboller is not None:
        X = X[X.sembol.isin(set(semboller))]
    return X, not_


def _vdyt_is_gunu_ekle(t: pd.Series, n: int) -> pd.Series:
    return pd.Series(np.busday_offset(t.values.astype("datetime64[D]"), n, roll="forward"), index=t.index).astype("datetime64[ns]")


def vdyt_olay_abd(semboller: Optional[List[str]] = None, meta: Optional[Dict[str, Any]] = None, E: Optional[Dict[str, Any]] = None
                  ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """ABD olayları: bilanço (Nasdaq takvimi 2022-12+; öncesi 10-Q / 10-K başvuru günü VEKİL), temettü / bölünme (Yahoo), EDGAR form grupları, rakip bilançosu."""
    E = E or VDYT_ESIK; parca, not_ = [], {}
    yl = os.path.join(VDYT_YOL["pead"], "liste_abd.csv.gz"); nas_bas = pd.Timestamp("2022-12-01")
    if os.path.exists(yl):
        N = pd.read_csv(yl).dropna(subset=["sembol"]); N["tarih"] = pd.to_datetime(N.tarih)
        N["sembol"] = N.sembol.astype(str).str.upper().str.replace(".", "-", regex=False)
        N = N.drop_duplicates(["sembol", "tarih"]); sonra = N.saat.astype(str).eq("time-after-hours")
        g0 = N.tarih + pd.to_timedelta(sonra.astype(int), unit="D"); nas_bas = N.tarih.min()
        not_["NASDAQ"] = {"satir": int(len(N)), "ilk": str(N.tarih.min()), "son": str(N.tarih.max()), "saat": N.saat.value_counts().to_dict()}
        parca.append(pd.DataFrame({"pazar": "ABD", "sembol": N.sembol.values, "tur": "ABD_BILANCO", "kat": "A", "onceden": True, "g0_tarih": g0.values,
                                   "bilgi_tarih": g0.values, "kaynak": "Nasdaq", "ek": N.saat.astype(str).values}))
    else:
        not_["NASDAQ"] = "EKSİK"
    X, not_["EDGAR"] = vdyt_edgar(semboller)
    bil = X[(X.grup == "ABD_BILANCO_EDGAR") & (X.tarih < nas_bas)].drop_duplicates(["sembol", "tarih"])
    parca.append(pd.DataFrame({"pazar": "ABD", "sembol": bil.sembol.values, "tur": "ABD_BILANCO", "kat": "A", "onceden": True, "g0_tarih": bil.tarih.values,
                               "bilgi_tarih": _vdyt_is_gunu_ekle(bil.tarih, 1).values, "kaynak": "EDGAR 10-Q/10-K (vekil)", "ek": bil.form.values}))
    for g, L in VDYT_EDGAR_FORM.items():
        if g == "ABD_BILANCO_EDGAR":
            continue
        Y = X[X.grup == g].drop_duplicates(["sembol", "tarih"]); T = VDYT_OLAY_TUR[g]
        parca.append(pd.DataFrame({"pazar": "ABD", "sembol": Y.sembol.values, "tur": g, "kat": T["kat"], "onceden": T["onceden"], "g0_tarih": Y.tarih.values,
                                   "bilgi_tarih": _vdyt_is_gunu_ekle(Y.tarih, 1).values, "kaynak": "EDGAR", "ek": Y.form.values}))
    if meta:
        tm = [(s, t) for s, m in meta.items() for t in (m.get("temettu") or [])] + [(s, t) for s, m in meta.items() for t, _r in (m.get("bolunme") or [])]
        T_ = pd.DataFrame(tm, columns=["sembol", "t"]).drop_duplicates()
        parca.append(pd.DataFrame({"pazar": "ABD", "sembol": T_.sembol.values, "tur": "ABD_TEMETTU", "kat": "A", "onceden": True, "g0_tarih": T_.t.values,
                                   "bilgi_tarih": T_.t.values, "kaynak": "Yahoo olayları", "ek": ""}))
    Ev = pd.concat(parca, ignore_index=True); Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    # 8-K: bilanço günü +-3 iş günü içindekiler (bilanço 8-K'sı) çıkarılır
    B = Ev[Ev.tur == "ABD_BILANCO"]; K8 = Ev[Ev.tur == "ABD_8K"]
    if len(K8) and len(B):
        bg = {s: np.sort(g.g0_tarih.values.astype("datetime64[D]")) for s, g in B.groupby("sembol")}
        yakin = np.zeros(len(K8), bool)
        for j, (s, t) in enumerate(zip(K8.sembol.values, K8.g0_tarih.values.astype("datetime64[D]"))):
            a = bg.get(s)
            if a is not None and len(a):
                p = np.searchsorted(a, t); kom = [a[q] for q in (p - 1, p) if 0 <= q < len(a)]
                yakin[j] = any(abs(int(np.busday_count(min(t, x), max(t, x)))) <= 3 for x in kom)
        not_["ABD_8K_bilanco_yakini_cikan"] = int(yakin.sum()); Ev = Ev.drop(index=K8.index[yakin])
    # rakip bilançosu (SIC grubu)
    sek = vdyt_sektor("ABD"); Bl = Ev[Ev.tur == "ABD_BILANCO"].assign(sektor=lambda x: x.sembol.map(sek)).dropna(subset=["sektor"])
    Bl = Bl.assign(ceyrek=Bl.g0_tarih.dt.to_period("Q").astype(str)); ilk = Bl.sort_values("g0_tarih").drop_duplicates(["sektor", "ceyrek"])
    uyeler: Dict[str, List[str]] = {}
    for s_, g_ in sek.items():
        if semboller is None or s_ in set(semboller):
            uyeler.setdefault(g_, []).append(s_)
    rk = [(u, r.g0_tarih, r.bilgi_tarih, r.sembol) for r in ilk.itertuples() for u in uyeler.get(r.sektor, []) if u != r.sembol]
    R_ = pd.DataFrame(rk, columns=["sembol", "g0", "bi", "kim"]); not_["ABD_RAKIP"] = {"sektor_ceyrek": int(len(ilk)), "olay": int(len(R_))}
    Ev = pd.concat([Ev, pd.DataFrame({"pazar": "ABD", "sembol": R_.sembol.values, "tur": "ABD_RAKIP", "kat": "C", "onceden": True, "g0_tarih": R_.g0.values,
                                      "bilgi_tarih": R_.bi.values, "kaynak": "bilanço + SIC", "ek": R_.kim.values})], ignore_index=True)
    if semboller is not None:
        Ev = Ev[Ev.sembol.isin(set(semboller))]
    Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    return Ev[OLAY_SUTUN].reset_index(drop=True), not_


def vdyt_sektor(pazar: str) -> Dict[str, str]:
    """BIST: sektor_BIST.csv 'sektor' (BIST alt endekslerinden, 12 grup). ABD: SEC SIC 2 haneli ana grup (k35_sic, CIK -> bugünkü kod); 10'dan az üyeli
    grup SIC bölümüne (division) birleştirilir. Eşlenemeyen hisse sektörsüz (sektör rejimi / rakip olayı NaN)."""
    if pazar.startswith("BIST"):
        if not os.path.exists(VDYT_YOL["sektor_bist"]):
            return {}
        d = pd.read_csv(VDYT_YOL["sektor_bist"]); return dict(zip(d.sembol.astype(str), d.sektor.astype(str)))
    if not os.path.exists(VDYT_YOL["sic"]):
        return {}
    d = pd.read_csv(VDYT_YOL["sic"]).dropna(subset=["sic"]); ct = vdyt_cik_ticker(); sat = []
    for r in d.itertuples():
        for s in ct.get(int(r.cik), []):
            sat.append((s, int(r.sic)))
    X = pd.DataFrame(sat, columns=["sembol", "sic"]).drop_duplicates("sembol")
    X["ana"] = (X.sic // 100).astype(int)

    def bolum(a: int) -> str:
        for lo, hi, ad in ((1, 9, "A"), (10, 14, "B"), (15, 17, "C"), (20, 39, "D"), (40, 49, "E"), (50, 51, "F"), (52, 59, "G"), (60, 67, "H"),
                           (70, 89, "I"), (91, 99, "J")):
            if lo <= a <= hi:
                return "DIV_" + ad
        return "DIV_X"
    say = X.ana.value_counts()
    X["grup"] = [f"SIC{a:02d}" if say[a] >= 10 else bolum(a) for a in X.ana]
    return dict(zip(X.sembol, X.grup))


# ---------------------------------------------------------------- 6) MAKRO TAKVİM (yalnız TARİH; içerik / sürpriz yok)
_AYLAR_TR = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}
_AYLAR_EN = {m[:3]: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
                                              "December"], 1)}


def _vdyt_ay_en(ad: str) -> Optional[int]:
    return _AYLAR_EN.get(ad.strip()[:3].title())


def vdyt_fomc_ayristir(metin: str, yil: Optional[int] = None) -> List[Tuple[str, bool]]:
    """federalreserve.gov FOMC sayfası -> [(karar günü ISO, planlı mı)]. Karar günü = toplantının son günü; 'unscheduled' / 'conference call' / 'cancelled'
    planlı değil ('notation vote' toplantı sayılmaz); güncel sayfadaki '*' = projeksiyonlu toplantı (planlı)."""
    out = []
    for m in re.finditer(r'<h5[^>]*>\s*([A-Za-z/]+)\s+(\d{1,2})(?:-(\d{1,2}))?\s*([^<]*?)Meeting\s*-\s*(\d{4})\s*</h5>', metin):
        aylar = m.group(1).split("/"); g1, g2, ek, y = m.group(2), m.group(3), m.group(4), int(m.group(5))
        ay = _vdyt_ay_en(aylar[-1] if g2 else aylar[0]); gun = int(g2 or g1)
        if ay:
            out.append((f"{y:04d}-{ay:02d}-{gun:02d}", not any(x in ek.lower() for x in ("unscheduled", "conference", "cancel"))))
    for blok in re.finditer(r'<h4><a id="\d+">(\d{4}) FOMC Meetings</a></h4>(.*?)(?=<h4><a id="\d+">\d{4} FOMC Meetings|$)', metin, re.S):
        y = int(blok.group(1))
        for mm in re.finditer(r'fomc-meeting__month[^>]*><strong>([^<]+)</strong>.*?fomc-meeting__date[^>]*>([^<]+)<', blok.group(2), re.S):
            aylar = mm.group(1).strip().split("/"); tarih = mm.group(2).strip()
            if "notation" in tarih.lower():
                continue
            planli = not any(x in tarih.lower() for x in ("unscheduled", "cancel"))   # "*" = ekonomik projeksiyon toplantısı (planlı)
            gunler = re.findall(r"\d{1,2}", tarih)
            if not gunler:
                continue
            ay = _vdyt_ay_en(aylar[-1] if len(gunler) > 1 or len(aylar) == 1 else aylar[0])
            if ay:
                out.append((f"{y:04d}-{ay:02d}-{int(gunler[-1]):02d}", planli))
    return sorted(set(out))


def vdyt_ppk_ayristir(metin: str) -> List[str]:
    """tcmb.gov.tr PPK yıl sayfası -> karar günleri (tablonun ilk sütunu: 'Para Politikası Kurulu Toplantı Kararı')."""
    out = []
    for tr_ in re.findall(r"<tr>(.*?)</tr>", metin, re.S):
        td = re.findall(r"<td[^>]*>(.*?)</td>", tr_, re.S)
        if not td:
            continue
        m = re.search(r"(\d{1,2})\s+(" + "|".join(_AYLAR_TR) + r")\s+(\d{4})", _html.unescape(re.sub("<[^>]+>", " ", td[0])))
        if m:
            out.append(f"{int(m.group(3)):04d}-{_AYLAR_TR[m.group(2)]:02d}-{int(m.group(1)):02d}")
    return sorted(set(out))


def vdyt_makro_indir(getir: Optional[Callable[[str], Optional[str]]] = None, yil_bas: int = 2009, yil_bit: int = 2026) -> Dict[str, Any]:
    """Resmi kaynaklardan yalnız TARİH listesi: FOMC (federalreserve.gov fomccalendars + fomchistorical<yıl>) ve TCMB PPK (tcmb.gov.tr PPK/<yıl>).
    BLS (CPI / istihdam) ve TÜİK yayın günleri bu ortamda erişilemedi -> EKSİK. Yazılan: VDYT_YOL['makro'] (JSON; kaynak, tarih, planlı)."""
    import urllib.request

    def _getir(u: str) -> Optional[str]:
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": _VDYT_UA}), timeout=40)
            return r.read().decode("utf-8", "ignore")
        except Exception as ex:   # ağ hatası: o sayfa EKSİK yazılır, diğerleri sürer
            vdytlog.warning("makro sayfa alınamadı %s: %s", u, str(ex)[:120]); return None
    getir = getir or _getir; fomc, ppk, eksik = set(), set(), []
    m = getir("https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm")
    if m:
        fomc |= set(vdyt_fomc_ayristir(m))
    else:
        eksik.append("fomccalendars")
    for y in range(yil_bas, yil_bit + 1):
        if any(t.startswith(str(y)) for t, _p in fomc):
            continue
        m = getir(f"https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm"); time.sleep(0.5)
        if m:
            fomc |= set(vdyt_fomc_ayristir(m, y))
        else:
            eksik.append(f"fomchistorical{y}")
    for y in range(yil_bas, yil_bit + 1):
        m = getir(f"https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/PPK/{y}"); time.sleep(0.5)
        g = vdyt_ppk_ayristir(m) if m else []
        if g:
            ppk |= set(g)
        else:
            eksik.append(f"PPK{y}")
    out = {"uretim": _vdyt_simdi(), "surum": VDYT_SURUM,
           "kaynak": {"FOMC": "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm + fomchistorical<yıl>.htm",
                      "PPK": "https://www.tcmb.gov.tr/.../Para+Politikasi/PPK/<yıl>"},
           "FOMC": [{"tarih": t, "planli": p} for t, p in sorted(fomc)], "PPK": [{"tarih": t, "planli": True} for t in sorted(ppk)],
           "EKSIK": {"CPI_BLS": "bls.gov 403 (erişim engeli)", "ISTIHDAM_BLS": "bls.gov 403", "TUIK_ENFLASYON": "data.tuik.gov.tr yayın takvimi alınmadı",
                     "sayfa": eksik}}
    _vdyt_json(VDYT_YOL["makro"], out); vdytlog.info("makro takvim: FOMC %d, PPK %d, eksik sayfa %d", len(fomc), len(ppk), len(eksik))
    return out


def vdyt_olay_makro(pazar: str, E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Piyasa geneli olaylar (sembol '*'): FOMC (planlı), PPK, emtia / kur / faiz şokları (surucu.pkl). g0 pazar kuralına göre (VDYT_OLAY_TUR)."""
    E = E or VDYT_ESIK; parca, not_ = [], {}; bist = pazar.startswith("BIST")
    if os.path.exists(VDYT_YOL["makro"]):
        M = _vdyt_json_oku(VDYT_YOL["makro"])
        F = pd.to_datetime([x["tarih"] for x in M.get("FOMC", []) if x.get("planli")]); P = pd.to_datetime([x["tarih"] for x in M.get("PPK", [])])
        not_["FOMC"] = len(F); not_["PPK"] = len(P)
        gF = F + pd.Timedelta(days=1) if bist else F
        parca.append(pd.DataFrame({"pazar": pazar, "sembol": "*", "tur": "MAKRO_FOMC", "kat": "C", "onceden": True, "g0_tarih": gF, "bilgi_tarih": gF,
                                   "kaynak": "federalreserve.gov", "ek": ""}))
        parca.append(pd.DataFrame({"pazar": pazar, "sembol": "*", "tur": "MAKRO_PPK", "kat": "C", "onceden": True, "g0_tarih": P, "bilgi_tarih": P,
                                   "kaynak": "tcmb.gov.tr", "ek": ""}))
    else:
        not_["MAKRO_TAKVIM"] = "EKSİK (python VDYT.py makro)"
    if os.path.exists(VDYT_YOL["surucu"]):
        Sr = _vdyt_pickle_oku(VDYT_YOL["surucu"]); O = E["olay"]; sat = []
        for ad, s in Sr.items():
            if ad == "CDS":
                continue
            s = pd.Series(s).dropna(); s = s[s > 0]; r = np.log(s).diff()
            sd = r.rolling(int(O["emtia_gecmis"]), min_periods=int(O["emtia_gecmis"]) - 50).std().shift(1)
            for t in r.index[(r.abs() >= float(O["emtia_soku_z"]) * sd).to_numpy()]:
                sat.append((t, ad))
        X = pd.DataFrame(sat, columns=["t", "seri"]); not_["MAKRO_EMTIA"] = {"sok_gun": int(len(X)), "seri": sorted(X.seri.unique().tolist()) if len(X) else []}
        g0 = X.t + pd.Timedelta(days=1) if bist else X.t
        parca.append(pd.DataFrame({"pazar": pazar, "sembol": "*", "tur": "MAKRO_EMTIA", "kat": "C", "onceden": False, "g0_tarih": g0.values,
                                   "bilgi_tarih": (X.t + pd.Timedelta(days=1)).values, "kaynak": "surucu.pkl", "ek": X.seri.values}))
    else:
        not_["MAKRO_EMTIA"] = "EKSİK (surucu.pkl yok)"
    if not parca:
        return pd.DataFrame(columns=OLAY_SUTUN), not_
    Ev = pd.concat(parca, ignore_index=True); Ev["g0_tarih"] = pd.to_datetime(Ev.g0_tarih); Ev["bilgi_tarih"] = pd.to_datetime(Ev.bilgi_tarih)
    return Ev[OLAY_SUTUN], not_


def vdyt_olaylar(pazar: str, F: Dict[str, Any], E: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazarın bütün olayları (hisse + piyasa geneli). BIST_K62 BIST hisse olaylarını kullanır."""
    sem = sorted(F["S"])
    if pazar.startswith("BIST"):
        Ev, n1 = vdyt_olay_bist(sem, E)
        if pazar == "BIST_K62":
            Ev = Ev.assign(pazar="BIST_K62")
    else:
        Ev, n1 = vdyt_olay_abd(sem, F.get("meta"), E)
    Mk, n2 = vdyt_olay_makro(pazar, E)
    return pd.concat([Ev, Mk], ignore_index=True), {**n1, **n2}


def vdyt_olay_hizala(gun: pd.DatetimeIndex, tarih: Any) -> np.ndarray:
    """Takvim tarihlerini hissenin işlem günü indeksine hizalar: tarihten sonraki (ya da aynı) ilk işlem günü; yoksa -1."""
    g = gun.to_numpy("datetime64[ns]"); t = pd.to_datetime(pd.Series(tarih)).to_numpy("datetime64[ns]")
    i = np.searchsorted(g, t, side="left")
    return np.where(i < len(g), i, -1).astype(np.int64)


# ---------------------------------------------------------------- 7) PAZAR HAZIRLIĞI (panel, uygunluk, bölge kombinasyonları)
def vdyt_kombolar(pazar: str, E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Ön kayıtlı tanım x eşik x genişleme kombinasyonları. ANA: T1-T5 ana eşik, TR genişleme, k = ana_k (BIST_K62: T2-T4, RV). DUYARLILIK: T1-T4 alternatif
    eşikler (ana k); T1 için k alternatifleri ve RV genişlemesi (K62'de yalnız alternatif eşikler)."""
    E = E or VDYT_ESIK; G = E["genisleme"]; k0 = float(G["ana_k"]); out = []
    if pazar == "BIST_K62":
        for t in ("T2", "T3", "T4"):
            out.append({"ad": t, "tanim": t, "esik_idx": 0, "k": k0, "tur": "RV", "rol": "ana"})
        for t in ("T2", "T3", "T4"):
            for e in (1, 2):
                out.append({"ad": f"{t}_e{E['tanim'][t]['esik'][e]}", "tanim": t, "esik_idx": e, "k": k0, "tur": "RV", "rol": "duyarlilik"})
        return out
    for t in ("T1", "T2", "T3", "T4", "T5"):
        out.append({"ad": t, "tanim": t, "esik_idx": 0, "k": k0, "tur": G["ana_tur"], "rol": "ana"})
    for t in ("T1", "T2", "T3", "T4"):
        for e in (1, 2):
            out.append({"ad": f"{t}_e{E['tanim'][t]['esik'][e]}", "tanim": t, "esik_idx": e, "k": k0, "tur": G["ana_tur"], "rol": "duyarlilik"})
    t = E["duyarlilik"]["k_alt_tanim"]
    for k in G["k"]:
        if float(k) != k0:
            out.append({"ad": f"{t}_k{k}", "tanim": t, "esik_idx": 0, "k": float(k), "tur": G["ana_tur"], "rol": "duyarlilik"})
    out.append({"ad": f"{E['duyarlilik']['rv_tanim']}_RV", "tanim": E["duyarlilik"]["rv_tanim"], "esik_idx": 0, "k": k0, "tur": "RV", "rol": "duyarlilik"})
    return out


def _vdyt_panel_satir(arg: Tuple[str, pd.DataFrame, Dict[str, Any]]) -> Tuple[str, Dict[str, pd.Series]]:
    s, d, E = arg
    Ol = vdyt_olculer(d, E); ix = d.index
    return s, {k: pd.Series(Ol[k].astype(np.float32), index=ix) for k in ("rv_yuzde", "ret20", "ret60", "deger20", "natr", "lr", "bar_no")}


def _vdyt_harita(fn: Callable, isler: List[Any], isci: int) -> List[Any]:
    if isci and isci > 1 and len(isler) > 50:
        import multiprocessing as mp
        try:
            with mp.get_context("fork").Pool(isci) as p:
                return p.map(fn, isler, chunksize=max(1, len(isler) // (isci * 8)))
        except (OSError, ValueError) as ex:   # fork yoksa (ör. bazı not defterleri) tek işçiye düşer
            vdytlog.warning("paralel çalışma açılamadı (%s); tek işçi", ex)
    return [fn(x) for x in isler]


def vdyt_panel(pazar: str, F: Dict[str, Any], E: Optional[Dict[str, Any]] = None, isci: int = 2) -> Dict[str, Any]:
    """Kesit bilgileri (her gün yalnız o günün değerleri): pazar takvimi, uygunluk, momentum / likidite tertilleri, sektör rejimi ve yönü, endeks rejimi ve yönü,
    mutlak NATR ondalığı (K6 karşılaştırması için)."""
    E = E or VDYT_ESIK; S = F["S"]; U = E["pazar"]["BIST" if pazar.startswith("BIST") else "ABD"]["uygunluk"]
    R = dict(_vdyt_harita(_vdyt_panel_satir, [(s, S[s], E) for s in sorted(S)], isci))
    takvim = pd.DatetimeIndex(sorted(set().union(*[S[s].index for s in S]))) if S else pd.DatetimeIndex([])
    P = {k: pd.DataFrame({s: R[s][k] for s in R}).reindex(takvim) for k in ("rv_yuzde", "ret20", "ret60", "deger20", "natr", "bar_no")}
    gec = P["bar_no"] >= float(U["gecmis_gun"])
    if pazar.startswith("BIST"):
        esik = P["deger20"].quantile(float(U["likit_pct"]), axis=1)
        uygun = gec & P["deger20"].ge(esik, axis=0)
    else:
        M = F.get("meta", {}); tur_ok = pd.Series({s: (M.get(s, {}).get("tur") in U["tur"]) for s in P["deger20"].columns})
        carp = pd.DataFrame({s: pd.Series(vdyt_bolunme_carpan(M.get(s, {}).get("bolunme") or [], S[s].index), index=S[s].index) for s in S}).reindex(takvim)
        kap = pd.DataFrame({s: S[s].c for s in S}).reindex(takvim) * carp
        uygun = gec & (P["deger20"] >= float(U["likit_min"])) & (kap >= float(U["fiyat_min"]))
        uygun.loc[:, ~tur_ok.reindex(uygun.columns).fillna(False).to_numpy(bool)] = False
    uygun = uygun & P["deger20"].notna()

    def tertil(X: pd.DataFrame) -> pd.DataFrame:
        r = X.where(uygun).rank(axis=1, pct=True)
        return np.floor(r.clip(upper=0.999999) * 3).where(r.notna())
    sek = vdyt_sektor(pazar); grup = pd.Series({s: sek.get(s) for s in P["rv_yuzde"].columns})
    rj_s, ret_s = {}, {}
    for g, uy in grup.dropna().groupby(grup.dropna()):
        cols = list(uy.index)
        if len(cols) >= int(E["rejim"]["sektor_min"]):
            rj_s[g] = P["rv_yuzde"][cols].where(uygun[cols]).median(axis=1); ret_s[g] = P["ret20"][cols].where(uygun[cols]).median(axis=1)
    en = vdyt_endeks(pazar, E)
    if en is not None and len(en) > 300:
        en2 = en.copy()
        for k_ in ("o", "h", "l"):
            en2[k_] = (en2[k_] if k_ in en2 else en2.c).fillna(en2.c)
        en2["v"] = (en2.v if "v" in en2 else pd.Series(0.0, index=en2.index)).fillna(0.0) + 1.0
        Oe = vdyt_olculer(en2[["o", "h", "l", "c", "v"]], E)
        rj_p = pd.Series(Oe["rv_yuzde"], index=en.index).reindex(takvim, method="ffill")
        pr60 = pd.Series(Oe["ret60"], index=en.index).reindex(takvim, method="ffill"); plr = pd.Series(Oe["lr"], index=en.index).reindex(takvim)
        kaynak_en = "endeks"
    else:   # endeks yoksa: eşit ağırlıklı medyan (beyan)
        med_lr = pd.DataFrame({s: R[s]["lr"] for s in R}).reindex(takvim).median(axis=1)
        rv = med_lr.rolling(20).std(); rj_p = pd.Series(vdyt_yuzde_gecmis(rv.to_numpy(), 250, 200), index=takvim)
        pr60 = med_lr.rolling(60).sum(); plr = med_lr; kaynak_en = "medyan"
    nd = P["natr"].where(uygun).rank(axis=1, pct=True)
    return {"takvim": takvim, "uygun": uygun, "mom_t": tertil(P["ret60"]), "liq_t": tertil(P["deger20"]), "sektor": sek,
            "rj_sektor": pd.DataFrame(rj_s).reindex(takvim) if rj_s else pd.DataFrame(index=takvim),
            "p_sektor_ret20": pd.DataFrame(ret_s).reindex(takvim) if ret_s else pd.DataFrame(index=takvim),
            "rj_pazar": rj_p, "p_pazar_ret60": pr60, "p_pazar_lr": plr, "endeks_kaynak": kaynak_en,
            "natr_ondalik": np.floor(nd.clip(upper=0.999999) * 10).where(nd.notna())}


def _vdyt_bolge_tablosu(s: str, d: pd.DataFrame, Ol: Dict[str, np.ndarray], kombolar: List[Dict[str, Any]], uygun: Optional[np.ndarray],
                        E: Dict[str, Any], yon: bool) -> Dict[str, pd.DataFrame]:
    kop = vdyt_kopuk(d.index, E); c = d.c.to_numpy(float); out = {}
    for K in kombolar:
        dur = vdyt_durum(Ol, K["tanim"], K["esik_idx"], E)
        B = vdyt_bolgeler(dur, Ol["trn"], Ol["lr"], kop, K["k"], K["tur"], E)
        T = pd.DataFrame(B, columns=["bas", "tespit", "bit", "bit_tur", "gen_bas"])
        T.insert(0, "sembol", s); T["sure"] = T.bit - T.bas + 1
        T["bas_tarih"] = d.index[T.bas.to_numpy()] if len(T) else pd.DatetimeIndex([])
        T["tespit_tarih"] = d.index[T.tespit.to_numpy()] if len(T) else pd.DatetimeIndex([])
        T["bit_tarih"] = d.index[T.bit.to_numpy()] if len(T) else pd.DatetimeIndex([])
        T["uygun"] = uygun[T.tespit.to_numpy()] if (uygun is not None and len(T)) else True
        if yon:
            y1, y2 = vdyt_yon(c, B, E); T["Y1"] = y1; T["Y2"] = y2
        out[K["ad"]] = T
    return out


def vdyt_hisse_uygun(s: str, d: pd.DataFrame, Pn: Dict[str, Any]) -> np.ndarray:
    u = Pn["uygun"][s] if s in Pn["uygun"] else None
    return np.zeros(len(d), bool) if u is None else u.reindex(d.index).fillna(False).to_numpy(bool)


# ---------------------------------------------------------------- 8) KARAR NOKTASI ÖZELLİKLERİ (bilgi tarihi <= karar günü t)
def vdyt_hisse_baglam(s: str, d: pd.DataFrame, Pn: Dict[str, Any], Ev_s: pd.DataFrame, Ev_m: pd.DataFrame) -> Dict[str, Any]:
    """Hisse günlerine hizalanmış kesit serileri ve olay indeksleri. Ev_s: hissenin olayları, Ev_m: piyasa geneli olaylar. Bilgi indeksi = bilgi tarihinden
    sonraki (ya da aynı) ilk işlem günü; özellikler yalnız bilgi indeksi <= t olan olayları görür."""
    ix = d.index; sek = Pn["sektor"].get(s)

    def al(X: Any) -> np.ndarray:
        if isinstance(X, pd.Series):
            return X.reindex(ix).to_numpy(float)
        return X[s].reindex(ix).to_numpy(float) if s in X else np.full(len(ix), np.nan)
    ctx = {"rj_pazar": al(Pn["rj_pazar"]), "p_pazar_ret60": al(Pn["p_pazar_ret60"]), "p_lr": al(Pn["p_pazar_lr"]),
           "rj_sektor": Pn["rj_sektor"][sek].reindex(ix).to_numpy(float) if sek in Pn["rj_sektor"] else np.full(len(ix), np.nan),
           "p_sektor_ret20": Pn["p_sektor_ret20"][sek].reindex(ix).to_numpy(float) if sek in Pn["p_sektor_ret20"] else np.full(len(ix), np.nan),
           "mom_t": al(Pn["mom_t"]), "liq_t": al(Pn["liq_t"]), "natr_d": al(Pn["natr_ondalik"]), "sektor": sek}
    gun = ix.to_numpy("datetime64[D]")
    bil = Ev_s[Ev_s.tur.str.endswith("_BILANCO")].sort_values("g0_tarih")
    ctx["bilanco_tarih"] = pd.to_datetime(bil.g0_tarih).to_numpy("datetime64[D]")
    ctx["bilanco_bilgi_i"] = vdyt_olay_hizala(ix, bil.bilgi_tarih)
    Bb = Ev_s[Ev_s.kat == "B"]
    ctx["B_bilgi_i"] = vdyt_olay_hizala(ix, Bb.bilgi_tarih); ctx["B_g0_i"] = vdyt_olay_hizala(ix, Bb.g0_tarih)
    pl = Ev_m[(Ev_m.onceden.astype(bool)) & Ev_m.tur.isin(["MAKRO_FOMC", "MAKRO_PPK"])]
    ctx["makro_g0_i"] = np.unique(vdyt_olay_hizala(ix, pl.g0_tarih)); ctx["gun"] = gun
    return ctx


def vdyt_beklenen_bilanco(gecmis: np.ndarray, t_gun: np.datetime64) -> Tuple[float, float]:
    """Yalnız t'ye kadar bilinen bilanço günlerinden: adaylar = son 12 aydaki raporların yıldönümleri ve son rapor + 91 gün; beklenen sonraki bilanço =
    adaylardan t'den sonraki en yakını. Döner (beklenene takvim günü ya da NaN, son rapordan bu yana takvim günü ya da NaN)."""
    g = np.sort(gecmis[gecmis <= t_gun])
    if not len(g):
        return np.nan, np.nan
    son = float((t_gun - g[-1]).astype(int))
    aday = np.r_[g[g > t_gun - np.timedelta64(365, "D")] + np.timedelta64(365, "D"), g[-1] + np.timedelta64(91, "D")]
    aday = aday[aday > t_gun]
    return (float((aday.min() - t_gun).astype(int)) if len(aday) else np.nan), son


def vdyt_hisse_karar(s: str, d: pd.DataFrame, Ol: Dict[str, np.ndarray], T: pd.DataFrame, ctx: Dict[str, Any], pazar: str,
                     E: Optional[Dict[str, Any]] = None, tabanlar: bool = True) -> pd.DataFrame:
    """Bir hissenin bir kombinasyondaki karar noktaları: etiketler (y5/y10/y20, bölgenin Y1/Y2'si), çözülme tarihleri, eşleme anahtarları, özellikler
    (VDYT_OZELLIK; hepsi t ve öncesi), bilgi amaçlı getiriler (t+1 açılıştan; maliyet sonrası) ve MFE / MAE."""
    E = E or VDYT_ESIK; n = len(d); o, h, l, c, v = (d[k].to_numpy(float) for k in ("o", "h", "l", "c", "v")); gun = d.index
    B = T[["bas", "tespit", "bit", "bit_tur", "gen_bas"]].to_numpy(np.int64)
    KN = vdyt_karar_noktalari(B, n, E)
    if not len(KN):
        return pd.DataFrame()
    KN = KN[T.uygun.to_numpy(bool)[KN.bolge.to_numpy()]]
    if not len(KN):
        return pd.DataFrame()
    mal = float(E["pazar"]["BIST" if pazar.startswith("BIST") else "ABD"]["maliyet"]); Hm = E["hisse_gecmis"]; sat = []
    for r_, a, t in KN[["bolge", "yas", "t"]].itertuples(index=False):
        bas, tes, bit, tur, gb = B[r_]
        row: Dict[str, Any] = {"sembol": s, "bolge": int(r_), "yas": int(a), "t": int(t), "tarih": gun[t], "bit": int(bit), "gen_bas": int(gb),
                               "Y1": float(T.Y1.iat[r_]) if "Y1" in T else np.nan, "Y2": float(T.Y2.iat[r_]) if "Y2" in T else np.nan}
        for hh in E["ufuk"]:
            row[f"son{hh}"] = gun[min(t + hh, n - 1)]
        row["y1_son"] = gun[min(bit + int(E["yon"]["Y1_ufuk"]), n - 1)]
        row["mom_t"] = ctx["mom_t"][t]; row["liq_t"] = ctx["liq_t"][t]; row["natr_d"] = ctx["natr_d"][t]
        # SURE + HISSE
        row["yas_log"] = float(np.log(a))
        for kk in (20, 40, 60, 90, 120):
            row[f"yk_{kk}"] = float(a >= kk)
        once = B[:r_]; once = once[np.isin(once[:, 3], (BITIS_GEN, BITIS_SONME))]
        if len(once) >= int(Hm["min_bolge"]):
            sure = once[:, 2] - once[:, 0] + 1
            row.update({"hs_oran": a / float(np.median(sure)), "hs_yetersiz": 0.0, "hs_gen_pay": float(np.mean(once[:, 3] == BITIS_GEN))})
        else:
            row.update({"hs_oran": 0.0, "hs_yetersiz": 1.0, "hs_gen_pay": 0.0})
        # REJIM + PAZAR
        row.update({"rj_pazar": ctx["rj_pazar"][t], "rj_sektor": ctx["rj_sektor"][t], "p_pazar_ret60": ctx["p_pazar_ret60"][t],
                    "p_sektor_ret20": ctx["p_sektor_ret20"][t]})
        # VOL / HACIM / MUM / FIYAT
        ref = Ol["trn"][bas: max(bas, t - 2)]
        row.update({"v_natr_oran": Ol["natr_oran"][t], "v_rv_yuzde": Ol["rv_yuzde"][t], "v_bbw_yuzde": Ol["bbw_yuzde"][t], "v_bant": Ol["bant"][t],
                    "v_rv5_rv20": Ol["rv5_rv20"][t],
                    "v_tr_son3": float(np.mean(Ol["trn"][t - 2: t + 1]) / np.median(ref)) if len(ref) >= 3 and np.median(ref) > 0 else np.nan,
                    "h_hacim_oran": Ol["hacim_oran"][t], "h_yukselen_hacim": Ol["yuk_hacim"][t],
                    "h_hacim_son5": float(np.mean(v[t - 4: t + 1]) / np.median(v[bas: t + 1])) if np.median(v[bas: t + 1]) > 0 else np.nan,
                    "m_govde_aralik": Ol["govde_aralik"][t], "m_govde_gecmis": Ol["govde_gecmis"][t], "m_fitil_ust": Ol["fitil_ust"][t],
                    "m_fitil_alt": Ol["fitil_alt"][t], "m_kapanis_konum": Ol["kap_konum"][t],
                    "f_sma20": Ol["sma20"][t], "f_sma50": Ol["sma50"][t], "f_sma200": Ol["sma200"][t], "f_sma50_egim": Ol["sma50_egim"][t],
                    "f_ret20": Ol["ret20"][t], "f_ret60": Ol["ret60"][t], "f_likidite": Ol["likidite"][t]})
        lo, hi = float(np.min(c[bas: t + 1])), float(np.max(c[bas: t + 1]))
        row["f_bolge_konum"] = (c[t] - lo) / (hi - lo) if hi > lo else 0.5
        # OLAY (bilgi indeksi <= t)
        bb = ctx["bilanco_bilgi_i"]
        bg, bs = vdyt_beklenen_bilanco(ctx["bilanco_tarih"][(bb >= 0) & (bb <= t)], ctx["gun"][t])
        row["o_bilanco_gun"] = float(np.clip(bg, 0, 90)) if np.isfinite(bg) else 90.0; row["o_bilanco_yok"] = float(not np.isfinite(bg))
        row["o_bilanco_son"] = float(np.clip(bs, 0, 120)) if np.isfinite(bs) else 120.0
        mg = ctx["makro_g0_i"]; row["o_makro_10"] = float(np.any((mg > t) & (mg <= t + 10)))
        bi, b0 = ctx["B_bilgi_i"], ctx["B_g0_i"]; ok = (bi >= 0) & (bi <= t)
        row["o_olay_son5"] = float(np.sum(ok & (bi > t - 5))); row["o_olay_son20"] = float(np.sum(ok & (bi > t - 20)))
        son = np.flatnonzero(ok & (b0 > t - 20) & (b0 >= 1) & (b0 <= t))
        if len(son):
            g0 = int(b0[son[np.argmax(b0[son])]]); pl = ctx["p_lr"][g0]
            row["o_olay_tepki"] = float(Ol["lr"][g0] - (pl if np.isfinite(pl) else 0.0))
        else:
            row["o_olay_tepki"] = 0.0
        # HAT (yalnız bas..t)
        sv = vdyt_savunma(o, h, l, c, v, Ol["tr"], Ol["atr"], int(bas), int(t), E["savunma"]["ana_taban"], E)
        row.update({f"sv_{k}": float(x) for k, x in sv.items() if k != "seviye"}); row["sv_seviye"] = sv["seviye"]
        if tabanlar:
            for tb, on in (("fitil", "svf"), ("kapanis", "svk")):
                sv2 = vdyt_savunma(o, h, l, c, v, Ol["tr"], Ol["atr"], int(bas), int(t), tb, E)
                row.update({f"{on}_hat_var": sv2["hat_var"], f"{on}_kirilma": sv2["kirilma"], f"{on}_fitil_ihlal": sv2["fitil_ihlal"]})
        # bilgi: getiriler (t+1 açılış -> t+h kapanış, maliyet sonrası), MFE / MAE
        if t + 1 <= n - 1:
            gir = o[t + 1]
            for hh in E["getiri_ufuk"]:
                row[f"r{hh}"] = (c[t + hh] / gir - 1.0 - 2.0 * mal) if t + hh <= n - 1 else np.nan
            mu = int(E["mfe_ufuk"])
            if t + mu <= n - 1:
                row["mfe"] = float(np.max(h[t + 1: t + mu + 1]) / gir - 1.0); row["mae"] = float(np.min(l[t + 1: t + mu + 1]) / gir - 1.0)
        sat.append(row)
    D = pd.DataFrame(sat).merge(KN[["bolge", "yas"] + [f"y{hh}" for hh in E["ufuk"]]], on=["bolge", "yas"], how="left")
    D["yil"] = D.tarih.dt.year; D["ay"] = D.tarih.dt.month; D["yas_kova"] = vdyt_yas_kova(D.yas, E)
    return D


# ---------------------------------------------------------------- 9) MODELLER VE ÖLÇÜTLER
def vdyt_sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))


def vdyt_lojistik(X: np.ndarray, y: np.ndarray, ridge: float = 1.0, tur: int = 25, tol: float = 1e-8) -> np.ndarray:
    """Sırt cezalı lojistik regresyon (Newton / IRLS; ceza sabite uygulanmaz). Döner [sabit, b1, ...]."""
    X1 = np.column_stack([np.ones(len(X)), X]); b = np.zeros(X1.shape[1]); R = np.eye(X1.shape[1]) * ridge; R[0, 0] = 0.0
    for _ in range(int(tur)):
        p = vdyt_sigmoid(X1 @ b); W = p * (1.0 - p)
        Hs = (X1 * W[:, None]).T @ X1 + R; g = X1.T @ (y - p) - R @ b
        try:
            adim = np.linalg.solve(Hs, g)
        except np.linalg.LinAlgError:
            adim = np.linalg.lstsq(Hs, g, rcond=None)[0]
        b = b + adim
        if np.max(np.abs(adim)) < tol:
            break
    return b


def vdyt_standart(Xtr: np.ndarray, Xte: np.ndarray, winsor: Tuple[float, float] = (0.01, 0.99)) -> Tuple[np.ndarray, np.ndarray]:
    """Yalnız eğitim verisinden: uç değer kırpma (yüzdelik), z-ölçek; NaN -> 0 (ortalama). Test aynı parametrelerle dönüştürülür."""
    with np.errstate(all="ignore"):
        lo = np.nanquantile(Xtr, winsor[0], axis=0); hi = np.nanquantile(Xtr, winsor[1], axis=0)
        A = np.clip(Xtr, lo, hi); Bt = np.clip(Xte, lo, hi)
        m = np.nanmean(A, axis=0); sd = np.nanstd(A, axis=0)
    m = np.where(np.isfinite(m), m, 0.0); sd = np.where(np.isfinite(sd) & (sd > 0), sd, 1.0)
    return np.nan_to_num((A - m) / sd), np.nan_to_num((Bt - m) / sd)


def vdyt_temel_tablo(Dtr: pd.DataFrame, Dte: pd.DataFrame, anahtar: List[str], y: str, kucuk: int = 20) -> np.ndarray:
    """Koşulsuz oran tablosu (eğitim sıklığı): tam anahtar hücresi n >= kucuk ise o, değilse sondan bir anahtar düşürülerek, en sonda genel oran."""
    genel = float(Dtr[y].mean()) if len(Dtr) else 0.5; p = np.full(len(Dte), np.nan)
    for k in range(len(anahtar), 0, -1):
        a = anahtar[:k]; G = Dtr.groupby(a)[y].agg(["mean", "size"]); G = G[G["size"] >= kucuk]
        if not len(G):
            continue
        idx = pd.MultiIndex.from_frame(Dte[a]) if len(a) > 1 else pd.Index(Dte[a[0]])
        q = G["mean"].reindex(idx).to_numpy(float); bos = np.isnan(p); p[bos] = q[bos]
    p[np.isnan(p)] = genel
    return np.clip(p, 1e-4, 1 - 1e-4)


def vdyt_wf(D: pd.DataFrame, y: str, son: str, modeller: Dict[str, List[str]], temeller: Dict[str, Any], yillar: List[int],
            E: Optional[Dict[str, Any]] = None, kesik: Optional[str] = None, Dtest: Optional[pd.DataFrame] = None,
            test_son: Optional[str] = None) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """Zaman sıralı walk-forward: her test yılı Y için eğitim = etiketi Y başından ÖNCE tamamlanmış satırlar (son < Y-01-01), test = karar günü Y içinde
    (ve son <= kesik). Modeller yıllık yeniden eğitilir; standartlaştırma yalnız eğitimden. Temeller: tablo anahtar listesi ya da sabit olasılık."""
    E = E or VDYT_ESIK; M = E["model"]; tah, kayit = [], []
    T_ = D if Dtest is None else Dtest; D = D[D[y].notna()]
    if Dtest is None:
        T_ = D
    for Y in yillar:
        b = pd.Timestamp(f"{Y}-01-01"); tr = D[D[son] < b]; te = T_[T_.tarih.dt.year == Y]
        if kesik is not None:
            te = te[te[test_son or son] <= pd.Timestamp(kesik)]
        k_ = {"yil": Y, "egitim": int(len(tr)), "test": int(len(te)), "egitim_son_max": str(tr[son].max()) if len(tr) else None}
        if len(tr) < int(M["min_egitim"]) or not len(te) or tr[y].nunique() < 2:
            k_["durum"] = "atlandı (eğitim yetersiz ya da test boş)"; kayit.append(k_); continue
        P = pd.DataFrame({"satir": te.index, "yil": Y}, index=te.index)
        for ad, kol in modeller.items():
            Xa, Xb = vdyt_standart(tr[kol].to_numpy(float), te[kol].to_numpy(float), tuple(M["winsor"]))
            bta = vdyt_lojistik(Xa, tr[y].to_numpy(float), float(M["ridge"]), int(M["tur"]), float(M["tol"]))
            P[f"p_{ad}"] = np.clip(vdyt_sigmoid(np.column_stack([np.ones(len(Xb)), Xb]) @ bta), 1e-4, 1 - 1e-4)
            P[f"esik90_{ad}"] = float(np.quantile(vdyt_sigmoid(np.column_stack([np.ones(len(Xa)), Xa]) @ bta), 0.9))
        for ad, an in temeller.items():
            P[f"p_{ad}"] = float(an) if isinstance(an, (int, float)) else vdyt_temel_tablo(tr, te, list(an), y, int(E["temel"]["kucuk_hucre"]))
        k_["durum"] = "tamam"; kayit.append(k_); tah.append(P)
    return (pd.concat(tah) if tah else pd.DataFrame()), kayit


def vdyt_brier(y: np.ndarray, p: np.ndarray) -> float:
    return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


def vdyt_logloss(y: np.ndarray, p: np.ndarray) -> float:
    p = np.clip(np.asarray(p, float), 1e-12, 1 - 1e-12); y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def vdyt_dengeli_dogruluk(y: np.ndarray, p: np.ndarray, esik: float = 0.5) -> float:
    y = np.asarray(y, float); k = np.asarray(p, float) >= esik; P, N = (y == 1), (y == 0)
    if not P.any() or not N.any():
        return np.nan
    return 0.5 * (float(np.mean(k[P])) + float(np.mean(~k[N])))


def vdyt_kesinlik_duyarlilik(y: np.ndarray, p: np.ndarray, esik: float) -> Tuple[float, float]:
    y = np.asarray(y, float); k = np.asarray(p, float) >= esik
    kes = float(np.mean(y[k])) if k.any() else np.nan; duy = float(np.mean(k[y == 1])) if (y == 1).any() else np.nan
    return kes, duy


def vdyt_kalibrasyon(y: np.ndarray, p: np.ndarray, kutu: int = 10) -> Tuple[pd.DataFrame, float]:
    y = np.asarray(y, float); p = np.asarray(p, float); b = np.minimum((p * kutu).astype(int), kutu - 1)
    T = pd.DataFrame({"b": b, "y": y, "p": p}).groupby("b").agg(n=("y", "size"), p_ort=("p", "mean"), y_ort=("y", "mean")).reset_index()
    ece = float(np.sum(T.n / max(1, len(y)) * np.abs(T.p_ort - T.y_ort)))
    return T, ece


def vdyt_p_normal(nokta: float, bs: np.ndarray) -> float:
    """İki yanlı p = erfc(|nokta| / (sd_boot x kök 2)) (bootstrap standart hatasıyla normal yaklaşım; 1/B tabanı olmadığı için BH'de güç kaybı yok)."""
    import math
    bs = np.asarray(bs, float); bs = bs[np.isfinite(bs)]
    if len(bs) < 2 or not np.isfinite(nokta):
        return np.nan
    sd = float(np.std(bs, ddof=1))
    if sd <= 0:
        return 0.0 if nokta != 0 else 1.0
    return float(math.erfc(abs(nokta) / (sd * math.sqrt(2.0))))


def _vdyt_bootstrap_agirlik(nk: int, B: int, tohum: int) -> np.ndarray:
    rng = np.random.default_rng(tohum)
    return rng.multinomial(nk, np.full(nk, 1.0 / nk), size=B).astype(np.float64)


def vdyt_bootstrap(kume: Any, y: np.ndarray, p_m: np.ndarray, p_0: np.ndarray, B: int = 2000, tohum: int = 20261112,
                   guven: Tuple[float, float] = (2.5, 97.5), yon: bool = False) -> Dict[str, float]:
    """Küme (hisse) bootstrap: Brier skill = 1 - Σ(p_m - y)² / Σ(p_0 - y)², log loss skill = 1 - LL_m / LL_0, (yon=True ise) dengeli doğruluk farkı
    BA_m - BA_0 (eşik 0,5). Kümeler çekilir (yerine koyarak); her istatistiğin nokta değeri, %95 aralığı ve iki yanlı bootstrap p'si."""
    y = np.asarray(y, float); p_m = np.clip(np.asarray(p_m, float), 1e-12, 1 - 1e-12); p_0 = np.clip(np.asarray(p_0, float), 1e-12, 1 - 1e-12)
    kod, _u = pd.factorize(pd.Series(kume)); nk = int(kod.max()) + 1 if len(kod) else 0
    if nk < 2:
        return {"n": int(len(y)), "kume": nk}
    bc = lambda w: np.bincount(kod, weights=w, minlength=nk)   # noqa: E731
    S = {"bm": bc((p_m - y) ** 2), "b0": bc((p_0 - y) ** 2), "lm": bc(-(y * np.log(p_m) + (1 - y) * np.log(1 - p_m))),
         "l0": bc(-(y * np.log(p_0) + (1 - y) * np.log(1 - p_0)))}
    if yon:
        km, k0 = p_m >= 0.5, p_0 >= 0.5
        S.update({"tpm": bc((km & (y == 1)).astype(float)), "tnm": bc((~km & (y == 0)).astype(float)), "tp0": bc((k0 & (y == 1)).astype(float)),
                  "tn0": bc((~k0 & (y == 0)).astype(float)), "P": bc((y == 1).astype(float)), "N": bc((y == 0).astype(float))})
    W = _vdyt_bootstrap_agirlik(nk, int(B), int(tohum)); bir = np.ones((1, nk))

    def ist(Wm: np.ndarray) -> Dict[str, np.ndarray]:
        T = {k: Wm @ v for k, v in S.items()}
        with np.errstate(invalid="ignore", divide="ignore"):
            o = {"brier_skill": 1 - T["bm"] / T["b0"], "logloss_skill": 1 - T["lm"] / T["l0"]}
            if yon:
                o["ba_fark"] = 0.5 * (T["tpm"] / T["P"] + T["tnm"] / T["N"]) - 0.5 * (T["tp0"] / T["P"] + T["tn0"] / T["N"])
        return o
    nok, bs = ist(bir), ist(W); out: Dict[str, float] = {"n": int(len(y)), "kume": nk, "brier_m": float(S["bm"].sum() / len(y)),
                                                          "brier_0": float(S["b0"].sum() / len(y))}
    for k in nok:
        x = bs[k][np.isfinite(bs[k])]
        out[k] = float(nok[k][0])
        out[k + "_alt"], out[k + "_ust"] = (float(np.percentile(x, guven[0])), float(np.percentile(x, guven[1]))) if len(x) else (np.nan, np.nan)
        out[k + "_p"] = vdyt_p_normal(out[k], x)
    return out


def vdyt_bootstrap_fark(kume: Any, a: np.ndarray, grup: np.ndarray, B: int = 2000, tohum: int = 20261112,
                        guven: Tuple[float, float] = (2.5, 97.5), agirlik: Optional[np.ndarray] = None) -> Dict[str, float]:
    """İki grup ortalaması farkı (grup 1 - grup 0), küme bootstrap. a: ölçü (ör. yukarı = 1), grup: 1 / 0 (diğerleri NaN, atılır)."""
    a = np.asarray(a, float); g = np.asarray(grup, float); w = np.ones(len(a)) if agirlik is None else np.asarray(agirlik, float)
    ok = np.isfinite(a) & np.isfinite(g); a, g, w = a[ok], g[ok], w[ok]; kod, _u = pd.factorize(pd.Series(np.asarray(kume)[ok]))
    nk = int(kod.max()) + 1 if len(kod) else 0
    out: Dict[str, float] = {"n1": int((g == 1).sum()), "n0": int((g == 0).sum()), "kume": nk}
    if nk < 2 or out["n1"] == 0 or out["n0"] == 0:
        out.update({"fark": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}); return out
    bc = lambda v: np.bincount(kod, weights=v, minlength=nk)   # noqa: E731
    s1, n1, s0, n0 = bc(a * w * (g == 1)), bc(w * (g == 1)), bc(a * w * (g == 0)), bc(w * (g == 0))
    W = _vdyt_bootstrap_agirlik(nk, int(B), int(tohum))
    with np.errstate(invalid="ignore", divide="ignore"):
        bs = (W @ s1) / (W @ n1) - (W @ s0) / (W @ n0)
    bs = bs[np.isfinite(bs)]; f = float(s1.sum() / n1.sum() - s0.sum() / n0.sum())
    out.update({"ort1": float(s1.sum() / n1.sum()), "ort0": float(s0.sum() / n0.sum()), "fark": f, "alt": float(np.percentile(bs, guven[0])),
                "ust": float(np.percentile(bs, guven[1])), "p": vdyt_p_normal(f, bs)})
    return out


def vdyt_bh(p: Any, q: float = 0.10) -> np.ndarray:
    """Benjamini-Hochberg: q düzeyinde reddedilen hipotezler (NaN p reddedilmez)."""
    p = np.asarray(p, float); ok = np.isfinite(p); out = np.zeros(len(p), bool); m = int(ok.sum())
    if not m:
        return out
    idx = np.flatnonzero(ok); s = idx[np.argsort(p[idx])]; esik = q * np.arange(1, m + 1) / m
    gec = np.flatnonzero(p[s] <= esik)
    if len(gec):
        out[s[: gec[-1] + 1]] = True
    return out


def vdyt_sureklilik(sure: np.ndarray, tur: np.ndarray, bas_yas: int = 10) -> pd.DataFrame:
    """Süre analizi (bölge başına bir satır): yaş a (bas_yas+1..) için risk altındaki, GENİŞLEME / SÖNME / SANSÜR sayısı, kesikli hazard (GENİŞLEME),
    Kaplan-Meier (GENİŞLEME nedenine özgü; diğerleri sansür), herhangi bitişe göre hayatta kalma ve Aalen-Johansen kümülatif GENİŞLEME olasılığı (CIF)."""
    sure = np.asarray(sure, int); tur = np.asarray(tur, int)
    if not len(sure):
        return pd.DataFrame(columns=["yas", "risk", "gen", "sonme", "sansur", "hazard", "km_gen", "s_hepsi", "cif_gen"])
    yaslar = np.arange(bas_yas + 1, int(sure.max()) + 1); sat = []; km = 1.0; sh = 1.0; cif = 0.0
    for a in yaslar:
        risk = int(np.sum(sure >= a)); g = int(np.sum((sure == a) & (tur == BITIS_GEN))); so = int(np.sum((sure == a) & (tur == BITIS_SONME)))
        sa = int(np.sum((sure == a) & (tur == BITIS_SANSUR)))
        if risk == 0:
            break
        hz = g / risk; cif += sh * hz; km *= (1 - hz); sh *= (1 - (g + so) / risk)
        sat.append((int(a), risk, g, so, sa, hz, km, sh, cif))
    return pd.DataFrame(sat, columns=["yas", "risk", "gen", "sonme", "sansur", "hazard", "km_gen", "s_hepsi", "cif_gen"])


# ---------------------------------------------------------------- 10) HİSSE BAŞINA İŞLEM (geçiş 2): bölgeler, karar noktaları, olay eşleme, havuz
_VDYT_IS: Dict[str, Any] = {}          # çatallanan işçilere bağlam (fork ile kopyalanır; ana süreçte yazılır)


def _vdyt_tohum(*parca: Any) -> int:
    """Süreçten bağımsız, tekrarlanabilir tohum (Python hash() her süreçte değişir; kullanılmaz)."""
    return int(hashlib.sha256("|".join(map(str, parca)).encode("utf-8")).hexdigest()[:8], 16)


def _vdyt_tur_indeks(ix: pd.DatetimeIndex, Ev_s: pd.DataFrame, Ev_m: pd.DataFrame) -> Dict[str, np.ndarray]:
    out = {}
    for tur, g in pd.concat([Ev_s, Ev_m]).groupby("tur"):
        i = vdyt_olay_hizala(ix, g.g0_tarih); out[str(tur)] = np.unique(i[i >= 0])
    return out


def _vdyt_bolge_olay_bayrak(T: pd.DataFrame, ti: Dict[str, np.ndarray], c: np.ndarray, ctx: Dict[str, Any], pazar: str) -> pd.DataFrame:
    """GENİŞLEME bölgelerinin olay bayrakları (genişleme penceresinin ilk günü gb'ye göre) + büyüklük + tabakalama anahtarları (gb - 1 günü)."""
    sp = [k for k in ti if not k.startswith("MAKRO") and VDYT_OLAY_TUR.get(k, {}).get("kat") in ("A", "B")]
    bil = [k for k in ti if k.endswith("_BILANCO")]; rk = [k for k in ti if k.endswith("_RAKIP")]; mk_pl = [k for k in ("MAKRO_FOMC", "MAKRO_PPK") if k in ti]
    mk = [k for k in ti if k.startswith("MAKRO")]; n = len(c)

    def var(turler: List[str], a: int, b: int) -> bool:
        return any(np.any((ti[k] >= a) & (ti[k] <= b)) for k in turler)
    cols = {k: [] for k in ("haberli", "habersiz", "bilanco_once", "bilanco_sonra", "rakip_once", "rakip_yok", "makro_once", "makro_yok", "buyukluk",
                            "mom_g", "liq_g", "yil_g", "rj_tespit")}
    for r in T.itertuples():
        gb = int(r.gen_bas); cols["rj_tespit"].append(ctx["rj_pazar"][int(r.tespit)])
        if r.bit_tur != BITIS_GEN or gb <= 0:
            for k in cols:
                if k != "rj_tespit":
                    cols[k].append(np.nan)
            continue
        h_ = var(sp, gb - 5, gb + 1); hs = (not var(sp, gb - 10, gb + 1)) and (not var(mk, gb - 1, gb))
        cols["haberli"].append(float(h_)); cols["habersiz"].append(float(hs))
        cols["bilanco_once"].append(float(var(bil, gb + 1, gb + 10))); cols["bilanco_sonra"].append(float(var(bil, gb - 10, gb)))
        cols["rakip_once"].append(float(var(rk, gb + 1, gb + 10))); cols["rakip_yok"].append(float(not var(rk, gb - 10, gb + 10)))
        cols["makro_once"].append(float(var(mk_pl, gb + 1, gb + 5))); cols["makro_yok"].append(float(not var(mk_pl, gb - 5, gb + 5)))
        j = int(r.bit) + 5
        cols["buyukluk"].append(float(abs(np.log(c[j] / c[gb - 1]))) if j <= n - 1 else np.nan)
        cols["mom_g"].append(ctx["mom_t"][gb - 1]); cols["liq_g"].append(ctx["liq_t"][gb - 1]); cols["yil_g"].append(float(ctx["gun"][gb - 1].astype("datetime64[Y]").astype(int) + 1970))
    return T.assign(**cols)


def _vdyt_olay_bolge_satir(s: str, d: pd.DataFrame, Ol: Dict[str, np.ndarray], T: pd.DataFrame, ti: Dict[str, np.ndarray], E: Dict[str, Any]) -> pd.DataFrame:
    """Olay-bölge eşleme tablosu (çıktı 3): g0 bölgenin [bas, bit + 20] aralığındaki her (bölge, olay) çifti."""
    sat = []; c = d.c.to_numpy(float); n = len(c); trn = Ol["trn"]; O = E["olay"]; gun = d.index
    for r in T[T.uygun].itertuples():
        for tur, ii in ti.items():
            for g0 in ii[(ii >= r.bas) & (ii <= r.bit + 20)]:
                g0 = int(g0); on = trn[max(r.bas, g0 - O["on_artis_gun"]): g0]; ref = trn[r.bas: max(r.bas, g0 - O["on_artis_gun"])]
                artis = float(np.mean(on) / np.median(ref)) if len(on) and len(ref) >= 3 and np.median(ref) > 0 else np.nan
                gen = r.bit_tur == BITIS_GEN
                sat.append({"sembol": s, "bolge": int(r.Index), "bas_tarih": r.bas_tarih, "yas_olayda": g0 - int(r.bas) + 1, "olay_tarih": gun[g0], "tur": tur,
                            "kat": VDYT_OLAY_TUR.get(tur, {}).get("kat"), "onceden": VDYT_OLAY_TUR.get(tur, {}).get("onceden"),
                            "genisleme_tarih": gun[int(r.bit)] if gen else pd.NaT, "olay_gen_gun": int(r.bit) - g0 if gen else np.nan,
                            "yon_Y1": r.Y1 if gen else np.nan,
                            "buyukluk": float(np.log(c[int(r.bit) + 5] / c[int(r.gen_bas) - 1])) if gen and int(r.bit) + 5 <= n - 1 else np.nan,
                            "on_vol_artis": artis, "on_vol_basladi": float(artis >= float(O["on_artis_esik"])) if np.isfinite(artis) else np.nan,
                            "bit_tur": BITIS_AD[int(r.bit_tur)]})
    return pd.DataFrame(sat)


def _vdyt_pseudo_bolge(trn: np.ndarray, lr: np.ndarray, n: int, sureler: np.ndarray, rng: np.random.Generator, E: Dict[str, Any], k: float, tur: str
                       ) -> np.ndarray:
    """Plasebo P2: gerçek bölge süreleriyle aynı uzunlukta, rastgele başlangıçlı bölgeler (sıkışma şartı yok). Bitiş: tespitten sonra aynı genişleme kuralı
    tetiklenirse GENİŞLEME, tetiklenmezse süre sonunda SÖNME."""
    m = int(E["bolge"]["min_gun"]); w = int(E["genisleme"]["tr_pencere"] if tur == "TR" else E["genisleme"]["rv_pencere"]); out = []
    for L in sureler:
        L = int(L); ust = n - 1 - L - 25
        if ust <= 260:
            continue
        bas = int(rng.integers(260, ust)); tes = bas + m - 1; bit, bt = bas + L - 1, BITIS_SONME
        for i in range(tes + 1, bas + L):
            if vdyt_genisleme_mi(i, bas, trn, lr, k, tur, E):
                bit, bt = i, BITIS_GEN; break
        out.append((bas, tes, bit, bt, bit - w + 1 if bt == BITIS_GEN else -1))
    return np.array(out, dtype=np.int64).reshape(-1, 5)


def _vdyt_hisse_is(s: str) -> Dict[str, Any]:
    """Geçiş 2 (tek hisse): kip 'kapsam' -> yalnız sayım girdileri; kip 'kos' -> bölge tabloları (yön dahil), karar noktaları + özellikler, olay eşleme,
    E1 / E2 havuzu, K6 sözde günleri, P2 plasebo bölgeleri. Hata bu hisseyi atlar ve kaydedilir."""
    X = _VDYT_IS; E = X["E"]; d = X["F"]["S"][s]; pazar = X["pazar"]; kip = X["kip"]
    try:
        Ol = vdyt_olculer(d, E); uy = vdyt_hisse_uygun(s, d, X["Pn"]); n = len(d)
        Ev_s = X["Ev_s"].get(s, X["bos_olay"]); ctx = vdyt_hisse_baglam(s, d, X["Pn"], Ev_s, X["Ev_m"])
        Tt = _vdyt_bolge_tablosu(s, d, Ol, X["kombolar"], uy, E, yon=(kip == "kos"))
        ti = _vdyt_tur_indeks(d.index, Ev_s, X["Ev_m"]); ana = [K["ad"] for K in X["kombolar"] if K["rol"] == "ana"]
        out: Dict[str, Any] = {"sembol": s, "n": n, "bolge": {}, "karar": {}, "olay": {}, "havuz": {}, "hata": None}
        ym = (d.index.year * 100 + d.index.month).to_numpy(np.int32)
        if kip == "kapsam":
            for ad, T in Tt.items():
                out["bolge"][ad] = T[["sembol", "bas_tarih", "tespit_tarih", "sure", "uygun"]]
                if ad in ana:
                    B = T[["bas", "tespit", "bit", "bit_tur", "gen_bas"]].to_numpy(np.int64); KN = vdyt_karar_noktalari(B, n, E)
                    KN = KN[T.uygun.to_numpy(bool)[KN.bolge.to_numpy()]] if len(KN) else KN
                    once = np.array([int(np.sum(np.isin(B[:r_, 3], (BITIS_GEN, BITIS_SONME)))) for r_ in KN.bolge]) if len(KN) else np.zeros(0)
                    out["karar"][ad] = pd.DataFrame({"yas": KN.yas.to_numpy() if len(KN) else [], "yil": d.index[KN.t.to_numpy()].year if len(KN) else [],
                                                     "hs_yeterli": once >= int(E["hisse_gecmis"]["min_bolge"])})
                    sat = []; acik = np.zeros(n, bool)
                    for r in T[T.uygun].itertuples():
                        acik[r.tespit: r.bit] = True
                    for tur, ii in ti.items():
                        bolge_say = sum(bool(np.any((ii >= r.bas) & (ii <= r.bit))) for r in T[T.uygun].itertuples())
                        e2 = int(np.sum(acik[np.clip(ii - 1, 0, n - 1)] & (ii >= 1)))
                        sat.append({"tur": tur, "olay": int(len(ii)), "bolgede_olay_olan_bolge": bolge_say, "e2_uygun_olay": e2})
                    out["olay"][ad] = pd.DataFrame(sat)
            return out
        ks = int(np.searchsorted(d.index, pd.Timestamp(E["wf"]["kasa"][0]))) - 1
        for ad, T in Tt.items():
            T = _vdyt_bolge_olay_bayrak(T, ti, d.c.to_numpy(float), ctx, pazar)
            T["bit_wf"] = np.minimum(T.bit, ks); T["tur_wf"] = np.where(T.bit <= ks, T.bit_tur, BITIS_SANSUR); T["sure_wf"] = T.bit_wf - T.bas + 1
            T["y1_son"] = d.index[np.minimum(T.bit.to_numpy() + int(E["yon"]["Y1_ufuk"]), n - 1)] if len(T) else pd.DatetimeIndex([])
            out["bolge"][ad] = T
            if ad in ana:
                D = vdyt_hisse_karar(s, d, Ol, T, ctx, pazar, E, tabanlar=(ad == E["ana_tanim"]))
                out["karar"][ad] = D
                out["olay"][ad] = _vdyt_olay_bolge_satir(s, d, Ol, T, ti, E)
                acik = np.full(n, -1, np.int32)
                for r in T[T.uygun].itertuples():
                    acik[r.tespit: r.bit] = int(r.Index)
                out["havuz"][ad] = {"acik": acik, "B": T[["bas", "tespit", "bit", "bit_tur"]].to_numpy(np.int64)}
        out["havuz"]["_ortak"] = {"ym": ym, "yil": d.index.year.to_numpy(np.int32), "mom": np.nan_to_num(ctx["mom_t"], nan=-1).astype(np.int8),
                                  "liq": np.nan_to_num(ctx["liq_t"], nan=-1).astype(np.int8), "ti": ti, "gun": d.index}
        # K6: sıkışma DIŞI günler (ana tanım bölgesi açık değil, uygun), sözde yaş = gerçek karar yaşları; aynı genişleme kuralı, ref = sözde bölge
        an = E["ana_tanim"]; Ta = out["bolge"][an]; acik_herhangi = np.zeros(n, bool)
        for r in Ta.itertuples():
            acik_herhangi[r.bas: r.bit + 1] = True
        rng = np.random.default_rng(_vdyt_tohum(s, "K6", E["coklu"]["tohum"]))
        Dk = out["karar"].get(an); k6 = []
        if Dk is not None and len(Dk):
            aday = np.flatnonzero(~acik_herhangi & uy & (np.arange(n) >= 260) & (np.arange(n) <= n - 1 - max(E["ufuk"])))
            K_ = next(K for K in X["kombolar"] if K["ad"] == an)
            for t in rng.choice(aday, size=min(len(aday), 2 * len(Dk)), replace=False) if len(aday) else []:
                a = int(rng.choice(Dk.yas.to_numpy())); bas = int(t) - a + 1
                if bas < 1:
                    continue
                row = {"sembol": s, "t": int(t), "yas": a, "yil": int(d.index[t].year), "natr_d": ctx["natr_d"][t], "mom_t": ctx["mom_t"][t], "liq_t": ctx["liq_t"][t],
                       "tarih": d.index[t], "son20": d.index[min(int(t) + max(E["ufuk"]), n - 1)]}
                for hh in E["ufuk"]:
                    row[f"y{hh}"] = float(any(vdyt_genisleme_mi(i, bas, Ol["trn"], Ol["lr"], K_["k"], K_["tur"], E) for i in range(int(t) + 1, int(t) + hh + 1)))
                k6.append(row)
        out["k6"] = pd.DataFrame(k6)
        # P2: rastgele bölge plasebosu (ana tanım)
        if X.get("p2_tekrar", 0) and an in Tt and len(Ta[Ta.uygun]):
            K_ = next(K for K in X["kombolar"] if K["ad"] == an); p2 = []
            for rep in range(int(X["p2_tekrar"])):
                rg = np.random.default_rng(_vdyt_tohum(s, "P2", rep, E["coklu"]["tohum"]))
                Bp = _vdyt_pseudo_bolge(Ol["trn"], Ol["lr"], n, Ta[Ta.uygun].sure.to_numpy(), rg, E, K_["k"], K_["tur"])
                if not len(Bp):
                    continue
                Tp = pd.DataFrame(Bp, columns=["bas", "tespit", "bit", "bit_tur", "gen_bas"]); Tp["uygun"] = uy[Tp.tespit.to_numpy()]
                Dp = vdyt_hisse_karar(s, d, Ol, Tp, ctx, pazar, E, tabanlar=False)
                if len(Dp):
                    p2.append(Dp.assign(tekrar=rep))
            out["p2"] = pd.concat(p2, ignore_index=True) if p2 else pd.DataFrame()
        return out
    except Exception as ex:   # tek hissenin hatası koşuyu durdurmaz; sayısı ve nedeni meta'ya yazılır
        return {"sembol": s, "hata": f"{type(ex).__name__}: {str(ex)[:200]}", "bolge": {}, "karar": {}, "olay": {}, "havuz": {}}


def vdyt_pazar_isle(pazar: str, kip: str, E: Optional[Dict[str, Any]] = None, isci: int = 2, F: Optional[Dict[str, Any]] = None,
                    Ev: Optional[pd.DataFrame] = None, p2_tekrar: int = 0) -> Dict[str, Any]:
    """Pazarın bütün hisseleri için geçiş 1 (panel) + geçiş 2 (_vdyt_hisse_is). F / Ev verilirse (sentetik test) yükleme atlanır."""
    E = E or VDYT_ESIK; t0 = time.time()
    F = F or vdyt_fiyat_yukle(pazar, E)
    if Ev is None:
        Ev, ev_not = vdyt_olaylar(pazar, F, E)
    else:
        ev_not = {"kaynak": "verilen"}
    Pn = vdyt_panel(pazar, F, E, isci)
    Ev_m = Ev[Ev.sembol == "*"]; Ev_s = {s: g for s, g in Ev[Ev.sembol != "*"].groupby("sembol")}
    _VDYT_IS.clear()
    _VDYT_IS.update({"E": E, "F": F, "pazar": pazar, "kip": kip, "Pn": Pn, "Ev_s": Ev_s, "Ev_m": Ev_m, "bos_olay": Ev.iloc[:0],
                     "kombolar": vdyt_kombolar(pazar, E), "p2_tekrar": p2_tekrar})
    R = _vdyt_harita(_vdyt_hisse_is, sorted(F["S"]), isci)
    hata = {r["sembol"]: r["hata"] for r in R if r.get("hata")}
    if hata:
        vdytlog.warning("%s: %d hissede hata (ilk: %s)", pazar, len(hata), list(hata.items())[:2])
    vdytlog.info("%s %s: %d hisse, %.0f sn", pazar, kip, len(R), time.time() - t0)
    return {"pazar": pazar, "R": [r for r in R if not r.get("hata")], "hata": hata, "Pn": Pn, "Ev": Ev, "ev_not": ev_not, "F": F,
            "kombolar": _VDYT_IS["kombolar"], "sure_sn": round(time.time() - t0, 1)}


# ---------------------------------------------------------------- 11) OLAY ANALİZİ (E1 / E2): olay günündeki yaşa eşlenmiş olaysız kontrollerle
def vdyt_olay_sonuc(B: np.ndarray, r: int, g0: int, n: int, pencere: List[List[int]]) -> int:
    """Açık bölge r için g0'a göre ilk genişlemenin penceresi (bit - g0 ∈ pencere k -> k); pencerelerde genişleme yok -> len(pencere); ölçülemez -> -1.
    Ölçülemez: g0 + en büyük pencere sonu veri dışında, ya da bölge pencere sonundan önce SANSÜR ile bitti."""
    mx = max(b for _a, b in pencere)
    if g0 + mx > n - 1:
        return -1
    bas, _tes, bit, tur = (int(x) for x in B[r][:4]); dd = bit - g0
    if tur == BITIS_GEN:
        for k, (a, b) in enumerate(pencere):
            if a <= dd <= b:
                return k
        return len(pencere)
    if tur == BITIS_SANSUR and dd < mx:
        return -1
    return len(pencere)


_VDYT_HAVUZ: Dict[Any, Any] = {}       # E1 / E2 kontrol havuzu önbelleği (aynı H, tanım ve zaman anahtarı için bir kez kurulur)


def _vdyt_olay_havuz(H: List[Dict[str, Any]], ad: str, makro: bool) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[int, Tuple[int, int]]]:
    """Bütün hisselerde açık bölge günleri: (hisse, gün, yaş, anahtar = zaman x 100 + momentum tertili x 10 + likidite tertili); anahtar ve yaşa göre sıralı."""
    ps, pc, pa, pk = [], [], [], []
    for si, h in enumerate(H):
        if ad not in h["havuz"]:
            continue
        ac = h["havuz"][ad]["acik"]; B = h["havuz"][ad]["B"]; o = h["havuz"]["_ortak"]
        c = np.flatnonzero((ac >= 0) & (o["mom"] >= 0) & (o["liq"] >= 0))
        if not len(c):
            continue
        zaman = (o["yil"][c] if makro else o["ym"][c]).astype(np.int64)
        ps.append(np.full(len(c), si)); pc.append(c); pa.append(c - B[ac[c], 0] + 1); pk.append(zaman * 100 + o["mom"][c] * 10 + o["liq"][c])
    if not ps:
        z = np.zeros(0, np.int64)
        return z, z, z, z, {}
    ps, pc, pa, pk = (np.concatenate(x) for x in (ps, pc, pa, pk))
    srt = np.lexsort((pa, pk)); ps, pc, pa, pk = ps[srt], pc[srt], pa[srt], pk[srt]
    uk, ui = np.unique(pk, return_index=True); ue = np.r_[ui[1:], len(pk)]
    return ps, pc, pa, pk, {int(k): (int(a), int(b)) for k, a, b in zip(uk, ui, ue)}


def vdyt_olay_analizi(H: List[Dict[str, Any]], ad: str, tur: str, kip: str, E: Optional[Dict[str, Any]] = None, olaylar: Optional[Dict[int, np.ndarray]] = None,
                      ust: int = 50000, tohum: Optional[int] = None, donem: Tuple[Optional[str], Optional[str]] = (None, None)) -> Dict[str, Any]:
    """E1 (kip 'e1': koşul günü c = g0 - 21, pencereler -20..+20) / E2 (kip 'e2': c = g0 - 1, pencereler 0..+20). Olay: c gününde açık (tespit edilmiş, bitmemiş)
    bölgesi olan hisse-olay. Gözlenen = ilk genişlemenin penceresi. Beklenen = aynı c ayı (makroda yılı), aynı momentum ve likidite tertili, yaşı +-yas_tol
    olan, ölçülen aralıkta aynı türden olayı olmayan başka bölgelerden en çok kontrol_n kontrolün ortalaması. Fark = gözlenen - beklenen, küme bootstrap
    (hisse; makroda olay günü). H: hisse başına havuz (vdyt_pazar_isle 'kos' çıktısı). olaylar verilirse (plasebo) gerçek olay günleri yerine kullanılır."""
    E = E or VDYT_ESIK; O = E["olay"]; P = O["pencere_e1"] if kip == "e1" else O["pencere_e2"]; off = 21 if kip == "e1" else 1
    mx = max(b for _a, b in P); W = len(P); es = O["esleme"]; makro = tur.startswith("MAKRO")
    d_bas = np.datetime64(pd.Timestamp(donem[0]).date()) if donem[0] else None; d_son = np.datetime64(pd.Timestamp(donem[1]).date()) if donem[1] else None

    def donemde(h: Dict[str, Any], g: int) -> bool:
        gun = h["havuz"]["_ortak"]["gun"]
        if g + mx > len(gun) - 1:
            return False
        a = gun[g].to_datetime64().astype("datetime64[D]"); b = gun[g + mx].to_datetime64().astype("datetime64[D]")
        return (d_bas is None or a >= d_bas) and (d_son is None or b <= d_son)
    rng = np.random.default_rng(tohum if tohum is not None else _vdyt_tohum(ad, tur, kip, es["tohum"]))
    anahtar = (id(H), hash(tuple(h.get("sembol") for h in H)), ad, makro)
    if anahtar in _VDYT_HAVUZ:
        ps, pc, pa, pk, kb = _VDYT_HAVUZ[anahtar]
    else:
        ps, pc, pa, pk, kb = _vdyt_olay_havuz(H, ad, makro)
        _VDYT_HAVUZ.clear(); _VDYT_HAVUZ[anahtar] = (ps, pc, pa, pk, kb)
    if not len(ps):
        return {"tur": tur, "kip": kip, "olay": 0}
    gozlem = []
    for si, h in enumerate(H):
        if ad not in h["havuz"]:
            continue
        ii = (olaylar or {}).get(si) if olaylar is not None else h["havuz"]["_ortak"]["ti"].get(tur)
        if ii is None or not len(ii):
            continue
        for g0 in ii:
            gozlem.append((si, int(g0)))
    toplam = len(gozlem)
    if len(gozlem) > ust:
        sec = rng.choice(len(gozlem), size=ust, replace=False); gozlem = [gozlem[i] for i in np.sort(sec)]
    obs, exp, kume, nk = [], [], [], 0
    for si, g0 in gozlem:
        h = H[si]; ac = h["havuz"][ad]["acik"]; B = h["havuz"][ad]["B"]; o = h["havuz"]["_ortak"]; n = len(ac); c = g0 - off
        if c < 0 or ac[c] < 0 or o["mom"][c] < 0 or o["liq"][c] < 0:
            continue
        r = int(ac[c]); sg = vdyt_olay_sonuc(B, r, g0, n, P)
        if sg < 0 or not donemde(h, g0):
            continue
        yas = c - int(B[r, 0]) + 1; key = int((o["yil"][c] if makro else o["ym"][c])) * 100 + int(o["mom"][c]) * 10 + int(o["liq"][c])
        blok = kb.get(key); kon = []
        if blok:
            a0, b0 = blok; i0 = a0 + int(np.searchsorted(pa[a0:b0], yas - int(es["yas_tol"]), side="left"))
            i1 = a0 + int(np.searchsorted(pa[a0:b0], yas + int(es["yas_tol"]), side="right"))
            if i1 > i0:
                for j in rng.permutation(np.arange(i0, i1))[: int(es["aday_n"])]:
                    sj, cj = int(ps[j]), int(pc[j]); hj = H[sj]; acj = hj["havuz"][ad]["acik"]; rj = int(acj[cj])
                    if sj == si and rj == r:
                        continue
                    gj = cj + off; ev = hj["havuz"]["_ortak"]["ti"].get(tur, np.zeros(0, np.int64)) if olaylar is None else (olaylar.get(sj) if olaylar.get(sj) is not None else np.zeros(0, np.int64))
                    if (len(ev) and np.any((ev >= cj + 1) & (ev <= gj + mx))) or not donemde(hj, gj):
                        continue
                    sj_ = vdyt_olay_sonuc(hj["havuz"][ad]["B"], rj, gj, len(acj), P)
                    if sj_ < 0:
                        continue
                    kon.append(sj_)
                    if len(kon) >= int(es["kontrol_n"]):
                        break
        if not kon:
            nk += 1; continue
        ob = np.zeros(W + 1); ob[sg] = 1.0; ex = np.bincount(kon, minlength=W + 1)[: W + 1] / len(kon)
        obs.append(ob); exp.append(ex); kume.append(str(h["havuz"]["_ortak"]["gun"][g0].date()) if makro else h["sembol"])
    out: Dict[str, Any] = {"tur": tur, "kip": kip, "olay_toplam": toplam, "olay_kullanilan": len(obs), "kontrolsuz": nk,
                           "pencere": [f"[{a},{b}]" for a, b in P] + ["yok"]}
    if len(obs) < 2:
        return out
    ob, ex = np.array(obs), np.array(exp); fark = ob - ex
    B_ = int(E["basari"]["bootstrap"]); g = tuple(E["basari"]["guven"])
    kod, _u = pd.factorize(pd.Series(kume)); nkm = int(kod.max()) + 1
    Wt = _vdyt_bootstrap_agirlik(nkm, B_, _vdyt_tohum(ad, tur, kip, "bs")) if nkm >= 2 else None
    satir = []
    for k in range(W + 1):
        s_f = np.bincount(kod, weights=fark[:, k], minlength=nkm); s_n = np.bincount(kod, minlength=nkm).astype(float)
        f_ = float(fark[:, k].mean()); alt = ust_ = pval = np.nan
        if Wt is not None:
            bs = (Wt @ s_f) / (Wt @ s_n); bs = bs[np.isfinite(bs)]
            alt, ust_ = float(np.percentile(bs, g[0])), float(np.percentile(bs, g[1]))
            pval = vdyt_p_normal(f_, bs)
        satir.append({"pencere": out["pencere"][k], "gozlenen": float(ob[:, k].mean()), "beklenen": float(ex[:, k].mean()), "fark": f_, "alt": alt,
                      "ust": ust_, "p": pval, "oran": float(ob[:, k].mean() / ex[:, k].mean()) if ex[:, k].mean() > 0 else np.nan})
    out["tablo"] = satir; out["kume"] = nkm
    return out


def vdyt_tabakali_agirlik(grup: np.ndarray, tabaka: pd.DataFrame) -> np.ndarray:
    """Grup 0 birimlerini grup 1'in tabaka dağılımına göre yeniden ağırlıklar (tabaka içinde ağırlık = n1 / n0); tek grubu olan tabaka ve NaN grup 0 ağırlık."""
    g = np.asarray(grup, float); w = np.zeros(len(g)); ok = np.isfinite(g)
    if not ok.any():
        return w
    k = tabaka.reset_index(drop=True).groupby(list(tabaka.columns), sort=False, dropna=False).ngroup().to_numpy(); m = int(k.max()) + 1
    n1 = np.bincount(k[ok], weights=(g[ok] == 1).astype(float), minlength=m); n0 = np.bincount(k[ok], weights=(g[ok] == 0).astype(float), minlength=m)
    iki = (n1 > 0) & (n0 > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        w[ok] = np.where(iki[k[ok]], np.where(g[ok] == 1, 1.0, n1[k[ok]] / n0[k[ok]]), 0.0)
    return w


# ---------------------------------------------------------------- 12) PAZAR ANALİZİ (Faz 2; yalnız `kos` çağırır)
def _vdyt_donem(asama: str, E: Dict[str, Any]) -> Tuple[Optional[str], str, List[int]]:
    if asama == "wf":
        return None, str((pd.Timestamp(E["wf"]["kasa"][0]) - pd.Timedelta(days=1)).date()), list(E["wf"]["kesif_yillar"])
    if asama == "kasa":
        return E["wf"]["kasa"][0], E["wf"]["kasa"][1], list(E["wf"]["kasa_yillar"])
    raise VdytHata(f"bilinmeyen aşama: {asama}")


def _vdyt_bs_oran(kume: Any, lm: np.ndarray, l0: np.ndarray, B: int, tohum: int, guven: Tuple[float, float]) -> Dict[str, float]:
    kod, _u = pd.factorize(pd.Series(kume)); nk = int(kod.max()) + 1 if len(kod) else 0
    if nk < 2:
        return {"skill": np.nan, "alt": np.nan, "ust": np.nan, "p": np.nan}
    sm, s0 = np.bincount(kod, weights=lm, minlength=nk), np.bincount(kod, weights=l0, minlength=nk); W = _vdyt_bootstrap_agirlik(nk, B, tohum)
    bs = 1 - (W @ sm) / (W @ s0); bs = bs[np.isfinite(bs)]
    return {"skill": float(1 - sm.sum() / s0.sum()), "alt": float(np.percentile(bs, guven[0])), "ust": float(np.percentile(bs, guven[1])),
            "p": vdyt_p_normal(float(1 - sm.sum() / s0.sum()), bs)}


def _vdyt_degerlendir(P: pd.DataFrame, D: pd.DataFrame, y: str, m: str, t0: str, E: Dict[str, Any], yon: bool = False, alt: Optional[np.ndarray] = None
                      ) -> Dict[str, Any]:
    """Tahmin tablosu P (satir, p_*) üzerinde model m'nin temel t0'a göre ölçütleri (küme = hisse)."""
    if not len(P) or f"p_{m}" not in P or f"p_{t0}" not in P:
        return {"model": m, "temel": t0, "n": 0}
    Q = P if alt is None else P[alt]
    yy = D.loc[Q.satir, y].to_numpy(float); ok = np.isfinite(yy); Q = Q[ok]; yy = yy[ok]
    if len(Q) < 30 or len(np.unique(yy)) < 2:
        return {"model": m, "temel": t0, "n": int(len(Q))}
    pm, p0 = Q[f"p_{m}"].to_numpy(float), Q[f"p_{t0}"].to_numpy(float); kume = D.loc[Q.satir, "sembol"].to_numpy()
    b = vdyt_bootstrap(kume, yy, pm, p0, int(E["basari"]["bootstrap"]), int(E["basari"]["tohum"]), tuple(E["basari"]["guven"]), yon=yon)
    _cal, ece = vdyt_kalibrasyon(yy, pm)
    out = {"model": m, "temel": t0, **b, "ece": ece, "y_ort": float(yy.mean()), "p_ort": float(pm.mean()), "logloss_m": vdyt_logloss(yy, pm),
           "logloss_0": vdyt_logloss(yy, p0)}
    if yon:
        out["ba_m"] = vdyt_dengeli_dogruluk(yy, pm); out["ba_0"] = vdyt_dengeli_dogruluk(yy, p0)
    else:
        e90 = Q[f"esik90_{m}"].to_numpy(float) if f"esik90_{m}" in Q else np.full(len(Q), np.nan)
        k_ = pm >= e90; out["kesinlik_ust10"] = float(yy[k_].mean()) if k_.any() else np.nan
        out["duyarlilik_ust10"] = float(k_[yy == 1].mean()) if (yy == 1).any() else np.nan
        out["kesinlik_05"], out["duyarlilik_05"] = vdyt_kesinlik_duyarlilik(yy, pm, 0.5)
    return out


def vdyt_analiz(Z: Dict[str, Any], asama: str, E: Optional[Dict[str, Any]] = None, ara: Optional[str] = None, p1_tekrar: Optional[int] = None) -> Dict[str, Any]:
    """Bir pazarın Faz 2 analizi (aşama 'wf' = 2023 sonuna kadar veri, test yılları kesif_yillar; 'kasa' = 2024-01 -> kesik, test yılları kasa_yillar).
    Döner: özet tablolar (dict of DataFrame) + hipotez satırları; büyük tablolar ara klasöre yazılır."""
    _VDYT_HAVUZ.clear()
    E = E or VDYT_ESIK; pazar = Z["pazar"]; R = Z["R"]; K = Z["kombolar"]; ana = [k["ad"] for k in K if k["rol"] == "ana"]
    an = E["ana_tanim"] if E["ana_tanim"] in ana else ana[0]; bas, son, yillar = _vdyt_donem(asama, E); ts = pd.Timestamp(son)
    tb = pd.Timestamp(bas) if bas else None; Bb = int(E["basari"]["bootstrap"]); tohum = int(E["basari"]["tohum"]); gv = tuple(E["basari"]["guven"])
    ara = ara or os.path.join(VDYT_YOL["ara"], asama); os.makedirs(ara, exist_ok=True); out: Dict[str, Any] = {"pazar": pazar, "asama": asama}
    hip: List[Dict[str, Any]] = []
    Rb = {k["ad"]: pd.concat([h["bolge"][k["ad"]] for h in R if k["ad"] in h["bolge"]], ignore_index=True) for k in K}
    for ad, T in Rb.items():
        T.assign(kombo=ad).to_csv(os.path.join(ara, f"bolge_{pazar}_{ad}.csv.gz"), index=False)
    # --- süre analizi
    sure_ozet = []
    for ad, T in Rb.items():
        T = T[T.uygun]
        if asama == "wf":
            T = T[T.tespit_tarih < pd.Timestamp(E["wf"]["kasa"][0])]; su, tu = T.sure_wf.to_numpy(), T.tur_wf.to_numpy()
        else:
            T = T[T.tespit_tarih >= tb]; su, tu = T.sure.to_numpy(), T.bit_tur.to_numpy()
        S = vdyt_sureklilik(su, tu); S.to_csv(os.path.join(ara, f"sure_{pazar}_{ad}.csv"), index=False)
        row = {"kombo": ad, "bolge": int(len(T)), "medyan_sure": float(S.yas[S.s_hepsi <= 0.5].min()) if (S.s_hepsi <= 0.5).any() else np.nan}
        for a in (20, 40, 60, 90, 120):
            row[f"cif_gen_{a}"] = float(S.cif_gen[S.yas <= a].iloc[-1]) if (S.yas <= a).any() else np.nan
        kv = vdyt_yas_kova(S.yas)
        for i, (a, b) in enumerate(E["yas_kova"]):
            m_ = kv == i; row[f"hazard_{a}_{b}"] = float(S.gen[m_].sum() / S.risk[m_].sum()) if S.risk[m_].sum() > 0 else np.nan
        rt = np.digitize(T.rj_tespit.to_numpy(float), E["rejim"]["tertil"])
        for k_ in range(3):
            Sk = vdyt_sureklilik(su[(rt == k_) & np.isfinite(T.rj_tespit.to_numpy(float))], tu[(rt == k_) & np.isfinite(T.rj_tespit.to_numpy(float))])
            row[f"hazard_rejim{k_}"] = float(Sk.gen.sum() / Sk.risk.sum()) if len(Sk) and Sk.risk.sum() > 0 else np.nan
        sure_ozet.append(row)
    out["sure"] = pd.DataFrame(sure_ozet)
    # --- karar noktaları
    D = {ad: (pd.concat([h["karar"][ad] for h in R if ad in h["karar"] and len(h["karar"][ad])], ignore_index=True)
              if any(ad in h["karar"] and len(h["karar"][ad]) for h in R) else pd.DataFrame()) for ad in ana}
    for ad in ana:
        if len(D[ad]):
            D[ad]["pazar_yon"] = (D[ad].p_pazar_ret60.fillna(0) >= 0).astype(int)
            D[ad]["yukari"] = np.where(D[ad].Y1 == 1, 1.0, np.where(D[ad].Y1 == -1, 0.0, np.nan))
    if len(D.get(an, [])):
        ince = [c for c in ("sembol", "bolge", "yas", "t", "tarih", "bit", "gen_bas", "y10", "y20", "Y1", "y1_son", "sv_hat_var", "sv_seviye", "sv_kirilma") if c in D[an]]
        D[an][ince].rename_axis("satir").reset_index().to_csv(os.path.join(ara, f"karar_{pazar}_{an}.csv.gz"), index=False)
    gr = lambda gs: [c for g in gs for c in VDYT_OZELLIK[g]]   # noqa: E731
    m1_sat, m2_sat, tahm1 = [], [], {}
    for ad in ana:
        Dd = D[ad]
        if not len(Dd):
            continue
        for hh in E["ufuk"]:
            mod = {m: gr(g) for m, g in VDYT_SURE_MODEL.items()}
            if ad == an and hh == int(E["ana_ufuk"]):
                mod.update({f"M_EKSI_{g}": gr([x for x in VDYT_OZELLIK if x != g]) for g in VDYT_OZELLIK})
            P, kay = vdyt_wf(Dd, f"y{hh}", f"son{hh}", mod, {"T0": E["temel"]["G_T0"], "T1": E["temel"]["G_T1"]}, yillar, E, kesik=son)
            if not len(P):
                continue
            tahm1[(ad, hh)] = P
            P.assign(sembol=Dd.loc[P.satir, "sembol"].values, tarih=Dd.loc[P.satir, "tarih"].values, y=Dd.loc[P.satir, f"y{hh}"].values).to_csv(
                os.path.join(ara, f"tahmin_m1_{pazar}_{ad}_y{hh}.csv.gz"), index=False)
            for m in VDYT_SURE_MODEL:
                for t0 in (("T1", "T0") if m != "M_TAM" else ("T1",)):
                    r = _vdyt_degerlendir(P, Dd, f"y{hh}", m, t0, E); r.update({"kombo": ad, "ufuk": hh, "yillar": kay}); m1_sat.append(r)
                    hip.append({"aile": "F1_MOTOR1" if m == "M_TAM" else "F5_SURE", "id": f"M1-{pazar}-{ad}-y{hh}-{m}-vs-{t0}",
                                "nokta": r.get("brier_skill"), "alt": r.get("brier_skill_alt"), "ust": r.get("brier_skill_ust"), "p": r.get("brier_skill_p"),
                                "ana": bool(ad == an and hh == int(E["ana_ufuk"]) and m == "M_TAM" and t0 == "T1")})
            if ad == an and hh == int(E["ana_ufuk"]):
                for g in VDYT_OZELLIK:
                    r = _vdyt_degerlendir(P, Dd, f"y{hh}", "M_TAM", f"M_EKSI_{g}", E); r.update({"kombo": ad, "ufuk": hh, "katki": g}); m1_sat.append(r)
                    hip.append({"aile": "F6_KATKI", "id": f"M1-{pazar}-{ad}-katki-{g}", "nokta": r.get("brier_skill"), "alt": r.get("brier_skill_alt"),
                                "ust": r.get("brier_skill_ust"), "p": r.get("brier_skill_p"), "ana": False})
        # --- Motor 2 (yön), yalnız 20 gün içinde genişleyen ve yönü çözülen karar noktaları
        D2 = Dd[(Dd.y20 == 1) & Dd.yukari.notna()]
        mod2 = {"M_TAM": gr(list(VDYT_OZELLIK))}
        if ad == an:
            mod2.update({f"M_EKSI_{g}": gr([x for x in VDYT_OZELLIK if x != g]) for g in VDYT_OZELLIK})
        P2, kay2 = vdyt_wf(D2, "yukari", "y1_son", mod2, {"B0": E["temel"]["Y_B0"], "B1": ["pazar_yon"]}, yillar, E, kesik=son)
        if len(P2):
            P2.assign(sembol=D2.loc[P2.satir, "sembol"].values, y=D2.loc[P2.satir, "yukari"].values).to_csv(os.path.join(ara, f"tahmin_m2_{pazar}_{ad}.csv.gz"), index=False)
            for t0 in ("B1", "B0"):
                r = _vdyt_degerlendir(P2, D2, "yukari", "M_TAM", t0, E, yon=True); r.update({"kombo": ad, "yillar": kay2}); m2_sat.append(r)
                hip.append({"aile": "F1_MOTOR2", "id": f"M2-{pazar}-{ad}-M_TAM-vs-{t0}", "nokta": r.get("brier_skill"), "alt": r.get("brier_skill_alt"),
                            "ust": r.get("brier_skill_ust"), "p": r.get("brier_skill_p"), "ana": bool(ad == an and t0 == "B1")})
            if ad == an:
                hz = (D2.loc[P2.satir, "sv_hat_var"] == 0).to_numpy()
                r = _vdyt_degerlendir(P2, D2, "yukari", "M_TAM", "B1", E, yon=True, alt=hz); r.update({"kombo": ad, "hipotez": "H4 (hatsız alt küme)"})
                m2_sat.append(r)
                hip.append({"aile": "F3_HAT", "id": f"H4-{pazar}-{ad}", "nokta": r.get("ba_fark"), "alt": r.get("ba_fark_alt"), "ust": r.get("ba_fark_ust"),
                            "p": r.get("ba_fark_p"), "ana": False})
                for g in VDYT_OZELLIK:
                    r = _vdyt_degerlendir(P2, D2, "yukari", "M_TAM", f"M_EKSI_{g}", E, yon=True); r.update({"kombo": ad, "katki": g}); m2_sat.append(r)
                    if g == "HAT":
                        hip.append({"aile": "F3_HAT", "id": f"H5-{pazar}-{ad}", "nokta": r.get("brier_skill"), "alt": r.get("brier_skill_alt"),
                                    "ust": r.get("brier_skill_ust"), "p": r.get("brier_skill_p"), "ana": False})
        # --- birleşik (bilgi): yukarı-genişleme / aşağı-genişleme / diğer, 20 gün
        if ad == an and (ad, 20) in tahm1 and len(D2):
            Dall = Dd[Dd.y20.notna() & ((Dd.y20 == 0) | (Dd.Y1.notna() & (Dd.y1_son <= ts)))]
            P3, _k = vdyt_wf(D2, "yukari", "y1_son", {"M_TAM": gr(list(VDYT_OZELLIK))}, {"B1": ["pazar_yon"]}, yillar, E, kesik=son, Dtest=Dall, test_son="son20")
            P1 = tahm1[(ad, 20)].set_index("satir")
            if len(P3):
                P3 = P3.set_index("satir").join(P1[["p_M_TAM", "p_T1"]].rename(columns={"p_M_TAM": "g_m", "p_T1": "g_0"}), how="inner")
                yy = Dd.loc[P3.index]; yu = ((yy.y20 == 1) & (yy.Y1 == 1)).astype(float).to_numpy(); ya = ((yy.y20 == 1) & (yy.Y1 == -1)).astype(float).to_numpy()
                yd = 1 - yu - ya

                def br(g: np.ndarray, u: np.ndarray) -> np.ndarray:
                    return (g * u - yu) ** 2 + (g * (1 - u) - ya) ** 2 + ((1 - g) - yd) ** 2
                lm, l0 = br(P3.g_m.to_numpy(), P3.p_M_TAM.to_numpy()), br(P3.g_0.to_numpy(), P3.p_B1.to_numpy())
                out["birlesik"] = {"kombo": ad, "n": int(len(P3)), **_vdyt_bs_oran(yy.sembol.to_numpy(), lm, l0, Bb, tohum, gv)}
                # bilgi: basit portföy kuralı (yüksek genişleme olasılığı x yukarı olasılığı >= 0,5), 20 gün tut, 10 yuva, maliyet sonrası
                Q = P3.assign(tarih=yy.tarih.values, r20=yy.r20.values, sembol=yy.sembol.values)
                Q = Q[(Q.g_m >= tahm1[(ad, 20)].set_index("satir").loc[Q.index, "esik90_M_TAM"]) & (Q.p_M_TAM >= 0.5) & Q.r20.notna()].sort_values("tarih")
                out["portfoy"] = vdyt_portfoy(Q, E)
        # --- savunma hattı hipotezleri (H1-H3) ve bölge karşılaştırmaları (K1-K5), K6
        son_dp = Dd.sort_values("yas").groupby(["sembol", "bolge"]).tail(1)
        son_dp = son_dp[son_dp.Y1.isin([1, -1])]
        son_dp = son_dp[(son_dp.y1_son <= ts) & ((son_dp.tarih >= tb) if tb is not None else True)]
        yuk = (son_dp.Y1 == 1).astype(float).to_numpy(); kume = son_dp.sembol.to_numpy()
        for on, adb in (("sv", "govde"), ("svf", "fitil"), ("svk", "kapanis")):
            if f"{on}_hat_var" not in son_dp:
                continue
            hv, kr, fi = (son_dp[f"{on}_{k}"].to_numpy(float) for k in ("hat_var", "kirilma", "fitil_ihlal"))
            for hid, g1, g0, beklenen in (("H1", (hv == 1) & (kr == 0), hv == 0, "+"), ("H2", (hv == 1) & (kr == 1), (hv == 1) & (kr == 0), "-"),
                                          ("H3", (hv == 1) & (kr == 0) & (fi >= 1), (hv == 1) & (kr == 1), "+")):
                g = np.where(g1, 1.0, np.where(g0, 0.0, np.nan)); r = vdyt_bootstrap_fark(kume, yuk, g, Bb, tohum, gv)
                hip.append({"aile": "F3_HAT", "id": f"{hid}-{pazar}-{ad}-{adb}", "nokta": r.get("fark"), "alt": r.get("alt"), "ust": r.get("ust"), "p": r.get("p"),
                            "beklenen_isaret": beklenen, "n1": r.get("n1"), "n0": r.get("n0"), "ana": False})
        Tg = Rb[ad]; Tg = Tg[Tg.uygun & (Tg.bit_tur == BITIS_GEN) & Tg.Y1.isin([1, -1]) & (Tg.y1_son <= ts)]
        if tb is not None:
            Tg = Tg[Tg.bit_tarih >= tb]
        for kid, g1, g0 in (("K1", "haberli", "habersiz"), ("K2", "bilanco_once", "bilanco_sonra"), ("K3", "rakip_once", "rakip_yok"),
                            ("K4", "makro_once", "makro_yok")):
            g = np.where(Tg[g1] == 1, 1.0, np.where(Tg[g0] == 1, 0.0, np.nan))
            if kid == "K2":
                g = np.where((Tg[g1] == 1) & (Tg[g0] == 1), np.nan, g)
            w = vdyt_tabakali_agirlik(g, Tg[["yil_g", "mom_g", "liq_g"]].fillna(-1))
            for olc in ("yukari", "buyukluk"):
                a = (Tg.Y1 == 1).astype(float).to_numpy() if olc == "yukari" else Tg.buyukluk.to_numpy(float)
                r = vdyt_bootstrap_fark(Tg.sembol.to_numpy(), a, np.where(w > 0, g, np.nan), Bb, tohum, gv, agirlik=w)
                hip.append({"aile": "F4_KARSILASTIRMA", "id": f"{kid}-{pazar}-{ad}-{olc}", "nokta": r.get("fark"), "alt": r.get("alt"), "ust": r.get("ust"),
                            "p": r.get("p"), "n1": r.get("n1"), "n0": r.get("n0"), "ana": False})
        g5 = np.where(son_dp.sv_hat_var == 1, 1.0, 0.0); w5 = vdyt_tabakali_agirlik(g5, son_dp[["yil", "mom_t", "liq_t"]].fillna(-1))
        r = vdyt_bootstrap_fark(kume, yuk, np.where(w5 > 0, g5, np.nan), Bb, tohum, gv, agirlik=w5)
        hip.append({"aile": "F4_KARSILASTIRMA", "id": f"K5-{pazar}-{ad}-yukari", "nokta": r.get("fark"), "alt": r.get("alt"), "ust": r.get("ust"), "p": r.get("p"),
                    "n1": r.get("n1"), "n0": r.get("n0"), "ana": False})
        if ad == an:
            K6 = pd.concat([h["k6"] for h in R if isinstance(h.get("k6"), pd.DataFrame) and len(h["k6"])], ignore_index=True) if any(
                isinstance(h.get("k6"), pd.DataFrame) and len(h["k6"]) for h in R) else pd.DataFrame()
            hh = int(E["ana_ufuk"]); Dr = Dd[Dd[f"y{hh}"].notna() & (Dd.son20 <= ts)]
            if tb is not None:
                Dr = Dr[Dr.tarih >= tb]
            if len(K6):
                K6 = K6[(K6.son20 <= ts) & ((K6.tarih >= tb) if tb is not None else True)]
                U = pd.concat([Dr[["sembol", "yil", "natr_d", "mom_t", "liq_t", f"y{hh}"]].assign(g=1.0),
                               K6[["sembol", "yil", "natr_d", "mom_t", "liq_t", f"y{hh}"]].assign(g=0.0)], ignore_index=True)
                w6 = vdyt_tabakali_agirlik(U.g.to_numpy(), U[["yil", "natr_d", "mom_t", "liq_t"]].fillna(-1))
                r = vdyt_bootstrap_fark(U.sembol.to_numpy(), U[f"y{hh}"].to_numpy(float), np.where(w6 > 0, U.g, np.nan), Bb, tohum, gv, agirlik=w6)
                hip.append({"aile": "F4_KARSILASTIRMA", "id": f"K6-{pazar}-{ad}-y{hh}", "nokta": r.get("fark"), "alt": r.get("alt"), "ust": r.get("ust"),
                            "p": r.get("p"), "n1": r.get("n1"), "n0": r.get("n0"), "ana": False})
    out["motor1"] = pd.DataFrame(m1_sat); out["motor2"] = pd.DataFrame(m2_sat)
    # --- olay analizleri (E1, E2), bütün ana tanımlar ve olay türleri
    ol = []; turler = sorted({t for h in R for t in h["havuz"].get("_ortak", {}).get("ti", {})})
    for ad in ana:
        for tur in turler:
            for kip in ("e1", "e2"):
                r = vdyt_olay_analizi(R, ad, tur, kip, E, donem=(bas, son))
                for x in r.get("tablo", []):
                    ol.append({"kombo": ad, "tur": tur, "kip": kip, "olay_toplam": r["olay_toplam"], "olay_kullanilan": r["olay_kullanilan"],
                               "kontrolsuz": r["kontrolsuz"], **x})
                    if x["pencere"] != "yok":
                        hip.append({"aile": "F2_OLAY", "id": f"{kip.upper()}-{pazar}-{ad}-{tur}-{x['pencere']}", "nokta": x["fark"], "alt": x["alt"], "ust": x["ust"],
                                    "p": x["p"], "ana": False})
    out["olay"] = pd.DataFrame(ol)
    pd.concat([h["olay"][an] for h in R if an in h["olay"] and len(h["olay"][an])], ignore_index=True).to_csv(
        os.path.join(ara, f"olay_eslesme_{pazar}_{an}.csv.gz"), index=False) if any(an in h["olay"] and len(h["olay"][an]) for h in R) else None
    # --- plasebo P1 (rastgele olay günleri), yalnız wf aşamasında
    if asama == "wf":
        out["plasebo_olay"] = vdyt_plasebo_olay(R, an, [t for t in turler if not t.startswith("MAKRO")], E, (bas, son), p1_tekrar)
        P2r = pd.concat([h["p2"] for h in R if isinstance(h.get("p2"), pd.DataFrame) and len(h["p2"])], ignore_index=True) if any(
            isinstance(h.get("p2"), pd.DataFrame) and len(h["p2"]) for h in R) else pd.DataFrame()
        sat = []
        for rep, Dp in (P2r.groupby("tekrar") if len(P2r) else []):
            hh = int(E["ana_ufuk"]); Dp = Dp.reset_index(drop=True)
            Pp, _k = vdyt_wf(Dp, f"y{hh}", f"son{hh}", {"M_TAM": gr(list(VDYT_OZELLIK))}, {"T1": E["temel"]["G_T1"]}, yillar, E, kesik=son)
            r = _vdyt_degerlendir(Pp, Dp, f"y{hh}", "M_TAM", "T1", E); r["tekrar"] = int(rep); sat.append(r)
        out["plasebo_bolge"] = pd.DataFrame(sat)
    H = pd.DataFrame(hip)
    if len(H):
        H["bh_ret"] = False
        for a, g in H.groupby("aile"):
            H.loc[g.index, "bh_ret"] = vdyt_bh(g.p.to_numpy(float), float(E["coklu"]["bh_q"]))
    out["hipotez"] = H
    return out


def vdyt_plasebo_olay(R: List[Dict[str, Any]], ad: str, turler: List[str], E: Dict[str, Any], donem: Tuple[Optional[str], Optional[str]],
                      tekrar: Optional[int] = None) -> pd.DataFrame:
    """Plasebo P1: her hissede gerçek olay sayısı kadar rastgele 'olay' günü (tekdüze; 260. gün ile n-22 arası), E2 aynı yöntemle; her tekrarda bütün
    tür x pencere p'lerine BH (q); keşif sayısı. Tür başına en çok 3.000 olay."""
    tekrar = int(tekrar if tekrar is not None else E["coklu"]["plasebo_olay_tekrar"]); sat = []
    for rep in range(tekrar):
        ps = []
        for tur in turler:
            ol = {}
            for si, h in enumerate(R):
                ii = h["havuz"].get("_ortak", {}).get("ti", {}).get(tur)
                if ii is None or not len(ii) or ad not in h["havuz"]:
                    continue
                n = len(h["havuz"][ad]["acik"])
                if n - 22 <= 260:
                    continue
                rg = np.random.default_rng(_vdyt_tohum(h["sembol"], tur, rep, E["coklu"]["tohum"]))
                ol[si] = np.unique(rg.integers(260, n - 22, size=len(ii)))
            r = vdyt_olay_analizi(R, ad, tur, "e2", E, olaylar=ol, ust=3000, tohum=_vdyt_tohum(tur, rep, "P1"), donem=donem)
            ps += [x["p"] for x in r.get("tablo", []) if x["pencere"] != "yok"]
        ret = vdyt_bh(np.array(ps, float), float(E["coklu"]["bh_q"]))
        sat.append({"tekrar": rep, "test": int(np.isfinite(np.array(ps, float)).sum()), "kesif": int(ret.sum()),
                    "ham_p_lt_005": int(np.sum(np.array(ps, float) < 0.05))})
    return pd.DataFrame(sat)


def vdyt_portfoy(Q: pd.DataFrame, E: Dict[str, Any]) -> Dict[str, Any]:
    """Bilgi amaçlı yuva simülasyonu: tarih sırasıyla aday (olasılık çarpımına göre), en çok 'yuva' açık pozisyon, her biri 'tut' gün (r20 maliyet sonrası),
    sermayenin 1/yuva'sı. Döner: işlem sayısı, ortalama ve medyan r20, isabet (r20 > 0), toplam (bileşiksiz), en büyük düşüş (çıkış sırasıyla birikimli)."""
    Y = int(E["portfoy"]["yuva"]); tut = int(E["portfoy"]["tut"]); acik: List[pd.Timestamp] = []; isl = []
    if not len(Q):
        return {"islem": 0}
    Q = Q.assign(skor=Q.g_m * Q.p_M_TAM).sort_values(["tarih", "skor"], ascending=[True, False])
    for t, g in Q.groupby("tarih"):
        acik = [x for x in acik if x > t]
        for r in g.itertuples():
            if len(acik) >= Y:
                break
            cik = t + pd.tseries.offsets.BDay(tut); acik.append(cik); isl.append((cik, float(r.r20)))
    if not isl:
        return {"islem": 0}
    I = pd.DataFrame(isl, columns=["cikis", "r"]).sort_values("cikis"); kum = (I.r / Y).cumsum()
    return {"islem": int(len(I)), "ort_r20": float(I.r.mean()), "medyan_r20": float(I.r.median()), "isabet": float((I.r > 0).mean()),
            "toplam_bilesiksiz": float(kum.iloc[-1]), "en_buyuk_dusus": float((kum - kum.cummax()).min()), "rol": "yalnız bilgi"}


# ---------------------------------------------------------------- 13) VERİ SHA256, PARAMETRE KAYDI
def vdyt_veri_sha() -> Dict[str, Tuple[str, int]]:
    """Koşunun okuduğu bütün veri kaynaklarının sha256'sı (dosya ya da klasör özeti) ve dosya sayısı; yoksa ('YOK', 0)."""
    Y = VDYT_YOL; out: Dict[str, Tuple[str, int]] = {}
    for ad, yol in (("V_BIST.pkl", Y["v_bist"]), ("liste_abd.csv.gz", os.path.join(Y["pead"], "liste_abd.csv.gz")), ("G.pkl", Y["fon_G"]),
                    ("company_tickers.json", Y["ticker"]), ("k35_sic.csv", Y["sic"]), ("surucu.pkl", Y["surucu"]), ("sektor_BIST.csv", Y["sektor_bist"]),
                    ("vdyt_makro_takvim.json", Y["makro"])):
        out[ad] = (vdyt_sha_dosya(yol), 1) if os.path.exists(yol) else ("YOK", 0)
    for ad, yol, desen in (("k60_fiyat", Y["k60_fiyat"], "*.json"), ("k62_fiyat", os.path.join(Y["k62"], "fiyat"), "*.csv.gz"),
                           ("k62_kap", os.path.join(Y["k62"], "kap"), "*.json.gz"), ("k58_yahoo", Y["k58_yahoo"], "*.json"),
                           ("kap_iceriden", Y["kap_iceriden"], "*"), ("edgar_master", Y["edgar"], "edgar_master_*.gz")):
        out[ad] = vdyt_sha_klasor(yol, desen)
    return out


def _vdyt_git(args: List[str], kok: Optional[str] = None) -> Tuple[int, str, str]:
    try:
        r = subprocess.run(["git", "-C", kok or KOK_VDYT] + args, capture_output=True, text=True, timeout=60)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (OSError, subprocess.SubprocessError) as ex:
        return 1, "", str(ex)


def vdyt_git_islenmis(yol: str, ne: str) -> Dict[str, str]:
    """Dosya git'e işlenmiş ve işlendikten sonra değişmemiş olmalı; değilse VdytHata."""
    kl, rel = os.path.dirname(os.path.abspath(yol)), os.path.basename(yol)
    k1, o1, e1 = _vdyt_git(["log", "-1", "--format=%H %cI", "--", rel], kl); k2, o2, e2 = _vdyt_git(["status", "--porcelain", "--", rel], kl)
    if k1 != 0 or not o1:
        raise VdytHata(f"{ne} git'e işlenmemiş ({rel}): önce ana oturum denetleyip commit eder; koşu REDDEDİLDİ")
    if k2 != 0 or o2:
        raise VdytHata(f"{ne} git'e işlendikten sonra değişmiş ({o2 or e2}): koşu REDDEDİLDİ")
    h, z = o1.split(" ", 1)
    return {"commit": h, "commit_zamani": z}


def vdyt_parametre_kaydi(cikti: Optional[str] = None, ek: Optional[Dict[str, Any]] = None) -> str:
    """Tekrarlanabilirlik kaydı (çıktı 12): sürüm, kod sha256, git commit, eşik mührü, veri sha256'ları, tarih aralıkları, kütüphane sürümleri."""
    k, h, _e = _vdyt_git(["rev-parse", "HEAD"])
    kayit = {"zaman": _vdyt_simdi(), "surum": VDYT_SURUM, "kod_sha256": vdyt_kod_sha(), "git_head": h if k == 0 else None, "esik_sha256": vdyt_esik_sha(),
             "veri_sha256": {a: list(v) for a, v in vdyt_veri_sha().items()}, "kesik": VDYT_ESIK["kesik"],
             "pazar_bas": {p: v["bas"] for p, v in VDYT_ESIK["pazar"].items()}, "python": sys.version.split()[0], "numpy": np.__version__,
             "pandas": pd.__version__, "esik": VDYT_ESIK, **(ek or {})}
    return _vdyt_json(_vdyt_yol("parametre", cikti), kayit)


# ---------------------------------------------------------------- 14) KAPSAM (yalnız sayım)
def vdyt_kapsam(pazarlar: Optional[List[str]] = None, cikti: Optional[str] = None, isci: int = 2, E: Optional[Dict[str, Any]] = None,
                girdi: Optional[Dict[str, Tuple[Dict[str, Any], pd.DataFrame]]] = None) -> Dict[str, Any]:
    """Gerçek veride YALNIZ SAYIM: pazar x tanım x dönem sıkışma bölgesi sayısı, süre dağılımı (yalnız süre), karar noktası sayısı (yaş x dönem), olay türü
    başına olay ve olayı olan bölge sayısı, hisseye özgü geçmişi yeterli karar noktası oranı. Genişleme oranı, yön, getiri, model başarısı HESAPLANMAZ."""
    E = E or VDYT_ESIK; pazarlar = pazarlar or ["BIST", "ABD", "BIST_K62"]; out: Dict[str, Any] = {"zaman": _vdyt_simdi(), "surum": VDYT_SURUM, "pazar": {}}
    for pz in pazarlar:
        try:
            F_, Ev_ = (girdi or {}).get(pz, (None, None))
            Z = vdyt_pazar_isle(pz, "kapsam", E, isci, F_, Ev_)
        except VdytHata as ex:
            out["pazar"][pz] = {"durum": f"EKSİK: {ex}"}; continue
        R = Z["R"]; Ev = Z["Ev"]; Pn = Z["Pn"]; o: Dict[str, Any] = {"hisse": len(Z["F"]["S"]), "hisse_hata": len(Z["hata"]), "sure_sn": Z["sure_sn"],
                                                                     "takvim": [str(Pn["takvim"].min().date()), str(Pn["takvim"].max().date())] if len(Pn["takvim"]) else None,
                                                                     "endeks_kaynak": Pn["endeks_kaynak"], "olay_notu": Z["ev_not"]}
        U = Pn["uygun"]; o["uygun_hisse_gun_yil"] = {int(y): int(v) for y, v in U.sum(axis=1).groupby(U.index.year).sum().items()}
        o["uygun_hisse_yil_sonu"] = {int(y): int(v) for y, v in U.sum(axis=1).groupby(U.index.year).last().items()}
        o["sektorlu_hisse"] = int(sum(1 for s in Z["F"]["S"] if s in Pn["sektor"]))
        o["olay_turu"] = {t: {"olay": int(len(g)), "hisse": int(g.sembol.nunique()), "ilk": str(g.g0_tarih.min().date()), "son": str(g.g0_tarih.max().date())}
                          for t, g in Ev.groupby("tur")}
        bol, kar, olay = {}, {}, {}
        for K in Z["kombolar"]:
            ad = K["ad"]; T = pd.concat([h["bolge"][ad] for h in R if ad in h["bolge"]], ignore_index=True)
            Tu = T[T.uygun]; dsat = {}
            for dn, a, b in E["donem_kapsam"]:
                m = (Tu.bas_tarih >= pd.Timestamp(a)) & (Tu.bas_tarih <= pd.Timestamp(b)); dsat[dn] = int(m.sum())
            q = Tu.sure.quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_dict() if len(Tu) else {}
            bol[ad] = {"rol": K["rol"], "tanim": K["tanim"], "esik": E["tanim"][K["tanim"]].get("esik", [None])[K["esik_idx"]] if K["tanim"] != "T5" else "T1-T4 ana, en az 3",
                       "k": K["k"], "genisleme": K["tur"], "bolge_hepsi": int(len(T)), "bolge_uygun": int(len(Tu)), "donem": dsat,
                       "hisse": int(Tu.sembol.nunique()) if len(Tu) else 0,
                       "sure": {"ort": float(Tu.sure.mean()) if len(Tu) else None, **{f"q{int(k * 100)}": float(v) for k, v in q.items()},
                                "max": int(Tu.sure.max()) if len(Tu) else None, **{f">={a}": int((Tu.sure >= a).sum()) for a in (20, 40, 60, 90, 120)}}}
            if K["rol"] == "ana":
                KD = pd.concat([h["karar"][ad] for h in R if ad in h["karar"]], ignore_index=True)
                kar[ad] = {"toplam": int(len(KD)), "yas": {int(a): int(v) for a, v in KD.yas.value_counts().sort_index().items()} if len(KD) else {},
                           "donem": {dn: int(((KD.yil >= pd.Timestamp(a).year) & (KD.yil <= pd.Timestamp(b).year)).sum()) for dn, a, b in E["donem_kapsam"]} if len(KD) else {},
                           "hisse_gecmisi_yeterli_pay": float(KD.hs_yeterli.mean()) if len(KD) else None}
                OL = pd.concat([h["olay"][ad] for h in R if ad in h["olay"] and len(h["olay"][ad])], ignore_index=True)
                olay[ad] = {t: {"olay_hizali": int(g.olay.sum()), "olayi_olan_bolge": int(g.bolgede_olay_olan_bolge.sum()), "e2_uygun_olay": int(g.e2_uygun_olay.sum())}
                            for t, g in OL.groupby("tur")} if len(OL) else {}
        o["bolge"] = bol; o["karar"] = kar; o["olay_eslesme"] = olay; out["pazar"][pz] = o
        del Z, R
    _vdyt_json(_vdyt_yol("kapsam", cikti), out)
    _vdyt_yaz(_vdyt_yol("kapsam_md", cikti), vdyt_kapsam_md(out))
    vdyt_parametre_kaydi(cikti, {"komut": "kapsam"})
    return out


def vdyt_kapsam_md(K: Dict[str, Any]) -> str:
    L = [f"# VDYT kapsam sayımı (YALNIZ SAYI)\n\nÜretim: {K['zaman']} ({K['surum']}). `python -I VDYT.py kapsam`. Genişleme oranı, yön, getiri, model başarısı "
         f"HESAPLANMADI; bitiş türü (genişleme / sönme) dağılımı bu raporda YOK (etiket bilgisi).\n"]
    for pz, o in K["pazar"].items():
        if "bolge" not in o:
            L.append(f"\n## {pz}\n\n{o.get('durum')}\n"); continue
        L.append(f"\n## {pz}\n\nHisse {_t(o['hisse'])} (hata {o['hisse_hata']}), takvim {o['takvim']}, sektörlü hisse {_t(o['sektorlu_hisse'])}, endeks kaynağı "
                 f"{o['endeks_kaynak']}, süre {o['sure_sn']} sn.\n\nYıl sonu uygun hisse: " + ", ".join(f"{y}: {_t(v)}" for y, v in o["uygun_hisse_yil_sonu"].items()) + "\n")
        dn = [d[0] for d in VDYT_ESIK["donem_kapsam"]]
        L.append("\n### Sıkışma bölgeleri (uygun; başlangıç dönemine göre) ve süre dağılımı (işlem günü)\n\n| kombinasyon | rol | eşik | k / genişleme | bölge (uygun / hepsi) | "
                 + " | ".join(dn) + " | hisse | süre ort | q10 | q25 | medyan | q75 | q90 | max | >=20 | >=40 | >=60 | >=90 | >=120 |\n|" + "---|" * (17 + len(dn)) + "\n")
        for ad, b in o["bolge"].items():
            s = b["sure"]
            L.append(f"| {ad} | {b['rol']} | {b['esik']} | {b['k']} {b['genisleme']} | {_t(b['bolge_uygun'])} / {_t(b['bolge_hepsi'])} | "
                     + " | ".join(_t(b["donem"].get(x)) for x in dn) + f" | {_t(b['hisse'])} | {_t(s.get('ort'), 1)} | {_t(s.get('q10'))} | {_t(s.get('q25'))} | "
                     f"{_t(s.get('q50'))} | {_t(s.get('q75'))} | {_t(s.get('q90'))} | {_t(s.get('max'))} | " + " | ".join(_t(s.get(f'>={a}')) for a in (20, 40, 60, 90, 120)) + " |\n")
        L.append("\n### Karar noktaları (ana tanımlar; bölge o yaşta hâlâ açık, uygun)\n\n| tanım | toplam | " + " | ".join(f"yaş {a}" for a in VDYT_ESIK["karar_yas"])
                 + " | " + " | ".join(dn) + " | hisse geçmişi yeterli (>= 3 önceki bölge) |\n|" + "---|" * (3 + len(VDYT_ESIK["karar_yas"]) + len(dn)) + "\n")
        for ad, k in o["karar"].items():
            L.append(f"| {ad} | {_t(k['toplam'])} | " + " | ".join(_t(k["yas"].get(a, 0)) for a in VDYT_ESIK["karar_yas"]) + " | "
                     + " | ".join(_t(k["donem"].get(x, 0)) for x in dn) + f" | %{_t(100 * (k['hisse_gecmisi_yeterli_pay'] or 0), 1)} |\n")
        L.append("\n### Olaylar (tür başına) ve ana tanımda eşleşme\n\n| tür | olay | hisse | ilk | son | " + " | ".join(f"{ad}: olayı olan bölge / E2 uygun olay" for ad in o["olay_eslesme"])
                 + " |\n|" + "---|" * (5 + len(o["olay_eslesme"])) + "\n")
        for t, v in sorted(o["olay_turu"].items()):
            L.append(f"| {t} | {_t(v['olay'])} | {_t(v['hisse'])} | {v['ilk']} | {v['son']} | "
                     + " | ".join(f"{_t(o['olay_eslesme'][ad].get(t, {}).get('olayi_olan_bolge'))} / {_t(o['olay_eslesme'][ad].get(t, {}).get('e2_uygun_olay'))}"
                                  for ad in o["olay_eslesme"]) + " |\n")
        L.append("\nOlay kaynak notları: `" + json.dumps(o["olay_notu"], ensure_ascii=False, default=str)[:3000] + "`\n")
    return "".join(L)


# ---------------------------------------------------------------- 15) VERİ ENVANTERİ (yeni indirme yok)
def _vdyt_dene(fn: Callable[[], Any]) -> Any:
    try:
        return fn()
    except Exception as ex:   # envanter hiçbir kaynakta durmaz; hata satıra yazılır
        return {"hata": f"{type(ex).__name__}: {str(ex)[:160]}"}


def vdyt_envanter_olc() -> Dict[str, Any]:
    """Kaynak başına sayım (yalnız kapsam / alan / tarih; getiri yok)."""
    Y = VDYT_YOL; S: Dict[str, Any] = {}

    def fiyat_sozluk(yol: str) -> Dict[str, Any]:
        V = _vdyt_pickle_oku(yol); V = {s: d.rename(columns=str.title) for s, d in V.items() if isinstance(d, pd.DataFrame) and len(d)}
        V = {s: d for s, d in V.items() if {"High", "Low", "Close", "Volume"} <= set(d.columns)}
        ilk = pd.Series({s: V[s].index.min() for s in V}); son = pd.Series({s: V[s].index.max() for s in V})
        hl = sum(int((V[s].High == V[s].Low).sum()) for s in V); sv = sum(int((V[s].Volume <= 0).sum()) for s in V); sat = sum(len(V[s]) for s in V)
        tut = sum(int(((V[s].High < V[s].Low) | (V[s].Close > V[s].High * 1.0001) | (V[s].Close < V[s].Low * 0.9999)).sum()) for s in V)
        return {"hisse": len(V), "alanlar": list(next(iter(V.values())).columns), "ilk_min": str(ilk.min().date()), "ilk_medyan": str(ilk.median().date()),
                "son_max": str(son.max().date()), "son_min": str(son.min().date()), "ilk_2015_07_once": int((ilk <= pd.Timestamp("2015-07-31")).sum()),
                "son_2026_06_once": int((son < pd.Timestamp("2026-06-01")).sum()), "satir": int(sat), "H_eq_L": hl, "hacim_sifir": sv, "OHLC_tutarsiz": tut}
    S["V_BIST"] = _vdyt_dene(lambda: fiyat_sozluk(Y["v_bist"]))
    S["V_ABD"] = _vdyt_dene(lambda: fiyat_sozluk(Y["v_abd"]))
    S["k34_yahoo"] = _vdyt_dene(lambda: fiyat_sozluk(Y["k34"]))

    def k60() -> Dict[str, Any]:
        F = vdyt_fiyat_yukle("ABD"); M = F["meta"]; ilk = pd.Series({s: d.index.min() for s, d in F["S"].items()})
        son = pd.Series({s: d.index.max() for s, d in F["S"].items()})
        return {"json": len(M), "fiyatli": len(F["S"]), "durum": pd.Series([m.get("durum") for m in M.values()]).value_counts().to_dict(),
                "tur": pd.Series([m.get("tur") for m in M.values() if m.get("durum") == "fiyat"]).value_counts().to_dict(),
                "ilk_2010_once": int((ilk <= pd.Timestamp("2010-01-31")).sum()), "ilk_2015_once": int((ilk <= pd.Timestamp("2015-12-31")).sum()),
                "ilk_min": str(ilk.min().date()), "son_max": str(son.max().date()), "son_2026_06_once": int((son < pd.Timestamp("2026-06-01")).sum()),
                "bolunmeli": int(sum(1 for m in M.values() if m.get("bolunme"))), "temettulu": int(sum(1 for m in M.values() if m.get("temettu"))),
                "alanlar": ["o", "h", "l", "c (bölünme düzeltmeli)", "v", "adjclose", "temettü / bölünme olayları"]}
    S["k60_fiyat"] = _vdyt_dene(k60)

    def k62() -> Dict[str, Any]:
        sat = []
        for f in glob.glob(os.path.join(Y["k62"], "fiyat", "*.csv.gz")):
            try:
                d = pd.read_csv(f, usecols=["tarih"])
            except (OSError, ValueError, pd.errors.EmptyDataError):
                sat.append((None, None)); continue
            t = pd.to_datetime(d.tarih.astype(str).str[:10]) if len(d) else pd.Series([], dtype="datetime64[ns]")
            sat.append((t.min() if len(t) else None, t.max() if len(t) else None))
        K = pd.DataFrame(sat, columns=["ilk", "son"]).dropna()
        hdr = pd.read_csv(sorted(glob.glob(os.path.join(Y["k62"], "fiyat", "*.csv.gz")))[0], nrows=1).columns.tolist()
        return {"dosya": len(sat), "dolu": int(len(K)), "ilk_2010_once": int((K.ilk <= pd.Timestamp("2010-01-31")).sum()), "ilk_min": str(K.ilk.min().date()),
                "son_max": str(K.son.max().date()), "kotasyondan_cikmis_son_2026_06_once": int((K.son < pd.Timestamp("2026-06-01")).sum()),
                "cikis_yillari": K[K.son < pd.Timestamp("2026-06-01")].son.dt.year.value_counts().sort_index().to_dict(), "alanlar": hdr}
    S["k62_fiyat"] = _vdyt_dene(k62)

    def k62kap() -> Dict[str, Any]:
        c: Dict[str, int] = {}; z = []
        for f in sorted(glob.glob(os.path.join(Y["k62"], "kap", "*.json.gz"))):
            for j in _vdyt_jsongz_oku(f):
                c[j.get("subject")] = c.get(j.get("subject"), 0) + 1; z.append(j.get("publishDate"))
        t = pd.to_datetime(pd.Series(z), format="%d.%m.%Y %H:%M:%S", errors="coerce")
        return {"kayit": len(z), "konu": dict(sorted(c.items(), key=lambda x: -x[1])), "ilk": str(t.min()), "son": str(t.max())}
    S["k62_kap"] = _vdyt_dene(k62kap)

    def liste(yol: str, tcol: str, scol: str, fmt: Optional[str]) -> Dict[str, Any]:
        X = pd.read_csv(yol); t = pd.to_datetime(X[tcol], format=fmt, errors="coerce")
        return {"satir": int(len(X)), "ilk": str(t.min()), "son": str(t.max()), "kod": int(X[scol].nunique()), "alanlar": X.columns.tolist()}
    S["pead_bist"] = _vdyt_dene(lambda: liste(os.path.join(Y["pead"], "liste_bist.csv.gz"), "yayin", "kod", "%d.%m.%Y %H:%M:%S"))
    S["pead_bist_2016_22"] = _vdyt_dene(lambda: liste(os.path.join(Y["pead"], "liste_bist_2016_22.csv.gz"), "yayin", "kod", "%d.%m.%Y %H:%M:%S"))
    S["pead_abd"] = _vdyt_dene(lambda: {**liste(os.path.join(Y["pead"], "liste_abd.csv.gz"), "tarih", "sembol", None),
                                        "saat": pd.read_csv(os.path.join(Y["pead"], "liste_abd.csv.gz")).saat.value_counts().to_dict()})

    def ic() -> Dict[str, Any]:
        L = pd.read_csv(os.path.join(Y["kap_iceriden"], "liste.csv.gz")); I = pd.read_csv(os.path.join(Y["kap_iceriden"], "islem.csv.gz"))
        haric = r"MENKUL DE[ĞG]ER|YATIRIM MENKUL|PORTF[ÖO]Y Y[ÖO]NET|B[ÜU]Y[ÜU]KŞEH|MENKUL KIYMET"; t = pd.to_datetime(L.yayin, format="%d.%m.%Y %H:%M:%S")
        yb = os.path.join(Y["kap_iceriden"], "bos.txt"); bos = []
        if os.path.exists(yb):
            with open(yb, encoding="utf-8") as f:
                bos = f.read().split()
        return {"bildirim_liste": int(len(L)), "haric_sonrasi": int((~L.unvan.astype(str).str.upper().str.contains(haric, regex=True)).sum()),
                "ayristirilan_bildirim": int(I.indeks.nunique()), "islem_satiri": int(len(I)), "ayristirilamayan_bos": len(bos),
                "kaynak_bildirim_ilk": I.groupby("indeks").kaynak.first().value_counts().to_dict(), "ilk": str(t.min()), "son": str(t.max()),
                "hisse": int(L.ilgili.astype(str).str.split(",").str[0].nunique()), "alanlar_islem": I.columns.tolist()}
    S["kap_iceriden"] = _vdyt_dene(ic)

    def fon() -> Dict[str, Any]:
        G = _vdyt_pickle_oku(Y["fon_G"])
        return {"satir": int(len(G)), "rapor": int(G.indeks.nunique()), "fon": int(G.fon.nunique()), "hisse": int(G.kod.nunique()),
                "ilk": str(G.bilinme.min()), "son": str(G.bilinme.max()), "alanlar": G.columns.tolist()}
    S["fon_G"] = _vdyt_dene(fon)

    def kapfon() -> Dict[str, Any]:
        k, o, e = _vdyt_git(["ls-tree", "-r", "--name-only", Y["kapfon_dal"]])
        if k != 0:
            return {"durum": f"dal yok ya da okunamadı ({e[:120]})"}
        k2, man, _e2 = _vdyt_git(["show", f"{Y['kapfon_dal']}:kapfon/manifest.json"])
        return {"dosyalar": o.splitlines(), "manifest_ozet": man[:600] if k2 == 0 else None, "acma": "python FON_IZI.py k9ac kapfon (yerelde AÇILMADI)"}
    S["kapfon_dal"] = _vdyt_dene(kapfon)

    def edgar() -> Dict[str, Any]:
        f = sorted(glob.glob(os.path.join(Y["edgar"], "edgar_master_*.gz")))
        X, n_ = vdyt_edgar(None)
        return {"dosya": len(f), "ilk_ceyrek": os.path.basename(f[0])[13:19] if f else None, "son_ceyrek": os.path.basename(f[-1])[13:19] if f else None,
                **n_, "grup_sayim": X.groupby("grup").size().to_dict() if len(X) else {}, "kodlu_sirket": int(X.sembol.nunique()) if len(X) else 0}
    S["edgar"] = _vdyt_dene(edgar)

    def finra() -> Dict[str, Any]:
        f = sorted(glob.glob(os.path.join(Y["k66_finra"], "shrt*.csv")))
        return {"dosya": len(f), "ilk": os.path.basename(f[0])[4:12] if f else None, "son": os.path.basename(f[-1])[4:12] if f else None}
    S["finra"] = _vdyt_dene(finra)

    def surucu() -> Dict[str, Any]:
        Sr = _vdyt_pickle_oku(Y["surucu"])
        return {k: [str(pd.Series(v).index.min().date()), str(pd.Series(v).index.max().date()), int(len(v))] for k, v in Sr.items()}
    S["surucu"] = _vdyt_dene(surucu)
    S["endeks"] = _vdyt_dene(lambda: {ad: [str(d.index.min().date()), str(d.index.max().date()), int(len(d))] for ad in ("XU100.IS", "SPY")
                                      for d in [vdyt_yahoo_oku(os.path.join(Y["k58_yahoo"], f"{ad}.json"))[0]] if d is not None})
    S["sektor"] = _vdyt_dene(lambda: {"BIST_sektor_BIST": len(vdyt_sektor("BIST")), "BIST_grup": len(set(vdyt_sektor("BIST").values())),
                                      "ABD_SIC_eslenen": len(vdyt_sektor("ABD")), "ABD_grup": len(set(vdyt_sektor("ABD").values())),
                                      "sektor_ABD_csv": int(len(pd.read_csv(Y["sektor_abd"]))) if os.path.exists(Y["sektor_abd"]) else 0})
    S["makro"] = _vdyt_dene(lambda: (lambda M: {"FOMC": len(M.get("FOMC", [])), "FOMC_planli": sum(1 for x in M.get("FOMC", []) if x.get("planli")),
                                                "PPK": len(M.get("PPK", [])), "ilk_FOMC": (M.get("FOMC") or [{}])[0].get("tarih"),
                                                "ilk_PPK": (M.get("PPK") or [{}])[0].get("tarih"), "EKSIK": M.get("EKSIK")})(
        _vdyt_json_oku(Y["makro"])) if os.path.exists(Y["makro"]) else {"durum": "EKSİK (python VDYT.py makro)"})
    S["onceki_tablolar"] = _vdyt_dene(lambda: {d: sorted(os.path.basename(x) for x in glob.glob(os.path.join(KOK_VDYT, "arastirma_cikti", d, "*")))[:30]
                                               for d in ("mum_sukun", "sessiz_ml", "k55_dallanma", "col_goz", "k60_veri")})
    return S


def vdyt_envanter(cikti: Optional[str] = None) -> Dict[str, Any]:
    """VDYT_VERI_ENVANTERI.md + VDYT_EKSIKLER.md (sayılar vdyt_envanter_olc'tan; yorum ve karar sabit metin)."""
    S = vdyt_envanter_olc(); _vdyt_json(os.path.join(cikti or VDYT_YOL["cikti"], "vdyt_envanter.json"), S)
    _vdyt_yaz(_vdyt_yol("envanter", cikti), vdyt_envanter_md(S)); _vdyt_yaz(_vdyt_yol("eksik", cikti), vdyt_eksik_md(S))
    return S


def _j(x: Any, n: int = 400) -> str:
    return json.dumps(x, ensure_ascii=False, default=str)[:n]


def vdyt_envanter_md(S: Dict[str, Any]) -> str:
    g = lambda k, a, d="-": (S.get(k) or {}).get(a, d) if isinstance(S.get(k), dict) else d   # noqa: E731
    ic = S.get("kap_iceriden", {})
    L = [f"""# VDYT veri envanteri (yeni indirmeden önce)

Üretim: {_vdyt_simdi()} — `python VDYT.py envanter` ({VDYT_SURUM}). Sayılar dosyalardan okundu; getiri hesaplanmadı. Kesik: fiyatlar {VDYT_ESIK['kesik']}'de kesilir
(fon krizi kuralı). Durum: VAR = analizde kullanılabilir; KISMEN = dönem / alan / pazar eksik; EKSİK = yok (ikame / uydurma yapılmadı).

## 1. Özet tablo (veri türü x pazar)

| veri türü | BIST | ABD | VDYT'de kullanım |
|---|---|---|---|
| Günlük OHLCV | VAR: V_BIST {g('V_BIST','hisse')} hisse, {g('V_BIST','ilk_min')} → {g('V_BIST','son_max')} ({g('V_BIST','ilk_2015_07_once')} hisse 2015-07 öncesinden); yalnız yaşayanlar | VAR: k60_fiyat {g('k60_fiyat','fiyatli')} hisse, {g('k60_fiyat','ilk_min')} → {g('k60_fiyat','son_max')} ({g('k60_fiyat','ilk_2010_once')} hisse 2010 başından); yalnız yaşayanlar | ana fiyat verisi |
| Uzun geçmiş / kotasyondan çıkanlar | KISMEN: K62 İş Yatırım {g('k62_fiyat','dolu')} hisse, {g('k62_fiyat','ilk_min')} → {g('k62_fiyat','son_max')}, çıkmış {g('k62_fiyat','kotasyondan_cikmis_son_2026_06_once')}; YALNIZ kapanış + hacim (açılış / yüksek / düşük YOK) | KISMEN: k34_yahoo {g('k34_yahoo','hisse')} hisse ama {g('k34_yahoo','ilk_min')}+ ve neredeyse hepsi yaşayan ({g('k34_yahoo','son_2026_06_once')} çıkmış); batanların Tiingo fiyatı lisans gereği yok | BIST_K62: yanlılık kontrolü (kapanış tanımları T2-T4); ABD delist: EKSİK |
| Endeks | VAR: XU100.IS {_j(g('endeks','XU100.IS'))}; K62 'endeks' sütunu | VAR: SPY {_j(g('endeks','SPY'))}; Fama-French günlük piyasa (1926+) | piyasa rejimi, pazar yönü |
| Sektör | VAR: sektor_BIST.csv (BIST alt endekslerinden; {g('sektor','BIST_grup')} grup, {g('sektor','BIST_sektor_BIST')} hisse) | KISMEN: SIC (k35, CIK→bugünkü kod) {g('sektor','ABD_SIC_eslenen')} hisse, {g('sektor','ABD_grup')} grup; sektor_ABD.csv yalnız V_ABD | sektör rejimi, rakip bilançosu |
| Bilanço tarihleri | VAR: KAP Finansal Rapor 2009-06+ (K62 kap; {_j(g('k62_kap','konu',{}).get('Finansal Rapor') if isinstance(g('k62_kap','konu',{}), dict) else '-')} kayıt), yayın saatli | KISMEN: Nasdaq takvimi {g('pead_abd','ilk')} → {g('pead_abd','son')} (saat %99 verilmemiş); öncesi 10-Q/10-K başvuru günü (EDGAR, VEKİL) | A planlı olay, beklenen bilanço özelliği |
| Temettü / bölünme / hak kullanım | KISMEN: K62 ham / düzeltilmiş kapanış oranı ve sermaye değişimi (hak kullanım günü; duyuru günü YOK) | VAR: Yahoo olayları (hak kullanım günü; {g('k60_fiyat','temettulu')} hisse temettü, {g('k60_fiyat','bolunmeli')} bölünme) | A planlı olay |
| Sermaye artırımı / pay arzı | KISMEN: K62 sermaye değişimi (tescil / işlem günü; karar günü YOK) | VAR: EDGAR S-1, S-3, 424B* başvuru günleri | B olay |
| Genel kurul | EKSİK | KISMEN: DEF 14A (vekâlet bildirimi; toplantı günü değil) | A olay (ABD) |
| İhale / sözleşme / sipariş / ortaklık / yönetim / dava / ürün (KAP özel durum) | EKSİK (KAP ÖDA listesi inmedi) | KISMEN: 8-K (madde kodu YOK), 13D, 425 / SC TO / DEFM14A | B olay; BIST'te 'habersiz' grup kirli (beyan) |
| İçeriden işlem | KISMEN: KAP Pay Alım Satım 2022-07 → 2026-10 ({ic.get('ayristirilan_bildirim', '-')} bildirim ayrıştırıldı; bölüm 3) | KISMEN: k30 Form 4 açık piyasa alımları 2022+ (özet; VDYT'de kullanılmıyor) | B olay (BIST) |
| Fon portföy raporları | KISMEN: G.pkl {g('fon_G','ilk')} → {g('fon_G','son')} ({g('fon_G','rapor')} rapor, {g('fon_G','fon')} fon); ham paket kapfon-veri dalında (açılmadı) | — | B olay (fon girişi) |
| Makro takvim | KISMEN: TCMB PPK günleri (`makro`); TÜİK enflasyon günü EKSİK | KISMEN: FOMC günleri (`makro`); CPI / istihdam (BLS 403) EKSİK | C olay; içerik / sürpriz YOK |
| Emtia / kur / faiz | VAR: surucu.pkl (GC, SI, CL, HG, ZW, HRC, ALI, USDTRY, ^TNX 2015+, CDS 2022+) | aynı | C olay (şok günleri), 2010-2014 EKSİK |
| Sektör haberleri | VERİ YOK | VERİ YOK | yok (beyan) |
| Endeks gelişmeleri (endekse giriş / çıkış) | EKSİK | EKSİK | yok |
| Açığa satış | — | VAR: FINRA iki haftalık {g('finra','ilk')} → {g('finra','son')} ({g('finra','dosya')} dosya) | VDYT'de kullanılmıyor (olay değil; bilgi) |
| Saatlik veri | — | KISMEN: k40 saatlik yalnız 4 endeks, son 730 gün | kullanılmıyor |
| Önceki sıkışma / volatilite / rejim tabloları | VAR (farklı tanımlar): MUM_SUKUN, SESSIZ_ML, K55 dallanma, COL_GOZ, rejim.py (CDS / EEM) | K55 / K60 kapsam tabloları | KULLANILMAZ: VDYT bağımsız motor; tanımlar ön kayıtta baştan |

## 2. Kaynak ayrıntıları

### 2.1 BIST günlük OHLCV — V_BIST.pkl (islenmis-veri dalı → /tmp/veri)
- Konum: `{VDYT_YOL['v_bist']}`; FON_IZI fi_k1_veri çıktısı (bölünme / marj düzeltmeli). Alanlar {g('V_BIST','alanlar')}.
- {g('V_BIST','hisse')} hisse; ilk gün en erken {g('V_BIST','ilk_min')} (medyan {g('V_BIST','ilk_medyan')}); son gün {g('V_BIST','son_min')} … {g('V_BIST','son_max')}; {g('V_BIST','satir')} satır.
- Kalite: H = L {g('V_BIST','H_eq_L')} gün, hacim <= 0 {g('V_BIST','hacim_sifir')} gün (VDYT bunları işlemsiz gün sayar, atar), OHLC tutarsız {g('V_BIST','OHLC_tutarsiz')} satır (H = max(O,H,C), L = min(O,L,C) ile düzeltilir).
- Delist: YOK (bugün işlem görenler). Durum: VAR (yaşayan yanlılığı beyan).

### 2.2 BIST uzun geçmiş — K62 İş Yatırım günlük (/tmp/k62_veri/fiyat)
- {g('k62_fiyat','dosya')} kod dosyası, {g('k62_fiyat','dolu')} dolu; ilk {g('k62_fiyat','ilk_min')} ({g('k62_fiyat','ilk_2010_once')} hisse 2010 başından), son {g('k62_fiyat','son_max')} (K62 kesiği). Alanlar {g('k62_fiyat','alanlar')}.
- Kotasyondan çıkmış (son gün 2026-06 öncesi): {g('k62_fiyat','kotasyondan_cikmis_son_2026_06_once')}; çıkış yılları {_j(g('k62_fiyat','cikis_yillari'))}.
- AÇILIŞ / YÜKSEK / DÜŞÜK YOK → ATR, gövde, fitil, savunma hattı (gövde / fitil tabanı) hesaplanamaz. Durum: KISMEN (yalnız kapanış tanımları T2-T4 ve RV genişlemesi; yanlılık kontrolü).

### 2.3 ABD günlük OHLCV — k60_fiyat (Yahoo, /tmp/k60_fiyat) ve V_ABD
- k60_fiyat: {g('k60_fiyat','json')} JSON, fiyatlı {g('k60_fiyat','fiyatli')}; durum {_j(g('k60_fiyat','durum'))}; tür {_j(g('k60_fiyat','tur'))}; ilk {g('k60_fiyat','ilk_min')}, son {g('k60_fiyat','son_max')} (K60 kesiği); 2015 sonundan önce başlayan {g('k60_fiyat','ilk_2015_once')}.
- V_ABD: {g('V_ABD','hisse')} hisse, {g('V_ABD','ilk_min')} → {g('V_ABD','son_max')} (hepsi k60 evreninde; VDYT ABD = k60, V_ABD alt küme bilgisi).
- k34_yahoo (veri2): {g('k34_yahoo','hisse')} hisse, {g('k34_yahoo','ilk_min')} → {g('k34_yahoo','son_max')}, son günü 2026-06 öncesi {g('k34_yahoo','son_2026_06_once')} → delist yanlılığını azaltmaz.
- Delist: Yahoo batan şirketin fiyatını vermez; Tiingo fiyatları lisans gereği repoda yok. Durum: VAR (yaşayan yanlılığı büyük, beyan).

### 2.4 Olay kaynakları
- KAP Finansal Rapor (K62 kap, 2009-06+): {g('k62_kap','kayit')} kayıt; konu sayımı {_j(g('k62_kap','konu'), 600)}; {g('k62_kap','ilk')} → {g('k62_kap','son')}. pead listeleri: 2022-07+ {g('pead_bist','satir')} satır, 2016-07 → 2022-12 {g('pead_bist_2016_22','satir')} satır (K62 kap bunları kapsar).
- Nasdaq bilanço takvimi (pead/liste_abd): {g('pead_abd','satir')} satır, {g('pead_abd','kod')} kod, {g('pead_abd','ilk')} → {g('pead_abd','son')}; saat {_j(g('pead_abd','saat'))}.
- EDGAR üç aylık ana dizin (/tmp/k60_secframes/edgar_master_*): {g('edgar','dosya')} dosya ({g('edgar','ilk_ceyrek')} → {g('edgar','son_ceyrek')}), {g('edgar','satir')} satır; seçili formlar {g('edgar','secili_form')}, bugünkü kodla eşlenen {g('edgar','kodla_eslenen')}; grup sayımı {_j(g('edgar','grup_sayim'))}. Yalnız form türü ve başvuru GÜNÜ (saat yok, 8-K madde kodu yok); CIK → kod eşlemesi bugünkü company_tickers ({g('edgar','cik_ticker')} CIK).
- Fon portföy raporları: G.pkl {g('fon_G','satir')} satır, {g('fon_G','rapor')} rapor, {g('fon_G','fon')} fon, {g('fon_G','hisse')} hisse, {g('fon_G','ilk')} → {g('fon_G','son')}; ham KAP fon raporu paketi kapfon-veri dalında ({_j(g('kapfon_dal','dosyalar'), 300)}).
- Makro: {_j(S.get('makro'), 500)}.
- Emtia / kur / faiz (k36 surucu.pkl): {_j(S.get('surucu'), 700)}.

## 3. '6.637 KAP raporu' kaydı (Cemal'in bildiği kaynak)
- Nerede yazıyor: IZ_DEFTERI.md görev günlüğü 2026-10-26 satırı ve Ç99 (IZ_KARNE.py IK_KAYIT, K27); kod FON_IZI.py `fi_k27_liste`, `fi_k27_ayristir`, `fi_k27_pdf_ayristir`, `fi_k27_indir`, `fi_k27_olaylar`; çıktılar arastirma_cikti/fon_izi/k27_ozet.csv, k27_olay.csv, k27_deneme.csv.
- Ne: finansal rapor DEĞİL; KAP 'Pay Alım Satım Bildirimi' (içeriden işlem bildirimleri; konu 8aca490d50286f620150287614ae005c), 2022-07 → 2026-10.
- Veri: islenmis-veri dalı `kap_iceriden/` (liste.csv.gz, islem.csv.gz, bos.txt) → `{VDYT_YOL['kap_iceriden']}` (git worktree; yeniden indirilmedi).
- Dosyadan sayım: liste {ic.get('bildirim_liste', '-')} bildirim ({ic.get('ilk', '-')} → {ic.get('son', '-')}); aracı kurum / portföy şirketi hariç {ic.get('haric_sonrasi', '-')}; ayrıştırılan
  {ic.get('ayristirilan_bildirim', '-')} bildirim = {ic.get('islem_satiri', '-')} işlem satırı (bildirim başına ilk kaynak {_j(ic.get('kaynak_bildirim_ilk'))}); ayrıştırılamayan {ic.get('ayristirilamayan_bos', '-')}.
  Alanlar: {ic.get('alanlar_islem', '-')}. Not: defterde '6.265'i MKK aktarımı PDF' yazıyor; dosyadaki bildirim başına ilk kaynak sayımı yukarıdaki gibidir (fark sayım biçiminden; ana oturum denetlesin).
- VDYT kullanımı: B olayı 'içeriden net alım / net satım bildirimi' (net = gün sonu - gün başı nominal, yoksa alım - satım), bilgi zamanı KAP yayın saati.
- KAP finansal rapor listesi ayrıdır: 2009-06+ {_j(g('k62_kap','konu',{}).get('Finansal Rapor') if isinstance(g('k62_kap','konu',{}), dict) else '-')} 'Finansal Rapor' kaydı (K62), 2016-07+ pead listeleri.

## 4. Önceki sıkışma / volatilite / rejim tabloları
{_j(S.get('onceki_tablolar'), 1500)}
Bunlar farklı amaçla ve farklı tanımla üretildi (Çöl Yolu, K55, MUM_SUKUN). VDYT bunları GİRDİ olarak kullanmaz; tanımlar ön kayıtta baştan ve bağımsız.

## 5. Kullanım kararı (ön kayıtta bağlayıcı)
- Karar pazarları: BIST = V_BIST (OHLCV, 2015-06+), ABD = k60_fiyat (OHLCV, 2010+). BIST_K62 (kapanış, 2008+, kotasyondan çıkanlar dahil) yalnız yanlılık kontrolü.
- Yeni fiyat / olay indirmesi YOK. Tek ağ işi: `makro` komutu ile resmi FOMC / PPK tarih listesi (bu oturumda indirildiyse yukarıda sayısı var).
"""]
    return "".join(L)


def vdyt_eksik_md(S: Dict[str, Any]) -> str:
    sat = [
        ("BIST açılış / yüksek / düşük, 2015-06 öncesi ve kotasyondan çıkanlar", "BIST", "T1 (ATR), T5, TR genişlemesi, mum / fitil / gövde ölçüleri, savunma hattı (gövde, fitil) 2008-2015 ve batanlarda yapılamaz; BIST OHLC analizleri yalnız yaşayanlarla", "K62 kapanışıyla T2-T4 + RV genişlemesi (yanlılık kontrolü)"),
        ("ABD kotasyondan çıkan / batan şirket fiyatları", "ABD", "hayatta kalma yanlılığı düzeltilemez; sıkışmadan sonra batanlar eksik (aşağı yönlü genişlemeler eksik sayılır)", "beyan; sonuç 'yaşayan evren' koşullu"),
        ("KAP özel durum açıklamaları (sözleşme, ihale, ortaklık, sermaye artırımı KARARI, genel kurul, temettü KARARI, yönetim, dava, ürün)", "BIST", "B kategorisinin çoğu, olay türüne göre ayrım, BIST 'habersiz kırılım' kontrol grubunun temizliği (habersiz = 'kayıtlı veri setlerinde olay yok')", "yok; KAP API'den indirilebilir (ana oturum kararı, Faz 2 öncesi)"),
        ("BIST genel kurul ve temettü duyuru günleri", "BIST", "planlı olayın önceden bilinme günü; yalnız hak kullanım günü (K62) var", "hak kullanım günü (bilgi = o gün)"),
        ("ABD 8-K madde kodları", "ABD", "8-K içeriği (sözleşme / yönetim / satın alma) ayrılamaz; bilanço 8-K'sı yalnız tarih yakınlığıyla (+-3 iş günü) çıkarılır", "8-K tek tür"),
        ("ABD bilanço açıklama günü 2010 → 2022-11", "ABD", "gerçek açıklama günü yerine 10-Q / 10-K başvuru günü (çoğu kez açıklamadan sonra) → olay penceresinde kayma", "VEKİL olarak işaretli; 2022-12+ Nasdaq ile ayrı rapor"),
        ("Nasdaq bilanço saati", "ABD", "%99 'time-not-supplied' → olay günü 0 / +1 ayrımı belirsiz", "g0 = takvim günü; [0] ve [1,5] pencereleri ayrı raporlanır"),
        ("ABD CPI / istihdam yayın günleri (BLS)", "ABD", "makro C kategorisinde enflasyon / istihdam günleri", "yok (bls.gov 403); FOMC var"),
        ("TÜİK enflasyon yayın günleri", "BIST", "makro C kategorisinde enflasyon günü", "yok; PPK var"),
        ("Makro içerik / beklenti / sürpriz", "ikisi", "'sürpriz' etkisi ayrılamaz; yalnız 'planlı makro gün' etkisi", "beyan"),
        ("Sektör haberleri", "ikisi", "C kategorisinde sektör haberi", "VERİ YOK; yalnız rakip bilançosu (sektörün çeyrekteki ilk bilanço günü)"),
        ("Endeks giriş / çıkış günleri", "ikisi", "endeks gelişmesi olayı", "yok"),
        ("Emtia / kur / faiz serileri 2010-2014", "ABD", "2015 öncesi emtia şoku olayı", "2015+ ile sınırlı"),
        ("İçeriden işlem 2022-07 öncesi (BIST); Form 4 yönü (ABD)", "ikisi", "B içeriden olayı yalnız BIST 2022-07+; ABD'de yok", "BIST 2022-07+"),
        ("Fon raporları 2023 öncesi", "BIST", "fon girişi olayı yalnız 2023+", "2023+"),
        ("Gün içi (saatlik) hisse verisi", "ikisi", "kırılımın gün içi sırası, KAP saatine göre tepki", "yok"),
        ("Kod değişikliği / eski kod eşlemesi (EDGAR CIK → bugünkü kod)", "ABD", "kodu değişmiş şirketlerin eski başvuruları eşlenmez (eksik olay)", "beyan"),
    ]
    L = ["# VDYT eksik veri raporu\n\nÜretim: " + _vdyt_simdi() + ". İkame / uydurma yapılmadı. Engellenen analizler Faz 2 raporunda 'EKSİK' olarak kalır.\n\n",
         "| eksik veri | pazar | engellediği analiz | VDYT'deki karşılık |\n|---|---|---|---|\n"]
    L += [f"| {a} | {b} | {c} | {d} |\n" for a, b, c, d in sat]
    mk = S.get("makro") or {}
    L.append(f"\nMakro takvim durumu: {_j(mk, 600)}\n")
    return "".join(L)


# ---------------------------------------------------------------- 16) ÖN KAYIT
def vdyt_onkayit_metin(zaman: str, veri_sha: Dict[str, Tuple[str, int]], kapsam: Optional[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> str:
    E = E or VDYT_ESIK; T = E["tanim"]; G = E["genisleme"]; O = E["olay"]; W = E["wf"]
    oz = "\n".join(f"| {g} | {', '.join(c)} |" for g, c in VDYT_OZELLIK.items())
    olay = "\n".join(f"| {k} | {v['pazar']} | {v['kat']} | {v['ad']} | {v['kaynak']} | {'EVET' if v['onceden'] else 'HAYIR'} | {v['bilgi']} |" for k, v in VDYT_OLAY_TUR.items())
    tanim = "\n".join(f"| {k} | {v['ad']} | {v['tarif']} | {', '.join(map(str, v.get('esik', ['-'])))} (ilk = ana) | {v['veri']} |" for k, v in T.items())
    kombo = "\n".join(f"| {K['ad']} | {K['rol']} | {K['tanim']} | {T[K['tanim']].get('esik', ['T1-T4 ana'])[K['esik_idx']] if K['tanim'] != 'T5' else 'T1-T4 ana, >= 3'} | {K['k']} | {K['tur']} |"
                      for K in vdyt_kombolar("BIST", E) + [dict(x, ad="K62:" + x["ad"]) for x in vdyt_kombolar("BIST_K62", E)])
    veri = "\n".join(f"- {a}: sha256 {h} ({n} dosya)" for a, (h, n) in sorted(veri_sha.items()))
    kap = "(kapsam koşulmadı)"
    if kapsam:
        sat = []
        for pz, o in kapsam.get("pazar", {}).items():
            if "bolge" not in o:
                sat.append(f"| {pz} | {o.get('durum')} | | | |"); continue
            for ad, b in o["bolge"].items():
                if b["rol"] == "ana":
                    k_ = o["karar"].get(ad, {})
                    sat.append(f"| {pz} | {ad} | {_t(b['bolge_uygun'])} | {_t(b['sure'].get('q50'))} | {_t(k_.get('toplam'))} |")
        kap = ("| pazar | ana tanım | bölge (uygun) | medyan süre | karar noktası |\n|---|---|---|---|---|\n" + "\n".join(sat)
               + f"\n\nAyrıntı (dönem, duyarlılık kombinasyonları, olay eşleşmeleri): arastirma_cikti/vdyt/VDYT_KAPSAM.md ({kapsam.get('zaman')}).")
    return f"""# VDYT ÖN KAYIT — Volatilite Denge ve Yön Tahmini (ölçümden ÖNCE)

Yazım zamanı: {zaman}
ESIK_SHA256: {vdyt_esik_sha(E)}
KOD_SHA256: {vdyt_kod_sha()}
Sürüm: {VDYT_SURUM}

Bu dosya git'e işlenmeden, eşik mührü / kod sha256'sı / veri sha256'ları tutmadan `kos` ÇALIŞMAZ (VdytHata, çıkış 1). Sonuç görüldükten sonra tanım,
eşik, pencere, ufuk, bölme, model ya da karar kuralı değişmez; değişirse bu dosyada SAPMA olarak tarihli yazılır ve mühür / kod satırı yeniden işlenir.

## 0. Sınır ve beyan
- VDYT ayrı araştırma motorudur (Cemal'in açık isteği, 12 Kasım 2026). Çöl Yolu'nu, IZ_KARNE karar ölçütlerini (FI_OLCUT, tek cetvel) ve mevcut kodları
  DEĞİŞTİRMEZ, onlardan kod içe almaz; sonuçları Çöl Yolu kararlarına bağlanmaz.
- Çöl Yolu'nda KAPALI konulara değen değişkenler (hacim / hacim daralması, mum şekli ölçüleri: gövde, fitil, kapanış konumu; sektör rejimi) YALNIZ bu
  motorda, bu ön kayıttaki tanımlarla ölçülür. Kapalı konu yeniden açılmış sayılmaz; VDYT sonucu Çöl Yolu'na 'yaz' kararı olmadan taşınmaz.
- VDYT sonucu doğrulanmış sinyal değildir; yüksek genişleme olasılığı tek başına alım sinyali değildir; ilişki nedensellik diye yorumlanmaz; eğitim
  başarısı tahmin başarısı diye gösterilmez; yeni sinyal ancak bağımsız ileriye dönük testle (KASA) kanıtlanırsa söylenir; başarısız testler rapordan çıkmaz.

## 1. Sorular
S1 sıkışma ne zaman biter; S2 bitiş olasılığı yaşla nasıl değişir (hazard); S3 bitişten önce / sırasında hangi olaylar etkili ('haber bitirdi' ile
'zaten bitecekti' ayrı); S4 bitişin yönü; S5 hisseye özgü süre mi, piyasa rejimi mi, haber / bilanço mu daha açıklayıcı.
NİHAİ SORU: süre + kendi geçmişi + olay takvimi + savunma hattı (+ volatilite / hacim / mum / fiyat ölçüleri) birlikte, genişlemenin NE ZAMAN (Motor 1) ve
HANGİ YÖNE (Motor 2) olacağını basit piyasa kontrollerinden (bölüm 9) daha iyi tahmin ediyor mu?

## 2. Veri ve dönem
- Karar pazarları: BIST = {E['pazar']['BIST']['kaynak']}, {E['pazar']['BIST']['bas']}+; ABD = {E['pazar']['ABD']['kaynak']}, {E['pazar']['ABD']['bas']}+.
  Yanlılık kontrolü: BIST_K62 = {E['pazar']['BIST_K62']['kaynak']}; rol: {E['pazar']['BIST_K62']['rol']}.
- Kesik: bütün fiyatlar {E['kesik']}'de kesilir (fon krizi). Etiket penceresi kesiği aşan karar noktası ölçülmez; açık bölge kesikte SANSÜR.
- Bar temizliği: OHLC eksik / kapanış <= 0 atılır; hacim <= 0 (işlemsiz gün) atılır; H = max(O,H,C), L = min(O,L,C); iki bar arası > {E['bar']['bosluk_takvim_gun']} takvim günü = kopukluk (açık bölge SANSÜR, koşu sayımı yeniden).
- Uygunluk (bölge tespit gününde; karar noktaları yalnız uygun bölgelerden): BIST >= {E['pazar']['BIST']['uygunluk']['gecmis_gun']} bar geçmiş ve 20 gün medyan işlem değeri o günün BIST kesitinde
  %{int(100 * E['pazar']['BIST']['uygunluk']['likit_pct'])} yüzdeliğinin üstünde; ABD tür EQUITY, >= 252 bar, o gün ekranda görülen fiyat (bölünmeler geri alınmış) >= {E['pazar']['ABD']['uygunluk']['fiyat_min']} $, 20 gün medyan işlem değeri >= 1 milyon $ (K60 kuralı).
- Maliyet (yalnız bilgi amaçlı getirilerde, tek yön): BIST {E['pazar']['BIST']['maliyet'] * 1e4:.0f} bp, ABD {E['pazar']['ABD']['maliyet'] * 1e4:.0f} bp.
- Endeks (rejim ve pazar yönü): BIST XU100.IS, ABD SPY (k58 Yahoo); yoksa eşit ağırlıklı medyan getiri (beyan).
- Sektör: BIST sektor_BIST.csv 'sektor'; ABD SEC SIC 2 haneli ana grup (k35_sic, CIK → bugünkü kod; < 10 üyeli grup SIC bölümüne birleşir).

## 3. Test sırası (Faz 2; hepsi raporlanır)
1. Veri yükleme + mühür / kod / veri sha256 / git doğrulaması (biri tutmazsa ret).
2. Günlük ölçüler (bölüm 4.1), panel (uygunluk, tertiller, rejim).
3. Bütün kombinasyonlarda sıkışma bölgeleri (bölüm 4.3), yön (4.5), karar noktaları ve etiketler (4.6).
4. Süre analizi (bölüm 5): KM, CIF, yaş kovası hazard'ı, rejim tertiline göre hazard; süre yaklaşımları A-D'nin ileriye dönük Brier'i (bölüm 9).
5. Motor 1 (genişleme; 5 ana tanım x 3 ufuk) ve Motor 2 (yön; 5 ana tanım) walk-forward (bölüm 10), temellere karşı (bölüm 9), ablasyon (ana tanım / ana ufuk).
6. Birleşik üç sınıf (bilgi) + basit portföy (bilgi).
7. Olay analizi E1, E2 (bölüm 6), her ana tanım x her olay türü.
8. Savunma hattı H1-H5 (bölüm 7), karşılaştırma grupları K1-K6 (bölüm 8).
9. Plasebolar P1 (rastgele olay günü), P2 (rastgele sıkışma bölgesi) (bölüm 12).
10. Çoklu test (BH) + hipotez tablosu; karar tablosu.
11. Aşama 'wf' biter → rapor. Aşama 'kasa' ayrı komutla BİR KEZ açılır (bölüm 10) → final karar tablosu.
12. Grafik arşivi (bölüm 13), rapor (bölüm 15).

## 4. Tanımlar (hepsi yalnız t ve öncesi barlardan)
### 4.1 Günlük ölçüler (`vdyt_olculer`)
TR = max(H-L, |H-C[-1]|, |L-C[-1]|); TRn = TR / C[-1]; ATR14 = 14 bar TR ortalaması; NATR14 = ATR14 / C; RV20 = 20 bar log getiri std (ddof 1);
BBW20 = 4 x std(C,20, ddof 0) / SMA20; geçmiş penceresi = [t-{E['olcu']['gecmis_n']}, t-1], en az {E['olcu']['gecmis_min']} geçerli değer; yüzdelik = (küçük + 0,5 x eşit) / geçerli.
Diğer: RV5/RV20; hacim oranı = medyan(V,20) / medyan(V,250); gövde / aralık, üst ve alt fitil / aralık, kapanış konumu (C-L)/(H-L) (son 10 bar ort.);
gövde / C son 10 ort. ÷ 250 ort.; ln(C/SMA20, 50, 200); SMA50 eğimi (10 bar ln); ln getiri 20 / 60; likidite = ln medyan(C x V, 20); yükselen gün hacim payı (20).
### 4.2 Sıkışma tanımı ALTERNATİFLERİ (önceden; hepsi raporlanır, sonradan seçme yok; ANA = {E['ana_tanim']})
| kod | ad | tanım | eşikler | veri |
|---|---|---|---|---|
{tanim}
### 4.3 Bölge başlangıç / bitiş kuralı (`vdyt_bolgeler`)
- Açılış: 'sıkışık' durum {E['bolge']['min_gun']} işlem günü kesintisiz → bas = koşunun ilk günü, tespit = bas + {E['bolge']['min_gun'] - 1} (bölge tespit kapanışında bilinir; yaş = t - bas + 1, tespitte yaş {E['bolge']['min_gun']}).
- Bitiş (tespitten SONRAKİ ilk gerçekleşen): GENİŞLEME (4.4) | SÖNME: durum {E['bolge']['sonme_gun']} gün üst üste yanlış (bitiş = 5. gün) | SANSÜR: veri sonu / kesik / kopukluk.
- Bölge kapandıktan sonra yeni koşu sayımı ertesi günden başlar (aynı tanımda bölgeler çakışmaz).
### 4.4 Genişleme (bitiş) tanımı (eşiklerin hepsi önceden; ANA = {G['ana_tur']}, k = {G['ana_k']})
- TR: {G['tarif']['TR']}; k ∈ {G['k']}.
- RV: {G['tarif']['RV']} (kapanış verisi için; ANA tanımda duyarlılık).
- Referans gün sayısı < {E['bolge']['ref_min']} ise genişleme sayılmaz. Genişleme GÜNÜ = bit (genişlemenin bilindiği gün); pencerenin ilk günü gen_bas (grafik ve olay bayrakları için).
### 4.5 Yön
- Y1 (ANA): bölge kapanış aralığı [Lo, Hi] = bas .. gen_bas-1 kapanışları; gen_bas'tan bit + {E['yon']['Y1_ufuk']}'ye kadar ilk kapanış > Hi → YUKARI, < Lo → AŞAĞI, hiçbiri → BELİRSİZ; veri yetmezse ölçülmez.
- Y2: işaret(ln(C[bit + {E['yon']['Y2_ufuk']}] / C[gen_bas - 1])).
### 4.6 Karar noktaları ve etiketler (bağımlılık kuralı)
- Her bölgede yaşlar {E['karar_yas']} (o günün kapanışında bölge hâlâ açıksa), her biri ayrı satır; belirsizlik HİSSE kümeli bootstrap (bölgeler hisse içinde iç içe).
- Motor 1 etiketi y_h, h ∈ {E['ufuk']} (ANA {E['ana_ufuk']}): GENİŞLEME t < bit <= t+h → 1; bit > t+h ya da SÖNME t+h içinde → 0; SANSÜR t+h içinde ya da t+h veri dışında → ölçülmez.
- Motor 2 etiketi: y20 = 1 olan ve Y1 ∈ (YUKARI, AŞAĞI) satırlarda 'yukarı' = 1(Y1 = YUKARI). Çözülme tarihi = bit + 20.
- Savunma hipotezleri ve bölge karşılaştırmaları bölge başına TEK satır kullanır (genişlemeden önceki son karar noktası).
- Etiket tamamlanma tarihi: son_h = t + h. bar günü; Motor 2 için y1_son.
### 4.7 Kombinasyonlar (tanım x eşik x genişleme)
| ad | rol | tanım | eşik | k | genişleme |
|---|---|---|---|---|---|
{kombo}
ANA kombinasyonlarda bütün analizler; DUYARLILIK kombinasyonlarında yalnız bölge sayımı + süre analizi (KM, CIF, hazard).

## 5. Süre (S1, S2, S5)
- KM (GENİŞLEME nedenine özgü; SÖNME ve SANSÜR sansür), herhangi bitişe göre hayatta kalma, Aalen-Johansen kümülatif GENİŞLEME olasılığı (CIF), yaş başına
  kesikli hazard; yaş kovaları {E['yas_kova']}; tespit günündeki piyasa rejimi tertiline göre hazard. 'Süreye bağlı Markov' ayrıca kurulmaz: kesikli yaş hazard'ı
  zaten süreye bağlı geçiş olasılığıdır (beyan).
- Yaklaşımlar (ileriye dönük, Motor 1 etiketleriyle; özellik grupları bölüm 10): A ORTAK = {VDYT_SURE_MODEL['A_ORTAK']}; B HİSSE = {VDYT_SURE_MODEL['B_HISSE']}
  (hissenin yalnız t'den ÖNCE biten GENİŞLEME / SÖNME bölgeleri; en az {E['hisse_gecmis']['min_bolge']} bölge yoksa 'yetersiz' bayrağı ve oran 0);
  C REJİM = {VDYT_SURE_MODEL['C_REJIM']}; D ADAPTİF = {VDYT_SURE_MODEL['D_ADAPTIF']}. Her biri T0 (süresiz) ve T1 (süreli) temeline karşı.
- WF aşamasında 2024-01-01'i aşan bölgeler 2023 son işlem gününde SANSÜR sayılır (KASA verisi görülmez).

## 6. Olaylar (S3) — kategori, bilgi tarihi, pencereler
| kod | pazar | kategori | olay | kaynak | önceden bilinir | bilgi tarihi / g0 kuralı |
|---|---|---|---|---|---|---|
{olay}
- A planlı şirket, B beklenmedik şirket, C sektör / makro, D = habersiz kırılım (kontrol grubu; bölüm 8 K1). EDGAR formları: {json.dumps(VDYT_EDGAR_FORM, ensure_ascii=False)}.
- g0 = olayın ilk etkili işlem günü (takvim tarihinden sonraki ya da aynı ilk işlem günü). Özelliklerde bir olay ancak bilgi günü <= t ise görülür.
- E1 (uzun): koşul günü c = g0 - 21, c'de açık bölge; pencereler {O['pencere_e1']} (ilk genişlemenin bit - g0 farkı). E2 (kısa): c = g0 - 1; pencereler {O['pencere_e2']}.
- 'Haber bitirdi' ile 'zaten bitecekti' AYRIMI: beklenen oran = aynı c ayı (makroda aynı yıl), aynı momentum tertili, aynı likidite tertili, c'deki yaşı
  +-{O['esleme']['yas_tol']} gün olan, ölçülen aralıkta aynı türden olayı olmayan başka bölgelerden en çok {O['esleme']['kontrol_n']} kontrol (en çok {O['esleme']['aday_n']} aday, tohum {O['esleme']['tohum']}).
  Fark = gözlenen - beklenen (pencere başına), küme bootstrap (hisse; makroda olay günü). Tür başına en çok 50.000 hisse-olay (rastgele, tohumlu; toplam yazılır).
- Olay-bölge eşleme tablosu (çıktı 3): bölgenin [bas, bit + 20] aralığındaki her olay: bas, olay günündeki yaş, olay tarihi, önceden bilinir mi, kategori,
  genişleme tarihi, olay-genişleme işlem günü (bit - g0), yön (Y1), büyüklük ln(C[bit+5]/C[gen_bas-1]), olaydan önce volatilite artışı (ort TRn[g0-5..g0-1] /
  medyan TRn[bas..g0-6] >= {O['on_artis_esik']}).

## 7. Savunma hattı (S4) ve H1-H5
- Tanım (`vdyt_savunma`, YALNIZ bas..t barları): taban b ∈ {E['savunma']['tabanlar']} (ANA {E['savunma']['ana_taban']} = min(O,C)); tol = {E['savunma']['tolerans_tr']} x medyan TR;
  adaylar b'nin bölge aralığının alt {E['savunma']['alt_dilim']:.3f}'ündeki değerleri; temas(p) = |b - p| <= tol sayısı; p* = en çok temas (eşitlikte en düşük);
  hat VAR ⇔ temas >= {E['savunma']['min_temas']} ve ilk-son temas arası >= {E['savunma']['min_aralik']} bar. Çıktılar: temas, korunma süresi, kapanışla kırılma, fitil ihlali sayısı,
  mesafe / ATR, son testten beri gün, test hacmi / bölge medyan hacmi, yükselen dipler / alçalan tepeler ({E['savunma']['blok']}'lik blok eğimi).
- H1: hat korunmuş (VAR, kırılma yok) → YUKARI payı, hatsıza göre yüksek (+). H2: kapanışla kırılmış hat → YUKARI payı korunmuşa göre düşük (-).
  H3: yalnız fitil ihlali (kırılma yok) → YUKARI payı kapanışla kırılmışa göre yüksek (+). H4: hatsız karar noktalarında Motor 2 dengeli doğruluğu B1'den yüksek mi.
  H5: Motor 2'de HAT grubunun bağımsız katkısı (M_TAM vs M_TAM - HAT, Brier skill > 0) — süre ve olay özellikleri modelde varken.
- H1-H3 bölge başına son karar noktası, üç taban için ayrı (govde ANA); fark hisse kümeli bootstrap.

## 8. Karşılaştırma grupları (genişleyen bölgeler; sonuç = YUKARI payı ve büyüklük)
K1 haberli (A/B olayı g0 ∈ [gb{O['haberli'][0]}, gb+{O['haberli'][1]}]) vs habersiz (A/B yok [gb{O['habersiz'][0]}, gb+{O['habersiz'][1]}] ve makro yok [gb{O['makro_haberli'][0]}, gb]);
K2 bilanço öncesi (bilanço ∈ [gb+1, gb+10]) vs sonrası ([gb-10, gb]); K3 rakip bilançosu öncesi (∈ [gb+1, gb+10]) vs rakip yok (+-10);
K4 planlı makro öncesi (FOMC / PPK ∈ [gb+1, gb+5]) vs yok (+-5); K5 hatlı vs hatsız (son karar noktası); K6 sıkışma karar noktaları vs sıkışma DIŞI ve
aynı mutlak NATR ondalığında günler (sözde yaş, aynı genişleme kuralı; sonuç y{E['ana_ufuk']}). Kontroller: tabakalama (yıl x momentum tertili x likidite tertili;
K6'da + NATR ondalığı), grup 0 grup 1'in tabaka dağılımına yeniden ağırlıklanır; hisse kümeli bootstrap. Haber etkisinde sektör eşlerinin tepkisi: olay
günü getirisi - pazar getirisi özelliği (o_olay_tepki) ve rakip bilançosu olayı.

## 9. Temel modeller ('basit piyasa kontrolleri')
- Motor 1: T0 = eğitim sıklığı tablosu {E['temel']['G_T0']} (süresiz); T1 (ANA TEMEL) = {E['temel']['G_T1']} (pazar ayrı model olduğu için pazar x yaş kovası x
  takvim ayı); hücre n < {E['temel']['kucuk_hucre']} ise sondan bir anahtar düşürülür, en sonda genel oran.
- Motor 2: B0 = 0,5; B1 (ANA TEMEL) = eğitimde P(yukarı | pazarın son 60 gün yönü >= 0 / < 0).

## 10. Motorlar, özellikler, walk-forward
- Model: sırt cezalı lojistik regresyon (IRLS, ceza {E['model']['ridge']}, en çok {E['model']['tur']} tur); özellikler yalnız eğitimden uç kırpma {E['model']['winsor']} + z-ölçek, NaN → 0.
- Özellik grupları (Motor 1 ve Motor 2 aynı tam kümeyi kullanır; ablasyon = grubu çıkarıp yeniden eğitme, ana tanım x ana ufuk):
| grup | özellikler |
|---|---|
{oz}
- Olay özelliklerinde bilgi kuralı: beklenen bilanço = t'ye kadar BİLİNEN raporlardan (adaylar: son 12 aydaki raporların yıldönümleri ve son rapor + 91 gün;
  t'den sonraki en yakın aday; takvim günü, 0-90 kırpılır, yoksa 90 + 'yok' bayrağı); gerçekleşen
  gelecek bilanço günü kullanılmaz. Planlı makro (FOMC / PPK takvimi önceden yayımlanır) t+1..t+10 içinde mi. B olayları yalnız bilgi günü <= t.
- WALK-FORWARD: {W['kural']}. KEŞİF-WF test yılları {W['kesif_yillar']} (aşama 'wf'; veri 2023-12-31'de kesilir: etiket / çözülme tarihi 2024'e taşan
  test satırı ölçülmez). KASA = {W['kasa'][0]} → {W['kasa'][1]}, test yılları {W['kasa_yillar']}, eğitim aynı kural (ör. 2024 için 2023 sonuna kadar tamamlanan
  etiketler). KASA yalnız `kos --asama kasa` ile ve BİR KEZ açılır (vdyt_kasa_acildi.json; varsa ret). BIST'te OHLC 2015-06'dan → ilk test yılı 2019 (eğitim 2016-2018).
- Birleşik (bilgi): 20 gün içinde {{yukarı genişleme, aşağı genişleme, diğer}} çok sınıflı Brier; M = p1 x p2 vs T1 x B1.
- Portföy (bilgi): p1(y20) >= eğitimin %90'lık eşiği ve p2 >= 0,5 → ertesi açılış, 20 gün tut, {E['portfoy']['yuva']} yuva, maliyet sonrası; işlem sayısı, ort / medyan, isabet, en büyük düşüş.

## 11. Değerlendirme ve BAŞARI ÖLÇÜTÜ (karar kuralı)
- Ölçütler: Brier, log loss, Brier skill = 1 - Brier / Brier_temel, log loss skill, kalibrasyon (10 kutu, ECE), kesinlik / duyarlılık (0,5 ve eğitim %90 eşiği),
  dengeli doğruluk (yön), genişlemeye kadar süre (KM), 5 / 10 / 20 / 60 gün getiri, MFE / MAE (20), maliyet sonrası, işlem sayısı, portföy düşüşü (bilgi).
- Belirsizlik: hisse kümeli bootstrap B = {E['basari']['bootstrap']}, tohum {E['basari']['tohum']}, %95 yüzdelik aralık; iki yanlı p = erfc(|nokta| / (bootstrap sd x kök 2))
  (normal yaklaşım; yüzdelik p'nin 1/B tabanı BH'de tek güçlü etkiyi bile reddettirmeyeceği için).
- KARAR: {E['basari']['kural']}.
  ANA KARAR HÜCRELERİ: Motor 1 = ANA tanım {E['ana_tanim']}, ANA ufuk {E['ana_ufuk']}, M_TAM vs T1; Motor 2 = ANA tanım, M_TAM vs B1 (Brier skill, log loss skill, dengeli doğruluk farkı).
  Pazar başına iki motor → 4 ana karar; 'BASİTTEN İYİ' yalnız WF-TOPLAM ve KASA'nın İKİSİNDE şart tutarsa. Diğer tanım / ufuk / model satırları BİLGİ (BH ailesi F1 / F5).
- Etki büyüklüğü (skill, oran farkı) her satırda yazılır.

## 12. Çoklu test ve plasebo
- Aileler (BH q = {E['coklu']['bh_q']}, aile içinde): F1_MOTOR1, F1_MOTOR2 (tanım x ufuk x temel), F5_SURE (A-D x temel), F6_KATKI (ablasyon), F2_OLAY (tanım x tür x
  E1 / E2 x pencere), F3_HAT (H1-H5 x taban), F4_KARSILASTIRMA (K1-K6 x sonuç). Hipotez kimliği: '<test>-<pazar>-<tanım>-<ayrıntı>'.
- Bir aile bulgusu 'tutar' ancak WF'de BH ile reddedilir VE KASA'da aynı işaretle %95 aralığı 0'ı dışlarsa.
- P1 rastgele olay günleri (ana tanım, hisse olay türleri, E2; {E['coklu']['plasebo_olay_tekrar']} tekrar, tür başına en çok 3.000 olay): tekrar başına BH keşif sayısı → yanlış pozitif oranı.
- P2 rastgele sıkışma bölgeleri (gerçek sürelerle, rastgele başlangıç, sıkışma şartı yok, aynı genişleme kuralı; {E['coklu']['plasebo_bolge_tekrar']} tekrar): Motor 1 M_TAM vs T1 skill'i
  gerçek bölgelerinkiyle yan yana (sıkışmanın kendine özgü bilgisi var mı).

## 13. Grafik seçim kuralı (sonuç görülmeden)
Gruplar {E['grafik']['gruplar']}: BAŞARILI = Motor 1 ana hücre test satırı p >= eğitim %90 eşiği ve y = 1; BAŞARISIZ = aynı eşik ve y = 0; HABERLİ / HABERSİZ = K1 grupları;
HATLI / HATSIZ = genişlemeden önceki son karar noktasında hat var / yok. Pazar x grup başına {E['grafik']['grup_n']} örnek, numpy default_rng(sha256 tohum: {E['grafik']['tohum']},
pazar, grup), aday listesi (sembol, tarih) sıralı. Her örnek iki PNG ({E['grafik']['dpi']} dpi): tam (bas-{E['grafik']['on_bar']} .. bit+{E['grafik']['son_bar']}: mum gövde + fitil, ayrı hacim
paneli, sıkışma alanı, savunma hattı, olay günleri, genişleme başlangıcı, yön) ve SİNYAL GÜNÜ (yalnız karar gününe kadarki mumlar). Seçim sonuç görülerek değiştirilmez.

## 14. Tablo şemaları (bilgi tarihi kuralıyla)
**Sıkışma bölgeleri** (`bolge_<pazar>_<kombo>.csv.gz`): sembol str; bas, tespit, bit, gen_bas int (hisse bar indeksi); bit_tur int (1 GENİŞLEME, 2 SÖNME, 3 SANSÜR);
sure int (bit - bas + 1); bas_tarih, tespit_tarih, bit_tarih datetime; uygun bool (tespit günü); Y1, Y2 float (+1 / -1 / 0 / NaN); y1_son datetime; haberli, habersiz,
bilanco_once, bilanco_sonra, rakip_once, rakip_yok, makro_once, makro_yok float (0 / 1; gb'ye göre); buyukluk float; mom_g, liq_g float (gb-1 tertili); yil_g; rj_tespit
float (tespit günü piyasa rejimi); bit_wf, tur_wf, sure_wf (2023 sonu sansürlü). BİLGİ: bölge tespit kapanışında bilinir; bitiş bit kapanışında; yön çözülme günü y1_son.
**Olay eşleme** (`olay_eslesme_<pazar>_<ana>.csv.gz`): sembol, bolge, bas_tarih, yas_olayda int, olay_tarih (g0), tur, kat (A/B/C), onceden bool, genisleme_tarih,
olay_gen_gun int (bit - g0), yon_Y1, buyukluk, on_vol_artis float, on_vol_basladi (0/1), bit_tur str. BİLGİ: olay g0'da, özelliklerde bilgi günü <= t.
**Karar noktaları** (bellek içi; grafik için ince kopya): sembol, bolge, yas, t, tarih, bit, gen_bas, y5 / y10 / y20 (0/1/NaN), son5 / son10 / son20, Y1, Y2, y1_son, yukari,
mom_t, liq_t, natr_d, pazar_yon, yil, ay, yas_kova + bölüm 10 özellikleri (sv_*, svf_*, svk_*, sv_seviye) + bilgi: r5, r10, r20, r60, mfe, mae. BİLGİ: bütün özellikler <= t.
**Tahminler** (`tahmin_m1_<pazar>_<kombo>_y<h>.csv.gz`, `tahmin_m2_<pazar>_<kombo>.csv.gz`): satir, yil (test yılı), p_<model> (A_ORTAK, B_HISSE, C_REJIM, D_ADAPTIF, M_TAM,
M_EKSI_<grup>, T0, T1 / B0, B1), esik90_M_TAM, sembol, tarih, y. Eğitim yalnız son_h < test yılı başı.
**Hipotez** (`vdyt_sonuc_<aşama>.json` 'hipotez'): aile, id, nokta, alt, ust, p, bh_ret, ana, beklenen_isaret, n1, n0.

## 15. Çıktılar (Cemal'in 13. maddesi; Drive 'MyDrive/COLAB_VERILER/OUTPUT/VDYT' yüklemesini ana oturum yapar)
1 VDYT_VERI_ENVANTERI.md; 2 bolge_*.csv.gz (+ VDYT_KAPSAM.md); 3 olay_eslesme_*.csv.gz; 4 süre karşılaştırma (VDYT_RAPOR.md §Süre, sure_*.csv); 5 haberli-habersiz
(§Karşılaştırma K1, §Olay E1 / E2); 6 genişleme tahmin raporu (§Motor 1); 7 yön tahmin raporu (§Motor 2); 8 savunma hattı raporu (§H1-H5); 9 BIST ve ABD ayrı (her bölüm
pazar ayrı); 10 grafik/ (PNG); 11 VDYT_HATA_VE_EKSIK.md + VDYT_EKSIKLER.md; 12 vdyt_parametre_kaydi.json. Raporlar arastirma_cikti/vdyt/, büyük tablolar /tmp/vdyt/<aşama>/.

## 16. Yanlılık beyanı
- Yaşayan evren: V_BIST ve k60_fiyat bugün işlem görenler; batan / kotasyondan çıkan yok (BIST_K62 kontrolü yalnız kapanış tanımlarında). Aşağı yönlü genişlemeler
  ve sıkışmadan sonra batanlar eksik sayılır → yön sonuçları YUKARI lehine yanlı olabilir.
- Yeniden sunum: VDYT temel (bilanço) DEĞERİ kullanmaz; yalnız olay günü. Frames / yeniden sunum sorunu yok.
- KAP saati: yayın saati var; seans bitişi {O['bist_seans_bitis']} varsayımı (yıllara göre 17:30-18:10 farklı) → kenar olaylarda g0 bir gün kayabilir.
- EDGAR: yalnız başvuru günü (saat yok; özellikte ertesi işlem günü); 8-K madde kodu yok; CIK → bugünkü kod (eski kodlar eşlenmez).
- ABD bilanço 2010 → 2022-11: 10-Q / 10-K başvuru günü VEKİL; Nasdaq saatleri %99 belirsiz.
- Makro takvimde yalnız TARİH (içerik, beklenti, sürpriz yok); CPI / istihdam / TÜİK EKSİK.
- BIST KAP özel durum açıklamaları EKSİK → BIST 'habersiz' = kayıtlı veri setlerinde olay yok (gerçek habersizlik değil).
- Hacim ve mum değişkenleri Çöl Yolu'nda kapalı konudur; burada ayrı motor (bölüm 0).

## 17. SAPMA / BOŞLUK listesi (ana oturumun tasarım kararlarına göre)
1. Walk-forward test yılları: KEŞİF-WF 2019-2023 + KASA 2024-2026 (tasarımdaki '2019-2026' ikiye bölündü; KASA bir kez açılır). KASA yılları da yıllık yeniden eğitilir.
2. Temel T1'de 'ay' = takvim ayı (1-12; mevsimsellik), çünkü aynı takvim ayının oranı test anında bilinemez. Pazar ayrı model olduğundan anahtarda yok.
3. Karar noktası: sıkışma başına çok nokta (yaş 10-120) + hisse kümeli bootstrap; savunma / karşılaştırma testleri bölge başına tek nokta.
4. Motor 2 yalnız 20 gün içinde genişleyen satırlarda eğitilir / sınanır ('genişlerse yönü'); birleşik üç sınıf bilgi.
5. Makro: FOMC (federalreserve.gov) + PPK (tcmb.gov.tr) tarih listesi; CPI / istihdam / TÜİK EKSİK. Emtia: surucu.pkl (2015+), şok = |log getiri| >= 3 x geçmiş std.
6. Sektör haberi VERİ YOK; yerine 'rakip bilançosu' (sektörün çeyrekteki ilk bilanço günü).
7. ABD delist: veri yok (k34 de yaşayan). BIST delist: yalnız kapanış (BIST_K62).
8. Olay analizi tür başına en çok 50.000 hisse-olay (tohumlu rastgele; makro türleri çok büyük); plasebo P1 tür başına 3.000.
9. 'Süreye bağlı Markov' ayrı kurulmadı (kesikli yaş hazard'ı = süreye bağlı geçiş; bölüm 5).
10. BOŞLUK: BIST'te 2015 öncesi OHLC yok → BIST WF eğitimi 2016'dan; T1 / savunma hattı / mum ölçüleri BIST'te yalnız yaşayanlarla.
11. BOŞLUK: KAP özel durum açıklamaları indirilmedi (iş tanımı: gereksiz indirme yok); ana oturum isterse Faz 2 öncesi indirme kararı + SAPMA.
12. Grafikler matplotlib ister (Colab'da var; bu konteynerde yoksa `grafik` komutu durur ve nedeni yazar).
13. p değerleri bootstrap standart hatasıyla normal yaklaşım (bölüm 11); yüzdelik bootstrap p'sinin 1/B tabanı büyük ailelerde BH'yi işlemez kılardı.
14. ABD_SERMAYE'den 424B2 çıkarıldı (bankaların yapılandırılmış ürün / borç senedi akışı; pay arzı değil). FOMC güncel sayfasındaki '*' = projeksiyonlu
    toplantı (planlı); 'unscheduled' / 'cancelled' planlı değil; 'notation vote' toplantı sayılmaz. PPK 2009-2014 sayfaları alınamadı → EKSİK (BIST OHLC 2015-06'dan).
15. KOD_SHA256 kuralı: VDYT.py'nin her değişikliği (yorum dahil) `kos`u durdurur; ön kayıt sonrası düzeltme bu listeye tarihli SAPMA + yeni KOD_SHA256 ile işlenir.
16. Veri sha256'ları bu konteynerdeki /tmp dosyalarına bağlıdır (k60_fiyat Yahoo'dan yeniden inerse sha değişir → ret). Faz 2 aynı veriyle koşmalı; veri
    yenilenirse SAPMA + yeni veri satırları + kapsam yeniden.

## 18. Veri sha256 (ön kayıt anı; `kos` yeniden hesaplar, farklıysa ret)
{veri}

## 19. Kapsam (yalnız SAYI; `python -I VDYT.py kapsam`)
{kap}

## 20. Faz 2 komutları
1. (ana oturum) bu dosyayı ve VDYT.py'yi denetler, git'e işler.
2. `python -I VDYT.py kos --asama wf` → KEŞİF-WF ölçümü + rapor (mühür, kod, veri sha256 ve git doğrulanır; yoksa ret).
3. `python -I VDYT.py kos --asama kasa` → KASA bir kez açılır, final karar tablosu.
4. `python VDYT.py grafik --asama wf` (ve kasa), `python VDYT.py rapor --asama kasa`.

## 21. Değişmezlik
VDYT_ESIK, VDYT_OLAY_TUR, VDYT_EDGAR_FORM, VDYT_OZELLIK, VDYT_SURE_MODEL değişirse ESIK_SHA256 değişir; VDYT.py değişirse KOD_SHA256 tutmaz; veri değişirse veri
sha256 tutmaz → `kos` durur.
"""


def _vdyt_onkayit_oku(yol: str) -> Dict[str, Any]:
    with open(yol, encoding="utf-8") as f:
        m = f.read()
    a = re.search(r"^ESIK_SHA256: ([0-9a-f]{64})$", m, re.M); k = re.search(r"^KOD_SHA256: ([0-9a-f]{64})$", m, re.M)
    z = re.search(r"^Yazım zamanı: (.+)$", m, re.M)
    veri = {x: (h, int(n)) for x, h, n in re.findall(r"^- ([\w.\-]+): sha256 ([0-9a-f]{64}|YOK) \((\d+) dosya\)$", m, re.M)}
    return {"esik": a.group(1) if a else None, "kod": k.group(1) if k else None, "zaman": z.group(1) if z else "", "veri": veri}


def vdyt_onkayit(cikti: Optional[str] = None, kapsam: Optional[Dict[str, Any]] = None, veri_sha: Optional[Dict[str, Tuple[str, int]]] = None) -> str:
    """Ön kaydı yazar. Dosya varsa ÜZERİNE YAZMAZ (mühür ve kod aynıysa yolu döndürür, değilse durur). kapsam None ise vdyt_kapsam.json okunur."""
    yol = _vdyt_yol("onkayit", cikti)
    if os.path.exists(yol):
        oc = _vdyt_onkayit_oku(yol)
        if oc["esik"] != vdyt_esik_sha() or oc["kod"] != vdyt_kod_sha():
            raise VdytHata(f"ön kayıt zaten var ve mühür / kod farklı (esik {oc['esik']} / {vdyt_esik_sha()}, kod {oc['kod']} / {vdyt_kod_sha()}); üzerine yazılmadı")
        vdytlog.info("ön kayıt zaten var (mühür ve kod aynı): %s", yol); return yol
    if kapsam is None and os.path.exists(_vdyt_yol("kapsam", cikti)):
        kapsam = _vdyt_json_oku(_vdyt_yol("kapsam", cikti))
    simdi = _dt.datetime.now(_dt.timezone.utc)
    zaman = simdi.strftime("%Y-%m-%d %H:%M:%S UTC") + " (" + (simdi + _dt.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M TR") + ")"
    _vdyt_yaz(yol, vdyt_onkayit_metin(zaman, vdyt_veri_sha() if veri_sha is None else veri_sha, kapsam))
    vdytlog.info("ön kayıt yazıldı: %s (mühür %s, kod %s)", yol, vdyt_esik_sha()[:12], vdyt_kod_sha()[:12])
    return yol


def vdyt_onkayit_dogrula(cikti: Optional[str] = None, veri: bool = True, git: bool = True) -> Dict[str, Any]:
    """`kos` kapısı: ön kayıt var; eşik mührü ve VDYT.py sha256'sı ön kayıttakiyle aynı; (veri) veri sha256'ları aynı; (git) ön kayıt VE VDYT.py git'e
    işlenmiş ve sonra değişmemiş. Biri tutmazsa VdytHata (koşu REDDEDİLİR)."""
    yol = _vdyt_yol("onkayit", cikti)
    if not os.path.exists(yol):
        raise VdytHata(f"ön kayıt yok ({yol}): önce `python VDYT.py onkayit`; koşu REDDEDİLDİ")
    oc = _vdyt_onkayit_oku(yol)
    if oc["esik"] != vdyt_esik_sha():
        raise VdytHata(f"eşik mührü tutmuyor ({oc['esik']} != {vdyt_esik_sha()}): eşikler ön kayıttan sonra değişmiş; koşu REDDEDİLDİ")
    if oc["kod"] != vdyt_kod_sha():
        raise VdytHata(f"VDYT.py sha256 ön kayıttakiyle aynı değil ({oc['kod']} != {vdyt_kod_sha()}): kod değişmiş; SAPMA yazılıp ön kayıt yeniden işlenmeli; koşu REDDEDİLDİ")
    out = {"yol": yol, "esik": oc["esik"], "kod": oc["kod"], "zaman": oc["zaman"], "dosya_sha256": vdyt_sha_dosya(yol)}
    if veri:
        simdi = vdyt_veri_sha(); fark = sorted(k for k in set(simdi) | set(oc["veri"]) if tuple(simdi.get(k, ("", -1))) != tuple(oc["veri"].get(k, ("", -1))))
        if fark:
            raise VdytHata(f"veri ön kayıttakiyle aynı değil (sha256 / dosya sayısı): {fark}; koşu REDDEDİLDİ")
    if git:
        out["git_onkayit"] = vdyt_git_islenmis(yol, "VDYT ön kaydı"); out["git_kod"] = vdyt_git_islenmis(os.path.join(KOK_VDYT, "VDYT.py"), "VDYT.py")
    return out


# ---------------------------------------------------------------- 17) KOŞU (Faz 2), KARAR TABLOSU, RAPOR, GRAFİK
def _vdyt_kayit(x: Any) -> Any:
    if isinstance(x, pd.DataFrame):
        return json.loads(x.to_json(orient="records", date_format="iso", default_handler=str))
    if isinstance(x, dict):
        return {str(k): _vdyt_kayit(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_vdyt_kayit(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


def vdyt_karar_tablosu(wf: Dict[str, Any], kasa: Optional[Dict[str, Any]], E: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """Ana karar hücreleri: pazar x {Motor 1 (ana tanım, ana ufuk, M_TAM vs T1), Motor 2 (ana tanım, M_TAM vs B1)}. BASİTTEN İYİ ⇔ WF ve KASA'nın ikisinde
    Brier skill > 0 ve alt sınır > 0 (Motor 2'de ayrıca log loss skill ve dengeli doğruluk farkı aynı şartla)."""
    E = E or VDYT_ESIK; sat = []

    def bul(S: Optional[Dict[str, Any]], pazar: str, motor: str) -> Optional[Dict[str, Any]]:
        if not S or pazar not in S.get("pazar", {}):
            return None
        L = S["pazar"][pazar].get("motor1" if motor == "M1" else "motor2") or []
        for r in L:
            if motor == "M1" and r.get("kombo") == E["ana_tanim"] and r.get("ufuk") == int(E["ana_ufuk"]) and r.get("model") == "M_TAM" and r.get("temel") == "T1" and not r.get("katki"):
                return r
            if motor == "M2" and r.get("kombo") == E["ana_tanim"] and r.get("model") == "M_TAM" and r.get("temel") == "B1" and not r.get("katki") and not r.get("hipotez"):
                return r
        return None

    def gec(r: Optional[Dict[str, Any]], motor: str) -> Optional[bool]:
        if not r or r.get("brier_skill") is None:
            return None
        ok = (r.get("brier_skill", -1) or -1) > 0 and (r.get("brier_skill_alt", -1) or -1) > 0
        if motor == "M2":
            ok = ok and (r.get("logloss_skill", -1) or -1) > 0 and (r.get("logloss_skill_alt", -1) or -1) > 0 and (r.get("ba_fark", -1) or -1) > 0 \
                and (r.get("ba_fark_alt", -1) or -1) > 0
        return bool(ok)
    for pz in E["karar_pazari"]:
        for mt in ("M1", "M2"):
            a, b = bul(wf, pz, mt), bul(kasa, pz, mt); ga, gb = gec(a, mt), gec(b, mt)
            karar = "KASA AÇILMADI" if kasa is None else ("BASİTTEN İYİ" if ga and gb else ("VERİ YOK" if ga is None or gb is None else "BASİTTEN İYİ DEĞİL"))
            sat.append({"pazar": pz, "motor": "Motor 1 (genişleme)" if mt == "M1" else "Motor 2 (yön)", "wf": {k: (a or {}).get(k) for k in
                        ("n", "kume", "brier_skill", "brier_skill_alt", "brier_skill_ust", "logloss_skill", "logloss_skill_alt", "ba_fark", "ba_fark_alt")},
                        "kasa": {k: (b or {}).get(k) for k in ("n", "kume", "brier_skill", "brier_skill_alt", "brier_skill_ust", "logloss_skill",
                                                                 "logloss_skill_alt", "ba_fark", "ba_fark_alt")}, "wf_gecti": ga, "kasa_gecti": gb, "karar": karar})
    return sat


def vdyt_kos(asama: str = "wf", cikti: Optional[str] = None, isci: int = 2, git_sart: bool = True, veri_sart: bool = True, pazarlar: Optional[List[str]] = None,
             girdi: Optional[Dict[str, Tuple[Dict[str, Any], pd.DataFrame]]] = None, p1_tekrar: Optional[int] = None, E: Optional[Dict[str, Any]] = None
             ) -> Dict[str, Any]:
    """Faz 2 ölçümü. Önce vdyt_onkayit_dogrula (ret kapısı). 'kasa' yalnız 'wf' sonucu varken ve KASA daha önce açılmamışsa. girdi (sentetik test):
    {pazar: (F, Ev)}."""
    E = E or VDYT_ESIK; t0 = time.time(); bas = _vdyt_simdi()
    if asama not in ("wf", "kasa"):
        raise VdytHata(f"aşama 'wf' ya da 'kasa' olmalı: {asama}")
    oc = vdyt_onkayit_dogrula(cikti, veri=veri_sart, git=git_sart)
    wf_yol = _vdyt_yol(f"vdyt_sonuc_wf.json", cikti); ky = _vdyt_yol("kasa", cikti)
    if asama == "kasa":
        if not os.path.exists(wf_yol):
            raise VdytHata("KASA açılamaz: önce `kos --asama wf` bitmeli")
        if os.path.exists(ky):
            raise VdytHata(f"KASA zaten açılmış ({ky}); ikinci kez açılmaz")
        _vdyt_json(ky, {"acilis": bas, "onkayit": oc, "kod_sha256": vdyt_kod_sha()})
    pazarlar = pazarlar or (list(E["karar_pazari"]) + ["BIST_K62"]); sonuc: Dict[str, Any] = {"asama": asama, "baslangic": bas, "onkayit": oc, "pazar": {}}
    hata_rapor: Dict[str, Any] = {}
    for pz in pazarlar:
        try:
            F, Ev = (girdi or {}).get(pz, (None, None))
            Z = vdyt_pazar_isle(pz, "kos", E, isci, F, Ev, p2_tekrar=int(E["coklu"]["plasebo_bolge_tekrar"]) if (asama == "wf" and pz in E["karar_pazari"]) else 0)
            A = vdyt_analiz(Z, asama, E, os.path.join(VDYT_YOL["ara"], asama), p1_tekrar if pz in E["karar_pazari"] else 0)
            sonuc["pazar"][pz] = _vdyt_kayit({k: v for k, v in A.items()}); hata_rapor[pz] = {"hisse_hata": Z["hata"], "olay_notu": Z["ev_not"], "sure_sn": Z["sure_sn"]}
            del Z, A
        except VdytHata as ex:
            sonuc["pazar"][pz] = {"durum": f"EKSİK: {ex}"}; hata_rapor[pz] = {"durum": str(ex)}
    wf = _vdyt_json_oku(wf_yol) if asama == "kasa" else sonuc
    sonuc["karar"] = vdyt_karar_tablosu(wf, sonuc if asama == "kasa" else None, E)
    if asama == "kasa":
        sonuc["teyit"] = vdyt_teyit(wf, sonuc)
    sonuc["bitis"] = _vdyt_simdi(); sonuc["sure_sn"] = round(time.time() - t0, 1)
    _vdyt_json(_vdyt_yol(f"vdyt_sonuc_{asama}.json", cikti), sonuc)
    _vdyt_json(_vdyt_yol("meta", cikti), {"asama": asama, "baslangic": bas, "bitis": sonuc["bitis"], "sure_sn": sonuc["sure_sn"], "onkayit": oc,
                                           "hata": hata_rapor})
    vdyt_parametre_kaydi(cikti, {"komut": f"kos {asama}"}); vdyt_hata_raporu(hata_rapor, sonuc, cikti); sonuc["rapor"] = vdyt_rapor(asama, cikti)
    return sonuc


def vdyt_teyit(wf: Dict[str, Any], kasa: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Bölüm 12 kuralı: WF'de BH ile reddedilen her hipotez KASA'da aynı işaretle ve %95 aralığı 0'ı dışlayarak tekrar ederse TUTTU, yoksa TUTMADI."""
    sat = []
    for pz, P in (wf.get("pazar") or {}).items():
        K = {h["id"]: h for h in ((kasa.get("pazar") or {}).get(pz, {}).get("hipotez") or [])}
        for h in P.get("hipotez") or []:
            if not h.get("bh_ret"):
                continue
            k = K.get(h["id"]); n0 = h.get("nokta") or 0.0
            ok = bool(k and k.get("nokta") is not None and np.sign(k["nokta"]) == np.sign(n0) and (
                (n0 > 0 and (k.get("alt") or -1) > 0) or (n0 < 0 and (k.get("ust") or 1) < 0)))
            sat.append({"pazar": pz, "id": h["id"], "aile": h.get("aile"), "wf_nokta": n0, "wf_p": h.get("p"), "kasa_nokta": (k or {}).get("nokta"),
                        "kasa_alt": (k or {}).get("alt"), "kasa_ust": (k or {}).get("ust"), "sonuc": "TUTTU" if ok else "TUTMADI"})
    return sat


def vdyt_hata_raporu(H: Dict[str, Any], S: Dict[str, Any], cikti: Optional[str] = None) -> str:
    L = [f"# VDYT hata ve veri eksikliği raporu ({S.get('asama')})\n\nÜretim: {_vdyt_simdi()}. Veri eksikleri: VDYT_EKSIKLER.md.\n"]
    for pz, h in H.items():
        L.append(f"\n## {pz}\n- durum: {h.get('durum', 'tamam')}\n- hata veren hisse: {len(h.get('hisse_hata') or {})} {_j(h.get('hisse_hata'), 800)}\n"
                 f"- olay kaynak notları: {_j(h.get('olay_notu'), 1500)}\n")
    return _vdyt_yaz(_vdyt_yol("hata", cikti), "".join(L))


def _vdyt_md_tablo(rows: List[Dict[str, Any]], kol: List[str], n: int = 4) -> str:
    if not rows:
        return "(satır yok)\n"
    def f(x: Any) -> str:
        if isinstance(x, float):
            return _t(x, n) if np.isfinite(x) else "-"
        if isinstance(x, bool):
            return "EVET" if x else "hayır"
        return "-" if x is None else str(x)
    return "| " + " | ".join(kol) + " |\n|" + "---|" * len(kol) + "\n" + "".join("| " + " | ".join(f(r.get(k)) for k in kol) + " |\n" for r in rows)


def vdyt_rapor(asama: str = "wf", cikti: Optional[str] = None) -> str:
    """VDYT_RAPOR.md (aşama 'kasa' varsa final). Bölümler: karar, Motor 1, Motor 2, süre, olay, savunma, karşılaştırma, plasebo, portföy (bilgi), BH."""
    y = _vdyt_yol(f"vdyt_sonuc_{asama}.json", cikti)
    if not os.path.exists(y):
        return _vdyt_yaz(_vdyt_yol("rapor", cikti), f"# VDYT raporu\n\nÖlçüm yapılmadı ({asama} sonucu yok). Faz 2: `python -I VDYT.py kos --asama wf`.\n")
    S = _vdyt_json_oku(y)
    L = [f"# VDYT raporu — aşama {asama}\n\nKoşu {S.get('baslangic')} → {S.get('bitis')} ({S.get('sure_sn')} sn). Ön kayıt mührü {str(S.get('onkayit', {}).get('esik'))[:12]}, "
         f"kod {str(S.get('onkayit', {}).get('kod'))[:12]}, ön kayıt commit {str(S.get('onkayit', {}).get('git_onkayit', {}).get('commit'))[:7]}.\n"
         "VDYT sonucu doğrulanmış sinyal değildir; ilişki nedensellik değildir; yüksek genişleme olasılığı alım sinyali değildir.\n\n## 1. Karar tablosu (ana hücreler)\n"]
    L.append(_vdyt_md_tablo([{"pazar": r["pazar"], "motor": r["motor"], "WF skill": (r["wf"] or {}).get("brier_skill"), "WF alt": (r["wf"] or {}).get("brier_skill_alt"),
                              "KASA skill": (r["kasa"] or {}).get("brier_skill"), "KASA alt": (r["kasa"] or {}).get("brier_skill_alt"),
                              "WF BA farkı": (r["wf"] or {}).get("ba_fark"), "karar": r["karar"]} for r in S.get("karar", [])],
                            ["pazar", "motor", "WF skill", "WF alt", "KASA skill", "KASA alt", "WF BA farkı", "karar"]))
    if asama == "kasa":
        L.append("\n## 2. WF'de BH ile reddedilen hipotezlerin KASA teyidi\n" + _vdyt_md_tablo(S.get("teyit") or [], ["pazar", "id", "wf_nokta", "wf_p", "kasa_nokta",
                                                                                                          "kasa_alt", "kasa_ust", "sonuc"]))
    for pz, P in S.get("pazar", {}).items():
        if "durum" in P:
            L.append(f"\n## {pz}\n{P['durum']}\n"); continue
        L.append(f"\n## {pz}\n\n### Süre (KM / CIF / hazard)\n" + _vdyt_md_tablo(P.get("sure") or [], ["kombo", "bolge", "medyan_sure", "cif_gen_20", "cif_gen_60",
                                                                                                   "cif_gen_120", "hazard_10_19", "hazard_20_39", "hazard_60_89",
                                                                                                   "hazard_rejim0", "hazard_rejim2"]))
        m1 = [r for r in (P.get("motor1") or []) if not r.get("katki")]
        L.append("\n### Motor 1 — genişleme (WF test toplamı; skill = 1 - Brier / Brier_temel)\n" + _vdyt_md_tablo(
            m1, ["kombo", "ufuk", "model", "temel", "n", "kume", "brier_skill", "brier_skill_alt", "brier_skill_ust", "logloss_skill", "ece", "y_ort",
                 "kesinlik_ust10", "duyarlilik_ust10"]))
        L.append("\n### Motor 1 — grup katkısı (M_TAM vs grubu çıkarılmış)\n" + _vdyt_md_tablo([r for r in (P.get("motor1") or []) if r.get("katki")],
                                                                                                ["katki", "brier_skill", "brier_skill_alt", "brier_skill_ust"]))
        L.append("\n### Motor 2 — yön\n" + _vdyt_md_tablo(P.get("motor2") or [], ["kombo", "temel", "katki", "hipotez", "n", "brier_skill", "brier_skill_alt",
                                                                                  "logloss_skill", "logloss_skill_alt", "ba_m", "ba_0", "ba_fark", "ba_fark_alt"]))
        H = P.get("hipotez") or []
        for aile in ("F3_HAT", "F4_KARSILASTIRMA", "F2_OLAY", "F5_SURE"):
            Hs = [h for h in H if h.get("aile") == aile]
            if aile == "F2_OLAY":
                Hs = sorted(Hs, key=lambda h: (h.get("p") if h.get("p") is not None else 9))[:40]
            L.append(f"\n### {aile} (BH q = {VDYT_ESIK['coklu']['bh_q']}){' — en küçük 40 p' if aile == 'F2_OLAY' else ''}\n"
                     + _vdyt_md_tablo(Hs, ["id", "nokta", "alt", "ust", "p", "bh_ret", "n1", "n0", "beklenen_isaret"]))
        if P.get("plasebo_olay"):
            po = P["plasebo_olay"]
            L.append(f"\n### Plasebo P1 (rastgele olay günü)\n{len(po)} tekrar; en az bir BH keşfi olan tekrar payı "
                     f"{_t(np.mean([r['kesif'] > 0 for r in po]), 3)}; ortalama keşif {_t(np.mean([r['kesif'] for r in po]), 2)} / {_t(np.mean([r['test'] for r in po]), 0)} test.\n")
        if P.get("plasebo_bolge"):
            L.append("\n### Plasebo P2 (rastgele bölge; Motor 1 ana hücre)\n" + _vdyt_md_tablo(P["plasebo_bolge"], ["tekrar", "n", "brier_skill", "brier_skill_alt"]))
        if P.get("birlesik"):
            L.append(f"\n### Birleşik üç sınıf (bilgi)\n{_j(P['birlesik'], 400)}\n")
        if P.get("portfoy"):
            L.append(f"\n### Basit portföy (YALNIZ BİLGİ; doğrulanmış sinyal değil)\n{_j(P['portfoy'], 400)}\n")
    return _vdyt_yaz(_vdyt_yol("rapor", cikti), "".join(L))


def vdyt_mum_ciz(ax: Any, d: pd.DataFrame, x0: int) -> None:
    """Mum çizimi (gövde + fitil; yeşil yükselen, kırmızı düşen); x = bar indeksi."""
    from matplotlib.patches import Rectangle
    for i, r in enumerate(d.itertuples()):
        x = x0 + i; yuk = r.c >= r.o; renk = "#1a9850" if yuk else "#d73027"
        ax.vlines(x, r.l, r.h, color=renk, linewidth=0.8)
        ax.add_patch(Rectangle((x - 0.3, min(r.o, r.c)), 0.6, max(abs(r.c - r.o), 1e-9), facecolor=renk, edgecolor=renk))


def vdyt_grafik_ciz(d: pd.DataFrame, b: Dict[str, Any], t: int, hat: float, olaylar: List[int], yol: str, sadece_gecmis: bool, baslik: str,
                    E: Optional[Dict[str, Any]] = None) -> str:
    """Bir örneğin grafiği: mum + hacim paneli, sıkışma alanı, savunma hattı, olay günleri, genişleme başlangıcı ve yön. sadece_gecmis=True ise yalnız
    karar günü t'ye kadarki mumlar (sinyal günü grafiği; gelecek gösterilmez)."""
    E = E or VDYT_ESIK; Gr = E["grafik"]
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as ex:
        raise VdytHata(f"grafik için matplotlib gerekli ({ex}); Colab'da kurulu, burada `pip install matplotlib`")
    a = max(0, int(b["bas"]) - int(Gr["on_bar"])); son = int(t) if sadece_gecmis else min(len(d) - 1, int(b["bit"]) + int(Gr["son_bar"]))
    X = d.iloc[a: son + 1]
    fig, (ax, av) = plt.subplots(2, 1, figsize=(12, 6.5), sharex=True, gridspec_kw={"height_ratios": [3.2, 1]})
    vdyt_mum_ciz(ax, X, a)
    ax.axvspan(int(b["bas"]) - 0.5, min(int(b["bit"]) if not sadece_gecmis else int(t), son) + 0.5, color="#4575b4", alpha=0.08, label="sıkışma")
    if np.isfinite(hat):
        ax.hlines(hat, int(b["bas"]), min(int(t), son), color="#542788", linestyle="--", linewidth=1.2, label="savunma hattı (t'ye kadar)")
    for g in olaylar:
        if a <= g <= son:
            ax.axvline(g, color="#fdae61", linestyle=":", linewidth=1.2)
    ax.axvline(int(t), color="black", linewidth=0.8, alpha=0.6, label="karar günü")
    if not sadece_gecmis and int(b.get("gen_bas", -1)) >= 0:
        gb = int(b["gen_bas"]); ax.axvline(gb, color="#d73027" if b.get("Y1") == -1 else "#1a9850", linewidth=1.5, label="genişleme başlangıcı")
        yon = {1.0: "YUKARI", -1.0: "AŞAĞI", 0.0: "BELİRSİZ"}.get(b.get("Y1"), "?"); ax.annotate(yon, (gb, float(X.h.max())), fontsize=10, color="black")
    av.bar(np.arange(a, son + 1), X.v.to_numpy(), color=["#1a9850" if c >= o else "#d73027" for c, o in zip(X.c, X.o)], width=0.7)
    ax.set_title(baslik, fontsize=10); ax.legend(loc="upper left", fontsize=7); av.set_ylabel("hacim", fontsize=8)
    tick = np.linspace(a, son, min(8, son - a + 1)).astype(int); av.set_xticks(tick); av.set_xticklabels([str(d.index[i].date()) for i in tick], fontsize=7, rotation=20)
    os.makedirs(os.path.dirname(yol), exist_ok=True); fig.tight_layout(); fig.savefig(yol, dpi=int(Gr["dpi"])); plt.close(fig)
    return yol


def vdyt_grafik(asama: str = "wf", cikti: Optional[str] = None, pazarlar: Optional[List[str]] = None, E: Optional[Dict[str, Any]] = None,
                F_ver: Optional[Dict[str, Dict[str, Any]]] = None) -> List[str]:
    """Önceden tanımlı kuralla örnek seçimi (bölüm 13) ve çizim. Girdi: /tmp/vdyt/<aşama>/ tahmin, karar, bölge, olay eşleme tabloları."""
    E = E or VDYT_ESIK; ara = os.path.join(VDYT_YOL["ara"], asama); an = E["ana_tanim"]; hh = int(E["ana_ufuk"]); yazilan = []
    _bas, son, _y = _vdyt_donem(asama, E); ts = pd.Timestamp(son)
    for pz in pazarlar or list(E["karar_pazari"]):
        yk, yp, yb = (os.path.join(ara, f) for f in (f"karar_{pz}_{an}.csv.gz", f"tahmin_m1_{pz}_{an}_y{hh}.csv.gz", f"bolge_{pz}_{an}.csv.gz"))
        if not all(os.path.exists(x) for x in (yk, yp, yb)):
            vdytlog.warning("%s: grafik girdisi yok (önce kos)", pz); continue
        Kd = pd.read_csv(yk, parse_dates=["tarih", "y1_son"]); Pd = pd.read_csv(yp, parse_dates=["tarih"]); Bd = pd.read_csv(yb, parse_dates=["bas_tarih", "bit_tarih", "y1_son"])
        yo = os.path.join(ara, f"olay_eslesme_{pz}_{an}.csv.gz"); Od = pd.read_csv(yo, parse_dates=["olay_tarih"]) if os.path.exists(yo) else pd.DataFrame()
        F = (F_ver or {}).get(pz) or vdyt_fiyat_yukle(pz, E)
        P1 = Pd.merge(Kd[["satir", "bolge"]], on="satir", how="left")
        son_dp = Kd[Kd.Y1.isin([1, -1]) & (Kd.y1_son <= ts)].sort_values("yas").groupby(["sembol", "bolge"]).tail(1)
        Bg = Bd.assign(bolge=Bd.groupby("sembol").cumcount())
        Bg = Bg[(Bg.bit_tur == BITIS_GEN) & Bg.uygun.astype(bool) & (Bg.y1_son <= ts)]
        gruplar = {"BASARILI": P1[(P1.p_M_TAM >= P1.esik90_M_TAM) & (P1.y == 1)][["sembol", "bolge", "satir"]],
                   "BASARISIZ": P1[(P1.p_M_TAM >= P1.esik90_M_TAM) & (P1.y == 0)][["sembol", "bolge", "satir"]],
                   "HABERLI": Bg[Bg.haberli == 1][["sembol", "bolge"]], "HABERSIZ": Bg[Bg.habersiz == 1][["sembol", "bolge"]],
                   "HATLI": son_dp[son_dp.sv_hat_var == 1][["sembol", "bolge", "satir"]], "HATSIZ": son_dp[son_dp.sv_hat_var == 0][["sembol", "bolge", "satir"]]}
        for g, A in gruplar.items():
            A = A.sort_values(["sembol", "bolge"]).reset_index(drop=True)
            if not len(A):
                continue
            rng = np.random.default_rng(_vdyt_tohum(E["grafik"]["tohum"], pz, g)); sec = np.sort(rng.choice(len(A), size=min(int(E["grafik"]["grup_n"]), len(A)), replace=False))
            for j, i in enumerate(sec):
                r = A.iloc[i]; s = r.sembol; d = F["S"].get(s)
                if d is None:
                    continue
                b = Bd[Bd.sembol == s].reset_index(drop=True).iloc[int(r.bolge)].to_dict()
                if "satir" in A and pd.notna(r.get("satir")):
                    k = Kd[Kd.satir == int(r.satir)].iloc[0]
                else:
                    kk = Kd[(Kd.sembol == s) & (Kd.bolge == int(r.bolge))].sort_values("yas"); k = kk.iloc[-1] if len(kk) else None
                t = int(k.t) if k is not None else int(b["tespit"]); hat = float(k.sv_seviye) if k is not None and pd.notna(k.sv_seviye) else np.nan
                og = [int(x) for x in np.searchsorted(d.index, Od[(Od.sembol == s) & (Od.bolge == int(r.bolge))].olay_tarih.values)] if len(Od) else []
                for gecmis in (False, True):
                    ad = f"{pz}_{g}_{j + 1}_{s}_{'sinyal' if gecmis else 'tam'}.png"
                    yazilan.append(vdyt_grafik_ciz(d, b, t, hat, [x for x in og if (not gecmis) or x <= t], os.path.join(_vdyt_yol("grafik", cikti), asama, ad), gecmis,
                                                   f"{pz} {g} #{j + 1} — karar günü {d.index[t].date()} (yaş {t - int(b['bas']) + 1})"
                                                   + (" — YALNIZ O GÜNE KADARKİ MUMLAR" if gecmis else ""), E))
    return yazilan


def _cakisma_kontrol_vdyt(_once=_CK_ONCE_VDYT, _dosya="VDYT.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_VDYT", "_CK_KAYIT", "_cakisma_kontrol_vdyt", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "time", "re", "pickle", "hashlib", "glob", "gzip", "subprocess", "_dt", "_html", "annotations",
           "Any", "Callable", "Dict", "List", "Optional", "Tuple")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_vdyt()

if __name__ == "__main__" and "get_ipython" not in globals():
    import argparse
    ap = argparse.ArgumentParser(description=VDYT_SURUM)
    ap.add_argument("komut", choices=["envanter", "makro", "kapsam", "onkayit", "kos", "grafik", "rapor"])
    ap.add_argument("--asama", default="wf", choices=["wf", "kasa"])
    ap.add_argument("--cikti", default=None)
    ap.add_argument("--isci", type=int, default=2)
    ap.add_argument("--pazar", action="append", default=None)
    a_ = ap.parse_args()
    try:
        if a_.komut == "envanter":
            vdyt_envanter(a_.cikti); print(_vdyt_yol("envanter", a_.cikti)); print(_vdyt_yol("eksik", a_.cikti))
        elif a_.komut == "makro":
            M_ = vdyt_makro_indir(); print(VDYT_YOL["makro"], "FOMC", len(M_["FOMC"]), "PPK", len(M_["PPK"]), "eksik sayfa", len(M_["EKSIK"]["sayfa"]))
        elif a_.komut == "kapsam":
            vdyt_kapsam(a_.pazar, a_.cikti, a_.isci); print(_vdyt_yol("kapsam_md", a_.cikti))
        elif a_.komut == "onkayit":
            y_ = vdyt_onkayit(a_.cikti); print(y_, "mühür", vdyt_esik_sha(), "kod", vdyt_kod_sha(), "dosya sha256", vdyt_sha_dosya(y_))
        elif a_.komut == "kos":
            R_ = vdyt_kos(a_.asama, a_.cikti, a_.isci, pazarlar=a_.pazar)
            print(json.dumps(R_["karar"], ensure_ascii=False, default=str, indent=1)); print(R_["rapor"])
        elif a_.komut == "grafik":
            print("\n".join(vdyt_grafik(a_.asama, a_.cikti, a_.pazar)))
        else:
            print(vdyt_rapor(a_.asama, a_.cikti))
    except (VdytHata, FileNotFoundError) as ex:
        vdytlog.error("%s", ex); sys.exit(1)
