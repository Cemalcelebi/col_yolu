# COL SEKIL — Cemal'in tarifi olcuye   (COL_SEKIL v1.0 (2026-10-21), 2026-10-24 22:01)

Etiket: COL 28 (Cemal'in colleri, 2024-26) | DEGIL 29 (eski OLUMSUZ 8 + 21 Eki kutulari 21).
Pencere = etiketin kendisi. n kucuk, donemler farkli: BULGU DEGIL, OLCUM. AUC 0.5 = ayirmiyor, 1.0/0.0 = tam ayiriyor.

DENETIM 24 Eki: 'bugun' DEGIL kutulari cokus haftasinda biten ve COL_BUGUN'un kendi ret nedenine ('yeni dip', 'dipte degil')
gore secilmis kutular; dip olculeri bu kutularda tanim geregi farkli. COL kutularinin sonu ise grafigin devami gorulerek cizildi
(19/29'da kirilim 5 bar icinde). Karsilastirilabilir negatif yalniz ayni yoldan (gozle) cizilen eski OLUMSUZ: AUC_esk sutunu esastir.

## Olcu basina medyan (COL | DEGIL) ve AUC (COL > DEGIL olasiligi)

| olcu | COL medyan | DEGIL medyan | AUC (tum DEGIL) | AUC_esk (yalniz eski OLUMSUZ) | yorum |
|---|---|---|---|---|---|
| aralik_pct | 3.34 | 3.00 | 0.58 | 0.54 | gun araligi % (mutlak kucuk mum) |
| aralik_kutu | 0.18 | 0.14 | 0.60 | 0.44 | aralik / kutu yuksekligi |
| aralik_ref60 | 0.89 | 0.95 | 0.44 | 0.54 | onceki 60 gune gore |
| aralik_ref250 | 0.79 | 0.87 | 0.38 | 0.48 | onceki 250 gune gore (kodun olcusu) |
| kucuk_oran250 | 0.65 | 0.62 | 0.58 | 0.47 | kodun 'kucuk' imzasi |
| dip_pos | 0.09 | 0.76 | 0.20 | 0.51 | dip kutunun neresinde (0 bas) |
| dip_sonrasi_bar | 26.50 | 12.00 | 0.79 | 0.54 | dipten sonra kac bar |
| retest | 4.00 | 1.00 | 0.71 | 0.37 | dibe yaklasan bar (savunma testi) |
| dip_oncesi_dusus | 4.00 | 14.40 | 0.21 | 0.56 | kutu basi -> dip % |
| egri_a | -4.00 | -13.20 | 0.67 | 0.53 | parabol ic bukeyligi (>0 yuvarlanma) |
| ilk_egim | 16.00 | 22.60 | 0.40 | 0.53 | dipten sonra ilk egim |
| son_egim | 3.50 | -2.90 | 0.69 | 0.59 | kutu sonu egim (>0 yukari) |
| obek | 2.00 | 0.00 | 0.74 | 0.47 | kucuk mum obegi sayisi |
| obek_yukselen | 1.00 | 1.00 | 0.48 | 0.53 | obekler yukseliyor mu |
| bb_son | 0.21 | 0.46 | 0.34 | 0.60 | kutu sonu Bollinger sirasi |
| hacim_kat60 | 0.91 | 0.72 | 0.71 | 0.57 | hacim / onceki 60 gun |
| uz | 34.00 | 44.00 | 0.35 | 0.44 | bar |
| yuvarlak | %32 evet | %10 evet | - | dipten sonra parabol yukari donmus |
| sma10_donus | %50 evet | %38 evet | - | SMA10 once duz/asagi sonra yukari |

## Bileşik: dip savunması + yuvarlanma (dip_pos <= 0.6 ve yuvarlak)

- COL: 8/28 gecer
- DEGIL: 2/29 gecer
- DEGIL yalniz eski OLUMSUZ: 2/8 gecer

## Etiket basina

        etiket sinif   set  uz  aralik_pct  aralik_kutu  aralik_ref250  dip_pos  dip_sonrasi_bar  retest  egri_a  son_egim  yuvarlak  obek  obek_yukselen  bb_son
ARZUM_20240806   COL  eski  34        4.49        0.222           0.73     0.50               16       4    -4.0       9.2     False     2           1.00    0.26
BASCM_20250302   COL  eski  80        1.18        0.034           0.86     0.56               34       1     0.5       6.2      True     2           1.00    0.26
BINBN_20260225   COL  eski  35        3.24        0.177           0.59     0.09               31       0    -8.0      -5.4     False     3           0.50    0.01
BURVA_20250626   COL  eski  17        2.85        0.283           0.70     0.12               14      12    -2.7      -1.1     False     2           0.00    0.07
EMNIS_20250414   COL  eski  23        3.14        0.257           0.93     0.09               20       3    -9.0      -5.9     False     2           1.00    0.06
ESCAR_20250919   COL  eski  59        3.10        0.166           0.73     0.63               21       5   -10.0       0.0     False     3           1.00    0.31
EUREN_20251001   COL  eski  23        5.84        0.333           1.45     0.09               20       7     5.6      10.5      True     0            NaN    0.18
EYGYO_20250528   COL  eski  30        3.78        0.207           1.13     0.10               26       3     8.2      18.0      True     1            NaN    0.46
GEDZA_20241015   COL  eski  34        3.08        0.171           0.67     0.00               33       4    -9.4       2.3     False     3           1.00    0.05
HDFGS_20250422   COL  eski  33        4.20        0.147           1.29     0.12               28       3   -10.7       1.3     False     2           1.00    0.28
 INFO_20250326   COL  eski  35        3.69        0.157           1.01     0.63               12       2     1.2      18.5      True     0            NaN    0.80
INVES_20250508   COL  eski  29        3.86        0.218           1.47     0.00               28       7   -21.4     -13.3     False     2           1.00    0.42
KATMR_20250416   COL  eski  60        3.62        0.097           1.00     0.05               56       7    -3.2      30.5     False     4           1.00    0.30
 ODAS_20240606   COL  eski  24        3.36        0.203           0.81     0.08               21       5   -15.8     -12.7     False     1            NaN    0.15
ORCAY_20241005   COL  eski  30        3.02        0.193           0.63     0.17               24       9    -2.1       0.1     False     1            NaN    0.21
 OTTO_20240702   COL  eski  51        0.85        0.039           0.58     0.00               50       0   -22.5     -17.7     False     4           0.00    0.02
SEYKM_20250415   COL  eski  61        3.17        0.161           0.72     0.72               16       1    -8.1       3.5     False     1            NaN    0.58
SKTAS_20240710   COL  eski  22        4.08        0.220           0.75     0.77                4       3     NaN       NaN     False     0            NaN    0.38
SMRTG_20241121   COL  eski  27        2.63        0.243           0.70     0.00               26       5   -11.4      -6.8     False     2           1.00    0.02
SUNTK_20240827   COL  eski  53        4.60        0.081           0.92     0.02               51       7    18.5      47.4      True     5           1.00    0.95
TATGD_20240530   COL  eski  29        2.98        0.219           0.68     0.31               19      10     7.6      15.4      True     1            NaN    0.20
TATGD_20240805   COL  eski  64        3.67        0.186           0.95     0.42               36       4     4.9      11.0      True     3           0.50    0.44
TEHOL_20241007   COL  eski  48        3.21        0.122           0.66     0.00               47      12   -19.2      -6.4     False     4           0.67    0.00
TEHOL_20260203   COL  eski  43        4.42        0.121           0.77     0.02               41       5     8.9      42.9      True     2           1.00    0.10
TUKAS_20241002   COL  eski  43        2.52        0.167           0.72     0.09               38       4    -0.4       3.9     False     3           1.00    0.04
VESTL_20241105   COL  eski  20        3.46        0.192           0.91     0.00               19       1     3.9      16.0      True     1            NaN    0.38
VESTL_20250602   COL  eski  48        3.33        0.125           0.97     0.15               40       6    -8.2      17.4     False     2           1.00    0.13
VRGYO_20250814   COL  eski  28        5.74        0.213           1.45     0.00               27       3   -24.4     -14.5     False     1            NaN    0.07
ARZUM_20260922 DEGIL bugun  20        4.33        0.294           1.15     0.95                0       0     NaN       NaN     False     0            NaN    0.09
AVGYO_20260915 DEGIL bugun  25        6.25        0.276           1.09     0.92                1       1     NaN       NaN     False     0            NaN    0.34
BIMAS_20260819 DEGIL bugun  44        2.42        0.137           0.86     0.98                0       0     NaN       NaN     False     0            NaN    0.82
CLEBI_20260825 DEGIL bugun  40        2.03        0.109           0.77     0.97                0       0     NaN       NaN     False     0            NaN    0.62
 DOCO_20260617 DEGIL bugun  88        2.55        0.127           0.83     0.76               20      10     3.5       8.4      True     3           1.00    0.08
EKGYO_20260915 DEGIL bugun  25        2.94        0.207           0.89     0.04               23       3   -13.2      -9.3     False     1            NaN    0.11
ENTRA_20260810 DEGIL bugun  51        2.77        0.117           0.80     0.57               21       1   -12.7      -0.3     False     2           1.00    0.18
 EUYO_20260825 DEGIL bugun  40        6.11        0.157           1.23     0.68               12       0   -72.2     -73.5     False     0            NaN    0.80
GLYHO_20260709 DEGIL bugun  72        2.98        0.128           0.90     0.71               20       2    -4.4      13.7     False     0            NaN    0.71
GRSEL_20260904 DEGIL bugun  32        3.61        0.182           1.15     0.34               20       4    -1.1       4.9     False     1            NaN    0.44
HTTBT_20260825 DEGIL bugun  40        3.20        0.133           1.03     0.47               20       2   -39.3     -33.4     False     0            NaN    0.78
 LOGO_20260609 DEGIL bugun  94        2.69        0.110           0.86     0.99                0       0     NaN       NaN     False     0            NaN    0.90
MTRYO_20260730 DEGIL bugun  58        4.71        0.135           1.08     0.76               13       3   -35.1     -38.3     False     1            NaN    0.69
NTGAZ_20260624 DEGIL bugun  83        3.00        0.143           0.83     0.99                0       0     NaN       NaN     False     0            NaN    0.51
NUHCM_20260518 DEGIL bugun 106        2.26        0.111           0.86     0.80               20       1   -19.0     -15.2     False     1            NaN    0.33
OYLUM_20260817 DEGIL bugun  46        3.24        0.128           0.87     0.54               20       0   -29.3     -14.8     False     1            NaN    0.74
SEKFK_20260820 DEGIL bugun  43        3.83        0.138           1.31     0.98                0       0     NaN       NaN     False     0            NaN    0.69
TABGD_20260901 DEGIL bugun  35        3.35        0.137           1.13     0.97                0       0     NaN       NaN     False     0            NaN    0.84
VAKKO_20260708 DEGIL bugun  73        3.92        0.101           1.22     0.99                0       0     NaN       NaN     False     0            NaN    0.92
YGGYO_20260819 DEGIL bugun  44        2.41        0.173           0.68     0.98                0       0     NaN       NaN     False     0            NaN    0.02
ZRGYO_20260812 DEGIL bugun  49        2.26        0.147           0.82     0.96                1       1     NaN       NaN     False     0            NaN    0.47
ALTNY_20251023 DEGIL  eski  54        2.63        0.153           0.80     0.22               41      19     4.9      10.3      True     4           0.67    0.12
 ERCB_20250613 DEGIL  eski 109        2.85        0.086           0.94     0.00              108       1   -85.4     -82.6     False     7           0.50    0.74
GARFA_20260731 DEGIL  eski  32        2.64        0.370           0.72     0.00               31      26    -2.8      -0.3     False     3           1.00    0.04
GEDIK_20250915 DEGIL  eski  34        4.60        0.191           1.33     0.00               33      12    24.0      31.8      True     1            NaN    0.46
PAPIL_20251112 DEGIL  eski  20        2.69        0.269           0.47     0.60                7       7     NaN       NaN     False     1            NaN    0.00
SDTTR_20240328 DEGIL  eski  24        4.95        0.231           0.76     0.00               23       6   -15.1      -2.9     False     2           1.00    0.06
SEYKM_20260308 DEGIL  eski  34        4.03        0.213           0.79     0.62               12       0   -14.0      -7.0     False     2           1.00    0.11
TUREX_20260330 DEGIL  eski  99        3.33        0.072           1.00     0.91                8       4    -2.3       5.9     False     0            NaN    0.07
