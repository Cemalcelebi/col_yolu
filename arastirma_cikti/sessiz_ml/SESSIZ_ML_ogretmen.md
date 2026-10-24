# SESSIZ_ML ogretmen — SESSIZ_ML v1.3 (2026-10-24, denetim: bar ufuklu embargo, islem basina satis puani, slot hisse basina tek)

Maliyet: komisyon %0.2 + kayma her yonde %0.3 = islem basina %0.8

## 1) Egitim kaniti (logloss ilk/son agac, model dosyasi)

| model               |   pozitif |   negatif |   cv_auc_hisse_gruplu |   agac |   egitim_kayip_ilk |   egitim_kayip_son |   ayrik_hisse_kayip_ilk |   ayrik_hisse_kayip_son |   esik | dosya                                                      |
|:--------------------|----------:|----------:|----------------------:|-------:|-------------------:|-------------------:|------------------------:|------------------------:|-------:|:-----------------------------------------------------------|
| ogretmen_alim       |     10150 |    150000 |                 0.736 |    300 |              0.239 |              0.209 |                   0.184 |                   0.321 |  0.601 | arastirma_cikti/sessiz_ml/modeller/ogretmen_alim.txt       |
| ogretmen_alim_kesim |      5695 |     80945 |                 0.596 |    300 |              0.256 |              0.176 |                   0.153 |                   0.253 |  0.559 | arastirma_cikti/sessiz_ml/modeller/ogretmen_alim_kesim.txt |
| ogretmen_satis      |       943 |    150000 |                 0.847 |    300 |              0.033 |              0.002 |                   0.035 |                   0.029 |  0.002 | arastirma_cikti/sessiz_ml/modeller/ogretmen_satis.txt      |

## 2) Gormedigi veri: tarih kesimli ogretmen (kesim oncesiyle egitildi, sonrasinda fon hisselerini tanidi mi)

| ogretmen   | egitim       |   fon_gun_kesim_sonrasi |   fon_isaretlenme_% |   gorulmemis_hisse_gun |   gorulmemis_isaretlenme_% |   ayirt_kat |
|:-----------|:-------------|------------------------:|--------------------:|-----------------------:|---------------------------:|------------:|
| alim       | < 2025-07-01 |                    4455 |              35.892 |                  83904 |                      6.128 |       5.857 |

## 3a) Tuttu mu: iz goren hisselerde sonuc vs ayni hisselerin rastgele gunleri

| ogretmen   | sonuc   | pazar   | donem         |    n |   isabet_% |   taban_isabet_% |   kat |   r60_medyan_% |   taban_r60_medyan_% |   r20_medyan_% |   taban_r20_medyan_% |
|:-----------|:--------|:--------|:--------------|-----:|-----------:|-----------------:|------:|---------------:|---------------------:|---------------:|---------------------:|
| alim       | y_k20   | ABD     | 2016-21       | 7454 |     36.048 |           23.237 | 1.551 |          2.26  |                3.306 |        nan     |              nan     |
| alim       | y_k20   | ABD     | 2022-26       | 6514 |     36.537 |           25.876 | 1.412 |          0.441 |                1.162 |        nan     |              nan     |
| alim       | y_k20   | BIST    | 2016-21       | 2471 |     43.343 |           38.08  | 1.138 |          1.724 |                2.646 |        nan     |              nan     |
| alim       | y_k20   | BIST    | 2022-26       | 2332 |     46.012 |           40.809 | 1.127 |          5.558 |                3.448 |        nan     |              nan     |
| alim       | y_x2    | ABD     | 2016-21       | 7454 |     23.88  |           10.275 | 2.324 |          2.26  |                3.306 |        nan     |              nan     |
| alim       | y_x2    | ABD     | 2022-26       | 5378 |     27.743 |           11.907 | 2.33  |          0.527 |                1.107 |        nan     |              nan     |
| alim       | y_x2    | BIST    | 2016-21       | 2471 |     36.22  |           32.198 | 1.125 |          1.724 |                2.646 |        nan     |              nan     |
| alim       | y_x2    | BIST    | 2022-26       | 2133 |     41.772 |           39.964 | 1.045 |          6.325 |                5.636 |        nan     |              nan     |
| satis      | y_dus20 | ABD     | 2016-21       | 6860 |     41.414 |           24.402 | 1.697 |        nan     |              nan     |          1.652 |                1.274 |
| satis      | y_dus20 | ABD     | 2022-26       | 8854 |     44.319 |           31.062 | 1.427 |        nan     |              nan     |          0     |                0.27  |
| satis      | y_dus20 | BIST    | 2016-21       |  864 |     38.889 |           28.303 | 1.374 |        nan     |              nan     |         -0.303 |                0.585 |
| satis      | y_dus20 | BIST    | 2022-26       | 1669 |     41.702 |           36.283 | 1.149 |        nan     |              nan     |         -0.881 |                0.755 |
| alim_kesim | y_k20   | ABD     | >= 2025-07-01 | 2133 |     42.569 |           29.089 | 1.463 |          6.248 |                2.084 |        nan     |              nan     |
| alim_kesim | y_k20   | BIST    | >= 2025-07-01 |  480 |     37.083 |           36.123 | 1.027 |         -5.224 |               -2.952 |        nan     |              nan     |

## 3b) Alim izinden acilan islemler (uretim cikisi, maliyet dusulmus)

| secim        | pazar   | donem   |    n |   hedefe_ulasan_% |   zararla_kapanan_% |   agir_zarar_% |   ort_net_% |   medyan_net_% |   ort_brut_% |   ort_bar |   portfoy_% |
|:-------------|:--------|:--------|-----:|------------------:|--------------------:|---------------:|------------:|---------------:|-------------:|----------:|------------:|
| alim_izi     | ABD     | 2016-21 | 7454 |            31.876 |              72.86  |         13.55  |       1.802 |           -0.8 |        2.602 |    23.536 |      56.799 |
| alim_izi     | ABD     | 2022-26 | 6716 |            31.522 |              74.36  |         13.431 |       1.932 |           -0.8 |        2.732 |    19.777 |     272.638 |
| alim_izi     | BIST    | 2016-21 | 2471 |            35.573 |              69.972 |         13.153 |       6.042 |           -0.8 |        6.842 |    23.892 |     762.824 |
| alim_izi     | BIST    | 2022-26 | 2370 |            39.114 |              64.852 |         12.743 |       8.655 |           -0.8 |        9.455 |    23.316 |     605.331 |
| rastgele_gun | ABD     | 2016-21 | 8496 |            24.659 |              71.128 |          5.579 |       1.244 |           -0.8 |        2.044 |    38.077 |      90.877 |
| rastgele_gun | ABD     | 2022-26 | 8423 |            22.32  |              76.671 |          7.468 |      -0.012 |           -0.8 |        0.788 |    27.767 |      27.966 |
| rastgele_gun | BIST    | 2016-21 | 1523 |            28.628 |              72.948 |          8.011 |       3.155 |           -0.8 |        3.955 |    26.808 |     148.815 |
| rastgele_gun | BIST    | 2022-26 | 1558 |            32.349 |              69.512 |          9.756 |       4.32  |           -0.8 |        5.12  |    21.63  |     204.109 |

## Ogretmenin gordugu: fon gunleri vs diger hisseler (ozellik medyanlari)

| ozellik       |   fon_alim_medyan |   fon_satis_medyan |   diger_medyan |
|:--------------|------------------:|-------------------:|---------------:|
| g             |             0.091 |              0.238 |         -0.001 |
| mk            |             0.985 |              1.089 |          0.925 |
| verim         |             0.181 |              0.425 |         -0.003 |
| dd            |            -0.139 |             -0.119 |         -0.143 |
| udvr          |             1.53  |              2.144 |          1.146 |
| hk            |             0.826 |              0.738 |          0.89  |
| emilim        |             0.875 |              0.766 |          0.964 |
| vcv           |             0.591 |              0.654 |          0.519 |
| dh            |             0.83  |              0.871 |          0.823 |
| emilim_gun    |             0     |              0     |          0     |
| g5            |             0.022 |              0.067 |          0     |
| g60           |             0.289 |              0.782 |          0.006 |
| g120          |             0.607 |              1.548 |          0.03  |
| g250          |             1.437 |              6.655 |          0.171 |
| yuk250        |            -0.123 |             -0.026 |         -0.253 |
| dip250        |             1.653 |              7.543 |          0.426 |
| konum250      |             0.817 |              0.97  |          0.472 |
| vol20         |             0.034 |              0.037 |          0.027 |
| vol60         |             0.036 |              0.04  |          0.029 |
| vol_oran      |             0.973 |              0.943 |          0.956 |
| mum14         |             0.047 |              0.059 |          0.036 |
| sma20_uz      |             0.041 |              0.116 |         -0.003 |
| sma50_uz      |             0.106 |              0.275 |         -0.006 |
| sma200_uz     |             0.423 |              0.934 |          0.02  |
| sma50_egim    |             0.042 |              0.101 |          0     |
| rsi14         |            58.274 |             70.676 |         49.193 |
| maxup60       |             0.1   |              0.1   |          0.098 |
| maxdn60       |            -0.096 |             -0.1   |         -0.073 |
| tavan60       |             2     |              3     |          1     |
| taban60       |             1     |              1     |          0     |
| r2_120        |             0.668 |              0.846 |          0.38  |
| tl_log        |             8.05  |              8.707 |          7.723 |
| hk60          |             0.888 |              0.848 |          0.921 |
| clv20         |             0.482 |              0.568 |          0.422 |
| doji20        |             0.2   |              0.15  |          0.15  |
| altfitil20    |             0.241 |              0.262 |          0.223 |
| gapup20       |             0.1   |              0.1   |          0.1   |
| logp          |             1.517 |              2.256 |          1.198 |
| tl_yzd        |             0.717 |              0.888 |          0.5   |
| g60_yzd       |             0.853 |              0.967 |          0.493 |
| sektor_ruzgar |             0.004 |             -0.004 |         -0.002 |

## Ogretmen ozellik onemi

| ozellik       |   onem_alim |   onem_satis |
|:--------------|------------:|-------------:|
| dip250        |       0.193 |        0.526 |
| logp          |       0.148 |        0.063 |
| g250          |       0.087 |        0.111 |
| maxdn60       |       0.058 |        0.039 |
| tl_log        |       0.057 |        0.043 |
| tl_yzd        |       0.055 |        0.002 |
| maxup60       |       0.049 |        0.03  |
| hk60          |       0.032 |        0.03  |
| mum14         |       0.029 |        0.001 |
| g60_yzd       |       0.027 |        0.003 |
| vcv           |       0.024 |        0.005 |
| vol60         |       0.023 |        0.002 |
| r2_120        |       0.022 |        0.004 |
| sma200_uz     |       0.021 |        0.001 |
| emilim        |       0.018 |        0.002 |
| yuk250        |       0.017 |        0.01  |
| altfitil20    |       0.016 |        0.001 |
| clv20         |       0.015 |        0.002 |
| g120          |       0.015 |        0.002 |
| sektor_ruzgar |       0.012 |        0.005 |
