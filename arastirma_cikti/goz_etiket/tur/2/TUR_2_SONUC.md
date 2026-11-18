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

## Sayfa sayfa (sonuç açıldı)

| Sayfa | Pazar | Dönem | parmak (F19) | Model | Cemal | +%5 gördü (h5) | eş payı | +%10 (h10) | stop önce (st5) | getiri (takip stoplu, bilgi) | model yanıldı | Cemal yanıldı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | 2024-26 | 1 | OLUR | OLUR | 1 | %71,2 | 0 | 0 | %1,1 |  |  |
| 2 | AVR | 2023 | 0 | OLUR | OLMAZ | 1 | %47,1 | 0 | 0 | %12,9 |  | X |
| 3 | ABD | 2024-26 | 0 | OLUR | OLUR | 1 | %47,4 | 1 | 0 | %17,1 |  |  |
| 4 | BIST | 2023 | 0 | OLUR | OLUR | 0 | %72,4 | 0 | 1 | -%7,8 | X | X |
| 5 | ABD | 2024-26 | 0 | OLMAZ | OLUR | 0 | %59,4 | 0 | 0 | -%0,5 |  | X |
| 6 | AVR | 2024-26 | 0 | OLMAZ | OLMAZ | 0 | %3,6 | 0 | 0 | %9,0 |  |  |
| 7 | BIST | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %62,1 | 0 | 1 | -%9,3 | X |  |
| 8 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %12,2 | 0 | 0 | %1,2 | X | X |
| 9 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %40,2 | 0 | 0 | %11,7 | X |  |
| 10 | ABD | 2023 | 0 | OLMAZ | OLUR | 0 | %11,8 | 0 | 1 | -%6,0 |  | X |
| 11 | ABD | 2024-26 | 1 | OLUR | OLUR | 1 | %64,7 | 0 | 0 | %6,2 |  |  |
| 12 | ABD | 2023 | 0 | OLUR | BELİRSİZ | 1 | %39,1 | 0 | 0 | -%0,1 |  |  |
| 13 | BIST | 2023 | 1 | OLUR | BELİRSİZ | 1 | %34,8 | 0 | 0 | -%3,9 |  |  |
| 14 | ABD | 2023 | 1 | OLMAZ | OLMAZ | 1 | %64,9 | 1 | 0 | %6,9 | X | X |
| 15 | ABD | 2023 | 1 | OLMAZ | OLUR | 0 | %47,7 | 0 | 1 | -%12,9 |  | X |
| 16 | ABD | 2023 | 1 | OLUR | OLUR | 0 | %20,0 | 0 | 1 | -%8,8 | X | X |
| 17 | AVR | 2023 | 1 | OLUR | BELİRSİZ | 0 | %25,0 | 0 | 0 | -%4,8 | X |  |
| 18 | ABD | 2023 | 1 | OLUR | BELİRSİZ | 1 | %53,5 | 1 | 0 | %20,2 |  |  |
| 19 | ABD | 2024-26 | 0 | OLMAZ | BELİRSİZ | 0 | %36,2 | 0 | 1 | -%6,7 |  |  |
| 20 | ABD | 2023 | 0 | OLUR | OLUR | 0 | %8,6 | 0 | 1 | -%6,6 | X | X |
| 21 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 1 | %36,9 | 1 | 0 | -%7,1 |  |  |
| 22 | BIST | 2024-26 | 0 | OLUR | OLUR | 1 | %100,0 | 1 | 0 | %8,7 |  |  |
| 23 | ABD | 2024-26 | 1 | OLMAZ | OLUR | 1 | %38,8 | 0 | 0 | %28,0 | X |  |
| 24 | ABD | 2024-26 | 0 | OLUR | BELİRSİZ | 0 | %53,0 | 0 | 0 | %1,6 | X |  |
| 25 | AVR | 2024-26 | 1 | OLUR | BELİRSİZ | 0 | %38,2 | 0 | 0 | %11,6 | X |  |
| 26 | ABD | 2024-26 | 1 | OLUR | OLUR | 0 | %50,7 | 0 | 1 | -%8,2 | X | X |
| 27 | AVR | 2024-26 | 1 | OLUR | OLMAZ | 1 | %33,3 | 0 | 0 | -%0,2 |  | X |
| 28 | ABD | 2024-26 | 1 | BELİRSİZ | OLUR | 0 | %34,7 | 0 | 0 | -%0,7 |  | X |
| 29 | ABD | 2023 | 0 | OLUR | BELİRSİZ | 0 | %9,1 | 0 | 1 | -%9,0 | X |  |
| 30 | BIST | 2023 | 1 | OLMAZ | OLUR | 0 | %26,3 | 0 | 1 | -%5,3 |  | X |

Not: küçük örneklem (30 sayfa); tek turdan bulgu denmez, birikimli tablo ve Fisher p ile okunur. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı; sonuç yukarı yanlı okunur).
