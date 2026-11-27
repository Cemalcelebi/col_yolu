"""WEB_DESEN — web'de anlatılan bilinen mum / likidite desenleri: yapay örneğini kur, dedektörü yapay pozitif / negatif örneklerle sına, gerçek veride
sonrasını iş tanımındaki sabit ölçülerle ölç (27 Kasım 2026).

İş tanımı: arastirma_cikti/web_desen/WD_IS_TANIMI.md (ana model; eşikler sabit). Desen kolları: W1 üç beyaz asker, W1T üç kara karga, W2 / W2T fitille dip /
tepe süpürme, W2E / W2TE eşit dipler / tepeler süpürmesi, W3 / W3T kaplumbağa çorbası +1, W4 / W4Y süpürme + yapı kırılımı + geri test, W5 / W5Y tuzak (2B),
W6 / W6T çekiç / kayan yıldız, W7 / W7D / W7T emilim vekili (durdurma hacmi). Her dedektör yalnız o barın sonuna kadarki veriyi kullanır (test: sonrası
bozulunca / kesilince aynı olay).

Veri / evren / geçerli bar / ATRP20 / T1 / PİYASA(t) / ay kümeli bootstrap: YUKSELIS_ONCESI ile aynı (içe alınır; YO'nun hazırladığı ham_{pazar}.npz paneli
ve ozellik_{pazar}.pkl örnek günleri okunur, hacim MI.mi_veri'den). HACİM yalnız W7 kollarında. Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ.

Komut:  python WEB_DESEN.py sentetik    yapay pozitif / negatif sınaması -> arastirma_cikti/web_desen/wd_sentetik.json
        python WEB_DESEN.py yapay_pdf   WD_YAPAY_DESENLER.pdf (desen başına bir sayfa; YAPAY VERİ)
        python WEB_DESEN.py olay        gerçek veride olaylar (GETİRİSİZ) -> /root/.kasa/ham/web_desen/olay_*.pkl + sayim.json
        python WEB_DESEN.py onkayit     WD_ON_KAYIT.md (mühürler + sayım + sentetik + yorum noktaları + kontrol tablosu)
        python WEB_DESEN.py olcum       kapı -> sonrası ölçümü (bir kez) -> wd_sonuc.json + wd_ozet.csv
        python WEB_DESEN.py rapor       WD_RAPOR.md (sonuç json'undan)
        python WEB_DESEN.py gercek_pdf  WD_GERCEK_ORNEKLER.pdf (desen başına 4 rastgele gerçek örnek; SONRASI YOK)
        python WEB_DESEN.py sha         kod / eşik sha
Colab:  exec(open('WEB_DESEN.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı; aşağı yönlü desenlerin aleyhine, yukarı yönlülerin lehine).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_WD = {k: id(v) for k, v in globals().items()}

import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_WD = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_WD not in sys.path:
    sys.path.insert(0, KOK_WD)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; veri, yazma, sha, git, mum çizimi)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; kesik kapısı, hücre adı, ay özeti, BH, json sha)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; panel, örnek günler, P15)

wdlog = logging.getLogger("col.web_desen")
if not wdlog.handlers:
    _wd_h = logging.StreamHandler(sys.stderr)
    _wd_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s web_desen: %(message)s", "%H:%M:%S"))
    wdlog.addHandler(_wd_h)
    wdlog.setLevel(logging.INFO)
    wdlog.propagate = False


class WDHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / sıra / yeniden üretim uyuşmazlığı."""


WD_SURUM = "WEB_DESEN v1.0 (2026-11-27): web desenleri, yapay sınama + gerçek veride sonrası"
WD_YOL = {"cikti": os.path.join(KOK_WD, "arastirma_cikti", "web_desen"), "kod": os.path.join(KOK_WD, "WEB_DESEN.py"),
          "ham": os.environ.get("WD_HAM", "/root/.kasa/ham/web_desen"), "yo_ham": YO.YO_YOL["ham"], "acik": YO.YO_YOL["acik"]}
WD_DOSYA = {"sentetik": "wd_sentetik.json", "yapay_pdf": "WD_YAPAY_DESENLER.pdf", "onkayit": "WD_ON_KAYIT.md", "sonuc": "wd_sonuc.json",
            "ozet": "wd_ozet.csv", "rapor": "WD_RAPOR.md", "gercek_pdf": "WD_GERCEK_ORNEKLER.pdf"}
WD_KESIK = pd.Timestamp("2022-12-31")
WD_PAZAR = ("ABD", "AVR")
WD_HUCRE = ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022")

# kol -> yön (+1 yukarı / -1 aşağı), ad, kaynak
WD_KOL: Dict[str, Dict[str, Any]] = {
    "W1": {"yon": 1, "ad": "Üç beyaz asker", "kaynak": "Bulkowski, 'Top 10 Candles That Work' (Stocks & Commodities); kırılım yönü oranı %82-84"},
    "W1T": {"yon": -1, "ad": "Üç kara karga", "kaynak": "Bulkowski, 'Top 10 Candles That Work'; kırılım yönü oranı %78-79"},
    "W2": {"yon": 1, "ad": "Dip süpürme (fitille)", "kaynak": "VT Markets 'liquidity sweep' sayfası (Cemal'in verdiği); sayı vermiyor"},
    "W2T": {"yon": -1, "ad": "Tepe süpürme (fitille)", "kaynak": "Cemal'in şeması + VT Markets; sayı vermiyor"},
    "W2E": {"yon": 1, "ad": "Eşit dipler süpürmesi", "kaynak": "VT Markets / şema ('equal lows = retail liquidity'); sayı vermiyor"},
    "W2TE": {"yon": -1, "ad": "Eşit tepeler süpürmesi", "kaynak": "Cemal'in şeması ('Equal Highs - Retail Liquidity'); sayı vermiyor"},
    "W3": {"yon": 1, "ad": "Kaplumbağa çorbası +1", "kaynak": "Connors & Raschke, Street Smarts (Turtle Soup Plus One; LuxAlgo / TradingMarkets aktarımı)"},
    "W3T": {"yon": -1, "ad": "Kaplumbağa çorbası +1 (tepe)", "kaynak": "Connors & Raschke (ayna)"},
    "W4": {"yon": -1, "ad": "Süpürme + yapı kırılımı + geri test", "kaynak": "Cemal'in şeması (Liquidity Sweep Wick, Break of Structure, Entry, Stop, Target)"},
    "W4Y": {"yon": 1, "ad": "Süpürme + yapı kırılımı + geri test (dip)", "kaynak": "Cemal'in şeması (ayna)"},
    "W5": {"yon": -1, "ad": "Tuzak / 2B (tepe)", "kaynak": "Sperandeo 2B kuralı (aracı kurum blogu aktarımı)"},
    "W5Y": {"yon": 1, "ad": "Tuzak / 2B (dip)", "kaynak": "Sperandeo 2B (ayna)"},
    "W6": {"yon": 1, "ad": "Çekiç", "kaynak": "LuxAlgo çekiç tanımı; Bulkowski çekiç kırılım yönü ~%60"},
    "W6T": {"yon": -1, "ad": "Kayan yıldız", "kaynak": "LuxAlgo (ayna); Bulkowski kayan yıldız ~%59"},
    "W7": {"yon": 1, "ad": "Emilim vekili (durdurma hacmi)", "kaynak": "Trader Dale emilim (mum içi alış / satış ister; bu günlük vekil) + LuxAlgo VSA durdurma hacmi"},
    "W7D": {"yon": 1, "ad": "Emilim vekili, dar aralık", "kaynak": "VSA 'çaba var sonuç yok' (LuxAlgo)"},
    "W7T": {"yon": -1, "ad": "Emilim vekili (tepe)", "kaynak": "VSA (ayna)"},
}
WD_KOLLAR = list(WD_KOL)
WD_ICGIRIS = ("W3", "W3T", "W4", "W4Y")             # giriş bar içinde bir seviyede (ötekiler: sinyal barından sonraki açılış)

# ================================================================ MÜHÜRLÜ EŞİK SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
WD_ESIK: Dict[str, Any] = {
    "surum": "WD-1.0",
    "ortak": {"ort_boy": 10, "atr": 20, "uc_pencere": 20, "uc_yas": 4, "uc_yas_w3": 3, "baglam": 10,
              "tanim": "boy = H - L; gövde = |C - O|; üst fitil = H - max(O, C); alt fitil = min(O, C) - L; ORT_BOY(i) = i'den önceki 10 barın boy medyanı "
                       "(desenin İLK barının ORT_BOY'u bütün desen mumları için); ATR(i) = TR'nin (önceki kapanışla; ilk bar H - L) i dahil 20 bar ortalaması "
                       "(YO ATRP20 x C); PL(i) / PH(i) = i'den önceki 20 barın (i-20 .. i-1) en düşük L / en yüksek H'si; YAŞ = i - (bu ucun SON görüldüğü bar); "
                       "YAŞ < 4 ise (W3'te < 3) PL / PH yok sayılır (olay yok); DÜŞÜŞ bağlamı(ilk) = C[ilk-1] < C[ilk-11]; YÜKSELİŞ = C[ilk-1] > C[ilk-11]; "
                       "yerel dip i: L_i < L_{i-1}, L_i < L_{i-2}, L_i <= L_{i+1}, L_i <= L_{i+2} (YO YUKSELEN_DIP tanımı); yerel tepe aynası; yerel uç yalnız "
                       "i + 2 barı tamamlandıktan sonra kullanılır"},
    "W1": {"tepe_pay": 0.25, "tanim": "art arda 3 yeşil (C > O) mum a, b, c; her birinin boyu > ORT_BOY(a); C_a < C_b < C_c; her mumda H - C <= 0,25 x boy; "
                                      "O_b ∈ [O_a, C_a] ve O_c ∈ [O_b, C_b] (sınır dahil); DÜŞÜŞ(a). Giriş c'den sonraki açılış; stop L_a. W1T aynası (kırmızı, C - L "
                                      "<= 0,25 boy, kapanışlar düşen, açılış önceki gövde içinde, YÜKSELİŞ(a), stop H_a)"},
    "W2": {"fitil_pay": 0.5, "stop_atr": 0.1, "tanim": "L_t < PL_t ve C_t > PL_t ve alt fitil >= 0,5 x boy (YAŞ >= 4). Giriş t + 1 açılış; stop L_t - 0,1 ATR_t. "
                                                       "W2T aynası (stop H_t + 0,1 ATR_t)"},
    "W2E": {"atr_pay": 0.25, "ara_fark": 4, "tanim": "W2 + t'den önceki 20 barda (t-20 .. t-1; i + 2 <= t - 1) |L_i - PL_t| <= 0,25 ATR_t olan yerel dipler "
                                                     "içinde indeks farkı >= 4 ('aralarında en az 3 bar') olan en az iki dip. W2TE aynası"},
    "W3": {"tik": 0.999, "tanim": "t: C_t <= PL_t (YAŞ >= 3); t + 1: H_{t+1} >= PL_t ise giriş = O_{t+1} >= PL_t ise O_{t+1}, değilse PL_t; ulaşmazsa olay yok "
                                  "(girişsiz aday). Stop = min(L_t, L_{t+1}) x 0,999. W3T aynası (C_t >= PH_t; L_{t+1} <= PH_t; giriş O_{t+1} <= PH ise açılış, "
                                  "değilse PH; stop max(H_t, H_{t+1}) x 1,001)"},
    "W4": {"bos_bar": 10, "test_bar": 5, "tanim": "W2T olayı s; seviye = s'den önce tamamlanmış son yerel dibin L'si (i + 2 <= s - 1); yapı kırılımı b = s+1 .. "
                                                  "s+10 içinde ilk C_b < seviye; giriş e = b+1 .. b+5 içinde ilk H_e >= seviye: giriş = O_e >= seviye ise O_e (açılış "
                                                  "seviyeyi geçmiş), değilse seviye (satış). Stop H_s. W4Y aynası (W2 olayı, son yerel tepe H'si, C_b > seviye, L_e <= "
                                                  "seviye, giriş O_e <= seviye ise O_e değilse seviye, stop L_s)"},
    "W5": {"geri_bar": 3, "tanim": "t: C_t > PH_t (YAŞ >= 4); u = t+1 .. t+3 içinde ilk C_u < PH_t; giriş u + 1 açılışında satış; stop = max(H_t .. H_u). W5Y "
                                   "aynası (C_t < PL_t, C_u > PL_t, alış, stop min(L_t .. L_u))"},
    "W6": {"alt_govde": 2.0, "ust_pay": 0.1, "boy_ort": 0.8, "dip_bar": 10,
           "tanim": "alt fitil >= 2 x gövde; üst fitil <= 0,1 x boy; boy >= 0,8 x ORT_BOY(t); L_t = min(L_{t-9..t}); DÜŞÜŞ(t). Giriş t + 1 açılış; stop L_t. "
                    "W6T aynası (üst fitil >= 2 x gövde; alt fitil <= 0,1 boy; H_t = max(H_{t-9..t}); YÜKSELİŞ(t); stop H_t)"},
    "W7": {"hacim_kat": 2.0, "hacim_pencere": 20, "kapanis_pay": 0.5, "dip_bar": 20,
           "tanim": "DÜŞÜŞ(t); L_t = min(L_{t-19..t}); V_t >= 2 x medyan(V_{t-20..t-1}); (C - L) / boy >= 0,5. Giriş t + 1 açılış; stop L_t. W7D: ayrıca boy <= "
                    "ORT_BOY(t). W7T: YÜKSELİŞ(t); H_t = max(H_{t-19..t}); aynı hacim şartı; (C - L) / boy <= 0,5; stop H_t"},
    "filtre": {"sira": ["GIRIS_YOK", "STOP_TERS", "BOSLUK", "UFUK_KESIK", "DONEM_DISI", "EVREN_DISI", "KILITLI", "T1_YOK", "TEKIL"],
               "giris_bosluk": 10, "pencere_satir": 30, "kilitli_pay": 0.20, "tekil_bar": 5, "t1_en_az": 30,
               "tanim": "GIRIS_YOK: giriş barı veride yok; STOP_TERS: giriş stopun yanlış tarafında ya da R = 0; BOSLUK: giriş barı satırı - sinyal barı satırı > "
                        "10 birleşik takvim satırı; UFUK_KESIK: e + 14 barı yok, tarihi > 2022-12-31 ya da e .. e+14 > 30 takvim satırı; DONEM_DISI: giriş "
                        "2016-01-01 .. 2022-12-31 dışında; EVREN_DISI: giriş satırında P2 değil (YO evreni); KILITLI: desenin ilk barı .. giriş barı takvim "
                        "aralığında ham veride geçersiz bar payı (MUM_IZI_UC.uc_kilitli_pay) > 0,20; T1_YOK: aynı hisse aynı hücrede YO örnek günü < 30; "
                        "TEKIL: aynı hisse aynı kolda önceki tutulan olayın giriş barından < 5 bar sonra giriş"},
    "olcu": {"ufuk": 15, "atr_hedef": 2.0, "atr_stop": 1.0, "R_hedef": 2.0, "yon_bar": 10,
             "tanim": "barlar e .. e+14 (giriş barı dahil; YO gibi); R15 = C[e+14] / giriş - 1; TOPLAM FARK = yön x (R15 - T1), T1 = aynı hissenin aynı hücredeki "
                      "YO örnek günlerinin (k % 5 == 0, P2) R15 ortalaması (giriş O[k+1], C[k+15]); SEÇİM = yön x (R15 - P15(e satırı)) (YO.yo_P15); ATR HEDEFİ "
                      "= yönde giriş ± 2 x ATR(e-1)'e ters yönde 1 x ATR(e-1) görmeden ulaşma (aynı barda ikisi = STOP ÖNCE); taban = aynı hissenin aynı "
                      "hücredeki örnek günlerinde (giriş O[k+1], ATR(k)) aynı yöndeki pay; KAT = Σ isabet / Σ taban(hisse-hücre); KAYNAK STOPU: R = |giriş - stop|, "
                      "hedef giriş ± 2R, stop seviyesi; aynı bar = stop önce; taban = aynı hissenin aynı hücredeki örnek günlerinde aynı R / giriş oranıyla pay; "
                      "R KATI = yön x (çıkış - giriş) / R, çıkış = stopa ilk dokunulan bar (e'den sonraki barda açılış stopun ötesindeyse açılış) yoksa C[e+14]; "
                      "10 GÜN YÖN (bilgi) = yön x (C[e+9] - giriş) > 0; taban aynı hissenin örnek günlerinde C[k+10] / O[k+1] - 1 yönde"},
    "boot": {"B": 10000, "tohum": 2711, "kume": "giriş ayı (YYYY-AA)",
             "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık, kol x hücre başına bir W; np.random.default_rng([2711, crc32(kol|hücre)])); "
                      "ortalama ve KAT her tekrarda ağırlıklı toplamlardan; %95 = 2,5 / 97,5 yüzdelik; T1 / taban sabit",
             "p": "tek yönlü p = (1 + #(istatistik* <= sıfır noktası)) / (B + 1); sıfır noktası TOPLAM FARK'ta 0, KAT'ta 1"},
    "bh": {"q": 0.10, "aile": "17 desen kolu; kol p'si = max(p_TF ABD 2016-19, p_TF ABD 2020-22, p_KAT ABD 2016-19, p_KAT ABD 2020-22) (kesişim-birleşim)"},
    "hukum": {"n_min": 300, "ay_min": 12, "avr_n": 100,
              "sira": "ÖLÇÜLEMEDİ (ABD hücrelerinden birinde n < 300 ya da farklı ay < 12) > TUTAR > TERS > TEK DÖNEM > TUTMADI",
              "TUTAR": "ABD 2016-19 ve 2020-22'de TOPLAM FARK > 0 ve alt > 0 VE ATR KAT > 1 ve alt > 1 VE AVR iki dönemde (n >= 100 olan hücrelerde) TOPLAM "
                       "FARK nokta değeri > 0 VE BH (q 0,10) geçer",
              "TERS": "ABD iki dönemde de TOPLAM FARK üst ucu < 0",
              "TEK_DONEM": "ABD şartları (TF ve KAT alt uçları) yalnız bir dönemde", "TUTMADI": "ötekiler (ABD iki dönemde geçip AVR / BH'de kalan dahil)",
              "avr_not": "AVR hücresi n < 100 ise o hücre şartı aranmaz ve 'AVR n < 100' notu yazılır"},
    "sentetik": {"olcek": [5.0, 50.0, 500.0], "oyn": [0.004, 0.008], "tohum_sayi": 25, "gurultu": [0.0, 0.10, 0.20], "hedef_yakala": 0.90, "hedef_kabul": 0.05,
                 "rastgele": {"seri": 200, "uzunluk": 300},
                 "tanim": "pozitif: desen şeması gibi kurulmuş yapay mumlar rastgele yürüyüşe gömülü; gürültü = desen barlarının O/H/L/C'sine N(0, g x boy) "
                          "(sonra H = max, L = min); yakalama = beklenen giriş barında o kolun olayı; negatif (yakın ama değil): desen bölgesinde (ilk bar .. "
                          "beklenen giriş + 2) o kolun herhangi bir olayı = yanlış kabul; rastgele seri: 1000 barda olay sıklığı (gerçek veriyle yan yana)"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her pazar) + KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl, '2022-12-31')",
    "sira": "kod + sentetik + yapay PDF -> getirisiz sayım -> ön kayıt commit + push -> ik_kontrol_kapisi -> ölçüm (bir kez) -> rapor + gerçek örnek PDF",
}

WD_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hisse aynı hücre (pazar x dönem) YO örnek günleri: TOPLAM FARK = hissenin kendi dönem ortalamasına göre (T1); ATR hedefi KAT ve +2R "
                   "payı aynı hissenin rastgele günleriyle, +2R tabanında aynı R / giriş oranı (desen stopunun mekanik etkisi dışlanır); SEÇİM aynı gün piyasa "
                   "P15'i; aşağı desenlerde işaret çevrilir"),
    "K2": ("EVET", "her dedektör yalnız giriş barına kadarki veriyle (test: giriş barından sonraki barlar bozulunca ve seri kesilince olaylar aynı); yerel uç "
                   "i + 2 tamamlanınca (test); PL / PH önceki 20 bar; ATR hedefinde ATR(e-1); sonuç fonksiyonları ayrı ve yalnız ölçüm kapısından sonra; veri "
                   "<= 2022-12-31 assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0, fiyat sonlu > 0); kilitli / hacimsiz / fiyat adımına yapışmış bar payı > 0,20 olan desen penceresi "
                   "atılır (MUM_IZI_UC.uc_kilitli_pay); 15 bar <= 30 takvim satırı; giriş boşluğu <= 10 satır"),
    "K4": ("EVET", "aynı hisse aynı kolda 5 bar içindeki ikinci olay atılır (atılan sayı yazılır); çıkarım ay kümeli bootstrap; n olay ve farklı ay ayrı; "
                   "en kalabalık 3 ay payı; medyan R15 ve medyan R katı bilgi"),
    "K5": ("EVET", "giriş = sinyal barından sonraki açılış (W1, W2, W5, W6, W7); W3 / W4'te kaynak kuralı: seviyeye dokunulunca seviyede, açılış seviyeyi geçmişse "
                   "açılışta (test); sinyal barı kapanışı kullanılmaz"),
    "K6": ("EVET", "YO paneli (OS / MI bölünme düzeltmeli açık kopya); getiriler oransal, yerel para; pazar içi taban; hacim yalnız hisse içi oran (W7)"),
    "K7": ("EVET", "evren bugün yaşayan hisseler: sonuç yukarı yanlı; aşağı yönlü desenlerin aleyhine, yukarı yönlülerin lehine; raporda yazılır"),
    "K8": ("EVET", "n < 300 ya da farklı ay < 12 -> ÖLÇÜLEMEDİ; ABD iki dönem + AVR iki dönem; BH q 0,10 (17 kol); AVR n < 100 hücrede şart aranmaz (not)"),
    "K9": ("EVET", "WD_ON_KAYIT.md: WD_KOD_SHA, WD_ESIK_SHA, olay dosyası ve YO panel sha'ları, SAYIM_SHA, sentetik sonuçları; ölçüm kapısı: kontrol + sha + "
                   "commit + temiz ağaç + KASA; ikinci koşu durur; eşikler sonuçtan sonra değişmez"),
    "K10": ("EVET", "hacim sütunu ve kapanışlar YO panel deposuyla bar bar eşit (assert); olay dosyası şeması sayımda; dedektörler elle kurulmuş yapay seriler ve "
                    "pozitif / negatif sentetik setle sınandı"),
    "K11": ("EVET", "rapordan önce >= 3 satır (kol x hücre) olay dosyası + ham panelden bağımsız kısa kodla yeniden üretilir; fark DUR"),
    "K12": ("EVET", "'TUTAR' yalnız hüküm kuralının bütün şartları sağlanınca; Bulkowski oranları 'kırılım yönü' oranıdır, bizim 10 gün yön payı ile yan yana ama "
                    "aynı ölçü değil; sayı ile yorum ayrı cümlede; evren notu"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_wd); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı "
                    "taraması MI._mi_yaz; SEKIL_DEVAM'a dokunulmaz / import edilmez; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _wd_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or WD_YOL["cikti"], WD_DOSYA[ad])


def _wd_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or WD_YOL["ham"], ad)


def wd_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or WD_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def wd_kod_sha() -> str:
    return MI._mi_sha(WD_YOL["kod"])


def _wd_rng(anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(WD_ESIK["boot"]["tohum"]), zlib.crc32(str(anahtar).encode("utf-8"))])


def wd_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri") -> pd.Timestamp:
    try:
        return HV.hv_kesik_kapi(V, ad, WD_KESIK)
    except HV.HVHata as ex:
        raise WDHata(str(ex)) from ex


def wd_tarih_kapi(tarih: Any, ad: str = "panel") -> None:
    """Kesik assert (mekanik): panel takviminde 2022-12-31 sonrası tarih varsa DUR."""
    t = pd.DatetimeIndex(np.asarray(tarih))
    if len(t) and t.max() > WD_KESIK:
        raise WDHata(f"KESİK AŞIMI: {ad} en geç {t.max().date()} > {WD_KESIK.date()} (KASA açılmaz)")


# ================================================================ 1) ORTAK ÖLÇÜLER (yalnız i barına kadarki veri)
def _wd_roll(x: np.ndarray, w: int, f: str) -> np.ndarray:
    return getattr(pd.Series(np.asarray(x, float)).rolling(w, min_periods=w), f)().to_numpy(float)


def _wd_once(x: np.ndarray, k: int = 1) -> np.ndarray:
    """x'i k bar sağa kaydır (i'deki değer = x[i-k])."""
    x = np.asarray(x, float)
    return np.r_[np.full(min(k, len(x)), np.nan), x[:-k]] if k else x.copy()


def wd_uc(x: np.ndarray, w: int, tur: str) -> Tuple[np.ndarray, np.ndarray]:
    """i'den önceki w barın (i-w .. i-1) en düşüğü ('min') / en yükseği ('max') ve YAŞI = i - (ucun SON görüldüğü bar). i < w -> NaN."""
    x = np.asarray(x, float); m = len(x); deger = np.full(m, np.nan); yas = np.full(m, np.nan)
    if m <= w:
        return deger, yas
    Wv = np.lib.stride_tricks.sliding_window_view(x[:-1], w)               # satır q = x[q .. q+w-1] -> i = q + w
    rev = Wv[:, ::-1]
    a = np.argmin(rev, axis=1) if tur == "min" else np.argmax(rev, axis=1)    # sondan indeks (eşitlerde en son görülen)
    deger[w:] = rev[np.arange(len(rev)), a]; yas[w:] = a + 1
    return deger, yas


def wd_yerel(L: np.ndarray, H: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Yerel dip / tepe (YO YUKSELEN_DIP tanımı; i - 2 >= 0, i + 2 < m). Kullanan, i + 2 barının tamamlanmış olmasını ayrıca şart koşar."""
    m = len(L); D = np.zeros(m, bool); T = np.zeros(m, bool)
    if m >= 5:
        i = np.arange(2, m - 2)
        D[i] = (L[i] < L[i - 1]) & (L[i] < L[i - 2]) & (L[i] <= L[i + 1]) & (L[i] <= L[i + 2])
        T[i] = (H[i] > H[i - 1]) & (H[i] > H[i - 2]) & (H[i] >= H[i + 1]) & (H[i] >= H[i + 2])
    return D, T


def wd_son_uc(B: np.ndarray, gecikme: int = 3) -> np.ndarray:
    """out[s] = s - gecikme'ye kadar (dahil) son True indeksi (yoksa -1): 'i + 2 <= s - 1' <=> i <= s - 3."""
    m = len(B); ix = np.where(B, np.arange(m), -1); acc = np.maximum.accumulate(ix) if m else ix
    out = np.full(m, -1, np.int64)
    if m > gecikme:
        out[gecikme:] = acc[:m - gecikme]
    return out


def wd_ortak(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Bir hissenin kendi geçerli barlarında ortak ölçüler; i'deki değer yalnız 0..i barlarından."""
    O, H, L, C = (np.asarray(a, float) for a in (O, H, L, C)); E = WD_ESIK["ortak"]; m = len(C)
    A: Dict[str, np.ndarray] = {"O": O, "H": H, "L": L, "C": C, "m": np.array(m)}
    A["boy"] = H - L; A["govde"] = np.abs(C - O); A["ust"] = H - np.maximum(O, C); A["alt"] = np.minimum(O, C) - L
    A["ORT"] = _wd_once(_wd_roll(A["boy"], int(E["ort_boy"]), "median"), 1)
    pc = _wd_once(C, 1)
    TR = np.where(np.isfinite(pc), np.maximum(H, pc) - np.minimum(L, pc), H - L)
    A["ATR"] = _wd_roll(TR, int(E["atr"]), "mean")
    b = int(E["baglam"]); c1 = _wd_once(C, 1); c11 = _wd_once(C, b + 1)
    with np.errstate(invalid="ignore"):
        A["DUS"] = (c1 < c11) & np.isfinite(c11); A["YUK"] = (c1 > c11) & np.isfinite(c11)
    A["PL"], A["PLyas"] = wd_uc(L, int(E["uc_pencere"]), "min"); A["PH"], A["PHyas"] = wd_uc(H, int(E["uc_pencere"]), "max")
    A["DIP"], A["TEPE"] = wd_yerel(L, H)
    A["L10"] = _wd_roll(L, int(WD_ESIK["W6"]["dip_bar"]), "min"); A["H10"] = _wd_roll(H, int(WD_ESIK["W6"]["dip_bar"]), "max")
    A["L20"] = _wd_roll(L, int(WD_ESIK["W7"]["dip_bar"]), "min"); A["H20"] = _wd_roll(H, int(WD_ESIK["W7"]["dip_bar"]), "max")
    if V is not None:
        V = np.asarray(V, float); A["V"] = V
        A["VMED"] = _wd_once(_wd_roll(V, int(WD_ESIK["W7"]["hacim_pencere"]), "median"), 1)
    return A


# ================================================================ 2) DEDEKTÖRLER (her biri ayrı; olay = dict listesi)
def _wd_olay(kol: str, ilk: int, t: int, e: int, giris: float, stop: float, seviye: float = float("nan")) -> Dict[str, Any]:
    return {"kol": kol, "yon": int(WD_KOL[kol]["yon"]), "ilk": int(ilk), "t": int(t), "e": int(e), "giris": float(giris), "stop": float(stop),
            "seviye": float(seviye)}


def _wd_sonraki_acilis(A: Dict[str, np.ndarray], kol: str, ilk: np.ndarray, t: np.ndarray, stop: np.ndarray) -> List[Dict[str, Any]]:
    """Sinyal barı t'den sonraki açılışta giriş (t + 1 yoksa giriş NaN -> GIRIS_YOK filtresi)."""
    O = A["O"]; m = len(O); out = []
    for a, tt, s in zip(ilk, t, stop):
        e = int(tt) + 1
        out.append(_wd_olay(kol, int(a), int(tt), e, float(O[e]) if e < m else float("nan"), float(s)))
    return out


def wd_w1(A: Dict[str, np.ndarray], yon: int = 1) -> List[Dict[str, Any]]:
    """W1 üç beyaz asker (yon = 1) / W1T üç kara karga (yon = -1)."""
    O, H, L, C, boy = A["O"], A["H"], A["L"], A["C"], A["boy"]; m = len(C); p = float(WD_ESIK["W1"]["tepe_pay"])
    if m < 3:
        return []
    a = np.arange(0, m - 2); b = a + 1; c = a + 2; ort = A["ORT"][a]
    with np.errstate(invalid="ignore"):
        buyuk = (boy[a] > ort) & (boy[b] > ort) & (boy[c] > ort)
        if yon == 1:
            renk = (C[a] > O[a]) & (C[b] > O[b]) & (C[c] > O[c])
            kap = (C[a] < C[b]) & (C[b] < C[c])
            uc = ((H - C) <= p * boy)
            acil = (O[b] >= O[a]) & (O[b] <= C[a]) & (O[c] >= O[b]) & (O[c] <= C[b])
            bag = A["DUS"][a]; stop = L[a]
        else:
            renk = (C[a] < O[a]) & (C[b] < O[b]) & (C[c] < O[c])
            kap = (C[a] > C[b]) & (C[b] > C[c])
            uc = ((C - L) <= p * boy)
            acil = (O[b] <= O[a]) & (O[b] >= C[a]) & (O[c] <= O[b]) & (O[c] >= C[b])
            bag = A["YUK"][a]; stop = H[a]
        ok = buyuk & renk & kap & uc[a] & uc[b] & uc[c] & acil & bag & np.isfinite(ort)
    i = np.flatnonzero(ok)
    return _wd_sonraki_acilis(A, "W1" if yon == 1 else "W1T", a[i], c[i], stop[i])


def wd_w2_maske(A: Dict[str, np.ndarray], yon: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """W2 / W2T olay maskesi (t) ve stop dizisi."""
    H, L, C, boy, ATR = A["H"], A["L"], A["C"], A["boy"], A["ATR"]; E = WD_ESIK["W2"]; yas = int(WD_ESIK["ortak"]["uc_yas"])
    with np.errstate(invalid="ignore"):
        if yon == 1:
            ok = (L < A["PL"]) & (C > A["PL"]) & (A["alt"] >= E["fitil_pay"] * boy) & (A["PLyas"] >= yas) & np.isfinite(ATR)
            stop = L - E["stop_atr"] * ATR
        else:
            ok = (H > A["PH"]) & (C < A["PH"]) & (A["ust"] >= E["fitil_pay"] * boy) & (A["PHyas"] >= yas) & np.isfinite(ATR)
            stop = H + E["stop_atr"] * ATR
    return ok, stop


def wd_w2(A: Dict[str, np.ndarray], yon: int = 1) -> List[Dict[str, Any]]:
    ok, stop = wd_w2_maske(A, yon); t = np.flatnonzero(ok)
    return _wd_sonraki_acilis(A, "W2" if yon == 1 else "W2T", t, t, stop[t])


def wd_esitlik(A: Dict[str, np.ndarray], t: int, yon: int = 1) -> bool:
    """W2E / W2TE eşitlik şartı: t-20 .. t-1 içinde (i + 2 <= t - 1) |uç_i - PL_t| <= 0,25 ATR_t yerel dip (tepe), indeks farkı >= 4 en az iki."""
    E = WD_ESIK["W2E"]; w = int(WD_ESIK["ortak"]["uc_pencere"]); atr = A["ATR"][t]
    if yon == 1:
        B, X, U = A["DIP"], A["L"], A["PL"][t]
    else:
        B, X, U = A["TEPE"], A["H"], A["PH"][t]
    ii = np.arange(max(0, t - w), t - 2)                                     # i + 2 <= t - 1
    ii = ii[B[ii] & (np.abs(X[ii] - U) <= E["atr_pay"] * atr)]
    return bool(len(ii) >= 2 and ii.max() - ii.min() >= int(E["ara_fark"]))


def wd_w2e(A: Dict[str, np.ndarray], yon: int = 1) -> List[Dict[str, Any]]:
    ok, stop = wd_w2_maske(A, yon)
    t = np.array([i for i in np.flatnonzero(ok) if wd_esitlik(A, int(i), yon)], np.int64)
    return _wd_sonraki_acilis(A, "W2E" if yon == 1 else "W2TE", t, t, stop[t]) if len(t) else []


def wd_w3(A: Dict[str, np.ndarray], yon: int = 1, say: Optional[Dict[str, int]] = None) -> List[Dict[str, Any]]:
    """W3 kaplumbağa çorbası +1 (yon = 1) / W3T. t: C <= PL (YAŞ >= 3); t + 1 PL'ye ulaşırsa giriş."""
    O, H, L, C = A["O"], A["H"], A["L"], A["C"]; m = len(C); E = WD_ESIK["W3"]; yas = int(WD_ESIK["ortak"]["uc_yas_w3"]); kol = "W3" if yon == 1 else "W3T"
    with np.errstate(invalid="ignore"):
        aday = (C <= A["PL"]) & (A["PLyas"] >= yas) if yon == 1 else (C >= A["PH"]) & (A["PHyas"] >= yas)
    out = []; s = say if say is not None else {}
    for t in np.flatnonzero(aday):
        e = int(t) + 1
        if e >= m:
            s["veri_sonu"] = s.get("veri_sonu", 0) + 1; continue
        if yon == 1:
            lv = float(A["PL"][t])
            if H[e] < lv:
                s["girissiz"] = s.get("girissiz", 0) + 1; continue
            giris = float(O[e]) if O[e] >= lv else lv; stop = min(L[t], L[e]) * E["tik"]
        else:
            lv = float(A["PH"][t])
            if L[e] > lv:
                s["girissiz"] = s.get("girissiz", 0) + 1; continue
            giris = float(O[e]) if O[e] <= lv else lv; stop = max(H[t], H[e]) * (2.0 - E["tik"])
        out.append(_wd_olay(kol, int(t), e, e, giris, float(stop), lv))
    return out


def wd_w4(A: Dict[str, np.ndarray], yon: int = -1, say: Optional[Dict[str, int]] = None) -> List[Dict[str, Any]]:
    """W4 (yon = -1: W2T sonrası son yerel dibin altına kapanış + geri test, satış) / W4Y (yon = 1: W2 sonrası, alış)."""
    O, H, L, C = A["O"], A["H"], A["L"], A["C"]; m = len(C); E = WD_ESIK["W4"]; kol = "W4" if yon == -1 else "W4Y"
    ok, _ = wd_w2_maske(A, yon)                        # W4 (yon -1) tepe süpürmesinden (W2T); W4Y (yon 1) dip süpürmesinden (W2)
    son = wd_son_uc(A["DIP"] if yon == -1 else A["TEPE"], 3)
    out = []; s_ = say if say is not None else {}
    for s in np.flatnonzero(ok):
        s = int(s); i = int(son[s])
        if i < 0:
            s_["seviye_yok"] = s_.get("seviye_yok", 0) + 1; continue
        lv = float(L[i]) if yon == -1 else float(H[i])
        bb = np.arange(s + 1, min(s + int(E["bos_bar"]), m - 1) + 1)
        kir = (C[bb] < lv) if yon == -1 else (C[bb] > lv)
        if not kir.any():
            s_["bos_yok" if s + int(E["bos_bar"]) <= m - 1 else "veri_sonu"] = s_.get("bos_yok" if s + int(E["bos_bar"]) <= m - 1 else "veri_sonu", 0) + 1
            continue
        b = int(bb[np.argmax(kir)])
        ee = np.arange(b + 1, min(b + int(E["test_bar"]), m - 1) + 1)
        dok = (H[ee] >= lv) if yon == -1 else (L[ee] <= lv)
        if not len(ee) or not dok.any():
            s_["test_yok" if b + int(E["test_bar"]) <= m - 1 else "veri_sonu"] = s_.get("test_yok" if b + int(E["test_bar"]) <= m - 1 else "veri_sonu", 0) + 1
            continue
        e = int(ee[np.argmax(dok)])
        if yon == -1:
            giris = float(O[e]) if O[e] >= lv else lv; stop = float(H[s])
        else:
            giris = float(O[e]) if O[e] <= lv else lv; stop = float(L[s])
        r = _wd_olay(kol, s, e, e, giris, stop, lv); r["bos"] = b; r["yerel"] = i
        out.append(r)
    return out


def wd_w5(A: Dict[str, np.ndarray], yon: int = -1, say: Optional[Dict[str, int]] = None) -> List[Dict[str, Any]]:
    """W5 tuzak / 2B (yon = -1: C > PH sonra 1-3 barda PH altına kapanış, satış) / W5Y (yon = 1)."""
    O, H, L, C = A["O"], A["H"], A["L"], A["C"]; m = len(C); g = int(WD_ESIK["W5"]["geri_bar"]); yas = int(WD_ESIK["ortak"]["uc_yas"])
    kol = "W5" if yon == -1 else "W5Y"
    with np.errstate(invalid="ignore"):
        aday = (C > A["PH"]) & (A["PHyas"] >= yas) if yon == -1 else (C < A["PL"]) & (A["PLyas"] >= yas)
    out = []; s_ = say if say is not None else {}
    for t in np.flatnonzero(aday):
        t = int(t); lv = float(A["PH"][t] if yon == -1 else A["PL"][t])
        uu = np.arange(t + 1, min(t + g, m - 1) + 1)
        geri = (C[uu] < lv) if yon == -1 else (C[uu] > lv)
        if not len(uu) or not geri.any():
            k = "girissiz" if t + g <= m - 1 else "veri_sonu"; s_[k] = s_.get(k, 0) + 1; continue
        u = int(uu[np.argmax(geri)]); e = u + 1
        stop = float(H[t:u + 1].max()) if yon == -1 else float(L[t:u + 1].min())
        out.append(_wd_olay(kol, t, u, e, float(O[e]) if e < m else float("nan"), stop, lv))
    return out


def wd_w6(A: Dict[str, np.ndarray], yon: int = 1) -> List[Dict[str, Any]]:
    """W6 çekiç (yon = 1) / W6T kayan yıldız (yon = -1)."""
    E = WD_ESIK["W6"]; boy = A["boy"]
    with np.errstate(invalid="ignore"):
        if yon == 1:
            ok = (A["alt"] >= E["alt_govde"] * A["govde"]) & (A["ust"] <= E["ust_pay"] * boy) & (boy >= E["boy_ort"] * A["ORT"]) & (A["L"] <= A["L10"]) & A["DUS"]
            stop = A["L"]
        else:
            ok = (A["ust"] >= E["alt_govde"] * A["govde"]) & (A["alt"] <= E["ust_pay"] * boy) & (boy >= E["boy_ort"] * A["ORT"]) & (A["H"] >= A["H10"]) & A["YUK"]
            stop = A["H"]
    t = np.flatnonzero(ok & np.isfinite(A["ORT"]))
    return _wd_sonraki_acilis(A, "W6" if yon == 1 else "W6T", t, t, stop[t])


def wd_w7(A: Dict[str, np.ndarray], kol: str = "W7") -> List[Dict[str, Any]]:
    """W7 / W7D (yukarı) / W7T (aşağı) emilim vekili. Hacim yoksa boş."""
    if "V" not in A:
        return []
    E = WD_ESIK["W7"]; boy = A["boy"]
    with np.errstate(invalid="ignore", divide="ignore"):
        clv = (A["C"] - A["L"]) / boy
        hac = (A["V"] >= E["hacim_kat"] * A["VMED"]) & np.isfinite(A["VMED"])
        if kol in ("W7", "W7D"):
            ok = A["DUS"] & (A["L"] <= A["L20"]) & hac & (clv >= E["kapanis_pay"])
            if kol == "W7D":
                ok &= (boy <= A["ORT"])
            stop = A["L"]
        else:
            ok = A["YUK"] & (A["H"] >= A["H20"]) & hac & (clv <= E["kapanis_pay"]); stop = A["H"]
    t = np.flatnonzero(ok)
    return _wd_sonraki_acilis(A, kol, t, t, stop[t])


def wd_tara(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: Optional[np.ndarray] = None,
            kollar: Optional[List[str]] = None) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    """Bir seride bütün kolların olayları (getirisiz) + girişi gerçekleşmeyen aday sayıları (W3 / W4 / W5)."""
    A = wd_ortak(O, H, L, C, V); kollar = kollar or WD_KOLLAR; R: List[Dict[str, Any]] = []; say: Dict[str, Dict[str, int]] = {}
    f = {"W1": lambda: wd_w1(A, 1), "W1T": lambda: wd_w1(A, -1), "W2": lambda: wd_w2(A, 1), "W2T": lambda: wd_w2(A, -1),
         "W2E": lambda: wd_w2e(A, 1), "W2TE": lambda: wd_w2e(A, -1),
         "W3": lambda: wd_w3(A, 1, say.setdefault("W3", {})), "W3T": lambda: wd_w3(A, -1, say.setdefault("W3T", {})),
         "W4": lambda: wd_w4(A, -1, say.setdefault("W4", {})), "W4Y": lambda: wd_w4(A, 1, say.setdefault("W4Y", {})),
         "W5": lambda: wd_w5(A, -1, say.setdefault("W5", {})), "W5Y": lambda: wd_w5(A, 1, say.setdefault("W5Y", {})),
         "W6": lambda: wd_w6(A, 1), "W6T": lambda: wd_w6(A, -1), "W7": lambda: wd_w7(A, "W7"), "W7D": lambda: wd_w7(A, "W7D"), "W7T": lambda: wd_w7(A, "W7T")}
    for k in kollar:
        R.extend(f[k]())
    D = pd.DataFrame(R, columns=["kol", "yon", "ilk", "t", "e", "giris", "stop", "seviye", "bos", "yerel"])
    D["atr"] = A["ATR"][np.clip(D.e.to_numpy(np.int64) - 1, 0, max(len(C) - 1, 0))] if len(D) else np.zeros(0)
    return D, say


def wd_tekil(D: pd.DataFrame, bar: Optional[int] = None, anahtar: Tuple[str, ...] = ("kol",)) -> Tuple[pd.DataFrame, int]:
    """Aynı (anahtar) içinde giriş barı sırasıyla; son tutulan girişten < bar sonraki olay atılır."""
    bar = int(bar if bar is not None else WD_ESIK["filtre"]["tekil_bar"])
    if not len(D):
        return D.copy(), 0
    D = D.sort_values(list(anahtar) + ["e"], kind="stable"); tut = np.ones(len(D), bool); son: Dict[Any, int] = {}
    for i, (k, e) in enumerate(zip(D[list(anahtar)].itertuples(index=False, name=None), D.e.astype(int))):
        if k in son and e - son[k] < bar:
            tut[i] = False; continue
        son[k] = e
    return D[tut].reset_index(drop=True), int((~tut).sum())


# ================================================================ 3) SONUÇ ÇEKİRDEĞİ (yalnız ölçüm kapısından sonra / sentetik testte)
def wd_ilk_dokunma(Hs: np.ndarray, Ls: np.ndarray, hedef: np.ndarray, stop: np.ndarray, yon: np.ndarray) -> np.ndarray:
    """'Önce hangisine dokundu' (vektör; satır başına seviye). yon 1: hedef = H >= hedef, stop = L <= stop; yon -1 ayna. Aynı bar = STOP ÖNCE -> 0."""
    hedef = np.asarray(hedef, float)[:, None]; stop = np.asarray(stop, float)[:, None]; y = np.asarray(yon)[:, None]
    with np.errstate(invalid="ignore"):
        hit = np.where(y == 1, Hs >= hedef, Ls <= hedef); stp = np.where(y == 1, Ls <= stop, Hs >= stop)
    BIG = 10 ** 9
    kh = np.where(hit.any(1), hit.argmax(1), BIG); ks = np.where(stp.any(1), stp.argmax(1), BIG)
    return ((kh < BIG) & (kh < ks)).astype(float)


def wd_r_kati(Os: np.ndarray, Hs: np.ndarray, Ls: np.ndarray, Cs: np.ndarray, giris: np.ndarray, stop: np.ndarray, yon: np.ndarray) -> np.ndarray:
    """R katı: stopa ilk dokunulan barda çıkış (giriş barından sonraki barda açılış stopun ötesindeyse açılışta), yoksa son barın kapanışı."""
    giris = np.asarray(giris, float); stop = np.asarray(stop, float); y = np.asarray(yon, float); R = np.abs(giris - stop)
    with np.errstate(invalid="ignore"):
        stp = np.where(y[:, None] == 1, Ls <= stop[:, None], Hs >= stop[:, None])
    N, U = Cs.shape; ks = np.where(stp.any(1), stp.argmax(1), -1); cik = Cs[:, -1].copy()
    v = ks >= 0
    if v.any():
        r = np.flatnonzero(v); k = ks[v]; o = Os[r, k]
        gap = (k > 0) & np.where(y[r] == 1, o <= stop[r], o >= stop[r])
        cik[r] = np.where(gap, o, stop[r])
    with np.errstate(invalid="ignore", divide="ignore"):
        return y * (cik - giris) / R


def wd_sonuc_olay(dep: Dict[str, np.ndarray], j: np.ndarray, e: np.ndarray, giris: np.ndarray, stop: np.ndarray, yon: np.ndarray,
                  atr: np.ndarray) -> Dict[str, np.ndarray]:
    """Olay sonuçları (getiri): R15, ATR_H, R2_H, RKAT, Y10 (10 gün yön) — e'den itibaren 15 bar."""
    U = int(WD_ESIK["olcu"]["ufuk"]); Eo = WD_ESIK["olcu"]; j = np.asarray(j, np.int64); e = np.asarray(e, np.int64)
    giris = np.asarray(giris, float); stop = np.asarray(stop, float); yon = np.asarray(yon, np.int64); atr = np.asarray(atr, float); N = len(j)
    out = {a: np.full(N, np.nan) for a in ("R15", "ATR_H", "R2_H", "RKAT", "Y10")}
    if not N:
        return out
    g = dep["off"][j] + e
    if (g + U - 1 > dep["off"][j + 1] - 1).any():
        raise WDHata("K10: sonuç penceresi hissenin verisini aşıyor (UFUK_KESIK filtresi bozuk)")
    W = g[:, None] + np.arange(U)[None, :]
    Os, Hs, Ls, Cs = dep["O"][W], dep["H"][W], dep["L"][W], dep["C"][W]
    out["R15"] = Cs[:, -1] / giris - 1
    out["ATR_H"] = wd_ilk_dokunma(Hs, Ls, giris + yon * Eo["atr_hedef"] * atr, giris - yon * Eo["atr_stop"] * atr, yon)
    R = np.abs(giris - stop)
    out["R2_H"] = wd_ilk_dokunma(Hs, Ls, giris + yon * Eo["R_hedef"] * R, stop, yon)
    out["RKAT"] = wd_r_kati(Os, Hs, Ls, Cs, giris, stop, yon)
    out["Y10"] = ((yon * (Cs[:, int(Eo["yon_bar"]) - 1] - giris)) > 0).astype(float)
    return out


def wd_atr_dizi(dep: Dict[str, np.ndarray]) -> np.ndarray:
    """Bütün hisseler için ATR(20) (hissenin kendi barlarında; wd_ortak ile aynı formül)."""
    out = np.full(len(dep["C"]), np.nan); off = dep["off"]
    for j in range(len(off) - 1):
        a, b = int(off[j]), int(off[j + 1])
        if b - a < 2:
            continue
        H, L, C = dep["H"][a:b], dep["L"][a:b], dep["C"][a:b]; pc = _wd_once(C, 1)
        TR = np.where(np.isfinite(pc), np.maximum(H, pc) - np.minimum(L, pc), H - L)
        out[a:b] = _wd_roll(TR, int(WD_ESIK["ortak"]["atr"]), "mean")
    return out


def wd_taban_gun(dep: Dict[str, np.ndarray], ATR: np.ndarray, j: np.ndarray, k: np.ndarray) -> Dict[str, np.ndarray]:
    """YO örnek günleri (hisse j, bar k): giriş O[k+1], barlar k+1 .. k+15. R15 (T1), ATR hedefi yukarı / aşağı, 10 gün yön, normalize H / L (2R tabanı)."""
    U = int(WD_ESIK["olcu"]["ufuk"]); Eo = WD_ESIK["olcu"]; j = np.asarray(j, np.int64); k = np.asarray(k, np.int64); N = len(j)
    g = dep["off"][j] + k
    if N and (g + U > dep["off"][j + 1] - 1).any():
        raise WDHata("K10: taban penceresi hissenin verisini aşıyor")
    W = g[:, None] + 1 + np.arange(U)[None, :]
    E0 = dep["O"][g + 1]; Hs, Ls = dep["H"][W], dep["L"][W]; a = ATR[g]
    one = np.ones(N, np.int64)
    return {"R15": dep["C"][g + U] / E0 - 1,
            "ATR_U": wd_ilk_dokunma(Hs, Ls, E0 + Eo["atr_hedef"] * a, E0 - Eo["atr_stop"] * a, one),
            "ATR_D": wd_ilk_dokunma(Hs, Ls, E0 - Eo["atr_hedef"] * a, E0 + Eo["atr_stop"] * a, -one),
            "Y10_U": (dep["C"][g + int(Eo["yon_bar"])] > E0).astype(float), "Y10_D": (dep["C"][g + int(Eo["yon_bar"])] < E0).astype(float),
            "Hn": Hs / E0[:, None], "Ln": Ls / E0[:, None], "atr_ok": np.isfinite(a)}


def wd_taban_2R(Hn: np.ndarray, Ln: np.ndarray, r: np.ndarray, yon: np.ndarray) -> np.ndarray:
    """Her olay için (oran r = R / giriş, yön) örnek günlerinde +2R'ye stoptan önce ulaşma payı (aynı bar = stop önce)."""
    r = np.asarray(r, float); yon = np.asarray(yon); out = np.full(len(r), np.nan)
    if not len(r) or not len(Hn):
        return out
    BIG = 10 ** 9
    for y in (1, -1):
        q = np.flatnonzero(yon == y)
        if not len(q):
            continue
        rr = r[q][:, None, None]
        with np.errstate(invalid="ignore"):
            if y == 1:
                hit = Hn[None] >= 1 + 2 * rr; stp = Ln[None] <= 1 - rr
            else:
                hit = Ln[None] <= 1 - 2 * rr; stp = Hn[None] >= 1 + rr
        kh = np.where(hit.any(2), hit.argmax(2), BIG); ks = np.where(stp.any(2), stp.argmax(2), BIG)
        out[q] = ((kh < BIG) & (kh < ks)).mean(1)
    return out


# ================================================================ 4) GERÇEK VERİ: OLAYLAR (GETİRİSİZ)
def wd_panel_yukle(pazar: str, yo_ham: Optional[str] = None) -> Dict[str, np.ndarray]:
    z = np.load(os.path.join(yo_ham or WD_YOL["yo_ham"], f"ham_{pazar}.npz"))
    P = {k: z[k] for k in z.files}
    wd_tarih_kapi(P["tarih"], f"YO paneli {pazar}")
    return P


def wd_olay_pazar(pazar: str, P: Dict[str, np.ndarray], Vd: Dict[str, Any], Xs: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazar: bütün hisselerde tarama -> filtreler (sıra WD_ESIK['filtre']['sira']) -> tekil. Getiri hesaplanmaz.
    P = YO ham paneli (O/H/L/C/POS/off/P2/tarih/sembol); Vd = MI.mi_veri (hacim + geçersiz tarihler); Xs = YO örnek günleri (j, k, hucre)."""
    import MUM_IZI_UC as UC
    t0 = time.time(); F = WD_ESIK["filtre"]; U = int(WD_ESIK["olcu"]["ufuk"])
    wd_kesik_kapi(Vd["V"], f"günlük {pazar}")
    idx = pd.DatetimeIndex(P["tarih"]); S = [str(s) for s in P["sembol"]]; off = P["off"]; POS = P["POS"]; P2 = P["P2"]
    if sorted(Vd["V"]) != S:
        raise WDHata(f"K10: {pazar} sembol listesi YO paneliyle farklı")
    t1n = Xs.groupby(["j", "hucre"]).size().to_dict()
    atma = {k: {a: 0 for a in F["sira"]} for k in WD_KOLLAR}; aday = {k: 0 for k in WD_KOLLAR}; girissiz = {k: {} for k in WD_KOLLAR}
    bar_say = 0; parca = []
    for j, s in enumerate(S):
        a, b = int(off[j]), int(off[j + 1]); m = b - a
        if m < 3:
            continue
        d = Vd["V"][s]; Vv = d.Volume.to_numpy(float)
        if len(d) != m or not np.allclose(d.Close.to_numpy(float), P["C"][a:b], rtol=0, atol=0):
            raise WDHata(f"K10: {s} hacim verisi YO paneliyle bar bar eşleşmiyor")
        O, H, L, C = P["O"][a:b], P["H"][a:b], P["L"][a:b], P["C"][a:b]; pos = POS[a:b]; bar_say += m
        D, say = wd_tara(O, H, L, C, Vv)
        for k, v in say.items():
            for kk, vv in v.items():
                girissiz[k][kk] = girissiz[k].get(kk, 0) + int(vv)
        if not len(D):
            continue
        for k, c in D.kol.value_counts().items():
            aday[k] += int(c)
        D["j"] = j; D["sembol"] = s; e = D.e.to_numpy(np.int64); t = D.t.to_numpy(np.int64); ilk = D.ilk.to_numpy(np.int64)
        neden = np.full(len(D), "", object)

        def isaretle(maske, ad):
            neden[(neden == "") & maske] = ad
        gir = D.giris.to_numpy(float); st = D.stop.to_numpy(float); yn = D.yon.to_numpy(np.int64)
        isaretle((e >= m) | ~np.isfinite(gir), "GIRIS_YOK")
        with np.errstate(invalid="ignore"):
            isaretle(~((yn * (gir - st)) > 0), "STOP_TERS")
        ec = np.minimum(e, m - 1)
        isaretle(pos[ec] - pos[t] > int(F["giris_bosluk"]), "BOSLUK")
        e14 = e + U - 1; v14 = e14 <= m - 1; e14c = np.minimum(e14, m - 1)
        isaretle(~v14 | (idx[pos[e14c]] > WD_KESIK) | (pos[e14c] - pos[ec] > int(F["pencere_satir"]) - 1), "UFUK_KESIK")
        gt = idx[pos[ec]]
        isaretle((gt < pd.Timestamp("2016-01-01")) | (gt > pd.Timestamp("2022-12-31")), "DONEM_DISI")
        isaretle(~P2[pos[ec], j], "EVREN_DISI")
        kp = UC.uc_kilitli_pay(Vd["gecersiz"].get(s, pd.DatetimeIndex([])), d.index, idx[pos[ilk]], idx[pos[ec]])
        isaretle(kp > float(F["kilitli_pay"]), "KILITLI")
        hc = np.array([HV.hv_hucre_ad(g, pazar) for g in gt], object)
        isaretle(np.array([t1n.get((j, h), 0) < int(F["t1_en_az"]) for h in hc]), "T1_YOK")
        D["neden"] = neden; D["hucre"] = hc; D["giris_tarih"] = gt; D["sinyal_tarih"] = idx[pos[t]]; D["ilk_tarih"] = idx[pos[ilk]]
        D["e_row"] = pos[ec]; D["kilitli_pay"] = kp
        parca.append(D)
    X = pd.concat(parca, ignore_index=True) if parca else pd.DataFrame()
    for (k, nd), c in X.groupby(["kol", "neden"]).size().items():
        if nd:
            atma[k][nd] += int(c)
    T = X[X.neden == ""].drop(columns=["neden"])
    T, _ = wd_tekil(T, None, ("kol", "j"))
    for k in WD_KOLLAR:
        n0 = int(((X.kol == k) & (X.neden == "")).sum()); atma[k]["TEKIL"] = n0 - int((T.kol == k).sum())
    T["pazar"] = pazar; T["ay"] = pd.DatetimeIndex(T.giris_tarih).strftime("%Y-%m")
    T = T.sort_values(["kol", "giris_tarih", "sembol"], kind="stable").reset_index(drop=True)
    info = {"pazar": pazar, "hisse": len(S), "bar": int(bar_say), "aday": aday, "atma": atma, "girissiz": girissiz,
            "sure_sn": round(time.time() - t0, 1)}
    wdlog.info("%s: %d olay (filtre + tekil sonrası), %d bar (%.0f sn)", pazar, len(T), bar_say, time.time() - t0)
    return T, info


def wd_sayim(TS: Dict[str, pd.DataFrame], INFO: Dict[str, Dict[str, Any]], sent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """GETİRİSİZ SAYIM: kol x hücre olay / farklı ay / en kalabalık 3 ay payı; filtre atmaları; girişsiz adaylar; 1000 barda ham sıklık."""
    S: Dict[str, Any] = {"hucre": {}, "atma": {}, "girissiz": {}, "aday": {}, "siklik_1000": {}, "bar": {}}
    for p, T in TS.items():
        I = INFO[p]; S["bar"][p] = I["bar"]
        for k in WD_KOLLAR:
            S["atma"][f"{p}|{k}"] = I["atma"][k]; S["girissiz"][f"{p}|{k}"] = I["girissiz"][k]; S["aday"][f"{p}|{k}"] = I["aday"][k]
            S["siklik_1000"][f"{p}|{k}"] = round(1000.0 * I["aday"][k] / max(I["bar"], 1), 4)
            for h in [x for x in WD_HUCRE if x.startswith(p)]:
                g = T[(T.kol == k) & (T.hucre == h)]
                ao = HV.hv25_ay_ozet(pd.DatetimeIndex(g.giris_tarih).strftime("%Y-%m-%d").tolist())
                S["hucre"][f"{k}|{h}"] = {"n": ao["n"], "ay": ao["ay"], "ust3_pay": ao["ust3_pay"], "hisse": int(g.sembol.nunique())}
    return S


# ================================================================ 5) İSTATİSTİK
def wd_ay_W(ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    B = int(B or WD_ESIK["boot"]["B"]); u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = _wd_rng(anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return k, W


def _wd_q(v: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    v = v[np.isfinite(v)]
    return (float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))) if len(v) else (None, None)


def wd_boot_ort(x: np.ndarray, k: np.ndarray, W: np.ndarray, sifir: float = 0.0) -> Dict[str, Any]:
    x = np.asarray(x, float); f = np.isfinite(x)
    if f.sum() < 2:
        return {"ort": None, "alt": None, "ust": None, "p": None, "medyan": None}
    K = W.shape[1]; s = np.bincount(k[f], weights=x[f], minlength=K); n = np.bincount(k[f], minlength=K).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W @ s) / (W @ n)
    a, b = _wd_q(d); dd = d[np.isfinite(d)]
    return {"ort": float(x[f].mean()), "alt": a, "ust": b, "medyan": float(np.median(x[f])),
            "p": float((1 + (dd <= sifir).sum()) / (len(dd) + 1)) if len(dd) else None}


def wd_boot_kat(hit: np.ndarray, taban: np.ndarray, k: np.ndarray, W: np.ndarray) -> Dict[str, Any]:
    hit = np.asarray(hit, float); taban = np.asarray(taban, float); f = np.isfinite(hit) & np.isfinite(taban)
    if f.sum() < 2 or taban[f].sum() <= 0:
        return {"pay": None, "taban": None, "kat": None, "alt": None, "ust": None, "p": None}
    K = W.shape[1]; sh = np.bincount(k[f], weights=hit[f], minlength=K); sb = np.bincount(k[f], weights=taban[f], minlength=K)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W @ sh) / (W @ sb)
    a, b = _wd_q(d); dd = d[np.isfinite(d)]
    return {"pay": float(hit[f].mean()), "taban": float(taban[f].mean()), "kat": float(hit[f].sum() / taban[f].sum()), "alt": a, "ust": b,
            "p": float((1 + (dd <= 1.0).sum()) / (len(dd) + 1)) if len(dd) else None}


def wd_hucre_olc(g: pd.DataFrame, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Bir kol x hücre: n, ay, üst3 payı, TOPLAM FARK, SEÇİM, ATR KAT, +2R payı / taban, R katı, 10 gün yön."""
    ao = HV.hv25_ay_ozet(pd.DatetimeIndex(g.giris_tarih).strftime("%Y-%m-%d").tolist())
    o: Dict[str, Any] = {"n": ao["n"], "ay": ao["ay"], "ust3_pay": ao["ust3_pay"]}
    if len(g) < 2:
        return o
    k, W = wd_ay_W(g.ay.to_numpy(), anahtar, B)
    o["TF"] = wd_boot_ort(g.TF.to_numpy(float), k, W); o["SECIM"] = wd_boot_ort(g.SECIM.to_numpy(float), k, W)
    o["ATR"] = wd_boot_kat(g.ATR_H.to_numpy(float), g.ATR_TABAN.to_numpy(float), k, W)
    o["R2"] = wd_boot_kat(g.R2_H.to_numpy(float), g.R2_TABAN.to_numpy(float), k, W)
    o["RKAT"] = wd_boot_ort(g.RKAT.to_numpy(float), k, W)
    o["Y10"] = {"pay": float(np.nanmean(g.Y10)), "taban": float(np.nanmean(g.Y10_TABAN))}
    o["R15_medyan_yonlu"] = float(np.nanmedian(g.yon * g.R15))
    return o


def wd_hukum(o: Dict[str, Dict[str, Any]], bh_gecti: bool) -> Tuple[str, List[str]]:
    Hk = WD_ESIK["hukum"]; notlar: List[str] = []
    A = [o.get(f"ABD|{d}", {}) for d in ("d1619", "d2022")]
    if any(a.get("n", 0) < Hk["n_min"] or a.get("ay", 0) < Hk["ay_min"] for a in A):
        return "ÖLÇÜLEMEDİ", notlar

    def gec(a):
        tf, at = a.get("TF", {}), a.get("ATR", {})
        return bool(tf.get("ort") is not None and tf["ort"] > 0 and (tf.get("alt") or -1) > 0 and at.get("kat") is not None and at["kat"] > 1
                    and (at.get("alt") or 0) > 1)
    g = [gec(a) for a in A]
    avr_ok = True
    for d in ("d1619", "d2022"):
        a = o.get(f"AVR|{d}", {})
        if a.get("n", 0) < Hk["avr_n"]:
            notlar.append(f"AVR {d} n < {Hk['avr_n']} (şart aranmadı)"); continue
        if not (a.get("TF", {}).get("ort") is not None and a["TF"]["ort"] > 0):
            avr_ok = False
    if all(g) and avr_ok and bh_gecti:
        return "TUTAR", notlar
    if all((a.get("TF", {}).get("ust") is not None and a["TF"]["ust"] < 0) for a in A):
        return "TERS", notlar
    if sum(g) == 1:
        return "TEK DÖNEM", notlar
    if all(g):
        notlar.append("ABD iki dönemde geçti; " + ("AVR işareti tutmadı" if not avr_ok else "BH geçmedi"))
    return "TUTMADI", notlar


# ================================================================ 6) SENTETİK (yapay pozitif / negatif)
class _WDSeri:
    """Yapay seri kurucu (desen şeması mum mum). İşaretler grafikte Türkçe etiket olur."""

    def __init__(self, P0: float, rng: np.random.Generator, oyn: float):
        self.O: List[float] = []; self.H: List[float] = []; self.L: List[float] = []; self.C: List[float] = []; self.V: List[float] = []
        self.r = rng; self.oyn = oyn; self.c = float(P0); self.isaret: List[Dict[str, Any]] = []

    @property
    def n(self) -> int:
        return len(self.C)

    def bar(self, o: float, h: float, l_: float, c: float, v: Optional[float] = None) -> int:
        h = max(h, o, c); l_ = min(l_, o, c)
        if not h > l_:
            h = l_ * (1 + 1e-4) + 1e-9
        self.O.append(o); self.H.append(h); self.L.append(l_); self.C.append(c)
        self.V.append(float(v) if v is not None else float(self.r.lognormal(np.log(1e5), 0.25))); self.c = c
        return self.n - 1

    def yuru(self, n: int, egim: float) -> None:
        for _ in range(n):
            o = self.c * (1 + self.r.normal(0, self.oyn / 3)); c = self.c * (1 + egim + self.r.normal(0, self.oyn))
            h = max(o, c) * (1 + abs(self.r.normal(0, self.oyn / 2))); l_ = min(o, c) * (1 - abs(self.r.normal(0, self.oyn / 2)))
            self.bar(o, h, l_, c)

    def yatay(self, n: int, taban: float, u: float, alt_sinir: Optional[float] = None, ust_sinir: Optional[float] = None) -> None:
        """taban çevresinde küçük mumlar; L >= alt_sinir / H <= ust_sinir."""
        for _ in range(n):
            o = taban + self.r.normal(0, 0.25 * u); c = taban + self.r.normal(0, 0.25 * u)
            h = max(o, c) + abs(self.r.normal(0.25 * u, 0.08 * u)); l_ = min(o, c) - abs(self.r.normal(0.25 * u, 0.08 * u))
            if alt_sinir is not None:
                l_ = max(l_, alt_sinir); o = max(o, l_ + 0.02 * u); c = max(c, l_ + 0.02 * u)
            if ust_sinir is not None:
                h = min(h, ust_sinir); o = min(o, h - 0.02 * u); c = min(c, h - 0.02 * u)
            self.bar(o, h, l_, c)

    def trend(self, n: int, egim: float) -> None:
        """Belirli (gürültüsü küçük) eğilim barları: bağlam deterministik olsun."""
        for _ in range(n):
            o = self.c * (1 + self.r.normal(0, self.oyn / 8)); c = self.c * (1 + egim + self.r.normal(0, self.oyn / 6))
            h = max(o, c) * (1 + abs(self.r.normal(0, self.oyn / 3))); l_ = min(o, c) * (1 - abs(self.r.normal(0, self.oyn / 3)))
            self.bar(o, h, l_, c)

    def u(self) -> float:
        b = np.asarray(self.H[-10:]) - np.asarray(self.L[-10:])
        return float(np.median(b))

    def isa(self, **k) -> None:
        self.isaret.append(k)

    def dizi(self) -> Dict[str, np.ndarray]:
        return {a: np.asarray(getattr(self, a), float) for a in ("O", "H", "L", "C", "V")}


def _wd_dip_kur(s: _WDSeri, u: float, c_ust: float = 1.0) -> Tuple[int, float]:
    """Belirgin 20 barlık dip barı: L = önceki 20 barın en düşüğü - 1u, kapanış dip + c_ust u."""
    PL = min(s.L[-20:]) - 1.0 * u; o = s.c
    p = s.bar(o, max(o, PL + c_ust * u) + 0.2 * u, PL, PL + c_ust * u)
    return p, PL


# Her yapıcı: (s, tip) -> {'ilk', 'son', 'e'} ; 'son' = son desen barı (gürültü bölgesi ilk .. son); e = beklenen giriş barı
def _yb_w1(s: _WDSeri, tip: str) -> Dict[str, int]:
    eg = 0.003 if tip == "yukselis" else -0.003
    s.yuru(45, eg); s.trend(12, 1.6 * eg)
    u = s.u(); c0 = s.c; bos = tip == "bosluk"; fit = 1.5 * u if tip == "fitil" else 0.2 * u
    s.isa(tur="kutu", x0=s.n - 11, x1=s.n - 1, yazi="yükseliş bağlamı" if tip == "yukselis" else "düşüş bağlamı")
    a = s.bar(c0, c0 + 2 * u + fit, c0 - 0.2 * u, c0 + 2 * u)
    ob = c0 + 2.5 * u if bos else c0 + 1.0 * u; cb = ob + 2.0 * u if bos else c0 + 4 * u
    b = s.bar(ob, cb + fit, ob - 0.2 * u, cb)
    oc = cb + 0.5 * u if bos else c0 + 3.0 * u; cc = oc + 2.0 * u if bos else c0 + 6 * u
    t = s.bar(oc, cc + fit, oc - 0.2 * u, cc)
    for i, x in enumerate((a, b, t)):
        s.isa(tur="ok", x=x, y=s.H[x], yazi=str(i + 1), yukari=True)
    s.isa(tur="cizgi", y=s.L[a], x0=a, x1=t + 6, yazi="stop (1. mumun dibi)", renk="#c00000")
    if tip == "bosluk":
        s.isa(tur="ok", x=b, y=s.L[b], yazi="açılış gövdenin DIŞINDA (boşluk)", yukari=False)
    if tip == "fitil":
        s.isa(tur="ok", x=t, y=s.H[t], yazi="uzun üst fitil", yukari=True, dy=2)
    s.yuru(8, 0.002)
    s.isa(tur="giris", x=t + 1, y=s.O[t + 1], yazi="giriş: sonraki açılış")
    return {"ilk": a, "son": t, "e": t + 1}


def _yb_w2(s: _WDSeri, tip: str, esit: bool = False) -> Dict[str, int]:
    s.yuru(40, -0.002); u = s.u()
    p1, PL = _wd_dip_kur(s, u)
    s.isa(tur="ok", x=p1, y=PL, yazi="20 günlük dip", yukari=False, dy=4 if esit else 1)
    if esit:
        s.yatay(4, PL + 4 * u, u, alt_sinir=PL + 3 * u)
        if tip == "tek_dip":
            s.yatay(1, PL + 4 * u, u, alt_sinir=PL + 3 * u)
        else:
            l2 = PL + (1.5 * u if tip == "esit_degil" else 0.05 * u)
            p2 = s.bar(PL + 3.5 * u, PL + 3.7 * u, l2, l2 + 1.6 * u)
            s.isa(tur="ok", x=p2, y=l2, yazi="ikinci dip (eşit değil)" if tip == "esit_degil" else "eşit dip", yukari=False)
        s.yatay(5, PL + 4 * u, u, alt_sinir=PL + 3 * u)
        s.isa(tur="cizgi", y=PL, x0=p1, x1=s.n + 3, yazi="eşit dipler (likidite)", renk="#555555", stil="--")
    else:
        s.yatay(8, PL + 2 * u, u, alt_sinir=PL + 0.6 * u)
        s.isa(tur="cizgi", y=PL, x0=p1, x1=s.n + 3, yazi="önceki dip (PL)", renk="#555555", stil="--")
    o = s.c
    if tip == "kapanis_disari":
        t = s.bar(o, o + 0.1 * u, PL - 0.7 * u, PL - 0.4 * u)
        s.isa(tur="ok", x=t, y=s.C[t], yazi="dibin ALTINDA kapanış (gerçek kırılım)", yukari=False, dy=2)
    elif tip == "kisa_fitil":
        t = s.bar(PL - 0.4 * u, PL + 1.7 * u, PL - 0.5 * u, PL + 1.6 * u)
        s.isa(tur="ok", x=t, y=s.L[t], yazi="alt fitil kısa (açılış dipte)", yukari=False, dy=2)
    else:
        t = s.bar(o, max(o, o + 0.3 * u) + 0.2 * u, PL - 0.5 * u, o + 0.3 * u)
        s.isa(tur="ok", x=t, y=s.L[t], yazi="süpürme fitili", yukari=False, dy=2)
        s.isa(tur="ok", x=t, y=s.H[t], yazi="aralığa geri kapanış", yukari=True)
    s.isa(tur="cizgi", y=s.L[t] - 0.1 * u * 1.2, x0=t, x1=t + 6, yazi="stop (fitil dibi - 0,1 ATR)", renk="#c00000")
    s.yuru(8, 0.002)
    s.isa(tur="giris", x=t + 1, y=s.O[t + 1], yazi="giriş: sonraki açılış")
    return {"ilk": t, "son": t, "e": t + 1}


def _yb_w2e(s: _WDSeri, tip: str) -> Dict[str, int]:
    return _yb_w2(s, tip, esit=True)


def _yb_w3(s: _WDSeri, tip: str) -> Dict[str, int]:
    s.yuru(40, -0.002); u = s.u()
    p, PL = _wd_dip_kur(s, u)
    s.yatay(6, PL + 2 * u, u, alt_sinir=PL + 0.8 * u)
    s.isa(tur="cizgi", y=PL, x0=p, x1=s.n + 4, yazi="20 günlük dip (PL)", renk="#555555", stil="--")
    o = s.c
    if tip == "fitil_kapanis":
        t = s.bar(o, o + 0.1 * u, PL - 0.8 * u, PL + 0.3 * u)
        s.isa(tur="ok", x=t, y=s.C[t], yazi="dibin ÜSTÜNDE kapanış (yalnız fitil)", yukari=True, dy=2)
    else:
        t = s.bar(o, o + 0.1 * u, PL - 0.8 * u, PL - 0.5 * u)
        s.isa(tur="ok", x=t, y=s.L[t], yazi="dibin altında kapanış", yukari=False)
    if tip == "ulasmadi":
        e = s.bar(PL - 0.4 * u, PL - 0.1 * u, PL - 0.9 * u, PL - 0.2 * u)
        s.isa(tur="ok", x=e, y=s.H[e], yazi="ertesi gün dibe ULAŞAMADI", yukari=True, dy=2)
    else:
        e = s.bar(PL - 0.3 * u, PL + 1.0 * u, PL - 0.5 * u, PL + 0.7 * u)
        s.isa(tur="giris", x=e, y=PL, yazi="ertesi gün dibe dönüş = giriş (PL'de)")
    s.isa(tur="cizgi", y=min(s.L[t], s.L[e]) * 0.999, x0=t, x1=e + 6, yazi="stop (iki günün dibi - 1 tik)", renk="#c00000")
    s.yuru(8, 0.002)
    return {"ilk": t, "son": e, "e": e}


def _yb_w4y(s: _WDSeri, tip: str) -> Dict[str, int]:
    """Cemal'in şemasının aynası (yukarı): eşit dipler, süpürme fitili, yapı kırılımı, geri test, giriş, stop, hedef."""
    s.yuru(35, -0.002); u = s.u(); PL = min(s.L[-20:]) - 1.0 * u; o = s.c

    def B(oo, hh, ll, cc):
        return s.bar(PL + oo * u, PL + hh * u, PL + ll * u, PL + cc * u)
    p1 = s.bar(o, max(o, PL + 1.0 * u) + 0.2 * u, PL, PL + 1.0 * u)
    B(1.0, 2.8, 0.8, 2.5); B(2.5, 3.8, 2.2, 3.5); B(3.5, 4.2, 2.8, 3.0); B(3.0, 3.2, 1.8, 2.0); B(2.0, 2.2, 0.8, 1.0)
    p2 = B(1.0, 1.5, 0.05, 1.2)
    B(1.2, 2.6, 1.0, 2.4); B(2.4, 3.5, 2.2, 3.2); h2 = B(3.2, 3.6, 2.6, 2.8); B(2.8, 3.0, 1.8, 2.0); B(2.0, 2.2, 1.2, 1.4)
    if tip == "gercek_kirilim":
        sw = B(1.4, 1.5, -2.0, -0.6)
    else:
        sw = B(1.4, 1.5, -2.0, 1.2)
    lv = PL + 3.6 * u
    if tip == "bos_yok":
        B(1.2, 2.4, 1.0, 2.2); B(2.2, 3.4, 2.0, 3.0); B(3.0, 3.55, 2.8, 3.3); B(3.3, 3.5, 2.7, 2.9); B(2.9, 3.5, 2.6, 3.4)
        e = B(3.4, 3.58, 3.0, 3.2); B(3.2, 3.5, 2.9, 3.1); B(3.1, 3.5, 2.9, 3.3); B(3.3, 3.55, 3.0, 3.2); B(3.2, 3.5, 3.0, 3.3); B(3.3, 3.55, 3.0, 3.4)
        b = None
    else:
        B(1.2, 2.4, 1.0, 2.2); B(2.2, 3.3, 2.0, 3.1); b = B(3.1, 4.5, 2.9, 4.3); B(4.3, 5.0, 4.1, 4.8)
        e = B(4.8, 4.9, 3.5, 4.2)
    stop = PL - 2.0 * u; R = (lv - stop)
    for k in range(16):
        B(4.2 + 0.85 * k, 5.2 + 0.85 * k, 3.9 + 0.85 * k, 5.0 + 0.85 * k)
    s.isa(tur="cizgi", y=PL, x0=p1 - 1, x1=sw + 1, yazi="eşit dipler (likidite)", renk="#555555", stil="--")
    s.isa(tur="ok", x=sw, y=s.L[sw], yazi="süpürme fitili" if tip != "gercek_kirilim" else "dibin ALTINDA kapanış (süpürme değil)", yukari=False)
    s.isa(tur="cizgi", y=lv, x0=h2, x1=e + 3, yazi="kırılan seviye (son yerel tepe)", renk="#1f4fbf", stil="-")
    if b is not None and tip != "gercek_kirilim":
        s.isa(tur="ok", x=b, y=s.H[b], yazi="yapı kırılımı (BOS)", yukari=True, dy=3)
        s.isa(tur="giris", x=e, y=lv, yazi="giriş (geri test)")
    elif b is not None:
        s.isa(tur="ok", x=b, y=s.H[b], yazi="kırılım var ama önce süpürme yok", yukari=True, dy=3)
    else:
        s.isa(tur="ok", x=e, y=s.H[e], yazi="kapanış seviyeyi GEÇMEDİ (BOS yok)", yukari=True, dy=2)
    s.isa(tur="cizgi", y=stop, x0=sw, x1=s.n, yazi="stop (süpürme dibi)", renk="#c00000", stil="--")
    s.isa(tur="cizgi", y=lv + 2 * R, x0=sw, x1=s.n, yazi="hedef (+2R)", renk="#1a9850", stil="--")
    return {"ilk": p1, "son": e, "e": e}


def _yb_w5y(s: _WDSeri, tip: str) -> Dict[str, int]:
    s.yuru(40, -0.002); u = s.u()
    p, PL = _wd_dip_kur(s, u)
    s.yatay(6, PL + 2 * u, u, alt_sinir=PL + 0.8 * u)
    s.isa(tur="cizgi", y=PL, x0=p, x1=s.n + 5, yazi="20 günlük dip (PL)", renk="#555555", stil="--")
    o = s.c
    if tip == "sadece_fitil":
        t = s.bar(o, o + 0.1 * u, PL - 0.8 * u, PL + 0.3 * u)
        s.isa(tur="ok", x=t, y=s.L[t], yazi="yalnız fitil (altında kapanış yok)", yukari=False)
    else:
        t = s.bar(o, o + 0.1 * u, PL - 0.8 * u, PL - 0.5 * u)
        s.isa(tur="ok", x=t, y=s.L[t], yazi="dibin altında kapanış (kırılım gibi)", yukari=False)
    if tip == "gercek_kirilim":
        s.bar(PL - 0.5 * u, PL - 0.3 * u, PL - 1.1 * u, PL - 0.8 * u); s.bar(PL - 0.8 * u, PL - 0.6 * u, PL - 1.5 * u, PL - 1.2 * u)
        uu = s.bar(PL - 1.2 * u, PL - 1.0 * u, PL - 1.8 * u, PL - 1.5 * u)
        s.isa(tur="ok", x=uu, y=s.H[uu], yazi="3 barda geri dönüş yok", yukari=True, dy=2)
        stop = min(s.L[t:uu + 1])
    else:
        uu = s.bar(PL - 0.5 * u, PL + 1.0 * u, PL - 0.6 * u, PL + 0.8 * u)
        s.isa(tur="ok", x=uu, y=s.H[uu], yazi="geri aralığa kapanış = tuzak", yukari=True)
        stop = min(s.L[t:uu + 1])
    s.yuru(8, 0.002)
    if tip != "gercek_kirilim":
        s.isa(tur="giris", x=uu + 1, y=s.O[uu + 1], yazi="giriş: sonraki açılış")
    s.isa(tur="cizgi", y=stop, x0=t, x1=uu + 6, yazi="stop (t'den beri en dip)", renk="#c00000")
    return {"ilk": t, "son": uu, "e": uu + 1}


def _yb_w6(s: _WDSeri, tip: str) -> Dict[str, int]:
    eg = 0.003 if tip == "yukselis" else -0.003
    s.yuru(45, eg); s.trend(12, 1.6 * eg); u = s.u()
    s.isa(tur="kutu", x0=s.n - 11, x1=s.n - 1, yazi="yükseliş bağlamı" if tip == "yukselis" else "düşüş bağlamı")
    o = s.c - 0.2 * u; c = o + 0.3 * u; l_ = min(o, c) - 2.2 * u; h = max(o, c) + (1.0 * u if tip == "ust_fitil" else 0.05 * u)
    t = s.bar(o, h, l_, c)
    s.isa(tur="ok", x=t, y=l_, yazi="uzun alt fitil (>= 2 x gövde)", yukari=False)
    s.isa(tur="ok", x=t, y=h, yazi="üst fitil UZUN" if tip == "ust_fitil" else "küçük gövde, üst fitil yok", yukari=True, dy=2)
    s.isa(tur="cizgi", y=l_, x0=t, x1=t + 6, yazi="stop (mumun dibi)", renk="#c00000")
    s.yuru(8, 0.002)
    s.isa(tur="giris", x=t + 1, y=s.O[t + 1], yazi="giriş: sonraki açılış")
    return {"ilk": t, "son": t, "e": t + 1}


def _yb_w7(s: _WDSeri, tip: str, dar: bool = False) -> Dict[str, int]:
    s.yuru(45, -0.003); s.trend(12, -0.005); u = s.u()
    vmed = float(np.median(s.V[-20:])); ort = u
    boy = (1.6 if (not dar or tip == "genis") else 0.8) * ort
    l_ = min(s.L[-20:]) - 0.1 * u; h = l_ + boy
    if tip == "dipte_kapanis":
        c = l_ + 0.1 * boy; o = l_ + 0.6 * boy
    else:
        c = l_ + 0.75 * boy; o = l_ + 0.45 * boy
    v = (1.3 if tip == "dusuk_hacim" else 3.0) * vmed
    t = s.bar(o, h, l_, c, v=v)
    s.isa(tur="kutu", x0=t - 11, x1=t - 1, yazi="düşüş bağlamı")
    s.isa(tur="ok", x=t, y=l_, yazi="20 günün en dibi", yukari=False)
    s.isa(tur="ok", x=t, y=h, yazi=("kapanış DİPTE" if tip == "dipte_kapanis" else "kapanış üst yarıda") + (", geniş mum" if tip == "genis" else ""),
          yukari=True, dy=2)
    s.isa(tur="hacim", x=t, yazi=f"hacim {v / vmed:.1f} x medyan".replace(".", ","))
    s.isa(tur="cizgi", y=l_, x0=t, x1=t + 6, yazi="stop (mumun dibi)", renk="#c00000")
    s.yuru(8, 0.002)
    s.isa(tur="giris", x=t + 1, y=s.O[t + 1], yazi="giriş: sonraki açılış")
    return {"ilk": t, "son": t, "e": t + 1}


# kol -> (temel yukarı yapıcı, ayna mı, negatif tipleri (2 PDF için ilk ikisi))
WD_YAPI: Dict[str, Tuple[Any, bool, List[str]]] = {
    "W1": (_yb_w1, False, ["bosluk", "fitil", "yukselis"]), "W1T": (_yb_w1, True, ["bosluk", "fitil", "yukselis"]),
    "W2": (_yb_w2, False, ["kapanis_disari", "kisa_fitil"]), "W2T": (_yb_w2, True, ["kapanis_disari", "kisa_fitil"]),
    "W2E": (_yb_w2e, False, ["esit_degil", "tek_dip"]), "W2TE": (_yb_w2e, True, ["esit_degil", "tek_dip"]),
    "W3": (_yb_w3, False, ["ulasmadi", "fitil_kapanis"]), "W3T": (_yb_w3, True, ["ulasmadi", "fitil_kapanis"]),
    "W4": (_yb_w4y, True, ["bos_yok", "gercek_kirilim"]), "W4Y": (_yb_w4y, False, ["bos_yok", "gercek_kirilim"]),
    "W5": (_yb_w5y, True, ["gercek_kirilim", "sadece_fitil"]), "W5Y": (_yb_w5y, False, ["gercek_kirilim", "sadece_fitil"]),
    "W6": (_yb_w6, False, ["yukselis", "ust_fitil"]), "W6T": (_yb_w6, True, ["yukselis", "ust_fitil"]),
    "W7": (_yb_w7, False, ["dipte_kapanis", "dusuk_hacim"]), "W7D": (lambda s, tip: _yb_w7(s, tip, dar=True), False, ["genis", "dipte_kapanis"]),
    "W7T": (_yb_w7, True, ["dipte_kapanis", "dusuk_hacim"]),
}
WD_NEDEN: Dict[str, str] = {
    "bosluk": "açılışlar önceki gövdenin dışında (boşluklu)", "fitil": "uzun üst fitiller (kapanış tepeye yakın değil)",
    "yukselis": "bağlam ters (önceki 10 bar yükseliş)", "kapanis_disari": "fitil değil: seviyenin ötesinde kapanış (gerçek kırılım)",
    "kisa_fitil": "fitil kısa (boyun yarısından az)", "esit_degil": "ikinci dip / tepe 0,25 ATR'den uzak (eşit değil)",
    "tek_dip": "tek dip / tepe (eşitlik yok)", "ulasmadi": "ertesi gün seviyeye ulaşmadı (giriş yok)", "fitil_kapanis": "seviyenin ötesinde kapanış yok (yalnız fitil)",
    "bos_yok": "yapı kırılımı yok (kapanış seviyeyi geçmedi)", "gercek_kirilim": "seviyenin ötesinde kapanış sürdü (tuzak / süpürme değil)",
    "sadece_fitil": "kırılım kapanışı yok (yalnız fitil)", "ust_fitil": "karşı fitil uzun", "dipte_kapanis": "yüksek hacim ama kapanış uçta (emilim değil)",
    "dusuk_hacim": "hacim 2 x medyanın altında", "genis": "mum dar değil (boy > ORT_BOY)",
}


def wd_ayna(Dz: Dict[str, np.ndarray], isaret: List[Dict[str, Any]]) -> Tuple[Dict[str, np.ndarray], List[Dict[str, Any]]]:
    """Fiyat aynası (P' = M - P; M = 2 x en yüksek): yukarı desen -> aşağı desen; geometri birebir. İşaretler de aynalanır."""
    M = 2.0 * float(np.max(Dz["H"]))
    D = {"O": M - Dz["O"], "H": M - Dz["L"], "L": M - Dz["H"], "C": M - Dz["C"], "V": Dz["V"].copy()}
    ceviri = {"dip": "tepe", "Dip": "Tepe", "dibi": "tepesi", "dibin": "tepenin", "dipler": "tepeler", "dibe": "tepeye", "DİPTE": "TEPEDE",
              "alt fitil": "üst fitil", "ALTINDA": "ÜSTÜNDE", "altında": "üstünde", "ÜSTÜNDE": "ALTINDA", "üst yarıda": "alt yarıda",
              "düşüş bağlamı": "yükseliş bağlamı", "yükseliş bağlamı": "düşüş bağlamı", "üst fitil": "alt fitil", "yerel tepe": "yerel dip",
              "+2R": "-2R", "PL": "PH", "dipte": "tepede", "- 0,1 ATR": "+ 0,1 ATR", "- 1 tik": "+ 1 tik"}

    def cevir(m: str) -> str:
        parca = sorted(ceviri, key=len, reverse=True); out = ""; i = 0
        while i < len(m):
            for p in parca:
                if m.startswith(p, i):
                    out += ceviri[p]; i += len(p); break
            else:
                out += m[i]; i += 1
        return out
    I2 = []
    for r in isaret:
        r = dict(r)
        if "y" in r:
            r["y"] = M - r["y"]
        if "yukari" in r:
            r["yukari"] = not r["yukari"]
        if "yazi" in r:
            r["yazi"] = cevir(r["yazi"])
        I2.append(r)
    return D, I2


def wd_yapay(kol: str, tip: str, P0: float, oyn: float, tohum: int, gurultu: float = 0.0) -> Dict[str, Any]:
    """Bir yapay seri: kol'un pozitifi (tip = 'poz') ya da negatifi; ayna kollarda yukarı yapı aynalanır; gürültü desen barlarına."""
    yapici, ayna, _ = WD_YAPI[kol]
    rng = np.random.default_rng([int(tohum), zlib.crc32(f"{kol}|{tip}".encode())])
    s = _WDSeri(100.0, rng, oyn); bil = yapici(s, tip); D = s.dizi(); isa = s.isaret
    if ayna:
        D, isa = wd_ayna(D, isa)
    k = P0 / float(np.median(D["C"]))
    for a in ("O", "H", "L", "C"):
        D[a] = D[a] * k
    isa = [dict(r, y=r["y"] * k) if "y" in r else r for r in isa]
    if gurultu > 0:
        a, b = bil["ilk"], bil["son"]; boy = (D["H"] - D["L"])[a:b + 1]
        for c in ("O", "H", "L", "C"):
            D[c][a:b + 1] = D[c][a:b + 1] + rng.normal(0, 1, b - a + 1) * gurultu * boy
        O, H, L, C = D["O"], D["H"], D["L"], D["C"]
        D["H"] = np.maximum.reduce([O, H, L, C]); D["L"] = np.minimum.reduce([O, H, L, C])
        z = ~(D["H"] > D["L"]); D["H"][z] = D["L"][z] * (1 + 1e-4)
    return {**D, **bil, "isaret": isa, "kol": kol, "tip": tip}


def wd_sentetik_olc(kol: str, tip: str, gurultu: float, E: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Yakalama (tip 'poz') ya da yanlış kabul payı: ölçekler x oynaklık x tohum."""
    E = E or WD_ESIK["sentetik"]; n = 0; ok = 0
    for P0 in E["olcek"]:
        for oyn in E["oyn"]:
            for tt in range(int(E["tohum_sayi"])):
                Y = wd_yapay(kol, tip, P0, oyn, tt, gurultu)
                D, _ = wd_tara(Y["O"], Y["H"], Y["L"], Y["C"], Y["V"], [kol])
                if tip == "poz":
                    hit = bool((D.e == Y["e"]).any())
                else:
                    hit = bool(((D.e >= Y["ilk"]) & (D.e <= Y["e"] + 2)).any())
                n += 1; ok += int(hit)
    return {"n": n, "pay": ok / n if n else None}


def wd_rastgele_siklik(E: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
    """Rastgele yürüyüş serilerinde (hacim lognormal) kol başına 1000 barda olay (ham, filtresiz)."""
    E = E or WD_ESIK["sentetik"]; R = E["rastgele"]; say = {k: 0 for k in WD_KOLLAR}; bar = 0
    for i in range(int(R["seri"])):
        rng = np.random.default_rng([int(WD_ESIK["boot"]["tohum"]), i]); s = _WDSeri(50.0, rng, float(E["oyn"][i % len(E["oyn"])]))
        s.yuru(int(R["uzunluk"]), 0.0); D, _ = wd_tara(*(np.asarray(getattr(s, a), float) for a in ("O", "H", "L", "C", "V")))
        bar += s.n
        for k, c in D.kol.value_counts().items():
            say[k] += int(c)
    return {k: round(1000.0 * v / bar, 4) for k, v in say.items()}


def wd_sentetik(cikti: Optional[str] = None) -> Dict[str, Any]:
    """Bütün kollar: pozitif yakalama (3 gürültü) + negatif kabul (tip x 3 gürültü) + rastgele sıklık -> wd_sentetik.json."""
    t0 = time.time(); E = WD_ESIK["sentetik"]; J: Dict[str, Any] = {"surum": WD_SURUM, "esik_sha": wd_esik_sha(), "kol": {}}
    for kol in WD_KOLLAR:
        r: Dict[str, Any] = {"poz": {}, "neg": {}}
        for g in E["gurultu"]:
            r["poz"][str(g)] = wd_sentetik_olc(kol, "poz", g)
        for tip in WD_YAPI[kol][2]:
            r["neg"][tip] = {str(g): wd_sentetik_olc(kol, tip, g) for g in E["gurultu"]}
        r["yakalama_0"] = r["poz"]["0.0"]["pay"]
        r["kabul_0_en_cok"] = max(v["0.0"]["pay"] for v in r["neg"].values())
        r["kabul_hepsi_en_cok"] = max(x["pay"] for v in r["neg"].values() for x in v.values())
        r["hedef_tuttu"] = bool(r["yakalama_0"] >= E["hedef_yakala"] and r["kabul_0_en_cok"] <= E["hedef_kabul"])
        J["kol"][kol] = r
        wdlog.info("sentetik %s: yakalama %.2f, kabul en çok %.2f", kol, r["yakalama_0"], r["kabul_0_en_cok"])
    J["rastgele_1000_bar"] = wd_rastgele_siklik(E)
    J["sure_sn"] = round(time.time() - t0, 1)
    MI._mi_jyaz(_wd_yol("sentetik", cikti), J, "wd_sentetik")
    return J


# ================================================================ 7) ÇİZİM (yapay + gerçek)
def _wd_plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    return plt


def _wd_mum(ax, O, H, L, C, x0: int = 0, gen: float = 0.62) -> None:
    MI._mi_mum_ciz(ax, O, H, L, C, x0=x0, genislik=gen)


def _wd_isaret_ciz(ax, isaret: List[Dict[str, Any]], x_ofset: int, yrng: float, fs: float = 11.5, x_son: Optional[float] = None) -> None:
    for r in isaret:
        tur = r.get("tur")
        if tur == "cizgi":
            x1 = r["x1"] - x_ofset + 0.4; xe = (x_son if x_son is not None else x1) + 0.3
            ax.hlines(r["y"], r["x0"] - x_ofset - 0.4, min(x1, xe), colors=r.get("renk", "#555555"), linestyles=r.get("stil", "-"), linewidth=1.8, zorder=5)
            if x1 < xe:
                ax.hlines(r["y"], x1, xe, colors=r.get("renk", "#555555"), linestyles=":", linewidth=0.8, zorder=5)
            ax.text(xe + 0.2, r["y"], r["yazi"], color=r.get("renk", "#555555"), fontsize=fs - 0.5, va="center", ha="left", weight="bold",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85), zorder=7, clip_on=True)
        elif tur in ("ok", "giris"):
            yuk = r.get("yukari", True) if tur == "ok" else False
            dy = (0.10 + 0.06 * r.get("dy", 1)) * yrng * (1 if yuk else -1)
            renk = "#1f4fbf" if tur == "giris" else "#222222"
            xt = r["x"] - x_ofset
            if tur == "giris":
                ax.plot(r["x"] - x_ofset, r["y"], marker=">", color=renk, markersize=12, zorder=8)
                xt = r["x"] - x_ofset + 2.5; dy = -0.05 * yrng
            ax.annotate(r["yazi"], xy=(r["x"] - x_ofset, r["y"]), xytext=(xt, r["y"] + dy), ha="left" if tur == "giris" else "center",
                        va="center" if tur == "giris" else ("bottom" if yuk else "top"),
                        fontsize=fs, weight="bold", color=renk, arrowprops=dict(arrowstyle="->", color=renk, lw=1.4), zorder=8,
                        bbox=dict(boxstyle="round,pad=0.2", fc="#fffbe6", ec=renk, lw=0.8))
        elif tur == "kutu":
            ax.axvspan(r["x0"] - x_ofset - 0.5, r["x1"] - x_ofset + 0.5, color="#bfbfbf", alpha=0.25, zorder=0)
            ax.text((r["x0"] + r["x1"]) / 2 - x_ofset, ax.get_ylim()[1], r["yazi"], ha="center", va="top", fontsize=fs - 1, color="#444444")


def _wd_yapay_ax(ax, Y: Dict[str, Any], once: int = 18, sonra: int = 14, fs: float = 11.5, baslik: str = "") -> None:
    a = max(0, Y["ilk"] - once)
    if Y["kol"] in ("W4", "W4Y"):
        a = max(0, Y["ilk"] - 6)
    b = min(len(Y["C"]), Y["e"] + sonra)
    O, H, L, C = (Y[c][a:b] for c in ("O", "H", "L", "C"))
    _wd_mum(ax, O, H, L, C)
    lo, hi = float(np.min(L)), float(np.max(H)); yr = hi - lo
    hv = any(r.get("tur") == "hacim" for r in Y["isaret"])
    ax.set_ylim(lo - (0.85 if hv else 0.32) * yr, hi + 0.32 * yr); ax.set_xlim(-1, (b - a) * 1.72)       # sağdaki %40 çizgi etiketlerine; hacim paneli altta
    ax.axvspan(Y["ilk"] - a - 0.5, Y["son"] - a + 0.5, color="#ffb347", alpha=0.22, zorder=0)
    isa = [r for r in Y["isaret"] if r.get("tur") != "hacim"]
    _wd_isaret_ciz(ax, isa, a, yr, fs, x_son=float(b - a))
    h = [r for r in Y["isaret"] if r.get("tur") == "hacim"]
    if h:
        axv = ax.inset_axes([0.0, 0.0, 1.0, 0.16]); x = np.arange(b - a)
        axv.bar(x, Y["V"][a:b], color=["#ff7f00" if i + a == h[0]["x"] else "#9a9a9a" for i in x], width=0.6)
        axv.set_xlim(ax.get_xlim()); axv.axis("off")
        axv.text(float(b - a) + 0.5, float(np.max(Y["V"][a:b])), h[0]["yazi"], fontsize=fs - 1, color="#ff7f00", weight="bold", va="top", ha="left",
                 bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.set_xticks([]); ax.set_yticks([])
    if baslik:
        ax.set_title(baslik, fontsize=fs + 1.5, weight="bold", loc="left")


WD_KURAL_METNI: Dict[str, List[str]] = {
    "W1": ["Düşüşten sonra art arda 3 büyük yeşil mum; her biri bir öncekinden yüksek kapanır.", "Her mum tepesine yakın kapanır; 2. ve 3. mum bir öncekinin gövdesi içinde açılır.",
           "Giriş: 3. mumdan sonraki açılış. Stop: 1. mumun dibi."],
    "W1T": ["Yükselişten sonra art arda 3 büyük kırmızı mum; her biri bir öncekinden düşük kapanır.", "Her mum dibine yakın kapanır; açılışlar önceki gövdenin içinde.",
            "Giriş (satış): 3. mumdan sonraki açılış. Stop: 1. mumun tepesi."],
    "W2": ["Fiyat son 20 günün dibinin (en az 4 gün önceki) altına fitil atar.", "Aynı gün dibin üstünde kapanır; alt fitil mumun en az yarısıdır.",
           "Giriş: ertesi açılış. Stop: fitil dibi - 0,1 ATR."],
    "W2T": ["Fiyat son 20 günün tepesinin (en az 4 gün önceki) üstüne fitil atar.", "Aynı gün tepenin altında kapanır; üst fitil mumun en az yarısıdır.",
            "Giriş (satış): ertesi açılış. Stop: fitil tepesi + 0,1 ATR."],
    "W2E": ["Dip süpürme (W2) + süpürülen dipte eşitlik:", "son 20 günde aynı seviyede (0,25 ATR içinde), arası en az 3 bar olan en az iki dip.",
            "Giriş: ertesi açılış. Stop: fitil dibi - 0,1 ATR."],
    "W2TE": ["Tepe süpürme (W2T) + süpürülen tepede eşitlik:", "son 20 günde aynı seviyede (0,25 ATR içinde), arası en az 3 bar olan en az iki tepe.",
             "Giriş (satış): ertesi açılış. Stop: fitil tepesi + 0,1 ATR."],
    "W3": ["Bugün fiyat 20 günlük dibin (en az 3 gün önceki) altında ya da ona eşit kapanır.",
           "Yarın fiyat o dibe geri çıkarsa dipte alış (açılış dibin üstündeyse açılışta); çıkmazsa işlem yok.", "Stop: iki günün en dibinin 1 tik (%0,1) altı."],
    "W3T": ["Bugün 20 günlük tepenin üstünde ya da ona eşit kapanış.", "Yarın fiyat o tepeye geri inerse tepede satış (açılış tepenin altındaysa açılışta).",
            "Stop: iki günün en tepesinin 1 tik (%0,1) üstü."],
    "W4": ["Tepe süpürme (W2T) olur; sonraki 10 bar içinde fiyat son yerel dibin altında kapanır (yapı kırılımı).",
           "Kırılımdan sonraki 5 bar içinde fiyat o seviyeye geri çıkarsa seviyede satış (geri test).", "Stop: süpürme mumunun tepesi. Hedef çizgisi: 2R."],
    "W4Y": ["Dip süpürme (W2) olur; sonraki 10 bar içinde fiyat son yerel tepenin üstünde kapanır (yapı kırılımı).",
            "Kırılımdan sonraki 5 bar içinde fiyat o seviyeye geri inerse seviyede alış (geri test).", "Stop: süpürme mumunun dibi. Hedef çizgisi: 2R."],
    "W5": ["Bugün 20 günlük tepenin üstünde kapanış (kırılım gibi görünür).", "Sonraki 1-3 bar içinde tepenin altında kapanış: tuzak.",
           "Giriş (satış): o barın ertesi açılışı. Stop: kırılımdan beri en tepe."],
    "W5Y": ["Bugün 20 günlük dibin altında kapanış (kırılım gibi görünür).", "Sonraki 1-3 bar içinde dibin üstünde kapanış: tuzak.",
            "Giriş: o barın ertesi açılışı. Stop: kırılımdan beri en dip."],
    "W6": ["Düşüşte, son 10 günün en dibinde küçük gövdeli mum.", "Alt fitil gövdenin en az 2 katı; üst fitil yok gibi (boyun %10'u); boy olağanın en az %80'i.",
           "Giriş: ertesi açılış. Stop: mumun dibi."],
    "W6T": ["Yükselişte, son 10 günün en tepesinde küçük gövdeli mum.", "Üst fitil gövdenin en az 2 katı; alt fitil yok gibi (boyun %10'u).",
            "Giriş (satış): ertesi açılış. Stop: mumun tepesi."],
    "W7": ["Düşüşte, 20 günün en dibinde, hacim önceki 20 günün medyanının en az 2 katı.", "Kapanış mumun üst yarısında (satış emildi).",
           "Giriş: ertesi açılış. Stop: mumun dibi. (Gerçek emilim mum içi veri ister; bu günlük vekil.)"],
    "W7D": ["W7 + mum dar: boy olağan boydan (önceki 10 günün medyanı) büyük değil.", "'Çaba var, sonuç yok': yüksek hacme rağmen fiyat az gitti.",
            "Giriş: ertesi açılış. Stop: mumun dibi."],
    "W7T": ["Yükselişte, 20 günün en tepesinde, hacim medyanın en az 2 katı.", "Kapanış mumun alt yarısında (alış emildi).",
            "Giriş (satış): ertesi açılış. Stop: mumun tepesi."],
}


def wd_yapay_pdf(cikti: Optional[str] = None, sent: Optional[Dict[str, Any]] = None) -> str:
    """WD_YAPAY_DESENLER.pdf: kapak + desen başına bir sayfa (üstte etiketli yapay desen, altta 2 'yakın ama değil', en altta kural + kaynak)."""
    plt = _wd_plt()
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or WD_YOL["cikti"]; yol = _wd_yol("yapay_pdf", cikti)
    if sent is None and os.path.exists(_wd_yol("sentetik", cikti)):
        sent = json.load(open(_wd_yol("sentetik", cikti), encoding="utf-8"))
    os.makedirs(cikti, exist_ok=True)

    def damga(fig):
        fig.text(0.5, 0.995, "YAPAY VERİ", ha="center", va="top", fontsize=26, color="#c00000", weight="bold")
        fig.text(0.5, 0.5, "YAPAY VERİ", ha="center", va="center", fontsize=80, color="#c00000", alpha=0.06, rotation=30, weight="bold")
    with PdfPages(yol, metadata={"Title": "WEB_DESEN yapay desenler", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); damga(fig)
        sat = ["Web'de anlatılan bilinen desenler: yapay örnekler", "",
               "Her sayfada bir desen: üstte desenin kuralına göre çizilmiş", "YAPAY mumlar (gerçek hisse değil), etiketleriyle.",
               "Altta 'yakın ama değil' iki örnek ve neden sayılmadığı.", "En altta kuralın düz Türkçesi ve kaynağı.", "",
               "Turuncu bant = desen barları. Mavi ok = giriş.", "Kırmızı çizgi = stop. Yeşil = hedef.", "",
               "Dedektör bu yapay örneklerle sınandı (yakalama / yanlış kabul):"]
        for i, s_ in enumerate(sat):
            fig.text(0.07, 0.90 - i * 0.032, s_, fontsize=15 if i else 19, weight="bold" if not i else "normal")
        if sent:
            y = 0.90 - len(sat) * 0.032 - 0.01
            for i, kol in enumerate(WD_KOLLAR):
                r = sent["kol"][kol]
                fig.text(0.09 if i < 9 else 0.53, y - (i % 9) * 0.03,
                         f"{kol}: yakalama %{r['yakalama_0'] * 100:.0f} · yanlış kabul %{r['kabul_0_en_cok'] * 100:.0f}", fontsize=12.5)
            fig.text(0.07, 0.10, "(gürültüsüz yapay set; hedef yakalama >= %90, yanlış kabul <= %5;\n%10 / %20 gürültülü sonuçlar ön kayıtta)", fontsize=11.5,
                     color="#444444")
        pdf.savefig(fig); plt.close(fig)
        for kol in WD_KOLLAR:
            fig = plt.figure(figsize=(8.3, 11.7)); damga(fig)
            yon = "YUKARI (alış)" if WD_KOL[kol]["yon"] == 1 else "AŞAĞI (satış)"
            fig.text(0.05, 0.935, f"{kol}  {WD_KOL[kol]['ad']}", fontsize=21, weight="bold"); fig.text(0.05, 0.903, f"Kaynağın iddiası: {yon}", fontsize=14)
            ax = fig.add_axes([0.03, 0.47, 0.94, 0.41])
            Y = wd_yapay(kol, "poz", 100.0, 0.005, 3)
            _wd_yapay_ax(ax, Y, once=14, sonra=19 if kol in ("W4", "W4Y") else 10, fs=12)
            for i, tip in enumerate(WD_YAPI[kol][2][:2]):
                axn = fig.add_axes([0.03 + i * 0.49, 0.185, 0.44, 0.235])
                Yn = wd_yapay(kol, tip, 100.0, 0.005, 3)
                Yn["isaret"] = [r for r in Yn["isaret"] if r.get("tur") != "giris"]          # negatifte giriş yok
                _wd_yapay_ax(axn, Yn, once=10, sonra=6, fs=8)
                axn.set_title(f"YAKIN AMA DEĞİL {i + 1}", fontsize=12.5, weight="bold", color="#c00000", loc="left")
                fig.text(0.03 + i * 0.49, 0.172, "neden: " + WD_NEDEN[tip], fontsize=10.5, va="top", wrap=True)
            for i, s_ in enumerate(WD_KURAL_METNI[kol]):
                fig.text(0.05, 0.118 - i * 0.026, f"{i + 1}. {s_}", fontsize=11.2, va="top")
            fig.text(0.05, 0.035, "Kaynak: " + WD_KOL[kol]["kaynak"], fontsize=9.5, color="#444444", va="top")
            if sent:
                r = sent["kol"][kol]
                fig.text(0.97, 0.903, f"dedektör: yakalama %{r['yakalama_0'] * 100:.0f} · yanlış kabul %{r['kabul_0_en_cok'] * 100:.0f}", fontsize=11.5,
                         ha="right", color="#1f4fbf")
            pdf.savefig(fig); plt.close(fig)
    return yol


def wd_gercek_pdf(cikti: Optional[str] = None, ham: Optional[str] = None, yo_ham: Optional[str] = None, adet: int = 4) -> str:
    """WD_GERCEK_ORNEKLER.pdf: desen başına gerçek veriden rastgele 4 olay (tohum 2711): öncesi 60 bar + desen barları; SONRASI YOK (son bar = desenin
    tanındığı bar: sonraki açılışta girilen desenlerde sinyal barı, bar içi girişlerde giriş barı); sağda yüzde ekseni (0 = son çizilen kapanış)."""
    import MUM_IZI_HAKEM as HK
    plt = _wd_plt()
    from matplotlib.backends.backend_pdf import PdfPages
    cikti = cikti or WD_YOL["cikti"]; yol = _wd_yol("gercek_pdf", cikti)
    TS = {p: pickle.load(open(_wd_ham(f"olay_{p}.pkl", ham), "rb")) for p in WD_PAZAR}
    PN = {p: wd_panel_yukle(p, yo_ham) for p in WD_PAZAR}
    with PdfPages(yol, metadata={"Title": "WEB_DESEN gerçek örnekler", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7))
        sat = ["Web desenleri: gerçek veriden rastgele örnekler", "", "Her sayfada bir desen kolu, 4 rastgele olay (ABD + Avrupa,", "2016-2022; tohum 2711).",
               "Gösterilen: desenden önceki 60 mum + desen (turuncu).", "SONRASI GÖSTERİLMİYOR: son mum, desenin tanındığı mum.",
               "Kırmızı kesik = stop; mavi = giriş seviyesi / açılışı;", "gri kesik = süpürülen / kırılan seviye.",
               "Sağdaki eksen: son kapanışa göre yüzde (0 = son kapanış)."]
        for i, s_ in enumerate(sat):
            fig.text(0.07, 0.90 - i * 0.034, s_, fontsize=15 if i else 19, weight="bold" if not i else "normal")
        pdf.savefig(fig); plt.close(fig)
        for kol in WD_KOLLAR:
            A = pd.concat([TS[p][TS[p].kol == kol] for p in WD_PAZAR], ignore_index=True)
            fig = plt.figure(figsize=(8.3, 11.7))
            fig.text(0.04, 0.965, f"{kol}  {WD_KOL[kol]['ad']} — gerçek örnekler (sonrası yok)", fontsize=16, weight="bold", va="top")
            if not len(A):
                fig.text(0.1, 0.5, "olay yok", fontsize=20); pdf.savefig(fig); plt.close(fig); continue
            sec = _wd_rng(f"gercek|{kol}").choice(len(A), size=min(adet, len(A)), replace=False)
            for q, i in enumerate(sorted(sec)):
                r = A.iloc[int(i)]; Pn = PN[r.pazar]; j = int(r.j); a0 = int(Pn["off"][j])
                son = int(r.e) if kol in WD_ICGIRIS else int(r.t)
                bas = max(0, int(r.ilk) - 60)
                sl = slice(a0 + bas, a0 + son + 1)
                O, H, L, C = Pn["O"][sl], Pn["H"][sl], Pn["L"][sl], Pn["C"][sl]
                ax = fig.add_axes([0.05 + (q % 2) * 0.485, 0.50 - (q // 2) * 0.455, 0.39, 0.39])
                _wd_mum(ax, O, H, L, C, gen=0.7)
                kutu = (int(r.ilk) - bas, son - bas)
                ax.axvspan(kutu[0] - 0.5, kutu[1] + 0.5, color="#ffb347", alpha=0.25, zorder=0)
                y0, y1 = HK.hk_y_sinir(O, H, L, C, kutu)
                ax.set_ylim(y0, y1); ax.set_xlim(-0.8, len(C) + 3)
                ref = float(C[-1]); _, yz = HK.hk_yuzde_adim(y0, y1, ref)
                ax.yaxis.tick_right(); ax.set_yticks([ref * (1 + p / 100) for p in yz]); ax.set_yticklabels([HK._hk_yuzde_yazi(p) for p in yz], fontsize=9)
                for p in yz:
                    ax.axhline(ref * (1 + p / 100), color="#9a9a9a", linewidth=0.4, linestyle=":", zorder=1)
                ax.set_xticks([])
                x1 = len(C) + 2
                if np.isfinite(r.stop) and y0 <= r.stop <= y1:
                    ax.hlines(r.stop, kutu[0] - 0.5, x1, colors="#c00000", linestyles="--", linewidth=1.3); ax.text(x1, r.stop, "stop", color="#c00000",
                                                                                                                       fontsize=9, ha="right", va="bottom")
                if kol in WD_ICGIRIS:
                    ax.plot(son, r.giris, marker=">", color="#1f4fbf", markersize=9, zorder=9)
                    ax.hlines(r.seviye, kutu[0] - 0.5, x1, colors="#777777", linestyles="--", linewidth=1.0)
                    ax.text(son, r.giris, " giriş", color="#1f4fbf", fontsize=9, va="center", weight="bold")
                else:
                    ax.annotate("giriş: sonraki açılış", xy=(son + 0.6, C[-1]), xytext=(son - 8, y1 - 0.08 * (y1 - y0)), fontsize=8.5, color="#1f4fbf",
                                arrowprops=dict(arrowstyle="->", color="#1f4fbf"))
                    if np.isfinite(r.seviye):
                        ax.hlines(r.seviye, kutu[0] - 0.5, x1, colors="#777777", linestyles="--", linewidth=1.0)
                    if kol.startswith("W2"):
                        lv = _wd_seviye_w2(Pn, j, int(r.t), WD_KOL[kol]["yon"])
                        if np.isfinite(lv):
                            ax.hlines(lv, max(0, kutu[0] - 20), x1, colors="#777777", linestyles="--", linewidth=1.0)
                            ax.text(max(0, kutu[0] - 20), lv, "20 günlük uç", fontsize=8, color="#555555", va="bottom")
                tar = pd.Timestamp(Pn["tarih"][Pn["POS"][a0 + son]]).date()
                ax.set_title(f"{r.pazar} {r.sembol} · {tar}", fontsize=10.5, loc="left")
            pdf.savefig(fig); plt.close(fig)
    return yol


def _wd_seviye_w2(Pn: Dict[str, np.ndarray], j: int, t: int, yon: int) -> float:
    a = int(Pn["off"][j]); w = int(WD_ESIK["ortak"]["uc_pencere"])
    if t < w:
        return float("nan")
    x = Pn["L"][a + t - w:a + t] if yon == 1 else Pn["H"][a + t - w:a + t]
    return float(x.min() if yon == 1 else x.max())


# ================================================================ 8) GERÇEK VERİ AKIŞI (olay -> ön kayıt -> kapı -> ölçüm -> rapor)
def wd_olay(ham: Optional[str] = None, yo_ham: Optional[str] = None) -> Dict[str, Any]:
    """Getirisiz: iki pazarda olaylar -> olay_{pazar}.pkl + sayim.json (ham klasörü)."""
    ham = ham or WD_YOL["ham"]; os.makedirs(ham, exist_ok=True); TS, INFO = {}, {}
    for p in WD_PAZAR:
        P = wd_panel_yukle(p, yo_ham); Vd = MI.mi_veri(p, WD_YOL["acik"])
        Xs, _ = YO.yo_yukle(p, yo_ham or WD_YOL["yo_ham"]); Xs = Xs[["j", "k", "hucre"]]
        T, info = wd_olay_pazar(p, P, Vd, Xs); TS[p] = T; INFO[p] = info
        with open(_wd_ham(f"olay_{p}.pkl", ham), "wb") as f:
            pickle.dump(T, f, protocol=4)
        del P, Vd
    S = wd_sayim(TS, INFO); S["info"] = INFO
    MI._mi_jyaz(_wd_ham("sayim.json", ham), S, "wd_sayim")
    return S


def wd_dosya_sha(ham: Optional[str] = None, yo_ham: Optional[str] = None) -> Dict[str, str]:
    out = {}
    for p in WD_PAZAR:
        out[f"olay_{p}.pkl"] = MI._mi_sha(_wd_ham(f"olay_{p}.pkl", ham))
        out[f"YO_ham_{p}.npz"] = MI._mi_sha(os.path.join(yo_ham or WD_YOL["yo_ham"], f"ham_{p}.npz"))
        out[f"YO_ozellik_{p}.pkl"] = MI._mi_sha(os.path.join(yo_ham or WD_YOL["yo_ham"], f"ozellik_{p}.pkl"))
    return out


WD_YORUM = [
    "PL / PH YAŞI: 'uç en az 4 seans eski' = önceki 20 barın en düşüğünün (eşitlerde SON görüldüğü bar) indeksi t - 4 ya da daha eski; değilse o bar için PL "
    "yok sayılır (olay yok). W3'te 3.",
    "ORT_BOY: desenin İLK barından önceki 10 barın boy medyanı; üç mumlu desende üç mum da aynı ORT_BOY ile karşılaştırılır (desen mumları kendi eşiğini şişirmez).",
    "BAĞLAM: DÜŞÜŞ = C[ilk-1] < C[ilk-11] (iş tanımı 'desenin ilk barından önceki kapanış, ondan 10 bar önceki kapanışın altında'); W6 / W7'de ilk = t.",
    "W1 'açılış önceki gövde içinde': O_b ∈ [O_a, C_a], O_c ∈ [O_b, C_b] (sınır dahil). 'Kapanışlar yükselen' kesin (<).",
    "W2E 'aralarında en az 3 bar' = iki dip indeks farkı >= 4; yerel dip i + 2 <= t - 1 (süpürme barından önce tamamlanmış); tolerans ATR_t ile.",
    "W3 'ulaşırsa giriş' gün içi sıra varsayımı: t + 1 barında H >= PL ise giriş olmuş sayılır; açılış PL'nin üstünde (>=) ise açılış fiyatıyla, değilse PL'de. "
    "1 tik = %0,1 (x 0,999 / x 1,001; iş tanımı). Stop t + 1'in TAM gün dibini kullanır (kaynağın kuralı; giriş anında bilinmeyebilir: R'yi büyütür, +2R'yi zorlaştırır).",
    "W4 KIRILAN SEVİYE: süpürme barı s'den ÖNCE tamamlanmış (i + 2 <= s - 1) en son yerel dibin L'si (W4Y'de en son yerel tepenin H'si); geri bakış sınırı yok. "
    "Yapı kırılımı = s+1 .. s+10 içinde İLK kapanış seviyenin ötesinde; geri test = kırılımdan sonraki 5 bar içinde İLK seviyeye dokunuş; açılış seviyeyi "
    "geçmişse (W4: O >= seviye; W4Y: O <= seviye) açılışta. Kırılım ile geri test arasında stopa dokunma aranmaz (pozisyon yok).",
    "W5: 'sonraki 1-3 bar' = t+1 .. t+3; ilk geri kapanış barı u; giriş u + 1 açılışı; stop = H_t .. H_u en yükseği (W5Y: en düşük L).",
    "W6 'L son 10 barın en düşüğü' = L_t <= min(L_{t-9..t}) (t dahil); W7'de 20. W7T 'kapanış alt yarıda' = (C - L) / boy <= 0,5 (W7'nin >= 0,5 aynası).",
    "W7 hacim: V_t >= 2 x medyan(V_{t-20..t-1}) (t hariç). Hacim, MI.mi_veri günlük açık kopyasının Volume sütunu (YO paneliyle bar bar eşit; assert). "
    "Hacim verisi VAR (iki pazarda); W7 kolları ölçülür.",
    "GİRİŞ BARI DAHİL: sonuç barları e .. e+14 (YO gibi giriş barı dahil). Bar içi girişlerde (W3 / W4) giriş barının H / L'si girişten önce de oluşmuş "
    "olabilir: aynı barda hedef ve stop = STOP ÖNCE (kötümser; iki yönde aynı). Giriş barında stopa dokunuş da sayılır (kötümser).",
    "ATR HEDEFİ: ATR(e-1) (giriş barından önceki son tamamlanmış bar); taban günlerinde ATR(k) (giriş k + 1); taban hissenin aynı hücredeki YO örnek günleri "
    "(k % 5 == 0, P2), giriş açılışta.",
    "+2R TABANI: olayın R / giriş oranı r ile aynı hissenin aynı hücredeki örnek günlerinde H >= O(1 + 2r) önce mi L <= O(1 - r) önce mi (aşağıda ayna).",
    "R KATI: stopa ilk dokunulan bar; o bar e'den sonraysa ve açılışı stopun ötesindeyse çıkış açılışta (boşluk kaybı), değilse stop seviyesinde; dokunulmazsa C[e+14].",
    "10 GÜN YÖN: yön x (C[e+9] - giriş) > 0 (giriş barı 1. gün). Bulkowski'nin %82-84 / %78-79 / %60 / %59'u 'kırılım yönü' oranıdır; bizim ölçü aynı değil, "
    "yalnız yan yana yazılır.",
    "TOPLAM FARK / SEÇİM / ATR / +2R / R katı yön düzeltmeli (aşağı desende işaret çevrilir). SEÇİM'de P15 giriş satırının açılışından (bar içi girişte de).",
    "BH: kol p'si = dört ABD p'sinin en büyüğü (TF ve KAT, iki dönem; kesişim-birleşim). Aile 17 kol. p = (1 + #(boot <= sıfır)) / (B + 1).",
    "AVR şartı yalnız n >= 100 hücrede; n < 100 hücrede şart aranmaz, 'AVR n < 100' notu yazılır. ÖLÇÜLEMEDİ yalnız ABD hücreleriyle (n < 300 ya da ay < 12).",
    "TEKİL: aynı hisse aynı kolda giriş barı farkı < 5 olan ikinci olay atılır (giriş barına göre, filtrelerden sonra). Kollar arası örtüşme atılmaz (ayrı ölçülür).",
    "KİLİTLİ: desenin ilk barının tarihi .. giriş barının tarihi takvim aralığında ham veride geçersiz bar payı > 0,20 -> atılır (MUM_IZI_UC.uc_kilitli_pay).",
    "Evren bugün yaşayan hisseler: aşağı yönlü desenlerin aleyhine, yukarı yönlülerin lehine; T1 aynı evrenden olduğu için TOPLAM FARK bu yanlılığı kısmen giderir.",
]


def _wd_f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return (f"{x * 100:.{n}f}" if yuzde else f"{x:.{n}f}").replace(".", ",")


def wd_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None, yo_ham: Optional[str] = None) -> str:
    cikti = cikti or WD_YOL["cikti"]; S = json.load(open(_wd_ham("sayim.json", ham), encoding="utf-8"))
    SJ = json.load(open(_wd_yol("sentetik", cikti), encoding="utf-8"))
    sh = wd_dosya_sha(ham, yo_ham); Sc = {k: v for k, v in S.items() if k != "info"}
    L = [f"# WD_ON_KAYIT — web desenleri: gerçek veride sonrası ölçümünden ÖNCE ({time.strftime('%Y-%m-%d %H:%M')})", "",
         f"Sürüm: {WD_SURUM}. İş tanımı: WD_IS_TANIMI.md. Sonuç dosyası (wd_sonuc.json) bu ön kayıt commit + push edilmeden üretilmez (kapı).", "",
         "## Mühürler", f"WD_KOD_SHA: {wd_kod_sha()}", f"WD_ESIK_SHA: {wd_esik_sha()}"]
    L += [f"DOSYA_{a}: {v}" for a, v in sh.items()]
    L += [f"SAYIM_SHA: {HV.hv_json_sha(Sc)}", f"SENTETIK_SHA: {MI._mi_sha(_wd_yol('sentetik', cikti))}", "",
          "## Eşik sözlüğü (WD_ESIK, sabit)", "```json", json.dumps(WD_ESIK, ensure_ascii=False, indent=1), "```", "",
          "## SENTETİK (yapay pozitif / negatif; gerçek veri görülmeden)", "",
          "| kol | yakalama %0 | %10 | %20 | yanlış kabul en çok (%0) | en çok (her gürültü) | negatif tipleri (%0 kabul) | rastgele 1000 barda | hedef |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k in WD_KOLLAR:
        r = SJ["kol"][k]; ng = "; ".join(f"{t}: {_wd_f(v['0.0']['pay'], 0, True)}" for t, v in r["neg"].items())
        L.append(f"| {k} | {_wd_f(r['poz']['0.0']['pay'], 0, True)} | {_wd_f(r['poz']['0.1']['pay'], 0, True)} | {_wd_f(r['poz']['0.2']['pay'], 0, True)} | "
                 f"{_wd_f(r['kabul_0_en_cok'], 0, True)} | {_wd_f(r['kabul_hepsi_en_cok'], 0, True)} | {ng} | {_wd_f(SJ['rastgele_1000_bar'][k], 2)} | "
                 f"{'TUTTU' if r['hedef_tuttu'] else 'TUTMADI'} |")
    L += ["", "## GETİRİSİZ SAYIM (filtre + tekil sonrası olay; n / farklı ay / en kalabalık 3 ay payı)", "",
          "| kol | yön | ABD 2016-19 | ABD 2020-22 | AVR 2016-19 | AVR 2020-22 | 1000 barda ham (ABD / AVR) | rastgele seri 1000 barda |", "|---|---|---|---|---|---|---|---|"]
    for k in WD_KOLLAR:
        c = []
        for h in WD_HUCRE:
            x = S["hucre"][f"{k}|{h}"]; c.append(f"{x['n']} / {x['ay']} / {_wd_f(x['ust3_pay'], 0, True)}")
        L.append(f"| {k} | {'+' if WD_KOL[k]['yon'] == 1 else '-'} | " + " | ".join(c) +
                 f" | {_wd_f(S['siklik_1000'][f'ABD|{k}'], 2)} / {_wd_f(S['siklik_1000'][f'AVR|{k}'], 2)} | {_wd_f(SJ['rastgele_1000_bar'][k], 2)} |")
    L += ["", "### Filtre atmaları (ham aday -> atılan; sıra WD_ESIK filtre)", "", "| pazar | kol | ham aday | " + " | ".join(WD_ESIK["filtre"]["sira"]) + " |",
          "|---|---|---|" + "---|" * len(WD_ESIK["filtre"]["sira"])]
    for p in WD_PAZAR:
        for k in WD_KOLLAR:
            a = S["atma"][f"{p}|{k}"]
            L.append(f"| {p} | {k} | {S['aday'][f'{p}|{k}']} | " + " | ".join(str(a[x]) for x in WD_ESIK["filtre"]["sira"]) + " |")
    L += ["", "### Girişi gerçekleşmeyen adaylar (W3 / W4 / W5; tarama aşamasında, tarih / evren filtresinden önce)", ""]
    for p in WD_PAZAR:
        for k in ("W3", "W3T", "W4", "W4Y", "W5", "W5Y"):
            L.append(f"- {p} {k}: {json.dumps(S['girissiz'][f'{p}|{k}'], ensure_ascii=False)}")
    L += ["", "## Yorum noktaları (ölçümden ÖNCE sabit)", ""] + [f"{i + 1}. {s}" for i, s in enumerate(WD_YORUM)]
    L += ["", "## Hüküm (önceden; iş tanımı 3. bölüm)", "", f"- {WD_ESIK['hukum']['TUTAR']}", f"- TERS: {WD_ESIK['hukum']['TERS']}",
          f"- TEK DÖNEM: {WD_ESIK['hukum']['TEK_DONEM']}", f"- sıra: {WD_ESIK['hukum']['sira']}", "",
          "## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)", "", "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    import IZ_KARNE as IK
    for k in IK.IK_KONTROL:
        y, kn = WD_KONTROL[k["kod"]]
        L.append(f"| {k['kod']} | {k.get('ad', k.get('madde', ''))} | {y} | {kn} |")
    return MI._mi_yaz(_wd_yol("onkayit", cikti), "\n".join(L) + "\n", "WD_ON_KAYIT")


def wd_kapi(cikti: Optional[str] = None, ham: Optional[str] = None, yo_ham: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt kapısı: kontrol listesi + mühürler + commit + temiz ağaç + KASA; sonuç zaten varsa DUR."""
    import IZ_KARNE as IK
    import KASA as KS
    cikti = cikti or WD_YOL["cikti"]; yol = _wd_yol("onkayit", cikti)
    if os.path.exists(_wd_yol("sonuc", cikti)):
        raise WDHata("sonuç zaten var (ikinci koşu DURUR)")
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise WDHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    S = json.load(open(_wd_ham("sayim.json", ham), encoding="utf-8")); Sc = {a: v for a, v in S.items() if a != "info"}
    bek = {"WD_KOD_SHA": wd_kod_sha(), "WD_ESIK_SHA": wd_esik_sha(), **{f"DOSYA_{a}": v for a, v in wd_dosya_sha(ham, yo_ham).items()},
           "SAYIM_SHA": HV.hv_json_sha(Sc)}
    for a, v in bek.items():
        if f"{a}: {v}" not in metin:
            raise WDHata(f"ön kayıt kapısı: {a} farklı -> DURDU")
    rel = os.path.relpath(yol, KOK_WD); c = MI._mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise WDHata("ön kayıt commit'li değil -> DURDU")
    if MI._mi_git(["status", "--porcelain", "--", rel, "WEB_DESEN.py"]):
        raise WDHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    try:
        kasa = KS.kasa_kapisi([os.path.join(WD_YOL["acik"], f"V_{p}.pkl") for p in WD_PAZAR], "2022-12-31")
    except KS.KasaHata as ex:
        raise WDHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, "kasa": kasa, **bek}


def wd_sonuc_pazar(T: pd.DataFrame, P: Dict[str, np.ndarray], Xs: pd.DataFrame) -> pd.DataFrame:
    """Olay satırlarına sonuç + taban sütunları (getiri). Xs = YO örnek günleri (j, k, hucre)."""
    dep = {k: P[k] for k in ("O", "H", "L", "C", "POS", "off")}; ATR = wd_atr_dizi(dep)
    T = T.copy()
    R = wd_sonuc_olay(dep, T.j.to_numpy(), T.e.to_numpy(), T.giris.to_numpy(), T.stop.to_numpy(), T.yon.to_numpy(), T.atr.to_numpy())
    for a, v in R.items():
        T[a] = v
    B = wd_taban_gun(dep, ATR, Xs.j.to_numpy(), Xs.k.to_numpy())
    Xb = pd.DataFrame({"j": Xs.j.to_numpy(), "hucre": Xs.hucre.to_numpy(), "R15": B["R15"], "ATR_U": np.where(B["atr_ok"], B["ATR_U"], np.nan),
                       "ATR_D": np.where(B["atr_ok"], B["ATR_D"], np.nan), "Y10_U": B["Y10_U"], "Y10_D": B["Y10_D"]})
    gb = Xb.groupby(["j", "hucre"]).agg(T1=("R15", "mean"), AU=("ATR_U", "mean"), AD=("ATR_D", "mean"), YU=("Y10_U", "mean"), YD=("Y10_D", "mean"))
    M = gb.reindex(pd.MultiIndex.from_arrays([T.j.to_numpy(), T.hucre.to_numpy()])).to_numpy(float)
    yon = T.yon.to_numpy(np.int64)
    T["T1"] = M[:, 0]; T["ATR_TABAN"] = np.where(yon == 1, M[:, 1], M[:, 2]); T["Y10_TABAN"] = np.where(yon == 1, M[:, 3], M[:, 4])
    T["TF"] = yon * (T.R15 - T.T1)
    P15, _ = YO.yo_P15(P["Op"], P["Cl"], P["P2"])
    T["P15"] = P15[T.e_row.to_numpy(np.int64)]; T["SECIM"] = yon * (T.R15 - T.P15)
    r = (np.abs(T.giris - T.stop) / T.giris).to_numpy(float); out = np.full(len(T), np.nan)
    gi = pd.Series(np.arange(len(Xs))).groupby([Xs.j.to_numpy(), Xs.hucre.to_numpy()]).indices
    ge = pd.Series(np.arange(len(T))).groupby([T.j.to_numpy(), T.hucre.to_numpy()]).indices
    for key, ii in ge.items():
        dd = gi.get(key)
        if dd is None:
            continue
        out[ii] = wd_taban_2R(B["Hn"][dd], B["Ln"][dd], r[ii], yon[ii])
    T["R2_TABAN"] = out
    return T


def wd_olcum_hesap(SS: Dict[str, pd.DataFrame], B: Optional[int] = None) -> Dict[str, Any]:
    """Sonuç satırlarından kol x hücre ölçüleri + BH + hüküm (bellekte; kapı çağıranda)."""
    J: Dict[str, Any] = {"surum": WD_SURUM, "kol": {}}
    A = pd.concat(list(SS.values()), ignore_index=True)
    for kol in WD_KOLLAR:
        J["kol"][kol] = {"yon": WD_KOL[kol]["yon"], "hucre": {}}
        for h in WD_HUCRE:
            g = A[(A.kol == kol) & (A.hucre == h)]
            J["kol"][kol]["hucre"][h] = wd_hucre_olc(g, f"{kol}|{h}", B)
    p = []
    for kol in WD_KOLLAR:
        ps = []
        for d in ("d1619", "d2022"):
            o = J["kol"][kol]["hucre"][f"ABD|{d}"]
            ps += [o.get("TF", {}).get("p"), o.get("ATR", {}).get("p")]
        ps = [x for x in ps]
        p.append(max(ps) if all(x is not None for x in ps) else None)
    adj = HV._hv_bh(p, float(WD_ESIK["bh"]["q"]))
    for kol, pp, aa in zip(WD_KOLLAR, p, adj):
        bh = aa is not None and aa <= float(WD_ESIK["bh"]["q"])
        J["kol"][kol]["p"] = pp; J["kol"][kol]["bh_q"] = aa; J["kol"][kol]["bh_gecti"] = bool(bh)
        J["kol"][kol]["hukum"], J["kol"][kol]["not"] = wd_hukum(J["kol"][kol]["hucre"], bool(bh))
    return J


def wd_ozet_csv(J: Dict[str, Any], yol: str) -> str:
    R = []
    for kol, v in J["kol"].items():
        for h, o in v["hucre"].items():
            R.append({"kol": kol, "yon": v["yon"], "hucre": h, "n": o.get("n"), "ay": o.get("ay"), "ust3_pay": o.get("ust3_pay"),
                      "TF": o.get("TF", {}).get("ort"), "TF_alt": o.get("TF", {}).get("alt"), "TF_ust": o.get("TF", {}).get("ust"),
                      "SECIM": o.get("SECIM", {}).get("ort"), "ATR_pay": o.get("ATR", {}).get("pay"), "ATR_taban": o.get("ATR", {}).get("taban"),
                      "ATR_KAT": o.get("ATR", {}).get("kat"), "ATR_KAT_alt": o.get("ATR", {}).get("alt"), "ATR_KAT_ust": o.get("ATR", {}).get("ust"),
                      "R2_pay": o.get("R2", {}).get("pay"), "R2_taban": o.get("R2", {}).get("taban"), "RKAT": o.get("RKAT", {}).get("ort"),
                      "RKAT_medyan": o.get("RKAT", {}).get("medyan"), "Y10_pay": o.get("Y10", {}).get("pay"), "Y10_taban": o.get("Y10", {}).get("taban"),
                      "hukum": v["hukum"], "bh_q": v["bh_q"]})
    MI._mi_yaz(yol, pd.DataFrame(R).to_csv(index=False), "wd_ozet")
    return yol


def wd_olcum(cikti: Optional[str] = None, ham: Optional[str] = None, yo_ham: Optional[str] = None) -> Dict[str, Any]:
    """Kapı -> sonuç (bir kez) -> wd_sonuc.json + wd_ozet.csv; satır dosyaları ham klasörüne."""
    cikti = cikti or WD_YOL["cikti"]; G = wd_kapi(cikti, ham, yo_ham); t0 = time.time(); SS = {}
    for p in WD_PAZAR:
        T = pickle.load(open(_wd_ham(f"olay_{p}.pkl", ham), "rb")); P = wd_panel_yukle(p, yo_ham)
        Xs, _ = YO.yo_yukle(p, yo_ham or WD_YOL["yo_ham"]); Xs = Xs[["j", "k", "hucre"]]
        SS[p] = wd_sonuc_pazar(T, P, Xs)
        with open(_wd_ham(f"satir_{p}.pkl", ham), "wb") as f:
            pickle.dump(SS[p], f, protocol=4)
        del P
    J = wd_olcum_hesap(SS); J["kapi"] = G; J["sure_sn"] = round(time.time() - t0, 1); J["baslangic"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    MI._mi_jyaz(_wd_yol("sonuc", cikti), J, "wd_sonuc"); wd_ozet_csv(J, _wd_yol("ozet", cikti))
    return J


WD_BULKOWSKI = {"W1": "%82-84", "W1T": "%78-79", "W6": "%60", "W6T": "%59"}


def wd_rapor_yaz(cikti: Optional[str] = None, yeniden: Optional[List[str]] = None, hata: Optional[List[str]] = None,
                 sapma: Optional[List[str]] = None) -> str:
    cikti = cikti or WD_YOL["cikti"]; J = json.load(open(_wd_yol("sonuc", cikti), encoding="utf-8"))
    SJ = json.load(open(_wd_yol("sentetik", cikti), encoding="utf-8"))

    def hs(o: Dict[str, Any]) -> str:
        tf = o.get("TF", {})
        return f"{o.get('n', 0)}, {_wd_f(tf.get('ort'), 2, True)} [{_wd_f(tf.get('alt'), 2, True)}; {_wd_f(tf.get('ust'), 2, True)}]"

    def at(o: Dict[str, Any]) -> str:
        a = o.get("ATR", {})
        return f"{_wd_f(a.get('pay'), 1, True)} / {_wd_f(a.get('taban'), 1, True)} / {_wd_f(a.get('kat'), 2)} [{_wd_f(a.get('alt'), 2)}; {_wd_f(a.get('ust'), 2)}]"
    L = ["# WD_RAPOR — web desenleri: gerçek veride sonrası (15 bar; ABD + AVR 2016-2022)", "",
         "Birimler: TOPLAM FARK yüzde puan (yön düzeltmeli; aşağı desende işaret çevrildi), [ay kümeli bootstrap %95]. ATR hedefi = +2 ATR'ye -1 ATR'den önce "
         "ulaşma payı / aynı hissenin rastgele günlerindeki pay / KAT [aralık]. +2R = kaynağın stopuyla 2R'ye stoptan önce ulaşma payı / aynı R ile rastgele gün "
         "payı. Evren bugün yaşayan hisseler (yukarı yanlı: aşağı desenlerin aleyhine, yukarı desenlerin lehine).", "", "## SONUÇ", "",
         "| desen | yön | ABD 16-19: n, TF [aralık] | ABD 20-22: n, TF [aralık] | ATR 16-19 pay / taban / KAT | ATR 20-22 pay / taban / KAT | +2R pay / taban (16-19; 20-22) "
         "| ort R (16-19; 20-22) | 10 gün yön payı / taban (ABD 16-22) | AVR 16-19 / 20-22: n, TF | BH q | hüküm |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for kol in WD_KOLLAR:
        v = J["kol"][kol]; o = v["hucre"]; a1, a2 = o["ABD|d1619"], o["ABD|d2022"]; v1, v2 = o["AVR|d1619"], o["AVR|d2022"]
        r2 = f"{_wd_f(a1.get('R2', {}).get('pay'), 1, True)} / {_wd_f(a1.get('R2', {}).get('taban'), 1, True)}; " \
             f"{_wd_f(a2.get('R2', {}).get('pay'), 1, True)} / {_wd_f(a2.get('R2', {}).get('taban'), 1, True)}"
        rk = f"{_wd_f(a1.get('RKAT', {}).get('ort'), 2)}; {_wd_f(a2.get('RKAT', {}).get('ort'), 2)}"
        n1, n2 = a1.get("n", 0), a2.get("n", 0)
        y10 = (a1.get("Y10", {}).get("pay", np.nan) * n1 + a2.get("Y10", {}).get("pay", np.nan) * n2) / max(n1 + n2, 1) if n1 + n2 else None
        y10t = (a1.get("Y10", {}).get("taban", np.nan) * n1 + a2.get("Y10", {}).get("taban", np.nan) * n2) / max(n1 + n2, 1) if n1 + n2 else None
        avr = f"{v1.get('n', 0)}, {_wd_f(v1.get('TF', {}).get('ort'), 2, True)} / {v2.get('n', 0)}, {_wd_f(v2.get('TF', {}).get('ort'), 2, True)}"
        L.append(f"| {kol} {WD_KOL[kol]['ad']} | {'+' if v['yon'] == 1 else '-'} | {hs(a1)} | {hs(a2)} | {at(a1)} | {at(a2)} | {r2} | {rk} | "
                 f"{_wd_f(y10, 1, True)} / {_wd_f(y10t, 1, True)} | {avr} | {_wd_f(v['bh_q'], 3)} | **{v['hukum']}**{(' (' + '; '.join(v['not']) + ')') if v['not'] else ''} |")
    L += ["", "### Bulkowski oranları ile bizim 10 gün yön payımız (aynı ölçü DEĞİL: onunki kırılım yönü)", "", "| desen | Bulkowski | bizim 10 gün yön payı ABD 16-19 / 20-22 | taban |",
          "|---|---|---|---|"]
    for k, b in WD_BULKOWSKI.items():
        o = J["kol"][k]["hucre"]
        L.append(f"| {k} | {b} | {_wd_f(o['ABD|d1619'].get('Y10', {}).get('pay'), 1, True)} / {_wd_f(o['ABD|d2022'].get('Y10', {}).get('pay'), 1, True)} | "
                 f"{_wd_f(o['ABD|d1619'].get('Y10', {}).get('taban'), 1, True)} / {_wd_f(o['ABD|d2022'].get('Y10', {}).get('taban'), 1, True)} |")
    L += ["", "### Hücre ayrıntısı (n / farklı ay / en kalabalık 3 ay payı; SEÇİM; R katı medyanı)", "",
          "| desen | hücre | n | ay | üst3 | TF medyan | SEÇİM [aralık] | R katı [aralık] | R katı medyan |", "|---|---|---|---|---|---|---|---|---|"]
    for kol in WD_KOLLAR:
        for h, o in J["kol"][kol]["hucre"].items():
            s_, r_ = o.get("SECIM", {}), o.get("RKAT", {})
            L.append(f"| {kol} | {h} | {o.get('n')} | {o.get('ay')} | {_wd_f(o.get('ust3_pay'), 0, True)} | {_wd_f(o.get('TF', {}).get('medyan'), 2, True)} | "
                     f"{_wd_f(s_.get('ort'), 2, True)} [{_wd_f(s_.get('alt'), 2, True)}; {_wd_f(s_.get('ust'), 2, True)}] | {_wd_f(r_.get('ort'), 2)} "
                     f"[{_wd_f(r_.get('alt'), 2)}; {_wd_f(r_.get('ust'), 2)}] | {_wd_f(r_.get('medyan'), 2)} |")
    L += ["", "### Sentetik (yapay) dedektör sınaması", "", "| kol | yakalama (gürültü %0 / %10 / %20) | yanlış kabul en çok (%0) |", "|---|---|---|"]
    for k in WD_KOLLAR:
        r = SJ["kol"][k]
        L.append(f"| {k} | {_wd_f(r['poz']['0.0']['pay'], 0, True)} / {_wd_f(r['poz']['0.1']['pay'], 0, True)} / {_wd_f(r['poz']['0.2']['pay'], 0, True)} | "
                 f"{_wd_f(r['kabul_0_en_cok'], 0, True)} |")
    L += ["", "## KONTROL LİSTESİ", "", "Ön kayıttaki tablo (WD_ON_KAYIT.md) aynen geçerli; ölçüm kapısı geçti: "
          f"{J.get('kapi', {}).get('onkayit_commit', '—')}.", "", "## YENİDEN ÜRETİM", ""] + [f"- {x}" for x in (yeniden or ["—"])]
    L += ["", "## HATA", ""] + [f"- {x}" for x in (hata or ["—"])] + ["", "## SAPMA", ""] + [f"- {x}" for x in (sapma or ["—"])]
    L += ["", "## ÖNERİLEN DEFTER SATIRLARI", "", "(ana model işler; alt ajan deftere yazmaz)", ""]
    hk = {k: J["kol"][k]["hukum"] for k in WD_KOLLAR}
    L.append(f"- Ç (WEB_DESEN): web'de anlatılan 17 desen kolu (W1-W7) yapay örnekle sınandı, gerçek veride 15 bar ölçüldü; hükümler: "
             + ", ".join(f"{k} {v}" for k, v in hk.items()) + ". Evren bugün yaşayanlar.")
    return MI._mi_yaz(_wd_yol("rapor", cikti), "\n".join(L) + "\n", "WD_RAPOR")


# ================================================================ 9) ÇAKIŞMA KAPISI + KOMUT
def _cakisma_kontrol_wd(_once=_CK_ONCE_WD, _dosya="WEB_DESEN.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_WD",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_wd()


def _wd_ana(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print(__doc__); return 0
    k = argv[0]
    try:
        if k == "sentetik":
            J = wd_sentetik(); print(json.dumps({a: {"yakalama": v["yakalama_0"], "kabul": v["kabul_0_en_cok"]} for a, v in J["kol"].items()}, ensure_ascii=False))
        elif k == "yapay_pdf":
            print(wd_yapay_pdf())
        elif k == "olay":
            S = wd_olay(); print(json.dumps({a: v["n"] for a, v in S["hucre"].items()}, ensure_ascii=False))
        elif k == "onkayit":
            print(wd_onkayit_yaz())
        elif k == "olcum":
            J = wd_olcum(); print(json.dumps({a: v["hukum"] for a, v in J["kol"].items()}, ensure_ascii=False))
        elif k == "rapor":
            print(wd_rapor_yaz())
        elif k == "gercek_pdf":
            print(wd_gercek_pdf())
        elif k == "sha":
            print(json.dumps({"kod": wd_kod_sha(), "esik": wd_esik_sha()}))
        else:
            print(__doc__); return 2
    except (WDHata, YO.YOHata, MI.MIHata) as ex:
        wdlog.error("DURDU: %s", ex); return 1
    return 0


if __name__ == "__main__":
    sys.exit(_wd_ana())
