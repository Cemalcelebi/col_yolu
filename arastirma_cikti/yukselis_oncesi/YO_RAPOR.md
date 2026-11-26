# YO RAPOR — yükseliş trendinden önce hangi bölge var: geriye bakış (ABD 2016-19) + ileriye doğru sınama (ABD 2020-22, AVR)

Sürüm YUKSELIS_ONCESI v1.0 (2026-11-26): yükselişten geriye bakış + ileriye doğru sınama (ATRP beşliği içinde); ön kayıt 6ad5cfc9baa4c02e53fd087b32dfca32b92b2d2b 2026-11-26T20:29:03+00:00; kesim feafbbc3fecbecf5236c3be1087aa5f8c49aeadd 2026-11-26T20:30:50+00:00; süre 106 sn. Evren bugün yaşayan hisseler (yukarı yanlı; Y10 ve D10 için de). KASA açılmadı (veri <= 2022-12-31). Hacim kullanılmadı.

Panel / satır dosyaları (repo dışı): /root/.kasa/ham/yukselis_oncesi; sha256: ozellik_ABD.pkl 9e470d0658ccca89…; piyasa_ABD.pkl de1cb9a2af4dd6e3…; ham_ABD.npz 41f317fbd7e89282…; ozellik_AVR.pkl daa33b4c6ba06dee…; piyasa_AVR.pkl 53b5013074841ca0…; ham_AVR.npz bf3dfcf27019a243…

## SONUÇ (OLASILIK TABLOSU)

**GENEL HÜKÜM: YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde)**

- TUTAR satırlar: yok; TUTAR + KONTROLÜ GEÇER: yok; piyasa TUTAR: yok
- En yakın üç satır (TUTAR olmayan): MIKRO|0.10, MIKRO|0.02, RS_DIP_BIR|BAYRAK

### Taban oranları (hisse-gün; 15 bar)

| hücre | hisse-gün | P(Y10) % | P(Y5) % | P(D10) % | R15 ort % | KALICI % |
|---|---|---|---|---|---|---|
| ABD|d1619 | 400337 | 15,91 | 40,05 | 13,70 | 0,91 | 9,31 |
| ABD|d2022 | 391113 | 23,47 | 45,10 | 23,39 | 0,40 | 16,56 |
| AVR|d1619 | 80675 | 9,94 | 35,31 | 8,14 | 0,74 | 3,91 |
| AVR|d2022 | 64958 | 16,59 | 40,72 | 17,62 | 0,15 | 9,00 |

### Oynaklık tuzağı: ATRP20 beşliklerine göre P(Y10) / P(D10) %

| hücre | B1 Y10 / D10 | B2 Y10 / D10 | B3 Y10 / D10 | B4 Y10 / D10 | B5 Y10 / D10 |
|---|---|---|---|---|---|
| ABD|d1619 | 3,4 / 4,2 | 8,6 / 8,4 | 14,2 / 11,9 | 22,2 / 17,0 | 31,1 / 26,9 |
| ABD|d2022 | 3,9 / 9,3 | 8,3 / 13,9 | 14,5 / 16,4 | 22,1 / 20,7 | 31,7 / 30,0 |
| AVR|d1619 | 2,3 / 3,4 | 4,9 / 5,6 | 7,8 / 7,2 | 12,2 / 10,0 | 22,5 / 14,5 |
| AVR|d2022 | 2,7 / 5,9 | 5,4 / 9,8 | 7,6 / 12,1 | 11,8 / 16,1 | 24,6 / 22,6 |

### Hisse satırları (keşif yönü ve kesimi; ATRP beşliği içinde KAT; ASİMETRİ ve TOPLAM FARK puan)

| satır | yön | KEŞİF n | KEŞİF KAT ham | KEŞİF KAT [%95] | 20-22 n | 20-22 P(Y10) uç % | 20-22 KAT ham | 20-22 KAT [%95] | 20-22 ASİMETRİ [%95] | 20-22 TOPLAM FARK [%95] | AVR yönü 16-19/20-22 | BH q | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MIKRO|0.10 | KÜÇÜK | 73901 | 1,27 | 1,07 [1,03; 1,11] | 84717 | 26,3 | 1,12 | 1,04 [1,00; 1,07] | 2,02 [0,25; 3,80] | 1,15 [-0,54; 2,80] | +/+ | 0,181 | TUTMADI |
| MIKRO|0.02 | KÜÇÜK | 20764 | 1,37 | 1,08 [1,03; 1,14] | 24284 | 27,1 | 1,15 | 1,05 [1,00; 1,10] | 2,38 [-0,43; 5,22] | 1,79 [0,11; 3,54] | +/+ | 0,249 | YALNIZ OYNAKLIK |
| RS_UZAK|0.10 | KÜÇÜK | 40034 | 1,80 | 1,04 [1,00; 1,08] | 88880 | 30,6 | 1,30 | 1,03 [1,00; 1,07] | -0,52 [-2,65; 1,70] | 1,41 [-0,90; 3,71] | +/+ | 0,249 | YALNIZ OYNAKLIK |
| RS_UZAK|0.02 | KÜÇÜK | 8007 | 2,00 | 1,04 [0,98; 1,11] | 26993 | 31,8 | 1,36 | 1,01 [0,96; 1,07] | -3,87 [-7,21; -0,25] | 2,67 [-0,54; 6,03] | +/+ | 0,651 | YALNIZ OYNAKLIK |
| RS_DIP_BIR|BAYRAK | KÜÇÜK | 389132 | 0,99 | 1,00 [0,99; 1,00] | 374463 | 23,5 | 1,00 | 1,00 [0,99; 1,01] | 0,01 [-0,28; 0,26] | -0,01 [-1,65; 1,60] | +/~ | 0,753 | TUTMADI |
| GEN50|0.10 | BÜYÜK | 40248 | 0,86 | 0,90 [0,66; 1,10] | 54732 | 27,0 | 1,15 | 1,11 [0,82; 1,33] | 5,08 [-10,65; 17,41] | 1,56 [-2,80; 5,00] | ~/~ | 0,520 | ÖLÇÜLEMEDİ |
| GEN50|0.02 | BÜYÜK | 9506 | 0,61 | 0,60 [0,38; 0,88] | 7271 | 32,8 | 1,40 | 1,26 [0,95; 1,56] | 3,98 [-5,64; 21,12] | -1,09 [-3,47; 7,95] | ~/~ | 0,249 | ÖLÇÜLEMEDİ |
| GEN50_D10|0.10 | KÜÇÜK | 40360 | 1,10 | 0,98 [0,76; 1,23] | 57201 | 22,4 | 0,95 | 0,93 [0,79; 1,12] | -4,51 [-14,55; 6,21] | -2,30 [-5,82; 0,94] | +/- | 0,897 | TUTMADI |
| GEN50_D10|0.02 | KÜÇÜK | 8755 | 1,16 | 0,95 [0,66; 1,25] | 15280 | 17,8 | 0,76 | 0,75 [0,34; 1,05] | -18,55 [-60,71; 6,56] | -10,30 [-25,51; -0,02] | ~/- | 0,966 | ÖLÇÜLEMEDİ |
| OYN_SIRA|0.10 | BÜYÜK | 40034 | 1,91 | 1,02 [0,97; 1,07] | 39159 | 30,6 | 1,31 | 0,97 [0,92; 1,03] | -6,27 [-9,36; -2,92] | 0,73 [-2,32; 4,16] | +/~ | 0,897 | YALNIZ OYNAKLIK |
| OYN_SIRA|0.02 | BÜYÜK | 8007 | 1,92 | 0,99 [0,93; 1,06] | 7861 | 29,0 | 1,24 | 0,92 [0,85; 0,99] | -8,48 [-12,75; -3,94] | 1,62 [-1,75; 5,44] | ~/~ | 0,983 | YALNIZ OYNAKLIK |
| MA_KOD|BAYRAK | KÜÇÜK | 84056 | 1,40 | 1,08 [1,01; 1,15] | 105058 | 27,6 | 1,18 | 1,03 [0,94; 1,11] | 0,82 [-3,80; 4,85] | 0,98 [-1,17; 2,95] | ~/+ | 0,561 | YALNIZ OYNAKLIK |
| MA_EGIM_DEG|0.10 | KÜÇÜK | 40034 | 1,68 | 1,07 [0,99; 1,15] | 69841 | 29,2 | 1,24 | 1,01 [0,93; 1,09] | -0,39 [-5,40; 5,02] | 0,89 [-1,42; 3,16] | +/~ | 0,714 | YALNIZ OYNAKLIK |
| MA_EGIM_DEG|0.02 | KÜÇÜK | 8007 | 2,01 | 1,08 [0,99; 1,16] | 23064 | 31,7 | 1,35 | 1,01 [0,91; 1,11] | -1,09 [-8,13; 5,94] | 2,26 [-1,47; 5,79] | +/+ | 0,714 | YALNIZ OYNAKLIK |
| ZIRVE_BAR|0.10 | BÜYÜK | 40122 | 1,47 | 1,15 [1,10; 1,21] | 37353 | 28,7 | 1,23 | 1,05 [0,96; 1,15] | 0,45 [-4,26; 5,12] | 1,22 [-1,26; 3,42] | +/+ | 0,440 | YALNIZ OYNAKLIK |
| ZIRVE_BAR|0.02 | BÜYÜK | 8678 | 1,53 | 1,19 [1,06; 1,33] | 8431 | 30,2 | 1,29 | 1,08 [0,94; 1,26] | 1,39 [-5,51; 9,13] | 1,28 [-1,85; 4,11] | +/+ | 0,453 | YALNIZ OYNAKLIK |
| ZIRVE_DUSUS|0.10 | KÜÇÜK | 39097 | 2,05 | 1,13 [1,09; 1,17] | 87496 | 31,9 | 1,37 | 1,03 [0,99; 1,07] | -1,66 [-4,28; 0,95] | 1,16 [-1,52; 3,85] | +/+ | 0,258 | YALNIZ OYNAKLIK |
| ZIRVE_DUSUS|0.02 | KÜÇÜK | 7820 | 2,12 | 1,08 [1,01; 1,16] | 32004 | 31,3 | 1,34 | 0,98 [0,92; 1,05] | -5,45 [-9,14; -1,48] | 1,50 [-1,87; 4,98] | +/+ | 0,897 | YALNIZ OYNAKLIK |
| DIP_BAR|0.10 | BÜYÜK | 39191 | 1,09 | 1,06 [0,98; 1,14] | 41885 | 25,2 | 1,08 | 1,09 [0,95; 1,22] | 4,75 [-1,90; 10,32] | 1,40 [-1,62; 3,71] | +/+ | 0,362 | TUTMADI |
| DIP_BAR|0.02 | BÜYÜK | 7919 | 1,40 | 1,35 [1,08; 1,63] | 11771 | 27,2 | 1,17 | 1,19 [0,95; 1,51] | 14,15 [3,46; 21,63] | 3,58 [0,82; 4,49] | +/+ | 0,258 | TUTMADI |
| DIP_HIZ|0.10 | KÜÇÜK | 74702 | 0,87 | 0,98 [0,90; 1,07] | 68150 | 21,0 | 0,90 | 0,97 [0,91; 1,03] | -0,13 [-2,95; 2,89] | -0,25 [-2,54; 1,58] | ~/- | 0,897 | TUTMADI |
| DIP_HIZ|0.02 | KÜÇÜK | 74702 | 0,87 | 0,98 [0,90; 1,07] | 68150 | 21,0 | 0,90 | 0,97 [0,91; 1,03] | -0,13 [-2,91; 2,81] | -0,25 [-2,58; 1,57] | ~/- | 0,897 | TUTMADI |
| CLV10|0.10 | KÜÇÜK | 40034 | 1,35 | 1,16 [1,04; 1,30] | 42327 | 25,4 | 1,08 | 1,03 [0,95; 1,10] | 1,34 [-2,46; 5,13] | 0,52 [-1,76; 2,74] | ~/~ | 0,561 | TUTMADI |
| CLV10|0.02 | KÜÇÜK | 8007 | 1,67 | 1,35 [1,01; 1,69] | 7225 | 26,2 | 1,12 | 1,05 [0,93; 1,18] | 1,44 [-4,74; 7,10] | 0,84 [-1,78; 3,43] | ~/~ | 0,561 | TUTMADI |
| CLV_FARK|0.10 | KÜÇÜK | 40034 | 1,17 | 1,14 [1,00; 1,30] | 34618 | 22,7 | 0,97 | 0,97 [0,90; 1,05] | -1,21 [-5,28; 3,17] | -0,68 [-2,92; 1,58] | ~/- | 0,897 | TUTMADI |
| CLV_FARK|0.02 | KÜÇÜK | 8007 | 1,34 | 1,29 [0,97; 1,64] | 5946 | 22,1 | 0,94 | 0,96 [0,83; 1,10] | -2,37 [-8,33; 4,03] | -1,35 [-3,96; 1,38] | ~/- | 0,897 | TUTMADI |
| YUKSELEN_DIP|0.10 | KÜÇÜK | 183122 | 1,09 | 1,03 [1,00; 1,06] | 185907 | 24,3 | 1,04 | 1,01 [0,98; 1,04] | 0,05 [-1,68; 1,84] | 0,10 [-1,47; 1,66] | +/~ | 0,651 | YALNIZ OYNAKLIK |
| YUKSELEN_DIP|0.02 | KÜÇÜK | 183122 | 1,09 | 1,03 [1,00; 1,06] | 185907 | 24,3 | 1,04 | 1,01 [0,98; 1,04] | 0,05 [-1,70; 1,81] | 0,10 [-1,51; 1,69] | +/~ | 0,651 | YALNIZ OYNAKLIK |
| MOM_12_1|0.10 | BÜYÜK | 39068 | 1,49 | 1,06 [0,99; 1,14] | 73784 | 24,6 | 1,05 | 0,96 [0,88; 1,06] | -1,23 [-5,89; 3,43] | -0,38 [-1,89; 1,35] | ~/~ | 0,897 | TUTMADI |
| MOM_12_1|0.02 | BÜYÜK | 7814 | 1,94 | 1,07 [0,99; 1,15] | 26441 | 29,2 | 1,25 | 0,97 [0,88; 1,07] | -3,60 [-9,16; 2,33] | -0,67 [-2,83; 2,00] | ~/+ | 0,897 | YALNIZ OYNAKLIK |
| F15|0.10 | KÜÇÜK | 40034 | 1,79 | 1,07 [0,99; 1,17] | 71924 | 29,2 | 1,24 | 0,99 [0,94; 1,03] | -1,22 [-4,25; 2,35] | 0,55 [-1,65; 2,76] | +/~ | 0,897 | YALNIZ OYNAKLIK |
| F15|0.02 | KÜÇÜK | 8007 | 2,07 | 1,07 [0,94; 1,23] | 23798 | 32,1 | 1,37 | 1,02 [0,95; 1,09] | -0,85 [-5,24; 3,50] | 2,46 [-0,75; 4,89] | +/~ | 0,651 | YALNIZ OYNAKLIK |
| KONUM120|0.10 | KÜÇÜK | 39820 | 1,59 | 1,12 [1,05; 1,19] | 55033 | 27,5 | 1,17 | 1,00 [0,91; 1,08] | -0,89 [-5,10; 3,35] | 0,85 [-1,67; 3,24] | +/~ | 0,768 | YALNIZ OYNAKLIK |
| KONUM120|0.02 | KÜÇÜK | 12131 | 1,68 | 1,18 [0,97; 1,33] | 17495 | 27,8 | 1,19 | 1,01 [0,92; 1,11] | 1,00 [-4,07; 6,23] | 1,74 [-2,42; 4,89] | +/~ | 0,714 | YALNIZ OYNAKLIK |
| ATRP20|0.10 | BÜYÜK | 40034 | 2,04 | 1,04 [1,02; 1,07] | 129756 | 33,0 | 1,41 | 1,04 [1,02; 1,06] | -0,32 [-2,10; 1,40] | 1,35 [-1,12; 3,64] | +/+ | 0,020 | YALNIZ OYNAKLIK |
| ATRP20|0.02 | BÜYÜK | 8007 | 1,97 | 1,01 [0,95; 1,08] | 48003 | 33,7 | 1,44 | 1,06 [0,99; 1,13] | 0,29 [-5,49; 5,47] | 3,31 [-0,34; 6,58] | +/+ | 0,258 | YALNIZ OYNAKLIK |
| BOY_YUZDE_ORAN|0.10 | KÜÇÜK | 39739 | 0,84 | 1,11 [1,02; 1,22] | 45559 | 19,9 | 0,85 | 1,01 [0,90; 1,16] | -2,31 [-7,63; 3,70] | -0,73 [-2,34; 1,21] | ~/- | 0,714 | TUTMADI |
| BOY_YUZDE_ORAN|0.02 | KÜÇÜK | 7948 | 0,79 | 1,08 [0,94; 1,24] | 12846 | 17,6 | 0,75 | 0,92 [0,79; 1,18] | -5,80 [-12,49; 2,44] | -1,20 [-2,46; 1,11] | ~/~ | 0,897 | TUTMADI |
| ONCEKI_DUSUS|0.10 | KÜÇÜK | 40034 | 1,99 | 1,08 [1,04; 1,12] | 103436 | 32,7 | 1,39 | 1,05 [1,00; 1,09] | -0,40 [-3,67; 2,46] | 1,43 [-1,18; 3,86] | +/+ | 0,181 | YALNIZ OYNAKLIK |
| ONCEKI_DUSUS|0.02 | KÜÇÜK | 8007 | 2,04 | 1,05 [0,98; 1,12] | 38787 | 34,0 | 1,45 | 1,07 [1,01; 1,13] | 0,17 [-4,93; 4,58] | 3,25 [-0,62; 6,63] | +/+ | 0,181 | YALNIZ OYNAKLIK |

- KEŞİF ASİMETRİ / TOPLAM FARK, AVR sayıları, KAT_PUAN (kontrol puanı beşliği içinde KAT), Y5 / KALICI / SEÇİM: yo_ozet.csv.

### BİRLEŞİM ve BASİT PUAN

- Birleşim kurulmadı (keşif adayları: yok).
- BASİT PUAN uç 0.10: keşif KAT 1,13 [1,08; 1,18]; 20-22 n 66609, KAT ham 1,35, KAT 1,00 [0,94; 1,06], ASİMETRİ -2,86 [-6,35; 0,30], TOPLAM FARK 0,68 [-2,06; 3,31]; hüküm YALNIZ OYNAKLIK; en iyi tek (GEN50|0.10) KAT 1,11 -> GEÇMEDİ (seçilmez)
- BASİT PUAN uç 0.02: keşif KAT 1,20 [1,02; 1,38]; 20-22 n 20579, KAT ham 1,39, KAT 1,03 [0,95; 1,11], ASİMETRİ -1,07 [-6,12; 3,68], TOPLAM FARK 2,73 [-0,96; 5,97]; hüküm YALNIZ OYNAKLIK; en iyi tek (GEN50|0.02) KAT 1,26 -> GEÇMEDİ (seçilmez)

### PİYASA TAHMİNİ (pazar-gün; YP = P15 >= +%5, DP = P15 <= -%5)

| hücre | gün | P(YP) % | P(DP) % | P15 ort % |
|---|---|---|---|---|
| ABD|d1619 | 1006 | 8,35 | 5,37 | 0,91 |
| ABD|d2022 | 742 | 25,07 | 17,65 | 0,48 |
| AVR|d1619 | 1024 | 4,20 | 3,91 | 0,71 |
| AVR|d2022 | 759 | 11,07 | 10,94 | 0,20 |

| satır | yön | KEŞİF n gün | KEŞİF P(YP) / P(DP) uç % | KEŞİF P15 farkı [%95] | 20-22 n | 20-22 P(YP) / P(DP) uç % | 20-22 KAT [%95] | 20-22 P15 farkı [%95] | AVR | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN20|0.10 | KÜÇÜK | 101 | 22,8 / 8,9 | 1,35 [-0,19; 3,72] | 125 | 31,2 / 25,6 | 1,24 [0,76; 1,92] | -0,43 [-2,46; 1,91] | +/~ | TUTMADI |
| GEN20|0.02 | KÜÇÜK | 21 | 28,6 / 0,0 | 2,16 [-2,08; 7,70] | 34 | 29,4 / 32,4 | 1,17 [0,00; 2,37] | -1,55 [-4,84; 2,67] | +/~ | ÖLÇÜLEMEDİ |
| GEN50|0.10 | KÜÇÜK | 101 | 27,7 / 7,9 | 1,49 [-0,66; 4,62] | 142 | 38,7 / 17,6 | 1,55 [1,00; 2,30] | 1,34 [-1,12; 3,67] | +/+ | TUTMADI |
| GEN50|0.02 | KÜÇÜK | 21 | 33,3 / 0,0 | 2,52 [-1,62; 9,91] | 39 | 48,7 / 15,4 | 1,94 [0,00; 3,27] | 4,09 [-1,11; 8,48] | +/+ | ÖLÇÜLEMEDİ |
| GEN200|0.10 | KÜÇÜK | 101 | 37,6 / 12,9 | 1,28 [-2,55; 4,50] | 254 | 35,8 / 23,2 | 1,43 [0,90; 2,06] | 1,06 [-1,21; 3,31] | +/+ | ÖLÇÜLEMEDİ |
| GEN200|0.02 | KÜÇÜK | 21 | 66,7 / 0,0 | 6,07 [-0,90; 10,56] | 53 | 58,5 / 5,7 | 2,33 [0,89; 3,68] | 6,15 [2,46; 8,53] | +/+ | ÖLÇÜLEMEDİ |
| GEN20_D5|0.10 | BÜYÜK | 101 | 13,9 / 4,0 | 0,13 [-1,19; 1,23] | 97 | 26,8 / 15,5 | 1,07 [0,47; 1,65] | 0,77 [-1,32; 2,87] | ~/+ | TUTMADI |
| GEN20_D5|0.02 | BÜYÜK | 21 | 19,0 / 0,0 | 1,65 [-0,69; 3,19] | 20 | 25,0 / 25,0 | 1,00 [0,00; 2,07] | -0,02 [-3,72; 3,52] | ~/+ | ÖLÇÜLEMEDİ |
| GEN20_D10|0.10 | BÜYÜK | 101 | 11,9 / 5,0 | 0,75 [-0,54; 1,84] | 93 | 32,3 / 23,7 | 1,29 [0,51; 2,02] | -0,30 [-3,31; 2,34] | ~/~ | TUTMADI |
| GEN20_D10|0.02 | BÜYÜK | 21 | 23,8 / 0,0 | 1,40 [-1,56; 3,03] | 27 | 48,1 / 29,6 | 1,92 [0,29; 3,23] | 1,82 [-5,31; 6,39] | ~/+ | ÖLÇÜLEMEDİ |
| GEN50_D5|0.10 | BÜYÜK | 101 | 16,8 / 7,9 | -0,06 [-1,60; 1,27] | 99 | 26,3 / 17,2 | 1,05 [0,39; 1,55] | 0,42 [-1,62; 2,33] | ~/+ | TUTMADI |
| GEN50_D5|0.02 | BÜYÜK | 21 | 28,6 / 4,8 | 2,15 [0,11; 3,97] | 28 | 32,1 / 25,0 | 1,28 [0,00; 2,30] | 0,62 [-2,96; 3,84] | +/+ | ÖLÇÜLEMEDİ |
| GEN50_D10|0.10 | BÜYÜK | 101 | 19,8 / 6,9 | 0,89 [-1,01; 2,24] | 93 | 37,6 / 16,1 | 1,50 [0,52; 2,37] | 1,41 [-1,82; 4,25] | ~/+ | TUTMADI |
| GEN50_D10|0.02 | BÜYÜK | 21 | 28,6 / 14,3 | 1,29 [-2,28; 4,08] | 20 | 50,0 / 15,0 | 1,99 [0,00; 3,48] | 3,11 [-1,67; 6,65] | ~/+ | ÖLÇÜLEMEDİ |
| GEN200_D5|0.10 | KÜÇÜK | 101 | 23,8 / 7,9 | 1,22 [-0,08; 2,59] | 101 | 22,8 / 29,7 | 0,91 [0,49; 1,48] | -2,06 [-5,04; 0,86] | +/~ | TUTMADI |
| GEN200_D5|0.02 | KÜÇÜK | 21 | 14,3 / 9,5 | -0,12 [-2,18; 2,80] | 25 | 24,0 / 40,0 | 0,96 [0,42; 1,79] | -6,81 [-13,87; 3,96] | +/~ | ÖLÇÜLEMEDİ |
| GEN200_D10|0.10 | KÜÇÜK | 101 | 20,8 / 5,0 | 1,20 [-0,61; 3,45] | 106 | 21,7 / 25,5 | 0,87 [0,48; 1,32] | -1,39 [-3,76; 0,93] | +/~ | TUTMADI |
| GEN200_D10|0.02 | KÜÇÜK | 21 | 9,5 / 0,0 | 0,99 [-1,31; 4,73] | 31 | 22,6 / 48,4 | 0,90 [0,00; 1,58] | -7,07 [-15,21; 0,90] | ~/~ | ÖLÇÜLEMEDİ |
| PAZ_R20|0.10 | KÜÇÜK | 101 | 29,7 / 5,9 | 1,89 [0,35; 3,72] | 164 | 28,7 / 24,4 | 1,14 [0,69; 1,75] | -0,41 [-2,32; 1,69] | +/+ | TEK DÖNEM |
| PAZ_R20|0.02 | KÜÇÜK | 21 | 38,1 / 0,0 | 3,34 [-1,14; 10,20] | 64 | 43,8 / 18,8 | 1,75 [0,93; 2,77] | 2,95 [0,64; 6,39] | +/+ | ÖLÇÜLEMEDİ |
| PAZ_R60|0.10 | KÜÇÜK | 101 | 32,7 / 12,9 | 0,65 [-2,21; 4,05] | 214 | 37,9 / 16,8 | 1,51 [0,99; 2,15] | 1,96 [0,03; 3,95] | +/+ | ÖLÇÜLEMEDİ |
| PAZ_R60|0.02 | KÜÇÜK | 21 | 76,2 / 0,0 | 6,94 [-3,19; 8,90] | 97 | 59,8 / 7,2 | 2,39 [1,56; 3,69] | 5,72 [2,42; 8,76] | +/+ | ÖLÇÜLEMEDİ |
| PAZ_DD60|0.10 | KÜÇÜK | 101 | 31,7 / 11,9 | 0,90 [-1,85; 4,33] | 269 | 34,9 / 21,6 | 1,39 [0,94; 2,00] | 0,85 [-0,91; 2,74] | +/+ | TUTMADI |
| PAZ_DD60|0.02 | KÜÇÜK | 21 | 71,4 / 0,0 | 6,61 [-1,45; 11,49] | 112 | 54,5 / 6,2 | 2,17 [1,52; 3,18] | 5,27 [3,03; 7,54] | +/+ | ÖLÇÜLEMEDİ |
| DIP20_PAY|0.10 | BÜYÜK | 101 | 22,8 / 13,9 | 0,73 [-0,68; 2,70] | 123 | 25,2 / 25,2 | 1,01 [0,65; 1,51] | -0,78 [-2,72; 1,07] | +/~ | TUTMADI |
| DIP20_PAY|0.02 | BÜYÜK | 21 | 38,1 / 0,0 | 2,61 [-0,87; 6,30] | 31 | 25,8 / 38,7 | 1,03 [0,31; 2,12] | -3,71 [-10,25; 3,48] | +/~ | ÖLÇÜLEMEDİ |
| YENI_ZD|0.10 | KÜÇÜK | 101 | 22,8 / 12,9 | 0,83 [-0,64; 3,10] | 114 | 30,7 / 25,4 | 1,22 [0,74; 1,87] | -0,53 [-2,93; 1,64] | +/~ | TUTMADI |
| YENI_ZD|0.02 | KÜÇÜK | 21 | 28,6 / 0,0 | 2,24 [-1,16; 6,66] | 29 | 34,5 / 31,0 | 1,38 [0,32; 2,64] | -2,38 [-10,46; 3,79] | +/~ | ÖLÇÜLEMEDİ |
| KESIT_SD|0.10 | BÜYÜK | 101 | 7,9 / 5,9 | 0,25 [-0,88; 1,36] | 558 | 27,6 / 14,9 | 1,10 [0,97; 1,26] | 0,60 [-0,20; 1,59] | +/+ | TUTMADI |
| KESIT_SD|0.02 | BÜYÜK | 21 | 0,0 / 9,5 | -1,13 [-4,67; 0,66] | 349 | 34,4 / 12,6 | 1,37 [1,06; 1,74] | 1,40 [-0,05; 3,00] | +/+ | ÖLÇÜLEMEDİ |
| ATRP_MED_SIRA|0.10 | BÜYÜK | 103 | 21,4 / 4,9 | 1,26 [-0,99; 3,58] | 68 | 39,7 / 29,4 | 1,58 [0,70; 2,57] | -0,70 [-6,63; 4,30] | +/~ | ÖLÇÜLEMEDİ |
| ATRP_MED_SIRA|0.02 | BÜYÜK | 26 | 11,5 / 0,0 | 0,67 [-2,59; 7,41] | 19 | 42,1 / 52,6 | 1,68 [0,00; 3,02] | -3,52 [-28,96; 4,39] | ~/~ | ÖLÇÜLEMEDİ |

## ADIM 1 (yalnız keşif): yükselişten önce en çok ayrışan özellikler

| sıra | özellik | yön | SMD [%95] | eşli AUC [%95] |
|---|---|---|---|---|
| 1 | ZIRVE_DUSUS | KÜÇÜK | -0,115 [-0,152; -0,077] | 0,458 [0,443; 0,474] |
| 2 | OYN_SIRA | BÜYÜK | 0,094 [0,078; 0,110] | 0,548 [0,540; 0,556] |
| 3 | ZIRVE_BAR | BÜYÜK | 0,085 [0,047; 0,123] | 0,526 [0,514; 0,537] |
| 4 | BOY_YUZDE_ORAN | KÜÇÜK | -0,069 [-0,093; -0,048] | 0,465 [0,456; 0,473] |
| 5 | ONCEKI_DUSUS | KÜÇÜK | -0,057 [-0,084; -0,031] | 0,471 [0,459; 0,483] |
| 6 | MA_KOD | KÜÇÜK | -0,056 [-0,100; -0,010] | 0,483 [0,471; 0,497] |
| 7 | KONUM120 | KÜÇÜK | -0,052 [-0,100; -0,004] | 0,481 [0,465; 0,497] |
| 8 | RS_UZAK | KÜÇÜK | -0,045 [-0,076; -0,014] | 0,480 [0,469; 0,492] |
| 9 | MIKRO | KÜÇÜK | -0,045 [-0,069; -0,020] | 0,487 [0,481; 0,494] |
| 10 | DIP_BAR | BÜYÜK | 0,037 [0,009; 0,063] | 0,509 [0,501; 0,518] |
| 11 | CLV10 | KÜÇÜK | -0,030 [-0,052; -0,006] | 0,489 [0,480; 0,497] |
| 12 | F15 | KÜÇÜK | -0,017 [-0,045; 0,011] | 0,488 [0,476; 0,501] |
| 13 | MA_EGIM_DEG | KÜÇÜK | -0,016 [-0,035; 0,004] | 0,493 [0,484; 0,502] |
| 14 | RS_DIP_BIR | KÜÇÜK | -0,016 [-0,037; 0,008] | 0,499 [0,496; 0,501] |
| 15 | YUKSELEN_DIP | KÜÇÜK | -0,015 [-0,037; 0,007] | 0,494 [0,488; 0,501] |
| 16 | CLV_FARK | KÜÇÜK | -0,012 [-0,029; 0,006] | 0,496 [0,490; 0,502] |
| 17 | DIP_HIZ | KÜÇÜK | -0,007 [-0,021; 0,009] | 0,498 [0,493; 0,505] |
| 18 | ATRP20 | BÜYÜK | 0,005 [-0,012; 0,023] | 0,541 [0,536; 0,547] |
| 19 | MOM_12_1 | BÜYÜK | 0,003 [-0,022; 0,023] | 0,482 [0,468; 0,497] |
| 20 | GEN50 | BÜYÜK | 0,001 [-0,001; 0,003] | 0,500 [0,500; 0,500] |
| 21 | GEN50_D10 | KÜÇÜK | -0,001 [-0,002; 0,000] | 0,500 [0,500; 0,500] |

## OKUMA (sayı ile yorum ayrı)

- Taban: 15 günde +%10 (önce -%5 görmeden) ABD 2016-19'da hisse-günlerin %15,9'unda, 2020-22'de %23,5'inde; ayna D10 %13,7 / %23,4. ATRP20 beşliğinde 1'den 5'e P(Y10) %3,4 -> %31,1 (keşif): 9 kat. OYNAKLIK TUZAĞI büyük: ham KAT'ların çoğu (1,2-2,1) bu yüzden.
- Yorum: ATRP beşliği içinde okununca 21 sütunun hiçbiri iki dönemde üç şartı (KAT, ASİMETRİ, TOPLAM FARK alt uçları) birlikte geçmedi. 'Yükselişten önce' en çok ayrışanlar (zirveden derin düşüş, yüksek oynaklık sırası, zirveden uzun süre) ileriye doğru ya aynı oynaklık beşliğindeki hisselerden ayrışmadı ya da D10'u da aynı ölçüde artırdı (ASİMETRİ ~0): YALNIZ OYNAKLIK.
- Keşifte iyi görünüp doğrulamada tutmayanlar: CLV10 düşük uç (KAT 1,16 -> 1,03), BOY_YUZDE_ORAN küçük uç (1,11 -> 1,01), ZIRVE_BAR (1,15 -> 1,05), KONUM120 (1,12 -> 1,00): 'tutmadı'.
- Piyasa: keşifte P(YP) %8,4; genişlik düşükken / pazar 60 günde düşmüşken YP sıklığı uçta 3-4 kat (GEN200 düşük uç %37,6), ama P15 farkının aralığı iki dönemde sıfırı içeriyor; uç %2 satırlarında n < 30 gün. Hiçbir piyasa satırı TUTAR değil (yalnız PAZ_R20 düşük uç keşifte P15 farkı > 0: TEK DÖNEM).
- Evren bugün yaşayan hisseler: Y10 ve D10 yukarı yanlı; fark ölçüleri aynı evrende kurulduğu için yanlılık kısmen düşer, kalkmaz.

## KONTROL LİSTESİ

Ön kayıttaki 14 madde (YO_ON_KAYIT.md) aynen geçerli; ADIM 1 ve ADIM 2 kapıları geçti (ik_kontrol_kapisi + kod / eşik / panel / sayım sha + ön kayıt commit + temiz ağaç + KASA 2022-12-31; ADIM 2'de ayrıca yo_kesim.json / YO_KESIM.md commit + kesim sha). Keşif satırları ADIM 2'de ADIM 1 ile birebir aynı üretildi (kod denetimi, DUR yok).

## YENİDEN ÜRETİM (bağımsız kısa kod; satir_ABD.pkl / satir_AVR.pkl / piyasa_satir_ABD.pkl + yo_kesim.json; YUKSELIS_ONCESI fonksiyonları kullanılmadı)

- ZIRVE_DUSUS uç %10, ABD 2020-22: n 87.496, KAT ham 1,369179, KAT 1,030315, ASİMETRİ -0,016619, TOPLAM FARK 0,011556 = json (birebir).
- MIKRO uç %10, AVR 2016-19: n 15.902, KAT 1,031924, ASİMETRİ 0,006445, TOPLAM FARK 0,002446 = json.
- ONCEKI_DUSUS uç %2, ABD 2020-22: n 38.787, KAT 1,074246 = json. Piyasa GEN200 uç %10, ABD 2020-22: 254 gün, KAT 1,429219, P15 farkı 0,010569 = json. Taban P(Y10) ABD 2020-22 0,234664 = json.
- Ham veriden (MI.mi_veri) rastgele 6 hisse-günün Y10 / D10 / R15'i döngüyle: 6 / 6 aynı.

## HATA

- (yok) Ölçümü etkileyen hata bulunmadı. Test aşamasında yakalanan test-kurgu hataları (kodda değil): elle örnekte 100 x 1,10 kayan noktada 110,00000000000001 (GZ ile aynı formül; sınırda 'tam 110' dokunmaz); linspace sınırında eşit iki değerde 'son görülen bar' kuralı; çakışma kapısının aynı ad alanında ikinci exec'i durdurması (tasarım gereği).

## SAPMA

- Gösterim (hesap değil): ADIM 2'den sonra yalnız yo_png değişti (eksen yerleşimi, lejant yeri, satır etiketine '[yüksek / düşük uç]' eki; KÜÇÜK yönlü satırların etiketi yanlış okunmasın diye). Kod sha'sı ön kayıttaki 344fa104… idi, gösterim sonrası 6aa8d433…; hesap fonksiyonları ve YO_ESIK aynı (git diff: 5 satır, hepsi yo_png).
- 'En yakın üç satır' kod çıktısı (MIKRO 0.10, MIKRO 0.02, RS_DIP_BIR) alt uçların eşiğe uzaklığıyla sıralandı; RS_DIP_BIR'in yakınlığı dar aralığından (KAT 1,00) gelir, anlamlı yakınlık değildir. Raporda okuma için ayrıca 'gerçek en yakınlar' yazıldı (ÖNERİLEN DEFTER SATIRLARI).

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- Ç (YUKSELIS_ONCESI): 'Yükseliş trendinden önce hangi bölge var' — 21 hisse sütunu (15 yeni: MIKRO, RS_DIP, GENISLIK, OYN_SIRA, MA_DIZI, DD_SURE, CLV, YUKSELEN_DIP + 6 kontrol) ve 16 piyasa sütunu; keşif ABD 2016-19 (400.337 hisse-gün), doğrulama ABD 2020-22 (391.113), AVR 2016-19 / 2020-22 (80.675 / 64.958); ATRP beşliği içinde. HÜKÜM: YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde); güç yeterli (uç n 5.946-389.132, 36-48 ay; ÖLÇÜLEMEDİ 3 satır: genişlik satırlarında farklı ay < 12) -> İZ DEĞİL sınıfı; 40 hisse satırından 23 YALNIZ OYNAKLIK, 14 TUTMADI, 3 ÖLÇÜLEMEDİ, 0 TUTAR; birleşim kurulmadı (keşifte aday yok); basit L1 puan 2020-22'de KAT 1,00 (YALNIZ OYNAKLIK). Piyasa (32 satır): 0 TUTAR, 1 TEK DÖNEM (PAZ_R20 düşük uç), 12 TUTMADI, 19 ÖLÇÜLEMEDİ (uç gün < 30 ya da ay < 12).
- En yakın (okuma): MIKRO düşük uç (az yükselen-kapanış serisi; KAT 1,07 / 1,04, alt uçlar >= 1,00; ASİMETRİ 2020-22 +2,0 puan [0,3; 3,8]; TOPLAM FARK aralığı sıfırı içeriyor; BH q 0,18; AVR +/+), DIP_BAR yüksek uç %2 (KAT 1,35 / 1,19 [0,95; 1,51]; ASİMETRİ 2020-22 +14,2 puan [3,5; 21,6]; TOPLAM FARK +3,6 [0,8; 4,5]; keşif ASİMETRİ aralığı sıfırı içeriyor), ONCEKI_DUSUS derin uç %2 (KAT 1,05 / 1,07 [1,01; 1,13], ASİMETRİ ~0: YALNIZ OYNAKLIK).
- İleri test (IK_ILERI önerisi): aynı komut, aynı kesim dosyasıyla 2023-24 verisi (kasa) — yalnız ana model kararıyla; şimdilik kapalı.
- IK_HATA önerisi: yok.
