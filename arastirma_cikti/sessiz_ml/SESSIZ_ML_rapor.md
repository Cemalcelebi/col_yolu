# SESSIZ_ML — SESSIZ_ML v1.3 (2026-10-24, denetim: bar ufuklu embargo, islem basina satis puani, slot hisse basina tek)

Z0 olaylari: 25404 (BIST 5590, ABD 19814). Maliyet: komisyon %0.2 + kayma her yonde %0.3 = islem basina %0.8.

## 1) Egitim kaniti (logloss: ilk/son agac, sabit tahmin kaybi, model dosyasi)

| model    |   test_yili |   n_egitim |   n_test |   agac |   egitim_kayip_ilk |   egitim_kayip_son |   egitim_sabit_tahmin |   test_kayip_ilk |   test_kayip_son |   test_kayip_en_dusuk |   test_sabit_tahmin | dosya                                                |
|:---------|------------:|-----------:|---------:|-------:|-------------------:|-------------------:|----------------------:|-----------------:|-----------------:|----------------------:|--------------------:|:-----------------------------------------------------|
| alis_k20 |        2019 |       6264 |     3309 |    300 |              0.481 |              0.303 |                 0.484 |            0.542 |            0.455 |                 0.452 |               0.546 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2019.txt |
| alis_k20 |        2020 |       8649 |     1710 |    300 |              0.492 |              0.33  |                 0.496 |            0.718 |            0.67  |                 0.646 |               0.723 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2020.txt |
| alis_k20 |        2021 |      10635 |     3635 |    300 |              0.511 |              0.349 |                 0.515 |            0.513 |            0.488 |                 0.482 |               0.515 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2021.txt |
| alis_k20 |        2022 |      14254 |     1453 |    300 |              0.525 |              0.386 |                 0.529 |            0.66  |            0.541 |                 0.536 |               0.664 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2022.txt |
| alis_k20 |        2023 |      16028 |     3504 |    300 |              0.536 |              0.394 |                 0.541 |            0.53  |            0.475 |                 0.47  |               0.533 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2023.txt |
| alis_k20 |        2024 |      19128 |     2530 |    300 |              0.533 |              0.394 |                 0.537 |            0.606 |            0.587 |                 0.565 |               0.609 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2024.txt |
| alis_k20 |        2025 |      21854 |     1933 |    300 |              0.541 |              0.415 |                 0.546 |            0.641 |            0.582 |                 0.581 |               0.645 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2025.txt |
| alis_k20 |        2026 |      24037 |      755 |    300 |              0.55  |              0.429 |                 0.554 |            0.645 |            0.625 |                 0.622 |               0.647 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2026.txt |
| alis_x2  |        2019 |       5204 |     3309 |    300 |              0.287 |              0.105 |                 0.292 |            0.445 |            0.338 |                 0.317 |               0.455 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2019.txt  |
| alis_x2  |        2020 |       6333 |     1710 |    300 |              0.276 |              0.111 |                 0.28  |            0.533 |            0.457 |                 0.429 |               0.539 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2020.txt  |
| alis_x2  |        2021 |       9733 |     3635 |    300 |              0.329 |              0.149 |                 0.336 |            0.304 |            0.267 |                 0.256 |               0.307 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2021.txt  |
| alis_x2  |        2022 |      11349 |     1453 |    300 |              0.355 |              0.175 |                 0.362 |            0.733 |            0.514 |                 0.501 |               0.744 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2022.txt  |
| alis_x2  |        2023 |      14990 |     3504 |    300 |              0.343 |              0.179 |                 0.35  |            0.319 |            0.257 |                 0.254 |               0.323 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2023.txt  |
| alis_x2  |        2024 |      16432 |     2530 |    300 |              0.377 |              0.188 |                 0.384 |            0.353 |            0.42  |                 0.334 |               0.356 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2024.txt  |
| alis_x2  |        2025 |      19957 |     1622 |    300 |              0.365 |              0.197 |                 0.374 |            0.54  |            0.569 |                 0.509 |               0.546 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2025.txt  |
| alis_x2  |        2026 |      22471 |        0 |    300 |              0.365 |              0.212 |                 0.372 |          nan     |          nan     |               nan     |             nan     | arastirma_cikti/sessiz_ml/modeller/alis_x2_2026.txt  |
| satis    |        2020 |     123507 |    67100 |    300 |              0.423 |              0.288 |                 0.426 |            0.821 |            1.048 |                 0.821 |               0.82  | arastirma_cikti/sessiz_ml/modeller/satis_2020.txt    |
| satis    |        2021 |     199123 |   200494 |    300 |              0.53  |              0.355 |                 0.536 |            0.451 |            0.445 |                 0.434 |               0.452 | arastirma_cikti/sessiz_ml/modeller/satis_2021.txt    |
| satis    |        2022 |     397093 |    54045 |    300 |              0.48  |              0.363 |                 0.483 |            0.631 |            0.677 |                 0.622 |               0.633 | arastirma_cikti/sessiz_ml/modeller/satis_2022.txt    |
| satis    |        2023 |     455108 |   152522 |    300 |              0.502 |              0.398 |                 0.504 |            0.497 |            0.48  |                 0.474 |               0.499 | arastirma_cikti/sessiz_ml/modeller/satis_2023.txt    |
| satis    |        2024 |     601547 |   144093 |    300 |              0.503 |              0.417 |                 0.505 |            0.438 |            0.398 |                 0.397 |               0.439 | arastirma_cikti/sessiz_ml/modeller/satis_2024.txt    |
| satis    |        2025 |     749028 |    78005 |    300 |              0.487 |              0.409 |                 0.489 |            0.545 |            0.524 |                 0.518 |               0.547 | arastirma_cikti/sessiz_ml/modeller/satis_2025.txt    |
| satis    |        2026 |     831003 |    40194 |    300 |              0.494 |              0.421 |                 0.496 |            0.636 |            0.59  |                 0.586 |               0.638 | arastirma_cikti/sessiz_ml/modeller/satis_2026.txt    |

## 2) Gormedigi veri: yil yil ileri yuruyen alis modeli (AUC, ust %20 kat)

| etiket   | pazar   | donem   |    n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-----:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_k20    | ABD     | 2019-21 | 6867 | 0.67  |       30.691 |         15.259 |       18.349 | 2.011 |    1375 |
| y_k20    | ABD     | 2022-26 | 7561 | 0.666 |       33.047 |         17.659 |       20.738 | 1.871 |    1513 |
| y_k20    | BIST    | 2019-21 | 1787 | 0.561 |       54.875 |         48.109 |       49.468 | 1.141 |     359 |
| y_k20    | BIST    | 2022-26 | 2614 | 0.536 |       57.905 |         47.056 |       49.235 | 1.231 |     525 |
| y_x2     | ABD     | 2019-21 | 6867 | 0.775 |       12.145 |          2.458 |        4.398 | 4.941 |    1375 |
| y_x2     | ABD     | 2022-26 | 6934 | 0.762 |       19.885 |          4.85  |        7.86  | 4.1   |    1388 |
| y_x2     | BIST    | 2019-21 | 1787 | 0.56  |       51.811 |         47.269 |       48.181 | 1.096 |     359 |
| y_x2     | BIST    | 2022-26 | 2175 | 0.342 |       41.419 |         40.161 |       40.414 | 1.031 |     437 |

## 3a) Alis basarisi: pozitif tahminlerden acilan islemler (maliyet dusulmus)

| pazar   | donem   | secim                      |    n |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |
|:--------|:--------|:---------------------------|-----:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|
| ABD     | 2019-21 | tum_Z0                     | 6867 |            24.771 |              68.414 |          9.407 |       0.492 |         -0.8   |        1.292 |    52.734 |
| ABD     | 2019-21 | model_ust20 (alis tahmini) | 1665 |            31.772 |              67.327 |         16.877 |       1.13  |         -0.8   |        1.93  |    39.531 |
| ABD     | 2019-21 | model_alt80                | 5202 |            22.53  |              68.762 |          7.017 |       0.287 |         -0.8   |        1.087 |    56.96  |
| ABD     | 2022-26 | tum_Z0                     | 7768 |            25.515 |              67.92  |         12.152 |       0.355 |         -0.8   |        1.155 |    49.234 |
| ABD     | 2022-26 | model_ust20 (alis tahmini) | 1987 |            32.411 |              67.589 |         21.792 |       0.955 |         -0.8   |        1.755 |    33.734 |
| ABD     | 2022-26 | model_alt80                | 5781 |            23.145 |              68.033 |          8.839 |       0.148 |         -0.8   |        0.948 |    54.562 |
| BIST    | 2019-21 | tum_Z0                     | 1787 |            44.04  |              59.317 |          9.233 |      10.478 |         -0.8   |       11.278 |    30.928 |
| BIST    | 2019-21 | model_ust20 (alis tahmini) |  191 |            45.55  |              57.592 |          8.901 |      14.104 |         -0.8   |       14.904 |    29.738 |
| BIST    | 2019-21 | model_alt80                | 1596 |            43.86  |              59.524 |          9.273 |      10.044 |         -0.8   |       10.844 |    31.07  |
| BIST    | 2022-26 | tum_Z0                     | 2657 |            42.68  |              58.976 |         12.834 |      10.746 |         -0.8   |       11.546 |    29.803 |
| BIST    | 2022-26 | model_ust20 (alis tahmini) |  358 |            54.469 |              46.369 |          5.307 |      12.473 |          3.909 |       13.273 |    28.14  |
| BIST    | 2022-26 | model_alt80                | 2299 |            40.844 |              60.94  |         14.006 |      10.477 |         -0.8   |       11.277 |    30.062 |

## 3b) Alis portfoyu (30 slot)

| pazar   | donem   | secim       |   islem |   portfoy |   kazanan |   islem_basi |   agir |   rastgele_ayni_sayi_medyan |   secilen_oran_yzd |
|:--------|:--------|:------------|--------:|----------:|----------:|-------------:|-------:|----------------------------:|-------------------:|
| ABD     | 2019-21 | tum_Z0      |     418 |    39.675 |    36.603 |        2.707 |  7.416 |                     nan     |            nan     |
| ABD     | 2019-21 | model_ust20 |     444 |    64.491 |    37.838 |        3.937 | 14.414 |                      30.479 |             24.246 |
| ABD     | 2022-26 | tum_Z0      |     733 |    -3.392 |    31.924 |        0.023 | 15.007 |                     nan     |            nan     |
| ABD     | 2022-26 | model_ust20 |     788 |    18.538 |    31.472 |        0.958 | 20.812 |                       1.328 |             25.579 |
| BIST    | 2019-21 | tum_Z0      |     468 |   479.996 |    42.735 |       14.009 |  9.615 |                     nan     |            nan     |
| BIST    | 2019-21 | model_ust20 |     167 |    92.702 |    42.515 |       14.187 |  8.982 |                      81.832 |             10.688 |
| BIST    | 2022-26 | tum_Z0      |     776 |  1250.76  |    43.041 |       13.33  | 14.304 |                     nan     |            nan     |
| BIST    | 2022-26 | model_ust20 |     143 |   104.746 |    55.944 |       16.609 |  7.692 |                     181.86  |             13.474 |

## 3c) Satis modeli (y_sat: 20 barda once -%10) ileri yuruyen degerlendirme

| etiket   | pazar   | donem   |      n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-------:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_sat    | ABD     | 2019-21 | 235920 | 0.532 |       27.907 |         19.484 |       20.326 | 1.432 |   23593 |
| y_sat    | ABD     | 2022-26 | 388884 | 0.665 |       34.548 |         17.617 |       19.31  | 1.961 |   38891 |
| y_sat    | BIST    | 2019-21 |  31674 | 0.488 |       34.427 |         29.233 |       29.753 | 1.178 |    3169 |
| y_sat    | BIST    | 2022-26 |  79975 | 0.541 |       33.804 |         28.709 |       29.219 | 1.177 |    8002 |

## 3d) Satis basarisi: ayni girislerde uretim cikisi vs uretim + model satisi

| pazar   | donem   | cikis        |   islem |   portfoy |   kazanan |   islem_basi |   agir |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |   model_satis_n |   dogru_satis_% |   satis_sonrasi_20bar_medyan_% |
|:--------|:--------|:-------------|--------:|----------:|----------:|-------------:|-------:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|----------------:|----------------:|-------------------------------:|
| ABD     | 2019-21 | uretim       |     301 |    28.086 |    33.223 |        3.057 |  8.97  |            26.322 |              67.425 |          9.793 |       0.988 |           -0.8 |        1.788 |    50.607 |             nan |         nan     |                        nan     |
| ABD     | 2019-21 | uretim+model |     478 |    15.684 |    39.121 |        1.106 |  3.138 |            12.575 |              64.138 |          5.011 |      -0.292 |           -0.8 |        0.508 |    26.757 |            2355 |          34.14  |                          3.057 |
| ABD     | 2022-26 | uretim       |     733 |    -3.392 |    31.924 |        0.023 | 15.007 |            25.515 |              67.92  |         12.152 |       0.355 |           -0.8 |        1.155 |    49.234 |             nan |         nan     |                        nan     |
| ABD     | 2022-26 | uretim+model |    1079 |   -16.065 |    37.071 |       -0.389 |  3.614 |            12.693 |              62.925 |          4.042 |      -0.057 |           -0.8 |        0.743 |    32.586 |            4016 |          50.398 |                         -0.202 |
| BIST    | 2019-21 | uretim       |     281 |   251.852 |    46.619 |       16.337 |  9.253 |            43.819 |              60     |         10.653 |      10.105 |           -0.8 |       10.905 |    28.879 |             nan |         nan     |                        nan     |
| BIST    | 2019-21 | uretim+model |     336 |   190.929 |    46.429 |       11.124 |  7.143 |            41.106 |              60.101 |          9.648 |       8.764 |           -0.8 |        9.564 |    24.849 |             167 |          37.126 |                          4.091 |
| BIST    | 2022-26 | uretim       |     776 |  1250.76  |    43.041 |       13.33  | 14.304 |            42.68  |              58.976 |         12.834 |      10.746 |           -0.8 |       11.546 |    29.803 |             nan |         nan     |                        nan     |
| BIST    | 2022-26 | uretim+model |     982 |   353.197 |    45.418 |        5.485 |  8.248 |            30.222 |              58.073 |          9.597 |       4.101 |           -0.8 |        4.901 |    20.382 |            1079 |          39.944 |                          4.953 |

## 4) Sizinti kontrolu (karistirilmis etiket ~0,5 olmali; gelecek kanaryasi sicramali)

| deneme               | pazar   | donem   |   auc |   kat_ust20 |
|:---------------------|:--------|:--------|------:|------------:|
| normal               | ABD     | 2019-21 | 0.681 |       2.077 |
| normal               | ABD     | 2022-26 | 0.666 |       1.921 |
| normal               | BIST    | 2019-21 | 0.557 |       1.178 |
| normal               | BIST    | 2022-26 | 0.547 |       1.199 |
| karistirilmis_etiket | ABD     | 2019-21 | 0.502 |       0.966 |
| karistirilmis_etiket | ABD     | 2022-26 | 0.502 |       0.998 |
| karistirilmis_etiket | BIST    | 2019-21 | 0.482 |       0.899 |
| karistirilmis_etiket | BIST    | 2022-26 | 0.498 |       1.131 |
| gelecek_kanaryasi    | ABD     | 2019-21 | 0.913 |       9.215 |
| gelecek_kanaryasi    | ABD     | 2022-26 | 0.926 |       9.282 |
| gelecek_kanaryasi    | BIST    | 2019-21 | 0.819 |       2.18  |
| gelecek_kanaryasi    | BIST    | 2022-26 | 0.818 |       1.962 |

## Ozellik onemi — alis y_k20

| ozellik       |   pay |
|:--------------|------:|
| mum14         | 0.131 |
| pazar_bist    | 0.113 |
| logp          | 0.08  |
| vol60         | 0.073 |
| piy60         | 0.054 |
| piy20         | 0.035 |
| genislik      | 0.031 |
| mk            | 0.028 |
| tl_log        | 0.022 |
| hk60          | 0.021 |
| maxdn60       | 0.021 |
| g250          | 0.021 |
| sektor_ruzgar | 0.021 |
| dip250        | 0.02  |
| tl_yzd        | 0.018 |

## Ozellik onemi — satis

| ozellik       |   pay |
|:--------------|------:|
| piy60         | 0.195 |
| genislik      | 0.151 |
| piy20         | 0.145 |
| vol60         | 0.118 |
| mum14         | 0.11  |
| vol20         | 0.031 |
| mk            | 0.021 |
| vol_oran      | 0.018 |
| sektor_ruzgar | 0.014 |
| yuk250        | 0.014 |
| hk60          | 0.013 |
| logp          | 0.012 |
| pazar_bist    | 0.011 |
| maxdn60       | 0.011 |
| g250          | 0.011 |

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
