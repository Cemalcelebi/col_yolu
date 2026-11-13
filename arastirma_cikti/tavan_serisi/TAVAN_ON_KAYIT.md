# TAVAN SERİSİ ÖN KAYDI (ölçümden önce)

TAVAN_SERISI v1.0 (tavan_serisi_20261113): çökmüş BIST hissesinde art arda tavan; canlı tarama + geçmiş taban oranlar (ön kayıtlı). Yazılma 2026-11-13 11:33:13 UTC. Bu dosya git'e işlenmeden `python TAVAN_SERISI.py kos` çalışmaz (mühür kapısı).

## Soru

Çökmüş (seri öncesi kapanış 250 günlük en yüksekten >= %80 aşağıda) BIST hissesinde art arda tavan serisinin k. gününden sonra katılmak (ertesi gün açılış) ne getirmiş, ne kaybettirmiş; aynı gün aynı derinlikte çökmüş ama tavan yapmayan hisselerden iyi mi?

## Tanımlar ve eşikler (TS_ESIK, değişmez)

```json
{
 "bootstrap": {
  "B": 2000,
  "guven": [
   2.5,
   97.5
  ],
  "kume": "hisse (olayları hisseleriyle birlikte çekilir)",
  "olcu": "medyan fark ve ortalama fark (60 gün)",
  "tohum": 20261113
 },
 "canli": {
  "dip_bas": "2026-09-01",
  "dusus": -0.8,
  "fon": "kriz öncesi fon payı = bilinme tarihi <= 31.08.2026 olan son KAP fon raporu ayındaki pay (FON_IZI.fi_k25_pay_tablo); ayrıca 2026 Oca-Ağu en yüksek pay",
  "gun20": 20,
  "gun_ici": "son bar bugünün tarihi ve saat < 15:10 UTC (18:10 TR) ise 'gün içi' yazılır; ardışık tavan hem 'dünkü kapanışla kesin' hem 'bugün dahil (gün içi)' verilir",
  "hacim5": 5,
  "hacim_med": 20,
  "tepe": [
   "2026-06-01",
   "2026-08-31"
  ]
 },
 "donem": {
  "2016-19": [
   "2016-01-01",
   "2019-12-31"
  ],
  "2020-22": [
   "2020-01-01",
   "2022-12-31"
  ],
  "2023-26.08": [
   "2023-01-01",
   "2026-08-31"
  ],
  "tanim": "dönem = k. tavan gününün tarihi"
 },
 "duyarlilik": {
  "esik": [
   -0.6,
   -0.7
  ],
  "kova": "e, e + (-1 - e) / 3, e + 2 (-1 - e) / 3 (ana -0,80 için iş tanımındaki sabit kovalar)",
  "not": "BİLGİ, karara girmez: ÇÖKMÜŞ eşiği gevşetilince aynı ölçüler (ana n küçükse yön bilgisi için)"
 },
 "karar": {
  "donem_min": 2,
  "donem_n_min": 10,
  "karsilastirma": "ÇÖKMEMİŞ hisselerde k. tavan: aynı ölçüler BİLGİ (kontrolsüz)",
  "metin": "her k için: 'k. tavandan sonra katılmak kontrolden iyi' <=> n >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(-%50, 60g) <= 1,2 x kontrolün P(-%50, 60g) VE üç dönemin en az ikisinde dönem medyan farkı > 0 (n >= 10 olan dönemler; n < 10 dönem 'yön yok' sayılır); değilse 'kumar: beklenen değer kontrolden iyi değil'. n < 30 -> 'örneklem yetersiz'. 8 ayrı k sınanır: tek k'nın geçmesi çoklu deneme şansı olabilir, raporda yazılır.",
  "n_min": 30,
  "p50_kat": 1.2
 },
 "kontrol": {
  "fark": "olay başına fark = olay r60 - kontrol ortalama r60; kontrolü olmayan olay farkta dışarıda (sayılır)",
  "kova": [
   -0.8,
   -0.85,
   -0.9
  ],
  "kova_tanim": "derinlik kovası: (-0,85, -0,80], (-0,90, -0,85], <= -0,90 (sabit)",
  "tanim": "her ÇÖKMÜŞ olay için: aynı referans gününde (olay hissesinin seri öncesi günü) ÇÖKMÜŞ ve aynı derinlik kovasında olan, seri başından k. tavan gününe kadar (dahil) hiç tavan yapmamış, giriş günü e'de işlem gören (O var, hacim > 0) bütün öteki hisseler; girişleri aynı gün O_e; ölçüler aynı. Kontrol değeri = kontrol hisselerinin ortalaması (oran ölçülerde ortalama oran)"
 },
 "olay": {
  "ana_n": "ana tablo n'i = 60 gün penceresi kesik içinde tamamlanan olaylar",
  "bilgi": [
   "2026-09-01",
   null
  ],
  "cokmus": {
   "en_az": 250,
   "esik": -0.8,
   "pencere": 250,
   "tanim": "derinlik = seri ilk tavanından ÖNCEKİ günün kapanışı / (kendi son 250 barının en yüksek kapanışı) - 1; 250 bar kırıktan sonra dolmalı (yoksa tanımsız: ne ÇÖKMÜŞ ne ÇÖKMEMİŞ). ÇÖKMÜŞ <=> derinlik <= -0,80; ÇÖKMEMİŞ <=> > -0,80"
  },
  "dokunma": {
   "asagi": -0.5,
   "tanim": "P(+%100, 60g) <=> max H[e..e+59] >= 2 O_e; P(-%50, 60g) <=> min L[e..e+59] <= 0,5 O_e; P(-%50, 120g) aynı 120 barda",
   "yukari": 1.0
  },
  "dolum_belirsiz": "e günü tavan VE O_e = H_e = L_e (tam kilitli tavan; alıcı sırada kalır): işaretlenir; ana sonuç yine O_e'den, 'yalnız dolum belirsiz olmayanlar' ayrı satır",
  "donem": [
   "2016-01-01",
   "2026-08-31"
  ],
  "getiri": "r_h = C(e + h - 1) / O_e - 1 (e = 1. gün; takvim satırı, durdurmada son kapanış ileri taşınır); h penceresi kriz kesiğini (31.08.2026) aşan olay o ufukta ölçülmez",
  "giris": "t'den sonraki ilk kendi barı e'nin açılışı O_e; e'de hacim 0 / O yok -> dışarıda (sayılır)",
  "k": [
   1,
   2,
   3,
   4,
   5,
   6,
   8,
   10
  ],
  "kriz": "2026-08-31",
  "seri": "ardışık tavan günleri (kendi barları) bir seri; k. tavan günü t = seri başı + k - 1; aynı serinin her k'sı ayrı satır; seri uzunluğu L; ertesi gün tavan <=> L > k",
  "ufuk": [
   5,
   20,
   60,
   120
  ]
 },
 "surum_etiket": "tavan_serisi_20261113",
 "tavan": {
  "esik_kat": 0.95,
  "kilitli": "kilitli tavan günü = tavan VE O = H = C (göreli tolerans 1e-6); tam kilitli = ayrıca L = H",
  "kirik": 0.25,
  "kirik_tanim": "|r| > 0,25 = VERİ KIRIĞI (düzeltilmemiş bedelsiz / bedelli, uzun durdurma sonrası baz fiyat, Yahoo hatası): tavan değildir, seriyi keser ve 250 gün tepesi kırıktan sonra yeniden başlar",
  "rejim": [
   [
    "2000-01-01",
    "2020-03-12",
    0.2
   ],
   [
    "2020-03-13",
    "2099-12-31",
    0.1
   ]
  ],
  "rejim_kaynak": "BIST günlük fiyat marjı 12.03.2020'ye kadar ±%20, 13.03.2020'den ±%10 (veride: 2016-19 tavan kümesi +%19,5-20,5, +%9,5-10,5 günü yılda ~200; 12.03.2020'de 134 gün <= -%19, 13.03.2020'den sonra yok; Mart 2020'den +%9,5-10,5 yılda 3.500+)",
  "tanim": "marj m (o günün rejimi); tavan günü <=> r = C_t / C_t-1 - 1 >= min(0,95 m ; adim_tavan - 1e-9) VE r <= 1,05 m; adim_tavan = (ekran C_t-1 x (1 + m) BIST fiyat adımına aşağı yuvarlanmış) / ekran C_t-1 - 1. m = %10 için eşik iş tanımındaki +%9,5 aynen; 1-2 TL'de adım yuvarlaması gerçek tavanı %9,5'in altına indirdiği için (1,38 -> 1,51 = +%9,42) o günlerde gerçek tavan fiyatı kullanılır; r > 1,05 m marjla olamaz -> tavan sayılmaz. 2016 - 12.03.2020 (±%20 rejimi) +%9,5 günü tavan DEĞİLDİR (eşik +%19)",
  "tol": 1e-06,
  "ust_kat": 1.05
 },
 "veri": {
  "bas": "2015-01-01",
  "bit": "2026-11-14",
  "ekran": "ekran fiyatı = Yahoo fiyatı x tarihi o günden SONRA olan bölünme oranlarının çarpımı (K60_veri.k60v_bolunme_carpan)",
  "evren": "V_BIST.pkl sembolleri ∪ dol.pkl kodları, Yahoo kodu SEMBOL.IS",
  "fiyat": "Yahoo quote OHLC (bölünme / bedelsiz düzeltmeli, temettüsüz); O/H/L tutarsızsa H = max(O,H,C), L = min(O,L,C)",
  "kaynak": "Yahoo chart API v8 günlük (K60_veri.k60v_fiyat_indir, değiştirilmeden; yalnız bas / bit bu iş için)",
  "takvim": "hafta içi ve en az 10 hissenin işlem gördüğü günler; her hisse kendi barlarıyla (durdurma günleri atlanır)"
 },
 "yanlilik": "evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker); Yahoo BIST geçmişinde eksik bedelsiz düzeltmesi kırık kuralıyla ayıklanır; işlem maliyeti yok"
}
```

Fiyat adımları (TS_ADIM): [[0.0, 0.01], [20.0, 0.02], [50.0, 0.05], [100.0, 0.1], [250.0, 0.25], [500.0, 0.5], [1000.0, 1.0], [2500.0, 2.5]]

## Karar cümlesi (önceden yazılı)

her k için: 'k. tavandan sonra katılmak kontrolden iyi' <=> n >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(-%50, 60g) <= 1,2 x kontrolün P(-%50, 60g) VE üç dönemin en az ikisinde dönem medyan farkı > 0 (n >= 10 olan dönemler; n < 10 dönem 'yön yok' sayılır); değilse 'kumar: beklenen değer kontrolden iyi değil'. n < 30 -> 'örneklem yetersiz'. 8 ayrı k sınanır: tek k'nın geçmesi çoklu deneme şansı olabilir, raporda yazılır.

Ölçülecekler (k = 1, 2, 3, 4, 5, 6, 8, 10): P(ertesi gün de tavan); seri uzunluğu dağılımı (k'ya koşullu); getiri 5 / 20 / 60 / 120 gün (medyan, ortalama, %25 / %75); P(60 günde +%100'e dokunma), P(60 günde -%50'ye dokunma), P(120 günde -%50); kontrole göre fark ve hisse kümeli bootstrap %95 aralık; dönem kırılımı 2016-19 / 2020-22 / 2023-26.08; 'yalnız dolum belirsiz olmayanlar' ayrı satır; ÇÖKMEMİŞ hisselerde k. tavan (BİLGİ); Eylül - Kasım 2026 olayları ayrı BİLGİ tablosu (karara girmez).

## Veri ve tanım sayımı (sonuç içermez)

- Fiyat: 630 hisse okundu, 0 eksik (); son tarih 2026-11-13; manifest sha256 5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56.
- Test paneli (kesik 2026-08-31): {"hisse": 626, "takvim_bas": "2015-01-01", "takvim_son": "2026-08-31", "seri_cokmus": 134, "seri_cokmemis": 17555, "seri_tanimsiz": 2685, "cokmus_seri_hisse": 40}

## Ön kayıttan önce görülenler (sonuç değil)

- Günlük getiri dağılımı yıllara göre (BIST fiyat marjı rejimini bulmak için: 12.03.2020'ye kadar ±%20). Bu yüzden 2016 - 12.03.2020 tavan eşiği +%19 (iş tanımındaki +%9,5 o dönemde tavan değildir).
- Tanım denetimi için k'ya göre ÇÖKMÜŞ olay sayıları (k = 1: 134, 2: 47, 3: 19, 4: 7, 5: 6, 6: 4, 8: 2, 10: 1; 40 hisse). n küçük: k >= 3 büyük olasılıkla 'örneklem yetersiz' çıkar. Bu yüzden ÇÖKMÜŞ eşiği -%60 / -%70 duyarlılığı BİLGİ olarak eklendi (karar ana tanımda kalır). Getiri, dokunma oranı, kontrol farkı görülmedi.
- Canlı tarama (İŞ 1) bugünkü durumu gösterir, getiri içermez.

## Bilinen yanlılıklar

evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker); Yahoo BIST geçmişinde eksik bedelsiz düzeltmesi kırık kuralıyla ayıklanır; işlem maliyeti yok

ESIK_SHA256: b6cccebae0a04b9caf7d6686558791afcbca0caec0add5bfadcceed413b33c5a
KOD_SHA256: 1c6ecf2be0a69ba63fd811f2130ec948b1c8990a04f76b1e045d7d7016dc2c00
VERI_MANIFEST_SHA256: 5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56
