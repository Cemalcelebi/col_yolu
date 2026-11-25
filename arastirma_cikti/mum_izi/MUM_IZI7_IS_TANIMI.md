# MUM_IZI EK 7 İŞ TANIMI — Cemal'in kapak notundan EVRE KURALI (v4), mühürlü etiketlerle sınama (25 Kasım 2026)

Yazan: ana model. Cemal etiket seti 2'nin kapağına şu notu yazdı (PDF yorumu, harfiyen): "SMA alt bandı da ikin bir geo git (yükseliş düşüş şeklinde) sonrasında yeşil mum ile SMA rin orta bandını yeşil mum ile çıkış yaparak ama üst bandına içerden boncuk şeklinde küçük küçük mumlar düzenli tirmenis ve mumların çoğu üst fitil uzun".

Ana modelin okuması (yazım düzeltilmiş): "SMA'nın alt bandında bir-iki gel-git (yükseliş-düşüş şeklinde); sonrasında yeşil mumla SMA'nın orta bandını aşarak çıkış; ama üst banda İÇERİDEN, boncuk gibi küçük küçük mumlarla düzenli tırmanış; ve mumların çoğunda üst fitil uzun."

## Mühür ve kurallar
- BU İŞTE etiket dosyaları (cemal_mum_izi6_etiket.json, cemal_mum_izi4_onay.json), işaretli PDF'ler, mum_izi6 `olc` çıktıları (mum_izi6_sonuc*, mum_izi6_olc*) ve mum_izi5_sinama.csv, v4 tanımı + sentetik + ön kayıt (MUM_IZI7_ON_KAYIT.md) COMMIT EDİLENE KADAR AÇILMAZ / KULLANILMAZ. v4 yalnız Cemal'in notundan, şablonun kendi mumlarından ve sentetikten kurulur. Ön kayıttan sonra tanım değişmez (fikir = 'ÖNERİ').
- MUM_IZI_IS_TANIMI.md ve CLAUDE.md 'Tespit geçerliliği' aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31, KASA açılmaz, GETİRİ / SONRASI YOK. Eski kodlar değişmez. Yeni: MUM_IZI_V4.py + test_mum_izi7.py. Commit mesajına / rapora etiket-sayfa eşlemesi yazılmaz (sayfa numarasıyla sonuç tablosu yalnız rapor dosyasında, ön kayıttan sonra).

## A. v4 EVRE KURALI (bant koordinatı: b = (fiyat - SMA20) / (üst bant - SMA20); SMA 0, üst bant +1, alt bant -1; her mum kendi gününe kadarki bantla)
Bölge 16-24 mum. Dört parça; her biri hem EVET / HAYIR hem 0-1 arası dereceli puan üretir:
- E1 ALT BANTTA GEL-GİT: bölgenin BAŞINDA (orta banda çıkıştan önceki kısım; en az 3, en çok bölgenin yarısı kadar mum) kapanışlar SMA'nın altında ve alt bant tarafında (bC ortalaması <= -0,3) VE bu kısımda en az bir yükseliş-düşüş dönüşü var (kapanış yönü en az 2 kez değişiyor: 'bir-iki gel-git'); tek yönlü düz iniş ya da tek mumluk dip gel-git değildir.
- E2 YEŞİL MUMLA ORTA BANDI AŞMA: E1'den sonra kapanışı SMA'nın üstüne çıkan İLK mum yeşil (C > O), bir önceki kapanış SMA'nın altında; bu çıkıştan sonra kapanışların en az %80'i SMA'nın üstünde kalıyor (kalıcı çıkış).
- E3 ÜST BANDA İÇERİDEN BONCUK GİBİ DÜZENLİ TIRMANIŞ: çıkıştan sonraki mumlar (en az 5): (a) İÇERİDEN: kapanışların en az %80'i 0 < bC <= 1,05 (SMA ile üst bant arasında; üst bandın dışına taşarak değil; bölgenin son 3 mumu bu orandan muaf, kalıpta son mumlar üst banda değiyor); (b) KÜÇÜK KÜÇÜK: bu kısımdaki gövdelerin medyanı (b biriminde) <= şablonun aynı kısmındaki medyanın 1,5 katı VE en büyük gövde <= şablondakinin 1,5 katı; (c) DÜZENLİ TIRMANIŞ: bC'nin sıraya göre Spearman korelasyonu >= 0,6 ve son kapanış bC >= 0,6; (d) BONCUK: ardışık mumların gövde / aralık örtüşmesi şablon düzeyinde (örtüşme >= şablonun 0,75 katı; mumlar arasında boşluk / sıçrama yok).
- E4 ÇOĞU MUMDA UZUN ÜST FİTİL: bölgenin bütün mumlarında 'uzun üst fitil' = üst fitil >= mum boyunun %30'u VE üst fitil > alt fitil; bu mumların payı >= %50 (şablonda bu pay kaç ise ön kayda yazılır; şablon geçmeli).
- KURAL: v4 VAR <=> E1 ∧ E2 ∧ E3 ∧ E4. PUAN4 = dört parçanın dereceli puanlarının EN KÜÇÜĞÜ (telafi yok). Dereceli puanların tanımı (eşiğe uzaklığın 0-1'e eşlenmesi) ön kayıtta sabitlenir.
- Eşiklerdeki sayılar (0,3; %80; 1,05; 1,5; 0,6; 0,75; %30; %50) bu iş tanımında SABİTTİR. Şablon (Cemal'in kalıbı) dört parçadan da geçmelidir; geçmiyorsa DUR ve hangi parçanın neden geçmediğini raporla (eşik değiştirme; ana model karar verir).

## B. Sentetik (pozitif + negatif), getirisiz
Pozitif: gömülü şablon (%0 / 10 / 20 gürültü; 200 tohum; dip / yatay bağlam). Negatif: n1 fitilsiz büyük gövde; n2 fitiller ters; n3 mumlar 2 kat; n5 aynı mumlar yatay gidiş; n6 V dönüş (alt bantta gel-git yok: tek dip + sert yükseliş); n7 üst bandın DIŞINDAN yürüyüş (büyük mumlarla bandı delerek); n8 SMA'yı kırmızı mumlu boşlukla / tek dev mumla aşma; rastgele (blok + rastgele yürüyüş). KABUL ÖLÇÜTÜ (önceden): %10 gürültüde pozitif VAR payı >= %60; her negatifte VAR <= %5; rastgele seride 1.000 barda VAR <= 0,3. Geçmezse yazılır, tanım değişmez.

## C. Etiketlerle sınama (ön kayıt commit'inden SONRA)
- Etiketler: set 1 (cemal_mum_izi4_onay.json; anahtar mum_izi4_onay_anahtar.json; 24 sayfa) + set 2 (cemal_mum_izi6_etiket.json; anahtar mum_izi6_anahtar.json; 'isaret' EVET / HAYIR olanlar; IKISI / YOK / BELIRSIZ karar dışı; tekrar sayfaları set 2'de sayılmaz, çift sayım olmasın). Her sayfanın bölgesi için v4 VAR / YOK ve PUAN4.
- Ölçü: kappa (v4 VAR ile Cemal EVET), bootstrap %95 (B 5000), uyum, 2x2; PUAN4 AUC + %95; set 1, set 2 ve birleşik ayrı; günlük / haftalık ayrı (bilgi). Cemal EVET / v4 YOK sayfalarında hangi parça düştü (sayım), Cemal HAYIR / v4 VAR sayfaları.
- HÜKÜM (önceden, birleşik): kappa >= 0,60 ve alt uç >= 0,40 -> 'Cemal'in gözüyle UYUMLU'; kappa 0,40-0,60 KISMEN; < 0,40 UYUMSUZ. v4 VAR sayısı < 5 ise 'kural çok dar: ÖLÇÜLEMEDİ' (AUC yine yazılır).

## D. Yalnız hüküm UYUMLU ise: evren taraması (getirisiz) + onay seti
Günlük 2016-22, haftalık 2001-22; ABD / AVR P2, BIST (işlem değeri medyan üstü); v4 VAR bölge sayısı (pazar x dilim; tekil 15 mum, kümenin en yüksek PUAN4'lü hizası). MUM_IZI7_ONAY.pdf: v4 VAR bölgelerinden RASTGELE 24 (günlük 12 + haftalık 12; hisse başına bir; önceki setlerin hisseleri hariç), düzen MUM_IZI4_ONAY ile aynı, hisse / tarih / sonrası yok; anahtar ayrı. Onay eşiği >= 19 / 24.

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI7_ON_KAYIT.md, MUM_IZI7_RAPOR.md (v4 TANIM: uygulama kararları ve şablonun dört parçadaki değerleri; SENTETİK; ETİKETLERLE SINAMA; (varsa) SAYIM ve ONAY SETİ; KONTROL LİSTESİ; HATA; SAPMA; ÖNERİ; ÖNERİLEN DEFTER SATIRLARI), mum_izi7_sonuc.json, mum_izi7_sinama.csv, (varsa) MUM_IZI7_ONAY.pdf + anahtar.
