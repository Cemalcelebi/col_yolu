# K59-B ÖN KAYIT — K59 §6'daki önceden yazılı üç deneme: küçük-orta hisseler, 3 ay tutma, French yinelemesi

Yazım zamanı: 2026-11-11 10:44:08 UTC (2026-11-11 13:44 TR) (ölçümden ÖNCE; gerçek veride hiçbir K59-B portföy getirisi, fazla ya da t hesaplanmadı, sonuç görülmedi). Sürüm: K59-B v1.0 (2026-11-11): K59 §6'daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; sinyaller ve cetvel v2 K59 ile aynı
K59B_ESIK_SHA256: 54591b5ffdcdd27b73d7ba145652f7ce36c8a330a04178a6415636f273588522
K59_ESIK_SHA256: 6fe8bb38566701f175883f803332524dbbab493561eef3e4c968bfa332c51eb0
(K59-B mührü = K59B_ESIK + K59 mührünün sha256'sı. K59 mührü DEĞİŞMEDİ: K59_ON_KAYIT.md dosya sha256 11560c74c315c676daffea4763861cdbb16001092abd863d2714a9130b4659e9,
git 9e04f3e953; K59'un ölçüm kodu, sinyal tanımları, evren kuralları ve cetvel v2 eşikleri aynen kullanılır. `python -I K59.py b_kos`
iki mühürle, aşağıdaki veri sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; koşu başında yeniden hesaplanır)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- F-F_Research_Data_5_Factors_2x3_CSV.zip: sha256 17d7a575e71d6764a70ddec3f8d887756c0eebf3a60f64d6ba95d2adde3fed26 (1 dosya)
- F-F_Momentum_Factor_CSV.zip: sha256 27ed60e5b2caa9ea334a261cddfa864a9926f6bf45e9677c95dfd835c5abb315 (1 dosya)
- secframes: sha256 aca462674de19f06ec4f9e98767d6a5bb2735fb61598bbcc4591271b738dd0c7 (206 dosya)
- secfs: sha256 d44ce77eeb4780b5edb9277728323f6360e88110ec86dcc4349e6ec00c07ec69 (24 dosya)
- k57b_fiyat: sha256 a7fb07ef3926327be1a10c6285c6692436b201fca34b8d86c6ee6ad8fd8c50a9 (4461 dosya)
- liste_abd.csv.gz: sha256 87539954817d5d551623eeed04fa410844646539093a4e841a7755a2cfc674cb (1 dosya)
- 10_Portfolios_Prior_12_2_CSV.zip: sha256 688467caa28578a8dca70698537c4f03c406b246350b6f3e9c396e15e1e7964f (1 dosya)
- Portfolios_Formed_on_OP_CSV.zip: sha256 2bdf5bdbe9e8231d37b8607de6361fc51213487e763e1bc855f7cd3c055183cf (1 dosya)
K59 ön kaydındaki sekiz kaynak burada da AYNI özetle yer alır (koşu iki ön kaydı karşılaştırır); son iki zip (c) içindir. Klasör özeti = ada
göre sıralı 'dosya adı:sha256' satırlarının sha256'sı. SEC'e istek atılmaz; e-posta kullanılmaz.

## 0. Neden ve önceden bilinenler
K59 kararı: PORTFÖY-ADAY yok. CLAUDE.md 'İz yok çıkarsa durma' kuralı gereği, K59_ON_KAYIT.md §6'da K59 ÖLÇÜLMEDEN ÖNCE yazılmış üç deneme
şimdi K59-B olarak koşulur. Hangi üç denemenin yapılacağı sonuca göre seçilmedi (K59 ön kaydı git 9e04f3e953, K59 koşusundan önce).
Denemelerin AYRINTILARI ise (aşağıda 'BOŞLUK n' diye işaretli; §7'de liste) K59 sonucu görüldükten SONRA, K59-B ölçümünden ÖNCE dolduruldu.
K59 sonucu (K59_RAPOR.md; git e5312ca) bu ön kayıttan ÖNCE görüldü; K59-B bu dört sinyal için kör DEĞİLDİR:
  COMP4:   U1 net yıllık fazla -%1,6 (NW t -0,49; dört şartın dördü de tutmadı); U2 +%5,5 (NW t 2,30; alfa t 2,87; tutmayan tek şart
           'son %30 ayda fazla > 0': -%0,06 / ay).
  DOSYA_Y: U1 +%0,8 (NW t 0,22); U2 +%5,1 (NW t 2,14; tutmayan: son %30).   S5: U1 -%1,8 (NW t -0,61); U2 +%5,4 (NW t 1,99; tutmayan: NW t, son %30).
  S1:      U1 +%11,9 (NW t 2,77; TUTAR (yineleme)); U2 -%2,8 (NW t -0,54).   S3 küçüklük: U1 +%10,8 (NW t 3,03), U2 -%11,8 (NW t -2,11):
           momentum ve küçüklük iki evrende TERS işaretli çıktı.
  Plasebo (U2, 200 rastgele sinyal, aylık tutma, tam evren): yanlış pozitif maliyetli %0,0, maliyetsiz %1,5; cetvel v2 GÜVENİLİR.
ÇOKLU DENEME: K59 bu örneklemde 12 deneme saydı (9 tekil + 3 DOSYA; COMP4 önceden yazılı karar bileşiği). K59-B aynı 2021-2026 örnekleminde
8 deneme daha ekler (4 sinyal x 2 tasarım). Bu yüzden K59-B'de tutan sonuç, K59'da tutmuş olsaydı taşıyacağı ağırlığı TAŞIMAZ;
'ikinci tur adayı'dır ve K60'ta (uzun tarih) doğrulanmadan kullanılmaz.
Faz 1'de gerçek veride yalnız şunlar yapıldı: (i) `python -I K59.py b_kapsam` (hisse / ay / sinyal başına hisse SAYISI; getiri yok),
(ii) iki French zip'i indirildi; bölüm başlıkları, sütun adları, ilk / son ay etiketleri okundu ve ayrıştırıcı gerçek dosyalarda yalnız BİÇİM
için denendi (satır / sütun sayısı, eksik hücre sayısı, ayların ardışıklığı). Hiçbir getiri değeri basılmadı, harman kurulmadı, ortalama ya da
başka istatistik hesaplanmadı.

## 1. K59'dan aynen alınanlar (değişmez)
- Evrenler U1 (V_ABD (islenmis-veri; bugün yaşayan ~1.400 ABD hissesi)) ve U2 (geniş ABD evreni (K57-B Yahoo önbelleği; bugün yaşayan ~4.260 hisse)); K59 §1'deki uygunluk kuralları, kriz
  kesiği 2026-08-31, maliyet tek yön 10 bp x devir. İkisi de yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı) ve bağımsız değil.
- Sinyal tanımları K59 §2 (yalnız t ve öncesi bilgi; temel veri SEC 'filed' <= t). K59-B'de ölçülenler: COMP4 (BİRİNCİL), DOSYA_Y, S5, S1 (bilgi).
- Portföy: sinyali olan uygun hisselerin üst %10'u, eşit ağırlık, ay sonu kapanışında işlem (K58 k58_ust_dilim).
- CETVEL v2 (K59 §3) aynen, MALİYETTEN SONRA: (1) aylık fazla ortalaması > 0 ve Newey-West (gecikme 6) t > 2.0; (2) ayların ardışık eşit
  3 parçasının en az 2'sinde ortalama fazla > 0; (3) son %30 ayda ortalama fazla > 0; (4) beta düzeltmeli alfa > 0 ve NW t(alfa) > 2.0.
  Ölçüm ayı < 36 ise 'ÖLÇÜLEMEDİ' (tutar sayılmaz). Bilgi istatistikleri (FF5 + UMD alfası, Sharpe, en büyük düşüş, devir, brüt) K59 gibi.
- BOŞLUK 10: K59'un öteki sinyalleri (S2-S4, S6-S9), COMP9, DOSYA_D, DOSYA_YD ve UCUZLUK koşulmaz; BIST ölçülmez (iş tanımı yalnız U1 ve U2 diyor).

## 2. Tasarım (a): yalnız küçük-orta hisseler
- Her ay sonu t'de alt evren = uygun (K59 §1) VE boyut ölçüsü olan hisselerden, boyutu o ayın kesit medyanının ALTINDA olanlar.
- BOŞLUK 1: boyut ölçüsü = K59 S3'ün o ay kullandığı ölçü (K59 §2 S3 kuralı aynen): U2'de piyasa değeri (o günkü fiyat x pay sayısı; uygun
  hisselerin en az %50'sinin payı olan aylarda), öteki aylarda ve U1'de her ay 20 günlük medyan işlem değeri. Medyan, boyutu olan uygun
  hisseler üzerinden hesaplanır; 'altı' KESİN küçüktür (medyana eşit olan dışarıda); boyutu olmayan hisse (U2'de payı bilinmeyen) alt evrene girmez.
- BOŞLUK 2: alt evren, o ay için evrenin YERİNE geçer: (i) bileşik sinyallerin (COMP4, DOSYA_Y) yüzdelik sıraları alt evren içinde yeniden
  hesaplanır (üye sinyallerin ham değerleri aynı; S4'ün 'ear'ı K57 olay tablosundaki gibi, tam panel medyanına göre kalır); (ii) üst %10 alt
  evrende sinyali olan hisseler arasından seçilir; (iii) KIYAS = alt evrenin eşit ağırlıklı getirisi (maliyetsiz); (iv) alt evren < 100 hisse
  olan ay atlanır; ölçüm dönemi = alt evrende sinyali olan hisse sayısının ilk kez >= 100 olduğu aydan sona. Aylık dengeleme, maliyet ve
  cetvel v2 K59 ile aynı. Alt evrenden çıkan (medyanı aşan) hisse o ay satılır (devir ve maliyet buna göre).

## 3. Tasarım (b): 3 ay tutma, örtüşen üç kohort (Jegadeesh-Titman düzeni)
- Evren, sinyaller, bileşik sıraları ve üst %10 seçimi K59 ile birebir aynı (tam uygun evren). Her ay sonu yeni bir kohort kurulur ve 3 ay
  tutulur; sermaye üç kohorta bölünmüştür ve her ay yalnız süresi dolan kohort yenilenir (ölçümün i. oluşum ayında i mod 3 numaralı kohort).
  Bir ayın getirisi = o ay canlı olan üç kohortun getirilerinin basit ortalaması. KIYAS = K59 ile aynı (bütün uygun evrenin eşit ağırlıklısı).
- BOŞLUK 3: kohort içi AL-TUT: kuruluşta eşit ağırlık, 3 ay boyunca ara dengeleme yok (ağırlıklar fiyatla kayar, ara ayda işlem ve maliyet yok).
  Yenilemede kohortun devri = Σ|w_yeni - w_kaymış| (yeni seçimde de kalan hisse yalnız fark kadar işlem görür; ilk kuruluşta devir 1);
  maliyet = 10 bp x devir, yenilenen kohortun o ayki getirisinden düşülür (net = (1 - maliyet x devir) x (1 + r) - 1, K58 ile aynı biçim).
  Kohortlar arası sermayeyi her ay 1/3'e eşitlemenin maliyeti sayılmaz (yayındaki takvim-zamanı düzeni; küçük, ama net getiriyi hafif iyimser yapar).
  Raporlanan aylık devir = üç kohortun devir ortalaması (portföyün tamamına oranla).
- BOŞLUK 4: tutulan hisse sonraki aylarda uygunluğu yitirse de (fiyat < 2 $, likidite, veri boşluğu) SATILMAZ, süre dolana kadar tutulur.
  Tutma getirisi = sonsuz ileri taşımalı ay sonu kapanışlarının oranı - 1 (kapanışı olmayan ay 0 getiri; uygun hissede K59 ay getirisiyle
  aynıdır, koşu bunu doğrular). Evren yalnız yaşayanlardan oluştuğu için borsadan çıkış getirisi yoktur.
- BOŞLUK 5: başlangıç: üç kohortun üçü de canlı olana kadarki ilk 2 ay ölçüme GİRMEZ (ölçüm ayı = K59'daki ay sayısı - 2).
  Kohortlar sinyalin K59'daki ilk ölçüm ayından (sinyali olan hisse >= 100) başlayarak kurulur.
- BOŞLUK 6: oluşum ayları kesintisiz olmalıdır (K59 kapsam.csv: U1 123, U2 68 ardışık ay). Kesinti çıkarsa kohort takvimi belirsizleşir; koşu durur.

## 4. Tasarım (c): French veri kütüphanesinde momentum + kârlılık harmanı (BİLGİ; hayatta kalma yanlılığı yok)
- Kaynak (https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/; CRSP'nin bütün hisseleri, batanlar dahil):
  momentum = 10_Portfolios_Prior_12_2_CSV.zip ('10 Portfolios Formed on Momentum', önceki 12-2 ay getirisi, NYSE onluk sınırları), sütun 'Hi PRIOR' (en üst onluk);
  kârlılık = Portfolios_Formed_on_OP_CSV.zip ('Portfolios Formed on Operating Profitability'), sütun 'Hi 20' (en üst beşlik);
  piyasa ve RF = K59'un French 5 faktör dosyası (MKT = Mkt-RF + RF).
  Aylık bölümler başlık satırıyla seçilir (büyük / küçük harf ayrımsız, satırın tamamı; dosyada tam 1 eşleşme olmalı, yoksa koşu durur):
  değer ağırlıklı `^(average\s+)?value[\s-]*weight(ed)?\s+returns\s*--\s*monthly$`, eşit ağırlıklı `^(average\s+)?equal[\s-]*weight(ed)?\s+returns\s*--\s*monthly$`.
  Eksik değerler (-99.99, -999.0) yok sayılır; getiriler % -> ondalık. Zip'ler ayrı `python -I` alt sürecinde, boş klasörde ayrıştırılır.
- HARMAN (uzun-yalnız, aylık dengeli): aylık getiri = 0.5 x momentum üst onluğu + 0.5 x kârlılık üst beşliği. İki harman: VW (iki bacak da değer
  ağırlıklı) ve EW (iki bacak da eşit ağırlıklı).
- KIYAS: VW harman için piyasa (MKT). EW harman için EW10 = on momentum onluğunun eşit ağırlıklı getirilerinin basit ortalaması (geniş eşit
  ağırlıklı evren VEKİLİ; onluklar NYSE sınırlarıyla kurulduğu için hisse sayıları eşit değildir, tam eşit ağırlıklı piyasa değildir).
  BOŞLUK 7a: üç satır raporlanır: VW_MKT (VW harman - MKT; ANA), EW_EW10 (EW harman - EW10; ANA), EW_MKT (EW harman - MKT; BİLGİ). EW harmanın MKT'ye göre
  fazlası küçük hisse primini de taşır; o satır yalnız bilgidir, okuma cümlesine girmez.
- MALİYET: French serilerinde işlem maliyeti yok. Brüt ve NET ayrı raporlanır; net = brüt - %0.10 / ay (10 bp x %100 aylık devir varsayımı,
  üst sınır diye önceden yazıldı; her ay sabit düşülür). Okuma NET seriye bakar.
- DÖNEMLER: '1963-son' = 1963-07 .. son ay; '2000-son' = 2000-01 .. son ay; '2000-09' = 2000-01 .. 2009-12; '2010-19' = 2010-01 .. 2019-12; '2020-son' = 2020-01 .. son ay.
  BOŞLUK 7b: 'son ay' = harmanın dört sütununda, EW10'da, MKT ve RF'de birlikte bulunan son ay (Faz 1 başlık okuması: bütün dosyalar
  1963-07 .. 2026-09; CRSP 202609). Fon krizi kesiği (31.08.2026, BIST olayı) French ABD serisine uygulanmaz (K58 B de son aya kadar ölçtü).
  Ortak aylar ardışık değilse koşu durur.
- ÖLÇÜ: her varyant x dönem için cetvel v2 (K59 §3'ün dört şartı; portföy = harman, kıyas = yukarıdaki) brüt ve net ayrı ayrı; ayrıca yıllık
  fazla, NW t, alt dönem ortalamaları, alfa, t(alfa), beta. Dönem < 36 ay ise 'ÖLÇÜLEMEDİ'.
- BOŞLUK 7c: ÖNCEDEN YAZILI OKUMA (ANA iki varyant için ayrı ayrı; NET seri): 'uzun dönemde tutuyor' ⇔ cetvel v2 hem '1963-son' hem '2000-son'
  döneminde TUTAR. '2020 sonrası güçlü' ⇔ '2020-son' döneminde ortalama net fazla > 0; 'zayıf' ⇔ <= 0 ('güçlü' burada yalnız 'pozitif' demektir;
  NW t yanında yazılır). Cümleler: 'bileşik uzun dönemde tutuyor ve 2020 sonrası güçlü' / 'bileşik uzun dönemde tutuyor ama 2020 sonrası zayıf' /
  'bileşik uzun dönemde tutmuyor (hangi dönem tutmadı); 2020 sonrası güçlü | zayıf'.
- SINIRLAR: harman, K59 COMP4'ün (momentum + PEAD + kârlılık + düşük ihraç sıra ortalaması) kendisi DEĞİL, iki hazır portföyün yarı yarıya
  karışımıdır; kârlılık ölçüsü faaliyet kârlılığıdır (K59 S5 = net kâr / özkaynak değil); VW harman dev şirketlerin, EW harman çok küçük
  hisselerin ağırlığındadır. (c) U1 / U2 sonucunu ne doğrular ne çürütür; 'bu tür bileşik uzun tarihte ve yanlılıksız veride var mı' sorusuna bakar.

## 5. Plasebo (cetvelin her tasarımda sınanması) — BOŞLUK 8
K59 plasebosu aylık tutma ve tam evren içindi. (a) ve (b) için ayrı ayrı: U2'de 200 rastgele sinyal (her ay uygun hisselere rastgele sıra;
numpy default_rng(tohum + i); tohum (a) 59100, (b) 59200), o tasarımın portföy kuralı ve cetvel v2. Yanlış pozitif oranı = TUTAN payı; maliyetli ve
maliyetsiz (brüt) İKİSİ de <= %5 olmalı. Biri > %5 ise (ya da plasebo ölçülemediyse) o tasarımda cetvel GÜVENİLMEZ sayılır ve o tasarımın dört sinyali
için 'HÜKÜM YOK' yazılır (öteki tasarım etkilenmez).

## 6. Karar kuralları (şimdi yazıldı; sonuçtan sonra değişmez)
1. Evren düzeyi etiket (bilgi): bir sinyal bir tasarımda bir evrende cetvel v2'nin dört şartını maliyetten sonra sağlıyorsa 'TUTAR (yineleme)';
   hem NW t(fazla) hem t(alfa) > 2.75 ise 'GÜÇLÜ' (4 sinyal x 2 tasarım = 8 deneme için Bonferroni); aksi 'TUTMAZ'; ay < 36 'ÖLÇÜLEMEDİ'.
2. Tasarım düzeyi: (a) ya da (b)'de bir sinyal 'TUTAR' ⇔ HEM U1 HEM U2'de cetvel v2 maliyetten sonra tutar VE iki evrende de net yıllık fazla
   >= +4 puan. İki evrende de 'GÜÇLÜ' ise tasarım düzeyinde de 'GÜÇLÜ' yazılır. BOŞLUK 9: iki evrende tutar ama birinde net yıllık fazla
   < +4 puan ise 'TUTMAZ (küçük)' (K59'daki 'TUTAR AMA KÜÇÜK' ara etiketi burada yok); bir evrende tutmazsa / ölçülemezse 'TUTMAZ'.
3. KARAR yalnız COMP4'e bakar: 'K59-B PORTFÖY-ADAY' ⇔ COMP4 (a) YA DA (b) tasarımında 'TUTAR' (iki evrende). Aksi 'TUTMAZ'. BOŞLUK 9: iki
   tasarımda da cetvel güvenilmez / plasebo ölçülmemiş ise karar 'HÜKÜM YOK' yazılır. DOSYA_Y, S5 ve S1 bilgidir; kararı değiştirmez, onlardan
   yeni bileşik kurulmaz.
4. (c) karara GİRMEZ; tarih hakkında bilgidir ve §4'teki önceden yazılı okuma cümlesiyle raporlanır.
5. İZ ilan EDİLEMEZ (CLAUDE.md standardı FI_OLCUT, ABD + Avrupa; Avrupa'da temel veri yok). K59-B'nin çıkabilecek etiketleri yalnız
   'K59-B PORTFÖY-ADAY' ve 'TUTMAZ' (ya da 'HÜKÜM YOK')'tur. 'K59-B PORTFÖY-ADAY' bir öneri kapısı (CLAUDE.md 'tarama' kapısı) SAYILMAZ; K60 doğrulaması gerekir.

## 7. BOŞLUK listesi (iş tanımında açık kalan, ölçümden önce burada doldurulan ayrıntılar)
1. (a) boyut = K59 S3'ün o ayki ölçüsü; medyan boyutu olan uygun hisselerde; kesin altı; boyutu olmayan dışarıda.
2. (a) sıralar, üst %10 ve kıyas alt evren içinde; S4 'ear' aynen; alt evren < 100 ay atlanır; sinyal eşiği 100.
3. (b) kohort içi al-tut; devir ve maliyet yalnız yenilenen kohortta; kohortlar arası eşitleme maliyetsiz.
4. (b) tutulan hisse uygunluğu yitirse de satılmaz; tutma getirisi ileri taşımalı kapanıştan.
5. (b) ilk 2 ay (üç kohort canlı değil) ölçüme girmez; kıyas tam uygun evren.
6. (b) oluşum ayları kesintiliyse koşu durur.
7. (c) üç rapor satırı (EW - MKT bilgi), 'son ay' tanımı ve kriz kesiğinin uygulanmaması, okuma cümlesinin ölçülebilir tanımı, bölüm desenleri.
8. Tasarıma özel plasebo (200 rastgele sinyal, U2; > %5 ise o tasarımda hüküm yok).
9. 'küçük' (< +4 puan) tasarım düzeyinde TUTMAZ sayılır; iki tasarım da hükümsüzse 'HÜKÜM YOK'.
10. Yalnız dört sinyal, yalnız U1 ve U2; BIST, UCUZLUK ve öteki sinyaller koşulmaz.

## 8. Kapsam (veriden ötürü, sonuçtan bağımsız)
Faz 1 sayımı (11 Kas 2026, `python -I K59.py b_kapsam`; yalnız hisse sayıları, getiri hesaplanmadı):
  U1: 123 oluşum ayı (2016-05-31 .. 2026-07-31, ardışık), uygun evren ortalama 1.084. (a) alt evren 123 ay, ortalama 542 (en az 399); boyut her ay
      işlem değeri. Alt evrende sinyali olan hisse / beklenen ölçüm ayı: COMP4 501 / 66 ay (2021-02-26'dan), DOSYA_Y 392 / 63 ay (2021-05-28'den; tam
      evrenden bir ay geç), S5 445 / 66 ay, S1 543 / 122 ay (2016-06-30'dan). (b) beklenen ölçüm ayı: COMP4 64, DOSYA_Y 62, S5 64, S1 120.
  U2: 68 oluşum ayı (2020-12-31 .. 2026-07-31, ardışık), uygun evren ortalama 2.146; boyutu olan ortalama 1.917 (payı bilinmeyen ~%11 alt evrene
      giremez). (a) alt evren 68 ay, ortalama 958 (en az 813); boyut 65 ay piyasa değeri, ilk 3 ay işlem değeri. Alt evrende sinyali olan hisse /
      beklenen ölçüm ayı: COMP4 875 / 66 ay, DOSYA_Y 783 / 63 ay, S5 801 / 66 ay, S1 958 / 67 ay. (b) beklenen ölçüm ayı: COMP4 64, DOSYA_Y 62, S5 64, S1 65.
  Hepsi >= 36 ay: 'ÖLÇÜLEMEDİ' beklenmez. S1'in U1'deki ölçüm dönemi (2016'dan) öteki sinyallerden (2021'den) uzundur; K59'da da böyleydi.
  French (yalnız başlık okuması): iki portföy dosyası CRSP 202609 tabanlı; momentum 1927-01 .. 2026-09 (1.197 ay), kârlılık ve 5 faktör
      1963-07 .. 2026-09 (759 ay); gerekli sütunlarda eksik hücre yok, aylar ardışık. Beklenen ay sayıları: 1963-son 759, 2000-son 321, 2000-09 120,
      2010-19 120, 2020-son 81. Momentum dosyasında değer ağırlıklı aylık bölümün başlığı 'Value Weight Returns -- Monthly', kârlılık dosyasında
      'Average Value Weight Returns -- Monthly'; eşit ağırlıklı bölüm ikisinde de 'Average Equal Weighted Returns -- Monthly'.

## 9. K59-B'den sonra (sonuç ne olursa olsun)
Hat K60'a geçer: K60 (uzun tarih, batanlar dahil evren, sinyal kütüphanesinin tamamı); bu dokuz sinyalin 2021-26 örnekleminde başka çeşitlemesi denenmez.
K59-B tutsa da tutmasa da bu ön kayda yeni tasarım, yeni eşik ya da yeni sinyal eklenmez.

## 10. Değişmezlik
Yukarıdaki bütün eşikler, tanımlar ve kurallar sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön kayıt
değişmez, düzeltme raporda ayrıca yazılır. K59_ON_KAYIT.md ve K59 çıktıları değişmez.

## 11. Faz 2 komutu (bu dosya git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K59.py b_kos`
