# K55 — VERİ KAPSAMI (K55-20261030-115506-8bed3ef; kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); evren sürümü 811989df4fda)

## Evren ve seri kalitesi

- sembol: 3260
- eksiksiz: 3012
- tarihsel_eksik: 242
- bosluklu: 86
- kisa_seri: 0
- sifir_hacim_yuksek: 179
- sert_hareketli_bilgi: 738
- ozellik_yeterli: 3260
- asiri_getirili: 704
- ohlc_hatali: 9
- yinelenen_tarihli: 0
- cik_eslesen: 3259
- sektor_bilinen: 3235
- seri_erken_biten: 266
- sinif: {1: 2994, 2: 19, 3: 159, 4: 9, 5: 79}
- seri_sonu: {'k51': 3082, 'd0': 159, 'd100': 19}
- kaynak: {'K34_yahoo': 1428, 'V_ABD': 1410, 'K34_tiingo': 422}
- ilk_gun_medyan: 2020-10-01
- son_gun_max: 2026-08-31
- kisa_seri_yukleyici_disi: 60

## Panel

- sure_sn: 69.2
- sembol: 3260
- satir: 4909423
- likit_satir: 3291650
- r60_tanimli_likit: 3168880
- donem_t0: {'KESIF': 1223817, 'BAGIMSIZ': 1146915, 'IC_DOGRULAMA': 800167, 'DISI': 120751}
- donem60_purge_embargo: {'KESIF': 1140437, 'BAGIMSIZ': 1005755, 'IC_DOGRULAMA': 683574, 'PURGE': 303056, 'DISI': 120751, 'EMBARGO': 29989, 'TANIMSIZ': 8088}
- donem250_purge_embargo: {'KESIF': 937262, 'PURGE': 811871, 'BAGIMSIZ': 621558, 'TANIMSIZ': 405934, 'IC_DOGRULAMA': 364285, 'DISI': 120751, 'EMBARGO': 29989}
- ozelliksiz_satir_toplam: 847600
- atlanan: 0

## Olaylar (kilitli tanımlar: Y60 +%30, Y120 +%50, Y250 +%100; örtüşmez; tam pencere)

| ufuk | olay | hisse | tanimli_likit_gun | taban_orani | getiri_medyan | en_yuksek_medyan |
|---|---|---|---|---|---|---|
| Y120 | 6201 | 1913 | 3035761 | +0.002 | +0.547 | +0.600 |
| Y250 | 2407 | 1379 | 2764634 | +0.001 | +1.072 | +1.162 |
| Y60 | 13894 | 2265 | 3162719 | +0.004 | +0.336 | +0.363 |

Yıl başına olay sayısı:

| yil | Y120 | Y250 | Y60 |
|---|---|---|---|
| 2016 | 183 | 78 | 356 |
| 2017 | 185 | 74 | 393 |
| 2018 | 193 | 78 | 518 |
| 2019 | 198 | 110 | 442 |
| 2020 | 1133 | 554 | 1959 |
| 2021 | 306 | 80 | 814 |
| 2022 | 653 | 249 | 1567 |
| 2023 | 802 | 397 | 1907 |
| 2024 | 844 | 347 | 1863 |
| 2025 | 1446 | 440 | 2752 |
| 2026 | 258 | 0 | 1323 |

## Sembol başına kalite (ilk 60 satır; tamamı K55_VERI_KALITESI.csv)

| sembol | kaynak | sinif | n_gun | ilk | son | bosluk_sayi | bosluk_max_gun | sifir_hacim_pay | asiri_getiri_sayi | sert_hareket_sayi | ohlc_hata | cik_var | eksiksiz | ozellik_yeterli | tarihsel_eksik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AAIC | K34_tiingo | 3 | 807 | 2020-10-01 00:00:00 | 2023-12-14 00:00:00 | 0 | 0 | +0.001 | 0 | 0 | 0 | True | True | True | False |
| AAL | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AAME | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.004 | 1 | 0 | 0 | True | True | True | False |
| AAMI | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AAOI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AAON | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AAP | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AAPL | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AARD | K34_yahoo | 1 | 388 | 2025-02-13 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| AAWH | K34_yahoo | 1 | 1322 | 2021-05-26 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABAT | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABBV | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABCL | V_ABD | 1 | 1435 | 2020-12-11 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABCP | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.310 | 1 | 0 | 0 | True | False | True | True |
| ABEO | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ABM | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABNB | V_ABD | 1 | 1436 | 2020-12-10 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABOS | K34_yahoo | 1 | 1297 | 2021-07-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 0 | 0 | True | True | True | False |
| ABR | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABSI | V_ABD | 1 | 1283 | 2021-07-22 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABT | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ABTC | V_ABD | 1 | 2140 | 2018-02-26 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.096 | 2 | 1 | 0 | True | True | True | False |
| ABUS | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 1 | 0 | True | True | True | False |
| ACAD | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ACAHU | K34_tiingo | 5 | 756 | 2021-03-04 00:00:00 | 2024-03-05 00:00:00 | 0 | 0 | +0.454 | 0 | 0 | 0 | True | False | True | True |
| ACCO | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACDC | V_ABD | 1 | 1078 | 2022-05-13 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACER | K34_tiingo | 3 | 790 | 2020-10-01 00:00:00 | 2023-11-20 00:00:00 | 0 | 0 | +0.000 | 1 | 1 | 0 | True | True | True | False |
| ACET | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ACGL | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACH | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ACHC | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACHR | V_ABD | 1 | 1430 | 2020-12-18 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACHV | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACI | V_ABD | 1 | 1552 | 2020-06-26 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACIC | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 2 | 0 | True | True | True | False |
| ACIW | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACMC | K34_tiingo | 5 | 557 | 2020-10-01 00:00:00 | 2022-12-15 00:00:00 | 0 | 0 | +0.424 | 0 | 1 | 0 | True | False | True | True |
| ACMR | V_ABD | 1 | 2217 | 2017-11-02 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACN | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACOG | K34_yahoo | 1 | 450 | 2024-11-12 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACORQ | K34_tiingo | 1 | 1124 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 1 | 374 | +0.130 | 1 | 1 | 0 | True | False | True | True |
| ACQR | K34_tiingo | 5 | 456 | 2021-05-19 00:00:00 | 2023-03-10 00:00:00 | 0 | 0 | +0.029 | 0 | 0 | 0 | True | True | True | False |
| ACRE | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACRS | V_ABD | 1 | 2741 | 2015-10-06 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 3 | 0 | True | True | True | False |
| ACRV | K34_yahoo | 1 | 950 | 2022-11-15 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ACTU | K34_yahoo | 1 | 514 | 2024-08-13 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACU | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ACVA | V_ABD | 1 | 1366 | 2021-03-24 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.001 | 0 | 0 | 0 | True | True | True | False |
| ACXP | K34_yahoo | 1 | 1301 | 2021-06-25 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 2 | 0 | 0 | True | True | True | False |
| ADAM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ADAPY | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 4 | 4 | 0 | True | True | True | False |
| ADBE | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ADC | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ADCT | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ADEA | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.001 | 0 | 0 | 0 | True | True | True | False |
| ADGM | K34_yahoo | 1 | 522 | 2024-08-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| ADI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ADIL | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 1 | 0 | True | True | True | False |
