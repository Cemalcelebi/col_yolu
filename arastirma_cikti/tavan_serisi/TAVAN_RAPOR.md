# Çökmüş hissede art arda tavan: k. tavandan sonra katılmak (BIST 2016 - Ağu 2026)

Ön kayıt 4c5da06 (2026-11-13T11:33:22+00:00), mühür b6cccebae0a0; SAPMA: ön kayıttan sonra üç değişiklik: (1) ts_donem kriz sonrası BİLGİ olaylarında 'tanim' anahtarında çöküyordu, döngü sırası düzeltildi; (2) rapor metni: sonuç cümlesi 'örneklem yetersiz' k'ları ayrı yazıyor, kontrol kapsamı satırı, n < 30 dönem sütunu; (3) rapora düz dille özeti. Tanım, eşik, ölçü aynı.

## Sonuç

**Hiçbir k'da 'kontrolden iyi' değil.** KUMAR (beklenen değer kontrolden iyi değil): k = 1. Örneklem yetersiz (n < 30, karar yok): k = 2, 3, 4, 5, 6, 8, 10.

Duyarlılık (BİLGİ, karara girmez): eşik %-60: n >= 30 olan k = 1, 2, 3, 4, 5; bunlardan medyan farkın %95 aralığı tamamen 0'ın altında olan: 1, 2, 3, 4, 5; eşik %-70: n >= 30 olan k = 1, 2, 3; bunlardan medyan farkın %95 aralığı tamamen 0'ın altında olan: 1, 2, 3.

Düz dille:
- Çökmüş hissede 1. tavandan sonraki gün açılıştan katılan (120 olay, 38 hisse): ertesi gün de tavan %35; 60 günde medyan %-10; +%100'e ulaşan %9, -%50'ye düşen %7 (120 günde %15); tavan yapmayan eş çökmüşlere göre medyan fark %-3,9.
- Çökmüş hissede 2. tavandan sonraki gün açılıştan katılan (42 olay, 24 hisse): ertesi gün de tavan %40; 60 günde medyan %-18; +%100'e ulaşan %7, -%50'ye düşen %12 (120 günde %31); tavan yapmayan eş çökmüşlere göre medyan fark %-11,6.
- Çökmüş hissede 3. tavandan sonraki gün açılıştan katılan (18 olay, 15 hisse): ertesi gün de tavan %37; 60 günde medyan %-25; +%100'e ulaşan %11, -%50'ye düşen %11 (120 günde %18); tavan yapmayan eş çökmüşlere göre medyan fark %-17,0.
- Çökmemiş hissede aynı durum (BİLGİ): 1. tavandan sonra 60 günde medyan %0, +%100 %13, -%50 %3.
- Fon krizi sonrası (Eylül - Kasım 2026, BİLGİ): çökmüş hissede 1. tavandan sonra ertesi gün de tavan %56, 3. tavandan sonra %66 (geçmişte %35 / %37): seriler bu dönemde daha uzun; sonucu henüz bilinmiyor.

## Olasılık tablosu (ÇÖKMÜŞ hisse, giriş k. tavandan sonraki gün açılış)

| k | n (hisse) | ertesi gün de tavan | 60g medyan getiri | 60g'de +%100'e dokunma | 60g'de -%50'ye dokunma | 120g'de -%50 | kontrol 60g -%50 | medyan fark (60g) | %95 aralık | karar |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 120 (38) | %35 | %-10 | %9 | %7 | %15 | %0 | %-3,9 | [-14,5, 9,4] | KUMAR: beklenen değer kontrolden iyi değil |
| 2 | 42 (24) | %40 | %-18 | %7 | %12 | %31 | %0 | %-11,6 | [-27,5, 5,0] | örneklem yetersiz |
| 3 | 18 (15) | %37 | %-25 | %11 | %11 | %18 | %0 | %-17,0 | [-26,9, 25,7] | örneklem yetersiz |
| 4 | 7 (7) | %86 | %-11 | %14 | %0 | %0 | %0 | %18,5 | [-37,8, 32,4] | örneklem yetersiz |
| 5 | 6 (6) | %67 | %-13 | %17 | %0 | %0 | %0 | %16,7 | [-52,2, 43,7] | örneklem yetersiz |
| 6 | 4 (4) | %100 | %-17 | %0 | %25 | %33 | %0 | %1,5 | [-27,4, 30,4] | örneklem yetersiz |
| 8 | 2 (2) | %100 | %-20 | %0 | %0 | %0 | %0 | %17,4 | — | örneklem yetersiz |
| 10 | 1 (1) | %0 | %-30 | %0 | %0 | — | %0 | %-5,5 | — | örneklem yetersiz |

Kontrol kapsamı: k=1: farkı ölçülen 63, kontrolsüz 57, olay başına kontrol hissesi medyanı 2; k=2: farkı ölçülen 22, kontrolsüz 20, olay başına kontrol hissesi medyanı 1; k=3: farkı ölçülen 11, kontrolsüz 7, olay başına kontrol hissesi medyanı 2; k=4: farkı ölçülen 3, kontrolsüz 4, olay başına kontrol hissesi medyanı 2; k=5: farkı ölçülen 3, kontrolsüz 3, olay başına kontrol hissesi medyanı 1; k=6: farkı ölçülen 2, kontrolsüz 2, olay başına kontrol hissesi medyanı 1; k=8: farkı ölçülen 1, kontrolsüz 1, olay başına kontrol hissesi medyanı 1; k=10: farkı ölçülen 1, kontrolsüz 0, olay başına kontrol hissesi medyanı 1.

Fark = olayın 60 gün getirisi - aynı gün, aynı derinlik kovasında çökmüş ama seri boyunca tavan yapmamış hisselerin ortalaması; aralık hisse kümeli bootstrap. 'Ertesi gün de tavan' bütün olaylardan; getiriler 60 gün penceresi 31.08.2026'dan önce biten olaylardan.

## Getiri dağılımı ve seri uzunluğu

| k | 5g medyan | 20g medyan | 60g medyan (ort.) [%25, %75] | 120g medyan | seri en az k+1 | k+3 | k+5 | dolum belirsiz payı | kontrol 60g medyan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | %-5 | %-6 | %-10 (%-3) [%-26, %12] | %-8 (n 94) | %35 | %5 | %3 | %2 | %-2 |
| 2 | %-11 | %-15 | %-18 (%-14) [%-33, %-0] | %-22 (n 32) | %40 | %13 | %9 | %2 | %-4 |
| 3 | %-8 | %-17 | %-25 (%-12) [%-37, %-0] | %-16 (n 11) | %37 | %21 | %11 | %6 | %-12 |
| 4 | %6 | %8 | %-11 (%6) [%-28, %13] | %-21 (n 4) | %86 | %57 | %29 | %0 | %-10 |
| 5 | %9 | %3 | %-13 (%-1) [%-34, %16] | %-40 (n 3) | %67 | %33 | %17 | %17 | %-21 |
| 6 | %-0 | %-14 | %-17 (%-20) [%-35, %-2] | %-46 (n 3) | %100 | %50 | %0 | %0 | %-13 |
| 8 | %-8 | %-12 | %-20 (%-20) [%-24, %-16] | %27 (n 1) | %100 | %0 | %0 | %50 | %-29 |
| 10 | %-18 | %-33 | %-30 (%-30) [%-30, %-30] | — (n 0) | %0 | %0 | %0 | %0 | %-25 |

## Dönemler (60g medyan fark; P(-%50) olay / kontrol)

| k | 2016-19 | 2020-22 | 2023-26.08 | yön tutan dönem |
|---|---|---|---|---|
| 1 | n 9: %-21,0; %20 / %0 | n 11: %10,8; %4 / %0 | n 43: %-2,3; %4 / %0 | 1 / 2 |
| 2 | n 3: %-34,1; %29 / %0 | n 5: %14,9; %7 / %0 | n 14: %-11,6; %10 / %0 | — (n < 30) |
| 3 | n 1: %-27,5; %0 / %0 | n 3: %23,5; %0 / %0 | n 7: %-17,0; %18 / %0 | — (n < 30) |
| 4 | n 0: —; — / — | n 1: %18,5; %0 / %0 | n 2: %-2,7; %0 / %0 | — (n < 30) |
| 5 | n 0: —; — / — | n 1: %16,7; %0 / %0 | n 2: %-4,3; %0 / %0 | — (n < 30) |
| 6 | n 0: —; — / — | n 0: —; %50 / — | n 2: %1,5; %0 / %0 | — (n < 30) |
| 8 | n 0: —; — / — | n 0: —; %0 / — | n 1: %17,4; %0 / %0 | — (n < 30) |
| 10 | n 0: —; — / — | n 0: —; — / — | n 1: %-5,5; %0 / %0 | — (n < 30) |

## Yalnız dolum belirsiz olmayan girişler (giriş günü tam kilitli tavan değil)

| k | n | 60g medyan | +%100 | -%50 | medyan fark [%95] | karar |
|---|---|---|---|---|---|---|
| 1 | 118 | %-10 | %9 | %7 | %-4,3 [-15,4, 9,4] | KUMAR: beklenen değer kontrolden iyi değil |
| 2 | 41 | %-19 | %7 | %12 | %-13,2 [-31,6, 4,9] | örneklem yetersiz |
| 3 | 17 | %-28 | %6 | %12 | %-21,4 [-26,9, 23,5] | örneklem yetersiz |
| 4 | 7 | %-11 | %14 | %0 | %18,5 [-37,8, 32,4] | örneklem yetersiz |
| 5 | 5 | %-22 | %20 | %0 | %-17,7 [-52,2, 16,7] | örneklem yetersiz |
| 6 | 4 | %-17 | %0 | %25 | %1,5 [-27,4, 30,4] | örneklem yetersiz |
| 8 | 1 | %-12 | %0 | %0 | %17,4 — | örneklem yetersiz |
| 10 | 1 | %-30 | %0 | %0 | %-5,5 — | örneklem yetersiz |

## Karşılaştırma: ÇÖKMEMİŞ hissede k. tavan (BİLGİ, kontrolsüz)

| k | n | ertesi gün tavan | 60g medyan | +%100 | -%50 |
|---|---|---|---|---|---|
| 1 | 16935 | %24 | %0 | %13 | %3 |
| 2 | 4120 | %35 | %-2 | %17 | %5 |
| 3 | 1465 | %45 | %-2 | %21 | %7 |
| 4 | 663 | %52 | %-0 | %24 | %9 |
| 5 | 346 | %59 | %0 | %28 | %8 |
| 6 | 203 | %64 | %1 | %32 | %11 |
| 8 | 79 | %71 | %-13 | %35 | %19 |
| 10 | 38 | %79 | %-12 | %37 | %29 |

## Duyarlılık: ÇÖKMÜŞ eşiği gevşek (BİLGİ, karara girmez)

| eşik | k | n (hisse) | ertesi gün tavan | 60g medyan | +%100 | -%50 (kontrol) | medyan fark [%95] | kural sonucu |
|---|---|---|---|---|---|---|---|---|
| %-60 | 1 | 935 (208) | %32 | %-7 | %9 | %5 (%1) | %-12,2 [-14,3, -10,1] | KUMAR: beklenen değer kontrolden iyi değil |
| %-60 | 2 | 300 (138) | %45 | %-13 | %11 | %7 (%1) | %-19,8 [-23,6, -15,4] | KUMAR: beklenen değer kontrolden iyi değil |
| %-60 | 3 | 139 (90) | %49 | %-15 | %11 | %9 (%1) | %-25,3 [-29,8, -19,9] | KUMAR: beklenen değer kontrolden iyi değil |
| %-60 | 4 | 69 (53) | %67 | %-14 | %14 | %10 (%0) | %-27,6 [-31,1, -18,7] | KUMAR: beklenen değer kontrolden iyi değil |
| %-60 | 5 | 47 (37) | %57 | %-20 | %11 | %9 (%1) | %-29,0 [-37,1, -20,4] | KUMAR: beklenen değer kontrolden iyi değil |
| %-60 | 6 | 27 (22) | %67 | %-14 | %7 | %15 (%0) | %-27,4 [-43,5, -17,7] | örneklem yetersiz |
| %-60 | 8 | 10 (10) | %60 | %-27 | %0 | %10 (%0) | %-45,5 [-85,4, -11,0] | örneklem yetersiz |
| %-60 | 10 | 2 (2) | %0 | %-38 | %0 | %50 (%0) | %-25,9 [-46,2, -5,5] | örneklem yetersiz |
| %-70 | 1 | 399 (106) | %34 | %-10 | %7 | %7 (%2) | %-11,3 [-15,0, -8,7] | KUMAR: beklenen değer kontrolden iyi değil |
| %-70 | 2 | 137 (75) | %47 | %-17 | %9 | %9 (%3) | %-18,1 [-22,7, -11,4] | KUMAR: beklenen değer kontrolden iyi değil |
| %-70 | 3 | 66 (49) | %47 | %-20 | %3 | %11 (%1) | %-24,6 [-30,1, -14,1] | KUMAR: beklenen değer kontrolden iyi değil |
| %-70 | 4 | 31 (28) | %66 | %-17 | %6 | %19 (%0) | %-18,1 [-34,1, -8,9] | örneklem yetersiz |
| %-70 | 5 | 21 (19) | %57 | %-22 | %5 | %19 (%0) | %-23,3 [-36,8, -5,2] | örneklem yetersiz |
| %-70 | 6 | 12 (10) | %50 | %-20 | %0 | %25 (%0) | %-21,6 [-33,9, 13,2] | örneklem yetersiz |
| %-70 | 8 | 2 (2) | %100 | %-20 | %0 | %0 (%0) | %17,4 — | örneklem yetersiz |
| %-70 | 10 | 1 (1) | %0 | %-30 | %0 | %0 (%0) | %-5,5 — | örneklem yetersiz |

## BİLGİ: fon krizi sonrası (Eylül 2026 - 2026-11-12) çökmüş hissede k. tavan (karara girmez)

| k | olay (hisse) | ertesi gün de tavan | seri hâlâ açık | 5g medyan (n) |
|---|---|---|---|---|
| 1 | 147 (68) | %56 (n 138) | 26 | %4 (111) |
| 2 | 77 (50) | %58 (n 71) | 17 | %-1 (56) |
| 3 | 41 (34) | %66 (n 38) | 11 | %4 (28) |
| 4 | 25 (23) | %82 (n 22) | 8 | %2 (14) |
| 5 | 18 (17) | %78 (n 18) | 5 | %-15 (11) |
| 6 | 14 (14) | %70 (n 10) | 5 | %-13 (9) |
| 8 | 3 (3) | %100 (n 3) | 0 | %-9 (3) |
| 10 | 1 (1) | %100 (n 1) | 0 | %-34 (1) |

## Tanım ve sınırlar

- ÇÖKMÜŞ: seri ilk tavanından önceki gün kapanışı, kendi son 250 barının en yüksek kapanışından en az %80 aşağıda. Tavan: 13.03.2020'den (BIST ±%10) günlük >= %9,5 (1-2 TL'de fiyat adımına göre gerçek tavan) ve <= %10,5; 12.03.2020'ye kadar (BIST ±%20) >= %19 ve <= %21; |günlük| > %25 veri kırığı.
- Kontrol: aynı referans günü, aynı derinlik kovası ((-%85, -%80], (-%90, -%85], <= -%90), seri boyunca tavansız, giriş günü işlem gören hisseler.
- Yanlılık: evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker); Yahoo BIST geçmişinde eksik bedelsiz düzeltmesi kırık kuralıyla ayıklanır; işlem maliyeti yok.
- Karar cümlesi (önceden yazılı): her k için: 'k. tavandan sonra katılmak kontrolden iyi' <=> n >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(-%50, 60g) <= 1,2 x kontrolün P(-%50, 60g) VE üç dönemin en az ikisinde dönem medyan farkı > 0 (n >= 10 olan dönemler; n < 10 dönem 'yön yok' sayılır); değilse 'kumar: beklenen değer kontrolden iyi değil'. n < 30 -> 'örneklem yetersiz'. 8 ayrı k sınanır: tek k'nın geçmesi çoklu deneme şansı olabilir, raporda yazılır.
