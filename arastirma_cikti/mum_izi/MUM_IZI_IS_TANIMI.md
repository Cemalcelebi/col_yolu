# MUM_IZI İŞ TANIMI — Cemal'in işaretlediği mum bölgesinin parmak izi, sentetik tutturma testi, gerçek veride benzerlik (25 Kasım 2026)

Yazan: ana model. Cemal (25 Kas, ekran görüntüsü ORNEK_25Kas.jpg, turuncu daire): "Buradaki mumların parmak izini çıkar: büyüklük, alt fitil, üst fitil, birbirine bağlı / birbirine göre dizilimi ve SMA konumlarını, her şeyi ölç; bu ölçünün ne kadarını tutturduğunun birebir kodunu tekrar tekrar sentetik veri ile test et; veriye / testlere ne oranda benziyor ve fiyatın en tepesi olmadan diğer yerlerinde ne oranda tutturmuşsun görelim."

Not (ana model): şekil / parmak izi hattı 11 Kas yol haritasında 'yanlış yol' sınıfındaydı ve '90'dan fazla şekil ölçüsü' kapalı konudur. Bu iş Cemal'in açık isteğiyle yapılır; ölçü sayısı 40'ı geçmez; sonuç önce bir TESPİT / BENZERLİK ölçüsüdür, getiri sonucu yalnız ön kayıtlı bilgi satırıdır.

## 0. Kesin kurallar

- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/. Önerilen kayıt metni raporda.
- Aynı dalda başka bir alt ajan (UC_IZ2, arastirma_cikti/uc_iz2/, UC_IZ2.py) çalışıyor: onun dosyalarına dokunma; `git add -A` / `commit -a` YASAK, yalnız kendi yollarını ekle; index.lock görürsen bekle, yeniden dene. /root/.kasa/ham/veri3 ve /tmp/veri* yalnız OKUNUR.
- KASA AÇILMAZ: gerçek veri taraması 2022-12-31'e kadar (kod en büyük tarihi assert eder).
- Gerçek veri taramasından ÖNCE ön kayıt commit edilir (benzerlik eşiği, tanımlar, kod sha, KONTROL LİSTESİ); `IZ_KARNE.ik_kontrol_kapisi` geçmeden tarama başlamaz. Eşik sentetik testten seçilir, gerçek veriye bakılarak değişmez.
- Tek dosya MUM_IZI.py (KURAL_MOTORU, hata yakalama, loglama, çakışma kapısı) + test_mum_izi.py.

## 1. Görüntüden sayısallaştırma (A)

- ORNEK_25Kas.jpg'den turuncu dairenin içindeki her mum için piksel ölçüsü: gövde üst / alt, fitil üst / alt, renk (yeşil / kırmızı / doji), x merkezi; aynı x'te Bollinger üst / orta (SMA20) / alt çizgileri. Fiyat ekseni etiketi yok: her şey göreli (piksel; y yukarı pozitif). Dairenin hemen solundaki büyük kırmızı mum ve öncesi 'bağlam' olarak ayrı tutulur.
- Zaman ekseni: '22 Kas' ile '24 K' arasında ~12 mum var; grafik GÜN İÇİ (büyük olasılıkla 4 saatlik, 7/24 piyasa). İz ölçek bağımsız kurulur ve günlük veriye uygulanır; bu varsayım raporda yazılır.
- Sağlama: sayısallaştırılmış mumlar orijinal görüntünün üstüne çizilip (bindirme PNG) göz kontrolüne konur; mum sayısı ve renkleri elle sayımla aynı olmalı.

## 2. Parmak izi (B), en çok 40 ölçü, hepsi ölçek bağımsız

Birimi bölgenin ortalama mum boyu (H-L) ya da ATR. Mum başına: boy, gövde / boy, üst fitil / boy, alt fitil / boy, renk. Dizilim: ardışık mumların Low / High / kapanış farkı (yükselen dipler), örtüşme oranı, gövde ortası eğimi, kapanışların doğru eğimi ve R². Bant: her mumun %B konumu (alt bant 0, üst 1), SMA20'ye göre konum (üstünde / altında, mesafe), bant genişliği değişimi (sıkışma -> açılma), SMA20 eğimi. Bölge özeti: üst fitil baskınlığı (üst fitil / alt fitil oranı), uzun üst fitilli mum sayısı, büyük mum sayısı, başlangıç bağlamı (önceki düşüş). Görsel okuma (doğrulanacak): dipten sonra küçük mumlar, uzun üst fitiller, kısa alt fitiller, yükselen dipler, fiyat alt banttan SMA20'nin üstüne geçip üst banda yürüyor, bant önce dar.

## 3. Tespit kodu (C)

Kayan pencerede (bölge uzunluğu L ve L ± %20 zaman esnetmesi) iz ile benzerlik puanı S (0-1): standartlaştırılmış ölçü uzaklığı + mum dizisi eşlemesi (DTW ya da sabit hizalama; birini seç, gerekçesini yaz). TEPESİZ İZ: son tepe mumları (daire sonundaki uzun üst fitilli 2-3 mum ve üst bant yürüyüşü) çıkarılmış ikinci şablon; 'fiyatın en tepesi olmadan' testleri bununla.

## 4. Sentetik tutturma testi (D), tekrar tekrar

- Üretici: gerçekçi mum serisi (gerçek veriden blok bootstrap getiri + gerçek fitil dağılımı; ayrıca saf rastgele yürüyüş). İçine izi gömer: gürültü düzeyi %0 / 10 / 20 / 30 (ortalama boy oranı), ölçek x0,5..x2, zaman esnetmesi ±%20, bağlam üç tür (düşüş sonrası dip, yatay, yükseliş ortası / tepe).
- Her koşulda en az 200 tohum. Ölçü: YAKALAMA (gömülü izin bulunma oranı, konum ± 3 bar), YANLIŞ ALARM (gömülmemiş seride 1.000 bar başına eşiği geçen pencere), birebir tutturma (gömülü izin ölçüleriyle bulunan pencerenin ölçüleri arasındaki ortalama mutlak fark / korelasyon). Tam iz ve TEPESİZ iz ayrı.
- Eşik seçimi: %20 gürültüde YAKALAMA >= %80 veren en yüksek S eşiği; bu eşik ön kayda yazılır, sonra değişmez.

## 5. Gerçek veride (E), ön kayıttan sonra, açık veri <= 2022-12-31

- Panel: TEZGÂH 2 P2 havuzu ABD + AVR günlük (karar), BIST V_BIST bilgi. Her hisse için eşiği geçen pencereler (aynı hissede 15 bar tekil).
- BENZERLİK: eşiği geçen pencere sıklığı (hisse-yıl başına) gerçek veride vs sentetik rastgele seride (aynı uzunluk); S dağılımı.
- KONUM: eşleşmelerin ne kadarı fiyatın tepesinde (pencere sonu son 120 barın en yüksek kapanışının %3 içinde) ve ne kadarı başka yerde (dip / orta), tam iz ve tepesiz iz için ayrı.
- SONRASI (BİLGİ, karar değil): pencere sonu t, giriş t+1 açılış, R15 eşli fark (CETVEL2 v2.2 konum eşi) ve +%5 stop'tan önce (stop = pencere en düşük Low x 0,98) payı; hücre ABD 2016-19 / 2020-22, AVR aynı; plasebo şans tabanı sayıyla. KASA KURALI: tek iz, kasa açılmaz; en fazla 'birleşik iz bileşeni adayı'.
- Görsel: en yüksek puanlı 12 eşleşme (tepede 6, başka yerde 6) + rastgele 8 eşleşme, sonrası 15 mumla, hisse adı ve tarih kapalı değil (bu kör set değil, kontrol seti).

## 6. Çıktılar

arastirma_cikti/mum_izi/: MUM_IZI_ON_KAYIT.md, MUM_IZI_RAPOR.md, mum_izi_sonuc.json, iz tablosu (csv), sayısallaştırma bindirmesi PNG, MUM_IZI_GORSEL.pdf (sayfa 1: Cemal'in görüntüsü + kodun gördüğü mumlar; sayfa 2: parmak izi tablosu düz dille; sayfa 3: sentetik test tablosu; sonra eşleşmeler). Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.
