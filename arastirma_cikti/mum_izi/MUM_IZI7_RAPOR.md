# MUM_IZI7 RAPOR (2026-11-25): v4 evre kuralı (Cemal'in kapak notu), sentetik, mühürlü etiketlerle sınama

İş tanımı: MUM_IZI7_IS_TANIMI.md (2e79fa3). Ön kayıt: MUM_IZI7_ON_KAYIT.md (9fafd70, 21:06:10Z); etiketler ilk kez 21:06:19Z'de açıldı. Kod: MUM_IZI_V4.py,
test_mum_izi7.py (11 / 11). GETİRİ / SONRASI YOK. Veri <= 2022-12-31.

## SONUÇ (tek bakışta)

- v4 61 karar sayfasının (set 1: 24, set 2: 37; 16 EVET / 45 HAYIR) HİÇBİRİNE 'VAR' demedi -> hüküm (önceden yazılı): ÖLÇÜLEMEDİ (kural çok dar; v4 VAR 0 < 5).
- PUAN4 AUC birleşik 0,503 (%95 0,42-0,60; p 0,57); set 1 0,441; set 2 0,550. Dereceli puan da Cemal'in EVET'ini ayırmıyor.
- Cemal'in 16 EVET sayfasının 16'sında E3 (üst banda içeriden boncuk gibi düzenli tırmanış) düştü; E4 (çoğu mumda uzun üst fitil) 9'unda, E2 5'inde, E1 4'ünde, yapı 1'inde.
- Sentetik kabul ölçütü de GEÇMEDİ: pozitif %10 gürültüde %22,4 (ölçüt >= %60); n7 %11,4, n8a %6,1, n8b %6,2 (> %5); öteki negatifler ve rastgele seri geçti.
- D (evren taraması, onay seti) yapılmadı (hüküm UYUMLU değil). Karar etiketi: TESPİT GEÇERSİZ / ÖLÇÜLEMEDİ.

## v4 TANIM (uygulama kararları ve şablonun dört parçadaki değerleri)

Eşikler iş tanımındaki sabitler (0,3; %80; 1,05; 1,5; 0,6; 0,75; %30; %50). Uygulama kararları (ön kayıtta 12 madde):
1. Uzunluk 16-24 (dokuzu); bir son, uzunluklardan biri VAR ise VAR; PUAN4 uzunluklar içinde en büyüğü.
2. Çıkış mumu k = pencerede bC > 0 olan ilk mum; ön kısım 0..k-1 (3 <= k <= floor(m / 2)); tırmanış k+1..m-1 (>= 5 mum). Yapı yoksa E1-E3 YOK (puan 0).
3. E1 yön = fiyat kapanış farkının işareti, ön kısım içindeki çiftler; değişim = ardışık yön çarpımı < 0.
4. E2 'çıkıştan sonra' = tırmanış kısmı; E3 (a) bölgenin son 3 mumu hariç.
5. E3 (b) gövde |bC - bO|; (c) Spearman eşitlerde ortalama sıra; (d) MI 'ortusme' tanımı, tırmanış kısmı içindeki çiftler.
6. Dereceli puan: g = 0,5 + (x - eşik) / (2 s), [0, 1]; parça = alt koşulların en küçüğü; PUAN4 = parçaların en küçüğü.

Şablon (Cemal'in kalıbı, görüntü bantları): k = 10 (ön kısım 10 mum = floor(20 / 2): SINIRDA), tırmanış 9 mum.
- E1: bC ortalaması -0,412 (<= -0,3), yön değişimi 6 (>= 2): GEÇTİ (puan 0,69).
- E2: çıkış mumu yeşil, önceki bC -0,109, tırmanışta SMA üstü %100: GEÇTİ (puan 1,0).
- E3: içeriden %100; gövde medyanı 0,1305 / en büyük 0,4503 (referansın kendisi); Spearman 0,70; son bC 0,905; örtüşme 0,702 (referans): GEÇTİ (puan 0,625).
- E4: uzun üst fitil payı 10 / 20 = %50 (eşik %50): GEÇTİ ama SINIRDA (puan 0,5).
- Şablon VAR, PUAN4 0,50.

## SENTETİK (etiketlerden önce; kök 25112071; 200 tohum x 2 üretici x 2 bağlam x 3 gürültü; başarı = gerçek sonun +-3 barında VAR)

| tür | VAR | gürültü 0 / 0,1 / 0,2 | dip / yatay |
|---|---|---|---|
| pozitif | %21,1 | 29,1 / 22,4 / 11,8 | 29,3 / 12,8 |
| n1 fitilsiz büyük gövde | %0 | 0 / 0 / 0 | |
| n2 fitiller ters | %0,04 | 0 / 0,1 / 0 | |
| n3 mumlar 2 kat | %3,4 | 2,9 / 4,8 / 2,6 | |
| n5 yatay yol | %0 | | |
| n6 V dönüş | %3,1 | 0,6 / 4,4 / 4,4 | |
| n7 üst bandın dışından | %11,4 | 13,8 / 12,3 / 8,1 | |
| n8a kırmızı boşluklu çıkış | %6,1 | 5,6 / 8,4 / 4,4 | |
| n8b tek dev mumla çıkış | %6,2 | 7,5 / 6,5 / 4,6 | |
| rastgele (tekil VAR / 1.000 bar) | blok 0,18; ry 0,30 | | |

- Ölçüt: pozitif >= %60 GEÇMEDİ (%22,4); negatiflerden n1, n2, n3, n5, n6 <= %5 GEÇTİ, n7 / n8a / n8b GEÇMEDİ; rastgele <= 0,3 GEÇTİ (ry 0,297 sınırda). Toplam: GEÇMEDİ. Tanım değişmedi.
- Tanı (bilgi): pozitiflerde en iyi pencerede yapı koşulu yalnız %56'sında var (gömülen kalıbın esnemesi ve bağlam mumları ilk SMA üstü kapanışı 3..m/2 aralığından çıkarıyor); yapı varken en çok düşen alt koşullar en büyük gövde (%74 geçer), E1 bC ortalaması (%78), Spearman (%82), E4 (%83). Şablon iki sınırda (E4 %50, k = m / 2) olduğu için küçük bozulmalar onu kuraldan çıkarıyor.
- n7 / n8a / n8b: bantlar sentetik seriden yeniden hesaplanınca ilk SMA üstü kapanış çoğu zaman kalıbın 10. mumu olmuyor; kırmızı / dev çıkış mumu başka hizada 'çıkış mumu' olmaktan çıkıyor. Bu kurgular sentetik bant içinde tam negatif değil (HATA 1).

## ETİKETLERLE SINAMA (C)

Etiketler: set 1 24 sayfa (EVET 7 / HAYIR 17); set 2 48 sayfa (EVET 13 / HAYIR 32 / IKISI 1 / BELIRSIZ 1 / YOK 1), tekrar 8 sayfa sayılmadı -> 37 karar sayfası
(EVET 9 / HAYIR 28). Birleşik 61 (EVET 16 / HAYIR 45).

| küme | n | Cemal EVET | v4 VAR | 2x2 (EVET-VAR / EVET-YOK / HAYIR-VAR / HAYIR-YOK) | uyum | kappa (%95) | PUAN4 AUC (%95; p) |
|---|---|---|---|---|---|---|---|
| birleşik | 61 | 16 | 0 | 0 / 16 / 0 / 45 | 0,738 | 0 (0-0) | 0,503 (0,42-0,60; 0,57) |
| set 1 | 24 | 7 | 0 | 0 / 7 / 0 / 17 | 0,708 | 0 (0-0) | 0,441 (0,35-0,50; 1,00) |
| set 2 | 37 | 9 | 0 | 0 / 9 / 0 / 28 | 0,757 | 0 (0-0) | 0,550 (0,42-0,71; 0,32) |
| günlük (bilgi) | 31 | 8 | 0 | 0 / 8 / 0 / 23 | 0,742 | 0 | 0,500 |
| haftalık (bilgi) | 30 | 8 | 0 | 0 / 8 / 0 / 22 | 0,733 | 0 | 0,494 (0,34-0,68) |

- Kappa 0: v4 hiçbir sayfaya VAR demediği için uyum (%74) yalnız HAYIR'ların payı; kappa tanım gereği 0.
- HÜKÜM: ÖLÇÜLEMEDİ (kural çok dar; v4 VAR 0 < 5). AUC yazıldı: 0,503, şansla aynı.
- Cemal EVET / v4 YOK (16 sayfa) hangi parça düştü: yapı 1; E1 4 (bC ortalaması 1, yön değişimi 4); E2 5 (yeşil çıkış 3, önceki kapanış 1, SMA üstü kalma 4); E3 16 (içeriden 9, gövde medyanı 10, en büyük gövde 9, Spearman 11, son kapanış 4, örtüşme 1); E4 9. (Alt koşul sayımlarına yapısı olmayan 1 sayfa da girer.) EVET sayfalarında düşen parça sayısı: 1 parça 3 sayfa, 2 parça 8, 3 parça 5.
- Cemal HAYIR / v4 VAR: 0.
- Parça geçme payı EVET / HAYIR: yapı %94 / %56, E1 %75 / %33, E2 %69 / %42, E3 %0 / %2, E4 %44 / %47. Parça puanlarının AUC'si (bilgi): E1 0,70, E2 0,60, E3 0,53, E4 0,58.
- Esnek hizalama (bilgi, hüküm dışı; son +-3 bar, 16-24 uzunluk): 3 VAR (kappa 0,02); esnek PUAN4 AUC 0,538 (0,39-0,69).
- Yeniden üretim: AUC scipy Mann-Whitney ile aynı (birleşik 0,5028; set 1 0,4412; set 2 0,5496); her sayfada vektörlü kural = düz döngü (v4_duz; fark olsa komut dururdu); set 1 pencerelerinde v1 S anahtardaki S ile aynı (K10).

Sayfa sayfa (C = Cemal 1 EVET / 0 HAYIR; parça sütunları geçti mi; p = parça puanı):

| set | sayfa | zaman | C | v4 | PUAN4 | yapı (k) | E1 | E2 | E3 | E4 | p E1 / E2 / E3 / E4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 3 | günlük | 0 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 1,00 |
| 1 | 4 | haftalık | 0 | - | 0,292 | 9 | ✓ | ✓ | - | ✓ | 0,93 / 1,00 / 0,29 / 0,50 |
| 1 | 5 | günlük | 0 | - | 0,000 | yok (15) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,59 |
| 1 | 6 | günlük | 1 | - | 0,000 | 7 | ✓ | ✓ | - | ✓ | 0,74 / 1,00 / 0,00 / 0,61 |
| 1 | 7 | haftalık | 0 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,86 |
| 1 | 8 | haftalık | 0 | - | 0,000 | yok (15) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,80 |
| 1 | 9 | haftalık | 0 | - | 0,000 | yok (10) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,63 |
| 1 | 10 | günlük | 1 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,88 |
| 1 | 11 | haftalık | 0 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,50 |
| 1 | 12 | günlük | 0 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,72 |
| 1 | 13 | haftalık | 0 | - | 0,000 | yok (10) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,50 |
| 1 | 14 | günlük | 0 | - | 0,000 | 8 | - | ✓ | - | ✓ | 0,00 / 1,00 / 0,00 / 0,61 |
| 1 | 15 | haftalık | 0 | - | 0,000 | 8 | ✓ | ✓ | - | ✓ | 0,50 / 1,00 / 0,00 / 0,75 |
| 1 | 16 | haftalık | 0 | - | 0,000 | yok (11) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,75 |
| 1 | 17 | günlük | 0 | - | 0,000 | 6 | ✓ | - | - | ✓ | 1,00 / 0,00 / 0,00 / 0,68 |
| 1 | 18 | haftalık | 0 | - | 0,000 | yok (11) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,50 |
| 1 | 19 | haftalık | 1 | - | 0,000 | 9 | ✓ | ✓ | - | ✓ | 0,50 / 0,58 / 0,00 / 0,94 |
| 1 | 20 | günlük | 0 | - | 0,000 | 7 | - | ✓ | - | ✓ | 0,00 / 1,00 / 0,44 / 0,50 |
| 1 | 21 | günlük | 1 | - | 0,000 | 4 | - | - | - | ✓ | 0,00 / 0,09 / 0,00 / 1,00 |
| 1 | 22 | günlük | 1 | - | 0,000 | 4 | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,61 |
| 1 | 23 | günlük | 1 | - | 0,000 | 5 | - | ✓ | - | ✓ | 0,00 / 1,00 / 0,13 / 0,50 |
| 1 | 24 | haftalık | 1 | - | 0,000 | 12 | ✓ | ✓ | - | ✓ | 0,81 / 0,72 / 0,00 / 0,67 |
| 1 | 25 | günlük | 0 | - | 0,000 | 8 | ✓ | ✓ | - | ✓ | 0,86 / 1,00 / 0,00 / 0,75 |
| 1 | 26 | haftalık | 0 | - | 0,099 | 5 | ✓ | ✓ | - | ✓ | 0,50 / 1,00 / 0,10 / 0,50 |
| 2 | 2 | günlük | 0 | - | 0,000 | yok (0) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,32 |
| 2 | 3 | haftalık | 0 | - | 0,000 | 10 | ✓ | ✓ | - | - | 0,83 / 1,00 / 0,00 / 0,10 |
| 2 | 4 | günlük | 0 | - | 0,000 | yok (11) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,25 |
| 2 | 5 | günlük | 0 | - | 0,000 | 8 | ✓ | ✓ | - | - | 0,50 / 1,00 / 0,00 / 0,13 |
| 2 | 6 | günlük | 0 | - | 0,000 | 3 | - | - | - | - | 0,00 / 0,29 / 0,08 / 0,06 |
| 2 | 10 | günlük | 1 | - | 0,000 | 11 | ✓ | ✓ | - | - | 0,55 / 1,00 / 0,00 / 0,32 |
| 2 | 11 | haftalık | 1 | - | 0,000 | 7 | ✓ | ✓ | - | - | 0,62 / 0,71 / 0,00 / 0,17 |
| 2 | 13 | günlük | 0 | - | 0,000 | yok (0) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,00 |
| 2 | 14 | haftalık | 1 | - | 0,000 | 7 | ✓ | - | - | - | 1,00 / 0,00 / 0,00 / 0,00 |
| 2 | 15 | günlük | 0 | - | 0,000 | 6 | - | - | - | - | 0,00 / 0,33 / 0,00 / 0,23 |
| 2 | 16 | haftalık | 0 | - | 0,000 | yok (0) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,17 |
| 2 | 17 | günlük | 1 | - | 0,000 | 12 | ✓ | ✓ | - | - | 0,67 / 1,00 / 0,30 / 0,00 |
| 2 | 18 | haftalık | 1 | - | 0,055 | 6 | ✓ | - | - | - | 0,73 / 0,42 / 0,06 / 0,42 |
| 2 | 19 | haftalık | 0 | - | 0,227 | 7 | ✓ | ✓ | - | - | 0,50 / 1,00 / 0,32 / 0,23 |
| 2 | 21 | haftalık | 0 | - | 0,000 | 7 | - | ✓ | - | - | 0,00 / 0,95 / 0,00 / 0,06 |
| 2 | 23 | günlük | 0 | - | 0,000 | yok (-) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,05 |
| 2 | 24 | günlük | 0 | - | 0,000 | yok (13) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,00 |
| 2 | 25 | günlük | 0 | - | 0,000 | yok (12) | - | - | - | ✓ | 0,00 / 0,00 / 0,00 / 0,61 |
| 2 | 27 | haftalık | 1 | - | 0,000 | 5 | ✓ | ✓ | - | - | 0,88 / 1,00 / 0,00 / 0,38 |
| 2 | 29 | haftalık | 0 | - | 0,000 | 4 | ✓ | - | - | - | 0,50 / 0,17 / 0,00 / 0,20 |
| 2 | 30 | günlük | 0 | - | 0,000 | 7 | - | ✓ | - | - | 0,00 / 1,00 / 0,00 / 0,30 |
| 2 | 31 | haftalık | 0 | - | 0,000 | yok (15) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,00 |
| 2 | 32 | günlük | 1 | - | 0,000 | 10 | ✓ | ✓ | - | - | 0,83 / 1,00 / 0,00 / 0,42 |
| 2 | 33 | haftalık | 1 | - | 0,100 | 7 | ✓ | ✓ | - | - | 0,50 / 0,58 / 0,17 / 0,10 |
| 2 | 35 | günlük | 0 | - | 0,000 | 5 | ✓ | - | - | - | 0,50 / 0,00 / 0,00 / 0,00 |
| 2 | 37 | haftalık | 0 | - | 0,000 | 3 | - | ✓ | - | - | 0,00 / 1,00 / 0,00 / 0,00 |
| 2 | 38 | günlük | 0 | - | 0,000 | 8 | - | ✓ | - | ✓ | 0,34 / 1,00 / 0,00 / 0,50 |
| 2 | 39 | günlük | 0 | - | 0,000 | 10 | ✓ | ✓ | ✓ | - | 0,81 / 1,00 / 0,60 / 0,00 |
| 2 | 40 | haftalık | 0 | - | 0,076 | 11 | ✓ | ✓ | - | - | 0,73 / 1,00 / 0,08 / 0,23 |
| 2 | 41 | günlük | 0 | - | 0,000 | yok (13) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,42 |
| 2 | 42 | haftalık | 0 | - | 0,000 | yok (1) | - | - | - | - | 0,00 / 0,00 / 0,00 / 0,00 |
| 2 | 43 | haftalık | 1 | - | 0,000 | 9 | ✓ | ✓ | - | - | 0,54 / 0,82 / 0,00 / 0,33 |
| 2 | 44 | günlük | 0 | - | 0,000 | 10 | ✓ | ✓ | - | ✓ | 1,00 / 0,72 / 0,00 / 0,50 |
| 2 | 45 | günlük | 0 | - | 0,000 | 5 | - | - | - | - | 0,28 / 0,46 / 0,00 / 0,30 |
| 2 | 47 | haftalık | 0 | - | 0,000 | 9 | ✓ | ✓ | - | - | 0,91 / 1,00 / 0,00 / 0,17 |
| 2 | 48 | haftalık | 0 | - | 0,235 | 5 | - | ✓ | - | ✓ | 0,40 / 1,00 / 0,24 / 0,63 |
| 2 | 49 | haftalık | 0 | - | 0,000 | 7 | ✓ | ✓ | - | - | 0,50 / 1,00 / 0,00 / 0,00 |

('yok (k)': yapı koşulu yok; parantezde ilk SMA üstü kapanışın sırası; '-' içinde hiç SMA üstü kapanış yok.)

## SAYIM ve ONAY SETİ

YAPILMADI: hüküm UYUMLU değil (iş tanımı D'yi yalnız UYUMLU'da koşturur). MUM_IZI7_ONAY.pdf ve anahtarı üretilmedi.

## KONTROL LİSTESİ

- K1 EVET: negatifler sentetikte sayıyla; kappa bootstrap ve AUC permütasyonu.
- K2 EVET: b her mumun kendi gününe kadarki bantla; test_gelecege_bakmama geçti; etiketler ön kayıt commit'inden (21:06:10Z) sonra (21:06:19Z) açıldı. Tarama yapılmadığı için KASA kapısı çağrılmadı (sınama penceresi en geç 2022-09-16).
- K3 EVET: geçerli bar; haftalıkta eksik haftalı pencere (esnek bilgide) atılır.
- K4 EVET: tekrar sayfaları set 2'de sayılmadı; tekil kuralı (D'de) hazır.
- K5 UYGULANMAZ. K6 EVET. K7 EVET (getiri yok).
- K8 EVET: 61 karar sayfası; v4 VAR 0 -> ÖLÇÜLEMEDİ.
- K9 EVET: ön kayıt sha'ları; v4_kapi sınamadan önce geçti.
- K10 EVET: set 1 pencerelerinde v1 S = anahtar S; etiket şeması bilinmeyen değerde durur (iki dosya da şemaya uydu).
- K11 EVET: vektörlü = düz döngü (her sayfa); AUC scipy ile aynı.
- K12 EVET: hüküm önceden yazılı eşikle; commit mesajlarında etiket-sayfa eşlemesi yok (sayfa tablosu yalnız bu dosyada ve mum_izi7_sinama.csv'de).
- K13 EVET: eski kodlar / defterler / UC_IZ2 değişmedi; başka ajanın çalışma ağacındaki mum_izi6 olc dosyaları (MUM_IZI6_OLCUM.md, mum_izi6_olcum.json) açılmadı, git add edilmedi.
- K14 UYGULANMAZ.

## HATA

1. (kurgu; benim; tekrar eden örüntü, EK 5 HATA 4) n7 / n8a / n8b negatifleri görüntü bantlarıyla kuruldu ve orada v4 YOK veriyordu (test); sentetik seride bantlar yeniden hesaplanınca ilk SMA üstü kapanış kalıbın 10. mumundan kayıyor ve kırmızı / dev çıkış mumu 'çıkış mumu' olmaktan çıkıyor: bu negatifler sentetik bantta tam negatif değil (%6-11 VAR). Ders aynı: negatif önce sentetik bant içinde kendi ölçüsünde sınanır (hangi parçayı düşürdüğü), sonra ölçüte girer.
2. (test; benim; ön kayıttan önce düzeltildi) test_puan_esikte_yarim kayan nokta eşitliği (0,9999999999999999 = 1,0) beklediği için kaldı; toleranslı karşılaştırmaya çevrildi.
3. (bilgi) Kappa hiç VAR yokken sayısal olarak 4e-16 basıldı; tanım gereği 0. Raporda 0 yazıldı.

## SAPMA

- İş tanımındaki negatif listesinde n4 yok; atlandı. n8 iki ayrı negatif olarak koşuldu (n8a, n8b; ölçüt her birine ayrı).
- Tanım, eşik ve puan ön kayıttan sonra değişmedi. Başka sapma yok.

## ÖNERİ (uygulanmadı; aynı etiketlere sonradan bakış, karar değil)

1. Kural her parçada Cemal'in EVET'lerinden dar: EVET sayfalarının hiçbiri E3'ü geçmiyor; en çok Spearman (11 / 16), gövde medyanı 1,5 x şablon (10 / 16), içeriden %80 (9 / 16) düşüyor. Cemal'in 'küçük küçük, düzenli' dediği tırmanış bant içinde tek yönlü bir bC sırası değil; fiyat kapanışlarıyla ölçülen bir tırmanış ya da gövde sınırının şablona değil bant genişliğine göre konması sınanabilir (yeni ön kayıtla).
2. E4: EVET sayfalarının 9 / 16'sında uzun üst fitil payı < %50; set 1'de hepsi geçiyor (v2 kapısı üst fitili zaten seçmişti), set 2'de çoğu düşüyor. 'Mumların çoğu' tırmanış kısmına özgü olabilir.
3. En çok bilgi taşıyan parça E1 (alt bantta gel-git; parça puanı AUC 0,70); E3 puanı (0,53) bilgi taşımıyor.
4. Şablon iki sınırda (E4 %50, k = m / 2): sentetik pozitif yakalamanın %22'de kalması bununla tutarlı. Sözlü tariften sabit eşik çıkarmak dördüncü kez Cemal'in gözüyle uyuşmadı; Cemal'den 3-4 EVET sayfasında parçaların yerini (gel-git, çıkış mumu, tırmanış başı / sonu) doğrudan işaretlemesi istenebilir; ya da EK 6'daki öğrenen model sonucu (T4) ile karar verilir.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler; etiket-sayfa eşlemesi yazılmaz)

- IK_KAYIT Ç233 (ya da sıradaki no): MUM_IZI EK 7 v4 evre kuralı (Cemal'in kapak notu: E1 alt bantta gel-git, E2 yeşil mumla SMA aşma, E3 üst banda içeriden boncuk gibi tırmanış, E4 çoğu mumda uzun üst fitil; sabit eşikler). Şablon dört parçadan geçiyor ama iki sınırda (E4 %50, k = m / 2). Sentetik GEÇMEDİ (pozitif %22,4; n7 / n8a / n8b %6-11). 61 karar sayfasında (16 EVET) v4 VAR 0 -> ÖLÇÜLEMEDİ (kural çok dar); PUAN4 AUC 0,50 (0,42-0,60). EVET sayfalarının hepsinde E3 düşüyor. D yapılmadı. Karar: TESPİT GEÇERSİZ / ÖLÇÜLEMEDİ. Getiri yok. Commit 3636571 / 9fafd70 / (sonuç).
- IK_GOREV: 25 Kas, EK 7 v4 + sentetik + iki setle sınama: ÖLÇÜLEMEDİ; açık: Cemal'in kararı.
- IK_HATA: n7 / n8a / n8b negatif kurgusu sentetik bantta tam negatif değil (kurgu; EK 5 HATA 4 tekrarı; ders: negatif önce sentetik bant içinde kendi ölçüsünde sınanır).
- IK_ACIK: Cemal karar: (1) EVET sayfalarında parçaların yerini doğrudan işaretlemek, (2) E3'ü fiyat kapanışıyla / bant genişliğine göre yeniden tanımlayan v5 (yeni ön kayıt, aynı iki setle değil yeni etiketle), ya da (3) hattı kapatmak.
