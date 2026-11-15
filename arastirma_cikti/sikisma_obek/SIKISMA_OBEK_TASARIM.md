# SIKISMA_OBEK (S5) — TASARIM SINAMASI (ön kayıttan ÖNCE; getiri / sonuç ölçülmedi)

SIKISMA_OBEK v1.0 (2026-11-15): öbek sıkışması S5 (öbek + zıplama hariç küçük mum + Bollinger şart; DİP / YOL ÜSTÜ sınıfı) -> büyük hareket

- ZAMAN (UTC): `2026-11-15 09:10:01 UTC`
- Fiyat kaynakları: ekran, V_BIST (ekran = Yahoo x bölünme çarpanı, tespit oranla; V_BIST = düzeltilmiş).
- Izgara: p [15, 20], k_m [0.65, 0.75, 0.85], bant BIST %8 / ABD-AVR %6, BIST %10 / ABD-AVR %8, bb [0.15, 0.2, 0.25], uzunluk ['p', '10'] -> 72 nokta.
- Sabit (ızgara dışı): eğim [-0.02, 0.1], aşağı açılış <= 0.5, DİP konum120 <= 0.25 ve tepeden <= -0.1, YOL konum120 >= 0.6 + SMA50 üstü ve yükselen + taban (ilk 5 gün min x 0.99).
- Örnek kuralı: SEÇMELİ tutar: karar günü (t) örnek aralığında [ilk, son] olan en az bir S5 günü VE o gün sınıf doğru. SEÇMEMELİ tutar: aralıkta hiç S5 günü yok (sınıf ne olursa olsun). Aralıklar iş tanımındaki ekran-fiyat aralıkları (CCOLA seçmeli: 02.10-20.10.2025).
- Seçim kuralı: (1) 7 örnek x 2 fiyat kaynağı (ekran / V_BIST) = 14 sınamanın hepsini tutan noktalar; yoksa en çok tutan noktalar. (2) Aralarından EN SADE: orta noktadan (p 15, k_m 0,75, bant 8/6, bb 0,20, uzunluk 'p') farklı parametre sayısı en az. (3) Eşitlikte sıra: p küçük, |k_m - 0,75| küçük, bant dar, |bb - 0,20| küçük, uzunluk 'p'; yine eşitse SIKI olan (k_m küçük, bb küçük).

## Sonuç: en çok tutan 14 / 14 sınama; 14/14 tutan nokta 16; aday 16 nokta

**SEÇİLEN:** p = 15, k_m = 0.75, bant BIST %8 / ABD-AVR %6, bb = 0.2, uzunluk 'p'.

Seçilen noktada kaçan sınama: YOK.

## Tasarım sınaması tablosu (seçilen nokta; örnek x koşul: aralıkta en az bir gün sağlandı = E)

| örnek | kaynak | beklenen | S5 sonucu | (a) mum | (b) öbek | (c) eğim | (d) aşağı açılış | (e) BB | (f) uzunluk | (a-f) hep | DİP | YOL | tutar | en iyi gün ölçüleri (mum/ATR, öbek, eğim, BB yüzdelik, konum120, 120 gün tepeden) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FENER-E 10-14..11-07 | ekran | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %3.8, %+2.2, 0.16, 0.01, %-83 (2025-10-31) |
| FENER-E 10-14..11-07 | V_BIST | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.69, %3.8, %+2.2, 0.16, 0.12, %-30 (2025-10-31) |
| CCOLA-E 10-02..10-20 | ekran | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| CCOLA-E 10-02..10-20 | V_BIST | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| ENJSA-T 07-10..08-14 | ekran | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| ENJSA-T 07-10..08-14 | V_BIST | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| FENER-A 12-03..12-16 | ekran | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.70, %19.1, %-20.9, 0.53, 0.02, %-79 (2025-12-05) |
| FENER-A 12-03..12-16 | V_BIST | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.73, %20.9, %-23.3, 0.75, 0.06, %-32 (2025-12-10) |
| CCOLA-T 07-29..08-29 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.61, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| CCOLA-T 07-29..08-29 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.67, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| ENJSA-O 01-20..02-14 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-O 01-20..02-14 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-A 12-30..01-27 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |
| ENJSA-A 12-30..01-27 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |

## Orta nokta (p 15, k_m 0,75, bant 8/6, bb 0,20, 'p') tablosu (kıyas)

| örnek | kaynak | beklenen | S5 sonucu | (a) mum | (b) öbek | (c) eğim | (d) aşağı açılış | (e) BB | (f) uzunluk | (a-f) hep | DİP | YOL | tutar | en iyi gün ölçüleri (mum/ATR, öbek, eğim, BB yüzdelik, konum120, 120 gün tepeden) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FENER-E 10-14..11-07 | ekran | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %3.8, %+2.2, 0.16, 0.01, %-83 (2025-10-31) |
| FENER-E 10-14..11-07 | V_BIST | SEÇ DIP | S5 2025-10-31 (DIP), 6 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.69, %3.8, %+2.2, 0.16, 0.12, %-30 (2025-10-31) |
| CCOLA-E 10-02..10-20 | ekran | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| CCOLA-E 10-02..10-20 | V_BIST | SEÇ DIP | S5 2025-10-02 (DIP), 10 gün | E | E | E | E | E | E | E | E | - | TUTTU | 0.62, %5.4, %-1.7, 0.08, 0.2, %-15 (2025-10-02) |
| ENJSA-T 07-10..08-14 | ekran | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| ENJSA-T 07-10..08-14 | V_BIST | SEÇ YOL | S5 2025-08-06 (YOL), 5 gün | E | E | E | E | E | E | E | - | E | TUTTU | 0.65, %4.2, %+0.6, 0.17, 0.93, %-2 (2025-08-06) |
| FENER-A 12-03..12-16 | ekran | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.70, %19.1, %-20.9, 0.53, 0.02, %-79 (2025-12-05) |
| FENER-A 12-03..12-16 | V_BIST | SEÇME | S5 yok | E | - | - | E | - | E | - | E | - | TUTTU | 0.73, %20.9, %-23.3, 0.75, 0.06, %-32 (2025-12-10) |
| CCOLA-T 07-29..08-29 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.61, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| CCOLA-T 07-29..08-29 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | - | TUTTU | 0.67, %5.5, %+1.3, 0.05, 0.28, %-15 (2025-07-29) |
| ENJSA-O 01-20..02-14 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-O 01-20..02-14 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | E | - | E | TUTTU | 0.69, %3.7, %-0.6, 0.02, 0.82, %-3 (2025-02-14) |
| ENJSA-A 12-30..01-27 | ekran | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |
| ENJSA-A 12-30..01-27 | V_BIST | SEÇME | S5 yok | E | E | E | E | E | E | - | - | E | TUTTU | 0.75, %6.5, %+7.1, 0.2, 1.0, %+0 (2026-01-09) |

## Bütün ızgara (tutan / 14; kaçan sınamalar)

| p | k_m | bant (BIST/ABD) | bb | uzunluk | tutan | orta farkı | kaçan |
|---|---|---|---|---|---|---|---|
| 15 | 0.65 | 0.08/0.06 | 0.15 | p | 12 | 2 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.08/0.06 | 0.15 | 10 | 8 | 3 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.08/0.06 | 0.2 | p | 12 | 1 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.08/0.06 | 0.2 | 10 | 8 | 2 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.08/0.06 | 0.25 | p | 12 | 2 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.08/0.06 | 0.25 | 10 | 8 | 3 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.15 | p | 12 | 3 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.15 | 10 | 8 | 4 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.2 | p | 12 | 2 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.2 | 10 | 8 | 3 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.25 | p | 12 | 3 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 15 | 0.65 | 0.10/0.08 | 0.25 | 10 | 8 | 4 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.08/0.06 | 0.15 | p | 14 | 1 | - |
| 15 | 0.75 | 0.08/0.06 | 0.15 | 10 | 10 | 2 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.08/0.06 | 0.2 | p | 14 | 0 | - |
| 15 | 0.75 | 0.08/0.06 | 0.2 | 10 | 10 | 1 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.08/0.06 | 0.25 | p | 14 | 1 | - |
| 15 | 0.75 | 0.08/0.06 | 0.25 | 10 | 10 | 2 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.10/0.08 | 0.15 | p | 14 | 2 | - |
| 15 | 0.75 | 0.10/0.08 | 0.15 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.10/0.08 | 0.2 | p | 14 | 1 | - |
| 15 | 0.75 | 0.10/0.08 | 0.2 | 10 | 10 | 2 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.75 | 0.10/0.08 | 0.25 | p | 14 | 2 | - |
| 15 | 0.75 | 0.10/0.08 | 0.25 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.08/0.06 | 0.15 | p | 14 | 2 | - |
| 15 | 0.85 | 0.08/0.06 | 0.15 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.08/0.06 | 0.2 | p | 12 | 1 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 15 | 0.85 | 0.08/0.06 | 0.2 | 10 | 10 | 2 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.08/0.06 | 0.25 | p | 12 | 2 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 15 | 0.85 | 0.08/0.06 | 0.25 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.10/0.08 | 0.15 | p | 14 | 3 | - |
| 15 | 0.85 | 0.10/0.08 | 0.15 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.10/0.08 | 0.2 | p | 12 | 2 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 15 | 0.85 | 0.10/0.08 | 0.2 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 15 | 0.85 | 0.10/0.08 | 0.25 | p | 12 | 3 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 15 | 0.85 | 0.10/0.08 | 0.25 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.15 | p | 12 | 3 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.15 | 10 | 8 | 4 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.2 | p | 12 | 2 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.2 | 10 | 8 | 3 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.25 | p | 12 | 3 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.08/0.06 | 0.25 | 10 | 8 | 4 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.15 | p | 12 | 4 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.15 | 10 | 8 | 5 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.2 | p | 12 | 3 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.2 | 10 | 8 | 4 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.25 | p | 12 | 4 | ENJSA-T|ekran, ENJSA-T|V_BIST |
| 20 | 0.65 | 0.10/0.08 | 0.25 | 10 | 8 | 5 | FENER-E|ekran, CCOLA-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, CCOLA-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.08/0.06 | 0.15 | p | 14 | 2 | - |
| 20 | 0.75 | 0.08/0.06 | 0.15 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.08/0.06 | 0.2 | p | 14 | 1 | - |
| 20 | 0.75 | 0.08/0.06 | 0.2 | 10 | 10 | 2 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.08/0.06 | 0.25 | p | 14 | 2 | - |
| 20 | 0.75 | 0.08/0.06 | 0.25 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.10/0.08 | 0.15 | p | 14 | 3 | - |
| 20 | 0.75 | 0.10/0.08 | 0.15 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.10/0.08 | 0.2 | p | 14 | 2 | - |
| 20 | 0.75 | 0.10/0.08 | 0.2 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.75 | 0.10/0.08 | 0.25 | p | 14 | 3 | - |
| 20 | 0.75 | 0.10/0.08 | 0.25 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.08/0.06 | 0.15 | p | 14 | 3 | - |
| 20 | 0.85 | 0.08/0.06 | 0.15 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.08/0.06 | 0.2 | p | 12 | 2 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 20 | 0.85 | 0.08/0.06 | 0.2 | 10 | 10 | 3 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.08/0.06 | 0.25 | p | 12 | 3 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 20 | 0.85 | 0.08/0.06 | 0.25 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.10/0.08 | 0.15 | p | 14 | 4 | - |
| 20 | 0.85 | 0.10/0.08 | 0.15 | 10 | 10 | 5 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.10/0.08 | 0.2 | p | 12 | 3 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 20 | 0.85 | 0.10/0.08 | 0.2 | 10 | 10 | 4 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |
| 20 | 0.85 | 0.10/0.08 | 0.25 | p | 12 | 4 | ENJSA-A|ekran, ENJSA-A|V_BIST |
| 20 | 0.85 | 0.10/0.08 | 0.25 | 10 | 10 | 5 | FENER-E|ekran, ENJSA-T|ekran, FENER-E|V_BIST, ENJSA-T|V_BIST |

Not: tasarım 7 örneğe göre ayarlandı (aşırı uyum riski): ızgara kaba ve önceden yazılı; ölçüm başka hisse / pazar / dönemlerde ileri sınamadır.
