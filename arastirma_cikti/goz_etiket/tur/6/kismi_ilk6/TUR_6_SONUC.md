# HAKEM TURU 6 — SONUÇ

Mühür sırası: TUTTU · 2026-11-19 14:46:28 UTC

BAŞARI tanımı (önceden yazılı): CLAUDE.md 'Hakem turları' (önceden yazılı, değişmez): sonuç = olay_Y1 h5 (15 geçerli barda +%5 kapanışla, stop'tan önce; 1 / 0; NaN ölçülemedi). OLUR isabeti = OLUR'larda h5 = 1 payı; OLMAZ isabeti = OLMAZ'larda h5 = 0 payı; BAŞARI = (doğru OLUR + doğru OLMAZ) / (OLUR + OLMAZ) (BELİRSİZ karar değil, ayrı sayılır; h5 NaN sayfa ölçülemedi, ayrı sayılır). Taban = aynı sayfaların eş payı (ortalama es_h5). Fisher iki yönlü (karar OLUR / OLMAZ x h5). Uyum = Cohen kappa (3 sınıf, iki tarafın da geçerli yanıtı olan sayfalar). Birikimli = tur 1..K satır dosyaları birleşik.

**Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).**

## İsabet tablosu

| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (bu tur) | 18 / 22 / 0 | 9 / 18 (%50,0) | 12 / 22 (%54,5) | **%52,5** (21 / 40) | %51,9 | %48,0 | %52,5 | 1,000 | 0 / 0 |
| Cemal (bu tur) | 3 / 3 / 0 | 1 / 3 (%33,3) | 1 / 3 (%33,3) | **%33,3** (2 / 6) | %34,0 | %48,0 | %52,5 | 1,000 | 34 / 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 48 / 91 / 1 | 24 / 48 (%50,0) | 49 / 91 (%53,8) | **%52,5** (73 / 139) | %47,1 | %46,6 | %52,9 | 0,722 | 0 / 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 50 / 27 / 29 | 22 / 50 (%44,0) | 13 / 27 (%48,1) | **%45,5** (35 / 77) | %43,1 | %46,6 | %52,9 | 0,633 | 34 / 0 |

- Uyum (kappa, 3 sınıf): bu tur 1,000 (n 6); birikimli 0,095 (n 106).
- Yanılınan sayfalar: model [4, 5, 7, 9, 10, 15, 16, 17, 20, 22, 23, 25, 26, 27, 29, 30, 31, 37, 40]; Cemal [4, 5, 7, 9].
- Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).

Üç cetvel (bilgi; BAŞARI yalnız ilk cetvelle, değişmez):

| Taraf | Cetvel | OLUR isabeti | OLMAZ isabeti | BAŞARI | taban (sayfa payı) | hep OLMAZ deseydi | ölçülemedi |
|---|---|---|---|---|---|---|---|
| model (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 9 / 18 (%50,0) | 12 / 22 (%54,5) | **%52,5** (21 / 40) | %47,5 | %52,5 | 0 |
| model (bu tur) | 15 g gün içi +%5 (High; bilgi) | 11 / 18 (%61,1) | 8 / 22 (%36,4) | **%47,5** (19 / 40) | %62,5 | %37,5 | 0 |
| model (bu tur) | 60 g kapanış +%5 (bilgi) | 13 / 18 (%72,2) | 5 / 22 (%22,7) | **%45,0** (18 / 40) | %75,0 | %25,0 | 0 |
| Cemal (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 1 / 3 (%33,3) | 1 / 3 (%33,3) | **%33,3** (2 / 6) | %47,5 | %52,5 | 0 |
| Cemal (bu tur) | 15 g gün içi +%5 (High; bilgi) | 1 / 3 (%33,3) | 1 / 3 (%33,3) | **%33,3** (2 / 6) | %62,5 | %37,5 | 0 |
| Cemal (bu tur) | 60 g kapanış +%5 (bilgi) | 2 / 3 (%66,7) | 0 / 3 (%0,0) | **%33,3** (2 / 6) | %75,0 | %25,0 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 24 / 48 (%50,0) | 49 / 91 (%53,8) | **%52,5** (73 / 139) | %47,1 | %52,9 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 15 g gün içi +%5 (High; bilgi) | 27 / 48 (%56,2) | 33 / 91 (%36,3) | **%43,2** (60 / 139) | %60,7 | %39,3 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 60 g kapanış +%5 (bilgi) | 38 / 48 (%79,2) | 24 / 89 (%27,0) | **%45,3** (62 / 137) | %74,6 | %25,4 | 2 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 22 / 50 (%44,0) | 13 / 27 (%48,1) | **%45,5** (35 / 77) | %47,1 | %52,9 | 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 15 g gün içi +%5 (High; bilgi) | 29 / 50 (%58,0) | 10 / 27 (%37,0) | **%50,6** (39 / 77) | %60,7 | %39,3 | 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 60 g kapanış +%5 (bilgi) | 36 / 49 (%73,5) | 5 / 27 (%18,5) | **%53,9** (41 / 76) | %74,6 | %25,4 | 2 |
- Yön doğru / eşik kaçtı (OLUR, h5 = 0, 15 g kapanış max +%3..+%5): model [27]; Cemal yok; birikimli model 5, Cemal 6.
- Cemal'in birikimli etiketi 100'ü geçti: göz ölçümü (Ç192 planı) Cemal'in kendi etiketleriyle koşulur.

## Dönem kırılımı (bilgi; T1.6)

| Taraf (dönem) | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (2016-22) | 8 / 9 / 0 | 1 / 8 (%12,5) | 7 / 9 (%77,8) | **%47,1** (8 / 17) | %35,0 | %38,4 | %82,4 | 1,000 | 0 / 0 |
| cemal (2016-22) | 2 / 2 / 0 | 0 / 2 (%0,0) | 1 / 2 (%50,0) | **%25,0** (1 / 4) | %41,5 | %38,4 | %82,4 | 1,000 | 13 / 0 |
| model (2023) | 0 / 2 / 0 | 0 / 0 (-) | 1 / 2 (%50,0) | **%50,0** (1 / 2) | - | %59,3 | %50,0 | - | 0 / 0 |
| cemal (2023) | 0 / 0 / 0 | 0 / 0 (-) | 0 / 0 (-) | **-** (0 / 0) | - | %59,3 | %50,0 | - | 2 / 0 |
| model (2024-26) | 10 / 11 / 0 | 8 / 10 (%80,0) | 4 / 11 (%36,4) | **%57,1** (12 / 21) | %65,3 | %54,7 | %28,6 | 0,635 | 0 / 0 |
| cemal (2024-26) | 1 / 1 / 0 | 1 / 1 (%100,0) | 0 / 1 (%0,0) | **%50,0** (1 / 2) | %19,0 | %54,7 | %28,6 | 1,000 | 19 / 0 |

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | 15 g kapanış max (bilgi) | gün içi +%5 (15 g High; bilgi) | 60 g max / min / son kapanış (bilgi) | eşik kaçtı (+%3..+%5) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIST | 2024-26 | 0 | OLUR | - | 1 | %53,6 | 1 | 0 | %6,1 | %11,0 | 1 (%12,3) | %22,1 / -%12,3 / %22,1 |  |  |  |
| 2 | BIST | 2024-26 | 0 | OLUR | - | 1 | %90,5 | 1 | 0 | %25,8 | %10,5 | 1 (%10,6) | %32,7 / -%2,5 / %19,1 |  |  |  |
| 3 | BIST | 2016-22 | 0 | OLMAZ | - | 0 | %45,5 | 0 | 0 | %7,0 | %0,0 | 0 (%1,8) | %13,5 / -%11,1 / -%8,2 |  |  |  |
| 4 | ABD | 2016-22 | 0 | OLUR | OLUR | 0 | %18,6 | 0 | 1 | -%6,9 | -%0,9 | 0 (%0,5) | -%0,9 / -%13,7 / -%12,0 |  | X | X |
| 5 | ABD | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %29,5 | 1 | 0 | %35,7 | %19,9 | 1 (%21,7) | %35,7 / -%0,6 / %35,7 |  | X | X |
| 6 | BIST | 2024-26 | 0 | OLUR | OLUR | 1 | %19,0 | 0 | 0 | %0,7 | %31,3 | 1 (%31,7) | %36,0 / -%5,7 / %13,4 |  |  |  |
| 7 | BIST | 2016-22 | 0 | OLUR | OLUR | 0 | %64,3 | 0 | 0 | %0,8 | %1,9 | 0 (%4,6) | %6,5 / -%14,2 / -%11,5 |  | X | X |
| 8 | ABD | 2016-22 | 1 | OLMAZ | OLMAZ | 0 | %26,3 | 0 | 0 | %2,9 | %2,6 | 0 (%3,3) | %6,4 / -%1,9 / %2,9 |  |  |  |
| 9 | BIST | 2016-22 | 0 | OLMAZ | OLMAZ | 1 | %57,9 | 1 | 0 | %34,6 | %27,6 | 1 (%34,2) | %59,5 / %1,6 / %54,5 |  | X | X |
| 10 | ABD | 2016-22 | 0 | OLUR | - | 0 | %8,2 | 0 | 1 | -%8,6 | %2,0 | 0 (%4,5) | %6,7 / -%15,5 / -%13,8 |  | X |  |
| 11 | BIST | 2024-26 | 0 | OLUR | - | 1 | %96,3 | 1 | 0 | %9,3 | %17,0 | 1 (%22,7) | %17,0 / -%2,6 / %5,7 |  |  |  |
| 12 | BIST | 2024-26 | 0 | OLMAZ | - | 0 | %18,9 | 0 | 1 | -%4,2 | %2,4 | 0 (%5,0) | %2,4 / -%33,2 / -%27,4 |  |  |  |
| 13 | BIST | 2024-26 | 0 | OLUR | - | 1 | %71,4 | 1 | 0 | %39,7 | %12,2 | 1 (%15,2) | %50,7 / -%1,8 / %50,5 |  |  |  |
| 14 | AVR | 2016-22 | 0 | OLMAZ | - | 0 | %52,9 | 0 | 0 | %0,7 | %4,7 | 1 (%5,1) | %8,6 / -%4,2 / %6,3 | K |  |  |
| 15 | ABD | 2016-22 | 0 | OLUR | - | 0 | %48,3 | 0 | 0 | -%7,4 | %1,9 | 0 (%3,2) | %2,4 / -%30,5 / -%30,1 |  | X |  |
| 16 | BIST | 2024-26 | 0 | OLMAZ | - | 1 | %68,4 | 0 | 0 | -%0,7 | %7,0 | 1 (%8,9) | %37,4 / -%1,8 / %23,3 |  | X |  |
| 17 | BIST | 2016-22 | 0 | OLUR | - | 0 | %41,4 | 0 | 1 | -%6,2 | %1,1 | 0 (%3,6) | %23,0 / -%13,5 / %23,0 |  | X |  |
| 18 | BIST | 2024-26 | 0 | OLUR | - | 1 | %71,4 | 0 | 0 | %0,1 | %5,6 | 1 (%8,5) | %5,6 / -%11,7 / -%7,4 |  |  |  |
| 19 | BIST | 2024-26 | 0 | OLUR | - | 1 | %61,4 | 1 | 0 | %15,5 | %21,5 | 1 (%32,4) | %50,7 / -%6,2 / %10,5 |  |  |  |
| 20 | AVR | 2024-26 | 0 | OLMAZ | - | 1 | %40,5 | 1 | 0 | %12,8 | %14,2 | 1 (%15,5) | %20,8 / -%0,7 / %14,1 |  | X |  |
| 21 | AVR | 2024-26 | 0 | OLMAZ | - | 0 | %8,6 | 0 | 1 | -%6,4 | %1,7 | 0 (%2,5) | %11,4 / -%11,2 / %11,4 |  |  |  |
| 22 | BIST | 2024-26 | 0 | OLMAZ | - | 1 | %42,4 | 0 | 0 | %1,5 | %9,1 | 1 (%11,3) | %10,0 / -%9,2 / -%6,6 |  | X |  |
| 23 | BIST | 2024-26 | 1 | OLUR | - | 0 | %70,0 | 0 | 1 | -%8,7 | %0,8 | 1 (%6,2) | %2,5 / -%18,4 / -%18,2 |  | X |  |
| 24 | AVR | 2024-26 | 1 | OLMAZ | - | 0 | %45,0 | 0 | 1 | -%16,4 | -%4,1 | 0 (%0,8) | %1,5 / -%25,8 / %1,1 |  |  |  |
| 25 | BIST | 2016-22 | 0 | OLUR | - | 0 | %25,0 | 0 | 1 | -%8,7 | -%0,5 | 0 (%0,4) | -%0,5 / -%17,5 / -%12,6 |  | X |  |
| 26 | BIST | 2024-26 | 0 | OLMAZ | - | 1 | %84,0 | 1 | 0 | %7,7 | %13,7 | 1 (%21,2) | %13,7 / -%14,1 / -%3,4 |  | X |  |
| 27 | ABD | 2024-26 | 0 | OLUR | - | 0 | %30,4 | 0 | 1 | -%3,4 | %4,3 | 1 (%5,1) | %14,6 / -%6,3 / %14,3 | K | X |  |
| 28 | BIST | 2024-26 | 0 | OLUR | - | 1 | %89,3 | 0 | 0 | %0,1 | %8,8 | 1 (%11,7) | %8,8 / -%15,5 / -%5,6 |  |  |  |
| 29 | BIST | 2016-22 | 0 | OLUR | - | 0 | %12,5 | 0 | 0 | -%10,1 | %1,0 | 0 (%1,4) | %3,0 / -%13,3 / %0,0 |  | X |  |
| 30 | BIST | 2024-26 | 1 | OLMAZ | - | 1 | %31,6 | 0 | 0 | %0,8 | %9,6 | 1 (%11,5) | %9,6 / -%10,4 / -%7,9 |  | X |  |
| 31 | AVR | 2016-22 | 0 | OLMAZ | - | 1 | %65,5 | 0 | 0 | %5,6 | %9,9 | 1 (%10,5) | %19,4 / -%2,4 / %19,4 |  | X |  |
| 32 | AVR | 2016-22 | 0 | OLUR | - | 1 | %62,1 | 1 | 0 | %5,9 | %12,6 | 1 (%12,6) | %30,9 / -%1,4 / %25,7 |  |  |  |
| 33 | ABD | 2016-22 | 0 | OLMAZ | - | 0 | %7,7 | 0 | 0 | %18,5 | %0,6 | 0 (%1,4) | %18,5 / -%6,3 / %18,5 |  |  |  |
| 34 | ABD | 2024-26 | 0 | OLMAZ | - | 0 | %41,7 | 0 | 1 | -%4,1 | %4,1 | 1 (%7,5) | %20,4 / -%12,8 / %20,1 | K |  |  |
| 35 | ABD | 2016-22 | 1 | OLMAZ | - | 0 | %31,7 | 0 | 0 | %28,5 | %2,7 | 0 (%5,0) | %28,5 / -%4,0 / %28,5 |  |  |  |
| 36 | BIST | 2016-22 | 0 | OLMAZ | - | 0 | %52,6 | 0 | 1 | -%5,6 | %1,8 | 1 (%5,6) | %1,8 / -%16,2 / -%13,7 |  |  |  |
| 37 | ABD | 2023 | 0 | OLMAZ | - | 1 | %86,6 | 0 | 0 | -%0,5 | %6,6 | 1 (%7,5) | %6,6 / -%8,0 / %2,0 |  | X |  |
| 38 | BIST | 2016-22 | 0 | OLMAZ | - | 0 | %31,6 | 0 | 1 | -%12,6 | -%1,3 | 0 (%3,8) | -%1,3 / -%19,2 / -%14,6 |  |  |  |
| 39 | ABD | 2023 | 0 | OLMAZ | - | 0 | %31,9 | 0 | 1 | -%4,0 | %3,9 | 1 (%5,8) | %3,9 / -%25,0 / -%22,7 | K |  |  |
| 40 | BIST | 2024-26 | 0 | OLMAZ | - | 1 | %84,4 | 1 | 0 | %63,6 | %76,7 | 1 (%86,5) | %88,1 / %9,5 / %69,3 |  | X |  |

Bilgi sütunları (B1.0): Fiyat = ge_hazir (YAPI_HEDEF geçerli bar + kriz kesiği 31.08.2026). Bar 0 = giriş günü (olay 'giris'; geçerli bar olmalı, yoksa DURUR), E0 = giriş günü açılışı (olay dosyasında E0 varsa göreli 1e-4 ile aynı olmalı, yoksa DURUR). 15 g = bar 0..14 (15 geçerli bar; h5 ile aynı sayım, stop YOK); 60 g = bar 0..59 (60 geçerli bar; kriz kesiği ya da hissenin son barı yüzünden 60 bar yoksa 60 g sütunları NaN = ölçülemedi). k15 = max Close(0..14) / E0 - 1; gi15 = max High(0..14) / E0 - 1; m60 / n60 / s60 = max / min / son (bar 59) Close(0..59) / E0 - 1. yön doğru / eşik kaçtı: karar OLUR VE h5 = 0 VE +%3 <= k15 < +%5 (kapanışla +%3..+%5 arası kaldı). Bilgi; BAŞARI'yı değiştirmez. 'eşik kaçtı' sütunu (K) sayfanın kapanış bandını gösterir; taraf sayımı yalnız o tarafın OLUR dediği sayfalarda.

Not: küçük örneklem (40 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
