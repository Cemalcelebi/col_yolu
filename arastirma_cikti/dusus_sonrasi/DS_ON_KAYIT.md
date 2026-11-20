# DÜŞÜŞ SONRASI — ÖN KAYIT (DS; 25 sınıf I hipotez, 15 bar cetveli; 2026-11-20)

DUSUS_SONRASI v1.0 (2026-11-20): 25 sınıf I hipotez (DS_ELESTIRI bölüm 5), 15 bar cetveli, DS içi eş, karne v3 + BH q 0,10. Kodlayıcı alt ajan (KOL F). Bu dosya koşudan ÖNCE yazıldı ve git'e işlendi ('DS ön kayıt'); ds_kos kapısı aşağıdaki sha'ları, ds_esik.json eşitliğini, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Sınama verisinin SONUCU (h5 / st5 / getiri) bu dosya yazılırken hesaplanmadı: yalnız özellik değerleri, olay sayıları ve eğitim eşikleri (getirisiz).

- DS_ESIK_SHA: `052ac9c4439cf5eaa3679c3d2ae9ba6389021321008d474015a2b7e9af208a9d`
- DS_KOD_SHA: `b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf`
- YH_KOD_SHA: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e`
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9`
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
- OC_ESIK_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d`
- DS_ESIK_JSON_SHA: `80305c746420876283e425d28632f503c695ea00136700b8c03d74bb678ca83d`
- DS_PREFIX_SHA: `da034c7038b512a5aa43e6ee58f0722e57e68cb550510819cac875f065ec682c`
- CERCEVE_SHA: `8a62e354285a529d03dee3de627ad18d01c2834e238c8e58c823cef6b7dc0589`
- ELESTIRI_SHA: `5d40abb075ddb0f20acf205793c6a740e5e29ae63beaedfa40eb58a627dcd4c4`
- SEKTOR_SHA: `f715c532d83cce13c53927a8134442f5f1be60c65322ecc60321f0ad355eef32`
- V_ABD_SHA: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR_SHA: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST_SHA: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- GİRDİ MÜHRÜ: DS_ELESTIRI.md commit `eff87f3b156564fbafd16a27fc60960e3a559860` (2026-11-20T10:33:41+00:00); DS_OLCUM_CERCEVE.md commit `8ea21e58db41339b2757795fadf194360149f2b2` (2026-11-20T10:10:02+00:00)
- ZAMAN (UTC): `2026-11-20 11:24:31 UTC`

## 1. SORU, OLAY, CETVEL, EŞ, HÜCRE (DS_ESIK; çerçeve DS_OLCUM_CERCEVE.md AYNEN)

- OLAY: hisse-gün t (geçerli bar; OC.oc_veri temiz veri): (a) C_t / max(C son 120 geçerli bar) - 1 <= -0,30; (b) F15_t = (C_t - min C) / (max C - min C), son 120 kapanış t dahil, <= 0,25; (c) medyan(C x V x Kur, son 20 bar t dahil) >= 1 mn $ (ABD) / 1 mn EUR (AVR) / 5 mn TL (BIST); (d) ABD C_t >= 2 $; (e) giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla: havuz üyeliği, alt %20 likidite dışı, geçmiş bölünme şüphesi dışı, giriş boşluğu <= 10 gün; tekil_gun = 1); kriz kesiği 31.08.2026 (15 bar ölçülemeyen olay ölçülmez). ANA = aynı hissede ilk DS günü, sonraki >= 15 birleşik takvim günü sonra (BÜTÜN DS günleri eş havuzu).
- AÇILIŞ TEMİZLİĞİ: O < L ya da O > H olan barlarda O = kırp(O, L, H) (bütün pazarlar; sayı huni'de); DS21 penceresinde kırpılmış bar varsa DS21 NaN.
- CETVEL: YAPI_HEDEF YH_ESIK['olcu'] AYNEN (ufuk 15, hedef +%5 / +%10, stop0 = hat x 0,98, kilit / takip stopu); yh_sim ile olay ve eşler; hat = son 20 geçerli bar en düşük Low (t dahil).
- EŞ: aynı giriş günü d, aynı pazar, aynı kova, DS kümesi İÇİ (o gün DS durumunda ve OC havuzunda öteki hisseler), özelliği 0 (NaN değil), 15 barı ölçülebilir; eş stop'u = eş açılışı x (1 - d_olay); en az 3 eş.
- KOVA: kova = ATRP tercili (ATRP_t = ort TR [t-13, t] / C_t; tercil sınırları pazar başına eğitim DS ANA olaylarından, ds_esik.json) x OC likidite üçlüsü (H[d] % 3; giriş günü kesiti).
- BİLGİ EŞLERİ: DS dışı eş = aynı gün, aynı kova, havuzda, DS durumunda OLMAYAN hisseler (bilgi); aynı gün aynı OC kovası (bilgi).
- DÖNEM: eğitim ['2016-01-01', '2022-12-31'], sınama ['2023-01-01', '2026-08-31']; giriş tarihine göre; sınama girişi >= panel takviminde (son eğitim ANA girişi + 60 bar) (ds_esik.json 'ambargo'). Ambargo (sınama ilk izinli giriş): ABD 2023-03-29, AVR 2023-03-24, BIST 2023-03-30.
- GÜÇ: yh_d3_guc: hücre tabanından (bütün DS ANA olayları, h5 - es_h5_hepsi; es_h5_hepsi = özellik ayrımı olmadan DS içi eş ortalaması) n olay yerine koymadan R kez; güç = Phi(delta / sigma - z); karar hücrelerinden birinde < 0,80 -> ÖLÇÜLEMEDİ.
- p: ay kümeli işaret permütasyonu: ay toplamı s_m = sum(h5 - es_h5); T = sum s_m / sum n_m; T* = sum e_m s_m / sum n_m, e_m = +-1; tek yönlü '+': p = (1 + #{T* >= T}) / (R + 1); '-': T* <= T; iki yönlü (yön '?' ya da iki=True): |T*| >= |T|.
- BH: YH._yh_bh, 25 p (DS_ELESTIRI bölüm 5 listesi, ANA kollar), q 0,10; p_DS = max(p ABD sınama, p AVR sınama) (kesişim-birleşim; iki pazar şartı); hücre n < 30 -> p = 1.
- ETİKET: karne v3 (YH.yh_d3_etiket): karar hücreleri ABD eğitim / sınama, AVR eğitim / sınama; ÖLÇÜLEMEDİ = bir hücrede n < 30 ya da güç < 0,80; KATKI+ = her hücrede FARK > 0 VE boot %95 alt > 0 VE leave-3-out FARK > 0 VE st5 olay <= eş VE ATRP şartı (her karar pazarı x hücre x ATRP tercilinde FARK sonlu ve > 0); KATKI− = her hücrede FARK < 0 VE boot üst < 0; değilse SORGULA. ÇELİŞKİLİ (KATKI'dan önce): bir karar pazarında eğitim ve sınama boot aralıkları sıfırın ZIT taraflarında ya da ABD sınama ile AVR sınama zıt tarafta. SON ETİKET: KATKI+ / KATKI− yalnız BH (q 0,10, önceden yazılı yönlü p) geçerse; geçmezse 'SORGULA (BH)'. BIST ve sınıf II BİLGİ.
- YENİDEN ÜRETİM (önceden seçildi): [['DS01', 'ABD', 'sinama'], ['DS09', 'AVR', 'egitim']] + 50 rastgele olayın h5'i bağımsız döngüyle.
- KARAR PAZARLARI ABD ve AVR; BIST BİLGİ. Sınıf II (ABD-olay) BİLGİ, BH dışı.

## 2. HİPOTEZ TABLOSU (BH listesi, m = 25, DS_ELESTIRI bölüm 5 sırası; ANA kol)

| sıra | DS | hipotez | tanım (t'de bilinir) | yön | p yönü | SABİT eşik | kaynak |
|---|---|---|---|---|---|---|---|
| 1 | DS01 | son 10 günde sona doğru hızlanan düşüş (içbükey yol) | KONV10_t = (M - ort(C_t-9..t)) / M, M = (C_t-9 + C_t) / 2; 1 = KONV10 <= eğitim alt beşte bir sınırı (q20) | + | iki yönlü | KONV10_q20 (eğitim) | Gulen-Woeppel JFQA (10 gün beşli, t 7,31) |
| 2 | DS04 | tek gün büyük düşüş sonrası sıçrama fazı | son barlarda r_s = C_s / C_s-1 - 1 <= -0,15 ve t - s in [2, 23] (geçerli bar) | + | iki yönlü | -%15; [2, 23] (kaynak) | Bulkowski dead-cat; Cox-Peterson JF 1994; Guo 2024 (İDDİA) |
| 3 | DS02 | düşük göreli devirli kaybeden | DEVIR_t = ort(V_t-20..t) / medyan(V_t-251..t); 1 = DEVIR <= eğitim alt onda (q10) | + | iki yönlü | DEVIR_q10 (eğitim) | Medhat-Schmeling RFS 2022; Lee-Swaminathan JF 2000 |
| 4 | DS03 | sektörden (AVR / BIST: evrenden) bağımsız son ay düşüşü | ART21_t = r21(hisse) - ort r21(sektör eşit ağırlık, sektor_ABD.csv, >= 5 hisse; yoksa evren); 1 = ART21 <= eğitim q10 | + | tek yönlü + | ART21_q10 (eğitim) | Da-Liu-Schaumburg MS 2014 |
| 5 | DS08 | Weinstein evre 4 (SMA150 düşüyor, fiyat altında) | EGIM = SMA150_t / SMA150_t-20 - 1; 1 = EGIM < 0 VE C_t < SMA150_t | - | tek yönlü - | işaret (kaynak) | Weinstein; Bulkowski Stages (evre 4 alım n 127) |
| 6 | DS05 | satış doruğu barı (geniş aralık + hacim + dipten uzak kapanış) | s in [t-59, t]: C_s < C_s-1 VE (H-L)_s / ATR20_s-1 >= q VE V_s >= 2 x SMA20(V)_s-1 VE CLV_s >= m | + | tek yönlü + | 2 x SMA20 (kaynak); q = ARALIK eğitim q75, m = CLV eğitim medyanı (t günü değerleri) | Wyckoff; Huddart MS 2009 |
| 7 | DS06 | Turtle Soup dip süpürme + kapanışla geri alma | L_t < m20 = min(L_t-20..t-1), m20'nin yaşı >= 4 bar, C_t >= m20, (H-L)_t <= 3 x ATR14_t-1 | + | tek yönlü + | 20 / 4 / 3 (kaynak) | Connors-Raschke 1996 |
| 8 | DS11 | kapanış 7 günün en düşüğü (Double 7 / H2) | C_t <= min(C_t-6..t) | ? | iki yönlü | 7 gün (kaynak) | Connors; KAZANANLAR H2 |
| 9 | DS09 | RSI(2) aşırı satım | RSI2_t <= 5 (Wilder, alfa 1/2) | + | iki yönlü | 5 (kaynak) | Connors / ChartSchool |
| 10 | DS14 | son alçalan onaylı tepenin kapanışla aşılması (CHoCH) | son iki onaylı 6/6 tepe LH1 > LH2 (onay p + 6 <= t) VE C_t-1 <= LH2 < C_t | + | tek yönlü + | işaret; pivot 6/6 | DeMark / Wyckoff / smc (İDDİA) |
| 11 | DS15 | busted aşağı kırılım (S6 tabanı) | son S6 bölgesi s'de KIRILDI (S6 kuralı C_s < dip x (1 - kirTol)); min(L_s..t) >= 0,90 x kutu_alt; C_t > kutu_ust ilk kez | + | iki yönlü | %10 (kaynak) | Bulkowski Busted |
| 12 | DS16 | Wyckoff ikinci test (DS05 doruğuna düşük hacim + dar aralıkla dönüş) | son DS05 doruk barı s, u* = argmin L[s+5..t]: |L_u/L_s - 1| <= e VE V_u/V_s < q1 VE (H-L)_u/(H-L)_s < q2; doruk yoksa 0 | + | tek yönlü + | e, q1, q2 = eğitim medyanları | Wyckoff ChartSchool |
| 13 | DS18 | evren endeksine göre göreli güç eğimi yukarı | RS = C / E (evren eşit ağırlık); SMA22(RS)_t-1 > SMA22(RS)_t-2 | + | iki yönlü | işaret (Bulkowski) | Bulkowski RS |
| 14 | DS21 | düşüşün çoğu gece (boşluk) olmuş | GECE_PAY = sum ln(O_i/C_i-1) / sum ln(C_i/C_i-1), i in [t-19, t], payda < 0; 1 = >= eğitim q75 (açılışı temizlenmiş bar penceredeyse NaN) | - | tek yönlü - | GECE_q75 (eğitim) | Miwa (QuantPedia); Lou-Polk-Skouras |
| 15 | DS22 | düşüşteki büyük aşağı günün kapanışla doldurulması | i in [t-59, t-1]: r_i <= -2 x std20(r)_i-1; C_t >= C_i-1 ilk kez (C_i..t-1 < C_i-1) | + | tek yönlü + | 2 sigma (kaynak) | tastylive |
| 16 | DS13 | TD Sequential setup 9 | C_i < C_i-4 art arda tam 9 bar, 9. bar = t (kesişim şartı yok) | + | tek yönlü + | 9 (kaynak) | DeMark (MarketInOut) |
| 17 | DS12 | Elder Impulse kırmızıdan çıkış | KIRMIZI_i = EMA13_i < EMA13_i-1 VE HIST_i < HIST_i-1 (MACD 12,26,9); KIRMIZI_t-1 VE değil KIRMIZI_t | + | tek yönlü + | ikili (kaynak) | Elder (ChartSchool) |
| 18 | DS19 | Bollinger %b W dip | son iki onaylı 6/6 dip d1 < d2: %b_d1 <= 0 VE %b_d2 > 0 VE d2 - d1 in [Q1, Q3] VE L_d2 <= L_d1 x (1 + tol); BB(20,2) | + | tek yönlü + | Q1 / Q3 = eğitim dip arası bar çeyrekleri; tol = eğitim medyan |L_d2/L_d1 - 1| | bollingerbands.com |
| 19 | DS20 | alt bantta yürüme | YURU = sayı(C_i < Alt_i), i in [t-9, t], BB(20,2); 1 = YURU >= eğitim q75 | - | tek yönlü - | YURU_q75 (eğitim) | Bollinger kural 7-8 |
| 20 | DS17 | piyasa aşağı günlerinde direnç | DIRENC = ort(r_i - r_m,i | r_m,i < 0), i in [t-39, t], r_m evren eşit ağırlık; 1 = >= eğitim q75 | + | tek yönlü + | DIRENC_q75 (eğitim) | Wyckoff alım testi 7 |
| 21 | DS07 | smash day dönüşü | C_t-1 < L_t-2 VE L_t-1 < min(L_t-9..t-2) VE H_t > H_t-1 | + | tek yönlü + | 8 gün (kaynak) | Larry Williams |
| 22 | DS28 | 252 gün tepeden en az %60 derin | C_t / max(C son 252 bar) - 1 <= -0,60 | ? | iki yönlü | -%60 (kaynak) | Brandes; Mauboussin (ikincil) |
| 23 | DS10 | DV2 < 10 | DV2 = yüzdelik sıra(SMA2(C / ((H+L)/2) - 1), son 252 bar) x 100 < 10 | + | iki yönlü | 10; 252 (kaynak) | Quantitativo (İDDİA) |
| 24 | DS23 | yukarıda +%5..+%10 bandında dolmamış 2 sigma aşağı gün | i in [t-119, t]: r_i <= -2 x std20_i-1, C_i..t < C_i-1 (dolmamış), C_i-1 / C_t - 1 in (0,05; 0,10] | + | tek yönlü + | 2 sigma; bant | tastylive; smc (İDDİA) |
| 25 | DS25 | dipten çapalı AVWAP testi | AVWAP = son 120 bar en düşük L barından t'ye sum TP*V / sum V; C_t > AVWAP VE min(L_t-2..t) <= AVWAP x (1 + e) | + | tek yönlü + | e = eğitim medyanı (C_t > AVWAP olaylarında min(L_t-2..t)/AVWAP - 1) | MMT / takeprofitapp (İDDİA) |

## 3. EĞİTİM EŞİKLERİ (2016-22 DS ANA olaylarından, getirisiz; SAYI; ds_esik.json)

| eşik | ABD | AVR | BIST |
|---|---|---|---|
| KONV10_q20 | -0.0403262 | -0.0335988 | -0.0326263 |
| DEVIR_q10 | 0.902197 | 0.966679 | 0.458333 |
| ART21_q10 | -0.232071 | -0.200896 | -0.239993 |
| DIRENC_q75 | -0.00203303 | -0.00255324 | -0.000552394 |
| YURU_q75 | 2 | 2 | 2 |
| GECE_q75 | 0.620281 | 0.422853 | 0.239963 |
| DS05_q | 1.26766 | 1.40057 | 1.27781 |
| DS05_m | -0.433552 | -0.45098 | -0.509089 |
| DS19_Q1 | 12 | 13 | 13 |
| DS19_Q3 | 25 | 26 | 25 |
| DS19_tol | 0.0858676 | 0.07844 | 0.0822785 |
| DS25_e | -0.0187934 | -0.0143082 | -0.0134934 |
| ATRP_t1 | 0.047276 | 0.0395066 | 0.0383663 |
| ATRP_t2 | 0.0692647 | 0.0558236 | 0.055598 |
| n_egitim_ana | 14061 | 4562 | 2947 |
| DS16_e | 0.151306 | 0.144413 | 0.160047 |
| DS16_q1 | 0.49312 | 0.60018 | 0.333903 |
| DS16_q2 | 0.583104 | 0.634909 | 0.515 |
| n_DS16 | 4902 | 1720 | 759 |

## 4. HUNİ (getirisiz)

- **ABD**: hisse 1411; DS günü 355057; havuzdan geçen DS günü 261466 (düşen: likidite alt %20 85424, geçmiş bölünme 7978, havuz dışı 93412, giriş yok / geç 179 / 0); ANA olay 24899; dönem ambargo 494, dis 241, egitim 14061, sinama 10103; açılış kırpılan bar 0.
- **AVR**: hisse 580; DS günü 75067; havuzdan geçen DS günü 68534 (düşen: likidite alt %20 5249, geçmiş bölünme 1246, havuz dışı 6522, giriş yok / geç 11 / 0); ANA olay 6806; dönem ambargo 57, dis 259, egitim 4562, sinama 1928; açılış kırpılan bar 2932.
- **BIST**: hisse 581; DS günü 114105; havuzdan geçen DS günü 102191 (düşen: likidite alt %20 11033, geçmiş bölünme 549, havuz dışı 11747, giriş yok / geç 163 / 4); ANA olay 9494; dönem ambargo 554, dis 18, egitim 2947, sinama 5975; açılış kırpılan bar 1.

Hipotez başına ANA olay (tutan / tutmayan / NaN; 'tutan_es3' = en az 3 özelliği tutmayan DS içi adayı olan tutan olay; 15 bar ölçülebilirliği bakılmadan):

| DS | ABD egitim | ABD sinama | AVR egitim | AVR sinama | BIST egitim | BIST sinama |
|---|---|---|---|---|---|---|
| DS01 | 2813 / 11248 / 0 (es3 2490) | 1719 / 8384 / 0 (es3 1582) | 913 / 3649 / 0 (es3 601) | 287 / 1641 / 0 (es3 128) | 590 / 2357 / 0 (es3 342) | 881 / 5094 / 0 (es3 721) |
| DS04 | 1604 / 12457 / 0 (es3 1437) | 1115 / 8988 / 0 (es3 1016) | 319 / 4243 / 0 (es3 210) | 183 / 1745 / 0 (es3 80) | 159 / 2788 / 0 (es3 93) | 81 / 5894 / 0 (es3 65) |
| DS02 | 1253 / 11268 / 1540 (es3 1179) | 848 / 9213 / 42 (es3 832) | 449 / 4037 / 76 (es3 284) | 134 / 1791 / 3 (es3 86) | 283 / 2541 / 123 (es3 252) | 192 / 5416 / 367 (es3 185) |
| DS03 | 1407 / 12654 / 0 (es3 1120) | 1590 / 8513 / 0 (es3 1395) | 457 / 4105 / 0 (es3 254) | 307 / 1621 / 0 (es3 122) | 295 / 2652 / 0 (es3 109) | 442 / 5533 / 0 (es3 318) |
| DS08 | 11096 / 2321 / 644 (es3 2780) | 7834 / 2256 / 13 (es3 3399) | 4092 / 441 / 29 (es3 284) | 1737 / 191 / 0 (es3 17) | 1701 / 1184 / 62 (es3 516) | 3449 / 2380 / 146 (es3 1781) |
| DS05 | 5721 / 8340 / 0 (es3 4841) | 4316 / 5787 / 0 (es3 4054) | 2058 / 2504 / 0 (es3 1216) | 909 / 1019 / 0 (es3 313) | 876 / 2071 / 0 (es3 536) | 1332 / 4643 / 0 (es3 1149) |
| DS06 | 351 / 13710 / 0 (es3 331) | 246 / 9857 / 0 (es3 243) | 97 / 4465 / 0 (es3 75) | 38 / 1890 / 0 (es3 29) | 54 / 2893 / 0 (es3 42) | 112 / 5863 / 0 (es3 108) |
| DS11 | 7715 / 6346 / 0 (es3 5609) | 5298 / 4805 / 0 (es3 4627) | 2618 / 1944 / 0 (es3 1093) | 1027 / 901 / 0 (es3 320) | 1624 / 1323 / 0 (es3 602) | 2969 / 3006 / 0 (es3 1891) |
| DS09 | 3450 / 10611 / 0 (es3 3068) | 2352 / 7751 / 0 (es3 2255) | 1322 / 3240 / 0 (es3 899) | 528 / 1400 / 0 (es3 266) | 890 / 2057 / 0 (es3 484) | 1397 / 4578 / 0 (es3 1199) |
| DS14 | 74 / 13987 / 0 (es3 71) | 40 / 10063 / 0 (es3 39) | 17 / 4545 / 0 (es3 10) | 13 / 1915 / 0 (es3 6) | 17 / 2930 / 0 (es3 12) | 34 / 5941 / 0 (es3 33) |
| DS15 | 1 / 14060 / 0 (es3 1) | 0 / 10103 / 0 (es3 0) | 0 / 4562 / 0 (es3 0) | 1 / 1927 / 0 (es3 0) | 1 / 2946 / 0 (es3 1) | 3 / 5972 / 0 (es3 3) |
| DS16 | 1206 / 12855 / 0 (es3 1070) | 1301 / 8802 / 0 (es3 1259) | 460 / 4102 / 0 (es3 255) | 339 / 1589 / 0 (es3 188) | 134 / 2813 / 0 (es3 96) | 237 / 5738 / 0 (es3 216) |
| DS18 | 2889 / 11172 / 0 (es3 2646) | 1909 / 8194 / 0 (es3 1830) | 997 / 3565 / 0 (es3 742) | 335 / 1593 / 0 (es3 164) | 622 / 2325 / 0 (es3 466) | 1179 / 4796 / 0 (es3 1070) |
| DS21 | 2878 / 8634 / 2549 (es3 2527) | 1970 / 6180 / 1953 (es3 1762) | 952 / 2855 / 755 (es3 571) | 504 / 1043 / 381 (es3 147) | 573 / 1719 / 655 (es3 311) | 703 / 3950 / 1322 (es3 548) |
| DS22 | 117 / 13944 / 0 (es3 109) | 101 / 10002 / 0 (es3 100) | 28 / 4534 / 0 (es3 21) | 23 / 1905 / 0 (es3 19) | 31 / 2916 / 0 (es3 22) | 62 / 5913 / 0 (es3 60) |
| DS13 | 332 / 13729 / 0 (es3 306) | 227 / 9876 / 0 (es3 226) | 144 / 4418 / 0 (es3 104) | 48 / 1880 / 0 (es3 34) | 81 / 2866 / 0 (es3 56) | 187 / 5788 / 0 (es3 179) |
| DS12 | 1038 / 13023 / 0 (es3 958) | 759 / 9344 / 0 (es3 737) | 325 / 4237 / 0 (es3 225) | 132 / 1796 / 0 (es3 69) | 199 / 2748 / 0 (es3 146) | 453 / 5522 / 0 (es3 413) |
| DS19 | 1014 / 13047 / 0 (es3 938) | 741 / 9362 / 0 (es3 726) | 317 / 4245 / 0 (es3 208) | 141 / 1787 / 0 (es3 79) | 245 / 2702 / 0 (es3 199) | 263 / 5712 / 0 (es3 244) |
| DS20 | 4019 / 10042 / 0 (es3 3376) | 2486 / 7617 / 0 (es3 2308) | 1530 / 3032 / 0 (es3 803) | 566 / 1362 / 0 (es3 247) | 778 / 2169 / 0 (es3 469) | 1281 / 4694 / 0 (es3 1111) |
| DS17 | 3516 / 10545 / 0 (es3 3123) | 2523 / 7580 / 0 (es3 2402) | 1141 / 3421 / 0 (es3 781) | 396 / 1532 / 0 (es3 203) | 737 / 2210 / 0 (es3 485) | 1370 / 4605 / 0 (es3 1213) |
| DS07 | 416 / 13645 / 0 (es3 400) | 329 / 9774 / 0 (es3 320) | 130 / 4432 / 0 (es3 103) | 63 / 1865 / 0 (es3 38) | 55 / 2892 / 0 (es3 41) | 160 / 5815 / 0 (es3 150) |
| DS28 | 2769 / 9752 / 1540 (es3 2244) | 1821 / 8240 / 42 (es3 1623) | 504 / 3982 / 76 (es3 256) | 199 / 1726 / 3 (es3 78) | 472 / 2352 / 123 (es3 252) | 715 / 4893 / 367 (es3 601) |
| DS10 | 3815 / 8703 / 1543 (es3 3245) | 2538 / 7523 / 42 (es3 2422) | 1644 / 2840 / 78 (es3 973) | 516 / 1409 / 3 (es3 249) | 733 / 2090 / 124 (es3 405) | 1004 / 4602 / 369 (es3 844) |
| DS23 | 2520 / 11541 / 0 (es3 2298) | 1920 / 8183 / 0 (es3 1876) | 1182 / 3380 / 0 (es3 801) | 489 / 1439 / 0 (es3 277) | 597 / 2350 / 0 (es3 419) | 1189 / 4786 / 0 (es3 1076) |
| DS25 | 2666 / 11395 / 0 (es3 2327) | 1851 / 8252 / 0 (es3 1748) | 890 / 3672 / 0 (es3 544) | 358 / 1570 / 0 (es3 161) | 393 / 2554 / 0 (es3 286) | 988 / 4987 / 0 (es3 900) |

## 5. SINIF II (ABD-olay, sec_ozet; BİLGİ tablosu, BH dışı)

- DS47 (+): 5.02 sonrası ilk 2.02 tepkisi negatif (t = tepkiden sonraki ilk gün); 8-K 5.02 başvurusu tarih(t) - 180 takvim günü içinde; sonraki ilk 2.02 bilgi barı i0; tepki = r(C_i0-2 -> C_i0+1) - r_evren < 0; t = i0 + 2
- DS48 (-): Form 144 [t-20, t-1]; bilgi barı (başvuru + 1 işlem günü) in [t-20, t-1] NOT: 2023 öncesi kâğıt başvuru kapsamı eksik (DS_ELESTIRI HATA 10): eğitim hücresi yorumlanmaz
- DS49 (+): yeni pasif %5 ortak (SC 13G / SCHEDULE 13G, değişikliksiz) [t-60, t]; bilgi barı in [t-60, t]; form 'SC 13G' ya da 'SCHEDULE 13G' (iki ad birlikte)
- DS50 (?): 8-K 2.03 yeni borç [t-20, t]; bilgi barı in [t-20, t]
- DS51 (-): 8-K 2.04 borç hızlandırma [t-60, t]; bilgi barı in [t-60, t]
- DS52 (-): 8-K 1.02 sözleşme feshi [t-20, t]; bilgi barı in [t-20, t]
- DS53 (-): 8-K 3.03 ortak hakları değişimi [t-60, t]; bilgi barı in [t-60, t]
- DS44: VERİ YOK (Yahoo not günlüğü / bilanço takvimi k67: /tmp, kalıcı değil)
- DS45: VERİ YOK (k67 not düşürme günlüğü)
- DS46: bu koşuda kapsam dışı (Form 4 k30; ana model kararı: sınıf II yalnız sec_ozet)

K10 sec_ozet ham satır gösterimi (elle):
- CIK 1750 (AIR): form '8-K', tarih 2026-10-26, madde '1.01,2.03,7.01,9.01'
- CIK 1800 (ABT): form 'SCHEDULE 13G', tarih 2026-04-29, madde ''
- CIK 2098 (ACU): form '8-K', tarih 2026-07-21, madde '1.01,1.02,2.03,9.01'

## 6. PREFIX (K2; ds_prefix.json)

- ABD: 30 olay, bozuk 0 (40 ham özellik, rtol 1e-09).
- AVR: 30 olay, bozuk 0 (40 ham özellik, rtol 1e-09).
- BIST: 30 olay, bozuk 0 (40 ham özellik, rtol 1e-09).

## 7. ÖNCEDEN YAZILI NOTLAR

- DS01 / DS09 / DS10 / DS11 (son günlerin zayıflığı) ve DS05 / DS16 (aynı doruk barı) yüksek ilişkili beklenir: birden fazlası geçerse tek bulgu.
- DS08 / DS20 / DS28: özellik DS olayında sık; tutmayan eş azlığı ÖLÇÜLEMEDİ üretebilir (huni yukarıda).
- DS03 sektör sınıfı bugünkü (sektor_ABD.csv; K2 notu); AVR / BIST evren artığı.
- Etiket KATKI+ olsa bile 'iz' denmez; ileri test (Mart 2027, kriz sonrası veri) gerekir.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü), DS kümesi içi, özelliği tutmayan; eşler olayın stop uzaklığı d ile aynı 15 bar kuralıyla (yh_sim, aynı giriş / çıkış geometrisi); mekanik üstünlük: DS30 / DS31 / DS34 havuzda elendi, DS08 / DS20 / DS28 için tutan / tutmayan sayıları getirisiz huni'de; DS dışı eş ve OC eşi bilgi satırı |
| K2 | geleceğe bakma | EVET | bütün ham özellikler yalnız [.., t] barlarından (pivotlar 6/6 onayı p + 6 <= t); ds_prefix.json pazar başına 30 olayda veri t'de kesilince eşit (DURUR); sınıf II olaylar başvuru günü + 1 işlem günü <= t; eşikler eğitim olaylarından getirisiz; sektör sınıfı bugünkü (DS03 notu); evren endeksi aynı gün getirilerinin ortalaması |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği; açılış H-L dışı bar kırpılır (sayı huni'de, DS21 NaN); 15 bar yalnız geçerli barlarla (yh_sim); sinyal günü geçerli bar |
| K4 | tekilleştirme | EVET | ANA = hisse başına ilk DS günü, sonraki >= 15 birleşik takvim günü sonra (oc_olay_hazirla sonrası); n = ANA olay; bootstrap / permütasyon birimi giriş ayı; ortalama yanında h5 / getiri medyanı raporda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla d; YH.yh_sim satır 0); açılış stop'un altındaysa olay ölçülmez (sayım) |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur (EUR); geçmiş bölünme şüphesi [d-61, d-1] havuz dışı (DS04 -%15 günleri bölünme hatası olamaz: OC sup_gecmis); AVR açılış temizliği |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST 581; k34 yüklenmez): (+) yönlü özellikler lehine, (−) yönlüler aleyhine yanlı; DS içi eş FARK'ta kısmen götürür; raporda yazılır |
| K8 | örneklem ve dönem | EVET | ABD ve AVR ayrı, eğitim + sınama; n < 30 ÖLÇÜLEMEDİ ve olayları ds_sonuc.json 'kucuk' listesinde; güç < 0,80 ÖLÇÜLEMEDİ; BH q 0,10 m = 25 sabit; aynı aileden (DS01 / DS09 / DS10 / DS11; DS05 / DS16) birden fazla geçen tek bulgu sayılır |
| K9 | ön kayıt | EVET | DS_ON_KAYIT.md: DS_ESIK sha, ds_esik.json (eğitim eşikleri SAYI), ds_prefix.json, kod sha'ları, girdi sha'ları, getirisiz huni; ds_kos kapısı sha + git (işlenmiş ve değişmemiş) + ik_kontrol_kapisi denetler, eşikleri yeniden hesaplayıp json ile eşitler; ön kayıt commit'i koşudan önce; ikinci koşu DURUR |
| K10 | ayrıştırma | EVET | sınıf I yalnız OHLCV (UYGULANMAZ); sınıf II sec_ozet: form adları 'SC 13G' + 'SCHEDULE 13G' birlikte, 8-K madde kodu virgülle ayrılmış alan, başvuru günü + 1 işlem günü; ham sec_ozet'ten 3 satır ön kayıtta elle gösterildi |
| K11 | yeniden üretim | EVET | ds_olay.csv.gz satır dosyası; DS_RAPOR.md YENİDEN ÜRETİM iki hücre (DS01 ABD sınama, DS09 AVR eğitim) düz pandas ile + 50 rastgele olayın h5'i bağımsız döngüyle yeniden simüle; fark > 1e-12 DURUR |
| K12 | ifade | EVET | etiket yalnız karne v3 + BH kuralıyla; 'iz / emare / anlamlı' yazılmaz; FARK yüzde puan h5 (stop'tan önce +%5 payı), getiri değil; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_ds; ds_ / DS_ önekli adlar dışında ezme DURUR; test_dusus_sonrasi); yasak defter dosyalarına ve YAPI_HEDEF.py'ye dokunulmadı (git diff); e-posta / anahtar taraması (YH._yh_yaz); dış servis yok; kod değişti -> 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |
