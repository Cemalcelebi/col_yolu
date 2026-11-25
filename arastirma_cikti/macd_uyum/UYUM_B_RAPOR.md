# MACD_UYUM — U1b RAPOR (Ç219: bariz derin ikinci dip >= %5, fitil yok)

Ön kayıt: UYUM_B_ON_KAYIT.md (git d1ca775, 2026-11-24 19:42:18 UTC). Kontrol kapısı geçti. Doğrulama: Ç217 U1 ABD 2016-19 birebir. Betik: u1b_olc.py. Sonuç dosyası: uyum_b_sonuc.json. Plasebo hariç; evren bugün işlem görenler; açık veri 2016-22.

## KARAR: **TUTMADI**
Dört karar hücresinin dördü de TUTMADI (güç 0,86-1,00). U1b − U1e farkı yön değiştiriyor. Derinlikle artış 4 karar hücresinin 3'ünde var, Avrupa 2020-22'de ters; bu yüzden "derinlikle artıyor" denmez.

| hip | pazar | dönem | n | FARK [%95] | SIRA [alt] | L3O | güç | hüküm | +%5 olay / eş | stop olay / eş | r15 olay / eş |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U1b | ABD | 2016-19 | 505 | -0,36 [-1,54; +0,60] | 0,495 [0,456] | -1,23 | 0,98 | TUTMADI | 49,8 / 47,4 | 35,2 / 30,8 | +1,13 / +1,49 |
| U1b | ABD | 2020-22 | 848 | +0,04 [-0,92; +1,15] | 0,492 [0,469] | -0,60 | 1,00 | TUTMADI | 48,8 / 49,8 | 42,9 / 39,4 | +2,04 / +2,01 |
| U1b | AVR | 2016-19 | 189 | +1,52 [-0,36; +3,25] | 0,533 [0,471] | +0,08 | 0,86 | TUTMADI | 47,3 / 45,6 | 26,3 / 26,7 | +2,77 / +1,25 |
| U1b | AVR | 2020-22 | 260 | +0,63 [-0,67; +2,02] | 0,532 [0,493] | -0,33 | 0,89 | TUTMADI | 54,9 / 51,6 | 34,6 / 33,4 | +3,94 / +3,31 |
| U1b | BIST (bilgi) | 2016-19 | 271 | +1,38 [-1,08; +4,97] | 0,519 [0,479] | -0,58 | 0,97 | TUTMADI | 42,2 / 44,2 | 37,7 / 38,0 | +1,31 / -0,07 |
| U1b | BIST (bilgi) | 2020-22 | 114 | -1,38 [-3,04; -0,02] | 0,459 [0,407] | -2,35 | 0,45 | ÖLÇÜLEMEDİ | 43,9 / 44,7 | 47,4 / 38,9 | -0,65 / +0,73 |
| U1bb (>= %10) | ABD | 2016-19 | 197 | -0,03 [-1,98; +1,63] | 0,501 | -1,44 | 0,68 | ÖLÇÜLEMEDİ | 56,7 / 52,1 | 30,5 / 29,2 | +2,34 / +2,37 |
| U1bb (>= %10) | ABD | 2020-22 | 387 | +0,94 [-0,44; +2,69] | 0,501 | +0,01 | 0,85 | TUTMADI | 51,2 / 50,5 | 46,7 / 42,3 | +2,28 / +1,35 |
| U1bb (>= %10) | AVR | 2016-19 | 67 | +3,25 [-0,09; +7,64] | 0,537 | +0,28 | 0,41 | ÖLÇÜLEMEDİ | 53,0 / 51,6 | 21,2 / 23,0 | +5,60 / +2,35 |
| U1bb (>= %10) | AVR | 2020-22 | 93 | -0,18 [-3,07; +2,71] | 0,511 | -2,53 | 0,44 | ÖLÇÜLEMEDİ | 51,1 / 53,0 | 45,7 / 33,5 | +2,84 / +3,03 |

U1b − U1e (puan): ABD 2016-19 +0,57, ABD 2020-22 -0,09, AVR 2016-19 +1,59, AVR 2020-22 -0,08.

## Derinlik dilimleri (bilgi; FARK puan, n)
| hücre | e (> -%1) | d1 (-1..-5) | d2 (-5..-10) | d3 (<= -10) | Spearman |
|---|---|---|---|---|---|
| ABD 2016-19 | -0,93 (305) | -0,07 (469) | -0,56 (308) | -0,03 (197) | +0,80 |
| ABD 2020-22 | +0,12 (354) | +0,13 (691) | -0,72 (461) | +0,94 (387) | +0,40 |
| AVR 2016-19 | -0,07 (161) | -0,31 (281) | +0,57 (122) | +3,25 (67) | +0,80 |
| AVR 2020-22 | +0,71 (151) | -0,08 (225) | +1,08 (167) | -0,18 (93) | -0,40 |

## Eşiğe en yakın
- AVR 2016-19: U1b +1,52 [-0,36; +3,25], SIRA 0,533, L3O +0,08; %10'dan derin dipte +3,25 (n 67, güç 0,41).
- ABD'de yok; Avrupa 2020-22'de dilimler karışık. Cemal'in kuralı (her yerde aynı yön) geçmiyor.

## K47 özeti (dört ölçüm)
| ölçüm | sonuç |
|---|---|
| YAPI_HEDEF 8. tur (taban kırılımı içinde) | ÖLÇÜLEMEDİ |
| Ç217 (dipte, tek başına) | TUTMADI |
| Ç218 (net dip, >= %1) | TUTMADI |
| Ç219 (bariz dip, >= %5) | TUTMADI |

Karar Cemal'in:
- (a) K47 kapanır.
- (b) Yalnız U1b, KASA 2023-24 bloklarıyla bir kez kör sınanır. Bunun öncesinde plasebo kapısı MACD_UYUM ile koşulur.
