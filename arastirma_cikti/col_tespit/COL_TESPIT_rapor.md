# COL TESPIT — Cemal'in uc kurali ile tespit motoru adaylari   (COL_TESPIT v1.0 (2026-10-21, D13 adayi: dip -> savunma -> yuvarlanma -> kucuk mum obekleri), 2026-10-21 17:11)

Kutu = [yeni dip d, bugun e] (d = son N barin en dusuk Low'u; dipten onceki raf/dusus kutuya girmez). Varyant = esikler; her dip bir kez sinyal.
GOZ: Cemal'in 29 colu (yakalanan) ve 29 'degil' kutusu (yanlis alarm); ARZUM 3 obek + 1 dusen bicak ayri. D12 uretim: 16/29 yakaliyor, 8/29 yanlis alarm.
EVREN: sinyalden sonra 60 barda alim (a: dip -%2 kirilirsa islem yok; b: kirilip toparlansa da sayilir), bozulma, 60/120 bar ileri getiri (%200 kirpili), once +10, alim sonrasi uretim cikisi getirisi. TABAN = her 5. gunun 15 mumluk kutusu. f_ = varyant - taban.
Skor = COL yakalama orani - yanlis alarm orani + 0,1 x (alim tabandan >10 puan iyi donem) + 0,1 x (ileri60 tabandan iyi donem) + 0,05 x (getiri tabandan iyi donem).

## Taban (donem)

| donem | n | alim a | alim b | bozulma | ileri60 | ileri120 | once +10 | getiri a |
|---|---|---|---|---|---|---|---|---|
| 2016-19 | 42097 | %56 | %66 | %38 | +8.46 | +16.27 | %56 | +7.21 |
| 2020-22 | 58593 | %64 | %75 | %31 | +20.13 | +38.69 | %63 | +12.27 |
| 2023 | 22852 | %56 | %73 | %41 | +23.56 | +49.75 | %57 | +13.17 |
| 2024-26 | 74612 | %52 | %64 | %44 | +5.46 | +10.83 | %57 | +2.80 |
| ABD 2022-23 | 79291 | %59 | %71 | %39 | +4.88 | +8.35 | %47 | +1.03 |
| ABD 2024-26 | 194679 | %58 | %69 | %38 | +5.51 | +10.93 | %49 | +1.02 |

## En iyi 15 varyant (skor)

| sira | varyant | COL yak. | DEGIL yanlis | ARZUM obek/bicak | donem | sinyal | alim>taban+10 | i60>taban | getiri>taban | f_alim | f_i60 | f_i120 | f_getiri | bozulma | toparlanan | skor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | N120 konum<=1.01 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 10945 | 6 | 6 | 5 | +19p | +5.16 | +4.45 | +2.84 | %13 | %3 | 1.86 |
| 2 | N60 konum<=0.5 bar>=15 inis>=10% retest>=0 yuv=ucte_bir kucuk<=99 obek>=2 obek_yuk=hayir | 20/29 | 8/29 | 1/3 / 0/1 | 6 | 21169 | 6 | 6 | 5 | +17p | +3.16 | +3.13 | +1.83 | %16 | %3 | 1.86 |
| 3 | N120 konum<=1.01 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 10777 | 6 | 6 | 5 | +19p | +5.29 | +4.60 | +2.81 | %13 | %3 | 1.86 |
| 4 | N120 konum<=1.01 bar>=25 inis>=5% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 10918 | 6 | 6 | 5 | +19p | +5.20 | +4.48 | +2.82 | %13 | %3 | 1.86 |
| 5 | N60 konum<=0.5 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=2 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 10865 | 6 | 6 | 5 | +19p | +5.49 | +5.98 | +3.40 | %16 | %4 | 1.83 |
| 6 | N60 konum<=0.5 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=2 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 10361 | 6 | 6 | 5 | +19p | +5.41 | +6.01 | +3.28 | %16 | %4 | 1.83 |
| 7 | N60 konum<=0.5 bar>=25 inis>=5% retest>=0 yuv=sma10 kucuk<=99 obek>=2 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 10801 | 6 | 6 | 5 | +19p | +5.48 | +5.99 | +3.39 | %16 | %4 | 1.83 |
| 8 | N60 konum<=0.5 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 11770 | 6 | 6 | 5 | +19p | +5.56 | +6.39 | +3.46 | %16 | %4 | 1.83 |
| 9 | N120 konum<=0.35 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 14/29 | 3/29 | 0/3 / 0/1 | 6 | 6714 | 6 | 6 | 5 | +21p | +5.95 | +5.58 | +2.47 | %13 | %3 | 1.83 |
| 10 | N60 konum<=0.5 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 11254 | 6 | 6 | 5 | +19p | +5.51 | +6.39 | +3.32 | %16 | %4 | 1.83 |
| 11 | N120 konum<=0.35 bar>=25 inis>=5% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 14/29 | 3/29 | 0/3 / 0/1 | 6 | 6761 | 6 | 6 | 5 | +21p | +5.83 | +5.38 | +2.49 | %13 | %3 | 1.83 |
| 12 | N60 konum<=0.5 bar>=25 inis>=5% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 4/29 | 0/3 / 0/1 | 6 | 11707 | 6 | 6 | 5 | +19p | +5.55 | +6.39 | +3.45 | %16 | %4 | 1.83 |
| 13 | N120 konum<=1.01 bar>=15 inis>=5% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 1/3 / 0/1 | 6 | 22761 | 6 | 4 | 6 | +19p | +1.45 | -0.89 | +1.68 | %6 | %1 | 1.82 |
| 14 | N120 konum<=1.01 bar>=15 inis>=10% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 1/3 / 0/1 | 6 | 18694 | 6 | 4 | 6 | +21p | +2.67 | -0.13 | +1.82 | %7 | %1 | 1.82 |
| 15 | N120 konum<=0.5 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 8618 | 6 | 6 | 4 | +20p | +5.87 | +5.84 | +2.66 | %13 | %3 | 1.81 |

## Eksen etkileri (tum varyantlarin ortalamasi)

| eksen | deger | COL yak. ort | DEGIL yanlis ort | f_alim ort | f_i60 ort | f_getiri ort | sinyal ort |
|---|---|---|---|---|---|---|---|
| N | 60 | 10.6 | 5.9 | +16p | +2.77 | +1.45 | 11385 |
| N | 120 | 10.1 | 2.9 | +17p | +3.26 | +1.70 | 7802 |
| konum | 0.35 | 9.9 | 3.8 | +17p | +3.26 | +1.19 | 5923 |
| konum | 0.5 | 10.6 | 3.9 | +17p | +3.37 | +1.81 | 8563 |
| konum | 1.01 | 10.6 | 5.6 | +16p | +2.40 | +1.73 | 14296 |
| bar | 15 | 11.6 | 5.6 | +16p | +3.01 | +1.48 | 10532 |
| bar | 25 | 9.1 | 3.2 | +17p | +3.01 | +1.67 | 8656 |
| inis | 0.0 | 10.4 | 4.5 | +16p | +2.87 | +1.62 | 10676 |
| inis | 5.0 | 10.4 | 4.5 | +17p | +2.91 | +1.55 | 9785 |
| inis | 10.0 | 10.3 | 4.3 | +17p | +3.25 | +1.57 | 8320 |
| retest | 0 | 11.0 | 5.0 | +17p | +3.24 | +1.78 | 11590 |
| retest | 2 | 9.7 | 3.9 | +16p | +2.79 | +1.37 | 7598 |
| yuv | parabol | 8.3 | 3.0 | +23p | +3.35 | +1.43 | 6964 |
| yuv | sma10 | 10.2 | 4.5 | +19p | +3.99 | +1.83 | 5953 |
| yuv | ucte_bir | 11.3 | 4.2 | +16p | +2.75 | +1.55 | 11326 |
| yuv | yok | 11.6 | 6.0 | +8p | +1.95 | +1.50 | 14133 |
| kucuk | 0.9 | 7.4 | 3.5 | +16p | +2.88 | +1.32 | 5379 |
| kucuk | 1.0 | 10.0 | 3.8 | +17p | +3.19 | +1.76 | 8403 |
| kucuk | 99.0 | 13.7 | 6.0 | +16p | +2.97 | +1.64 | 14999 |
| obek | 1 | 10.6 | 5.1 | +16p | +3.14 | +1.57 | 10189 |
| obek | 2 | 10.1 | 3.7 | +17p | +2.88 | +1.58 | 8999 |
| obek_yuk | 0 | 11.5 | 4.7 | +14p | +2.92 | +1.57 | 11932 |
| obek_yuk | 1 | 9.2 | 4.1 | +19p | +3.10 | +1.58 | 7255 |

## 1. varyant donem tablosu: N120 konum<=1.01 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir

| donem | n | alim a | alim b | bozulma | toparlanan | ileri60 | ileri120 | once +10 | getiri a | getiri b | f_alim | f_i60 | f_getiri |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2016-19 | 1217 | %71 | %74 | %17 | %4 | +9.85 | +17.09 | %58 | +6.63 | +6.46 | +15p | +1.39 | -0.58 |
| 2020-22 | 1373 | %77 | %79 | %8 | %2 | +22.21 | +44.33 | %71 | +12.49 | +12.54 | +13p | +2.08 | +0.22 |
| 2023 | 397 | %83 | %89 | %10 | %6 | +47.78 | +71.11 | %63 | +28.34 | +28.69 | +27p | +24.21 | +15.16 |
| 2024-26 | 1655 | %74 | %76 | %16 | %2 | +7.53 | +10.84 | %63 | +3.85 | +3.90 | +21p | +2.07 | +1.05 |
| ABD 2022-23 | 2124 | %80 | %83 | %12 | %3 | +5.68 | +6.86 | %53 | +1.06 | +1.02 | +21p | +0.80 | +0.03 |
| ABD 2024-26 | 4179 | %77 | %79 | %14 | %2 | +5.94 | +11.28 | %51 | +2.14 | +2.09 | +19p | +0.43 | +1.12 |

### 1. varyant goz testi (etiket basina)

| etiket | sinif | set | yakalandi |
|---|---|---|---|
| TEHOL_20241007 | COL | eski | EVET |
| TEHOL_20260203 | COL | eski | EVET |
| INVES_20250508 | COL | eski | hayir |
| BURVA_20250626 | COL | eski | EVET |
| EYGYO_20250528 | COL | eski | hayir |
| BASCM_20250302 | COL | eski | EVET |
| SEYKM_20250415 | COL | eski | hayir |
| GEDZA_20241015 | COL | eski | EVET |
| SUNTK_20240827 | COL | eski | EVET |
| HDFGS_20250422 | COL | eski | EVET |
| INFO_20250326 | COL | eski | EVET |
| KATMR_20250416 | COL | eski | EVET |
| OTTO_20240702 | COL | eski | hayir |
| TUKAS_20241002 | COL | eski | EVET |
| ORCAY_20241005 | COL | eski | EVET |
| TATGD_20240530 | COL | eski | hayir |
| TATGD_20240805 | COL | eski | hayir |
| EUREN_20251001 | COL | eski | hayir |
| VRGYO_20250814 | COL | eski | hayir |
| VESTL_20241105 | COL | eski | hayir |
| VESTL_20250602 | COL | eski | EVET |
| ARZUM_20240806 | COL | eski | hayir |
| EMNIS_20250414 | COL | eski | hayir |
| SKTAS_20240710 | COL | eski | hayir |
| SMRTG_20241121 | COL | eski | hayir |
| ODAS_20240606 | COL | eski | EVET |
| BINBN_20260225 | COL | eski | EVET |
| BINBN_20241217 | COL | eski | hayir |
| ESCAR_20250919 | COL | eski | EVET |
| PEKER_20250227 | COL | eski | veri yok |
| PAPIL_20251112 | DEGIL | eski | hayir |
| GEDIK_20250915 | DEGIL | eski | hayir |
| SEYKM_20260308 | DEGIL | eski | hayir |
| ALTNY_20251023 | DEGIL | eski | EVET |
| TUREX_20260330 | DEGIL | eski | hayir |
| SDTTR_20240328 | DEGIL | eski | hayir |
| GARFA_20260731 | DEGIL | eski | hayir |
| ERCB_20250613 | DEGIL | eski | EVET |
| CLEBI_20260825 | DEGIL | bugun | hayir |
| EKGYO_20260915 | DEGIL | bugun | hayir |
| MTRYO_20260730 | DEGIL | bugun | hayir |
| ENTRA_20260810 | DEGIL | bugun | hayir |
| GRSEL_20260904 | DEGIL | bugun | hayir |
| SEKFK_20260820 | DEGIL | bugun | hayir |
| OYLUM_20260817 | DEGIL | bugun | hayir |
| TABGD_20260901 | DEGIL | bugun | hayir |
| GLYHO_20260709 | DEGIL | bugun | hayir |
| NTGAZ_20260624 | DEGIL | bugun | hayir |
| HTTBT_20260825 | DEGIL | bugun | hayir |
| ZRGYO_20260812 | DEGIL | bugun | hayir |
| BIMAS_20260819 | DEGIL | bugun | hayir |
| LOGO_20260609 | DEGIL | bugun | hayir |
| YGGYO_20260819 | DEGIL | bugun | hayir |
| EUYO_20260825 | DEGIL | bugun | hayir |
| NUHCM_20260518 | DEGIL | bugun | EVET |
| DOCO_20260617 | DEGIL | bugun | hayir |
| VAKKO_20260708 | DEGIL | bugun | hayir |
| AVGYO_20260915 | DEGIL | bugun | hayir |
| ARZUM_20260922 | DEGIL | bugun | hayir |
| ARZUM_20251015 | DEGIL | arzum | hayir |
| ARZUM_20251117 | COL | arzum | hayir |
| ARZUM_20260102 | COL | arzum | hayir |
| ARZUM_20260420 | COL | arzum | hayir |

## Okuma

- Kural 1 (kutu dipten baslar) tum varyantlarda yapisal; kural 3 (kirilip toparlanan) 'alim b - alim a' ve 'toparlanan' sutunlarinda.
- Secim kriteri: COL yakalama >= 16/29 VE yanlis alarm <= 8/29 VE evrende alim ve ileri60 tabandan iyi 4/4 BIST donemi. Gecen yoksa 'araştırıldı, D12 kalır'.

