# HAKEM TURU 2 — SONUÇ

Mühür sırası: TUTTU · 2026-11-18 12:50:38 UTC

BAŞARI tanımı (önceden yazılı): CLAUDE.md 'Hakem turları' (önceden yazılı, değişmez): sonuç = olay_Y1 h5 (15 geçerli barda +%5 kapanışla, stop'tan önce; 1 / 0; NaN ölçülemedi). OLUR isabeti = OLUR'larda h5 = 1 payı; OLMAZ isabeti = OLMAZ'larda h5 = 0 payı; BAŞARI = (doğru OLUR + doğru OLMAZ) / (OLUR + OLMAZ) (BELİRSİZ karar değil, ayrı sayılır; h5 NaN sayfa ölçülemedi, ayrı sayılır). Taban = aynı sayfaların eş payı (ortalama es_h5). Fisher iki yönlü (karar OLUR / OLMAZ x h5). Uyum = Cohen kappa (3 sınıf, iki tarafın da geçerli yanıtı olan sayfalar). Birikimli = tur 1..K satır dosyaları birleşik.

**Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).**

## İsabet tablosu

| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (bu tur) | 21 / 8 / 1 | 10 / 21 (%47,6) | 6 / 8 (%75,0) | **%55,2** (16 / 29) | %43,8 | %41,4 | %60,0 | 0,408 | 0 / 0 |
| Cemal (bu tur) | 15 / 4 / 11 | 5 / 15 (%33,3) | 1 / 4 (%25,0) | **%31,6** (6 / 19) | %44,4 | %41,4 | %60,0 | 0,262 | 0 / 0 |
| model (birikimli, tur [1, 2]) | 28 / 31 / 1 | 13 / 28 (%46,4) | 17 / 31 (%54,8) | **%50,8** (30 / 59) | %43,6 | %41,5 | %55,0 | 1,000 | 0 / 0 |
| Cemal (birikimli, tur [1, 2]) | 28 / 13 / 19 | 11 / 28 (%39,3) | 5 / 13 (%38,5) | **%39,0** (16 / 41) | %40,9 | %41,5 | %55,0 | 0,313 | 0 / 0 |

- Uyum (kappa, 3 sınıf): bu tur -0,052 (n 30); birikimli 0,098 (n 60).
- Yanılınan sayfalar: model [4, 7, 8, 9, 14, 16, 17, 20, 23, 24, 25, 26, 29]; Cemal [2, 4, 5, 8, 10, 14, 15, 16, 20, 26, 27, 28, 30].
- Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).
- Bilgi sütunlarıyla yeniden koşu: 2026-11-18 12:57:13 UTC (TUTTU (önceki tur_K_sonuc.json ile karar sayıları aynı)).

Üç cetvel (bilgi; BAŞARI yalnız ilk cetvelle, değişmez):

| Taraf | Cetvel | OLUR isabeti | OLMAZ isabeti | BAŞARI | taban (sayfa payı) | hep OLMAZ deseydi | ölçülemedi |
|---|---|---|---|---|---|---|---|
| model (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 10 / 21 (%47,6) | 6 / 8 (%75,0) | **%55,2** (16 / 29) | %40,0 | %60,0 | 0 |
| model (bu tur) | 15 g gün içi +%5 (High; bilgi) | 10 / 21 (%47,6) | 3 / 8 (%37,5) | **%44,8** (13 / 29) | %50,0 | %50,0 | 0 |
| model (bu tur) | 60 g kapanış +%5 (bilgi) | 17 / 21 (%81,0) | 1 / 8 (%12,5) | **%62,1** (18 / 29) | %80,0 | %20,0 | 0 |
| Cemal (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 5 / 15 (%33,3) | 1 / 4 (%25,0) | **%31,6** (6 / 19) | %40,0 | %60,0 | 0 |
| Cemal (bu tur) | 15 g gün içi +%5 (High; bilgi) | 7 / 15 (%46,7) | 1 / 4 (%25,0) | **%42,1** (8 / 19) | %50,0 | %50,0 | 0 |
| Cemal (bu tur) | 60 g kapanış +%5 (bilgi) | 12 / 15 (%80,0) | 0 / 4 (%0,0) | **%63,2** (12 / 19) | %80,0 | %20,0 | 0 |
| model (birikimli, tur [1, 2]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 13 / 28 (%46,4) | 17 / 31 (%54,8) | **%50,8** (30 / 59) | %45,0 | %55,0 | 0 |
| model (birikimli, tur [1, 2]) | 15 g gün içi +%5 (High; bilgi) | 14 / 28 (%50,0) | 10 / 31 (%32,3) | **%40,7** (24 / 59) | %58,3 | %41,7 | 0 |
| model (birikimli, tur [1, 2]) | 60 g kapanış +%5 (bilgi) | 23 / 28 (%82,1) | 8 / 29 (%27,6) | **%54,4** (31 / 57) | %75,9 | %24,1 | 2 |
| Cemal (birikimli, tur [1, 2]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 11 / 28 (%39,3) | 5 / 13 (%38,5) | **%39,0** (16 / 41) | %45,0 | %55,0 | 0 |
| Cemal (birikimli, tur [1, 2]) | 15 g gün içi +%5 (High; bilgi) | 16 / 28 (%57,1) | 3 / 13 (%23,1) | **%46,3** (19 / 41) | %58,3 | %41,7 | 0 |
| Cemal (birikimli, tur [1, 2]) | 60 g kapanış +%5 (bilgi) | 21 / 27 (%77,8) | 1 / 13 (%7,7) | **%55,0** (22 / 40) | %75,9 | %24,1 | 2 |
- Yön doğru / eşik kaçtı (OLUR, h5 = 0, 15 g kapanış max +%3..+%5): model [9, 24, 25]; Cemal [5, 15]; birikimli model 4, Cemal 5.

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | 15 g kapanış max (bilgi) | gün içi +%5 (15 g High; bilgi) | 60 g max / min / son kapanış (bilgi) | eşik kaçtı (+%3..+%5) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | 2024-26 | 1 | OLUR | OLUR | 1 | %71,2 | 0 | 0 | %1,1 | %7,0 | 1 (%7,5) | %52,4 / -%3,1 / %52,4 |  |  |  |
| 2 | AVR | 2023 | 0 | OLUR | OLMAZ | 1 | %47,1 | 0 | 0 | %12,9 | %7,4 | 1 (%8,7) | %20,8 / -%0,5 / %13,8 |  |  | X |
| 3 | ABD | 2024-26 | 0 | OLUR | OLUR | 1 | %47,4 | 1 | 0 | %17,1 | %30,0 | 1 (%30,6) | %44,2 / -%4,1 / %40,8 |  |  |  |
| 4 | BIST | 2023 | 0 | OLUR | OLUR | 0 | %72,4 | 0 | 1 | -%7,8 | -%1,7 | 0 (%0,9) | %19,0 / -%12,1 / %7,8 |  | X | X |
| 5 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %59,4 | 0 | 0 | -%0,5 | %4,8 | 1 (%5,4) | %23,0 / -%8,9 / %20,1 | K |  | X |
| 6 | AVR | 2024-26 | 0 | OLMAZ | OLMAZ | 0 | %3,6 | 0 | 0 | %9,0 | %3,1 | 0 (%3,8) | %9,0 / %0,3 / %9,0 | K |  |  |
| 7 | BIST | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %62,1 | 0 | 1 | -%9,3 | -%1,4 | 0 (%0,1) | -%1,4 / -%18,5 / -%17,5 |  | X |  |
| 8 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %12,2 | 0 | 0 | %1,2 | %2,2 | 0 (%2,8) | %7,0 / -%2,9 / %1,6 |  | X | X |
| 9 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %40,2 | 0 | 0 | %11,7 | %4,1 | 0 (%4,7) | %26,3 / -%0,7 / %7,7 | K | X |  |
| 10 | ABD | 2023 | 0 | OLMAZ | OLUR | 0 | %11,8 | 0 | 1 | -%6,0 | %2,0 | 0 (%4,3) | %2,0 / -%33,6 / -%20,7 |  |  | X |
| 11 | ABD | 2024-26 | 1 | OLUR | OLUR | 1 | %64,7 | 0 | 0 | %6,2 | %9,0 | 1 (%10,1) | %19,8 / -%1,6 / %19,8 |  |  |  |
| 12 | ABD | 2023 | 0 | OLUR | BELİRSİZ | 1 | %39,1 | 0 | 0 | -%0,1 | %5,4 | 1 (%5,7) | %16,3 / -%0,4 / %3,7 |  |  |  |
| 13 | BIST | 2023 | 1 | OLUR | BELİRSİZ | 1 | %34,8 | 0 | 0 | -%3,9 | %5,6 | 1 (%15,2) | %11,6 / -%28,7 / %11,6 |  |  |  |
| 14 | ABD | 2023 | 1 | OLMAZ | OLMAZ | 1 | %64,9 | 1 | 0 | %6,9 | %17,4 | 1 (%19,5) | %27,0 / -%19,6 / -%17,7 |  | X | X |
| 15 | ABD | 2023 | 1 | OLMAZ | OLUR | 0 | %47,7 | 0 | 1 | -%12,9 | %4,6 | 1 (%7,6) | %8,0 / -%27,3 / -%17,2 | K |  | X |
| 16 | ABD | 2023 | 1 | OLUR | OLUR | 0 | %20,0 | 0 | 1 | -%8,8 | -%1,5 | 0 (%0,2) | -%1,5 / -%17,9 / -%17,9 |  | X | X |
| 17 | AVR | 2023 | 1 | OLUR | BELİRSİZ | 0 | %25,0 | 0 | 0 | -%4,8 | %2,1 | 0 (%2,6) | %3,2 / -%14,1 / -%13,4 |  | X |  |
| 18 | ABD | 2023 | 1 | OLUR | BELİRSİZ | 1 | %53,5 | 1 | 0 | %20,2 | %13,5 | 1 (%14,0) | %30,1 / %1,3 / %18,6 |  |  |  |
| 19 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 0 | %36,2 | 0 | 1 | -%6,7 | %1,5 | 1 (%5,5) | %6,4 / -%7,5 / %5,6 |  |  |  |
| 20 | ABD | 2023 | 0 | OLUR | OLUR | 0 | %8,6 | 0 | 1 | -%6,6 | -%0,0 | 0 (%1,8) | %21,3 / -%16,0 / %19,9 |  | X | X |
| 21 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 1 | %36,9 | 1 | 0 | -%7,1 | %11,2 | 1 (%12,3) | %11,7 / -%6,9 / %0,7 |  |  |  |
| 22 | BIST | 2024-26 | 0 | OLUR | OLUR | 1 | %100,0 | 1 | 0 | %8,7 | %18,3 | 1 (%19,9) | %18,3 / -%28,0 / -%16,7 |  |  |  |
| 23 | ABD | 2024-26 | 1 | OLMAZ | OLUR | 1 | %38,8 | 0 | 0 | %28,0 | %7,1 | 1 (%8,6) | %34,5 / %0,2 / %28,0 |  | X |  |
| 24 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %53,0 | 0 | 0 | %1,6 | %3,1 | 0 (%4,5) | %5,2 / -%12,0 / -%6,3 | K | X |  |
| 25 | AVR | 2024-26 | 1 | OLUR | BELİRSİZ | 0 | %38,2 | 0 | 0 | %11,6 | %3,0 | 0 (%3,6) | %11,6 / %0,1 / %11,6 | K | X |  |
| 26 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %50,7 | 0 | 1 | -%8,2 | -%0,4 | 0 (%0,1) | %8,1 / -%14,6 / -%7,7 |  | X | X |
| 27 | AVR | 2024-26 | 1 | OLUR | OLMAZ | 1 | %33,3 | 0 | 0 | -%0,2 | %8,8 | 1 (%11,5) | %8,8 / -%20,4 / -%19,9 |  |  | X |
| 28 | ABD | 2024-26 | 1 | BELİRSİZ | OLUR | 0 | %34,7 | 0 | 0 | -%0,7 | %1,4 | 0 (%2,2) | %1,4 / -%4,9 / -%0,7 |  |  | X |
| 29 | ABD | 2023 | 0 | OLUR | BELİRSİZ | 0 | %9,1 | 0 | 1 | -%9,0 | -%0,4 | 0 (%1,1) | %1,2 / -%32,1 / -%22,8 |  | X |  |
| 30 | BIST | 2023 | 1 | OLMAZ | OLUR | 0 | %26,3 | 0 | 1 | -%5,3 | %1,0 | 0 (%1,3) | %12,6 / -%36,3 / %4,7 |  |  | X |

Bilgi sütunları (B1.0): Fiyat = ge_hazir (YAPI_HEDEF geçerli bar + kriz kesiği 31.08.2026). Bar 0 = giriş günü (olay 'giris'; geçerli bar olmalı, yoksa DURUR), E0 = giriş günü açılışı (olay dosyasında E0 varsa göreli 1e-4 ile aynı olmalı, yoksa DURUR). 15 g = bar 0..14 (15 geçerli bar; h5 ile aynı sayım, stop YOK); 60 g = bar 0..59 (60 geçerli bar; kriz kesiği ya da hissenin son barı yüzünden 60 bar yoksa 60 g sütunları NaN = ölçülemedi). k15 = max Close(0..14) / E0 - 1; gi15 = max High(0..14) / E0 - 1; m60 / n60 / s60 = max / min / son (bar 59) Close(0..59) / E0 - 1. yön doğru / eşik kaçtı: karar OLUR VE h5 = 0 VE +%3 <= k15 < +%5 (kapanışla +%3..+%5 arası kaldı). Bilgi; BAŞARI'yı değiştirmez. 'eşik kaçtı' sütunu (K) sayfanın kapanış bandını gösterir; taraf sayımı yalnız o tarafın OLUR dediği sayfalarda.

Not: küçük örneklem (30 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
