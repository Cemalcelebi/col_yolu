# K54 — TARİHSEL HİSSE EVRENİ SAĞLAMLIK DENETİMİ (v1.5, ön kayıt d4dcdfb + ek 8 5fa687d; düzeltilmiş koşu)

K54 yeni iz araştırması değildir. K51 / K52 / K53 ön kayıtları ve kararları değişmedi (K51 İZ DEĞİL). Eski dosyalar üzerine yazılmadı; ilk K54 koşusu (ac63f0d) git geçmişinde. Bu koşu ek 8'in dört düzeltmesini ve ortak örneklem deneyini uygular.

- Evren 3267 sembol; panel 3175671 likit hisse-gün (A); düzeltilmiş evren 3171992 satır (B); ortak örneklem 3171992 satır (C); sınıf 6 dahil 3171992 satır; 2752 hisse; süre 3.2 dk; kod CY v1.5 (2026-10-30, K54 tarihsel evren sağlamlık denetimi + ek 8: sınıf 1 / 2 / 4a doğrulama, sınıf 6 bandı, ortak örneklem A / B / C; v1.4 K53 bilgi direnci / analist dağınıklığı / karar gecikmesi; v1.3 K52 grafik izi + analist revizyonları: Yahoo not günlüğü, dört grup, H0-H6; v1.2 K51 sonrası bağımsız denetim: veri bütünlüğü, kırılganlık, eşleşmiş kontrollerle H-A..H-E; v1.1 K51 ABD Çöl Yolu: üçlü bariyer (sabit + oynaklık), meta-etiketleme, model merdiveni LR/GBM/CNN/LSTM, PBO/DSR, batanlar dahil), commit 0ad1c90.
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
- Sembol başına kural ve kanıt tarihleri K54_SIRKET_DURUMU.csv'de; K51'in eski tahmini K51_EVREN_PIT.csv 'cikis_turu_tahmin' ile birleştirilerek görülür.

### 1.1 Sınıf 1 doğrulaması (ek 8.1: SEC güncel sembolü tek başına kanıt değil)

- Tiingo + SEC: 2831
- yalnız Tiingo (SEC sembol listesi boş): 159
- yalnız SEC, Tiingo'da yok → belirsiz: 10
- yalnız SEC, Tiingo bitiş çelişiyor → belirsiz: 1
- Belirsiz işaretli sınıf 1: 11 sembol (BOXL, CIRC, DBA, DBB, DBO, FIEE, NGTF, SNBRQ, UNG, UNL, UUP). Seri 2026-08-01 sonrasına sürdüğü için çıkış işlemi yok; K51 P1 / P2 hücreleri bu semboller çıkarılarak ayrıca hesaplandı (3.1 duyarlılık satırları).
- Belirsizlerin Tiingo ham türü (Stock süzgeci dışında kalma nedeni): BOXL: ETF; CIRC: ETF / Stock; DBA: ETF; DBB: ETF; DBO: ETF; FIEE: ETF; NGTF: Tiingo'da yok; SNBRQ: Tiingo'da yok; UNG: ETF; UNL: ETF; UUP: ETF. Tiingo'nun 'ETF' dediği semboller ya gerçekten ETF'dir (K51 evreninde hisse olmayan sembol: evren temizliği maddesi) ya da Tiingo tür hatasıdır; hangisi olduğu bu çalışmada çözülmedi, kayıt belirsiz kaldı.

### 1.2 Sınıf 2 kronolojisi (ek 8.2: 8-K madde 1.03 başvurusunun T'ye göre zamanı)

- 19 sembol; başvuru T'den önce 18, aynı gün 1, T'den sonra 0; fark (başvuru − T, gün) en az -322, medyan -174, en çok 0.
- Başvuru çoğunlukla T'den önce: iflas duyurusundan sonra hisse pembe tahtada ('Q' eki) bir süre daha işlem görmüş, T o işlemin bittiği gündür. Sınıf atanması (±365 gün) değişmedi; kronoloji kanıt olarak aşağıda.

| sembol | son_islem | b103_tarih | b103_T_fark_gun | b103_zaman | b103_tarihler | nse25_tarih | son_10k_10q |
|---|---|---|---|---|---|---|---|
| BASXQ | 2022-08-26 | 2021-10-08 | -322 | T'den 322 gün önce | 2021-10-08 |  | 2021-05-17 |
| TLGTQ | 2022-07-27 | 2021-10-15 | -285 | T'den 285 gün önce | 2021-10-15 | 2021-10-27 | 2021-08-16 |
| IMBIQ | 2024-04-01 | 2023-06-29 | -277 | T'den 277 gün önce | 2023-06-29;2024-02-27 | 2023-07-27 | 2022-12-13 |
| AMRSQ | 2024-05-07 | 2023-08-10 | -271 | T'den 271 gün önce | 2023-08-10;2024-02-09 | 2023-09-08 | 2023-05-10 |
| NSTGQ | 2024-10-16 | 2024-02-05 | -254 | T'den 254 gün önce | 2024-02-05;2024-02-13;2024-06-26 | 2024-04-09 | 2023-11-06 |
| CLVSQ | 2023-07-25 | 2022-12-13 | -224 | T'den 224 gün önce | 2022-12-13;2023-07-11 | 2022-12-29 | 2022-11-09 |
| LHDXQ | 2023-10-04 | 2023-02-22 | -224 | T'den 224 gün önce | 2023-02-22;2023-09-25 | 2023-04-12 | 2022-11-14 |
| STRYQ | 2023-09-01 | 2023-02-21 | -192 | T'den 192 gün önce | 2023-02-21 | 2022-12-30 | 2022-11-09 |
| CDAKQ | 2023-09-18 | 2023-03-27 | -175 | T'den 175 gün önce | 2023-03-27 | 2023-05-02 | 2022-11-03 |
| TMBRQ | 2024-05-09 | 2023-11-17 | -174 | T'den 174 gün önce | 2023-11-17;2024-01-23;2024-05-09;2024-05-09 | 2023-11-29 | 2023-08-21 |
| PLXPQ | 2023-09-29 | 2023-04-13 | -169 | T'den 169 gün önce | 2023-04-13;2023-05-26;2023-09-20 | 2023-05-02 | 2022-11-10 |
| NOGNQ | 2024-05-03 | 2023-12-11 | -144 | T'den 144 gün önce | 2023-12-11;2024-04-03;2024-05-09 | 2024-02-15 | 2023-11-22 |
| ATNXQ | 2023-10-02 | 2023-05-22 | -133 | T'den 133 gün önce | 2023-05-22;2023-07-18;2023-10-02 | 2023-07-10 | 2023-04-28 |
| TRKAQ | 2024-04-09 | 2023-12-07 | -124 | T'den 124 gün önce | 2023-12-07;2024-03-05;2024-04-01 | 2023-12-27 | 2023-12-21 |
| FSRDQ | 2023-03-06 | 2022-11-08 | -118 | T'den 118 gün önce | 2022-11-08;2022-12-14 | 2022-02-04 | 2022-11-14 |
| IMPLQ | 2024-04-05 | 2023-12-20 | -107 | T'den 107 gün önce | 2023-12-20;2024-02-14 | 2023-12-27 | 2023-11-14 |
| SUNLQ | 2023-12-15 | 2023-10-31 | -45 | T'den 45 gün önce | 2023-10-31;2023-11-13;2023-12-07 | 2023-10-10 | 2023-08-09 |
| GMDAQ | 2024-05-24 | 2024-04-22 | -32 | T'den 32 gün önce | 2024-04-22 | 2024-04-25 | 2024-05-23 |
| ID | 2023-12-26 | 2023-12-26 | 0 | T ile aynı gün | 2023-12-26;2024-02-09;2024-02-28 | 2024-01-03 | 2023-12-08 |

### 1.3 Sınıf 4a doğrulaması (ek 8.3: son kapanış otomatik nakit bedel değil)

- Bu evrende seri erken bitip T'den ≥ 180 gün sonra 10-K / 10-Q vermeye devam eden şirket yok (sınıf 4a n = 0); doğrulama kuralı kodda ve testte var, uygulanacak kayıt çıkmadı. Sebep: V_ABD ve K34 Yahoo serileri bugünkü sembol altında geriye doğru doldurulmuştur (sembol değiştiren şirket yeni sembolüyle tam seri taşır); eski sembollü seriler yalnız Tiingo'nun nakdi biten 422'lik örneklemindedir.

## 2. Delist duyarlılığı (sınıf başına sayılar; P1 / P2 hücrelerinin −%0 / −%30 / −%100 bandı ve düzeltilmiş etiket; 4a doğrulanamayan bandı)

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
| P1 bandı, yalnız 4a doğrulanamayan | 2016-22 | 0 | 0 |  |  |  |  |  |
| P1 bandı | 2023 | 906 | 42 | +0.313 | +0.313 | +0.313 | +0.311 | +0.000 |
| P1 bandı, yalnız 4a doğrulanamayan | 2023 | 0 | 0 |  |  |  |  |  |
| P1 bandı | 2024-26 | 1316 | 23 | +0.357 | +0.357 | +0.357 | +0.356 | +0.000 |
| P1 bandı, yalnız 4a doğrulanamayan | 2024-26 | 0 | 0 |  |  |  |  |  |
| P2 bandı | 2016-22 | 571 | 9 | +0.255 | +0.255 | +0.255 | +0.255 | +0.000 |
| P2 bandı, yalnız 4a doğrulanamayan | 2016-22 | 0 | 0 |  |  |  |  |  |
| P2 bandı | 2023 | 476 | 25 | +0.286 | +0.286 | +0.286 | +0.283 | +0.000 |
| P2 bandı, yalnız 4a doğrulanamayan | 2023 | 0 | 0 |  |  |  |  |  |
| P2 bandı | 2024-26 | 667 | 13 | +0.324 | +0.324 | +0.324 | +0.325 | +0.000 |
| P2 bandı, yalnız 4a doğrulanamayan | 2024-26 | 0 | 0 |  |  |  |  |  |

## 3. A (eski evren) / B (düzeltilmiş evren) / C (ortak örneklem) — aynı tanım ve eşikler

Taban-ayarlı isabet = y − e_y (aynı gün, aynı oynaklık ondalığı; taban her örneklemde kendi satırlarında yeniden). A: K51 etiketi, bütün satırlar. B: düzeltilmiş etiket, sınıf 6 ve 4b kesim sonrası çıkarılmış. C: iki evrende ortak satırlar; C-eski = K51 etiketi, C-yeni = düzeltilmiş etiket (C-yeni ≡ B, çünkü B ⊂ A). Ayrıştırma (puan): evren etkisi = C-eski − A; etiket etkisi = C-yeni − C-eski; toplam (fark_fark) = B − A. Değerlendirme A ile B arasında: SAĞLAM (≤ 2 puan, karar ve aralık aynı), ETKİLENMİŞ, GEÇERSİZ (sınıf 5 + 6 payı > %30 ya da evren kurulamıyor).

### 3.1 K51 temel hücreleri (A / B / C ve ayrıştırma)

| kume | donem | eski_n | ortak_eski_n | yeni_n | eski_ust_oran | yeni_ust_oran | eski_alt_oran | yeni_alt_oran | eski_net | yeni_net | eski_fark | eski_fark_alt | eski_fark_ust | ortak_eski_fark | ortak_eski_fark_alt | ortak_eski_fark_ust | yeni_fark | yeni_fark_alt | yeni_fark_ust | evren_etkisi | etiket_etkisi | fark_fark | eski_karar | ortak_eski_karar | yeni_karar | sinif56_pay_olay | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K51 P1 | 2016-22 | 1415 | 1415 | 1415 | +0.286 | +0.286 | +0.646 | +0.646 | -0.026 | -0.026 | +0.018 | -0.004 | +0.042 | +0.017 | -0.004 | +0.042 | +0.017 | -0.005 | +0.041 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 (en iyi 20 çıkarıldı) | 2016-22 | 1355 | 1355 | 1355 | +0.262 | +0.262 | +0.667 | +0.667 | -0.033 | -0.033 | -0.005 | -0.028 | +0.019 | -0.005 | -0.028 | +0.019 | -0.005 | -0.029 | +0.019 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 | 2023 | 906 | 905 | 905 | +0.313 | +0.311 | +0.614 | +0.615 | -0.018 | -0.019 | +0.025 | -0.006 | +0.061 | +0.024 | -0.007 | +0.060 | +0.024 | -0.008 | +0.059 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 (en iyi 20 çıkarıldı) | 2023 | 848 | 847 | 847 | +0.283 | +0.282 | +0.639 | +0.641 | -0.027 | -0.027 | -0.002 | -0.036 | +0.035 | -0.003 | -0.036 | +0.032 | -0.003 | -0.035 | +0.033 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 P1 | 2024-26 | 1316 | 1314 | 1314 | +0.357 | +0.356 | +0.603 | +0.603 | -0.011 | -0.011 | +0.024 | +0.000 | +0.050 | +0.023 | -0.001 | +0.049 | +0.023 | -0.000 | +0.049 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | ETKİLENMİŞ |
| K51 P1 (en iyi 20 çıkarıldı) | 2024-26 | 1256 | 1254 | 1254 | +0.332 | +0.332 | +0.625 | +0.626 | -0.019 | -0.019 | +0.000 | -0.022 | +0.024 | -0.001 | -0.022 | +0.021 | -0.001 | -0.023 | +0.021 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 P2 | 2016-22 | 571 | 571 | 571 | +0.255 | +0.255 | +0.614 | +0.611 | -0.022 | -0.022 | -0.013 | -0.045 | +0.019 | -0.013 | -0.045 | +0.019 | -0.013 | -0.046 | +0.019 | -0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2016-22 | 537 | 537 | 537 | +0.217 | +0.217 | +0.646 | +0.642 | -0.032 | -0.032 | -0.055 | -0.093 | -0.021 | -0.055 | -0.092 | -0.021 | -0.055 | -0.092 | -0.020 | -0.000 | +0.000 | +0.000 | TERS YÖN | TERS YÖN | TERS YÖN | +0.002 | SAĞLAM |
| K51 P2 | 2023 | 476 | 475 | 475 | +0.286 | +0.283 | +0.581 | +0.583 | -0.020 | -0.021 | +0.010 | -0.024 | +0.053 | +0.008 | -0.027 | +0.057 | +0.008 | -0.027 | +0.057 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2023 | 455 | 454 | 454 | +0.252 | +0.249 | +0.608 | +0.611 | -0.030 | -0.031 | -0.031 | -0.058 | +0.009 | -0.033 | -0.059 | +0.007 | -0.033 | -0.060 | +0.006 | -0.002 | +0.000 | -0.002 | TUTMAZ | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 P2 | 2024-26 | 667 | 666 | 666 | +0.324 | +0.325 | +0.616 | +0.614 | -0.021 | -0.021 | +0.006 | -0.018 | +0.034 | +0.007 | -0.018 | +0.036 | +0.007 | -0.017 | +0.037 | +0.000 | +0.000 | +0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 P2 (en iyi 20 çıkarıldı) | 2024-26 | 627 | 626 | 626 | +0.285 | +0.286 | +0.651 | +0.650 | -0.032 | -0.032 | -0.031 | -0.055 | -0.005 | -0.031 | -0.055 | -0.004 | -0.031 | -0.054 | -0.001 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ES | 2016-22 | 2316 | 2315 | 2315 | +0.300 | +0.299 | +0.638 | +0.639 | -0.025 | -0.026 | +0.010 | -0.009 | +0.030 | +0.010 | -0.010 | +0.029 | +0.010 | -0.010 | +0.029 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2016-22 | 2228 | 2227 | 2227 | +0.286 | +0.285 | +0.652 | +0.652 | -0.030 | -0.030 | -0.004 | -0.026 | +0.015 | -0.005 | -0.026 | +0.014 | -0.005 | -0.025 | +0.014 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.002 | SAĞLAM |
| K51 ES | 2023 | 896 | 896 | 896 | +0.311 | +0.311 | +0.612 | +0.612 | -0.021 | -0.021 | -0.002 | -0.028 | +0.021 | -0.003 | -0.030 | +0.021 | -0.003 | -0.029 | +0.022 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2023 | 857 | 857 | 857 | +0.283 | +0.283 | +0.638 | +0.638 | -0.030 | -0.030 | -0.029 | -0.055 | -0.005 | -0.029 | -0.053 | -0.004 | -0.029 | -0.055 | -0.004 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ES | 2024-26 | 2382 | 2377 | 2377 | +0.342 | +0.342 | +0.589 | +0.589 | -0.007 | -0.007 | +0.008 | -0.015 | +0.032 | +0.009 | -0.016 | +0.032 | +0.009 | -0.016 | +0.033 | +0.001 | -0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ES (en iyi 20 çıkarıldı) | 2024-26 | 2316 | 2311 | 2311 | +0.329 | +0.329 | +0.601 | +0.601 | -0.011 | -0.011 | -0.006 | -0.031 | +0.017 | -0.005 | -0.031 | +0.018 | -0.006 | -0.032 | +0.017 | +0.001 | -0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 HT | 2016-22 | 163 | 163 | 163 | +0.340 | +0.340 | +0.592 | +0.592 | -0.013 | -0.013 | +0.035 | -0.054 | +0.117 | +0.035 | -0.052 | +0.121 | +0.035 | -0.051 | +0.118 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.012 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2016-22 | 140 | 140 | 140 | +0.233 | +0.233 | +0.688 | +0.688 | -0.044 | -0.044 | -0.093 | -0.162 | -0.025 | -0.093 | -0.164 | -0.025 | -0.093 | -0.167 | -0.022 | -0.000 | +0.000 | -0.000 | TERS YÖN | TERS YÖN | TERS YÖN | +0.012 | SAĞLAM |
| K51 HT | 2023 | 58 | 58 | 58 | +0.276 | +0.276 | +0.724 | +0.724 | -0.045 | -0.045 | -0.055 | -0.147 | +0.033 | -0.055 | -0.147 | +0.041 | -0.055 | -0.142 | +0.037 | +0.000 | -0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2023 | 37 | 37 | 37 | +0.000 | +0.000 | +1.000 | +1.000 | -0.127 | -0.127 | -0.318 | -0.397 | -0.235 | -0.318 | -0.397 | -0.239 | -0.318 | -0.392 | -0.237 | -0.000 | -0.000 | -0.000 | TERS YÖN | TERS YÖN | TERS YÖN | +0.000 | SAĞLAM |
| K51 HT | 2024-26 | 191 | 191 | 191 | +0.331 | +0.331 | +0.650 | +0.650 | -0.027 | -0.027 | -0.012 | -0.060 | +0.041 | -0.012 | -0.060 | +0.042 | -0.012 | -0.061 | +0.041 | -0.000 | -0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 HT (en iyi 20 çıkarıldı) | 2024-26 | 167 | 167 | 167 | +0.241 | +0.241 | +0.737 | +0.737 | -0.054 | -0.054 | -0.121 | -0.170 | -0.066 | -0.121 | -0.171 | -0.067 | -0.121 | -0.172 | -0.068 | +0.000 | -0.000 | +0.000 | TERS YÖN | TERS YÖN | TERS YÖN | +0.000 | SAĞLAM |
| K51 ÇEK | 2016-22 | 4193 | 4192 | 4192 | +0.286 | +0.286 | +0.647 | +0.646 | -0.027 | -0.027 | +0.006 | -0.008 | +0.019 | +0.006 | -0.008 | +0.020 | +0.006 | -0.008 | +0.019 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2016-22 | 4051 | 4050 | 4050 | +0.275 | +0.275 | +0.656 | +0.655 | -0.030 | -0.030 | -0.005 | -0.019 | +0.008 | -0.005 | -0.019 | +0.008 | -0.005 | -0.019 | +0.009 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK | 2023 | 1983 | 1982 | 1982 | +0.314 | +0.313 | +0.607 | +0.607 | -0.019 | -0.019 | +0.007 | -0.009 | +0.025 | +0.007 | -0.010 | +0.024 | +0.007 | -0.010 | +0.025 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2023 | 1924 | 1923 | 1923 | +0.297 | +0.297 | +0.621 | +0.622 | -0.024 | -0.024 | -0.010 | -0.027 | +0.010 | -0.011 | -0.028 | +0.008 | -0.011 | -0.028 | +0.008 | -0.000 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.001 | SAĞLAM |
| K51 ÇEK | 2024-26 | 4192 | 4187 | 4187 | +0.347 | +0.347 | +0.592 | +0.593 | -0.007 | -0.007 | +0.016 | -0.002 | +0.036 | +0.016 | -0.003 | +0.037 | +0.016 | -0.003 | +0.037 | -0.000 | -0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| K51 ÇEK (en iyi 20 çıkarıldı) | 2024-26 | 4086 | 4081 | 4081 | +0.337 | +0.337 | +0.601 | +0.602 | -0.010 | -0.010 | +0.005 | -0.014 | +0.025 | +0.005 | -0.014 | +0.026 | +0.005 | -0.014 | +0.025 | -0.000 | -0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |

### 3.1b Duyarlılık satırları (ek 8.1 sınıf 1 belirsiz çıkarılmış; ek 8.4 sınıf 6 −%30 / −%100 dahil; 'yeni_*' sütunları bu varyantı, 'eski_*' A'yı gösterir)

- Sınıf 6 sembol sayısı: 0. Sınıf 6 boşsa 'sınıf 6 dahil' varyantları B ile birebir aynıdır (satırlar yine de yazıldı).

| kume | donem | eski_n | yeni_n | eski_fark | eski_fark_alt | eski_fark_ust | yeni_fark | yeni_fark_alt | yeni_fark_ust | fark_fark | eski_karar | yeni_karar | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K51 P1 (sınıf 6 −%30 dahil) | 2016-22 | 1415 | 1415 | +0.018 | -0.004 | +0.042 | +0.017 | -0.004 | +0.042 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 6 −%100 dahil) | 2016-22 | 1415 | 1415 | +0.018 | -0.004 | +0.042 | +0.017 | -0.003 | +0.042 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 1 belirsiz çıkarıldı) | 2016-22 | 1415 | 1415 | +0.018 | -0.004 | +0.042 | +0.018 | -0.005 | +0.042 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 6 −%30 dahil) | 2023 | 906 | 905 | +0.025 | -0.006 | +0.061 | +0.024 | -0.009 | +0.057 | -0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 6 −%100 dahil) | 2023 | 906 | 905 | +0.025 | -0.006 | +0.061 | +0.024 | -0.006 | +0.058 | -0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 1 belirsiz çıkarıldı) | 2023 | 906 | 901 | +0.025 | -0.006 | +0.061 | +0.025 | -0.006 | +0.060 | +0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P1 (sınıf 6 −%30 dahil) | 2024-26 | 1316 | 1314 | +0.024 | +0.000 | +0.050 | +0.023 | -0.002 | +0.048 | -0.001 | TUTMAZ | TUTMAZ | ETKİLENMİŞ |
| K51 P1 (sınıf 6 −%100 dahil) | 2024-26 | 1316 | 1314 | +0.024 | +0.000 | +0.050 | +0.023 | -0.002 | +0.048 | -0.001 | TUTMAZ | TUTMAZ | ETKİLENMİŞ |
| K51 P1 (sınıf 1 belirsiz çıkarıldı) | 2024-26 | 1316 | 1310 | +0.024 | +0.000 | +0.050 | +0.024 | -0.000 | +0.048 | +0.000 | TUTMAZ | TUTMAZ | ETKİLENMİŞ |
| K51 P2 (sınıf 6 −%30 dahil) | 2016-22 | 571 | 571 | -0.013 | -0.045 | +0.019 | -0.013 | -0.047 | +0.018 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 6 −%100 dahil) | 2016-22 | 571 | 571 | -0.013 | -0.045 | +0.019 | -0.013 | -0.047 | +0.021 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 1 belirsiz çıkarıldı) | 2016-22 | 571 | 571 | -0.013 | -0.045 | +0.019 | -0.013 | -0.044 | +0.020 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 6 −%30 dahil) | 2023 | 476 | 475 | +0.010 | -0.024 | +0.053 | +0.008 | -0.027 | +0.055 | -0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 6 −%100 dahil) | 2023 | 476 | 475 | +0.010 | -0.024 | +0.053 | +0.008 | -0.028 | +0.056 | -0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 1 belirsiz çıkarıldı) | 2023 | 476 | 474 | +0.010 | -0.024 | +0.053 | +0.009 | -0.026 | +0.058 | -0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 6 −%30 dahil) | 2024-26 | 667 | 666 | +0.006 | -0.018 | +0.034 | +0.007 | -0.017 | +0.036 | +0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 6 −%100 dahil) | 2024-26 | 667 | 666 | +0.006 | -0.018 | +0.034 | +0.007 | -0.017 | +0.035 | +0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 P2 (sınıf 1 belirsiz çıkarıldı) | 2024-26 | 667 | 665 | +0.006 | -0.018 | +0.034 | +0.007 | -0.018 | +0.037 | +0.001 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%30 dahil) | 2016-22 | 2316 | 2315 | +0.010 | -0.009 | +0.030 | +0.010 | -0.011 | +0.029 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%100 dahil) | 2016-22 | 2316 | 2315 | +0.010 | -0.009 | +0.030 | +0.010 | -0.010 | +0.029 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%30 dahil) | 2023 | 896 | 896 | -0.002 | -0.028 | +0.021 | -0.003 | -0.029 | +0.022 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%100 dahil) | 2023 | 896 | 896 | -0.002 | -0.028 | +0.021 | -0.003 | -0.029 | +0.022 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%30 dahil) | 2024-26 | 2382 | 2377 | +0.008 | -0.015 | +0.032 | +0.009 | -0.016 | +0.032 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ES (sınıf 6 −%100 dahil) | 2024-26 | 2382 | 2377 | +0.008 | -0.015 | +0.032 | +0.009 | -0.015 | +0.032 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%30 dahil) | 2016-22 | 163 | 163 | +0.035 | -0.054 | +0.117 | +0.035 | -0.045 | +0.127 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%100 dahil) | 2016-22 | 163 | 163 | +0.035 | -0.054 | +0.117 | +0.035 | -0.053 | +0.117 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%30 dahil) | 2023 | 58 | 58 | -0.055 | -0.147 | +0.033 | -0.055 | -0.148 | +0.038 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%100 dahil) | 2023 | 58 | 58 | -0.055 | -0.147 | +0.033 | -0.055 | -0.150 | +0.031 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%30 dahil) | 2024-26 | 191 | 191 | -0.012 | -0.060 | +0.041 | -0.012 | -0.060 | +0.044 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 HT (sınıf 6 −%100 dahil) | 2024-26 | 191 | 191 | -0.012 | -0.060 | +0.041 | -0.012 | -0.061 | +0.042 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%30 dahil) | 2016-22 | 4193 | 4192 | +0.006 | -0.008 | +0.019 | +0.006 | -0.008 | +0.020 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%100 dahil) | 2016-22 | 4193 | 4192 | +0.006 | -0.008 | +0.019 | +0.006 | -0.007 | +0.020 | +0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%30 dahil) | 2023 | 1983 | 1982 | +0.007 | -0.009 | +0.025 | +0.007 | -0.010 | +0.025 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%100 dahil) | 2023 | 1983 | 1982 | +0.007 | -0.009 | +0.025 | +0.007 | -0.010 | +0.026 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%30 dahil) | 2024-26 | 4192 | 4187 | +0.016 | -0.002 | +0.036 | +0.016 | -0.003 | +0.036 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |
| K51 ÇEK (sınıf 6 −%100 dahil) | 2024-26 | 4192 | 4187 | +0.016 | -0.002 | +0.036 | +0.016 | -0.003 | +0.037 | -0.000 | TUTMAZ | TUTMAZ | SAĞLAM |

### 3.2 Küçük mum / hacim kuruması / hacimli taban (v1.2 eşleşmiş kontrol; eşleştirme havuzu her örneklemde ayrı; evren: eski = A, yeni = B, ortak_eski = C-eski, ortak_yeni = C-yeni)

| kume | donem | evren | n | fark | fark_alt | fark_ust | net_fark | karar | eslesmeyen_pay | evren_etkisi | etiket_etkisi | fark_fark | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H-B P1 vs ES (küçük mum) | 2016-22 | eski | 235 | -0.012 | -0.120 | +0.085 | -0.001 | TUTMAZ | +0.830 |  |  |  |  |
| H-B P1 vs ES (küçük mum) | 2023 | eski | 135 | -0.015 | -0.079 | +0.051 | +0.002 | TUTMAZ | +0.830 |  |  |  |  |
| H-B P1 vs ES (küçük mum) | 2024-26 | eski | 249 | +0.041 | -0.033 | +0.119 | -0.000 | TUTMAZ | +0.830 |  |  |  |  |
| H-B P1 vs ES (küçük mum) | 2016-22 | yeni | 235 | -0.012 | -0.112 | +0.095 | -0.001 | TUTMAZ | +0.830 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-B P1 vs ES (küçük mum) | 2023 | yeni | 135 | -0.015 | -0.075 | +0.052 | +0.002 | TUTMAZ | +0.830 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-B P1 vs ES (küçük mum) | 2024-26 | yeni | 249 | +0.041 | -0.034 | +0.116 | -0.000 | TUTMAZ | +0.830 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-B P1 vs ES (küçük mum) | 2016-22 | ortak_eski | 235 | -0.012 | -0.108 | +0.085 | -0.001 | TUTMAZ | +0.830 |  |  |  |  |
| H-B P1 vs ES (küçük mum) | 2023 | ortak_eski | 135 | -0.015 | -0.077 | +0.053 | +0.002 | TUTMAZ | +0.830 |  |  |  |  |
| H-B P1 vs ES (küçük mum) | 2024-26 | ortak_eski | 249 | +0.041 | -0.037 | +0.120 | -0.000 | TUTMAZ | +0.830 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | eski | 135 | -0.032 | -0.152 | +0.089 | -0.014 | TUTMAZ | +0.903 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | eski | 68 | +0.061 | -0.091 | +0.197 | +0.024 | TUTMAZ | +0.903 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | eski | 151 | +0.093 | -0.012 | +0.195 | +0.043 | TUTMAZ | +0.903 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | yeni | 134 | -0.032 | -0.167 | +0.092 | -0.014 | TUTMAZ | +0.904 | -0.000 | +0.000 | -0.000 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | yeni | 67 | +0.050 | -0.106 | +0.188 | +0.023 | TUTMAZ | +0.904 | -0.011 | +0.000 | -0.011 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | yeni | 151 | +0.093 | -0.014 | +0.200 | +0.043 | TUTMAZ | +0.904 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | ortak_eski | 134 | -0.032 | -0.159 | +0.103 | -0.014 | TUTMAZ | +0.904 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | ortak_eski | 67 | +0.050 | -0.114 | +0.181 | +0.023 | TUTMAZ | +0.904 |  |  |  |  |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | ortak_eski | 151 | +0.093 | -0.008 | +0.197 | +0.043 | TUTMAZ | +0.904 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2016-22 | eski | 99 | +0.092 | -0.036 | +0.203 | +0.034 | TUTMAZ | +0.316 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2023 | eski | 43 | +0.027 | -0.099 | +0.125 | +0.018 | TUTMAZ | +0.316 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2024-26 | eski | 140 | -0.030 | -0.102 | +0.040 | -0.003 | TUTMAZ | +0.316 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2016-22 | yeni | 99 | +0.092 | -0.045 | +0.204 | +0.034 | TUTMAZ | +0.316 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2023 | yeni | 43 | +0.027 | -0.102 | +0.123 | +0.018 | TUTMAZ | +0.316 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2024-26 | yeni | 140 | -0.030 | -0.106 | +0.039 | -0.003 | TUTMAZ | +0.316 | +0.000 | +0.000 | +0.000 | SAĞLAM |
| H-D hacimli taban (HT) vs genel | 2016-22 | ortak_eski | 99 | +0.092 | -0.029 | +0.208 | +0.034 | TUTMAZ | +0.316 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2023 | ortak_eski | 43 | +0.027 | -0.098 | +0.126 | +0.018 | TUTMAZ | +0.316 |  |  |  |  |
| H-D hacimli taban (HT) vs genel | 2024-26 | ortak_eski | 140 | -0.030 | -0.105 | +0.041 | -0.003 | TUTMAZ | +0.316 |  |  |  |  |
| K48 / K49 / K50 deneyleri | hepsi |  |  |  |  |  |  |  |  |  |  |  | GEÇERSİZ (evren yeniden kurulamıyor: yalnız bugün işlem gören V_ABD evreninde koştu; kod K34 evrenini almıyor) |
| H-B P1 vs ES (küçük mum) | 2016-22 | ortak_yeni | 235 | -0.012 | -0.112 | +0.095 | -0.001 | TUTMAZ | +0.830 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-B P1 vs ES (küçük mum) | 2023 | ortak_yeni | 135 | -0.015 | -0.075 | +0.052 | +0.002 | TUTMAZ | +0.830 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-B P1 vs ES (küçük mum) | 2024-26 | ortak_yeni | 249 | +0.041 | -0.034 | +0.116 | -0.000 | TUTMAZ | +0.830 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2016-22 | ortak_yeni | 134 | -0.032 | -0.167 | +0.092 | -0.014 | TUTMAZ | +0.904 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2023 | ortak_yeni | 67 | +0.050 | -0.106 | +0.188 | +0.023 | TUTMAZ | +0.904 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-C ÇEK + hacim kuruması vs ÇEK hacimsiz | 2024-26 | ortak_yeni | 151 | +0.093 | -0.014 | +0.200 | +0.043 | TUTMAZ | +0.904 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-D hacimli taban (HT) vs genel | 2016-22 | ortak_yeni | 99 | +0.092 | -0.045 | +0.204 | +0.034 | TUTMAZ | +0.316 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-D hacimli taban (HT) vs genel | 2023 | ortak_yeni | 43 | +0.027 | -0.102 | +0.123 | +0.018 | TUTMAZ | +0.316 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |
| H-D hacimli taban (HT) vs genel | 2024-26 | ortak_yeni | 140 | -0.030 | -0.106 | +0.039 | -0.003 | TUTMAZ | +0.316 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |

### 3.3 Sessiz ML (LightGBM meta-etiketleme, P1, yıl yıl ileri 2019-26; özellikler, yıllar, embargo 10 gün, ayarlar, tohum 515 sabit; evren: A / B / C-eski / C-yeni)

| kume | donem | evren | n | egitim_son_n | auc | fark | ust_fark | ust_fark_alt | ust_fark_ust | alt_fark | karar | yillik_auc | evren_etkisi | etiket_etkisi | fark_fark | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | eski | 3410 | 3335 | +0.512 | +0.003 | +0.024 | -0.003 | +0.053 | +0.020 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.461; 2025: 0.549; 2026: 0.448 |  |  |  |  |
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | yeni | 3407 | 3332 | +0.513 | +0.004 | +0.021 | -0.006 | +0.049 | +0.017 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.449; 2025: 0.557; 2026: 0.475 | +0.001 | -0.000 | +0.001 | SAĞLAM |
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | ortak_eski | 3407 | 3332 | +0.513 | +0.004 | +0.021 | -0.006 | +0.049 | +0.017 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.449; 2025: 0.557; 2026: 0.475 |  |  |  |  |
| model üst üçte biri vs alt üçte biri | 2019-26 test yılları | ortak_yeni | 3407 | 3332 | +0.513 | +0.004 | +0.021 | -0.006 | +0.049 | +0.017 | TUTMAZ | 2019: 0.559; 2020: 0.546; 2021: 0.506; 2022: 0.495; 2023: 0.520; 2024: 0.449; 2025: 0.557; 2026: 0.475 |  |  |  | C-yeni ≡ B (düzeltilmiş evren eski evrenin alt kümesi) |

### 3.4 K52 / K53 (kayıtlı olay dosyaları; A = kayıtlı etiket, B = düzeltilmiş etiket, C-eski = düzeltilmiş evrende kalan olaylar kayıtlı etiketle; sınıf 6 çıkarıldı)

| test | kume | donem | eski_n | eski_n_b | ortak_eski_n | yeni_n | yeni_n_b | eski_fark | eski_fark_alt | eski_fark_ust | ortak_eski_fark | yeni_fark | yeni_fark_alt | yeni_fark_ust | evren_etkisi | etiket_etkisi | fark_fark | eski_karar | ortak_eski_karar | yeni_karar | sinif56_pay_olay | degerlendirme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2016-22 | 178 | 990 | 178 | 178 | 990 | +0.017 | -0.069 | +0.110 | +0.017 | +0.017 | -0.068 | +0.108 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2023 | 122 | 626 | 122 | 122 | 625 | +0.021 | -0.075 | +0.119 | +0.022 | +0.023 | -0.075 | +0.127 | +0.001 | +0.001 | +0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P1 | 2024-26 | 197 | 985 | 197 | 197 | 983 | -0.020 | -0.072 | +0.042 | -0.019 | -0.018 | -0.071 | +0.042 | +0.001 | +0.000 | +0.002 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2016-22 | 108 | 377 | 108 | 108 | 377 | +0.114 | +0.023 | +0.221 | +0.114 | +0.114 | +0.022 | +0.220 | +0.000 | -0.000 | -0.000 | TUTAR | TUTAR | TUTAR | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2023 | 79 | 320 | 79 | 79 | 319 | +0.055 | -0.074 | +0.148 | +0.057 | +0.057 | -0.074 | +0.150 | +0.002 | -0.000 | +0.002 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K52 H0 (G1 − G2a) | K52 P2 | 2024-26 | 128 | 493 | 128 | 128 | 492 | +0.020 | -0.053 | +0.110 | +0.019 | +0.020 | -0.050 | +0.118 | -0.001 | +0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2016-22 | 1007 | 15602 | 1007 | 1007 | 15602 | +0.008 | -0.015 | +0.033 | +0.008 | +0.008 | -0.015 | +0.032 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2023 | 235 | 4114 | 234 | 234 | 4108 | -0.012 | -0.076 | +0.053 | -0.012 | -0.012 | -0.076 | +0.050 | -0.000 | -0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T1 (BDS 3 − BDS < 3) | K53 T1 | 2024-26 | 749 | 12248 | 749 | 749 | 12220 | +0.020 | -0.012 | +0.052 | +0.020 | +0.020 | -0.013 | +0.053 | +0.000 | -0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2016-22 | 3999 | 4185 | 3999 | 3999 | 4185 | -0.012 | -0.031 | +0.008 | -0.012 | -0.012 | -0.030 | +0.008 | +0.000 | +0.000 | +0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2023 | 920 | 1291 | 919 | 919 | 1287 | -0.003 | -0.034 | +0.030 | -0.005 | -0.005 | -0.037 | +0.026 | -0.001 | +0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T5 (KGS geç − hızlı) | K53 T5 | 2024-26 | 2904 | 4032 | 2895 | 2895 | 4022 | -0.001 | -0.019 | +0.017 | -0.002 | -0.002 | -0.019 | +0.017 | -0.000 | -0.000 | -0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2016-22 | 2617 | 3259 | 2617 | 2617 | 3259 | +0.024 | +0.003 | +0.043 | +0.024 | +0.024 | +0.003 | +0.044 | +0.000 | -0.000 | -0.000 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2023 | 1199 | 933 | 1197 | 1197 | 933 | +0.028 | -0.014 | +0.064 | +0.030 | +0.030 | -0.013 | +0.067 | +0.001 | +0.000 | +0.002 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |
| 5 K53 T6 (ADE üst − alt üçte bir) | K53 T6 | 2024-26 | 3260 | 2885 | 3254 | 3254 | 2881 | +0.025 | +0.006 | +0.042 | +0.025 | +0.025 | +0.007 | +0.044 | +0.000 | +0.000 | +0.001 | TUTMAZ | TUTMAZ | TUTMAZ | +0.000 | SAĞLAM |

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

## 5. Değerlendirme özeti (A ile B)

- 1 K51 temel: SAĞLAM: 29, ETKİLENMİŞ: 1
- 3 BB sıkışması / EMA (K48, FON_IZI): GEÇERSİZ (evren yeniden kurulamıyor: yalnız bugün işlem gören V_ABD evreninde koştu; kod K34 evrenini almıyor): 1
- 3 küçük mum / hacim / taban (v1.2 eşleşmiş): SAĞLAM: 9
- 4 sessiz ML (LightGBM meta, P1, yıl yıl ileri 2019-26): SAĞLAM: 1
- 5 K52 H0 (G1 − G2a): SAĞLAM: 6
- 5 K53 T1 (BDS 3 − BDS < 3): SAĞLAM: 3
- 5 K53 T5 (KGS geç − hızlı): SAĞLAM: 3
- 5 K53 T6 (ADE üst − alt üçte bir): SAĞLAM: 3

- Ayrıştırma (bütün hücreler): |evren etkisi| en çok 0.0109, |etiket etkisi| en çok 0.0006, |toplam| en çok 0.0109 (taban-ayarlı isabet, oran birimi; 0,02 = 2 puan).

Sınıf 6 (doğrulanamayan) ve sınıf 5 (belirsiz) hiçbir hücrede iflas ya da aktif sayılmadı; 6 ana sonuçta evrenden çıktı (−%30 / −%100 varyantları 3.1b'de), 5 K51 kuralıyla kaldı ve bandı yazıldı; sınıf 1 belirsiz ve 4a doğrulanamayan kayıtlar ayrıca işaretlendi.

## 6. Hayatta kalma yanlılığı ve sınıf 6 (ek 8.4 tartışması)

- Sınıf 6 bu evrende 0 sembol. Sınıf 6'yı çıkarmak, geçmişi doğrulanamayan (dolayısıyla batmış olma olasılığı yüksek) şirketleri dışarıda bırakır; bu tek başına hayatta kalma yanlılığı üretir. Bu yüzden −%30 ve −%100 varsayımlı sonuçlar da üretildi: sınıf 6 varyantlarında B'ye göre en büyük değişim +0.0000 (oran birimi). Sınıf 6 boş olduğu için bu varyantlar B'yi değiştirmedi; yanlılık sınırı bu evrende sınıf 6'dan değil, evrende hiç bulunmayan şirketlerden gelir.
- Asıl sınır evrenin kuruluşudur: 3267 sembolün 266'ü borsadan çıkmış ya da belirsiz; V_ABD ve K34 Yahoo yalnız bugün Yahoo'da olan sembollerdir, eski sembolle biten seriler yalnız 422'lik Tiingo örnekleminden gelir. 2015-2026 arasında ABD'de borsadan çıkan şirket sayısı bunun çok üstündedir; eksik batık şirketler panelde yoktur, bu yüzden hiçbir K54 hücresi onların etkisini ölçemez. 'SAĞLAM' etiketi yalnız mevcut evren içindeki sınıflandırma ve çıkış işlemi düzeltmesi için geçerlidir; evren tamamlanmadan (Kasım Tiingo kotasıyla gerçek batan evreni) hayatta kalma yanlılığı tam ölçülemez.
- Yönü: eksik batık şirketler hem olay hem taban tarafına girerdi; eksikliğin taban-ayarlı isabeti hangi yönde oynatacağı önceden bilinemez, K51'in İZ DEĞİL kararını lehine çevirecek bir mekanizma da görünmüyor (desen olayları çoğunlukla hayatta kalanlarda; batıklar eklenince olay tarafı daha çok düşer).

## 7. Yorum ve sınırlar (sonuç görüldükten sonra yazılan açıklama; kararlar ve eşikler değişmedi)

- A ile B arasında değerlendirme dağılımı 5. bölümde. Ortak örneklem ayrıştırması evren etkisi (satır çıkarma: sınıf 6, 4b kesimi) ile etiket etkisini (çıkış işlemi) ayırır; iki etki de 5. bölümdeki en büyük mutlak değerlerle sınırlıdır.
- Sınıf 4b (kod yeniden kullanımı) listesi aynı şirketin yeniden kaydını da yakalayabilir; kesim bu durumda geçerli veriyi atar, yani düzeltme muhafazakârdır.
- K51'in eski 'batma benzeri' tahmininin bir bölümü SEC kanıtına göre birleşme / satın alma ya da belirsiz çıktı; sembol başına eski tahmin ve yeni sınıf K54_SIRKET_DURUMU.csv ile K51_EVREN_PIT.csv birleştirilerek görülür.
- ETKİLENMİŞ etiketi 2 puanın altındaki değişimlerde de çıkabilir (aralık alt ucunun sıfırın öbür yanına geçmesi); böyle hücrelerde karar değişip değişmediği tabloda 'eski_karar / yeni_karar' sütunlarındadır.

## Yeniden üretim

- `R = cy_v15_calistir(k54_yol='.../k54')` (k54: sec_ozet.json, sembol_cik.json, company_tickers.json, supported_tickers.csv; SEC indirmesi e-posta User-Agent ile, kodda yok). Çıktılar: K54_EVREN_ESLESTIRME.csv, K54_SIRKET_DURUMU.csv, K54_ESKI_YENI_TEST_KARSILASTIRMA.csv, K54_DELIST_DUYARLILIK.csv, bu belge.
