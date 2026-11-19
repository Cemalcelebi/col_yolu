# TUR DEFTERİ — hakem turları (Cemal vs model; CLAUDE.md 'Hakem turları')

## TUR 1 (2026-11-18 10:53:17 UTC)

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

## TUR 2 (2026-11-18 12:50:38 UTC)

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

## AÇILIŞ — TUR 4 / 5 (T1.6) (2026-11-19 07:15:21 UTC)

- Sürüm T1.6 (TUR4_IS_TANIMI.md; ön kayıtlı, sonuç görülmeden); tohum 104 (tek permütasyon, kotasız); tur eşik sha 7ed7753fc514.
- Havuz (U dip = Y1 olayı ∧ Ş1 dipte ∧ Ş9 U dip; Ş2 şart değil; dönem 2016-22 / 2023 / 2024-26): kriz süzgecinden önce 117; giriş <= kriz - 30 gün sonrası 115 (ABD 2016-22 31, ABD 2023 3, ABD 2024-26 20, AVR 2016-22 11, AVR 2023 2, AVR 2024-26 2, BIST 2016-22 16, BIST 2023 2, BIST 2024-26 28); kriz süzgecinde düşen 2.
- Gösterilmiş (300 + hakem + TUR 1-3 + S7 PDF 50; olay ve hisse) çıkan 26; kalan 89 (ABD 2016-22 23, ABD 2023 3, ABD 2024-26 16, AVR 2016-22 6, AVR 2023 2, AVR 2024-26 2, BIST 2016-22 13, BIST 2023 1, BIST 2024-26 23); hisse başına en çok 2; seçilen 80.
- TUR 4: 40 sayfa (ABD 2016-22 9, ABD 2023 2, ABD 2024-26 5, AVR 2016-22 1, AVR 2023 1, AVR 2024-26 1, BIST 2016-22 8, BIST 2023 1, BIST 2024-26 12); parmak F19 (bilgi): ABD parmak=0 15, ABD parmak=1 1, AVR parmak=0 3, BIST parmak=0 19, BIST parmak=1 2; PDF 2.54 MB, sızıntı sembol 0 / tarih 0.
- TUR 5: 40 sayfa (ABD 2016-22 11, ABD 2023 1, ABD 2024-26 10, AVR 2016-22 4, BIST 2016-22 4, BIST 2024-26 10); parmak F19 (bilgi): ABD parmak=0 18, ABD parmak=1 4, AVR parmak=0 4, BIST parmak=0 11, BIST parmak=1 3; PDF 2.52 MB, sızıntı sembol 0 / tarih 0.
- TUR 4 / 5, TUR 3 ölçülmeden açılır (ana model kararı, TUR4_IS_TANIMI.md; Cemal'in 19 Kas isteği). TUR 5 PDF'i Cemal'e TUR 4 yanıtından sonra gönderilir (ana model).

## TUR 4 (2026-11-19 09:50:28 UTC)

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

## AÇILIŞ — TUR 6 (T1.7) (2026-11-19 13:37:07 UTC)

- Sürüm T1.7 (TUR6_IS_TANIMI.md; ön kayıtlı, sonuç görülmeden); tohum 106 (tek permütasyon, kotasız); tur eşik sha 57e081e8da94.
- Havuz (dip savunulmuş + alt fitil kısa + parabolik U, 120 günün alt yarısı = Y1 ∧ Ş3 ∧ Ş5 ∧ Ş9 ∧ F15 <= 0,50; Ş1 bilgi; dönem 2016-22 / 2023 / 2024-26): kriz süzgecinden önce 302; giriş <= kriz - 30 gün sonrası 297 (ABD 2016-22 62, ABD 2023 14, ABD 2024-26 38, AVR 2016-22 37, AVR 2023 10, AVR 2024-26 23, BIST 2016-22 39, BIST 2023 2, BIST 2024-26 72); kriz süzgecinde düşen 5.
- Gösterilmiş (300 + hakem + TUR 1-5 + S7 PDF 50; olay ve hisse) çıkan 130; kalan 167 (ABD 2016-22 33, ABD 2023 10, ABD 2024-26 19, AVR 2016-22 23, AVR 2023 6, AVR 2024-26 15, BIST 2016-22 21, BIST 2024-26 40); hisse başına en çok 2; seçilen 40.
- TUR 6: 40 sayfa (ABD 2016-22 6, ABD 2023 2, ABD 2024-26 3, AVR 2016-22 3, AVR 2024-26 3, BIST 2016-22 8, BIST 2024-26 15); parmak F19 (bilgi): ABD parmak=0 9, ABD parmak=1 2, AVR parmak=0 5, AVR parmak=1 1, BIST parmak=0 21, BIST parmak=1 2; PDF 2.56 MB, sızıntı sembol 0 / tarih 0.
- Ş1 dipte (bilgi, şart değil): havuzda 64; seçilen sayfalarda TUR 6 1.
- Seçilmeyen kalan havuz (sonraki turlar için saklanır; PDF yok): 127 (ABD 2016-22 27, ABD 2023 8, ABD 2024-26 16, AVR 2016-22 20, AVR 2023 6, AVR 2024-26 12, BIST 2016-22 13, BIST 2024-26 25).
- İlk sayfa üst notu: 'havuz: dip savunulmuş + alt fitil kısa + parabolik U, 120 günün alt yarısı'.
- TUR 6, TUR 5 ölçülmeden açılır (ana model kararı, TUR6_IS_TANIMI.md; Cemal'in 19 Kas isteği). Kalan havuz TUR 7+ için saklanır (PDF üretilmez).

## AÇILIŞ — TUR 7 (T1.8) (2026-11-19 13:37:39 UTC)

- Sürüm T1.8 (TUR6_IS_TANIMI.md + ana model ek iş tanımı (TUR 7, 19 Kas); ön kayıtlı, sonuç görülmeden); tohum 107 (tek permütasyon, kotasız); tur eşik sha 5da2d281d289.
- Havuz (düşüş sonrası dipte + yakın tavanı gövdeli ortalayan kırılım = Y1 ∧ Ş1 ∧ Ş7 (RAPOR_6 filtre karnesi KATKI+ iki ölçü); dönem 2016-22 / 2023 / 2024-26): kriz süzgecinden önce 765; giriş <= kriz - 30 gün sonrası 750 (ABD 2016-22 176, ABD 2023 69, ABD 2024-26 98, AVR 2016-22 52, AVR 2023 12, AVR 2024-26 32, BIST 2016-22 129, BIST 2023 40, BIST 2024-26 142); kriz süzgecinde düşen 15.
- Gösterilmiş (300 + hakem + TUR 1-6 + S7 PDF 50; olay ve hisse) çıkan 278; kalan 472 (ABD 2016-22 97, ABD 2023 50, ABD 2024-26 69, AVR 2016-22 30, AVR 2023 10, AVR 2024-26 23, BIST 2016-22 73, BIST 2023 28, BIST 2024-26 92); hisse başına en çok 2; seçilen 40.
- TUR 7: 40 sayfa (ABD 2016-22 11, ABD 2023 4, ABD 2024-26 2, AVR 2016-22 2, AVR 2024-26 5, BIST 2016-22 5, BIST 2023 2, BIST 2024-26 9); parmak F19 (bilgi): ABD parmak=0 15, ABD parmak=1 2, AVR parmak=0 6, AVR parmak=1 1, BIST parmak=0 8, BIST parmak=1 8; PDF 2.52 MB, sızıntı sembol 0 / tarih 0.
- Seçilmeyen kalan havuz (sonraki turlar için saklanır; PDF yok): 432 (ABD 2016-22 86, ABD 2023 46, ABD 2024-26 67, AVR 2016-22 28, AVR 2023 10, AVR 2024-26 18, BIST 2016-22 68, BIST 2023 26, BIST 2024-26 83).
- İlk sayfa üst notu: 'havuz: düşüş sonrası dipte + yakın tavanı gövdeli ortalayan kırılım mumu (ölçümde katkı veren iki ölçü)'.
- TUR 7, TUR 5 / 6 ölçülmeden açılır (ana model kararı; Cemal'in 19 Kas isteği 'başarılı olanları da ver').

## TUR 6 (2026-11-19 18:38:07 UTC)

| Taraf | OLUR / OLMAZ / BELİRSİZ | OLUR isabeti (+%5 gördü) | OLMAZ isabeti (+%5 görmedi) | BAŞARI | OLUR sayfalarının eş payı | taban: bütün sayfaların eş payı | hep OLMAZ deseydi | Fisher p | yanıtsız / ölçülemedi |
|---|---|---|---|---|---|---|---|---|---|
| model (bu tur) | 18 / 22 / 0 | 9 / 18 (%50,0) | 12 / 22 (%54,5) | **%52,5** (21 / 40) | %51,9 | %48,0 | %52,5 | 1,000 | 0 / 0 |
| Cemal (bu tur) | 13 / 6 / 3 | 6 / 13 (%46,2) | 3 / 6 (%50,0) | **%47,4** (9 / 19) | %48,1 | %48,0 | %52,5 | 1,000 | 18 / 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 48 / 91 / 1 | 24 / 48 (%50,0) | 49 / 91 (%53,8) | **%52,5** (73 / 139) | %47,1 | %46,6 | %52,9 | 0,722 | 0 / 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 60 / 30 / 32 | 27 / 60 (%45,0) | 15 / 30 (%50,0) | **%46,7** (42 / 90) | %44,7 | %46,6 | %52,9 | 0,662 | 18 / 0 |

- Uyum (kappa, 3 sınıf): bu tur 0,257 (n 22); birikimli 0,092 (n 122).
- Yanılınan sayfalar: model [4, 5, 7, 9, 10, 15, 16, 17, 20, 22, 23, 25, 26, 27, 29, 30, 31, 37, 40]; Cemal [4, 5, 7, 9, 27, 29, 30, 35, 38, 39].
- Cemal'in hedefi BAŞARI %80-90; taban oran ~%40 (eş payı) olduğu için bu hedef zordur (her tur raporunda yazılır).
- Bilgi sütunlarıyla yeniden koşu: 2026-11-19 18:38:40 UTC (TUTTU (önceki tur_K_sonuc.json ile karar sayıları aynı)).

Üç cetvel (bilgi; BAŞARI yalnız ilk cetvelle, değişmez):

| Taraf | Cetvel | OLUR isabeti | OLMAZ isabeti | BAŞARI | taban (sayfa payı) | hep OLMAZ deseydi | ölçülemedi |
|---|---|---|---|---|---|---|---|
| model (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 9 / 18 (%50,0) | 12 / 22 (%54,5) | **%52,5** (21 / 40) | %47,5 | %52,5 | 0 |
| model (bu tur) | 15 g gün içi +%5 (High; bilgi) | 11 / 18 (%61,1) | 8 / 22 (%36,4) | **%47,5** (19 / 40) | %62,5 | %37,5 | 0 |
| model (bu tur) | 60 g kapanış +%5 (bilgi) | 13 / 18 (%72,2) | 5 / 22 (%22,7) | **%45,0** (18 / 40) | %75,0 | %25,0 | 0 |
| Cemal (bu tur) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 6 / 13 (%46,2) | 3 / 6 (%50,0) | **%47,4** (9 / 19) | %47,5 | %52,5 | 0 |
| Cemal (bu tur) | 15 g gün içi +%5 (High; bilgi) | 8 / 13 (%61,5) | 3 / 6 (%50,0) | **%57,9** (11 / 19) | %62,5 | %37,5 | 0 |
| Cemal (bu tur) | 60 g kapanış +%5 (bilgi) | 9 / 13 (%69,2) | 1 / 6 (%16,7) | **%52,6** (10 / 19) | %75,0 | %25,0 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 24 / 48 (%50,0) | 49 / 91 (%53,8) | **%52,5** (73 / 139) | %47,1 | %52,9 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 15 g gün içi +%5 (High; bilgi) | 27 / 48 (%56,2) | 33 / 91 (%36,3) | **%43,2** (60 / 139) | %60,7 | %39,3 | 0 |
| model (birikimli, tur [1, 2, 4, 6]) | 60 g kapanış +%5 (bilgi) | 38 / 48 (%79,2) | 24 / 89 (%27,0) | **%45,3** (62 / 137) | %74,6 | %25,4 | 2 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 15 g kapanış +%5, stop'tan önce (KARAR ÖLÇÜSÜ) | 27 / 60 (%45,0) | 15 / 30 (%50,0) | **%46,7** (42 / 90) | %47,1 | %52,9 | 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 15 g gün içi +%5 (High; bilgi) | 36 / 60 (%60,0) | 12 / 30 (%40,0) | **%53,3** (48 / 90) | %60,7 | %39,3 | 0 |
| Cemal (birikimli, tur [1, 2, 4, 6]) | 60 g kapanış +%5 (bilgi) | 43 / 59 (%72,9) | 6 / 30 (%20,0) | **%55,1** (49 / 89) | %74,6 | %25,4 | 2 |
- Yön doğru / eşik kaçtı (OLUR, h5 = 0, 15 g kapanış max +%3..+%5): model [27]; Cemal [27, 39]; birikimli model 5, Cemal 8.
- Cemal'in birikimli etiketi 100'ü geçti: göz ölçümü (Ç192 planı) Cemal'in kendi etiketleriyle koşulur.
