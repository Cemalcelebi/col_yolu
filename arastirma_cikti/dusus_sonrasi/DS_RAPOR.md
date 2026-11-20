# DÜŞÜŞ SONRASI — RAPOR (DS koşusu; 2026-11-20 11:31:42 UTC)

DUSUS_SONRASI v1.0 (2026-11-20): 25 sınıf I hipotez (DS_ELESTIRI bölüm 5), 15 bar cetveli, DS içi eş, karne v3 + BH q 0,10. Ön kayıt DS_ON_KAYIT.md (commit `5cc3cad198e665b2c26c1c8ce5904843601a3e23`, 2026-11-20T11:24:51+00:00); kapı 2026-11-20 11:24:59 UTC; süre 404.1 sn. FARK = hedef payı farkı (yüzde puan; h5 = 15 barda +%5 stop'tan önce), getiri değil. Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma: (+) yönlü özellikler lehine).

## 0. ÖZET

- Etiket dağılımı (25 hipotez): ÖLÇÜLEMEDİ 25.
- BH (q 0,10, m 25) geçen: yok.
- En küçük p_DS 5 hipotez: DS13 p 0,2571 q 1,000 (ÖLÇÜLEMEDİ); DS05 p 0,3141 q 1,000 (ÖLÇÜLEMEDİ); DS09 p 0,4153 q 1,000 (ÖLÇÜLEMEDİ); DS28 p 0,4486 q 1,000 (ÖLÇÜLEMEDİ); DS23 p 0,5702 q 1,000 (ÖLÇÜLEMEDİ).

## 1. HUNİ (ölçüm)

- ABD: DS günü 355057, havuz 261466, ANA 24899; egitim: ANA 14061, ölçülen 13741, açılış stop altı 320, h5 ort %51,0; sinama: ANA 10103, ölçülen 9673, açılış stop altı 277, h5 ort %50,0
- AVR: DS günü 75067, havuz 68534, ANA 6806; egitim: ANA 4562, ölçülen 4460, açılış stop altı 102, h5 ort %48,7; sinama: ANA 1928, ölçülen 1883, açılış stop altı 29, h5 ort %45,5
- BIST: DS günü 114105, havuz 102191, ANA 9494; egitim: ANA 2947, ölçülen 2846, açılış stop altı 101, h5 ort %44,6; sinama: ANA 5975, ölçülen 5716, açılış stop altı 109, h5 ort %47,3

## 2. SONUÇ TABLOSU (sınıf I; karar ABD + AVR, BIST bilgi)

Hücre: n / FARK / stop olay-eş (puan). boot = sınama ay kümeli %95 [alt, üst]; güç = sınama; p = pazar sınama p'si (önceden yazılı yön).

| DS | pazar | eğitim n / FARK / st olay-eş | sınama n / FARK / st olay-eş | sınama boot | güç e / s | p | p_DS / q | etiket |
|---|---|---|---|---|---|---|---|---|
| DS01 | ABD | 2392 / +2,0 / %47-%48 | 1422 / +0,5 / %45-%47 | [-3,0, +3,4] | 1,00 / 0,99 | 0,7745 | 0,7745 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS01 | AVR | 574 / +1,2 / %45-%48 | 123 / +2,6 / %37-%45 | [-7,6, +10,1] | 0,87 / 0,22 | 0,5577 |  |  |
| DS01 | BIST | 314 / +0,3 / %49-%47 | 658 / -4,2 / %49-%46 | [-7,6, -0,8] | 0,55 / 0,88 | 0,0257 |  | BİLGİ |
| DS04 | ABD | 1413 / -1,7 / %39-%38 | 964 / -0,9 / %44-%43 | [-4,4, +2,4] | 1,00 / 0,95 | 0,6216 | 0,6807 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS04 | AVR | 210 / -5,4 / %37-%32 | 80 / +2,6 / %31-%36 | [-9,6, +13,7] | 0,38 / 0,15 | 0,6807 |  |  |
| DS04 | BIST | 88 / -4,5 / %47-%40 | 56 / -1,5 / %46-%45 | [-16,4, +13,5] | 0,18 / 0,13 | 0,8611 |  | BİLGİ |
| DS02 | ABD | 1152 / +1,2 / %47-%46 | 790 / +0,2 / %48-%47 | [-3,4, +3,5] | 0,98 / 0,91 | 0,9258 | 0,9258 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS02 | AVR | 279 / +1,2 / %44-%45 | 85 / +2,4 / %44-%44 | [-5,0, +10,9] | 0,50 / 0,16 | 0,5322 |  |  |
| DS02 | BIST | 250 / -0,1 / %44-%44 | 183 / -1,4 / %39-%37 | [-8,9, +4,4] | 0,44 / 0,36 | 0,6856 |  | BİLGİ |
| DS03 | ABD | 1086 / -1,9 / %48-%47 | 1316 / -0,4 / %50-%50 | [-2,7, +2,1] | 0,98 / 0,99 | 0,6129 | 0,6340 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS03 | AVR | 249 / -5,9 / %43-%37 | 121 / -1,4 / %39-%41 | [-8,8, +6,1] | 0,48 / 0,20 | 0,6340 |  |  |
| DS03 | BIST | 104 / -7,9 / %62-%53 | 277 / +1,0 / %53-%53 | [-4,8, +6,3] | 0,20 / 0,51 | 0,3721 |  | BİLGİ |
| DS08 | ABD | 2691 / -1,6 / %43-%41 | 3224 / +0,5 / %42-%43 | [-2,4, +3,9] | 1,00 / 1,00 | 0,6384 | 1,0000 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS08 | AVR | 271 / +1,0 / %47-%48 | 13 / +18,7 / %8-%20 | [+4,1, +80,0] | 0,52 / 0,05 | 1,0000 |  |  |
| DS08 | BIST | 512 / -4,0 / %40-%41 | 1666 / -1,3 / %44-%43 | [-5,3, +2,2] | 0,83 / 1,00 | 0,2608 |  | BİLGİ |
| DS05 | ABD | 4716 / +1,1 / %44-%45 | 3905 / +0,4 / %43-%44 | [-1,2, +2,0] | 1,00 / 1,00 | 0,3141 | 0,3141 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS05 | AVR | 1185 / +1,4 / %42-%43 | 307 / +3,4 / %36-%41 | [-3,2, +11,0] | 1,00 / 0,51 | 0,1774 |  |  |
| DS05 | BIST | 516 / -1,1 / %45-%41 | 1086 / -0,8 / %45-%44 | [-3,3, +1,8] | 0,85 / 0,99 | 0,7236 |  | BİLGİ |
| DS06 | ABD | 321 / +2,3 / %50-%51 | 224 / +6,9 / %42-%49 | [+1,0, +12,9] | 0,59 / 0,38 | 0,0174 | 1,0000 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS06 | AVR | 72 / -4,7 / %43-%40 | 29 / -11,2 / %55-%47 | [-24,4, +3,4] | 0,17 / 0,08 | 0,9180 |  |  |
| DS06 | BIST | 42 / -13,8 / %71-%51 | 104 / -5,6 / %55-%48 | [-13,1, +2,5] | 0,11 / 0,21 | 0,9066 |  | BİLGİ |
| DS11 | ABD | 5393 / +1,3 / %47-%49 | 4342 / +0,4 / %49-%51 | [-1,8, +2,5] | 1,00 / 1,00 | 0,7038 | 0,7038 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS11 | AVR | 1046 / -1,0 / %49-%48 | 317 / +5,4 / %45-%50 | [-0,4, +10,6] | 0,99 / 0,53 | 0,1139 |  |  |
| DS11 | BIST | 578 / -7,1 / %51-%45 | 1793 / -1,8 / %54-%53 | [-4,1, +0,3] | 0,85 / 1,00 | 0,1024 |  | BİLGİ |
| DS09 | ABD | 2935 / +2,0 / %50-%52 | 2122 / +0,9 / %48-%50 | [-1,3, +3,1] | 1,00 / 1,00 | 0,4080 | 0,4153 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS09 | AVR | 840 / +0,8 / %55-%55 | 253 / +2,7 / %42-%48 | [-3,8, +8,5] | 0,96 / 0,45 | 0,4153 |  |  |
| DS09 | BIST | 464 / -3,0 / %53-%51 | 1123 / +0,5 / %53-%55 | [-2,3, +3,3] | 0,77 / 0,99 | 0,7201 |  | BİLGİ |
| DS14 | ABD | 71 / +12,8 / %31-%38 | 38 / +17,6 / %21-%38 | [+3,4, +33,5] | 0,16 / 0,10 | 0,0129 | 1,0000 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS14 | AVR | 10 / -33,1 / %60-%35 | 6 / -1,9 / %33-%32 | [-22,0, +20,4] | 0,05 / 0,04 | 0,5598 |  |  |
| DS14 | BIST | 12 / -20,4 / %33-%21 | 32 / -1,3 / %22-%24 | [-15,5, +17,2] | 0,06 / 0,10 | 0,5581 |  | BİLGİ |
| DS15 | ABD | 1 / -20,0 / %100-%40 | 0 / - / --- | [-, -] | 0,03 / 0,00 | - | 1,0000 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS15 | AVR | 0 / - / --- | 0 / - / --- | [-, -] | 0,00 / 0,00 | - |  |  |
| DS15 | BIST | 1 / -37,5 / %100-%38 | 2 / -20,0 / %0-%10 | [-40,0, +0,0] | 0,03 / 0,04 | 1,0000 |  | BİLGİ |
| DS16 | ABD | 1062 / +3,0 / %43-%46 | 1229 / -0,8 / %42-%44 | [-3,5, +1,7] | 0,98 / 0,99 | 0,7145 | 0,7145 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS16 | AVR | 252 / +2,7 / %44-%43 | 187 / +1,1 / %39-%44 | [-5,5, +8,3] | 0,48 / 0,31 | 0,3892 |  |  |
| DS16 | BIST | 95 / +6,5 / %45-%44 | 209 / -1,6 / %50-%49 | [-7,7, +4,0] | 0,20 / 0,42 | 0,7115 |  | BİLGİ |
| DS18 | ABD | 2628 / +0,1 / %43-%42 | 1732 / -1,6 / %42-%40 | [-4,5, +1,2] | 1,00 / 1,00 | 0,2878 | 0,6949 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS18 | AVR | 725 / +1,6 / %41-%43 | 163 / +1,5 / %30-%31 | [-7,0, +8,0] | 0,95 / 0,28 | 0,6949 |  |  |
| DS18 | BIST | 451 / +1,3 / %37-%38 | 1036 / -2,3 / %42-%41 | [-5,8, +1,1] | 0,74 / 0,98 | 0,1980 |  | BİLGİ |
| DS21 | ABD | 2473 / +0,6 / %45-%45 | 1668 / +0,2 / %40-%41 | [-3,4, +3,4] | 1,00 / 1,00 | 0,5521 | 0,7027 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS21 | AVR | 540 / +3,3 / %42-%45 | 145 / +3,0 / %32-%38 | [-8,7, +12,5] | 0,81 / 0,24 | 0,7027 |  |  |
| DS21 | BIST | 287 / -7,6 / %43-%39 | 500 / +0,9 / %39-%38 | [-1,9, +3,9] | 0,54 / 0,77 | 0,7417 |  | BİLGİ |
| DS22 | ABD | 109 / -2,5 / %42-%38 | 98 / +5,9 / %35-%38 | [-2,5, +13,8] | 0,22 / 0,19 | 0,0894 | 1,0000 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS22 | AVR | 21 / +4,9 / %24-%24 | 19 / +15,5 / %16-%27 | [-4,3, +33,6] | 0,08 / 0,06 | 0,0813 |  |  |
| DS22 | BIST | 22 / -10,9 / %45-%26 | 59 / -1,9 / %24-%22 | [-9,9, +3,7] | 0,08 / 0,15 | 0,7280 |  | BİLGİ |
| DS13 | ABD | 291 / -1,2 / %48-%48 | 213 / +2,2 / %46-%52 | [-3,9, +9,3] | 0,50 / 0,36 | 0,2571 | 0,2571 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS13 | AVR | 101 / -0,1 / %46-%43 | 32 / +11,4 / %38-%43 | [-3,1, +27,3] | 0,22 / 0,08 | 0,0820 |  |  |
| DS13 | BIST | 53 / +2,2 / %43-%42 | 176 / -2,0 / %55-%56 | [-9,7, +4,8] | 0,12 / 0,36 | 0,6916 |  | BİLGİ |
| DS12 | ABD | 955 / +0,5 / %42-%42 | 725 / -0,7 / %41-%42 | [-3,7, +2,4] | 0,96 / 0,83 | 0,6819 | 0,8418 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS12 | AVR | 223 / +3,1 / %35-%38 | 68 / -6,9 / %38-%31 | [-19,1, +7,1] | 0,42 / 0,13 | 0,8418 |  |  |
| DS12 | BIST | 146 / +3,2 / %37-%39 | 401 / -2,3 / %41-%38 | [-5,2, +1,1] | 0,28 / 0,66 | 0,9183 |  | BİLGİ |
| DS19 | ABD | 917 / +2,4 / %44-%45 | 706 / -2,9 / %46-%43 | [-6,4, +0,6] | 0,96 / 0,87 | 0,9424 | 0,9424 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS19 | AVR | 201 / -0,8 / %43-%41 | 78 / +5,6 / %32-%34 | [-6,6, +16,7] | 0,38 / 0,16 | 0,1779 |  |  |
| DS19 | BIST | 197 / -1,3 / %37-%39 | 234 / -0,5 / %44-%42 | [-6,7, +6,8] | 0,37 / 0,44 | 0,5482 |  | BİLGİ |
| DS20 | ABD | 3246 / +1,7 / %49-%51 | 2194 / +2,4 / %44-%48 | [+0,3, +4,8] | 1,00 / 1,00 | 0,9828 | 0,9828 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS20 | AVR | 774 / +1,5 / %46-%49 | 235 / +0,4 / %41-%44 | [-7,0, +6,3] | 0,97 / 0,42 | 0,5570 |  |  |
| DS20 | BIST | 443 / -0,9 / %44-%42 | 1039 / -3,1 / %48-%46 | [-7,6, +1,2] | 0,76 / 0,99 | 0,1049 |  | BİLGİ |
| DS17 | ABD | 3042 / -0,2 / %42-%44 | 2289 / -4,0 / %44-%44 | [-6,9, -1,1] | 1,00 / 1,00 | 0,9947 | 0,9947 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS17 | AVR | 763 / +1,0 / %43-%44 | 201 / +0,5 / %38-%39 | [-7,1, +8,6] | 0,94 / 0,32 | 0,4490 |  |  |
| DS17 | BIST | 467 / -2,1 / %43-%41 | 1166 / -2,8 / %44-%42 | [-5,7, -0,6] | 0,75 / 0,99 | 0,9854 |  | BİLGİ |
| DS07 | ABD | 390 / +4,1 / %42-%44 | 313 / +0,9 / %43-%43 | [-3,4, +5,6] | 0,63 / 0,50 | 0,3455 | 0,8505 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS07 | AVR | 101 / +4,9 / %41-%42 | 36 / -9,4 / %36-%30 | [-24,1, +8,4] | 0,22 / 0,09 | 0,8505 |  |  |
| DS07 | BIST | 41 / -7,5 / %54-%45 | 146 / -4,4 / %48-%42 | [-11,1, +3,7] | 0,11 / 0,29 | 0,8527 |  | BİLGİ |
| DS28 | ABD | 2208 / -1,2 / %47-%44 | 1577 / +1,0 / %44-%43 | [-1,4, +3,8] | 1,00 / 1,00 | 0,4486 | 0,4486 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS28 | AVR | 253 / -2,9 / %46-%40 | 77 / +12,1 / %35-%36 | [+3,7, +19,9] | 0,48 / 0,14 | 0,0110 |  |  |
| DS28 | BIST | 249 / -2,1 / %43-%41 | 554 / -1,2 / %42-%41 | [-5,2, +2,5] | 0,48 / 0,78 | 0,5641 |  | BİLGİ |
| DS10 | ABD | 3088 / +1,9 / %49-%51 | 2245 / -1,6 / %50-%50 | [-3,9, +0,4] | 1,00 / 1,00 | 0,1441 | 0,7804 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS10 | AVR | 950 / +1,7 / %47-%48 | 238 / -1,0 / %43-%46 | [-9,0, +5,4] | 0,98 / 0,40 | 0,7804 |  |  |
| DS10 | BIST | 371 / +1,4 / %47-%50 | 784 / -1,1 / %48-%48 | [-5,4, +2,8] | 0,63 / 0,94 | 0,5947 |  | BİLGİ |
| DS23 | ABD | 2231 / -0,7 / %48-%46 | 1811 / -0,1 / %44-%45 | [-1,9, +1,5] | 1,00 / 1,00 | 0,5702 | 0,5702 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS23 | AVR | 775 / +0,3 / %45-%46 | 270 / +5,7 / %37-%40 | [-0,5, +12,3] | 0,95 / 0,45 | 0,0523 |  |  |
| DS23 | BIST | 415 / -5,1 / %44-%41 | 1038 / -1,1 / %41-%40 | [-3,9, +1,6] | 0,66 / 0,99 | 0,7850 |  | BİLGİ |
| DS25 | ABD | 2321 / +0,2 / %42-%41 | 1724 / +2,2 / %39-%40 | [+0,6, +3,9] | 1,00 / 1,00 | 0,0083 | 0,6320 / 1,000 | **ÖLÇÜLEMEDİ** |
| DS25 | AVR | 538 / +1,0 / %36-%37 | 160 / -1,6 / %32-%28 | [-9,9, +6,8] | 0,81 / 0,27 | 0,6320 |  |  |
| DS25 | BIST | 286 / +5,0 / %33-%32 | 866 / -0,8 / %34-%32 | [-3,9, +2,2] | 0,50 / 0,98 | 0,7078 |  | BİLGİ |

Etiket kuralı: karne v3 (YH.yh_d3_etiket): karar hücreleri ABD eğitim / sınama, AVR eğitim / sınama; ÖLÇÜLEMEDİ = bir hücrede n < 30 ya da güç < 0,80; KATKI+ = her hücrede FARK > 0 VE boot %95 alt > 0 VE leave-3-out FARK > 0 VE st5 olay <= eş VE ATRP şartı (her karar pazarı x hücre x ATRP tercilinde FARK sonlu ve > 0); KATKI− = her hücrede FARK < 0 VE boot üst < 0; değilse SORGULA. ÇELİŞKİLİ (KATKI'dan önce): bir karar pazarında eğitim ve sınama boot aralıkları sıfırın ZIT taraflarında ya da ABD sınama ile AVR sınama zıt tarafta. SON ETİKET: KATKI+ / KATKI− yalnız BH (q 0,10, önceden yazılı yönlü p) geçerse; geçmezse 'SORGULA (BH)'. BIST ve sınıf II BİLGİ

ATRP tercil FARK'ı (sınama; T0 / T1 / T2, puan) ve L3O (sınama):

| DS | ABD T0 / T1 / T2 | AVR T0 / T1 / T2 | L3O ABD / AVR | ÇELİŞKİLİ | karne v3 |
|---|---|---|---|---|---|
| DS01 | +4,1 / -0,2 / -0,3 | +9,4 / -3,0 / +5,4 | -1,1 / -3,2 | - | ÖLÇÜLEMEDİ |
| DS04 | +3,5 / -0,8 / -3,0 | -11,3 / +5,9 / +18,0 | -2,8 / -5,9 | - | ÖLÇÜLEMEDİ |
| DS02 | +0,6 / -0,7 / +1,3 | +1,2 / +4,7 / +2,5 | -1,7 / -0,6 | - | ÖLÇÜLEMEDİ |
| DS03 | -2,7 / -2,0 / +1,7 | -4,1 / -1,4 / +1,7 | -1,6 / -6,7 | - | ÖLÇÜLEMEDİ |
| DS08 | +1,7 / +0,1 / +0,1 | +33,3 / +11,7 / +18,6 | -1,4 / +1,0 | - | ÖLÇÜLEMEDİ |
| DS05 | +0,2 / +0,0 / +1,6 | +1,5 / +7,1 / +4,0 | -0,3 / -1,3 | - | ÖLÇÜLEMEDİ |
| DS06 | -2,4 / +13,2 / +11,9 | -3,3 / -10,2 / -90,0 | +3,8 / -20,0 | - | ÖLÇÜLEMEDİ |
| DS11 | -1,3 / +1,7 / +1,9 | +5,0 / +4,5 / +9,5 | -0,9 / +1,4 | - | ÖLÇÜLEMEDİ |
| DS09 | +0,8 / +2,2 / -0,6 | +1,8 / -3,8 / +19,1 | -0,0 / -1,1 | - | ÖLÇÜLEMEDİ |
| DS14 | +15,3 / +16,5 / +24,7 | -1,9 / - / - | +9,5 / -26,2 | - | ÖLÇÜLEMEDİ |
| DS15 | - / - / - | - / - / - | - / - | - | ÖLÇÜLEMEDİ |
| DS16 | -2,1 / -0,6 / +4,3 | -4,3 / +9,8 / +22,2 | -2,4 / -2,6 | - | ÖLÇÜLEMEDİ |
| DS18 | -0,2 / -4,2 / -0,2 | -1,2 / +5,1 / +8,5 | -2,9 / -2,7 | - | ÖLÇÜLEMEDİ |
| DS21 | +2,7 / -2,8 / +1,0 | -2,2 / -0,4 / +37,5 | -1,9 / -3,1 | - | ÖLÇÜLEMEDİ |
| DS22 | +7,7 / +0,5 / +11,4 | +14,5 / +12,5 / +23,6 | +1,0 / +2,9 | - | ÖLÇÜLEMEDİ |
| DS13 | +5,3 / -0,4 / +1,9 | +10,5 / +15,0 / +6,2 | -1,8 / +1,9 | - | ÖLÇÜLEMEDİ |
| DS12 | -0,1 / -0,9 / -1,6 | +2,7 / -20,1 / -25,6 | -2,1 / -14,3 | - | ÖLÇÜLEMEDİ |
| DS19 | -2,7 / -1,0 / -6,8 | +9,2 / -1,3 / -0,4 | -4,3 / -1,2 | - | ÖLÇÜLEMEDİ |
| DS20 | +0,9 / +3,8 / +2,5 | +1,4 / -2,2 / +2,6 | +1,1 / -4,0 | - | ÖLÇÜLEMEDİ |
| DS17 | -4,6 / -2,2 / -5,1 | +4,4 / -5,0 / -9,1 | -5,5 / -3,6 | - | ÖLÇÜLEMEDİ |
| DS07 | +1,7 / -2,6 / +4,2 | -5,5 / -18,1 / -2,5 | -1,4 / -19,9 | - | ÖLÇÜLEMEDİ |
| DS28 | +2,6 / -1,3 / +2,7 | +19,5 / +2,5 / +17,6 | -0,4 / +8,2 | - | ÖLÇÜLEMEDİ |
| DS10 | -2,5 / -0,8 / -1,5 | -6,6 / -0,5 / +15,7 | -2,6 / -5,5 | - | ÖLÇÜLEMEDİ |
| DS23 | -0,0 / +0,3 / -2,8 | +6,0 / +6,2 / +2,9 | -0,9 / +2,0 | - | ÖLÇÜLEMEDİ |
| DS25 | +2,8 / +3,0 / +0,2 | +1,3 / -6,7 / +0,6 | +1,4 / -7,4 | - | ÖLÇÜLEMEDİ |

## 3. DS KÜMESİNİN KENDİSİ (BİLGİ)

| pazar | hücre | eş | n | h5 olay | h5 eş | FARK | boot [alt, üst] | st olay / eş |
|---|---|---|---|---|---|---|---|---|
| ABD | egitim | DS dışı eş (ATRP x likidite) | 13517 | %51,2 | %47,2 | +4,0 | [+2,1, +5,9] | %44,9 / %42,6 |
| ABD | egitim | OC eşi (momentum x likidite) | 13741 | %51,0 | %47,5 | +3,5 | [+2,5, +4,6] | %45,0 / %41,2 |
| ABD | sinama | DS dışı eş (ATRP x likidite) | 9658 | %50,0 | %47,0 | +3,0 | [+1,3, +4,6] | %44,5 / %41,1 |
| ABD | sinama | OC eşi (momentum x likidite) | 9673 | %50,0 | %46,2 | +3,8 | [+2,5, +5,2] | %44,5 / %40,7 |
| AVR | egitim | DS dışı eş (ATRP x likidite) | 4015 | %48,6 | %43,1 | +5,5 | [+2,9, +8,2] | %45,0 / %40,5 |
| AVR | egitim | OC eşi (momentum x likidite) | 4460 | %48,7 | %44,3 | +4,4 | [+3,0, +6,2] | %45,0 / %40,4 |
| AVR | sinama | DS dışı eş (ATRP x likidite) | 1668 | %45,1 | %38,2 | +6,9 | [+4,1, +10,2] | %42,3 / %35,7 |
| AVR | sinama | OC eşi (momentum x likidite) | 1883 | %45,5 | %38,3 | +7,2 | [+5,0, +10,0] | %42,7 / %35,4 |
| BIST | egitim | DS dışı eş (ATRP x likidite) | 2844 | %44,5 | %45,7 | -1,1 | [-3,2, +0,9] | %43,2 / %42,4 |
| BIST | egitim | OC eşi (momentum x likidite) | 2844 | %44,5 | %45,3 | -0,8 | [-2,2, +0,8] | %43,2 / %41,3 |
| BIST | sinama | DS dışı eş (ATRP x likidite) | 5701 | %47,3 | %48,9 | -1,6 | [-4,2, +1,5] | %45,5 / %43,6 |
| BIST | sinama | OC eşi (momentum x likidite) | 5716 | %47,3 | %48,3 | -1,0 | [-2,1, -0,0] | %45,5 / %43,6 |

## 4. SINIF II (ABD-olay, sec_ozet; BİLGİ, BH dışı)

| DS | yön | eğitim n / FARK | sınama n / FARK | sınama boot | p (sınama) | not |
|---|---|---|---|---|---|---|
| DS47 | + | 63 / +3,8 | 50 / +1,7 | [-9,0, +11,2] | 0,3752 |  |
| DS48 | - | 7 / +2,2 | 2689 / +0,5 | [-1,4, +2,4] | 0,6881 | 2023 öncesi kâğıt başvuru kapsamı eksik (DS_ELESTIRI HATA 10): eğitim hücresi yorumlanmaz |
| DS49 | + | 2708 / -0,3 | 2459 / +0,1 | [-2,3, +2,1] | 0,4790 |  |
| DS50 | ? | 833 / -1,0 | 514 / +0,6 | [-3,0, +4,4] | 0,7499 |  |
| DS51 | - | 46 / -4,2 | 18 / -2,3 | [-19,5, +12,9] | 0,3953 |  |
| DS52 | - | 163 / +7,2 | 117 / -2,5 | [-11,4, +6,8] | 0,2897 |  |
| DS53 | - | 286 / +0,5 | 194 / +2,9 | [-4,1, +10,1] | 0,7698 |  |
| DS44 | - | - | - | - | - | VERİ YOK (Yahoo not günlüğü / bilanço takvimi k67: /tmp, kalıcı değil) |
| DS45 | - | - | - | - | - | VERİ YOK (k67 not düşürme günlüğü) |
| DS46 | - | - | - | - | - | bu koşuda kapsam dışı (Form 4 k30; ana model kararı: sınıf II yalnız sec_ozet) |

## 5. OLASILIK TABLOSU (BİLGİ; 250 gün +%100 / -%50 dokunma, OC eşi KAT; 60 gün r60 eşli fark)

| pazar | dönem | n250 | P(+%100) olay / eş | KAT +%100 [alt, üst] | P(-%50) olay / eş | KAT -%50 [alt, üst] | r60 eşli fark ort / med |
|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | 14061 | %18,4 / %14,7 | 1,25 [1,15, 1,46] | %26,4 / %19,1 | 1,38 [1,30, 1,50] | -0,6 / -2,6 |
| ABD | 2023 | 2016 | %20,1 / %16,1 | 1,25 [1,12, 1,47] | %17,9 / %12,2 | 1,46 [1,29, 1,68] | -0,4 / -3,3 |
| ABD | 2024-26 | 4793 | %27,8 / %21,1 | 1,32 [1,20, 1,55] | %22,6 / %17,0 | 1,33 [1,23, 1,44] | +0,5 / -3,9 |
| AVR | 2016-22 | 4562 | %9,8 / %6,9 | 1,43 [1,23, 1,95] | %12,3 / %7,9 | 1,56 [1,43, 1,73] | +0,6 / +0,1 |
| AVR | 2023 | 389 | %4,9 / %2,5 | 1,93 [1,41, 3,05] | %14,7 / %7,8 | 1,88 [1,46, 2,57] | +0,5 / +0,5 |
| AVR | 2024-26 | 936 | %7,2 / %4,6 | 1,55 [1,30, 2,04] | %17,2 / %6,9 | 2,49 [2,14, 2,85] | -0,9 / -2,1 |
| BIST | 2016-22 | 2945 | %36,0 / %37,9 | 0,95 [0,91, 1,00] | %5,8 / %4,4 | 1,32 [1,15, 1,55] | -2,5 / -5,3 |
| BIST | 2023 | 1414 | %65,5 / %65,2 | 1,00 [0,98, 1,04] | %1,2 / %1,4 | 0,89 [0,60, 1,38] | -0,2 / -8,4 |
| BIST | 2024-26 | 2927 | %21,2 / %21,1 | 1,01 [0,91, 1,09] | %4,1 / %3,7 | 1,10 [0,96, 1,27] | -1,3 / -6,0 |

Özellik tutan / tutmayan (DS içi, sınama, havuzlu; aynı gün eşlemesi YOK, bilgi): P(+%100) ve P(-%50) oranları, r60 OC eşli fark ortalaması.

| DS | ABD tutan +100 / -50 / r60 | ABD tutmayan | AVR tutan | AVR tutmayan |
|---|---|---|---|---|
| DS01 | %32,4 / %22,2 / +2,3 (n 1128) | %24,1 / %21,0 / -0,1 (n 5681) | %7,3 / %15,6 / -0,0 (n 218) | %6,3 / %16,6 / -0,7 (n 1107) |
| DS04 | %35,7 / %22,5 / +2,5 (n 778) | %24,2 / %21,0 / -0,0 (n 6031) | %7,3 / %18,5 / -1,0 (n 124) | %6,4 / %16,2 / -0,6 (n 1201) |
| DS02 | %34,6 / %21,0 / +3,9 (n 462) | %24,7 / %21,2 / -0,1 (n 6312) | %5,6 / %21,5 / -0,6 (n 107) | %6,6 / %16,0 / -0,6 (n 1215) |
| DS03 | %33,1 / %29,1 / +1,9 (n 940) | %24,3 / %19,9 / -0,0 (n 5869) | %8,2 / %17,9 / +0,6 (n 195) | %6,2 / %16,2 / -0,8 (n 1130) |
| DS08 | %23,6 / %20,9 / -0,9 (n 5399) | %32,6 / %22,5 / +4,2 (n 1397) | %6,2 / %16,7 / -0,6 (n 1210) | %9,6 / %13,9 / -0,4 (n 115) |
| DS05 | %23,8 / %20,5 / -1,1 (n 3029) | %26,8 / %21,7 / +1,3 (n 3780) | %6,5 / %18,5 / +0,2 (n 664) | %6,5 / %14,4 / -1,4 (n 661) |
| DS06 | %28,5 / %25,5 / +0,1 (n 165) | %25,4 / %21,1 / +0,3 (n 6644) | %11,5 / %15,4 / +1,3 (n 26) | %6,4 / %16,5 / -0,6 (n 1299) |
| DS11 | %24,6 / %20,3 / +0,5 (n 3535) | %26,5 / %22,1 / -0,0 (n 3274) | %6,8 / %16,2 / +0,4 (n 718) | %6,1 / %16,8 / -1,8 (n 607) |
| DS09 | %22,1 / %19,3 / -0,9 (n 1569) | %26,5 / %21,8 / +0,6 (n 5240) | %5,8 / %13,9 / +0,6 (n 360) | %6,7 / %17,4 / -1,1 (n 965) |
| DS14 | %21,4 / %25,0 / -1,1 (n 28) | %25,5 / %21,2 / +0,3 (n 6781) | %0,0 / %11,1 / -7,1 (n 9) | %6,5 / %16,5 / -0,6 (n 1316) |
| DS15 | - / - / - (n 0) | %25,5 / %21,2 / +0,3 (n 6809) | %0,0 / %0,0 / -20,9 (n 1) | %6,5 / %16,5 / -0,6 (n 1324) |
| DS16 | %21,4 / %22,9 / -2,3 (n 869) | %26,1 / %20,9 / +0,7 (n 5940) | %5,1 / %24,5 / -0,8 (n 237) | %6,8 / %14,7 / -0,6 (n 1088) |
| DS18 | %27,3 / %22,4 / +1,0 (n 1333) | %25,1 / %20,9 / +0,1 (n 5476) | %7,6 / %14,4 / -1,5 (n 236) | %6,2 / %16,9 / -0,4 (n 1089) |
| DS21 | %28,8 / %16,8 / +2,2 (n 1379) | %24,3 / %22,0 / -0,5 (n 4128) | %4,6 / %16,2 / -0,3 (n 370) | %7,4 / %16,5 / +0,1 (n 715) |
| DS22 | %28,2 / %21,1 / -1,3 (n 71) | %25,5 / %21,2 / +0,3 (n 6738) | %6,2 / %6,2 / +3,1 (n 16) | %6,5 / %16,6 / -0,6 (n 1309) |
| DS13 | %26,5 / %18,4 / +2,1 (n 136) | %25,5 / %21,2 / +0,2 (n 6673) | %9,7 / %12,9 / -0,1 (n 31) | %6,4 / %16,5 / -0,6 (n 1294) |
| DS12 | %26,9 / %19,8 / +0,6 (n 494) | %25,4 / %21,3 / +0,2 (n 6315) | %5,8 / %18,6 / -1,7 (n 86) | %6,5 / %16,3 / -0,5 (n 1239) |
| DS19 | %21,5 / %21,1 / -2,1 (n 525) | %25,8 / %21,2 / +0,5 (n 6284) | %3,0 / %12,1 / -0,6 (n 99) | %6,8 / %16,8 / -0,6 (n 1226) |
| DS20 | %23,7 / %18,4 / -0,7 (n 1720) | %26,1 / %22,1 / +0,6 (n 5089) | %6,7 / %15,9 / -1,2 (n 402) | %6,4 / %16,7 / -0,3 (n 923) |
| DS17 | %16,6 / %18,1 / -4,1 (n 1639) | %28,3 / %22,2 / +1,7 (n 5170) | %6,3 / %15,1 / +0,9 (n 252) | %6,5 / %16,8 / -1,0 (n 1073) |
| DS07 | %26,6 / %17,5 / +0,4 (n 229) | %25,5 / %21,3 / +0,3 (n 6580) | %6,5 / %13,0 / -4,1 (n 46) | %6,5 / %16,6 / -0,5 (n 1279) |
| DS28 | %42,8 / %29,0 / +2,8 (n 1164) | %21,8 / %19,5 / -0,3 (n 5610) | %13,8 / %30,8 / +1,8 (n 130) | %5,7 / %14,9 / -0,9 (n 1192) |
| DS10 | %23,4 / %20,5 / -1,2 (n 1674) | %26,1 / %21,4 / +0,7 (n 5100) | %7,1 / %12,3 / +0,3 (n 350) | %6,3 / %18,0 / -0,9 (n 972) |
| DS23 | %18,2 / %19,5 / -1,7 (n 1377) | %27,3 / %21,6 / +0,7 (n 5432) | %7,3 / %16,2 / -0,8 (n 358) | %6,2 / %16,5 / -0,5 (n 967) |
| DS25 | %27,6 / %21,7 / -0,2 (n 1242) | %25,0 / %21,1 / +0,4 (n 5567) | %6,8 / %18,1 / -1,1 (n 249) | %6,4 / %16,1 / -0,5 (n 1076) |

## 6. YENİDEN ÜRETİM (K11)

- DS01 ABD sinama: kod n 1422 / FARK 0,004741; ds_olay.csv.gz düz pandas n 1422 / FARK 0,004741 -> TUTTU.
- DS09 AVR egitim: kod n 840 / FARK 0,007677; ds_olay.csv.gz düz pandas n 840 / FARK 0,007677 -> TUTTU.
- Bağımsız döngüyle h5 / st5 yeniden simülasyonu: 50 rastgele olay, bozuk 0.

## 7. n < 30 KARAR HÜCRELERİ (olaylar ds_sonuc.json 'kucuk')

- DS08 AVR sinama n 13; DS06 AVR sinama n 29; DS14 AVR egitim n 10; DS14 AVR sinama n 6; DS15 ABD egitim n 1; DS22 AVR egitim n 21; DS22 AVR sinama n 19.

## HATA

(ana model IK_HATA'ya işler; alt ajan KOL F, koşudan sonra elle eklendi; sayılar ds_sonuc.json / DS_ON_KAYIT.md)

1. PREFIX (geleceğe bakma, ön kayıttan önce yakalandı): ilk ön kayıt denemesinde 90 olaydan 2'si tutmadı (ABD PCVX 2020-12-03, BIST KLSER 2024-01-23; 'satır yok'). Neden: ds_ozellik_hisse uzunluk koruması N < 125 idi; serinin toplam uzunluğu (veri sonu) 120-124 bar iken DS günü üretmiyordu. N < 120 yapıldı (DS (a)/(b) zaten 120 bar ister); sonuç görülmeden, ön kayıt commit'inden önce. İkinci ön kayıt: 90 / 90 tuttu.
2. VERİ / SÜREÇ: CLAUDE.md'nin andığı evren_disi_ABD.csv ne repoda ne origin/main'de var; OC.oc_veri yalnız K55_EVREN_DISI.csv 'fon_evren_disi' satırlarını uyguladı, V_ABD'den 0 hisse çıktı.
3. VERİ: V_AVR açılış H-L dışı satır sayısı envanterde 13.622, OC geçerli bar süzgeci + kriz kesiği sonrası 2.932 (314 hisse); bunlar kırpıldı, DS21 penceresinde NaN. Fark (ham ↔ temiz) envanterde açıklanmalı.
4. TASARIM / GÜÇ: 25 hipotezin 25'i ÖLÇÜLEMEDİ çıktı; ortak neden AVR sınama hücresinin küçüklüğü (AVR sınama ANA 1.928, ölçülen 1.883; tutan alt kümeler n 6-317) ve güç < 0,80 (delta +5 puan). ABD hücrelerinin çoğunda güç >= 0,80. Ön kayıtta getirisiz huni AVR sınama tutan sayılarını gösteriyordu ama güç (sigma getiriden) ön kayıtta hesaplanmadı: bu sonucun önceden kestirilebilir olduğu ön kayda yazılmalıydı. Karar AVR verisi büyüyünce (ileri test) verilebilir.
5. K1 BOŞ KÜME: DS15 (busted, S6 tabanı) DS olay tanımıyla neredeyse olanaksız (6 tutan olay, üç pazar iki dönem toplam); C_t > kutu_ust ile F15 <= 0,25 çakışıyor. DS_ELESTIRI süzgecinde (g) yakalanmadı (DS31 ile aynı tür).
6. K1 EŞ AZLIĞI: DS08 (evre 4) AVR'de DS olaylarının %90'ı: sınama tutan 1.737, tutmayan eşi >= 3 olan tutan yalnız 17 (huni), ölçülen n 13. DS_ELESTIRI HATA 12 öngörmüştü.
7. ÖLÇÜ KARARSIZLIĞI: DS21 GECE_PAY oranı 20 gün toplam log getiri sıfıra yakınken aşırı değer alıyor (ör. -2,8e15); ikili eşik (q75) olduğu için sonuç etkilenmez, ölçü tanımı payda alt sınırı gerektirir.
8. KOD BAKIMI: pandas 4 uyarısı (DataFrame.mean(1) / sum(1) konumsal argüman, ds_baglam); ön kayıt kod sha'sı korunsun diye değiştirilmedi.
9. SÜREÇ: ilk iki arka plan işi (test + ön kayıt) oturum kesintisinde öldürüldü, nohup ile yeniden koşuldu; sınama sonucu hiçbir koşuda ön kayıt commit'inden (5cc3cad, 11:24:51 UTC) önce hesaplanmadı (test yalnız sentetik veri).

Önceden yazılı yönün TERSİNE belirgin çıkan ABD hücreleri (bilgi, iddia değil): DS17 (beklenen +) ABD sınama FARK -4,0 puan, boot [-6,9; -1,1], BIST sınama -2,8 [-5,7; -0,6], AVR +0,5; DS20 (beklenen -) ABD sınama +2,4 [+0,3; +4,8], AVR +0,4. İkisi de AVR'de güçsüz.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü), DS kümesi içi, özelliği tutmayan; eşler olayın stop uzaklığı d ile aynı 15 bar kuralıyla (yh_sim, aynı giriş / çıkış geometrisi); mekanik üstünlük: DS30 / DS31 / DS34 havuzda elendi, DS08 / DS20 / DS28 için tutan / tutmayan sayıları getirisiz huni'de; DS dışı eş ve OC eşi bilgi satırı |
| K2 | geleceğe bakma | EVET | bütün ham özellikler yalnız [.., t] barlarından (pivotlar 6/6 onayı p + 6 <= t); ds_prefix.json pazar başına 30 olayda veri t'de kesilince eşit (DURUR); sınıf II olaylar başvuru günü + 1 işlem günü <= t; eşikler eğitim olaylarından getirisiz; sektör sınıfı bugünkü (DS03 notu); evren endeksi aynı gün getirilerinin ortalaması |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği; açılış H-L dışı bar kırpılır (sayı huni'de, DS21 NaN); 15 bar yalnız geçerli barlarla (yh_sim); sinyal günü geçerli bar |
| K4 | tekilleştirme | EVET | ANA = hisse başına ilk DS günü, sonraki >= 15 birleşik takvim günü sonra (oc_olay_hazirla sonrası); n = ANA olay; bootstrap / permütasyon birimi giriş ayı; ortalama yanında h5 / getiri medyanı raporda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla d; YH.yh_sim satır 0); açılış stop'un altındaysa olay ölçülmez (sayım) |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur (EUR); geçmiş bölünme şüphesi [d-61, d-1] havuz dışı (DS04 -%15 günleri bölünme hatası olamaz: OC sup_gecmis); AVR açılış temizliği |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST 581; k34 yüklenmez): (+) yönlü özellikler lehine, (−) yönlüler aleyhine yanlı; DS içi eş FARK'ta kısmen götürür; raporda yazılır |
| K8 | örneklem ve dönem | EVET | ABD ve AVR ayrı, eğitim + sınama; n < 30 ÖLÇÜLEMEDİ ve olayları ds_sonuc.json 'kucuk' listesinde; güç < 0,80 ÖLÇÜLEMEDİ; BH q 0,10 m = 25 sabit; aynı aileden (DS01 / DS09 / DS10 / DS11; DS05 / DS16) birden fazla geçen tek bulgu sayılır |
| K9 | ön kayıt | EVET | DS_ON_KAYIT.md: DS_ESIK sha, ds_esik.json (eğitim eşikleri SAYI), ds_prefix.json, kod sha'ları, girdi sha'ları, getirisiz huni; ds_kos kapısı sha + git (işlenmiş ve değişmemiş) + ik_kontrol_kapisi denetler, eşikleri yeniden hesaplayıp json ile eşitler; ön kayıt commit'i koşudan önce; ikinci koşu DURUR |
| K10 | ayrıştırma | EVET | sınıf I yalnız OHLCV (UYGULANMAZ); sınıf II sec_ozet: form adları 'SC 13G' + 'SCHEDULE 13G' birlikte, 8-K madde kodu virgülle ayrılmış alan, başvuru günü + 1 işlem günü; ham sec_ozet'ten 3 satır ön kayıtta elle gösterildi |
| K11 | yeniden üretim | EVET | ds_olay.csv.gz satır dosyası; DS_RAPOR.md YENİDEN ÜRETİM iki hücre (DS01 ABD sınama, DS09 AVR eğitim) düz pandas ile + 50 rastgele olayın h5'i bağımsız döngüyle yeniden simüle; fark > 1e-12 DURUR |
| K12 | ifade | EVET | etiket yalnız karne v3 + BH kuralıyla; 'iz / emare / anlamlı' yazılmaz; FARK yüzde puan h5 (stop'tan önce +%5 payı), getiri değil; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_ds; ds_ / DS_ önekli adlar dışında ezme DURUR; test_dusus_sonrasi); yasak defter dosyalarına ve YAPI_HEDEF.py'ye dokunulmadı (git diff); e-posta / anahtar taraması (YH._yh_yaz); dış servis yok; kod değişti -> 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

Kod değişti: Colab'da çalışma zamanını yeniden başlat.
