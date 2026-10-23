# SESSIZ_ML — SESSIZ_ML v1.2 (2026-10-23, Z0 bolgelerinde alis + satis modeli, ileri yuruyen LightGBM)

Z0 olaylari: 25398 (BIST 5584, ABD 19814). Maliyet: komisyon %0.2 + kayma her yonde %0.3 = islem basina %0.8.

## 1) Egitim kaniti (logloss: ilk/son agac, sabit tahmin kaybi, model dosyasi)

| model    |   test_yili |   n_egitim |   n_test |   agac |   egitim_kayip_ilk |   egitim_kayip_son |   egitim_sabit_tahmin |   test_kayip_ilk |   test_kayip_son |   test_kayip_en_dusuk |   test_sabit_tahmin | dosya                                                |
|:---------|------------:|-----------:|---------:|-------:|-------------------:|-------------------:|----------------------:|-----------------:|-----------------:|----------------------:|--------------------:|:-----------------------------------------------------|
| alis_k20 |        2019 |       6256 |     3308 |    300 |              0.48  |              0.303 |                 0.483 |            0.541 |            0.453 |                 0.45  |               0.546 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2019.txt |
| alis_k20 |        2020 |       8640 |     1710 |    300 |              0.492 |              0.329 |                 0.496 |            0.718 |            0.678 |                 0.65  |               0.723 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2020.txt |
| alis_k20 |        2021 |      10615 |     3634 |    300 |              0.51  |              0.349 |                 0.514 |            0.513 |            0.488 |                 0.482 |               0.515 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2021.txt |
| alis_k20 |        2022 |      14227 |     1452 |    300 |              0.525 |              0.385 |                 0.529 |            0.658 |            0.545 |                 0.54  |               0.663 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2022.txt |
| alis_k20 |        2023 |      16024 |     3502 |    300 |              0.536 |              0.395 |                 0.541 |            0.53  |            0.475 |                 0.471 |               0.533 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2023.txt |
| alis_k20 |        2024 |      19120 |     2529 |    300 |              0.532 |              0.393 |                 0.537 |            0.606 |            0.588 |                 0.567 |               0.609 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2024.txt |
| alis_k20 |        2025 |      21820 |     1933 |    300 |              0.541 |              0.414 |                 0.545 |            0.641 |            0.58  |                 0.579 |               0.645 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2025.txt |
| alis_k20 |        2026 |      24015 |      755 |    300 |              0.55  |              0.429 |                 0.554 |            0.645 |            0.631 |                 0.624 |               0.647 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2026.txt |
| alis_x2  |        2019 |       5128 |     3308 |    300 |              0.285 |              0.103 |                 0.289 |            0.459 |            0.331 |                 0.314 |               0.468 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2019.txt  |
| alis_x2  |        2020 |       6325 |     1710 |    300 |              0.274 |              0.11  |                 0.278 |            0.535 |            0.459 |                 0.433 |               0.541 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2020.txt  |
| alis_x2  |        2021 |       9633 |     3634 |    300 |              0.333 |              0.147 |                 0.34  |            0.303 |            0.263 |                 0.253 |               0.306 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2021.txt  |
| alis_x2  |        2022 |      11343 |     1452 |    300 |              0.358 |              0.174 |                 0.365 |            0.708 |            0.504 |                 0.492 |               0.716 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2022.txt  |
| alis_x2  |        2023 |      14977 |     3502 |    300 |              0.344 |              0.177 |                 0.351 |            0.318 |            0.254 |                 0.251 |               0.322 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2023.txt  |
| alis_x2  |        2024 |      16429 |     2529 |    300 |              0.376 |              0.188 |                 0.383 |            0.352 |            0.408 |                 0.332 |               0.356 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2024.txt  |
| alis_x2  |        2025 |      19931 |     1622 |    300 |              0.365 |              0.196 |                 0.373 |            0.541 |            0.561 |                 0.508 |               0.547 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2025.txt  |
| alis_x2  |        2026 |      22460 |        0 |    300 |              0.364 |              0.212 |                 0.371 |          nan     |          nan     |               nan     |             nan     | arastirma_cikti/sessiz_ml/modeller/alis_x2_2026.txt  |
| satis    |        2020 |     119087 |    67062 |    300 |              0.43  |              0.293 |                 0.433 |            0.813 |            1.01  |                 0.813 |               0.813 | arastirma_cikti/sessiz_ml/modeller/satis_2020.txt    |
| satis    |        2021 |     197610 |   200525 |    300 |              0.532 |              0.356 |                 0.537 |            0.452 |            0.442 |                 0.434 |               0.453 | arastirma_cikti/sessiz_ml/modeller/satis_2021.txt    |
| satis    |        2022 |     390001 |    54008 |    300 |              0.48  |              0.36  |                 0.483 |            0.632 |            0.696 |                 0.626 |               0.634 | arastirma_cikti/sessiz_ml/modeller/satis_2022.txt    |
| satis    |        2023 |     453248 |   152475 |    300 |              0.501 |              0.396 |                 0.504 |            0.497 |            0.482 |                 0.473 |               0.499 | arastirma_cikti/sessiz_ml/modeller/satis_2023.txt    |
| satis    |        2024 |     599210 |   144080 |    300 |              0.504 |              0.418 |                 0.505 |            0.438 |            0.398 |                 0.397 |               0.439 | arastirma_cikti/sessiz_ml/modeller/satis_2024.txt    |
| satis    |        2025 |     745894 |    77971 |    300 |              0.487 |              0.407 |                 0.489 |            0.545 |            0.524 |                 0.517 |               0.547 | arastirma_cikti/sessiz_ml/modeller/satis_2025.txt    |
| satis    |        2026 |     829435 |    40195 |    300 |              0.495 |              0.422 |                 0.496 |            0.635 |            0.59  |                 0.586 |               0.638 | arastirma_cikti/sessiz_ml/modeller/satis_2026.txt    |

## 2) Gormedigi veri: yil yil ileri yuruyen alis modeli (AUC, ust %20 kat)

| etiket   | pazar   | donem   |    n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-----:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_k20    | ABD     | 2019-21 | 6867 | 0.667 |       31.127 |         15.149 |       18.349 | 2.055 |    1375 |
| y_k20    | ABD     | 2022-26 | 7561 | 0.666 |       32.518 |         17.791 |       20.738 | 1.828 |    1513 |
| y_k20    | BIST    | 2019-21 | 1785 | 0.567 |       52.925 |         48.457 |       49.356 | 1.092 |     359 |
| y_k20    | BIST    | 2022-26 | 2610 | 0.526 |       58.126 |         47.005 |       49.234 | 1.237 |     523 |
| y_x2     | ABD     | 2019-21 | 6867 | 0.779 |       12.509 |          2.367 |        4.398 | 5.285 |    1375 |
| y_x2     | ABD     | 2022-26 | 6934 | 0.766 |       19.741 |          4.886 |        7.86  | 4.04  |    1388 |
| y_x2     | BIST    | 2019-21 | 1785 | 0.577 |       53.76  |         47.826 |       49.02  | 1.124 |     359 |
| y_x2     | BIST    | 2022-26 | 2171 | 0.356 |       37.701 |         39.977 |       39.521 | 0.943 |     435 |

## 3a) Alis basarisi: pozitif tahminlerden acilan islemler (maliyet dusulmus)

| pazar   | donem   | secim                      |    n |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |
|:--------|:--------|:---------------------------|-----:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|
| ABD     | 2019-21 | tum_Z0                     | 6867 |            24.771 |              68.414 |          9.407 |       0.492 |         -0.8   |        1.292 |    52.734 |
| ABD     | 2019-21 | model_ust20 (alis tahmini) | 1612 |            31.203 |              67.556 |         16.253 |       1.037 |         -0.8   |        1.837 |    38.914 |
| ABD     | 2019-21 | model_alt80                | 5255 |            22.797 |              68.677 |          7.307 |       0.324 |         -0.8   |        1.124 |    56.973 |
| ABD     | 2022-26 | tum_Z0                     | 7768 |            25.515 |              67.92  |         12.152 |       0.355 |         -0.8   |        1.155 |    49.234 |
| ABD     | 2022-26 | model_ust20 (alis tahmini) | 2003 |            31.653 |              68.298 |         22.067 |       0.711 |         -0.8   |        1.511 |    33.49  |
| ABD     | 2022-26 | model_alt80                | 5765 |            23.382 |              67.788 |          8.708 |       0.231 |         -0.8   |        1.031 |    54.704 |
| BIST    | 2019-21 | tum_Z0                     | 1785 |            43.978 |              59.44  |          9.3   |      10.297 |         -0.8   |       11.097 |    30.952 |
| BIST    | 2019-21 | model_ust20 (alis tahmini) |  210 |            44.286 |              60.952 |          8.571 |      11.768 |         -0.8   |       12.568 |    28.329 |
| BIST    | 2019-21 | model_alt80                | 1575 |            43.937 |              59.238 |          9.397 |      10.101 |         -0.8   |       10.901 |    31.302 |
| BIST    | 2022-26 | tum_Z0                     | 2653 |            42.706 |              58.952 |         12.778 |      10.466 |         -0.8   |       11.266 |    29.803 |
| BIST    | 2022-26 | model_ust20 (alis tahmini) |  324 |            51.543 |              50     |          6.79  |       9.691 |         -0.116 |       10.491 |    27.238 |
| BIST    | 2022-26 | model_alt80                | 2329 |            41.477 |              60.198 |         13.611 |      10.574 |         -0.8   |       11.374 |    30.16  |

## 3b) Alis portfoyu (30 slot)

| pazar   | donem   | secim       |   islem |   portfoy |   kazanan |   islem_basi |   agir |   rastgele_ayni_sayi_medyan |   secilen_oran_yzd |
|:--------|:--------|:------------|--------:|----------:|----------:|-------------:|-------:|----------------------------:|-------------------:|
| ABD     | 2019-21 | tum_Z0      |     446 |    28.104 |    34.753 |        1.955 |  8.744 |                     nan     |            nan     |
| ABD     | 2019-21 | model_ust20 |     462 |    69.693 |    38.312 |        3.893 | 12.338 |                      29.264 |             23.475 |
| ABD     | 2022-26 | tum_Z0      |     741 |    -9.827 |    29.825 |       -0.241 | 14.44  |                     nan     |            nan     |
| ABD     | 2022-26 | model_ust20 |     810 |     3.959 |    30.617 |        0.342 | 21.975 |                      -1.868 |             25.785 |
| BIST    | 2019-21 | tum_Z0      |     496 |   445.71  |    40.927 |       12.927 | 10.685 |                     nan     |            nan     |
| BIST    | 2019-21 | model_ust20 |     179 |    77.483 |    37.989 |       11.416 |  8.38  |                      93.101 |             11.765 |
| BIST    | 2022-26 | tum_Z0      |     809 |  1272.05  |    42.274 |       12.665 | 12.979 |                     nan     |            nan     |
| BIST    | 2022-26 | model_ust20 |     141 |    71.857 |    53.191 |       12.314 |  7.801 |                     161.285 |             12.213 |

## 3c) Satis modeli (y_sat: 20 barda once -%10) ileri yuruyen degerlendirme

| etiket   | pazar   | donem   |      n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-------:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_sat    | ABD     | 2019-21 | 235920 | 0.539 |       26.864 |         19.6   |       20.326 | 1.371 |   23593 |
| y_sat    | ABD     | 2022-26 | 388884 | 0.664 |       33.573 |         17.725 |       19.31  | 1.894 |   38891 |
| y_sat    | BIST    | 2019-21 |  31667 | 0.555 |       33.902 |         29.408 |       29.858 | 1.153 |    3168 |
| y_sat    | BIST    | 2022-26 |  79845 | 0.533 |       34.176 |         28.74  |       29.284 | 1.189 |    7988 |

## 3d) Satis basarisi: ayni girislerde uretim cikisi vs uretim + model satisi

| pazar   | donem   | cikis        |   islem |   portfoy |   kazanan |   islem_basi |   agir |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |   model_satis_n |   dogru_satis_% |   satis_sonrasi_20bar_medyan_% |
|:--------|:--------|:-------------|--------:|----------:|----------:|-------------:|-------:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|----------------:|----------------:|-------------------------------:|
| ABD     | 2019-21 | uretim       |     311 |    23.569 |    35.691 |        2.562 |  9.325 |            26.322 |              67.425 |          9.793 |       0.988 |           -0.8 |        1.788 |    50.607 |             nan |         nan     |                        nan     |
| ABD     | 2019-21 | uretim+model |     536 |    -0.111 |    37.687 |        0.093 |  3.358 |            11.586 |              63.747 |          4.759 |      -0.43  |           -0.8 |        0.37  |    25.967 |            2471 |          34.278 |                          3.057 |
| ABD     | 2022-26 | uretim       |     741 |    -9.827 |    29.825 |       -0.241 | 14.44  |            25.515 |              67.92  |         12.152 |       0.355 |           -0.8 |        1.155 |    49.234 |             nan |         nan     |                        nan     |
| ABD     | 2022-26 | uretim+model |    1198 |   -25.769 |    33.639 |       -0.683 |  2.671 |            11.831 |              62.976 |          3.656 |      -0.114 |           -0.8 |        0.686 |    31.011 |            4272 |          49.696 |                         -0.011 |
| BIST    | 2019-21 | uretim       |     300 |   272.728 |    43.667 |       16.442 | 11     |            43.863 |              60.06  |         10.664 |       9.986 |           -0.8 |       10.786 |    28.891 |             nan |         nan     |                        nan     |
| BIST    | 2019-21 | uretim+model |     430 |   166.88  |    41.395 |        8.012 |  7.674 |            36.922 |              58.853 |          8.954 |       7.698 |           -0.8 |        8.498 |    22.698 |             274 |          39.051 |                          3.846 |
| BIST    | 2022-26 | uretim       |     809 |  1272.05  |    42.274 |       12.665 | 12.979 |            42.706 |              58.952 |         12.778 |      10.466 |           -0.8 |       11.266 |    29.803 |             nan |         nan     |                        nan     |
| BIST    | 2022-26 | uretim+model |    1042 |   314.696 |    42.994 |        4.872 |  7.39  |            29.627 |              58.5   |          9.273 |       3.769 |           -0.8 |        4.569 |    20.204 |            1088 |          39.798 |                          4.904 |

## 4) Sizinti kontrolu (karistirilmis etiket ~0,5 olmali; gelecek kanaryasi sicramali)

| deneme               | pazar   | donem   |   auc |   kat_ust20 |
|:---------------------|:--------|:--------|------:|------------:|
| normal               | ABD     | 2019-21 | 0.68  |       2.077 |
| normal               | ABD     | 2022-26 | 0.667 |       1.85  |
| normal               | BIST    | 2019-21 | 0.562 |       1.189 |
| normal               | BIST    | 2022-26 | 0.536 |       1.184 |
| karistirilmis_etiket | ABD     | 2019-21 | 0.493 |       0.892 |
| karistirilmis_etiket | ABD     | 2022-26 | 0.496 |       0.965 |
| karistirilmis_etiket | BIST    | 2019-21 | 0.491 |       0.834 |
| karistirilmis_etiket | BIST    | 2022-26 | 0.5   |       1.123 |
| gelecek_kanaryasi    | ABD     | 2019-21 | 0.913 |       9.18  |
| gelecek_kanaryasi    | ABD     | 2022-26 | 0.927 |       9.367 |
| gelecek_kanaryasi    | BIST    | 2019-21 | 0.818 |       2.2   |
| gelecek_kanaryasi    | BIST    | 2022-26 | 0.815 |       1.944 |

## Ozellik onemi — alis y_k20

| ozellik       |   pay |
|:--------------|------:|
| mum14         | 0.131 |
| pazar_bist    | 0.117 |
| vol60         | 0.074 |
| logp          | 0.074 |
| piy60         | 0.054 |
| piy20         | 0.034 |
| genislik      | 0.03  |
| mk            | 0.028 |
| tl_log        | 0.023 |
| maxdn60       | 0.022 |
| sektor_ruzgar | 0.022 |
| g250          | 0.021 |
| hk60          | 0.02  |
| dip250        | 0.019 |
| altfitil20    | 0.018 |

## Ozellik onemi — satis

| ozellik       |   pay |
|:--------------|------:|
| piy60         | 0.193 |
| genislik      | 0.154 |
| piy20         | 0.146 |
| vol60         | 0.118 |
| mum14         | 0.108 |
| vol20         | 0.033 |
| mk            | 0.022 |
| vol_oran      | 0.017 |
| sektor_ruzgar | 0.015 |
| yuk250        | 0.014 |
| hk60          | 0.013 |
| logp          | 0.012 |
| pazar_bist    | 0.011 |
| g250          | 0.011 |
| maxdn60       | 0.011 |

## Fon hisseleri 2026: satis modelinin ilk sat sinyali (Haz-Eyl)

| sembol   |   satis_puani_gun | ilk_sat_sinyali     |
|:---------|------------------:|:--------------------|
| TEHOL    |                61 | 2026-06-01 00:00:00 |
| ANELE    |                 0 | NaT                 |
| TRHOL    |                44 | 2026-06-01 00:00:00 |
| OZATD    |                 9 | 2026-08-27 00:00:00 |
| PEKGY    |                33 | NaT                 |
| IEYHO    |                79 | 2026-06-02 00:00:00 |
| DSTKF    |                 0 | NaT                 |
| ISKPL    |                 0 | NaT                 |
| SELEC    |                 0 | NaT                 |
| BIGEN    |                43 | 2026-06-01 00:00:00 |
| KTLEV    |                 0 | NaT                 |
| GUNDG    |                 0 | NaT                 |
| PASEU    |                 0 | NaT                 |
| ODINE    |                57 | 2026-06-01 00:00:00 |
| HEDEF    |                45 | 2026-06-08 00:00:00 |
| TERA     |                19 | NaT                 |
| IZFAS    |                 0 | NaT                 |
| LIDER    |                 0 | NaT                 |
| ALKLC    |                44 | 2026-07-20 00:00:00 |
| UFUK     |                 8 | 2026-08-10 00:00:00 |
| PRZMA    |                 0 | NaT                 |
| BINBN    |                12 | 2026-08-24 00:00:00 |
| DURDO    |                 0 | NaT                 |
