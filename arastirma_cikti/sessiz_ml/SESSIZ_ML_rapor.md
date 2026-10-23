# SESSIZ_ML — SESSIZ_ML v1.0 (2026-10-23, Z0 bolgelerinde alis + satis modeli, ileri yuruyen LightGBM)

Z0 olaylari: 25401 (BIST 5587, ABD 19814). Maliyet: komisyon %0.2 + kayma her yonde %0.3 = islem basina %0.8.

## 1) Egitim kaniti (logloss: ilk/son agac, sabit tahmin kaybi, model dosyasi)

| model    |   test_yili |   n_egitim |   n_test |   agac |   egitim_kayip_ilk |   egitim_kayip_son |   egitim_sabit_tahmin |   test_kayip_ilk |   test_kayip_son |   test_kayip_en_dusuk |   test_sabit_tahmin | dosya                                                |
|:---------|------------:|-----------:|---------:|-------:|-------------------:|-------------------:|----------------------:|-----------------:|-----------------:|----------------------:|--------------------:|:-----------------------------------------------------|
| alis_k20 |        2019 |       6256 |     3308 |    300 |              0.48  |              0.302 |                 0.483 |            0.541 |            0.453 |                 0.451 |               0.546 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2019.txt |
| alis_k20 |        2020 |       8640 |     1713 |    300 |              0.492 |              0.33  |                 0.496 |            0.718 |            0.673 |                 0.652 |               0.722 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2020.txt |
| alis_k20 |        2021 |      10619 |     3634 |    300 |              0.51  |              0.348 |                 0.514 |            0.512 |            0.488 |                 0.481 |               0.514 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2021.txt |
| alis_k20 |        2022 |      14230 |     1452 |    300 |              0.525 |              0.386 |                 0.529 |            0.658 |            0.543 |                 0.537 |               0.663 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2022.txt |
| alis_k20 |        2023 |      16027 |     3502 |    300 |              0.536 |              0.395 |                 0.54  |            0.53  |            0.477 |                 0.472 |               0.533 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2023.txt |
| alis_k20 |        2024 |      19123 |     2529 |    300 |              0.532 |              0.394 |                 0.536 |            0.606 |            0.588 |                 0.565 |               0.609 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2024.txt |
| alis_k20 |        2025 |      21823 |     1933 |    300 |              0.541 |              0.414 |                 0.545 |            0.641 |            0.582 |                 0.582 |               0.645 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2025.txt |
| alis_k20 |        2026 |      24018 |      755 |    300 |              0.55  |              0.429 |                 0.554 |            0.645 |            0.627 |                 0.621 |               0.647 | arastirma_cikti/sessiz_ml/modeller/alis_k20_2026.txt |
| alis_x2  |        2019 |       5128 |     3308 |    300 |              0.285 |              0.103 |                 0.289 |            0.485 |            0.347 |                 0.327 |               0.494 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2019.txt  |
| alis_x2  |        2020 |       6325 |     1713 |    300 |              0.274 |              0.11  |                 0.278 |            0.54  |            0.459 |                 0.435 |               0.546 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2020.txt  |
| alis_x2  |        2021 |       9633 |     3634 |    300 |              0.34  |              0.148 |                 0.348 |            0.303 |            0.259 |                 0.25  |               0.307 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2021.txt  |
| alis_x2  |        2022 |      11346 |     1452 |    300 |              0.365 |              0.175 |                 0.372 |            0.702 |            0.484 |                 0.476 |               0.711 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2022.txt  |
| alis_x2  |        2023 |      14980 |     3502 |    300 |              0.349 |              0.178 |                 0.357 |            0.319 |            0.254 |                 0.251 |               0.323 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2023.txt  |
| alis_x2  |        2024 |      16432 |     2529 |    300 |              0.381 |              0.19  |                 0.388 |            0.352 |            0.396 |                 0.334 |               0.356 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2024.txt  |
| alis_x2  |        2025 |      19934 |     1622 |    300 |              0.368 |              0.198 |                 0.377 |            0.539 |            0.561 |                 0.508 |               0.545 | arastirma_cikti/sessiz_ml/modeller/alis_x2_2025.txt  |
| alis_x2  |        2026 |      22463 |        0 |    300 |              0.367 |              0.212 |                 0.375 |          nan     |          nan     |               nan     |             nan     | arastirma_cikti/sessiz_ml/modeller/alis_x2_2026.txt  |
| satis    |        2020 |     119087 |    66959 |    300 |              0.43  |              0.293 |                 0.433 |            0.816 |            1.017 |                 0.816 |               0.815 | arastirma_cikti/sessiz_ml/modeller/satis_2020.txt    |
| satis    |        2021 |     197611 |   200429 |    300 |              0.533 |              0.357 |                 0.538 |            0.452 |            0.44  |                 0.434 |               0.453 | arastirma_cikti/sessiz_ml/modeller/satis_2021.txt    |
| satis    |        2022 |     389802 |    54008 |    300 |              0.48  |              0.361 |                 0.483 |            0.632 |            0.706 |                 0.626 |               0.634 | arastirma_cikti/sessiz_ml/modeller/satis_2022.txt    |
| satis    |        2023 |     453049 |   152475 |    300 |              0.502 |              0.398 |                 0.504 |            0.497 |            0.482 |                 0.474 |               0.499 | arastirma_cikti/sessiz_ml/modeller/satis_2023.txt    |
| satis    |        2024 |     599011 |   144080 |    300 |              0.504 |              0.419 |                 0.506 |            0.438 |            0.398 |                 0.397 |               0.44  | arastirma_cikti/sessiz_ml/modeller/satis_2024.txt    |
| satis    |        2025 |     745695 |    77971 |    300 |              0.487 |              0.408 |                 0.489 |            0.545 |            0.526 |                 0.518 |               0.547 | arastirma_cikti/sessiz_ml/modeller/satis_2025.txt    |
| satis    |        2026 |     829236 |    40195 |    300 |              0.495 |              0.422 |                 0.497 |            0.635 |            0.591 |                 0.586 |               0.638 | arastirma_cikti/sessiz_ml/modeller/satis_2026.txt    |

## 2) Gormedigi veri: yil yil ileri yuruyen alis modeli (AUC, ust %20 kat)

| etiket   | pazar   | donem   |    n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-----:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_k20    | ABD     | 2019-21 | 6867 | 0.672 |       31.127 |         15.149 |       18.349 | 2.055 |    1375 |
| y_k20    | ABD     | 2022-26 | 7561 | 0.663 |       32.915 |         17.692 |       20.738 | 1.86  |    1513 |
| y_k20    | BIST    | 2019-21 | 1788 | 0.56  |       54.596 |         47.796 |       49.161 | 1.142 |     359 |
| y_k20    | BIST    | 2022-26 | 2610 | 0.533 |       54.876 |         47.82  |       49.234 | 1.148 |     523 |
| y_x2     | ABD     | 2019-21 | 6867 | 0.78  |       12     |          2.495 |        4.398 | 4.811 |    1375 |
| y_x2     | ABD     | 2022-26 | 6934 | 0.768 |       20.029 |          4.814 |        7.86  | 4.16  |    1388 |
| y_x2     | BIST    | 2019-21 | 1788 | 0.578 |       55.71  |         50.035 |       51.174 | 1.113 |     359 |
| y_x2     | BIST    | 2022-26 | 2171 | 0.379 |       39.77  |         39.459 |       39.521 | 1.008 |     435 |

## 3a) Alis basarisi: pozitif tahminlerden acilan islemler (maliyet dusulmus)

| pazar   | donem   | secim                      |    n |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |
|:--------|:--------|:---------------------------|-----:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|
| ABD     | 2019-21 | tum_Z0                     | 6867 |            24.771 |              68.414 |          9.407 |       0.492 |           -0.8 |        1.292 |    52.734 |
| ABD     | 2019-21 | model_ust20 (alis tahmini) |  553 |            33.273 |              67.631 |         16.456 |       1.843 |           -0.8 |        2.643 |    34.183 |
| ABD     | 2019-21 | model_alt80                | 6314 |            24.026 |              68.483 |          8.79  |       0.373 |           -0.8 |        1.173 |    54.359 |
| ABD     | 2022-26 | tum_Z0                     | 7768 |            25.515 |              67.92  |         12.152 |       0.355 |           -0.8 |        1.155 |    49.234 |
| ABD     | 2022-26 | model_ust20 (alis tahmini) |  476 |            29.832 |              70.588 |         20.168 |       1.075 |           -0.8 |        1.875 |    32.664 |
| ABD     | 2022-26 | model_alt80                | 7292 |            25.233 |              67.745 |         11.629 |       0.308 |           -0.8 |        1.108 |    50.316 |
| BIST    | 2019-21 | tum_Z0                     | 1788 |            43.624 |              59.62  |          9.564 |      10.145 |           -0.8 |       10.945 |    30.789 |
| BIST    | 2019-21 | model_ust20 (alis tahmini) | 1038 |            44.701 |              59.056 |         10.983 |      11.711 |           -0.8 |       12.511 |    28.934 |
| BIST    | 2019-21 | model_alt80                |  750 |            42.133 |              60.4   |          7.6   |       7.978 |           -0.8 |        8.778 |    33.356 |
| BIST    | 2022-26 | tum_Z0                     | 2653 |            42.706 |              58.952 |         12.778 |      10.466 |           -0.8 |       11.266 |    29.803 |
| BIST    | 2022-26 | model_ust20 (alis tahmini) | 1968 |            44.309 |              57.317 |         12.551 |      10.641 |           -0.8 |       11.441 |    29.686 |
| BIST    | 2022-26 | model_alt80                |  685 |            38.102 |              63.65  |         13.431 |       9.964 |           -0.8 |       10.764 |    30.137 |

## 3b) Alis portfoyu (30 slot)

| pazar   | donem   | secim       |   islem |   portfoy |   kazanan |   islem_basi |   agir |   rastgele_ayni_sayi_medyan |
|:--------|:--------|:------------|--------:|----------:|----------:|-------------:|-------:|----------------------------:|
| ABD     | 2019-21 | tum_Z0      |     446 |    28.104 |    34.753 |        1.955 |  8.744 |                     nan     |
| ABD     | 2019-21 | model_ust20 |     381 |    33.607 |    32.808 |        2.463 | 14.173 |                      16.449 |
| ABD     | 2022-26 | tum_Z0      |     741 |    -9.827 |    29.825 |       -0.241 | 14.44  |                     nan     |
| ABD     | 2022-26 | model_ust20 |     386 |    35.158 |    32.383 |        2.672 | 17.876 |                       2.982 |
| BIST    | 2019-21 | tum_Z0      |     503 |   477.029 |    40.358 |       12.924 | 11.133 |                     nan     |
| BIST    | 2019-21 | model_ust20 |     471 |   394.667 |    42.887 |       12.542 | 12.102 |                     306.68  |
| BIST    | 2022-26 | tum_Z0      |     809 |  1272.05  |    42.274 |       12.665 | 12.979 |                     nan     |
| BIST    | 2022-26 | model_ust20 |     670 |  1121.66  |    46.567 |       14.443 | 14.03  |                    1271.93  |

## 3c) Satis modeli (y_sat: 20 barda once -%10) ileri yuruyen degerlendirme

| etiket   | pazar   | donem   |      n |   auc |   ust_isabet |   kalan_isabet |   tum_isabet |   kat |   n_ust |
|:---------|:--------|:--------|-------:|------:|-------------:|---------------:|-------------:|------:|--------:|
| y_sat    | ABD     | 2019-21 | 235920 | 0.54  |       26.372 |         19.655 |       20.326 | 1.342 |   23593 |
| y_sat    | ABD     | 2022-26 | 388884 | 0.664 |       33.77  |         17.703 |       19.31  | 1.908 |   38892 |
| y_sat    | BIST    | 2019-21 |  31468 | 0.57  |       37.897 |         29.386 |       30.237 | 1.29  |    3148 |
| y_sat    | BIST    | 2022-26 |  79845 | 0.523 |       32.165 |         28.964 |       29.284 | 1.111 |    7987 |

## 3d) Satis basarisi: ayni girislerde uretim cikisi vs uretim + model satisi

| pazar   | donem   | cikis        |   islem |   portfoy |   kazanan |   islem_basi |   agir |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |   model_satis_n |   dogru_satis_% |   satis_sonrasi_20bar_medyan_% |
|:--------|:--------|:-------------|--------:|----------:|----------:|-------------:|-------:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|----------------:|----------------:|-------------------------------:|
| ABD     | 2019-21 | uretim       |     311 |    23.569 |    35.691 |        2.562 |  9.325 |            26.322 |              67.425 |          9.793 |       0.988 |           -0.8 |        1.788 |    50.607 |             nan |         nan     |                        nan     |
| ABD     | 2019-21 | uretim+model |     525 |     1.671 |    37.333 |        0.206 |  3.81  |            10.897 |              63.241 |          4.897 |      -0.48  |           -0.8 |        0.32  |    25.48  |            2526 |          34.244 |                          2.998 |
| ABD     | 2022-26 | uretim       |     741 |    -9.827 |    29.825 |       -0.241 | 14.44  |            25.515 |              67.92  |         12.152 |       0.355 |           -0.8 |        1.155 |    49.234 |             nan |         nan     |                        nan     |
| ABD     | 2022-26 | uretim+model |    1206 |   -23.02  |    35.24  |       -0.571 |  3.151 |            12.114 |              62.745 |          3.901 |      -0.058 |           -0.8 |        0.742 |    31.215 |            4221 |          50.58  |                         -0.211 |
| BIST    | 2019-21 | uretim       |     295 |   256.817 |    42.373 |       15.776 | 10.847 |            43.23  |              60.381 |         11.133 |       9.714 |           -0.8 |       10.514 |    28.605 |             nan |         nan     |                        nan     |
| BIST    | 2019-21 | uretim+model |     425 |   178.108 |    41.176 |        8.119 |  8.235 |            34.905 |              58.375 |          8.726 |       7.398 |           -0.8 |        8.198 |    21.524 |             331 |          42.296 |                          2.335 |
| BIST    | 2022-26 | uretim       |     809 |  1272.05  |    42.274 |       12.665 | 12.979 |            42.706 |              58.952 |         12.778 |      10.466 |           -0.8 |       11.266 |    29.803 |             nan |         nan     |                        nan     |
| BIST    | 2022-26 | uretim+model |    1124 |   310.007 |    45.463 |        4.328 |  7.295 |            26.762 |              58.161 |          9.009 |       2.799 |           -0.8 |        3.599 |    18.8   |            1203 |          40.565 |                          3.59  |

## 4) Sizinti kontrolu (karistirilmis etiket ~0,5 olmali; gelecek kanaryasi sicramali)

| deneme               | pazar   | donem   |   auc |   kat_ust20 |
|:---------------------|:--------|:--------|------:|------------:|
| normal               | ABD     | 2019-21 | 0.681 |       2.047 |
| normal               | ABD     | 2022-26 | 0.664 |       1.871 |
| normal               | BIST    | 2019-21 | 0.553 |       1.203 |
| normal               | BIST    | 2022-26 | 0.54  |       1.184 |
| karistirilmis_etiket | ABD     | 2019-21 | 0.508 |       1.05  |
| karistirilmis_etiket | ABD     | 2022-26 | 0.497 |       0.994 |
| karistirilmis_etiket | BIST    | 2019-21 | 0.48  |       0.903 |
| karistirilmis_etiket | BIST    | 2022-26 | 0.502 |       1.001 |
| gelecek_kanaryasi    | ABD     | 2019-21 | 0.914 |       9.146 |
| gelecek_kanaryasi    | ABD     | 2022-26 | 0.927 |       9.115 |
| gelecek_kanaryasi    | BIST    | 2019-21 | 0.817 |       2.19  |
| gelecek_kanaryasi    | BIST    | 2022-26 | 0.819 |       1.958 |

## Ozellik onemi — alis y_k20

| ozellik       |   pay |
|:--------------|------:|
| mum14         | 0.129 |
| pazar_bist    | 0.115 |
| logp          | 0.078 |
| vol60         | 0.076 |
| piy60         | 0.053 |
| piy20         | 0.034 |
| genislik      | 0.03  |
| mk            | 0.028 |
| g250          | 0.022 |
| tl_log        | 0.022 |
| sektor_ruzgar | 0.021 |
| hk60          | 0.021 |
| maxdn60       | 0.021 |
| dip250        | 0.018 |
| tl_yzd        | 0.018 |

## Ozellik onemi — satis

| ozellik       |   pay |
|:--------------|------:|
| piy60         | 0.19  |
| genislik      | 0.153 |
| piy20         | 0.148 |
| vol60         | 0.119 |
| mum14         | 0.109 |
| vol20         | 0.033 |
| mk            | 0.021 |
| vol_oran      | 0.017 |
| sektor_ruzgar | 0.015 |
| yuk250        | 0.014 |
| pazar_bist    | 0.012 |
| hk60          | 0.012 |
| logp          | 0.012 |
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
