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

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BIST | 2024-26 | 0 | OLMAZ | OLUR | 0 | %49,0 | 0 | 1 | -%5,0 |  | X |
| 2 | AVR | 2023 | 0 | OLMAZ | OLMAZ | 0 | %51,2 | 0 | 0 | %3,7 |  |  |
| 3 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %42,6 | 1 | 0 | %5,6 | X |  |
| 4 | AVR | 2023 | 1 | OLMAZ | OLUR | 1 | %30,8 | 0 | 0 | -%2,7 | X |  |
| 5 | ABD | 2024-26 | 1 | OLMAZ | BELİRSİZ | 1 | %17,5 | 0 | 0 | %1,2 | X |  |
| 6 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 1 | %60,3 | 0 | 0 | %1,0 | X |  |
| 7 | BIST | 2023 | 0 | OLMAZ | BELİRSİZ | 1 | %74,2 | 1 | 0 | %13,0 | X |  |
| 8 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 1 | %31,4 | 0 | 0 | %6,9 | X |  |
| 9 | ABD | 2023 | 0 | OLMAZ | OLMAZ | 1 | %54,8 | 0 | 0 | %1,1 | X | X |
| 10 | ABD | 2023 | 0 | OLMAZ | OLUR | 0 | %25,3 | 0 | 1 | -%8,9 |  | X |
| 11 | ABD | 2024-26 | 1 | OLMAZ | OLMAZ | 1 | %19,0 | 0 | 0 | %2,8 | X | X |
| 12 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %39,6 | 0 | 0 | -%7,9 |  | X |
| 13 | BIST | 2024-26 | 1 | OLUR | OLUR | 1 | %54,3 | 0 | 0 | %0,4 |  |  |
| 14 | ABD | 2023 | 1 | OLUR | OLUR | 1 | %51,4 | 0 | 0 | %1,4 |  |  |
| 15 | ABD | 2023 | 0 | OLMAZ | BELİRSİZ | 0 | %61,3 | 0 | 0 | -%6,5 |  |  |
| 16 | ABD | 2023 | 1 | OLUR | OLUR | 1 | %19,4 | 0 | 0 | -%0,1 |  |  |
| 17 | ABD | 2024-26 | 1 | OLMAZ | OLMAZ | 1 | %53,2 | 1 | 0 | %0,6 | X | X |
| 18 | ABD | 2023 | 1 | OLMAZ | OLUR | 0 | %38,8 | 0 | 0 | %12,1 |  | X |
| 19 | ABD | 2024-26 | 0 | OLMAZ | OLMAZ | 0 | %38,4 | 0 | 0 | -%5,1 |  |  |
| 20 | AVR | 2024-26 | 1 | OLUR | OLMAZ | 0 | %45,7 | 0 | 0 | %11,9 | X |  |
| 21 | ABD | 2023 | 1 | OLUR | BELİRSİZ | 0 | %57,9 | 0 | 0 | -%1,4 | X |  |
| 22 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %58,2 | 0 | 0 | -%6,5 | X | X |
| 23 | BIST | 2023 | 0 | OLUR | OLUR | 0 | %14,3 | 0 | 1 | -%6,1 | X | X |
| 24 | ABD | 2023 | 1 | OLMAZ | BELİRSİZ | 0 | %23,1 | 0 | 0 | -%10,7 |  |  |
| 25 | ABD | 2023 | 0 | OLMAZ | OLMAZ | 0 | %32,9 | 0 | 1 | -%3,8 |  |  |
| 26 | ABD | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %49,3 | 0 | 0 | %13,7 | X | X |
| 27 | BIST | 2024-26 | 1 | OLMAZ | BELİRSİZ | 0 | %30,2 | 0 | 0 | -%8,9 |  |  |
| 28 | AVR | 2023 | 1 | OLMAZ | OLUR | 0 | %51,5 | 0 | 0 | -%4,1 |  | X |
| 29 | ABD | 2023 | 1 | OLMAZ | OLUR | 1 | %14,8 | 0 | 0 | -%0,4 | X |  |
| 30 | AVR | 2024-26 | 0 | OLMAZ | OLMAZ | 1 | %55,3 | 0 | 0 | %22,6 | X | X |

Not: küçük örneklem (30 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
