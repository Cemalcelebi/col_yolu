# FITIL_V2 — RAPOR (S+ v2 'TAM GİRİLİR', ORTAK CETVEL v1.0)

Ön kayıt yazım 2026-11-17 07:48:43 UTC (sha cc02f7fa3459…; git 04bbf174d5); iş tanımı git 22d7e502c4; koşu 2026-11-17 08:00:01 UTC; süre 684.6 sn. Geleceğe bakma denetimi: ABD 40 TAM günü TUTTU, AVR 40 TAM günü TUTTU, BIST 40 TAM günü TUTTU.

## ÖZET

- TAM GİRİLİR VE bağlam DİP [ANA] (Cemal: 'dipte risk alınır, stop bellidir'): KARAR **ÖLÇÜLEMEDİ**; olasılık etiketi YOK.
  - ABD 2023: n 47, eş farkı -1,7% [-9,0%, +2,9%] -> ÖLÇÜLEMEDİ; ABD 2024-26: n 187, eş farkı +1,1% [-4,3%, +5,4%] -> ÖLÇÜLEMEDİ; AVR 2023: n 34, eş farkı -3,8% [-8,6%, +0,9%] -> ÖLÇÜLEMEDİ; AVR 2024-26: n 132, eş farkı -1,8% [-5,2%, +1,4%] -> ÖLÇÜLEMEDİ; BIST 2023: n 101, eş farkı -4,1% [-9,8%, +3,1%] -> ÖLÇÜLEMEDİ; BIST 2024-26: n 387, eş farkı +2,2% [-2,5%, +9,3%] -> ÖLÇÜLEMEDİ
- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı momentum x likidite kovasındaki öteki hisselerin ortalaması. Hayatta kalma: evren bugün işlem görenler; getiriler yukarı, -%50 olasılığı aşağı yanlı. Komisyon yok.

## TANIM ve eşikler

- Seçilen nokta: N30: şekil S+ (ASIM >= 0,20, ALTYOK >= 0,50), düz kapalı, hatTol 0,02, düşüş >= 0,2, yol <= 0,1.
- BAĞLAM: EK (Cemal, 17 Kas; ön kayıttan önce, sonuç görülmeden): KONUM = (C_t - min(Low, t dahil 250 geçerli bar)) / (max(High, 250) - min(Low, 250)); DİP = KONUM <= 0,25 VE C_t <= max(Close, 120 geçerli bar) x (1 - 0,15); TEPE = KONUM >= 0,75; ORTA = ikisi de değil (yolun ortası); 250 bar yoksa TANIMSIZ (hiçbir sınıfa girmez). Eşikler sabit, ızgaraya girmez.
- (1) şekil: ŞEKİL: ASIM >= a VE ALTYOK >= b.
- (2) savunma hattı: SAVUNMA HATTI: HAT = min(Low, W); düz = (max(Low, W) - HAT) / medyan(R, W) <= duz (kapalı ise şart yok); sağlam = min(Close, W) >= HAT x (1 - tol) (tanım gereği doğru) VE HAT >= min(Low, W'den önceki 30 geçerli bar) x (1 - tol) VE C_t >= HAT.
- (3) dönüm: DÖNÜM: 1 - C_t / max(Close, W'den önceki 60 geçerli bar) >= dusus.
- (4) yol almamış: YOL ALMAMIŞ: C_t <= HAT x (1 + yol) VE C_t <= max(High, W \ {t}) (t HARİÇ önceki 9 pencere barının en yüksek High'ı: bugün pencere tepesini kapanışla kırmamış; SAPMA-1, ana model kararı 17 Kas).
- (5) tepede değil: TEPEDE DEĞİL: C_t <= max(Close, t dahil son 120 geçerli bar) x (1 - 0,15).
- TAM GİRİLİR = (1) VE (2) VE (3) VE (4) VE (5); tanımsız ölçü (yetersiz geçmiş) = şart tutmaz.

## TASARIM sonucu

TASARIM.md (etiket x şart tablosu, 72 noktalı ızgara).

## OLAY SAYIMI (cetvel düşmeleri)

| Satır | Pazar | girdi (durum günü) | havuz dışı | tekil düşen | r60 ölçülemedi | eş < 3 |
|---|---|---|---|---|---|---|
| TAM_DIP | ABD | 3618 | 2399 | 676 | 25 | 0 |
| TAM_DIP | AVR | 1697 | 787 | 584 | 3 | 0 |
| TAM_DIP | BIST | 4331 | 584 | 2845 | 96 | 0 |
| TAM | ABD | 5586 | 3606 | 1089 | 59 | 0 |
| TAM | AVR | 2517 | 1160 | 892 | 6 | 0 |
| TAM | BIST | 11104 | 1247 | 7618 | 139 | 0 |
| TAM_ORTA | ABD | 1511 | 853 | 324 | 34 | 0 |
| TAM_ORTA | AVR | 704 | 304 | 249 | 4 | 0 |
| TAM_ORTA | BIST | 6023 | 628 | 4052 | 59 | 0 |
| TAM_TEPE | ABD | 2 | 0 | 1 | 0 | 0 |
| TAM_TEPE | BIST | 1 | 0 | 0 | 0 | 0 |
| S1 | ABD | 52813 | 24339 | 20447 | 377 | 0 |
| S1 | AVR | 64142 | 30780 | 26955 | 146 | 0 |
| S1 | BIST | 76536 | 9622 | 59275 | 293 | 1 |
| S12 | ABD | 41726 | 18213 | 16433 | 338 | 0 |
| S12 | AVR | 53320 | 25583 | 21902 | 143 | 0 |
| S12 | BIST | 60691 | 6286 | 47386 | 244 | 0 |
| S123 | ABD | 8340 | 5618 | 1600 | 68 | 0 |
| S123 | AVR | 2973 | 1414 | 1038 | 7 | 0 |
| S123 | BIST | 13390 | 1501 | 9417 | 142 | 0 |
| SM_TEPE | ABD | 19595 | 3813 | 11603 | 46 | 0 |
| SM_TEPE | AVR | 30450 | 11633 | 15318 | 102 | 0 |
| SM_TEPE | BIST | 10840 | 4481 | 5187 | 26 | 0 |

## HÜCRE TABLOSU (r60 eşli fark; şart: n / fark+aralık / sıra / portföy / iki yarı; E = tuttu, h = tutmadı)

| Satır | Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / p90 / p10 | yarı1 / yarı2 | şart (beklenen yön) | güç (δ 5) | durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TAM_DIP | ABD | 2016-22 | b | 283 | +0,2% [-1,9%, +2,2%] | -2,5% | 0,50 | +30% / p90 +81% / p10 -12% | +1,4% / -0,9% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | ABD | 2023 | K | 47 | -1,7% [-9,0%, +2,9%] | -0,0% | 0,49 | -0% / p90 +28% / p10 -5% | -1,9% / -1,5% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| TAM_DIP | ABD | 2024-26 | K | 187 | +1,1% [-4,3%, +5,4%] | -2,2% | 0,51 | -0% / p90 +64% / p10 -17% | +2,7% / -0,4% | EhEhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR | 2016-22 | b | 156 | -0,6% [-3,5%, +2,2%] | +0,6% | 0,49 | +20% / p90 +44% / p10 -4% | -0,5% / -0,7% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR | 2023 | K | 34 | -3,8% [-8,6%, +0,9%] | +0,2% | 0,47 | -14% / p90 +11% / p10 -7% | -7,9% / +0,2% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR | 2024-26 | K | 132 | -1,8% [-5,2%, +1,4%] | -0,8% | 0,47 | -11% / p90 +39% / p10 -1% | -0,3% / -3,3% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST | 2016-22 | b | 296 | -1,9% [-5,7%, +2,0%] | -4,3% | 0,48 | +115% / p90 +414% / p10 +142% | -5,0% / +1,3% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST | 2023 | b | 101 | -4,1% [-9,8%, +3,1%] | -9,9% | 0,44 | +65% / p90 +128% / p10 +67% | -6,3% / -1,9% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST | 2024-26 | b | 387 | +2,2% [-2,5%, +9,3%] | -5,7% | 0,49 | +97% / p90 +102% / p10 -7% | +1,1% / +3,3% | EhhhE | 52% | ÖLÇÜLEMEDİ |
| TAM | ABD | 2016-22 | b | 442 | -0,2% [-2,3%, +1,8%] | -2,3% | 0,49 | +27% / p90 +229% / p10 +32% | +1,2% / -1,6% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM | ABD | 2023 | K | 76 | -1,0% [-6,1%, +2,8%] | +0,1% | 0,50 | +2% / p90 +32% / p10 -7% | -1,0% / -0,9% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| TAM | ABD | 2024-26 | K | 306 | +2,2% [-1,5%, +5,7%] | -3,6% | 0,50 | +34% / p90 +95% / p10 -13% | +2,9% / +1,6% | EhhhE | 52% | ÖLÇÜLEMEDİ |
| TAM | AVR | 2016-22 | b | 242 | -1,7% [-3,7%, +0,6%] | -0,9% | 0,47 | +3% / p90 +69% / p10 +9% | -1,4% / -1,9% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM | AVR | 2023 | K | 43 | -3,7% [-9,1%, +1,4%] | -0,4% | 0,46 | -15% / p90 +10% / p10 -9% | -9,1% / +1,5% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| TAM | AVR | 2024-26 | K | 166 | -0,9% [-4,4%, +2,2%] | +0,3% | 0,49 | -3% / p90 +34% / p10 -7% | +1,3% / -3,1% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM | BIST | 2016-22 | b | 831 | -1,2% [-4,0%, +1,8%] | -4,8% | 0,48 | +649% / p90 +2287% / p10 +492% | -0,2% / -2,2% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM | BIST | 2023 | b | 350 | -0,5% [-4,8%, +3,9%] | -5,0% | 0,48 | -7% / p90 +51% / p10 -6% | +2,0% / -2,9% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM | BIST | 2024-26 | b | 881 | -1,6% [-4,5%, +2,1%] | -7,0% | 0,47 | +150% / p90 +224% / p10 +33% | -2,3% / -0,8% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM_ORTA | ABD | 2016-22 | b | 140 | -0,3% [-4,3%, +4,3%] | -0,1% | 0,50 | +69% / p90 +167% / p10 +47% | +0,5% / -1,1% | EhEhh | 29% | ÖLÇÜLEMEDİ |
| TAM_ORTA | ABD | 2023 | K | 32 | +3,1% [-5,0%, +9,3%] | +1,4% | 0,54 | +13% / p90 +21% / p10 -5% | +0,8% / +5,5% | EhEhE | 10% | ÖLÇÜLEMEDİ |
| TAM_ORTA | ABD | 2024-26 | K | 128 | +3,5% [-5,2%, +12,1%] | -4,0% | 0,49 | +46% / p90 +110% / p10 -2% | +3,6% / +3,3% | EhhhE | 29% | ÖLÇÜLEMEDİ |
| TAM_ORTA | AVR | 2016-22 | b | 96 | -2,1% [-4,4%, +0,5%] | -1,9% | 0,47 | +12% / p90 +42% / p10 +7% | -2,0% / -2,2% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| TAM_ORTA | AVR | 2023 | K | 11 | -6,8% [-20,7%, +4,0%] | -2,1% | 0,39 | -7% / p90 +7% / p10 -4% | -14,4% / -0,4% | hhhhh | 0% | ÖLÇÜLEMEDİ |
| TAM_ORTA | AVR | 2024-26 | K | 40 | -0,3% [-6,4%, +5,6%] | +4,0% | 0,52 | +4% / p90 +21% / p10 -6% | -0,3% / -0,3% | EhEhh | 10% | ÖLÇÜLEMEDİ |
| TAM_ORTA | BIST | 2016-22 | b | 499 | -1,0% [-5,3%, +3,7%] | -5,2% | 0,48 | +1287% / p90 +2078% / p10 +517% | +5,9% / -7,8% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM_ORTA | BIST | 2023 | b | 260 | +0,1% [-6,9%, +7,3%] | -4,8% | 0,49 | -5% / p90 +56% / p10 +1% | +3,7% / -3,4% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| TAM_ORTA | BIST | 2024-26 | b | 519 | -5,5% [-8,1%, -2,5%] | -9,4% | 0,45 | +9% / p90 +269% / p10 +31% | -4,8% / -6,1% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| TAM_TEPE | ABD | 2016-22 | b | 0 | - | - | - | - | - | - | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | ABD | 2023 | K | 0 | - | - | - | - | - | - | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | ABD | 2024-26 | K | 1 | +122,5% [+122,5%, +122,5%] | +122,5% | 1,00 | +12% / p90 +4% / p10 -3% | - / +122,5% | hEEEh | 0% | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2016-22 | b | 1 | -40,7% [-40,7%, -40,7%] | -40,7% | 0,00 | -3% / p90 +2% / p10 -1% | - / -40,7% | hhhhh | 0% | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2023 | b | 0 | - | - | - | - | - | - | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2024-26 | b | 0 | - | - | - | - | - | - | - | ÖLÇÜLEMEDİ |
| S1 | ABD | 2016-22 | b | 4367 | -0,2% [-1,1%, +0,6%] | -1,0% | 0,50 | +159% / p90 +282% / p10 +48% | -0,3% / -0,2% | Ehhhh | 60% | TUTMADI |
| S1 | ABD | 2023 | K | 889 | +0,2% [-1,1%, +1,3%] | -0,8% | 0,50 | +32% / p90 +32% / p10 -1% | +0,3% / +0,1% | EhhEE | 52% | ÖLÇÜLEMEDİ |
| S1 | ABD | 2024-26 | K | 2180 | +0,3% [-1,1%, +1,7%] | -1,7% | 0,50 | +54% / p90 +104% / p10 +2% | -0,2% / +0,8% | EhEhh | 65% | TUTMADI |
| S1 | AVR | 2016-22 | b | 3485 | -0,3% [-0,8%, +0,2%] | -0,5% | 0,50 | +23% / p90 +115% / p10 +18% | +0,1% / -0,7% | Ehhhh | 60% | TUTMADI |
| S1 | AVR | 2023 | K | 649 | +0,1% [-0,8%, +0,8%] | +0,3% | 0,51 | -8% / p90 +19% / p10 -2% | +0,1% / +0,1% | EhEhE | 52% | ÖLÇÜLEMEDİ |
| S1 | AVR | 2024-26 | K | 1734 | -0,2% [-1,0%, +0,6%] | -0,5% | 0,49 | +26% / p90 +56% / p10 +9% | -0,3% / -0,2% | Ehhhh | 65% | TUTMADI |
| S1 | BIST | 2016-22 | b | 3725 | -0,1% [-1,2%, +1,1%] | -4,6% | 0,50 | +1395% / p90 +4019% / p10 +723% | -0,0% / -0,1% | Ehhhh | 60% | TUTMADI |
| S1 | BIST | 2023 | b | 719 | -0,5% [-2,2%, +1,2%] | -7,0% | 0,49 | +87% / p90 +110% / p10 +19% | -0,3% / -0,8% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| S1 | BIST | 2024-26 | b | 2597 | -0,8% [-2,1%, +0,6%] | -6,5% | 0,49 | +88% / p90 +230% / p10 +41% | -1,8% / +0,3% | Ehhhh | 65% | TUTMADI |
| S12 | ABD | 2016-22 | b | 3838 | -0,4% [-1,5%, +0,5%] | -1,0% | 0,50 | +93% / p90 +295% / p10 +61% | -0,3% / -0,6% | Ehhhh | 60% | TUTMADI |
| S12 | ABD | 2023 | K | 764 | +0,4% [-0,9%, +1,6%] | -0,6% | 0,50 | +12% / p90 +37% / p10 -2% | +0,6% / +0,1% | EhEhE | 52% | ÖLÇÜLEMEDİ |
| S12 | ABD | 2024-26 | K | 1953 | -0,1% [-1,5%, +1,2%] | -2,0% | 0,50 | +28% / p90 +99% / p10 +6% | -0,4% / +0,2% | Ehhhh | 65% | TUTMADI |
| S12 | AVR | 2016-22 | b | 3167 | -0,2% [-0,6%, +0,3%] | -0,5% | 0,50 | +23% / p90 +77% / p10 -7% | +0,2% / -0,6% | Ehhhh | 60% | TUTMADI |
| S12 | AVR | 2023 | K | 595 | -0,4% [-1,5%, +0,7%] | -0,3% | 0,50 | -12% / p90 +22% / p10 -1% | -0,7% / +0,0% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| S12 | AVR | 2024-26 | K | 1592 | -0,2% [-0,9%, +0,5%] | -0,4% | 0,49 | +10% / p90 +54% / p10 +6% | -0,1% / -0,4% | Ehhhh | 65% | TUTMADI |
| S12 | BIST | 2016-22 | b | 3501 | -0,0% [-1,2%, +1,1%] | -4,7% | 0,50 | +1209% / p90 +3242% / p10 +812% | +0,3% / -0,4% | Ehhhh | 60% | TUTMADI |
| S12 | BIST | 2023 | b | 665 | -0,3% [-2,2%, +1,8%] | -7,2% | 0,48 | +160% / p90 +95% / p10 +12% | +0,0% / -0,6% | EhhEh | 52% | ÖLÇÜLEMEDİ |
| S12 | BIST | 2024-26 | b | 2347 | -0,6% [-2,1%, +0,9%] | -6,3% | 0,49 | +284% / p90 +212% / p10 +25% | -1,6% / +0,4% | EhhEh | 65% | TUTMADI |
| S123 | ABD | 2016-22 | b | 549 | -1,0% [-3,0%, +1,1%] | -2,8% | 0,48 | -38% / p90 +187% / p10 -2% | -0,3% / -1,6% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| S123 | ABD | 2023 | K | 98 | -1,2% [-6,3%, +2,4%] | -0,1% | 0,50 | -6% / p90 +22% / p10 -13% | -1,1% / -1,3% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| S123 | ABD | 2024-26 | K | 369 | +3,0% [-1,0%, +7,2%] | -3,3% | 0,51 | +31% / p90 +113% / p10 -0% | +4,1% / +1,9% | EhEhE | 52% | ÖLÇÜLEMEDİ |
| S123 | AVR | 2016-22 | b | 276 | -1,7% [-3,7%, +0,4%] | -1,5% | 0,47 | -8% / p90 +79% / p10 +7% | -1,3% / -2,1% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| S123 | AVR | 2023 | K | 50 | -1,0% [-7,4%, +4,9%] | +0,2% | 0,47 | -8% / p90 +13% / p10 -9% | -7,4% / +5,5% | Ehhhh | 10% | ÖLÇÜLEMEDİ |
| S123 | AVR | 2024-26 | K | 178 | -0,7% [-3,8%, +2,0%] | +0,3% | 0,49 | +1% / p90 +36% / p10 -4% | +1,5% / -3,0% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| S123 | BIST | 2016-22 | b | 920 | -1,6% [-3,9%, +0,7%] | -4,6% | 0,48 | +495% / p90 +2983% / p10 +569% | -0,1% / -3,1% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| S123 | BIST | 2023 | b | 378 | -0,3% [-4,5%, +3,8%] | -5,3% | 0,48 | -9% / p90 +46% / p10 -7% | +0,5% / -1,1% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| S123 | BIST | 2024-26 | b | 951 | -1,5% [-4,4%, +1,8%] | -7,2% | 0,47 | +93% / p90 +177% / p10 +19% | -2,3% / -0,8% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| SM_TEPE | ABD | 2016-22 | b | 2810 | +0,3% [-0,4%, +1,0%] | -0,5% | 0,50 | +135% / p90 +215% / p10 +30% | +0,3% / +0,3% | Ehhhh | 65% | TUTMADI |
| SM_TEPE | ABD | 2023 | K | 230 | -0,2% [-2,1%, +1,9%] | -0,2% | 0,51 | +13% / p90 +30% / p10 -4% | +0,8% / -1,2% | Ehhhh | 29% | ÖLÇÜLEMEDİ |
| SM_TEPE | ABD | 2024-26 | K | 1092 | -0,5% [-2,4%, +1,3%] | -2,4% | 0,51 | +83% / p90 +121% / p10 +12% | +1,0% / -2,0% | Ehhhh | 65% | TUTMADI |
| SM_TEPE | AVR | 2016-22 | b | 2200 | +0,3% [-0,2%, +0,8%] | +0,2% | 0,51 | +21% / p90 +93% / p10 +8% | +0,3% / +0,3% | Ehhhh | 65% | TUTMADI |
| SM_TEPE | AVR | 2023 | K | 266 | +0,4% [-1,8%, +2,5%] | -0,2% | 0,50 | -1% / p90 +16% / p10 -5% | +0,9% / -0,1% | EhEhh | 29% | ÖLÇÜLEMEDİ |
| SM_TEPE | AVR | 2024-26 | K | 913 | +0,6% [-0,2%, +1,6%] | +0,4% | 0,51 | +22% / p90 +49% / p10 +8% | +0,8% / +0,4% | Ehhhh | 52% | ÖLÇÜLEMEDİ |
| SM_TEPE | BIST | 2016-22 | b | 730 | -1,9% [-6,3%, +2,8%] | -7,3% | 0,47 | +3359% / p90 +3514% / p10 +764% | -0,8% / -3,0% | EhEhE | 52% | ÖLÇÜLEMEDİ |
| SM_TEPE | BIST | 2023 | b | 123 | +0,5% [-9,4%, +10,1%] | -5,9% | 0,50 | +113% / p90 +156% / p10 +33% | -1,3% / +2,3% | EhEhh | 29% | ÖLÇÜLEMEDİ |
| SM_TEPE | BIST | 2024-26 | b | 276 | +6,1% [+0,1%, +12,9%] | -4,0% | 0,53 | +473% / p90 +286% / p10 +31% | +5,5% / +6,8% | Ehhhh | 29% | ÖLÇÜLEMEDİ |

## OLASILIK TABLOSU (250 gün dokunma; eş katı karar, taban katı bilgi)

| Satır | Pazar | Dönem | n250 | P(+%100) olay / eş | kat eş [%95] | kat taban | P(-%50) olay / eş | kat eş [%95] | kat taban | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| TAM_DIP | ABD | 2016-22 | 283 | +9,9% / +9,0% | 1,09 [0,78, 1,49] | 1,58 | +25,4% / +20,7% | 1,23 [1,05, 1,44] | 1,90 | YOK |
| TAM_DIP | ABD | 2023 | 47 | +12,8% / +14,6% | 0,88 [0,00, 1,81] | 1,10 | +17,0% / +10,1% | 1,68 [0,64, 3,04] | 2,62 | YOK |
| TAM_DIP | ABD | 2024-26 | 104 | +26,0% / +17,7% | 1,47 [0,97, 1,95] | 2,08 | +18,3% / +19,3% | 0,95 [0,53, 1,38] | 1,43 | YOK |
| TAM_DIP | AVR | 2016-22 | 156 | +5,1% / +5,2% | 0,99 [0,27, 1,75] | 1,73 | +17,3% / +10,9% | 1,59 [1,05, 2,29] | 2,59 | YOK |
| TAM_DIP | AVR | 2023 | 34 | +2,9% / +1,3% | 2,20 [0,00, 6,31] | 2,23 | +20,6% / +9,0% | 2,29 [0,97, 3,87] | 5,01 | YOK |
| TAM_DIP | AVR | 2024-26 | 91 | +3,3% / +3,8% | 0,88 [0,00, 2,56] | 1,11 | +16,5% / +8,0% | 2,06 [1,19, 2,88] | 3,93 | YOK |
| TAM_DIP | BIST | 2016-22 | 296 | +31,8% / +36,1% | 0,88 [0,70, 1,02] | 0,83 | +5,4% / +4,1% | 1,31 [0,72, 2,25] | 0,98 | YOK |
| TAM_DIP | BIST | 2023 | 101 | +66,3% / +64,9% | 1,02 [0,72, 1,10] | 1,04 | +1,0% / +1,5% | 0,68 [0,00, 2,97] | 0,35 | YOK |
| TAM_DIP | BIST | 2024-26 | 236 | +24,2% / +23,0% | 1,05 [0,88, 1,26] | 0,94 | +1,7% / +4,0% | 0,43 [0,13, 0,71] | 0,33 | YOK |
| TAM | ABD | 2016-22 | 442 | +11,8% / +9,7% | 1,22 [0,96, 1,56] | 1,68 | +26,5% / +19,5% | 1,36 [1,17, 1,59] | 2,01 | YOK |
| TAM | ABD | 2023 | 76 | +19,7% / +12,6% | 1,56 [0,68, 2,89] | 1,78 | +18,4% / +10,5% | 1,76 [1,04, 2,56] | 2,72 | YOK |
| TAM | ABD | 2024-26 | 175 | +28,0% / +17,2% | 1,63 [1,29, 2,06] | 2,25 | +22,3% / +18,8% | 1,19 [0,75, 1,56] | 1,71 | YOK |
| TAM | AVR | 2016-22 | 242 | +5,0% / +6,3% | 0,79 [0,33, 1,41] | 1,19 | +14,9% / +9,7% | 1,53 [1,02, 2,18] | 2,38 | YOK |
| TAM | AVR | 2023 | 43 | +4,7% / +1,2% | 3,88 [0,00, 13,66] | 3,62 | +18,6% / +8,9% | 2,10 [0,87, 3,55] | 4,45 | YOK |
| TAM | AVR | 2024-26 | 118 | +5,1% / +3,7% | 1,38 [0,42, 2,82] | 1,73 | +16,1% / +7,7% | 2,09 [1,41, 2,78] | 3,87 | YOK |
| TAM | BIST | 2016-22 | 832 | +32,2% / +35,3% | 0,91 [0,81, 1,00] | 0,87 | +7,8% / +6,1% | 1,28 [0,99, 1,64] | 1,27 | YOK |
| TAM | BIST | 2023 | 350 | +51,7% / +51,8% | 1,00 [0,93, 1,08] | 0,99 | +4,0% / +4,0% | 0,99 [0,39, 1,74] | 0,84 | YOK |
| TAM | BIST | 2024-26 | 538 | +21,4% / +21,8% | 0,98 [0,84, 1,14] | 0,93 | +6,3% / +6,0% | 1,06 [0,81, 1,36] | 1,00 | YOK |
| TAM_ORTA | ABD | 2016-22 | 140 | +15,0% / +11,5% | 1,30 [0,86, 1,91] | 1,63 | +26,4% / +18,5% | 1,43 [1,07, 1,85] | 1,94 | YOK |
| TAM_ORTA | ABD | 2023 | 32 | +31,2% / +9,4% | 3,33 [1,84, 4,94] | 2,88 | +15,6% / +9,9% | 1,57 [0,63, 3,75] | 2,29 | YOK |
| TAM_ORTA | ABD | 2024-26 | 75 | +30,7% / +16,3% | 1,88 [1,35, 2,61] | 2,46 | +26,7% / +18,4% | 1,45 [0,84, 2,01] | 1,99 | YOK |
| TAM_ORTA | AVR | 2016-22 | 96 | +5,2% / +8,3% | 0,63 [0,18, 1,69] | 0,83 | +7,3% / +6,9% | 1,06 [0,44, 1,95] | 1,44 | YOK |
| TAM_ORTA | AVR | 2023 | 11 | +9,1% / +0,6% | 16,26 [0,00, 74,00] | 8,15 | +18,2% / +7,8% | 2,33 [0,00, 7,59] | 4,09 | ÖLÇÜLEMEDİ |
| TAM_ORTA | AVR | 2024-26 | 31 | +9,7% / +3,2% | 3,00 [0,00, 7,24] | 3,41 | +12,9% / +6,7% | 1,92 [0,00, 4,48] | 3,23 | YOK |
| TAM_ORTA | BIST | 2016-22 | 500 | +32,8% / +35,4% | 0,93 [0,81, 1,05] | 0,90 | +8,8% / +7,4% | 1,18 [0,87, 1,62] | 1,27 | YOK |
| TAM_ORTA | BIST | 2023 | 260 | +50,0% / +49,9% | 1,00 [0,91, 1,14] | 0,98 | +4,2% / +4,4% | 0,96 [0,39, 1,71] | 0,82 | YOK |
| TAM_ORTA | BIST | 2024-26 | 301 | +19,3% / +20,8% | 0,93 [0,71, 1,18] | 0,93 | +9,0% / +7,4% | 1,21 [0,87, 1,56] | 1,24 | YOK |
| TAM_TEPE | ABD | 2016-22 | 0 | - / - | - [-, -] | - | - / - | - [-, -] | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | ABD | 2023 | 0 | - / - | - [-, -] | - | - / - | - [-, -] | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | ABD | 2024-26 | 0 | - / - | - [-, -] | - | - / - | - [-, -] | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2016-22 | 1 | +0,0% / +26,7% | 0,00 [0,00, 0,00] | 0,00 | +100,0% / +20,0% | 5,00 [5,00, 5,00] | 26,45 | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2023 | 0 | - / - | - [-, -] | - | - / - | - [-, -] | - | ÖLÇÜLEMEDİ |
| TAM_TEPE | BIST | 2024-26 | 0 | - / - | - [-, -] | - | - / - | - [-, -] | - | ÖLÇÜLEMEDİ |
| S1 | ABD | 2016-22 | 4367 | +6,5% / +6,9% | 0,93 [0,82, 1,06] | 0,96 | +14,4% / +14,0% | 1,02 [0,93, 1,11] | 1,05 | YOK |
| S1 | ABD | 2023 | 889 | +10,8% / +9,5% | 1,13 [0,99, 1,29] | 1,15 | +7,3% / +7,9% | 0,93 [0,73, 1,20] | 0,94 | YOK |
| S1 | ABD | 2024-26 | 1401 | +12,3% / +12,0% | 1,02 [0,87, 1,18] | 1,04 | +13,6% / +13,5% | 1,01 [0,83, 1,22] | 1,03 | YOK |
| S1 | AVR | 2016-22 | 3485 | +2,4% / +2,6% | 0,90 [0,72, 1,10] | 0,96 | +7,2% / +7,8% | 0,91 [0,78, 1,03] | 0,95 | YOK |
| S1 | AVR | 2023 | 649 | +1,4% / +1,2% | 1,14 [0,40, 1,91] | 1,12 | +4,5% / +4,4% | 1,01 [0,80, 1,23] | 1,03 | YOK |
| S1 | AVR | 2024-26 | 1256 | +2,6% / +2,7% | 0,98 [0,68, 1,31] | 0,92 | +4,2% / +4,5% | 0,93 [0,72, 1,18] | 1,00 | YOK |
| S1 | BIST | 2016-22 | 3727 | +39,5% / +40,0% | 0,99 [0,96, 1,02] | 0,98 | +6,6% / +6,5% | 1,02 [0,91, 1,13] | 1,01 | YOK |
| S1 | BIST | 2023 | 719 | +45,5% / +48,1% | 0,95 [0,85, 1,00] | 0,95 | +4,5% / +4,9% | 0,92 [0,75, 1,11] | 0,90 | YOK |
| S1 | BIST | 2024-26 | 1720 | +22,0% / +21,9% | 1,00 [0,92, 1,09] | 0,98 | +5,8% / +6,1% | 0,96 [0,85, 1,06] | 0,90 | YOK |
| S12 | ABD | 2016-22 | 3838 | +6,0% / +6,7% | 0,90 [0,79, 1,04] | 0,90 | +13,9% / +13,5% | 1,03 [0,94, 1,12] | 1,00 | YOK |
| S12 | ABD | 2023 | 764 | +9,3% / +9,0% | 1,04 [0,88, 1,23] | 1,02 | +6,9% / +7,7% | 0,90 [0,66, 1,22] | 0,86 | YOK |
| S12 | ABD | 2024-26 | 1266 | +11,4% / +12,0% | 0,95 [0,79, 1,11] | 0,96 | +13,0% / +13,2% | 0,98 [0,80, 1,20] | 0,98 | YOK |
| S12 | AVR | 2016-22 | 3167 | +2,2% / +2,5% | 0,91 [0,71, 1,12] | 0,94 | +7,2% / +7,7% | 0,94 [0,79, 1,07] | 0,96 | YOK |
| S12 | AVR | 2023 | 595 | +1,3% / +1,1% | 1,19 [0,31, 1,94] | 1,12 | +3,9% / +4,4% | 0,88 [0,63, 1,15] | 0,89 | YOK |
| S12 | AVR | 2024-26 | 1157 | +2,7% / +2,6% | 1,02 [0,68, 1,38] | 0,94 | +4,1% / +4,4% | 0,92 [0,69, 1,19] | 0,96 | YOK |
| S12 | BIST | 2016-22 | 3502 | +39,3% / +39,5% | 0,99 [0,96, 1,03] | 0,99 | +6,7% / +6,6% | 1,02 [0,92, 1,13] | 1,02 | YOK |
| S12 | BIST | 2023 | 665 | +45,7% / +48,0% | 0,95 [0,87, 1,00] | 0,96 | +4,4% / +4,9% | 0,88 [0,67, 1,10] | 0,88 | YOK |
| S12 | BIST | 2024-26 | 1549 | +22,4% / +22,1% | 1,01 [0,93, 1,11] | 1,00 | +6,1% / +6,3% | 0,98 [0,87, 1,10] | 0,94 | YOK |
| S123 | ABD | 2016-22 | 549 | +13,3% / +10,8% | 1,23 [1,02, 1,52] | 1,62 | +28,1% / +18,9% | 1,48 [1,29, 1,69] | 2,18 | PİYANGO |
| S123 | ABD | 2023 | 98 | +21,4% / +12,9% | 1,65 [1,01, 2,58] | 1,98 | +20,4% / +11,0% | 1,85 [1,17, 2,59] | 2,95 | PİYANGO |
| S123 | ABD | 2024-26 | 212 | +30,7% / +17,9% | 1,71 [1,45, 2,05] | 2,39 | +22,6% / +18,6% | 1,22 [0,80, 1,58] | 1,76 | YOK |
| S123 | AVR | 2016-22 | 276 | +5,8% / +6,4% | 0,91 [0,32, 1,62] | 1,32 | +15,2% / +9,6% | 1,59 [1,11, 2,18] | 2,52 | YOK |
| S123 | AVR | 2023 | 50 | +8,0% / +1,2% | 6,90 [0,00, 18,17] | 6,32 | +20,0% / +8,8% | 2,27 [1,03, 3,84] | 4,82 | YOK |
| S123 | AVR | 2024-26 | 126 | +5,6% / +3,5% | 1,60 [0,59, 2,94] | 1,88 | +15,9% / +7,6% | 2,10 [1,41, 2,77] | 3,82 | YOK |
| S123 | BIST | 2016-22 | 921 | +33,3% / +35,9% | 0,93 [0,84, 1,01] | 0,89 | +8,6% / +6,3% | 1,36 [1,11, 1,72] | 1,40 | YOK |
| S123 | BIST | 2023 | 378 | +52,1% / +52,2% | 1,00 [0,95, 1,07] | 0,99 | +3,7% / +4,1% | 0,91 [0,46, 1,58] | 0,79 | YOK |
| S123 | BIST | 2024-26 | 590 | +21,2% / +21,1% | 1,01 [0,87, 1,15] | 0,93 | +6,6% / +6,1% | 1,08 [0,87, 1,30] | 1,05 | YOK |
| SM_TEPE | ABD | 2016-22 | 2810 | +4,3% / +6,1% | 0,70 [0,56, 0,86] | 0,67 | +8,0% / +12,1% | 0,66 [0,56, 0,76] | 0,57 | YOK |
| SM_TEPE | ABD | 2023 | 230 | +9,6% / +8,9% | 1,07 [0,84, 1,45] | 1,11 | +8,3% / +7,4% | 1,11 [0,64, 1,67] | 0,97 | YOK |
| SM_TEPE | ABD | 2024-26 | 790 | +9,2% / +12,8% | 0,72 [0,54, 0,94] | 0,74 | +8,2% / +11,5% | 0,71 [0,55, 0,87] | 0,65 | YOK |
| SM_TEPE | AVR | 2016-22 | 2200 | +2,2% / +2,3% | 0,96 [0,71, 1,27] | 1,04 | +5,4% / +8,1% | 0,66 [0,55, 0,75] | 0,60 | YOK |
| SM_TEPE | AVR | 2023 | 266 | +1,5% / +1,3% | 1,12 [0,00, 2,45] | 1,38 | +1,1% / +4,6% | 0,25 [0,00, 0,45] | 0,24 | YOK |
| SM_TEPE | AVR | 2024-26 | 620 | +3,4% / +2,9% | 1,16 [0,69, 1,79] | 1,11 | +3,2% / +3,8% | 0,84 [0,62, 1,12] | 0,74 | YOK |
| SM_TEPE | BIST | 2016-22 | 731 | +37,3% / +43,1% | 0,87 [0,79, 0,94] | 0,93 | +14,0% / +9,6% | 1,45 [1,22, 1,71] | 1,92 | YOK |
| SM_TEPE | BIST | 2023 | 123 | +48,0% / +43,8% | 1,10 [0,90, 1,28] | 1,19 | +11,4% / +11,2% | 1,02 [0,64, 1,74] | 1,41 | YOK |
| SM_TEPE | BIST | 2024-26 | 163 | +33,1% / +28,8% | 1,15 [0,94, 1,37] | 1,54 | +16,0% / +11,0% | 1,44 [0,91, 2,08] | 2,28 | YOK |

## KIRILIM / STOP ORANLARI (tekil olaylar; t+1 .. t+60 geçerli bar, önce hangisi)

| Satır | Pazar | Dönem | n | ölçülen | KIRILIM | STOP | YOK | ÖLÇÜLMEZ | kırılım payı | stop payı |
|---|---|---|---|---|---|---|---|---|---|---|
| TAM_DIP | ABD | 2016-22 | 283 | 283 | 117 | 163 | 3 | 0 | +41% | +58% |
| TAM_DIP | ABD | 2023 | 47 | 47 | 24 | 23 | 0 | 0 | +51% | +49% |
| TAM_DIP | ABD | 2024-26 | 212 | 187 | 73 | 113 | 1 | 25 | +39% | +60% |
| TAM_DIP | AVR |  | 1 | 1 | 0 | 1 | 0 | 0 | +0% | +100% |
| TAM_DIP | AVR | 2016-22 | 156 | 156 | 51 | 104 | 1 | 0 | +33% | +67% |
| TAM_DIP | AVR | 2023 | 34 | 34 | 19 | 15 | 0 | 0 | +56% | +44% |
| TAM_DIP | AVR | 2024-26 | 135 | 132 | 52 | 79 | 1 | 3 | +39% | +60% |
| TAM_DIP | BIST | 2016-22 | 296 | 296 | 126 | 164 | 6 | 0 | +43% | +55% |
| TAM_DIP | BIST | 2023 | 101 | 101 | 26 | 75 | 0 | 0 | +26% | +74% |
| TAM_DIP | BIST | 2024-26 | 483 | 387 | 138 | 243 | 6 | 96 | +36% | +63% |
| TAM | ABD |  | 6 | 6 | 1 | 5 | 0 | 0 | +17% | +83% |
| TAM | ABD | 2016-22 | 442 | 442 | 187 | 249 | 6 | 0 | +42% | +56% |
| TAM | ABD | 2023 | 76 | 76 | 36 | 40 | 0 | 0 | +47% | +53% |
| TAM | ABD | 2024-26 | 365 | 306 | 130 | 175 | 1 | 59 | +42% | +57% |
| TAM | AVR |  | 8 | 8 | 3 | 5 | 0 | 0 | +38% | +62% |
| TAM | AVR | 2016-22 | 242 | 242 | 82 | 158 | 2 | 0 | +34% | +65% |
| TAM | AVR | 2023 | 43 | 43 | 20 | 22 | 1 | 0 | +47% | +51% |
| TAM | AVR | 2024-26 | 172 | 166 | 67 | 98 | 1 | 6 | +40% | +59% |
| TAM | BIST |  | 9 | 9 | 1 | 6 | 2 | 0 | +11% | +67% |
| TAM | BIST | 2016-22 | 832 | 832 | 315 | 491 | 26 | 0 | +38% | +59% |
| TAM | BIST | 2023 | 350 | 350 | 76 | 272 | 2 | 0 | +22% | +78% |
| TAM | BIST | 2024-26 | 1019 | 881 | 298 | 565 | 18 | 138 | +34% | +64% |
| TAM_ORTA | ABD | 2016-22 | 140 | 140 | 65 | 72 | 3 | 0 | +46% | +51% |
| TAM_ORTA | ABD | 2023 | 32 | 32 | 14 | 18 | 0 | 0 | +44% | +56% |
| TAM_ORTA | ABD | 2024-26 | 162 | 128 | 61 | 66 | 1 | 34 | +48% | +52% |
| TAM_ORTA | AVR | 2016-22 | 96 | 96 | 36 | 59 | 1 | 0 | +38% | +61% |
| TAM_ORTA | AVR | 2023 | 11 | 11 | 2 | 8 | 1 | 0 | +18% | +73% |
| TAM_ORTA | AVR | 2024-26 | 44 | 40 | 18 | 22 | 0 | 4 | +45% | +55% |
| TAM_ORTA | BIST | 2016-22 | 500 | 500 | 175 | 309 | 16 | 0 | +35% | +62% |
| TAM_ORTA | BIST | 2023 | 260 | 260 | 50 | 208 | 2 | 0 | +19% | +80% |
| TAM_ORTA | BIST | 2024-26 | 577 | 519 | 161 | 345 | 13 | 58 | +31% | +66% |
| TAM_TEPE | ABD | 2024-26 | 1 | 1 | 1 | 0 | 0 | 0 | +100% | +0% |
| TAM_TEPE | BIST | 2016-22 | 1 | 1 | 0 | 1 | 0 | 0 | +0% | +100% |
| S1 | ABD |  | 133 | 133 | 71 | 57 | 5 | 0 | +53% | +43% |
| S1 | ABD | 2016-22 | 4367 | 4367 | 2698 | 1602 | 67 | 0 | +62% | +37% |
| S1 | ABD | 2023 | 889 | 889 | 485 | 394 | 10 | 0 | +55% | +44% |
| S1 | ABD | 2024-26 | 2557 | 2180 | 1275 | 875 | 30 | 377 | +58% | +40% |
| S1 | AVR |  | 348 | 348 | 182 | 156 | 10 | 0 | +52% | +45% |
| S1 | AVR | 2016-22 | 3485 | 3485 | 2042 | 1374 | 69 | 0 | +59% | +39% |
| S1 | AVR | 2023 | 649 | 649 | 358 | 278 | 13 | 0 | +55% | +43% |
| S1 | AVR | 2024-26 | 1880 | 1733 | 952 | 732 | 49 | 147 | +55% | +42% |
| S1 | BIST |  | 226 | 226 | 136 | 83 | 7 | 0 | +60% | +37% |
| S1 | BIST | 2016-22 | 3728 | 3728 | 2186 | 1398 | 144 | 0 | +59% | +38% |
| S1 | BIST | 2023 | 719 | 719 | 302 | 411 | 6 | 0 | +42% | +57% |
| S1 | BIST | 2024-26 | 2888 | 2597 | 1215 | 1322 | 60 | 291 | +47% | +51% |
| S12 | ABD |  | 116 | 116 | 62 | 51 | 3 | 0 | +53% | +44% |
| S12 | ABD | 2016-22 | 3838 | 3838 | 2460 | 1333 | 45 | 0 | +64% | +35% |
| S12 | ABD | 2023 | 764 | 764 | 459 | 296 | 9 | 0 | +60% | +39% |
| S12 | ABD | 2024-26 | 2291 | 1953 | 1192 | 742 | 19 | 338 | +61% | +38% |
| S12 | AVR |  | 302 | 302 | 162 | 134 | 6 | 0 | +54% | +44% |
| S12 | AVR | 2016-22 | 3167 | 3167 | 1927 | 1194 | 46 | 0 | +61% | +38% |
| S12 | AVR | 2023 | 595 | 595 | 343 | 241 | 11 | 0 | +58% | +41% |
| S12 | AVR | 2024-26 | 1735 | 1591 | 936 | 626 | 29 | 144 | +59% | +39% |
| S12 | BIST |  | 205 | 205 | 124 | 75 | 6 | 0 | +60% | +37% |
| S12 | BIST | 2016-22 | 3502 | 3502 | 2132 | 1247 | 123 | 0 | +61% | +36% |
| S12 | BIST | 2023 | 665 | 665 | 293 | 369 | 3 | 0 | +44% | +55% |
| S12 | BIST | 2024-26 | 2590 | 2347 | 1157 | 1142 | 48 | 243 | +49% | +49% |
| S123 | ABD |  | 21 | 21 | 9 | 12 | 0 | 0 | +43% | +57% |
| S123 | ABD | 2016-22 | 549 | 549 | 273 | 266 | 10 | 0 | +50% | +48% |
| S123 | ABD | 2023 | 98 | 98 | 52 | 45 | 1 | 0 | +53% | +46% |
| S123 | ABD | 2024-26 | 437 | 369 | 187 | 180 | 2 | 68 | +51% | +49% |
| S123 | AVR |  | 10 | 10 | 5 | 5 | 0 | 0 | +50% | +50% |
| S123 | AVR | 2016-22 | 276 | 276 | 111 | 162 | 3 | 0 | +40% | +59% |
| S123 | AVR | 2023 | 50 | 50 | 26 | 23 | 1 | 0 | +52% | +46% |
| S123 | AVR | 2024-26 | 185 | 178 | 80 | 96 | 2 | 7 | +45% | +54% |
| S123 | BIST |  | 51 | 51 | 33 | 16 | 2 | 0 | +65% | +31% |
| S123 | BIST | 2016-22 | 921 | 921 | 383 | 496 | 42 | 0 | +42% | +54% |
| S123 | BIST | 2023 | 378 | 378 | 100 | 276 | 2 | 0 | +26% | +73% |
| S123 | BIST | 2024-26 | 1092 | 951 | 348 | 577 | 26 | 141 | +37% | +61% |
| SM_TEPE | ABD | 2016-22 | 2810 | 2810 | 2056 | 724 | 30 | 0 | +73% | +26% |
| SM_TEPE | ABD | 2023 | 230 | 230 | 169 | 61 | 0 | 0 | +73% | +27% |
| SM_TEPE | ABD | 2024-26 | 1138 | 1092 | 801 | 280 | 11 | 46 | +73% | +26% |
| SM_TEPE | AVR |  | 7 | 7 | 3 | 4 | 0 | 0 | +43% | +57% |
| SM_TEPE | AVR | 2016-22 | 2200 | 2200 | 1671 | 502 | 27 | 0 | +76% | +23% |
| SM_TEPE | AVR | 2023 | 266 | 266 | 195 | 66 | 5 | 0 | +73% | +25% |
| SM_TEPE | AVR | 2024-26 | 1015 | 913 | 704 | 186 | 23 | 102 | +77% | +20% |
| SM_TEPE | BIST | 2016-22 | 731 | 731 | 562 | 136 | 33 | 0 | +77% | +19% |
| SM_TEPE | BIST | 2023 | 123 | 123 | 80 | 35 | 8 | 0 | +65% | +28% |
| SM_TEPE | BIST | 2024-26 | 301 | 275 | 209 | 59 | 7 | 26 | +76% | +21% |

## KARAR (önceden yazılı etiket kuralı)

- Kural: TAM_DIP satırı ORTAK CETVEL v1.0: hücre TUTAR = dört şart + iki yarı > 0 (oc_hucre); durum oc_hucre_durum; genel etiket FO.fo_etiket(+) = OC.oc_etiket ve cetvelin 'İZ DEĞİL'i 'DESTEKLENMEDİ' (Ç187 ile aynı): İZ (dört karar hücresi ABD / AVR x 2023 / 2024-26 TUTAR) / EMARE (en az biri) / ÖLÇÜLEMEDİ (güç yetersiz) / DESTEKLENMEDİ (güç yeterli, tutmadı). BIST bilgi; 2016-22 keşif bilgi.
- TAM_DIP (ANA) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 ÖLÇÜLEMEDİ, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 ÖLÇÜLEMEDİ
- TAM (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 ÖLÇÜLEMEDİ, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 ÖLÇÜLEMEDİ
- TAM_ORTA (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 ÖLÇÜLEMEDİ, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 ÖLÇÜLEMEDİ
- TAM_TEPE (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 ÖLÇÜLEMEDİ, AVR 2023 None, AVR 2024-26 None
- S1 (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 TUTMADI, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 TUTMADI
- S12 (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 TUTMADI, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 TUTMADI
- S123 (bilgi) [yön +]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 ÖLÇÜLEMEDİ, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 ÖLÇÜLEMEDİ
- SM_TEPE (bilgi) [yön -]: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 TUTMADI, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 ÖLÇÜLEMEDİ
- Bilgi satırları BH q 0,10: 0 / 23 test geçti.

## KÖR SET 2

- Karar: **GÖZLE UYUMSUZ** (TAM sayfalarında E payı >= 0,60 VE TAM - DEĞİL E payı farkı >= 0,30 -> 'GÖZLE UYUMLU'; TAM E payı < 0,40 -> 'GÖZLE UYUMSUZ'; aksi 'KISMİ'. Fisher kesin p bilgi. Sonuç (r20 / r60 / önce kırılım-stop) yalnız bilgi; n küçük, bulgu değil). TAM E 1 / 19, DEĞİL E 1 / 7; Fisher p 0,474.
- Yanıtlı sayfa (n_yanitli) 26 / 40; yanıtsız 14 (paylardan çıkarıldı): 4, 6, 20, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40.
- TAM: E 1 / H 12 / B 6 (n 19; E payı +5%); DEĞİL: E 1 / H 1 / B 5 (n 7; E payı +14%); TAM BIST: E 0 / H 7 / B 3 (n 10; E payı +0%); TAM ABD: E 1 / H 5 / B 3 (n 9; E payı +11%).

| Yanıt türü | TAM E / H / B (n) | DEĞİL E / H / B (n) |
|---|---|---|
| açık | 0 / 4 / 5 (9) | 0 / 0 / 3 (3) |
| çıkarım | 1 / 8 / 1 (10) | 1 / 1 / 2 (4) |

| Cemal etiketi | TAM | DEĞİL |
|---|---|---|
| E | 1 | 1 |
| H | 12 | 1 |
| B | 6 | 5 |
| yanıtsız (-) | 11 | 3 |

| Grup | Cemal etiketi | n | r20 medyan | r60 medyan | önce KIRILIM payı | önce STOP payı |
|---|---|---|---|---|---|---|
| TAM | E | 1 | +40,0% | +53,6% | +100% | +0% |
| TAM | H | 12 | +4,8% | +0,1% | +50% | +50% |
| TAM | B | 6 | -7,3% | -6,1% | +17% | +83% |
| DEĞİL | E | 1 | -3,2% | +47,8% | +100% | +0% |
| DEĞİL | H | 1 | +21,1% | +11,2% | +100% | +0% |
| DEĞİL | B | 5 | +5,4% | -12,4% | +75% | +25% |
- Okuma: sonuç sütunları (r20 / r60 / önce kırılım-stop) yalnız bilgi; etiket başına n küçük, bulgu değil.

## VERİ ve SINIRLAR

- ABD: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 1411
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 580
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 581
- Hayatta kalma: evren bugün işlem gören hisseler; (3) / (5) düşmüş hisseleri seçtiği için yanlılık bu satırda büyüyebilir.
- Komisyon / kayma yok; 31.08.2026 sonrası fiyat yok.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: (3) dönüm (60 bar tepeden >= %10-20 düşmüş) ve (5) tepede değil sinyali düşük 60 gün momentumlu hisselere iter; eşler aynı momentum beşliğinden olduğu için bu fark eşlenir; kısa vadeli dönüş / oynaklık eşlenmez (raporda sınır) |
| K2 | geleceğe bakma | EVET | bütün ölçüler rolling geriye (fv_olcu: W, önceki 30 / 60 / 120 / 250 bar t'de biter; bağlam KONUM t dahil 250 bar); etiket seti Cemal'in t'de biten sayfaları; kos fv_gelecek_denetimi her pazarda 40 TAM_DIP gününde (bağlam dahil) seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma' (rastgele seride kesme = tam seri, bütün günler); tasarımda getiri / r20 / r60 hiç okunmadı (anahtarın r alanları atlanır) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz barlar (H>L, V>0, fiyat > 0; geçersiz bar atılır, pencereye girmez) + FO.fo_bar ikinci süzgeç; DGXX etiketi yfinance'ta 16 Kas (seans içi yarım bar) alınmaz ve aynı süzgeçten geçer |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir (ilk gün); n bağımsız olay; hücrede medyan da yazılır; ön kayıt OLAY SAYIMI durum günü ve tekil olayı ayrı verir |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter; kör set r20 / r60 de t+1 açılışından |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); bütün şartlar oran (fitil payı, HAT'a göre %, tepeye göre %), birimden bağımsız; bölünme şüphesi cetvelde geçmiş pencerede havuz dışı; DGXX etiketi ham (auto_adjust=False), yalnız etiket |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı, -%50 olasılığı aşağı yanlı' notu; (3) dönüm ve (5) tepede değil düşmüş hisseleri seçtiği için hayatta kalma yanlılığı bu işte daha büyük olabilir |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; tasarım seti küçük (19 + 10 sayfa + 5 aralık): eşik seçimi bulgu değil, yalnız tanım kalibrasyonu; olay sayımı getirisiz |
| K9 | ön kayıt | EVET | V2_ESIK sha + V2_SECIM + FITIL_V2.py sha + TASARIM.md sha + kör anahtar / cevap sha + cetvel üç sha + veri sha bu dosyada; ızgara (72 nokta) ve sadelik sırası tasarımdan önce kodda yazılı; iş tanımı git'te (22d7e50); kos ik_kontrol_kapisi + OC.oc_kapi + fv_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; etiket sayfaları kor_anahtar.json'dan (sembol / tarih) mekanik; 3 sayfa (PAPIL No 3, LIDER No 26, EPLAS No 41) ham V_BIST'ten bağımsız kodla yeniden hesaplandı: ASIM / ALTYOK / HAT / düşüş / yol / tepe / düz TASARIM tablosuyla aynı |
| K11 | yeniden üretim | EVET | ana olay satırları /tmp/fitil_v2/olay_TAM_DIP.csv.gz (bağlam ve kırılım sütunlu); rapor >= 2 hücreyi bağımsız kodla yeniden üretir (ana model denetimi); tasarım tablosu her etiketin ölçü değerlerini yazar (elle yeniden hesaplanabilir) |
| K12 | ifade | EVET | etiketler yalnız FO.fo_etiket / oc_etiket kuralıyla; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok; kör set sorusu 'tam girilir mi', alım tavsiyesi değil |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fv; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar taraması testte ve her yazımda; ücretli veri yok; commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tanım ölçümü ve kör set (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## ÖZET (bulgu dili; ek)

- TAM GİRİLİR + DİP (ana satır TAM_DIP) eşlerini geçmiyor, ama sayı az olduğu için "iz değil" de denemiyor: KARAR **ÖLÇÜLEMEDİ**. Karar hücrelerinde 60 günlük eşli fark ABD 2023 -%1,7 (n 47), ABD 2024-26 +%1,1 (n 187), AVR 2023 -%3,8 (n 34), AVR 2024-26 -%1,8 (n 132). Dört hücrenin hiçbirinde %95 aralığı sıfırın üstünde değil. Güç %10-29 (n 1.000'e uzak).
- BIST (bilgi): 2023 -%4,1 (n 101), 2024-26 +%2,2 (n 387). İkisi de tutmuyor.
- Olasılık (250 gün): TAM_DIP hissesinin -%50 görme olasılığı eşlerinden yüksek. ABD 2016-22'de 1,23 kat [1,05, 1,44], AVR 2016-22'de 1,59 kat [1,05, 2,29], AVR 2024-26'da 2,06 kat [1,19, 2,88]. +%100 tarafında ABD 2024-26'da 1,47 kat [0,97, 1,95], ama alt uç 1'in altında. Etiket her hücrede YOK. Yani bu günler eşlerden daha riskli; daha kazançlı oldukları görülmüyor.
- Önce kırılım mı, stop mu: TAM_DIP olaylarının çoğu önce stop oluyor (HAT x 0,98 altı kapanış; 60 bar içinde). Stop önce: ABD %49-60, AVR %44-67, BIST %55-74. Kırılım önce (pencere tepesi üstü kapanış): ABD %39-51, AVR %33-56, BIST %26-43.
- Ayna (SM_TEPE, tepede ters öbek = 'ÇIK'): ABD 2024-26'da güç yeterli ve TUTMADI (eşli fark -%0,5 [-2,4, +1,3], n 1.092). Tepede S- sonrası -%50 olasılığı eşlerinden DÜŞÜK: ABD 0,66-0,71 kat, AVR 0,25-0,84 kat. Bu, 'çık' okumasının tersine işaret eder (bilgi satırı).
- Bilgi satırları: S1 (şekil tek başına) ve S1+2 ABD 2024-26 / AVR 2024-26'da güç yeterli ve TUTMADI. Bu, Ç187'deki S+ sonucuyla aynı yöndür. S1+2+3 ABD'de 2016-22 ve 2023'te PİYANGO etiketi aldı: +%100 de -%50 de eşlerden sık. 2024-26'da etiket YOK. Bilgi testlerinin hiçbiri BH q 0,10'u geçmedi (0 / 23).
- Kör set 2 hazır (40 sayfa + 1 açıklama sayfası); Cemal'in işaretlemesi bekleniyor.

## DENETİM (K11; alt ajanın bağımsız yeniden üretimi)

- Satır dosyası: arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz (ana satır, 1.402 olay). Bilgi satırları scratchpad'te: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/fitil_v2_satir/olay_*.csv.gz.
- TAM_DIP satırının 9 hücresinde n, ortalama / medyan fark, sıra ve iki yarı, satır dosyasından ayrı bir betikle yeniden hesaplandı. 9 hücrenin 9'u sonuc.json ile birebir aynı (ör. ABD 2024-26: n 187, ort +0,01144, medyan -0,02214; AVR 2023: n 34, ort -0,03846).
- r60, ham V_ABD fiyatından (giriş açılışı, birleşik takvimde +59. gün kapanışı) rastgele 4 olayda yeniden hesaplandı: AGNT, GME, SHOE, CNM. Dördü de olay dosyasıyla aynı.
- Kırılım / stop sayıları satır dosyasından yeniden sayıldı; rapor tablosuyla aynı.
- Ön kayıt commit 04bbf17 (07:49:40 UTC) < koşu 08:00:01 UTC. Geleceğe bakma denetimi her pazarda 40 TAM_DIP gününde (bağlam dahil) TUTTU.

## HATA

1. **İlk kos koşusu kesildi.** Alt ajanın kabuk zaman aşımı (595 sn) koşuyu S12 satırından sonra kesti; sonuc.json yazılmamıştı. Log yalnız satır etiketlerini gösterdi (hepsi ÖLÇÜLEMEDİ). Aynı kod ve aynı ön kayıtla ikinci koşu baştan, arka planda yapıldı. Koşu deterministik (sabit tohumlar); eşik ve kod değişmedi. Süreç notu.
2. **Kırılım / stop tablosunda dönemi boş satırlar var.** Bunlar giriş günü 2016 öncesi ya da 2026-08-31 sonrası olaylar. Gösterim kusuru, karar dışı. Paylar "+41%" gibi işaretli basılıyor (`_yz` biçimi). Kod ön kayıt sha'sında mühürlü olduğu için düzeltilmedi.
3. **Kırılım / stop "n" sütunu tekil olay sayısıdır** (r60'ı ölçülemeyenler dahil); 60 bar yoksa ÖLÇÜLMEZ. Hücre tablosundaki n r60'ı ölçülebilir olaylardır. İki n farklıdır (ör. ABD 2024-26: 212 / 187).
4. **Kırılım / stop geometrisi satırlar arası karşılaştırılamaz.** Tavan = pencere tepesi, stop = HAT x 0,98; ikisi de satırın kendi penceresinden. SM_TEPE'nin %73-77 'önce kırılım' payı tepede dar pencerenin geometrisidir, yükseliş kanıtı değildir.
5. **TAM_TEPE yapısal olarak boş** (n 0-1): (5) 'tepede değil' şartı TEPE bağlamını zaten dışlıyor. Ön kayıtta öngörülmüştü.
6. **Önceki turlardan:** HATA 2 (sağlam hattın iki alt şartı tanım gereği hep doğru), HATA 3 (BINBN'de geçmiş yetersiz), HATA 4 (SÜREÇ NOTU: r20 / r60 `head` ile görüldü) ve HATA 6 (KONUM'un High / Low aralığıyla tanımlanması bir yorumdur) ön kayıtta yazılı.

## ÖNERİLEN DEFTER METNİ (ana model işler)

- **IK_KAYIT Ç189** — S+ v2 'TAM GİRİLİR' (FITIL_V2.py; Cemal'in K10-K15 kuralları: şekil + savunma hattı + dönüm + yol almamış + tepede değil; bağlam DİP). Tasarım: 72 noktalı ızgara, N30 seçildi (S+, düz kapalı, tol 0,02, düşüş 0,20, yol 0,10); SAPMA-1 ((4) t hariç pencere tepesi) tasarımdan önce. ORTAK CETVEL v1.0, ana satır TAM_DIP: ÖLÇÜLEMEDİ. Karar hücreleri ABD 2023 -%1,7 n 47, ABD 2024-26 +%1,1 n 187, AVR 2023 -%3,8 n 34, AVR 2024-26 -%1,8 n 132; güç %10-29. Olasılık YOK, ama -%50 eş katı > 1 (ABD 2016-22 1,23; AVR 2024-26 2,06). Önce stop %44-74. SM_TEPE 'ÇIK' aynası ABD 2024-26 TUTMADI. S1 / S1+2 ABD + AVR 2024-26 TUTMADI (Ç187 ile aynı yön). Kör set 2 (40 sayfa) Cemal'de. Ön kayıt 04bbf17, ON_KAYIT sha cc02f7fa.
- **IK_ILERI:** TAM_DIP ÖLÇÜLEMEDİ. Aynı komut (`python FITIL_V2.py kos`, sha'lar sabit, yeni veri kesiğiyle) kriz sonrası 2026-09 .. 2027-06 girişleri ölçülebilir olunca (2027 Ağustos sonu) yeniden koşulur. Eşik aynı; karar hücresi n hedefi her hücrede >= 100. Ayrıca kör set 2 yanıtı gelince `olc` kuralı (GÖZLE UYUMLU / KISMİ / UYUMSUZ) yazılır.
- **IK_GOREV:** 17 Kas: FITIL_V2 iş tanımı + EK (bağlam) + SAPMA-1; tasarım (N30) + ön kayıt (04bbf17) + koşu (TAM_DIP ÖLÇÜLEMEDİ; SM_TEPE ABD 2024-26 TUTMADI) + kör set 2 (FITIL_V2_KOR_SET.pdf, 40 sayfa). Açık: Cemal'in kör set 2 yanıtı (`python FITIL_V2.py olc --cevap "1:E,..."`).
