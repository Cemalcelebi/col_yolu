# S4 sonuclari (esikler 2026-11-08T20:53:00.967583 tarihinde egitimden yazildi; test 2026-11-08T20:53:07.757350)

Egitim: 478 token, 363213 token-gun, +%100 gun 285, +%50 gun 1192. Test (liste >= 2025-07-01): 281 token, 91012 token-gun, +%100 gun 108, +%50 gun 462.

Secim kurali: her ozellik icin egitim yuzdelik (5..95) esikleri, iki yon; destek >= %5 ve sinyalde >= 20 olay; en yuksek lift. Kombinasyon: secilen tekli kurallarin ikili VE birlesimi, destek >= %2, en yuksek lift. Ikinci set: yalniz d >= 8 gunleri (listeden ilk haftayi disarida birakir).


### hedef +%100, populasyon tum (test taban 0.12%, egitim taban 0.08%)

| kural                                                                                          | egit_destek   | egit_P   |   egit_lift | test_destek   |   test_olay | test_P   | test_taban   |   test_lift | test_yakalama   |
|:-----------------------------------------------------------------------------------------------|:--------------|:---------|------------:|:--------------|------------:|:---------|:-------------|------------:|:----------------|
| onceki gun getirisi >= 0.115                                                                   | 5.0%          | 0.39%    |        4.91 | 5.4%          |          31 | 0.64%    | 0.12%        |        5.36 | 29%             |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862                                                | 9.9%          | 0.25%    |        3.15 | 10.1%         |          25 | 0.27%    | 0.12%        |        2.29 | 23%             |
| hacim orani (t-1 / onceki 7g ort.) >= 1.845                                                    | 10.0%         | 0.22%    |        2.82 | 11.7%         |          34 | 0.32%    | 0.12%        |        2.68 | 31%             |
| hacim orani (son 3g / onceki 7g) >= 1.966                                                      | 9.9%          | 0.22%    |        2.75 | 12.0%         |          29 | 0.27%    | 0.12%        |        2.24 | 27%             |
| listeden beri gun <= 39                                                                        | 5.0%          | 0.19%    |        2.46 | 11.7%         |          24 | 0.22%    | 0.12%        |        1.89 | 22%             |
| liste zirvesinden dusus (fitil) <= -0.9926                                                     | 15.0%         | 0.16%    |        2.08 | 6.9%          |          13 | 0.21%    | 0.12%        |        1.74 | 12%             |
| liste zirvesinden dusus (kapanis) <= -0.9922                                                   | 10.0%         | 0.15%    |        1.96 | 3.9%          |           7 | 0.20%    | 0.12%        |        1.66 | 6%              |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862 VE hacim orani (t-1 / onceki 7g ort.) >= 1.845 | 2.9%          | 0.39%    |        4.94 | 3.5%          |          18 | 0.56%    | 0.12%        |        4.72 | 17%             |

### hedef +%100, populasyon d>=8 (test taban 0.11%, egitim taban 0.07%)

| kural                                                                                          | egit_destek   | egit_P   |   egit_lift | test_destek   |   test_olay | test_P   | test_taban   |   test_lift | test_yakalama   |
|:-----------------------------------------------------------------------------------------------|:--------------|:---------|------------:|:--------------|------------:|:---------|:-------------|------------:|:----------------|
| onceki gun getirisi >= 0.1138                                                                  | 5.0%          | 0.37%    |        4.98 | 5.3%          |          32 | 0.68%    | 0.11%        |        6.09 | 32%             |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862                                                | 10.0%         | 0.25%    |        3.31 | 10.3%         |          25 | 0.27%    | 0.11%        |        2.43 | 25%             |
| hacim orani (t-1 / onceki 7g ort.) >= 1.847                                                    | 10.0%         | 0.21%    |        2.86 | 11.8%         |          32 | 0.30%    | 0.11%        |        2.71 | 32%             |
| hacim orani (son 3g / onceki 7g) >= 1.967                                                      | 10.0%         | 0.21%    |        2.86 | 12.1%         |          28 | 0.26%    | 0.11%        |        2.31 | 28%             |
| liste zirvesinden dusus (fitil) <= -0.9927                                                     | 15.0%         | 0.16%    |        2.18 | 7.0%          |          12 | 0.19%    | 0.11%        |        1.71 | 12%             |
| liste zirvesinden dusus (kapanis) <= -0.9923                                                   | 10.0%         | 0.16%    |        2.08 | 4.0%          |           7 | 0.20%    | 0.11%        |        1.77 | 7%              |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862 VE hacim orani (t-1 / onceki 7g ort.) >= 1.847 | 2.9%          | 0.39%    |        5.2  | 3.6%          |          18 | 0.56%    | 0.11%        |        5.01 | 18%             |

### hedef +%50, populasyon tum (test taban 0.51%, egitim taban 0.33%)

| kural                                                                                          | egit_destek   | egit_P   |   egit_lift | test_destek   |   test_olay | test_P   | test_taban   |   test_lift | test_yakalama   |
|:-----------------------------------------------------------------------------------------------|:--------------|:---------|------------:|:--------------|------------:|:---------|:-------------|------------:|:----------------|
| onceki gun getirisi >= 0.115                                                                   | 5.0%          | 1.78%    |        5.44 | 5.4%          |         124 | 2.54%    | 0.51%        |        5.01 | 27%             |
| listeden beri gun <= 39                                                                        | 5.0%          | 0.91%    |        2.77 | 11.7%         |         104 | 0.97%    | 0.51%        |        1.92 | 23%             |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862                                                | 9.9%          | 0.85%    |        2.58 | 10.1%         |         111 | 1.21%    | 0.51%        |        2.38 | 24%             |
| hacim orani (t-1 / onceki 7g ort.) >= 1.845                                                    | 10.0%         | 0.78%    |        2.36 | 11.7%         |         131 | 1.23%    | 0.51%        |        2.42 | 28%             |
| hacim orani (son 3g / onceki 7g) >= 1.966                                                      | 9.9%          | 0.75%    |        2.29 | 12.0%         |         124 | 1.14%    | 0.51%        |        2.24 | 27%             |
| liste zirvesinden dusus (kapanis) >= -0.2405                                                   | 5.0%          | 0.62%    |        1.9  | 8.1%          |          85 | 1.15%    | 0.51%        |        2.27 | 18%             |
| liste zirvesinden dusus (fitil) <= -0.9963                                                     | 10.0%         | 0.54%    |        1.64 | 4.2%          |          23 | 0.60%    | 0.51%        |        1.18 | 5%              |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862 VE hacim orani (t-1 / onceki 7g ort.) >= 1.845 | 2.9%          | 1.30%    |        3.98 | 3.5%          |          63 | 1.96%    | 0.51%        |        3.86 | 14%             |

### hedef +%50, populasyon d>=8 (test taban 0.48%, egitim taban 0.31%)

| kural                                                                                          | egit_destek   | egit_P   |   egit_lift | test_destek   |   test_olay | test_P   | test_taban   |   test_lift | test_yakalama   |
|:-----------------------------------------------------------------------------------------------|:--------------|:---------|------------:|:--------------|------------:|:---------|:-------------|------------:|:----------------|
| onceki gun getirisi >= 0.1138                                                                  | 5.0%          | 1.69%    |        5.39 | 5.3%          |         118 | 2.51%    | 0.48%        |        5.22 | 27%             |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862                                                | 10.0%         | 0.85%    |        2.7  | 10.3%         |         111 | 1.21%    | 0.48%        |        2.5  | 26%             |
| hacim orani (t-1 / onceki 7g ort.) >= 1.847                                                    | 10.0%         | 0.76%    |        2.42 | 11.8%         |         125 | 1.19%    | 0.48%        |        2.46 | 29%             |
| hacim orani (son 3g / onceki 7g) >= 1.967                                                      | 10.0%         | 0.75%    |        2.39 | 12.1%         |         121 | 1.12%    | 0.48%        |        2.32 | 28%             |
| liste zirvesinden dusus (kapanis) <= -0.997                                                    | 5.0%          | 0.59%    |        1.89 | 1.2%          |          10 | 0.92%    | 0.48%        |        1.9  | 2%              |
| liste zirvesinden dusus (fitil) <= -0.9963                                                     | 10.0%         | 0.54%    |        1.71 | 4.2%          |          23 | 0.61%    | 0.48%        |        1.26 | 5%              |
| aralik sikismasi (son 3g / onceki 10g) >= 1.862 VE hacim orani (t-1 / onceki 7g ort.) >= 1.847 | 2.9%          | 1.31%    |        4.16 | 3.6%          |          63 | 1.96%    | 0.48%        |        4.08 | 15%             |


### Olay gunleri vs ayni tokenlarin rastgele olay-disi gunleri (tum ornek; olay-disi orneklem n=7860, olay tokeni n=530, +%100 n=393, +%50 n=1654)

| ozellik                                |   +%100 gunu medyan |   +%50 gunu medyan |   rastgele olay-disi gun medyan | +%100 p25-p75   | olay-disi p25-p75   |
|:---------------------------------------|--------------------:|-------------------:|--------------------------------:|:----------------|:--------------------|
| listeden beri gun                      |           263       |            241     |                       318       | 112 / 447       | 158 / 527           |
| hacim orani (t-1 / onceki 7g ort.)     |             1.04    |              1.01  |                         0.866   | 0.608 / 2.11    | 0.538 / 1.17        |
| hacim orani (son 3g / onceki 7g)       |             1.12    |              1.05  |                         0.912   | 0.674 / 2.23    | 0.593 / 1.21        |
| liste zirvesinden dusus (kapanis)      |            -0.922   |             -0.884 |                        -0.895   | -0.985 / -0.69  | -0.973 / -0.71      |
| liste zirvesinden dusus (fitil)        |            -0.96    |             -0.937 |                        -0.938   | -0.993 / -0.825 | -0.985 / -0.815     |
| onceki gun getirisi                    |             0.00379 |              0.008 |                        -0.00434 | -0.056 / 0.123  | -0.0358 / 0.0218    |
| aralik sikismasi (son 3g / onceki 10g) |             1.18    |              1.14  |                         0.892   | 0.732 / 2.24    | 0.621 / 1.27        |
| son 10 gunde +%50 gun (0/1)            |             0       |              0     |                         0       | 0 / 0           | 0 / 0               |