"""MACD_UYUM — K47 MACD POZİTİF UYUMSUZLUK, TEK BAŞINA VE DİPTE (24 Kasım 2026; iş tanımı: ana model mesajı).

Cemal (24 Kas 2026): "test et, bu uyumsuzluğun getirisi ne". Örnek grafik DGXX: fiyat 120 günün dibinde ikinci dip yaptı; MACD (12, 26, 9) ilk
dipten yukarıda ve sinyal çizgisinin üstüne geçti; RSI ilk dipte 30'un altındaydı, şimdi daha yukarıda.
Önceki ölçüm (YAPI_HEDEF 8. tur, RAPOR_8.md): Ş10 yalnız Y1 taban kırılımı olaylarının İÇİNDE ölçüldü (karar hücreleri ÖLÇÜLEMEDİ, n < 1.000).
Bu iş AYNI Ş10 tanımını Y1 şartı OLMADAN, dipte ölçer.

TANIM (MU_ESIK; sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
  Geçerli bar YH._yh_hazir (= GOZ_ETIKET.ge_hazir: H > L, V > 0, O/H/L/C > 0). MACD / dipler / F65 / F66 / F68 = YAPI_HEDEF 8. tur AYNEN (YH_ESIK8,
  yh_s10_bar; vektör sürüm mu_s10_vektor, yh_s10_bar ile birebir eşitlik denetimi). DİPTE: Low(L2) <= min Low[L2-120 .. L2-1] x 1,01 VE
  Close(L2) <= 0,80 x max High[L2-120 .. L2]. Olay günü t: L2(t) için şartların İLK tuttuğu gün, t <= L2 + 20; her L2 en çok bir olay; aynı
  hissede olaylar arası >= 15 bar. U1 (ANA) = Ş10 VE F68 VE DİPTE; U0 (KONTROL) = F65 VE DİPTE VE NOT F66 VE F68; bilgi: U1b, U2 (RSI), U3, U1d.
ÖLÇÜ
  ANA: CETVEL2 v2.2 R15 (c2_olc22 ufuk 15, konum eşli fark, bütün evren havuzu); hücre hükmü KART_TUR2 ön kaydı (3) HÜCRE TUTAR kuralı + güç
  (cetvel2_guc_v2.2.json) -> TUTAR / TUTMADI / ÖLÇÜLEMEDİ. R30 bilgi. İKİNCİL: YAPI_HEDEF 1. tur 15 bar cetveli (h5 / h10 / stop, KAT5, konum
  eşli KAT, plasebo KAT5), stop0 = Low(L2) x 0,98. Hücreler ABD / AVR x d1619 / d2022 (KARAR), BIST (BİLGİ). Veri YALNIZ KASA açık kesik
  (2022-12-31): /tmp/veri -> /tmp/kasa/acik; her koşudan önce KASA.kasa_kapisi.

Komut:  python MACD_UYUM.py esitlik            yh_s10_bar eşitliği (getirisiz; DURUR)
        python MACD_UYUM.py onkayit [--uzerine] olaylar + huni + eşitlik + güç beklentisi -> UYUM_ON_KAYIT.md (getirisiz)
        python MACD_UYUM.py kos                 kapı -> ölçüm -> prefix -> satır dosyası, sonuc.json, UYUM_RAPOR.md
        python MACD_UYUM.py rapor               sonuc.json -> UYUM_RAPOR.md
        python MACD_UYUM.py sha                 kod / eşik / veri sha'ları
Colab:  exec(open('MACD_UYUM.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Veri:   /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (KASA açık kısım). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı).
YAPI_HEDEF / CETVEL2 / ORTAK_CETVEL / POZITIF_KONTROL / KASA / FON_IZI DEĞİŞTİRİLMEZ; içe alınır.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MU = {k: id(v) for k, v in globals().items()}

import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv  # noqa: E402

KOK_MU = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MU not in sys.path:
    sys.path.insert(0, KOK_MU)

import CETVEL2 as C2  # noqa: E402
import KASA as KS  # noqa: E402
import ORTAK_CETVEL as OC  # noqa: E402
import POZITIF_KONTROL as PK  # noqa: E402
import YAPI_HEDEF as YH  # noqa: E402

mulog = logging.getLogger("col.macd_uyum")
if not mulog.handlers:
    _mu_h = logging.StreamHandler(sys.stderr)
    _mu_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s macd_uyum: %(message)s", "%H:%M:%S"))
    mulog.addHandler(_mu_h)
    mulog.setLevel(logging.INFO)
    mulog.propagate = False

MU_SURUM = "MACD_UYUM v1.0 (2026-11-24): K47 MACD pozitif uyumsuzluk tek başına ve DİPTE; CETVEL2 v2.2 R15 + 1. tur 15 bar cetveli; açık veri"
MU_YOL = {"cikti": os.path.join(KOK_MU, "arastirma_cikti", "macd_uyum"), "veri": os.environ.get("MU_VERI", "/tmp/veri"),
          "kod": os.path.join(KOK_MU, "MACD_UYUM.py"), "kasa": os.environ.get("KASA_DIZIN", "/tmp/kasa")}
MU_DOSYA = {"onkayit": "UYUM_ON_KAYIT.md", "rapor": "UYUM_RAPOR.md", "satir": "uyum_satir.csv.gz", "sonuc": "sonuc.json",
            "olay": "uyum_olay.csv.gz", "huni": "uyum_huni.json", "esitlik": "uyum_esitlik.json", "prefix": "uyum_prefix.json"}
MU_PAZAR = ["ABD", "AVR", "BIST"]
MU_KARAR_PAZAR = ["ABD", "AVR"]
MU_DONEM = {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]}
MU_HIP = ["U1", "U0", "U1b", "U2", "U3", "U1d"]
MU_BILGI = ["U1b", "U2", "U3", "U1d"]
MU_BAGIMLI = ["YAPI_HEDEF.py", "CETVEL2.py", "ORTAK_CETVEL.py", "POZITIF_KONTROL.py", "DUSUS_SONRASI.py", "KASA.py", "FON_IZI.py",
              "SIKISMA_YENIDEN.py", "IZ_KARNE.py"]

_KT2_HUCRE = ("(3) HÜCRE TUTAR (beklenen yön +; − ise işaretler ters): n >= 30; ortalama FARK > 0 ve ay kümeli bootstrap (B 2000) alt ucu > 0; "
              "ortalama SIRA > 0,50 ve onun da boot alt ucu > 0,50; L3O (en iyi 3 ay çıkınca) FARK > 0; PLASEBO KAPISI (hücre, 200 tohum rastgele "
              "etiket: |ortalama FARK| < 0,5 puan ve yön başına tutar payı <= %7). [KART_TUR2_ON_KAYIT.md bölüm 1, ANA MODEL KARARI (3), AYNEN] "
              "+ GÜÇ: 'Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural)' ve 'ÖLÇÜLEMEDİ <=> bir karar hücresi GÜÇLÜ değil; "
              "GÜÇLÜ(c) = n >= 30 VE güç >= 0,80' [KART_TUR2_ON_KAYIT.md bölüm 5 ve 8, AYNEN]")

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
MU_ESIK: Dict[str, Any] = {
    "surum": "MU-1.0",
    "is": "K47 MACD POZİTİF UYUMSUZLUK, TEK BAŞINA VE DİPTE (Cemal 24 Kas 2026: 'test et, bu uyumsuzluğun getirisi ne'); örnek DGXX (hüküm yok)",
    "gecerli_bar": "YH._yh_hazir (= GOZ_ETIKET.ge_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0 ve sonlu, kriz kesiği); göstergeler "
                   "kapanıştan, YALNIZ t'ye kadar olan geçerli barlarla",
    "s10": "MACD, dipler, F65, F66, F68: YAPI_HEDEF 8. tur AYNEN (YH_ESIK8 sha ön kayıtta; yh_s10_bar; ON_KAYIT_8 uygulama yorumları 1-6). Dipler "
           "[t-60, t-1], k in [t-55, t-6]; sol komşular katı küçük, sağ komşular eşit izinli; L1 = L2'den en az 8 bar önceki en yakın dip. "
           "Vektör sürüm mu_s10_vektor (pandas ewm adjust=False özyinelemesinin aynısı); pazar başına >= 100 barda yh_s10_bar ile birebir",
    "dipte": {"geri": 120, "dip_tol": 0.01, "tepe_pay": 0.80,
              "tanim": "DİPTE(L2) <=> L2 - 120 >= 0 VE Low(L2) <= min(Low[L2-120 .. L2-1]) x 1,01 VE Close(L2) <= 0,80 x max(High[L2-120 .. L2]) "
                       "(geçerli bar sırası); L2 - 120 seri başından önceyse olay yok"},
    "olay": {"taze_azami": 20, "ara": 15,
             "tanim": "t günü yh_s10_bar kuralıyla bulunan L2(t) için şartların İLK kez tuttuğu gün; t <= L2 + 20 (değilse olay yok); her L2 en çok "
                      "bir olay (hipotez başına); aynı hissede iki olay arası >= 15 geçerli bar (t sırasıyla ilki kalır)"},
    "stop_carpan": 0.98,
    "stop": "STOP = Low(L2) x 0,98 (8. turdaki 'hat x 0,98' mantığı); giriş açılışı stopun altında ya da eşitse olay STOP sayılır (sayısı yazılır)",
    "giris": "t+1 açılış = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla; CETVEL2 E0)",
    "hipotez": {
        "U1": "ANA: Ş10 (F65 VE F66) VE F68 (MACD > sinyal) VE DİPTE, olay günü kuralıyla",
        "U0": "KONTROL (K1 mekanik etki): F65 VE DİPTE VE NOT F66 (s66 = 0) VE F68, aynı olay günü kuralıyla (dipte aynı çift dip, MACD uyumsuzluğu yok)",
        "U1b": "BİLGİ: Ş10 VE F68, DİPTE şartı yok, olay günü kuralıyla",
        "U2": "BİLGİ: RSI(14, Wilder) uyumsuzluğu: F65 VE RSI(L2) > RSI(L1) VE RSI(L1) < 30 VE DİPTE; t = L2 + 6 (L1 / F65 t'de)",
        "U3": "BİLGİ: U1 VE U2, aynı L2'de (olay günü U1'in günü)",
        "U1d": "BİLGİ (yalnız ABD, DGXX benzeri): U1 VE olay günü ATR%14 o günün en oynak %20'sinde VE Close(t) < 5 $ VE Close(L2) <= 0,50 x "
               "max(High[L2-120 .. L2])"},
    "u2": {"rsi_n": 14, "rsi_esik": 30.0, "t_kayma": 6, "rsi": "FON_IZI._fi_k38b_rsi (ewm alpha 1/14, adjust False, min_periods 14; repodaki hazır "
                                                                "uygulama), serinin başından t'ye kadar geçerli kapanışlar (nedensel)"},
    "u1d": {"pazar": "ABD", "atrp_gun": 14, "atrp_ust_pay": 0.20, "fiyat_ust": 5.0, "tepe_pay": 0.50,
            "atrp": "POZITIF_KONTROL.pk_seri ATRP (CETVEL2 kovası ile aynı: ort TR 14 / C); 'en oynak %20' <=> ATRP(t) >= o gün geçerli barı ve sonlu "
                    "ATRP'si olan bütün ABD açık evren hisselerinin ATRP %80 niceli (numpy quantile, doğrusal)"},
    "olcu": {"ana": "CETVEL2 v2.2 R15: C2.c2_olc22(ufuk 15, donem = d1619 / d2022, plasebo ayrı çağrıyla, bilgi yok); hipotez başına AYRI çağrı "
                    "(eş dışı küme = aynı hipotezin o günkü olayları); R15 = 15. geçerli bar kapanışı / E0 - 1 (stop yok)",
             "ufuk": 15, "bilgi_ufuk": 30, "donem": MU_DONEM, "karar_pazar": MU_KARAR_PAZAR, "bilgi_pazar": ["BIST"], "tekil_gun": 15,
             "r30": "BİLGİ: c2_olc22 ufuk 30 (CETVEL2 v2.2 tanımı AYNEN: tekil 30, plasebo yok); yalnız n / FARK [boot]",
             "getiri": "r15 = R15 (t+1 açılış -> 15. geçerli bar kapanışı); olay ve eş (olay başına eş ortalaması) için ortalama ve medyan; olay - eş "
                       "farkı (= FARK). Takip stoplu getiri: YH.yh_getiri (repoda hazır, yh_olay_olc 'getiri'; yalnız olay; bilgi)"},
    "hucre_kurali": _KT2_HUCRE,
    "hucre": {"n_min": 30, "sira": 0.50, "sira_boot_alt": 0.50, "guc_esik": 0.80,
              "sira_boot": {"B": 2000, "tohum": 2471, "alt": 0.025, "ust": 0.975,
                            "yontem": "KART_TUR2.k2_stat ile aynı: giriş ayı kümeleri, multinomial ağırlık, ort SIRA = W @ ay toplamı / W @ ay sayısı"},
              "plasebo": {"fark_mutlak": 0.005, "tutar_pay": 0.07, "tohum_sayi": 200},
              "hukum": "ÖLÇÜLEMEDİ <=> n < 30 ya da güç < 0,80 (cetvel2_guc_v2.2.json pazar x d1619 / d2022 x H 15, delta +0,02); TUTAR <=> güç "
                       "yeterli VE FARK > 0 VE FARK boot %95 alt > 0 VE SIRA > 0,50 VE SIRA boot %95 alt > 0,50 VE L3O > 0 VE plasebo kapısı "
                       "geçer; TUTMADI <=> güç yeterli ama TUTAR değil (nedeni yazılır)"},
    "karar_kurali": (
        "AÇIK VERİDE TUTTU <=> 4 karar hücresinin (ABD / AVR x 2016-19 / 2020-22) hepsinde U1 R15 hükmü TUTAR VE (U1 - U0) R15 farkı 4 hücrenin "
        "hepsinde > 0. Bu durumda sonraki adım yalnız öneri olarak yazılır: KASA 2023-24 kör sınaması (Cemal kararı). TUTMADI <=> gücü yeterli "
        "hücrelerde tutmuyor (CETVEL2 kuralı). ÖLÇÜLEMEDİ <=> güç yetersiz. Yön hücreden hücreye değişiyorsa ÇELİŞKİLİ. Bilgi varyantlarında hüküm "
        "yok. Aile içi BH ile q < 0,10 olanlar 'bilgi: dikkat' diye yazılır. Hayatta kalma (K7): evren yalnız bugün işlem görenlerse bu raporda "
        "yazılır; dipteki olaylarda sonuç YUKARI yanlıdır."),
    "karar_islem": "sıra: (1) TUTTU (yukarıdaki); (2) ÇELİŞKİLİ <=> bir karar hücresinde U1 FARK boot %95 aralığı tümüyle > 0 VE bir başkasında "
                   "tümüyle < 0 (CETVEL2 c2_etiket ÇELİŞKİLİ ölçütü, dört hücreye); (3) TUTMADI <=> gücü yeterli (n >= 30 VE güç >= 0,80) bir karar "
                   "hücresinde U1 hükmü TUTMADI, ya da dört hücrede U1 TUTAR iken U0'ı ölçülebilir (n >= 30) bir hücrede U1 - U0 <= 0; (4) "
                   "ÖLÇÜLEMEDİ <=> geri kalan (gücü yeterli hücreler tutuyor ama en az bir karar hücresinde güç yetersiz ya da U0 ölçülemedi)",
    "ikincil": {"tanim": "YAPI_HEDEF 1. tur 15 bar cetveli AYNEN: OC.oc_olay_hazirla (tekil 15 = ana ölçüyle aynı olay kümesi) -> YH.yh_olay_olc "
                         "(eş: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d = 1 - stop0 / E0, aynı hedef / takip / 15 bar; taban; "
                         "plasebo aynı hisse rastgele gün) -> YH.yh_konum_es_olc (F15 = panel F15[d, j] = t değeri) -> YH.yh_hucre / "
                         "yh_hucre_konum; h5 = 15 geçerli barda kapanış +%5 stop'tan önce, h10 = +%10, stop payı st5; KAT5 [%95] ay kümeli",
                "deneme_no": {"U1": 901, "U0": 902, "U1b": 903, "U2": 904, "U3": 905, "U1d": 906},
                "giris_stop_alti": "E0 <= stop0 (yh_olay_olc 'giris_stop_otesi'): KAT5 / konum KAT / plasebo 1. tur gibi DIŞINDA; olay payı "
                                   "tablosunda STOP sayılır (h5 = 0, h10 = 0, stop = 1) ve sayısı yazılır; R15'te stop yok (olay ölçülür)"},
    "fark_u1_u0": {"B": 2000, "tohum": 2474, "tanim": "FARK(U1) - FARK(U0) aynı pazar x hücre; boot %95 iki grubun giriş ayları bağımsız "
                                                       "yeniden örneklenir (bilgi; karar yalnız nokta değerle)"},
    "bh": {"q": 0.10, "aile": "U1b, U2, U3, U1d x karar pazarları (ABD, AVR; U1d yalnız ABD) x d1619 / d2022, n >= 30; p = c2_hucre ay kümeli "
                              "işaret permütasyonu (tek yönlü +); BH geçen = 'bilgi: dikkat'"},
    "esitlik": {"n_rastgele": 50, "n_aday": 50, "n_olay": 50, "tohum": 2472,
                "tanim": "pazar başına 150 bar: 50 rastgele bar, 50 rastgele aday gün (L1 / L2 var VE ham F65), 50 rastgele olay günü (herhangi "
                         "hipotez); 10 çıktı (F65, F66, F66m, F66h, F67, F68, tL2, s65, s66, S10) mu_s10_vektor = yh_s10_bar BİREBİR (tam eşit; "
                         "NaN = NaN); değilse DURUR"},
    "prefix": {"n": 30, "tohum": 2473,
               "tanim": "koşuda pazar başına 30 rastgele olay (satır dosyası): hissenin verisi t'de kesilir, olay taraması kesik seriyle yeniden "
                        "yapılır; aynı (hipotez, t) olayı aynı L1 / L2 ve aynı bayraklarla (F65-F68, s65, s66, S10, DİPTE, RSI, ATRP) çıkmalı; "
                        "değilse DURUR"},
    "k34": "BİLGİ: batanlar dahil ABD (k34_yahoo.pkl açık kısım 2020-10-01 .. 2022-12-30) yalnız d2022 hücresinin bir bölümünü kapsar; ana koşu "
           "bittikten sonra süre kalırsa koşulur (U1 / U0 R15, bilgi); koşulmazsa raporda 'uygulanmadı' yazılır",
    "uygulama_yorumlari": [
        "(1) Hücre kuralı KART_TUR2 ön kaydı (3) AYNEN; güç eğrisi CETVEL2 v2.2'nin kendi eğrisi (cetvel2_guc_v2.2.json, pazar x d1619 / d2022 x "
        "H 15, delta +0,02, %80): ana ölçü c2_olc22 bütün evren havuzunda, KART_TUR2'nin P2 / +1 puan / d1-d3 eğrisi bu hücrelerle örtüşmüyor. "
        "Tek bakış (açık veri): boot %95 (KART_TUR2 %98,33 yalnız KASA üç bakışında).",
        "(2) Plasebo kapısı CETVEL2.c2_plasebo ile (200 tohum, aynı giriş günü havuzdan rastgele hisse, eş dışı = çekilen küme, iki yön ayrı); GEÇER "
        "<=> |ort FARK| < 0,005 VE + yönde TUTAR payı <= %7 VE - yönde TUTAR payı <= %7; tohum TUTAR'ı c2_hucre kuralıyla (SIRA boot şartı yok: "
        "KART_TUR2 kuralından katı ya da eşit). tohum_ek c2_olc formülüyle aynı.",
        "(3) U0 ile U1 aynı L2'de ayrı günlerde olay verebilir (L1 pencereden çıkarsa ya da MACD [t-250, t] tohum etkisiyle s66 günden güne "
        "değişirse); her biri kendi tanımıyla kalır; ortak L2 sayısı huni'de.",
        "(4) 15 bar aralığı hissenin geçerli bar sırasıyla ve hipotez başına; ardından c2_olay OC giriş / havuz (alt %20 likidite, geçmiş "
        "bölünme) / tekil (birleşik takvimde 15 işlem günü, giriş günüyle) uygular; düşenler huni'de.",
        "(5) U3 = 15 bar sonrası U1 olaylarından L2'si U2 şartını (t = L2 + 6'da F65, RSI, DİPTE) tutanlar; U1d = 15 bar sonrası ABD U1 "
        "olaylarından olay gününde ATRP / fiyat / tepe şartlarını tutanlar; ikisine 15 bar yeniden uygulanmaz (U1'in alt kümesi).",
        "(6) Hücre = giriş günü (CETVEL2); huni'nin ön aşamaları t (L2 aşamaları L2 + 6) tarihiyle sayılır; 2015 ve öncesi hücre dışı.",
        "(7) Karar kuralı işlemsel sırası MU_ESIK['karar_islem']; U1 - U0 yalnız nokta değerle (boot bilgi).",
        "(8) İkincil cetvelde plasebo tohum deneme no 901-906 (YAPI_HEDEF Y1-Y13c numaralarından ayrı); dönem OC '2016-22'.",
        "(9) Satır dosyası olay başına bir satır; eş alanları olay başına eş özetidir (es_r15 = eş ortalaması, n_es, es_h5 / es_h10 / es_st5)."],
}

MU_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "ANA: CETVEL2 v2.2 konum eşi = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x likidite üçlüsü x F15 çeyreği), bütün evren, "
                   "aynı geometri (R15 stop'suz, aynı E0, 15 bar), aynı hipotezin o günkü olayları eş dışı, en az 5 eş (C2.c2_es); taban rastgele "
                   "olay sağlaması = plasebo kapısı 200 tohum (C2.c2_plasebo, iki yön); MEKANİK ÜSTÜNLÜK: U0 kontrolü = dipte aynı çift dip "
                   "(F65 + DİPTE + F68) ama MACD uyumsuzluğu yok; karar U1 - U0 > 0 ister; İKİNCİL: 1. tur eşi aynı d / hedef / takip"),
    "K2": ("EVET", "göstergeler yalnız t'ye kadar (MACD [t-250, t], dipler [t-60, t-1], DİPTE <= L2, RSI nedensel, ATRP kesiti t günü); veri KASA "
                   "açık kesik 2022-12-31 (kasa_kapisi her komuttan önce; satır dosyası en geç tarihi raporda); koşuda pazar başına 30 olay veri "
                   "t'de kesilip yeniden taranır (DURUR); kova sınırları / güç eğrisi CETVEL2 v2.2 mühürlü dosyaları (getirisiz)"),
    "K3": ("EVET", "YH._yh_hazir (= ge_hazir: H > L, V > 0, O/H/L/C > 0) bütün göstergeler ve bar sayıları geçerli bar sırasıyla; ölçümde "
                   "OC.oc_veri_hazirla + DS açılış kırpması (CETVEL2); sinyal günü geçersiz bar olamaz (tarama geçerli barlarda)"),
    "K4": ("EVET", "her L2 en çok bir olay; hipotez başına aynı hissede >= 15 geçerli bar aralık; c2_olay OC tekil 15 işlem günü; n = bağımsız "
                   "olay (hipotez başına ayrı c2_olc22 çağrısı); FARK ortalama + medyan, r15 ortalama + medyan; boot / permütasyon birimi giriş ayı"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla d; R15 paydası P['Op'][d, j]); eşler aynı gün açılışı; "
                   "giriş stop altıysa STOP sayılır (sayısı yazılır)"),
    "K6": ("EVET", "V_*.pkl açık kısım tek kip (KASA bayt bayt; sha ön kayıtta); MACD fiyat birimli, F66 Close(L2)'ye bölünür; R15 / ATRP / F15 "
                   "oran; AVR yerel para (hisse içi oran); U1d 5 $ eşiği yalnız ABD ham kapanış; geçmiş bölünme şüphesi havuz dışı (OC)"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (V_ABD açık 1.361, V_AVR 575, V_BIST 475 sembol): batan / kottan çıkan yok -> dipteki "
                   "olaylarda sonuç YUKARI yanlı; rapora yazılır; K34 batanlar (2020-10 sonrası) bilgi koşusu süre kalırsa"),
    "K8": ("EVET", "getirisiz huni pazar x dönem (U1, U0, bilgi varyantları) ve güç beklentisi ön kayıtta; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; "
                   "iki alt dönem (2016-19, 2020-22) ayrı hücre, ABD ve AVR ayrı; bilgi varyantları BH q 0,10; küçük örneklemden bulgu denmez"),
    "K9": ("EVET", "UYUM_ON_KAYIT.md: MU_ESIK sha + YH_ESIK8 / C2_ESIK22 / C2_ESIK sha + MACD_UYUM.py ve bağımlı kod sha + kod commit + veri / "
                   "eşik / güç / olay / huni / eşitlik sha'ları; mu_kapi git kaydı (ön kayıt commit < koşu), değişmemişlik, ik_kontrol_kapisi, "
                   "kasa_kapisi; ikinci koşu DURUR; eşikler sonuç görülünce değişmez"),
    "K10": ("UYGULANMAZ", "haber / KAP / SEC / metin ayrıştırması yok; yalnız OHLCV (V_*.pkl açık kısım) ve mühürlü CETVEL2 v2.2 eşik / güç "
                          "dosyaları"),
    "K11": ("EVET", "raporda >= 2 hücre (U1 ABD d1619 ve U0 AVR d2022) satır dosyasından bağımsız düz pandas ile yeniden üretilir (n, ort FARK, "
                    "ort SIRA, r15 ort; göreli 1e-9); tutmazsa DURUR"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı kuralla (TUTAR / TUTMADI / ÖLÇÜLEMEDİ, TUTTU / TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ); bilgi "
                    "varyantlarında hüküm yok ('bilgi: dikkat' yalnız BH); 'iz / emare' sözü yok; sayı ile yorum ayrı cümle; DGXX için hüküm yok"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_mu; mu_ / MU_ önekleri; test); yasak dosyalar (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, "
                    "COL_OZET.md, ONERI_DEFTERI.md, KASA_DEFTERI.md) ve mevcut modüller değişmedi (git diff); KASA bloğu açılmadı; e-posta / "
                    "anahtar taraması (YH._yh_yaz); push yok; kod değişirse 'çalışma zamanını yeniden başlat'"),
    "K14": ("UYGULANMAZ", "bu işte alım-satım önerisi yok; ölçüm"),
}


class MUHata(RuntimeError):
    """Durdurucu hata: veri / kasa kapısı, ön kayıt / sha tutmuyor, eşitlik / prefix / yeniden üretim tutmadı."""


# ================================================================ 0) ORTAK
def _mu_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def mu_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return YH.yh_esik_sha(MU_ESIK if E is None else E)


def _mu_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _mu_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MU_YOL["cikti"], MU_DOSYA.get(ad, ad))


def _mu_json(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, _dt.date)):
        return str(pd.Timestamp(o).date())
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return str(o)


def _mu_jyaz(yol: str, J: Any, ad: str) -> None:
    YH._yh_yaz(yol, json.dumps(J, ensure_ascii=False, indent=1, default=_mu_json, allow_nan=False) if _mu_sonlu(J) else
               json.dumps(_mu_nan_none(J), ensure_ascii=False, indent=1, default=_mu_json), ad)


def _mu_sonlu(J: Any) -> bool:
    try:
        json.dumps(J, default=_mu_json, allow_nan=False)
        return True
    except ValueError:
        return False


def _mu_nan_none(o: Any) -> Any:
    if isinstance(o, dict):
        return {k: _mu_nan_none(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_mu_nan_none(v) for v in o]
    if isinstance(o, (float, np.floating)) and not np.isfinite(o):
        return None
    return o


def _mu_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_MU, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as ex:
        raise MUHata(f"git {' '.join(args)} başarısız: {ex}") from ex


def _mu_donem(g: Any) -> np.ndarray:
    return C2._c2_donem22(g, MU_DONEM)


def mu_kasa(veri: Optional[str] = None) -> Dict[str, Any]:
    """KASA kapısı: KASA_DURUM açık kesik 2022-12-31 ve V_*.pkl en geç tarihi <= kesik; değilse DURUR."""
    v = veri or MU_YOL["veri"]
    try:
        D = KS._durum_oku(MU_YOL["kasa"])
    except Exception as ex:   # durum okunamazsa ölçüm başlamaz (fail-closed)
        raise MUHata(f"KASA durumu okunamadı: {type(ex).__name__}: {ex}") from ex
    if str(D.get("acik_kesik")) != "2022-12-31" or D.get("acilan"):
        raise MUHata(f"KASA açık kesik {D.get('acik_kesik')} / açılan {D.get('acilan')}: açık veri 2022-12-31 değil -> DURDU")
    yollar = [os.path.join(v, f"V_{p}.pkl") for p in MU_PAZAR]
    try:
        K = KS.kasa_kapisi(yollar, "2022-12-31")
    except KS.KasaHata as ex:
        raise MUHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kesik": K["kesik"], "dosya": K["dosya"], "muhur_id": D.get("muhur_id"), "acilan": D.get("acilan")}


# ================================================================ 1) Ş10 VEKTÖR (yh_s10_bar ile birebir)
def mu_ema(X: np.ndarray, span: int) -> np.ndarray:
    """pandas Series.ewm(span, adjust=False).mean() özyinelemesinin aynısı (satır başına, eksen 1; NaN yok): com = (span - 1) / 2,
    a = 1 / (1 + com); w_r = (1 - a) w_(r-1) + a x_r, (w + x farklıysa) / ((1 - a) + a). Bit-eşitliği testte denetlenir."""
    com = (float(span) - 1.0) / 2.0
    a = 1.0 / (1.0 + com); ow = 1.0 - a; den = ow + a
    X = np.asarray(X, float)
    out = np.empty_like(X); w = X[:, 0].copy(); out[:, 0] = w
    for r in range(1, X.shape[1]):
        x = X[:, r]
        nw = (ow * w + a * x) / den
        w = np.where(w != x, nw, w)
        out[:, r] = w
    return out


def mu_dip(L: np.ndarray, E8: Dict[str, Any] = YH.YH_ESIK8) -> np.ndarray:
    """Salınım dibi bayrağı k: L[k] sonlu VE L[k] < min(L[k-5 .. k-1]) VE L[k] <= min(L[k+1 .. k+5]) (yh_s10_dipler'in k koşulu; pencereden bağımsız)."""
    D = E8["dip"]; a, b = int(D["sol"]), int(D["sag"])
    L = np.asarray(L, float); n = len(L); out = np.zeros(n, bool)
    if n < a + b + 1:
        return out
    W = _swv(L, a + b + 1)
    with np.errstate(invalid="ignore"):
        sol = W[:, :a].min(axis=1); sag = W[:, a + 1:].min(axis=1); orta = W[:, a]
        out[a:n - b] = np.isfinite(orta) & (orta < sol) & (orta <= sag)
    return out


def _mu_son_dip(isd: np.ndarray) -> np.ndarray:
    n = len(isd)
    return np.maximum.accumulate(np.where(isd, np.arange(n), -1)) if n else np.array([], np.int64)


def mu_l2l1(I: np.ndarray, son: np.ndarray, E8: Dict[str, Any] = YH.YH_ESIK8) -> Tuple[np.ndarray, np.ndarray]:
    """t = I için L2 (t'ye en yakın dip, k in [t-55, t-6]) ve L1 (L2 - 8'e kadar en yakın dip, k >= t-55); yoksa -1. t < 60 -> yok."""
    D = E8["dip"]; pen, sol, sag, ara = int(D["pencere"]), int(D["sol"]), int(D["sag"]), int(D["L1_min_ara"])
    I = np.asarray(I, np.int64); n = len(son)
    alt = I - pen + sol
    j6 = I - sag - 1
    L2 = np.where((I >= pen) & (j6 >= 0) & (j6 < n), son[np.clip(j6, 0, max(n - 1, 0))] if n else -1, -1)
    L2 = np.where(L2 >= alt, L2, -1)
    j8 = L2 - ara
    L1 = np.where((L2 >= 0) & (j8 >= 0), son[np.clip(j8, 0, max(n - 1, 0))] if n else -1, -1)
    L1 = np.where((L1 >= 0) & (L1 >= alt), L1, -1)
    return L2.astype(np.int64), L1.astype(np.int64)


def mu_s10_vektor(L: np.ndarray, C: np.ndarray, I: np.ndarray, E8: Dict[str, Any] = YH.YH_ESIK8, parca: int = 6000,
                  son: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """yh_s10_bar'ın vektör sürümü (aynı işlemler, aynı sıra): I bar sıraları için F65, F66, F66m, F66h, F67, F68, tL2, s65, s66, S10 + L1, L2."""
    L = np.asarray(L, float); C = np.asarray(C, float); I = np.asarray(I, np.int64); K = len(I)
    M = E8["macd"]; T = E8["esik"]; pen = int(M["pencere"]); isn = int(M["isinma"])
    if son is None:
        son = _mu_son_dip(mu_dip(L, E8))
    L2, L1 = mu_l2l1(I, son, E8)
    out = {k: np.full(K, np.nan) for k in YH._YH_S10_SAYI}
    for k in ("s65", "s66", "S10"):
        out[k] = np.zeros(K)
    out["L1"] = L1; out["L2"] = L2
    out["tL2"] = np.where(L2 >= 0, (I - L2).astype(float), np.nan)
    if K == 0:
        return out
    w0 = np.maximum(0, I - pen)
    for b0 in range(0, K, parca):
        sl = slice(b0, min(K, b0 + parca)); ii = I[sl]; ww = w0[sl]; nb = len(ii)
        Wm = int((ii - ww).max()) + 1
        pos = np.minimum(ww[:, None] + np.arange(Wm)[None, :], ii[:, None])
        Cw = C[pos]
        m = mu_ema(Cw, int(M["hizli"])) - mu_ema(Cw, int(M["yavas"]))
        s = mu_ema(m, int(M["sinyal"]))
        rows = np.arange(nb)
        ri = ii - ww
        mi, si = m[rows, ri], s[rows, ri]
        f68 = np.where(ri >= isn, np.where(mi > si, 1.0, 0.0), np.nan)
        out["F68"][sl] = f68
        l1 = L1[sl]; l2 = L2[sl]
        r1 = l1 - ww; r2 = l2 - ww
        ok = (l1 >= 0) & (r1 >= isn) & (r2 >= isn)
        if not ok.any():
            continue
        q = np.flatnonzero(ok); rq = rows[q]
        m1 = m[rq, r1[q]]; m2 = m[rq, r2[q]]; h1 = m1 - s[rq, r1[q]]; h2 = m2 - s[rq, r2[q]]
        lo1 = L[l1[q]]; lo2 = L[l2[q]]; c2 = C[l2[q]]
        g = b0 + q
        with np.errstate(invalid="ignore", divide="ignore"):
            out["F65"][g] = lo2 / lo1 - 1.0
            out["F66"][g] = (m2 - m1) / c2
            out["F66m"][g] = m2 / c2
            out["F66h"][g] = (h2 - h1) / c2
            out["F67"][g] = (l2[q] - l1[q]).astype(float)
            s65 = lo2 <= lo1 * (1.0 + float(T["F65_ust"]))
            s66 = ((m2 - m1) / c2 > float(T["F66_alt_acik"])) & (m2 / c2 < float(T["F66m_ust_acik"]))
        out["s65"][g] = np.where(s65, 1.0, 0.0); out["s66"][g] = np.where(s66, 1.0, 0.0)
        out["S10"][g] = np.where(s65 & s66, 1.0, 0.0)
    return out


def _mu_rsi(C: np.ndarray) -> np.ndarray:
    import FON_IZI as _FI   # repodaki hazır RSI (K38-B); FON_IZI kendi çakışma kapısını taşır
    return _FI._fi_k38b_rsi(pd.Series(np.asarray(C, float)), int(MU_ESIK["u2"]["rsi_n"])).to_numpy(float)


# ================================================================ 2) HİSSE TARAMASI (yalnız t'ye kadar)
_MU_OLAY_KOL = ["hipotez", "i", "tarih", "L1", "L2", "L1_tarih", "L2_tarih", "tL2", "F65", "F66", "F66m", "F66h", "F67", "F68", "s65", "s66",
                "S10", "dipte", "rsi_L1", "rsi_L2", "low_L1", "low_L2", "close_L2", "close_t", "tepe120", "stop0", "atrp_t", "u2_L2"]
_MU_HUNI_ASAMA = ["L2 onaylı dip (L2 + 6 >= 60)", "+ L1 var (L2 + 6'da)", "+ F65 (L2 + 6'da)", "+ DİPTE", "+ Ş10 bir günde (L2 + 6 .. L2 + 20)",
                  "+ F68 aynı gün = U1 ham olay"]


def mu_hisse(d: pd.DataFrame, E: Dict[str, Any] = MU_ESIK, E8: Dict[str, Any] = YH.YH_ESIK8, atrp: Optional[np.ndarray] = None
             ) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """Hazır (geçerli bar) seri -> hipotez olayları (U1, U0, U1b, U2 ham; 15 bar aralığı uygulanmış; U3 bayrağı u2_L2) + L2 hunisi (t tarihi
    dönemine göre sayım). Yalnız t'ye kadar bilgi: dipler [t-60, t-1], MACD [t-250, t], DİPTE <= L2, RSI nedensel, ATRP t."""
    L = d["Low"].to_numpy(float); H = d["High"].to_numpy(float); C = d["Close"].to_numpy(float); idx = d.index; n = len(L)
    Dp = E["dipte"]; Ol = E["olay"]; U2 = E["u2"]
    huni: Dict[str, Dict[str, int]] = {}
    bos = pd.DataFrame(columns=_MU_OLAY_KOL)
    if n < 70:
        return bos, huni
    isd = mu_dip(L, E8); son = _mu_son_dip(isd); dips = np.flatnonzero(isd)
    if not len(dips):
        return bos, huni
    sag = int(E8["dip"]["sag"]); pen = int(E8["dip"]["pencere"]); taze = int(Ol["taze_azami"])
    nxt = np.r_[dips[1:], n + 10 ** 6]
    a = np.maximum(dips + sag + 1, pen); b = np.minimum(np.minimum(dips + taze, nxt + sag), n - 1)
    ln = np.clip(b - a + 1, 0, None)
    # DİPTE (dip başına)
    g = int(Dp["geri"]); dipte = np.zeros(len(dips), bool); tepe = np.full(len(dips), np.nan)
    if n > g:
        mnL = _swv(L, g).min(axis=1); mxH = _swv(H, g + 1).max(axis=1)
        okk = dips >= g
        jj = np.clip(dips - g, 0, len(mxH) - 1)
        tepe = np.where(okk, mxH[jj], np.nan)
        with np.errstate(invalid="ignore"):
            dipte = okk & (L[dips] <= mnL[np.clip(dips - g, 0, len(mnL) - 1)] * (1.0 + float(Dp["dip_tol"]))) & \
                (C[dips] <= float(Dp["tepe_pay"]) * tepe)
    # aday günler (dip, gün)
    tot = int(ln.sum())
    if tot == 0:
        return bos, huni
    di = np.repeat(np.arange(len(dips)), ln)
    I = np.repeat(a, ln) + (np.arange(tot) - np.repeat(np.cumsum(ln) - ln, ln))
    K2 = dips[di]
    L2c, L1c = mu_l2l1(I, son, E8)
    if not (np.array_equal(L2c, K2)):
        raise MUHata("aday gün L2'si dip sırasıyla tutmuyor (iç tutarlılık)")
    isn = int(E8["macd"]["isinma"]); pw = int(E8["macd"]["pencere"])
    with np.errstate(invalid="ignore"):
        s65ham = (L1c >= 0) & (L[K2] <= L[np.clip(L1c, 0, n - 1)] * (1.0 + float(E8["esik"]["F65_ust"])))
    macdok = (L1c >= 0) & ((I >= pw) | (L1c >= isn))
    gerek = s65ham & macdok
    V = mu_s10_vektor(L, C, I[gerek], E8, son=son)
    if not (np.array_equal(V["L2"], K2[gerek]) and np.array_equal(V["L1"], L1c[gerek])):
        raise MUHata("vektör L1 / L2 aday günlerle tutmuyor (iç tutarlılık)")
    if not np.array_equal(V["s65"] == 1.0, np.ones(int(gerek.sum()), bool)):
        raise MUHata("vektör s65 ham F65 ile tutmuyor (iç tutarlılık)")
    Ig = I[gerek]; dg = di[gerek]
    rsi = _mu_rsi(C)
    S10 = V["S10"] == 1.0; F68 = V["F68"] == 1.0; s66 = V["s66"] == 1.0; dp = dipte[dg]
    kosul = {"U1": S10 & F68 & dp, "U0": (~s66) & F68 & dp, "U1b": S10 & F68}
    # U2: t = L2 + 6 (dipin ilk aday günü olmalı), F65 (gerek), RSI(L1) < 30, RSI(L2) > RSI(L1), DİPTE
    kay = int(U2["t_kayma"])
    with np.errstate(invalid="ignore"):
        r1 = rsi[np.clip(V["L1"], 0, n - 1)]; r2 = rsi[np.clip(V["L2"], 0, n - 1)]
        u2k = (Ig == K2[gerek] + kay) & (r1 < float(U2["rsi_esik"])) & (r2 > r1) & dp
    kosul["U2"] = u2k
    u2_dip = np.zeros(len(dips), bool); u2_dip[dg[u2k]] = True
    sat = []
    for hip, mk in kosul.items():
        q = np.flatnonzero(mk)
        if not len(q):
            continue
        _, ilk = np.unique(dg[q], return_index=True)       # dip başına ilk gün (aday günler dip içinde artan sırada)
        q = q[ilk]
        q = q[np.argsort(Ig[q], kind="stable")]
        tut, son_t = [], -10 ** 9
        for x in q:
            if Ig[x] - son_t >= int(Ol["ara"]):
                tut.append(x); son_t = Ig[x]
        for x in tut:
            i = int(Ig[x]); k = int(V["L2"][x]); l1 = int(V["L1"][x]); dj = int(dg[x])
            sat.append({"hipotez": hip, "i": i, "tarih": idx[i], "L1": l1, "L2": k, "L1_tarih": idx[l1], "L2_tarih": idx[k],
                        **{c: float(V[c][x]) for c in ("tL2", "F65", "F66", "F66m", "F66h", "F67", "F68", "s65", "s66", "S10")},
                        "dipte": bool(dipte[dj]), "rsi_L1": float(rsi[l1]), "rsi_L2": float(rsi[k]), "low_L1": float(L[l1]),
                        "low_L2": float(L[k]), "close_L2": float(C[k]), "close_t": float(C[i]), "tepe120": float(tepe[dj]),
                        "stop0": float(L[k]) * float(E["stop_carpan"]), "atrp_t": float(atrp[i]) if atrp is not None else np.nan,
                        "u2_L2": bool(u2_dip[dj])})
    # L2 hunisi (dip başına; L2 + 6 tarihi)
    t6 = dips + sag + 1
    v6 = (t6 >= pen) & (t6 < n)
    # L2 + 6 günündeki L1 / F65 (ilk aday gün = L2 + 6 ise)
    ilk_mask = I == (K2 + sag + 1)
    l1_6 = np.zeros(len(dips), bool); l1_6[di[ilk_mask & (L1c >= 0)]] = True
    f65_6 = np.zeros(len(dips), bool); f65_6[di[ilk_mask & gerek]] = True
    s10_bir = np.zeros(len(dips), bool); s10_bir[dg[S10]] = True
    u1_ham = np.zeros(len(dips), bool); u1_ham[dg[kosul["U1"]]] = True
    asama = [v6, v6 & l1_6, v6 & l1_6 & f65_6, v6 & l1_6 & f65_6 & dipte, v6 & l1_6 & f65_6 & dipte & s10_bir, v6 & u1_ham]
    don = _mu_donem(idx[np.clip(t6, 0, n - 1)])
    for ad, m_ in zip(_MU_HUNI_ASAMA, asama):
        for hc in list(MU_DONEM) + ["dis"]:
            huni.setdefault(ad, {})[hc] = int((m_ & (don == hc)).sum())
    O = pd.DataFrame(sat, columns=_MU_OLAY_KOL)
    return O, huni


def mu_atrp_kesit(Vd: Dict[str, Any]) -> Tuple[Dict[str, pd.Series], pd.Series]:
    """Hisse başına ATRP (PK.pk_seri, hazır seri) ve gün başına kesit %80 niceli (o gün geçerli barı ve sonlu ATRP'si olan hisseler)."""
    A: Dict[str, pd.Series] = {}
    for s in sorted(Vd["V"]):
        d = YH._yh_hazir(Vd["V"][s])
        A[s] = PK.pk_seri(d)[0]
    M = pd.DataFrame(A)
    q = 1.0 - float(MU_ESIK["u1d"]["atrp_ust_pay"])
    esik = M.apply(lambda r: float(np.quantile(r.dropna().to_numpy(float), q)) if r.notna().any() else np.nan, axis=1)
    return A, esik


def mu_pazar(pazar: str, veri: Optional[str] = None, Vd: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazarın bütün hisseleri -> olay tablosu (U1, U0, U1b, U2, U3, U1d) + L2 hunisi. Veri: CETVEL2 tabanı (DS.ds_veri) Vd."""
    t0 = time.time()
    if Vd is None:
        Vd = C2.c2_panel22_al(pazar, veri, None)["Vd"]
    atrpA, esik = (mu_atrp_kesit(Vd) if pazar == MU_ESIK["u1d"]["pazar"] else ({}, None))
    parca, huni = [], {}
    for s in sorted(Vd["V"]):
        d = YH._yh_hazir(Vd["V"][s])
        at = atrpA[s].reindex(d.index).to_numpy(float) if s in atrpA else None
        O, h = mu_hisse(d, atrp=at)
        for a_, x in h.items():
            for k_, v_ in x.items():
                huni.setdefault(a_, {}).setdefault(k_, 0)
                huni[a_][k_] += v_
        if len(O):
            O.insert(0, "sembol", s); O.insert(0, "pazar", pazar)
            parca.append(O)
    O = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame(columns=["pazar", "sembol"] + _MU_OLAY_KOL)
    # U3 ve U1d (U1'in alt kümeleri)
    U1 = O[O.hipotez == "U1"].copy()
    U3 = U1[U1.u2_L2.astype(bool)].copy(); U3["hipotez"] = "U3"
    ek = [U3]
    if pazar == MU_ESIK["u1d"]["pazar"] and len(U1):
        Z = MU_ESIK["u1d"]
        es = esik.reindex(pd.DatetimeIndex(U1.tarih)).to_numpy(float)
        with np.errstate(invalid="ignore"):
            m = (U1.atrp_t.to_numpy(float) >= es) & (U1.close_t.to_numpy(float) < float(Z["fiyat_ust"])) & \
                (U1.close_L2.to_numpy(float) <= float(Z["tepe_pay"]) * U1.tepe120.to_numpy(float))
        U1d = U1[m].copy(); U1d["hipotez"] = "U1d"; U1d["atrp_esik"] = es[m]
        ek.append(U1d)
    O = pd.concat([O] + ek, ignore_index=True)
    O["tarih"] = pd.to_datetime(O.tarih); O["L1_tarih"] = pd.to_datetime(O.L1_tarih); O["L2_tarih"] = pd.to_datetime(O.L2_tarih)
    O = O.sort_values(["hipotez", "sembol", "tarih"], kind="mergesort").reset_index(drop=True)
    mulog.info("%s tarama: %d hisse, olay %s (%.0f sn)", pazar, len(Vd["V"]), O.hipotez.value_counts().to_dict(), time.time() - t0)
    return O, {"L2": huni}


def mu_olay_tablo_sha(O: pd.DataFrame) -> str:
    """Olay tablosunun içerik sha'sı (sıralı, 12 anlamlı basamak; getirisiz)."""
    kol = ["pazar", "sembol", "hipotez", "tarih", "L1", "L2", "F65", "F66", "F68", "s65", "s66", "S10", "dipte", "rsi_L1", "rsi_L2", "stop0", "atrp_t"]
    X = O[kol].copy()
    for c in ("tarih",):
        X[c] = pd.to_datetime(X[c]).dt.strftime("%Y-%m-%d")
    b = X.to_csv(index=False, float_format="%.12g").encode()
    return hashlib.sha256(b).hexdigest()


# ================================================================ 3) EŞİTLİK (yh_s10_bar) ve PREFIX (K2)
def mu_esitlik(Vd: Dict[str, Any], O: pd.DataFrame, pazar: str, pi: int) -> Dict[str, Any]:
    """Pazar başına 150 bar: mu_s10_vektor = yh_s10_bar birebir (10 çıktı, tam eşit). Değilse MUHata."""
    Es = MU_ESIK["esitlik"]; rng = np.random.default_rng([int(Es["tohum"]), pi])
    S = sorted(Vd["V"]); kol = YH._YH_S10_OZ; sat = []; bozuk = []
    hz: Dict[str, pd.DataFrame] = {}

    def hazir(s: str) -> pd.DataFrame:
        if s not in hz:
            hz[s] = YH._yh_hazir(Vd["V"][s])
        return hz[s]
    secim: List[Tuple[str, int, str]] = []
    while sum(1 for x in secim if x[2] == "rastgele") < int(Es["n_rastgele"]):
        s = S[int(rng.integers(len(S)))]; d = hazir(s)
        if len(d) >= 2:
            secim.append((s, int(rng.integers(len(d))), "rastgele"))
    tur = 0
    while sum(1 for x in secim if x[2] == "aday") < int(Es["n_aday"]) and tur < 20000:
        tur += 1
        s = S[int(rng.integers(len(S)))]; d = hazir(s); L = d.Low.to_numpy(float)
        if len(d) < 80:
            continue
        i = int(rng.integers(60, len(d)))
        L2, L1 = mu_l2l1(np.array([i]), _mu_son_dip(mu_dip(L)))
        if L1[0] >= 0 and L[L2[0]] <= L[L1[0]] * 1.01:
            secim.append((s, i, "aday"))
    if len(O):
        q = rng.choice(len(O), min(int(Es["n_olay"]), len(O)), replace=False)
        for x in q:
            r = O.iloc[int(x)]; d = hazir(r.sembol)
            secim.append((r.sembol, int(d.index.get_loc(pd.Timestamp(r.tarih))), "olay"))
    for s, i, tur_ in secim:
        d = hazir(s); L = d.Low.to_numpy(float); C = d.Close.to_numpy(float)
        a = YH.yh_s10_bar(L, C, i)
        v = mu_s10_vektor(L, C, np.array([i]))
        av = np.array([a[k] for k in kol], float); vv = np.array([v[k][0] for k in kol], float)
        esit = bool(np.array_equal(av, vv, equal_nan=True))
        sat.append({"sembol": s, "i": i, "tur": tur_, "esit": esit, "S10": a["S10"], "F68": a["F68"]})
        if not esit:
            bozuk.append({"sembol": s, "i": i, "yh": av.tolist(), "mu": vv.tolist()})
    T = pd.DataFrame(sat)
    sonuc = {"pazar": pazar, "n": int(len(T)), "tur": T.tur.value_counts().to_dict(), "esit": int(T.esit.sum()),
             "S10_1": int((T.S10 == 1).sum()), "F68_1": int((T.F68 == 1).sum()), "bozuk": bozuk[:5]}
    if bozuk:
        raise MUHata(f"{pazar}: yh_s10_bar eşitliği TUTMADI ({len(bozuk)} / {len(T)}): {bozuk[:2]} -> DURDU")
    mulog.info("%s eşitlik: %d / %d bar birebir (S10 = 1: %d)", pazar, sonuc["esit"], sonuc["n"], sonuc["S10_1"])
    return sonuc


def mu_prefix(Vd: Dict[str, Any], O: pd.DataFrame, pazar: str, pi: int) -> Dict[str, Any]:
    """K2: pazar başına 30 rastgele olay; hissenin verisi t'de kesilir, tarama kesik seriyle yeniden; olay aynı çıkmalı. Değilse MUHata."""
    Pr = MU_ESIK["prefix"]; rng = np.random.default_rng([int(Pr["tohum"]), pi]); bozuk, sat = [], []
    if not len(O):
        return {"pazar": pazar, "n": 0, "tuttu": 0}
    kol = ["L1", "L2", "F65", "F66", "F66m", "F66h", "F67", "F68", "s65", "s66", "S10", "dipte", "rsi_L1", "rsi_L2", "stop0", "atrp_t"]
    for x in rng.choice(len(O), min(int(Pr["n"]), len(O)), replace=False):
        r = O.iloc[int(x)]; t = pd.Timestamp(r.tarih)
        ham = Vd["V"][r.sembol]; kes = YH._yh_hazir(ham[ham.index <= t])
        at = PK.pk_seri(kes)[0].to_numpy(float) if pazar == MU_ESIK["u1d"]["pazar"] else None
        Ok, _ = mu_hisse(kes, atrp=at)
        hip = "U1" if r.hipotez in ("U3", "U1d") else r.hipotez
        e = Ok[(Ok.hipotez == hip) & (pd.to_datetime(Ok.tarih) == t)]
        tut = len(e) == 1
        if tut:
            e = e.iloc[0]
            a = np.array([float(r[c]) for c in kol]); b = np.array([float(e[c]) for c in kol])
            tut = bool(np.array_equal(a, b, equal_nan=True))
            if r.hipotez == "U3":
                tut = tut and bool(e.u2_L2)
        sat.append({"sembol": r.sembol, "tarih": str(t.date()), "hipotez": r.hipotez, "tuttu": tut})
        if not tut:
            bozuk.append(sat[-1])
    if bozuk:
        raise MUHata(f"{pazar}: prefix (K2) TUTMADI {len(bozuk)} / {len(sat)}: {bozuk[:3]} -> DURDU")
    return {"pazar": pazar, "n": len(sat), "tuttu": int(sum(s["tuttu"] for s in sat)), "olay": sat}


# ================================================================ 4) HUNİ (getirisiz) ve GÜÇ BEKLENTİSİ
def mu_c2_huni(O: pd.DataFrame, pazar: str, veri: Optional[str] = None) -> Dict[str, Any]:
    """Hipotez başına c2_olay (OC giriş / havuz / tekil 15) ve R15 ölçülebilir / eşli SAYILARI (getiri değeri okunmaz)."""
    Pn = C2.c2_panel22_al(pazar, veri, int(MU_ESIK["olcu"]["ufuk"]))
    out: Dict[str, Any] = {}
    for hip in MU_HIP:
        Oh = O[O.hipotez == hip]
        if not len(Oh):
            out[hip] = {"oc": {}, "r15": {}, "esli": {}, "say": {}}
            continue
        X, say = C2.c2_olay(Oh[["sembol", "tarih"]], Pn, int(MU_ESIK["olcu"]["tekil_gun"]))
        dn = _mu_donem(X.giris)
        e = C2.c2_es(Pn, X.d.to_numpy(np.int64), X.j.to_numpy(np.int64), X.r15.to_numpy(float), X.d.to_numpy(np.int64), X.j.to_numpy(np.int64))
        fin = np.isfinite(X.r15.to_numpy(float)); esl = np.isfinite(e["fark"])
        out[hip] = {"oc": {h: int((dn == h).sum()) for h in list(MU_DONEM) + ["dis"]},
                    "r15": {h: int(((dn == h) & fin).sum()) for h in list(MU_DONEM) + ["dis"]},
                    "esli": {h: int(((dn == h) & esl).sum()) for h in list(MU_DONEM) + ["dis"]},
                    "say": {k: v for k, v in say.items() if k != "donem"}}
    return out


def mu_huni_tablo(O: pd.DataFrame, H: Dict[str, Any]) -> pd.DataFrame:
    """Huni satırları: hipotez x aşama x pazar x hücre (t tarihi ön aşamalar, giriş tarihi OC sonrası)."""
    sat = []
    for p in MU_PAZAR:
        L2 = H.get(p, {}).get("L2", {})
        for a_ in _MU_HUNI_ASAMA:
            for h in MU_DONEM:
                sat.append({"hipotez": "U1 (L2 hunisi)", "asama": a_, "pazar": p, "hucre": h, "n": int(L2.get(a_, {}).get(h, 0))})
        Op = O[O.pazar == p]
        for hip in MU_HIP:
            Oh = Op[Op.hipotez == hip]
            dn = _mu_donem(Oh.tarih) if len(Oh) else np.array([])
            for h in MU_DONEM:
                sat.append({"hipotez": hip, "asama": "olay (ilk gün + 15 bar; t tarihi)", "pazar": p, "hucre": h, "n": int((dn == h).sum())})
            c = H.get(p, {}).get("c2", {}).get(hip, {})
            for ad, k_ in (("OC sonrası (giriş + havuz + tekil; giriş tarihi)", "oc"), ("R15 ölçülebilir", "r15"), ("eşli (>= 5 eş) = n", "esli")):
                for h in MU_DONEM:
                    sat.append({"hipotez": hip, "asama": ad, "pazar": p, "hucre": h, "n": int(c.get(k_, {}).get(h, 0))})
    return pd.DataFrame(sat)


def mu_guc_beklenti(T: pd.DataFrame, guc: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
    """Beklenen n (eşli) -> güç (cetvel2_guc_v2.2.json, H 15, delta +0,02). Getiri kullanılmaz."""
    sat = []
    for hip in MU_HIP:
        for p in MU_PAZAR:
            for h in MU_DONEM:
                x = T[(T.hipotez == hip) & (T.pazar == p) & (T.hucre == h) & (T.asama == "eşli (>= 5 eş) = n")]
                n = int(x.n.sum()) if len(x) else 0
                eg = C2._c2_egri22_al(p, h, int(MU_ESIK["olcu"]["ufuk"]), guc)
                g = C2.c2_guc(n, eg) if n > 0 else 0.0
                sat.append({"hipotez": hip, "pazar": p, "hucre": h, "n": n, "guc": g,
                            "durum": "güç yeterli" if (n >= 30 and np.isfinite(g) and g >= 0.80) else "ÖLÇÜLEMEDİ beklenir"})
    return pd.DataFrame(sat)


# ================================================================ 5) HÜCRE HÜKMÜ ve KARAR
def mu_sira_boot(sira: np.ndarray, ay: np.ndarray, tohum_ek: int) -> Tuple[float, float]:
    """KART_TUR2.k2_stat SIRA boot yöntemi: giriş ayı kümeleri, multinomial ağırlık, ort SIRA = W @ ay toplamı / W @ ay sayısı."""
    s = np.asarray(sira, float); ay = np.asarray(ay); m = np.isfinite(s); s, ay = s[m], ay[m]
    if not len(s):
        return np.nan, np.nan
    B = MU_ESIK["hucre"]["sira_boot"]
    ua, inv = np.unique(ay, return_inverse=True); K = len(ua)
    ss = np.bincount(inv, weights=s, minlength=K); nn = np.bincount(inv, minlength=K).astype(float)
    rng = np.random.default_rng([int(B["tohum"]), int(tohum_ek) % (2 ** 31)])
    W = rng.multinomial(K, np.full(K, 1.0 / K), size=int(B["B"])).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        ms = (W @ ss) / (W @ nn)
    ms = ms[np.isfinite(ms)]
    if not len(ms):
        return np.nan, np.nan
    return float(np.quantile(ms, float(B["alt"]))), float(np.quantile(ms, float(B["ust"])))


def mu_hukum(c: Dict[str, Any]) -> Tuple[str, str]:
    """Hücre hükmü (KART_TUR2 (3) + güç): ÖLÇÜLEMEDİ / TUTAR / TUTMADI ve gerekçe. c: c2_hucre + sira_alt + plasebo alanları."""
    Hk = MU_ESIK["hucre"]; n = int(c.get("n", 0) or 0); g = c.get("guc", np.nan)
    if n < int(Hk["n_min"]) or not (g is not None and np.isfinite(g) and g >= float(Hk["guc_esik"])):
        gs = "-" if g is None or not np.isfinite(g) else f"{float(g):.2f}".replace(".", ",")
        return "ÖLÇÜLEMEDİ", f"n {n}, güç {gs} (< 0,80 ya da n < 30)"
    neden = []
    f = lambda k: c.get(k) is not None and np.isfinite(c.get(k))  # noqa: E731
    if not (f("fark") and c["fark"] > 0):
        neden.append("FARK <= 0")
    if not (f("boot_alt") and c["boot_alt"] > 0):
        neden.append("FARK boot alt <= 0")
    if not (f("sira") and c["sira"] > float(Hk["sira"])):
        neden.append("SIRA <= 0,50")
    if not (f("sira_alt") and c["sira_alt"] > float(Hk["sira_boot_alt"])):
        neden.append("SIRA boot alt <= 0,50")
    if not (f("l3o") and c["l3o"] > 0):
        neden.append("L3O <= 0")
    if not c.get("plasebo_gecti", False):
        neden.append("plasebo kapısı düştü")
    return ("TUTAR", "bütün şartlar") if not neden else ("TUTMADI", "; ".join(neden))


def mu_karar(h1: Dict[str, Dict[str, Any]], h0: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """h1 / h0: 'pazar|hücre' -> hücre sözlüğü (hukum, n, guc, fark, boot_alt, boot_ust) U1 / U0. Önceden yazılı karar kuralı (MU_ESIK)."""
    Hk = MU_ESIK["hucre"]
    hucre = [f"{p}|{h}" for p in MU_KARAR_PAZAR for h in MU_DONEM]
    c1 = {k: h1.get(k, {"hukum": "ÖLÇÜLEMEDİ", "n": 0}) for k in hucre}
    fark = {}
    for k in hucre:
        a, b = c1[k].get("fark", np.nan), h0.get(k, {}).get("fark", np.nan)
        fark[k] = float(a - b) if (a is not None and b is not None and np.isfinite(a) and np.isfinite(b)) else np.nan
    u0_olc = {k: int(h0.get(k, {}).get("n", 0) or 0) >= int(Hk["n_min"]) for k in hucre}
    hep_tutar = all(c1[k]["hukum"] == "TUTAR" for k in hucre)
    if hep_tutar and all(np.isfinite(fark[k]) and fark[k] > 0 for k in hucre):
        return {"karar": "AÇIK VERİDE TUTTU", "neden": "4 hücrede U1 TUTAR ve U1 - U0 > 0", "u1_u0": fark,
                "sonraki": "ÖNERİ: KASA 2023-24 kör sınaması (Cemal kararı)"}

    def poz(c):
        return c.get("boot_alt") is not None and np.isfinite(c.get("boot_alt", np.nan)) and c["boot_alt"] > 0

    def neg(c):
        return c.get("boot_ust") is not None and np.isfinite(c.get("boot_ust", np.nan)) and c["boot_ust"] < 0
    if any(poz(c1[k]) for k in hucre) and any(neg(c1[k]) for k in hucre):
        return {"karar": "ÇELİŞKİLİ", "neden": "U1 FARK boot aralığı bir hücrede tümüyle > 0, bir başkasında tümüyle < 0", "u1_u0": fark}
    guclu = [k for k in hucre if c1[k]["hukum"] in ("TUTAR", "TUTMADI")]
    tutmayan = [k for k in guclu if c1[k]["hukum"] == "TUTMADI"]
    if tutmayan:
        return {"karar": "TUTMADI", "neden": "gücü yeterli hücrede U1 TUTMADI: " + ", ".join(tutmayan), "u1_u0": fark}
    if hep_tutar:
        kotu = [k for k in hucre if u0_olc[k] and np.isfinite(fark[k]) and fark[k] <= 0]
        if kotu:
            return {"karar": "TUTMADI", "neden": "U1 TUTAR ama U1 - U0 <= 0: " + ", ".join(kotu), "u1_u0": fark}
    eksik = [k for k in hucre if c1[k]["hukum"] == "ÖLÇÜLEMEDİ"] + [f"{k} (U0)" for k in hucre if hep_tutar and not u0_olc[k]]
    return {"karar": "ÖLÇÜLEMEDİ", "neden": "güç yetersiz: " + ", ".join(eksik) if eksik else "güç yetersiz", "u1_u0": fark}


def mu_fark_boot(f1: np.ndarray, a1: np.ndarray, f0: np.ndarray, a0: np.ndarray, tohum_ek: int) -> Tuple[float, float]:
    """FARK(U1) - FARK(U0) için bağımsız ay kümeli bootstrap %95 (bilgi)."""
    B = MU_ESIK["fark_u1_u0"]

    def hazir(f, a):
        f = np.asarray(f, float); a = np.asarray(a); m = np.isfinite(f); f, a = f[m], a[m]
        ua, inv = np.unique(a, return_inverse=True)
        return np.bincount(inv, weights=f, minlength=len(ua)), np.bincount(inv, minlength=len(ua)).astype(float)
    s1, n1 = hazir(f1, a1); s0, n0 = hazir(f0, a0)
    if not len(s1) or not len(s0):
        return np.nan, np.nan
    rng = np.random.default_rng([int(B["tohum"]), int(tohum_ek) % (2 ** 31)])
    W1 = rng.multinomial(len(s1), np.full(len(s1), 1.0 / len(s1)), size=int(B["B"])).astype(float)
    W0 = rng.multinomial(len(s0), np.full(len(s0), 1.0 / len(s0)), size=int(B["B"])).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W1 @ s1) / (W1 @ n1) - (W0 @ s0) / (W0 @ n0)
    d = d[np.isfinite(d)]
    return (float(np.quantile(d, 0.025)), float(np.quantile(d, 0.975))) if len(d) else (np.nan, np.nan)


# ================================================================ 6) ÖLÇÜM
def mu_olc_r(O: pd.DataFrame, hip: str, ufuk: int, plasebo: bool, veri: Optional[str] = None) -> Dict[str, Any]:
    """ANA (ufuk 15) ya da BİLGİ (ufuk 30): c2_olc22 (hipotez başına ayrı çağrı, plasebo ayrı) + SIRA boot + plasebo kapısı + hüküm."""
    Oh = O[O.hipotez == hip]
    if not len(Oh):
        return {"satir": pd.DataFrame(), "hucre": [], "say": {}}
    kod = hip; tohum0 = MU_HIP.index(hip) + 1
    R = C2.c2_olc22(Oh[["pazar", "sembol", "tarih"]].copy(), {kod: {"bayrak": None, "yon": "+"}}, ufuk=int(ufuk), donem=MU_DONEM,
                    plasebo=False, bilgi=False, veri=veri, tohum0=tohum0)
    S = R["satir"]; Hc = R["hucre"]; hucre = []
    pazarlar = sorted(Oh.pazar.astype(str).unique())
    for r in Hc.to_dict("records"):
        p, hc = r["pazar"], r["hucre"]
        pi = pazarlar.index(p); hi = list(MU_DONEM).index(hc)
        tek = int(tohum0) * 100000 + 0 * 1000 + pi * 100 + hi
        mm = (S.pazar.to_numpy() == p) & (S.donem.to_numpy() == hc) & np.isfinite(S[f"fark_{kod}"].to_numpy(float))
        ay = pd.to_datetime(S.giris[mm]).dt.strftime("%Y-%m").to_numpy()
        sa, su = mu_sira_boot(S[f"sira_{kod}"].to_numpy(float)[mm], ay, tek)
        c = {**r, "sira_alt": sa, "sira_ust": su, "ufuk": int(ufuk),
             "es_r15_ort": float(np.mean(S[f"es_r15_{kod}"].to_numpy(float)[mm])) if mm.any() else np.nan,
             "es_r15_med": float(np.median(S[f"es_r15_{kod}"].to_numpy(float)[mm])) if mm.any() else np.nan,
             "r15_ort_olc": float(np.mean(S.r15.to_numpy(float)[mm])) if mm.any() else np.nan,
             "r15_med_olc": float(np.median(S.r15.to_numpy(float)[mm])) if mm.any() else np.nan,
             "fark_med": float(np.median(S[f"fark_{kod}"].to_numpy(float)[mm])) if mm.any() else np.nan}
        if plasebo and c["n"] > 0:
            Pn = C2.c2_panel22_al(p, veri, int(ufuk))
            eg = C2._c2_egri22_al(p, hc, int(ufuk), None)
            pl = C2.c2_plasebo(Pn, S.d.to_numpy(np.int64)[mm], "+", eg, tohum_ek=tek, iki_yon_ayri=True)
            P_ = MU_ESIK["hucre"]["plasebo"]
            gec = bool(np.isfinite(pl["fark_ort"]) and abs(pl["fark_ort"]) < float(P_["fark_mutlak"])
                       and pl["tutar_pay_arti"] <= float(P_["tutar_pay"]) and pl["tutar_pay_eksi"] <= float(P_["tutar_pay"]))
            c.update({"plasebo_fark": pl["fark_ort"], "plasebo_pay_arti": pl["tutar_pay_arti"], "plasebo_pay_eksi": pl["tutar_pay_eksi"],
                      "plasebo_gecti": gec})
        else:
            c.update({"plasebo_fark": np.nan, "plasebo_pay_arti": np.nan, "plasebo_pay_eksi": np.nan, "plasebo_gecti": False})
        c["hukum"], c["hukum_neden"] = mu_hukum(c)
        hucre.append(c)
    return {"satir": S, "hucre": hucre, "say": R["say"]}


def mu_olc_h5(O: pd.DataFrame, hip: str, pazar: str, veri: Optional[str] = None) -> pd.DataFrame:
    """İKİNCİL: 1. tur 15 bar cetveli (YH.yh_olay_olc + yh_konum_es_olc), stop0 = Low(L2) x 0,98, tekil 15."""
    Oh = O[(O.hipotez == hip) & (O.pazar == pazar)]
    if not len(Oh):
        return pd.DataFrame()
    Pb = C2.c2_panel22_al(pazar, veri, None); P, Cl, Vd = Pb["P"], Pb["Cl"], Pb["Vd"]
    E1 = copy.deepcopy(OC.OC_ESIK); E1["olay"]["tekil_gun"] = int(MU_ESIK["olcu"]["tekil_gun"])
    sig = Oh[["sembol", "tarih", "stop0"]].copy(); sig["pazar"] = pazar; sig["tarih"] = pd.to_datetime(sig.tarih)
    X, _ = OC.oc_olay_hazirla(sig[["sembol", "tarih", "pazar"]], P, E1)
    if not len(X):
        return pd.DataFrame()
    X = X.merge(sig[["sembol", "tarih", "stop0"]], on=["sembol", "tarih"], how="left", validate="one_to_one"); X["yon"] = 1
    dno = int(MU_ESIK["ikincil"]["deneme_no"][hip]); pno = OC.OC_ESIK["pazar"].index(pazar) + 1
    Z = YH.yh_olay_olc(P, Cl, Vd, X, dno, pno, YH.YH_ESIK)
    Z["F15"] = Pb["F15"][Z.d.to_numpy(int), Z.j.to_numpy(int)]
    Z = YH.yh_konum_es_olc(P, Cl, Z, Pb["F15"], 1, YH.YH_ESIK)
    Z["hucre"] = _mu_donem(Z.giris); Z["pazar"] = pazar; Z["hipotez"] = hip
    return Z


def mu_h5_hucre(Z: pd.DataFrame) -> Dict[str, Any]:
    """İkincil hücre özeti: yh_hucre (KAT5, P olay / eş, stop, plasebo KAT5) + yh_hucre_konum + giriş stop altı (STOP sayılır)."""
    if not len(Z):
        return {"n": 0}
    h = YH.yh_hucre(Z, YH.YH_ESIK); k = YH.yh_hucre_konum(Z, YH.YH_ESIK)
    gs = int((Z.cikis_tur == "giris_stop_otesi").sum())
    g = Z[Z.h5.notna() & Z.es_h5.notna()]
    n = int(len(g))
    out = {"n": n, "giris_stop_alti": gs,
           "p_h5": h.get("h5_p_olay"), "es_h5": h.get("h5_p_ref"), "kat5": h.get("h5_kat"), "kat5_alt": h.get("h5_alt"), "kat5_ust": h.get("h5_ust"),
           "p_h10": h.get("h10_p_olay"), "es_h10": h.get("h10_p_ref"), "p_st5": h.get("st5_p_olay"), "es_st5": h.get("st5_p_ref"),
           "k_kat5": k.get("k_h5_kat"), "k_kat5_alt": k.get("k_h5_alt"), "k_kat5_ust": k.get("k_h5_ust"),
           "pl_kat5": h.get("pl_h5_kat"), "pl_kat5_alt": h.get("pl_h5_alt"), "pl_kat5_ust": h.get("pl_h5_ust"),
           "getiri_ort": h.get("getiri_ort"), "getiri_med": h.get("getiri_med"), "cikis_bar_med": h.get("cikis_bar_med")}
    if n + gs > 0:
        out["p_h5_stopdahil"] = float((g.h5.sum()) / (n + gs)); out["p_h10_stopdahil"] = float(g.h10.sum() / (n + gs))
        out["p_st5_stopdahil"] = float((g.st5.sum() + gs) / (n + gs))
    return out


# ================================================================ 7) SHA, ÖN KAYIT, KAPI
def mu_sha_simdi(veri: Optional[str] = None) -> Dict[str, str]:
    v = veri or MU_YOL["veri"]; c2c = C2.C2_YOL["cikti"]
    out = {"MU_ESIK_SHA": mu_esik_sha(), "YH_ESIK8_SHA": YH.yh_esik8_sha(), "C2_ESIK22_SHA": C2.c2_esik22_sha(), "C2_ESIK_SHA": C2.c2_esik_sha(),
           "MU_KOD_SHA": _mu_sha(MU_YOL["kod"])}
    for f in MU_BAGIMLI:
        out[f"KOD:{f}"] = _mu_sha(os.path.join(KOK_MU, f))
    for ad, y in (("C2_ESIK22_JSON_SHA", os.path.join(c2c, "cetvel2_esik_v2.2.json")), ("C2_GUC22_JSON_SHA", os.path.join(c2c, "cetvel2_guc_v2.2.json"))):
        out[ad] = _mu_sha(y)
    for p in MU_PAZAR:
        out[f"V_{p}_SHA"] = _mu_sha(os.path.join(v, f"V_{p}.pkl"))
    return out


def mu_hazirlik(veri: Optional[str] = None, cikti: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt girdileri (getirisiz): olaylar, huni, yh_s10_bar eşitliği, güç beklentisi."""
    c = cikti or MU_YOL["cikti"]; os.makedirs(c, exist_ok=True)
    K = mu_kasa(veri)
    Os, H, Es = [], {}, {}
    for pi, p in enumerate(MU_PAZAR):
        Pb = C2.c2_panel22_al(p, veri, None)
        O, h = mu_pazar(p, veri, Pb["Vd"])
        Es[p] = mu_esitlik(Pb["Vd"], O, p, pi)
        H[p] = {**h, "c2": mu_c2_huni(O, p, veri)}
        Os.append(O)
    O = pd.concat(Os, ignore_index=True)
    yol = _mu_yol("olay", c)
    Ow = O.copy()
    for k_ in ("tarih", "L1_tarih", "L2_tarih"):
        Ow[k_] = pd.to_datetime(Ow[k_]).dt.strftime("%Y-%m-%d")
    Ow.to_csv(yol, index=False, float_format="%.12g", compression={"method": "gzip", "mtime": 0})
    T = mu_huni_tablo(O, H)
    G = mu_guc_beklenti(T)
    ortak = {}
    for p in MU_PAZAR:
        a = O[(O.pazar == p) & (O.hipotez == "U1")]; b = O[(O.pazar == p) & (O.hipotez == "U0")]
        ortak[p] = int(len(set(zip(a.sembol, a.L2_tarih)) & set(zip(b.sembol, b.L2_tarih))))
    J = {"surum": MU_SURUM, "olay_sha": mu_olay_tablo_sha(O), "olay_dosya_sha": _mu_sha(yol), "huni": T.to_dict("records"),
         "guc": G.to_dict("records"), "esitlik": Es, "kasa": K, "ortak_L2_U1_U0": ortak,
         "c2_say": {p: H[p]["c2"] for p in MU_PAZAR}}
    _mu_jyaz(_mu_yol("huni", c), {k: J[k] for k in ("surum", "olay_sha", "olay_dosya_sha", "huni", "guc", "ortak_L2_U1_U0", "c2_say")}, "MU huni")
    _mu_jyaz(_mu_yol("esitlik", c), Es, "MU eşitlik")
    return {**J, "O": O, "T": T, "G": G}


def _mu_tablo_md(T: pd.DataFrame) -> List[str]:
    L = ["| Hipotez | Aşama | " + " | ".join(f"{p} {h}" for p in MU_PAZAR for h in MU_DONEM) + " |",
         "|---|---|" + "---|" * (len(MU_PAZAR) * len(MU_DONEM))]
    for (hip, a_), g in T.groupby(["hipotez", "asama"], sort=False):
        v = {(r.pazar, r.hucre): r.n for r in g.itertuples()}
        L.append(f"| {hip} | {a_} | " + " | ".join(str(v.get((p, h), 0)) for p in MU_PAZAR for h in MU_DONEM) + " |")
    return L


def mu_onkayit_yaz(veri: Optional[str] = None, cikti: Optional[str] = None, uzerine: bool = False) -> str:
    c = cikti or MU_YOL["cikti"]; yol = _mu_yol("onkayit", c)
    if os.path.exists(yol) and not uzerine:
        raise MUHata(f"ön kayıt zaten var: {yol}")
    if os.path.exists(_mu_yol("sonuc", c)):
        raise MUHata("sonuc.json var: koşu yapılmış; ön kayıt yeniden yazılmaz")
    J = mu_hazirlik(veri, c)
    S = mu_sha_simdi(veri)
    kod_git = _mu_git(["log", "-1", "--format=%H %cI", "--", "MACD_UYUM.py"]) or "-"
    durum = _mu_git(["status", "--porcelain", "--", "MACD_UYUM.py"])
    if durum:
        raise MUHata("MACD_UYUM.py git'e işlenmemiş ya da değişmiş: önce kod commit")
    L = [f"# MACD_UYUM — ÖN KAYIT (K47 MACD pozitif uyumsuzluk, tek başına ve DİPTE) — {_mu_simdi()}", "",
         "Bu dosya ölçümden (R15 / h5 / getiri) ÖNCE yazıldı ve git'e işlendi; aşağıdaki sayılar yalnız olay SAYILARI, güç beklentisi (CETVEL2 v2.2 "
         "eğrisi, getirisiz) ve yh_s10_bar eşitlik denetimidir. `python MACD_UYUM.py kos` mu_kapi ile bu dosyanın git kaydını, değişmemişliğini, "
         "sha'larını, olay tablosu sha'sını, IZ_KARNE.ik_kontrol_kapisi'ni ve KASA kapısını denetler; biri tutmazsa DURUR. İkinci koşu DURUR.", "",
         f"KASA: açık kesik {J['kasa']['kesik']} (KASA_DURUM mühür {J['kasa']['muhur_id']}, açılan blok {J['kasa']['acilan']}); veri /tmp/veri -> "
         f"/tmp/kasa/acik; açık kısım V_*.pkl sha'ları arastirma_cikti/kasa/KASA_MANIFEST.json (mühür 4a7fbad49def764c) acik_sha256 ile AYNI "
         f"(bu oturumda islenmis-veri fce5d94'ten aynı kesikle yeniden mühürlendi; manifest repo dışında). En geç tarih: "
         + "; ".join(f"{os.path.basename(k)} {v}" for k, v in J["kasa"]["dosya"].items()), "",
         f"Kod commit (MACD_UYUM.py son git kaydı): `{kod_git}`", ""]
    L += [f"- {k}: `{v}`" for k, v in S.items()]
    L += [f"- OLAY_TABLO_SHA (içerik): `{J['olay_sha']}`", f"- OLAY_DOSYA_SHA ({MU_DOSYA['olay']}): `{J['olay_dosya_sha']}`",
          f"- HUNI_JSON_SHA ({MU_DOSYA['huni']}): `{_mu_sha(_mu_yol('huni', c))}`", f"- ESITLIK_JSON_SHA ({MU_DOSYA['esitlik']}): `{_mu_sha(_mu_yol('esitlik', c))}`", ""]
    L += ["## 1. TANIMLAR ve EŞİKLER (MU_ESIK; iş tanımından AYNEN, sha yukarıda)", ""]
    for k, v in MU_ESIK.items():
        if k == "uygulama_yorumlari":
            continue
        L.append(f"- {k}: {json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v}")
    L += ["", "### Ş10 tanımı (YH_ESIK8 macd / dip / esik, AYNEN)", ""]
    for k in ("macd", "dip", "esik"):
        L.append(f"- {k}: {json.dumps(YH.YH_ESIK8[k], ensure_ascii=False)}")
    L += ["", "### Hücre kuralı (KART_TUR2 ön kaydından kopya)", "", _KT2_HUCRE, "",
          "### Karar kuralı (iş tanımından AYNEN)", "", MU_ESIK["karar_kurali"], "", "İşlemsel sıra: " + MU_ESIK["karar_islem"], "",
          "### UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden ÖNCE yazıldı)", ""]
    L += [f"- {x}" for x in MU_ESIK["uygulama_yorumlari"]]
    L += ["", "## 2. yh_s10_bar EŞİTLİĞİ (getirisiz; mu_s10_vektor = yh_s10_bar, 10 çıktı tam eşit)", ""]
    for p, e in J["esitlik"].items():
        L.append(f"- {p}: {e['esit']} / {e['n']} bar birebir (tür {e['tur']}; S10 = 1 olan {e['S10_1']}, F68 = 1 olan {e['F68_1']})")
    L += ["", "## 3. GETİRİSİZ HUNİ (olay sayısı; pazar x hücre)", ""] + _mu_tablo_md(J["T"])
    L += ["", f"U1 ile U0'ın ortak L2 sayısı (ayrı günlerde ikisi de olay; uygulama yorumu 3): {J['ortak_L2_U1_U0']}", "",
          "## 4. GÜÇ BEKLENTİSİ (cetvel2_guc_v2.2.json, H 15, delta +0,02; n = eşli olay sayısı)", "",
          "| Hipotez | Pazar | Hücre | n | güç | beklenti |", "|---|---|---|---|---|---|"]
    for r in J["G"].itertuples():
        L.append(f"| {r.hipotez} | {r.pazar} | {r.hucre} | {r.n} | {r.guc:.2f} | {r.durum} |")
    L += ["", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "",
          "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    import IZ_KARNE as _IK
    for k in _IK.IK_KONTROL:
        y, kn = MU_KONTROL[k["kod"]]
        L.append(f"| {k['kod']} | {k['ad'] if 'ad' in k else k.get('madde', '')} | {y} | {kn} |")
    metin = "\n".join(L) + "\n"
    YH._yh_yaz(yol, metin, "MU ön kayıt")
    _IK.ik_kontrol_kapisi(yol)
    return yol


def _mu_onkayit_sha(metin: str, ad: str) -> Optional[str]:
    import re
    m = re.search(rf"^- {re.escape(ad)}(?: \([^)]*\))?: `([0-9a-f]{{64}})`", metin, flags=re.M)
    return m.group(1) if m else None


def mu_kapi(veri: Optional[str] = None, cikti: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Ölçüm kapısı: ön kayıt git'te ve değişmemiş, sha'lar aynı, kontrol listesi dolu, KASA kapısı açık, sonuc.json yok."""
    c = cikti or MU_YOL["cikti"]; yol = _mu_yol("onkayit", c)
    if not os.path.exists(yol):
        raise MUHata(f"ön kayıt yok: {yol}")
    if os.path.exists(_mu_yol("sonuc", c)):
        raise MUHata("sonuc.json var: ikinci koşu DURDU")
    metin = open(yol, encoding="utf-8").read()
    g = {}
    if git:
        rel = os.path.relpath(yol, KOK_MU)
        if _mu_git(["status", "--porcelain", "--", rel, "MACD_UYUM.py"]):
            raise MUHata("ön kayıt ya da MACD_UYUM.py git'te değişmiş / işlenmemiş -> DURDU")
        g["onkayit_commit"] = _mu_git(["log", "-1", "--format=%H %cI", "--", rel])
        if not g["onkayit_commit"]:
            raise MUHata("ön kayıt git'e işlenmemiş -> DURDU")
    S = mu_sha_simdi(veri)
    bozuk = [k for k, v in S.items() if _mu_onkayit_sha(metin, k) != v]
    if bozuk:
        raise MUHata(f"sha tutmuyor: {bozuk} -> DURDU")
    import IZ_KARNE as _IK
    kk = _IK.ik_kontrol_kapisi(yol)
    K = mu_kasa(veri)
    return {"onkayit": os.path.relpath(yol, KOK_MU), **g, "sha": S, "kontrol": kk["gecti"], "kasa": K, "metin": metin}


# ================================================================ 8) KOŞU
def mu_kos(veri: Optional[str] = None, cikti: Optional[str] = None, git: bool = True) -> Dict[str, Any]:
    """Kapı -> olay taraması (ön kayıttaki olay tablosu sha'sıyla aynı olmalı) -> mu_olc_hepsi."""
    c = cikti or MU_YOL["cikti"]
    G = mu_kapi(veri, c, git)
    zaman = _mu_simdi()
    mulog.info("kapı geçti (%s); koşu başlıyor %s", G.get("onkayit_commit", "-"), zaman)
    Os = []
    for p in MU_PAZAR:
        Pb = C2.c2_panel22_al(p, veri, None)
        O, _ = mu_pazar(p, veri, Pb["Vd"])
        Os.append(O)
    O = pd.concat(Os, ignore_index=True)
    if mu_olay_tablo_sha(O) != _mu_onkayit_sha(G["metin"], "OLAY_TABLO_SHA"):
        raise MUHata("olay tablosu ön kayıttakinden farklı -> DURDU")
    return mu_olc_hepsi(O, veri, c, G, zaman)


def mu_olc_hepsi(O: pd.DataFrame, veri: Optional[str], c: str, G: Dict[str, Any], zaman: str) -> Dict[str, Any]:
    """Prefix (K2) -> ANA R15 + R30 bilgi + İKİNCİL cetvel -> hüküm / karar / BH -> satır dosyası, yeniden üretim, sonuc.json, rapor."""
    t0 = time.time(); os.makedirs(c, exist_ok=True); pre = {}
    for pi, p in enumerate(MU_PAZAR):
        if (O.pazar == p).any():
            pre[p] = mu_prefix(C2.c2_panel22_al(p, veri, None)["Vd"], O[O.pazar == p].reset_index(drop=True), p, pi)
    ana, r30, ik = {}, {}, {}
    for hip in MU_HIP:
        ana[hip] = mu_olc_r(O, hip, 15, True, veri)
        r30[hip] = mu_olc_r(O, hip, 30, False, veri)
        ik[hip] = {}
        for p in sorted(O[O.hipotez == hip].pazar.unique()):
            ik[hip][p] = mu_olc_h5(O, hip, p, veri)
        mulog.info("%s ölçüldü (%.0f sn)", hip, time.time() - t0)
    # hücre tabloları
    H: Dict[str, Dict[str, Any]] = {hip: {f"{c_['pazar']}|{c_['hucre']}": c_ for c_ in ana[hip]["hucre"]} for hip in MU_HIP}
    H30: Dict[str, Dict[str, Any]] = {hip: {f"{c_['pazar']}|{c_['hucre']}": c_ for c_ in r30[hip]["hucre"]} for hip in MU_HIP}
    IK: Dict[str, Dict[str, Any]] = {}
    for hip in MU_HIP:
        IK[hip] = {}
        for p, Z in ik[hip].items():
            for h in MU_DONEM:
                IK[hip][f"{p}|{h}"] = mu_h5_hucre(Z[Z.hucre == h]) if len(Z) else {"n": 0}
    # U1 - U0
    S1, S0 = ana["U1"]["satir"], ana["U0"]["satir"]; u10 = {}
    for p in MU_PAZAR:
        for hi, h in enumerate(MU_DONEM):
            k = f"{p}|{h}"
            m1 = (S1.pazar == p) & (S1.donem == h) & np.isfinite(S1.fark_U1) if len(S1) else pd.Series([], dtype=bool)
            m0 = (S0.pazar == p) & (S0.donem == h) & np.isfinite(S0.fark_U0) if len(S0) else pd.Series([], dtype=bool)
            f1 = S1.fark_U1[m1].to_numpy(float) if len(S1) else np.array([]); f0 = S0.fark_U0[m0].to_numpy(float) if len(S0) else np.array([])
            a, b = mu_fark_boot(f1, pd.to_datetime(S1.giris[m1]).dt.strftime("%Y-%m").to_numpy() if len(f1) else np.array([]),
                                f0, pd.to_datetime(S0.giris[m0]).dt.strftime("%Y-%m").to_numpy() if len(f0) else np.array([]),
                                MU_PAZAR.index(p) * 10 + hi)
            u10[k] = {"n1": int(len(f1)), "n0": int(len(f0)), "fark": float(f1.mean() - f0.mean()) if len(f1) and len(f0) else np.nan,
                      "alt": a, "ust": b}
    karar = mu_karar(H["U1"], H["U0"])
    # BH (bilgi varyantları)
    aile = []
    for hip in MU_BILGI:
        for p in (["ABD"] if hip == "U1d" else MU_KARAR_PAZAR):
            for h in MU_DONEM:
                c_ = H[hip].get(f"{p}|{h}")
                if c_ and c_["n"] >= int(MU_ESIK["hucre"]["n_min"]) and np.isfinite(c_.get("p", np.nan)):
                    aile.append((hip, p, h, float(c_["p"])))
    bh = C2.c2_bh([x[3] for x in aile], float(MU_ESIK["bh"]["q"])) if aile else []
    bh_sat = [{"hipotez": a[0], "pazar": a[1], "hucre": a[2], "p": a[3], "dikkat": bool(b)} for a, b in zip(aile, bh)]
    # satır dosyası
    sat = []
    for hip in MU_HIP:
        S = ana[hip]["satir"]
        if not len(S):
            continue
        S = S.copy()
        S = S.rename(columns={f"es_r15_{hip}": "es_r15", f"n_es_{hip}": "n_es", f"sira_{hip}": "sira", f"fark_{hip}": "fark"})
        S["hipotez"] = hip
        Oh = O[O.hipotez == hip][["pazar", "sembol", "tarih", "L1_tarih", "L2_tarih", "F65", "F66", "F68", "S10", "s66", "dipte", "rsi_L1",
                                   "rsi_L2", "stop0", "close_t", "atrp_t"]]
        S = S.merge(Oh, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
        Zs = [Z for Z in ik[hip].values() if len(Z)]
        if Zs:
            Z = pd.concat(Zs, ignore_index=True)[["pazar", "sembol", "tarih", "h5", "h10", "st5", "es_h5", "es_h10", "es_st5", "k_es_h5", "pl_h5",
                                                   "getiri", "cikis_tur", "dd"]]
            S = S.merge(Z, on=["pazar", "sembol", "tarih"], how="left", validate="one_to_one")
        gsa = (S.get("cikis_tur", pd.Series([""] * len(S))).astype(str) == "giris_stop_otesi")
        S["giris_stop_alti"] = gsa.astype(int)
        S["stop_oldu"] = np.where(gsa, 1.0, S.get("st5", pd.Series(np.nan, index=S.index)))
        sat.append(S)
    SA = pd.concat(sat, ignore_index=True) if sat else pd.DataFrame()
    kol = ["hipotez", "pazar", "sembol", "tarih", "giris", "donem", "L1_tarih", "L2_tarih", "E0", "stop0", "giris_stop_alti", "h5", "h10",
           "st5", "stop_oldu", "r15", "es_r15", "n_es", "fark", "sira", "kova", "es_h5", "es_h10", "es_st5", "k_es_h5", "pl_h5", "getiri",
           "cikis_tur", "F65", "F66", "F68", "S10", "s66", "dipte", "rsi_L1", "rsi_L2", "close_t", "atrp_t"]
    SA = SA[[k for k in kol if k in SA.columns]]
    for k_ in ("tarih", "giris", "L1_tarih", "L2_tarih"):
        if k_ in SA:
            SA[k_] = pd.to_datetime(SA[k_]).dt.strftime("%Y-%m-%d")
    sy = _mu_yol("satir", c)
    SA.to_csv(sy, index=False, float_format="%.15g", compression={"method": "gzip", "mtime": 0})
    en_gec = KS.ks_en_gec_tarih(sy)
    yu = mu_yeniden(sy, H)
    J = {"surum": MU_SURUM, "zaman": zaman, "kapi": {k: v for k, v in G.items() if k != "metin"}, "prefix": pre,
         "ana": {hip: {k: H[hip][k] for k in H[hip]} for hip in MU_HIP}, "r30": {hip: H30[hip] for hip in MU_HIP}, "ikincil": IK,
         "u1_u0": u10, "karar": karar, "bh": bh_sat, "satir_dosya": os.path.relpath(sy, KOK_MU), "satir_sha": _mu_sha(sy),
         "satir_en_gec_tarih": str(en_gec.date()) if en_gec is not None else None, "yeniden": yu,
         "say": {hip: ana[hip]["say"] for hip in MU_HIP}, "sure_sn": round(time.time() - t0, 1)}
    _mu_jyaz(_mu_yol("sonuc", c), J, "MU sonuç")
    mu_rapor(c)
    mulog.info("koşu bitti: karar %s (%.0f sn)", karar["karar"], time.time() - t0)
    return J


def mu_yeniden(satir: str, H: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """K11: iki hücre (U1 ABD d1619, U0 AVR d2022) satır dosyasından düz pandas: n, ort FARK, ort SIRA, ort r15. Göreli 1e-9 değilse DURUR."""
    X = pd.read_csv(satir)
    out = {}
    for hip, p, h in (("U1", "ABD", "d1619"), ("U0", "AVR", "d2022")):
        g = X[(X.hipotez == hip) & (X.pazar == p) & (X.donem == h)]
        g = g[g.fark.notna() & g.r15.notna()]
        y = {"n": int(len(g)), "fark": float(g.fark.mean()) if len(g) else np.nan, "sira": float(g.sira.mean()) if len(g) else np.nan,
             "r15": float(g.r15.mean()) if len(g) else np.nan}
        c = H.get(hip, {}).get(f"{p}|{h}", {})
        k = {"n": int(c.get("n", 0)), "fark": c.get("fark", np.nan), "sira": c.get("sira", np.nan), "r15": c.get("r15_ort", np.nan)}
        tut = y["n"] == k["n"] and all((not np.isfinite(k[q]) and not np.isfinite(y[q])) or
                                         (np.isfinite(k[q]) and abs(y[q] - k[q]) <= 1e-9 * max(1.0, abs(k[q]))) for q in ("fark", "sira", "r15"))
        out[f"{hip} {p} {h}"] = {"kod": k, "yeniden": y, "tuttu": bool(tut)}
        if not tut:
            raise MUHata(f"yeniden üretim TUTMADI: {hip} {p} {h}: kod {k} / yeniden {y} -> DURDU")
    return out


# ================================================================ 9) RAPOR
def _y(x: Any, n: int = 2, yuzde: bool = True, isaret: bool = True) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "-"
    if not np.isfinite(v):
        return "-"
    v = v * 100 if yuzde else v
    s = f"{v:+.{n}f}" if isaret else f"{v:.{n}f}"
    return s.replace(".", ",")


def _s(x: Any, n: int = 2) -> str:
    return _y(x, n, False, False)


def mu_rapor(cikti: Optional[str] = None) -> str:
    c = cikti or MU_YOL["cikti"]; J = json.load(open(_mu_yol("sonuc", c), encoding="utf-8"))
    A, IK, U = J["ana"], J["ikincil"], J["u1_u0"]
    L = [f"# MACD_UYUM — RAPOR (K47 MACD pozitif uyumsuzluk, tek başına ve DİPTE)", "",
         f"Koşu {J['zaman']}; ön kayıt {J['kapi'].get('onkayit')} (git {J['kapi'].get('onkayit_commit', '-')}); süre {J['sure_sn']} sn. Veri KASA "
         f"açık kesik {J['kapi']['kasa']['kesik']} (satır dosyası en geç tarih {J['satir_en_gec_tarih']}). Evren bugün işlem gören hisseler: batanlar "
         "yok, dipteki olaylarda sonuç YUKARI yanlıdır (K7). Komisyon / kayma yok.", "",
         f"## KARAR (önceden yazılı kural): **{J['karar']['karar']}** — {J['karar']['neden']}", ""]
    if J["karar"].get("sonraki"):
        L += [f"Sonraki adım (yalnız öneri): {J['karar']['sonraki']}", ""]
    L += ["## 1. BULGU TABLOSU (ANA: CETVEL2 v2.2 R15; FARK = R15 olay - eş ortalaması, puan)", "",
          "| Hipotez | Hücre | n | R15 FARK [%95] | medyan FARK | SIRA [boot alt] | L3O | güç | plasebo FARK / + pay / - pay | HÜKÜM | gerekçe |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for hip in ("U1", "U0"):
        for p in MU_PAZAR:
            for h in MU_DONEM:
                r = A[hip].get(f"{p}|{h}")
                if not r:
                    L.append(f"| {hip} | {p} {h} | 0 | - | - | - | - | - | - | ÖLÇÜLEMEDİ | olay yok |"); continue
                hk = r["hukum"] if p in MU_KARAR_PAZAR else f"BİLGİ ({r['hukum']})"
                L.append(f"| {hip} | {p} {h} | {r['n']} | {_y(r['fark'])} [{_y(r['boot_alt'])}; {_y(r['boot_ust'])}] | {_y(r.get('fark_med'))} | "
                         f"{_s(r['sira'], 3)} [{_s(r.get('sira_alt'), 3)}] | {_y(r['l3o'])} | {_s(r['guc'])} | {_y(r.get('plasebo_fark'))} / "
                         f"{_y(r.get('plasebo_pay_arti'), 1, True, False)} / {_y(r.get('plasebo_pay_eksi'), 1, True, False)} | {hk} | {r['hukum_neden']} |")
    L += ["", "| U1 - U0 | Hücre | n U1 / U0 | FARK(U1) - FARK(U0) [%95 boot, bilgi] | > 0 ? |", "|---|---|---|---|---|"]
    for p in MU_PAZAR:
        for h in MU_DONEM:
            u = U[f"{p}|{h}"]
            L.append(f"| U1 - U0 | {p} {h} | {u['n1']} / {u['n0']} | {_y(u['fark'])} [{_y(u['alt'])}; {_y(u['ust'])}] | "
                     f"{'EVET' if u['fark'] is not None and np.isfinite(u['fark']) and u['fark'] > 0 else 'HAYIR'} |")
    L += ["", "### Getiri ve 1. tur cetveli (olay vs eş)", "",
          "| Hipotez | Hücre | r15 ort olay / eş | r15 medyan olay / eş | n (cetvel) | h5 olay / eş | h10 olay / eş | stop olay / eş | KAT5 [%95] | "
          "konum eşli KAT [%95] | plasebo KAT5 [%95] | giriş stop altı (STOP sayıldı: h5 / stop) | takip stoplu getiri ort / medyan |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for hip in ("U1", "U0"):
        for p in MU_PAZAR:
            for h in MU_DONEM:
                r = A[hip].get(f"{p}|{h}") or {}; q = IK.get(hip, {}).get(f"{p}|{h}") or {"n": 0}
                L.append(f"| {hip} | {p} {h} | {_y(r.get('r15_ort'))} / {_y(r.get('es_r15_ort'))} | {_y(r.get('r15_med_olc'))} / {_y(r.get('es_r15_med'))} | "
                         f"{q.get('n', 0)} | {_y(q.get('p_h5'), 1, True, False)} / {_y(q.get('es_h5'), 1, True, False)} | "
                         f"{_y(q.get('p_h10'), 1, True, False)} / {_y(q.get('es_h10'), 1, True, False)} | {_y(q.get('p_st5'), 1, True, False)} / "
                         f"{_y(q.get('es_st5'), 1, True, False)} | {_s(q.get('kat5'))} [{_s(q.get('kat5_alt'))}; {_s(q.get('kat5_ust'))}] | "
                         f"{_s(q.get('k_kat5'))} [{_s(q.get('k_kat5_alt'))}; {_s(q.get('k_kat5_ust'))}] | {_s(q.get('pl_kat5'))} "
                         f"[{_s(q.get('pl_kat5_alt'))}; {_s(q.get('pl_kat5_ust'))}] | {q.get('giris_stop_alti', 0)} "
                         f"({_y(q.get('p_h5_stopdahil'), 1, True, False)} / {_y(q.get('p_st5_stopdahil'), 1, True, False)}) | "
                         f"{_y(q.get('getiri_ort'))} / {_y(q.get('getiri_med'))} |")
    L += ["", "## 2. BİLGİ VARYANTLARI (hüküm yok)", "",
          "| Hipotez | Hücre | n | R15 FARK [%95] | SIRA | r15 olay / eş | h5 olay / eş | stop olay / eş | KAT5 [%95] | R30 FARK [%95] (n) | p | BH |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    bhd = {(b["hipotez"], b["pazar"], b["hucre"]): b for b in J["bh"]}
    for hip in MU_BILGI:
        for p in (["ABD"] if hip == "U1d" else MU_PAZAR):
            for h in MU_DONEM:
                r = A[hip].get(f"{p}|{h}") or {}; q = IK.get(hip, {}).get(f"{p}|{h}") or {}; r3 = J["r30"].get(hip, {}).get(f"{p}|{h}") or {}
                b = bhd.get((hip, p, h))
                L.append(f"| {hip} | {p} {h} | {r.get('n', 0)} | {_y(r.get('fark'))} [{_y(r.get('boot_alt'))}; {_y(r.get('boot_ust'))}] | "
                         f"{_s(r.get('sira'), 3)} | {_y(r.get('r15_ort'))} / {_y(r.get('es_r15_ort'))} | {_y(q.get('p_h5'), 1, True, False)} / "
                         f"{_y(q.get('es_h5'), 1, True, False)} | {_y(q.get('p_st5'), 1, True, False)} / {_y(q.get('es_st5'), 1, True, False)} | "
                         f"{_s(q.get('kat5'))} [{_s(q.get('kat5_alt'))}; {_s(q.get('kat5_ust'))}] | {_y(r3.get('fark'))} [{_y(r3.get('boot_alt'))}; "
                         f"{_y(r3.get('boot_ust'))}] ({r3.get('n', 0)}) | {_s(r.get('p'), 4)} | "
                         f"{('bilgi: dikkat' if b['dikkat'] else 'geçmedi') if b else '-'} |")
    L += ["", "R30 (bilgi; CETVEL2 v2.2 tanımı, tekil 30) U1 / U0:", ""]
    for hip in ("U1", "U0"):
        L.append("- " + hip + ": " + "; ".join(f"{p} {h} n {J['r30'][hip].get(f'{p}|{h}', {}).get('n', 0)} FARK "
                                            f"{_y(J['r30'][hip].get(f'{p}|{h}', {}).get('fark'))}" for p in MU_PAZAR for h in MU_DONEM))
    hy = _mu_yol("huni", c)
    if os.path.exists(hy):
        Hj = json.load(open(hy, encoding="utf-8"))
        L += ["", "## 3. HUNİ (getirisiz; ön kayıttakiyle aynı dosya)", ""] + _mu_tablo_md(pd.DataFrame(Hj["huni"]))
        L += ["", f"U1 ile U0'ın ortak L2 sayısı: {Hj.get('ortak_L2_U1_U0')}"]
    ey = _mu_yol("esitlik", c)
    if os.path.exists(ey):
        Ej = json.load(open(ey, encoding="utf-8"))
        L += ["", "yh_s10_bar eşitliği (ön kayıttan önce): " + "; ".join(f"{p} {e['esit']} / {e['n']} bar birebir (S10 = 1: {e['S10_1']})"
                                                                     for p, e in Ej.items())]
    L += ["", "## 4. DENETİMLER", "",
          "- Prefix (K2; veri t'de kesilip yeniden tarandı): " + "; ".join(f"{p} {v['tuttu']} / {v['n']}" for p, v in J["prefix"].items()),
          "- Yeniden üretim (K11; satır dosyasından düz pandas): " + "; ".join(f"{k} {'TUTTU' if v['tuttu'] else 'TUTMADI'} (n {v['yeniden']['n']}, "
                                                                           f"FARK {_y(v['yeniden']['fark'], 4)})" for k, v in J["yeniden"].items()),
          f"- Satır dosyası: {J['satir_dosya']} (sha {J['satir_sha'][:16]}…)",
          f"- OC / c2 sayımı (U1): {json.dumps(J['say'].get('U1', {}), ensure_ascii=False)[:600]}"]
    hk = os.path.join(c, "uyum_hata.json")
    L += ["", "## HATA", ""]
    L += [f"- {x}" for x in (json.load(open(hk, encoding="utf-8")) if os.path.exists(hk) else ["(kayıt yok)"])]
    import IZ_KARNE as _IK
    L += ["", "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; ön kayıttaki tablo)", "", "| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |",
          "|---|---|---|---|"]
    L += [f"| {k['kod']} | {k['ad']} | {MU_KONTROL[k['kod']][0]} | {MU_KONTROL[k['kod']][1]} |" for k in _IK.IK_KONTROL]
    L += ["", "Colab notu: MACD_UYUM.py yeni; Colab'da kullanılırsa çalışma zamanını yeniden başlatın, sonra exec(open('MACD_UYUM.py').read())."]
    metin = "\n".join(L) + "\n"
    YH._yh_yaz(_mu_yol("rapor", c), metin, "MU rapor")
    return metin


# ================================================================ 10) ÇAKIŞMA KAPISI
def _cakisma_kontrol_mu(_once=_CK_ONCE_MU, _dosya="MACD_UYUM.py"):
    """Çakışma kapısı: bu dosya bellekteki mevcut bir adı (başka dosyanın) ezdiyse durur."""
    g = globals(); kayit = g.setdefault("_CK_KAYIT", {})
    atla = ("_CK_ONCE_MU", "_CK_KAYIT", "_cakisma_kontrol_mu", "In", "Out", "_", "_i", "_ii", "_iii", "get_ipython", "exit", "quit")
    std = ("os", "sys", "np", "pd", "json", "logging", "math", "hashlib", "subprocess", "time", "copy", "_dt", "annotations", "Any", "Dict",
           "List", "Optional", "Tuple", "_swv", "C2", "KS", "OC", "PK", "YH")
    degisen = [k for k, i in _once.items() if k in g and id(g[k]) != i and not k.startswith("__") and k not in atla
               and not (k.startswith("_i") and k[2:].isdigit()) and not (k.startswith("_") and k[1:].isdigit())]
    ezilen = sorted(k for k in degisen if kayit.get(k) != _dosya and k not in std)
    for k in [k for k in g if k not in _once and not k.startswith("__") and k not in atla] + degisen:
        kayit[k] = _dosya
    if ezilen:
        raise RuntimeError(f"{_dosya}: bellekteki şu adları EZDİ -> {ezilen}")


_cakisma_kontrol_mu()


def _mu_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=MU_SURUM)
    alt = ap.add_subparsers(dest="komut", required=True)
    for k in ("esitlik", "onkayit", "kos", "rapor", "sha"):
        p = alt.add_parser(k); p.add_argument("--veri", default=None); p.add_argument("--cikti", default=None)
        if k == "onkayit":
            p.add_argument("--uzerine", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.komut == "esitlik":
            mu_kasa(a.veri)
            for pi, p in enumerate(MU_PAZAR):
                Pb = C2.c2_panel22_al(p, a.veri, None)
                O, _ = mu_pazar(p, a.veri, Pb["Vd"])
                print(json.dumps(mu_esitlik(Pb["Vd"], O, p, pi), ensure_ascii=False, default=_mu_json))
        elif a.komut == "onkayit":
            print("ÖN KAYIT:", mu_onkayit_yaz(a.veri, a.cikti, a.uzerine))
        elif a.komut == "kos":
            J = mu_kos(a.veri, a.cikti)
            print("KOŞU TAMAM:", J["karar"]["karar"], "-", J["karar"]["neden"])
        elif a.komut == "rapor":
            print(mu_rapor(a.cikti))
        else:
            print(json.dumps(mu_sha_simdi(a.veri), ensure_ascii=False, indent=1))
    except MUHata as ex:
        mulog.error("%s", ex)
        print(f"DURDU: {ex}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__" and "get_ipython" not in globals():
    sys.exit(_mu_ana())
