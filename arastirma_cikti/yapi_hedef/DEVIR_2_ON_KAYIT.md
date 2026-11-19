# YAPI_HEDEF — DEVİR 2 ÖN KAYIT (karne v2; Y2 web entegrasyon adayları F43-F64 + DEVİR 1 YENİDEN W1 / W2 / W2D; 2026-11-19)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; DEVİR 2 eklendi (yh_devir2_ozellik, yh_devir2_kos). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar yalnız satır kimliği, dönem, giriş tarihi ve özellik dağılımıdır (getirisiz: h5 / es_h5 / st5 okunmadı).

- YH_ESIK_D2_SHA: `83c387e6e0651fc112b40a19d0f9b6123777e4679779c5aeb4707bcfa729e858` (DEVİR 2: tanımlar, pencereler, aday kuralları, kol, dönem, ambargo, bootstrap, L3O, tabaka, etiket)
- YH_ESIK_D1_SHA: `2ffac1e395318b6f837ff3c627e022684a31951ed2a3a443442115bab842ea7e` (= DEVIR_1_ON_KAYIT.md; W1 / W2 / W2D tanım ve eşik kuralı AYNEN)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md: Y1-Y11c AYNEN)
- YH_ESIK6_SHA: `6f05f68cd07560e407c7d1b06431990704b79441c51f4e09bbddfafba4086410` (= ON_KAYIT_6.md)
- YH_ESIK7_SHA: `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26` (= ON_KAYIT_7.md; Y12)
- YH_KOD_SHA: `ffb3e5de498a0ee0fcfca3e89154ec787baee2748f8e8122309e9421b8f5c9a1` (YAPI_HEDEF.py)
- D2_OZELLIK_SHA: `9f164d91401fc025ac8c6db19d65e1c104a3e9a01491383d89636c02f2ffbbdc` (ozellik_Y1_d2.csv.gz; F43-F64)
- D2_ESIK_JSON_SHA: `d4f2eb2c1ebbbeaa9474dd38b377e7bce0ec5dd6fd68b67f5afa44491bd4f03a` (devir2_esik.json; çeyrekler, tabaka tercilleri, ambargo tarihleri)
- D1_OZELLIK_SHA: `e80d9fb9af3d51c72f5f707c9cddb0319518f6aad5f5b25711e8dfb97f91fd7e` (ozellik_Y1_d1.csv.gz; F30-F32 DEVİR 1 YENİDEN)
- D1_ESIK_JSON_SHA: `9f9db30fce92e9a91edd045b9a5f8b2a1026f5a25b7474d51cb4a03d93ef15e3` (devir1_esik.json; = DEVIR_1_ON_KAYIT mührü, yeni eşik seçilmedi)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; ölçü satırları)
- Y9_OLAY_SHA: `56aa6101aba25cddd66dedddcba3d536a05b8e0850b727f015ef3cec295d5809` (olay_Y9.csv.gz; KOL-B regresyonu)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F7 / F8 / F10 / F15 / F17)
- ZAMAN (UTC): `2026-11-19 12:51:05 UTC`

## 1. ADAYLAR, F-KODLARI, TANIM, PENCERE, SABİT EŞİK

F-kodları F43'ten başlar: F30-F42 DEVİR 1'in (ozellik_Y1_d1.csv.gz) kodlarıdır; DEVİR 1 YENİDEN adayları F30 / F31 / F32'yi aynen kullanır.
Pencereler: {"pp": 10, "sma_kisa": 10, "sma_uzun": 50, "kutu": 20, "kutu_gecmis": 252, "kutu_min": 200, "pivot": 6, "rvol": 14, "rvol_min": 10, "atr": 14, "atr_min_oran": 0.01, "kesit_ilk": 20, "nr7": 7, "nr4": 4, "trend": 20, "vcp_gun": 120, "vcp_atr_kat": 1.5, "vcp_oran": 0.7, "vcp_ilk": 10.0, "vcp_ilk_kucuk": 5.0, "vcp_son": 15.0, "vcp_bar": 5, "vcp_hacim": 50}. t = Y1 sinyal günü (kırılım mumu; kapanışı biliniyor), giriş t+1 açılış; bölge [sol, t-1], sol = t - F8.

- **F43**: Y2_PP pocket pivot (filtresiz, ana): 1 eğer C_t > C_t-1 ve V_t > max{V_i: i in [t-10, t-1], C_i < C_i-1} (kesin büyük); C_t <= C_t-1 ise 0; yukarı gün ama pencerede düşüş günü yoksa NaN; t-11'den geçmiş yoksa NaN.
- **F44**: Y2_PPR = V_t / max(düşüş günü V, [t-10, t-1]) (sürekli; düşüş günü yoksa NaN; yukarı gün şartı YOK).
- **F45**: Y2_PP LuxAlgo filtreli (bilgi): F43 = 1 VE C_t > SMA50_t VE L_t <= max(SMA10_t, 1,02 x SMA50_t) VE C_t > SMA10_t; SMA50 için 50 bar yoksa NaN.
- **F46**: Y2_YUZDELIK: P_s = (max H - min L) / min L, kutu [s-19, s]; F46 = (#{P_s < P_t} + 0,5 x #{P_s = P_t}) / M, s in [t-251, t] (t dahil, s-19 >= 0); M < 200 ise NaN.
- **F47**: Y2_KAYMA = |C_t - C_t-19| / (max H - min L) (kutu [t-19, t]).
- **F48**: Y2_ARALIK_CV = std(H-L) / ort(H-L), kutu [t-19, t] (ddof 0).
- **F49**: Y2_TEK_GUN_PAYI = max(H-L) / (max H - min L), kutu [t-19, t].
- **F50**: Y2_DUZ_TAVAN: pivot tepe j = H_j = max H[j-6, j+6] ve H_j > max H[j-6, j-1]; onaylı pivot j + 6 <= t; bölge pivotları j in [sol, t-6]; a, c = son iki onaylı pivot (a önce); 1 eğer |a - c| <= ort(H-L)[idx a .. idx c] VE C_t-1 <= max(a, c); ikiden az pivot ise 0.
- **F51**: Y2_TAVAN_FARK = |a - c| / ort(H-L)[idx a .. idx c] (sürekli; ikiden az pivot NaN).
- **F52**: Y2_RVOL14: R_t = V_t / ort(V_t-14..t-1) (geçerli bar; t < 14 ise NaN; ort 0 ise NaN).
- **F53**: Y2_KESIT_SIRA: aynı tarih, aynı pazar evreninde (V_<pazar>.pkl o gün geçerli barı olan hisseler; evren_bas sonrası) ATR14/C > %1 olanlar içinde R_t'ye göre azalan sıra (1 = en yüksek; eşitlik 'min'); olay hissesi ATR filtresini geçmezse NaN.
- **F54**: Y2_KESIT_YUZDE: R_t'nin aynı gün aynı pazar bütün evren içindeki yüzdelik sırası (ortalama sıra / sayı; bilgi).
- **F55**: Y2_ATRP = ort(TR_j, j in [t-13, t]) / C_t; TR_j = max(H_j, C_j-1) - min(L_j, C_j-1); t < 14 ise NaN.
- **F56**: Y2_NR7 (t-1): R_i = H_i - L_i; 1 eğer R_t-1 = min(R_t-7..t-1) (eşitlik dahil); t < 8 ise NaN.
- **F57**: Y2_IDNR4 (t-1): 1 eğer R_t-1 = min(R_t-4..t-1) VE H_t-1 < H_t-2 VE L_t-1 > L_t-2.
- **F58**: Y2_ONCEKI_TREND_ASAGI = 1 eğer C_t-1 < C_t-21 (bilgi tabakası; t < 21 ise NaN).
- **F59**: Y2_NR7 (t; bilgi): 1 eğer R_t = min(R_t-6..t).
- **F60**: Y2_VCP (kaynak, ilk derinlik >= %10): ZigZag (H / L, dönüş eşiği 1,5 x ATR14_j) pencere [t-120, t-1]; yalnız ONAYLI pivotlar (dönüş görülen; son açık salınım girmez); daralmalar = ardışık (tepe -> sonraki dip) çiftleri, penceredeki EN YÜKSEK tepe pivotundan başlar; d_k = 100 (H_k - L_k) / H_k; 1 eğer n >= 2 VE d_1 >= 10 VE her d_k+1 <= 0,70 d_k VE her daralma (dip idx - tepe idx) >= 5 bar VE d_n <= 15 VE ort V[son daralma] < ort V[t-50, t-1]; değilse 0; t-120 < 14 ise NaN.
- **F61**: Y2_VCP5 (bilgi): F60 ile aynı, ilk derinlik >= %5.
- **F62**: Y2_VCP_ORAN = d_n / d_1 (n >= 2; değilse NaN).
- **F63**: Y2_VCP_N = daralma sayısı n (bilgi).
- **F64**: Y2_KIRILIM_HACMI = V_t / ort V[t-50, t-1] (bilgi; kaynakta alım şartı >= 1,5).

Çeyrek kuralı: kaynakta eşik olmayan adaylar (F44 q75, F47 / F48 / F49 q25, F52 q75) için PAZAR içinde bütün Y1 olaylarının sonlu değerlerinden (getirisiz); YÖN 1 eğitim 2016-22, YÖN 2 (ters yürüyen, BİLGİ) 2023-26; KOL-B aynı eşikler; devir2_esik.json. W1 / W2 / W2D (DEVİR 1 YENİDEN) eşikleri devir1_esik.json'dan AYNEN (esik_d1_sha = YH_ESIK_D1 sha; yeni eşik seçilmez).

| Aday | Kaynak | Tür | Süzgeç kuralı | Eşik kaynağı | Ad |
|---|---|---|---|---|---|
| PP | Y2_PP_HACIM | ana (KAPALI KONU) | F43 == 1.0 | sabit / devir2_esik.json | Pocket pivot (filtresiz): yukarı gün hacmi > son 10 gün en büyük düşüş günü hacmi |
| PPq | Y2_PP_HACIM | bilgi | F44 >= q75 | sabit / devir2_esik.json | PPR üst çeyrek |
| PPb | Y2_PP_HACIM | bilgi | F45 == 1.0 | sabit / devir2_esik.json | Pocket pivot LuxAlgo filtreli |
| PPt | Y2_PP_HACIM | ters | F43 == 0.0 | sabit / devir2_esik.json | ters: pocket pivot değil |
| AY | Y2_ARALIK_YUZDELIK_KAYMA | ana | F46 <= 0.1 | sabit / devir2_esik.json | 20 günlük kutu yüzdeliği <= %10 (nadir sıkışma) |
| AYK | Y2_ARALIK_YUZDELIK_KAYMA | ana | F47 <= q25 | sabit / devir2_esik.json | KAYMA alt çeyrek (yatay kutu) |
| AY5 | Y2_ARALIK_YUZDELIK_KAYMA | bilgi | F46 <= 0.05 | sabit / devir2_esik.json | yüzdelik <= %5 |
| AY2 | Y2_ARALIK_YUZDELIK_KAYMA | bilgi | F46 <= 0.02 | sabit / devir2_esik.json | yüzdelik <= %2 |
| AYKK | Y2_ARALIK_YUZDELIK_KAYMA | bilgi | F46 <= 0.1 VE F47 <= q25 | sabit / devir2_esik.json | nadir VE yatay |
| AYC | Y2_ARALIK_YUZDELIK_KAYMA | bilgi | F48 <= q25 | sabit / devir2_esik.json | aralık CV alt çeyrek |
| AYT | Y2_ARALIK_YUZDELIK_KAYMA | bilgi | F49 <= q25 | sabit / devir2_esik.json | tek gün payı alt çeyrek |
| AYt | Y2_ARALIK_YUZDELIK_KAYMA | ters | F46 >= 0.9 | sabit / devir2_esik.json | ters: yüzdelik >= %90 (geniş kutu) |
| DT | Y2_DUZ_TAVAN_ABL | ana | F50 == 1.0 | sabit / devir2_esik.json | düz tavan: son iki pivot tepe farkı <= 1 x ort(H-L) |
| DT05 | Y2_DUZ_TAVAN_ABL | bilgi | F51 <= 0.5 | sabit / devir2_esik.json | tavan farkı <= 0,5 x ort(H-L) |
| DT2 | Y2_DUZ_TAVAN_ABL | bilgi | F51 <= 2.0 | sabit / devir2_esik.json | tavan farkı <= 2 x ort(H-L) |
| DTt | Y2_DUZ_TAVAN_ABL | ters | F50 == 0.0 | sabit / devir2_esik.json | ters: düz tavan yok |
| RV | Y2_RVOL14_KESIT | ana (KAPALI KONU) | F52 >= 1.0 VE F53 <= 20.0 VE F55 > 0.01 | sabit / devir2_esik.json | RVOL14 >= 1 VE günün ilk 20'si (ATR/C > %1 evreninde) |
| RVq | Y2_RVOL14_KESIT | bilgi | F52 >= q75 | sabit / devir2_esik.json | RVOL14 üst çeyrek |
| RVt | Y2_RVOL14_KESIT | ters | F52 < 1.0 | sabit / devir2_esik.json | ters: RVOL14 < 1 |
| NR7 | Y2_NR7_IDNR4 | ana | F56 == 1.0 | sabit / devir2_esik.json | kırılım öncesi bar NR7 |
| NR7a | Y2_NR7_IDNR4 | bilgi | F56 == 1.0 VE F58 == 1.0 | sabit / devir2_esik.json | NR7 VE önceki trend aşağı |
| NR7y | Y2_NR7_IDNR4 | bilgi | F56 == 1.0 VE F58 == 0.0 | sabit / devir2_esik.json | NR7 VE önceki trend yukarı |
| IDNR4 | Y2_NR7_IDNR4 | bilgi | F57 == 1.0 | sabit / devir2_esik.json | kırılım öncesi bar ID/NR4 |
| NR7t | Y2_NR7_IDNR4 | ters | F56 == 0.0 | sabit / devir2_esik.json | ters: NR7 değil |
| VCP | Y2_VCP_ORAN | ana | F60 == 1.0 | sabit / devir2_esik.json | VCP (kaynak eşikleri; ilk derinlik >= %10) |
| VCP5 | Y2_VCP_ORAN | bilgi | F61 == 1.0 | sabit / devir2_esik.json | VCP ilk derinlik >= %5 (küçük yapı) |
| VCPt | Y2_VCP_ORAN | ters | F60 == 0.0 | sabit / devir2_esik.json | ters: VCP değil |
| W1 | DEVİR 1 YENİDEN W1 | ana | F30 < 1.0 VE F30 <= q25 | devir1_esik.json | DEVİR 1 YENİDEN: CS spread daraldı |
| W1t | DEVİR 1 YENİDEN W1 | ters | F30 >= q75 | devir1_esik.json | ters: spread üst çeyrek |
| W2 | DEVİR 1 YENİDEN W2 | ana | F31 > 0.0 VE F31 >= q75 | devir1_esik.json | DEVİR 1 YENİDEN: gün-içi birikim B > 0 ve üst çeyrek |
| W2t | DEVİR 1 YENİDEN W2 | ters | F31 <= q25 | devir1_esik.json | ters: B alt çeyrek |
| W2D | DEVİR 1 YENİDEN W2 | ana | F32 >= q75 | devir1_esik.json | DEVİR 1 YENİDEN: D = gece - gün-içi üst çeyrek |
| W2Dt | DEVİR 1 YENİDEN W2 | ters | F32 <= q25 | devir1_esik.json | ters: D alt çeyrek |

### Çeyrek eşikleri (devir2_esik.json; YÖN 1 = 2016-22 karar, YÖN 2 = 2023-26 bilgi; pazar içi, bütün Y1 olayları)

| Özellik | Pazar | YÖN 1 q25 / q75 (n) | YÖN 2 q25 / q75 (n) |
|---|---|---|---|
| F44 | ABD | 0.708884 / 1.4074 (8684) | 0.719272 / 1.384 (6193) |
| F44 | AVR | 0.68714 / 1.42609 (4494) | 0.618608 / 1.44685 (2556) |
| F44 | BIST | 1.38174 / 4.00799 (2580) | 1.1306 / 2.50179 (2139) |
| F47 | ABD | 0.390143 / 0.723198 (8686) | 0.350464 / 0.713035 (6195) |
| F47 | AVR | 0.408722 / 0.742558 (4496) | 0.420847 / 0.740981 (2558) |
| F47 | BIST | 0.352629 / 0.714286 (2588) | 0.278922 / 0.695454 (2140) |
| F48 | ABD | 0.31081 / 0.429897 (8686) | 0.313053 / 0.438331 (6195) |
| F48 | AVR | 0.315776 / 0.44782 (4496) | 0.323034 / 0.455968 (2558) |
| F48 | BIST | 0.40118 / 0.593522 (2588) | 0.367975 / 0.514998 (2140) |
| F49 | ABD | 0.385471 / 0.541747 (8686) | 0.383984 / 0.542026 (6195) |
| F49 | AVR | 0.398575 / 0.562449 (4496) | 0.396601 / 0.567335 (2558) |
| F49 | BIST | 0.447292 / 0.64108 (2588) | 0.443182 / 0.618087 (2140) |
| F52 | ABD | 0.947761 / 1.71673 (8686) | 0.964207 / 1.679 (6195) |
| F52 | AVR | 0.944721 / 1.76569 (4496) | 0.901731 / 1.80826 (2558) |
| F52 | BIST | 1.7462 / 4.5825 (2588) | 1.39024 / 2.91811 (2140) |

### DEVİR 1 YENİDEN eşikleri (devir1_esik.json AYNEN)

| Özellik | Pazar | YÖN 1 q25 / q75 | YÖN 2 q25 / q75 |
|---|---|---|---|
| F30 | ABD | 0.754556 / 1.15633 | 0.767149 / 1.17767 |
| F30 | AVR | 0.779934 / 1.14936 | 0.806001 / 1.15772 |
| F30 | BIST | 0.711636 / 1.10136 | 0.707135 / 1.14256 |
| F31 | ABD | -0.0170995 / 0.0502927 | -0.0211116 / 0.0527261 |
| F31 | AVR | -0.0198502 / 0.0555593 | -0.0180964 / 0.0579193 |
| F31 | BIST | -0.0759499 / 0.0116031 | -0.0815237 / 0.00376359 |
| F32 | ABD | -0.0463054 / 0.061542 | -0.0532395 / 0.0610446 |
| F32 | AVR | -0.0591623 / 0.0626246 | -0.0657552 / 0.061323 |
| F32 | BIST | 0.0187321 / 0.159009 | 0.0318036 / 0.160568 |

### K1 tabaka tercil sınırları (2016-22, pazar içi; getirisiz)

| Pazar | F10 t33 / t67 | F15 t33 / t67 | F7 t33 / t67 |
|---|---|---|---|
| ABD | 0.01649 / 0.03774 | 0.7282 / 1 | 0.4857 / 0.5556 |
| AVR | 0.01759 / 0.03737 | 0.7593 / 1 | 0.4762 / 0.5515 |
| BIST | 0.005435 / 0.02899 | 0.538 / 0.9099 | 0.3667 / 0.4581 |

### Ambargo (60 bar; pazar takvimi = V_<pazar>.pkl geçerli barlarının birleşimi; YÖN 1: sınama (2023-26) olayı giriş sırası - eğitim (2016-22) son giriş sırası >= 60 bar; YÖN 2 (BİLGİ): eğitim (2023-26) ilk giriş sırası - sınama (2016-22) olayı giriş sırası >= 60 bar; kol tabanı aynı ambargoyla)

| Pazar | YÖN 1 eğitim son giriş | YÖN 1 sınama ilk izinli | YÖN 2 eğitim ilk giriş | YÖN 2 sınama son izinli |
|---|---|---|---|---|
| ABD | 2022-12-30 | 2023-03-29 | 2023-01-03 | 2022-10-06 |
| AVR | 2022-12-30 | 2023-03-24 | 2023-01-03 | 2022-10-10 |
| BIST | 2022-12-28 | 2023-03-29 | 2023-01-02 | 2022-10-10 |

## 2. ÖLÇÜ, KOLLAR, KARNE v2

- KOLLAR: A = Y1 (bütün olay_Y1.csv.gz satırları); B = Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; olay_Y9.csv.gz ile küme eşitliği).
- ÖLÇÜ: 1. tur 15 bar cetveli AYNEN, satırlar olay_Y1.csv.gz (yeniden simülasyon yok): n = h5 ve es_h5 olan olay; FARK = ort h5 - ort es_h5 (aynı gün aynı OC kovası eşleri); MARJ = FARK(aday VE kol) - FARK(kol), aynı pazar x hücre (aynı ambargo); stop: ort st5 / ort es_st5.
- KARNE v2 ETİKET: KARNE v2 (yalnız 'ana' adaylar): KATKI+ = ABD ve AVR AYRI AYRI, eğitim (2016-22) ve sınama (2023-26, ambargolu) dört hücrenin her birinde n >= 30 VE FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; ayrıca K1 tabaka şartı; KATKI− = dört hücrede n >= 30 VE MARJ < 0; değilse SORGULA. Ters yön (YÖN 2) hücresi ve 'bilgi' / 'ters' adaylar yalnız BİLGİ (bağımsız sayılmaz). BIST ve ABD+AVR bilgi (tabaka hariç).
- BOOTSTRAP: {"B": 2000, "q": 0.025, "tohum": 1120, "birim": "giriş ayı (YYYY-MM)"}; MARJ her örneklemde (aday ve kol tabanı aynı aylarla) yeniden hesaplanır.
- LEAVE-3-OUT: hücrede tek tek çıkarıldığında MARJ'ı en çok düşüren 3 ay birlikte çıkarılır; kalan MARJ > 0 olmalı.
- K1 TABAKA: tercil sınırları pazar içinde 2016-22 bütün Y1 olaylarından (getirisiz; ozellik_Y1.csv.gz); her ana aday için MARJ (aday VE kol VE tabaka) - (kol VE tabaka) ABD+AVR havuzunda eğitim ve sınama hücrelerinde; n >= 30 olan bir tabakada MARJ <= 0 ise KATKI+ -> SORGULA ('K1 tabaka').
- KAPALI KONU: PP ve RV 'giriş zamanlaması / onay / hacim' kapalı konusuna dokunur (COL_OZET): sonuç yapı ölçüsü olarak raporlanır; KATKI+ çıksa bile üretime / kurala girmeden ana model ve Cemal onayı gerekir.
- ÇOKLU KARŞILAŞTIRMA: 10 ana aday x 2 kol = 20 karar satırı: BH uygulanmaz (dört hücre + bootstrap + L3O + tabaka ikili kuralı); şansla KATKI+ notu raporda.
- YENİDEN ÜRETİM hücreleri: AY / A / ABD / sinama; W2 / B / AVR / egitim.
- REGRESYON KAPISI: YH_ESIK / 6 / 7 sha = ON_KAYIT_5 / 6 / 7; YH_ESIK_D1 ve devir1_esik.json = DEVIR_1_ON_KAYIT mührü; KOL-B = olay_Y9 kümesi; eşik json yeniden hesapla aynı; değilse DURUR.

## 3. GETİRİSİZ HUNİ (Y1 olayı -> aday tutan olay sayısı; YÖN 1 eşikleri; pazar x dönem; 'amb' = sınama ambargo sonrası)

| Satır | Kol | ABD 2016-22 | ABD 2023 | ABD 2024-26 | ABD amb | AVR 2016-22 | AVR 2023 | AVR 2024-26 | AVR amb | BIST 2016-22 | BIST 2023 | BIST 2024-26 | BIST amb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| taban | A | 8686 | 2042 | 4153 | 5700 | 4496 | 815 | 1743 | 2291 | 2588 | 381 | 1759 | 2118 |
| PP | A | 4195 | 1008 | 2033 | 2802 | 2175 | 367 | 803 | 1034 | 2265 | 303 | 1442 | 1726 |
| PPq | A | 2171 | 469 | 1027 | 1379 | 1124 | 221 | 441 | 582 | 645 | 21 | 167 | 185 |
| PPb | A | 1511 | 402 | 727 | 1052 | 851 | 132 | 293 | 385 | 1136 | 121 | 753 | 867 |
| PPt | A | 4489 | 1032 | 2120 | 2896 | 2319 | 447 | 939 | 1255 | 315 | 78 | 316 | 391 |
| AY | A | 1813 | 624 | 834 | 1283 | 823 | 180 | 280 | 385 | 465 | 112 | 536 | 645 |
| AYK | A | 2172 | 660 | 1154 | 1624 | 1124 | 200 | 409 | 548 | 647 | 149 | 532 | 671 |
| AY5 | A | 912 | 338 | 412 | 642 | 423 | 81 | 123 | 174 | 204 | 54 | 259 | 312 |
| AY2 | A | 352 | 135 | 160 | 256 | 172 | 36 | 42 | 66 | 70 | 23 | 111 | 134 |
| AYKK | A | 499 | 242 | 294 | 459 | 185 | 43 | 65 | 92 | 142 | 47 | 172 | 217 |
| AYC | A | 2172 | 490 | 998 | 1351 | 1124 | 173 | 371 | 490 | 647 | 157 | 651 | 803 |
| AYT | A | 2172 | 633 | 944 | 1411 | 1124 | 250 | 411 | 576 | 647 | 103 | 460 | 562 |
| AYt | A | 56 | 10 | 66 | 76 | 51 | 4 | 33 | 37 | 23 | 0 | 2 | 2 |
| DT | A | 1753 | 394 | 748 | 1022 | 1046 | 194 | 453 | 576 | 396 | 7 | 187 | 193 |
| DT05 | A | 1301 | 281 | 543 | 750 | 787 | 146 | 335 | 425 | 244 | 8 | 128 | 135 |
| DT2 | A | 2651 | 602 | 1120 | 1553 | 1623 | 308 | 656 | 859 | 563 | 12 | 250 | 261 |
| DTt | A | 6933 | 1648 | 3405 | 4678 | 3450 | 621 | 1290 | 1715 | 2192 | 374 | 1572 | 1925 |
| RV | A | 587 | 94 | 225 | 295 | 585 | 81 | 201 | 253 | 1091 | 82 | 469 | 544 |
| RVq | A | 2172 | 465 | 1012 | 1369 | 1124 | 214 | 456 | 588 | 647 | 18 | 172 | 185 |
| RVt | A | 2587 | 573 | 1169 | 1587 | 1322 | 249 | 563 | 740 | 144 | 36 | 132 | 167 |
| NR7 | A | 1164 | 233 | 532 | 708 | 612 | 100 | 212 | 289 | 381 | 69 | 248 | 313 |
| NR7a | A | 207 | 67 | 121 | 171 | 110 | 19 | 34 | 47 | 120 | 34 | 97 | 130 |
| NR7y | A | 957 | 166 | 411 | 537 | 502 | 81 | 178 | 242 | 261 | 35 | 151 | 183 |
| IDNR4 | A | 461 | 121 | 255 | 347 | 297 | 51 | 99 | 137 | 183 | 24 | 118 | 140 |
| NR7t | A | 7522 | 1809 | 3621 | 4992 | 3884 | 715 | 1531 | 2002 | 2207 | 312 | 1511 | 1805 |
| VCP | A | 24 | 8 | 12 | 18 | 12 | 2 | 2 | 3 | 9 | 1 | 13 | 14 |
| VCP5 | A | 29 | 8 | 14 | 20 | 15 | 2 | 2 | 3 | 9 | 1 | 13 | 14 |
| VCPt | A | 8662 | 2034 | 4141 | 5682 | 4484 | 813 | 1741 | 2288 | 2579 | 380 | 1746 | 2104 |
| W1 | A | 1978 | 381 | 935 | 1188 | 1060 | 196 | 325 | 439 | 572 | 69 | 364 | 430 |
| W1t | A | 1978 | 459 | 1040 | 1431 | 1060 | 188 | 441 | 594 | 572 | 72 | 416 | 484 |
| W2 | A | 1752 | 447 | 815 | 1119 | 973 | 179 | 419 | 527 | 469 | 32 | 236 | 265 |
| W2t | A | 1752 | 421 | 890 | 1230 | 973 | 191 | 350 | 496 | 469 | 22 | 336 | 356 |
| W2D | A | 1752 | 375 | 814 | 1109 | 973 | 197 | 357 | 509 | 469 | 18 | 302 | 319 |
| W2Dt | A | 1752 | 489 | 837 | 1172 | 973 | 176 | 431 | 554 | 469 | 24 | 236 | 258 |
| taban | B | 346 | 146 | 232 | 355 | 89 | 20 | 55 | 72 | 238 | 81 | 297 | 373 |
| PP | B | 150 | 68 | 95 | 153 | 42 | 9 | 30 | 38 | 208 | 66 | 249 | 311 |
| PPq | B | 72 | 27 | 43 | 69 | 15 | 6 | 16 | 21 | 75 | 8 | 35 | 41 |
| PPb | B | 49 | 26 | 35 | 57 | 20 | 2 | 12 | 14 | 109 | 18 | 95 | 113 |
| PPt | B | 196 | 78 | 137 | 202 | 47 | 11 | 25 | 34 | 28 | 15 | 48 | 62 |
| AY | B | 74 | 61 | 57 | 111 | 10 | 7 | 12 | 16 | 77 | 15 | 119 | 133 |
| AYK | B | 157 | 80 | 123 | 189 | 41 | 13 | 23 | 34 | 101 | 53 | 143 | 192 |
| AY5 | B | 32 | 35 | 27 | 56 | 4 | 3 | 5 | 7 | 35 | 4 | 58 | 62 |
| AY2 | B | 12 | 16 | 11 | 25 | 1 | 3 | 3 | 5 | 12 | 2 | 28 | 30 |
| AYKK | B | 31 | 36 | 37 | 70 | 2 | 5 | 6 | 9 | 36 | 11 | 50 | 60 |
| AYC | B | 105 | 32 | 67 | 90 | 25 | 4 | 13 | 16 | 53 | 26 | 83 | 109 |
| AYT | B | 54 | 18 | 39 | 54 | 17 | 1 | 8 | 9 | 49 | 16 | 60 | 76 |
| AYt | B | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| DT | B | 24 | 8 | 14 | 21 | 6 | 0 | 5 | 5 | 33 | 0 | 16 | 16 |
| DT05 | B | 19 | 4 | 9 | 13 | 4 | 0 | 2 | 2 | 19 | 0 | 10 | 10 |
| DT2 | B | 33 | 11 | 22 | 31 | 10 | 0 | 7 | 7 | 45 | 0 | 21 | 21 |
| DTt | B | 322 | 138 | 218 | 334 | 83 | 20 | 50 | 67 | 205 | 81 | 281 | 357 |
| RV | B | 18 | 4 | 7 | 11 | 12 | 2 | 3 | 5 | 112 | 16 | 99 | 112 |
| RVq | B | 59 | 30 | 40 | 68 | 19 | 4 | 15 | 19 | 71 | 5 | 40 | 43 |
| RVt | B | 123 | 34 | 68 | 96 | 33 | 9 | 20 | 27 | 15 | 5 | 21 | 26 |
| NR7 | B | 48 | 20 | 44 | 61 | 13 | 2 | 4 | 6 | 44 | 13 | 41 | 54 |
| NR7a | B | 20 | 14 | 27 | 39 | 7 | 1 | 2 | 3 | 24 | 12 | 27 | 39 |
| NR7y | B | 28 | 6 | 17 | 22 | 6 | 1 | 2 | 3 | 20 | 1 | 14 | 15 |
| IDNR4 | B | 15 | 10 | 13 | 23 | 2 | 0 | 2 | 2 | 22 | 3 | 17 | 20 |
| NR7t | B | 298 | 126 | 188 | 294 | 76 | 18 | 51 | 66 | 194 | 68 | 256 | 319 |
| VCP | B | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| VCP5 | B | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| VCPt | B | 346 | 146 | 231 | 354 | 89 | 20 | 55 | 72 | 238 | 81 | 297 | 373 |
| W1 | B | 53 | 15 | 44 | 52 | 15 | 2 | 4 | 5 | 56 | 13 | 73 | 85 |
| W1t | B | 84 | 46 | 54 | 95 | 31 | 9 | 18 | 27 | 54 | 19 | 54 | 71 |
| W2 | B | 37 | 11 | 12 | 20 | 4 | 4 | 6 | 9 | 34 | 5 | 17 | 21 |
| W2t | B | 78 | 40 | 63 | 98 | 22 | 6 | 20 | 26 | 49 | 6 | 82 | 88 |
| W2D | B | 51 | 31 | 39 | 66 | 15 | 5 | 17 | 22 | 43 | 3 | 65 | 68 |
| W2Dt | B | 51 | 13 | 23 | 33 | 8 | 4 | 6 | 9 | 48 | 6 | 20 | 25 |

## 4. ÖZELLİK DENETİMİ (getirisiz)

| Pazar | olay | prefix tuttu | kesit hisse-gün | takvim bar | NaN (F43..F64) |
|---|---|---|---|---|---|
| ABD | 14881 | 25 | 3331251 | 2830 | F43 4, F44 4, F45 4, F51 9988, F53 139, F62 2758 |
| AVR | 7054 | 25 | 1602780 | 2994 | F43 4, F44 4, F45 4, F51 4150, F53 109, F62 1365 |
| BIST | 4728 | 25 | 1194101 | 2819 | F43 9, F44 9, F45 9, F51 3832, F53 4, F62 415 |

### Mekanik ilişki (K1; Spearman, bütün Y1, getirisiz)

| Özellik | F3 mum boyu | F10 bölge net | F13 kırılım hacmi | F15 konum |
|---|---|---|---|---|
| F44 | -0.15 | -0.14 | +0.82 | -0.04 |
| F46 | +0.30 | -0.07 | +0.24 | +0.03 |
| F47 | -0.04 | +0.19 | +0.01 | +0.25 |
| F48 | -0.17 | -0.16 | +0.42 | -0.03 |
| F49 | +0.05 | -0.15 | +0.15 | -0.10 |
| F51 | -0.06 | -0.03 | +0.03 | -0.01 |
| F52 | -0.15 | -0.18 | +0.95 | -0.03 |
| F54 | -0.13 | -0.17 | +0.87 | -0.01 |
| F55 | -0.02 | -0.26 | +0.29 | -0.35 |
| F62 | +0.13 | -0.03 | -0.07 | +0.10 |
| F64 | -0.11 | -0.17 | +0.92 | -0.00 |

Uygulama yorumları (ölçümden önce): (1) t barı (sinyal günü) girdidir; DEVİR 1'den farklı olarak PP / kutu / RVOL / NR7_t t'yi okur, NR7 karar hücresi t-1 barıdır; (2) PP'de yukarı gün ama 10 günde düşüş günü yoksa NaN (süzgeç tutmaz); (3) DÜZ TAVAN'da ikiden az onaylı pivot = 0 (düz tavan yok), 6 bar onay gecikmesi yüzünden son 6 barın tepeleri sayılmaz (küçük 3-5 günlük yapıyı geç yakalar; karnede not); (4) VCP daralmaları penceredeki en yüksek tepeden başlar, son açık salınım girmez; (5) RV kesit evreni bugün işlem gören hisseler (K7), ilk-20 pazar büyüklüğüne göre farklı seçicilik (ABD ~1.400, AVR / BIST ~580 hisse); (6) KATKI+ dört hücre + bootstrap + L3O + tabaka şartları birlikte; ters yön hücresi yalnız bilgi.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | olay ve eş olay_Y1.csv.gz'den (aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hat / hedef / 15 bar takip geometrisi); MARJ kol tabanına göre (Y1 / Y9) aynı pazar x hücre x ambargo; K1 TABAKALI koşulur: her ana aday MARJ'ı F10, F15, F7 tercil tabakalarında (sınırlar devir2_esik.json, 2016-22 getirisiz) ölçülür, n >= 30 tabakada MARJ <= 0 -> SORGULA; mekanik ilişki Spearman tablosu (F3 / F10 / F13 / F15) ön kayıtta; RV kesit sırası aynı gün eşlerinden bağımsız değil (eşler aynı günün hisseleri) -> raporda |
| K2 | geleceğe bakma | EVET | F43-F64 yalnız [.., t] barları (t = sinyal günü kapanışı, giriş t+1 açılış); pivot onayı j+6 <= t; ZigZag yalnız onaylı pivot; yh_d2_bar dizileri t+1'de keser; yh_devir2_ozellik_yaz pazar başına 25 rastgele olayda veri t'de kesilince aynı değer (DURUR) ve panel R (kesit) = olay R (DURUR); kesit evreni o günün geçerli barları (evren_bas sonrası); eşikler getirisiz, ön kayıtta mühürlü |
| K3 | geçerli bar | EVET | geçerli bar süzgeci _yh_hazir (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); pencereler geçerli bar sayımıyla; kesit evreninde o gün geçerli barı olmayan hisse yok; hacim 0 bar veri dizisinde yok |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (olay_Y1); n = bağımsız olay (h5 ve es_h5 olan); süzgeç yalnız seçer; FARK ortalama, P olay / P eş ayrı |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (olay_Y1 E0); yeni simülasyon yok, satırlar mühürlü olay_Y1 (Y1_OLAY_SHA) |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip (Yahoo düzeltilmiş); yeni ölçüler oran / pay / sıra / ikili (birimsiz); AVR yerel para ama hepsi hisse içi oran; RV kesit sırası oranla (birimden bağımsız) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batanlar yok): P olay ve P eş yukarı yanlı, FARK'ta kısmen götürür; kesit evreni de bugünün listesi (geçmiş günlerin batan hisseleri sırada yok) -> RV ilk-20 sırası yanlı; rapora yazılır |
| K8 | örneklem ve dönem | EVET | hücre n < 30 SORGULA (ölçülemedi); ABD ve AVR ayrı, eğitim + sınama dört hücre aynı yön şartı; 20 karar satırı BH yok -> şans notu; ABD / AVR 2023-26 önceki turlarda görüldü (bakılmış) -> KATKI+ en fazla EMARE düzeyi; küçük n bulgu değil |
| K9 | ön kayıt | EVET | DEVIR_2_ON_KAYIT.md: YH_ESIK_D2_SHA, YH_ESIK / 6 / 7 / D1 sha, kod / özellik d2 / eşik json d2 / d1 özellik / d1 eşik json / olay_Y1 / olay_Y9 sha + getirisiz huni; yh_d2_kapi hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i ('DEVİR 2 ön kayıt') koşudan önce; eşik sonuca göre oynanmaz; ikinci koşu DURUR |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları |
| K11 | yeniden üretim | EVET | devir2_sonuc.json + ozellik_Y1_d2.csv.gz + olay_Y1.csv.gz; DEVIR_2_RAPOR.md 'YENİDEN ÜRETİM' iki hücre (AY A ABD sınama, W2 B AVR eğitim) ayrı kodla (_yh_d2_yeniden: düz pandas sorgusu + kendi ambargo hesabı) yeniden üretilir; fark > 1e-12 ise DURUR |
| K12 | ifade | EVET | etiket yalnız karne v2 kuralı (KATKI+ / KATKI− / SORGULA / BİLGİ); 'iz / emare' denmez; FARK yüzde puan; h5 hedef payı (stop'tan önce +%5), getiri değil; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_d2_ / yh_devir2_ / YH_ESIK_D2 / _YH_D2 önekli; DEVİR 1 adları ezilmez); yasak defter dosyalarına, GOZ_ETIKET.py'ye, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat'; PP / RV kapalı konuya dokunur -> raporda onay notu |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm ve süzgeç karnesi |

