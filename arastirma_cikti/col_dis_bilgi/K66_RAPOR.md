# K66 — ABD açığa satış talebi çöl sinyaline ek bilgi: RAPOR

K66 v1.0 (2026-11-12): ABD açığa satış talebi (FINRA açık pozisyon) çöl sinyaline ek bilgi; K64 tasarımı aynen, 4 değişken x 2 yön. Ön kayıt K66_ON_KAYIT.md (mühür 1d820a4e2638, dosya sha256 61d92443a7d1, git 89fb9f6); koşu 2026-11-12 04:43:01 UTC -> 2026-11-12 04:48:40 UTC (340 sn).

## Karar tablosu (ANA tanım K24; karar sırası çöl içi; yön = hangi üçte bir daha iyi)
| değişken | yön | karar | ABD | ek katkı (3 dönem) | BH (bağımsız) | işaret tutarlı | grubun dört şartı (brüt / net) |
|---|---|---|---|---|---|---|---|
| SI_PAY | ÜST | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | evet | hayır / hayır |
| SI_PAY | ALT | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |
| DTC | ÜST | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |
| DTC | ALT | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | evet | hayır / hayır |
| SI_DEG | ÜST | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |
| SI_DEG | ALT | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |
| SI_DEG1 | ÜST | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |
| SI_DEG1 | ALT | İZ DEĞİL | İZ DEĞİL | h/h/h | h/h | hayır | hayır / hayır |

BH ailesi m = 16 ölçülebilen hipotez; q = %10. 'İZ' bu işte verilemez (Avrupa açığa satış verisi yok).

## Temel model (yalnız çöl; değişkensiz)
| pazar | dönem | n | ort. r60 | medyan r60 | ort. r20 | ort. eşli fark [%95] | medyan eşli fark | sıra | dört şart |
|---|---|---|---|---|---|---|---|---|---|
| ABD | 2018-2021 | 2321 | %+10,4 | %+5,8 | %+3,1 | %-2,9 [%-9,5; %+0,7] | %-4,8 | 0.48 | tutmaz |
| ABD | 2022-2026 | 3508 | %+6,2 | %+1,0 | %+2,6 | %+0,2 [%-1,3; %+1,8] | %-4,5 | 0.49 | tutmaz |
| ABD | 2023-2026 | 2461 | %+10,5 | %+3,5 | %+3,4 | %+0,4 [%-1,4; %+2,7] | %-5,8 | 0.49 | tutmaz |

## SI_PAY
Tanım: SI(r0) x b(r0) / PAY(t): son bilinen rapor r0'ın açık pozisyonu (bugünkü pay birimine bölünme çarpanı b ile) / t günü bilinen toplam pay (K60.k60_pay, bugünkü birim). PAY > 0; oran > 2 ise veri hatası sayılır (yok). Beklenti: açığa satış oranı (yüksek = kötü haber beklentisi; Dechow vd. 2001, Asquith vd. 2005). Karar sırası: çöl içi (İÇ); öteki sıra sağlamlık.

| dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018-2021 | ÜST | 562 | %+12,5 | %+7,2 | %+3,7 | %+1,3 | %-2,4 [%-16,6; %+5,4] | %-4,5 | %+11,0 | %-2,6 | tutmaz / tutmaz |
| 2018-2021 | ALT | 612 | %+10,5 | %+6,3 | %+3,8 | %+2,4 | %-4,0 [%-10,9; %+3,0] | %-5,3 | %+7,0 | %-4,2 | tutmaz / tutmaz |
| 2022-2026 | ÜST | 1079 | %+8,4 | %+0,8 | %+2,9 | %+0,8 | %+2,0 [%-1,0; %+5,2] | %-5,2 | %+3,1 | %+1,8 | tutmaz / tutmaz |
| 2022-2026 | ALT | 944 | %+4,5 | %+1,2 | %+1,8 | %+0,8 | %-0,8 [%-3,4; %+2,2] | %-4,2 | %+2,8 | %-1,0 | tutmaz / tutmaz |
| 2023-2026 | ÜST | 822 | %+11,9 | %+2,1 | %+3,8 | %+0,6 | %+2,5 [%-1,1; %+6,7] | %-6,6 | %+3,9 | %+2,3 | tutmaz / tutmaz |
| 2023-2026 | ALT | 595 | %+9,8 | %+4,7 | %+2,5 | %+1,5 | %-0,4 [%-4,0; %+4,4] | %-6,1 | %+4,2 | %-0,6 | tutmaz / tutmaz |

| tanım | sıra | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |
|---|---|---|---|---|---|---|---|
| K24 | EVREN | 2018-2021 | 855 / 459 | %+2,6 [%-5,3; %+8,4] | %-2,9 | yok | %+1,1 |
| K24 | IC | 2018-2021 | 562 / 612 | %+1,6 [%-10,4; %+10,0] | %-2,9 | yok | %+1,6 |
| K24 | EVREN | 2022-2026 | 1448 / 618 | %+1,3 [%-3,2; %+5,0] | %+0,2 | yok | %+1,2 |
| K24 | IC | 2022-2026 | 1079 / 944 | %+2,7 [%-1,1; %+6,4] | %+0,2 | yok | %+1,3 |
| K24 | EVREN | 2023-2026 | 1081 / 393 | %+1,3 [%-5,4; %+6,6] | %+0,4 | yok | %+1,3 |
| K24 | IC | 2023-2026 | 822 / 595 | %+2,9 [%-2,7; %+7,9] | %+0,4 | yok | %+1,5 |
| D13 | EVREN | 2018-2021 | 399 / 273 | %-5,3 [%-12,0; %+0,2] | %-3,9 | yok | %-1,6 |
| D13 | IC | 2018-2021 | 341 / 309 | %-3,6 [%-9,8; %+1,6] | %-3,9 | yok | %-1,3 |
| D13 | EVREN | 2022-2026 | 665 / 496 | %-0,8 [%-3,8; %+2,2] | %-0,4 | yok | %-0,1 |
| D13 | IC | 2022-2026 | 612 / 531 | %-0,6 [%-3,6; %+2,5] | %-0,4 | yok | %-0,2 |
| D13 | EVREN | 2023-2026 | 489 / 340 | %-1,3 [%-5,3; %+2,8] | %-0,2 | yok | %-0,5 |
| D13 | IC | 2023-2026 | 459 / 361 | %-0,7 [%-4,6; %+3,4] | %-0,2 | yok | %-0,6 |

S2 (çöl dışı evren; bilgi): 2018-2021 ÜST - ALT %-0,1 [%-1,9; %+1,7] (n 135139 / 148414); 2022-2026 ÜST - ALT %-0,5 [%-1,8; %+0,8] (n 231798 / 266469); 2023-2026 ÜST - ALT %-0,2 [%-1,6; %+1,2] (n 188142 / 216636)

Piyasa koşulu (bilgi): 2018-2021 endeks ort. üstü ÜST n 384 eşli fark %-5,3; 2018-2021 endeks ort. üstü ALT n 306 eşli fark %-2,9; 2018-2021 endeks ort. altı ÜST n 178 eşli fark %+3,8; 2018-2021 endeks ort. altı ALT n 306 eşli fark %-5,2; 2022-2026 endeks ort. üstü ÜST n 718 eşli fark %+1,0; 2022-2026 endeks ort. üstü ALT n 478 eşli fark %-1,3; 2022-2026 endeks ort. altı ÜST n 361 eşli fark %+3,8; 2022-2026 endeks ort. altı ALT n 466 eşli fark %-0,2; 2023-2026 endeks ort. üstü ÜST n 709 eşli fark %+0,9; 2023-2026 endeks ort. üstü ALT n 471 eşli fark %-1,3; 2023-2026 endeks ort. altı ÜST n 113 eşli fark %+12,6; 2023-2026 endeks ort. altı ALT n 124 eşli fark %+3,1

## DTC
Tanım: SI(r0) / ADV(r0): r0 raporunun açık pozisyonu / aynı raporun ortalama günlük hacmi (FINRA 'days to cover' formülü; dosyadaki 1,00 tabanı ve yuvarlama uygulanmaz); ADV > 0. Beklenti: kapatma günü (Hong vd. 2016). Karar sırası: çöl içi (İÇ); öteki sıra sağlamlık.

| dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018-2021 | ÜST | 649 | %+10,7 | %+5,9 | %+3,2 | %+1,7 | %-5,5 [%-19,7; %+2,1] | %-4,4 | %+10,9 | %-5,7 | tutmaz / tutmaz |
| 2018-2021 | ALT | 688 | %+10,4 | %+6,7 | %+3,4 | %+1,8 | %-2,8 [%-6,6; %+0,9] | %-5,8 | %+3,8 | %-3,0 | tutmaz / tutmaz |
| 2022-2026 | ÜST | 1102 | %+9,0 | %+0,8 | %+3,0 | %+0,6 | %+0,7 [%-1,8; %+3,5] | %-6,4 | %+2,6 | %+0,5 | tutmaz / tutmaz |
| 2022-2026 | ALT | 1113 | %+5,6 | %+1,4 | %+2,6 | %+0,7 | %+0,9 [%-1,5; %+3,8] | %-2,8 | %+2,6 | %+0,7 | tutmaz / tutmaz |
| 2023-2026 | ÜST | 809 | %+12,6 | %+2,0 | %+3,9 | %+0,8 | %+0,8 [%-2,3; %+4,5] | %-7,9 | %+3,4 | %+0,6 | tutmaz / tutmaz |
| 2023-2026 | ALT | 766 | %+10,4 | %+4,8 | %+3,9 | %+1,5 | %+1,3 [%-2,0; %+4,9] | %-4,7 | %+3,4 | %+1,1 | tutmaz / tutmaz |

| tanım | sıra | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |
|---|---|---|---|---|---|---|---|
| K24 | EVREN | 2018-2021 | 668 / 725 | %-0,6 [%-12,6; %+5,9] | %-2,9 | yok | %+1,8 |
| K24 | IC | 2018-2021 | 649 / 688 | %-2,7 [%-16,7; %+5,2] | %-2,9 | yok | %+1,1 |
| K24 | EVREN | 2022-2026 | 1085 / 1257 | %+0,1 [%-2,9; %+3,3] | %+0,2 | yok | %-0,8 |
| K24 | IC | 2022-2026 | 1102 / 1113 | %-0,2 [%-3,4; %+2,8] | %+0,2 | yok | %-1,0 |
| K24 | EVREN | 2023-2026 | 785 / 887 | %-0,1 [%-4,1; %+4,4] | %+0,4 | yok | %-1,1 |
| K24 | IC | 2023-2026 | 809 / 766 | %-0,5 [%-4,4; %+3,6] | %+0,4 | yok | %-1,1 |
| D13 | EVREN | 2018-2021 | 430 / 318 | %-2,9 [%-10,0; %+3,6] | %-3,9 | yok | %+1,3 |
| D13 | IC | 2018-2021 | 359 / 346 | %-3,6 [%-10,9; %+2,0] | %-3,9 | yok | %+1,1 |
| D13 | EVREN | 2022-2026 | 664 / 597 | %-1,2 [%-4,8; %+2,5] | %-0,4 | yok | %-0,8 |
| D13 | IC | 2022-2026 | 609 / 626 | %-1,2 [%-4,8; %+2,7] | %-0,4 | yok | %-0,3 |
| D13 | EVREN | 2023-2026 | 490 / 428 | %-1,8 [%-6,5; %+3,7] | %-0,2 | yok | %-1,3 |
| D13 | IC | 2023-2026 | 462 / 425 | %-1,4 [%-6,2; %+4,2] | %-0,2 | yok | %-1,0 |

S2 (çöl dışı evren; bilgi): 2018-2021 ÜST - ALT %-2,5 [%-3,7; %-1,4] (n 156011 / 157958); 2022-2026 ÜST - ALT %-1,6 [%-2,5; %-0,6] (n 271010 / 278545); 2023-2026 ÜST - ALT %-1,5 [%-2,7; %-0,5] (n 220083 / 225973)

Piyasa koşulu (bilgi): 2018-2021 endeks ort. üstü ÜST n 445 eşli fark %-8,6; 2018-2021 endeks ort. üstü ALT n 360 eşli fark %-2,2; 2018-2021 endeks ort. altı ÜST n 204 eşli fark %+1,4; 2018-2021 endeks ort. altı ALT n 328 eşli fark %-3,4; 2022-2026 endeks ort. üstü ÜST n 694 eşli fark %-0,0; 2022-2026 endeks ort. üstü ALT n 643 eşli fark %-0,0; 2022-2026 endeks ort. altı ÜST n 408 eşli fark %+2,0; 2022-2026 endeks ort. altı ALT n 470 eşli fark %+2,2; 2023-2026 endeks ort. üstü ÜST n 681 eşli fark %-0,1; 2023-2026 endeks ort. üstü ALT n 635 eşli fark %+0,1; 2023-2026 endeks ort. altı ÜST n 128 eşli fark %+5,5; 2023-2026 endeks ort. altı ALT n 131 eşli fark %+7,0

## SI_DEG
Tanım: ln(SI(r0) x b(r0) / (SI(r0-6) x b(r0-6))): son bilinen rapor ile 6 rapor (~3 ay) önceki rapor; ikisi de > 0. Aradaki 6 raporun birinde FINRA bölünme bayrağı varken K60 bölünme kaydında o aralıkta bölünme yoksa (düzeltilemiyor) yok. Beklenti: açık pozisyon artışı (proje ölçüsü). Karar sırası: çöl içi (İÇ); öteki sıra sağlamlık.

| dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018-2021 | ÜST | 607 | %+9,7 | %+5,9 | %+2,8 | %+1,9 | %-2,8 [%-8,4; %+0,5] | %-4,5 | %+4,5 | %-3,0 | tutmaz / tutmaz |
| 2018-2021 | ALT | 688 | %+12,6 | %+7,1 | %+4,4 | %+2,2 | %-2,6 [%-11,6; %+1,8] | %-4,4 | %+6,7 | %-2,8 | tutmaz / tutmaz |
| 2022-2026 | ÜST | 1112 | %+6,3 | %+1,4 | %+2,8 | %+0,5 | %+0,4 [%-2,0; %+2,7] | %-4,3 | %+2,3 | %+0,2 | tutmaz / tutmaz |
| 2022-2026 | ALT | 1073 | %+6,5 | %+1,6 | %+2,7 | %+1,1 | %-0,1 [%-2,0; %+2,2] | %-4,6 | %+2,1 | %-0,3 | tutmaz / tutmaz |
| 2023-2026 | ÜST | 802 | %+11,5 | %+4,1 | %+3,3 | %+0,5 | %+0,8 [%-2,1; %+4,0] | %-5,7 | %+3,1 | %+0,6 | tutmaz / tutmaz |
| 2023-2026 | ALT | 755 | %+9,6 | %+5,1 | %+3,9 | %+2,2 | %-0,3 [%-2,9; %+2,7] | %-5,6 | %+2,8 | %-0,5 | tutmaz / tutmaz |

| tanım | sıra | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |
|---|---|---|---|---|---|---|---|
| K24 | EVREN | 2018-2021 | 770 / 587 | %+0,9 [%-2,3; %+4,8] | %-2,9 | yok | %-0,3 |
| K24 | IC | 2018-2021 | 607 / 688 | %-0,3 [%-3,5; %+5,5] | %-2,9 | yok | %-0,9 |
| K24 | EVREN | 2022-2026 | 1307 / 974 | %-0,3 [%-3,6; %+2,6] | %+0,2 | yok | %+0,2 |
| K24 | IC | 2022-2026 | 1112 / 1073 | %+0,4 [%-2,8; %+3,3] | %+0,2 | yok | %+0,4 |
| K24 | EVREN | 2023-2026 | 958 / 660 | %+0,5 [%-3,8; %+4,3] | %+0,4 | yok | %-0,2 |
| K24 | IC | 2023-2026 | 802 / 755 | %+1,1 [%-3,1; %+5,0] | %+0,4 | yok | %-0,3 |
| D13 | EVREN | 2018-2021 | 347 / 334 | %+6,3 [%+0,7; %+12,8] | %-3,9 | VAR (ÜST) | %+1,4 |
| D13 | IC | 2018-2021 | 347 / 332 | %+7,0 [%+0,8; %+13,9] | %-3,9 | VAR (ÜST) | %+1,4 |
| D13 | EVREN | 2022-2026 | 636 / 600 | %+2,6 [%-0,8; %+6,7] | %-0,4 | yok | %+1,5 |
| D13 | IC | 2022-2026 | 645 / 603 | %+2,8 [%-0,8; %+6,9] | %-0,4 | yok | %+1,1 |
| D13 | EVREN | 2023-2026 | 467 / 439 | %+2,8 [%-1,8; %+8,4] | %-0,2 | yok | %+1,7 |
| D13 | IC | 2023-2026 | 450 / 453 | %+3,4 [%-1,7; %+9,4] | %-0,2 | yok | %+1,8 |

S2 (çöl dışı evren; bilgi): 2018-2021 ÜST - ALT %+0,8 [%+0,0; %+1,8] (n 145349 / 151701); 2022-2026 ÜST - ALT %-0,0 [%-0,7; %+0,7] (n 266726 / 282350); 2023-2026 ÜST - ALT %+0,0 [%-0,9; %+0,9] (n 217075 / 229473)

Piyasa koşulu (bilgi): 2018-2021 endeks ort. üstü ÜST n 377 eşli fark %-3,6; 2018-2021 endeks ort. üstü ALT n 370 eşli fark %-4,6; 2018-2021 endeks ort. altı ÜST n 230 eşli fark %-1,6; 2018-2021 endeks ort. altı ALT n 318 eşli fark %-0,3; 2022-2026 endeks ort. üstü ÜST n 678 eşli fark %-0,9; 2022-2026 endeks ort. üstü ALT n 635 eşli fark %-0,7; 2022-2026 endeks ort. altı ÜST n 434 eşli fark %+2,4; 2022-2026 endeks ort. altı ALT n 438 eşli fark %+0,9; 2023-2026 endeks ort. üstü ÜST n 671 eşli fark %-0,9; 2023-2026 endeks ort. üstü ALT n 624 eşli fark %-0,8; 2023-2026 endeks ort. altı ÜST n 131 eşli fark %+9,4; 2023-2026 endeks ort. altı ALT n 131 eşli fark %+2,1

## SI_DEG1
Tanım: changePercent(r0) / 100: son raporun bir önceki rapora göre değişimi (dosyadaki alan); önceki pozisyon > 0; r0'da bölünme bayrağı ya da (r0-1, r0] aralığında bilinen bölünme varsa yok. Beklenti: kısa vade değişim (bilgi). Karar sırası: çöl içi (İÇ); öteki sıra sağlamlık.

| dönem | grup | n | ort. r60 | medyan r60 | ort. r20 | medyan r20 | ort. eşli fark [%95] | medyan eşli fark | yarı genişlik | net eşli fark | dört şart (brüt / net) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018-2021 | ÜST | 643 | %+8,9 | %+5,8 | %+2,7 | %+1,7 | %-2,1 [%-4,7; %+0,4] | %-6,4 | %+2,6 | %-2,3 | tutmaz / tutmaz |
| 2018-2021 | ALT | 695 | %+10,1 | %+6,0 | %+3,3 | %+2,2 | %-4,1 [%-12,6; %-0,2] | %-4,6 | %+6,2 | %-4,3 | tutmaz / tutmaz |
| 2022-2026 | ÜST | 1105 | %+4,5 | %+0,3 | %+2,1 | %+0,3 | %-1,4 [%-3,7; %+1,1] | %-4,8 | %+2,4 | %-1,6 | tutmaz / tutmaz |
| 2022-2026 | ALT | 1084 | %+7,7 | %+4,0 | %+3,0 | %+1,5 | %+1,3 [%-1,1; %+4,2] | %-3,6 | %+2,7 | %+1,1 | tutmaz / tutmaz |
| 2023-2026 | ÜST | 790 | %+8,5 | %+3,3 | %+3,1 | %+0,5 | %-0,9 [%-3,9; %+2,7] | %-6,0 | %+3,3 | %-1,1 | tutmaz / tutmaz |
| 2023-2026 | ALT | 758 | %+12,4 | %+6,2 | %+4,3 | %+2,2 | %+1,7 [%-1,4; %+5,9] | %-4,9 | %+3,7 | %+1,5 | tutmaz / tutmaz |

| tanım | sıra | dönem | n ÜST / ALT | ÜST - ALT [%95] | temel eşli fark | ek katkı | 20 gün ÜST - ALT |
|---|---|---|---|---|---|---|---|
| K24 | EVREN | 2018-2021 | 766 / 666 | %+1,6 [%-1,8; %+6,3] | %-2,9 | yok | %-0,0 |
| K24 | IC | 2018-2021 | 643 / 695 | %+2,0 [%-1,1; %+8,9] | %-2,9 | yok | %-0,1 |
| K24 | EVREN | 2022-2026 | 1262 / 1018 | %-2,1 [%-6,1; %+1,5] | %+0,2 | yok | %-0,2 |
| K24 | IC | 2022-2026 | 1105 / 1084 | %-2,6 [%-6,2; %+0,5] | %+0,2 | yok | %-0,5 |
| K24 | EVREN | 2023-2026 | 897 / 712 | %-2,4 [%-7,8; %+2,7] | %+0,4 | yok | %-0,0 |
| K24 | IC | 2023-2026 | 790 / 758 | %-2,6 [%-7,3; %+2,0] | %+0,4 | yok | %-0,4 |
| D13 | EVREN | 2018-2021 | 338 / 350 | %-0,0 [%-4,6; %+5,2] | %-3,9 | yok | %-0,3 |
| D13 | IC | 2018-2021 | 341 / 354 | %+0,1 [%-4,0; %+5,2] | %-3,9 | yok | %-0,6 |
| D13 | EVREN | 2022-2026 | 620 / 581 | %+1,3 [%-3,2; %+6,0] | %-0,4 | yok | %+0,1 |
| D13 | IC | 2022-2026 | 650 / 616 | %+0,7 [%-3,6; %+5,4] | %-0,4 | yok | %-0,4 |
| D13 | EVREN | 2023-2026 | 457 / 409 | %+0,9 [%-4,9; %+7,9] | %-0,2 | yok | %-0,2 |
| D13 | IC | 2023-2026 | 470 / 446 | %+0,3 [%-4,9; %+6,9] | %-0,2 | yok | %-0,7 |

S2 (çöl dışı evren; bilgi): 2018-2021 ÜST - ALT %+0,7 [%-0,1; %+1,6] (n 154951 / 158818); 2022-2026 ÜST - ALT %+0,3 [%-0,2; %+0,8] (n 273218 / 279523); 2023-2026 ÜST - ALT %+0,4 [%-0,2; %+0,9] (n 222221 / 226998)

Piyasa koşulu (bilgi): 2018-2021 endeks ort. üstü ÜST n 388 eşli fark %-2,4; 2018-2021 endeks ort. üstü ALT n 405 eşli fark %-5,8; 2018-2021 endeks ort. altı ÜST n 255 eşli fark %-1,7; 2018-2021 endeks ort. altı ALT n 290 eşli fark %-1,7; 2022-2026 endeks ort. üstü ÜST n 666 eşli fark %-1,2; 2022-2026 endeks ort. üstü ALT n 628 eşli fark %+1,9; 2022-2026 endeks ort. altı ÜST n 439 eşli fark %-1,6; 2022-2026 endeks ort. altı ALT n 456 eşli fark %+0,3; 2023-2026 endeks ort. üstü ÜST n 662 eşli fark %-1,2; 2023-2026 endeks ort. üstü ALT n 613 eşli fark %+1,7; 2023-2026 endeks ort. altı ÜST n 128 eşli fark %+0,3; 2023-2026 endeks ort. altı ALT n 145 eşli fark %+1,5

## Veri eksikleri ve sınırlar
BIST VERİSİ YOK (açığa satış yalnız BIST-30 / 50, açık pozisyon yayını yok). ÖDÜNÇ ÜCRETİ / KULLANILABİLİR ADET: VERİ YOK (ücretli). Pay toplam paydır (float değil). Bilgi tarihi tutucu: ödeme + 12 işlem günü. Evren yalnız yaşayanlar (ön kayıt §10). 'ÖLÇÜLEMEZ' = hücrede n < 30 (az veri), 'İZ DEĞİL' değildir. Ayrıntı: K66_ON_KAYIT.md §9-§11; koşu sayıları k66_meta.json.
