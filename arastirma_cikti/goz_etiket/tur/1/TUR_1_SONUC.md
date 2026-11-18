# HAKEM TURU 1 — SONUÇ

Mühür sırası: TUTTU · 2026-11-18 10:53:17 UTC

BAŞARI tanımı (önceden yazılı): CLAUDE.md 'Hakem turları' (önceden yazılı, değişmez): sonuç = olay_Y1 h5 (15 geçerli barda +%5 kapanışla, stop'tan önce; 1 / 0; NaN ölçülemedi). OLUR isabeti = OLUR'larda h5 = 1 payı; OLMAZ isabeti = OLMAZ'larda h5 = 0 payı; BAŞARI = (doğru OLUR + doğru OLMAZ) / (OLUR + OLMAZ) (BELİRSİZ karar değil, ayrı sayılır; h5 NaN sayfa ölçülemedi, ayrı sayılır). Taban = aynı sayfaların eş payı (ortalama es_h5). Fisher iki yönlü (karar OLUR / OLMAZ x h5). Uyum = Cohen kappa (3 sınıf, iki tarafın da geçerli yanıtı olan sayfalar). Birikimli = tur 1..K satır dosyaları birleşik.

**Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).**

## İsabet tablosu

| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (bu tur) | 7 / 23 / 0 | 3 / 7 (%42,9) | 11 / 23 (%47,8) | **%46,7** (14 / 30) | %43,0 | %41,5 | %50,0 | 1,000 | 0 / 0 |
| Cemal (bu tur) | 13 / 9 / 8 | 6 / 13 (%46,2) | 4 / 9 (%44,4) | **%45,5** (10 / 22) | %36,8 | %41,5 | %50,0 | 1,000 | 0 / 0 |
| model (birikimli, tur [1]) | 7 / 23 / 0 | 3 / 7 (%42,9) | 11 / 23 (%47,8) | **%46,7** (14 / 30) | %43,0 | %41,5 | %50,0 | 1,000 | 0 / 0 |
| Cemal (birikimli, tur [1]) | 13 / 9 / 8 | 6 / 13 (%46,2) | 4 / 9 (%44,4) | **%45,5** (10 / 22) | %36,8 | %41,5 | %50,0 | 1,000 | 0 / 0 |

- Uyum (kappa, 3 sınıf): bu tur 0,153 (n 30); birikimli 0,153 (n 30).
- Yanılınan sayfalar: model [3, 4, 5, 6, 7, 8, 9, 11, 17, 20, 21, 22, 23, 26, 29, 30]; Cemal [1, 9, 10, 11, 12, 17, 18, 22, 23, 26, 28, 30].
- Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).
- Bilgi sütunlarıyla yeniden koşu: 2026-11-18 12:56:58 UTC (TUTTU (önceki tur_K_sonuc.json ile karar sayıları aynı)).

Üç cetvel (bilgi; BAŞARI yalnız ilk cetvelle, değişmez):

| Taraf | Cetvel | OLUR isabeti | OLMAZ isabeti | BAŞARI | taban (sayfa payı) | hep OLMAZ deseydi | ölçülemedi |
|---|---|---|---|---|---|---|---|
| model (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 3 / 7 (%42,9) | 11 / 23 (%47,8) | **%46,7** (14 / 30) | %50,0 | %50,0 | 0 |
| model (bu tur) | 15 g gün içi +%5 (High; bilgi) | 4 / 7 (%57,1) | 7 / 23 (%30,4) | **%36,7** (11 / 30) | %66,7 | %33,3 | 0 |
| model (bu tur) | 60 g kapanış +%5 (bilgi) | 6 / 7 (%85,7) | 7 / 21 (%33,3) | **%46,4** (13 / 28) | %71,4 | %28,6 | 2 |
| Cemal (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 6 / 13 (%46,2) | 4 / 9 (%44,4) | **%45,5** (10 / 22) | %50,0 | %50,0 | 0 |
| Cemal (bu tur) | 15 g gün içi +%5 (High; bilgi) | 9 / 13 (%69,2) | 2 / 9 (%22,2) | **%50,0** (11 / 22) | %66,7 | %33,3 | 0 |
| Cemal (bu tur) | 60 g kapanış +%5 (bilgi) | 9 / 12 (%75,0) | 1 / 9 (%11,1) | **%47,6** (10 / 21) | %71,4 | %28,6 | 2 |
| model (birikimli, tur [1]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 3 / 7 (%42,9) | 11 / 23 (%47,8) | **%46,7** (14 / 30) | %50,0 | %50,0 | 0 |
| model (birikimli, tur [1]) | 15 g gün içi +%5 (High; bilgi) | 4 / 7 (%57,1) | 7 / 23 (%30,4) | **%36,7** (11 / 30) | %66,7 | %33,3 | 0 |
| model (birikimli, tur [1]) | 60 g kapanış +%5 (bilgi) | 6 / 7 (%85,7) | 7 / 21 (%33,3) | **%46,4** (13 / 28) | %71,4 | %28,6 | 2 |
| Cemal (birikimli, tur [1]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 6 / 13 (%46,2) | 4 / 9 (%44,4) | **%45,5** (10 / 22) | %50,0 | %50,0 | 0 |
| Cemal (birikimli, tur [1]) | 15 g gün içi +%5 (High; bilgi) | 9 / 13 (%69,2) | 2 / 9 (%22,2) | **%50,0** (11 / 22) | %66,7 | %33,3 | 0 |
| Cemal (birikimli, tur [1]) | 60 g kapanış +%5 (bilgi) | 9 / 12 (%75,0) | 1 / 9 (%11,1) | **%47,6** (10 / 21) | %71,4 | %28,6 | 2 |
- Yön doğru / eşik kaçtı (OLUR, h5 = 0, 15 g kapanış max +%3..+%5): model [22]; Cemal [1, 22, 28]; birikimli model 1, Cemal 3.

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | 15 g kapanış max (bilgi) | gün içi +%5 (15 g High; bilgi) | 60 g max / min / son kapanış (bilgi) | eşik kaçtı (+%3..+%5) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIST | 2024-26 | 0 | OLMAZ | OLUR | 0 | %49,0 | 0 | 1 | -%5,0 | %4,9 | 1 (%8,3) | ölçülemedi | K |  | X |
| 2 | AVR | 2023 | 0 | OLMAZ | OLMAZ | 0 | %51,2 | 0 | 0 | %3,7 | %4,7 | 1 (%5,4) | %9,5 / -%2,2 / %3,7 | K |  |  |
| 3 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %42,6 | 1 | 0 | %5,6 | %13,4 | 1 (%14,8) | ölçülemedi |  | X |  |
| 4 | AVR | 2023 | 1 | OLMAZ | OLUR | 1 | %30,8 | 0 | 0 | -%2,7 | %5,3 | 1 (%7,5) | %5,3 / -%60,2 / -%60,2 |  | X |  |
| 5 | ABD | 2024-26 | 1 | OLMAZ | BELİRSİZ | 1 | %17,5 | 0 | 0 | %1,2 | %6,6 | 1 (%8,5) | %14,3 / -%20,0 / -%15,0 |  | X |  |
| 6 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %60,3 | 0 | 0 | %1,0 | %8,8 | 1 (%9,9) | %8,8 / -%27,1 / -%16,1 |  | X |  |
| 7 | BIST | 2023 | 0 | OLMAZ | BELİRSİZ | 1 | %74,2 | 1 | 0 | %13,0 | %25,5 | 1 (%31,0) | %93,0 / -%6,5 / %52,2 |  | X |  |
| 8 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 1 | %31,4 | 0 | 0 | %6,9 | %6,4 | 1 (%6,5) | %16,5 / -%2,8 / %10,4 |  | X |  |
| 9 | ABD | 2023 | 0 | OLMAZ | OLMAZ | 1 | %54,8 | 0 | 0 | %1,1 | %7,0 | 1 (%7,8) | %7,0 / -%14,7 / -%14,7 |  | X | X |
| 10 | ABD | 2023 | 0 | OLMAZ | OLUR | 0 | %25,3 | 0 | 1 | -%8,9 | %1,2 | 0 (%1,8) | %1,2 / -%16,4 / -%12,6 |  |  | X |
| 11 | ABD | 2024-26 | 1 | OLMAZ | OLMAZ | 1 | %19,0 | 0 | 0 | %2,8 | %6,3 | 1 (%6,7) | %11,1 / -%3,0 / %8,8 |  | X | X |
| 12 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %39,6 | 0 | 0 | -%7,9 | -%0,6 | 0 (%0,9) | -%0,6 / -%16,2 / -%11,3 |  |  | X |
| 13 | BIST | 2024-26 | 1 | OLUR | OLUR | 1 | %54,3 | 0 | 0 | %0,4 | %10,4 | 1 (%15,6) | %10,4 / -%16,4 / -%14,2 |  |  |  |
| 14 | ABD | 2023 | 1 | OLUR | OLUR | 1 | %51,4 | 0 | 0 | %1,4 | %8,8 | 1 (%14,5) | %32,6 / -%1,3 / %30,2 |  |  |  |
| 15 | ABD | 2023 | 0 | OLMAZ | BELİRSİZ | 0 | %61,3 | 0 | 0 | -%6,5 | %3,5 | 0 (%4,2) | %3,5 / -%9,6 / -%7,3 | K |  |  |
| 16 | ABD | 2023 | 1 | OLUR | OLUR | 1 | %19,4 | 0 | 0 | -%0,1 | %8,4 | 1 (%11,5) | %72,7 / -%10,3 / %64,6 |  |  |  |
| 17 | ABD | 2024-26 | 1 | OLMAZ | OLMAZ | 1 | %53,2 | 1 | 0 | %0,6 | %21,2 | 1 (%29,0) | %21,2 / -%25,9 / -%17,8 |  | X | X |
| 18 | ABD | 2023 | 1 | OLMAZ | OLUR | 0 | %38,8 | 0 | 0 | %12,1 | %2,8 | 0 (%4,7) | %22,5 / -%3,0 / %21,2 |  |  | X |
| 19 | ABD | 2024-26 | 0 | OLMAZ | OLMAZ | 0 | %38,4 | 0 | 0 | -%5,1 | %2,4 | 0 (%2,9) | %2,4 / -%12,9 / -%3,4 |  |  |  |
| 20 | AVR | 2024-26 | 1 | OLUR | OLMAZ | 0 | %45,7 | 0 | 0 | %11,9 | %2,0 | 0 (%2,8) | %12,6 / -%1,2 / %11,9 |  | X |  |
| 21 | ABD | 2023 | 1 | OLUR | BELİRSİZ | 0 | %57,9 | 0 | 0 | -%1,4 | %1,3 | 0 (%2,8) | %2,3 / -%3,6 / -%1,4 |  | X |  |
| 22 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %58,2 | 0 | 0 | -%6,5 | %4,1 | 1 (%6,0) | %8,3 / -%12,1 / %8,3 | K | X | X |
| 23 | BIST | 2023 | 0 | OLUR | OLUR | 0 | %14,3 | 0 | 1 | -%6,1 | %2,3 | 0 (%3,2) | %22,3 / -%16,5 / %18,1 |  | X | X |
| 24 | ABD | 2023 | 1 | OLMAZ | BELİRSİZ | 0 | %23,1 | 0 | 0 | -%10,7 | %1,5 | 0 (%2,1) | %3,0 / -%16,6 / -%9,8 |  |  |  |
| 25 | ABD | 2023 | 0 | OLMAZ | OLMAZ | 0 | %32,9 | 0 | 1 | -%3,8 | %3,6 | 1 (%6,0) | %6,4 / -%7,9 / -%7,5 | K |  |  |
| 26 | ABD | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %49,3 | 0 | 0 | %13,7 | %8,2 | 1 (%8,3) | %20,4 / %1,4 / %17,1 |  | X | X |
| 27 | BIST | 2024-26 | 1 | OLMAZ | BELİRSİZ | 0 | %30,2 | 0 | 0 | -%8,9 | -%3,6 | 0 (%1,7) | %3,8 / -%13,5 / -%10,7 |  |  |  |
| 28 | AVR | 2023 | 1 | OLMAZ | OLUR | 0 | %51,5 | 0 | 0 | -%4,1 | %4,0 | 1 (%5,2) | %4,0 / -%9,5 / -%3,8 | K |  | X |
| 29 | ABD | 2023 | 1 | OLMAZ | OLUR | 1 | %14,8 | 0 | 0 | -%0,4 | %6,4 | 1 (%7,5) | %52,4 / -%15,2 / %32,8 |  | X |  |
| 30 | AVR | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %55,3 | 0 | 0 | %22,6 | %8,0 | 1 (%8,6) | %33,9 / %0,2 / %25,5 |  | X | X |

Bilgi sütunları (B1.0): Fiyat = ge_hazir (YAPI_HEDEF geçerli bar + kriz kesiği 31.08.2026). Bar 0 = giriş günü (olay 'giris'; geçerli bar olmalı, yoksa DURUR), E0 = giriş günü açılışı (olay dosyasında E0 varsa göreli 1e-4 ile aynı olmalı, yoksa DURUR). 15 g = bar 0..14 (15 geçerli bar; h5 ile aynı sayım, stop YOK); 60 g = bar 0..59 (60 geçerli bar; kriz kesiği ya da hissenin son barı yüzünden 60 bar yoksa 60 g sütunları NaN = ölçülemedi). k15 = max Close(0..14) / E0 - 1; gi15 = max High(0..14) / E0 - 1; m60 / n60 / s60 = max / min / son (bar 59) Close(0..59) / E0 - 1. yön doğru / eşik kaçtı: karar OLUR VE h5 = 0 VE +%3 <= k15 < +%5 (kapanışla +%3..+%5 arası kaldı). Bilgi; BAŞARI'yı değiştirmez. 'eşik kaçtı' sütunu (K) sayfanın kapanış bandını gösterir; taraf sayımı yalnız o tarafın OLUR dediği sayfalarda.

Not: küçük örneklem (30 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
