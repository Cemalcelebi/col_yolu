# HAKEM TURU 4 — SONUÇ

Mühür sırası: TUTTU · 2026-11-19 09:50:28 UTC

BAŞARI tanımı (önceden yazılı): CLAUDE.md 'Hakem turları' (önceden yazılı, değişmez): sonuç = olay_Y1 h5 (15 geçerli barda +%5 kapanışla, stop'tan önce; 1 / 0; NaN ölçülemedi). OLUR isabeti = OLUR'larda h5 = 1 payı; OLMAZ isabeti = OLMAZ'larda h5 = 0 payı; BAŞARI = (doğru OLUR + doğru OLMAZ) / (OLUR + OLMAZ) (BELİRSİZ karar değil, ayrı sayılır; h5 NaN sayfa ölçülemedi, ayrı sayılır). Taban = aynı sayfaların eş payı (ortalama es_h5). Fisher iki yönlü (karar OLUR / OLMAZ x h5). Uyum = Cohen kappa (3 sınıf, iki tarafın da geçerli yanıtı olan sayfalar). Birikimli = tur 1..K satır dosyaları birleşik.

**Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).**

## İsabet tablosu

| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (bu tur) | 2 / 38 / 0 | 2 / 2 (%100,0) | 20 / 38 (%52,6) | **%55,0** (22 / 40) | %52,1 | %53,1 | %50,0 | 0,487 | 0 / 0 |
| Cemal (bu tur) | 19 / 11 / 10 | 10 / 19 (%52,6) | 7 / 11 (%63,6) | **%56,7** (17 / 30) | %47,8 | %53,1 | %50,0 | 0,466 | 0 / 0 |
| model (birikimli, tur [1, 2, 4]) | 30 / 69 / 1 | 15 / 30 (%50,0) | 37 / 69 (%53,6) | **%52,5** (52 / 99) | %44,2 | %46,1 | %53,0 | 0,828 | 0 / 0 |
| Cemal (birikimli, tur [1, 2, 4]) | 47 / 24 / 29 | 21 / 47 (%44,7) | 12 / 24 (%50,0) | **%46,5** (33 / 71) | %43,7 | %46,1 | %53,0 | 0,802 | 0 / 0 |

- Uyum (kappa, 3 sınıf): bu tur -0,014 (n 40); birikimli 0,059 (n 100).
- Yanılınan sayfalar: model [1, 2, 3, 9, 10, 14, 16, 17, 19, 20, 26, 28, 31, 33, 35, 36, 39, 40]; Cemal [4, 5, 6, 8, 10, 11, 15, 17, 27, 29, 34, 37, 39].
- Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).

Üç cetvel (bilgi; BAŞARI yalnız ilk cetvelle, değişmez):

| Taraf | Cetvel | OLUR isabeti | OLMAZ isabeti | BAŞARI | taban (sayfa payı) | hep OLMAZ deseydi | ölçülemedi |
|---|---|---|---|---|---|---|---|
| model (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 2 / 2 (%100,0) | 20 / 38 (%52,6) | **%55,0** (22 / 40) | %50,0 | %50,0 | 0 |
| model (bu tur) | 15 g gün içi +%5 (High; bilgi) | 2 / 2 (%100,0) | 15 / 38 (%39,5) | **%42,5** (17 / 40) | %62,5 | %37,5 | 0 |
| model (bu tur) | 60 g kapanış +%5 (bilgi) | 2 / 2 (%100,0) | 11 / 38 (%28,9) | **%32,5** (13 / 40) | %72,5 | %27,5 | 0 |
| Cemal (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 10 / 19 (%52,6) | 7 / 11 (%63,6) | **%56,7** (17 / 30) | %50,0 | %50,0 | 0 |
| Cemal (bu tur) | 15 g gün içi +%5 (High; bilgi) | 12 / 19 (%63,2) | 6 / 11 (%54,5) | **%60,0** (18 / 30) | %62,5 | %37,5 | 0 |
| Cemal (bu tur) | 60 g kapanış +%5 (bilgi) | 13 / 19 (%68,4) | 4 / 11 (%36,4) | **%56,7** (17 / 30) | %72,5 | %27,5 | 0 |
| model (birikimli, tur [1, 2, 4]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 15 / 30 (%50,0) | 37 / 69 (%53,6) | **%52,5** (52 / 99) | %47,0 | %53,0 | 0 |
| model (birikimli, tur [1, 2, 4]) | 15 g gün içi +%5 (High; bilgi) | 16 / 30 (%53,3) | 25 / 69 (%36,2) | **%41,4** (41 / 99) | %60,0 | %40,0 | 0 |
| model (birikimli, tur [1, 2, 4]) | 60 g kapanış +%5 (bilgi) | 25 / 30 (%83,3) | 19 / 67 (%28,4) | **%45,4** (44 / 97) | %74,5 | %25,5 | 2 |
| Cemal (birikimli, tur [1, 2, 4]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 21 / 47 (%44,7) | 12 / 24 (%50,0) | **%46,5** (33 / 71) | %47,0 | %53,0 | 0 |
| Cemal (birikimli, tur [1, 2, 4]) | 15 g gün içi +%5 (High; bilgi) | 28 / 47 (%59,6) | 9 / 24 (%37,5) | **%52,1** (37 / 71) | %60,0 | %40,0 | 0 |
| Cemal (birikimli, tur [1, 2, 4]) | 60 g kapanış +%5 (bilgi) | 34 / 46 (%73,9) | 5 / 24 (%20,8) | **%55,7** (39 / 70) | %74,5 | %25,5 | 2 |
- Yön doğru / eşik kaçtı (OLUR, h5 = 0, 15 g kapanış max +%3..+%5): model yok; Cemal [11]; birikimli model 4, Cemal 6.
- Cemal'in birikimli etiketi 100'ü geçti: göz ölçümü (Ç192 planı) Cemal'in kendi etiketleriyle koşulur.

## Dönem kırılımı (bilgi; T1.6)

| Taraf (dönem) | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (2016-22) | 0 / 18 / 0 | 0 / 0 (-) | 11 / 18 (%61,1) | **%61,1** (11 / 18) | - | %57,0 | %61,1 | - | 0 / 0 |
| cemal (2016-22) | 7 / 7 / 4 | 3 / 7 (%42,9) | 6 / 7 (%85,7) | **%64,3** (9 / 14) | %61,1 | %57,0 | %61,1 | 0,559 | 0 / 0 |
| model (2023) | 0 / 4 / 0 | 0 / 0 (-) | 2 / 4 (%50,0) | **%50,0** (2 / 4) | - | %27,2 | %50,0 | - | 0 / 0 |
| cemal (2023) | 3 / 0 / 1 | 2 / 3 (%66,7) | 0 / 0 (-) | **%66,7** (2 / 3) | %27,8 | %27,2 | %50,0 | - | 0 / 0 |
| model (2024-26) | 2 / 16 / 0 | 2 / 2 (%100,0) | 7 / 16 (%43,8) | **%50,0** (9 / 18) | %52,1 | %54,9 | %38,9 | 0,497 | 0 / 0 |
| cemal (2024-26) | 9 / 4 / 5 | 5 / 9 (%55,6) | 1 / 4 (%25,0) | **%46,2** (6 / 13) | %44,2 | %54,9 | %38,9 | 1,000 | 0 / 0 |

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | 15 g kapanış max (bilgi) | gün içi +%5 (15 g High; bilgi) | 60 g max / min / son kapanış (bilgi) | eşik kaçtı (+%3..+%5) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | 2023 | 0 | OLMAZ | OLUR | 1 | %25,0 | 1 | 0 | %15,3 | %49,5 | 1 (%52,5) | %63,9 / -%5,4 / -%5,4 |  | X |  |
| 2 | BIST | 2016-22 | 0 | OLMAZ | OLUR | 1 | %65,7 | 1 | 0 | %5,3 | %16,5 | 1 (%20,2) | %48,1 / -%3,3 / %48,1 |  | X |  |
| 3 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 1 | %65,2 | 1 | 0 | %6,7 | %14,4 | 1 (%17,4) | %14,4 / -%0,5 / %4,4 |  | X |  |
| 4 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %42,5 | 0 | 0 | -%4,3 | -%0,5 | 0 (%2,2) | %3,6 / -%20,5 / -%8,3 |  |  | X |
| 5 | BIST | 2024-26 | 0 | OLMAZ | OLUR | 0 | %7,7 | 0 | 1 | -%6,9 | %7,4 | 1 (%14,9) | %86,3 / -%18,5 / %76,6 |  |  | X |
| 6 | ABD | 2016-22 | 0 | OLMAZ | OLUR | 0 | %37,8 | 0 | 1 | -%6,9 | -%0,2 | 0 (%2,8) | %2,6 / -%11,1 / -%10,1 |  |  | X |
| 7 | ABD | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %3,8 | 0 | 1 | -%12,5 | %5,2 | 1 (%7,3) | %21,1 / -%12,2 / %3,7 |  |  |  |
| 8 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %38,6 | 0 | 1 | -%5,4 | %2,6 | 0 (%4,2) | %2,6 / -%30,9 / -%17,8 |  |  | X |
| 9 | ABD | 2016-22 | 0 | OLMAZ | OLUR | 1 | %81,3 | 1 | 0 | %10,7 | %19,6 | 1 (%20,1) | %23,2 / -%1,4 / %23,2 |  | X |  |
| 10 | ABD | 2016-22 | 0 | OLMAZ | OLMAZ | 1 | %75,9 | 1 | 0 | %13,0 | %22,2 | 1 (%26,9) | %22,2 / -%13,3 / -%13,1 |  | X | X |
| 11 | BIST | 2024-26 | 0 | OLMAZ | OLUR | 0 | %21,9 | 0 | 0 | -%2,6 | %4,2 | 1 (%7,8) | %4,2 / -%20,0 / -%7,1 | K |  | X |
| 12 | BIST | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %47,4 | 0 | 0 | -%11,1 | -%2,8 | 0 (%0,9) | -%2,8 / -%14,8 / -%10,2 |  |  |  |
| 13 | ABD | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %53,3 | 0 | 0 | %0,1 | %0,8 | 0 (%1,8) | %9,6 / -%5,7 / -%1,2 |  |  |  |
| 14 | ABD | 2016-22 | 0 | OLMAZ | OLUR | 1 | %59,7 | 1 | 0 | %38,0 | %26,1 | 1 (%29,2) | %55,9 / -%24,5 / -%24,5 |  | X |  |
| 15 | BIST | 2016-22 | 0 | OLMAZ | OLUR | 0 | %92,9 | 0 | 0 | -%4,8 | %2,2 | 0 (%2,2) | %2,2 / -%5,4 / -%0,5 |  |  | X |
| 16 | AVR | 2024-26 | 0 | OLMAZ | OLUR | 1 | %36,1 | 1 | 0 | %11,5 | %17,1 | 1 (%18,3) | %17,1 / -%10,8 / -%9,7 |  | X |  |
| 17 | BIST | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %96,9 | 1 | 0 | %20,4 | %17,9 | 1 (%21,7) | %30,9 / -%1,8 / %8,9 |  | X | X |
| 18 | ABD | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %24,4 | 0 | 1 | -%10,9 | %1,3 | 0 (%2,6) | %1,3 / -%30,2 / -%16,9 |  |  |  |
| 19 | ABD | 2016-22 | 0 | OLMAZ | BELİRSİZ | 1 | %83,6 | 0 | 0 | %1,8 | %6,7 | 1 (%7,3) | %6,7 / -%16,4 / -%9,4 |  | X |  |
| 20 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 1 | %63,1 | 1 | 0 | %4,4 | %11,7 | 1 (%13,3) | %11,7 / -%22,6 / -%12,2 |  | X |  |
| 21 | BIST | 2024-26 | 0 | OLUR | OLUR | 1 | %50,0 | 1 | 0 | %11,7 | %25,4 | 1 (%27,9) | %101,7 / %2,5 / %53,0 |  |  |  |
| 22 | ABD | 2023 | 0 | OLMAZ | BELİRSİZ | 0 | %25,6 | 0 | 1 | -%11,5 | -%2,6 | 0 (%0,4) | -%2,6 / -%41,2 / -%30,7 |  |  |  |
| 23 | BIST | 2024-26 | 0 | OLMAZ | BELİRSİZ | 0 | %54,5 | 0 | 0 | %1,6 | %1,2 | 0 (%1,4) | %7,7 / -%8,4 / -%8,4 |  |  |  |
| 24 | BIST | 2024-26 | 0 | OLMAZ | OLMAZ | 0 | %60,7 | 0 | 0 | %6,1 | %0,3 | 0 (%1,5) | %28,2 / -%6,1 / %7,4 |  |  |  |
| 25 | BIST | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %31,8 | 0 | 0 | -%7,8 | -%5,6 | 0 (%0,3) | -%0,4 / -%16,8 / -%13,7 |  |  |  |
| 26 | BIST | 2024-26 | 0 | OLMAZ | OLUR | 1 | %72,7 | 0 | 0 | %2,2 | %8,7 | 1 (%16,6) | %8,7 / -%17,0 / %4,4 |  | X |  |
| 27 | AVR | 2023 | 0 | OLMAZ | OLUR | 0 | %25,0 | 0 | 1 | -%4,2 | %2,5 | 0 (%3,6) | %7,2 / -%7,0 / %2,5 |  |  | X |
| 28 | BIST | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %83,9 | 1 | 0 | %6,0 | %14,7 | 1 (%23,0) | %16,6 / -%5,0 / -%5,0 |  | X |  |
| 29 | BIST | 2016-22 | 1 | OLMAZ | OLUR | 0 | %46,2 | 0 | 0 | %30,7 | %2,6 | 0 (%4,1) | %40,7 / -%0,3 / %20,8 |  |  | X |
| 30 | BIST | 2016-22 | 0 | OLMAZ | OLMAZ | 0 | %44,4 | 0 | 0 | -%8,3 | -%3,6 | 0 (%0,3) | -%2,1 / -%13,6 / -%5,0 |  |  |  |
| 31 | BIST | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %84,0 | 0 | 0 | %6,2 | %7,9 | 1 (%11,4) | %18,9 / -%0,2 / %16,1 |  | X |  |
| 32 | BIST | 2024-26 | 0 | OLMAZ | BELİRSİZ | 0 | %74,4 | 0 | 0 | -%0,1 | %4,3 | 1 (%6,9) | %8,7 / -%11,5 / -%7,8 | K |  |  |
| 33 | ABD | 2016-22 | 0 | OLMAZ | BELİRSİZ | 1 | %54,7 | 1 | 0 | %7,4 | %11,1 | 1 (%13,1) | %11,1 / -%17,3 / %0,4 |  | X |  |
| 34 | BIST | 2016-22 | 0 | OLMAZ | OLUR | 0 | %44,4 | 0 | 0 | -%10,8 | -%1,1 | 0 (%0,2) | -%1,1 / -%23,9 / -%21,6 |  |  | X |
| 35 | BIST | 2016-22 | 0 | OLMAZ | BELİRSİZ | 1 | %94,6 | 1 | 0 | %6,5 | %21,3 | 1 (%23,2) | %50,1 / %5,6 / %29,7 |  | X |  |
| 36 | BIST | 2023 | 0 | OLMAZ | OLUR | 1 | %33,3 | 1 | 0 | %38,8 | %47,9 | 1 (%49,0) | %102,1 / -%6,0 / %100,1 |  | X |  |
| 37 | BIST | 2024-26 | 0 | OLUR | OLMAZ | 1 | %54,3 | 0 | 0 | %0,5 | %5,3 | 1 (%10,9) | %5,3 / -%18,8 / -%16,5 |  |  | X |
| 38 | AVR | 2016-22 | 0 | OLMAZ | BELİRSİZ | 0 | %83,3 | 0 | 1 | -%4,9 | %4,2 | 1 (%6,2) | %7,4 / -%4,7 / %1,5 | K |  |  |
| 39 | BIST | 2024-26 | 1 | OLMAZ | OLMAZ | 1 | %64,5 | 0 | 0 | %0,3 | %8,7 | 1 (%14,0) | %23,2 / -%5,7 / %9,6 |  | X | X |
| 40 | ABD | 2024-26 | 1 | OLMAZ | BELİRSİZ | 1 | %17,5 | 0 | 0 | %0,8 | %6,3 | 1 (%7,1) | %7,9 / -%20,2 / -%9,9 |  | X |  |

Bilgi sütunları (B1.0): Fiyat = ge_hazir (YAPI_HEDEF geçerli bar + kriz kesiği 31.08.2026). Bar 0 = giriş günü (olay 'giris'; geçerli bar olmalı, yoksa DURUR), E0 = giriş günü açılışı (olay dosyasında E0 varsa göreli 1e-4 ile aynı olmalı, yoksa DURUR). 15 g = bar 0..14 (15 geçerli bar; h5 ile aynı sayım, stop YOK); 60 g = bar 0..59 (60 geçerli bar; kriz kesiği ya da hissenin son barı yüzünden 60 bar yoksa 60 g sütunları NaN = ölçülemedi). k15 = max Close(0..14) / E0 - 1; gi15 = max High(0..14) / E0 - 1; m60 / n60 / s60 = max / min / son (bar 59) Close(0..59) / E0 - 1. yön doğru / eşik kaçtı: karar OLUR VE h5 = 0 VE +%3 <= k15 < +%5 (kapanışla +%3..+%5 arası kaldı). Bilgi; BAŞARI'yı değiştirmez. 'eşik kaçtı' sütunu (K) sayfanın kapanış bandını gösterir; taraf sayımı yalnız o tarafın OLUR dediği sayfalarda.

Not: küçük örneklem (40 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
