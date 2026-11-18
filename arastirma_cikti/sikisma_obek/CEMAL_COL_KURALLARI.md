# Cemal'in çöl kuralları — işaretli grafiklerden çıkarılan taslak (15 Kasım 2026; S6 tasarım girdisi)

Kaynak: Cemal'in 15 Kasım'da gönderdiği 10 ekran görüntüsü (ENJSA x3, DESA, KNFRT, TUCLK x2, YKSLN, PAPIL) ve notları. Kodun karar günleri V_BIST verisinden (SIKISMA_OBEK.so_s5) çıkarıldı; "ekranda" denen yerler fotoğraftan okunmuştur ve TAHMİNDİR (tarih çıkarsanmaz). Bu taslak Cemal onaylayınca S6 ön kaydının tasarım kuralı olur; eşikler onaydan sonra, sonuç görülmeden yazılır.

## Kurallar (taslak)
- K1 BÖLGE = TABANIN TAMAMI: tabanın başladığı yerden kırılım mumuna kadar; 15 barlık parça değil. Uzunluk en az 8 mum (5 alt sınır), çoğu 40-70 mum (DESA 41 / 70, KNFRT ~2 ay, TUCLK 2025 ~2,5 ay, YKSLN Mart-Mayıs).
- K2 SINIR MUMLARDAN: tabanın tavan ve dip çizgileri; mumlar bu bandın içinde kalır. Band kısa bölgede %5-8, uzun tabanda %20'ye kadar (DESA %20). Bitişik parçalar tek bölge; tek mumluk bölge yok.
- K3 SAKİN: bölgenin ilk-son kapanış farkı küçük (aday <= %5). Eğimli pencere çöl değil (ENJSA 1 Eyl 2021 +%8, 18 Eki 2021 +%9,7: YANLIŞ; 16 Kas 2021 +%0,3: DOĞRU).
- K4 DÜŞÜŞ SONRASI VE DİP SAVUNULUR: kayan düşüş kanalı çöl değil ("çöl yok, BB yok, daralma yok": TUCLK 13 Ağu 2026, kod BB yüzdeliği 0,04 görse de). Daralma zamanla gözle görünür olmalı; dip koruması olmalı (PAPIL "dip koruması var").
- K5 KÜÇÜK MUM: mumlar hissenin normalinden küçük; 0,75 x ATR250 bazen fazla sıkı (ENJSA May-Haz 2025: medyan mum ATR'nin %82'si, Cemal: çöl).
- K6 AL MUMU: tabanın tavanını kıran büyük mum; giriş bu mumda ya da sonrasında, S5 karar gününde değil (KNFRT: en büyük gün 14 Eyl 2022 +%10; TUCLK: 22 Ağu 2025 +%10). Tavan kırılmadan alım yok (PAPIL: "tavan kırıldı mı? yok; alış mumu aslında buradaydı").
- K6b TAVAN MUMU (Cemal, PAPIL düzeltmesi): büyük çölün tavanı, taban içindeki sivri tepe mumudur (PAPIL: 5-6 Kas 2025, 6 Kas tepesi 20,32 düzeltilmiş fiyat; büyük aralık, yüksek hacim, kapanış geri içeride). O tepeden yatay çizgi çekilir; bu yatayı KAPANIŞLA kıran mum al mumudur. Küçük taban (PAPIL 13 Kas - 9 Ara, bant %8,7) için kendi tepesi (21 Kas 16,72) ve kendi kırılımı (10 Ara büyük mum, kapanışla 11 Ara) geçerlidir; kodun 3 Ara karar günü küçük bölgenin içidir, al günü değil. UYARI (veri): PAPIL'de 20,32 yatayı kapanışla ilk kez 2 Mar 2026'da kırıldı ve o gün 2026'nın en yüksek kapanışıydı (20,48): büyük çöl kuralıyla alım tam tepeye denk gelirdi; 19,12 (5 Kas kapanışı) ile 27 Oca 2026, sonraki en yüksek kapanış 20,14 (+%3). Küçük tabanın kırılımı (11 Ara 17,01) 19 Ara'da 18,35'e (+%8) gitti, sonra söndü. Yani tavan kırılımı tek başına yetmez; S6'da al mumu kuralı bu örnekle birlikte (başarısız kırılım) sınanır.
- K7 ÇÖL AYLARCA SÜREBİLİR: başlangıç doğru görülse bile giriş mumu aylar sonra gelebilir (YKSLN: çöl Mart-Nisan 2026'da başladı, giriş mumu Mayıs); düşüşten sonra ikinci çöl olabilir ama riskli (YKSLN Ağu 2026, sonra çöküş).
- K8 STOP: taban kırılınca çıkış (YKSLN Temmuz stop; üretim T6 kuralıyla aynı).

## Etiketler (kodun karar günü = veriden; Cemal'in bölgesi = notundan)
| Hisse | Kod karar günü (pencere) | Kod ölçüleri | Cemal | Ders |
|---|---|---|---|---|
| KNFRT | 2022-08-16 YOL (27 Tem-16 Ağu) | net +1,4 öbek 7,2 bbp 0,20 | parça (X) YANLIŞ; "çöl" = Haz/Tem-Ağu tabanının tamamı; "al mumu" = kırılım mumu (Ağu sonu-Eyl; veride en büyük gün 14 Eyl +%10) | K1, K6 |
| TUCLK | 2026-08-13 DİP (24 Tem-13 Ağu) | net -1,0 öbek 4,6 bbp 0,04 dd120 -27 | "çöl yok, BB yok, daralma yok" (XX) YANLIŞ | K4 |
| TUCLK | 2025-07-28 YOL (7-28 Tem) | net +4,5 öbek 4,9 bbp 0,20 | parçalar (X) yanlış; bölge = Haz-Ağu 2025 tabanının tamamı (yeşil daire); kırılım 22 Ağu +%10 | K1, K6 |
| YKSLN | 2026-04-09 DİP (19 Mar-9 Nis) | net -2,8 öbek 4,2 bbp 0,09 | "çöl burada başlamış, güzel çöl" DOĞRU; giriş mumu Mayıs; stop Temmuz | K7, K8 |
| YKSLN | 2026-08-26 DİP (6-26 Ağu) | net +1,8 öbek 3,6 bbp 0,12 dd120 -25 | "tekrar çöl vermiş ama girmek yürek ister" (sonra çöküş) | K7 |
| PAPIL | 2025-12-03 DİP (13 Kas-3 Ara); Cemal: '3 Ara olmaz; küçük bölge için 10 Ara (kırılım mumu) olur' | net -1,2 öbek 2,9 bbp 0,13 dd120 -60 | Eki-Kas 2025 tabanı (siyah elips), "dip koruması var"; "tavan kırıldı mı? yok; alış mumu aslında buradaydı" | K4, K6 |
| PAPIL | 2026-01-13, 04-08, 05-18, 06-23 DİP | düşüş içinde (dd120 -20..-43) | işaret yok | — |
| ENJSA | 2021-09-01, 2021-10-18 YOL | net +8,0 / +9,7 | X YANLIŞ | K3 |
| ENJSA | 2021-11-16 YOL | net +0,3 | "tamamı" DOĞRU | K1, K3 |
| ENJSA | 2025-02-18 YOL | — | 1. bölge DOĞRU | — |
| ENJSA | (karar yok) 2025-05-08..06-27 | (a) küçük mum düşürüyor (0,82 x ATR) | çöl | K5 |
| DESA | 2021-10-26, 2022-01-07 DİP | parçalar | TEK bölge 27 Eki-23 Ara 2021 (ya da 2 Şub 2022'ye), bant %20 | K1, K2 |
| FENER | 2025-10-31.. | S5 tuttu | 14 Eki-7 Kas (kısmi örtüşme) | K1 |
| CCOLA | 2025-09-02 / 10-02 | S5 tuttu | 2-15 Eki | — |
| ENJSA | (bant %23) | S5 dışı | 28 Tem-12 Eyl 2025 | K2 |

## S6 tasarımı için sonuç
Kodun bulduğu "parçalar" çoğunlukla gerçek tabanın içinde ama tabanın kendisi değil: S6'da bölge, karar günü penceresinden değil tabanın tamamından (başlangıç: sert düşüşün bitip dibin savunulduğu yer; bitiş: tavanı kıran al mumu) tanımlanır; ölçüler (küçük mum, bant, net değişim, BB daralması, dip koruması) tabanın tamamında ölçülür; yanlış pozitifler (kayan düşüş kanalı, eğimli pencere) K3-K4 ile elenir. Kalibrasyon: bu 16 etiket + Cemal'in ekleyeceği yeni bölgeler; eşikler ön kayıtta, sonuç görülmeden.

## Mum parmak izi denemesi (Cemal, 16 Kas: PAPIL Kas-Ara 2025 bölgesi; 'alt fitil yok, üst fitil biraz uzun = has yukarı çıkma mumları; öbek olunca')
Ölçü (V_BIST, geçerli bar): alt fitil / aralık, alt fitil < %10 olan bar payı, üst fitil / aralık, kapanışın aralıktaki konumu, yeşil payı.

| Bölge | n | alt fitil medyan | alt fitil yok payı | üst fitil medyan | kapanış konumu | yeşil payı |
|---|---|---|---|---|---|---|
| PAPIL küçük taban 13 Kas-9 Ara 2025 | 19 | 0,12 | 0,47 | 0,44 | 0,17 | 0,26 |
| PAPIL bütün günler | 1.700 | 0,18 | 0,34 | 0,26 | 0,38 | 0,43 |
| FENER (doğru) | 18 | 0,17 | 0,28 | 0,31 | 0,38 | 0,44 |
| CCOLA (doğru) | 10 | 0,12 | 0,30 | 0,22 | 0,23 | 0,30 |
| ENJSA Kas 2021 (doğru) | 15 | 0,40 | 0,00 | 0,31 | 0,50 | 0,33 |
| DESA (doğru) | 41 | 0,26 | 0,20 | 0,33 | 0,43 | 0,51 |
| YKSLN (doğru) | 34 | 0,18 | 0,21 | 0,35 | 0,37 | 0,50 |
| TUCLK 2025 (doğru) | 35 | 0,32 | 0,14 | 0,28 | 0,47 | 0,51 |
| ENJSA May-Haz 2025 (çöl) | 34 | 0,32 | 0,18 | 0,18 | 0,63 | 0,53 |
| ENJSA Eyl 2021 (YANLIŞ) | 15 | 0,22 | 0,33 | 0,29 | 0,58 | 0,67 |
| ENJSA Eki 2021 (YANLIŞ) | 15 | 0,32 | 0,20 | 0,38 | 0,44 | 0,67 |
| TUCLK Ağu 2026 (YANLIŞ) | 15 | 0,10 | 0,53 | 0,31 | 0,17 | 0,27 |

Sonuç: PAPIL bölgesinin parmak izi (alt fitil yok %47, üst fitil uzun, kapanış dipte 0,17, çoğu kırmızı) Cemal'in öteki DOĞRU bölgelerinde YOK (alt fitil yok payı %0-30, kapanış konumu 0,37-0,50); en çok benzeyen bölge TUCLK Ağu 2026 (YANLIŞ). Yani 'alt fitilsiz, üst fitilli öbek' etiket kümesinde çölün ortak izi değil; PAPIL'e özgü. Kural adayı olmadı; ileride etiket çoğalırsa yeniden bakılır.

### Fitil öbeği etiketleri (Cemal, 16 Kas; 'kesin tanı, yüzlerce örnek var')
| Bölge (Cemal) | n | alt fitilsiz payı | üst fitil medyan | kapanış konumu | yeşil | ASİM | Kod S+ günü | Sonrası |
|---|---|---|---|---|---|---|---|---|
| TEHOL 2024-12-01..2025-05-28 (tek yapı; parmak izi Mayıs'ta) — Mayıs 2025 | 18 | %78 | 0,66 | 0,03 | %17 | +0,52 | 17/18 | 60 günde 7,57 -> 14,79 (+%95) |
| TEHOL Ara 2024 - Şub 2025 (aynı yapının yükseliş bacağı) | 64 | %36-45 | 0,02-0,26 | 0,70-0,98 | %64-77 | -0,10..+0,09 | 0 | 0,87 -> 9,83 |
| BINBN 2024-12-17..2025-01-21 ('en net') | 25 | %52 | 0,59 | 0,11 | %20 | +0,42 | 17 (23 Ara'dan) | — |
| PAPIL 2025-11-13..12-09 | 19 | %47 | 0,44 | 0,17 | %26 | +0,26 | 14 | 11 Ara kırılım, +%8 sonra söndü |
| DGXX 2026-10-27..11-13 (ters: S- beklenen) | 14 | — | 0,18 | 0,56 | — | -0,10 | S- tutmadı (üst fitilsiz payı %30) | 2,50 -> 2,02 |

Not: Cemal'in 'Şubat 2026' yazdığı TEHOL etiketi düzeltildi (2024 Aralık - 28 Mayıs 2025). Kod (Ç187 S+ tanımı) üç S+ örneğini de algılıyor: hata 'algılama' halkasında değil; bağlam (taban içi) ve ölçü (60 gün yerine kırılım / 20 gün) halkaları HALKA_IS_TANIMI.md ile sınanıyor.

### Kör set sonucu (17 Kas; 50 sayfa, Cemal işaretledi; anahtar arastirma_cikti/fitil_obek/kor_anahtar.json, yanıtlar kor_cevap_cemal.json)
| Kodun grubu | n | E | B | H |
|---|---|---|---|---|
| S+ taban içi | 15 | 6 | 6 | 3 |
| S+ taban dışı | 15 | 6 | 8 | 1 |
| S+ düz dip | 10 | 3 | 7 | 0 |
| S- (ters) | 10 | 4 | 5 | 1 |

Kodun S+ sayfalarında 'benim mumum' payı B dahil %38 (B hariç paydada %79), S- sayfalarında %40 (B hariç %80); önceden yazılı kurala göre karar KISMİ (SAĞLAM için S+ E >= 0,60 VE S+ - S- farkı >= 0,30 gerekirdi; fark sıfır: kod S+ ile S- sayfalarını Cemal'in gözünde ayıramıyor). Yani S+ tanımı (fitil asimetrisi + alt fitilsiz pay) Cemal'in gözünü yakalamıyor; Cemal'in E dediği 19 sayfanın sonraki 60 gün getirisi medyan -%2,4 (RTALB +%560 hariç ortalama +%3,7), B dediklerinin +%1,9: n küçük, gözün öngörüsü de bu sette görünmüyor.

Cemal'in notlarından çıkan kurallar (S+ tanımının eksikleri):
- K10 SAVUNMA HATTI: şekil aynı olsa bile savunulan seviye (dip / üst hat) kırılmışsa 'aşağı', kırılmamışsa 'yukarı' (sayfa 41, 37, 38, 28). Sinyal = şekil + hat sağlam; kodda hat yok.
- K11 YOL ALMIŞ = KOVALAMA YOK: mumlar doğru ama fiyat zaten çıkmışsa giriş değil (24, 25, 21, 20); içindeysen son büyük mumda büyük kısmı satılır (20, 24).
- K12 DÖNÜM MUMU vs YÖN MUMU: düşüşün son mumları 'son nokta' diyorsa dönüm (22, 3, 9: akümülasyon); yalnız yön gösteren mumlar (4, 2, 1) sinyal değil.
- K13 TEPEDE DİKKAT: aynı şekil tepede (sol tepe mumları aşağı göstermişse) alım değil (14, 27, 8).
- K14 KAVGA: alt tabanda savunma var ama her yükselişte satıcı çıkıyorsa belirsiz (19, 18, 23, 5); yatay / stabil (11, 33) sinyal değil.
- K15 KİM ALIYOR: akümülasyonda alıcının kurumsal olup olmadığı önemli (9) — AKD verisi ücretsiz yok (K25 / Ç171 notu).

### Kör set 2 dersleri (17 Kas akşam; Cemal'in el yazısıyla işaretlediği FITIL_V2_KOR_SET.pdf; tam metin arastirma_cikti/fitil_v2/KOR2_DERS_CEMAL.md)
Cemal soruyu mum gününe göre değil formasyona göre yanıtladı (26 yanıt: E 2, H 13, B 11; 14 yanıtsız). Kodun 'tam girilir' günleri Cemal'in girişi değil. Çıkan kurallar (K16-K29; hepsi ölçülmedi, kural defteri K1-K14 ile aynı):
- K16 HEDEF KÜÇÜK: formasyon hedefi +%5..+%10; 60 gün ölçüsü bunu ölçmez; hedef sonrası yeni yapı belirler (No 4).
- K17 İKİ SAVUNMA İKİ YÖN: düz taban yukarı (hedef önceki tepe), düz tavan aşağı (hedef önceki dip) (No 4, 6, 8, 14, 20, 23).
- K18 KUBBE: şemsiye aşağı, kazan yukarı (No 5, 21).
- K19 DÖNÜŞ GÖRÜLMEDEN GİRİŞ YOK: çanak sağ kenarı yükselmeden alım yok (No 5, 9; H'lerin ana nedeni).
- K20 KIRIK TABANIN HÜKMÜ YOK (No 3, 12). K21 TUTMAYAN DİP güven yok (No 16, 18, 24). K22 KÜÇÜCÜK YAPI güven vermez; boy düşüşle orantılı (No 7, 13, 17, 28).
- K23 KAĞIT HAFIZASI: aynı hissede önceki formasyonlar hedefe gittiyse güven artar, patladıysa biter (No 8, 11, 25) — kodda hiç yok, Cemal'in en ağır şartı.
- K24 SAT MUMU: düz tavandan kopan ilk büyük kırmızı mum (No 8, 10, 14, 20). K25 ÇEKİŞTİRME = belirsiz, bekle (No 22, 27; REEDR). K26 OLUŞUM YOKSA yön önceki yol; kod 'yapı yok' diyebilmeli (No 2, 19, 26, 29).
- K27 DEV TEK MUM varsa kağıt şüpheli (No 1). K28 ÜÇ KEZ TEPEN TABAN (No 10, düşük öncelik). K29 GERİ TEST hedefi büyütür; asıl giriş retest (No 15; A4 ile aynı).
- K30 UFUK 15 MUM (17 Kas akşam, 'bunu kaydet'): kodun gördüğü yapılar en fazla 15 mumun geleceğini gösterir; 60 gün ölçüsünde rolleri yok. Eski 20-60 mumlu büyük çöller fon iziydi; gerçek hissede giriş-çıkış eşit, küçük yapılar, hedef <= 15 mum. Yapı ölçümlerinde karar ufku 15 bar (CLAUDE.md).
- K31 SON DERS (17 Kas akşam): fon çöllerinin kuralları gerçek ve geçerli (alt fitili az mumlar + dip savunması = yukarı; tersi aşağı) ama etkisi kısa: hedef %5-10, ufuk 15 mum. Eski çöle benzer yapı = manipülasyon şüphesi; kurum girişinde benzer yapı en fazla 3-5 gün.
- K32-K42 (17 Kas akşam, YAPI_HEDEF PDF notları; sonuç görülerek yazıldı, sınanacak; tam metin arastirma_cikti/yapi_hedef/CEMAL_DEGERLENDIRME_2026-11-17.md): büyük desen önce; hat >= 3 dokunuş ve eğimi aşağı değil; giriş mumu gerçek kırılım (pay + gövde); kazan şemsiye değil (iki kenar, dipte küçük mum, savunma); stop uzaklığı <= %10 ya da ana stop %5, stop büyük dip; hedef önceki tepe, ters formasyonda çık; hafıza = benzer yapı patladıysa girme; dip savunması şart; zayıf hat +%5; patlamış / 10 barlık yapı yok; tavan = ilk dip yapısının tavanı.
- K43-K46 (18 Kas, hakem PDF'i): fitil teorisi (üst fitil = satıcı emiliyor, alt fitil = alıcı yok; fitilsiz kısım yukarıdaysa ters); giriş teyidi iki gün kapanış (kapalı 'giriş onayı' konusuyla çelişir, Cemal kararı); parmak izi = alış mumundan önceki 4 mum öbeği; kazan = olur / şemsiye = olmaz. HAKEM SONUCU: kör yarıda Cemal ile vekil göz uyumu %26 (kappa -0,13); Cemal 19'da 8 OLUR; vekil göz Cemal'in gözü değil (Ç192 yorumu düzeltildi).
