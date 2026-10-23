# SESSIZ_ML ogretmen — SESSIZ_ML v1.0 (2026-10-23, Z0 bolgelerinde alis + satis modeli, ileri yuruyen LightGBM)

Maliyet: komisyon %0.2 + kayma her yonde %0.3 = islem basina %0.8

## 1) Egitim kaniti (logloss ilk/son agac, model dosyasi)

| model               |   pozitif |   negatif |   cv_auc_hisse_gruplu |   agac |   egitim_kayip_ilk |   egitim_kayip_son |   ayrik_hisse_kayip_ilk |   ayrik_hisse_kayip_son |   esik | dosya                                                      |
|:--------------------|----------:|----------:|----------------------:|-------:|-------------------:|-------------------:|------------------------:|------------------------:|-------:|:-----------------------------------------------------------|
| ogretmen_alim       |     10121 |    150000 |                 0.731 |    300 |              0.237 |              0.211 |                   0.182 |                   0.319 |  0.601 | arastirma_cikti/sessiz_ml/modeller/ogretmen_alim.txt       |
| ogretmen_alim_kesim |      5666 |     80945 |                 0.59  |    300 |              0.255 |              0.179 |                   0.153 |                   0.249 |  0.552 | arastirma_cikti/sessiz_ml/modeller/ogretmen_alim_kesim.txt |
| ogretmen_satis      |       943 |    150000 |                 0.84  |    300 |              0.034 |              0.002 |                   0.037 |                   0.03  |  0.002 | arastirma_cikti/sessiz_ml/modeller/ogretmen_satis.txt      |

## 2) Gormedigi veri: tarih kesimli ogretmen (kesim oncesiyle egitildi, sonrasinda fon hisselerini tanidi mi)

| ogretmen   | egitim       |   fon_gun_kesim_sonrasi |   fon_isaretlenme_% |   gorulmemis_hisse_gun |   gorulmemis_isaretlenme_% |   ayirt_kat |
|:-----------|:-------------|------------------------:|--------------------:|-----------------------:|---------------------------:|------------:|
| alim       | < 2025-07-01 |                    4455 |              35.241 |                  83904 |                      5.677 |       6.208 |

## 3a) Tuttu mu: iz goren hisselerde sonuc vs ayni hisselerin rastgele gunleri

| ogretmen   | sonuc   | pazar   | donem         |    n |   isabet_% |   taban_isabet_% |   kat |   r60_medyan_% |   taban_r60_medyan_% |   r20_medyan_% |   taban_r20_medyan_% |
|:-----------|:--------|:--------|:--------------|-----:|-----------:|-----------------:|------:|---------------:|---------------------:|---------------:|---------------------:|
| alim       | y_k20   | ABD     | 2016-21       | 8931 |     35.965 |           23.237 | 1.548 |          2.41  |                3.306 |        nan     |              nan     |
| alim       | y_k20   | ABD     | 2022-26       | 7562 |     35.983 |           25.876 | 1.391 |          0.535 |                1.162 |        nan     |              nan     |
| alim       | y_k20   | BIST    | 2016-21       | 2521 |     42.166 |           37.748 | 1.117 |          2.664 |                2.941 |        nan     |              nan     |
| alim       | y_k20   | BIST    | 2022-26       | 2245 |     45.39  |           40.664 | 1.116 |          4.629 |                3.162 |        nan     |              nan     |
| alim       | y_x2    | ABD     | 2016-21       | 8931 |     24.23  |           10.275 | 2.358 |          2.41  |                3.306 |        nan     |              nan     |
| alim       | y_x2    | ABD     | 2022-26       | 6240 |     27.949 |           11.907 | 2.347 |          0.691 |                1.107 |        nan     |              nan     |
| alim       | y_x2    | BIST    | 2016-21       | 2521 |     39.072 |           33.409 | 1.169 |          2.664 |                2.941 |        nan     |              nan     |
| alim       | y_x2    | BIST    | 2022-26       | 2037 |     38.292 |           37.656 | 1.017 |          5.544 |                5.295 |        nan     |              nan     |
| satis      | y_dus20 | ABD     | 2016-21       | 7064 |     39.057 |           24.402 | 1.601 |        nan     |              nan     |          2.057 |                1.274 |
| satis      | y_dus20 | ABD     | 2022-26       | 8491 |     43.799 |           31.062 | 1.41  |        nan     |              nan     |         -0.19  |                0.27  |
| satis      | y_dus20 | BIST    | 2016-21       |  873 |     38.373 |           28.441 | 1.349 |        nan     |              nan     |         -1.084 |                0.555 |
| satis      | y_dus20 | BIST    | 2022-26       | 1753 |     42.27  |           36.383 | 1.162 |        nan     |              nan     |         -1.594 |                0.519 |
| alim_kesim | y_k20   | ABD     | >= 2025-07-01 | 2792 |     42.944 |           29.089 | 1.476 |          7.193 |                2.084 |        nan     |              nan     |
| alim_kesim | y_k20   | BIST    | >= 2025-07-01 |  440 |     38.182 |           36.123 | 1.057 |         -6.438 |               -2.952 |        nan     |              nan     |

## 3b) Alim izinden acilan islemler (uretim cikisi, maliyet dusulmus)

| secim        | pazar   | donem   |    n |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |   portfoy_% |
|:-------------|:--------|:--------|-----:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|------------:|
| alim_izi     | ABD     | 2016-21 | 8931 |            30.724 |              73.418 |         13.358 |       4.057 |           -0.8 |        4.857 |    23.081 |      22.133 |
| alim_izi     | ABD     | 2022-26 | 7803 |            31.078 |              74.125 |         14.751 |       1.637 |           -0.8 |        2.437 |    19.629 |     128.969 |
| alim_izi     | BIST    | 2016-21 | 2521 |            34.708 |              70.369 |         12.257 |       5.594 |           -0.8 |        6.394 |    23.211 |     494.134 |
| alim_izi     | BIST    | 2022-26 | 2291 |            38.804 |              65.168 |         13.924 |       8.354 |           -0.8 |        9.154 |    23.786 |     533.831 |
| rastgele_gun | ABD     | 2016-21 | 8496 |            24.659 |              71.128 |          5.579 |       1.244 |           -0.8 |        2.044 |    38.077 |     106.684 |
| rastgele_gun | ABD     | 2022-26 | 8423 |            22.32  |              76.671 |          7.468 |      -0.012 |           -0.8 |        0.788 |    27.767 |      -1.313 |
| rastgele_gun | BIST    | 2016-21 | 1523 |            28.299 |              73.145 |          8.207 |       3.063 |           -0.8 |        3.863 |    26.884 |     155.228 |
| rastgele_gun | BIST    | 2022-26 | 1558 |            32.157 |              69.705 |          9.884 |       4.165 |           -0.8 |        4.965 |    21.379 |     256.22  |

## Ogretmenin gordugu: fon gunleri vs diger hisseler (ozellik medyanlari)

| ozellik       |   fon_alim_medyan |   fon_satis_medyan |   diger_medyan |
|:--------------|------------------:|-------------------:|---------------:|
| g             |             0.09  |              0.246 |         -0.001 |
| mk            |             0.985 |              1.074 |          0.925 |
| verim         |             0.18  |              0.445 |         -0.004 |
| dd            |            -0.14  |             -0.112 |         -0.143 |
| udvr          |             1.529 |              2.152 |          1.145 |
| hk            |             0.832 |              0.715 |          0.893 |
| emilim        |             0.887 |              0.78  |          0.966 |
| vcv           |             0.59  |              0.647 |          0.519 |
| dh            |             0.83  |              0.871 |          0.823 |
| emilim_gun    |             0     |              0     |          0     |
| g5            |             0.022 |              0.069 |          0     |
| g60           |             0.285 |              0.75  |          0.005 |
| g120          |             0.599 |              1.584 |          0.029 |
| g250          |             1.416 |              6.493 |          0.161 |
| yuk250        |            -0.126 |             -0.023 |         -0.255 |
| dip250        |             1.634 |              8.014 |          0.423 |
| konum250      |             0.814 |              0.974 |          0.469 |
| vol20         |             0.034 |              0.037 |          0.027 |
| vol60         |             0.036 |              0.039 |          0.029 |
| vol_oran      |             0.972 |              0.943 |          0.956 |
| mum14         |             0.047 |              0.058 |          0.036 |
| sma20_uz      |             0.04  |              0.121 |         -0.003 |
| sma50_uz      |             0.105 |              0.281 |         -0.006 |
| sma200_uz     |             0.418 |              0.935 |          0.019 |
| sma50_egim    |             0.042 |              0.098 |          0     |
| rsi14         |            58.156 |             71.166 |         49.177 |
| maxup60       |             0.1   |              0.1   |          0.098 |
| maxdn60       |            -0.096 |             -0.1   |         -0.073 |
| tavan60       |             2     |              3     |          1     |
| taban60       |             1     |              1     |          0     |
| r2_120        |             0.67  |              0.851 |          0.378 |
| tl_log        |             8.049 |              8.707 |          7.723 |
| hk60          |             0.891 |              0.79  |          0.923 |
| clv20         |             0.482 |              0.578 |          0.422 |
| doji20        |             0.2   |              0.15  |          0.15  |
| altfitil20    |             0.241 |              0.261 |          0.223 |
| gapup20       |             0.1   |              0.1   |          0.1   |
| logp          |             1.514 |              2.233 |          1.198 |
| tl_yzd        |             0.717 |              0.888 |          0.5   |
| g60_yzd       |             0.853 |              0.967 |          0.493 |
| sektor_ruzgar |             0.004 |             -0.004 |         -0.002 |

## Ogretmen ozellik onemi

| ozellik    |   onem_alim |   onem_satis |
|:-----------|------------:|-------------:|
| dip250     |       0.197 |        0.592 |
| logp       |       0.14  |        0.079 |
| g250       |       0.089 |        0.017 |
| maxdn60    |       0.062 |        0.043 |
| tl_log     |       0.059 |        0.041 |
| maxup60    |       0.054 |        0.031 |
| tl_yzd     |       0.052 |        0.003 |
| hk60       |       0.031 |        0.03  |
| mum14      |       0.029 |        0.001 |
| g60_yzd    |       0.027 |        0.002 |
| vcv        |       0.023 |        0.006 |
| r2_120     |       0.022 |        0.005 |
| vol60      |       0.022 |        0.001 |
| emilim     |       0.021 |        0.001 |
| yuk250     |       0.019 |        0.011 |
| g120       |       0.018 |        0.002 |
| sma200_uz  |       0.016 |        0.001 |
| clv20      |       0.016 |        0.003 |
| altfitil20 |       0.015 |        0.001 |
| mk         |       0.013 |        0.001 |
