# MUM_IZI EK 8 İŞ TANIMI — v5: etiketlerden öğrenilmiş evre kuralı + 'kod nasıl tespit ediyor' PDF'i (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas): "Yeni bir PDF gönder, nasıl tespit ediyor; düzelmesi gerekir artık." Durum: 61 karar etiketi var (16 EVET / 45 HAYIR; set 1 + set 2). v4'ün parçalarından gözle örtüşenler: yapı (SMA'yı aşan çıkış var) EVET %94 / HAYIR %56, E1 alt bantta gel-git %75 / %33, E2 yeşil mumla kalıcı çıkış %69 / %42; E3 (tırmanış; ana modelin sayıları) 16 / 16 EVET'te düştü; E4 uzun üst fitil ayırmıyor (%44 / %47). Cemal'in EVET sayfalarındaki çizimleri (set 2 s18, s33, s43) baştaki düşüş / gel-git mumlarını ve SONDAKİ tırmanış mumlarını işaret ediyor. Tekrar uyumu 6 / 8 (%75).

Bu iş ETİKETLERİ KULLANIR (mühür yok): amaç, küçük ve önceden yazılı bir kural ailesinden etiketlerle en uyumlu olanı seçmek, sentetikle sınamak ve Cemal'e kodun NASIL okuduğunu gösteren yeni bir onay PDF'i vermek. Seçim iç örnektir (ezber riski); gerçek sınama Cemal'in yeni PDF'teki işaretleridir.

## Kurallar
- MUM_IZI_IS_TANIMI.md ve CLAUDE.md 'Tespit geçerliliği' aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31, KASA açılmaz, GETİRİ / SONRASI YOK. Eski kodlar değişmez. Yeni: MUM_IZI_V5.py + test_mum_izi8.py.
- Sıra: (1) aday kuralların kodu + testleri; (2) 61 etikette aday tablosu; (3) seçim kuralıyla v5 seçilir; (4) sentetik; (5) ön kayıt MUM_IZI8_ON_KAYIT.md (aday tablosu, seçilen kural, sentetik, onay seti seçim kuralı, tohum, KONTROL LİSTESİ) commit; (6) evren taraması + sayım + PDF. (5)'ten sonra kural değişmez.

## A. Parçalar (bant koordinatı b: SMA 0, üst bant +1, alt bant -1; pencere 16-24 mum; k = penceredeki ilk SMA üstü kapanış)
- Y yapı: 3 <= k <= 0,6 x m ve çıkıştan sonra en az 5 mum.
- G1 gel-git (v4 E1 aynen): çıkıştan önceki kısımda bC ortalaması <= -0,3 ve kapanış yönü en az 2 kez değişiyor.
- G2 yeşil kalıcı çıkış (v4 E2 aynen): çıkış mumu yeşil, önceki kapanış SMA altında, sonraki kapanışların >= %80'i SMA üstünde.
- T tırmanış (gevşek; FİYAT kapanışlarıyla): çıkıştan sonraki kapanışların sıra korelasyonu (Spearman) >= 0,5 ve son kapanış bC >= 0,6.
- I içeriden: çıkıştan sonraki kapanışların >= %60'ı bC <= 1,05.
- B boncuk (küçük mum; BANT genişliğine göre): çıkıştan sonraki gövdelerin en büyüğü <= bant yarı genişliğinin 0,9 katı (b biriminde <= 0,9) ve medyan gövde <= 0,30.
- F fitil (yalnız tırmanış kısmı): üst fitili alt fitilinden uzun olan mum payı >= %50.
- S: v1 benzerlik puanı >= 0,59 (v1 eşiği).

## B. Aday kurallar (yalnız bu 8; başka aday eklenmez)
R1 = Y ∧ G1 ∧ G2; R2 = R1 ∧ S; R3 = R1 ∧ T; R4 = R3 ∧ I; R5 = R3 ∧ B; R6 = R3 ∧ I ∧ B; R7 = R6 ∧ F; R8 = R6 ∧ S.
Her aday için 61 etikette: VAR sayısı, 2x2, isabet (VAR içinde EVET payı), yakalama (EVET içinde VAR payı), kappa + bootstrap %95; set 1 / set 2 ayrı (iki sette yön aynı mı).
SEÇİM KURALI (önceden): VAR >= 8 olan adaylar içinde en yüksek kappa; fark < 0,03 ise daha az parçalı olan. Hiçbir adayın kappası 0,20'yi geçmiyorsa DUR ve raporla (PDF üretme).
Bilgi: seçilen kuralın bir-sayfa-dışarıda (LOO) değil ama 'set 1'de seç, set 2'de sına' ve tersi sonuçları da yazılır (aday seçimi ne kadar oynuyor).

## C. Sentetik (seçilen kural için; pozitif + negatif)
Pozitif: gömülü şablon (%0 / 10 / 20 gürültü; 200 tohum; dip / yatay bağlam; bantlar sentetik seride yeniden hesaplanır). Negatif: n1 fitilsiz büyük gövde, n3 mumlar 2 kat, n5 yatay gidiş, n6 V dönüş (gel-git yok), n7 üst bandın dışından büyük mumlarla, n8 kırmızı / tek dev mumla çıkış; her negatif ÖNCE kendi ölçüsünde sınanır (gerçekten ihlal ettiği parçayı sentetik bantta da ihlal ediyor mu; etmiyorsa 'negatif kurgusu geçersiz' diye yazılır, sayılmaz); rastgele (blok + rastgele yürüyüş). Ölçüt (önceden): %10 gürültüde pozitif VAR >= %50; geçerli negatiflerde VAR <= %10; rastgele seride 1.000 barda VAR <= 1. Geçmezse yazılır; kural değişmez; PDF yine üretilir ama kapakta 'sentetik ölçütü geçmedi' yazar.

## D. Evren taraması ve PDF (getirisiz)
- Tarama: günlük 2016-22, haftalık 2001-22; ABD / AVR P2, BIST (işlem değeri medyan üstü); geçerli bar; haftalıkta eksik haftasız; tekil 15 mum (kümede en yüksek v1 S'li hiza). Sayım: v5 VAR bölge sayısı pazar x dilim, hisse-yıl başına sıklık.
- MUM_IZI8_ONAY.pdf (telefonda okunur):
  - Sayfa 1 'KOD NASIL TESPİT EDİYOR' (düz dil, en çok 8 satır): seçilen kuralın parçaları Cemal'in kendi cümlesiyle; senin 61 işaretinle uyumu ('benziyor dediğin 16 sayfanın kaçını buldu; var dediği kaç sayfanın kaçına sen de benziyor demiştin'); 'tekrar sayfalarında sen de 8'de 6 aynı dedin'.
  - Sayfa 2: Cemal'in KENDİ KALIBI üstünde kodun okuması: gel-git kısmı mavi şerit, çıkış mumu yeşil ok, tırmanış kısmı turuncu şerit, SMA ve bantlar; her parçanın ölçtüğü sayı küçük yazıyla.
  - Sonra 24 bölge: v5 VAR bölgelerinden RASTGELE (tohum ön kayıtta; günlük 12 + haftalık 12; hisse başına bir; önceki iki setin hisseleri hariç; BIST dilim başına en çok 4). Her sayfa: solda küçük 'Senin kalıbın', sağda bölge (öncesi 15 mum, Bollinger 20 + SMA20, bölge sonunda kesik) ve ÜSTÜNDE KODUN OKUMASI (aynı renkler: mavi gel-git, yeşil ok çıkış mumu, turuncu tırmanış); altta ✓ benziyor / × benzemiyor kutuları ve küçük not: 'yanlış okunan parçayı daire içine al'. Hisse / tarih / sonrası YOK. Anahtar mum_izi8_onay_anahtar.json'da.
- Onay eşiği (CLAUDE.md): >= 19 / 24 tespit geçerli. Beklenti raporda yazılır (etiketlerdeki isabet payı ve %75 tekrar uyumu).

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI8_ON_KAYIT.md, MUM_IZI8_RAPOR.md (ADAY TABLOSU, SEÇİM, SENTETİK, SAYIM, ONAY SETİ, KONTROL LİSTESİ, HATA, SAPMA, ÖNERİLEN DEFTER SATIRLARI), mum_izi8_sonuc.json, MUM_IZI8_ONAY.pdf, mum_izi8_onay_anahtar.json.
