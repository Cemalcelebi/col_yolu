# TANIM ADIMI 2 — ADIM A: ADAY ÖZELLİKLER (KEŞİF)

Üretim: 2026-11-23T16:19:46Z (UTC). Etiket: **KEŞİF** (Cemal'in 40 işareti hedef: VAR 14, YOK 26). GETİRİ YOK; bütün özellikler sinyal günü t dahil, t'de kesik veriden (kör sayfanın 121 barı ya da goz_uyum anahtarındaki nedensel özellikler).

**ÇOKLU KARŞILAŞTIRMA UYARISI:** 40 tek özellik x 2 yön x ~39 eşik ve 30 çift kural (ilk 6 adayın 15 çifti x VE / VEYA) aynı 40 sayfada denendi. 40 sayfada en iyi kuralın kappa'sı şans eseri yüksek çıkar (seçim yanlılığı); LOOCV bunu kısmen düzeltir ama sıralamada en yüksek LOOCV kappa'yı seçmek de yukarı yanlıdır. Bu yüzden buradaki sayılar bulgu değildir; seçilen kural YALNIZ ikinci bağımsız kör sette sınanır (TANIM2_ON_KAYIT.md).

## Seçim kuralı (önceden yazılı, aynen)

ADAY_1 = LOOCV kappa'sı en yüksek TEK özellikli kural; ADAY_2 = LOOCV kappa'sı en yüksek iki özellikli kural (ADAY_1'den LOOCV kappa'da en az 0,10 yüksek değilse ADAY_2 = yok, basit olan kalır); her ikisinin eşiği 40 sayfanın TAMAMIYLA yeniden seçilir ve SAYI olarak mühürlenir. Ayrıca KONTROL = eski Ş3 (değişmez).

## Seçilen kurallar

- **ADAY_1**: dip_bolge_n: son 40 barda dip bölgesi (alt %20) bar sayısı. Kural: VAR ⇔ dip_bolge_n >= 18.5 (NaN = YOK). 40 sayfada kappa 0.634, LOOCV kappa 0.634.
- **ADAY_2**: VAR ⇔ (dip_bolge_n >= 18.5) VEYA (F2 >= 0.00779846). 40 sayfada kappa 0.773, LOOCV kappa 0.773. Tanım: dip_bolge_n: son 40 barda dip bölgesi (alt %20) bar sayısı VEYA F2: hat eğimi (son / ilk dokunuş Low - 1).
- **KONTROL**: eski Ş3: F2 (hat eğimi) >= -0,01; 40 sayfada kappa 0.400 (ilk setin hükmü).

## Yeni özellikler (Cemal'in çizimlerinden; tanım ve pencere ölçümden önce yazıldı: tanim2.py TZ_YENI, ilk commit)

- **Y1_dip_tepki_konum**: dipten sonraki en yüksek tepkiye göre son fiyatın konumu: (C_t - lo) / (max H[jd..t] - lo); 1 = dip sonrası tepede, 0 = dipte (payda 0 ise NaN). Çizim: 5 (orta bölgede V dönüş, VAR)
- **Y2_dip_alt_yari**: dip bölgesinde kapanışların alt yarıda kalma payı: dip bölgesi = W'de L <= lo + 0,20 x (hi - lo) olan barlar; pay((C - L) / (H - L) < 0,5). Sözlü kural: 'alt fitili az mumlar' (kapanış dip bölgesinde aşağıda = savunma yok)
- **Y3_dokunus2_hacim**: dibe ikinci dokunuşta hacmin birincisine oranı: dokunuş barı = L <= lo x 1,03; ardışık dokunuş barları arasında 5 bardan fazla boşluk yeni dokunuş epizodu başlatır; ort V(2. epizot) / ort V(1. epizot); 2 epizot yoksa NaN
- **Y4_yukselen_dip_n**: dip sonrası yükselen dip sayısı (higher lows): pivot dip = j (jd < j <= t-3, j >= 3) ve L_j = min L[j-3..j+3]; sırayla her pivotun L'si bir öncekinden (ilki için lo) büyükse +1. Çizim: 12 (yıldız, VAR)
- **Y5_direnc_uzaklik**: tabanın üstündeki yatay direnç çizgisine uzaklık: R = max H[jd..t-1] (dip sonrası tavan, t hariç); C_t / R - 1 (< 0: fiyat direncin altında); jd = t ise NaN. Çizim: 2 (tabanın üstüne yatay direnç, YOK)
- **Y6_tepe_egim20**: son 20 mumun tepeleri düşüyor mu (dağıtım): H[t-19..t] doğrusal regresyon eğimi x 19 / ort H[t-19..t] (20 barlık göreli değişim; < 0 düşen tepeler). Çizim: 35 (tepe bölgesi, dağıtım, YOK)
- **Y7_v_hiz**: V dönüş hızı: dipten sonra ilk C_j >= 1,10 x lo olan bara kadar bar sayısı (j - jd); t'ye kadar olmadıysa 121 (küçük = hızlı V). Çizim: 5 (V dönüş, VAR)
- **Y8_dip_sonrasi_boy**: dip sonrası mumların ortalama boyunun düşüş mumlarına oranı: ort((H - L) / C, [jd+1..t]) / ort((H - L) / C, W içinde [0..jd] düşüş mumları C < O); dip sonrası 3 bardan ya da düşüş mumu 3'ten azsa NaN. Sözlü kural: 'dip savunması' (dip sonrası küçük mum)

## Tek özellik tablosu (LOOCV kappa sırasıyla)

Kural: VAR ⇔ özellik (yön) eşik; eşik 40 sayfada dengeli doğruluğu en yüksek yapan. VAR / YOK sütunları: medyan [q25, q75] (NaN sayısı).

| sıra | özellik | yön | eşik | dengeli doğr. | kappa (40) | LOOCV kappa | LOOCV uyum | kural VAR | Cemal VAR: medyan [q25, q75] (NaN) | Cemal YOK: medyan [q25, q75] (NaN) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dip_bolge_n | >= | 18.5 | 0.786 | 0.634 | 0.634 | 0.850 | 8 | 19.500 [12.500, 24.000] (0) | 10.500 [6.500, 14.000] (0) |
| 2 | dokunus_egim | >= | -0.00923083 | 0.758 | 0.485 | 0.485 | 0.750 | 18 | -0.001 [-0.009, 0.006] (0) | -0.010 [-0.012, 0.006] (8) |
| 3 | F17 | <= | -0.275689 | 0.723 | 0.424 | 0.424 | 0.725 | 17 | -0.290 [-0.354, -0.262] (0) | -0.253 [-0.279, -0.221] (0) |
| 4 | F18 | >= | 0.137957 | 0.695 | 0.441 | 0.367 | 0.750 | 7 | 0.129 [0.110, 0.156] (0) | 0.112 [0.094, 0.118] (0) |
| 5 | F22 | >= | 0.0129249 | 0.764 | 0.545 | 0.364 | 0.725 | 12 | 0.018 [0.001, 0.037] (0) | -0.001 [-0.019, 0.009] (0) |
| 6 | F2 | >= | -0.00515945 | 0.739 | 0.442 | 0.340 | 0.675 | 19 | 0.000 [-0.003, 0.008] (0) | -0.011 [-0.012, 0.002] (1) |
| 7 | hacim_dus_yuk | >= | 0.929741 | 0.668 | 0.319 | 0.319 | 0.675 | 17 | 0.955 [0.795, 1.033] (0) | 0.821 [0.666, 1.050] (0) |
| 8 | Y6_tepe_egim20 (yeni) | >= | -0.0187717 | 0.679 | 0.302 | 0.302 | 0.625 | 25 | 0.009 [-0.013, 0.024] (0) | -0.008 [-0.041, 0.021] (0) |
| 9 | F13 | >= | 1.77654 | 0.723 | 0.424 | 0.297 | 0.675 | 17 | 2.070 [1.392, 2.324] (0) | 1.384 [1.040, 1.887] (0) |
| 10 | Y7_v_hiz (yeni) | <= | 1.5 | 0.624 | 0.290 | 0.290 | 0.725 | 5 | 5.500 [1.250, 13.500] (0) | 5.500 [3.000, 10.250] (0) |
| 11 | F5 | <= | 0.537976 | 0.681 | 0.320 | 0.261 | 0.625 | 22 | 0.500 [0.451, 0.528] (0) | 0.549 [0.426, 0.632] (0) |
| 12 | F9 | >= | 0.106929 | 0.706 | 0.405 | 0.255 | 0.650 | 15 | 0.109 [0.101, 0.118] (0) | 0.102 [0.085, 0.107] (0) |
| 13 | F16 | >= | 0.5 | 0.629 | 0.239 | 0.239 | 0.625 | 19 | 1.000 [0.000, 1.750] (0) | 0.000 [0.000, 1.000] (0) |
| 14 | dibe_dokunus | >= | 1.5 | 0.654 | 0.237 | 0.237 | 0.550 | 32 | 2.500 [2.000, 4.000] (0) | 2.000 [1.000, 3.000] (0) |
| 15 | F19 | >= | 0.5 | 0.588 | 0.211 | 0.211 | 0.700 | 4 | 0.000 [0.000, 0.000] (0) | 0.000 [0.000, 0.000] (0) |
| 16 | fitil40 | <= | 0.26624 | 0.646 | 0.261 | 0.200 | 0.600 | 21 | 0.257 [0.232, 0.278] (0) | 0.267 [0.248, 0.297] (0) |
| 17 | Y2_dip_alt_yari (yeni) | >= | 0.616516 | 0.695 | 0.441 | 0.176 | 0.650 | 7 | 0.593 [0.522, 0.637] (0) | 0.544 [0.500, 0.578] (0) |
| 18 | low20_onceki20 | >= | 0.984121 | 0.646 | 0.261 | 0.163 | 0.575 | 21 | 1.006 [0.969, 1.034] (0) | 0.972 [0.939, 1.023] (0) |
| 19 | F10 | >= | -0.0138913 | 0.618 | 0.185 | 0.153 | 0.500 | 31 | 0.004 [-0.010, 0.018] (0) | 0.003 [-0.017, 0.020] (0) |
| 20 | F14 | <= | -0.200312 | 0.706 | 0.405 | 0.133 | 0.625 | 15 | -0.264 [-0.713, 0.058] (0) | -0.023 [-0.189, 0.185] (0) |
| 21 | fitil20 | <= | 0.271724 | 0.607 | 0.187 | 0.126 | 0.550 | 23 | 0.263 [0.236, 0.284] (0) | 0.265 [0.232, 0.298] (0) |
| 22 | F3 | >= | 0.570327 | 0.599 | 0.153 | 0.121 | 0.475 | 32 | 0.749 [0.623, 0.832] (0) | 0.698 [0.574, 0.820] (0) |
| 23 | F4 | <= | 0.24853 | 0.610 | 0.200 | 0.100 | 0.550 | 20 | 0.234 [0.197, 0.316] (0) | 0.255 [0.186, 0.303] (0) |
| 24 | Y4_yukselen_dip_n (yeni) | >= | 0.5 | 0.563 | 0.099 | 0.099 | 0.475 | 31 | 2.000 [1.000, 2.750] (0) | 2.000 [0.250, 3.000] (0) |
| 25 | Y5_direnc_uzaklik (yeni) | >= | -0.00156839 | 0.643 | 0.245 | 0.029 | 0.500 | 24 | 0.007 [0.001, 0.013] (0) | -0.001 [-0.059, 0.015] (0) |
| 26 | F15 | <= | 0.138143 | 0.624 | 0.290 | -0.049 | 0.625 | 5 | 0.208 [0.147, 0.222] (0) | 0.207 [0.162, 0.222] (0) |
| 27 | F23 | <= | 0.506405 | 0.585 | 0.193 | -0.061 | 0.525 | 7 | 0.761 [0.508, 0.908] (0) | 0.797 [0.605, 0.899] (0) |
| 28 | Y1_dip_tepki_konum (yeni) | >= | 0.830362 | 0.604 | 0.174 | -0.100 | 0.425 | 26 | 0.926 [0.836, 0.970] (0) | 0.889 [0.666, 0.962] (0) |
| 29 | F11 | >= | 0.0203429 | 0.654 | 0.318 | -0.135 | 0.475 | 12 | 0.019 [0.008, 0.034] (0) | 0.009 [0.003, 0.019] (0) |
| 30 | F7 | <= | 0.533597 | 0.635 | 0.205 | -0.155 | 0.275 | 33 | 0.451 [0.403, 0.500] (0) | 0.432 [0.385, 0.538] (0) |
| 31 | F22a | >= | -0.0483788 | 0.640 | 0.231 | -0.165 | 0.400 | 27 | -0.016 [-0.046, -0.007] (0) | -0.033 [-0.061, -0.013] (0) |
| 32 | F21 | <= | 26.0356 | 0.588 | 0.151 | -0.168 | 0.425 | 24 | 15.785 [9.192, 41.853] (0) | 23.317 [9.649, 51.583] (0) |
| 33 | F6 | >= | 0.263854 | 0.591 | 0.163 | -0.243 | 0.425 | 21 | 0.275 [0.221, 0.360] (0) | 0.262 [0.202, 0.319] (0) |
| 34 | Y3_dokunus2_hacim (yeni) | >= | 0.262198 | 0.577 | 0.149 | -0.243 | 0.425 | 16 | 0.906 [0.590, 1.164] (7) | 0.957 [0.525, 2.136] (14) |
| 35 | dip_bolge_fitil | <= | 0.300577 | 0.624 | 0.209 | -0.322 | 0.200 | 25 | 0.279 [0.261, 0.300] (0) | 0.299 [0.232, 0.336] (0) |
| 36 | F12 | <= | 1.00833 | 0.615 | 0.231 | -0.377 | 0.425 | 14 | 1.033 [0.724, 1.620] (0) | 1.221 [1.004, 1.560] (0) |
| 37 | Y8_dip_sonrasi_boy (yeni) | >= | 0.810982 | 0.626 | 0.223 | -0.416 | 0.175 | 22 | 0.851 [0.793, 0.904] (0) | 0.810 [0.729, 1.000] (1) |
| 38 | F1 | <= | 2.5 | 0.558 | 0.110 | -0.477 | 0.350 | 17 | 2.500 [2.000, 4.000] (0) | 3.000 [2.000, 4.000] (0) |
| 39 | F8 | <= | 10.5 | 0.602 | 0.222 | -0.538 | 0.300 | 9 | 17.000 [10.000, 21.750] (0) | 14.000 [13.000, 23.250] (0) |
| 40 | F20 | >= | 4.13068e-05 | 0.599 | 0.153 | -0.835 | 0.000 | 32 | 0.011 [0.005, 0.038] (0) | 0.013 [-0.000, 0.032] (0) |

## Çift kurallar (ilk 6: dip_bolge_n, dokunus_egim, F17, F18, F22, F2; LOOCV kappa sırasıyla)

| sıra | A | yön A | eşik A | op | B | yön B | eşik B | dengeli doğr. | kappa (40) | LOOCV kappa | LOOCV uyum | kural VAR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dip_bolge_n | >= | 18.5 | VEYA | F2 | >= | 0.00779846 | 0.874 | 0.773 | 0.773 | 0.900 | 12 |
| 2 | dip_bolge_n | >= | 18.5 | VEYA | F18 | >= | 0.140028 | 0.857 | 0.765 | 0.711 | 0.875 | 10 |
| 3 | dip_bolge_n | >= | 18.5 | VEYA | F22 | >= | 0.0371164 | 0.857 | 0.765 | 0.701 | 0.875 | 10 |
| 4 | dip_bolge_n | >= | 18.5 | VE | F18 | >= | 0.0707646 | 0.786 | 0.634 | 0.634 | 0.850 | 8 |
| 5 | dokunus_egim | >= | -0.0128715 | VE | F17 | <= | -0.275689 | 0.819 | 0.659 | 0.595 | 0.825 | 12 |
| 6 | dip_bolge_n | >= | 18.5 | VE | F22 | >= | -0.0416304 | 0.786 | 0.634 | 0.565 | 0.825 | 8 |
| 7 | dip_bolge_n | >= | 18.5 | VEYA | dokunus_egim | >= | 0.00836474 | 0.819 | 0.659 | 0.529 | 0.800 | 12 |
| 8 | dokunus_egim | >= | -0.00923083 | VE | F18 | >= | 0.0909063 | 0.777 | 0.529 | 0.529 | 0.775 | 17 |
| 9 | dokunus_egim | >= | -0.00923083 | VEYA | F18 | >= | 0.150895 | 0.794 | 0.543 | 0.500 | 0.750 | 19 |
| 10 | F17 | <= | -0.275689 | VE | F22 | >= | -0.00795718 | 0.783 | 0.595 | 0.497 | 0.775 | 11 |
| 11 | dokunus_egim | <= | 0.0144935 | VE | F2 | >= | -0.00515945 | 0.816 | 0.622 | 0.451 | 0.750 | 15 |
| 12 | F17 | <= | -0.275689 | VEYA | F18 | >= | 0.140028 | 0.794 | 0.543 | 0.442 | 0.725 | 19 |
| 13 | dip_bolge_n | >= | 18.5 | VEYA | F17 | <= | -0.277764 | 0.830 | 0.600 | 0.424 | 0.725 | 20 |
| 14 | dokunus_egim | >= | -0.00923083 | VE | F22 | >= | -0.00156839 | 0.799 | 0.609 | 0.385 | 0.725 | 13 |
| 15 | F17 | <= | -0.275689 | VEYA | F22 | >= | 0.0210149 | 0.810 | 0.557 | 0.381 | 0.700 | 21 |
| 16 | F18 | >= | 0.140028 | VEYA | F22 | >= | 0.0129249 | 0.764 | 0.545 | 0.364 | 0.725 | 12 |
| 17 | F18 | >= | 0.0944421 | VE | F2 | >= | -0.00817697 | 0.797 | 0.574 | 0.362 | 0.700 | 16 |
| 18 | F17 | <= | -0.275689 | VE | F18 | >= | 0.0944421 | 0.742 | 0.468 | 0.362 | 0.700 | 16 |
| 19 | F22 | >= | 0.00982005 | VE | F2 | >= | -0.0106883 | 0.766 | 0.581 | 0.341 | 0.725 | 9 |
| 20 | F22 | >= | 0.0210149 | VEYA | F2 | >= | 0.00693001 | 0.819 | 0.659 | 0.318 | 0.700 | 12 |
| 21 | dip_bolge_n | >= | 18.5 | VE | dokunus_egim | <= | 0.0144935 | 0.786 | 0.634 | 0.294 | 0.700 | 8 |
| 22 | F17 | <= | -0.256083 | VE | F2 | >= | -0.0106883 | 0.780 | 0.560 | 0.278 | 0.650 | 14 |
| 23 | dip_bolge_n | >= | 18.5 | VE | F2 | >= | -0.0133317 | 0.786 | 0.634 | 0.274 | 0.675 | 8 |
| 24 | F18 | >= | 0.0953984 | VE | F22 | >= | 0.0129249 | 0.783 | 0.595 | 0.189 | 0.625 | 11 |
| 25 | F18 | >= | 0.140028 | VEYA | F2 | >= | -0.00515945 | 0.810 | 0.557 | 0.175 | 0.600 | 21 |
| 26 | dokunus_egim | >= | -0.00923083 | VEYA | F17 | >= | -0.208329 | 0.758 | 0.485 | 0.163 | 0.575 | 18 |
| 27 | F17 | >= | -0.204162 | VEYA | F2 | >= | -0.00515945 | 0.775 | 0.500 | 0.151 | 0.550 | 20 |
| 28 | dip_bolge_n | >= | 18.5 | VE | F17 | >= | -0.378747 | 0.750 | 0.565 | 0.059 | 0.600 | 7 |
| 29 | dokunus_egim | <= | -0.0140197 | VEYA | F22 | >= | 0.0129249 | 0.799 | 0.609 | 0.036 | 0.525 | 13 |
| 30 | dokunus_egim | <= | 0.00149999 | VEYA | F2 | >= | 0.00693001 | 0.769 | 0.450 | -0.071 | 0.400 | 26 |

## Cemal'in çizim sayfalarında yeni özellikler (bilgi)

| sayfa | Cemal | Y1_dip_tepki_konum | Y2_dip_alt_yari | Y3_dokunus2_hacim | Y4_yukselen_dip_n | Y5_direnc_uzaklik | Y6_tepe_egim20 | Y7_v_hiz | Y8_dip_sonrasi_boy |
|---|---|---|---|---|---|---|---|---|---|
| 2 | YOK | 0.826 | 0.533 | — | 2.000 | -0.017 | 0.006 | 5.000 | 1.188 |
| 5 | VAR | 0.909 | 0.654 | 0.299 | 0.000 | 0.003 | 0.096 | 2.000 | 0.768 |
| 12 | VAR | 0.834 | 0.667 | — | 4.000 | 0.063 | 0.026 | 32.000 | 0.812 |
| 35 | YOK | 0.932 | 0.469 | 0.625 | 2.000 | 0.027 | 0.008 | 26.000 | 0.723 |

Çizimler: 2 = tabanın üstünde yatay direnç (YOK), 35 = tepe bölgesi / dağıtım (YOK), 5 = orta bölgede V dönüş (VAR), 12 = yıldız (VAR).
