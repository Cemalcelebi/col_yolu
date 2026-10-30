# K55 — VERİ KAPSAMI (K55-20261030-123258-7ce1627; kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); evren sürümü 0d00d2c97608)

## Evren ve seri kalitesi

- sembol: 50
- eksiksiz: 46
- tarihsel_eksik: 4
- bosluklu: 0
- kisa_seri: 0
- sifir_hacim_yuksek: 4
- sert_hareketli_bilgi: 15
- ozellik_yeterli: 50
- asiri_getirili: 12
- ohlc_hatali: 0
- yinelenen_tarihli: 0
- cik_eslesen: 50
- sektor_bilinen: 49
- seri_erken_biten: 12
- sinif: {1: 38, 2: 4, 3: 4, 4: 2, 5: 2}
- seri_sonu: {'k51': 40, 'd100': 4, 'd0': 4, 'kes': 2}
- kaynak: {'V_ABD': 28, 'K34_tiingo': 12, 'K34_yahoo': 10}
- ilk_gun_medyan: 2020-10-01
- son_gun_max: 2026-08-31
- dislama_kategorileri: {'kisa_seri_yukleyici': 60, 'fon_evren_disi': 7, 'eslesme_yok_cik': 1}
- kisa_seri_yukleyici_disi: 60
- kesim_4b: [{'sembol': 'ARIS', 'once': 2830, 'sonra': 2649, 'atilan': 181}, {'sembol': 'UNIT', 'once': 2830, 'sonra': 2642, 'atilan': 188}, {'sembol': 'AXP', 'once': 1485, 'sonra': 354, 'atilan': 1131}, {'sembol': 'BG', 'once': 1485, 'sonra': 854, 'atilan': 631}, {'sembol': 'KNDI', 'once': 1485, 'sonra': 950, 'atilan': 535}, {'sembol': 'ZYME', 'once': 1485, 'sonra': 548, 'atilan': 937}, {'sembol': 'NE', 'once': 1313, 'sonra': 379, 'atilan': 934}, {'sembol': 'LOGC', 'once': 1421, 'sonra': 1185, 'atilan': 236}, {'sembol': 'HCIC', 'once': 561, 'sonra': 454, 'atilan': 107}]
- v_ev_tutarlilik: {'ev_serisiz': [], 'v_fazla': [], 'bos_seri': [], 'kesim_sonrasi_satir': [], 'gecti': True}
- orneklem_eksik_tabaka: [{'tabaka': 'V_ABD sınıf 1 lik 0', 'kota': 10, 'aday': 7, 'secilen': 7, 'eksik': 3}]

## Panel

- sure_sn: 1.5
- sembol: 50
- satir: 67098
- likit_satir: 45948
- r60_tanimli_likit: 44150
- donem_t0: {'BAGIMSIZ': 16708, 'KESIF': 16304, 'IC_DOGRULAMA': 11170, 'DISI': 1766}
- donem60_purge_embargo: {'KESIF': 15342, 'BAGIMSIZ': 14691, 'IC_DOGRULAMA': 9547, 'PURGE': 4042, 'DISI': 1766, 'EMBARGO': 395, 'TANIMSIZ': 165}
- donem250_purge_embargo: {'KESIF': 12849, 'PURGE': 10938, 'BAGIMSIZ': 9212, 'TANIMSIZ': 5919, 'IC_DOGRULAMA': 4869, 'DISI': 1766, 'EMBARGO': 395}
- ozelliksiz_satir_toplam: 13000
- atlanan: 0

## Olaylar (kilitli tanımlar: Y60 +%30, Y120 +%50, Y250 +%100; örtüşmez; tam pencere)

| ufuk | olay | hisse | tanimli_likit_gun | taban_orani | getiri_medyan | en_yuksek_medyan |
|---|---|---|---|---|---|---|
| Y120 | 97 | 28 | 42174 | +0.002 | +0.539 | +0.585 |
| Y250 | 39 | 23 | 38244 | +0.001 | +1.057 | +1.127 |
| Y60 | 216 | 36 | 44008 | +0.005 | +0.334 | +0.358 |

Yıl başına olay sayısı:

| yil | Y120 | Y250 | Y60 |
|---|---|---|---|
| 2016 | 5 | 2 | 5 |
| 2017 | 2 | 1 | 7 |
| 2018 | 7 | 3 | 6 |
| 2019 | 3 | 3 | 11 |
| 2020 | 18 | 7 | 33 |
| 2021 | 1 | 0 | 7 |
| 2022 | 12 | 4 | 25 |
| 2023 | 12 | 7 | 36 |
| 2024 | 12 | 4 | 32 |
| 2025 | 22 | 8 | 32 |
| 2026 | 3 | 0 | 22 |

## Sembol başına kalite (ilk 60 satır; tamamı K55_VERI_KALITESI.csv)

| sembol | kaynak | sinif | n_gun | ilk | son | bosluk_sayi | bosluk_max_gun | sifir_hacim_pay | asiri_getiri_sayi | sert_hareket_sayi | ohlc_hata | cik_var | eksiksiz | ozellik_yeterli | tarihsel_eksik |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AEHL | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.336 | 6 | 1 | 0 | True | False | True | True |
| AGGRU | K34_tiingo | 5 | 505 | 2021-03-10 00:00:00 | 2023-03-10 00:00:00 | 0 | 0 | +0.283 | 0 | 0 | 0 | True | False | True | True |
| ALVO | V_ABD | 1 | 1055 | 2022-06-16 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| AMRSQ | K34_tiingo | 2 | 905 | 2020-10-01 00:00:00 | 2024-05-07 00:00:00 | 0 | 0 | +0.000 | 13 | 10 | 0 | True | True | True | False |
| ASPI | V_ABD | 1 | 953 | 2022-11-10 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| BRBS | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.282 | 0 | 0 | 0 | True | False | True | True |
| CCI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| CHRS | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| CTRI | V_ABD | 1 | 593 | 2024-04-19 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| CYTH | K34_tiingo | 3 | 1126 | 2020-10-01 00:00:00 | 2025-03-26 00:00:00 | 0 | 0 | +0.001 | 0 | 1 | 0 | True | True | True | False |
| EAR | K34_tiingo | 3 | 844 | 2020-10-16 00:00:00 | 2024-02-26 00:00:00 | 0 | 0 | +0.007 | 1 | 1 | 0 | True | True | True | False |
| EPM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| EXTR | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| FDUS | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| FND | V_ABD | 1 | 2349 | 2017-04-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| FSRDQ | K34_tiingo | 2 | 483 | 2021-04-06 00:00:00 | 2023-03-06 00:00:00 | 0 | 0 | +0.006 | 2 | 2 | 0 | True | True | True | False |
| GDC | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.002 | 3 | 3 | 0 | True | True | True | False |
| GFR | V_ABD | 1 | 1183 | 2021-12-13 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.089 | 0 | 0 | 0 | True | True | True | False |
| GORO | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.222 | 3 | 20 | 0 | True | False | True | True |
| HARP | K34_tiingo | 3 | 865 | 2020-10-01 00:00:00 | 2024-03-11 00:00:00 | 0 | 0 | +0.001 | 1 | 0 | 0 | True | True | True | False |
| IMBIQ | K34_tiingo | 2 | 878 | 2020-10-01 00:00:00 | 2024-04-01 00:00:00 | 0 | 0 | +0.021 | 6 | 15 | 0 | True | True | True | False |
| INN | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| JANX | V_ABD | 1 | 1311 | 2021-06-11 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 1 | 0 | True | True | True | False |
| KIM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| LOGC | K34_tiingo | 4 | 1185 | 2020-12-16 00:00:00 | 2025-09-05 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| MCHP | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| MNDY | V_ABD | 1 | 1312 | 2021-06-10 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| MSGE | K34_yahoo | 1 | 847 | 2023-04-17 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| MTRN | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| NNBR | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| NWTG | K34_yahoo | 1 | 764 | 2023-08-15 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 4 | 0 | True | True | True | False |
| OABI | V_ABD | 1 | 1234 | 2021-09-30 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.071 | 0 | 1 | 0 | True | True | True | False |
| ONB | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| PBI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| PDYN | V_ABD | 1 | 1237 | 2021-09-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 1 | 0 | 0 | True | True | True | False |
| PLCE | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| RBBN | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| RMO | K34_tiingo | 3 | 514 | 2020-10-01 00:00:00 | 2022-10-14 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| RNW | V_ABD | 1 | 1402 | 2021-02-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ROKU | V_ABD | 1 | 2242 | 2017-09-28 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| SEPN | K34_yahoo | 1 | 462 | 2024-10-25 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| SUNLQ | K34_tiingo | 2 | 735 | 2021-01-15 00:00:00 | 2023-12-15 00:00:00 | 0 | 0 | +0.001 | 2 | 3 | 0 | True | True | True | False |
| SVFB | K34_tiingo | 5 | 505 | 2021-03-09 00:00:00 | 2023-03-09 00:00:00 | 0 | 0 | +0.014 | 0 | 0 | 0 | True | True | True | False |
| TBCH | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| TNON | V_ABD | 1 | 1090 | 2022-04-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 3 | 3 | 0 | True | True | True | False |
| VIR | V_ABD | 1 | 1730 | 2019-10-11 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 1 | 0 | True | True | True | False |
| WDAY | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| WING | V_ABD | 1 | 2821 | 2015-06-12 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| WRBY | V_ABD | 1 | 1235 | 2021-09-29 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
| ZYME | K34_tiingo | 4 | 548 | 2020-10-01 00:00:00 | 2022-12-02 00:00:00 | 0 | 0 | +0.000 | 0 | 0 | 0 | True | True | True | False |
