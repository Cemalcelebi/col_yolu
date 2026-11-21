# K56-EVREN2 BATAN ŞİRKETLERLE EVREN v2 (K56-EVREN2-20261108-043114-56cdbcd)

- commit 56cdbcd; evren v2 sürümü 3055f07be1ba (K55: 0d00d2c97608, DEĞİŞMEDİ); doğrulama tablosu sha 131c350f13e1; süre 48.7 dk.
- K51-K55 evreni ve sonuçları değişmedi; v2 ayrı sürüm. Getiri (asıl): yeni şirkette pencere seri sonunu aşarsa TANIMSIZ; son işlem fiyatı tasfiye ödemesi sayılmadı; eksik delist getirisi uydurulmadı.
- Aday 490 ({'Ö2 (Tiingo KEŞİF bitişi)': 291, 'Ö1 (K34 kalan)': 199}); meta aşamasında DIŞI (ilk neden) {'CIK bağlanamadı (sınıf 6)': 101, 'KİMLİK: Tiingo adı SEC adlarıyla uyumsuz (Jaccard 0.33)': 17, 'ad: ETF': 2, 'SEC KAPSAM: dönemsel rapor yok': 2, 'META VARLIK: başlangıç 2022-05-03 ≠ liste 2014-09-25': 1, 'META VARLIK: başlangıç 2020-12-14 ≠ liste 2006-12-28': 1, 'M
- Kimlik (Tiingo adı ~ SEC adı): {'UYUMLU': 323, 'SEC YOK': 108, 'YAKIN': 39, 'UYUMSUZ': 19, 'META YOK': 1}; Ö2 CIK bağlama {'K34 eşleme (Ö1)': 199, 'ad + tarih': 183, 'BAĞLANAMADI': 108}; son işlem tutarlılığı {'TUTARLI': 325, 'YAKIN': 14, 'OTC KUYRUĞU': 13, 'UYUMSUZ': 1}.
- Son sınıf (K54 kuralı + K56 ayrımı): {'BİRLEŞME': 267, 'VERİ SAĞLAYICISI KAYBOLMASI': 36, 'İFLAS': 21, 'SEMBOL DEĞİŞİKLİĞİ': 21, 'TASFİYE': 11}.
- Evren dışı (ilk neden): {'CIK bağlanamadı (sınıf 6)': 101, 'KİMLİK: Tiingo adı SEC adlarıyla uyumsuz (Jaccard 0.33)': 17, "CIK tekrarı (aynı şirket K55'te ya da başka yeni sembolde; eklenmedi)": 10, 'seri: İNMEDİ': 3, 'ad: ETF': 2, 'SEC KAPSAM: dönemsel rapor yok': 2, 'META VARLIK: başlangıç 2022-05-03 ≠ liste 2014-09-25': 1, 'META VARLIK: başlangıç 2020-12-14 ≠ liste
- Evrene giren yeni şirket 342; evren v2 3602 sembol (K55 3260); duyarlılıkta hariç tutulan işaretli 96.
- BAĞIMSIZ etkisi: koşulmaz (v1.2-C ve v1.3-I: EVREN2 etkisi yalnız KEŞİF ve İÇ; BAĞIMSIZ bir kez açılır).

## Olay sayıları (dönem × ufuk)

| donem | ufuk | k55 | v2 | v2_yeni_sirket | v2_k55_sirket | fark | fark_k55_sirket |
|---|---|---|---|---|---|---|---|
| IC_DOGRULAMA | Y120 | 946 | 997 | 51 | 946 | 51 | 0 |
| IC_DOGRULAMA | Y250 | 243 | 254 | 11 | 243 | 11 | 0 |
| IC_DOGRULAMA | Y60 | 2916 | 3062 | 146 | 2916 | 146 | 0 |
| KESIF | Y120 | 2062 | 2503 | 294 | 2209 | 441 | 147 |
| KESIF | Y250 | 895 | 1081 | 106 | 975 | 186 | 80 |
| KESIF | Y60 | 4292 | 5237 | 627 | 4610 | 945 | 318 |

## Aday doğrulama (denetim × sonuç)

| kaynak | evrende | n |
|---|---|---|
| Ö1 (K34 kalan) | False | 21 |
| Ö1 (K34 kalan) | True | 178 |
| Ö2 (Tiingo KEŞİF bitişi) | False | 127 |
| Ö2 (Tiingo KEŞİF bitişi) | True | 164 |

Ön / son sınıf:

| sinif_on_k56 | BİRLEŞME | SEMBOL DEĞİŞİKLİĞİ | TASFİYE | VERİ SAĞLAYICISI KAYBOLMASI | İFLAS |
|---|---|---|---|---|---|
| BİRLEŞME | 267 | 0 | 0 | 0 | 0 |
| SEMBOL DEĞİŞİKLİĞİ | 0 | 21 | 0 | 0 | 0 |
| TASFİYE | 0 | 0 | 11 | 0 | 0 |
| VERİ SAĞLAYICISI KAYBOLMASI | 0 | 0 | 0 | 36 | 0 |
| İFLAS | 0 | 0 | 0 | 0 | 21 |

## Yeni şirketlerin tarihsel kapsamı

- KEŞİF günü olan şirket 334; İÇ 172; 2024 sonrası verisi olan 88 (BAĞIMSIZ dönemi kapı dışında sayılmaz).

| kaynak | sinif_k56 | n | evrende |
|---|---|---|---|
| Ö1 (K34 kalan) | BİRLEŞME | 126 | 126 |
| Ö1 (K34 kalan) | TASFİYE | 8 | 8 |
| Ö1 (K34 kalan) | VERİ SAĞLAYICISI KAYBOLMASI | 26 | 26 |
| Ö1 (K34 kalan) | İFLAS | 18 | 18 |
| Ö2 (Tiingo KEŞİF bitişi) | BİRLEŞME | 141 | 135 |
| Ö2 (Tiingo KEŞİF bitişi) | SEMBOL DEĞİŞİKLİĞİ | 21 | 15 |
| Ö2 (Tiingo KEŞİF bitişi) | TASFİYE | 3 | 3 |
| Ö2 (Tiingo KEŞİF bitişi) | VERİ SAĞLAYICISI KAYBOLMASI | 10 | 10 |
| Ö2 (Tiingo KEŞİF bitişi) | İFLAS | 3 | 1 |

## Veri eksikleri

| durum | n |

(Bu tablo transkriptten kurtarılamadı; Ç142 metnindeki sayılar: KEŞİF Y60 4.292 -> 5.237 (yeni şirket 627), İÇ Y60 2.916 -> 3.062.)

## Veri eksikleri

| durum | n |
|---|---|
| eklendi (evren_insa'ya) | 342 |
| CIK tekrarı (aynı şirket K55'te ya da başka yeni sembolde; eklenmedi) | 10 |
| İNMEDİ | 3 |
| kısa seri (212 < 320) | 1 |

## Getiri duyarlılığı (A1'i etkilemez: olay ve nitelikli gün tam pencere ister)

| ufuk_gun | sinif_k56 | likit_satir | pencere_tanimsiz | duyarlilik |
|---|---|---|---|---|
| 60 | BİRLEŞME | 144316 | 6711 | son kapanış |
| 60 | SEMBOL DEĞİŞİKLİĞİ | 405 | 41 | TANIMSIZ kalır |
| 60 | TASFİYE | 4820 | 276 | TANIMSIZ kalır |
| 60 | VERİ SAĞLAYICISI KAYBOLMASI | 5775 | 350 | TANIMSIZ kalır |
| 60 | İFLAS | 7314 | 0 | −%100 |
| 120 | BİRLEŞME | 144316 | 12965 | son kapanış |
| 120 | SEMBOL DEĞİŞİKLİĞİ | 405 | 86 | TANIMSIZ kalır |
| 120 | TASFİYE | 4820 | 481 | TANIMSIZ kalır |
| 120 | VERİ SAĞLAYICISI KAYBOLMASI | 5775 | 577 | TANIMSIZ kalır |
| 120 | İFLAS | 7314 | 7 | −%100 |
| 250 | BİRLEŞME | 144316 | 25546 | son kapanış |
| 250 | SEMBOL DEĞİŞİKLİĞİ | 405 | 195 | TANIMSIZ kalır |
| 250 | TASFİYE | 4820 | 993 | TANIMSIZ kalır |
| 250 | VERİ SAĞLAYICISI KAYBOLMASI | 5775 | 954 | TANIMSIZ kalır |
| 250 | İFLAS | 7314 | 495 | −%100 |

## Etki: 125 KEŞİF satırı (v2 − K55)

- sınıfı değişen satır: {'IC_DOGRULAMA': 3, 'KESIF': 2}; d(i) farkı medyanı {'IC_DOGRULAMA': -0.0011, 'KESIF': -0.0054}; d(ii) farkı medyanı {'IC_DOGRULAMA': -0.0012, 'KESIF': -0.0013}

| donem | hucre | varyant | ufuk | eski_i_n_olay | i_n_olay | eski_i_d | i_d | eski_ii_d | ii_d | eski_sinif_a1 | sinif_a1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IC_DOGRULAMA | D01-S02 | D01-S02/10 | Y120 | 946 | 997 | -0.356 | -0.360 | -0.020 | -0.019 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/10 | Y250 | 243 | 254 | -0.457 | -0.464 | 0.003 | 0.001 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/10 | Y60 | 2916 | 3062 | -0.306 | -0.304 | -0.013 | -0.012 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/20 | Y120 | 946 | 997 | -0.249 | -0.248 | -0.008 | -0.009 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/20 | Y250 | 243 | 254 | -0.349 | -0.354 | -0.006 | -0.016 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/20 | Y60 | 2916 | 3062 | -0.285 | -0.282 | -0.046 | -0.040 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/40 | Y120 | 946 | 997 | -0.287 | -0.291 | 0.029 | 0.024 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/5 | Y120 | 946 | 997 | -0.370 | -0.363 | -0.005 | -0.005 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/5 | Y250 | 243 | 254 | -0.314 | -0.312 | -0.006 | -0.005 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/5 | Y60 | 2916 | 3062 | -0.289 | -0.290 | -0.005 | -0.006 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S02 | D01-S02/60 | Y120 | 946 | 997 | -0.297 | -0.293 | -0.004 | 0.000 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S05 | D01-S05/20 | Y250 | 243 | 254 | -0.218 | -0.249 | 0.060 | 0.060 | TERS KALINTI | TERS KALINTI |
| IC_DOGRULAMA | D01-S05 | D01-S05/40 | Y250 | 243 | 254 | -0.221 | -0.242 | 0.071 | 0.072 | TERS KALINTI | TERS KALINTI |
| IC_DOGRULAMA | D01-S05 | D01-S05/60 | Y250 | 243 | 254 | -0.213 | -0.230 | 0.058 | 0.062 | TERS KALINTI | TERS KALINTI |
| IC_DOGRULAMA | D01-S07 | D01-S07/10 | Y250 | 243 | 254 | -0.362 | -0.354 | -0.061 | -0.060 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S07 | D01-S07/5 | Y250 | 243 | 254 | -0.285 | -0.284 | -0.035 | -0.033 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S08 | D01-S08/20 | Y250 | 243 | 254 | -0.379 | -0.360 | 0.033 | 0.029 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D01-S08 | D01-S08/20 | Y60 | 2916 | 3062 | -0.251 | -0.253 | -0.072 | -0.070 | KISMEN MEKANİK | KISMEN MEKANİK |
| IC_DOGRULAMA | D01-S10 | D01-S10/20 | Y250 | 243 | 254 | 0.199 | 0.196 | 0.060 | 0.056 | KISMEN MEKANİK | KISMEN MEKANİK |
| IC_DOGRULAMA | D02-S02 | D02-S02/10 | Y120 | 946 | 997 | 0.403 | 0.390 | -0.005 | -0.000 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/10 | Y250 | 243 | 254 | 0.504 | 0.492 | 0.017 | 0.021 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/10 | Y60 | 2916 | 3062 | 0.373 | 0.368 | 0.067 | 0.066 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/20 | Y120 | 946 | 997 | 0.319 | 0.309 | -0.022 | -0.017 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/20 | Y250 | 243 | 254 | 0.526 | 0.507 | 0.027 | 0.028 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/20 | Y60 | 2916 | 3062 | 0.304 | 0.299 | 0.080 | 0.077 | KISMEN MEKANİK | KISMEN MEKANİK |
| IC_DOGRULAMA | D02-S02 | D02-S02/40 | Y250 | 243 | 254 | 0.537 | 0.521 | 0.047 | 0.041 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/5 | Y120 | 946 | 997 | 0.448 | 0.441 | -0.000 | 0.005 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/5 | Y250 | 243 | 254 | 0.469 | 0.442 | 0.018 | 0.021 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S02 | D02-S02/5 | Y60 | 2916 | 3062 | 0.383 | 0.380 | 0.052 | 0.053 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S05 | D02-S05/20 | Y250 | 243 | 254 | 0.347 | 0.326 | 0.042 | 0.033 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S05 | D02-S05/40 | Y250 | 243 | 254 | 0.304 | 0.296 | 0.070 | 0.060 | KISMEN MEKANİK | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S05 | D02-S05/60 | Y250 | 243 | 254 | 0.255 | 0.233 | 0.087 | 0.079 | KISMEN MEKANİK | KISMEN MEKANİK |
| IC_DOGRULAMA | D02-S06 | D02-S06/10 | Y250 | 243 | 254 | 0.381 | 0.359 | 0.049 | 0.036 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S06 | D02-S06/20 | Y250 | 243 | 254 | 0.339 | 0.304 | 0.062 | 0.047 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S06 | D02-S06/40 | Y250 | 243 | 254 | 0.257 | 0.240 | 0.087 | 0.071 | KISMEN MEKANİK | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S06 | D02-S06/60 | Y250 | 243 | 254 | 0.193 | 0.161 | 0.085 | 0.070 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D02-S08 | D02-S08/10 | Y120 | 946 | 997 | -0.587 | -0.586 | -0.028 | -0.025 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/10 | Y250 | 243 | 254 | -0.800 | -0.817 | -0.106 | -0.099 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/10 | Y60 | 2916 | 3062 | -0.450 | -0.448 | -0.033 | -0.030 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/20 | Y120 | 946 | 997 | -0.483 | -0.484 | -0.022 | -0.021 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/20 | Y250 | 243 | 254 | -0.708 | -0.705 | -0.131 | -0.125 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/20 | Y60 | 2916 | 3062 | -0.390 | -0.381 | -0.045 | -0.040 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/40 | Y120 | 946 | 997 | -0.422 | -0.430 | -0.026 | -0.027 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/40 | Y250 | 243 | 254 | -0.643 | -0.652 | -0.127 | -0.121 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/5 | Y120 | 946 | 997 | -0.619 | -0.606 | -0.027 | -0.024 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/5 | Y250 | 243 | 254 | -0.767 | -0.779 | -0.100 | -0.092 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/5 | Y60 | 2916 | 3062 | -0.498 | -0.495 | -0.029 | -0.027 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D02-S08 | D02-S08/60 | Y250 | 243 | 254 | -0.655 | -0.658 | -0.112 | -0.109 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D03-S02 | D03-S02/20 | Y120 | 946 | 997 | 0.420 | 0.431 | 0.007 | 0.013 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D03-S02 | D03-S02/20 | Y250 | 243 | 254 | 0.654 | 0.688 | 0.024 | 0.026 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D03-S02 | D03-S02/20 | Y60 | 2916 | 3062 | 0.338 | 0.339 | 0.029 | 0.029 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D03-S02 | D03-S02/40 | Y250 | 243 | 254 | 0.491 | 0.494 | 0.001 | -0.002 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D03-S02 | D03-S02/60 | Y250 | 243 | 254 | 0.488 | 0.505 | -0.004 | -0.008 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
| IC_DOGRULAMA | D04-S04 | D04-S04/tek | Y250 | 243 | 254 | -0.233 | -0.236 | 0.003 | 0.020 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) |
| IC_DOGRULAMA | D04-S06 | D04-S06/tek | Y120 | 946 | 997 | -0.257 | -0.263 | -0.002 | -0.004 | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek + sentetik) |
----
K56_EVREN2_ETKI.csv (250, 53) ['hucre', 'varyant', 'ufuk', 'donem', 'n_satir', 'sent_oran_faz0', 'i_n_olay', 'i_d', 'i_d_alt', 'i_d_ust', 'i_p', 'i_auc', 'i_yil', 'ii_n_olay', 'ii_d', 'ii_d_alt']
   sinif_a1 {'MEKANİK (gerçek + sentetik)': 210, 'MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)': 23, 'TERS KALINTI': 9, 'KISMEN MEKANİK': 8}
   sinif_iii {'GERÇEK ETKİ KALIYOR': 248, 'MEKANİK (gerçek + sentetik)': 2}
   eski_sinif_a1 {'MEKANİK (gerçek + sentetik)': 207, 'MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)': 21, 'KISMEN MEKANİK': 12, 'TERS KALINTI': 10}
   sinif_degisti {False: 245, True: 5}
K56_EVREN2_ETKI_DUYARLILIK.csv (250, 53) ['hucre', 'varyant', 'ufuk', 'donem', 'n_satir', 'sent_oran_faz0', 'i_n_olay', 'i_d', 'i_d_alt', 'i_d_ust', 'i_p', 'i_auc', 'i_yil', 'ii_n_olay', 'ii_d', 'ii_d_alt']
   sinif_a1 {'MEKANİK (gerçek + sentetik)': 210, 'MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)': 19, 'KISMEN MEKANİK': 12, 'TERS KALINTI': 9}
   sinif_iii {'GERÇEK ETKİ KALIYOR': 249, 'MEKANİK (gerçek + sentetik)': 1}
   eski_sinif_a1 {'MEKANİK (gerçek + sentetik)': 207, 'MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)': 21, 'KISMEN MEKANİK': 12, 'TERS KALINTI': 10}
   sinif_degisti {False: 245, True: 5}
GETIRI_DUY (15, 5) ['ufuk_gun', 'sinif_k56', 'likit_satir', 'pencere_tanimsiz', 'duyarlilik']
   ufuk_gun                    sinif_k56  likit_satir  pencere_tanimsiz      duyarlilik
0        60                     BİRLEŞME       144316              6711     son kapanış
1        60           SEMBOL DEĞİŞİKLİĞİ          405                41  TANIMSIZ kalır
2        60                      TASFİYE         4820               276  TANIMSIZ kalır
3        60  VERİ SAĞLAYICISI KAYBOLMASI         5775               350  TANIMSIZ kalır
4        60                        İFLAS         7314                 0           −%100
5       120                     BİRLEŞME       144316             12965     son kapanış
FIYAT_DEN (356, 22) ['sembol', 'seri_durum', 'seri_son', 'seri_n', 'sinif_son_k54', 'sinif_son_k56', 'sinif_on_k54', 'sinif_on_k56', 'sinif_degisti', 'n_temiz', 'veri_hatasi', 'veri_yetersiz', 'supheli_sicrama', 'bolunme_n']
   seri_durum {'TAMAM': 353, 'İNMEDİ': 3}
   isaretler_fiyat {'supheli_sicrama: muhtemel_bolunme': 11, 'veri_yetersiz: ciddi_bosluk_sayi': 7, 'supheli_sicrama: aciklanamayan_sicrama': 7, 'veri_yetersiz: sifir_hacim_pay_yuksek': 5, 'supheli_sicrama: muhtemel_bolunme;aciklanamayan_sicrama': 3, 'son işlem UYUMSUZ (en yakın çıkış belgesi 49 gün)': 1}
