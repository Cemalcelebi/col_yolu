# K60 — sinyal kütüphanesi, iki cetvel, üç dönem: RAPOR

Ön kayıt: 2026-11-11 12:09:42 UTC (mühür e1749249eeb8, dosya sha256 eba12e1d0602). K60 v1.0 (2026-11-11): sinyal kütüphanesi x iki cetvel (R1 portföy cetveli v2, R2 olasılık tablosu), KEŞİF / DOĞRULAMA / KASA, Benjamini-Hochberg + plasebo; geniş ABD evreni (yalnız yaşayanlar)

- KEŞİF: koşu 2026-11-11 12:14:07 UTC → 2026-11-11 12:15:09 UTC (61 sn); 4666 hisse, oluşum ayı R1 120, R2 120; uygun evren ort. 1642. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%1625, +%300 üstü 10 / 197085 hisse-ay; en büyük 12 aylık getiri +%8364, +%1000 üstü 52 / 197085.
- DOĞRULAMA: koşu 2026-11-11 12:16:19 UTC → 2026-11-11 12:17:07 UTC (48 sn); 4666 hisse, oluşum ayı R1 24, R2 24; uygun evren ort. 2274. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%494, +%300 üstü 2 / 54569 hisse-ay; en büyük 12 aylık getiri +%1095, +%1000 üstü 2 / 54569.
- KASA: koşu 2026-11-11 12:19:40 UTC → 2026-11-11 12:20:31 UTC (50 sn); 4666 hisse, oluşum ayı R1 31, R2 20; uygun evren ort. 2516. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%482, +%300 üstü 5 / 77996 hisse-ay; en büyük 12 aylık getiri +%1844, +%1000 üstü 18 / 48635.

## Bulgular (düz dille)
- KEŞİF (2012-01 .. 2021-12): bir hissenin 12 ayda en az +%100 yapma taban oranı %4,1, en az -%50 düşme taban oranı %5,8 (yalnız yaşayanlar; ortanca ölçüm).
- 166 (sinyal, uç) satırı R1'de, 167 satır R2'de ölçüldü. KEŞİF-SEÇİLİ 114 çift: R1 yolundan 2, +%100 olasılığı (R2) yolundan 106, -%50 olasılığı (R2K) yolundan 98.
- Plasebo (200 rastgele sinyal): cetvel v2 yanlış pozitif net %0,0, brüt %1,5 (eşik %5; R1 yolu AÇIK); 'lift alt sınırı > 1' oranı +%100 için %4,5, -%50 için %4,0. Eşikler: net t(alfa) > 3,32 (eksi yön: brüt t < -2,69), +%100 lift > 1,08, -%50 lift > 1,07 (88 ve 165 hipotez).
- DOĞRULAMA: giren 125 çift, geçen 109 (R1 5, R2 96, R2K 93, R1 ters 0).
- KASA: giren 109 çift, geçen 97 (R1 1, R2 88, R2K 93, R1 ters 0).
- ETİKETLER: ACCRUALS (ALT): K60-OLASILIK İZİ; ACCRUALS (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; ACT_13D (UST): K60-KAÇINMA İZİ; AILE_DIS (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_EAR (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_INV (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_LIQ (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_MOM (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_PRF (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_RSK (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_SEA (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_SEA (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AILE_VAL (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; AM (ALT): K60-KAÇINMA İZİ; AMIHUD (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; ASSET_G (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; ASSET_G (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; BETA_BAB (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; BE_G (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; BE_G (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; BUYBACK_YLD (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; CAPEX_G (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; CAPEX_G (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; CBOP_A (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; CFP (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; CHS_FAIL (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; COMP4 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; DOLVOL (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; DOSYA_Y (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; D_ASSET_TURN (UST): K60-OLASILIK İZİ; EARN_STREAK (ALT): K60-KAÇINMA İZİ; EAR_ANN (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; EAR_ANN (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; EAR_FILE (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; EAR_FILE (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; EAR_VOL (ALT): K60-KAÇINMA İZİ; EAR_VOL (UST): K60-KAÇINMA İZİ; EP (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; E_424B5 (ALT): K60-KAÇINMA İZİ; E_IPO_3Y (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; E_RSPLIT (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; E_S3 (ALT): K60-KAÇINMA İZİ; F_SCORE (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; GAP_OVN (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; GAP_OVN (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; GP_A (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; HIGH52 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; IND_LEAD_BIG (ALT): K60-OLASILIK İZİ; ISKEW (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; IVOL_FF3 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; LEV_MKT (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; LTREV_60_13 (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MAX5 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MOM_12_1 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MOM_12_1 (UST): K60-OLASILIK İZİ; MOM_6_1 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MOM_6_1 (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MOM_INT_12_7 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; MOM_INT_12_7 (UST): K60-OLASILIK İZİ; NDF_BS (ALT): K60-OLASILIK İZİ; NDF_BS (UST): K60-OLASILIK İZİ; NEF (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; NET_PAYOUT_YLD (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; NOA (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; NSI_1Y (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; NSI_5Y (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; NT_LATE (ALT): K60-KAÇINMA İZİ; OP_BE (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; O_SCORE (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; PRICE_LVL (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; RD_ME (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; ROA_Q (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; ROE_TTM (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; RUNWAY (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SALES_ACCEL (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SALES_ACCEL (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SEAS_1 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SEAS_1 (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SEAS_2_5 (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SEAS_2_5 (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SIZE_ME (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SKEW_TOT (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SP (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SP (UST): K60-OLASILIK İZİ; SPREAD_CS (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; STREV_1M (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; STREV_1M (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; SUE_SRW (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; TREND_MA (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; TREND_MA (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; TURN_12M (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; VOL_60D (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; VOL_SHOCK (ALT): K60-OLASILIK İZİ, K60-KAÇINMA İZİ; VOL_SHOCK (UST): K60-OLASILIK İZİ, K60-KAÇINMA İZİ.
- İZ ilan edilemez: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi; bu ölçüm yalnız ABD ve yalnız yaşayanlar.

## Olasılık tablosu (ana sonuç)

Okuma: 'taban' = aynı aylarda BÜTÜN uygun evrende 12 ayda o olayın görülme oranı; 'kat' = uçtaki oran / taban oran; köşeli parantez = ay kümeli blok bootstrap %95 aralığı. ÜST = beklenen yöne göre en iyi %10 (bayrakta bayraklı grup), ALT = en kötü %10. Evren yalnız BUGÜN yaşayan şirketlerdir: P(-%50) ve katı ALT SINIRDIR, P(+%100) tabanı yukarı yanlıdır. Hiçbir satır İZ değildir (CLAUDE.md standardı: ABD + Avrupa).

## KEŞİF-SEÇİLİ özellikler (114 çift)

| özellik (uç) | dönem | ay | taban P(+%100) | P(+%100) | kat (lift) [%95 aralık] | taban P(-%50) | P(-%50) | kat [%95 aralık] | ort. 12 ay | medyan | evren ort. | etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACCRUALS (ALT) — (net kâr(y0) - faaliyet nakit akışı(y0)) / [varlık(y0 sonu)  | KEŞİF | 120 | %4,1 | %5,2 | 1,27 [1,05; 1,49] | %5,8 | %7,7 | 1,34 [0,83; 1,66] | +%14,2 | +%8,3 | +%14,5 | yol R2; K60-OLASILIK İZİ |
| ACCRUALS (ALT) | DOĞRULAMA | 24 | %3,7 | %5,6 | 1,52 [1,42; 1,64] | %7,0 | %10,2 | 1,47 [1,32; 1,62] | +%13,5 | +%5,3 | +%10,0 |  |
| ACCRUALS (ALT) | KASA | 20 | %6,8 | %9,0 | 1,32 [1,12; 1,65] | %7,3 | %9,8 | 1,35 [1,30; 1,41] | +%17,3 | +%1,0 | +%16,1 |  |
| ACCRUALS (ÜST) — (net kâr(y0) - faaliyet nakit akışı(y0)) / [varlık(y0 sonu)  | KEŞİF | 120 | %4,1 | %9,2 | 2,24 [1,83; 3,03] | %5,8 | %14,8 | 2,57 [2,08; 2,98] | +%19,0 | +%6,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ACCRUALS (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,9 | 1,60 [1,52; 1,70] | %7,0 | %14,0 | 2,00 [1,83; 2,15] | +%6,9 | -%2,6 | +%10,0 |  |
| ACCRUALS (ÜST) | KASA | 20 | %6,8 | %10,0 | 1,47 [1,25; 1,89] | %7,3 | %16,3 | 2,24 [1,99; 2,55] | +%15,3 | -%4,3 | +%16,1 |  |
| ACT_13D (ÜST) — son 60 takvim gününde SC 13D / SCHEDULE 13D (değişiklik hari | KEŞİF | 114 | %4,2 | %5,3 | 1,26 [1,03; 1,44] | %5,9 | %13,3 | 2,24 [2,03; 2,56] | +%12,3 | +%1,2 | +%14,2 | yol R2+R2K; K60-KAÇINMA İZİ |
| ACT_13D (ÜST) | DOĞRULAMA | 24 | %3,7 | %2,2 | 0,60 [0,40; 0,96] | %7,0 | %14,6 | 2,09 [1,64; 2,42] | -%2,5 | -%6,5 | +%10,0 |  |
| ACT_13D (ÜST) | KASA | 20 | %6,8 | %5,5 | 0,81 [0,60; 1,03] | %7,3 | %14,6 | 2,01 [1,54; 2,45] | +%8,7 | +%1,0 | +%16,1 |  |
| AILE_DIS (ALT) | KEŞİF | 120 | %4,1 | %9,5 | 2,32 [1,83; 3,34] | %5,8 | %18,4 | 3,20 [2,63; 3,67] | +%18,7 | +%0,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_DIS (ALT) | DOĞRULAMA | 24 | %3,7 | %10,2 | 2,76 [2,45; 3,06] | %7,0 | %27,3 | 3,92 [3,77; 4,09] | +%6,4 | -%17,6 | +%10,0 |  |
| AILE_DIS (ALT) | KASA | 20 | %6,8 | %17,8 | 2,61 [2,36; 3,12] | %7,3 | %24,4 | 3,35 [3,06; 3,60] | +%32,2 | -%6,5 | +%16,1 |  |
| AILE_EAR (ALT) | KEŞİF | 120 | %4,1 | %6,0 | 1,46 [1,34; 1,75] | %5,8 | %10,4 | 1,80 [1,56; 1,97] | +%13,7 | +%7,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_EAR (ALT) | DOĞRULAMA | 24 | %3,7 | %5,3 | 1,45 [1,27; 1,69] | %7,0 | %12,2 | 1,75 [1,60; 1,91] | +%9,5 | +%0,8 | +%10,0 |  |
| AILE_EAR (ALT) | KASA | 20 | %6,8 | %9,8 | 1,44 [1,30; 1,53] | %7,3 | %11,4 | 1,57 [1,25; 1,86] | +%20,5 | +%2,8 | +%16,1 |  |
| AILE_INV (ALT) | KEŞİF | 120 | %4,1 | %6,0 | 1,47 [1,15; 2,02] | %5,8 | %14,5 | 2,52 [1,90; 2,90] | +%9,9 | +%3,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_INV (ALT) | DOĞRULAMA | 24 | %3,7 | %6,2 | 1,67 [1,59; 1,72] | %7,0 | %14,2 | 2,04 [1,69; 2,33] | +%5,8 | -%6,1 | +%10,0 |  |
| AILE_INV (ALT) | KASA | 20 | %6,8 | %11,6 | 1,71 [1,53; 1,98] | %7,3 | %12,6 | 1,73 [1,59; 1,86] | +%23,7 | +%3,3 | +%16,1 |  |
| AILE_LIQ (ÜST) | KEŞİF | 120 | %4,1 | %7,4 | 1,80 [1,58; 2,29] | %5,8 | %11,1 | 1,93 [1,80; 2,20] | +%15,7 | +%5,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_LIQ (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,5 | 2,04 [1,84; 2,44] | %7,0 | %15,2 | 2,17 [2,09; 2,25] | +%7,5 | -%4,0 | +%10,0 |  |
| AILE_LIQ (ÜST) | KASA | 20 | %6,8 | %10,5 | 1,53 [1,43; 1,72] | %7,3 | %16,3 | 2,24 [2,18; 2,31] | +%16,6 | -%1,7 | +%16,1 |  |
| AILE_MOM (ALT) | KEŞİF | 120 | %4,1 | %6,7 | 1,62 [1,41; 1,71] | %5,8 | %10,7 | 1,85 [1,65; 2,08] | +%15,6 | +%7,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_MOM (ALT) | DOĞRULAMA | 24 | %3,7 | %5,8 | 1,57 [1,22; 2,06] | %7,0 | %16,4 | 2,36 [1,83; 2,75] | +%4,5 | -%7,8 | +%10,0 |  |
| AILE_MOM (ALT) | KASA | 20 | %6,8 | %11,7 | 1,72 [1,59; 1,81] | %7,3 | %11,7 | 1,61 [1,39; 1,77] | +%23,4 | +%3,4 | +%16,1 |  |
| AILE_MOM (ÜST) | KEŞİF | 120 | %4,1 | %4,9 | 1,19 [1,04; 1,54] | %5,8 | %6,7 | 1,17 [0,86; 1,49] | +%13,6 | +%7,5 | +%14,5 | yol R2 |
| AILE_MOM (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,4 | 1,47 [0,93; 1,83] | %7,0 | %3,7 | 0,53 [0,40; 0,70] | +%15,5 | +%5,6 | +%10,0 |  |
| AILE_PRF (ALT) | KEŞİF | 120 | %4,1 | %6,3 | 1,53 [1,37; 1,87] | %5,8 | %14,0 | 2,43 [2,13; 2,64] | +%10,0 | +%2,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_PRF (ALT) | DOĞRULAMA | 24 | %3,7 | %7,2 | 1,95 [1,84; 2,07] | %7,0 | %18,7 | 2,68 [2,40; 2,92] | +%5,0 | -%8,8 | +%10,0 |  |
| AILE_PRF (ALT) | KASA | 20 | %6,8 | %13,5 | 1,98 [1,79; 2,15] | %7,3 | %15,3 | 2,11 [1,67; 2,47] | +%26,0 | +%1,4 | +%16,1 |  |
| AILE_RSK (ALT) | KEŞİF | 120 | %4,1 | %8,6 | 2,10 [1,95; 2,42] | %5,8 | %12,8 | 2,23 [1,98; 2,41] | +%18,0 | +%4,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_RSK (ALT) | DOĞRULAMA | 24 | %3,7 | %7,5 | 2,02 [1,79; 2,17] | %7,0 | %15,5 | 2,23 [2,19; 2,28] | +%8,5 | -%5,8 | +%10,0 |  |
| AILE_RSK (ALT) | KASA | 20 | %6,8 | %13,6 | 1,99 [1,78; 2,34] | %7,3 | %16,4 | 2,26 [2,11; 2,40] | +%23,5 | -%3,5 | +%16,1 |  |
| AILE_SEA (ALT) | KEŞİF | 120 | %4,1 | %7,1 | 1,73 [1,57; 2,04] | %5,8 | %11,4 | 1,97 [1,89; 2,17] | +%15,2 | +%5,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_SEA (ALT) | DOĞRULAMA | 24 | %3,7 | %6,9 | 1,86 [1,71; 1,98] | %7,0 | %16,2 | 2,32 [2,13; 2,48] | +%5,2 | -%6,1 | +%10,0 |  |
| AILE_SEA (ALT) | KASA | 20 | %6,8 | %10,8 | 1,58 [1,37; 1,94] | %7,3 | %16,5 | 2,27 [2,17; 2,36] | +%17,2 | -%2,8 | +%16,1 |  |
| AILE_SEA (ÜST) | KEŞİF | 120 | %4,1 | %6,6 | 1,61 [1,40; 2,00] | %5,8 | %11,1 | 1,93 [1,64; 2,09] | +%14,1 | +%6,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_SEA (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,2 | 1,41 [1,22; 1,55] | %7,0 | %11,8 | 1,70 [1,52; 1,92] | +%6,8 | -%1,1 | +%10,0 |  |
| AILE_SEA (ÜST) | KASA | 20 | %6,8 | %11,4 | 1,66 [1,48; 1,89] | %7,3 | %10,8 | 1,49 [1,43; 1,55] | +%24,0 | +%3,7 | +%16,1 |  |
| AILE_VAL (ALT) | KEŞİF | 120 | %4,1 | %8,8 | 2,14 [1,51; 3,41] | %5,8 | %16,3 | 2,82 [2,10; 3,37] | +%15,0 | +%3,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AILE_VAL (ALT) | DOĞRULAMA | 24 | %3,7 | %6,7 | 1,81 [1,61; 2,00] | %7,0 | %17,7 | 2,54 [2,35; 2,75] | +%4,7 | -%8,4 | +%10,0 |  |
| AILE_VAL (ALT) | KASA | 20 | %6,8 | %13,1 | 1,92 [1,65; 2,41] | %7,3 | %18,0 | 2,48 [2,37; 2,58] | +%20,0 | -%3,6 | +%16,1 |  |
| AM (ALT) — toplam varlık(ç0) / PD | KEŞİF | 120 | %4,1 | %6,8 | 1,65 [1,18; 2,63] | %5,8 | %11,7 | 2,03 [1,42; 2,48] | +%15,7 | +%8,4 | +%14,5 | yol R2+R2K; K60-KAÇINMA İZİ |
| AM (ALT) | DOĞRULAMA | 24 | %3,7 | %4,7 | 1,27 [1,16; 1,44] | %7,0 | %8,8 | 1,27 [1,17; 1,38] | +%9,9 | +%4,2 | +%10,0 |  |
| AM (ALT) | KASA | 20 | %6,8 | %7,8 | 1,14 [0,94; 1,55] | %7,3 | %11,3 | 1,55 [1,23; 1,92] | +%11,6 | -%2,1 | +%16,1 |  |
| AMIHUD (ÜST) — son 252 işlem gününde (en az 150) ortalama |günlük getiri| / | KEŞİF | 120 | %4,1 | %8,6 | 2,08 [1,72; 2,83] | %5,8 | %15,9 | 2,76 [2,42; 3,31] | +%13,9 | -%0,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| AMIHUD (ÜST) | DOĞRULAMA | 24 | %3,7 | %8,6 | 2,33 [2,20; 2,48] | %7,0 | %18,6 | 2,67 [2,56; 2,82] | +%5,1 | -%10,0 | +%10,0 |  |
| AMIHUD (ÜST) | KASA | 20 | %6,8 | %10,9 | 1,60 [1,34; 2,12] | %7,3 | %23,5 | 3,23 [3,03; 3,46] | +%10,5 | -%9,6 | +%16,1 |  |
| ASSET_G (ALT) — varlık(ç0) / varlık(ç0-4) - 1 | KEŞİF | 120 | %4,1 | %6,8 | 1,65 [1,32; 2,23] | %5,8 | %14,9 | 2,58 [1,96; 2,97] | +%11,5 | +%4,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ASSET_G (ALT) | DOĞRULAMA | 24 | %3,7 | %5,8 | 1,58 [1,40; 1,69] | %7,0 | %15,7 | 2,25 [1,69; 2,70] | +%5,7 | -%4,1 | +%10,0 |  |
| ASSET_G (ALT) | KASA | 20 | %6,8 | %11,5 | 1,68 [1,44; 1,99] | %7,3 | %12,2 | 1,68 [1,45; 1,91] | +%24,7 | +%3,6 | +%16,1 |  |
| ASSET_G (ÜST) — varlık(ç0) / varlık(ç0-4) - 1 | KEŞİF | 120 | %4,1 | %7,4 | 1,79 [1,48; 2,39] | %5,8 | %8,3 | 1,43 [1,26; 1,82] | +%21,4 | +%7,9 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ASSET_G (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,3 | 1,98 [1,89; 2,09] | %7,0 | %15,0 | 2,15 [1,71; 2,70] | +%8,9 | -%2,4 | +%10,0 |  |
| ASSET_G (ÜST) | KASA | 20 | %6,8 | %10,8 | 1,59 [1,38; 2,00] | %7,3 | %16,9 | 2,32 [1,99; 2,58] | +%19,1 | -%3,0 | +%16,1 |  |
| BETA_BAB (ALT) — korelasyon(hisse, piyasa; son 1260 gün, en az 504) x σ_hisse | KEŞİF | 120 | %4,1 | %9,9 | 2,41 [2,18; 2,99] | %5,8 | %10,9 | 1,89 [1,46; 2,60] | +%23,0 | +%7,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| BETA_BAB (ALT) | DOĞRULAMA | 24 | %3,7 | %8,8 | 2,39 [2,32; 2,45] | %7,0 | %12,6 | 1,80 [1,62; 2,05] | +%14,2 | -%3,1 | +%10,0 |  |
| BETA_BAB (ALT) | KASA | 20 | %6,8 | %18,5 | 2,71 [2,59; 2,80] | %7,3 | %16,3 | 2,24 [1,90; 2,52] | +%41,6 | +%5,9 | +%16,1 |  |
| BE_G (ALT) — özkaynak(ç0) / özkaynak(ç0-4) - 1; ikisi de > 0 | KEŞİF | 120 | %4,1 | %6,0 | 1,46 [1,19; 1,93] | %5,8 | %13,3 | 2,31 [1,73; 2,67] | +%11,2 | +%3,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| BE_G (ALT) | DOĞRULAMA | 24 | %3,7 | %4,6 | 1,25 [1,15; 1,35] | %7,0 | %12,4 | 1,78 [1,35; 2,16] | +%6,9 | -%0,7 | +%10,0 |  |
| BE_G (ALT) | KASA | 20 | %6,8 | %9,7 | 1,42 [1,23; 1,66] | %7,3 | %10,2 | 1,41 [1,19; 1,63] | +%20,9 | +%3,4 | +%16,1 |  |
| BE_G (ÜST) — özkaynak(ç0) / özkaynak(ç0-4) - 1; ikisi de > 0 | KEŞİF | 120 | %4,1 | %7,5 | 1,82 [1,59; 2,31] | %5,8 | %8,6 | 1,49 [1,34; 1,82] | +%20,7 | +%10,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| BE_G (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,2 | 1,95 [1,80; 2,14] | %7,0 | %13,5 | 1,93 [1,63; 2,34] | +%10,8 | +%0,2 | +%10,0 |  |
| BE_G (ÜST) | KASA | 20 | %6,8 | %10,6 | 1,55 [1,39; 1,84] | %7,3 | %16,1 | 2,22 [1,93; 2,43] | +%18,9 | -%2,9 | +%16,1 |  |
| BM (ALT) — StockholdersEquity(ç0) / PD; özkaynak > 0 | KEŞİF | 120 | %4,1 | %5,6 | 1,36 [1,04; 2,06] | %5,8 | %9,2 | 1,60 [1,24; 1,87] | +%16,6 | +%11,4 | +%14,5 | yol R2+R2K |
| BM (ALT) | DOĞRULAMA | 24 | %3,7 | %3,4 | 0,93 [0,84; 1,04] | %7,0 | %7,0 | 1,00 [0,92; 1,12] | +%11,5 | +%7,2 | +%10,0 |  |
| BM (ÜST) — StockholdersEquity(ç0) / PD; özkaynak > 0 | KEŞİF | 120 | %4,1 | %6,6 | 1,59 [1,03; 1,95] | %5,8 | %6,9 | 1,20 [0,73; 1,97] | +%19,8 | +%9,1 | +%14,5 | yol R2 |
| BM (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,33 [1,19; 1,58] | %7,0 | %7,1 | 1,01 [0,80; 1,19] | +%12,2 | +%5,0 | +%10,0 |  |
| BM (ÜST) | KASA | 20 | %6,8 | %6,9 | 1,01 [0,82; 1,11] | %7,3 | %7,5 | 1,03 [0,95; 1,10] | +%15,5 | +%6,7 | +%16,1 |  |
| BUYBACK_YLD (ALT) — geri alım ödemesi (y0; yoksa 0, y0'da faaliyet nakit akışı o | KEŞİF | 120 | %4,1 | %5,3 | 1,28 [1,15; 1,55] | %5,8 | %8,5 | 1,48 [1,32; 1,58] | +%13,7 | +%7,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| BUYBACK_YLD (ALT) | DOĞRULAMA | 24 | %3,7 | %5,3 | 1,44 [1,35; 1,57] | %7,0 | %10,7 | 1,54 [1,43; 1,64] | +%7,9 | +%0,4 | +%10,0 |  |
| BUYBACK_YLD (ALT) | KASA | 20 | %6,8 | %8,3 | 1,22 [1,13; 1,36] | %7,3 | %9,7 | 1,33 [1,22; 1,42] | +%19,4 | +%4,6 | +%16,1 |  |
| CAPEX_G (ALT) — yatırım harcaması(y0) / [(y0-1) + (y0-2)] / 2 - 1; payda > 0 | KEŞİF | 120 | %4,1 | %7,2 | 1,75 [1,41; 2,25] | %5,8 | %12,7 | 2,21 [1,99; 2,54] | +%14,3 | +%5,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| CAPEX_G (ALT) | DOĞRULAMA | 24 | %3,7 | %6,2 | 1,68 [1,53; 1,90] | %7,0 | %17,0 | 2,43 [2,13; 2,73] | +%3,1 | -%9,5 | +%10,0 |  |
| CAPEX_G (ALT) | KASA | 20 | %6,8 | %9,4 | 1,38 [1,21; 1,48] | %7,3 | %12,6 | 1,74 [1,63; 1,84] | +%18,0 | -%1,0 | +%16,1 |  |
| CAPEX_G (ÜST) — yatırım harcaması(y0) / [(y0-1) + (y0-2)] / 2 - 1; payda > 0 | KEŞİF | 120 | %4,1 | %6,3 | 1,52 [1,35; 1,90] | %5,8 | %9,2 | 1,59 [1,28; 1,81] | +%15,5 | +%6,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| CAPEX_G (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,3 | 1,70 [1,45; 1,83] | %7,0 | %8,8 | 1,27 [1,20; 1,34] | +%15,2 | +%6,9 | +%10,0 |  |
| CAPEX_G (ÜST) | KASA | 20 | %6,8 | %12,4 | 1,82 [1,46; 2,25] | %7,3 | %18,4 | 2,53 [2,42; 2,63] | +%17,3 | -%5,0 | +%16,1 |  |
| CBOP_A (ALT) — faaliyet nakit akışı(y0) / varlık(y0 sonu) (yaklaşık sürüm) | KEŞİF | 120 | %4,1 | %8,9 | 2,15 [1,58; 3,39] | %5,8 | %19,4 | 3,37 [2,61; 3,88] | +%15,6 | -%1,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| CBOP_A (ALT) | DOĞRULAMA | 24 | %3,7 | %9,4 | 2,55 [2,43; 2,67] | %7,0 | %26,2 | 3,76 [3,58; 3,97] | +%5,4 | -%17,0 | +%10,0 |  |
| CBOP_A (ALT) | KASA | 20 | %6,8 | %16,4 | 2,40 [2,24; 2,70] | %7,3 | %24,8 | 3,42 [2,84; 3,89] | +%27,0 | -%7,7 | +%16,1 |  |
| CFP (ALT) — faaliyet nakit akışı (y0, yıllık) / PD | KEŞİF | 120 | %4,1 | %9,0 | 2,19 [1,68; 3,31] | %5,8 | %16,4 | 2,85 [2,46; 3,35] | +%17,9 | -%0,3 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| CFP (ALT) | DOĞRULAMA | 24 | %3,7 | %9,8 | 2,67 [2,46; 2,87] | %7,0 | %22,1 | 3,16 [2,89; 3,46] | +%9,1 | -%7,2 | +%10,0 |  |
| CFP (ALT) | KASA | 20 | %6,8 | %15,5 | 2,28 [2,13; 2,53] | %7,3 | %22,6 | 3,12 [2,50; 3,60] | +%26,6 | -%4,3 | +%16,1 |  |
| CFP (ÜST) — faaliyet nakit akışı (y0, yıllık) / PD | KEŞİF | 120 | %4,1 | %8,7 | 2,11 [1,34; 2,64] | %5,8 | %7,2 | 1,24 [0,68; 2,16] | +%22,2 | +%10,8 | +%14,5 | yol R2 |
| CFP (ÜST) | DOĞRULAMA | 24 | %3,7 | %3,5 | 0,95 [0,85; 1,11] | %7,0 | %5,4 | 0,77 [0,67; 0,88] | +%13,6 | +%9,9 | +%10,0 |  |
| CHS_FAIL (ALT) — Campbell-Hilscher-Szilagyi 12 ay ufuklu batma logiti (katsay | KEŞİF | 120 | %4,1 | %11,1 | 2,70 [2,45; 3,39] | %5,8 | %16,0 | 2,77 [2,55; 3,26] | +%24,0 | +%5,6 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| CHS_FAIL (ALT) | DOĞRULAMA | 24 | %3,7 | %9,0 | 2,45 [2,25; 2,66] | %7,0 | %23,8 | 3,41 [3,25; 3,54] | +%4,7 | -%14,3 | +%10,0 |  |
| CHS_FAIL (ALT) | KASA | 20 | %6,8 | %15,7 | 2,31 [2,21; 2,46] | %7,3 | %20,9 | 2,88 [2,56; 3,16] | +%25,3 | -%5,3 | +%16,1 |  |
| COMP4 (ALT) | KEŞİF | 120 | %4,1 | %7,8 | 1,89 [1,68; 2,43] | %5,8 | %14,3 | 2,49 [2,36; 2,71] | +%15,0 | +%4,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| COMP4 (ALT) | DOĞRULAMA | 24 | %3,7 | %7,7 | 2,09 [1,92; 2,25] | %7,0 | %18,9 | 2,71 [2,62; 2,79] | +%4,5 | -%10,6 | +%10,0 |  |
| COMP4 (ALT) | KASA | 20 | %6,8 | %14,8 | 2,17 [2,08; 2,30] | %7,3 | %17,4 | 2,39 [2,22; 2,56] | +%27,3 | -%0,8 | +%16,1 |  |
| DOLVOL (ÜST) — ln(m-1 ayının ortalama günlük işlem değeri) | KEŞİF | 120 | %4,1 | %6,5 | 1,58 [1,44; 1,90] | %5,8 | %10,3 | 1,78 [1,64; 2,09] | +%14,9 | +%5,9 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| DOLVOL (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,2 | 1,68 [1,53; 1,93] | %7,0 | %12,8 | 1,84 [1,78; 1,92] | +%5,6 | -%4,6 | +%10,0 |  |
| DOLVOL (ÜST) | KASA | 20 | %6,8 | %8,5 | 1,25 [1,15; 1,43] | %7,3 | %15,9 | 2,18 [1,98; 2,42] | +%12,3 | -%1,6 | +%16,1 |  |
| DOSYA_Y (ALT) | KEŞİF | 120 | %4,1 | %7,8 | 1,89 [1,69; 2,24] | %5,8 | %11,4 | 1,98 [1,80; 2,21] | +%17,2 | +%4,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| DOSYA_Y (ALT) | DOĞRULAMA | 24 | %3,7 | %5,7 | 1,54 [1,38; 1,62] | %7,0 | %14,7 | 2,10 [1,90; 2,32] | +%4,1 | -%5,3 | +%10,0 |  |
| DOSYA_Y (ALT) | KASA | 20 | %6,8 | %10,3 | 1,50 [1,30; 1,68] | %7,3 | %16,1 | 2,21 [1,97; 2,42] | +%16,1 | -%3,6 | +%16,1 |  |
| D_ASSET_TURN (ALT) — gelir 4ç(ç0) / varlık(ç0) - gelir 4ç(ç0-4) / varlık(ç0-4) | KEŞİF | 120 | %4,1 | %6,1 | 1,48 [1,14; 1,63] | %5,8 | %7,8 | 1,35 [0,99; 1,60] | +%17,4 | +%9,4 | +%14,5 | yol R2+R2K |
| D_ASSET_TURN (ALT) | DOĞRULAMA | 24 | %3,7 | %4,2 | 1,15 [0,94; 1,46] | %7,0 | %9,3 | 1,33 [1,14; 1,52] | +%10,5 | +%4,2 | +%10,0 |  |
| D_ASSET_TURN (ALT) | KASA | 20 | %6,8 | %7,0 | 1,02 [0,85; 1,13] | %7,3 | %7,9 | 1,09 [0,93; 1,24] | +%12,7 | +%0,7 | +%16,1 |  |
| D_ASSET_TURN (ÜST) — gelir 4ç(ç0) / varlık(ç0) - gelir 4ç(ç0-4) / varlık(ç0-4) | KEŞİF | 120 | %4,1 | %6,4 | 1,55 [1,36; 2,01] | %5,8 | %7,6 | 1,33 [1,22; 1,50] | +%19,7 | +%8,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ |
| D_ASSET_TURN (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,9 | 1,61 [1,06; 1,88] | %7,0 | %6,0 | 0,86 [0,72; 1,04] | +%15,8 | +%8,7 | +%10,0 |  |
| D_ASSET_TURN (ÜST) | KASA | 20 | %6,8 | %10,9 | 1,59 [1,32; 2,13] | %7,3 | %12,3 | 1,70 [1,49; 1,92] | +%20,5 | +%2,8 | +%16,1 |  |
| EARN_STREAK (ALT) — art arda aynı işaretli yıllık net kâr farkı sayısı (ç0'dan g | KEŞİF | 120 | %4,1 | %6,0 | 1,45 [1,34; 1,67] | %5,8 | %10,0 | 1,73 [1,41; 2,01] | +%14,3 | +%8,0 | +%14,5 | yol R2+R2K; K60-KAÇINMA İZİ |
| EARN_STREAK (ALT) | DOĞRULAMA | 24 | %3,7 | %5,3 | 1,44 [1,32; 1,65] | %7,0 | %14,8 | 2,11 [1,91; 2,27] | +%6,1 | -%2,9 | +%10,0 |  |
| EARN_STREAK (ALT) | KASA | 20 | %6,8 | %9,0 | 1,31 [1,00; 1,48] | %7,3 | %9,0 | 1,24 [1,01; 1,41] | +%20,3 | +%2,6 | +%16,1 |  |
| EAR_ANN (ALT) — açıklama günü VEKİLİ d* = 10-Q / 10-K başvuru gününe kadarki | KEŞİF | 120 | %4,1 | %6,9 | 1,67 [1,51; 1,92] | %5,8 | %10,8 | 1,87 [1,66; 2,05] | +%16,1 | +%5,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| EAR_ANN (ALT) | DOĞRULAMA | 24 | %3,7 | %5,8 | 1,57 [1,49; 1,67] | %7,0 | %12,5 | 1,79 [1,58; 2,05] | +%8,1 | -%1,6 | +%10,0 |  |
| EAR_ANN (ALT) | KASA | 20 | %6,8 | %10,5 | 1,54 [1,38; 1,76] | %7,3 | %11,6 | 1,59 [1,49; 1,69] | +%19,4 | -%1,7 | +%16,1 |  |
| EAR_ANN (ÜST) — açıklama günü VEKİLİ d* = 10-Q / 10-K başvuru gününe kadarki | KEŞİF | 120 | %4,1 | %7,0 | 1,70 [1,56; 1,99] | %5,8 | %8,3 | 1,44 [1,25; 1,65] | +%18,3 | +%7,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| EAR_ANN (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,1 | 1,93 [1,70; 2,07] | %7,0 | %13,1 | 1,87 [1,69; 2,07] | +%9,8 | -%2,0 | +%10,0 |  |
| EAR_ANN (ÜST) | KASA | 20 | %6,8 | %11,0 | 1,61 [1,47; 1,85] | %7,3 | %11,7 | 1,61 [1,52; 1,71] | +%19,0 | -%0,5 | +%16,1 |  |
| EAR_FILE (ALT) — EAR_ANN ile aynı, olay günü 10-Q / 10-K başvuru gününün kend | KEŞİF | 120 | %4,1 | %7,1 | 1,73 [1,56; 2,03] | %5,8 | %11,2 | 1,94 [1,78; 2,08] | +%17,2 | +%6,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| EAR_FILE (ALT) | DOĞRULAMA | 24 | %3,7 | %6,3 | 1,70 [1,55; 1,95] | %7,0 | %12,7 | 1,81 [1,61; 2,07] | +%9,1 | -%1,3 | +%10,0 |  |
| EAR_FILE (ALT) | KASA | 20 | %6,8 | %11,1 | 1,62 [1,46; 1,89] | %7,3 | %11,6 | 1,60 [1,44; 1,75] | +%20,8 | -%1,5 | +%16,1 |  |
| EAR_FILE (ÜST) — EAR_ANN ile aynı, olay günü 10-Q / 10-K başvuru gününün kend | KEŞİF | 120 | %4,1 | %7,1 | 1,71 [1,55; 2,03] | %5,8 | %8,8 | 1,53 [1,40; 1,73] | +%18,0 | +%7,9 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| EAR_FILE (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,7 | 1,81 [1,66; 1,91] | %7,0 | %12,8 | 1,83 [1,66; 1,99] | +%8,1 | -%2,2 | +%10,0 |  |
| EAR_FILE (ÜST) | KASA | 20 | %6,8 | %11,4 | 1,67 [1,53; 1,94] | %7,3 | %11,5 | 1,59 [1,54; 1,62] | +%20,4 | +%1,0 | +%16,1 |  |
| EAR_VOL (ALT) — d* günündeki hacim / önceki 50 işlem gününün ortalama hacmi  | KEŞİF | 120 | %4,1 | %4,5 | 1,09 [1,00; 1,34] | %5,8 | %10,0 | 1,74 [1,42; 1,94] | +%11,2 | +%6,1 | +%14,5 | yol R2K; K60-KAÇINMA İZİ |
| EAR_VOL (ALT) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,32 [1,21; 1,42] | %7,0 | %9,4 | 1,35 [1,22; 1,46] | +%9,2 | +%1,7 | +%10,0 |  |
| EAR_VOL (ALT) | KASA | 20 | %6,8 | %8,5 | 1,25 [1,12; 1,43] | %7,3 | %12,5 | 1,72 [1,28; 2,12] | +%17,3 | +%4,7 | +%16,1 |  |
| EAR_VOL (ÜST) — d* günündeki hacim / önceki 50 işlem gününün ortalama hacmi  | KEŞİF | 120 | %4,1 | %5,0 | 1,20 [0,94; 1,32] | %5,8 | %6,6 | 1,15 [1,01; 1,25] | +%15,0 | +%8,9 | +%14,5 | yol R2+R2K; K60-KAÇINMA İZİ |
| EAR_VOL (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,6 | 1,25 [1,18; 1,32] | %7,0 | %7,7 | 1,10 [1,03; 1,17] | +%10,7 | +%4,3 | +%10,0 |  |
| EAR_VOL (ÜST) | KASA | 20 | %6,8 | %7,0 | 1,03 [0,95; 1,17] | %7,3 | %8,8 | 1,22 [1,02; 1,46] | +%12,9 | -%0,3 | +%16,1 |  |
| EP (ALT) — NetIncomeLoss son 4 çeyrek toplamı / PD | KEŞİF | 120 | %4,1 | %11,1 | 2,69 [2,21; 3,69] | %5,8 | %16,4 | 2,84 [2,36; 3,91] | +%22,8 | +%1,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| EP (ALT) | DOĞRULAMA | 24 | %3,7 | %10,4 | 2,82 [2,75; 2,93] | %7,0 | %23,2 | 3,32 [3,00; 3,64] | +%7,2 | -%12,8 | +%10,0 |  |
| EP (ALT) | KASA | 20 | %6,8 | %15,8 | 2,32 [2,23; 2,49] | %7,3 | %21,4 | 2,95 [2,51; 3,30] | +%26,5 | -%5,7 | +%16,1 |  |
| EV_EBITDA (ALT) — (PD + uzun vadeli borç(ç0; yoksa 0) - nakit(ç0; yoksa 0)) /  | KEŞİF | 120 | %4,1 | %6,0 | 1,46 [1,11; 2,10] | %5,8 | %6,3 | 1,10 [0,83; 1,29] | +%19,8 | +%12,6 | +%14,5 | yol R2 |
| EV_EBITDA (ALT) | DOĞRULAMA | 24 | %3,7 | %4,0 | 1,07 [1,00; 1,15] | %7,0 | %7,8 | 1,12 [1,00; 1,26] | +%8,1 | +%2,9 | +%10,0 |  |
| EV_EBITDA (ÜST) — (PD + uzun vadeli borç(ç0; yoksa 0) - nakit(ç0; yoksa 0)) /  | KEŞİF | 120 | %4,1 | %6,2 | 1,52 [1,02; 1,74] | %5,8 | %6,9 | 1,21 [0,59; 2,14] | +%17,0 | +%8,4 | +%14,5 | yol R2 |
| EV_EBITDA (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,4 | 1,18 [0,95; 1,46] | %7,0 | %4,8 | 0,69 [0,57; 0,80] | +%11,6 | +%6,4 | +%10,0 |  |
| E_424B5 (ALT) — son 60 takvim gününde 424B5 | KEŞİF | 120 | %4,1 | %4,2 | 1,02 [0,78; 1,10] | %5,8 | %8,0 | 1,39 [1,01; 1,77] | +%12,5 | +%7,2 | +%14,5 | yol R2K; K60-KAÇINMA İZİ |
| E_424B5 (ALT) | DOĞRULAMA | 24 | %3,7 | %3,4 | 0,91 [0,59; 1,11] | %7,0 | %8,8 | 1,26 [1,10; 1,45] | +%7,0 | +%1,9 | +%10,0 |  |
| E_424B5 (ALT) | KASA | 20 | %6,8 | %7,0 | 1,03 [0,92; 1,11] | %7,3 | %12,3 | 1,69 [1,46; 1,89] | +%16,7 | +%7,3 | +%16,1 |  |
| E_DIV_OMIT (ALT) — (t-730, t-365] aralığında en az 2 temettü var, son 365 günde | KEŞİF | 30 | %4,7 | %8,0 | 1,70 [1,43; 3,43] | %10,4 | %8,1 | 0,78 [0,51; 2,29] | +%22,5 | -%6,8 | +%9,8 | yol R2 |
| E_DIV_OMIT (ALT) | DOĞRULAMA | 0 | — | — | — | — | — | — | — | — | — |  |
| E_IPO_3Y (ALT) — ilk işlem günü (Yahoo) t'den en çok 1095 gün önce | KEŞİF | 120 | %4,1 | %7,9 | 1,93 [1,45; 2,87] | %5,8 | %16,1 | 2,79 [2,25; 3,11] | +%12,7 | +%2,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| E_IPO_3Y (ALT) | DOĞRULAMA | 24 | %3,7 | %6,5 | 1,77 [1,65; 1,87] | %7,0 | %18,6 | 2,66 [2,40; 2,89] | +%2,5 | -%8,7 | +%10,0 |  |
| E_IPO_3Y (ALT) | KASA | 20 | %6,8 | %11,2 | 1,64 [1,44; 2,01] | %7,3 | %14,6 | 2,01 [1,89; 2,10] | +%19,3 | -%0,6 | +%16,1 |  |
| E_RSPLIT (ALT) — son 365 günde ters bölünme (oran < 1) | KEŞİF | 64 | %5,4 | %8,5 | 1,57 [1,23; 2,33] | %7,3 | %31,5 | 4,30 [3,49; 6,64] | +%15,9 | -%20,4 | +%15,4 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| E_RSPLIT (ALT) | DOĞRULAMA | 24 | %3,7 | %6,7 | 1,81 [1,42; 2,43] | %7,0 | %27,5 | 3,95 [3,74; 4,20] | -%1,5 | -%8,4 | +%10,0 |  |
| E_RSPLIT (ALT) | KASA | 20 | %6,8 | %9,2 | 1,35 [1,12; 1,69] | %7,3 | %40,2 | 5,53 [5,05; 5,98] | -%3,9 | -%30,9 | +%16,1 |  |
| E_S3 (ALT) — son 90 takvim gününde S-3 / S-3ASR | KEŞİF | 120 | %4,1 | %4,8 | 1,17 [0,99; 1,35] | %5,8 | %9,0 | 1,56 [1,30; 1,74] | +%13,6 | +%7,9 | +%14,5 | yol R2+R2K; K60-KAÇINMA İZİ |
| E_S3 (ALT) | DOĞRULAMA | 24 | %3,7 | %3,9 | 1,05 [0,96; 1,11] | %7,0 | %10,1 | 1,45 [1,32; 1,59] | +%5,6 | +%1,5 | +%10,0 |  |
| E_S3 (ALT) | KASA | 20 | %6,8 | %8,0 | 1,17 [1,00; 1,36] | %7,3 | %10,9 | 1,50 [1,25; 1,67] | +%17,7 | +%6,7 | +%16,1 |  |
| F_SCORE (ALT) — Piotroski 9 ikili ölçü, yıllık (y0, y0-1): ROA > 0; OCF > 0; | KEŞİF | 120 | %4,1 | %8,4 | 2,04 [1,61; 2,96] | %5,8 | %15,0 | 2,60 [2,12; 3,10] | +%15,7 | +%1,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| F_SCORE (ALT) | DOĞRULAMA | 24 | %3,7 | %9,9 | 2,67 [2,46; 2,91] | %7,0 | %20,2 | 2,90 [2,81; 3,01] | +%10,9 | -%8,0 | +%10,0 |  |
| F_SCORE (ALT) | KASA | 20 | %6,8 | %14,2 | 2,08 [2,02; 2,19] | %7,3 | %20,9 | 2,87 [2,55; 3,14] | +%23,3 | -%5,1 | +%16,1 |  |
| GAP_OVN (ALT) — t'nin takvim ayındaki gece getirilerinin toplamı Σ ln(açılış | KEŞİF | 120 | %4,1 | %5,5 | 1,35 [1,21; 1,68] | %5,8 | %10,3 | 1,80 [1,51; 1,99] | +%13,8 | +%7,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| GAP_OVN (ALT) | DOĞRULAMA | 24 | %3,7 | %5,1 | 1,38 [1,21; 1,71] | %7,0 | %12,9 | 1,85 [1,64; 2,02] | +%6,5 | -%1,0 | +%10,0 |  |
| GAP_OVN (ALT) | KASA | 20 | %6,8 | %9,5 | 1,39 [1,25; 1,54] | %7,3 | %10,9 | 1,49 [1,42; 1,56] | +%17,7 | +%1,9 | +%16,1 |  |
| GAP_OVN (ÜST) — t'nin takvim ayındaki gece getirilerinin toplamı Σ ln(açılış | KEŞİF | 120 | %4,1 | %7,5 | 1,82 [1,67; 2,15] | %5,8 | %12,3 | 2,13 [1,90; 2,47] | +%15,8 | +%3,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| GAP_OVN (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,2 | 1,69 [1,33; 1,94] | %7,0 | %13,4 | 1,92 [1,68; 2,24] | +%8,1 | -%2,7 | +%10,0 |  |
| GAP_OVN (ÜST) | KASA | 20 | %6,8 | %12,9 | 1,88 [1,60; 2,38] | %7,3 | %14,9 | 2,05 [1,82; 2,29] | +%22,1 | +%0,6 | +%16,1 |  |
| GP_A (ALT) — brüt kâr son 4 çeyrek / varlık(ç0); brüt kâr = GrossProfit,  | KEŞİF | 120 | %4,1 | %6,0 | 1,46 [1,18; 1,93] | %5,8 | %12,4 | 2,16 [1,96; 2,53] | +%12,6 | +%5,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| GP_A (ALT) | DOĞRULAMA | 24 | %3,7 | %5,2 | 1,42 [1,15; 1,65] | %7,0 | %19,8 | 2,83 [2,57; 3,11] | -%2,3 | -%10,6 | +%10,0 |  |
| GP_A (ALT) | KASA | 20 | %6,8 | %12,8 | 1,88 [1,50; 2,22] | %7,3 | %13,1 | 1,80 [1,58; 1,99] | +%28,2 | +%2,2 | +%16,1 |  |
| GP_A (ÜST) — brüt kâr son 4 çeyrek / varlık(ç0); brüt kâr = GrossProfit,  | KEŞİF | 120 | %4,1 | %6,1 | 1,49 [1,01; 2,05] | %5,8 | %7,0 | 1,21 [0,91; 1,41] | +%20,4 | +%8,7 | +%14,5 | yol R2+R2K |
| GP_A (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,7 | 1,27 [1,09; 1,38] | %7,0 | %6,0 | 0,86 [0,71; 1,01] | +%8,2 | +%0,2 | +%10,0 |  |
| GP_A (ÜST) | KASA | 20 | %6,8 | %4,7 | 0,69 [0,51; 1,04] | %7,3 | %10,9 | 1,50 [0,96; 2,15] | +%3,5 | -%4,9 | +%16,1 |  |
| HIGH52 (ALT) — C(t) / son 252 işlem gününün en yüksek gün içi fiyatı (en az | KEŞİF | 120 | %4,1 | %10,0 | 2,43 [2,22; 2,99] | %5,8 | %20,0 | 3,47 [3,22; 3,83] | +%13,9 | -%4,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| HIGH52 (ALT) | DOĞRULAMA | 24 | %3,7 | %9,0 | 2,45 [2,17; 2,82] | %7,0 | %23,6 | 3,38 [3,01; 3,69] | +%3,7 | -%16,8 | +%10,0 |  |
| HIGH52 (ALT) | KASA | 20 | %6,8 | %15,3 | 2,24 [2,05; 2,58] | %7,3 | %20,3 | 2,79 [2,67; 2,91] | +%26,1 | -%2,9 | +%16,1 |  |
| IND_LEAD_BIG (ALT) — aynı SIC 2 hane sektöründe (PD'si olan en az 10 uygun hisse) | KEŞİF | 120 | %4,1 | %5,0 | 1,21 [0,95; 1,37] | %5,8 | %8,4 | 1,46 [1,28; 1,69] | +%13,5 | +%8,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ |
| IND_LEAD_BIG (ALT) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,33 [1,12; 1,51] | %7,0 | %9,5 | 1,36 [1,02; 1,66] | +%9,4 | +%2,0 | +%10,0 |  |
| IND_LEAD_BIG (ALT) | KASA | 20 | %6,8 | %10,5 | 1,54 [1,13; 1,92] | %7,3 | %7,4 | 1,02 [0,95; 1,08] | +%23,5 | +%5,1 | +%16,1 |  |
| IND_LEAD_BIG (ÜST) — aynı SIC 2 hane sektöründe (PD'si olan en az 10 uygun hisse) | KEŞİF | 120 | %4,1 | %6,0 | 1,46 [1,09; 1,73] | %5,8 | %6,3 | 1,10 [0,96; 1,32] | +%18,4 | +%9,6 | +%14,5 | yol R2 |
| IND_LEAD_BIG (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,5 | 1,21 [0,85; 1,46] | %7,0 | %7,3 | 1,05 [0,77; 1,38] | +%9,7 | +%2,6 | +%10,0 |  |
| IND_MOM_6 (ALT) — aynı SIC 2 hane sektöründeki uygun hisselerin (en az 5) A(m) | KEŞİF | 120 | %4,1 | %4,9 | 1,18 [0,73; 1,43] | %5,8 | %8,2 | 1,43 [0,90; 2,14] | +%13,9 | +%8,7 | +%14,5 | yol R2K |
| IND_MOM_6 (ALT) | DOĞRULAMA | 24 | %3,7 | %4,2 | 1,14 [1,01; 1,34] | %7,0 | %8,8 | 1,26 [0,57; 1,85] | +%10,9 | +%5,5 | +%10,0 |  |
| IND_MOM_6 (ALT) | KASA | 20 | %6,8 | %7,1 | 1,04 [0,82; 1,25] | %7,3 | %5,4 | 0,74 [0,70; 0,78] | +%16,0 | +%4,5 | +%16,1 |  |
| IND_MOM_6 (ÜST) — aynı SIC 2 hane sektöründeki uygun hisselerin (en az 5) A(m) | KEŞİF | 120 | %4,1 | %5,9 | 1,42 [1,13; 2,10] | %5,8 | %7,7 | 1,34 [1,04; 1,91] | +%15,4 | +%8,8 | +%14,5 | yol R2+R2K |
| IND_MOM_6 (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,32 [0,91; 1,59] | %7,0 | %4,1 | 0,59 [0,36; 0,90] | +%15,7 | +%7,0 | +%10,0 |  |
| ISKEW (ALT) — IVOL_FF3 artıklarının çarpıklığı | KEŞİF | 120 | %4,1 | %4,8 | 1,17 [1,11; 1,30] | %5,8 | %7,9 | 1,37 [1,19; 1,52] | +%14,3 | +%8,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ISKEW (ALT) | DOĞRULAMA | 24 | %3,7 | %4,6 | 1,25 [1,20; 1,29] | %7,0 | %8,8 | 1,26 [1,23; 1,29] | +%10,1 | +%3,3 | +%10,0 |  |
| ISKEW (ALT) | KASA | 20 | %6,8 | %8,1 | 1,18 [1,10; 1,29] | %7,3 | %10,2 | 1,40 [1,31; 1,49] | +%14,9 | +%2,4 | +%16,1 |  |
| IVOL_FF3 (ALT) — t'nin takvim ayındaki günlük fazla getirinin French günlük M | KEŞİF | 120 | %4,1 | %10,3 | 2,49 [2,10; 3,34] | %5,8 | %19,6 | 3,40 [3,06; 3,97] | +%16,0 | -%5,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| IVOL_FF3 (ALT) | DOĞRULAMA | 24 | %3,7 | %9,2 | 2,49 [2,45; 2,57] | %7,0 | %22,7 | 3,26 [3,10; 3,46] | +%5,0 | -%14,2 | +%10,0 |  |
| IVOL_FF3 (ALT) | KASA | 20 | %6,8 | %14,4 | 2,10 [1,72; 2,77] | %7,3 | %23,6 | 3,25 [2,90; 3,59] | +%19,6 | -%8,6 | +%16,1 |  |
| LEV_MKT (ALT) — toplam yükümlülük(ç0) / PD | KEŞİF | 120 | %4,1 | %6,4 | 1,56 [1,13; 2,48] | %5,8 | %13,6 | 2,36 [1,67; 2,83] | +%11,1 | +%3,6 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| LEV_MKT (ALT) | DOĞRULAMA | 24 | %3,7 | %5,6 | 1,51 [1,39; 1,69] | %7,0 | %13,1 | 1,88 [1,79; 1,97] | +%6,4 | -%2,9 | +%10,0 |  |
| LEV_MKT (ALT) | KASA | 20 | %6,8 | %10,0 | 1,47 [1,38; 1,59] | %7,3 | %13,2 | 1,81 [1,65; 2,00] | +%17,6 | -%2,9 | +%16,1 |  |
| LTREV_60_13 (ÜST) — A(m-12) / A(m-60) - 1 | KEŞİF | 84 | %4,6 | %9,9 | 2,14 [1,82; 3,12] | %6,8 | %16,0 | 2,34 [2,03; 2,95] | +%20,0 | -%3,9 | +%13,3 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| LTREV_60_13 (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,1 | 1,91 [1,77; 2,02] | %7,0 | %10,2 | 1,47 [1,30; 1,66] | +%12,0 | +%0,9 | +%10,0 |  |
| LTREV_60_13 (ÜST) | KASA | 20 | %6,8 | %10,5 | 1,54 [1,46; 1,65] | %7,3 | %16,7 | 2,30 [2,16; 2,44] | +%14,7 | -%5,0 | +%16,1 |  |
| MAX5 (ALT) — t'nin takvim ayındaki en yüksek 5 günlük getirinin ortalamas | KEŞİF | 120 | %4,1 | %10,8 | 2,62 [2,27; 3,41] | %5,8 | %18,6 | 3,23 [2,93; 3,81] | +%16,7 | -%4,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| MAX5 (ALT) | DOĞRULAMA | 24 | %3,7 | %8,7 | 2,35 [2,22; 2,43] | %7,0 | %23,6 | 3,38 [3,31; 3,47] | +%3,2 | -%15,8 | +%10,0 |  |
| MAX5 (ALT) | KASA | 20 | %6,8 | %15,5 | 2,27 [1,87; 2,94] | %7,3 | %22,8 | 3,14 [2,81; 3,42] | +%24,5 | -%8,2 | +%16,1 |  |
| MOM_12_1 (ALT) — A(m-1) / A(m-12) - 1 | KEŞİF | 120 | %4,1 | %8,9 | 2,16 [1,89; 2,59] | %5,8 | %13,8 | 2,40 [2,04; 2,93] | +%18,1 | +%3,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| MOM_12_1 (ALT) | DOĞRULAMA | 24 | %3,7 | %7,8 | 2,11 [1,72; 2,61] | %7,0 | %21,4 | 3,07 [2,67; 3,41] | +%3,5 | -%14,3 | +%10,0 |  |
| MOM_12_1 (ALT) | KASA | 20 | %6,8 | %13,0 | 1,90 [1,85; 1,99] | %7,3 | %16,5 | 2,27 [2,14; 2,37] | +%21,3 | -%1,7 | +%16,1 |  |
| MOM_12_1 (ÜST) — A(m-1) / A(m-12) - 1 | KEŞİF | 120 | %4,1 | %7,4 | 1,79 [1,45; 2,51] | %5,8 | %11,8 | 2,05 [1,52; 2,51] | +%14,2 | +%4,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ |
| MOM_12_1 (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,5 | 2,03 [1,49; 2,38] | %7,0 | %7,0 | 1,01 [0,77; 1,32] | +%16,8 | +%4,4 | +%10,0 |  |
| MOM_12_1 (ÜST) | KASA | 20 | %6,8 | %12,9 | 1,90 [1,50; 2,57] | %7,3 | %14,7 | 2,02 [1,79; 2,23] | +%22,9 | +%1,3 | +%16,1 |  |
| MOM_6_1 (ALT) — A(m-1) / A(m-6) - 1 | KEŞİF | 120 | %4,1 | %8,3 | 2,01 [1,77; 2,39] | %5,8 | %14,6 | 2,54 [2,30; 2,83] | +%15,5 | +%4,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| MOM_6_1 (ALT) | DOĞRULAMA | 24 | %3,7 | %7,5 | 2,02 [1,85; 2,27] | %7,0 | %20,6 | 2,95 [2,54; 3,31] | +%4,5 | -%11,6 | +%10,0 |  |
| MOM_6_1 (ALT) | KASA | 20 | %6,8 | %13,2 | 1,94 [1,84; 2,04] | %7,3 | %15,5 | 2,13 [1,97; 2,29] | +%23,9 | +%0,6 | +%16,1 |  |
| MOM_6_1 (ÜST) — A(m-1) / A(m-6) - 1 | KEŞİF | 120 | %4,1 | %7,8 | 1,88 [1,51; 2,67] | %5,8 | %11,2 | 1,94 [1,56; 2,36] | +%16,1 | +%4,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| MOM_6_1 (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,3 | 1,98 [1,61; 2,19] | %7,0 | %10,1 | 1,44 [1,11; 1,80] | +%13,2 | +%1,4 | +%10,0 |  |
| MOM_6_1 (ÜST) | KASA | 20 | %6,8 | %12,2 | 1,78 [1,36; 2,55] | %7,3 | %15,9 | 2,19 [1,73; 2,62] | +%19,8 | -%1,0 | +%16,1 |  |
| MOM_FIP (ALT) — ay içi yüzdelik sıra ortalaması: MOM_12_1 ve süreklilik = iş | KEŞİF | 120 | %4,1 | %4,8 | 1,16 [1,02; 1,23] | %5,8 | %8,2 | 1,43 [1,22; 1,61] | +%14,0 | +%9,0 | +%14,5 | yol R2+R2K |
| MOM_FIP (ALT) | DOĞRULAMA | 24 | %3,7 | %3,6 | 0,97 [0,84; 1,14] | %7,0 | %8,9 | 1,27 [1,23; 1,31] | +%8,0 | +%3,7 | +%10,0 |  |
| MOM_FIP (ALT) | KASA | 20 | %6,8 | %6,8 | 1,00 [0,83; 1,10] | %7,3 | %7,3 | 1,00 [0,83; 1,16] | +%15,4 | +%2,3 | +%16,1 |  |
| MOM_INT_12_7 (ALT) — A(m-6) / A(m-12) - 1 (t-12 .. t-7 ayları) | KEŞİF | 120 | %4,1 | %8,5 | 2,06 [1,86; 2,46] | %5,8 | %12,1 | 2,10 [1,79; 2,63] | +%18,7 | +%4,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| MOM_INT_12_7 (ALT) | DOĞRULAMA | 24 | %3,7 | %7,5 | 2,03 [1,67; 2,50] | %7,0 | %19,7 | 2,83 [2,54; 3,04] | +%4,3 | -%11,7 | +%10,0 |  |
| MOM_INT_12_7 (ALT) | KASA | 20 | %6,8 | %12,5 | 1,83 [1,62; 2,21] | %7,3 | %18,2 | 2,51 [2,32; 2,65] | +%20,0 | -%4,0 | +%16,1 |  |
| MOM_INT_12_7 (ÜST) — A(m-6) / A(m-12) - 1 (t-12 .. t-7 ayları) | KEŞİF | 120 | %4,1 | %7,0 | 1,69 [1,41; 2,30] | %5,8 | %11,8 | 2,05 [1,55; 2,40] | +%13,7 | +%4,1 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ |
| MOM_INT_12_7 (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,1 | 1,93 [1,22; 2,40] | %7,0 | %8,4 | 1,21 [0,96; 1,48] | +%15,1 | +%3,7 | +%10,0 |  |
| MOM_INT_12_7 (ÜST) | KASA | 20 | %6,8 | %13,4 | 1,96 [1,74; 2,29] | %7,3 | %12,5 | 1,72 [1,62; 1,84] | +%27,8 | +%4,7 | +%16,1 |  |
| NDF_BS (ALT) — (uzun vadeli borç(ç0) - (ç0-4)) / [varlık(ç0) + varlık(ç0-4) | KEŞİF | 120 | %4,1 | %4,8 | 1,15 [1,03; 1,32] | %5,8 | %5,9 | 1,03 [0,89; 1,24] | +%17,3 | +%11,7 | +%14,5 | yol R2; K60-OLASILIK İZİ |
| NDF_BS (ALT) | DOĞRULAMA | 24 | %3,7 | %5,1 | 1,39 [1,29; 1,51] | %7,0 | %7,0 | 1,01 [0,92; 1,08] | +%13,2 | +%5,0 | +%10,0 |  |
| NDF_BS (ALT) | KASA | 20 | %6,8 | %8,5 | 1,25 [1,11; 1,45] | %7,3 | %7,4 | 1,02 [0,97; 1,07] | +%20,4 | +%2,0 | +%16,1 |  |
| NDF_BS (ÜST) — (uzun vadeli borç(ç0) - (ç0-4)) / [varlık(ç0) + varlık(ç0-4) | KEŞİF | 120 | %4,1 | %5,2 | 1,27 [0,98; 1,52] | %5,8 | %5,2 | 0,91 [0,76; 1,21] | +%19,1 | +%10,7 | +%14,5 | yol R2; K60-OLASILIK İZİ |
| NDF_BS (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,5 | 1,23 [1,17; 1,31] | %7,0 | %5,0 | 0,72 [0,63; 0,83] | +%12,7 | +%5,1 | +%10,0 |  |
| NDF_BS (ÜST) | KASA | 20 | %6,8 | %7,9 | 1,15 [1,08; 1,20] | %7,3 | %7,2 | 0,99 [0,91; 1,09] | +%15,7 | +%1,8 | +%16,1 |  |
| NEF (ALT) — (hisse ihracı geliri - geri alım - temettü) (y0; olmayan kal | KEŞİF | 120 | %4,1 | %6,3 | 1,52 [1,20; 2,07] | %5,8 | %15,1 | 2,63 [2,01; 3,02] | +%11,3 | +%1,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| NEF (ALT) | DOĞRULAMA | 24 | %3,7 | %6,7 | 1,82 [1,59; 1,95] | %7,0 | %16,8 | 2,40 [2,13; 2,62] | +%5,3 | -%6,0 | +%10,0 |  |
| NEF (ALT) | KASA | 20 | %6,8 | %13,2 | 1,94 [1,65; 2,44] | %7,3 | %14,7 | 2,02 [1,88; 2,13] | +%25,5 | +%3,6 | +%16,1 |  |
| NEF (ÜST) — (hisse ihracı geliri - geri alım - temettü) (y0; olmayan kal | KEŞİF | 120 | %4,1 | %2,8 | 0,67 [0,47; 0,76] | %5,8 | %2,0 | 0,35 [0,27; 0,41] | +%16,9 | +%13,6 | +%14,5 | yol R1 |
| NEF (ÜST) | DOĞRULAMA | 24 | %3,7 | %2,6 | 0,70 [0,61; 0,81] | %7,0 | %3,3 | 0,47 [0,38; 0,59] | +%14,6 | +%11,6 | +%10,0 |  |
| NEF (ÜST) | KASA | 20 | %6,8 | %3,2 | 0,46 [0,41; 0,55] | %7,3 | %4,1 | 0,57 [0,48; 0,66] | +%9,2 | +%1,9 | +%16,1 |  |
| NET_PAYOUT_YLD (ALT) — (temettü + geri alım - hisse ihracı geliri) (y0, yıllık; olm | KEŞİF | 120 | %4,1 | %5,9 | 1,43 [1,15; 1,92] | %5,8 | %13,6 | 2,36 [2,04; 2,58] | +%11,7 | +%2,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| NET_PAYOUT_YLD (ALT) | DOĞRULAMA | 24 | %3,7 | %6,4 | 1,74 [1,59; 1,82] | %7,0 | %16,0 | 2,29 [2,00; 2,53] | +%4,4 | -%5,2 | +%10,0 |  |
| NET_PAYOUT_YLD (ALT) | KASA | 20 | %6,8 | %12,3 | 1,81 [1,54; 2,23] | %7,3 | %14,2 | 1,96 [1,73; 2,16] | +%23,2 | +%4,5 | +%16,1 |  |
| NOA (ALT) — (uzun vadeli borç(ç0; yoksa 0) + özkaynak(ç0) - nakit(ç0)) / | KEŞİF | 120 | %4,1 | %3,9 | 0,94 [0,83; 1,04] | %5,8 | %9,3 | 1,62 [1,42; 1,78] | +%10,6 | +%7,4 | +%14,5 | yol R2K |
| NOA (ALT) | DOĞRULAMA | 24 | %3,7 | %4,2 | 1,15 [1,05; 1,30] | %7,0 | %9,3 | 1,34 [0,83; 1,75] | +%9,2 | +%3,1 | +%10,0 |  |
| NOA (ALT) | KASA | 20 | %6,8 | %7,2 | 1,06 [0,84; 1,19] | %7,3 | %7,7 | 1,06 [0,99; 1,13] | +%18,1 | +%3,4 | +%16,1 |  |
| NOA (ÜST) — (uzun vadeli borç(ç0; yoksa 0) + özkaynak(ç0) - nakit(ç0)) / | KEŞİF | 120 | %4,1 | %6,1 | 1,49 [1,27; 1,98] | %5,8 | %10,4 | 1,81 [1,39; 2,13] | +%16,9 | +%8,3 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| NOA (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,0 | 1,63 [1,53; 1,77] | %7,0 | %13,3 | 1,90 [1,83; 1,97] | +%10,8 | +%2,9 | +%10,0 |  |
| NOA (ÜST) | KASA | 20 | %6,8 | %10,1 | 1,48 [1,18; 2,06] | %7,3 | %12,9 | 1,77 [1,62; 1,92] | +%19,8 | +%6,4 | +%16,1 |  |
| NSI_1Y (ALT) — ln(pay(t) / pay(t - 12 ay)); pay bölünme düzeltmeli, iki uç  | KEŞİF | 120 | %4,1 | %6,7 | 1,62 [1,40; 2,11] | %5,8 | %15,2 | 2,64 [2,27; 2,99] | +%11,2 | +%1,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| NSI_1Y (ALT) | DOĞRULAMA | 24 | %3,7 | %6,7 | 1,81 [1,51; 2,03] | %7,0 | %15,3 | 2,19 [2,12; 2,26] | +%6,7 | -%4,5 | +%10,0 |  |
| NSI_1Y (ALT) | KASA | 20 | %6,8 | %13,1 | 1,92 [1,66; 2,24] | %7,3 | %17,1 | 2,35 [2,00; 2,64] | +%25,3 | +%2,8 | +%16,1 |  |
| NSI_5Y (ALT) — ln(pay(t) / pay(t - 60 ay)); oran > 20 ya da < 1/20 ise veri | KEŞİF | 84 | %4,6 | %6,8 | 1,46 [1,25; 1,83] | %6,8 | %15,0 | 2,19 [1,87; 2,52] | +%12,5 | -%0,0 | +%13,3 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| NSI_5Y (ALT) | DOĞRULAMA | 24 | %3,7 | %5,1 | 1,39 [1,17; 1,55] | %7,0 | %14,4 | 2,06 [2,01; 2,13] | +%3,6 | -%6,1 | +%10,0 |  |
| NSI_5Y (ALT) | KASA | 20 | %6,8 | %10,9 | 1,59 [1,52; 1,64] | %7,3 | %13,7 | 1,88 [1,59; 2,14] | +%20,9 | +%3,4 | +%16,1 |  |
| NT_LATE (ALT) — son 60 takvim gününde (t hariç) NT 10-K / NT 10-Q başvurusu | KEŞİF | 47 | %5,0 | %5,8 | 1,16 [0,72; 1,41] | %7,6 | %20,8 | 2,74 [2,33; 3,19] | +%2,8 | -%5,8 | +%13,0 | yol R2K; K60-KAÇINMA İZİ |
| NT_LATE (ALT) | DOĞRULAMA | 16 | %3,9 | %5,8 | 1,50 [0,97; 1,94] | %6,6 | %16,6 | 2,49 [2,02; 2,82] | +%10,2 | -%2,7 | +%11,7 |  |
| NT_LATE (ALT) | KASA | 13 | %7,0 | %8,4 | 1,20 [0,99; 1,42] | %7,3 | %19,2 | 2,62 [2,36; 2,89] | +%5,2 | -%6,4 | +%16,7 |  |
| OPLEV (ÜST) — (gelir 4ç - OperatingIncomeLoss 4ç) / varlık(ç0) (toplam faa | KEŞİF | 120 | %4,1 | %5,8 | 1,42 [1,18; 1,63] | %5,8 | %6,1 | 1,06 [0,98; 1,15] | +%22,3 | +%10,6 | +%14,5 | yol R2 |
| OPLEV (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,8 | 1,56 [1,23; 1,78] | %7,0 | %6,9 | 0,99 [0,73; 1,31] | +%15,9 | +%8,6 | +%10,0 |  |
| OPLEV (ÜST) | KASA | 20 | %6,8 | %6,9 | 1,01 [0,83; 1,34] | %7,3 | %11,4 | 1,57 [1,36; 1,83] | +%10,1 | -%0,4 | +%16,1 |  |
| OP_BE (ALT) — OperatingIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); ö | KEŞİF | 120 | %4,1 | %10,1 | 2,45 [1,80; 3,86] | %5,8 | %18,9 | 3,28 [2,81; 4,13] | +%16,8 | -%2,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| OP_BE (ALT) | DOĞRULAMA | 24 | %3,7 | %9,1 | 2,45 [2,28; 2,56] | %7,0 | %23,9 | 3,43 [3,36; 3,51] | +%4,0 | -%15,3 | +%10,0 |  |
| OP_BE (ALT) | KASA | 20 | %6,8 | %15,4 | 2,25 [1,96; 2,77] | %7,3 | %24,1 | 3,32 [3,11; 3,50] | +%23,7 | -%8,9 | +%16,1 |  |
| O_SCORE (ALT) — Ohlson (1980) batma puanı, yıllık (y0, y0-1); FFO yerine faa | KEŞİF | 120 | %4,1 | %10,0 | 2,43 [1,71; 3,88] | %5,8 | %20,3 | 3,52 [2,75; 4,15] | +%18,7 | -%1,3 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| O_SCORE (ALT) | DOĞRULAMA | 24 | %3,7 | %9,2 | 2,48 [2,24; 2,72] | %7,0 | %23,6 | 3,39 [3,19; 3,61] | +%5,9 | -%12,8 | +%10,0 |  |
| O_SCORE (ALT) | KASA | 20 | %6,8 | %14,0 | 2,05 [1,77; 2,56] | %7,3 | %24,7 | 3,41 [3,25; 3,55] | +%17,6 | -%10,5 | +%16,1 |  |
| PRICE_LVL (ÜST) — ln(o günkü fiyat) (ölçü yüksek = pahalı; beklenen yön düşük  | KEŞİF | 120 | %4,1 | %10,2 | 2,47 [2,15; 3,30] | %5,8 | %17,9 | 3,11 [2,89; 3,63] | +%18,6 | -%2,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| PRICE_LVL (ÜST) | DOĞRULAMA | 24 | %3,7 | %8,0 | 2,18 [1,99; 2,37] | %7,0 | %23,0 | 3,30 [3,24; 3,37] | +%2,9 | -%13,4 | +%10,0 |  |
| PRICE_LVL (ÜST) | KASA | 20 | %6,8 | %15,2 | 2,23 [1,99; 2,66] | %7,3 | %20,0 | 2,75 [2,71; 2,80] | +%25,2 | -%3,5 | +%16,1 |  |
| RD_ME (ALT) — ResearchAndDevelopmentExpense son 4 çeyrek / PD; yalnız Ar-G | KEŞİF | 120 | %4,1 | %3,1 | 0,75 [0,44; 0,98] | %5,8 | %9,5 | 1,64 [1,21; 1,98] | +%9,8 | +%7,1 | +%14,5 | yol R2K |
| RD_ME (ALT) | DOĞRULAMA | 24 | %3,7 | %2,7 | 0,74 [0,19; 1,10] | %7,0 | %8,3 | 1,20 [1,05; 1,39] | +%3,5 | +%0,6 | +%10,0 |  |
| RD_ME (ALT) | KASA | 20 | %6,8 | %7,3 | 1,07 [0,92; 1,17] | %7,3 | %7,9 | 1,09 [0,91; 1,27] | +%17,4 | +%5,2 | +%16,1 |  |
| RD_ME (ÜST) — ResearchAndDevelopmentExpense son 4 çeyrek / PD; yalnız Ar-G | KEŞİF | 120 | %4,1 | %10,7 | 2,59 [1,77; 4,36] | %5,8 | %19,8 | 3,43 [2,79; 4,20] | +%19,4 | -%4,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| RD_ME (ÜST) | DOĞRULAMA | 24 | %3,7 | %12,5 | 3,38 [3,22; 3,58] | %7,0 | %24,8 | 3,56 [3,05; 4,08] | +%13,5 | -%12,9 | +%10,0 |  |
| RD_ME (ÜST) | KASA | 20 | %6,8 | %15,8 | 2,32 [2,14; 2,59] | %7,3 | %26,2 | 3,61 [2,31; 4,63] | +%27,0 | -%10,6 | +%16,1 |  |
| REV_SURP (ALT) — SUE_SRW'nin gelirle hesaplanmışı | KEŞİF | 119 | %4,1 | %4,9 | 1,19 [0,89; 1,38] | %5,8 | %5,8 | 1,00 [0,75; 1,24] | +%19,4 | +%10,1 | +%14,4 | yol R2 |
| REV_SURP (ALT) | DOĞRULAMA | 24 | %3,7 | %3,2 | 0,86 [0,76; 0,92] | %7,0 | %8,3 | 1,20 [1,07; 1,34] | +%7,2 | +%4,2 | +%10,0 |  |
| REV_SURP (ALT) | KASA | 20 | %6,8 | %5,9 | 0,86 [0,62; 0,99] | %7,3 | %8,5 | 1,17 [1,02; 1,31] | +%10,1 | +%2,1 | +%16,1 |  |
| REV_SURP (ÜST) — SUE_SRW'nin gelirle hesaplanmışı | KEŞİF | 119 | %4,1 | %3,3 | 0,79 [0,52; 1,12] | %5,8 | %4,9 | 0,85 [0,35; 1,18] | +%15,9 | +%13,1 | +%14,4 | yol R1 |
| REV_SURP (ÜST) | DOĞRULAMA | 24 | %3,7 | %3,3 | 0,90 [0,61; 1,06] | %7,0 | %5,3 | 0,76 [0,58; 0,93] | +%11,6 | +%6,3 | +%10,0 |  |
| ROA_Q (ALT) — NetIncomeLoss(ç0) / toplam varlık(ç0-1) | KEŞİF | 120 | %4,1 | %10,1 | 2,44 [1,83; 3,76] | %5,8 | %19,7 | 3,42 [2,86; 4,05] | +%15,8 | -%1,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ROA_Q (ALT) | DOĞRULAMA | 24 | %3,7 | %8,7 | 2,36 [2,08; 2,59] | %7,0 | %25,4 | 3,63 [3,50; 3,78] | +%2,3 | -%17,9 | +%10,0 |  |
| ROA_Q (ALT) | KASA | 20 | %6,8 | %16,4 | 2,41 [2,26; 2,64] | %7,3 | %23,9 | 3,29 [2,85; 3,66] | +%29,4 | -%6,5 | +%16,1 |  |
| ROE_TTM (ALT) — NetIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); özkayna | KEŞİF | 120 | %4,1 | %10,2 | 2,48 [1,92; 3,67] | %5,8 | %17,6 | 3,06 [2,64; 3,74] | +%18,1 | +%0,3 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| ROE_TTM (ALT) | DOĞRULAMA | 24 | %3,7 | %9,1 | 2,47 [2,35; 2,61] | %7,0 | %22,5 | 3,22 [3,17; 3,30] | +%4,7 | -%13,3 | +%10,0 |  |
| ROE_TTM (ALT) | KASA | 20 | %6,8 | %14,8 | 2,16 [1,94; 2,54] | %7,3 | %22,5 | 3,10 [2,81; 3,33] | +%23,3 | -%6,8 | +%16,1 |  |
| RUNWAY (ALT) — nakit tüketim hızı = -faaliyet nakit akışı(y0) / nakit(ç0);  | KEŞİF | 120 | %4,1 | %9,0 | 2,19 [1,63; 3,44] | %5,8 | %17,0 | 2,95 [2,45; 3,45] | +%17,6 | -%0,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| RUNWAY (ALT) | DOĞRULAMA | 24 | %3,7 | %9,6 | 2,61 [2,46; 2,79] | %7,0 | %22,6 | 3,24 [2,96; 3,56] | +%9,0 | -%10,4 | +%10,0 |  |
| RUNWAY (ALT) | KASA | 20 | %6,8 | %15,8 | 2,32 [2,16; 2,63] | %7,3 | %22,6 | 3,11 [2,59; 3,53] | +%27,1 | -%5,5 | +%16,1 |  |
| SALES_ACCEL (ALT) — gelir(ç0) / [gelir(ç0-1) + gelir(ç0-2)] / 2; payda > 0 (K59  | KEŞİF | 120 | %4,1 | %6,4 | 1,56 [1,35; 1,70] | %5,8 | %8,5 | 1,48 [1,38; 1,65] | +%17,5 | +%6,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SALES_ACCEL (ALT) | DOĞRULAMA | 24 | %3,7 | %4,5 | 1,21 [1,15; 1,26] | %7,0 | %11,1 | 1,60 [1,39; 1,81] | +%6,2 | -%0,0 | +%10,0 |  |
| SALES_ACCEL (ALT) | KASA | 20 | %6,8 | %8,5 | 1,25 [1,14; 1,37] | %7,3 | %12,2 | 1,67 [1,36; 1,95] | +%16,3 | +%3,7 | +%16,1 |  |
| SALES_ACCEL (ÜST) — gelir(ç0) / [gelir(ç0-1) + gelir(ç0-2)] / 2; payda > 0 (K59  | KEŞİF | 120 | %4,1 | %6,1 | 1,47 [1,27; 1,75] | %5,8 | %9,3 | 1,62 [1,46; 1,79] | +%16,9 | +%6,9 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SALES_ACCEL (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,0 | 1,62 [1,50; 1,73] | %7,0 | %11,6 | 1,67 [1,54; 1,81] | +%7,7 | -%1,2 | +%10,0 |  |
| SALES_ACCEL (ÜST) | KASA | 20 | %6,8 | %8,7 | 1,28 [1,12; 1,44] | %7,3 | %10,1 | 1,39 [1,28; 1,51] | +%20,5 | +%5,1 | +%16,1 |  |
| SEAS_1 (ALT) — m-11 ayının getirisi (gelecek ayla aynı takvim ayı, bir yıl  | KEŞİF | 120 | %4,1 | %7,3 | 1,76 [1,58; 2,15] | %5,8 | %10,7 | 1,86 [1,72; 2,21] | +%16,7 | +%4,5 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SEAS_1 (ALT) | DOĞRULAMA | 24 | %3,7 | %6,8 | 1,85 [1,60; 2,08] | %7,0 | %15,9 | 2,28 [2,06; 2,45] | +%6,2 | -%6,1 | +%10,0 |  |
| SEAS_1 (ALT) | KASA | 20 | %6,8 | %11,2 | 1,65 [1,51; 1,89] | %7,3 | %15,9 | 2,19 [2,06; 2,31] | +%19,3 | -%2,4 | +%16,1 |  |
| SEAS_1 (ÜST) — m-11 ayının getirisi (gelecek ayla aynı takvim ayı, bir yıl  | KEŞİF | 120 | %4,1 | %6,7 | 1,63 [1,48; 1,95] | %5,8 | %11,5 | 1,99 [1,74; 2,15] | +%13,8 | +%4,8 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SEAS_1 (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,4 | 1,47 [1,19; 1,68] | %7,0 | %10,8 | 1,55 [1,41; 1,73] | +%8,4 | +%0,4 | +%10,0 |  |
| SEAS_1 (ÜST) | KASA | 20 | %6,8 | %12,3 | 1,81 [1,67; 1,98] | %7,3 | %11,2 | 1,54 [1,46; 1,62] | +%26,1 | +%4,2 | +%16,1 |  |
| SEAS_2_5 (ALT) — m-23, m-35, m-47, m-59 aylarının getiri ortalaması (dördü de | KEŞİF | 84 | %4,6 | %6,8 | 1,46 [1,38; 1,57] | %6,8 | %12,3 | 1,79 [1,70; 1,95] | +%13,4 | +%1,4 | +%13,3 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SEAS_2_5 (ALT) | DOĞRULAMA | 24 | %3,7 | %5,3 | 1,43 [1,21; 1,64] | %7,0 | %9,0 | 1,29 [1,23; 1,37] | +%9,3 | +%0,6 | +%10,0 |  |
| SEAS_2_5 (ALT) | KASA | 20 | %6,8 | %9,5 | 1,40 [1,31; 1,47] | %7,3 | %11,3 | 1,56 [1,42; 1,68] | +%18,0 | +%2,3 | +%16,1 |  |
| SEAS_2_5 (ÜST) — m-23, m-35, m-47, m-59 aylarının getiri ortalaması (dördü de | KEŞİF | 84 | %4,6 | %6,7 | 1,44 [1,33; 1,72] | %6,8 | %9,4 | 1,38 [1,28; 1,55] | +%14,6 | +%3,4 | +%13,3 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SEAS_2_5 (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,32 [1,19; 1,46] | %7,0 | %10,1 | 1,45 [1,40; 1,51] | +%9,2 | +%0,7 | +%10,0 |  |
| SEAS_2_5 (ÜST) | KASA | 20 | %6,8 | %10,4 | 1,53 [1,35; 1,65] | %7,3 | %9,7 | 1,34 [1,25; 1,42] | +%21,3 | +%3,2 | +%16,1 |  |
| SIZE_ME (ÜST) — ln(PD) | KEŞİF | 120 | %4,1 | %9,3 | 2,25 [1,98; 2,83] | %5,8 | %17,0 | 2,94 [2,65; 3,52] | +%17,3 | -%0,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SIZE_ME (ÜST) | DOĞRULAMA | 24 | %3,7 | %7,8 | 2,11 [2,00; 2,23] | %7,0 | %18,6 | 2,67 [2,61; 2,75] | +%5,1 | -%9,8 | +%10,0 |  |
| SIZE_ME (ÜST) | KASA | 20 | %6,8 | %11,0 | 1,61 [1,41; 1,97] | %7,3 | %20,5 | 2,82 [2,71; 2,94] | +%14,0 | -%8,0 | +%16,1 |  |
| SKEW_TOT (ALT) — t'nin takvim ayındaki günlük getirilerin çarpıklığı (en az 1 | KEŞİF | 120 | %4,1 | %5,2 | 1,26 [1,15; 1,37] | %5,8 | %8,3 | 1,44 [1,28; 1,57] | +%15,2 | +%7,6 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SKEW_TOT (ALT) | DOĞRULAMA | 24 | %3,7 | %4,5 | 1,22 [1,08; 1,32] | %7,0 | %10,3 | 1,48 [1,37; 1,57] | +%8,5 | +%2,0 | +%10,0 |  |
| SKEW_TOT (ALT) | KASA | 20 | %6,8 | %7,4 | 1,09 [1,01; 1,22] | %7,3 | %11,6 | 1,59 [1,49; 1,72] | +%13,1 | -%0,2 | +%16,1 |  |
| SP (ALT) — gelir son 4 çeyrek toplamı / PD | KEŞİF | 120 | %4,1 | %6,8 | 1,66 [1,25; 2,53] | %5,8 | %13,4 | 2,33 [1,55; 2,80] | +%12,7 | +%4,6 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SP (ALT) | DOĞRULAMA | 24 | %3,7 | %5,0 | 1,36 [1,13; 1,58] | %7,0 | %15,7 | 2,24 [1,93; 2,56] | +%1,4 | -%8,0 | +%10,0 |  |
| SP (ALT) | KASA | 20 | %6,8 | %10,9 | 1,60 [1,48; 1,75] | %7,3 | %12,9 | 1,78 [1,57; 1,96] | +%22,1 | +%3,4 | +%16,1 |  |
| SP (ÜST) — gelir son 4 çeyrek toplamı / PD | KEŞİF | 120 | %4,1 | %8,9 | 2,17 [1,54; 2,51] | %5,8 | %6,0 | 1,04 [0,63; 1,69] | +%27,8 | +%11,7 | +%14,5 | yol R2; K60-OLASILIK İZİ |
| SP (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,3 | 1,71 [1,53; 1,86] | %7,0 | %6,3 | 0,91 [0,83; 1,00] | +%17,4 | +%11,0 | +%10,0 |  |
| SP (ÜST) | KASA | 20 | %6,8 | %8,0 | 1,18 [1,06; 1,26] | %7,3 | %9,4 | 1,29 [1,15; 1,44] | +%14,5 | +%3,6 | +%16,1 |  |
| SPREAD_CS (ÜST) — Corwin-Schultz alış-satış farkı tahmini, t'nin takvim ayında | KEŞİF | 120 | %4,1 | %10,7 | 2,61 [2,14; 3,58] | %5,8 | %20,8 | 3,60 [3,24; 4,29] | +%16,2 | -%6,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SPREAD_CS (ÜST) | DOĞRULAMA | 24 | %3,7 | %9,5 | 2,57 [2,28; 2,74] | %7,0 | %26,3 | 3,76 [3,70; 3,83] | +%3,0 | -%18,5 | +%10,0 |  |
| SPREAD_CS (ÜST) | KASA | 20 | %6,8 | %16,0 | 2,35 [2,06; 2,89] | %7,3 | %25,9 | 3,56 [3,22; 3,85] | +%23,7 | -%12,3 | +%16,1 |  |
| STREV_1M (ALT) — A(m) / A(m-1) - 1 (geçen ayın getirisi) | KEŞİF | 120 | %4,1 | %7,3 | 1,76 [1,59; 2,12] | %5,8 | %10,5 | 1,82 [1,62; 2,22] | +%16,3 | +%4,7 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| STREV_1M (ALT) | DOĞRULAMA | 24 | %3,7 | %6,5 | 1,75 [1,66; 1,83] | %7,0 | %12,7 | 1,81 [1,60; 2,05] | +%8,0 | -%2,6 | +%10,0 |  |
| STREV_1M (ALT) | KASA | 20 | %6,8 | %12,2 | 1,78 [1,62; 2,08] | %7,3 | %14,4 | 1,98 [1,79; 2,23] | +%22,9 | -%0,4 | +%16,1 |  |
| STREV_1M (ÜST) — A(m) / A(m-1) - 1 (geçen ayın getirisi) | KEŞİF | 120 | %4,1 | %7,3 | 1,77 [1,58; 2,15] | %5,8 | %13,8 | 2,39 [2,17; 2,56] | +%13,9 | +%3,4 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| STREV_1M (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,9 | 1,86 [1,74; 2,01] | %7,0 | %16,3 | 2,34 [2,15; 2,54] | +%6,9 | -%4,1 | +%10,0 |  |
| STREV_1M (ÜST) | KASA | 20 | %6,8 | %11,4 | 1,67 [1,53; 1,90] | %7,3 | %16,2 | 2,24 [2,00; 2,44] | +%17,3 | -%3,8 | +%16,1 |  |
| SUE_SRW (ALT) — (net kâr(ç0) - net kâr(ç0-4)) / son 8 yıllık farkın (ç0 .. ç | KEŞİF | 119 | %4,1 | %5,5 | 1,34 [1,07; 1,46] | %5,8 | %9,8 | 1,69 [1,30; 2,02] | +%13,6 | +%8,4 | +%14,4 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| SUE_SRW (ALT) | DOĞRULAMA | 24 | %3,7 | %4,4 | 1,18 [1,01; 1,46] | %7,0 | %12,0 | 1,71 [1,63; 1,79] | +%8,4 | +%1,5 | +%10,0 |  |
| SUE_SRW (ALT) | KASA | 20 | %6,8 | %8,6 | 1,26 [1,12; 1,35] | %7,3 | %9,2 | 1,27 [1,10; 1,41] | +%19,8 | +%4,8 | +%16,1 |  |
| TAX_CHG (ALT) — (IncomeTaxExpenseBenefit(ç0) - (ç0-4)) / varlık(ç0-4) | KEŞİF | 120 | %4,1 | %5,4 | 1,31 [1,07; 1,46] | %5,8 | %5,8 | 1,01 [0,85; 1,19] | +%17,5 | +%10,7 | +%14,5 | yol R2 |
| TAX_CHG (ALT) | DOĞRULAMA | 24 | %3,7 | %3,4 | 0,93 [0,87; 1,02] | %7,0 | %7,9 | 1,13 [1,07; 1,20] | +%7,2 | +%2,4 | +%10,0 |  |
| TAX_CHG (ALT) | KASA | 20 | %6,8 | %7,0 | 1,02 [0,91; 1,08] | %7,3 | %7,2 | 1,00 [0,94; 1,05] | +%13,8 | +%1,3 | +%16,1 |  |
| TREND_MA (ALT) — x_L = L günlük ortalama C / C(t), L = 3, 5, 10, 20, 50, 100, | KEŞİF | 120 | %4,1 | %7,8 | 1,90 [1,70; 2,28] | %5,8 | %12,5 | 2,18 [1,99; 2,40] | +%17,1 | +%6,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| TREND_MA (ALT) | DOĞRULAMA | 24 | %3,7 | %6,8 | 1,84 [1,64; 2,17] | %7,0 | %17,3 | 2,48 [1,86; 2,95] | +%5,7 | -%6,1 | +%10,0 |  |
| TREND_MA (ALT) | KASA | 20 | %6,8 | %9,7 | 1,42 [1,18; 1,82] | %7,3 | %16,5 | 2,27 [2,08; 2,42] | +%13,7 | -%3,8 | +%16,1 |  |
| TREND_MA (ÜST) — x_L = L günlük ortalama C / C(t), L = 3, 5, 10, 20, 50, 100, | KEŞİF | 120 | %4,1 | %7,3 | 1,77 [1,58; 2,17] | %5,8 | %11,0 | 1,91 [1,62; 2,30] | +%14,5 | +%4,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| TREND_MA (ÜST) | DOĞRULAMA | 24 | %3,7 | %6,6 | 1,78 [1,52; 1,94] | %7,0 | %12,1 | 1,73 [1,25; 2,38] | +%9,7 | -%1,5 | +%10,0 |  |
| TREND_MA (ÜST) | KASA | 20 | %6,8 | %12,7 | 1,87 [1,74; 2,04] | %7,3 | %13,9 | 1,92 [1,74; 2,07] | +%25,7 | +%0,6 | +%16,1 |  |
| TURN_12M (ALT) — son 252 işlem gününün (en az 150) ortalama hacmi / pay sayıs | KEŞİF | 120 | %4,1 | %9,7 | 2,36 [2,22; 2,71] | %5,8 | %15,8 | 2,74 [2,37; 3,04] | +%20,3 | -%0,3 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| TURN_12M (ALT) | DOĞRULAMA | 24 | %3,7 | %8,0 | 2,16 [1,93; 2,29] | %7,0 | %18,1 | 2,59 [2,49; 2,67] | +%6,2 | -%8,1 | +%10,0 |  |
| TURN_12M (ALT) | KASA | 20 | %6,8 | %13,7 | 2,01 [1,71; 2,50] | %7,3 | %19,1 | 2,64 [2,27; 2,94] | +%25,2 | -%4,3 | +%16,1 |  |
| VOL_60D (ALT) — son 60 işlem gününün günlük getiri std'si (en az 40) | KEŞİF | 120 | %4,1 | %11,2 | 2,73 [2,33; 3,60] | %5,8 | %20,9 | 3,62 [3,23; 4,33] | +%17,0 | -%7,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| VOL_60D (ALT) | DOĞRULAMA | 24 | %3,7 | %9,5 | 2,56 [2,46; 2,64] | %7,0 | %26,6 | 3,81 [3,71; 3,91] | +%2,5 | -%20,3 | +%10,0 |  |
| VOL_60D (ALT) | KASA | 20 | %6,8 | %16,8 | 2,46 [2,03; 3,15] | %7,3 | %25,0 | 3,44 [3,02; 3,80] | +%26,6 | -%8,6 | +%16,1 |  |
| VOL_SHOCK (ALT) — son 5 işlem gününün ortalama hacmi / ondan önceki 50 günün o | KEŞİF | 120 | %4,1 | %5,5 | 1,33 [1,24; 1,52] | %5,8 | %10,9 | 1,90 [1,52; 2,15] | +%13,4 | +%6,0 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| VOL_SHOCK (ALT) | DOĞRULAMA | 24 | %3,7 | %4,7 | 1,26 [1,11; 1,36] | %7,0 | %13,4 | 1,92 [1,70; 2,09] | +%5,3 | -%2,1 | +%10,0 |  |
| VOL_SHOCK (ALT) | KASA | 20 | %6,8 | %8,9 | 1,30 [1,20; 1,45] | %7,3 | %13,8 | 1,90 [1,78; 2,00] | +%14,3 | +%0,8 | +%16,1 |  |
| VOL_SHOCK (ÜST) — son 5 işlem gününün ortalama hacmi / ondan önceki 50 günün o | KEŞİF | 120 | %4,1 | %5,2 | 1,26 [1,17; 1,40] | %5,8 | %7,5 | 1,30 [1,21; 1,42] | +%15,0 | +%8,2 | +%14,5 | yol R2+R2K; K60-OLASILIK İZİ, K60-KAÇINMA İZİ |
| VOL_SHOCK (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,9 | 1,33 [1,23; 1,44] | %7,0 | %8,9 | 1,28 [1,18; 1,39] | +%10,5 | +%3,8 | +%10,0 |  |
| VOL_SHOCK (ÜST) | KASA | 20 | %6,8 | %8,4 | 1,23 [1,10; 1,45] | %7,3 | %10,0 | 1,37 [1,27; 1,50] | +%17,5 | +%2,9 | +%16,1 |  |

## Aile bileşikleri ve K59 bileşikleri (seçilmemiş olanlar; bilgi)

| özellik (uç) | dönem | ay | taban P(+%100) | P(+%100) | kat (lift) [%95 aralık] | taban P(-%50) | P(-%50) | kat [%95 aralık] | ort. 12 ay | medyan | evren ort. | etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AILE_DIS (ÜST) | KEŞİF | 120 | %4,1 | %1,3 | 0,33 [0,25; 0,44] | %5,8 | %1,5 | 0,27 [0,18; 0,38] | +%12,6 | +%10,2 | +%14,5 | AİLE BİLGİSİ |
| AILE_DIS (ÜST) | DOĞRULAMA | 24 | %3,7 | %1,1 | 0,30 [0,18; 0,44] | %7,0 | %0,7 | 0,10 [0,06; 0,15] | +%11,9 | +%8,5 | +%10,0 |  |
| AILE_EAR (ÜST) | KEŞİF | 120 | %4,1 | %4,3 | 1,05 [0,89; 1,15] | %5,8 | %4,7 | 0,81 [0,76; 0,91] | +%16,0 | +%10,8 | +%14,5 | AİLE BİLGİSİ |
| AILE_EAR (ÜST) | DOĞRULAMA | 24 | %3,7 | %5,8 | 1,57 [1,25; 1,78] | %7,0 | %6,2 | 0,88 [0,85; 0,92] | +%15,9 | +%8,1 | +%10,0 |  |
| AILE_EAR (ÜST) | KASA | 20 | %6,8 | %8,1 | 1,19 [1,00; 1,51] | %7,3 | %8,5 | 1,16 [0,95; 1,43] | +%17,7 | +%3,8 | +%16,1 |  |
| AILE_INV (ÜST) | KEŞİF | 120 | %4,1 | %3,4 | 0,83 [0,41; 1,06] | %5,8 | %2,1 | 0,37 [0,26; 0,58] | +%19,5 | +%12,4 | +%14,5 | AİLE BİLGİSİ |
| AILE_INV (ÜST) | DOĞRULAMA | 24 | %3,7 | %2,5 | 0,69 [0,51; 0,79] | %7,0 | %2,8 | 0,41 [0,31; 0,51] | +%14,0 | +%9,0 | +%10,0 |  |
| AILE_INV (ÜST) | KASA | 20 | %6,8 | %3,1 | 0,46 [0,32; 0,63] | %7,3 | %4,8 | 0,66 [0,58; 0,75] | +%8,9 | +%3,5 | +%16,1 |  |
| AILE_LIQ (ALT) | KEŞİF | 120 | %4,1 | %1,7 | 0,41 [0,28; 0,47] | %5,8 | %2,6 | 0,45 [0,32; 0,51] | +%13,8 | +%11,6 | +%14,5 | AİLE BİLGİSİ |
| AILE_LIQ (ALT) | DOĞRULAMA | 24 | %3,7 | %2,0 | 0,55 [0,44; 0,65] | %7,0 | %1,8 | 0,25 [0,17; 0,33] | +%13,3 | +%8,8 | +%10,0 |  |
| AILE_PRF (ÜST) | KEŞİF | 120 | %4,1 | %3,1 | 0,76 [0,61; 0,86] | %5,8 | %3,4 | 0,58 [0,47; 0,74] | +%15,6 | +%11,6 | +%14,5 | AİLE BİLGİSİ |
| AILE_PRF (ÜST) | DOĞRULAMA | 24 | %3,7 | %2,9 | 0,77 [0,57; 0,88] | %7,0 | %2,3 | 0,33 [0,29; 0,37] | +%14,2 | +%10,8 | +%10,0 |  |
| AILE_RSK (ÜST) | KEŞİF | 120 | %4,1 | %0,9 | 0,21 [0,11; 0,27] | %5,8 | %1,0 | 0,18 [0,08; 0,37] | +%11,5 | +%10,2 | +%14,5 | AİLE BİLGİSİ |
| AILE_RSK (ÜST) | DOĞRULAMA | 24 | %3,7 | %0,6 | 0,16 [0,11; 0,22] | %7,0 | %1,3 | 0,18 [0,14; 0,22] | +%7,0 | +%4,1 | +%10,0 |  |
| AILE_SEC (ÜST) | KEŞİF | 120 | %4,1 | %4,8 | 1,16 [0,95; 1,60] | %5,8 | %5,4 | 0,94 [0,81; 1,11] | +%16,3 | +%10,4 | +%14,5 | AİLE BİLGİSİ |
| AILE_SEC (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,2 | 1,14 [0,62; 1,43] | %7,0 | %3,3 | 0,47 [0,35; 0,66] | +%15,4 | +%7,8 | +%10,0 |  |
| AILE_SEC (ALT) | KEŞİF | 120 | %4,1 | %4,2 | 1,02 [0,61; 1,24] | %5,8 | %7,1 | 1,23 [0,83; 1,74] | +%13,4 | +%9,3 | +%14,5 | AİLE BİLGİSİ |
| AILE_SEC (ALT) | DOĞRULAMA | 24 | %3,7 | %3,7 | 1,00 [0,83; 1,26] | %7,0 | %7,3 | 1,05 [0,47; 1,55] | +%11,8 | +%7,1 | +%10,0 |  |
| AILE_VAL (ÜST) | KEŞİF | 120 | %4,1 | %5,4 | 1,32 [0,70; 1,62] | %5,8 | %3,6 | 0,63 [0,29; 1,16] | +%19,6 | +%11,2 | +%14,5 | AİLE BİLGİSİ |
| AILE_VAL (ÜST) | DOĞRULAMA | 24 | %3,7 | %2,3 | 0,62 [0,58; 0,70] | %7,0 | %3,5 | 0,51 [0,43; 0,58] | +%13,1 | +%9,8 | +%10,0 |  |
| COMP4 (ÜST) | KEŞİF | 120 | %4,1 | %2,9 | 0,70 [0,55; 0,80] | %5,8 | %2,5 | 0,43 [0,38; 0,48] | +%15,4 | +%12,2 | +%14,5 | AİLE BİLGİSİ |
| COMP4 (ÜST) | DOĞRULAMA | 24 | %3,7 | %3,8 | 1,02 [0,66; 1,22] | %7,0 | %1,7 | 0,25 [0,17; 0,34] | +%19,0 | +%12,7 | +%10,0 |  |
| COMP4 (ÜST) | KASA | 20 | %6,8 | %5,0 | 0,74 [0,66; 0,85] | %7,3 | %3,4 | 0,47 [0,43; 0,50] | +%16,1 | +%7,1 | +%16,1 |  |
| DOSYA_Y (ÜST) | KEŞİF | 120 | %4,1 | %3,9 | 0,95 [0,76; 1,06] | %5,8 | %3,6 | 0,62 [0,53; 0,77] | +%15,6 | +%10,5 | +%14,5 | AİLE BİLGİSİ |
| DOSYA_Y (ÜST) | DOĞRULAMA | 24 | %3,7 | %4,0 | 1,08 [0,86; 1,19] | %7,0 | %3,8 | 0,54 [0,46; 0,62] | +%17,5 | +%11,8 | +%10,0 |  |
| DOSYA_Y (ÜST) | KASA | 20 | %6,8 | %6,7 | 0,98 [0,82; 1,26] | %7,3 | %4,4 | 0,61 [0,48; 0,76] | +%17,8 | +%5,9 | +%16,1 |  |

## Birleşik olasılık modeli (üst %10; bilgi)

| özellik (uç) | dönem | ay | taban P(+%100) | P(+%100) | kat (lift) [%95 aralık] | taban P(-%50) | P(-%50) | kat [%95 aralık] | ort. 12 ay | medyan | evren ort. | etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ODDS_MODEL (ÜST) | KEŞİF | 120 | %4,1 | %10,4 | 2,53 [2,17; 3,30] | %5,8 | %16,4 | 2,85 [2,54; 3,28] | +%19,4 | +%1,2 | +%14,5 | birleşik model (bilgi; KEŞİF örneklem içi) |
| ODDS_MODEL (ÜST) | DOĞRULAMA | 24 | %3,7 | %9,7 | 2,64 [2,40; 2,83] | %7,0 | %22,3 | 3,20 [3,10; 3,30] | +%7,4 | -%12,7 | +%10,0 |  |
| ODDS_MODEL (ÜST) | KASA | 20 | %6,8 | %14,9 | 2,18 [1,85; 2,78] | %7,3 | %23,3 | 3,20 [3,00; 3,37] | +%23,1 | -%8,4 | +%16,1 |  |


## R1 — portföy cetveli v2 (seçilen çiftler ve bileşiklerin ÜST ucu)
| özellik (uç) | dönem | ay | yıllık fazla (net) | NW t | alfa (yıllık) | t(alfa) | beta | alt 1/2/3 | son %30 | cetvel v2 | FF5+UMD alfa | t | devir | hisse | en büyük üç katkı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACCRUALS (ALT) | KEŞİF | 120 | -%0,6 | -0,26 | -%2,1 | -0,98 | 1,10 | +%0,07 / -%0,31 / +%0,09 | +%0,12 | tutmaz | -%0,6 | -0,35 | %27 | 127 | ERNA 3%; MCRB 2%; ALNY 2% |
| ACCRUALS (ALT) | DOĞRULAMA | 24 | +%0,1 | 0,04 | -%0,2 | -0,08 | 1,18 | -%0,15 / +%0,24 / -%0,06 | -%0,06 | tutmaz | -%1,9 | -0,61 | %31 | 203 | RYTM 32%; SMCI 21%; SYM 20% |
| ACCRUALS (ALT) | KASA | 31 | +%0,2 | 0,06 | -%2,2 | -0,61 | 1,15 | +%0,70 / +%0,44 / -%1,15 | -%1,15 | tutmaz | -%1,2 | -0,35 | %33 | 229 | ASTS 4%; HUT 3%; AEHR 3% |
| ACCRUALS (ÜST) | KEŞİF | 120 | +%1,6 | 0,40 | -%2,6 | -0,70 | 1,28 | -%0,07 / +%0,34 / +%0,14 | +%0,29 | tutmaz | +%1,5 | 0,74 | %31 | 127 | DXCM 2%; NCTY 2%; AMZN 2% |
| ACCRUALS (ÜST) | DOĞRULAMA | 24 | -%6,5 | -1,13 | -%6,9 | -1,50 | 1,20 | -%0,94 / -%0,36 / -%0,32 | -%0,32 | tutmaz | -%2,2 | -0,48 | %35 | 203 | — |
| ACCRUALS (ÜST) | KASA | 31 | -%2,5 | -0,38 | -%7,4 | -1,00 | 1,30 | +%0,31 / +%0,30 / -%1,28 | -%1,28 | tutmaz | -%7,5 | -0,92 | %37 | 229 | AGL 5%; DAVE 5%; QBTS 4% |
| ACT_13D (ÜST) | KEŞİF | 114 | -%7,6 | -2,39 | -%9,3 | -3,04 | 1,10 | -%0,28 / -%0,42 / -%1,21 | -%1,33 | tutmaz | -%9,0 | -2,79 | %113 | 23 | CRDF 7%; ALT 7%; AUPH 6% |
| ACT_13D (ÜST) | DOĞRULAMA | 24 | -%13,2 | -0,89 | -%13,5 | -0,92 | 1,18 | -%2,71 / -%2,48 / +%1,90 | +%1,90 | tutmaz | -%16,1 | -1,43 | %113 | 26 | — |
| ACT_13D (ÜST) | KASA | 31 | -%12,0 | -1,54 | -%16,4 | -1,74 | 1,27 | -%0,32 / -%1,33 / -%1,44 | -%1,44 | tutmaz | -%14,3 | -2,21 | %113 | 32 | NVAX 80%; ALMS 29%; SEI 25% |
| AILE_DIS (ALT) | KEŞİF | 120 | +%1,9 | 0,30 | -%4,9 | -0,84 | 1,45 | +%0,06 / +%0,09 / +%0,33 | +%0,65 | tutmaz | +%1,3 | 0,40 | %47 | 114 | GME 7%; ERNA 4%; WKHS 2% |
| AILE_DIS (ALT) | DOĞRULAMA | 24 | -%16,8 | -2,02 | -%17,5 | -2,63 | 1,39 | -%1,42 / -%1,50 / -%1,27 | -%1,27 | tutmaz | -%9,0 | -1,26 | %54 | 172 | — |
| AILE_DIS (ALT) | KASA | 31 | +%5,3 | 0,76 | -%3,0 | -0,47 | 1,50 | +%0,92 / +%1,17 / -%0,83 | -%0,83 | tutmaz | +%3,0 | 0,60 | %57 | 193 | CAPR 7%; QURE 5%; BKKT 4% |
| AILE_DIS (ÜST) | KEŞİF | 120 | -%1,9 | -0,77 | +%2,9 | 2,22 | 0,68 | -%0,28 / -%0,10 / -%0,10 | -%0,15 | tutmaz | -%0,5 | -0,44 | %36 | 114 | NVDA 2%; ODFL 2%; DHR 2% |
| AILE_DIS (ÜST) | DOĞRULAMA | 24 | +%4,1 | 1,09 | +%4,6 | 2,03 | 0,74 | +%0,65 / +%0,26 / +%0,11 | +%0,11 | tutmaz | -%1,0 | -0,49 | %34 | 172 | RMBS 6%; BLDR 5%; AMR 5% |
| AILE_EAR (ALT) | KEŞİF | 120 | -%0,2 | -0,08 | -%3,9 | -1,91 | 1,24 | +%0,11 / -%0,01 / -%0,15 | -%0,09 | tutmaz | -%0,2 | -0,10 | %83 | 145 | NKTR 2%; ACAD 2%; AMC 2% |
| AILE_EAR (ALT) | DOĞRULAMA | 24 | +%1,4 | 0,26 | +%1,1 | 0,20 | 1,16 | +%0,26 / +%0,63 / -%0,55 | -%0,55 | tutmaz | +%1,5 | 0,26 | %82 | 207 | MDGL 18%; RYTM 16%; TDS 12% |
| AILE_EAR (ALT) | KASA | 31 | -%4,9 | -0,98 | -%7,4 | -1,65 | 1,15 | -%1,15 / +%0,66 / -%0,66 | -%0,66 | tutmaz | -%8,6 | -1,89 | %78 | 231 | SRRK 5%; PRAX 5%; COGT 5% |
| AILE_EAR (ÜST) | KEŞİF | 120 | +%1,5 | 0,93 | +%2,1 | 1,41 | 0,96 | +%0,16 / +%0,22 / +%0,01 | +%0,07 | tutmaz | +%0,8 | 0,52 | %76 | 145 | NXH 1%; DXCM 1%; CLSK 1% |
| AILE_EAR (ÜST) | DOĞRULAMA | 24 | -%0,0 | -0,01 | +%0,1 | 0,04 | 0,93 | +%0,17 / -%0,09 / -%0,09 | -%0,09 | tutmaz | -%3,6 | -1,45 | %75 | 207 | ELF 15%; VRT 12%; TWST 10% |
| AILE_EAR (ÜST) | KASA | 31 | +%3,4 | 0,78 | +%3,4 | 0,74 | 1,00 | +%1,23 / -%0,09 / -%0,38 | -%0,38 | tutmaz | +%1,3 | 0,31 | %71 | 231 | RGTI 3%; OUST 2%; APP 2% |
| AILE_INV (ALT) | KEŞİF | 120 | -%3,2 | -0,83 | -%5,6 | -1,32 | 1,16 | -%0,13 / -%0,22 / -%0,44 | -%0,33 | tutmaz | -%2,9 | -1,97 | %36 | 145 | PBYI 3%; WKHS 2%; TTD 2% |
| AILE_INV (ALT) | DOĞRULAMA | 24 | -%10,3 | -1,96 | -%10,7 | -2,46 | 1,19 | -%1,51 / -%0,17 / -%0,90 | -%0,90 | tutmaz | -%10,3 | -3,49 | %42 | 207 | — |
| AILE_INV (ALT) | KASA | 31 | +%0,6 | 0,11 | -%3,9 | -0,72 | 1,27 | +%0,41 / +%1,06 / -%1,38 | -%1,38 | tutmaz | -%5,8 | -1,51 | %40 | 233 | ASTS 6%; INOD 4%; HUT 3% |
| AILE_INV (ÜST) | KEŞİF | 120 | +%3,2 | 1,80 | +%3,6 | 1,99 | 0,97 | +%0,23 / +%0,03 / +%0,55 | +%0,55 | tutmaz | +%3,1 | 2,12 | %30 | 145 | GME 6%; DDS 1%; HD 1% |
| AILE_INV (ÜST) | DOĞRULAMA | 24 | +%5,7 | 2,89 | +%5,9 | 3,04 | 0,90 | +%0,22 / +%0,56 / +%0,63 | +%0,63 | TUTAR | +%1,2 | 0,78 | %29 | 207 | CDLX 7%; XPO 4%; APP 3% |
| AILE_INV (ÜST) | KASA | 31 | -%2,5 | -1,05 | -%0,5 | -0,17 | 0,88 | -%0,30 / -%0,70 / +%0,39 | +%0,39 | tutmaz | -%3,9 | -1,96 | %30 | 233 | LASE 3%; NEGG 3%; WDC 3% |
| AILE_LIQ (ÜST) | KEŞİF | 120 | -%1,6 | -0,54 | -%4,2 | -1,77 | 1,18 | -%0,34 / +%0,30 / -%0,36 | -%0,08 | tutmaz | +%0,1 | 0,06 | %114 | 164 | AMRN 2%; MDXG 1%; NCTY 1% |
| AILE_LIQ (ÜST) | DOĞRULAMA | 24 | -%9,4 | -3,18 | -%9,7 | -4,16 | 1,15 | -%0,94 / -%0,53 / -%0,88 | -%0,88 | tutmaz | -%7,5 | -2,13 | %117 | 227 | — |
| AILE_LIQ (ÜST) | KASA | 31 | -%5,3 | -1,17 | -%8,4 | -1,74 | 1,19 | +%0,13 / -%0,39 / -%1,11 | -%1,11 | tutmaz | -%4,2 | -0,48 | %115 | 252 | BKKT 7%; LASE 4%; NUTX 4% |
| AILE_MOM (ALT) | KEŞİF | 120 | -%5,0 | -1,58 | -%10,0 | -3,72 | 1,33 | -%0,48 / -%0,20 / -%0,56 | -%0,66 | tutmaz | -%3,8 | -2,26 | %104 | 164 | NCTY 2%; AMRN 2%; NXH 1% |
| AILE_MOM (ALT) | DOĞRULAMA | 24 | -%7,9 | -0,93 | -%8,4 | -1,19 | 1,25 | -%2,11 / -%0,04 / +%0,17 | +%0,17 | tutmaz | -%5,7 | -1,13 | %105 | 227 | — |
| AILE_MOM (ALT) | KASA | 31 | -%1,1 | -0,18 | -%2,4 | -0,34 | 1,08 | -%0,69 / -%0,30 / +%0,77 | +%0,77 | tutmaz | +%0,3 | 0,07 | %96 | 252 | CAPR 6%; AGL 4%; MLGO 4% |
| AILE_MOM (ÜST) | KEŞİF | 120 | +%2,9 | 1,34 | +%2,7 | 1,47 | 1,01 | -%0,02 / +%0,36 / +%0,39 | +%0,66 | tutmaz | +%1,2 | 0,55 | %108 | 164 | GME 4%; WKHS 2%; MCRB 1% |
| AILE_MOM (ÜST) | DOĞRULAMA | 24 | +%4,2 | 0,71 | +%4,5 | 0,92 | 0,85 | +%1,57 / -%0,45 / -%0,06 | -%0,06 | tutmaz | +%1,7 | 0,58 | %103 | 227 | SMCI 11%; EYPT 8%; MOD 5% |
| AILE_PRF (ALT) | KEŞİF | 120 | -%3,6 | -0,87 | -%8,0 | -2,20 | 1,29 | +%0,08 / -%0,38 / -%0,58 | -%0,38 | tutmaz | -%3,5 | -1,76 | %48 | 128 | ERNA 5%; PBYI 3%; ALNY 3% |
| AILE_PRF (ALT) | DOĞRULAMA | 24 | -%12,3 | -2,47 | -%12,9 | -3,24 | 1,32 | -%1,11 / -%1,10 / -%0,86 | -%0,86 | tutmaz | -%9,9 | -4,23 | %50 | 192 | — |
| AILE_PRF (ALT) | KASA | 31 | +%4,1 | 0,62 | -%1,0 | -0,17 | 1,31 | +%0,01 / +%1,31 / -%0,28 | -%0,28 | tutmaz | +%1,4 | 0,30 | %50 | 214 | CAPR 6%; RGTI 5%; OKLO 4% |
| AILE_PRF (ÜST) | KEŞİF | 120 | +%1,3 | 0,57 | +%3,3 | 1,82 | 0,87 | +%0,10 / +%0,19 / +%0,04 | +%0,07 | tutmaz | +%0,2 | 0,18 | %35 | 128 | MANH 2%; MED 2%; DPZ 1% |
| AILE_PRF (ÜST) | DOĞRULAMA | 24 | +%3,7 | 1,21 | +%3,9 | 1,37 | 0,89 | +%0,19 / +%0,03 / +%0,71 | +%0,71 | tutmaz | -%2,7 | -0,92 | %36 | 192 | BLDR 5%; CNR 5%; URI 4% |
| AILE_RSK (ALT) | KEŞİF | 120 | -%3,5 | -0,85 | -%9,3 | -2,70 | 1,38 | -%0,30 / -%0,32 / -%0,26 | -%0,11 | tutmaz | -%4,4 | -2,12 | %150 | 164 | GME 6%; INSM 2%; NXH 1% |
| AILE_RSK (ALT) | DOĞRULAMA | 24 | -%13,0 | -2,48 | -%13,6 | -3,67 | 1,32 | -%1,43 / -%0,87 / -%0,95 | -%0,95 | tutmaz | -%9,3 | -3,19 | %144 | 227 | — |
| AILE_RSK (ALT) | KASA | 31 | -%3,3 | -0,44 | -%12,0 | -1,98 | 1,53 | -%0,57 / +%0,79 / -%1,01 | -%1,01 | tutmaz | -%12,1 | -1,67 | %146 | 252 | RGTI 4%; AGL 4%; MSTR 4% |
| AILE_RSK (ÜST) | KEŞİF | 120 | -%1,7 | -0,54 | +%3,9 | 1,52 | 0,62 | -%0,09 / -%0,14 / -%0,20 | -%0,38 | tutmaz | +%0,2 | 0,11 | %118 | 164 | NXDT 1%; REXR 1%; NAGE 1% |
| AILE_RSK (ÜST) | DOĞRULAMA | 24 | -%2,1 | -0,32 | -%1,3 | -0,38 | 0,60 | +%0,99 / -%0,70 / -%0,81 | -%0,81 | tutmaz | -%7,4 | -2,33 | %120 | 227 | GETYQ 30%; GTX 12%; HTGC 12% |
| AILE_SEA (ALT) | KEŞİF | 120 | -%0,2 | -0,06 | -%4,0 | -1,56 | 1,25 | -%0,38 / -%0,09 / +%0,42 | +%0,57 | tutmaz | -%0,6 | -0,22 | %171 | 164 | GME 4%; ERNA 3%; AMRN 2% |
| AILE_SEA (ALT) | DOĞRULAMA | 24 | -%5,9 | -1,02 | -%6,5 | -1,39 | 1,29 | -%1,04 / -%1,11 / +%0,66 | +%0,66 | tutmaz | -%4,6 | -1,46 | %162 | 227 | — |
| AILE_SEA (ALT) | KASA | 31 | -%1,1 | -0,41 | -%4,5 | -1,22 | 1,21 | +%0,30 / -%0,11 / -%0,51 | -%0,51 | tutmaz | -%1,7 | -0,36 | %168 | 252 | RGTI 5%; RCAT 3%; NEGG 3% |
| AILE_SEA (ÜST) | KEŞİF | 120 | -%4,0 | -1,20 | -%7,2 | -2,20 | 1,21 | -%0,19 / -%0,15 / -%0,66 | -%0,50 | tutmaz | -%5,6 | -3,32 | %170 | 164 | MCRB 2%; CZR 1%; DXCM 1% |
| AILE_SEA (ÜST) | DOĞRULAMA | 24 | -%7,5 | -2,41 | -%7,6 | -2,39 | 1,06 | -%0,28 / -%0,08 / -%1,52 | -%1,52 | tutmaz | -%6,2 | -3,04 | %174 | 227 | — |
| AILE_SEA (ÜST) | KASA | 31 | +%1,5 | 0,41 | -%3,6 | -1,02 | 1,31 | -%0,01 / +%1,11 / -%0,71 | -%0,71 | tutmaz | -%4,9 | -1,13 | %168 | 252 | NVAX 3%; CRDO 3%; PRAX 2% |
| AILE_SEC (ÜST) | KEŞİF | 120 | -%0,8 | -0,45 | +%0,4 | 0,22 | 0,93 | +%0,07 / -%0,33 / +%0,07 | +%0,17 | tutmaz | +%0,0 | 0,01 | %107 | 111 | RIOT 1%; MARA 1%; CDE 1% |
| AILE_SEC (ÜST) | DOĞRULAMA | 24 | +%6,1 | 0,80 | +%6,1 | 0,82 | 0,97 | +%1,74 / -%0,15 / -%0,07 | -%0,07 | tutmaz | +%4,8 | 0,94 | %102 | 159 | DFH 6%; HOV 5%; PBF 4% |
| AILE_VAL (ALT) | KEŞİF | 120 | +%0,5 | 0,09 | -%2,8 | -0,41 | 1,22 | +%0,19 / +%0,27 / -%0,33 | -%0,08 | tutmaz | +%0,7 | 0,38 | %33 | 141 | TSLA 2%; DXCM 2%; ACAD 2% |
| AILE_VAL (ALT) | DOĞRULAMA | 24 | -%10,6 | -1,77 | -%10,6 | -1,72 | 0,98 | -%0,60 / -%0,50 / -%1,56 | -%1,56 | tutmaz | -%6,1 | -1,25 | %38 | 197 | — |
| AILE_VAL (ALT) | KASA | 31 | +%1,6 | 0,25 | -%2,6 | -0,34 | 1,26 | +%0,10 / +%1,46 / -%1,15 | -%1,15 | tutmaz | -%2,1 | -0,35 | %40 | 219 | RGTI 5%; RKLB 4%; QBTS 3% |
| AILE_VAL (ÜST) | KEŞİF | 120 | +%3,7 | 1,27 | +%0,5 | 0,12 | 1,21 | +%0,28 / +%0,25 / +%0,40 | +%0,31 | tutmaz | +%3,2 | 2,22 | %32 | 141 | VLO 1%; SANM 1%; UVE 1% |
| AILE_VAL (ÜST) | DOĞRULAMA | 24 | +%6,9 | 1,30 | +%6,7 | 1,26 | 1,10 | +%0,06 / -%0,29 / +%1,94 | +%1,94 | tutmaz | +%2,5 | 1,13 | %31 | 197 | HOV 3%; AD 3%; CVI 3% |
| AM (ALT) | KEŞİF | 120 | +%0,9 | 0,21 | -%0,1 | -0,02 | 1,07 | +%0,02 / +%0,11 / +%0,10 | +%0,29 | tutmaz | +%0,1 | 0,04 | %31 | 142 | ACAD 2%; DXCM 2%; TSLA 2% |
| AM (ALT) | DOĞRULAMA | 24 | -%4,5 | -0,84 | -%4,4 | -0,75 | 0,93 | -%0,73 / +%0,39 / -%0,79 | -%0,79 | tutmaz | -%5,1 | -1,39 | %31 | 198 | — |
| AM (ALT) | KASA | 31 | -%1,1 | -0,20 | -%2,6 | -0,44 | 1,09 | +%0,34 / +%0,19 / -%0,85 | -%0,85 | tutmaz | -%4,1 | -0,88 | %37 | 220 | QBTS 4%; CRDO 4%; PLTR 4% |
| AMIHUD (ÜST) | KEŞİF | 120 | -%1,3 | -0,31 | -%5,5 | -1,71 | 1,28 | -%0,23 / +%0,20 / -%0,29 | -%0,05 | tutmaz | -%0,9 | -0,45 | %57 | 164 | ERNA 3%; MCRB 2%; PACB 2% |
| AMIHUD (ÜST) | DOĞRULAMA | 24 | -%11,0 | -2,81 | -%11,3 | -2,81 | 1,17 | -%0,43 / -%1,22 / -%1,09 | -%1,09 | tutmaz | -%8,7 | -2,46 | %61 | 227 | — |
| AMIHUD (ÜST) | KASA | 31 | -%15,0 | -3,04 | -%20,4 | -3,12 | 1,33 | -%0,28 / -%0,87 / -%2,71 | -%2,71 | tutmaz | -%15,5 | -1,75 | %64 | 251 | BKKT 36%; WGS 29%; AXTI 23% |
| ASSET_G (ALT) | KEŞİF | 120 | -%0,5 | -0,12 | -%4,3 | -0,89 | 1,25 | +%0,49 / -%0,17 / -%0,46 | -%0,37 | tutmaz | -%2,2 | -1,12 | %39 | 148 | WKHS 2%; ENPH 2%; TSLA 2% |
| ASSET_G (ALT) | DOĞRULAMA | 24 | -%10,0 | -1,93 | -%10,3 | -2,25 | 1,16 | -%1,31 / -%0,88 / -%0,29 | -%0,29 | tutmaz | -%9,8 | -5,70 | %42 | 208 | — |
| ASSET_G (ALT) | KASA | 31 | -%1,7 | -0,39 | -%6,5 | -1,24 | 1,29 | +%0,33 / +%0,58 / -%1,39 | -%1,39 | tutmaz | -%9,1 | -2,13 | %41 | 232 | APLD 4%; INOD 4%; HUT 3% |
| ASSET_G (ÜST) | KEŞİF | 120 | +%2,2 | 0,59 | -%1,3 | -0,51 | 1,23 | -%0,13 / -%0,01 / +%0,69 | +%0,81 | tutmaz | +%2,6 | 0,98 | %43 | 148 | GME 6%; AMC 2%; MCRB 2% |
| ASSET_G (ÜST) | DOĞRULAMA | 24 | -%2,9 | -0,65 | -%3,2 | -0,68 | 1,17 | +%0,25 / -%0,91 / -%0,07 | -%0,07 | tutmaz | -%1,2 | -0,27 | %48 | 208 | — |
| ASSET_G (ÜST) | KASA | 31 | +%5,2 | 1,15 | +%0,2 | 0,06 | 1,30 | +%0,40 / +%0,78 / +%0,11 | +%0,11 | tutmaz | +%1,2 | 0,30 | %49 | 232 | AGL 3%; WGS 3%; QURE 3% |
| BETA_BAB (ALT) | KEŞİF | 120 | +%2,5 | 0,57 | -%6,5 | -2,18 | 1,59 | -%0,12 / +%0,04 / +%0,72 | +%0,95 | tutmaz | +%0,4 | 0,15 | %31 | 158 | AMC 2%; LNWO 2%; CAR 1% |
| BETA_BAB (ALT) | DOĞRULAMA | 24 | +%2,8 | 0,38 | +%1,9 | 0,36 | 1,48 | -%0,30 / +%0,73 / +%0,27 | +%0,27 | tutmaz | +%8,1 | 2,31 | %34 | 213 | EYPT 14%; TMDX 10%; BBIO 9% |
| BETA_BAB (ALT) | KASA | 31 | +%16,7 | 1,45 | +%1,3 | 0,14 | 1,93 | +%0,66 / +%3,21 / +%0,37 | +%0,37 | tutmaz | -%2,2 | -0,24 | %36 | 246 | BE 2%; RGTI 2%; WGS 2% |
| BE_G (ALT) | KEŞİF | 120 | -%2,3 | -0,67 | -%5,0 | -1,25 | 1,18 | +%0,24 / -%0,24 / -%0,58 | -%0,50 | tutmaz | -%3,5 | -2,19 | %39 | 132 | ARWR 2%; MARA 2%; ALNY 2% |
| BE_G (ALT) | DOĞRULAMA | 24 | -%4,8 | -1,32 | -%5,1 | -1,84 | 1,16 | -%0,97 / -%0,21 / -%0,04 | -%0,04 | tutmaz | -%6,0 | -2,65 | %40 | 184 | — |
| BE_G (ALT) | KASA | 31 | -%5,1 | -1,02 | -%8,7 | -1,41 | 1,22 | +%0,40 / +%0,25 / -%2,00 | -%2,00 | tutmaz | -%11,9 | -2,86 | %40 | 205 | APLD 5%; DAVE 5%; OLMA 5% |
| BE_G (ÜST) | KEŞİF | 120 | +%4,6 | 1,39 | +%0,4 | 0,19 | 1,28 | +%0,25 / +%0,06 / +%0,84 | +%0,97 | tutmaz | +%3,8 | 1,69 | %40 | 132 | GME 6%; PACB 2%; CLSK 1% |
| BE_G (ÜST) | DOĞRULAMA | 24 | -%2,2 | -0,49 | -%2,5 | -0,60 | 1,17 | -%0,01 / +%0,03 / -%0,56 | -%0,56 | tutmaz | +%0,7 | 0,15 | %46 | 184 | ALT 491%; MDGL 379%; RYTM 378% |
| BE_G (ÜST) | KASA | 31 | +%3,4 | 1,02 | -%0,7 | -0,22 | 1,25 | +%0,17 / +%0,72 / -%0,02 | -%0,02 | tutmaz | +%0,2 | 0,07 | %44 | 205 | BKKT 4%; RCAT 3%; REPL 3% |
| BM (ALT) | KEŞİF | 120 | +%3,1 | 0,98 | +%3,0 | 0,79 | 1,01 | +%0,24 / +%0,32 / +%0,22 | +%0,35 | tutmaz | +%1,5 | 1,19 | %30 | 130 | TSLA 2%; NFLX 2%; ENPH 2% |
| BM (ALT) | DOĞRULAMA | 24 | -%0,9 | -0,20 | -%0,7 | -0,14 | 0,89 | -%0,18 / +%0,96 / -%1,01 | -%1,01 | tutmaz | -%1,9 | -0,57 | %29 | 180 | MDGL 65%; AXSM 39%; SYM 37% |
| BM (ÜST) | KEŞİF | 120 | +%2,2 | 0,65 | -%3,0 | -0,86 | 1,35 | +%0,06 / +%0,11 / +%0,39 | +%0,46 | tutmaz | +%1,8 | 1,10 | %35 | 130 | ERNA 4%; RDN 2%; BAC 1% |
| BM (ÜST) | DOĞRULAMA | 24 | +%2,2 | 0,52 | +%1,6 | 0,35 | 1,30 | -%0,19 / -%0,39 / +%1,12 | +%1,12 | tutmaz | -%0,2 | -0,10 | %41 | 180 | MARA 15%; RYTM 13%; SRG 11% |
| BM (ÜST) | KASA | 31 | -%1,0 | -0,23 | -%2,7 | -0,61 | 1,10 | -%0,65 / -%0,35 / +%0,82 | +%0,82 | tutmaz | -%4,8 | -1,51 | %42 | 198 | NEGG 3%; ACDC 3%; PACK 2% |
| BUYBACK_YLD (ALT) | KEŞİF | 120 | -%1,6 | -1,14 | -%1,8 | -1,07 | 1,01 | -%0,08 / +%0,06 / -%0,36 | -%0,35 | tutmaz | -%0,2 | -0,15 | %158 | 130 | FCEL 2%; NCTY 1%; DXPE 1% |
| BUYBACK_YLD (ALT) | DOĞRULAMA | 24 | -%3,6 | -1,27 | -%3,7 | -1,38 | 1,04 | -%0,58 / +%0,21 / -%0,54 | -%0,54 | tutmaz | -%3,6 | -1,23 | %162 | 198 | MDGL 837%; MARA 462%; JOBY 381% |
| BUYBACK_YLD (ALT) | KASA | 31 | -%2,5 | -1,21 | -%5,1 | -2,75 | 1,16 | -%0,20 / -%0,08 / -%0,34 | -%0,34 | tutmaz | -%6,8 | -2,53 | %163 | 219 | CAPR 5%; RGTI 5%; UAVS 3% |
| CAPEX_G (ALT) | KEŞİF | 120 | +%0,4 | 0,10 | -%1,9 | -0,47 | 1,15 | +%0,04 / -%0,10 / +%0,15 | +%0,28 | tutmaz | +%0,6 | 0,30 | %32 | 108 | WKHS 3%; CLSK 2%; UI 2% |
| CAPEX_G (ALT) | DOĞRULAMA | 24 | -%9,5 | -2,09 | -%10,0 | -2,50 | 1,28 | -%0,56 / -%1,22 / -%0,59 | -%0,59 | tutmaz | -%7,4 | -3,00 | %36 | 152 | — |
| CAPEX_G (ALT) | KASA | 31 | +%3,3 | 0,67 | -%1,3 | -0,31 | 1,28 | +%0,17 / +%0,53 / +%0,12 | +%0,12 | tutmaz | -%2,1 | -0,53 | %35 | 169 | ASTS 7%; CELC 4%; AAOI 3% |
| CAPEX_G (ÜST) | KEŞİF | 120 | +%0,7 | 0,30 | -%1,0 | -0,45 | 1,11 | +%0,20 / -%0,02 / -%0,00 | +%0,23 | tutmaz | +%0,9 | 0,67 | %34 | 108 | ERNA 4%; MCRB 2%; AMRN 2% |
| CAPEX_G (ÜST) | DOĞRULAMA | 24 | +%4,8 | 1,26 | +%4,7 | 1,35 | 1,08 | +%0,40 / +%0,37 / +%0,43 | +%0,43 | tutmaz | +%6,5 | 1,71 | %33 | 152 | RYTM 12%; CLSK 11%; ALT 9% |
| CAPEX_G (ÜST) | KASA | 31 | -%2,1 | -0,37 | -%6,1 | -1,21 | 1,25 | -%0,65 / +%0,42 / -%0,24 | -%0,24 | tutmaz | -%4,5 | -1,57 | %41 | 169 | PRAX 5%; QURE 5%; ERAS 5% |
| CBOP_A (ALT) | KEŞİF | 120 | -%1,8 | -0,31 | -%7,1 | -1,13 | 1,35 | +%0,22 / -%0,19 / -%0,49 | -%0,20 | tutmaz | -%1,4 | -0,54 | %34 | 137 | ERNA 4%; ALNY 3%; PBYI 3% |
| CBOP_A (ALT) | DOĞRULAMA | 24 | -%16,2 | -2,04 | -%16,7 | -2,37 | 1,26 | -%1,19 / -%1,67 / -%1,20 | -%1,20 | tutmaz | -%9,2 | -1,18 | %39 | 213 | — |
| CBOP_A (ALT) | KASA | 31 | +%0,4 | 0,05 | -%5,5 | -0,70 | 1,36 | -%0,19 / +%0,88 / -%0,57 | -%0,57 | tutmaz | +%1,5 | 0,30 | %41 | 237 | CAPR 6%; ASTS 5%; QURE 5% |
| CFP (ALT) | KEŞİF | 120 | +%1,2 | 0,20 | -%4,5 | -0,85 | 1,37 | +%0,05 / -%0,21 / +%0,45 | +%0,83 | tutmaz | +%0,8 | 0,26 | %37 | 130 | GME 6%; ERNA 4%; PBYI 2% |
| CFP (ALT) | DOĞRULAMA | 24 | -%11,2 | -1,52 | -%11,8 | -1,97 | 1,34 | -%1,21 / -%1,05 / -%0,53 | -%0,53 | tutmaz | -%5,9 | -0,89 | %47 | 198 | — |
| CFP (ALT) | KASA | 31 | +%4,2 | 0,49 | -%2,1 | -0,27 | 1,38 | -%0,18 / +%0,86 / +%0,43 | +%0,43 | tutmaz | +%0,7 | 0,15 | %47 | 219 | CAPR 6%; QURE 5%; WGS 4% |
| CFP (ÜST) | KEŞİF | 120 | +%3,8 | 0,99 | -%2,2 | -0,59 | 1,39 | +%0,25 / -%0,03 / +%0,72 | +%0,82 | tutmaz | +%1,6 | 0,72 | %33 | 130 | LNWO 2%; AROC 1%; AER 1% |
| CFP (ÜST) | DOĞRULAMA | 24 | +%9,2 | 1,95 | +%8,9 | 1,64 | 1,17 | +%0,57 / +%0,15 / +%1,57 | +%1,57 | tutmaz | +%5,1 | 1,99 | %35 | 198 | CNR 4%; AMPY 4%; AD 3% |
| CHS_FAIL (ALT) | KEŞİF | 120 | +%4,3 | 0,75 | -%6,0 | -1,56 | 1,68 | +%0,19 / +%0,10 / +%0,78 | +%0,99 | tutmaz | +%0,9 | 0,41 | %62 | 114 | ERNA 4%; MCRB 2%; TNDM 2% |
| CHS_FAIL (ALT) | DOĞRULAMA | 24 | -%12,7 | -1,11 | -%13,9 | -2,12 | 1,63 | -%3,25 / +%0,16 / -%0,10 | -%0,10 | tutmaz | -%8,5 | -0,99 | %70 | 156 | — |
| CHS_FAIL (ALT) | KASA | 31 | +%1,1 | 0,17 | -%10,5 | -2,96 | 1,71 | +%0,33 / +%0,15 / -%0,23 | -%0,23 | tutmaz | -%9,0 | -1,84 | %72 | 173 | CAPR 9%; REPL 4%; NVAX 4% |
| COMP4 (ALT) | KEŞİF | 120 | -%2,7 | -0,68 | -%8,9 | -2,50 | 1,41 | -%0,19 / -%0,10 / -%0,39 | -%0,31 | tutmaz | -%2,2 | -1,16 | %76 | 143 | CLSK 2%; MTDR 2%; GRPN 2% |
| COMP4 (ALT) | DOĞRULAMA | 24 | -%8,6 | -1,27 | -%9,5 | -2,01 | 1,46 | -%1,08 / -%0,47 / -%0,61 | -%0,61 | tutmaz | -%4,7 | -1,12 | %78 | 202 | — |
| COMP4 (ALT) | KASA | 31 | +%1,9 | 0,32 | -%3,7 | -0,84 | 1,34 | +%0,15 / +%0,01 / +%0,31 | +%0,31 | tutmaz | -%6,0 | -2,14 | %74 | 226 | CAPR 5%; BKKT 5%; SRRK 3% |
| COMP4 (ÜST) | KEŞİF | 120 | +%1,9 | 1,03 | +%4,1 | 2,63 | 0,86 | +%0,42 / +%0,02 / +%0,05 | +%0,11 | tutmaz | +%0,9 | 0,56 | %67 | 143 | UI 1%; TTD 1%; UVE 1% |
| COMP4 (ÜST) | DOĞRULAMA | 24 | +%5,8 | 1,88 | +%6,1 | 2,64 | 0,82 | +%0,70 / +%0,15 / +%0,60 | +%0,60 | tutmaz | +%0,1 | 0,03 | %65 | 202 | AMR 4%; MOD 4%; ACLS 3% |
| COMP4 (ÜST) | KASA | 31 | +%0,3 | 0,08 | -%0,3 | -0,07 | 1,04 | +%0,69 / -%0,11 / -%0,56 | -%0,56 | tutmaz | -%4,4 | -2,20 | %63 | 226 | APP 3%; WDC 2%; MSTR 2% |
| DOLVOL (ÜST) | KEŞİF | 120 | -%2,7 | -1,16 | -%3,9 | -2,07 | 1,08 | -%0,35 / +%0,10 / -%0,42 | -%0,28 | tutmaz | +%0,3 | 0,20 | %83 | 164 | MCRB 2%; NXDT 1%; TBCH 1% |
| DOLVOL (ÜST) | DOĞRULAMA | 24 | -%6,7 | -3,57 | -%6,7 | -3,67 | 1,03 | -%0,65 / -%0,27 / -%0,75 | -%0,75 | tutmaz | -%7,3 | -2,47 | %85 | 227 | — |
| DOLVOL (ÜST) | KASA | 31 | -%8,9 | -3,85 | -%10,2 | -5,33 | 1,08 | -%0,50 / -%0,96 / -%0,79 | -%0,79 | tutmaz | -%8,3 | -1,96 | %85 | 252 | NUTX 5%; LASE 5%; BLZE 5% |
| DOSYA_Y (ALT) | KEŞİF | 120 | +%1,3 | 0,29 | -%3,8 | -1,15 | 1,34 | +%0,11 / -%0,33 / +%0,56 | +%0,67 | tutmaz | +%0,3 | 0,11 | %69 | 116 | GME 6%; ERNA 4%; WKHS 2% |
| DOSYA_Y (ALT) | DOĞRULAMA | 24 | -%1,0 | -0,25 | -%1,5 | -0,57 | 1,28 | -%0,43 / +%0,50 / -%0,32 | -%0,32 | tutmaz | +%0,6 | 0,18 | %68 | 175 | TDS 35%; AD 31%; CYTK 31% |
| DOSYA_Y (ALT) | KASA | 31 | -%3,7 | -0,75 | -%9,1 | -1,92 | 1,33 | -%0,53 / +%0,17 / -%0,54 | -%0,54 | tutmaz | -%8,8 | -1,91 | %68 | 194 | BKKT 6%; LASE 5%; NVAX 4% |
| DOSYA_Y (ÜST) | KEŞİF | 120 | +%1,8 | 0,85 | +%2,9 | 1,61 | 0,93 | +%0,32 / +%0,08 / +%0,05 | +%0,10 | tutmaz | +%0,8 | 0,50 | %67 | 116 | UVE 1%; MANH 1%; WSM 1% |
| DOSYA_Y (ÜST) | DOĞRULAMA | 24 | +%4,0 | 1,62 | +%4,2 | 2,33 | 0,90 | +%0,65 / +%0,09 / +%0,26 | +%0,26 | tutmaz | -%0,6 | -0,19 | %62 | 175 | APLD 6%; PBF 5%; ACLS 5% |
| DOSYA_Y (ÜST) | KASA | 31 | +%2,3 | 0,53 | +%2,7 | 0,69 | 0,98 | +%1,04 / -%0,13 / -%0,42 | -%0,42 | tutmaz | -%1,9 | -0,55 | %64 | 194 | APP 3%; SEZL 3%; WDC 3% |
| D_ASSET_TURN (ALT) | KEŞİF | 120 | +%4,3 | 1,66 | +%1,6 | 0,80 | 1,18 | +%0,07 / +%0,33 / +%0,68 | +%0,78 | tutmaz | +%2,7 | 1,29 | %40 | 108 | GME 5%; ERNA 3%; NXH 2% |
| D_ASSET_TURN (ALT) | DOĞRULAMA | 24 | -%3,6 | -1,28 | -%3,8 | -1,40 | 1,10 | -%0,47 / +%0,26 / -%0,70 | -%0,70 | tutmaz | -%5,7 | -2,95 | %40 | 172 | — |
| D_ASSET_TURN (ALT) | KASA | 31 | -%7,3 | -2,12 | -%10,0 | -2,93 | 1,17 | -%0,83 / -%0,37 / -%0,60 | -%0,60 | tutmaz | -%11,6 | -2,74 | %39 | 194 | MNTS 5%; NVAX 5%; PSIX 4% |
| D_ASSET_TURN (ÜST) | KEŞİF | 120 | -%0,9 | -0,60 | -%2,5 | -1,64 | 1,10 | -%0,14 / -%0,08 / -%0,01 | +%0,16 | tutmaz | -%1,8 | -1,24 | %43 | 108 | CLSK 2%; DXCM 2%; TREE 2% |
| D_ASSET_TURN (ÜST) | DOĞRULAMA | 24 | +%5,8 | 1,64 | +%5,7 | 1,59 | 1,09 | +%0,13 / +%0,45 / +%0,88 | +%0,88 | tutmaz | +%1,4 | 0,47 | %37 | 172 | SMCI 6%; CDLX 5%; BLBD 5% |
| D_ASSET_TURN (ÜST) | KASA | 31 | +%11,6 | 2,95 | +%7,4 | 2,02 | 1,25 | +%1,30 / +%1,14 / +%0,43 | +%0,43 | TUTAR | +%7,5 | 1,61 | %42 | 194 | BKKT 3%; WGS 3%; DAVE 2% |
| EARN_STREAK (ALT) | KEŞİF | 120 | +%0,8 | 0,28 | -%2,3 | -0,90 | 1,20 | +%0,19 / +%0,24 / -%0,24 | -%0,14 | tutmaz | +%0,8 | 0,45 | %51 | 134 | ERNA 3%; FATE 1%; NTLA 1% |
| EARN_STREAK (ALT) | DOĞRULAMA | 24 | -%9,1 | -1,84 | -%9,3 | -2,03 | 1,09 | -%1,12 / -%0,11 / -%1,05 | -%1,05 | tutmaz | -%7,2 | -1,41 | %54 | 193 | — |
| EARN_STREAK (ALT) | KASA | 31 | +%1,8 | 0,33 | -%0,6 | -0,10 | 1,14 | -%0,93 / +%1,15 / +%0,35 | +%0,35 | tutmaz | -%1,6 | -0,36 | %41 | 217 | CAPR 4%; PRAX 3%; COGT 3% |
| EAR_ANN (ALT) | KEŞİF | 120 | +%2,7 | 0,93 | -%1,7 | -0,77 | 1,30 | +%0,15 / +%0,08 / +%0,46 | +%0,47 | tutmaz | +%1,7 | 1,05 | %88 | 135 | GME 5%; WKHS 2%; AMC 1% |
| EAR_ANN (ALT) | DOĞRULAMA | 24 | +%0,4 | 0,07 | -%0,2 | -0,05 | 1,30 | -%0,32 / +%1,02 / -%0,62 | -%0,62 | tutmaz | +%0,9 | 0,20 | %88 | 194 | RYTM 23%; CDLX 18%; FDMT 18% |
| EAR_ANN (ALT) | KASA | 31 | -%3,0 | -0,87 | -%6,2 | -1,73 | 1,19 | -%0,22 / -%0,29 / -%0,24 | -%0,24 | tutmaz | -%6,3 | -1,35 | %83 | 218 | BKKT 5%; CRDO 4%; BE 3% |
| EAR_ANN (ÜST) | KEŞİF | 120 | +%0,5 | 0,19 | -%2,3 | -1,11 | 1,19 | -%0,13 / +%0,06 / +%0,18 | +%0,35 | tutmaz | -%0,1 | -0,08 | %86 | 135 | TNDM 1%; DXCM 1%; GRWG 1% |
| EAR_ANN (ÜST) | DOĞRULAMA | 24 | -%8,4 | -1,84 | -%8,6 | -1,94 | 1,08 | -%0,92 / -%0,34 / -%0,84 | -%0,84 | tutmaz | -%5,9 | -1,49 | %87 | 194 | — |
| EAR_ANN (ÜST) | KASA | 31 | -%1,3 | -0,37 | -%7,3 | -1,54 | 1,36 | +%0,47 / -%0,12 / -%0,73 | -%0,73 | tutmaz | -%9,8 | -2,53 | %82 | 218 | AGL 5%; BAND 2%; CVNA 2% |
| EAR_FILE (ALT) | KEŞİF | 120 | +%2,3 | 0,71 | -%2,6 | -1,09 | 1,33 | +%0,09 / +%0,15 / +%0,34 | +%0,43 | tutmaz | +%1,3 | 0,90 | %80 | 143 | GME 5%; WKHS 2%; SRPT 1% |
| EAR_FILE (ALT) | DOĞRULAMA | 24 | -%1,4 | -0,29 | -%1,8 | -0,42 | 1,26 | -%0,16 / +%0,56 / -%0,73 | -%0,73 | tutmaz | -%0,5 | -0,12 | %83 | 201 | RYTM 48%; CDLX 39%; TDS 36% |
| EAR_FILE (ALT) | KASA | 31 | -%5,1 | -1,68 | -%8,8 | -2,94 | 1,23 | -%0,27 / -%0,43 / -%0,58 | -%0,58 | tutmaz | -%8,9 | -2,05 | %81 | 224 | BKKT 5%; ASTS 4%; NVAX 4% |
| EAR_FILE (ÜST) | KEŞİF | 120 | +%1,8 | 0,66 | -%1,3 | -0,55 | 1,20 | -%0,18 / +%0,18 / +%0,45 | +%0,59 | tutmaz | +%1,0 | 0,51 | %77 | 143 | ERNA 3%; AMRN 1%; TNDM 1% |
| EAR_FILE (ÜST) | DOĞRULAMA | 24 | -%7,0 | -1,95 | -%7,2 | -2,11 | 1,09 | -%0,70 / -%0,24 / -%0,83 | -%0,83 | tutmaz | -%5,5 | -1,93 | %82 | 201 | — |
| EAR_FILE (ÜST) | KASA | 31 | -%1,7 | -0,48 | -%7,2 | -1,48 | 1,33 | +%0,26 / +%0,13 / -%0,86 | -%0,86 | tutmaz | -%8,7 | -1,85 | %78 | 224 | AGL 5%; ERAS 3%; PRCH 3% |
| EAR_VOL (ALT) | KEŞİF | 120 | -%4,0 | -1,77 | -%4,8 | -1,89 | 1,06 | +%0,01 / -%0,41 / -%0,59 | -%0,56 | tutmaz | -%2,6 | -1,22 | %91 | 135 | ERNA 5%; GERN 2%; ACAD 2% |
| EAR_VOL (ALT) | DOĞRULAMA | 24 | -%7,4 | -2,54 | -%7,4 | -2,54 | 1,00 | -%0,65 / -%1,24 / +%0,03 | +%0,03 | tutmaz | -%8,1 | -2,51 | %90 | 194 | — |
| EAR_VOL (ALT) | KASA | 31 | -%4,7 | -0,93 | -%4,6 | -0,99 | 1,00 | -%0,85 / +%0,59 / -%0,85 | -%0,85 | tutmaz | -%4,9 | -1,05 | %87 | 218 | OLMA 5%; SRRK 4%; RDW 4% |
| EAR_VOL (ÜST) | KEŞİF | 120 | +%1,6 | 1,14 | +%0,4 | 0,36 | 1,08 | +%0,10 / +%0,07 / +%0,23 | +%0,22 | tutmaz | +%1,1 | 0,89 | %82 | 135 | WKHS 2%; W 1%; NXH 1% |
| EAR_VOL (ÜST) | DOĞRULAMA | 24 | -%1,1 | -0,34 | -%1,2 | -0,40 | 1,06 | -%0,46 / +%0,68 / -%0,49 | -%0,49 | tutmaz | -%3,6 | -1,31 | %78 | 194 | LNTH 30%; AI 22%; AMTX 18% |
| EAR_VOL (ÜST) | KASA | 31 | -%4,6 | -2,02 | -%5,9 | -2,31 | 1,08 | +%0,18 / -%0,87 / -%0,51 | -%0,51 | tutmaz | -%4,5 | -1,66 | %80 | 218 | LASE 4%; PRAX 3%; NLST 2% |
| EP (ALT) | KEŞİF | 120 | +%3,3 | 0,57 | -%4,5 | -1,04 | 1,51 | +%0,35 / -%0,07 / +%0,55 | +%0,96 | tutmaz | +%2,1 | 0,59 | %40 | 127 | GME 6%; ERNA 3%; ALNY 3% |
| EP (ALT) | DOĞRULAMA | 24 | -%7,0 | -0,93 | -%7,8 | -1,39 | 1,45 | -%0,87 / -%0,74 / -%0,13 | -%0,13 | tutmaz | -%0,0 | -0,00 | %53 | 181 | — |
| EP (ALT) | KASA | 31 | +%2,1 | 0,26 | -%6,8 | -1,17 | 1,54 | -%0,29 / +%0,82 / +%0,05 | +%0,05 | tutmaz | -%6,1 | -1,67 | %51 | 202 | CAPR 8%; AGL 4%; PRAX 3% |
| EV_EBITDA (ALT) | KEŞİF | 120 | +%3,4 | 1,07 | +%3,7 | 1,05 | 0,99 | +%0,14 / +%0,55 / +%0,16 | +%0,19 | tutmaz | +%3,9 | 2,37 | %34 | 64 | NFLX 4%; MPWR 3%; ENPH 3% |
| EV_EBITDA (ALT) | DOĞRULAMA | 24 | -%4,1 | -0,82 | -%4,2 | -0,84 | 1,06 | -%0,33 / +%0,69 / -%1,38 | -%1,38 | tutmaz | -%5,1 | -1,72 | %38 | 82 | — |
| EV_EBITDA (ÜST) | KEŞİF | 120 | +%0,5 | 0,13 | -%4,1 | -1,05 | 1,30 | -%0,14 / -%0,13 / +%0,38 | +%0,43 | tutmaz | -%1,8 | -0,76 | %36 | 64 | AMKR 3%; NBR 2%; ARCB 2% |
| EV_EBITDA (ÜST) | DOĞRULAMA | 24 | +%10,4 | 1,60 | +%10,4 | 1,55 | 1,03 | +%0,86 / -%0,47 / +%2,23 | +%2,23 | tutmaz | +%4,0 | 0,96 | %33 | 82 | AD 6%; BTU 6%; AMR 6% |
| E_424B5 (ALT) | KEŞİF | 120 | -%1,7 | -0,83 | -%1,5 | -0,88 | 0,99 | -%0,10 / -%0,51 / +%0,18 | +%0,18 | tutmaz | -%1,7 | -0,68 | %101 | 97 | GME 9%; AMC 4%; PACB 2% |
| E_424B5 (ALT) | DOĞRULAMA | 24 | -%12,4 | -2,42 | -%12,3 | -2,54 | 0,94 | +%0,06 / -%1,89 / -%1,28 | -%1,28 | tutmaz | -%12,4 | -3,39 | %106 | 89 | — |
| E_424B5 (ALT) | KASA | 31 | -%5,5 | -1,58 | -%5,3 | -1,32 | 0,99 | +%0,20 / -%0,44 / -%1,19 | -%1,19 | tutmaz | -%2,0 | -0,42 | %106 | 141 | RGTI 10%; BKKT 9%; PRAX 6% |
| E_DIV_OMIT (ALT) | KEŞİF | 30 | — | — | — | — | — | — / — / — | — | tutmaz | — | — | %59 | 35 | GME 22%; RYAM 15%; GPRE 8% |
| E_DIV_OMIT (ALT) | DOĞRULAMA | 0 | — | — | — | — | — | — / — / — | — | tutmaz | — | — | — | — | — |
| E_IPO_3Y (ALT) | KEŞİF | 120 | +%1,0 | 0,23 | -%3,1 | -0,79 | 1,27 | +%0,61 / +%0,15 / -%0,52 | -%0,40 | tutmaz | +%0,8 | 0,50 | %25 | 127 | PBYI 3%; VIPS 2%; PCRX 2% |
| E_IPO_3Y (ALT) | DOĞRULAMA | 24 | -%12,9 | -2,01 | -%13,3 | -2,50 | 1,25 | -%1,48 / -%1,13 / -%0,61 | -%0,61 | tutmaz | -%9,4 | -3,92 | %29 | 279 | — |
| E_IPO_3Y (ALT) | KASA | 31 | +%0,4 | 0,10 | -%4,9 | -1,19 | 1,32 | +%0,15 / +%0,19 / -%0,25 | -%0,25 | tutmaz | -%1,0 | -0,19 | %35 | 115 | SEZL 8%; NUTX 7%; HSAI 7% |
| E_RSPLIT (ALT) | KEŞİF | 64 | -%19,7 | -1,50 | -%30,0 | -2,69 | 1,51 | -%1,77 / -%2,65 / -%0,50 | -%1,07 | tutmaz | -%24,4 | -2,61 | %63 | 18 | NVAX 389%; TNDM 326%; ERNA 283% |
| E_RSPLIT (ALT) | DOĞRULAMA | 24 | -%61,3 | -5,15 | -%62,2 | -5,04 | 1,49 | -%5,14 / -%5,50 / -%4,69 | -%4,69 | tutmaz | -%55,6 | -4,03 | %67 | 17 | — |
| E_RSPLIT (ALT) | KASA | 31 | -%39,7 | -3,67 | -%44,4 | -4,00 | 1,29 | -%2,64 / -%3,67 / -%3,68 | -%3,68 | tutmaz | -%42,9 | -3,41 | %73 | 43 | — |
| E_S3 (ALT) | KEŞİF | 120 | -%1,9 | -0,96 | -%2,3 | -1,28 | 1,03 | -%0,08 / -%0,48 / +%0,09 | +%0,18 | tutmaz | -%1,8 | -0,81 | %79 | 103 | GME 8%; AMC 3%; WKHS 3% |
| E_S3 (ALT) | DOĞRULAMA | 24 | -%5,4 | -1,86 | -%5,5 | -1,90 | 1,06 | -%0,31 / -%1,08 / +%0,03 | +%0,03 | tutmaz | -%6,6 | -2,47 | %80 | 123 | — |
| E_S3 (ALT) | KASA | 31 | -%7,5 | -1,74 | -%10,6 | -2,44 | 1,19 | +%0,37 / -%0,51 / -%1,83 | -%1,83 | tutmaz | -%12,8 | -2,69 | %81 | 165 | CAPR 16%; ACHR 6%; HYMC 5% |
| F_SCORE (ALT) | KEŞİF | 120 | +%0,9 | 0,22 | -%3,4 | -0,89 | 1,28 | +%0,16 / -%0,18 / +%0,24 | +%0,54 | tutmaz | +%1,3 | 0,55 | %35 | 119 | ERNA 3%; PBYI 3%; ALNY 3% |
| F_SCORE (ALT) | DOĞRULAMA | 24 | -%8,4 | -1,22 | -%8,8 | -1,51 | 1,23 | -%1,07 / +%0,20 / -%1,23 | -%1,23 | tutmaz | -%3,6 | -0,60 | %42 | 196 | — |
| F_SCORE (ALT) | KASA | 31 | -%1,2 | -0,23 | -%7,7 | -1,79 | 1,39 | +%0,10 / -%0,02 / -%0,39 | -%0,39 | tutmaz | -%3,0 | -0,80 | %44 | 221 | ASTS 5%; RGTI 4%; CELC 4% |
| GAP_OVN (ALT) | KEŞİF | 120 | -%3,1 | -1,52 | -%5,8 | -2,57 | 1,18 | -%0,17 / -%0,32 / -%0,29 | -%0,28 | tutmaz | -%3,6 | -1,90 | %176 | 164 | ERNA 3%; APA 1%; RRC 1% |
| GAP_OVN (ALT) | DOĞRULAMA | 24 | -%7,8 | -1,52 | -%8,1 | -2,01 | 1,19 | -%1,33 / +%0,02 / -%0,64 | -%0,64 | tutmaz | -%8,1 | -2,22 | %172 | 227 | — |
| GAP_OVN (ALT) | KASA | 31 | -%0,3 | -0,08 | -%1,4 | -0,38 | 1,07 | -%0,69 / +%0,47 / +%0,20 | +%0,20 | tutmaz | -%3,8 | -0,64 | %179 | 252 | AGL 4%; BE 3%; REPL 2% |
| GAP_OVN (ÜST) | KEŞİF | 120 | -%3,8 | -1,05 | -%6,7 | -1,93 | 1,19 | -%0,26 / -%0,23 / -%0,45 | -%0,30 | tutmaz | -%3,7 | -2,10 | %166 | 164 | WKHS 2%; TSLA 2%; RIOT 2% |
| GAP_OVN (ÜST) | DOĞRULAMA | 24 | -%7,3 | -1,52 | -%7,6 | -1,47 | 1,15 | +%0,11 / -%1,75 / -%0,19 | -%0,19 | tutmaz | -%4,7 | -1,15 | %170 | 227 | — |
| GAP_OVN (ÜST) | KASA | 31 | -%5,8 | -1,18 | -%9,5 | -1,80 | 1,22 | +%0,40 / -%0,57 / -%1,36 | -%1,36 | tutmaz | -%4,4 | -0,56 | %169 | 252 | RGTI 4%; RCAT 4%; LASE 4% |
| GP_A (ALT) | KEŞİF | 120 | -%3,2 | -0,66 | -%9,0 | -3,42 | 1,38 | -%0,07 / -%0,59 / -%0,15 | -%0,03 | tutmaz | -%4,0 | -1,41 | %26 | 85 | WKHS 4%; HALO 4%; TSLA 4% |
| GP_A (ALT) | DOĞRULAMA | 24 | -%11,4 | -1,60 | -%12,2 | -1,44 | 1,44 | -%0,29 / -%1,04 / -%1,52 | -%1,52 | tutmaz | -%7,9 | -1,10 | %30 | 120 | — |
| GP_A (ALT) | KASA | 31 | +%4,3 | 0,70 | -%3,3 | -0,51 | 1,46 | +%0,56 / +%1,48 / -%1,00 | -%1,00 | tutmaz | -%7,2 | -0,75 | %33 | 131 | RGTI 7%; RKLB 5%; APLD 5% |
| GP_A (ÜST) | KEŞİF | 120 | +%5,2 | 1,39 | +%5,2 | 1,51 | 1,00 | +%0,08 / +%0,55 / +%0,66 | +%0,67 | tutmaz | +%4,2 | 1,23 | %21 | 85 | GME 8%; AMRN 3%; MED 2% |
| GP_A (ÜST) | DOĞRULAMA | 24 | -%2,6 | -0,42 | -%2,6 | -0,42 | 1,00 | -%1,79 / +%0,83 / +%0,31 | +%0,31 | tutmaz | -%6,2 | -1,07 | %22 | 120 | — |
| GP_A (ÜST) | KASA | 31 | -%7,7 | -1,10 | -%7,7 | -1,17 | 1,00 | +%0,14 / -%1,09 / -%1,06 | -%1,06 | tutmaz | -%6,2 | -0,83 | %23 | 131 | HIMS 10%; CORT 9%; REAL 7% |
| HIGH52 (ALT) | KEŞİF | 120 | -%4,3 | -0,76 | -%15,1 | -3,32 | 1,71 | -%0,38 / -%0,21 / -%0,48 | -%0,48 | tutmaz | -%6,3 | -2,05 | %62 | 164 | ERNA 4%; SRPT 3%; AMC 3% |
| HIGH52 (ALT) | DOĞRULAMA | 24 | -%12,0 | -1,06 | -%13,2 | -1,88 | 1,64 | -%2,91 / -%0,09 / +%0,01 | +%0,01 | tutmaz | -%6,1 | -0,97 | %65 | 227 | — |
| HIGH52 (ALT) | KASA | 31 | -%4,7 | -0,67 | -%13,1 | -1,96 | 1,51 | -%0,24 / -%0,12 / -%0,84 | -%0,84 | tutmaz | -%11,1 | -1,43 | %70 | 252 | CAPR 7%; BKKT 6%; AGL 5% |
| IND_LEAD_BIG (ALT) | KEŞİF | 120 | -%3,6 | -1,15 | -%7,2 | -3,03 | 1,24 | -%0,73 / -%0,24 / +%0,08 | +%0,16 | tutmaz | -%5,2 | -1,72 | %173 | 61 | TBCH 3%; AAOI 2%; CANN 2% |
| IND_LEAD_BIG (ALT) | DOĞRULAMA | 24 | -%1,0 | -0,12 | -%1,3 | -0,16 | 1,16 | -%1,16 / +%1,95 / -%1,04 | -%1,04 | tutmaz | -%2,5 | -0,35 | %176 | 93 | LASR 24%; MVIS 22%; MARA 22% |
| IND_LEAD_BIG (ALT) | KASA | 31 | -%12,3 | -2,56 | -%17,6 | -3,22 | 1,32 | -%0,99 / -%0,36 / -%1,74 | -%1,74 | tutmaz | -%28,0 | -4,76 | %169 | 105 | AGL 15%; UAVS 14%; ACHR 12% |
| IND_LEAD_BIG (ÜST) | KEŞİF | 120 | -%3,7 | -1,27 | -%4,8 | -2,16 | 1,07 | -%0,66 / -%0,18 / -%0,10 | -%0,20 | tutmaz | -%1,7 | -0,76 | %181 | 61 | MARA 3%; RIOT 3%; PENN 2% |
| IND_LEAD_BIG (ÜST) | DOĞRULAMA | 24 | +%2,6 | 0,23 | +%2,6 | 0,22 | 1,04 | +%1,34 / -%1,84 / +%1,15 | +%1,15 | tutmaz | +%1,6 | 0,19 | %156 | 93 | LMND 12%; ANF 10%; WING 9% |
| IND_MOM_6 (ALT) | KEŞİF | 120 | -%8,1 | -2,91 | -%12,1 | -3,65 | 1,27 | -%1,01 / -%0,64 / -%0,37 | -%0,45 | tutmaz | -%8,9 | -2,37 | %85 | 111 | PENN 2%; MTDR 2%; CZR 2% |
| IND_MOM_6 (ALT) | DOĞRULAMA | 24 | -%2,9 | -0,30 | -%3,5 | -0,46 | 1,32 | -%2,37 / +%0,07 / +%1,57 | +%1,57 | tutmaz | -%5,0 | -0,97 | %97 | 159 | PGY 1487%; EYPT 1163%; TMDX 460% |
| IND_MOM_6 (ALT) | KASA | 31 | +%5,4 | 0,60 | +%5,0 | 0,59 | 1,02 | +%0,78 / -%0,58 / +%1,11 | +%1,11 | tutmaz | -%0,4 | -0,05 | %85 | 178 | ASTS 3%; HNST 2%; ULCC 2% |
| IND_MOM_6 (ÜST) | KEŞİF | 120 | +%0,8 | 0,28 | +%0,3 | 0,10 | 1,04 | +%0,41 / -%0,43 / +%0,22 | +%0,46 | tutmaz | +%1,7 | 0,48 | %102 | 111 | MCRB 2%; RIOT 2%; MARA 2% |
| IND_MOM_6 (ÜST) | DOĞRULAMA | 24 | +%8,3 | 0,96 | +%8,3 | 0,95 | 1,02 | +%2,25 / +%0,44 / -%0,61 | -%0,61 | tutmaz | +%7,1 | 1,14 | %91 | 159 | TRMD 5%; UPST 5%; HOV 3% |
| ISKEW (ALT) | KEŞİF | 120 | -%3,1 | -1,96 | -%3,8 | -2,93 | 1,05 | -%0,23 / -%0,22 / -%0,34 | -%0,29 | tutmaz | -%2,5 | -1,43 | %182 | 164 | GME 6%; SRPT 1%; AMD 1% |
| ISKEW (ALT) | DOĞRULAMA | 24 | -%3,8 | -3,26 | -%3,9 | -3,20 | 1,01 | -%0,07 / -%0,51 / -%0,38 | -%0,38 | tutmaz | -%4,3 | -1,98 | %181 | 227 | FDMT 296%; EWTX 246%; VERA 223% |
| ISKEW (ALT) | KASA | 31 | -%5,7 | -2,51 | -%5,8 | -3,00 | 1,01 | -%0,59 / -%0,53 / -%0,29 | -%0,29 | tutmaz | -%6,5 | -1,74 | %182 | 252 | RGTI 5%; NEGG 3%; OKLO 3% |
| IVOL_FF3 (ALT) | KEŞİF | 120 | -%2,7 | -0,41 | -%10,4 | -1,94 | 1,51 | -%0,49 / -%0,19 / +%0,00 | +%0,38 | tutmaz | -%4,9 | -1,41 | %132 | 164 | GME 6%; ERNA 3%; AMC 2% |
| IVOL_FF3 (ALT) | DOĞRULAMA | 24 | -%13,6 | -2,60 | -%14,4 | -3,41 | 1,43 | -%1,28 / -%0,87 / -%1,24 | -%1,24 | tutmaz | -%9,4 | -2,30 | %138 | 227 | — |
| IVOL_FF3 (ALT) | KASA | 31 | -%7,3 | -1,18 | -%14,9 | -2,37 | 1,46 | +%0,46 / -%0,79 / -%1,61 | -%1,61 | tutmaz | -%9,0 | -1,10 | %137 | 252 | ASTS 8%; CAPR 7%; WGS 7% |
| LEV_MKT (ALT) | KEŞİF | 120 | -%4,4 | -1,07 | -%5,5 | -1,03 | 1,08 | -%0,14 / -%0,16 / -%0,79 | -%0,64 | tutmaz | -%3,6 | -2,73 | %30 | 140 | ACAD 3%; RIOT 3%; ALGN 3% |
| LEV_MKT (ALT) | DOĞRULAMA | 24 | -%5,3 | -1,30 | -%5,2 | -1,27 | 0,98 | -%0,09 / -%0,43 / -%0,80 | -%0,80 | tutmaz | -%4,3 | -1,68 | %33 | 196 | — |
| LEV_MKT (ALT) | KASA | 31 | +%2,0 | 0,46 | -%0,3 | -0,06 | 1,14 | +%0,25 / +%0,79 / -%0,55 | -%0,55 | tutmaz | +%0,7 | 0,17 | %34 | 218 | RGTI 5%; OKLO 4%; RCAT 4% |
| LTREV_60_13 (ÜST) | KEŞİF | 84 | +%3,6 | 0,49 | -%2,1 | -0,44 | 1,41 | -%0,29 / -%0,49 / +%1,69 | +%1,84 | tutmaz | +%3,1 | 0,67 | %45 | 151 | GME 8%; ERNA 4%; WKHS 3% |
| LTREV_60_13 (ÜST) | DOĞRULAMA | 24 | +%4,6 | 0,70 | +%4,2 | 0,57 | 1,22 | +%1,11 / +%0,58 / -%0,53 | -%0,53 | tutmaz | +%6,2 | 3,30 | %45 | 182 | EYPT 11%; AAOI 6%; HOS 6% |
| LTREV_60_13 (ÜST) | KASA | 31 | -%10,4 | -2,17 | -%15,3 | -2,91 | 1,29 | -%0,60 / -%0,33 / -%1,70 | -%1,70 | tutmaz | -%19,6 | -2,60 | %52 | 213 | QURE 12%; AEVA 11%; HYMC 8% |
| MAX5 (ALT) | KEŞİF | 120 | -%4,7 | -0,82 | -%12,4 | -2,58 | 1,51 | -%0,49 / -%0,36 / -%0,33 | -%0,02 | tutmaz | -%6,0 | -2,19 | %127 | 164 | GME 7%; ACAD 2%; PBYI 2% |
| MAX5 (ALT) | DOĞRULAMA | 24 | -%17,3 | -3,36 | -%18,0 | -4,30 | 1,42 | -%1,41 / -%1,67 / -%1,24 | -%1,24 | tutmaz | -%11,7 | -2,47 | %129 | 227 | — |
| MAX5 (ALT) | KASA | 31 | +%0,7 | 0,09 | -%9,9 | -1,16 | 1,64 | +%1,06 / +%0,44 / -%1,44 | -%1,44 | tutmaz | -%4,8 | -0,45 | %128 | 252 | ASTS 4%; RGTI 4%; WGS 3% |
| MOM_12_1 (ALT) | KEŞİF | 120 | -%3,4 | -0,69 | -%11,8 | -3,30 | 1,55 | -%0,65 / -%0,04 / -%0,17 | -%0,18 | tutmaz | -%3,0 | -1,32 | %66 | 164 | NCTY 2%; SRPT 2%; AMC 2% |
| MOM_12_1 (ALT) | DOĞRULAMA | 24 | -%16,3 | -1,58 | -%17,2 | -2,52 | 1,52 | -%3,14 / -%0,44 / -%0,50 | -%0,50 | tutmaz | -%11,6 | -2,02 | %67 | 227 | — |
| MOM_12_1 (ALT) | KASA | 31 | -%0,8 | -0,13 | -%4,5 | -0,76 | 1,22 | -%0,16 / -%0,54 / +%0,50 | +%0,50 | tutmaz | +%1,0 | 0,24 | %72 | 252 | CAPR 6%; AGL 4%; BKKT 3% |
| MOM_12_1 (ÜST) | KEŞİF | 120 | +%3,6 | 0,90 | +%1,3 | 0,33 | 1,16 | +%0,38 / -%0,03 / +%0,56 | +%0,78 | tutmaz | +%1,1 | 0,42 | %64 | 164 | GME 4%; WKHS 2%; ACAD 1% |
| MOM_12_1 (ÜST) | DOĞRULAMA | 24 | +%4,6 | 0,87 | +%4,6 | 0,88 | 1,00 | +%1,50 / -%0,23 / -%0,12 | -%0,12 | tutmaz | +%4,0 | 1,55 | %64 | 227 | SMCI 10%; EYPT 9%; MOD 6% |
| MOM_12_1 (ÜST) | KASA | 31 | +%3,8 | 0,55 | -%5,2 | -0,60 | 1,55 | +%0,37 / +%1,94 / -%1,36 | -%1,36 | tutmaz | -%5,5 | -0,92 | %64 | 252 | DAVE 3%; APP 3%; RKLB 2% |
| MOM_6_1 (ALT) | KEŞİF | 120 | -%6,7 | -1,78 | -%12,6 | -3,71 | 1,39 | -%0,46 / -%0,31 / -%0,91 | -%0,95 | tutmaz | -%7,5 | -2,93 | %89 | 164 | NCTY 2%; AMRN 2%; MTDR 1% |
| MOM_6_1 (ALT) | DOĞRULAMA | 24 | -%15,1 | -1,45 | -%16,0 | -2,25 | 1,49 | -%3,17 / -%0,29 / -%0,31 | -%0,31 | tutmaz | -%11,9 | -1,72 | %87 | 227 | — |
| MOM_6_1 (ALT) | KASA | 31 | +%0,1 | 0,01 | -%4,2 | -0,57 | 1,26 | +%0,36 / -%1,15 / +%0,78 | +%0,78 | tutmaz | -%4,5 | -0,71 | %92 | 252 | AGL 4%; CAPR 3%; SRRK 3% |
| MOM_6_1 (ÜST) | KEŞİF | 120 | +%4,0 | 0,99 | +%0,7 | 0,23 | 1,22 | +%0,33 / +%0,26 / +%0,41 | +%0,68 | tutmaz | +%2,1 | 0,69 | %88 | 164 | GME 4%; MCRB 1%; ARWR 1% |
| MOM_6_1 (ÜST) | DOĞRULAMA | 24 | -%1,7 | -0,26 | -%1,7 | -0,26 | 0,96 | +%1,38 / -%0,92 / -%0,90 | -%0,90 | tutmaz | -%1,9 | -0,32 | %93 | 227 | VKTX 36%; SMCI 33%; AAOI 28% |
| MOM_6_1 (ÜST) | KASA | 31 | -%5,6 | -0,66 | -%12,4 | -1,22 | 1,41 | -%0,02 / +%1,08 / -%2,51 | -%2,51 | tutmaz | -%10,7 | -1,66 | %87 | 252 | AXTI 4%; MSTR 4%; RCAT 3% |
| MOM_FIP (ALT) | KEŞİF | 120 | -%5,2 | -3,29 | -%6,9 | -4,08 | 1,11 | -%0,46 / -%0,14 / -%0,70 | -%0,84 | tutmaz | -%3,6 | -2,79 | %84 | 164 | LAB 1%; SGI 1%; CHEF 1% |
| MOM_FIP (ALT) | DOĞRULAMA | 24 | -%6,3 | -2,54 | -%6,4 | -2,87 | 1,06 | -%0,79 / -%0,76 / -%0,02 | -%0,02 | tutmaz | -%7,9 | -3,68 | %81 | 227 | — |
| MOM_FIP (ALT) | KASA | 31 | -%2,3 | -0,64 | -%0,3 | -0,08 | 0,88 | -%0,74 / -%0,04 / +%0,26 | +%0,26 | tutmaz | -%4,0 | -1,51 | %81 | 252 | CAPR 4%; OLMA 3%; PRAX 3% |
| MOM_INT_12_7 (ALT) | KEŞİF | 120 | +%0,2 | 0,05 | -%7,4 | -2,22 | 1,50 | -%0,20 / -%0,03 / +%0,29 | +%0,37 | tutmaz | +%0,6 | 0,24 | %83 | 164 | TNDM 1%; CLSK 1%; NXH 1% |
| MOM_INT_12_7 (ALT) | DOĞRULAMA | 24 | -%21,7 | -3,25 | -%22,4 | -4,61 | 1,36 | -%2,33 / -%1,75 / -%1,35 | -%1,35 | tutmaz | -%16,7 | -5,41 | %81 | 227 | — |
| MOM_INT_12_7 (ALT) | KASA | 31 | -%2,4 | -0,40 | -%6,6 | -1,11 | 1,25 | -%0,20 / +%0,02 / -%0,43 | -%0,43 | tutmaz | +%0,7 | 0,11 | %87 | 252 | CAPR 7%; LASE 4%; AGL 3% |
| MOM_INT_12_7 (ÜST) | KEŞİF | 120 | +%0,5 | 0,16 | -%1,0 | -0,28 | 1,09 | +%0,18 / -%0,11 / +%0,05 | +%0,21 | tutmaz | -%1,1 | -0,64 | %80 | 164 | WKHS 2%; VIPS 1%; PBYI 1% |
| MOM_INT_12_7 (ÜST) | DOĞRULAMA | 24 | +%4,2 | 0,96 | +%4,1 | 0,97 | 1,05 | +%0,74 / +%0,04 / +%0,28 | +%0,28 | tutmaz | +%3,1 | 1,34 | %84 | 227 | SMCI 10%; EYPT 8%; KRUS 5% |
| MOM_INT_12_7 (ÜST) | KASA | 31 | +%10,3 | 1,89 | +%1,8 | 0,31 | 1,51 | +%1,00 / +%1,54 / +%0,01 | +%0,01 | tutmaz | -%0,7 | -0,11 | %80 | 252 | QURE 2%; RCAT 2%; APP 2% |
| NDF_BS (ALT) | KEŞİF | 120 | +%4,5 | 3,29 | +%2,6 | 2,08 | 1,12 | +%0,63 / +%0,16 / +%0,32 | +%0,35 | TUTAR | +%4,2 | 2,15 | %39 | 78 | UI 2%; ENPH 2%; TSLA 2% |
| NDF_BS (ALT) | DOĞRULAMA | 24 | -%2,8 | -0,85 | -%3,0 | -1,00 | 1,13 | -%0,66 / +%0,51 / -%0,54 | -%0,54 | tutmaz | -%4,7 | -1,71 | %40 | 114 | — |
| NDF_BS (ALT) | KASA | 31 | +%5,5 | 2,35 | +%3,8 | 1,56 | 1,10 | +%0,65 / +%0,59 / +%0,11 | +%0,11 | tutmaz | +%0,4 | 0,16 | %40 | 129 | ASTS 8%; WGS 4%; URGN 4% |
| NDF_BS (ÜST) | KEŞİF | 120 | +%0,7 | 0,42 | -%0,4 | -0,26 | 1,08 | +%0,18 / -%0,12 / +%0,13 | +%0,17 | tutmaz | +%0,1 | 0,04 | %45 | 78 | PPC 2%; CDLX 2%; AMD 2% |
| NDF_BS (ÜST) | DOĞRULAMA | 24 | +%3,9 | 1,81 | +%3,9 | 1,76 | 1,01 | +%0,56 / +%0,10 / +%0,32 | +%0,32 | tutmaz | +%0,5 | 0,19 | %42 | 114 | EYPT 19%; TH 10%; XTKGF 9% |
| NDF_BS (ÜST) | KASA | 31 | +%0,1 | 0,03 | -%0,7 | -0,31 | 1,05 | +%0,39 / -%0,48 / +%0,07 | +%0,07 | tutmaz | -%1,3 | -0,29 | %42 | 129 | QURE 7%; RGTI 6%; VISN 4% |
| NEF (ALT) | KEŞİF | 120 | -%3,6 | -0,97 | -%5,9 | -1,43 | 1,16 | -%0,17 / -%0,35 / -%0,37 | -%0,24 | tutmaz | -%2,5 | -1,25 | %29 | 136 | WKHS 3%; ACAD 3%; MCRB 3% |
| NEF (ALT) | DOĞRULAMA | 24 | -%10,7 | -2,18 | -%11,1 | -2,73 | 1,20 | -%1,14 / -%0,63 / -%0,91 | -%0,91 | tutmaz | -%8,6 | -2,03 | %38 | 210 | — |
| NEF (ALT) | KASA | 31 | -%0,4 | -0,08 | -%5,7 | -0,92 | 1,32 | +%0,35 / +%0,91 / -%1,41 | -%1,41 | tutmaz | -%6,9 | -1,17 | %34 | 235 | CAPR 6%; ASTS 6%; RGTI 5% |
| NEF (ÜST) | KEŞİF | 120 | +%2,2 | 1,20 | +%5,0 | 4,51 | 0,82 | +%0,09 / +%0,15 / +%0,32 | +%0,33 | tutmaz | +%2,3 | 2,18 | %17 | 136 | MANH 1%; AXON 1%; SPGI 1% |
| NEF (ÜST) | DOĞRULAMA | 24 | +%4,9 | 2,62 | +%5,2 | 2,81 | 0,87 | +%0,28 / +%0,56 / +%0,39 | +%0,39 | TUTAR | +%0,2 | 0,08 | %17 | 210 | BLDR 4%; DECK 4%; NVDA 4% |
| NEF (ÜST) | KASA | 31 | -%4,3 | -1,18 | -%0,2 | -0,06 | 0,75 | -%0,26 / -%0,60 / -%0,22 | -%0,22 | tutmaz | -%4,2 | -1,42 | %18 | 235 | APP 4%; UI 3%; OKLO 2% |
| NET_PAYOUT_YLD (ALT) | KEŞİF | 120 | -%3,6 | -1,25 | -%5,5 | -1,75 | 1,13 | -%0,26 / -%0,38 / -%0,25 | -%0,12 | tutmaz | -%2,4 | -1,28 | %30 | 130 | ACAD 3%; WKHS 3%; MCRB 3% |
| NET_PAYOUT_YLD (ALT) | DOĞRULAMA | 24 | -%8,2 | -1,97 | -%8,5 | -2,47 | 1,21 | -%0,80 / -%0,33 / -%0,92 | -%0,92 | tutmaz | -%6,2 | -2,00 | %38 | 198 | — |
| NET_PAYOUT_YLD (ALT) | KASA | 31 | -%1,8 | -0,47 | -%6,3 | -1,26 | 1,27 | -%0,02 / +%0,38 / -%0,82 | -%0,82 | tutmaz | -%7,1 | -1,24 | %36 | 219 | CAPR 7%; AAOI 4%; QBTS 4% |
| NOA (ALT) | KEŞİF | 120 | -%3,8 | -1,87 | -%4,2 | -1,90 | 1,03 | +%0,19 / -%0,37 / -%0,77 | -%0,73 | tutmaz | -%3,5 | -1,84 | %34 | 132 | MARA 2%; FLGT 1%; IIPR 1% |
| NOA (ALT) | DOĞRULAMA | 24 | -%6,0 | -1,81 | -%6,1 | -1,91 | 1,06 | -%0,91 / -%0,32 / -%0,27 | -%0,27 | tutmaz | -%7,8 | -4,12 | %35 | 178 | — |
| NOA (ALT) | KASA | 31 | -%3,1 | -1,23 | -%3,2 | -1,10 | 1,01 | +%0,01 / -%0,23 / -%0,56 | -%0,56 | tutmaz | -%8,0 | -3,68 | %33 | 198 | MSTR 4%; CELC 4%; ORKA 4% |
| NOA (ÜST) | KEŞİF | 120 | +%0,8 | 0,26 | -%1,2 | -0,37 | 1,13 | +%0,28 / +%0,19 / -%0,28 | -%0,32 | tutmaz | +%0,5 | 0,31 | %30 | 132 | WKHS 2%; MCRB 2%; LNWO 2% |
| NOA (ÜST) | DOĞRULAMA | 24 | -%3,3 | -0,91 | -%3,4 | -0,95 | 1,03 | -%0,25 / -%0,54 / -%0,04 | -%0,04 | tutmaz | -%1,7 | -0,36 | %34 | 178 | — |
| NOA (ÜST) | KASA | 31 | +%3,6 | 0,57 | +%0,2 | 0,03 | 1,21 | +%0,94 / +%1,37 / -%1,48 | -%1,48 | tutmaz | -%3,7 | -0,61 | %34 | 198 | QURE 4%; BKKT 4%; LUNR 3% |
| NSI_1Y (ALT) | KEŞİF | 120 | -%3,1 | -0,71 | -%7,1 | -1,73 | 1,27 | -%0,23 / -%0,38 / -%0,15 | +%0,09 | tutmaz | -%3,2 | -1,37 | %36 | 140 | NVAX 3%; WKHS 3%; ALNY 3% |
| NSI_1Y (ALT) | DOĞRULAMA | 24 | -%10,3 | -2,70 | -%10,6 | -2,56 | 1,19 | -%0,20 / -%1,07 / -%1,30 | -%1,30 | tutmaz | -%9,1 | -4,01 | %41 | 198 | — |
| NSI_1Y (ALT) | KASA | 31 | -%3,2 | -0,53 | -%8,9 | -1,39 | 1,35 | -%0,24 / +%0,80 / -%1,36 | -%1,36 | tutmaz | -%9,0 | -1,43 | %42 | 222 | RGTI 6%; RCAT 5%; AAOI 5% |
| NSI_5Y (ALT) | KEŞİF | 84 | -%4,0 | -1,08 | -%6,0 | -1,80 | 1,14 | -%0,60 / -%0,41 / -%0,00 | -%0,15 | tutmaz | -%3,1 | -1,04 | %29 | 116 | ENPH 6%; WKHS 5%; NCTY 5% |
| NSI_5Y (ALT) | DOĞRULAMA | 24 | -%8,1 | -1,87 | -%8,3 | -1,77 | 1,11 | +%0,19 / -%0,95 / -%1,27 | -%1,27 | tutmaz | -%6,3 | -1,76 | %28 | 157 | — |
| NSI_5Y (ALT) | KASA | 31 | +%4,8 | 0,85 | +%1,2 | 0,23 | 1,22 | +%0,03 / +%0,82 / +%0,38 | +%0,38 | tutmaz | -%3,1 | -0,76 | %30 | 180 | CAPR 6%; AAOI 4%; RCAT 3% |
| NT_LATE (ALT) | KEŞİF | 47 | -%11,2 | -1,12 | -%16,7 | -1,71 | 1,29 | +%0,92 / -%1,94 / -%1,83 | -%1,83 | tutmaz | -%12,9 | -1,62 | %103 | 16 | RDNW 30%; TSLA 28%; OLOX 18% |
| NT_LATE (ALT) | DOĞRULAMA | 16 | — | — | — | — | — | — / — / — | — | tutmaz | — | — | %110 | 19 | — |
| NT_LATE (ALT) | KASA | 20 | -%4,3 | -0,27 | -%14,4 | -0,72 | 1,52 | +%2,56 / -%0,82 / -%3,22 | -%3,22 | tutmaz | -%8,4 | -0,42 | %108 | 23 | LASE 66%; ASPI 42%; RILY 29% |
| OPLEV (ÜST) | KEŞİF | 120 | +%5,1 | 1,71 | +%3,7 | 1,64 | 1,09 | +%0,26 / -%0,02 / +%1,03 | +%1,18 | tutmaz | +%3,8 | 1,41 | %22 | 99 | GME 6%; LAD 2%; MED 2% |
| OPLEV (ÜST) | DOĞRULAMA | 24 | +%4,5 | 1,43 | +%4,4 | 1,46 | 1,02 | +%0,04 / +%0,86 / +%0,22 | +%0,22 | tutmaz | +%0,9 | 0,38 | %22 | 151 | SMCI 17%; MDGL 16%; BLBD 8% |
| OPLEV (ÜST) | KASA | 31 | -%2,4 | -0,51 | -%5,9 | -1,27 | 1,21 | +%0,51 / -%1,01 / -%0,17 | -%0,17 | tutmaz | -%3,9 | -0,66 | %27 | 168 | BKKT 8%; AGL 5%; HIMS 5% |
| OP_BE (ALT) | KEŞİF | 120 | +%3,0 | 0,52 | -%4,0 | -0,61 | 1,46 | +%0,38 / +%0,14 / +%0,23 | +%0,56 | tutmaz | +%2,6 | 0,78 | %38 | 106 | ERNA 4%; SRPT 3%; ACAD 3% |
| OP_BE (ALT) | DOĞRULAMA | 24 | -%17,0 | -1,82 | -%17,6 | -2,35 | 1,36 | -%1,65 / -%1,20 / -%1,39 | -%1,39 | tutmaz | -%9,3 | -1,05 | %44 | 149 | — |
| OP_BE (ALT) | KASA | 31 | +%7,4 | 0,95 | -%0,2 | -0,02 | 1,46 | +%0,52 / +%1,43 / -%0,11 | -%0,11 | tutmaz | +%5,5 | 1,03 | %46 | 164 | CAPR 6%; BKKT 4%; RGTI 4% |
| O_SCORE (ALT) | KEŞİF | 120 | +%1,4 | 0,24 | -%4,5 | -0,78 | 1,39 | +%0,34 / +%0,27 / -%0,26 | +%0,05 | tutmaz | +%0,6 | 0,20 | %37 | 100 | ERNA 4%; PBYI 3%; WKHS 3% |
| O_SCORE (ALT) | DOĞRULAMA | 24 | -%15,4 | -2,22 | -%15,9 | -2,79 | 1,26 | -%1,21 / -%1,30 / -%1,34 | -%1,34 | tutmaz | -%8,3 | -1,21 | %46 | 165 | — |
| O_SCORE (ALT) | KASA | 31 | -%8,2 | -1,38 | -%15,9 | -3,05 | 1,47 | +%0,23 / -%0,69 / -%1,69 | -%1,69 | tutmaz | -%6,9 | -1,45 | %46 | 188 | AGL 11%; ASTS 10%; WGS 10% |
| PRICE_LVL (ÜST) | KEŞİF | 120 | -%0,1 | -0,02 | -%8,0 | -2,07 | 1,52 | -%0,40 / -%0,01 / +%0,38 | +%0,64 | tutmaz | -%0,9 | -0,28 | %45 | 164 | ERNA 3%; AMRN 2%; MCRB 2% |
| PRICE_LVL (ÜST) | DOĞRULAMA | 24 | -%11,7 | -2,35 | -%12,5 | -3,27 | 1,46 | -%1,17 / -%0,68 / -%1,06 | -%1,06 | tutmaz | -%7,3 | -2,68 | %55 | 227 | — |
| PRICE_LVL (ÜST) | KASA | 31 | +%3,6 | 0,76 | -%3,0 | -0,62 | 1,40 | +%0,89 / +%0,34 / -%0,39 | -%0,39 | tutmaz | -%0,3 | -0,03 | %59 | 252 | CAPR 6%; REPL 3%; RGTI 3% |
| RD_ME (ALT) | KEŞİF | 120 | -%3,7 | -1,18 | -%2,0 | -0,61 | 0,89 | -%0,57 / +%0,15 / -%0,52 | -%0,45 | tutmaz | -%3,4 | -1,63 | %26 | 39 | PAYC 6%; RGEN 6%; NEOG 6% |
| RD_ME (ALT) | DOĞRULAMA | 24 | -%8,0 | -1,65 | -%7,8 | -1,76 | 0,92 | +%0,07 / -%0,45 / -%1,61 | -%1,61 | tutmaz | -%10,6 | -2,68 | %25 | 65 | — |
| RD_ME (ALT) | KASA | 31 | -%3,8 | -0,66 | -%5,8 | -0,84 | 1,12 | +%0,36 / +%0,86 / -%2,24 | -%2,24 | tutmaz | -%6,9 | -1,32 | %32 | 75 | LASE 12%; PLTR 10%; POWL 9% |
| RD_ME (ÜST) | KEŞİF | 120 | -%0,2 | -0,03 | -%4,9 | -0,68 | 1,31 | -%0,02 / +%0,71 / -%0,73 | -%0,39 | tutmaz | +%0,4 | 0,07 | %49 | 39 | SRPT 10%; MCRB 6%; NKTR 5% |
| RD_ME (ÜST) | DOĞRULAMA | 24 | -%12,8 | -0,73 | -%13,6 | -0,82 | 1,41 | -%0,69 / -%2,64 / +%0,13 | +%0,13 | tutmaz | -%4,5 | -0,26 | %61 | 65 | — |
| RD_ME (ÜST) | KASA | 31 | +%4,0 | 0,27 | -%6,9 | -0,54 | 1,67 | -%0,78 / +%0,70 / +%1,21 | +%1,21 | tutmaz | -%1,2 | -0,15 | %60 | 75 | CAPR 19%; REPL 9%; NVAX 7% |
| REV_SURP (ALT) | KEŞİF | 119 | +%1,5 | 0,46 | +%0,2 | 0,07 | 1,09 | -%0,38 / +%0,21 / +%0,56 | +%0,59 | tutmaz | +%2,6 | 0,86 | %52 | 88 | ERNA 4%; AMC 3%; AMTX 2% |
| REV_SURP (ALT) | DOĞRULAMA | 24 | -%0,9 | -0,27 | -%1,0 | -0,31 | 1,06 | -%0,15 / +%0,42 / -%0,49 | -%0,49 | tutmaz | -%2,6 | -0,98 | %53 | 158 | ALT 38%; TGTX 33%; UPST 26% |
| REV_SURP (ALT) | KASA | 31 | -%9,3 | -2,41 | -%10,8 | -2,92 | 1,09 | -%0,97 / -%1,29 / -%0,04 | -%0,04 | tutmaz | -%11,5 | -5,93 | %51 | 185 | JTAI 5%; MSTR 5%; ECHO 4% |
| REV_SURP (ÜST) | KEŞİF | 119 | +%4,4 | 1,62 | +%6,9 | 3,08 | 0,83 | -%0,09 / +%0,93 / +%0,25 | +%0,23 | tutmaz | +%4,9 | 2,46 | %33 | 88 | DXCM 2%; AMZN 1%; VEEV 1% |
| REV_SURP (ÜST) | DOĞRULAMA | 24 | -%2,1 | -0,46 | -%1,8 | -0,36 | 0,88 | -%0,84 / +%0,32 / +%0,00 | +%0,00 | tutmaz | -%4,4 | -1,70 | %32 | 158 | CELH 219%; OSCR 190%; ELF 179% |
| ROA_Q (ALT) | KEŞİF | 120 | +%0,4 | 0,08 | -%6,1 | -1,03 | 1,43 | +%0,28 / +%0,22 / -%0,40 | -%0,07 | tutmaz | -%0,2 | -0,08 | %49 | 136 | ERNA 3%; ACAD 2%; AMC 2% |
| ROA_Q (ALT) | DOĞRULAMA | 24 | -%19,7 | -2,21 | -%20,3 | -2,65 | 1,30 | -%1,55 / -%1,91 / -%1,46 | -%1,46 | tutmaz | -%11,9 | -1,43 | %51 | 195 | — |
| ROA_Q (ALT) | KASA | 31 | +%2,9 | 0,36 | -%5,7 | -0,80 | 1,52 | +%0,29 / +%1,10 / -%0,68 | -%0,68 | tutmaz | +%3,1 | 0,61 | %52 | 218 | CAPR 6%; AGL 4%; RGTI 4% |
| ROE_TTM (ALT) | KEŞİF | 120 | +%3,1 | 0,55 | -%3,7 | -0,67 | 1,45 | +%0,35 / +%0,03 / +%0,39 | +%0,77 | tutmaz | +%2,6 | 0,84 | %38 | 122 | GME 6%; ERNA 3%; ACAD 2% |
| ROE_TTM (ALT) | DOĞRULAMA | 24 | -%14,2 | -1,66 | -%14,8 | -2,28 | 1,35 | -%1,69 / -%0,62 / -%1,23 | -%1,23 | tutmaz | -%7,2 | -0,85 | %44 | 174 | — |
| ROE_TTM (ALT) | KASA | 31 | +%2,4 | 0,35 | -%5,3 | -0,86 | 1,47 | +%0,21 / +%1,37 / -%0,98 | -%0,98 | tutmaz | -%1,9 | -0,42 | %45 | 193 | CAPR 6%; BKKT 5%; WGS 4% |
| RUNWAY (ALT) | KEŞİF | 120 | +%1,2 | 0,22 | -%4,4 | -0,85 | 1,37 | +%0,15 / -%0,08 / +%0,24 | +%0,59 | tutmaz | +%1,4 | 0,50 | %38 | 126 | GME 7%; ERNA 4%; ALNY 2% |
| RUNWAY (ALT) | DOĞRULAMA | 24 | -%14,8 | -2,24 | -%15,2 | -2,57 | 1,22 | -%0,88 / -%1,56 / -%1,27 | -%1,27 | tutmaz | -%9,5 | -1,69 | %45 | 184 | — |
| RUNWAY (ALT) | KASA | 31 | +%2,1 | 0,24 | -%4,4 | -0,58 | 1,39 | -%0,06 / +%0,46 / +%0,13 | +%0,13 | tutmaz | +%1,2 | 0,29 | %44 | 204 | CAPR 6%; RGTI 5%; WGS 4% |
| SALES_ACCEL (ALT) | KEŞİF | 120 | -%3,2 | -1,25 | -%6,3 | -3,54 | 1,20 | -%0,25 / -%0,55 / +%0,00 | +%0,09 | tutmaz | -%3,0 | -1,48 | %66 | 122 | AMC 2%; ARWR 2%; BBY 2% |
| SALES_ACCEL (ALT) | DOĞRULAMA | 24 | -%1,5 | -0,60 | -%1,7 | -0,67 | 1,07 | -%0,10 / +%0,11 / -%0,39 | -%0,39 | tutmaz | -%2,3 | -0,69 | %64 | 182 | IDYA 43%; TGTX 42%; CYTK 41% |
| SALES_ACCEL (ALT) | KASA | 31 | -%3,1 | -0,68 | -%7,3 | -1,55 | 1,26 | -%0,21 / +%0,35 / -%0,93 | -%0,93 | tutmaz | -%5,2 | -1,14 | %67 | 202 | PRAX 5%; LASE 5%; QBTS 4% |
| SALES_ACCEL (ÜST) | KEŞİF | 120 | +%3,0 | 1,45 | +%1,2 | 0,58 | 1,12 | +%0,24 / +%0,11 / +%0,39 | +%0,63 | tutmaz | +%1,8 | 1,16 | %64 | 122 | WKHS 2%; TSLA 2%; PGEN 1% |
| SALES_ACCEL (ÜST) | DOĞRULAMA | 24 | -%5,9 | -2,29 | -%6,2 | -1,90 | 1,16 | +%0,04 / -%0,69 / -%0,84 | -%0,84 | tutmaz | -%5,7 | -4,61 | %63 | 182 | — |
| SALES_ACCEL (ÜST) | KASA | 31 | -%4,9 | -1,95 | -%7,6 | -3,28 | 1,16 | -%0,28 / -%0,20 / -%0,76 | -%0,76 | tutmaz | -%10,9 | -3,44 | %65 | 202 | CRDO 5%; RKLB 4%; IONQ 4% |
| SEAS_1 (ALT) | KEŞİF | 120 | +%1,9 | 0,56 | -%2,4 | -0,88 | 1,28 | -%0,26 / -%0,09 / +%0,83 | +%0,90 | tutmaz | +%1,6 | 0,56 | %172 | 164 | GME 4%; ERNA 3%; ACAD 1% |
| SEAS_1 (ALT) | DOĞRULAMA | 24 | -%4,9 | -0,65 | -%5,5 | -0,96 | 1,33 | -%1,52 / -%0,53 / +%0,84 | +%0,84 | tutmaz | -%3,6 | -1,12 | %167 | 227 | — |
| SEAS_1 (ALT) | KASA | 31 | -%3,5 | -1,15 | -%5,9 | -2,07 | 1,14 | +%0,09 / -%0,44 / -%0,57 | -%0,57 | tutmaz | -%3,6 | -1,09 | %170 | 252 | CAPR 8%; RGTI 5%; LASE 3% |
| SEAS_1 (ÜST) | KEŞİF | 120 | -%3,4 | -0,92 | -%5,8 | -1,58 | 1,16 | -%0,24 / -%0,27 / -%0,35 | -%0,09 | tutmaz | -%4,7 | -2,24 | %172 | 164 | WKHS 2%; MCRB 2%; DDD 1% |
| SEAS_1 (ÜST) | DOĞRULAMA | 24 | -%7,6 | -1,81 | -%7,7 | -1,74 | 1,07 | +%0,32 / -%0,79 / -%1,42 | -%1,42 | tutmaz | -%7,0 | -2,69 | %174 | 227 | — |
| SEAS_1 (ÜST) | KASA | 31 | -%1,2 | -0,25 | -%9,0 | -2,20 | 1,47 | +%0,04 / +%0,82 / -%1,18 | -%1,18 | tutmaz | -%8,7 | -1,83 | %168 | 252 | SRRK 3%; IONQ 2%; OUST 2% |
| SEAS_2_5 (ALT) | KEŞİF | 84 | -%0,4 | -0,08 | -%2,3 | -0,64 | 1,14 | -%0,19 / -%0,68 / +%0,78 | +%0,83 | tutmaz | +%0,1 | 0,04 | %169 | 151 | GME 10%; ERNA 6%; WKHS 3% |
| SEAS_2_5 (ALT) | DOĞRULAMA | 24 | +%1,7 | 0,32 | +%1,5 | 0,26 | 1,11 | +%0,91 / -%0,61 / +%0,11 | +%0,11 | tutmaz | +%0,7 | 0,31 | %175 | 182 | ALT 25%; EYPT 13%; AAOI 9% |
| SEAS_2_5 (ALT) | KASA | 31 | -%0,3 | -0,08 | -%4,8 | -2,22 | 1,27 | -%0,48 / +%0,15 / +%0,29 | +%0,29 | tutmaz | -%10,0 | -4,28 | %173 | 213 | RCAT 3%; AAOI 3%; HUT 3% |
| SEAS_2_5 (ÜST) | KEŞİF | 84 | -%2,2 | -0,72 | -%5,4 | -2,00 | 1,23 | -%0,47 / -%0,36 / +%0,29 | +%0,21 | tutmaz | -%4,6 | -2,05 | %171 | 151 | MCRB 4%; NVAX 3%; SRPT 2% |
| SEAS_2_5 (ÜST) | DOĞRULAMA | 24 | -%4,3 | -1,22 | -%4,5 | -1,36 | 1,10 | -%0,50 / +%0,32 / -%0,89 | -%0,89 | tutmaz | -%4,4 | -2,21 | %170 | 182 | — |
| SEAS_2_5 (ÜST) | KASA | 31 | -%1,9 | -0,74 | -%3,8 | -1,75 | 1,12 | -%0,18 / +%0,32 / -%0,61 | -%0,61 | tutmaz | -%4,1 | -1,44 | %171 | 213 | URGN 4%; CAPR 3%; SRRK 3% |
| SIZE_ME (ÜST) | KEŞİF | 120 | -%0,1 | -0,01 | -%6,1 | -1,56 | 1,40 | -%0,18 / +%0,05 / +%0,11 | +%0,34 | tutmaz | -%0,3 | -0,14 | %59 | 147 | ERNA 3%; WKHS 2%; MCRB 2% |
| SIZE_ME (ÜST) | DOĞRULAMA | 24 | -%8,4 | -1,87 | -%8,9 | -2,70 | 1,28 | -%1,14 / -%0,51 / -%0,44 | -%0,44 | tutmaz | -%6,3 | -1,28 | %65 | 207 | — |
| SIZE_ME (ÜST) | KASA | 31 | -%11,4 | -2,38 | -%18,2 | -3,67 | 1,42 | -%0,26 / -%0,93 / -%1,72 | -%1,72 | tutmaz | -%17,1 | -2,17 | %66 | 229 | CAPR 22%; REPL 12%; RCAT 10% |
| SKEW_TOT (ALT) | KEŞİF | 120 | -%4,3 | -2,40 | -%5,4 | -3,43 | 1,08 | -%0,23 / -%0,37 / -%0,46 | -%0,39 | tutmaz | -%4,0 | -2,49 | %181 | 164 | TBCH 1%; ALT 1%; FCEL 1% |
| SKEW_TOT (ALT) | DOĞRULAMA | 24 | -%8,3 | -4,65 | -%8,4 | -4,57 | 1,02 | -%0,43 / -%0,66 / -%0,99 | -%0,99 | tutmaz | -%8,8 | -3,31 | %181 | 227 | — |
| SKEW_TOT (ALT) | KASA | 31 | -%6,8 | -2,43 | -%7,9 | -3,72 | 1,07 | -%0,78 / -%0,57 / -%0,33 | -%0,33 | tutmaz | -%7,5 | -3,33 | %182 | 252 | NEGG 4%; IONQ 4%; OKLO 3% |
| SP (ALT) | KEŞİF | 120 | +%0,1 | 0,03 | -%1,6 | -0,31 | 1,12 | +%0,36 / -%0,07 / -%0,26 | -%0,09 | tutmaz | +%1,1 | 0,43 | %28 | 113 | ACAD 3%; WKHS 2%; IONS 2% |
| SP (ALT) | DOĞRULAMA | 24 | -%14,3 | -2,38 | -%14,4 | -2,54 | 1,08 | -%0,91 / -%1,86 / -%0,80 | -%0,80 | tutmaz | -%11,1 | -2,46 | %34 | 170 | — |
| SP (ALT) | KASA | 31 | -%2,2 | -0,39 | -%5,5 | -0,87 | 1,20 | -%0,60 / +%1,34 / -%1,24 | -%1,24 | tutmaz | -%9,1 | -1,81 | %33 | 188 | PRAX 5%; QBTS 5%; CRDO 5% |
| SP (ÜST) | KEŞİF | 120 | +%8,2 | 2,01 | +%2,3 | 0,76 | 1,39 | +%0,42 / +%0,38 / +%1,26 | +%1,38 | tutmaz | +%5,6 | 3,30 | %28 | 113 | GME 5%; PPC 1%; CNC 1% |
| SP (ÜST) | DOĞRULAMA | 24 | +%8,3 | 2,66 | +%7,9 | 2,37 | 1,23 | +%0,03 / +%0,87 / +%1,18 | +%1,18 | TUTAR | +%4,8 | 2,10 | %30 | 170 | AD 4%; OSCR 4%; CLF 4% |
| SP (ÜST) | KASA | 31 | +%1,6 | 0,32 | -%4,2 | -0,90 | 1,35 | -%0,36 / -%0,58 / +%1,40 | +%1,40 | tutmaz | -%7,2 | -1,80 | %34 | 188 | AGL 4%; ACDC 3%; TPC 2% |
| SPREAD_CS (ÜST) | KEŞİF | 120 | -%3,6 | -0,56 | -%11,6 | -1,95 | 1,53 | -%0,12 / -%0,14 / -%0,64 | -%0,32 | tutmaz | -%4,2 | -1,31 | %108 | 164 | GME 6%; ACAD 3%; AMRN 2% |
| SPREAD_CS (ÜST) | DOĞRULAMA | 24 | -%17,2 | -2,47 | -%18,1 | -3,02 | 1,46 | -%1,16 / -%1,86 / -%1,29 | -%1,29 | tutmaz | -%11,5 | -2,30 | %118 | 227 | — |
| SPREAD_CS (ÜST) | KASA | 31 | -%7,6 | -1,12 | -%18,7 | -2,55 | 1,67 | +%0,03 / +%0,02 / -%2,02 | -%2,02 | tutmaz | -%14,2 | -1,97 | %114 | 252 | ASTS 7%; PRAX 7%; BKKT 6% |
| STREV_1M (ALT) | KEŞİF | 120 | -%5,7 | -2,43 | -%5,7 | -2,07 | 1,00 | -%0,54 / -%0,16 / -%0,72 | -%0,45 | tutmaz | -%3,7 | -1,70 | %173 | 164 | TSLA 2%; NXH 2%; AMRN 2% |
| STREV_1M (ALT) | DOĞRULAMA | 24 | -%7,7 | -1,59 | -%7,8 | -1,57 | 1,05 | +%0,29 / -%1,76 / -%0,45 | -%0,45 | tutmaz | -%5,4 | -1,17 | %173 | 227 | — |
| STREV_1M (ALT) | KASA | 31 | +%7,3 | 1,38 | +%5,1 | 0,94 | 1,13 | +%0,72 / +%0,93 / +%0,16 | +%0,16 | tutmaz | +%9,0 | 1,15 | %167 | 252 | RGTI 3%; LASE 2%; IONQ 2% |
| STREV_1M (ÜST) | KEŞİF | 120 | +%0,6 | 0,15 | -%6,8 | -2,26 | 1,49 | -%0,17 / -%0,02 / +%0,35 | +%0,40 | tutmaz | -%2,4 | -0,88 | %175 | 164 | ERNA 3%; WKHS 2%; MCRB 2% |
| STREV_1M (ÜST) | DOĞRULAMA | 24 | -%5,4 | -0,62 | -%6,1 | -0,87 | 1,39 | -%1,56 / +%1,56 / -%1,34 | -%1,34 | tutmaz | -%5,0 | -0,87 | %174 | 227 | — |
| STREV_1M (ÜST) | KASA | 31 | -%10,1 | -2,06 | -%14,8 | -3,68 | 1,29 | -%0,61 / -%0,42 / -%1,52 | -%1,52 | tutmaz | -%13,9 | -2,67 | %176 | 252 | REPL 7%; SRRK 6%; ASTS 6% |
| SUE_SRW (ALT) | KEŞİF | 119 | -%2,5 | -1,13 | -%5,1 | -2,68 | 1,18 | -%0,27 / -%0,02 / -%0,33 | -%0,39 | tutmaz | -%2,1 | -1,47 | %66 | 115 | NFLX 3%; AMRN 3%; MTDR 1% |
| SUE_SRW (ALT) | DOĞRULAMA | 24 | -%2,7 | -0,65 | -%2,8 | -0,69 | 1,06 | -%0,19 / +%0,14 / -%0,64 | -%0,64 | tutmaz | -%1,7 | -0,37 | %64 | 172 | — |
| SUE_SRW (ALT) | KASA | 31 | +%2,4 | 0,46 | -%0,1 | -0,03 | 1,15 | -%0,52 / +%1,40 / -%0,22 | -%0,22 | tutmaz | +%0,3 | 0,05 | %64 | 202 | CAPR 4%; SRRK 4%; COGT 3% |
| TAX_CHG (ALT) | KEŞİF | 120 | +%1,5 | 0,58 | -%1,0 | -0,50 | 1,16 | -%0,19 / -%0,17 / +%0,73 | +%0,81 | tutmaz | +%1,6 | 0,87 | %64 | 133 | GME 6%; CVI 1%; MSTR 1% |
| TAX_CHG (ALT) | DOĞRULAMA | 24 | -%1,1 | -0,31 | -%1,2 | -0,36 | 1,06 | -%0,54 / +%0,55 / -%0,27 | -%0,27 | tutmaz | -%3,5 | -1,49 | %61 | 188 | RYTM 54%; ARRY 21%; BLBD 20% |
| TAX_CHG (ALT) | KASA | 31 | +%2,5 | 0,89 | +%0,0 | 0,01 | 1,15 | -%0,23 / +%0,27 / +%0,63 | +%0,63 | tutmaz | -%3,5 | -1,17 | %65 | 208 | MXL 3%; HUT 3%; MP 2% |
| TREND_MA (ALT) | KEŞİF | 120 | -%3,7 | -0,87 | -%10,6 | -3,44 | 1,45 | -%0,09 / -%0,40 / -%0,44 | -%0,47 | tutmaz | -%5,9 | -2,27 | %149 | 164 | AMC 2%; NVAX 2%; NCTY 2% |
| TREND_MA (ALT) | DOĞRULAMA | 24 | -%10,7 | -1,51 | -%11,1 | -1,97 | 1,24 | -%2,07 / -%0,34 / -%0,26 | -%0,26 | tutmaz | -%10,2 | -1,77 | %129 | 227 | — |
| TREND_MA (ALT) | KASA | 31 | -%8,0 | -1,19 | -%13,3 | -2,42 | 1,32 | -%0,72 / -%1,46 / +%0,18 | +%0,18 | tutmaz | -%12,8 | -2,51 | %163 | 252 | CAPR 7%; LASE 6%; MLGO 5% |
| TREND_MA (ÜST) | KEŞİF | 120 | -%2,2 | -0,54 | -%4,4 | -1,11 | 1,15 | -%0,46 / -%0,08 / -%0,01 | +%0,42 | tutmaz | -%2,4 | -0,69 | %156 | 164 | GME 5%; ERNA 3%; FCEL 1% |
| TREND_MA (ÜST) | DOĞRULAMA | 24 | -%5,5 | -1,01 | -%6,0 | -1,00 | 1,28 | +%0,23 / -%0,61 / -%0,98 | -%0,98 | tutmaz | -%2,4 | -1,17 | %151 | 227 | — |
| TREND_MA (ÜST) | KASA | 31 | +%3,6 | 0,43 | +%0,0 | 0,00 | 1,22 | +%0,67 / +%1,53 / -%1,35 | -%1,35 | tutmaz | +%4,1 | 0,34 | %157 | 252 | ASTS 3%; OKLO 3%; BKKT 3% |
| TURN_12M (ALT) | KEŞİF | 120 | +%1,2 | 0,20 | -%7,3 | -1,74 | 1,56 | -%0,02 / -%0,32 / +%0,65 | +%0,90 | tutmaz | -%3,3 | -1,15 | %27 | 147 | GME 6%; ERNA 3%; SRPT 3% |
| TURN_12M (ALT) | DOĞRULAMA | 24 | -%5,3 | -0,75 | -%6,4 | -1,53 | 1,59 | -%1,33 / -%0,51 / +%0,52 | +%0,52 | tutmaz | -%2,4 | -1,09 | %32 | 207 | — |
| TURN_12M (ALT) | KASA | 31 | -%4,3 | -0,51 | -%15,4 | -1,80 | 1,67 | -%0,08 / +%1,04 / -%2,07 | -%2,07 | tutmaz | -%12,9 | -1,32 | %40 | 229 | QURE 7%; BE 7%; RGTI 7% |
| VOL_60D (ALT) | KEŞİF | 120 | -%0,4 | -0,06 | -%10,2 | -1,75 | 1,65 | -%0,25 / -%0,04 / +%0,18 | +%0,43 | tutmaz | -%2,9 | -0,88 | %66 | 164 | GME 5%; ERNA 3%; ACAD 2% |
| VOL_60D (ALT) | DOĞRULAMA | 24 | -%15,6 | -2,05 | -%16,6 | -2,94 | 1,56 | -%1,52 / -%1,07 / -%1,32 | -%1,32 | tutmaz | -%8,7 | -2,03 | %72 | 227 | — |
| VOL_60D (ALT) | KASA | 31 | -%1,4 | -0,16 | -%13,8 | -1,38 | 1,75 | +%0,39 / +%1,02 / -%1,81 | -%1,81 | tutmaz | -%8,5 | -0,74 | %75 | 252 | CAPR 5%; ASTS 4%; RGTI 4% |
| VOL_SHOCK (ALT) | KEŞİF | 120 | -%3,3 | -1,31 | -%5,5 | -2,02 | 1,15 | +%0,02 / -%0,26 / -%0,57 | -%0,53 | tutmaz | -%2,8 | -1,94 | %166 | 164 | ERNA 3%; FCEL 1%; SRPT 1% |
| VOL_SHOCK (ALT) | DOĞRULAMA | 24 | -%14,7 | -3,09 | -%14,8 | -3,16 | 1,01 | -%1,21 / -%2,00 / -%0,47 | -%0,47 | tutmaz | -%14,5 | -4,09 | %162 | 227 | — |
| VOL_SHOCK (ALT) | KASA | 31 | -%9,0 | -2,41 | -%12,9 | -4,06 | 1,23 | -%0,98 / +%0,10 / -%1,34 | -%1,34 | tutmaz | -%13,8 | -3,76 | %164 | 252 | ASTS 6%; NVAX 4%; CAPR 4% |
| VOL_SHOCK (ÜST) | KEŞİF | 120 | -%3,1 | -2,08 | -%4,3 | -2,91 | 1,08 | -%0,27 / -%0,11 / -%0,39 | -%0,34 | tutmaz | -%3,3 | -1,88 | %185 | 164 | AMRN 2%; TBCH 1%; NXH 1% |
| VOL_SHOCK (ÜST) | DOĞRULAMA | 24 | -%1,4 | -0,55 | -%1,6 | -0,64 | 1,11 | -%0,25 / +%0,35 / -%0,46 | -%0,46 | tutmaz | -%2,4 | -1,49 | %184 | 227 | ALT 24%; EWTX 14%; IMVT 13% |
| VOL_SHOCK (ÜST) | KASA | 31 | -%2,1 | -0,40 | -%0,7 | -0,12 | 0,92 | +%0,60 / -%0,49 / -%0,70 | -%0,70 | tutmaz | +%1,8 | 0,19 | %185 | 252 | CAPR 5%; RGTI 4%; LASE 3% |

## En büyük üç katkı (KEŞİF; aykırılar kırpılmadı)
| özellik (uç) | R1: toplam getiri katkısındaki pay | R2: +%100 olayı sayısı / uçtaki toplam olay |
|---|---|---|
| ACCRUALS (ALT) | ERNA 3%; MCRB 2%; ALNY 2% | CVNA 19/793; RUN 17/793; ALNY 16/793 |
| ACCRUALS (ÜST) | DXCM 2%; NCTY 2%; AMZN 2% | DXCM 27/1402; SE 24/1402; EXTR 23/1402 |
| ACT_13D (ÜST) | CRDF 7%; ALT 7%; AUPH 6% | RILY 8/140; GME 5/140; MTZ 4/140 |
| AILE_DIS (ALT) | GME 7%; ERNA 4%; WKHS 2% | PACB 22/1309; ALNY 22/1309; ENPH 21/1309 |
| AILE_EAR (ALT) | NKTR 2%; ACAD 2%; AMC 2% | ALNY 14/1050; MU 12/1050; NBIX 12/1050 |
| AILE_INV (ALT) | PBYI 3%; WKHS 2%; TTD 2% | SEDG 30/1051; TTD 18/1051; DQ 17/1051 |
| AILE_LIQ (ÜST) | AMRN 2%; MDXG 1%; NCTY 1% | KRO 14/1458; AXGN 11/1458; PRTA 11/1458 |
| AILE_MOM (ALT) | NCTY 2%; AMRN 2%; NXH 1% | PACB 10/1312; CLF 9/1312; FSLR 9/1312 |
| AILE_MOM (ÜST) | GME 4%; WKHS 2%; MCRB 1% | ENPH 17/966; NVDA 15/966; GNRC 13/966 |
| AILE_PRF (ALT) | ERNA 5%; PBYI 3%; ALNY 3% | ALNY 21/973; NBIX 19/973; TDOC 18/973 |
| AILE_RSK (ALT) | GME 6%; INSM 2%; NXH 1% | ENPH 17/1702; TSLA 17/1702; SHOP 15/1702 |
| AILE_SEA (ALT) | GME 4%; ERNA 3%; AMRN 2% | CNR 13/1403; SEDG 12/1403; HOV 9/1403 |
| AILE_SEA (ÜST) | MCRB 2%; CZR 1%; DXCM 1% | SHOP 13/1303; NVCR 12/1303; SEDG 10/1303 |
| AILE_VAL (ALT) | TSLA 2%; DXCM 2%; ACAD 2% | DXCM 27/1493; ALNY 26/1493; NVCR 25/1493 |
| AM (ALT) | ACAD 2%; DXCM 2%; TSLA 2% | NVDA 28/1165; DXCM 27/1165; STAA 19/1165 |
| AMIHUD (ÜST) | ERNA 3%; MCRB 2%; PACB 2% | CLDX 16/1688; HOV 16/1688; EHTH 14/1688 |
| ASSET_G (ALT) | WKHS 2%; ENPH 2%; TSLA 2% | ENPH 22/1204; SEDG 22/1204; CVNA 15/1204 |
| ASSET_G (ÜST) | GME 6%; AMC 2%; MCRB 2% | GME 20/1303; LNWO 16/1303; BTU 15/1303 |
| BETA_BAB (ALT) | AMC 2%; LNWO 2%; CAR 1% | LNWO 27/1879; MU 26/1879; CAR 21/1879 |
| BE_G (ALT) | ARWR 2%; MARA 2%; ALNY 2% | TTD 16/952; FATE 16/952; IIPR 15/952 |
| BE_G (ÜST) | GME 6%; PACB 2%; CLSK 1% | RRC 19/1182; EXTR 17/1182; PACB 15/1182 |
| BM (ALT) | TSLA 2%; NFLX 2%; ENPH 2% | ENPH 23/876; TSLA 22/876; NVDA 19/876 |
| BM (ÜST) | ERNA 4%; RDN 2%; BAC 1% | GPRE 20/1026; CENX 18/1026; AR 17/1026 |
| BUYBACK_YLD (ALT) | FCEL 2%; NCTY 1%; DXPE 1% | TSLA 11/822; ENPH 8/822; CHGG 8/822 |
| CAPEX_G (ALT) | WKHS 3%; CLSK 2%; UI 2% | ETSY 18/935; SE 17/935; ARWR 17/935 |
| CAPEX_G (ÜST) | ERNA 4%; MCRB 2%; AMRN 2% | ENPH 22/810; EXTR 17/810; CLDX 17/810 |
| CBOP_A (ALT) | ERNA 4%; ALNY 3%; PBYI 3% | ALNY 23/1461; PACB 22/1461; CVNA 19/1461 |
| CFP (ALT) | GME 6%; ERNA 4%; PBYI 2% | ALNY 23/1405; PACB 22/1405; PRTA 19/1405 |
| CFP (ÜST) | LNWO 2%; AROC 1%; AER 1% | LNWO 25/1350; MU 20/1350; CNR 19/1350 |
| CHS_FAIL (ALT) | ERNA 4%; MCRB 2%; TNDM 2% | LNWO 25/1518; SM 15/1518; CYH 15/1518 |
| COMP4 (ALT) | CLSK 2%; MTDR 2%; GRPN 2% | PACB 16/1341; FSLR 13/1341; IOVA 12/1341 |
| DOLVOL (ÜST) | MCRB 2%; NXDT 1%; TBCH 1% | KRO 12/1282; CALX 11/1282; AGNT 10/1282 |
| DOSYA_Y (ALT) | GME 6%; ERNA 4%; WKHS 2% | EXTR 15/1084; NXH 14/1084; ARWR 13/1084 |
| D_ASSET_TURN (ALT) | GME 5%; ERNA 3%; NXH 2% | ENPH 15/789; EHTH 12/789; CELH 12/789 |
| D_ASSET_TURN (ÜST) | CLSK 2%; DXCM 2%; TREE 2% | TSLA 14/826; ETSY 14/826; DXCM 13/826 |
| EARN_STREAK (ALT) | ERNA 3%; FATE 1%; NTLA 1% | MU 23/964; FATE 17/964; IOVA 14/964 |
| EAR_ANN (ALT) | GME 5%; WKHS 2%; AMC 1% | LNWO 12/1116; W 10/1116; GBX 9/1116 |
| EAR_ANN (ÜST) | TNDM 1%; DXCM 1%; GRWG 1% | ENPH 17/1139; SEDG 15/1139; RH 12/1139 |
| EAR_FILE (ALT) | GME 5%; WKHS 2%; SRPT 1% | LNWO 12/1224; GME 10/1224; HOV 10/1224 |
| EAR_FILE (ÜST) | ERNA 3%; AMRN 1%; TNDM 1% | ENPH 13/1214; CNR 12/1214; TROX 11/1214 |
| EAR_VOL (ALT) | ERNA 5%; GERN 2%; ACAD 2% | ARWR 13/733; KRO 9/733; STLD 8/733 |
| EAR_VOL (ÜST) | WKHS 2%; W 1%; NXH 1% | CROX 17/806; W 14/806; LOVE 10/806 |
| EP (ALT) | GME 6%; ERNA 3%; ALNY 3% | ALNY 27/1685; TGTX 24/1685; LNWO 22/1685 |
| EV_EBITDA (ALT) | NFLX 4%; MPWR 3%; ENPH 3% | ETSY 22/463; ENPH 20/463; LGND 17/463 |
| EV_EBITDA (ÜST) | AMKR 3%; NBR 2%; ARCB 2% | ARCB 21/482; MU 18/482; LNWO 17/482 |
| E_424B5 (ALT) | GME 9%; AMC 4%; PACB 2% | TSLA 12/489; FLGT 9/489; NVAX 8/489 |
| E_DIV_OMIT (ALT) | GME 22%; RYAM 15%; GPRE 8% | VET 8/85; RRC 8/85; GPRE 7/85 |
| E_IPO_3Y (ALT) | PBYI 3%; VIPS 2%; PCRX 2% | SE 23/1205; PCRX 17/1205; NVCR 17/1205 |
| E_RSPLIT (ALT) | NVAX 389%; TNDM 326%; ERNA 283% | OVV 11/97; NVAX 10/97; NBR 7/97 |
| E_S3 (ALT) | GME 8%; AMC 3%; WKHS 3% | ENPH 9/598; TSLA 9/598; IIPR 8/598 |
| F_SCORE (ALT) | ERNA 3%; PBYI 3%; ALNY 3% | ALNY 23/1206; NFLX 18/1206; NBIX 18/1206 |
| GAP_OVN (ALT) | ERNA 3%; APA 1%; RRC 1% | LOGI 7/1092; LAB 7/1092; RRC 7/1092 |
| GAP_OVN (ÜST) | WKHS 2%; TSLA 2%; RIOT 2% | TSLA 18/1477; ENPH 13/1477; SE 10/1477 |
| GP_A (ALT) | WKHS 4%; HALO 4%; TSLA 4% | GPRE 26/614; MU 21/614; CENX 19/614 |
| GP_A (ÜST) | GME 8%; AMRN 3%; MED 2% | CROX 23/629; NXH 19/629; CALX 19/629 |
| HIGH52 (ALT) | ERNA 4%; SRPT 3%; AMC 3% | SRPT 14/1975; TECK 13/1975; OVV 13/1975 |
| IND_LEAD_BIG (ALT) | TBCH 3%; AAOI 2%; CANN 2% | PENN 8/363; RRC 8/363; MTDR 7/363 |
| IND_LEAD_BIG (ÜST) | MARA 3%; RIOT 3%; PENN 2% | VET 7/439; CDNA 7/439; MTDR 5/439 |
| IND_MOM_6 (ALT) | PENN 2%; MTDR 2%; CZR 2% | MTDR 13/650; BOOT 11/650; RRC 10/650 |
| IND_MOM_6 (ÜST) | MCRB 2%; RIOT 2%; MARA 2% | GPRE 10/784; VET 10/784; BCRX 10/784 |
| ISKEW (ALT) | GME 6%; SRPT 1%; AMD 1% | ACH 8/953; HALO 7/953; LNWO 7/953 |
| IVOL_FF3 (ALT) | GME 6%; ERNA 3%; AMC 2% | ENPH 21/2024; TSLA 16/2024; NVAX 16/2024 |
| LEV_MKT (ALT) | ACAD 3%; RIOT 3%; ALGN 3% | NVDA 25/1082; ALGN 22/1082; FRPT 19/1082 |
| LTREV_60_13 (ÜST) | GME 8%; ERNA 4%; WKHS 3% | ENPH 23/1251; RRC 19/1251; ACH 18/1251 |
| MAX5 (ALT) | GME 7%; ACAD 2%; PBYI 2% | ENPH 29/2126; NVAX 16/2126; ARWR 15/2126 |
| MOM_12_1 (ALT) | NCTY 2%; SRPT 2%; AMC 2% | TECK 15/1757; OVV 14/1757; ARCB 13/1757 |
| MOM_12_1 (ÜST) | GME 4%; WKHS 2%; ACAD 1% | ENPH 32/1449; NVDA 25/1449; SE 19/1449 |
| MOM_6_1 (ALT) | NCTY 2%; AMRN 2%; MTDR 1% | BOOT 10/1634; TECK 10/1634; TRGP 9/1634 |
| MOM_6_1 (ÜST) | GME 4%; MCRB 1%; ARWR 1% | NVDA 24/1529; ENPH 23/1529; SE 16/1529 |
| MOM_FIP (ALT) | LAB 1%; SGI 1%; CHEF 1% | TRGP 11/940; MTDR 10/940; AEO 9/940 |
| MOM_INT_12_7 (ALT) | TNDM 1%; CLSK 1%; NXH 1% | TECK 13/1672; OVV 13/1672; TROX 13/1672 |
| MOM_INT_12_7 (ÜST) | WKHS 2%; VIPS 1%; PBYI 1% | ENPH 24/1375; NVDA 17/1375; ALNY 14/1375 |
| NDF_BS (ALT) | UI 2%; ENPH 2%; TSLA 2% | ENPH 16/447; NVCR 15/447; W 13/447 |
| NDF_BS (ÜST) | PPC 2%; CDLX 2%; AMD 2% | BXC 14/491; DFIN 12/491; CDLX 11/491 |
| NEF (ALT) | WKHS 3%; ACAD 3%; MCRB 3% | ENPH 25/1019; PACB 22/1019; ARWR 20/1019 |
| NEF (ÜST) | MANH 1%; AXON 1%; SPGI 1% | NVDA 21/450; AXON 15/450; SAM 13/450 |
| NET_PAYOUT_YLD (ALT) | ACAD 3%; WKHS 3%; MCRB 3% | ENPH 23/913; ARWR 20/913; PLUG 16/913 |
| NOA (ALT) | MARA 2%; FLGT 1%; IIPR 1% | IIPR 16/615; FRPT 13/615; LNG 12/615 |
| NOA (ÜST) | WKHS 2%; MCRB 2%; LNWO 2% | LNWO 26/969; RNG 22/969; ENPH 21/969 |
| NSI_1Y (ALT) | NVAX 3%; WKHS 3%; ALNY 3% | ENPH 26/1123; TGTX 21/1123; NVAX 19/1123 |
| NSI_5Y (ALT) | ENPH 6%; WKHS 5%; NCTY 5% | ENPH 33/658; PACB 20/658; ARWR 20/658 |
| NT_LATE (ALT) | RDNW 30%; TSLA 28%; OLOX 18% | GVA 5/43; ACH 2/43; RDNW 2/43 |
| OPLEV (ÜST) | GME 6%; LAD 2%; MED 2% | GPRE 26/695; NXH 19/695; ACH 18/695 |
| OP_BE (ALT) | ERNA 4%; SRPT 3%; ACAD 3% | ALNY 27/1287; EXTR 23/1287; PACB 22/1287 |
| O_SCORE (ALT) | ERNA 4%; PBYI 3%; WKHS 3% | ENPH 27/1205; PACB 22/1205; EXTR 19/1205 |
| PRICE_LVL (ÜST) | ERNA 3%; AMRN 2%; MCRB 2% | EXTR 23/2005; PACB 21/2005; CENX 20/2005 |
| RD_ME (ALT) | PAYC 6%; RGEN 6%; NEOG 6% | CYRX 12/145; ONC 10/145; PLUG 10/145 |
| RD_ME (ÜST) | SRPT 10%; MCRB 6%; NKTR 5% | EXTR 23/497; BCRX 16/497; LNWO 15/497 |
| REV_SURP (ALT) | ERNA 4%; AMC 3%; AMTX 2% | NVAX 10/517; PRKS 9/517; CAR 9/517 |
| REV_SURP (ÜST) | DXCM 2%; AMZN 1%; VEEV 1% | TRUP 14/341; FRPT 14/341; ETSY 14/341 |
| ROA_Q (ALT) | ERNA 3%; ACAD 2%; AMC 2% | ALNY 27/1635; TGTX 24/1635; NVCR 20/1635 |
| ROE_TTM (ALT) | GME 6%; ERNA 3%; ACAD 2% | ALNY 27/1503; EXTR 23/1503; PACB 23/1503 |
| RUNWAY (ALT) | GME 7%; ERNA 4%; ALNY 2% | ALNY 23/1366; PACB 22/1366; CVNA 19/1366 |
| SALES_ACCEL (ALT) | AMC 2%; ARWR 2%; BBY 2% | EHTH 13/939; NVAX 13/939; ARWR 13/939 |
| SALES_ACCEL (ÜST) | WKHS 2%; TSLA 2%; PGEN 1% | CVNA 12/886; TSLA 12/886; DVN 11/886 |
| SEAS_1 (ALT) | GME 4%; ERNA 3%; ACAD 1% | TROX 10/1429; TSLA 10/1429; ENPH 10/1429 |
| SEAS_1 (ÜST) | WKHS 2%; MCRB 2%; DDD 1% | ENPH 14/1322; NVCR 10/1322; SHOP 10/1322 |
| SEAS_2_5 (ALT) | GME 10%; ERNA 6%; WKHS 3% | ENPH 12/857; AR 9/857; APPS 9/857 |
| SEAS_2_5 (ÜST) | MCRB 4%; NVAX 3%; SRPT 2% | SRPT 11/842; DQ 9/842; NVDA 9/842 |
| SIZE_ME (ÜST) | ERNA 3%; WKHS 2%; MCRB 2% | EHTH 18/1637; GPRE 18/1637; CLDX 14/1637 |
| SKEW_TOT (ALT) | TBCH 1%; ALT 1%; FCEL 1% | NVAX 8/1025; ENPH 7/1025; BCRX 6/1025 |
| SP (ALT) | ACAD 3%; WKHS 2%; IONS 2% | NVCR 26/931; ARWR 21/931; DXCM 19/931 |
| SP (ÜST) | GME 5%; PPC 1%; CNC 1% | GPRE 26/1218; ACH 18/1218; CAR 18/1218 |
| SPREAD_CS (ÜST) | GME 6%; ACAD 3%; AMRN 2% | ENPH 23/2115; TGTX 19/2115; ARWR 17/2115 |
| STREV_1M (ALT) | TSLA 2%; NXH 2%; AMRN 2% | ENPH 17/1430; TSLA 12/1430; ETSY 10/1430 |
| STREV_1M (ÜST) | ERNA 3%; WKHS 2%; MCRB 2% | ENPH 8/1437; SM 8/1437; W 8/1437 |
| SUE_SRW (ALT) | NFLX 3%; AMRN 3%; MTDR 1% | FATE 15/756; AXSM 10/756; NFLX 10/756 |
| TAX_CHG (ALT) | GME 6%; CVI 1%; MSTR 1% | NFLX 12/863; ETSY 12/863; KRO 11/863 |
| TREND_MA (ALT) | AMC 2%; NVAX 2%; NCTY 2% | TROX 11/1542; LNWO 11/1542; NVAX 11/1542 |
| TREND_MA (ÜST) | GME 5%; ERNA 3%; FCEL 1% | NVCR 11/1435; TSLA 9/1435; EHTH 8/1435 |
| TURN_12M (ALT) | GME 6%; ERNA 3%; SRPT 3% | SEDG 30/1718; ENPH 28/1718; MU 28/1718 |
| VOL_60D (ALT) | GME 5%; ERNA 3%; ACAD 2% | ENPH 27/2215; TGTX 20/2215; NVAX 19/2215 |
| VOL_SHOCK (ALT) | ERNA 3%; FCEL 1%; SRPT 1% | ARWR 10/1079; ALNY 9/1079; RH 9/1079 |
| VOL_SHOCK (ÜST) | AMRN 2%; TBCH 1%; NXH 1% | ENPH 10/1020; CALX 7/1020; TSLA 6/1020 |

## Kütüphanenin tamamı (KEŞİF; R1 sütunları bayrakta bayraklı grup içindir)
| sinyal | aile | yön | R1 ÜST: yıllık fazla | t(alfa) | BH | +%100 kat ÜST | ALT | -%50 kat ÜST | ALT | seçili |
|---|---|---|---|---|---|---|---|---|---|---|
| MOM_12_1 | MOM | + | +%3,6 | 0,33 |  | 1,79 [1,45; 2,51] | 2,16 [1,89; 2,59] | 2,05 [1,52; 2,51] | 2,40 [2,04; 2,93] | UST R2+R2K; ALT R2+R2K |
| MOM_6_1 | MOM | + | +%4,0 | 0,23 |  | 1,88 [1,51; 2,67] | 2,01 [1,77; 2,39] | 1,94 [1,56; 2,36] | 2,54 [2,30; 2,83] | UST R2+R2K; ALT R2+R2K |
| MOM_INT_12_7 | MOM | + | +%0,5 | -0,28 |  | 1,69 [1,41; 2,30] | 2,06 [1,86; 2,46] | 2,05 [1,55; 2,40] | 2,10 [1,79; 2,63] | UST R2+R2K; ALT R2+R2K |
| MOM_RES_12_1 | MOM | + | -%0,3 | -0,53 |  | 1,09 [0,92; 1,28] | 1,08 [0,87; 1,19] | 1,02 [0,81; 1,19] | 1,08 [0,96; 1,26] |  |
| HIGH52 | MOM | + | -%3,3 | 1,19 |  | 0,48 [0,39; 0,56] | 2,43 [2,22; 2,99] | 0,28 [0,23; 0,36] | 3,47 [3,22; 3,83] | ALT R2+R2K |
| STREV_1M | MOM | - | +%0,6 | -2,26 |  | 1,77 [1,58; 2,15] | 1,76 [1,59; 2,12] | 2,39 [2,17; 2,56] | 1,82 [1,62; 2,22] | UST R2+R2K; ALT R2+R2K |
| LTREV_60_13 | MOM | - | +%3,6 | -0,44 |  | 2,14 [1,82; 3,12] | 1,05 [0,90; 1,27] | 2,34 [2,03; 2,95] | 1,18 [0,74; 1,46] | UST R2+R2K |
| MOM_FIP | MOM | + | +%2,2 | 2,10 |  | 0,94 [0,80; 1,24] | 1,16 [1,02; 1,23] | 0,89 [0,58; 1,14] | 1,43 [1,22; 1,61] | ALT R2+R2K |
| TREND_MA | MOM | + | -%2,2 | -1,11 |  | 1,77 [1,58; 2,17] | 1,90 [1,70; 2,28] | 1,91 [1,62; 2,30] | 2,18 [1,99; 2,40] | UST R2+R2K; ALT R2+R2K |
| BM | VAL | + | +%2,2 | -0,86 |  | 1,59 [1,03; 1,95] | 1,36 [1,04; 2,06] | 1,20 [0,73; 1,97] | 1,60 [1,24; 1,87] | UST R2; ALT R2+R2K |
| EP | VAL | + | +%0,3 | -0,69 |  | 1,14 [0,63; 1,40] | 2,69 [2,21; 3,69] | 0,78 [0,48; 1,26] | 2,84 [2,36; 3,91] | ALT R2+R2K |
| SP | VAL | + | +%8,2 | 0,76 |  | 2,17 [1,54; 2,51] | 1,66 [1,25; 2,53] | 1,04 [0,63; 1,69] | 2,33 [1,55; 2,80] | UST R2; ALT R2+R2K |
| AM | VAL | + | +%2,5 | -0,16 |  | 1,28 [0,72; 1,60] | 1,65 [1,18; 2,63] | 0,67 [0,46; 1,03] | 2,03 [1,42; 2,48] | ALT R2+R2K |
| LEV_MKT | VAL | + | +%2,8 | 0,10 |  | 1,24 [0,72; 1,53] | 1,56 [1,13; 2,48] | 0,62 [0,46; 0,91] | 2,36 [1,67; 2,83] | ALT R2+R2K |
| CFP | VAL | + | +%3,8 | -0,59 |  | 2,11 [1,34; 2,64] | 2,19 [1,68; 3,31] | 1,24 [0,68; 2,16] | 2,85 [2,46; 3,35] | UST R2; ALT R2+R2K |
| EV_EBITDA | VAL | - | +%0,5 | -1,05 |  | 1,52 [1,02; 1,74] | 1,46 [1,11; 2,10] | 1,21 [0,59; 2,14] | 1,10 [0,83; 1,29] | UST R2; ALT R2 |
| NET_PAYOUT_YLD | VAL | + | +%3,6 | 0,39 |  | 1,23 [0,63; 1,55] | 1,43 [1,15; 1,92] | 0,57 [0,34; 1,01] | 2,36 [2,04; 2,58] | ALT R2+R2K |
| ROE_TTM | PRF | + | +%1,1 | 2,04 |  | 0,70 [0,50; 0,80] | 2,48 [1,92; 3,67] | 0,57 [0,47; 0,65] | 3,06 [2,64; 3,74] | ALT R2+R2K |
| ROA_Q | PRF | + | +%0,6 | 1,61 |  | 0,81 [0,69; 1,04] | 2,44 [1,83; 3,76] | 0,82 [0,70; 0,92] | 3,42 [2,86; 4,05] | ALT R2+R2K |
| D_ASSET_TURN | PRF | + | -%0,9 | -1,64 |  | 1,55 [1,36; 2,01] | 1,48 [1,14; 1,63] | 1,33 [1,22; 1,50] | 1,35 [0,99; 1,60] | UST R2+R2K; ALT R2+R2K |
| SALES_ACCEL | PRF | + | +%3,0 | 0,58 |  | 1,47 [1,27; 1,75] | 1,56 [1,35; 1,70] | 1,62 [1,46; 1,79] | 1,48 [1,38; 1,65] | UST R2+R2K; ALT R2+R2K |
| ACCRUALS | PRF | - | +%1,6 | -0,70 |  | 2,24 [1,83; 3,03] | 1,27 [1,05; 1,49] | 2,57 [2,08; 2,98] | 1,34 [0,83; 1,66] | UST R2+R2K; ALT R2 |
| GP_A | PRF | + | +%5,2 | 1,51 |  | 1,49 [1,01; 2,05] | 1,46 [1,18; 1,93] | 1,21 [0,91; 1,41] | 2,16 [1,96; 2,53] | UST R2+R2K; ALT R2+R2K |
| OP_BE | PRF | + | +%1,5 | 1,76 |  | 0,74 [0,51; 0,84] | 2,45 [1,80; 3,86] | 0,50 [0,38; 0,66] | 3,28 [2,81; 4,13] | ALT R2+R2K |
| CBOP_A | PRF | + | +%1,4 | 2,39 |  | 0,92 [0,80; 1,17] | 2,15 [1,58; 3,39] | 0,78 [0,67; 0,89] | 3,37 [2,61; 3,88] | ALT R2+R2K |
| F_SCORE | PRF | + | +%0,2 | 0,63 |  | 0,68 [0,45; 0,79] | 2,04 [1,61; 2,96] | 0,62 [0,47; 0,87] | 2,60 [2,12; 3,10] | ALT R2+R2K |
| NOA | PRF | - | +%0,8 | -0,37 |  | 1,49 [1,27; 1,98] | 0,94 [0,83; 1,04] | 1,81 [1,39; 2,13] | 1,62 [1,42; 1,78] | UST R2+R2K; ALT R2K |
| OPLEV | PRF | + | +%5,1 | 1,64 |  | 1,42 [1,18; 1,63] | 0,46 [0,26; 0,64] | 1,06 [0,98; 1,15] | 0,78 [0,59; 0,94] | UST R2 |
| RD_ME | PRF | + | -%0,2 | -0,68 |  | 2,59 [1,77; 4,36] | 0,75 [0,44; 0,98] | 3,43 [2,79; 4,20] | 1,64 [1,21; 1,98] | UST R2+R2K; ALT R2K |
| TAX_CHG | PRF | + | +%0,3 | 0,49 |  | 1,07 [0,95; 1,29] | 1,31 [1,07; 1,46] | 0,89 [0,72; 1,20] | 1,01 [0,85; 1,19] | ALT R2 |
| ASSET_G | INV | - | +%2,2 | -0,51 |  | 1,79 [1,48; 2,39] | 1,65 [1,32; 2,23] | 1,43 [1,26; 1,82] | 2,58 [1,96; 2,97] | UST R2+R2K; ALT R2+R2K |
| NSI_1Y | INV | - | +%3,0 | 0,99 |  | 0,91 [0,39; 1,18] | 1,62 [1,40; 2,11] | 0,43 [0,31; 0,63] | 2,64 [2,27; 2,99] | ALT R2+R2K |
| BE_G | INV | - | +%4,6 | 0,19 |  | 1,82 [1,59; 2,31] | 1,46 [1,19; 1,93] | 1,49 [1,34; 1,82] | 2,31 [1,73; 2,67] | UST R2+R2K; ALT R2+R2K |
| NSI_5Y | INV | - | +%3,7 | 0,94 |  | 1,06 [0,40; 1,39] | 1,46 [1,25; 1,83] | 0,48 [0,31; 0,79] | 2,19 [1,87; 2,52] | ALT R2+R2K |
| NEF | INV | - | +%2,2 | 4,51 | evet | 0,67 [0,47; 0,76] | 1,52 [1,20; 2,07] | 0,35 [0,27; 0,41] | 2,63 [2,01; 3,02] | UST R1; ALT R2+R2K |
| NDF_BS | INV | - | +%0,7 | -0,26 |  | 1,27 [0,98; 1,52] | 1,15 [1,03; 1,32] | 0,91 [0,76; 1,21] | 1,03 [0,89; 1,24] | UST R2; ALT R2 |
| BUYBACK_YLD | INV | + | +%4,8 | 1,02 |  | 1,13 [0,53; 1,45] | 1,28 [1,15; 1,55] | 0,42 [0,27; 0,67] | 1,48 [1,32; 1,58] | ALT R2+R2K |
| CAPEX_G | INV | - | +%0,7 | -0,45 |  | 1,52 [1,35; 1,90] | 1,75 [1,41; 2,25] | 1,59 [1,28; 1,81] | 2,21 [1,99; 2,54] | UST R2+R2K; ALT R2+R2K |
| EAR_ANN | EAR | + | +%0,5 | -1,11 |  | 1,70 [1,56; 1,99] | 1,67 [1,51; 1,92] | 1,44 [1,25; 1,65] | 1,87 [1,66; 2,05] | UST R2+R2K; ALT R2+R2K |
| EAR_FILE | EAR | + | +%1,8 | -0,55 |  | 1,71 [1,55; 2,03] | 1,73 [1,56; 2,03] | 1,53 [1,40; 1,73] | 1,94 [1,78; 2,08] | UST R2+R2K; ALT R2+R2K |
| SUE_SRW | EAR | + | -%1,1 | 0,18 |  | 0,78 [0,50; 0,89] | 1,34 [1,07; 1,46] | 0,68 [0,60; 0,75] | 1,69 [1,30; 2,02] | ALT R2+R2K |
| REV_SURP | EAR | + | +%4,4 | 3,08 | evet | 0,79 [0,52; 1,12] | 1,19 [0,89; 1,38] | 0,85 [0,35; 1,18] | 1,00 [0,75; 1,24] | UST R1; ALT R2 |
| EARN_STREAK | EAR | + | +%1,1 | 2,20 |  | 0,74 [0,59; 0,83] | 1,45 [1,34; 1,67] | 0,61 [0,51; 0,66] | 1,73 [1,41; 2,01] | ALT R2+R2K |
| EAR_VOL | EAR | + | +%1,6 | 0,36 |  | 1,20 [0,94; 1,32] | 1,09 [1,00; 1,34] | 1,15 [1,01; 1,25] | 1,74 [1,42; 1,94] | UST R2+R2K; ALT R2K |
| VOL_60D | RSK | - | -%1,3 | 2,23 |  | 0,09 [0,02; 0,12] | 2,73 [2,33; 3,60] | 0,11 [0,04; 0,28] | 3,62 [3,23; 4,33] | ALT R2+R2K |
| IVOL_FF3 | RSK | - | -%1,7 | 1,31 |  | 0,18 [0,06; 0,23] | 2,49 [2,10; 3,34] | 0,11 [0,04; 0,24] | 3,40 [3,06; 3,97] | ALT R2+R2K |
| BETA_BAB | RSK | - | -%3,0 | 0,77 |  | 0,60 [0,52; 0,79] | 2,41 [2,18; 2,99] | 1,17 [0,77; 1,53] | 1,89 [1,46; 2,60] | ALT R2+R2K |
| MAX5 | RSK | - | -%1,5 | 1,74 |  | 0,19 [0,13; 0,22] | 2,62 [2,27; 3,41] | 0,22 [0,12; 0,41] | 3,23 [2,93; 3,81] | ALT R2+R2K |
| SKEW_TOT | RSK | - | -%2,8 | -2,03 |  | 0,93 [0,86; 1,07] | 1,26 [1,15; 1,37] | 0,95 [0,90; 1,02] | 1,44 [1,28; 1,57] | ALT R2+R2K |
| ISKEW | RSK | - | -%3,6 | -2,72 | evet | 0,94 [0,84; 1,01] | 1,17 [1,11; 1,30] | 0,93 [0,88; 0,98] | 1,37 [1,19; 1,52] | ALT R2+R2K |
| PRICE_LVL | RSK | - | -%0,1 | -2,07 |  | 2,47 [2,15; 3,30] | 0,41 [0,29; 0,54] | 3,11 [2,89; 3,63] | 0,43 [0,22; 0,55] | UST R2+R2K |
| SIZE_ME | LIQ | - | -%0,1 | -1,56 |  | 2,25 [1,98; 2,83] | 0,26 [0,16; 0,30] | 2,94 [2,65; 3,52] | 0,26 [0,13; 0,34] | UST R2+R2K |
| AMIHUD | LIQ | + | -%1,3 | -1,71 |  | 2,08 [1,72; 2,83] | 0,32 [0,21; 0,37] | 2,76 [2,42; 3,31] | 0,36 [0,22; 0,45] | UST R2+R2K |
| TURN_12M | LIQ | - | -%1,4 | 1,33 |  | 0,74 [0,65; 0,91] | 2,36 [2,22; 2,71] | 0,59 [0,50; 0,64] | 2,74 [2,37; 3,04] | ALT R2+R2K |
| DOLVOL | LIQ | - | -%2,7 | -2,07 |  | 1,58 [1,44; 1,90] | 0,55 [0,43; 0,66] | 1,78 [1,64; 2,09] | 0,71 [0,40; 0,90] | UST R2+R2K |
| VOL_SHOCK | LIQ | + | -%3,1 | -2,91 | evet | 1,26 [1,17; 1,40] | 1,33 [1,24; 1,52] | 1,30 [1,21; 1,42] | 1,90 [1,52; 2,15] | UST R2+R2K; ALT R2+R2K |
| SPREAD_CS | LIQ | + | -%3,6 | -1,95 |  | 2,61 [2,14; 3,58] | 0,28 [0,12; 0,37] | 3,60 [3,24; 4,29] | 0,17 [0,10; 0,31] | UST R2+R2K |
| GAP_OVN | LIQ | ? | -%3,8 | -1,93 |  | 1,82 [1,67; 2,15] | 1,35 [1,21; 1,68] | 2,13 [1,90; 2,47] | 1,80 [1,51; 1,99] | UST R2+R2K; ALT R2+R2K |
| SEAS_1 | SEA | + | -%3,4 | -1,58 |  | 1,63 [1,48; 1,95] | 1,76 [1,58; 2,15] | 1,99 [1,74; 2,15] | 1,86 [1,72; 2,21] | UST R2+R2K; ALT R2+R2K |
| SEAS_2_5 | SEA | + | -%2,2 | -2,00 |  | 1,44 [1,33; 1,72] | 1,46 [1,38; 1,57] | 1,38 [1,28; 1,55] | 1,79 [1,70; 1,95] | UST R2+R2K; ALT R2+R2K |
| EA_MONTH | SEA | + | +%0,4 | 0,85 |  | 0,99 [0,89; 1,04] | — | 0,90 [0,81; 0,99] | — |  |
| DIV_MONTH | SEA | + | -%2,3 | -0,23 |  | 0,52 [0,31; 0,64] | — | 0,31 [0,14; 0,56] | — |  |
| RUNWAY | DIS | - | -%0,2 | 0,90 |  | 0,74 [0,37; 1,06] | 2,19 [1,63; 3,44] | 0,58 [0,32; 0,97] | 2,95 [2,45; 3,45] | ALT R2+R2K |
| NT_LATE | DIS | - | -%11,2 | -1,71 |  | — | 1,16 [0,72; 1,41] | — | 2,74 [2,33; 3,19] | ALT R2K |
| CHS_FAIL | DIS | - | -%0,5 | 2,85 | evet | 0,52 [0,40; 0,83] | 2,70 [2,45; 3,39] | 0,22 [0,19; 0,25] | 2,77 [2,55; 3,26] | ALT R2+R2K |
| O_SCORE | DIS | - | -%1,4 | 0,42 |  | 0,94 [0,72; 1,43] | 2,43 [1,71; 3,88] | 0,86 [0,64; 0,99] | 3,52 [2,75; 4,15] | ALT R2+R2K |
| IND_MOM_6 | SEC | + | +%0,8 | 0,10 |  | 1,42 [1,13; 2,10] | 1,18 [0,73; 1,43] | 1,34 [1,04; 1,91] | 1,43 [0,90; 2,14] | UST R2+R2K; ALT R2K |
| IND_LEAD_BIG | SEC | + | -%3,7 | -2,16 |  | 1,46 [1,09; 1,73] | 1,21 [0,95; 1,37] | 1,10 [0,96; 1,32] | 1,46 [1,28; 1,69] | UST R2; ALT R2+R2K |
| ACT_13D | OWN | + | -%7,6 | -3,04 | evet | 1,26 [1,03; 1,44] | — | 2,24 [2,03; 2,56] | — | UST R2+R2K |
| E_S3 | EVT | - | -%1,9 | -1,28 |  | — | 1,17 [0,99; 1,35] | — | 1,56 [1,30; 1,74] | ALT R2+R2K |
| E_424B5 | EVT | - | -%1,7 | -0,88 |  | — | 1,02 [0,78; 1,10] | — | 1,39 [1,01; 1,77] | ALT R2K |
| E_TENDER_SELF | EVT | + | — | — |  | 2,15 [2,15; 2,15] | — | 0,86 [0,86; 0,86] | — |  |
| E_IPO_3Y | EVT | - | +%1,0 | -0,79 |  | — | 1,93 [1,45; 2,87] | — | 2,79 [2,25; 3,11] | ALT R2+R2K |
| E_SPLIT | EVT | + | +%3,0 | 1,74 |  | 0,35 [0,22; 0,49] | — | 0,39 [0,22; 0,59] | — |  |
| E_RSPLIT | EVT | - | -%19,7 | -2,69 | evet | — | 1,57 [1,23; 2,33] | — | 4,30 [3,49; 6,64] | ALT R2+R2K |
| E_DIV_INIT | EVT | + | +%1,3 | 0,53 |  | 0,87 [0,66; 1,28] | — | 0,49 [0,29; 0,83] | — |  |
| E_DIV_OMIT | EVT | - | — | — |  | — | 1,70 [1,43; 3,43] | — | 0,78 [0,51; 2,29] | ALT R2 |
| AILE_MOM | AİLE | + | +%2,9 | 1,47 |  | 1,19 [1,04; 1,54] | 1,62 [1,41; 1,71] | 1,17 [0,86; 1,49] | 1,85 [1,65; 2,08] | UST R2; ALT R2+R2K |
| AILE_VAL | AİLE | + | +%3,7 | 0,12 |  | 1,32 [0,70; 1,62] | 2,14 [1,51; 3,41] | 0,63 [0,29; 1,16] | 2,82 [2,10; 3,37] | ALT R2+R2K |
| AILE_PRF | AİLE | + | +%1,3 | 1,82 |  | 0,76 [0,61; 0,86] | 1,53 [1,37; 1,87] | 0,58 [0,47; 0,74] | 2,43 [2,13; 2,64] | ALT R2+R2K |
| AILE_INV | AİLE | + | +%3,2 | 1,99 |  | 0,83 [0,41; 1,06] | 1,47 [1,15; 2,02] | 0,37 [0,26; 0,58] | 2,52 [1,90; 2,90] | ALT R2+R2K |
| AILE_EAR | AİLE | + | +%1,5 | 1,41 |  | 1,05 [0,89; 1,15] | 1,46 [1,34; 1,75] | 0,81 [0,76; 0,91] | 1,80 [1,56; 1,97] | ALT R2+R2K |
| AILE_RSK | AİLE | + | -%1,7 | 1,52 |  | 0,21 [0,11; 0,27] | 2,10 [1,95; 2,42] | 0,18 [0,08; 0,37] | 2,23 [1,98; 2,41] | ALT R2+R2K |
| AILE_LIQ | AİLE | + | -%1,6 | -1,77 |  | 1,80 [1,58; 2,29] | 0,41 [0,28; 0,47] | 1,93 [1,80; 2,20] | 0,45 [0,32; 0,51] | UST R2+R2K |
| AILE_SEA | AİLE | + | -%4,0 | -2,20 |  | 1,61 [1,40; 2,00] | 1,73 [1,57; 2,04] | 1,93 [1,64; 2,09] | 1,97 [1,89; 2,17] | UST R2+R2K; ALT R2+R2K |
| AILE_DIS | AİLE | + | -%1,9 | 2,22 |  | 0,33 [0,25; 0,44] | 2,32 [1,83; 3,34] | 0,27 [0,18; 0,38] | 3,20 [2,63; 3,67] | ALT R2+R2K |
| AILE_SEC | AİLE | + | -%0,8 | 0,22 |  | 1,16 [0,95; 1,60] | 1,02 [0,61; 1,24] | 0,94 [0,81; 1,11] | 1,23 [0,83; 1,74] |  |
| COMP4 | K59 | + | +%1,9 | 2,63 | evet | 0,70 [0,55; 0,80] | 1,89 [1,68; 2,43] | 0,43 [0,38; 0,48] | 2,49 [2,36; 2,71] | ALT R2+R2K |
| DOSYA_Y | K59 | + | +%1,8 | 1,61 |  | 0,95 [0,76; 1,06] | 1,89 [1,69; 2,24] | 0,62 [0,53; 0,77] | 1,98 [1,80; 2,21] | ALT R2+R2K |

## Plasebo dağılımı (KEŞİF, 200 rastgele sinyal)
| istatistik | medyan | %95 | en büyük | seçim eşiği |
|---|---|---|---|---|
| net t(alfa) (bilgi) | -2,54 | -0,92 | 0,87 | — |
| brüt t(alfa) | -0,01 | 1,49 | 3,32 | 3,32 |
| -brüt t(alfa) | 0,01 | 1,94 | 2,69 | 2,69 |
| +%100 lift | 1,00 | 1,05 | 1,08 | 1,08 |
| -%50 lift | 1,00 | 1,04 | 1,07 | 1,07 |

## Birleşik olasılık modeli (bilgi)
Katsayılar (KEŞİF'te donduruldu): sabit -1,61, AILE_MOM 0,02, AILE_VAL 0,46, AILE_PRF 0,27, AILE_INV -0,38, AILE_EAR -0,38, AILE_RSK -3,43, AILE_LIQ 1,34, AILE_SEA -0,05, AILE_DIS -1,72, AILE_SEC 0,20.

| dönem | dilim | gözlem | tahmin | gerçekleşen |
|---|---|---|---|---|
| KEŞİF | 1 | 19709 | %0,89 | %0,52 |
| KEŞİF | 2 | 19709 | %1,34 | %1,13 |
| KEŞİF | 3 | 19709 | %1,75 | %1,52 |
| KEŞİF | 4 | 19709 | %2,20 | %1,83 |
| KEŞİF | 5 | 19709 | %2,74 | %2,67 |
| KEŞİF | 6 | 19708 | %3,39 | %3,60 |
| KEŞİF | 7 | 19708 | %4,22 | %4,73 |
| KEŞİF | 8 | 19708 | %5,38 | %6,47 |
| KEŞİF | 9 | 19708 | %7,23 | %8,10 |
| KEŞİF | 10 | 19708 | %12,07 | %10,63 |
| DOĞRULAMA | 1 | 5457 | %0,85 | %0,46 |
| DOĞRULAMA | 2 | 5457 | %1,30 | %1,06 |
| DOĞRULAMA | 3 | 5457 | %1,70 | %1,28 |
| DOĞRULAMA | 4 | 5457 | %2,14 | %1,92 |
| DOĞRULAMA | 5 | 5457 | %2,68 | %2,38 |
| DOĞRULAMA | 6 | 5457 | %3,34 | %3,43 |
| DOĞRULAMA | 7 | 5457 | %4,26 | %4,16 |
| DOĞRULAMA | 8 | 5457 | %5,56 | %5,30 |
| DOĞRULAMA | 9 | 5457 | %7,64 | %7,00 |
| DOĞRULAMA | 10 | 5456 | %12,76 | %9,93 |
| KASA | 1 | 4864 | %0,82 | %0,62 |
| KASA | 2 | 4864 | %1,26 | %1,67 |
| KASA | 3 | 4864 | %1,66 | %2,67 |
| KASA | 4 | 4864 | %2,10 | %2,94 |
| KASA | 5 | 4864 | %2,63 | %5,08 |
| KASA | 6 | 4863 | %3,31 | %6,56 |
| KASA | 7 | 4863 | %4,25 | %9,01 |
| KASA | 8 | 4863 | %5,63 | %11,17 |
| KASA | 9 | 4863 | %7,91 | %13,70 |
| KASA | 10 | 4863 | %13,43 | %14,85 |

## Yanlılık ve sınırlar
Yalnız yaşayanlar (kaybeden olasılıkları ALT SINIR; küçüklük, düşük fiyat, sıkıntı ve likidite aileleri en açık); frames en son bildirilen değeri verir; XBRL kapsamı 2011'e kadar kademeli; Yahoo kırpık hisseler dışarıda; aykırı getiriler tutuldu; dönemler oluşum ayına göre (12 aylık pencereler komşu döneme taşar). R1 için tam kör OLMAYAN satırlar (K58 / K59'da görüldü): MOM_12_1, ROE_TTM, NSI_1Y, SALES_ACCEL, VOL_60D, HIGH52, STREV_1M, SIZE_ME, COMP4, DOSYA_Y. Ayrıntı: K60_ON_KAYIT.md §9 ve §11.
