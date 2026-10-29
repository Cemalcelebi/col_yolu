# ÇÖL YOLU — ABD araştırması (CY v1.1 (2026-10-29, K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil))

Süre 51.5 dk. Kurallar koşudan önce yazıldı (dosya başı, ÖN KAYIT).

## Veri

- ABD: {'hisse': 2752, 'panel_satir': 3175671, 'ilk': '2016-06-10', 'son': '2026-07-23', 'batan_hisse': 101}
- AVR: {'hisse': 561, 'panel_satir': 1144456, 'ilk': '2016-01-04', 'son': '2026-06-08', 'batan_hisse': 0}
- BIST: {'hisse': 574, 'panel_satir': 842132, 'ilk': '2016-05-30', 'son': '2026-06-05', 'batan_hisse': 0}
- havuz: {'egitim': 129398, 'dogrulama': 21637, 'egitim_isabet': 0.2061314731836319}

## Hipotez kararları

| Kod | Hipotez | Karar | Ayrıntı |
|---|---|---|---|
| H1 | Çöl Yolu oluşurken (P1) aynı gün aynı oynaklıktaki rastgeleden iyi (ABD) | **DESTEKLENMİYOR** | 2023: n 906, isabet 0.313, taban 0.288, fark +0.025 [-0.005], net -0.0183 (taban farkı +0.0009); 2024-26: n 1316, isabet 0.357, taban 0.333, fark +0.024 [+0.001], net -0.0109 (taban farkı -0.0010) |
| H3 | Kırılım (P2) rastgeleden iyi (ABD) | **DESTEKLENMİYOR** | 2023: n 476, isabet 0.286, taban 0.276, fark +0.010 [-0.024], net -0.0199 (taban farkı +0.0031); 2024-26: n 667, isabet 0.324, taban 0.318, fark +0.006 [-0.017], net -0.0209 (taban farkı -0.0045) |
| H2 | Sıkışma imzası fark yaratıyor: P1, aynı düşüş ve dipteki imzasız eşlerden iyi (ABD) | **DESTEKLENMİYOR** | 2023: fark +0.027 [-0.011, +0.065], n 906 / eş 896.0; 2024-26: fark +0.016 [-0.019, +0.054], n 1316 / eş 2382.0 |
| H4 | Meta-etiketleme P1 seçimini iyileştiriyor (ABD) | **DESTEKLENMİYOR** | 2023: seçilen n 172 / 906.0, isabet farkı +0.066 [-0.021], net farkı +0.0220, AUC 0.533 [0.461]; 2024-26: seçilen n 452 / 1316.0, isabet farkı +0.026 [-0.011], net farkı +0.0016, AUC 0.525 [0.482] |
| H5 | CNN P1 seçimini iyileştiriyor (ABD) | **DESTEKLENMİYOR** | 2023: seçilen n 617 / 906.0, isabet farkı +0.001 [-0.020], net farkı -0.0033, AUC 0.511 [0.466]; 2024-26: seçilen n 893 / 1316.0, isabet farkı -0.015 [-0.032], net farkı -0.0064, AUC 0.482 [0.449] |
| H6 | CNN ile sayısal model aynı adaylarda (AUC farkı; yön önceden yok) | **DESTEKLENMİYOR** | 2023: CNN - sayısal -0.050 [-0.124, +0.057]; 2024-26: CNN - sayısal -0.056 [-0.103, -0.005] (DESTEKLENİYOR = CNN daha iyi; DESTEKLENMİYOR = CNN üstün değil) |
| H7 | Meta portföyü maliyet sonrası piyasayı, rastgeleyi ve SPY'yi geçiyor (ABD) | **DESTEKLENMİYOR** | 2023: portföy +12.5% (MDD -19.9%, işlem 93, kazanma 44%), piyasa +18.6%, rastgele +0.5%, SPY +26.7%; 2024-26: portföy -29.5% (MDD -44.3%, işlem 308, kazanma 40%), piyasa +47.3%, rastgele -19.2%, SPY +67.7% |
| H8 | Aşırı uyum riski düşük: PBO < 0,5 ve seçilmiş yapının DSR >= 0,95 | **DESTEKLENMİYOR** | PBO 0.39 (12870 bölünme), DSR 0.03, seçilen P1|-0.35|60|0.8|3, ana P1|-0.35|60|0.8|3 |
| H9 | Hayatta kalma yanlılığı (batanlar çıkarılınca P1 farkı; bilgi) | **ÖLÇÜLEMEDİ** | 2023: batanlar dahil +0.025 (n 906), batansız +0.036 (n 864); 2024-26: batanlar dahil +0.024 (n 1316), batansız +0.024 (n 1293) |
| H10 | Çoğaltma AVR: P1 / P2 rastgeleden iyi (donmuş kurallar) | **DESTEKLENMİYOR** | P1 2023: n 145, isabet 0.207, taban 0.149, fark +0.058 [-0.007], net -0.0265 (taban farkı +0.0029); 2024-26: n 128, isabet 0.227, taban 0.201, fark +0.026 [-0.039], net -0.0223 (taban farkı -0.0101) | P2 2023: n 76, isabet 0.250, taban 0.148, fark +0.102 [+0.034], net -0.0153 (taban farkı +0.0116); 2024-26: n 59, isabet 0.153, taban 0.190, fark -0.038 [-0.117], net -0.0530 (taban farkı -0.0306) |
| H10-META | Çoğaltma AVR: ABD'de eğitilmiş meta model seçimi iyileştiriyor | **DESTEKLENMİYOR** | 2023: isabet farkı -0.060 [-0.165], n 34; 2024-26: isabet farkı +0.040 [-0.088], n 30 |
| H10-BIST | Çoğaltma BIST: P1 / P2 rastgeleden iyi (donmuş kurallar) | **DESTEKLENMİYOR** | P1 2023: n 126, isabet 0.611, taban 0.579, fark +0.032 [-0.077], net +0.0628 (taban farkı +0.0092); 2024-26: n 953, isabet 0.332, taban 0.346, fark -0.014 [-0.045], net -0.0101 (taban farkı -0.0072) | P2 2023: n 85, isabet 0.800, taban 0.818, fark -0.018 [-0.252], net +0.1196 (taban farkı -0.0059); 2024-26: n 355, isabet 0.287, taban 0.333, fark -0.046 [-0.103], net -0.0296 (taban farkı -0.0190) |
| H10-BIST-META | Çoğaltma BIST: ABD'de eğitilmiş meta model seçimi iyileştiriyor | **DESTEKLENMİYOR** | 2023: isabet farkı -0.236 [-0.309], n 48; 2024-26: isabet farkı -0.016 [-0.067], n 501 |
| SONUÇ | Çöl Yolu öngörü değeri (önceden yazılı kural) | **İZ DEĞİL** | ABD (H1/H3 ve H2): False; Avrupa çoğaltma (H10): False |

## Olay hücreleri (ana etiket +%20 / -%10 / 60 gün)

| Pazar | Küme | Dönem | n | İsabet | Taban | Fark [alt] | Net ort | Net-taban | Kazanma | Ort kazanç | Ort kayıp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | P1 | egitim | 505 | +0.299 | +0.280 | +0.019 [-0.018] | -0.0117 | -0.0057 | +0.38 | +0.164 | -0.121 |
| ABD | P1_batansiz | egitim | 505 | +0.299 | +0.280 | +0.019 [-0.017] | -0.0117 | -0.0057 | +0.38 | +0.164 | -0.121 |
| ABD | P1 | dogrulama | 910 | +0.279 | +0.262 | +0.017 [-0.010] | -0.0335 | +0.0013 | +0.30 | +0.174 | -0.125 |
| ABD | P1_batansiz | dogrulama | 883 | +0.274 | +0.259 | +0.015 [-0.009] | -0.0349 | +0.0010 | +0.30 | +0.173 | -0.125 |
| ABD | P1 | 2023 | 906 | +0.313 | +0.288 | +0.025 [-0.005] | -0.0183 | +0.0009 | +0.36 | +0.176 | -0.124 |
| ABD | P1_batansiz | 2023 | 864 | +0.319 | +0.283 | +0.036 [+0.003] | -0.0166 | +0.0051 | +0.36 | +0.175 | -0.124 |
| ABD | P1 | 2024-26 | 1316 | +0.357 | +0.333 | +0.024 [+0.001] | -0.0109 | -0.0010 | +0.38 | +0.181 | -0.130 |
| ABD | P1_batansiz | 2024-26 | 1293 | +0.360 | +0.336 | +0.024 [-0.004] | -0.0109 | -0.0008 | +0.38 | +0.181 | -0.130 |
| ABD | P2 | egitim | 261 | +0.268 | +0.297 | -0.028 [-0.085] | -0.0167 | -0.0165 | +0.37 | +0.153 | -0.116 |
| ABD | P2 | dogrulama | 310 | +0.245 | +0.246 | -0.001 [-0.026] | -0.0264 | +0.0075 | +0.30 | +0.173 | -0.121 |
| ABD | P2 | 2023 | 476 | +0.286 | +0.276 | +0.010 [-0.024] | -0.0199 | +0.0031 | +0.37 | +0.157 | -0.123 |
| ABD | P2 | 2024-26 | 667 | +0.324 | +0.318 | +0.006 [-0.017] | -0.0209 | -0.0045 | +0.36 | +0.172 | -0.128 |
| ABD | ES | egitim | 782 | +0.332 | +0.327 | +0.006 [-0.021] | -0.0046 | -0.0075 | +0.40 | +0.167 | -0.121 |
| ABD | ES | dogrulama | 1534 | +0.284 | +0.271 | +0.013 [-0.015] | -0.0355 | -0.0026 | +0.31 | +0.168 | -0.128 |
| ABD | ES | 2023 | 896 | +0.311 | +0.313 | -0.002 [-0.028] | -0.0214 | -0.0061 | +0.36 | +0.169 | -0.126 |
| ABD | ES | 2024-26 | 2382 | +0.342 | +0.334 | +0.008 [-0.016] | -0.0069 | +0.0026 | +0.38 | +0.186 | -0.128 |
| AVR | P1 | egitim | 214 | +0.327 | +0.235 | +0.092 [+0.025] | +0.0162 | +0.0109 | +0.50 | +0.149 | -0.114 |
| AVR | P1 | dogrulama | 140 | +0.264 | +0.206 | +0.058 [-0.025] | -0.0165 | +0.0021 | +0.36 | +0.151 | -0.110 |
| AVR | P1 | 2023 | 145 | +0.207 | +0.149 | +0.058 [-0.007] | -0.0265 | +0.0029 | +0.33 | +0.131 | -0.105 |
| AVR | P1 | 2024-26 | 128 | +0.227 | +0.201 | +0.026 [-0.039] | -0.0223 | -0.0101 | +0.33 | +0.147 | -0.105 |
| AVR | P2 | egitim | 145 | +0.234 | +0.227 | +0.007 [-0.060] | +0.0064 | -0.0011 | +0.50 | +0.127 | -0.113 |
| AVR | P2 | dogrulama | 50 | +0.220 | +0.238 | -0.018 [-0.082] | -0.0103 | -0.0100 | +0.42 | +0.126 | -0.109 |
| AVR | P2 | 2023 | 76 | +0.250 | +0.148 | +0.102 [+0.034] | -0.0153 | +0.0116 | +0.34 | +0.148 | -0.100 |
| AVR | P2 | 2024-26 | 59 | +0.153 | +0.190 | -0.038 [-0.117] | -0.0530 | -0.0306 | +0.24 | +0.156 | -0.118 |
| AVR | ES | egitim | 365 | +0.268 | +0.242 | +0.027 [-0.012] | +0.0032 | -0.0013 | +0.45 | +0.140 | -0.109 |
| AVR | ES | dogrulama | 355 | +0.282 | +0.238 | +0.044 [+0.002] | -0.0061 | +0.0061 | +0.42 | +0.144 | -0.116 |
| AVR | ES | 2023 | 136 | +0.228 | +0.220 | +0.007 [-0.051] | -0.0141 | -0.0039 | +0.35 | +0.150 | -0.104 |
| AVR | ES | 2024-26 | 300 | +0.230 | +0.234 | -0.004 [-0.052] | -0.0179 | -0.0107 | +0.38 | +0.138 | -0.113 |
| BIST | P1 | egitim | 727 | +0.388 | +0.356 | +0.032 [-0.005] | +0.0233 | +0.0076 | +0.50 | +0.157 | -0.109 |
| BIST | P1 | dogrulama | 541 | +0.497 | +0.491 | +0.006 [-0.026] | +0.0494 | +0.0033 | +0.56 | +0.172 | -0.106 |
| BIST | P1 | 2023 | 126 | +0.611 | +0.579 | +0.032 [-0.077] | +0.0628 | +0.0092 | +0.61 | +0.180 | -0.122 |
| BIST | P1 | 2024-26 | 953 | +0.332 | +0.346 | -0.014 [-0.045] | -0.0101 | -0.0072 | +0.37 | +0.172 | -0.115 |
| BIST | P2 | egitim | 318 | +0.384 | +0.409 | -0.025 [-0.091] | +0.0098 | -0.0163 | +0.43 | +0.171 | -0.114 |
| BIST | P2 | dogrulama | 256 | +0.492 | +0.535 | -0.043 [-0.111] | +0.0348 | -0.0164 | +0.51 | +0.181 | -0.118 |
| BIST | P2 | 2023 | 85 | +0.800 | +0.818 | -0.018 [-0.252] | +0.1196 | -0.0059 | +0.80 | +0.181 | -0.124 |
| BIST | P2 | 2024-26 | 355 | +0.287 | +0.333 | -0.046 [-0.103] | -0.0296 | -0.0190 | +0.30 | +0.178 | -0.121 |
| BIST | ES | egitim | 642 | +0.371 | +0.361 | +0.010 [-0.029] | +0.0133 | +0.0058 | +0.46 | +0.160 | -0.110 |
| BIST | ES | dogrulama | 232 | +0.466 | +0.452 | +0.013 [-0.046] | +0.0238 | +0.0022 | +0.49 | +0.176 | -0.121 |
| BIST | ES | 2023 | 115 | +0.583 | +0.572 | +0.010 [-0.082] | +0.0522 | +0.0045 | +0.58 | +0.180 | -0.126 |
| BIST | ES | 2024-26 | 542 | +0.382 | +0.388 | -0.006 [-0.067] | +0.0000 | -0.0045 | +0.41 | +0.173 | -0.120 |
| ABD | P1_META | dogrulama | 455 | +0.308 | +0.273 | +0.035 [-0.005] | -0.0244 | +0.0067 | +0.33 | +0.173 | -0.124 |
| ABD | P1_GENEL | dogrulama | 273 | +0.322 | +0.289 | +0.034 [-0.023] | -0.0229 | +0.0078 | +0.34 | +0.181 | -0.127 |
| ABD | P1_CNN | dogrulama | 637 | +0.284 | +0.264 | +0.020 [-0.011] | -0.0317 | +0.0030 | +0.31 | +0.176 | -0.126 |
| ABD | P1_META | 2023 | 172 | +0.384 | +0.340 | +0.044 [-0.007] | +0.0059 | +0.0056 | +0.42 | +0.184 | -0.122 |
| ABD | P1_GENEL | 2023 | 194 | +0.345 | +0.306 | +0.039 [-0.016] | -0.0098 | +0.0112 | +0.37 | +0.191 | -0.128 |
| ABD | P1_CNN | 2023 | 617 | +0.319 | +0.294 | +0.025 [-0.004] | -0.0195 | -0.0007 | +0.35 | +0.179 | -0.125 |
| ABD | P1_META | 2024-26 | 452 | +0.385 | +0.354 | +0.030 [-0.005] | -0.0091 | -0.0010 | +0.40 | +0.178 | -0.134 |
| ABD | P1_GENEL | 2024-26 | 260 | +0.381 | +0.376 | +0.005 [-0.040] | -0.0123 | -0.0070 | +0.39 | +0.181 | -0.135 |
| ABD | P1_CNN | 2024-26 | 893 | +0.344 | +0.334 | +0.010 [-0.017] | -0.0171 | -0.0055 | +0.37 | +0.178 | -0.130 |
| AVR | P1_META | dogrulama | 78 | +0.282 | +0.205 | +0.078 [-0.023] | -0.0124 | +0.0072 | +0.37 | +0.153 | -0.111 |
| AVR | P1_GENEL | dogrulama | 20 | +0.200 | +0.160 | +0.040 [-0.139] | -0.0420 | +0.0030 | +0.25 | +0.150 | -0.106 |
| AVR | P1_CNN | dogrulama | 91 | +0.264 | +0.187 | +0.077 [-0.000] | -0.0219 | +0.0048 | +0.34 | +0.151 | -0.111 |
| AVR | P1_META | 2023 | 34 | +0.147 | +0.142 | +0.005 [-0.135] | -0.0490 | -0.0128 | +0.29 | +0.110 | -0.115 |
| AVR | P1_GENEL | 2023 | 36 | +0.222 | +0.156 | +0.067 [-0.091] | -0.0168 | +0.0192 | +0.44 | +0.113 | -0.121 |
| AVR | P1_CNN | 2023 | 90 | +0.167 | +0.141 | +0.026 [-0.040] | -0.0408 | -0.0076 | +0.29 | +0.123 | -0.107 |
| AVR | P1_META | 2024-26 | 30 | +0.267 | +0.222 | +0.044 [-0.096] | -0.0205 | -0.0165 | +0.27 | +0.185 | -0.095 |
| AVR | P1_GENEL | 2024-26 | 19 | +0.211 | +0.265 | -0.055 [-0.207] | -0.0415 | -0.0394 | +0.26 | +0.157 | -0.112 |
| AVR | P1_CNN | 2024-26 | 78 | +0.231 | +0.201 | +0.030 [-0.062] | -0.0261 | -0.0099 | +0.32 | +0.146 | -0.107 |
| BIST | P1_META | dogrulama | 245 | +0.510 | +0.491 | +0.019 [-0.016] | +0.0545 | +0.0041 | +0.58 | +0.171 | -0.104 |
| BIST | P1_GENEL | dogrulama | 90 | +0.422 | +0.420 | +0.002 [-0.084] | +0.0352 | +0.0064 | +0.52 | +0.160 | -0.101 |
| BIST | P1_CNN | dogrulama | 386 | +0.505 | +0.476 | +0.029 [-0.008] | +0.0513 | +0.0095 | +0.57 | +0.172 | -0.107 |
| BIST | P1_META | 2023 | 48 | +0.375 | +0.414 | -0.039 [-0.171] | -0.0075 | -0.0118 | +0.38 | +0.180 | -0.120 |
| BIST | P1_GENEL | 2023 | 45 | +0.511 | +0.496 | +0.016 [-0.137] | +0.0331 | +0.0045 | +0.51 | +0.179 | -0.120 |
| BIST | P1_CNN | 2023 | 94 | +0.617 | +0.599 | +0.018 [-0.075] | +0.0639 | +0.0046 | +0.62 | +0.180 | -0.123 |
| BIST | P1_META | 2024-26 | 501 | +0.315 | +0.354 | -0.039 [-0.079] | -0.0134 | -0.0138 | +0.35 | +0.170 | -0.113 |
| BIST | P1_GENEL | 2024-26 | 76 | +0.355 | +0.390 | -0.034 [-0.118] | -0.0091 | -0.0153 | +0.36 | +0.183 | -0.115 |
| BIST | P1_CNN | 2024-26 | 703 | +0.340 | +0.354 | -0.014 [-0.048] | -0.0092 | -0.0080 | +0.37 | +0.175 | -0.116 |

## Portföy (10 yuva, günde en çok 2 giriş, üçlü bariyer çıkışı, maliyetli)

| Pazar | Dönem | Strateji | Toplam | Yıllık | MDD | İşlem | Kazanma | Ort işlem | Ort kazanç | Ort kayıp | Piyasa (EA) | Piyasa MDD | Rastgele | Endeks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2023 | P1_hepsi | -0.026 | -0.027 | -0.389 | 131 | +0.39 | -0.0021 | +0.186 | -0.122 | +0.186 | -0.200 | +0.005 | SPY +0.267, IWM +0.175 |
| ABD | 2023 | P1_META | +0.125 | +0.127 | -0.199 | 93 | +0.44 | +0.0175 | +0.192 | -0.120 | +0.186 | -0.200 | +0.005 | SPY +0.267, IWM +0.175 |
| ABD | 2023 | P1_GENEL | -0.196 | -0.199 | -0.398 | 114 | +0.35 | -0.0174 | +0.184 | -0.126 | +0.186 | -0.200 | +0.005 | SPY +0.267, IWM +0.175 |
| ABD | 2023 | P1_CNN | +0.049 | +0.049 | -0.271 | 128 | +0.43 | +0.0038 | +0.171 | -0.122 | +0.186 | -0.200 | +0.005 | SPY +0.267, IWM +0.175 |
| ABD | 2023 | P2_hepsi | +0.060 | +0.061 | -0.238 | 98 | +0.47 | +0.0093 | +0.153 | -0.118 | +0.186 | -0.200 | +0.005 | SPY +0.267, IWM +0.175 |
| ABD | 2024-26 | P1_hepsi | -0.483 | -0.220 | -0.557 | 362 | +0.37 | -0.0161 | +0.171 | -0.126 | +0.473 | -0.274 | -0.192 | SPY +0.677, IWM +0.523 |
| ABD | 2024-26 | P1_META | -0.295 | -0.123 | -0.443 | 308 | +0.40 | -0.0094 | +0.173 | -0.133 | +0.473 | -0.274 | -0.192 | SPY +0.677, IWM +0.523 |
| ABD | 2024-26 | P1_GENEL | -0.112 | -0.044 | -0.285 | 206 | +0.42 | -0.0042 | +0.173 | -0.131 | +0.473 | -0.274 | -0.192 | SPY +0.677, IWM +0.523 |
| ABD | 2024-26 | P1_CNN | -0.476 | -0.216 | -0.528 | 353 | +0.37 | -0.0165 | +0.173 | -0.127 | +0.473 | -0.274 | -0.192 | SPY +0.677, IWM +0.523 |
| ABD | 2024-26 | P2_hepsi | -0.296 | -0.124 | -0.362 | 300 | +0.39 | -0.0101 | +0.167 | -0.123 | +0.473 | -0.274 | -0.192 | SPY +0.677, IWM +0.523 |
| AVR | 2023 | P1_hepsi | -0.180 | -0.182 | -0.276 | 69 | +0.30 | -0.0319 | +0.135 | -0.105 | +0.159 | -0.117 | -0.036 | STOXX +0.103 |
| AVR | 2023 | P1_META | -0.167 | -0.169 | -0.186 | 33 | +0.27 | -0.0534 | +0.106 | -0.113 | +0.159 | -0.117 | -0.036 | STOXX +0.103 |
| AVR | 2023 | P1_GENEL | -0.090 | -0.091 | -0.119 | 33 | +0.39 | -0.0278 | +0.112 | -0.118 | +0.159 | -0.117 | -0.036 | STOXX +0.103 |
| AVR | 2023 | P1_CNN | -0.164 | -0.166 | -0.224 | 60 | +0.33 | -0.0328 | +0.116 | -0.107 | +0.159 | -0.117 | -0.036 | STOXX +0.103 |
| AVR | 2023 | P2_hepsi | +0.018 | +0.018 | -0.171 | 46 | +0.37 | +0.0007 | +0.158 | -0.091 | +0.159 | -0.117 | -0.036 | STOXX +0.103 |
| AVR | 2024-26 | P1_hepsi | -0.231 | -0.094 | -0.324 | 105 | +0.33 | -0.0248 | +0.140 | -0.107 | +0.361 | -0.142 | +0.032 | STOXX +0.381 |
| AVR | 2024-26 | P1_META | -0.061 | -0.024 | -0.106 | 30 | +0.27 | -0.0203 | +0.182 | -0.094 | +0.361 | -0.142 | +0.032 | STOXX +0.381 |
| AVR | 2024-26 | P1_GENEL | -0.076 | -0.029 | -0.083 | 19 | +0.26 | -0.0409 | +0.154 | -0.111 | +0.361 | -0.142 | +0.032 | STOXX +0.381 |
| AVR | 2024-26 | P1_CNN | -0.170 | -0.068 | -0.256 | 69 | +0.33 | -0.0247 | +0.141 | -0.107 | +0.361 | -0.142 | +0.032 | STOXX +0.381 |
| AVR | 2024-26 | P2_hepsi | -0.266 | -0.110 | -0.283 | 58 | +0.24 | -0.0511 | +0.153 | -0.116 | +0.361 | -0.142 | +0.032 | STOXX +0.381 |
| BIST | 2023 | P1_hepsi | +0.050 | +0.050 | -0.169 | 66 | +0.47 | +0.0189 | +0.176 | -0.120 | +0.182 | -0.393 | -0.224 | XU100_IS +0.320 |
| BIST | 2023 | P1_META | -0.171 | -0.173 | -0.190 | 40 | +0.33 | -0.0229 | +0.175 | -0.118 | +0.182 | -0.393 | -0.224 | XU100_IS +0.320 |
| BIST | 2023 | P1_GENEL | -0.045 | -0.046 | -0.190 | 35 | +0.46 | +0.0159 | +0.174 | -0.117 | +0.182 | -0.393 | -0.224 | XU100_IS +0.320 |
| BIST | 2023 | P1_CNN | +0.063 | +0.064 | -0.182 | 59 | +0.49 | +0.0248 | +0.175 | -0.120 | +0.182 | -0.393 | -0.224 | XU100_IS +0.320 |
| BIST | 2023 | P2_hepsi | +0.281 | +0.285 | -0.052 | 38 | +0.66 | +0.0723 | +0.174 | -0.122 | +0.182 | -0.393 | -0.224 | XU100_IS +0.320 |
| BIST | 2024-26 | P1_hepsi | -0.047 | -0.018 | -0.359 | 223 | +0.41 | +0.0015 | +0.163 | -0.112 | +0.900 | -0.201 | +0.140 | XU100_IS +0.920 |
| BIST | 2024-26 | P1_META | -0.285 | -0.118 | -0.351 | 189 | +0.35 | -0.0144 | +0.165 | -0.113 | +0.900 | -0.201 | +0.140 | XU100_IS +0.920 |
| BIST | 2024-26 | P1_GENEL | -0.067 | -0.026 | -0.216 | 59 | +0.36 | -0.0103 | +0.178 | -0.115 | +0.900 | -0.201 | +0.140 | XU100_IS +0.920 |
| BIST | 2024-26 | P1_CNN | -0.002 | -0.001 | -0.380 | 218 | +0.42 | +0.0037 | +0.171 | -0.116 | +0.900 | -0.201 | +0.140 | XU100_IS +0.920 |
| BIST | 2024-26 | P2_hepsi | -0.477 | -0.216 | -0.528 | 210 | +0.31 | -0.0284 | +0.176 | -0.120 | +0.900 | -0.201 | +0.140 | XU100_IS +0.920 |

## Parametre arama ve aşırı uyum

- {'pbo': 0.3883449883449883, 'kombinasyon': 12870, 'logit_medyan': 0.3829922522561059, 'dsr_dsr': 0.02621534701881528, 'dsr_sr': -0.05527506023645401, 'dsr_sr0': 0.1600988534722287, 'dsr_T': 84, 'dsr_N': 36, 'secilen_yapi': 'P1|-0.35|60|0.8|3', 'ana_yapi': 'P1|-0.35|60|0.8|3'}
- Meta seçim: {'pay': 0.5, 'p': 0.3303529585412348, 'yillik': [{'yil': 2021, 'egitim_n': 488, 'egitim_isabet': 0.29713115096092224, 'test_n': 271}, {'yil': 2022, 'egitim_n': 762, 'egitim_isabet': 0.2979002594947815, 'test_n': 639}, {'yil': 2023, 'egitim_n': 1332, 'egitim_isabet': 0.2680180072784424, 'test_n': 906}, {'yil': 2024, 'egitim_n': 2276, 'egitim_isabet': 0.29393672943115234, 'test_n': 486}, {'yil': 2025, 'egitim_n': 2778, 'egitim_isabet': 0.3088552951812744, 'test_n': 586}, {'yil': 2026, 'egitim_n': 3335, 'egitim_isabet': 0.3205397427082062, 'test_n': 244}]}; genel: {'pay': 0.3, 'p': 0.4795426008937907}; CNN: {'pay': 0.7, 'p': 0.1487518861889839}
- CNN epoch kaydı: [{'epoch': 1, 'egitim_kayip': 0.5421214964257545, 'dogrulama_kayip': 0.5238483548164368, 'sure_sn': 682}, {'epoch': 2, 'egitim_kayip': 0.5112528750967539, 'dogrulama_kayip': 0.5398319363594055, 'sure_sn': 645}, {'epoch': 3, 'egitim_kayip': 0.5016908885148447, 'dogrulama_kayip': 0.5347580909729004, 'sure_sn': 683}]

## Notlar


## v1.1 — birleştirilmiş plan (model merdiveni, katkı, kontroller)

| Kod | Hipotez | Karar | Ayrıntı |
|---|---|---|---|
| B2 | Önceki aday 'ABD hacimli taban' üçlü bariyerde rastgeleden iyi | **DESTEKLENMİYOR** | 2023: n 58, isabet 0.276, taban 0.331, fark -0.055 [-0.147], net -0.0445; 2024-26: n 191, isabet 0.331, taban 0.343, fark -0.012 [-0.059], net -0.0274 |
| B1 | P1 oynaklığa bağlı bariyerle rastgeleden iyi | **DESTEKLENMİYOR** | 2023: n 906, fark +0.026 [-0.007]; 2024-26: n 1316, fark +0.043 [+0.016] |
| B1-P2 | P2 oynaklığa bağlı bariyerle rastgeleden iyi | **DESTEKLENMİYOR** | 2023: n 476, fark +0.021 [-0.007]; 2024-26: n 667, fark +0.034 [+0.007] |
| B1-belirsiz | P1 belirsiz mumlar çıkarılınca da rastgeleden iyi (sıra uydurulmadan) | **DESTEKLENMİYOR** | 2023: n 906, fark +0.025 [-0.006], belirsiz payı 0.000; 2024-26: n 1316, fark +0.024 [-0.000], belirsiz payı 0.000 |
| B4-P1-LR | P1: lojistik referans modeli adayları iyileştiriyor | **DESTEKLENMİYOR** | 2023: seçilen 99/906, precision 0.404 (taban 0.318), AUC 0.534, net fark +0.0239; 2024-26: seçilen 134/1316, precision 0.358 (taban 0.359), AUC 0.539, net fark -0.0054 |
| B4-P1-GBM | P1: ağaç modeli lojistik modeli geçiyor | **DESTEKLENMİYOR** | 2023: AUC farkı +0.008 [-0.038, +0.054]; 2024-26: AUC farkı -0.036 [-0.061, -0.011] |
| B4-P1-CNN | P1: CNN sayısal modelin üstüne bilgi ekliyor | **DESTEKLENMİYOR** | 2023: -0.013 [-0.065, +0.058]; 2024-26: -0.022 [-0.064, +0.027] |
| B4-P1-LSTM | P1: LSTM sayısal modelin üstüne bilgi ekliyor | **DESTEKLENMİYOR** | 2023: +0.029 [-0.050, +0.098]; 2024-26: +0.021 [-0.022, +0.070] |
| B5-P1-mum | P1: 'mum' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC -0.001 [-0.018], yalnız grup AUC 0.506; 2024-26: tam - çıkarılmış AUC -0.015 [-0.032], yalnız grup AUC 0.490 |
| B5-P1-oynaklik | P1: 'oynaklik' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.002 [-0.024], yalnız grup AUC 0.482; 2024-26: tam - çıkarılmış AUC +0.002 [-0.013], yalnız grup AUC 0.512 |
| B5-P1-hacim | P1: 'hacim' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC -0.013 [-0.030], yalnız grup AUC 0.473; 2024-26: tam - çıkarılmış AUC +0.003 [-0.017], yalnız grup AUC 0.484 |
| B5-P1-akis | P1: 'akis' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC -0.004 [-0.020], yalnız grup AUC 0.504; 2024-26: tam - çıkarılmış AUC -0.002 [-0.016], yalnız grup AUC 0.496 |
| B5-P1-trend | P1: 'trend' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.002 [-0.009], yalnız grup AUC 0.529; 2024-26: tam - çıkarılmış AUC +0.003 [-0.010], yalnız grup AUC 0.521 |
| B5-P1-momentum_dusus | P1: 'momentum_dusus' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.009 [-0.010], yalnız grup AUC 0.503; 2024-26: tam - çıkarılmış AUC +0.012 [-0.003], yalnız grup AUC 0.502 |
| B5-P1-likidite_piyasa | P1: 'likidite_piyasa' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.020 [-0.022], yalnız grup AUC 0.562; 2024-26: tam - çıkarılmış AUC +0.011 [-0.011], yalnız grup AUC 0.522 |
| B5-P1-col | P1: 'col' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC -0.010 [-0.032], yalnız grup AUC 0.514; 2024-26: tam - çıkarılmış AUC +0.010 [-0.005], yalnız grup AUC 0.489 |
| B4-P1-ZİNCİR | P1: sisteme alınan en üst model basamağı (karmaşık model yalnız bir alttakini geçerse) | **ÖLÇÜLEMEDİ** | birincil kural |
| B4-P2-LR | P2: lojistik referans modeli adayları iyileştiriyor | **DESTEKLENMİYOR** | 2023: seçilen 130/476, precision 0.392 (taban 0.286), AUC 0.595, net fark +0.0240; 2024-26: seçilen 441/667, precision 0.338 (taban 0.327), AUC 0.517, net fark -0.0014 |
| B4-P2-GBM | P2: ağaç modeli lojistik modeli geçiyor | **DESTEKLENMİYOR** | 2023: AUC farkı +0.025 [-0.034, +0.087]; 2024-26: AUC farkı +0.007 [-0.032, +0.050] |
| B4-P2-CNN | P2: CNN sayısal modelin üstüne bilgi ekliyor | **DESTEKLENMİYOR** | 2023: -0.006 [-0.023, +0.012]; 2024-26: -0.006 [-0.020, +0.006] |
| B4-P2-LSTM | P2: LSTM sayısal modelin üstüne bilgi ekliyor | **DESTEKLENMİYOR** | 2023: -0.038 [-0.048, -0.026]; 2024-26: -0.005 [-0.021, +0.010] |
| B5-P2-mum | P2: 'mum' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.001 [-0.028], yalnız grup AUC 0.480; 2024-26: tam - çıkarılmış AUC +0.005 [-0.025], yalnız grup AUC 0.499 |
| B5-P2-oynaklik | P2: 'oynaklik' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.020 [-0.000], yalnız grup AUC 0.561; 2024-26: tam - çıkarılmış AUC -0.011 [-0.036], yalnız grup AUC 0.448 |
| B5-P2-hacim | P2: 'hacim' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.003 [-0.016], yalnız grup AUC 0.507; 2024-26: tam - çıkarılmış AUC +0.001 [-0.017], yalnız grup AUC 0.495 |
| B5-P2-akis | P2: 'akis' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.023 [-0.009], yalnız grup AUC 0.577; 2024-26: tam - çıkarılmış AUC +0.013 [-0.013], yalnız grup AUC 0.471 |
| B5-P2-trend | P2: 'trend' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.017 [+0.003], yalnız grup AUC 0.517; 2024-26: tam - çıkarılmış AUC -0.006 [-0.033], yalnız grup AUC 0.483 |
| B5-P2-momentum_dusus | P2: 'momentum_dusus' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.024 [+0.002], yalnız grup AUC 0.496; 2024-26: tam - çıkarılmış AUC +0.027 [-0.007], yalnız grup AUC 0.535 |
| B5-P2-likidite_piyasa | P2: 'likidite_piyasa' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.035 [-0.006], yalnız grup AUC 0.520; 2024-26: tam - çıkarılmış AUC +0.002 [-0.031], yalnız grup AUC 0.523 |
| B5-P2-col | P2: 'col' özellik grubu ek bilgi taşıyor | **DESTEKLENMİYOR** | 2023: tam - çıkarılmış AUC +0.006 [-0.021], yalnız grup AUC 0.497; 2024-26: tam - çıkarılmış AUC +0.003 [-0.019], yalnız grup AUC 0.503 |
| B4-P2-ZİNCİR | P2: sisteme alınan en üst model basamağı (karmaşık model yalnız bir alttakini geçerse) | **ÖLÇÜLEMEDİ** | birincil kural |
| B9-P1_hepsi | Sıkı portföy: P1_hepsi piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: -2.6% (MDD -38.9%, Sharpe 0.01, beta 1.24, alfa -30.4%) | piyasa +18.6%, eşleşik rastgele p90 +10.1%, SPY +26.7%; 2024-26: -48.3% (MDD -55.7%, Sharpe -0.82, beta 0.85, alfa -39.1%) | piyasa +47.3%, eşleşik rastgele p90 -21.6%, SPY +67.7% |
| B9-P2_hepsi | Sıkı portföy: P2_hepsi piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: +6.0% (MDD -23.8%, Sharpe 0.38, beta 1.06, alfa -18.3%) | piyasa +18.6%, eşleşik rastgele p90 +10.3%, SPY +26.7%; 2024-26: -29.6% (MDD -36.2%, Sharpe -0.47, beta 0.64, alfa -24.0%) | piyasa +47.3%, eşleşik rastgele p90 -9.2%, SPY +67.7% |
| B9-P1_p_GBM | Sıkı portföy: P1_p_GBM piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: -4.7% (MDD -33.7%, Sharpe -0.08, beta 1.25, alfa -32.9%) | piyasa +18.6%, eşleşik rastgele p90 +1.0%, SPY +26.7%; 2024-26: -36.5% (MDD -47.1%, Sharpe -0.52, beta 0.84, alfa -31.2%) | piyasa +47.3%, eşleşik rastgele p90 -2.7%, SPY +67.7% |
| B9-P1_Y_GC | Sıkı portföy: P1_Y_GC piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: +1.9% (MDD -27.6%, Sharpe 0.20, beta 1.20, alfa -25.1%) | piyasa +18.6%, eşleşik rastgele p90 -0.2%, SPY +26.7%; 2024-26: -49.9% (MDD -54.6%, Sharpe -0.96, beta 0.62, alfa -36.1%) | piyasa +47.3%, eşleşik rastgele p90 -17.9%, SPY +67.7% |
| B9-P2_p_GBM | Sıkı portföy: P2_p_GBM piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: +4.8% (MDD -12.4%, Sharpe 0.56, beta 0.19, alfa +0.6%) | piyasa +18.6%, eşleşik rastgele p90 +12.3%, SPY +26.7%; 2024-26: -27.6% (MDD -32.3%, Sharpe -0.68, beta 0.33, alfa -17.7%) | piyasa +47.3%, eşleşik rastgele p90 +1.8%, SPY +67.7% |
| B9-HT_hepsi | Sıkı portföy: HT_hepsi piyasa, eşleşik rastgele %90 ve SPY'yi geçiyor | **DESTEKLENMİYOR** | 2023: -20.9% (MDD -25.3%, Sharpe -2.15, beta 0.18, alfa -27.6%) | piyasa +18.6%, eşleşik rastgele p90 -4.5%, SPY +26.7%; 2024-26: -43.4% (MDD -49.7%, Sharpe -1.58, beta 0.11, alfa -22.9%) | piyasa +47.3%, eşleşik rastgele p90 -28.4%, SPY +67.7% |
| B8-PBO-model | Model x seçim payı seçiminde aşırı uyum riski düşük (PBO < 0,5; doğrulama ayları, 8 blok) | **DESTEKLENMİYOR** | PBO 0.57, 30 aday, 24 ay |
| B7-negatif_karisik_etiket | Kontrol: negatif_karisik_etiket (AUC ~0,5) | **DESTEKLENİYOR** | P1_negatif_karisik_etiket 2023: AUC 0.536 [0.482, 0.574]; P1_negatif_karisik_etiket 2024-26: AUC 0.506 [0.480, 0.541]; P2_negatif_karisik_etiket 2023: AUC 0.546 [0.504, 0.577]; P2_negatif_karisik_etiket 2024-26: AUC 0.519 [0.467, 0.559] |
| B7-pozitif_gelecek5_sizinti | Kontrol: pozitif_gelecek5_sizinti (AUC belirgin yüksek) | **DESTEKLENİYOR** | P1_pozitif_gelecek5_sizinti 2023: AUC 0.784 [0.749, 0.819]; P1_pozitif_gelecek5_sizinti 2024-26: AUC 0.828 [0.804, 0.849]; P2_pozitif_gelecek5_sizinti 2023: AUC 0.784 [0.747, 0.820]; P2_pozitif_gelecek5_sizinti 2024-26: AUC 0.785 [0.745, 0.830] |
| B7-plasebo | Kontrol: plasebo (aynı gün aynı oynaklık rastgele) farkı ~0 | **DESTEKLENİYOR** | egitim: fark -0.032 [-0.066, +0.007] n 505; dogrulama: fark +0.003 [-0.019, +0.025] n 910; 2023: fark -0.013 [-0.036, +0.016] n 906; 2024-26: fark +0.000 [-0.022, +0.020] n 1316 |
| B8 | Çoklu test (Holm): düzeltme sonrası anlamlı (p < 0,05) testler | **ÖLÇÜLEMEDİ** | 0 / 84 test;  |

### Etiket türleri, belirsiz mumlar, hacimli taban

| Küme | Dönem | Etiket | n | İsabet | Taban | Fark [alt] | Net | Belirsiz payı |
|---|---|---|---|---|---|---|---|---|
| P1_agirlikli | egitim | sabit_20_10_60 | 505 | +0.299 |  | +0.019 [] | -0.0117 |  |
| P1 | egitim | sabit_20_10_60 | 505 | +0.299 | +0.280 | +0.019 [-0.017] | -0.0117 |  |
| P1 | egitim | oynak_s_0.5s_60 | 505 | +0.311 | +0.289 | +0.022 [-0.008] | -0.0059 |  |
| P1_belirsizsiz | egitim | sabit_20_10_60 | 505 | +0.299 | +0.280 | +0.019 [-0.020] | -0.0117 | +0.000 |
| P1_agirlikli | dogrulama | sabit_20_10_60 | 910 | +0.279 |  | +0.017 [] | -0.0335 |  |
| P1 | dogrulama | sabit_20_10_60 | 910 | +0.279 | +0.262 | +0.017 [-0.009] | -0.0335 |  |
| P1 | dogrulama | oynak_s_0.5s_60 | 910 | +0.240 | +0.227 | +0.013 [-0.011] | -0.0455 |  |
| P1_belirsizsiz | dogrulama | sabit_20_10_60 | 910 | +0.279 | +0.262 | +0.017 [-0.010] | -0.0335 | +0.000 |
| P1_agirlikli | 2023 | sabit_20_10_60 | 906 | +0.313 |  | +0.025 [] | -0.0183 |  |
| P1 | 2023 | sabit_20_10_60 | 906 | +0.313 | +0.288 | +0.025 [-0.006] | -0.0183 |  |
| P1 | 2023 | oynak_s_0.5s_60 | 906 | +0.284 | +0.259 | +0.026 [-0.007] | -0.0202 |  |
| P1_belirsizsiz | 2023 | sabit_20_10_60 | 906 | +0.313 | +0.288 | +0.025 [-0.006] | -0.0183 | +0.000 |
| P1_agirlikli | 2024-26 | sabit_20_10_60 | 1316 | +0.357 |  | +0.024 [] | -0.0109 |  |
| P1 | 2024-26 | sabit_20_10_60 | 1316 | +0.357 | +0.333 | +0.024 [-0.001] | -0.0109 |  |
| P1 | 2024-26 | oynak_s_0.5s_60 | 1316 | +0.348 | +0.305 | +0.043 [+0.016] | +0.0034 |  |
| P1_belirsizsiz | 2024-26 | sabit_20_10_60 | 1316 | +0.357 | +0.333 | +0.024 [-0.000] | -0.0109 | +0.000 |
| P2 | egitim | sabit_20_10_60 | 261 | +0.268 | +0.297 | -0.028 [-0.085] | -0.0167 |  |
| P2 | egitim | oynak_s_0.5s_60 | 261 | +0.276 | +0.306 | -0.030 [-0.082] | -0.0120 |  |
| P2_belirsizsiz | egitim | sabit_20_10_60 | 261 | +0.268 | +0.297 | -0.028 [-0.085] | -0.0167 | +0.000 |
| P2_suren_kirilim | egitim | sabit_20_10_60 (BİLGİ: gelecek) | 109 | +0.358 | +0.351 | +0.007 [-0.075] | +0.0162 |  |
| P2_basarisiz_kirilim | egitim | sabit_20_10_60 (BİLGİ: gelecek) | 152 | +0.204 | +0.258 | -0.054 [-0.117] | -0.0403 |  |
| P2 | dogrulama | sabit_20_10_60 | 310 | +0.245 | +0.246 | -0.001 [-0.030] | -0.0264 |  |
| P2 | dogrulama | oynak_s_0.5s_60 | 310 | +0.179 | +0.212 | -0.033 [-0.073] | -0.0442 |  |
| P2_belirsizsiz | dogrulama | sabit_20_10_60 | 310 | +0.245 | +0.246 | -0.001 [-0.029] | -0.0264 | +0.000 |
| P2_suren_kirilim | dogrulama | sabit_20_10_60 (BİLGİ: gelecek) | 107 | +0.442 | +0.281 | +0.161 [+0.091] | +0.0605 |  |
| P2_basarisiz_kirilim | dogrulama | sabit_20_10_60 (BİLGİ: gelecek) | 203 | +0.137 | +0.227 | -0.090 [-0.127] | -0.0743 |  |
| P2 | 2023 | sabit_20_10_60 | 476 | +0.286 | +0.276 | +0.010 [-0.024] | -0.0199 |  |
| P2 | 2023 | oynak_s_0.5s_60 | 476 | +0.256 | +0.235 | +0.021 [-0.007] | -0.0218 |  |
| P2_belirsizsiz | 2023 | sabit_20_10_60 | 476 | +0.286 | +0.276 | +0.009 [-0.023] | -0.0199 | +0.000 |
| P2_suren_kirilim | 2023 | sabit_20_10_60 (BİLGİ: gelecek) | 196 | +0.453 | +0.327 | +0.126 [+0.069] | +0.0379 |  |
| P2_basarisiz_kirilim | 2023 | sabit_20_10_60 (BİLGİ: gelecek) | 280 | +0.170 | +0.241 | -0.070 [-0.125] | -0.0598 |  |
| P2 | 2024-26 | sabit_20_10_60 | 667 | +0.324 | +0.318 | +0.006 [-0.017] | -0.0209 |  |
| P2 | 2024-26 | oynak_s_0.5s_60 | 667 | +0.318 | +0.284 | +0.034 [+0.007] | +0.0037 |  |
| P2_belirsizsiz | 2024-26 | sabit_20_10_60 | 666 | +0.325 | +0.318 | +0.006 [-0.017] | -0.0207 | +0.001 |
| P2_suren_kirilim | 2024-26 | sabit_20_10_60 (BİLGİ: gelecek) | 254 | +0.545 | +0.356 | +0.190 [+0.129] | +0.0489 |  |
| P2_basarisiz_kirilim | 2024-26 | sabit_20_10_60 (BİLGİ: gelecek) | 413 | +0.189 | +0.295 | -0.106 [-0.143] | -0.0636 |  |
| ES | egitim | sabit_20_10_60 | 782 | +0.332 | +0.327 | +0.006 [-0.023] | -0.0046 |  |
| ES | egitim | oynak_s_0.5s_60 | 782 | +0.312 | +0.301 | +0.011 [-0.013] | +0.0097 |  |
| ES_belirsizsiz | egitim | sabit_20_10_60 | 782 | +0.332 | +0.327 | +0.006 [-0.021] | -0.0046 | +0.000 |
| ES | dogrulama | sabit_20_10_60 | 1534 | +0.284 | +0.271 | +0.013 [-0.015] | -0.0355 |  |
| ES | dogrulama | oynak_s_0.5s_60 | 1534 | +0.232 | +0.216 | +0.016 [-0.012] | -0.0441 |  |
| ES_belirsizsiz | dogrulama | sabit_20_10_60 | 1533 | +0.284 | +0.271 | +0.013 [-0.016] | -0.0354 | +0.001 |
| ES | 2023 | sabit_20_10_60 | 896 | +0.311 | +0.313 | -0.002 [-0.027] | -0.0214 |  |
| ES | 2023 | oynak_s_0.5s_60 | 896 | +0.259 | +0.266 | -0.006 [-0.029] | -0.0326 |  |
| ES_belirsizsiz | 2023 | sabit_20_10_60 | 896 | +0.311 | +0.313 | -0.003 [-0.028] | -0.0214 | +0.000 |
| ES | 2024-26 | sabit_20_10_60 | 2382 | +0.342 | +0.334 | +0.008 [-0.015] | -0.0069 |  |
| ES | 2024-26 | oynak_s_0.5s_60 | 2382 | +0.315 | +0.294 | +0.021 [-0.003] | +0.0082 |  |
| ES_belirsizsiz | 2024-26 | sabit_20_10_60 | 2380 | +0.342 | +0.334 | +0.008 [-0.016] | -0.0068 | +0.001 |
| HT | egitim | sabit_20_10_60 | 66 | +0.379 | +0.348 | +0.031 [-0.093] | +0.0214 |  |
| HT | egitim | oynak_s_0.5s_60 | 66 | +0.273 | +0.290 | -0.018 [-0.117] | +0.0404 |  |
| HT_belirsizsiz | egitim | sabit_20_10_60 | 66 | +0.379 | +0.348 | +0.031 [-0.088] | +0.0214 | +0.000 |
| HT | dogrulama | sabit_20_10_60 | 97 | +0.317 | +0.279 | +0.038 [-0.084] | -0.0336 |  |
| HT | dogrulama | oynak_s_0.5s_60 | 97 | +0.208 | +0.199 | +0.009 [-0.077] | -0.0639 |  |
| HT_belirsizsiz | dogrulama | sabit_20_10_60 | 97 | +0.317 | +0.280 | +0.038 [-0.082] | -0.0336 | +0.000 |
| HT | 2023 | sabit_20_10_60 | 58 | +0.276 | +0.331 | -0.055 [-0.147] | -0.0445 |  |
| HT | 2023 | oynak_s_0.5s_60 | 58 | +0.242 | +0.271 | -0.029 [-0.131] | +0.0527 |  |
| HT_belirsizsiz | 2023 | sabit_20_10_60 | 55 | +0.293 | +0.327 | -0.033 [-0.132] | -0.0389 | +0.052 |
| HT | 2024-26 | sabit_20_10_60 | 191 | +0.331 | +0.343 | -0.012 [-0.059] | -0.0274 |  |
| HT | 2024-26 | oynak_s_0.5s_60 | 191 | +0.207 | +0.254 | -0.048 [-0.095] | -0.0146 |  |
| HT_belirsizsiz | 2024-26 | sabit_20_10_60 | 187 | +0.338 | +0.341 | -0.004 [-0.054] | -0.0251 | +0.021 |
| HT | egitim | sabit_20_10_60 | 12 | +0.250 | +0.253 | -0.003 [-0.240] | +0.0036 |  |
| HT | egitim | oynak_s_0.5s_60 | 12 | +0.250 | +0.236 | +0.014 [-0.187] | +0.0242 |  |
| HT_belirsizsiz | egitim | sabit_20_10_60 | 12 | +0.250 | +0.253 | -0.003 [-0.240] | +0.0036 | +0.000 |
| HT | dogrulama | sabit_20_10_60 | 2 | +1.000 | +0.169 | +0.831 [] | +0.1858 |  |
| HT | dogrulama | oynak_s_0.5s_60 | 2 | +0.500 | +0.226 | +0.274 [] | +0.1772 |  |
| HT_belirsizsiz | dogrulama | sabit_20_10_60 | 2 | +1.000 | +0.169 | +0.831 [] | +0.1858 | +0.000 |
| HT | 2023 | sabit_20_10_60 | 3 | +0.333 | +0.391 | -0.058 [-0.283] | -0.0214 |  |
| HT | 2023 | oynak_s_0.5s_60 | 3 | +0.333 | +0.312 | +0.022 [-0.217] | +0.0039 |  |
| HT_belirsizsiz | 2023 | sabit_20_10_60 | 3 | +0.333 | +0.391 | -0.058 [-0.283] | -0.0214 | +0.000 |
| HT | 2024-26 | sabit_20_10_60 | 15 | +0.333 | +0.290 | +0.043 [-0.142] | +0.0087 |  |
| HT | 2024-26 | oynak_s_0.5s_60 | 15 | +0.133 | +0.224 | -0.091 [-0.230] | -0.0390 |  |
| HT_belirsizsiz | 2024-26 | sabit_20_10_60 | 15 | +0.333 | +0.290 | +0.043 [-0.134] | +0.0087 | +0.000 |
| HT | egitim | sabit_20_10_60 | 110 | +0.264 | +0.372 | -0.108 [-0.173] | -0.0366 |  |
| HT | egitim | oynak_s_0.5s_60 | 110 | +0.264 | +0.314 | -0.050 [-0.120] | -0.0370 |  |
| HT_belirsizsiz | egitim | sabit_20_10_60 | 110 | +0.264 | +0.372 | -0.108 [-0.174] | -0.0366 | +0.000 |
| HT | dogrulama | sabit_20_10_60 | 15 | +0.133 | +0.334 | -0.201 [-0.330] | -0.0909 |  |
| HT | dogrulama | oynak_s_0.5s_60 | 15 | +0.200 | +0.279 | -0.079 [-0.193] | -0.0761 |  |
| HT_belirsizsiz | dogrulama | sabit_20_10_60 | 15 | +0.133 | +0.334 | -0.201 [-0.333] | -0.0909 | +0.000 |
| HT | 2023 | sabit_20_10_60 | 6 | +0.000 | +0.161 | -0.161 [-0.259] | -0.1395 |  |
| HT | 2023 | oynak_s_0.5s_60 | 6 | +0.000 | +0.106 | -0.106 [-0.174] | -0.2077 |  |
| HT_belirsizsiz | 2023 | sabit_20_10_60 | 6 | +0.000 | +0.161 | -0.161 [-0.259] | -0.1395 | +0.000 |
| HT | 2024-26 | sabit_20_10_60 | 26 | +0.115 | +0.369 | -0.254 [-0.404] | -0.0945 |  |
| HT | 2024-26 | oynak_s_0.5s_60 | 26 | +0.115 | +0.329 | -0.214 [-0.346] | -0.1269 |  |
| HT_belirsizsiz | 2024-26 | sabit_20_10_60 | 26 | +0.115 | +0.369 | -0.254 [-0.400] | -0.0945 | +0.000 |
| P1 | egitim | sabit_20_10_60 | 214 | +0.327 | +0.235 | +0.092 [+0.027] | +0.0162 |  |
| P1 | egitim | oynak_s_0.5s_60 | 214 | +0.383 | +0.292 | +0.091 [+0.017] | +0.0188 |  |
| P1_belirsizsiz | egitim | sabit_20_10_60 | 214 | +0.327 | +0.235 | +0.092 [+0.024] | +0.0162 | +0.000 |
| P1 | dogrulama | sabit_20_10_60 | 140 | +0.264 | +0.206 | +0.058 [-0.030] | -0.0165 |  |
| P1 | dogrulama | oynak_s_0.5s_60 | 140 | +0.307 | +0.234 | +0.073 [-0.009] | -0.0115 |  |
| P1_belirsizsiz | dogrulama | sabit_20_10_60 | 140 | +0.264 | +0.206 | +0.058 [-0.029] | -0.0165 | +0.000 |
| P1 | 2023 | sabit_20_10_60 | 145 | +0.207 | +0.149 | +0.058 [-0.014] | -0.0265 |  |
| P1 | 2023 | oynak_s_0.5s_60 | 145 | +0.262 | +0.201 | +0.061 [-0.001] | -0.0262 |  |
| P1_belirsizsiz | 2023 | sabit_20_10_60 | 145 | +0.207 | +0.149 | +0.058 [-0.008] | -0.0265 | +0.000 |
| P1 | 2024-26 | sabit_20_10_60 | 128 | +0.227 | +0.201 | +0.026 [-0.041] | -0.0223 |  |
| P1 | 2024-26 | oynak_s_0.5s_60 | 128 | +0.266 | +0.261 | +0.005 [-0.066] | -0.0183 |  |
| P1_belirsizsiz | 2024-26 | sabit_20_10_60 | 128 | +0.227 | +0.201 | +0.026 [-0.038] | -0.0223 | +0.000 |
| P1 | egitim | sabit_20_10_60 | 727 | +0.388 | +0.356 | +0.032 [-0.010] | +0.0233 |  |
| P1 | egitim | oynak_s_0.5s_60 | 727 | +0.410 | +0.385 | +0.025 [-0.010] | +0.0143 |  |
| P1_belirsizsiz | egitim | sabit_20_10_60 | 727 | +0.388 | +0.356 | +0.032 [-0.007] | +0.0233 | +0.000 |
| P1 | dogrulama | sabit_20_10_60 | 541 | +0.497 | +0.491 | +0.006 [-0.026] | +0.0494 |  |
| P1 | dogrulama | oynak_s_0.5s_60 | 541 | +0.512 | +0.491 | +0.021 [-0.010] | +0.0395 |  |
| P1_belirsizsiz | dogrulama | sabit_20_10_60 | 541 | +0.497 | +0.491 | +0.006 [-0.027] | +0.0494 | +0.000 |
| P1 | 2023 | sabit_20_10_60 | 126 | +0.611 | +0.579 | +0.032 [-0.080] | +0.0628 |  |
| P1 | 2023 | oynak_s_0.5s_60 | 126 | +0.643 | +0.622 | +0.021 [-0.086] | +0.0955 |  |
| P1_belirsizsiz | 2023 | sabit_20_10_60 | 126 | +0.611 | +0.579 | +0.032 [-0.070] | +0.0628 | +0.000 |
| P1 | 2024-26 | sabit_20_10_60 | 953 | +0.332 | +0.346 | -0.014 [-0.046] | -0.0101 |  |
| P1 | 2024-26 | oynak_s_0.5s_60 | 953 | +0.326 | +0.352 | -0.025 [-0.060] | -0.0084 |  |
| P1_belirsizsiz | 2024-26 | sabit_20_10_60 | 953 | +0.332 | +0.346 | -0.014 [-0.046] | -0.0101 | +0.000 |

### Model merdiveni (seçim eşiği doğrulamada, 2021-22)

| Faz | Model | Dönem | Seçilen / hepsi | Precision | Taban | Recall | ROC-AUC [alt] | PR-AUC | Brier | Net seçilen | Net fark [alt] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | p_LR | dogrulama | 273 / 910 | +0.322 | +0.276 | +0.351 | +0.554 [+0.492] | +0.321 | +0.221 | -0.0242 | +0.0105 [-0.0071] |
| P1 | p_LR | 2023 | 99 / 906 | +0.404 | +0.318 | +0.139 | +0.534 [+0.471] | +0.352 | +0.232 | +0.0077 | +0.0239 [-0.0157] |
| P1 | p_LR | 2024-26 | 134 / 1316 | +0.358 | +0.359 | +0.102 | +0.539 [+0.498] | +0.388 | +0.241 | -0.0161 | -0.0054 [-0.0378] |
| P1 | p_GBM10 | dogrulama | 455 / 910 | +0.308 | +0.276 | +0.558 | +0.528 [+0.490] | +0.283 | +0.228 | -0.0244 | +0.0103 [+0.0014] |
| P1 | p_GBM10 | 2023 | 172 / 906 | +0.384 | +0.318 | +0.229 | +0.533 [+0.467] | +0.353 | +0.235 | +0.0059 | +0.0220 [-0.0052] |
| P1 | p_GBM10 | 2024-26 | 452 / 1316 | +0.385 | +0.359 | +0.369 | +0.525 [+0.482] | +0.376 | +0.240 | -0.0091 | +0.0016 [-0.0112] |
| P1 | p_GBM | dogrulama | 637 / 910 | +0.287 | +0.276 | +0.729 | +0.508 [+0.466] | +0.275 | +0.228 | -0.0309 | +0.0038 [-0.0017] |
| P1 | p_GBM | 2023 | 346 / 906 | +0.341 | +0.318 | +0.410 | +0.542 [+0.467] | +0.357 | +0.233 | -0.0063 | +0.0099 [-0.0073] |
| P1 | p_GBM | 2024-26 | 914 / 1316 | +0.364 | +0.359 | +0.706 | +0.504 [+0.470] | +0.364 | +0.244 | -0.0099 | +0.0009 [-0.0040] |
| P1 | cnn_p | dogrulama | 637 / 910 | +0.284 | +0.276 | +0.721 | +0.521 [+0.466] | +0.286 | +0.211 | -0.0317 | +0.0030 [-0.0030] |
| P1 | cnn_p | 2023 | 617 / 906 | +0.319 | +0.318 | +0.684 | +0.511 [+0.468] | +0.337 | +0.239 | -0.0195 | -0.0033 [-0.0108] |
| P1 | cnn_p | 2024-26 | 893 / 1316 | +0.344 | +0.359 | +0.650 | +0.482 [+0.446] | +0.353 | +0.267 | -0.0171 | -0.0064 [-0.0117] |
| P1 | lstm_p | dogrulama | 637 / 910 | +0.284 | +0.276 | +0.721 | +0.505 [+0.440] | +0.267 | +0.220 | -0.0391 | -0.0044 [-0.0133] |
| P1 | lstm_p | 2023 | 479 / 906 | +0.359 | +0.318 | +0.597 | +0.556 [+0.513] | +0.344 | +0.219 | -0.0159 | +0.0003 [-0.0110] |
| P1 | lstm_p | 2024-26 | 898 / 1316 | +0.376 | +0.359 | +0.716 | +0.524 [+0.474] | +0.369 | +0.235 | -0.0111 | -0.0003 [-0.0076] |
| P1 | Y_GC | dogrulama | 455 / 910 | +0.281 | +0.276 | +0.510 | +0.520 [+0.469] | +0.288 | +0.199 | -0.0326 | +0.0021 [-0.0075] |
| P1 | Y_GC | 2023 | 364 / 906 | +0.343 | +0.318 | +0.434 | +0.529 [+0.475] | +0.353 | +0.218 | -0.0109 | +0.0053 [-0.0063] |
| P1 | Y_GC | 2024-26 | 639 / 1316 | +0.340 | +0.359 | +0.460 | +0.482 [+0.447] | +0.355 | +0.238 | -0.0189 | -0.0082 [-0.0161] |
| P1 | Y_GL | dogrulama | 637 / 910 | +0.294 | +0.276 | +0.745 | +0.513 [+0.449] | +0.271 | +0.200 | -0.0359 | -0.0012 [-0.0107] |
| P1 | Y_GL | 2023 | 414 / 906 | +0.367 | +0.318 | +0.528 | +0.571 [+0.517] | +0.358 | +0.218 | -0.0125 | +0.0037 [-0.0112] |
| P1 | Y_GL | 2024-26 | 899 / 1316 | +0.367 | +0.359 | +0.699 | +0.525 [+0.478] | +0.374 | +0.237 | -0.0143 | -0.0036 [-0.0112] |
| P1 | Y_GCL | dogrulama | 455 / 910 | +0.303 | +0.276 | +0.550 | +0.535 [+0.471] | +0.296 | +0.199 | -0.0323 | +0.0023 [-0.0112] |
| P1 | Y_GCL | 2023 | 294 / 906 | +0.367 | +0.318 | +0.375 | +0.551 [+0.506] | +0.362 | +0.218 | -0.0095 | +0.0067 [-0.0111] |
| P1 | Y_GCL | 2024-26 | 631 / 1316 | +0.363 | +0.359 | +0.485 | +0.503 [+0.463] | +0.361 | +0.237 | -0.0150 | -0.0042 [-0.0141] |
| P1 | p_KARISIK | dogrulama | 273 / 910 | +0.278 | +0.276 | +0.303 | +0.478 [+0.427] | +0.268 | +0.231 | -0.0255 | +0.0092 [-0.0106] |
| P1 | p_KARISIK | 2023 | 74 / 906 | +0.324 | +0.318 | +0.083 | +0.536 [+0.480] | +0.343 | +0.228 | -0.0035 | +0.0126 [-0.0129] |
| P1 | p_KARISIK | 2024-26 | 125 / 1316 | +0.376 | +0.359 | +0.100 | +0.506 [+0.477] | +0.372 | +0.242 | -0.0126 | -0.0018 [-0.0227] |
| P1 | p_SIZINTI | dogrulama | 273 / 910 | +0.553 | +0.276 | +0.602 | +0.802 [+0.757] | +0.631 | +0.157 | +0.0532 | +0.0879 [+0.0718] |
| P1 | p_SIZINTI | 2023 | 198 / 906 | +0.646 | +0.318 | +0.444 | +0.784 [+0.747] | +0.660 | +0.169 | +0.0879 | +0.1040 [+0.0732] |
| P1 | p_SIZINTI | 2024-26 | 374 / 1316 | +0.693 | +0.359 | +0.549 | +0.828 [+0.804] | +0.738 | +0.162 | +0.0941 | +0.1048 [+0.0919] |
| P1 | p_GBM_oynak_etiket | dogrulama | 637 / 910 | +0.237 | +0.238 | +0.696 | +0.465 [+0.423] | +0.213 | +0.219 | -0.0505 | -0.0042 [-0.0121] |
| P1 | p_GBM_oynak_etiket | 2023 | 355 / 906 | +0.330 | +0.286 | +0.452 | +0.560 [+0.504] | +0.340 | +0.214 | +0.0019 | +0.0206 [-0.0062] |
| P1 | p_GBM_oynak_etiket | 2024-26 | 893 / 1316 | +0.353 | +0.353 | +0.679 | +0.501 [+0.477] | +0.361 | +0.244 | +0.0035 | -0.0019 [-0.0102] |
| P2 | p_LR | dogrulama | 155 / 310 | +0.284 | +0.235 | +0.603 | +0.560 [+0.467] | +0.292 | +0.201 | -0.0176 | +0.0154 [+0.0009] |
| P2 | p_LR | 2023 | 130 / 476 | +0.392 | +0.286 | +0.375 | +0.595 [+0.491] | +0.386 | +0.211 | +0.0045 | +0.0240 [-0.0085] |
| P2 | p_LR | 2024-26 | 441 / 667 | +0.338 | +0.327 | +0.683 | +0.517 [+0.460] | +0.344 | +0.235 | -0.0219 | -0.0014 [-0.0117] |
| P2 | p_GBM10 | dogrulama | 217 / 310 | +0.258 | +0.235 | +0.767 | +0.573 [+0.481] | +0.285 | +0.202 | -0.0266 | +0.0064 [-0.0056] |
| P2 | p_GBM10 | 2023 | 183 / 476 | +0.361 | +0.286 | +0.485 | +0.580 [+0.491] | +0.358 | +0.216 | -0.0055 | +0.0140 [-0.0066] |
| P2 | p_GBM10 | 2024-26 | 482 / 667 | +0.334 | +0.327 | +0.739 | +0.505 [+0.463] | +0.333 | +0.240 | -0.0205 | -0.0001 [-0.0044] |
| P2 | p_GBM | dogrulama | 93 / 310 | +0.366 | +0.235 | +0.466 | +0.643 [+0.555] | +0.334 | +0.184 | -0.0063 | +0.0267 [-0.0086] |
| P2 | p_GBM | 2023 | 37 / 476 | +0.432 | +0.286 | +0.118 | +0.620 [+0.527] | +0.373 | +0.218 | +0.0125 | +0.0320 [-0.0264] |
| P2 | p_GBM | 2024-26 | 182 / 667 | +0.346 | +0.327 | +0.289 | +0.524 [+0.463] | +0.341 | +0.236 | -0.0201 | +0.0004 [-0.0197] |
| P2 | cnn_p | dogrulama | 155 / 310 | +0.219 | +0.235 | +0.466 | +0.476 [+0.394] | +0.247 | +0.188 | -0.0316 | +0.0014 [-0.0169] |
| P2 | cnn_p | 2023 | 268 / 476 | +0.295 | +0.286 | +0.581 | +0.502 [+0.441] | +0.288 | +0.221 | -0.0211 | -0.0016 [-0.0127] |
| P2 | cnn_p | 2024-26 | 360 / 667 | +0.325 | +0.327 | +0.537 | +0.509 [+0.467] | +0.361 | +0.248 | -0.0262 | -0.0057 [-0.0154] |
| P2 | lstm_p | dogrulama | 217 / 310 | +0.249 | +0.235 | +0.740 | +0.513 [+0.442] | +0.232 | +0.195 | -0.0371 | -0.0040 [-0.0158] |
| P2 | lstm_p | 2023 | 265 / 476 | +0.358 | +0.286 | +0.699 | +0.606 [+0.563] | +0.345 | +0.199 | -0.0154 | +0.0041 [-0.0072] |
| P2 | lstm_p | 2024-26 | 513 / 667 | +0.324 | +0.327 | +0.761 | +0.524 [+0.479] | +0.359 | +0.224 | -0.0295 | -0.0090 [-0.0153] |
| P2 | Y_GC | dogrulama | 93 / 310 | +0.355 | +0.235 | +0.452 | +0.643 [+0.551] | +0.330 | +0.173 | -0.0107 | +0.0223 [-0.0130] |
| P2 | Y_GC | 2023 | 41 / 476 | +0.439 | +0.286 | +0.132 | +0.614 [+0.525] | +0.367 | +0.212 | +0.0245 | +0.0440 [-0.0114] |
| P2 | Y_GC | 2024-26 | 191 / 667 | +0.330 | +0.327 | +0.289 | +0.518 [+0.457] | +0.335 | +0.231 | -0.0198 | +0.0007 [-0.0176] |
| P2 | Y_GL | dogrulama | 93 / 310 | +0.376 | +0.235 | +0.479 | +0.652 [+0.561] | +0.341 | +0.173 | -0.0022 | +0.0308 [-0.0034] |
| P2 | Y_GL | 2023 | 50 / 476 | +0.400 | +0.286 | +0.147 | +0.582 [+0.496] | +0.338 | +0.215 | +0.0244 | +0.0439 [-0.0032] |
| P2 | Y_GL | 2024-26 | 167 / 667 | +0.353 | +0.327 | +0.271 | +0.518 [+0.464] | +0.337 | +0.231 | -0.0083 | +0.0122 [-0.0109] |
| P2 | Y_GCL | dogrulama | 93 / 310 | +0.355 | +0.235 | +0.452 | +0.653 [+0.558] | +0.334 | +0.173 | -0.0070 | +0.0260 [-0.0077] |
| P2 | Y_GCL | 2023 | 59 / 476 | +0.407 | +0.286 | +0.176 | +0.578 [+0.491] | +0.333 | +0.216 | +0.0294 | +0.0489 [+0.0031] |
| P2 | Y_GCL | 2024-26 | 188 / 667 | +0.319 | +0.327 | +0.275 | +0.514 [+0.449] | +0.332 | +0.232 | -0.0129 | +0.0075 [-0.0109] |
| P2 | p_KARISIK | dogrulama | 93 / 310 | +0.215 | +0.235 | +0.274 | +0.506 [+0.457] | +0.242 | +0.214 | -0.0117 | +0.0213 [-0.0110] |
| P2 | p_KARISIK | 2023 | 76 / 476 | +0.276 | +0.286 | +0.154 | +0.546 [+0.500] | +0.309 | +0.225 | -0.0293 | -0.0098 [-0.0409] |
| P2 | p_KARISIK | 2024-26 | 193 / 667 | +0.337 | +0.327 | +0.298 | +0.519 [+0.477] | +0.359 | +0.234 | -0.0280 | -0.0076 [-0.0240] |
| P2 | p_SIZINTI | dogrulama | 93 / 310 | +0.527 | +0.235 | +0.671 | +0.793 [+0.724] | +0.533 | +0.144 | +0.0473 | +0.0803 [+0.0542] |
| P2 | p_SIZINTI | 2023 | 88 / 476 | +0.670 | +0.286 | +0.434 | +0.784 [+0.738] | +0.596 | +0.176 | +0.0906 | +0.1101 [+0.0756] |
| P2 | p_SIZINTI | 2024-26 | 216 / 667 | +0.620 | +0.327 | +0.615 | +0.785 [+0.738] | +0.654 | +0.174 | +0.0687 | +0.0892 [+0.0683] |
| P2 | p_GBM_oynak_etiket | dogrulama | 155 / 310 | +0.200 | +0.174 | +0.574 | +0.562 [+0.458] | +0.221 | +0.161 | -0.0449 | +0.0050 [-0.0178] |
| P2 | p_GBM_oynak_etiket | 2023 | 97 / 476 | +0.330 | +0.256 | +0.262 | +0.567 [+0.518] | +0.317 | +0.207 | -0.0042 | +0.0178 [-0.0157] |
| P2 | p_GBM_oynak_etiket | 2024-26 | 386 / 667 | +0.339 | +0.321 | +0.612 | +0.539 [+0.501] | +0.362 | +0.231 | +0.0051 | -0.0004 [-0.0197] |

### katki

| faz | kiyas | donem | n | fark | alt | ust | p |
|---|---|---|---|---|---|---|---|
| P1 | GBM-LR | 2023 | 906 | +0.008 | -0.038 | +0.054 | +0.359 |
| P1 | GBM-GBM10 (v1.1 ölçüleri) | 2023 | 906 | +0.009 | -0.011 | +0.026 | +0.140 |
| P1 | CNN katkısı [G,C]-[G] | 2023 | 906 | -0.013 | -0.065 | +0.058 | +0.621 |
| P1 | LSTM katkısı [G,L]-[G] | 2023 | 906 | +0.029 | -0.050 | +0.098 | +0.219 |
| P1 | LSTM üstüne [G,C,L]-[G,C] | 2023 | 906 | +0.023 | -0.015 | +0.061 | +0.159 |
| P1 | CNN tek - GBM | 2023 | 906 | -0.031 | -0.098 | +0.070 | +0.757 |
| P1 | LSTM tek - GBM | 2023 | 906 | +0.014 | -0.084 | +0.110 | +0.395 |
| P1 | LR - rastgele(0,5) | 2023 | 906 | +0.034 | -0.035 | +0.092 |  |
| P1 | GBM-LR | 2024-26 | 1316 | -0.036 | -0.061 | -0.011 | +1.000 |
| P1 | GBM-GBM10 (v1.1 ölçüleri) | 2024-26 | 1316 | -0.021 | -0.049 | +0.006 | +0.937 |
| P1 | CNN katkısı [G,C]-[G] | 2024-26 | 1316 | -0.022 | -0.064 | +0.027 | +0.831 |
| P1 | LSTM katkısı [G,L]-[G] | 2024-26 | 1316 | +0.021 | -0.022 | +0.070 | +0.166 |
| P1 | LSTM üstüne [G,C,L]-[G,C] | 2024-26 | 1316 | +0.021 | -0.005 | +0.049 | +0.073 |
| P1 | CNN tek - GBM | 2024-26 | 1316 | -0.022 | -0.077 | +0.041 | +0.691 |
| P1 | LSTM tek - GBM | 2024-26 | 1316 | +0.020 | -0.039 | +0.085 | +0.286 |
| P1 | LR - rastgele(0,5) | 2024-26 | 1316 | +0.039 | +0.005 | +0.073 |  |
| P2 | GBM-LR | 2023 | 476 | +0.025 | -0.034 | +0.087 | +0.236 |
| P2 | GBM-GBM10 (v1.1 ölçüleri) | 2023 | 476 | +0.040 | -0.004 | +0.079 | +0.040 |
| P2 | CNN katkısı [G,C]-[G] | 2023 | 476 | -0.006 | -0.023 | +0.012 | +0.771 |
| P2 | LSTM katkısı [G,L]-[G] | 2023 | 476 | -0.038 | -0.048 | -0.026 | +1.000 |
| P2 | LSTM üstüne [G,C,L]-[G,C] | 2023 | 476 | -0.036 | -0.048 | -0.024 | +1.000 |
| P2 | CNN tek - GBM | 2023 | 476 | -0.118 | -0.220 | +0.010 | +0.957 |
| P2 | LSTM tek - GBM | 2023 | 476 | -0.014 | -0.100 | +0.117 | +0.561 |
| P2 | LR - rastgele(0,5) | 2023 | 476 | +0.095 | -0.000 | +0.168 |  |
| P2 | GBM-LR | 2024-26 | 667 | +0.007 | -0.032 | +0.050 | +0.362 |
| P2 | GBM-GBM10 (v1.1 ölçüleri) | 2024-26 | 667 | +0.019 | -0.015 | +0.051 | +0.110 |
| P2 | CNN katkısı [G,C]-[G] | 2024-26 | 667 | -0.006 | -0.020 | +0.006 | +0.827 |
| P2 | LSTM katkısı [G,L]-[G] | 2024-26 | 667 | -0.005 | -0.021 | +0.010 | +0.728 |
| P2 | LSTM üstüne [G,C,L]-[G,C] | 2024-26 | 667 | -0.004 | -0.019 | +0.014 | +0.728 |
| P2 | CNN tek - GBM | 2024-26 | 667 | -0.014 | -0.086 | +0.074 | +0.648 |
| P2 | LSTM tek - GBM | 2024-26 | 667 | +0.000 | -0.060 | +0.066 | +0.472 |
| P2 | LR - rastgele(0,5) | 2024-26 | 667 | +0.017 | -0.040 | +0.061 |  |

### grup

| faz | grup | donem | n | tam_eksi_cikarilmis | alt | ust | yalniz_auc |
|---|---|---|---|---|---|---|---|
| P1 | mum | 2023 | 906 | -0.001 | -0.018 | +0.026 | +0.506 |
| P1 | oynaklik | 2023 | 906 | +0.002 | -0.024 | +0.023 | +0.482 |
| P1 | hacim | 2023 | 906 | -0.013 | -0.030 | +0.006 | +0.473 |
| P1 | akis | 2023 | 906 | -0.004 | -0.020 | +0.014 | +0.504 |
| P1 | trend | 2023 | 906 | +0.002 | -0.009 | +0.013 | +0.529 |
| P1 | momentum_dusus | 2023 | 906 | +0.009 | -0.010 | +0.028 | +0.503 |
| P1 | likidite_piyasa | 2023 | 906 | +0.020 | -0.022 | +0.070 | +0.562 |
| P1 | col | 2023 | 906 | -0.010 | -0.032 | +0.009 | +0.514 |
| P1 | mum | 2024-26 | 1316 | -0.015 | -0.032 | +0.004 | +0.490 |
| P1 | oynaklik | 2024-26 | 1316 | +0.002 | -0.013 | +0.020 | +0.512 |
| P1 | hacim | 2024-26 | 1316 | +0.003 | -0.017 | +0.028 | +0.484 |
| P1 | akis | 2024-26 | 1316 | -0.002 | -0.016 | +0.015 | +0.496 |
| P1 | trend | 2024-26 | 1316 | +0.003 | -0.010 | +0.017 | +0.521 |
| P1 | momentum_dusus | 2024-26 | 1316 | +0.012 | -0.003 | +0.025 | +0.502 |
| P1 | likidite_piyasa | 2024-26 | 1316 | +0.011 | -0.011 | +0.037 | +0.522 |
| P1 | col | 2024-26 | 1316 | +0.010 | -0.005 | +0.027 | +0.489 |
| P2 | mum | 2023 | 476 | +0.001 | -0.028 | +0.028 | +0.480 |
| P2 | oynaklik | 2023 | 476 | +0.020 | -0.000 | +0.044 | +0.561 |
| P2 | hacim | 2023 | 476 | +0.003 | -0.016 | +0.024 | +0.507 |
| P2 | akis | 2023 | 476 | +0.023 | -0.009 | +0.050 | +0.577 |
| P2 | trend | 2023 | 476 | +0.017 | +0.003 | +0.034 | +0.517 |
| P2 | momentum_dusus | 2023 | 476 | +0.024 | +0.002 | +0.056 | +0.496 |
| P2 | likidite_piyasa | 2023 | 476 | +0.035 | -0.006 | +0.060 | +0.520 |
| P2 | col | 2023 | 476 | +0.006 | -0.021 | +0.036 | +0.497 |
| P2 | mum | 2024-26 | 667 | +0.005 | -0.025 | +0.033 | +0.499 |
| P2 | oynaklik | 2024-26 | 667 | -0.011 | -0.036 | +0.014 | +0.448 |
| P2 | hacim | 2024-26 | 667 | +0.001 | -0.017 | +0.020 | +0.495 |
| P2 | akis | 2024-26 | 667 | +0.013 | -0.013 | +0.039 | +0.471 |
| P2 | trend | 2024-26 | 667 | -0.006 | -0.033 | +0.022 | +0.483 |
| P2 | momentum_dusus | 2024-26 | 667 | +0.027 | -0.007 | +0.060 | +0.535 |
| P2 | likidite_piyasa | 2024-26 | 667 | +0.002 | -0.031 | +0.028 | +0.523 |
| P2 | col | 2024-26 | 667 | +0.003 | -0.019 | +0.027 | +0.503 |

### kontrol

| kontrol | donem | n | isabet | taban | fark | fark_alt | fark_ust | net | net_taban | net_fark | net_fark_alt | kazanma | ort_kazanc | ort_kayip | en_kotu | medyan_gun | auc | auc_alt | auc_ust |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| plasebo_P1_esli_rastgele | egitim | 505 | +0.248 | +0.280 | -0.032 | -0.066 | +0.007 | -0.014 | -0.006 | -0.008 | -0.021 | +0.390 | +0.144 | -0.116 | -0.558 | +23.000 |  |  |  |
| plasebo_P1_esli_rastgele | dogrulama | 910 | +0.264 | +0.261 | +0.003 | -0.019 | +0.025 | -0.036 | -0.035 | -0.000 | -0.007 | +0.315 | +0.161 | -0.125 | -0.622 | +12.000 |  |  |  |
| plasebo_P1_esli_rastgele | 2023 | 906 | +0.274 | +0.287 | -0.013 | -0.036 | +0.016 | -0.022 | -0.020 | -0.002 | -0.011 | +0.349 | +0.159 | -0.118 | -0.501 | +17.000 |  |  |  |
| plasebo_P1_esli_rastgele | 2024-26 | 1316 | +0.334 | +0.333 | +0.000 | -0.022 | +0.020 | -0.009 | -0.010 | +0.001 | -0.007 | +0.391 | +0.172 | -0.125 | -0.358 | +12.000 |  |  |  |
| P1_negatif_karisik_etiket | 2023 | 906 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.536 | +0.482 | +0.574 |
| P1_pozitif_gelecek5_sizinti | 2023 | 906 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.784 | +0.749 | +0.819 |
| P1_negatif_karisik_etiket | 2024-26 | 1316 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.506 | +0.480 | +0.541 |
| P1_pozitif_gelecek5_sizinti | 2024-26 | 1316 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.828 | +0.804 | +0.849 |
| P2_negatif_karisik_etiket | 2023 | 476 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.546 | +0.504 | +0.577 |
| P2_pozitif_gelecek5_sizinti | 2023 | 476 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.784 | +0.747 | +0.820 |
| P2_negatif_karisik_etiket | 2024-26 | 667 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.519 | +0.467 | +0.559 |
| P2_pozitif_gelecek5_sizinti | 2024-26 | 667 |  |  |  |  |  |  |  |  |  |  |  |  |  |  | +0.785 | +0.745 | +0.830 |

### portfoy

| donem | strateji | sinyal_n | toplam | yillik | mdd | sharpe | calmar | islem_n | kazanma | ort_islem | ort_kayip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | P1_p_LR | 99 | +0.095 | +0.096 | -0.168 | +0.588 | +0.572 | 68 | +0.456 | +0.016 | -0.116 |
| 2023 | P1_p_GBM | 346 | -0.047 | -0.048 | -0.337 | -0.078 | -0.142 | 117 | +0.385 | -0.003 | -0.120 |
| 2023 | P1_Y_GC | 364 | +0.019 | +0.019 | -0.276 | +0.197 | +0.069 | 125 | +0.400 | -0.000 | -0.117 |
| 2023 | P1_Y_GL | 414 | -0.166 | -0.169 | -0.511 | -0.406 | -0.330 | 183 | +0.393 | -0.009 | -0.131 |
| 2024-26 | P1_p_LR | 134 | -0.229 | -0.093 | -0.316 | -0.733 | -0.294 | 125 | +0.376 | -0.020 | -0.134 |
| 2024-26 | P1_p_GBM | 914 | -0.365 | -0.157 | -0.471 | -0.520 | -0.333 | 355 | +0.394 | -0.010 | -0.128 |
| 2024-26 | P1_Y_GC | 639 | -0.499 | -0.229 | -0.546 | -0.965 | -0.418 | 332 | +0.358 | -0.018 | -0.127 |
| 2024-26 | P1_Y_GL | 899 | -0.534 | -0.249 | -0.562 | -0.851 | -0.444 | 435 | +0.384 | -0.016 | -0.131 |
| 2023 | P2_p_LR | 130 | +0.057 | +0.058 | -0.230 | +0.401 | +0.252 | 81 | +0.457 | +0.011 | -0.123 |
| 2023 | P2_p_GBM | 37 | +0.048 | +0.049 | -0.124 | +0.558 | +0.396 | 36 | +0.444 | +0.007 | -0.120 |
| 2023 | P2_Y_GC | 41 | +0.100 | +0.102 | -0.125 | +1.016 | +0.814 | 41 | +0.512 | +0.024 | -0.120 |
| 2023 | P2_Y_GL | 50 | +0.129 | +0.131 | -0.112 | +1.157 | +1.165 | 47 | +0.468 | +0.020 | -0.104 |
| 2024-26 | P2_p_LR | 441 | -0.519 | -0.240 | -0.532 | -1.130 | -0.452 | 290 | +0.355 | -0.022 | -0.126 |
| 2024-26 | P2_p_GBM | 182 | -0.276 | -0.114 | -0.323 | -0.681 | -0.354 | 176 | +0.369 | -0.016 | -0.125 |
| 2024-26 | P2_Y_GC | 191 | -0.316 | -0.133 | -0.353 | -0.770 | -0.376 | 179 | +0.341 | -0.019 | -0.123 |
| 2024-26 | P2_Y_GL | 167 | -0.155 | -0.061 | -0.241 | -0.374 | -0.255 | 159 | +0.390 | -0.009 | -0.121 |
| 2023 | HT_hepsi | 58 | -0.209 | -0.212 | -0.253 | -2.150 | -0.837 | 56 | +0.286 | -0.042 | -0.125 |
| 2023 | P1_hepsi | 906 | -0.026 | -0.027 | -0.389 | +0.011 | -0.069 | 131 | +0.389 | -0.002 | -0.122 |
| 2023 | P2_hepsi | 476 | +0.060 | +0.061 | -0.238 | +0.384 | +0.255 | 98 | +0.469 | +0.009 | -0.118 |
| 2024-26 | HT_hepsi | 191 | -0.434 | -0.192 | -0.497 | -1.576 | -0.387 | 188 | +0.340 | -0.029 | -0.130 |
| 2024-26 | P1_hepsi | 1316 | -0.483 | -0.220 | -0.557 | -0.819 | -0.395 | 362 | +0.370 | -0.016 | -0.126 |
| 2024-26 | P2_hepsi | 667 | -0.296 | -0.124 | -0.362 | -0.467 | -0.342 | 300 | +0.390 | -0.010 | -0.123 |

### sektor

| kume | yil | n | en_buyuk_sektor | en_buyuk_pay | hhi | bilinmiyor_pay |
|---|---|---|---|---|---|---|
| P1 | 2016 | 57 | Healthcare | +0.316 | +0.164 | +0.000 |
| P1 | 2017 | 90 | Basic Materials | +0.278 | +0.172 | +0.000 |
| P1 | 2018 | 80 | Technology | +0.225 | +0.146 | +0.000 |
| P1 | 2019 | 186 | Healthcare | +0.215 | +0.129 | +0.000 |
| P1 | 2020 | 92 | Healthcare | +0.272 | +0.135 | +0.000 |
| P1 | 2021 | 271 | Healthcare | +0.369 | +0.187 | +0.015 |
| P1 | 2022 | 639 | bilinmiyor | +0.304 | +0.158 | +0.304 |
| P1 | 2023 | 906 | bilinmiyor | +0.289 | +0.153 | +0.289 |
| P1 | 2024 | 486 | bilinmiyor | +0.407 | +0.220 | +0.407 |
| P1 | 2025 | 586 | bilinmiyor | +0.449 | +0.250 | +0.449 |
| P1 | 2026 | 244 | bilinmiyor | +0.451 | +0.244 | +0.451 |
| P2 | 2016 | 33 | Healthcare | +0.364 | +0.190 | +0.000 |
| P2 | 2017 | 41 | Healthcare | +0.220 | +0.143 | +0.000 |
| P2 | 2018 | 36 | Healthcare | +0.222 | +0.148 | +0.000 |
| P2 | 2019 | 98 | Healthcare | +0.214 | +0.129 | +0.000 |
| P2 | 2020 | 53 | Healthcare | +0.226 | +0.134 | +0.000 |
| P2 | 2021 | 96 | Healthcare | +0.323 | +0.157 | +0.000 |
| P2 | 2022 | 214 | bilinmiyor | +0.280 | +0.145 | +0.280 |
| P2 | 2023 | 476 | bilinmiyor | +0.261 | +0.142 | +0.261 |
| P2 | 2024 | 236 | bilinmiyor | +0.360 | +0.202 | +0.360 |
| P2 | 2025 | 314 | bilinmiyor | +0.385 | +0.210 | +0.385 |
| P2 | 2026 | 118 | bilinmiyor | +0.415 | +0.222 | +0.415 |
| HT | 2016 | 15 | Healthcare | +0.333 | +0.227 | +0.000 |
| HT | 2017 | 10 | Healthcare | +0.300 | +0.180 | +0.000 |
| HT | 2018 | 10 | Technology | +0.400 | +0.240 | +0.000 |
| HT | 2019 | 22 | Healthcare | +0.227 | +0.198 | +0.000 |
| HT | 2020 | 9 | Healthcare | +0.556 | +0.358 | +0.000 |
| HT | 2021 | 37 | Healthcare | +0.405 | +0.268 | +0.270 |
| HT | 2022 | 60 | bilinmiyor | +0.633 | +0.435 | +0.633 |
| HT | 2023 | 58 | bilinmiyor | +0.569 | +0.360 | +0.569 |
| HT | 2024 | 60 | bilinmiyor | +0.583 | +0.388 | +0.583 |
| HT | 2025 | 95 | bilinmiyor | +0.695 | +0.507 | +0.695 |
| HT | 2026 | 36 | bilinmiyor | +0.722 | +0.540 | +0.722 |

### kirilim

| faz | kirilim | deger | n | isabet | taban | fark | fark_alt | net | gbm_secilen_test_n | gbm_secilen_test_isabet |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 | yil | 2016 | 57 | +0.351 | +0.276 | +0.075 | -0.014 | +0.001 | 0 |  |
| P1 | yil | 2017 | 90 | +0.367 | +0.310 | +0.057 | -0.021 | +0.006 | 0 |  |
| P1 | yil | 2018 | 80 | +0.175 | +0.179 | -0.004 | -0.073 | -0.042 | 0 |  |
| P1 | yil | 2019 | 186 | +0.280 | +0.253 | +0.027 | -0.025 | -0.013 | 0 |  |
| P1 | yil | 2020 | 92 | +0.348 | +0.394 | -0.046 | -0.155 | -0.007 | 0 |  |
| P1 | yil | 2021 | 271 | +0.292 | +0.258 | +0.034 | -0.014 | -0.029 | 0 |  |
| P1 | yil | 2022 | 639 | +0.269 | +0.264 | +0.005 | -0.025 | -0.037 | 0 |  |
| P1 | yil | 2023 | 906 | +0.318 | +0.286 | +0.032 | +0.002 | -0.016 | 346 | +0.341 |
| P1 | yil | 2024 | 486 | +0.368 | +0.315 | +0.054 | +0.007 | -0.008 | 277 | +0.375 |
| P1 | yil | 2025 | 586 | +0.382 | +0.352 | +0.030 | +0.004 | -0.001 | 424 | +0.387 |
| P1 | yil | 2026 | 244 | +0.283 | +0.325 | -0.042 | -0.073 | -0.040 | 213 | +0.305 |
| P1 | rejim | ayi (SPY < SMA200) | 698 | +0.315 | +0.301 | +0.014 | -0.018 | -0.021 | 62 | +0.532 |
| P1 | rejim | boga (SPY > SMA200) | 2939 | +0.321 | +0.295 | +0.026 | +0.010 | -0.018 | 1198 | +0.349 |
| P1 | likidite | dusuk | 1215 | +0.324 | +0.307 | +0.017 | -0.006 | -0.022 | 477 | +0.352 |
| P1 | likidite | orta | 1210 | +0.327 | +0.297 | +0.031 | +0.006 | -0.014 | 393 | +0.369 |
| P1 | likidite | yuksek | 1212 | +0.307 | +0.284 | +0.023 | -0.003 | -0.019 | 390 | +0.354 |
| P1 | sektor_ruzgari | rüzgâr var | 88 | +0.295 | +0.288 | +0.007 | -0.074 | -0.033 | 43 | +0.302 |
| P1 | sektor_ruzgari | rüzgâr yok | 2518 | +0.328 | +0.290 | +0.038 | +0.017 | -0.013 | 689 | +0.399 |
| P1 | sektor_ruzgari | sektör bilinmiyor | 1031 | +0.302 | +0.312 | -0.010 | -0.032 | -0.030 | 528 | +0.309 |
| P2 | yil | 2016 | 33 | +0.424 | +0.324 | +0.100 | -0.083 | +0.024 | 0 |  |
| P2 | yil | 2017 | 41 | +0.244 | +0.309 | -0.066 | -0.194 | +0.003 | 0 |  |
| P2 | yil | 2018 | 36 | +0.194 | +0.201 | -0.006 | -0.138 | -0.026 | 0 |  |
| P2 | yil | 2019 | 98 | +0.204 | +0.244 | -0.039 | -0.103 | -0.042 | 0 |  |
| P2 | yil | 2020 | 53 | +0.358 | +0.433 | -0.075 | -0.168 | -0.004 | 0 |  |
| P2 | yil | 2021 | 96 | +0.240 | +0.252 | -0.012 | -0.077 | -0.047 | 0 |  |
| P2 | yil | 2022 | 214 | +0.234 | +0.241 | -0.007 | -0.025 | -0.027 | 0 |  |
| P2 | yil | 2023 | 476 | +0.286 | +0.273 | +0.013 | -0.020 | -0.020 | 37 | +0.432 |
| P2 | yil | 2024 | 236 | +0.314 | +0.281 | +0.033 | -0.012 | -0.020 | 52 | +0.308 |
| P2 | yil | 2025 | 314 | +0.344 | +0.344 | -0.000 | -0.028 | -0.016 | 84 | +0.357 |
| P2 | yil | 2026 | 118 | +0.305 | +0.325 | -0.020 | -0.089 | -0.034 | 46 | +0.370 |
| P2 | rejim | ayi (SPY < SMA200) | 231 | +0.303 | +0.284 | +0.019 | -0.015 | -0.008 | 14 | +0.500 |
| P2 | rejim | boga (SPY > SMA200) | 1484 | +0.288 | +0.290 | -0.002 | -0.023 | -0.024 | 205 | +0.351 |
| P2 | likidite | dusuk | 575 | +0.318 | +0.312 | +0.007 | -0.031 | -0.023 | 91 | +0.407 |
| P2 | likidite | orta | 567 | +0.266 | +0.279 | -0.013 | -0.044 | -0.029 | 56 | +0.268 |
| P2 | likidite | yuksek | 573 | +0.284 | +0.276 | +0.008 | -0.019 | -0.014 | 72 | +0.375 |
| P2 | sektor_ruzgari | rüzgâr var | 71 | +0.324 | +0.296 | +0.028 | -0.064 | -0.018 | 22 | +0.318 |
| P2 | sektor_ruzgari | rüzgâr yok | 1205 | +0.286 | +0.285 | +0.002 | -0.021 | -0.020 | 118 | +0.398 |
| P2 | sektor_ruzgari | sektör bilinmiyor | 439 | +0.294 | +0.300 | -0.007 | -0.045 | -0.028 | 79 | +0.316 |

### Notlar v1.1

- LSTM epoch kaydı: [{'epoch': 1, 'egitim_kayip': 0.4844155728298316, 'dogrulama_kayip': 0.5261172652244568, 'sure_sn': 8}, {'epoch': 2, 'egitim_kayip': 0.44976391986213526, 'dogrulama_kayip': 0.5281358361244202, 'sure_sn': 7}, {'epoch': 3, 'egitim_kayip': 0.4495287619603819, 'dogrulama_kayip': 0.535022497177124, 'sure_sn': 8}]
