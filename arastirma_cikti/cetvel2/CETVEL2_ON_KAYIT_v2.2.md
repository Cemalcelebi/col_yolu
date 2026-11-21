# CETVEL2 — ÖN KAYIT v2.2 (2026-11-21 11:41:16 UTC)

CETVEL2 v2.2 (2026-11-21): R_H (H = 15 / 30 / 45) konum eşli fark (bütün evren), iki yönlü plasebo eşiği yön başına, açık veri (KASA <= 2022-12-31); pozitif kontrol v2.2. Bu dosya pozitif kontrol v2.2 koşusundan ÖNCE yazıldı ve git'e işlendi; c2_kapi22 C2_ESIK22 / kod / girdi sha'larını, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Kova sınırları getirisiz havuz dağılımından, güç eğrisi yalnız FARK yayılımından (ortalama kullanılmaz); hiçbir hücre FARK'ı / p'si bu dosya yazılırken hesaplanmadı.

KASA: açık kesik 2022-12-31 (KASA_DURUM.json: mühür 4a7fbad49def764c, açılan blok []); veri klasörü /tmp/veri (= /tmp/kasa/acik); kasa_kapisi V_ABD / V_AVR / V_BIST ve açık DS olay kopyası için geçti.

Kod commit (CETVEL2.py son git kaydı): `1a990f52413ddc5f88bd46320933f042d1deb9b2 2026-11-21T11:40:14+00:00`

- C2_ESIK22_SHA: `df651ccbcd312f2e260befcbf5fa84bb192598c051467d081dc874b77889c71a`
- C2_ESIK_SHA: `c44d76dd5da1d42c358f5bc1a9db3a34ee826c2c142d3113239248023637ff03`
- C2_KOD_SHA: `2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6`
- PK_KOD_SHA: `896a70ed704442531a0a4d747dff23fe241ac623b4c3a192114395baa5876fd6`
- KASA_KOD_SHA: `3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b`
- DS_KOD_SHA: `b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf`
- YH_KOD_SHA: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e`
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
- DS_ESIK_SHA: `052ac9c4439cf5eaa3679c3d2ae9ba6389021321008d474015a2b7e9af208a9d`
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9`
- OC_ESIK_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
- V_ABD_SHA: `e96a5728320e59ef51b340aa092e227a9f42ee457a41ae4ce460df7afece238b`
- V_AVR_SHA: `0c47dd662dcf90f49b3bcfac7f46d32519e655f1914737dec8738165564907c0`
- V_BIST_SHA: `d6e9466e3c4577d5f0b194f0c4df0d4a4e9227e0b72079561f3704eb8f66c529`
- KASA_DURUM_SHA: `6ce17abb8c9c36cff70164deddeeee1b85bdf9d14fe93ee4c9986593146cb95d`
- DS_OLAY_SHA: `66794c356e733c8dc3e037246f62389d089a0f85febd844754fbb52852c8e98d`
- C2_DS_ACIK22_SHA: `f3c0ef2d2c97e23d33f6c1eb0b62f154452eb31f200d6583d1dd037202306691`
- C2_ESIK22_JSON_SHA: `f45e68ed49de307188ba35f894ee94f81035e357b59d6ce46f5e94fb0da74335`
- C2_GUC22_JSON_SHA: `95528165cb5ce2752a727a3f4d796f7cae48cb54848d0d0269b9b4afe4f4a13b`
- C2_PREFIX22_SHA: `10e4bff1dd7ad6a8a230ed45b5b184d958b337b8e331c7b6a365050bc23715fd`
- C2_ESIK21_JSON_SHA: `17833e1ceb278b1598923585e9fb1d8b8c42118d538ce36f898463a3c9352dd7`
- PK_B_OLAY_SHA: `fe2509100f2ac3fac0ade06a224a4b6f8710c7de4d25da777fdcbc34efd57c30`
- C2_B21_SATIR_SHA: `3a396bdbc76980cac352b92cde7ad13a7e2a3efe00d383b76e18dd56a8f94369`

## 1. İŞ TANIMI (KART_TUR1_IS_TANIMI.md bölüm 2, AYNEN)

1. CETVEL2.py eklemesi: ufuk parametresi H ∈ {15, 30, 45} (R_H = H. geçerli bar kapanışı / t+1 açılış − 1; eş ve kova tanımı aynı; tekil = H işlem günü); iki yönlü ('?') hipotezde plasebo kapısı eşiği iki yön için ayrı sayılır (Ç204 hata v); sürüm etiketi '_v2.2'; v2.1 çağrıları aynı sonucu verir (test: c2_b_olay_v2.1 hücrelerinden 3'ü birebir). Kova sınırları açık veriden (2016-22) yeniden sabitlenir, sayı olarak ön kayda.
2. POZİTİF KONTROL v2.2, H = 15 / 30 / 45, yalnız açık veri (2016-2022; H bar 2022-12-30'u aşan olay ölçülmez): (A) yapay iz delta +%1 / +%2 / +%3 / +%5, n 30 / 100 / 300 / 1000, 20 tohum; güç eğrisi hücre x H (cetvel2_guc_v2.2.json); (B) ABD + AVR: 12-1 momentum üst onda (+) ve alt onda (−; 0'ı kesmesi yeter), PEAD üst / alt (ABD; sec_ozet açık veride yoksa 'VERİ YOK' yaz, atla); dönem ikiye bölünür: 2016-19 ve 2020-22; (C) plasebo kapısı 200 tohum, hücre x H.
3. R45 KURALI (önceden yazılı): R45 KARAR ufkuna ancak şu ikisi birlikte tutarsa girer: (i) plasebo kapısı H = 45'te ABD ve AVR hücrelerinde geçer; (ii) momentum üst onda ABD'de iki alt dönemde de R45 FARK boot alt ucu > 0 iken R30'da en az birinde değil (yani 45 mum 30'un göremediğini görüyor). Tutmazsa R45 yalnız BİLGİ sütunu. R15 ve R30 her durumda KARAR ufku.
4. Sıra: 'CETVEL2 v2.2 kod' commit -> CETVEL2_ON_KAYIT_v2.2.md (kontrol tablosu, kova sınırları, R45 kuralı, sha'lar, KASA açık kesik) commit -> koşu -> CETVEL2_POZITIF_KONTROL_v2.2.md commit. Rapor: commit'ler + UTC; A (H başına >= %80 yakalama n / delta), B tablosu (H x dönem: FARK [boot], p), C; R45 kararı (KARAR / BİLGİ + gerekçe); cetvel 'doğru şeye duyarlı mı' H başına; YENİDEN ÜRETİM >= 2 hücre; en geç tarih denetimi; HATA; KONTROL LİSTESİ; ADIM K2 için arayüz.

## 2. v2.2 AYRINTILARI (C2_ESIK22; sha yukarıda; v2.1 C2_ESIK aynen, CETVEL2_ON_KAYIT_v2.1.md)

- surum: C2.2
- taban: C2_ESIK (v2.1; sha ön kayıtta) AYNEN: giriş E0 (t'den sonraki ilk geçerli bar açılışı), eş (aynı giriş günü, aynı pazar, aynı kova = ATRP tercili x likidite üçlüsü x F15 çeyreği, bütün evren, aynı denemenin o günkü olayları ve olayın kendisi dışı, en az 5), FARK / SIRA, boot (ay kümeli, B 2000), perm (ay kümeli işaret, R 10000), hücre TUTAR şartları (n >= 30, güç >= 0,80, FARK yönlü, boot ucu, SIRA, L3O), plasebo (200 tohum, |ort FARK| < 0,005, TUTAR payı <= %7), güç (delta +0,02, %80), BH q 0,10. Yalnız bu sözlüktekiler eklendi / değişti
- ufuklar: [15, 30, 45]
- karar_ufuk: [15, 30]
- bilgi_ufuk: [45]
- r_h: R_H = H. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 2H birleşik takvim satırında H geçerli bar yoksa NaN (H = 15: v2.1 R15 ile aynı, 30 satır); stop YOK. Matris c2_rh; olay satırında 'r15' sütunu R_H'yi taşır, 'ufuk' sütunu H
- pencere_kat: 2
- tekil: aynı hissede olaylar giriş günü sırasıyla birleşik takvimde >= H işlem günü arayla (OC tekil kuralı, tekil_gun = H)
- es: v2.1 ile aynı; eş havuzu ufuk başına (havuzda, kovası var, R_H ölçülebilir)
- donem:
-   d1619: ['2016-01-01', '2019-12-31']
-   d2022: ['2020-01-01', '2022-12-31']
- donem_not: hücre = pazar x dönem (giriş günü); 2023 sonrası KASA'da mühürlü, bu sürümde görülmez
- kova_donem: ['2016-01-01', '2022-12-31']
- kova: v2.1 tanımı (c2_kova_sinir: ATRP tercil ve F15 çeyrek sınırları, havuz hisse-günleri, getirisiz) AÇIK VERİDEN (giriş 2016-22) yeniden sabitlenir; sayılar cetvel2_esik_v2.2.json ve ön kayıtta (v2.1 sayıları yan yana)
- veri:
-   klasor: /tmp/kasa/acik (= /tmp/veri = /tmp/veri2); başka fiyat kaynağı YOK
-   kesik_tarih: 2022-12-31
-   kesik: KASA açık kesik 2022-12-31 (veri sonu 2022-12-30); H. barı veri sonunu aşan olay ölçülmez (R_H NaN, eş havuzu da)
-   kapi: KASA.kasa_kapisi(V_ABD / V_AVR / V_BIST + açık DS olay kopyası) her koşudan önce; KASA_DURUM.json açık kesik = kesik_tarih değilse DURUR; çıktı satır dosyalarının en geç tarihi (KASA.ks_en_gec_tarih) raporda
- plasebo_iki_yon: '?' hipotezde plasebo kapısı: |200 tohum ort FARK| < 0,005 VE + yönde TUTAR payı <= %7 VE - yönde TUTAR payı <= %7 (yön başına ayrı; v2.1'de iki yönün birleşik payı %7 ile karşılaştırılıyordu: H286 / Ç204 hata v). '+' / '-' hipotezde v2.1 ile aynı (hipotezin yönündeki pay)
- guc:
-   hucre: ['d1619', 'd2022', 'acik']
-   tanim: v2.1 tanımı (DS ANA olaylarının konum eşli FARK yayılımı, sigma(n) = exp(a + b ln n), güç = Phi(0,02 / sigma - 1,96), %80) pazar x hücre x H; 'acik' = 2016-22 bütün açık olaylar; c2_olc(ufuk = H) adı eğride olmayan hücrede (ör. KASA blok birikimi) 'acik' eğrisini kullanır. Getiri ortalaması kullanılmaz
- A:
-   pazar: ['ABD', 'AVR', 'BIST']
-   karar_pazar: ['ABD', 'AVR']
-   n: [30, 100, 300, 1000]
-   delta: [0.0, 0.01, 0.02, 0.03, 0.05]
-   tohum_sayi: 20
-   tohum: 2221
-   n_azami_pay: 0.6666666666666666
-   olay: DS ANA olayları (ds_olay.csv.gz; tarih <= açık kesik süzülmüş kopya c2_ds_olay_acik_v2.2.csv.gz; c2_olay tekil H); havuz = hücrede R_H ölçülebilir ve tek başına (deneme = kendisi) >= 5 eşi olan olaylar; her tohum x n x hücre x H havuzdan yerine koymadan n 'tutan' (n > 2/3 havuz ise ölçülmez)
-   taban: DS = seçilen DS olayları; RAST = her seçilen olayın giriş gününde havuzdan rastgele hisse (c2_rastgele; delta 0 = saf plasebo)
-   surukleme: tutan olayın R_H'si (1 + R_H)(1 + delta) - 1 (E0 değişmez); eşler dokunulmaz
-   yakala: hücre TUTAR şartları güç HARİÇ (n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0); güç dahil TUTAR ve p < 0,05 bilgi
- B:
-   pazar: ['ABD', 'AVR']
-   karar_pazar: ['ABD']
-   hipotez:
-     B1U: ['U', '+']
-     B1A: ['A', '-']
-   olay: 12-1 momentum: POZITIF_KONTROL.pk_b_sinyal_mom + pk_b_kur AÇIK VERİDEN yeniden üretilir (ay sonu t, MOM = C(t-21) / C(t-252) - 1, havuz sonrası aynı t kesitinde sıra: üst onda U, alt onda A; ANA = U ya da A, aynı hissede >= 15 bar arayla ilk); c2_olc (ufuk = H, tekil H; eş = bütün evren, aynı gün aynı kova, aynı denemenin o günkü olayları dışı)
-   pead: B2 PEAD: sec_ozet (8-K madde 2.02) olay verisi açık klasörde (/tmp/kasa/acik) YOK -> 'VERİ YOK', atlanır (internete çıkılmaz)
-   b1u_kural: üst onda (+): ABD iki dönemde FARK > 0 ve en az birinde boot alt > 0
-   b1a_kural: alt onda (-): 0'ı kesmesi yeter = ABD iki dönemde boot alt <= 0 (FARK > 0 VE boot alt > 0 = KUSUR)
- C:
-   n: ['tam', 100, 300]
-   tohum: 2231
-   tanim: plasebo kapısı her pazar x dönem x H hücresinde DS ANA olay günleriyle (tam n ve n 100 / 300 rastgele alt küme günleri), 200 tohum, '+' ve '-' payları ayrı; geçti = |ort FARK| < 0,005 VE + payı <= %7 VE - payı <= %7; tanı: havuz, eş, eşsiz, dolu kova
- r45_kurali: R45 KARAR ufkuna ancak şu ikisi birlikte tutarsa girer: (i) plasebo kapısı H = 45'te ABD ve AVR hücrelerinde geçer (C, tam n, d1619 ve d2022, dört hücre); (ii) momentum üst onda (B1U) ABD'de iki alt dönemde de R45 FARK boot alt ucu > 0 iken R30'da en az birinde değil (boot alt <= 0; yani 45 mum 30'un göremediğini görüyor). Tutmazsa R45 yalnız BİLGİ sütunu. R15 ve R30 her durumda KARAR ufku
- sonuc_kurali:
-   tanim: her H için ayrı ('cetvel H mumda doğru şeye duyarlı mı')
-   KUSUR: (i) B1A ABD d1619 ya da d2022 hücresinde FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı (C, tam n) ABD d1619 / d2022 hücrelerinden birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR hücresinde n 100 / 300 / 1000 tohumları birleşik > %10
-   EVET: KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin (ABD / AVR x d1619 / d2022) her birinde bir n'de >= %80 yakalama VE B1U ABD iki dönemde FARK > 0 ve en az birinde boot alt > 0
-   KISMEN: KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)
-   HAYIR: KUSUR var
- yeniden_uretim:
-   hucre: [['B1U', 'ABD', 'd2022', 30], ['B1A', 'ABD', 'd1619', 15], ['B1U', 'AVR', 'd1619', 45]]
-   elle_rh: 20
-   elle_es: 5
-   elle_es_ufuk: 30
-   tohum: 2241
-   tanim: c2_b_olay_v2.2 satır dosyasından üç hücre (yukarıdaki) n / ort FARK / ort SIRA düz pandas; her H için 20 B1 ABD olayının R_H'si ham veriden düz döngüyle; 5 B1U ABD olayının (H = 30) eş ortalaması bütün evren üzerinde düz döngüyle (kova elle)
- regresyon_v21:
-   giris_son: 2022-10-31
-   hucre: [['B1U', 'ABD'], ['B1A', 'ABD'], ['B1U', 'AVR']]
-   tanim: v2.1 çağrısı (ufuk yok, cetvel2_esik_v2.1.json kova sınırları) açık veride, pk_b_olay.csv.gz B1 ANA olaylarıyla (tarih <= açık kesik); giriş <= 2022-10-31 olaylarında giris / kova / E0 / R15 / eş ortalaması / eş sayısı / SIRA / FARK c2_b_olay_v2.1.csv.gz ile BİREBİR (rtol 1e-12); üç eğitim hücresinin bu olay alt kümesinde n / ort FARK / ort SIRA eşit (< 1e-12)

## 3. AÇIK VERİDE (giriş 2016-22) SABİTLENEN KOVA SINIRLARI (sayı; cetvel2_esik_v2.2.json; v2.1 sayıları yan yana)

| pazar | sürüm | ATRP t1 | ATRP t2 | F15 q1 | F15 q2 | F15 q3 | havuz hisse-gün |
|---|---|---|---|---|---|---|---|
| ABD | v2.2 | 0.022713 | 0.036046 | 0.285426 | 0.616974 | 0.876994 | 1513611 |
| ABD | v2.1 | 0.022713 | 0.036047 | 0.285417 | 0.616971 | 0.876991 | 1513661 |
| AVR | v2.2 | 0.019577 | 0.028393 | 0.282243 | 0.610584 | 0.871178 | 753910 |
| AVR | v2.1 | 0.019577 | 0.028393 | 0.282253 | 0.610589 | 0.871181 | 753886 |
| BIST | v2.2 | 0.033376 | 0.048387 | 0.263736 | 0.578475 | 0.848708 | 510403 |
| BIST | v2.1 | 0.033376 | 0.048387 | 0.263721 | 0.578442 | 0.848691 | 510386 |

## 4. GÜÇ EĞRİSİ (cetvel2_guc_v2.2.json; delta +0,02 R_H; sigma(n) = exp(a + b ln n); güç = Phi(delta / sigma - 1,96))

| pazar | hücre | H | N (DS ANA, eşli) | sd (olay) | a | b | n = 30 | 100 | 300 | 1000 | 3000 | güç >= 0,80 için en küçük n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | d1619 | 15 | 4236 | 0,1218 | -1,9808 | -0,5344 | 0,14 | 0,40 | 0,86 | 1,00 | 1,00 | 260 |
| ABD | d1619 | 30 | 2583 | 0,1636 | -1,5747 | -0,5624 | 0,10 | 0,25 | 0,67 | 1,00 | 1,00 | 400 |
| ABD | d1619 | 45 | 2018 | 0,2058 | -1,2950 | -0,5781 | 0,08 | 0,18 | 0,51 | 0,98 | 1,00 | 550 |
| ABD | d2022 | 15 | 9421 | 0,1402 | -1,8074 | -0,5383 | 0,12 | 0,31 | 0,75 | 1,00 | 1,00 | 340 |
| ABD | d2022 | 30 | 5412 | 0,2735 | -1,2530 | -0,5162 | 0,06 | 0,11 | 0,26 | 0,70 | 0,99 | 1280 |
| ABD | d2022 | 45 | 4083 | 0,3474 | -0,9322 | -0,5374 | 0,05 | 0,09 | 0,19 | 0,55 | 0,96 | 1750 |
| ABD | acik | 15 | 13657 | 0,1348 | -1,9122 | -0,5237 | 0,12 | 0,33 | 0,77 | 1,00 | 1,00 | 330 |
| ABD | acik | 30 | 7995 | 0,2435 | -1,0846 | -0,5641 | 0,06 | 0,12 | 0,31 | 0,83 | 1,00 | 940 |
| ABD | acik | 45 | 6101 | 0,3079 | -0,7312 | -0,5860 | 0,05 | 0,09 | 0,22 | 0,66 | 0,99 | 1330 |
| AVR | d1619 | 15 | 1147 | 0,1005 | -2,1502 | -0,5493 | 0,20 | 0,58 | 0,98 | 1,00 | 1,00 | 170 |
| AVR | d1619 | 30 | 729 | 0,1345 | -1,5911 | -0,6115 | 0,12 | 0,37 | 0,89 | 1,00 | 1,00 | 240 |
| AVR | d1619 | 45 | 579 | 0,1571 | -1,6460 | -0,5683 | 0,11 | 0,29 | 0,76 | 1,00 | 1,00 | 340 |
| AVR | d2022 | 15 | 3172 | 0,1124 | -2,0089 | -0,5496 | 0,16 | 0,47 | 0,93 | 1,00 | 1,00 | 210 |
| AVR | d2022 | 30 | 1865 | 0,1425 | -1,7797 | -0,5543 | 0,12 | 0,33 | 0,80 | 1,00 | 1,00 | 310 |
| AVR | d2022 | 45 | 1456 | 0,1668 | -1,6818 | -0,5411 | 0,10 | 0,25 | 0,65 | 0,99 | 1,00 | 420 |
| AVR | acik | 15 | 4319 | 0,1094 | -2,0079 | -0,5497 | 0,16 | 0,47 | 0,93 | 1,00 | 1,00 | 210 |
| AVR | acik | 30 | 2594 | 0,1406 | -1,7157 | -0,5580 | 0,11 | 0,31 | 0,76 | 1,00 | 1,00 | 330 |
| AVR | acik | 45 | 2035 | 0,1642 | -1,4725 | -0,5845 | 0,09 | 0,25 | 0,69 | 1,00 | 1,00 | 380 |
| BIST | d1619 | 15 | 818 | 0,1060 | -1,8373 | -0,6139 | 0,17 | 0,56 | 0,99 | 1,00 | 1,00 | 160 |
| BIST | d1619 | 30 | 499 | 0,1832 | -1,5209 | -0,5618 | 0,09 | 0,23 | 0,62 | 0,99 | 1,00 | 450 |
| BIST | d1619 | 45 | 385 | 0,2385 | -1,2524 | -0,5661 | 0,07 | 0,16 | 0,42 | 0,94 | 1,00 | 680 |
| BIST | d2022 | 15 | 1598 | 0,1193 | -1,8976 | -0,5520 | 0,14 | 0,40 | 0,87 | 1,00 | 1,00 | 250 |
| BIST | d2022 | 30 | 957 | 0,2350 | -1,2018 | -0,5781 | 0,07 | 0,16 | 0,44 | 0,95 | 1,00 | 650 |
| BIST | d2022 | 45 | 785 | 0,3611 | -0,6876 | -0,5986 | 0,05 | 0,09 | 0,23 | 0,70 | 1,00 | 1230 |
| BIST | acik | 15 | 2416 | 0,1150 | -1,7885 | -0,5861 | 0,14 | 0,43 | 0,92 | 1,00 | 1,00 | 220 |
| BIST | acik | 30 | 1456 | 0,2187 | -1,4559 | -0,5208 | 0,07 | 0,15 | 0,39 | 0,88 | 1,00 | 810 |
| BIST | acik | 45 | 1170 | 0,3261 | -1,0422 | -0,5348 | 0,05 | 0,10 | 0,22 | 0,63 | 0,98 | 1470 |

Huni (DS ANA olayları, açık kopya; H başına tekil H): ABD H15: girdi 14061, ölçülen R_H 13845, eşli 13657, son ölçülen giriş 2022-12-09; ABD H30: girdi 14061, ölçülen R_H 8111, eşli 7995, son ölçülen giriş 2022-11-17; ABD H45: girdi 14061, ölçülen R_H 6194, eşli 6101, son ölçülen giriş 2022-10-27; AVR H15: girdi 4562, ölçülen R_H 4518, eşli 4319, son ölçülen giriş 2022-12-09; AVR H30: girdi 4562, ölçülen R_H 2705, eşli 2594, son ölçülen giriş 2022-11-17; AVR H45: girdi 4562, ölçülen R_H 2109, eşli 2035, son ölçülen giriş 2022-10-28; BIST H15: girdi 2947, ölçülen R_H 2942, eşli 2416, son ölçülen giriş 2022-12-12; BIST H30: girdi 2947, ölçülen R_H 1784, eşli 1456, son ölçülen giriş 2022-11-15; BIST H45: girdi 2947, ölçülen R_H 1419, eşli 1170, son ölçülen giriş 2022-10-13

## 5. PREFIX (K2; cetvel2_prefix_v2.2.json)

- ABD: 30 olay, bozuk 0
- AVR: 30 olay, bozuk 0
- BIST: 30 olay, bozuk 0

## 6. R45 KURALI (önceden yazılı)

- R45 KARAR ufkuna ancak şu ikisi birlikte tutarsa girer: (i) plasebo kapısı H = 45'te ABD ve AVR hücrelerinde geçer (C, tam n, d1619 ve d2022, dört hücre); (ii) momentum üst onda (B1U) ABD'de iki alt dönemde de R45 FARK boot alt ucu > 0 iken R30'da en az birinde değil (boot alt <= 0; yani 45 mum 30'un göremediğini görüyor). Tutmazsa R45 yalnız BİLGİ sütunu. R15 ve R30 her durumda KARAR ufku

## 7. PLASEBO KAPISI (v2.2)

- '?' hipotezde plasebo kapısı: |200 tohum ort FARK| < 0,005 VE + yönde TUTAR payı <= %7 VE - yönde TUTAR payı <= %7 (yön başına ayrı; v2.1'de iki yönün birleşik payı %7 ile karşılaştırılıyordu: H286 / Ç204 hata v). '+' / '-' hipotezde v2.1 ile aynı (hipotezin yönündeki pay)

## 8. ÖNCEDEN YAZILI SONUÇ KURALI (pozitif kontrol v2.2; her H ayrı)

- tanim: her H için ayrı ('cetvel H mumda doğru şeye duyarlı mı')
- KUSUR: (i) B1A ABD d1619 ya da d2022 hücresinde FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı (C, tam n) ABD d1619 / d2022 hücrelerinden birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR hücresinde n 100 / 300 / 1000 tohumları birleşik > %10
- EVET: KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin (ABD / AVR x d1619 / d2022) her birinde bir n'de >= %80 yakalama VE B1U ABD iki dönemde FARK > 0 ve en az birinde boot alt > 0
- KISMEN: KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)
- HAYIR: KUSUR var

## 9. B2 PEAD

- B2 PEAD: sec_ozet (8-K madde 2.02) olay verisi açık klasörde (/tmp/kasa/acik) YOK -> 'VERİ YOK', atlanır (internete çıkılmaz)

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü x F15 çeyreği), bütün evren havuzu, aynı geometri (R_H stop'suz, aynı E0, aynı H); aynı denemenin o günkü olayları ve olayın kendisi eş dışı; en az 5 eş (c2_es); taban rastgele olay sağlaması = plasebo kapısı 200 tohum (c2_plasebo; '?' yön başına); mekanik üstünlük yok: stop / hedef yok, R_H olay ve eşte aynı |
| K2 | geleceğe bakma | EVET | kova girdileri giriş gününden ÖNCEKİ son geçerli barda; c2_prefix her pazarda 30 olayda veri t'de kesilince ATRP / F15 / hat aynı (cetvel2_prefix_v2.2.json; tutmazsa DURUR); kova sınırları getirisiz; R_H yalnız giriş açılışından sonrası; veri KASA açık kesik 2022-12-31 (kasa_kapisi her koşudan önce; satır dosyası en geç tarihi raporda); momentum olayları açık veriden yeniden |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması; R_H yalnız geçerli barlar (hissenin kendi takvimi); sinyal günü geçersiz bar ise olay düşer |
| K4 | tekilleştirme | EVET | olaylar aynı hissede >= H işlem günü arayla (tekil_gun = H; örtüşmeyen H bar); n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan FARK raporda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (oc_olay_hazirla d; R_H paydası P['Op'][d, j]); eşler aynı gün açılışı |
| K6 | veri birimi | EVET | V_*.pkl tek kip (açık kısım, KASA bayt bayt bölünmüş); R_H / ATRP / F15 oran (birimsiz); likidite günlük kesit sırası; geçmiş bölünme şüphesi havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST 581); kesikten sonra doğan semboller açık kısımda yok; yanlılık olaya ve eşe aynı; raporda yazılı |
| K8 | örneklem ve dönem | EVET | iki alt dönem (2016-19, 2020-22) ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç eğrisi pazar x dönem x H; A 20 tohum x 4 n x 5 delta x 3 H; plasebo 200 tohum; R45 kuralı ve sonuç kuralı önceden yazılı |
| K9 | ön kayıt | EVET | CETVEL2_ON_KAYIT_v2.2.md: C2_ESIK22 sha, C2_ESIK (v2.1) sha, CETVEL2.py sha + kod commit, kova sınırları (sayı), güç eğrisi, R45 kuralı, DS / YH / OC / PK / KASA sha'ları, veri ve açık DS olay kopyası sha'ları, KASA açık kesik; c2_kapi22 git kaydı + değişmemiş + ik_kontrol_kapisi; sıra kod commit -> ön kayıt commit -> koşu |
| K10 | ayrıştırma | UYGULANMAZ | ham haber / KAP / SEC ayrıştırması yok; DS olayları repo satır dosyasından (açık kesiğe süzülmüş kopya), momentum açık fiyattan; PEAD VERİ YOK |
| K11 | yeniden üretim | EVET | c2_yeniden22: üç hücre satır dosyasından düz pandas; 3 x 20 olayın R_H'si ham veriden düz döngü; 5 olayın eş ortalaması bütün evren düz döngü (kova elle); c2_regresyon21: v2.1 çağrısı satır dosyasıyla birebir; tutmazsa koşu TUTMADI |
| K12 | ifade | EVET | cetvel sınaması; 'iz' iddiası yok; FARK, SIRA, p, yakalama payı ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_c2; test); DS / YH / OC / PK / KASA ve defter dosyalarına dokunulmadı (sha ön kayıtta); e-posta / anahtar taraması (YH._yh_yaz); dış servis / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; cetvel sınaması |
