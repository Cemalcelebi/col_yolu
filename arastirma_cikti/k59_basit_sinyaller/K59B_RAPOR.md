# K59-B — K59 §6'daki üç deneme (küçük-orta, 3 ay tutma, French): RAPOR

Ön kayıt: 2026-11-11 10:44:08 UTC (K59-B mührü 54591b5ffdcd, dosya sha256 36b540f0a401, git 5b3475a0b5; K59 mührü 6fe8bb385667 değişmedi); koşu 2026-11-11 10:47:02 UTC → 2026-11-11 10:51:45 UTC. K59-B v1.0 (2026-11-11): K59 §6'daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; sinyaller ve cetvel v2 K59 ile aynı

## Düz dille
Tasarım (a) yalnız küçük-orta hisselerde: cetvel güvenilir (200 rastgele sinyalden maliyetli %0,0, maliyetsiz %1,0 'tutar' çıktı; eşik %5). COMP4 U1'de maliyetten sonra kıyasa göre yıllık -%2,5 (NW t -0,55, alfa t 0,09; 66 ay): TUTMAZ (sağlanmayan şart: fazla NW t, alt dönem, son %30, alfa). COMP4 U2'de maliyetten sonra kıyasa göre yıllık +%7,0 (NW t 2,39, alfa t 3,09; 66 ay): TUTAR (yineleme). Tasarım (a) COMP4 sonucu: TUTMAZ (U1 TUTMAZ, U2 TUTAR (yineleme)). Tasarım (b) 3 ay tutmalı örtüşen portföylerde: cetvel GÜVENİLMEZ; bu tasarımda hüküm verilmedi. KARAR: TUTMAZ. Öteki üç sinyalden (bilgi; seçim yapılmaz) tasarım düzeyinde tutan: hiçbiri. French tarihi (VW_MKT; bilgi): bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü. French tarihi (EW_EW10; bilgi): bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf.

## Karar (ön kayıt §5-§6)
- KARAR (COMP4): TUTMAZ.
- Tasarım (a): cetvel GÜVENİLİR; COMP4 TUTMAZ (U1 TUTMAZ, U2 TUTAR (yineleme)).
- Tasarım (b): cetvel GÜVENİLMEZ; COMP4 HÜKÜM YOK (cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde).
- (c) French okuması (bilgi): VW_MKT: bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü; EW_EW10: bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf.
- İZ ilan edilemez (CLAUDE.md standardı değişmedi). K59-B PORTFÖY-ADAY öneri kapısı sayılmaz; K60 doğrulaması gerekir.
- Sonraki adım (sonuçtan bağımsız, ön kayıt §9): K60 (uzun tarih, batanlar dahil evren, sinyal kütüphanesinin tamamı); bu dokuz sinyalin 2021-26 örnekleminde başka çeşitlemesi denenmez.

Cetvel v2 şartları (maliyetten sonra; K59 ile aynı): ortalama fazla > 0 ve NW t > 2.0; 3 alt dönemin en az 2'sinde > 0; son %30 ayda > 0;
alfa > 0 ve NW t(alfa) > 2.0. Tasarım düzeyi 'TUTAR' = iki evrende de cetvel v2 + net yıllık fazla >= +4 puan; 'GÜÇLÜ' = iki evrende iki t de > 2.75 (8 deneme).

| Tasarım | Sinyal | Rol | U1 | U2 | Tasarım düzeyi |
|---|---|---|---|---|---|
| (a) | COMP4 | BİRİNCİL | TUTMAZ | TUTAR (yineleme) | TUTMAZ (U1 TUTMAZ, U2 TUTAR (yineleme)) |
| (a) | DOSYA_Y | bilgi | TUTMAZ | TUTMAZ | TUTMAZ (U1 TUTMAZ, U2 TUTMAZ) |
| (a) | S5 | bilgi | TUTMAZ | TUTMAZ | TUTMAZ (U1 TUTMAZ, U2 TUTMAZ) |
| (a) | S1 | bilgi | TUTAR (yineleme) | TUTMAZ | TUTMAZ (U1 TUTAR (yineleme), U2 TUTMAZ) |
| (b) | COMP4 | BİRİNCİL | HÜKÜM YOK | HÜKÜM YOK | HÜKÜM YOK (cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde) |
| (b) | DOSYA_Y | bilgi | HÜKÜM YOK | HÜKÜM YOK | HÜKÜM YOK (cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde) |
| (b) | S5 | bilgi | HÜKÜM YOK | HÜKÜM YOK | HÜKÜM YOK (cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde) |
| (b) | S1 | bilgi | HÜKÜM YOK | HÜKÜM YOK | HÜKÜM YOK (cetvel bu tasarımda güvenilmez: plasebo yanlış pozitif oranı eşiğin üstünde) |

## Tasarım (a): yalnız küçük-orta hisseler (her ay boyut medyanının altı); kıyas = alt evrenin eşit ağırlıklısı
Cetvel: GÜVENİLİR (plasebo yanlış pozitif maliyetli %0,0, maliyetsiz %1,0; eşik %5).

### (a) U1 — alt evren 123 ay, ortalama 542 hisse (tam uygun evren 1084); boyut ölçüsü (ay sayısı): {'islem_degeri': 123}

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 66 | 2021-02-26 | -%2,5 | -0,55 | +%0,97 / -%0,56 / -%1,03 | -%1,11 | +%0,3 | 0,09 | 0,83 | -%0,6 | -0,23 | 0,51 | -%24,6 | %79 | 50 | -%1,5 | -0,33 | 0,37 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 63 | 2021-05-28 | -%0,7 | -0,16 | +%0,01 / +%0,69 / -%0,87 | -%0,82 | +%0,1 | 0,01 | 0,95 | +%5,1 | 1,24 | 0,51 | -%29,1 | %79 | 39 | +%0,3 | 0,06 | 0,25 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 66 | 2021-02-26 | -%4,7 | -1,09 | +%0,53 / -%0,78 / -%0,91 | -%1,04 | -%2,5 | -0,73 | 0,87 | -%2,3 | -0,81 | 0,41 | -%29,6 | %47 | 44 | -%4,1 | -0,95 | -0,56 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S1 momentum 12-1 | 122 | 2016-06-30 | +%12,0 | 2,54 | +%0,78 / +%1,76 / +%0,44 | +%0,55 | +%9,3 | 2,13 | 1,13 | +%13,5 | 3,76 | 0,98 | -%29,4 | %72 | 54 | +%12,9 | 2,73 | 2,33 | TUTAR (yineleme) |

### (a) U2 — alt evren 68 ay, ortalama 958 hisse (tam uygun evren 2146); boyut ölçüsü (ay sayısı): {'piyasa_degeri': 65, 'islem_degeri': 3}

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 66 | 2021-02-26 | +%7,0 | 2,39 | +%1,25 / +%0,35 / +%0,14 | +%0,07 | +%7,5 | 3,09 | 0,86 | -%1,1 | -0,34 | 0,34 | -%29,0 | %76 | 88 | +%7,9 | 2,71 | 3,48 | TUTAR (yineleme) |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 63 | 2021-05-28 | +%5,8 | 1,73 | +%0,79 / +%0,92 / -%0,25 | -%0,46 | +%6,0 | 1,90 | 0,95 | -%1,0 | -0,26 | 0,23 | -%31,8 | %72 | 78 | +%6,7 | 1,99 | 2,17 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 66 | 2021-02-26 | +%4,0 | 1,14 | +%0,81 / -%0,05 / +%0,23 | +%0,19 | +%4,5 | 1,42 | 0,87 | -%2,6 | -0,62 | 0,21 | -%32,7 | %41 | 80 | +%4,5 | 1,28 | 1,58 | TUTMAZ (tutmayan: fazla NW t, alfa) |
| S1 momentum 12-1 | 67 | 2021-01-29 | -%6,3 | -1,15 | -%0,55 / -%0,74 / -%0,29 | -%0,48 | -%6,9 | -1,22 | 1,10 | -%9,2 | -1,43 | -0,13 | -%50,4 | %79 | 96 | -%5,4 | -0,98 | -1,06 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |

## Tasarım (b): 3 ay tutma, örtüşen üç aylık kohort; kıyas = tam uygun evrenin eşit ağırlıklısı
Cetvel: GÜVENİLMEZ (plasebo yanlış pozitif maliyetli %1,5, maliyetsiz %13,5; eşik %5).

### (b) U1 — tam uygun evren ortalama 1084 hisse; 'Hisse' = üç kohortta tutulan farklı hisse sayısı, 'Devir' = portföyün tamamına oranla aylık

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 64 | 2021-04-30 | -%1,2 | -0,37 | +%0,18 / -%0,02 / -%0,47 | -%0,39 | +%0,3 | 0,12 | 0,89 | -%1,6 | -0,69 | 0,45 | -%23,8 | %42 | 161 | -%0,7 | -0,21 | 0,31 | HÜKÜM YOK |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 62 | 2021-06-30 | +%1,1 | 0,34 | +%0,52 / +%0,25 / -%0,52 | -%0,65 | +%1,2 | 0,40 | 0,99 | +%0,6 | 0,22 | 0,51 | -%25,8 | %48 | 136 | +%1,7 | 0,52 | 0,59 | HÜKÜM YOK |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 64 | 2021-04-30 | -%2,6 | -0,94 | +%0,29 / -%0,36 / -%0,59 | -%0,65 | -%0,3 | -0,15 | 0,83 | -%2,1 | -1,07 | 0,41 | -%25,8 | %15 | 103 | -%2,4 | -0,87 | -0,06 | HÜKÜM YOK |
| S1 momentum 12-1 | 120 | 2016-08-31 | +%10,3 | 2,83 | +%0,48 / +%1,22 / +%0,88 | +%0,98 | +%7,9 | 2,17 | 1,14 | +%9,3 | 2,81 | 0,88 | -%24,4 | %33 | 159 | +%10,7 | 2,94 | 2,28 | HÜKÜM YOK |

### (b) U2 — tam uygun evren ortalama 2146 hisse; 'Hisse' = üç kohortta tutulan farklı hisse sayısı, 'Devir' = portföyün tamamına oranla aylık

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 64 | 2021-04-30 | +%5,8 | 2,50 | +%0,48 / +%0,84 / +%0,11 | +%0,23 | +%6,1 | 2,88 | 0,93 | -%1,3 | -0,62 | 0,41 | -%26,2 | %42 | 295 | +%6,3 | 2,73 | 3,12 | HÜKÜM YOK |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 62 | 2021-06-30 | +%6,1 | 2,84 | +%0,72 / +%0,58 / +%0,21 | +%0,08 | +%6,2 | 2,90 | 0,99 | -%0,7 | -0,32 | 0,39 | -%27,0 | %47 | 267 | +%6,7 | 3,11 | 3,16 | HÜKÜM YOK |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 64 | 2021-04-30 | +%4,7 | 2,15 | +%0,64 / +%0,40 / +%0,12 | +%0,13 | +%5,3 | 2,86 | 0,88 | -%1,5 | -0,71 | 0,39 | -%27,1 | %16 | 197 | +%4,8 | 2,23 | 2,96 | HÜKÜM YOK |
| S1 momentum 12-1 | 65 | 2021-03-31 | +%0,6 | 0,15 | -%0,55 / +%0,56 / +%0,16 | +%0,29 | -%0,7 | -0,16 | 1,22 | -%4,9 | -1,15 | 0,13 | -%38,5 | %35 | 323 | +%1,1 | 0,24 | -0,06 | HÜKÜM YOK |

## Tasarım (c): French kütüphanesinde momentum + kârlılık harmanı (bilgi; karara girmez)
Harman = 0.5 x momentum üst onluğu + 0.5 x faaliyet kârlılığı üst beşliği; net = brüt - %0.10 / ay (varsayım, üst sınır). VW_MKT: değer ağırlıklı harman - piyasa; EW_EW10: eşit ağırlıklı harman - on momentum onluğunun EW ortalaması; EW_MKT yalnız bilgi.

| Varyant | Dönem | Ay | Brüt yıllık fazla | Net yıllık fazla | NW t (net) | Alt 1/2/3 (net) | Son %30 (net) | Alfa (net, yıllık) | t(alfa) | Beta | Cetvel v2 net | Cetvel v2 brüt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| VW_MKT (ANA) | 1963-son (1963-07 .. 2026-09) | 759 | +%3,9 | +%2,7 | 3,42 | +%0,38 / +%0,22 / +%0,08 | +%0,09 | +%2,0 | 2,50 | 1,07 | TUTAR | TUTAR |
| VW_MKT (ANA) | 2000-son (2000-01 .. 2026-09) | 321 | +%2,2 | +%1,0 | 0,81 | +%0,14 / -%0,10 / +%0,21 | +%0,15 | +%1,0 | 0,80 | 1,01 | TUTMAZ | TUTMAZ |
| VW_MKT (ANA) | 2000-09 (2000-01 .. 2009-12) | 120 | +%1,6 | +%0,4 | 0,19 | +%0,16 / -%0,14 / +%0,09 | +%0,08 | +%0,5 | 0,23 | 0,91 | TUTMAZ | TUTMAZ |
| VW_MKT (ANA) | 2010-19 (2010-01 .. 2019-12) | 120 | +%1,6 | +%0,4 | 0,32 | -%0,01 / -%0,02 / +%0,12 | +%0,17 | -%1,0 | -0,85 | 1,10 | TUTMAZ | TUTMAZ |
| VW_MKT (ANA) | 2020-son (2020-01 .. 2026-09) | 81 | +%4,1 | +%2,9 | 0,85 | -%0,09 / +%0,54 / +%0,28 | +%0,38 | +%2,0 | 0,64 | 1,06 | TUTMAZ | TUTMAZ |
| EW_EW10 (ANA) | 1963-son (1963-07 .. 2026-09) | 759 | +%2,5 | +%1,3 | 1,92 | +%0,23 / +%0,19 / -%0,10 | -%0,13 | +%0,4 | 0,61 | 1,06 | TUTMAZ | TUTMAZ |
| EW_EW10 (ANA) | 2000-son (2000-01 .. 2026-09) | 321 | +%0,2 | -%1,0 | -1,04 | +%0,02 / -%0,29 / +%0,01 | -%0,04 | -%1,2 | -1,42 | 1,02 | TUTMAZ | TUTMAZ |
| EW_EW10 (ANA) | 2000-09 (2000-01 .. 2009-12) | 120 | -%0,4 | -%1,6 | -0,73 | +%0,04 / -%0,12 / -%0,32 | -%0,39 | -%1,3 | -0,69 | 0,98 | TUTMAZ | TUTMAZ |
| EW_EW10 (ANA) | 2010-19 (2010-01 .. 2019-12) | 120 | +%0,4 | -%0,8 | -0,88 | +%0,03 / -%0,24 / +%0,00 | +%0,08 | -%1,5 | -1,54 | 1,06 | TUTMAZ | TUTMAZ |
| EW_EW10 (ANA) | 2020-son (2020-01 .. 2026-09) | 81 | +%0,7 | -%0,5 | -0,29 | -%0,24 / +%0,34 / -%0,21 | -%0,27 | -%0,9 | -0,59 | 1,04 | TUTMAZ | TUTMAZ |
| EW_MKT (BİLGİ) | 1963-son (1963-07 .. 2026-09) | 759 | +%5,6 | +%4,4 | 2,76 | +%0,83 / +%0,42 / -%0,16 | -%0,17 | +%2,1 | 1,32 | 1,20 | TUTMAZ | TUTMAZ |
| EW_MKT (BİLGİ) | 2000-son (2000-01 .. 2026-09) | 321 | +%3,3 | +%2,1 | 0,99 | +%0,78 / +%0,03 / -%0,27 | -%0,35 | +%0,5 | 0,22 | 1,17 | TUTMAZ | TUTMAZ |
| EW_MKT (BİLGİ) | 2000-09 (2000-01 .. 2009-12) | 120 | +%10,5 | +%9,3 | 2,56 | +%1,66 / +%0,74 / -%0,07 | -%0,13 | +%9,2 | 2,60 | 1,15 | TUTMAZ | TUTMAZ |
| EW_MKT (BİLGİ) | 2010-19 (2010-01 .. 2019-12) | 120 | -%0,5 | -%1,7 | -0,77 | +%0,22 / -%0,28 / -%0,37 | -%0,44 | -%5,0 | -2,34 | 1,24 | TUTMAZ | TUTMAZ |
| EW_MKT (BİLGİ) | 2020-son (2020-01 .. 2026-09) | 81 | -%1,6 | -%2,8 | -0,59 | +%0,31 / -%0,55 / -%0,47 | -%0,66 | -%5,9 | -1,27 | 1,20 | TUTMAZ | TUTMAZ |

Önceden yazılı okuma (net seri): VW_MKT: bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü; EW_EW10: bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf.

## Plasebo (U2; tasarım başına rastgele sinyaller)
| Tasarım | Plasebo sayısı | Yanlış pozitif (maliyetli) | Yanlış pozitif (maliyetsiz) | Brüt NW t ortalaması | Brüt NW t en büyük | Brüt t(alfa) en büyük |
|---|---|---|---|---|---|---|
| (a) | 200 | %0,0 | %1,0 | -0,08 | 2,41 | 2,36 |
| (b) | 200 | %1,5 | %13,5 | 1,02 | 3,84 | 3,98 |

## Kapsam (hisse sayıları)
| Tasarım | Evren | Sinyal | İlk ay (>= eşik) | Beklenen ölçüm ayı | Ortalama sinyalli hisse |
|---|---|---|---|---|---|
| (a) | U1 | COMP4 | 2021-02-26 | 66 | 501 |
| (b) | U1 | COMP4 | 2021-02-26 | 64 | 1034 |
| (a) | U1 | DOSYA_Y | 2021-05-28 | 63 | 392 |
| (b) | U1 | DOSYA_Y | 2021-04-30 | 62 | 867 |
| (a) | U1 | S5 | 2021-02-26 | 66 | 445 |
| (b) | U1 | S5 | 2021-02-26 | 64 | 910 |
| (a) | U1 | S1 | 2016-06-30 | 122 | 543 |
| (b) | U1 | S1 | 2016-06-30 | 120 | 1087 |
| (a) | U2 | COMP4 | 2021-02-26 | 66 | 875 |
| (b) | U2 | COMP4 | 2021-02-26 | 64 | 1877 |
| (a) | U2 | DOSYA_Y | 2021-05-28 | 63 | 783 |
| (b) | U2 | DOSYA_Y | 2021-04-30 | 62 | 1710 |
| (a) | U2 | S5 | 2021-02-26 | 66 | 801 |
| (b) | U2 | S5 | 2021-02-26 | 64 | 1722 |
| (a) | U2 | S1 | 2021-01-29 | 67 | 958 |
| (b) | U2 | S1 | 2021-01-29 | 65 | 2150 |

## Koşu notları
- yok

## Sınırlar
- K59-B kör değildir: K59 sonucu görüldükten sonra, K59 ön kaydında önceden yazılı üç deneme koşuldu; ayrıntılar (BOŞLUK listesi) ölçümden önce yazıldı.
- Aynı 2021-2026 örnekleminde K59'un 12 denemesine 8 deneme eklendi; tutan sonuç 'ikinci tur adayı'dır.
- U1 ve U2 yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı) ve bağımsız değil. (a)'da kıyas alt evrendir; (b)'de kohortlar arası
  eşitleme maliyeti sayılmadı. (c) K59 COMP4'ün kendisi değil, iki hazır French portföyünün yarı yarıya harmanıdır; maliyet varsayımdır.
- Tutan sonuç İZ değildir.

## IZ_KARNE önerisi: kayıt metni (numarayı ve kaydı ana oturum işler)
```
_ik_k("Ç153", "2026-11-11", "K59-B: K59 §6daki önceden yazılı üç deneme: (a) yalnız küçük-orta hisseler, (b) 3 ay tutma + örtüşen üç kohort, (c) French kütüphanesinde momentum + kârlılık harmanı; COMP4, DOSYA_Y, S5, S1; cetvel v2 aynı", "K59.py, test_k59.py", "K59da tutmayan bileşik küçük-orta hisselerde ya da 3 ay tutmayla tutuyor mu; uzun tarihte (French) bu tür bileşik var mı?", "Ön kayıt K59B_ON_KAYIT.md (mühür 54591b5ffdcd; K59 mührü 6fe8bb385667 değişmedi; ölçümden önce git kaydına işlendi)", "", 0, cikti="arastirma_cikti/k59_basit_sinyaller/ (K59B_ON_KAYIT.md, K59B_RAPOR.md, k59b_sonuc.csv, k59b_aylik.csv, k59b_plasebo.csv, k59b_kapsam.csv, k59b_french.csv, k59b_french_aylik.csv)", notu="Karar: TUTMAZ; cetvel (a) GÜVENİLİR, (b) GÜVENİLMEZ; (a) U1 COMP4 yıllık fazla -%2,5, NW t -0,55, t(alfa) 0,09, TUTMAZ; (a) U2 COMP4 yıllık fazla +%7,0, NW t 2,39, t(alfa) 3,09, TUTAR (yineleme); (b) U1 COMP4 yıllık fazla -%1,2, NW t -0,37, t(alfa) 0,12, HÜKÜM YOK; (b) U2 COMP4 yıllık fazla +%5,8, NW t 2,50, t(alfa) 2,88, HÜKÜM YOK. French (c): VW_MKT: bileşik uzun dönemde tutmuyor (1963-son: TUTAR, 2000-son: TUTMAZ); 2020 sonrası güçlü; EW_EW10: bileşik uzun dönemde tutmuyor (1963-son: TUTMAZ, 2000-son: TUTMAZ); 2020 sonrası zayıf. İZ ilan edilemez; seviye 0. Sonraki: K60 (uzun tarih, batanlar dahil evren, sinyal kütüphanesinin tamamı); bu dokuz sinyalin 2021-26 örnekleminde başka çeşitlemesi denenmez."),
```
