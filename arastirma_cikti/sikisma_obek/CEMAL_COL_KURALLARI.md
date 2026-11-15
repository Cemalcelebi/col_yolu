# Cemal'in çöl kuralları — işaretli grafiklerden çıkarılan taslak (15 Kasım 2026; S6 tasarım girdisi)

Kaynak: Cemal'in 15 Kasım'da gönderdiği 10 ekran görüntüsü (ENJSA x3, DESA, KNFRT, TUCLK x2, YKSLN, PAPIL) ve notları. Kodun karar günleri V_BIST verisinden (SIKISMA_OBEK.so_s5) çıkarıldı; "ekranda" denen yerler fotoğraftan okunmuştur ve TAHMİNDİR (tarih çıkarsanmaz). Bu taslak Cemal onaylayınca S6 ön kaydının tasarım kuralı olur; eşikler onaydan sonra, sonuç görülmeden yazılır.

## Kurallar (taslak)
- K1 BÖLGE = TABANIN TAMAMI: tabanın başladığı yerden kırılım mumuna kadar; 15 barlık parça değil. Uzunluk en az 8 mum (5 alt sınır), çoğu 40-70 mum (DESA 41 / 70, KNFRT ~2 ay, TUCLK 2025 ~2,5 ay, YKSLN Mart-Mayıs).
- K2 SINIR MUMLARDAN: tabanın tavan ve dip çizgileri; mumlar bu bandın içinde kalır. Band kısa bölgede %5-8, uzun tabanda %20'ye kadar (DESA %20). Bitişik parçalar tek bölge; tek mumluk bölge yok.
- K3 SAKİN: bölgenin ilk-son kapanış farkı küçük (aday <= %5). Eğimli pencere çöl değil (ENJSA 1 Eyl 2021 +%8, 18 Eki 2021 +%9,7: YANLIŞ; 16 Kas 2021 +%0,3: DOĞRU).
- K4 DÜŞÜŞ SONRASI VE DİP SAVUNULUR: kayan düşüş kanalı çöl değil ("çöl yok, BB yok, daralma yok": TUCLK 13 Ağu 2026, kod BB yüzdeliği 0,04 görse de). Daralma zamanla gözle görünür olmalı; dip koruması olmalı (PAPIL "dip koruması var").
- K5 KÜÇÜK MUM: mumlar hissenin normalinden küçük; 0,75 x ATR250 bazen fazla sıkı (ENJSA May-Haz 2025: medyan mum ATR'nin %82'si, Cemal: çöl).
- K6 AL MUMU: tabanın tavanını kıran büyük mum; giriş bu mumda ya da sonrasında, S5 karar gününde değil (KNFRT: en büyük gün 14 Eyl 2022 +%10; TUCLK: 22 Ağu 2025 +%10). Tavan kırılmadan alım yok (PAPIL: "tavan kırıldı mı? yok; alış mumu aslında buradaydı").
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
| PAPIL | 2025-12-03 DİP (13 Kas-3 Ara); ekranda üçgen ~6 Kas çizgisinde (fark: fiyat düzeltmesi / geçerli bar sayımı, kontrol edilecek) | net -1,2 öbek 2,9 bbp 0,13 dd120 -60 | Eki-Kas 2025 tabanı (siyah elips), "dip koruması var"; "tavan kırıldı mı? yok; alış mumu aslında buradaydı" | K4, K6 |
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
