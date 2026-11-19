# YAPI_HEDEF — DEVİR 3 RAPORU (DAR YENİDEN SINAMA, karne v3: AYK / NR7 / W2D / W1)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo. Koşu: 2026-11-19 13:37:06 UTC. Ön kayıt: DEVIR_3_ON_KAYIT.md (2026-11-19 13:36:25 UTC, git 650ded5884). Komut: `python YAPI_HEDEF.py devir3kos`.

**SONUÇ (8 karar satırı = 4 aday x 2 kol): KATKI+ 0, KATKI− 0, SORGULA 4, ÖLÇÜLEMEDİ 4.** SEÇİM YANLILIĞI: dört adayın sonucu DEVİR 1-2'de aynı veride görüldü; KATKI+ en fazla 'EMARE (bakılmış)', kesin karar Mart 2027 ileri testi.

Ölçü: 1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): n = h5 ve es_h5 olan olay; FARK = ort h5 - ort es_h5 (aynı gün aynı OC kovası eşleri); MARJ = FARK(aday VE kol) - FARK(kol), aynı pazar x hücre x ambargo; stop: ort st5 / ort es_st5. BİLGİ: MARJ_sonlu = FARK(aday VE kol) - FARK(kol VE aday özelliği sonlu) (W2D F32 / W1 F30 NaN tabanı farkı). Etiket: KARNE v3 (yalnız 'ana' adaylar). Kol A karar pazarları ABD ve AVR AYRI, kol B yalnız ABD; hücreler eğitim (2016-22) ve sınama (2023-26, ambargolu). ÖLÇÜLEMEDİ = bir karar hücresinde n < 30 (kol B: ya da ABD hücrelerinden birinde güç < 0,80). KATKI+ = her karar hücresinde FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; VE genel tabaka şartı; VE ATRP şartı (her F55 tercilinde MARJ > 0). KATKI− = her karar hücresinde MARJ < 0 VE bootstrap %95 üst ucu < 0. Değilse SORGULA. Ters yön (YÖN 2) hücresi, 'bilgi' / 'ters' adaylar, BIST ve ABD+AVR havuzu, AVR kol B yalnız BİLGİ. Değerler yüzde puan; P = 15 barda +%5 hedefin stop'tan önce görülme payı.

## 1. Karar tablosu (kol A: ABD ve AVR ayrı; kol B: ABD; eğitim 2016-22, sınama 2023-26 ambargolu)

| Aday | Kol | Pazar | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | stop olay / eş (eğitim; sınama) | boot alt / üst (eğ; sın) | L3O (eğ; sın) | güç (eğ; sın) | etiket | karar okuması |
|---|---|---|---|---|---|---|---|---|---|---|
| AYK | A | ABD | 2172 / +1,25 (+2,49) | 1601 / +1,78 (+1,94) | %30,8 / %26,8; %32,6 / %28,8 | +0,76 / +4,33; -0,05 / +4,16 | +1,75; +0,54 | 1,00; 1,00 | SORGULA | SORGULA (karar yok) |
| AYK | A | AVR | 1122 / +3,06 (+2,56) | 543 / -0,40 (+0,73) | %22,8 / %20,5; %23,9 / %20,1 | +0,42 / +4,71; -2,75 / +4,17 | +1,52; -0,86 | 0,99; 0,83 | SORGULA | SORGULA (karar yok) |
| AYK | B | ABD | 157 / -3,09 (-5,93) | 188 / +9,36 (+1,10) | %43,9 / %29,2; %34,6 / %34,5 | -11,76 / +1,08; -4,49 / +6,73 | -7,94; -2,21 | 0,42; 0,59 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (iddia kapanmaz) |
| AYK | B | AVR | 41 / +15,06 (+7,87) | 34 / +7,87 (-0,41) | %24,4 / %22,4; %29,4 / %23,1 | -2,82 / +17,01; -14,33 / +12,12 | +2,31; -6,73 | 0,14; 0,13 | BİLGİ (ÖLÇÜLEMEDİ) | - |
| NR7 | A | ABD | 1164 / +1,50 (+2,74) | 698 / +4,06 (+4,23) | %24,9 / %26,5; %27,2 / %29,1 | -0,11 / +5,71; +0,97 / +7,64 | +1,64; +2,42 | 0,98; 0,84 | SORGULA | SORGULA (karar yok) |
| NR7 | A | AVR | 612 / +0,80 (+0,30) | 287 / -5,91 (-4,79) | %18,8 / %19,4; %24,0 / %19,4 | -2,80 / +3,23; -8,80 / -0,88 | -0,93; -7,27 | 0,88; 0,54 | SORGULA | SORGULA (karar yok) |
| NR7 | B | ABD | 48 / +7,43 (+4,59) | 60 / +13,35 (+5,08) | %29,2 / %29,6; %31,7 / %33,9 | -10,45 / +16,32; -4,58 / +16,16 | -3,90; +0,69 | 0,12; 0,15 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (iddia kapanmaz) |
| NR7 | B | AVR | 13 / -5,09 (-12,28) | 6 / +6,53 (-1,75) | %46,2 / %14,4; %33,3 / %31,5 | -37,17 / +17,14; -33,91 / +38,30 | -31,92; -30,18 | 0,06; 0,04 | BİLGİ (ÖLÇÜLEMEDİ) | - |
| W2D | A | ABD | 1752 / -0,26 (+0,99) | 1098 / +2,43 (+2,60) | %25,8 / %25,2; %26,0 / %27,3 | -1,62 / +3,66; -0,25 / +6,02 | -0,05; +1,25 | 1,00; 0,97 | SORGULA | SORGULA (karar yok) |
| W2D | A | AVR | 973 / +0,50 (-0,00) | 500 / +0,65 (+1,77) | %18,4 / %18,7; %22,6 / %20,5 | -2,47 / +2,59; -2,66 / +6,50 | -0,98; -1,58 | 0,98; 0,81 | SORGULA | SORGULA (karar yok) |
| W2D | B | ABD | 51 / +4,73 (+1,89) | 66 / +3,34 (-4,93) | %39,2 / %27,6; %39,4 / %35,1 | -12,05 / +15,78; -12,49 / +2,80 | -5,38; -7,95 | 0,12; 0,17 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (iddia kapanmaz) |
| W2D | B | AVR | 15 / +5,15 (-2,04) | 22 / +12,30 (+4,01) | %26,7 / %23,9; %27,3 / %22,7 | -29,12 / +19,17; -15,81 / +24,22 | -25,01; -8,02 | 0,06; 0,08 | BİLGİ (ÖLÇÜLEMEDİ) | - |
| W1 | A | ABD | 1977 / -1,15 (+0,10) | 1175 / +1,44 (+1,61) | %23,9 / %25,1; %24,3 / %26,5 | -1,80 / +1,82; -0,52 / +4,08 | -0,74; +0,51 | 1,00; 0,99 | SORGULA | SORGULA (karar yok) |
| W1 | A | AVR | 1060 / +1,75 (+1,25) | 433 / -0,14 (+0,98) | %19,2 / %19,5; %20,1 / %19,6 | -1,10 / +3,56; -2,37 / +4,04 | +0,18; -0,51 | 0,99; 0,75 | SORGULA | SORGULA (karar yok) |
| W1 | B | ABD | 53 / +9,71 (+6,87) | 52 / +12,59 (+4,32) | %26,4 / %30,9; %30,8 / %32,0 | -4,37 / +18,08; -5,29 / +17,96 | +2,08; -1,93 | 0,13; 0,14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (iddia kapanmaz) |
| W1 | B | AVR | 15 / +4,28 (-2,91) | 5 / -15,89 (-24,17) | %20,0 / %22,2; %60,0 / %27,7 | -22,94 / +21,07; -52,24 / +8,85 | -18,00; -47,19 | 0,06; 0,04 | BİLGİ (ÖLÇÜLEMEDİ) | - |

AVR kol B satırları BİLGİ'dir (karar ABD ile). Kol B etiketi ABD satırındadır.

## 2. ATRP (F55) tercilleri içinde MARJ (KATKI+ ek şartı: HER hücrede > 0)

| Aday | Kol | Pazar | Hücre | T0 n / MARJ | T1 n / MARJ | T2 n / MARJ | ATRP şartı |
|---|---|---|---|---|---|---|---|
| AYK | A | ABD | egitim | 400 / +1,10 | 643 / +1,67 | 1129 / -0,90 | TUTMADI |
| AYK | A | ABD | sinama | 177 / -3,07 | 482 / -1,87 | 942 / +1,01 | TUTMADI |
| AYK | A | AVR | egitim | 238 / +3,62 | 323 / +1,06 | 561 / -0,50 | TUTMADI |
| AYK | A | AVR | sinama | 95 / -3,32 | 152 / -0,65 | 296 / -1,36 | TUTMADI |
| NR7 | A | ABD | egitim | 368 / +0,01 | 383 / +3,57 | 413 / +3,67 | TUTMADI |
| NR7 | A | ABD | sinama | 143 / +1,27 | 249 / +4,32 | 306 / +5,22 | TUTMADI |
| NR7 | A | AVR | egitim | 216 / -0,20 | 186 / -1,71 | 210 / +2,83 | TUTMADI |
| NR7 | A | AVR | sinama | 80 / +4,06 | 93 / -0,79 | 114 / -14,28 | TUTMADI |
| W2D | A | ABD | egitim | 488 / +1,99 | 713 / +1,40 | 551 / -1,56 | TUTMADI |
| W2D | A | ABD | sinama | 203 / -4,37 | 445 / +3,66 | 450 / +4,22 | TUTMADI |
| W2D | A | AVR | egitim | 310 / +1,19 | 327 / -2,50 | 336 / +0,84 | TUTMADI |
| W2D | A | AVR | sinama | 111 / -0,83 | 163 / +1,92 | 226 / +0,78 | TUTMADI |
| W1 | A | ABD | egitim | 790 / +1,49 | 695 / +0,23 | 492 / +1,74 | TUTMADI |
| W1 | A | ABD | sinama | 316 / +3,89 | 467 / +3,12 | 392 / +1,93 | TUTMADI |
| W1 | A | AVR | egitim | 354 / +3,49 | 370 / -1,58 | 336 / +2,27 | TUTMADI |
| W1 | A | AVR | sinama | 136 / +2,57 | 149 / -3,57 | 148 / +6,45 | TUTMADI |
| AYK | B | ABD | egitim | 1 / -42,53 | 23 / +0,29 | 133 / -6,79 | TUTMADI |
| AYK | B | ABD | sinama | 1 / -14,71 | 27 / +3,96 | 160 / -0,94 | TUTMADI |
| NR7 | B | ABD | egitim | 0 / - | 11 / +4,55 | 37 / +4,03 | TUTMADI |
| NR7 | B | ABD | sinama | 3 / +24,33 | 6 / +1,87 | 51 / +3,91 | TUTMADI |
| W2D | B | ABD | egitim | 1 / -34,30 | 12 / +18,26 | 38 / -2,59 | TUTMADI |
| W2D | B | ABD | sinama | 0 / - | 20 / -1,10 | 46 / -5,54 | TUTMADI |
| W1 | B | ABD | egitim | 1 / +100,35 | 18 / -5,47 | 34 / +9,72 | TUTMADI |
| W1 | B | ABD | sinama | 1 / -14,93 | 12 / -0,81 | 39 / +6,92 | TUTMADI |

## 3. Genel K1 tabaka (F10 / F15 / F7 / F55 / F13; karar pazarları havuzu; n >= 30 tabakada MARJ <= 0 olanlar)

| Aday | Kol | tabaka şartı | MARJ <= 0 olan tabakalar (n >= 30) |
|---|---|---|---|
| AYK | A | TUTMADI | F10|T2|egitim (883 / -0,28); F55|T0|sinama (272 / -3,15); F55|T1|sinama (634 / -1,53); F55|T2|egitim (1690 / -0,78) |
| NR7 | A | TUTMADI | F10|T0|egitim (597 / -0,27); F7|T2|sinama (334 / -0,81); F55|T2|sinama (420 / -0,08) |
| W2D | A | TUTMADI | F10|T2|egitim (871 / -1,47); F15|T0|egitim (940 / -0,53); F7|T0|egitim (1793 / -0,17); F7|T1|egitim (792 / -1,06); F7|T1|sinama (441 / -0,10); F7|T2|sinama (97 / -6,40); F55|T0|sinama (314 / -3,11); F55|T2|egitim (887 / -0,61); F13|T1|egitim (853 / -1,15) |
| W1 | A | TUTMADI | F7|T0|egitim (899 / -1,09); F55|T1|egitim (1065 / -0,39); F13|T0|egitim (1040 / -0,23); F13|T2|egitim (972 / -0,03); F13|T2|sinama (539 / -0,28) |
| AYK | B | TUTMADI | F10|T0|egitim (95 / -5,34); F10|T0|sinama (130 / -0,40); F10|T1|egitim (43 / -5,43); F15|T0|egitim (157 / -5,93); F7|T0|egitim (62 / -11,39); F7|T0|sinama (98 / -3,87); F7|T1|egitim (48 / -5,84); F55|T2|egitim (133 / -6,79); F55|T2|sinama (160 / -0,94); F13|T0|egitim (65 / -7,82); F13|T1|egitim (48 / -12,49) |
| NR7 | B | TUTTU | - |
| W2D | B | TUTMADI | F15|T0|sinama (66 / -4,93); F7|T0|sinama (51 / -2,69); F55|T2|egitim (38 / -2,59); F55|T2|sinama (46 / -5,54) |
| W1 | B | TUTTU | - |

### F13 (kırılım hacmi) tercilleri içinde MARJ (bilgi; kol A ABD+AVR havuzu)

| Aday | Hücre | T0 n / MARJ | T1 n / MARJ | T2 n / MARJ |
|---|---|---|---|---|
| AYK | egitim | 1185 / +3,17 | 1124 / +2,03 | 985 / +2,60 |
| AYK | sinama | 679 / +2,20 | 820 / +2,04 | 645 / +0,75 |
| NR7 | egitim | 747 / +3,37 | 587 / +1,47 | 442 / +1,11 |
| NR7 | sinama | 378 / +2,48 | 329 / +0,81 | 278 / +1,71 |
| W2D | egitim | 792 / +2,16 | 853 / -1,15 | 1080 / +0,57 |
| W2D | sinama | 423 / +0,68 | 545 / +1,31 | 630 / +4,12 |
| W1 | egitim | 1040 / -0,23 | 1025 / +1,87 | 972 / -0,03 |
| W1 | sinama | 505 / +4,87 | 564 / +0,11 | 539 / -0,28 |

## 4. Bilgi satırları (karar değil)

### MARJ_sonlu (taban = aday özelliği sonlu olaylar; W2D / W1 NaN tabanı farkı)

| Aday | Kol | Pazar | eğitim MARJ / MARJ_sonlu | sınama MARJ / MARJ_sonlu |
|---|---|---|---|---|
| AYK | A | ABD | +2,49 / +2,49 | +1,94 / +1,94 |
| NR7 | A | ABD | +2,74 / +2,74 | +4,23 / +4,23 |
| W2D | A | ABD | +0,99 / +1,86 | +2,60 / +3,26 |
| W1 | A | ABD | +0,10 / +0,46 | +1,61 / +2,14 |
| AYK | A | AVR | +2,56 / +2,56 | +0,73 / +0,73 |
| NR7 | A | AVR | +0,30 / +0,30 | -4,79 / -4,79 |
| W2D | A | AVR | -0,00 / +0,20 | +1,77 / +2,16 |
| W1 | A | AVR | +1,25 / +1,20 | +0,98 / +0,80 |
| AYK | B | ABD | -5,93 / -5,93 | +1,10 / +1,10 |
| NR7 | B | ABD | +4,59 / +4,59 | +5,08 / +5,08 |
| W2D | B | ABD | +1,89 / +1,46 | -4,93 / -2,00 |
| W1 | B | ABD | +6,87 / +6,33 | +4,32 / +5,60 |
| AYK | B | AVR | +7,87 / +7,87 | -0,41 / -0,41 |
| NR7 | B | AVR | -12,28 / -12,28 | -1,75 / -1,75 |
| W2D | B | AVR | -2,04 / -6,81 | +4,01 / +1,18 |
| W1 | B | AVR | -2,91 / -4,60 | -24,17 / -26,21 |

### Bilgi / ters adaylar ve öteki pazarlar (ABD+AVR havuzu, BIST)

| Aday | Kol | Pazar | eğitim n / FARK (MARJ) | sınama n / FARK (MARJ) | ters yön n / FARK (MARJ) | etiket |
|---|---|---|---|---|---|---|
| AYK | A | ABD+AVR | 3294 / +1,86 (+2,51) | 2144 / +1,23 (+1,67) | 2859 / +2,31 (+2,91) | BİLGİ (SORGULA) |
| NR7 | A | ABD+AVR | 1776 / +1,26 (+1,91) | 985 / +1,15 (+1,59) | 1699 / +1,46 (+2,06) | BİLGİ (SORGULA) |
| W2D | A | ABD+AVR | 2725 / +0,01 (+0,66) | 1598 / +1,87 (+2,31) | 2708 / -0,16 (+0,45) | BİLGİ (SORGULA) |
| W1 | A | ABD+AVR | 3037 / -0,14 (+0,51) | 1608 / +1,02 (+1,46) | 3200 / -0,33 (+0,28) | BİLGİ (SORGULA) |
| NR7a | A | ABD+AVR | 317 / +4,74 (+5,39) | 216 / +4,70 (+5,14) | 303 / +4,64 (+5,24) | BİLGİ (SORGULA) |
| NR7y | A | ABD+AVR | 1459 / +0,50 (+1,15) | 769 / +0,16 (+0,60) | 1396 / +0,77 (+1,37) | BİLGİ (SORGULA) |
| IDNR4 | A | ABD+AVR | 758 / +1,98 (+2,63) | 479 / +1,97 (+2,41) | 734 / +2,02 (+2,62) | BİLGİ (SORGULA) |
| NR7t | A | ABD+AVR | 11399 / -0,95 (-0,30) | 6902 / -0,67 (-0,23) | 10974 / -0,92 (-0,32) | BİLGİ (SORGULA) |
| W2Dt | A | ABD+AVR | 2723 / -2,32 (-1,67) | 1710 / -0,69 (-0,25) | 2384 / -2,35 (-1,74) | BİLGİ (SORGULA) |
| W1t | A | ABD+AVR | 3035 / -0,06 (+0,59) | 1994 / -0,65 (-0,21) | 2687 / -0,01 (+0,59) | BİLGİ (SORGULA) |
| NR7a | A | ABD | 207 / +3,20 (+4,44) | 169 / +8,50 (+8,67) | 197 / +3,14 (+4,30) | BİLGİ (SORGULA) |
| NR7y | A | ABD | 957 / +1,13 (+2,38) | 529 / +2,64 (+2,81) | 917 / +1,34 (+2,51) | BİLGİ (SORGULA) |
| IDNR4 | A | ABD | 461 / +0,94 (+2,18) | 342 / +1,61 (+1,77) | 446 / +0,83 (+2,00) | BİLGİ (SORGULA) |
| NR7t | A | ABD | 7518 / -1,67 (-0,42) | 4930 / -0,77 (-0,60) | 7237 / -1,60 (-0,44) | BİLGİ (SORGULA) |
| W2Dt | A | ABD | 1750 / -2,91 (-1,66) | 1164 / -0,63 (-0,46) | 1520 / -3,00 (-1,83) | BİLGİ (SORGULA) |
| W1t | A | ABD | 1976 / -1,41 (-0,17) | 1412 / -0,41 (-0,24) | 1706 / -1,38 (-0,21) | BİLGİ (SORGULA) |
| NR7a | A | AVR | 110 / +7,63 (+7,13) | 47 / -8,97 (-7,85) | 106 / +7,43 (+6,95) | BİLGİ (SORGULA) |
| NR7y | A | AVR | 502 / -0,70 (-1,20) | 240 / -5,31 (-4,19) | 479 / -0,33 (-0,82) | BİLGİ (SORGULA) |
| IDNR4 | A | AVR | 297 / +3,59 (+3,09) | 137 / +2,87 (+3,99) | 288 / +3,87 (+3,38) | BİLGİ (SORGULA) |
| NR7t | A | AVR | 3881 / +0,45 (-0,05) | 1972 / -0,42 (+0,70) | 3737 / +0,39 (-0,09) | BİLGİ (SORGULA) |
| W2Dt | A | AVR | 973 / -1,25 (-1,75) | 546 / -0,83 (+0,29) | 864 / -1,21 (-1,69) | BİLGİ (SORGULA) |
| W1t | A | AVR | 1059 / +2,47 (+1,97) | 582 / -1,23 (-0,11) | 981 / +2,36 (+1,87) | BİLGİ (SORGULA) |
| AYK | A | BIST | 647 / -0,90 (+0,33) | 652 / -2,01 (-1,27) | 463 / -3,51 (-2,29) | BİLGİ (SORGULA) |
| NR7 | A | BIST | 381 / -1,55 (-0,32) | 311 / -2,06 (-1,32) | 369 / -1,69 (-0,46) | BİLGİ (SORGULA) |
| W2D | A | BIST | 469 / -7,12 (-5,89) | 309 / -0,01 (+0,73) | 454 / -6,43 (-5,21) | BİLGİ (SORGULA) |
| W1 | A | BIST | 572 / -0,39 (+0,84) | 423 / -2,96 (-2,22) | 549 / -0,98 (+0,24) | BİLGİ (SORGULA) |
| NR7a | A | BIST | 120 / -2,13 (-0,90) | 129 / -2,80 (-2,06) | 118 / -2,09 (-0,86) | BİLGİ (SORGULA) |
| NR7y | A | BIST | 261 / -1,28 (-0,06) | 182 / -1,53 (-0,79) | 251 / -1,50 (-0,27) | BİLGİ (SORGULA) |
| IDNR4 | A | BIST | 183 / -4,60 (-3,37) | 139 / -5,72 (-4,98) | 172 / -4,38 (-3,15) | BİLGİ (SORGULA) |
| NR7t | A | BIST | 2207 / -1,17 (+0,06) | 1763 / -0,51 (+0,23) | 2134 / -1,14 (+0,08) | BİLGİ (SORGULA) |
| W2Dt | A | BIST | 469 / -1,29 (-0,06) | 253 / -1,74 (-1,00) | 533 / -0,79 (+0,44) | BİLGİ (SORGULA) |
| W1t | A | BIST | 572 / -4,57 (-3,34) | 474 / -0,61 (+0,13) | 472 / -4,26 (-3,04) | BİLGİ (SORGULA) |
| AYK | B | ABD+AVR | 198 / +0,67 (-3,07) | 222 / +9,14 (+0,87) | 165 / +0,64 (-3,51) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7 | B | ABD+AVR | 61 / +4,76 (+1,03) | 66 / +12,73 (+4,46) | 55 / +6,53 (+2,38) | BİLGİ (ÖLÇÜLEMEDİ) |
| W2D | B | ABD+AVR | 66 / +4,83 (+1,09) | 88 / +5,58 (-2,69) | 66 / +5,78 (+1,63) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1 | B | ABD+AVR | 68 / +8,51 (+4,78) | 57 / +10,09 (+1,82) | 67 / +5,46 (+1,31) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7a | B | ABD+AVR | 27 / +17,77 (+14,04) | 41 / +10,01 (+1,74) | 25 / +19,15 (+15,00) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7y | B | ABD+AVR | 34 / -5,56 (-9,30) | 25 / +17,19 (+8,92) | 30 / -3,99 (-8,14) | BİLGİ (ÖLÇÜLEMEDİ) |
| IDNR4 | B | ABD+AVR | 17 / -5,91 (-9,65) | 25 / +12,67 (+4,40) | 17 / -5,91 (-10,06) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7t | B | ABD+AVR | 374 / +3,57 (-0,17) | 360 / +7,45 (-0,82) | 344 / +3,77 (-0,38) | BİLGİ (SORGULA) |
| W2Dt | B | ABD+AVR | 59 / +6,83 (+3,10) | 42 / +13,92 (+5,65) | 52 / +3,25 (-0,90) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1t | B | ABD+AVR | 115 / -1,19 (-4,93) | 122 / +2,45 (-5,82) | 97 / +0,80 (-3,35) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7a | B | ABD | 20 / +17,84 (+15,00) | 38 / +10,03 (+1,76) | 20 / +17,84 (+13,83) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7y | B | ABD | 28 / +0,00 (-2,85) | 22 / +19,08 (+10,82) | 26 / +1,88 (-2,13) | BİLGİ (ÖLÇÜLEMEDİ) |
| IDNR4 | B | ABD | 15 / -14,71 (-17,55) | 23 / +15,34 (+7,07) | 15 / -14,71 (-18,72) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7t | B | ABD | 298 / +2,11 (-0,74) | 294 / +7,23 (-1,04) | 275 / +3,21 (-0,80) | BİLGİ (SORGULA) |
| W2Dt | B | ABD | 51 / +3,77 (+0,92) | 33 / +14,15 (+5,88) | 46 / +1,59 (-2,42) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1t | B | ABD | 84 / -5,51 (-8,35) | 95 / +0,60 (-7,67) | 70 / -3,32 (-7,33) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7a | B | AVR | 7 / +17,58 (+10,38) | 3 / +9,79 (+1,50) | 5 / +24,38 (+19,68) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7y | B | AVR | 6 / -31,53 (-38,73) | 3 / +3,28 (-5,01) | 4 / -42,18 (-46,89) | BİLGİ (ÖLÇÜLEMEDİ) |
| IDNR4 | B | AVR | 2 / +60,04 (+52,85) | 2 / -17,99 (-26,27) | 2 / +60,04 (+55,34) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7t | B | AVR | 76 / +9,30 (+2,10) | 66 / +8,44 (+0,16) | 69 / +6,00 (+1,29) | BİLGİ (SORGULA) |
| W2Dt | B | AVR | 8 / +26,35 (+19,16) | 9 / +13,07 (+4,78) | 6 / +15,92 (+11,21) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1t | B | AVR | 31 / +10,51 (+3,31) | 27 / +8,94 (+0,66) | 27 / +11,49 (+6,78) | BİLGİ (ÖLÇÜLEMEDİ) |
| AYK | B | BIST | 101 / +0,21 (+0,01) | 180 / +0,45 (-1,44) | 79 / -5,64 (-6,24) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7 | B | BIST | 44 / -5,26 (-5,46) | 52 / +1,68 (-0,21) | 44 / -5,26 (-5,85) | BİLGİ (ÖLÇÜLEMEDİ) |
| W2D | B | BIST | 43 / +2,82 (+2,61) | 63 / -2,64 (-4,53) | 41 / +5,20 (+4,60) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1 | B | BIST | 56 / +0,23 (+0,02) | 84 / +4,40 (+2,52) | 55 / -1,20 (-1,79) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7a | B | BIST | 24 / -3,36 (-3,56) | 38 / +2,76 (+0,88) | 24 / -3,36 (-3,95) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7y | B | BIST | 20 / -7,54 (-7,74) | 14 / -1,28 (-3,16) | 20 / -7,54 (-8,13) | BİLGİ (ÖLÇÜLEMEDİ) |
| IDNR4 | B | BIST | 22 / +2,69 (+2,48) | 20 / +5,59 (+3,70) | 22 / +2,69 (+2,09) | BİLGİ (ÖLÇÜLEMEDİ) |
| NR7t | B | BIST | 194 / +1,44 (+1,24) | 305 / +1,92 (+0,04) | 192 / +1,93 (+1,34) | BİLGİ (SORGULA) |
| W2Dt | B | BIST | 48 / -6,03 (-6,23) | 24 / -6,17 (-8,06) | 53 / -4,99 (-5,59) | BİLGİ (ÖLÇÜLEMEDİ) |
| W1t | B | BIST | 54 / -6,31 (-6,51) | 68 / -8,12 (-10,00) | 49 / -10,37 (-10,96) | BİLGİ (ÖLÇÜLEMEDİ) |

### Kol tabanları

| Kol | Pazar | eğitim n / FARK | sınama n / FARK | stop olay / eş (eğitim; sınama) |
|---|---|---|---|---|
| A | ABD+AVR | 13175 / -0,65 | 7887 / -0,44 | %23,4 / %23,5; %25,5 / %25,8 |
| A | ABD | 8682 / -1,24 | 5628 / -0,17 | %25,5 / %25,4; %27,5 / %28,2 |
| A | AVR | 4493 / +0,50 | 2259 / -1,12 | %19,4 / %19,7; %20,6 / %19,8 |
| A | BIST | 2588 / -1,23 | 2074 / -0,74 | %28,3 / %26,3; %36,5 / %36,0 |
| B | ABD+AVR | 435 / +3,74 | 426 / +8,27 | %33,6 / %27,8; %32,2 / %31,6 |
| B | ABD | 346 / +2,85 | 354 / +8,27 | %35,3 / %29,6; %31,9 / %33,1 |
| B | AVR | 89 / +7,20 | 72 / +8,28 | %27,0 / %20,9; %33,3 / %24,1 |
| B | BIST | 238 / +0,20 | 357 / +1,89 | %30,7 / %29,6; %29,1 / %31,2 |

## 5. n < 30 hücrelerin olayları (K8; ana adaylar, ABD / AVR)

**NR7 kol B AVR egitim (n 13)**: CBK.DE 2018-04-23 (h5 0, eş 0.50, st 0); CBK.DE 2018-07-24 (h5 0, eş 0.22, st 1); EZJ.L 2022-08-04 (h5 0, eş 0.29, st 1); GSK.L 2022-10-21 (h5 0, eş 0.83, st 1); HIK.L 2017-09-29 (h5 0, eş 0.15, st 0); HOC.L 2017-11-21 (h5 0, eş 0.39, st 1); ITRK.L 2022-07-15 (h5 0, eş 0.79, st 1); LDO.MI 2022-10-21 (h5 1, eş 0.81, st 0); OCDO.L 2019-01-07 (h5 1, eş 0.31, st 0); TIT.MI 2019-06-04 (h5 1, eş 0.36, st 0); TOM.OL 2022-11-10 (h5 1, eş 0.37, st 0); UBI.PA 2022-12-01 (h5 0, eş 0.18, st 1); VITR.ST 2016-12-27 (h5 1, eş 0.46, st 0)

**NR7 kol B AVR sinama (n 6)**: CDR.WA 2026-07-02 (h5 0, eş 0.29, st 0); KBC.BR 2023-11-24 (h5 1, eş 0.48, st 0); KNOS.L 2023-05-22 (h5 1, eş 0.17, st 0); LOGN.SW 2026-03-12 (h5 0, eş 0.25, st 1); RNO.PA 2025-09-11 (h5 0, eş 0.35, st 0); VTY.L 2025-03-20 (h5 0, eş 0.07, st 1)

**W2D kol B AVR egitim (n 15)**: AF.PA 2021-08-24 (h5 0, eş 0.21, st 1); ASHM.L 2017-01-04 (h5 0, eş 0.32, st 1); AVON.L 2021-09-23 (h5 1, eş 0.21, st 0); BARC.L 2022-05-17 (h5 1, eş 0.61, st 0); CTEC.L 2021-10-29 (h5 0, eş 0.50, st 0); HIK.L 2017-09-29 (h5 0, eş 0.15, st 0); HOC.L 2021-09-03 (h5 0, eş 0.33, st 1); IPN.PA 2021-01-14 (h5 0, eş 0.40, st 0); LOGN.SW 2022-01-05 (h5 0, eş 0.41, st 1); NOKIA.HE 2020-01-02 (h5 1, eş 0.35, st 0); PNN.L 2021-11-25 (h5 0, eş 0.30, st 0); RIO.L 2021-12-07 (h5 0, eş 0.21, st 0); RR.L 2022-05-27 (h5 1, eş 0.23, st 0); TKA.DE 2022-05-11 (h5 1, eş 0.68, st 0); VK.PA 2022-08-23 (h5 1, eş 0.32, st 0)

**W2D kol B AVR sinama (n 22)**: ADS.DE 2025-09-05 (h5 1, eş 0.24, st 0); AF.PA 2024-08-30 (h5 1, eş 0.18, st 0); AFX.DE 2025-09-22 (h5 0, eş 0.51, st 1); AIXA.DE 2024-05-15 (h5 0, eş 0.21, st 1); BOL.ST 2023-06-02 (h5 0, eş 0.23, st 1); CDR.WA 2023-04-27 (h5 0, eş 0.14, st 0); CDR.WA 2023-11-14 (h5 0, eş 0.47, st 1); CDR.WA 2026-07-02 (h5 0, eş 0.29, st 0); DHER.DE 2023-04-11 (h5 1, eş 0.59, st 0); EDV.L 2024-03-04 (h5 1, eş 0.49, st 0); EDV.L 2026-08-05 (h5 1, eş 0.37, st 0); ELUX-B.ST 2025-10-21 (h5 1, eş 0.32, st 0); GNC.L 2026-07-16 (h5 1, eş 0.73, st 0); HOC.L 2026-08-05 (h5 1, eş 0.43, st 0); MC.PA 2025-07-01 (h5 1, eş 0.14, st 0); NOKIA.HE 2025-09-03 (h5 1, eş 0.37, st 0); RAT.L 2026-07-15 (h5 0, eş 0.64, st 0); SIX2.DE 2026-01-09 (h5 0, eş 0.32, st 1); SPI.L 2026-01-13 (h5 1, eş 0.37, st 0); TATE.L 2026-02-04 (h5 0, eş 0.25, st 0); TGS.OL 2025-05-09 (h5 0, eş 0.75, st 0); VOD.L 2023-07-24 (h5 0, eş 0.25, st 1)

**W1 kol B AVR egitim (n 15)**: BARC.L 2022-05-17 (h5 1, eş 0.61, st 0); CDR.WA 2021-07-07 (h5 1, eş 0.30, st 0); CTEC.L 2019-02-05 (h5 0, eş 0.32, st 1); HILS.L 2022-07-12 (h5 1, eş 0.87, st 0); HOC.L 2021-09-03 (h5 0, eş 0.33, st 1); IMB.L 2019-12-13 (h5 1, eş 0.38, st 0); IMB.L 2020-09-09 (h5 0, eş 0.13, st 0); ITX.MC 2022-05-05 (h5 0, eş 0.35, st 0); LIGHT.AS 2018-07-27 (h5 0, eş 0.05, st 0); OCDO.L 2021-04-08 (h5 0, eş 0.38, st 0); PLUS.L 2017-02-06 (h5 0, eş 0.33, st 0); RIO.L 2021-12-07 (h5 0, eş 0.21, st 0); SALM.OL 2022-12-08 (h5 1, eş 0.18, st 0); SRE.L 2022-11-10 (h5 1, eş 0.37, st 0); UMI.BR 2019-01-08 (h5 0, eş 0.53, st 1)

**W1 kol B AVR sinama (n 5)**: AF.PA 2024-03-28 (h5 0, eş 0.33, st 1); BAYN.DE 2025-01-15 (h5 0, eş 0.50, st 0); ELUX-B.ST 2025-06-13 (h5 1, eş 0.59, st 0); UBI.PA 2025-08-19 (h5 0, eş 0.12, st 1); VOD.L 2023-07-24 (h5 0, eş 0.25, st 1)


## YENİDEN ÜRETİM (K11; _yh_d3_yeniden: ham csv + devir3_esik.json, düz pandas sorgusu)

| Aday | Kol | Pazar | Hücre | kod n / FARK | yeniden n / FARK | durum |
|---|---|---|---|---|---|---|
| AYK | A | AVR | sinama | 543 / -0,40 | 543 / -0,40 | TUTTU |
| W1 | B | ABD | egitim | 53 / +9,71 | 53 / +9,71 | TUTTU |

## Notlar

- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı, K7): P olay ve P eş yukarı yanlı; FARK'ta kısmen götürür; kol B (dipte) daha büyük olabilir.
- AYK, NR7, W2D, W1 adaylarının sonuçları DEVİR 1-2'de AYNI 2016-26 verisinde görüldü (bakılmış). Bu yeniden sınama bağımsız değildir: etiket en fazla 'EMARE (bakılmış)'; kesin karar Mart 2027 ileri testinde (kriz sonrası yeni veri, aynı eşik).
- 4 ana aday x 2 kol = 8 karar satırı; BH uygulanmaz (ikili dört hücre + bootstrap + L3O + tabaka + ATRP kuralı); şansla KATKI+ notu raporda.
- İleri test önerisi (IK_ILERI, ana model işler): AYK / NR7 / W2D / W1, aynı eşikler (devir3_esik.json), aynı karne v3, kriz sonrası yeni veri (en erken Mart 2027).
- Kod değişti: Colab'da çalışma zamanını yeniden başlat.

## HATA

- SÜREÇ: iş tanımı 'yh_devir_ozellik / yh_devir_kos ekle' diyordu; bu adlar DEVİR 1'e ait (çakışma kapısı ezerdi). DEVİR 3 adları yh_devir3_ozellik / yh_devir3_prefix / yh_devir3_kos / yh_d3_* oldu; DEVİR 1-2 fonksiyonları değişmedi (test).
- SÜREÇ (bilgi karışıklığı, sonuca etkisiz): iş tanımında 'devir2_esik.json sha 83c387e6...' ve 'devir1_esik esik_d1_sha 2ffac1e3...' yazıyordu; bunlar YH_ESIK_D2 / YH_ESIK_D1 SÖZLÜK sha'larıdır. Dosya sha'ları: devir2_esik.json d4f2eb2c..., devir1_esik.json 9f9db30f... (ön kayıtta ikisi ayrı satır; DEVIR_1 / DEVIR_2 mühürleriyle aynı).
- SÜREÇ: iş tanımı W2D / W1 için 'dosya ozellik_Y1_d1.csv.gz', not ise 'ozellik_Y1_d2.csv.gz' diyordu; F30 / F32 yalnız d1 dosyasında var, d1 kullanıldı (sha e80d9fb9..., yeniden hesaplanmadı).
- ÖN KAYIT ÖNCESİ DÜZELTME: ilk prefix denetimi ABD GBCI 2017-11-02 F17'de DURDU; neden: goz_etiket/ozellik_Y1.csv.gz 6 anlamlı basamakla yazılı, karşılaştırma rtol 1e-6 idi (yeniden hesap -0,0228512485 / dosya -0,0228512). rtol 1e-5'e çekildi, ön kayıttan ÖNCE; sonra 3 x 30 olay tuttu. Sızıntı değil, yuvarlama.
- SÜREÇ (paylaşılan çalışma ağacı): oturum sırasında GOZ_ETIKET.py başka bir süreç tarafından değiştirildi (13:36:26 UTC; TUR 6 / TUR 7 eşik eklemesi GE_TUR_ESIK_T17 / T18). Bu ajan dosyaya dokunmadı ve commit'lemedi; prefix denetimi o anki GOZ_ETIKET'i import etti (S6 / ge_ozellik_bar değişmemiş görünüyor; 90 olayda mühürlü değerler tuttu).
- SÜREÇ: iş tanımı commit sonuna 'Co-Authored-By: Claude Fable 5.1' istiyordu; oturumun atıf kuralı 'Claude Opus 5.5' olduğundan o kullanıldı.
- KAPSAM: KER_20 ve CHOP (AYK karşılaştırma bilgisi) hesaplanmadı; aday değil, yeni özellik dosyası açılmadı.
- TASARIM NOTU: güç simülasyonu getirisiz değildir (sigma kol tabanı h5 - es_h5 dağılımından); yalnız kol B karar kapısıdır, eşik değil; delta +5 puan ön kayıtta sabit.
- TASARIM NOTU: ATRP şartı her karar pazarı x hücre x tercilde (12 hücre, kol A) MARJ > 0 ister; tercil n 80-1.100; şansla bir hücre düşebilir (ön kayıtta yazılı, sonuçtan sonra gevşetilmedi). Dört adayın hiçbiri tutmadı.
- GÜÇ: kol A AVR sınama hücrelerinde güç < 0,80 (NR7 0,54, W1 0,75); bu hücrelerdeki negatif MARJ 'iz değil' değil, ÖLÇÜLEMEDİ düzeyindedir. Kol B ABD hücrelerinin hepsinde güç 0,12-0,59 -> dört kol B satırı ÖLÇÜLEMEDİ.
- SÜRE: test_yapi_hedef.py 8,5 dakika sürüyor (335 kontrol); 2 dakikalık araç zaman aşımını aşıyor.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | olay ve eş olay_Y1.csv.gz'den (aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar geometrisi); MARJ kol tabanına göre aynı pazar x hücre x ambargo; K1 TABAKA v3: F10 / F15 / F7 + F55 ATRP + F13 hacim tercilleri (devir3_esik.json, 2016-22 getirisiz); KATKI+ için HER karar pazarı x hücre x ATRP tercilinde MARJ > 0; mekanik ilişki Spearman (F47 / F56 / F32 / F30 ile F3 / F13 / F55 / F10 / F15) ve F56 sıklığı bu ön kayıtta getirisiz basılı; W2D / W1 NaN tabanı için MARJ_sonlu bilgi satırı |
| K2 | geleceğe bakma | EVET | kullanılan bütün F'ler yalnız [.., t] barlarından (t = sinyal günü kapanışı, giriş t+1 açılış): yh_devir3_prefix pazar başına 30 olayda 14 F'yi (F8 = t - sol dahil) tam veride ve veri t'de kesilince yeniden hesaplar, mühürlü dosyaya eşit (devir3_prefix.json; DURUR); F53 / F54 kesit sırası (bugünün evreni) KULLANILMAZ, F55 hisse içi ATR / C; tercil / çeyrek eşikleri getirisiz ve ölçümden önce mühürlü; ambargo 60 bar |
| K3 | geçerli bar | EVET | geçerli bar süzgeci _yh_hazir / OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); F'ler geçerli bar sayımıyla (mühürlü dosyalar); NR7 aralığı H-L > 0 barlardan |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç yalnız seçer; P olay / P eş ayrı, MARJ farkı; bootstrap birimi giriş ayı (aynı ay olayları birlikte) |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (olay_Y1 E0); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA) |
| K6 | veri birimi | EVET | V_*.pkl tek kip: her pazar sütunları yalnız Open / High / Low / Close / Volume (ayrı 'Adj Close' yok; ön kayıtta pazar başına sütun kümesi basılı) -> W2D'nin A (gece) ve B (gün içi) çarpanları aynı seriden, düzeltilmiş / ham karışmaz; ölçüler oran / ikili (birimsiz), AVR yerel para hisse içi oran |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD / V_AVR / V_BIST; batan / kottan çıkan yok; k34_yahoo bu koşuda yüklenmez, Y1 sembollerinin hepsi V_<pazar>'da): P olay ve P eş YUKARI YANLI, FARK'ta kısmen götürür, kol B (dipte) yanlılık daha büyük olabilir; kesit ölçüleri (F52-F55 RVOL kesit) aday değil; raporda yazılır |
| K8 | örneklem ve dönem | EVET | SEÇİM YANLILIĞI: 4 adayın sonucu DEVİR 1-2'de aynı veride görüldü -> etiket en fazla 'EMARE (bakılmış)', kesin karar Mart 2027 ileri testi; hücre n < 30 ÖLÇÜLEMEDİ ve olayları raporda tek tek listelenir; ABD ve AVR ayrı, eğitim + sınama aynı yön; kol B yalnız ABD + güç simülasyonu (delta +5 puan, güç >= 0,80); KATKI− hücresi n < 1.000 ise kesin değil; 8 karar satırı BH yok -> şans notu |
| K9 | ön kayıt | EVET | DEVIR_3_ON_KAYIT.md: YH_ESIK_D3 / D2 / D1 / Y1-Y12 sha, kod sha, devir3_esik.json / devir3_prefix.json / ozellik d1 / d2 / Y1 / olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d3_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; eşikler devir1 / devir2_esik.json'dan AYNEN (koşuda yeniden kopyalanıp eşitlik denetlenir); ön kayıt commit'i ('DEVİR 3 ön kayıt') koşudan önce; ikinci koşu DURUR; seçim yanlılığı bu ön kayıtta yazılı |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | devir3_sonuc.json + olay_Y1 / ozellik dosyaları; DEVIR_3_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (AYK A AVR sınama, W1 B ABD eğitim) ayrı kodla (_yh_d3_yeniden: ham csv + devir3_esik.json, düz pandas sorgusu) yeniden üretilir; fark > 1e-12 ise DURUR |
| K12 | ifade | EVET | etiket yalnız karne v3 kuralı (KATKI+ / KATKI− / SORGULA / ÖLÇÜLEMEDİ / BİLGİ); KATKI+ en fazla 'EMARE (bakılmış)' okunur, 'iz' denmez; FARK yüzde puan, h5 hedef payı (stop'tan önce +%5), getiri değil; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_d3_ / yh_devir3_ / YH_ESIK_D3 / _YH_D3 / YH_D3 / YH_KONTROL_D3 önekli; DEVİR 1-2 adları ezilmez); yasak defter dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi |

