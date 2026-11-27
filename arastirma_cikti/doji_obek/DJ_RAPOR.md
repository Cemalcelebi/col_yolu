# DJ RAPOR — aynı seviyede doji öbekleri: doji sayısına göre sonrası

Kod sha 72d92ca7ffc6, eşik sha 94ffcc2e0b8f; ön kayıt commit a2cb80ba840c307034663d29001b3534a00d551e|2026-11-27T06:47:03+00:00. Evren bugün yaşayan hisseler (yukarı yanlı). Getiriler fiyat değişimidir (komisyon / kayma yok). Kasa açılmadı (veri <= 2022-12-31).

## SONUÇ

GENEL: DOJİ ÖBEĞİ SONRASI AYIRT EDİCİ DEĞİL (bu tanımla)
DOZ - YANIT: DOJİ SAYISI ETKİSİZ (bu tanımla)

### Yön (R15, TOPLAM FARK = R15 - aynı hissenin rastgele günü)

| hücre | k | n | ay | R15 ort | R15 medyan | TOPLAM FARK [%95] | SEÇİM [%95] | +2ATR önce | rastgele | -2ATR önce | rastgele | ASİMETRİ [%95] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD|d1619 | k=1 (tek doji) | 172339 | 48 | 0,86% | 0,82% | -0,06% [-0,69%; 0,58%] | -0,02% [-0,06%; 0,03%] | 33,0% | 32,9% | 27,1% | 26,7% | -0,3% [-4,9%; 4,3%] |
| ABD|d1619 | k=2 | 31114 | 48 | 0,85% | 0,85% | -0,07% [-0,76%; 0,61%] | -0,08% [-0,18%; 0,02%] | 33,2% | 32,7% | 26,6% | 26,5% | 0,4% [-4,4%; 5,2%] |
| ABD|d1619 | k=3 | 4990 | 48 | 0,72% | 0,66% | -0,21% [-0,95%; 0,53%] | -0,13% [-0,35%; 0,10%] | 32,1% | 32,5% | 27,1% | 26,3% | -1,2% [-6,7%; 4,3%] |
| ABD|d1619 | k=4+ | 844 | 48 | 1,79% | 1,08% | 0,94% [-0,18%; 2,16%] | 0,92% [0,06%; 1,97%] | 32,5% | 32,1% | 25,9% | 26,3% | 0,7% [-6,4%; 7,8%] |
| ABD|d1619 | herhangi gün | 400337 | — | 0,91% | 0,87% | — | — | 32,9% | — | 26,7% | — | — |
| ABD|d2022 | k=1 (tek doji) | 163181 | 36 | 0,37% | 0,14% | -0,05% [-1,64%; 1,48%] | 0,01% [-0,08%; 0,10%] | 30,7% | 30,4% | 29,6% | 29,0% | -0,4% [-6,2%; 5,4%] |
| ABD|d2022 | k=2 | 26472 | 36 | 0,65% | 0,22% | 0,30% [-1,13%; 1,75%] | 0,11% [-0,08%; 0,30%] | 30,8% | 30,2% | 28,5% | 28,9% | 0,9% [-5,3%; 7,0%] |
| ABD|d2022 | k=3 | 3651 | 36 | 0,66% | 0,17% | 0,38% [-1,03%; 1,79%] | 0,09% [-0,30%; 0,46%] | 30,6% | 29,8% | 27,7% | 28,6% | 1,7% [-5,2%; 8,6%] |
| ABD|d2022 | k=4+ | 532 | 36 | -0,02% | -0,18% | -0,18% [-1,84%; 1,43%] | -0,34% [-1,10%; 0,41%] | 26,9% | 29,2% | 27,6% | 28,7% | -1,2% [-10,9%; 8,5%] |
| ABD|d2022 | herhangi gün | 391113 | — | 0,40% | 0,12% | — | — | 30,4% | — | 29,0% | — | — |
| AVR|d1619 | k=1 (tek doji) | 34025 | 48 | 0,71% | 0,73% | -0,02% [-0,56%; 0,49%] | -0,01% [-0,08%; 0,05%] | 32,8% | 33,1% | 27,1% | 26,8% | -0,5% [-5,4%; 4,4%] |
| AVR|d1619 | k=2 | 6027 | 48 | 0,63% | 0,68% | -0,10% [-0,69%; 0,48%] | -0,11% [-0,27%; 0,04%] | 32,9% | 33,0% | 26,9% | 26,8% | -0,2% [-5,4%; 5,0%] |
| AVR|d1619 | k=3 | 951 | 48 | 0,82% | 0,94% | 0,12% [-0,53%; 0,76%] | -0,07% [-0,40%; 0,26%] | 34,8% | 33,0% | 25,4% | 26,6% | 3,0% [-3,8%; 9,4%] |
| AVR|d1619 | k=4+ | 140 | 46 | 0,27% | 0,07% | -0,41% [-1,54%; 0,67%] | -0,59% [-1,40%; 0,28%] | 34,3% | 32,8% | 24,3% | 26,0% | 3,1% [-12,0%; 16,2%] |
| AVR|d1619 | herhangi gün | 80675 | — | 0,74% | 0,75% | — | — | 33,2% | — | 26,8% | — | — |
| AVR|d2022 | k=1 (tek doji) | 26799 | 36 | 0,20% | 0,36% | 0,05% [-1,29%; 1,29%] | 0,02% [-0,09%; 0,12%] | 30,8% | 30,4% | 29,1% | 29,0% | 0,4% [-6,9%; 7,4%] |
| AVR|d2022 | k=2 | 4332 | 36 | 0,32% | 0,43% | 0,15% [-1,01%; 1,27%] | 0,09% [-0,13%; 0,31%] | 30,6% | 30,4% | 28,1% | 28,9% | 0,9% [-6,5%; 8,3%] |
| AVR|d2022 | k=3 | 607 | 36 | 1,07% | 0,73% | 0,84% [-0,33%; 1,99%] | 0,68% [0,12%; 1,27%] | 32,5% | 30,3% | 26,0% | 28,6% | 4,7% [-5,0%; 13,7%] |
| AVR|d2022 | k=4+ | 58 | 29 | 0,09% | 0,11% | -0,23% [-2,30%; 1,63%] | -0,12% [-1,42%; 1,17%] | 31,0% | 30,0% | 24,1% | 27,3% | 4,2% [-15,5%; 23,6%] |
| AVR|d2022 | herhangi gün | 64958 | — | 0,15% | 0,31% | — | — | 30,4% | — | 29,1% | — | — |

Hüküm (TOPLAM FARK): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ ÖLÇÜLEMEDİ
Hüküm (ASİMETRİ): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ ÖLÇÜLEMEDİ
Hüküm (SEÇİM): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ TEK DÖNEM

### Hareketin büyüklüğü (|R15| / (ATRP20 x karekök 15); KAT = olay / aynı hissenin rastgele günü)

| hücre | k | olay | rastgele | KAT [%95] | FARK [%95] |
|---|---|---|---|---|---|
| ABD|d1619 | k=1 (tek doji) | 0,564 | 0,554 | 1,019 [0,975; 1,064] | 0,010 [-0,014; 0,035] |
| ABD|d1619 | k=2 | 0,561 | 0,550 | 1,020 [0,977; 1,066] | 0,011 [-0,013; 0,036] |
| ABD|d1619 | k=3 | 0,557 | 0,547 | 1,019 [0,972; 1,069] | 0,010 [-0,016; 0,037] |
| ABD|d1619 | k=4+ | 0,607 | 0,545 | 1,113 [1,041; 1,187] | 0,061 [0,022; 0,101] |
| ABD|d2022 | k=1 (tek doji) | 0,575 | 0,574 | 1,002 [0,916; 1,123] | 0,001 [-0,048; 0,071] |
| ABD|d2022 | k=2 | 0,561 | 0,568 | 0,988 [0,915; 1,091] | -0,007 [-0,049; 0,052] |
| ABD|d2022 | k=3 | 0,569 | 0,563 | 1,010 [0,930; 1,104] | 0,006 [-0,040; 0,058] |
| ABD|d2022 | k=4+ | 0,587 | 0,559 | 1,051 [0,906; 1,251] | 0,029 [-0,054; 0,145] |
| AVR|d1619 | k=1 (tek doji) | 0,552 | 0,548 | 1,007 [0,953; 1,067] | 0,004 [-0,025; 0,036] |
| AVR|d1619 | k=2 | 0,540 | 0,547 | 0,987 [0,929; 1,052] | -0,007 [-0,039; 0,028] |
| AVR|d1619 | k=3 | 0,526 | 0,547 | 0,962 [0,879; 1,051] | -0,021 [-0,065; 0,029] |
| AVR|d1619 | k=4+ | 0,508 | 0,541 | 0,941 [0,810; 1,087] | -0,032 [-0,101; 0,048] |
| AVR|d2022 | k=1 (tek doji) | 0,570 | 0,561 | 1,015 [0,898; 1,182] | 0,008 [-0,057; 0,101] |
| AVR|d2022 | k=2 | 0,552 | 0,559 | 0,988 [0,888; 1,116] | -0,007 [-0,064; 0,064] |
| AVR|d2022 | k=3 | 0,528 | 0,554 | 0,953 [0,852; 1,072] | -0,026 [-0,082; 0,042] |
| AVR|d2022 | k=4+ | 0,523 | 0,516 | 1,014 [0,770; 1,268] | 0,007 [-0,115; 0,141] |

Hüküm (BÜYÜKLÜK FARKI): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ TEK DÖNEM

### Çıkış yönü (öbek bandı; 15 bar içinde ilk kapanış) ve devam (çıkıştan sonraki 10 bar, çıkış yönünde)

| hücre | k | yukarı | aşağı | hiç | çıkış barı (medyan) | DEVAM yukarı [%95] (n) | DEVAM aşağı [%95] (n) | sürüklenmesiz yukarı | sürüklenmesiz aşağı |
|---|---|---|---|---|---|---|---|---|---|
| ABD|d1619 | k=1 (tek doji) | 53,8% | 45,9% | 0,3% | 1 | 0,52% [0,06%; 0,98%] (92777) | -0,61% [-1,08%; -0,15%] (79058) | -0,11% [-0,58%; 0,33%] | -0,06% [-0,56%; 0,40%] |
| ABD|d1619 | k=2 | 55,1% | 44,0% | 0,9% | 2 | 0,49% [0,00%; 0,95%] (17134) | -0,62% [-1,19%; -0,10%] (13704) | -0,16% [-0,63%; 0,31%] | -0,10% [-0,65%; 0,43%] |
| ABD|d1619 | k=3 | 54,5% | 43,9% | 1,6% | 2 | 0,32% [-0,27%; 0,88%] (2719) | -0,90% [-1,58%; -0,26%] (2190) | -0,35% [-0,94%; 0,20%] | -0,38% [-1,03%; 0,26%] |
| ABD|d1619 | k=4+ | 55,7% | 42,4% | 1,9% | 3 | 1,22% [0,15%; 2,53%] (470) | -0,97% [-2,03%; 0,03%] (358) | 0,55% [-0,47%; 1,82%] | -0,56% [-1,57%; 0,38%] |
| ABD|d2022 | k=1 (tek doji) | 50,8% | 49,1% | 0,1% | 1 | 0,03% [-0,93%; 0,93%] (82882) | -0,42% [-1,63%; 0,80%] (80065) | -0,30% [-1,24%; 0,60%] | -0,24% [-1,46%; 0,97%] |
| ABD|d2022 | k=2 | 51,8% | 47,6% | 0,6% | 2 | 0,15% [-0,72%; 1,02%] (13715) | -0,57% [-1,83%; 0,65%] (12603) | -0,16% [-1,03%; 0,69%] | -0,46% [-1,68%; 0,72%] |
| ABD|d2022 | k=3 | 52,5% | 46,2% | 1,3% | 2 | 0,10% [-0,80%; 0,90%] (1917) | -0,80% [-2,21%; 0,48%] (1686) | -0,21% [-1,08%; 0,62%] | -0,79% [-2,17%; 0,47%] |
| ABD|d2022 | k=4+ | 50,9% | 47,4% | 1,7% | 2 | -0,24% [-1,63%; 1,11%] (271) | -0,90% [-2,85%; 0,88%] (252) | -0,45% [-1,83%; 0,89%] | -0,95% [-2,89%; 0,83%] |
| AVR|d1619 | k=1 (tek doji) | 53,8% | 45,9% | 0,3% | 1 | 0,42% [0,04%; 0,79%] (18306) | -0,54% [-0,92%; -0,17%] (15618) | -0,06% [-0,43%; 0,30%] | -0,10% [-0,47%; 0,26%] |
| AVR|d1619 | k=2 | 53,8% | 45,3% | 0,9% | 2 | 0,32% [-0,08%; 0,72%] (3243) | -0,53% [-0,98%; -0,10%] (2729) | -0,15% [-0,57%; 0,24%] | -0,10% [-0,56%; 0,34%] |
| AVR|d1619 | k=3 | 50,9% | 47,4% | 1,7% | 2 | 0,54% [0,09%; 0,96%] (484) | -0,59% [-1,14%; -0,06%] (451) | 0,09% [-0,34%; 0,50%] | -0,15% [-0,71%; 0,39%] |
| AVR|d1619 | k=4+ | 55,0% | 42,9% | 2,1% | 3 | -0,34% [-1,33%; 0,51%] (77) | -0,88% [-3,02%; 0,90%] (60) | -0,80% [-1,78%; 0,02%] | -0,51% [-2,53%; 1,17%] |
| AVR|d2022 | k=1 (tek doji) | 51,3% | 48,2% | 0,4% | 1 | 0,22% [-0,50%; 0,92%] (13753) | 0,10% [-1,04%; 1,34%] (12926) | 0,12% [-0,60%; 0,80%] | 0,14% [-0,97%; 1,38%] |
| AVR|d2022 | k=2 | 52,1% | 46,4% | 1,5% | 2 | 0,23% [-0,45%; 0,88%] (2256) | 0,03% [-1,11%; 1,24%] (2008) | 0,13% [-0,54%; 0,76%] | 0,08% [-1,04%; 1,31%] |
| AVR|d2022 | k=3 | 54,4% | 44,2% | 1,5% | 2 | 1,24% [0,34%; 2,05%] (330) | 0,06% [-1,09%; 1,30%] (267) | 1,10% [0,23%; 1,89%] | 0,18% [-1,00%; 1,41%] |
| AVR|d2022 | k=4+ | 50,0% | 48,3% | 1,7% | 3 | 1,96% [-0,05%; 4,13%] (29) | 2,78% [0,26%; 5,34%] (28) | 1,70% [-0,13%; 3,68%] | 2,84% [0,41%; 5,38%] |

Hüküm (DEVAM yukarı): k=1 (tek doji) TEK DÖNEM; k=2 TEK DÖNEM; k=3 AYRIŞMIYOR; k=4+ TEK DÖNEM
Hüküm (DEVAM aşağı): k=1 (tek doji) TEK DÖNEM; k=2 TEK DÖNEM; k=3 TEK DÖNEM; k=4+ ÖLÇÜLEMEDİ

### Önceki 10 bara göre (dönüş payı = R15 işareti önceki yönün tersi)

| hücre | k | düşüş sonrası n | dönüş | taban | FARK [%95] | yükseliş sonrası n | dönüş | taban | FARK [%95] |
|---|---|---|---|---|---|---|---|---|---|
| ABD|d1619 | k=1 (tek doji) | 75896 | 56,6% | 56,9% | -0,3% [-3,9%; 3,3%] | 95716 | 45,1% | 44,7% | 0,4% [-3,2%; 4,2%] |
| ABD|d1619 | k=2 | 13303 | 57,0% | 56,9% | 0,0% [-3,9%; 3,9%] | 17673 | 44,4% | 44,7% | -0,3% [-3,9%; 3,5%] |
| ABD|d1619 | k=3 | 2105 | 55,5% | 56,9% | -1,5% [-5,8%; 2,6%] | 2845 | 45,6% | 44,7% | 0,9% [-3,1%; 5,2%] |
| ABD|d1619 | k=4+ | 329 | 59,3% | 56,9% | 2,3% [-5,3%; 10,1%] | 511 | 45,2% | 44,7% | 0,5% [-5,0%; 6,2%] |
| ABD|d2022 | k=1 (tek doji) | 77610 | 50,0% | 49,7% | 0,3% [-5,0%; 5,6%] | 85129 | 48,8% | 48,7% | 0,1% [-5,0%; 5,4%] |
| ABD|d2022 | k=2 | 11960 | 50,1% | 49,7% | 0,4% [-4,6%; 5,8%] | 14426 | 48,2% | 48,7% | -0,5% [-5,6%; 4,9%] |
| ABD|d2022 | k=3 | 1615 | 50,3% | 49,7% | 0,6% [-4,6%; 6,1%] | 2019 | 48,4% | 48,7% | -0,3% [-5,9%; 5,3%] |
| ABD|d2022 | k=4+ | 228 | 47,8% | 49,7% | -1,9% [-10,1%; 6,7%] | 301 | 50,8% | 48,7% | 2,1% [-5,1%; 9,6%] |
| AVR|d1619 | k=1 (tek doji) | 14852 | 56,8% | 57,1% | -0,3% [-4,4%; 4,0%] | 18999 | 45,0% | 44,5% | 0,4% [-3,6%; 4,4%] |
| AVR|d1619 | k=2 | 2626 | 57,4% | 57,1% | 0,3% [-4,0%; 4,7%] | 3365 | 45,0% | 44,5% | 0,5% [-3,9%; 5,2%] |
| AVR|d1619 | k=3 | 411 | 57,2% | 57,1% | 0,1% [-7,3%; 7,1%] | 534 | 42,3% | 44,5% | -2,2% [-8,7%; 4,7%] |
| AVR|d1619 | k=4+ | 51 | 45,1% | 57,1% | -12,0% [-24,9%; 0,6%] | 88 | 44,3% | 44,5% | -0,2% [-9,1%; 8,7%] |
| AVR|d2022 | k=1 (tek doji) | 12593 | 51,6% | 52,2% | -0,6% [-6,4%; 5,5%] | 14070 | 47,5% | 48,5% | -0,9% [-6,3%; 4,9%] |
| AVR|d2022 | k=2 | 1938 | 52,7% | 52,2% | 0,5% [-5,3%; 6,2%] | 2366 | 47,4% | 48,5% | -1,0% [-6,9%; 5,4%] |
| AVR|d2022 | k=3 | 267 | 53,9% | 52,2% | 1,7% [-5,7%; 9,1%] | 337 | 43,3% | 48,5% | -5,1% [-11,8%; 1,8%] |
| AVR|d2022 | k=4+ | 25 | 48,0% | 52,2% | -4,2% [-23,0%; 13,2%] | 29 | 44,8% | 48,5% | -3,6% [-22,6%; 15,8%] |

Hüküm (dönüş, düşüş sonrası): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ ÖLÇÜLEMEDİ
Hüküm (dönüş, yükseliş sonrası): k=1 (tek doji) AYRIŞMIYOR; k=2 AYRIŞMIYOR; k=3 AYRIŞMIYOR; k=4+ ÖLÇÜLEMEDİ

### Doz - yanıt (k = 1 -> 2 -> 3 -> 4+)

- TOPLAM_FARK: yön (ABD 16-19, 20-22) [0, 0], tek yönlü False, k3 / k4+ - k1 farkı ayrışıyor False -> etkisiz
- BUYUKLUK_FARK: yön (ABD 16-19, 20-22) [0, 0], tek yönlü False, k3 / k4+ - k1 farkı ayrışıyor False -> etkisiz
- YUKARI_PAY: yön (ABD 16-19, 20-22) [0, 0], tek yönlü False, k3 / k4+ - k1 farkı ayrışıyor False -> etkisiz

k - tek doji farkları (TOPLAM FARK, ABD):
- ABD|d1619: k=2 - 1: -0,01% [-0,12%; 0,10%]; k=3 - 1: -0,15% [-0,44%; 0,14%]; k=4 - 1: 1,00% [0,14%; 2,03%]
- ABD|d2022: k=2 - 1: 0,34% [-0,02%; 0,76%]; k=3 - 1: 0,43% [-0,16%; 1,03%]; k=4 - 1: -0,13% [-1,29%; 1,00%]

### BİLGİ satırları (hükmü değiştirmez)

Bağlam (TOPLAM FARK, KONUM120 üçte biri):
- ABD|d1619: k=1 (tek doji): DIPTE 0,73% [-0,38%; 1,85%] (n 46137), ORTADA 0,00% [-0,66%; 0,65%] (n 42805), TEPEDE -0,52% [-1,03%; -0,03%] (n 82496) | k=2: DIPTE 0,73% [-0,45%; 1,96%] (n 8055), ORTADA 0,09% [-0,62%; 0,76%] (n 7555), TEPEDE -0,56% [-1,10%; -0,04%] (n 15332) | k=3: DIPTE 0,13% [-1,29%; 1,44%] (n 1263), ORTADA 0,11% [-0,72%; 0,88%] (n 1197), TEPEDE -0,53% [-1,15%; 0,11%] (n 2492) | k=4+: DIPTE 1,73% [-0,28%; 4,13%] (n 208), ORTADA 1,26% [-0,24%; 2,82%] (n 200), TEPEDE 0,41% [-1,00%; 2,21%] (n 433)
- ABD|d2022: k=1 (tek doji): DIPTE 0,30% [-1,68%; 2,36%] (n 56724), ORTADA -0,35% [-1,99%; 1,23%] (n 41423), TEPEDE -0,17% [-1,78%; 1,21%] (n 63452) | k=2: DIPTE 0,79% [-1,09%; 2,79%] (n 8891), ORTADA 0,31% [-1,25%; 1,87%] (n 6619), TEPEDE -0,15% [-1,70%; 1,21%] (n 10648) | k=3: DIPTE 0,81% [-1,11%; 2,93%] (n 1192), ORTADA 0,11% [-1,64%; 1,73%] (n 903), TEPEDE 0,18% [-1,15%; 1,45%] (n 1499) | k=4+: DIPTE 0,08% [-2,22%; 2,43%] (n 153), ORTADA -0,02% [-2,40%; 2,31%] (n 116), TEPEDE -0,47% [-2,62%; 1,56%] (n 251)
- AVR|d1619: k=1 (tek doji): DIPTE 0,37% [-0,53%; 1,25%] (n 8665), ORTADA 0,05% [-0,49%; 0,60%] (n 8741), TEPEDE -0,28% [-0,74%; 0,18%] (n 16543) | k=2: DIPTE 0,29% [-0,67%; 1,24%] (n 1507), ORTADA 0,01% [-0,63%; 0,58%] (n 1518), TEPEDE -0,37% [-0,91%; 0,16%] (n 2982) | k=3: DIPTE 0,36% [-0,84%; 1,53%] (n 233), ORTADA 0,52% [-0,28%; 1,34%] (n 244), TEPEDE -0,25% [-1,02%; 0,49%] (n 472) | k=4+: DIPTE -1,40% [-4,40%; 1,11%] (n 32), ORTADA -0,17% [-1,70%; 1,34%] (n 32), TEPEDE -0,08% [-1,48%; 1,37%] (n 75)
- AVR|d2022: k=1 (tek doji): DIPTE 0,60% [-1,29%; 2,48%] (n 8564), ORTADA -0,35% [-1,88%; 1,04%] (n 6813), TEPEDE -0,12% [-1,39%; 0,83%] (n 11375) | k=2: DIPTE 0,58% [-1,28%; 2,50%] (n 1291), ORTADA -0,02% [-1,27%; 1,10%] (n 1083), TEPEDE -0,04% [-1,21%; 0,88%] (n 1952) | k=3: DIPTE 2,22% [0,26%; 4,12%] (n 175), ORTADA 0,87% [-0,55%; 2,39%] (n 143), TEPEDE -0,01% [-1,33%; 1,03%] (n 289) | k=4+: DIPTE 0,57% [-3,49%; 4,59%] (n 19), ORTADA -2,30% [-7,68%; 2,25%] (n 12), TEPEDE 0,11% [-1,91%; 1,87%] (n 27)

D15 kolu (gövde <= 0,15 boy; TOPLAM FARK):
- ABD|d1619: k=1 (tek doji) n 236567 -0,05% [-0,68%; 0,58%]; k=2 n 60532 -0,02% [-0,69%; 0,65%]; k=3 n 13658 -0,10% [-0,78%; 0,59%]; k=4+ n 3029 0,15% [-0,55%; 0,84%]
- ABD|d2022: k=1 (tek doji) n 226385 -0,05% [-1,68%; 1,49%]; k=2 n 52228 0,24% [-1,19%; 1,66%]; k=3 n 10246 0,16% [-1,29%; 1,55%]; k=4+ n 1950 0,03% [-1,38%; 1,42%]
- AVR|d1619: k=1 (tek doji) n 46729 -0,00% [-0,54%; 0,51%]; k=2 n 11508 0,01% [-0,53%; 0,53%]; k=3 n 2472 -0,09% [-0,70%; 0,53%]; k=4+ n 510 -0,24% [-1,05%; 0,54%]
- AVR|d2022: k=1 (tek doji) n 37259 0,08% [-1,28%; 1,33%]; k=2 n 8583 0,19% [-0,98%; 1,29%]; k=3 n 1651 0,67% [-0,44%; 1,76%]; k=4+ n 282 0,11% [-1,35%; 1,47%]

HAFTA kolu (haftalık mum, 15 hafta; TOPLAM FARK):
- ABD|d1619: k=1 (tek doji) n 33228 -0,23% [-2,81%; 1,95%]; k=2 n 5632 -0,36% [-3,57%; 2,31%]; k=3 n 825 -1,72% [-6,25%; 1,83%]; k=4+ n 97 -0,31% [-5,71%; 4,49%]
- ABD|d2022: k=1 (tek doji) n 29754 -0,25% [-4,70%; 4,45%]; k=2 n 5139 -1,45% [-5,47%; 2,77%]; k=3 n 831 -3,85% [-7,79%; 0,72%]; k=4+ n 119 -6,94% [-13,12%; -0,36%]
- AVR|d1619: k=1 (tek doji) n 6485 0,09% [-2,12%; 1,90%]; k=2 n 1119 0,42% [-2,07%; 2,58%]; k=3 n 173 -0,09% [-3,63%; 3,34%]; k=4+ n 24 -6,75% [-13,12%; 0,88%]
- AVR|d2022: k=1 (tek doji) n 4828 -0,27% [-3,49%; 3,04%]; k=2 n 811 -1,21% [-4,33%; 1,86%]; k=3 n 121 -2,12% [-6,36%; 1,82%]; k=4+ n 16 -1,13% [-10,96%; 8,75%]

Tabanı olmayan (hissenin o hücrede rastgele günü yok) düşen olay: {'ABD': 9, 'AVR': 0}

## KONTROL LİSTESİ

| Kod | Yanıt | Kanıt |
|---|---|---|
| K1 | EVET | taban aynı hissenin aynı hücredeki rastgele (her 5. bar) günleri: TOPLAM FARK = R15 - T1, U2 / D2 / büyüklük için p_h / q_h / h_h aynı hisseden; ATR ölçekli eşikler (oynaklığın mekanik etkisi ATRP20 ile ölçeklenir); D2 aynası ve asimetri mekanik üstünlüğü ölçer; tek doji (k = 1) ve herhangi gün iki taban; k farkları aynı ay ağırlıklarıyla; SEÇİM = R15 - PİYASA(t) |
| K2 | EVET | doji / öbek / k t barına kadarki barlarla (test: t + 1 ve sonrası bozulunca olaylar aynı); ORT_BOY t - 10 .. t - 1; ATR20 ve ADIM t'ye kadar; sonuç sütunları ayrı fonksiyonda, yalnız kapıdan sonra; olay dosyası ile getiri dosyası ayrı; öbeğin son uzunluğu yalnız sayımda (bilgi); veri <= 2022-12-31 assert |
| K3 | EVET | MI.mi_veri geçerli barları (H > L, V > 0, O/H/L/C sonlu > 0); ölü / fiyat adımına yapışmış bar doji sayılmaz (ADIM kuralı, test); öbekte takvim satırı farkı > 6 bağlanmaz; 15 bar <= 30 takvim satırı; giriş P2 evreninde |
| K4 | EVET | öbek başına her k satırında bir olay (4+ = 4. doji; sonrakiler olay değil); olaylar örtüşebilir, çıkarım ay kümeli bootstrap; n ve farklı ay ayrı yazılır; medyan R15 yazılır; taban her 5. bar |
| K5 | EVET | giriş = t + 1 barının açılışı; çıkış devamı çıkış barından sonraki açılıştan (e + 1); P15 de giriş satırından |
| K6 | EVET | OS / MI bölünme düzeltmeli açık kopya (YO ile aynı depo); getiriler oransal, yerel para; pazar içi karşılaştırma; eşikler ATR oranlı (birimden bağımsız); fiyat adımı kuralı birimden bağımsız (kendi fiyat farklarından) |
| K7 | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer; raporda yazılır; kasa açılmaz |
| K8 | EVET | n >= 1.000 değilse ÖLÇÜLEMEDİ (n < 30 'örneklem yetersiz'); iki ABD dönemi + iki AVR dönemi; BH q 0,10 (32 satır aile); en kalabalık 3 ay payı her satırda |
| K9 | EVET | DJ_ON_KAYIT.md: DJ_KOD_SHA, DJ_ESIK_SHA, olay / taban dosya sha'ları, SAYIM_SHA, yorum noktaları; ölçüm kapısı: kontrol + sha + ön kayıt commit + push + kod temiz; getiri dosyası varsa ikinci koşu DURUR; eşikler sonuca göre değişmez |
| K10 | EVET | doji / öbek kuralı sentetik pozitif / negatif serilerle (yakalama >= %95, yanlış kabul <= %5); uygunluk maskesi YO.yo_ornek_maske ile 5. barlarda birebir; dokunma YO.yo_ilk_dokunma; kaynak npz sha YO ön kaydıyla aynı; PDF'te gerçek örnekler gözle denetlenir |
| K11 | EVET | rapordan önce >= 3 satır olay + getiri dosyalarından bağımsız kısa kodla yeniden üretilir; rapordaki sayılar dj_sonuc.json'dan basılır |
| K12 | EVET | 'emare / etkili' sözü yalnız hüküm kuralıyla; ABD tek dönem 'TEK DÖNEM'; sayı ile yorum ayrı cümlede; evren bugün yaşayanlar; fiyat değişimi gerçek kâr değil (komisyon / kayma yok) |
| K13 | EVET | çakışma kapısı (_cakisma_kontrol_dj); mevcut modüller ve defter dosyaları değişmez (yalnız import; SEKIL_DEVAM / WEB_DESEN içe alınmaz); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat |
| K14 | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## Yeniden üretim (bağımsız kısa kod)

- Bağımsız kısa kod (olay + getiri + taban getiri pkl'lerinden, pandas merge) 4 satırda n, R15 ort, TOPLAM FARK, +2ATR payı, yukarı çıkış payı, yukarı DEVAM, büyüklük KAT birebir: ABD 16-19 k=2 (n 31.114; TF -0,068%; KAT 1,020), ABD 20-22 k=3 (n 3.651; TF +0,382%; yukarı %52,5), AVR 16-19 k=2 (n 6.027; TF -0,099%), ABD 16-19 k=4+ (n 844; TF +0,939%; KAT 1,113).
- Ham bar deposundan (npz) 5 rastgele olayda R15 = C[t+15] / O[t+1] - 1 ve giriş tarihi birebir.
- 300 rastgele k >= 2 olayında doji kuralı (gövde <= 0,10 boy, boy >= 0,5 x önceki 10 bar medyanı) ve önceki dojinin <= 3 bar önce olması bağımsız kodla: 0 aykırı.

## HATA

- HATA (kod, ön kayıttan önce bulundu): dj_olc_kol her pazarda dört hücreyi de dolduruyordu; birleştirmede AVR'nin boş ABD hücreleri ABD sonuçlarını eziyordu. Uçtan uca sentetik testte bulundu, pazar süzgeci + test eklendi; gerçek veride getiri hesaplanmadan önce.
- HATA (gösterim, ilk commit'ten önce bulundu): DJ_ORNEKLER.pdf'te öbeğin dojileri uygun olay tablosundan alındığı için 2016 öncesine düşen dojiler işaretlenmiyordu (4+ örneğinde 'Doji sayısı: 1'). PNG denetiminde görüldü; dojiler artık hissenin t'ye kadarki barlarıyla yeniden tespit ediliyor.
- NOT (veri bütünlüğü): olay pkl dosyalarının sha'sı yeniden üretimde bayt olarak farklı çıkıyor (pickle düzeni); içerik birebir aynı (AVR olay dosyası assert_frame_equal). Ön kayıttaki sha'lar bütünlük mührüdür; olay dosyaları ölçümde değişmedi (kapı denetledi).
- NOT: olay dosyaları, PDF / örnek ayarı (ESIK 'ornek') ve rapor kodu düzeltilmeden önceki kod sürümüyle üretildi; tespit / uygunluk kodu değişmedi, AVR yeniden üretimi içerik olarak aynı.

## SAPMA

- (yok) Ölçüm bir kez koştu; eşikler ve hüküm kuralları ön kayıttaki gibi. Rapor gösterim kodu ön kayıt sha'sıyla aynı (değişmedi).

## ÖNERİLEN DEFTER SATIRLARI

- IK_KAYIT Ç satırı: DOJI_OBEK (27 Kas): aynı seviyede (0,5 ATR), aralarında en çok 2 mum olan doji öbekleri; sıklık bin hisse-günde tek doji ~83-86, k=2 ~13-15, k=3 ~2-2,5, k=4+ ~0,2-0,4. Sonrası (R15, TOPLAM FARK aynı hissenin rastgele gününe göre): k=1/2/3 AYRIŞMIYOR (n >= 3.600, iki ABD dönemi), k=4+ ÖLÇÜLEMEDİ (n 844 / 532); hareket büyüklüğü, öbek bandından çıkış yönü, önceki yöne göre dönüş: AYRIŞMIYOR; çıkış sonrası 10 bar devamı yalnız pazarın sürüklenmesi kadar; DOZ - YANIT: ETKİSİZ; BH 32 satırda 0 geçen. Hüküm: DOJİ ÖBEĞİ SONRASI AYIRT EDİCİ DEĞİL (bu tanımla). Kasa açılmadı.
- IK_ILERI: k=4+ satırı ÖLÇÜLEMEDİ (ABD 16-19'da TF +0,94% [-0,18; 2,16], büyüklük KAT 1,11 [1,04; 1,19] tek dönem; ABD 20-22'de yok): kriz sonrası / 2023-24 verisi açıldığında aynı komut, aynı eşik; kasa kuralına göre tek başına açılmaz.
- IK_HATA: dj_olc_kol pazar birleştirme hatası (sentetik testte, ölçümden önce); PDF doji listesi hatası (PNG denetiminde).
