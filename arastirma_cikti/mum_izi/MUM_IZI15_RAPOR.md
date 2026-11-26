# MUM_IZI15 RAPOR — kopma ayrımı (26 Kasım 2026)

Etiket: **BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK** (bütün gruplar n < 30 ya da tek dönem; ölçüt Cemal 128 bölgenin sonrasını gördükten sonra söylendi). Karar vermez; asıl sınama EK 14 setidir (set 6).

Ön kayıt: MUM_IZI15_ON_KAYIT.md (commit f7ed0871287e8d8a5dd09e3b1adddc665d92fa6b 2026-11-26T11:46:03+00:00); kapı geçti (kontrol listesi 14 / 14, sha'lar eşit, ağaç temiz). Kod: MUM_IZI_GOZ2.py `kopma` (KOD15_SHA d5f19876109e86326c3bc5d4877a20a65711d38f34284494856bdccaeb6d10fd). Satırlar mum_izi13_olay.csv'den aynen (OLAY13_SHA fc27c506ae981157f13b2aeb534e2c9c098a947ad0b158130f0c5845f73dcec8); yeni getiri hesabı yok. Eşi olan satır sayısı denetimi: es_neden boş 117 = fark sonlu 117.

## SONUÇ

- **Okuma kuralı (uzlaşı): OKUNAMADI (karşılaştırma yapılamaz).** Cemal'in EVET dediği 36 bölgede iki hakemin birlikte BASKI dediği bölge 1 (haftalık), günlükte 0: KOPMUS - BASKI karşılaştırması yapılamaz (ön kayıtta önceden yazıldı).
- **Okuma kuralı (duyarlılık): OKUNAMADI (karşılaştırma yapılamaz).** BASKI* (ort. puan <= 4) EVET içinde haftalık 1, günlük 0.
- EVET içinde KOPMUS (uzlaşı) eşli fark ortalaması: haftalık -6.1% (n 10), günlük +6.0% (n 7). Karşılaştırılabilen tek grup KARISIK: haftalık -30,8% (n 7), günlük -6,7% (n 5); KOPMUS - KARISIK ön kayıtta karşılaştırma değildi, yalnız bilgi.
- Hakemler 128 bölgenin 70'ine birlikte KOPMUS, yalnız 9'una birlikte BASKI dedi (BASKI'ların 8'i Cemal HAYIR günlük). Ayrım Cemal'in EVET'lerinde neredeyse hiç BASKI üretmedi: bu sette hakem ayrımı EVET'leri ikiye bölmüyor.
- ÜÇÜNCÜ (128, Cemal'den bağımsız): günlükte KOPMUS - BASKI eşli fark farkı +9,3 puan (p 0,036; n 30 / 8), birlikte +7,7 (p 0,17; n 64 / 9), haftalık yapılamaz (BASKI n 1). Duyarlılıkta günlük +8,4 (p 0,036; n 44 / 10), haftalık -20,1 (p 0,25; n 47 / 2), birlikte +0,6 (p 0,93). Yön günlükte Cemal'in dediği gibi, haftalıkta ölçülemedi ya da ters; çoklu karşılaştırma düzeltmesi yok, iki dönem yok.
- BİLGİ (Spearman, EVET bölgelerinde ort. hakem puanı ~ eşli fark): haftalık rho +0.11 (n 18, p 0.65), günlük +0.64 (n 12, p 0.026), birlikte +0.36 (n 30, p 0.048). Günlükte puan arttıkça eşli fark artıyor; haftalıkta ilişki yok.
- Hakem uyumu: 128 bölgede üç sınıf kappa 0.44 (uyum %71; Ç210-216 sınırı 0,40'ın hemen üstü); bütün 144 sayfada 0.45; puan Spearman 0.74. KOPMUS / BASKI çatışması yalnız 3 sayfada (K1 BASKI, K2 KOPMUS); öteki 34 ayrılık BELIRSIZ üzerinden.
- Hakemin kendi tutarlılığı (set2 tekrar = set1: s7=23, s8=19, s9=16, s20=11, s26=9, s28=10, s34=26, s46=6): K1 aynı k 7 / 8, K2 8 / 8; puan farkı ikisinde de 0,00 (hakem aynı görüntüyü tanımış olabilir: yukarı yanlı).
- Eş sınırı (Ç229 / Ç240): eşler bölgenin kendi koşusuyla eşlenmedi.

## Tablolar

### ANA (Cemal EVET, 36) — UZLAŞI

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS | 12 | 10 | +4.7% | +6.1% | -6.1% | -3.3% | %50 | %50 |
| haftalik | BASKI | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| haftalik | KARISIK | 7 | 7 | -20.7% | -6.0% | -30.8% | -13.1% | %29 | %14 |
| gunluk | KOPMUS | 10 | 7 | -0.4% | -2.0% | +6.0% | +2.5% | %30 | %71 |
| gunluk | BASKI | 0 | 0 | - | - | - | - | - | - |
| gunluk | KARISIK | 6 | 5 | -3.8% | -2.3% | -6.7% | -5.9% | %33 | %20 |
| birlikte | KOPMUS | 22 | 17 | +2.4% | -1.2% | -1.1% | +1.9% | %41 | %59 |
| birlikte | BASKI | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| birlikte | KARISIK | 13 | 12 | -12.9% | -3.0% | -20.7% | -10.7% | %31 | %17 |

- haftalik: karşılaştırma yapılamaz (eşi olan n 10 / 1)
- gunluk: karşılaştırma yapılamaz (eşi olan n 7 / 0)
- birlikte: karşılaştırma yapılamaz (eşi olan n 17 / 1)

### ANA (Cemal EVET, 36) — DUYARLILIK (ort. puan)

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS* | 17 | 15 | -4.5% | -1.4% | -17.6% | -8.6% | %41 | %40 |
| haftalik | BASKI* | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| haftalik | ARA* | 2 | 2 | -6.1% | -6.1% | -6.3% | -6.3% | %50 | %0 |
| gunluk | KOPMUS* | 15 | 11 | -1.6% | -1.6% | +1.3% | +1.9% | %33 | %55 |
| gunluk | BASKI* | 0 | 0 | - | - | - | - | - | - |
| gunluk | ARA* | 1 | 1 | -3.0% | -3.0% | -5.9% | -5.9% | %0 | %0 |
| birlikte | KOPMUS* | 32 | 26 | -3.1% | -1.5% | -9.6% | -6.2% | %38 | %46 |
| birlikte | BASKI* | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| birlikte | ARA* | 3 | 3 | -5.1% | -3.0% | -6.2% | -5.9% | %33 | %0 |

- haftalik: karşılaştırma yapılamaz (eşi olan n 15 / 1)
- gunluk: karşılaştırma yapılamaz (eşi olan n 11 / 0)
- birlikte: karşılaştırma yapılamaz (eşi olan n 26 / 1)

### İKİNCİ (EVET + KISMEN, 52) — UZLAŞI

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS | 17 | 15 | +7.5% | +13.1% | -1.8% | +3.8% | %59 | %60 |
| haftalik | BASKI | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| haftalik | KARISIK | 8 | 8 | -17.8% | -3.8% | -26.6% | -10.7% | %38 | %25 |
| gunluk | KOPMUS | 15 | 12 | +0.4% | -1.6% | +4.0% | +2.2% | %40 | %67 |
| gunluk | BASKI | 0 | 0 | - | - | - | - | - | - |
| gunluk | KARISIK | 11 | 9 | -4.2% | -3.0% | -4.4% | -4.2% | %27 | %22 |
| birlikte | KOPMUS | 32 | 27 | +4.2% | +0.6% | +0.8% | +2.2% | %50 | %63 |
| birlikte | BASKI | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| birlikte | KARISIK | 19 | 17 | -9.9% | -3.0% | -14.8% | -5.0% | %32 | %24 |

- haftalik: karşılaştırma yapılamaz (eşi olan n 15 / 1)
- gunluk: karşılaştırma yapılamaz (eşi olan n 12 / 0)
- birlikte: karşılaştırma yapılamaz (eşi olan n 27 / 1)

### İKİNCİ (EVET + KISMEN, 52) — DUYARLILIK (ort. puan)

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS* | 23 | 21 | -0.1% | +1.9% | -10.8% | +0.8% | %52 | %52 |
| haftalik | BASKI* | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| haftalik | ARA* | 2 | 2 | -6.1% | -6.1% | -6.3% | -6.3% | %50 | %0 |
| gunluk | KOPMUS* | 23 | 19 | -1.5% | -1.6% | +0.8% | +0.9% | %35 | %53 |
| gunluk | BASKI* | 0 | 0 | - | - | - | - | - | - |
| gunluk | ARA* | 3 | 2 | -1.9% | -3.0% | -3.0% | -3.0% | %33 | %0 |
| birlikte | KOPMUS* | 46 | 40 | -0.8% | -1.2% | -5.3% | +0.9% | %43 | %52 |
| birlikte | BASKI* | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| birlikte | ARA* | 5 | 4 | -3.6% | -3.0% | -4.7% | -5.1% | %40 | %0 |

- haftalik: karşılaştırma yapılamaz (eşi olan n 21 / 1)
- gunluk: karşılaştırma yapılamaz (eşi olan n 19 / 0)
- birlikte: karşılaştırma yapılamaz (eşi olan n 40 / 1)

### ÜÇÜNCÜ (128 bölgenin tamamı) — UZLAŞI

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS | 36 | 34 | +6.8% | +9.3% | -1.5% | -3.2% | %58 | %47 |
| haftalik | BASKI | 1 | 1 | -1.7% | -1.7% | -10.5% | -10.5% | %0 | %0 |
| haftalik | KARISIK | 25 | 23 | -0.2% | -3.3% | -9.7% | -6.0% | %44 | %35 |
| gunluk | KOPMUS | 34 | 30 | +3.2% | +0.6% | +2.4% | +2.1% | %50 | %60 |
| gunluk | BASKI | 8 | 8 | -8.7% | -0.6% | -6.9% | -2.8% | %38 | %38 |
| gunluk | KARISIK | 24 | 21 | -1.1% | -1.4% | -4.0% | -4.2% | %33 | %33 |
| birlikte | KOPMUS | 70 | 64 | +5.0% | +2.7% | +0.3% | +1.2% | %54 | %53 |
| birlikte | BASKI | 9 | 9 | -7.9% | -0.8% | -7.3% | -5.2% | %33 | %33 |
| birlikte | KARISIK | 49 | 44 | -0.6% | -1.6% | -7.0% | -4.8% | %39 | %34 |

- haftalik: karşılaştırma yapılamaz (eşi olan n 34 / 1)
- gunluk: KOPMUS - BASKI eşli fark farkı +9.3%, p 0.036 (n 30 / 8)
- birlikte: KOPMUS - BASKI eşli fark farkı +7.7%, p 0.170 (n 64 / 9)

### ÜÇÜNCÜ (128 bölgenin tamamı) — DUYARLILIK (ort. puan)

| zaman | grup | n | n_es | R15 ort | R15 med | eşli fark ort | eşli fark med | artıda | eşinden iyi |
|---|---|---|---|---|---|---|---|---|---|
| haftalik | KOPMUS* | 49 | 47 | +0.2% | +0.3% | -8.0% | -6.0% | %51 | %40 |
| haftalik | BASKI* | 2 | 2 | +14.5% | +14.5% | +12.1% | +12.1% | %50 | %50 |
| haftalik | ARA* | 11 | 9 | +18.1% | +4.3% | +7.6% | -4.3% | %55 | %44 |
| gunluk | KOPMUS* | 50 | 44 | +2.4% | -0.8% | +0.6% | +1.0% | %46 | %52 |
| gunluk | BASKI* | 10 | 10 | -6.9% | -0.6% | -7.8% | -6.8% | %40 | %30 |
| gunluk | ARA* | 6 | 5 | -6.5% | -3.6% | -3.4% | -0.2% | %17 | %40 |
| birlikte | KOPMUS* | 99 | 91 | +1.3% | -0.7% | -3.9% | -2.7% | %48 | %46 |
| birlikte | BASKI* | 12 | 12 | -3.3% | -0.6% | -4.5% | -6.8% | %42 | %33 |
| birlikte | ARA* | 17 | 14 | +9.4% | -3.0% | +3.7% | -2.2% | %41 | %43 |

- haftalik: KOPMUS - BASKI eşli fark farkı -20.1%, p 0.248 (n 47 / 2)
- gunluk: KOPMUS - BASKI eşli fark farkı +8.4%, p 0.036 (n 44 / 10)
- birlikte: KOPMUS - BASKI eşli fark farkı +0.6%, p 0.927 (n 91 / 12)


## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşli fark mum_izi13_olay.csv'den aynen (aynı giriş günü aynı kova CETVEL2 konum eşi); yeni eş yok; sınır: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240) |
| K2 | geleceğe bakma | EVET | hakemler sonrasını görmedi (işaretsiz PDF bölge sonunda kesik; yasak liste hakem metninde); hakem json'ları hesaptan önce commit; SINIR: ölçüt Cemal sonrasını gördükten sonra söylendi -> GERİYE DÖNÜK |
| K3 | geçerli bar | EVET | geçerli bar kuralı MUM_IZI11 / 13 ölçümünde (MI.mi_veri H > L, V > 0); bu iş bar okumaz |
| K4 | tekilleştirme | EVET | 128 tekil bölge (GZ.gz_ornek K4 denetimi); set2 T tekrar sayfaları ayrı bölge sayılmaz, yalnız hakem tutarlılığında kullanılır |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (MUM_IZI11 tanımı, csv aynen) |
| K6 | veri birimi | EVET | getiriler oransal, csv aynen; pazarlar arası karşılaştırma eşli farkla |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | bütün gruplar n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; n < 2 grup 'karşılaştırma yapılamaz'; tek dönem (<= 2022), BH yok (karar yok) |
| K9 | ön kayıt | EVET | bu ön kayıt (KOD15 / EK15 / hakem / olay sha + getirisiz sayımlar) hesaptan önce commit; k15_kapi sha + commit + temiz ağaç denetler |
| K10 | ayrıştırma | EVET | hakem json şeması denetlenir (k ve puan aralığı; bilinmeyen değer DUR); (set, sayfa) eşleşmesi 128 / 128 değilse DUR; tekrar eşlemesi anahtardan |
| K11 | yeniden üretim | EVET | tablo sayılarından >= 2 hücre olay csv'sinden bağımsız pandas koduyla yeniden üretilir (rapor öncesi denetim) |
| K12 | ifade | EVET | 'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; okuma kuralı yalnız yön |
| K13 | süreç | EVET | çakışma kapısı korunur; çalışan komutlar değişmez (test); yasak defter dosyalarına dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez |

K11 yeniden üretim (bağımsız pandas, mum_izi15_olay.csv): ANA uzlaşı haftalık KOPMUS (n 12, R15 ort +4,68%, eşli fark ort -6,09% / med -3,29%, eşinden iyi %50) ve ÜÇÜNCÜ uzlaşı günlük KOPMUS - BASKI (+9,34 puan, perm p 0,0360, tohum 15) ve EVET birlikte Spearman (0,364) birebir aynı.

## HATA

- H-a (süreç): iki hakem aynı geçici klasörü paylaştı; K2 ara notlarının ezildiğini bildirdi. Hakem bağımsızlığı kesin değil (kappa 0,44 bu yüzden yukarı yanlı olabilir).
- H-b (ifade, küçük): ön kayıttaki 'Önceden bilinen sonuçlar' notu "yalnız ÜÇÜNCÜ günlük ve birlikte hesaplanabilir" dedi; duyarlılıkta ÜÇÜNCÜ haftalık da hesaplanabilirdi (BASKI* n_es 2). Ön kayıttaki n < 2 listesi (makine çıktısı) doğruydu; hesaba etkisi yok.
- H-c (yöntem sınırı): tekrar sayfalarında puanların birebir aynı olması tutarlılığı değil, görüntü tanımayı ölçüyor olabilir.
- H-d (süreç notu): MUM_IZI_GOZ2.py değiştiği için MUM_IZI13 ön kaydındaki KOD13_SHA artık eşleşmez; `kos` zaten sonuç varken durur, MUM_IZI13 yeniden koşulmaz (bilgi).

## SAPMA

Yok. Grup, eşik, tohum ve okuma kuralı ön kayıttaki gibi; n < 2 gruplar 'karşılaştırma yapılamaz' bırakıldı. Kodda ön kayıttan sonra değişiklik yok (KOD15_SHA kapıda eşit).

## ÖNERİLEN DEFTER SATIRLARI

- IK_KAYIT (Ç yeni): MUM_IZI EK 15 kopma ayrımı (iki sonrasını-görmeyen hakem, 128 bölge, mum_izi13_olay.csv aynen). Okuma kuralı OKUNAMADI: Cemal EVET 36 bölgede uzlaşı BASKI 1 (günlük 0); karşılaştırma yapılamaz. ÜÇÜNCÜ (128) günlük KOPMUS - BASKI eşli +9,3 puan (p 0,036, n 30 / 8), haftalık yapılamaz. Kappa 0,44. BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK. Asıl sınama EK 14 set 6.
- IK_GOREV: 26 Kas 2026 MUM_IZI15 kopma gruplaması (kod 0aeb71a, ön kayıt f7ed087, sonuç <bu commit>); karar yok.
- IK_HATA: hakemler ortak geçici klasör kullandı, K2 ara notları ezildi (süreç; bulan K2; etkisi: bağımsızlık kesin değil; ders: her hakeme ayrı geçici klasör).
- IK_ILERI: kopma ayrımı (KOPMUS - BASKI eşli fark, 15 mum) set 6 (EK 14, Cemal sonrasını görmeden) geldiğinde aynı `kopma` tanımıyla; aynı eşik (uzlaşı, puan 6 / 4, tohum 15).
