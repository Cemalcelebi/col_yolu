"""SEKIL_DEVAM — 'benzer şekil benzer devam getiriyor mu' (önerme sınaması) + 'veri kendi desenlerini bulsun' (k-ortalama kümeleri; keşif / doğrulama)
(27 Kasım 2026).

İş tanımı: arastirma_cikti/sekil_devam/SD_IS_TANIMI.md (ana model). Birim: pencere = hissenin kendi geçerli barlarında k'de biten L bar (L20 ve L10);
pencere sonları YUKSELIS_ONCESI örneklemiyle AYNI (her hissede her 5 barda bir, giriş günü TEZGÂH 2 P2 evreni, giriş k + 1 açılışı, 15 bar kuralı):
YO'nun mühürlü özellik paneli (ozellik_*.pkl) ve bar deposu (ham_*.npz) içe alınır, kopyalanmaz. Hacim MI.mi_veri açık kopyasından (C birebir denetlenir).
TANIMLAYICI A: her bar O / H / L / C bant koordinatı b = (fiyat - SMA20) / (2 sigma20) [MI.mi_bant: std ddof 0], [-3, +3] kırpılır + 4 ek sayı
(bant genişliği değişimi, önceki 60 bar tepesinden pencere dibine düşüş ATR biriminde, pencere başı / sonu KONUM120). TANIMLAYICI B: A + göreli hacim
log(V / önceki 60 barın medyanı) [-3, +3]. TANIMLAYICI 0: son barın bant koordinatı, F15 / ATRP20, KONUM120.
DEVAM: Z15 = (15. bar kapanışı / giriş - 1) / (ATRP20 x kök 15); HEDEF = +2 ATRP önce -1 ATRP görmeden; AYNA = -2 ATRP önce +1 görmeden (aynı bar = stop).
SINAMA 1: K = 50 en yakın komşu (yalnız geçmiş: sorgu ayının ilk sorgu barından >= 20 satır önce biten ve 15. barı o satırdan önce olan pencereler; başka
hisse) -> TAHMİN = komşuların ortalama Z15'i; aylık sıra IC; ay kümeli bootstrap. SINAMA 2: keşifte (ABD 2016-19) 60 küme (k-ortalama), en iyi 5 / en kötü 5;
doğrulamada (ABD 2020-22; AVR 2020-22 yön) bir kez. Veri <= 2022-12-31 (assert + KASA kapısı). KASA AÇILMAZ. Mevcut modüller DEĞİŞTİRİLMEZ; içe alınır.

Komut:  python SEKIL_DEVAM.py hazirla     ABD + AVR pencere tanımlayıcıları (getirisiz) + Cemal bölgeleri -> /root/.kasa/ham/sekil_devam
        python SEKIL_DEVAM.py sayim       GETİRİSİZ SAYIM (pencere / atılan / ay / boyut / komşu havuzu; standartlaştırma istatistikleri)
        python SEKIL_DEVAM.py onkayit     SD_ON_KAYIT.md (mühürler + sayım + yorum noktaları + kontrol tablosu)
        python SEKIL_DEVAM.py kesif       kapı -> YALNIZ ABD 2016-19 sonuçları -> kümeler + seçim -> sd_kesim.json + SD_KESIM.md
        python SEKIL_DEVAM.py dogrulama   kapı + kesim kapısı -> SINAMA 1 + SINAMA 2 (bir kez) -> sd_sonuc.json + sd_ozet.csv
        python SEKIL_DEVAM.py rapor       SD_RAPOR.md + SD_DESENLER.pdf
        python SEKIL_DEVAM.py sentetik    Cemal'in kalıbı gömülü yapay panel + N1 / N2 / N3 negatifleri -> sd_sentetik.json + SD_YAPAY_DESEN.pdf
        python SEKIL_DEVAM.py sha         kod / eşik sha
Colab:  exec(open('SEKIL_DEVAM.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Evren bugün işlem gören hisseler (K7: sonuç yukarı yanlı; iki taraf için de).
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_SD = {k: id(v) for k, v in globals().items()}

import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import pickle  # noqa: E402
import time  # noqa: E402
import zlib  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

KOK_SD = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_SD not in sys.path:
    sys.path.insert(0, KOK_SD)

import MUM_IZI as MI  # noqa: E402  (DEĞİŞTİRİLMEZ; veri, bant, yazma, git, sızıntı)
import MUM_IZI_V2 as MV  # noqa: E402  (DEĞİŞTİRİLMEZ; açık kopya yolu, şablon, mum çizimi)
import MUM_IZI_HAVUZ as HV  # noqa: E402  (DEĞİŞTİRİLMEZ; dönem ataması, ay özeti, BH, json sha)
import YUKSELIS_ONCESI as YO  # noqa: E402  (DEĞİŞTİRİLMEZ; örneklem, panel, dokunma, ATRP20 / F15 / KONUM120, kesik kapısı)

sdlog = logging.getLogger("col.sekil_devam")
if not sdlog.handlers:
    _sd_h = logging.StreamHandler(sys.stderr)
    _sd_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s sekil_devam: %(message)s", "%H:%M:%S"))
    sdlog.addHandler(_sd_h)
    sdlog.setLevel(logging.INFO)
    sdlog.propagate = False


class SDHata(RuntimeError):
    """Durdurucu hata: kapı / şema / veri / kesik / sıra / yeniden üretim uyuşmazlığı."""


SD_SURUM = "SEKIL_DEVAM v1.0 (2026-11-27): benzer şekil benzer devam mı (komşu) + veri kendi desenleri (k-ortalama)"
SD_YOL = {"cikti": os.path.join(KOK_SD, "arastirma_cikti", "sekil_devam"), "kod": os.path.join(KOK_SD, "SEKIL_DEVAM.py"),
          "ham": os.environ.get("SD_HAM", "/root/.kasa/ham/sekil_devam"), "yo_ham": YO.YO_YOL["ham"], "acik": MV.MV_YOL["gunluk"],
          "yo_onkayit": os.path.join(KOK_SD, "arastirma_cikti", "yukselis_oncesi", "YO_ON_KAYIT.md"),
          "cemal": os.path.join(KOK_SD, "arastirma_cikti", "mum_izi", "mum_izi23_olay.csv"),
          "is_tanimi": os.path.join(KOK_SD, "arastirma_cikti", "sekil_devam", "SD_IS_TANIMI.md")}
SD_DOSYA = {"onkayit": "SD_ON_KAYIT.md", "kesim_md": "SD_KESIM.md", "kesim": "sd_kesim.json", "sonuc": "sd_sonuc.json", "ozet": "sd_ozet.csv",
            "rapor": "SD_RAPOR.md", "pdf": "SD_DESENLER.pdf", "sentetik": "sd_sentetik.json", "yapay_pdf": "SD_YAPAY_DESEN.pdf"}
SD_KESIK = pd.Timestamp("2022-12-31")
SD_PAZAR = ("ABD", "AVR")

# ================================================================ MÜHÜRLÜ PARAMETRE SÖZLÜĞÜ (sha ön kayıtta; sonuçtan sonra DEĞİŞMEZ)
SD_ESIK: Dict[str, Any] = {
    "surum": "SD-1.0",
    "tohum": {"boot": 271, "kmeans": 272, "rastgele": 273, "ornek": 274, "sentetik": 275,
              "tanim": "np.random.default_rng([tohum, crc32(anahtar)]) (kmeans: default_rng(272) doğrudan); sıra bağımsız, tekrarlanabilir"},
    "pencere": {"L": [20, 10], "adim": 5,
                "tanim": "pencere sonu k = YO örnek satırı (YO ozellik_<pazar>.pkl: hissenin kendi geçerli bar indeksi k % 5 == 0, giriş k + 1 barı P2, "
                         "giriş 2016-2022, 15. bar <= 2022-12-31, YO boşluk kuralları); pencere = k - L + 1 .. k (L20 ve L10 aynı pencere sonları)"},
    "bant": {"n": 20, "k": 2.0, "klip": 3.0, "tanim": "MI.mi_bant(C) (SMA20, std ddof 0, yalnız o bara kadarki kapanışlar); b = (fiyat - BO) / (BU - BO) "
                                                       "= (fiyat - SMA20) / (2 sigma20); BU <= BO (sigma 0) ise tanımsız; [-3, +3] kırpılır"},
    "tanimlayici": {
        "A": "her bar i = k - L + 1 .. k için [b(O), b(H), b(L), b(C)] (bar sırasıyla, 4L sayı) + BW_DEG = bw_k / bw_s - 1 (bw = (BU - BA) / BO, s = pencere başı) "
             "+ DUSUS = (min L[s..k] - maks H[s-60 .. s-1]) / (ATRP20_k x C_k) (ATR birimi; kırpılmaz) + KON_BAS = KONUM120[s] + KON_SON = KONUM120[k] "
             "(KONUM120 = OLCU_SINAMA._os_atrp_f15 'f15', YO ile aynı); ek 4 sayı kırpılmaz (iş tanımı kırpmayı yalnız b ve göreli hacim için yazdı)",
        "B": "A + her bar için RV = log(V_i / medyan(V_{i-60} .. V_{i-1})) [-3, +3] (L sayı; hacim MI.mi_veri açık kopya, geçerli barlar)",
        "0": "[b(C_k), F15 / ATRP20_k, KONUM120_k] (F15 = C_k / C_{k-15} - 1, YO tanımı)",
        "gecerli": "pencerenin bütün A, RV ve 0 sayıları sonlu VE s - 60 >= 0 (önceki 60 bar var); A / B / 0 AYNI pencere kümesinde (eşli karşılaştırma)",
        "standart": "her boyut KEŞİF (ABD 2016-19) geçerli pencerelerinin ortalaması / std'si (ddof 0) ile (getirisiz; sayım aşamasında; sha ön kayıtta); "
                    "AVR de ABD keşif istatistikleriyle; std = 0 ise DUR"},
    "atma": {"sira": ["KILITLI", "TANIMSIZ"], "KILITLI": 0.20,
             "tanim": "KILITLI = pencerenin takvim aralığında (s barının günü .. k barının günü) ham veride geçersiz günlük bar payı (MI.mi_veri 'gecersiz': "
                      "kilitli / hacimsiz / H = L) > 0,20 (MUM_IZI_UC.uc_kilitli_pay; UC kuralı aynen); TANIMSIZ = geçerli şartı tutmuyor; ilk tutan neden"},
    "devam": {"ufuk": 15, "hedef": 2.0, "stop": 1.0,
              "tanim": "E0 = k + 1 açılışı; barlar k + 1 .. k + 15 (giriş barı dahil; YO ile aynı); R15 = C_{k+15} / E0 - 1; Z15 = R15 / (ATRP20_k x kök 15); "
                       "YOL_j = (C_{k+j} / E0 - 1) / (ATRP20_k x kök 15), j = 1..15; HEDEF = High >= E0 (1 + 2 ATRP20_k) ilk barı Low <= E0 (1 - 1 ATRP20_k) "
                       "ilk barından ÖNCE (aynı bar = stop önce -> 0; YO.yo_ilk_dokunma ATRP birimine çevrilmiş fiyatla); AYNA = Low <= E0 (1 - 2 ATRP) "
                       "önce High >= E0 (1 + 1 ATRP) görmeden"},
    "komsu": {"K": 50, "ara": 20, "kume": "giriş ayı",
              "havuz": "sorgular giriş ayına göre gruplanır; r0 = grubun en küçük pencere sonu satırı (birleşik takvim); havuz = aynı pazarın geçerli "
                       "pencereleri, t_row <= r0 - 20 VE 15. sonuç barının satırı < r0 (komşunun devamı sorgudan önce bilinir) VE başka hisse; ayda bir "
                       "güncellenen havuz; uzaklık standart tanımlayıcıda Öklid (float32 BLAS, |y|^2 - 2xy sıralaması); TAHMİN = 50 komşunun ortalama Z15'i",
              "rastgele": "şans tabanı: aynı havuzdan (başka hisse) eşit olasılıkla 50 pencere (tohum 273, anahtar 'pazar|L|ay')"},
    "ic": {"ay_en_az": 30, "tanim": "her giriş ayında (>= 30 sorgu) TAHMİN ile Z15'in Spearman sıra ilişkisi (ortalama sıra); IC = ayların eşit ağırlıklı ortalaması; "
                                    "fark (A - 0, B - A) aynı ayların aylık farklarının ortalaması"},
    "uc": {"pay": 0.10, "tanim": "her giriş ayında TAHMİN'in kesit yüzdelik sırası (ortalama sıra / n): ÜST = > 0,90, ALT = <= 0,10"},
    "toplam_fark": "R15 - aynı hissenin aynı hücredeki (pazar x dönem) bütün YO örnek pencerelerinin (tanımlayıcısı geçersiz olanlar dahil) R15 ortalaması",
    "yol": "her sorgu için corr(YOL_sorgu, komşuların ortalama YOL'u) (15 nokta; sabitse yok); sorgular üzerinden ortalama; rastgele komşularla aynı",
    "boot": {"B": 10000, "kume": "giriş ayı (YYYY-AA)",
             "tanim": "ay kümeli bootstrap (aylar yerine koyarak; multinomial ağırlık); oran / ortalama = ağırlıklı toplam / ağırlıklı sayı; IC = ağırlıklı aylık IC "
                      "ortalaması; %95 = 2,5 / 97,5 yüzdelik; ÜST - ALT aynı ağırlıklarla"},
    "kmeans": {"k": 60, "iter": 300, "tanim": "k-ortalama++ başlangıç (default_rng(272); tek başlangıç), Lloyd adımları atama değişmeyince ya da 300 adımda durur; "
                                              "boş küme önceki merkezini korur; KEŞİF standart A (L20 ve L10 ayrı) üzerinde; doğrulama / AVR / Cemal pencereleri en "
                                              "yakın merkeze atanır"},
    "secim": {"en_iyi": 5, "en_kotu": 5, "n_min": 1000, "ay_min": 12,
              "tanim": "aday küme = keşif n >= 1000 ve farklı ay >= 12; EN İYİ 5 = keşif ortalama Z15'i en büyük 5 (azalan), EN KÖTÜ 5 = en küçük 5 (artan); "
                       "eşitlikte küçük küme no"},
    "bh_q": 0.10,
    "hucre": {"kesif": "ABD|d1619", "dogrulama": "ABD|d2022", "avr": "AVR|d2022", "avr_bilgi": "AVR|d1619",
              "tanim": "dönem giriş tarihine göre HV.hv_hucre_ad; AVR yön sınaması AVR 2020-22 sorguları (havuz AVR 2016'dan); AVR 2016-19 yalnız SINAMA 2'de bilgi"},
    "hukum": {
        "S1_TASIYOR": "ABD 2020-22'de IC(A) > 0 ve alt > 0 VE IC(A) - IC(0) > 0 ve alt > 0 VE ÜST - ALT Z15 > 0 ve alt > 0 VE AVR 2020-22 IC(A) > 0 -> 'ŞEKİL BİLGİ TAŞIYOR'",
        "S1_BASIT": "IC(A) > 0 ve alt > 0 ama IC(A) - IC(0) alt <= 0 -> 'BASİT KONUMDAN FAZLASI YOK'",
        "S1_TASIMIYOR": "IC(A) alt <= 0 (aralık sıfırı içeriyor ya da eksi) -> 'ŞEKİL BİLGİ TAŞIMIYOR'",
        "S1_ARA": "IC(A) alt > 0, IC(A) - IC(0) alt > 0 ama ÜST - ALT ya da AVR şartı tutmuyor -> 'ARA: <eksik şart>' (ŞEKİL BİLGİ TAŞIYOR denmez)",
        "HACIM": "IC(B) - IC(A) > 0 ve alt > 0 -> 'HACİM EKLİYOR'; değilse 'HACİM EKLEMİYOR'",
        "S2_IYI": "EN İYİ küme: doğrulamada Z15 > 0 ve alt > 0 VE TOPLAM FARK > 0 ve alt > 0 VE AVR 2020-22 ortalama Z15 > 0 (AVR n >= 30; değilse şart tutmamış) "
                  "-> 'TUTTU'",
        "S2_KOTU": "EN KÖTÜ küme: Z15 < 0 ve üst < 0 VE TOPLAM FARK < 0 ve üst < 0 VE AVR ortalama Z15 < 0 -> 'TUTTU'",
        "DESEN": "'DESEN TUTTU' <=> keşif sırası 1 olan EN İYİ küme TUTTU (EN KÖTÜ 1 için ayrı satır); 10 küme için BH q 0,10 (tek yönlü bootstrap p: iyi "
                 "(1 + #Z15* <= 0) / (B + 1), kötü (1 + #Z15* >= 0) / (B + 1))",
        "L10": "aynı kurallar L10 için ayrı (ERKEN EVRE)"},
    "cemal": {"sinif": "EVET", "zaman": "gunluk",
              "tanim": "mum_izi23_olay.csv günlük satırları: pencere = bolge_son barında biten 20 (ve 10) bar (Cemal'in bölgesi 16-24 bar; pencere uzunluğu sabit), "
                       "ABD / AVR / BIST serisi MI.mi_veri açık kopyasından; P2 / kilit kuralı uygulanmaz (bilgi); EVET = BENZİYOR; KISMEN / HAYIR bilgi",
              "APPN": {"SOL": "2021-06-07", "SAG": "2021-09-07", "tanim": "MUM_IZI26_IKI_BOLGE: SOL 2021-05-07 .. 06-07, SAĞ 2021-08-16 .. 09-07; pencere = son "
                                                                          "barda biten 20 bar"}},
    "pdf": {"ornek": 6, "once": 40, "tanim": "her seçilen küme bir sayfa: merkez (bant koordinatında mum + Bollinger), keşif üyelerinden rastgele 6 gerçek örnek "
                                             "(tohum 274; pencere + önceki 40 bar; yüzde ekseni; SONRASI YOK: dilim k + 1'de biter, assert)"},
    "sentetik": {"hisse": 150, "bar": 2000, "olay_ara": [70, 110], "ilk": 200, "pay": {"POZ": 0.5, "N1": 0.25, "N2": 0.25}, "gurultu": [0.0, 0.10, 0.20, 0.30],
                 "olcek": [0.5, 2.0], "Z_ek": 0.5, "n_min": 30, "ay_min": 12,
                 "tanim": "POZ = Cemal'in kalıbı (MV.mv_sablon()['tam'] 20 mum) bant ölçeğinde gömülür: fiyat = SMA20(s-1) + (şablon - şablon BO_0) x sigma20(s-1) / "
                          "şablon sigma_0 x ölçek (log-düzgün 0,5..2), gürültü = düzey x ölçekli ortalama şablon mum boyu (O / H / L / C'ye ayrı normal), "
                          "sonra giriş barından sonraki barda (k + 2) +0,5 Z'lik tek sıçrama (bilerek; sonraki pencerelerin devamına taşmasın diye); N1 = aynı kapanış yolu, iri gövdeli üst fitilsiz mum (gövde = şablon ortalama mum boyu), "
                          "ilişki YOK; N2 = şablonun mum biçimi (O / H / L kapanışa göre), yatay ya da düşen kapanış yolu, ilişki YOK; N3 = gömülmemiş rastgele "
                          "yürüyüş pencereleri; ilişkisiz panel = yalnız rastgele yürüyüş; kalıbın kümesi = POZ keşif pencerelerinin en çok düştüğü küme"},
}

# ================================================================ KONTROL LİSTESİ (ön kayıtta; IZ_KARNE.ik_kontrol_kapisi)
SD_KONTROL = {
    "K1": ("EVET", "taban = aynı pazar x dönem, aynı evren; IC aynı ay içinde (kesit) hesaplanır (zaman etkisi dışlanır); TAHMİN'in şans tabanı rastgele komşu "
                   "(aynı havuz) ve basit taban TANIMLAYICI 0 (son bant konumu, F15 / ATRP, KONUM120: bilinen etkiler); Z15 ATRP20 ile oynaklıktan arındırılmış; "
                   "TOPLAM FARK aynı hissenin aynı dönem ortalamasına göre; ÜST / ALT aynı ayın kesitinde; HEDEF ve AYNA iki yönde aynı kötümser kural"),
    "K2": ("EVET", "tanımlayıcı yalnız k'ye kadarki barlardan (test: k + 1 ve sonrası bozulunca aynı); komşular yalnız geçmişten: t_row <= r0 - 20 ve 15. sonuç barı "
                   "< r0, başka hisse (kodda maske + test); giriş k + 1 açılışı; sonuçlar ayrı fonksiyonda, keşif aşamasında yalnız ABD 2016-19 (assert); "
                   "standartlaştırma ve kümeler yalnız keşiften; veri <= 2022-12-31 assert + KASA kapısı"),
    "K3": ("EVET", "MI.mi_veri geçerli bar (H > L, V > 0, sonlu > 0); kilitli / hacimsiz / H = L bar payı > 0,20 olan pencere atılır (UC kuralı); bant sigma 0 "
                   "ise tanımsız; YO örneklem kuralları (giriş boşluğu <= 10 satır, 15 bar <= 30 satır)"),
    "K4": ("EVET", "her hissede her 5 barda bir pencere (örtüşme azaltılır, kalkmaz: 20 barlık pencereler örtüşür); çıkarım ay kümeli bootstrap (pencereler "
                   "bağımsız sayılmaz); n pencere ve farklı ay ayrı yazılır; medyan Z15 bilgi; komşu başka hisseden"),
    "K5": ("EVET", "giriş = pencere sonundan sonraki ilk geçerli bar açılışı (k + 1), k kapanışı değil"),
    "K6": ("EVET", "YO / OS bölünme düzeltmeli açık kopya; getiriler oransal, yerel para, pazar içi; tanımlayıcı birimsiz (bant koordinatı, ATR birimi, konum); "
                   "hacim oranı hissenin kendi geçmişine göre; açık kopya kapanışları YO bar deposuyla birebir (assert)"),
    "K7": ("EVET", "evren bugün yaşayan hisseler (hayatta kalma yanlılığı): Z15 / R15 yukarı yanlı; ÜST - ALT ve IC kesit içi olduğu için yanlılık iki tarafa da "
                   "biner; raporda yazılır; kasa açılmaz"),
    "K8": ("EVET", "n büyük (yüz binler; ay 36); küme hükmü n >= 1000 ve ay >= 12 kümelerde; 10 küme BH q 0,10; iki dönem (keşif / doğrulama) + iki pazar; "
                   "en kalabalık 3 ay payı her küme satırında; Cemal bölgeleri (36 günlük EVET) yalnız sayım, sonuç değil"),
    "K9": ("EVET", "SD_ON_KAYIT.md: SD_KOD_SHA, SD_ESIK_SHA, panel dosya sha'ları, SAYIM_SHA, YO panel sha'ları + yorum noktaları; keşif ön kayıt commit + push "
                   "sonrası (kapı: kontrol + sha + commit + temiz ağaç); doğrulama sd_kesim.json commit'inden sonra (kapı); ikinci koşu durur; K, küme sayısı, "
                   "pencere uzunluğu için ikinci değer denenmez"),
    "K10": ("EVET", "YO panel sha'ları YO_ON_KAYIT ile aynı (assert); açık kopya kapanışları bar deposuyla birebir; tanımlayıcı elle kurulmuş sentetik örnekte; "
                    "KONUM120 / F15 yeniden hesabı YO panelindeki değerle aynı (assert); Cemal bölgesi bolge_son tarihi seride yoksa 'YOK' yazılır"),
    "K11": ("EVET", "küme merkezleri doğrulamada yeniden hesaplanır ve sd_kesim.json'la aynı olmalı (DUR); raporda >= 2 sayı satır dosyalarından bağımsız kısa "
                    "kodla yeniden üretilir; komşu araması küçük örnekte saf çözümle karşılaştırılır (test)"),
    "K12": ("EVET", "hüküm yalnız önceden yazılı kurala göre; IC küçükse 'küçük' denir ve para karşılığı (ÜST - ALT R15 %, rastgele güne göre TOPLAM FARK) yanına "
                    "yazılır; sayı ile yorum ayrı cümlede; 'iz' sözü kullanılmaz (önerme sınaması); evren bugün yaşayanlar"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_sd); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması "
                    "MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat; KNN / şekil ölçüsü kapalı konusu Cemal'in açık isteğiyle yalnız bu işte"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; karar vermez, kasa açılmaz"),
}


# ================================================================ 0) YARDIMCI
def _sd_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or SD_YOL["cikti"], SD_DOSYA[ad])


def _sd_ham(ad: str, ham: Optional[str] = None) -> str:
    return os.path.join(ham or SD_YOL["ham"], ad)


def sd_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or SD_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def sd_kod_sha() -> str:
    return MI._mi_sha(SD_YOL["kod"])


def _sd_rng(tur: str, anahtar: str) -> np.random.Generator:
    return np.random.default_rng([int(SD_ESIK["tohum"][tur]), zlib.crc32(str(anahtar).encode("utf-8"))])


def _sd_git(args: List[str]) -> str:
    return MI._mi_git(args)


def sd_kesik_kapi(V: Dict[str, pd.DataFrame], ad: str = "veri") -> pd.Timestamp:
    """Kasa kapısı (mekanik): YO.yo_kesik_kapi aynen (kesik 2022-12-31)."""
    try:
        return YO.yo_kesik_kapi(V, ad)
    except YO.YOHata as ex:
        raise SDHata(str(ex)) from ex


def _sd_tarih_kapi(tarih: Any, ad: str) -> None:
    t = pd.DatetimeIndex(tarih)
    if len(t) and t.max() > SD_KESIK:
        raise SDHata(f"KESİK AŞIMI: {ad} en geç {t.max().date()} > {SD_KESIK.date()} (KASA açılmaz)")


# ================================================================ 1) TANIMLAYICI (yalnız k'ye kadarki barlar)
def sd_bant_koord(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray) -> Dict[str, np.ndarray]:
    """Bar başına bant koordinatları ve bant genişliği (MI.mi_bant; yalnız o bara kadarki kapanışlar)."""
    E = SD_ESIK["bant"]; BU, BO, BA = MI.mi_bant(np.asarray(C, float), int(E["n"]), float(E["k"])); kl = float(E["klip"])
    with np.errstate(invalid="ignore", divide="ignore"):
        g = BU - BO; inv = np.where(g > 0, 1.0 / g, np.nan)
        out = {a: np.clip((np.asarray(x, float) - BO) * inv, -kl, kl) for a, x in (("bO", O), ("bH", H), ("bL", L), ("bC", C))}
        out["bw"] = (BU - BA) / BO
    return out


def sd_tanim_seri(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, V: np.ndarray, ks: np.ndarray, Lw: int,
                  atrp_k: np.ndarray) -> Dict[str, np.ndarray]:
    """Bir hissenin barlarında pencere sonları ks için TANIMLAYICI A (4L + 4), göreli hacim (L), TANIMLAYICI 0 (3) ve geçerlilik. Pencere k - L + 1 .. k;
    hiçbir değer k + 1 ve sonrasına bakmaz (bantlar, hareketli ortalamalar yalnız geride)."""
    import OLCU_SINAMA as OS
    O, H, L, C, V = (np.asarray(a, float) for a in (O, H, L, C, V)); ks = np.asarray(ks, np.int64); atrp_k = np.asarray(atrp_k, float)
    m = len(C); n = len(ks); Lw = int(Lw)
    b = sd_bant_koord(O, H, L, C)
    kon = OS._os_atrp_f15(pd.DataFrame({"High": H, "Low": L, "Close": C}))[1]
    on = 60                                                                              # TANIMLAYICI B: önceki 60 barın medyan hacmi
    with np.errstate(invalid="ignore", divide="ignore"):
        medV = pd.Series(V).rolling(on, min_periods=on).median().shift(1).to_numpy(float)
        rv = np.clip(np.log(V / medV), -3.0, 3.0)
    rv[~np.isfinite(medV)] = np.nan
    mx60 = pd.Series(H).rolling(60, min_periods=60).max().shift(1).to_numpy(float)       # s'de: maks H[s-60 .. s-1]
    mnW = pd.Series(L).rolling(Lw, min_periods=Lw).min().to_numpy(float)                 # k'de: min L[k-L+1 .. k]
    s = ks - Lw + 1
    ok = (s - 60 >= 0) & (ks < m) & (ks >= 0)
    sg = np.clip(s, 0, m - 1); kg = np.clip(ks, 0, m - 1)
    idx = np.clip(s[:, None] + np.arange(Lw)[None, :], 0, m - 1)
    Ab = np.stack([b["bO"][idx], b["bH"][idx], b["bL"][idx], b["bC"][idx]], axis=2).reshape(n, 4 * Lw)
    with np.errstate(invalid="ignore", divide="ignore"):
        bwd = b["bw"][kg] / b["bw"][sg] - 1
        dus = (mnW[kg] - mx60[sg]) / (atrp_k * C[kg])
        f15 = np.where(kg - 15 >= 0, C[kg] / C[np.clip(kg - 15, 0, m - 1)] - 1, np.nan)
        z0 = np.stack([b["bC"][kg], f15 / atrp_k, kon[kg]], axis=1)
    A = np.concatenate([Ab, bwd[:, None], dus[:, None], kon[sg][:, None], kon[kg][:, None]], axis=1)
    VOL = rv[idx]
    ok &= np.isfinite(A).all(1) & np.isfinite(VOL).all(1) & np.isfinite(z0).all(1)
    return {"A": A, "VOL": VOL, "Z0": z0, "ok": ok, "KON": kon[kg], "F15": f15}


# ================================================================ 2) PANEL (getirisiz)
def sd_panel_kur(dep: Dict[str, np.ndarray], tarih: pd.DatetimeIndex, sembol: np.ndarray, X: pd.DataFrame,
                 gec: Optional[Dict[str, pd.DatetimeIndex]] = None, pazar: str = "?", kontrol_yo: bool = True) -> Dict[str, Any]:
    """dep: O, H, L, C, V, POS, off (hisse sırası sembol); X: YO örnek satırları (j, k, t_row, d_row, giris, hucre, ay, ATRP20, F15, KONUM120).
    Dönüş: meta dizileri + her L için A / VOL / Z0 / ok / neden. Sonuç (getiri) hesaplanmaz."""
    import MUM_IZI_UC as UC
    t0 = time.time(); tarih = pd.DatetimeIndex(tarih); _sd_tarih_kapi(tarih, f"{pazar} takvim")
    X = X.sort_values(["j", "k"], kind="stable").reset_index(drop=True)
    N = len(X); U = int(SD_ESIK["devam"]["ufuk"]); kp = float(SD_ESIK["atma"]["KILITLI"])
    j = X.j.to_numpy(np.int64); k = X.k.to_numpy(np.int64); off = np.asarray(dep["off"], np.int64); POS = np.asarray(dep["POS"], np.int64)
    g = off[j] + k
    if (g + U > off[j + 1] - 1).any():
        raise SDHata("K10: pencere sonu + 15 hissenin verisini aşıyor (YO örneklemi bozuk)")
    if (POS[g] != X.t_row.to_numpy(np.int64)).any() or (POS[g + 1] != X.d_row.to_numpy(np.int64)).any():
        raise SDHata("K10: YO t_row / d_row bar deposuyla uyuşmuyor")
    P: Dict[str, Any] = {"pazar": pazar, "N": N, "j": j, "k": k, "t_row": X.t_row.to_numpy(np.int64), "d_row": X.d_row.to_numpy(np.int64),
                         "s15_row": POS[g + U], "giris": X.giris.to_numpy("datetime64[ns]"), "tarih": X.tarih.to_numpy("datetime64[ns]"),
                         "hucre": X.hucre.to_numpy(str), "ay": X.ay.to_numpy(str), "atrp": X.ATRP20.to_numpy(float),
                         "sembol": np.asarray(sembol, str), "L": [int(x) for x in SD_ESIK["pencere"]["L"]]}
    atrp = P["atrp"]
    for Lw in P["L"]:
        P[f"A{Lw}"] = np.full((N, 4 * Lw + 4), np.nan, np.float32); P[f"VOL{Lw}"] = np.full((N, Lw), np.nan, np.float32)
        P[f"Z0{Lw}"] = np.full((N, 3), np.nan, np.float32); P[f"ok{Lw}"] = np.zeros(N, bool); P[f"neden{Lw}"] = np.full(N, "TAMAM", dtype="<U8")
    gr = pd.Series(np.arange(N)).groupby(j).indices
    kon_hata = 0
    for jj, ii in gr.items():
        a, b_ = int(off[jj]), int(off[jj + 1]); kk = k[ii]
        O_, H_, L_, C_, V_ = (np.asarray(dep[c][a:b_], float) for c in ("O", "H", "L", "C", "V"))
        gun = tarih[POS[a:b_]]
        for Lw in P["L"]:
            T = sd_tanim_seri(O_, H_, L_, C_, V_, kk, Lw, atrp[ii])
            if kontrol_yo and Lw == P["L"][0]:
                for ad, yo in (("KON", "KONUM120"), ("F15", "F15")):
                    v1 = T[ad]; v2 = X[yo].to_numpy(float)[ii]; f = np.isfinite(v1) | np.isfinite(v2)
                    if f.any() and not np.allclose(np.nan_to_num(v1[f], nan=-9), np.nan_to_num(v2[f], nan=-9), rtol=1e-9, atol=1e-12):
                        kon_hata += 1
            ned = np.where(T["ok"], "TAMAM", "TANIMSIZ").astype("<U8")
            if gec is not None:
                s = np.clip(kk - Lw + 1, 0, len(gun) - 1)
                kpay = UC.uc_kilitli_pay(gec.get(str(P["sembol"][jj]), pd.DatetimeIndex([])), gun, gun[s], gun[kk])
                ned = np.where(kpay > kp, "KILITLI", ned)
            P[f"A{Lw}"][ii] = T["A"]; P[f"VOL{Lw}"][ii] = T["VOL"]; P[f"Z0{Lw}"][ii] = T["Z0"]
            P[f"ok{Lw}"][ii] = ned == "TAMAM"; P[f"neden{Lw}"][ii] = ned
    if kon_hata:
        raise SDHata(f"K10: {pazar}: KONUM120 / F15 yeniden hesabı YO panelinden farklı ({kon_hata} hisse)")
    sdlog.info("%s panel: %d pencere, L20 geçerli %d, L10 geçerli %d (%.0f sn)", pazar, N, int(P["ok20"].sum()) if "ok20" in P else -1,
               int(P["ok10"].sum()) if "ok10" in P else -1, time.time() - t0)
    return P


def sd_panel_yaz(P: Dict[str, Any], yol: str) -> str:
    D = {k: v for k, v in P.items() if isinstance(v, np.ndarray)}
    D["_meta"] = np.array(json.dumps({"pazar": P["pazar"], "N": P["N"], "L": P["L"]}))
    np.savez(yol, **D)
    return yol


def sd_panel_oku(yol: str) -> Dict[str, Any]:
    z = np.load(yol, allow_pickle=False); P: Dict[str, Any] = {k: z[k] for k in z.files if k != "_meta"}
    P.update(json.loads(str(z["_meta"])))
    return P


# ================================================================ 3) SONUÇ ÇEKİRDEĞİ (devam; yalnız sd_sonuc üzerinden)
def sd_sonuc_dizi(dep: Dict[str, np.ndarray], j: np.ndarray, k: np.ndarray, atrp: np.ndarray) -> Dict[str, np.ndarray]:
    """Z15, R15, HEDEF, AYNA, YOL (15) — giriş k + 1 açılışı, barlar k + 1 .. k + 15 (YO ile aynı geometri)."""
    E = SD_ESIK["devam"]; U = int(E["ufuk"]); j = np.asarray(j, np.int64); k = np.asarray(k, np.int64); a = np.asarray(atrp, float); N = len(j)
    out = {c: np.full(N, np.nan) for c in ("E0", "R15", "Z15", "HEDEF", "AYNA")}; out["YOL"] = np.full((N, U), np.nan)
    if not N:
        return out
    off = np.asarray(dep["off"], np.int64); g = off[j] + k
    if (g + U > off[j + 1] - 1).any():
        raise SDHata("K10: sonuç penceresi hissenin verisini aşıyor")
    W = g[:, None] + 1 + np.arange(U)[None, :]
    E0 = np.asarray(dep["O"], float)[g + 1]; Cw = np.asarray(dep["C"], float)[W]
    sc = a * np.sqrt(U)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["E0"] = E0; out["R15"] = Cw[:, -1] / E0 - 1; out["Z15"] = out["R15"] / sc
        out["YOL"] = (Cw / E0[:, None] - 1) / sc[:, None]
        Hn = 1 + (np.asarray(dep["H"], float)[W] / E0[:, None] - 1) / a[:, None]
        Ln = 1 + (np.asarray(dep["L"], float)[W] / E0[:, None] - 1) / a[:, None]
    one = np.ones(N)
    out["HEDEF"] = YO.yo_ilk_dokunma(one, Hn, Ln, float(E["hedef"]), float(E["stop"]), "yukari")
    out["AYNA"] = YO.yo_ilk_dokunma(one, Hn, Ln, float(E["hedef"]), float(E["stop"]), "asagi")
    bad = ~(np.isfinite(E0) & (E0 > 0) & np.isfinite(a) & (a > 0))
    for c in ("R15", "Z15", "HEDEF", "AYNA"):
        out[c][bad] = np.nan
    out["YOL"][bad] = np.nan
    return out


_SD_ASAMA_IZIN = {"kesif": {"ABD|d1619"}, "dogrulama": {"ABD|d1619", "ABD|d2022", "AVR|d1619", "AVR|d2022"}, "test": None}


def sd_sonuc(P: Dict[str, Any], dep: Dict[str, np.ndarray], asama: str, satir: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
    """Sonuç sütunları YALNIZ izin verilen hücrelerin satırları için (keşifte yalnız ABD|d1619; assert). satir: hesaplanacak satır indeksleri."""
    if asama not in _SD_ASAMA_IZIN:
        raise SDHata(f"aşama: {asama}")
    satir = np.arange(P["N"]) if satir is None else np.asarray(satir, np.int64)
    izin = _SD_ASAMA_IZIN[asama]
    if izin is not None:
        h = set(np.unique(P["hucre"][satir]).tolist())
        if not h <= izin:
            raise SDHata(f"SIRA: {asama} aşamasında izin dışı hücre sonucu istendi: {sorted(h - izin)}")
    R = sd_sonuc_dizi(dep, P["j"][satir], P["k"][satir], P["atrp"][satir])
    R["satir"] = satir
    return R


def sd_toplam_fark(R15: np.ndarray, j: np.ndarray, hucre: np.ndarray) -> np.ndarray:
    """R15 - aynı hissenin aynı hücredeki bütün örnek pencerelerinin R15 ortalaması."""
    df = pd.DataFrame({"r": R15, "j": j, "h": hucre})
    return (df.r - df.groupby(["j", "h"]).r.transform("mean")).to_numpy(float)


# ================================================================ 4) STANDART + KOMŞU
def sd_standart_kur(M: np.ndarray) -> Dict[str, List[float]]:
    M = np.asarray(M, float); ort = M.mean(0); sd = M.std(0)
    if not np.isfinite(ort).all() or (sd <= 0).any() or not np.isfinite(sd).all():
        raise SDHata("standartlaştırma: std 0 ya da sonlu değil (DUR)")
    return {"ort": [float(x) for x in ort], "sd": [float(x) for x in sd]}


def sd_std_hepsi(P: Dict[str, Any], maske: np.ndarray) -> Dict[str, Any]:
    """Keşif geçerli pencerelerinden her L için A, VOL, Z0 standartlaştırma istatistikleri (getirisiz)."""
    S = {}
    for Lw in P["L"]:
        m = maske & P[f"ok{Lw}"]
        S[str(Lw)] = {ad: sd_standart_kur(P[f"{ad}{Lw}"][m]) for ad in ("A", "VOL", "Z0")}
    return S


def sd_matris(P: Dict[str, Any], Lw: int, tur: str, S: Dict[str, Any]) -> np.ndarray:
    """Standart tanımlayıcı (float32): 'A', 'B' (= A + VOL), '0'."""
    st = S[str(Lw)]

    def z(ad):
        return ((P[f"{ad}{Lw}"].astype(float) - np.array(st[ad]["ort"])) / np.array(st[ad]["sd"])).astype(np.float32)
    if tur == "A":
        return z("A")
    if tur == "B":
        return np.concatenate([z("A"), z("VOL")], axis=1)
    if tur == "0":
        return z("Z0")
    raise SDHata(f"tanımlayıcı: {tur}")


def sd_havuz_maske(t_row: np.ndarray, s15_row: np.ndarray, r0: int, ara: Optional[int] = None) -> np.ndarray:
    ara = int(SD_ESIK["komsu"]["ara"] if ara is None else ara)
    return (np.asarray(t_row) <= int(r0) - ara) & (np.asarray(s15_row) < int(r0))


def sd_komsu(M: np.ndarray, sorgu: np.ndarray, havuz: np.ndarray, j: np.ndarray, t_row: np.ndarray, s15_row: np.ndarray, ay: np.ndarray,
             K: Optional[int] = None, rastgele: bool = False, anahtar: str = "", is_parcasi: int = 64, isci: int = 4) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Her sorgu satırı için K komşu (havuz satırlarından; global satır indeksi). Yalnız geçmiş + başka hisse (sd_havuz_maske). Ay ay; havuz ayda bir.
    rastgele=True: aynı havuzdan eşit olasılıkla K (şans tabanı)."""
    K = int(SD_ESIK["komsu"]["K"] if K is None else K); sorgu = np.asarray(sorgu, np.int64); havuz = np.asarray(havuz, np.int64)
    out = np.full((len(sorgu), K), -1, np.int64); bilgi = {"ay": {}, "havuz_min": None, "havuz_max": None}
    gr = pd.Series(np.arange(len(sorgu))).groupby(np.asarray(ay)[sorgu]).indices
    hz = []
    for a_, qi in sorted(gr.items()):
        q = sorgu[qi]; r0 = int(t_row[q].min())
        pm = havuz[sd_havuz_maske(t_row[havuz], s15_row[havuz], r0)]
        pm = pm[np.argsort(j[pm], kind="stable")]; pj = j[pm]
        if len(pm) < 2 * K:
            raise SDHata(f"komşu havuzu çok küçük ({a_}: {len(pm)})")
        hz.append(len(pm)); bilgi["ay"][a_] = {"sorgu": int(len(q)), "havuz": int(len(pm))}
        if rastgele:
            rng = _sd_rng("rastgele", f"{anahtar}|{a_}")
            for ii, qq in enumerate(q):
                sec = np.zeros(0, np.int64)
                while len(sec) < K:
                    c = pm[rng.integers(0, len(pm), size=2 * K)]; c = c[j[c] != j[qq]]; sec = np.r_[sec, c]
                out[qi[ii]] = sec[:K]
            continue
        Pm = np.ascontiguousarray(M[pm], np.float32); pn = (Pm.astype(np.float64) ** 2).sum(1).astype(np.float32)
        Qm = np.ascontiguousarray(M[q], np.float32); qj = j[q]
        lo = np.searchsorted(pj, qj, "left"); hi = np.searchsorted(pj, qj, "right")

        def is_(sl):
            D = Qm[sl] @ Pm.T; D *= -2.0; D += pn[None, :]
            for r, (a1, b1) in enumerate(zip(lo[sl], hi[sl])):
                D[r, a1:b1] = np.inf
            I = np.argpartition(D, K - 1, axis=1)[:, :K]
            return sl, pm[I]
        parca = [slice(x, min(x + is_parcasi, len(q))) for x in range(0, len(q), is_parcasi)]
        with ThreadPoolExecutor(isci) as ex:
            for sl, I in ex.map(is_, parca):
                out[qi[sl]] = I
        del Pm, Qm; gc.collect()
    if (out < 0).any():
        raise SDHata("komşu: doldurulmamış satır")
    bilgi["havuz_min"] = int(min(hz)) if hz else None; bilgi["havuz_max"] = int(max(hz)) if hz else None
    bilgi["havuz_medyan"] = float(np.median(hz)) if hz else None
    return out, bilgi


def sd_komsu_denetim(I: np.ndarray, sorgu: np.ndarray, j: np.ndarray, t_row: np.ndarray, s15_row: np.ndarray, ay: np.ndarray) -> Dict[str, int]:
    """Mekanik denetim: her komşu başka hisse, t_row <= r0 - 20, s15_row < r0 (r0 = sorgunun ay grubundaki en küçük t_row) ve <= sorgu t_row - 20."""
    ara = int(SD_ESIK["komsu"]["ara"]); ayq = np.asarray(ay)[sorgu]
    r0 = pd.Series(t_row[sorgu]).groupby(ayq).transform("min").to_numpy(np.int64)
    ayni = int((j[I] == j[sorgu][:, None]).sum()); gec = int((t_row[I] > (r0[:, None] - ara)).sum()); s15 = int((s15_row[I] >= r0[:, None]).sum())
    gec2 = int((t_row[I] > (t_row[sorgu][:, None] - ara)).sum())
    return {"ayni_hisse": ayni, "yakin": gec, "sonuc_bilinmiyor": s15, "sorgudan_20_bar_once_degil": gec2}


# ================================================================ 5) İSTATİSTİK
def _sd_q(v: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
    v = v[np.isfinite(v)]
    if not len(v):
        return None, None
    return float(np.quantile(v, 0.025)), float(np.quantile(v, 0.975))


def sd_W(K: int, anahtar: str, B: Optional[int] = None) -> np.ndarray:
    B = int(B or SD_ESIK["boot"]["B"])
    return _sd_rng("boot", anahtar).multinomial(K, np.full(K, 1.0 / K), size=B).astype(float)


def sd_sira(x: np.ndarray) -> np.ndarray:
    return pd.Series(x).rank(method="average").to_numpy(float)


def sd_ic_ay(T: np.ndarray, Z: np.ndarray, ay: np.ndarray, en_az: Optional[int] = None) -> pd.Series:
    """Aylık Spearman (ortalama sıra); >= en_az sorgulu aylar."""
    en_az = int(SD_ESIK["ic"]["ay_en_az"] if en_az is None else en_az); T = np.asarray(T, float); Z = np.asarray(Z, float)
    f = np.isfinite(T) & np.isfinite(Z); df = pd.DataFrame({"T": T[f], "Z": Z[f], "a": np.asarray(ay)[f]}); r = {}
    for a_, g in df.groupby("a"):
        if len(g) < en_az:
            continue
        x = sd_sira(g["T"].to_numpy()); y = sd_sira(g["Z"].to_numpy())
        r[a_] = float(np.corrcoef(x, y)[0, 1]) if x.std() > 0 and y.std() > 0 else np.nan
    return pd.Series(r, dtype=float).dropna()


def sd_boot_ic(ic: pd.Series, anahtar: str, B: Optional[int] = None) -> Dict[str, Any]:
    v = ic.to_numpy(float); K = len(v)
    if K < 2:
        return {"ic": None, "alt": None, "ust": None, "ay": K}
    W = sd_W(K, anahtar, B); d = (W @ v) / K; a, b = _sd_q(d)
    return {"ic": float(v.mean()), "alt": a, "ust": b, "ay": int(K)}


def sd_boot_grup(x: np.ndarray, ay: np.ndarray, maskeler: Dict[str, np.ndarray], anahtar: str, B: Optional[int] = None,
                 farklar: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
    """Ay kümeli bootstrap: her maskenin ortalaması (aynı ağırlıklarla) + istenen farklar. x NaN satırlar maske dışı."""
    x = np.asarray(x, float); u, kix = np.unique(np.asarray(ay, str), return_inverse=True); K = len(u)
    out: Dict[str, Any] = {}
    if K < 2:
        return {ad: {"ort": None, "alt": None, "ust": None, "n": int(m.sum())} for ad, m in maskeler.items()}
    W = sd_W(K, anahtar, B); dag = {}
    for ad, m in maskeler.items():
        f = np.asarray(m, bool) & np.isfinite(x)
        s = np.bincount(kix[f], weights=x[f], minlength=K); n = np.bincount(kix[f], minlength=K).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            d = (W @ s) / (W @ n)
        dag[ad] = d; a, b = _sd_q(d)
        out[ad] = {"ort": float(x[f].mean()) if f.any() else None, "medyan": float(np.median(x[f])) if f.any() else None, "alt": a, "ust": b,
                   "n": int(f.sum())}
    for a1, a2 in (farklar or []):
        d = dag[a1] - dag[a2]; lo, hi = _sd_q(d)
        o1, o2 = out[a1]["ort"], out[a2]["ort"]
        out[f"{a1}-{a2}"] = {"ort": None if o1 is None or o2 is None else o1 - o2, "alt": lo, "ust": hi}
        out[f"{a1}-{a2}"]["p_alt"] = float((1 + np.sum(d[np.isfinite(d)] <= 0)) / (np.isfinite(d).sum() + 1))
    out["_dag"] = dag
    return out


def sd_p_tek(dag: np.ndarray, yon: str) -> float:
    d = dag[np.isfinite(dag)]
    k = np.sum(d <= 0) if yon == "iyi" else np.sum(d >= 0)
    return float((1 + k) / (len(d) + 1))


def sd_uc_maske(T: np.ndarray, ay: np.ndarray, pay: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
    pay = float(SD_ESIK["uc"]["pay"] if pay is None else pay)
    s = pd.Series(np.asarray(T, float)); r = s.groupby(np.asarray(ay)).rank(method="average", pct=True).to_numpy(float)
    return (r > 1 - pay), (r <= pay)


def sd_yol_benzer(Y: np.ndarray, Yk: np.ndarray) -> np.ndarray:
    """Satır başına corr(YOL, komşu ortalama YOL)."""
    a = Y - Y.mean(1, keepdims=True); b = Yk - Yk.mean(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        return (a * b).sum(1) / np.sqrt((a * a).sum(1) * (b * b).sum(1))


# ================================================================ 6) K-ORTALAMA
def sd_ata(X: np.ndarray, C: np.ndarray, parca: int = 100000) -> np.ndarray:
    X = np.asarray(X, float); C = np.asarray(C, float); cn = (C * C).sum(1); out = np.empty(len(X), np.int64)
    for a in range(0, len(X), parca):
        D = cn[None, :] - 2.0 * (X[a:a + parca] @ C.T); out[a:a + parca] = np.argmin(D, axis=1)
    return out


def sd_kmeans(X: np.ndarray, k: Optional[int] = None, tohum: Optional[int] = None, it: Optional[int] = None) -> Dict[str, Any]:
    """k-ortalama++ + Lloyd (tek başlangıç; boş küme merkezini korur)."""
    k = int(SD_ESIK["kmeans"]["k"] if k is None else k); it = int(SD_ESIK["kmeans"]["iter"] if it is None else it)
    rng = np.random.default_rng(int(SD_ESIK["tohum"]["kmeans"] if tohum is None else tohum)); X = np.asarray(X, float); n = len(X)
    if n < k:
        raise SDHata("k-ortalama: örnek < küme")
    i0 = int(rng.integers(n)); C = [X[i0].copy()]; d2 = ((X - X[i0]) ** 2).sum(1)
    for _ in range(1, k):
        p = d2 / d2.sum(); i = int(rng.choice(n, p=p)); C.append(X[i].copy()); d2 = np.minimum(d2, ((X - X[i]) ** 2).sum(1))
    C = np.array(C); lab = np.full(n, -1, np.int64); adim = 0
    for adim in range(1, it + 1):
        yeni = sd_ata(X, C)
        if (yeni == lab).all():
            break
        lab = yeni
        for c in range(k):
            m = lab == c
            if m.any():
                C[c] = X[m].mean(0)
    return {"merkez": C, "etiket": lab, "adim": int(adim)}


# ================================================================ 7) DÜZ DİL TARİF
def _sd_konum_soz(b: float) -> str:
    if b <= -0.6:
        return "alt bantta"
    if b <= -0.2:
        return "orta ile alt bant arasında"
    if b < 0.2:
        return "ortada (SMA20 çevresinde)"
    if b < 0.6:
        return "orta ile üst bant arasında"
    return "üst bantta"


def sd_tarif(ham: np.ndarray, Lw: int) -> str:
    """Küme merkezinin (ham birim) tek cümlelik düz dil tarifi."""
    h = np.asarray(ham, float); B = h[:4 * Lw].reshape(Lw, 4); q = max(1, Lw // 4)
    bas = float(B[:q, 3].mean()); son = float(B[-q:, 3].mean()); boy = float((B[:, 1] - B[:, 2]).mean()) / 2.0 * 100
    ust = float((B[:, 1] - np.maximum(B[:, 0], B[:, 3])).mean()); alt = float((np.minimum(B[:, 0], B[:, 3]) - B[:, 2]).mean())
    bwd, dus, ks, ke = (float(x) for x in h[4 * Lw:4 * Lw + 4])
    fitil = "üst fitil uzun" if ust > 1.3 * alt else ("alt fitil uzun" if alt > 1.3 * ust else "fitiller dengeli")
    return (f"Kapanışlar {_sd_konum_soz(bas)} başlayıp {_sd_konum_soz(son)} bitiyor; mum boyu bant genişliğinin %{boy:.0f}'i, {fitil}; bant "
            f"%{abs(bwd) * 100:.0f} {'daralıyor' if bwd < 0 else 'genişliyor'}; dip önceki 60 günün tepesinin {abs(dus):.1f} ATR "
            f"{'altında' if dus < 0 else 'üstünde'}; 120 günlük aralıkta %{ks * 100:.0f} konumundan %{ke * 100:.0f}'e")


# ================================================================ 8) VERİ ve HAZIRLIK
def sd_yo_panel_denetim() -> Dict[str, str]:
    """YO panel dosyalarının sha'ları YO_ON_KAYIT.md'deki mühürlerle aynı mı (K10)."""
    metin = open(SD_YOL["yo_onkayit"], encoding="utf-8").read(); out = {}
    for p in SD_PAZAR:
        for ad in (f"ozellik_{p}.pkl", f"ham_{p}.npz"):
            sh = MI._mi_sha(os.path.join(SD_YOL["yo_ham"], ad))
            if f"DOSYA_{ad}: {sh}" not in metin:
                raise SDHata(f"K10: YO panel dosyası {ad} mühürden farklı -> DURDU")
            out[ad] = sh
    return out


def sd_veri_pazar(pazar: str, Vd: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, np.ndarray], pd.DatetimeIndex, np.ndarray, pd.DataFrame, Dict[str, Any]]:
    """YO bar deposu + YO örnek satırları + açık kopyadan hacim (kapanış birebir denetlenir)."""
    z = np.load(os.path.join(SD_YOL["yo_ham"], f"ham_{pazar}.npz"))
    X = pd.read_pickle(os.path.join(SD_YOL["yo_ham"], f"ozellik_{pazar}.pkl"))
    if Vd is None:
        Vd = MI.mi_veri(pazar, SD_YOL["acik"])
    sd_kesik_kapi(Vd["V"], f"günlük {pazar}")
    S = z["sembol"]; off = z["off"]; Vv = np.empty(len(z["C"]))
    for jj, s in enumerate(S):
        d = Vd["V"][str(s)]; a, b = int(off[jj]), int(off[jj + 1])
        if len(d) != b - a or not np.array_equal(d.Close.to_numpy(float), z["C"][a:b]):
            raise SDHata(f"K10: {pazar} {s}: açık kopya kapanışları YO bar deposundan farklı")
        Vv[a:b] = d.Volume.to_numpy(float)
    dep = {c: z[c] for c in ("O", "H", "L", "C", "POS", "off")}; dep["V"] = Vv
    tarih = pd.DatetimeIndex(z["tarih"]); _sd_tarih_kapi(tarih, f"{pazar} takvim")
    return dep, tarih, S, X[["j", "k", "t_row", "d_row", "tarih", "giris", "hucre", "ay", "ATRP20", "F15", "KONUM120"]], Vd


def sd_cemal_tanim(Vds: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Cemal'in günlük bölgeleri + APPN SOL / SAĞ: bolge_son'da biten L20 / L10 tanımlayıcısı (ham; getirisiz)."""
    C = pd.read_csv(SD_YOL["cemal"]); C = C[C.zaman == SD_ESIK["cemal"]["zaman"]].copy()
    ek = [{"set": "MUM_IZI26", "sinif": "APPN_" + ad, "pazar": "ABD", "sembol": "APPN", "bolge_bas": None, "bolge_son": t, "m": None}
          for ad, t in (("SOL", SD_ESIK["cemal"]["APPN"]["SOL"]), ("SAG", SD_ESIK["cemal"]["APPN"]["SAG"]))]
    R = pd.concat([C[["set", "sinif", "pazar", "sembol", "bolge_bas", "bolge_son", "m"]], pd.DataFrame(ek)], ignore_index=True)
    sat = []
    for _, r in R.iterrows():
        o = {**r.to_dict(), "durum": "TAMAM"}
        Vd = Vds.get(r.pazar)
        if Vd is None or str(r.sembol) not in Vd["V"]:
            o["durum"] = "VERI_YOK"; sat.append(o); continue
        d = Vd["V"][str(r.sembol)]; t = pd.Timestamp(r.bolge_son)
        if t not in d.index:
            o["durum"] = "TARIH_YOK"; sat.append(o); continue
        kk = int(d.index.get_loc(t)); O_, H_, L_, C_, V_ = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close", "Volume"))
        atrp = YO.yo_hisse_ozellik(O_, H_, L_, C_, C_)["ATRP20"]
        for Lw in SD_ESIK["pencere"]["L"]:
            T = sd_tanim_seri(O_[:kk + 1], H_[:kk + 1], L_[:kk + 1], C_[:kk + 1], V_[:kk + 1], np.array([kk]), int(Lw), atrp[[kk]])
            o[f"A{Lw}"] = T["A"][0].tolist(); o[f"ok{Lw}"] = bool(T["ok"][0])
        sat.append(o)
    return pd.DataFrame(sat)


def sd_hazirla(ham: Optional[str] = None) -> Dict[str, Any]:
    ham = ham or SD_YOL["ham"]; os.makedirs(ham, exist_ok=True); out: Dict[str, Any] = {"yo_panel": sd_yo_panel_denetim()}
    Vds: Dict[str, Dict[str, Any]] = {}
    for p in SD_PAZAR:
        dep, tarih, S, X, Vd = sd_veri_pazar(p)
        P = sd_panel_kur(dep, tarih, S, X, Vd.get("gecersiz", {}), p)
        sd_panel_yaz(P, _sd_ham(f"ozellik_{p}.npz", ham))
        out[p] = {"N": int(P["N"]), **{f"ok{Lw}": int(P[f"ok{Lw}"].sum()) for Lw in P["L"]}}
        Vds[p] = {"V": Vd["V"]}; del P, dep, X; gc.collect()
    try:
        Vb = MI.mi_veri("BIST", SD_YOL["acik"]); sd_kesik_kapi(Vb["V"], "günlük BIST"); Vds["BIST"] = {"V": Vb["V"]}
    except Exception as ex:   # BIST yalnız Cemal bölgeleri için bilgi; yüklenemezse 'VERI_YOK'
        sdlog.warning("BIST yüklenemedi (Cemal bölgeleri VERI_YOK): %s", ex); out["bist_hata"] = str(ex)
    Cm = sd_cemal_tanim(Vds); Cm.to_pickle(_sd_ham("cemal_tanim.pkl", ham))
    out["cemal"] = Cm.groupby(["pazar", "sinif", "durum"]).size().reset_index().values.tolist()
    MI._mi_jyaz(_sd_ham("hazirla_log.json", ham), out, "hazırla")
    return out


# ================================================================ 9) GETİRİSİZ SAYIM
def sd_sayim(PS: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Dönem x pazar x L: pencere, atılan (neden), geçerli, farklı ay, en kalabalık 3 ay payı; boyutlar; komşu havuzu (doğrulama ayları); standart istatistikleri."""
    S: Dict[str, Any] = {"hucre": {}, "boyut": {}, "havuz": {}}
    for p, P in PS.items():
        for h in np.unique(P["hucre"]):
            m = P["hucre"] == h
            for Lw in P["L"]:
                ok = m & P[f"ok{Lw}"]; ao = HV.hv25_ay_ozet(pd.DatetimeIndex(P["giris"][ok]).strftime("%Y-%m-%d").tolist())
                ned = pd.Series(P[f"neden{Lw}"][m]).value_counts().to_dict()
                S["hucre"][f"{h}|L{Lw}"] = {"pencere": int(m.sum()), "gecerli": int(ok.sum()), "atilan": {k: int(v) for k, v in ned.items() if k != "TAMAM"},
                                           "ay": ao["ay"], "ust3_pay": ao["ust3_pay"], "hisse": int(len(np.unique(P["j"][ok])))}
        for Lw in P["L"]:
            S["boyut"][f"L{Lw}"] = {"A": 4 * Lw + 4, "B": 5 * Lw + 4, "0": 3}
            q_h = SD_ESIK["hucre"]["dogrulama"] if p == "ABD" else SD_ESIK["hucre"]["avr"]
            ok = P[f"ok{Lw}"]; q = np.flatnonzero(ok & (P["hucre"] == q_h)); hv = np.flatnonzero(ok)
            hz = []
            for a_, qi in pd.Series(q).groupby(P["ay"][q]).groups.items():
                r0 = int(P["t_row"][q[np.asarray(qi)]].min()); hz.append(int(sd_havuz_maske(P["t_row"][hv], P["s15_row"][hv], r0).sum()))
            S["havuz"][f"{p}|L{Lw}"] = {"sorgu": int(len(q)), "ay": len(hz), "havuz_min": min(hz) if hz else None, "havuz_medyan": float(np.median(hz)) if hz else None,
                                       "havuz_max": max(hz) if hz else None}
    P = PS["ABD"]; S["standart"] = sd_std_hepsi(P, P["hucre"] == SD_ESIK["hucre"]["kesif"])
    return S


def sd_yukle_hepsi(ham: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    return {p: sd_panel_oku(_sd_ham(f"ozellik_{p}.npz", ham)) for p in SD_PAZAR}


def sd_dosya_sha(ham: Optional[str] = None) -> Dict[str, str]:
    return {ad: MI._mi_sha(_sd_ham(ad, ham)) for ad in [f"ozellik_{p}.npz" for p in SD_PAZAR] + ["cemal_tanim.pkl"]}


def sd_sayim_kos(ham: Optional[str] = None) -> Dict[str, Any]:
    return sd_sayim(sd_yukle_hepsi(ham))


# ================================================================ 10) KAPILAR
def sd_kapi(cikti: Optional[str] = None, ham: Optional[str] = None, sayim: bool = True) -> Dict[str, Any]:
    """Ön kayıt kapısı: kontrol listesi + mühürler + commit + temiz ağaç + panel sha + sayım sha + KASA."""
    import IZ_KARNE as IK
    import KASA as KS
    cikti = cikti or SD_YOL["cikti"]; yol = _sd_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise SDHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    bek = {"SD_KOD_SHA": sd_kod_sha(), "SD_ESIK_SHA": sd_esik_sha(), **{f"DOSYA_{a}": v for a, v in sd_dosya_sha(ham).items()}}
    for a, v in bek.items():
        if f"{a}: {v}" not in metin:
            raise SDHata(f"ön kayıt kapısı: {a} farklı -> DURDU")
    S = None
    if sayim:
        S = json.load(open(_sd_ham("sayim.json", ham), encoding="utf-8"))
        if f"SAYIM_SHA: {HV.hv_json_sha(S)}" not in metin:
            raise SDHata("getirisiz sayım ön kayıttakiyle aynı değil -> DURDU")
    rel = os.path.relpath(yol, KOK_SD); c = _sd_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise SDHata("ön kayıt commit'li değil -> DURDU")
    if _sd_git(["status", "--porcelain", "--", rel, "SEKIL_DEVAM.py"]):
        raise SDHata("ön kayıt / kod çalışma ağacında değişmiş -> DURDU")
    try:
        kasa = KS.kasa_kapisi([os.path.join(SD_YOL["acik"], f"V_{p}.pkl") for p in SD_PAZAR], "2022-12-31")
    except KS.KasaHata as ex:
        raise SDHata(f"KASA kapısı KAPALI: {ex}") from ex
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, "kasa": kasa, **bek, "_sayim": S}


def sd_kesim_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or SD_YOL["cikti"]; y = _sd_yol("kesim", cikti); ym = _sd_yol("kesim_md", cikti)
    for f in (y, ym):
        if not os.path.exists(f):
            raise SDHata(f"kesim dosyası yok: {f}")
        rel = os.path.relpath(f, KOK_SD)
        if not _sd_git(["log", "-1", "--format=%H", "--", rel]):
            raise SDHata(f"kesim commit'li değil: {rel}")
        if _sd_git(["status", "--porcelain", "--", rel]):
            raise SDHata(f"kesim çalışma ağacında değişmiş: {rel}")
    return {"kesim_commit": _sd_git(["log", "-1", "--format=%H %cI", "--", os.path.relpath(y, KOK_SD)]), "kesim_sha": MI._mi_sha(y)}


# ================================================================ 11) KEŞİF (yalnız ABD 2016-19 sonuçları)
def sd_kume_ozet(lab: np.ndarray, R: Dict[str, np.ndarray], ay: np.ndarray, k: int) -> List[Dict[str, Any]]:
    out = []
    for c in range(k):
        m = lab == c; z = R["Z15"][m]; f = np.isfinite(z)
        out.append({"kume": c, "n": int(f.sum()), "ay": int(len(np.unique(ay[m][f]))) if f.any() else 0,
                    "Z15": float(z[f].mean()) if f.any() else None, "R15": float(np.nanmean(R["R15"][m])) if f.any() else None,
                    "HEDEF": float(np.nanmean(R["HEDEF"][m])) if f.any() else None, "AYNA": float(np.nanmean(R["AYNA"][m])) if f.any() else None})
    return out


def sd_sec(oz: List[Dict[str, Any]], n_min: Optional[int] = None, ay_min: Optional[int] = None) -> Dict[str, Any]:
    E = SD_ESIK["secim"]; n_min = int(E["n_min"] if n_min is None else n_min); ay_min = int(E["ay_min"] if ay_min is None else ay_min)
    ad = [o for o in oz if o["n"] >= n_min and o["ay"] >= ay_min and o["Z15"] is not None]
    iyi = sorted(ad, key=lambda o: (-o["Z15"], o["kume"]))[:int(E["en_iyi"])]
    kotu = sorted(ad, key=lambda o: (o["Z15"], o["kume"]))[:int(E["en_kotu"])]
    sira = {o["kume"]: i + 1 for i, o in enumerate(sorted([o for o in oz if o["Z15"] is not None], key=lambda o: (-o["Z15"], o["kume"])))}
    return {"iyi": [o["kume"] for o in iyi], "kotu": [o["kume"] for o in kotu], "aday": len(ad), "sira": sira}


def sd_kesif_hesap(P: Dict[str, Any], dep: Dict[str, np.ndarray], Sstd: Dict[str, Any], Cm: Optional[pd.DataFrame] = None,
                   n_min: Optional[int] = None, ay_min: Optional[int] = None, k: Optional[int] = None) -> Dict[str, Any]:
    kh = SD_ESIK["hucre"]["kesif"]; K: Dict[str, Any] = {"L": {}}
    for Lw in P["L"]:
        m = (P["hucre"] == kh) & P[f"ok{Lw}"]; ii = np.flatnonzero(m)
        M = sd_matris(P, Lw, "A", Sstd)[ii].astype(float)
        km = sd_kmeans(M, k=k)
        R = sd_sonuc(P, dep, "kesif" if P["pazar"] == "ABD" else "test", ii)
        oz = sd_kume_ozet(km["etiket"], R, P["ay"][ii], len(km["merkez"])); sec = sd_sec(oz, n_min, ay_min)
        st = Sstd[str(Lw)]["A"]; hamm = km["merkez"] * np.array(st["sd"]) + np.array(st["ort"])
        for o in oz:
            o["sira"] = sec["sira"].get(o["kume"]); o["tarif"] = sd_tarif(hamm[o["kume"]], Lw)
        L_ = {"merkez": km["merkez"].tolist(), "merkez_ham": hamm.tolist(), "adim": km["adim"], "n": int(len(ii)), "kume": oz, "secim": sec}
        if Cm is not None:
            L_["cemal"] = sd_cemal_ata(Cm, Lw, Sstd, km["merkez"], sec, oz)
        K["L"][str(Lw)] = L_
        sdlog.info("keşif L%d: %d pencere, %d adım; iyi %s, kötü %s", Lw, len(ii), km["adim"], sec["iyi"], sec["kotu"])
    return K


def sd_cemal_ata(Cm: pd.DataFrame, Lw: int, Sstd: Dict[str, Any], merkez: np.ndarray, sec: Dict[str, Any], oz: List[Dict[str, Any]]) -> Dict[str, Any]:
    st = Sstd[str(Lw)]["A"]; ok = Cm.get(f"ok{Lw}", pd.Series(False, index=Cm.index)).fillna(False).astype(bool).to_numpy()
    sat = []
    for i, r in Cm.iterrows():
        o = {"set": r["set"], "sinif": r.sinif, "pazar": r.pazar, "sembol": r.sembol, "bolge_son": str(r.bolge_son), "durum": r.durum, "kume": None, "sira": None}
        if r.durum == "TAMAM" and ok[i]:
            x = (np.array(r[f"A{Lw}"], float) - np.array(st["ort"])) / np.array(st["sd"])
            c = int(sd_ata(x[None, :], merkez)[0]); o["kume"] = c; o["sira"] = sec["sira"].get(c)
        elif r.durum == "TAMAM":
            o["durum"] = "TANIMSIZ"
        sat.append(o)
    D = pd.DataFrame(sat); ozet = {}
    for sn in ("EVET", "KISMEN", "HAYIR"):
        g = D[(D.sinif == sn) & D.kume.notna()]
        v = g.kume.astype(int).value_counts()
        ozet[sn] = {"n": int(len(g)), "n_tum": int((D.sinif == sn).sum()), "ilk5": [[int(c), int(n), float(n / max(len(g), 1)), sec["sira"].get(int(c))] for c, n in v.iloc[:5].items()],
                    "secilen_iyi_pay": float(g.kume.astype(int).isin(sec["iyi"]).mean()) if len(g) else None,
                    "secilen_kotu_pay": float(g.kume.astype(int).isin(sec["kotu"]).mean()) if len(g) else None,
                    "pazar": g.pazar.value_counts().to_dict()}
    appn = {r["sinif"]: {"kume": r["kume"], "sira": r["sira"], "durum": r["durum"]} for r in sat if str(r["sinif"]).startswith("APPN_")}
    return {"satir": sat, "ozet": ozet, "appn": appn}


def sd_kesif(cikti: Optional[str] = None, ham: Optional[str] = None) -> Dict[str, Any]:
    cikti = cikti or SD_YOL["cikti"]
    if os.path.exists(_sd_yol("kesim", cikti)):
        raise SDHata("kesim zaten var (ikinci keşif koşusu DURUR)")
    G = sd_kapi(cikti, ham); S = G.pop("_sayim")
    P = sd_panel_oku(_sd_ham("ozellik_ABD.npz", ham)); dep, *_ = _sd_dep_oku("ABD")
    Cm = pd.read_pickle(_sd_ham("cemal_tanim.pkl", ham))
    K = sd_kesif_hesap(P, dep, S["standart"], Cm)
    K.update({"surum": SD_SURUM, "kapi": G, "esik_sha": sd_esik_sha(), "kod_sha": sd_kod_sha(), "standart_sha": HV.hv_json_sha(S["standart"]),
              "zaman": pd.Timestamp.now(tz="UTC").isoformat()})
    MI._mi_jyaz(_sd_yol("kesim", cikti), K, "kesim")
    MI._mi_yaz(_sd_yol("kesim_md", cikti), sd_kesim_md(K, MI._mi_sha(_sd_yol("kesim", cikti))), "kesim md")
    return K


def _sd_dep_oku(pazar: str) -> Tuple[Dict[str, np.ndarray], pd.DatetimeIndex, np.ndarray]:
    z = np.load(os.path.join(SD_YOL["yo_ham"], f"ham_{pazar}.npz"))
    return {c: z[c] for c in ("O", "H", "L", "C", "POS", "off")}, pd.DatetimeIndex(z["tarih"]), z["sembol"]


def sd_kesim_md(K: Dict[str, Any], sha: str) -> str:
    s = [f"# SD KESİM — keşif (ABD 2016-19) kümeleri ve seçim ({K['zaman']})", "",
         "Doğrulama (ABD 2020-22, AVR) sonuçları HİÇ hesaplanmadan önce commit + push edilir. Merkezler sd_kesim.json'da (standart ve ham birimde).", "",
         f"KESIM_JSON_SHA: {sha}", f"SD_KOD_SHA: {K['kod_sha']}", f"SD_ESIK_SHA: {K['esik_sha']}", f"STANDART_SHA: {K['standart_sha']}",
         f"Ön kayıt commit: {K['kapi']['onkayit_commit']}", ""]
    for Lw, L_ in K["L"].items():
        sec = L_["secim"]; oz = {o["kume"]: o for o in L_["kume"]}
        s += [f"## L{Lw}: {L_['n']} keşif penceresi, 60 küme ({L_['adim']} Lloyd adımı), aday küme {sec['aday']}", "",
              "| seçim | küme | keşif sırası | n | farklı ay | Z15 | R15 % | HEDEF | AYNA | şekil (merkez) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for ad, ls in (("EN İYİ", sec["iyi"]), ("EN KÖTÜ", sec["kotu"])):
            for c in ls:
                o = oz[c]
                s.append(f"| {ad} | {c} | {o['sira']} | {o['n']} | {o['ay']} | {_f(o['Z15'], 3)} | {_f(o['R15'], 2, True)} | {_f(o['HEDEF'], 3)} | "
                         f"{_f(o['AYNA'], 3)} | {o['tarif']} |")
        s += ["", "Bütün kümeler (keşif): küme / n / Z15", "", " ".join(f"{o['kume']}:{o['n']}/{_f(o['Z15'], 3)}" for o in L_["kume"]), ""]
        if "cemal" in L_:
            c = L_["cemal"]
            s.append(f"Cemal'in günlük bölgeleri (L{Lw} penceresi, bolge_son'da biten):")
            for sn, o in c["ozet"].items():
                s.append(f"- {sn}: {o['n']} / {o['n_tum']} atandı; ilk 5 küme [küme, n, pay, keşif sırası]: {o['ilk5']}; seçilen iyi 5 payı {_f(o['secilen_iyi_pay'], 2)}, "
                         f"kötü 5 payı {_f(o['secilen_kotu_pay'], 2)}; pazar {o['pazar']}")
            s.append(f"- APPN: {c['appn']}")
            s.append("")
    return "\n".join(s) + "\n"


def _f(x: Any, n: int = 2, yuzde: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    v = float(x) * (100 if yuzde else 1)
    return f"{v:.{n}f}".replace(".", ",")


# ================================================================ 12) DOĞRULAMA (bir kez)
def sd_sinama1(P: Dict[str, Any], R: Dict[str, np.ndarray], Sstd: Dict[str, Any], Lw: int, q_hucre: str, tanimlar: List[str],
               isci: int = 4, kayit: Optional[str] = None) -> Dict[str, Any]:
    """Bir pazar x L: her tanımlayıcı (A, B, 0, R = rastgele) için TAHMİN; IC, farklar, ÜST / ALT, yol benzerliği. R: bütün satırların sonuçları."""
    ok = P[f"ok{Lw}"] & np.isfinite(R["Z15"]); q = np.flatnonzero(ok & (P["hucre"] == q_hucre)); hv = np.flatnonzero(ok)
    j, tr, s15, ay = P["j"], P["t_row"], P["s15_row"], P["ay"]
    Z = R["Z15"]; Y = R["YOL"]; T: Dict[str, np.ndarray] = {}; YK: Dict[str, np.ndarray] = {}; den = {}; hb = {}
    for t_ in tanimlar:
        t0 = time.time()
        if t_ == "R":
            I, b = sd_komsu(np.zeros((P["N"], 1), np.float32), q, hv, j, tr, s15, ay, rastgele=True, anahtar=f"{P['pazar']}|{Lw}")
        else:
            I, b = sd_komsu(sd_matris(P, Lw, t_, Sstd), q, hv, j, tr, s15, ay, isci=isci)
        den[t_] = sd_komsu_denetim(I, q, j, tr, s15, ay)
        if any(den[t_].values()):
            raise SDHata(f"K2: komşu denetimi bozuk {t_}: {den[t_]}")
        T[t_] = Z[I].mean(1); YK[t_] = Y[I].mean(1); hb[t_] = {k: v for k, v in b.items() if k != "ay"}
        sdlog.info("%s L%d %s: %d sorgu, havuz %s..%s (%.0f sn)", P["pazar"], Lw, t_, len(q), b["havuz_min"], b["havuz_max"], time.time() - t0)
    if kayit:
        np.savez(kayit, sorgu=q, **{f"T_{k}": v for k, v in T.items()})
    zq = Z[q]; aq = ay[q]; out: Dict[str, Any] = {"n": int(len(q)), "ay": int(len(np.unique(aq))), "denetim": den, "havuz": hb, "ic": {}, "fark": {}}
    icm = {t_: sd_ic_ay(T[t_], zq, aq) for t_ in tanimlar}
    for t_ in tanimlar:
        out["ic"][t_] = sd_boot_ic(icm[t_], f"{P['pazar']}|{Lw}|ic|{t_}")
    for a1, a2 in (("A", "0"), ("B", "A"), ("A", "R")):
        if a1 in icm and a2 in icm:
            d = (icm[a1] - icm[a2]).dropna(); out["fark"][f"{a1}-{a2}"] = sd_boot_ic(d, f"{P['pazar']}|{Lw}|fark|{a1}-{a2}")
    # ÜST / ALT (A'nın TAHMİN'i; ötekiler bilgi)
    TF = R["TF"][q]
    out["uc"] = {}
    for t_ in [x for x in tanimlar if x != "R"]:
        us, al = sd_uc_maske(T[t_], aq); mk = {"UST": us, "ALT": al, "HEPSI": np.ones(len(q), bool)}; o = {}
        for ad, x in (("Z15", zq), ("R15", R["R15"][q]), ("HEDEF", R["HEDEF"][q]), ("AYNA", R["AYNA"][q]), ("TF", TF)):
            bg = sd_boot_grup(x, aq, mk, f"{P['pazar']}|{Lw}|uc|{t_}|{ad}", farklar=[("UST", "ALT")]); bg.pop("_dag")
            o[ad] = bg
        out["uc"][t_] = o
    # yol benzerliği
    out["yol"] = {}
    for t_ in tanimlar:
        rb = sd_yol_benzer(Y[q], YK[t_]); bg = sd_boot_grup(rb, aq, {"HEPSI": np.isfinite(rb)}, f"{P['pazar']}|{Lw}|yol|{t_}"); bg.pop("_dag")
        out["yol"][t_] = bg["HEPSI"]
    return out


def sd_hukum1(o: Dict[str, Any], avr_ic: Optional[float]) -> Dict[str, Any]:
    a = o["ic"]["A"]; d = o["fark"]["A-0"]; ua = o["uc"]["A"]["Z15"]["UST-ALT"]
    p = lambda r: r["ic"] is not None and r["ic"] > 0 and r["alt"] is not None and r["alt"] > 0  # noqa: E731
    k1 = p(a); k2 = p(d); k3 = ua["ort"] is not None and ua["ort"] > 0 and ua["alt"] is not None and ua["alt"] > 0; k4 = avr_ic is not None and avr_ic > 0
    if k1 and k2 and k3 and k4:
        h = "ŞEKİL BİLGİ TAŞIYOR"
    elif k1 and not k2:
        h = "BASİT KONUMDAN FAZLASI YOK"
    elif not k1:
        h = "ŞEKİL BİLGİ TAŞIMIYOR"
    else:
        h = "ARA: " + ", ".join(x for x, ok_ in (("ÜST - ALT", k3), ("AVR IC(A) işareti", k4)) if not ok_) + " tutmadı"
    hb = None
    if "B-A" in o["fark"]:
        hb = "HACİM EKLİYOR" if p(o["fark"]["B-A"]) else "HACİM EKLEMİYOR"
    return {"hukum": h, "hacim": hb, "sart": {"IC_A": k1, "A-0": k2, "UST-ALT": k3, "AVR": k4}}


def sd_sinama2(P: Dict[str, Any], R: Dict[str, np.ndarray], Sstd: Dict[str, Any], KL: Dict[str, Any], Lw: int, hucre: str) -> Dict[str, Any]:
    """Bir hücre: pencereler en yakın merkeze; bütün kümeler için Z15 / R15 / HEDEF / AYNA / TF (ay kümeli); seçilenler için tek yönlü p."""
    ok = P[f"ok{Lw}"] & np.isfinite(R["Z15"]) & (P["hucre"] == hucre); ii = np.flatnonzero(ok)
    if not len(ii):
        return {"n": 0}
    lab = sd_ata(sd_matris(P, Lw, "A", Sstd)[ii].astype(float), np.array(KL["merkez"])); ay = P["ay"][ii]
    out: Dict[str, Any] = {"n": int(len(ii)), "kume": {}}
    sec = set(KL["secim"]["iyi"]) | set(KL["secim"]["kotu"])
    for c in range(len(KL["merkez"])):
        m = lab == c; o: Dict[str, Any] = {"n": int(m.sum())}
        if m.sum() < 2:
            out["kume"][str(c)] = o; continue
        ao = HV.hv25_ay_ozet(pd.DatetimeIndex(P["giris"][ii][m]).strftime("%Y-%m-%d").tolist()); o.update({"ay": ao["ay"], "ust3_pay": ao["ust3_pay"]})
        for ad in ("Z15", "R15", "HEDEF", "AYNA", "TF"):
            x = R[ad][ii]
            if c in sec:
                bg = sd_boot_grup(x, ay, {"K": m}, f"{P['pazar']}|{hucre}|{Lw}|kume|{c}|{ad}"); dag = bg.pop("_dag")["K"]; o[ad] = bg["K"]
                if ad == "Z15":
                    o["p_iyi"] = sd_p_tek(dag, "iyi"); o["p_kotu"] = sd_p_tek(dag, "kotu")
            else:
                v = x[m]; v = v[np.isfinite(v)]; o[ad] = {"ort": float(v.mean()) if len(v) else None, "n": int(len(v))}
        out["kume"][str(c)] = o
    return out


def sd_hukum2(KL: Dict[str, Any], V: Dict[str, Any], A: Dict[str, Any]) -> Dict[str, Any]:
    """10 seçilen küme: TUTTU / TUTMADI + BH; DESEN TUTTU (iyi 1, kötü 1)."""
    sat = []; p = []
    for ad, ls in (("iyi", KL["secim"]["iyi"]), ("kotu", KL["secim"]["kotu"])):
        for r_, c in enumerate(ls, 1):
            v = V["kume"].get(str(c), {}); a = A.get("kume", {}).get(str(c), {})
            z = v.get("Z15", {}); tf = v.get("TF", {}); az = a.get("Z15", {}).get("ort") if a.get("n", 0) >= 30 else None
            if ad == "iyi":
                t = (z.get("ort") or 0) > 0 and (z.get("alt") or -1) > 0 and (tf.get("ort") or 0) > 0 and (tf.get("alt") or -1) > 0 and az is not None and az > 0
            else:
                t = (z.get("ort") or 0) < 0 and (z.get("ust") or 1) < 0 and (tf.get("ort") or 0) < 0 and (tf.get("ust") or 1) < 0 and az is not None and az < 0
            pp = v.get("p_iyi" if ad == "iyi" else "p_kotu"); p.append(pp)
            sat.append({"secim": ad, "sira": r_, "kume": c, "tuttu": bool(t), "p": pp, "avr_z15": az, "avr_n": a.get("n", 0)})
    q = YO.yo_bh(p, float(SD_ESIK["bh_q"]))
    for s, qq in zip(sat, q):
        s["bh_q"] = qq; s["bh_gecti"] = qq is not None and qq <= float(SD_ESIK["bh_q"])
    iyi1 = next(s for s in sat if s["secim"] == "iyi" and s["sira"] == 1); kotu1 = next(s for s in sat if s["secim"] == "kotu" and s["sira"] == 1)
    return {"satir": sat, "DESEN_IYI": "DESEN TUTTU" if iyi1["tuttu"] else "DESEN TUTMADI", "DESEN_KOTU": "DESEN TUTTU" if kotu1["tuttu"] else "DESEN TUTMADI",
            "bh_gecen": [s["kume"] for s in sat if s["bh_gecti"]]}


def sd_dogrulama_hesap(PS: Dict[str, Dict[str, Any]], deps: Dict[str, Dict[str, np.ndarray]], Sstd: Dict[str, Any], K: Dict[str, Any],
                       asama: str = "dogrulama", isci: int = 4, ham: Optional[str] = None, kmeans_denet: bool = True) -> Dict[str, Any]:
    J: Dict[str, Any] = {"sinama1": {}, "sinama2": {}, "hukum1": {}, "hukum2": {}}
    RS = {}
    for p, P in PS.items():
        R = sd_sonuc(P, deps[p], asama); R["TF"] = sd_toplam_fark(R["R15"], P["j"], P["hucre"]); RS[p] = R
    if kmeans_denet:   # K11: merkezler yeniden üretilir
        P = PS["ABD"]
        for Lw in P["L"]:
            ii = np.flatnonzero((P["hucre"] == SD_ESIK["hucre"]["kesif"]) & P[f"ok{Lw}"])
            km = sd_kmeans(sd_matris(P, Lw, "A", Sstd)[ii].astype(float))
            if not np.allclose(km["merkez"], np.array(K["L"][str(Lw)]["merkez"]), rtol=0, atol=1e-9):
                raise SDHata(f"K11: L{Lw} küme merkezleri yeniden üretilemedi -> DURDU")
    for Lw in PS["ABD"]["L"]:
        L = str(Lw); KL = K["L"][L]
        a = sd_sinama1(PS["ABD"], RS["ABD"], Sstd, Lw, SD_ESIK["hucre"]["dogrulama"], ["A", "B", "0", "R"], isci,
                       os.path.join(ham, f"tahmin_ABD_L{Lw}.npz") if ham else None)
        v = sd_sinama1(PS["AVR"], RS["AVR"], Sstd, Lw, SD_ESIK["hucre"]["avr"], ["A", "0", "R"], isci,
                       os.path.join(ham, f"tahmin_AVR_L{Lw}.npz") if ham else None)
        J["sinama1"][L] = {"ABD": a, "AVR": v}; J["hukum1"][L] = sd_hukum1(a, v["ic"]["A"]["ic"])
        s2 = {h: sd_sinama2(PS[h.split("|")[0]], RS[h.split("|")[0]], Sstd, KL, Lw, h)
              for h in (SD_ESIK["hucre"]["dogrulama"], SD_ESIK["hucre"]["avr"], SD_ESIK["hucre"]["avr_bilgi"])}
        J["sinama2"][L] = s2; J["hukum2"][L] = sd_hukum2(KL, s2[SD_ESIK["hucre"]["dogrulama"]], s2[SD_ESIK["hucre"]["avr"]])
    return J


def sd_dogrulama(cikti: Optional[str] = None, ham: Optional[str] = None, isci: int = 4) -> Dict[str, Any]:
    cikti = cikti or SD_YOL["cikti"]; ham = ham or SD_YOL["ham"]
    if os.path.exists(_sd_yol("sonuc", cikti)):
        raise SDHata("sonuç zaten var (ikinci doğrulama koşusu DURUR)")
    G = sd_kapi(cikti, ham); S = G.pop("_sayim"); KK = sd_kesim_kapi(cikti)
    K = json.load(open(_sd_yol("kesim", cikti), encoding="utf-8"))
    if K["standart_sha"] != HV.hv_json_sha(S["standart"]):
        raise SDHata("standart istatistikleri kesimdekiyle aynı değil -> DURDU")
    bas = pd.Timestamp.now(tz="UTC").isoformat()
    PS = sd_yukle_hepsi(ham); deps = {p: _sd_dep_oku(p)[0] for p in SD_PAZAR}
    J = sd_dogrulama_hesap(PS, deps, S["standart"], K, "dogrulama", isci, ham)
    J.update({"surum": SD_SURUM, "baslangic": bas, "bitis": pd.Timestamp.now(tz="UTC").isoformat(), "kapi": G, "kesim_kapi": KK,
              "esik_sha": sd_esik_sha(), "kod_sha": sd_kod_sha()})
    MI._mi_jyaz(_sd_yol("sonuc", cikti), J, "sonuç")
    sd_ozet_csv(J, K, _sd_yol("ozet", cikti))
    return J


def sd_ozet_csv(J: Dict[str, Any], K: Dict[str, Any], yol: str) -> str:
    sat = []
    for L, d in J["sinama1"].items():
        for p, o in d.items():
            for t_, r in o["ic"].items():
                sat.append({"sinama": 1, "L": L, "pazar": p, "olcu": f"IC_{t_}", "deger": r["ic"], "alt": r["alt"], "ust": r["ust"], "n": o["n"], "ay": r["ay"]})
            for t_, r in o["fark"].items():
                sat.append({"sinama": 1, "L": L, "pazar": p, "olcu": f"IC_{t_}", "deger": r["ic"], "alt": r["alt"], "ust": r["ust"], "n": o["n"], "ay": r["ay"]})
            for g in ("UST", "ALT", "UST-ALT"):
                for ad in ("Z15", "R15", "HEDEF", "AYNA", "TF"):
                    r = o["uc"]["A"][ad][g]
                    sat.append({"sinama": 1, "L": L, "pazar": p, "olcu": f"A_{g}_{ad}", "deger": r["ort"], "alt": r["alt"], "ust": r["ust"], "n": r.get("n"), "ay": None})
            for t_, r in o["yol"].items():
                sat.append({"sinama": 1, "L": L, "pazar": p, "olcu": f"YOL_{t_}", "deger": r["ort"], "alt": r["alt"], "ust": r["ust"], "n": r["n"], "ay": None})
    for L, d in J["sinama2"].items():
        KL = K["L"][L]; oz = {o["kume"]: o for o in KL["kume"]}
        for h, o in d.items():
            for c in KL["secim"]["iyi"] + KL["secim"]["kotu"]:
                v = o.get("kume", {}).get(str(c), {})
                for ad in ("Z15", "R15", "HEDEF", "AYNA", "TF"):
                    r = v.get(ad, {})
                    sat.append({"sinama": 2, "L": L, "pazar": h, "olcu": f"kume{c}_{ad}", "deger": r.get("ort"), "alt": r.get("alt"), "ust": r.get("ust"),
                                "n": v.get("n"), "ay": v.get("ay"), "kesif_Z15": oz[c]["Z15"], "kesif_n": oz[c]["n"]})
    df = pd.DataFrame(sat); MI._mi_yaz(yol, df.to_csv(index=False), "özet csv")
    return yol


# ================================================================ 13) SENTETİK (Cemal'in kalıbı gömülü; N1 / N2 / N3)
def _sd_sablon() -> Dict[str, np.ndarray]:
    return {k: np.asarray(v, float) for k, v in MV.mv_sablon()["tam"]["ohlc"].items()}


def _sd_onar(O, H, L, C):
    H = np.maximum.reduce([H, O, C]); L = np.minimum.reduce([L, O, C])
    return O, H, L, C


def sd_sablon_gurultu(a: Dict[str, np.ndarray], duzey: float, rng: np.random.Generator) -> Dict[str, np.ndarray]:
    """Şablon biriminde gürültü (ortalama mum boyunun düzey katı std; O / H / L / C ayrı); H / L onarılır."""
    m = float(np.mean(a["H"] - a["L"])); out = {k: v.copy() for k, v in a.items()}
    if duzey > 0:
        for c in "OHLC":
            out[c] = out[c] + rng.normal(0, duzey * m, len(out[c]))
    out["O"], out["H"], out["L"], out["C"] = _sd_onar(out["O"], out["H"], out["L"], out["C"])
    return out


def sd_gom(tur: str, Cs: np.ndarray, a: Dict[str, np.ndarray], olcek: float, duzey: float, rng: np.random.Generator,
           egim: str = "yatay") -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Bir olayın 20 barlık O / H / L / C'si (fiyat): Cs = olaydan önceki kapanışlar (en az 20). Bant ölçeğine eşleme (SMA20, sigma20 son önceki bardan)."""
    Lw = len(a["C"]); sma = float(np.mean(Cs[-20:])); sg = float(np.std(Cs[-20:])) or 1e-3
    sg0 = float((a["BU"][0] - a["BO"][0]) / 2.0); f = sg / sg0 * olcek; b0 = float(a["BO"][0]); mboy = float(np.mean(a["H"] - a["L"]))
    g = sd_sablon_gurultu(a, duzey, rng)
    fy = lambda x: sma + (x - b0) * f  # noqa: E731
    if tur == "POZ":
        O, H, L, C = (fy(g[c]) for c in "OHLC")
    elif tur == "N1":                 # aynı kapanış yolu; iri gövde, üst fitil yok
        C = fy(g["C"]); pc = np.r_[fy(g["C"][0]) - (g["C"][1] - g["C"][0]) * f, C[:-1]]
        yon = np.sign(C - pc); yon[yon == 0] = 1.0
        O = C - yon * mboy * f; H = np.maximum(O, C); L = np.minimum(O, C) - 0.05 * mboy * f
    elif tur == "N2":                 # aynı mum biçimi; yatay / düşen kapanış yolu
        c0 = fy(g["C"][0]); top = float(g["C"].max() - g["C"].min()) * f
        yol = np.full(Lw, c0) if egim == "yatay" else c0 - top * np.arange(Lw) / (Lw - 1)
        yol = yol + rng.normal(0, 0.15 * mboy * f, Lw)
        C = yol; O = C + (g["O"] - g["C"]) * f; H = C + (g["H"] - g["C"]) * f; L = C + (g["L"] - g["C"]) * f
    else:
        raise SDHata(f"sentetik tür: {tur}")
    O, H, L, C = _sd_onar(np.asarray(O, float), np.asarray(H, float), np.asarray(L, float), np.asarray(C, float))
    if (L <= 0).any():
        raise SDHata("sentetik: eksi fiyat")
    return O, H, L, C


def sd_sentetik_panel(tohum: int, n_hisse: Optional[int] = None, n_bar: Optional[int] = None, gom: bool = True, sig: float = 0.02,
                      z_ek: Optional[float] = None) -> Dict[str, Any]:
    """Yapay pazar: rastgele yürüyüş; gom=True ise Cemal'in kalıbı (POZ, sonrasında +Z_ek sürüklenme) ve N1 / N2 (ilişkisiz) gömülür.
    Dönüş: dep (O, H, L, C, V, POS, off), tarih, sembol, X (YO örnek satırları gibi), olay tablosu."""
    E = SD_ESIK["sentetik"]; n_hisse = int(n_hisse or E["hisse"]); n_bar = int(n_bar or E["bar"]); z_ek = float(E["Z_ek"] if z_ek is None else z_ek)
    rng = np.random.default_rng([int(SD_ESIK["tohum"]["sentetik"]), int(tohum)]); a = _sd_sablon(); Lw = len(a["C"]); U = int(SD_ESIK["devam"]["ufuk"])
    tarih = pd.bdate_range("2015-01-02", periods=n_bar); _sd_tarih_kapi(tarih, "sentetik")
    parca = {c: [] for c in ("O", "H", "L", "C", "V")}; olay = []; sat = []
    pay = E["pay"]; turler = list(pay.keys()); pp = np.array([pay[t] for t in turler])
    for j in range(n_hisse):
        lc = rng.normal(0, sig, n_bar); lo = rng.normal(0, sig / 2, n_bar); uh = np.abs(rng.normal(0, sig, n_bar)) * 0.6; ul = np.abs(rng.normal(0, sig, n_bar)) * 0.6
        O = np.zeros(n_bar); H = np.zeros(n_bar); L = np.zeros(n_bar); C = np.zeros(n_bar)
        ev = []
        if gom:
            k = int(E["ilk"])
            while k + U + 5 < n_bar:
                k = k - k % 5; ev.append(k); k += int(rng.integers(E["olay_ara"][0], E["olay_ara"][1] + 1))
        evd = {}
        for i, k in enumerate(ev):
            t = turler[int(rng.choice(len(turler), p=pp))]
            evd[k] = {"tur": t, "duzey": float(E["gurultu"][i % len(E["gurultu"])]) if t == "POZ" else 0.10,
                      "olcek": float(np.exp(rng.uniform(np.log(E["olcek"][0]), np.log(E["olcek"][1])))), "egim": "yatay" if rng.random() < 0.5 else "dusen"}
        bas = {k - Lw + 1: k for k in evd}; drift = np.zeros(n_bar); i = 0; pc = 20.0
        while i < n_bar:
            if i in bas:
                k = bas[i]; d = evd[k]
                o, h, l_, c = sd_gom(d["tur"], C[:i], a, d["olcek"], d["duzey"], rng, d["egim"])
                O[i:k + 1], H[i:k + 1], L[i:k + 1], C[i:k + 1] = o, h, l_, c; pc = C[k]
                atrp = YO.yo_hisse_ozellik(O[:k + 1], H[:k + 1], L[:k + 1], C[:k + 1], C[:k + 1])["ATRP20"][k]
                if d["tur"] == "POZ":
                    drift[k + 2] = np.log1p(z_ek * atrp * np.sqrt(U))     # girişten sonraki barda tek sıçrama: sonraki pencerelerin devamına taşmaz
                olay.append({"j": j, "k": k, **d, "atrp": float(atrp)}); i = k + 1; continue
            m = drift[i]
            O[i] = pc * np.exp(lo[i] + m); C[i] = pc * np.exp(lc[i] + m)
            H[i] = max(O[i], C[i]) * np.exp(uh[i]); L[i] = min(O[i], C[i]) * np.exp(-ul[i]); pc = C[i]; i += 1
        V = 1000.0 * np.exp(rng.normal(0, 0.3, n_bar))
        for c, v in (("O", O), ("H", H), ("L", L), ("C", C), ("V", V)):
            parca[c].append(v)
        F = YO.yo_hisse_ozellik(O, H, L, C, C)
        kk = YO.yo_ornek_maske(n_bar, np.arange(n_bar), np.ones(n_bar, bool), tarih)
        for k in kk:
            sat.append({"j": j, "k": int(k), "t_row": int(k), "d_row": int(k) + 1, "tarih": tarih[k], "giris": tarih[k + 1],
                        "ATRP20": F["ATRP20"][k], "F15": F["F15"][k], "KONUM120": F["KONUM120"][k]})
    dep = {c: np.concatenate(v) for c, v in parca.items()}
    dep["POS"] = np.tile(np.arange(n_bar), n_hisse).astype(np.int64); dep["off"] = np.arange(0, n_bar * (n_hisse + 1), n_bar, dtype=np.int64)
    X = pd.DataFrame(sat); X["hucre"] = [YO.yo_hucre(g, "ABD") for g in X.giris]; X["ay"] = pd.DatetimeIndex(X.giris).strftime("%Y-%m")
    return {"dep": dep, "tarih": tarih, "sembol": np.array([f"S{j:03d}" for j in range(n_hisse)]), "X": X, "olay": pd.DataFrame(olay)}


def sd_sentetik_olc(tohum: int = 1, n_hisse: Optional[int] = None, n_bar: Optional[int] = None, isci: int = 4, ilgisiz: bool = True) -> Dict[str, Any]:
    """Yöntemin gömülü panelde ve ilişkisiz panelde davranışı: yakalama (gürültü düzeyine göre), N1 / N2 / N3 yanlış kabul, kalıp kümesinin keşif sırası,
    IC (L20, A) ve küme seçimi. Yalnız sentetik; gerçek veri görülmez."""
    E = SD_ESIK["sentetik"]; out: Dict[str, Any] = {"tohum": tohum}
    for ad, gom in (("gomulu", True), ("ilgisiz", False)):
        if ad == "ilgisiz" and not ilgisiz:
            continue
        S = sd_sentetik_panel(tohum + (0 if gom else 1000), n_hisse, n_bar, gom)
        P = sd_panel_kur(S["dep"], S["tarih"], S["sembol"], S["X"], None, "SENT")
        kh = SD_ESIK["hucre"]["kesif"]; Sstd = sd_std_hepsi(P, P["hucre"] == kh)
        K = sd_kesif_hesap(P, S["dep"], Sstd, None, int(E["n_min"]), int(E["ay_min"]))
        R = sd_sonuc(P, S["dep"], "test"); R["TF"] = sd_toplam_fark(R["R15"], P["j"], P["hucre"])
        o1 = sd_sinama1(P, R, Sstd, 20, SD_ESIK["hucre"]["dogrulama"], ["A", "0", "R"], isci)
        o = {"n_pencere": int(P["ok20"].sum()), "ic": o1["ic"], "fark": o1["fark"], "ust_alt_Z15": o1["uc"]["A"]["Z15"]["UST-ALT"]}
        if gom:
            ol = S["olay"]; key = {(int(r.j), int(r.k)): r for r in ol.itertuples()}
            ok = P["ok20"]; ii = np.flatnonzero(ok)
            lab = sd_ata(sd_matris(P, 20, "A", Sstd)[ii].astype(float), np.array(K["L"]["20"]["merkez"]))
            tur = np.array([key[(int(P["j"][i]), int(P["k"][i]))].tur if (int(P["j"][i]), int(P["k"][i])) in key else "N3" for i in ii])
            duz = np.array([key[(int(P["j"][i]), int(P["k"][i]))].duzey if (int(P["j"][i]), int(P["k"][i])) in key else np.nan for i in ii])
            kes = P["hucre"][ii] == kh
            vp = pd.Series(lab[(tur == "POZ") & kes]).value_counts(); kk = int(vp.index[0])
            sec = K["L"]["20"]["secim"]
            o["kalip_kume"] = kk; o["kalip_sira"] = sec["sira"].get(kk); o["kalip_en_iyi5"] = kk in sec["iyi"]
            o["kalip_kume_poz_pay"] = float((tur[lab == kk] == "POZ").mean())
            o["yakalama"] = {f"{d:.2f}": float((lab[(tur == "POZ") & (duz == d)] == kk).mean()) for d in E["gurultu"]}
            o["yakalama_hepsi"] = float((lab[tur == "POZ"] == kk).mean())
            ilk3 = [int(x) for x in vp.index[:3]]
            o["yakalama_ilk3"] = float(np.isin(lab[tur == "POZ"], ilk3).mean())
            o["yanlis_kabul"] = {t: float((lab[tur == t] == kk).mean()) for t in ("N1", "N2", "N3")}
            o["yanlis_kabul_ilk3"] = {t: float(np.isin(lab[tur == t], ilk3).mean()) for t in ("N1", "N2", "N3")}
            o["olay_say"] = ol.tur.value_counts().to_dict()
            o["iyi5"] = sec["iyi"]; o["kotu5"] = sec["kotu"]
            o["iyi5_poz_pay"] = float((tur[np.isin(lab, sec["iyi"])] == "POZ").mean()); o["genel_poz_pay"] = float((tur == "POZ").mean())
            # en yakın olaya göre konum (pencere sonu - olay sonu): -15..-1 = kalıbın ERKEN evresi (devamı kalıbın kendi kalan kısmı)
            ofs = np.full(len(ii), 10 ** 6); ytur = np.full(len(ii), "N3", dtype="<U3")
            for jj, g_ in ol.groupby("j"):
                m_ = P["j"][ii] == jj; ek_ = g_.k.to_numpy(); d_ = P["k"][ii][m_][:, None] - ek_[None, :]; a_ = np.argmin(np.abs(d_), axis=1)
                ofs[m_] = d_[np.arange(len(a_)), a_]; ytur[m_] = g_.tur.to_numpy()[a_]
            erken = (ofs >= -15) & (ofs <= -1); iy = np.isin(lab, sec["iyi"])
            o["iyi5_erken_pay"] = float(erken[iy].mean()); o["iyi5_tam_kalip_pay"] = float(((ofs == 0) & (ytur == "POZ"))[iy].mean())
            o["iyi5_bilesim"] = {c: pd.Series([f"{t}{int(x):+d}" for t, x in zip(ytur[lab == c], ofs[lab == c])]).value_counts().iloc[:3].to_dict()
                                 for c in sec["iyi"]}
        out[ad] = o
    return out


def sd_sentetik_kos(cikti: Optional[str] = None, isci: int = 4) -> Dict[str, Any]:
    cikti = cikti or SD_YOL["cikti"]; J = sd_sentetik_olc(1, isci=isci)
    J.update({"surum": SD_SURUM, "esik_sha": sd_esik_sha(), "zaman": pd.Timestamp.now(tz="UTC").isoformat()})
    MI._mi_jyaz(_sd_yol("sentetik", cikti), J, "sentetik")
    sd_yapay_pdf(J, _sd_yol("yapay_pdf", cikti))
    return J


# ================================================================ 14) GÖRSEL
def _sd_plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def _sd_yapay_baslik(fig, alt: str) -> None:
    fig.text(0.5, 0.975, "YAPAY VERİ", ha="center", va="top", fontsize=34, weight="bold", color="#b30000")
    fig.text(0.5, 0.925, alt, ha="center", va="top", fontsize=15)


def _sd_seri_ciz(ax, O, H, L, C, kutu, baslik, sonra_bas: Optional[int] = None, sonra_yazi: str = "") -> None:
    BU, BO, BA = MI.mi_bant(C)
    MV._mv_ciz(ax, O, H, L, C, BU, BO, BA, kutu, "")
    ax.set_title(baslik, fontsize=13, weight="bold")
    if sonra_bas is not None:
        ax.axvspan(sonra_bas - 0.5, len(C) - 0.5, color="#4daf4a", alpha=0.12, zorder=0)
        ax.text(sonra_bas + 0.3, np.nanmin(L), sonra_yazi, fontsize=11, va="bottom", color="#1b5e20", weight="bold")


def sd_yapay_pdf(J: Dict[str, Any], yol: str) -> str:
    """SD_YAPAY_DESEN.pdf: s1 kalıp (gürültüsüz + 3 gürültü), s2 3 gömülü seri (sonrası dahil, bilerek +0,5), s3 N1 / N2 / N3, s4 sonuç tablosu."""
    plt = _sd_plt()
    from matplotlib.backends.backend_pdf import PdfPages
    a = _sd_sablon(); rng = np.random.default_rng([int(SD_ESIK["tohum"]["sentetik"]), 99])
    S = sd_sentetik_panel(int(J.get("tohum", 1)), 40, 900, True)
    dep, ol = S["dep"], S["olay"]; off = dep["off"]; once = 40; U = 15

    def seri(r, sonra=True):
        a0 = int(off[r.j]); s = r.k - 19; b0 = max(0, s - once); e = r.k + (U + 1 if sonra else 1)
        sl = slice(a0 + b0, a0 + e)
        return [np.asarray(dep[c][sl], float) for c in "OHLC"], (s - b0, r.k - b0), r.k + 1 - b0
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with PdfPages(yol, metadata={"Title": "SD yapay desen", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7)); _sd_yapay_baslik(fig, "Gömülen desen = senin kalıbın (20 mum, Bollinger çizgileriyle)")
        for i, d in enumerate(SD_ESIK["sentetik"]["gurultu"]):
            g = sd_sablon_gurultu(a, d, rng); ax = fig.add_axes([0.06 + (i % 2) * 0.47, 0.50 - (i // 2) * 0.40, 0.42, 0.33])
            MV._mv_ciz(ax, g["O"], g["H"], g["L"], g["C"], g["BU"], g["BO"], g["BA"], None, "")
            ax.set_title("gürültüsüz" if d == 0 else f"%{d * 100:.0f} gürültü", fontsize=16, weight="bold")
        fig.text(0.5, 0.05, "Gürültü = mumlara rastgele sapma (ortalama mum boyunun yüzdesi). Yapay serilere bu dört hali\n"
                            "farklı büyüklükte (x0,5 .. x2) koyduk.", ha="center", fontsize=13)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); _sd_yapay_baslik(fig, "Kalıbın gömüldüğü 3 yapay seri (turuncu kutu = kalıp)")
        poz = ol[ol.tur == "POZ"]; ex = [poz[poz.duzey == d].iloc[0] for d in (0.0, 0.10, 0.20)]
        for i, r in enumerate(ex):
            (O, H, L, C), kutu, sb = seri(r, True)
            _sd_seri_ciz(fig.add_axes([0.06, 0.64 - i * 0.29, 0.88, 0.23]), O, H, L, C, kutu, f"Örnek {i + 1}: gürültü %{r.duzey * 100:.0f}, büyüklük x{r.olcek:.2f}",
                         sb, "SONRASI:\nbilerek\n+0,5 koyduk")
        fig.text(0.5, 0.04, "Yapay veri olduğu için sonrası gösteriliyor (yeşil alan). Gerçek veride sonrası hiç gösterilmez.", ha="center", fontsize=12)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); _sd_yapay_baslik(fig, "Negatifler: kalıba benzemesi GEREKMEYENLER (sonrasında ilişki yok)")
        yazi = {"N1": "N1: aynı yol (aynı kapanışlar), ama mumlar iri gövdeli ve üst fitilsiz.",
                "N2": "N2: aynı mum biçimi (küçük gövde, uzun üst fitil), ama yol yatay ya da düşen.",
                "N3": "N3: hiçbir şey gömülmemiş rastgele yürüyüş."}
        for i, t in enumerate(("N1", "N2", "N3")):
            ax = fig.add_axes([0.06, 0.64 - i * 0.29, 0.88, 0.21])
            if t == "N3":
                k3 = int(ol.iloc[3].k) - 35; j3 = int(ol.iloc[3].j)   # önceki olayın sürüklenmesinden sonra, sonraki olaydan önce
                (O, H, L, C), kutu, _ = seri(pd.Series({"j": j3, "k": k3}), False)
            else:
                (O, H, L, C), kutu, _ = seri(ol[ol.tur == t].iloc[0], False)
            _sd_seri_ciz(ax, O, H, L, C, kutu, yazi[t].split(":")[0])
            fig.text(0.5, 0.62 - i * 0.29, yazi[t], ha="center", fontsize=13)
        pdf.savefig(fig); plt.close(fig)
        fig = plt.figure(figsize=(8.3, 11.7)); _sd_yapay_baslik(fig, "Sonuç: yöntem yapay veride ne yaptı?")
        g = J["gomulu"]; n = J.get("ilgisiz", {})
        ic = lambda r: f"{_f(r['ic'], 3)} [{_f(r['alt'], 3)} / {_f(r['ust'], 3)}]"  # noqa: E731
        satir = [("Kalıbı aynı kümeye topladı mı (yakalama)", ""),
                 *[(f"   gürültü %{float(d) * 100:.0f}", f"%{v * 100:.0f}") for d, v in g["yakalama"].items()],
                 ("   en kalabalık 3 kümeye (hepsi)", f"%{g['yakalama_ilk3'] * 100:.0f}"),
                 ("Negatifleri aynı kümeye soktu mu (yanlış kabul)", ""),
                 *[(f"   {t}", f"%{v * 100:.0f}") for t, v in g["yanlis_kabul"].items()],
                 ("Kalıbın kümesi keşifte kaçıncı (60 küme)", f"{g['kalip_sira']}. ({'en iyi 5 içinde' if g['kalip_en_iyi5'] else 'en iyi 5 dışında'})"),
                 ("En iyi 5 kümede kalıbın ERKEN hali (bitişten 1-15 mum önce)", f"%{g['iyi5_erken_pay'] * 100:.0f}"),
                 ("Benzer şekil -> benzer devam (IC), kalıp gömülü", ic(g["ic"]["A"])),
                 ("IC, hiçbir şey gömülmemiş (ilişkisiz) veri", ic(n["ic"]["A"]) if n else "—"),
                 ("IC, rastgele komşu (şans)", ic(g["ic"]["R"]))]
        for i, (s1, s2) in enumerate(satir):
            y = 0.84 - i * 0.042
            fig.text(0.06, y, s1, fontsize=14, weight="bold" if not s1.startswith("   ") else "normal"); fig.text(0.94, y, s2, fontsize=14, ha="right")
        uyar = []
        for t, v in g["yanlis_kabul"].items():
            if v > 0.30:
                uyar.append(f"{t}'in %{v * 100:.0f}'i kalıbın kümesine düştü: tanımlayıcı " + ("mum yapısını" if t == "N1" else "gidişi" if t == "N2" else "rastgeleyi") + " ayırt etmiyor.")
        fig.text(0.06, 0.20, "\n".join(uyar) if uyar else "Negatiflerin hiçbiri %30'dan fazla kalıbın kümesine düşmedi.", fontsize=13, color="#8b0000" if uyar else "#1b5e20",
                 va="top", wrap=True)
        fig.text(0.06, 0.15, "Not: kalıbın kendisi alt banttan üst banda yükseliyor. Kalıbın ilk yarısını gören\npencere, devamında kalıbın kalan "
                             "yükselişini görür; bu yüzden 'en iyi' kümeler\nkalıbın ERKEN hali çıktı (kalıbın parası kalıbın içinde).", fontsize=11.5, va="top")
        fig.text(0.06, 0.07, "IC = benzer şekli olanların devamı ile gerçek devamın sıra ilişkisi (0 = ilişki yok).", fontsize=11, va="top")
        pdf.savefig(fig); plt.close(fig)
    return yol


def sd_desen_pdf(J: Dict[str, Any], K: Dict[str, Any], yol: str, Lw: int = 20) -> str:
    """SD_DESENLER.pdf: kapak (SINAMA 1 tek cümle) + seçilen 10 küme (merkez + keşiften 6 gerçek örnek, SONRASI YOK)."""
    plt = _sd_plt()
    from matplotlib.backends.backend_pdf import PdfPages
    import MUM_IZI_HAKEM as HK
    L = str(Lw); KL = K["L"][L]; oz = {o["kume"]: o for o in KL["kume"]}; P = sd_panel_oku(_sd_ham("ozellik_ABD.npz")); dep, tarih, S = _sd_dep_oku("ABD")
    Sstd = json.load(open(_sd_ham("sayim.json"), encoding="utf-8"))["standart"]
    ii = np.flatnonzero((P["hucre"] == SD_ESIK["hucre"]["kesif"]) & P[f"ok{Lw}"])
    lab = sd_ata(sd_matris(P, Lw, "A", Sstd)[ii].astype(float), np.array(KL["merkez"]))
    V = J["sinama2"][L][SD_ESIK["hucre"]["dogrulama"]]["kume"]; H2 = {s["kume"]: s for s in J["hukum2"][L]["satir"]}
    h1 = J["hukum1"]
    with PdfPages(yol, metadata={"Title": "SD desenler", "CreationDate": None, "ModDate": None}) as pdf:
        fig = plt.figure(figsize=(8.3, 11.7))
        fig.text(0.5, 0.95, "Verinin kendi desenleri", ha="center", fontsize=26, weight="bold")
        a20 = J["sinama1"]["20"]["ABD"]["ic"]["A"]; a10 = J["sinama1"]["10"]["ABD"]["ic"]["A"]
        fig.text(0.07, 0.88, f"Benzer şekil benzer devam getiriyor mu? 20 mum: {h1['20']['hukum']} (IC {_f(a20['ic'], 3)}); "
                             f"10 mum: {h1['10']['hukum']} (IC {_f(a10['ic'], 3)}).", fontsize=13, va="top", wrap=True)
        fig.text(0.07, 0.78, "Sonraki 10 sayfa: 2016-19'da en iyi 5 ve en kötü 5 devam eden şekil kümesi (20 mum).\nHer sayfada: kümenin ortalama şekli "
                             "(bant çizgilerine göre) + o kümeden 6 gerçek örnek.\nGerçek örneklerde SONRASI YOK. En altta: 2016-19 ve 2020-22 sonucu.\n"
                             "Z = 15 günlük getiri / hissenin olağan oynaklığı (0 = sıradan).", fontsize=12, va="top")
        pdf.savefig(fig); plt.close(fig)
        for ad, ls in (("EN İYİ", KL["secim"]["iyi"]), ("EN KÖTÜ", KL["secim"]["kotu"])):
            for r_, c in enumerate(ls, 1):
                fig = plt.figure(figsize=(8.3, 11.7)); o = oz[c]; h = np.array(KL["merkez_ham"][c]); Bm = h[:4 * Lw].reshape(Lw, 4)
                fig.text(0.5, 0.975, f"{ad} {r_}. küme (no {c})", ha="center", va="top", fontsize=22, weight="bold")
                fig.text(0.05, 0.935, o["tarif"], fontsize=10.5, va="top", wrap=True)
                ax = fig.add_axes([0.08, 0.66, 0.84, 0.21])
                MV._mv_ciz(ax, Bm[:, 0], Bm[:, 1], Bm[:, 2], Bm[:, 3], np.ones(Lw), np.zeros(Lw), -np.ones(Lw), None, "")
                ax.set_title("Ortalama şekil (üst çizgi = üst bant, kesikli = SMA20, alt = alt bant)", fontsize=11)
                uy = ii[lab == c]; rng = _sd_rng("ornek", f"L{Lw}|{c}"); sec = rng.choice(uy, size=min(int(SD_ESIK["pdf"]["ornek"]), len(uy)), replace=False)
                for e, ri in enumerate(sorted(sec, key=lambda x: P["tarih"][x])):
                    jj = int(P["j"][ri]); k = int(P["k"][ri]); a0 = int(dep["off"][jj]); s = k - Lw + 1; b0 = max(0, s - int(SD_ESIK["pdf"]["once"]))
                    sl = slice(a0 + b0, a0 + k + 1)
                    O_, H_, L_, C_ = (np.asarray(dep[cc][a0:a0 + k + 1], float) for cc in ("O", "H", "L", "C"))
                    assert len(C_) == k + 1, "geleceğe bakma kapısı: pencere sonundan sonraki bar çizime girdi"
                    BU, BO, BA = MI.mi_bant(C_); w = slice(b0, k + 1)
                    axe = fig.add_axes([0.04 + (e % 2) * 0.48, 0.44 - (e // 2) * 0.17, 0.40, 0.135])
                    HK._hk_grafik_gecmis(axe, O_[w], H_[w], L_[w], C_[w], BU[w], BO[w], BA[w], (s - b0, k - b0), float(C_[k]), HK.HK_ESIK_OLCEK, True,
                                         f"{S[jj]} {pd.Timestamp(P['tarih'][ri]).date()}")
                    axe.title.set_fontsize(10)
                    for tl in axe.get_yticklabels():
                        tl.set_fontsize(8)
                    del sl
                v = V.get(str(c), {}); z = v.get("Z15", {}); tf = v.get("TF", {}); r15 = v.get("R15", {}); hh = H2.get(c, {})
                fig.text(0.05, 0.075, f"2016-19: Z {_f(o['Z15'], 2)}, 15 günde ort. %{_f(o['R15'], 1, True)} ({o['n']} pencere).", fontsize=12)
                fig.text(0.05, 0.045, f"2020-22: Z {_f(z.get('ort'), 2)} [{_f(z.get('alt'), 2)} / {_f(z.get('ust'), 2)}], ort. %{_f(r15.get('ort'), 1, True)}, "
                                      f"hissenin olağanına göre %{_f(tf.get('ort'), 1, True)} -> {'TUTTU' if hh.get('tuttu') else 'TUTMADI'}", fontsize=12, weight="bold")
                pdf.savefig(fig); plt.close(fig)
    return yol


# ================================================================ 15) ÖN KAYIT / RAPOR METİNLERİ
SD_YORUM = [
    "Pencere sonları YO örnek satırlarıdır (YO_ON_KAYIT yorum 1-4: k % 5 == 0, giriş k + 1 barı P2, giriş 2016-22, 15. bar kesik içinde); SEKIL_DEVAM yeni örneklem "
    "kurmaz, YO panel dosyalarını sha denetimiyle içe alır. L10 ve L20 aynı pencere sonlarını kullanır.",
    "Bant koordinatı MI.mi_bant ile: sigma ddof 0 (MUM_IZI / UC / HAKEM ile aynı); b = (fiyat - SMA20) / (BU - SMA20); BU = SMA20 ise pencere TANIMSIZ.",
    "Ek 4 sayı kırpılmaz (iş tanımı kırpmayı yalnız b ve göreli hacim için yazdı); 'pencere içi bant genişliği değişimi' = bw_k / bw_s - 1 (UC DARALMA tanımı); "
    "'önceki 60 barın en yükseğinden pencere dibine düşüş (ATR birimi)' = (min L pencere - maks H önceki 60) / (ATRP20_k x C_k) (eksi = düşüş).",
    "Göreli hacim: medyan önceki 60 barın (i hariç) hacmi; hacim sütunu MI.mi_veri açık kopyasında var (Volume; V > 0 geçerli bar şartı) -> TANIMLAYICI B koşulur.",
    "Geçerlilik: A, B ve 0 aynı pencere kümesinde; bir pencerenin A'sı geçerli, B'si geçersiz olamaz (eşli IC farkı için); önceki 60 bar şartı (s - 60 >= 0).",
    "Kilit kuralı: pencerenin takvim aralığında geçersiz bar payı > 0,20 -> KILITLI (UC_ESIK atma KILITLI; uc_kilitli_pay içe alınır). Cemal bölgelerine uygulanmaz.",
    "Standartlaştırma ABD keşif (2016-19) geçerli pencerelerinin ortalama / std'si ile; AVR de aynı istatistiklerle (AVR'ye özel ölçek yok; yön sınaması).",
    "Komşu havuzu (yalnız geçmiş): sorgular giriş ayına göre gruplanır; r0 = grubun en küçük pencere sonu satırı; havuz = t_row <= r0 - 20 VE 15. sonuç barının "
    "satırı < r0 VE başka hisse. Böylece her komşu her sorgudan >= 20 satır önce biter ve devamı sorgu gününden önce bilinir. Havuz ayda bir güncellenir; "
    "ABD doğrulamasının havuzu 2016'dan başlar (keşif pencereleri + doğrulamanın geçmiş pencereleri). Sorgular seyreltilmez (her 5 barda bir; hesap yetiyor).",
    "Komşu araması tam (yaklaşık değil): float32 |y|^2 - 2xy sıralaması, argpartition; eşit uzaklıklar sırası belirsiz (etkisi yok sayılır).",
    "IC: her giriş ayında >= 30 sorgu; aylık Spearman; IC = ayların eşit ağırlıklı ortalaması; bootstrap ayları yerine koyarak (B 10.000, tohum 271). IC farkları "
    "aynı ayların aylık farklarıyla.",
    "ÜST / ALT: her giriş ayında TAHMİN'in kesit sırası (ortalama sıra / n) > 0,90 / <= 0,10 (aylık kesit: piyasa zamanlaması dışlanır); ölçüler pencere "
    "ağırlıklı (ay kümeli oran).",
    "TOPLAM FARK = R15 - aynı hissenin aynı hücrede (pazar x dönem) bütün YO örnek pencerelerinin (tanımlayıcısı geçersizler dahil) R15 ortalaması (YO yorum 10 gibi).",
    "AVR: SINAMA 1 sorguları AVR 2020-22 (havuz AVR 2016'dan; AVR'nin kendi geçmişi); SINAMA 2 AVR şartı AVR 2020-22 ortalama Z15 işareti (n >= 30); AVR 2016-19 bilgi. "
    "AVR'de TANIMLAYICI B koşulmaz (iş tanımı AVR için yalnız IC(A) istiyor; 0 ve rastgele bilgi).",
    "Küme seçimi yalnız keşif Z15'iyle; aday n >= 1000 ve ay >= 12; L10 için de aynı seçim (5 / 5) yapılır ve SD_KESIM'e yazılır; PDF yalnız L20'nin 10 kümesi.",
    "Doğrulamada bütün 60 kümenin sonucu bilgi olarak hesaplanır (Cemal bölgelerinin ve APPN'nin düştüğü kümelerin sonucunu yazmak için); hüküm yalnız seçilen 10'da.",
    "Cemal bölgeleri: mum_izi23_olay.csv günlük satırları (EVET 36: ABD 23, BIST 12, AVR 1; KISMEN / HAYIR bilgi); pencere = bolge_son barında biten 20 bar "
    "(bölge 16-24 bar; sabit pencere uzunluğu iş tanımı gereği); APPN SOL = 2021-06-07'de biten 20 bar, SAĞ = 2021-09-07'de biten 20 bar. Atama keşifte (getirisiz).",
    "PDF örnekleri keşif üyelerinden (tohum 274); çizim pencere sonu k'de biter (assert); hisse adı ve tarih yazılır (iş tanımı izin verdi).",
    "Sentetik ek (koordinatörün iletisi, gerçek sonucu etkilemez): Cemal'in kalıbı (MV.mv_sablon 'tam' 20 mum) gömülü panel + N1 / N2 / N3; sonuçlar sd_sentetik.json ve "
    "SD_YAPAY_DESEN.pdf; sentetikte aday küme şartı n >= 30 ve ay >= 12.",
]


def sd_onkayit_yaz(cikti: Optional[str] = None, ham: Optional[str] = None) -> str:
    import IZ_KARNE as IK
    cikti = cikti or SD_YOL["cikti"]; S = json.load(open(_sd_ham("sayim.json", ham), encoding="utf-8")); Jh = json.load(open(_sd_ham("hazirla_log.json", ham), encoding="utf-8"))
    sh = sd_dosya_sha(ham)
    s = [f"# SD ÖN KAYIT — benzer şekil benzer devam mı + verinin kendi desenleri ({pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%dT%H:%M:%SZ')})", "",
         "İş tanımı SD_IS_TANIMI.md (ana model). Bu dosya Z15 / R15 / HEDEF / AYNA HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, "
         "hüküm kuralları sonra değişmez (değişirse SAPMA). K, küme sayısı, pencere uzunluğu için ikinci değer denenmez. Evren bugün yaşayan hisseler. KASA açılmaz "
         "(veri <= 2022-12-31).", "", "## Mühürler", "",
         f"SD_KOD_SHA: {sd_kod_sha()}", f"SD_ESIK_SHA: {sd_esik_sha()}", *[f"DOSYA_{a}: {v}" for a, v in sh.items()],
         f"SAYIM_SHA: {HV.hv_json_sha(S)}", f"STANDART_SHA: {HV.hv_json_sha(S['standart'])}", f"IS_TANIMI_SHA: {MI._mi_sha(SD_YOL['is_tanimi'])}",
         *[f"YO_{a}: {v}" for a, v in Jh["yo_panel"].items()], "",
         f"- Panel dosyaları (repo dışı): {SD_YOL['ham']} (ozellik_*.npz = pencere meta + tanımlayıcılar, sonuç sütunu YOK; cemal_tanim.pkl; sayim.json)", "",
         "## GETİRİSİZ SAYIM (Z15 / R15 hesaplanmadı)", "",
         "| hücre | L | pencere | geçerli | atılan (neden) | farklı ay | en kalabalık 3 ay payı | hisse |", "|---|---|---|---|---|---|---|---|"]
    for k, v in sorted(S["hucre"].items()):
        h, L = k.rsplit("|", 1)
        s.append(f"| {h.replace('|', ' ')} | {L} | {v['pencere']} | {v['gecerli']} | {v['atilan']} | {v['ay']} | {_f(v['ust3_pay'], 3)} | {v['hisse']} |")
    s += ["", "Tanımlayıcı boyutu: " + "; ".join(f"{L}: A {b['A']}, B {b['B']}, 0 {b['0']}" for L, b in S["boyut"].items()), "",
          "| komşu havuzu | sorgu | ay | havuz en az | medyan | en çok |", "|---|---|---|---|---|---|"]
    for k, v in S["havuz"].items():
        s.append(f"| {k.replace('|', ' ')} | {v['sorgu']} | {v['ay']} | {v['havuz_min']} | {_f(v['havuz_medyan'], 0)} | {v['havuz_max']} |")
    s += ["", f"Cemal bölgeleri (pazar, sınıf, durum, sayı): {Jh['cemal']}", "", "## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)", ""]
    s += [f"{i}. {y}" for i, y in enumerate(SD_YORUM, 1)]
    s += ["", "## Tanımlar (SD_ESIK; sha yukarıda)", "", "```", json.dumps(SD_ESIK, ensure_ascii=False, indent=1), "```", "", "## KONTROL LİSTESİ", "",
          "| Kod | Madde | Yanıt | Kanıt |", "|---|---|---|---|"]
    ad = {k["kod"]: k.get("baslik", k.get("ad", k["kod"])) for k in IK.IK_KONTROL}
    for k in IK.IK_KONTROL:
        y, kn = SD_KONTROL[k["kod"]]
        s.append(f"| {k['kod']} | {ad[k['kod']]} | {y} | {kn} |")
    s += ["", "## SAPMA", "", "(ön kayıt anında yok)", ""]
    return MI._mi_yaz(_sd_yol("onkayit", cikti), "\n".join(s) + "\n", "ön kayıt")


def _sd_ar(r: Dict[str, Any], n: int = 3, yuzde: bool = False, ad: str = "ic") -> str:
    v = r.get(ad, r.get("ort"))
    return f"{_f(v, n, yuzde)} [{_f(r.get('alt'), n, yuzde)} / {_f(r.get('ust'), n, yuzde)}]"


def sd_rapor_yaz(cikti: Optional[str] = None, ek: Optional[Dict[str, Any]] = None) -> str:
    cikti = cikti or SD_YOL["cikti"]; J = json.load(open(_sd_yol("sonuc", cikti), encoding="utf-8")); K = json.load(open(_sd_yol("kesim", cikti), encoding="utf-8"))
    ST = json.load(open(_sd_yol("sentetik", cikti), encoding="utf-8")) if os.path.exists(_sd_yol("sentetik", cikti)) else None
    ek = ek or {}; s = [f"# SD RAPOR — benzer şekil benzer devam mı; verinin kendi desenleri ({J['bitis'][:10]})", "",
                        f"Ön kayıt commit: {J['kapi']['onkayit_commit']}; kesim commit: {J['kesim_kapi']['kesim_commit']}; doğrulama {J['baslangic']} .. {J['bitis']}.",
                        "Evren bugün yaşayan hisseler (yukarı yanlı; ÜST - ALT ve IC kesit içi). KASA açılmadı (veri <= 2022-12-31).", "", "## SONUÇ", ""]
    for L in ("20", "10"):
        a = J["sinama1"][L]["ABD"]; v = J["sinama1"][L]["AVR"]; h = J["hukum1"][L]; u = a["uc"]["A"]
        s += [f"### SINAMA 1, L{L}{' (ERKEN EVRE)' if L == '10' else ''}: {h['hukum']}; tanımlayıcı B: {h['hacim']}", "",
              f"ABD 2020-22: {a['n']} sorgu, {a['ay']} ay. IC(A) {_sd_ar(a['ic']['A'])}; IC(0) {_sd_ar(a['ic']['0'])}; IC(rastgele) {_sd_ar(a['ic']['R'])}; "
              f"IC(A) - IC(0) {_sd_ar(a['fark']['A-0'])}; IC(B) {_sd_ar(a['ic']['B'])}; IC(B) - IC(A) {_sd_ar(a['fark']['B-A'])}. "
              f"AVR 2020-22 ({v['n']} sorgu): IC(A) {_sd_ar(v['ic']['A'])}, IC(0) {_sd_ar(v['ic']['0'])}, IC(rastgele) {_sd_ar(v['ic']['R'])}.", "",
              "| grup (TAHMİN A) | n | Z15 | R15 % | HEDEF | AYNA | TOPLAM FARK % |", "|---|---|---|---|---|---|---|"]
        for g in ("UST", "ALT", "HEPSI"):
            s.append(f"| {g} | {u['Z15'][g]['n']} | {_sd_ar(u['Z15'][g])} | {_sd_ar(u['R15'][g], 2, True)} | {_sd_ar(u['HEDEF'][g])} | {_sd_ar(u['AYNA'][g])} | "
                     f"{_sd_ar(u['TF'][g], 2, True)} |")
        s.append(f"| ÜST - ALT | | {_sd_ar(u['Z15']['UST-ALT'])} | {_sd_ar(u['R15']['UST-ALT'], 2, True)} | {_sd_ar(u['HEDEF']['UST-ALT'])} | "
                 f"{_sd_ar(u['AYNA']['UST-ALT'])} | {_sd_ar(u['TF']['UST-ALT'], 2, True)} |")
        s += ["", f"Yol benzerliği (ortalama korelasyon): komşu A {_sd_ar(a['yol']['A'])}, rastgele {_sd_ar(a['yol']['R'])}, 0 {_sd_ar(a['yol']['0'])}, B {_sd_ar(a['yol']['B'])}.",
              f"Şartlar: {h['sart']}.", ""]
    for L in ("20", "10"):
        KL = K["L"][L]; oz = {o["kume"]: o for o in KL["kume"]}; V = J["sinama2"][L]; H2 = J["hukum2"][L]
        s += [f"### SINAMA 2, L{L}: en iyi küme {H2['DESEN_IYI']}; en kötü küme {H2['DESEN_KOTU']}; BH'den geçen: {H2['bh_gecen'] or 'yok'}", "",
              "| seçim | küme | şekil | keşif Z15 / n | doğr. Z15 | R15 % | TOPLAM FARK % | HEDEF | AYNA | ay / üst3 | AVR Z15 (n) | AVR 16-19 Z15 | p | BH q | hüküm |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in H2["satir"]:
            c = r["kume"]; o = oz[c]; d = V[SD_ESIK["hucre"]["dogrulama"]]["kume"][str(c)]; ab = V[SD_ESIK["hucre"]["avr_bilgi"]].get("kume", {}).get(str(c), {})
            s.append(f"| {'İYİ' if r['secim'] == 'iyi' else 'KÖTÜ'} {r['sira']} | {c} | {o['tarif']} | {_f(o['Z15'], 3)} / {o['n']} | {_sd_ar(d['Z15'])} | "
                     f"{_sd_ar(d['R15'], 2, True)} | {_sd_ar(d['TF'], 2, True)} | {_f(d['HEDEF']['ort'], 3)} | {_f(d['AYNA']['ort'], 3)} | {d.get('ay')} / "
                     f"{_f(d.get('ust3_pay'), 2)} | {_f(r['avr_z15'], 3)} ({r['avr_n']}) | {_f(ab.get('Z15', {}).get('ort'), 3)} | {_f(r['p'], 4)} | "
                     f"{_f(r['bh_q'], 3)} | {'TUTTU' if r['tuttu'] else 'TUTMADI'} |")
        s.append("")
        if "cemal" in KL:
            c = KL["cemal"]; e = c["ozet"]["EVET"]
            s.append(f"Cemal'in BENZİYOR dediği günlük bölgeler (L{L}): {e['n']} / {e['n_tum']} atandı; ilk 5 küme [küme, n, pay, keşif sırası]: {e['ilk5']}; "
                     f"seçilen iyi 5 payı {_f(e['secilen_iyi_pay'], 2)}, kötü 5 payı {_f(e['secilen_kotu_pay'], 2)}. HAYIR (bilgi): ilk 5 {c['ozet']['HAYIR']['ilk5']}.")
            for ad_, o in c["appn"].items():
                kc = o["kume"]; d = V[SD_ESIK["hucre"]["dogrulama"]]["kume"].get(str(kc), {}) if kc is not None else {}
                s.append(f"- {ad_}: küme {kc}, keşif sırası {o['sira']} (keşif Z15 {_f(oz[kc]['Z15'] if kc is not None else None, 3)}, n {oz[kc]['n'] if kc is not None else '—'}); "
                         f"doğrulama Z15 {_f(d.get('Z15', {}).get('ort'), 3)} (n {d.get('n')}); şekil: {oz[kc]['tarif'] if kc is not None else '—'}")
            s.append("")
    if ST:
        g = ST["gomulu"]; n = ST.get("ilgisiz", {})
        s += ["## SENTETİK", "", f"- Yakalama (kalıbın kümesine düşen POZ payı, gürültüye göre): {g['yakalama']}; hepsi {_f(g['yakalama_hepsi'], 3)}; en kalabalık 3 küme {_f(g['yakalama_ilk3'], 3)}",
              f"- Yanlış kabul (kalıbın kümesine düşen): {g['yanlis_kabul']}; ilk 3 küme: {g['yanlis_kabul_ilk3']}",
              f"- Kalıbın kümesi {g['kalip_kume']}: keşif sırası {g['kalip_sira']} / 60, en iyi 5 içinde: {g['kalip_en_iyi5']}; kümede POZ payı {_f(g['kalip_kume_poz_pay'], 3)}",
              f"- IC(A) gömülü {_sd_ar(g['ic']['A'])}; ilişkisiz {_sd_ar(n['ic']['A']) if n else '—'}; rastgele komşu (gömülü) {_sd_ar(g['ic']['R'])}",
              f"- En iyi 5 küme: kalıbın erken evresi (pencere sonu olay bitişinden 1-15 bar önce) payı {_f(g['iyi5_erken_pay'], 3)}, tam kalıp payı "
              f"{_f(g['iyi5_tam_kalip_pay'], 3)}; bileşim {g['iyi5_bilesim']}", ""]
        for t, v in g["yanlis_kabul"].items():
            if v > 0.30:
                s.append(f"- UYARI: {t}'in %{v * 100:.0f}'i kalıbın kümesine düştü: tanımlayıcı " + ("mum yapısını" if t == "N1" else "gidişi" if t == "N2" else "rastgeleyi") + " ayırt etmiyor.")
        s.append("")
    s += ["## KONTROL LİSTESİ", "", "Ön kayıttaki tablo (14 madde) aynen geçerli; denetim kanıtı: komşu denetimi (aynı hisse / yakın / sonucu bilinmeyen komşu sayısı) "
          + "; ".join(f"L{L} {p}: {J['sinama1'][L][p]['denetim']['A']}" for L in J["sinama1"] for p in J["sinama1"][L]) + ".", "",
          "## HATA", ""] + [f"- {x}" for x in ek.get("hata", ["(yok)"])] + ["", "## SAPMA", ""] + [f"- {x}" for x in ek.get("sapma", ["(yok)"])]
    s += ["", "## YENİDEN ÜRETİM", ""] + [f"- {x}" for x in ek.get("yeniden", ["(eklenmedi)"])]
    s += ["", "## ÖNERİLEN DEFTER SATIRLARI", ""] + [f"- {x}" for x in ek.get("defter", ["(ana model yazar)"])]
    s += ["", "## DOSYALAR", "", *[f"- {a}: {v}" for a, v in ek.get("dosya", {}).items()], ""]
    return MI._mi_yaz(_sd_yol("rapor", cikti), "\n".join(s) + "\n", "rapor")


def sd_sha_simdi(ham: Optional[str] = None) -> Dict[str, str]:
    out = {"SD_KOD_SHA": sd_kod_sha(), "SD_ESIK_SHA": sd_esik_sha()}
    try:
        out.update(sd_dosya_sha(ham))
    except FileNotFoundError:
        pass
    return out


def _cakisma_kontrol_sd(_once=_CK_ONCE_SD, _dosya="SEKIL_DEVAM.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_SD",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_sd()


def _sd_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="SEKIL_DEVAM")
    ap.add_argument("komut", choices=["hazirla", "sayim", "onkayit", "kesif", "dogrulama", "rapor", "sentetik", "sha"])
    ap.add_argument("--ek", default=None, help="rapor eki json (hata / sapma / yeniden / defter / dosya)")
    a = ap.parse_args(argv)
    try:
        if a.komut == "hazirla":
            print(json.dumps(MI._mi_json(sd_hazirla()), ensure_ascii=False, indent=1))
        elif a.komut == "sayim":
            S = sd_sayim_kos(); MI._mi_jyaz(_sd_ham("sayim.json"), S, "sayım")
            print(json.dumps(MI._mi_json({k: v for k, v in S.items() if k != "standart"}), ensure_ascii=False, indent=1)); print("SAYIM_SHA:", HV.hv_json_sha(S))
        elif a.komut == "onkayit":
            print(sd_onkayit_yaz())
        elif a.komut == "kesif":
            K = sd_kesif(); print(json.dumps(MI._mi_json({L: v["secim"]["iyi"] + v["secim"]["kotu"] for L, v in K["L"].items()}), ensure_ascii=False))
        elif a.komut == "dogrulama":
            J = sd_dogrulama(); print(json.dumps(MI._mi_json({"hukum1": J["hukum1"], "hukum2": {L: {k: v for k, v in h.items() if k != "satir"} for L, h in J["hukum2"].items()}}),
                                                 ensure_ascii=False, indent=1))
        elif a.komut == "rapor":
            E = json.load(open(a.ek, encoding="utf-8")) if a.ek else {}
            print(sd_rapor_yaz(ek=E))
            J = json.load(open(_sd_yol("sonuc"), encoding="utf-8")); K = json.load(open(_sd_yol("kesim"), encoding="utf-8")); print(sd_desen_pdf(J, K, _sd_yol("pdf")))
        elif a.komut == "sentetik":
            J = sd_sentetik_kos(); print(json.dumps(MI._mi_json({k: v for k, v in J["gomulu"].items() if k not in ("fark",)}), ensure_ascii=False, indent=1))
            print(json.dumps(MI._mi_json(J.get("ilgisiz", {}).get("ic")), ensure_ascii=False))
        elif a.komut == "sha":
            print(json.dumps(sd_sha_simdi(), indent=1))
    except SDHata as ex:
        sdlog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_sd_ana())
