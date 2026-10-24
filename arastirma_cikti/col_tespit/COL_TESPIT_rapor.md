# COL TESPIT — Cemal'in uc kurali ile tespit motoru adaylari   (COL_TESPIT v1.1 (2026-10-24, denetim: mesafe-esli taban, ABD pazar sutunu, trail ufuksuz), 2026-10-24 23:11)

Kutu = [yeni dip d, bugun e] (d = son N barin en dusuk Low'u; dipten onceki raf/dusus kutuya girmez). Varyant = esikler; her dip bir kez sinyal.
GOZ: Cemal'in 29 colu (yakalanan) ve 29 'degil' kutusu (yanlis alarm); ARZUM 3 obek + 1 dusen bicak ayri. D12 uretim: 16/29 yakaliyor, 8/29 yanlis alarm.
EVREN: sinyalden sonra 60 barda alim (a: dip -%2 kirilirsa islem yok; b: kirilip toparlansa da sayilir), bozulma, 60/120 bar ileri getiri (%200 kirpili), once +10, alim sonrasi uretim cikisi getirisi. TABAN = her 5. gunun 15 mumluk kutusu. f_ = varyant - taban.
Skor = COL yakalama orani - yanlis alarm orani + 0,1 x (alim tabandan >10 puan iyi donem) + 0,1 x (ileri60 tabandan iyi donem) + 0,05 x (getiri tabandan iyi donem).

## Taban (donem)

| donem | n | alim a | alim b | bozulma | ileri60 | ileri120 | once +10 | getiri a |
|---|---|---|---|---|---|---|---|---|
| 2016-19 | 68279 | %58 | %68 | %35 | +8.63 | +17.66 | %55 | +6.49 |
| 2020-22 | 58242 | %65 | %75 | %31 | +20.38 | +38.73 | %64 | +12.42 |
| 2023 | 22852 | %56 | %73 | %41 | +23.31 | +49.47 | %58 | +13.19 |
| 2024-26 | 75007 | %52 | %64 | %44 | +5.38 | +10.74 | %56 | +2.90 |
| ABD 2022-23 | 131002 | %55 | %68 | %42 | +2.16 | +4.69 | %46 | -0.35 |
| ABD 2024-26 | 195938 | %59 | %70 | %37 | +5.89 | +11.73 | %50 | +1.44 |

## En iyi 15 varyant (skor)

| sira | varyant | COL yak. | DEGIL yanlis | ARZUM obek/bicak | donem | sinyal | alim>taban+10 | i60>taban | getiri>taban | f_alim | f_i60 | f_i120 | f_getiri | bozulma | toparlanan | skor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | N120 konum<=0.35 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 14/29 | 3/29 | 0/3 / 0/1 | 6 | 7857 | 1 | 5 | 5 | +4p | +5.40 | +5.52 | +2.53 | %14 | %3 | 1.23 |
| 2 | N120 konum<=1.01 bar>=15 inis>=0% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 1/3 / 0/1 | 6 | 29552 | 0 | 4 | 6 | +0p | +0.46 | -1.57 | +1.59 | %6 | %1 | 1.22 |
| 3 | N60 konum<=0.5 bar>=15 inis>=10% retest>=0 yuv=ucte_bir kucuk<=99 obek>=2 obek_yuk=hayir | 20/29 | 8/29 | 1/3 / 0/1 | 6 | 24275 | 0 | 5 | 6 | +1p | +2.86 | +3.10 | +1.86 | %16 | %4 | 1.21 |
| 4 | N60 konum<=0.5 bar>=25 inis>=10% retest>=0 yuv=ucte_bir kucuk<=99 obek>=1 obek_yuk=hayir | 18/29 | 5/29 | 0/3 / 0/1 | 6 | 22293 | 0 | 5 | 5 | +2p | +3.20 | +2.83 | +1.93 | %15 | %3 | 1.20 |
| 5 | N60 konum<=0.5 bar>=25 inis>=10% retest>=0 yuv=ucte_bir kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 4/29 | 0/3 / 0/1 | 6 | 21302 | 0 | 5 | 5 | +2p | +3.09 | +2.35 | +1.92 | %15 | %3 | 1.20 |
| 6 | N120 konum<=1.01 bar>=15 inis>=5% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 1/3 / 0/1 | 6 | 25882 | 0 | 4 | 5 | +1p | +1.17 | -0.97 | +1.71 | %7 | %1 | 1.17 |
| 7 | N120 konum<=1.01 bar>=25 inis>=10% retest>=0 yuv=ucte_bir kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 0/3 / 0/1 | 6 | 30602 | 0 | 4 | 5 | -0p | +0.46 | -0.95 | +1.77 | %11 | %1 | 1.17 |
| 8 | N120 konum<=1.01 bar>=15 inis>=10% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 17/29 | 2/29 | 1/3 / 0/1 | 6 | 21196 | 0 | 4 | 5 | +2p | +2.48 | -0.04 | +1.90 | %7 | %1 | 1.17 |
| 9 | N120 konum<=1.01 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=2 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 12070 | 0 | 5 | 5 | +3p | +4.52 | +3.81 | +2.78 | %13 | %3 | 1.16 |
| 10 | N120 konum<=1.01 bar>=25 inis>=0% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 12866 | 0 | 5 | 5 | +3p | +4.69 | +4.39 | +2.85 | %13 | %3 | 1.16 |
| 11 | N60 konum<=0.5 bar>=15 inis>=5% retest>=0 yuv=ucte_bir kucuk<=99 obek>=2 obek_yuk=hayir | 20/29 | 8/29 | 1/3 / 0/1 | 6 | 29086 | 0 | 5 | 5 | +1p | +2.12 | +1.93 | +1.42 | %16 | %3 | 1.16 |
| 12 | N120 konum<=1.01 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 12655 | 0 | 5 | 5 | +3p | +4.82 | +4.56 | +2.85 | %13 | %3 | 1.16 |
| 13 | N120 konum<=1.01 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=2 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 11861 | 0 | 5 | 5 | +3p | +4.64 | +3.99 | +2.78 | %13 | %3 | 1.16 |
| 14 | N120 konum<=1.01 bar>=25 inis>=5% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir | 15/29 | 3/29 | 0/3 / 0/1 | 6 | 12832 | 0 | 5 | 5 | +3p | +4.71 | +4.42 | +2.84 | %13 | %3 | 1.16 |
| 15 | N60 konum<=0.5 bar>=15 inis>=10% retest>=0 yuv=parabol kucuk<=99 obek>=2 obek_yuk=hayir | 16/29 | 4/29 | 1/3 / 0/1 | 6 | 16158 | 0 | 5 | 5 | +1p | +3.78 | +3.12 | +2.17 | %10 | %2 | 1.16 |

## Eksen etkileri (tum varyantlarin ortalamasi)

| eksen | deger | COL yak. ort | DEGIL yanlis ort | f_alim ort | f_i60 ort | f_getiri ort | sinyal ort |
|---|---|---|---|---|---|---|---|
| N | 60 | 10.6 | 5.9 | +0p | +2.67 | +1.53 | 13048 |
| N | 120 | 10.1 | 2.9 | +2p | +2.95 | +1.78 | 8955 |
| konum | 0.35 | 9.9 | 3.8 | +1p | +2.99 | +1.25 | 6848 |
| konum | 0.5 | 10.6 | 3.9 | +1p | +3.15 | +1.83 | 9787 |
| konum | 1.01 | 10.6 | 5.6 | +1p | +2.29 | +1.88 | 16370 |
| bar | 15 | 11.6 | 5.6 | +0p | +2.75 | +1.56 | 12115 |
| bar | 25 | 9.1 | 3.2 | +2p | +2.87 | +1.74 | 9889 |
| inis | 0.0 | 10.4 | 4.5 | +1p | +2.67 | +1.68 | 12255 |
| inis | 5.0 | 10.4 | 4.5 | +1p | +2.73 | +1.63 | 11195 |
| inis | 10.0 | 10.3 | 4.3 | +1p | +3.03 | +1.65 | 9556 |
| retest | 0 | 11.0 | 5.0 | +1p | +3.00 | +1.86 | 13343 |
| retest | 2 | 9.7 | 3.9 | +1p | +2.62 | +1.45 | 8661 |
| yuv | parabol | 8.3 | 3.0 | +2p | +3.13 | +1.49 | 7961 |
| yuv | sma10 | 10.2 | 4.5 | +2p | +3.71 | +1.90 | 6957 |
| yuv | ucte_bir | 11.3 | 4.2 | +1p | +2.60 | +1.63 | 12917 |
| yuv | yok | 11.6 | 6.0 | -0p | +1.80 | +1.60 | 16172 |
| kucuk | 0.9 | 7.4 | 3.5 | +0p | +2.86 | +1.47 | 6200 |
| kucuk | 1.0 | 10.0 | 3.8 | +1p | +3.00 | +1.86 | 9653 |
| kucuk | 99.0 | 13.7 | 6.0 | +1p | +2.57 | +1.62 | 17152 |
| obek | 1 | 10.6 | 5.1 | +1p | +2.91 | +1.62 | 11711 |
| obek | 2 | 10.1 | 3.7 | +1p | +2.71 | +1.69 | 10293 |
| obek_yuk | 0 | 11.5 | 4.7 | +1p | +2.71 | +1.62 | 13625 |
| obek_yuk | 1 | 9.2 | 4.1 | +2p | +2.91 | +1.68 | 8379 |

## 1. varyant donem tablosu: N120 konum<=0.35 bar>=25 inis>=10% retest>=0 yuv=sma10 kucuk<=99 obek>=1 obek_yuk=hayir

| donem | n | alim a | alim b | bozulma | toparlanan | ileri60 | ileri120 | once +10 | getiri a | getiri b | f_alim | f_i60 | f_getiri |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2016-19 | 1234 | %71 | %74 | %16 | %3 | +9.06 | +19.67 | %59 | +6.49 | +6.40 | +0p | +0.43 | +0.01 |
| 2020-22 | 689 | %82 | %84 | %8 | %2 | +24.85 | +50.09 | %74 | +12.58 | +12.69 | +6p | +4.47 | +0.16 |
| 2023 | 173 | %87 | %91 | %8 | %3 | +48.72 | +67.78 | %69 | +27.37 | +28.90 | +10p | +25.41 | +14.17 |
| 2024-26 | 1068 | %73 | %76 | %19 | %3 | +6.98 | +10.31 | %63 | +3.45 | +3.33 | +4p | +1.59 | +0.55 |
| ABD 2022-23 | 2389 | %78 | %81 | %16 | %3 | +1.00 | +3.74 | %51 | -1.49 | -1.41 | +3p | -1.17 | -1.14 |
| ABD 2024-26 | 2304 | %77 | %80 | %15 | %3 | +7.57 | +14.57 | %54 | +2.85 | +2.76 | +1p | +1.68 | +1.40 |

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
| SUNTK_20240827 | COL | eski | hayir |
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

