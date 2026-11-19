# YAPI_HEDEF — DEVİR 1 ÖN KAYIT (web / hakem adayları F30-F42, süzgeç karnesi; 2026-11-19)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; DEVİR 1 eklendi (yh_devir_ozellik, yh_devir_kos). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar yalnız satır kimliği, dönem ve özellik dağılımıdır (getirisiz: h5 / es_h5 / st5 okunmadı).

- YH_ESIK_D1_SHA: `2ffac1e395318b6f837ff3c627e022684a31951ed2a3a443442115bab842ea7e` (DEVİR 1: tanımlar, pencereler, aday kuralları, kol, dönem, etiket)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md: Y1-Y11c AYNEN)
- YH_ESIK6_SHA: `6f05f68cd07560e407c7d1b06431990704b79441c51f4e09bbddfafba4086410` (= ON_KAYIT_6.md)
- YH_ESIK7_SHA: `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26` (= ON_KAYIT_7.md; Y12)
- YH_KOD_SHA: `065b75e3685db0588cb5390f7f7416f94fd6dbe7f1823b92aece199c9a437441` (YAPI_HEDEF.py)
- D1_OZELLIK_SHA: `e80d9fb9af3d51c72f5f707c9cddb0319518f6aad5f5b25711e8dfb97f91fd7e` (ozellik_Y1_d1.csv.gz; F30-F42)
- D1_ESIK_JSON_SHA: `9f9db30fce92e9a91edd045b9a5f8b2a1026f5a25b7474d51cb4a03d93ef15e3` (devir1_esik.json; çeyrekler)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; ölçü satırları)
- Y9_OLAY_SHA: `56aa6101aba25cddd66dedddcba3d536a05b8e0850b727f015ef3cec295d5809` (olay_Y9.csv.gz; KOL-B regresyonu)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F8 / F15 / F17)
- ZAMAN (UTC): `2026-11-19 12:04:39 UTC`

## 1. ADAYLAR, F-KODLARI, TANIM, PENCERE, SABİT EŞİK

Pencereler: {"onceki": 60, "onceki_min": 40, "bolge_min_cs": 10, "bolge_min": 15, "er_kisa": 10, "mdd_gun": 30, "hiz_gun": 250, "hiz_hedef": 0.1, "hiz_hedef2": 0.05, "hiz_esik": 15}. Bölge = Y1 olayının S6 bölgesi [sol, t-1] (GOZ_ETIKET.ge_bolge; t - sol = F8).

- **F30**: W1 Corwin-Schultz spread oranı: ort S (bölge [sol, t-1] içi iki-gün çiftleri, >= 10 çift) / ort S (önceki pencere [sol-60, sol-1] içi çiftler, >= 40 bar); S = 2(e^a - 1)/(1 + e^a), a = (sqrt(2b) - sqrt(b))/k - sqrt(g/k), k = 3 - 2 sqrt2, b = ln(H_j/L_j)^2 + ln(H_j+1/L_j+1)^2, g = ln(max H / min L)^2; gece düzeltmesi: C_j < L_j+1 ise j+1'in H ve L'si (L_j+1 - C_j) kadar aşağı, C_j > H_j+1 ise (C_j - H_j+1) kadar yukarı; S < 0 -> 0; önceki ort S = 0 ise NaN.
- **F31**: W2 B gün-içi birikim = prod(C_j/O_j) - 1, j = [sol, t-1] (>= 15 bar).
- **F32**: W2 D = A - B; A gece birikim = prod(O_j/C_j-1) - 1, j = [sol, t-1].
- **F33**: W3 Amihud oranı: ort(|C_j/C_j-1 - 1| / (C_j V_j)) bölge [sol, t-1] (>= 15) / aynısı önceki [sol-60, sol-1] (>= 40); önceki ort 0 ise NaN (günlük oranların ortalaması).
- **F34**: W4 sıfır getiri payı farkı: pay(C_j == C_j-1) bölge [sol, t-1] (>= 15) - aynısı önceki [sol-60, sol-1] (>= 40).
- **F35**: W5 ER_bölge = |C_t-1 - C_sol-1| / sum |C_k - C_k-1|, k = sol..t-1 (n = bölge boyu, >= 15); payda 0 -> NaN.
- **F36**: W5 ER_10 = |C_t-1 - C_t-11| / sum |C_k - C_k-1|, k = t-10..t-1; payda 0 -> NaN.
- **F37**: W6 R/MDD: P = ln C, pencere [t-30, t-1]; MDD = max(koşan tepe - P); tau* = ilk en derin nokta; R = P_t-1 - P_tau*; MDD = 0 -> NaN.
- **F38**: W6 R (log toparlanma, aynı pencere; bilgi).
- **F39**: E1 mahkeme BAYRAK: 1 = yh_mahkeme_hisse 'ÖNCEKİ BÖLGE DAHA UYGUN' (max aday puanı > seçilen puanı), 0 = değil; mahkeme hatası NaN.
- **F40**: E1 PUAN_FARK = puan(seçilen) - max puan(aday); aday yoksa NaN (bilgi).
- **F41**: E2 HIZ: j* = ilk argmin Low [t-250, sol-1]; HIZ = ilk m (j* < m <= sol-1) Close_m >= Low_j* x 1,10 için m - j* (geçerli bar); ulaşmadı = inf (UL); t'den önce 250 geçerli bar yoksa ya da sol <= t-250 ise NaN.
- **F42**: E2 HIZ +%5 varyantı (bilgi; süzgece girmez).

Çeyrek kuralı: kaynakta eşik olmayan adaylar için q25 / q75 PAZAR içinde, bütün Y1 olaylarının (KOL-A tabanı) sonlu özellik değerlerinden (getirisiz; inf ve NaN dışarıda); YÖN 1 eşiği eğitim 2016-22 olaylarından, YÖN 2 (ters yürüyen sınama) eşiği 2023-26 olaylarından; KOL-B aynı eşikleri kullanır; eşikler devir1_esik.json'da ön kayıtta mühürlü.

| Aday | Kaynak | Yön | Süzgeç kuralı | Ad |
|---|---|---|---|---|
| W1 | W1 | ana | F30 < 1.0 VE F30 <= q25 | W1 CS spread daraldı (oran < 1 ve alt çeyrek) |
| W1t | W1 | ters | F30 >= q75 | W1 ters: spread genişledi (üst çeyrek) |
| W2 | W2 | ana | F31 > 0.0 VE F31 >= q75 | W2 gün-içi birikim B > 0 ve üst çeyrek |
| W2t | W2 | ters | F31 <= q25 | W2 ters: B alt çeyrek |
| W2D | W2 | ana | F32 >= q75 | W2 D = gece - gün-içi üst çeyrek |
| W2Dt | W2 | ters | F32 <= q25 | W2 ters: D alt çeyrek |
| W3 | W3 | ana | F33 < 1.0 VE F33 <= q25 | W3 Amihud düştü (oran < 1 ve alt çeyrek) |
| W3t | W3 | ters | F33 >= q75 | W3 ters: Amihud üst çeyrek |
| W4 | W4 | ana | F34 < 0.0 VE F34 <= q25 | W4 sıfır getiri payı düştü (< 0 ve alt çeyrek) |
| W4t | W4 | ters | F34 > 0.0 VE F34 >= q75 | W4 ters: sıfır getiri payı arttı (> 0 ve üst çeyrek; q75 = 0 olan pazarda dejenere olmasın) |
| W5a | W5 | ana | F35 <= q25 | W5a ER_bölge alt çeyrek (yerinde sayma) |
| W5b | W5 | ana | F36 >= q75 | W5b ER_10 üst çeyrek (çıkış) |
| W6 | W6 | ana | F37 >= q75 | W6 R/MDD üst çeyrek (dipten toparlanmış) |
| W6t | W6 | ters | F37 <= q25 | W6 ters: R/MDD alt çeyrek |
| E1 | E1 | ana | F39 == 0.0 | E1 ÖNCEKİ BÖLGE süzgeci (bayrak 0 kalır) |
| E1t | E1 | ters | F39 == 1.0 | E1 ters: bayrak 1 (önceki bölge daha uygun) |
| E2 | E2 | ana | F41 <= 15.0 | E2 HIZLI toparlanma hafızası (HIZ <= 15 bar) |
| E2t | E2 | ters | F41 > 15.0 | E2 ters: YAVAŞ (> 15) ya da UL |

### Çeyrek eşikleri (devir1_esik.json; YÖN 1 = 2016-22, YÖN 2 = 2023-26; pazar içi, bütün Y1 olayları)

| Özellik | Pazar | YÖN 1 q25 / q75 (n) | YÖN 2 q25 / q75 (n) |
|---|---|---|---|
| F30 | ABD | 0.754556 / 1.15633 (7912) | 0.767149 / 1.17767 (5566) |
| F30 | AVR | 0.779934 / 1.14936 (4239) | 0.806001 / 1.15772 (2433) |
| F30 | BIST | 0.711636 / 1.10136 (2288) | 0.707135 / 1.14256 (1696) |
| F31 | ABD | -0.0170995 / 0.0502927 (7006) | -0.0211116 / 0.0527261 (4786) |
| F31 | AVR | -0.0198502 / 0.0555593 (3890) | -0.0180964 / 0.0579193 (2247) |
| F31 | BIST | -0.0759499 / 0.0116031 (1874) | -0.0815237 / 0.00376359 (1266) |
| F32 | ABD | -0.0463054 / 0.061542 (7006) | -0.0532395 / 0.0610446 (4786) |
| F32 | AVR | -0.0591623 / 0.0626246 (3890) | -0.0657552 / 0.061323 (2247) |
| F32 | BIST | 0.0187321 / 0.159009 (1874) | 0.0318036 / 0.160568 (1266) |
| F33 | ABD | 0.696169 / 1.03653 (7006) | 0.716086 / 1.03195 (4786) |
| F33 | AVR | 0.678956 / 1.03509 (3890) | 0.72327 / 1.06074 (2247) |
| F33 | BIST | 0.546067 / 1.12527 (1874) | 0.699725 / 1.2526 (1266) |
| F34 | ABD | -0.0047619 / 0 (7006) | 0 / 0 (4786) |
| F34 | AVR | -0.0166667 / 0.0166667 (3890) | -0.0166667 / 0.0178161 (2247) |
| F34 | BIST | -0.0166667 / 0.0540416 (1874) | -0.0166667 / 0.0322581 (1266) |
| F35 | ABD | 0.0666825 / 0.241561 (7006) | 0.0578489 / 0.225617 (4786) |
| F35 | AVR | 0.0647402 / 0.243132 (3890) | 0.0626424 / 0.230476 (2247) |
| F35 | BIST | 0.0484262 / 0.209925 (1874) | 0.0478865 / 0.191092 (1266) |
| F36 | ABD | 0.107638 / 0.347874 (8686) | 0.10145 / 0.339292 (6195) |
| F36 | AVR | 0.104744 / 0.362317 (4496) | 0.113004 / 0.380465 (2558) |
| F36 | BIST | 0.11112 / 0.367392 (2588) | 0.0962159 / 0.328355 (2140) |
| F37 | ABD | 0.573977 / 1.24107 (8686) | 0.485824 / 1.13774 (6195) |
| F37 | AVR | 0.629641 / 1.2855 (4496) | 0.587241 / 1.23425 (2558) |
| F37 | BIST | 0.423372 / 1.06984 (2588) | 0.335434 / 0.922684 (2140) |

## 2. ÖLÇÜ, KOLLAR, ETİKET

- KOLLAR: A = Y1 (bütün olay_Y1.csv.gz satırları); B = Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; YH_ESIK6 G2; olay_Y9.csv.gz ile küme eşitliği).
- ÖLÇÜ: 1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): hücre = (aday süzgeci VE kol tabanı) x pazar x dönem; n = h5 ve es_h5 olan olay; P olay = ort h5, P eş = ort es_h5 (aynı gün aynı OC kovası eşleri), FARK = P olay - P eş; MARJİNAL = FARK(süzgeçli) - FARK(kol tabanı, aynı pazar x dönem); stop: ort st5 (olay) / ort es_st5 (eş).
- ETİKET: YÖN 1 (eşik 2016-22): eğitim hücresi 2016-22, sınama 2023-26; YÖN 2 (eşik 2023-26): sınama hücresi 2016-22. KATKI+ = (eğitim, sınama, YÖN 2 sınama) üçünde n >= 30 VE FARK > 0 VE MARJİNAL > 0, ayrıca eğitim ve sınamada st5 olay <= es_st5 eş (eş payından stop payı büyük değil); KATKI− = üçünde n >= 30 VE MARJİNAL < 0; değilse SORGULA. Karar pazarı ABD+AVR; ABD / AVR / BIST bilgi.
- ÇOKLU KARŞILAŞTIRMA: 18 aday x 2 kol = 36 karne satırı: BH uygulanmaz (ikili, iki dönem + ters yön kuralı); şansla KATKI+ olasılığı rapora yazılır.
- YENİDEN ÜRETİM hücreleri: W1 / A / ABD+AVR / sinama; E2 / B / ABD+AVR / egitim.
- REGRESYON KAPISI: YH_ESIK / 6 / 7 sha = ON_KAYIT_5 / 6 / 7 mührü; KOL-B kümesi = olay_Y9.csv.gz kümesi; t - sol = F8; değilse DURUR.

## 3. GETİRİSİZ HUNİ (Y1 olayı -> aday tutan olay sayısı; YÖN 1 eşikleri; pazar x dönem)

| Satır | Kol | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|---|---|
| taban | A | 8686 | 2042 | 4153 | 4496 | 815 | 1743 | 2588 | 381 | 1759 |
| W1 | A | 1978 | 381 | 935 | 1060 | 196 | 325 | 572 | 69 | 364 |
| W1t | A | 1978 | 459 | 1040 | 1060 | 188 | 441 | 572 | 72 | 416 |
| W2 | A | 1752 | 447 | 815 | 973 | 179 | 419 | 469 | 32 | 236 |
| W2t | A | 1752 | 421 | 890 | 973 | 191 | 350 | 469 | 22 | 336 |
| W2D | A | 1752 | 375 | 814 | 973 | 197 | 357 | 469 | 18 | 302 |
| W2Dt | A | 1752 | 489 | 837 | 973 | 176 | 431 | 469 | 24 | 236 |
| W3 | A | 1752 | 316 | 745 | 973 | 138 | 288 | 469 | 41 | 144 |
| W3t | A | 1752 | 409 | 755 | 973 | 189 | 434 | 469 | 25 | 394 |
| W4 | A | 1756 | 356 | 702 | 1180 | 198 | 484 | 608 | 58 | 410 |
| W4t | A | 1450 | 275 | 602 | 986 | 175 | 426 | 469 | 13 | 146 |
| W5a | A | 1752 | 487 | 850 | 973 | 196 | 382 | 469 | 26 | 291 |
| W5b | A | 2172 | 520 | 951 | 1124 | 273 | 436 | 647 | 48 | 357 |
| W6 | A | 2172 | 433 | 776 | 1124 | 190 | 388 | 647 | 69 | 316 |
| W6t | A | 2172 | 693 | 1287 | 1124 | 232 | 480 | 647 | 164 | 580 |
| E1 | A | 3281 | 689 | 1340 | 1687 | 296 | 590 | 1125 | 155 | 639 |
| E1t | A | 5405 | 1353 | 2813 | 2809 | 519 | 1153 | 1463 | 226 | 1120 |
| E2 | A | 6874 | 1730 | 3364 | 3154 | 663 | 1179 | 2170 | 345 | 1586 |
| E2t | A | 1811 | 311 | 789 | 1337 | 152 | 559 | 418 | 36 | 173 |
| taban | B | 346 | 146 | 232 | 89 | 20 | 55 | 238 | 81 | 297 |
| W1 | B | 53 | 15 | 44 | 15 | 2 | 4 | 56 | 13 | 73 |
| W1t | B | 84 | 46 | 54 | 31 | 9 | 18 | 54 | 19 | 54 |
| W2 | B | 37 | 11 | 12 | 4 | 4 | 6 | 34 | 5 | 17 |
| W2t | B | 78 | 40 | 63 | 22 | 6 | 20 | 49 | 6 | 82 |
| W2D | B | 51 | 31 | 39 | 15 | 5 | 17 | 43 | 3 | 65 |
| W2Dt | B | 51 | 13 | 23 | 8 | 4 | 6 | 48 | 6 | 20 |
| W3 | B | 20 | 6 | 12 | 7 | 2 | 7 | 25 | 0 | 8 |
| W3t | B | 78 | 42 | 51 | 21 | 7 | 17 | 64 | 4 | 101 |
| W4 | B | 59 | 25 | 26 | 22 | 3 | 14 | 45 | 10 | 58 |
| W4t | B | 29 | 10 | 33 | 7 | 4 | 9 | 54 | 3 | 32 |
| W5a | B | 76 | 32 | 54 | 16 | 7 | 14 | 44 | 5 | 45 |
| W5b | B | 70 | 27 | 31 | 21 | 6 | 14 | 70 | 11 | 61 |
| W6 | B | 17 | 4 | 9 | 4 | 0 | 4 | 24 | 3 | 10 |
| W6t | B | 256 | 112 | 160 | 59 | 17 | 39 | 120 | 62 | 180 |
| E1 | B | 176 | 56 | 99 | 40 | 8 | 25 | 132 | 51 | 138 |
| E1t | B | 170 | 90 | 133 | 49 | 12 | 30 | 106 | 30 | 159 |
| E2 | B | 214 | 109 | 165 | 47 | 12 | 25 | 176 | 60 | 229 |
| E2t | B | 132 | 37 | 67 | 42 | 8 | 30 | 62 | 21 | 68 |

## 4. ÖZELLİK DENETİMİ (getirisiz)

| Pazar | olay | prefix tuttu | mahkeme prefix | mahkeme hata | NaN (F30..F42) | inf F41 / F42 |
|---|---|---|---|---|---|---|
| ABD | 14881 | 25 | 3 | 0 | F30 1403, F31 3089, F32 3089, F33 3089, F34 3089, F35 3089, F40 130, F41 2, F42 2 | 820 / 390 |
| AVR | 7054 | 25 | 3 | 0 | F30 382, F31 917, F32 917, F33 917, F34 917, F35 917, F40 63, F41 10, F42 10 | 590 / 266 |
| BIST | 4728 | 25 | 3 | 0 | F30 744, F31 1588, F32 1588, F33 1588, F34 1588, F35 1588, F40 54 | 273 / 147 |

### Mekanik ilişki (K1; Spearman, bütün Y1, getirisiz)

| Özellik | F3 mum boyu | F10 bölge net | F13 kırılım hacmi | F15 konum |
|---|---|---|---|---|
| F30 | +0.29 | -0.06 | -0.04 | -0.02 |
| F31 | +0.05 | +0.48 | -0.22 | +0.28 |
| F32 | -0.09 | -0.23 | +0.19 | -0.16 |
| F33 | +0.19 | -0.14 | +0.05 | -0.28 |
| F34 | -0.06 | -0.00 | +0.03 | -0.03 |
| F35 | -0.11 | +0.44 | -0.11 | +0.26 |
| F36 | -0.07 | +0.14 | -0.09 | +0.05 |
| F37 | -0.04 | +0.43 | -0.24 | +0.39 |
| F41 | +0.27 | +0.07 | -0.08 | +0.14 |

Uygulama yorumları (ölçümden önce): (1) CS çiftleri geçerli barlar dizisinde komşu (geçersiz bar atılmış; ABD'de nadir); (2) W2'de gece = O_j / C_j-1 - 1 düzeltilmiş fiyatla (temettü günü geceye düşer); (3) E1 seçilen bölge puanı 12 kural (YH_ESIK6 mahkeme), prefix=False ile hesaplanır, prefix=True pazar başına 3 olayda denetlenir; (4) E2 UL = inf (HIZLI değil, YAVAŞ sınıfına girer); (5) W5'te iki hücre (W5a, W5b) ayrı karne satırıdır, ters yön yok; (6) KATKI+ ters yön şartı E1 / E2'de (sabit eşik) YÖN 2 sınama hücresi = eğitim hücresi olur (aynı sayı).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | olay ve eş olay_Y1.csv.gz'den (yh_olay_olc: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar takip geometrisi); FARK = P olay - P eş aynı satırlarda; MARJİNAL kol tabanına göre (Y1 / Y9) aynı pazar x dönem; mekanik üstünlük: F30 / F33 / F34 aralık ve hacim ölçüleri F3 / F13 ile ilişkili -> Spearman tablosu ön kayıtta (getirisiz); E1 / E2 sabit eşik |
| K2 | geleceğe bakma | EVET | F30-F38 ve F41-F42 yalnız [.., t-1] barları (yh_d1_bar t barını okumaz); sol = GOZ_ETIKET.ge_bolge (S6 nedensel); F39-F40 yh_mahkeme_hisse veriyi t'de keser; yh_devir_ozellik_yaz pazar başına 25 rastgele olayda veri t'de kesilince aynı değer (DURUR) ve t - sol = F8 (ozellik_Y1) bütün satırlarda (DURUR); çeyrek eşikleri getirisiz, ön kayıtta mühürlü |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); pencereler geçerli bar sayımıyla; geçersiz bar veri dizisinde yok (CS çiftleri geçerli komşu barlar) |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç olay düşürmez, yalnız seçer; hücrede ort yanında P olay / P eş ayrı |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (olay_Y1 E0 / OC); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA) |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip (Yahoo düzeltilmiş); bütün yeni ölçüler oran / pay / log / bar sayısı (birimsiz; Amihud oranı para birimini götürür); F34 hisse kendi öncesine göre fark (tick düzeyi hisseler arası kullanılmaz); AVR yerel para |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batanlar yok): P olay ve P eş yukarı yanlı, FARK'ta kısmen götürür; dipte (KOL-B) daha büyük olabilir; rapora yazılır |
| K8 | örneklem ve dönem | EVET | hücre n < 30 SORGULA (ölçülemedi); iki dönem + ters yön aynı yön şartı; 36 karne satırı BH yok (ikili kural) -> şans KATKI+ notu; ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış) -> KATKI+ en fazla EMARE düzeyi, iz denmez; küçük n bulgu değil |
| K9 | ön kayıt | EVET | DEVIR_1_ON_KAYIT.md: YH_ESIK_D1_SHA, YH_ESIK / 6 / 7 sha (= ON_KAYIT_5 / 6 / 7), kod / özellik / eşik json / olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d1_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i ('DEVİR 1 ön kayıt') koşudan önce; eşik sonuca göre oynanmaz; ikinci koşu DURUR |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | devir1_sonuc.json + ozellik_Y1_d1.csv.gz + olay_Y1.csv.gz; DEVIR_1_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (W1 A ABD+AVR sınama, E2 B ABD+AVR eğitim) ayrı kodla (_yh_d1_yeniden: düz pandas sorgusu) yeniden üretilir; fark > 1e-12 ise DURUR |
| K12 | ifade | EVET | etiket yalnız karne kuralı (KATKI+ / KATKI− / SORGULA); 'iz / emare' denmez; FARK yüzde puan, yorum ayrı cümle; fiyat değişimi ile gerçekleşen getiri ayrımı: h5 hedef payı (stop'tan önce +%5), getiri değil |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_d1_ / yh_devir_ / YH_ESIK_D1 / _YH_D1 önekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi |


## DÜZELTME (ölçümden önce, 2026-11-19)

İlk ön kayıt commit'i b7ee46d (12:04 UTC). Koşu kapısı (yh_d1_kapi) ilk denemede DURDU: `OZELLIK_SHA` deseni `D1_OZELLIK_SHA` satırını da yakalıyordu (kapı kod hatası). Koşu kapıda durduğu için hiçbir getiri (h5 / es_h5 / st5) okunmadı, devir1_sonuc.json yazılmadı. Yalnız desen düzeltildi (`(?<![A-Z0-9_])OZELLIK_SHA`); tanımlar, eşikler (YH_ESIK_D1_SHA, devir1_esik.json), özellik dosyası ve huni değişmedi. Ön kayıt bu düzeltilmiş kodla yeniden üretildi ve ayrı commit'lendi; koşu bu commit'ten sonradır.
