# MACD_UYUM — ÖN KAYIT (K47 MACD pozitif uyumsuzluk, tek başına ve DİPTE) — 2026-11-24 16:27:13 UTC

Bu dosya ölçümden (R15 / h5 / getiri) ÖNCE yazıldı ve git'e işlendi; aşağıdaki sayılar yalnız olay SAYILARI, güç beklentisi (CETVEL2 v2.2 eğrisi, getirisiz) ve yh_s10_bar eşitlik denetimidir. `python MACD_UYUM.py kos` mu_kapi ile bu dosyanın git kaydını, değişmemişliğini, sha'larını, olay tablosu sha'sını, IZ_KARNE.ik_kontrol_kapisi'ni ve KASA kapısını denetler; biri tutmazsa DURUR. İkinci koşu DURUR.

KASA: açık kesik 2022-12-31 (KASA_DURUM mühür f674b4ee291c2f35, açılan blok []); veri /tmp/veri -> /tmp/kasa/acik; açık kısım V_*.pkl sha'ları arastirma_cikti/kasa/KASA_MANIFEST.json (mühür 4a7fbad49def764c) acik_sha256 ile AYNI (bu oturumda islenmis-veri fce5d94'ten aynı kesikle yeniden mühürlendi; manifest repo dışında). En geç tarih: V_ABD.pkl 2022-12-30; V_AVR.pkl 2022-12-30; V_BIST.pkl 2022-12-30

Kod commit (MACD_UYUM.py son git kaydı): `9656b02f2ed67298a2e6d576b2d6ea5628f068b4 2026-11-24T19:26:03+03:00`

- MU_ESIK_SHA: `d53e8cf81ba49dd5f58bce7bb2d0d8f8f8a25d7367a2a5cab6e47f0b08d6eb21`
- YH_ESIK8_SHA: `d28e8257274a85e0301d262d5808e51460fb944f4e5dd56a5f7ade762b03b09c`
- C2_ESIK22_SHA: `df651ccbcd312f2e260befcbf5fa84bb192598c051467d081dc874b77889c71a`
- C2_ESIK_SHA: `c44d76dd5da1d42c358f5bc1a9db3a34ee826c2c142d3113239248023637ff03`
- MU_KOD_SHA: `0adfa43c2b3bc63e504a9a1b3a3166941e7357e4c38d536db677489135988fb6`
- KOD:YAPI_HEDEF.py: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e`
- KOD:CETVEL2.py: `2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6`
- KOD:ORTAK_CETVEL.py: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
- KOD:POZITIF_KONTROL.py: `896a70ed704442531a0a4d747dff23fe241ac623b4c3a192114395baa5876fd6`
- KOD:DUSUS_SONRASI.py: `b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf`
- KOD:KASA.py: `3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b`
- KOD:FON_IZI.py: `ce23940da7eb38a5f3a0fd0b14716869dd2d309aaa0a334785f373e365149afb`
- KOD:SIKISMA_YENIDEN.py: `ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae`
- KOD:IZ_KARNE.py: `9579349c40f7745eaf082e46b95be75748a8fa223282ead6aedcc52f3cf33a4d`
- C2_ESIK22_JSON_SHA: `f45e68ed49de307188ba35f894ee94f81035e357b59d6ce46f5e94fb0da74335`
- C2_GUC22_JSON_SHA: `95528165cb5ce2752a727a3f4d796f7cae48cb54848d0d0269b9b4afe4f4a13b`
- V_ABD_SHA: `e96a5728320e59ef51b340aa092e227a9f42ee457a41ae4ce460df7afece238b`
- V_AVR_SHA: `0c47dd662dcf90f49b3bcfac7f46d32519e655f1914737dec8738165564907c0`
- V_BIST_SHA: `d6e9466e3c4577d5f0b194f0c4df0d4a4e9227e0b72079561f3704eb8f66c529`
- OLAY_TABLO_SHA (içerik): `297e7672bac0598e3304243a43832b9680e6d40d0dfea7f956bcaddbd4238899`
- OLAY_DOSYA_SHA (uyum_olay.csv.gz): `7b6720b895b0fa899f3e7a005025e2e85383e0ea03228d9e466dfb2e3fe9a29d`
- HUNI_JSON_SHA (uyum_huni.json): `4553d08813249f4504b0147962807ff20671637e80797090075b3d904c99c52f`
- ESITLIK_JSON_SHA (uyum_esitlik.json): `97f06cadce72e4b1a02eedd524eb019740d9ffa3ade41a3d3d7df6408d863aa8`

## 1. TANIMLAR ve EŞİKLER (MU_ESIK; iş tanımından AYNEN, sha yukarıda)

- surum: MU-1.0
- is: K47 MACD POZİTİF UYUMSUZLUK, TEK BAŞINA VE DİPTE (Cemal 24 Kas 2026: 'test et, bu uyumsuzluğun getirisi ne'); örnek DGXX (hüküm yok)
- gecerli_bar: YH._yh_hazir (= GOZ_ETIKET.ge_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0 ve sonlu, kriz kesiği); göstergeler kapanıştan, YALNIZ t'ye kadar olan geçerli barlarla
- s10: MACD, dipler, F65, F66, F68: YAPI_HEDEF 8. tur AYNEN (YH_ESIK8 sha ön kayıtta; yh_s10_bar; ON_KAYIT_8 uygulama yorumları 1-6). Dipler [t-60, t-1], k in [t-55, t-6]; sol komşular katı küçük, sağ komşular eşit izinli; L1 = L2'den en az 8 bar önceki en yakın dip. Vektör sürüm mu_s10_vektor (pandas ewm adjust=False özyinelemesinin aynısı); pazar başına >= 100 barda yh_s10_bar ile birebir
- dipte: {"geri": 120, "dip_tol": 0.01, "tepe_pay": 0.8, "tanim": "DİPTE(L2) <=> L2 - 120 >= 0 VE Low(L2) <= min(Low[L2-120 .. L2-1]) x 1,01 VE Close(L2) <= 0,80 x max(High[L2-120 .. L2]) (geçerli bar sırası); L2 - 120 seri başından önceyse olay yok"}
- olay: {"taze_azami": 20, "ara": 15, "tanim": "t günü yh_s10_bar kuralıyla bulunan L2(t) için şartların İLK kez tuttuğu gün; t <= L2 + 20 (değilse olay yok); her L2 en çok bir olay (hipotez başına); aynı hissede iki olay arası >= 15 geçerli bar (t sırasıyla ilki kalır)"}
- stop_carpan: 0.98
- stop: STOP = Low(L2) x 0,98 (8. turdaki 'hat x 0,98' mantığı); giriş açılışı stopun altında ya da eşitse olay STOP sayılır (sayısı yazılır)
- giris: t+1 açılış = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla; CETVEL2 E0)
- hipotez: {"U1": "ANA: Ş10 (F65 VE F66) VE F68 (MACD > sinyal) VE DİPTE, olay günü kuralıyla", "U0": "KONTROL (K1 mekanik etki): F65 VE DİPTE VE NOT F66 (s66 = 0) VE F68, aynı olay günü kuralıyla (dipte aynı çift dip, MACD uyumsuzluğu yok)", "U1b": "BİLGİ: Ş10 VE F68, DİPTE şartı yok, olay günü kuralıyla", "U2": "BİLGİ: RSI(14, Wilder) uyumsuzluğu: F65 VE RSI(L2) > RSI(L1) VE RSI(L1) < 30 VE DİPTE; t = L2 + 6 (L1 / F65 t'de)", "U3": "BİLGİ: U1 VE U2, aynı L2'de (olay günü U1'in günü)", "U1d": "BİLGİ (yalnız ABD, DGXX benzeri): U1 VE olay günü ATR%14 o günün en oynak %20'sinde VE Close(t) < 5 $ VE Close(L2) <= 0,50 x max(High[L2-120 .. L2])"}
- u2: {"rsi_n": 14, "rsi_esik": 30.0, "t_kayma": 6, "rsi": "FON_IZI._fi_k38b_rsi (ewm alpha 1/14, adjust False, min_periods 14; repodaki hazır uygulama), serinin başından t'ye kadar geçerli kapanışlar (nedensel)"}
- u1d: {"pazar": "ABD", "atrp_gun": 14, "atrp_ust_pay": 0.2, "fiyat_ust": 5.0, "tepe_pay": 0.5, "atrp": "POZITIF_KONTROL.pk_seri ATRP (CETVEL2 kovası ile aynı: ort TR 14 / C); 'en oynak %20' <=> ATRP(t) >= o gün geçerli barı ve sonlu ATRP'si olan bütün ABD açık evren hisselerinin ATRP %80 niceli (numpy quantile, doğrusal)"}
- olcu: {"ana": "CETVEL2 v2.2 R15: C2.c2_olc22(ufuk 15, donem = d1619 / d2022, plasebo ayrı çağrıyla, bilgi yok); hipotez başına AYRI çağrı (eş dışı küme = aynı hipotezin o günkü olayları); R15 = 15. geçerli bar kapanışı / E0 - 1 (stop yok)", "ufuk": 15, "bilgi_ufuk": 30, "donem": {"d1619": ["2016-01-01", "2019-12-31"], "d2022": ["2020-01-01", "2022-12-31"]}, "karar_pazar": ["ABD", "AVR"], "bilgi_pazar": ["BIST"], "tekil_gun": 15, "r30": "BİLGİ: c2_olc22 ufuk 30 (CETVEL2 v2.2 tanımı AYNEN: tekil 30, plasebo yok); yalnız n / FARK [boot]", "getiri": "r15 = R15 (t+1 açılış -> 15. geçerli bar kapanışı); olay ve eş (olay başına eş ortalaması) için ortalama ve medyan; olay - eş farkı (= FARK). Takip stoplu getiri: YH.yh_getiri (repoda hazır, yh_olay_olc 'getiri'; yalnız olay; bilgi)"}
- hucre_kurali: (3) HÜCRE TUTAR (beklenen yön +; − ise işaretler ters): n >= 30; ortalama FARK > 0 ve ay kümeli bootstrap (B 2000) alt ucu > 0; ortalama SIRA > 0,50 ve onun da boot alt ucu > 0,50; L3O (en iyi 3 ay çıkınca) FARK > 0; PLASEBO KAPISI (hücre, 200 tohum rastgele etiket: |ortalama FARK| < 0,5 puan ve yön başına tutar payı <= %7). [KART_TUR2_ON_KAYIT.md bölüm 1, ANA MODEL KARARI (3), AYNEN] + GÜÇ: 'Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural)' ve 'ÖLÇÜLEMEDİ <=> bir karar hücresi GÜÇLÜ değil; GÜÇLÜ(c) = n >= 30 VE güç >= 0,80' [KART_TUR2_ON_KAYIT.md bölüm 5 ve 8, AYNEN]
- hucre: {"n_min": 30, "sira": 0.5, "sira_boot_alt": 0.5, "guc_esik": 0.8, "sira_boot": {"B": 2000, "tohum": 2471, "alt": 0.025, "ust": 0.975, "yontem": "KART_TUR2.k2_stat ile aynı: giriş ayı kümeleri, multinomial ağırlık, ort SIRA = W @ ay toplamı / W @ ay sayısı"}, "plasebo": {"fark_mutlak": 0.005, "tutar_pay": 0.07, "tohum_sayi": 200}, "hukum": "ÖLÇÜLEMEDİ <=> n < 30 ya da güç < 0,80 (cetvel2_guc_v2.2.json pazar x d1619 / d2022 x H 15, delta +0,02); TUTAR <=> güç yeterli VE FARK > 0 VE FARK boot %95 alt > 0 VE SIRA > 0,50 VE SIRA boot %95 alt > 0,50 VE L3O > 0 VE plasebo kapısı geçer; TUTMADI <=> güç yeterli ama TUTAR değil (nedeni yazılır)"}
- karar_kurali: AÇIK VERİDE TUTTU <=> 4 karar hücresinin (ABD / AVR x 2016-19 / 2020-22) hepsinde U1 R15 hükmü TUTAR VE (U1 - U0) R15 farkı 4 hücrenin hepsinde > 0. Bu durumda sonraki adım yalnız öneri olarak yazılır: KASA 2023-24 kör sınaması (Cemal kararı). TUTMADI <=> gücü yeterli hücrelerde tutmuyor (CETVEL2 kuralı). ÖLÇÜLEMEDİ <=> güç yetersiz. Yön hücreden hücreye değişiyorsa ÇELİŞKİLİ. Bilgi varyantlarında hüküm yok. Aile içi BH ile q < 0,10 olanlar 'bilgi: dikkat' diye yazılır. Hayatta kalma (K7): evren yalnız bugün işlem görenlerse bu raporda yazılır; dipteki olaylarda sonuç YUKARI yanlıdır.
- karar_islem: sıra: (1) TUTTU (yukarıdaki); (2) ÇELİŞKİLİ <=> bir karar hücresinde U1 FARK boot %95 aralığı tümüyle > 0 VE bir başkasında tümüyle < 0 (CETVEL2 c2_etiket ÇELİŞKİLİ ölçütü, dört hücreye); (3) TUTMADI <=> gücü yeterli (n >= 30 VE güç >= 0,80) bir karar hücresinde U1 hükmü TUTMADI, ya da dört hücrede U1 TUTAR iken U0'ı ölçülebilir (n >= 30) bir hücrede U1 - U0 <= 0; (4) ÖLÇÜLEMEDİ <=> geri kalan (gücü yeterli hücreler tutuyor ama en az bir karar hücresinde güç yetersiz ya da U0 ölçülemedi)
- ikincil: {"tanim": "YAPI_HEDEF 1. tur 15 bar cetveli AYNEN: OC.oc_olay_hazirla (tekil 15 = ana ölçüyle aynı olay kümesi) -> YH.yh_olay_olc (eş: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d = 1 - stop0 / E0, aynı hedef / takip / 15 bar; taban; plasebo aynı hisse rastgele gün) -> YH.yh_konum_es_olc (F15 = panel F15[d, j] = t değeri) -> YH.yh_hucre / yh_hucre_konum; h5 = 15 geçerli barda kapanış +%5 stop'tan önce, h10 = +%10, stop payı st5; KAT5 [%95] ay kümeli", "deneme_no": {"U1": 901, "U0": 902, "U1b": 903, "U2": 904, "U3": 905, "U1d": 906}, "giris_stop_alti": "E0 <= stop0 (yh_olay_olc 'giris_stop_otesi'): KAT5 / konum KAT / plasebo 1. tur gibi DIŞINDA; olay payı tablosunda STOP sayılır (h5 = 0, h10 = 0, stop = 1) ve sayısı yazılır; R15'te stop yok (olay ölçülür)"}
- fark_u1_u0: {"B": 2000, "tohum": 2474, "tanim": "FARK(U1) - FARK(U0) aynı pazar x hücre; boot %95 iki grubun giriş ayları bağımsız yeniden örneklenir (bilgi; karar yalnız nokta değerle)"}
- bh: {"q": 0.1, "aile": "U1b, U2, U3, U1d x karar pazarları (ABD, AVR; U1d yalnız ABD) x d1619 / d2022, n >= 30; p = c2_hucre ay kümeli işaret permütasyonu (tek yönlü +); BH geçen = 'bilgi: dikkat'"}
- esitlik: {"n_rastgele": 50, "n_aday": 50, "n_olay": 50, "tohum": 2472, "tanim": "pazar başına 150 bar: 50 rastgele bar, 50 rastgele aday gün (L1 / L2 var VE ham F65), 50 rastgele olay günü (herhangi hipotez); 10 çıktı (F65, F66, F66m, F66h, F67, F68, tL2, s65, s66, S10) mu_s10_vektor = yh_s10_bar BİREBİR (tam eşit; NaN = NaN); değilse DURUR"}
- prefix: {"n": 30, "tohum": 2473, "tanim": "koşuda pazar başına 30 rastgele olay (satır dosyası): hissenin verisi t'de kesilir, olay taraması kesik seriyle yeniden yapılır; aynı (hipotez, t) olayı aynı L1 / L2 ve aynı bayraklarla (F65-F68, s65, s66, S10, DİPTE, RSI, ATRP) çıkmalı; değilse DURUR"}
- k34: BİLGİ: batanlar dahil ABD (k34_yahoo.pkl açık kısım 2020-10-01 .. 2022-12-30) yalnız d2022 hücresinin bir bölümünü kapsar; ana koşu bittikten sonra süre kalırsa koşulur (U1 / U0 R15, bilgi); koşulmazsa raporda 'uygulanmadı' yazılır

### Ş10 tanımı (YH_ESIK8 macd / dip / esik, AYNEN)

- macd: {"hizli": 12, "yavas": 26, "sinyal": 9, "pencere": 250, "isinma": 35, "tanim": "MACD = EMA12(C) - EMA26(C); sinyal = EMA9(MACD); histogram = MACD - sinyal. t için EMA'lar YALNIZ [t-250, t] geçerli barlarıyla (pandas ewm(span, adjust=False): ilk değer tohum); pencerenin ilk 35 barı ısınma (MACD / sinyal NaN). t < 250 ise pencere serinin başından (t-250 yok); ısınma aynı kural"}
- dip: {"pencere": 60, "sol": 5, "sag": 5, "L1_min_ara": 8, "tanim": "salınım dibi k: [t-60, t-1] içinde Low'un 5 sol / 5 sağ yerel minimumu; komşular da pencerede (k in [t-55, t-6]); Low_k < min(Low_k-5..k-1) (sol KATI) VE Low_k <= min(Low_k+1..k+5) (sağ eşit izinli): eşit dizide ilk bar dip olur. L2 = t'ye en yakın dip (L2 <= t-6); L1 = L2 - 8'e kadar (L1 <= L2 - 8) en yakın önceki dip; yoksa Ş10 NaN = tutmaz. t < 60 geçerli bar -> NaN"}
- esik: {"F65_ust": 0.01, "F66_alt_acik": 0.0, "F66m_ust_acik": 0.0, "F68": 1.0, "F65": "s65 = Low(L2) <= Low(L1) x 1,01 (ikili; F65 = Low(L2) / Low(L1) - 1 bilgi sayısı)", "F66": "s66 = MACD(L2) > MACD(L1) VE MACD(L2) < 0 (ikili); F66 = (MACD(L2) - MACD(L1)) / Close(L2); F66m = MACD(L2) / Close(L2)", "F66h": "BİLGİ: (hist(L2) - hist(L1)) / Close(L2) > 0 (histogram sürümü)", "F67": "L2 - L1 (bar)", "F68_tanim": "t barında MACD > sinyal (0 / 1; dönüş teyidi)", "tL2": "t - L2 (bar; bilgi)", "S10": "Ş10 TUTAR <=> s65 VE s66 (F66 > 0 VE F66m < 0); Ş10t (bilgi) = Ş10 VE F68 = 1"}

### Hücre kuralı (KART_TUR2 ön kaydından kopya)

(3) HÜCRE TUTAR (beklenen yön +; − ise işaretler ters): n >= 30; ortalama FARK > 0 ve ay kümeli bootstrap (B 2000) alt ucu > 0; ortalama SIRA > 0,50 ve onun da boot alt ucu > 0,50; L3O (en iyi 3 ay çıkınca) FARK > 0; PLASEBO KAPISI (hücre, 200 tohum rastgele etiket: |ortalama FARK| < 0,5 puan ve yön başına tutar payı <= %7). [KART_TUR2_ON_KAYIT.md bölüm 1, ANA MODEL KARARI (3), AYNEN] + GÜÇ: 'Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural)' ve 'ÖLÇÜLEMEDİ <=> bir karar hücresi GÜÇLÜ değil; GÜÇLÜ(c) = n >= 30 VE güç >= 0,80' [KART_TUR2_ON_KAYIT.md bölüm 5 ve 8, AYNEN]

### Karar kuralı (iş tanımından AYNEN)

AÇIK VERİDE TUTTU <=> 4 karar hücresinin (ABD / AVR x 2016-19 / 2020-22) hepsinde U1 R15 hükmü TUTAR VE (U1 - U0) R15 farkı 4 hücrenin hepsinde > 0. Bu durumda sonraki adım yalnız öneri olarak yazılır: KASA 2023-24 kör sınaması (Cemal kararı). TUTMADI <=> gücü yeterli hücrelerde tutmuyor (CETVEL2 kuralı). ÖLÇÜLEMEDİ <=> güç yetersiz. Yön hücreden hücreye değişiyorsa ÇELİŞKİLİ. Bilgi varyantlarında hüküm yok. Aile içi BH ile q < 0,10 olanlar 'bilgi: dikkat' diye yazılır. Hayatta kalma (K7): evren yalnız bugün işlem görenlerse bu raporda yazılır; dipteki olaylarda sonuç YUKARI yanlıdır.

İşlemsel sıra: sıra: (1) TUTTU (yukarıdaki); (2) ÇELİŞKİLİ <=> bir karar hücresinde U1 FARK boot %95 aralığı tümüyle > 0 VE bir başkasında tümüyle < 0 (CETVEL2 c2_etiket ÇELİŞKİLİ ölçütü, dört hücreye); (3) TUTMADI <=> gücü yeterli (n >= 30 VE güç >= 0,80) bir karar hücresinde U1 hükmü TUTMADI, ya da dört hücrede U1 TUTAR iken U0'ı ölçülebilir (n >= 30) bir hücrede U1 - U0 <= 0; (4) ÖLÇÜLEMEDİ <=> geri kalan (gücü yeterli hücreler tutuyor ama en az bir karar hücresinde güç yetersiz ya da U0 ölçülemedi)

### UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden ÖNCE yazıldı)

- (1) Hücre kuralı KART_TUR2 ön kaydı (3) AYNEN; güç eğrisi CETVEL2 v2.2'nin kendi eğrisi (cetvel2_guc_v2.2.json, pazar x d1619 / d2022 x H 15, delta +0,02, %80): ana ölçü c2_olc22 bütün evren havuzunda, KART_TUR2'nin P2 / +1 puan / d1-d3 eğrisi bu hücrelerle örtüşmüyor. Tek bakış (açık veri): boot %95 (KART_TUR2 %98,33 yalnız KASA üç bakışında).
- (2) Plasebo kapısı CETVEL2.c2_plasebo ile (200 tohum, aynı giriş günü havuzdan rastgele hisse, eş dışı = çekilen küme, iki yön ayrı); GEÇER <=> |ort FARK| < 0,005 VE + yönde TUTAR payı <= %7 VE - yönde TUTAR payı <= %7; tohum TUTAR'ı c2_hucre kuralıyla (SIRA boot şartı yok: KART_TUR2 kuralından katı ya da eşit). tohum_ek c2_olc formülüyle aynı.
- (3) U0 ile U1 aynı L2'de ayrı günlerde olay verebilir (L1 pencereden çıkarsa ya da MACD [t-250, t] tohum etkisiyle s66 günden güne değişirse); her biri kendi tanımıyla kalır; ortak L2 sayısı huni'de.
- (4) 15 bar aralığı hissenin geçerli bar sırasıyla ve hipotez başına; ardından c2_olay OC giriş / havuz (alt %20 likidite, geçmiş bölünme) / tekil (birleşik takvimde 15 işlem günü, giriş günüyle) uygular; düşenler huni'de.
- (5) U3 = 15 bar sonrası U1 olaylarından L2'si U2 şartını (t = L2 + 6'da F65, RSI, DİPTE) tutanlar; U1d = 15 bar sonrası ABD U1 olaylarından olay gününde ATRP / fiyat / tepe şartlarını tutanlar; ikisine 15 bar yeniden uygulanmaz (U1'in alt kümesi).
- (6) Hücre = giriş günü (CETVEL2); huni'nin ön aşamaları t (L2 aşamaları L2 + 6) tarihiyle sayılır; 2015 ve öncesi hücre dışı.
- (7) Karar kuralı işlemsel sırası MU_ESIK['karar_islem']; U1 - U0 yalnız nokta değerle (boot bilgi).
- (8) İkincil cetvelde plasebo tohum deneme no 901-906 (YAPI_HEDEF Y1-Y13c numaralarından ayrı); dönem OC '2016-22'.
- (9) Satır dosyası olay başına bir satır; eş alanları olay başına eş özetidir (es_r15 = eş ortalaması, n_es, es_h5 / es_h10 / es_st5).

## 2. yh_s10_bar EŞİTLİĞİ (getirisiz; mu_s10_vektor = yh_s10_bar, 10 çıktı tam eşit)

- ABD: 150 / 150 bar birebir (tür {'rastgele': 50, 'aday': 50, 'olay': 50}; S10 = 1 olan 47, F68 = 1 olan 105)
- AVR: 150 / 150 bar birebir (tür {'rastgele': 50, 'aday': 50, 'olay': 50}; S10 = 1 olan 44, F68 = 1 olan 87)
- BIST: 150 / 150 bar birebir (tür {'rastgele': 50, 'aday': 50, 'olay': 50}; S10 = 1 olan 54, F68 = 1 olan 107)

## 3. GETİRİSİZ HUNİ (olay sayısı; pazar x hücre)

| Hipotez | Aşama | ABD d1619 | ABD d2022 | AVR d1619 | AVR d2022 | BIST d1619 | BIST d2022 |
|---|---|---|---|---|---|---|---|
| U1 (L2 hunisi) | L2 onaylı dip (L2 + 6 >= 60) | 59621 | 56479 | 32186 | 25785 | 21129 | 17558 |
| U1 (L2 hunisi) | + L1 var (L2 + 6'da) | 59274 | 56156 | 32040 | 25667 | 20947 | 17291 |
| U1 (L2 hunisi) | + F65 (L2 + 6'da) | 30774 | 29237 | 17554 | 13566 | 11263 | 7954 |
| U1 (L2 hunisi) | + DİPTE | 6868 | 9243 | 2685 | 3474 | 3345 | 1828 |
| U1 (L2 hunisi) | + Ş10 bir günde (L2 + 6 .. L2 + 20) | 2343 | 3278 | 969 | 1046 | 1184 | 653 |
| U1 (L2 hunisi) | + F68 aynı gün = U1 ham olay | 2267 | 3183 | 942 | 1013 | 1130 | 627 |
| U1 | olay (ilk gün + 15 bar; t tarihi) | 1946 | 2705 | 807 | 845 | 959 | 517 |
| U1 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 1298 | 1930 | 683 | 681 | 714 | 353 |
| U1 | R15 ölçülebilir | 1298 | 1911 | 683 | 677 | 714 | 353 |
| U1 | eşli (>= 5 eş) = n | 1279 | 1893 | 631 | 636 | 659 | 320 |
| U0 | olay (ilk gün + 15 bar; t tarihi) | 3826 | 5126 | 1414 | 2111 | 1738 | 997 |
| U0 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 2744 | 3929 | 1200 | 1730 | 1343 | 716 |
| U0 | R15 ölçülebilir | 2744 | 3896 | 1200 | 1723 | 1342 | 715 |
| U0 | eşli (>= 5 eş) = n | 2684 | 3872 | 1087 | 1677 | 1244 | 644 |
| U1b | olay (ilk gün + 15 bar; t tarihi) | 4952 | 5309 | 2829 | 2113 | 2088 | 1245 |
| U1b | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 3672 | 3941 | 2272 | 1667 | 1535 | 870 |
| U1b | R15 ölçülebilir | 3672 | 3909 | 2272 | 1659 | 1535 | 870 |
| U1b | eşli (>= 5 eş) = n | 3581 | 3780 | 2074 | 1507 | 1366 | 723 |
| U2 | olay (ilk gün + 15 bar; t tarihi) | 1267 | 1441 | 589 | 587 | 621 | 248 |
| U2 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 893 | 1065 | 506 | 482 | 489 | 196 |
| U2 | R15 ölçülebilir | 893 | 1063 | 506 | 480 | 489 | 196 |
| U2 | eşli (>= 5 eş) = n | 881 | 1057 | 468 | 467 | 452 | 181 |
| U3 | olay (ilk gün + 15 bar; t tarihi) | 838 | 929 | 374 | 372 | 423 | 153 |
| U3 | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 571 | 664 | 323 | 305 | 337 | 121 |
| U3 | R15 ölçülebilir | 571 | 661 | 323 | 303 | 337 | 121 |
| U3 | eşli (>= 5 eş) = n | 563 | 656 | 299 | 290 | 315 | 113 |
| U1d | olay (ilk gün + 15 bar; t tarihi) | 156 | 230 | 0 | 0 | 0 | 0 |
| U1d | OC sonrası (giriş + havuz + tekil; giriş tarihi) | 15 | 51 | 0 | 0 | 0 | 0 |
| U1d | R15 ölçülebilir | 15 | 48 | 0 | 0 | 0 | 0 |
| U1d | eşli (>= 5 eş) = n | 15 | 48 | 0 | 0 | 0 | 0 |

U1 ile U0'ın ortak L2 sayısı (ayrı günlerde ikisi de olay; uygulama yorumu 3): {'ABD': 0, 'AVR': 0, 'BIST': 0}

## 4. GÜÇ BEKLENTİSİ (cetvel2_guc_v2.2.json, H 15, delta +0,02; n = eşli olay sayısı)

| Hipotez | Pazar | Hücre | n | güç | beklenti |
|---|---|---|---|---|---|
| U1 | ABD | d1619 | 1279 | 1.00 | güç yeterli |
| U1 | ABD | d2022 | 1893 | 1.00 | güç yeterli |
| U1 | AVR | d1619 | 631 | 1.00 | güç yeterli |
| U1 | AVR | d2022 | 636 | 1.00 | güç yeterli |
| U1 | BIST | d1619 | 659 | 1.00 | güç yeterli |
| U1 | BIST | d2022 | 320 | 0.90 | güç yeterli |
| U0 | ABD | d1619 | 2684 | 1.00 | güç yeterli |
| U0 | ABD | d2022 | 3872 | 1.00 | güç yeterli |
| U0 | AVR | d1619 | 1087 | 1.00 | güç yeterli |
| U0 | AVR | d2022 | 1677 | 1.00 | güç yeterli |
| U0 | BIST | d1619 | 1244 | 1.00 | güç yeterli |
| U0 | BIST | d2022 | 644 | 1.00 | güç yeterli |
| U1b | ABD | d1619 | 3581 | 1.00 | güç yeterli |
| U1b | ABD | d2022 | 3780 | 1.00 | güç yeterli |
| U1b | AVR | d1619 | 2074 | 1.00 | güç yeterli |
| U1b | AVR | d2022 | 1507 | 1.00 | güç yeterli |
| U1b | BIST | d1619 | 1366 | 1.00 | güç yeterli |
| U1b | BIST | d2022 | 723 | 1.00 | güç yeterli |
| U2 | ABD | d1619 | 881 | 1.00 | güç yeterli |
| U2 | ABD | d2022 | 1057 | 1.00 | güç yeterli |
| U2 | AVR | d1619 | 468 | 1.00 | güç yeterli |
| U2 | AVR | d2022 | 467 | 0.99 | güç yeterli |
| U2 | BIST | d1619 | 452 | 1.00 | güç yeterli |
| U2 | BIST | d2022 | 181 | 0.65 | ÖLÇÜLEMEDİ beklenir |
| U3 | ABD | d1619 | 563 | 0.99 | güç yeterli |
| U3 | ABD | d2022 | 656 | 0.98 | güç yeterli |
| U3 | AVR | d1619 | 299 | 0.98 | güç yeterli |
| U3 | AVR | d2022 | 290 | 0.92 | güç yeterli |
| U3 | BIST | d1619 | 315 | 0.99 | güç yeterli |
| U3 | BIST | d2022 | 113 | 0.44 | ÖLÇÜLEMEDİ beklenir |
| U1d | ABD | d1619 | 15 | 0.09 | ÖLÇÜLEMEDİ beklenir |
| U1d | ABD | d2022 | 48 | 0.16 | ÖLÇÜLEMEDİ beklenir |
| U1d | AVR | d1619 | 0 | 0.00 | ÖLÇÜLEMEDİ beklenir |
| U1d | AVR | d2022 | 0 | 0.00 | ÖLÇÜLEMEDİ beklenir |
| U1d | BIST | d1619 | 0 | 0.00 | ÖLÇÜLEMEDİ beklenir |
| U1d | BIST | d2022 | 0 | 0.00 | ÖLÇÜLEMEDİ beklenir |

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | ANA: CETVEL2 v2.2 konum eşi = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x likidite üçlüsü x F15 çeyreği), bütün evren, aynı geometri (R15 stop'suz, aynı E0, 15 bar), aynı hipotezin o günkü olayları eş dışı, en az 5 eş (C2.c2_es); taban rastgele olay sağlaması = plasebo kapısı 200 tohum (C2.c2_plasebo, iki yön); MEKANİK ÜSTÜNLÜK: U0 kontrolü = dipte aynı çift dip (F65 + DİPTE + F68) ama MACD uyumsuzluğu yok; karar U1 - U0 > 0 ister; İKİNCİL: 1. tur eşi aynı d / hedef / takip |
| K2 | geleceğe bakma | EVET | göstergeler yalnız t'ye kadar (MACD [t-250, t], dipler [t-60, t-1], DİPTE <= L2, RSI nedensel, ATRP kesiti t günü); veri KASA açık kesik 2022-12-31 (kasa_kapisi her komuttan önce; satır dosyası en geç tarihi raporda); koşuda pazar başına 30 olay veri t'de kesilip yeniden taranır (DURUR); kova sınırları / güç eğrisi CETVEL2 v2.2 mühürlü dosyaları (getirisiz) |
| K3 | geçerli bar | EVET | YH._yh_hazir (= ge_hazir: H > L, V > 0, O/H/L/C > 0) bütün göstergeler ve bar sayıları geçerli bar sırasıyla; ölçümde OC.oc_veri_hazirla + DS açılış kırpması (CETVEL2); sinyal günü geçersiz bar olamaz (tarama geçerli barlarda) |
| K4 | tekilleştirme | EVET | her L2 en çok bir olay; hipotez başına aynı hissede >= 15 geçerli bar aralık; c2_olay OC tekil 15 işlem günü; n = bağımsız olay (hipotez başına ayrı c2_olc22 çağrısı); FARK ortalama + medyan, r15 ortalama + medyan; boot / permütasyon birimi giriş ayı |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla d; R15 paydası P['Op'][d, j]); eşler aynı gün açılışı; giriş stop altıysa STOP sayılır (sayısı yazılır) |
| K6 | veri birimi | EVET | V_*.pkl açık kısım tek kip (KASA bayt bayt; sha ön kayıtta); MACD fiyat birimli, F66 Close(L2)'ye bölünür; R15 / ATRP / F15 oran; AVR yerel para (hisse içi oran); U1d 5 $ eşiği yalnız ABD ham kapanış; geçmiş bölünme şüphesi havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD açık 1.361, V_AVR 575, V_BIST 475 sembol): batan / kottan çıkan yok -> dipteki olaylarda sonuç YUKARI yanlı; rapora yazılır; K34 batanlar (2020-10 sonrası) bilgi koşusu süre kalırsa |
| K8 | örneklem ve dönem | EVET | getirisiz huni pazar x dönem (U1, U0, bilgi varyantları) ve güç beklentisi ön kayıtta; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; iki alt dönem (2016-19, 2020-22) ayrı hücre, ABD ve AVR ayrı; bilgi varyantları BH q 0,10; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | UYUM_ON_KAYIT.md: MU_ESIK sha + YH_ESIK8 / C2_ESIK22 / C2_ESIK sha + MACD_UYUM.py ve bağımlı kod sha + kod commit + veri / eşik / güç / olay / huni / eşitlik sha'ları; mu_kapi git kaydı (ön kayıt commit < koşu), değişmemişlik, ik_kontrol_kapisi, kasa_kapisi; ikinci koşu DURUR; eşikler sonuç görülünce değişmez |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / SEC / metin ayrıştırması yok; yalnız OHLCV (V_*.pkl açık kısım) ve mühürlü CETVEL2 v2.2 eşik / güç dosyaları |
| K11 | yeniden üretim | EVET | raporda >= 2 hücre (U1 ABD d1619 ve U0 AVR d2022) satır dosyasından bağımsız düz pandas ile yeniden üretilir (n, ort FARK, ort SIRA, r15 ort; göreli 1e-9); tutmazsa DURUR |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı kuralla (TUTAR / TUTMADI / ÖLÇÜLEMEDİ, TUTTU / TUTMADI / ÖLÇÜLEMEDİ / ÇELİŞKİLİ); bilgi varyantlarında hüküm yok ('bilgi: dikkat' yalnız BH); 'iz / emare' sözü yok; sayı ile yorum ayrı cümle; DGXX için hüküm yok |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mu; mu_ / MU_ önekleri; test); yasak dosyalar (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KASA_DEFTERI.md) ve mevcut modüller değişmedi (git diff); KASA bloğu açılmadı; e-posta / anahtar taraması (YH._yh_yaz); push yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | bu işte alım-satım önerisi yok; ölçüm |
