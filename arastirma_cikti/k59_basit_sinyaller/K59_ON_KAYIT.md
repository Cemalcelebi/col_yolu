# K59 ÖN KAYIT — basit sinyaller, portföy cetveli v2 (aylık, geniş evren)

Yazım zamanı: 2026-11-11 05:28:28 UTC (2026-11-11 08:28 TR) (ölçümden ÖNCE; gerçek veride hiçbir sinyal portföyü getirisi hesaplanmadı, sonuç görülmedi). Sürüm: K59 v1.0 (2026-11-11): basit sinyaller (S1-S9, COMP4, COMP9) x portföy cetveli v2 (K58 C + beta düzeltmeli alfa); ABD iki evren karar, BIST bilgi
ESIK_SHA256: 6f4aca9fd2e26afe3caae6c0675d588cba017c9203ac17fddf2354234b169fa1
(K59_ESIK + içe alınan K57_ESIK / K57B_ESIK / K58 B / FI_K28 / FI_K31 tanımlarının sha256'sı. `python -I K59.py kos` bu mühürle, aşağıdaki
veri sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; koşu başında yeniden hesaplanır)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- F-F_Research_Data_5_Factors_2x3_CSV.zip: sha256 17d7a575e71d6764a70ddec3f8d887756c0eebf3a60f64d6ba95d2adde3fed26 (1 dosya)
- F-F_Momentum_Factor_CSV.zip: sha256 27ed60e5b2caa9ea334a261cddfa864a9926f6bf45e9677c95dfd835c5abb315 (1 dosya)
- secframes: sha256 aca462674de19f06ec4f9e98767d6a5bb2735fb61598bbcc4591271b738dd0c7 (206 dosya)
- secfs: sha256 d44ce77eeb4780b5edb9277728323f6360e88110ec86dcc4349e6ec00c07ec69 (24 dosya)
- k57b_fiyat: sha256 a7fb07ef3926327be1a10c6285c6692436b201fca34b8d86c6ee6ad8fd8c50a9 (4461 dosya)
- liste_abd.csv.gz: sha256 87539954817d5d551623eeed04fa410844646539093a4e841a7755a2cfc674cb (1 dosya)
Klasör özeti = ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı. SEC'e istek atılmaz; frames önbelleği yoksa koşu durur.

## 0. Soru ve önceden bilinenler
Yol haritası (11 Kas) Y1: ~150 çalışmada şart ekleyip daralttık (n küçüldü, olay cetveli kördü). Burada tersi: nedeni bilinen, basit,
SÜREKLİ sinyaller her ay binlerce hissede sıralanır; ölçüm portföy düzeyinde, aylık, maliyetli, beta düzeltmeli.
Bu ön kayıttan ÖNCE görülmüş ilgili sonuçlar (kör olmayan kısım): K58 C1 = V_ABD'de 12-1 momentum, K58 evreniyle (fiyat / likidite tabanı
yok) net yıllık fazla +%8,5, NW t 2,10, K58 C 'TUTAR'. Bu yüzden S1 / U1 kör değildir (evren süzgeci ve alfa şartı yeni). Öteki sinyaller
ve bileşikler bu evrenlerde portföy olarak hiç ölçülmedi; K57 / B / C bilanço tepkisini olay cetveliyle (FI_OLCUT) ölçtü, İZ DEĞİL çıktı.
Faz 1'de gerçek veride yalnız `kapsam` komutu koşuldu (hisse / ay / sinyal başına hisse SAYISI); getiri, fazla, t hesaplanmadı.

## 1. Evrenler (ABD = karar, BIST = bilgi)
- U1: V_ABD (islenmis-veri; bugün yaşayan ~1.400 ABD hissesi). Oluşum ayları ay sonu >= 2016-01-01, fiyat 2026-08-31'de kesik (K58 C ile aynı kriz kesiği).
- U2: geniş ABD evreni (K57-B Yahoo önbelleği; bugün yaşayan ~4.260 hisse). Üyelik = SEC frames'te gelir + net kâr + özkaynak etiketi ve borsa kodu olan CIK (K57 k57b_evren), Yahoo türü
  EQUITY, en az 150 gün fiyat (K57 k57b_fiyat_genis). Fiyatlar 2020-01-01 .. 2026-08-31; en az 3000 hisse yüklenemezse koşu durur.
- BIST: V_BIST (islenmis-veri; bugün yaşayan ~580 hisse), kriz kesiği 2026-08-31, maliyet tek yön 30 bp; yalnız fiyat / hacim sinyalleri
  (S1, S2, S3, S8, S9) ve bunların ortalaması (COMP9, 5 üye). Karar rolü yok.
- Ay sonu = panel takviminin her aydaki son işlem günü (K58 k58_aylik). Ay getirisi (k -> k+1) = sonraki ay sonu kapanışı (ileri taşımalı)
  / ay sonu kapanışı - 1; fiyatlar temettü / bölünme düzeltmeli. Son oluşum ayı kesikten önceki ay sonu.
- UYGUNLUK (her ay sonu t, yalnız t ve öncesi bilgi): (1) t'ye kadar en az 252 günlük kapanış; (2) ABD: o günkü fiyat >= 2 $;
  (3) ABD: son 20 işlem gününün (en az 15 gözlem) medyan işlem değeri (kapanış x hacim) >= 1 milyon $;
  (4) ay sonu k ve k-1 kapanışı var (en çok 5 gün ileri taşıma). BIST'te (2) ve (3) yok (TL eşiği zamanla anlamını yitirir).
  'O günkü fiyat': U2'de Yahoo HAM kapanışı (bölünme düzeltmeli, temettüsüz) x t'den SONRAKİ bölünmelerin çarpımı = o gün işlem gören fiyat
  (sonradan ters bölünen kuruşluk hisse tabanı geçemez); işlem değeri de ham kapanışla. U1'de (V_ABD'de bölünme kaydı ve ham fiyat yok)
  düzeltilmiş kapanış kullanılır: sonradan ters bölünen hisse olduğundan pahalı, sonradan bölünen / temettü ödeyen ucuz görünür (yanlılık).
  U2 sınırı: Yahoo kapanışı indirme gününe (9 Kas 2026) kadarki bölünmelere göre düzeltilmiştir, bölünme kaydı ise 2026-09-01'de biter; bu
  arada bölünen az sayıda hissede o günkü fiyat ve piyasa değeri bölünme oranı kadar sapar.
  Uygun hisse sayısı < 100 (BIST 50) olan ay atlanır.
- HAYATTA KALMA YANLILIĞI: üç evren de yalnız BUGÜN işlem gören hisselerdir. Batan / borsadan çıkan hisseler yok; bu, kaybedenleri taşıyan
  sinyalleri (dönüş S2, küçüklük S3) olduğundan iyi, düşük oynaklık / kârlılık gibi 'kaliteli' sinyalleri olduğundan kötü gösterebilir.
  Kıyas (eşit ağırlıklı evren) aynı yanlılığı taşır, fark kısmen silinir ama sıfır değildir. Yanlılıksız kontrol sıradaki deneme (c).
- U1 ve U2 BAĞIMSIZ DEĞİL: U1'in ~1.100 hissesi U2'de de var ve temel veri (aşağıda) 2020'de başladığı için S4-S7 ve COMP4 iki evrende de
  aynı 2021-2026 dönemini ölçer. 'İki evrende tutar' bağımsız yineleme değil, evren genişliğine dayanıklılıktır.

## 2. Sinyaller (ay sonu t'de yalnız t ve öncesi bilgi; her sinyalde 'yüksek = iyi' yönü)
Temel veri: SEC XBRL frames önbelleği (K57 k57_abd_temel_tablo; çeyrekler 2020Q1 .. 2026Q2, 4. çeyrek yıllıktan türetilir).
BİLGİ TARİHİ = o çeyreğin ilk 10-Q / 10-K başvurusunun SEC 'filed' günü (dönem sonu ±10 gün eşleşen, K57 _k57_abd_bilgi_tarihleri, Nasdaq
takvimi VERİLMEDEN: basın açıklaması günü kullanılmaz); başvuru özütlerde yoksa (2021 öncesi başvurular) çeyrek sonu + 90 gün.
Bir çeyrek ancak bilgi tarihi <= t ise kullanılır; en son bilinen çeyreğin sonu t'den en çok 200 gün önce olmalı (bayat veri yok).
Sınır: frames değerleri şirketin EN SON bildirdiği değerdir (sonradan düzeltilmiş olabilir); tarih özgün başvuru günüdür.
- S1 momentum 12-1: kapanış(k-1) / kapanış(k-12) - 1 (ay sonları; K58 k58_sinyal_momentum). Yüksek iyi.
- S2 1 ay dönüş (geçen ayın en çok düşenleri): -(kapanış(k) / kapanış(k-1) - 1). En çok düşen iyi.
- S3 küçüklük: U2'de piyasa değeri = o günkü fiyat x pay sayısı (SEC finansal özütleri, FON_IZI fi_k31_finansal; başvuru 'filed' <= t,
  pay tarihi t'den en çok 200 gün önce; pay tarihinden sonraki bölünmelerle düzeltilir). Bir ayda uygun hisselerin en az
  %50'sinin pay sayısı varsa o ay piyasa değeri kullanılır (payı olmayan hisse S3'e girmez); yoksa o ay 20 günlük medyan işlem
  değeri. U1 ve BIST'te HER AY 20 günlük medyan işlem değeri (V_ABD'de bölünme kaydı yok: düzeltilmiş fiyat x eski pay sayısı, sonradan
  bölünen = iyi giden hisseyi küçük gösterir, geleceğe bakma olur). En küçük iyi. Hangi ay hangi ölçü: kapsam.csv 'S3_olcu'.
- S4 bilanço tepkisi (PEAD): K57 k57_olay_abd olayları (Nasdaq bilanço takvimi 2022-12-01 sonrası; öncesinde 2021-01-01'den itibaren SEC 10-Q / 10-K
  başvuru günü). 'ear' = açıklama gününden önceki son kapanıştan sonraki ilk kapanışa getiri - aynı pencerede evren medyanı (FON_IZI
  fi_k28_olaylar). Tepki penceresi t'ye kadar bitmiş ve son 63 işlem günü içinde olan EN SON olayın 'ear'ı. Olayı olmayan hisse S4'e
  girmez; üst %10 olayı olanlar arasındadır. Yüksek iyi. Sınır: 2021-22'de olay günü başvuru günüdür (basın açıklamasından sonra olabilir).
- S5 kârlılık (son 4 çeyrek net kâr / özkaynak): NetIncomeLoss son 4 çeyrek toplamı / StockholdersEquity (en son bilinen çeyrek sonu); özkaynak > 0 şart. Yüksek iyi.
- S6 düşük net ihraç (yıllık pay değişimi): en son başvurunun ('filed' <= t) yıllık pay değişimi (fi_k31_finansal pay_yil: 300-430 gün önceki paya oran).
  Bölünme K57 F4 gibi: oran (1 + değişim) bir tamsayıya (>= 2) ±%3 yakınsa bölünme, değişim = oran / tamsayı - 1. EK (F4'te gerekmiyordu):
  ters bölünme aynı kuralla (1 / oran tamsayıya yakınsa değişim = oran x tamsayı - 1); yoksa ters bölünme dev geri alım gibi görünür.
  Oran > 5 ya da < 1/5 ise veri YOK sayılır. En düşük değişim iyi.
- S7 satış ivmesi (son çeyrek / önceki iki çeyrek ortalaması): gelir (K57 etiket sırası: Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet; üç çeyreği de olan ilk etiket)
  son çeyrek / önceki iki çeyreğin ortalaması; ortalama > 0 şart. Yüksek iyi.
- S8 düşük oynaklık (60 gün): -(son 60 işlem gününün günlük getiri standart sapması; en az 40 gözlem). En düşük iyi.
- S9 52 hafta zirvesine yakınlık: ay sonu kapanışı / son 252 işlem gününün en yüksek gün içi fiyatı (en az 200 gözlem). Yüksek iyi.
- COMP4 (KARAR; önceden yazıldı, seçim yok): S1, S4, S5, S6 sinyallerinin ay içi yüzdelik sıralarının ((sıra - 0,5) / n; uygun ve o sinyali
  olan hisseler arasında, eşitlikte ortalama sıra) ortalaması; hissenin dördün en az 3'ünde değeri olmalı. Üst %10.
- COMP9 (BİLGİ): dokuz sinyalin sıra ortalaması; en az 5 sinyal. (BIST'te beş fiyat / hacim sinyali.)
KAPSAM (veriden ötürü, sonuçtan bağımsız): temel veri 2020'de başlar; pay sayısı özütleri 2021'de başlar, yıllık değişim bir yıl ister.
Bir sinyalin ölçüm dönemi = o sinyali olan uygun hisse sayısının ilk kez >= 100 (BIST 30) olduğu aydan sona.
Faz 1 kapsam sayımı (11 Kas 2026, yalnız hisse sayıları; getiri hesaplanmadı):
  U1: 1.411 hisse, 123 oluşum ayı (2016-05-31 .. 2026-07-31), uygun evren ortalama 1.084 (799-1.406). S1, S2, S3, S8, S9 2016'dan (122-123 ay);
      S7 2020-12'den (68 ay), S4 / S5 / COMP4 2021-02'den (66 ay), S6 2022-02'den (54 ay). S3 her ay işlem değeri. COMP9 2021 öncesi beş fiyat
      sinyalinin ortalamasıdır (bileşimi zamanla değişir; bilgi).
  U2: 4.261 hisse (1.151'inde 2020-26 arasında bölünme / ters bölünme var), 68 oluşum ayı (2020-12-31 .. 2026-07-31), uygun evren ortalama 2.146
      (1.916-2.477). S1 2021-01'den (67 ay), S4 / S5 / COMP4 2021-02'den (66 ay), S6 2022-02'den (54 ay), ötekiler 68 ay. S3: ilk 3 ay işlem
      değeri, sonraki 65 ay piyasa değeri. COMP4 2022-02'ye kadar üç üyeyle (S1, S4, S5) kurulur (S6 henüz yok).
  BIST: 581 hisse, 123 oluşum ayı, uygun evren ortalama 423 (357-581).

## 3. Portföy ve cetvel v2
- Portföy: sinyali olan uygun hisselerin en üst %10'u (sayı = max(1, yuvarla(0,10 x sinyali olan uygun hisse)); eşitlikte kod sırası),
  eşit ağırlık, aylık yeniden dengeleme, ay sonu kapanışında işlem (K58 k58_ust_dilim / k58_portfoy). Maliyet tek yön ABD 10 bp,
  BIST 30 bp x devir (devir = Σ|w_yeni - w_kaymış|, ilk ay 1). Kıyas = BÜTÜN uygun evrenin eşit ağırlıklı getirisi (maliyetsiz).
  Aykırı getiri kırpması yok (K58 C ile aynı).
- CETVEL v2 TUTAR ⇔ dört şart birden, MALİYETTEN SONRA:
  (1) aylık fazla e = net portföy - kıyas: ortalama > 0 ve Newey-West (gecikme 6) t > 2.0;
  (2) ayların ardışık eşit 3 parçasının en az 2'sinde ortalama e > 0;
  (3) son %30 ayda (yukarı yuvarlanmış) ortalama e > 0;
  (4) BETA DÜZELTMELİ ALFA: net portföy getirisi = alfa + beta x kıyas getirisi + hata (sabitli EKK); alfa > 0 ve Newey-West (gecikme 6,
      Bartlett, serbestlik düzeltmesi yok) t(alfa) > 2.0.
  Ölçüm ayı < 36 ise 'ÖLÇÜLEMEDİ' (tutar sayılmaz).
- BİLGİ (karar rolü yok): FF5 + UMD alfası (net portföy - RF'nin MKT-RF, SMB, HML, RMW, CMA, UMD üzerine sabitli EKK'si; French dosyaları K58
  ile aynı, RF 5 faktör dosyasından; ortak aylar), yıllık fazla (12 x ortalama e), Sharpe ((portföy - RF) ort / sd x √12), en büyük düşüş,
  aylık devir, ortalama hisse sayısı ve aynı istatistiklerin maliyetsiz (brüt) hali. BIST'te French alfası yok, Sharpe'ta rf = 0.

## 4. Karar kuralları (şimdi yazıldı; sonuçtan sonra değişmez)
1. Bir sinyal bir evrende TUTAR ⇔ cetvel v2'nin dört şartı maliyetten sonra sağlanır. Etiket: 'TUTAR (yineleme)' (t > 2.0; bilinen etkinin
   yinelemesi eşiği); hem NW t(fazla) hem t(alfa) > 2.8 ise 'GÜÇLÜ' (dokuz tekil sinyal için Bonferroni'ye dayanıklı). Aksi 'TUTMAZ'.
2. PORTFÖY-ADAY ⇔ COMP4 hem U1 hem U2'de TUTAR VE iki evrende de net yıllık fazla >= +4 puan. İkisinde tutar ama birinde
   yıllık fazla < +4 puan ise 'TUTAR AMA KÜÇÜK'. Birinde tutmazsa 'TUTMAZ'. Tekil sinyallerde yıllık fazla < +4 puan 'küçük' diye işaretlenir.
3. İZ ilan EDİLEMEZ: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi ve Avrupa'da temel veri yok. Standart değişikliği Cemal'in kararı.
4. Seçim yok: karar yalnız COMP4'e bakar. Tekil sinyaller ve COMP9 bilgi içindir; 'en iyi tutan sinyali seçip' yeni bileşik kurulmaz.
5. BIST bilgi olarak raporlanır; karara girmez.

## 5. Plasebo (cetvelin kendisinin sınaması)
U2'de 200 rastgele sinyal (her ay uygun hisselere rastgele sıra; numpy default_rng(59000 + i)), aynı üst %10 portföyü ve cetvel v2.
Yanlış pozitif oranı = TUTAN payı; hem maliyetli hem maliyetsiz (brüt) cetvelle hesaplanır, İKİSİ de <= %5 olmalı (maliyet yüksek devirli
rastgele portföyü zaten cezalandırır; brüt oran sert olanıdır). Biri > %5 ise cetvel v2 GÜVENİLMEZ ilan edilir ve hiçbir sinyal için hüküm verilmez.

## 6. COMP4 tutmazsa önceden yazılı sıradaki üç deneme (Faz 2'de KOŞULMAZ; ana oturum karar verir)
- (a) yalnız küçük-orta hisseler (her ay uygun evrenin boyut medyanının altı), aynı sinyaller ve cetvel.
- (b) 3 ay tutma, örtüşen portföyler (her ay üçte biri yenilenir), aynı sinyaller ve cetvel.
- (c) French veri kütüphanesinde 2000-2026 momentum + kârlılık bileşiğinin yinelemesi (hayatta kalma yanlılığı yok).

## 7. Değişmezlik
Yukarıdaki bütün eşikler, tanımlar ve evren kuralları sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön
kayıt değişmez, düzeltme raporda ayrıca yazılır.

## 8. Faz 2 komutu (bu dosya git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K59.py kos`
