# MUM_IZI EK 2 İŞ TANIMI — ENSRI grafiğinin parmak izi ve ilk izle ortak noktalar (25 Kasım 2026)

Yazan: ana model. Cemal (25 Kas 13:00, ORNEK2_ENSRI_25Kas.jpg): "Buradaki parmak izini çıkar; yukarıda önce verdiğim parmak izi ile bütün ortak noktaları metrik olarak yaz."

## Kurallar
- MUM_IZI_IS_TANIMI.md kuralları aynen (yasak dosyalar, yalnız kendi yollarını commit, KASA açılmaz, eşik oynanmaz). MUM_IZI.py'nin ölçü fonksiyonları AYNEN kullanılır (33 ölçü, aynı tanım); yeni ölçü eklenmez, eşik / şablon / ön kayıt değişmez. Ek kod gerekiyorsa MUM_IZI.py'ye yeni alt komut (`iz2`) ya da ayrı küçük dosya; test_mum_izi.py geçmeye devam etmeli.
- 2022-12-31 sonrası gerçek fiyat verisi OKUNMAZ (ENSRI 2024-25 dahil): sayısallaştırma yalnız görüntüden, sağlama bindirme PNG + eksen etiketleriyle.

## 1. Sayısallaştırma
- Görüntü: ENSRI, '5Y' görünümü, 12 mum (soldaki ilk mum kısmen kesik olabilir: kesikse ayrı işaretle), fiyat ekseni etiketli (TL 0,50 .. 7,00): piksel -> TL doğrusal kalibrasyon (en az 4 etiketle, artık hata yazılır). Mum aralığı büyük olasılıkla AYLIK (5 yıllık görünüm, yıl etiketleri arası ~3-4 mum); varsayım raporda yazılır.
- Her mum: O, H, L, C (TL), renk; Bollinger üst ve alt çizgi (orta çizgi / SMA20 görünmüyorsa orta = (üst + alt) / 2 olarak türetilir ve 'türetildi' diye yazılır). Üstte 'Piyasa Fiyatı TL 2,23' yazıyor, mumlar ~TL 4 düzeyinde: bu çelişki yalnız NOT edilir (neden aranmaz, veriye bakılmaz).
- Sağlama: bindirme PNG (kodun gördüğü mumlar görüntünün üstünde), mum sayısı ve renk dizisi elle sayımla aynı; rastgele 3 mum elle piksel doğrulaması (K10).

## 2. Parmak izi 2 ve karşılaştırma
- Aynı 33 ölçü ENSRI bölgesi için (bütün 12 mum = bölge; ayrıca 'tepesiz' karşılığı yok, tek sütun).
- ORTAK NOKTA tanımı (önceden sabit): her ölçü için gerçek açık verideki (ABD + AVR + BIST, <= 2022-12-31; MUM_IZI taramasının kullandığı pencere dağılımı; yoksa aynı panelden rastgele 20.000 pencere, tohum sabit, L = 20 ve L = 12 ayrı) yüzdelik konumu hesaplanır: p1 (iz 1, L = 20 dağılımında), p2 (iz 2, L = 12 dağılımında). ORTAK = ikisi de aynı uçta: p1 >= 0,75 ve p2 >= 0,75 (ikisi de YÜKSEK) ya da p1 <= 0,25 ve p2 <= 0,25 (ikisi de DÜŞÜK). GÜÇLÜ ORTAK = 0,90 / 0,10. ZIT = biri >= 0,75 öteki <= 0,25. Kalanı SIRADAN / AYRI.
- Çıktı tablosu: ölçü | düz dil | iz 1 | iz 2 | p1 | p2 | sınıf (GÜÇLÜ ORTAK / ORTAK / ZIT / AYRI). Ayrıca: iki iz arasında ön kayıtlı S benzerlik puanı (iz 2'ye iz 1 şablonu uygulanınca; L farkı zaman esnetmesi sınırını aşıyorsa 'S uygulanamaz' yazılır ve ölçü uzaklığı bileşeni verilir).
- ŞANS TABANI: rastgele iki pencere (biri L 20, biri L 12; 5.000 çift) aynı kuralla kaç ORTAK ölçü veriyor (ortalama, %95 üst sınır)? İki izin ORTAK sayısı bu tabanla yan yana yazılır. 33 ölçü birbirine bağımlı: 'ortak nokta çok' sözü yalnız taban aşılırsa.
- ORTAK ÖLÇÜLERLE BİRLEŞİK KURAL (yalnız BİLGİ, kasa açılmaz): GÜÇLÜ ORTAK + ORTAK ölçülerin hepsini aynı uçta (0,75 / 0,25 eşiği) taşıyan pencereler açık veride kaç tane (ABD / AVR / BIST, L 12-20), tepede / başka yerde payı, R15 eşli fark ve +%5 payı vs eş (MUM_IZI 'sonrası' fonksiyonuyla, aynı hücreler, plasebo taban). n < 30 ise 'örneklem yetersiz'. Bu kural iki örnekten türetildiği için sonucu EZBER RİSKLİ diye etiketlenir; karar etiketi verilmez.

## 3. Çıktılar
arastirma_cikti/mum_izi/: mum_izi2_mumlar.csv, mum_izi2_bindirme.png, mum_izi2_karsilastirma.csv, mum_izi2_sonuc.json, MUM_IZI2_RAPOR.md (başlıklar: SAYISALLAŞTIRMA, PARMAK İZİ 2, ORTAK NOKTALAR, ŞANS TABANI, BİRLEŞİK KURAL (BİLGİ), KONTROL LİSTESİ, HATA, SAPMA, ÖNERİLEN DEFTER SATIRLARI), MUM_IZI2_GORSEL.pdf (sayfa 1: iki grafik yan yana + kodun gördüğü mumlar; sayfa 2: ortak noktalar tablosu düz dille; sayfa 3: şans tabanı ve birleşik kural).
