# K58 — cetvel sağlaması: RAPOR

Ön kayıt: 2026-11-10 19:19:52 UTC (mühür 5aec67198fe9, dosya sha256 234c3444b5bc); koşu 2026-11-10 19:22:05 UTC → 2026-11-10 19:46:07 UTC. K58 v1.0 (2026-11-10): cetvel sağlaması (FI_OLCUT gücü, French pozitif kontrol, portföy cetveli kalibrasyonu, C4 trend filtresi)

## Düz dille
Ölçüm aletimiz (FI_OLCUT olay cetveli), olaylara bilerek eklenen 60 günde +%2'lik gerçek bir üstünlüğü 30/100/300/1000/3000 olayda sırasıyla %4 / %8 / %11 / %13 / %21 olasılıkla görüyor (+%4 için %12 / %28 / %45 / %74 / %86); üstünlük yokken yanlış alarm en çok %1,5. Gerçek İZ dört hücre birden ister, olasılık yaklaşık bu sayıların dördüncü kuvvetidir. Yani alet küçük ama gerçek etkileri büyük ölçüde KAÇIRIYOR: 'iz yok' sonuçlarının bir kısmı piyasadan değil aletten. Bilinen faktörlerden (French, 2000-2026) portföy cetvelinden geçenler: MKT_RF, RMW; yani bu cetvel de yalnız güçlü etkileri görür. Önerilen portföy cetveli ABD'de 12-1 momentumu kabul etti (maliyetli yıllık fazla +%8,5, NW t 2,10); rastgele sinyallerin yanlış geçme oranı maliyetli %0,0, maliyetsiz %0,0. Bu yüzden cetvel 'kalibre aday standart'; benimsemek Cemal'in kararı. BIST'te momentum geçmedi (bilgi). SMA200 trend filtresi (endeks): SPY: filtre yıllık +%5,7 / al-tut +%8,3, en büyük düşüş -%28,8 / -%55,2 -> TUTMAZ; XU100.IS: filtre yıllık +%15,1 / al-tut +%25,9, en büyük düşüş -%73,4 / -%63,4 -> TUTMAZ. Hisse düzeyinde 'SMA200 üstü' ve 'SMA atılımı' portföyleri: ABD C4b1_sma200_ustu tutmaz; ABD C4b2_atilim tutmaz; BIST C4b1_sma200_ustu tutmaz; BIST C4b2_atilim tutmaz.

## Özet (D kuralları, ön kayıttan)
- A (FI_OLCUT gücü): küçük etkiyi GÖREMİYOR (D1 bulgusu); δ 0 yanlış pozitif en çok %1,5.
- C (portföy cetveli): KALİBRE ADAY (ABD karar; BIST bilgi).
- C4a: SPY TUTMAZ; XU100.IS TUTMAZ.
- C4b: ABD C4b1_sma200_ustu tutmaz; ABD C4b2_atilim tutmaz; BIST C4b1_sma200_ustu tutmaz; BIST C4b2_atilim tutmaz.

## A. FI_OLCUT gücü (V_ABD, plasebo olay + bilinen δ, 200 tekrar)
Güç = hücrenin dört şartla TUTTUĞU tekrar payı (δ 0 = yanlış pozitif).

| n | δ +%0 | δ +%1 | δ +%2 | δ +%4 | δ +%8 | δ +%16 | aralık yarı genişliği (δ 0) | ay |
|---|---|---|---|---|---|---|---|---|
| 30 | %1 | %4 | %4 | %12 | %46 | %92 | %10,6 | 27 |
| 100 | %2 | %4 | %8 | %28 | %80 | %96 | %6,7 | 68 |
| 300 | %0 | %3 | %11 | %45 | %96 | %100 | %3,9 | 113 |
| 1000 | %0 | %2 | %13 | %74 | %100 | %100 | %3,2 | 126 |
| 3000 | %0 | %2 | %21 | %86 | %100 | %100 | %2,0 | 126 |

Şart başına geçme payı (seçili δ):

| n | δ | aralık şartı | sıra şartı | portföy şartı | güç | dört hücre ≈ güç^4 |
|---|---|---|---|---|---|---|
| 30 | +%0 | %2 | %55 | %12 | %1 | %0,0 |
| 30 | +%2 | %4 | %81 | %22 | %4 | %0,0 |
| 30 | +%4 | %12 | %96 | %31 | %12 | %0,0 |
| 100 | +%0 | %2 | %56 | %12 | %2 | %0,0 |
| 100 | +%2 | %8 | %90 | %28 | %8 | %0,0 |
| 100 | +%4 | %30 | %99 | %50 | %28 | %0,6 |
| 300 | +%0 | %0 | %45 | %14 | %0 | %0,0 |
| 300 | +%2 | %12 | %100 | %38 | %11 | %0,0 |
| 300 | +%4 | %50 | %100 | %74 | %45 | %4,1 |
| 1000 | +%0 | %0 | %48 | %9 | %0 | %0,0 |
| 1000 | +%2 | %27 | %100 | %35 | %13 | %0,0 |
| 1000 | +%4 | %84 | %100 | %86 | %74 | %29,2 |
| 3000 | +%0 | %0 | %52 | %12 | %0 | %0,0 |
| 3000 | +%2 | %54 | %100 | %36 | %21 | %0,2 |
| 3000 | +%4 | %98 | %100 | %86 | %86 | %53,4 |

D1: δ +%2, n <= 300 en yüksek güç %11,0 -> BULGU: 'FI_OLCUT küçük etkiyi göremiyor'.

## B. Pozitif kontrol: French faktörleri (uzun-kısa, hayatta kalma yanlılığı yok)
Veri ayları: 1963-07 .. 2026-09.

| Faktör | Dönem | Ay | Aylık ort. | Yıllık | t | NW t | Sharpe |
|---|---|---|---|---|---|---|---|
| MKT_RF | 1963-2026 | 759 | +%0,60 | +%7,2 | 3,71 | 3,63 | 0,47 |
| MKT_RF | 2000-2026 | 321 | +%0,62 | +%7,5 | 2,48 | 2,40 | 0,48 |
| MKT_RF | 2000-09 | 120 | -%0,14 | -%1,7 | -0,32 | -0,27 | -0,10 |
| MKT_RF | 2010-19 | 120 | +%1,10 | +%13,1 | 3,21 | 4,33 | 1,01 |
| MKT_RF | 2020-26 | 81 | +%1,06 | +%12,8 | 1,91 | 2,32 | 0,73 |
| SMB | 1963-2026 | 759 | +%0,18 | +%2,2 | 1,64 | 1,55 | 0,21 |
| SMB | 2000-2026 | 321 | +%0,16 | +%1,9 | 0,93 | 1,04 | 0,18 |
| SMB | 2000-09 | 120 | +%0,59 | +%7,1 | 1,76 | 2,38 | 0,56 |
| SMB | 2010-19 | 120 | -%0,03 | -%0,4 | -0,14 | -0,16 | -0,05 |
| SMB | 2020-26 | 81 | -%0,19 | -%2,2 | -0,52 | -0,50 | -0,20 |
| HML | 1963-2026 | 759 | +%0,29 | +%3,5 | 2,71 | 2,27 | 0,34 |
| HML | 2000-2026 | 321 | +%0,21 | +%2,6 | 1,11 | 0,94 | 0,21 |
| HML | 2000-09 | 120 | +%0,66 | +%7,9 | 1,97 | 1,74 | 0,62 |
| HML | 2010-19 | 120 | -%0,20 | -%2,3 | -0,94 | -0,92 | -0,30 |
| HML | 2020-26 | 81 | +%0,15 | +%1,8 | 0,32 | 0,26 | 0,12 |
| RMW | 1963-2026 | 759 | +%0,25 | +%3,0 | 2,97 | 2,73 | 0,37 |
| RMW | 2000-2026 | 321 | +%0,35 | +%4,2 | 2,09 | 2,11 | 0,40 |
| RMW | 2000-09 | 120 | +%0,69 | +%8,3 | 1,95 | 1,98 | 0,62 |
| RMW | 2010-19 | 120 | +%0,11 | +%1,4 | 0,83 | 0,87 | 0,26 |
| RMW | 2020-26 | 81 | +%0,19 | +%2,2 | 0,54 | 0,60 | 0,21 |
| CMA | 1963-2026 | 759 | +%0,24 | +%2,9 | 3,25 | 2,86 | 0,41 |
| CMA | 2000-2026 | 321 | +%0,22 | +%2,7 | 1,81 | 1,55 | 0,35 |
| CMA | 2000-09 | 120 | +%0,55 | +%6,6 | 2,55 | 2,11 | 0,81 |
| CMA | 2010-19 | 120 | +%0,02 | +%0,2 | 0,12 | 0,11 | 0,04 |
| CMA | 2020-26 | 81 | +%0,05 | +%0,6 | 0,15 | 0,14 | 0,06 |
| UMD | 1963-2026 | 759 | +%0,60 | +%7,3 | 3,96 | 3,94 | 0,50 |
| UMD | 2000-2026 | 321 | +%0,21 | +%2,5 | 0,73 | 0,76 | 0,14 |
| UMD | 2000-09 | 120 | +%0,08 | +%1,0 | 0,13 | 0,13 | 0,04 |
| UMD | 2010-19 | 120 | +%0,27 | +%3,2 | 0,92 | 1,09 | 0,29 |
| UMD | 2020-26 | 81 | +%0,31 | +%3,7 | 0,62 | 0,74 | 0,24 |

Bilgi (karar rolü yok): portföy cetveli şartları uzun-kısa faktörlere, 2000-2026:

| Faktör | Alt dönem > 0 (3) | Cetvel C 2000-2026: yıllık | NW t | alt dönem | son %30 | TUTAR |
|---|---|---|---|---|---|---|
| MKT_RF | 2 | +%7,5 | 2,40 | evet | evet | TUTAR |
| SMB | 1 | +%1,9 | 1,04 | evet | hayır | tutmaz |
| HML | 2 | +%2,6 | 0,94 | hayır | evet | tutmaz |
| RMW | 3 | +%4,2 | 2,11 | evet | evet | TUTAR |
| CMA | 3 | +%2,7 | 1,55 | evet | evet | tutmaz |
| UMD | 3 | +%2,5 | 0,76 | evet | evet | tutmaz |

## C. Portföy cetveli (aylık, uzun-yalnız, eşit ağırlıklı evrene karşı; V_ABD hayatta kalanlar)
| Pazar | Sinyal | Ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Portföy yıllık | Kıyas yıllık | Sharpe | Devir | Brüt fazla | TUTAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | C1_momentum_12_1 | 122 | +%8,5 | 2,10 | +%0,81 / +%0,56 / +%0,75 | +%0,81 | +%32,5 | +%23,4 | 1,11 | %60 | +%9,2 | TUTAR |
| ABD | C4b1_sma200_ustu | 122 | -%3,9 | -1,16 | -%0,16 / -%0,68 / -%0,13 | -%0,04 | +%20,2 | +%23,4 | 1,09 | %46 | -%3,3 | tutmaz |
| ABD | C4b2_atilim | 122 | -%6,8 | -1,95 | -%0,26 / -%1,23 / -%0,19 | -%0,09 | +%17,0 | +%23,4 | 0,99 | %147 | -%5,0 | tutmaz |
| BIST | C1_momentum_12_1 | 122 | -%4,5 | -0,83 | -%0,11 / -%0,86 / -%0,15 | -%0,00 | +%52,5 | +%60,4 | 1,42 | %60 | -%2,2 | tutmaz |
| BIST | C4b1_sma200_ustu | 122 | +%1,4 | 0,89 | -%0,15 / +%0,33 / +%0,17 | +%0,20 | +%62,3 | +%60,4 | 1,66 | %49 | +%3,3 | tutmaz |
| BIST | C4b2_atilim | 122 | +%0,6 | 0,18 | -%0,14 / +%0,30 / -%0,01 | +%0,04 | +%60,2 | +%60,4 | 1,55 | %154 | +%6,4 | tutmaz |

C2 plasebo ve D2:
- ABD: 200 rastgele sinyal, yanlış pozitif maliyetli %0,0, brüt %0,0; C1 TUTAR -> KALİBRE ADAY
- BIST: 200 rastgele sinyal, yanlış pozitif maliyetli %0,0, brüt %3,0; C1 tutmaz -> aday değil
D2 (karar pazarı ABD): KALİBRE ADAY STANDART (benimseme Cemal kararı).

C4b eşli plasebo (bilgi):
- ABD C4b1_sma200_ustu: ortalama 673 hisse; NW t eşli plasebonun %40'ından büyük
- ABD C4b2_atilim: ortalama 319 hisse; NW t eşli plasebonun %22'ından büyük
- BIST C4b1_sma200_ustu: ortalama 255 hisse; NW t eşli plasebonun %100'ından büyük
- BIST C4b2_atilim: ortalama 105 hisse; NW t eşli plasebonun %100'ından büyük

## C4a. Endeks trend filtresi (kapanış > SMA200 elde, değilse nakit; ertesi açılışta işlem)
| Endeks | Dönem | Gün | Elde payı | İşlem | Filtre yıllık | Al-tut yıllık | Filtre MDD | Al-tut MDD | Filtre Sharpe | Al-tut Sharpe | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SPY | tam (2000-01-01) | 6705 | %74 | 184 | +%5,7 | +%8,3 | -%28,8 | -%55,2 | 0,54 | 0,51 | TUTMAZ |
| SPY | 2000-09 (2000-01-01) | 2515 | %58 | 94 | +%1,2 | -%1,0 | -%28,8 | -%55,2 | 0,16 | 0,07 |  |
| SPY | 2010-19 (2010-01-01) | 2516 | %87 | 54 | +%6,8 | +%13,5 | -%24,9 | -%19,3 | 0,63 | 0,93 |  |
| SPY | 2020-26 (2020-01-01) | 1674 | %80 | 36 | +%11,0 | +%15,6 | -%20,4 | -%33,7 | 0,89 | 0,82 |  |
| XU100.IS | tam (1999-01-01) | 6904 | %69 | 215 | +%15,1 | +%25,9 | -%73,4 | -%63,4 | 0,69 | 0,87 | TUTMAZ |
| XU100.IS | 2000-09 (2000-01-01) | 2495 | %62 | 76 | +%5,6 | +%13,4 | -%73,4 | -%63,4 | 0,33 | 0,51 |  |
| XU100.IS | 2010-19 (2010-01-01) | 2511 | %63 | 96 | -%0,7 | +%8,1 | -%55,2 | -%34,3 | 0,04 | 0,46 |  |
| XU100.IS | 2020-26 (2020-01-01) | 1662 | %85 | 42 | +%33,1 | +%46,7 | -%35,8 | -%31,8 | 1,24 | 1,52 |  |

Veri notları: temettü düzeltmeli (adjclose).

## Sınırlar
- A'daki plasebo olaylar on yıla yayılır; gerçek karar hücresi (bir-üç yıl) daha az ay içerir, aralığı daha geniştir: buradaki güç üst sınırdır.
- V_ABD yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı); French verisi bunun yanlılıksız kontrolüdür.
- C4a nakit getirisi 0 (faiz yok; filtre aleyhine). XU100 fiyat endeksidir (temettüsüz), TL bazında.
- Tutan C4 sonucu İZ değildir; CLAUDE.md test standardı (FI_OLCUT, ABD + AVR) değişmedikçe 'cetvel C altında tutar' diye okunur.

## IZ_KARNE önerisi (Ç151; IZ_KARNE.py'ye ana oturum işler)
```
_ik_k("Ç151", "2026-11-10", "K58 CETVEL SAĞLAMASI: FI_OLCUT gücü (plasebo olay + bilinen δ), French faktörleri pozitif kontrol, portföy cetveli (aylık üst %10) kalibrasyonu, SMA200 trend filtresi (endeks ve hisse)", "K58.py, test_k58.py", "İz bulamamamızın nedeni piyasa mı, ölçüm aletimiz mi?", "Ön kayıt K58_ON_KAYIT.md (sha 5aec67198fe9, git 657c2a1, ölçümden önce); FI_OLCUT değişmedi; portföy cetveli yalnız aday", "", 0, cikti="arastirma_cikti/k58_cetvel_sagla/ (K58_ON_KAYIT.md, K58_RAPOR.md, A_guc.csv, B_french.csv, C_portfoy.csv, C_plasebo.csv, C4a_endeks.csv)", notu="A güç (δ +%2, n 30/100/300/1000/3000): %4/%8/%11/%13/%21, δ 0 yanlış pozitif en çok %1,5; D1 BULGU: FI_OLCUT küçük etkiyi göremiyor; C portföy cetveli: ABD C1 momentum TUTAR, plasebo yanlış pozitif %0,0 (brüt %0,0); D2 KALİBRE ADAY STANDART (benimseme Cemal kararı); BIST C1 tutmaz; C4a SMA200 endeks filtresi: SPY TUTMAZ, XU100.IS TUTMAZ; C4b: ABD C4b1_sma200_ustu tutmaz, ABD C4b2_atilim tutmaz, BIST C4b1_sma200_ustu tutmaz, BIST C4b2_atilim tutmaz. İz iddiası yok (ölçüm aleti sağlaması); seviye 0."),
```
