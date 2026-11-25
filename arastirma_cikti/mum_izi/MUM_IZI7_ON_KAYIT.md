# MUM_IZI7 ÖN KAYIT (2026-11-25T21:05:41Z)

v4 yalnız Cemal'in kapak notundan, şablonun kendi mumlarından ve sentetikten kuruldu. Etiket dosyaları (set 1, set 2), işaretli PDF'ler, mum_izi6 olc çıktıları ve mum_izi5_sinama.csv bu dosya commit edilene kadar AÇILMADI. Sınama (C) bu commit'ten sonra; sonra tanım değişmez.

## Mühürler

KOD7_SHA: 6b3e2e4fa74f9cde3b4e99c1b47c8f4b9c31765cc604d478e5699bf2768cafbe
ESIK7_SHA: 78b41aa0d540b4cbc6aff3a759385d029439b7ec301dcd03df8b15d1a8c71750
SABLON7_SHA: dc61888d92bfc7781598d54892d0edb5a1ccb91f18f8214500a0be9ab6e2a3bc
SENTETIK7_SHA: 40cec1fb16cd2c1425ea42f6afaa85e55da2418230b274734421eed7d919ea71
V3_KOD_SHA: 70fc2fb979c47b2a2bd5fb260e1fb1891e7b34268f49c4a4276f482b66a4eb69
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
E6_KOD_SHA: cc8c6c914d7ecaa02682eb9c302e63635e567a1d828f7416a0cbb6bdeb291f1d

- MUM_IZI_V4.py commit'i: 3636571ed0472f7faa393f1c83d91c3fd94b07b1 2026-11-25T21:05:40+00:00

## Şablonun dört parçadaki değerleri (mum_izi7_sablon.json)

- Yapı: k = 10 (ilk SMA üstü kapanış; ön kısım 10 mum = floor(20 / 2) SINIRDA), tırmanış kısmı 9 mum.
- Değerler: {"E1_bC_ort": -0.412, "E1_degisim": 6.0, "E2_yesil": 0.7891, "E2_onceki": -0.1091, "E2_ust_pay": 1.0, "E3_icerden": 1.0, "E3_govde_med": 1.0, "E3_govde_max": 1.0, "E3_spearman": 0.7, "E3_son_bC": 0.9048, "E3_ortusme": 1.0, "E4_pay": 0.5}
- Parçalar: E1 True, E2 True, E3 True, E4 True; VAR True; parça puanları {'E1': 0.687, 'E2': 1.0, 'E3': 0.625, 'E4': 0.5}; PUAN4 0.500
- Referanslar (tırmanış kısmı): gövde medyanı 0.1305, en büyük gövde 0.4503 (b birimi), ardışık örtüşme 0.7023.
- Sınırdaki değerler: E4 uzun üst fitil payı şablonda tam %50 (10 / 20; eşik %50): şablon geçiyor ama sınırda (PUAN4 0,5). k = 10 = floor(m / 2) sınırda.

## Uygulama kararları (iş tanımında açık bırakılanlar; etiketlerden önce)

1. Bölge uzunlukları 16, 17, ..., 24 (dokuzu); bir pencere sonu, uzunluklardan biri VAR ise VAR; PUAN4 uzunluklar içinde en büyüğü.
2. Çıkış mumu k = pencerede bC > 0 olan İLK mum. Ön kısım = 0..k-1 (iş tanımındaki 'en az 3, en çok bölgenin yarısı' -> 3 <= k <= floor(m / 2)); tırmanış kısmı = k+1..m-1 (çıkış mumu hariç), en az 5 mum. Yapı yoksa E1-E3 YOK, puanları 0.
3. E1 'kapanış yönü': fiyat kapanışlarının ardışık farkının işareti, yalnız ön kısım içindeki çiftler; 'değişim' = ardışık iki yönün çarpımı < 0 (sıfır yön değişim saymaz).
4. E2 'çıkıştan sonra' = tırmanış kısmı (k+1..m-1). E3 (a) payı tırmanış kısmının bölgenin son 3 mumu dışındaki mumlarında (k+1..m-4).
5. E3 (b) gövde = |bC - bO| (b birimi); şablon referansı tırmanış kısmı (mum 11-19): medyan 0,1305, en büyük 0,4503.
6. E3 (c) Spearman eşitlerde ortalama sıra; tırmanış kısmında bC ile sıra numarası. 'Son kapanış' = bölgenin son mumu.
7. E3 (d) örtüşme = MI 'ortusme' (ortak aralık / iki mumdan küçüğünün boyu), yalnız ikisi de tırmanış kısmında olan ardışık çiftler; şablon 0,7023.
8. E4 bölgenin bütün mumları; şablon payı 10 / 20 = %50 (sınırda geçiyor).
9. Dereceli puan: V4_ESIK['puan'] (eşikte 0,5; ölçek s alt koşul başına sabit); parça puanı alt koşulların en küçüğü; PUAN4 dört parçanın en küçüğü.
10. Sentetik: MUM_IZI_V3.v3_seri gömmesi (MI üreteci; ölçek 0,5-2, esneme 0,8-1,2); bağlam dip / yatay (iş tanımı); başarı = gerçek sonun +-3 barında VAR. n4 iş tanımında yok (atlandı); n8 iki ayrı negatif (n8a kırmızı boşluklu çıkış, n8b tek dev mum). Rastgele: 200 seri x 1.060 bar x iki üretici, tekil VAR / 1.000 bar.
11. Sınama: sayfanın kendi penceresi (anahtardaki hisse, son, m); set 2'de katman 'T' (tekrar) sayfaları dışarıda; YOK / IKISI / BELIRSIZ karar dışı. Kappa bootstrap'ında kappası tanımsız (tek sınıflı) örnekler atılır ve sayısı yazılır. Hüküm birleşik kümede. Esnek hizalama yalnız bilgi.
12. D yalnız C hükmü UYUMLU ise (MUM_IZI_ETIKET2'nin P2 / BIST maskeleri; onay tohumu 25112073).

## v4 tanımı (V4_ESIK; sha yukarıda)

```
{
 "surum": "V4-1.0",
 "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20); Bollinger (20, 2; std ddof 0), her mum kendi gününe kadarki barlarla (MI.mi_bant); şablonda bantlar görüntüden; üst bant <= SMA olan pencere geçersiz",
 "uzunluklar": [
  16,
  17,
  18,
  19,
  20,
  21,
  22,
  23,
  24
 ],
 "yapi": "k = pencerede kapanışı SMA'nın üstünde (bC > 0) olan İLK mumun sırası (0'dan). Ön kısım = 0..k-1, çıkış mumu = k, tırmanış kısmı = k+1..m-1. Yapı koşulu: böyle bir mum var, 3 <= k <= floor(m / 2) (ön kısım en az 3, en çok bölgenin yarısı), tırmanış kısmı >= 5 mum. Yapı yoksa E1-E3 YOK ve puanları 0",
 "E1": {
  "tanim": "ön kısımda bC ortalaması <= -0,3 VE kapanış yönü (sign(C_j - C_j-1), ön kısım içindeki ardışık çiftler) en az 2 kez değişiyor (ardışık iki yön çarpımı < 0)",
  "bC_ort": -0.3,
  "degisim": 2
 },
 "E2": {
  "tanim": "çıkış mumu k yeşil (C > O); önceki kapanış SMA altında (bC_k-1 < 0); tırmanış kısmında kapanışların >= %80'i SMA üstünde (bC > 0)",
  "ust_pay": 0.8
 },
 "E3": {
  "tanim": "tırmanış kısmı (k+1..m-1): (a) bölgenin son 3 mumu hariç bu kısmın kapanışlarının >= %80'i 0 < bC <= 1,05; (b) gövde |bC - bO| medyanı <= şablonun tırmanış kısmındaki medyanın 1,5 katı VE en büyük gövde <= şablondakinin 1,5 katı; (c) bC'nin sıraya göre Spearman korelasyonu (eşitlerde ortalama sıra) >= 0,6 VE bölgenin son kapanışı bC >= 0,6; (d) tırmanış kısmı içindeki ardışık mum çiftlerinin örtüşmesi (ortak aralık / küçük mum boyu; MI 'ortusme' tanımı) ortalaması >= şablonun aynı ortalamasının 0,75 katı",
  "icerden_pay": 0.8,
  "icerden_ust": 1.05,
  "muaf_son": 3,
  "govde_kat": 1.5,
  "spearman": 0.6,
  "son_bC": 0.6,
  "ortusme_kat": 0.75
 },
 "E4": {
  "tanim": "bölgenin bütün mumlarında uzun üst fitil = üst fitil >= mum boyunun %30'u VE üst fitil > alt fitil; bu mumların payı >= %50",
  "fitil_oran": 0.3,
  "pay": 0.5
 },
 "kural": "v4 VAR <=> E1 ve E2 ve E3 ve E4 (ikili koşullar); bir pencere sonunda 16-24 uzunluklarından biri VAR ise o son VAR",
 "puan": {
  "tanim": "her alt koşul için g = 0,5 + (x - eşik) / (2 s) ('>=' koşulu) ya da 0,5 + (eşik - x) / (2 s) ('<=' koşulu), [0, 1]'e kırpılır; parça puanı = alt koşulların en küçüğü; PUAN4 = dört parça puanının en küçüğü (telafi yok); yapı yoksa E1-E3 puanı 0. Eşikte g = 0,5. Bir pencere sonunun PUAN4'ü uzunluklar içinde en büyüğü",
  "s": {
   "E1_bC_ort": 0.3,
   "E1_degisim": 1.0,
   "E2_yesil": 0.1,
   "E2_onceki": 0.1,
   "E2_ust_pay": 0.2,
   "E3_icerden": 0.2,
   "E3_govde_med": 0.5,
   "E3_govde_max": 0.5,
   "E3_spearman": 0.4,
   "E3_son_bC": 0.4,
   "E3_ortusme": 0.25,
   "E4_pay": 0.25
  },
  "not": "E2_yesil x = bC_k - bO_k (eşik 0); E2_onceki x = bC_k-1 (<= 0); ikili VAR kesin eşitsizlik kullandığı için eşitlikte (ölçü sıfır) PUAN4 0,5 iken VAR YOK olabilir"
 },
 "tekil": "aynı hissede VAR sonları birbirine < 15 mum olan zincir = bir olay; olay = kümenin en yüksek PUAN4'lü hizası",
 "sentetik": {
  "kok": 25112071,
  "tohum": 200,
  "gurultu": [
   0.0,
   0.1,
   0.2
  ],
  "baglam": [
   "dip",
   "yatay"
  ],
  "uretec": [
   "blok",
   "ry"
  ],
  "tol": 3,
  "negatif": {
   "n1": "fitilsiz büyük gövde (MV n1)",
   "n2": "fitiller ters (MV n2)",
   "n3": "mumlar 2 kat (MV n3)",
   "n5": "aynı mumlar yatay yol (MV p1)",
   "n6": "V dönüş: ön kısım kapanışları şablonun ilk kapanışından ön kısmın en düşük kapanışına doğrusal (tek yönlü iniş, gel-git yok), sonra 10 mumda şablonun son kapanışına doğrusal sert yükseliş; mum biçimleri şablonun",
   "n7": "üst bandın dışından yürüyüş: mum 0-10 şablon; 11-19 kapanışları mum başına şablon tırmanışının ortalama adımının 3 katıyla yükselir, mumlar kapanış çevresinde 2 kat",
   "n8a": "SMA'yı kırmızı mumlu boşlukla aşma: mum 10 kırmızı, açılış kapanışın gövde boyu kadar üstünde (önceki kapanıştan boşluk)",
   "n8b": "SMA'yı tek dev mumla aşma: mum 10 yeşil, açılış = önceki kapanış, gövde = şablonun en büyük gövdesinin 4 katı; sonraki mumlar aynı fazla kadar yukarı kayar"
  },
  "yanlis": {
   "seri": 200,
   "n": 1000
  },
  "kabul_olcutu": "%10 gürültüde pozitif VAR payı (gerçek sonun +-3 barında VAR) >= %60 (iki bağlam x iki üretici birleşik); her negatifte VAR payı <= %5 (bütün gürültüler birleşik; n8a ve n8b ayrı ayrı); rastgele seride tekil VAR <= 0,3 / 1.000 bar (iki üretici ayrı). Geçmezse yazılır; tanım değişmez",
  "tani": "her negatif ve pozitif için hangi parçanın kaç kez düştüğü (gerçek son +-3 bar, en yüksek PUAN4'lü pencere) yazılır"
 },
 "sinama": {
  "set1": "cemal_mum_izi4_onay.json 'isaret' (EVET / HAYIR) + mum_izi4_onay_anahtar.json (24 sayfa)",
  "set2": "cemal_mum_izi6_etiket.json 'isaret' EVET / HAYIR (IKISI / YOK / BELIRSIZ karar dışı) + mum_izi6_anahtar.json; katman 'T' (tekrar) sayfaları set 2'de sayılmaz",
  "pencere": "sayfadaki bölgenin kendisi (aynı uzunluk m, aynı son); v4 VAR / YOK ve PUAN4 o pencerede",
  "kappa": "Cohen kappa (v4 VAR ile Cemal EVET); bootstrap %95 (sayfalar yerine koyarak, B 5000, tohum 25112072; kappa tanımsız örnekler atılır, sayısı yazılır); uyum payı; 2x2",
  "auc": "PUAN4 AUC = P(PUAN4 EVET > PUAN4 HAYIR) + 0,5 eşit; bootstrap %95 (grup içi, B 5000, tohum 25112072); tam permütasyon p",
  "ayri": "set 1, set 2, birleşik; günlük / haftalık ayrı (bilgi)",
  "dusus": "Cemal EVET / v4 YOK sayfalarında hangi parça (yapı, E1, E2, E3 ve alt koşulları, E4) kaç kez düştü; Cemal HAYIR / v4 VAR sayısı",
  "bilgi_esnek": "bilgi (hüküm dışı): aynı sayfanın son +-3 barında biten 16-24 uzunluklu pencerelerde en yüksek PUAN4 ve VAR",
  "hukum": "birleşik: v4 VAR sayısı < 5 -> 'kural çok dar: ÖLÇÜLEMEDİ' (AUC yine yazılır); kappa >= 0,60 VE alt uç >= 0,40 -> UYUMLU; değilse kappa >= 0,40 -> KISMEN; kappa < 0,40 -> UYUMSUZ",
  "esik": {
   "var_en_az": 5,
   "uyumlu": 0.6,
   "alt_uc": 0.4,
   "kismen": 0.4
  },
  "B": 5000,
  "tohum": 25112072
 },
 "tarama": {
  "yalniz": "C hükmü UYUMLU",
  "gunluk": [
   "2016-01-01",
   "2022-12-31"
  ],
  "haftalik": [
   "2001-01-01",
   "2022-12-31"
  ],
  "evren": "ABD / AVR P2 (MUM_IZI_ETIKET2.e6_p2_maske; günlük açık kopya, haftalık 2001-15 p1 / 2016-22 açık kopya), BIST işlem değeri aynı gün / ISO haftası kesit medyanı üstü; olay sonu barında",
  "sayim": "tekil v4 VAR olay sayısı pazar x zaman dilimi (evren içi ve hepsi)",
  "onay": {
   "tohum": 25112073,
   "gunluk": 12,
   "haftalik": 12,
   "secim": "evren içi tekil VAR olaylarından RASTGELE; hisse başına bir; önceki iki setin hisseleri hariç; sayfa sırası karışık",
   "esik": "24'ün >= 19'u ✓"
  }
 }
}
```

## Sentetik (B; etiketlerden bağımsız)

- pozitif VAR payı: {'0.0': 0.29125, '0.1': 0.22375, '0.2': 0.1175} (bağlam {'dip': 0.29333333333333333, 'yatay': 0.12833333333333333}; parça geçme payları {'yapi': 0.5708333333333333, 'E1': 0.4066666666666667, 'E2': 0.5108333333333334, 'E3': 0.28708333333333336, 'E4': 0.7354166666666667})
- n1: VAR 0.0 % (parça geçme payları {'yapi': 0.19166666666666668, 'E1': 0.05375, 'E2': 0.16041666666666668, 'E3': 0.0, 'E4': 0.0})
- n2: VAR 0.0 % (parça geçme payları {'yapi': 0.33416666666666667, 'E1': 0.1775, 'E2': 0.29, 'E3': 0.08583333333333333, 'E4': 0.005})
- n3: VAR 3.4 % (parça geçme payları {'yapi': 0.39791666666666664, 'E1': 0.16958333333333334, 'E2': 0.3491666666666667, 'E3': 0.06833333333333333, 'E4': 0.7095833333333333})
- n5: VAR 0.0 % (parça geçme payları {'yapi': 0.13916666666666666, 'E1': 0.0275, 'E2': 0.049166666666666664, 'E3': 0.0, 'E4': 0.6645833333333333})
- n6: VAR 3.1 % (parça geçme payları {'yapi': 0.21041666666666667, 'E1': 0.15958333333333333, 'E2': 0.17333333333333334, 'E3': 0.055, 'E4': 0.6991666666666667})
- n7: VAR 11.4 % (parça geçme payları {'yapi': 0.47291666666666665, 'E1': 0.25916666666666666, 'E2': 0.3925, 'E3': 0.21041666666666667, 'E4': 0.6966666666666667})
- n8a: VAR 6.1 % (parça geçme payları {'yapi': 0.3975, 'E1': 0.24375, 'E2': 0.24875, 'E3': 0.12708333333333333, 'E4': 0.66})
- n8b: VAR 6.2 % (parça geçme payları {'yapi': 0.3975, 'E1': 0.27958333333333335, 'E2': 0.36791666666666667, 'E3': 0.08083333333333333, 'E4': 0.33208333333333334})
- rastgele: {'blok': {'n_bar': 205200, 'tekil': 37, 'VAR_1000': 0.18031189083820662}, 'ry': {'n_bar': 205200, 'tekil': 61, 'VAR_1000': 0.297270955165692}}
- KABUL ÖLÇÜTÜ: GEÇMEDİ {'poz_g10_ge_60': False, 'neg_le_5': {'n1': True, 'n2': True, 'n3': True, 'n5': True, 'n6': True, 'n7': False, 'n8a': False, 'n8b': False}, 'rastgele_le_03': {'blok': True, 'ry': True}, 'gecti': False}

- Tanı (bilgi; tanım değişmez; 100 tohum x 2 üretici x 2 bağlam, %10 gürültü, gerçek sonun +-3 barındaki en yüksek PUAN4'lü pencere): pozitiflerde yapı koşulu yalnız %56'sında var (ilk SMA üstü kapanış ön kısmı 3..m/2 aralığına düşmüyor: gömülen kalıbın esnemesi ve bağlam mumları); yapı varken alt koşul geçme payları: E1 bC ort %78, E1 değişim %98, E2 %96-100, E3 içeriden %84, gövde medyanı %86, en büyük gövde %74, Spearman %82, son bC %93, örtüşme %100, E4 %83. n7 / n8a / n8b'de bantlar sentetik seriden yeniden hesaplandığı için ilk SMA üstü kapanış çoğu zaman kalıbın 10. mumu olmuyor; kırmızı çıkış ya da dev mum başka bir hizada çıkış mumu olmaktan çıkıyor (n8a'da yeşil çıkış koşulu en iyi pencerede %70 geçiyor). Ders (EK 5 HATA 4 tekrarı): negatif kurgu sentetik bant içinde kendi ölçüsünde sınanmadan negatif sayılmamalı.
- Kural gereği: sentetik geçmedi diye tanım değişmez; C iş tanımındaki sırayla koşulur. Pozitif yakalama %22 olduğu için C'de v4 VAR sayısının çok az çıkması (< 5 -> ÖLÇÜLEMEDİ) önceden beklenen bir sonuçtur.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | negatifler sentetikte sayıyla (n1, n2, n3, n5, n6, n7, n8a, n8b + rastgele seri), kabul ölçütü önceden; sınamada kappa bootstrap ve AUC permütasyonu; getiri / eş yok |
| K2 | geleceğe bakma | EVET | b her mumun kendi gününe kadarki bantla; v4_tara_seri sonu t olan pencerede yalnız <= t barları kullanır (test: seri t'de kesilince aynı); veri <= 2022-12-31 + KASA kapısı (tarama); etiketler ön kayıt commit'inden sonra açılır |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (V3 kuralı); BIST işlem değeri kesit medyanı üstü; ABD / AVR P2 |
| K4 | tekilleştirme | EVET | tekil: < 15 mum zincir = bir olay, en yüksek PUAN4; sınamada tekrar sayfaları set 2'de sayılmaz (çift sayım yok) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok |
| K6 | veri birimi | EVET | b birimi ölçek bağımsız; örtüşme ve fitil oranları oransal |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; sayım ve görsel onay (getiri yok) |
| K8 | örneklem ve dönem | EVET | set 1 24 + set 2 (tekrar hariç) karar sayfaları; v4 VAR < 5 ise ÖLÇÜLEMEDİ; aralıklar raporda |
| K9 | ön kayıt | EVET | MUM_IZI7_ON_KAYIT.md: KOD7_SHA, ESIK7_SHA, SABLON7_SHA, SENTETIK7_SHA + eski kod sha'ları; v4_kapi (kontrol + sha + git) sınama ve tarama öncesi |
| K10 | ayrıştırma | EVET | sayfa pencereleri anahtarlardan (hisse / son / m / zaman); set 1 sayfalarında v1 S anahtardaki S ile aynı (denetim); etiket şeması ('isaret' EVET / HAYIR / YOK / IKISI / BELIRSIZ) bilinmeyen değerde DUR |
| K11 | yeniden üretim | EVET | v4_duz: tek pencerede E1-E4 ve PUAN4 düz döngüyle yeniden; test ve sınamada vektörlü sonuçla aynı |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kappa eşikleriyle; commit mesajında etiket-sayfa eşlemesi yok; 'iz' sözü yok |
| K13 | süreç | EVET | çakışma kapısı; eski kodlar / defterler / UC_IZ2 / başka ajanın mum_izi6 olc dosyaları değişmez, git add edilmez |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

(ön kayıt anında yok)
