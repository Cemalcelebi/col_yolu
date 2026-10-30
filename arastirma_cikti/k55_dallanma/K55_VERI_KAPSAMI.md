# K55 — VERİ KAPSAMI (K55-20261030-130849-e726670; kod K55 v0.2 (2026-10-30, Faz 0 + ön kayıt v1.2: purge = ufuk, embargo, güçlü koşu kimliği, çıktı yolu denetimi, blok bootstrap, FDR ailesi); evren sürümü 0d00d2c97608)

## Evren toplamı ve kapsam (EV'deki BÜTÜN semboller; fiyatı olmayanlar dahil)

- sembol_ev: 50
- fiyat_var: 50
- fiyat_yok: 0
- bos_seri: 0
- kisa_seri_320: 0
- kesilmis_k54: 2
- v_fazla: 0
- v_fazla_liste: []
- ev_yinelenen: 0
- kaynak: {'V_ABD': 28, 'K34_tiingo': 12, 'K34_yahoo': 10}
- sinif: {1: 38, 2: 4, 3: 4, 4: 2, 5: 2}
- sinif_4a: 0
- sinif_4b: 2
- fiyat_turu: bölünme + temettü düzeltmeli (V_ABD / K34 Yahoo auto_adjust; Tiingo adj); ham Close yok

## Şirket eşleştirmesi

- cik_eslesen: 50
- cik_bos: 0
- cik_gecersiz: 0
- cik_coklu_sembol: 0
- sembol_yeniden_kullanim: 2
- sec_ad_bos: 0
- sektor_bilinen: 45
- sektor_bos: 5
- seri_erken: 12
- seri_erken_gecersiz: 0

## Tarih ve takvim (ABD işlem takvimi; tatiller eksik gün değil)

- takvim: NYSE kuralları (pandas holiday; Juneteenth 2022+, özel kapanışlar 2018-12-05, 2025-01-09)
- saat_dilimli: 0
- sirasiz: 0
- yinelenen_islem_gunlu: 0
- takvim_disi_satirli: 0
- eksik_islem_gunu_toplam: 1
- bosluklu: 1
- ciddi_bosluklu: 0
- en_uzun_bosluk_max: 1

## OHLCV sorunları (veri hatası; sembol sayısı)

- sutun_eksik: 0
- tur_hatali: 0
- nan_fiyatli: 0
- inf_fiyatli: 0
- sifir_negatif_fiyatli: 0
- negatif_hacimli: 0
- eksik_hacimli: 0
- eksik_hacim_pay_yuksek: 0
- sifir_hacim_pay_yuksek: 4
- ohlc_high_dusuk: 0
- ohlc_low_yuksek: 0
- ohlc_high_low: 0

## Getiri ve bölünme benzeri hareket (kesin / muhtemel / açıklanamayan / sert haber; kurumsal veri yoksa kesin denmez)

- getiri_100_ustu: 12
- kesin_bolunme: 0
- muhtemel_bolunme: 8
- aciklanamayan_sicrama: 7
- sert_haber_hareketi: 18
- kurumsal_veri_var: False

## Özellik ve sonuç pencereleri, dönem kapsamı

- ozellik_yeterli: 50
- sonuc_Y60_yeterli: 50
- sonuc_Y120_yeterli: 50
- sonuc_Y250_yeterli: 46
- olay_pencere_eksik: 0
- donem_kapsami: {'KESIF': 43, 'IC_DOGRULAMA': 48, 'BAGIMSIZ': 44}

## Sınıf özetleri (sembol sayısı)

- veri_hatali: 0
- veri_yetersiz: 4
- piyasa_davranisli: 18
- supheli_sicramali: 11
- kullanilabilir: 46

## Panel

- sure_sn: 1.6
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

## Sembol başına kalite (ilk 60 satır; tamamı K55_VERI_KALITESI.csv; her sorun ayrı sütun)

| sembol | kaynak | sinif | n_gun | ilk | son | fiyat_yok | kisa_seri_320 | eksik_islem_gunu | ciddi_bosluk_sayi | yinelenen_islem_gunu | takvim_disi_satir | sifir_hacim_pay | eksik_hacim_pay | ohlc_high_low | getiri_100_ustu_sayi | muhtemel_bolunme | aciklanamayan_sicrama | sert_haber_hareketi | cik_bos | sektor_bos | veri_hatasi | veri_yetersiz | kullanilabilir |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AEHL | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.336 | +0.000 | 0 | 6 | 0 | 1 | 10 | 0 | 0 |  | sifir_hacim_pay_yuksek | False |
| AGGRU | K34_tiingo | 5 | 505 | 2021-03-10 00:00:00 | 2023-03-10 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.283 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | sifir_hacim_pay_yuksek | False |
| ALVO | V_ABD | 1 | 1055 | 2022-06-16 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| AMRSQ | K34_tiingo | 2 | 905 | 2020-10-01 00:00:00 | 2024-05-07 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 13 | 7 | 21 | 12 | 0 | 0 |  |  | True |
| ASPI | V_ABD | 1 | 953 | 2022-11-10 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| BRBS | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.282 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | sifir_hacim_pay_yuksek | False |
| CCI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| CHRS | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| CTRI | V_ABD | 1 | 593 | 2024-04-19 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| CYTH | K34_tiingo | 3 | 1126 | 2020-10-01 00:00:00 | 2025-03-26 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.001 | +0.000 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |  |  | True |
| EAR | K34_tiingo | 3 | 844 | 2020-10-16 00:00:00 | 2024-02-26 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.007 | +0.000 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |  |  | True |
| EPM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| EXTR | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| FDUS | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  | True |
| FND | V_ABD | 1 | 2349 | 2017-04-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| FSRDQ | K34_tiingo | 2 | 483 | 2021-04-06 00:00:00 | 2023-03-06 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.006 | +0.000 | 0 | 2 | 0 | 0 | 4 | 0 | 0 |  |  | True |
| GDC | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.002 | +0.000 | 0 | 3 | 2 | 0 | 6 | 0 | 0 |  |  | True |
| GFR | V_ABD | 1 | 1183 | 2021-12-13 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.089 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| GORO | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.222 | +0.000 | 0 | 3 | 30 | 23 | 12 | 0 | 0 |  | sifir_hacim_pay_yuksek | False |
| HARP | K34_tiingo | 3 | 865 | 2020-10-01 00:00:00 | 2024-03-11 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.001 | +0.000 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |  |  | True |
| IMBIQ | K34_tiingo | 2 | 878 | 2020-10-01 00:00:00 | 2024-04-01 00:00:00 | 0 | 0 | 1 | 0 | 0 | 0 | +0.021 | +0.000 | 0 | 6 | 10 | 12 | 20 | 0 | 0 |  |  | True |
| INN | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| JANX | V_ABD | 1 | 1311 | 2021-06-11 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 1 | 0 | 0 | 2 | 0 | 0 |  |  | True |
| KIM | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| LOGC | K34_tiingo | 4 | 1185 | 2020-12-16 00:00:00 | 2025-09-05 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| MCHP | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| MNDY | V_ABD | 1 | 1312 | 2021-06-10 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| MSGE | K34_yahoo | 1 | 847 | 2023-04-17 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| MTRN | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| NNBR | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |  |  | True |
| NWTG | K34_yahoo | 1 | 764 | 2023-08-15 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 1 | 1 | 4 | 0 | 0 |  |  | True |
| OABI | V_ABD | 1 | 1234 | 2021-09-30 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.071 | +0.000 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |  |  | True |
| ONB | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| PBI | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |  |  | True |
| PDYN | V_ABD | 1 | 1237 | 2021-09-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |  |  | True |
| PLCE | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |  |  | True |
| RBBN | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| RMO | K34_tiingo | 3 | 514 | 2020-10-01 00:00:00 | 2022-10-14 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| RNW | V_ABD | 1 | 1402 | 2021-02-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| ROKU | V_ABD | 1 | 2242 | 2017-09-28 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| SEPN | K34_yahoo | 1 | 462 | 2024-10-25 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |  |  | True |
| SUNLQ | K34_tiingo | 2 | 735 | 2021-01-15 00:00:00 | 2023-12-15 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.001 | +0.000 | 0 | 2 | 0 | 4 | 5 | 0 | 0 |  |  | True |
| SVFB | K34_tiingo | 5 | 505 | 2021-03-09 00:00:00 | 2023-03-09 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.014 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| TBCH | K34_yahoo | 1 | 1485 | 2020-10-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
| TNON | V_ABD | 1 | 1090 | 2022-04-27 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 3 | 1 | 0 | 5 | 0 | 0 |  |  | True |
| VIR | V_ABD | 1 | 1730 | 2019-10-11 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |  |  | True |
| WDAY | V_ABD | 1 | 2830 | 2015-06-01 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  | True |
| WING | V_ABD | 1 | 2821 | 2015-06-12 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  | True |
| WRBY | V_ABD | 1 | 1235 | 2021-09-29 00:00:00 | 2026-08-31 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |  |  | True |
| ZYME | K34_tiingo | 4 | 548 | 2020-10-01 00:00:00 | 2022-12-02 00:00:00 | 0 | 0 | 0 | 0 | 0 | 0 | +0.000 | +0.000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  | True |
