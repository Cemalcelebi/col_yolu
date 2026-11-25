"""MUM_IZI — CEMAL'İN İŞARETLEDİĞİ MUM BÖLGESİNİN PARMAK İZİ, SENTETİK TUTTURMA TESTİ, AÇIK VERİDE BENZERLİK / KONUM (25 Kasım 2026).

İş tanımı: arastirma_cikti/mum_izi/MUM_IZI_IS_TANIMI.md (commit d07b660; ana model). Cemal (25 Kas): "Buradaki mumların parmak izini çıkar:
büyüklük, alt fitil, üst fitil, birbirine bağlı / birbirine göre dizilimi ve SMA konumlarını, her şeyi ölç; bu ölçünün ne kadarını
tutturduğunun birebir kodunu tekrar tekrar sentetik veri ile test et; veriye / testlere ne oranda benziyor ve fiyatın en tepesi olmadan
diğer yerlerinde ne oranda tutturmuşsun görelim."

Bu iş bir TESPİT / BENZERLİK ölçüsüdür (ölçü sayısı <= 40; '90'dan fazla şekil ölçüsü' kapalı konusuna girmez). Getiri sonucu yalnız ön
kayıtlı BİLGİ satırıdır. KASA AÇILMAZ (açık veri <= 2022-12-31; kod en büyük tarihi assert eder). KASA KURALI: tek iz kasa açmaz; en fazla
'birleşik iz bileşeni adayı'.

ADIMLAR
  A  sayısallaştırma: ORNEK_25Kas.jpg (1080 x 2400) -> mum ızgarası (gövde renk maskeleri, en küçük kareler ızgara), fitil (mavi-gri mürekkep
     koşusu), Bollinger üst / orta / alt (lavanta çizgi izleme), turuncu daireye göre konum (iç / çizgi / dış). Fiyat ekseni etiketi yok:
     her şey piksel (y yukarı pozitif). Bindirme PNG + elle doğrulama PNG.
  B  parmak izi: <= 40 ölçü, ölçek bağımsız (birim = bölgenin ortalama mum boyu H-L); MI_OZELLIK.
  C  tespit: kayan pencere (uzunluk L x {0,8 .. 1,2}), benzerlik S = exp(-(D_dizi / tau_dizi + D_bant / tau_bant + D_oz / tau_oz) / 3);
     sabit hizalama + doğrusal yeniden örnekleme (DTW değil; gerekçe MI_ESIK['benzerlik']['hizalama']). TAM iz ve TEPESİZ iz (son H > üst
     bant mumları çıkarılmış) ayrı şablon.
  D  sentetik tutturma: blok bootstrap (ABD 2005-2014 gerçek mumları, karar hücreleri dışı) ve saf rastgele yürüyüş; gürültü 0 / 10 / 20 / 30,
     ölçek x0,5..x2, esneme +-%20, bağlam dip / yatay / tepe; koşul başına 200 tohum, iki bağımsız kök (tekrar). Eşik: %20 gürültüde
     yakalama >= %80 veren en yüksek S (0,01 ızgara).
  E  gerçek veri (ön kayıttan SONRA): TEZGAH2 P2 havuzu ABD + AVR (karar), BIST (bilgi); benzerlik sıklığı gerçek vs sentetik; konum (tepe /
     dip / orta); sonrası BİLGİ: R15 eşli fark (CETVEL2 v2.2 konum eşi), +%5 stop'tan önce (stop = pencere en düşük Low x 0,98) vs eş,
     plasebo (C2.c2_plasebo 200 tohum).

Komut:  python MUM_IZI.py sayisallastir   görüntü -> mum_izi_mumlar.csv, mum_izi_sablon.json, mum_izi_parmak_izi.csv, bindirme PNG
        python MUM_IZI.py acik            V_ABD2 / V_AVR2 (/root/.kasa/ham/veri3, YALNIZ OKUNUR) + V_BIST (/tmp/veri) -> kesikli açık kopya
                                          /tmp/mum_izi/acik + üretici havuzu (ABD 2005-2014) -> mum_izi_acik.json
        python MUM_IZI.py sentetik        kalibrasyon (tau, sd) + sentetik test (iki kök) + eşik -> mum_izi_sentetik.json / _tablo.csv
        python MUM_IZI.py kuru            gerçek veri hattının SENTETİK panelde kuru koşusu (kapı yok; çıktı /tmp/mum_izi/kuru)
        python MUM_IZI.py onkayit         MUM_IZI_ON_KAYIT.md
        python MUM_IZI.py kos             kapı (kontrol + ön kayıt sha + commit + KASA) -> gerçek veri -> mum_izi_olay.csv.gz, mum_izi_sonuc.json
        python MUM_IZI.py gorsel          MUM_IZI_GORSEL.pdf
        python MUM_IZI.py rapor           MUM_IZI_RAPOR.md
        python MUM_IZI.py sha             kod / eşik sha
Colab:  exec(open('MUM_IZI.py').read())   (kod değiştiyse çalışma zamanını yeniden başlat)
Mevcut modüller (CETVEL2, KART_TUR2, OLCU_SINAMA, TEZGAH2_DOGRULAMA, KASA, IZ_KARNE) DEĞİŞTİRİLMEZ; içe alınır. Evren bugün işlem gören
hisseler (K7: sonuç yukarı yanlı). Komisyon yok.
"""
from __future__ import annotations

import os
import sys

_CK_ONCE_MI = {k: id(v) for k, v in globals().items()}

import datetime as _dt  # noqa: E402
import gc  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import logging  # noqa: E402
import math  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from typing import Any, Dict, List, Optional, Tuple  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view as _swv  # noqa: E402

KOK_MI = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if KOK_MI not in sys.path:
    sys.path.insert(0, KOK_MI)

milog = logging.getLogger("col.mum_izi")
if not milog.handlers:
    _mi_h = logging.StreamHandler(sys.stderr)
    _mi_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s mum_izi: %(message)s", "%H:%M:%S"))
    milog.addHandler(_mi_h)
    milog.setLevel(logging.INFO)
    milog.propagate = False


class MIHata(RuntimeError):
    """Durdurucu hata: görüntü / veri yok, kesik aşımı, kontrol / ön kayıt kapısı, sağlama tutmadı, ikinci koşu."""


MI_SURUM = "MUM_IZI v1.0 (2026-11-25): ORNEK_25Kas parmak izi + sentetik tutturma + açık veride benzerlik / konum / sonrası (bilgi)"
MI_YOL = {"cikti": os.path.join(KOK_MI, "arastirma_cikti", "mum_izi"), "kod": os.path.join(KOK_MI, "MUM_IZI.py"),
          "goruntu": os.path.join(KOK_MI, "arastirma_cikti", "mum_izi", "ORNEK_25Kas.jpg"),
          "is_tanimi": os.path.join(KOK_MI, "arastirma_cikti", "mum_izi", "MUM_IZI_IS_TANIMI.md"),
          "veri3": os.environ.get("MI_VERI3", "/root/.kasa/ham/veri3"), "veri": os.environ.get("MI_VERI", "/tmp/veri"),
          "acik": os.environ.get("MI_ACIK", "/tmp/mum_izi/acik"), "gecici": os.environ.get("MI_GECICI", "/tmp/mum_izi")}
MI_DOSYA = {"mumlar": "mum_izi_mumlar.csv", "sablon": "mum_izi_sablon.json", "parmak": "mum_izi_parmak_izi.csv",
            "bindirme": "mum_izi_bindirme.png", "elle": "mum_izi_elle_dogrulama.png", "acik_json": "mum_izi_acik.json",
            "sentetik": "mum_izi_sentetik.json", "sentetik_tablo": "mum_izi_sentetik_tablo.csv", "onkayit": "MUM_IZI_ON_KAYIT.md",
            "olay": "mum_izi_olay.csv.gz", "sonuc": "mum_izi_sonuc.json", "rapor": "MUM_IZI_RAPOR.md", "pdf": "MUM_IZI_GORSEL.pdf",
            "havuz": "uretec_havuz.pkl"}
MI_KESIK = pd.Timestamp("2022-12-31")

# ================================================================ MÜHÜRLÜ AYAR SÖZLÜĞÜ (sha ön kayıtta; gerçek veriden sonra DEĞİŞMEZ)
MI_ESIK: Dict[str, Any] = {
    "surum": "MI-1.0",
    "goruntu": {
        "boyut": [1080, 2400], "fiyat_satir": [380, 1200],
        "renk": {"yesil": "G-R > 60, G-B > 30, G > 110", "kirmizi": "R > 170, G < 105, B < 100, R-G > 90",
                 "turuncu": "R >= 225, 95 <= G <= 175, B <= 150, R-B >= 90; 4 aşındırma + 8 genişletme (kalın çizgi çekirdeği)",
                 "fitil": "max(R,G,B) < 190, B-R >= 3, |R-G| <= 14 (mavi-gri); tarih kesikli çizgisi nötr gri (B = R) olduğu için dışarıda",
                 "doji": "kırmızımsı R-(G+B)/2 >= 20 ya da yeşilimsi G-(R+B)/2 >= 15, merkezden 4-11 piksel yanda (fitil dışı)",
                 "bant": "|R-G| <= 10, 5 <= B-R <= 28, 170 <= R <= 230 (lavanta)"},
        "izgara": "katı gövde sütun öbekleri (genişlik >= 20 px) -> merkezler -> x = a + b k en küçük kareler (b ilk tahmin ardışık fark medyanı)",
        "govde_satir_min": 4, "fitil_bosluk": 2, "fitil_yari": 3, "govde_yari": 10, "bant_yari": [14, 22], "bant_izleme_tol": 6,
        "konum": "İÇ = mumun sütununda turuncu çekirdek hem tepenin üstünde hem dibin altında VE merkez pikseli turuncu değil; ÇİZGİ = merkez "
                 "turuncu; DIŞ = öteki. Bölge = İÇ mumlar (görüntü kenarında kesilen mum KESİK, bölgeye girmez); bölgenin solundaki DIŞ / "
                 "ÇİZGİ mumlar BAĞLAM (gövdesi hiç görünmeyen çizgi mumu GİZLİ, ölçülmez)",
        "y": "fiyat_px = 2400 - satır (y yukarı pozitif)"},
    "sablon": {"tam": "bölgenin bütün tam görünen mumları (İÇ)",
               "tepe": "bölge sonundaki ardışık High > üst bant mumları (üst bant yürüyüşü); TEPESİZ şablon = bunlar çıkarılmış ilk mumlar",
               "esneme": [0.8, 0.9, 1.0, 1.1, 1.2]},
    "benzerlik": {
        "bant": {"n": 20, "k": 2.0, "std": "ddof 0 (anakütle)"},
        "dizi": "pencere mumları birim u = ort(H-L), seviye = ort((H+L)/2); z = (X - seviye) / u, X = O / H / L / C; pencere L mumuna doğrusal "
                "yeniden örneklenir (esneme); D_dizi = kök(ort (z - z*)^2) (birim: ortalama mum boyu)",
        "bant_dizi": "%B = (C - alt) / (üst - alt) (üst = alt ise 0,5); D_bant = kök(ort (%B - %B*)^2)",
        "ozellik_alt": ["ust_fitil", "alt_fitil", "ust_alt_log", "govde_oran", "kucuk_mum_pay", "yuk_dip_pay", "kapanis_egim", "kapanis_r2",
                        "pB_bas", "pB_son", "sma_ustu_pay", "bant_gen_oran_log"],
        "oz": "D_oz = kök(ort ((F - F*) / sd)^2) ozellik_alt üzerinde; sd = rastgele (blok bootstrap) pencerelerde IQR / 1,349 (0 ise std)",
        "S": "S = exp(-(D_dizi / tau_dizi + D_bant / tau_bant + D_oz / tau_oz) / 3); tau = rastgele pencerelerin medyan uzaklığı (kalibrasyon) "
             "-> rastgele pencere S ~ e^-1 = 0,37, birebir şablon S = 1",
        "uc_bilesen": "S her pencere sonu t için t'ye kadarki barlardan; pencere uzunlukları L x esneme (yuvarlak, tekil); t'de en büyük S",
        "hizalama": "sabit hizalama + doğrusal yeniden örnekleme (DTW değil): DTW her dizini serbest bükerek rastgele diziyi de şablona "
                    "yaklaştırır (yanlış alarm), hesap yükü milyonlarca pencerede ağır; esneme +-%20 açık uzunluk ızgarasıyla aranır",
        "kalibrasyon": {"seri": 400, "n": 320, "pencere": 20000, "kok": 7700}},
    "sentetik": {
        "uretec": ["blok", "ry"], "baglam": ["dip", "yatay", "tepe"], "gurultu": [0.0, 0.1, 0.2, 0.3], "tohum": 200,
        "olcek": [0.5, 2.0], "olcek_dagilim": "log-düzgün", "esneme": [0.8, 1.2], "esneme_dagilim": "düzgün", "konum_tol": 3,
        "seri_on": 200, "seri_son": 60, "baglam_bar": 40, "baglam_egim": 0.005, "blok": 5,
        "ry": {"sigma": [0.01, 0.03], "bosluk_kat": 0.25, "fitil_kat": 0.5},
        "yanlis": {"seri": 200, "n": 1000, "tekil": 15},
        "kok": {"A": 25112026, "B": 25112027},
        "esik": {"gurultu": 0.2, "yakalama": 0.80, "izgara": 0.01,
                 "kural": "kök A, %20 gürültü, üç bağlam x iki üretici birleşik (1.200 tohum): yakalama >= %80 veren EN YÜKSEK S (0,01 ızgara); "
                          "tam ve tepesiz ayrı; kök B aynı eşikle TEKRAR (yalnız rapor)"},
        "birebir": "yakalanan tohumlarda bulunan pencerenin ölçüleri ile gömülü (gerçek) pencerenin ölçüleri arasında ort |fark| / sd ve "
                   "Pearson r (MI_OZELLIK, bağlam ölçüleri hariç)"},
    "uretec_havuz": {"pazar": "ABD", "donem": ["2005-01-01", "2014-12-31"], "hisse": 300, "min_bar": 1000, "min_fiyat": 5.0, "tohum": 2511,
                     "tanim": "TEZGAH2 V_ABD2 geçerli barları (H > L, V > 0); mum tanımlayıcıları: log boşluk O/C(-1), log gövde C/O, log üst "
                              "fitil H/max(O,C), log alt fitil min(O,C)/L; |log| > 0,3 olan bar (bölünme / hata) havuz dışı"},
    "gercek": {
        "pazar_karar": ["ABD", "AVR"], "pazar_bilgi": ["BIST"], "veri_bas": "2015-01-01", "tarama": ["2016-01-01", "2022-12-31"],
        "tekil": 15, "konum_bar": 120, "konum_pay": 0.03,
        "konum_tanim": "TEPE: C(t) >= 0,97 x son 120 barın (t dahil) en yüksek kapanışı; DİP: değilse ve C(t) <= 1,03 x en düşük kapanış; ORTA: "
                       "öteki; KISA: 120 bar yok. BAŞKA YERDE = DİP + ORTA",
        "havuz": "ABD / AVR: TEZGAH2 P2 (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1; giriş günü d'de) VE CETVEL2 v2.2 havuzu (c2_olay tekil 15). "
                 "BIST: yalnız CETVEL2 v2.2 havuzu (P2 BIST'te tanımlı değil; bilgi)",
        "donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]},
        "ufuk": 15, "es_min": 5, "stop_carpan": 0.98, "h5_es_sayi": 20, "h5_es_kok": 2513, "plasebo_tohum": 200, "yon": "?",
        "prefix_n": 30, "prefix_kok": 2514, "duz_n": 20,
        "gorsel": {"tepe": 6, "baska": 6, "rastgele": 8, "once": 20, "sonra": 15, "tohum": 2512}},
    "karar_kurali": (
        "BİLGİ ETİKETİ (şablon başına, 'hepsi' grubu, yön '?'): (1) dört karar hücresinin (ABD d1619 / d2022, AVR d1619 / d2022) dördünde C2 "
        "hükmü aynı yönde TUTAR (C2.c2_hucre: n >= 30, güç >= 0,80, FARK yönlü, boot ucu, SIRA, L3O) VE c2_plasebo o yönde geçti -> 'BİRLEŞİK "
        "İZ BİLEŞENİ ADAYI' (KASA KURALI: tek iz, kasa açılmaz); (2) değilse dört hücrede n >= 30 ve güç >= 0,80 -> 'İZ DEĞİL'; (3) değilse en "
        "az bir hücre TUTAR -> 'EMARE'; (4) değilse 'ÖLÇÜLEMEDİ'. BENZERLİK: gerçek tekil eşleşme sıklığı (1.000 bar başına) / sentetik "
        "rastgele (aynı eşik, aynı tekil) oranı yazılır; hüküm yok. KONUM: tepe / başka yerde payları yazılır; hüküm yok."),
}

# ölçüler: (ad, düz dil açıklama, grup)
MI_OZELLIK: List[Tuple[str, str, str]] = [
    ("boy_cv", "mum boyu değişkenliği (std / ortalama boy)", "mum"),
    ("govde_oran", "ortalama gövde / boy", "mum"),
    ("ust_fitil", "ortalama üst fitil / boy", "mum"),
    ("alt_fitil", "ortalama alt fitil / boy", "mum"),
    ("ust_alt_log", "üst fitil baskınlığı: log(toplam üst fitil / toplam alt fitil)", "mum"),
    ("yesil_pay", "yeşil (C > O) mum payı", "mum"),
    ("doji_pay", "doji payı (gövde / boy < 0,10)", "mum"),
    ("uzun_ust_pay", "uzun üst fitilli mum payı (üst fitil >= boyun yarısı)", "mum"),
    ("buyuk_mum_pay", "büyük mum payı (boy >= 1,5 x ortalama)", "mum"),
    ("kucuk_mum_pay", "küçük mum payı (boy <= 0,7 x ortalama)", "mum"),
    ("yuk_dip_pay", "yükselen dip payı (L > önceki L)", "dizilim"),
    ("yuk_tepe_pay", "yükselen tepe payı (H > önceki H)", "dizilim"),
    ("yuk_kapanis_pay", "yükselen kapanış payı", "dizilim"),
    ("ortusme", "ardışık mumların örtüşme oranı (ortak aralık / küçük boy)", "dizilim"),
    ("govde_orta_egim", "gövde ortası eğimi (mum boyu / mum)", "dizilim"),
    ("kapanis_egim", "kapanış doğrusu eğimi (mum boyu / mum)", "dizilim"),
    ("kapanis_r2", "kapanış doğrusu R^2 (düzgün yürüyüş)", "dizilim"),
    ("net_hareket", "net hareket: (son kapanış - ilk açılış) / boy", "dizilim"),
    ("dipten_yukselis", "dipten yükseliş: (son kapanış - en düşük) / boy", "dizilim"),
    ("dip_konum", "en düşük mumun yeri (0 = baş, 1 = son)", "dizilim"),
    ("tepe_konum", "en yüksek mumun yeri (0 = baş, 1 = son)", "dizilim"),
    ("dip_sonrasi_alt_fitil", "dipten sonraki mumlarda ortalama alt fitil / boy", "dizilim"),
    ("dip_sonrasi_ust_fitil", "dipten sonraki mumlarda ortalama üst fitil / boy", "dizilim"),
    ("pB_bas", "ilk 3 mumda kapanışın bant içi yeri %B (0 alt bant, 1 üst bant)", "bant"),
    ("pB_son", "son 3 mumda %B", "bant"),
    ("pB_egim", "%B eğimi (mum başına)", "bant"),
    ("sma_ustu_pay", "kapanışı SMA20 üstünde olan mum payı", "bant"),
    ("sma_mesafe_son", "son kapanışın SMA20'ye uzaklığı (mum boyu)", "bant"),
    ("sma_gecis_konum", "SMA20 üstüne kalıcı geçişin yeri (0 baş, 1 = hiç / son)", "bant"),
    ("bant_gen_bas", "ilk 3 mumda bant genişliği / mum boyu", "bant"),
    ("bant_gen_oran_log", "bant açılması: log(son 3 genişlik / ilk 3 genişlik)", "bant"),
    ("bant_dar_konum", "bandın en dar olduğu yer (0 baş, 1 son)", "bant"),
    ("sma_egim", "SMA20 eğimi (mum boyu / mum)", "bant"),
    ("ust_bant_asim_pay", "High > üst bant mum payı", "bant"),
    ("alt_bant_asim_pay", "Low < alt bant mum payı", "bant"),
]
MI_BAGLAM_OZ: List[Tuple[str, str]] = [
    ("baglam_kirmizi_boy", "bölge öncesi büyük kırmızı mumun boyu / bölge ortalama boyu"),
    ("baglam_kirmizi_govde", "büyük kırmızı mumun gövdesi / bölge ortalama boyu"),
    ("baglam_dusus", "bağlam en yüksek High'dan bölge en düşük Low'a düşüş / bölge ortalama boyu"),
]

MI_KONTROL: Dict[str, Tuple[str, str]] = {
    "K1": ("EVET", "eş = CETVEL2 v2.2 konum eşi (C2.c2_es: aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün aynı şablonun "
                   "bütün olayları dışı); plasebo şans tabanı SAYIYLA: C2.c2_plasebo 200 tohum her karar hücresinde (aynı gün rastgele havuz "
                   "hissesi, aynı cetvel); +%5 payı eşi = aynı gün aynı kovadan 20 rastgele üye, AYNI geometri (kendi son m barının en düşük "
                   "Low x 0,98 stop); benzerlik sıklığının tabanı = sentetik rastgele seriler (blok bootstrap + rastgele yürüyüş, aynı eşik)"),
    "K2": ("EVET", "S(t) yalnız t'ye kadarki barlar (bant SMA20 / std20 kendi barına kadar; pencere [t-m+1, t]); konum son 120 bar t dahil; "
                   "mi_prefix: 30 rastgele olayda veri t'de kesilince S(t) aynı (assert); açık kopya <= 2022-12-31 + KASA.kasa_kapisi; "
                   "üretici havuzu 2005-2014 (karar hücreleri 2016-22 dışı); eşik sentetikten, gerçek veriden önce"),
    "K3": ("EVET", "gerçek veri OS.os_veri / OC.oc_veri_hazirla geçerli bar süzgeci (H > L, V > 0, O/H/L/C > 0); pencereler hissenin kendi "
                   "geçerli barlarında; sentetik barlar H >= max(O,C) > min(O,C) >= L > 0 (test)"),
    "K4": ("EVET", "aynı hissede aynı şablon için eşiği geçen pencere sonları 15 geçerli bar tekil (ilk kalır); C2.c2_olay tekil 15 (birleşik "
                   "takvim); sentetik yanlış alarm da 15 bar tekil sayılır (ham pencere sayısı ayrıca)"),
    "K5": ("EVET", "giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1; +%5 YH.yh_sim "
                   "(kapanışla, takip stoplu) c2_bilgi üzerinden"),
    "K6": ("EVET", "TEZGAH2 V_ABD2 / V_AVR2 (yfinance auto_adjust, bölünme düzeltmeli; AVR Kur sütunu likiditede); S ölçek bağımsız (oranlar, "
                   "mum boyu birimi); BIST V_BIST (fi_k1_veri) bilgi"),
    "K7": ("EVET", "evren bugün işlem gören hisseler (TEZGAH2 ABD 5.394 / AVR 578 sembolden 2015-22'de verisi olan ABD 4.450, AVR 572; BIST 475): "
                   "batanlar yok -> sonrası yukarı yanlı; olay ve eş aynı evrenden (yanlılık ikisine aynı); raporda yazılı"),
    "K8": ("EVET", "iki dönem (d1619, d2022) x iki karar pazarı ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç C2 eğrisi; sentetik koşul başına 200 tohum, "
                   "iki bağımsız kök; tam ve tepesiz iki şablon = iki aile (sonrası yalnız bilgi, BH gerekmez; p'ler yazılır)"),
    "K9": ("EVET", "MUM_IZI_ON_KAYIT.md: KOD_SHA, ESIK_SHA, SABLON_SHA, SENTETIK_SHA (eşik), açık kopya sha'ları; ön kayıt commit'i gerçek veri "
                   "taramasından önce; mi_kapi kos'tan önce ik_kontrol_kapisi + sha + git (commit'li ve değişmemiş) denetler"),
    "K10": ("EVET", "sayısallaştırma: bindirme PNG (bütün mumlar) + 3 rastgele mumun yakın plan elle doğrulama PNG'si (mum_izi_elle_dogrulama.png); "
                    "mum sayısı (20 iç) ve renk dizisi görüntüden elle sayımla karşılaştırılır (test_mum_izi)"),
    "K11": ("EVET", "mi_duz_S: 20 rastgele olayda S düz döngüyle (vektörsüz) yeniden; mi_yeniden: 2 hücre (ABD d1619, AVR d2022 tam iz) olay "
                    "satır dosyasından düz pandas ile n / ort FARK / +%5 payı; tutmazsa rapor TUTMADI"),
    "K12": ("EVET", "'iz' sözü yalnız karar kuralı geçerse; benzerlik / konum hükümsüz sayı; R15 (fiyat değişimi) ile kâr / zarar ayrı; sayı ve "
                    "yorum ayrı cümle"),
    "K13": ("EVET", "çakışma kapısı (_cakisma_kontrol_mi); yasak dosyalar (defterler, kural_defteri) ve UC_IZ2 dosyalarına dokunulmaz; yalnız "
                    "kendi yolları git add; veri3 / /tmp/veri yalnız okunur; e-posta / anahtar taraması (mi_sizinti); ücretli servis yok"),
    "K14": ("UYGULANMAZ", "öneri / gerçek para işi değil; tespit / benzerlik ölçümü; alım-satım önerisi yok"),
}


# ================================================================ 0) YARDIMCI
def _mi_simdi() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _mi_sha(yol: str) -> str:
    h = hashlib.sha256()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def mi_esik_sha(E: Optional[Dict[str, Any]] = None) -> str:
    return hashlib.sha256(json.dumps(E or MI_ESIK, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _mi_yol(ad: str, cikti: Optional[str] = None) -> str:
    return os.path.join(cikti or MI_YOL["cikti"], MI_DOSYA[ad])


def _mi_json(o: Any) -> Any:
    if isinstance(o, dict):
        return {str(k): _mi_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_mi_json(v) for v in o]
    if isinstance(o, np.ndarray):
        return [_mi_json(v) for v in o.tolist()]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (pd.Timestamp, np.datetime64)):
        return str(pd.Timestamp(o).date())
    return o


_MI_EPOSTA = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_MI_ANAHTAR = re.compile(r"(?i)(api[_-]?key|token|secret|password|sifre)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def mi_sizinti(metin: str, ad: str) -> None:
    """Çıktıya e-posta / anahtar sızmasın (fail-closed). 'noreply@anthropic.com' commit imzası çıktıya yazılmaz."""
    if _MI_EPOSTA.search(metin) or _MI_ANAHTAR.search(metin):
        raise MIHata(f"{ad}: e-posta / anahtar benzeri metin -> yazılmadı")


def _mi_yaz(yol: str, metin: str, ad: str = "dosya") -> str:
    mi_sizinti(metin, ad)
    os.makedirs(os.path.dirname(os.path.abspath(yol)), exist_ok=True)
    with open(yol + ".tmp", "w", encoding="utf-8") as f:
        f.write(metin)
    os.replace(yol + ".tmp", yol)
    return yol


def _mi_jyaz(yol: str, J: Any, ad: str = "json") -> str:
    return _mi_yaz(yol, json.dumps(_mi_json(J), ensure_ascii=False, indent=1), ad)


def _mi_git(args: List[str]) -> str:
    try:
        return subprocess.run(["git"] + args, cwd=KOK_MI, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception as ex:   # git yoksa kapı düşer (fail-closed çağıranda)
        milog.warning("git çalışmadı: %s", ex)
        return ""


def _mi_kosu(v: np.ndarray) -> List[Tuple[int, int]]:
    """Bool dizideki ardışık True koşuları [(baş, son)]."""
    ix = np.flatnonzero(v)
    if not len(ix):
        return []
    kir = np.flatnonzero(np.diff(ix) > 1)
    bas = np.r_[ix[0], ix[kir + 1]]; son = np.r_[ix[kir], ix[-1]]
    return list(zip(bas.tolist(), son.tolist()))


# ================================================================ 1) SAYISALLAŞTIRMA (A)
def mi_goruntu_oku(yol: Optional[str] = None) -> np.ndarray:
    from PIL import Image
    y = yol or MI_YOL["goruntu"]
    if not os.path.exists(y):
        raise MIHata(f"görüntü yok: {y}")
    im = np.asarray(Image.open(y).convert("RGB")).astype(np.int32)
    if list(im.shape[:2][::-1]) != MI_ESIK["goruntu"]["boyut"]:
        raise MIHata(f"görüntü boyutu {im.shape[1]}x{im.shape[0]} beklenen {MI_ESIK['goruntu']['boyut']}")
    return im


def mi_maskeler(im: np.ndarray) -> Dict[str, np.ndarray]:
    """Renk maskeleri (MI_ESIK['goruntu']['renk'] metniyle aynı sayılar)."""
    from scipy.ndimage import binary_dilation, binary_erosion
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    mx = im.max(2)
    M = {"yesil": (G - R > 60) & (G - B > 30) & (G > 110),
         "kirmizi": (R > 170) & (G < 105) & (B < 100) & (R - G > 90)}
    tur = (R >= 225) & (G >= 95) & (G <= 175) & (B <= 150) & (R - B >= 90)
    M["turuncu"] = binary_dilation(binary_erosion(tur, iterations=4), iterations=8)
    M["fitil"] = (mx < 190) & (B - R >= 3) & (np.abs(R - G) <= 14)
    M["kirmizi_acik"] = (R - (G + B) / 2 >= 20) & (R <= 232) & (G <= 170) & ~M["turuncu"]
    M["yesil_acik"] = (G - (R + B) / 2 >= 15) & (G <= 235) & ~M["turuncu"]
    M["bant"] = (np.abs(R - G) <= 10) & (B - R >= 5) & (B - R <= 28) & (R >= 170) & (R <= 230)
    return M


def mi_izgara(M: Dict[str, np.ndarray]) -> Tuple[float, float, List[float]]:
    """Katı gövde sütun öbeklerinden mum merkezi ızgarası x = a + b k."""
    y0, y1 = MI_ESIK["goruntu"]["fiyat_satir"]
    renkli = (M["yesil"] | M["kirmizi"])[y0:y1].sum(0) > 0
    oz = [(a, b) for a, b in _mi_kosu(renkli) if b - a + 1 >= 20]
    mer = np.array([(a + b) / 2.0 for a, b in oz])
    if len(mer) < 5:
        raise MIHata(f"ızgara için yeterli gövde yok ({len(mer)})")
    df = np.diff(mer); b0 = float(np.median(df[(df > 30) & (df < 60)]))
    k = np.round((mer - mer[0]) / b0)
    b, a = np.polyfit(k, mer, 1)
    art = mer - (a + b * k)
    if np.abs(art).max() > 3.0:
        raise MIHata(f"ızgara artığı büyük ({np.abs(art).max():.2f} px)")
    return float(a), float(b), mer.tolist()


def _mi_bant_izle(M: Dict[str, np.ndarray], merkezler: Optional[List[float]] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Lavanta bant çizgilerini sütun sütun izler (üst / orta / alt satır merkezleri; gözlenmeyen NaN). Mum merkezlerinin +-6 pikseli
    (fitil kenarları lavantaya benzer) ve 10 pikselden uzun dikey koşular (fitil) dışarıda; görünmeyen aralıkta tolerans aralıkla büyür."""
    y0, y1 = MI_ESIK["goruntu"]["fiyat_satir"]; tol = MI_ESIK["goruntu"]["bant_izleme_tol"]
    Bm = M["bant"] & ~M["turuncu"]; W = Bm.shape[1]
    yasak = np.zeros(W, bool)
    for xc in (merkezler or []):
        yasak[max(0, int(round(xc)) - 6):min(W, int(round(xc)) + 7)] = True
    mer = []
    for x in range(W):
        mer.append([] if yasak[x] else [(a + b) / 2.0 + y0 for a, b in _mi_kosu(Bm[y0:y1, x]) if 1 <= b - a <= 10])
    ref = [x for x in range(W) if len(mer[x]) == 3]
    if not ref:
        raise MIHata("bant: üç çizginin göründüğü sütun yok")
    x0 = ref[len(ref) // 2]
    U = np.full(W, np.nan); Mi = np.full(W, np.nan); Lo = np.full(W, np.nan)
    U[x0], Mi[x0], Lo[x0] = mer[x0]
    for yon in (1, -1):
        onc = list(mer[x0]); son_x = [x0, x0, x0]; x = x0 + yon
        while 0 <= x < W:
            for li, arr in enumerate((U, Mi, Lo)):
                if not mer[x]:
                    continue
                c = np.array(mer[x]); k = int(np.argmin(np.abs(c - onc[li])))
                if abs(c[k] - onc[li]) <= tol + 0.4 * abs(x - son_x[li] - yon):
                    arr[x] = c[k]; onc[li] = float(c[k]); son_x[li] = x
            x += yon
    return U, Mi, Lo


def _mi_bant_x(arr: np.ndarray, xc: float) -> Tuple[float, bool]:
    """xc çevresindeki (merkezin +-14..22 px) gözlenen bant sütunlarına doğru uydurup xc'de değer; yetmezse (turuncu çizgi altında) iki
    yandaki en yakın gözlenen sütunlar arasında doğrusal ara değer (en çok 100 px). Döner (değer, ara_deger_mi)."""
    a, b = MI_ESIK["goruntu"]["bant_yari"]
    xs = [x for x in range(int(xc - b), int(xc + b) + 1) if 0 <= x < len(arr) and abs(x - xc) >= a and np.isfinite(arr[x])]
    if len(xs) >= 4:
        p = np.polyfit(np.array(xs, float), arr[xs], 1)
        return float(np.polyval(p, xc)), False
    sol = [x for x in range(int(xc) - 1, max(-1, int(xc) - 101), -1) if np.isfinite(arr[x])]
    sag = [x for x in range(int(xc) + 1, min(len(arr), int(xc) + 101)) if np.isfinite(arr[x])]
    if sol and sag:
        x1, x2 = sol[0], sag[0]
        return float(arr[x1] + (arr[x2] - arr[x1]) * (xc - x1) / (x2 - x1)), True
    return float("nan"), True


def mi_mum(M: Dict[str, np.ndarray], xc: float) -> Optional[Dict[str, Any]]:
    """Izgara merkezindeki mum: gövde (katı renk) ya da doji çizgisi, fitil (mavi-gri mürekkep koşusu, boşluk <= 2)."""
    G_ = MI_ESIK["goruntu"]; y0, y1 = G_["fiyat_satir"]; W = M["yesil"].shape[1]
    x = int(round(xc)); hy = G_["govde_yari"]
    c0, c1 = max(0, x - hy), min(W, x + hy + 1)
    if c1 - c0 < 3:
        return None
    gs = M["yesil"][y0:y1, c0:c1].sum(1); rs = M["kirmizi"][y0:y1, c0:c1].sum(1)
    sat = np.flatnonzero((gs + rs) >= G_["govde_satir_min"])
    doji = False
    if len(sat):
        ust, alt = int(sat.min() + y0), int(sat.max() + y0); renk = "Y" if gs.sum() > rs.sum() else "K"
    else:
        cols = [c for c in list(range(x - 11, x - 3)) + list(range(x + 4, x + 12)) if 0 <= c < W]
        if not cols:
            return None
        gl = M["yesil_acik"][y0:y1, cols].sum(1); rl = M["kirmizi_acik"][y0:y1, cols].sum(1)
        tik = np.flatnonzero((gl + rl) >= 3)
        if not len(tik):
            return None
        ust, alt = int(tik.min() + y0), int(tik.max() + y0); renk = "Y" if gl.sum() > rl.sum() else "K"; doji = True
    fy = G_["fitil_yari"]; w0, w1 = max(0, x - fy), min(W, x + fy + 1)
    ink = (M["fitil"][:, w0:w1] | M["yesil"][:, w0:w1] | M["kirmizi"][:, w0:w1] | M["yesil_acik"][:, w0:w1] | M["kirmizi_acik"][:, w0:w1]).any(1)
    gap_max = G_["fitil_bosluk"]

    def uzat(bas: int, adim: int) -> int:
        y = bas; son = bas; bos = 0
        while y0 < y < y1 - 1:
            y += adim
            if ink[y]:
                son = y; bos = 0
            else:
                bos += 1
                if bos > gap_max:
                    break
        return son
    hi = uzat(ust, -1); lo = uzat(alt, +1)
    return {"x": float(xc), "renk": renk, "doji_cizgi": doji, "govde_ust": ust, "govde_alt": alt, "fitil_ust": hi, "fitil_alt": lo}


def mi_konum_px(M: Dict[str, np.ndarray], x: float, ust: int, alt: int) -> str:
    """İÇ / ÇİZGİ / DIŞ (MI_ESIK['goruntu']['konum'])."""
    xi = int(round(x)); T = M["turuncu"]
    if not (0 <= xi < T.shape[1]):
        return "KESIK"
    if T[(ust + alt) // 2, xi]:
        return "CIZGI"
    kol = np.flatnonzero(T[:, xi])
    if len(kol) and (kol < ust - 2).any() and (kol > alt + 2).any():
        return "IC"
    return "DIS"


def mi_sayisallastir(yol: Optional[str] = None) -> Dict[str, Any]:
    """Görüntü -> mum tablosu (piksel; y yukarı), bant, konum, şablon sınıfları."""
    im = mi_goruntu_oku(yol); M = mi_maskeler(im); Hh, W = im.shape[:2]
    a, b, mer = mi_izgara(M)
    kmin0 = int(math.ceil((0 - a) / b - 0.5)); kmax0 = int(math.floor((W + b - 1 - a) / b))
    U, Mi, Lo = _mi_bant_izle(M, [a + b * k for k in range(kmin0, kmax0 + 1)])
    kmin = int(math.ceil((0 - a) / b - 0.5)); kmax = int(math.floor((W + b - 1 - a) / b))
    sat = []
    for k in range(kmin, kmax + 1):
        xc = a + b * k
        r: Dict[str, Any] = {"i": k, "x": round(xc, 2)}
        if xc > W - 1:
            # görüntü kenarında kesilen mum: görünen gövde satırları
            sutun = slice(int(xc - MI_ESIK["goruntu"]["govde_yari"]), W)
            y0, y1 = MI_ESIK["goruntu"]["fiyat_satir"]
            g = (M["yesil"] | M["kirmizi"])[y0:y1, sutun].sum(1)
            s = np.flatnonzero(g >= 2)
            if not len(s):
                continue
            r.update({"konum": "KESIK", "renk": "Y" if M["yesil"][y0:y1, sutun].sum() >= M["kirmizi"][y0:y1, sutun].sum() else "K",
                      "doji_cizgi": False, "govde_ust": int(s.min() + y0), "govde_alt": int(s.max() + y0), "fitil_ust": np.nan, "fitil_alt": np.nan})
            sat.append(r); continue
        m = mi_mum(M, xc)
        if m is None:
            xi = int(round(xc)); y0, y1 = MI_ESIK["goruntu"]["fiyat_satir"]
            if 0 <= xi < W and M["turuncu"][y0:y1, xi].any():
                r.update({"konum": "GIZLI", "renk": "?", "doji_cizgi": False, "govde_ust": np.nan, "govde_alt": np.nan,
                          "fitil_ust": np.nan, "fitil_alt": np.nan})
                sat.append(r)
            continue
        r.update(m); r["konum"] = mi_konum_px(M, xc, m["fitil_ust"], m["fitil_alt"])
        sat.append(r)
    T = pd.DataFrame(sat).sort_values("i").reset_index(drop=True)
    for c, arr in (("bant_ust", U), ("bant_orta", Mi), ("bant_alt", Lo)):
        v = [_mi_bant_x(arr, x) if x <= W - 1 else (float("nan"), True) for x in T.x]
        T[c] = [z[0] for z in v]; T[c + "_ara"] = [z[1] for z in v]
    # piksel -> fiyat (y yukarı pozitif)
    Y = float(Hh)
    gu, ga = T.govde_ust.astype(float), T.govde_alt.astype(float)
    yes = T.renk == "Y"; doj = T.doji_cizgi.astype(bool)
    orta = (gu + ga) / 2
    T["O"] = np.where(doj, Y - orta, np.where(yes, Y - ga, Y - gu))
    T["C"] = np.where(doj, Y - orta, np.where(yes, Y - gu, Y - ga))
    T["H"] = Y - T.fitil_ust.astype(float); T["L"] = Y - T.fitil_alt.astype(float)
    T["BU"] = Y - T.bant_ust; T["BO"] = Y - T.bant_orta; T["BA"] = Y - T.bant_alt
    # sınıf: bölge (İÇ), bağlam (bölgenin solundaki DIŞ / ÇİZGİ), gizli, kesik
    ic = np.flatnonzero(T.konum.to_numpy() == "IC")
    if not len(ic):
        raise MIHata("turuncu dairenin içinde mum bulunamadı")
    ilk, son = int(ic.min()), int(ic.max())
    if not (T.konum.iloc[ilk:son + 1] == "IC").all():
        raise MIHata(f"bölge mumları kesintili: {T.konum.iloc[ilk:son + 1].tolist()}")
    sinif = np.full(len(T), "DIS", dtype=object)
    sinif[ilk:son + 1] = "BOLGE"
    for i in range(ilk):
        sinif[i] = "GIZLI" if T.konum.iloc[i] == "GIZLI" else "BAGLAM"
    for i in range(son + 1, len(T)):
        sinif[i] = "KESIK" if T.konum.iloc[i] == "KESIK" else "SAG"
    T["sinif"] = sinif
    T["k_izgara"] = T.i.astype(int)
    T["i"] = T.k_izgara - int(T.k_izgara.iloc[ilk]) + 1          # bölgenin ilk mumu 1; bağlam <= 0
    B = T[T.sinif == "BOLGE"]
    if B[["O", "H", "L", "C", "BU", "BO", "BA"]].isna().any().any():
        raise MIHata("bölge mumlarında eksik ölçü (fitil / bant)")
    if ((B.H < B[["O", "C"]].max(axis=1) - 1e-9) | (B.L > B[["O", "C"]].min(axis=1) + 1e-9)).any():
        raise MIHata("bölge mumu H / L gövdeyi kapsamıyor")
    # tepe: bölge sonundaki ardışık H > üst bant mumları
    ust_asim = (B.H > B.BU).to_numpy()
    nt = 0
    for v in ust_asim[::-1]:
        if not v:
            break
        nt += 1
    return {"tablo": T, "izgara": {"a": a, "b": b, "govde_merkez": mer}, "n_bolge": int(len(B)), "n_tepe": int(nt),
            "goruntu_sha": _mi_sha(yol or MI_YOL["goruntu"]), "boyut": [W, Hh]}


# ================================================================ 2) PARMAK İZİ (B)
def _mi_egim_r2(Y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Satır başına y = a + b x (x = 0..m-1) eğimi ve R^2."""
    N, m = Y.shape; x = np.arange(m, dtype=float); xc = x - x.mean(); sxx = float((xc ** 2).sum())
    yc = Y - Y.mean(1, keepdims=True)
    b = (yc * xc).sum(1) / sxx
    syy = (yc ** 2).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        r2 = np.where(syy > 0, (b * b * sxx) / syy, 0.0)
    return b, np.clip(r2, 0.0, 1.0)


def mi_ozellik(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, BU: np.ndarray, BO: np.ndarray, BA: np.ndarray) -> Dict[str, np.ndarray]:
    """Pencere başına MI_OZELLIK ölçüleri. Girdi (N, m) ya da (m,). Bütün ölçüler ölçek bağımsız ve sonlu."""
    A = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BO, BA)]
    O, H, L, C, BU, BO, BA = A
    N, m = C.shape
    rng = np.maximum(H - L, 1e-12); u = rng.mean(1); uk = u[:, None]
    ust_g = np.maximum(O, C); alt_g = np.minimum(O, C)
    body = np.abs(C - O); upw = np.maximum(H - ust_g, 0.0); low = np.maximum(alt_g - L, 0.0)
    F: Dict[str, np.ndarray] = {}
    F["boy_cv"] = rng.std(1) / u
    F["govde_oran"] = (body / rng).mean(1)
    F["ust_fitil"] = (upw / rng).mean(1)
    F["alt_fitil"] = (low / rng).mean(1)
    eps = 0.05 * m * u
    F["ust_alt_log"] = np.log((upw.sum(1) + eps) / (low.sum(1) + eps))
    F["yesil_pay"] = (C > O).mean(1)
    F["doji_pay"] = (body / rng < 0.10).mean(1)
    F["uzun_ust_pay"] = (upw / rng >= 0.5).mean(1)
    F["buyuk_mum_pay"] = (rng >= 1.5 * uk).mean(1)
    F["kucuk_mum_pay"] = (rng <= 0.7 * uk).mean(1)
    F["yuk_dip_pay"] = (L[:, 1:] > L[:, :-1]).mean(1)
    F["yuk_tepe_pay"] = (H[:, 1:] > H[:, :-1]).mean(1)
    F["yuk_kapanis_pay"] = (C[:, 1:] > C[:, :-1]).mean(1)
    ort = np.maximum(np.minimum(H[:, 1:], H[:, :-1]) - np.maximum(L[:, 1:], L[:, :-1]), 0.0)
    F["ortusme"] = (ort / np.minimum(rng[:, 1:], rng[:, :-1])).mean(1)
    b, _ = _mi_egim_r2((O + C) / 2 / uk); F["govde_orta_egim"] = b
    b, r2 = _mi_egim_r2(C / uk); F["kapanis_egim"] = b; F["kapanis_r2"] = r2
    F["net_hareket"] = (C[:, -1] - O[:, 0]) / u
    imin = L.argmin(1); imax = H.argmax(1)
    F["dipten_yukselis"] = (C[:, -1] - L[np.arange(N), imin]) / u
    F["dip_konum"] = imin / (m - 1)
    F["tepe_konum"] = imax / (m - 1)
    sonra = np.arange(m)[None, :] > imin[:, None]
    ns = sonra.sum(1)
    lf = (low / rng); uf = (upw / rng)
    F["dip_sonrasi_alt_fitil"] = np.where(ns > 0, (lf * sonra).sum(1) / np.maximum(ns, 1), F["alt_fitil"])
    F["dip_sonrasi_ust_fitil"] = np.where(ns > 0, (uf * sonra).sum(1) / np.maximum(ns, 1), F["ust_fitil"])
    gen = BU - BA
    with np.errstate(invalid="ignore", divide="ignore"):
        pB = np.where(gen > 0, (C - BA) / np.where(gen > 0, gen, 1.0), 0.5)
    k3 = min(3, m)
    F["pB_bas"] = pB[:, :k3].mean(1); F["pB_son"] = pB[:, -k3:].mean(1)
    b, _ = _mi_egim_r2(pB); F["pB_egim"] = b
    ust = C > BO
    F["sma_ustu_pay"] = ust.mean(1)
    F["sma_mesafe_son"] = (C[:, -1] - BO[:, -1]) / u
    # kalıcı geçiş: sondan geriye ardışık üstte koşusu
    kos = np.zeros(N, int)
    hepsi = np.ones(N, bool)
    for k in range(m - 1, -1, -1):
        hepsi &= ust[:, k]; kos += hepsi
    F["sma_gecis_konum"] = np.where(kos > 0, (m - kos) / m, 1.0)
    gn = gen / uk
    F["bant_gen_bas"] = gn[:, :k3].mean(1)
    F["bant_gen_oran_log"] = np.log(np.maximum(gn[:, -k3:].mean(1), 1e-6) / np.maximum(gn[:, :k3].mean(1), 1e-6))
    F["bant_dar_konum"] = gen.argmin(1) / (m - 1)
    b, _ = _mi_egim_r2(BO / uk); F["sma_egim"] = b
    F["ust_bant_asim_pay"] = (H > BU).mean(1)
    F["alt_bant_asim_pay"] = (L < BA).mean(1)
    for k, v in F.items():
        F[k] = np.where(np.isfinite(v), v, 0.0)
    return F


def mi_dizi(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, BU: np.ndarray, BA: np.ndarray, Lh: int) -> Tuple[np.ndarray, np.ndarray]:
    """Normalleştirilmiş mum dizisi z (N, Lh, 4) ve %B (N, Lh); pencere Lh mumuna doğrusal yeniden örneklenir."""
    O, H, L, C, BU, BA = [np.atleast_2d(np.asarray(v, float)) for v in (O, H, L, C, BU, BA)]
    N, m = C.shape
    u = np.maximum((H - L).mean(1), 1e-12)[:, None]; ref = ((H + L) / 2).mean(1)[:, None]
    Z = np.stack([(X - ref) / u for X in (O, H, L, C)], -1)
    gen = BU - BA
    with np.errstate(invalid="ignore", divide="ignore"):
        pB = np.where(gen > 0, (C - BA) / np.where(gen > 0, gen, 1.0), 0.5)
    if m != Lh:
        q = np.linspace(0.0, m - 1.0, Lh); i0 = np.minimum(np.floor(q).astype(int), m - 2); w = q - i0
        Z = Z[:, i0, :] * (1 - w)[None, :, None] + Z[:, i0 + 1, :] * w[None, :, None]
        pB = pB[:, i0] * (1 - w)[None, :] + pB[:, i0 + 1] * w[None, :]
    return Z, pB


def mi_mesafe(Z: np.ndarray, pB: np.ndarray, F: Dict[str, np.ndarray], sab: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    D1 = np.sqrt(((Z - sab["Z"][None]) ** 2).mean((1, 2)))
    D2 = np.sqrt(((pB - sab["pB"][None]) ** 2).mean(1))
    alt = MI_ESIK["benzerlik"]["ozellik_alt"]; sd = sab.get("sd") or {k: 1.0 for k in alt}
    D3 = np.sqrt(np.mean([((F[k] - sab["F"][k]) / sd[k]) ** 2 for k in alt], axis=0))
    return D1, D2, D3


def mi_S_bilesen(D1: np.ndarray, D2: np.ndarray, D3: np.ndarray, tau: List[float]) -> np.ndarray:
    return np.exp(-(D1 / tau[0] + D2 / tau[1] + D3 / tau[2]) / 3.0)


def mi_S_pencere(O, H, L, C, BU, BO, BA, sab: Dict[str, Any]) -> np.ndarray:
    """Pencereler (N, m) -> S (N,)."""
    if sab.get("tau") is None:
        raise MIHata("şablon kalibre değil (tau yok): önce 'sentetik'")
    F = mi_ozellik(O, H, L, C, BU, BO, BA)
    Z, pB = mi_dizi(O, H, L, C, BU, BA, sab["L"])
    return mi_S_bilesen(*mi_mesafe(Z, pB, F, sab), sab["tau"])


def mi_bant(C: np.ndarray, n: int = 20, k: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Bollinger (SMA n, k x std ddof 0) yalnız t'ye kadarki kapanışlarla; ilk n-1 bar NaN."""
    C = np.asarray(C, float); T = len(C)
    BU = np.full(T, np.nan); BO = np.full(T, np.nan); BA = np.full(T, np.nan)
    if T >= n:
        W = _swv(C, n); mu = W.mean(1); sd = W.std(1)
        BO[n - 1:] = mu; BU[n - 1:] = mu + k * sd; BA[n - 1:] = mu - k * sd
    return BU, BO, BA


def mi_tara_seri(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, sab: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
    """Bir seride her pencere sonu e için en büyük S (uzunluklar sab['uzunluklar']) ve o uzunluk. Pencere başı bandın tanımlı olduğu
    ilk bardan (n-1) sonra. Yalnız e'ye kadarki barlar."""
    O, H, L, C = (np.asarray(v, float) for v in (O, H, L, C))
    T = len(C); nb = int(MI_ESIK["benzerlik"]["bant"]["n"])
    BU, BO, BA = mi_bant(C, nb, float(MI_ESIK["benzerlik"]["bant"]["k"]))
    best = np.full(T, np.nan); bm = np.zeros(T, np.int64); s0 = nb - 1
    for m in sab["uzunluklar"]:
        if T - s0 < m:
            continue
        W = [_swv(x[s0:], m) for x in (O, H, L, C, BU, BO, BA)]
        S = mi_S_pencere(*W, sab)
        e = np.arange(s0 + m - 1, T)
        iyi = ~(S <= best[e])
        best[e[iyi]] = S[iyi]; bm[e[iyi]] = m
    return best, bm


def mi_sablon_kur(D: Dict[str, Any], kal: Optional[Dict[str, Any]] = None) -> Dict[str, Dict[str, Any]]:
    """Sayısallaştırmadan iki şablon (tam, tepesiz). kal: {'tam': {'tau', 'sd'}, 'tepesiz': {...}} (sentetik kalibrasyonu)."""
    T = D["tablo"]; B = T[T.sinif == "BOLGE"].reset_index(drop=True); nt = int(D["n_tepe"])
    out: Dict[str, Dict[str, Any]] = {}
    for ad, n in (("tam", len(B)), ("tepesiz", len(B) - nt)):
        X = B.iloc[:n]
        arr = {c: X[c].to_numpy(float) for c in ("O", "H", "L", "C", "BU", "BO", "BA")}
        F = {k: float(v[0]) for k, v in mi_ozellik(*(arr[c] for c in ("O", "H", "L", "C", "BU", "BO", "BA"))).items()}
        Z, pB = mi_dizi(arr["O"], arr["H"], arr["L"], arr["C"], arr["BU"], arr["BA"], n)
        uz = sorted({int(round(n * f)) for f in MI_ESIK["sablon"]["esneme"]})
        s = {"ad": ad, "L": int(n), "uzunluklar": uz, "Z": Z[0], "pB": pB[0], "F": F, "ohlc": arr, "tau": None, "sd": None}
        if kal and ad in kal:
            s["tau"] = list(map(float, kal[ad]["tau"])); s["sd"] = {k: float(v) for k, v in kal[ad]["sd"].items()}
        out[ad] = s
    return out


def mi_baglam_olcu(D: Dict[str, Any]) -> Dict[str, float]:
    T = D["tablo"]; B = T[T.sinif == "BOLGE"]; G = T[(T.sinif == "BAGLAM") & T.H.notna() & T.L.notna()]
    u = float((B.H - B.L).mean())
    if not len(G):
        return {k: float("nan") for k, _ in MI_BAGLAM_OZ}
    kr = G[G.renk == "K"]
    k = kr.loc[(kr.H - kr.L).idxmax()] if len(kr) else G.iloc[-1]
    return {"baglam_kirmizi_boy": float((k.H - k.L) / u), "baglam_kirmizi_govde": float(abs(k.C - k.O) / u),
            "baglam_dusus": float((G.H.max() - B.L.min()) / u)}


def mi_parmak_tablo(D: Dict[str, Any], S: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """Parmak izi tablosu (tam ve tepesiz) + bağlam + görsel okuma maddeleri."""
    sat = []
    for k, acik, grup in MI_OZELLIK:
        sat.append({"olcu": k, "aciklama": acik, "grup": grup, "tam": S["tam"]["F"][k], "tepesiz": S["tepesiz"]["F"][k],
                    "benzerlikte": k in MI_ESIK["benzerlik"]["ozellik_alt"]})
    for k, v in mi_baglam_olcu(D).items():
        sat.append({"olcu": k, "aciklama": dict(MI_BAGLAM_OZ)[k], "grup": "baglam", "tam": v, "tepesiz": v, "benzerlikte": False})
    return pd.DataFrame(sat)


def mi_gorsel_okuma(D: Dict[str, Any], S: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Cemal'in görsel okuması (iş tanımı B) -> sayıyla doğrulama (tam şablon)."""
    T = D["tablo"]; B = T[T.sinif == "BOLGE"].reset_index(drop=True); F = S["tam"]["F"]
    rng = (B.H - B.L).to_numpy(); u = rng.mean()
    imin = int(B.L.to_numpy().argmin())
    sonra = B.iloc[imin + 1:]
    kucuk_sonra = float((((sonra.H - sonra.L) / u) <= 1.0).mean()) if len(sonra) else float("nan")
    gen = (B.BU - B.BA).to_numpy() / u
    pB = ((B.C - B.BA) / (B.BU - B.BA)).to_numpy()
    out = [
        {"madde": "dipten sonra küçük mumlar", "olcu": f"dip mumu {imin + 1}. mum; sonraki {len(sonra)} mumun %{100 * kucuk_sonra:.0f}'i ortalama boyun altında",
         "dogru": bool(kucuk_sonra >= 0.5)},
        {"madde": "uzun üst fitiller", "olcu": f"ort üst fitil / boy {F['ust_fitil']:.2f}; üst fitil >= boyun yarısı olan mum {int(round(F['uzun_ust_pay'] * len(B)))} / {len(B)}",
         "dogru": bool(F["ust_fitil"] > F["alt_fitil"])},
        {"madde": "kısa alt fitiller", "olcu": f"ort alt fitil / boy {F['alt_fitil']:.2f} (üst {F['ust_fitil']:.2f}); dipten sonra alt fitil {F['dip_sonrasi_alt_fitil']:.2f}",
         "dogru": bool(F["alt_fitil"] < F["ust_fitil"])},
        {"madde": "yükselen dipler", "olcu": f"yükselen dip payı {F['yuk_dip_pay']:.2f}; dipten sonra {float((sonra.L.diff().dropna() > 0).mean()) if len(sonra) > 1 else float('nan'):.2f}",
         "dogru": bool(F["yuk_dip_pay"] > 0.5)},
        {"madde": "alt banttan SMA20 üstüne geçiş", "olcu": f"%B ilk 3 mum {F['pB_bas']:.2f}, son 3 mum {F['pB_son']:.2f}; kalıcı SMA üstü geçiş {F['sma_gecis_konum']:.2f} konumunda",
         "dogru": bool(F["pB_bas"] < 0.5 < F["pB_son"])},
        {"madde": "üst banda yürüyüş", "olcu": f"son {int(D['n_tepe'])} mumun High'ı üst bandın üstünde; %B son 3 = {F['pB_son']:.2f}",
         "dogru": bool(D["n_tepe"] >= 2 and F["pB_son"] >= 0.8)},
        {"madde": "bant önce dar, sonra açılıyor",
         "olcu": (f"bant genişliği (mum boyu): ilk 3 mum {gen[:3].mean():.2f}, en dar {gen.min():.2f} ({int(gen.argmin()) + 1}. mum, konum "
                  f"{F['bant_dar_konum']:.2f}), son 3 mum {gen[-3:].mean():.2f}; en dar / ilk 3 = {gen.min() / gen[:3].mean():.2f}, son 3 / en dar = "
                  f"{gen[-3:].mean() / gen.min():.2f}"),
         "dogru": (True if (F["bant_dar_konum"] <= 0.5 and gen[-3:].mean() >= 1.2 * gen.min()) else
                   ("KISMEN" if gen[-3:].mean() >= 1.2 * gen.min() else False))},
        {"madde": "%B dizisi (mum mum)", "olcu": " ".join(f"{v:.2f}" for v in pB), "dogru": None},
    ]
    return out


def mi_bindirme_png(D: Dict[str, Any], yol: Optional[str] = None, kirp: Optional[Tuple[int, int, int, int]] = None,
                    olcek: int = 1) -> str:
    """Kodun gördüğü mumları orijinal görüntünün üstüne çizer (gövde mavi çerçeve, fitil siyah, bant mor nokta, numara)."""
    from PIL import Image, ImageDraw
    im = Image.open(MI_YOL["goruntu"]).convert("RGB"); dr = ImageDraw.Draw(im)
    T = D["tablo"]
    renk = {"BOLGE": (0, 70, 255), "BAGLAM": (120, 0, 160), "GIZLI": (255, 0, 255), "KESIK": (0, 160, 160), "SAG": (90, 90, 90), "DIS": (90, 90, 90)}
    for r in T.itertuples():
        x = float(r.x); rc = renk.get(r.sinif, (0, 0, 0))
        if np.isfinite(r.govde_ust):
            dr.rectangle([x - 14, r.govde_ust - 1, x + 14, r.govde_alt + 1], outline=rc, width=2)
        if np.isfinite(r.fitil_ust):
            dr.line([x + 16, r.fitil_ust, x + 16, r.fitil_alt], fill=(0, 0, 0), width=2)
            dr.line([x + 12, r.fitil_ust, x + 20, r.fitil_ust], fill=(0, 0, 0), width=2)
            dr.line([x + 12, r.fitil_alt, x + 20, r.fitil_alt], fill=(0, 0, 0), width=2)
        for c in ("bant_ust", "bant_orta", "bant_alt"):
            v = getattr(r, c)
            if np.isfinite(v):
                dr.ellipse([x - 4, v - 4, x + 4, v + 4], outline=(200, 0, 200), width=2)
        yy = (r.fitil_ust if np.isfinite(r.fitil_ust) else (r.govde_ust if np.isfinite(r.govde_ust) else 600)) - 30
        etik = f"{r.i}" + ("" if r.sinif == "BOLGE" else {"BAGLAM": "b", "GIZLI": "g", "KESIK": "k"}.get(r.sinif, ""))
        dr.text((x - 8, yy), etik, fill=rc)
    if kirp is not None:
        im = im.crop(kirp)
        if olcek > 1:
            im = im.resize((im.size[0] * olcek, im.size[1] * olcek), Image.NEAREST)
    y = yol or _mi_yol("bindirme")
    os.makedirs(os.path.dirname(os.path.abspath(y)), exist_ok=True)
    im.save(y)
    return y


def mi_elle_png(D: Dict[str, Any], yol: Optional[str] = None, n: int = 3, tohum: int = 2515) -> Dict[str, Any]:
    """K10: bölgeden rastgele n mumun yakın planı (sol: ham, sağ: bindirme) tek PNG'de; seçilen mumların sayıları."""
    from PIL import Image
    T = D["tablo"]; B = T[T.sinif == "BOLGE"]
    rng = np.random.default_rng(tohum); sec = sorted(rng.choice(B.index.to_numpy(), size=min(n, len(B)), replace=False).tolist())
    ham = Image.open(MI_YOL["goruntu"]).convert("RGB")
    tmp = os.path.join(MI_YOL["gecici"], "bindirme_tam.png"); mi_bindirme_png(D, tmp); bnd = Image.open(tmp).convert("RGB")
    parca = []; bilgi = []
    for i in sec:
        r = T.loc[i]; x = int(r.x); y0 = int(min(r.fitil_ust, r.bant_ust) - 40); y1 = int(max(r.fitil_alt, r.bant_alt) + 40)
        kut = (max(0, x - 40), max(0, y0), min(1080, x + 40), min(2400, y1))
        a = ham.crop(kut).resize(((kut[2] - kut[0]) * 3, (kut[3] - kut[1]) * 3), Image.NEAREST)
        b = bnd.crop(kut).resize(a.size, Image.NEAREST)
        c = Image.new("RGB", (a.size[0] * 2 + 10, a.size[1]), (255, 255, 255)); c.paste(a, (0, 0)); c.paste(b, (a.size[0] + 10, 0))
        parca.append(c)
        bilgi.append({"i": int(r.i), "x": float(r.x), "renk": r.renk, "doji_cizgi": bool(r.doji_cizgi), "govde_ust": int(r.govde_ust),
                      "govde_alt": int(r.govde_alt), "fitil_ust": int(r.fitil_ust), "fitil_alt": int(r.fitil_alt),
                      "bant_ust": round(float(r.bant_ust), 1), "bant_orta": round(float(r.bant_orta), 1), "bant_alt": round(float(r.bant_alt), 1)})
    Wt = sum(p.size[0] for p in parca) + 20 * (len(parca) - 1); Ht = max(p.size[1] for p in parca)
    out = Image.new("RGB", (Wt, Ht), (255, 255, 255)); x = 0
    for p in parca:
        out.paste(p, (x, 0)); x += p.size[0] + 20
    y = yol or _mi_yol("elle"); out.save(y)
    return {"png": y, "mumlar": bilgi}


def mi_sayisallastir_kos(cikti: Optional[str] = None) -> Dict[str, Any]:
    """A + B: mum tablosu, şablon json (kalibrasyonsuz), parmak izi csv, bindirme ve elle doğrulama PNG."""
    cikti = cikti or MI_YOL["cikti"]
    D = mi_sayisallastir()
    T = D["tablo"]
    T.to_csv(_mi_yol("mumlar", cikti), index=False, float_format="%.3f")
    S = mi_sablon_kur(D)
    P = mi_parmak_tablo(D, S); P.to_csv(_mi_yol("parmak", cikti), index=False, float_format="%.4f")
    J = {"surum": MI_SURUM, "zaman": _mi_simdi(), "goruntu_sha": D["goruntu_sha"], "izgara": D["izgara"], "n_bolge": D["n_bolge"],
         "n_tepe": D["n_tepe"], "sinif_sayim": T.sinif.value_counts().to_dict(),
         "renk_dizisi": "".join(T[T.sinif == "BOLGE"].renk.tolist()),
         "sablon": {k: {"L": v["L"], "uzunluklar": v["uzunluklar"], "Z": v["Z"], "pB": v["pB"], "F": v["F"], "ohlc": v["ohlc"]} for k, v in S.items()},
         "baglam": mi_baglam_olcu(D), "gorsel_okuma": mi_gorsel_okuma(D, S)}
    mi_bindirme_png(D, _mi_yol("bindirme", cikti))
    os.makedirs(MI_YOL["gecici"], exist_ok=True)
    J["elle"] = mi_elle_png(D, _mi_yol("elle", cikti))
    _mi_jyaz(_mi_yol("sablon", cikti), J, "şablon")
    milog.info("sayısallaştırma: %d bölge mumu (%s), tepe %d, sınıflar %s", D["n_bolge"], J["renk_dizisi"], D["n_tepe"], J["sinif_sayim"])
    return J


def mi_sablon_yukle(cikti: Optional[str] = None, kalibre: bool = True) -> Dict[str, Dict[str, Any]]:
    """Şablon json + (kalibre=True) sentetik json'daki tau / sd."""
    J = json.load(open(_mi_yol("sablon", cikti), encoding="utf-8"))
    out = {}
    for ad, v in J["sablon"].items():
        out[ad] = {"ad": ad, "L": int(v["L"]), "uzunluklar": [int(x) for x in v["uzunluklar"]], "Z": np.array(v["Z"], float),
                   "pB": np.array(v["pB"], float), "F": {k: float(x) for k, x in v["F"].items()},
                   "ohlc": {k: np.array(x, float) for k, x in v["ohlc"].items()}, "tau": None, "sd": None}
    if kalibre:
        yol = _mi_yol("sentetik", cikti)
        if not os.path.exists(yol):
            raise MIHata("sentetik json yok (kalibrasyon): önce 'sentetik'")
        K = json.load(open(yol, encoding="utf-8"))["kalibrasyon"]
        for ad in out:
            out[ad]["tau"] = [float(x) for x in K[ad]["tau"]]; out[ad]["sd"] = {k: float(x) for k, x in K[ad]["sd"].items()}
            out[ad]["esik"] = float(json.load(open(yol, encoding="utf-8"))["esik"][ad]["S"])
    return out


# ================================================================ 3) ÜRETİCİ ve GÖMME (D)
def mi_havuz_yap(V: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Üretici havuzu: ABD 2005-2014 geçerli barlarından mum tanımlayıcıları (rastgele 300 hisse, sabit tohum)."""
    E = MI_ESIK["uretec_havuz"]; a, b = pd.Timestamp(E["donem"][0]), pd.Timestamp(E["donem"][1])
    aday = []
    for s in sorted(V):
        d = V[s]; d = d[(d.index >= a) & (d.index <= b)]
        ok = (d.High > d.Low) & (d.Volume > 0) & (d.Low > 0) & (d.Open > 0) & (d.Close > 0)
        d = d[ok]
        if len(d) >= E["min_bar"] and float(d.Close.median()) >= E["min_fiyat"]:
            aday.append(s)
    rng = np.random.default_rng(E["tohum"]); sec = sorted(rng.choice(aday, size=min(E["hisse"], len(aday)), replace=False).tolist())
    desc = []
    for s in sec:
        d = V[s]; d = d[(d.index >= a) & (d.index <= b)]
        d = d[(d.High > d.Low) & (d.Volume > 0) & (d.Low > 0) & (d.Open > 0) & (d.Close > 0)]
        O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close"))
        lg = np.log(O[1:] / C[:-1]); lc = np.log(C[1:] / O[1:])
        uw = np.log(H[1:] / np.maximum(O[1:], C[1:])); lw = np.log(np.minimum(O[1:], C[1:]) / L[1:])
        X = np.stack([lg, lc, np.maximum(uw, 0), np.maximum(lw, 0)], 1)
        ok = (np.abs(X) <= 0.3).all(1) & np.isfinite(X).all(1)
        desc.append(X[ok])
    return {"sembol": sec, "desc": desc, "aday": len(aday), "bar": int(sum(len(x) for x in desc)), "donem": E["donem"]}


def mi_uret(rng: np.random.Generator, n: int, havuz: Optional[Dict[str, Any]], tip: str) -> Tuple[np.ndarray, ...]:
    """Log OHLC dizisi (n bar). 'blok': tek hissenin tanımlayıcılarından blok bootstrap; 'ry': saf rastgele yürüyüş."""
    Sn = MI_ESIK["sentetik"]
    if tip == "blok":
        X = havuz["desc"][int(rng.integers(len(havuz["desc"])))]; bl = int(Sn["blok"]); nb = int(math.ceil(n / bl))
        st = rng.integers(0, len(X) - bl, size=nb)
        D = np.concatenate([X[s:s + bl] for s in st])[:n]
    elif tip == "ry":
        sg = float(rng.uniform(*Sn["ry"]["sigma"]))
        D = np.stack([rng.normal(0, Sn["ry"]["bosluk_kat"] * sg, n), rng.normal(0, sg, n),
                      np.abs(rng.normal(0, Sn["ry"]["fitil_kat"] * sg, n)), np.abs(rng.normal(0, Sn["ry"]["fitil_kat"] * sg, n))], 1)
    else:
        raise MIHata(f"bilinmeyen üretici {tip}")
    lC = math.log(100.0) + np.cumsum(D[:, 0] + D[:, 1]); lO = lC - D[:, 1]
    lH = np.maximum(lO, lC) + D[:, 2]; lL = np.minimum(lO, lC) - D[:, 3]
    return lO, lH, lL, lC


def mi_baglam_uygula(lO: np.ndarray, lH: np.ndarray, lL: np.ndarray, lC: np.ndarray, p: int, tip: str) -> None:
    """[p-40, p-1] barlarına deterministik eğim (yerinde): dip = doğal eğim silinip bar başına -0,5 %, tepe +0,5 %, yatay = doğal eğim
    silinir. p ve sonrası aynı düzey kaymasıyla sürer (süreklilik)."""
    Sn = MI_ESIK["sentetik"]; nb = int(Sn["baglam_bar"]); a = p - nb
    if a < 1:
        raise MIHata("bağlam için seri başı yetersiz")
    dogal = (lC[p - 1] - lC[a - 1]) / nb
    mu = {"dip": -float(Sn["baglam_egim"]), "yatay": 0.0, "tepe": float(Sn["baglam_egim"])}[tip] - dogal
    kay = np.zeros(len(lC)); kay[a:p] = mu * np.arange(1, nb + 1); kay[p:] = mu * nb
    for x in (lO, lH, lL, lC):
        x += kay


def mi_gom(rng: np.random.Generator, lO: np.ndarray, lH: np.ndarray, lL: np.ndarray, lC: np.ndarray, p: int, sab: Dict[str, Any],
           gurultu: float, olcek: float, esneme: float) -> int:
    """Şablonu p'den itibaren gömer (yerinde); döner gömülü mum sayısı. Birim = olcek x son 20 barın medyan göreli boyu (H/L - 1); esneme: en yakın
    komşu ile mum tanımlayıcıları yeniden örneklenir, net hareket korunur; gürültü: her O / H / L / C'ye N(0, gurultu x birim)."""
    A = sab["ohlc"]; O, H, L, C = (np.asarray(A[c], float) for c in ("O", "H", "L", "C")); n = len(C)
    u_px = float((H - L).mean())
    g = np.r_[0.0, (O[1:] - C[:-1]) / u_px]; b = (C - O) / u_px
    wu = (H - np.maximum(O, C)) / u_px; wd = (np.minimum(O, C) - L) / u_px
    Le = max(3, int(round(n * esneme)))
    ix = np.rint(np.linspace(0, n - 1, Le)).astype(int)
    g2, b2, wu2, wd2 = g[ix].copy(), b[ix].copy(), wu[ix], wd[ix]
    g2[0] = 0.0
    duz = (float((g + b).sum()) - float((g2 + b2).sum())) / max(Le - 1, 1)
    g2[1:] += duz
    zC = np.cumsum(g2 + b2); zO = zC - b2
    zH = np.maximum(zO, zC) + wu2; zL = np.minimum(zO, zC) - wd2
    if gurultu > 0:
        zO = zO + rng.normal(0, gurultu, Le); zH = zH + rng.normal(0, gurultu, Le)
        zL = zL + rng.normal(0, gurultu, Le); zC = zC + rng.normal(0, gurultu, Le)
        zH = np.maximum.reduce([zH, zO, zC]); zL = np.minimum.reduce([zL, zO, zC])
    u_rel = float(olcek) * float(np.median(np.exp(lH[p - 20:p] - lL[p - 20:p]) - 1.0))
    if p + Le > len(lC):
        raise MIHata("gömme seri sonunu aşıyor")
    if 1.0 + float(min(zL.min(), 0.0)) * u_rel <= 0.05:
        raise MIHata("gömme: fiyat sıfıra yaklaşıyor (ölçek çok büyük)")
    bas = lC[p - 1]
    eski_son = lC[p + Le - 1]
    # doğrusal fiyat uzayında gömülür (şablon piksel = doğrusal fiyat): X = P0 (1 + z u_rel); seri log uzayında sürer
    for x, z in ((lO, zO), (lH, zH), (lL, zL), (lC, zC)):
        x[p:p + Le] = bas + np.log1p(z * u_rel)
    kay = lC[p + Le - 1] - eski_son
    for x in (lO, lH, lL, lC):
        x[p + Le:] += kay
    return Le


def _mi_tekil(e: np.ndarray, aralik: int) -> np.ndarray:
    """Sıralı indekslerden ilk kalır, sonraki >= aralik uzakta olmalı."""
    out = []; son = -10 ** 9
    for x in np.sort(e):
        if x - son >= aralik:
            out.append(x); son = x
    return np.array(out, np.int64)


def mi_kalibre(havuz: Dict[str, Any], sab: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """tau ve sd: blok bootstrap rastgele pencerelerinden (şablon uzunluğu L), sabit kök."""
    K = MI_ESIK["benzerlik"]["kalibrasyon"]; rng = np.random.default_rng(K["kok"]); nb = int(MI_ESIK["benzerlik"]["bant"]["n"])
    seriler = [mi_uret(rng, int(K["n"]), havuz, "blok") for _ in range(int(K["seri"]))]
    out = {}
    for ad, s in sab.items():
        m = s["L"]; Wl = {c: [] for c in ("O", "H", "L", "C", "BU", "BO", "BA")}
        for lO, lH, lL, lC in seriler:
            O, H, L, C = np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC)
            BU, BO, BA = mi_bant(C, nb)
            for c, x in zip(("O", "H", "L", "C", "BU", "BO", "BA"), (O, H, L, C, BU, BO, BA)):
                Wl[c].append(_swv(x[nb - 1:], m))
        W = {c: np.concatenate(v) for c, v in Wl.items()}
        sec = rng.choice(len(W["C"]), size=min(int(K["pencere"]), len(W["C"])), replace=False)
        W = {c: v[sec] for c, v in W.items()}
        F = mi_ozellik(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BO"], W["BA"])
        sd = {}
        for k in MI_ESIK["benzerlik"]["ozellik_alt"]:
            q = np.quantile(F[k], [0.25, 0.75]); v = float((q[1] - q[0]) / 1.349)
            sd[k] = v if v > 1e-9 else float(max(F[k].std(), 1e-6))
        s2 = dict(s); s2["sd"] = sd
        Z, pB = mi_dizi(W["O"], W["H"], W["L"], W["C"], W["BU"], W["BA"], m)
        D1, D2, D3 = mi_mesafe(Z, pB, F, s2)
        tau = [float(np.median(D1)), float(np.median(D2)), float(np.median(D3))]
        out[ad] = {"tau": tau, "sd": sd, "n_pencere": int(len(sec)),
                   "D_ceyrek": {"dizi": np.quantile(D1, [0.05, 0.5, 0.95]).tolist(), "bant": np.quantile(D2, [0.05, 0.5, 0.95]).tolist(),
                                "oz": np.quantile(D3, [0.05, 0.5, 0.95]).tolist()}}
    return out


def _mi_sentetik_seri(rng: np.random.Generator, havuz: Dict[str, Any], s: Dict[str, Any], uretec: str, baglam: str, gurultu: float
                      ) -> Dict[str, Any]:
    Sn = MI_ESIK["sentetik"]; p = int(Sn["seri_on"])
    esn = float(rng.uniform(*Sn["esneme"])); olc = float(math.exp(rng.uniform(math.log(Sn["olcek"][0]), math.log(Sn["olcek"][1]))))
    Le_max = int(round(s["L"] * Sn["esneme"][1])) + 1
    n = p + Le_max + int(Sn["seri_son"])
    lO, lH, lL, lC = mi_uret(rng, n, havuz, uretec)
    mi_baglam_uygula(lO, lH, lL, lC, p, baglam)
    Le = mi_gom(rng, lO, lH, lL, lC, p, s, gurultu, olc, esn)
    return {"O": np.exp(lO), "H": np.exp(lH), "L": np.exp(lL), "C": np.exp(lC), "p": p, "Le": Le, "e": p + Le - 1, "olcek": olc, "esneme": esn}


def mi_sentetik_kos(havuz: Dict[str, Any], sab: Dict[str, Dict[str, Any]], kok: int, tohum: Optional[int] = None,
                    sadece_gurultu: Optional[List[float]] = None) -> pd.DataFrame:
    """Gömülü seriler: koşul (şablon x üretici x bağlam x gürültü) x tohum -> en iyi S (gerçek sonun +-3 barında), bulunan pencere, ölçü
    farkları (bulunan vs gömülü gerçek pencere)."""
    Sn = MI_ESIK["sentetik"]; T = int(tohum or Sn["tohum"]); tol = int(Sn["konum_tol"]); nb = int(MI_ESIK["benzerlik"]["bant"]["n"])
    oz_ad = [k for k, _, _ in MI_OZELLIK]
    sat = []
    for si, (ad, s) in enumerate(sab.items()):
        for ui, ur in enumerate(Sn["uretec"]):
            for bi, bg in enumerate(Sn["baglam"]):
                for gi, gr in enumerate(sadece_gurultu or Sn["gurultu"]):
                    for t in range(T):
                        rng = np.random.default_rng([int(kok), si, ui, bi, int(round(gr * 100)), t])
                        X = _mi_sentetik_seri(rng, havuz, s, ur, bg, float(gr))
                        best, bm = mi_tara_seri(X["O"], X["H"], X["L"], X["C"], s)
                        e = X["e"]; a, b = max(0, e - tol), min(len(best) - 1, e + tol)
                        yak = best[a:b + 1]
                        if np.isfinite(yak).any():
                            k = int(np.nanargmax(yak)) + a; Sb = float(best[k]); mb = int(bm[k])
                        else:
                            k, Sb, mb = -1, float("nan"), 0
                        r = {"sablon": ad, "uretec": ur, "baglam": bg, "gurultu": gr, "tohum": t, "olcek": X["olcek"], "esneme": X["esneme"],
                             "Le": X["Le"], "S_iyi": Sb, "e_bulunan": k, "m_bulunan": mb, "e_gercek": e,
                             "S_gercek_pencere": float(best[e]) if np.isfinite(best[e]) else float("nan"),
                             "S_baska_max": float(np.nanmax(np.r_[best[:a], best[b + 1:]])) if np.isfinite(np.r_[best[:a], best[b + 1:]]).any() else float("nan")}
                        # birebir: bulunan pencere vs gömülü gerçek pencere ölçüleri
                        if k >= 0:
                            BU, BO, BA = mi_bant(X["C"], nb)
                            def oz(e_, m_):
                                sl = slice(e_ - m_ + 1, e_ + 1)
                                return mi_ozellik(X["O"][sl], X["H"][sl], X["L"][sl], X["C"][sl], BU[sl], BO[sl], BA[sl])
                            Fb = oz(k, mb); Fg = oz(e, X["Le"])
                            for kk in oz_ad:
                                r[f"fb_{kk}"] = float(Fb[kk][0]); r[f"fg_{kk}"] = float(Fg[kk][0])
                        sat.append(r)
            milog.info("sentetik kök %d: %s bitti (%d satır)", kok, ad, len(sat))
    return pd.DataFrame(sat)


def mi_yanlis_kos(havuz: Dict[str, Any], sab: Dict[str, Dict[str, Any]], kok: int) -> Dict[str, Any]:
    """Gömülmemiş seriler (iki üretici): S dağılımı (0,01 kutu) ve eşik ızgarasında ham / tekil eşleşme sayıları."""
    Y = MI_ESIK["sentetik"]["yanlis"]; out: Dict[str, Any] = {}
    kutu = np.linspace(0, 1, 101)
    for si, (ad, s) in enumerate(sab.items()):
        out[ad] = {}
        for ui, ur in enumerate(MI_ESIK["sentetik"]["uretec"]):
            hist = np.zeros(100, np.int64); n_pen = 0; tepe_S = []
            seriler_best = []
            for t in range(int(Y["seri"])):
                rng = np.random.default_rng([int(kok), 99, si, ui, t])
                lO, lH, lL, lC = mi_uret(rng, int(Y["n"]) + 60, havuz, ur)
                best, _ = mi_tara_seri(np.exp(lO), np.exp(lH), np.exp(lL), np.exp(lC), s)
                b = best[np.isfinite(best)]
                hist += np.histogram(b, kutu)[0]; n_pen += len(b); seriler_best.append(best)
            out[ad][ur] = {"hist": hist.tolist(), "n_pencere": int(n_pen), "_best": seriler_best}
    return out


def mi_yanlis_esik(Yb: Dict[str, Any], esik: float, tekil: int) -> Dict[str, float]:
    ham = 0; tek = 0; n = 0
    for best in Yb["_best"]:
        f = np.isfinite(best); n += int(f.sum())
        e = np.flatnonzero(f & (np.nan_to_num(best, nan=-1) >= esik))
        ham += len(e); tek += len(_mi_tekil(e, tekil))
    return {"ham_1000": 1000.0 * ham / max(n, 1), "tekil_1000": 1000.0 * tek / max(n, 1), "n_bar": n, "ham": ham, "tekil": tek}


def mi_esik_sec(R: pd.DataFrame, ad: str) -> Dict[str, Any]:
    """Kök A, %20 gürültü, bütün bağlam x üretici: yakalama >= %80 veren en yüksek S (0,01 ızgara)."""
    Es = MI_ESIK["sentetik"]["esik"]
    x = R[(R.sablon == ad) & (np.isclose(R.gurultu, Es["gurultu"]))].S_iyi.to_numpy(float)
    x = np.where(np.isfinite(x), x, -1.0)
    izg = np.round(np.arange(0, 1.0 + 1e-9, Es["izgara"]), 2)
    yak = np.array([(x >= t).mean() for t in izg])
    ok = izg[yak >= Es["yakalama"]]
    if not len(ok):
        raise MIHata(f"{ad}: hiçbir eşikte %20 gürültü yakalaması >= %80 değil")
    S = float(ok.max())
    return {"S": S, "yakalama": float((x >= S).mean()), "n": int(len(x)), "izgara": {f"{t:.2f}": float(v) for t, v in zip(izg, yak)}}


def mi_birebir(R: pd.DataFrame, esik: float, ref: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
    """Yakalanan tohumlarda bulunan pencere ölçüleri vs gömülü gerçek pencere ölçüleri: ort |fark| / sd ve tohum başına Pearson r. Ölçü
    başına ortalama / sd = kök A'daki bütün gömülü gerçek pencereler (ref); r merkezlenmiş (z = (F - ort) / sd) ölçü vektörlerinde."""
    oz = [k for k, _, _ in MI_OZELLIK]
    Y = R[R.S_iyi.to_numpy(float) >= esik]
    if not len(Y):
        return {"n": 0}
    Fb = Y[[f"fb_{k}" for k in oz]].to_numpy(float); Fg = Y[[f"fg_{k}" for k in oz]].to_numpy(float)
    mu = np.array([ref[k]["ort"] for k in oz]); sd = np.array([max(ref[k]["sd"], 1e-9) for k in oz])
    Zb = (Fb - mu) / sd; Zg = (Fg - mu) / sd
    mae = np.abs(Zb - Zg).mean(1)
    zbc = Zb - Zb.mean(1, keepdims=True); zgc = Zg - Zg.mean(1, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = (zbc * zgc).sum(1) / np.sqrt((zbc ** 2).sum(1) * (zgc ** 2).sum(1))
    tam = (Y.e_bulunan.to_numpy() == Y.e_gercek.to_numpy()) & (Y.m_bulunan.to_numpy() == Y.Le.to_numpy())
    olcu_mae = {k: float(np.abs(Zb[:, i] - Zg[:, i]).mean()) for i, k in enumerate(oz)}
    return {"n": int(len(Y)), "mae_sd": float(np.mean(mae)), "r_ort": float(np.nanmean(r)), "r_med": float(np.nanmedian(r)),
            "ayni_pencere_pay": float(tam.mean()), "son_ayni_pay": float((Y.e_bulunan.to_numpy() == Y.e_gercek.to_numpy()).mean()),
            "olcu_mae_sd": olcu_mae}


def mi_sentetik_tablo(R: pd.DataFrame, Yd: Dict[str, Any], esik: Dict[str, float], kok_ad: str, sd_ref: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    sat = []
    for (ad, ur, bg, gr), g in R.groupby(["sablon", "uretec", "baglam", "gurultu"]):
        th = esik[ad]; x = g.S_iyi.to_numpy(float)
        bb = mi_birebir(g, th, sd_ref[ad])
        ya = mi_yanlis_esik(Yd[ad][ur], th, int(MI_ESIK["sentetik"]["yanlis"]["tekil"]))
        sat.append({"kok": kok_ad, "sablon": ad, "uretec": ur, "baglam": bg, "gurultu": gr, "n": len(g), "esik": th,
                    "yakalama": float(np.mean(np.nan_to_num(x, nan=-1) >= th)), "S_iyi_med": float(np.nanmedian(x)),
                    "yanlis_tekil_1000": ya["tekil_1000"], "yanlis_ham_1000": ya["ham_1000"],
                    "birebir_n": bb.get("n", 0), "birebir_mae_sd": bb.get("mae_sd"), "birebir_r": bb.get("r_ort"),
                    "ayni_pencere_pay": bb.get("ayni_pencere_pay"), "son_ayni_pay": bb.get("son_ayni_pay")})
    return pd.DataFrame(sat)


def mi_sentetik(cikti: Optional[str] = None, havuz_yol: Optional[str] = None, tohum: Optional[int] = None) -> Dict[str, Any]:
    """Kalibrasyon + iki köklü sentetik test + eşik seçimi -> mum_izi_sentetik.json / _tablo.csv."""
    t0 = time.time(); cikti = cikti or MI_YOL["cikti"]
    hy = havuz_yol or os.path.join(MI_YOL["gecici"], MI_DOSYA["havuz"])
    if not os.path.exists(hy):
        raise MIHata(f"üretici havuzu yok: {hy} (önce 'acik')")
    havuz = pd.read_pickle(hy)
    sab = mi_sablon_yukle(cikti, kalibre=False)
    K = mi_kalibre(havuz, sab)
    for ad in sab:
        sab[ad]["tau"] = K[ad]["tau"]; sab[ad]["sd"] = K[ad]["sd"]
    milog.info("kalibrasyon: %s", {k: v["tau"] for k, v in K.items()})
    Sn = MI_ESIK["sentetik"]; out: Dict[str, Any] = {"surum": MI_SURUM, "zaman": _mi_simdi(), "esik_sha": mi_esik_sha(),
                                                      "havuz_sha": _mi_sha(hy), "havuz": {"hisse": len(havuz["sembol"]), "bar": havuz["bar"],
                                                                                         "aday": havuz["aday"], "donem": havuz["donem"]},
                                                      "kalibrasyon": K, "sablon_sha": _mi_sha(_mi_yol("sablon", cikti))}
    RA = mi_sentetik_kos(havuz, sab, Sn["kok"]["A"], tohum)
    esik = {ad: mi_esik_sec(RA, ad) for ad in sab}
    out["esik"] = esik
    th = {ad: esik[ad]["S"] for ad in sab}
    RB = mi_sentetik_kos(havuz, sab, Sn["kok"]["B"], tohum)
    YA = mi_yanlis_kos(havuz, sab, Sn["kok"]["A"]); YB = mi_yanlis_kos(havuz, sab, Sn["kok"]["B"])
    oz = [k for k, _, _ in MI_OZELLIK]
    sd_ref = {ad: {k: {"ort": float(np.nanmean(RA[RA.sablon == ad][f"fg_{k}"].to_numpy(float))),
                       "sd": float(np.nanstd(RA[RA.sablon == ad][f"fg_{k}"].to_numpy(float)))} for k in oz} for ad in sab}
    TA = mi_sentetik_tablo(RA, YA, th, "A", sd_ref); TB = mi_sentetik_tablo(RB, YB, th, "B", sd_ref)
    Tt = pd.concat([TA, TB], ignore_index=True)
    Tt.to_csv(_mi_yol("sentetik_tablo", cikti), index=False, float_format="%.4f")
    oz_tab: Dict[str, Any] = {}
    for kn, R, Yd in (("A", RA, YA), ("B", RB, YB)):
        oz_tab[kn] = {}
        for ad in sab:
            g = R[R.sablon == ad]
            oz_tab[kn][ad] = {"yakalama_gurultu": {f"{gr:.1f}": float((np.nan_to_num(g[g.gurultu == gr].S_iyi, nan=-1) >= th[ad]).mean())
                                                   for gr in Sn["gurultu"]},
                              "yakalama_baglam_g20": {bg: float((np.nan_to_num(g[(g.gurultu == 0.2) & (g.baglam == bg)].S_iyi, nan=-1) >= th[ad]).mean())
                                                      for bg in Sn["baglam"]},
                              "yanlis": {ur: {k: v for k, v in mi_yanlis_esik(Yd[ad][ur], th[ad], int(Sn["yanlis"]["tekil"])).items()}
                                         for ur in Sn["uretec"]},
                              "birebir_g20": mi_birebir(g[g.gurultu == 0.2], th[ad], sd_ref[ad]),
                              "birebir_hepsi": mi_birebir(g, th[ad], sd_ref[ad]),
                              "S_baska_max_med": float(np.nanmedian(g.S_baska_max)),
                              "olcek_yakalama_g20": {str(k): float(v) for k, v in g[g.gurultu == 0.2].groupby(
                                  pd.cut(g[g.gurultu == 0.2].olcek, [0.49, 0.8, 1.25, 2.01])).S_iyi.apply(
                                  lambda s, t=th[ad]: float((np.nan_to_num(s, nan=-1) >= t).mean())).items()},
                              "esneme_yakalama_g20": {str(k): float(v) for k, v in g[g.gurultu == 0.2].groupby(
                                  pd.cut(g[g.gurultu == 0.2].esneme, [0.79, 0.93, 1.07, 1.21])).S_iyi.apply(
                                  lambda s, t=th[ad]: float((np.nan_to_num(s, nan=-1) >= t).mean())).items()}}
    out["ozet"] = oz_tab
    out["yanlis_hist"] = {kn: {ad: {ur: Yd[ad][ur]["hist"] for ur in Sn["uretec"]} for ad in sab} for kn, Yd in (("A", YA), ("B", YB))}
    out["yanlis_n_pencere"] = {kn: {ad: {ur: Yd[ad][ur]["n_pencere"] for ur in Sn["uretec"]} for ad in sab} for kn, Yd in (("A", YA), ("B", YB))}
    out["sd_ref"] = sd_ref
    out["satir"] = {"A": int(len(RA)), "B": int(len(RB))}
    out["sure_sn"] = round(time.time() - t0)
    os.makedirs(MI_YOL["gecici"], exist_ok=True)
    pd.concat([RA.assign(kok="A"), RB.assign(kok="B")]).to_pickle(os.path.join(MI_YOL["gecici"], "sentetik_satir.pkl"))
    _mi_jyaz(_mi_yol("sentetik", cikti), out, "sentetik")
    milog.info("sentetik bitti: eşik %s (%.0f sn)", th, time.time() - t0)
    return out


# ================================================================ 4) AÇIK KOPYA (gerçek veri <= 2022-12-31) ve KAPILAR
def mi_kes_fiyat(V: Dict[str, pd.DataFrame], bas: Optional[str] = None, kesik: pd.Timestamp = MI_KESIK) -> Tuple[Dict[str, pd.DataFrame], Dict[str, int]]:
    out: Dict[str, pd.DataFrame] = {}; say = {"sembol": len(V), "bos": 0}
    b = pd.Timestamp(bas) if bas else None
    for s, d in V.items():
        ix = pd.DatetimeIndex(d.index)
        ix = ix.tz_convert(None) if ix.tz is not None else ix
        m = ix <= kesik
        if b is not None:
            m &= ix >= b
        x = d[m].copy(); x.index = ix[m].astype("datetime64[ns]")
        if not len(x):
            say["bos"] += 1; continue
        if x.index.max() > kesik:
            raise MIHata(f"{s}: kesik sonrası satır kaldı -> DURDU")
        out[str(s)] = x
    return out, say


def mi_acik(cikti: Optional[str] = None) -> Dict[str, Any]:
    """V_ABD2 / V_AVR2 (veri3, YALNIZ OKUNUR) ve V_BIST (/tmp/veri) -> /tmp/mum_izi/acik (veri_bas..2022-12-31) + üretici havuzu."""
    import KASA as KS
    cikti = cikti or MI_YOL["cikti"]; ac = MI_YOL["acik"]; os.makedirs(ac, exist_ok=True)
    J: Dict[str, Any] = {"zaman": _mi_simdi(), "kesik": str(MI_KESIK.date()), "veri_bas": MI_ESIK["gercek"]["veri_bas"]}
    for p, kay in (("ABD", os.path.join(MI_YOL["veri3"], "V_ABD2.pkl")), ("AVR", os.path.join(MI_YOL["veri3"], "V_AVR2.pkl")),
                   ("BIST", os.path.join(MI_YOL["veri"], "V_BIST.pkl"))):
        if not os.path.exists(kay):
            raise MIHata(f"veri yok: {kay}")
        V = pd.read_pickle(kay)
        if isinstance(V, dict) and "veri" in V and isinstance(V["veri"], dict):
            V = V["veri"]
        W, say = mi_kes_fiyat(V, MI_ESIK["gercek"]["veri_bas"])
        yol = os.path.join(ac, f"V_{p}.pkl"); pd.to_pickle(W, yol)
        J[p] = {"kaynak": kay, "kaynak_sha": _mi_sha(kay), "kaynak_sembol": len(V), "yazilan": len(W), **say, "sha": _mi_sha(yol),
                "ilk": str(min(d.index.min() for d in W.values()).date()) if W else None,
                "son": str(max(d.index.max() for d in W.values()).date()) if W else None,
                "yil_sembol": {str(y): int(sum(1 for d in W.values() if (d.index.year == y).any())) for y in range(2015, 2023)}}
        if p == "ABD":
            H = mi_havuz_yap(V)
            hy = os.path.join(MI_YOL["gecici"], MI_DOSYA["havuz"]); pd.to_pickle(H, hy)
            J["havuz"] = {"hisse": len(H["sembol"]), "aday": H["aday"], "bar": H["bar"], "sha": _mi_sha(hy), "donem": H["donem"]}
            del H
        del V, W; gc.collect()
        milog.info("açık kopya %s: %s", p, {k: J[p][k] for k in ("yazilan", "ilk", "son")})
    J["kasa"] = KS.kasa_kapisi([os.path.join(ac, f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")], str(MI_KESIK.date()))
    _mi_jyaz(_mi_yol("acik_json", cikti), J, "açık")
    return J


def mi_kasa_kapi(acik: Optional[str] = None) -> Dict[str, Any]:
    import KASA as KS
    ac = acik or MI_YOL["acik"]
    try:
        return KS.kasa_kapisi([os.path.join(ac, f"V_{p}.pkl") for p in ("ABD", "AVR", "BIST")], str(MI_KESIK.date()))
    except KS.KasaHata as ex:
        raise MIHata(f"KASA kapısı KAPALI: {ex}") from ex


def mi_sha_simdi(cikti: Optional[str] = None) -> Dict[str, str]:
    cikti = cikti or MI_YOL["cikti"]
    return {"KOD_SHA": _mi_sha(MI_YOL["kod"]), "ESIK_SHA": mi_esik_sha(), "SABLON_SHA": _mi_sha(_mi_yol("sablon", cikti)),
            "SENTETIK_SHA": _mi_sha(_mi_yol("sentetik", cikti))}


def mi_kapi(cikti: Optional[str] = None) -> Dict[str, Any]:
    """Ölçüm kapısı: IZ_KARNE kontrol kapısı + ön kayıttaki sha'lar = şimdiki + ön kayıt commit'li ve çalışma ağacında değişmemiş."""
    import IZ_KARNE as IK
    cikti = cikti or MI_YOL["cikti"]; yol = _mi_yol("onkayit", cikti)
    try:
        k = IK.ik_kontrol_kapisi(yol)
    except RuntimeError as ex:
        raise MIHata(str(ex)) from ex
    metin = open(yol, encoding="utf-8").read()
    bek = mi_sha_simdi(cikti)
    for ad, v in bek.items():
        if f"{ad}: {v}" not in metin:
            raise MIHata(f"ön kayıt kapısı: {ad} ön kayıtta yok ya da farklı (şimdiki {v[:12]}) -> DURDU")
    rel = os.path.relpath(yol, KOK_MI)
    c = _mi_git(["log", "-1", "--format=%H %cI", "--", rel])
    if not c:
        raise MIHata("ön kayıt commit'li değil -> DURDU")
    if _mi_git(["status", "--porcelain", "--", rel, os.path.relpath(MI_YOL["kod"], KOK_MI), os.path.relpath(_mi_yol("sentetik", cikti), KOK_MI),
                os.path.relpath(_mi_yol("sablon", cikti), KOK_MI)]):
        raise MIHata("ön kayıt / kod / sentetik / şablon çalışma ağacında değişmiş -> DURDU")
    return {"kontrol": {"gecti": k["gecti"]}, "onkayit_commit": c, **bek}


# ================================================================ 5) GERÇEK VERİ (E)
def mi_konum_seri(C: np.ndarray, e: np.ndarray) -> np.ndarray:
    """TEPE / DIP / ORTA / KISA (MI_ESIK['gercek']['konum_tanim'])."""
    G = MI_ESIK["gercek"]; n = int(G["konum_bar"]); q = float(G["konum_pay"]); out = np.full(len(e), "KISA", dtype=object)
    for i, t in enumerate(e):
        if t + 1 < n:
            continue
        w = C[t - n + 1:t + 1]
        if C[t] >= (1 - q) * w.max():
            out[i] = "TEPE"
        elif C[t] <= (1 + q) * w.min():
            out[i] = "DIP"
        else:
            out[i] = "ORTA"
    return out


def mi_tara_hisse(d: pd.DataFrame, sab: Dict[str, Dict[str, Any]], bas: pd.Timestamp, son: pd.Timestamp) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Bir hissenin geçerli barları: şablon başına S(t), eşik, 15 bar tekil olaylar (tarama aralığındaki t), S dağılımı."""
    O, H, L, C = (d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")); ix = d.index
    ara = (ix >= bas) & (ix <= son); ol = []; ist: Dict[str, Any] = {}
    tek = int(MI_ESIK["gercek"]["tekil"])
    for ad, s in sab.items():
        best, bm = mi_tara_seri(O, H, L, C, s)
        f = ara & np.isfinite(best)
        ist[ad] = {"n": int(f.sum()), "hist": np.histogram(best[f], np.linspace(0, 1, 101))[0]}
        e = np.flatnonzero(f & (np.nan_to_num(best, nan=-1) >= s["esik"]))
        ist[ad]["ham"] = int(len(e))
        if not len(e):
            continue
        e = _mi_tekil(e, tek)
        kon = mi_konum_seri(C, e)
        for t, k in zip(e, kon):
            m = int(bm[t]); a = t - m + 1
            ol.append({"sablon": ad, "tarih": ix[t], "S": float(best[t]), "m": m, "pencere_bas": ix[a], "pencere_min_low": float(L[a:t + 1].min()),
                       "C_t": float(C[t]), "konum": k, "bar_no": int(t)})
    return ol, ist


_MI_ISCI: Dict[str, Any] = {}


def _mi_isci_tara(sembol: str) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    o, i = mi_tara_hisse(_MI_ISCI["V"][sembol], _MI_ISCI["sab"], _MI_ISCI["bas"], _MI_ISCI["son"])
    return sembol, o, i


def mi_tara_pazar(Vd: Dict[str, Any], sab: Dict[str, Dict[str, Any]], pazar: str, islem: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Pazarın bütün hisseleri (sıralı); islem > 1 ise fork süreç havuzu (sonuç sıralı ve sıralı koşuyla aynı)."""
    import multiprocessing as mp
    G = MI_ESIK["gercek"]; bas, son = pd.Timestamp(G["tarama"][0]), pd.Timestamp(G["tarama"][1])
    ist = {ad: {"n": 0, "ham": 0, "hist": np.zeros(100, np.int64), "hisse": 0} for ad in sab}
    t0 = time.time(); semb = []
    for s_, d in sorted(Vd["V"].items()):
        if d.index.max() > MI_KESIK:
            raise MIHata(f"{pazar} {s_}: KESİK AŞIMI {d.index.max().date()}")
        if len(d) >= 40:
            semb.append(s_)
    islem = int(islem or os.environ.get("MI_ISLEM", 3))
    _MI_ISCI.clear(); _MI_ISCI.update({"V": Vd["V"], "sab": sab, "bas": bas, "son": son})
    sonuc = []
    try:
        if islem > 1 and "fork" in mp.get_all_start_methods():
            with mp.get_context("fork").Pool(islem) as pool:
                for k, r in enumerate(pool.imap(_mi_isci_tara, semb, chunksize=16)):
                    sonuc.append(r)
                    if k % 500 == 0:
                        milog.info("%s tarama %d / %d hisse (%.0f sn)", pazar, k, len(semb), time.time() - t0)
        else:
            for k, s_ in enumerate(semb):
                sonuc.append(_mi_isci_tara(s_))
                if k % 500 == 0:
                    milog.info("%s tarama %d / %d hisse (%.0f sn)", pazar, k, len(semb), time.time() - t0)
    finally:
        _MI_ISCI.clear()
    ol = []
    for s_, o, i in sonuc:
        for r in o:
            r["sembol"] = s_
        ol.extend(o)
        for ad in sab:
            ist[ad]["n"] += i[ad]["n"]; ist[ad]["ham"] += i[ad]["ham"]; ist[ad]["hist"] += i[ad]["hist"]; ist[ad]["hisse"] += int(i[ad]["n"] > 0)
    X = pd.DataFrame(ol)
    if len(X):
        X["pazar"] = pazar
    for ad in sab:
        ist[ad]["tekil"] = int((X.sablon == ad).sum()) if len(X) else 0
        ist[ad]["hisse_yil"] = ist[ad]["n"] / 252.0
        ist[ad]["tekil_1000"] = 1000.0 * ist[ad]["tekil"] / max(ist[ad]["n"], 1)
        ist[ad]["tekil_hisse_yil"] = ist[ad]["tekil"] / max(ist[ad]["hisse_yil"], 1e-9)
        ist[ad]["ham_1000"] = 1000.0 * ist[ad]["ham"] / max(ist[ad]["n"], 1)
        ist[ad]["hist"] = ist[ad]["hist"].tolist()
    milog.info("%s tarama bitti: %d hisse, olay %d (%.0f sn)", pazar, len(semb), len(X), time.time() - t0)
    return X, ist


def mi_prefix(Vd: Dict[str, Any], X: pd.DataFrame, sab: Dict[str, Dict[str, Any]], n: Optional[int] = None) -> Dict[str, Any]:
    """K2: rastgele olaylarda hisse verisi t'de kesilince S(t) aynı (|fark| < 1e-12) olmalı; tutmazsa DURUR."""
    G = MI_ESIK["gercek"]; n = int(n or G["prefix_n"])
    if not len(X):
        return {"n": 0, "tuttu": True}
    rng = np.random.default_rng(G["prefix_kok"]); sec = X.iloc[rng.choice(len(X), size=min(n, len(X)), replace=False)]
    fark = []
    for r in sec.itertuples():
        d = Vd["V"][r.sembol]; dk = d[d.index <= r.tarih]
        b, _ = mi_tara_seri(*(dk[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), sab[r.sablon])
        fark.append(abs(float(b[-1]) - float(r.S)))
    mx = float(max(fark))
    if not mx < 1e-12:
        raise MIHata(f"PREFIX TUTMADI: en büyük |fark| {mx}")
    return {"n": len(fark), "en_buyuk_fark": mx, "tuttu": True}


def mi_duz_S(O: np.ndarray, H: np.ndarray, L: np.ndarray, C: np.ndarray, t: int, m: int, s: Dict[str, Any]) -> float:
    """K11: tek pencerede S düz döngüyle (vektörsüz yeniden yazım; mi_ozellik / mi_dizi / mi_bant kullanılmaz)."""
    nb = int(MI_ESIK["benzerlik"]["bant"]["n"]); kk = float(MI_ESIK["benzerlik"]["bant"]["k"])
    a = t - m + 1
    bu, bo, ba = [], [], []
    for i in range(a, t + 1):
        w = [float(C[j]) for j in range(i - nb + 1, i + 1)]; mu = sum(w) / nb; sd = math.sqrt(sum((x - mu) ** 2 for x in w) / nb)
        bu.append(mu + kk * sd); bo.append(mu); ba.append(mu - kk * sd)
    o = [float(x) for x in O[a:t + 1]]; h = [float(x) for x in H[a:t + 1]]; l_ = [float(x) for x in L[a:t + 1]]; c = [float(x) for x in C[a:t + 1]]
    rg = [max(h[i] - l_[i], 1e-12) for i in range(m)]; u = sum(rg) / m
    up = [max(h[i] - max(o[i], c[i]), 0.0) for i in range(m)]; lw = [max(min(o[i], c[i]) - l_[i], 0.0) for i in range(m)]
    pb = [(c[i] - ba[i]) / (bu[i] - ba[i]) if bu[i] - ba[i] > 0 else 0.5 for i in range(m)]

    def egim(y: List[float]) -> Tuple[float, float]:
        xm = (m - 1) / 2; ym = sum(y) / m; sxy = sum((i - xm) * (y[i] - ym) for i in range(m)); sxx = sum((i - xm) ** 2 for i in range(m))
        syy = sum((v - ym) ** 2 for v in y); b = sxy / sxx
        return b, (min(max(b * b * sxx / syy, 0.0), 1.0) if syy > 0 else 0.0)
    F = {"ust_fitil": sum(up[i] / rg[i] for i in range(m)) / m, "alt_fitil": sum(lw[i] / rg[i] for i in range(m)) / m,
         "ust_alt_log": math.log((sum(up) + 0.05 * m * u) / (sum(lw) + 0.05 * m * u)),
         "govde_oran": sum(abs(c[i] - o[i]) / rg[i] for i in range(m)) / m, "kucuk_mum_pay": sum(1 for x in rg if x <= 0.7 * u) / m,
         "yuk_dip_pay": sum(1 for i in range(1, m) if l_[i] > l_[i - 1]) / (m - 1)}
    F["kapanis_egim"], F["kapanis_r2"] = egim([x / u for x in c])
    k3 = min(3, m)
    F["pB_bas"] = sum(pb[:k3]) / k3; F["pB_son"] = sum(pb[-k3:]) / k3
    F["sma_ustu_pay"] = sum(1 for i in range(m) if c[i] > bo[i]) / m
    g = [(bu[i] - ba[i]) / u for i in range(m)]
    F["bant_gen_oran_log"] = math.log(max(sum(g[-k3:]) / k3, 1e-6) / max(sum(g[:k3]) / k3, 1e-6))
    ref = sum((h[i] + l_[i]) / 2 for i in range(m)) / m
    z = [[(v - ref) / u for v in (o[i], h[i], l_[i], c[i])] for i in range(m)]
    L_ = s["L"]
    if m != L_:
        zz, pp = [], []
        for k in range(L_):
            q = k * (m - 1) / (L_ - 1); i0 = min(int(math.floor(q)), m - 2); w = q - i0
            zz.append([z[i0][f] * (1 - w) + z[i0 + 1][f] * w for f in range(4)]); pp.append(pb[i0] * (1 - w) + pb[i0 + 1] * w)
        z, pb = zz, pp
    D1 = math.sqrt(sum((z[k][f] - s["Z"][k][f]) ** 2 for k in range(L_) for f in range(4)) / (4 * L_))
    D2 = math.sqrt(sum((pb[k] - s["pB"][k]) ** 2 for k in range(L_)) / L_)
    alt = MI_ESIK["benzerlik"]["ozellik_alt"]
    D3 = math.sqrt(sum(((F[k] - s["F"][k]) / s["sd"][k]) ** 2 for k in alt) / len(alt))
    return math.exp(-(D1 / s["tau"][0] + D2 / s["tau"][1] + D3 / s["tau"][2]) / 3.0)


def mi_duz_dogrula(Vd: Dict[str, Any], X: pd.DataFrame, sab: Dict[str, Dict[str, Any]], n: Optional[int] = None) -> Dict[str, Any]:
    n = int(n or MI_ESIK["gercek"]["duz_n"])
    if not len(X):
        return {"n": 0, "tuttu": True}
    rng = np.random.default_rng(2516); sec = X.iloc[rng.choice(len(X), size=min(n, len(X)), replace=False)]
    fk = []
    for r in sec.itertuples():
        d = Vd["V"][r.sembol]; t = int(d.index.get_loc(r.tarih))
        v = mi_duz_S(*(d[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")), t, int(r.m), sab[r.sablon])
        fk.append(abs(v - float(r.S)))
    mx = float(max(fk))
    return {"n": len(fk), "en_buyuk_fark": mx, "tuttu": bool(mx < 1e-9)}


def _mi_es_uyeleri(Pn: Dict[str, Any], d: np.ndarray, j: np.ndarray, exd: np.ndarray, exj: np.ndarray, k: int, kok: int) -> List[np.ndarray]:
    """Her olay için aynı (gün, kova) havuzundan (olaylar hariç) en çok k rastgele üye (havuz konumları)."""
    import CETVEL2 as C2
    K = C2.C2_KOVA_SAYI; hk = Pn["h_key"]
    ex = np.zeros(len(hk), bool); pp = Pn["h_pix"][exd, exj]; ex[pp[pp >= 0]] = True
    kv = Pn["KV"][d, j].astype(np.int64); key = d * K + kv
    lo = np.searchsorted(hk, key, "left"); hi = np.searchsorted(hk, key, "right")
    out = []
    for i, (a, b, kk) in enumerate(zip(lo, hi, kv)):
        if kk < 0:
            out.append(np.zeros(0, np.int64)); continue
        r = np.arange(a, b, dtype=np.int64); r = r[~ex[r]]
        rng = np.random.default_rng([kok, i])
        out.append(r if len(r) <= k else rng.choice(r, size=k, replace=False))
    return out


def mi_h5_es(Pn: Dict[str, Any], X: pd.DataFrame, exd: np.ndarray, exj: np.ndarray) -> np.ndarray:
    """Olay başına eş +%5 payı: aynı gün aynı kovadan 20 rastgele üye; stop = üyenin giriş öncesi son m geçerli barının en düşük Low x 0,98
    (olayla aynı geometri); YH.yh_sim c2_bilgi üzerinden."""
    import CETVEL2 as C2
    G = MI_ESIK["gercek"]; P = Pn["P"]; Vd = Pn["Vd"]
    d = X.d.to_numpy(np.int64); j = X.j.to_numpy(np.int64); m = X.m.to_numpy(np.int64)
    U = _mi_es_uyeleri(Pn, d, j, exd, exj, int(G["h5_es_sayi"]), int(G["h5_es_kok"]))
    oi, od, oj, om = [], [], [], []
    for i, u in enumerate(U):
        if not len(u):
            continue
        oi.append(np.full(len(u), i)); od.append(Pn["h_d"][u]); oj.append(Pn["h_j"][u]); om.append(np.full(len(u), m[i]))
    out = np.full(len(X), np.nan)
    if not oi:
        return out
    oi, od, oj, om = (np.concatenate(v) for v in (oi, od, oj, om))
    S = np.asarray(P["sembol"]); tarih = P["tarih"]
    hat = np.full(len(oi), np.nan)
    for jj in np.unique(oj):
        s = S[jj]; dd = Vd["V"][s]; ix = dd.index; Lw = dd.Low.to_numpy(float)
        sel = np.flatnonzero(oj == jj)
        g = tarih[od[sel]]
        k = ix.searchsorted(g, side="left") - 1      # giriş gününden önceki son geçerli bar (t)
        for q, (kk, mm) in enumerate(zip(k, om[sel])):
            if kk - mm + 1 >= 0:
                hat[sel[q]] = float(Lw[kk - mm + 1:kk + 1].min())
    Xu = pd.DataFrame({"sembol": S[oj], "tarih": tarih[od], "giris": tarih[od], "d": od, "j": oj, "hat": hat,
                       "atr": Pn["ATR"][od, oj]})
    B = C2.c2_bilgi(Pn, Xu)
    h = B.h5.to_numpy(float)
    df = pd.DataFrame({"i": oi, "h": h}).dropna()
    if len(df):
        ag = df.groupby("i").h.mean()
        out[ag.index.to_numpy(int)] = ag.to_numpy(float)
    return out


def mi_hucre(X: pd.DataFrame, maske: np.ndarray, hc: str, pazar: str, tohum_ek: int) -> Dict[str, Any]:
    import CETVEL2 as C2
    mm = maske & (X.donem.to_numpy() == hc) & np.isfinite(X.fark.to_numpy(float))
    x = X[mm]; out: Dict[str, Any] = {"n": int(mm.sum())}
    if len(x) < 2:
        out.update({"hukum": "ÖLÇÜLEMEDİ", "fark": float(x.fark.mean()) if len(x) else np.nan})
        return out
    eg = C2._c2_egri22_al(pazar, hc, int(MI_ESIK["gercek"]["ufuk"]), None)
    c = C2.c2_hucre(x.r15.to_numpy(float), x.es_r15.to_numpy(float), x.sira.to_numpy(float), x.giris.to_numpy(), MI_ESIK["gercek"]["yon"],
                    tohum_ek=tohum_ek, egri=eg)
    yon = "+" if c.get("tutar_p") else ("-" if c.get("tutar_n") else "")
    out.update({k: c.get(k) for k in ("fark", "med", "boot_alt", "boot_ust", "sira", "l3o", "l3o_neg", "p", "guc", "r15_ort", "es_ort",
                                      "tutar_p", "tutar_n", "yakala_p", "yakala_n")})
    out["hukum"] = f"TUTAR ({yon})" if yon else ("TUTMADI" if (out["n"] >= 30 and np.isfinite(c.get("guc", np.nan)) and c["guc"] >= 0.8) else "ÖLÇÜLEMEDİ")
    out["yon"] = yon
    h5 = x.h5.to_numpy(float); h5e = x.h5_es.to_numpy(float); ok = np.isfinite(h5) & np.isfinite(h5e)
    out["h5_n"] = int(ok.sum()); out["h5"] = float(h5[ok].mean()) if ok.any() else np.nan; out["h5_es"] = float(h5e[ok].mean()) if ok.any() else np.nan
    out["h5_fark"] = out["h5"] - out["h5_es"] if ok.any() else np.nan
    out["S_med"] = float(x.S.median())
    out["konum"] = {k: int(v) for k, v in x.konum.value_counts().items()}
    return out


def mi_sonrasi(X: pd.DataFrame, Vd_os: Dict[str, Any], pazar: str, sab: Dict[str, Dict[str, Any]], acik: str, plasebo: bool = True,
               tohum_sayi: Optional[int] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Olaylar -> (karar pazarı) P2 süzgeci -> C2 v2.2 olay / eş / hücre / plasebo + h5 (pencere stop) + eş h5."""
    import CETVEL2 as C2
    G = MI_ESIK["gercek"]; info: Dict[str, Any] = {"girdi": int(len(X))}
    if not len(X):
        return X, info
    Z = X.copy()
    if pazar in G["pazar_karar"]:
        import KART_TUR2 as KT2
        Pk, P2 = KT2.k2_panel(Vd_os, pazar); P = KT2.k2_P(Pk, Vd_os, P2)
        parca = []
        for ad in sab:
            Y = Z[Z.sablon == ad]
            Zp, sp = KT2._k2_oc(Y[["sembol", "tarih"]], P, 1)
            k = set(zip(Zp.sembol, pd.to_datetime(Zp.tarih)))
            parca.append(Y.assign(p2=[(s, pd.Timestamp(t)) in k for s, t in zip(Y.sembol, Y.tarih)]))
            info[f"p2_{ad}"] = sp
        Z = pd.concat(parca, ignore_index=True)
        del Pk, P2, P; gc.collect()
    else:
        Z["p2"] = True
    info["p2_tablo"] = Z[["sembol", "tarih", "sablon", "p2"]].copy()
    Pn = C2.c2_panel22_al(pazar, acik, int(G["ufuk"]))
    out = []; H: Dict[str, Any] = {}
    for si, ad in enumerate(sab):
        Y = Z[(Z.sablon == ad) & Z.p2.astype(bool)]
        kol = ["sembol", "tarih", "S", "m", "pencere_bas", "pencere_min_low", "C_t", "konum", "bar_no"]
        S, say = C2.c2_olay(Y[kol], Pn, int(G["tekil"]))
        info[f"c2_{ad}"] = say
        if not len(S):
            continue
        d = S.d.to_numpy(np.int64); j = S.j.to_numpy(np.int64)
        e = C2.c2_es(Pn, d, j, S.r15.to_numpy(float), d, j, es_min=int(G["es_min"]))
        S["es_r15"] = e["es_r15"]; S["n_es"] = e["n_es"]; S["sira"] = e["sira"]; S["fark"] = e["fark"]
        S["donem"] = C2._c2_donem22(S.giris, G["donem"])
        B = C2.c2_bilgi(Pn, S.assign(hat=S.pencere_min_low.to_numpy(float)))
        S["h5"] = B.h5.to_numpy(float); S["st5"] = B.st5.to_numpy(float); S["h10"] = B.h10.to_numpy(float)
        S["h5_es"] = mi_h5_es(Pn, S, d, j)
        S["sablon"] = ad; S["pazar"] = pazar
        out.append(S)
        grup = {"hepsi": np.ones(len(S), bool), "tepe": S.konum.to_numpy() == "TEPE",
                "baska": np.isin(S.konum.to_numpy(), ["DIP", "ORTA"]), "dip": S.konum.to_numpy() == "DIP"}
        for gi, (g, mk) in enumerate(grup.items()):
            for hi, hc in enumerate(list(G["donem"]) + ["hepsi"]):
                if hc == "hepsi":
                    continue
                c = mi_hucre(S, mk, hc, pazar, 600000 + si * 1000 + gi * 10 + hi)
                if plasebo and g == "hepsi" and pazar in G["pazar_karar"] and c["n"] >= 2:
                    mmk = mk & (S.donem.to_numpy() == hc) & np.isfinite(S.fark.to_numpy(float))
                    eg = C2._c2_egri22_al(pazar, hc, int(G["ufuk"]), None)
                    pl = C2.c2_plasebo(Pn, S.d.to_numpy(np.int64)[mmk], G["yon"], eg, tohum_ek=700 + si * 10 + hi, iki_yon_ayri=True,
                                       tohum_sayi=tohum_sayi or int(G["plasebo_tohum"]))
                    c["plasebo"] = {k: pl[k] for k in ("fark_ort", "fark_sd", "tutar_pay", "tutar_pay_arti", "tutar_pay_eksi", "gecti_arti",
                                                       "gecti_eksi", "gecti", "n_ort", "yakala_pay")}
                H[f"{pazar}|{ad}|{g}|{hc}"] = c
        milog.info("%s %s: c2 olay %d, ölçülen %d", pazar, ad, len(S), int(np.isfinite(S.fark).sum()))
    info["hucre"] = H
    A = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    del Pn; C2._C2_PN22.clear(); gc.collect()
    return A, info


def mi_etiket(H: Dict[str, Any], ad: str) -> Dict[str, Any]:
    """Ön kayıtlı bilgi etiketi (MI_ESIK['karar_kurali'])."""
    kh = [(p, hc) for p in MI_ESIK["gercek"]["pazar_karar"] for hc in MI_ESIK["gercek"]["donem"]]
    C = {f"{p}|{hc}": H.get(f"{p}|{ad}|hepsi|{hc}", {"n": 0}) for p, hc in kh}
    yon = {k: (c.get("yon") or "") for k, c in C.items()}
    pl = {k: (c.get("plasebo") or {}) for k, c in C.items()}
    tut = {k: bool(yon[k]) and bool(pl[k].get("gecti_arti" if yon[k] == "+" else "gecti_eksi")) for k in C}
    guclu = {k: bool(c.get("n", 0) >= 30 and c.get("guc") is not None and np.isfinite(c.get("guc", np.nan)) and c["guc"] >= 0.8) for k, c in C.items()}
    ayni = len({yon[k] for k in C}) == 1
    if all(tut.values()) and ayni:
        e = "BİRLEŞİK İZ BİLEŞENİ ADAYI"
    elif all(guclu.values()):
        e = "İZ DEĞİL"
    elif any(bool(yon[k]) for k in C):
        e = "EMARE"
    else:
        e = "ÖLÇÜLEMEDİ"
    return {"etiket": e, "c2_yon": yon, "tutar_plasebo": tut, "guclu": guclu}


def mi_yeniden(cikti: Optional[str] = None) -> Dict[str, Any]:
    """K11: 2 hücre (ABD d1619, AVR d2022; tam iz, hepsi) olay satır dosyasından düz pandas: n / ort FARK / +%5 payı -> sonuç json'la."""
    cikti = cikti or MI_YOL["cikti"]
    O = pd.read_csv(_mi_yol("olay", cikti)); J = json.load(open(_mi_yol("sonuc", cikti), encoding="utf-8"))
    out = {}
    for p, hc in (("ABD", "d1619"), ("AVR", "d2022")):
        x = O[(O.pazar == p) & (O.sablon == "tam") & (O.donem == hc)]
        x = x[x.fark.notna()]
        h = x[x.h5.notna() & x.h5_es.notna()]
        a = {"n": int(len(x)), "fark": float(x.fark.mean()) if len(x) else None, "h5": float(h.h5.mean()) if len(h) else None}
        b = J["hucre"].get(f"{p}|tam|hepsi|{hc}", {})
        ok = a["n"] == b.get("n") and (a["fark"] is None or abs(a["fark"] - b.get("fark", np.nan)) < 1e-9) and \
            (a["h5"] is None or abs(a["h5"] - b.get("h5", np.nan)) < 1e-9)
        out[f"{p}|{hc}"] = {"duz": a, "json": {"n": b.get("n"), "fark": b.get("fark"), "h5": b.get("h5")}, "tuttu": bool(ok)}
    out["tuttu"] = all(v["tuttu"] for v in out.values() if isinstance(v, dict))
    return out


def mi_veri(pazar: str, acik: str) -> Dict[str, Any]:
    """ABD / AVR: OS.os_veri (TEZGAH2 / KART_TUR2 ile aynı yükleyici); BIST: C2.c2_veri (DS.ds_veri; OS BIST'i tanımıyor)."""
    import OLCU_SINAMA as OS
    if pazar in OS.OS_ESIK["veri"]["pazar"]:
        return OS.os_veri(pazar, acik)
    import CETVEL2 as C2
    return C2.c2_veri(pazar, acik)


def mi_kos(acik: Optional[str] = None, cikti: Optional[str] = None, kuru: bool = False, pazarlar: Optional[List[str]] = None,
           plasebo_tohum: Optional[int] = None, ayar: Optional[str] = None) -> Dict[str, Any]:
    """Kapı -> tarama (ABD, AVR, BIST) -> prefix / düz S doğrulaması -> sonrası (bilgi) -> olay satırları + sonuç json."""
    import OLCU_SINAMA as OS
    t0 = time.time(); bas = _mi_simdi(); acik = acik or MI_YOL["acik"]; cikti = cikti or MI_YOL["cikti"]
    if os.path.exists(_mi_yol("sonuc", cikti)) and not kuru:
        raise MIHata("sonuç zaten var (ikinci koşu DURUR)")
    G0 = {"kuru": True} if kuru else mi_kapi(cikti)
    kasa = mi_kasa_kapi(acik) if not kuru else {"kuru": True}
    ayar = ayar or (MI_YOL["cikti"] if kuru else cikti)          # şablon + sentetik json klasörü (kuru koşuda deneme ayarı olabilir)
    sab = mi_sablon_yukle(ayar)
    SJ = json.load(open(_mi_yol("sentetik", ayar), encoding="utf-8"))
    J: Dict[str, Any] = {"surum": MI_SURUM, "baslangic": bas, "kapi": G0, "kasa": kasa, "esik": {ad: s["esik"] for ad, s in sab.items()},
                         "tarama": {}, "prefix": {}, "duz": {}, "sonrasi_info": {}, "hucre": {}}
    olay = []
    for pazar in (pazarlar or MI_ESIK["gercek"]["pazar_karar"] + MI_ESIK["gercek"]["pazar_bilgi"]):
        Vd = mi_veri(pazar, acik)
        en_gec = max(d.index.max() for d in Vd["V"].values())
        if en_gec > MI_KESIK:
            raise MIHata(f"{pazar}: KESİK AŞIMI {en_gec.date()}")
        X, ist = mi_tara_pazar(Vd, sab, pazar)
        J["tarama"][pazar] = {**ist, "hisse": len(Vd["V"]), "en_gec": str(en_gec.date())}
        J["prefix"][pazar] = mi_prefix(Vd, X, sab)
        J["duz"][pazar] = mi_duz_dogrula(Vd, X, sab)
        if not J["duz"][pazar]["tuttu"]:
            raise MIHata(f"{pazar}: düz S yeniden üretimi TUTMADI {J['duz'][pazar]}")
        A, info = mi_sonrasi(X, Vd, pazar, sab, acik, plasebo=True, tohum_sayi=plasebo_tohum)
        J["hucre"].update(info.pop("hucre", {})); p2t = info.pop("p2_tablo", None); J["sonrasi_info"][pazar] = info
        # P2 / C2 dışında kalan olaylar da satır dosyasında (konum ve benzerlik için); ölçüm sütunları yalnız havuzdakilerde
        if len(X):
            X2 = X.copy(); X2["tarih"] = pd.to_datetime(X2.tarih)
            if len(A):
                A2 = A.copy(); A2["tarih"] = pd.to_datetime(A2.tarih)
                ek = [c for c in A2.columns if c not in X2.columns or c in ("sembol", "tarih", "sablon")]
                X2 = X2.merge(A2[ek], on=["sembol", "tarih", "sablon"], how="left", validate="one_to_one")
            if p2t is not None and len(p2t):
                p2t = p2t.assign(tarih=pd.to_datetime(p2t.tarih))
                X2 = X2.merge(p2t, on=["sembol", "tarih", "sablon"], how="left", validate="one_to_one")
            X2["olculdu"] = X2["fark"].notna() if "fark" in X2.columns else False
            olay.append(X2)
        del Vd, X, A; gc.collect()
        milog.info("%s bitti (%.0f sn)", pazar, time.time() - t0)
    O = pd.concat(olay, ignore_index=True) if olay else pd.DataFrame()
    for c in ("tarih", "pencere_bas", "giris"):
        if c in O.columns:
            O[c] = pd.to_datetime(O[c]).dt.strftime("%Y-%m-%d")
    if len(O):
        eg = max(pd.to_datetime(O.tarih).max(), pd.to_datetime(O.giris.dropna()).max() if "giris" in O.columns and O.giris.notna().any() else pd.Timestamp("1900-01-01"))
        if eg > MI_KESIK:
            raise MIHata(f"KESİK AŞIMI: olay {eg}")
        J["en_gec"] = str(eg.date())
    kol = ["pazar", "sablon", "sembol", "tarih", "S", "m", "pencere_bas", "pencere_min_low", "C_t", "konum", "p2", "olculdu", "giris", "donem",
           "kova", "r15", "es_r15", "n_es", "sira", "fark", "h5", "st5", "h10", "h5_es"]
    O = O[[c for c in kol if c in O.columns]]
    ys = _mi_yol("olay", cikti)
    O.to_csv(ys, index=False, compression={"method": "gzip", "mtime": 0}, float_format="%.10g")
    J["satir_sha"] = _mi_sha(ys); J["olay_n"] = int(len(O))
    J["etiket"] = {ad: mi_etiket(J["hucre"], ad) for ad in sab}
    # benzerlik: gerçek / sentetik rastgele (aynı eşik, tekil 1000 bar başına)
    J["benzerlik"] = {}
    for ad in sab:
        sy = SJ["ozet"]["A"][ad]["yanlis"]
        J["benzerlik"][ad] = {p: {"gercek_tekil_1000": J["tarama"][p][ad]["tekil_1000"], "gercek_tekil_hisse_yil": J["tarama"][p][ad]["tekil_hisse_yil"],
                                  "sentetik_blok_tekil_1000": sy["blok"]["tekil_1000"], "sentetik_ry_tekil_1000": sy["ry"]["tekil_1000"],
                                  "oran_blok": J["tarama"][p][ad]["tekil_1000"] / sy["blok"]["tekil_1000"] if sy["blok"]["tekil_1000"] > 0 else None,
                                  "oran_ry": J["tarama"][p][ad]["tekil_1000"] / sy["ry"]["tekil_1000"] if sy["ry"]["tekil_1000"] > 0 else None}
                              for p in J["tarama"]}
    # konum payları (bütün tekil olaylar, P2 / C2 süzgeci öncesi)
    J["konum"] = {}
    for (p, ad), g in O.groupby(["pazar", "sablon"]) if len(O) else []:
        vc = g.konum.value_counts(); n = int(len(g))
        J["konum"][f"{p}|{ad}"] = {"n": n, **{k: int(vc.get(k, 0)) for k in ("TEPE", "DIP", "ORTA", "KISA")},
                                   "tepe_pay": float(vc.get("TEPE", 0) / n), "baska_pay": float((vc.get("DIP", 0) + vc.get("ORTA", 0)) / n)}
    J["bitis"] = _mi_simdi(); J["sure_sn"] = round(time.time() - t0)
    _mi_jyaz(_mi_yol("sonuc", cikti), J, "sonuç")
    if not kuru:
        J["yeniden"] = mi_yeniden(cikti)
        _mi_jyaz(_mi_yol("sonuc", cikti), J, "sonuç")
    milog.info("kos bitti: etiket %s (%.0f sn)", {k: v["etiket"] for k, v in J["etiket"].items()}, time.time() - t0)
    return J


# ================================================================ 6) KURU KOŞU (sentetik panel; kapı yok)
def mi_kuru_veri(klasor: str, n_hisse: int = 80, tohum: int = 2517, ayar: Optional[str] = None) -> str:
    """Sentetik ABD / AVR / BIST pkl'leri (2015-01-01..2022-12-30 iş günleri), içine şablon gömülmüş; yalnız kod hattı sınaması."""
    havuz = pd.read_pickle(os.path.join(MI_YOL["gecici"], MI_DOSYA["havuz"]))
    sab = mi_sablon_yukle(ayar or MI_YOL["cikti"], kalibre=True)
    gun = pd.bdate_range("2015-01-01", "2022-12-30"); n = len(gun)
    os.makedirs(klasor, exist_ok=True); rng = np.random.default_rng(tohum)
    for pz in ("ABD", "AVR", "BIST"):
        V = {}
        for k in range(n_hisse):
            lO, lH, lL, lC = mi_uret(rng, n, havuz, "blok")
            for q in range(4):
                p = int(rng.integers(300, n - 80))
                mi_baglam_uygula(lO, lH, lL, lC, p, ["dip", "yatay", "tepe"][q % 3])
                mi_gom(rng, lO, lH, lL, lC, p, sab["tam" if q % 2 == 0 else "tepesiz"], 0.1, 1.0, 1.0)
            sc = 50.0 / math.exp(lC[0])
            df = pd.DataFrame({"Open": np.exp(lO) * sc, "High": np.exp(lH) * sc, "Low": np.exp(lL) * sc, "Close": np.exp(lC) * sc,
                               "Volume": rng.uniform(2e5, 2e6, n)}, index=gun)
            if pz == "AVR":
                df["Kur"] = 1.0
            V[f"KURU{pz}{k:03d}"] = df
        pd.to_pickle(V, os.path.join(klasor, f"V_{pz}.pkl"))
    return klasor


# ================================================================ 7) ÖN KAYIT
def mi_kontrol_tablosu() -> str:
    s = ["| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |", "|---|---|---|---|"]
    try:
        import IZ_KARNE as IK
        ad = {k["kod"]: k.get("baslik", k.get("ad", k["kod"])) for k in IK.IK_KONTROL}
    except Exception:   # IZ_KARNE yoksa yalnız kodlar
        ad = {}
    for k, (y, kn) in MI_KONTROL.items():
        s.append(f"| {k} | {ad.get(k, k)} | {y} | {kn} |")
    return "\n".join(s)


def mi_onkayit_metni(cikti: Optional[str] = None) -> str:
    cikti = cikti or MI_YOL["cikti"]
    sh = mi_sha_simdi(cikti)
    SJ = json.load(open(_mi_yol("sentetik", cikti), encoding="utf-8"))
    AJ = json.load(open(_mi_yol("acik_json", cikti), encoding="utf-8"))
    BJ = json.load(open(_mi_yol("sablon", cikti), encoding="utf-8"))
    kc = _mi_git(["log", "-1", "--format=%H %cI", "--", os.path.relpath(MI_YOL["kod"], KOK_MI)])
    s = [f"# MUM_IZI ÖN KAYIT ({_mi_simdi()})", "",
         "Gerçek veri taraması (E) bu dosya commit edildikten SONRA koşar; `mi_kapi` bu dosyadaki sha'ları, kontrol tablosunu ve git kaydını denetler.",
         "Bu ana kadar gerçek veride (2016-22 ABD / AVR / BIST) hiçbir pencere puanlanmadı; sentetik üretici yalnız ABD 2005-2014 barlarını kullandı.", "",
         "## Mühürler", "",
         f"KOD_SHA: {sh['KOD_SHA']}", f"ESIK_SHA: {sh['ESIK_SHA']}", f"SABLON_SHA: {sh['SABLON_SHA']}", f"SENTETIK_SHA: {sh['SENTETIK_SHA']}", "",
         f"- Kod commit'i: {kc or 'yok'}",
         f"- Görüntü sha: {BJ['goruntu_sha']}",
         f"- Açık kopya: ABD {AJ['ABD']['sha'][:16]} ({AJ['ABD']['yazilan']} hisse, {AJ['ABD']['ilk']}..{AJ['ABD']['son']}), AVR {AJ['AVR']['sha'][:16]} "
         f"({AJ['AVR']['yazilan']}, {AJ['AVR']['ilk']}..{AJ['AVR']['son']}), BIST {AJ['BIST']['sha'][:16]} ({AJ['BIST']['yazilan']}, {AJ['BIST']['ilk']}..{AJ['BIST']['son']}); "
         f"KASA kapısı kesik {AJ['kasa']['kesik']}",
         f"- Üretici havuzu: {AJ['havuz']['hisse']} ABD hissesi, {AJ['havuz']['bar']} bar ({AJ['havuz']['donem'][0]}..{AJ['havuz']['donem'][1]}), sha {AJ['havuz']['sha'][:16]}", "",
         "## Şablon (sayısallaştırma)", "",
         f"- Bölge mumu {BJ['n_bolge']} (renk {BJ['renk_dizisi']}), tepe mumu {BJ['n_tepe']} -> TAM L = {BJ['sablon']['tam']['L']}, TEPESİZ L = {BJ['sablon']['tepesiz']['L']}",
         f"- Pencere uzunlukları: tam {BJ['sablon']['tam']['uzunluklar']}, tepesiz {BJ['sablon']['tepesiz']['uzunluklar']}",
         f"- Sınıflar: {BJ['sinif_sayim']}", "",
         "## Eşik (sentetik testten; gerçek veriye bakılarak DEĞİŞMEZ)", ""]
    for ad in ("tam", "tepesiz"):
        e = SJ["esik"][ad]; oz = SJ["ozet"]["A"][ad]; ob = SJ["ozet"]["B"][ad]
        s.append(f"- {ad.upper()}: S eşiği = {e['S']:.2f} (kök A %20 gürültü yakalama {100 * e['yakalama']:.1f} %, n {e['n']}); kök B (tekrar) %20 gürültü yakalama "
                 f"{100 * ob['yakalama_gurultu']['0.2']:.1f} %; yanlış alarm (tekil / 1.000 bar) blok {oz['yanlis']['blok']['tekil_1000']:.2f}, "
                 f"rastgele yürüyüş {oz['yanlis']['ry']['tekil_1000']:.2f}; tau {[round(x, 4) for x in SJ['kalibrasyon'][ad]['tau']]}")
    s += ["", "## Tanımlar (MI_ESIK; sha yukarıda)", "", "```", json.dumps(MI_ESIK, ensure_ascii=False, indent=1), "```", "",
          "## Karar / bilgi kuralı (önceden yazılı)", "", MI_ESIK["karar_kurali"], "",
          "Sonrası (R15, +%5) yalnız BİLGİ satırıdır; ana çıktı benzerlik sıklığı ve konumdur. KASA KURALI: tek iz -> kasa açılmaz.", "",
          "## KONTROL LİSTESİ", "", mi_kontrol_tablosu(), "",
          "## SAPMA", "", "(ön kayıt anında yok; gerçek veriden sonra zorunlu sapma olursa raporda SAPMA başlığıyla yazılır)", ""]
    return "\n".join(s)


def mi_onkayit_yaz(cikti: Optional[str] = None, uzerine: bool = False) -> str:
    y = _mi_yol("onkayit", cikti)
    if os.path.exists(y) and not uzerine:
        raise MIHata("ön kayıt zaten var (üzerine yazılmaz)")
    return _mi_yaz(y, mi_onkayit_metni(cikti), "ön kayıt")


# ================================================================ 8) GÖRSEL (PDF)
def _mi_mum_ciz(ax, O, H, L, C, x0: int = 0, genislik: float = 0.6, alfa: float = 1.0) -> None:
    for i, (o, h, l_, c) in enumerate(zip(O, H, L, C)):
        if not np.isfinite(o):
            continue
        rk = "#1a9850" if c >= o else "#d73027"
        ax.vlines(x0 + i, l_, h, color="#555555", linewidth=0.9, zorder=3, alpha=alfa)
        ax.bar(x0 + i, max(abs(c - o), (h - l_) * 0.02), bottom=min(o, c), width=genislik, color=rk, edgecolor=rk, zorder=4, alpha=alfa)


def mi_olay_ciz(ax, d: pd.DataFrame, r: Any, baslik: str) -> None:
    G = MI_ESIK["gercek"]["gorsel"]; t = d.index.get_loc(pd.Timestamp(r.tarih)); m = int(r.m)
    a = max(0, t - m + 1 - G["once"]); b = min(len(d), t + 1 + G["sonra"])
    w = d.iloc[a:b]; C = d.Close.to_numpy(float)
    BU, BO, BA = mi_bant(C)
    x = np.arange(b - a)
    _mi_mum_ciz(ax, *(w[c].to_numpy(float) for c in ("Open", "High", "Low", "Close")))
    for arr, ls in ((BU, "-"), (BO, "--"), (BA, "-")):
        ax.plot(x, arr[a:b], color="#9e8fd6", linewidth=0.9, linestyle=ls)
    p0 = t - m + 1 - a; p1 = t - a
    ax.axvspan(p0 - 0.5, p1 + 0.5, color="#ffb347", alpha=0.18, zorder=0)
    ax.axvline(p1 + 0.5, color="#333333", linewidth=0.7, linestyle=":")
    if t + 1 < len(d):
        e0 = float(d.Open.iloc[t + 1]); st = float(r.pencere_min_low) * MI_ESIK["gercek"]["stop_carpan"]
        ax.axhline(e0 * 1.05, color="#1a9850", linewidth=0.7, linestyle="--"); ax.axhline(st, color="#d73027", linewidth=0.7, linestyle="--")
    ax.set_title(baslik, fontsize=7.5)
    ax.tick_params(labelsize=6)


def mi_gorsel(cikti: Optional[str] = None, acik: Optional[str] = None, kuru: bool = False, ayar: Optional[str] = None) -> str:
    """MUM_IZI_GORSEL.pdf: s1 görüntü + kodun mumları; s2 parmak izi; s3 sentetik; s4 gerçek veri özeti; sonra eşleşmeler (tam + tepesiz)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from PIL import Image
    import OLCU_SINAMA as OS
    cikti = cikti or MI_YOL["cikti"]; acik = acik or MI_YOL["acik"]
    ayar = ayar or MI_YOL["cikti"]
    BJ = json.load(open(_mi_yol("sablon", MI_YOL["cikti"]), encoding="utf-8"))
    SJ = json.load(open(_mi_yol("sentetik", ayar), encoding="utf-8"))
    J = json.load(open(_mi_yol("sonuc", cikti), encoding="utf-8"))
    PT = pd.read_csv(_mi_yol("parmak", MI_YOL["cikti"]))
    O = pd.read_csv(_mi_yol("olay", cikti))
    y = _mi_yol("pdf", cikti)
    with PdfPages(y, metadata={"Title": "MUM_IZI", "CreationDate": None, "ModDate": None}) as pdf:
        # s1
        fig = plt.figure(figsize=(11.7, 8.3))
        a1 = fig.add_axes([0.02, 0.05, 0.3, 0.88]); a1.imshow(Image.open(MI_YOL["goruntu"])); a1.axis("off"); a1.set_title("Cemal'in görüntüsü", fontsize=9)
        a2 = fig.add_axes([0.34, 0.05, 0.3, 0.88]); a2.imshow(Image.open(_mi_yol("bindirme", MI_YOL["cikti"]))); a2.axis("off")
        a2.set_title("kodun gördüğü (mavi gövde, siyah fitil, mor bant; b bağlam, g gizli, k kesik)", fontsize=7)
        a3 = fig.add_axes([0.68, 0.45, 0.3, 0.45])
        T = pd.read_csv(_mi_yol("mumlar", MI_YOL["cikti"])); B = T[T.sinif.isin(["BOLGE", "BAGLAM", "GIZLI"])].reset_index(drop=True)
        _mi_mum_ciz(a3, B.O.to_numpy(), B.H.to_numpy(), B.L.to_numpy(), B.C.to_numpy())
        xx = np.arange(len(B))
        for c in ("BU", "BO", "BA"):
            a3.plot(xx, B[c].to_numpy(), color="#9e8fd6", linewidth=1, linestyle="--" if c == "BO" else "-")
        nb = int(B.sinif.isin(["BAGLAM", "GIZLI"]).sum()); a3.axvspan(nb - 0.5, len(B) - 0.5, color="#ffb347", alpha=0.15)
        a3.axvspan(len(B) - BJ["n_tepe"] - 0.5, len(B) - 0.5, color="#d73027", alpha=0.08)
        a3.set_title(f"sayısallaştırılmış: {BJ['n_bolge']} bölge mumu ({BJ['renk_dizisi']}), son {BJ['n_tepe']} = tepe", fontsize=8)
        a3.tick_params(labelsize=6)
        fig.text(0.68, 0.40, "Varsayım: grafik 4 saatlik (22 Kas - 24 Kas arası 12 mum).\nİz ölçek bağımsız kuruldu, günlük veriye uygulandı.\n"
                 "Fiyat ekseni yok: her şey piksel ve ortalama mum boyu birimi.", fontsize=8, va="top")
        pdf.savefig(fig); plt.close(fig)
        # s2 parmak izi
        fig = plt.figure(figsize=(8.3, 11.7)); ax = fig.add_axes([0.03, 0.02, 0.94, 0.94]); ax.axis("off")
        sat = [[r.olcu, r.aciklama[:62], f"{r.tam:.2f}", f"{r.tepesiz:.2f}", "S" if r.benzerlikte else ""] for r in PT.itertuples()]
        tb = ax.table(cellText=sat, colLabels=["ölçü", "düz dil", "tam", "tepesiz", "S'de"], loc="upper center", cellLoc="left", colLoc="left",
                      colWidths=[0.2, 0.58, 0.07, 0.08, 0.05])
        tb.auto_set_font_size(False); tb.set_fontsize(6.2); tb.scale(1, 1.05)
        gk = "\n".join(f"- {g['madde']}: {g['olcu'][:110]} -> {_mi_dogru(g['dogru'])}" for g in BJ["gorsel_okuma"])
        ax.text(0.0, 0.10, "Görsel okuma (sayıyla):\n" + gk, fontsize=6.3, va="top", transform=ax.transAxes)
        ax.set_title("PARMAK İZİ (birim = bölgenin ortalama mum boyu)", fontsize=10)
        pdf.savefig(fig); plt.close(fig)
        # s3 sentetik
        fig = plt.figure(figsize=(11.7, 8.3)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.92]); ax.axis("off")
        TT = pd.read_csv(_mi_yol("sentetik_tablo", ayar))
        g = TT[TT.kok == "A"].groupby(["sablon", "gurultu", "baglam"]).agg(yakalama=("yakalama", "mean"), yanlis=("yanlis_tekil_1000", "mean"),
                                                                        mae=("birebir_mae_sd", "mean"), r=("birebir_r", "mean")).reset_index()
        gb = TT[TT.kok == "B"].groupby(["sablon", "gurultu", "baglam"]).yakalama.mean().reset_index()
        g = g.merge(gb, on=["sablon", "gurultu", "baglam"], suffixes=("", "_B"))
        sat = [[r.sablon, f"%{100 * r.gurultu:.0f}", r.baglam, f"%{100 * r.yakalama:.0f}", f"%{100 * r.yakalama_B:.0f}", f"{r.yanlis:.2f}",
                f"{r.mae:.2f}" if np.isfinite(r.mae) else "-", f"{r.r:.2f}" if np.isfinite(r.r) else "-"] for r in g.itertuples()]
        tb = ax.table(cellText=sat, colLabels=["şablon", "gürültü", "bağlam", "yakalama A", "yakalama B (tekrar)", "yanlış alarm /1000 bar",
                                               "birebir |fark| / sd", "birebir r"], loc="upper center", cellLoc="center")
        tb.auto_set_font_size(False); tb.set_fontsize(6.5); tb.scale(1, 0.95)
        ax.set_title(f"SENTETİK TUTTURMA (iki üretici ortalaması; 200 tohum / koşul / üretici). Eşik: tam {SJ['esik']['tam']['S']:.2f}, "
                     f"tepesiz {SJ['esik']['tepesiz']['S']:.2f}", fontsize=9)
        pdf.savefig(fig); plt.close(fig)
        # s4 gerçek özet
        fig = plt.figure(figsize=(11.7, 8.3)); ax = fig.add_axes([0.02, 0.02, 0.96, 0.92]); ax.axis("off")
        sat = []
        for ad in ("tam", "tepesiz"):
            for p in J["tarama"]:
                bz = J["benzerlik"][ad][p]; kn = J["konum"].get(f"{p}|{ad}", {})
                for hc in MI_ESIK["gercek"]["donem"]:
                    c = J["hucre"].get(f"{p}|{ad}|hepsi|{hc}", {})
                    pl = c.get("plasebo") or {}
                    sat.append([ad, p, hc, f"{bz['gercek_tekil_1000']:.2f}", f"{bz['oran_blok']:.2f}" if bz.get("oran_blok") else "-",
                                f"%{100 * kn.get('tepe_pay', np.nan):.0f}" if kn else "-", str(c.get("n", 0)),
                                f"{100 * c['fark']:+.2f}" if c.get("fark") is not None and np.isfinite(c.get("fark", np.nan)) else "-",
                                f"%{100 * c['h5']:.0f} / %{100 * c['h5_es']:.0f}" if c.get("h5") is not None and np.isfinite(c.get("h5", np.nan)) else "-",
                                f"%{100 * pl['tutar_pay']:.0f}" if pl.get("tutar_pay") is not None else "-", c.get("hukum", "-")])
        tb = ax.table(cellText=sat, colLabels=["şablon", "pazar", "hücre", "eşleşme /1000 bar", "gerçek / rastgele", "tepede", "n (ölçülen)",
                                               "R15 eşli fark (puan)", "+%5: olay / eş", "plasebo TUTAR payı", "C2 hüküm"], loc="upper center", cellLoc="center")
        tb.auto_set_font_size(False); tb.set_fontsize(6.5); tb.scale(1, 1.1)
        ax.set_title("GERÇEK VERİ (açık, <= 2022-12-31). Etiket: " + ", ".join(f"{k} = {v['etiket']}" for k, v in J["etiket"].items()), fontsize=9)
        pdf.savefig(fig); plt.close(fig)
        # eşleşmeler
        G = MI_ESIK["gercek"]["gorsel"]
        Vc: Dict[str, Any] = {}
        for ad in ("tam", "tepesiz"):
            x = O[(O.sablon == ad) & O.pazar.isin(MI_ESIK["gercek"]["pazar_karar"]) & (pd.to_datetime(O.tarih) <= MI_KESIK - pd.Timedelta(days=30))]
            if "p2" in x.columns:
                x = x[x.p2.fillna(False).astype(bool)]
            tep = x[x.konum == "TEPE"].sort_values("S", ascending=False).head(G["tepe"])
            bas_ = x[x.konum.isin(["DIP", "ORTA"])].sort_values("S", ascending=False).head(G["baska"])
            kalan = x.drop(index=tep.index.union(bas_.index))
            rs = kalan.sample(n=min(G["rastgele"], len(kalan)), random_state=G["tohum"]) if len(kalan) else kalan
            liste = [("en yüksek S, TEPE", r) for r in tep.itertuples()] + [("en yüksek S, başka yerde", r) for r in bas_.itertuples()] + \
                    [("rastgele", r) for r in rs.itertuples()]
            for i0 in range(0, len(liste), 4):
                fig, axs = plt.subplots(2, 2, figsize=(11.7, 8.3)); axs = axs.ravel()
                for k, (tur, r) in enumerate(liste[i0:i0 + 4]):
                    if r.pazar not in Vc:
                        Vc[r.pazar] = mi_veri(r.pazar, acik)["V"]
                    d = Vc[r.pazar][r.sembol]
                    r15 = f"{100 * r.r15:+.1f}%" if hasattr(r, "r15") and pd.notna(r.r15) else "-"
                    fk = f"{100 * r.fark:+.1f}" if hasattr(r, "fark") and pd.notna(r.fark) else "-"
                    h5 = getattr(r, "h5", np.nan)
                    h5s = "-" if not (isinstance(h5, (int, float)) and np.isfinite(h5)) else ("evet" if h5 >= 0.5 else "hayır")
                    mi_olay_ciz(axs[k], d, r, f"{ad} | {tur} | {r.pazar} {r.sembol} {r.tarih} | S {r.S:.2f}, {r.m} mum | {r.konum} | R15 {r15}, eşli {fk} puan | +%5 stop öncesi: {h5s}")
                for k in range(len(liste[i0:i0 + 4]), 4):
                    axs[k].axis("off")
                fig.suptitle(f"EŞLEŞMELER ({ad}): turuncu = pencere, sağı sonraki 15 mum; yeşil kesik = giriş +%5, kırmızı kesik = stop (pencere dibi x 0,98)",
                             fontsize=8)
                fig.tight_layout(rect=[0, 0, 1, 0.96]); pdf.savefig(fig); plt.close(fig)
    return y


# ================================================================ 9) RAPOR
def _mi_dogru(v: Any) -> str:
    return "-" if v is None else ("KISMEN" if v == "KISMEN" else ("DOĞRU" if v else "DEĞİL"))


def _p(x: Any, n: int = 1) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"%{100 * float(x):.{n}f}"


def _s(x: Any, n: int = 2) -> str:
    return "-" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{float(x):.{n}f}"


def mi_rapor(cikti: Optional[str] = None) -> str:
    cikti = cikti or MI_YOL["cikti"]
    BJ = json.load(open(_mi_yol("sablon", cikti), encoding="utf-8")); SJ = json.load(open(_mi_yol("sentetik", cikti), encoding="utf-8"))
    J = json.load(open(_mi_yol("sonuc", cikti), encoding="utf-8")); PT = pd.read_csv(_mi_yol("parmak", cikti))
    s = [f"# MUM_IZI RAPOR ({_mi_simdi()})", "", f"Sürüm: {MI_SURUM}", "",
         "## SONUÇ", ""]
    for ad in ("tam", "tepesiz"):
        s.append(f"- {ad.upper()} iz: etiket {J['etiket'][ad]['etiket']}; S eşiği {SJ['esik'][ad]['S']:.2f}")
    s += ["", "## SAYISALLAŞTIRMA", "",
          f"- Bölge mumu {BJ['n_bolge']}, renk dizisi {BJ['renk_dizisi']} (Y yeşil, K kırmızı); tepe mumu {BJ['n_tepe']}; sınıflar {BJ['sinif_sayim']}",
          f"- Izgara: x = {BJ['izgara']['a']:.2f} + {BJ['izgara']['b']:.3f} k (piksel)", f"- Elle doğrulama mumları: {BJ['elle']['mumlar'] if 'elle' in BJ else '-'}", "",
          "## PARMAK İZİ", "", "| ölçü | düz dil | tam | tepesiz |", "|---|---|---|---|"]
    for r in PT.itertuples():
        s.append(f"| {r.olcu} | {r.aciklama} | {_s(r.tam)} | {_s(r.tepesiz)} |")
    s += ["", "Görsel okuma:", ""] + [f"- {g['madde']}: {g['olcu']} -> {_mi_dogru(g['dogru'])}" for g in BJ["gorsel_okuma"]]
    s += ["", "## SENTETİK TEST", ""]
    for kn in ("A", "B"):
        for ad in ("tam", "tepesiz"):
            o = SJ["ozet"][kn][ad]
            s.append(f"- kök {kn} {ad}: yakalama gürültü {', '.join(f'{k}: {_p(v, 0)}' for k, v in o['yakalama_gurultu'].items())}; %20 bağlam "
                     f"{', '.join(f'{k}: {_p(v, 0)}' for k, v in o['yakalama_baglam_g20'].items())}; yanlış alarm tekil / 1.000 bar blok "
                     f"{_s(o['yanlis']['blok']['tekil_1000'])}, ry {_s(o['yanlis']['ry']['tekil_1000'])}; birebir (%20) |fark| / sd "
                     f"{_s(o['birebir_g20'].get('mae_sd'))}, r {_s(o['birebir_g20'].get('r_ort'))}, aynı pencere {_p(o['birebir_g20'].get('ayni_pencere_pay'), 0)}")
    s += ["", "## GERÇEK VERİ", "", "| şablon | pazar | eşleşme / 1.000 bar | hisse-yıl başına | gerçek / blok | gerçek / ry | tepede | başka yerde |",
          "|---|---|---|---|---|---|---|---|"]
    for ad in ("tam", "tepesiz"):
        for p, b in J["benzerlik"][ad].items():
            k = J["konum"].get(f"{p}|{ad}", {})
            s.append(f"| {ad} | {p} | {_s(b['gercek_tekil_1000'], 3)} | {_s(b['gercek_tekil_hisse_yil'], 3)} | {_s(b['oran_blok'])} | {_s(b['oran_ry'])} | "
                     f"{_p(k.get('tepe_pay'), 0)} | {_p(k.get('baska_pay'), 0)} |")
    s += ["", "Sonrası (BİLGİ):", "", "| şablon | pazar | hücre | grup | n | R15 eşli fark | boot %95 | SIRA | güç | +%5 olay | +%5 eş | plasebo fark / TUTAR payı | hüküm |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in J["hucre"].items():
        p, ad, g, hc = k.split("|"); pl = c.get("plasebo") or {}
        s.append(f"| {ad} | {p} | {hc} | {g} | {c.get('n', 0)} | {_p(c.get('fark'), 2)} | {_p(c.get('boot_alt'), 2)}..{_p(c.get('boot_ust'), 2)} | {_s(c.get('sira'), 3)} | "
                 f"{_s(c.get('guc'))} | {_p(c.get('h5'), 0)} | {_p(c.get('h5_es'), 0)} | {_p(pl.get('fark_ort'), 2)} / {_p(pl.get('tutar_pay'), 0)} | {c.get('hukum', '-')} |")
    s += ["", "## DOĞRULAMA", "", f"- prefix (K2): {J['prefix']}", f"- düz S (K11): {J['duz']}", f"- 2 hücre yeniden üretim (K11): {J.get('yeniden')}",
          f"- KASA: {J['kasa']}", f"- en geç tarih: {J.get('en_gec')}", ""]
    return _mi_yaz(_mi_yol("rapor", cikti), "\n".join(s), "rapor")


# ================================================================ 10) ÇAKIŞMA KAPISI ve ANA
def _cakisma_kontrol_mi(_once=_CK_ONCE_MI, _dosya="MUM_IZI.py"):
    g = globals(); ezilen = []
    for k, v in _once.items():
        if k.startswith("__") or k in ("_CK_ONCE_MI",):
            continue
        if k in g and id(g[k]) != v and not k.startswith("_"):
            ezilen.append(k)
    if ezilen:
        raise RuntimeError(f"{_dosya}: çakışma kapısı: bellekteki adlar ezildi {ezilen[:8]} -> çalışma zamanını yeniden başlat")


_cakisma_kontrol_mi()


def _mi_ana(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="MUM_IZI: Cemal'in mum bölgesi parmak izi")
    ap.add_argument("komut", choices=["sayisallastir", "acik", "sentetik", "kuru", "onkayit", "kos", "gorsel", "rapor", "sha"])
    ap.add_argument("--tohum", type=int, default=None)
    ap.add_argument("--plasebo_tohum", type=int, default=None)
    a = ap.parse_args(argv)
    try:
        if a.komut == "sha":
            print(json.dumps({"KOD_SHA": _mi_sha(MI_YOL["kod"]), "ESIK_SHA": mi_esik_sha()}, indent=1))
        elif a.komut == "sayisallastir":
            J = mi_sayisallastir_kos()
            print(json.dumps(_mi_json({k: J[k] for k in ("n_bolge", "n_tepe", "renk_dizisi", "sinif_sayim", "gorsel_okuma")}), ensure_ascii=False, indent=1))
        elif a.komut == "acik":
            J = mi_acik()
            print(json.dumps(_mi_json({k: {kk: vv for kk, vv in v.items() if kk != "yil_sembol"} if isinstance(v, dict) else v for k, v in J.items()}),
                             ensure_ascii=False)[:3000])
        elif a.komut == "sentetik":
            J = mi_sentetik(tohum=a.tohum)
            print(json.dumps(_mi_json({"esik": {k: {kk: vv for kk, vv in v.items() if kk != "izgara"} for k, v in J["esik"].items()},
                                       "kalibrasyon": {k: v["tau"] for k, v in J["kalibrasyon"].items()}}), ensure_ascii=False, indent=1))
        elif a.komut == "kuru":
            kl = os.path.join(MI_YOL["gecici"], "kuru"); ay = os.environ.get("MI_KURU_AYAR") or MI_YOL["cikti"]
            vk = mi_kuru_veri(os.path.join(kl, "veri"), ayar=ay)
            J = mi_kos(acik=vk, cikti=kl, kuru=True, plasebo_tohum=a.plasebo_tohum or 5, ayar=ay)
            mi_gorsel(cikti=kl, acik=vk, kuru=True, ayar=ay)
            print(json.dumps(_mi_json({k: J[k] for k in ("etiket", "benzerlik", "konum", "prefix", "duz")}), ensure_ascii=False)[:5000])
        elif a.komut == "onkayit":
            print(mi_onkayit_yaz())
        elif a.komut == "kos":
            J = mi_kos(plasebo_tohum=a.plasebo_tohum)
            print(json.dumps(_mi_json({k: J[k] for k in ("etiket", "benzerlik", "konum", "prefix", "duz", "yeniden")}), ensure_ascii=False)[:6000])
        elif a.komut == "gorsel":
            print(mi_gorsel())
        elif a.komut == "rapor":
            print(mi_rapor())
    except MIHata as ex:
        milog.error("DURDU: %s", ex)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_mi_ana())
