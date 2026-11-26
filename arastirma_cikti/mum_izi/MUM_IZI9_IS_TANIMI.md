# MUM_IZI EK 9 İŞ TANIMI — v6: v5M + Cemal'in üç yeni şartı (küçük mum, muntazam dizilim, net Bollinger daralması) (26 Kasım 2026)

Yazan: ana model. Cemal MUM_IZI8_ONAY'ı işaretledi: 24 bölgenin 2'si BENZİYOR (sayfa 5, 8), 17'si BENZEMİYOR, 1 iki kutu (s9), 4 işaretsiz (s20, 21, 24, 26). v5M TESPİT GEÇERSİZ (eşik 19 / 24). Ardından yazdı (26 Kas): "Mumlar küçük olmalı, dizilim muntazam olmalı, Bollinger daralması net olmalı." İşaret dosyası: cemal_mum_izi8_onay.json (anahtar: mum_izi8_onay_anahtar.json). Sayfa 19'daki daireleri: gel-git sonundaki mumlar ve dev çıkış mumu + dağınık tırmanış.

Bu iş etiketleri KULLANIR. v5M'nin yapısı (gel-git + yeşil kalıcı çıkış + düzenli tırmanış + bandın içinden + mum yapısı M) aynen kalır; üstüne üç yeni zorunlu kapı gelir. Her kapı için önceden yazılı az sayıda aday ölçü var; eşik sonuca göre serbestçe aranmaz, tek kuralla konur.

## Kurallar
- MUM_IZI_IS_TANIMI.md ve CLAUDE.md 'Tespit geçerliliği' aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31, KASA açılmaz, GETİRİ / SONRASI YOK. Eski kodlar değişmez. Yeni: MUM_IZI_V6.py + test_mum_izi9.py.
- Sıra: aday ölçüler + tablo -> seçim -> sentetik -> ön kayıt MUM_IZI9_ON_KAYIT.md commit -> evren taraması + PDF. Ön kayıttan sonra kural değişmez.

## A. Etiket kümesi (v5M VAR sayfaları)
EVET = Cemal'in BENZİYOR dediği v5M sayfaları: yeni set s5, s8 + önceki 61 etikette v5M VAR olup EVET olanlar (4). HAYIR = yeni setin 17 BENZEMİYOR sayfası + önceki 61'de v5M VAR olup HAYIR olan (1). İki kutu / işaretsiz sayfalar karar dışı. (Sayılar raporda doğrulanır.)

## B. Aday ölçüler (bant koordinatı b: SMA 0, bant ±1; k = çıkış mumu; 'tırmanış' = çıkıştan sonraki mumlar)
KÜÇÜK MUM (K): K1 bölgedeki en büyük gövde (b birimi); K2 medyan mum boyu (H-L) / bant genişliği; K3 medyan mum boyu / bölgeden önceki 60 barın medyan mum boyu (şablonda ölçülemez: şablon şartından muaf); K4 çıkış mumunun gövdesi (b birimi). Hepsi 'küçük iyi'.
MUNTAZAM DİZİLİM (D): D1 çıkış + tırmanışta en büyük kapanış adımı |C_i - C_{i-1}| (b birimi; küçük iyi); D2 bölgede ardışık mum örtüşmesi (MI 'ortusme'; büyük iyi); D3 tırmanışta kapanışların doğrusal uyumu R² (büyük iyi); D4 tırmanışta mum boyu değişkenliği (std / ortalama; küçük iyi).
NET BOLLINGER DARALMASI (BB): BB1 bölge içi en dar bant genişliği / bölgenin ilk 3 mumundaki ortalama bant genişliği (küçük iyi); BB2 bölge içi en dar bant genişliği / [bölge başından 20 bar önce, bölge sonu] aralığındaki en geniş bant genişliği (küçük iyi; şablonda yalnız görüntüdeki mumlarla); BB3 en dar noktadaki (bant genişliği / SMA) değerinin o güne kadarki son 120 bardaki yüzdeliği (küçük iyi; şablonda ölçülemez: muaf); BB4 en dar noktanın bölge içindeki yeri 0,25-0,90 arasında (ikili).
Hepsi yalnız pencere sonuna kadarki veriyle (K2).

## C. Eşik ve seçim kuralı (önceden)
- Her aday için eşik = EVET sayfalarının ve (ölçülebiliyorsa) şablonun EN KÖTÜ değeri, %5 payla gevşetilmiş (yani bütün EVET sayfaları ve şablon geçer). İkili aday (BB4) ancak bütün EVET sayfaları ve şablon sağlıyorsa adaydır.
- Adayın puanı = bu eşikle reddedilen HAYIR sayfası payı. Her sözcük (K, D, BB) için en yüksek puanlı TEK aday seçilir (eşitlikte listedeki ilk). Puanı 0,15'in altında kalan sözcükte kapı konmaz ve bu açıkça yazılır.
- v6 = v5M ∧ K* ∧ D* ∧ BB*. Tablo: aday | EVET değerleri (min-maks) | HAYIR medyanı | eşik | reddedilen HAYIR payı; v6'nın birlikte reddettiği HAYIR payı.
- v6 HAYIR sayfalarının yarısından azını reddediyorsa DUR ve raporla (PDF üretme).
- Bilgi: önceki 61 etiketin tamamında (v5M olmayanlar dahil) ve MUM_IZI4 / 6 setlerinde v6'nın VAR dediği sayfalar ve Cemal'in yanıtı.

## D. Sentetik (v6; bantlar sentetik seride yeniden hesaplanır)
Pozitif: gömülü şablon %0 / 10 / 20 gürültü (K3 / BB3 için sentetik serinin kendi geçmişi kullanılır). Negatif (her biri önce kendi ölçüsünde doğrulanır; doğrulanmayan sayılmaz): n1 fitilsiz büyük gövde, n2 fitiller ters, n5 yatay gidiş, n8 TEK DEV MUMLA ÇIKIŞ (çıkış mumunun gövdesi bant yarı genişliğinin >= 1,2 katı olacak şekilde, sentetik bantta ölçülerek kurulur), n9 DARALMASIZ (kalıbın mumları geniş ve açılan bantta: önüne oynak dönem eklenir; BB* ölçüsü sentetikte gerçekten bozuluyor mu denetlenir), n10 DAĞINIK (aynı kapanış yolu, mum boyları rastgele 0,5-3 katla çarpılmış). Ölçüt (önceden): %10 gürültüde pozitif VAR >= %40; geçerli negatiflerde VAR <= %10; rastgele seride 1.000 barda VAR <= 0,5. Geçmezse yazılır, kural değişmez, kapakta belirtilir.

## E. Evren taraması + PDF (getirisiz)
- Tarama ve sayım MUM_IZI8 ile aynı evren / tekil kuralı; v6 VAR sayısı pazar x dilim.
- MUM_IZI9_ONAY.pdf: düzen MUM_IZI8_ONAY ile aynı (kapak: kural düz dille + üç yeni şart ve nasıl ölçüldüğü + 'senin işaretlerinle: v5M'nin 17 benzemiyor sayfasından kaçını artık eliyor'; sayfa 2: senin kalıbında kodun okuması + yeni üç sayı; sonra v6 VAR bölgelerinden RASTGELE 24 (günlük 12 + haftalık 12; hisse başına bir; önceki setlerin hisseleri hariç; bir dilimde 12'den az varsa hepsi), her sayfada kodun okuması (mavi / yeşil ok / turuncu) + mum yapısı satırı + yeni üç sayı (küçük mum, dizilim, daralma); ✓ / × kutuları; hisse / tarih / sonrası yok). Anahtar mum_izi9_onay_anahtar.json. Toplam v6 VAR < 8 ise DUR ve raporla.
- PDF Cemal'e ana modelin ön elemesinden sonra gidecek: son raporda PDF yolunu ver.

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI9_ON_KAYIT.md, MUM_IZI9_RAPOR.md (ADAY TABLOSU, SEÇİM, SENTETİK, SAYIM, ONAY SETİ, KONTROL LİSTESİ, HATA, SAPMA, ÖNERİLEN DEFTER SATIRLARI), mum_izi9_sonuc.json, MUM_IZI9_ONAY.pdf, mum_izi9_onay_anahtar.json.
