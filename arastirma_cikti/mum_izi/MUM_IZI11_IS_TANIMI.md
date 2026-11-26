# MUM_IZI EK 11 İŞ TANIMI — GÖZ ÖLÇÜMÜ: Cemal'in kendi 'benziyor' dediği bölgelerin sonrası (26 Kasım 2026)

Yazan: ana model. Durum: hakemin seçtiği 24 bölgede Cemal 7 BENZİYOR, 8 KISMEN (benzeyen yer: sondaki tırmanış), 9 BENZEMİYOR dedi (eşik 19 / 24: tespit yine geçersiz; hakem tam benzerlikte ilk formül setini geçemedi, kısmen benzerlikte geçti). Ama dört sette Cemal'in KENDİ gözüyle (sonrasını görmeden) etiketlediği ~104 bölge birikti (Ç192 planı: 100 etiket geçince göz ölçümü Cemal'in etiketleriyle koşulur). Bu iş kod tespitini değil CEMAL'İN ETİKETİNİ tespit sayar: 'Cemal'in benziyor dediği bölgeler sonrasında ne yapmış; benzemiyor dediklerinden ve eşlerinden farklı mı?'

## Kurallar
- CLAUDE.md kuralları aynen: yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31 (ufku kesiği aşan olay ölçülmez, sayısı yazılır), KASA açılmaz. Ön kayıt MUM_IZI11_ON_KAYIT.md (tanımlar, sınıf sayıları, KONTROL LİSTESİ) sonrası getirileri hesaplanmadan ÖNCE commit; kapı.
- Sonuç BİLGİ'dir: n < 30 olan her hücre 'örneklem yetersiz' etiketi taşır; 'iz / tuttu' sözü kullanılmaz; kasa kuralı (tek iz, kasa açılmaz).

## Örneklem
- Bölgeler: MUM_IZI4_ONAY (24), MUM_IZI6_ETIKET (48; 8'i set 1 tekrarı: tekrar sayfaları ayrı bölge sayılmaz, İLK işaret geçerlidir; iki tekrar sayfasında yanıt değişti: ayrıca duyarlılık satırı 'son işaretle'), MUM_IZI8_ONAY (24), MUM_IZI10_ONAY (24). Etiketler: cemal_mum_izi4_onay.json, cemal_mum_izi6_etiket.json, cemal_mum_izi8_onay.json, cemal_mum_izi10_onay.json ('isaret': EVET / HAYIR / KISMEN; IKISI / YOK / BELIRSIZ karar dışı). Anahtarlar: mum_izi4_onay_anahtar.json, mum_izi6_anahtar.json, mum_izi8_onay_anahtar.json, mum_izi10_onay_anahtar.json (+ hakem_aday/mum_izi10_aday_anahtar.json).
- Sınıflar: EVET, KISMEN, HAYIR. Zaman dilimi (günlük / haftalık) ayrı. Hepsi kodun önceden seçtiği adaylardır; HAYIR sınıfı EVET için doğal kontrol grubudur (aynı seçim hattı, fark yalnız Cemal'in gözü).

## Ölçü (her bölge için; mumun kendi zaman diliminde)
- Giriş = bölgenin son mumundan sonraki ilk geçerli barın açılışı (haftalıkta: sonraki haftanın ilk geçerli günü). Ufuk 15 mum (günlük 15 gün, haftalık 15 hafta); R15 = 15. mumun kapanışı / giriş - 1. Ayrıca 15 mum içinde en yüksek (max High / giriş - 1) ve en derin (min Low / giriş - 1); stop = bölgenin en düşük Low'u x 0,98; stop'tan önce dokunma: günlükte +%5 ve +%10, haftalıkta +%10 ve +%20. Bilgi: R30.
- Eş: aynı giriş günü, aynı kova (CETVEL2 v2.2 konum eşi, >= 5 eş), aynı takvim aralığı; eşli fark = R15 - eş ortalaması; eş bulunamayan olay eşli tabloya girmez (sayısı yazılır).
- Tablolar: sınıf x zaman dilimi: n, R15 ortalama ve MEDYAN, eşli fark ortalama ve medyan + olay bootstrap %95 (B 5000), artıda kapanan pay, dokunma payları, stop payı, en yüksek / en derin medyanı. Karşılaştırma: EVET - HAYIR farkı (R15 ve eşli fark) + permütasyon p (10.000); EVET + KISMEN birlikte ayrı satır. Pazar dağılımı (ABD / AVR / BIST) not edilir; BIST ayrı satır (bilgi).
- Olay listesi: mum_izi11_olay.csv (set, sayfa, sınıf, zaman, pazar, sembol, bölge başı / sonu, giriş, R15, eş, eşli fark, max, min, dokunmalar).

## Cemal'in göreceği dosya: MUM_IZI11_SONRASI.pdf (telefonda okunur)
- Sayfa 1 (tek sayfa, düz dil): 'Senin BENZİYOR dediğin N bölge sonrasında ne yaptı' tablosu (günlük / haftalık ayrı: kaçı 15 mumda artıda kapandı, ortalama ve medyan getiri, eşlerinin ortalaması, +%10'a kaçı dokundu, kaçı stop oldu), aynı satırlar KISMEN ve BENZEMİYOR için; altında tek cümle uyarı: 'Sayılar az (N < 30): bu bir sonuç değil, ilk bakış.'
- Sonra Cemal'in BENZİYOR dediği HER bölge bir sayfa (önce haftalık, sonra günlük; tarih sırasıyla): mum grafiği, bölge turuncu kutu, öncesi 15 mum, SONRASI 30 mum (veri kesiğini aşmaz; eksikse yazılır), Bollinger 20 + SMA20, giriş çizgisi, stop çizgisi, 15. mum dikey çizgi; hisse kodu + tarih AÇIK; altında: 15 mum getirisi, eş ortalaması, en yüksek / en derin. Sonra KISMEN bölgeleri aynı düzenle. BENZEMİYOR bölgeleri yalnız tabloda.

## Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI11_ON_KAYIT.md, MUM_IZI11_RAPOR.md (ÖRNEKLEM, TABLOLAR, KARŞILAŞTIRMA, KONTROL LİSTESİ, HATA, SAPMA, ÖNERİLEN DEFTER SATIRLARI), mum_izi11_sonuc.json, mum_izi11_olay.csv, MUM_IZI11_SONRASI.pdf. Kod: MUM_IZI_GOZ.py + test.
