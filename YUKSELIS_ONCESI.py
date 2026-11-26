"""YUKSELIS_ONCESI — 'yükseliş trendinden önce hangi bölge var': yükselişten geriye bakış (yalnız KEŞİF: ABD 2016-19), sonra keşifte belirlenen yön ve
kesimlerle ileriye doğru sınama (ABD 2020-22, AVR 2016-19 / 2020-22); hisse düzeyi + piyasa düzeyi; oynaklık tuzağına karşı ATRP beşliği içinde okuma (26 Kasım 2026).

İş tanımı: arastirma_cikti/yukselis_oncesi/YO_IS_TANIMI.md (ana model). Birim: hisse-gün t (hissenin kendi geçerli barları; her 5 barda bir). Giriş = t + 1
barının açılışı; ufuk 15 geçerli bar. Y10 = +%10'a, girişin %5 altına inmeden; Y5 = +%5'e, %5 altına inmeden; D10 (ayna) = -%10'a, %5 üstüne çıkmadan;
aynı barda iki sınır = STOP ÖNCE (kötümser; MUM_IZI_GOZ.gz_olc_bir mantığı). Evren = TEZGÂH 2 P2 havuzu (KART_TUR2.k2_panel; giriş günü P2 üyeliği).
Veri / geçerli bar = MUM_IZI.mi_veri (MUM_IZI_HAVUZ / MUM_IZI_GOZ ile aynı açık kopya). HACİM KULLANILMAZ (yalnız P2 likidite süzgeci kadar).
Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ. Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır.

Komut:  python YUKSELIS_ONCESI.py hazirla   ABD + AVR özellik panelleri (getirisiz) -> /root/.kasa/ham/yukselis_oncesi
        python YUKSELIS_ONCESI.py sayim     GETİRİSİZ SAYIM (sayim.json; Y / R15 hesaplanmaz)
        python YUKSELIS_ONCESI.py onkayit   YO_ON_KAYIT.md (mühürler + sayım + yorum noktaları + kontrol tablosu)
        python YUKSELIS_ONCESI.py adim1     kapı -> YALNIZ ABD 2016-19 sonuçları -> yo_kesim.json + YO_KESIM.md
        python YUKSELIS_ONCESI.py adim2     kapı + kesim kapısı -> doğrulama (bir kez) -> yo_sonuc.json + yo_ozet.csv
        python YUKSELIS_ONCESI.py rapor     YO_RAPOR.md + YO_OZET.png (sonuç json'undan)
        python YUKSELIS_ONCESI.py sha       kod / eşik sha
Colab:  exec(open('YUKSELIS_ONCESI.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı; iki taraf için de).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_YO = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_YO = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_YO not in sys.path:
    sys.path.insert(0, KOK_YO)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; veri, yazma, git)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ; açık kopya yolu)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; kesik kapısı, dönem ataması, ay özeti, BH, json sha)

yolog = logging.getLogger("col.yukselis_oncesi")
if not yolog.handlers:
    _yo_h = logging.StreamHandler(sys.stderr)
    _yo_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s yukselis_oncesi: %(message)s", "%H:%M:%S"))
    yolog.addHandler(_yo_h)
    yolog.setLevel(logging.INFO)
    yolog.propagate = False


class YOHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / sıra / yeniden üretim uyuşmazlığı."""


YO_SURUM = "YUKSELIS_ONCESI v1.0 (2026-11-26): yükselişten geriye bakış + ileriye doğru sınama (ATRP beşliği içinde)"
YO_YOL = {"cikti": os.path.join(KOK_YO, "arastirma_cikti", "yukselis_oncesi"), "kod": os.path.join(KOK_YO, "YUKSELIS_ONCESI.py"),
          "ham": os.environ.get("YO_HAM", "/root/.kasa/ham/yukselis_oncesi"), "acik": MV.MV_YOL["gunluk"],
          "is_tanimi": os.path.join(KOK_YO, "arastirma_cikti", "yukselis_oncesi", "YO_IS_TANIMI.md")}
YO_DOSYA = {"onkayit": "YO_ON_KAYIT.md", "kesim_md": "YO_KESIM.md", "kesim": "yo_kesim.json", "sonuc": "yo_sonuc.json", "ozet": "yo_ozet.csv",
            "rapor": "YO_RAPOR.md", "png": "YO_OZET.png"}
YO_KESIK = pd.Timestamp("2022-12-31")
YO_PAZAR = ("ABD", "AVR")
YO_HUCRE = ("ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022")
YO_KESIF = "ABD|d1619"

# özellik listeleri (sıra sabit)
YO_YENI = ["MIKRO", "RS_UZAK", "RS_DIP_BIR", "GEN50", "GEN50_D10", "OYN_SIRA", "MA_KOD", "MA_EGIM_DEG", "ZIRVE_BAR", "ZIRVE_DUSUS", "DIP_BAR",
           "DIP_HIZ", "CLV10", "CLV_FARK", "YUKSELEN_DIP"]
YO_KONTROL_OZ = ["MOM_12_1", "F15", "KONUM120", "ATRP20", "BOY_YUZDE_ORAN", "ONCEKI_DUSUS"]
YO_OZ = YO_YENI + YO_KONTROL_OZ
YO_AILE = {"MIKRO": "MIKRO", "RS_UZAK": "RS_DIP", "RS_DIP_BIR": "RS_DIP", "GEN50": "GENISLIK", "GEN50_D10": "GENISLIK", "OYN_SIRA": "OYN_SIRA",
           "MA_KOD": "MA_DIZI", "MA_EGIM_DEG": "MA_DIZI", "ZIRVE_BAR": "DD_SURE", "ZIRVE_DUSUS": "DD_SURE", "DIP_BAR": "DD_SURE", "DIP_HIZ": "DD_SURE",
           "CLV10": "CLV", "CLV_FARK": "CLV", "YUKSELEN_DIP": "YUKSELEN_DIP", "MOM_12_1": "KONTROL", "F15": "KONTROL", "KONUM120": "KONTROL",
           "ATRP20": "KONTROL", "BOY_YUZDE_ORAN": "KONTROL", "ONCEKI_DUSUS": "KONTROL"}
YO_BAYRAK = {"RS_DIP_BIR": (0.0, 1.0), "MA_KOD": (0.0, 3.0)}         # uç = yönün işaret ettiği uç kategori (tek satır 'BAYRAK')
YO_PIYASA_OZ = ["GEN20", "GEN50", "GEN200", "GEN20_D5", "GEN20_D10", "GEN50_D5", "GEN50_D10", "GEN200_D5", "GEN200_D10", "PAZ_R20", "PAZ_R60",
                "PAZ_DD60", "DIP20_PAY", "YENI_ZD", "KESIT_SD", "ATRP_MED_SIRA"]

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
YO_ESIK: Dict[str, Any] = {
    "surum": "YO-1.0",
    "tohum": 28,
    "tohum_tanim": "np.random.default_rng([28, crc32(anahtar)]); eşleşme anahtarı 'esle', bootstrap anahtarı satır adı; sıra bağımsız, tekrarlanabilir",
    "veri": "MUM_IZI.mi_veri(pazar, MUM_IZI_V2.MV_YOL['gunluk']) (OS.os_veri: geçerli bar O/H/L/C > 0 sonlu, H > L, V > 0; ABD evren dışı fon listesi; DS "
            "açılış kırpması); ABD, AVR; BIST hesaplanmaz (P2 tanımsız; iş tanımında bilgi)",
    "evren": "TEZGÂH 2 P2 havuzu: KART_TUR2.k2_panel(Vd, pazar) -> P2[d, j] (d = birleşik takvim satırı; d - 1'e kadarki bilgi); hisse-gün t örneklemde <=> "
             "giriş barı t + 1'in satırında P2",
    "ornek": {"adim": 5, "tanim": "hissenin kendi geçerli bar indeksi k (0'dan) k % 5 == 0; giriş barı k + 1 ile k arasında <= 10 birleşik takvim satırı (OS "
                                   "giriş azami boşluğu); k + 15 hissenin verisinde ve k + 1 .. k + 15 barları <= 30 birleşik takvim satırında (2H kuralı); "
                                   "giriş tarihi 2016-01-01 .. 2022-12-31; 15. bar <= 2022-12-31",
              "giris_bosluk": 10, "pencere_satir": 30},
    "hucre": {"tanim": "giriş tarihine göre MUM_IZI_HAVUZ.hv_hucre_ad (d1619 = 2016-19, d2022 = 2020-22)", "kesif": "ABD|d1619",
              "dogrulama": "ABD|d2022", "avr": ["AVR|d1619", "AVR|d2022"]},
    "yukselis": {"ufuk": 15, "Y10": [0.10, 0.05], "Y5": [0.05, 0.05], "D10": [0.10, 0.05],
                 "tanim": "giriş E0 = t + 1 barının açılışı; barlar t + 1 .. t + 15 (giriş barı dahil, GZ gibi); Y10: ilk High >= E0 x 1,10 barı, ilk Low <= "
                          "E0 x 0,95 barından ÖNCE; Y5 aynı (+%5 / -%5); D10 (ayna): ilk Low <= E0 x 0,90 barı, ilk High >= E0 x 1,05 barından ÖNCE; aynı "
                          "barda iki sınır = STOP ÖNCE (Y10 / Y5 / D10 = 0; kötümser, iki yönde aynı); R15 = t + 15 kapanışı / E0 - 1; KALICI (bilgi) = 30 "
                          "barda +%20, -%8'den önce (aynı kural; k + 30 yoksa ya da > 60 satır ise NaN)",
                 "KALICI": [0.20, 0.08, 30]},
    "piyasa": {"en_az_hisse": 5, "esik_YP": 0.05, "esik_DP": -0.05, "kume_en_az": 30,
               "P15": "P15(d) = d satırında P2 ve açılışı sonlu > 0 olan bütün hisselerin [d, d + 14] satırlarındaki son geçerli kapanış / açılış(d) - 1 "
                      "eşit ağırlıklı ortalaması (hv25_piyasa_R mantığı; olay dışlaması yok); < 5 hisse ise yok; hisse-gün için d = giriş barının satırı",
               "endeks": "pazar endeksi L: r(t) = P2[t] hisselerinin Cl[t] / Cf[t - 1] - 1 ortalaması (Cf = kapanış 5 satıra kadar ileri taşınmış; < 5 hisse "
                         "ise r = 0); L = birikimli çarpım",
               "gun": "piyasa birimi pazar-gün t (her satır; örtüşmeli), giriş satırı d = t + 1, dönem d tarihine göre; d + 14 veri içinde; özellikler t "
                      "satırına kadar; kesit kümesi A_t = P2[t] ve değer sonlu, >= 30 hisse"},
    "ozellik": {
        "MIKRO": "son 60 barda (u_i = C_i > C_{i-1}, i = k-59..k; k >= 60) art arda en az 3 yükselen kapanış serisi sayısı (pencere başında kesilen seri "
                 "pencere içi uzunluğuyla)",
        "RS_UZAK": "RS = C_k / L(satır_k); RS_k / maks(RS_{k-59..k}) - 1 (<= 0)",
        "RS_DIP_BIR": "bayrak: KONUM120 < 0,5 VE RS_UZAK >= -0,03 ('fiyat alt yarıda, göreli güç zirveye %3 içinde'); RS_DIP ailesinin konum sütunu "
                      "KONUM120 ile aynı tanım olduğu için ayrı satır yazılmaz (kontrolde)",
        "GEN50": "pazarda SMA50 üstündeki hisse payı (t satırı; A_t kümesi; her hisseye aynı gün aynı değer)", "GEN50_D10": "GEN50(t) - GEN50(t - 10 satır)",
        "OYN_SIRA": "OYN60 = son 60 günlük log getirinin std'si (ddof 1, kendi barları); t satırında A_t kümesindeki yüzdelik sırası ((küçük + 0,5 eşit) / n)",
        "MA_KOD": "sıralama kodu (SMA20 > SMA50) + (SMA50 > SMA200) + (SMA20 > SMA200) ∈ {0,1,2,3} (3 = tam yukarı dizi, 0 = tam aşağı); kendi kapanışları",
        "MA_EGIM_DEG": "SMA20 eğimi e_k = SMA20_k / SMA20_{k-10} - 1; değişim = e_k - e_{k-10}",
        "ZIRVE_BAR": "son 250 barın en yüksek kapanışından (son kez görüldüğü bar) bu yana bar sayısı", "ZIRVE_DUSUS": "C_k / maks250 - 1",
        "DIP_BAR": "zirveden k'ye en düşük kapanışın (son kez) barından bu yana bar sayısı", "DIP_HIZ": "(C_k / C_dip - 1) / maks(DIP_BAR, 1) x 100 (% / bar)",
        "CLV10": "son 10 barda (C - L) / (H - L) ortalaması", "CLV_FARK": "CLV10 - önceki 30 barın (k-39 .. k-10) ortalaması",
        "YUKSELEN_DIP": "yerel dip i: L_i < L_{i-1}, L_i < L_{i-2}, L_i <= L_{i+1}, L_i <= L_{i+2} (i + 2 <= k); pencere i ∈ [k-57, k-2]; son dipten geriye art "
                        "arda yükselen dip sayısı (eşit kırar; pencere içiyle sınırlı)",
        "MOM_12_1": "C_{k-21} / C_{k-252} - 1 (OLCU_SINAMA kart MOM tanımı; kendi barları)", "F15": "C_k / C_{k-15} - 1 (iş tanımı: 15 barlık geçmiş getiri)",
        "KONUM120": "OLCU_SINAMA._os_atrp_f15 'f15' (son 120 kapanışın aralığında konum; repoda adı F15, burada KONUM120)",
        "ATRP20": "son 20 barın TR (önceki kapanışla; ilk bar H - L) ortalaması / C_k (UC_IZ2.uc2_ret_atrp formülü)",
        "BOY_YUZDE_ORAN": "EK 27 ölçü 1 (iş tanımı metninden): (H - L) / C medyanı son 16 bar / önceki 120 bar (k-135 .. k-16) medyanı",
        "ONCEKI_DUSUS": "EK 27 ölçü 12 (iş tanımı metninden): min L_{k-15..k} / maks H_{k-75..k-16} - 1 (pencere 16 bar, önceki 60 bar)"},
    "piyasa_ozellik": {
        "GEN20/GEN50/GEN200": "A_t kümesinde C > SMA(n) (kendi barları) payı", "_D5/_D10": "düzey(t) - düzey(t - 5 / 10 satır)",
        "PAZ_R20/PAZ_R60": "L(t) / L(t - 20 / 60) - 1", "PAZ_DD60": "L(t) / maks L(t-59 .. t) - 1",
        "DIP20_PAY": "A_t'de C_k <= min C_{k-19..k} payı (20 günlük dipte)", "YENI_ZD": "60 günlük kapanış zirvesinde olan pay - 60 günlük dipte olan pay",
        "KESIT_SD": "A_t'de C_k / C_{k-20} - 1 kesit std'si (ddof 1)",
        "ATRP_MED_SIRA": "A_t'de ATRP20 medyanı; bu medyanın önceki 250 satırdaki (t dahil, >= 60 değer) kendi geçmişinde yüzdelik sırası"},
    "adim1": {"es": 5, "tanim": "KEŞİF (ABD 2016-19) Y10 = 1 hisse-günleri; kontroller aynı t tarihi, aynı ATRP20 beşliği (keşif beşlik sınırları), Y10 = 0; olay "
                                "başına 5 (yerine koymadan; < 5 ise hepsi; 0 ise olay düşer); gruplar (tarih, beşlik) sırasıyla, olaylar sembol sırasıyla; tohum 28",
              "smd": "(ort_olay - ort_kontrol) / sqrt((var_olay + var_kontrol) / 2) (kontroller satır olarak); özelliği sonlu olay ve en az bir sonlu kontrolü olan olaylar",
              "auc": "eşli AUC = olay başına kendi kontrollerine göre [1(x_o > x_k) + 0,5 1(=)] ortalaması, olaylar üzerinden ortalama",
              "yon": "SMD > 0 -> BÜYÜK, < 0 -> KÜÇÜK (= 0 ya da yok -> BÜYÜK, not)",
              "piyasa": "ABD keşif günleri: YP = 1 günleri ile öteki günler (eşsiz) SMD ve AUC (Mann-Whitney); yön aynı kural"},
    "kesim": {"uc": [0.10, 0.02], "besli": [0.2, 0.4, 0.6, 0.8],
              "tanim": "BÜYÜK yönde uç = değer >= keşif dağılımının %90 (%98) yüzdeliği; KÜÇÜK yönde <= %10 (%2) (eşitler dahil; gerçek pay yazılır); bayraklar "
                       "(RS_DIP_BIR, MA_KOD) tek satır: yönün uç kategorisi; ATRP20 beşlik sınırları keşif dağılımının %20/40/60/80'i; ABD 2020-22 KEŞİFİN "
                       "sayısal kesimleriyle; AVR hücreleri aynı yüzdelik DÜZEYLERİNİN AVR 2016-19 ÖZELLİK dağılımındaki (getirisiz) değerleriyle (ATRP "
                       "beşlik sınırları dahil); piyasa özellikleri aynı kural (pazar-gün dağılımı)",
              "nump": "np.quantile (doğrusal)"},
    "olcu": {"populasyon": "hücrede özelliği sonlu VE ATRP20 sonlu hisse-günler (taban da bu küme)",
             "KAT_HAM": "P(Y10 | uç) / P(Y10) (hücre)",
             "KAT": "ATRP içi: sum(Y10 uçta) / sum(p_q(i)) uçta, p_q = hücrede ATRP beşliği q'nun P(Y10)'u (= beşliklerin olay ağırlıklı ortalama oranı)",
             "ASIMETRI": "[P(Y10) - P(D10)] uçta - sum_q (n_uq / n_u) [P(Y10 | q) - P(D10 | q)]",
             "TOPLAM_FARK": "R15 - aynı hissenin aynı hücredeki bütün örnek günlerinin R15 ortalaması (uç satırların ortalaması)",
             "SECIM": "R15 - P15(d) (bilgi)", "KAT_PUAN": "KAT ile aynı, ATRP beşliği yerine KONTROL PUANI beşliği (kontrolü geçme)",
             "bilgi": "Y5 KAT, KALICI payı, medyan R15"},
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)", "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık); oranlar / KAT her tekrarda "
                                                                 "ağırlıklı toplamlardan; %95 = 2,5 / 97,5 yüzdelik; TOPLAM FARK'ta hisse ortalaması sabit",
             "p": "tek yönlü p = (1 + #(KAT* <= 1)) / (B + 1) (doğrulama ABD 2020-22)"},
    "bh": {"q": 0.10, "aile": "hisse satırları: 21 sütun x 2 uç (bayraklar tek) = 40 satır; p = ABD 2020-22 KAT p'si; piyasa satırları ayrı aile (16 x 2)"},
    "hukum": {"n_min": 1000, "ay_min": 12,
              "TUTAR": "KEŞİF ve ABD 2020-22'de: n >= 1000 VE farklı ay >= 12 VE KAT > 1 ve alt > 1 VE ASİMETRİ > 0 ve alt > 0 VE TOPLAM FARK > 0 ve alt > 0; "
                       "VE BH (q 0,10) geçer VE AVR 2016-19 ve 2020-22'nin İKİSİNDE (KAT - 1), ASİMETRİ, TOPLAM FARK nokta değerleri > 0 (AVR hücresinde n >= 30)",
              "sira": "ÖLÇÜLEMEDİ (keşif ya da ABD 2020-22 n < 1000 ya da ay < 12) > TUTAR > YALNIZ OYNAKLIK > TEK DÖNEM > TERS > TUTMADI",
              "YALNIZ_OYNAKLIK": "KAT_HAM alt > 1 keşifte ve ABD 2020-22'de, ama ikisinden birinde KAT alt <= 1 ya da ASİMETRİ <= 0",
              "TEK_DONEM": "üç şart (KAT, ASİMETRİ, TOPLAM FARK alt uçları) keşif ve ABD 2020-22'den yalnız birinde (= ileriye doğru 'tutmadı' sayılır)",
              "TERS": "ABD 2020-22'de KAT üst < 1 VE ASİMETRİ üst < 0", "TUTMADI": "ötekiler (iki dönemde geçip BH / AVR'de kalan dahil)",
              "KONTROL": "TUTAR satırı ABD 2020-22'de KAT_PUAN > 1 ve alt > 1 -> KONTROLÜ GEÇER; değilse 'BİLİNENİN TEKRARI'",
              "piyasa": "aynı kalıp: keşif ve ABD 2020-22'de n >= 30 gün VE ay >= 12 VE KAT = P(YP | uç) / P(YP) > 1 ve alt > 1 VE ASİMETRİ = [P(YP) - P(DP)] "
                        "uç - taban > 0 ve alt > 0 VE P15 farkı (uç - bütün günler) > 0 ve alt > 0 VE AVR iki dönemde üç nokta işareti > 0; BH ayrı aile",
              "GENEL": "en az bir hisse satırı TUTAR ve KONTROLÜ GEÇER ise 'AÇIK VERİDE ADAY (kasa açılmaz; KASA KURALI: tek iz kasa açmaz; ileri test)'; aksi "
                       "'YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde)'"},
    "birlesim": {"en_cok": 2, "tanim": "aday = tek başına KEŞİF uç %10 (bayrakta bayrak) satırı n >= 1000, ay >= 12, KAT alt > 1, ASİMETRİ alt > 0, TOPLAM FARK alt > "
                                       "0 olan sütunlar; >= 2 aday varsa farklı iki sütunun uçlarının kesişimi (n >= 1000) içinden keşif KAT'ı en büyük çift; doğrulamada "
                                       "bir kez; < 2 aday ise birleşim kurulmaz"},
    "puan": {"L1_lambda": 0.001, "iter": 400,
             "tanim": "keşifte L1 lojistik Y10 ~ 21 hisse özelliği (keşif ort / std ile standart; eksik = 0), ortalama log kaybı + lambda |w|_1 (sabit kesişim "
                      "cezasız), FISTA 400 adım; puan uç %10 / %2 = keşif puan dağılımının %90 / %98'i (AVR: AVR 2016-19 puan dağılımı); doğrulamada bir kez; "
                      "'karmaşık olan en iyi tek özelliği geçmiyorsa seçilmez' = ABD 2020-22 KAT'ı en iyi tek satırın ABD 2020-22 KAT'ından büyük VE TUTAR",
             "kontrol_model": "keşifte lojistik (Newton) Y10 ~ MOM_12_1 + F15 + KONUM120 + ATRP20 (standart, eksik = 0); KONTROL PUANI beşlik sınırları keşiften"},
    "kesik": "veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her pazar) + KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl, '2022-12-31')",
    "sira": "kod + sentetik test -> getirisiz sayım -> ön kayıt commit + push -> ik_kontrol_kapisi -> ADIM 1 (yalnız ABD 2016-19 sonuçları) -> yo_kesim.json + "
            "YO_KESIM.md commit + push -> ADIM 2 (bir kez) -> rapor",
}

YO_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "taban aynı hücre (pazar x dönem) aynı evren; ATRP içi KAT ve ASİMETRİ aynı ATRP beşliğiyle (oynaklığın mekanik etkisi dışlanır); ADIM 1 kontrolleri "
                   "aynı gün aynı ATRP beşliği; TOPLAM FARK aynı hissenin aynı dönem ortalamasına göre; kontrol özellikleri (MOM_12_1, F15, KONUM120, ATRP20, EK 27 "
                   "ölçüleri) ve kontrol puanı beşliği içinde KAT (bilinenin tekrarı denetimi); D10 aynası mekanik üstünlüğü ölçer"),
    "K2": ("EVET", "her özellik k barına kadarki barlardan (test: k + 1 ve sonrası bozulunca değerler aynı); piyasa özellikleri t satırına kadar; P2 d - 1'e kadar; "
                   "giriş k + 1 açılışı; Y / R15 ayrı fonksiyonda ve ADIM 1'de yalnız ABD 2016-19 (assert); kesimler yalnız keşiften (assert); veri <= 2022-12-31 "
                   "assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0, O/H/L/C sonlu > 0); bütün ölçüler hissenin kendi geçerli barlarında; 15 bar <= 30 takvim satırı; P2 "
                   "bölünme / likidite alt %20 / fiyat-likidite alt sınırı dışı"),
    "K4": ("EVET", "hisse başına her 5 barda bir t (örtüşme azaltılır, kalkmaz); çıkarım ay kümeli bootstrap (günler bağımsız sayılmaz); n hisse-gün ve farklı ay "
                   "ayrı yazılır; medyan R15 bilgi"),
    "K5": ("EVET", "giriş = t + 1 barının açılışı (t kapanışı değil); P15 de d = t + 1 açılışından"),
    "K6": ("EVET", "OS / MI bölünme düzeltmeli açık kopya; getiriler oransal, yerel para; pazar içi karşılaştırma; P2 bölünme şüphesi günlerini dışlar"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı, iki taraf (Y10 ve D10) için de; raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n >= 1.000 ve farklı ay >= 12 olmayan satır ÖLÇÜLEMEDİ; iki dönem + iki pazar; BH q 0,10 (40 satır aile); en kalabalık 3 ay payı her satırda"),
    "K9": ("EVET", "YO_ON_KAYIT.md: YO_KOD_SHA, YO_ESIK_SHA, panel dosya sha'ları, SAYIM_SHA + getirisiz sayım + yorum noktaları; ADIM 1 ön kayıt commit + push'tan "
                   "sonra (kapı: kontrol + sha + commit + temiz ağaç); ADIM 2 yo_kesim.json commit'inden sonra (kapı); ikinci koşu durur"),
    "K10": ("EVET", "panel şeması (sütunlar) ve satır sayıları ön kayıttakiyle aynı (sayım sha); özellik tanımları sentetik elle hesaplanmış örneklerle; dokunma "
                    "mantığı MUM_IZI_GOZ.gz_olc_bir ile rastgele sentetik serilerde birebir"),
    "K11": ("EVET", "keşif satırları ADIM 1 ve ADIM 2'de aynı kodla (eşit olmalı, DUR); rapordan önce >= 3 satır panel dosyalarından bağımsız kısa kodla yeniden üretilir"),
    "K12": ("EVET", "'iz / aday' sözü yalnız hüküm kuralıyla; oynaklıkla açıklanan satır 'YALNIZ OYNAKLIK'; keşifte iyi doğrulamada değil -> 'TEK DÖNEM (tutmadı)'; "
                    "sayı ile yorum ayrı cümlede; evren bugün yaşayanlar"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_yo); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı "
                    "taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _yo_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or YO_YOL["cikti"], YO_DOSYA[ad])


def _yo_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or YO_YOL["ham"], ad)


def yo_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or YO_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def yo_kod_sha() -> str:
    return MI._mi_sha(YO_YOL["kod"])


def _yo_rng(anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(YO_ESIK["tohum"]), zlib.crc32(str(anahtar).encode("utf-8"))])


def _yo_git(args: List[str]) -> str:
    return MI._mi_git(args)


def yo_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri") -> pd.Timestamp:
    """Kasa kapısı (mekanik): HV.hv_kesik_kapi aynen (kesik 2022-12-31)."""
    try:
        return HV.hv_kesik_kapi(V, ad, YO_KESIK)
    except HV.HVHata as ex:
        raise YOHata(str(ex)) from ex


def yo_hucre(giris: Any, pazar: str) -> str:
    return HV.hv_hucre_ad(giris, pazar)


# ================================================================ 1) SONUÇ ÇEKİRDEĞİ (dokunma; getiri) — yalnız yo_sonuc üzerinden çağrılır
def yo_ilk_dokunma(E0: np.ndarray, Hs: np.ndarray, Ls: np.ndarray, hedef: float, stop: float, yon: str = "yukari") -> np.ndarray:
    """'Önce hangisine dokundu' (vektör). Hs / Ls: (N x U) barlar (geçersiz hücre NaN). yukari: hedef = High >= E0 (1 + hedef), stop = Low <= E0 (1 - stop);
    asagi (ayna): hedef = Low <= E0 (1 - hedef), stop = High >= E0 (1 + stop). Sonuç 1 <=> hedef barı stop barından ÖNCE (aynı bar = stop önce -> 0)."""
    E0 = np.asarray(E0, float)[:, None]
    with np.errstate(invalid="ignore"):
        if yon == "yukari":
            hit = Hs >= E0 * (1 + hedef); stp = Ls <= E0 * (1 - stop)
        elif yon == "asagi":
            hit = Ls <= E0 * (1 - hedef); stp = Hs >= E0 * (1 + stop)
        else:
            raise YOHata(f"yön: {yon}")
    BIG = 10 ** 9
    kh = np.where(hit.any(1), hit.argmax(1), BIG); ks = np.where(stp.any(1), stp.argmax(1), BIG)
    return ((kh < BIG) & (kh < ks)).astype(float)


def yo_sonuc_dizi(dep: Dict[str, np.ndarray], j: np.ndarray, k: np.ndarray) -> Dict[str, np.ndarray]:
    """Örnek satırları (hisse j, kendi bar k = t): E0, Y10, Y5, D10, R15, KALICI. Örnekleme uygunluğu çağıranda (k + 15 var)."""
    Y = YO_ESIK["yukselis"]; U = int(Y["ufuk"]); j = np.asarray(j, np.int64); k = np.asarray(k, np.int64); N = len(j)
    out = {a: np.full(N, np.nan) for a in ("E0", "Y10", "Y5", "D10", "R15", "KALICI")}
    if not N:
        return out
    g = dep["off"][j] + k; son = dep["off"][j + 1] - 1
    if (g + U > son).any():
        raise YOHata("K10: sonuç penceresi hissenin verisini aşıyor (örnekleme kuralı bozuk)")
    W = g[:, None] + 1 + np.arange(U)[None, :]
    E0 = dep["O"][g + 1]; Hs = dep["H"][W]; Ls = dep["L"][W]
    out["E0"] = E0; out["R15"] = dep["C"][g + U] / E0 - 1
    out["Y10"] = yo_ilk_dokunma(E0, Hs, Ls, Y["Y10"][0], Y["Y10"][1], "yukari")
    out["Y5"] = yo_ilk_dokunma(E0, Hs, Ls, Y["Y5"][0], Y["Y5"][1], "yukari")
    out["D10"] = yo_ilk_dokunma(E0, Hs, Ls, Y["D10"][0], Y["D10"][1], "asagi")
    h, s, U2 = Y["KALICI"]; U2 = int(U2)
    ok = (g + U2 <= son)
    if ok.any():
        gg = g[ok]; W2 = gg[:, None] + 1 + np.arange(U2)[None, :]
        span = dep["POS"][gg + U2] - dep["POS"][gg + 1]
        kal = yo_ilk_dokunma(dep["O"][gg + 1], dep["H"][W2], dep["L"][W2], h, s, "yukari")
        kal[span > 2 * int(YO_ESIK["ornek"]["pencere_satir"]) - 1] = np.nan
        out["KALICI"][ok] = kal
    return out


def yo_P15(Op: np.ndarray, Cl: np.ndarray, P2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """P15(d) bütün satırlar için (hv25_piyasa_R mantığı, kovasız; küme P2[d] ve açılış sonlu > 0)."""
    n, u = Op.shape; U = int(YO_ESIK["yukselis"]["ufuk"]); out = np.full(n, np.nan); say = np.zeros(n, np.int64)
    mn = int(YO_ESIK["piyasa"]["en_az_hisse"])
    for d in range(n - U + 1):
        with np.errstate(invalid="ignore"):
            jj = np.flatnonzero(P2[d] & np.isfinite(Op[d]) & (Op[d] > 0))
        if not len(jj):
            continue
        c = Cl[d:d + U, jj]; okc = np.isfinite(c)
        sonk = np.where(okc.any(0), U - 1 - np.argmax(okc[::-1], axis=0), -1)
        R = np.where(sonk >= 0, c[np.maximum(sonk, 0), np.arange(len(jj))] / Op[d, jj] - 1, np.nan); R = R[np.isfinite(R)]
        say[d] = len(R)
        if len(R) >= mn:
            out[d] = float(R.mean())
    return out, say


# ================================================================ 2) ÖZELLİKLER (yalnız k'ye kadarki barlar)
def _sw(x: np.ndarray, w: int) -> np.ndarray:
    return np.lib.stride_tricks.sliding_window_view(x, w)


def _yo_roll(x: np.ndarray, w: int, f: str) -> np.ndarray:
    s = pd.Series(x).rolling(w, min_periods=w)
    return getattr(s, f)().to_numpy(float)


def yo_hisse_ozellik(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, Lp: np.ndarray) -> Dict[str, np.ndarray]:
    """Bir hissenin kendi geçerli barlarında özellikler (k barındaki değer yalnız 0..k barlarından). Lp = pazar endeksi L'nin bar satırlarındaki değeri.
    Ayrıca piyasa özellikleri için bayraklar (_u20, _u50, _u200, _d20, _z60, _d60, _r20, _oyn60)."""
    import OLCU_SINAMA as OS
    O, H, L, C, Lp = (np.asarray(a, float) for a in (O, H, L, C, Lp)); m = len(C); out: Dict[str, np.ndarray] = {}
    nanv = lambda: np.full(m, np.nan)  # noqa: E731
    pc = np.r_[np.nan, C[:-1]]
    with np.errstate(invalid="ignore", divide="ignore"):
        up = C > pc
    # MIKRO
    mk = nanv()
    if m >= 61:
        Wu = _sw(up, 60); third = Wu[:, 2:] & Wu[:, 1:-1] & Wu[:, :-2]
        cond = np.concatenate([np.ones((len(Wu), 1), bool), ~Wu[:, :57]], axis=1)
        mk[59:] = (third & cond).sum(1); mk[59] = np.nan
    out["MIKRO"] = mk
    # RS
    with np.errstate(invalid="ignore", divide="ignore"):
        rs = C / Lp
        out["RS_UZAK"] = rs / _yo_roll(rs, 60, "max") - 1
    kon = OS._os_atrp_f15(pd.DataFrame({"High": H, "Low": L, "Close": C}))[1]
    out["KONUM120"] = kon
    with np.errstate(invalid="ignore"):
        bir = ((kon < 0.5) & (out["RS_UZAK"] >= -0.03)).astype(float)
    bir[~(np.isfinite(kon) & np.isfinite(out["RS_UZAK"]))] = np.nan; out["RS_DIP_BIR"] = bir
    # oynaklık
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.log(C / pc)
    out["_oyn60"] = pd.Series(lr).rolling(60, min_periods=60).std(ddof=1).to_numpy(float)
    TR = np.where(np.isfinite(pc), np.maximum(H, pc) - np.minimum(L, pc), H - L)
    out["ATRP20"] = _yo_roll(TR, 20, "mean") / C
    # MA
    S20, S50, S200 = (_yo_roll(C, w, "mean") for w in (20, 50, 200))
    with np.errstate(invalid="ignore"):
        kod = (S20 > S50).astype(float) + (S50 > S200).astype(float) + (S20 > S200).astype(float)
    kod[~np.isfinite(S200)] = np.nan; out["MA_KOD"] = kod
    with np.errstate(invalid="ignore", divide="ignore"):
        e = S20 / np.r_[np.full(10, np.nan), S20[:-10]] - 1 if m > 10 else nanv()
        out["MA_EGIM_DEG"] = e - np.r_[np.full(10, np.nan), e[:-10]] if m > 10 else nanv()
    # DD (250)
    zb, zd, db, dh = nanv(), nanv(), nanv(), nanv()
    if m >= 250:
        Wc = _sw(C, 250); ar = np.arange(250)
        pk = 249 - np.argmax(Wc[:, ::-1], axis=1); cmax = Wc[np.arange(len(Wc)), pk]
        Mk = np.where(ar[None, :] >= pk[:, None], Wc, np.inf)
        dk = 249 - np.argmin(Mk[:, ::-1], axis=1); cdip = Wc[np.arange(len(Wc)), dk]; Ck = C[249:]
        zb[249:] = 249 - pk; zd[249:] = Ck / cmax - 1; db[249:] = 249 - dk
        dh[249:] = (Ck / cdip - 1) / np.maximum(249 - dk, 1) * 100.0
    out.update({"ZIRVE_BAR": zb, "ZIRVE_DUSUS": zd, "DIP_BAR": db, "DIP_HIZ": dh})
    # CLV
    clv = (C - L) / (H - L)
    c10 = _yo_roll(clv, 10, "mean"); c30 = _yo_roll(clv, 30, "mean")
    out["CLV10"] = c10; out["CLV_FARK"] = c10 - np.r_[np.full(10, np.nan), c30[:-10]] if m > 10 else nanv()
    # YUKSELEN_DIP
    yd = nanv()
    if m >= 60:
        D = np.zeros(m, bool)
        if m >= 5:
            i = np.arange(2, m - 2)
            D[i] = (L[i] < L[i - 1]) & (L[i] < L[i - 2]) & (L[i] <= L[i + 1]) & (L[i] <= L[i + 2])
        dp = np.flatnonzero(D); ch = np.zeros(len(dp), np.int64)
        for q in range(1, len(dp)):
            ch[q] = ch[q - 1] + 1 if L[dp[q - 1]] < L[dp[q]] else 0
        kk = np.arange(59, m); lo = np.searchsorted(dp, kk - 57, "left"); hi = np.searchsorted(dp, kk - 2, "right"); nd = hi - lo
        v = np.zeros(len(kk)); has = nd > 0
        v[has] = np.minimum(ch[hi[has] - 1], nd[has] - 1)
        yd[59:] = v
    out["YUKSELEN_DIP"] = yd
    # kontroller
    with np.errstate(invalid="ignore", divide="ignore"):
        mom = nanv()
        if m > 252:
            mom[252:] = C[231:m - 21] / C[:m - 252] - 1
        out["MOM_12_1"] = mom
        f15 = nanv()
        if m > 15:
            f15[15:] = C[15:] / C[:-15] - 1
        out["F15"] = f15
        r = (H - L) / C
        med16 = _yo_roll(r, 16, "median"); med120 = _yo_roll(r, 120, "median")
        out["BOY_YUZDE_ORAN"] = med16 / (np.r_[np.full(16, np.nan), med120[:-16]] if m > 16 else nanv())
        mn16 = _yo_roll(L, 16, "min"); mx60 = _yo_roll(H, 60, "max")
        out["ONCEKI_DUSUS"] = mn16 / (np.r_[np.full(16, np.nan), mx60[:-16]] if m > 16 else nanv()) - 1
        # piyasa bayrakları
        for ad, S in (("_u20", S20), ("_u50", S50), ("_u200", S200)):
            b = (C > S).astype(float); b[~np.isfinite(S)] = np.nan; out[ad] = b
        mn20 = _yo_roll(C, 20, "min"); b = (C <= mn20).astype(float); b[~np.isfinite(mn20)] = np.nan; out["_d20"] = b
        mx60c = _yo_roll(C, 60, "max"); mn60c = _yo_roll(C, 60, "min")
        b = (C >= mx60c).astype(float); b[~np.isfinite(mx60c)] = np.nan; out["_z60"] = b
        b = (C <= mn60c).astype(float); b[~np.isfinite(mn60c)] = np.nan; out["_d60"] = b
        r20 = nanv()
        if m > 20:
            r20[20:] = C[20:] / C[:-20] - 1
        out["_r20"] = r20
    return out


def yo_endeks(Cl: np.ndarray, P2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Pazar endeksi L (eşit ağırlıklı günlük getiri, P2[t] kümesi; Cf = 5 satır ileri taşınmış kapanış)."""
    n = len(Cl); Cf = pd.DataFrame(Cl).ffill(limit=5).to_numpy(float); r = np.zeros(n); mn = int(YO_ESIK["piyasa"]["en_az_hisse"])
    with np.errstate(invalid="ignore", divide="ignore"):
        g = Cl[1:] / Cf[:-1] - 1
    ok = P2[1:] & np.isfinite(g); k = ok.sum(1); s = np.where(ok, g, 0.0).sum(1)
    r[1:] = np.where(k >= mn, s / np.maximum(k, 1), 0.0)
    return np.cumprod(1 + r), r


def _yo_pay(M: np.ndarray, A: np.ndarray, en_az: int) -> np.ndarray:
    ok = A & np.isfinite(M); k = ok.sum(1); s = np.where(ok, M, 0.0).sum(1)
    return np.where(k >= en_az, s / np.maximum(k, 1), np.nan)


def yo_piyasa_ozellik(L: np.ndarray, P2: np.ndarray, MAT: Dict[str, np.ndarray]) -> pd.DataFrame:
    """Pazar-gün özellikleri (t satırı; t'ye kadarki bilgi). MAT: n x u matrisleri (_u20, _u50, _u200, _d20, _z60, _d60, _r20, ATRP20)."""
    n = len(L); ea = int(YO_ESIK["piyasa"]["kume_en_az"]); F: Dict[str, np.ndarray] = {}
    for w, ad in ((20, "_u20"), (50, "_u50"), (200, "_u200")):
        g = _yo_pay(MAT[ad], P2, ea); F[f"GEN{w}"] = g
        for dd in (5, 10):
            F[f"GEN{w}_D{dd}"] = g - np.r_[np.full(dd, np.nan), g[:-dd]]
    Ls = pd.Series(L)
    F["PAZ_R20"] = (Ls / Ls.shift(20) - 1).to_numpy(float); F["PAZ_R60"] = (Ls / Ls.shift(60) - 1).to_numpy(float)
    F["PAZ_DD60"] = (Ls / Ls.rolling(60, min_periods=60).max() - 1).to_numpy(float)
    F["DIP20_PAY"] = _yo_pay(MAT["_d20"], P2, ea)
    F["YENI_ZD"] = _yo_pay(MAT["_z60"], P2, ea) - _yo_pay(MAT["_d60"], P2, ea)
    sd = np.full(n, np.nan); med = np.full(n, np.nan)
    for t in range(n):
        x = MAT["_r20"][t][P2[t]]; x = x[np.isfinite(x)]
        if len(x) >= ea:
            sd[t] = float(np.std(x, ddof=1))
        a = MAT["ATRP20"][t][P2[t]]; a = a[np.isfinite(a)]
        if len(a) >= ea:
            med[t] = float(np.median(a))
    F["KESIT_SD"] = sd
    sira = np.full(n, np.nan)
    for t in range(n):
        if not np.isfinite(med[t]):
            continue
        h = med[max(0, t - 249):t + 1]; h = h[np.isfinite(h)]
        if len(h) >= 60:
            sira[t] = float(((h < med[t]).sum() + 0.5 * (h == med[t]).sum()) / len(h))
    F["ATRP_MED_SIRA"] = sira
    return pd.DataFrame(F)[YO_PIYASA_OZ]


def yo_kesit_sira(deger: np.ndarray, satir: np.ndarray, MATv: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Örnek satırlarının (değer, t satırı) A_t kümesindeki yüzdelik sırası ((küçük + 0,5 eşit) / n; küme >= 30)."""
    out = np.full(len(deger), np.nan); ea = int(YO_ESIK["piyasa"]["kume_en_az"])
    s = pd.Series(np.arange(len(deger))).groupby(np.asarray(satir)).indices
    for t, ii in s.items():
        x = MATv[t][A[t]]; x = np.sort(x[np.isfinite(x)])
        if len(x) < ea:
            continue
        v = deger[ii]; lo = np.searchsorted(x, v, "left"); hi = np.searchsorted(x, v, "right")
        r = (lo + 0.5 * (hi - lo)) / len(x); r[~np.isfinite(v)] = np.nan; out[ii] = r
    return out


def yo_ornek_maske(m: int, pos: np.ndarray, p2: np.ndarray, tarih: pd.DatetimeIndex) -> np.ndarray:
    """Örnek k'ler (getirisiz): k % 5 == 0, k + 15 < m, boşluk / pencere kuralı, giriş satırında P2, giriş tarihi 2016-2022, 15. bar <= kesik."""
    E = YO_ESIK["ornek"]; U = int(YO_ESIK["yukselis"]["ufuk"])
    if m < U + 2:
        return np.array([], np.int64)
    k = np.arange(0, m - U, int(E["adim"]))
    ok = (pos[k + 1] - pos[k] <= int(E["giris_bosluk"])) & (pos[k + U] - pos[k + 1] <= int(E["pencere_satir"]) - 1) & p2[pos[k + 1]]
    gt = tarih[pos[k + 1]]; ok &= (gt >= pd.Timestamp("2016-01-01")) & (gt <= pd.Timestamp("2022-12-31")) & (tarih[pos[k + U]] <= YO_KESIK)
    return k[ok]


# ================================================================ 3) PANEL HAZIRLIĞI (getirisiz)
def yo_hazirla_pazar(pazar: str, ham: Optional[str] = None, Vd: Optional[Dict[str, Any]] = None, Pn: Optional[Dict[str, Any]] = None,
                     P2: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """Veri -> P2 paneli -> özellikler (örnek satırları + pazar-gün) + sonuç ham deposu. Getiri hesaplanmaz. Dosyalar ham klasöre."""
    t0 = time.time(); ham = ham or YO_YOL["ham"]; os.makedirs(ham, exist_ok=True)
    if Vd is None:
        Vd = MI.mi_veri(pazar, YO_YOL["acik"])
    yo_kesik_kapi(Vd["V"], f"günlük {pazar}")
    if Pn is None or P2 is None:
        import KART_TUR2 as KT2
        Pn, P2 = KT2.k2_panel(Vd, pazar)
    idx = Pn["tarih"]; S = Pn["sembol"]; dep = Pn["dep"]; n, u = len(idx), len(S)
    if (np.asarray(dep["m"]) != np.array([len(Vd["V"][s]) for s in S])).any():
        raise YOHata("K10: bar deposu ile veri uzunluğu farklı")
    L, r = yo_endeks(Pn["Cl"], P2)
    MAT = {a: np.full((n, u), np.nan) for a in ("_u20", "_u50", "_u200", "_d20", "_z60", "_d60", "_r20", "ATRP20", "_oyn60")}
    parca = []
    for j, s in enumerate(S):
        a, b = int(dep["off"][j]), int(dep["off"][j + 1]); pos = dep["POS"][a:b]; m = b - a
        if m < 2:
            continue
        Fh = yo_hisse_ozellik(dep["O"][a:b], dep["H"][a:b], dep["L"][a:b], dep["C"][a:b], L[pos])
        for ad in MAT:
            MAT[ad][pos, j] = Fh[ad]
        kk = yo_ornek_maske(m, pos, P2[:, j], idx)
        if not len(kk):
            continue
        D = {"j": np.full(len(kk), j, np.int64), "k": kk, "t_row": pos[kk], "d_row": pos[kk + 1]}
        for ad in YO_OZ:
            if ad in Fh:
                D[ad] = Fh[ad][kk]
        D["_oyn60"] = Fh["_oyn60"][kk]
        parca.append(pd.DataFrame(D))
    X = pd.concat(parca, ignore_index=True)
    PZ = yo_piyasa_ozellik(L, P2, MAT)
    X["GEN50"] = PZ.GEN50.to_numpy()[X.t_row.to_numpy()]; X["GEN50_D10"] = PZ.GEN50_D10.to_numpy()[X.t_row.to_numpy()]
    X["OYN_SIRA"] = yo_kesit_sira(X._oyn60.to_numpy(float), X.t_row.to_numpy(), MAT["_oyn60"], P2)
    X["pazar"] = pazar; X["sembol"] = np.asarray(S, object)[X.j.to_numpy()]
    X["tarih"] = idx[X.t_row.to_numpy()]; X["giris"] = idx[X.d_row.to_numpy()]
    X["hucre"] = [yo_hucre(g, pazar) for g in X.giris]; X["ay"] = X.giris.dt.strftime("%Y-%m")
    X = X[["pazar", "sembol", "j", "k", "t_row", "d_row", "tarih", "giris", "hucre", "ay"] + YO_OZ].sort_values(["giris", "sembol"], kind="stable").reset_index(drop=True)
    # pazar-gün satırları (t; giriş d = t + 1)
    U = int(YO_ESIK["yukselis"]["ufuk"]); tt = np.arange(0, n - U)
    gd = idx[tt + 1]; okd = (gd >= pd.Timestamp("2016-01-01")) & (gd <= pd.Timestamp("2022-12-31")) & (idx[tt + U] <= YO_KESIK)
    tt = tt[okd]
    G = PZ.iloc[tt].reset_index(drop=True); G.insert(0, "t_row", tt); G.insert(1, "d_row", tt + 1); G.insert(2, "tarih", idx[tt]); G.insert(3, "giris", idx[tt + 1])
    G.insert(4, "hucre", [yo_hucre(g, pazar) for g in G.giris]); G.insert(5, "ay", G.giris.dt.strftime("%Y-%m")); G.insert(0, "pazar", pazar)
    # dosyalar
    yol_x = _yo_ham(f"ozellik_{pazar}.pkl", ham); yol_g = _yo_ham(f"piyasa_{pazar}.pkl", ham); yol_h = _yo_ham(f"ham_{pazar}.npz", ham)
    with open(yol_x, "wb") as f:
        pickle.dump(X, f, protocol=4)
    with open(yol_g, "wb") as f:
        pickle.dump(G, f, protocol=4)
    np.savez(yol_h, O=dep["O"], H=dep["H"], L=dep["L"], C=dep["C"], POS=dep["POS"], off=dep["off"], Op=Pn["Op"], Cl=Pn["Cl"], P2=P2,
             tarih=np.asarray(idx.values.astype("datetime64[ns]")), sembol=np.asarray(S, dtype="U32"))
    yolog.info("%s: %d hisse-gün, %d pazar-gün, %d hisse (%.0f sn)", pazar, len(X), len(G), u, time.time() - t0)
    del MAT; gc.collect()
    return {"pazar": pazar, "hisse_gun": int(len(X)), "pazar_gun": int(len(G)), "hisse": u, "dosya": {"ozellik": yol_x, "piyasa": yol_g, "ham": yol_h}}


def yo_hazirla(ham: Optional[str] = None) -> Dict[str, Any]:
    out = {}
    for p in YO_PAZAR:
        out[p] = yo_hazirla_pazar(p, ham); gc.collect()
    return out


def yo_yukle(pazar: str, ham: Optional[str] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    with open(_yo_ham(f"ozellik_{pazar}.pkl", ham), "rb") as f:
        X = pickle.load(f)
    with open(_yo_ham(f"piyasa_{pazar}.pkl", ham), "rb") as f:
        G = pickle.load(f)
    return X, G


def yo_dosya_sha(ham: Optional[str] = None) -> Dict[str, str]:
    out = {}
    for p in YO_PAZAR:
        for ad in (f"ozellik_{p}.pkl", f"piyasa_{p}.pkl", f"ham_{p}.npz"):
            out[ad] = MI._mi_sha(_yo_ham(ad, ham))
    return out


# ================================================================ 4) SONUÇ KAPISI (Y / R15 yalnız buradan)
_YO_ASAMA_IZIN = {"adim1": {YO_KESIF}, "adim2": set(YO_HUCRE), "test": set(YO_HUCRE)}


def yo_sonuc(pazar: str, X: pd.DataFrame, G: pd.DataFrame, asama: str, ham: Optional[str] = None,
             depo: Optional[Dict[str, np.ndarray]] = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Sonuç sütunları (Y10, Y5, D10, R15, KALICI, P15) YALNIZ izin verilen hücrelerin satırları için. ADIM 1'de yalnız ABD|d1619 (assert)."""
    if asama not in _YO_ASAMA_IZIN:
        raise YOHata(f"aşama: {asama}")
    izin = _YO_ASAMA_IZIN[asama]
    hx = set(X.hucre.unique()); hg = set(G.hucre.unique())
    if not (hx | hg) <= izin:
        raise YOHata(f"SIRA: {asama} aşamasında izin dışı hücre sonucu istendi: {sorted((hx | hg) - izin)}")
    if asama == "adim1" and (pazar != "ABD" or hx != {YO_KESIF}):
        raise YOHata("SIRA: ADIM 1 yalnız ABD 2016-19 (keşif) satırlarıyla")
    if depo is None:
        z = np.load(_yo_ham(f"ham_{pazar}.npz", ham)); depo = {k: z[k] for k in z.files}
    dep = {k: depo[k] for k in ("O", "H", "L", "C", "POS", "off")}
    R = yo_sonuc_dizi(dep, X.j.to_numpy(np.int64), X.k.to_numpy(np.int64))
    P15, _ = yo_P15(depo["Op"], depo["Cl"], depo["P2"])
    Sx = pd.DataFrame(R, index=X.index); Sx["P15"] = P15[X.d_row.to_numpy()]
    Sg = pd.DataFrame({"P15": P15[G.d_row.to_numpy()]}, index=G.index)
    yp, dp = float(YO_ESIK["piyasa"]["esik_YP"]), float(YO_ESIK["piyasa"]["esik_DP"])
    with np.errstate(invalid="ignore"):
        Sg["YP"] = np.where(np.isfinite(Sg.P15), (Sg.P15 >= yp).astype(float), np.nan)
        Sg["DP"] = np.where(np.isfinite(Sg.P15), (Sg.P15 <= dp).astype(float), np.nan)
    return Sx, Sg


# ================================================================ 5) GETİRİSİZ SAYIM
def yo_sayim(XS: Dict[str, pd.DataFrame], GS: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Hücre x pazar: hisse-gün, farklı ay, hisse; özelliklerin eksik payı ve dağılımı; sıra ilişkisi matrisi (keşif + hücreler). Y / R15 yok."""
    S: Dict[str, Any] = {"hisse": {}, "piyasa": {}, "spearman": {}}
    qs = [0.01, 0.02, 0.10, 0.25, 0.50, 0.75, 0.90, 0.98, 0.99]
    for p, X in XS.items():
        for h, g in X.groupby("hucre"):
            if h not in YO_HUCRE:
                continue
            ao = HV.hv25_ay_ozet(g.giris.dt.strftime("%Y-%m-%d").tolist())
            oz = {}
            for c in YO_OZ:
                v = g[c].to_numpy(float); f = np.isfinite(v)
                oz[c] = {"eksik": float(1 - f.mean()), "q": [float(x) for x in np.quantile(v[f], qs)] if f.any() else []}
            S["hisse"][h] = {"hisse_gun": int(len(g)), "ay": ao["ay"], "ust3_pay": ao["ust3_pay"], "hisse": int(g.sembol.nunique()), "ozellik": oz}
            R = g[YO_OZ].rank().corr(method="pearson")
            S["spearman"][h] = [[None if not np.isfinite(x) else round(float(x), 3) for x in row] for row in R.to_numpy()]
    for p, G in GS.items():
        for h, g in G.groupby("hucre"):
            if h not in YO_HUCRE:
                continue
            oz = {c: {"eksik": float(1 - np.isfinite(g[c].to_numpy(float)).mean())} for c in YO_PIYASA_OZ}
            S["piyasa"][h] = {"gun": int(len(g)), "ay": int(g.ay.nunique()), "ozellik": oz}
    S["sutun"] = YO_OZ
    return S


def yo_sayim_kos(ham: Optional[str] = None) -> Dict[str, Any]:
    XS, GS = {}, {}
    for p in YO_PAZAR:
        XS[p], GS[p] = yo_yukle(p, ham)
    return yo_sayim(XS, GS)


# ================================================================ 6) İSTATİSTİK
def yo_ay_W(ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Ay kümeleri (yerine koyarak; multinomial ağırlık). Döner (küme indeksi, W B x K)."""
    B = int(B or YO_ESIK["boot"]["B"]); u, k = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    W = _yo_rng(anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)
    return k, W


def _q(v: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    v = v[np.isfinite(v)]
    if not len(v):
        return None, None
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


def yo_boot_ort(x: np.ndarray, ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Ay kümeli bootstrap ortalama."""
    x = np.asarray(x, float); f = np.isfinite(x); x = x[f]; ay = np.asarray(ay, str)[f]
    if len(x) < 2:
        return {"ort": None, "alt": None, "ust": None}
    k, W = yo_ay_W(ay, anahtar, B); K = W.shape[1]
    s = np.bincount(k, weights=x, minlength=K); n = np.bincount(k, minlength=K).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (W @ s) / (W @ n)
    a, b = _q(d)
    return {"ort": float(x.mean()), "alt": a, "ust": b}


def yo_olc(uc: np.ndarray, q: np.ndarray, Y: np.ndarray, D: np.ndarray, TF: np.ndarray, ay: np.ndarray, anahtar: str,
           B: Optional[int] = None, ek: Optional[Dict[str, np.ndarray]] = None, nq: int = 5) -> Dict[str, Any]:
    """Bir satır x hücre: ham KAT, ATRP (ya da puan) beşliği içi KAT, ASİMETRİ, TOPLAM FARK; ay kümeli bootstrap. q: 0..nq-1 (popülasyon)."""
    uc = np.asarray(uc, bool); q = np.asarray(q, np.int64); Y = np.asarray(Y, float); D = np.asarray(D, float); TF = np.asarray(TF, float)
    ay = np.asarray(ay, str); nu = int(uc.sum()); N = len(uc)
    out: Dict[str, Any] = {"n": nu, "N": int(N)}
    ao = HV.hv25_ay_ozet([f"{a}-01" for a in ay[uc]]) if nu else {"ay": 0, "ust3_pay": None, "ust3": []}
    out.update({"ay": ao["ay"], "ust3_pay": ao["ust3_pay"], "ust3": ao["ust3"]})
    if nu < 2 or N < 10:
        return out
    pq = np.array([Y[q == i].mean() if (q == i).any() else np.nan for i in range(nq)]); dq = np.array([D[q == i].mean() if (q == i).any() else np.nan for i in range(nq)])
    nuq = np.array([(uc & (q == i)).sum() for i in range(nq)], float)
    E = float(np.nansum(nuq * pq)); O = float(Y[uc].sum())
    out["P_uc"] = O / nu; out["P_taban"] = float(Y.mean()); out["P_beklenen"] = E / nu; out["D_uc"] = float(D[uc].mean()); out["D_taban"] = float(D.mean())
    out["KAT_HAM"] = (O / nu) / out["P_taban"] if out["P_taban"] > 0 else None
    out["KAT"] = O / E if E > 0 else None
    out["ASIMETRI"] = (O - D[uc].sum()) / nu - float(np.nansum(nuq * (pq - dq))) / nu
    out["TOPLAM_FARK"] = float(TF[uc].mean())
    k, W = yo_ay_W(ay, anahtar, B); K = W.shape[1]
    bc = lambda v: np.bincount(k, weights=v, minlength=K)  # noqa: E731
    Nq = np.stack([bc((q == i).astype(float)) for i in range(nq)], 1); Yq = np.stack([bc(Y * (q == i)) for i in range(nq)], 1)
    Dq = np.stack([bc(D * (q == i)) for i in range(nq)], 1); NUq = np.stack([bc((uc & (q == i)).astype(float)) for i in range(nq)], 1)
    YU = bc(Y * uc); DU = bc(D * uc); TFU = bc(np.where(uc, TF, 0.0)); NU = bc(uc.astype(float)); YA = bc(Y); NA = bc(np.ones(N))
    with np.errstate(invalid="ignore", divide="ignore"):
        wN = W @ Nq; pq_ = (W @ Yq) / wN; dq_ = (W @ Dq) / wN; wNU = W @ NUq
        E_ = np.nansum(wNU * pq_, axis=1); O_ = W @ YU; nu_ = W @ NU
        kat = O_ / E_; kh = (O_ / nu_) / ((W @ YA) / (W @ NA))
        asm = (O_ - W @ DU) / nu_ - np.nansum(wNU * (pq_ - dq_), axis=1) / nu_
        tf = (W @ TFU) / nu_
    for ad, v in (("KAT", kat), ("KAT_HAM", kh), ("ASIMETRI", asm), ("TOPLAM_FARK", tf)):
        a, b = _q(v); out[f"{ad}_alt"] = a; out[f"{ad}_ust"] = b
    kv = kat[np.isfinite(kat)]
    out["p"] = float((1 + (kv <= 1).sum()) / (len(kv) + 1)) if len(kv) else None
    if ek:
        for ad, v in ek.items():
            v = np.asarray(v, float); f = uc & np.isfinite(v)
            out[ad] = float(v[f].mean()) if f.any() else None
    return out


def yo_bh(p: List[Optional[float]], q: float) -> List[Optional[float]]:
    return HV._hv_bh(p, q)


def yo_besli(x: np.ndarray, sinir: List[float]) -> np.ndarray:
    """Beşlik indeksi 0..4 (sınırlar sağdan kapalı: x <= s0 -> 0); NaN -> -1."""
    x = np.asarray(x, float); q = np.searchsorted(np.asarray(sinir, float), x, side="left").astype(np.int64); q[~np.isfinite(x)] = -1
    return q


def yo_logit_newton(Xm: np.ndarray, y: np.ndarray, it: int = 30) -> np.ndarray:
    """Lojistik (Newton / IRLS; küçük ridge 1e-8). Xm kesişim sütunu dahil."""
    w = np.zeros(Xm.shape[1])
    for _ in range(it):
        z = np.clip(Xm @ w, -30, 30); p = 1 / (1 + np.exp(-z)); g = Xm.T @ (p - y)
        Hm = (Xm * (p * (1 - p))[:, None]).T @ Xm + 1e-8 * np.eye(Xm.shape[1])
        st = np.linalg.solve(Hm, g); w -= st
        if np.abs(st).max() < 1e-10:
            break
    return w


def yo_logit_l1(Xm: np.ndarray, y: np.ndarray, lam: float, it: int) -> np.ndarray:
    """L1 lojistik (FISTA): ort log kaybı + lam |w[1:]|_1 (kesişim cezasız)."""
    n = len(y); v = np.random.default_rng(0).normal(size=Xm.shape[1])
    for _ in range(50):
        v = Xm.T @ (Xm @ v); v /= np.linalg.norm(v)
    Lc = 0.25 * float(v @ (Xm.T @ (Xm @ v))) / n; st = 1.0 / max(Lc, 1e-12)
    w = np.zeros(Xm.shape[1]); z = w.copy(); tk = 1.0
    for _ in range(int(it)):
        p = 1 / (1 + np.exp(-np.clip(Xm @ z, -30, 30))); g = Xm.T @ (p - y) / n
        wn = z - st * g; wn[1:] = np.sign(wn[1:]) * np.maximum(np.abs(wn[1:]) - st * lam, 0.0)
        tn = (1 + np.sqrt(1 + 4 * tk * tk)) / 2; z = wn + (tk - 1) / tn * (wn - w); w = wn; tk = tn
    return w


def yo_tasarim(X: pd.DataFrame, sutun: List[str], ort: Dict[str, float], sd: Dict[str, float]) -> np.ndarray:
    M = np.ones((len(X), len(sutun) + 1))
    for i, c in enumerate(sutun):
        v = (X[c].to_numpy(float) - ort[c]) / (sd[c] if sd[c] > 0 else 1.0); v[~np.isfinite(v)] = 0.0; M[:, i + 1] = v
    return M


# ================================================================ 7) ADIM 1 (yalnız KEŞİF)
def yo_esle(tarih_row: np.ndarray, q: np.ndarray, Y: np.ndarray, es: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Olay (Y = 1) başına aynı gün aynı beşlik Y = 0 kontroller (yerine koymadan; tohum 28). Döner (olay indeksleri, kontrol matrisi n_o x es, -1 boş)."""
    es = int(es or YO_ESIK["adim1"]["es"]); rng = _yo_rng("esle")
    df = pd.DataFrame({"t": np.asarray(tarih_row), "q": np.asarray(q), "Y": np.asarray(Y, float), "i": np.arange(len(Y))})
    df = df[df.q >= 0]; ev, ct = [], []
    for (_, _), g in df.groupby(["t", "q"], sort=True):
        o = g.i[g.Y == 1].to_numpy(); c = g.i[g.Y == 0].to_numpy()
        if not len(o) or not len(c):
            continue
        for i in o:
            sec = rng.choice(c, size=min(es, len(c)), replace=False); row = np.full(es, -1, np.int64); row[:len(sec)] = sec
            ev.append(i); ct.append(row)
    return np.asarray(ev, np.int64), (np.vstack(ct) if ct else np.zeros((0, es), np.int64))


def yo_smd_auc(x: np.ndarray, ev: np.ndarray, ct: np.ndarray, ay_ev: np.ndarray, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Eşli SMD ve eşli AUC + ay kümeli bootstrap (olay ayı)."""
    x = np.asarray(x, float); xe = x[ev]; xc = np.where(ct >= 0, x[np.maximum(ct, 0)], np.nan)
    okc = np.isfinite(xc); oke = np.isfinite(xe) & okc.any(1)
    if oke.sum() < 10:
        return {"n_olay": int(oke.sum())}
    xe = xe[oke]; xc = xc[oke]; okc = okc[oke]; ay = np.asarray(ay_ev, str)[oke]
    nc = okc.sum(1).astype(float); s1c = np.where(okc, xc, 0).sum(1); s2c = np.where(okc, xc * xc, 0).sum(1)
    with np.errstate(invalid="ignore"):
        a = (np.where(okc, (xe[:, None] > xc).astype(float) + 0.5 * (xe[:, None] == xc), 0).sum(1)) / nc
    def smd(se1, se2, ne, sc1, sc2, ncc):
        me = se1 / ne; mc = sc1 / ncc; ve = se2 / ne - me * me; vc = sc2 / ncc - mc * mc
        with np.errstate(invalid="ignore", divide="ignore"):
            return (me - mc) / np.sqrt((ve + vc) / 2)
    out = {"n_olay": int(len(xe)), "n_kontrol": int(nc.sum()), "ort_olay": float(xe.mean()), "ort_kontrol": float(s1c.sum() / nc.sum()),
           "SMD": float(smd(xe.sum(), (xe * xe).sum(), len(xe), s1c.sum(), s2c.sum(), nc.sum())), "AUC": float(a.mean())}
    k, W = yo_ay_W(ay, anahtar, B); K = W.shape[1]; bc = lambda v: np.bincount(k, weights=v, minlength=K)  # noqa: E731
    sm = smd(W @ bc(xe), W @ bc(xe * xe), W @ bc(np.ones(len(xe))), W @ bc(s1c), W @ bc(s2c), W @ bc(nc))
    with np.errstate(invalid="ignore", divide="ignore"):
        au = (W @ bc(a)) / (W @ bc(np.ones(len(xe))))
    out["SMD_alt"], out["SMD_ust"] = _q(sm); out["AUC_alt"], out["AUC_ust"] = _q(au)
    return out


def yo_smd_auc_esiz(x: np.ndarray, y: np.ndarray, ay: np.ndarray, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    """Eşsiz (piyasa günü) SMD ve AUC (Mann-Whitney) + ay kümeli bootstrap."""
    x = np.asarray(x, float); y = np.asarray(y, float); f = np.isfinite(x) & np.isfinite(y); x, y, ay = x[f], y[f], np.asarray(ay, str)[f]
    a, b = x[y == 1], x[y == 0]
    if len(a) < 5 or len(b) < 5:
        return {"n_olay": int(len(a)), "n_kontrol": int(len(b))}
    def smd(m1, v1, m0, v0):
        with np.errstate(invalid="ignore", divide="ignore"):
            return (m1 - m0) / np.sqrt((v1 + v0) / 2)
    Pm = (a[:, None] > b[None, :]).astype(float) + 0.5 * (a[:, None] == b[None, :])
    out = {"n_olay": int(len(a)), "n_kontrol": int(len(b)), "ort_olay": float(a.mean()), "ort_kontrol": float(b.mean()),
           "SMD": float(smd(a.mean(), a.var(), b.mean(), b.var())), "AUC": float(Pm.mean())}
    k, W = yo_ay_W(ay, anahtar, B); ka, kb = k[y == 1], k[y == 0]
    wa = W[:, ka]; wb = W[:, kb]
    sa, na, sa2 = wa @ a, wa.sum(1), wa @ (a * a); sb, nb, sb2 = wb @ b, wb.sum(1), wb @ (b * b)
    with np.errstate(invalid="ignore", divide="ignore"):
        ma, mb = sa / na, sb / nb; sm = smd(ma, sa2 / na - ma * ma, mb, sb2 / nb - mb * mb)
        au = np.einsum("bi,ij,bj->b", wa, Pm, wb) / (na * nb)
    out["SMD_alt"], out["SMD_ust"] = _q(sm); out["AUC_alt"], out["AUC_ust"] = _q(au)
    return out


def yo_uc_maske(x: np.ndarray, ozellik: str, yon: str, esik: Optional[float]) -> np.ndarray:
    """Uç maskesi (BÜYÜK: >= eşik; KÜÇÜK: <= eşik; bayrak: yönün kategorisi)."""
    x = np.asarray(x, float)
    with np.errstate(invalid="ignore"):
        if ozellik in YO_BAYRAK:
            lo, hi = YO_BAYRAK[ozellik]; return x == (hi if yon == "BÜYÜK" else lo)
        return (x >= esik) if yon == "BÜYÜK" else (x <= esik)


def yo_kesim_belirle(Xk: pd.DataFrame, ad: str, yon: str) -> Dict[str, Any]:
    """Keşif dağılımından uç kesimleri (yalnız keşif satırları; assert)."""
    if set(Xk.hucre.unique()) != {YO_KESIF}:
        raise YOHata("SIRA: kesimler yalnız keşif satırlarından belirlenir")
    v = Xk[ad].to_numpy(float); v = v[np.isfinite(v)]
    if ad in YO_BAYRAK:
        return {"bayrak": True}
    out = {}
    for u in YO_ESIK["kesim"]["uc"]:
        out[f"{u:.2f}"] = float(np.quantile(v, 1 - u if yon == "BÜYÜK" else u))
    return out


def yo_satirlar(K: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Hisse satırları (özellik x uç; bayraklar tek)."""
    S = []
    for c in YO_OZ:
        y = K["yon"][c]["yon"]
        if c in YO_BAYRAK:
            S.append({"ad": f"{c}|BAYRAK", "ozellik": c, "uc": "BAYRAK", "yon": y})
        else:
            for u in YO_ESIK["kesim"]["uc"]:
                S.append({"ad": f"{c}|{u:.2f}", "ozellik": c, "uc": f"{u:.2f}", "yon": y})
    return S


def yo_hucre_esik(K: Dict[str, Any], hucre: str) -> str:
    """Hangi kesim kümesi: ABD hücreleri 'ABD' (keşif sayıları), AVR hücreleri 'AVR' (AVR 2016-19 özellik dağılımındaki aynı yüzdelik)."""
    return "AVR" if hucre.startswith("AVR") else "ABD"


def yo_hucre_kur(X: pd.DataFrame, S: pd.DataFrame, K: Dict[str, Any], hucre: str) -> Dict[str, Any]:
    """Hücre ortak dizileri: ATRP beşliği, toplam fark, ay, kontrol puanı beşliği."""
    m = (X.hucre == hucre).to_numpy(); x = X[m]; s = S[m]; ek = yo_hucre_esik(K, hucre)
    q = yo_besli(x.ATRP20.to_numpy(float), K["atrp_besli"][ek])
    r = s.R15.to_numpy(float); hm = pd.Series(r).groupby(x.sembol.to_numpy()).transform("mean").to_numpy()
    km = K["kontrol_model"]; Mk = yo_tasarim(x, km["sutun"], km["ort"], km["sd"]); puan = Mk @ np.asarray(km["w"])
    qp = yo_besli(puan, km["besli"][ek])
    return {"m": m, "x": x, "s": s, "q": q, "TF": r - hm, "ay": x.ay.to_numpy(str), "qp": qp}


def yo_satir_maske(H: Dict[str, Any], K: Dict[str, Any], sat: Dict[str, Any], hucre: str) -> Tuple[np.ndarray, np.ndarray]:
    """Döner (popülasyon maskesi, uç maskesi) hücre satırları üzerinde."""
    x = H["x"]; ek = yo_hucre_esik(K, hucre)
    if sat.get("tur") == "birlesim":
        pop = np.ones(len(x), bool); uc = np.ones(len(x), bool)
        for c, u in sat["uye"]:
            v = x[c].to_numpy(float); pop &= np.isfinite(v)
            uc &= yo_uc_maske(v, c, K["yon"][c]["yon"], None if c in YO_BAYRAK else K["kesim"][ek][c][u])
    elif sat.get("tur") == "puan":
        P = K["puan"]; v = yo_tasarim(x, P["sutun"], P["ort"], P["sd"]) @ np.asarray(P["w"]); pop = np.isfinite(v)
        uc = v >= P["kesim"][ek][sat["uc"]]
    else:
        c = sat["ozellik"]; v = x[c].to_numpy(float); pop = np.isfinite(v)
        uc = yo_uc_maske(v, c, sat["yon"], None if c in YO_BAYRAK else K["kesim"][ek][c][sat["uc"]])
    pop &= H["q"] >= 0
    return pop, uc & pop


def yo_satir_olc(H: Dict[str, Any], K: Dict[str, Any], sat: Dict[str, Any], hucre: str, B: Optional[int] = None) -> Dict[str, Any]:
    pop, uc = yo_satir_maske(H, K, sat, hucre); s = H["s"]
    ek = {"Y5_uc": s.Y5.to_numpy(float), "KALICI_uc": s.KALICI.to_numpy(float), "R15_uc": s.R15.to_numpy(float),
          "SECIM": (s.R15 - s.P15).to_numpy(float)}
    o = yo_olc(uc[pop], H["q"][pop], s.Y10.to_numpy(float)[pop], s.D10.to_numpy(float)[pop], H["TF"][pop], H["ay"][pop], f"{sat['ad']}|{hucre}", B,
               {a: v[pop] for a, v in ek.items()})
    o["pay"] = float(uc[pop].mean()) if pop.any() else None
    if uc.any():
        o["R15_medyan"] = float(np.median(s.R15.to_numpy(float)[uc]))
    qp = H["qp"]; okp = pop & (qp >= 0)
    kp = yo_olc(uc[okp], qp[okp], s.Y10.to_numpy(float)[okp], s.D10.to_numpy(float)[okp], H["TF"][okp], H["ay"][okp], f"{sat['ad']}|{hucre}|puan", B)
    o["KAT_PUAN"] = kp.get("KAT"); o["KAT_PUAN_alt"] = kp.get("KAT_alt"); o["KAT_PUAN_ust"] = kp.get("KAT_ust")
    return o


def yo_taban(X: pd.DataFrame, S: pd.DataFrame, K: Dict[str, Any], hucre: str) -> Dict[str, Any]:
    """Hücrede Y10 / Y5 / D10 taban oranları ve ATRP beşliklerine göre Y10 / D10."""
    m = (X.hucre == hucre).to_numpy(); x = X[m]; s = S[m]; q = yo_besli(x.ATRP20.to_numpy(float), K["atrp_besli"][yo_hucre_esik(K, hucre)])
    out = {"n": int(m.sum()), "Y10": float(s.Y10.mean()), "Y5": float(s.Y5.mean()), "D10": float(s.D10.mean()), "R15_ort": float(s.R15.mean()),
           "KALICI": float(np.nanmean(s.KALICI.to_numpy(float))), "besli": []}
    for i in range(5):
        b = q == i
        out["besli"].append({"q": i + 1, "n": int(b.sum()), "Y10": float(s.Y10[b].mean()) if b.any() else None, "D10": float(s.D10[b].mean()) if b.any() else None})
    return out


def yo_piyasa_olc(g: pd.DataFrame, s: pd.DataFrame, ad: str, yon: str, esik: float, hucre: str, B: Optional[int] = None) -> Dict[str, Any]:
    v = g[ad].to_numpy(float); f = np.isfinite(v) & np.isfinite(s.P15.to_numpy(float))
    with np.errstate(invalid="ignore"):
        uc = ((v >= esik) if yon == "BÜYÜK" else (v <= esik)) & f
    yp = s.YP.to_numpy(float)[f]; dp = s.DP.to_numpy(float)[f]; p15 = s.P15.to_numpy(float)[f]; u = uc[f]; ay = g.ay.to_numpy(str)[f]
    out: Dict[str, Any] = {"n": int(u.sum()), "N": int(f.sum())}
    ao = HV.hv25_ay_ozet([f"{a}-01" for a in ay[u]]) if u.any() else {"ay": 0, "ust3_pay": None, "ust3": []}
    out.update({"ay": ao["ay"], "ust3_pay": ao["ust3_pay"]})
    if u.sum() < 2:
        return out
    out.update({"P_YP_uc": float(yp[u].mean()), "P_DP_uc": float(dp[u].mean()), "P_YP": float(yp.mean()), "P_DP": float(dp.mean()),
                "P15_uc": float(p15[u].mean()), "P15_taban": float(p15.mean())})
    out["KAT"] = out["P_YP_uc"] / out["P_YP"] if out["P_YP"] > 0 else None
    out["ASIMETRI"] = (out["P_YP_uc"] - out["P_DP_uc"]) - (out["P_YP"] - out["P_DP"]); out["P15_FARK"] = out["P15_uc"] - out["P15_taban"]
    k, W = yo_ay_W(ay, f"piyasa|{ad}|{hucre}", B); K = W.shape[1]; bc = lambda w: np.bincount(k, weights=w, minlength=K)  # noqa: E731
    with np.errstate(invalid="ignore", divide="ignore"):
        nu = W @ bc(u.astype(float)); na = W @ bc(np.ones(len(u)))
        pyu = (W @ bc(yp * u)) / nu; pdu = (W @ bc(dp * u)) / nu; py = (W @ bc(yp)) / na; pd_ = (W @ bc(dp)) / na
        kat = pyu / py; asm = (pyu - pdu) - (py - pd_); pf = (W @ bc(p15 * u)) / nu - (W @ bc(p15)) / na
    for a_, v_ in (("KAT", kat), ("ASIMETRI", asm), ("P15_FARK", pf)):
        lo, hi = _q(v_); out[f"{a_}_alt"] = lo; out[f"{a_}_ust"] = hi
    kv = kat[np.isfinite(kat)]; out["p"] = float((1 + (kv <= 1).sum()) / (len(kv) + 1)) if len(kv) else None
    return out


def yo_kapi(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    """Ön kayıt kapısı: kontrol listesi + mühürler + commit + temiz ağaç + panel sha + sayım sha + KASA."""
    import IZ_KARNE as IK
    import KASA as KS
    cikti = cikti or YO_YOL["cikti"]; yol = _yo_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise YOHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    bek = {"YO_KOD_SHA": yo_kod_sha(), "YO_ESIK_SHA": yo_esik_sha(), **{f"DOSYA_{a}": v for a, v in yo_dosya_sha(ham).items()}}
    for a, v in bek.items():
        if f"{a}: {v}" not in metin:
            raise YOHata(f"ön kayıt kapısı: {a} farklı -> DURDU")
    S = yo_sayim_kos(ham)
    if f"SAYIM_SHA: {HV.hv_json_sha(S)}" not in metin:
        raise YOHata("getirisiz sayım ön kayıttakiyle aynı değil -> DURDU")
    rel = os.path.relpath(yol, KOK_YO); c = _yo_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise YOHata("ön kayıt commit'li değil -> DURDU")
    if _yo_git(["status", "--porcelain", "--", rel, "YUKSELIS_ONCESI.py"]):
        raise YOHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    try:
        kasa = KS.kasa_kapisi([os.path.join(YO_YOL["acik"], f"V_{p}.pkl") for p in YO_PAZAR], "2022-12-31")
    except KS.KasaHata as ex:
        raise YOHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, "kasa": kasa, **bek}


def yo_adim1_hesap(X: pd.DataFrame, S: pd.DataFrame, G: pd.DataFrame, Sg: pd.DataFrame, XA: pd.DataFrame, GA: pd.DataFrame,
                   B: Optional[int] = None) -> Dict[str, Any]:
    """ADIM 1: X / S / G / Sg yalnız keşif (ABD 2016-19); XA / GA = AVR 2016-19 ÖZELLİKLERİ (getirisiz; yalnız yüzdelik değerleri için)."""
    if set(X.hucre.unique()) != {YO_KESIF} or set(G.hucre.unique()) != {YO_KESIF}:
        raise YOHata("SIRA: ADIM 1 girdisi yalnız keşif")
    if set(XA.hucre.unique()) != {"AVR|d1619"} or set(GA.hucre.unique()) != {"AVR|d1619"}:
        raise YOHata("SIRA: AVR yüzdelik dağılımı yalnız AVR 2016-19 özelliklerinden")
    if any(c in XA.columns for c in ("Y10", "R15", "P15")) or any(c in GA.columns for c in ("YP", "P15")):
        raise YOHata("SIRA: AVR girdisinde sonuç sütunu var")
    K: Dict[str, Any] = {"surum": YO_SURUM, "esik_sha": yo_esik_sha()}
    bq = YO_ESIK["kesim"]["besli"]
    K["atrp_besli"] = {"ABD": [float(x) for x in np.quantile(X.ATRP20.dropna(), bq)], "AVR": [float(x) for x in np.quantile(XA.ATRP20.dropna(), bq)]}
    q = yo_besli(X.ATRP20.to_numpy(float), K["atrp_besli"]["ABD"]); Y = S.Y10.to_numpy(float)
    ev, ct = yo_esle(X.t_row.to_numpy(), q, Y)
    K["esle"] = {"olay": int(len(ev)), "kontrol": int((ct >= 0).sum()), "olay_toplam_Y10": int(Y.sum()), "eksik_kontrol_olay": int((ct < 0).any(1).sum())}
    ay_ev = X.ay.to_numpy(str)[ev]
    K["adim1"] = {}; K["yon"] = {}
    for c in YO_OZ:
        r = yo_smd_auc(X[c].to_numpy(float), ev, ct, ay_ev, f"adim1|{c}", B); K["adim1"][c] = r
        smd = r.get("SMD")
        K["yon"][c] = {"yon": "KÜÇÜK" if (smd is not None and np.isfinite(smd) and smd < 0) else "BÜYÜK",
                       "not": "" if (smd is not None and np.isfinite(smd) and smd != 0) else "SMD yok / 0 -> BÜYÜK"}
    K["sira"] = sorted(YO_OZ, key=lambda c: -abs(K["adim1"][c].get("SMD") or 0.0))
    K["kesim"] = {"ABD": {}, "AVR": {}}
    for c in YO_OZ:
        K["kesim"]["ABD"][c] = yo_kesim_belirle(X, c, K["yon"][c]["yon"])
        if c not in YO_BAYRAK:
            va = XA[c].to_numpy(float); va = va[np.isfinite(va)]
            K["kesim"]["AVR"][c] = {f"{u:.2f}": float(np.quantile(va, 1 - u if K["yon"][c]["yon"] == "BÜYÜK" else u)) for u in YO_ESIK["kesim"]["uc"]}
        else:
            K["kesim"]["AVR"][c] = {"bayrak": True}
    # kontrol modeli (lojistik)
    ks = ["MOM_12_1", "F15", "KONUM120", "ATRP20"]
    ort = {c: float(np.nanmean(X[c].to_numpy(float))) for c in ks}; sd = {c: float(np.nanstd(X[c].to_numpy(float))) for c in ks}
    w = yo_logit_newton(yo_tasarim(X, ks, ort, sd), Y)
    pk = yo_tasarim(X, ks, ort, sd) @ w; pa = yo_tasarim(XA, ks, ort, sd) @ w
    K["kontrol_model"] = {"sutun": ks, "ort": ort, "sd": sd, "w": [float(v) for v in w],
                          "besli": {"ABD": [float(v) for v in np.quantile(pk, bq)], "AVR": [float(v) for v in np.quantile(pa, bq)]}}
    # basit puan (L1)
    ort2 = {c: float(np.nanmean(X[c].to_numpy(float))) for c in YO_OZ}; sd2 = {c: float(np.nanstd(X[c].to_numpy(float))) for c in YO_OZ}
    w2 = yo_logit_l1(yo_tasarim(X, YO_OZ, ort2, sd2), Y, float(YO_ESIK["puan"]["L1_lambda"]), int(YO_ESIK["puan"]["iter"]))
    sk = yo_tasarim(X, YO_OZ, ort2, sd2) @ w2; sa = yo_tasarim(XA, YO_OZ, ort2, sd2) @ w2
    K["puan"] = {"sutun": YO_OZ, "ort": ort2, "sd": sd2, "w": [float(v) for v in w2],
                 "kesim": {"ABD": {f"{u:.2f}": float(np.quantile(sk, 1 - u)) for u in YO_ESIK["kesim"]["uc"]},
                           "AVR": {f"{u:.2f}": float(np.quantile(sa, 1 - u)) for u in YO_ESIK["kesim"]["uc"]}}}
    # keşif taban oranları + keşif satır ölçüleri (birleşim adayları için)
    K["taban_kesif"] = yo_taban(X, S, K, YO_KESIF)
    H = yo_hucre_kur(X, S, K, YO_KESIF); K["kesif_olc"] = {}
    for sat in yo_satirlar(K):
        K["kesif_olc"][sat["ad"]] = yo_satir_olc(H, K, sat, YO_KESIF, B)
    nmin, amin = int(YO_ESIK["hukum"]["n_min"]), int(YO_ESIK["hukum"]["ay_min"])
    def gecer(o):
        return (o.get("n", 0) >= nmin and o.get("ay", 0) >= amin and (o.get("KAT_alt") or 0) > 1 and (o.get("ASIMETRI_alt") or -1) > 0
                and (o.get("TOPLAM_FARK_alt") or -1) > 0)
    aday = []
    for c in YO_OZ:
        a = f"{c}|BAYRAK" if c in YO_BAYRAK else f"{c}|0.10"
        if gecer(K["kesif_olc"][a]):
            aday.append(c)
    K["birlesim"] = {"aday": aday, "secilen": None, "denenen": []}
    if len(aday) >= 2:
        best = None
        for i in range(len(aday)):
            for jx in range(i + 1, len(aday)):
                u1 = "BAYRAK" if aday[i] in YO_BAYRAK else "0.10"; u2 = "BAYRAK" if aday[jx] in YO_BAYRAK else "0.10"
                sat = {"ad": f"BIRLESIM|{aday[i]}+{aday[jx]}", "tur": "birlesim", "uye": [[aday[i], u1], [aday[jx], u2]], "yon": "BÜYÜK", "uc": "KESISIM"}
                pop, uc = yo_satir_maske(H, K, sat, YO_KESIF)
                n_ = int(uc.sum())
                if n_ < nmin:
                    K["birlesim"]["denenen"].append({"ad": sat["ad"], "n": n_}); continue
                o = yo_olc(uc[pop], H["q"][pop], H["s"].Y10.to_numpy(float)[pop], H["s"].D10.to_numpy(float)[pop], H["TF"][pop], H["ay"][pop], sat["ad"], 200)
                K["birlesim"]["denenen"].append({"ad": sat["ad"], "n": n_, "KAT": o.get("KAT")})
                if o.get("KAT") is not None and (best is None or o["KAT"] > best[0]):
                    best = (o["KAT"], sat)
        if best is not None:
            K["birlesim"]["secilen"] = best[1]
    # piyasa
    K["piyasa"] = {"adim1": {}, "yon": {}, "kesim": {"ABD": {}, "AVR": {}}}
    ypv = Sg.YP.to_numpy(float)
    K["piyasa"]["taban_kesif"] = {"gun": int(np.isfinite(ypv).sum()), "YP": float(np.nanmean(ypv)), "DP": float(np.nanmean(Sg.DP.to_numpy(float))),
                                  "P15_ort": float(np.nanmean(Sg.P15.to_numpy(float)))}
    for c in YO_PIYASA_OZ:
        r = yo_smd_auc_esiz(G[c].to_numpy(float), ypv, G.ay.to_numpy(str), f"adim1p|{c}", B); K["piyasa"]["adim1"][c] = r
        smd = r.get("SMD"); y = "KÜÇÜK" if (smd is not None and np.isfinite(smd) and smd < 0) else "BÜYÜK"; K["piyasa"]["yon"][c] = y
        for ek, GG in (("ABD", G), ("AVR", GA)):
            v = GG[c].to_numpy(float); v = v[np.isfinite(v)]
            K["piyasa"]["kesim"][ek][c] = {f"{u:.2f}": float(np.quantile(v, 1 - u if y == "BÜYÜK" else u)) for u in YO_ESIK["kesim"]["uc"]}
    K["piyasa"]["sira"] = sorted(YO_PIYASA_OZ, key=lambda c: -abs(K["piyasa"]["adim1"][c].get("SMD") or 0.0))
    K["piyasa"]["kesif_olc"] = {}
    for c in YO_PIYASA_OZ:
        for u in YO_ESIK["kesim"]["uc"]:
            K["piyasa"]["kesif_olc"][f"{c}|{u:.2f}"] = yo_piyasa_olc(G, Sg, c, K["piyasa"]["yon"][c], K["piyasa"]["kesim"]["ABD"][c][f"{u:.2f}"], YO_KESIF, B)
    return K


def yo_adim1(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or YO_YOL["cikti"]
    if os.path.exists(_yo_yol("kesim", cikti)):
        raise YOHata("yo_kesim.json zaten var (ADIM 1 ikinci kez koşmaz)")
    G0 = yo_kapi(cikti, ham)
    X, G = yo_yukle("ABD", ham); XA, GA = yo_yukle("AVR", ham)
    Xk = X[X.hucre == YO_KESIF].reset_index(drop=True); Gk = G[G.hucre == YO_KESIF].reset_index(drop=True)
    XA = XA[XA.hucre == "AVR|d1619"].reset_index(drop=True); GA = GA[GA.hucre == "AVR|d1619"].reset_index(drop=True)
    del X, G; gc.collect()
    S, Sg = yo_sonuc("ABD", Xk, Gk, "adim1", ham)
    K = yo_adim1_hesap(Xk, S, Gk, Sg, XA, GA)
    K["kapi"] = G0; K["zaman"] = pd.Timestamp.utcnow().isoformat()
    MI._mi_jyaz(_yo_yol("kesim", cikti), K, "kesim")
    MI._mi_yaz(_yo_yol("kesim_md", cikti), yo_kesim_md(K, MI._mi_sha(_yo_yol("kesim", cikti))), "kesim md")
    return K


# ================================================================ 8) ADIM 2 (doğrulama; bir kez)
def yo_kesim_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or YO_YOL["cikti"]; yj = _yo_yol("kesim", cikti); ym = _yo_yol("kesim_md", cikti)
    if not (os.path.exists(yj) and os.path.exists(ym)):
        raise YOHata("SIRA: yo_kesim.json / YO_KESIM.md yok (ADIM 1 önce)")
    sha = MI._mi_sha(yj)
    if f"KESIM_SHA: {sha}" not in open(ym, encoding="utf-8").read():
        raise YOHata("YO_KESIM.md kesim sha'sı uyuşmuyor -> DURDU")
    out = {"KESIM_SHA": sha}
    for f in (yj, ym):
        rel = os.path.relpath(f, KOK_YO); c = _yo_git(["log", "-1", "--format=%H %cI", "--", rel])
        if not c:
            raise YOHata(f"SIRA: {os.path.basename(f)} commit'li değil -> DURDU")
        if _yo_git(["status", "--porcelain", "--", rel]):
            raise YOHata(f"{os.path.basename(f)} çalışma ağacında değişmiş -> DURDU")
        out[os.path.basename(f)] = c
    return out


def yo_hukum(o: Dict[str, Dict[str, Any]], bh_gecti: bool) -> str:
    """Satır hükmü (YO_ESIK['hukum']); o: hücre -> ölçü."""
    nmin, amin = int(YO_ESIK["hukum"]["n_min"]), int(YO_ESIK["hukum"]["ay_min"])
    k, d = o.get(YO_KESIF, {}), o.get("ABD|d2022", {})
    if any(x.get("n", 0) < nmin or x.get("ay", 0) < amin for x in (k, d)):
        return "ÖLÇÜLEMEDİ"
    def uc_sart(x):
        return (x.get("KAT_alt") or 0) > 1 and (x.get("ASIMETRI_alt") or -1) > 0 and (x.get("TOPLAM_FARK_alt") or -1) > 0
    def avr_isaret(x):
        return x.get("n", 0) >= 30 and (x.get("KAT") or 0) > 1 and (x.get("ASIMETRI") or -1) > 0 and (x.get("TOPLAM_FARK") or -1) > 0
    ik = uc_sart(k), uc_sart(d)
    if all(ik) and bh_gecti and all(avr_isaret(o.get(h, {})) for h in ("AVR|d1619", "AVR|d2022")):
        return "TUTAR"
    if (k.get("KAT_HAM_alt") or 0) > 1 and (d.get("KAT_HAM_alt") or 0) > 1 and \
            any((x.get("KAT_alt") or 0) <= 1 or (x.get("ASIMETRI") or 0) <= 0 for x in (k, d)):
        return "YALNIZ OYNAKLIK"
    if sum(ik) == 1:
        return "TEK DÖNEM"
    if (d.get("KAT_ust") is not None and d["KAT_ust"] < 1) and (d.get("ASIMETRI_ust") is not None and d["ASIMETRI_ust"] < 0):
        return "TERS"
    return "TUTMADI"


def yo_piyasa_hukum(o: Dict[str, Dict[str, Any]], bh_gecti: bool) -> str:
    mn = int(YO_ESIK["piyasa"]["kume_en_az"]); amin = int(YO_ESIK["hukum"]["ay_min"])
    k, d = o.get(YO_KESIF, {}), o.get("ABD|d2022", {})
    if any(x.get("n", 0) < mn or x.get("ay", 0) < amin for x in (k, d)):
        return "ÖLÇÜLEMEDİ"
    def sart(x):
        return (x.get("KAT_alt") or 0) > 1 and (x.get("ASIMETRI_alt") or -1) > 0 and (x.get("P15_FARK_alt") or -1) > 0
    def avr(x):
        return x.get("n", 0) >= 10 and (x.get("KAT") or 0) > 1 and (x.get("ASIMETRI") or -1) > 0 and (x.get("P15_FARK") or -1) > 0
    ik = sart(k), sart(d)
    if all(ik) and bh_gecti and all(avr(o.get(h, {})) for h in ("AVR|d1619", "AVR|d2022")):
        return "TUTAR"
    if sum(ik) == 1:
        return "TEK DÖNEM"
    if (d.get("KAT_ust") is not None and d["KAT_ust"] < 1) and (d.get("ASIMETRI_ust") is not None and d["ASIMETRI_ust"] < 0):
        return "TERS"
    return "TUTMADI"


def yo_adim2_hesap(XS: Dict[str, pd.DataFrame], SS: Dict[str, pd.DataFrame], GS: Dict[str, pd.DataFrame], SG: Dict[str, pd.DataFrame],
                   K: Dict[str, Any], B: Optional[int] = None) -> Dict[str, Any]:
    J: Dict[str, Any] = {"taban": {}, "satir": {}, "piyasa": {}, "birlesim": None, "puan": {}}
    Hc: Dict[str, Dict[str, Any]] = {}
    for h in YO_HUCRE:
        p = h.split("|")[0]; X, S = XS[p], SS[p]
        J["taban"][h] = yo_taban(X, S, K, h); Hc[h] = yo_hucre_kur(X, S, K, h)
    satirlar = yo_satirlar(K)
    for sat in satirlar:
        J["satir"][sat["ad"]] = {"ozellik": sat["ozellik"], "uc": sat["uc"], "yon": sat["yon"], "aile": YO_AILE[sat["ozellik"]],
                                 "olc": {h: yo_satir_olc(Hc[h], K, sat, h, B) for h in YO_HUCRE}}
    # keşif yeniden üretim (ADIM 1 ile aynı olmalı)
    fark = []
    for a, r in J["satir"].items():
        k1, k2 = K["kesif_olc"][a], r["olc"][YO_KESIF]
        for f in ("n", "KAT", "ASIMETRI", "TOPLAM_FARK", "KAT_alt"):
            v1, v2 = k1.get(f), k2.get(f)
            if (v1 is None) != (v2 is None) or (v1 is not None and abs(float(v1) - float(v2)) > 1e-9):
                fark.append((a, f, v1, v2))
    if fark:
        raise YOHata(f"K11: keşif satırları ADIM 1 ile aynı değil: {fark[:3]}")
    ad = list(J["satir"]); bh = yo_bh([J["satir"][a]["olc"]["ABD|d2022"].get("p") for a in ad], float(YO_ESIK["bh"]["q"]))
    for a, b in zip(ad, bh):
        r = J["satir"][a]; r["bh_q"] = b; r["bh_gecti"] = bool(b is not None and b <= float(YO_ESIK["bh"]["q"]))
        r["hukum"] = yo_hukum(r["olc"], r["bh_gecti"])
        if r["hukum"] == "TUTAR":
            d = r["olc"]["ABD|d2022"]
            r["kontrol"] = "KONTROLÜ GEÇER" if (d.get("KAT_PUAN") or 0) > 1 and (d.get("KAT_PUAN_alt") or 0) > 1 else "BİLİNENİN TEKRARI"
        else:
            r["kontrol"] = ""
    # birleşim ve puan
    tek_en_iyi = {}
    for u in ("0.10", "0.02"):
        cand = [(r["olc"]["ABD|d2022"].get("KAT") or 0, a) for a, r in J["satir"].items() if r["uc"] in (u, "BAYRAK")]
        tek_en_iyi[u] = max(cand)[1] if cand else None
    J["tek_en_iyi"] = tek_en_iyi
    if K["birlesim"].get("secilen"):
        sat = K["birlesim"]["secilen"]; o = {h: yo_satir_olc(Hc[h], K, sat, h, B) for h in YO_HUCRE}
        p = o["ABD|d2022"].get("p"); hk = yo_hukum(o, bool(p is not None and p <= float(YO_ESIK["bh"]["q"])))
        en = J["satir"][tek_en_iyi["0.10"]]["olc"]["ABD|d2022"].get("KAT") if tek_en_iyi["0.10"] else None
        J["birlesim"] = {"sat": sat, "olc": o, "hukum": hk, "en_iyi_tek": tek_en_iyi["0.10"], "en_iyi_tek_KAT": en,
                         "gecti": bool(hk == "TUTAR" and en is not None and (o["ABD|d2022"].get("KAT") or 0) > en)}
    for u in ("0.10", "0.02"):
        sat = {"ad": f"PUAN|{u}", "tur": "puan", "uc": u, "yon": "BÜYÜK", "ozellik": "PUAN"}
        o = {h: yo_satir_olc(Hc[h], K, sat, h, B) for h in YO_HUCRE}
        p = o["ABD|d2022"].get("p"); hk = yo_hukum(o, bool(p is not None and p <= float(YO_ESIK["bh"]["q"])))
        en = J["satir"][tek_en_iyi[u]]["olc"]["ABD|d2022"].get("KAT") if tek_en_iyi[u] else None
        J["puan"][u] = {"olc": o, "hukum": hk, "en_iyi_tek": tek_en_iyi[u], "en_iyi_tek_KAT": en,
                        "gecti": bool(hk == "TUTAR" and en is not None and (o["ABD|d2022"].get("KAT") or 0) > en)}
    # piyasa
    J["piyasa_taban"] = {}
    for h in YO_HUCRE:
        p = h.split("|")[0]; m = (GS[p].hucre == h).to_numpy(); s = SG[p][m]
        J["piyasa_taban"][h] = {"gun": int(np.isfinite(s.P15.to_numpy(float)).sum()), "YP": float(np.nanmean(s.YP)), "DP": float(np.nanmean(s.DP)),
                                "P15_ort": float(np.nanmean(s.P15))}
    for c in YO_PIYASA_OZ:
        y = K["piyasa"]["yon"][c]
        for u in YO_ESIK["kesim"]["uc"]:
            a = f"{c}|{u:.2f}"; o = {}
            for h in YO_HUCRE:
                p = h.split("|")[0]; m = (GS[p].hucre == h).to_numpy()
                o[h] = yo_piyasa_olc(GS[p][m].reset_index(drop=True), SG[p][m].reset_index(drop=True), c, y, K["piyasa"]["kesim"][yo_hucre_esik(K, h)][c][f"{u:.2f}"], h, B)
            J["piyasa"][a] = {"ozellik": c, "uc": f"{u:.2f}", "yon": y, "olc": o}
    pa = list(J["piyasa"]); pbh = yo_bh([J["piyasa"][a]["olc"]["ABD|d2022"].get("p") for a in pa], float(YO_ESIK["bh"]["q"]))
    for a, b in zip(pa, pbh):
        r = J["piyasa"][a]; r["bh_q"] = b; r["bh_gecti"] = bool(b is not None and b <= float(YO_ESIK["bh"]["q"]))
        r["hukum"] = yo_piyasa_hukum(r["olc"], r["bh_gecti"])
    tut = [a for a, r in J["satir"].items() if r["hukum"] == "TUTAR" and r["kontrol"] == "KONTROLÜ GEÇER"]
    J["genel"] = {"hukum": "AÇIK VERİDE ADAY (kasa açılmaz; KASA KURALI: tek iz kasa açmaz; ileri test)" if tut else
                  "YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde)", "tutar_kontrol": tut,
                  "tutar": [a for a, r in J["satir"].items() if r["hukum"] == "TUTAR"],
                  "piyasa_tutar": [a for a, r in J["piyasa"].items() if r["hukum"] == "TUTAR"]}
    # en yakın üç satır (TUTAR olmayan; ABD 2020-22 KAT alt ucunun ve ASİMETRİ alt ucunun en küçüğü en büyük olanlar)
    def yakin(r):
        d, k = r["olc"]["ABD|d2022"], r["olc"][YO_KESIF]
        return min((d.get("KAT_alt") or 0) - 1, (k.get("KAT_alt") or 0) - 1, (d.get("ASIMETRI_alt") or -1) * 10, (k.get("ASIMETRI_alt") or -1) * 10,
                   (d.get("TOPLAM_FARK_alt") or -1) * 10, (k.get("TOPLAM_FARK_alt") or -1) * 10)
    J["en_yakin"] = [a for a in sorted([a for a, r in J["satir"].items() if r["hukum"] != "TUTAR"], key=lambda a: -yakin(J["satir"][a]))[:3]]
    return J


def yo_adim2(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    t0 = time.time(); cikti = cikti or YO_YOL["cikti"]
    if os.path.exists(_yo_yol("sonuc", cikti)):
        raise YOHata("sonuç zaten var (ADIM 2 ikinci kez koşmaz)")
    G0 = yo_kapi(cikti, ham); G1 = yo_kesim_kapi(cikti)
    K = json.load(open(_yo_yol("kesim", cikti), encoding="utf-8"))
    if K.get("esik_sha") != yo_esik_sha():
        raise YOHata("kesim dosyasının eşik sha'sı farklı -> DURDU")
    XS, SS, GS, SG = {}, {}, {}, {}
    for p in YO_PAZAR:
        X, G = yo_yukle(p, ham)
        X = X[X.hucre.isin(YO_HUCRE)].reset_index(drop=True); G = G[G.hucre.isin(YO_HUCRE)].reset_index(drop=True)
        S, Sg = yo_sonuc(p, X, G, "adim2", ham); XS[p], SS[p], GS[p], SG[p] = X, S, G, Sg; gc.collect()
    J = yo_adim2_hesap(XS, SS, GS, SG, K)
    J.update({"surum": YO_SURUM, "kapi": G0, "kesim_kapi": G1, "sure_sn": round(time.time() - t0), "dosya_sha": yo_dosya_sha(ham),
              "kesim_sha": G1["KESIM_SHA"], "ham_yol": YO_YOL["ham"]})
    MI._mi_jyaz(_yo_yol("sonuc", cikti), J, "sonuç")
    yo_ozet_csv(J, K, _yo_yol("ozet", cikti))
    # yeniden üretim için satır dosyası (repo dışı)
    for p in YO_PAZAR:
        A = pd.concat([XS[p][["pazar", "sembol", "j", "k", "tarih", "giris", "hucre", "ay"] + YO_OZ], SS[p]], axis=1)
        A.to_pickle(_yo_ham(f"satir_{p}.pkl", ham), protocol=4)
        pd.concat([GS[p], SG[p]], axis=1).to_pickle(_yo_ham(f"piyasa_satir_{p}.pkl", ham), protocol=4)
    return J


def yo_ozet_csv(J: Dict[str, Any], K: Dict[str, Any], yol: str) -> str:
    rows = []
    def ekle(tur, a, ozellik, uc, yon, olc, hukum, kontrol="", bh=None):
        for h, o in olc.items():
            rows.append({"tur": tur, "satir": a, "ozellik": ozellik, "uc": uc, "yon": yon, "hucre": h, "hukum": hukum, "kontrol": kontrol, "bh_q": bh,
                         **{k: v for k, v in o.items() if not isinstance(v, (list, dict))}})
    for a, r in J["satir"].items():
        ekle("hisse", a, r["ozellik"], r["uc"], r["yon"], r["olc"], r["hukum"], r["kontrol"], r["bh_q"])
    if J.get("birlesim"):
        ekle("birlesim", J["birlesim"]["sat"]["ad"], "BIRLESIM", "KESISIM", "BÜYÜK", J["birlesim"]["olc"], J["birlesim"]["hukum"])
    for u, r in J["puan"].items():
        ekle("puan", f"PUAN|{u}", "PUAN", u, "BÜYÜK", r["olc"], r["hukum"])
    for a, r in J["piyasa"].items():
        ekle("piyasa", a, r["ozellik"], r["uc"], r["yon"], r["olc"], r["hukum"], "", r["bh_q"])
    D = pd.DataFrame(rows); MI.mi_sizinti(D.to_csv(index=False), "özet csv"); D.to_csv(yol, index=False, float_format="%.6f")
    return yol


# ================================================================ 9) ÖN KAYIT / KESİM / RAPOR METİNLERİ
def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "-"
    v = float(x) * (100 if yuzde else 1)
    return f"{v:.{n}f}".replace(".", ",")


def yo_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or YO_YOL["cikti"]; S = yo_sayim_kos(ham); ds = yo_dosya_sha(ham)
    L = [f"# YO ÖN KAYIT — yükseliş trendinden önce hangi bölge var: geriye bakış (keşif) + ileriye doğru sınama ({pd.Timestamp.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')})",
         "", "İş tanımı YO_IS_TANIMI.md (ana model). Bu dosya Y10 / Y5 / D10 / R15 / P15 HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, "
         "eşikler, okuma ve hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (yukarı yanlı, iki taraf için de). KASA açılmaz (veri <= 2022-12-31). "
         "HACİM KULLANILMAZ (P2 likidite süzgeci dışında).", "", "## Mühürler", "",
         f"YO_KOD_SHA: {yo_kod_sha()}", f"YO_ESIK_SHA: {yo_esik_sha()}"]
    L += [f"DOSYA_{a}: {v}" for a, v in ds.items()]
    L += [f"SAYIM_SHA: {HV.hv_json_sha(S)}", f"IS_TANIMI_SHA: {MI._mi_sha(YO_YOL['is_tanimi'])}", "",
          f"- Panel dosyaları (repo dışı): {YO_YOL['ham']} (ozellik_*.pkl = örnek satırları + özellikler, piyasa_*.pkl = pazar-gün özellikleri, ham_*.npz = "
          "sonuç için bar deposu; sonuç sütunu YOK)", "", "## GETİRİSİZ SAYIM (Y / R15 / P15 hesaplanmadı)", "",
          "| hücre | hisse-gün | farklı ay | en kalabalık 3 ay payı | hisse | pazar-gün | ay (pazar-gün) |", "|---|---|---|---|---|---|---|"]
    for h in YO_HUCRE:
        a = S["hisse"].get(h, {}); b = S["piyasa"].get(h, {})
        L.append(f"| {h} | {a.get('hisse_gun', 0)} | {a.get('ay', 0)} | {_f(a.get('ust3_pay'), 3)} | {a.get('hisse', 0)} | {b.get('gun', 0)} | {b.get('ay', 0)} |")
    L += ["", "### Özelliklerin eksik payı (%) ve dağılımı (ABD 2016-19: %2 / %10 / %50 / %90 / %98 yüzdelikleri)", "",
          "| özellik | aile | eksik ABD 16-19 | eksik ABD 20-22 | eksik AVR 16-19 | eksik AVR 20-22 | %2 | %10 | %50 | %90 | %98 |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in YO_OZ:
        e = [_f(S["hisse"].get(h, {}).get("ozellik", {}).get(c, {}).get("eksik"), 1, True) for h in YO_HUCRE]
        q = S["hisse"].get(YO_KESIF, {}).get("ozellik", {}).get(c, {}).get("q", [])
        qq = [_f(q[i], 4) if q else "-" for i in (1, 2, 4, 6, 7)]
        L.append(f"| {c} | {YO_AILE[c]} | " + " | ".join(e) + " | " + " | ".join(qq) + " |")
    L += ["", "### Piyasa özelliklerinin eksik payı (%)", "", "| özellik | ABD 16-19 | ABD 20-22 | AVR 16-19 | AVR 20-22 |", "|---|---|---|---|---|"]
    for c in YO_PIYASA_OZ:
        L.append(f"| {c} | " + " | ".join(_f(S["piyasa"].get(h, {}).get("ozellik", {}).get(c, {}).get("eksik"), 1, True) for h in YO_HUCRE) + " |")
    L += ["", "### Özellikler arası sıra ilişkisi (Spearman; ABD 2016-19)", "", "| | " + " | ".join(f"{i + 1}" for i in range(len(YO_OZ))) + " |",
          "|---|" + "---|" * len(YO_OZ)]
    M = S["spearman"].get(YO_KESIF, [])
    for i, c in enumerate(YO_OZ):
        L.append(f"| {i + 1} {c} | " + " | ".join(_f(M[i][jx], 2) if M else "-" for jx in range(len(YO_OZ))) + " |")
    yuksek = [(YO_OZ[i], YO_OZ[jx], M[i][jx]) for i in range(len(YO_OZ)) for jx in range(i + 1, len(YO_OZ)) if M and M[i][jx] is not None and abs(M[i][jx]) >= 0.7]
    L += ["", "- |rho| >= 0,70 olan çiftler: " + ("; ".join(f"{a} - {b} {_f(v, 2)}" for a, b, v in yuksek) if yuksek else "yok"),
          "", "## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)", ""]
    L += [f"{i + 1}. {t}" for i, t in enumerate(YO_YORUM)]
    L += ["", "## Tanımlar (YO_ESIK; sha yukarıda)", "", "```", json.dumps(YO_ESIK, ensure_ascii=False, indent=1), "```", "", "## KONTROL LİSTESİ", "",
          "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    ad = {k["kod"]: k.get("ad", k.get("baslik", "")) for k in IK.IK_KONTROL}
    for k, (y, kn) in YO_KONTROL.items():
        L.append(f"| {k} | {ad.get(k, '')} | {y} | {kn} |")
    L += ["", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(_yo_yol("onkayit", cikti), "\n".join(L), "ön kayıt")


YO_YORUM = [
    "Birim hisse-gün t = hissenin kendi geçerli bar indeksi k, k % 5 == 0 (0'dan); t takvim satırı değil, hissenin barıdır. Giriş = k + 1 barının açılışı; "
    "15 geçerli bar giriş barı dahil (k + 1 .. k + 15; MUM_IZI_GOZ.gz_olc_bir gibi giriş barının High / Low'u sayılır).",
    "Aynı barda hedef ve stop: STOP ÖNCE (Y10 / Y5 = 0; D10 aynasında da 'stop' = +%5 önce, D10 = 0). Bu kötümser kural iki yönde aynıdır; ASİMETRİ'de iki taraf da "
    "aynı kuralla sayılır.",
    "Evren = giriş barı satırında TEZGÂH 2 P2 (KART_TUR2.k2_panel; MUM_IZI_HAKEM / MH.mh_p2 ile aynı 'giriş günü' üyeliği). BIST'te P2 yok: BIST hesaplanmaz "
    "(iş tanımında yalnız bilgi).",
    "Dönem giriş tarihine göre (HV.hv_hucre_ad). 2016 öncesi giriş yok; özellikler 2015 verisini geçmiş olarak kullanır (veri 2015-01-02'de başlar: MOM_12_1 / "
    "DD_SURE / SMA200 2016 başında eksik olabilir, eksik payı sayımda).",
    "Kontrol özellikleri repodaki tanımlarla: KONUM120 = OLCU_SINAMA._os_atrp_f15 'f15' (repoda adı F15 = 120 barlık konum); iş tanımındaki F15 = '15 barlık geçmiş "
    "getiri' (C_k / C_{k-15} - 1; repoda bu adla başka tanım yok, iş tanımı uygulandı); MOM_12_1 = OLCU_SINAMA kart MOM (C_{k-21} / C_{k-252} - 1; K60'ın aylık "
    "MOM_12_1'inin günlük karşılığı); ATRP20 = UC_IZ2.uc2_ret_atrp formülü (20 bar TR ortalaması / C; OS kovasındaki ATRP14 değil, iş tanımı ATRP20 dedi).",
    "EK 27 ölçüleri (BOY_YUZDE_ORAN, ONCEKI_DUSUS) MUM_IZI27_IS_TANIMI.md 2. bölüm metninden kuruldu (MUM_IZI_UC.py içe alınmadı): pencere = t'de biten 16 bar "
    "(EK 27 E2 'her pencere' genişliği); 'önceki 120 bar' = k-135 .. k-16; ONCEKI_DUSUS = pencere dibi (min Low) / önceki 60 barın (k-75 .. k-16) en yükseği "
    "(maks High) - 1.",
    "RS_DIP ailesi: göreli güç = hisse kapanışı / pazar eşit ağırlıklı endeksi L (P2 kümesi günlük getirilerinden); 'fiyatın 120 barlık konumu' sütunu KONUM120 "
    "kontrolüyle aynı tanım olduğundan ayrı satır yazılmaz; 'birlikte' = RS_DIP_BIR bayrağı. GENISLIK ailesi hisse satırlarında GEN50 ve GEN50_D10; öteki "
    "genişlik düzeyleri piyasa özellikleridir.",
    "MA_DIZI 'sıralama kodu' sıralı tamsayı (0-3) olarak kodlandı; MA_KOD ve RS_DIP_BIR bayrak satırıdır (uç = yönün uç kategorisi; uç %10 / %2 ayrımı yok; "
    "gerçek pay yazılır). Tamsayı özelliklerde (MIKRO, YUKSELEN_DIP, ZIRVE_BAR, DIP_BAR) yüzdelik eşiği eşitleri içerir; uç payı %10'dan büyük olabilir (yazılır).",
    "Yön: ADIM 1'de eşli SMD işareti (> 0 BÜYÜK, < 0 KÜÇÜK); AUC bilgi. Kesimler: ABD 2020-22 keşfin SAYISAL kesimleriyle (gerçek ileri sınama); AVR "
    "hücreleri AVR'nin fiyat ölçeği / oynaklık düzeyi farklı olduğu için aynı yüzdelik DÜZEYLERİNİN AVR 2016-19 ÖZELLİK dağılımındaki değerleriyle (getirisiz; "
    "ADIM 1'de, AVR sonucu görülmeden yo_kesim.json'a yazılır). ATRP beşlik sınırları ve kontrol / basit puan kesimleri de aynı kural.",
    "Popülasyon her satırda özelliği sonlu ve ATRP20 sonlu olan hisse-günler; taban (P(Y10), ATRP beşliği oranları) bu kümeden. TOPLAM FARK için hisse "
    "ortalaması hissenin o hücredeki BÜTÜN örnek günlerinden (özellik eksik olanlar dahil).",
    "Bootstrap kümesi giriş ayı; B = 10.000; tohum 28 (+ satır anahtarı crc32). BH p'si ABD 2020-22 KAT için tek yönlü bootstrap p'si ((1 + #KAT* <= 1) / (B + 1)); "
    "hisse ailesi 40 satır (21 sütun; RS_DIP_BIR ve MA_KOD tek), piyasa ailesi 32 satır ayrı. BİRLEŞİM ve PUAN BH ailesine girmez (tek sınama; p <= 0,10).",
    "Hükümde 'AVR yönü' = AVR 2016-19 ve 2020-22'nin İKİSİNDE (KAT - 1), ASİMETRİ, TOPLAM FARK nokta değerlerinin > 0 olması (n >= 30); aralık aranmaz. "
    "'YALNIZ OYNAKLIK' = ham KAT alt ucu iki ABD döneminde > 1 ama ATRP içi KAT alt ucu <= 1 ya da ASİMETRİ <= 0 (birinde). 'TEK DÖNEM' raporda "
    "'ileriye doğru tutmadı' diye okunur.",
    "Piyasa birimi pazar-gün (her satır; 15 günlük pencereler örtüşür, çıkarım ay kümeli). Piyasa satırında ÖLÇÜLEMEDİ = uç gün < 30 ya da farklı ay < 12 "
    "(hisse satırının n >= 1.000 şartı piyasa için konamaz: dönem başına ~750-1.000 gün); piyasa 'AVR yönü' AVR hücresinde >= 10 uç günle. P15'te olay dışlaması yok.",
    "BİRLEŞİM adayı keşif uç %10 satırıyla (doğrulama görülmeden): tek başına keşifte üç alt uç şartını geçen sütunlar; çift seçimi keşif KAT'ıyla (bootstrap "
    "200, yalnız nokta değer kullanılır). BASİT PUAN: L1 lojistik lambda 0,001 sabit (ayar yok); KONTROL PUANI: Newton lojistik (cezasız).",
    "Kontrolü geçme: TUTAR satırının ABD 2020-22 uç kümesinde KAT, ATRP beşliği yerine kontrol puanı beşliğiyle (keşif sınırları) > 1 ve alt ucu > 1.",
    "KALICI (30 bar +%20 / -%8) ve Y5 yalnız bilgi; hükme girmez. SEÇİM = R15 - P15(d) bilgi.",
]


def yo_kesim_md(K: Dict[str, Any], sha: str) -> str:
    L = [f"# YO KESİM — ADIM 1 (yalnız KEŞİF: ABD 2016-19) yönleri, kesimleri ve keşif taban oranları ({K.get('zaman', '')})", "",
         "Bu dosya ADIM 2 (doğrulama: ABD 2020-22, AVR) sonuçları hesaplanmadan ÖNCE commit + push edilir. AVR kesimleri AVR 2016-19 ÖZELLİK dağılımındandır "
         "(getirisiz). Tanım ve kesimler sonra değişmez.", "", f"KESIM_SHA: {sha}", f"YO_ESIK_SHA: {K['esik_sha']}", "",
         "## Keşif taban oranları (ABD 2016-19)", "", f"- hisse-gün {K['taban_kesif']['n']}; P(Y10) {_f(K['taban_kesif']['Y10'], 2, True)} %, P(Y5) "
         f"{_f(K['taban_kesif']['Y5'], 2, True)} %, P(D10) {_f(K['taban_kesif']['D10'], 2, True)} %, R15 ort {_f(K['taban_kesif']['R15_ort'], 2, True)} %, KALICI "
         f"{_f(K['taban_kesif']['KALICI'], 2, True)} %", "", "| ATRP20 beşliği | n | P(Y10) % | P(D10) % |", "|---|---|---|---|"]
    for b in K["taban_kesif"]["besli"]:
        L.append(f"| {b['q']} | {b['n']} | {_f(b['Y10'], 2, True)} | {_f(b['D10'], 2, True)} |")
    L += ["", f"- ATRP20 beşlik sınırları: ABD {[round(x, 5) for x in K['atrp_besli']['ABD']]}; AVR {[round(x, 5) for x in K['atrp_besli']['AVR']]}",
          f"- Eşleşme: {K['esle']['olay']} olay (Y10 = 1; toplam {K['esle']['olay_toplam_Y10']}), {K['esle']['kontrol']} kontrol; 5'ten az kontrollü olay {K['esle']['eksik_kontrol_olay']}",
          "", "## ADIM 1: yükselişten önce ayrışma (eşli; |SMD| sırasıyla)", "",
          "| sıra | özellik | aile | yön | SMD [%95] | eşli AUC [%95] | ort olay | ort kontrol | n olay |", "|---|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(K["sira"]):
        r = K["adim1"][c]
        L.append(f"| {i + 1} | {c} | {YO_AILE[c]} | {K['yon'][c]['yon']} | {_f(r.get('SMD'), 3)} [{_f(r.get('SMD_alt'), 3)}; {_f(r.get('SMD_ust'), 3)}] | "
                 f"{_f(r.get('AUC'), 3)} [{_f(r.get('AUC_alt'), 3)}; {_f(r.get('AUC_ust'), 3)}] | {_f(r.get('ort_olay'), 4)} | {_f(r.get('ort_kontrol'), 4)} | {r.get('n_olay')} |")
    L += ["", "## Kesimler (uç eşikleri)", "", "| özellik | yön | ABD uç %10 | ABD uç %2 | AVR uç %10 | AVR uç %2 |", "|---|---|---|---|---|---|"]
    for c in YO_OZ:
        a, v = K["kesim"]["ABD"][c], K["kesim"]["AVR"][c]
        if c in YO_BAYRAK:
            kat = YO_BAYRAK[c][1] if K["yon"][c]["yon"] == "BÜYÜK" else YO_BAYRAK[c][0]
            L.append(f"| {c} | {K['yon'][c]['yon']} | bayrak = {kat:g} | - | bayrak = {kat:g} | - |")
        else:
            L.append(f"| {c} | {K['yon'][c]['yon']} | {_f(a['0.10'], 5)} | {_f(a['0.02'], 5)} | {_f(v['0.10'], 5)} | {_f(v['0.02'], 5)} |")
    L += ["", "## Keşif satırları (uç; ATRP beşliği içinde)", "", "| satır | n | ay | P(Y10) uç % | KAT ham | KAT [%95] | ASİMETRİ puan [%95] | TOPLAM FARK % [%95] |",
          "|---|---|---|---|---|---|---|---|"]
    for a, o in K["kesif_olc"].items():
        L.append(f"| {a} | {o.get('n')} | {o.get('ay')} | {_f(o.get('P_uc'), 2, True)} | {_f(o.get('KAT_HAM'), 2)} | {_f(o.get('KAT'), 2)} [{_f(o.get('KAT_alt'), 2)}; "
                 f"{_f(o.get('KAT_ust'), 2)}] | {_f(o.get('ASIMETRI'), 2, True)} [{_f(o.get('ASIMETRI_alt'), 2, True)}; {_f(o.get('ASIMETRI_ust'), 2, True)}] | "
                 f"{_f(o.get('TOPLAM_FARK'), 2, True)} [{_f(o.get('TOPLAM_FARK_alt'), 2, True)}; {_f(o.get('TOPLAM_FARK_ust'), 2, True)}] |")
    b = K["birlesim"]
    L += ["", "## BİRLEŞİM ve BASİT PUAN (keşifte seçildi)", "", f"- Birleşim adayları (keşif uç %10 üç alt uç şartı): {b['aday'] or 'yok'}",
          f"- Seçilen birleşim: {b['secilen']['ad'] if b.get('secilen') else 'kurulmadı (< 2 aday ya da n < 1.000)'}",
          f"- Kontrol modeli (Newton lojistik) ağırlıkları: {dict(zip(['kesişim'] + K['kontrol_model']['sutun'], [round(x, 4) for x in K['kontrol_model']['w']]))}",
          f"- Basit puan (L1, lambda {YO_ESIK['puan']['L1_lambda']}) ağırlıkları: " + ", ".join(f"{a} {w:+.4f}" for a, w in zip(['kesişim'] + K['puan']['sutun'], K['puan']['w']) if abs(w) > 0),
          f"- Puan kesimleri: ABD {K['puan']['kesim']['ABD']}; AVR {K['puan']['kesim']['AVR']}", "",
          "## PİYASA (ABD 2016-19 günleri; YP = P15 >= +%5)", "",
          f"- gün {K['piyasa']['taban_kesif']['gun']}; P(YP) {_f(K['piyasa']['taban_kesif']['YP'], 2, True)} %, P(DP) {_f(K['piyasa']['taban_kesif']['DP'], 2, True)} %, "
          f"P15 ort {_f(K['piyasa']['taban_kesif']['P15_ort'], 2, True)} %", "",
          "| sıra | özellik | yön | SMD [%95] | AUC [%95] | n YP günü | ABD uç %10 | AVR uç %10 |", "|---|---|---|---|---|---|---|---|"]
    for i, c in enumerate(K["piyasa"]["sira"]):
        r = K["piyasa"]["adim1"][c]
        L.append(f"| {i + 1} | {c} | {K['piyasa']['yon'][c]} | {_f(r.get('SMD'), 3)} [{_f(r.get('SMD_alt'), 3)}; {_f(r.get('SMD_ust'), 3)}] | {_f(r.get('AUC'), 3)} "
                 f"[{_f(r.get('AUC_alt'), 3)}; {_f(r.get('AUC_ust'), 3)}] | {r.get('n_olay')} | {_f(K['piyasa']['kesim']['ABD'][c]['0.10'], 4)} | {_f(K['piyasa']['kesim']['AVR'][c]['0.10'], 4)} |")
    L += ["", "## SAPMA", "", "(kesim anında yok)", ""]
    return "\n".join(L)


def _yo_aralik(o: Dict[str, Any], ad: str, n: int = 2, yuzde: bool = False) -> str:
    return f"{_f(o.get(ad), n, yuzde)} [{_f(o.get(ad + '_alt'), n, yuzde)}; {_f(o.get(ad + '_ust'), n, yuzde)}]"


def _yo_avr_yon(r: Dict[str, Any], uc: str = "TOPLAM_FARK") -> str:
    s = []
    for h in ("AVR|d1619", "AVR|d2022"):
        o = r["olc"].get(h, {})
        if o.get("n", 0) < (30 if uc == "TOPLAM_FARK" else 10):
            s.append("?"); continue
        ok = (o.get("KAT") or 0) > 1 and (o.get("ASIMETRI") or -1) > 0 and (o.get(uc) or -1) > 0
        ters = (o.get("KAT") or 0) < 1 and (o.get("ASIMETRI") or 0) < 0 and (o.get(uc) or 0) < 0
        s.append("+" if ok else ("-" if ters else "~"))
    return "/".join(s)


def yo_rapor_yaz(cikti: Optional[str] = None) -> str:
    cikti = cikti or YO_YOL["cikti"]
    J = json.load(open(_yo_yol("sonuc", cikti), encoding="utf-8")); K = json.load(open(_yo_yol("kesim", cikti), encoding="utf-8"))
    T = J["taban"]
    L = ["# YO RAPOR — yükseliş trendinden önce hangi bölge var: geriye bakış (ABD 2016-19) + ileriye doğru sınama (ABD 2020-22, AVR)", "",
         f"Sürüm {J['surum']}; ön kayıt {J['kapi']['onkayit_commit']}; kesim {J['kesim_kapi'].get('yo_kesim.json')}; süre {J['sure_sn']} sn. Evren bugün yaşayan "
         "hisseler (yukarı yanlı; Y10 ve D10 için de). KASA açılmadı (veri <= 2022-12-31). Hacim kullanılmadı.", "",
         f"Panel / satır dosyaları (repo dışı): {J['ham_yol']}; sha256: " + "; ".join(f"{a} {v[:16]}…" for a, v in J["dosya_sha"].items()), "",
         "## SONUÇ (OLASILIK TABLOSU)", "", f"**GENEL HÜKÜM: {J['genel']['hukum']}**", "",
         f"- TUTAR satırlar: {J['genel']['tutar'] or 'yok'}; TUTAR + KONTROLÜ GEÇER: {J['genel']['tutar_kontrol'] or 'yok'}; piyasa TUTAR: {J['genel']['piyasa_tutar'] or 'yok'}",
         f"- En yakın üç satır (TUTAR olmayan): {', '.join(J['en_yakin'])}", "", "### Taban oranları (hisse-gün; 15 bar)", "",
         "| hücre | hisse-gün | P(Y10) % | P(Y5) % | P(D10) % | R15 ort % | KALICI % |", "|---|---|---|---|---|---|---|"]
    for h, t in T.items():
        L.append(f"| {h} | {t['n']} | {_f(t['Y10'], 2, True)} | {_f(t['Y5'], 2, True)} | {_f(t['D10'], 2, True)} | {_f(t['R15_ort'], 2, True)} | {_f(t['KALICI'], 2, True)} |")
    L += ["", "### Oynaklık tuzağı: ATRP20 beşliklerine göre P(Y10) / P(D10) %", "", "| hücre | " + " | ".join(f"B{i} Y10 / D10" for i in range(1, 6)) + " |", "|---|" + "---|" * 5]
    for h, t in T.items():
        L.append(f"| {h} | " + " | ".join(f"{_f(b['Y10'], 1, True)} / {_f(b['D10'], 1, True)}" for b in t["besli"]) + " |")
    L += ["", "### Hisse satırları (keşif yönü ve kesimi; ATRP beşliği içinde KAT; ASİMETRİ ve TOPLAM FARK puan)", "",
          "| satır | yön | KEŞİF n | KEŞİF KAT ham | KEŞİF KAT [%95] | 20-22 n | 20-22 P(Y10) uç % | 20-22 KAT ham | 20-22 KAT [%95] | 20-22 ASİMETRİ [%95] | "
          "20-22 TOPLAM FARK [%95] | AVR yönü 16-19/20-22 | BH q | hüküm |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a, r in J["satir"].items():
        k, d = r["olc"][YO_KESIF], r["olc"]["ABD|d2022"]
        hk = r["hukum"] + (f" ({r['kontrol']})" if r["kontrol"] else "") + (" = tutmadı" if r["hukum"] == "TEK DÖNEM" else "")
        L.append(f"| {a} | {r['yon']} | {k.get('n')} | {_f(k.get('KAT_HAM'), 2)} | {_yo_aralik(k, 'KAT')} | {d.get('n')} | {_f(d.get('P_uc'), 1, True)} | {_f(d.get('KAT_HAM'), 2)} | "
                 f"{_yo_aralik(d, 'KAT')} | {_yo_aralik(d, 'ASIMETRI', 2, True)} | {_yo_aralik(d, 'TOPLAM_FARK', 2, True)} | {_yo_avr_yon(r)} | {_f(r['bh_q'], 3)} | {hk} |")
    L += ["", "- KEŞİF ASİMETRİ / TOPLAM FARK, AVR sayıları, KAT_PUAN (kontrol puanı beşliği içinde KAT), Y5 / KALICI / SEÇİM: yo_ozet.csv.", ""]
    b = J.get("birlesim")
    L += ["### BİRLEŞİM ve BASİT PUAN", ""]
    if b:
        d = b["olc"]["ABD|d2022"]
        L.append(f"- {b['sat']['ad']}: 20-22 n {d.get('n')}, KAT {_yo_aralik(d, 'KAT')}, ASİMETRİ {_yo_aralik(d, 'ASIMETRI', 2, True)}, TOPLAM FARK "
                 f"{_yo_aralik(d, 'TOPLAM_FARK', 2, True)}; hüküm {b['hukum']}; en iyi tek ({b['en_iyi_tek']}) KAT {_f(b['en_iyi_tek_KAT'], 2)} -> {'GEÇTİ' if b['gecti'] else 'GEÇMEDİ (seçilmez)'}")
    else:
        L.append(f"- Birleşim kurulmadı (keşif adayları: {K['birlesim']['aday'] or 'yok'}).")
    for u, r in J["puan"].items():
        d = r["olc"]["ABD|d2022"]; k = r["olc"][YO_KESIF]
        L.append(f"- BASİT PUAN uç {u}: keşif KAT {_yo_aralik(k, 'KAT')}; 20-22 n {d.get('n')}, KAT ham {_f(d.get('KAT_HAM'), 2)}, KAT {_yo_aralik(d, 'KAT')}, ASİMETRİ "
                 f"{_yo_aralik(d, 'ASIMETRI', 2, True)}, TOPLAM FARK {_yo_aralik(d, 'TOPLAM_FARK', 2, True)}; hüküm {r['hukum']}; en iyi tek ({r['en_iyi_tek']}) KAT "
                 f"{_f(r['en_iyi_tek_KAT'], 2)} -> {'GEÇTİ' if r['gecti'] else 'GEÇMEDİ (seçilmez)'}")
    L += ["", "### PİYASA TAHMİNİ (pazar-gün; YP = P15 >= +%5, DP = P15 <= -%5)", "", "| hücre | gün | P(YP) % | P(DP) % | P15 ort % |", "|---|---|---|---|---|"]
    for h, t in J["piyasa_taban"].items():
        L.append(f"| {h} | {t['gun']} | {_f(t['YP'], 2, True)} | {_f(t['DP'], 2, True)} | {_f(t['P15_ort'], 2, True)} |")
    L += ["", "| satır | yön | KEŞİF n gün | KEŞİF P(YP) / P(DP) uç % | KEŞİF P15 farkı [%95] | 20-22 n | 20-22 P(YP) / P(DP) uç % | 20-22 KAT [%95] | 20-22 P15 farkı [%95] | AVR | hüküm |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for a, r in J["piyasa"].items():
        k, d = r["olc"][YO_KESIF], r["olc"]["ABD|d2022"]
        L.append(f"| {a} | {r['yon']} | {k.get('n')} | {_f(k.get('P_YP_uc'), 1, True)} / {_f(k.get('P_DP_uc'), 1, True)} | {_yo_aralik(k, 'P15_FARK', 2, True)} | {d.get('n')} | "
                 f"{_f(d.get('P_YP_uc'), 1, True)} / {_f(d.get('P_DP_uc'), 1, True)} | {_yo_aralik(d, 'KAT')} | {_yo_aralik(d, 'P15_FARK', 2, True)} | {_yo_avr_yon(r, 'P15_FARK')} | {r['hukum']} |")
    L += ["", "## ADIM 1 (yalnız keşif): yükselişten önce en çok ayrışan özellikler", "", "| sıra | özellik | yön | SMD [%95] | eşli AUC [%95] |", "|---|---|---|---|---|"]
    for i, c in enumerate(K["sira"]):
        r = K["adim1"][c]
        L.append(f"| {i + 1} | {c} | {K['yon'][c]['yon']} | {_yo_aralik(r, 'SMD', 3)} | {_yo_aralik(r, 'AUC', 3)} |")
    L += ["", "## KONTROL LİSTESİ", "", "Ön kayıttaki tablo (YO_ON_KAYIT.md) aynen geçerli; ADIM 1 ve ADIM 2 kapıları geçti (kontrol + mühür + commit + temiz ağaç + KASA + kesim sha).",
          "", "## HATA", "", "(rapor ekinde; alt ajan raporu)", "", "## SAPMA", "", "(yok — rapor ekinde güncellenir)", "", "## ÖNERİLEN DEFTER SATIRLARI", "", "(alt ajan raporunda)", ""]
    yol = MI._mi_yaz(_yo_yol("rapor", cikti), "\n".join(L), "rapor")
    yo_png(J, K, _yo_yol("png", cikti))
    return yol


def yo_png(J: Dict[str, Any], K: Dict[str, Any], yol: str) -> str:
    """Cemal için tek sayfa (telefon): üstte 'yükselişten önce en çok ne vardı' (ADIM 1 |SMD|), altta 'ileriye doğru sınayınca' (keşif ve 2020-22 KAT)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    TR = {"MIKRO": "art arda yükselen kapanış serileri", "RS_UZAK": "göreli güç zirveye yakın", "RS_DIP_BIR": "fiyat dipte + göreli güç zirvede",
          "GEN50": "pazar genişliği (SMA50 üstü pay)", "GEN50_D10": "genişlik 10 günde değişim", "OYN_SIRA": "oynaklık sırası (60 gün)",
          "MA_KOD": "ortalamalar dizilimi (20/50/200)", "MA_EGIM_DEG": "SMA20 eğimi hızlanıyor", "ZIRVE_BAR": "zirveden bu yana gün", "ZIRVE_DUSUS": "zirveden düşüş %",
          "DIP_BAR": "dipten bu yana gün", "DIP_HIZ": "dipten toparlanma hızı", "CLV10": "kapanış mumun üstünde (10 gün)", "CLV_FARK": "kapanış konumu iyileşiyor",
          "YUKSELEN_DIP": "yükselen dipler", "MOM_12_1": "(kontrol) 12 aylık momentum", "F15": "(kontrol) son 15 gün getiri", "KONUM120": "(kontrol) 120 gün aralıkta konum",
          "ATRP20": "(kontrol) oynaklık ATRP20", "BOY_YUZDE_ORAN": "(kontrol) mum boyu küçülmesi", "ONCEKI_DUSUS": "(kontrol) önceki düşüş"}
    renk = {"TUTAR": "#1a7f37", "YALNIZ OYNAKLIK": "#d4a017", "TEK DÖNEM": "#e07b00", "TERS": "#b42318", "TUTMADI": "#8a8f98", "ÖLÇÜLEMEDİ": "#c8ccd2"}
    fig = plt.figure(figsize=(7.2, 12.8), dpi=150)
    fig.text(0.04, 0.975, "Yükselişten önce ne vardı? (ABD 2016-19)", fontsize=15, weight="bold", va="top")
    fig.text(0.04, 0.952, "Yükseliş = 15 günde +%10, önce -%5 görmeden. Aynı gün, aynı oynaklıktaki hisselerle karşılaştırma.", fontsize=8.2, va="top", color="#444")
    ax1 = fig.add_axes([0.40, 0.56, 0.55, 0.37])
    sira = K["sira"][:12][::-1]; v = [K["adim1"][c].get("SMD") or 0 for c in sira]
    ax1.barh(range(len(sira)), v, color=["#2b6cb0" if x > 0 else "#c05621" for x in v])
    ax1.set_yticks(range(len(sira))); ax1.set_yticklabels([TR.get(c, c) for c in sira], fontsize=8)
    ax1.axvline(0, color="k", lw=0.8); ax1.set_xlabel("fark (standart sapma; sağ = yükselişten önce DAHA BÜYÜK)", fontsize=8); ax1.tick_params(axis="x", labelsize=8)
    fig.text(0.04, 0.505, "İleriye doğru sınayınca tuttu mu? (uç %10; oynaklık sabit)", fontsize=13, weight="bold", va="top")
    fig.text(0.04, 0.483, "KAT = uçtaki hisselerin yükseliş olasılığı / aynı oynaklıktaki hisselerin. 1'in üstü = daha sık yükseliş.", fontsize=8.2, va="top", color="#444")
    ax2 = fig.add_axes([0.40, 0.09, 0.55, 0.37])
    sat = [a for a, r in J["satir"].items() if r["uc"] in ("0.10", "BAYRAK")]
    sat = sorted(sat, key=lambda a: J["satir"][a]["olc"]["ABD|d2022"].get("KAT") or 0)[-14:]
    for i, a in enumerate(sat):
        r = J["satir"][a]
        for h, dy, mk in ((YO_KESIF, 0.18, "o"), ("ABD|d2022", -0.18, "s")):
            o = r["olc"][h]; x = o.get("KAT")
            if x is None:
                continue
            lo, hi = o.get("KAT_alt") or x, o.get("KAT_ust") or x
            ax2.plot([lo, hi], [i + dy, i + dy], color=renk.get(r["hukum"], "#888"), lw=1.6)
            ax2.plot(x, i + dy, mk, color=renk.get(r["hukum"], "#888"), ms=4.5, mfc="white" if h == YO_KESIF else renk.get(r["hukum"], "#888"))
    ax2.set_yticks(range(len(sat))); ax2.set_yticklabels([TR.get(J["satir"][a]["ozellik"], a) for a in sat], fontsize=8)
    ax2.axvline(1, color="k", lw=0.8); ax2.set_xlabel("KAT (boş daire = 2016-19, dolu kare = 2020-22; çizgi = %95 aralık)", fontsize=8); ax2.tick_params(axis="x", labelsize=8)
    from matplotlib.patches import Patch
    ax2.legend(handles=[Patch(color=c, label=k) for k, c in renk.items()], fontsize=6.5, loc="lower right", ncol=2, frameon=False)
    g = J["genel"]["hukum"]
    fig.text(0.04, 0.035, "SONUÇ: " + g, fontsize=9.5, weight="bold", va="top", wrap=True)
    fig.text(0.04, 0.012, "Evren bugün yaşayan hisseler (yukarı yanlı). Kasa açılmadı. Alım-satım kararı Cemal'in.", fontsize=7, va="top", color="#555")
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True); fig.savefig(yol); plt.close(fig)
    return yol


def yo_sha_simdi(ham: Optional[str] = None) -> Dict[str, str]:
    return {"YO_KOD_SHA": yo_kod_sha(), "YO_ESIK_SHA": yo_esik_sha()}


# ================================================================ 10) ÇAKIŞMA KAPISI + KOMUT
def _cakisma_kontrol_yo(_once=_CK_ONCE_YO, _dosya="YUKSELIS_ONCESI.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_YO",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_yo()


def _yo_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="YUKSELIS_ONCESI")
    ap.add_argument("komut", choices=["hazirla", "sayim", "onkayit", "adim1", "adim2", "rapor", "sha"])
    a = ap.parse_args(argv)
    try:
        if a.komut == "hazirla":
            print(json.dumps(MI._mi_json(yo_hazirla()), ensure_ascii=False, indent=1))
        elif a.komut == "sayim":
            S = yo_sayim_kos(); MI._mi_jyaz(_yo_ham("sayim.json"), S, "sayım")
            print(json.dumps(MI._mi_json({h: {k: v for k, v in x.items() if k != "ozellik"} for h, x in S["hisse"].items()}), ensure_ascii=False, indent=1))
            print("SAYIM_SHA:", HV.hv_json_sha(S))
        elif a.komut == "onkayit":
            print(yo_onkayit_yaz())
        elif a.komut == "adim1":
            K = yo_adim1(); print(json.dumps(MI._mi_json({"sira": K["sira"], "birlesim": K["birlesim"]["aday"]}), ensure_ascii=False, indent=1))
        elif a.komut == "adim2":
            J = yo_adim2(); print(json.dumps(MI._mi_json(J["genel"]), ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            print(yo_rapor_yaz())
        elif a.komut == "sha":
            print(json.dumps(yo_sha_simdi(), indent=1))
    except YOHata as ex:
        yolog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_yo_ana())
