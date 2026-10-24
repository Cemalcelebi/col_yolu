# FON_IZI gosterge bataryasi — FON_IZI v1.6 (2026-10-24, denetim v1.6: fi_duzelt yukari/piyasa gunu, K13 pencere, esli kutu gecmis bilgi, K10 o an bilinen; yukselis izi + hacim esligi + gosterge/uyumsuzluk/Fibonacci/blok hacim/KAP; denetim duzeltmeleri; KAP fon raporlari: defter + fon girisi testi)

Soru (Cemal, 23 Eki): fonlar hisseleri alirken iz birakmadi mi? Mum ve hacim disinda her gosterge, uyumsuzluk, Fibonacci.

## Fon hisselerinde blok hacim gunleri (hacim >= 20x onceki 20 gun medyani, dip -> tepe)

| sembol   | tarih      |   r_yzd |   hacim_kat |   kilit_tavan_onceki5 | faz   |
|:---------|:-----------|--------:|------------:|----------------------:|:------|
| ANELE    | 2025-07-29 |    3.69 |       20.3  |                     0 | ERKEN |
| ANELE    | 2026-04-10 |    9.9  |       34.35 |                     0 | KOSU  |
| BIGEN    | 2026-07-23 |    9.96 |       57.41 |                     0 | KOSU  |
| DURDO    | 2024-09-17 |   -2.37 |       24.65 |                     0 | KOSU  |
| DURDO    | 2024-09-20 |   -5.63 |       22.64 |                     0 | KOSU  |
| DURDO    | 2024-09-25 |    9.98 |       29.5  |                     0 | KOSU  |
| GUNDG    | 2025-10-22 |    0.55 |       21.67 |                     0 | KOSU  |
| OZATD    | 2026-04-30 |    9.94 |       26.32 |                     2 | KOSU  |
| OZATD    | 2026-05-14 |    9.95 |       27.65 |                     5 | KOSU  |
| PASEU    | 2026-04-29 |   -5.53 |       36.58 |                     0 | KOSU  |
| PASEU    | 2026-04-30 |    8.82 |       23.99 |                     0 | KOSU  |
| SELEC    | 2026-06-15 |    9.98 |       35.23 |                     0 | KOSU  |
| SELEC    | 2026-06-19 |    2.13 |       21.14 |                     2 | KOSU  |
| TRHOL    | 2025-01-10 |    0    |      191.63 |                     0 | ERKEN |
| UFUK     | 2025-10-20 |    9.92 |       25.14 |                     0 | KOSU  |

## Fon hisseleri: 100 gunde sinyal sikligi (ONCE = dipten onceki 120 bar, ERKEN = dip -> 2 kat, KOSU = 2 kat -> tepe; DIGER = fon disi BIST 2024-26)

| sinyal                 |    ONCE |   ERKEN |    KOSU |     DIGER |   ONCE/DIGER |   ERKEN/DIGER |   KOSU/DIGER |
|:-----------------------|--------:|--------:|--------:|----------:|-------------:|--------------:|-------------:|
| rsi_30_alti            |    5.81 |    1.91 |    2.16 |      3.49 |         1.67 |          0.55 |         0.62 |
| rsi_70_ustu            |    8.59 |   11.73 |   30.73 |      6.86 |         1.25 |          1.71 |         4.48 |
| rsi_50_kesme           |    3.94 |    5.26 |    3.68 |      5.44 |         0.73 |          0.97 |         0.68 |
| stoch_20_donus         |    6.57 |    5.26 |    4.05 |      6.55 |         1    |          0.8  |         0.62 |
| wr_80_alti             |   33.52 |   17.24 |   13.04 |     27.13 |         1.24 |          0.64 |         0.48 |
| cci_100_alti           |   12.44 |    4.49 |    4.92 |     10.07 |         1.23 |          0.45 |         0.49 |
| cci_100_ustu           |   10.41 |   20.96 |   23.25 |     13.97 |         0.75 |          1.5  |         1.67 |
| mfi_20_alti            |    5.06 |    1.1  |    1.23 |      2.65 |         1.91 |          0.42 |         0.46 |
| mfi_80_ustu            |    8.29 |   11.8  |   19.23 |      6.63 |         1.25 |          1.78 |         2.9  |
| cmf_pozitif            |   25.58 |   21.4  |   45.61 |     16.52 |         1.55 |          1.3  |         2.76 |
| cmf_negatif            |   41.51 |   41.07 |   24.35 |     51.8  |         0.8  |          0.79 |         0.47 |
| obv_lider              |    2.33 |    2.5  |    4.5  |      2.52 |         0.92 |          0.99 |         1.79 |
| ad_birikim_yatay       |    0.61 |    0.4  |    0.9  |      0.62 |         0.98 |          0.66 |         1.45 |
| macd_al_sifir_alti     |    2.33 |    1.54 |    1.02 |      2.54 |         0.91 |          0.61 |         0.4  |
| macd_sifir_kesme       |    1.11 |    2.13 |    1.09 |      1.73 |         0.64 |          1.23 |         0.63 |
| adx_25_trend           |    0.81 |    1.76 |    1.09 |      1.12 |         0.72 |          1.57 |         0.97 |
| aroon_yukari           |   22.24 |   29.41 |   46.02 |     22.35 |         1    |          1.32 |         2.06 |
| bb_sikisma             |   15.67 |   16.54 |   15.67 |     17.64 |         0.89 |          0.94 |         0.89 |
| bb_ust_kirilim         |    5.92 |   12.13 |   14.06 |      7.61 |         0.78 |          1.59 |         1.85 |
| bb_alt_kirilim         |    5.06 |    1.8  |    2.31 |      4.24 |         1.19 |          0.43 |         0.54 |
| squeeze_yukari_cozulme |    1.21 |    1.88 |    0.75 |      1.11 |         1.09 |          1.69 |         0.68 |
| bulut_ustu_kesme       |    1.77 |    2.9  |    1.45 |      2.38 |         0.74 |          1.22 |         0.61 |
| tenkan_kijun_kesme     |    1.97 |    3.2  |    2.08 |      2.42 |         0.82 |          1.32 |         0.86 |
| altin_kesisim          |    0.1  |    0.4  |    0.25 |      0.3  |         0.33 |          1.33 |         0.83 |
| fib_618_bolge          |   12.54 |    6.99 |    2.82 |      9.17 |         1.37 |          0.76 |         0.31 |
| fib_382_bolge          |    7.03 |    3.31 |    7.95 |      8.46 |         0.83 |          0.39 |         0.94 |
| fib_dip_bolge          |   12.49 |   11.99 |    1.06 |     17.76 |         0.7  |          0.67 |         0.06 |
| fib_tepe_bolge         |   10.47 |    3.53 |   36.61 |      7.35 |         1.42 |          0.48 |         4.98 |
| force_guclu            |   24.27 |   33.49 |   43.96 |     23.77 |         1.02 |          1.41 |         1.85 |
| ulcer_sakin_trend      |    8.7  |   16.36 |   27.16 |     12.71 |         0.68 |          1.29 |         2.14 |
| blok_hacim             |    0.1  |    0.07 |    0.16 |      0.06 |         1.58 |          1.15 |         2.42 |
| blok_tavan             |    0    |    0    |    0.08 |      0.01 |         0    |          0    |         6.43 |
| blok_seri_ici          |    0    |    0    |    0.02 |      0    |         0    |          0    |        12.6  |
| blok_taban             |    0    |    0    |    0    |      0.01 |         0    |          0    |         0    |
| kilit_tavan            |    0.4  |    0.4  |    0.91 |      0.17 |         2.39 |          2.39 |         5.37 |
| uy_rsi_boga            |    0.71 |    0.59 |    0.25 |      0.71 |         0.99 |          0.82 |         0.35 |
| uy_rsi_gizli_boga      |    0.66 |    0.99 |    1.23 |      0.73 |         0.9  |          1.36 |         1.69 |
| uy_rsi_ayi             |    0.66 |    0.74 |    1.09 |      0.68 |         0.96 |          1.08 |         1.59 |
| uy_macd_boga           |    1.21 |    0.59 |    0.49 |      1.13 |         1.08 |          0.52 |         0.43 |
| uy_macd_gizli_boga     |    0.71 |    1.21 |    1.59 |      1.06 |         0.67 |          1.14 |         1.5  |
| uy_macd_ayi            |    0.86 |    1.1  |    1.34 |      0.92 |         0.94 |          1.2  |         1.46 |
| uy_obv_boga            |    1.16 |    0.85 |    0.69 |      1.05 |         1.11 |          0.8  |         0.66 |
| uy_obv_gizli_boga      |    0.25 |    0.4  |    0.56 |      0.59 |         0.43 |          0.69 |         0.95 |
| uy_obv_ayi             |    0.3  |    0.48 |    0.42 |      0.45 |         0.67 |          1.06 |         0.93 |
| uy_mfi_boga            |    0.91 |    0.7  |    0.45 |      1.02 |         0.89 |          0.69 |         0.45 |
| uy_mfi_gizli_boga      |    0.91 |    1.25 |    1.43 |      0.99 |         0.92 |          1.27 |         1.45 |
| uy_mfi_ayi             |    0.96 |    0.88 |    1.49 |      0.87 |         1.11 |          1.02 |         1.72 |
| uy_cmf_boga            |    1.16 |    0.66 |    0.49 |      1.01 |         1.15 |          0.66 |         0.48 |
| uy_cmf_gizli_boga      |    0.76 |    1.25 |    1.48 |      1.04 |         0.73 |          1.2  |         1.42 |
| uy_cmf_ayi             |    0.96 |    0.88 |    1.35 |      0.96 |         1    |          0.92 |         1.4  |
| kap_vbts_tedbir        |    0.96 |    0.74 |    1.96 |      0.65 |         1.48 |          1.13 |         3.02 |
| kap_tipe_donusum       |    1.62 |    0.81 |    1.03 |      1.01 |         1.6  |          0.8  |         1.02 |
| kap_toptan             |    0.05 |    0.15 |    0.49 |      0.06 |         0.83 |          2.41 |         8.04 |
| kap_pay_alim_satim     |    0.71 |    0.88 |    1.56 |      0.85 |         0.84 |          1.04 |         1.85 |
| kap_devre_kesici       |   10.87 |    6.32 |   10.35 |      6.8  |         1.6  |          0.93 |         1.52 |
| kap_olagan_disi        |    0.1  |    0.22 |    0.53 |      0.12 |         0.86 |          1.88 |         4.47 |
| kap_spk_yasak          |    0.46 |    0.48 |    0.53 |      0.35 |         1.28 |          1.35 |         1.48 |
| kap_fiili_dolasim      |    0.2  |    0.15 |    0.64 |      0.11 |         1.86 |          1.35 |         5.92 |
| kap_piyasa_yapici      |    0    |    0    |    0    |      0.32 |         0    |          0    |         0    |
| kap_soylenti           |    0.1  |    0.07 |    0.06 |      0.04 |         2.33 |          1.7  |         1.38 |
| _gun_sayisi            | 1978    | 2720    | 8373    | 369298    |       nan    |        nan    |       nan    |

## Fon hisseleri: gosterge medyanlari

| gosterge   |   ONCE |   ERKEN |   KOSU |   DIGER |
|:-----------|-------:|--------:|-------:|--------:|
| rsi        | 46.11  |  54.713 | 61.133 |  49.136 |
| mfi        | 54.177 |  61.486 | 64.461 |  55.27  |
| cmf        | -0.059 |  -0.056 |  0.073 |  -0.111 |
| obv20      |  0.039 |   0.142 |  0.247 |   0.066 |
| ad20       | -0.059 |  -0.055 |  0.073 |  -0.111 |
| adx        | 23.555 |  24.476 | 31.983 |  22.523 |
| bb_gen     |  0.97  |   0.842 |  1.108 |   0.937 |
| fib_konum  |  0.56  |   0.444 |  0.854 |   0.453 |
| atr_yzd    |  0.054 |   0.048 |  0.053 |   0.043 |
| macd_hist  | -0     |   0.003 |  0.002 |   0     |
| vk         |  0.955 |   0.994 |  0.952 |   0.969 |
| roc20      | -0.03  |   0.05  |  0.126 |  -0.001 |
| ulcer      |  8.549 |   5.396 |  5.463 |   6.65  |
| force      |  0.001 |   0.006 |  0.008 |   0.002 |

## Evren testi: gostergeler (4 dilim BIST/ABD x 2016-21/2022-26; kat = sinyal orani / her 5. gun tabani)

| sinyal                 | yon    |   dilim |   n_min |   gecti_k20 |   kat_k20_min |   kat_k20_ort |   gecti_x2 |   kat_x2_min |   gecti_dus |   kat_dus_min |   kat_dus_ort |   kat_dus_esli_min |   kat_dus_esli_ort |   kat_k20_esli_min |   kat_k20_esli_ort | esli_taban        | iz    |
|:-----------------------|:-------|--------:|--------:|------------:|--------------:|--------------:|-----------:|-------------:|------------:|--------------:|--------------:|-------------------:|-------------------:|-------------------:|-------------------:|:------------------|:------|
| blok_taban             | asagi  |       4 |      80 |           0 |          0.32 |          1.05 |          0 |         0.49 |           4 |          1.64 |          2.08 |               0.91 |               1.23 |               0.37 |               0.9  | _es_taban_bloksuz | False |
| force_guclu            | yukari |       4 |   17457 |           0 |          1.04 |          1.14 |          2 |         1.03 |           0 |          1.04 |          1.16 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| cmf_negatif            | asagi  |       4 |   18949 |           0 |          0.95 |          1.03 |          0 |         0.95 |           0 |          1.02 |          1.05 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| obv_lider              | yukari |       4 |    5328 |           0 |          1    |          1.11 |          1 |         1.03 |           0 |          1.03 |          1.14 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| tenkan_kijun_kesme     | yukari |       4 |   11928 |           0 |          1    |          1.01 |          0 |         0.99 |           0 |          0.94 |          0.98 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| rsi_50_kesme           | yukari |       4 |   14444 |           0 |          0.98 |          1    |          0 |         0.96 |           0 |          0.97 |          1    |             nan    |             nan    |             nan    |             nan    | nan               | False |
| macd_al_sifir_alti     | yukari |       4 |    9228 |           0 |          0.97 |          1.02 |          0 |         0.94 |           0 |          0.94 |          1.01 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| macd_sifir_kesme       | yukari |       4 |    7831 |           0 |          0.97 |          1.01 |          0 |         0.95 |           0 |          0.87 |          0.95 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| rsi_70_ustu            | asagi  |       4 |    8033 |           0 |          0.86 |          1.02 |          0 |         0.93 |           0 |          0.96 |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| mfi_80_ustu            | asagi  |       4 |    9011 |           0 |          0.93 |          1.02 |          0 |         1.08 |           0 |          0.96 |          1.03 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| bb_alt_kirilim         | asagi  |       4 |    8910 |           0 |          0.86 |          0.98 |          0 |         0.89 |           0 |          0.96 |          1.03 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| bb_sikisma             | yukari |       4 |   10666 |           0 |          0.95 |          0.97 |          0 |         0.82 |           0 |          0.86 |          0.93 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| stoch_20_donus         | yukari |       4 |   15953 |           0 |          0.95 |          1.01 |          0 |         0.96 |           0 |          1.01 |          1.02 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_obv_boga            | yukari |       4 |    4815 |           0 |          0.94 |          0.98 |          0 |         0.86 |           0 |          0.99 |          1.04 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_macd_gizli_boga     | yukari |       4 |    5232 |           0 |          0.94 |          0.99 |          0 |         0.95 |           0 |          0.9  |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| bulut_ustu_kesme       | yukari |       4 |    7939 |           0 |          0.94 |          0.99 |          0 |         0.91 |           0 |          0.9  |          0.96 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_cmf_gizli_boga      | yukari |       4 |    5407 |           0 |          0.94 |          0.98 |          0 |         0.93 |           0 |          0.9  |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_mfi_gizli_boga      | yukari |       4 |    5032 |           0 |          0.93 |          0.97 |          0 |         0.92 |           0 |          0.89 |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| fib_382_bolge          | yukari |       4 |    6177 |           0 |          0.93 |          0.96 |          0 |         0.83 |           0 |          0.91 |          1.08 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_obv_gizli_boga      | yukari |       4 |    2509 |           0 |          0.93 |          0.98 |          0 |         0.91 |           0 |          0.92 |          0.95 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| altin_kesisim          | yukari |       4 |    1855 |           0 |          0.93 |          1    |          0 |         1.05 |           0 |          0.91 |          0.92 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| fib_dip_bolge          | yukari |       4 |    5758 |           0 |          0.92 |          1.1  |          1 |         0.97 |           0 |          0.75 |          1.14 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| fib_618_bolge          | yukari |       4 |    4448 |           0 |          0.92 |          0.99 |          0 |         0.89 |           0 |          0.94 |          1.12 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| squeeze_yukari_cozulme | yukari |       4 |    5581 |           0 |          0.92 |          0.99 |          0 |         0.99 |           0 |          0.85 |          0.96 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| cci_100_ustu           | yukari |       4 |   12493 |           0 |          0.92 |          1.02 |          0 |         0.96 |           0 |          0.91 |          0.95 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| bb_ust_kirilim         | yukari |       4 |   12311 |           0 |          0.91 |          1.02 |          0 |         0.95 |           0 |          0.93 |          0.97 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_rsi_gizli_boga      | yukari |       4 |    3888 |           0 |          0.91 |          0.96 |          0 |         0.84 |           0 |          0.89 |          1.03 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| aroon_yukari           | yukari |       4 |   13147 |           0 |          0.91 |          1    |          0 |         0.91 |           0 |          0.89 |          0.94 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| wr_80_alti             | yukari |       4 |   17314 |           0 |          0.9  |          0.99 |          0 |         0.95 |           0 |          1.03 |          1.04 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| mfi_20_alti            | yukari |       4 |    4533 |           0 |          0.9  |          1.05 |          0 |         0.95 |           0 |          0.93 |          1.11 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| cmf_pozitif            | yukari |       4 |   11354 |           0 |          0.9  |          0.99 |          0 |         0.91 |           0 |          0.95 |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_cmf_boga            | yukari |       4 |    4407 |           0 |          0.9  |          1.01 |          0 |         0.85 |           0 |          0.91 |          1    |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_mfi_boga            | yukari |       4 |    3935 |           0 |          0.9  |          1.02 |          0 |         0.85 |           0 |          0.93 |          1.02 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| adx_25_trend           | yukari |       4 |    5385 |           0 |          0.9  |          1.01 |          0 |         0.97 |           0 |          0.81 |          0.94 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_cmf_ayi             | asagi  |       4 |    5285 |           0 |          0.95 |          0.98 |          0 |         0.9  |           0 |          0.89 |          0.97 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_rsi_ayi             | asagi  |       4 |    3622 |           0 |          0.92 |          0.97 |          0 |         0.77 |           0 |          0.89 |          1.01 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_rsi_boga            | yukari |       4 |    2710 |           0 |          0.88 |          1.03 |          0 |         0.81 |           0 |          0.89 |          0.98 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_macd_boga           | yukari |       4 |    3890 |           0 |          0.88 |          0.99 |          0 |         0.82 |           0 |          0.97 |          1.02 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| cci_100_alti           | yukari |       4 |   10067 |           0 |          0.87 |          0.97 |          0 |         0.89 |           0 |          0.97 |          1.04 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_macd_ayi            | asagi  |       4 |    4495 |           0 |          0.94 |          0.99 |          0 |         0.92 |           0 |          0.87 |          0.95 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| uy_mfi_ayi             | asagi  |       4 |    4583 |           0 |          0.92 |          0.98 |          0 |         0.84 |           0 |          0.86 |          0.99 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| blok_tavan             | yukari |       4 |      81 |           2 |          0.86 |          1.21 |          2 |         0.65 |           0 |          1.41 |          1.75 |               1.03 |               1.2  |               0.72 |               0.94 | _es_tavan_bloksuz | False |
| uy_obv_ayi             | asagi  |       4 |    1915 |           0 |          0.95 |          0.97 |          0 |         0.84 |           0 |          0.86 |          0.95 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| rsi_30_alti            | yukari |       4 |    4577 |           0 |          0.85 |          1.05 |          0 |         0.88 |           0 |          0.77 |          1.06 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| ulcer_sakin_trend      | yukari |       4 |    8892 |           0 |          0.81 |          0.98 |          0 |         0.64 |           0 |          0.8  |          0.82 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| blok_hacim             | yukari |       4 |     284 |           0 |          0.76 |          1.02 |          2 |         0.84 |           0 |          1.07 |          1.38 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| ad_birikim_yatay       | yukari |       4 |    1219 |           0 |          0.74 |          0.87 |          0 |         0.76 |           0 |          0.76 |          0.87 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| fib_tepe_bolge         | asagi  |       4 |    5482 |           0 |          0.74 |          0.98 |          0 |         0.59 |           0 |          0.7  |          0.92 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| kilit_tavan            | yukari |       4 |      39 |           2 |          0.3  |          1.06 |          2 |         0.65 |           0 |          1.04 |          1.94 |             nan    |             nan    |             nan    |             nan    | nan               | False |
| blok_seri_ici          | yukari |       4 |       1 |           0 |          0    |          1.59 |          0 |         0    |           0 |          0    |          2.05 |               0    |               1.28 |               0    |               1.29 | _es_tavan_bloksuz | False |

## Evren testi: KAP olaylari (yalniz BIST, 2 dilim; 2017 oncesi KAP verisi yok)

| sinyal             | yon    |   dilim |   n_min |   gecti_k20 |   kat_k20_min |   kat_k20_ort |   gecti_x2 |   kat_x2_min |   gecti_dus |   kat_dus_min |   kat_dus_ort |   kat_dus_esli_min |   kat_dus_esli_ort |   kat_k20_esli_min |   kat_k20_esli_ort | esli_taban    | iz    |
|:-------------------|:-------|--------:|--------:|------------:|--------------:|--------------:|-----------:|-------------:|------------:|--------------:|--------------:|-------------------:|-------------------:|-------------------:|-------------------:|:--------------|:------|
| kap_olagan_disi    | asagi  |       2 |    1082 |           0 |          0.96 |          0.97 |          0 |         0.92 |           2 |          1.52 |          1.57 |               1.14 |               1.14 |               0.75 |               0.81 | _es_sicrama20 | False |
| kap_vbts_tedbir    | asagi  |       2 |    2437 |           0 |          0.93 |          0.95 |          0 |         0.97 |           2 |          1.36 |          1.37 |               1.02 |               1.08 |               0.84 |               0.84 | _es_tavan     | False |
| kap_devre_kesici   | asagi  |       2 |    8004 |           0 |          0.94 |          0.99 |          0 |         0.96 |           1 |          1.15 |          1.26 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_tipe_donusum   | asagi  |       2 |    2495 |           0 |          0.92 |          0.94 |          0 |         0.93 |           0 |          1.14 |          1.21 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_spk_yasak      | asagi  |       2 |    1101 |           0 |          1.02 |          1.05 |          0 |         1.03 |           1 |          1.02 |          1.22 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_pay_alim_satim | yukari |       2 |    2408 |           0 |          0.99 |          1.02 |          0 |         1    |           0 |          1.12 |          1.13 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_soylenti       | yukari |       2 |     276 |           0 |          0.97 |          0.99 |          0 |         0.8  |           0 |          1.12 |          1.12 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_piyasa_yapici  | yukari |       2 |     103 |           0 |          0.93 |          1.03 |          1 |         0.77 |           0 |          0.5  |          0.69 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_fiili_dolasim  | yukari |       2 |     528 |           0 |          0.88 |          0.99 |          0 |         0.92 |           0 |          1.35 |          1.46 |             nan    |             nan    |             nan    |             nan    | nan           | False |
| kap_toptan         | yukari |       2 |      72 |           0 |          0.81 |          0.89 |          0 |         0.95 |           0 |          1.26 |          1.31 |             nan    |             nan    |             nan    |             nan    | nan           | False |

## Vaka kosulari

| sembol   | dip        | x2         | tepe       |    kat |   bar |
|:---------|:-----------|:-----------|:-----------|-------:|------:|
| TEHOL    | 2024-10-04 | 2024-12-26 | 2026-08-19 |  64.78 |   469 |
| ANELE    | 2024-08-22 | 2025-08-22 | 2026-09-09 |  17.63 |   514 |
| TRHOL    | 2024-09-11 | 2025-02-28 | 2026-09-14 | 327.45 |   504 |
| OZATD    | 2024-10-23 | 2025-06-16 | 2026-08-31 |  69.27 |   464 |
| PEKGY    | 2024-10-14 | 2025-06-16 | 2026-05-12 |  22.92 |   397 |
| IEYHO    | 2024-06-11 | 2024-07-19 | 2026-09-14 |  48.93 |   565 |
| DSTKF    | 2025-02-06 | 2025-02-21 | 2026-07-07 |  75.9  |   352 |
| ISKPL    | 2023-12-26 | 2024-07-16 | 2026-05-05 |  23.84 |   590 |
| SELEC    | 2024-07-02 | 2025-06-23 | 2026-09-10 |   9.15 |   551 |
| BIGEN    | 2026-03-09 | 2026-04-30 | 2026-09-02 |  22.03 |   120 |
| KTLEV    | 2024-08-05 | 2025-04-29 | 2026-08-28 |  70.06 |   519 |
| GUNDG    | 2024-10-14 | 2025-08-19 | 2026-07-27 |  63.34 |   446 |
| PASEU    | 2024-04-04 | 2024-11-18 | 2026-08-28 |  21.14 |   597 |
| ODINE    | 2024-06-11 | 2024-07-24 | 2026-08-12 |  65.54 |   542 |
| HEDEF    | 2024-10-14 | 2025-02-17 | 2026-08-04 | 193.55 |   452 |
| TERA     | 2024-07-29 | 2024-09-05 | 2026-04-17 | 153.98 |   436 |
| IZFAS    | 2023-11-13 | 2024-01-04 | 2026-04-20 |  28.78 |   612 |
| LIDER    | 2023-12-13 | 2024-09-30 | 2026-04-20 |  16.55 |   590 |
| ALKLC    | 2024-06-12 | 2025-03-13 | 2026-09-14 |  25.4  |   564 |
| UFUK     | 2023-05-22 | 2023-09-07 | 2025-11-03 |  49.77 |   614 |
| PRZMA    | 2024-12-23 | 2025-06-12 | 2026-08-31 |  13.25 |   422 |
| BINBN    | 2024-10-16 | 2025-03-27 | 2025-06-10 |   3.09 |   161 |
| DURDO    | 2022-06-27 | 2022-10-21 | 2024-12-05 |   4    |   612 |
