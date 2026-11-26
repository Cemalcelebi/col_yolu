# MUM_IZI8 ÖN KAYIT (2026-11-26T07:14:43Z)

v5: etiketlerle (61 karar) önceden yazılı 8 aday arasından önceden yazılı seçim kuralıyla seçilen evre kuralı; NİHAİ KURAL v5M = seçilen kural ∧ M (Cemal'in 26 Kasım kesin şartı: küçük gövde, alt fitil az / yok, üst fitil uzun; sözle kondu, etiketle seçilmedi). Bu dosya evren taramasından ve PDF'ten ÖNCE commit edilir; sonra kural, eşik ve onay seçimi değişmez. Seçim iç örnektir (ezber riski); gerçek sınama Cemal'in MUM_IZI8_ONAY.pdf işaretleri.

## Mühürler

KOD8_SHA: af74ac0e74ba71b20699b56b89a4ea7fddc1bc7e8dcf2905e0e9cac19d93595f
ESIK8_SHA: 02b79be4d17ee09dba328bf36878c34a319414ac1f64093c17a3b4c3a1ae6e87
ADAY8_SHA: 89a48a0385bffe8e8b96fc7632e4830ae092cf8a73b669f9f02419f9e4830e97
SENTETIK8_SHA: 61979e76dd301033aa5c26447cebaf294bea99f6eaf49c678fd4a4347e8ea76d
SENTETIK8M_SHA: 16eef3e555fa4eb9846b1be11faef41bd86f12fd0ffda7a656abc3179391c724
V4_KOD_SHA: 6b3e2e4fa74f9cde3b4e99c1b47c8f4b9c31765cc604d478e5699bf2768cafbe
V3_KOD_SHA: 70fc2fb979c47b2a2bd5fb260e1fb1891e7b34268f49c4a4276f482b66a4eb69
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
E6_KOD_SHA: cc8c6c914d7ecaa02682eb9c302e63635e567a1d828f7416a0cbb6bdeb291f1d
ETIKET_CSV_SHA: 8fb91d4ad284aacbb893fc33b85efe4f993b46fd094569f7cee353546796da82

- MUM_IZI_V5.py commit'i: 5ee48cb454915740b46f08690cf391a095128e3d 2026-11-26T07:14:41+00:00

## Aday tablosu (61 etiket; 16 EVET) + nihai v5M

| kural | parça | VAR | EVET-VAR | isabet | yakalama | kappa (%95) | set 1 kappa | set 2 kappa |
|---|---|---|---|---|---|---|---|---|
| R1 | 3 | 26 | 10 | 0.38 | 0.62 | 0.224 (-0.01..0.46) | 0.070 | 0.323 |
| R2 | 4 | 10 | 4 | 0.40 | 0.25 | 0.133 (-0.12..0.39) | 0.070 | 0.159 |
| R3 | 4 | 17 | 8 | 0.47 | 0.50 | 0.294 (0.03..0.54) | 0.339 | 0.275 |
| R4 | 5 | 15 | 8 | 0.53 | 0.50 | 0.352 (0.08..0.61) | 0.423 | 0.317 |
| R5 | 5 | 11 | 5 | 0.45 | 0.31 | 0.199 (-0.07..0.46) | 0.192 | 0.206 |
| R6 | 6 | 10 | 5 | 0.50 | 0.31 | 0.229 (-0.04..0.49) | 0.273 | 0.206 |
| R7 | 7 | 7 | 4 | 0.57 | 0.25 | 0.224 (-0.04..0.49) | 0.273 | 0.186 |
| R8 | 7 | 3 | 2 | 0.67 | 0.12 | 0.139 (-0.06..0.38) | 0.273 | 0.000 |
| R4+M (v5M, nihai) | 6 | 5 | 4 | 0.80 | 0.25 | 0.293 (0.03..0.55) | 0.423 | 0.159 |

- Seçim: {"secilen": "R4", "durum": "SEÇİLDİ", "kappa": 0.3515237420269312, "kmax": 0.3515237420269312, "yakin": ["R4"], "uygun": ["R1", "R2", "R3", "R4", "R5", "R6"]}
- Çapraz set (bilgi): {"set1_sec_set2_sina": {"var_en_az": 4, "secilen": "R4", "durum": "SEÇİLDİ", "kappa_secim_seti": 0.42307692307692285, "kappa_obur_set": 0.31734317343173424}, "set2_sec_set1_sina": {"var_en_az": 5, "secilen": "R1", "durum": "SEÇİLDİ", "kappa_secim_seti": 0.32317073170731697, "kappa_obur_set": 0.06976744186046535}}

## M (mum yapısı) Cemal'in kendi işaretlerinde (geçme payı EVET / HAYIR; medyan değer EVET / HAYIR)

- M: geçme 50 % / 36 %
- m1: geçme 69 % / 60 %; medyan 0.397 / 0.413
- m2: geçme 81 % / 62 %; medyan 0.215 / 0.234
- m3: geçme 56 % / 49 %; medyan 0.339 / 0.324
- m4: geçme 69 % / 40 %; medyan 1.655 / 1.242
- Şablon M değerleri: m1 0.379 (<= 0,45), m2 0.203 (<= 0,25), m3 0.419 (>= 0,33), m4 3.593 (>= 1,5; toplam üst / toplam alt fitil); M True. Şablon bütün parçalar: {'Y': True, 'G1': True, 'G2': True, 'T': True, 'I': True, 'B': True, 'F': True, 'S': True, 'M': True}

## Sentetik: seçilen aday kural R4 = Y ∧ G1 ∧ G2 ∧ T ∧ I (bilgi)

- pozitif VAR: {'0.0': 0.51375, '0.1': 0.52, '0.2': 0.4975} (bağlam {'dip': 0.6925, 'yatay': 0.3283333333333333}; gömülü pencerede parça geçme {'Y': 0.48541666666666666, 'G1': 0.28541666666666665, 'G2': 0.42625, 'T': 0.47708333333333336, 'I': 0.48125, 'B': 0.42791666666666667, 'F': 0.45125})
- n1: kendi ölçüsü B ihlal payı 99.8 % -> GEÇERLİ; VAR 47.3 %
- n3: kendi ölçüsü B ihlal payı 69.3 % -> KURGU GEÇERSİZ; VAR 43.4 %
- n5: kendi ölçüsü T ihlal payı 98.8 % -> GEÇERLİ; VAR 1.2 %
- n6: kendi ölçüsü G1 ihlal payı 68.0 % -> KURGU GEÇERSİZ; VAR 19.4 %
- n7: kendi ölçüsü I ihlal payı 43.3 % -> KURGU GEÇERSİZ; VAR 44.7 %
- n8a: kendi ölçüsü G2 ihlal payı 73.2 % -> KURGU GEÇERSİZ; VAR 28.9 %
- n8b: kendi ölçüsü çıkış mumu gövdesi > 0,9 (b) ihlal payı 71.7 % -> KURGU GEÇERSİZ; VAR 44.5 %
- rastgele: {'blok': {'n_bar': 205200, 'tekil': 1590, 'VAR_1000': 7.748538011695906}, 'ry': {'n_bar': 205200, 'tekil': 1821, 'VAR_1000': 8.874269005847953}}
- KABUL ÖLÇÜTÜ: GEÇMEDİ {"poz_g10": true, "neg": {"n1": false, "n3": "geçersiz kurgu (sayılmaz)", "n5": true, "n6": "geçersiz kurgu (sayılmaz)", "n7": "geçersiz kurgu (sayılmaz)", "n8a": "geçersiz kurgu (sayılmaz)", "n8b": "geçersiz kurgu (sayılmaz)"}, "rastgele": {"blok": false, "ry": false}, "gecti": false}

## Sentetik: NİHAİ v5M R4+M = Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ M

- pozitif VAR: {'0.0': 0.49375, '0.1': 0.45375, '0.2': 0.30625} (bağlam {'dip': 0.57, 'yatay': 0.2658333333333333}; gömülü pencerede parça geçme {'Y': 0.48541666666666666, 'G1': 0.28541666666666665, 'G2': 0.42625, 'T': 0.47708333333333336, 'I': 0.48125, 'B': 0.42791666666666667, 'F': 0.45125, 'M': 0.7670833333333333})
- n1: kendi ölçüsü B ihlal payı 99.8 % -> GEÇERLİ; VAR 0.0 %
- n2: kendi ölçüsü M ihlal payı 100.0 % -> GEÇERLİ; VAR 0.0 %
- n3: kendi ölçüsü B ihlal payı 70.4 % -> KURGU GEÇERSİZ; VAR 36.6 %
- n5: kendi ölçüsü T ihlal payı 99.2 % -> GEÇERLİ; VAR 0.9 %
- n6: kendi ölçüsü G1 ihlal payı 67.7 % -> KURGU GEÇERSİZ; VAR 14.9 %
- n7: kendi ölçüsü I ihlal payı 45.4 % -> KURGU GEÇERSİZ; VAR 35.5 %
- n8a: kendi ölçüsü G2 ihlal payı 74.1 % -> KURGU GEÇERSİZ; VAR 21.4 %
- n8b: kendi ölçüsü çıkış mumu gövdesi > 0,9 (b) ihlal payı 71.9 % -> KURGU GEÇERSİZ; VAR 34.0 %
- rastgele: {'blok': {'n_bar': 205200, 'tekil': 96, 'VAR_1000': 0.4678362573099415}, 'ry': {'n_bar': 205200, 'tekil': 95, 'VAR_1000': 0.46296296296296297}}
- KABUL ÖLÇÜTÜ: GEÇMEDİ {"poz_g10": false, "neg": {"n1": true, "n2": true, "n3": "geçersiz kurgu (sayılmaz)", "n5": true, "n6": "geçersiz kurgu (sayılmaz)", "n7": "geçersiz kurgu (sayılmaz)", "n8a": "geçersiz kurgu (sayılmaz)", "n8b": "geçersiz kurgu (sayılmaz)"}, "rastgele": {"blok": true, "ry": true}, "gecti": false}

## Uygulama kararları (iş tanımında açık bırakılanlar)

1. Pencere uzunlukları 16-24 (dokuzu); bir son, uzunluklardan biri VAR ise VAR. k = penceredeki ilk SMA üstü kapanış; Y: 3 <= k <= floor(0,6 x m), çıkıştan sonra (k+1..m-1) >= 5 mum.
2. 'Çıkıştan sonraki' her ölçü k+1..m-1 mumlarında (çıkış mumu hariç). T: fiyat kapanışlarının sıra numarasıyla Spearman'ı (eşitlerde ortalama sıra) ve pencerenin son kapanışı bC. I: son 3 mum muafiyeti YOK. B: gövde |bC - bO| (bant yarı genişliği birimi). F: üst fitil > alt fitil (kesin).
3. M bölgenin BÜTÜN mumlarında; m4 = toplam üst fitil / toplam alt fitil (alt toplamı 0 ise sonsuz). Şablonda m4 = 3,59 (ana modelin notundaki '~2,96' başka bir oranla hesaplanmış olmalı; tanım 'toplam / toplam' aynen uygulandı; şablon iki hesapta da 1,5'i geçiyor).
4. S = MI.mi_S_pencere (tam şablon, kalibre); eşik 0,59.
5. Etiket eşlemesi mum_izi7_sinama.csv (61 karar; tekrar sayfaları ve YOK / IKISI / BELIRSIZ zaten dışarıda); pencere = sayfanın kendi penceresi (anahtardan). Set 1'de v1 S anahtardaki S ile aynı denetlendi.
6. Kappa bootstrap'ı sayfalar yerine koyarak (B 5000, tohum 25112081), tanımsız örnekler atılır. Seçimde 'fark < 0,03' = en yüksek kappadan 0,03'ten az geride olanlar; aralarında en az parçalı. DUR: seçilenin kappası <= 0,20.
7. Çapraz set (bilgi): tek sette VAR en az = tavan(8 x n_set / 61) (set 1: 4; set 2: 5).
8. Sentetik negatiflerin 'kendi ölçüsü' gömülü pencerenin kendisinde (sentetik bant) pencerenin kendi k'sıyla, Y sınırları aranmadan; k yoksa ihlal; tohumların >= %80'inde ihlal -> GEÇERLİ. Hedefler: n1 B, n2 M, n3 B, n5 T, n6 G1, n7 I, n8a G2, n8b çıkış mumu gövdesi > 0,9. n8 iki ayrı negatif (n8a kırmızı boşluklu, n8b tek dev mum).
9. Tarama: tekil = < 15 mum zinciri, en yüksek v1 S'li hiza (S bütün VAR pencerelerinde hesaplanır); sayım hem R4 hem v5M için.
10. Onay: YALNIZ v5M VAR (evren içi) olaylarından RASTGELE (tohum 25112083); önce haftalık sonra günlük (hisse başına bir, iki dilim birlikte); önceki iki setin hisseleri hariç; BIST dilim başına <= 4; dilimde 12'den az uygun olay varsa hepsi; toplam < 8 ise DUR (PDF yok). Sayfa 1 kapak, 2 şablonda okuma, bölgeler 3'ten başlar.
11. PDF okuması: mavi şerit = 0..k-1 (gel-git kısmı), yeşil ok = çıkış mumu k, turuncu şerit = k+1..m-1 (tırmanış); şeritler yarı saydam, mumların arkasında; bölge kutusu çizilmez (şeritler bölgeyi gösterir); M'nin dört sayısı her bölgede küçük yazıyla.

## Cemal'in EK şartı (26 Kas, iş sürerken; ana model iletti)

"Mum yapısı küçük, altta fitil az ya da yok, üstte uzun fitil; mum bu şekilde KESİN." M zorunlu kapı olarak eklendi: R1-R8 aday tablosu ve seçim aynen (seçim M'den önce yapılmıştı, M eklenince yeniden hesaplandı ve AYNI çıktı); nihai kural v5M = R4 ∧ M. M etiketle seçilmedi; eşikler (0,45 / 0,25 / 0,33 / 1,5) ana modelin yazdığı sabitler.

## Beklenti (onay seti)

- 61 etikette v5M isabeti 0,80 (5 VAR'ın 4'ü EVET) ama n küçük (aralık geniş); R4 isabeti 0,53 (15 VAR). Cemal kendi tekrarlarında 8'de 6 (%75) aynı diyor.
- Kaba beklenti: 24 sayfanın %45-65'i ✓ (isabet x tutarlılık civarı); 19 / 24 (%79) beklenmiyor ama dışlanmıyor. Sentetik pozitif ölçütü (v5M %45 < %50) geçmedi; kapakta yazılır.
- Not: Cemal'in KENDİ 16 EVET sayfasının yalnız %50'si M'yi geçiyor (HAYIR'larda %36): sözle konan kesin şart kendi işaretlerinin yarısını dışarıda bırakıyor.

## Kural, eşikler, onay seçimi (V5_ESIK; sha yukarıda)

```
{
 "surum": "V5-1.0",
 "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20); Bollinger (20, 2), her mum kendi gününe kadarki barlarla; üst bant <= SMA olan pencere geçersiz",
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
 "parca": {
  "Y": "k = pencerede ilk SMA üstü kapanış (0'dan); 3 <= k <= floor(0,6 x m) ve çıkıştan sonra (k+1..m-1) en az 5 mum",
  "G1": "v4 E1 aynen: ön kısım (0..k-1) bC ortalaması <= -0,3 ve fiyat kapanış yönü (ön kısım içindeki çiftler) en az 2 kez değişiyor",
  "G2": "v4 E2 aynen: çıkış mumu yeşil (C > O), önceki kapanış bC < 0, çıkıştan sonraki kapanışların >= %80'i bC > 0",
  "T": "çıkıştan sonraki FİYAT kapanışlarının sıra numarasıyla Spearman korelasyonu (eşitlerde ortalama sıra) >= 0,5 ve pencerenin son kapanışı bC >= 0,6",
  "I": "çıkıştan sonraki kapanışların >= %60'ı bC <= 1,05",
  "B": "çıkıştan sonraki gövdelerin (|bC - bO|, bant yarı genişliği birimi) en büyüğü <= 0,9 ve medyanı <= 0,30",
  "F": "çıkıştan sonraki mumlarda üst fitili alt fitilinden uzun olanların payı >= %50",
  "S": "v1 benzerlik puanı (MI.mi_S_pencere, tam şablon, kalibre) >= 0,59",
  "M": "MUM YAPISI (Cemal 26 Kas, sözle kondu, etiketle seçilmedi; bölgenin BÜTÜN mumları): m1 ortalama gövde / mum boyu <= 0,45; m2 ortalama alt fitil / mum boyu <= 0,25; m3 ortalama üst fitil / mum boyu >= 0,33; m4 toplam üst fitil / toplam alt fitil >= 1,5 (alt fitil toplamı 0 ise sonsuz); M = dördü birden"
 },
 "esik": {
  "k_ust": 0.6,
  "en_az_sonra": 5,
  "G1_ort": -0.3,
  "G1_degisim": 2,
  "G2_ust": 0.8,
  "T_spearman": 0.5,
  "T_son": 0.6,
  "I_pay": 0.6,
  "I_ust": 1.05,
  "B_max": 0.9,
  "B_med": 0.3,
  "F_pay": 0.5,
  "S": 0.59,
  "m1": 0.45,
  "m2": 0.25,
  "m3": 0.33,
  "m4": 1.5
 },
 "kural": {
  "R1": "Y ∧ G1 ∧ G2",
  "R2": "Y ∧ G1 ∧ G2 ∧ S",
  "R3": "Y ∧ G1 ∧ G2 ∧ T",
  "R4": "Y ∧ G1 ∧ G2 ∧ T ∧ I",
  "R5": "Y ∧ G1 ∧ G2 ∧ T ∧ B",
  "R6": "Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ B",
  "R7": "Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ B ∧ F",
  "R8": "Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ B ∧ S"
 },
 "nihai": "v5M = seçilen aday kural ∧ M (Cemal'in kesin şartı; sözle kondu, etiketle seçilmedi); 61 etikette hem seçilen kural hem v5M raporlanır; EVET / HAYIR sayfalarında M ve m1-m4 geçme payları",
 "pencere_sonu": "bir son, uzunluklardan biri VAR ise VAR",
 "etiket": "61 karar etiketi (mum_izi7_sinama.csv: set, sayfa, zaman, cemal); pencere anahtarlardan (set 1 mum_izi4_onay_anahtar.json, set 2 mum_izi6_anahtar.json); sayfanın kendi penceresi (aynı m, aynı son)",
 "aday": {
  "olcu": "VAR, 2x2, isabet (VAR içinde EVET), yakalama (EVET içinde VAR), kappa + bootstrap %95 (sayfalar yerine koyarak, B 5000, tohum 25112081); set 1 / set 2 ayrı",
  "B": 5000,
  "tohum": 25112081
 },
 "secim": {
  "kural": "61 etikette VAR >= 8 olan adaylar içinde en yüksek kappa; kappası en yüksekten 0,03'ten az geride olanlar arasında en az parçalı (eşit parçada yüksek kappa); seçilenin kappası <= 0,20 ise (ya da uygun aday yoksa) DUR, PDF yok",
  "var_en_az": 8,
  "fark": 0.03,
  "kappa_en_az": 0.2,
  "capraz": "bilgi: aynı kural tek sette (VAR en az = tavan(8 x n_set / 61)) seçilir, öteki sette kappası yazılır"
 },
 "sentetik": {
  "kok": 25112082,
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
   "n2": "fitiller ters (MV n2; yalnız v5M sentetiğinde)",
   "n3": "mumlar 2 kat (MV n3)",
   "n5": "aynı mumlar yatay yol (MV p1)",
   "n6": "V dönüş (MUM_IZI_V4.v4_karsi n6: tek yönlü iniş, gel-git yok)",
   "n7": "üst bandın dışından büyük mumlarla (V4 n7)",
   "n8a": "kırmızı boşluklu çıkış (V4 n8a)",
   "n8b": "tek dev mumla çıkış (V4 n8b)"
  },
  "kendi_olcu": {
   "n1": "B",
   "n2": "M",
   "n3": "B",
   "n5": "T",
   "n6": "G1",
   "n7": "I",
   "n8a": "G2",
   "n8b": "çıkış mumu gövdesi > 0,9 (b)"
  },
  "dogrulama": "her negatifte gömülü pencerenin kendisinde (son = gerçek son, m = gömülü uzunluk; sentetik bantla) hedef koşul pencerenin kendi k'sıyla (Y sınırları aranmadan) hesaplanır; k yoksa ihlal sayılır; tohumların >= %80'inde ihlal varsa negatif GEÇERLİ, yoksa 'negatif kurgusu geçersiz' (sayılmaz)",
  "gecerli_pay": 0.8,
  "yanlis": {
   "seri": 200,
   "n": 1000
  },
  "kabul_olcutu": "%10 gürültüde pozitif VAR (gerçek sonun +-3 barında, 16-24 uzunluk) >= %50 (iki bağlam x iki üretici); geçerli her negatifte VAR <= %10 (bütün gürültüler); rastgele seride tekil VAR <= 1 / 1.000 bar (iki üretici ayrı). Geçmezse yazılır, kural değişmez; PDF kapağında 'sentetik ölçütü geçmedi' yazar",
  "esik": {
   "poz": 0.5,
   "neg": 0.1,
   "rastgele": 1.0
  }
 },
 "tarama": {
  "gunluk": [
   "2016-01-01",
   "2022-12-31"
  ],
  "haftalik": [
   "2001-01-01",
   "2022-12-31"
  ],
  "evren": "ABD / AVR P2 (MUM_IZI_ETIKET2.e6_p2_maske; günlük açık kopya, haftalık 2001-15 p1 / 2016-22 açık kopya), BIST işlem değeri aynı gün / ISO haftası kesit medyanı üstü (olay sonu barında); geçerli bar; haftalıkta eksik haftalı pencere yok",
  "tekil": "aynı hissede VAR sonları < 15 mum zinciri = bir olay; olay = kümenin en yüksek v1 S'li hizası (uzunluklar içinde en yüksek S)",
  "sayim": "tekil v5 VAR olay sayısı pazar x zaman dilimi (evren içi ve hepsi); hisse-yıl başına sıklık = olay / (bar / 252 günlük, / 52 haftalık)"
 },
 "onay": {
  "tohum": 25112083,
  "gunluk": 12,
  "haftalik": 12,
  "bist_tavan": 4,
  "kural": "YALNIZ v5M VAR bölgeleri; bir dilimde 12'den az uygun olay varsa hepsi (sayı yazılır); toplam < 8 ise DUR (PDF yok)",
  "en_az": 8,
  "secim": "evren içi tekil v5 VAR olaylarından RASTGELE (S'ye göre değil); hisse başına bir; önceki iki setin hisseleri hariç; BIST dilim başına <= 4; önce haftalık sonra günlük; sayfa sırası tohumla karışık",
  "sayfa": "s1 KOD NASIL TESPİT EDİYOR (<= 8 satır, Cemal'in cümlesiyle + 61 işaretle uyum + tekrar uyumu); s2 Cemal'in kalıbı üstünde kodun okuması (mavi gel-git şeridi, yeşil ok çıkış mumu, turuncu tırmanış şeridi; parça sayıları); s3-26 bölgeler: solda küçük 'Senin kalıbın', sağda bölge (öncesi 15 mum, Bollinger 20 + SMA20, bölge sonunda kesik) ve üstünde kodun okuması (aynı renkler, yarı saydam, mumların arkasında); altta ✓ / × kutuları ve 'yanlış okunan parçayı daire içine al'; hisse / tarih / sonrası yok",
  "esik": "24'ün >= 19'u ✓ -> tespit GEÇERLİ"
 }
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | aday tablosunda kappa bootstrap; negatifler sentetikte kendi ölçüsünde doğrulanıp sayılır; rastgele seri tabanı; getiri / eş yok |
| K2 | geleceğe bakma | EVET | b her mumun kendi gününe kadarki bantla; v5_tara_seri sonu t olan pencerede <= t barları (test); veri <= 2022-12-31 + KASA kapısı (tarama) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır; BIST işlem değeri kesit medyanı üstü; ABD / AVR P2 |
| K4 | tekilleştirme | EVET | tekil < 15 mum zincir, en yüksek v1 S; etiketlerde tekrar sayfaları zaten dışarıda (mum_izi7_sinama.csv) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok |
| K6 | veri birimi | EVET | b birimi ölçek bağımsız; gövde sınırı bant yarı genişliğine göre |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; yalnız sayım ve görsel onay |
| K8 | örneklem ve dönem | EVET | 61 etiket iç örnek (ezber riski raporda); çapraz set bilgisi; gerçek sınama yeni PDF işaretleri |
| K9 | ön kayıt | EVET | MUM_IZI8_ON_KAYIT.md: KOD8, ESIK8, ADAY8, SENTETIK8 sha + eski kod sha'ları; v5_kapi (kontrol + sha + git) tarama öncesi |
| K10 | ayrıştırma | EVET | etiket eşlemesi mum_izi7_sinama.csv'den, sayı denetimi (61; 16 EVET); pencereler anahtarlardan; set 1'de v1 S anahtardaki S ile aynı |
| K11 | yeniden üretim | EVET | v5_duz: tek pencerede parçalar düz döngüyle; 61 sayfada vektörlü sonuçla aynı (fark -> DUR) |
| K12 | ifade | EVET | seçim yalnız önceden yazılı kuralla; 'iz' sözü yok; iç örnek uyarısı |
| K13 | süreç | EVET | çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

- Aday tablosu ve R4 sentetiği M eklenmeden önce koşulup commit edildi (31be2c2); Cemal'in EK şartı gelince ön kayıt henüz commit edilmemişti: taslak silindi, M kodlandı, aday tablosu yeniden üretildi (R1-R8 tablosu, seçim ve çapraz set birebir aynı; denetlendi), v5M sentetiği koşuldu (5ee48cb), bu ön kayıt sonra yazıldı.
