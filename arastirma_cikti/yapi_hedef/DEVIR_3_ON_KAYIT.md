# YAPI_HEDEF — DEVİR 3 ÖN KAYIT (DAR YENİDEN SINAMA, karne v3: AYK / NR7 / W2D / W1; 2026-11-19)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; DEVİR 3 eklendi (yh_devir3_ozellik, yh_devir3_prefix, yh_devir3_kos). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar yalnız satır kimliği, dönem, giriş tarihi ve özellik dağılımıdır (getirisiz: h5 / es_h5 / st5 okunmadı).

- YH_ESIK_D3_SHA: `0b168445d9882171a1e389169779f710df0b5ec3f529803da786220472136179` (DEVİR 3: adaylar, kollar, karne v3, tabaka, güç, bootstrap, L3O, prefix)
- YH_ESIK_D2_SHA: `83c387e6e0651fc112b40a19d0f9b6123777e4679779c5aeb4707bcfa729e858` (= DEVIR_2_ON_KAYIT.md)
- YH_ESIK_D1_SHA: `2ffac1e395318b6f837ff3c627e022684a31951ed2a3a443442115bab842ea7e` (= DEVIR_1_ON_KAYIT.md)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md: Y1-Y11c AYNEN)
- YH_ESIK6_SHA: `6f05f68cd07560e407c7d1b06431990704b79441c51f4e09bbddfafba4086410` (= ON_KAYIT_6.md)
- YH_ESIK7_SHA: `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26` (= ON_KAYIT_7.md; Y12)
- YH_KOD_SHA: `4dd9fb27f27dd424ae1817ed9033eaf974df3c166241da2532497145c5b9c627` (YAPI_HEDEF.py)
- D3_ESIK_JSON_SHA: `c4a57e438d078737e95f1fdb15d8dad617ceb3c003ea58e578456f78fcf0cc40` (devir3_esik.json; d1 / d2 eşikleri AYNEN + F55 / F13 tercilleri)
- D3_PREFIX_SHA: `ee903323a05e4ab3c70b8ed1f5746445efd1e6aaaecc66008fa441aaf53fcfb3` (devir3_prefix.json; prefix / sızıntı denetimi, getirisiz)
- D2_OZELLIK_SHA: `9f164d91401fc025ac8c6db19d65e1c104a3e9a01491383d89636c02f2ffbbdc` (ozellik_Y1_d2.csv.gz; F47 / F55-F58; yeniden hesaplanmadı)
- D2_ESIK_JSON_SHA: `d4f2eb2c1ebbbeaa9474dd38b377e7bce0ec5dd6fd68b67f5afa44491bd4f03a` (devir2_esik.json; = DEVIR_2_ON_KAYIT mührü)
- D1_OZELLIK_SHA: `e80d9fb9af3d51c72f5f707c9cddb0319518f6aad5f5b25711e8dfb97f91fd7e` (ozellik_Y1_d1.csv.gz; F30 / F32; yeniden hesaplanmadı)
- D1_ESIK_JSON_SHA: `9f9db30fce92e9a91edd045b9a5f8b2a1026f5a25b7474d51cb4a03d93ef15e3` (devir1_esik.json; = DEVIR_1_ON_KAYIT mührü)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; ölçü satırları)
- Y9_OLAY_SHA: `56aa6101aba25cddd66dedddcba3d536a05b8e0850b727f015ef3cec295d5809` (olay_Y9.csv.gz; KOL-B)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F3 / F7 / F8 / F10 / F13 / F15 / F17)
- ZAMAN (UTC): `2026-11-19 13:36:25 UTC`

## 0. SEÇİM YANLILIĞI (K8 / K9; ölçümden önce yazıldı)

AYK, NR7, W2D, W1 adaylarının sonuçları DEVİR 1-2'de AYNI 2016-26 verisinde görüldü (bakılmış). Bu yeniden sınama bağımsız değildir: etiket en fazla 'EMARE (bakılmış)'; kesin karar Mart 2027 ileri testinde (kriz sonrası yeni veri, aynı eşik). Görülen önceki sonuçlar (DEVIR_2.md): AYK A eğitim 3294 / +1,86, sınama 2144 / +1,23 (çürütme lensi: oynaklık bileşimi, Simpson); NR7 A 1776 / +1,26, 985 / +1,15 (ABD sınama MARJ +4,2, AVR -4,8); W2D A 2725 / +0,01, 1598 / +1,87 (DEVİR 1'de de görüldü: ÇİFT KAT); W1 A 3037 / -0,14, 1608 / +1,02 (ÇİFT KAT). Bu yüzden: KATKI+ çıksa bile okuma 'EMARE (bakılmış)'; KATKI− 'kapandı (bakılmış)'; kesin karar Mart 2027 ileri testinde (IK_ILERI önerisi raporda).

### Beklenen ret nedenleri (ölçümden önce)

- **AYK**: stop payı (DEVİR 2'de dört hücrede st5 eşten +2,3..+4,0 puan yüksek) ve ATRP şartı (DEVİR 2 çürütme: ATRP tercilleri içinde sınama MARJ ABD T0 -3,1, T1 -1,9, AVR üç tercilde negatif).
- **NR7**: pazarlar arasında işaret (DEVİR 2 sınama ABD MARJ +4,2, AVR -4,8).
- **W2D**: eğitim FARK sıfırda (DEVİR 2 +0,01).
- **W1**: eğitim FARK negatif (DEVİR 2 -0,14); ATRP şartı (spread H/L'den türer).

## 1. ADAYLAR, F-KODLARI, TANIM, PENCERE, SABİT EŞİK

F-kodları DEVİR 1-2'nin kodlarıdır (F30 / F32: ozellik_Y1_d1; F47 / F55-F58: ozellik_Y1_d2). YENİ F-KODU YOK, yeni özellik dosyası yok; t = Y1 sinyal günü (kırılım mumu; kapanışı biliniyor), giriş t+1 açılış, ufuk 15 işlem günü, hedef +%5 (kapanış), stop = hat x 0,98; bölge [sol, t-1], sol = t - F8.

- **F47**: AYK kayma = |C_t - C_t-19| / (max H - min L), kutu [t-19, t] (ozellik_Y1_d2).
- **F55**: ATRP = ort(TR_j, j in [t-13, t]) / C_t; TR_j = max(H_j, C_j-1) - min(L_j, C_j-1) (ozellik_Y1_d2; yalnız K1 tabakası, aday değil).
- **F56**: NR7 (t-1): R = H - L; 1 eğer R_t-1 = min(R_t-7..t-1) (eşitlik dahil; Bulkowski 'kesin dar' tanımından küçük fark); t < 8 NaN (ozellik_Y1_d2).
- **F57**: ID/NR4 (t-1): R_t-1 = min(R_t-4..t-1) VE H_t-1 < H_t-2 VE L_t-1 > L_t-2 (bilgi; ozellik_Y1_d2).
- **F58**: önceki trend aşağı: 1 eğer C_t-1 < C_t-21 (bilgi tabakası; ozellik_Y1_d2).
- **F30**: W1 Corwin-Schultz spread oranı: ort S bölge [sol, t-1] (>= 10 çift) / ort S [sol-60, sol-1] (>= 40 bar); gece düzeltmesi; S < 0 -> 0 (ozellik_Y1_d1).
- **F32**: W2D = A - B; A = prod(O_j / C_j-1) - 1, B = prod(C_j / O_j) - 1, j in [sol, t-1], >= 15 bar (ozellik_Y1_d1).
- **F13**: kırılım hacmi = V_t / medyan(V bölge [sol, t-1]) (goz_etiket/ozellik_Y1; yalnız K1 tabakası).
- **F8**: bölge boyu = t - sol (sol = GOZ_ETIKET.ge_bolge, S6 nedensel; goz_etiket/ozellik_Y1).
- **F3**: bölge mum boyu / ATR (goz_etiket/ozellik_Y1; Spearman bilgi).
- **F7 / F10 / F15 / F17**: goz_etiket/ozellik_Y1 (tabaka F7 / F10 / F15; kol B F15 / F17).

| Aday | Kaynak | Tür | Süzgeç kuralı | Eşik kaynağı | Ad |
|---|---|---|---|---|---|
| AYK | DEVİR 2 AYK (F47) | ana | F47 <= q25 | devir2_esik.json AYNEN (F47) | kayma / yataylık alt çeyrek (yatay kutu) |
| NR7 | DEVİR 2 NR7 (F56) | ana | F56 == 1.0 | ikili sabit eşik (F56 / F57 / F58 == 1 ya da 0) | kırılım öncesi bar NR7 |
| W2D | DEVİR 1-2 W2D (F32) | ana | F32 >= q75 | devir1_esik.json AYNEN (F30 / F32; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi) | gece - gün içi birikim farkı üst çeyrek |
| W1 | DEVİR 1-2 W1 (F30) | ana | F30 < 1.0 VE F30 <= q25 | devir1_esik.json AYNEN (F30 / F32; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi) | Corwin-Schultz spread daraldı (oran < 1 VE alt çeyrek) |
| NR7a | DEVİR 2 NR7 | bilgi | F56 == 1.0 VE F58 == 1.0 | ikili sabit eşik (F56 / F57 / F58 == 1 ya da 0) | NR7 VE önceki trend aşağı (Bulkowski koşulu; sonuçtan sonra karar satırına YÜKSELTİLMEZ) |
| NR7y | DEVİR 2 NR7 | bilgi | F56 == 1.0 VE F58 == 0.0 | ikili sabit eşik (F56 / F57 / F58 == 1 ya da 0) | NR7 VE önceki trend yukarı |
| IDNR4 | DEVİR 2 NR7 | bilgi | F57 == 1.0 | ikili sabit eşik (F56 / F57 / F58 == 1 ya da 0) | kırılım öncesi bar ID/NR4 |
| NR7t | DEVİR 2 NR7 | ters | F56 == 0.0 | ikili sabit eşik (F56 / F57 / F58 == 1 ya da 0) | ters: NR7 değil |
| W2Dt | DEVİR 1-2 W2D | ters | F32 <= q25 | devir1_esik.json AYNEN (F30 / F32; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi) | ters: D alt çeyrek (ayna) |
| W1t | DEVİR 1-2 W1 | ters | F30 >= q75 | devir1_esik.json AYNEN (F30 / F32; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi) | ters: spread oranı üst çeyrek |

Kaynak notları: AYK — kaynakta birebir ölçü ve eşik yok (Kaufman ER / Choppiness akrabası; KER_20 ve CHOP bu devirde HESAPLANMADI, yalnız tanım bilgisi); NR7 — Crabel 1990 / Bulkowski thepatternsite.com/nr7.html ('önceki altı barın her birinden dar' = kesin; depo tanımı eşitlik dahil, küçük fark korunur); W2D — Lou, Polk, Skouras (2019) JFE 134(1) (kaynak penceresi ~1 ay; bizde bölge penceresi: 'kaynakta pencere uyumu yok', depo tanımı korunur); W1 — Corwin ve Schultz (2012) JF 67(2) (kaynak aylık ort; bizde bölge / önceki 60 bar oranı = depo uyarlaması). Kaynaklarda süzgeç eşiği yok -> veri-bağımsız çeyrek kuralı (2016-22, getirisiz) DEVİR 1-2'de sabitlendi; burada AYNEN kopyalandı.

### Eşikler (devir3_esik.json; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi; pazar içi, bütün Y1 olayları; kaynak json'lardan AYNEN)

| Özellik | Pazar | YÖN 1 q25 / q75 (n) | YÖN 2 q25 / q75 (n) | kaynak |
|---|---|---|---|---|
| F47 | ABD | 0.390143 / 0.723198 (8686) | 0.350464 / 0.713035 (6195) | devir2_esik.json |
| F47 | AVR | 0.408722 / 0.742558 (4496) | 0.420847 / 0.740981 (2558) | devir2_esik.json |
| F47 | BIST | 0.352629 / 0.714286 (2588) | 0.278922 / 0.695454 (2140) | devir2_esik.json |
| F30 | ABD | 0.754556 / 1.15633 (7912) | 0.767149 / 1.17767 (5566) | devir1_esik.json |
| F30 | AVR | 0.779934 / 1.14936 (4239) | 0.806001 / 1.15772 (2433) | devir1_esik.json |
| F30 | BIST | 0.711636 / 1.10136 (2288) | 0.707135 / 1.14256 (1696) | devir1_esik.json |
| F32 | ABD | -0.0463054 / 0.061542 (7006) | -0.0532395 / 0.0610446 (4786) | devir1_esik.json |
| F32 | AVR | -0.0591623 / 0.0626246 (3890) | -0.0657552 / 0.061323 (2247) | devir1_esik.json |
| F32 | BIST | 0.0187321 / 0.159009 (1874) | 0.0318036 / 0.160568 (1266) | devir1_esik.json |

Sabit ek şartlar: W1 için F30 < 1,0; NR7 F56 == 1 (ters F56 == 0); NR7a F58 == 1; IDNR4 F57 == 1.

### K1 tabaka tercil sınırları (2016-22, pazar içi; getirisiz; F10 / F15 / F7 devir2_esik.json AYNEN, F55 / F13 YENİ)

| Pazar | F10 t33 / t67 | F15 t33 / t67 | F7 t33 / t67 | F55 t33 / t67 | F13 t33 / t67 |
|---|---|---|---|---|---|
| ABD | 0.01649 / 0.03774 | 0.7282 / 1 | 0.4857 / 0.5556 | 0.01943 / 0.02812 | 1.078 / 1.566 |
| AVR | 0.01759 / 0.03737 | 0.7593 / 1 | 0.4762 / 0.5515 | 0.01741 / 0.02378 | 1.092 / 1.614 |
| BIST | 0.005435 / 0.02899 | 0.538 / 0.9099 | 0.3667 / 0.4581 | 0.02716 / 0.03439 | 2.32 / 4.502 |

### Ambargo (60 bar; devir2_esik.json 'ambargo' tarihleri AYNEN (pazar takvimi = V_<pazar>.pkl geçerli barları; YÖN 1 sınama girişi >= eğitim son girişi + 60 bar; YÖN 2 bilgi); kol tabanı aynı ambargoyla)

| Pazar | YÖN 1 eğitim son giriş | YÖN 1 sınama ilk izinli | YÖN 2 eğitim ilk giriş | YÖN 2 sınama son izinli |
|---|---|---|---|---|
| ABD | 2022-12-30 | 2023-03-29 | 2023-01-03 | 2022-10-06 |
| AVR | 2022-12-30 | 2023-03-24 | 2023-01-03 | 2022-10-10 |
| BIST | 2022-12-28 | 2023-03-29 | 2023-01-02 | 2022-10-10 |

## 2. ÖLÇÜ, KOLLAR, KARNE v3

- KOLLAR: A = Y1 (bütün olay_Y1.csv.gz satırları); B = Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; olay_Y9.csv.gz ile küme eşitliği). Karar pazarları: kol A ABD / AVR, kol B ABD (AVR kol B BİLGİ).
- ÖLÇÜ: 1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): n = h5 ve es_h5 olan olay; FARK = ort h5 - ort es_h5 (aynı gün aynı OC kovası eşleri); MARJ = FARK(aday VE kol) - FARK(kol), aynı pazar x hücre x ambargo; stop: ort st5 / ort es_st5. BİLGİ: MARJ_sonlu = FARK(aday VE kol) - FARK(kol VE aday özelliği sonlu) (W2D F32 / W1 F30 NaN tabanı farkı).
- KARNE v3 ETİKET: KARNE v3 (yalnız 'ana' adaylar). Kol A karar pazarları ABD ve AVR AYRI, kol B yalnız ABD; hücreler eğitim (2016-22) ve sınama (2023-26, ambargolu). ÖLÇÜLEMEDİ = bir karar hücresinde n < 30 (kol B: ya da ABD hücrelerinden birinde güç < 0,80). KATKI+ = her karar hücresinde FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; VE genel tabaka şartı; VE ATRP şartı (her F55 tercilinde MARJ > 0). KATKI− = her karar hücresinde MARJ < 0 VE bootstrap %95 üst ucu < 0. Değilse SORGULA. Ters yön (YÖN 2) hücresi, 'bilgi' / 'ters' adaylar, BIST ve ABD+AVR havuzu, AVR kol B yalnız BİLGİ.
- KARAR OKUMASI: KATKI+ en fazla 'EMARE (bakılmış)' okunur (seçim yanlılığı); KATKI− 'kapandı (bakılmış)' ancak bir karar hücresi n < 1.000 ise o hücre kesin değil; ÖLÇÜLEMEDİ iddia kapatmaz; kesin karar Mart 2027 ileri testi.
- BOOTSTRAP: {"B": 2000, "alt": 0.025, "ust": 0.975, "tohum": 1931, "birim": "giriş ayı (YYYY-MM)"}; MARJ her örneklemde (aday ve kol tabanı aynı aylarla) yeniden hesaplanır; alt ve üst uç aynı örneklemden.
- LEAVE-3-OUT: hücrede tek tek çıkarıldığında MARJ'ı en çok düşüren 3 ay birlikte çıkarılır; kalan MARJ > 0 olmalı (KATKI+) (AVR sınama AYK hücresi raporda ayrıca yazılır).
- K1 TABAKA: tercil sınırları pazar içinde 2016-22 bütün Y1 olaylarından (getirisiz): F10 / F15 / F7 devir2_esik.json'dan AYNEN, F55 / F13 yeni (devir3_esik.json). (i) GENEL TABAKA: MARJ (aday VE kol VE tabaka) - (kol VE tabaka), karar pazarları havuzunda (kol A ABD+AVR, kol B ABD) eğitim ve sınama; n >= 30 olan bir tabakada MARJ <= 0 ise KATKI+ -> SORGULA. (ii) ATRP ŞARTI (KATKI+ için ek): HER karar pazarı x HER hücre (eğitim, sınama) x HER F55 tercilinde MARJ sonlu VE > 0 (n şartı yok; n = 0 ise tutmaz).
- GÜÇ: hücre (kol x pazar x dönem) için: kol tabanından (h5 ve es_h5 olan olaylar) aday n'i kadar olay yerine koymadan R kez rastgele çekilir, MARJ_r = ort(h5 - es_h5)[çekilen] - ort(h5 - es_h5)[kol]; sigma = std(MARJ_r); güç = Phi(delta / sigma - z), delta = +5 puan (sabit, sonuçtan önce); kol B kararı yalnız ABD: iki ABD hücresinde güç >= 0,80 değilse ÖLÇÜLEMEDİ. Kol A güç bilgi. Getirisiz değildir (sigma getiriden); yalnız karar kapısı, eşik değil.
- KAPALI KONU: 4 aday da kapalı konuya (giriş zamanlaması / onay / hacim / stop) dokunmaz; F13 hacmi yalnız tabaka (aday değil).
- ÇOKLU KARŞILAŞTIRMA: 4 ana aday x 2 kol = 8 karar satırı; BH uygulanmaz (ikili dört hücre + bootstrap + L3O + tabaka + ATRP kuralı); şansla KATKI+ notu raporda.
- n < 30 HÜCRELER: karar pazarlarında (ve AVR kol B bilgi) 0 < n < 30 olan her ana aday hücresinin olayları raporda tek tek listelenir.
- YENİDEN ÜRETİM hücreleri: AYK / A / AVR / sinama; W1 / B / ABD / egitim.
- REGRESYON KAPISI: Y1-Y12 sha = ON_KAYIT_5 / 6 / 7; YH_ESIK_D1 + devir1_esik.json = DEVIR_1 mührü; YH_ESIK_D2 + devir2_esik.json + ozellik_Y1_d2 + olay_Y1 + olay_Y9 = DEVIR_2 mührü; KOL-B = olay_Y9 kümesi; devir3_esik.json koşuda kaynak json'lardan yeniden kopyalanır, aynı değilse DURUR.

## 3. GETİRİSİZ HUNİ (Y1 olayı -> aday tutan olay sayısı; YÖN 1 eşikleri; pazar x dönem; 'amb' = sınama ambargo sonrası)

| Satır | Kol | ABD 2016-22 | ABD 2023 | ABD 2024-26 | ABD amb | AVR 2016-22 | AVR 2023 | AVR 2024-26 | AVR amb | BIST 2016-22 | BIST 2023 | BIST 2024-26 | BIST amb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| taban | A | 8686 | 2042 | 4153 | 5700 | 4496 | 815 | 1743 | 2291 | 2588 | 381 | 1759 | 2118 |
| AYK | A | 2172 | 660 | 1154 | 1624 | 1124 | 200 | 409 | 548 | 647 | 149 | 532 | 671 |
| NR7 | A | 1164 | 233 | 532 | 708 | 612 | 100 | 212 | 289 | 381 | 69 | 248 | 313 |
| W2D | A | 1752 | 375 | 814 | 1109 | 973 | 197 | 357 | 509 | 469 | 18 | 302 | 319 |
| W1 | A | 1978 | 381 | 935 | 1188 | 1060 | 196 | 325 | 439 | 572 | 69 | 364 | 430 |
| NR7a | A | 207 | 67 | 121 | 171 | 110 | 19 | 34 | 47 | 120 | 34 | 97 | 130 |
| NR7y | A | 957 | 166 | 411 | 537 | 502 | 81 | 178 | 242 | 261 | 35 | 151 | 183 |
| IDNR4 | A | 461 | 121 | 255 | 347 | 297 | 51 | 99 | 137 | 183 | 24 | 118 | 140 |
| NR7t | A | 7522 | 1809 | 3621 | 4992 | 3884 | 715 | 1531 | 2002 | 2207 | 312 | 1511 | 1805 |
| W2Dt | A | 1752 | 489 | 837 | 1172 | 973 | 176 | 431 | 554 | 469 | 24 | 236 | 258 |
| W1t | A | 1978 | 459 | 1040 | 1431 | 1060 | 188 | 441 | 594 | 572 | 72 | 416 | 484 |
| taban | B | 346 | 146 | 232 | 355 | 89 | 20 | 55 | 72 | 238 | 81 | 297 | 373 |
| AYK | B | 157 | 80 | 123 | 189 | 41 | 13 | 23 | 34 | 101 | 53 | 143 | 192 |
| NR7 | B | 48 | 20 | 44 | 61 | 13 | 2 | 4 | 6 | 44 | 13 | 41 | 54 |
| W2D | B | 51 | 31 | 39 | 66 | 15 | 5 | 17 | 22 | 43 | 3 | 65 | 68 |
| W1 | B | 53 | 15 | 44 | 52 | 15 | 2 | 4 | 5 | 56 | 13 | 73 | 85 |
| NR7a | B | 20 | 14 | 27 | 39 | 7 | 1 | 2 | 3 | 24 | 12 | 27 | 39 |
| NR7y | B | 28 | 6 | 17 | 22 | 6 | 1 | 2 | 3 | 20 | 1 | 14 | 15 |
| IDNR4 | B | 15 | 10 | 13 | 23 | 2 | 0 | 2 | 2 | 22 | 3 | 17 | 20 |
| NR7t | B | 298 | 126 | 188 | 294 | 76 | 18 | 51 | 66 | 194 | 68 | 256 | 319 |
| W2Dt | B | 51 | 13 | 23 | 33 | 8 | 4 | 6 | 9 | 48 | 6 | 20 | 25 |
| W1t | B | 84 | 46 | 54 | 95 | 31 | 9 | 18 | 27 | 54 | 19 | 54 | 71 |

## 4. PREFIX / SIZINTI DENETİMİ (K2; devir3_prefix.json, getirisiz)

pazar başına n rastgele Y1 olayında F3 / F7 / F8 / F10 / F13 / F15 / F17 (GOZ_ETIKET.ge_ozellik_bar), F30 / F32 (yh_d1_bar), F47 / F55 / F56-F58 (yh_d2_bar) tam veride ve veri t'de kesilince yeniden hesaplanır; ikisi de mühürlü dosya değerine eşit olmalı (rtol 1e-5: goz_etiket/ozellik_Y1 6 anlamlı basamakla yazılı); t - sol = F8 ayrıca; tutmazsa DURUR.

| Pazar | denetlenen | tuttu | V_<pazar>.pkl sütunları (K6) |
|---|---|---|---|
| ABD | 30 | 30 | Close, High, Low, Open, Volume |
| AVR | 30 | 30 | Close, High, Kur, Low, Open, Volume |
| BIST | 30 | 30 | Close, High, Low, Open, Volume |

## 5. MEKANİK İLİŞKİ (K1; getirisiz)

### Spearman (aday özelliği x F3 mum boyu / F13 kırılım hacmi / F55 ATRP / F10 bölge net / F15 konum)

| Kapsam | Özellik | F3 | F13 | F55 | F10 | F15 |
|---|---|---|---|---|---|---|
| hepsi | F47 | -0.04 | +0.01 | -0.26 | +0.19 | +0.25 |
| hepsi | F56 | -0.01 | -0.06 | +0.01 | -0.01 | -0.01 |
| hepsi | F32 | -0.09 | +0.19 | +0.17 | -0.23 | -0.16 |
| hepsi | F30 | +0.29 | -0.04 | +0.07 | -0.06 | -0.02 |
| ABD | F47 | -0.05 | +0.04 | -0.27 | +0.18 | +0.25 |
| ABD | F56 | +0.00 | -0.09 | +0.01 | -0.00 | -0.01 |
| ABD | F32 | -0.00 | +0.07 | +0.10 | -0.20 | -0.08 |
| ABD | F30 | +0.26 | +0.01 | +0.12 | -0.10 | -0.06 |
| AVR | F47 | -0.10 | +0.02 | -0.23 | +0.12 | +0.20 |
| AVR | F56 | -0.00 | -0.07 | -0.01 | -0.00 | +0.01 |
| AVR | F32 | -0.04 | +0.08 | +0.05 | -0.19 | -0.14 |
| AVR | F30 | +0.26 | -0.03 | +0.06 | -0.07 | -0.08 |
| BIST | F47 | +0.03 | +0.04 | -0.18 | +0.25 | +0.27 |
| BIST | F56 | -0.02 | -0.01 | +0.03 | -0.04 | -0.02 |
| BIST | F32 | -0.15 | +0.17 | +0.02 | -0.31 | -0.07 |
| BIST | F30 | +0.38 | -0.09 | +0.13 | +0.03 | +0.07 |

### F56 (NR7) sıklığı ve NaN sayıları (bütün Y1)

| Pazar | olay | F56 sonlu n | F56 = 1 payı | NaN F47 / F55 / F56 / F32 / F30 / F13 |
|---|---|---|---|---|
| ABD | 14881 | 14881 | %13.0 | 0 / 0 / 0 / 3089 / 1403 / 0 |
| AVR | 7054 | 7054 | %13.1 | 0 / 0 / 0 / 917 / 382 / 0 |
| BIST | 4728 | 4728 | %14.8 | 0 / 0 / 0 / 1588 / 744 / 0 |

Uygulama yorumları (ölçümden önce): (1) W2D (F32) ve W1 (F30) bölge kısa / önceki pencere eksikse NaN'dır; kol tabanı (bütün Y1) ile aday kümesi farklı uzunlukta bölgelerden gelir -> MARJ_sonlu (taban = aynı F sonlu olaylar) BİLGİ satırı olarak raporlanır, karar MARJ'ladır; (2) W2D ve W2Dt aynı F32'nin iki ucudur (ayna): ikisi bağımsız sayılmaz; (3) NR7 aralığı ATR'ye göre küçük olduğundan F55 ile mekanik ilişki beklenir (Spearman yukarıda) -> ATRP şartı belirleyici; (4) W1 spread H/L aralığından türer: F3 / F55 ile Spearman yüksekse ve ATRP şartı tutmazsa W1 'küçük mum'un yeniden adlandırılmışı sayılır; (5) NR7a (Bulkowski düşüş trendi koşulu) yalnız bilgi; (6) K6: W2D için düzeltilmiş / ham fiyat karışmaz (her pazar tek OHLCV kipi; ayrı Adj Close yok; tablo 4); temettü gecesi kip neyse eş ve olay için aynı; (7) KER_20 / CHOP hesaplanmadı (aday değil).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | olay ve eş olay_Y1.csv.gz'den (aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar geometrisi); MARJ kol tabanına göre aynı pazar x hücre x ambargo; K1 TABAKA v3: F10 / F15 / F7 + F55 ATRP + F13 hacim tercilleri (devir3_esik.json, 2016-22 getirisiz); KATKI+ için HER karar pazarı x hücre x ATRP tercilinde MARJ > 0; mekanik ilişki Spearman (F47 / F56 / F32 / F30 ile F3 / F13 / F55 / F10 / F15) ve F56 sıklığı bu ön kayıtta getirisiz basılı; W2D / W1 NaN tabanı için MARJ_sonlu bilgi satırı |
| K2 | geleceğe bakma | EVET | kullanılan bütün F'ler yalnız [.., t] barlarından (t = sinyal günü kapanışı, giriş t+1 açılış): yh_devir3_prefix pazar başına 30 olayda 14 F'yi (F8 = t - sol dahil) tam veride ve veri t'de kesilince yeniden hesaplar, mühürlü dosyaya eşit (devir3_prefix.json; DURUR); F53 / F54 kesit sırası (bugünün evreni) KULLANILMAZ, F55 hisse içi ATR / C; tercil / çeyrek eşikleri getirisiz ve ölçümden önce mühürlü; ambargo 60 bar |
| K3 | geçerli bar | EVET | geçerli bar süzgeci _yh_hazir / OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); F'ler geçerli bar sayımıyla (mühürlü dosyalar); NR7 aralığı H-L > 0 barlardan |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç yalnız seçer; P olay / P eş ayrı, MARJ farkı; bootstrap birimi giriş ayı (aynı ay olayları birlikte) |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (olay_Y1 E0); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA) |
| K6 | veri birimi | EVET | V_*.pkl tek kip: her pazar sütunları yalnız Open / High / Low / Close / Volume (ayrı 'Adj Close' yok; ön kayıtta pazar başına sütun kümesi basılı) -> W2D'nin A (gece) ve B (gün içi) çarpanları aynı seriden, düzeltilmiş / ham karışmaz; ölçüler oran / ikili (birimsiz), AVR yerel para hisse içi oran |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD / V_AVR / V_BIST; batan / kottan çıkan yok; k34_yahoo bu koşuda yüklenmez, Y1 sembollerinin hepsi V_<pazar>'da): P olay ve P eş YUKARI YANLI, FARK'ta kısmen götürür, kol B (dipte) yanlılık daha büyük olabilir; kesit ölçüleri (F52-F55 RVOL kesit) aday değil; raporda yazılır |
| K8 | örneklem ve dönem | EVET | SEÇİM YANLILIĞI: 4 adayın sonucu DEVİR 1-2'de aynı veride görüldü -> etiket en fazla 'EMARE (bakılmış)', kesin karar Mart 2027 ileri testi; hücre n < 30 ÖLÇÜLEMEDİ ve olayları raporda tek tek listelenir; ABD ve AVR ayrı, eğitim + sınama aynı yön; kol B yalnız ABD + güç simülasyonu (delta +5 puan, güç >= 0,80); KATKI− hücresi n < 1.000 ise kesin değil; 8 karar satırı BH yok -> şans notu |
| K9 | ön kayıt | EVET | DEVIR_3_ON_KAYIT.md: YH_ESIK_D3 / D2 / D1 / Y1-Y12 sha, kod sha, devir3_esik.json / devir3_prefix.json / ozellik d1 / d2 / Y1 / olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d3_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; eşikler devir1 / devir2_esik.json'dan AYNEN (koşuda yeniden kopyalanıp eşitlik denetlenir); ön kayıt commit'i ('DEVİR 3 ön kayıt') koşudan önce; ikinci koşu DURUR; seçim yanlılığı bu ön kayıtta yazılı |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | devir3_sonuc.json + olay_Y1 / ozellik dosyaları; DEVIR_3_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (AYK A AVR sınama, W1 B ABD eğitim) ayrı kodla (_yh_d3_yeniden: ham csv + devir3_esik.json, düz pandas sorgusu) yeniden üretilir; fark > 1e-12 ise DURUR |
| K12 | ifade | EVET | etiket yalnız karne v3 kuralı (KATKI+ / KATKI− / SORGULA / ÖLÇÜLEMEDİ / BİLGİ); KATKI+ en fazla 'EMARE (bakılmış)' okunur, 'iz' denmez; FARK yüzde puan, h5 hedef payı (stop'tan önce +%5), getiri değil; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_d3_ / yh_devir3_ / YH_ESIK_D3 / _YH_D3 / YH_D3 / YH_KONTROL_D3 önekli; DEVİR 1-2 adları ezilmez); yasak defter dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi |

