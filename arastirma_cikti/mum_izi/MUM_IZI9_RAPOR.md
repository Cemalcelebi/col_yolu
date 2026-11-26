# MUM_IZI9 RAPOR (2026-11-26): v6 = v5M ∧ küçük mum ∧ muntazam dizilim ∧ net Bollinger daralması

İş tanımı: MUM_IZI9_IS_TANIMI.md (fd454da). Ön kayıt: MUM_IZI9_ON_KAYIT.md (fcf7c32). Kod: MUM_IZI_V6.py, test_mum_izi9.py (8 / 8). Etiketler KULLANILDI (iç örnek;
ezber riski). GETİRİ / SONRASI YOK. Veri <= 2022-12-31. PDF ana modelin ön elemesinden sonra Cemal'e gidecek.

## SONUÇ (tek bakışta)

- Seçilen kapılar: KÜÇÜK MUM = K3 (bölgenin medyan mum boyu / önceki 60 bar <= 1,14); DİZİLİM = D3 (tırmanış kapanışlarının doğrusallığı R² >= 0,60); DARALMA = BB4 (en dar bant noktası bölgenin %25-90 arasında).
- v6 bu etiketlerde HAYIR'ların %89'unu (16 / 18) reddediyor, EVET'lerin hepsini (6 / 6) geçiriyor: eşikler bu 6 EVET'e oturtulduğu için iyimser.
- Evrende v6, v5M bölgelerinin yalnız ~%40-50'sini eliyor (etiketlerdeki %89'un yarısı): etiket kümesindeki ayrım evrene taşınmıyor olabilir.
- Sentetik ölçüt GEÇMEDİ: pozitif %10 gürültüde %39 (ölçüt %40); tek dev mumla çıkış (n8, geçerli) %23 VAR (ölçüt %10); n1 / n2 / n5 ve rastgele geçti; 'daralmasız' (n9) ve 'dağınık' (n10) kurgusu seçilen ölçülerle doğrulanamadı.
- MUM_IZI9_ONAY.pdf: 26 sayfa (kapak + şablonda okuma + 24 rastgele v6 bölgesi). Yol: arastirma_cikti/mum_izi/MUM_IZI9_ONAY.pdf.

## ETİKET KÜMESİ (doğrulandı)

- EVET 6: MUM_IZI8_ONAY s5, s8 (2) + önceki 61'de v5M VAR olup EVET (set 1: 3, set 2: 1).
- HAYIR 18: MUM_IZI8_ONAY BENZEMİYOR (17) + önceki 61'de v5M VAR olup HAYIR (set 1: 1).
- Karar dışı (MUM_IZI8): IKISI 1 (s9), işaretsiz 4 (s20, 21, 24, 26).
- MUM_IZI8 sayfalarında anahtardaki k yeniden hesaplananla aynı ve hepsi v5M VAR; önceki 61'de v5M mum_izi8_aday.csv ile aynı.

## ADAY TABLOSU (eşik = EVET ve şablonun en kötüsü, %5 pay; puan = reddedilen HAYIR payı)

| aday | ölçü | yön | EVET min..maks | HAYIR medyan | şablon | eşik | reddedilen HAYIR |
|---|---|---|---|---|---|---|---|
| K1 | en büyük gövde (b) | küçük | 0,38..0,93 | 0,80 | 0,79 | 0,98 | 0,39 (7) |
| K2 | medyan mum boyu / bant | küçük | 0,18..0,40 | 0,20 | 0,30 | 0,42 | 0,00 |
| **K3** | medyan mum boyu / önceki 60 bar | küçük | 0,54..1,08 | 1,17 | muaf | 1,14 | **0,56 (10)** |
| K4 | çıkış mumu gövdesi (b) | küçük | 0,02..0,57 | 0,60 | 0,79 | 0,83 | 0,06 (1) |
| D1 | en büyük kapanış adımı (b) | küçük | 0,39..1,06 | 0,75 | 0,73 | 1,12 | 0,17 (3) |
| D2 | mum örtüşmesi | büyük | 0,63..0,89 | 0,72 | 0,81 | 0,60 | 0,00 |
| **D3** | tırmanış doğrusallığı R² | büyük | 0,63..0,90 | 0,76 | 0,94 | 0,60 | **0,44 (8)** |
| D4 | tırmanış mum boyu değişkenliği | küçük | 0,28..1,35 | 0,40 | 0,97 | 1,42 | 0,00 |
| BB1 | en dar bant / ilk 3 mum | küçük | 0,12..0,84 | 0,78 | 0,71 | 0,88 | 0,33 (6) |
| BB2 | en dar / en geniş bant (önceki 20 dahil) | küçük | 0,12..0,70 | 0,44 | 0,60 | 0,74 | 0,06 (1) |
| BB3 | daralma yüzdeliği (120 bar) | küçük | 0,01..0,74 | 0,41 | muaf | 0,78 | 0,11 (2) |
| **BB4** | en dar nokta bölgenin %25-90'ında | ikili | hepsi evet | evet | evet | - | **0,39 (7)** |

## SEÇİM

- K* = K3 (0,56), D* = D3 (0,44), BB* = BB4 (0,39); üçü de >= 0,15: üç kapı da kondu.
- v6 = v5M ∧ K3 <= 1,138 ∧ D3 >= 0,601 ∧ BB4: HAYIR'ların %88,9'unu (16 / 18) reddediyor (DUR eşiği %50: geçti); EVET'lerin %100'ü geçiyor (tanım gereği).
- Önceki setlerde v6 VAR ve Cemal'in yanıtı (iç örnek; eşikler bunlara oturtuldu):
  - MUM_IZI4 (set 1, 24 sayfa): v5M VAR 4 (3 EVET, 1 HAYIR) -> v6 VAR 3, üçü de EVET.
  - MUM_IZI6 (set 2, 37 karar): v5M VAR 1 (EVET) -> v6 VAR 1 (EVET).
  - MUM_IZI8 (24 sayfa, hepsi v5M): v6 VAR 7: EVET 2, HAYIR 2, işaretsiz 2, iki kutu 1.
- Not: 'net daralma' için seçilen BB4 daralmanın ŞİDDETİNİ ölçmüyor (yalnız en dar noktanın yeri); şiddet ölçüleri (BB1 / BB2 / BB3) daha az HAYIR ayırdı. 'Küçük mum' için seçilen K3 tek dev çıkış mumunu görmüyor (K4 yalnız %6).

## SENTETİK (v6; bantlar sentetik seride yeniden hesaplanır; 200 tohum x 2 üretici x 2 bağlam x 3 gürültü)

| tür | kendi ölçüsü (ihlal payı) | geçerli mi | VAR (v5M) |
|---|---|---|---|
| pozitif | | | %35,4 (gürültü 0 / 0,1 / 0,2: 44,1 / 39,0 / 23,0) (v5M %45) |
| n1 fitilsiz büyük gövde | B (%99,7) | GEÇERLİ | %0 |
| n2 fitiller ters | M (%100) | GEÇERLİ | %0 |
| n5 yatay yol | T (%98,9) | GEÇERLİ | %0,3 |
| n8 tek dev mumla çıkış | çıkış gövdesi >= 1,2 b (%86,0) | GEÇERLİ | %23,4 |
| n9 daralmasız | BB* = BB4 (%53,5) | kurgu geçersiz | (%21,4) |
| n10 dağınık | D* = D3 (%53,0) | kurgu geçersiz | (%24,0) |
| rastgele | | | blok 0,19, ry 0,29 / 1.000 bar |

- Ölçüt: pozitif >= %40 GEÇMEDİ (%39,0); geçerli negatifler <= %10: n1 / n2 / n5 GEÇTİ, n8 GEÇMEDİ (%23,4); rastgele <= 0,5 GEÇTİ. Toplam GEÇMEDİ; kapakta yazıyor.
- n8 kurgusu iş tanımına göre 'sentetik bantta ölçülerek' kuruldu (kat 6 / 9 / 13,5 / 20 sırayla); ilk sabit 6 kat sürümü %72,6 geçerliydi (ön kayıtta yazılı).
- n9 / n10 geçersizliği kuralın zayıflığını gösteriyor: BB4 daralmanın varlığını / şiddetini, D3 mum boylarının dağınıklığını ölçmüyor (aynı kapanış yolu korunduğu için).

## SAYIM (tekil v6 VAR; MUM_IZI8 evreni; getirisiz)

| dilim / pazar | v6 olay (evren içi) | v5M olay (evren içi) | v6 / v5M (evren içi) | evren içi hisse-yıl başına |
|---|---|---|---|---|
| günlük ABD | 2.592 (1.681) | 5.288 (3.326) | 0,49 (0,51) | 0,071 |
| günlük AVR | 297 (219) | 611 (449) | 0,49 (0,49) | 0,058 |
| günlük BIST | 603 (423) | 1.197 (837) | 0,50 (0,51) | 0,162 |
| haftalık ABD | 735 (398) | 1.785 (1.013) | 0,41 (0,39) | 0,007 |
| haftalık AVR | 90 (59) | 221 (151) | 0,41 (0,39) | 0,006 |
| haftalık BIST | 177 (109) | 376 (235) | 0,47 (0,46) | 0,038 |

- v6 evrende v5M'nin yarısını tutuyor; etiket kümesinde ise HAYIR'ların yalnız %11'ini tutuyordu. Bu fark iç örnek eşiklerin iyimser olduğunu düşündürüyor.

## ONAY SETİ

- MUM_IZI9_ONAY.pdf: 26 sayfa. s1 'KOD NASIL TESPİT EDİYOR (v6)': eski kural tek satır, üç yeni şart ve ölçüsü (mum boyu / önceki 60 bar <= 1,14; tırmanış doğrusallığı >= 0,60; en dar nokta bölgenin ortasında), 'v5M'nin 17 benzemiyor sayfasından 15'ini artık eliyor; benziyor dediğin 2 sayfanın 2'si kalıyor', sentetik uyarısı. s2 şablonda okuma + mum yapısı + üç sayı. s3-26: 24 rastgele v6 bölgesi (haftalık 12, günlük 12; ABD 16, AVR 3, BIST 5), her birinde mavi / yeşil ok / turuncu okuma, mum yapısı satırı ve üç sayı (küçük mum, dizilim, daralma), ✓ / × kutuları. Hisse / tarih / sonrası yok (pdftotext 0 eşleşme).
- Seçim: evren içi tekil v6 olaylarından RASTGELE, tohum 25112093; uygun olay günlük 2.244, haftalık 545 (önceki üç setin hisseleri hariç); hisse başına bir; önceki setlerle kesişim 0; en geç bölge sonu 2022-11-18.
- Anahtar: mum_izi9_onay_anahtar.json (MÜHÜRLÜ; PDF'e girmez). Yol: /home/user/col_yolu/arastirma_cikti/mum_izi/MUM_IZI9_ONAY.pdf.
- Beklenti: v5M onayı 2 / 24 ✓ idi; v6 v5M bölgelerinin yarısını eliyor; MUM_IZI8 sayfalarında v6 VAR 7'nin 2'si EVET, 2'si HAYIR (karar verilen 4'te %50). Kaba beklenti %15-40 ✓; 19 / 24 beklenmiyor.

## KONTROL LİSTESİ

- K1 EVET: eşik EVET'lerden, puan HAYIR'lardan (iç örnek, yazıldı); negatifler kendi ölçüsünde doğrulandı; rastgele taban.
- K2 EVET: bütün ölçüler pencere sonuna kadarki veriyle; seri t'de kesilince aynı (test); KASA kapısı açık (en geç 2022-12-30).
- K3 EVET: geçerli bar, eksik haftalı pencere yok, BIST medyan üstü, ABD / AVR P2.
- K4 EVET: tekil < 15 mum en yüksek v1 S; hisse başına bir; etiketlerde her sayfa bir kez.
- K5 UYGULANMAZ. K6 EVET. K7 EVET.
- K8 EVET: EVET 6 / HAYIR 18 çok küçük; aralık ve iç örnek uyarısı yazıldı.
- K9 EVET: ön kayıt (fcf7c32) taramadan önce; v6_kapi tarama başında geçti.
- K10 EVET: etiket şeması bilinmeyen değerde durur; MUM_IZI8 sayfalarında k ve v5M anahtarla aynı.
- K11 EVET: 85 etiket penceresinde 12 ölçü vektörlü = düz döngü (fark olsa durur).
- K12 EVET: seçim önceden yazılı kuralla; 'iz' sözü yok.
- K13 EVET: eski kodlar, defterler, UC_IZ2 değişmedi; yalnız kendi yollarım commit.
- K14 UYGULANMAZ.

## HATA

1. (kurgu; benim) n8 ilk sürümde sabit katla kuruldu (iş tanımı 'sentetik bantta ölçülerek kurulur' diyordu); ön kayıttan önce düzeltildi (geçerlilik %72,6 -> %86,0).
2. (sunum; benim) PDF ilk üretimde bölge sayfalarındaki üç sayı satırı sağdan taştı ve sayfa 2'de BB4 'şablonda ölçülemez' yazıyordu (BB4 şablonda ölçülür: evet). Metin üç satıra bölündü, BB4 düzeltildi, PDF yeniden üretildi (ilk PDF silindi, gönderilmedi). Ön kayıttan sonraki tek kod değişikliği (SAPMA 1).
3. (yorum sınırı) v6'nın etiketlerdeki %89 HAYIR reddi eşiklerin 6 EVET'e oturtulmasından; evrende v5M'nin ancak yarısı elendi. Bu sayı 'v6 HAYIR'ları ayırıyor' diye okunmamalı.

## SAPMA

1. Ön kayıttan sonra MUM_IZI_V6.py'de yalnız PDF metni değişti (üç sayı satır kırılımı ve sayfa 2'de BB4 yazısı); kural ve eşikler aynı (ESIK9_SHA 233dd753 değişmedi; KOD9_SHA ön kayıtta 2129b71d, şimdi a9dc5640). Tarama ön kayıtlı kodla koştu.
2. Başka sapma yok.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç236: MUM_IZI EK 9 v6 = v5M ∧ K3 (mum boyu / önceki 60 bar <= 1,14) ∧ D3 (tırmanış R² >= 0,60) ∧ BB4 (en dar nokta ortada). Etiket kümesi EVET 6 / HAYIR 18 (iç örnek): HAYIR reddi %89. Evrende v5M'nin %40-50'si kalıyor. Sentetik GEÇMEDİ (pozitif %39; tek dev mum n8 %23); n9 / n10 seçilen ölçülerle doğrulanamadı (BB4 daralma şiddetini, D3 mum boyu dağınıklığını ölçmüyor). MUM_IZI9_ONAY.pdf (24 rastgele v6 bölgesi) ana modelde, sonra Cemal'e. Getiri yok. Commit a42bcb0 / fcf7c32 / (sonuç).
- IK_GOREV: 26 Kas, EK 9 v6 + onay PDF'i; açık: ana model ön eleme, Cemal'in işaretleri.
- IK_HATA: n8 negatifi ilk sürümde iş tanımına aykırı sabit katla kuruldu (kurgu; ön kayıttan önce düzeltildi; ders: 'ölçülerek kur' denen negatif ölçerek kurulur).
- IK_ACIK: Cemal MUM_IZI9_ONAY.pdf'i işaretler; >= 19 / 24 ✓ değilse sözlü şartların (küçük, muntazam, net daralma) ölçüsü yeniden düşünülmeli: seçilen K3 / D3 / BB4 Cemal'in sözcüklerini dar karşılıyor (dev çıkış mumu, daralma şiddeti, mum boyu dağınıklığı görülmüyor).
