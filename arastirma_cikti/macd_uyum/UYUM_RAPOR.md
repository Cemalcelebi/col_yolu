# MACD_UYUM — RAPOR (K47 MACD pozitif uyumsuzluk, tek başına ve DİPTE)

Koşu 2026-11-24 16:36:52 UTC; ön kayıt arastirma_cikti/macd_uyum/UYUM_ON_KAYIT.md (git 6b08d4c8aedeb67a018c262070012c0389d2c4dc 2026-11-24T19:36:46+03:00); süre 366.5 sn. Veri KASA açık kesik 2022-12-31 (satır dosyası en geç tarih 2022-12-30). Evren bugün işlem gören hisseler: batanlar yok, dipteki olaylarda sonuç YUKARI yanlıdır (K7). Komisyon / kayma yok.

## KARAR (önceden yazılı kural): **TUTMADI** — gücü yeterli hücrede U1 TUTMADI: ABD|d1619, ABD|d2022, AVR|d1619, AVR|d2022

## 1. BULGU TABLOSU (ANA: CETVEL2 v2.2 R15; FARK = R15 olay - eş ortalaması, puan)

| Hipotez | Hücre | n | R15 FARK [%95] | medyan FARK | SIRA [boot alt] | L3O | güç | plasebo FARK / + pay / - pay | HÜKÜM | gerekçe |
|---|---|---|---|---|---|---|---|---|---|---|
| U1 | ABD d1619 | 1279 | -0,39 [-1,02; +0,18] | -0,55 | 0,481 [0,457] | -0,83 | 1,00 | -0,02 / 2,5 / 4,0 | TUTMADI | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U1 | ABD d2022 | 1893 | +0,09 [-0,51; +0,74] | -0,34 | 0,501 [0,484] | -0,29 | 1,00 | +0,01 / 4,0 / 1,5 | TUTMADI | FARK boot alt <= 0; SIRA boot alt <= 0,50; L3O <= 0 |
| U1 | AVR d1619 | 631 | +0,30 [-0,27; +0,89] | +0,11 | 0,497 [0,471] | -0,14 | 1,00 | -0,00 / 4,5 / 3,0 | TUTMADI | FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U1 | AVR d2022 | 636 | +0,40 [-0,30; +1,10] | +0,33 | 0,521 [0,498] | -0,15 | 1,00 | +0,01 / 5,5 / 3,5 | TUTMADI | FARK boot alt <= 0; SIRA boot alt <= 0,50; L3O <= 0 |
| U1 | BIST d1619 | 659 | +0,28 [-0,86; +1,64] | -1,28 | 0,499 [0,470] | -0,73 | 1,00 | -0,01 / 2,0 / 4,0 | BİLGİ (TUTMADI) | FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U1 | BIST d2022 | 320 | -0,74 [-2,39; +0,47] | -1,31 | 0,483 [0,452] | -1,58 | 0,90 | +0,06 / 2,0 / 4,5 | BİLGİ (TUTMADI) | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | ABD d1619 | 2684 | +0,33 [-0,25; +0,90] | +0,10 | 0,509 [0,492] | -0,11 | 1,00 | +0,00 / 2,0 / 3,0 | TUTMADI | FARK boot alt <= 0; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | ABD d2022 | 3872 | -0,86 [-1,58; -0,05] | -1,00 | 0,484 [0,469] | -1,24 | 1,00 | +0,01 / 2,5 / 4,5 | TUTMADI | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | AVR d1619 | 1087 | -0,08 [-0,60; +0,43] | +0,02 | 0,499 [0,477] | -0,45 | 1,00 | -0,02 / 3,0 / 5,0 | TUTMADI | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | AVR d2022 | 1677 | -0,51 [-1,37; +0,47] | -0,77 | 0,476 [0,444] | -1,09 | 1,00 | +0,01 / 3,0 / 3,0 | TUTMADI | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | BIST d1619 | 1244 | -0,05 [-0,58; +0,52] | -1,37 | 0,494 [0,480] | -0,39 | 1,00 | -0,00 / 2,5 / 5,5 | BİLGİ (TUTMADI) | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |
| U0 | BIST d2022 | 644 | -0,87 [-2,31; +0,41] | -1,57 | 0,490 [0,456] | -1,67 | 1,00 | -0,06 / 0,5 / 5,5 | BİLGİ (TUTMADI) | FARK <= 0; FARK boot alt <= 0; SIRA <= 0,50; SIRA boot alt <= 0,50; L3O <= 0 |

| U1 - U0 | Hücre | n U1 / U0 | FARK(U1) - FARK(U0) [%95 boot, bilgi] | > 0 ? |
|---|---|---|---|---|
| U1 - U0 | ABD d1619 | 1279 / 2684 | -0,72 [-1,57; +0,09] | HAYIR |
| U1 - U0 | ABD d2022 | 1893 / 3872 | +0,94 [-0,06; +1,86] | EVET |
| U1 - U0 | AVR d1619 | 631 / 1087 | +0,38 [-0,44; +1,16] | EVET |
| U1 - U0 | AVR d2022 | 636 / 1677 | +0,91 [-0,28; +2,05] | EVET |
| U1 - U0 | BIST d1619 | 659 / 1244 | +0,34 [-0,96; +1,76] | EVET |
| U1 - U0 | BIST d2022 | 320 / 644 | +0,13 [-2,01; +2,11] | EVET |

### Getiri ve 1. tur cetveli (olay vs eş)

| Hipotez | Hücre | r15 ort olay / eş | r15 medyan olay / eş | n (cetvel) | h5 olay / eş | h10 olay / eş | stop olay / eş | KAT5 [%95] | konum eşli KAT [%95] | plasebo KAT5 [%95] | giriş stop altı (STOP sayıldı: h5 / stop) | takip stoplu getiri ort / medyan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| U1 | ABD d1619 | +0,79 / +1,18 | +0,82 / +1,64 | 1278 | 44,8 / 44,7 | 20,6 / 20,2 | 35,2 / 30,3 | 1,00 [0,93; 1,06] | 1,00 [0,93; 1,06] | 1,09 [0,84; 1,33] | 20 (44,1 / 36,2) | +1,25 / -0,88 |
| U1 | ABD d2022 | +1,76 / +1,67 | +1,02 / +1,73 | 1878 | 48,1 / 48,3 | 23,5 / 24,5 | 39,5 / 38,9 | 1,00 [0,95; 1,05] | 1,00 [0,95; 1,05] | 1,10 [0,87; 1,34] | 34 (47,3 / 40,6) | -0,26 / -1,58 |
| U1 | AVR d1619 | +1,31 / +1,01 | +1,47 / +1,51 | 674 | 42,6 / 38,4 | 14,2 / 13,0 | 30,3 / 27,1 | 1,11 [1,04; 1,21] | 1,09 [1,02; 1,19] | 1,15 [0,88; 1,47] | 9 (42,0 / 31,2) | +1,15 / +0,46 |
| U1 | AVR d2022 | +3,17 / +2,78 | +2,66 / +2,49 | 668 | 51,0 / 48,6 | 25,4 / 25,6 | 32,9 / 33,3 | 1,05 [0,98; 1,12] | 1,06 [0,99; 1,13] | 1,49 [1,12; 1,87] | 9 (50,4 / 33,8) | +1,42 / +0,23 |
| U1 | BIST d1619 | +0,19 / -0,09 | -0,42 / +0,09 | 709 | 40,9 / 43,3 | 19,0 / 22,8 | 39,1 / 37,4 | 0,95 [0,84; 1,02] | 0,96 [0,86; 1,03] | 0,85 [0,62; 1,08] | 5 (40,6 / 39,5) | +0,60 / -2,08 |
| U1 | BIST d2022 | +1,13 / +1,87 | +0,29 / +1,87 | 353 | 45,3 / 47,7 | 28,3 / 25,6 | 38,0 / 35,9 | 0,95 [0,86; 1,06] | 0,95 [0,87; 1,07] | 0,98 [0,83; 1,13] | 0 (45,3 / 38,0) | +2,87 / +0,64 |
| U0 | ABD d1619 | +2,80 / +2,47 | +2,52 / +2,44 | 2694 | 50,4 / 47,4 | 25,5 / 21,8 | 29,7 / 28,1 | 1,06 [1,02; 1,14] | 1,05 [1,01; 1,12] | 1,18 [0,88; 1,46] | 50 (49,5 / 30,9) | +2,60 / +0,61 |
| U0 | ABD d2022 | +1,48 / +2,34 | +1,83 / +2,38 | 3824 | 51,5 / 50,9 | 26,4 / 26,8 | 38,6 / 37,9 | 1,01 [0,97; 1,06] | 1,01 [0,98; 1,05] | 1,23 [1,03; 1,44] | 74 (50,6 / 39,8) | +0,37 / -1,23 |
| U0 | AVR d1619 | +1,38 / +1,46 | +1,14 / +1,59 | 1175 | 42,0 / 39,5 | 16,3 / 14,1 | 31,4 / 27,7 | 1,06 [0,98; 1,15] | 1,04 [0,96; 1,11] | 1,19 [0,90; 1,48] | 25 (41,2 / 32,8) | +1,21 / -0,19 |
| U0 | AVR d2022 | +1,68 / +2,19 | +1,43 / +3,31 | 1691 | 48,8 / 48,5 | 23,8 / 23,0 | 35,7 / 33,2 | 1,01 [0,94; 1,09] | 1,01 [0,95; 1,09] | 1,35 [1,05; 1,61] | 32 (47,9 / 36,9) | +0,72 / -0,26 |
| U0 | BIST d1619 | +1,56 / +1,62 | +0,83 / +2,22 | 1318 | 45,1 / 45,6 | 22,3 / 22,3 | 31,2 / 29,9 | 0,99 [0,94; 1,03] | 0,99 [0,94; 1,03] | 0,98 [0,78; 1,19] | 24 (44,3 / 32,4) | +2,56 / +0,28 |
| U0 | BIST d2022 | +4,15 / +5,02 | +3,55 / +3,37 | 705 | 56,6 / 57,2 | 34,8 / 36,9 | 30,4 / 30,3 | 0,99 [0,94; 1,04] | 0,99 [0,94; 1,04] | 1,24 [0,96; 1,50] | 10 (55,8 / 31,3) | +7,62 / +1,86 |

## 2. BİLGİ VARYANTLARI (hüküm yok)

| Hipotez | Hücre | n | R15 FARK [%95] | SIRA | r15 olay / eş | h5 olay / eş | stop olay / eş | KAT5 [%95] | R30 FARK [%95] (n) | p | BH |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U1b | ABD d1619 | 3581 | -0,22 [-0,51; +0,06] | 0,489 | +0,75 / +0,97 | 37,4 / 38,7 | 28,1 / 27,8 | 0,96 [0,92; 1,01] | -0,17 [-0,65; +0,29] (3117) | 0,9258 | geçmedi |
| U1b | ABD d2022 | 3780 | +0,14 [-0,31; +0,61] | 0,507 | +1,77 / +1,63 | 47,7 / 46,8 | 35,7 / 36,4 | 1,02 [0,98; 1,06] | -1,27 [-4,27; +0,59] (3214) | 0,2740 | geçmedi |
| U1b | AVR d1619 | 2074 | +0,10 [-0,17; +0,36] | 0,503 | +0,90 / +0,80 | 33,8 / 31,9 | 24,0 / 24,5 | 1,06 [1,00; 1,11] | +0,17 [-0,24; +0,56] (1782) | 0,2235 | geçmedi |
| U1b | AVR d2022 | 1507 | +0,32 [-0,04; +0,66] | 0,515 | +2,32 / +2,00 | 45,6 / 44,2 | 28,6 / 30,7 | 1,03 [0,99; 1,08] | +0,20 [-0,28; +0,67] (1318) | 0,0511 | geçmedi |
| U1b | BIST d1619 | 1366 | +0,19 [-0,41; +0,89] | 0,501 | +0,58 / +0,39 | 39,9 / 40,5 | 33,2 / 34,3 | 0,99 [0,93; 1,03] | +0,40 [-0,48; +1,46] (1157) | 0,3537 | - |
| U1b | BIST d2022 | 723 | -0,43 [-1,50; +0,44] | 0,494 | +2,15 / +2,58 | 50,3 / 50,0 | 33,8 / 33,3 | 1,01 [0,94; 1,07] | -1,09 [-2,68; +0,33] (598) | 0,8054 | - |
| U2 | ABD d1619 | 881 | -0,32 [-1,25; +0,37] | 0,487 | +1,04 / +1,37 | 45,9 / 45,7 | 34,6 / 31,8 | 1,00 [0,93; 1,07] | +0,16 [-0,81; +0,91] (814) | 0,7921 | geçmedi |
| U2 | ABD d2022 | 1057 | -0,68 [-1,63; +0,32] | 0,489 | +3,09 / +3,76 | 54,4 / 53,9 | 37,0 / 38,1 | 1,01 [0,95; 1,07] | -2,23 [-5,34; +0,31] (997) | 0,8682 | geçmedi |
| U2 | AVR d1619 | 468 | -0,13 [-1,13; +0,95] | 0,485 | +1,50 / +1,62 | 44,2 / 40,5 | 31,0 / 28,1 | 1,09 [1,00; 1,22] | -0,11 [-1,28; +1,17] (433) | 0,5908 | geçmedi |
| U2 | AVR d2022 | 467 | +0,55 [-0,19; +1,32] | 0,511 | +4,20 / +3,65 | 56,7 / 53,2 | 28,8 / 32,1 | 1,06 [0,98; 1,15] | -0,32 [-1,37; +0,67] (446) | 0,0882 | geçmedi |
| U2 | BIST d1619 | 452 | -0,01 [-1,03; +0,82] | 0,513 | +0,77 / +0,78 | 46,8 / 47,7 | 34,1 / 34,1 | 0,98 [0,89; 1,08] | +0,12 [-1,46; +1,26] (396) | 0,5078 | - |
| U2 | BIST d2022 | 181 | -0,01 [-2,49; +1,76] | 0,497 | +2,54 / +2,55 | 49,2 / 53,6 | 32,1 / 32,1 | 0,92 [0,78; 1,04] | +0,30 [-3,65; +2,95] (176) | 0,5001 | - |
| U3 | ABD d1619 | 563 | -0,41 [-1,64; +0,55] | 0,478 | +1,01 / +1,41 | 45,7 / 47,2 | 34,9 / 31,1 | 0,97 [0,82; 1,04] | +0,50 [-0,96; +1,70] (531) | 0,7960 | geçmedi |
| U3 | ABD d2022 | 656 | -0,29 [-1,26; +0,57] | 0,497 | +2,58 / +2,87 | 50,3 / 51,8 | 40,0 / 38,3 | 0,97 [0,91; 1,05] | -1,39 [-5,87; +1,57] (625) | 0,7286 | geçmedi |
| U3 | AVR d1619 | 299 | +0,51 [-0,51; +1,64] | 0,501 | +2,01 / +1,50 | 45,0 / 41,3 | 28,4 / 26,2 | 1,09 [1,00; 1,24] | +0,59 [-0,73; +2,29] (278) | 0,1799 | geçmedi |
| U3 | AVR d2022 | 290 | +0,21 [-0,70; +1,19] | 0,509 | +3,60 / +3,39 | 53,4 / 52,1 | 29,2 / 33,2 | 1,02 [0,91; 1,15] | -0,70 [-1,63; +0,41] (277) | 0,3373 | geçmedi |
| U3 | BIST d1619 | 315 | +0,20 [-1,02; +1,25] | 0,515 | +0,38 / +0,19 | 44,7 / 47,1 | 37,2 / 35,4 | 0,95 [0,82; 1,05] | +0,26 [-1,64; +2,04] (292) | 0,3689 | - |
| U3 | BIST d2022 | 113 | -1,20 [-3,47; +0,82] | 0,474 | -0,04 / +1,16 | 42,1 / 49,3 | 38,0 / 34,4 | 0,85 [0,67; 1,03] | -0,45 [-4,05; +2,81] (111) | 0,8592 | - |
| U1d | ABD d1619 | 15 | +9,05 [+0,19; +17,33] | 0,631 | +11,14 / +2,08 | 71,4 / 56,8 | 28,6 / 25,2 | 1,26 [0,91; 1,61] | +18,49 [-3,18; +41,62] (13) | 0,0514 | - |
| U1d | ABD d2022 | 48 | +2,22 [-3,02; +7,96] | 0,518 | +7,91 / +5,69 | 51,1 / 53,9 | 48,9 / 40,0 | 0,95 [0,65; 1,29] | -16,86 [-85,32; +13,23] (38) | 0,2363 | geçmedi |

R30 (bilgi; CETVEL2 v2.2 tanımı, tekil 30) U1 / U0:

- U1: ABD d1619 n 1092 FARK -0,20; ABD d2022 n 1592 FARK -1,70; AVR d1619 n 533 FARK +0,39; AVR d2022 n 549 FARK +0,38; BIST d1619 n 548 FARK +0,37; BIST d2022 n 261 FARK -0,10
- U0: ABD d1619 n 2462 FARK -0,08; ABD d2022 n 3531 FARK -1,54; AVR d1619 n 1007 FARK -0,24; AVR d2022 n 1547 FARK -0,45; BIST d1619 n 1116 FARK -0,33; BIST d2022 n 586 FARK -1,23

## 3. HUNİ (getirisiz; ön kayıttakiyle aynı dosya)

| Hipotez | Aşama | ABD d1619 | ABD d2022 | AVR d1619 | AVR d2022 | BIST d1619 | BIST d2022 |
|---|---|---|---|---|---|---|---|
| U1 (L2 hunisi) | L2 onaylı dip (L2 + 6 >= 60) | 59621 | 56479 | 32186 | 25785 | 21129 | 17558 |
| U1 (L2 hunisi) | + L1 var (L2 + 6'da) | 59274 | 56156 | 32040 | 25667 | 20947 | 17291 |
| U1 (L2 hunisi) | + F65 (L2 + 6'da) | 30774 | 29237 | 17554 | 13566 | 11263 | 7954 |
| U1 (L2 hunisi) | + DİPTE | 6868 | 9243 | 2685 | 3474 | 3345 | 1828 |
| U1 (L2 hunisi) | + Ş10 bir günde (L2 + 6 .. L2 + 20) | 2343 | 3278 | 969 | 1046 | 1184 | 653 |
| U1 (L2 hunisi) | + F68 aynı gün = U1 ham olay | 2267 | 3183 | 942 | 1013 | 1130 | 627 |
| U1 | olay (ilk gün + 15 bar; t tarihi) | 1946 | 2705 | 807 | 845 | 959 | 517 |
| U1 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 1298 | 1930 | 683 | 681 | 714 | 353 |
| U1 | R15 ölçülebilir | 1298 | 1911 | 683 | 677 | 714 | 353 |
| U1 | eşli (>= 5 eş) = n | 1279 | 1893 | 631 | 636 | 659 | 320 |
| U0 | olay (ilk gün + 15 bar; t tarihi) | 3826 | 5126 | 1414 | 2111 | 1738 | 997 |
| U0 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 2744 | 3929 | 1200 | 1730 | 1343 | 716 |
| U0 | R15 ölçülebilir | 2744 | 3896 | 1200 | 1723 | 1342 | 715 |
| U0 | eşli (>= 5 eş) = n | 2684 | 3872 | 1087 | 1677 | 1244 | 644 |
| U1b | olay (ilk gün + 15 bar; t tarihi) | 4952 | 5309 | 2829 | 2113 | 2088 | 1245 |
| U1b | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 3672 | 3941 | 2272 | 1667 | 1535 | 870 |
| U1b | R15 ölçülebilir | 3672 | 3909 | 2272 | 1659 | 1535 | 870 |
| U1b | eşli (>= 5 eş) = n | 3581 | 3780 | 2074 | 1507 | 1366 | 723 |
| U2 | olay (ilk gün + 15 bar; t tarihi) | 1267 | 1441 | 589 | 587 | 621 | 248 |
| U2 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 893 | 1065 | 506 | 482 | 489 | 196 |
| U2 | R15 ölçülebilir | 893 | 1063 | 506 | 480 | 489 | 196 |
| U2 | eşli (>= 5 eş) = n | 881 | 1057 | 468 | 467 | 452 | 181 |
| U3 | olay (ilk gün + 15 bar; t tarihi) | 838 | 929 | 374 | 372 | 423 | 153 |
| U3 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 571 | 664 | 323 | 305 | 337 | 121 |
| U3 | R15 ölçülebilir | 571 | 661 | 323 | 303 | 337 | 121 |
| U3 | eşli (>= 5 eş) = n | 563 | 656 | 299 | 290 | 315 | 113 |
| U1d | olay (ilk gün + 15 bar; t tarihi) | 156 | 230 | 0 | 0 | 0 | 0 |
| U1d | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 15 | 51 | 0 | 0 | 0 | 0 |
| U1d | R15 ölçülebilir | 15 | 48 | 0 | 0 | 0 | 0 |
| U1d | eşli (>= 5 eş) = n | 15 | 48 | 0 | 0 | 0 | 0 |

U1 ile U0'ın ortak L2 sayısı: {'ABD': 0, 'AVR': 0, 'BIST': 0}

yh_s10_bar eşitliği (ön kayıttan önce): ABD 150 / 150 bar birebir (S10 = 1: 47); AVR 150 / 150 bar birebir (S10 = 1: 44); BIST 150 / 150 bar birebir (S10 = 1: 54)

## 4. DENETİMLER

- Prefix (K2; veri t'de kesilip yeniden tarandı): ABD 30 / 30; AVR 30 / 30; BIST 30 / 30
- Yeniden üretim (K11; satır dosyasından düz pandas): U1 ABD d1619 TUTTU (n 1279, FARK -0,3885); U0 AVR d2022 TUTTU (n 1677, FARK -0,5143)
- Satır dosyası: arastirma_cikti/macd_uyum/uyum_satir.csv.gz (sha c8964b7bc42d19b4…)
- OC / c2 sayımı (U1): {"ABD": {"girdi": 4716, "sembol_yok": 0, "sinyal_bar_gecersiz": 0, "giris_yok": 0, "giris_gec": 1, "likidite_alt20": 1367, "bolunme_gecmis": 70, "evren_once": 0, "gecmis_eksik": 12, "havuz_az": 0, "havuz_disi": 1449, "tekil": 0, "olcum_r15": 3247, "kova_yok": 0, "donem": {"d2022": 1930, "d1619": 1298, "dis": 38}}, "AVR": {"girdi": 1798, "sembol_yok": 0, "sinyal_bar_gecersiz": 0, "giris_yok": 0, "giris_gec": 0, "likidite_alt20": 285, "bolunme_gecmis": 12, "evren_once": 0, "gecmis_eksik": 2, "havuz_az": 0, "havuz_disi": 299, "tekil": 0, "olcum_r15": 1495, "kova_yok": 0, "donem": {"d1619": 683, "

## HATA

- (koşudan önce; kod; K2 türü) mu_hisse'de 'n < 70' erken dönüşü olay taramasını serinin GELECEKTEKİ uzunluğuna bağlıyordu (seri başından 60-69 bar sonraki olaylar yalnız seri uzun olduğu için bulunuyordu). İlk koşunun prefix denetimi (16:28 UTC) BIST'te 2 / 30 olayda (GENIL 2021-11-11, TMSN 2015-09-01) DURDU; ölçüm (R15 / h5 / getiri) başlamadan, sonuç görülmeden. Düzeltme: eşik n <= 60 (git ec4f8c3), yeni test test_prefix_seri_basi (17 / 17), yeniden ön kayıt (git 6b08d4c). Eşikler (MU_ESIK sha), olay tablosu, huni ve eşitlik dosyaları bayt bayt aynı; tam veride olay kümesi değişmedi.
- (koşudan önce; test) Sentetik U0 serisi yatay bölgede kendiliğinden geçerli bir U1 de üretti; test 'aynı ikinci dipte U1 yok' sınayacak biçimde düzeltildi (kod hatası değil).
- (ifade; sonuca etkisiz) MU_KONTROL K7 kanıtındaki sembol sayıları (V_ABD 1.361 / AVR 575 / BIST 475) açık dosyadaki sayılardır; ölçüm evreni DS.ds_veri sonrası (fon / evren dışı, kısa seri çıkınca) ABD 1.348, AVR 573, BIST 467.
- (süreç; bilgi) KASA açık kesiti bu oturumda islenmis-veri fce5d94'ten aynı kesikle (2022-12-31) yeniden mühürlendi; manifest repo dışında (/tmp/kasa_yerel), mühür f674b4ee291c2f35 (CETVEL2 v2.2 ön kaydındaki 4a7fbad49def764c değil). Açık kısım V_ABD / V_AVR / V_BIST / k34 sha'ları arastirma_cikti/kasa/KASA_MANIFEST.json acik_sha256 ile AYNI. KASA.py ac çalıştırılmadı, KASA_DEFTERI / KASA_MANIFEST değişmedi; tam kaynak veri ve worktree mühürden hemen sonra silindi.
- (kapsam) K34 batanlar dahil ABD bilgi koşusu YAPILMADI (süre; ön kayıtta 'süre kalırsa' diye koşullu yazılıydı). k34_yahoo açık kısmı yalnız 2020-10-01 .. 2022-12-30 (d2022 hücresinin bir bölümü). Açık iş.
- (bilgi) R30 sütunu CETVEL2 v2.2 tanımıyla tekil 30 kullanır; n R15'ten küçüktür (ör. U1 ABD d2022 1.592 / 1.893).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; ön kayıttaki tablo)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | ANA: CETVEL2 v2.2 konum eşi = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x likidite üçlüsü x F15 çeyreği), bütün evren, aynı geometri (R15 stop'suz, aynı E0, 15 bar), aynı hipotezin o günkü olayları eş dışı, en az 5 eş (C2.c2_es); taban rastgele olay sağlaması = plasebo kapısı 200 tohum (C2.c2_plasebo, iki yön); MEKANİK ÜSTÜNLÜK: U0 kontrolü = dipte aynı çift dip (F65 + DİPTE + F68) ama MACD uyumsuzluğu yok; karar U1 - U0 > 0 ister; İKİNCİL: 1. tur eşi aynı d / hedef / takip |
| K2 | geleceğe bakma | EVET | göstergeler yalnız t'ye kadar (MACD [t-250, t], dipler [t-60, t-1], DİPTE <= L2, RSI nedensel, ATRP kesiti t günü); veri KASA açık kesik 2022-12-31 (kasa_kapisi her komuttan önce; satır dosyası en geç tarihi raporda); koşuda pazar başına 30 olay veri t'de kesilip yeniden taranır (DURUR); kova sınırları / güç eğrisi CETVEL2 v2.2 mühürlü dosyaları (getirisiz) |
| K3 | geçerli bar | EVET | YH._yh_hazir (= ge_hazir: H > L, V > 0, O/H/L/C > 0) bütün göstergeler ve bar sayıları geçerli bar sırasıyla; ölçümde OC.oc_veri_hazirla + DS açılış kırpması (CETVEL2); sinyal günü geçersiz bar olamaz (tarama geçerli barlarda) |
| K4 | tekilleştirme | EVET | her L2 en çok bir olay; hipotez başına aynı hissede >= 15 geçerli bar aralık; c2_olay OC tekil 15 işlem günü; n = bağımsız olay (hipotez başına ayrı c2_olc22 çağrısı); FARK ortalama + medyan, r15 ortalama + medyan; boot / permütasyon birimi giriş ayı |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla d; R15 paydası P['Op'][d, j]); eşler aynı gün açılışı; giriş stop altıysa STOP sayılır (sayısı yazılır) |
| K6 | veri birimi | EVET | V_*.pkl açık kısım tek kip (KASA bayt bayt; sha ön kayıtta); MACD fiyat birimli, F66 Close(L2)'ye bölünür; R15 / ATRP / F15 oran; AVR yerel para (hisse içi oran); U1d 5 $ eşiği yalnız ABD ham kapanış; geçmiş bölünme şüphesi havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD açık 1.361, V_AVR 575, V_BIST 475 sembol): batan / kottan çıkan yok -> dipteki olaylarda sonuç YUKARI yanlı; rapora yazılır; K34 batanlar (2020-10 sonrası) bilgi koşusu süre kalırsa |
| K8 | örneklem ve dönem | EVET | getirisiz huni pazar x dönem (U1, U0, bilgi varyantları) ve güç beklentisi ön kayıtta; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; iki alt dönem (2016-19, 2020-22) ayrı hücre, ABD ve AVR ayrı; bilgi varyantları BH q 0,10; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | UYUM_ON_KAYIT.md: MU_ESIK sha + YH_ESIK8 / C2_ESIK22 / C2_ESIK sha + MACD_UYUM.py ve bağımlı kod sha + kod commit + veri / eşik / güç / olay / huni / eşitlik sha'ları; mu_kapi git kaydı (ön kayıt commit < koşu), değişmemişlik, ik_kontrol_kapisi, kasa_kapisi; ikinci koşu DURUR; eşikler sonuç görülünce değişmez |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / SEC / metin ayrıştırması yok; yalnız OHLCV (V_*.pkl açık kısım) ve mühürlü CETVEL2 v2.2 eşik / güç dosyaları |
| K11 | yeniden üretim | EVET | raporda >= 2 hücre (U1 ABD d1619 ve U0 AVR d2022) satır dosyasından bağımsız düz pandas ile yeniden üretilir (n, ort FARK, ort SIRA, r15 ort; göreli 1e-9); tutmazsa DURUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla (TUTAR / TUTMADI / ÖLÇÜLEMEDİ, TUTTU / TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ); bilgi varyantlarında hüküm yok ('bilgi: dikkat' yalnız BH); 'iz / emare' sözü yok; sayı ile yorum ayrı cümle; DGXX için hüküm yok |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mu; mu_ / MU_ önekleri; test); yasak dosyalar (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KASA_DEFTERI.md) ve mevcut modüller değişmedi (git diff); KASA bloğu açılmadı; e-posta / anahtar taraması (YH._yh_yaz); push yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | bu işte alım-satım önerisi yok; ölçüm |

Colab notu: MACD_UYUM.py yeni; Colab'da kullanılırsa çalışma zamanını yeniden başlatın, sonra exec(open('MACD_UYUM.py').read()).
