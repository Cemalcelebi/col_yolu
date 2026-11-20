# POZİTİF KONTROL — RAPOR (2026-11-20 21:36:15 UTC)

POZITIF_KONTROL v1.0 (2026-11-20): 15 bar cetveli pozitif kontrol (yapay iz, momentum 12-1, bilanço sonrası sürüklenme, örnekler). Ön kayıt POZITIF_KONTROL_ON_KAYIT.md (git 3b614aa78d95118adcc6f335e7916c77079f744d 2026-11-20T21:30:01+00:00); koşu 2026-11-20 21:30:06 UTC .. 2026-11-20 21:36:15 UTC (369.2 sn). Cetvel DS ile bayt bayt aynı (kod / eşik sha = DS_ON_KAYIT). h5 = 15 geçerli barda kapanışla +%5, stop'tan önce; FARK = olay h5 payı - eş h5 payı (yüzde puan). Komisyon yok. Evren bugün işlem gören hisseler (hayatta kalma).

## 1. A — YAPAY İZ: yakalama payı (20 tohum; yakalama = FARK > 0 VE boot %95 alt > 0 VE tek yönlü p < 0,05)

Sürüklenme delta: tutan olayın 15 barına doğrusal yayılmış fiyat artışı (15. barda +delta). Hücre başına: yakalama payı (iki yönlü p ile) / ortalama ölçülen n / ortalama FARK (puan).

**ABD egitim** (DS havuzu 12934 olay; DS h5 ortalaması %51.0)

| n | delta 0 (plasebo) | delta +%1 | delta +%2 | delta +%3 | delta +%5 |
|---|---|---|---|---|---|
| 30 | **%10** (%5) / 30 / +1,2 | **%10** (%10) / 30 / +2,8 | **%15** (%15) / 30 / +5,5 | **%15** (%15) / 30 / +7,0 | **%30** (%20) / 30 / +12,3 |
| 100 | **%0** (%0) / 100 / -0,3 | **%0** (%0) / 100 / +1,7 | **%10** (%10) / 100 / +4,1 | **%40** (%35) / 100 / +6,2 | **%65** (%65) / 100 / +10,4 |
| 300 | **%5** (%0) / 300 / +0,6 | **%15** (%15) / 300 / +2,8 | **%45** (%45) / 300 / +4,6 | **%70** (%65) / 300 / +6,5 | **%100** (%100) / 300 / +10,5 |
| 1000 | **%0** (%0) / 999 / +0,4 | **%55** (%50) / 999 / +2,3 | **%80** (%80) / 999 / +4,3 | **%95** (%95) / 999 / +6,2 | **%100** (%100) / 999 / +10,3 |
| yari | **%10** (%10) / 6429 / +0,5 | **%100** (%100) / 6429 / +2,3 | **%100** (%100) / 6429 / +4,4 | **%100** (%100) / 6429 / +6,3 | **%100** (%100) / 6429 / +10,5 |

**ABD sinama** (DS havuzu 9464 olay; DS h5 ortalaması %50.0)

| n | delta 0 (plasebo) | delta +%1 | delta +%2 | delta +%3 | delta +%5 |
|---|---|---|---|---|---|
| 30 | **%0** (%0) / 30 / -0,6 | **%5** (%0) / 30 / +1,9 | **%10** (%5) / 30 / +3,2 | **%10** (%10) / 30 / +5,4 | **%25** (%15) / 30 / +10,1 |
| 100 | **%5** (%5) / 100 / -0,2 | **%10** (%5) / 100 / +2,7 | **%30** (%20) / 100 / +4,8 | **%45** (%45) / 100 / +7,2 | **%70** (%55) / 100 / +11,4 |
| 300 | **%5** (%5) / 300 / +0,0 | **%30** (%30) / 300 / +3,2 | **%50** (%50) / 300 / +5,5 | **%75** (%75) / 300 / +7,9 | **%100** (%100) / 300 / +12,3 |
| 1000 | **%0** (%0) / 1000 / -0,1 | **%45** (%45) / 1000 / +2,6 | **%90** (%90) / 1000 / +4,9 | **%100** (%100) / 1000 / +7,3 | **%100** (%100) / 1000 / +12,0 |
| yari | **%0** (%0) / 4723 / +0,4 | **%100** (%100) / 4723 / +3,2 | **%100** (%100) / 4723 / +5,5 | **%100** (%100) / 4723 / +7,9 | **%100** (%100) / 4723 / +12,5 |

**AVR egitim** (DS havuzu 3389 olay; DS h5 ortalaması %48.7)

| n | delta 0 (plasebo) | delta +%1 | delta +%2 | delta +%3 | delta +%5 |
|---|---|---|---|---|---|
| 30 | **%10** (%10) / 30 / +0,4 | **%10** (%10) / 30 / +2,7 | **%10** (%10) / 30 / +5,4 | **%20** (%15) / 30 / +7,2 | **%40** (%25) / 30 / +12,2 |
| 100 | **%0** (%0) / 100 / -0,0 | **%0** (%0) / 100 / +2,2 | **%20** (%10) / 100 / +4,9 | **%40** (%30) / 100 / +6,6 | **%75** (%75) / 100 / +11,6 |
| 300 | **%0** (%0) / 299 / -0,6 | **%20** (%20) / 299 / +1,8 | **%50** (%50) / 299 / +4,3 | **%75** (%75) / 299 / +6,5 | **%100** (%100) / 299 / +11,4 |
| 1000 | **%0** (%0) / 991 / +0,0 | **%50** (%50) / 991 / +2,7 | **%100** (%100) / 991 / +5,0 | **%100** (%100) / 991 / +7,0 | **%100** (%100) / 991 / +11,8 |
| yari | **%0** (%0) / 1661 / -0,1 | **%80** (%75) / 1661 / +2,3 | **%100** (%100) / 1661 / +4,7 | **%100** (%100) / 1661 / +6,7 | **%100** (%100) / 1661 / +11,3 |

**AVR sinama** (DS havuzu 1206 olay; DS h5 ortalaması %45.5)

| n | delta 0 (plasebo) | delta +%1 | delta +%2 | delta +%3 | delta +%5 |
|---|---|---|---|---|---|
| 30 | **%0** (%0) / 30 / +1,8 | **%0** (%0) / 30 / +4,0 | **%10** (%10) / 30 / +8,3 | **%25** (%20) / 30 / +11,8 | **%45** (%25) / 30 / +16,6 |
| 100 | **%20** (%20) / 99 / +3,4 | **%30** (%25) / 99 / +7,1 | **%50** (%50) / 99 / +11,4 | **%100** (%100) / 99 / +15,7 | **%100** (%100) / 99 / +20,5 |
| 300 | **%0** (%0) / 294 / +1,4 | **%30** (%30) / 294 / +4,8 | **%90** (%85) / 294 / +8,8 | **%100** (%100) / 294 / +13,0 | **%100** (%100) / 294 / +18,2 |
| 1000 | - | - | - | - | - |
| yari | **%15** (%15) / 583 / +2,1 | **%90** (%75) / 583 / +5,7 | **%100** (%100) / 583 / +9,5 | **%100** (%100) / 583 / +13,7 | **%100** (%100) / 583 / +18,8 |

Dört karar hücresi (ABD + AVR x eğitim + sınama) AYNI tohumda birlikte yakalama payı (DS karne v3'ün 'her hücrede' şartının çekirdeği):

| n | delta 0 | delta +1% | delta +2% | delta +3% | delta +5% |
|---|---|---|---|---|---|
| 30 | %0 | %0 | %0 | %0 | %0 |
| 100 | %0 | %0 | %0 | %10 | %30 |
| 300 | %0 | %0 | %5 | %45 | %100 |
| 1000 | - | - | - | - | - |
| yari | %0 | %75 | %100 | %100 | %100 |

Düz dil: cetvelin bir hücrede >= %80 yakaladığı en küçük delta ve o delta'da en küçük n: ABD egitim: delta +1% için n >= yari; ABD sinama: delta +1% için n >= yari; AVR egitim: delta +1% için n >= yari; AVR sinama: delta +1% için n >= yari.
Plasebo (delta 0) yanlış pozitif payı: ortalama %4.2 (en yüksek hücre %20); iki yönlü p ile %3.7.

Plasebo (delta 0) hücre başına ortalama FARK (bütün n ve tohumlar; beklenen 0) / yakalama: ABD egitim +0,45 puan / %5; ABD sinama -0,11 puan / %2; AVR egitim -0,07 puan / %2; AVR sinama +2,17 puan / %9.

- ABD sürüklenmenin ham h5'e etkisi (bütün ANA olaylar tutan olsaydı; eğitim / sınama): delta +0%: %51.0 / %50.0; delta +1%: %52.9 / %52.9; delta +2%: %55.0 / %55.1; delta +3%: %57.0 / %57.5; delta +5%: %61.3 / %62.1
- AVR sürüklenmenin ham h5'e etkisi (bütün ANA olaylar tutan olsaydı; eğitim / sınama): delta +0%: %48.7 / %45.5; delta +1%: %51.4 / %48.7; delta +2%: %53.9 / %52.6; delta +3%: %56.0 / %56.3; delta +5%: %60.8 / %62.0

## 2. B — BİLİNEN GERÇEK İZ: üç cetvel yan yana (ABD karar; AVR momentum BİLGİ)

Kod: U = üst onda vs orta eşler; A = alt onda vs orta eşler; UA = üst onda vs aynı gün aynı kova alt onda (doğrudan). p = ay kümeli işaret permütasyonu, önceden yazılı yön (U +, A -, UA +). h5 FARK puan; r15 = stop'suz 15 bar kapanış getirisi farkı (aynı eşler); r60 = OC eşli fark (momentum x likidite eşleri). [alt, üst] = ay kümeli boot %95.

| B | pazar | kod | hücre | n | h5 olay / eş | h5 FARK [alt, üst] | p (h5) | güç | r15 FARK [alt, üst] | p (r15) | r60 FARK [alt, üst] | p (r60) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | ABD | U | egitim | 6510 | 48,0 / 44,2 | +3,7 [+0,2, +7,0] | 0,0173 | 1,00 | +0,47 [-0,31, +1,26] | 0,1185 | +1,48 [+0,21, +2,79] | 0,0135 |
| B1 | ABD | U | sinama | 4783 | 52,5 / 48,8 | +3,7 [+0,4, +6,9] | 0,0155 | 1,00 | +0,91 [-0,21, +2,07] | 0,0692 | +2,86 [+0,79, +5,17] | 0,0048 |
| B1 | ABD | A | egitim | 6508 | 50,8 / 45,4 | +5,3 [+3,1, +7,5] | 1,0000 | 1,00 | +0,17 [-0,72, +1,05] | 0,6516 | +0,30 [-1,72, +2,56] | 0,6060 |
| B1 | ABD | A | sinama | 4729 | 50,6 / 49,1 | +1,6 [-1,1, +4,2] | 0,8734 | 1,00 | -0,22 [-1,09, +0,66] | 0,3122 | +0,90 [-0,79, +2,65] | 0,8417 |
| B1 | ABD | UA | egitim | 5542 | 48,5 / 51,7 | -3,2 [-7,8, +1,6] | 0,9026 | 1,00 | +0,09 [-1,32, +1,44] | 0,4520 | - [-, -] | - |
| B1 | ABD | UA | sinama | 4503 | 52,4 / 49,4 | +2,9 [-2,7, +8,3] | 0,1691 | 1,00 | +1,53 [-0,27, +3,44] | 0,0658 | - [-, -] | - |
| B2 | ABD | U | egitim | 2326 | 51,1 / 45,6 | +5,5 [+3,0, +7,8] | 0,0004 | 1,00 | +0,93 [+0,32, +1,49] | 0,0013 | +1,25 [-0,07, +2,59] | 0,0363 |
| B2 | ABD | U | sinama | 2227 | 48,5 / 47,1 | +1,4 [-1,2, +4,2] | 0,1738 | 1,00 | -0,16 [-0,66, +0,30] | 0,7360 | -0,31 [-1,88, +1,34] | 0,6420 |
| B2 | ABD | A | egitim | 2280 | 40,9 / 42,5 | -1,6 [-3,9, +0,6] | 0,0728 | 1,00 | -0,02 [-0,63, +0,62] | 0,4799 | +1,37 [-0,05, +3,11] | 0,9597 |
| B2 | ABD | A | sinama | 2377 | 43,3 / 44,8 | -1,5 [-3,5, +0,5] | 0,0677 | 1,00 | -0,81 [-1,42, -0,23] | 0,0094 | +0,09 [-1,63, +1,67] | 0,5371 |
| B2 | ABD | UA | egitim | 133 | 63,9 / 52,5 | +11,4 [+1,3, +21,7] | 0,0230 | 0,25 | -0,39 [-2,39, +1,86] | 0,6256 | - [-, -] | - |
| B2 | ABD | UA | sinama | 354 | 56,2 / 51,9 | +4,3 [-2,4, +12,3] | 0,1316 | 0,54 | +0,05 [-1,43, +1,49] | 0,4778 | - [-, -] | - |
| B1 | AVR (bilgi) | U | egitim | 3309 | 37,7 / 35,0 | +2,7 [-0,4, +6,0] | 0,0545 | 1,00 | +0,10 [-0,53, +0,70] | 0,3817 | +0,23 [-0,51, +1,02] | 0,2948 |
| B1 | AVR (bilgi) | U | sinama | 1981 | 39,0 / 34,4 | +4,7 [+0,7, +8,4] | 0,0141 | 1,00 | +0,41 [-0,27, +1,03] | 0,1101 | +2,14 [+1,14, +3,16] | 0,0001 |
| B1 | AVR (bilgi) | A | egitim | 3212 | 41,7 / 37,2 | +4,5 [+1,8, +7,3] | 0,9989 | 1,00 | +0,32 [-0,32, +1,09] | 0,7954 | +0,51 [-0,68, +1,91] | 0,7760 |
| B1 | AVR (bilgi) | A | sinama | 1913 | 41,1 / 36,9 | +4,2 [+1,6, +7,1] | 0,9981 | 1,00 | +0,01 [-0,64, +0,70] | 0,5160 | -1,08 [-2,12, +0,02] | 0,0249 |
| B1 | AVR (bilgi) | UA | egitim | 2164 | 39,0 / 40,1 | -1,0 [-6,2, +3,7] | 0,6584 | 1,00 | -0,02 [-1,30, +1,04] | 0,5103 | - [-, -] | - |
| B1 | AVR (bilgi) | UA | sinama | 1464 | 39,5 / 38,9 | +0,6 [-4,7, +6,0] | 0,4059 | 1,00 | +0,75 [-0,28, +1,81] | 0,0809 | - [-, -] | - |

U - A yayılımı (her biri orta eşlere göre; ay kümeli ortak boot %95):

| B | pazar | hücre | h5 yayılım [alt, üst] | r15 yayılım [alt, üst] | r60 yayılım [alt, üst] |
|---|---|---|---|---|---|
| B1 | ABD | egitim | -1,6 [-6,1, +2,8] | +0,30 [-1,03, +1,56] | +1,19 [-1,55, +3,76] |
| B1 | ABD | sinama | +2,1 [-3,1, +7,4] | +1,14 [-0,42, +2,77] | +1,96 [-0,84, +4,97] |
| B2 | ABD | egitim | +7,1 [+3,8, +10,4] | +0,95 [+0,17, +1,74] | -0,12 [-1,84, +1,42] |
| B2 | ABD | sinama | +2,9 [-0,4, +6,1] | +0,65 [-0,07, +1,40] | -0,40 [-2,71, +2,02] |
| B1 | AVR | egitim | -1,8 [-6,4, +3,0] | -0,22 [-1,54, +0,90] | -0,28 [-2,14, +1,53] |
| B1 | AVR | sinama | +0,4 [-5,1, +5,5] | +0,40 [-0,60, +1,39] | +3,21 [+1,45, +4,96] |

Duyarlılık (aynı olaylar; z = FARK / (boot %95 yarı genişliği / 1,96); işaret beklenen yönle karşılaştırılır):

| B | pazar | kod | hücre | beklenen | z h5 | z r15 | z r60 |
|---|---|---|---|---|---|---|---|
| B1 | ABD | U | egitim | + | 2,14 | 1,19 | 2,25 |
| B1 | ABD | U | sinama | + | 2,22 | 1,57 | 2,56 |
| B1 | ABD | A | egitim | - | 4,74 | 0,38 | 0,27 |
| B1 | ABD | A | sinama | - | 1,18 | -0,50 | 1,03 |
| B1 | ABD | UA | egitim | + | -1,32 | 0,13 | - |
| B1 | ABD | UA | sinama | + | 1,03 | 1,61 | - |
| B2 | ABD | U | egitim | + | 4,54 | 3,15 | 1,84 |
| B2 | ABD | U | sinama | + | 1,01 | -0,65 | -0,38 |
| B2 | ABD | A | egitim | - | -1,43 | -0,05 | 1,70 |
| B2 | ABD | A | sinama | - | -1,46 | -2,67 | 0,10 |
| B2 | ABD | UA | egitim | + | 2,20 | -0,36 | - |
| B2 | ABD | UA | sinama | + | 1,15 | 0,07 | - |
| B1 | AVR | U | egitim | + | 1,66 | 0,30 | 0,59 |
| B1 | AVR | U | sinama | + | 2,38 | 1,25 | 4,13 |
| B1 | AVR | A | egitim | - | 3,25 | 0,88 | 0,77 |
| B1 | AVR | A | sinama | - | 2,96 | 0,03 | -1,97 |
| B1 | AVR | UA | egitim | + | -0,41 | -0,04 | - |
| B1 | AVR | UA | sinama | + | 0,23 | 1,41 | - |

Huni: B1_ABD: sinyal 144111, havuz olay 115003, U 11553, A 11442, ANA {'egitim': 13367, 'sinama': 9628}; B2_ABD: sinyal 50151, havuz olay 40275, U 4677, A 4866, ANA {'sinama': 4679, 'egitim': 4657}; B1_AVR: sinyal 67795, havuz olay 54092, U 5466, A 5353, ANA {'egitim': 6832, 'sinama': 3987}
PEAD onda sınırları (eğitim 23447 tepki): q10 -7,90, q90 +8,17. sec_ozet ham satır örnekleri: - CIK 1750 (AIR): form '8-K', tarih 2026-10-26, madde '1.01,2.03,7.01,9.01' | - CIK 1800 (ABT): form 'SCHEDULE 13G', tarih 2026-04-29, madde '' | - CIK 2098 (ACU): form '8-K', tarih 2026-07-21, madde '1.01,1.02,2.03,9.01'

## 3. C — ÖRNEKLER (her biri n = 1; bulgu denmez, tek tek okunur)

| örnek | sinyal (kaynak) | giriş | stop uzaklığı | h5 | h10 | st5 | takip getirisi | çıkış barı (tür) | r15 | neden |
|---|---|---|---|---|---|---|---|---|---|---|
| TEHOL-24 | 2024-12-17 (S6 al (AL)) | 2024-12-18 | %20.7 | 1 | 1 | 0 | +69,6 | 12 (stop) | +91,2 | HEDEFE ULAŞTI: +%5 kapanış bar 0 (+%10 da) |
| TEHOL-25 | 2025-06-27 (S6 al (AL)) | 2025-06-30 | %13.9 | 1 | 0 | 0 | -11,3 | 3 (stop) | -6,6 | HEDEFE ULAŞTI: +%5 kapanış bar 1 |
| BINBN-24 | 2025-04-03 (120 gün üst sınır kırılımı (hat 20 bar dip)) | 2025-04-04 | %42.7 | 1 | 1 | 0 | +24,2 | 15 (stop) | +23,7 | HEDEFE ULAŞTI: +%5 kapanış bar 2 (+%10 da) |
| KTLEV-24 | 2024-12-12 (120 gün üst sınır kırılımı (hat 20 bar dip)) | 2024-12-13 | %15.8 | 0 | 0 | 1 | -11,6 | 5 (stop) | -13,4 | stop önce: bar 4 kapanışı stop altında (stop uzaklığı %15.8; 15 barda en düşük kapanış %-17.2, en yüksek %-1.8) |
| CAPR (eş / ALKT) | 2026-10-21 (kendi hattı (20 bar dip)) | 2026-10-22 | %2.7 | 1 | 0 | 0 | +1,4 | 2 (stop) | +92,5 | HEDEFE ULAŞTI: +%5 kapanış bar 0 |
| ARRY (eş / RARE) | 2026-10-20 (kendi hattı (20 bar dip)) | 2026-10-21 | %7.8 | 0 | 0 | 1 | -5,3 | 4 (stop) | +39,1 | stop önce: bar 3 kapanışı stop altında (stop uzaklığı %7.8; 15 barda en düşük kapanış %-7.4, en yüksek %+72.2) |
| AXGN (eş / ALKT) | 2026-10-21 (kendi hattı (20 bar dip)) | 2026-10-22 | %8.4 | 1 | 1 | 0 | +54,5 | 20 (kesik) | +60,7 | HEDEFE ULAŞTI: +%5 kapanış bar 4 (+%10 da) |
| TDOC (eş / RARE) | 2026-10-20 (kendi hattı (20 bar dip)) | 2026-10-21 | %13.8 | 1 | 1 | 0 | +45,1 | 13 (stop) | +45,1 | HEDEFE ULAŞTI: +%5 kapanış bar 5 (+%10 da) |
| JBLU (eş / FNF) | 2026-10-22 (kendi hattı (20 bar dip)) | 2026-10-23 | %9.5 | 0 | 0 | 1 | +6,9 | 2 (stop) | +46,5 | stop önce: bar 1 kapanışı stop altında (stop uzaklığı %9.5; 15 barda en düşük kapanış %-8.8, en yüksek %+54.6) |
| LQDA (eş / FNF) | 2026-10-22 (kendi hattı (20 bar dip)) | 2026-10-23 | %45.1 | 1 | 1 | 0 | +4,6 | 7 (stop) | +45,8 | HEDEFE ULAŞTI: +%5 kapanış bar 0 (+%10 da) |

Ek satırlar: S6 sinyalinde hat = 20 bar dip ile; Ekim kazananlarında ESLER geometrisi (adayın stop uzaklığı):

- TEHOL-24 (20 bar dip hattı): d %20.7, h5 1.0, h10 1.0, st5 0.0, getiri +69,6, çıkış barı 12
- TEHOL-25 (20 bar dip hattı): d %15.7, h5 1.0, h10 0.0, st5 0.0, getiri -11,3, çıkış barı 3
- CAPR (eş / ALKT) (ESLER geometrisi): d %11.9, h5 1.0, h10 0.0, st5 0.0, getiri +1,4, çıkış barı 2; HEDEFE ULAŞTI: +%5 kapanış bar 0
- ARRY (eş / RARE) (ESLER geometrisi): d %13.9, h5 0.0, h10 0.0, st5 1.0, getiri -5,3, çıkış barı 4; stop önce: bar 3 kapanışı stop altında (stop uzaklığı %13.9; 15 barda en düşük kapanış %-7.4, en yüksek %+72.2)
- AXGN (eş / ALKT) (ESLER geometrisi): d %11.9, h5 1.0, h10 1.0, st5 0.0, getiri +54,5, çıkış barı 20; HEDEFE ULAŞTI: +%5 kapanış bar 4 (+%10 da)
- TDOC (eş / RARE) (ESLER geometrisi): d %13.9, h5 1.0, h10 1.0, st5 0.0, getiri +45,1, çıkış barı 13; HEDEFE ULAŞTI: +%5 kapanış bar 5 (+%10 da)
- JBLU (eş / FNF) (ESLER geometrisi): d %8.6, h5 0.0, h10 0.0, st5 1.0, getiri +6,9, çıkış barı 2; stop önce: bar 1 kapanışı stop altında (stop uzaklığı %8.6; 15 barda en düşük kapanış %-8.8, en yüksek %+54.6)
- LQDA (eş / FNF) (ESLER geometrisi): d %8.6, h5 1.0, h10 1.0, st5 0.0, getiri +4,6, çıkış barı 7; HEDEFE ULAŞTI: +%5 kapanış bar 0 (+%10 da)

## 4. SONUÇ

**Cetvel bilinen izi görüyor mu: EVET** (ön kayıt bölüm 2 kuralı).
- A: gerçek DS boyutunda (yari) dört hücrede de >= %80 yakalanan en küçük sürüklenme: +%1; plasebo yanlış pozitif ortalama %4.2.
- B: iki dönemde de beklenen yönde ve p < 0,05 olan (kod, cetvel): B1U/h5, B1U/r60.
- Beklenen yönün TERSİNE boot aralığı sıfırı dışlayan (kod, cetvel, hücre): B1A/h5 egitim (+5,31, boot [+3,11, +7,50]).
- Hangi cetvel daha duyarlı: duyarlılık tablosu (z) aynı olaylarda h5 / r15 / r60'ı yan yana koyar; A'da delta'nın h5'e dönüşümü (sürüklenme satırları) h5'in fiyat sürüklenmesini ne kadar seyrelttiğini gösterir.

## 5. YENİDEN ÜRETİM

- A hücresi ['ABD', 'sinama', 300, 0.03, 0] (pazar, hücre, n, delta, tohum): kod FARK +6,941 puan, satır dosyasından düz pandas +6,941 (n 300 / 300) -> EŞİT; 50 tutan olayın sürüklenmiş h5'i yh_sim'den bağımsız düz döngüyle: bozuk 0.
- B hücresi ['B1U', 'sinama']: kod h5 FARK +3,663 / dosya +3,663; r15 FARK kod +0,913 / dosya +0,913 -> EŞİT; 50 olayın h5 ve r15'i düz döngüyle: bozuk 0; 5 olayın eş h5'i (eş kümesi elle: aynı gün, aynı kova, orta, havuzda, adayın d'si) bozuk 0.
- Durum: **TUTTU**.

## 6. HATA

Koşu sırasında bulunan hatalar ve sınırlar (ayrıntı alt ajan raporunda):

- Ekim 2026 kazananları (C) /tmp/veri'de yok (V_ABD 22 Eki'de biter, kriz kesiği 31.08.2026); CANLI_SONUC ile aynı kaynak /tmp/veri_canli kullanıldı ve kriz kesiği YALNIZ bu bilgi satırında aşıldı (iş tanımı 'yalnız /tmp/veri' dedi: SAPMA, bilgi satırı).
- B1 eğitim hücresi V_ABD 2015-06 başlangıcı yüzünden 252 bar geçmiş ancak 2016 ortasından itibaren var (eğitim ilk ayları eksik).
- B2 PEAD tepki vekili 2 günlük artık getiri (analist sürprizi değil); 8-K 2.02 bilanço dışı (ara duyuru) başvuruları da içerir.
- B'de ambargo yok (önceden yazılı gerekçe: eşikler sonuç kullanmaz); A DS ambargosunu aynen taşır.
- A plasebosunda AVR sınama hücresi sıfır değil: rastgele 'tutan' kümesi DS içi eşlere göre ortalama +2,2 puan FARK veriyor (n 100'de yanlış pozitif %20, yarıda %15). Rastgele etiket altında bu fark DS içi eş geometrisinden (eşler olayın stop uzaklığıyla ölçülür) ve küçük hücreden geliyor; DS raporundaki AVR sınama FARK'larının çoğunun pozitif olması bununla okunmalı (cetvel bulgusu).
- A'da AVR sınama n = 1000 ölçülmedi: havuz 1.206 olay, önceden yazılı tavan (tutan <= havuzun 2/3'ü = 804).
- C: BINBN-24 ve KTLEV-24 için kutu sonu penceresinde S6 'al' yok; 120 gün kuralı veri kısa olduğu için (BINBN 2024-10, KTLEV 2024-03 başlıyor) ancak 2025-04-03 / 2024-12-12'de sinyal verdi: Cemal'in kırılım günü değil, bu iki satır onun örneğinin sınaması sayılmaz.
- Ön kayıttan önce gerçek veride yalnız getirisiz duman denemesi yapıldı (B sinyal / huni sayıları, C sinyal günleri; h5 / getiri hesaplanmadı).
- Rapor gösterimi koşudan SONRA genişletildi (plasebo hücre satırı, z duyarlılık tablosu, ters yön satırı, bu HATA maddeleri); hesap kodu ve pozitif_kontrol.json değişmedi (gösterim; ön kayıttaki PK_KOD_SHA koşu anındaki koddur).

## 7. KONTROL LİSTESİ (K1-K14)

| Kod | Yanıt | Kanıt |
|---|---|---|
| K1 | EVET | eş = DS ile aynı: aynı giriş günü, aynı kova (ATRP tercili x OC likidite üçlüsü), F == 0, olayın d'si ile aynı 15 bar kuralı (ds_olc / ds_es_topla, kopya yok); A'da sürüklenme yalnız tutan olayın kendi penceresine eklenir, eşler dokunulmaz; B'de U ve A orta eşlere karşı ayrı + doğrudan U-A; mekanik üstünlük: sürüklenme dışında olay ile eş aynı süreçten (A plasebo delta 0) |
| K2 | EVET | MOM t'de bitmiş barlardan (t-21, t-252); PEAD tepkisi b0 kapanışına kadar, giriş b0+1 açılışı; PEAD onda sınırları eğitimden (getirisiz) sabit; ATRP / hat t'de; test_pozitif_kontrol prefix: veri t'de kesilince MOM / tepki / ATRP / hat aynı |
| K3 | EVET | OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması (ds_veri); 15 bar yalnız geçerli barlar (yh_sim); sinyal günü geçerli bar (oc_olay_hazirla) |
| K4 | EVET | A: DS ANA olayları (15 gün tekil); B1 ay sonu (aynı hissede >= ~21 bar arayla); B2 ANA >= 15 bar arayla, aynı (hisse, t) bir kez; n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan raporda (B) |
| K5 | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (oc_olay_hazirla d; yh_sim satır 0); C Ekim: ESLER giriş günü açılışı |
| K6 | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur; geçmiş bölünme şüphesi havuz dışı (OC); C Ekim verisi /tmp/veri_canli aynı kip (CANLI_SONUC ile aynı kaynak) |
| K7 | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580); yanlılık hem olaya hem eşe; raporda yazılır; A'da sürüklenme bilinen değer olduğu için yanlılıktan bağımsız |
| K8 | EVET | A: 20 tohum x 5 n x 5 delta x 2 pazar x 2 hücre, n 30..yarı; B: eğitim 2016-22 / sınama 2023-26 ayrı; n < 30 hücre ÖLÇÜLEMEDİ yazılır; C n = 1 / örnek: bulgu denmez, tek tek okunur |
| K9 | EVET | POZITIF_KONTROL_ON_KAYIT.md: PK_ESIK sha, kod sha, cetvel sha'ları (DS_ON_KAYIT ile eşit), veri sha; pk_kapi ön kayıt git'te işlenmiş ve değişmemiş + ik_kontrol_kapisi denetler; tasarım iş tanımından (commit 4505d5c) önce yazıldı, sonuç görülmeden |
| K10 | EVET | sec_ozet 8-K madde alanı virgülle ayrılır (DS._ds_sec_olay ile aynı ayrıştırma, kopya yok); bilgi barı başvuru günü sonrası ilk geçerli bar; 3 ham satır ön kayıtta gösterilir |
| K11 | EVET | A bir hücre (ABD sınama n 300 delta +%3 tohum 0) ve B bir hücre (B1U sınama) satır dosyasından düz pandas ile; A'da 50 tutan olayın sürüklenmiş h5'i, B'de 50 olayın h5 / r15'i ve 5 olayın eş h5'i yh_sim'den bağımsız düz döngüyle |
| K12 | EVET | bu iş cetvel sınaması; 'iz' iddiası yok; yakalama payı, FARK ve p ayrı; sayı ve yorum ayrı cümle |
| K13 | EVET | çakışma kapısı (_cakisma_kontrol_pk; pk_ / PK_ önekleri dışında ezme DURUR; test); DS / YH / OC değişmedi (sha = DS ön kaydı); defter dosyalarına dokunulmadı; e-posta / anahtar taraması (YH._yh_yaz); dış servis yok |
| K14 | UYGULANMAZ | öneri / gerçek para işi değil; cetvel sınaması |
