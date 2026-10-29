# K53 — VERİ DENETİMİ, ÖRNEKLEM KAYBI VE DENGE (v1.4, ön kayıt EK)

Bu belge karar üretmez; K53 kararı K53_RAPOR.md'dedir ve bu denetimle değişmemiştir.

## Analist günlüğü (Yahoo, yfinance upgrades_downgrades)

- Ham kayıt 311015 (2515 hisse); zaman damgası geçersiz ya da aynı kurum aynı tarih kopyası atılan 447; kalan 310568.
- Kurum adı normalizasyonu: 393 ham ad → 371 normalize ad; birden çok ham adı birleştiren 22 normalize ad. En çok birleşenler: SIDOTI: 2; DEUTSCHEBANK: 2; HCWAINWRIGHT: 2; WUNDERLICH: 2; IBERIA: 2; CITIZENS: 2; SCOTIABANK: 2; STANDPOINT: 2.
- Hedef fiyatı eksik kayıt payı 0.081; olumlu kayıt payı 0.535 (up 0.079, Raises 0.420, alım notuyla başlangıç 0.066). Hedef fiyatı olmayan kurum olumlu / olumsuz görüş sayılmadı; ADE yalnız hedef fiyatı olan kurumlardan (≥ 3) hesaplandı, ortalama ≤ 0 ise ölçülemez.
- Kayıt tarihi: hafta sonu payı 0.0017; saat 00:00 payı 0.0000 (damga UTC kabul). Yıl dağılımı: {2011: 3, 2012: 7719, 2013: 8892, 2014: 9140, 2015: 9401, 2016: 9946, 2017: 7176, 2018: 12072, 2019: 11190, 2020: 21544, 2021: 18958, 2022: 26935, 2023: 36620, 2024: 44011, 2025: 45511, 2026: 41450}.
- Geçmiş tarihli verinin sonradan güncellenmiş olma riski: Yahoo günlüğü olay kaydıdır, sürüm bilgisi yoktur; geriye dönük düzeltme doğrulanamaz. Sonuçlar 'sağlayıcı günlüğü doğru' varsayımıyla okunur.
- SPY serisi 2015-06-01 – 2026-08-28; sektörü bilinmeyen hisse payı 0.008 (sektör göreli getiri boş kalır; BDS'de kullanılmaz).

## Olay seçilimi ve örneklem kaybı

- Olumlu kayıt 166000 → işlem gününe eşlenmeyen tarih 23651 (seri başından önce / sonundan sonra / 4 günden uzun boşluk) → ilk olay (önceki 20 gün temiz) 43153 → seri sonu (d0+4 yok) 36 → d0+4 panel dışı (likit değil ya da etiket yok; delist K51 kuralı) 9162 → ölçülemeyen 0 {} → ölçülen 33955.
- Kontroller: G3 aday 202564, G4 aday 60072; [i-24, i] aralığında olumlu kayıt olduğu için atılan 72482; ölçülemeyen 0.

## Denge (grup × dönem) ve G1'e göre standartlaştırılmış ortalama farkları (SMD)

| grup | donem | n | yil_ort | en_buyuk_sektor | en_buyuk_sektor_pay | sektor_bilinmiyor_pay | lt_ort | vd_ort | dd250_ort | vol60_ort | log_dv20_ort | r60_ort | kapsama_365_ort | boga_pay | V_ABD_pay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | 2016-22 | 1007 | +2019.676 | Financial Services | +0.130 | +0.000 | +1.332 | +3.825 | -0.183 | +0.026 | +7.890 | +0.022 | +17.768 | +0.774 | +0.981 |
| G1 | 2023 | 235 | +2023.000 | Technology | +0.145 | +0.000 | +1.468 | +3.481 | -0.214 | +0.025 | +7.834 | +0.028 | +28.613 | +0.966 | +0.864 |
| G1 | 2024-26 | 749 | +2024.790 | Healthcare | +0.135 | +0.005 | +1.319 | +3.797 | -0.214 | +0.032 | +7.814 | +0.088 | +27.753 | +0.857 | +0.814 |
| G2 | 2016-22 | 15602 | +2019.608 | Technology | +0.155 | +0.000 | +1.259 | +4.325 | -0.167 | +0.026 | +7.835 | +0.085 | +17.185 | +0.756 | +0.973 |
| G2 | 2023 | 4114 | +2023.000 | Technology | +0.151 | +0.003 | +1.281 | +4.207 | -0.195 | +0.028 | +7.659 | +0.103 | +25.760 | +0.946 | +0.835 |
| G2 | 2024-26 | 12248 | +2024.796 | Healthcare | +0.131 | +0.004 | +1.206 | +4.298 | -0.191 | +0.032 | +7.704 | +0.147 | +26.379 | +0.930 | +0.790 |
| G3 | 2016-22 | 61242 | +2020.704 | Healthcare | +0.200 | +0.000 | +0.585 | +6.504 | -0.463 | +0.036 | +7.177 | +0.008 | +8.146 | +0.521 | +0.826 |
| G3 | 2023 | 30437 | +2023.000 | İmalat | +0.182 | +0.001 | +0.612 | +6.370 | -0.468 | +0.038 | +7.016 | +0.040 | +11.973 | +0.928 | +0.675 |
| G3 | 2024-26 | 61578 | +2024.844 | İmalat | +0.279 | +0.001 | +0.474 | +6.154 | -0.485 | +0.041 | +6.970 | +0.036 | +13.216 | +0.965 | +0.573 |
| G4 | 2016-22 | 17971 | +2019.577 | Technology | +0.120 | +0.000 | +0.827 | +4.502 | -0.219 | +0.027 | +7.480 | +0.016 | +8.071 | +0.730 | +0.919 |
| G4 | 2023 | 4265 | +2023.000 | İmalat | +0.184 | +0.008 | +0.802 | +4.524 | -0.270 | +0.033 | +7.198 | +0.008 | +11.759 | +0.935 | +0.665 |
| G4 | 2024-26 | 10968 | +2024.781 | İmalat | +0.202 | +0.013 | +0.758 | +4.708 | -0.281 | +0.041 | +7.264 | +0.061 | +14.330 | +0.900 | +0.635 |
| G5 | 2016-22 | 1900 | +2019.718 | Healthcare | +0.120 | +0.000 | +0.834 | +4.618 | -0.260 | +0.028 | +7.483 | -0.049 | +8.405 | +0.737 | +0.907 |
| G5 | 2023 | 526 | +2023.000 | İmalat | +0.177 | +0.010 | +0.825 | +4.384 | -0.296 | +0.029 | +7.217 | -0.079 | +11.863 | +0.954 | +0.683 |
| G5 | 2024-26 | 1265 | +2024.794 | İmalat | +0.206 | +0.015 | +0.767 | +4.736 | -0.324 | +0.037 | +7.265 | -0.029 | +15.221 | +0.853 | +0.635 |

| grup | n | dd250_smd | vol60_smd | log_dv20_smd | r60_smd | kapsama_365_smd | boga_pay_fark | lt_ort_fark | vd_ort_fark |
|---|---|---|---|---|---|---|---|---|---|
| SMD G1 vs G2 | 31964 | -0.104 | -0.013 | +0.142 | -0.098 | +0.052 | -0.019 | +0.101 | -0.526 |
| SMD G1 vs G3 | 153257 | +1.558 | -0.332 | +1.233 | +0.037 | +0.709 | +0.048 | +0.797 | -2.562 |
| SMD G1 vs G4 | 33204 | +0.240 | -0.029 | +0.727 | +0.026 | +0.725 | +0.015 | +0.542 | -0.799 |
| SMD G1 vs G5 | 3691 | +0.433 | -0.109 | +0.723 | +0.149 | +0.677 | +0.020 | +0.534 | -0.851 |
| SMD G1 (eşleşen) vs eşleşmiş G5 | 121 | +0.045 | -0.013 | +0.014 | +0.208 | +0.255 | -0.002 | +0.033 | -0.112 |

## G1 − eşleşmiş G5 (negatif kontrol; nedensel kanıt değil)

| donem | n_a | isabet_a | isabet_b | delta | delta_alt | delta_ust | net_fark | p | karar_hucre | eslesen_pay |
|---|---|---|---|---|---|---|---|---|---|---|
| 2016-22 | 71 | +0.181 | +0.220 | -0.039 | -0.171 | +0.101 | -0.002 | +0.678 | TUTMAZ (bilgi) | +0.061 |
| 2023 | 17 |  |  |  |  |  |  |  | YETERSİZ ÖRNEKLEM | +0.061 |
| 2024-26 | 33 | +0.273 | +0.242 | +0.030 | -0.257 | +0.280 | +0.002 | +0.456 | TUTMAZ (bilgi) | +0.061 |

Eşleşme: aynı gün ±10 işlem günü, aynı oynaklık ondalığı ve likidite üçte biri, aynı trend işareti, |dd250 farkı| ≤ 0,10, sektör biliniyorsa aynı, en yakın 3 (standartlaştırılmış uzaklık). 'eslesen_pay' = eş bulunan G1 olayı payı.

## KGS-önce ve KGS-sonra

- KGS-önce (karar ölçüsü, T5): başlangıç d0−1 kapanışı. KGS-sonra (bilgi, EK 3): başlangıç d0 kapanışı; sonuçlar hücre tablosunda 'EK-KGS-sonra'. Kova ve eşik aynı; karar yalnız KGS-önce ile.
