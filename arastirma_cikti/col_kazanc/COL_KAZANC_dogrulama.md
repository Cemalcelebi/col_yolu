# COL KAZANC — DOGRULAMA: kucuk alim mumu izi (alim_mum_kat < 1.5)   (COL_KAZANC v1.3 (2026-10-24, denetim: kopya islem, hisse basina tek slot, ay kumeli p, dogru bos dagilim), 2026-10-24 22:27)

Soru (Cemal 21 Eki): 'alim mumu kucuk olsun' sarti gercek iz mi, yoksa volatilite / fiyat / likidite / cok test artefakti mi?
Fark = kucuk mum islemlerinin ort getirisi (%200 kirpili) - geri kalanin ort getirisi (puan). p = Welch, normal yaklasim. Slot = 30 slot portfoy.

## 1. Donem x pazar fark, esik duyarliligi (obek islemleri; parantez icinde TABAN kutulari)

| esik | donem | n kucuk / n diger | fark ort | kazanan fark | p | slot kucuk / hepsi | TABAN fark (p) |
|---|---|---|---|---|---|---|---|
| 1.2 | 2016-19 | 1490 / 5991 | +1.88 | +1.7 | 0.021 | +83% / +139% | +1.56 (0.002) |
| 1.2 | 2020-22 | 1802 / 6383 | +2.79 | +7.0 | 0.002 | +254% / +269% | +1.58 (0.006) |
| 1.2 | 2023 | 740 / 1986 | +4.68 | +3.8 | 0.014 | +81% / +85% | +1.62 (0.103) |
| 1.2 | 2024-26 | 2267 / 6841 | +2.99 | +8.3 | 0.000 | +109% / +83% | +2.01 (0.000) |
| 1.2 | ABD 2022-23 | 8176 / 10699 | -1.29 | -3.1 | 0.000 | -9% / +7% | -1.24 (0.000) |
| 1.2 | ABD 2024-26 | 9186 / 16146 | +0.42 | +2.0 | 0.096 | +9% / +12% | +0.28 (0.116) |
| 1.5 | 2016-19 | 2442 / 5039 | +1.67 | +2.5 | 0.014 | +106% / +139% | +1.14 (0.012) |
| 1.5 | 2020-22 | 3011 / 5174 | +2.04 | +4.7 | 0.008 | +257% / +269% | +1.99 (0.000) |
| 1.5 | 2023 | 1226 / 1500 | +3.48 | +3.5 | 0.032 | +93% / +85% | +1.32 (0.165) |
| 1.5 | 2024-26 | 3767 / 5341 | +2.26 | +7.4 | 0.000 | +108% / +83% | +1.80 (0.000) |
| 1.5 | ABD 2022-23 | 11942 / 6933 | -1.45 | -3.7 | 0.000 | -9% / +7% | -1.65 (0.000) |
| 1.5 | ABD 2024-26 | 14257 / 11075 | +0.27 | +1.6 | 0.278 | -4% / +12% | +0.04 (0.845) |
| 2.0 | 2016-19 | 3972 / 3509 | +1.21 | +3.4 | 0.047 | +115% / +139% | +0.47 (0.298) |
| 2.0 | 2020-22 | 4913 / 3272 | +1.95 | +3.1 | 0.009 | +278% / +269% | +1.69 (0.002) |
| 2.0 | 2023 | 1901 / 825 | +2.34 | +3.1 | 0.172 | +91% / +85% | -2.55 (0.044) |
| 2.0 | 2024-26 | 5783 / 3325 | +2.57 | +7.2 | 0.000 | +87% / +83% | +1.88 (0.000) |
| 2.0 | ABD 2022-23 | 15606 / 3269 | -1.31 | -3.9 | 0.000 | -4% / +7% | -1.96 (0.000) |
| 2.0 | ABD 2024-26 | 19682 / 5650 | -0.44 | +0.4 | 0.164 | -17% / +12% | -0.36 (0.169) |
| 3.0 | 2016-19 | 5681 / 1800 | +2.35 | +5.2 | 0.001 | +131% / +139% | +1.18 (0.030) |
| 3.0 | 2020-22 | 7163 / 1022 | +1.89 | +4.2 | 0.079 | +299% / +269% | +1.04 (0.223) |
| 3.0 | 2023 | 2613 / 113 | +7.17 | +10.7 | 0.044 | +91% / +85% | -5.79 (0.053) |
| 3.0 | 2024-26 | 8092 / 1016 | +2.91 | +7.2 | 0.000 | +82% / +83% | +1.79 (0.007) |
| 3.0 | ABD 2022-23 | 17959 / 916 | -1.07 | -3.9 | 0.080 | +3% / +7% | -2.25 (0.000) |
| 3.0 | ABD 2024-26 | 23554 / 1778 | -0.79 | -0.1 | 0.157 | -8% / +12% | -0.43 (0.358) |

### Coklu test duzeltmesi

Tarama: 99 kova (olcu x kova), 592 kova x donem hucresi. Bonferroni esigi 0,05/99 = 0.00051 (kova) ve 0,05/592 = 0.000084 (hucre).

- BIST havuz (tum donemler): n 10446 / 17054, fark +2.22, Welch p = 5.23e-09, AY KUMELI p = 1.30e-04 -> Bonferroni(kova, ay kumeli) GECER, Bonferroni(hucre, ay kumeli) GECMEZ (denetim 24 Eki: Welch bagimsiz gozlem varsayar, kumeli p esas)
- ABD havuz (tum donemler): n 59331 / 36125, fark -0.12, Welch p = 2.86e-01, AY KUMELI p = 2.43e-01 -> Bonferroni(kova, ay kumeli) GECMEZ, Bonferroni(hucre, ay kumeli) GECMEZ (denetim 24 Eki: Welch bagimsiz gozlem varsayar, kumeli p esas)
- BH-FDR (q < 0,10) ile ayakta kalan hucre: 273 / 592; kucuk mum hucreleri: 2016-19 q=0.04, 2020-22 q=0.02, 2023 q=0.07, 2024-26 q=0.00, ABD 2022-23 q=0.00, ABD 2024-26 q=0.40

## 2. Kaynak ayristirma — kova icinde kucuk vs buyuk mum farki (pazar havuzu, obek)

### BIST — fiyat

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| 20-50 | 1470 / 2029 | +6.85 | +5.23 | +1.62 | 0.085 | %38 / %32 |
| 5-20 | 2943 / 4482 | +7.91 | +6.48 | +1.43 | 0.034 | %39 / %35 |
| 50-100 | 617 / 746 | +9.14 | +7.28 | +1.86 | 0.301 | %39 / %36 |
| <5 | 4523 / 8477 | +12.23 | +8.75 | +3.48 | 0.000 | %43 / %37 |
| >100 | 893 / 1320 | +6.66 | +4.92 | +1.74 | 0.144 | %37 / %33 |

### BIST — likidite (lik60 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 1567 / 3933 | +12.71 | +7.74 | +4.97 | 0.000 | %41 / %34 |
| Q2 | 1909 / 3591 | +13.44 | +9.84 | +3.60 | 0.000 | %44 / %38 |
| Q3 | 2128 / 3372 | +10.88 | +8.16 | +2.72 | 0.001 | %44 / %37 |
| Q4 | 2218 / 3282 | +7.00 | +5.43 | +1.56 | 0.048 | %37 / %33 |
| Q5 | 2624 / 2876 | +6.11 | +5.10 | +1.01 | 0.168 | %37 / %35 |

### BIST — volatilite (vol20 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 2616 / 2884 | +7.72 | +6.94 | +0.78 | 0.277 | %38 / %37 |
| Q2 | 2311 / 3189 | +7.87 | +6.54 | +1.33 | 0.063 | %39 / %37 |
| Q3 | 2042 / 3458 | +10.41 | +8.45 | +1.96 | 0.020 | %43 / %37 |
| Q4 | 1734 / 3766 | +12.41 | +7.38 | +5.03 | 0.000 | %45 / %36 |
| Q5 | 1743 / 3757 | +10.95 | +7.42 | +3.53 | 0.001 | %37 / %31 |

### BIST — ATR% (atr20_pct besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 2326 / 3174 | +6.46 | +6.68 | -0.22 | 0.737 | %37 / %38 |
| Q2 | 2150 / 3350 | +7.35 | +6.62 | +0.73 | 0.310 | %40 / %36 |
| Q3 | 1999 / 3501 | +10.20 | +6.94 | +3.26 | 0.000 | %44 / %35 |
| Q4 | 1910 / 3590 | +12.71 | +8.73 | +3.98 | 0.000 | %45 / %36 |
| Q5 | 2061 / 3439 | +12.01 | +7.78 | +4.23 | 0.000 | %38 / %32 |

### BIST — iki yonlu: kucuk mum x fiyat (ort getiri, n)

| kucuk | 20-50 | 5-20 | 50-100 | <5 | >100 |
|---|---|---|---|---|---|
| buyuk | +5.2 (n2029) | +6.5 (n4482) | +7.3 (n746) | +8.8 (n8477) | +4.9 (n1320) |
| kucuk | +6.9 (n1470) | +7.9 (n2943) | +9.1 (n617) | +12.2 (n4523) | +6.7 (n893) |

### BIST — iki yonlu: kucuk mum x likidite (ort getiri, n)

| kucuk | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| buyuk | +7.7 (n3933) | +9.8 (n3591) | +8.2 (n3372) | +5.4 (n3282) | +5.1 (n2876) |
| kucuk | +12.7 (n1567) | +13.4 (n1909) | +10.9 (n2128) | +7.0 (n2218) | +6.1 (n2624) |

### BIST — iki yonlu: kucuk mum x RVOL (alim hacmi / obek medyan hacmi): ort getiri (n, kazanan)

| kucuk | <1 | 1-2 | 2-4 | >=4 |
|---|---|---|---|---|
| kucuk | +12.0 (n2245, %42) | +9.2 (n5474, %41) | +9.0 (n2289, %39) | +5.8 (n438, %32) |
| buyuk | +12.2 (n500, %41) | +8.1 (n4148, %37) | +7.9 (n6794, %36) | +5.9 (n5611, %33) |

### ABD — fiyat

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| 20-50 | 18113 / 10262 | +0.72 | +0.81 | -0.09 | 0.619 | %31 / %30 |
| 5-20 | 16066 / 10754 | +0.89 | +0.97 | -0.08 | 0.721 | %29 / %29 |
| 50-100 | 12316 / 6671 | +1.21 | +0.76 | +0.45 | 0.039 | %32 / %31 |
| <5 | 2508 / 2735 | +3.53 | +5.45 | -1.92 | 0.016 | %31 / %29 |
| >100 | 10328 / 5703 | +0.82 | +0.33 | +0.49 | 0.031 | %30 / %30 |

### ABD — likidite (lik60 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 10384 / 8708 | +1.39 | +1.76 | -0.37 | 0.242 | %29 / %28 |
| Q2 | 11951 / 7140 | +0.38 | +0.76 | -0.38 | 0.127 | %30 / %29 |
| Q3 | 12256 / 6835 | +0.57 | +0.82 | -0.25 | 0.292 | %30 / %29 |
| Q4 | 12306 / 6785 | +1.31 | +1.03 | +0.28 | 0.191 | %32 / %31 |
| Q5 | 12434 / 6657 | +1.39 | +1.09 | +0.30 | 0.176 | %32 / %31 |

### ABD — volatilite (vol20 besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 13671 / 5421 | +1.26 | +1.49 | -0.23 | 0.208 | %34 / %35 |
| Q2 | 12827 / 6264 | +0.68 | +0.76 | -0.08 | 0.664 | %30 / %31 |
| Q3 | 12066 / 7025 | +0.60 | +0.51 | +0.08 | 0.699 | %29 / %28 |
| Q4 | 11327 / 7764 | +0.63 | +1.01 | -0.37 | 0.131 | %29 / %29 |
| Q5 | 9440 / 9651 | +2.03 | +1.69 | +0.34 | 0.337 | %29 / %27 |

### ABD — ATR% (atr20_pct besteblik)

| kova | n kucuk / diger | ort kucuk | ort diger | fark | p | kazanan kucuk / diger |
|---|---|---|---|---|---|---|
| Q1 | 13032 / 6060 | +1.51 | +1.51 | +0.00 | 0.982 | %36 / %36 |
| Q2 | 12472 / 6619 | +0.44 | +0.70 | -0.26 | 0.182 | %29 / %30 |
| Q3 | 12033 / 7058 | +0.80 | +0.82 | -0.03 | 0.891 | %29 / %29 |
| Q4 | 11612 / 7479 | +0.53 | +0.67 | -0.13 | 0.589 | %29 / %29 |
| Q5 | 10182 / 8909 | +1.81 | +1.80 | +0.02 | 0.961 | %29 / %26 |

### ABD — iki yonlu: kucuk mum x fiyat (ort getiri, n)

| kucuk | 20-50 | 5-20 | 50-100 | <5 | >100 |
|---|---|---|---|---|---|
| buyuk | +0.8 (n10262) | +1.0 (n10754) | +0.8 (n6671) | +5.5 (n2735) | +0.3 (n5703) |
| kucuk | +0.7 (n18113) | +0.9 (n16066) | +1.2 (n12316) | +3.5 (n2508) | +0.8 (n10328) |

### ABD — iki yonlu: kucuk mum x likidite (ort getiri, n)

| kucuk | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| buyuk | +1.8 (n8708) | +0.8 (n7140) | +0.8 (n6835) | +1.0 (n6785) | +1.1 (n6657) |
| kucuk | +1.4 (n10384) | +0.4 (n11951) | +0.6 (n12256) | +1.3 (n12306) | +1.4 (n12434) |

### ABD — iki yonlu: kucuk mum x RVOL (alim hacmi / obek medyan hacmi): ort getiri (n, kazanan)

| kucuk | <1 | 1-2 | 2-4 | >=4 |
|---|---|---|---|---|
| kucuk | +1.0 (n26177, %31) | +0.9 (n29676, %30) | +2.0 (n3155, %31) | +1.6 (n318, %33) |
| buyuk | +0.8 (n4164, %30) | +1.0 (n19398, %30) | +1.2 (n9119, %29) | +1.7 (n3434, %28) |

### OLS: getiri ~ kucuk + log fiyat + log lik60 + vol20 + w + bekleme + piyasa60 + donem kuklalari (HC0 SE)

| pazar | n | kucuk katsayi | SE | t | kazanan modeli (LPM) kucuk katsayi | t | + log RVOL kontrolu: kucuk | log RVOL katsayisi |
|---|---|---|---|---|---|---|---|---|
| BIST | 27500 | +2.240 | 0.389 | +5.76 | +0.0418 | +6.81 | +0.253 (t +0.59) | -3.080 (t -10.12) |
| ABD | 95456 | +0.005 | 0.114 | +0.04 | +0.0002 | +0.06 | +0.019 (t +0.15) | +0.116 (t +0.84) |

Okuma: kucuk katsayisi, fiyat/likidite/volatilite/donem kontrolunden sonra |t| >= 2 ile ayni isarette kaliyorsa iz kendi basina; kayboluyorsa proxy.
Son iki sutun: alim gunu goreli hacmi (RVOL = alim hacmi / obek medyan hacmi) modele girince kucuk katsayisi sifira iniyorsa, kucuk mum dusuk hacmin vekilidir (iz hacimdedir, mum boyunda degil).

## 3-4. Normalizasyon (mum/ATR20) ve desil monotonlugu (obek, pazar havuzu)

### BIST — alim_mum_kat desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.92

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.91 | 2750 | +11.20 | -0.40 | %42 |
| D2 | <1.14 | 2750 | +9.91 | -0.40 | %41 |
| D3 | <1.34 | 2750 | +7.99 | -0.40 | %40 |
| D4 | <1.53 | 2750 | +8.97 | -0.40 | %38 |
| D5 | <1.75 | 2750 | +8.00 | -0.40 | %37 |
| D6 | <1.99 | 2750 | +8.38 | -0.40 | %38 |
| D7 | <2.29 | 2750 | +7.84 | -0.40 | %36 |
| D8 | <2.68 | 2750 | +7.43 | -0.40 | %35 |
| D9 | <3.37 | 2750 | +7.25 | -0.40 | %36 |
| D10 | >=3.37 | 2750 | +5.21 | -0.40 | %31 |

### BIST — alim_mum_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.78

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.81 | 2750 | +10.95 | -0.40 | %41 |
| D2 | <1.01 | 2750 | +9.19 | -0.40 | %40 |
| D3 | <1.18 | 2750 | +8.65 | -0.40 | %39 |
| D4 | <1.34 | 2750 | +7.98 | -0.40 | %38 |
| D5 | <1.51 | 2750 | +7.65 | -0.40 | %37 |
| D6 | <1.70 | 2750 | +8.14 | -0.40 | %36 |
| D7 | <1.92 | 2750 | +8.49 | -0.40 | %38 |
| D8 | <2.20 | 2750 | +8.29 | -0.40 | %37 |
| D9 | <2.65 | 2750 | +7.49 | -0.40 | %36 |
| D10 | >=2.65 | 2750 | +5.36 | -0.40 | %32 |

### BIST — govde_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.92

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.28 | 2750 | +10.27 | -0.40 | %40 |
| D2 | <0.45 | 2750 | +9.89 | -0.40 | %41 |
| D3 | <0.60 | 2750 | +8.13 | -0.40 | %38 |
| D4 | <0.75 | 2750 | +9.70 | -0.40 | %39 |
| D5 | <0.91 | 2750 | +8.42 | -0.40 | %38 |
| D6 | <1.09 | 2750 | +7.56 | -0.40 | %37 |
| D7 | <1.30 | 2750 | +7.10 | -0.40 | %37 |
| D8 | <1.57 | 2750 | +7.59 | -0.40 | %36 |
| D9 | <2.00 | 2750 | +6.56 | -0.40 | %33 |
| D10 | >=2.00 | 2750 | +6.97 | -0.40 | %34 |

### ABD — alim_mum_kat desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.09

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.77 | 9546 | +1.35 | -0.40 | %32 |
| D2 | <0.91 | 9546 | +0.81 | -0.40 | %30 |
| D3 | <1.04 | 9545 | +1.36 | -0.40 | %31 |
| D4 | <1.17 | 9546 | +0.86 | -0.40 | %30 |
| D5 | <1.30 | 9545 | +0.87 | -0.40 | %30 |
| D6 | <1.46 | 9546 | +0.73 | -0.40 | %29 |
| D7 | <1.65 | 9545 | +0.69 | -0.40 | %30 |
| D8 | <1.94 | 9546 | +1.20 | -0.40 | %30 |
| D9 | <2.47 | 9545 | +1.35 | -0.40 | %30 |
| D10 | >=2.47 | 9546 | +1.26 | -0.40 | %29 |

### ABD — alim_mum_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = +0.09

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.68 | 9546 | +1.47 | -0.40 | %32 |
| D2 | <0.80 | 9546 | +0.97 | -0.40 | %30 |
| D3 | <0.91 | 9545 | +1.08 | -0.40 | %31 |
| D4 | <1.01 | 9546 | +0.68 | -0.40 | %30 |
| D5 | <1.12 | 9545 | +1.11 | -0.40 | %30 |
| D6 | <1.24 | 9546 | +0.71 | -0.40 | %29 |
| D7 | <1.40 | 9545 | +0.96 | -0.40 | %30 |
| D8 | <1.61 | 9546 | +0.98 | -0.40 | %29 |
| D9 | <1.99 | 9545 | +1.21 | -0.40 | %30 |
| D10 | >=1.99 | 9546 | +1.30 | -0.40 | %29 |

### ABD — govde_atr desilleri (D1 en kucuk mum). Spearman(desil, ort) = -0.16

| desil | ust sinir | n | ort | medyan | kazanan |
|---|---|---|---|---|---|
| D1 | <0.21 | 9546 | +1.21 | -0.40 | %31 |
| D2 | <0.34 | 9546 | +1.24 | -0.40 | %30 |
| D3 | <0.46 | 9545 | +1.17 | -0.40 | %31 |
| D4 | <0.56 | 9546 | +0.99 | -0.40 | %30 |
| D5 | <0.68 | 9545 | +0.86 | -0.40 | %30 |
| D6 | <0.80 | 9546 | +0.79 | -0.40 | %30 |
| D7 | <0.95 | 9545 | +0.97 | -0.40 | %30 |
| D8 | <1.14 | 9546 | +0.89 | -0.40 | %29 |
| D9 | <1.46 | 9545 | +1.01 | -0.40 | %30 |
| D10 | >=1.46 | 9546 | +1.35 | -0.40 | %30 |

### ATR normalizasyonu ile esik: alim mumu < 1,0 x ATR20 (donem bazinda, obek)

| donem | n kucuk / diger | fark | p |
|---|---|---|---|
| 2016-19 | 1336 / 6145 | +1.70 | 0.046 |
| 2020-22 | 1486 / 6699 | +1.44 | 0.130 |
| 2023 | 644 / 2082 | +0.93 | 0.636 |
| 2024-26 | 1821 / 7287 | +3.25 | 0.000 |
| ABD 2022-23 | 7421 / 11454 | -1.11 | 0.000 |
| ABD 2024-26 | 8763 / 16569 | +0.32 | 0.204 |

## 5. Portfoy etkisinin kaynagi: sayi mi, secim mi? (obek, donem)

| donem | n kucuk / diger | ort kucuk / diger | slot kucuk | slot diger (ayni n, 20 rastgele orneklem ort) | slot hepsi | ort bar kucuk / diger | gunluk es zamanli sinyal kucuk / diger |
|---|---|---|---|---|---|---|---|
| 2016-19 | 2442 / 5039 | +7.1 / +5.5 | +106% | +106% | +139% | 36 / 32 | 3.7 / 6.1 |
| 2020-22 | 3011 / 5174 | +14.0 / +11.9 | +257% | +261% | +269% | 30 / 27 | 5.3 / 7.4 |
| 2023 | 1226 / 1500 | +16.9 / +13.4 | +93% | +89% | +85% | 27 / 24 | 6.4 / 6.6 |
| 2024-26 | 3767 / 5341 | +5.3 / +3.1 | +108% | +82% | +83% | 27 / 25 | 6.3 / 8.2 |
| ABD 2022-23 | 11942 / 6933 | -2.1 / -0.7 | -9% | -3% | +7% | 38 / 39 | 23.9 / 13.6 |
| ABD 2024-26 | 14257 / 11075 | +1.8 / +1.6 | -4% | +13% | +12% | 40 / 35 | 21.3 / 16.3 |

Okuma: 'slot kucuk' > 'slot diger (ayni n)' ise secim; yalniz n farkindan geliyorsa sayi. Es zamanli sinyal yuksekse slotlar doluyor, islem atlaniyor.

### 5b. Alim mumundan sonraki 5 gun: getiri ve volatilite genislemesi (obek; sonuc olcusu)

| donem | ileri5 ort kucuk / diger | ileri5 kazanan kucuk / diger | 5g (H-L)/ATR20 medyan kucuk / diger | NATR50 yuzdelik <=10 : n, islem getirisi, ileri5 | NATR50 yuzdelik >10 : islem getirisi |
|---|---|---|---|---|---|
| 2016-19 | +0.79 / +0.78 | %52 / %47 | 1.16 / 1.36 | 2923, +5.7, +0.88 | +6.2 |
| 2020-22 | +2.48 / +2.73 | %59 / %55 | 1.17 / 1.40 | 3813, +14.3, +2.76 | +11.3 |
| 2023 | +1.83 / +2.01 | %56 / %54 | 1.06 / 1.31 | 1362, +15.4, +1.18 | +14.6 |
| 2024-26 | +1.51 / +1.05 | %58 / %52 | 1.12 / 1.31 | 4645, +4.7, +1.47 | +3.2 |
| ABD 2022-23 | -0.29 / +0.04 | %48 / %49 | 0.95 / 1.05 | 11315, -1.8, -0.04 | -1.3 |
| ABD 2024-26 | +0.33 / +0.57 | %49 / %51 | 1.01 / 1.09 | 12443, +2.1, +0.54 | +1.4 |

Okuma: kucuk mumdan sonra 5 gunde getiri ve vol genislemesi digerinden buyuk degilse 'kucuk mum = hemen ardindan hacimli kirilim' hikayesi veri ile desteklenmiyor.

## 6. Karistiricilar: kucuk mum baska neyle birlikte geliyor? (obek, pazar havuzu)

| pazar | degisken | ort kucuk | ort diger | nokta-biserial r |
|---|---|---|---|---|
| BIST | w | 12.60 | 12.36 | +0.03 |
| BIST | bekleme | 7.44 | 8.69 | -0.06 |
| BIST | piyasa60 | 8.20 | 9.85 | -0.04 |
| BIST | ruzgar60 | 0.94 | 1.07 | -0.01 |
| BIST | lik60 | 201.10 | 123.17 | +0.06 |
| BIST | fiyat | 71.42 | 80.27 | -0.01 |
| BIST | vol20 | 2.33 | 2.54 | -0.10 |
| BIST | atr20_pct | 3.59 | 3.66 | -0.03 |
| BIST | obek_sira | 23.38 | 22.07 | +0.03 |
| BIST | alim_ustu_pct | 1.60 | 3.40 | -0.24 |
| BIST | gap_pct | 0.58 | 0.51 | +0.03 |
| BIST | hacim_alim_kat | 1.76 | 4.83 | -0.20 |
| BIST | natr50_pct | 15.51 | 24.62 | -0.20 |
| BIST | yuv_pct | 8.04 | 6.48 | +0.16 |
| BIST | konum250 | 0.66 | 0.64 | +0.03 |
| BIST | sektor payi farki (kucuk - diger), en buyuk 3 | XBANK +0.9, XHOLD +0.9, XTAST +0.6 | en kucuk 3: XYORT -1.0, XTEKS -0.7, XTRZM -0.5 | |
| ABD | w | 12.64 | 12.34 | +0.03 |
| ABD | bekleme | 7.32 | 8.57 | -0.07 |
| ABD | piyasa60 | 5.19 | 4.94 | +0.02 |
| ABD | ruzgar60 | 1.02 | 1.07 | -0.00 |
| ABD | lik60 | 191.10 | 163.49 | +0.01 |
| ABD | fiyat | 96.83 | 194.75 | -0.01 |
| ABD | vol20 | 1.93 | 2.42 | -0.16 |
| ABD | atr20_pct | 2.86 | 3.23 | -0.11 |
| ABD | obek_sira | 24.74 | 23.40 | +0.03 |
| ABD | alim_ustu_pct | 1.23 | 3.32 | -0.24 |
| ABD | gap_pct | 0.47 | 1.12 | -0.12 |
| ABD | hacim_alim_kat | 1.17 | 3.75 | -0.02 |
| ABD | natr50_pct | 15.48 | 26.19 | -0.23 |
| ABD | yuv_pct | 6.69 | 6.66 | +0.00 |
| ABD | konum250 | 0.72 | 0.70 | +0.03 |
| ABD | sektor payi farki (kucuk - diger), en buyuk 3 | Real Estate +2.1, Financial Services +1.7, Energy +0.7 | en kucuk 3: Healthcare -4.0, Basic Materials -0.8, Communication Services -0.3 | |

## 7. Karar kurali

- BIST kova ici arti: 19/20 kova (fiyat+likidite+vol+ATR)
- ABD kova ici arti: 8/20 kova (fiyat+likidite+vol+ATR)
- BIST OLS kucuk t = +5.76 (RVOL kontrollu t = +0.59); monotonluk Spearman alim_mum_kat -0.92, mum/ATR -0.78
- ABD OLS kucuk t = +0.04 (RVOL kontrollu t = +0.15); monotonluk Spearman alim_mum_kat -0.09, mum/ATR +0.09

Kriter: kova ici arti >= %70 (her pazar) VE OLS t >= 2 hacim kontrolu ile de (her pazar) VE desil monotonlugu Spearman <= -0,5 (her pazar). Sonuc: kova ici GECMEDI, OLS GECMEDI, monotonluk GECMEDI -> **ARASTIRILDI, ALINMADI**.

