# COL KAZANC — DOGRULAMA: kucuk alim mumu izi (alim_mum_kat < 1.5)   (COL_KAZANC v1.2 (2026-10-21, K8 birikim: NVI / CMF / A-D ayrismasi), 2026-10-21 14:08)

Soru (Cemal 21 Eki): 'alim mumu kucuk olsun' sarti gercek iz mi, yoksa volatilite / fiyat / likidite / cok test artefakti mi?
Fark = kucuk mum islemlerinin ort getirisi (%200 kirpili) - geri kalanin ort getirisi (puan). p = Welch, normal yaklasim. Slot = 30 slot portfoy.

## 1. Donem x pazar fark, esik duyarliligi (obek islemleri; parantez icinde TABAN kutulari)

| esik | donem | n kucuk / n diger | fark ort | kazanan fark | p | slot kucuk / hepsi | TABAN fark (p) |
|---|---|---|---|---|---|---|---|
| 1.2 | 2016-19 | 1814 / 8505 | +2.19 | +5.7 | 0.001 | +102% / +93% | +1.33 (0.006) |
| 1.2 | 2020-22 | 3491 / 14014 | +2.62 | +7.0 | 0.000 | +260% / +231% | +2.06 (0.000) |
| 1.2 | 2023 | 1117 / 3857 | +4.71 | +3.0 | 0.002 | +107% / +124% | +3.02 (0.000) |
| 1.2 | 2024-26 | 3953 / 13255 | +2.54 | +6.9 | 0.000 | +121% / +180% | +1.83 (0.000) |
| 1.2 | ABD 2022-23 | 8472 / 14624 | -0.08 | -0.9 | 0.719 | -2% / -6% | -0.73 (0.000) |
| 1.2 | ABD 2024-26 | 15934 / 32002 | -0.09 | +0.5 | 0.608 | +16% / +40% | +0.17 (0.157) |
| 1.5 | 2016-19 | 3137 / 7182 | +1.98 | +6.1 | 0.000 | +151% / +93% | +0.49 (0.245) |
| 1.5 | 2020-22 | 5992 / 11513 | +1.81 | +3.5 | 0.000 | +319% / +231% | +1.76 (0.000) |
| 1.5 | 2023 | 1951 / 3023 | +2.92 | +2.2 | 0.020 | +139% / +124% | +1.14 (0.106) |
| 1.5 | 2024-26 | 6678 / 10530 | +1.45 | +5.9 | 0.000 | +135% / +180% | +1.47 (0.000) |
| 1.5 | ABD 2022-23 | 12974 / 10122 | -0.58 | -2.0 | 0.006 | -7% / -6% | -1.09 (0.000) |
| 1.5 | ABD 2024-26 | 25386 / 22550 | +0.03 | +0.5 | 0.881 | -0% / +40% | +0.08 (0.530) |
| 2.0 | 2016-19 | 5140 / 5179 | +0.81 | +4.3 | 0.120 | +138% / +93% | +0.38 (0.344) |
| 2.0 | 2020-22 | 9997 / 7508 | +2.02 | +2.5 | 0.000 | +338% / +231% | +1.17 (0.002) |
| 2.0 | 2023 | 3271 / 1703 | +1.19 | +3.2 | 0.342 | +139% / +124% | -1.10 (0.211) |
| 2.0 | 2024-26 | 10637 / 6571 | +1.45 | +6.7 | 0.000 | +135% / +180% | +1.46 (0.000) |
| 2.0 | ABD 2022-23 | 18069 / 5027 | -0.88 | -3.0 | 0.001 | +1% / -6% | -1.50 (0.000) |
| 2.0 | ABD 2024-26 | 35918 / 12018 | -0.33 | -0.0 | 0.122 | +14% / +40% | +0.06 (0.700) |
| 3.0 | 2016-19 | 7594 / 2725 | +1.67 | +4.9 | 0.006 | +120% / +93% | +1.00 (0.032) |
| 3.0 | 2020-22 | 15151 / 2354 | +1.70 | +3.1 | 0.012 | +271% / +231% | +1.34 (0.014) |
| 3.0 | 2023 | 4723 / 251 | +8.05 | +13.4 | 0.001 | +117% / +124% | -4.77 (0.023) |
| 3.0 | 2024-26 | 15220 / 1988 | +1.13 | +6.2 | 0.060 | +168% / +180% | +1.37 (0.001) |
| 3.0 | ABD 2022-23 | 21498 / 1598 | -0.73 | -3.8 | 0.127 | -2% / -6% | -1.37 (0.001) |
| 3.0 | ABD 2024-26 | 43878 / 4058 | -0.76 | -1.1 | 0.036 | +13% / +40% | -0.25 (0.360) |

### Coklu test duzeltmesi

Tarama: 99 kova (olcu x kova), 594 kova x donem hucresi. Bonferroni esigi 0,05/99 = 0.00051 (kova) ve 0,05/594 = 0.000084 (hucre).

- BIST havuz (tum donemler): n 17758 / 32248, fark +1.76, p = 5.53e-10 -> Bonferroni(kova) GECER, Bonferroni(hucre) GECER
- ABD havuz (tum donemler): n 38360 / 32672, fark -0.22, p = 1.17e-01 -> Bonferroni(kova) GECMEZ, Bonferroni(hucre) GECMEZ
- BH-FDR (q < 0,10) ile ayakta kalan hucre: 358 / 594; kucuk mum hucreleri: 2016-19 q=0.00, 2020-22 q=0.00, 2023 q=0.04, 2024-26 q=0.00, ABD 2022-23 q=0.01, ABD 2024-26 q=0.90

## 2. Kaynak ayristirma — kova icinde kucuk vs buyuk mum farki (pazar havuzu, obek)

### BIST — fiyat

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| 20-50 | 2540 / 3908 | +6.41 | +5.76 | +0.64 | 0.363 | %36 / %34 |
| 5-20 | 4953 / 8722 | +8.62 | +7.45 | +1.17 | 0.025 | %40 / %37 |
| 50-100 | 1113 / 1526 | +10.07 | +7.52 | +2.56 | 0.036 | %41 / %37 |
| <5 | 7616 / 15469 | +12.54 | +9.39 | +3.14 | 0.000 | %46 / %38 |
| >100 | 1536 / 2623 | +5.93 | +6.23 | -0.30 | 0.730 | %37 / %35 |

### BIST — likidite (lik60 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 2584 / 7418 | +14.24 | +8.47 | +5.77 | 0.000 | %45 / %36 |
| Q2 | 3318 / 6683 | +14.16 | +12.36 | +1.80 | 0.014 | %47 / %41 |
| Q3 | 3621 / 6380 | +10.70 | +8.57 | +2.13 | 0.001 | %44 / %38 |
| Q4 | 3770 / 6231 | +6.87 | +5.30 | +1.57 | 0.009 | %36 / %33 |
| Q5 | 4465 / 5536 | +5.90 | +4.97 | +0.93 | 0.065 | %38 / %36 |

### BIST — volatilite (vol20 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 4764 / 5238 | +8.17 | +7.51 | +0.66 | 0.194 | %40 / %40 |
| Q2 | 4050 / 5951 | +7.65 | +7.72 | -0.07 | 0.892 | %40 / %37 |
| Q3 | 3305 / 6696 | +10.79 | +8.80 | +1.99 | 0.002 | %43 / %38 |
| Q4 | 2766 / 7235 | +14.07 | +7.87 | +6.21 | 0.000 | %48 / %37 |
| Q5 | 2873 / 7128 | +10.54 | +8.35 | +2.18 | 0.009 | %37 / %33 |

### BIST — ATR% (atr20_pct besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 4079 / 5923 | +7.85 | +7.66 | +0.19 | 0.721 | %40 / %40 |
| Q2 | 3637 / 6364 | +6.61 | +7.26 | -0.65 | 0.205 | %39 / %38 |
| Q3 | 3281 / 6720 | +9.12 | +7.78 | +1.34 | 0.023 | %44 / %36 |
| Q4 | 3228 / 6773 | +13.55 | +8.76 | +4.79 | 0.000 | %46 / %36 |
| Q5 | 3533 / 6468 | +12.76 | +8.89 | +3.87 | 0.000 | %40 / %35 |

### BIST — iki yonlu: kucuk mum x fiyat (ort getiri, n)

| kucuk | 20-50 | 5-20 | 50-100 | <5 | >100 |
|---|---|---|---|---|---|
| buyuk | +5.8 (n3908) | +7.5 (n8722) | +7.5 (n1526) | +9.4 (n15469) | +6.2 (n2623) |
| kucuk | +6.4 (n2540) | +8.6 (n4953) | +10.1 (n1113) | +12.5 (n7616) | +5.9 (n1536) |

### BIST — iki yonlu: kucuk mum x likidite (ort getiri, n)

| kucuk | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| buyuk | +8.5 (n7418) | +12.4 (n6683) | +8.6 (n6380) | +5.3 (n6231) | +5.0 (n5536) |
| kucuk | +14.2 (n2584) | +14.2 (n3318) | +10.7 (n3621) | +6.9 (n3770) | +5.9 (n4465) |

### BIST — iki yonlu: kucuk mum x RVOL (alim hacmi / obek medyan hacmi): ort getiri (n, kazanan)

| kucuk | <1 | 1-2 | 2-4 | >=4 |
|---|---|---|---|---|
| kucuk | +12.3 (n3571, %44) | +9.7 (n9578, %42) | +8.7 (n3964, %39) | +6.3 (n645, %36) |
| buyuk | +12.7 (n929, %43) | +8.6 (n7743, %38) | +8.5 (n13424, %38) | +6.8 (n10150, %34) |

### ABD — fiyat

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| 20-50 | 10125 / 8274 | -0.05 | +0.31 | -0.36 | 0.131 | %27 / %27 |
| 5-20 | 9841 / 9618 | +0.75 | +1.07 | -0.32 | 0.277 | %27 / %27 |
| 50-100 | 7728 / 5649 | +1.32 | +0.61 | +0.71 | 0.009 | %31 / %30 |
| <5 | 1879 / 2690 | +5.40 | +6.47 | -1.07 | 0.256 | %31 / %31 |
| >100 | 8787 / 6441 | +0.39 | -0.09 | +0.47 | 0.037 | %29 / %30 |

### ABD — likidite (lik60 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 6527 / 7680 | +1.82 | +2.67 | -0.86 | 0.043 | %26 / %27 |
| Q2 | 7567 / 6639 | +0.43 | +0.01 | +0.42 | 0.155 | %28 / %27 |
| Q3 | 7830 / 6376 | -0.16 | +0.80 | -0.96 | 0.000 | %27 / %28 |
| Q4 | 8123 / 6083 | +0.87 | +0.12 | +0.75 | 0.002 | %30 / %29 |
| Q5 | 8313 / 5894 | +1.16 | +1.14 | +0.02 | 0.933 | %30 / %32 |

### ABD — volatilite (vol20 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 9510 / 4697 | +0.21 | +0.23 | -0.02 | 0.933 | %30 / %32 |
| Q2 | 8376 / 5830 | -0.57 | -0.46 | -0.10 | 0.637 | %25 / %27 |
| Q3 | 7872 / 6334 | +0.42 | +0.71 | -0.30 | 0.285 | %27 / %28 |
| Q4 | 7107 / 7099 | +1.57 | +0.92 | +0.65 | 0.049 | %30 / %29 |
| Q5 | 5495 / 8712 | +3.44 | +2.72 | +0.72 | 0.124 | %29 / %29 |

### ABD — ATR% (atr20_pct besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 8738 / 5469 | +0.03 | +0.25 | -0.21 | 0.271 | %29 / %32 |
| Q2 | 8312 / 5894 | -0.16 | -0.15 | -0.01 | 0.972 | %26 / %27 |
| Q3 | 7754 / 6452 | -0.05 | +0.43 | -0.48 | 0.072 | %26 / %28 |
| Q4 | 7261 / 6945 | +1.35 | +0.98 | +0.37 | 0.230 | %31 / %29 |
| Q5 | 6295 / 7912 | +3.51 | +2.91 | +0.60 | 0.207 | %29 / %28 |

### ABD — iki yonlu: kucuk mum x fiyat (ort getiri, n)

| kucuk | 20-50 | 5-20 | 50-100 | <5 | >100 |
|---|---|---|---|---|---|
| buyuk | +0.3 (n8274) | +1.1 (n9618) | +0.6 (n5649) | +6.5 (n2690) | -0.1 (n6441) |
| kucuk | -0.1 (n10125) | +0.7 (n9841) | +1.3 (n7728) | +5.4 (n1879) | +0.4 (n8787) |

### ABD — iki yonlu: kucuk mum x likidite (ort getiri, n)

| kucuk | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| buyuk | +2.7 (n7680) | +0.0 (n6639) | +0.8 (n6376) | +0.1 (n6083) | +1.1 (n5894) |
| kucuk | +1.8 (n6527) | +0.4 (n7567) | -0.2 (n7830) | +0.9 (n8123) | +1.2 (n8313) |

### ABD — iki yonlu: kucuk mum x RVOL (alim hacmi / obek medyan hacmi): ort getiri (n, kazanan)

| kucuk | <1 | 1-2 | 2-4 | >=4 |
|---|---|---|---|---|
| kucuk | +0.5 (n15515, %28) | +0.9 (n20360, %28) | +2.5 (n2249, %29) | -0.1 (n236, %34) |
| buyuk | +0.9 (n3378, %29) | +0.8 (n17493, %29) | +0.7 (n8427, %27) | +2.9 (n3373, %32) |

### OLS: getiri ~ kucuk + log fiyat + log lik60 + vol20 + w + bekleme + piyasa60 + donem kuklalari (HC0 SE)

| pazar | n | kucuk katsayi | SE | t | kazanan modeli (LPM) kucuk katsayi | t | + log RVOL kontrolu: kucuk | log RVOL katsayisi |
|---|---|---|---|---|---|---|---|---|
| BIST | 50006 | +1.952 | 0.289 | +6.76 | +0.0404 | +8.72 | -0.055 (t -0.17) | -3.242 (t -13.86) |
| ABD | 71032 | +0.127 | 0.140 | +0.91 | -0.0067 | -1.94 | +0.148 (t +0.97) | +0.087 (t +0.53) |

Okuma: kucuk katsayisi, fiyat/likidite/volatilite/donem kontrolunden sonra |t| >= 2 ile ayni isarette kaliyorsa iz kendi basina; kayboluyorsa proxy.
Son iki sutun: alim gunu goreli hacmi (RVOL = alim hacmi / obek medyan hacmi) modele girince kucuk katsayisi sifira iniyorsa, kucuk mum dusuk hacmin vekilidir (iz hacimdedir, mum boyunda degil).

## 3-4. Normalizasyon (mum/ATR20) ve desil monotonlugu (obek, pazar havuzu)

### BIST — alim_mum_kat desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.87

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.94 | 5001 | +11.66 | -0.40 | %44 |
| D2 | <1.18 | 5001 | +9.89 | -0.40 | %43 |
| D3 | <1.39 | 5000 | +8.33 | -0.40 | %39 |
| D4 | <1.59 | 5001 | +8.54 | -0.40 | %39 |
| D5 | <1.81 | 5000 | +8.70 | -0.40 | %39 |
| D6 | <2.04 | 5001 | +9.10 | -0.40 | %39 |
| D7 | <2.33 | 5000 | +8.20 | -0.40 | %38 |
| D8 | <2.71 | 5001 | +8.04 | -0.40 | %36 |
| D9 | <3.36 | 5000 | +8.18 | -0.40 | %36 |
| D10 | >=3.36 | 5001 | +6.44 | -0.40 | %33 |

### BIST — alim_mum_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.53

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.86 | 5001 | +11.28 | -0.40 | %43 |
| D2 | <1.06 | 5001 | +8.79 | -0.40 | %41 |
| D3 | <1.24 | 5000 | +9.14 | -0.40 | %40 |
| D4 | <1.41 | 5001 | +8.56 | -0.40 | %39 |
| D5 | <1.58 | 5000 | +7.68 | -0.40 | %38 |
| D6 | <1.77 | 5001 | +8.28 | -0.40 | %38 |
| D7 | <1.98 | 5000 | +8.72 | -0.40 | %38 |
| D8 | <2.25 | 5001 | +8.65 | -0.40 | %38 |
| D9 | <2.71 | 5000 | +8.94 | -0.40 | %38 |
| D10 | >=2.71 | 5001 | +7.04 | -0.40 | %33 |

### BIST — govde_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.84

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.32 | 5001 | +10.18 | -0.40 | %42 |
| D2 | <0.51 | 5001 | +10.32 | -0.40 | %42 |
| D3 | <0.67 | 5000 | +8.71 | -0.40 | %39 |
| D4 | <0.82 | 5001 | +8.91 | -0.40 | %39 |
| D5 | <0.99 | 5000 | +10.04 | -0.40 | %41 |
| D6 | <1.17 | 5001 | +7.91 | -0.40 | %37 |
| D7 | <1.38 | 5000 | +6.97 | -0.40 | %38 |
| D8 | <1.67 | 5001 | +8.69 | -0.40 | %38 |
| D9 | <2.10 | 5000 | +7.73 | -0.40 | %35 |
| D10 | >=2.10 | 5001 | +7.62 | -0.40 | %33 |

### ABD — alim_mum_kat desilleri (D1 en kucuk mum). Spearman(desil, ort) = +0.36

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.83 | 7104 | +0.91 | -0.40 | %29 |
| D2 | <0.99 | 7103 | +0.99 | -0.40 | %29 |
| D3 | <1.14 | 7103 | +0.55 | -0.40 | %28 |
| D4 | <1.28 | 7103 | +0.89 | -0.40 | %28 |
| D5 | <1.43 | 7103 | +0.72 | -0.40 | %28 |
| D6 | <1.60 | 7103 | +0.51 | -0.40 | %28 |
| D7 | <1.83 | 7103 | +0.49 | -0.40 | %28 |
| D8 | <2.14 | 7103 | +1.26 | -0.40 | %29 |
| D9 | <2.77 | 7103 | +1.04 | -0.40 | %29 |
| D10 | >=2.77 | 7104 | +1.62 | -0.40 | %30 |

### ABD — alim_mum_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = +0.27

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.72 | 7104 | +1.19 | -0.40 | %29 |
| D2 | <0.86 | 7103 | +0.82 | -0.40 | %29 |
| D3 | <0.98 | 7103 | +0.59 | -0.40 | %28 |
| D4 | <1.10 | 7103 | +0.30 | -0.40 | %27 |
| D5 | <1.22 | 7103 | +0.88 | -0.40 | %28 |
| D6 | <1.36 | 7103 | +0.86 | -0.40 | %28 |
| D7 | <1.53 | 7103 | +0.86 | -0.40 | %28 |
| D8 | <1.77 | 7103 | +1.41 | -0.40 | %29 |
| D9 | <2.21 | 7103 | +0.35 | -0.40 | %28 |
| D10 | >=2.21 | 7104 | +1.70 | -0.40 | %30 |

### ABD — govde_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = +0.08

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.23 | 7104 | +1.37 | -0.40 | %30 |
| D2 | <0.38 | 7103 | +0.90 | -0.40 | %27 |
| D3 | <0.51 | 7103 | +1.00 | -0.40 | %28 |
| D4 | <0.64 | 7103 | +0.39 | -0.40 | %29 |
| D5 | <0.77 | 7103 | +0.13 | -0.40 | %27 |
| D6 | <0.90 | 7103 | +0.90 | -0.40 | %29 |
| D7 | <1.06 | 7103 | +0.64 | -0.40 | %28 |
| D8 | <1.28 | 7103 | +0.99 | -0.40 | %28 |
| D9 | <1.63 | 7103 | +1.65 | -0.40 | %30 |
| D10 | >=1.63 | 7104 | +0.99 | -0.40 | %28 |

### ATR normalizasyonu ile esik: alim mumu < 1,0 x ATR20 (donem bazinda, obek)

| donem | n kucuk / diger | fark | p |
|---|---|---|---|
| 2016-19 | 1551 / 8768 | +2.28 | 0.002 |
| 2020-22 | 2594 / 14911 | +1.14 | 0.094 |
| 2023 | 932 / 4042 | +0.74 | 0.651 |
| 2024-26 | 2998 / 14210 | +2.66 | 0.000 |
| ABD 2022-23 | 7446 / 15650 | +0.04 | 0.861 |
| ABD 2024-26 | 14575 / 33361 | -0.14 | 0.454 |

## 5. Portfoy etkisinin kaynagi: sayi mi, secim mi? (obek, donem)

| donem | n kucuk / diger | ort kucuk / diger | slot kucuk | slot diger (ayni n, 20 rastgele orneklem ort) | slot hepsi | ort bar kucuk / diger | gunluk es zamanli sinyal kucuk / diger |
|---|---|---|---|---|---|---|---|
| 2016-19 | 3137 / 7182 | +7.7 / +5.7 | +151% | +73% | +93% | 33 / 30 | 7.6 / 14.0 |
| 2020-22 | 5992 / 11513 | +13.6 / +11.7 | +319% | +235% | +231% | 30 / 26 | 10.6 / 16.6 |
| 2023 | 1951 / 3023 | +17.8 / +14.9 | +139% | +114% | +124% | 27 / 24 | 10.1 / 13.0 |
| 2024-26 | 6678 / 10530 | +5.2 / +3.7 | +135% | +62% | +180% | 27 / 25 | 11.0 / 16.1 |
| ABD 2022-23 | 12974 / 10122 | -0.5 / +0.1 | -7% | +11% | -6% | 44 / 42 | 40.5 / 30.9 |
| ABD 2024-26 | 25386 / 22550 | +1.5 / +1.4 | -0% | +53% | +40% | 39 / 35 | 37.7 / 32.7 |

Okuma: 'slot kucuk' > 'slot diger (ayni n)' ise secim; yalniz n farkindan geliyorsa sayi. Es zamanli sinyal yuksekse slotlar doluyor, islem atlaniyor.

### 5b. Alim mumundan sonraki 5 gun: getiri ve volatilite genislemesi (obek; sonuc olcusu)

| donem | ileri5 ort kucuk / diger | ileri5 kazanan kucuk / diger | 5g (H-L)/ATR20 medyan kucuk / diger | NATR50 yuzdelik <=10 : n, islem getirisi, ileri5 | NATR50 yuzdelik >10 : islem getirisi |
|---|---|---|---|---|---|
| 2016-19 | +1.23 / +1.04 | %54 / %48 | 1.18 / 1.40 | 4020, +6.8, +1.55 | +6.0 |
| 2020-22 | +2.77 / +3.18 | %60 / %57 | 1.20 / 1.45 | 8748, +14.0, +3.28 | +10.7 |
| 2023 | +2.40 / +1.95 | %57 / %54 | 1.10 / 1.36 | 2603, +16.8, +1.53 | +15.2 |
| 2024-26 | +1.50 / +1.27 | %58 / %52 | 1.14 / 1.32 | 9209, +5.5, +1.64 | +2.9 |
| ABD 2022-23 | -0.01 / +0.29 | %49 / %50 | 0.98 / 1.06 | 13285, -0.1, +0.32 | -0.5 |
| ABD 2024-26 | +0.15 / +0.59 | %48 / %50 | 1.02 / 1.10 | 23866, +1.8, +0.40 | +1.1 |

Okuma: kucuk mumdan sonra 5 gunde getiri ve vol genislemesi digerinden buyuk degilse 'kucuk mum = hemen ardindan hacimli kirilim' hikayesi veri ile desteklenmiyor.

## 6. Karistiricilar: kucuk mum baska neyle birlikte geliyor? (obek, pazar havuzu)

| pazar | degisken | ort kucuk | ort diger | nokta-biserial r |
|---|---|---|---|---|
| BIST | w | 14.35 | 14.52 | -0.02 |
| BIST | bekleme | 7.49 | 8.32 | -0.04 |
| BIST | piyasa60 | 10.29 | 12.08 | -0.04 |
| BIST | ruzgar60 | 0.77 | 1.07 | -0.02 |
| BIST | lik60 | 204.85 | 131.97 | +0.06 |
| BIST | fiyat | 70.21 | 74.70 | -0.00 |
| BIST | vol20 | 2.29 | 2.54 | -0.12 |
| BIST | atr20_pct | 3.61 | 3.69 | -0.03 |
| BIST | obek_sira | 24.42 | 24.22 | +0.00 |
| BIST | alim_ustu_pct | 1.62 | 3.49 | -0.25 |
| BIST | gap_pct | 0.62 | 0.54 | +0.03 |
| BIST | hacim_alim_kat | 1.74 | 4.71 | -0.14 |
| BIST | natr50_pct | 14.23 | 23.01 | -0.20 |
| BIST | yuv_pct | 8.74 | 7.24 | +0.15 |
| BIST | konum250 | 0.67 | 0.66 | +0.02 |
| BIST | sektor payi farki (kucuk - diger), en buyuk 3 | XHOLD +0.8, XBANK +0.7, XTCRT +0.7 | en kucuk 3: XYORT -1.2, XTRZM -0.8, XGIDA -0.7 | |
| ABD | w | 13.87 | 13.92 | -0.01 |
| ABD | bekleme | 7.58 | 8.34 | -0.04 |
| ABD | piyasa60 | 4.03 | 4.13 | -0.01 |
| ABD | ruzgar60 | 1.31 | 1.24 | +0.01 |
| ABD | lik60 | 279.94 | 198.83 | +0.03 |
| ABD | fiyat | 78.09 | 82.69 | -0.00 |
| ABD | vol20 | 2.03 | 2.60 | -0.18 |
| ABD | atr20_pct | 3.01 | 3.40 | -0.12 |
| ABD | obek_sira | 17.98 | 17.89 | +0.00 |
| ABD | alim_ustu_pct | 1.31 | 3.77 | -0.22 |
| ABD | gap_pct | 0.54 | 1.42 | -0.12 |
| ABD | hacim_alim_kat | 1.24 | 4.89 | -0.02 |
| ABD | natr50_pct | 15.71 | 24.88 | -0.20 |
| ABD | yuv_pct | 7.11 | 7.30 | -0.02 |
| ABD | konum250 | 0.69 | 0.67 | +0.04 |
| ABD | sektor payi farki (kucuk - diger), en buyuk 3 | Financial Services +2.1, Energy +2.0, Real Estate +1.2 | en kucuk 3: Healthcare -4.6, Technology -0.6, Industrials -0.5 | |

## 7. Karar kurali

- BIST kova ici arti: 17/20 kova (fiyat+likidite+vol+ATR)
- ABD kova ici arti: 9/20 kova (fiyat+likidite+vol+ATR)
- BIST OLS kucuk t = +6.76 (RVOL kontrollu t = -0.17); monotonluk Spearman alim_mum_kat -0.87, mum/ATR -0.53
- ABD OLS kucuk t = +0.91 (RVOL kontrollu t = +0.97); monotonluk Spearman alim_mum_kat +0.36, mum/ATR +0.27

Kriter: kova ici arti >= %70 (her pazar) VE OLS t >= 2 hacim kontrolu ile de (her pazar) VE desil monotonlugu Spearman <= -0,5 (her pazar). Sonuc: kova ici GECMEDI, OLS GECMEDI, monotonluk GECMEDI -> **ARASTIRILDI, ALINMADI**.

