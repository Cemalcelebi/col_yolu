# FITIL_OBEK — RAPOR (Cemal'in fitil öbeği hipotezi, ORTAK CETVEL v1.0)

Ön kayıt yazım 2026-11-16 20:06:22 UTC (sha d683f5106376…; git: İŞLENMEDİ (gitsiz koşu; ön kayıt sha d683f5106376…, yazım 2026-11-16 20:06:22 UTC)); iş tanımı git 99bdc76cc2 (2026-11-16T19:47:17+00:00); koşu 2026-11-16 20:06:22 UTC; süre 707.4 sn. Geleceğe bakma denetimi: ABD 40 + 4 onda olay TUTTU, AVR 40 + 4 onda olay TUTTU, BIST 40 + 4 onda olay TUTTU.

## ÖZET

- S+ (YUKARI öbek) k=10: ASIM >= 0,20 VE ALTYOK >= 0,50 [ANA]: KARAR **ÖLÇÜLEMEDİ** (beklenen yön +); ters yön (bilgi): ÖLÇÜLEMEDİ; olasılık etiketi YOK.
  - ABD 2023: n 889, eş farkı +0,2% [-1,1%, +1,3%], sıra 0,50 -> ÖLÇÜLEMEDİ; ABD 2024-26: n 2180, eş farkı +0,3% [-1,1%, +1,7%], sıra 0,50 -> TUTMADI; AVR 2023: n 649, eş farkı +0,1% [-0,8%, +0,8%], sıra 0,51 -> ÖLÇÜLEMEDİ; AVR 2024-26: n 1734, eş farkı -0,2% [-1,0%, +0,6%], sıra 0,49 -> TUTMADI; BIST 2023: n 719, eş farkı -0,5% [-2,2%, +1,2%], sıra 0,49 -> ÖLÇÜLEMEDİ; BIST 2024-26: n 2597, eş farkı -0,8% [-2,1%, +0,6%], sıra 0,49 -> TUTMADI
- S- (AŞAĞI öbek) k=10: ASIM <= -0,20 VE USTYOK >= 0,50 [ANA]: KARAR **ÖLÇÜLEMEDİ** (beklenen yön -); ters yön (bilgi): ÖLÇÜLEMEDİ; olasılık etiketi YOK.
  - ABD 2023: n 928, eş farkı +0,1% [-1,0%, +1,0%], sıra 0,50 -> ÖLÇÜLEMEDİ; ABD 2024-26: n 2367, eş farkı -0,3% [-1,7%, +1,1%], sıra 0,50 -> TUTMADI; AVR 2023: n 592, eş farkı +0,3% [-0,9%, +1,7%], sıra 0,50 -> ÖLÇÜLEMEDİ; AVR 2024-26: n 1557, eş farkı -0,2% [-0,9%, +0,4%], sıra 0,49 -> TUTMADI; BIST 2023: n 292, eş farkı -2,7% [-8,3%, +2,2%], sıra 0,47 -> ÖLÇÜLEMEDİ; BIST 2024-26: n 524, eş farkı +2,2% [-1,4%, +6,4%], sıra 0,50 -> ÖLÇÜLEMEDİ
- Okuma: 'eş farkı' = olay hissesinin 60 günlük getirisi eksi aynı gün, aynı 60 gün momentum ve likidite kovasındaki öteki hisselerin ortalaması. S+ için beklenen > 0, S- için < 0 (kaçınma, ayna şart). Hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı. Komisyon yok.

## TANIM

- Bar: geçerli bar (OC.oc_veri temiz: H > L, V > 0, fiyat > 0); R = H - L; alt = (min(O,C) - L) / R; üst = (H - max(O,C)) / R; gövde = |C - O| / R.
- Pencere: son k geçerli bar (t dahil, rolling; yalnız t'ye kadar bilgi). A = ortalama alt, U = ortalama üst, ASIM = U - A; ALTYOK = alt < 0,10 bar payı; USTYOK = üst < 0,10 bar payı.
- S+ k=10: ASIM >= 0,20 VE ALTYOK >= 0,50. S- k=10: ASIM <= -0,20 VE USTYOK >= 0,50.
- KUCUK: KUCUK = pencere medyanı (R / C) <= 0,75 x ATR%250; ATR%250 = t'de biten 250 geçerli barın (en az 120) ortalama TR / C; TR = max(H, önceki geçerli kapanış) - min(L, önceki geçerli kapanış).
- Onda: aynı gün (t), aynı pazarda k=10 ASIM'i tanımlı hisseler arasında yüzdelik sıra (rank pct, ortalama bağ); > 0,90 -> S+ onda; <= 0,10 -> S- onda (50 hissede 5 / 5); o gün en az 30 hisse (yalnız t günü bilinen).
- Olay: DURUM GÜNLERİ: şartın t (pencerenin son günü) kapanışında doğru olduğu her geçerli bar OC.oc_olc'a verilir; giriş t'den sonraki ilk geçerli açılış, tekilleştirme 60 gün (cetvel: ilk durum günü tutulur).
- S- ayna kuralı: S- beklenen yön aşağı (kaçınma, AYNA; fark = eşli - olay): n >= 30; ortalama eşli fark < 0 VE ay kümeli %95 ÜST uç < 0; ortalama hücre içi sıra < 0,50; slot portföyü < 200 plasebo portföyün %10 yüzdeliği (p10); iki yarının ortalama eşli farkı da < 0. Durum: n < 30 ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 ya da güç(n, δ 5) >= %80) -> TUTMADI; aksi ÖLÇÜLEMEDİ (OC.oc_hucre_durum, tutar yerine ayna şart).

## OLAY SAYIMI (cetvel düşmeleri; ana satırlar)

| Satır | Pazar | girdi (durum günü) | havuz dışı (lik alt %20 / geçmiş bölünme / geçmiş eksik / evren öncesi / havuz < 30) | tekil düşen | r60 ölçülemedi | eş < 3 |
|---|---|---|---|---|---|---|
| SP_k10 | ABD | 52813 | 24339 (21723 / 472 / 2144 / 0 / 0) | 20447 | 377 | 0 |
| SP_k10 | AVR | 64142 | 30780 (29594 / 122 / 1064 / 0 / 0) | 26955 | 146 | 0 |
| SP_k10 | BIST | 76536 | 9622 (6949 / 178 / 2495 / 0 / 0) | 59275 | 293 | 1 |
| SM_k10 | ABD | 60008 | 22863 (20184 / 324 / 2355 / 0 / 0) | 27445 | 98 | 0 |
| SM_k10 | AVR | 73719 | 31830 (28636 / 18 / 3175 / 0 / 1) | 34489 | 192 | 0 |
| SM_k10 | BIST | 50920 | 26518 (23394 / 186 / 2938 / 0 / 0) | 21231 | 48 | 0 |

## HÜCRE TABLOSU (r60 eşli fark; şartlar beklenen yönde: n / fark+aralık / sıra / portföy / iki yarı; E = tuttu, h = tutmadı)

| Satır | Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / plasebo | yarı1 / yarı2 | şart | güç (δ 5) | durum (beklenen) | durum (ters, bilgi) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SP_k10 | ABD | 2016-22 | b | 4367 | -0,2% [-1,1%, +0,6%] | -1,0% | 0,50 | +159% / p90 +282% / p10 +48% | -0,3% / -0,2% | Ehhhh | 60% | TUTMADI | TUTMADI |
| SP_k10 | ABD | 2023 | K | 889 | +0,2% [-1,1%, +1,3%] | -0,8% | 0,50 | +32% / p90 +32% / p10 -1% | +0,3% / +0,1% | EhhEE | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SP_k10 | ABD | 2024-26 | K | 2180 | +0,3% [-1,1%, +1,7%] | -1,7% | 0,50 | +54% / p90 +104% / p10 +2% | -0,2% / +0,8% | EhEhh | 65% | TUTMADI | TUTMADI |
| SP_k10 | AVR | 2016-22 | b | 3485 | -0,3% [-0,8%, +0,2%] | -0,5% | 0,50 | +23% / p90 +115% / p10 +18% | +0,1% / -0,7% | Ehhhh | 60% | TUTMADI | TUTMADI |
| SP_k10 | AVR | 2023 | K | 649 | +0,1% [-0,8%, +0,8%] | +0,3% | 0,51 | -8% / p90 +19% / p10 -2% | +0,1% / +0,1% | EhEhE | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SP_k10 | AVR | 2024-26 | K | 1734 | -0,2% [-1,0%, +0,6%] | -0,5% | 0,49 | +26% / p90 +56% / p10 +9% | -0,3% / -0,2% | Ehhhh | 65% | TUTMADI | TUTMADI |
| SP_k10 | BIST | 2016-22 | b | 3725 | -0,1% [-1,2%, +1,1%] | -4,6% | 0,50 | +1395% / p90 +4019% / p10 +723% | -0,0% / -0,1% | Ehhhh | 60% | TUTMADI | TUTMADI |
| SP_k10 | BIST | 2023 | b | 719 | -0,5% [-2,2%, +1,2%] | -7,0% | 0,49 | +87% / p90 +110% / p10 +19% | -0,3% / -0,8% | Ehhhh | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SP_k10 | BIST | 2024-26 | b | 2597 | -0,8% [-2,1%, +0,6%] | -6,5% | 0,49 | +88% / p90 +230% / p10 +41% | -1,8% / +0,3% | Ehhhh | 65% | TUTMADI | TUTMADI |
| SM_k10 | ABD | 2016-22 | b | 5975 | -0,2% [-0,9%, +0,4%] | -0,8% | 0,50 | +327% / p90 +226% / p10 +47% | +0,2% / -0,6% | EhEhh | 60% | TUTMADI | TUTMADI |
| SM_k10 | ABD | 2023 | K | 928 | +0,1% [-1,0%, +1,0%] | -1,4% | 0,50 | +13% / p90 +43% / p10 +4% | +0,4% / -0,2% | Ehhhh | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SM_k10 | ABD | 2024-26 | K | 2367 | -0,3% [-1,7%, +1,1%] | -2,4% | 0,50 | +46% / p90 +126% / p10 +19% | +0,9% / -1,5% | EhEhh | 65% | TUTMADI | TUTMADI |
| SM_k10 | AVR | 2016-22 | b | 4583 | +0,2% [-0,2%, +0,6%] | +0,0% | 0,51 | +108% / p90 +133% / p10 +36% | +0,3% / +0,0% | Ehhhh | 60% | TUTMADI | TUTMADI |
| SM_k10 | AVR | 2023 | K | 592 | +0,3% [-0,9%, +1,7%] | -0,2% | 0,50 | +5% / p90 +17% / p10 -3% | +0,1% / +0,5% | EhEhh | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SM_k10 | AVR | 2024-26 | K | 1557 | -0,2% [-0,9%, +0,4%] | -0,6% | 0,49 | +15% / p90 +50% / p10 +9% | -0,3% / -0,2% | EhEhE | 65% | TUTMADI | TUTMADI |
| SM_k10 | BIST | 2016-22 | b | 2068 | -0,6% [-2,6%, +1,3%] | -4,6% | 0,49 | +14580% / p90 +4498% / p10 +768% | +0,7% / -1,9% | EhEhh | 65% | TUTMADI | TUTMADI |
| SM_k10 | BIST | 2023 | b | 292 | -2,7% [-8,3%, +2,2%] | -8,3% | 0,47 | +28% / p90 +84% / p10 +5% | -1,5% / -3,9% | EhEhE | 29% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| SM_k10 | BIST | 2024-26 | b | 524 | +2,2% [-1,4%, +6,4%] | -6,0% | 0,50 | +305% / p90 +293% / p10 +56% | +1,1% / +3,2% | EhEhh | 52% | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |

## OLASILIK TABLOSU (250 gün dokunma; eş katı karar, taban katı bilgi)

| Satır | Pazar | Dönem | n250 | P(+%100) olay / eş | kat eş [%95] | kat taban | P(-%50) olay / eş | kat eş [%95] | kat taban | etiket | S- aşağı seçici |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SP_k10 | ABD | 2016-22 | 4367 | +6,5% / +6,9% | 0,93 [0,82, 1,06] | 0,96 | +14,4% / +14,0% | 1,02 [0,93, 1,11] | 1,05 | YOK | - |
| SP_k10 | ABD | 2023 | 889 | +10,8% / +9,5% | 1,13 [0,99, 1,29] | 1,15 | +7,3% / +7,9% | 0,93 [0,73, 1,20] | 0,94 | YOK | - |
| SP_k10 | ABD | 2024-26 | 1401 | +12,3% / +12,0% | 1,02 [0,87, 1,18] | 1,04 | +13,6% / +13,5% | 1,01 [0,83, 1,22] | 1,03 | YOK | - |
| SP_k10 | AVR | 2016-22 | 3485 | +2,4% / +2,6% | 0,90 [0,72, 1,10] | 0,96 | +7,2% / +7,8% | 0,91 [0,78, 1,03] | 0,95 | YOK | - |
| SP_k10 | AVR | 2023 | 649 | +1,4% / +1,2% | 1,14 [0,40, 1,91] | 1,12 | +4,5% / +4,4% | 1,01 [0,80, 1,23] | 1,03 | YOK | - |
| SP_k10 | AVR | 2024-26 | 1256 | +2,6% / +2,7% | 0,98 [0,68, 1,31] | 0,92 | +4,2% / +4,5% | 0,93 [0,72, 1,18] | 1,00 | YOK | - |
| SP_k10 | BIST | 2016-22 | 3727 | +39,5% / +40,0% | 0,99 [0,96, 1,02] | 0,98 | +6,6% / +6,5% | 1,02 [0,91, 1,13] | 1,01 | YOK | - |
| SP_k10 | BIST | 2023 | 719 | +45,5% / +48,1% | 0,95 [0,85, 1,00] | 0,95 | +4,5% / +4,9% | 0,92 [0,75, 1,11] | 0,90 | YOK | - |
| SP_k10 | BIST | 2024-26 | 1720 | +22,0% / +21,9% | 1,00 [0,92, 1,09] | 0,98 | +5,8% / +6,1% | 0,96 [0,85, 1,06] | 0,90 | YOK | - |
| SM_k10 | ABD | 2016-22 | 5975 | +7,2% / +7,9% | 0,92 [0,84, 1,02] | 0,93 | +12,1% / +12,9% | 0,94 [0,84, 1,05] | 0,92 | YOK | - |
| SM_k10 | ABD | 2023 | 928 | +7,7% / +8,9% | 0,86 [0,68, 1,08] | 0,85 | +8,5% / +8,3% | 1,03 [0,83, 1,24] | 1,07 | YOK | - |
| SM_k10 | ABD | 2024-26 | 1759 | +12,3% / +13,4% | 0,92 [0,79, 1,06] | 0,92 | +11,2% / +12,1% | 0,92 [0,79, 1,04] | 0,91 | YOK | - |
| SM_k10 | AVR | 2016-22 | 4583 | +2,7% / +2,7% | 0,99 [0,83, 1,17] | 1,03 | +7,3% / +7,7% | 0,95 [0,87, 1,04] | 0,96 | YOK | - |
| SM_k10 | AVR | 2023 | 592 | +1,2% / +1,3% | 0,94 [0,39, 1,60] | 1,01 | +2,9% / +4,7% | 0,61 [0,33, 0,93] | 0,63 | YOK | - |
| SM_k10 | AVR | 2024-26 | 1025 | +3,2% / +3,0% | 1,09 [0,75, 1,45] | 1,01 | +4,1% / +3,9% | 1,04 [0,81, 1,26] | 0,96 | YOK | - |
| SM_k10 | BIST | 2016-22 | 2070 | +38,6% / +38,7% | 1,00 [0,95, 1,05] | 1,06 | +8,2% / +6,5% | 1,27 [1,11, 1,46] | 1,32 | YOK | - |
| SM_k10 | BIST | 2023 | 292 | +44,9% / +47,9% | 0,94 [0,84, 1,04] | 1,01 | +7,5% / +8,5% | 0,89 [0,51, 1,57] | 0,96 | YOK | - |
| SM_k10 | BIST | 2024-26 | 329 | +28,9% / +27,2% | 1,06 [0,91, 1,24] | 1,24 | +10,9% / +7,7% | 1,42 [0,91, 2,00] | 1,82 | YOK | - |

## BİLGİ SATIRLARI (karar dışı; beklenen yönde p, BH q 0,10 karar hücrelerinde)

| Satır | etiket (beklenen) | ters (bilgi) | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|
| SP_k5 | DESTEKLENMEDİ | DESTEKLENMEDİ | n 2260, +0,1% [-0,8%, +1,0%], TUTMADI, p 0,418 | n 5325, +0,0% [-0,9%, +1,0%], TUTMADI, p 0,479 | n 1171, +0,0% [-0,4%, +0,4%], TUTMADI, p 0,470 | n 3025, -0,3% [-0,9%, +0,3%], TUTMADI, p 0,843 | n 1034, -0,8% [-3,5%, +2,0%], TUTMADI | n 3383, +0,1% [-0,9%, +1,2%], TUTMADI |
| SM_k5 | DESTEKLENMEDİ | DESTEKLENMEDİ | n 2178, -0,1% [-1,1%, +0,7%], TUTMADI, p 0,401 | n 5603, +0,0% [-1,0%, +1,0%], TUTMADI, p 0,526 | n 1116, +0,1% [-0,5%, +0,8%], TUTMADI, p 0,675 | n 2845, +0,2% [-0,3%, +0,6%], TUTMADI, p 0,760 | n 654, -0,8% [-4,5%, +3,2%], ÖLÇÜLEMEDİ | n 1458, +2,1% [-0,7%, +5,5%], TUTMADI |
| SP_k15 | ÖLÇÜLEMEDİ | EMARE (ABD 2024-26) | n 221, -0,8% [-3,1%, +1,1%], ÖLÇÜLEMEDİ, p 0,744 | n 522, -2,1% [-4,5%, -0,0%], ÖLÇÜLEMEDİ, p 0,975 | n 283, +0,2% [-1,5%, +1,9%], ÖLÇÜLEMEDİ, p 0,400 | n 774, -0,5% [-1,6%, +0,7%], ÖLÇÜLEMEDİ, p 0,810 | n 368, -1,7% [-4,8%, +1,3%], ÖLÇÜLEMEDİ | n 1576, -0,5% [-2,8%, +2,2%], TUTMADI |
| SM_k15 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ | n 188, -2,2% [-6,3%, +0,5%], ÖLÇÜLEMEDİ, p 0,059 | n 604, -1,2% [-3,8%, +1,3%], ÖLÇÜLEMEDİ, p 0,186 | n 242, +0,4% [-0,7%, +1,6%], ÖLÇÜLEMEDİ, p 0,735 | n 625, -0,6% [-1,4%, +0,1%], ÖLÇÜLEMEDİ, p 0,047 | n 119, -3,2% [-7,1%, +0,6%], ÖLÇÜLEMEDİ | n 214, +3,3% [-2,8%, +10,2%], ÖLÇÜLEMEDİ |
| SP_kucuk | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ | n 576, +0,8% [-0,6%, +1,8%], ÖLÇÜLEMEDİ, p 0,109 | n 779, -1,2% [-2,8%, -0,0%], ÖLÇÜLEMEDİ, p 0,977 | n 422, +0,1% [-1,3%, +1,8%], ÖLÇÜLEMEDİ, p 0,438 | n 759, -0,5% [-1,4%, +0,5%], ÖLÇÜLEMEDİ, p 0,817 | n 390, -0,5% [-2,0%, +1,5%], ÖLÇÜLEMEDİ | n 1549, -1,2% [-3,0%, +0,7%], TUTMADI |
| SM_kucuk | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ | n 591, -0,2% [-1,8%, +1,1%], ÖLÇÜLEMEDİ, p 0,398 | n 947, +0,7% [-0,9%, +2,5%], ÖLÇÜLEMEDİ, p 0,801 | n 401, +0,3% [-1,0%, +2,0%], ÖLÇÜLEMEDİ, p 0,652 | n 699, +0,0% [-0,9%, +1,1%], ÖLÇÜLEMEDİ, p 0,513 | n 59, -1,7% [-10,7%, +5,9%], ÖLÇÜLEMEDİ | n 223, -0,5% [-4,4%, +3,7%], ÖLÇÜLEMEDİ |
| SP_onda | DESTEKLENMEDİ | DESTEKLENMEDİ | n 2647, +0,4% [-0,4%, +1,3%], TUTMADI, p 0,153 | n 6820, +0,0% [-0,7%, +0,7%], TUTMADI, p 0,466 | n 1059, -0,1% [-0,7%, +0,6%], TUTMADI, p 0,617 | n 2637, +0,0% [-0,7%, +0,7%], TUTMADI, p 0,503 | n 967, -0,2% [-2,5%, +2,8%], ÖLÇÜLEMEDİ | n 2697, +0,0% [-0,9%, +1,0%], TUTMADI |
| SM_onda | DESTEKLENMEDİ | DESTEKLENMEDİ | n 2781, +0,0% [-0,7%, +0,7%], TUTMADI, p 0,506 | n 7139, +0,3% [-0,4%, +1,0%], TUTMADI, p 0,827 | n 1117, +0,2% [-0,5%, +0,8%], TUTMADI, p 0,695 | n 2857, -0,0% [-0,4%, +0,4%], TUTMADI, p 0,441 | n 724, -0,1% [-2,8%, +2,4%], ÖLÇÜLEMEDİ | n 1914, +2,2% [+0,0%, +4,4%], TUTMADI |

BH q 0,10 geçen bilgi testi: 0 / 32.

## ÖRNEK DOĞRULAMA (k=10; tanım değiştirilmedi)

| Hisse | bölge | kaynak | bar | alt medyan / üst medyan | alt yok / üst yok payı | ASIM min / maks | ALTYOK maks / USTYOK maks | S+ günleri | S- günleri |
|---|---|---|---|---|---|---|---|---|---|
| PAPIL | 2025-11-13 .. 2025-12-09 | oc_veri BIST | 19 | 0,12 / 0,44 | 0,47 / 0,11 | 0,11 / 0,33 | 0,70 / 0,30 | 2025-11-14, 2025-11-17, 2025-11-18, 2025-11-19, 2025-11-20, 2025-11-21, 2025-11-24, 2025-11-25, 2025-11-26, 2025-12-08 | yok |
| DGXX | 2026-10-27 .. 2026-11-13 | yfinance (yalnız örnek) | 14 | 0,27 / 0,18 | 0,07 / 0,29 | -0,25 / 0,02 | 0,20 / 0,50 | yok | yok |
| FENER | 2025-10-14 .. 2025-11-07 | oc_veri BIST | 18 | 0,17 / 0,31 | 0,28 / 0,28 | -0,06 / 0,11 | 0,70 / 0,30 | yok | yok |
| DESA | 2021-10-27 .. 2021-12-23 | oc_veri BIST | 41 | 0,26 / 0,33 | 0,20 / 0,15 | -0,14 / 0,31 | 0,50 / 0,30 | 2021-11-22 | yok |
| YKSLN | 2026-03-19 .. 2026-05-15 | oc_veri BIST | 38 | 0,18 / 0,33 | 0,24 / 0,21 | -0,01 / 0,37 | 0,50 / 0,30 | 2026-04-17 | yok |

## KARAR (önceden yazılı etiket kuralı)

- SP_k10: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 TUTMADI, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 TUTMADI
- SM_k10: **ÖLÇÜLEMEDİ** (cetvel genel: ÖLÇÜLEMEDİ); karar hücreleri: ABD 2023 ÖLÇÜLEMEDİ, ABD 2024-26 TUTMADI, AVR 2023 ÖLÇÜLEMEDİ, AVR 2024-26 TUTMADI

## VERİ ve SINIRLAR

- ABD: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 1411
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 580
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 581
- Hayatta kalma: evren bugün işlem gören hisseler; batan / kottan çıkan yok. Getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı.
- Komisyon / kayma yok; 31.08.2026 (fon krizi) sonrası fiyat yok; 250 gün dokunma en geç ~Ağustos 2025 girişlerini kapsar.
- Kısa vadeli dönüş / oynaklık eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: sinyal yalnız t'ye kadar mum şekli; giriş t+1 açılışı olduğu için t kapanış konumu getiriyi mekanik üretmez; kısa vadeli dönüş (üst fitilli = kapanış dipte) eşlenmez, raporda sınır olarak yazılır |
| K2 | geleceğe bakma | EVET | pencere ölçüleri rolling (geriye), ATR%250 t'de biter, onda sırası yalnız t günü; kos fo_gelecek_denetimi her pazarda 40 (+4 onda) rastgele olayda seriyi t'de kesip sinyali yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma' |
| K3 | geçerli bar | EVET | sinyal OC.oc_veri temiz barlarıyla (H>L, V>0, fiyat > 0; geçersiz bar veriden atılır, pencereye girmez); DGXX örneğinde 16 Kas (seans içi yarım bar) alınmaz |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücrede medyan da yazılır |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); fitil payları oran, birimden bağımsız; bölünme şüphesi cetvelde (geçmiş pencere); DGXX örneği ham (auto_adjust=False) ama yalnız fitil payı, birim etkisiz |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD 1.411 hisse); batanlar yok; raporda 'getiriler yukarı, -%50 olasılığı aşağı yanlı' notu |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; olay sayımı bu ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | FO_ESIK sha + FITIL_OBEK.py sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce git'e işlendi (99bdc76); kos ik_kontrol_kapisi + OC.oc_kapi + fo_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; örnek bölgelerde fitil payları ham bardan elle yeniden hesaplanır (rapor) |
| K11 | yeniden üretim | EVET | ana olay satırları arastirma_cikti/fitil_obek/olay_ana.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | etiketler yalnız oc_etiket / ayna kuralı; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fo; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar taraması testte ve raporda; ücretli veri yok; commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yön ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## YORUM (sayılardan ayrı)

- Etiket kuralı gereği iki ana satır da ÖLÇÜLEMEDİ: 2023 karar hücreleri n < 1.000 (ABD 889 / 928, AVR 649 / 592) ve güç (δ +%5) %52 < %80. 2024-26 hücreleri (n 1.557-2.367) güç yeterli ve TUTMADI.
- Etki büyüklüğü: dört karar hücresinin hiçbirinde ortalama eşli fark ±%0,3'ü geçmiyor. %95 aralıklar S+ için en çok +%1,7'ye, S- için en çok -%1,7'ye uzanıyor: 60 günde eşlerinden 2 puan ve daha fazla ayrışan bir etki dört hücrenin hiçbirinde aralık içinde değil. Sıra 0,49-0,51.
- Olasılık: +%100 / -%50 eş katlarının aralıkları dört karar hücresinde 1'i içeriyor (tek istisna: SM_k10 AVR 2023 -%50 katı 0,61 [0,33; 0,93], yani AŞAĞI öbekten sonra -%50'ye inme eşlerden SEYREK: beklenen yönün tersi).
- Cemal'in okuması da klasik okuma da (ters yön) karar hücrelerinde tutmuyor (ters yön etiketi iki satırda da ÖLÇÜLEMEDİ; 2024-26'da TUTMADI). Tek bilgi istisnası: SP_k15'in ters yönü (15 barlık S+ öbekten sonra eşlerden KÖTÜ) ABD 2024-26'da dört şartla tuttu (n 522, -%2,1 [-%4,5; -%0,0]); ters yön BH'ye girmedi, tek hücre, aynı öbeğin k=10 / k=5 sürümünde yok: bilgi, bulgu değil.
- BH q 0,10: 32 bilgi testinin 0'ı geçti.
- Örnek: PAPIL bölgesinde S+ 10 gün yanıyor (ilk 14 Kas 2025); DGXX 27 Eki - 13 Kas 2026'da S- YANMIYOR: ASIM 9-10 Kas'ta -0,20 / -0,25'e iniyor (alt fitiller baskın) ama USTYOK en çok 0,50 (28 Eki) ve ASIM'in eşiği geçtiği günlerde 0,30; şart 'ASIM VE USTYOK' aynı günde birlikte tutmuyor. Tanım değiştirilmedi. FENER'de S+ yok; DESA (22 Kas 2021) ve YKSLN (17 Nis 2026) bölgelerinde birer gün S+.

## DENETİM (K11, bağımsız kod: scratchpad fo_yeniden.py)

- Hücreler olay_ana.csv.gz'den ORTAK_CETVEL kullanmadan yeniden üretildi: SP_k10 ABD 2024-26 (n 2.180, ort +0,00302, %95 [-0,01121; +0,01682], sıra 0,5010), SM_k10 AVR 2023 (n 592, +0,00286 [-0,00870; +0,01745], sıra 0,4993), SM_k10 ABD 2023 (n 928, +0,00069 [-0,00960; +0,01022]): rapor ile aynı. İki yarı ortalamaları üçüncü ondalıkta farklı (ör. -0,0027 / +0,0087 vs -0,0023 / +0,0083): aynı giriş günündeki olayların sıralaması (bağ) farkı; işaret ve karar aynı.
- 6 olayın (ABD UBS, SON, EXTR; BIST ECILC, MACKO, KAREL) giriş günü, giriş açılışı ve r60'ı ham V_*.pkl'den (geçerli bar, birleşik takvim, 59 gün sonra kapanış) bağımsız hesaplandı: hepsi aynı.
- Geleceğe bakma denetimi koşu içinde: her pazarda 40 hisse olayı + 4 onda olayı seri t'de kesilerek yeniden hesaplandı, hepsi TUTTU.

## HATA

1. fo_hisse_sinyal 15 bardan kısa seride bütün satırları 'yanlış' döndürüyordu (erken çıkış). İlk kos'ta geleceğe bakma denetimi yakaladı (ABD TGT 2015-06-18 SP_k5: tam seride doğru, 13 barlık kesik seride yanlış) ve koşu durdu. Tam seride etkisi yok (oc_veri en az 80 bar); yalnız denetimin kesik serisini etkiliyordu. Düzeltildi (yalnız boş seride çıkış), test eklendi. Kod sha değiştiği için ön kayıt GETİRİ GÖRÜLMEDEN yeniden yazıldı (ilk sürüm scratchpad ON_KAYIT_v0.md; olay sayımı aynı).
2. kos'taki 'ön kayıt zamanı < koşu zamanı' denetimi aynı saniyede (onkayit && kos art arda) yanlış durdurdu (>= yerine >). Düzeltildi; ön kayıt yine getiri görülmeden yeniden yazıldı.
3. Onda tanımı ilk yazımda '>= 0,90' idi (50 hissede üst 6 / alt 5, asimetrik); ön kayıttan ÖNCE test yakaladı, '> 0,90' yapıldı.
4. SAPMA (süreç): ON_KAYIT.md git'e işlenmedi (alt ajana commit yasak). İş tanımı koşudan önce işlendi (99bdc76, 19:47); ON_KAYIT sha d683f5106376…, yazım 20:06:22 UTC, koşu 20:06:22 UTC (aynı saniye, onkayit && kos zinciri). Ana model işlerken sha'yı karşılaştırmalı; K9 'ön kayıt commit zamanı < koşu zamanı' bu iş için yalnız iş tanımında sağlanıyor.
5. Yorum seçimi: iş tanımı S- için 'fark = eşli - olay' diyor ama portföy şartının aynasını yazmıyor; K62'deki AYNA (portföy < plasebo p10) + cetvelin iki yarı şartının aynası kullanıldı ve ön kayda yazıldı.

## ÖNERİLEN DEFTER METNİ (ana model işler)

- IK_KAYIT Ç (yeni no): "Fitil öbeği (Cemal 16 Kas: PAPIL alt fitilsiz / üst fitilli öbek yukarı, DGXX üst fitilsiz öbek aşağı) ORTAK CETVEL v1.0 | FITIL_OBEK.py, test_fitil_obek.py (52/52) | S+ k10 (ASIM >= 0,20, ALTYOK >= 0,50) ÖLÇÜLEMEDİ: karar hücreleri eşli fark ABD 2023 +%0,2 [-1,1; 1,3] n 889, ABD 2024-26 +%0,3 [-1,1; 1,7] n 2.180 TUTMADI, AVR 2023 +%0,1 n 649, AVR 2024-26 -%0,2 n 1.734 TUTMADI; S- k10 (ASIM <= -0,20, USTYOK >= 0,50) ÖLÇÜLEMEDİ: +%0,1 / -%0,3 (TUTMADI) / +%0,3 / -%0,2 (TUTMADI); 2023 hücreleri n < 1.000 ve güç %52; ±2 puanlık etki dört hücrede aralık dışı. Olasılık YOK. Bilgi satırları (k5, k15, KUCUK, onda) BH 0/32. Ters yön de tutmadı (SP_k15 ters ABD 2024-26 tek hücre). PAPIL bölgesinde S+ var; DGXX'te S- yanmadı (USTYOK 0,30). Hayatta kalma: bugün işlem gören evren; ABD yalnız V_ABD (k34 yok)."
- IK_ILERI: "Fitil öbeği S+ / S- k10, ORTAK CETVEL v1.0, aynı FO_ESIK (sha ön kayıtta); sonraki test: 2027 ilk çeyrek veri kesiği (kriz sonrası 2026-09 .. 2027-03 girişleri, 60 gün) ve k34_yahoo ile ABD 2023 hücresinin n'i; aynı komut `python FITIL_OBEK.py kos`."
- IK_GOREV: "16 Kas: fitil öbeği hipotezi ölçüldü (alt ajan); karar S+ ÖLÇÜLEMEDİ, S- ÖLÇÜLEMEDİ, etki ~0; 3 hata (kısa seri erken çıkışı, zaman denetimi, onda asimetrisi) koşudan / getiriden önce düzeltildi; ON_KAYIT ana modelce işlenecek."
