# K54 — TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ (v1.5, ön kayıt d4dcdfb)

K54 yeni iz araştırması değildir. K51 / K52 / K53 ön kayıtları ve kararları değişmedi (K51 İZ DEĞİL). Eski dosyalar üzerine yazılmadı; eski ve düzeltilmiş evren değerleri yan yana.

- Evren 3267 sembol; panel 3175671 likit hisse-gün, düzeltilmiş evren 3171992 satır (2752 hisse); süre 1.5 dk; kod CY v1.5 (2026-10-30, K54 tarihsel evren sağlamlık denetimi; v1.4 K53 bilgi direnci / analist dağınıklığı / karar gecikmesi; v1.3 K52 grafik izi + analist revizyonları: Yahoo not günlüğü, dört grup, H0-H6; v1.2 K51 sonrası bağımsız denetim: veri bütünlüğü, kırılganlık, eşleşmiş kontrollerle H-A..H-E; v1.1 K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil), commit 85852b7.
- Kaynaklar: Tiingo desteklenen sembol listesi (bitiş tarihi, fiyat değil), SEC başvuru geçmişi (8-K madde 1.03 / 2.01, 25-NSE, 15-12G, birleşme belgeleri, 10-K / 10-Q devamı, güncel semboller, eski adlar), company_tickers.json. Tiingo fiyatı analist kaydının yerine kullanılmadı.

## 1. Şirket durumu sınıfları

| sınıf | ad | hisse | V_ABD | K34 Yahoo | K34 Tiingo | erken biten | analist kaydı payı |
|---|---|---|---|---|---|---|---|
| 1 | halen işlem gören | 3001 | 1408 | 1435 | 158 | 0 | +0.835 |
| 2 | iflas / tasfiye | 19 | 0 | 0 | 19 | 19 | +0.000 |
| 3 | birleşme / satın alma | 159 | 0 | 0 | 159 | 159 | +0.013 |
| 4 | sembol değiştiren / başka şirkete dönüşen | 9 | 2 | 0 | 7 | 0 | +0.778 |
| 5 | veri sağlayıcısında kaybolan, belirsiz | 79 | 0 | 0 | 79 | 79 | +0.000 |

- Seri erken biten (T < 2026-08-01) 257 sembol: sınıf 2: 19, sınıf 3: 159, sınıf 5: 79.
- K51'in eski tahmini (K51_EVREN_PIT 'cikis_turu_tahmin') ile karşılaştırma K54_SIRKET_DURUMU.csv'de (sembol başına kural ve kanıt tarihleri).

## 2. Delist duyarlılığı (sınıf başına sayılar; P1 / P2 hücrelerinin −%0 / −%30 / −%100 bandı ve düzeltilmiş etiket)

| sinif | sinif_ad | hisse | V_ABD | K34_yahoo | K34_tiingo | analist_kaydi_pay | panel_satir | P1_olay | P2_olay | son_kapanis_medyan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | halen işlem gören | 3001 | 1408 | 1435 | 158 | +0.835 | 3116066 | 3530 | 1659 | +13.400 |
| 2 | iflas / tasfiye | 19 | 0 | 0 | 19 | +0.000 | 1644 | 5 | 0 | +0.009 |
| 3 | birleşme / satın alma | 159 | 0 | 0 | 159 | +0.013 | 46121 | 85 | 46 | +10.500 |
| 4 | sembol değiştiren / başka şirkete dönüşen | 9 | 2 | 0 | 7 | +0.778 | 8226 | 15 | 8 | +19.990 |
| 5 | veri sağlayıcısında kaybolan, belirsiz | 79 | 0 | 0 | 79 | +0.000 | 3614 | 2 | 2 | +10.190 |

| kume | donem | n | erken_biten_olay | isabet_d0 | isabet_d30 | isabet_d100 | isabet_yeni | bant_genislik_puan |
|---|---|---|---|---|---|---|---|---|
| P1 bandı | 2016-22 | 1415 | 27 | +0.286 | +0.286 | +0.286 | +0.286 | +0.000 |
| P1 bandı | 2023 | 906 | 42 | +0.313 | +0.313 | +0.313 | +0.311 | +0.000 |
| P1 bandı | 2024-26 | 1316 | 23 | +0.357 | +0.357 | +0.357 | +0.356 | +0.000 |
| P2 bandı | 2016-22 | 571 | 9 | +0.255 | +0.255 | +0.255 | +0.255 | +0.000 |
| P2 bandı | 2023 | 476 | 25 | +0.286 | +0.286 | +0.286 | +0.283 | +0.000 |
| P2 bandı | 2024-26 | 667 | 13 | +0.324 | +0.324 | +0.324 | +0.325 | +0.000 |

## 3. Eski evren / düzeltilmiş evren / fark (aynı tanım ve eşikler)

Taban-ayarlı isabet = y − e_y (K51 tabanı aynı gün aynı oynaklık ondalığı); 'fark_fark' = düzeltilmiş − eski (puan, ×100 değil). Değerlendirme: SAĞLAM (≤ 2 puan, karar ve aralık aynı), ETKİLENMİŞ, GEÇERSİZ (sınıf 5 + 6 payı > %30 ya da evren kurulamıyor).

### 3.1 K51 temel hücreleri

| kume | donem | eski_n | yeni_n | eski_ust_oran | yeni_ust_oran | eski_alt_oran | yeni_alt_oran | eski_net | yeni_net | eski_fark | eski_fark_alt | eski_fark_ust | yeni_fark | yeni_fark_alt | yeni_fark_ust | fark_fark | eski_karar | yeni_karar | sinif56_pay_olay | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K51 P1 | 2016-22 | 1415 | 1415 | +0.286 | +0.286 | +0.646 | +0.646 | -0.026 | -0.026 | +0.018 | -0.004 | +0.042 | +0.017 | -0.005 | +0.041 | -0.000 | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 (en iyi 20 çıkarıldı) | 2016-22 | 1355 | 1355 | +0.262 | +0.262 | +0.667 | +0.667 | -0.033 | -0.033 | -0.005 | -0.028 | +0.019 | -0.005 | -0.028 | +0.019 | -0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 P1 | 2023 | 906 | 905 | +0.313 | +0.311 | +0.614 | +0.615 | -0.018 | -0.019 | +0.025 | -0.006 | +0.060 | +0.024 | -0.006 | +0.060 | -0.001 | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 (en iyi 20 çıkarıldı) | 2023 | 848 | 847 | +0.283 | +0.282 | +0.639 | +0.641 | -0.027 | -0.027 | -0.002 | -0.035 | +0.034 | -0.003 | -0.037 | +0.035 | -0.001 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 P1 | 2024-26 | 1316 | 1314 | +0.357 | +0.356 | +0.603 | +0.603 | -0.011 | -0.011 | +0.024 | +0.001 | +0.050 | +0.023 | -0.000 | +0.048 | -0.001 | TUTMAZ | TUTMAZ | +0.000 | ETKİLENMİŞ |
| K51 P1 (en iyi 20 çıkarıldı) | 2024-26 | 1256 | 1254 | +0.332 | +0.332 | +0.625 | +0.626 | -0.019 | -0.019 | +0.000 | -0.022 | +0.024 | -0.001 | -0.023 | +0.021 | -0.001 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 P2 | 2016-22 | 571 | 571 | +0.255 | +0.255 | +0.614 | +0.611 | -0.022 | -0.022 | -0.013 | -0.044 | +0.020 | -0.013 | -0.043 | +0.020 | +0.000 | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2016-22 | 537 | 537 | +0.217 | +0.217 | +0.646 | +0.642 | -0.032 | -0.032 | -0.055 | -0.092 | -0.021 | -0.055 | -0.094 | -0.021 | +0.000 | TERS YÖN | TERS YÖN |  | SAĞLAM |
| K51 P2 | 2023 | 476 | 475 | +0.286 | +0.283 | +0.581 | +0.583 | -0.020 | -0.021 | +0.010 | -0.026 | +0.059 | +0.008 | -0.026 | +0.057 | -0.001 | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2023 | 455 | 454 | +0.252 | +0.249 | +0.608 | +0.611 | -0.030 | -0.031 | -0.031 | -0.060 | +0.011 | -0.033 | -0.060 | +0.005 | -0.002 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 P2 | 2024-26 | 667 | 666 | +0.324 | +0.325 | +0.616 | +0.614 | -0.021 | -0.021 | +0.006 | -0.017 | +0.036 | +0.007 | -0.019 | +0.036 | +0.001 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2024-26 | 627 | 626 | +0.285 | +0.286 | +0.651 | +0.650 | -0.032 | -0.032 | -0.031 | -0.056 | -0.002 | -0.031 | -0.054 | -0.004 | +0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 ES | 2016-22 | 2316 | 2315 | +0.300 | +0.299 | +0.638 | +0.639 | -0.025 | -0.026 | +0.010 | -0.010 | +0.030 | +0.010 | -0.009 | +0.028 | -0.000 | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2016-22 | 2228 | 2227 | +0.286 | +0.285 | +0.652 | +0.652 | -0.030 | -0.030 | -0.004 | -0.026 | +0.016 | -0.005 | -0.026 | +0.014 | -0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 ES | 2023 | 896 | 896 | +0.311 | +0.311 | +0.612 | +0.612 | -0.021 | -0.021 | -0.002 | -0.028 | +0.022 | -0.003 | -0.029 | +0.022 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2023 | 857 | 857 | +0.283 | +0.283 | +0.638 | +0.638 | -0.030 | -0.030 | -0.029 | -0.055 | -0.004 | -0.029 | -0.054 | -0.004 | -0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 ES | 2024-26 | 2382 | 2377 | +0.342 | +0.342 | +0.589 | +0.589 | -0.007 | -0.007 | +0.008 | -0.016 | +0.032 | +0.009 | -0.018 | +0.032 | +0.000 | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2024-26 | 2316 | 2311 | +0.329 | +0.329 | +0.601 | +0.601 | -0.011 | -0.011 | -0.006 | -0.031 | +0.017 | -0.006 | -0.030 | +0.018 | +0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 HT | 2016-22 | 163 | 163 | +0.340 | +0.340 | +0.592 | +0.592 | -0.013 | -0.013 | +0.035 | -0.056 | +0.120 | +0.035 | -0.046 | +0.118 | -0.000 | TUTMAZ | TUTMAZ | +0.012 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2016-22 | 140 | 140 | +0.233 | +0.233 | +0.688 | +0.688 | -0.044 | -0.044 | -0.093 | -0.162 | -0.026 | -0.093 | -0.164 | -0.026 | -0.000 | TERS YÖN | TERS YÖN |  | SAĞLAM |
| K51 HT | 2023 | 58 | 58 | +0.276 | +0.276 | +0.724 | +0.724 | -0.045 | -0.045 | -0.055 | -0.148 | +0.036 | -0.055 | -0.146 | +0.034 | +0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2023 | 37 | 37 | +0.000 | +0.000 | +1.000 | +1.000 | -0.127 | -0.127 | -0.318 | -0.399 | -0.239 | -0.318 | -0.398 | -0.236 | -0.000 | TERS YÖN | TERS YÖN |  | SAĞLAM |
| K51 HT | 2024-26 | 191 | 191 | +0.331 | +0.331 | +0.650 | +0.650 | -0.027 | -0.027 | -0.012 | -0.060 | +0.040 | -0.012 | -0.062 | +0.038 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2024-26 | 167 | 167 | +0.241 | +0.241 | +0.737 | +0.737 | -0.054 | -0.054 | -0.121 | -0.170 | -0.068 | -0.121 | -0.170 | -0.070 | +0.000 | TERS YÖN | TERS YÖN |  | SAĞLAM |
| K51 ÇEK | 2016-22 | 4193 | 4192 | +0.286 | +0.286 | +0.647 | +0.646 | -0.027 | -0.027 | +0.006 | -0.008 | +0.019 | +0.006 | -0.008 | +0.020 | +0.000 | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2016-22 | 4051 | 4050 | +0.275 | +0.275 | +0.656 | +0.655 | -0.030 | -0.030 | -0.005 | -0.019 | +0.008 | -0.005 | -0.019 | +0.009 | +0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 ÇEK | 2023 | 1983 | 1982 | +0.314 | +0.313 | +0.607 | +0.607 | -0.019 | -0.019 | +0.007 | -0.010 | +0.025 | +0.007 | -0.011 | +0.026 | -0.000 | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2023 | 1924 | 1923 | +0.297 | +0.297 | +0.621 | +0.622 | -0.024 | -0.024 | -0.010 | -0.027 | +0.010 | -0.011 | -0.028 | +0.009 | -0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |
| K51 ÇEK | 2024-26 | 4192 | 4187 | +0.347 | +0.347 | +0.592 | +0.593 | -0.007 | -0.007 | +0.016 | -0.002 | +0.036 | +0.016 | -0.003 | +0.037 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2024-26 | 4086 | 4081 | +0.337 | +0.337 | +0.601 | +0.602 | -0.010 | -0.010 | +0.005 | -0.013 | +0.025 | +0.005 | -0.014 | +0.025 | -0.000 | TUTMAZ | TUTMAZ |  | SAĞLAM |

### 3.2 Küçük mum / hacim kuruması / hacimli taban (v1.2 eşleşmiş kontrol; eşleştirme havuzu her evrende ayrı)

| kume | donem | evren | n | fark | fark_alt | fark_ust | net_fark | karar | eslesmeyen_pay | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|
| H-B P1 vs ES (küçük mum) | 2016-22 | eski | 235 | -0.012 | -0.114 | +0.090 | -0.001 | TUTMAZ | +0.830 |  |
| H-B P1 vs ES (küçük mum) | 2023 | eski | 135 | -0.015 | -0.079 | +0.050 | +0.002 | TUTMAZ | +0.830 |  |
| H-B P1 vs ES (küçük mum) | 2024-26 | eski | 249 | +0.041 | -0.037 | +0.120 | -0.000 | TUTMAZ | +0.830 |  |
| H-B P1 vs ES (küçük mum) | 2016-22 | yeni | 235 | -0.012 | -0.111 | +0.089 | -0.001 | TUTMAZ | +0.830 | SAĞLAM |
| H-B P1 vs ES (küçük mum) | 2023 | yeni | 135 | -0.015 | -0.079 | +0.055 | +0.002 | TUTMAZ | +0.830 | SAĞLAM |
| H-B P1 vs ES (küçük mum) | 2024-26 | yeni | 249 | +0.041 | -0.034 | +0.117 | -0.000 | TUTMAZ | +0.830 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | eski | 135 | -0.032 | -0.160 | +0.089 | -0.014 | TUTMAZ | +0.903 |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | eski | 68 | +0.061 | -0.094 | +0.192 | +0.024 | TUTMAZ | +0.903 |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | eski | 151 | +0.093 | -0.012 | +0.195 | +0.043 | TUTMAZ | +0.903 |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | yeni | 134 | -0.032 | -0.157 | +0.099 | -0.014 | TUTMAZ | +0.904 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | yeni | 67 | +0.050 | -0.105 | +0.180 | +0.023 | TUTMAZ | +0.904 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | yeni | 151 | +0.093 | -0.012 | +0.197 | +0.043 | TUTMAZ | +0.904 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2016-22 | eski | 99 | +0.092 | -0.036 | +0.206 | +0.034 | TUTMAZ | +0.316 |  |
| H-D hacimli taban (HT) vs genel | 2023 | eski | 43 | +0.027 | -0.105 | +0.128 | +0.018 | TUTMAZ | +0.316 |  |
| H-D hacimli taban (HT) vs genel | 2024-26 | eski | 140 | -0.030 | -0.102 | +0.039 | -0.003 | TUTMAZ | +0.316 |  |
| H-D hacimli taban (HT) vs genel | 2016-22 | yeni | 99 | +0.092 | -0.047 | +0.203 | +0.034 | TUTMAZ | +0.316 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2023 | yeni | 43 | +0.027 | -0.091 | +0.126 | +0.018 | TUTMAZ | +0.316 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2024-26 | yeni | 140 | -0.030 | -0.107 | +0.041 | -0.003 | TUTMAZ | +0.316 | SAĞLAM |
| K48 / K49 / K50 deneyleri | hepsi |  |  |  |  |  |  |  |  | GEÇERSİZ (evren yeniden kurulamıyor: yalnız bugün işlem gören V_ABD evreninde koştu; kod K34 evrenini almıyor) |

### 3.3 Sessiz ML (LightGBM meta-etiketleme, P1, yıl yıl ileri)

| kume | donem | evren | n | auc | fark | ust_fark | ust_fark_alt | ust_fark_ust | alt_fark | karar | yillik_auc | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | eski | 3410 | +0.512 | +0.003 | +0.024 | -0.005 | +0.051 | +0.020 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.461; 2025: 0.549; 2026: 0.448 |  |
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | yeni | 3407 | +0.513 | +0.004 | +0.021 | -0.007 | +0.049 | +0.017 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.449; 2025: 0.557; 2026: 0.475 | SAĞLAM |

### 3.4 K52 / K53 (kayıtlı olay dosyaları, düzeltilmiş etiket; sınıf 6 çıkarıldı)

| test | kume | donem | eski_n | eski_n_b | yeni_n | yeni_n_b | eski_fark | eski_fark_alt | eski_fark_ust | yeni_fark | yeni_fark_alt | yeni_fark_ust | fark_fark | eski_karar | yeni_karar | sinif56_pay_olay | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2016-22 | 178 | 990 | 178 | 990 | +0.017 | -0.067 | +0.108 | +0.017 | -0.069 | +0.111 | +0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2023 | 122 | 626 | 122 | 625 | +0.021 | -0.077 | +0.122 | +0.023 | -0.077 | +0.124 | +0.001 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2024-26 | 197 | 985 | 197 | 983 | -0.020 | -0.074 | +0.043 | -0.018 | -0.072 | +0.045 | +0.002 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2016-22 | 108 | 377 | 108 | 377 | +0.114 | +0.024 | +0.212 | +0.114 | +0.023 | +0.214 | -0.000 | TUTAR | TUTAR | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2023 | 79 | 320 | 79 | 319 | +0.055 | -0.077 | +0.143 | +0.057 | -0.067 | +0.150 | +0.002 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2024-26 | 128 | 493 | 128 | 492 | +0.020 | -0.049 | +0.109 | +0.020 | -0.053 | +0.114 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2016-22 | 1007 | 15602 | 1007 | 15602 | +0.008 | -0.015 | +0.031 | +0.008 | -0.015 | +0.031 | +0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2023 | 235 | 4114 | 234 | 4108 | -0.012 | -0.075 | +0.049 | -0.012 | -0.076 | +0.052 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2024-26 | 749 | 12248 | 749 | 12220 | +0.020 | -0.013 | +0.051 | +0.020 | -0.013 | +0.054 | +0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2016-22 | 3999 | 4185 | 3999 | 4185 | -0.012 | -0.031 | +0.008 | -0.012 | -0.031 | +0.007 | +0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2023 | 920 | 1291 | 919 | 1287 | -0.003 | -0.034 | +0.027 | -0.005 | -0.036 | +0.027 | -0.001 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2024-26 | 2904 | 4032 | 2895 | 4022 | -0.001 | -0.019 | +0.017 | -0.002 | -0.018 | +0.017 | -0.001 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2016-22 | 2617 | 3259 | 2617 | 3259 | +0.024 | +0.003 | +0.044 | +0.024 | +0.003 | +0.044 | -0.000 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2023 | 1199 | 933 | 1197 | 933 | +0.028 | -0.014 | +0.063 | +0.030 | -0.011 | +0.067 | +0.002 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2024-26 | 3260 | 2885 | 3254 | 2881 | +0.025 | +0.006 | +0.042 | +0.025 | +0.007 | +0.043 | +0.001 | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |

## 4. K52 / K53 özel denetimi

- K52 olaylarında sınıf dağılımı: {1: 5189, 3: 130, 4: 23, 2: 5, 5: 4}
- K52 olaylarında analist kaydı olan pay (sınıf 2-6 içinde): 0.09876543209876543
- K53 olaylarında sınıf dağılımı: {1: 33896, 4: 53, 3: 6}
- sınıf 1 (halen işlem gören) analist kaydı olan pay: 0.8350549816727757
- sınıf 2 (iflas / tasfiye) analist kaydı olan pay: 0.0
- sınıf 3 (birleşme / satın alma) analist kaydı olan pay: 0.012578616352201259
- sınıf 4 (sembol değiştiren / başka şirkete dönüşen) analist kaydı olan pay: 0.7777777777777778
- sınıf 5 (veri sağlayıcısında kaybolan, belirsiz) analist kaydı olan pay: 0.0
- Analist geçmişi olmayan şirketlere sıfır revizyon atanmadı; K52 / K53'te bunlar 'veri yok' (G2b / G4b) alt grubundaydı. Yahoo günlüğü yalnız bugün Yahoo'da bulunan sembolleri kapsadığından K52 / K53 sonuçları **yalnız Yahoo kapsamındaki (çoğu halen işlem gören) şirketler için geçerlidir**; batan / birleşen şirketlerin analist geçmişi yoktur ve Tiingo fiyatı bunun yerine kullanılmamıştır.

## 5. Değerlendirme özeti

- 1 K51 temel: SAĞLAM: 29, ETKİLENMİŞ: 1
- 3 BB sıkışması / EMA (K48, FON_IZI): GEÇERSİZ (evren yeniden kurulamıyor: yalnız bugün işlem gören V_ABD evreninde koştu; kod K34 evrenini almıyor): 1
- 3 küçük mum / hacim / taban (v1.2 eşleşmiş): SAĞLAM: 9
- 4 sessiz ML (LightGBM meta, P1, yıl yıl ileri 2019-26): SAĞLAM: 1
- 5 K52 H0 (G1 − G2a): SAĞLAM: 6
- 5 K53 T1 (BDS 3 − BDS < 3): SAĞLAM: 3
- 5 K53 T5 (KGS geç − hızlı): SAĞLAM: 3
- 5 K53 T6 (ADE üst − alt üçte bir): SAĞLAM: 3

Sınıf 6 (doğrulanamayan) ve sınıf 5 (belirsiz) hiçbir hücrede iflas ya da aktif sayılmadı; 6 düzeltilmiş evrenden çıktı, 5 K51 kuralıyla kaldı ve bandı yazıldı.

## 6. Yorum ve sınırlar (sonuç görüldükten sonra yazılan açıklama; kararlar değişmedi)

- Evren düzeltmesi eski sonuçları değiştirmiyor: hücrelerin neredeyse hepsi SAĞLAM. Sebep: evrendeki 3267 sembolün 266'ü borsadan çıkmış ya da belirsiz; P1 / P2 olaylarının çok azı seri erken biten şirketlerde ve bunların 60 günlük penceresi nadiren seri sonuna çarpıyor. Bu yüzden delist varsayımı (−%0 / −%30 / −%100) hücreleri oynatmıyor (bant genişliği tabloda).
- Bu 'SAĞLAM' etiketi yalnız MEVCUT evren içindeki sınıflandırma ve çıkış işlemi düzeltmesi için geçerlidir. Evrenin kendisi çoğunlukla hayatta kalanlardan oluşur (V_ABD ve K34 Yahoo yalnız bugün Yahoo'da olanlar; batanlar yalnız 422'lik Tiingo örnekleminden). Eksik batan şirketler eklenmeden hayatta kalma yanlılığı tam ölçülemez; bu K54'ün kapsamı dışında kalan açık maddedir (Kasım Tiingo kotasıyla gerçek batan evreni).
- Sınıf 4b (kod yeniden kullanımı) listesi aynı şirketin yeniden kaydını da yakalayabilir (örn. aynı adlı şirketin başka CIK'i); kesim bu durumda geçerli veriyi atar, yani düzeltme muhafazakârdır (9 sembol).
- K51'in eski 'batma benzeri' tahmininin bir bölümü SEC kanıtına göre birleşme / satın alma ya da belirsiz çıktı; 'satın alma benzeri' tahmininin bir bölümü belirsiz. Sembol başına eski tahmin ve yeni sınıf K54_SIRKET_DURUMU.csv ile K51_EVREN_PIT.csv birleştirilerek görülür.
- ETKİLENMİŞ etiketi alan hücrelerde etki değişimi 2 puanın altındadır; etiket yalnız aralık alt ucunun sıfırın öbür yanına geçmesinden gelir (sınırda hücre; karar değişmedi).

## Yeniden üretim

- `R = cy_v15_calistir(k54_yol='.../k54')` (k54: sec_ozet.json, sembol_cik.json, company_tickers.json, supported_tickers.csv; SEC indirmesi e-posta User-Agent ile, kodda yok). Çıktılar: K54_EVREN_ESLESTIRME.csv, K54_SIRKET_DURUMU.csv, K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv, bu belge.
