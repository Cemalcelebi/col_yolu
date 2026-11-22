# TEZGÂH DOĞRULAMA — RAPOR (2026-11-22 10:18:08 UTC)

TEZGAH_DOGRULAMA v1.0 (2026-11-22). Ön kayıt TEZGAH_DOGRULAMA_ON_KAYIT.md (git e45524e1e91daf2e58fd8d3e09673f739f600eef 2026-11-22T10:16:56+00:00); koşu 2026-11-22 10:17:00 UTC .. 2026-11-22 10:18:08 UTC (68 sn). Hisse verisi yalnız KASA açık kısmı (kesik 2023-12-31); referans French veri kütüphanesi (yedek kullanılmadı), 2023-12'de kesik.

## 1. TEK SAYFA ÖZET

**Sonuç: tezgâh yayımlanmış ABD serilerini kısmen izliyor (DOĞRU olmayan: A3 KISMEN); US_MOM 2016-23 yayımlanmış seride de sıfırdan ayrışmıyor (t -0.31; bizim t +0.20): dönemin gerçeği; US_STREV 2016-23 yayımlanmış seride de sıfırdan ayrışmıyor (t +0.87; bizim t +0.45): dönemin gerçeği.**

- Piyasa: ABD eşit ağırlıklı DOĞRU (korelasyon +0,96, işaret uyumu %94), işlem değeri ağırlıklı DOĞRU (korelasyon +0,95, işaret uyumu %93); Avrupa DOĞRU (korelasyon +0,99, işaret uyumu %97).
- Momentum (12-1): French Mom ile DOĞRU (korelasyon +0,89, işaret uyumu %84); onluk farkı ağırlıklı DOĞRU (korelasyon +0,81, işaret uyumu %85), eşit ağırlıklı KISMEN (korelasyon +0,69, işaret uyumu %68); Avrupa WML ile DOĞRU (korelasyon +0,96, işaret uyumu %86).
- Kısa vadeli dönüş: French ST_Rev ile DOĞRU (korelasyon +0,87, işaret uyumu %76); onluk farkı ağırlıklı DOĞRU (korelasyon +0,73, işaret uyumu %77), eşit ağırlıklı DOĞRU (korelasyon +0,74, işaret uyumu %71).
- Yayımlanmış ABD momentumu (French Mom): 2000-15 ayda +0,27% (t +0,65), 2016-23 ayda -0,13% (t -0,31). ST_Rev: 2000-15 ayda +0,26% (t +0,87), 2016-23 ayda +0,29% (t +0,87). Avrupa WML: 2000-15 ayda +0,83% (t +2,48), 2016-23 ayda +0,47% (t +1,39).
- Veri kipi (E2): 20 / 20 büyük hissede bizim aylık getiri = Yahoo ayarlı kapanış (en düşük korelasyon +1,0000; medyan fark -0,00 bp): fiyatlar temettü dahil ayarlı.
- Evren bugün yaşayan hisseler: batan hisseler yok, bu yüzden alt onluklar (kaybedenler) olduğundan iyi görünür; korelasyon (ay ay zamanlama) bundan az, ortalama (seviye) çok etkilenir.

Seri başına hüküm (karşılaştırma penceresi: tutma ayı 2016-01..2023-12; kural: korelasyon >= 0,70 ve işaret uyumu >= %70 DOĞRU, piyasa serisinde korelasyon >= 0,90; 0,40-0,70 KISMEN; < 0,40 UYUŞMUYOR):

| kod | seri | ay | Pearson | Spearman | işaret uyumu | eğim | hüküm |
|---|---|---|---|---|---|---|---|
| A1 | ABD evren getirisi EW vs French EW piyasa (Prior_12_2 EW onlukları, firma ağırlıklı) | 96 | +0,96 | +0,94 | %94 | +0,89 | **DOĞRU** |
| A2 | ABD evren getirisi LQ vs French piyasa (Mkt-RF + RF, VW) | 96 | +0,95 | +0,92 | %93 | +1,25 | **DOĞRU** |
| A3 | ABD MOM onluk üst - alt EW vs French Prior_12_2 EW Hi - Lo | 91 | +0,69 | +0,58 | %68 | +0,72 | **KISMEN** |
| A4 | ABD MOM onluk üst - alt LQ vs French Prior_12_2 VW Hi - Lo | 91 | +0,81 | +0,85 | %85 | +0,92 | **DOĞRU** |
| A5 | ABD MOM 2x3 (üst 30 - alt 30) LQ vs French Mom | 91 | +0,89 | +0,87 | %84 | +1,07 | **DOĞRU** |
| A6 | ABD STREV onluk alt - üst EW vs French Prior_1_0 EW Lo - Hi | 96 | +0,74 | +0,68 | %71 | +0,66 | **DOĞRU** |
| A7 | ABD STREV onluk alt - üst LQ vs French Prior_1_0 VW Lo - Hi | 96 | +0,73 | +0,75 | %77 | +0,95 | **DOĞRU** |
| A8 | ABD STREV 2x3 (alt 30 - üst 30) LQ vs French ST_Rev | 96 | +0,87 | +0,85 | %76 | +0,97 | **DOĞRU** |
| E1 | AVR evren getirisi LQ (USD) vs French Avrupa piyasa (USD) | 96 | +0,99 | +0,98 | %97 | +1,05 | **DOĞRU** |
| E2 | AVR evren getirisi EW (USD) vs French Avrupa piyasa (USD) | 96 | +0,98 | +0,98 | %96 | +1,13 | **DOĞRU** |
| E3 | AVR MOM 2x3 LQ (USD) vs French Avrupa WML | 96 | +0,96 | +0,92 | %86 | +1,23 | **DOĞRU** |
| E4 | AVR MOM onluk üst - alt EW (USD) vs French Avrupa WML | 96 | +0,91 | +0,86 | %82 | +1,79 | **DOĞRU** |

Referansın KENDİ dönem ortalamaları (aylık, %; t = ort / (sd / kök n)): 'bu dönemde yayımlanmış veride de zayıf mıydı?'

| referans | 2000-15 ort (t) | 2016-23 ort (t) | 2016-19 ort (t) | 2020-23 ort (t) |
|---|---|---|---|---|
| US_MOM | +0,27 (+0,65, n 192) | -0,13 (-0,31, n 96) | -0,19 (-0,38, n 48) | -0,06 (-0,10, n 48) |
| US_P12_VW_FARK | +0,58 (+0,85, n 192) | -0,19 (-0,22, n 96) | +0,03 (+0,04, n 48) | -0,42 (-0,27, n 48) |
| US_P12_EW_FARK | +0,30 (+0,49, n 192) | +0,52 (+0,76, n 96) | +0,59 (+0,78, n 48) | +0,44 (+0,39, n 48) |
| US_STREV | +0,26 (+0,87, n 192) | +0,29 (+0,87, n 96) | +0,61 (+1,99, n 48) | -0,04 (-0,07, n 48) |
| US_P1_VW_FARK | +0,18 (+0,36, n 192) | +0,17 (+0,22, n 96) | +0,68 (+1,03, n 48) | -0,34 (-0,25, n 48) |
| US_P1_EW_FARK | +0,93 (+1,89, n 192) | +0,61 (+0,89, n 96) | +0,02 (+0,04, n 48) | +1,19 (+0,97, n 48) |
| US_MKT | +0,46 (+1,43, n 192) | +1,15 (+2,34, n 96) | +1,20 (+2,36, n 48) | +1,10 (+1,29, n 48) |
| US_EWMKT | +0,98 (+2,22, n 192) | +0,93 (+1,36, n 96) | +0,89 (+1,25, n 48) | +0,97 (+0,83, n 48) |
| EU_WML | +0,83 (+2,48, n 192) | +0,47 (+1,39, n 96) | +0,53 (+1,47, n 48) | +0,42 (+0,71, n 48) |
| EU_MKT | +0,48 (+1,21, n 192) | +0,70 (+1,35, n 96) | +0,73 (+1,40, n 48) | +0,66 (+0,74, n 48) |

Bizim ana serilerin aynı dönem ortalamaları:

| kod | 2016-23 ort (t) | 2016-19 | 2020-23 |
|---|---|---|---|
| A1 | +1,25 (+1,98, n 96) | +1,31 (+2,19, n 48) | +1,19 (+1,06, n 48) |
| A2 | +1,54 (+2,38, n 96) | +1,42 (+2,43, n 48) | +1,66 (+1,43, n 48) |
| A3 | +0,67 (+0,92, n 91) | +0,20 (+0,22, n 43) | +1,09 (+0,96, n 48) |
| A4 | +1,03 (+1,02, n 91) | +0,50 (+0,45, n 43) | +1,51 (+0,91, n 48) |
| A5 | +0,10 (+0,20, n 91) | -0,02 (-0,03, n 43) | +0,21 (+0,27, n 48) |
| A6 | +0,52 (+0,86, n 96) | +0,86 (+1,53, n 48) | +0,18 (+0,16, n 48) |
| A7 | +0,07 (+0,07, n 96) | +1,40 (+1,44, n 48) | -1,27 (-0,74, n 48) |
| A8 | +0,17 (+0,45, n 96) | +0,79 (+2,31, n 48) | -0,46 (-0,71, n 48) |
| E1 | +0,68 (+1,25, n 96) | +0,68 (+1,21, n 48) | +0,69 (+0,73, n 48) |
| E2 | +0,72 (+1,22, n 96) | +0,85 (+1,44, n 48) | +0,59 (+0,57, n 48) |
| E3 | +0,07 (+0,16, n 96) | +0,34 (+0,71, n 48) | -0,20 (-0,27, n 48) |
| E4 | -0,28 (-0,42, n 96) | -0,24 (-0,35, n 48) | -0,33 (-0,28, n 48) |

Okuma: evren bugün işlem gören hisselerdir (batan yok); bu, seviye getirilerini yukarı, alt onlukları (MOM alt, STREV alt) yukarı çeker: MOM farkı aşağı, STREV farkı yukarı yanlı okunur. Korelasyon (zamanlama) bu yanlılıktan az etkilenir; ortalama (seviye) çok etkilenir.

## 2. BÜTÜN ÇİFTLER (ana + teşhis)

| kod | tür | bizim | referans | ay | Pearson | Spearman | işaret | eğim | biz ort (t) | ref ort (t) | d1 r | d2 r | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | ANA | `ABD · havuz · r · PIYASA · - · EW` | `US_EWMKT` | 96 | +0,96 | +0,94 | %94 | +0,89 | +1,25 (+1,98) | +0,93 (+1,36) | +0,96 | +0,96 | DOĞRU |
| A2 | ANA | `ABD · havuz · r · PIYASA · - · LQ` | `US_MKT` | 96 | +0,95 | +0,92 | %93 | +1,25 | +1,54 (+2,38) | +1,15 (+2,34) | +0,98 | +0,95 | DOĞRU |
| A3 | ANA | `ABD · havuz · r · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | 91 | +0,69 | +0,58 | %68 | +0,72 | +0,67 (+0,92) | +0,68 (+0,98) | +0,60 | +0,74 | KISMEN |
| A4 | ANA | `ABD · havuz · r · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | 91 | +0,81 | +0,85 | %85 | +0,92 | +1,03 (+1,02) | +0,01 (+0,01) | +0,87 | +0,81 | DOĞRU |
| A5 | ANA | `ABD · havuz · r · MOM · 2X3 · LQ` | `US_MOM` | 91 | +0,89 | +0,87 | %84 | +1,07 | +0,10 (+0,20) | +0,00 (+0,01) | +0,90 | +0,89 | DOĞRU |
| A6 | ANA | `ABD · havuz · r · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | 96 | +0,74 | +0,68 | %71 | +0,66 | +0,52 (+0,86) | +0,61 (+0,89) | +0,62 | +0,78 | DOĞRU |
| A7 | ANA | `ABD · havuz · r · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | 96 | +0,73 | +0,75 | %77 | +0,95 | +0,07 (+0,07) | +0,17 (+0,22) | +0,64 | +0,76 | DOĞRU |
| A8 | ANA | `ABD · havuz · r · STREV · 2X3 · LQ` | `US_STREV` | 96 | +0,87 | +0,85 | %76 | +0,97 | +0,17 (+0,45) | +0,29 (+0,87) | +0,82 | +0,89 | DOĞRU |
| E1 | ANA | `AVR · havuz · r · PIYASA · - · LQ` | `EU_MKT` | 96 | +0,99 | +0,98 | %97 | +1,05 | +0,68 (+1,25) | +0,70 (+1,35) | +0,98 | +0,99 | DOĞRU |
| E2 | ANA | `AVR · havuz · r · PIYASA · - · EW` | `EU_MKT` | 96 | +0,98 | +0,98 | %96 | +1,13 | +0,72 (+1,22) | +0,70 (+1,35) | +0,97 | +0,99 | DOĞRU |
| E3 | ANA | `AVR · havuz · r · MOM · 2X3 · LQ` | `EU_WML` | 96 | +0,96 | +0,92 | %86 | +1,23 | +0,07 (+0,16) | +0,47 (+1,39) | +0,91 | +0,97 | DOĞRU |
| E4 | ANA | `AVR · havuz · r · MOM · D10-D1 · EW` | `EU_WML` | 96 | +0,91 | +0,86 | %82 | +1,79 | -0,28 (-0,42) | +0,47 (+1,39) | +0,81 | +0,95 | DOĞRU |
| A1.1 | TEŞHİS | `ABD · buyuk · r · PIYASA · - · EW` | `US_EWMKT` | 96 | +0,94 | +0,91 | %92 | +0,81 | +1,19 (+2,02) | +0,93 (+1,36) | +0,95 | +0,94 | DOĞRU |
| A1.2 | TEŞHİS | `ABD · tum · r · PIYASA · - · EW` | `US_EWMKT` | 96 | +0,92 | +0,97 | %93 | +1,09 | +1,82 (+2,26) | +0,93 (+1,36) | +0,98 | +0,92 | DOĞRU |
| A1.3 | TEŞHİS | `ABD · havuz · r · PIYASA · - · LQ` | `US_MKT` | 96 | +0,95 | +0,92 | %93 | +1,25 | +1,54 (+2,38) | +1,15 (+2,34) | +0,98 | +0,95 | DOĞRU |
| A1.4 | TEŞHİS | `ABD · havuz · r_os · PIYASA · - · EW` | `US_EWMKT` | 95 | +0,96 | +0,93 | %92 | +0,95 | +1,04 (+1,54) | +0,82 (+1,20) | +0,95 | +0,96 | DOĞRU |
| A2.1 | TEŞHİS | `ABD · buyuk · r · PIYASA · - · LQ` | `US_MKT` | 96 | +0,95 | +0,91 | %94 | +1,25 | +1,56 (+2,39) | +1,15 (+2,34) | +0,98 | +0,94 | DOĞRU |
| A2.2 | TEŞHİS | `ABD · tum · r · PIYASA · - · LQ` | `US_MKT` | 96 | +0,95 | +0,92 | %94 | +1,26 | +1,55 (+2,39) | +1,15 (+2,34) | +0,98 | +0,94 | DOĞRU |
| A2.3 | TEŞHİS | `ABD · havuz · r · PIYASA · - · EW` | `US_EWMKT` | 96 | +0,96 | +0,94 | %94 | +0,89 | +1,25 (+1,98) | +0,93 (+1,36) | +0,96 | +0,96 | DOĞRU |
| A2.4 | TEŞHİS | `ABD · havuz · r_os · PIYASA · - · LQ` | `US_MKT` | 95 | +0,92 | +0,87 | %89 | +1,29 | +1,39 (+2,00) | +1,11 (+2,23) | +0,95 | +0,91 | DOĞRU |
| A3.1 | TEŞHİS | `ABD · buyuk · r · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | 91 | +0,61 | +0,52 | %65 | +0,73 | +0,47 (+0,57) | +0,68 (+0,98) | +0,57 | +0,64 | KISMEN |
| A3.2 | TEŞHİS | `ABD · tum · r · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | 91 | +0,47 | +0,66 | %73 | +2,33 | -3,20 (-0,93) | +0,68 (+0,98) | +0,70 | +0,49 | KISMEN |
| A3.3 | TEŞHİS | `ABD · havuz · r · MOM · D10-D1 · LQ` | `US_P12_EW_FARK` | 91 | +0,44 | +0,38 | %59 | +0,64 | +1,03 (+1,02) | +0,68 (+0,98) | +0,52 | +0,42 | KISMEN |
| A3.4 | TEŞHİS | `ABD · havuz · r · MOM · D10-D1 · EW` | `US_P12_VW_FARK` | 91 | +0,79 | +0,76 | %85 | +0,64 | +0,67 (+0,92) | +0,01 (+0,01) | +0,84 | +0,79 | DOĞRU |
| A3.5 | TEŞHİS | `ABD · havuz · r_os · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | 90 | +0,69 | +0,57 | %69 | +0,76 | +0,29 (+0,37) | +0,69 (+0,99) | +0,56 | +0,74 | KISMEN |
| A4.1 | TEŞHİS | `ABD · buyuk · r · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | 91 | +0,76 | +0,83 | %84 | +0,86 | +0,95 (+0,93) | +0,01 (+0,01) | +0,89 | +0,73 | DOĞRU |
| A4.2 | TEŞHİS | `ABD · tum · r · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | 91 | +0,82 | +0,83 | %87 | +1,00 | +1,36 (+1,23) | +0,01 (+0,01) | +0,82 | +0,83 | DOĞRU |
| A4.3 | TEŞHİS | `ABD · havuz · r · MOM · D10-D1 · EW` | `US_P12_VW_FARK` | 91 | +0,79 | +0,76 | %85 | +0,64 | +0,67 (+0,92) | +0,01 (+0,01) | +0,84 | +0,79 | DOĞRU |
| A4.4 | TEŞHİS | `ABD · havuz · r · MOM · D10-D1 · LQ` | `US_P12_EW_FARK` | 91 | +0,44 | +0,38 | %59 | +0,64 | +1,03 (+1,02) | +0,68 (+0,98) | +0,52 | +0,42 | KISMEN |
| A4.5 | TEŞHİS | `ABD · havuz · r_os · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | 90 | +0,79 | +0,82 | %81 | +0,90 | +0,95 (+0,93) | +0,18 (+0,20) | +0,83 | +0,79 | DOĞRU |
| A5.1 | TEŞHİS | `ABD · buyuk · r · MOM · 2X3 · LQ` | `US_MOM` | 91 | +0,89 | +0,86 | %84 | +1,11 | +0,20 (+0,38) | +0,00 (+0,01) | +0,89 | +0,89 | DOĞRU |
| A5.2 | TEŞHİS | `ABD · tum · r · MOM · 2X3 · LQ` | `US_MOM` | 91 | +0,91 | +0,86 | %84 | +1,20 | +0,03 (+0,06) | +0,00 (+0,01) | +0,91 | +0,91 | DOĞRU |
| A5.3 | TEŞHİS | `ABD · havuz · r · MOM · U30A30 · EW` | `US_MOM` | 91 | +0,93 | +0,92 | %84 | +1,02 | +0,20 (+0,43) | +0,00 (+0,01) | +0,92 | +0,94 | DOĞRU |
| A5.4 | TEŞHİS | `ABD · havuz · r_os · MOM · 2X3 · LQ` | `US_MOM` | 90 | +0,87 | +0,83 | %83 | +1,08 | -0,05 (-0,09) | +0,06 (+0,15) | +0,89 | +0,86 | DOĞRU |
| A6.1 | TEŞHİS | `ABD · buyuk · r · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | 96 | +0,67 | +0,65 | %69 | +0,62 | +0,41 (+0,64) | +0,61 (+0,89) | +0,56 | +0,71 | KISMEN |
| A6.2 | TEŞHİS | `ABD · tum · r · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | 96 | +0,30 | +0,68 | %73 | +1,30 | +3,62 (+1,24) | +0,61 (+0,89) | +0,66 | +0,30 | UYUŞMUYOR |
| A6.3 | TEŞHİS | `ABD · havuz · r · STREV · D1-D10 · LQ` | `US_P1_EW_FARK` | 96 | +0,44 | +0,46 | %67 | +0,64 | +0,07 (+0,07) | +0,61 (+0,89) | +0,42 | +0,47 | KISMEN |
| A6.4 | TEŞHİS | `ABD · havuz · r · STREV · D1-D10 · EW` | `US_P1_VW_FARK` | 96 | +0,76 | +0,64 | %67 | +0,60 | +0,52 (+0,86) | +0,17 (+0,22) | +0,72 | +0,77 | KISMEN |
| A6.5 | TEŞHİS | `ABD · havuz · r_os · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | 95 | +0,75 | +0,64 | %71 | +0,73 | +0,58 (+0,87) | +0,62 (+0,91) | +0,59 | +0,80 | DOĞRU |
| A7.1 | TEŞHİS | `ABD · buyuk · r · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | 96 | +0,71 | +0,75 | %74 | +0,91 | +0,12 (+0,13) | +0,17 (+0,22) | +0,63 | +0,74 | DOĞRU |
| A7.2 | TEŞHİS | `ABD · tum · r · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | 96 | +0,68 | +0,73 | %81 | +0,92 | +0,12 (+0,12) | +0,17 (+0,22) | +0,54 | +0,72 | KISMEN |
| A7.3 | TEŞHİS | `ABD · havuz · r · STREV · D1-D10 · EW` | `US_P1_VW_FARK` | 96 | +0,76 | +0,64 | %67 | +0,60 | +0,52 (+0,86) | +0,17 (+0,22) | +0,72 | +0,77 | KISMEN |
| A7.4 | TEŞHİS | `ABD · havuz · r · STREV · D1-D10 · LQ` | `US_P1_EW_FARK` | 96 | +0,44 | +0,46 | %67 | +0,64 | +0,07 (+0,07) | +0,61 (+0,89) | +0,42 | +0,47 | KISMEN |
| A7.5 | TEŞHİS | `ABD · havuz · r_os · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | 95 | +0,75 | +0,76 | %78 | +1,01 | +0,28 (+0,27) | +0,19 (+0,25) | +0,68 | +0,77 | DOĞRU |
| A8.1 | TEŞHİS | `ABD · buyuk · r · STREV · 2X3 · LQ` | `US_STREV` | 96 | +0,89 | +0,85 | %82 | +1,13 | +0,34 (+0,81) | +0,29 (+0,87) | +0,77 | +0,92 | DOĞRU |
| A8.2 | TEŞHİS | `ABD · tum · r · STREV · 2X3 · LQ` | `US_STREV` | 96 | +0,85 | +0,82 | %76 | +1,05 | +0,23 (+0,56) | +0,29 (+0,87) | +0,82 | +0,86 | DOĞRU |
| A8.3 | TEŞHİS | `ABD · havuz · r · STREV · A30U30 · EW` | `US_STREV` | 96 | +0,90 | +0,80 | %76 | +0,97 | +0,19 (+0,53) | +0,29 (+0,87) | +0,88 | +0,90 | DOĞRU |
| A8.4 | TEŞHİS | `ABD · havuz · r_os · STREV · 2X3 · LQ` | `US_STREV` | 95 | +0,87 | +0,81 | %73 | +1,07 | +0,21 (+0,52) | +0,33 (+1,01) | +0,81 | +0,89 | DOĞRU |
| E1.1 | TEŞHİS | `AVR · buyuk · r · PIYASA · - · LQ` | `EU_MKT` | 96 | +0,98 | +0,98 | %97 | +1,03 | +0,67 (+1,23) | +0,70 (+1,35) | +0,98 | +0,98 | DOĞRU |
| E1.2 | TEŞHİS | `AVR · tum · r · PIYASA · - · LQ` | `EU_MKT` | 96 | +0,99 | +0,98 | %97 | +1,05 | +0,69 (+1,25) | +0,70 (+1,35) | +0,98 | +0,99 | DOĞRU |
| E1.3 | TEŞHİS | `AVR · havuz · r_os · PIYASA · - · LQ` | `EU_MKT` | 95 | +0,89 | +0,87 | %87 | +0,81 | +0,55 (+1,16) | +0,64 (+1,24) | +0,86 | +0,91 | KISMEN |
| E1.4 | TEŞHİS | `AVR · havuz · r_eur · PIYASA · - · LQ` | `EU_MKT` | 96 | +0,91 | +0,87 | %88 | +0,82 | +0,63 (+1,36) | +0,70 (+1,35) | +0,85 | +0,93 | DOĞRU |
| E2.1 | TEŞHİS | `AVR · buyuk · r · PIYASA · - · EW` | `EU_MKT` | 96 | +0,99 | +0,98 | %97 | +1,10 | +0,66 (+1,15) | +0,70 (+1,35) | +0,98 | +0,99 | DOĞRU |
| E2.2 | TEŞHİS | `AVR · tum · r · PIYASA · - · EW` | `EU_MKT` | 96 | +0,98 | +0,97 | %96 | +1,13 | +0,79 (+1,33) | +0,70 (+1,35) | +0,97 | +0,98 | DOĞRU |
| E2.3 | TEŞHİS | `AVR · havuz · r_os · PIYASA · - · EW` | `EU_MKT` | 95 | +0,90 | +0,88 | %88 | +0,88 | +0,55 (+1,08) | +0,64 (+1,24) | +0,86 | +0,92 | DOĞRU |
| E2.4 | TEŞHİS | `AVR · havuz · r_eur · PIYASA · - · EW` | `EU_MKT` | 96 | +0,91 | +0,87 | %88 | +0,90 | +0,67 (+1,30) | +0,70 (+1,35) | +0,84 | +0,93 | DOĞRU |
| E3.1 | TEŞHİS | `AVR · buyuk · r · MOM · 2X3 · LQ` | `EU_WML` | 96 | +0,92 | +0,90 | %82 | +1,25 | -0,05 (-0,10) | +0,47 (+1,39) | +0,90 | +0,94 | DOĞRU |
| E3.2 | TEŞHİS | `AVR · tum · r · MOM · 2X3 · LQ` | `EU_WML` | 96 | +0,95 | +0,92 | %85 | +1,21 | +0,05 (+0,12) | +0,47 (+1,39) | +0,92 | +0,96 | DOĞRU |
| E3.3 | TEŞHİS | `AVR · havuz · r_os · MOM · 2X3 · LQ` | `EU_WML` | 95 | +0,94 | +0,89 | %89 | +1,21 | +0,10 (+0,23) | +0,52 (+1,52) | +0,91 | +0,95 | DOĞRU |
| E3.4 | TEŞHİS | `AVR · havuz · r_eur · MOM · 2X3 · LQ` | `EU_WML` | 96 | +0,95 | +0,92 | %86 | +1,22 | +0,08 (+0,19) | +0,47 (+1,39) | +0,91 | +0,97 | DOĞRU |
| E4.1 | TEŞHİS | `AVR · buyuk · r · MOM · D10-D1 · EW` | `EU_WML` | 96 | +0,87 | +0,83 | %74 | +1,76 | -0,47 (-0,68) | +0,47 (+1,39) | +0,81 | +0,90 | DOĞRU |
| E4.2 | TEŞHİS | `AVR · tum · r · MOM · D10-D1 · EW` | `EU_WML` | 96 | +0,90 | +0,85 | %78 | +1,76 | -0,32 (-0,49) | +0,47 (+1,39) | +0,78 | +0,95 | DOĞRU |
| E4.3 | TEŞHİS | `AVR · havuz · r_os · MOM · D10-D1 · EW` | `EU_WML` | 95 | +0,89 | +0,82 | %83 | +1,75 | -0,10 (-0,14) | +0,52 (+1,52) | +0,79 | +0,93 | DOĞRU |
| E4.4 | TEŞHİS | `AVR · havuz · r_eur · MOM · D10-D1 · EW` | `EU_WML` | 96 | +0,91 | +0,86 | %82 | +1,77 | -0,27 (-0,40) | +0,47 (+1,39) | +0,81 | +0,95 | DOĞRU |

### Onluk seviyeleri (bilgi; piyasa eşiği)

| kod | ay | Pearson | işaret | eğim | biz ort | ref ort | hüküm |
|---|---|---|---|---|---|---|---|
| O.MOM.D1.EW | 91 | +0,90 | %82 | +0,85 | +1,41 | +0,57 | KISMEN |
| O.MOM.D1.LQ | 91 | +0,94 | %91 | +1,00 | +1,40 | +1,26 | DOĞRU |
| O.MOM.D2.EW | 91 | +0,93 | %89 | +0,92 | +1,28 | +1,13 | DOĞRU |
| O.MOM.D2.LQ | 91 | +0,91 | %88 | +0,96 | +1,63 | +1,26 | DOĞRU |
| O.MOM.D3.EW | 91 | +0,96 | %95 | +0,98 | +1,16 | +1,22 | DOĞRU |
| O.MOM.D3.LQ | 91 | +0,94 | %90 | +0,96 | +1,52 | +1,50 | DOĞRU |
| O.MOM.D4.EW | 91 | +0,95 | %95 | +0,94 | +1,25 | +1,19 | DOĞRU |
| O.MOM.D4.LQ | 91 | +0,92 | %85 | +0,97 | +1,22 | +1,20 | DOĞRU |
| O.MOM.D5.EW | 91 | +0,95 | %91 | +0,92 | +1,03 | +1,09 | DOĞRU |
| O.MOM.D5.LQ | 91 | +0,89 | %92 | +0,94 | +1,20 | +1,06 | KISMEN |
| O.MOM.D6.EW | 91 | +0,93 | %90 | +0,92 | +0,98 | +1,10 | DOĞRU |
| O.MOM.D6.LQ | 91 | +0,94 | %88 | +1,06 | +1,02 | +1,23 | DOĞRU |
| O.MOM.D7.EW | 91 | +0,94 | %90 | +1,03 | +1,08 | +1,03 | DOĞRU |
| O.MOM.D7.LQ | 91 | +0,91 | %89 | +1,12 | +1,69 | +1,14 | DOĞRU |
| O.MOM.D8.EW | 91 | +0,94 | %92 | +0,89 | +1,14 | +1,00 | DOĞRU |
| O.MOM.D8.LQ | 91 | +0,90 | %88 | +1,06 | +0,82 | +0,88 | KISMEN |
| O.MOM.D9.EW | 91 | +0,92 | %86 | +0,87 | +1,22 | +1,20 | DOĞRU |
| O.MOM.D9.LQ | 91 | +0,92 | %82 | +1,09 | +1,35 | +0,98 | DOĞRU |
| O.MOM.D10.EW | 91 | +0,94 | %85 | +1,02 | +2,08 | +1,25 | DOĞRU |
| O.MOM.D10.LQ | 91 | +0,91 | %85 | +1,36 | +2,43 | +1,27 | DOĞRU |
| O.STREV.D1.EW | 96 | +0,92 | %84 | +0,82 | +1,78 | +1,01 | DOĞRU |
| O.STREV.D1.LQ | 96 | +0,91 | %91 | +1,01 | +1,79 | +1,46 | DOĞRU |
| O.STREV.D2.EW | 96 | +0,95 | %86 | +0,91 | +1,24 | +0,84 | DOĞRU |
| O.STREV.D2.LQ | 96 | +0,94 | %92 | +1,08 | +1,46 | +1,18 | DOĞRU |
| O.STREV.D3.EW | 96 | +0,95 | %92 | +0,89 | +1,15 | +1,12 | DOĞRU |
| O.STREV.D3.LQ | 96 | +0,92 | %90 | +0,91 | +1,45 | +1,29 | DOĞRU |
| O.STREV.D4.EW | 96 | +0,95 | %88 | +0,94 | +1,35 | +1,21 | DOĞRU |
| O.STREV.D4.LQ | 96 | +0,93 | %88 | +1,10 | +1,29 | +1,22 | DOĞRU |
| O.STREV.D5.EW | 96 | +0,94 | %92 | +0,92 | +1,20 | +1,17 | DOĞRU |
| O.STREV.D5.LQ | 96 | +0,93 | %88 | +1,17 | +1,49 | +1,32 | DOĞRU |
| O.STREV.D6.EW | 96 | +0,96 | %91 | +0,89 | +1,12 | +1,04 | DOĞRU |
| O.STREV.D6.LQ | 96 | +0,88 | %84 | +0,95 | +1,69 | +1,27 | KISMEN |
| O.STREV.D7.EW | 96 | +0,94 | %88 | +0,89 | +1,07 | +1,00 | DOĞRU |
| O.STREV.D7.LQ | 96 | +0,90 | %89 | +1,10 | +1,23 | +1,17 | KISMEN |
| O.STREV.D8.EW | 96 | +0,92 | %85 | +0,87 | +1,05 | +0,79 | DOĞRU |
| O.STREV.D8.LQ | 96 | +0,90 | %93 | +1,09 | +1,10 | +1,01 | DOĞRU |
| O.STREV.D9.EW | 96 | +0,95 | %93 | +0,90 | +1,29 | +0,80 | DOĞRU |
| O.STREV.D9.LQ | 96 | +0,85 | %84 | +1,09 | +1,23 | +1,00 | KISMEN |
| O.STREV.D10.EW | 96 | +0,90 | %85 | +0,91 | +1,26 | +0,40 | KISMEN |
| O.STREV.D10.LQ | 96 | +0,86 | %83 | +1,29 | +1,72 | +1,29 | KISMEN |

## 3. EN ÇOK AYRIŞAN 10 AY (ana çiftler; % puan)

- **A1** (ABD evren getirisi EW vs French EW piyasa (Prior_12_2 EW onlukları, firma ağırlıklı)): 2021-01 biz +2,61 / ref +11,46; 2023-03 biz -1,80 / ref -6,40; 2022-11 biz +5,10 / ref +0,51; 2020-06 biz +2,86 / ref +6,97; 2023-01 biz +11,48 / ref +15,35; 2017-09 biz +3,99 / ref +7,22; 2022-10 biz +10,08 / ref +7,02; 2016-11 biz +6,09 / ref +9,01; 2021-10 biz +5,37 / ref +2,49; 2022-06 biz -9,71 / ref -6,86
- **A2** (ABD evren getirisi LQ vs French piyasa (Mkt-RF + RF, VW)): 2020-08 biz +17,56 / ref +7,63; 2023-01 biz +14,65 / ref +6,96; 2023-05 biz +6,54 / ref +0,70; 2021-12 biz -1,88 / ref +3,24; 2020-11 biz +17,12 / ref +12,46; 2021-01 biz +4,42 / ref -0,07; 2022-04 biz -13,69 / ref -9,41; 2020-04 biz +17,84 / ref +13,60; 2022-07 biz +13,79 / ref +9,65; 2020-06 biz +6,30 / ref +2,46
- **A3** (ABD MOM onluk üst - alt EW vs French Prior_12_2 EW Hi - Lo): 2020-07 biz +19,21 / ref +1,39; 2021-01 biz +9,85 / ref -6,87; 2019-06 biz -7,72 / ref +4,28; 2019-01 biz -5,06 / ref -15,53; 2019-08 biz +14,00 / ref +4,33; 2020-01 biz +8,12 / ref -1,32; 2016-11 biz -5,29 / ref +3,98; 2023-03 biz -0,17 / ref +8,86; 2020-03 biz +14,09 / ref +5,08; 2022-07 biz -6,00 / ref +2,95
- **A4** (ABD MOM onluk üst - alt LQ vs French Prior_12_2 VW Hi - Lo): 2020-04 biz -8,47 / ref -32,08; 2020-07 biz +29,51 / ref +11,11; 2021-01 biz +12,35 / ref -4,49; 2020-11 biz -12,11 / ref -27,10; 2020-06 biz +3,93 / ref -10,77; 2023-06 biz -14,40 / ref -1,28; 2019-01 biz +3,68 / ref -8,61; 2019-09 biz -18,51 / ref -8,18; 2020-08 biz +16,81 / ref +7,61; 2023-05 biz +12,61 / ref +3,90
- **A5** (ABD MOM 2x3 (üst 30 - alt 30) LQ vs French Mom): 2020-07 biz +14,01 / ref +7,70; 2020-11 biz -6,98 / ref -12,60; 2020-12 biz +3,17 / ref -2,26; 2018-10 biz -7,18 / ref -2,00; 2019-01 biz -4,03 / ref -8,64; 2021-02 biz -12,09 / ref -7,99; 2023-10 biz +5,36 / ref +1,69; 2020-01 biz +2,45 / ref +6,02; 2019-05 biz +10,99 / ref +7,56; 2020-09 biz -0,22 / ref +3,18
- **A6** (ABD STREV onluk alt - üst EW vs French Prior_1_0 EW Lo - Hi): 2020-04 biz +25,12 / ref +44,33; 2020-03 biz -19,08 / ref -7,09; 2019-01 biz +8,68 / ref +19,58; 2022-01 biz -11,99 / ref -1,79; 2020-05 biz -9,32 / ref +0,78; 2023-05 biz +10,48 / ref +2,11; 2020-02 biz -4,14 / ref -11,73; 2021-06 biz +10,39 / ref +3,10; 2020-06 biz -0,84 / ref +6,30; 2019-09 biz +9,82 / ref +2,86
- **A7** (ABD STREV onluk alt - üst LQ vs French Prior_1_0 VW Lo - Hi): 2020-08 biz -34,70 / ref -9,02; 2020-04 biz +17,97 / ref +38,91; 2018-10 biz +23,31 / ref +3,07; 2020-11 biz +17,81 / ref -0,11; 2020-01 biz -13,28 / ref +2,55; 2018-09 biz -14,23 / ref -2,08; 2016-03 biz -1,33 / ref +9,18; 2021-06 biz +16,07 / ref +6,21; 2021-02 biz +21,76 / ref +12,37; 2017-09 biz +1,54 / ref +10,82
- **A8** (ABD STREV 2x3 (alt 30 - üst 30) LQ vs French ST_Rev): 2020-08 biz -7,93 / ref -2,44; 2020-04 biz +10,71 / ref +15,72; 2021-10 biz -6,03 / ref -1,67; 2023-01 biz +13,42 / ref +9,60; 2023-05 biz +7,42 / ref +4,04; 2019-05 biz +3,95 / ref +0,71; 2016-04 biz -2,40 / ref +0,42; 2019-11 biz -2,95 / ref -0,18; 2023-02 biz -4,03 / ref -1,41; 2019-01 biz +5,63 / ref +8,19
- **E1** (AVR evren getirisi LQ (USD) vs French Avrupa piyasa (USD)): 2022-01 biz -2,09 / ref -5,39; 2020-11 biz +19,46 / ref +16,63; 2019-01 biz +8,34 / ref +6,40; 2021-11 biz -6,16 / ref -4,29; 2022-05 biz +3,17 / ref +1,30; 2020-03 biz -17,13 / ref -15,32; 2020-04 biz +4,97 / ref +6,70; 2023-01 biz +10,03 / ref +8,48; 2021-02 biz +4,05 / ref +2,60; 2022-10 biz +8,34 / ref +6,89
- **E2** (AVR evren getirisi EW (USD) vs French Avrupa piyasa (USD)): 2020-03 biz -19,63 / ref -15,32; 2020-11 biz +19,92 / ref +16,63; 2019-01 biz +9,64 / ref +6,40; 2016-06 biz -8,04 / ref -4,99; 2022-06 biz -12,92 / ref -10,26; 2023-07 biz +5,33 / ref +2,90; 2023-11 biz +12,01 / ref +9,65; 2021-02 biz +4,71 / ref +2,60; 2022-09 biz -11,75 / ref -9,65; 2022-08 biz -8,48 / ref -6,49
- **E3** (AVR MOM 2x3 LQ (USD) vs French Avrupa WML): 2020-11 biz -24,25 / ref -18,39; 2018-04 biz -3,26 / ref +0,70; 2018-05 biz +5,37 / ref +2,00; 2022-02 biz -3,05 / ref -0,02; 2022-06 biz +6,94 / ref +3,96; 2016-10 biz -3,64 / ref -0,82; 2021-11 biz -3,27 / ref -0,46; 2016-09 biz +5,88 / ref +3,13; 2019-10 biz -3,96 / ref -1,22; 2016-08 biz -4,26 / ref -1,76
- **E4** (AVR MOM onluk üst - alt EW (USD) vs French Avrupa WML): 2020-11 biz -38,51 / ref -18,39; 2021-02 biz -16,70 / ref -4,52; 2023-01 biz -13,00 / ref -5,26; 2020-07 biz +14,19 / ref +6,71; 2020-09 biz +12,03 / ref +4,86; 2016-02 biz -7,68 / ref -0,70; 2022-06 biz +10,44 / ref +3,96; 2016-05 biz +10,09 / ref +3,81; 2016-04 biz -9,64 / ref -3,91; 2018-09 biz -3,98 / ref +1,59

## 4. EK DOĞRULAMALAR

### E1 gece / gün içi (gün ortalaması baz puan; yıllık toplam %)

| pazar | yıl | gün | hisse | gece EW bp | gün içi EW bp | gece EW yıl % | gün içi EW yıl % | gece LQ bp | gün içi LQ bp | gece LQ yıl % | gün içi LQ yıl % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2015 | 70 | 710 | -0,29 | +2,93 | -0,2 | +2,0 | +2,87 | +2,18 | +2,0 | +1,5 |
| ABD | 2016 | 252 | 730 | +0,86 | +6,65 | +2,2 | +16,8 | +0,93 | +4,61 | +2,4 | +11,6 |
| ABD | 2017 | 251 | 757 | +6,99 | +1,75 | +17,5 | +4,4 | +7,93 | +1,69 | +19,9 | +4,3 |
| ABD | 2018 | 251 | 791 | +5,01 | -7,07 | +12,6 | -17,8 | +6,12 | -6,56 | +15,4 | -16,5 |
| ABD | 2019 | 252 | 830 | +5,47 | +5,82 | +13,8 | +14,7 | +6,32 | +6,49 | +15,9 | +16,4 |
| ABD | 2020 | 253 | 876 | +14,28 | -0,58 | +36,1 | -1,5 | +15,27 | +4,87 | +38,6 | +12,3 |
| ABD | 2021 | 252 | 976 | +11,14 | -2,06 | +28,1 | -5,2 | +10,96 | -1,18 | +27,6 | -3,0 |
| ABD | 2022 | 251 | 1056 | -5,54 | -0,80 | -13,9 | -2,0 | -7,72 | -5,92 | -19,4 | -14,9 |
| ABD | 2023 | 250 | 1078 | +4,93 | +4,23 | +12,3 | +10,6 | +5,04 | +11,75 | +12,6 | +29,4 |
| AVR | 2015 | 177 | 385 | +8,57 | -10,69 | +15,2 | -18,9 | +9,71 | -15,32 | +17,2 | -27,1 |
| AVR | 2016 | 257 | 398 | +2,84 | +2,45 | +7,3 | +6,3 | +2,71 | +1,83 | +7,0 | +4,7 |
| AVR | 2017 | 255 | 404 | +5,38 | +2,49 | +13,7 | +6,4 | +5,33 | +0,65 | +13,6 | +1,6 |
| AVR | 2018 | 256 | 406 | +5,70 | -9,28 | +14,6 | -23,8 | +5,73 | -10,55 | +14,7 | -27,0 |
| AVR | 2019 | 256 | 417 | +4,00 | +6,15 | +10,3 | +15,7 | +2,92 | +5,66 | +7,5 | +14,5 |
| AVR | 2020 | 258 | 429 | +9,85 | -5,18 | +25,4 | -13,4 | +5,33 | -3,53 | +13,8 | -9,1 |
| AVR | 2021 | 258 | 437 | +9,57 | -1,87 | +24,7 | -4,8 | +7,05 | +0,73 | +18,2 | +1,9 |
| AVR | 2022 | 257 | 447 | +1,32 | -6,40 | +3,4 | -16,5 | -0,67 | -1,39 | -1,7 | -3,6 |
| AVR | 2023 | 255 | 452 | +3,93 | +2,36 | +10,0 | +6,0 | +3,43 | +2,50 | +8,8 | +6,4 |

### E2 veri kipi (bizim ay sonu kapanış getirisi vs Yahoo Adj Close / Close; 2016-01..2023-12)

20 / 20 hissede Pearson(bizim, Adj Close) >= 0,99; en düşük +1,0000; medyan aylık fark (bizim - Adj) -0,00 bp, (bizim - Close) +19,96 bp.

| hisse | ay | r(Adj) | r(Close) | fark Adj bp | fark Close bp | maks |fark Adj| % |
|---|---|---|---|---|---|---|
| AAPL | 96 | 1.0000 | 0.9998 | -0,00 | +10,07 | 0.00 |
| MSFT | 96 | 1.0000 | 0.9994 | -0,00 | +12,53 | 0.00 |
| AMZN | 96 | 1.0000 | 1.0000 | +0,00 | +0,00 | 0.00 |
| GOOGL | 96 | 1.0000 | 1.0000 | -0,00 | -0,00 | 0.00 |
| META | 96 | 1.0000 | 1.0000 | -0,00 | -0,00 | 0.00 |
| NVDA | 96 | 1.0000 | 1.0000 | +0,00 | +2,71 | 0.00 |
| JPM | 96 | 1.0000 | 0.9989 | -0,00 | +24,29 | 0.00 |
| XOM | 96 | 1.0000 | 0.9974 | +0,00 | +38,58 | 0.00 |
| JNJ | 96 | 1.0000 | 0.9977 | -0,00 | +22,35 | 0.00 |
| UNH | 96 | 1.0000 | 0.9995 | +0,00 | +12,80 | 0.00 |
| CVX | 96 | 1.0000 | 0.9980 | +0,00 | +35,84 | 0.00 |
| PEP | 96 | 1.0000 | 0.9970 | +0,00 | +24,21 | 0.00 |
| MRK | 96 | 1.0000 | 0.9978 | +0,00 | +25,95 | 0.00 |
| BAC | 96 | 1.0000 | 0.9996 | +0,00 | +17,57 | 0.00 |
| CSCO | 96 | 1.0000 | 0.9986 | -0,00 | +26,25 | 0.00 |
| INTC | 96 | 1.0000 | 0.9991 | +0,00 | +23,28 | 0.00 |
| PFE | 96 | 1.0000 | 0.9978 | -0,00 | +32,06 | 0.00 |
| DIS | 96 | 1.0000 | 0.9997 | -0,00 | +6,51 | 0.00 |
| ORCL | 96 | 1.0000 | 0.9996 | +0,00 | +13,87 | 0.00 |
| ABBV | 96 | 1.0000 | 0.9977 | -0,00 | +35,72 | 0.00 |

## 5. YENİDEN ÜRETİM: TUTTU

Ham V_ABD.pkl'den düz pandas (OC / OS kodu kullanılmadan):

| seri | tutma ayı | elle | kod | tutar |
|---|---|---|---|---|
| `ABD · tum · r · MOM · D10-D1 · EW` | 2017-03 | 0.0002853687 | 0.0002853687 | E |
| `ABD · tum · r · PIYASA · - · EW` | 2017-03 | 0.0075683333 | 0.0075683333 | E |
| `ABD · tum · r · MOM · D10-D1 · EW` | 2020-04 | -0.1483456040 | -0.1483456040 | E |
| `ABD · tum · r · PIYASA · - · EW` | 2020-04 | 0.2058030930 | 0.2058030930 | E |
| `ABD · tum · r · MOM · D10-D1 · EW` | 2023-06 | -0.0680100022 | -0.0680100022 | E |
| `ABD · tum · r · PIYASA · - · EW` | 2023-06 | 0.0874190850 | 0.0874190850 | E |

French ham satırından elle (ayrıştırıcı kullanılmadan; değerler ondalık):

| dosya | ay | ham satır | hesap | elle | kod | tutar |
|---|---|---|---|---|---|---|
| F-F_Momentum_Factor_CSV.zip | 2020-03 | `202003,   8.20` | c[0] | 0.082000 | 0.082000 | E |
| F-F_Research_Data_Factors_CSV.zip | 2018-11 | `201811,   1.71,  -0.72,   0.34,   0.18` | c[0] + c[3] | 0.018900 | 0.018900 | E |
| 10_Portfolios_Prior_12_2_CSV.zip | 2021-06 | `202106,   2.55,   0.56,   1.53,   5.03,  -0.19,   4.14,   1.72,  -1.23,   2.09,   9.25` | c[9] - c[0] | 0.067000 | 0.067000 | E |
| Europe_Mom_Factor_CSV.zip | 2019-12 | `201912    ,1.66` | c[0] | 0.016600 | 0.016600 | E |

## 6. EN GEÇ TARİH

- hisse verisi en geç bar: {'ABD': '2023-12-29', 'AVR': '2023-12-29'}
- referans en geç ay: 2023-12
- Yahoo en geç: 2023-12-29

## 7. VERİ NOTU

- ABD: 1380 hisse, kesit satırı 113860, havuz satırı 87047; kur: -
- AVR: 576 hisse, kesit satırı 55606, havuz satırı 42881; kur: EURUSD=X Yahoo ay son kuru

## 8. HATA (koşu sırasında ve sonrasında bulunan; IK_HATA'ya ana model yazar)

- H-TD1 (doğrulama kodu, koşu 1): td_french_elle Avrupa dosyasında ay satırını 'YYYYMM,' önekiyle aradı; Avrupa dosyalarında ay kodundan sonra boşluk var ('201912    ,2.45') -> satır bulunamadı (StopIteration), yeniden üretim TUTMADI göründü (bizim 6 hücre ve French 3 satır tutmuştu). Ayrıştırıcı td_french_ayristir etkilenmedi (parçaları strip ediyor; EU_WML serisi doğru). Düzeltme: düzenli ifade '^\s*YYYYMM\s*,'. SAPMA: kod sha ön kayıttan farklı; ölçüm YENİDEN KOŞULMADI, yalnız yeniden üretim adımı 'yeniden' komutuyla koşu json'u üzerinde (KASA kapısından sonra) yeniden koşuldu; hükümler ve seriler koşu 1'in aynısı.
- H-TD2 (rapor üreteci, koşu 1): ilk rapor HATA / KONTROL LİSTESİ bölümlerini ve düz Türkçe özet maddelerini basmıyordu (iş tanımı istiyordu). Yalnız gösterim eklendi; sayılar json'dan, değişmedi.
- GÖZLEM (hata değil): 'tum' maskesinde (OS havuz süzgeci yok: likidite alt %20 ve bölünme şüpheli hisse-aylar dahil) STREV onluk farkı EW ayda +3,62% (A6.2, French ile korelasyon 0,30) — havuz dışı hisse-aylarda bayat / ayarsız fiyat sıçramaları alt-üst onluk farkını şişiriyor; havuz süzgeci bunu dışlıyor (A6: 0,74). Ayrıca araştırılmadı.

## 9. KONTROL LİSTESİ (ön kayıttaki tablo aynen)

| Kod | Yanıt | Kanıt |
|---|---|---|
| K1 | UYGULANMAZ | iz / sinyal sınaması yok; doğrulama: bizim aylık portföy serileri = yayımlanmış referans serilerle ay ay; 'kontrol grubu' yerine dış referans (French); eş kurulumu kullanılmaz |
| K2 | EVET | sıralama t kapanışında bilinenle (MOM C_{k-21}/C_{k-252}, STREV C_k/C_{k-21}, Lq t dahil önceki 20 gün); getiri t+1 ayında; onluk sırası getiriden önce; KASA kapısı hisse pkl + referans kesik pkl (2023-12-31); referans 2023-12 sonrası atılır |
| K3 | EVET | OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0); ay sonu t'de geçerli bar şartı (os_kart_sinyal) |
| K4 | UYGULANMAZ | olay yok; ay başına bir portföy getirisi (aylık seri, n = ay); tekrar sayım yok |
| K5 | EVET | birincil getiri French ile aynı kip (ay kapanışından ay kapanışına); OS kipi (t+1 açılış) ayrıca r_os olarak raporlanır |
| K6 | EVET | V_*.pkl tek kip; E2 ile Yahoo Adj Close / Close'a karşı kip ölçülür; AVR Kur (yerel -> EUR) x EURUSD = USD (French Avrupa USD); French yüzde -> ondalık, -99,99 / -999 eksik |
| K7 | EVET | evren bugün işlem gören hisseler (batan yok): seviye getirileri yukarı yanlı, alt onluklar (MOM alt, STREV alt) yukarı yanlı -> MOM farkı aşağı, STREV farkı yukarı yanlı okunur; raporda yazılı; teşhis 'buyuk' maskesi |
| K8 | EVET | 96 tutma ayı (MOM ABD ~90); n < 36 ay ÖLÇÜLEMEDİ; iki alt dönem (2016-19, 2020-23) ayrı; referans 2000-15 vs 2016-23 |
| K9 | EVET | TD_ESIK sha + kod sha + git commit, referans dosya sha'ları ön kayıtta; sıra kod commit -> ön kayıt commit -> koşu; td_kapi ön kaydın işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; hüküm kuralı iş tanımından aynen |
| K10 | EVET | French CSV ayrıştırma: bölüm başlığı + 6 haneli ay satırı; sütun sayısı başlıkla eşit; ham dosyadan rastgele 3 satır elle (rapor) ve test_tezgah_dogrulama; yıllık (4 haneli) satırlar alınmaz |
| K11 | EVET | td_yeniden: iki seri x 3 ay ham pkl'den düz pandas (OC / OS kodu yok); French 3 satır ham metinden |
| K12 | EVET | iz iddiası yok; hüküm yalnız önceden yazılı eşikle; sayı ve yorum ayrı cümle |
| K13 | EVET | çakışma kapısı (_cakisma_kontrol_td; test); OS / OC / KASA / defter / kart / kasa / tezgah2 dosyalarına dokunulmadı; dış istek yalnız French + Yahoo (kimlik yok, Tiingo yok); e-posta / anahtar taraması (_td_yaz) |
| K14 | UYGULANMAZ | öneri / gerçek para işi değil; tezgâh doğrulaması |
