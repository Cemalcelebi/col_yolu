# ÇÖKÜŞ SONRASI OYNAK HİSSE — RAPOR (COKUS_OYNAK v1.0 (16 Kas 2026))

Üreten: `python COKUS_OYNAK.py kos`. Ön kayıt: ON_KAYIT.md (2026-11-16T13:13:43.943733+00:00); mühür `302eaeada2b3525b`. Koşu: 2026-11-16T13:19:16.894211+00:00.

## ÖZET (bulgu)

- Çöküşten (+5 gün) sonra en oynak beşlik, 250 günde: P(+%100) %73,9 (orta üç beşlik %77,9; kat 0,95), P(-%50) %2,9 (orta %0,5; kat 6,29); medyan r250 %74,8 / %110,5; n 69 / 217.
- Normal dönem 2017 başı: oynak P(+%100) %38,5 / orta %27,6 (kat 1,40); P(-%50) %1,9 / %0,0 (kat -).
- Normal dönem 2023 başı: oynak P(+%100) %21,5 / orta %21,5 (kat 1,00); P(-%50) %47,7 / %40,2 (kat 1,19).
- KARAR (önceden yazılı kural, OYNAK): **ÖLÇÜLEMEDİ**. En çok düşmüş beşlik: ÖLÇÜLEMEDİ; çapraz: ÖLÇÜLEMEDİ.
- Bugün (karar 2026-11-13): evren medyan 120 gün getirisi %-38,1 -> çöküş eşiği (-%30) GEÇİLDİ; piyango profilinde 45 hisse.
- Hayatta kalma: yalnız bugün işlem gören hisseler; batanlar yok -> P(-%50) gerçekte daha yüksek, P(+%100) daha düşük olabilir.

## ÇÖKÜŞ GÜNLERİ

| Olay | Tür | Çöküş günü | Medyan r120 | Karar | Giriş | Evren | Sonuçlu (bölünmesiz) | Bölünme şüphesiyle çıkan | Sonuç yok |
|---|---|---|---|---|---|---|---|---|---|
| 2023 | cokus | 2023-05-22 | %-30,3 | 2023-05-26 | 2023-05-29 | 455 | 443 | 12 | - |
| 2023 | cokus_ek20 | 2023-05-22 | %-30,3 | 2023-06-16 | 2023-06-19 | 458 | 445 | 13 | - |
| 2026 | cokus | 2026-10-13 | %-31,6 | 2026-10-19 | 2026-10-20 | 0 | 0 | 0 | giriş kriz kesiğinden (31.08.2026) sonra: 1 |
| 2018B | bilgi | 2018-08-20 | %-28,5 | 2018-08-31 | 2018-09-03 | 357 | 351 | 5 | - |
| 2020B | bilgi | 2020-03-19 | %-1,7 | 2020-03-25 | 2020-03-26 | 370 | 360 | 10 | - |
| N2017 | normal | - | %2,9 | 2016-12-30 | 2017-01-02 | 325 | 324 | 1 | - |
| N2023 | normal | - | %120,2 | 2022-12-30 | 2023-01-02 | 437 | 426 | 11 | - |

Tespit edilen bütün çöküş günleri: 2023-05-22, 2026-10-13. 2026 çöküşünün sonucu kriz kesiği (31.08.2026) yüzünden ölçülemez.

## OLASILIK TABLOSU (ana giriş: çöküş + 5 işlem günü açılışı; ufuk 250 işlem günü)

P(+%100) = 250 gün içinde bir kapanış >= 2 x giriş; P(-%50) = bir kapanış <= 0,5 x giriş. Kat = dilim / taban. Fark aralığı: hisse düzeyinde bootstrap %95 (1.000; birleşikte olay içi katmanlı). Perm. p: olay içi etiket karıştırma, tek yönlü (P+100). TABAN = σ250 orta üç beşlik (DUSMUS için düşüş orta üç beşliği TABAN_D). PROFIL = OYNAK ve zirveden >= %60 düşmüş.

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | OYNAK | 69 | %73,9 | %2,9 | %74,8 | %168,4 | %-0,2 | 0,95 | %-4,0 [%-15,0, %7,9] | 6,29 | %2,4 [%-0,9, %6,8] | 0,82 |
| 2023 | TABAN | 217 | %77,9 | %0,5 | %110,5 | %149,7 | %0,0 | 1 | | 1 | | |
| 2023 | DUSMUS | 68 | %76,5 | %1,5 | %85,5 | %97,8 | %0,0 | 0,95 | %-4,3 [%-15,8, %6,7] | - | %1,5 [%0,0, %4,4] | 0,83 |
| 2023 | TABAN_D | 218 | %80,7 | %0,0 | %120,0 | %164,2 | %0,0 | 1 | | 1 | | |
| 2023 | CAPRAZ | 23 | %65,2 | %4,3 | %64,9 | %75,6 | %-0,2 | 0,84 | %-12,7 [%-31,9, %6,6] | 9,43 | %3,9 [%-1,4, %12,6] | 0,95 |
| 2023 | PROFIL | 16 | %56,2 | %6,2 | %35,9 | %59,5 | %-1,0 | 0,72 | %-21,6 [%-45,1, %6,1] | 13,56 | %5,8 [%-1,4, %18,8] | 0,98 |

## KARAR (önceden yazılı kural)

- OYNAK: **ÖLÇÜLEMEDİ** — tamamlanmış çöküş 1 < 2. BH q (P+100, tek yönlü): 1,00.
- DUSMUS: **ÖLÇÜLEMEDİ** — tamamlanmış çöküş 1 < 2. BH q (P+100, tek yönlü): 1,00.
- CAPRAZ: **ÖLÇÜLEMEDİ** — tamamlanmış çöküş 1 < 2. BH q (P+100, tek yönlü): 1,00.
- BİLGİ (2018B + 2020B, geriye bakarak seçilmiş dip günleri; karar değil) OYNAK: DESTEKLENMEDİ — P100 farkı +0.002 [-0.068, +0.075], olay farkları 2018B +0.074, 2020B -0.088; M50 farkı +0.015 [-0.020, +0.053].
- BİLGİ (2018B + 2020B, geriye bakarak seçilmiş dip günleri; karar değil) DUSMUS: EMARE — P100 farkı +0.077 [+0.009, +0.141], olay farkları 2018B +0.091, 2020B +0.045; M50 farkı +0.006 [-0.023, +0.042].
- BİLGİ (2018B + 2020B, geriye bakarak seçilmiş dip günleri; karar değil) CAPRAZ: ÖLÇÜLEMEDİ — 2018B: n 29 / 170 < 30.
- Birincil karar OYNAK satırıdır; iki çöküş = iki olay olduğu için kural tutsa bile en fazla EMARE (İZ değil).

## EK GİRİŞ (bilgi): çöküş + 20 işlem günü

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | OYNAK | 69 | %66,7 | %4,3 | %82,6 | %107,7 | %-7,4 | 1,02 | %1,1 [%-11,1, %13,5] | - | %4,3 [%0,0, %10,1] | 0,49 |
| 2023 | TABAN | 218 | %65,6 | %0,0 | %83,3 | %123,6 | %-7,0 | 1 | | 1 | | |
| 2023 | DUSMUS | 68 | %60,3 | %1,5 | %68,8 | %90,8 | %-7,1 | 0,92 | %-5,5 [%-17,6, %7,8] | 3,22 | %1,0 [%-1,4, %4,4] | 0,82 |
| 2023 | TABAN_D | 219 | %65,8 | %0,5 | %83,9 | %129,4 | %-7,1 | 1 | | 1 | | |
| 2023 | CAPRAZ | 24 | %54,2 | %4,2 | %39,2 | %62,3 | %-7,3 | 0,83 | %-11,4 [%-32,8, %10,8] | - | %4,2 [%0,0, %12,5] | 0,90 |
| 2023 | PROFIL | 11 | %36,4 | %0,0 | %19,7 | %31,4 | %-7,6 | 0,55 | %-29,2 [%-57,9, %-1,0] | - | %0,0 [%0,0, %0,0] | 0,99 |

## BİLGİ: 2018 ve 2020 dip günleri (ana tanımda çöküş değil; geriye bakarak seçildi, karar dışı)

BİLGİ, karar dışı (olay sayımından sonra, getiri görülmeden eklendi): ana tanım 2018 ve 2020'yi çöküş saymadı (2018 yıl en düşük medyan r120 -%28,5; 2020 -%1,7). Bu günler yılın en düşük medyan r120 günüdür, yani GERİYE BAKARAK seçildi (dip o gün bilinmezdi); aynı +5 gün girişiyle aynı tablo, etiket yalnız bilgi.

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018B | OYNAK | 54 | %20,4 | %7,4 | %8,9 | %34,9 | %-11,8 | 1,57 | %7,4 [%-4,7, %19,7] | 1,80 | %3,3 [%-3,5, %11,3] | 0,13 |
| 2018B | TABAN | 170 | %12,9 | %4,1 | %13,1 | %22,9 | %-12,3 | 1 | | 1 | | |
| 2020B | OYNAK | 60 | %86,7 | %0,0 | %173,2 | %259,7 | %0,0 | 0,91 | %-8,8 [%-19,4, %0,1] | - | %0,0 [%0,0, %0,0] | 1,00 |
| 2020B | TABAN | 177 | %95,5 | %0,0 | %218,8 | %310,4 | %0,0 | 1 | | 1 | | |
| BIRLESIK | OYNAK | 114 | %55,3 | %3,5 | %45,2 | %153,2 | %-1,9 | 1,00 | %0,2 [%-6,8, %7,5] | 1,74 | %1,5 [%-2,0, %5,3] | 0,67 |
| BIRLESIK | TABAN | 347 | %55,0 | %2,0 | %72,4 | %169,6 | %-2,6 | 1 | | 1 | | |
| 2018B | DUSMUS | 54 | %18,5 | %5,6 | %16,2 | %51,6 | %-11,6 | 1,97 | %9,1 [%-2,5, %20,6] | 1,35 | %1,4 [%-5,1, %8,8] | 0,07 |
| 2018B | TABAN_D | 170 | %9,4 | %4,1 | %7,4 | %13,2 | %-13,8 | 1 | | 1 | | |
| 2020B | DUSMUS | 59 | %93,2 | %0,0 | %227,1 | %293,5 | %0,0 | 1,05 | %4,5 [%-2,8, %11,9] | - | %0,0 [%0,0, %0,0] | 0,22 |
| 2020B | TABAN_D | 177 | %88,7 | %0,0 | %200,0 | %281,2 | %0,0 | 1 | | 1 | | |
| BIRLESIK | DUSMUS | 113 | %57,5 | %2,7 | %84,1 | %177,9 | %-1,4 | 1,15 | %7,7 [%0,9, %14,1] | 1,32 | %0,6 [%-2,3, %4,2] | 0,04 |
| BIRLESIK | TABAN_D | 347 | %49,9 | %2,0 | %49,3 | %149,9 | %-2,6 | 1 | | 1 | | |
| 2018B | CAPRAZ | 29 | %24,1 | %10,3 | %13,1 | %57,6 | %-11,8 | 1,87 | %11,2 [%-4,3, %26,8] | 2,51 | %6,2 [%-3,6, %18,3] | 0,10 |
| 2020B | CAPRAZ | 27 | %92,6 | %0,0 | %209,4 | %254,2 | %0,0 | 0,97 | %-2,9 [%-13,8, %5,6] | - | %0,0 [%0,0, %0,0] | 0,87 |
| BIRLESIK | CAPRAZ | 56 | %57,1 | %5,4 | %56,0 | %152,4 | %-1,9 | 1,04 | %2,1 [%-7,7, %11,9] | 2,66 | %3,3 [%-2,0, %9,6] | 0,22 |
| 2018B | PROFIL | 18 | %11,1 | %16,7 | %8,8 | %75,9 | %-17,4 | 0,86 | %-1,8 [%-14,7, %15,4] | 4,05 | %12,5 [%-4,1, %30,4] | 0,70 |
| 2020B | PROFIL | 6 | %83,3 | %0,0 | %141,7 | %351,3 | %-0,6 | 0,87 | %-12,1 [%-46,0, %6,8] | - | %0,0 [%0,0, %0,0] | 0,97 |
| BIRLESIK | PROFIL | 24 | %29,2 | %12,5 | %15,7 | %144,7 | %-12,0 | 0,53 | %-25,9 [%-39,0, %-11,4] | 6,20 | %10,5 [%-1,7, %23,8] | 0,87 |

## DUYARLILIK (SAPMA, bilgi): ham veride > %25 tek gün sıçraması olan hisseler çıkarılınca

ham (süzülmemiş) ardışık iki işlem günü kapanışı arasında |değişim| > %25 = düzeltilmemiş sermaye işlemi şüphesi (BIST fiyat marjı ±%10, 12.03.2020 öncesi ±%20; kilitli taban / tavan serileri ardışık ham günlerde %10'u aşmaz, bu yüzden yakalanmaz). Bugünün listesi: şüpheli günden önceki fiyatlar oranla geriye düzeltilir (hacim ters oranla). Geçmiş tablo: şüpheli günü [giriş-260 bar, ufuk sonu] içinde olan hisseler çıkarılarak DUYARLILIK tablosu (bilgi; karar değişmez).

**cokus**

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | OYNAK | 69 | %73,9 | %2,9 | %74,8 | %168,4 | %-0,2 | 0,95 | %-4,0 [%-15,0, %7,9] | 6,29 | %2,4 [%-0,9, %6,8] | 0,82 |
| 2023 | TABAN | 217 | %77,9 | %0,5 | %110,5 | %149,7 | %0,0 | 1 | | 1 | | |
| 2023 | DUSMUS | 68 | %76,5 | %1,5 | %85,5 | %97,8 | %0,0 | 0,95 | %-4,3 [%-15,8, %6,7] | - | %1,5 [%0,0, %4,4] | 0,83 |
| 2023 | TABAN_D | 218 | %80,7 | %0,0 | %120,0 | %164,2 | %0,0 | 1 | | 1 | | |
| 2023 | CAPRAZ | 23 | %65,2 | %4,3 | %64,9 | %75,6 | %-0,2 | 0,84 | %-12,7 [%-31,9, %6,6] | 9,43 | %3,9 [%-1,4, %12,6] | 0,95 |
| 2023 | PROFIL | 16 | %56,2 | %6,2 | %35,9 | %59,5 | %-1,0 | 0,72 | %-21,6 [%-45,1, %6,1] | 13,56 | %5,8 [%-1,4, %18,8] | 0,98 |

**bilgi**

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018B | OYNAK | 54 | %20,4 | %7,4 | %8,9 | %34,9 | %-11,8 | 1,57 | %7,4 [%-4,7, %19,7] | 1,80 | %3,3 [%-3,5, %11,3] | 0,13 |
| 2018B | TABAN | 170 | %12,9 | %4,1 | %13,1 | %22,9 | %-12,3 | 1 | | 1 | | |
| 2020B | OYNAK | 60 | %86,7 | %0,0 | %173,2 | %259,7 | %0,0 | 0,91 | %-8,8 [%-19,4, %0,1] | - | %0,0 [%0,0, %0,0] | 1,00 |
| 2020B | TABAN | 177 | %95,5 | %0,0 | %218,8 | %310,4 | %0,0 | 1 | | 1 | | |
| BIRLESIK | OYNAK | 114 | %55,3 | %3,5 | %45,2 | %153,2 | %-1,9 | 1,00 | %0,2 [%-6,8, %7,5] | 1,74 | %1,5 [%-2,0, %5,3] | 0,67 |
| BIRLESIK | TABAN | 347 | %55,0 | %2,0 | %72,4 | %169,6 | %-2,6 | 1 | | 1 | | |
| 2018B | DUSMUS | 54 | %18,5 | %5,6 | %16,2 | %51,6 | %-11,6 | 1,97 | %9,1 [%-2,5, %20,6] | 1,35 | %1,4 [%-5,1, %8,8] | 0,07 |
| 2018B | TABAN_D | 170 | %9,4 | %4,1 | %7,4 | %13,2 | %-13,8 | 1 | | 1 | | |
| 2020B | DUSMUS | 59 | %93,2 | %0,0 | %227,1 | %293,5 | %0,0 | 1,05 | %4,5 [%-2,8, %11,9] | - | %0,0 [%0,0, %0,0] | 0,22 |
| 2020B | TABAN_D | 177 | %88,7 | %0,0 | %200,0 | %281,2 | %0,0 | 1 | | 1 | | |
| BIRLESIK | DUSMUS | 113 | %57,5 | %2,7 | %84,1 | %177,9 | %-1,4 | 1,15 | %7,7 [%0,9, %14,1] | 1,32 | %0,6 [%-2,3, %4,2] | 0,04 |
| BIRLESIK | TABAN_D | 347 | %49,9 | %2,0 | %49,3 | %149,9 | %-2,6 | 1 | | 1 | | |
| 2018B | CAPRAZ | 29 | %24,1 | %10,3 | %13,1 | %57,6 | %-11,8 | 1,87 | %11,2 [%-4,3, %26,8] | 2,51 | %6,2 [%-3,6, %18,3] | 0,10 |
| 2020B | CAPRAZ | 27 | %92,6 | %0,0 | %209,4 | %254,2 | %0,0 | 0,97 | %-2,9 [%-13,8, %5,6] | - | %0,0 [%0,0, %0,0] | 0,87 |
| BIRLESIK | CAPRAZ | 56 | %57,1 | %5,4 | %56,0 | %152,4 | %-1,9 | 1,04 | %2,1 [%-7,7, %11,9] | 2,66 | %3,3 [%-2,0, %9,6] | 0,22 |
| 2018B | PROFIL | 18 | %11,1 | %16,7 | %8,8 | %75,9 | %-17,4 | 0,86 | %-1,8 [%-14,7, %15,4] | 4,05 | %12,5 [%-4,1, %30,4] | 0,70 |
| 2020B | PROFIL | 6 | %83,3 | %0,0 | %141,7 | %351,3 | %-0,6 | 0,87 | %-12,1 [%-46,0, %6,8] | - | %0,0 [%0,0, %0,0] | 0,97 |
| BIRLESIK | PROFIL | 24 | %29,2 | %12,5 | %15,7 | %144,7 | %-12,0 | 0,53 | %-25,9 [%-39,0, %-11,4] | 6,20 | %10,5 [%-1,7, %23,8] | 0,87 |

**normal**

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N2017 | OYNAK | 52 | %38,5 | %1,9 | %25,2 | %69,3 | %-2,4 | 1,40 | %10,9 [%-3,2, %27,6] | - | %1,9 [%0,0, %5,8] | 0,09 |
| N2017 | TABAN | 156 | %27,6 | %0,0 | %27,7 | %48,0 | %-2,8 | 1 | | 1 | | |
| N2023 | OYNAK | 65 | %21,5 | %47,7 | %-7,4 | %17,0 | %-39,0 | 1,00 | %0,0 [%-11,1, %12,4] | 1,19 | %7,5 [%-7,7, %21,4] | 0,56 |
| N2023 | TABAN | 209 | %21,5 | %40,2 | %-4,4 | %26,0 | %-41,0 | 1 | | 1 | | |
| BIRLESIK | OYNAK | 117 | %29,1 | %27,4 | %9,3 | %40,2 | %-29,1 | 1,21 | %5,0 [%-3,9, %15,1] | 1,19 | %4,3 [%-3,9, %12,5] | 0,19 |
| BIRLESIK | TABAN | 365 | %24,1 | %23,0 | %14,5 | %35,4 | %-26,0 | 1 | | 1 | | |
| N2017 | DUSMUS | 52 | %28,8 | %0,0 | %24,4 | %55,6 | %-1,9 | 1,10 | %2,6 [%-10,9, %16,0] | 0,00 | %-0,6 [%-2,6, %0,0] | 0,42 |
| N2017 | TABAN_D | 156 | %26,3 | %0,6 | %29,4 | %43,5 | %-2,6 | 1 | | 1 | | |
| N2023 | DUSMUS | 64 | %23,4 | %37,5 | %-14,4 | %25,0 | %-40,7 | 0,92 | %-1,9 [%-13,0, %10,2] | 1,00 | %0,2 [%-13,6, %14,1] | 0,68 |
| N2023 | TABAN_D | 209 | %25,4 | %37,3 | %1,3 | %28,5 | %-38,5 | 1 | | 1 | | |
| BIRLESIK | DUSMUS | 116 | %25,9 | %20,7 | %5,3 | %38,7 | %-27,2 | 1,00 | %0,1 [%-8,2, %9,2] | 0,96 | %-1,0 [%-8,5, %6,7] | 0,54 |
| BIRLESIK | TABAN_D | 365 | %25,8 | %21,6 | %19,3 | %34,9 | %-25,1 | 1 | | 1 | | |
| N2017 | CAPRAZ | 17 | %29,4 | %0,0 | %15,6 | %66,0 | %-1,9 | 1,07 | %1,8 [%-19,6, %26,8] | - | %0,0 [%0,0, %0,0] | 0,53 |
| N2023 | CAPRAZ | 40 | %20,0 | %40,0 | %-10,7 | %14,4 | %-38,4 | 0,93 | %-1,5 [%-14,9, %11,8] | 1,00 | %-0,2 [%-15,9, %15,8] | 0,66 |
| BIRLESIK | CAPRAZ | 57 | %22,8 | %28,1 | %-1,6 | %29,8 | %-32,8 | 0,95 | %-1,3 [%-12,8, %10,2] | 1,22 | %5,1 [%-5,6, %16,1] | 0,61 |
| N2017 | PROFIL | 0 | - | - | - | - | - | - | - | - | - | - |
| N2023 | PROFIL | 2 | %0,0 | %100,0 | %-17,1 | %-17,1 | %-41,9 | 0,00 | %-21,5 [%-27,3, %-16,7] | 2,49 | %59,8 [%53,1, %66,5] | 1,00 |
| BIRLESIK | PROFIL | 2 | %0,0 | %100,0 | %-17,1 | %-17,1 | %-41,9 | 0,00 | %-24,1 [%-28,8, %-19,7] | 4,35 | %77,0 [%73,4, %80,8] | 1,00 |


## NORMAL DÖNEM KIYASI (yılın ilk işlem günü girişi; aynı tablo)

| Olay | Dilim | n | P(+%100) | P(-%50) | Medyan r250 | Ort. r250 | Medyan MDD60 | Kat +100 | Fark +100 [%95] | Kat -50 | Fark -50 [%95] | Perm. p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N2017 | OYNAK | 52 | %38,5 | %1,9 | %25,2 | %69,3 | %-2,4 | 1,40 | %10,9 [%-3,2, %27,6] | - | %1,9 [%0,0, %5,8] | 0,09 |
| N2017 | TABAN | 156 | %27,6 | %0,0 | %27,7 | %48,0 | %-2,8 | 1 | | 1 | | |
| N2023 | OYNAK | 65 | %21,5 | %47,7 | %-7,4 | %17,0 | %-39,0 | 1,00 | %0,0 [%-11,1, %12,4] | 1,19 | %7,5 [%-7,7, %21,4] | 0,56 |
| N2023 | TABAN | 209 | %21,5 | %40,2 | %-4,4 | %26,0 | %-41,0 | 1 | | 1 | | |
| BIRLESIK | OYNAK | 117 | %29,1 | %27,4 | %9,3 | %40,2 | %-29,1 | 1,21 | %5,0 [%-3,9, %15,1] | 1,19 | %4,3 [%-3,9, %12,5] | 0,19 |
| BIRLESIK | TABAN | 365 | %24,1 | %23,0 | %14,5 | %35,4 | %-26,0 | 1 | | 1 | | |
| N2017 | DUSMUS | 52 | %28,8 | %0,0 | %24,4 | %55,6 | %-1,9 | 1,10 | %2,6 [%-10,9, %16,0] | 0,00 | %-0,6 [%-2,6, %0,0] | 0,42 |
| N2017 | TABAN_D | 156 | %26,3 | %0,6 | %29,4 | %43,5 | %-2,6 | 1 | | 1 | | |
| N2023 | DUSMUS | 64 | %23,4 | %37,5 | %-14,4 | %25,0 | %-40,7 | 0,92 | %-1,9 [%-13,0, %10,2] | 1,00 | %0,2 [%-13,6, %14,1] | 0,68 |
| N2023 | TABAN_D | 209 | %25,4 | %37,3 | %1,3 | %28,5 | %-38,5 | 1 | | 1 | | |
| BIRLESIK | DUSMUS | 116 | %25,9 | %20,7 | %5,3 | %38,7 | %-27,2 | 1,00 | %0,1 [%-8,2, %9,2] | 0,96 | %-1,0 [%-8,5, %6,7] | 0,54 |
| BIRLESIK | TABAN_D | 365 | %25,8 | %21,6 | %19,3 | %34,9 | %-25,1 | 1 | | 1 | | |
| N2017 | CAPRAZ | 17 | %29,4 | %0,0 | %15,6 | %66,0 | %-1,9 | 1,07 | %1,8 [%-19,6, %26,8] | - | %0,0 [%0,0, %0,0] | 0,53 |
| N2023 | CAPRAZ | 40 | %20,0 | %40,0 | %-10,7 | %14,4 | %-38,4 | 0,93 | %-1,5 [%-14,9, %11,8] | 1,00 | %-0,2 [%-15,9, %15,8] | 0,66 |
| BIRLESIK | CAPRAZ | 57 | %22,8 | %28,1 | %-1,6 | %29,8 | %-32,8 | 0,95 | %-1,3 [%-12,8, %10,2] | 1,22 | %5,1 [%-5,6, %16,1] | 0,61 |
| N2017 | PROFIL | 0 | - | - | - | - | - | - | - | - | - | - |
| N2023 | PROFIL | 2 | %0,0 | %100,0 | %-17,1 | %-17,1 | %-41,9 | 0,00 | %-21,5 [%-27,3, %-16,7] | 2,49 | %59,8 [%53,1, %66,5] | 1,00 |
| BIRLESIK | PROFIL | 2 | %0,0 | %100,0 | %-17,1 | %-17,1 | %-41,9 | 0,00 | %-24,1 [%-28,8, %-19,7] | 4,35 | %77,0 [%73,4, %80,8] | 1,00 |

Not: 2017 ve 2023 BIST'te güçlü yükseliş yıllarıdır (2023 yüksek TL enflasyonu); 'normal' dönem nötr değildir, kıyas kat ve fark üzerinden okunmalıdır.

## BUGÜNÜN LİSTESİ (aday listesi, ölçüm değil; hiçbir isim için alım dili yok)

Geçmişte bu profil (OYNAK ve zirveden >= %60 düşmüş; çöküş + 5 gün, birleşik): P(+%100) = %56,2, P(-%50) = %6,2, medyan r250 %35,9, n = 16 (n < 30: örneklem yetersiz).
- 2023: n 16, P(+%100) %56,2, P(-%50) %6,2.

Karar günü 2026-11-13: evren 581 hisse, likidite süzgecinden sonra 465; σ250 üst beşlik 93; bunlardan zirveden >= %60 düşmüş 77; fon lekesiyle çıkan 27, Uzak listesiyle çıkan 5; profil 45. Ölçüler düzeltilmemiş sermaye işlemine karşı geriye düzeltilmiş fiyatla (SAPMA K6): evrende 62 hisse, profilde 2 hisse düzeltildi. σ250 kilitli taban / tavan günlerini (H = L) atlayan geçerli bar getirileriyle hesaplanır: fon krizinde taban serisi yaşayan hissenin σ'sı bu yüzden çok yüksektir.

| # | Sembol | σ250 (günlük) | Zirveden düşüş | r60 | Likidite 60g (mn TL) | Fon | S6 durumu | Son 20 günde en büyük gün | Ham düzeltme |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HEDEF | %12,17 | %-98,1 | %-96,2 | 763.6 | temiz (2026-09) | yok (DIP) | %-27,0 (2026-10-26) | 0 |
| 2 | UFUK | %11,98 | %-92,6 | %-90,6 | 138.0 | temiz (2026-09) | yok (DIP) | %-72,0 (2026-10-07) | 0 |
| 3 | PRZMA | %11,97 | %-90,3 | %-87,3 | 257.8 | temiz (2026-09) | yok (DIP) | %-10,0 (2026-10-21) | 0 |
| 4 | LYDYE | %11,37 | %-91,6 | %-87,3 | 38.1 | temiz (2026-09) | yok (DIP) | %-74,3 (2026-11-04) | 0 |
| 5 | TMPOL | %10,59 | %-89,0 | %-82,1 | 473.0 | temiz (2026-09) | yok (DIP) | %-27,0 (2026-10-26) | 0 |
| 6 | MAGEN | %8,90 | %-89,8 | %-80,7 | 465.8 | temiz (2026-09) | yok (DIP) | %-10,0 (2026-10-27) | 0 |
| 7 | CRDFA | %8,74 | %-81,5 | %-80,3 | 59.9 | temiz (2026-09) | yok (DIP) | %-61,5 (2026-10-01) | 0 |
| 8 | EDATA | %8,18 | %-85,1 | %-80,4 | 79.6 | temiz (2026-09) | yok (DIP) | %-10,0 (2026-10-20) | 0 |
| 9 | GZNMI | %8,14 | %-93,2 | %-67,3 | 52.3 | temiz (2026-09) | yok (DIP) | %10,0 (2026-11-04) | 0 |
| 10 | KLRHO | %7,95 | %-96,8 | %-71,1 | 345.3 | temiz (2026-08) | yok (DIP) | %9,9 (2026-10-16) | 0 |
| 11 | LIDER | %7,77 | %-94,6 | %-85,9 | 531.1 | temiz (2026-09) | yok (DIP) | %-17,3 (2026-11-03) | 0 |
| 12 | DOGUB | %7,21 | %-69,4 | %-47,1 | 21.3 | temiz (2026-09) | yok (DIP) | %10,0 (2026-10-23) | 0 |
| 13 | BIGTK | %6,67 | %-87,2 | %-84,6 | 187.6 | temiz (2026-09) | yok (DIP) | %-10,0 (2026-10-30) | 0 |
| 14 | EFOR | %6,45 | %-67,1 | %-47,1 | 1004.8 | temiz (2026-09) | yok (DIP) | %-10,0 (2026-11-12) | 0 |
| 15 | KUYAS | %6,34 | %-88,1 | %-83,9 | 637.5 | temiz (2026-08) | yok (DIP) | %-10,0 (2026-10-21) | 0 |

## HAYATTA KALMA UYARISI

Evren V_BIST'teki bugün işlem gören 581 hissedir. 2018 ve 2020 çöküşlerinden sonra kottan çıkan / batan hisseler veride yoktur. Bu yüzden ölçülen P(-%50) gerçek değerden DÜŞÜK, P(+%100) ve medyan r250 YÜKSEK olabilir; en çok etkilenen dilim en oynak ve en çok düşmüş hisselerdir (batanlar çoğunlukla orada). Hb'nin (risk büyük değil) tutması bu yanlılıkla kısmen açıklanabilir. 3 yılda 10x taban oranı (BIST USD ~%1,85) değişmez.

## KONTROL LİSTESİ

| Kod | Yanıt | Kanıt |
|---|---|---|
| K1 | EVET | taban = aynı giriş günü, aynı evren (likidite süzgeci sonrası) σ250 orta üç beşlik; aynı giriş açılışı ve 250 gün geometrisi; mekanik üstünlük: yüksek σ iki kuyruğu birden büyütür, bu yüzden normal dönem (2017, 2023) aynı tabloyla kıyaslanır; olasılık ölçüsünde portföy yerine olay içi permütasyon (1000) |
| K2 | EVET | ölçüler yalnız karar günü (giriş-1) ve öncesi barlardan (co_hisse_olay içinde x.index.max() <= karar mekanik denetim, COHata); çöküş günü yalnız geçmiş 120 gün; fon tablosu bilinme <= karar denetimi (co_fon_leke); evren bugünün listesi (K7) |
| K3 | EVET | geçerli bar H>L, V>0, O,C>0 (co_gecerli); karar gününden 5 işlem gününden eski son bar -> hisse dışarıda; bugünün listesi 13 Kas tam bar (16 Kas yarım bar atılır) |
| K4 | EVET | çöküşler arası en az 250 işlem günü; her hisse olay başına bir kez; n = hisse sayısı; ortalama yanında medyan r250 |
| K5 | EVET | giriş = çöküş + 5. işlem günü AÇILIŞI (karar günü kapanışı değil); bar yoksa 5 gün içindeki ilk geçerli açılış |
| K6 | EVET | V_BIST tek kip düzeltilmiş fiyat; bölünme şüphesi SY.sy_bolunme_supheli ANA ile [giriş-260 bar, ufuk sonu] içinde olan hisse çıkar ve sayısı yazılır; likidite TL (dilim içi sıralama, birim farkı etkilemez) |
| K7 | EVET | evren bugün işlem görenler (V_BIST 581); 2018 / 2020 batanları yok -> P(-%50) aşağı, P(+%100) yukarı yanlı; RAPOR'da HAYATTA KALMA UYARISI bölümü |
| K8 | EVET | hücre n < 30 -> ÖLÇÜLEMEDİ; iki çöküş ayrı hücre + birleşik, Ha her olayda aynı yön şartı; üç (a) testi BH (bilgi); iki olay = en fazla EMARE |
| K9 | EVET | iş tanımı commit 69fbed0 koşudan önce; CO_ESIK sha256 mühürü + kod sha + veri sha ON_KAYIT.md'de, kos mühür farklıysa durur; git commit alt ajana yasak -> ON_KAYIT commit'i ana modelde (zaman damgası dosyada) |
| K10 | UYGULANMAZ | metin / haber ayrıştırması yok; yalnız fiyat-hacim; fon tablosu FON_IZI.FI_TASFIYE_RE ile mevcut ayrıştırılmış G.pkl'den |
| K11 | EVET | olay satırları csv.gz'ye yazılır; test_cokus_oynak.py en az iki hücreyi (2018 ve 2020 OYNAK P100 / M50) satır dosyasından bağımsız yeniden üretir |
| K12 | EVET | fiyat değişimi (kapanış / giriş) ile gerçekleşen kâr ayrı; 'emare / piyango' yalnız önceden yazılı kuralla; sayı ve yorum ayrı cümle; hiçbir isme alım dili yok |
| K13 | EVET | çakışma kapısı (_cakisma_kontrol_co); defter dosyaları ve mevcut .py değişmez; e-posta / anahtar taraması testte; commit / push yok; kod değişirse çalışma zamanını yeniden başlat |
| K14 | UYGULANMAZ | öneri işi değil, aday listesi; boyut / çıkış kuralı yok, alım dili yok; taban oran (3 yılda 10x ~%1-1,85) RAPOR'da yazılı |

## SAPMA

- kod sha ön kayıttan farklı (eşik mühürü aynı; değişiklik yalnız kod / gösterim olmalı, RAPOR SAPMA bölümüne bakın)
- İLK KOŞU HATASI: 2026 çöküşünde kesik veride hisse kalmayınca co_dilimle boş tabloda düştü; giriş kriz kesiğinden sonraysa olay 'sonuç yok' yazılıp atlanır (kod düzeltmesi, eşik değişmedi).
- K6 (ilk koşudan sonra): bugünün listesindeki ilk 15 hissenin hepsinde ham veride > %25 tek gün sıçrama vardı; bir kısmı kilitli taban serisi (gerçek), bir kısmı Yahoo'da düzeltilmemiş bedelsiz (ör. ardışık iki ham günde -%86). ham (süzülmemiş) ardışık iki işlem günü kapanışı arasında |değişim| > %25 = düzeltilmemiş sermaye işlemi şüphesi (BIST fiyat marjı ±%10, 12.03.2020 öncesi ±%20; kilitli taban / tavan serileri ardışık ham günlerde %10'u aşmaz, bu yüzden yakalanmaz). Bugünün listesi: şüpheli günden önceki fiyatlar oranla geriye düzeltilir (hacim ters oranla). Geçmiş tablo: şüpheli günü [giriş-260 bar, ufuk sonu] içinde olan hisseler çıkarılarak DUYARLILIK tablosu (bilgi; karar değişmez).

## HATA

- Beklenti tutmadı (yanlış yorum riski): iş tanımı 2018 ve 2020'yi çöküş bekliyordu; sabit tanımla (medyan r120 <= -%30) 2018'in en düşüğü -%28,5, 2020'nin -%1,7 (Mart 2020 öncesi 120 günde küçük hisseler yükselmişti). Çöküşler 2023-05-22 ve 2026-10-13; ölçülebilir tek olay 2023 -> birincil karar ÖLÇÜLEMEDİ. Tanım değiştirilmedi.
- Kod (süreç): ilk koşu 2026 olayında boş tabloda düştü (AttributeError); giriş kriz kesiğinden sonraysa olay atlanır. Sonuç görülmeden önceki hata; eşik değişmedi.
- Veri (K6): canlı Yahoo verisinde düzeltilmemiş bedelsiz var (ör. MERKO 30.04 -> 04.05.2026 ardışık iki günde -%86, hacim 15 kat); ilk liste MERKO'yu σ250 ile 1. sıraya koymuştu. Ham ardışık gün |değişim| > %25 geriye düzeltildi (evrende 62 hisse). Geçmiş V_BIST'te pencerelerde bu tür sıçrama 0 (duyarlılık tablosu ana tabloyla aynı).
- Ölçü yorumu: σ250 geçerli bar (H > L) getirisiyle hesaplanır; kilitli taban serisi (H = L günleri atılır) tek bir büyük getiri gibi görünür (UFUK 07.10 -%72, LYDYE 04.11 -%74). Bugünün listesinin üstü bu yüzden fon krizi taban serisi yaşayan hisselerdir; 'oynak' burada 'kilitli çöküş' demektir.
- Kapsam: fon lekesi yalnız fon portföyünde tasfiye fonu pozisyonuna bakar; HEDEF (Hedef Holding) tasfiyedeki portföy şirketiyle aynı adı taşır ama leke 'temiz' çıkar. Listedeki isimler DOSYA kapısından geçmedi.
- Kıyas: 'normal dönem' N2023 girişi (2023-01-02) balon sonrasıdır (medyan r120 +%120) ve 250 gün penceresi 2023 çöküşünü içerir; 2017 ve 2023 nötr dönem değildir.
- Süreç (K9): ON_KAYIT.md commit'i alt ajana yasak; ön kayıt zamanı dosyada (UTC), CO_ESIK mühürü kos'ta denetlenir; commit ana modelde.
- Geriye bakma (bilgi hücreleri): 2018B / 2020B günleri yılın en düşük medyan günü olarak seçildi (dip o gün bilinmezdi); getiri görülmeden eklendi, karar dışı.

## ÖNERİLEN DEFTER METNİ (ana model işler)

- IK_KAYIT Ç satırı: 'ÇÖKÜŞ SONRASI OYNAK (Cemal hipotezi, 16 Kas): BIST çöküş günleri 2023-05-22, 2026-10-13; OYNAK (σ250 üst beşlik) vs orta üç beşlik, 250 gün: P(+%100) %73,9 / %77,9, P(-%50) %2,9 / %0,5; karar ÖLÇÜLEMEDİ (iki olay; İZ değil); hayatta kalma yanlılığı yukarı.'
- IK_ILERI satırı: '2026 çöküşü (V_BIST kesiksiz tespit) sonucu: Mart 2027 (r120) ve Kasım 2027 (r250) aynı komut (`python COKUS_OYNAK.py kos`, aynı CO_ESIK, kriz kesiği kaldırılmış ayrı ön kayıtla), aynı eşik.'
