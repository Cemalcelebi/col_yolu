# KART TURU 1 — ÖN KAYIT (donmuş kod; KASA ile yürüyen ileri test)

Tarih: 2026-11-21 12:42:57 UTC. İş tanımı: arastirma_cikti/kart/KART_TUR1_IS_TANIMI.md (git 2d065a3992359d623f04ae98566afbd38cc7b4d3 2026-11-21T11:18:15+00:00). Kod: KART_TUR1.py (git 480eb31a4c587895e987dfa3e858b207a45f2ff2 2026-11-21T12:26:42+00:00). ADIM K1 kararı: R15 ve R30 KARAR, R45 BİLGİ (CETVEL2_POZITIF_KONTROL_v2.2.md).

KASA_HIPOTEZ: KART_TUR1
KASA_KOD: KART_TUR1.py 334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b
KASA_KOD: CETVEL2.py 2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6
KT_ESIK_SHA: 3080dce505a769dd54be85739442ab45aa4b358def3b7803af79a6d642411310

## 1. Kartlar (tanım ve eşik mevcut modüllerden; yeni eşik yok)

| Kart | Yön | Pazar (karar) | Cümle | Tanım (t'de bilinen) | Eşik | Kaynak (modül.fonksiyon) |
|---|---|---|---|---|---|---|
| KT00 | + | ABD, AVR (kontrol) | KONTROL KARTI: 12-1 momentum üst ondaki hisse (ay sonu, bütün evren) eşlerinden iyi. İz aramaz; kasada cetvelin bilinen etkiyi görüp görmediğini sınar | ay sonu t, MOM = C(t-21) / C(t-252) - 1, OC havuzu sonrası aynı t kesitinde sıra: üst onda U (POZITIF_KONTROL.pk_b_sinyal_mom + pk_b_kur; ANA = U ya da A, aynı hissede >= 15 bar arayla ilk) | üst onda (CETVEL2 v2.2 pozitif kontrol B1U ile AYNI tanım) | CETVEL2.c2_mom22 -> POZITIF_KONTROL.pk_b_sinyal_mom, pk_b_kur |
| KT01 | + | ABD, AVR, BIST | S6 taban kırılımı (YAPI_HEDEF Y1 olayı) eşlerinden iyi | S6 'al' günü (S6_TABAN.s6_taban; hat = kutu_alt (AL) ya da DİP(t-1) (AL_BOLGESIZ), hat > 0) -> OC.oc_olay_hazirla (giriş, havuz, 60 gün tekil) = Y1 OLAYI | S6 parametreleri (S6.s6_prm) + OC_ESIK olay (tekil 60) | YAPI_HEDEF.yh_sinyaller(['Y1']) -> yh_s6_hisse; ORTAK_CETVEL.oc_olay_hazirla |
| KT02 | + | ABD, AVR, BIST | Y1 ∧ Ş1 DİPTE eşlerinden iyi | Y1 olayı VE F15 <= 0,25 VE F17 <= -0,20 | F15_ust 0.25, F17_ust -0.2 (YH_ESIK Y10 esik) | YAPI_HEDEF.yh_s7_sartlar['S1']; F15 / F17 GOZ_ETIKET.ge_ozellik_hisse |
| KT03 | + | ABD, AVR, BIST | Y1 ∧ Ş3 DİP SAVUNULMUŞ eşlerinden iyi | Y1 olayı VE F2 >= -0,01 (son dokunuş dibi / ilk dokunuş dibi - 1; dokunuş yoksa NaN = tutmaz) | F2_min -0.01 | YAPI_HEDEF.yh_s7_sartlar['S3']; F2 GOZ_ETIKET |
| KT04 | + | ABD, AVR, BIST | Y1 ∧ Ş5 ALT FİTİL AZ eşlerinden iyi | Y1 olayı VE F4 <= 0,25 (bölge medyan alt fitil payı) | F4_ust 0.25 | YAPI_HEDEF.yh_s7_sartlar['S5']; F4 GOZ_ETIKET |
| KT05 | + | ABD, AVR, BIST | Y1 ∧ Ş4 KÜÇÜK MUM eşlerinden iyi | Y1 olayı VE F3 <= 0,90 (bölge medyan mum boyu / ATR250) | F3_ust 0.9 | YAPI_HEDEF.yh_s7_sartlar['S4']; F3 GOZ_ETIKET |
| KT06 | + | ABD, AVR, BIST | Y1 ∧ Ş7 GÖVDELİ YAKIN TAVAN KIRILIMI eşlerinden iyi | Y1 olayı VE F22 = C_t / F21 - 1 > 0 VE F22a = O_t / F21 - 1 < 0 VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (F21 = max High[t-15 .. t-1]) | F22 > 0.0, F22a < 0.0, F23_min 0.5 | YAPI_HEDEF.yh_s7_sartlar['S7']; F20-F23 YAPI_HEDEF.yh_s7_ozellik |
| KT07 | + | ABD, AVR, BIST | Cemal'in son dersi: Y1 ∧ Ş1 ∧ Ş3 ∧ Ş5 (dip + savunma + alt fitil az) eşlerinden iyi | Y1 olayı VE Ş1 VE Ş3 VE Ş5 (eşikler KT02 / KT03 / KT04 ile aynı) | KT02 + KT03 + KT04 | YAPI_HEDEF.yh_s7_sartlar['S1'] & ['S3'] & ['S5'] |
| KT08 | - | ABD, AVR, BIST | Düşen bıçak (kural defteri K50 / KAZANANLAR H2): düşüş sonrası dipte, 120 günün tam dibine son 5 günde düşerek gelen hisse eşlerinden kötü | DS ANA olayı (DUSUS_SONRASI: C_t / max C son 120 - 1 <= -0,30, F15 <= 0,25, likidite, ABD C >= 2 $; OC giriş / havuz; ANA 15 bar tekil) VE F15_t <= 0,05 VE r5 = C_t / C_t-5 - 1 <= -0,03 (geçerli barlar; arastirma_cikti/canli/kazananlar.kz_ozellik tanımı) | F15 <= 0,05; r5 <= -0,03 (K50 kaydı, KURAL_DEFTERI_TASLAK.md; KAZANANLAR_2026-10-22 H2) | DUSUS_SONRASI.ds_ozellik_pazar + ds_olay_kur (ana); F15 / r5 = kazananlar.kz_ozellik formülü (testte birebir) |
| KT09 | + | ABD, AVR | −%80 dip kurulumu (Ç173b): tepeden >= %80 düşmüş, son 10 günde yeni dip yapmamış, dipten <= 1,5 kat uzaktaki hisse eşlerinden iyi | D1 C_t / max(C[t-250 .. t-1]) - 1 <= -0,80 (en az 200 bar, veri kırığından sonra) VE D2 min(C[t-9 .. t]) > min(C[t-59 .. t-10]) VE D3 C_t <= 1,50 x min(C[t-59 .. t-10]); aynı hissede ilk kurulum günü, sonraki >= 60 bar sonra | BOFA_IZI.DP_ESIK['kurulum'] (dusus -0,80, tepe 250 / 200, dip 60 / 10, dipten 1,50, ayri 60, kırık ABD / AVR [-0,6667, 2,0]) | BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum (Ç173 'dosya' BOFA_IZI.py diponkayit / dipkos); BIST verisi Yahoo önbelleği (TAVAN_SERISI) kasada yok -> BIST VERİ YOK |
| KT10 | + | ABD | Sektör rüzgârı ABD (Ç181c): alt sektörü piyasadan >= 10 puan iyi giden (rüzgârlı) ve uzun çölde OLMAYAN hisse eşlerinden iyi | RÜZGÂR VE D9 DEĞİL (D9_YENIDEN.d9_satir 'c'): ruz = sepet (alt sektörün öteki >= 4 üyesi, 60 bar getiri eşit ağırlık) - piyasa (taze hisselerin 60 bar getiri medyanı) >= 0,10 VE sepet > 0; D9 uzun çöl değil; durum günleri (sektör ABD 'endustri', sektor_ABD.csv) | D9_YENIDEN.D9_PARAM (RUZ_GERI 60, RUZ_ESIK 0,10, RUZ_MIN_UYE 4, RUZ_MUTLAK 0, RUZ_BAYAT 5; UZUN_W 250, UZUN_BANT 1,50, UZUN_MUM 0,04, UZUN_KONUM 0,5) | D9_YENIDEN.d9_durum + d9_satir('c') (Ç181 'dosya' D9_YENIDEN.py); AVR sektör listesi yok -> AVRUPA VERİSİ YOK, karar en fazla ABD-ADAY (CLAUDE.md olay ölçüleri kuralı) |

Kurulamayan kart: yok (KT09 ve KT10 tanım / eşikleri ilgili modül fonksiyonlarıyla birebir; KT09 BIST ve KT10 AVR için veri yok, yukarıda yazılı).

## 2. Eşik sha'ları

| Ad | sha256 |
|---|---|
| KART_TUR1.py | 334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b |
| KT_ESIK_SHA | 3080dce505a769dd54be85739442ab45aa4b358def3b7803af79a6d642411310 |
| KT_KART_SHA | 16d107cdd75e961b22de6fc434eb3ebe1c899ad042f50e6d910d854aab9a47f5 |
| C2_ESIK22_SHA | df651ccbcd312f2e260befcbf5fa84bb192598c051467d081dc874b77889c71a |
| C2_ESIK_SHA | c44d76dd5da1d42c358f5bc1a9db3a34ee826c2c142d3113239248023637ff03 |
| YH_Y10_ESIK_SHA | b4ed76a3d6dc594b4e6e38af083c93e54b06958293b9988211065b0b37bdd235 |
| GE_OZELLIK_SHA | 68ea14bd5e5d31e0334eb55f953dd273fcb40a898c8441ba302584a74acfa206 |
| DS_OLAY_SHA | 167f3feb96c7a54970319691c1ebc9fb411046bc741ed65ce8b9171c0966229c |
| DP_KURULUM_SHA | e84a409896b6885bcb9aedec431797a43638cae4aa87c86bf375a0f76316bbf2 |
| D9_PARAM_SHA | 73dde4dbed813dc26779d522cbf2d74173571eabaf5f6b0ba0b72c30583e85e8 |
| OC_ESIK_SHA | 4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e |

Bağımlı dosyalar (olc blok açıkken bunların sha'sı aynı değilse DURUR):

BAGIMLI_SHA: CETVEL2.py 2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6
BAGIMLI_SHA: YAPI_HEDEF.py 812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e
BAGIMLI_SHA: GOZ_ETIKET.py 76d5c76b3a545ed585634d2994b66c11f4cdc1af924e2d31da1611595503bd9d
BAGIMLI_SHA: DUSUS_SONRASI.py b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf
BAGIMLI_SHA: BOFA_IZI.py fdbf98dfcfcf63d67ce8ac5e3e598084d30fcd0376ac63a27f31e39aaafc87b6
BAGIMLI_SHA: D9_YENIDEN.py a759d916915f2fc97f8258933fc5ce7d1b2cb8f6036691e1531e5d140c6bb80c
BAGIMLI_SHA: ORTAK_CETVEL.py 7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb
BAGIMLI_SHA: POZITIF_KONTROL.py 896a70ed704442531a0a4d747dff23fe241ac623b4c3a192114395baa5876fd6
BAGIMLI_SHA: KASA.py 3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b
BAGIMLI_SHA: S6_TABAN.py ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d
BAGIMLI_SHA: SIKISMA_YENIDEN.py ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae
BAGIMLI_SHA: sektor_ABD.csv f715c532d83cce13c53927a8134442f5f1be60c65322ecc60321f0ad355eef32
BAGIMLI_SHA: evren_disi_ABD.csv -
BAGIMLI_SHA: arastirma_cikti/col_yolu_abd/k34_evren.csv e138026a00492c25698dc5464d37c9f56769ab38f3ff1829252cc96c6e4946f1
BAGIMLI_SHA: arastirma_cikti/cetvel2/cetvel2_esik_v2.2.json f45e68ed49de307188ba35f894ee94f81035e357b59d6ce46f5e94fb0da74335
BAGIMLI_SHA: arastirma_cikti/cetvel2/cetvel2_guc_v2.2.json 95528165cb5ce2752a727a3f4d796f7cae48cb54848d0d0269b9b4afe4f4a13b

## 3. Karar kuralı (aynen)

Karar hücresi c(k, H, P) = kart k, karar ufku H in {15, 30}, karar pazarı P in {ABD, AVR} (KT10: yalnız ABD), birikimli hücre. GÜÇLÜ(c) = n >= 30 VE güç >= 0,80; KAPI(c) = plasebo kapısı geçti. T+(c) = GÜÇLÜ VE KAPI VE FARK > 0 VE boot alt > 0 VE SIRA > 0,50 VE L3O > 0; T-(c) = GÜÇLÜ VE KAPI VE FARK < 0 VE boot üst < 0 VE SIRA < 0,50 VE L3O(-) < 0 (boot bakışta %97,5). Yönü '+' olan kartta TUTAR = T+, TERS = T-; '-' kartta TUTAR = T-, TERS = T+. KART TUTAR <=> bir H1 karar ufkunda bütün karar pazarlarında TUTAR(c(k, H1, P)) VE öteki karar ufkunda (H2) bütün karar pazarlarında birikimli FARK beklenen işaretli VE açık veri (2016-22) hücresinde (H1) bütün karar pazarlarında FARK beklenen işaretli VE (k, H1) BH geçti (bakışta q 0,05, m 20). KATKI− <=> aynı şartlar ters yönde (TERS, ters işaretler, ters p ile BH). İkisi de değilse: bir karar hücresinde (iki ufuk, karar pazarları) GÜÇLÜ değil ya da KAPI düşmüşse ÖLÇÜLEMEDİ (neden yazılır); aksi 'İZ DEĞİL (bu ufuklarda, güç eğrisindeki en küçük yakalanır etki için)'. KT10 (AVR verisi yok): TUTAR -> 'ABD-ADAY', KATKI− -> 'ABD-ADAY (−)'. KONTROL KARTI KT00 (BH dışı): GÖRDÜ = bir karar ufkunda ABD ve AVR birikimli T+; KISMEN = bir karar ufkunda ABD ve AVR birikimli FARK > 0; aksi GÖRMEDİ. KT00 GÖRMEDİ ise tur 'cetvel / ufuk yetersiz' diye raporlanır ve 'İZ DEĞİL' etiketleri 'ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)' olur. Bakış dışı bloklarda aynı hesap BİLGİ (boot %95, BH q 0,10).

Cetvel: CETVEL2 v2.2 (C2.c2_olc22; C2_ESIK22 sha ön kayıtta): R_H = H. geçerli bar kapanışı / t+1 açılış - 1 (stop yok), konum eşli fark (aynı giriş günü, aynı pazar, aynı ATRP x likidite x F15 kovası, bütün evren, aynı kartın o günkü olayları ve olayın kendisi eş dışı, en az 5 eş), tekil H, ay kümeli boot (B 2000), ay kümeli işaret permütasyonu (R 10000), L3O, güç eğrisi (cetvel2_guc_v2.2.json; hücre adı eğride yoksa 'acik'), plasebo kapısı 200 tohum (|ort FARK| < 0,005 VE TUTAR payı <= %7, hipotez yönünde)

Ufuk: {'karar': [15, 30], 'bilgi': [45], 'plasebo': [15, 30], 'not': "ADIM K1 ana model kararı: R45 kuralı tutmadı (plasebo AVR 2020-22 %15, momentum R45'te de 0'dan ayrışmıyor) -> R45 BİLGİ, plasebosuz"}

Hücreler: hücre = pazar x giriş günü aralığı: 'acik' (2016-22, bilinen veri), açılmış her takvim çeyreği ('2023Q1' ...; BİLGİ, plasebosuz, permütasyonsuz) ve 'birikimli' (2023-01-01 .. açık kesik; plaseboyla). Fon krizi kesiği 31.08.2026 (OC); H. barı veri sonunu aşan olay ölçülmez, 'bekleyen' sayısı yazılır (sonraki blok açılınca ölçülür)

BH: aile = karar kartları (KT01-KT10; KT00 hariç) x karar ufku (15, 30) = 10 x 2 = 20 p; kart x ufuk p = karar pazarlarının birikimli hücrelerinde en büyük ay kümeli permütasyon p (beklenen yönde; ters yön etiketi için ters yön p'si ayrı BH)

Bonferroni: iki bakış için Bonferroni: bakış hücrelerinde boot aralığı %97,5 (alt 0,0125 / üst 0,9875 yüzdelik; aynı ay kümeli boot, B 2000) ve BH q 0,10 / 2 = 0,05

## 4. Bakış takvimi

- BAKIŞ 1: 2023Q1-2023Q4 birikimli: ana model 2023Q1, 2023Q2, 2023Q3, 2023Q4 bloklarını sırayla açar; her bloktan sonra olc (BİLGİ); 4. bloktan sonraki olc KARAR BAKIŞI 1.
- BAKIŞ 2: 2023Q1-2024Q4 birikimli: 2024Q1-Q4 açılınca 8. bloktan sonraki olc KARAR BAKIŞI 2.
- KARAR BAKIŞI yalnız açılmış blok sayısı 4 ve 8 iken (KASA_DURUM 'acilan' sırası 2023Q1'den kesintisiz); öteki blok sayılarında birikimli tablo BİLGİ (boot %95, BH q 0,10); 8'den sonra karar yok (bilgi)

## 5. Güç tablosu (açık veri sıklığından; 4 blok = 1 yıl, 8 blok = 2 yıl; güç cetvel2_guc_v2.2 'acik' eğrisi, delta +2 puan)

| Kart | Pazar | H | n açık (2016-22) | 4 blokta n | güç | 8 blokta n | güç |
|---|---|---|---|---|---|---|---|
| KT00 | ABD | 15 | 6024 | 861 | 1.00 | 1721 | 1.00 |
| KT00 | ABD | 30 | 3639 | 520 | 0.52 | 1040 | 0.85 |
| KT00 | ABD | 45 | 2716 | 388 | 0.28 | 776 | 0.54 |
| KT00 | AVR | 15 | 2788 | 398 | 0.98 | 797 | 1.00 |
| KT00 | AVR | 30 | 1737 | 248 | 0.67 | 496 | 0.94 |
| KT00 | AVR | 45 | 1351 | 193 | 0.47 | 386 | 0.81 |
| KT01 | ABD | 15 | 8487 | 1212 | 1.00 | 2425 | 1.00 |
| KT01 | ABD | 30 | 8394 | 1199 | 0.90 | 2398 | 1.00 |
| KT01 | ABD | 45 | 8322 | 1189 | 0.75 | 2378 | 0.98 |
| KT01 | AVR | 15 | 4177 | 597 | 1.00 | 1193 | 1.00 |
| KT01 | AVR | 30 | 4134 | 591 | 0.97 | 1181 | 1.00 |
| KT01 | AVR | 45 | 4084 | 583 | 0.95 | 1167 | 1.00 |
| KT01 | BIST | 15 | 2171 | 310 | 0.93 | 620 | 1.00 |
| KT01 | BIST | 30 | 2166 | 309 | 0.40 | 619 | 0.68 |
| KT01 | BIST | 45 | 2144 | 306 | 0.23 | 613 | 0.42 |
| KT02 | ABD | 15 | 334 | 48 | 0.18 | 95 | 0.31 |
| KT02 | ABD | 30 | 331 | 47 | 0.07 | 95 | 0.12 |
| KT02 | ABD | 45 | 327 | 47 | 0.06 | 93 | 0.09 |
| KT02 | AVR | 15 | 78 | 11 | 0.08 | 22 | 0.13 |
| KT02 | AVR | 30 | 76 | 11 | 0.06 | 22 | 0.09 |
| KT02 | AVR | 45 | 73 | 10 | 0.05 | 21 | 0.07 |
| KT02 | BIST | 15 | 205 | 29 | 0.14 | 59 | 0.26 |
| KT02 | BIST | 30 | 205 | 29 | 0.07 | 59 | 0.11 |
| KT02 | BIST | 45 | 205 | 29 | 0.05 | 59 | 0.07 |
| KT03 | ABD | 15 | 7445 | 1064 | 1.00 | 2127 | 1.00 |
| KT03 | ABD | 30 | 7361 | 1052 | 0.85 | 2103 | 0.99 |
| KT03 | ABD | 45 | 7297 | 1042 | 0.68 | 2085 | 0.96 |
| KT03 | AVR | 15 | 3622 | 517 | 1.00 | 1035 | 1.00 |
| KT03 | AVR | 30 | 3586 | 512 | 0.95 | 1025 | 1.00 |
| KT03 | AVR | 45 | 3542 | 506 | 0.91 | 1012 | 1.00 |
| KT03 | BIST | 15 | 1999 | 286 | 0.91 | 571 | 1.00 |
| KT03 | BIST | 30 | 1994 | 285 | 0.37 | 570 | 0.65 |
| KT03 | BIST | 45 | 1973 | 282 | 0.21 | 564 | 0.39 |
| KT04 | ABD | 15 | 3734 | 533 | 0.95 | 1067 | 1.00 |
| KT04 | ABD | 30 | 3693 | 528 | 0.53 | 1055 | 0.85 |
| KT04 | ABD | 45 | 3651 | 522 | 0.37 | 1043 | 0.68 |
| KT04 | AVR | 15 | 2063 | 295 | 0.92 | 589 | 1.00 |
| KT04 | AVR | 30 | 2042 | 292 | 0.75 | 583 | 0.97 |
| KT04 | AVR | 45 | 2027 | 290 | 0.67 | 579 | 0.95 |
| KT04 | BIST | 15 | 1334 | 191 | 0.74 | 381 | 0.97 |
| KT04 | BIST | 30 | 1330 | 190 | 0.26 | 380 | 0.47 |
| KT04 | BIST | 45 | 1315 | 188 | 0.15 | 376 | 0.27 |
| KT05 | ABD | 15 | 8062 | 1152 | 1.00 | 2303 | 1.00 |
| KT05 | ABD | 30 | 7973 | 1139 | 0.88 | 2278 | 1.00 |
| KT05 | ABD | 45 | 7908 | 1130 | 0.72 | 2259 | 0.97 |
| KT05 | AVR | 15 | 3873 | 553 | 1.00 | 1107 | 1.00 |
| KT05 | AVR | 30 | 3832 | 547 | 0.96 | 1095 | 1.00 |
| KT05 | AVR | 45 | 3787 | 541 | 0.93 | 1082 | 1.00 |
| KT05 | BIST | 15 | 2125 | 304 | 0.93 | 607 | 1.00 |
| KT05 | BIST | 30 | 2122 | 303 | 0.39 | 606 | 0.67 |
| KT05 | BIST | 45 | 2100 | 300 | 0.22 | 600 | 0.41 |
| KT06 | ABD | 15 | 4863 | 695 | 0.99 | 1389 | 1.00 |
| KT06 | ABD | 30 | 4808 | 687 | 0.65 | 1374 | 0.94 |
| KT06 | ABD | 45 | 4773 | 682 | 0.48 | 1364 | 0.81 |
| KT06 | AVR | 15 | 2603 | 372 | 0.97 | 744 | 1.00 |
| KT06 | AVR | 30 | 2581 | 369 | 0.85 | 737 | 0.99 |
| KT06 | AVR | 45 | 2542 | 363 | 0.78 | 726 | 0.98 |
| KT06 | BIST | 15 | 1368 | 195 | 0.75 | 391 | 0.98 |
| KT06 | BIST | 30 | 1366 | 195 | 0.27 | 390 | 0.48 |
| KT06 | BIST | 45 | 1354 | 193 | 0.16 | 387 | 0.28 |
| KT07 | ABD | 15 | 145 | 21 | 0.10 | 41 | 0.16 |
| KT07 | ABD | 30 | 145 | 21 | 0.05 | 41 | 0.07 |
| KT07 | ABD | 45 | 143 | 20 | 0.04 | 41 | 0.06 |
| KT07 | AVR | 15 | 30 | 4 | 0.05 | 9 | 0.07 |
| KT07 | AVR | 30 | 30 | 4 | 0.04 | 9 | 0.06 |
| KT07 | AVR | 45 | 29 | 4 | 0.04 | 8 | 0.05 |
| KT07 | BIST | 15 | 108 | 15 | 0.08 | 31 | 0.14 |
| KT07 | BIST | 30 | 108 | 15 | 0.05 | 31 | 0.07 |
| KT07 | BIST | 45 | 108 | 15 | 0.04 | 31 | 0.05 |
| KT08 | ABD | 15 | 4729 | 676 | 0.98 | 1351 | 1.00 |
| KT08 | ABD | 30 | 3347 | 478 | 0.48 | 956 | 0.81 |
| KT08 | ABD | 45 | 2845 | 406 | 0.29 | 813 | 0.56 |
| KT08 | AVR | 15 | 1774 | 253 | 0.88 | 507 | 1.00 |
| KT08 | AVR | 30 | 1356 | 194 | 0.56 | 387 | 0.87 |
| KT08 | AVR | 45 | 1226 | 175 | 0.43 | 350 | 0.76 |
| KT08 | BIST | 15 | 653 | 93 | 0.40 | 187 | 0.73 |
| KT08 | BIST | 30 | 436 | 62 | 0.11 | 125 | 0.18 |
| KT08 | BIST | 45 | 364 | 52 | 0.07 | 104 | 0.10 |
| KT09 | ABD | 15 | 162 | 23 | 0.10 | 46 | 0.17 |
| KT09 | ABD | 30 | 155 | 22 | 0.05 | 44 | 0.07 |
| KT09 | ABD | 45 | 148 | 21 | 0.04 | 42 | 0.06 |
| KT09 | AVR | 15 | 19 | 3 | 0.05 | 5 | 0.05 |
| KT09 | AVR | 30 | 19 | 3 | 0.04 | 5 | 0.05 |
| KT09 | AVR | 45 | 19 | 3 | 0.04 | 5 | 0.04 |
| KT10 | ABD | 15 | 17089 | 2441 | 1.00 | 4883 | 1.00 |
| KT10 | ABD | 30 | 10596 | 1514 | 0.96 | 3027 | 1.00 |
| KT10 | ABD | 45 | 8286 | 1184 | 0.75 | 2367 | 0.98 |

Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural); bu, sonuç görülmeden yazılmıştır.

## 6. Açık veri kuru koşusu (2016-22; BİLİNEN VERİ, karar değil)

Çıktı: arastirma_cikti/kart/acik/ (kt_hucre.csv, kt_satir.csv.gz, kt_huni.json, kt_prefix.json). Kesik 2022-12-31; KASA kapısı {'/tmp/kasa/acik/V_ABD.pkl': '2022-12-30', '/tmp/kasa/acik/V_AVR.pkl': '2022-12-30', '/tmp/kasa/acik/V_BIST.pkl': '2022-12-30', '/tmp/kasa/acik/k34_yahoo.pkl': '2022-12-30'}; çıktı en geç {'kt_satir.csv.gz': '2022-12-30', 'olculen_son_giris': {'15': '2022-12-12', '30': '2022-11-18', '45': '2022-10-28'}}; yeniden üretim TUTTU; prefix Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

Huni:

```
{
 "ABD": {
  "Y1": {
   "sinyal": 22667,
   "girdi": 22667,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 4,
   "giris_gec": 0,
   "likidite_alt20": 2933,
   "bolunme_gecmis": 25,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 2960,
   "tekil": 11017,
   "y1_olay": 8686,
   "F_KT02": 346,
   "F_KT03": 7614,
   "F_KT04": 3823,
   "F_KT05": 8245,
   "F_KT06": 4953,
   "F_KT07": 151,
   "sure_sn": 72.8
  },
  "D9": {
   "durum": 476557,
   "c": 234210,
   "sure_sn": 33.3
  },
  "MOM": {
   "sinyal": 83606,
   "ana": 13367,
   "U": 6718,
   "A": 6649,
   "son_tarih": "2022-11-30",
   "pk": {
    "girdi": 83606,
    "olay_havuz": 66837,
    "U": 6718,
    "A": 6649,
    "ana": 13367
   }
  },
  "BOFA": {
   "hisse": 1359,
   "kurulum": 508,
   "son": "2022-12-30"
  },
  "DS": {
   "girdi": 197352,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 236,
   "giris_gec": 0,
   "likidite_alt20": 45831,
   "bolunme_gecmis": 3532,
   "evren_once": 0,
   "gecmis_eksik": 5,
   "havuz_az": 0,
   "havuz_disi": 49368,
   "tekil": 0,
   "ds_gun": 197352,
   "havuz_gun": 147748,
   "ana": 14301,
   "F_KT08": 4936,
   "sure_sn": 73.0
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 13367,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 13367,
    "kova_yok": 0,
    "donem": {
     "acik": 13367
    }
   },
   "MOM|30": {
    "girdi": 13367,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 5468,
    "olcum_r15": 7785,
    "kova_yok": 0,
    "donem": {
     "acik": 7899
    }
   },
   "MOM|45": {
    "girdi": 13367,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 7388,
    "olcum_r15": 5818,
    "kova_yok": 0,
    "donem": {
     "acik": 5979
    }
   },
   "Y1|15": {
    "girdi": 8686,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 8605,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "Y1|30": {
    "girdi": 8686,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 8510,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "Y1|45": {
    "girdi": 8686,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 8433,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "DS|15": {
    "girdi": 14301,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 14087,
    "kova_yok": 0,
    "donem": {
     "acik": 14060,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 14301,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 5840,
    "olcum_r15": 8239,
    "kova_yok": 0,
    "donem": {
     "acik": 8319,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 14301,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 7760,
    "olcum_r15": 6287,
    "kova_yok": 0,
    "donem": {
     "acik": 6399,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 166,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "BOFA|30": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 159,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "BOFA|45": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 152,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "D9|15": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 161888,
    "olcum_r15": 18324,
    "kova_yok": 556,
    "donem": {
     "acik": 18011,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 168823,
    "olcum_r15": 11383,
    "kova_yok": 372,
    "donem": {
     "acik": 11238,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 171264,
    "olcum_r15": 8908,
    "kova_yok": 344,
    "donem": {
     "acik": 8851,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 12174,
   "girdi": 12174,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 2,
   "giris_gec": 0,
   "likidite_alt20": 1892,
   "bolunme_gecmis": 4,
   "evren_once": 0,
   "gecmis_eksik": 6,
   "havuz_az": 0,
   "havuz_disi": 1902,
   "tekil": 5773,
   "y1_olay": 4497,
   "F_KT02": 89,
   "F_KT03": 3911,
   "F_KT04": 2208,
   "F_KT05": 4161,
   "F_KT06": 2802,
   "F_KT07": 36,
   "sure_sn": 42.2
  },
  "MOM": {
   "sinyal": 43186,
   "ana": 6832,
   "U": 3452,
   "A": 3380,
   "son_tarih": "2022-11-30",
   "pk": {
    "girdi": 43186,
    "olay_havuz": 34183,
    "U": 3452,
    "A": 3380,
    "ana": 6832
   }
  },
  "BOFA": {
   "hisse": 575,
   "kurulum": 32,
   "son": "2022-12-30"
  },
  "DS": {
   "girdi": 51510,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 35,
   "giris_gec": 0,
   "likidite_alt20": 2666,
   "bolunme_gecmis": 702,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3386,
   "tekil": 0,
   "ds_gun": 51510,
   "havuz_gun": 48089,
   "ana": 4821,
   "F_KT08": 1969,
   "sure_sn": 29.5
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 6832,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 6832,
    "kova_yok": 0,
    "donem": {
     "acik": 6832
    }
   },
   "MOM|30": {
    "girdi": 6832,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 2688,
    "olcum_r15": 4088,
    "kova_yok": 0,
    "donem": {
     "acik": 4144
    }
   },
   "MOM|45": {
    "girdi": 6832,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 3602,
    "olcum
```

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 6718 | 6024 | 694 | 0 | +0.40 [-0.37; +1.14] | -0.13 | 0.502 | +0.04 | 0.1604 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT00 | + | ABD | 30 | 3948 | 3639 | 249 | 60 | +0.77 [-0.18; +1.75] | -0.63 | 0.503 | +0.35 | 0.0585 | 1.00 | -0.00 / 0.01 / True | False / False |
| KT00 | + | ABD | 45 | 2974 | 2716 | 172 | 86 | +1.07 [-0.07; +2.13] | -0.88 | 0.507 | +0.64 | 0.0380 | 0.99 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 3452 | 2788 | 664 | 0 | +0.07 [-0.45; +0.57] | -0.12 | 0.499 | -0.11 | 0.3821 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT00 | + | AVR | 30 | 2104 | 1737 | 337 | 30 | -0.24 [-1.12; +0.58] | -0.58 | 0.489 | -0.60 | 0.7121 | 1.00 | -0.02 / 0.01 / True | False / False |
| KT00 | + | AVR | 45 | 1640 | 1351 | 261 | 28 | +0.43 [-0.52; +1.42] | +0.12 | 0.507 | +0.01 | 0.1983 | 1.00 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 8686 | 8487 | 118 | 81 | -0.17 [-0.40; +0.07] | -0.18 | 0.496 | -0.27 | 0.9091 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | ABD | 30 | 8686 | 8394 | 116 | 176 | -0.25 [-0.58; +0.09] | -0.27 | 0.495 | -0.38 | 0.9183 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 45 | 8686 | 8322 | 111 | 253 | -0.25 [-0.65; +0.15] | -0.44 | 0.496 | -0.39 | 0.8737 | 1.00 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 4497 | 4177 | 279 | 41 | -0.02 [-0.23; +0.21] | -0.16 | 0.496 | -0.14 | 0.5787 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 4497 | 4134 | 275 | 88 | -0.16 [-0.48; +0.20] | -0.21 | 0.494 | -0.34 | 0.8096 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | AVR | 45 | 4497 | 4084 | 268 | 145 | -0.16 [-0.56; +0.27] | -0.40 | 0.494 | -0.36 | 0.7789 | 1.00 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 2588 | 2171 | 400 | 17 | -0.81 [-1.30; -0.29] | -2.82 | 0.451 | -1.08 | 0.9975 | 1.00 | -0.01 / 0.03 / True | False / True |
| KT01 | + | BIST | 30 | 2588 | 2166 | 395 | 27 | -0.77 [-1.75; +0.30] | -3.43 | 0.475 | -1.25 | 0.9190 | 1.00 | -0.01 / 0.03 / True | False / False |
| KT01 | + | BIST | 45 | 2588 | 2144 | 387 | 57 | -0.82 [-2.07; +0.50] | -4.31 | 0.473 | -1.39 | 0.8909 | 0.93 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 346 | 334 | 8 | 4 | -0.05 [-1.45; +1.38] | +0.17 | 0.507 | -0.57 | 0.5244 | 0.81 | -0.03 / 0.03 / True | False / False |
| KT02 | + | ABD | 30 | 346 | 331 | 8 | 7 | -1.20 [-6.73; +1.88] | +0.31 | 0.517 | -2.90 | 0.6395 | 0.34 | +0.08 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 346 | 327 | 8 | 11 | -2.22 [-8.79; +1.58] | -0.27 | 0.500 | -4.07 | 0.7472 | 0.23 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 89 | 78 | 11 | 0 | +0.49 [-1.51; +2.59] | +1.56 | 0.537 | -0.62 | 0.3264 | 0.37 | -0.03 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 89 | 76 | 11 | 2 | +0.97 [-1.17; +3.41] | +1.05 | 0.519 | -0.39 | 0.2094 | 0.24 | -0.06 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 89 | 73 | 11 | 5 | -0.28 [-3.73; +3.19] | -0.07 | 0.511 | -2.53 | 0.5570 | 0.19 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 238 | 205 | 33 | 0 | -0.23 [-1.74; +1.62] | -2.69 | 0.445 | -1.16 | 0.5962 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 238 | 205 | 33 | 0 | +0.02 [-2.21; +2.93] | -2.14 | 0.489 | -1.41 | 0.4923 | 0.28 | -0.04 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 238 | 205 | 33 | 0 | +1.02 [-1.90; +4.20] | -2.80 | 0.500 | -0.70 | 0.2563 | 0.16 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 7614 | 7445 | 102 | 67 | -0.20 [-0.44; +0.03] | -0.21 | 0.495 | -0.28 | 0.9438 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 30 | 7614 | 7361 | 101 | 152 | -0.25 [-0.61; +0.11] | -0.32 | 0.494 | -0.39 | 0.9148 | 1.00 | -0.14 / 0.03 / True | False / False |
| KT03 | + | ABD | 45 | 7614 | 7297 | 96 | 221 | -0.25 [-0.73; +0.18] | -0.50 | 0.496 | -0.39 | 0.8649 | 1.00 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 3911 | 3622 | 249 | 40 | +0.03 [-0.19; +0.27] | -0.15 | 0.497 | -0.09 | 0.4064 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT03 | + | AVR | 30 | 3911 | 3586 | 247 | 78 | -0.13 [-0.48; +0.22] | -0.24 | 0.494 | -0.33 | 0.7614 | 1.00 | +0.01 / 0.07 / True | False / False |
| KT03 | + | AVR | 45 | 3911 | 3542 | 240 | 129 | -0.14 [-0.57; +0.27] | -0.47 | 0.493 | -0.35 | 0.7546 | 1.00 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 2379 | 1999 | 366 | 14 | -0.64 [-1.18; -0.05] | -2.84 | 0.452 | -0.94 | 0.9861 | 1.00 | +0.02 / 0.02 / True | False / True |
| KT03 | + | BIST | 30 | 2379 | 1994 | 362 | 23 | -0.73 [-1.76; +0.37] | -3.49 | 0.475 | -1.25 | 0.8986 | 0.99 | +0.02 / 0.03 / True | False / False |
| KT03 | + | BIST | 45 | 2379 | 1973 | 355 | 51 | -0.64 [-1.91; +0.80] | -4.24 | 0.476 | -1.18 | 0.8113 | 0.91 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 3823 | 3734 | 50 | 39 | -0.20 [-0.50; +0.16] | -0.06 | 0.498 | -0.36 | 0.8716 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT04 | + | ABD | 30 | 3823 | 3693 | 50 | 80 | -0.46 [-0.97; +0.05] | -0.30 | 0.494 | -0.62 | 0.9546 | 1.00 | +0.02 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 3823 | 3651 | 45 | 127 | -0.65 [-1.27; -0.10] | -0.45 | 0.493 | -0.85 | 0.9852 | 1.00 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 2208 | 2063 | 128 | 17 | -0.03 [-0.36; +0.32] | -0.19 | 0.491 | -0.20 | 0.5721 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT04 | + | AVR | 30 | 2208 | 2042 | 128 | 38 | -0.03 [-0.50; +0.48] | -0.21 | 0.496 | -0.28 | 0.5520 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT04 | + | AVR | 45 | 2208 | 2027 | 125 | 56 | -0.04 [-0.57; +0.52] | -0.27 | 0.497 | -0.28 | 0.5533 | 1.00 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 1572 | 1334 | 224 | 14 | -0.84 [-1.51; -0.13] | -2.93 | 0.450 | -1.18 | 0.9892 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT04 | + | BIST | 30 | 1572 | 1330 | 221 | 21 | -0.70 [-1.80; +0.56] | -3.65 | 0.476 | -1.33 | 0.8724 | 0.95 | +0.02 / 0.02 / True | False / False |
| KT04 | + | BIST | 45 | 1572 | 1315 | 217 | 40 | -0.85 [-2.27; +0.76] | -4.41 | 0.470 | -1.49 | 0.8586 | 0.75 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 8245 | 8062 | 106 | 77 | -0.18 [-0.41; +0.05] | -0.18 | 0.496 | -0.29 | 0.9155 | 1.00 | -0.01 / 0.06 / True | False / False |
| KT05 | + | ABD | 30 | 8245 | 7973 | 105 | 167 | -0.31 [-0.66; +0.04] | -0.32 | 0.493 | -0.45 | 0.9592 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT05 | + | ABD | 45 | 8245 | 7908 | 102 | 235 | -0.34 [-0.79; +0.08] | -0.54 | 0.495 | -0.48 | 0.9337 | 1.00 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 4161 | 3873 | 251 | 37 | +0.00 [-0.21; +0.24] | -0.13 | 0.497 | -0.12 | 0.4859 | 1.00 | +0.00 / 0.01 / True | False / False |
| KT05 | + | AVR | 30 | 4161 | 3832 | 249 | 80 | -0.14 [-0.48; +0.24] | -0.21 | 0.496 | -0.33 | 0.7619 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 45 | 4161 | 3787 | 243 | 131 | -0.12 [-0.55; +0.30] | -0.34 | 0.496 | -0.33 | 0.6977 | 1.00 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 2535 | 2125 | 394 | 16 | -0.83 [-1.35; -0.25] | -2.78 | 0.451 | -1.10 | 0.9978 | 1.00 | +0.01 / 0.03 / True | False / True |
| KT05 | + | BIST | 30 | 2535 | 2122 | 389 | 24 | -0.79 [-1.85; +0.34] | -3.51 | 0.475 | -1.27 | 0.9155 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT05 | + | BIST | 45 | 2535 | 2100 | 381 | 54 | -0.87 [-2.10; +0.45] | -4.31 | 0.473 | -1.46 | 0.8926 | 0.92 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 4953 | 4863 | 68 | 22 | -0.01 [-0.26; +0.26] | -0.08 | 0.500 | -0.13 | 0.5279 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 4953 | 4808 | 66 | 79 | -0.06 [-0.41; +0.31] | -0.22 | 0.495 | -0.22 | 0.6409 | 1.00 | -0.03 / 0.03 / True | False / False |
| KT06 | + | ABD | 45 | 4953 | 4773 | 63 | 117 | -0.05 [-0.49; +0.39] | -0.27 | 0.498 | -0.24 | 0.5902 | 1.00 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 2802 | 2603 | 172 | 27 | -0.02 [-0.28; +0.25] | -0.14 | 0.496 | -0.14 | 0.5753 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT06 | + | AVR | 30 | 2802 | 2581 | 170 | 51 | -0.20 [-0.60; +0.24] | -0.27 | 0.494 | -0.42 | 0.8124 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 2802 | 2542 | 164 | 96 | -0.16 [-0.64; +0.30] | -0.33 | 0.495 | -0.39 | 0.7437 | 1.00 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 1626 | 1368 | 245 | 13 | -1.04 [-1.69; -0.35] | -2.86 | 0.442 | -1.36 | 0.9984 | 1.00 | +0.05 / 0.02 / True | False / True |
| KT06 | + | BIST | 30 | 1626 | 1366 | 244 | 16 | -1.38 [-2.48; -0.14] | -3.68 | 0.470 | -2.04 | 0.9844 | 0.96 | +0.05 / 0.03 / True | False / True |
| KT06 | + | BIST | 45 | 1626 | 1354 | 237 | 35 | -1.51 [-2.86; -0.15] | -4.07 | 0.467 | -2.15 | 0.9787 | 0.76 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 151 | 145 | 5 | 1 | -0.40 [-2.13; +1.42] | -0.52 | 0.487 | -1.28 | 0.6675 | 0.45 | -0.06 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 151 | 145 | 5 | 1 | -3.43 [-14.02; +2.19] | +0.34 | 0.512 | -5.89 | 0.6741 | 0.16 | -0.34 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 151 | 143 | 5 | 3 | -6.13 [-19.24; +0.88] | -0.48 | 0.485 | -9.78 | 0.8972 | 0.12 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 36 | 30 | 6 | 0 | +0.35 [-3.13; +4.02] | +0.66 | 0.518 | -1.54 | 0.4239 | 0.16 | +0.02 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 36 | 30 | 6 | 0 | -0.33 [-3.82; +2.84] | +0.77 | 0.517 | -2.00 | 0.5704 | 0.11 | +0.03 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 36 | 29 | 6 | 1 | +0.93 [-4.46; +5.70] | +1.27 | 0.534 | -3.00 | 0.3687 | 0.09 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 129 | 108 | 21 | 0 | -0.16 [-2.00; +2.28] | -2.69 | 0.454 | -1.56 | 0.5619 | 0.46 | +0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 129 | 108 | 21 | 0 | -0.55 [-3.23; +2.72] | -2.29 | 0.496 | -2.45 | 0.6379 | 0.16 | +0.13 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 129 | 108 | 21 | 0 | +0.54 [-3.11; +5.11] | -3.51 | 0.493 | -2.49 | 0.4119 | 0.10 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 4835 | 4729 | 45 | 61 | -0.02 [-0.48; +0.54] | -0.05 | 0.508 | -0.28 | 0.4617 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT08 | - | ABD | 30 | 3430 | 3347 | 36 | 47 | -0.47 [-1.72; +0.82] | -0.83 | 0.500 | -0.81 | 0.4003 | 1.00 | +0.01 / 0.05 / True | False / False |
| KT08 | - | ABD | 45 | 2946 | 2845 | 30 | 71 | -1.23 [-3.65; +1.31] | -1.87 | 0.495 | -1.76 | 0.4069 | 0.99 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 1838 | 1774 | 54 | 10 | +0.29 [-0.42; +1.11] | +0.35 | 0.515 | +0.05 | 0.7341 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | AVR | 30 | 1406 | 1356 | 40 | 10 | +0.42 [-0.71; +1.80] | +0.31 | 0.513 | +0.07 | 0.6945 | 1.00 | +0.04 / 0.03 / True | False / False |
| KT08 | - | AVR | 45 | 1266 | 1226 | 31 | 9 | +0.34 [-0.77; +1.93] | +0.20 | 0.510 | -0.28 | 0.6776 | 1.00 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 721 | 653 | 67 | 1 | -0.73 [-1.85; +0.51] | -1.50 | 0.480 | -1.40 | 0.1229 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | BIST | 30 | 475 | 436 | 38 | 1 | -2.08 [-5.69; +0.94] | -2.89 | 0.469 | -3.28 | 0.1807 | 0.53 | +0.03 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 400 | 364 | 34 | 2 | -3.83 [-9.60; +0.43] | -3.31 | 0.471 | -5.70 | 0.0979 | 0.26 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 167 | 162 | 4 | 1 | +4.39 [-1.47; +9.67] | +1.31 | 0.537 | -0.38 | 0.1082 | 0.49 | +0.00 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 167 | 155 | 4 | 8 | +6.67 [-2.13; +15.45] | +2.44 | 0.532 | -0.51 | 0.1109 | 0.17 | +0.01 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 167 | 148 | 4 | 15 | +10.23 [-8.64; +33.84] | -1.38 | 0.512 | -6.15 | 0.3596 | 0.12 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 20 | 19 | 0 | 1 | +2.31 [-10.77; +18.45] | -5.85 | 0.418 | -8.27 | 0.3755 | 0.11 | +0.08 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 20 | 19 | 0 | 1 | +2.51 [-8.79; +14.66] | +0.51 | 0.520 | -5.01 | 0.3341 | 0.08 | +0.21 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 20 | 19 | 0 | 1 | +1.07 [-12.55; +15.55] | -5.87 | 0.486 | -8.54 | 0.4330 | 0.07 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 18011 | 17089 | 751 | 171 | -0.01 [-0.21; +0.22] | -0.33 | 0.496 | -0.11 | 0.5255 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT10 | + | ABD | 30 | 11238 | 10596 | 465 | 177 | -0.10 [-0.58; +0.42] | -0.66 | 0.493 | -0.31 | 0.6431 | 1.00 | +0.00 / 0.00 / True | False / False |
| KT10 | + | ABD | 45 | 8851 | 8286 | 354 | 211 | -0.03 [-0.60; +0.60] | -0.72 | 0.500 | -0.30 | 0.5297 | 1.00 | - / - / False | False / False |

## 6b. Bayrak regresyonu (BİLGİ; olc'de kullanılmaz; `python KART_TUR1.py regresyon`, kt_regresyon.json)

Eski dosyalar (olay_Y1, ozellik_Y1, ozellik_Y1_s7, ds_olay) YALNIZ giriş <= 2022-12-30 satırlarıyla, açık fiyattan yeniden hesaplananlarla karşılaştırıldı.

| Pazar | Y1 olay yeni / eski / kesişim | Ş bayrağı farkı (KT02-KT07, kesişimde) | F1-F23 en büyük göreli fark | DS ANA yeni / eski / kesişim (yalnız yeni yıl) | DS yalnız eski |
|---|---|---|---|---|---|
| ABD | 8686 / 8686 / 8686 | 0 | 0.0e+00 | 14301 / 14061 / 14056 ({'2015': 241, '2022': 4}) | BFLY 2022-12-16, LWLG 2022-12-29, PAR 2022-11-01, PAR 2022-11-22, PAR 2022-12-14 |
| AVR | 4497 / 4496 / 4496 | 0 | 0.0e+00 | 4821 / 4562 / 4561 ({'2015': 259, '2022': 1}) | XPP.L 2022-10-28 |
| BIST | 2588 / 2588 / 2588 | 0 | 0.0e+00 | 2965 / 2947 / 2947 ({'2015': 18}) |  |

Notlar: AVR Y1'de tek fark FEV.L 2022-12-13 (yalnız açık veride olay; tam veride 2023-01-06 olayı; neden: kasa dışı veri sürümü karşılaştırılamaz). DS'de yalnız-yeni olaylar 2015 (eski ds_olay 2016'dan; cetvel 'acik' hücresi 2016'dan başladığı için ölçülmez) ve 2022 sonu birkaç olay; yalnız-eski 2022 sonu 5 (ABD) / 1 (AVR) olay (giriş veri sonuna yakın; açıklanamadı, HATA listesinde). KT00 = CETVEL2.c2_mom22 (K1 pozitif kontrolüyle aynı fonksiyon). KT09 kurulum sayısı (açık veri, 2016-22) ABD 508 / AVR 32 = BOFA_DIP sonuç dosyası 2016-22 n_olay 508 / 32 (birebir). KT10: D9_YENIDEN.d9_durum açık kesikte 250 bardan kısa yeni k34 serisinde AttributeError verdiği için KART_TUR1.kt_d9_durum satır satır kopyası kullanıldı (eksik bilgi sütunu NaN; bayrak hesabı aynı; test_kart_tur1 test_d9_durum_kopya: uzun serilerde d9_durum ile çerçeve eşit).

## 6c. Önceden yazılı uyarılar (sonuç görülmeden)

- Güç tablosuna göre 4. blok bakışında KT02, KT07, KT09 her karar hücresinde güç < 0,80 (ÖLÇÜLEMEDİ beklenir); KT04 / KT06 / KT08 R30 ABD hücresi < 0,80 olduğundan bu kartlar tutmazsa 'İZ DEĞİL' değil 'ÖLÇÜLEMEDİ' yazılır (kural).
- KT00 kontrol kartı açık veride (2016-22) R15 ABD +0,40 [−0,37; +1,14], R30 ABD +0,77 [−0,18; +1,75] puan: bir yılda (4 blok) T+ olması olası değil; KT00 GÖRMEDİ çıkarsa kural gereği tutmayan kartlar 'ÖLÇÜLEMEDİ (KT00 görmedi)' olur.
- R45 yalnız BİLGİ (plasebosuz); karar hücresi değil.

## 7. Ana modelin komutları (blok açtıktan sonra)

Her blok için (sırayla 2023Q1 ... ; 'KASA_GIZLI' ana modelin ortamında):

```
KASA_GIZLI=<yol> python KASA.py ac --blok 2023Q1 --hipotez KART_TUR1 --onkayit arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md
python KART_TUR1.py olc --veri /tmp/kasa/acik --cikti arastirma_cikti/kart/2023Q1 --islem 4
```

Her blok AYRI klasöre (aynı klasöre ikinci olc DURUR). 4. blok (2023Q4) ve 8. blok (2024Q4) klasöründeki kt_karar.csv KARAR BAKIŞIDIR. Beklenen çıktı (her blok klasöründe): kt_karar.csv (kart etiketleri; 4. ve 8. blokta KARAR, öteki BİLGİ), kt_hucre.csv (kart x ufuk x pazar x hücre), kt_satir.csv.gz, kt_huni.json, kt_prefix.json, kt_sonuc.json, kt_meta.json, KART_TUR1_SONUC.md. Ardından arastirma_cikti/kasa/KASA_DEFTERI.md ve çıktı klasörü commit edilir. KART_TUR1.py ve bu ön kayıt bu commit'ten sonra DEĞİŞMEZ.

## 8. KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = CETVEL2 v2.2 c2_es: aynı giriş günü, aynı pazar, aynı ATRP x likidite x F15 kovası, bütün evren, aynı geometri (R_H stop'suz); kartın o günkü olayları ve olayın kendisi eş dışı; plasebo kapısı 200 tohum aynı gün rastgele hisse (c2_plasebo); KT00 momentum kontrol kartı cetvelin bilinen etkiyi gördüğünü sınar; mekanik üstünlük yok (stop / hedef yok) |
| K2 | geleceğe bakma | EVET | bayraklar yalnız t ve öncesi barlarla; kt_prefix her grup x pazarda 8 olayda veri t'de kesilince aynı (kt_prefix.json; tutmazsa DURUR); KASA.kasa_kapisi veri en geç tarihi <= açık kesik; çıktı en geç tarihleri kt_meta.json; eski olay / özellik dosyaları olc'de okunmaz; evren / sektör listesi bugünkü (K7 / sınır) |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla + YH._yh_hazir (H > L, V > 0, fiyat > 0); sinyal günü geçersiz bar ise olay düşer (oc_olay_hazirla); R_H yalnız geçerli barlar |
| K4 | tekilleştirme | EVET | Y1 60 gün tekil (OC), DS ANA 15 bar tekil, BOFA 60 bar ayrı olay, MOM 15 bar ANA; cetvel tekil H (15 / 30 / 45); n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan FARK hücre tablosunda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla; R_H paydası); eşler aynı gün açılışı |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş; KASA bayt bayt bölünmüş); oranlar birimsiz; likidite günlük kesit sırası (AVR x Kur); BOFA veri kırığı kuralı (ABD / AVR 1/3 - 3 kat) aynen; geçmiş bölünme şüphesi havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (KT10 rüzgâr hesabında + ABD k34 nakdi biten, kesikten önce doğanlar); batan yok; dipteki kartlarda (KT02, KT07, KT08, KT09) yanlılık daha büyük; raporda yazılı |
| K8 | örneklem ve dönem | EVET | hücre başına n >= 30 ve güç >= 0,80 yoksa ÖLÇÜLEMEDİ; güç tablosu (4 / 8 blokta beklenen n) ön kayıtta; iki karar ufku + iki karar pazarı + açık veri işareti; BH q 0,10 (bakışta 0,05) m 20; iki bakış Bonferroni |
| K9 | ön kayıt | EVET | KART_TUR1_ON_KAYIT.md: KT_KART / KT_ESIK sha, KART_TUR1.py ve CETVEL2.py KASA_KOD sha'sı, bağımlı kod sha tablosu, karar kuralı, bakış takvimi, güç tablosu; sıra kod commit -> açık kuru koşu -> ön kayıt commit -> (ana model) blok aç -> olc; olc kesik > 2022-12-31 iken KASA.ks_onkayit_kapi + bağımlı sha denetimi |
| K10 | ayrıştırma | UYGULANMAZ | ham haber / KAP / SEC ayrıştırması yok; yalnız OHLCV + sektor_ABD.csv; eski olay dosyaları yalnız 'regresyon' komutunda (giriş <= 2022-12-30 satırları) karşılaştırma için okunur |
| K11 | yeniden üretim | EVET | kt_yeniden: iki hücre (KT01 ABD acik R15, KT08 AVR acik R30) satır dosyasından düz pandas ile n / ort FARK / ort SIRA; kt_satir.csv.gz'den bağımsız yeniden üretim; tutmazsa DURUR |
| K12 | ifade | EVET | etiketler yalnız karar kuralıyla; açık veri sonuçları 'bilinen veri' diye ayrı; sayı ve yorum ayrı cümle; 'iz' sözü yalnız kural geçerse |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_kt (test); defter / üretim / yasak modüllere dokunulmadı (bağımlı sha tablosu); e-posta / anahtar taraması (_kt_yaz); dış servis / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; kart ölçümü |

