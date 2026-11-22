# KART TURU 2 — ÖN KAYIT (donmuş kod; KASA 2 ile yürüyen ileri test, 2024Q1 .. 2026Q4)

Tarih: 2026-11-22 13:27:03 UTC. İş tanımı: arastirma_cikti/kart2/KART_TUR2_IS_TANIMI.md (git 5173c728dabab4481fd9a3561fb8d1835f7db640 2026-11-22T11:23:37+00:00). Kod: KART_TUR2.py (git b4406c9612c7f8748ef2c119d14ba8c3da70473e 2026-11-22T12:19:11+00:00).

KASA_HIPOTEZ: KART_TUR2
KASA_KOD: KART_TUR2.py 8baed7940c5422d5d3923dfb50b9b2bd22a6e58446b56e789e21a2fdea7c0842
KASA_KOD: KART_TUR1.py 334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b
KASA_KOD: YAPI_HEDEF.py 812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e
KASA_KOD: OLCU_SINAMA.py 86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087
KASA_KOD: TEZGAH2_DOGRULAMA.py 843b326cd53419c82a5e0eff593cbe615576c2fc0878da3e0a40d792088b4a91
KASA_KOD: ORTAK_CETVEL.py 7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb
KASA_KOD: DUSUS_SONRASI.py b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf
KASA_KOD: GOZ_ETIKET.py 76d5c76b3a545ed585634d2994b66c11f4cdc1af924e2d31da1611595503bd9d
KASA_KOD: BOFA_IZI.py fdbf98dfcfcf63d67ce8ac5e3e598084d30fcd0376ac63a27f31e39aaafc87b6
KASA_KOD: D9_YENIDEN.py a759d916915f2fc97f8258933fc5ce7d1b2cb8f6036691e1531e5d140c6bb80c
KASA_KOD: KASA.py 3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b
K2_ESIK_SHA: ca747d20f2fd6960fddabf1462dd440bed1a18dd2fe526c0a32c0c8d1aee8c8d
ACIK_TABLO_SHA: e28d59b0f050f70d8a666b15438862293f9862cedb3c43a22c33e28f37b347f9
GUC_SHA: 21b85eeec50caff470e2b3f88f81297f688c43641150b611497cc90ca769c68e
PREFIX_SHA: 552072248e07c474441d86467134c7aca52761b033632b258513b14539b7c4b8
OLAY_ACIK_SHA: ABD|Y1 626dbe865997da1e92008c0e98c13d19c5e8e81b0b0650c74b67cf6f815e8b8f
OLAY_ACIK_SHA: ABD|DS 631ec4c37af83382d23fb1619547d08e2431a1e7c7874b554388dd04c5f048e6
OLAY_ACIK_SHA: ABD|D9 dc5f429d1227a2b5e3daf4ffc2d1d067b78c99ff25143e78270f00b0880c0222
OLAY_ACIK_SHA: ABD|BOFA 3c0c4fcb6413feac491424fda2630b28c27c95f4f6a0c8966e2f34740e2e16ca
OLAY_ACIK_SHA: AVR|Y1 42be17b1c4c38f21d243ab3ffe927b294cd0e58bd7a8683eebd5cda28c3d4449
OLAY_ACIK_SHA: AVR|DS 607c9716e71bc7086afda755a4d14abe18850e4a556f1741feadfbdf645df590
OLAY_ACIK_SHA: AVR|D9 3ee3474680a56f4f93609bdd95ec163826fa31d3c8b0aaf16c7bb24ca8712996
OLAY_ACIK_SHA: AVR|BOFA c900133102007b01629fcdbdc9f543c789033242c9a8863fc0785cead84935ad

## 1. ANA MODEL KARARLARI (iş tanımından AYNEN)

(1) OLAY HAVUZU = P2 (`T2.t2_secili_panel(pazar, havuz='P2')`): tezgâh doğrulama kuralı piyasa serileri için P1'i seçti, ama kart ölçümü olay düzeyi 15-30 mum ortalamasıdır ve P1'in kuyruğu (R_15 > %300 olan 456 hisse-gün) ortalamayı anlamsız kılar; P2 36 hükmün 35'inde DOĞRU. Bu bir SAPMA notudur (kart sonucu görülmeden verildi). Eşler de yalnız P2 havuzundan. (2) ÖLÇÜ: R_H = H. geçerli bar kapanışı / t+1 açılış − 1, H = 15 ve 30 (karar); eş = aynı giriş günü, aynı pazar, OLCU_SINAMA KV1 kovası (ATRP tercili x likidite üçlüsü x F15 çeyreği; sınırlar tezgah2_hazirlik.json'daki sayılar), olay kümesi dışı, en az 5 eş; FARK = R_H − eş ortalaması; SIRA = eş dağılımındaki yüzdelik. Bilgi sütunları: medyan FARK, %1-%99 kırpılmış ortalama FARK, likidite üst yarı / alt yarı ayrı FARK. (3) HÜCRE TUTAR (beklenen yön +; − ise işaretler ters): n >= 30; ortalama FARK > 0 ve ay kümeli bootstrap (B 2000) alt ucu > 0; ortalama SIRA > 0,50 ve onun da boot alt ucu > 0,50; L3O (en iyi 3 ay çıkınca) FARK > 0; PLASEBO KAPISI (hücre, 200 tohum rastgele etiket: |ortalama FARK| < 0,5 puan ve yön başına tutar payı <= %7). (4) KARTLAR: KART_TUR1'deki tanımlar ve eşikler AYNEN (KT00 momentum yalnız bilgi; KT01 S6 taban kırılımı; KT02 dipte; KT03 dip savunulmuş; KT04 alt fitil az; KT05 küçük mum; KT06 gövdeli yakın tavan kırılımı; KT07 dip + savunma + alt fitil az; KT08 düşen bıçak (−); KT09 −%80 dip kurulumu; KT10 sektör rüzgârı yalnız sektörü bilinen ABD hisseleri) + üç yeni basit kart, tanımları mevcut kodda mühürlü: KT11 Y1 ∧ Ş9 U dip (YAPI_HEDEF Ş9 / Y11 eşikleri), KT12 Y1 ∧ Ş10 MACD pozitif uyumsuzluk (Y13 eşikleri), KT13 kısa vadeli dönüş kontrolü (son 21 gün getirisi alt onda, +; bilgi). Tanım koddan birebir alınamayan kart 'TANIM KURULAMADI' yazılır, uydurulmaz. Bayraklar yalnız açık fiyat verisinden hesaplanır; repo içindeki eski olay / sonuç dosyaları (2024+ satır içerir) OKUNMAZ. (5) YÜRÜYEN İLERİ TEST: KASA 2 blokları 2024Q1 .. 2026Q4 (12 blok) sırayla; her blok sonrası birikimli tablo (bilgi); KARAR BAKIŞI 4. blokta (2024 birikimli), 8. blokta ve 12. blokta; üç bakış için Bonferroni (boot güven düzeyi %98,33; p eşiği üçe bölünür). KART ETİKETİ (bakışta; karar hücreleri ABD ve AVR birikimli mühürlü dönem): İZ ADAYI = ABD ve AVR'de en az bir karar ufkunda TUTAR ve öteki ufukta aynı işaret ve açık verinin üç alt döneminin (2001-07, 2008-15, 2016-23) en az ikisinde aynı işaret, BH q 0,10 (m = kart sayısı x 2 ufuk; KT00 / KT13 hariç); ABD-ADAY = yalnız ABD'de aynı şartlar (AVR güçsüz ya da veri yok); KATKI− = ters yönde aynı şartlar; ETKİ YOK = iki pazarda iki ufukta güç >= 0,80 (yapay iz eğrisinden, +1 puan için) ve boot aralığı tümüyle (−1, +1) puan içinde; ÖLÇÜLEMEDİ = güç yetersiz; SORGULA = geri kalan. KT00 / KT13 hükmü kartların etiketini DEĞİŞTİRMEZ (tezgâh korelasyonla doğrulandı); yalnız raporlanır.

## 2. Kartlar (tanım ve eşik mevcut modüllerden; yeni eşik yok)

| Kart | Yön | Pazar | Karar | Cümle | Tanım (t'de bilinen) | Eşik | Kaynak (modül.fonksiyon) | KART_TUR2 uyarlaması |
|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD, AVR | kontrol (bilgi) | KONTROL KARTI: 12-1 momentum üst ondaki hisse (ay sonu, bütün evren) eşlerinden iyi. İz aramaz; kasada cetvelin bilinen etkiyi görüp görmediğini sınar | ay sonu t, MOM = C(t-21) / C(t-252) - 1, OC havuzu sonrası aynı t kesitinde sıra: üst onda U (POZITIF_KONTROL.pk_b_sinyal_mom + pk_b_kur; ANA = U ya da A, aynı hissede >= 15 bar arayla ilk) | üst onda (CETVEL2 v2.2 pozitif kontrol B1U ile AYNI tanım) | CETVEL2.c2_mom22 -> POZITIF_KONTROL.pk_b_sinyal_mom, pk_b_kur | KART_TUR1 tanımı (12-1 momentum, ay sonu, üst onda) aynen; sıra P2 havuzunda (giriş günü d'de P2 ve değeri sonlu hisseler, OS.os_kart_sinyal düzeni: t = ay sonu, d = hissenin sonraki geçerli barı, boşluk <= 10); KART_TUR1'in 'ANA = U ya da A, 15 bar' kuralı yerine cetvel tekili (H); yalnız BİLGİ |
| KT01 | + | ABD, AVR | karar | S6 taban kırılımı (YAPI_HEDEF Y1 olayı) eşlerinden iyi | S6 'al' günü (S6_TABAN.s6_taban; hat = kutu_alt (AL) ya da DİP(t-1) (AL_BOLGESIZ), hat > 0) -> OC.oc_olay_hazirla (giriş, havuz, 60 gün tekil) = Y1 OLAYI | S6 parametreleri (S6.s6_prm) + OC_ESIK olay (tekil 60) | YAPI_HEDEF.yh_sinyaller(['Y1']) -> yh_s6_hisse; ORTAK_CETVEL.oc_olay_hazirla | S6 'al' -> OC.oc_olay_hazirla (giriş, P2 havuzu, 60 gün tekil) = Y1 OLAYI |
| KT02 | + | ABD, AVR | karar | Y1 ∧ Ş1 DİPTE eşlerinden iyi | Y1 olayı VE F15 <= 0,25 VE F17 <= -0,20 | F15_ust 0.25, F17_ust -0.2 (YH_ESIK Y10 esik) | YAPI_HEDEF.yh_s7_sartlar['S1']; F15 / F17 GOZ_ETIKET.ge_ozellik_hisse | Y1 olayı (P2) VE Ş1 |
| KT03 | + | ABD, AVR | karar | Y1 ∧ Ş3 DİP SAVUNULMUŞ eşlerinden iyi | Y1 olayı VE F2 >= -0,01 (son dokunuş dibi / ilk dokunuş dibi - 1; dokunuş yoksa NaN = tutmaz) | F2_min -0.01 | YAPI_HEDEF.yh_s7_sartlar['S3']; F2 GOZ_ETIKET | Y1 olayı (P2) VE Ş3 |
| KT04 | + | ABD, AVR | karar | Y1 ∧ Ş5 ALT FİTİL AZ eşlerinden iyi | Y1 olayı VE F4 <= 0,25 (bölge medyan alt fitil payı) | F4_ust 0.25 | YAPI_HEDEF.yh_s7_sartlar['S5']; F4 GOZ_ETIKET | Y1 olayı (P2) VE Ş5 |
| KT05 | + | ABD, AVR | karar | Y1 ∧ Ş4 KÜÇÜK MUM eşlerinden iyi | Y1 olayı VE F3 <= 0,90 (bölge medyan mum boyu / ATR250) | F3_ust 0.9 | YAPI_HEDEF.yh_s7_sartlar['S4']; F3 GOZ_ETIKET | Y1 olayı (P2) VE Ş4 |
| KT06 | + | ABD, AVR | karar | Y1 ∧ Ş7 GÖVDELİ YAKIN TAVAN KIRILIMI eşlerinden iyi | Y1 olayı VE F22 = C_t / F21 - 1 > 0 VE F22a = O_t / F21 - 1 < 0 VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (F21 = max High[t-15 .. t-1]) | F22 > 0.0, F22a < 0.0, F23_min 0.5 | YAPI_HEDEF.yh_s7_sartlar['S7']; F20-F23 YAPI_HEDEF.yh_s7_ozellik | Y1 olayı (P2) VE Ş7 |
| KT07 | + | ABD, AVR | karar | Cemal'in son dersi: Y1 ∧ Ş1 ∧ Ş3 ∧ Ş5 (dip + savunma + alt fitil az) eşlerinden iyi | Y1 olayı VE Ş1 VE Ş3 VE Ş5 (eşikler KT02 / KT03 / KT04 ile aynı) | KT02 + KT03 + KT04 | YAPI_HEDEF.yh_s7_sartlar['S1'] & ['S3'] & ['S5'] | Y1 olayı (P2) VE Ş1 VE Ş3 VE Ş5 |
| KT08 | - | ABD, AVR | karar | Düşen bıçak (kural defteri K50 / KAZANANLAR H2): düşüş sonrası dipte, 120 günün tam dibine son 5 günde düşerek gelen hisse eşlerinden kötü | DS ANA olayı (DUSUS_SONRASI: C_t / max C son 120 - 1 <= -0,30, F15 <= 0,25, likidite, ABD C >= 2 $; OC giriş / havuz; ANA 15 bar tekil) VE F15_t <= 0,05 VE r5 = C_t / C_t-5 - 1 <= -0,03 (geçerli barlar; arastirma_cikti/canli/kazananlar.kz_ozellik tanımı) | F15 <= 0,05; r5 <= -0,03 (K50 kaydı, KURAL_DEFTERI_TASLAK.md; KAZANANLAR_2026-10-22 H2) | DUSUS_SONRASI.ds_ozellik_pazar + ds_olay_kur (ana); F15 / r5 = kazananlar.kz_ozellik formülü (testte birebir) | DS durum bayrağı DUSUS_SONRASI.ds_ozellik_hisse 's_ds' satırlarının satır satır kopyası (yalnız durum; özellik döngüsü atlanır; eşitlik testte ve hazırlıkta örneklemle denetlenir) -> DS.ds_olay_kur (OC giriş, P2 havuzu, ANA 15 bar) VE F15 <= 0,05 VE r5 <= -0,03 (KART_TUR1.kt_f15_r5) |
| KT09 | + | ABD, AVR | karar | −%80 dip kurulumu (Ç173b): tepeden >= %80 düşmüş, son 10 günde yeni dip yapmamış, dipten <= 1,5 kat uzaktaki hisse eşlerinden iyi | D1 C_t / max(C[t-250 .. t-1]) - 1 <= -0,80 (en az 200 bar, veri kırığından sonra) VE D2 min(C[t-9 .. t]) > min(C[t-59 .. t-10]) VE D3 C_t <= 1,50 x min(C[t-59 .. t-10]); aynı hissede ilk kurulum günü, sonraki >= 60 bar sonra | BOFA_IZI.DP_ESIK['kurulum'] (dusus -0,80, tepe 250 / 200, dip 60 / 10, dipten 1,50, ayri 60, kırık ABD / AVR [-0,6667, 2,0]) | BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum (Ç173 'dosya' BOFA_IZI.py diponkayit / dipkos); BIST verisi Yahoo önbelleği (TAVAN_SERISI) kasada yok -> BIST VERİ YOK | BOFA_IZI.dp_pkl_fiyat + dp_kurulum_tum aynen (kendi okuyucusu); kurulum günü -> OC.oc_olay_hazirla (giriş, P2, tekil 1; 60 bar ayrılık kurulum tanımında) |
| KT10 | + | ABD | karar | Sektör rüzgârı ABD (Ç181c): alt sektörü piyasadan >= 10 puan iyi giden (rüzgârlı) ve uzun çölde OLMAYAN hisse eşlerinden iyi | RÜZGÂR VE D9 DEĞİL (D9_YENIDEN.d9_satir 'c'): ruz = sepet (alt sektörün öteki >= 4 üyesi, 60 bar getiri eşit ağırlık) - piyasa (taze hisselerin 60 bar getiri medyanı) >= 0,10 VE sepet > 0; D9 uzun çöl değil; durum günleri (sektör ABD 'endustri', sektor_ABD.csv) | D9_YENIDEN.D9_PARAM (RUZ_GERI 60, RUZ_ESIK 0,10, RUZ_MIN_UYE 4, RUZ_MUTLAK 0, RUZ_BAYAT 5; UZUN_W 250, UZUN_BANT 1,50, UZUN_MUM 0,04, UZUN_KONUM 0,5) | D9_YENIDEN.d9_durum + d9_satir('c') (Ç181 'dosya' D9_YENIDEN.py); AVR sektör listesi yok -> AVRUPA VERİSİ YOK, karar en fazla ABD-ADAY (CLAUDE.md olay ölçüleri kuralı) | D9_YENIDEN.d9_durum hesabı (KART_TUR1.kt_d9_durum kopyası) aynen; tek fark dönem penceresi: D9_ESIK olay_bas 2015-06-01 D9 çalışmasının dönemi (kart tanımı değil) -> 2000-01-01; rüzgâr evreni = tezgâh evreni (OS.os_veri; k34 kasada yok); d9_satir 'c' -> OC.oc_olay_hazirla (giriş, P2, tekil 1) -> cetvel tekili (H); AVR sektör listesi yok |
| KT11 | + | ABD, AVR | karar | Y1 ∧ Ş9 U DİP (YAPI_HEDEF 5. tur Y11c tanımı) eşlerinden iyi | Y1 olayı VE Ş9: W = t'den önceki son 40 geçerli barın Low'u, L ≈ a x² + b x + c; F24 = a / ATR > 0 VE 0,20 <= F25 = x* / 39 <= 0,75 VE F26 = R² >= 0,40 VE F27 >= 1,0 VE F28 >= 0,5 VE |F29| <= 5 (NaN tutmaz; YAPI_HEDEF Ş9 tanımı aynen) | YH_ESIK['denemeler']['Y11']['esik'] = {'F24_alt_acik': 0.0, 'F25_alt': 0.2, 'F25_ust': 0.75, 'F26_min': 0.4, 'F27_min': 1.0, 'F28_min': 0.5, 'F29_mutlak_ust': 5.0} | YAPI_HEDEF.yh_s9_ozellik (F24-F29, 6 anlamlı basamak) + yh_s9_sartlar['S9'] | Y1 olayı (P2) VE Ş9; Y11 (Ş1 + Ş2 + Ş9) değil, iş tanımındaki 'Y1 ∧ Ş9' = Y11c kümesi |
| KT12 | + | ABD, AVR | karar | Y1 ∧ Ş10 MACD POZİTİF UYUMSUZLUK (YAPI_HEDEF 8. tur Y13) eşlerinden iyi | Y1 olayı VE Ş10: [t-60, t-1] içinde 5/5 salınım dipleri L1 < L2 (L1 <= L2 - 8); s65 = Low(L2) <= Low(L1) x 1,01 VE s66 = MACD(L2) > MACD(L1) VE MACD(L2) < 0 (MACD 12/26/9, [t-250, t] barları; YAPI_HEDEF Ş10 tanımı aynen) | YH_ESIK8['esik'] F65_ust 0.01, F66_alt_acik 0.0, F66m_ust_acik 0.0 | YAPI_HEDEF.yh_s10_ozellik ('S10' bayrağı) = yh_s10_maske('Y13') | Y1 olayı (P2) VE S10 == 1 |
| KT13 | + | ABD, AVR | kontrol (bilgi) | KONTROL KARTI: kısa vadeli dönüş (son 21 gün getirisi alt onda) eşlerinden iyi. İz aramaz | ay sonu t, STREV = C_k / C_{k-21} - 1 (k >= 21; OLCU_SINAMA kart tanımı), giriş günü d'de P2 havuzunda ve değeri sonlu hisseler arasında yüzde sıra <= 0,10 (alt onda) | OS_ESIK['kart'] onda 0,10 | OLCU_SINAMA.os_kart_sinyal (STREV) + P2 sırası | yalnız BİLGİ; KT00 ile birlikte raporlanır |

Kurulamayan kart: yok (KT00-KT13 tanım ve eşikleri ilgili modül fonksiyonlarıyla birebir; KT10 AVR için sektör verisi yok -> en fazla ABD-ADAY; BIST bu turda yok).

## 3. Eşik ve dosya sha'ları

| Ad | sha256 |
|---|---|
| KART_TUR2.py | 8baed7940c5422d5d3923dfb50b9b2bd22a6e58446b56e789e21a2fdea7c0842 |
| K2_ESIK_SHA | ca747d20f2fd6960fddabf1462dd440bed1a18dd2fe526c0a32c0c8d1aee8c8d |
| YH_Y10_ESIK_SHA | b4ed76a3d6dc594b4e6e38af083c93e54b06958293b9988211065b0b37bdd235 |
| YH_Y11_ESIK_SHA | e3ab7a3b3e81c36baf443975e5595158f0a61b45e09be526323200e24bceacf0 |
| YH_ESIK8_SHA | d28e8257274a85e0301d262d5808e51460fb944f4e5dd56a5f7ade762b03b09c |
| GE_OZELLIK_SHA | 68ea14bd5e5d31e0334eb55f953dd273fcb40a898c8441ba302584a74acfa206 |
| DS_OLAY_SHA | 167f3feb96c7a54970319691c1ebc9fb411046bc741ed65ce8b9171c0966229c |
| OC_ESIK_SHA | 4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e |
| OS_ESIK_SHA | 4bdc1d0617daed80531095f246e3d6c5e3c594374fd3021595c038b26bf441ab |
| T2_ESIK_SHA | 0c9b1d2ce8f326e4db5f804bbf0acb01f4c345d60e9b297ebff0fd5293d8d980 |
| DP_KURULUM_SHA | e84a409896b6885bcb9aedec431797a43638cae4aa87c86bf375a0f76316bbf2 |
| D9_PARAM_SHA | 73dde4dbed813dc26779d522cbf2d74173571eabaf5f6b0ba0b72c30583e85e8 |

Bağımlı dosyalar (olc blok açıkken bunların sha'sı aynı değilse DURUR):

BAGIMLI_SHA: KART_TUR1.py 334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b
BAGIMLI_SHA: YAPI_HEDEF.py 812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e
BAGIMLI_SHA: GOZ_ETIKET.py 76d5c76b3a545ed585634d2994b66c11f4cdc1af924e2d31da1611595503bd9d
BAGIMLI_SHA: DUSUS_SONRASI.py b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf
BAGIMLI_SHA: BOFA_IZI.py fdbf98dfcfcf63d67ce8ac5e3e598084d30fcd0376ac63a27f31e39aaafc87b6
BAGIMLI_SHA: D9_YENIDEN.py a759d916915f2fc97f8258933fc5ce7d1b2cb8f6036691e1531e5d140c6bb80c
BAGIMLI_SHA: ORTAK_CETVEL.py 7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb
BAGIMLI_SHA: OLCU_SINAMA.py 86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087
BAGIMLI_SHA: TEZGAH2_DOGRULAMA.py 843b326cd53419c82a5e0eff593cbe615576c2fc0878da3e0a40d792088b4a91
BAGIMLI_SHA: TEZGAH_DOGRULAMA.py 24232ab516bae5699306e9d9e60f5c24121421b7f1206a08a68a7fae7aeda702
BAGIMLI_SHA: KASA.py 3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b
BAGIMLI_SHA: S6_TABAN.py ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d
BAGIMLI_SHA: SIKISMA_YENIDEN.py ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae
BAGIMLI_SHA: CETVEL2.py 2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6
BAGIMLI_SHA: POZITIF_KONTROL.py 896a70ed704442531a0a4d747dff23fe241ac623b4c3a192114395baa5876fd6
BAGIMLI_SHA: sektor_ABD.csv f715c532d83cce13c53927a8134442f5f1be60c65322ecc60321f0ad355eef32
BAGIMLI_SHA: arastirma_cikti/tezgah2/tezgah2_hazirlik.json baba2309e2968828a60b78fa69505f241f6716dde113081b8c6f5fe934447ea8
BAGIMLI_SHA: arastirma_cikti/kasa/KASA2_MANIFEST.json 29ebf402cbedfffe441b3321e629b6fd8fa7cfa590137dce44ce1de0362b21e8
BAGIMLI_SHA: arastirma_cikti/k55_dallanma/K55_EVREN_DISI.csv e080ba048c071e063b40c1b9e7d97f0c62aefbf59d974651cf229dd6b8478da9

Önbellek (repo dışı; /tmp/kart2_onbellek): ABD: dosya sha 463f4afd9818af6c5b95b1274074a9bb44853ee92c58744bafc9ada1e27e1e42, satır {'Y1': 184021, 'DS': 1037337, 'D9': 519641, 'BOFA': 6166}; AVR: dosya sha eba0fd824e10afa63467daca83957a736beab28d8505d949316a7b862bf15261, satır {'Y1': 36625, 'DS': 129417, 'D9': 0, 'BOFA': 177}

## 4. Ölçü, hücre, plasebo, güç, BH, Bonferroni (K2_ESIK; aynen)

Havuz: TEZGAH2_DOGRULAMA T2_ESIK['havuz']['P2']: P1 (OS paneli ok VE H >= 0) VE d-1 kapanışı x Kur >= 2 USD (AVR 1 EUR) VE Lq (20 gün medyan işlem değeri, d-1'e kadar) >= 1 mn USD / EUR; panel = OS.os_veri + OS.os_panel(sinir = tezgah2_hazirlik.json) + T2.t2_havuz (= t2_secili_panel(pazar, havuz='P2') ile aynı hesap; KASA kapısı K2'nin kendi kapısı, çünkü t2_kasa_kapi açık kesiği 2023-12-31'e sabitler)

Ölçü: R_H = giriş barından (giriş barı 1.) H. geçerli barın kapanışı / giriş barı açılışı E0 - 1; giriş satırından 2H birleşik takvim satırında H geçerli bar yoksa ölçülmez (OS.os_olcu_hesap 'R' ile aynı; testte eşit)

Eş: aynı giriş günü d, aynı pazar, aynı KV1 kovası, P2 havuzunda, R_H ölçülebilir; aynı kartın o günkü olay kümesi (H tekilinden ÖNCE) ve olayın kendisi dışı; en az 5 eş (OS.os_havuz / OS.os_es)

Tekil: {'Y1': 'OC 60 gün (oc_olay_hazirla tekil_gun 60)', 'DS': 'ANA 15 bar (DS.ds_olay_kur)', 'BOFA': 'kurulum tanımında 60 bar', 'D9': 'yok (durum günleri)', 'MOM': 'yok (ay sonu)', 'STREV': 'yok (ay sonu)', 'H': 'sonra kart x H başına: aynı hissede birleşik takvimde >= H gün arayla ilk olay (OS.os_tekil kuralı); eş dışı küme tekil öncesi'}

Hücreler: hücre = kart x pazar x H x giriş günü aralığı. acik_d1 / d2 / d3 (bilinen veri; DONDURULMUŞ: giriş <= 2023-12-31 olan hisse-günün R_H'si H. barı > 2023-12-31 ise ölçülmez, olay ve eş için aynı -> 'acik_tasan'); açılmış her takvim çeyreği (BİLGİ, plasebosuz, permütasyonsuz); 'birikimli' = giriş 2024-01-01 .. açık kesik (karar; plaseboyla). Fon krizi kesiği 31.08.2026 (OC.oc_veri_hazirla); H. barı veri sonunu aşan olay 'bekleyen' (sonraki blokta ölçülür), kriz kesiğini aşan 'kriz' (hiç ölçülmez)

Boot: {'B': 2000, 'tohum': 2291, 'alt95': 0.025, 'ust95': 0.975, 'alt_bakis': 0.008333333333333333, 'ust_bakis': 0.9916666666666667, 'birim': 'giriş ayı (ay toplamı ve sayısı yeniden örneklenir; FARK ve SIRA aynı ağırlıklarla)'}

Permütasyon: ay kümeli işaret permütasyonu (FARK; beklenen yön ve ters yön tek yönlü p) (R 10000)

Plasebo: hücrenin her olayı için aynı giriş günü d'de P2 havuzundan (KV1 >= 0, R_H ölçülebilir) rastgele bir hisse (gün içinde yerine koymadan); eş dışı küme = çekilen küme; aynı hücre kuralı; 200 tohum. GEÇER = |200 tohum ortalama FARK| < 0,005 VE TUTAR(+) payı <= %7 VE TUTAR(-) payı <= %7. Plasebo hücreleri: açık alt dönemler (yalnız kuru koşuda; BİLGİ; açık tablo sha'lı) ve birikimli (karar)

Güç: yapay iz: pencerenin P2 havuzundan (KV1 >= 0, R_H ölçülebilir; dondurulmuş R) yerine koymadan n hisse-gün; R_H + delta (toplamsal: FARK tam delta kayar); eş dışı = çekilen küme; yakalama = hücre TUTAR(+) (plasebo hariç); 40 tohum. Pencere 1y / 2y / 3y bakış 1 / 2 / 3 için (boot %98,33), d1 / d2 / d3 açık alt dönemler için (boot %95). Gerçek kart olayları aylara kümelenir; rastgele hisse-gün daha dağınıktır -> güç İYİMSER (rapor notu). Hücre gücü = eğrinin hücre n'inde (log n doğrusal ara değer; n < 30 -> 0)

BH: aile = karar kartları (KT01-KT12; KT00 / KT13 hariç) x karar ufku (15, 30) = 24 p. İki aile: (A) iki pazar p = karar pazarlarının birikimli hücrelerinde en büyük ay kümeli permütasyon p (İZ ADAYI / KATKI−; KT10 yalnız ABD), (B) ABD p (ABD-ADAY / KATKI− yalnız ABD). Ters yön etiketi ters yön p'si ile ayrı BH (q 0.1; bakışta 0.0333)

## 5. Kart etiketi (işlemsel kural; ANA MODEL KARARI (5)'in kodu)

Karar hücresi c(k, H, P) = kart k, H in {15, 30}, P in {ABD, AVR} (KT10: yalnız ABD), birikimli. TUT(c) = hücre TUTAR (beklenen yönde, boot bakışta %98,33) VE plasebo GEÇER. İŞARET(c) = FARK beklenen işaretli. ALT(k, H, P) = acik_d1 / d2 / d3 hücrelerinden FARK'ı beklenen işaretli olanların sayısı. GÜÇLÜ(c) = n >= 30 VE güç(n; +1 puan; bakış penceresi) >= 0,80. İZ ADAYI <=> bir H1'de ABD ve AVR'de TUT VE öteki H2'de ABD ve AVR'de İŞARET VE ABD ve AVR'de ALT(k, H1) >= 2 VE (k, H1) BH (A) geçti. KATKI− <=> aynı şartlar ters yönde. ABD-ADAY <=> AVR veri yok (KT10) ya da AVR c(k, H1) GÜÇLÜ değil VE ABD'de aynı şartlar VE (k, H1) BH (B) geçti; ters yönde 'KATKI− (yalnız ABD)'. ETKİ YOK <=> bütün karar hücrelerinde GÜÇLÜ VE boot aralığı (bakış düzeyi) tümüyle (-0,01, +0,01) içinde. ÖLÇÜLEMEDİ <=> bir karar hücresi GÜÇLÜ değil. SORGULA <=> geri kalan. Sıra: İZ ADAYI, KATKI−, ABD-ADAY, KATKI− (yalnız ABD), ETKİ YOK, ÖLÇÜLEMEDİ, SORGULA. KONTROL (KT00, KT13; BH dışı, etiketleri değiştirmez): GÖRDÜ = bir H'de ABD ve AVR TUT; KISMEN = bir H'de ABD ve AVR İŞARET; aksi GÖRMEDİ. Bakış dışı bloklarda aynı hesap BİLGİ (boot %95, BH q 0,10).

## 6. Kova sınırları (tezgah2_hazirlik.json; KV1 = ATRP tercili x 12 + LQ3 x 4 + F15 çeyreği)

```json
{"ABD": {"KV1_ATRP": [0.02496298683654129, 0.0418801751616038], "KV1_F15": [0.23345296346069216, 0.5581271928100532, 0.8488934532165978]}, "AVR": {"KV1_ATRP": [0.019559290051277323, 0.02836184453749112], "KV1_F15": [0.28224258561611526, 0.6103212224324032, 0.8709724126665116]}}
```

## 7. Bakış takvimi

- Ana model blokları sırayla açar (2024Q1 ... 2026Q4); her bloktan sonra olc (BİLGİ, birikimli tablo).
- KARAR BAKIŞI 1: 4. blok (2024Q1-Q4) açıkken; BAKIŞ 2: 8. blok (2024Q1-2025Q4); BAKIŞ 3: 12. blok (2024Q1-2026Q4; veri 31.08.2026'da kesik).
- KARAR BAKIŞI yalnız açılmış blok sayısı 4 (2024), 8 (2024-25) ve 12 (2024-26) iken; KASA_DURUM 'acilan' sırası 2024Q1'den kesintisiz; öteki blok sayılarında tablo BİLGİ (boot %95, BH q 0,10)

## 8. Güç tablosu (yapay iz eğrisi, P2 havuzu, +1 puan; beklenen n = açık 2016-23 sıklığı / 8 yıl x etkin yıl)

| Kart | Pazar | H | n açık d3 | 4 blokta n | güç | 8 blokta n | güç | 12 blokta n | güç | karar verebilir (güç >= 0,80) |
|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | ABD | 15 | 21313 | 2506 | 1.00 | 5170 | 1.00 | 6938 | 1.00 | bakış 1, 2, 3 |
| KT00 | ABD | 30 | 12477 | 1374 | 0.62 | 2934 | 0.84 | 3969 | 0.94 | bakış 2, 3 |
| KT00 | AVR | 15 | 3126 | 367 | 0.70 | 758 | 0.82 | 1018 | 0.98 | bakış 2, 3 |
| KT00 | AVR | 30 | 1896 | 209 | 0.31 | 446 | 0.30 | 603 | 0.60 | hiçbir bakışta |
| KT01 | ABD | 15 | 27176 | 3195 | 1.00 | 6592 | 1.00 | 8847 | 1.00 | bakış 1, 2, 3 |
| KT01 | ABD | 30 | 26888 | 2961 | 0.80 | 6322 | 1.00 | 8553 | 1.00 | bakış 2, 3 |
| KT01 | AVR | 15 | 4763 | 560 | 0.87 | 1155 | 0.98 | 1551 | 0.99 | bakış 1, 2, 3 |
| KT01 | AVR | 30 | 4725 | 520 | 0.56 | 1111 | 0.83 | 1503 | 0.95 | bakış 2, 3 |
| KT02 | ABD | 15 | 1529 | 180 | 0.22 | 371 | 0.30 | 498 | 0.30 | hiçbir bakışta |
| KT02 | ABD | 30 | 1500 | 165 | 0.03 | 353 | 0.11 | 477 | 0.14 | hiçbir bakışta |
| KT02 | AVR | 15 | 93 | 11 | 0.00 | 23 | 0.00 | 30 | 0.00 | hiçbir bakışta |
| KT02 | AVR | 30 | 90 | 10 | 0.00 | 21 | 0.00 | 29 | 0.00 | hiçbir bakışta |
| KT03 | ABD | 15 | 23870 | 2806 | 1.00 | 5790 | 1.00 | 7771 | 1.00 | bakış 1, 2, 3 |
| KT03 | ABD | 30 | 23618 | 2601 | 0.75 | 5553 | 1.00 | 7513 | 1.00 | bakış 2, 3 |
| KT03 | AVR | 15 | 4124 | 485 | 0.83 | 1000 | 0.98 | 1343 | 0.99 | bakış 1, 2, 3 |
| KT03 | AVR | 30 | 4088 | 450 | 0.52 | 961 | 0.77 | 1300 | 0.92 | bakış 3 |
| KT04 | ABD | 15 | 12304 | 1446 | 0.94 | 2984 | 0.94 | 4006 | 0.99 | bakış 1, 2, 3 |
| KT04 | ABD | 30 | 12160 | 1339 | 0.62 | 2859 | 0.83 | 3868 | 0.94 | bakış 2, 3 |
| KT04 | AVR | 15 | 2358 | 277 | 0.60 | 572 | 0.65 | 768 | 0.91 | bakış 3 |
| KT04 | AVR | 30 | 2337 | 257 | 0.38 | 549 | 0.35 | 743 | 0.71 | hiçbir bakışta |
| KT05 | ABD | 15 | 26064 | 3064 | 1.00 | 6322 | 1.00 | 8485 | 1.00 | bakış 1, 2, 3 |
| KT05 | ABD | 30 | 25789 | 2840 | 0.78 | 6063 | 1.00 | 8204 | 1.00 | bakış 2, 3 |
| KT05 | AVR | 15 | 4458 | 524 | 0.86 | 1081 | 0.98 | 1451 | 0.99 | bakış 1, 2, 3 |
| KT05 | AVR | 30 | 4423 | 487 | 0.54 | 1040 | 0.81 | 1407 | 0.94 | bakış 2, 3 |
| KT06 | ABD | 15 | 15413 | 1812 | 0.98 | 3739 | 0.97 | 5018 | 1.00 | bakış 1, 2, 3 |
| KT06 | ABD | 30 | 15191 | 1673 | 0.64 | 3572 | 0.90 | 4832 | 0.99 | bakış 2, 3 |
| KT06 | AVR | 15 | 2946 | 346 | 0.67 | 715 | 0.78 | 959 | 0.96 | bakış 3 |
| KT06 | AVR | 30 | 2922 | 322 | 0.44 | 687 | 0.52 | 930 | 0.84 | bakış 3 |
| KT07 | ABD | 15 | 661 | 78 | 0.07 | 160 | 0.09 | 215 | 0.13 | hiçbir bakışta |
| KT07 | ABD | 30 | 648 | 71 | 0.11 | 152 | 0.07 | 206 | 0.07 | hiçbir bakışta |
| KT07 | AVR | 15 | 41 | 5 | 0.00 | 10 | 0.00 | 13 | 0.00 | hiçbir bakışta |
| KT07 | AVR | 30 | 38 | 4 | 0.00 | 9 | 0.00 | 12 | 0.00 | hiçbir bakışta |
| KT08 | ABD | 15 | 17558 | 2064 | 1.00 | 4259 | 0.98 | 5716 | 1.00 | bakış 1, 2, 3 |
| KT08 | ABD | 30 | 14263 | 1571 | 0.63 | 3354 | 0.88 | 4537 | 0.98 | bakış 2, 3 |
| KT08 | AVR | 15 | 1867 | 219 | 0.62 | 453 | 0.59 | 608 | 0.85 | bakış 3 |
| KT08 | AVR | 30 | 1587 | 175 | 0.26 | 373 | 0.35 | 505 | 0.51 | hiçbir bakışta |
| KT09 | ABD | 15 | 965 | 113 | 0.09 | 234 | 0.16 | 314 | 0.25 | hiçbir bakışta |
| KT09 | ABD | 30 | 955 | 105 | 0.09 | 225 | 0.08 | 304 | 0.08 | hiçbir bakışta |
| KT09 | AVR | 15 | 20 | 2 | 0.00 | 5 | 0.00 | 7 | 0.00 | hiçbir bakışta |
| KT09 | AVR | 30 | 20 | 2 | 0.00 | 5 | 0.00 | 6 | 0.00 | hiçbir bakışta |
| KT10 | ABD | 15 | 24591 | 2891 | 1.00 | 5965 | 1.00 | 8006 | 1.00 | bakış 1, 2, 3 |
| KT10 | ABD | 30 | 14930 | 1644 | 0.64 | 3510 | 0.89 | 4749 | 0.99 | bakış 2, 3 |
| KT11 | ABD | 15 | 1544 | 182 | 0.22 | 375 | 0.30 | 503 | 0.30 | hiçbir bakışta |
| KT11 | ABD | 30 | 1504 | 166 | 0.03 | 354 | 0.11 | 478 | 0.14 | hiçbir bakışta |
| KT11 | AVR | 15 | 253 | 30 | 0.00 | 61 | 0.09 | 82 | 0.16 | hiçbir bakışta |
| KT11 | AVR | 30 | 248 | 27 | 0.00 | 58 | 0.07 | 79 | 0.12 | hiçbir bakışta |
| KT12 | ABD | 15 | 2563 | 301 | 0.35 | 622 | 0.50 | 834 | 0.58 | hiçbir bakışta |
| KT12 | ABD | 30 | 2528 | 278 | 0.14 | 594 | 0.21 | 804 | 0.29 | hiçbir bakışta |
| KT12 | AVR | 15 | 381 | 45 | 0.13 | 92 | 0.16 | 124 | 0.20 | hiçbir bakışta |
| KT12 | AVR | 30 | 377 | 42 | 0.05 | 89 | 0.05 | 120 | 0.18 | hiçbir bakışta |
| KT13 | ABD | 15 | 21589 | 2538 | 1.00 | 5237 | 1.00 | 7028 | 1.00 | bakış 1, 2, 3 |
| KT13 | ABD | 30 | 18483 | 2035 | 0.66 | 4346 | 0.96 | 5880 | 1.00 | bakış 2, 3 |
| KT13 | AVR | 15 | 2869 | 337 | 0.66 | 696 | 0.77 | 934 | 0.96 | bakış 3 |
| KT13 | AVR | 30 | 2556 | 281 | 0.41 | 601 | 0.41 | 813 | 0.76 | hiçbir bakışta |

Güç eğrisi (yakalama payı; pencere 1y / 2y / 3y boot %98,33, d1-d3 %95; yanlış pozitif = delta 0):

| Pazar | H | Pencere | n | yanlış poz. | +0,5 | +1 | +2 |
|---|---|---|---|---|---|---|---|
| ABD | 15 | 1y | 30 | 0.00 | 0.03 | 0.05 | 0.15 |
| ABD | 15 | 1y | 50 | 0.03 | 0.03 | 0.10 | 0.25 |
| ABD | 15 | 1y | 100 | 0.00 | 0.00 | 0.05 | 0.60 |
| ABD | 15 | 1y | 200 | 0.03 | 0.10 | 0.25 | 0.72 |
| ABD | 15 | 1y | 300 | 0.00 | 0.17 | 0.35 | 0.90 |
| ABD | 15 | 1y | 500 | 0.03 | 0.10 | 0.50 | 0.93 |
| ABD | 15 | 1y | 1000 | 0.03 | 0.28 | 0.88 | 1.00 |
| ABD | 15 | 1y | 2000 | 0.00 | 0.47 | 1.00 | 1.00 |
| ABD | 15 | 1y | 5000 | 0.00 | 0.88 | 1.00 | 1.00 |
| ABD | 15 | 2y | 30 | 0.00 | 0.00 | 0.03 | 0.12 |
| ABD | 15 | 2y | 50 | 0.00 | 0.03 | 0.05 | 0.20 |
| ABD | 15 | 2y | 100 | 0.00 | 0.00 | 0.07 | 0.42 |
| ABD | 15 | 2y | 200 | 0.00 | 0.03 | 0.10 | 0.60 |
| ABD | 15 | 2y | 300 | 0.00 | 0.03 | 0.25 | 0.78 |
| ABD | 15 | 2y | 500 | 0.00 | 0.07 | 0.38 | 0.93 |
| ABD | 15 | 2y | 1000 | 0.03 | 0.23 | 0.78 | 1.00 |
| ABD | 15 | 2y | 2000 | 0.00 | 0.23 | 0.90 | 1.00 |
| ABD | 15 | 2y | 5000 | 0.00 | 0.80 | 1.00 | 1.00 |
| ABD | 15 | 3y | 30 | 0.03 | 0.03 | 0.03 | 0.12 |
| ABD | 15 | 3y | 50 | 0.00 | 0.03 | 0.07 | 0.15 |
| ABD | 15 | 3y | 100 | 0.03 | 0.05 | 0.20 | 0.45 |
| ABD | 15 | 3y | 200 | 0.00 | 0.00 | 0.10 | 0.45 |
| ABD | 15 | 3y | 300 | 0.00 | 0.03 | 0.25 | 0.78 |
| ABD | 15 | 3y | 500 | 0.03 | 0.10 | 0.30 | 0.97 |
| ABD | 15 | 3y | 1000 | 0.00 | 0.25 | 0.68 | 1.00 |
| ABD | 15 | 3y | 2000 | 0.00 | 0.38 | 0.97 | 1.00 |
| ABD | 15 | 3y | 5000 | 0.00 | 0.78 | 1.00 | 1.00 |
| ABD | 15 | d1 | 30 | 0.00 | 0.03 | 0.03 | 0.12 |
| ABD | 15 | d1 | 50 | 0.00 | 0.05 | 0.17 | 0.53 |
| ABD | 15 | d1 | 100 | 0.00 | 0.00 | 0.17 | 0.68 |
| ABD | 15 | d1 | 200 | 0.00 | 0.03 | 0.38 | 0.95 |
| ABD | 15 | d1 | 300 | 0.00 | 0.03 | 0.45 | 0.97 |
| ABD | 15 | d1 | 500 | 0.03 | 0.33 | 0.80 | 1.00 |
| ABD | 15 | d1 | 1000 | 0.00 | 0.42 | 0.97 | 1.00 |
| ABD | 15 | d1 | 2000 | 0.00 | 0.75 | 1.00 | 1.00 |
| ABD | 15 | d1 | 5000 | 0.00 | 0.95 | 1.00 | 1.00 |
| ABD | 15 | d2 | 30 | 0.03 | 0.05 | 0.10 | 0.23 |
| ABD | 15 | d2 | 50 | 0.00 | 0.03 | 0.07 | 0.28 |
| ABD | 15 | d2 | 100 | 0.05 | 0.10 | 0.30 | 0.60 |
| ABD | 15 | d2 | 200 | 0.00 | 0.10 | 0.38 | 0.88 |
| ABD | 15 | d2 | 300 | 0.00 | 0.07 | 0.47 | 0.95 |
| ABD | 15 | d2 | 500 | 0.00 | 0.33 | 0.78 | 1.00 |
| ABD | 15 | d2 | 1000 | 0.00 | 0.45 | 0.95 | 1.00 |
| ABD | 15 | d2 | 2000 | 0.00 | 0.90 | 1.00 | 1.00 |
| ABD | 15 | d2 | 5000 | 0.00 | 1.00 | 1.00 | 1.00 |
| ABD | 15 | d3 | 30 | 0.00 | 0.03 | 0.05 | 0.23 |
| ABD | 15 | d3 | 50 | 0.03 | 0.10 | 0.15 | 0.33 |
| ABD | 15 | d3 | 100 | 0.00 | 0.03 | 0.23 | 0.55 |
| ABD | 15 | d3 | 200 | 0.03 | 0.17 | 0.28 | 0.72 |
| ABD | 15 | d3 | 300 | 0.03 | 0.10 | 0.35 | 0.93 |
| ABD | 15 | d3 | 500 | 0.00 | 0.28 | 0.65 | 0.97 |
| ABD | 15 | d3 | 1000 | 0.00 | 0.23 | 0.88 | 1.00 |
| ABD | 15 | d3 | 2000 | 0.00 | 0.42 | 1.00 | 1.00 |
| ABD | 15 | d3 | 5000 | 0.00 | 0.95 | 1.00 | 1.00 |
| ABD | 30 | 1y | 30 | 0.00 | 0.00 | 0.00 | 0.05 |
| ABD | 30 | 1y | 50 | 0.00 | 0.03 | 0.12 | 0.23 |
| ABD | 30 | 1y | 100 | 0.00 | 0.05 | 0.10 | 0.17 |
| ABD | 30 | 1y | 200 | 0.00 | 0.00 | 0.00 | 0.38 |
| ABD | 30 | 1y | 300 | 0.00 | 0.03 | 0.17 | 0.47 |
| ABD | 30 | 1y | 500 | 0.00 | 0.07 | 0.28 | 0.80 |
| ABD | 30 | 1y | 1000 | 0.03 | 0.17 | 0.60 | 0.97 |
| ABD | 30 | 1y | 2000 | 0.03 | 0.25 | 0.65 | 1.00 |
| ABD | 30 | 1y | 5000 | 0.03 | 0.42 | 1.00 | 1.00 |
| ABD | 30 | 2y | 30 | 0.03 | 0.03 | 0.05 | 0.12 |
| ABD | 30 | 2y | 50 | 0.03 | 0.03 | 0.03 | 0.12 |
| ABD | 30 | 2y | 100 | 0.00 | 0.03 | 0.07 | 0.17 |
| ABD | 30 | 2y | 200 | 0.00 | 0.00 | 0.07 | 0.42 |
| ABD | 30 | 2y | 300 | 0.00 | 0.05 | 0.10 | 0.60 |
| ABD | 30 | 2y | 500 | 0.00 | 0.05 | 0.12 | 0.75 |
| ABD | 30 | 2y | 1000 | 0.00 | 0.05 | 0.47 | 0.93 |
| ABD | 30 | 2y | 2000 | 0.00 | 0.15 | 0.72 | 1.00 |
| ABD | 30 | 2y | 5000 | 0.00 | 0.45 | 1.00 | 1.00 |
| ABD | 30 | 3y | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| ABD | 30 | 3y | 50 | 0.00 | 0.03 | 0.03 | 0.05 |
| ABD | 30 | 3y | 100 | 0.00 | 0.00 | 0.00 | 0.07 |
| ABD | 30 | 3y | 200 | 0.00 | 0.03 | 0.07 | 0.25 |
| ABD | 30 | 3y | 300 | 0.03 | 0.05 | 0.07 | 0.45 |
| ABD | 30 | 3y | 500 | 0.00 | 0.03 | 0.15 | 0.62 |
| ABD | 30 | 3y | 1000 | 0.00 | 0.15 | 0.35 | 0.95 |
| ABD | 30 | 3y | 2000 | 0.00 | 0.10 | 0.78 | 1.00 |
| ABD | 30 | 3y | 5000 | 0.05 | 0.38 | 1.00 | 1.00 |
| ABD | 30 | d1 | 30 | 0.03 | 0.05 | 0.05 | 0.10 |
| ABD | 30 | d1 | 50 | 0.00 | 0.00 | 0.03 | 0.20 |
| ABD | 30 | d1 | 100 | 0.00 | 0.10 | 0.15 | 0.35 |
| ABD | 30 | d1 | 200 | 0.03 | 0.05 | 0.20 | 0.75 |
| ABD | 30 | d1 | 300 | 0.00 | 0.05 | 0.28 | 0.80 |
| ABD | 30 | d1 | 500 | 0.00 | 0.10 | 0.35 | 0.93 |
| ABD | 30 | d1 | 1000 | 0.00 | 0.30 | 0.82 | 1.00 |
| ABD | 30 | d1 | 2000 | 0.00 | 0.50 | 1.00 | 1.00 |
| ABD | 30 | d1 | 5000 | 0.00 | 0.88 | 1.00 | 1.00 |
| ABD | 30 | d2 | 30 | 0.00 | 0.00 | 0.03 | 0.20 |
| ABD | 30 | d2 | 50 | 0.03 | 0.05 | 0.05 | 0.25 |
| ABD | 30 | d2 | 100 | 0.00 | 0.05 | 0.17 | 0.35 |
| ABD | 30 | d2 | 200 | 0.03 | 0.10 | 0.28 | 0.78 |
| ABD | 30 | d2 | 300 | 0.00 | 0.07 | 0.35 | 0.85 |
| ABD | 30 | d2 | 500 | 0.03 | 0.10 | 0.38 | 0.95 |
| ABD | 30 | d2 | 1000 | 0.03 | 0.25 | 0.68 | 1.00 |
| ABD | 30 | d2 | 2000 | 0.00 | 0.53 | 0.97 | 1.00 |
| ABD | 30 | d2 | 5000 | 0.00 | 0.90 | 1.00 | 1.00 |
| ABD | 30 | d3 | 30 | 0.03 | 0.05 | 0.10 | 0.17 |
| ABD | 30 | d3 | 50 | 0.00 | 0.03 | 0.03 | 0.10 |
| ABD | 30 | d3 | 100 | 0.03 | 0.05 | 0.07 | 0.33 |
| ABD | 30 | d3 | 200 | 0.03 | 0.07 | 0.20 | 0.45 |
| ABD | 30 | d3 | 300 | 0.07 | 0.15 | 0.38 | 0.80 |
| ABD | 30 | d3 | 500 | 0.03 | 0.17 | 0.40 | 0.95 |
| ABD | 30 | d3 | 1000 | 0.00 | 0.10 | 0.45 | 1.00 |
| ABD | 30 | d3 | 2000 | 0.00 | 0.20 | 0.82 | 1.00 |
| ABD | 30 | d3 | 5000 | 0.03 | 0.65 | 1.00 | 1.00 |
| AVR | 15 | 1y | 30 | 0.00 | 0.00 | 0.05 | 0.10 |
| AVR | 15 | 1y | 50 | 0.00 | 0.05 | 0.15 | 0.53 |
| AVR | 15 | 1y | 100 | 0.00 | 0.12 | 0.23 | 0.75 |
| AVR | 15 | 1y | 200 | 0.00 | 0.20 | 0.62 | 0.97 |
| AVR | 15 | 1y | 300 | 0.00 | 0.17 | 0.60 | 1.00 |
| AVR | 15 | 1y | 500 | 0.03 | 0.28 | 0.85 | 1.00 |
| AVR | 15 | 1y | 1000 | 0.00 | 0.62 | 1.00 | 1.00 |
| AVR | 15 | 1y | 2000 | 0.03 | 0.88 | 1.00 | 1.00 |
| AVR | 15 | 1y | 5000 | 0.00 | 1.00 | 1.00 | 1.00 |
| AVR | 15 | 2y | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 15 | 2y | 50 | 0.00 | 0.03 | 0.05 | 0.30 |
| AVR | 15 | 2y | 100 | 0.03 | 0.12 | 0.17 | 0.68 |
| AVR | 15 | 2y | 200 | 0.03 | 0.12 | 0.28 | 0.88 |
| AVR | 15 | 2y | 300 | 0.00 | 0.12 | 0.68 | 0.97 |
| AVR | 15 | 2y | 500 | 0.03 | 0.15 | 0.57 | 1.00 |
| AVR | 15 | 2y | 1000 | 0.00 | 0.40 | 0.97 | 1.00 |
| AVR | 15 | 2y | 2000 | 0.00 | 0.85 | 1.00 | 1.00 |
| AVR | 15 | 2y | 5000 | 0.00 | 0.97 | 1.00 | 1.00 |
| AVR | 15 | 3y | 30 | 0.00 | 0.00 | 0.00 | 0.10 |
| AVR | 15 | 3y | 50 | 0.00 | 0.07 | 0.20 | 0.42 |
| AVR | 15 | 3y | 100 | 0.03 | 0.05 | 0.15 | 0.75 |
| AVR | 15 | 3y | 200 | 0.03 | 0.07 | 0.30 | 0.95 |
| AVR | 15 | 3y | 300 | 0.00 | 0.03 | 0.53 | 1.00 |
| AVR | 15 | 3y | 500 | 0.03 | 0.15 | 0.80 | 1.00 |
| AVR | 15 | 3y | 1000 | 0.00 | 0.42 | 0.97 | 1.00 |
| AVR | 15 | 3y | 2000 | 0.00 | 0.70 | 1.00 | 1.00 |
| AVR | 15 | 3y | 5000 | 0.03 | 1.00 | 1.00 | 1.00 |
| AVR | 15 | d1 | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 15 | d1 | 50 | 0.05 | 0.05 | 0.12 | 0.55 |
| AVR | 15 | d1 | 100 | 0.00 | 0.10 | 0.30 | 0.72 |
| AVR | 15 | d1 | 200 | 0.00 | 0.07 | 0.47 | 0.97 |
| AVR | 15 | d1 | 300 | 0.00 | 0.15 | 0.53 | 0.97 |
| AVR | 15 | d1 | 500 | 0.00 | 0.28 | 0.80 | 1.00 |
| AVR | 15 | d1 | 1000 | 0.00 | 0.60 | 0.95 | 1.00 |
| AVR | 15 | d1 | 2000 | 0.00 | 0.80 | 1.00 | 1.00 |
| AVR | 15 | d1 | 5000 | 0.05 | 0.97 | 1.00 | 1.00 |
| AVR | 15 | d2 | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 15 | d2 | 50 | 0.00 | 0.05 | 0.10 | 0.57 |
| AVR | 15 | d2 | 100 | 0.03 | 0.07 | 0.20 | 0.88 |
| AVR | 15 | d2 | 200 | 0.00 | 0.25 | 0.60 | 0.97 |
| AVR | 15 | d2 | 300 | 0.00 | 0.25 | 0.68 | 1.00 |
| AVR | 15 | d2 | 500 | 0.00 | 0.38 | 0.88 | 1.00 |
| AVR | 15 | d2 | 1000 | 0.03 | 0.53 | 1.00 | 1.00 |
| AVR | 15 | d2 | 2000 | 0.00 | 0.85 | 1.00 | 1.00 |
| AVR | 15 | d2 | 5000 | 0.00 | 1.00 | 1.00 | 1.00 |
| AVR | 15 | d3 | 30 | 0.00 | 0.00 | 0.00 | 0.03 |
| AVR | 15 | d3 | 50 | 0.00 | 0.07 | 0.20 | 0.65 |
| AVR | 15 | d3 | 100 | 0.00 | 0.10 | 0.28 | 0.72 |
| AVR | 15 | d3 | 200 | 0.00 | 0.20 | 0.57 | 0.97 |
| AVR | 15 | d3 | 300 | 0.07 | 0.23 | 0.72 | 1.00 |
| AVR | 15 | d3 | 500 | 0.00 | 0.40 | 0.85 | 1.00 |
| AVR | 15 | d3 | 1000 | 0.00 | 0.57 | 1.00 | 1.00 |
| AVR | 15 | d3 | 2000 | 0.05 | 0.95 | 1.00 | 1.00 |
| AVR | 15 | d3 | 5000 | 0.00 | 1.00 | 1.00 | 1.00 |
| AVR | 30 | 1y | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 30 | 1y | 50 | 0.03 | 0.05 | 0.07 | 0.20 |
| AVR | 30 | 1y | 100 | 0.00 | 0.05 | 0.07 | 0.35 |
| AVR | 30 | 1y | 200 | 0.03 | 0.07 | 0.30 | 0.82 |
| AVR | 30 | 1y | 300 | 0.03 | 0.15 | 0.42 | 0.93 |
| AVR | 30 | 1y | 500 | 0.03 | 0.20 | 0.55 | 1.00 |
| AVR | 30 | 1y | 1000 | 0.00 | 0.20 | 0.78 | 1.00 |
| AVR | 30 | 1y | 2000 | 0.03 | 0.72 | 1.00 | 1.00 |
| AVR | 30 | 1y | 5000 | 0.05 | 0.95 | 1.00 | 1.00 |
| AVR | 30 | 2y | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 30 | 2y | 50 | 0.00 | 0.05 | 0.07 | 0.28 |
| AVR | 30 | 2y | 100 | 0.00 | 0.03 | 0.05 | 0.33 |
| AVR | 30 | 2y | 200 | 0.00 | 0.03 | 0.07 | 0.88 |
| AVR | 30 | 2y | 300 | 0.03 | 0.12 | 0.40 | 0.82 |
| AVR | 30 | 2y | 500 | 0.00 | 0.05 | 0.28 | 0.95 |
| AVR | 30 | 2y | 1000 | 0.03 | 0.28 | 0.80 | 1.00 |
| AVR | 30 | 2y | 2000 | 0.00 | 0.42 | 0.97 | 1.00 |
| AVR | 30 | 2y | 5000 | 0.00 | 0.90 | 1.00 | 1.00 |
| AVR | 30 | 3y | 30 | 0.00 | 0.00 | 0.00 | 0.03 |
| AVR | 30 | 3y | 50 | 0.03 | 0.03 | 0.05 | 0.25 |
| AVR | 30 | 3y | 100 | 0.00 | 0.03 | 0.15 | 0.40 |
| AVR | 30 | 3y | 200 | 0.03 | 0.07 | 0.25 | 0.75 |
| AVR | 30 | 3y | 300 | 0.00 | 0.03 | 0.28 | 0.97 |
| AVR | 30 | 3y | 500 | 0.00 | 0.12 | 0.50 | 1.00 |
| AVR | 30 | 3y | 1000 | 0.00 | 0.35 | 0.88 | 1.00 |
| AVR | 30 | 3y | 2000 | 0.00 | 0.55 | 1.00 | 1.00 |
| AVR | 30 | 3y | 5000 | 0.00 | 0.82 | 1.00 | 1.00 |
| AVR | 30 | d1 | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 30 | d1 | 50 | 0.00 | 0.03 | 0.07 | 0.30 |
| AVR | 30 | d1 | 100 | 0.00 | 0.07 | 0.23 | 0.55 |
| AVR | 30 | d1 | 200 | 0.00 | 0.07 | 0.42 | 0.85 |
| AVR | 30 | d1 | 300 | 0.03 | 0.15 | 0.57 | 0.95 |
| AVR | 30 | d1 | 500 | 0.03 | 0.12 | 0.60 | 0.97 |
| AVR | 30 | d1 | 1000 | 0.05 | 0.25 | 0.85 | 1.00 |
| AVR | 30 | d1 | 2000 | 0.00 | 0.45 | 1.00 | 1.00 |
| AVR | 30 | d1 | 5000 | 0.00 | 0.93 | 1.00 | 1.00 |
| AVR | 30 | d2 | 30 | 0.00 | 0.00 | 0.00 | 0.00 |
| AVR | 30 | d2 | 50 | 0.03 | 0.07 | 0.15 | 0.45 |
| AVR | 30 | d2 | 100 | 0.03 | 0.07 | 0.15 | 0.50 |
| AVR | 30 | d2 | 200 | 0.00 | 0.03 | 0.23 | 0.72 |
| AVR | 30 | d2 | 300 | 0.00 | 0.17 | 0.40 | 0.90 |
| AVR | 30 | d2 | 500 | 0.00 | 0.25 | 0.65 | 0.97 |
| AVR | 30 | d2 | 1000 | 0.03 | 0.28 | 0.97 | 1.00 |
| AVR | 30 | d2 | 2000 | 0.00 | 0.75 | 0.97 | 1.00 |
| AVR | 30 | d2 | 5000 | 0.00 | 0.95 | 1.00 | 1.00 |
| AVR | 30 | d3 | 30 | 0.00 | 0.00 | 0.00 | 0.03 |
| AVR | 30 | d3 | 50 | 0.03 | 0.05 | 0.17 | 0.38 |
| AVR | 30 | d3 | 100 | 0.00 | 0.03 | 0.10 | 0.60 |
| AVR | 30 | d3 | 200 | 0.00 | 0.03 | 0.33 | 0.82 |
| AVR | 30 | d3 | 300 | 0.03 | 0.20 | 0.45 | 0.93 |
| AVR | 30 | d3 | 500 | 0.00 | 0.33 | 0.70 | 1.00 |
| AVR | 30 | d3 | 1000 | 0.03 | 0.45 | 0.93 | 1.00 |
| AVR | 30 | d3 | 2000 | 0.00 | 0.68 | 1.00 | 1.00 |
| AVR | 30 | d3 | 5000 | 0.00 | 0.97 | 1.00 | 1.00 |

Güç < 0,80 olan karar hücresi o bakışta ÖLÇÜLEMEDİ verir (kural); bu, sonuç görülmeden yazılmıştır. Rastgele hisse-gün kart olaylarından daha dağınık olduğu için güç İYİMSERDİR.

## 9. Prefix testi ve DS kopya denetimi (hazırlık; k2_prefix.json)

```json
{
 "prefix": {
  "ABD": {
   "sinyal": {
    "Y1": {
     "n_tam": 166791,
     "n_kisa": 166791,
     "esit": true
    },
    "DS": {
     "n_tam": 848969,
     "n_kisa": 848969,
     "esit": true
    },
    "D9": {
     "n_tam": 451259,
     "n_kisa": 451259,
     "esit": true
    },
    "BOFA": {
     "n_tam": 4265,
     "n_kisa": 4265,
     "esit": true
    }
   },
   "olay": {
    "KT01": {
     "n_tam": 50225,
     "n_kisa": 50225,
     "esit": true
    },
    "KT02": {
     "n_tam": 1934,
     "n_kisa": 1934,
     "esit": true
    },
    "KT03": {
     "n_tam": 43733,
     "n_kisa": 43733,
     "esit": true
    },
    "KT04": {
     "n_tam": 21664,
     "n_kisa": 21664,
     "esit": true
    },
    "KT05": {
     "n_tam": 47760,
     "n_kisa": 47760,
     "esit": true
    },
    "KT06": {
     "n_tam": 29817,
     "n_kisa": 29817,
     "esit": true
    },
    "KT07": {
     "n_tam": 835,
     "n_kisa": 835,
     "esit": true
    },
    "KT11": {
     "n_tam": 2595,
     "n_kisa": 2595,
     "esit": true
    },
    "KT12": {
     "n_tam": 3915,
     "n_kisa": 3915,
     "esit": true
    },
    "KT08": {
     "n_tam": 25758,
     "n_kisa": 25758,
     "esit": true
    },
    "KT09": {
     "n_tam": 959,
     "n_kisa": 959,
     "esit": true
    },
    "KT10": {
     "n_tam": 379803,
     "n_kisa": 379803,
     "esit": true
    },
    "KT00": {
     "n_tam": 38054,
     "n_kisa": 38054,
     "esit": true
    },
    "KT13": {
     "n_tam": 39378,
     "n_kisa": 39378,
     "esit": true
    }
   },
   "tutar": true
  },
  "AVR": {
   "sinyal": {
    "Y1": {
     "n_tam": 33730,
     "n_kisa": 33730,
     "esit": true
    },
    "DS": {
     "n_tam": 112772,
     "n_kisa": 112772,
     "esit": true
    },
    "D9": {
     "n_tam": 0,
     "n_kisa": 0,
     "esit": true
    },
    "BOFA": {
     "n_tam": 166,
     "n_kisa": 166,
     "esit": true
    }
   },
   "olay": {
    "KT01": {
     "n_tam": 10567,
     "n_kisa": 10567,
     "esit": true
    },
    "KT02": {
     "n_tam": 180,
     "n_kisa": 180,
     "esit": true
    },
    "KT03": {
     "n_tam": 9231,
     "n_kisa": 9231,
     "esit": true
    },
    "KT04": {
     "n_tam": 4804,
     "n_kisa": 4804,
     "esit": true
    },
    "KT05": {
     "n_tam": 9881,
     "n_kisa": 9881,
     "esit": true
    },
    "KT06": {
     "n_tam": 6582,
     "n_kisa": 6582,
     "esit": true
    },
    "KT07": {
     "n_tam": 66,
     "n_kisa": 66,
     "esit": true
    },
    "KT11": {
     "n_tam": 533,
     "n_kisa": 533,
     "esit": true
    },
    "KT12": {
     "n_tam": 728,
     "n_kisa": 728,
     "esit": true
    },
    "KT08": {
     "n_tam": 3902,
     "n_kisa": 3902,
     "esit": true
    },
    "KT09": {
     "n_tam": 53,
     "n_kisa": 53,
     "esit": true
    },
    "KT00": {
     "n_tam": 7731,
     "n_kisa": 7731,
     "esit": true
    },
    "KT13": {
     "n_tam": 7738,
     "n_kisa": 7738,
     "esit": true
    }
   },
   "tutar": true
  }
 },
 "ds_kopya": {
  "ABD": {
   "n": 200,
   "esit": 200,
   "durum_gunu": 43280
  },
  "AVR": {
   "n": 200,
   "esit": 200,
   "durum_gunu": 45085
  }
 },
 "sure_sn": {
  "ABD_tam": 1149,
  "ABD_kisa": 847,
  "AVR_tam": 332,
  "AVR_kisa": 137,
  "toplam": 2470
 }
}
```

## 10. Açık veri kuru koşusu (2001-2023; BİLİNEN VERİ, karar değil)

Çıktı: arastirma_cikti/kart2/acik/. Kesik 2023-12-31; KASA kapısı {'/tmp/kasa2/acik/V_ABD2.pkl': '2023-12-29', '/tmp/kasa2/acik/V_AVR2.pkl': '2023-12-29'}; çıktı en geç {'satir_en_gec_giris': '2023-12-29', 'olculen_son_giris': {'15': '2023-12-08', '30': '2023-11-16'}}; yeniden üretim TUTTU.

Huni:

```
{
 "ABD": {
  "sinyal_donem": {
   "Y1": {
    "acik_d1": 42719,
    "acik_d2": 63528,
    "acik_d3": 77774
   },
   "DS": {
    "acik_d1": 123511,
    "acik_d2": 286880,
    "acik_d3": 611421,
    "dis": 15525
   },
   "D9": {
    "acik_d1": 88880,
    "acik_d2": 126458,
    "acik_d3": 287099,
    "dis": 17204
   },
   "BOFA": {
    "acik_d1": 654,
    "acik_d2": 1271,
    "acik_d3": 4171,
    "dis": 70
   }
  },
  "olay": {
   "Y1": {
    "sinyal": 184021,
    "girdi": 184021,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 17,
    "giris_gec": 75,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 50712,
    "tekil": 76244,
    "y1_olay": 56973
   },
   "DS": {
    "girdi": 1037337,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 176,
    "giris_gec": 51,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 22372,
    "tekil": 0,
    "ds_gun": 1037337,
    "havuz_gun": 1014738,
    "ana": 94135,
    "F_KT08": 30674
   },
   "BOFA": {
    "kurulum": 6166,
    "girdi": 6166,
    "sembol_yok": 12,
    "sinyal_bar_gecersiz": 690,
    "giris_yok": 0,
    "giris_gec": 12,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 4077,
    "tekil": 0
   },
   "D9": {
    "c": 519641,
    "girdi": 519641,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 299,
    "giris_gec": 68,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 80831,
    "tekil": 0
   },
   "MOM_STREV": {
    "ay_sonu_aday": 711559,
    "p2": 443715,
    "KT00": 42855,
    "KT13": 44234
   }
  },
  "olcum": {
   "KT01|ABD|H15": {
    "olay": 56973,
    "tekil": 56973,
    "acik_tasan": 483,
    "essiz": 249,
    "olculdu": 56239,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 11025,
     "acik_d2": 18254,
     "acik_d3": 27694
    },
    "olculen_hucre": {
     "acik_d1": 10921,
     "acik_d2": 18142,
     "acik_d3": 27176
    }
   },
   "KT02|ABD|H15": {
    "olay": 2579,
    "tekil": 2579,
    "acik_tasan": 22,
    "essiz": 47,
    "olculdu": 2510,
    "olay_hucre": {
     "acik_d1": 425,
     "acik_d2": 599,
     "acik_d3": 1555
    },
    "olculen_hucre": {
     "acik_d1": 397,
     "acik_d2": 584,
     "acik_d3": 1529
    }
   },
   "KT03|ABD|H15": {
    "olay": 49674,
    "tekil": 49674,
    "acik_tasan": 455,
    "essiz": 217,
    "olculdu": 49000,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 9586,
     "acik_d2": 15734,
     "acik_d3": 24354
    },
    "olculen_hucre": {
     "acik_d1": 9493,
     "acik_d2": 15637,
     "acik_d3": 23870
    }
   },
   "KT04|ABD|H15": {
    "olay": 25110,
    "tekil": 25110,
    "acik_tasan": 281,
    "essiz": 114,
    "olculdu": 24713,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 5454,
     "acik_d2": 7053,
     "acik_d3": 12603
    },
    "olculen_hucre": {
     "acik_d1": 5402,
     "acik_d2": 7007,
     "acik_d3": 12304
    }
   },
   "KT05|ABD|H15": {
    "olay": 54253,
    "tekil": 54253,
    "acik_tasan": 475,
    "essiz": 235,
    "olculdu": 53541,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 10365,
     "acik_d2": 17318,
     "acik_d3": 26570
    },
    "olculen_hucre": {
     "acik_d1": 10266,
     "acik_d2": 17211,
     "acik_d3": 26064
    }
   },
   "KT06|ABD|H15": {
    "olay": 33506,
    "tekil": 33506,
    "acik_tasan": 299,
    "essiz": 138,
    "olculdu": 33068,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 6973,
     "acik_d2": 10807,
     "acik_d3": 15726
    },
    "olculen_hucre": {
     "acik_d1": 6906,
     "acik_d2": 10749,
     "acik_d3": 15413
    }
   },
   "KT07|ABD|H15": {
    "olay": 1088,
    "tekil": 1088,
    "acik_tasan": 11,
    "essiz": 14,
    "olculdu": 1063,
    "olay_hucre": {
     "acik_d1": 188,
     "acik_d2": 228,
     "acik_d3": 672
    },
    "olculen_hucre": {
     "acik_d1": 179,
     "acik_d2": 223,
     "acik_d3": 661
    }
   },
   "KT11|ABD|H15": {
    "olay": 3086,
    "tekil": 3086,
    "acik_tasan": 16,
    "essiz": 10,
    "olculdu": 3060,
    "olay_hucre": {
     "acik_d1": 582,
     "acik_d2": 943,
     "acik_d3": 1561
    },
    "olculen_hucre": {
     "acik_d1": 576,
     "acik_d2": 940,
     "acik_d3": 1544
    }
   },
   "KT12|ABD|H15": {
    "olay": 4847,
    "tekil": 4847,
    "acik_tasan": 47,
    "essiz": 33,
    "olculdu": 4767,
    "olay_hucre": {
     "acik_d1": 860,
     "acik_d2": 1373,
     "acik_d3": 2614
    },
    "olculen_hucre": {
     "acik_d1": 843,
     "acik_d2": 1361,
     "acik_d3": 2563
    }
   },
   "KT08|ABD|H15": {
    "olay": 30674,
    "tekil": 30674,
    "acik_tasan": 31,
    "essiz": 196,
    "olculdu": 30443,
    "olculemez": 4,
    "olay_hucre": {
     "acik_d1": 3875,
     "acik_d2": 8790,
     "acik_d3": 17601,
     "dis": 408
    },
    "olculen_hucre": {
     "acik_d1": 3770,
     "acik_d2": 8710,
     "acik_d3": 17558,
     "dis": 405
    }
   },
   "KT09|ABD|H15": {
    "olay": 1375,
    "tekil": 1375,
    "acik_tasan": 4,
    "essiz": 9,
    "olculdu": 1362,
    "olay_hucre": {
     "acik_d1": 140,
     "acik_d2": 246,
     "acik_d3": 973,
     "dis": 16
    },
    "olculen_hucre": {
     "acik_d1": 139,
     "acik_d2": 242,
     "acik_d3": 965,
     "dis": 16
    }
   },
   "KT10|ABD|H15": {
    "olay": 438443,
    "tekil": 44668,
    "acik_tasan": 331,
    "essiz": 1099,
    "olculdu": 43235,
    "olculemez": 3,
    "olay_hucre": {
     "acik_d1": 69967,
     "acik_d2": 104572,
     "acik_d3": 252506,
     "dis": 11398
    },
    "olculen_hucre": {
     "acik_d1": 7035,
     "acik_d2": 10842,
     "acik_d3": 24591,
     "dis": 767
    }
   },
   "KT00|ABD|H15": {
    "olay": 42855,
    "tekil": 42855,
    "essiz": 1842,
    "olculdu": 41012,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 7664,
     "acik_d2": 13560,
     "acik_d3": 21631
    },
    "olculen_hucre": {
     "acik_d1": 6989,
     "acik_d2": 12710,
     "acik_d3": 21313
    }
   },
   "KT13|ABD|H15": {
    "olay": 44234,
    "tekil": 44234,
    "essiz": 3178,
    "olculdu": 41055,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 7799,
     "acik_d2": 13729,
     "acik_d3": 22222,
     "dis": 484
    },
    "olculen_hucre": {
     "acik_d1": 6770,
     "acik_d2": 12349,
     "acik_d3": 21589,
     "dis": 347
    }
   },
   "KT01|ABD|H30": {
    "olay": 56973,
    "tekil": 56973,
    "acik_tasan": 772,
    "essiz": 248,
    "olculdu": 55951,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 11025,
     "acik_d2": 18254,
     "acik_d3": 27694
    },
    "olculen_hucre": {
     "acik_d1": 10921,
     "acik_d2": 18142,
     "acik_d3": 26888
    }
   },
   "KT02|ABD|H30": {
    "olay": 2579,
    "tekil": 2579,
    "acik_tasan": 51,
    "essiz": 47,
    "olculdu": 2481,
    "olay_hucre": {
     "acik_d1": 425,
     "acik_d2": 599,
     "acik_d3": 1555
    },
    "olculen_hucre": {
     "acik_d1": 397,
     "acik_d2": 584,
     "acik_d3": 1500
    }
   },
   "KT03|ABD|H30": {
    "olay": 49674,
    "tekil": 49674,
    "acik_tasan": 707,
    "essiz": 217,
    "olculdu": 48748,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 9586,
     "acik_d2": 15734,
     "acik_d3": 24354
    },
    "olculen_hucre": {
     "acik_d1": 9493,
     "acik_d2": 15637,
     "acik_d3": 23618
    }
   },
   "KT04|ABD|H30": {
    "olay": 25110,
    "tekil": 25110,
    "acik_tasan": 425,
    "essiz": 114,
    "olculdu": 24569,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 5454,
     "acik_d2": 7053,
     "acik_d3": 12603
    },
    "olculen_hucre": {
     "acik_d1": 5402,
     "acik_d2": 7007,
     "acik_d3": 12160
    }
   },
   "KT05|ABD|H30": {
    "olay": 54253,
    "tekil": 54253,
    "acik_tasan": 751,
    "essiz": 234,
    "olculdu": 53266,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 10365,
     "acik_d2": 17318,
     "acik_d3": 26570
    },
    "olculen_hucre": {
     "acik_d1": 10266,
     "acik_d2": 17211,
     "acik_d3": 25789
    }
   },
   "KT06|ABD|H30": {
    "olay": 33506,
    "tekil": 33506,
    "acik_tasan": 521,
    "essiz": 138,
    "olculdu": 32846,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 6973,
     "acik_d2": 10807,
     "acik_d3": 15726
    },
    "olculen_hucre": {
     "acik_d1": 6906,
     "acik_d2": 10749,
     "acik_d3": 15191
    }
   },
   "KT07|ABD|H30": {
    "olay": 1088,
    "tekil": 1088,
    "acik_tasan": 24,
    "essiz": 14,
    "olculdu": 1050,
    "olay_hucre": {
     "acik_d1": 188,
     "acik_d2": 228,
     "acik_d3": 672
    },
    "olculen_hucre": {
     "acik_d1": 179,
     "acik_d2": 223,
     "acik_d3": 648
    }
   },
   "KT11|ABD|H30": {
    "olay": 3086,
    "tekil": 3086,
    "acik_tasan": 56,
    "essiz": 10,
    "olculdu": 3020,
    "olay_hucre": {
     "acik_d1": 582,
     "acik_d2": 943,
     "acik_d3": 1561
    },
    "olculen_hucre": {
     "acik_d1": 576,
     "acik_d2": 940,
     "acik_d3": 1504
    }
   },
   "KT12|ABD|H30": {
    "olay": 4847,
    "tekil": 4847,
    "acik_tasan": 83,
    "essiz": 32,
    "olculdu": 4732,
    "olay_hucre": {
     "acik_d1": 860,
     "acik_d2": 1373,
     "acik_d3": 2614
    },
    "olculen_hucre": {
     "acik_d1": 843,
     "acik_d2": 1361,
     "acik_d3": 2528
    }
   },
   "KT08|ABD|H30": {
    "olay": 30674,
    "tekil": 25120,
    "acik_tasan": 77,
    "essiz": 164,
    "olculdu": 24875,
    "olculemez": 4,
    "olay_hucre": {
     "acik_d1": 3875,
     "acik_d2": 8790,
     "acik_d3": 17601,
     "dis": 408
    },
    "olculen_hucre": {
     "acik_d1": 3116,
     "acik_d2": 7165,
     "acik_d3": 14263,
     "dis": 331
    }
   },
   "KT09|ABD|H30": {
    "olay": 1375,
    "tekil": 1375,
    "acik_tasan": 14,
    "essiz": 9,
    "olculdu": 1352,
    "olay_hucre": {
     "acik_d1": 140,
     "acik_d2": 246,
     "acik_d3": 973,
     "dis": 16
    },
    "olculen_hucre": {
     "acik_d1": 139,
     "acik_d2": 242,
     "acik_d3": 955,
     "dis": 16
    }
   },
   "KT10|ABD|H30": {
    "olay": 438443,
    "tekil": 27570,
    "acik_tasan": 361,
    "essiz": 730,
    "olculdu": 26477,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 69967,
     "acik_d2": 104572,
     "acik_d3": 252506,
     "dis": 11398
    },
    "olculen_hucre": {
     "acik_d1": 4277,
     "acik_d2": 6806,
     "acik_d3": 14930,
     "dis": 464
    }
   },
   "KT00|ABD|H30": {
    "olay": 42855,
    "tekil": 25516,
    "acik_tasan": 169,
    "essiz": 1103,
    "olculdu": 24244,
    "olay_hucre": {
     "acik_d1": 7664,
     "acik_d2": 13560,
     "acik_d3": 21631
    },
    "olculen_hucre": {
     "acik_d1": 4181,
     "acik_d2": 7586,
     "acik_d3": 12477
    }
   },
   "KT13|ABD|H30": {
    "olay": 44234,
    "tekil": 38418,
    "acik_tasan": 252,
    "essiz": 2587,
    "olculdu": 35577,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 7799,
     "acik_d2": 13729,
     "acik_d3": 22222,
     "dis": 484
    },
    "olculen_hucre": {
     "acik_d1": 5959,
     "acik_d2": 10823,
     "acik_d3": 18483,
     "dis": 312
    }
   }
  }
 },
 "AVR": {
  "sinyal_donem": {
   "Y1": {
    "acik_d1": 8572,
    "acik_d2": 13673,
    "acik_d3": 14380
   },
   "DS": {
    "acik_d1": 23011,
    "acik_d2": 50534,
    "acik_d3": 53679,
    "dis": 2193
   },
   "D9": {},
   "BOFA": {
    "acik_d1": 66,
    "acik_d2": 73,
    "acik_d3": 35,
    "dis": 3
   }
  },
  "olay": {
   "Y1": {
    "sinyal": 36625,
    "girdi": 36625,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 2,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 9185,
    "tekil": 15754,
    "y1_olay": 11684
   },
   "DS": {
    "girdi": 129417,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 19,
    "giris_gec": 8,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 14244,
    "tekil": 0,
    "ds_gun": 129417,
    "havuz_gun": 115146,
    "ana": 11278,
    "F_KT08": 4462
   },
   "BOFA": {
    "kurulum": 177,
    "girdi": 177,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 11,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 107,
    "tekil": 0
   },
   "MOM_STREV": {
    "ay_sonu_aday": 121685,
    "p2": 86507,
    "KT00": 8533,
    "KT13": 8527
   }
  },
  "olcum": {
   "KT01|AVR|H15": {
    "olay": 11684,
    "tekil": 11684,
    "acik_tasan": 79,
    "essiz": 1218,
    "olculdu": 10380,
    "olculemez": 7,
    "olay_hucre": {
     "acik_d1": 2470,
     "acik_d2": 4047,
     "acik_d3": 5167
    },
    "olculen_hucre": {
     "acik_d1": 2029,
     "acik_d2": 3588,
     "acik_d3": 4763
    }
   },
   "KT02|AVR|H15": {
    "olay": 223,
    "tekil": 223,
    "acik_tasan": 1,
    "essiz": 39,
    "olculdu": 183,
    "olay_hucre": {
     "acik_d1": 32,
     "acik_d2": 87,
     "acik_d3": 104
    },
    "olculen_hucre": {
     "acik_d1": 19,
     "acik_d2": 71,
     "acik_d3": 93
    }
   },
   "KT03|AVR|H15": {
    "olay": 10203,
    "tekil": 10203,
    "acik_tasan": 72,
    "essiz": 1092,
    "olculdu": 9033,
    "olculemez": 6,
    "olay_hucre": {
     "acik_d1": 2173,
     "acik_d2": 3543,
     "acik_d3": 4487
    },
    "olculen_hucre": {
     "acik_d1": 1778,
     "acik_d2": 3131,
     "acik_d3": 4124
    }
   },
   "KT04|AVR|H15": {
    "olay": 5368,
    "tekil": 5368,
    "acik_tasan": 48,
    "essiz": 563,
    "olculdu": 4754,
    "olculemez": 3,
    "olay_hucre": {
     "acik_d1": 998,
     "acik_d2": 1809,
     "acik_d3": 2561
    },
    "olculen_hucre": {
     "acik_d1": 794,
     "acik_d2": 1602,
     "acik_d3": 2358
    }
   },
   "KT05|AVR|H15": {
    "olay": 10920,
    "tekil": 10920,
    "acik_tasan": 71,
    "essiz": 1120,
    "olculdu": 9722,
    "olculemez": 7,
    "olay_hucre": {
     "acik_d1": 2300,
     "acik_d2": 3798,
     "acik_d3": 4822
    },
    "olculen_hucre": {
     "acik_d1": 1883,
     "acik_d2": 3381,
     "acik_d3": 4458
    }
   },
   "KT06|AVR|H15": {
    "olay": 7253,
    "tekil": 7253,
    "acik_tasan": 39,
    "essiz": 725,
    "olculdu": 6486,
    "olculemez": 3,
    "olay_hucre": {
     "acik_d1": 1549,
     "acik_d2": 2523,
     "acik_d3": 3181
    },
    "olculen_hucre": {
     "acik_d1": 1278,
     "acik_d2": 2262,
     "acik_d3": 2946
    }
   },
   "KT07|AVR|H15": {
    "olay": 86,
    "tekil": 86,
    "acik_tasan": 1,
    "essiz": 14,
    "olculdu": 71,
    "olay_hucre": {
     "acik_d1": 7,
     "acik_d2": 32,
     "acik_d3": 47
    },
    "olculen_hucre": {
     "acik_d1": 5,
     "acik_d2": 25,
     "acik_d3": 41
    }
   },
   "KT11|AVR|H15": {
    "olay": 614,
    "tekil": 614,
    "essiz": 63,
    "olculdu": 551,
    "olay_hucre": {
     "acik_d1": 127,
     "acik_d2": 216,
     "acik_d3": 271
    },
    "olculen_hucre": {
     "acik_d1": 103,
     "acik_d2": 195,
     "acik_d3": 253
    }
   },
   "KT12|AVR|H15": {
    "olay": 856,
    "tekil": 856,
    "acik_tasan": 7,
    "essiz": 112,
    "olculdu": 737,
    "olay_hucre": {
     "acik_d1": 160,
     "acik_d2": 272,
     "acik_d3": 424
    },
    "olculen_hucre": {
     "acik_d1": 120,
     "acik_d2": 236,
     "acik_d3": 381
    }
   },
   "KT08|AVR|H15": {
    "olay": 4462,
    "tekil": 4462,
    "acik_tasan": 2,
    "essiz": 221,
    "olculdu": 4238,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 788,
     "acik_d2": 1660,
     "acik_d3": 1928,
     "dis": 86
    },
    "olculen_hucre": {
     "acik_d1": 726,
     "acik_d2": 1570,
     "acik_d3": 1867,
     "dis": 75
    }
   },
   "KT09|AVR|H15": {
    "olay": 59,
    "tekil": 59,
    "olculdu": 59,
    "olay_hucre": {
     "acik_d1": 17,
     "acik_d2": 21,
     "acik_d3": 20,
     "dis": 1
    },
    "olculen_hucre": {
     "acik_d1": 17,
     "acik_d2": 21,
     "acik_d3": 20,
     "dis": 1
    }
   },
   "KT00|AVR|H15": {
    "olay": 8533,
    "tekil": 8533,
    "essiz": 2067,
    "olculdu": 6457,
    "olculemez": 9,
    "olay_hucre": {
     "acik_d1": 1774,
     "acik_d2": 2871,
     "acik_d3": 3888
    },
    "olculen_hucre": {
     "acik_d1": 1149,
     "acik_d2": 2182,
     "acik_d3": 3126
    }
   },
   "KT13|AVR|H15": {
    "olay": 8527,
    "tekil": 8527,
    "essiz": 2762,
    "olculdu": 5758,
    "olculemez": 7,
    "olay_hucre": {
     "acik_d1": 1773,
     "acik_d2": 2808,
     "acik_d3": 3834,
     "dis": 112
    },
    "olculen_hucre": {
     "acik_d1": 1013,
     "acik_d2": 1816,
     "acik_d3": 2869,
     "dis": 60
    }
   },
   "KT01|AVR|H30": {
    "olay": 11684,
    "tekil": 11684,
    "acik_tasan": 119,
    "essiz": 1216,
    "olculdu": 10344,
    "olculemez": 5,
    "olay_hucre": {
     "acik_d1": 2470,
     "acik_d2": 4047,
     "acik_d3": 5167
    },
    "olculen_hucre": {
     "acik_d1": 2032,
     "acik_d2": 3587,
     "acik_d3": 4725
    }
   },
   "KT02|AVR|H30": {
    "olay": 223,
    "tekil": 223,
    "acik_tasan": 4,
    "essiz": 39,
    "olculdu": 180,
    "olay_hucre": {
     "acik_d1": 32,
     "acik_d2": 87,
     "acik_d3": 104
    },
    "olculen_hucre": {
     "acik_d1": 19,
     "acik_d2": 71,
     "acik_d3": 90
    }
   },
   "KT03|AVR|H30": {
    "olay": 10203,
    "tekil": 10203,
    "acik_tasan": 110,
    "essiz": 1091,
    "olculdu": 8998,
    "olculemez": 4,
    "olay_hucre": {
     "acik_d1": 2173,
     "acik_d2": 3543,
     "acik_d3": 4487
    },
    "olculen_hucre": {
     "acik_d1": 1780,
     "acik_d2": 3130,
     "acik_d3": 4088
    }
   },
   "KT04|AVR|H30": {
    "olay": 5368,
    "tekil": 5368,
    "acik_tasan": 69,
    "essiz": 563,
    "olculdu": 4734,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 998,
     "acik_d2": 1809,
     "acik_d3": 2561
    },
    "olculen_hucre": {
     "acik_d1": 795,
     "acik_d2": 1602,
     "acik_d3": 2337
    }
   },
   "KT05|AVR|H30": {
    "olay": 10920,
    "tekil": 10920,
    "acik_tasan": 107,
    "essiz": 1119,
    "olculdu": 9689,
    "olculemez": 5,
    "olay_hucre": {
     "acik_d1": 2300,
     "acik_d2": 3798,
     "acik_d3": 4822
    },
    "olculen_hucre": {
     "acik_d1": 1886,
     "acik_d2": 3380,
     "acik_d3": 4423
    }
   },
   "KT06|AVR|H30": {
    "olay": 7253,
    "tekil": 7253,
    "acik_tasan": 63,
    "essiz": 725,
    "olculdu": 6463,
    "olculemez": 2,
    "olay_hucre": {
     "acik_d1": 1549,
     "acik_d2": 2523,
     "acik_d3": 3181
    },
    "olculen_hucre": {
     "acik_d1": 1279,
     "acik_d2": 2262,
     "acik_d3": 2922
    }
   },
   "KT07|AVR|H30": {
    "olay": 86,
    "tekil": 86,
    "acik_tasan": 4,
    "essiz": 14,
    "olculdu": 68,
    "olay_hucre": {
     "acik_d1": 7,
     "acik_d2": 32,
     "acik_d3": 47
    },
    "olculen_hucre": {
     "acik_d1": 5,
     "acik_d2": 25,
     "acik_d3": 38
    }
   },
   "KT11|AVR|H30": {
    "olay": 614,
    "tekil": 614,
    "acik_tasan": 5,
    "essiz": 63,
    "olculdu": 546,
    "olay_hucre": {
     "acik_d1": 127,
     "acik_d2": 216,
     "acik_d3": 271
    },
    "olculen_hucre": {
     "acik_d1": 103,
     "acik_d2": 195,
     "acik_d3": 248
    }
   },
   "KT12|AVR|H30": {
    "olay": 856,
    "tekil": 856,
    "acik_tasan": 11,
    "essiz": 112,
    "olculdu": 733,
    "olay_hucre": {
     "acik_d1": 160,
     "acik_d2": 272,
     "acik_d3": 424
    },
    "olculen_hucre": {
     "acik_d1": 120,
     "acik_d2": 236,
     "acik_d3": 377
    }
   },
   "KT08|AVR|H30": {
    "olay": 4462,
    "tekil": 3692,
    "acik_tasan": 7,
    "essiz": 193,
    "olculdu": 3491,
    "olculemez": 1,
    "olay_hucre": {
     "acik_d1": 788,
     "acik_d2": 1660,
     "acik_d3": 1928,
     "dis": 86
    },
    "olculen_hucre": {
     "acik_d1": 589,
     "acik_d2": 1258,
     "acik_d3": 1587,
   
```

### acik_d1

| Kart | Yön | Pazar | H | n olay | n | bekleyen | FARK puan [boot %95] | [%98,33] | medyan | kırpılmış | SIRA [boot alt] | L3O + / - | p + / - | lik. üst n / FARK | lik. alt n / FARK | plasebo ort / pay+ / pay- / geçti | güç (+1) | TUT+ / TUT- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 7664 | 6989 | 0 | +0.12 [-0.45; +0.73] | [-0.58; +0.85] | -0.22 | -0.01 | 0.501 [0.484] | -0.11 / +0.36 | 0.3563 / 0.6438 | 3208 / +0.09 | 3781 / +0.13 | +0.01 / 0.01 / 0.00 / True | 1.00 | False / False |
| KT00 | + | ABD | 30 | 4572 | 4181 | 0 | +0.53 [-0.25; +1.30] | [-0.39; +1.52] | +0.07 | +0.36 | 0.509 [0.494] | +0.15 / +0.80 | 0.0884 / 0.9117 | 1907 / +0.38 | 2274 / +0.66 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT00 | + | AVR | 15 | 1774 | 1149 | 0 | +0.30 [-0.27; +0.92] | [-0.40; +1.07] | -0.09 | +0.25 | 0.508 [0.478] | +0.05 / +0.52 | 0.1628 / 0.8373 | 494 / +0.06 | 655 / +0.48 | -0.01 / 0.01 / 0.01 / True | 0.96 | False / False |
| KT00 | + | AVR | 30 | 1103 | 718 | 0 | +0.68 [-0.30; +1.61] | [-0.47; +1.89] | -0.14 | +0.59 | 0.514 [0.480] | +0.32 / +1.11 | 0.0876 / 0.9125 | 315 / +0.34 | 403 / +0.95 | +0.06 / 0.01 / 0.01 / True | 0.73 | False / False |
| KT01 | + | ABD | 15 | 11025 | 10921 | 0 | -0.11 [-0.26; +0.05] | [-0.29; +0.09] | -0.14 | -0.15 | 0.497 [0.491] | -0.17 / -0.03 | 0.8976 / 0.1025 | 5356 / -0.12 | 5565 / -0.10 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT01 | + | ABD | 30 | 11025 | 10921 | 0 | -0.20 [-0.42; +0.00] | [-0.46; +0.04] | -0.37 | -0.28 | 0.493 [0.487] | -0.27 / -0.12 | 0.9694 / 0.0307 | 5356 / -0.27 | 5565 / -0.14 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT01 | + | AVR | 15 | 2470 | 2029 | 0 | +0.13 [-0.09; +0.37] | [-0.14; +0.42] | -0.01 | +0.12 | 0.500 [0.487] | +0.03 / +0.20 | 0.1284 / 0.8717 | 1046 / +0.08 | 983 / +0.18 | -0.00 / 0.02 / 0.02 / True | 1.00 | False / False |
| KT01 | + | AVR | 30 | 2470 | 2032 | 0 | -0.02 [-0.29; +0.26] | [-0.35; +0.33] | -0.22 | +0.00 | 0.498 [0.486] | -0.14 / +0.08 | 0.5590 / 0.4411 | 1046 / -0.15 | 986 / +0.11 | -0.00 / 0.02 / 0.02 / True | 1.00 | False / False |
| KT02 | + | ABD | 15 | 425 | 397 | 0 | -0.60 [-1.70; +0.55] | [-2.02; +0.74] | -0.08 | -0.60 | 0.493 [0.458] | -1.12 / -0.07 | 0.8530 / 0.1471 | 166 / -0.57 | 231 / -0.62 | +0.01 / 0.01 / 0.00 / True | 0.64 | False / False |
| KT02 | + | ABD | 30 | 425 | 397 | 0 | -0.91 [-2.43; +0.58] | [-2.84; +0.85] | -0.40 | -0.84 | 0.494 [0.461] | -1.62 / -0.20 | 0.8748 / 0.1253 | 166 / -0.51 | 231 / -1.20 | -0.03 / 0.01 / 0.02 / True | 0.32 | False / False |
| KT02 | + | AVR | 15 | 32 | 19 | 0 | -1.33 [-4.09; +1.58] | [-4.68; +2.33] | -1.25 | -1.04 | 0.423 [0.294] | -2.97 / +0.90 | 0.7947 / 0.2055 | 9 / -1.66 | 10 / -1.02 | +0.02 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT02 | + | AVR | 30 | 32 | 19 | 0 | -0.61 [-4.86; +4.48] | [-6.10; +5.36] | +2.53 | -0.34 | 0.476 [0.327] | -2.94 / +3.53 | 0.5927 / 0.4075 | 9 / -1.89 | 10 / +0.55 | -0.16 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT03 | + | ABD | 15 | 9586 | 9493 | 0 | -0.05 [-0.23; +0.12] | [-0.26; +0.16] | -0.12 | -0.11 | 0.498 [0.492] | -0.12 / +0.03 | 0.7328 / 0.2673 | 4605 / -0.05 | 4888 / -0.06 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT03 | + | ABD | 30 | 9586 | 9493 | 0 | -0.16 [-0.39; +0.06] | [-0.44; +0.10] | -0.31 | -0.24 | 0.495 [0.489] | -0.23 / -0.07 | 0.9120 / 0.0881 | 4605 / -0.22 | 4888 / -0.10 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT03 | + | AVR | 15 | 2173 | 1778 | 0 | +0.14 [-0.12; +0.41] | [-0.19; +0.47] | -0.05 | +0.13 | 0.499 [0.485] | +0.01 / +0.24 | 0.1535 / 0.8466 | 916 / +0.14 | 862 / +0.14 | -0.01 / 0.01 / 0.01 / True | 0.99 | False / False |
| KT03 | + | AVR | 30 | 2173 | 1780 | 0 | -0.06 [-0.36; +0.28] | [-0.43; +0.34] | -0.27 | -0.04 | 0.497 [0.484] | -0.20 / +0.06 | 0.6463 / 0.3538 | 916 / -0.14 | 864 / +0.03 | -0.01 / 0.01 / 0.01 / True | 0.97 | False / False |
| KT04 | + | ABD | 15 | 5454 | 5402 | 0 | -0.06 [-0.30; +0.18] | [-0.34; +0.23] | -0.18 | -0.12 | 0.498 [0.490] | -0.13 / +0.05 | 0.6954 / 0.3047 | 2703 / -0.12 | 2699 / +0.01 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT04 | + | ABD | 30 | 5454 | 5402 | 0 | -0.11 [-0.39; +0.17] | [-0.45; +0.23] | -0.28 | -0.19 | 0.496 [0.489] | -0.20 / -0.01 | 0.7741 / 0.2260 | 2703 / -0.22 | 2699 / +0.00 | +0.01 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT04 | + | AVR | 15 | 998 | 794 | 0 | -0.11 [-0.49; +0.27] | [-0.57; +0.36] | -0.09 | -0.09 | 0.493 [0.472] | -0.24 / +0.04 | 0.7115 / 0.2886 | 345 / -0.32 | 449 / +0.04 | -0.00 / 0.01 / 0.03 / True | 0.90 | False / False |
| KT04 | + | AVR | 30 | 998 | 795 | 0 | -0.30 [-0.80; +0.18] | [-0.91; +0.31] | -0.43 | -0.24 | 0.489 [0.467] | -0.50 / -0.08 | 0.8826 / 0.1175 | 345 / -0.59 | 450 / -0.08 | -0.00 / 0.01 / 0.03 / True | 0.77 | False / False |
| KT05 | + | ABD | 15 | 10365 | 10266 | 0 | -0.13 [-0.30; +0.04] | [-0.34; +0.07] | -0.18 | -0.17 | 0.496 [0.490] | -0.19 / -0.04 | 0.9267 / 0.0734 | 5026 / -0.14 | 5240 / -0.12 | -0.01 / 0.02 / 0.04 / True | 1.00 | False / False |
| KT05 | + | ABD | 30 | 10365 | 10266 | 0 | -0.24 [-0.46; -0.01] | [-0.50; +0.03] | -0.39 | -0.31 | 0.492 [0.486] | -0.31 / -0.15 | 0.9823 / 0.0178 | 5026 / -0.30 | 5240 / -0.18 | -0.00 / 0.01 / 0.03 / True | 1.00 | False / True |
| KT05 | + | AVR | 15 | 2300 | 1883 | 0 | +0.12 [-0.13; +0.36] | [-0.19; +0.41] | -0.02 | +0.11 | 0.499 [0.486] | +0.01 / +0.20 | 0.1743 / 0.8258 | 961 / +0.09 | 922 / +0.15 | +0.01 / 0.02 / 0.00 / True | 1.00 | False / False |
| KT05 | + | AVR | 30 | 2300 | 1886 | 0 | -0.03 [-0.33; +0.26] | [-0.40; +0.33] | -0.23 | -0.01 | 0.498 [0.486] | -0.16 / +0.08 | 0.5867 / 0.4134 | 961 / -0.17 | 925 / +0.11 | +0.00 / 0.03 / 0.02 / True | 0.99 | False / False |
| KT06 | + | ABD | 15 | 6973 | 6906 | 0 | -0.21 [-0.40; -0.03] | [-0.44; +0.00] | -0.18 | -0.23 | 0.494 [0.488] | -0.29 / -0.13 | 0.9837 / 0.0164 | 3327 / -0.23 | 3579 / -0.20 | +0.02 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT06 | + | ABD | 30 | 6973 | 6906 | 0 | -0.28 [-0.55; +0.00] | [-0.62; +0.05] | -0.46 | -0.33 | 0.491 [0.482] | -0.38 / -0.17 | 0.9773 / 0.0228 | 3327 / -0.37 | 3579 / -0.19 | -0.00 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT06 | + | AVR | 15 | 1549 | 1278 | 0 | +0.14 [-0.16; +0.44] | [-0.20; +0.53] | +0.03 | +0.14 | 0.504 [0.487] | -0.01 / +0.25 | 0.1889 / 0.8112 | 636 / +0.05 | 642 / +0.22 | -0.03 / 0.01 / 0.01 / True | 0.97 | False / False |
| KT06 | + | AVR | 30 | 1549 | 1279 | 0 | +0.18 [-0.22; +0.60] | [-0.29; +0.67] | -0.09 | +0.20 | 0.506 [0.488] | -0.01 / +0.33 | 0.1822 / 0.8179 | 636 / +0.03 | 643 / +0.34 | -0.00 / 0.01 / 0.00 / True | 0.90 | False / False |
| KT07 | + | ABD | 15 | 188 | 179 | 0 | -0.23 [-1.75; +1.26] | [-2.16; +1.52] | -0.08 | -0.26 | 0.501 [0.450] | -0.99 / +0.58 | 0.6157 / 0.3844 | 70 / -0.77 | 109 / +0.12 | -0.02 / 0.01 / 0.02 / True | 0.34 | False / False |
| KT07 | + | ABD | 30 | 188 | 179 | 0 | -0.59 [-2.30; +1.11] | [-2.70; +1.55] | -0.17 | -0.59 | 0.495 [0.451] | -1.39 / +0.18 | 0.7537 / 0.2464 | 70 / -0.07 | 109 / -0.93 | +0.03 / 0.02 / 0.04 / True | 0.19 | False / False |
| KT07 | + | AVR | 15 | 7 | 5 | 0 | -1.29 [-9.59; +6.15] | [-12.11; +7.46] | -0.79 | +0.39 | 0.396 [0.067] | -10.72 / +7.88 | 0.6122 / 0.4178 | 3 / -5.23 | 2 / +4.61 | -0.46 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT07 | + | AVR | 30 | 7 | 5 | 0 | -2.26 [-11.85; +4.90] | [-13.43; +5.68] | +0.20 | +0.18 | 0.502 [0.200] | -11.82 / +6.08 | 0.5918 / 0.4389 | 3 / -5.18 | 2 / +2.12 | +0.72 / 0.00 / 0.00 / False | 0.00 | False / False |
| KT08 | - | ABD | 15 | 3875 | 3770 | 0 | +0.40 [-0.08; +0.87] | [-0.18; +0.96] | +0.20 | +0.18 | 0.503 [0.493] | +0.11 / +0.58 | 0.0579 / 0.9422 | 1756 / +0.64 | 2014 / +0.19 | +0.01 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT08 | - | ABD | 30 | 3203 | 3116 | 0 | +0.31 [-0.42; +1.02] | [-0.56; +1.16] | +0.04 | +0.10 | 0.507 [0.497] | -0.05 / +0.64 | 0.1997 / 0.8004 | 1439 / +0.85 | 1677 / -0.15 | +0.01 / 0.01 / 0.00 / True | 1.00 | False / False |
| KT08 | - | AVR | 15 | 788 | 726 | 0 | +0.50 [-0.41; +1.75] | [-0.58; +2.15] | +1.02 | +0.47 | 0.521 [0.492] | -0.09 / +1.18 | 0.1713 / 0.8288 | 360 / -0.39 | 366 / +1.37 | -0.03 / 0.01 / 0.03 / True | 0.88 | False / False |
| KT08 | - | AVR | 30 | 643 | 589 | 0 | +0.20 [-1.05; +1.48] | [-1.28; +1.89] | +0.68 | +0.14 | 0.512 [0.484] | -0.52 / +0.86 | 0.3706 / 0.6295 | 288 / -0.30 | 301 / +0.67 | -0.03 / 0.01 / 0.01 / True | 0.66 | False / False |
| KT09 | + | ABD | 15 | 140 | 139 | 0 | -0.29 [-4.95; +4.77] | [-5.75; +6.00] | -3.84 | -0.84 | 0.463 [0.405] | -3.37 / +2.41 | 0.5499 / 0.4502 | 61 / -2.59 | 78 / +1.50 | +0.05 / 0.01 / 0.01 / True | 0.27 | False / False |
| KT09 | + | ABD | 30 | 140 | 139 | 0 | -1.53 [-7.50; +5.17] | [-8.67; +7.38] | -1.68 | -2.39 | 0.453 [0.394] | -5.73 / +2.33 | 0.6742 / 0.3259 | 61 / -6.28 | 78 / +2.19 | -0.03 / 0.03 / 0.03 / True | 0.17 | False / False |
| KT09 | + | AVR | 15 | 17 | 17 | 0 | +2.50 [-6.85; +12.16] | [-8.36; +13.89] | +0.53 | +0.66 | 0.532 [0.353] | -5.89 / +9.05 | 0.3348 / 0.6656 | 7 / -3.80 | 10 / +6.91 | +0.11 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT09 | + | AVR | 30 | 17 | 17 | 0 | +7.13 [-6.64; +21.94] | [-8.58; +25.13] | -0.48 | +4.18 | 0.505 [0.312] | -6.52 / +14.56 | 0.2057 / 0.7945 | 7 / -2.01 | 10 / +13.53 | +0.12 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT10 | + | ABD | 15 | 7223 | 7035 | 0 | -0.07 [-0.37; +0.23] | [-0.44; +0.29] | -0.14 | -0.20 | 0.498 [0.488] | -0.17 / +0.07 | 0.6714 / 0.3287 | 4332 / -0.19 | 2703 / +0.11 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT10 | + | ABD | 30 | 4389 | 4277 | 0 | -0.03 [-0.54; +0.47] | [-0.65; +0.56] | -0.24 | -0.24 | 0.500 [0.487] | -0.21 / +0.19 | 0.5440 / 0.4561 | 2623 / -0.28 | 1654 / +0.37 | +0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT11 | + | ABD | 15 | 582 | 576 | 0 | -0.37 [-1.09; +0.21] | [-1.21; +0.35] | -0.12 | -0.27 | 0.494 [0.471] | -0.65 / -0.01 | 0.8756 / 0.1245 | 301 / -0.02 | 275 / -0.76 | +0.03 / 0.03 / 0.03 / True | 0.84 | False / False |
| KT11 | + | ABD | 30 | 582 | 576 | 0 | -0.74 [-1.77; +0.17] | [-2.01; +0.38] | -0.80 | -0.68 | 0.488 [0.464] | -1.31 / -0.22 | 0.9239 / 0.0762 | 301 / -0.28 | 275 / -1.24 | +0.06 / 0.01 / 0.00 / True | 0.45 | False / False |
| KT11 | + | AVR | 15 | 127 | 103 | 0 | +0.99 [-0.05; +2.01] | [-0.34; +2.30] | +0.69 | +0.93 | 0.544 [0.474] | +0.41 / +1.49 | 0.0370 / 0.9631 | 58 / +1.12 | 45 / +0.81 | +0.05 / 0.01 / 0.01 / True | 0.31 | False / False |
| KT11 | + | AVR | 30 | 127 | 103 | 0 | +0.15 [-1.20; +1.53] | [-1.51; +1.89] | -0.87 | +0.13 | 0.498 [0.439] | -0.68 / +0.78 | 0.4155 / 0.5846 | 58 / +0.60 | 45 / -0.43 | +0.09 / 0.03 / 0.01 / True | 0.23 | False / False |
| KT12 | + | ABD | 15 | 860 | 843 | 0 | -0.46 [-1.08; +0.27] | [-1.18; +0.45] | -0.48 | -0.64 | 0.481 [0.461] | -0.86 / -0.28 | 0.9011 / 0.0990 | 404 / -0.62 | 439 / -0.32 | -0.02 / 0.01 / 0.02 / True | 0.93 | False / False |
| KT12 | + | ABD | 30 | 860 | 843 | 0 | -0.37 [-1.07; +0.34] | [-1.21; +0.49] | -0.86 | -0.41 | 0.488 [0.468] | -0.70 / -0.14 | 0.8515 / 0.1486 | 404 / -0.23 | 439 / -0.49 | -0.02 / 0.01 / 0.02 / True | 0.71 | False / False |
| KT12 | + | AVR | 15 | 160 | 120 | 0 | +0.48 [-0.70; +1.65] | [-1.07; +1.95] | +0.17 | +0.46 | 0.506 [0.450] | -0.02 / +1.08 | 0.2117 / 0.7884 | 69 / +0.92 | 51 / -0.11 | +0.04 / 0.05 / 0.01 / True | 0.35 | False / False |
| KT12 | + | AVR | 30 | 160 | 120 | 0 | +0.74 [-0.80; +2.33] | [-1.17; +2.63] | -0.13 | +0.79 | 0.512 [0.453] | +0.13 / +1.59 | 0.1777 / 0.8224 | 69 / +1.34 | 51 / -0.07 | -0.04 / 0.03 / 0.01 / True | 0.28 | False / False |
| KT13 | + | ABD | 15 | 7799 | 6770 | 0 | +0.40 [-0.16; +0.98] | [-0.30; +1.11] | -0.04 | +0.23 | 0.504 [0.489] | +0.09 / +0.58 | 0.0906 / 0.9095 | 3234 / +0.43 | 3536 / +0.38 | +0.00 / 0.01 / 0.00 / True | 1.00 | False / False |
| KT13 | + | ABD | 30 | 6795 | 5959 | 0 | +0.49 [-0.21; +1.19] | [-0.38; +1.35] | -0.33 | +0.27 | 0.502 [0.488] | +0.15 / +0.72 | 0.0844 / 0.9157 | 2849 / +0.45 | 3110 / +0.52 | -0.02 / 0.01 / 0.02 / True | 1.00 | False / False |
| KT13 | + | AVR | 15 | 1773 | 1013 | 0 | +0.11 [-0.83; +1.12] | [-1.07; +1.34] | -0.28 | -0.04 | 0.489 [0.458] | -0.41 / +0.45 | 0.4075 / 0.5926 | 561 / -0.02 | 452 / +0.27 | -0.00 / 0.03 / 0.04 / True | 0.95 | False / False |
| KT13 | + | AVR | 30 | 1543 | 907 | 0 | -0.19 [-1.53; +1.16] | [-1.75; +1.50] | -0.49 | -0.33 | 0.479 [0.446] | -0.91 / +0.36 | 0.5991 / 0.4010 | 500 / -0.70 | 407 / +0.43 | -0.03 / 0.02 / 0.04 / True | 0.81 | False / False |

### acik_d2

| Kart | Yön | Pazar | H | n olay | n | bekleyen | FARK puan [boot %95] | [%98,33] | medyan | kırpılmış | SIRA [boot alt] | L3O + / - | p + / - | lik. üst n / FARK | lik. alt n / FARK | plasebo ort / pay+ / pay- / geçti | güç (+1) | TUT+ / TUT- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 13560 | 12710 | 0 | +0.07 [-0.42; +0.56] | [-0.51; +0.66] | -0.02 | +0.01 | 0.506 [0.492] | -0.12 / +0.25 | 0.3894 / 0.6107 | 5915 / +0.23 | 6795 / -0.07 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT00 | + | ABD | 30 | 8105 | 7586 | 0 | +0.08 [-0.60; +0.77] | [-0.75; +0.89] | -0.13 | -0.10 | 0.504 [0.489] | -0.16 / +0.36 | 0.4167 / 0.5834 | 3468 / +0.26 | 4118 / -0.07 | +0.00 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT00 | + | AVR | 15 | 2871 | 2182 | 0 | +0.45 [-0.02; +0.91] | [-0.13; +1.04] | +0.09 | +0.39 | 0.517 [0.496] | +0.25 / +0.65 | 0.0310 / 0.9691 | 1008 / +0.06 | 1174 / +0.79 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT00 | + | AVR | 30 | 1788 | 1372 | 0 | +0.59 [-0.07; +1.26] | [-0.23; +1.38] | +0.65 | +0.54 | 0.524 [0.502] | +0.35 / +0.95 | 0.0455 / 0.9546 | 644 / +0.38 | 728 / +0.78 | -0.01 / 0.01 / 0.01 / True | 0.97 | False / False |
| KT01 | + | ABD | 15 | 18254 | 18142 | 0 | +0.03 [-0.09; +0.15] | [-0.11; +0.17] | -0.07 | -0.02 | 0.500 [0.495] | -0.02 / +0.07 | 0.3208 / 0.6793 | 9149 / -0.04 | 8993 / +0.10 | -0.00 / 0.01 / 0.02 / True | 1.00 | False / False |
| KT01 | + | ABD | 30 | 18254 | 18142 | 0 | +0.04 [-0.14; +0.22] | [-0.17; +0.25] | -0.20 | -0.06 | 0.499 [0.493] | -0.02 / +0.12 | 0.3078 / 0.6923 | 9149 / -0.06 | 8993 / +0.15 | -0.00 / 0.02 / 0.03 / True | 1.00 | False / False |
| KT01 | + | AVR | 15 | 4047 | 3588 | 0 | -0.06 [-0.28; +0.16] | [-0.33; +0.22] | -0.03 | +0.00 | 0.501 [0.489] | -0.16 / +0.05 | 0.6795 / 0.3206 | 1750 / -0.18 | 1838 / +0.07 | -0.00 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT01 | + | AVR | 30 | 4047 | 3587 | 0 | +0.03 [-0.32; +0.33] | [-0.39; +0.40] | -0.03 | +0.04 | 0.501 [0.488] | -0.11 / +0.18 | 0.4252 / 0.5749 | 1749 / -0.19 | 1838 / +0.25 | -0.01 / 0.01 / 0.02 / True | 0.99 | False / False |
| KT02 | + | ABD | 15 | 599 | 584 | 0 | -0.05 [-0.88; +0.77] | [-1.03; +0.92] | -0.88 | -0.05 | 0.485 [0.459] | -0.37 / +0.34 | 0.5502 / 0.4499 | 221 / +0.75 | 363 / -0.54 | -0.04 / 0.01 / 0.02 / True | 0.81 | False / False |
| KT02 | + | ABD | 30 | 599 | 584 | 0 | -0.52 [-1.63; +0.71] | [-1.90; +0.98] | -1.06 | -0.46 | 0.486 [0.463] | -1.08 / +0.07 | 0.8007 / 0.1994 | 221 / -0.49 | 363 / -0.54 | +0.01 / 0.01 / 0.02 / True | 0.44 | False / False |
| KT02 | + | AVR | 15 | 87 | 71 | 0 | -1.00 [-3.27; +1.59] | [-3.80; +2.32] | +0.75 | -0.61 | 0.519 [0.463] | -1.93 / +1.20 | 0.7509 / 0.2492 | 25 / -2.35 | 46 / -0.27 | -0.18 / 0.02 / 0.02 / True | 0.15 | False / False |
| KT02 | + | AVR | 30 | 87 | 71 | 0 | -0.39 [-2.71; +2.00] | [-3.36; +2.47] | +0.64 | -0.26 | 0.526 [0.457] | -1.36 / +1.42 | 0.6195 / 0.3806 | 25 / -1.71 | 46 / +0.32 | -0.18 / 0.01 / 0.02 / True | 0.15 | False / False |
| KT03 | + | ABD | 15 | 15734 | 15637 | 0 | +0.01 [-0.11; +0.14] | [-0.13; +0.16] | -0.08 | -0.04 | 0.500 [0.494] | -0.04 / +0.05 | 0.4245 / 0.5756 | 7824 / -0.05 | 7813 / +0.08 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT03 | + | ABD | 30 | 15734 | 15637 | 0 | +0.02 [-0.17; +0.22] | [-0.21; +0.27] | -0.23 | -0.08 | 0.498 [0.492] | -0.05 / +0.10 | 0.4157 / 0.5844 | 7824 / -0.09 | 7813 / +0.14 | -0.00 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT03 | + | AVR | 15 | 3543 | 3131 | 0 | -0.12 [-0.36; +0.10] | [-0.43; +0.16] | -0.08 | -0.06 | 0.498 [0.485] | -0.22 / -0.01 | 0.8503 / 0.1498 | 1514 / -0.22 | 1617 / -0.03 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT03 | + | AVR | 30 | 3543 | 3130 | 0 | -0.07 [-0.45; +0.26] | [-0.52; +0.33] | -0.14 | -0.05 | 0.496 [0.482] | -0.20 / +0.09 | 0.6504 / 0.3497 | 1513 / -0.24 | 1617 / +0.10 | -0.01 / 0.03 / 0.03 / True | 0.99 | False / False |
| KT04 | + | ABD | 15 | 7053 | 7007 | 0 | -0.02 [-0.16; +0.13] | [-0.19; +0.16] | -0.03 | -0.07 | 0.502 [0.495] | -0.07 / +0.04 | 0.5928 / 0.4073 | 3793 / -0.10 | 3214 / +0.08 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT04 | + | ABD | 30 | 7053 | 7007 | 0 | -0.05 [-0.31; +0.20] | [-0.36; +0.25] | -0.15 | -0.15 | 0.496 [0.489] | -0.14 / +0.05 | 0.6633 / 0.3368 | 3793 / -0.16 | 3214 / +0.07 | -0.01 / 0.00 / 0.01 / True | 1.00 | False / False |
| KT04 | + | AVR | 15 | 1809 | 1602 | 0 | -0.13 [-0.42; +0.14] | [-0.50; +0.19] | +0.12 | -0.02 | 0.500 [0.483] | -0.23 / -0.01 | 0.8238 / 0.1763 | 782 / -0.13 | 820 / -0.13 | +0.00 / 0.01 / 0.02 / True | 1.00 | False / False |
| KT04 | + | AVR | 30 | 1809 | 1602 | 0 | -0.11 [-0.57; +0.37] | [-0.69; +0.46] | -0.13 | -0.04 | 0.498 [0.482] | -0.32 / +0.13 | 0.6678 / 0.3323 | 782 / -0.27 | 820 / +0.05 | -0.01 / 0.00 / 0.01 / True | 0.97 | False / False |
| KT05 | + | ABD | 15 | 17318 | 17211 | 0 | +0.03 [-0.08; +0.15] | [-0.11; +0.17] | -0.07 | -0.02 | 0.500 [0.495] | -0.02 / +0.07 | 0.3251 / 0.6750 | 8697 / -0.05 | 8514 / +0.11 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT05 | + | ABD | 30 | 17318 | 17211 | 0 | +0.05 [-0.13; +0.24] | [-0.16; +0.29] | -0.18 | -0.06 | 0.499 [0.493] | -0.02 / +0.13 | 0.2965 / 0.7036 | 8697 / -0.06 | 8514 / +0.16 | -0.00 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT05 | + | AVR | 15 | 3798 | 3381 | 0 | -0.08 [-0.32; +0.16] | [-0.37; +0.20] | -0.04 | -0.02 | 0.500 [0.488] | -0.19 / +0.03 | 0.7256 / 0.2745 | 1651 / -0.14 | 1730 / -0.02 | +0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT05 | + | AVR | 30 | 3798 | 3380 | 0 | +0.01 [-0.35; +0.34] | [-0.43; +0.41] | -0.04 | +0.02 | 0.500 [0.486] | -0.15 / +0.16 | 0.4765 / 0.5236 | 1650 / -0.16 | 1730 / +0.17 | -0.01 / 0.01 / 0.03 / True | 0.99 | False / False |
| KT06 | + | ABD | 15 | 10807 | 10749 | 0 | -0.03 [-0.17; +0.11] | [-0.19; +0.14] | -0.14 | -0.07 | 0.499 [0.492] | -0.08 / +0.01 | 0.6613 / 0.3388 | 5398 / -0.00 | 5351 / -0.05 | -0.00 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT06 | + | ABD | 30 | 10807 | 10749 | 0 | +0.04 [-0.15; +0.25] | [-0.19; +0.30] | -0.15 | -0.05 | 0.499 [0.493] | -0.03 / +0.11 | 0.3457 / 0.6544 | 5398 / +0.07 | 5351 / +0.01 | -0.01 / 0.02 / 0.04 / True | 1.00 | False / False |
| KT06 | + | AVR | 15 | 2523 | 2262 | 0 | +0.01 [-0.32; +0.32] | [-0.41; +0.38] | +0.09 | +0.07 | 0.508 [0.491] | -0.14 / +0.17 | 0.4707 / 0.5294 | 1072 / -0.03 | 1190 / +0.05 | -0.00 / 0.00 / 0.01 / True | 1.00 | False / False |
| KT06 | + | AVR | 30 | 2523 | 2262 | 0 | +0.06 [-0.39; +0.46] | [-0.49; +0.56] | -0.00 | +0.08 | 0.501 [0.484] | -0.13 / +0.23 | 0.3863 / 0.6138 | 1072 / -0.12 | 1190 / +0.22 | -0.03 / 0.00 / 0.01 / True | 0.98 | False / False |
| KT07 | + | ABD | 15 | 228 | 223 | 0 | -0.31 [-1.70; +1.05] | [-2.08; +1.31] | -0.76 | -0.15 | 0.488 [0.447] | -0.91 / +0.38 | 0.6843 / 0.3158 | 83 / +1.25 | 140 / -1.23 | +0.04 / 0.01 / 0.01 / True | 0.40 | False / False |
| KT07 | + | ABD | 30 | 228 | 223 | 0 | -1.27 [-3.32; +0.96] | [-3.82; +1.45] | -1.36 | -1.04 | 0.477 [0.429] | -2.38 / -0.21 | 0.8616 / 0.1385 | 83 / -0.39 | 140 / -1.80 | +0.00 / 0.01 / 0.02 / True | 0.30 | False / False |
| KT07 | + | AVR | 15 | 32 | 25 | 0 | +0.51 [-2.61; +3.72] | [-3.34; +4.25] | +1.84 | +0.80 | 0.569 [0.457] | -0.78 / +3.40 | 0.3784 / 0.6217 | 12 / +0.93 | 13 / +0.12 | -0.08 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT07 | + | AVR | 30 | 32 | 25 | 0 | -1.72 [-6.81; +3.30] | [-7.86; +4.08] | +0.64 | -1.34 | 0.514 [0.360] | -4.62 / +2.48 | 0.7378 / 0.2623 | 12 / -1.37 | 13 / -2.04 | -0.13 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT08 | - | ABD | 15 | 8790 | 8710 | 0 | +0.28 [-0.07; +0.62] | [-0.18; +0.69] | +0.07 | +0.14 | 0.507 [0.500] | +0.06 / +0.44 | 0.0686 / 0.9315 | 3902 / +0.32 | 4808 / +0.24 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT08 | - | ABD | 30 | 7233 | 7165 | 0 | +0.40 [-0.15; +0.84] | [-0.27; +0.93] | +0.11 | +0.18 | 0.508 [0.499] | +0.05 / +0.60 | 0.0873 / 0.9128 | 3211 / +0.44 | 3954 / +0.37 | -0.01 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT08 | - | AVR | 15 | 1660 | 1570 | 0 | +0.39 [-0.37; +1.03] | [-0.52; +1.20] | +0.17 | +0.27 | 0.507 [0.488] | -0.05 / +0.70 | 0.1572 / 0.8429 | 798 / -0.14 | 772 / +0.94 | -0.04 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT08 | - | AVR | 30 | 1339 | 1258 | 0 | +0.65 [-0.76; +1.90] | [-0.99; +2.16] | +0.14 | +0.37 | 0.505 [0.478] | -0.36 / +1.33 | 0.2012 / 0.7989 | 639 / -0.12 | 619 / +1.43 | -0.02 / 0.01 / 0.01 / True | 0.97 | False / False |
| KT09 | + | ABD | 15 | 246 | 242 | 0 | +1.71 [-3.24; +6.98] | [-3.92; +8.02] | -1.18 | +1.09 | 0.491 [0.408] | -2.15 / +4.19 | 0.3257 / 0.6744 | 93 / +2.83 | 149 / +1.01 | -0.03 / 0.03 / 0.04 / True | 0.42 | False / False |
| KT09 | + | ABD | 30 | 246 | 242 | 0 | +5.35 [-5.30; +16.55] | [-7.16; +19.08] | +3.09 | +3.71 | 0.525 [0.435] | -3.82 / +8.31 | 0.3154 / 0.6847 | 93 / +6.78 | 149 / +4.46 | -0.03 / 0.01 / 0.03 / True | 0.31 | False / False |
| KT09 | + | AVR | 15 | 21 | 21 | 0 | +2.88 [-3.63; +13.34] | [-4.11; +15.61] | +2.10 | +2.69 | 0.548 [0.410] | -3.45 / +12.24 | 0.4216 / 0.5824 | 6 / +3.79 | 15 / +2.52 | -0.05 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT09 | + | AVR | 30 | 21 | 21 | 0 | +1.72 [-9.69; +16.05] | [-11.34; +18.27] | -3.68 | +1.00 | 0.482 [0.314] | -6.89 / +11.97 | 0.3215 / 0.6826 | 6 / +1.74 | 15 / +1.71 | -0.18 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT10 | + | ABD | 15 | 11086 | 10842 | 0 | +0.11 [-0.22; +0.45] | [-0.27; +0.53] | -0.04 | +0.04 | 0.505 [0.495] | -0.04 / +0.23 | 0.2491 / 0.7510 | 7144 / -0.10 | 3698 / +0.52 | +0.00 / 0.01 / 0.02 / True | 1.00 | False / False |
| KT10 | + | ABD | 30 | 6965 | 6806 | 0 | +0.24 [-0.26; +0.75] | [-0.36; +0.88] | +0.14 | +0.11 | 0.507 [0.494] | +0.01 / +0.43 | 0.1766 / 0.8235 | 4455 / -0.08 | 2351 / +0.86 | -0.00 / 0.02 / 0.04 / True | 1.00 | False / False |
| KT11 | + | ABD | 15 | 943 | 940 | 0 | +0.53 [-0.10; +1.19] | [-0.24; +1.32] | +0.30 | +0.42 | 0.518 [0.491] | +0.22 / +0.85 | 0.0495 / 0.9506 | 466 / +0.20 | 474 / +0.85 | +0.02 / 0.01 / 0.01 / True | 0.93 | False / False |
| KT11 | + | ABD | 30 | 943 | 940 | 0 | +0.68 [-0.13; +1.50] | [-0.25; +1.74] | +0.59 | +0.47 | 0.513 [0.489] | +0.27 / +1.07 | 0.0515 / 0.9486 | 466 / +0.42 | 474 / +0.93 | +0.04 / 0.01 / 0.01 / True | 0.65 | False / False |
| KT11 | + | AVR | 15 | 216 | 195 | 0 | +0.45 [-0.18; +1.10] | [-0.31; +1.27] | +0.15 | +0.40 | 0.510 [0.474] | +0.14 / +0.76 | 0.0861 / 0.9140 | 103 / -0.08 | 92 / +1.04 | +0.04 / 0.02 / 0.02 / True | 0.59 | False / False |
| KT11 | + | AVR | 30 | 216 | 195 | 0 | +0.53 [-0.49; +1.46] | [-0.69; +1.68] | +0.30 | +0.58 | 0.526 [0.473] | -0.04 / +0.89 | 0.1699 / 0.8302 | 103 / +0.37 | 92 / +0.71 | +0.03 / 0.04 / 0.01 / True | 0.22 | False / False |
| KT12 | + | ABD | 15 | 1373 | 1361 | 0 | +0.33 [-0.12; +0.85] | [-0.21; +0.97] | +0.14 | +0.29 | 0.511 [0.495] | +0.15 / +0.51 | 0.0874 / 0.9127 | 609 / +0.29 | 752 / +0.37 | +0.00 / 0.01 / 0.01 / True | 0.97 | False / False |
| KT12 | + | ABD | 30 | 1373 | 1361 | 0 | +0.22 [-0.37; +0.88] | [-0.50; +0.99] | +0.40 | +0.21 | 0.507 [0.489] | -0.05 / +0.43 | 0.2301 / 0.7700 | 609 / +0.31 | 752 / +0.15 | +0.00 / 0.01 / 0.01 / True | 0.81 | False / False |
| KT12 | + | AVR | 15 | 272 | 236 | 0 | -1.16 [-2.51; +0.01] | [-2.94; +0.21] | -1.20 | -0.78 | 0.460 [0.411] | -1.86 / -0.41 | 0.9707 / 0.0294 | 115 / -0.87 | 121 / -1.44 | +0.03 / 0.03 / 0.01 / True | 0.63 | False / False |
| KT12 | + | AVR | 30 | 272 | 236 | 0 | -1.14 [-2.50; +0.04] | [-2.80; +0.24] | -0.81 | -0.71 | 0.473 [0.433] | -1.69 / -0.42 | 0.9661 / 0.0340 | 115 / -0.80 | 121 / -1.46 | +0.01 / 0.02 / 0.03 / True | 0.30 | False / False |
| KT13 | + | ABD | 15 | 13729 | 12349 | 0 | +0.18 [-0.28; +0.61] | [-0.35; +0.70] | -0.06 | +0.08 | 0.501 [0.489] | +0.01 / +0.37 | 0.2166 / 0.7835 | 5327 / -0.21 | 7022 / +0.47 | -0.00 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT13 | + | ABD | 30 | 11916 | 10823 | 0 | +0.17 [-0.42; +0.77] | [-0.56; +0.90] | -0.24 | -0.06 | 0.501 [0.489] | -0.10 / +0.43 | 0.2950 / 0.7051 | 4707 / -0.30 | 6116 / +0.52 | +0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT13 | + | AVR | 15 | 2808 | 1816 | 0 | -0.71 [-1.38; -0.02] | [-1.55; +0.11] | -0.43 | -0.65 | 0.481 [0.459] | -0.98 / -0.37 | 0.9760 / 0.0241 | 963 / -1.32 | 853 / -0.03 | -0.00 / 0.03 / 0.01 / True | 1.00 | False / False |
| KT13 | + | AVR | 30 | 2456 | 1608 | 0 | -0.57 [-1.47; +0.26] | [-1.65; +0.46] | -0.20 | -0.57 | 0.488 [0.464] | -0.95 / -0.15 | 0.9037 / 0.0964 | 852 / -0.99 | 756 / -0.10 | +0.00 / 0.02 / 0.01 / True | 0.97 | False / False |

### acik_d3

| Kart | Yön | Pazar | H | n olay | n | bekleyen | FARK puan [boot %95] | [%98,33] | medyan | kırpılmış | SIRA [boot alt] | L3O + / - | p + / - | lik. üst n / FARK | lik. alt n / FARK | plasebo ort / pay+ / pay- / geçti | güç (+1) | TUT+ / TUT- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 21631 | 21313 | 0 | +0.18 [-0.40; +0.74] | [-0.57; +0.90] | -0.54 | -0.19 | 0.496 [0.480] | -0.12 / +0.38 | 0.2723 / 0.7278 | 10476 / +0.05 | 10837 / +0.30 | +0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT00 | + | ABD | 30 | 12839 | 12477 | 0 | +0.47 [-0.48; +1.55] | [-0.75; +1.78] | -1.02 | -0.21 | 0.495 [0.480] | -0.06 / +0.75 | 0.1693 / 0.8308 | 6058 / -0.08 | 6419 / +0.99 | +0.00 / 0.03 / 0.02 / True | 1.00 | False / False |
| KT00 | + | AVR | 15 | 3888 | 3126 | 0 | -0.09 [-0.55; +0.38] | [-0.66; +0.47] | -0.24 | -0.13 | 0.492 [0.472] | -0.26 / +0.13 | 0.6489 / 0.3512 | 1457 / -0.24 | 1669 / +0.04 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT00 | + | AVR | 30 | 2384 | 1896 | 0 | -0.49 [-1.30; +0.31] | [-1.44; +0.42] | -0.62 | -0.57 | 0.482 [0.457] | -0.80 / -0.11 | 0.8881 / 0.1120 | 880 / -0.53 | 1016 / -0.45 | +0.01 / 0.01 / 0.02 / True | 0.99 | False / False |
| KT01 | + | ABD | 15 | 27694 | 27176 | 0 | -0.23 [-0.38; -0.07] | [-0.41; -0.03] | -0.28 | -0.30 | 0.491 [0.486] | -0.29 / -0.14 | 0.9972 / 0.0029 | 14088 / -0.20 | 13088 / -0.26 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / True |
| KT01 | + | ABD | 30 | 27694 | 26888 | 0 | -0.24 [-0.45; -0.01] | [-0.50; +0.04] | -0.49 | -0.39 | 0.491 [0.486] | -0.34 / -0.14 | 0.9814 / 0.0187 | 13950 / -0.15 | 12938 / -0.34 | -0.01 / 0.00 / 0.01 / True | 1.00 | False / True |
| KT01 | + | AVR | 15 | 5167 | 4763 | 0 | -0.02 [-0.22; +0.20] | [-0.26; +0.25] | -0.11 | -0.04 | 0.496 [0.486] | -0.11 / +0.06 | 0.5778 / 0.4223 | 2445 / -0.02 | 2318 / -0.02 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT01 | + | AVR | 30 | 5167 | 4725 | 0 | -0.08 [-0.40; +0.25] | [-0.47; +0.32] | -0.15 | -0.10 | 0.497 [0.485] | -0.23 / +0.04 | 0.6912 / 0.3089 | 2419 / -0.15 | 2306 / -0.01 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT02 | + | ABD | 15 | 1555 | 1529 | 0 | -0.89 [-1.54; -0.32] | [-1.64; -0.23] | -0.75 | -0.95 | 0.479 [0.463] | -1.08 / -0.56 | 0.9977 / 0.0024 | 599 / -0.64 | 930 / -1.05 | +0.02 / 0.02 / 0.01 / True | 0.95 | False / True |
| KT02 | + | ABD | 30 | 1555 | 1500 | 0 | -0.54 [-1.56; +0.29] | [-1.76; +0.44] | -0.93 | -0.64 | 0.496 [0.476] | -0.88 / -0.08 | 0.8709 / 0.1292 | 588 / +0.57 | 912 / -1.26 | -0.06 / 0.01 / 0.01 / True | 0.67 | False / False |
| KT02 | + | AVR | 15 | 104 | 93 | 0 | +1.12 [-1.01; +3.22] | [-1.49; +3.54] | +2.96 | +1.24 | 0.567 [0.490] | +0.01 / +2.35 | 0.1517 / 0.8484 | 46 / +0.93 | 47 / +1.31 | +0.00 / 0.04 / 0.02 / True | 0.27 | False / False |
| KT02 | + | AVR | 30 | 104 | 90 | 0 | +2.03 [-0.24; +4.53] | [-0.69; +5.01] | +1.93 | +2.01 | 0.544 [0.472] | +0.90 / +3.51 | 0.0417 / 0.9584 | 44 / +1.36 | 46 / +2.67 | -0.05 / 0.01 / 0.01 / True | 0.11 | False / False |
| KT03 | + | ABD | 15 | 24354 | 23870 | 0 | -0.24 [-0.40; -0.08] | [-0.44; -0.04] | -0.29 | -0.30 | 0.492 [0.486] | -0.31 / -0.15 | 0.9979 / 0.0022 | 12320 / -0.22 | 11550 / -0.25 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / True |
| KT03 | + | ABD | 30 | 24354 | 23618 | 0 | -0.24 [-0.46; -0.00] | [-0.51; +0.06] | -0.51 | -0.39 | 0.491 [0.485] | -0.34 / -0.13 | 0.9765 / 0.0236 | 12197 / -0.17 | 11421 / -0.31 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / True |
| KT03 | + | AVR | 15 | 4487 | 4124 | 0 | +0.03 [-0.18; +0.26] | [-0.21; +0.33] | -0.11 | +0.00 | 0.498 [0.487] | -0.07 / +0.13 | 0.3863 / 0.6138 | 2127 / +0.02 | 1997 / +0.05 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT03 | + | AVR | 30 | 4487 | 4088 | 0 | -0.03 [-0.34; +0.32] | [-0.41; +0.39] | -0.16 | -0.06 | 0.497 [0.485] | -0.19 / +0.11 | 0.5654 / 0.4347 | 2101 / -0.12 | 1987 / +0.07 | +0.03 / 0.03 / 0.01 / True | 1.00 | False / False |
| KT04 | + | ABD | 15 | 12603 | 12304 | 0 | -0.21 [-0.41; -0.00] | [-0.45; +0.04] | -0.26 | -0.27 | 0.492 [0.484] | -0.32 / -0.12 | 0.9699 / 0.0302 | 6503 / -0.16 | 5801 / -0.25 | -0.02 / 0.01 / 0.01 / True | 1.00 | False / True |
| KT04 | + | ABD | 30 | 12603 | 12160 | 0 | -0.26 [-0.54; +0.04] | [-0.59; +0.10] | -0.46 | -0.40 | 0.491 [0.484] | -0.39 / -0.13 | 0.9564 / 0.0437 | 6436 / -0.15 | 5724 / -0.37 | -0.01 / 0.03 / 0.03 / True | 1.00 | False / False |
| KT04 | + | AVR | 15 | 2561 | 2358 | 0 | -0.01 [-0.30; +0.30] | [-0.35; +0.38] | -0.18 | -0.03 | 0.492 [0.478] | -0.16 / +0.10 | 0.5363 / 0.4638 | 1175 / +0.08 | 1183 / -0.10 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT04 | + | AVR | 30 | 2561 | 2337 | 0 | +0.05 [-0.36; +0.48] | [-0.41; +0.59] | -0.16 | +0.03 | 0.498 [0.484] | -0.16 / +0.20 | 0.4014 / 0.5987 | 1162 / -0.06 | 1175 / +0.17 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT05 | + | ABD | 15 | 26570 | 26064 | 0 | -0.25 [-0.40; -0.09] | [-0.44; -0.04] | -0.30 | -0.32 | 0.491 [0.485] | -0.32 / -0.16 | 0.9985 / 0.0016 | 13450 / -0.22 | 12614 / -0.28 | +0.01 / 0.01 / 0.01 / True | 1.00 | False / True |
| KT05 | + | ABD | 30 | 26570 | 25789 | 0 | -0.28 [-0.49; -0.06] | [-0.54; +0.00] | -0.52 | -0.44 | 0.490 [0.485] | -0.39 / -0.19 | 0.9936 / 0.0065 | 13321 / -0.20 | 12468 / -0.37 | -0.00 / 0.00 / 0.01 / True | 1.00 | False / True |
| KT05 | + | AVR | 15 | 4822 | 4458 | 0 | +0.00 [-0.20; +0.23] | [-0.24; +0.28] | -0.08 | -0.02 | 0.498 [0.487] | -0.09 / +0.09 | 0.4851 / 0.5150 | 2306 / +0.00 | 2152 / +0.01 | -0.00 / 0.02 / 0.03 / True | 1.00 | False / False |
| KT05 | + | AVR | 30 | 4822 | 4423 | 0 | -0.06 [-0.38; +0.28] | [-0.45; +0.35] | -0.15 | -0.08 | 0.498 [0.486] | -0.23 / +0.06 | 0.6285 / 0.3716 | 2282 / -0.17 | 2141 / +0.06 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT06 | + | ABD | 15 | 15726 | 15413 | 0 | -0.17 [-0.34; -0.00] | [-0.37; +0.03] | -0.23 | -0.23 | 0.493 [0.486] | -0.25 / -0.09 | 0.9741 / 0.0260 | 7902 / -0.14 | 7511 / -0.20 | +0.00 / 0.03 / 0.00 / True | 1.00 | False / True |
| KT06 | + | ABD | 30 | 15726 | 15191 | 0 | -0.17 [-0.41; +0.07] | [-0.45; +0.12] | -0.48 | -0.33 | 0.491 [0.485] | -0.28 / -0.06 | 0.9155 / 0.0846 | 7798 / -0.10 | 7393 / -0.23 | -0.01 / 0.01 / 0.02 / True | 1.00 | False / False |
| KT06 | + | AVR | 15 | 3181 | 2946 | 0 | -0.06 [-0.28; +0.18] | [-0.32; +0.25] | -0.11 | -0.07 | 0.495 [0.483] | -0.16 / +0.04 | 0.7020 / 0.2981 | 1515 / +0.04 | 1431 / -0.17 | -0.02 / 0.01 / 0.04 / True | 1.00 | False / False |
| KT06 | + | AVR | 30 | 3181 | 2922 | 0 | -0.11 [-0.46; +0.28] | [-0.56; +0.38] | -0.14 | -0.11 | 0.496 [0.484] | -0.28 / +0.03 | 0.7159 / 0.2842 | 1497 / -0.17 | 1425 / -0.05 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT07 | + | ABD | 15 | 672 | 661 | 0 | -1.10 [-1.94; -0.28] | [-2.14; -0.09] | -0.60 | -1.11 | 0.483 [0.458] | -1.48 / -0.84 | 0.9949 / 0.0052 | 264 / -0.67 | 397 / -1.38 | -0.04 / 0.02 / 0.01 / True | 0.74 | False / False |
| KT07 | + | ABD | 30 | 672 | 648 | 0 | -1.08 [-2.15; -0.06] | [-2.38; +0.12] | -1.26 | -1.20 | 0.488 [0.466] | -1.58 / -0.65 | 0.9799 / 0.0202 | 260 / +0.35 | 388 / -2.04 | -0.01 / 0.01 / 0.01 / True | 0.42 | False / False |
| KT07 | + | AVR | 15 | 47 | 41 | 0 | +0.87 [-2.36; +3.75] | [-3.20; +4.18] | +1.52 | +1.04 | 0.545 [0.405] | -1.06 / +2.70 | 0.3035 / 0.6966 | 23 / +0.57 | 18 / +1.25 | +0.03 / 0.01 / 0.01 / True | 0.12 | False / False |
| KT07 | + | AVR | 30 | 47 | 38 | 0 | +1.17 [-2.36; +4.51] | [-3.07; +5.25] | +1.59 | +1.02 | 0.530 [0.409] | -1.19 / +3.30 | 0.2677 / 0.7324 | 21 / -1.06 | 17 / +3.93 | -0.02 / 0.01 / 0.02 / True | 0.08 | False / False |
| KT08 | - | ABD | 15 | 17601 | 17558 | 0 | -0.03 [-0.32; +0.25] | [-0.39; +0.32] | -0.29 | -0.20 | 0.504 [0.498] | -0.20 / +0.08 | 0.5695 / 0.4306 | 6935 / +0.16 | 10623 / -0.16 | +0.00 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT08 | - | ABD | 30 | 14350 | 14263 | 0 | -0.30 [-0.97; +0.37] | [-1.10; +0.48] | -0.89 | -0.61 | 0.501 [0.491] | -0.52 / +0.16 | 0.7436 / 0.2565 | 5737 / -0.12 | 8526 / -0.42 | +0.02 / 0.02 / 0.01 / True | 1.00 | False / False |
| KT08 | - | AVR | 15 | 1928 | 1867 | 0 | +0.26 [-0.39; +1.03] | [-0.52; +1.11] | +0.45 | +0.23 | 0.517 [0.500] | +0.03 / +0.83 | 0.2812 / 0.7189 | 842 / -0.13 | 1025 / +0.59 | +0.02 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT08 | - | AVR | 30 | 1643 | 1587 | 0 | +0.49 [-0.56; +1.65] | [-0.74; +1.82] | +0.41 | +0.43 | 0.517 [0.493] | +0.12 / +1.34 | 0.2105 / 0.7896 | 721 / +0.18 | 866 / +0.75 | +0.01 / 0.03 / 0.01 / True | 0.97 | False / False |
| KT09 | + | ABD | 15 | 973 | 965 | 0 | +0.67 [-1.74; +3.17] | [-2.31; +3.74] | -1.58 | -0.01 | 0.487 [0.450] | -1.34 / +1.44 | 0.3130 / 0.6871 | 225 / +2.74 | 740 / +0.04 | +0.02 / 0.01 / 0.01 / True | 0.86 | False / False |
| KT09 | + | ABD | 30 | 973 | 955 | 0 | +2.46 [-1.22; +5.95] | [-1.78; +6.65] | -2.54 | +1.20 | 0.496 [0.460] | -0.23 / +3.70 | 0.1130 / 0.8871 | 225 / +5.94 | 730 / +1.39 | +0.01 / 0.01 / 0.02 / True | 0.45 | False / False |
| KT09 | + | AVR | 15 | 20 | 20 | 0 | -0.69 [-13.61; +13.82] | [-15.44; +17.94] | -11.00 | -2.98 | 0.401 [0.211] | -10.18 / +6.88 | 0.5415 / 0.4586 | 1 / +47.67 | 19 / -3.23 | +0.14 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT09 | + | AVR | 30 | 20 | 20 | 0 | +3.05 [-7.29; +14.95] | [-10.10; +17.28] | -0.83 | +2.97 | 0.504 [0.344] | -4.48 / +9.28 | 0.2992 / 0.7010 | 1 / +35.36 | 19 / +1.35 | -0.34 / 0.00 / 0.00 / True | 0.00 | False / False |
| KT10 | + | ABD | 15 | 25233 | 24591 | 0 | +0.08 [-0.21; +0.36] | [-0.29; +0.43] | -0.29 | -0.16 | 0.499 [0.492] | -0.03 / +0.24 | 0.3056 / 0.6945 | 16881 / +0.01 | 7710 / +0.23 | -0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT10 | + | ABD | 30 | 15510 | 14930 | 0 | +0.17 [-0.26; +0.58] | [-0.36; +0.70] | -0.58 | -0.24 | 0.501 [0.492] | +0.03 / +0.40 | 0.2279 / 0.7722 | 10190 / +0.17 | 4740 / +0.18 | +0.00 / 0.01 / 0.03 / True | 1.00 | False / False |
| KT11 | + | ABD | 15 | 1561 | 1544 | 0 | +0.17 [-0.37; +0.72] | [-0.47; +0.84] | -0.04 | +0.08 | 0.501 [0.483] | -0.10 / +0.45 | 0.2751 / 0.7250 | 816 / -0.18 | 728 / +0.57 | -0.01 / 0.01 / 0.01 / True | 0.95 | False / False |
| KT11 | + | ABD | 30 | 1561 | 1504 | 0 | +0.61 [-0.22; +1.53] | [-0.37; +1.73] | -0.21 | +0.48 | 0.508 [0.486] | +0.14 / +0.95 | 0.0808 / 0.9193 | 798 / +0.10 | 706 / +1.18 | -0.06 / 0.01 / 0.02 / True | 0.67 | False / False |
| KT11 | + | AVR | 15 | 271 | 253 | 0 | +1.14 [+0.20; +2.21] | [+0.01; +2.50] | +0.52 | +0.87 | 0.533 [0.490] | +0.49 / +1.45 | 0.0186 / 0.9815 | 130 / +0.69 | 123 / +1.62 | +0.01 / 0.01 / 0.01 / True | 0.66 | False / False |
| KT11 | + | AVR | 30 | 271 | 248 | 0 | +0.65 [-0.86; +2.22] | [-1.15; +2.65] | +0.57 | +0.48 | 0.510 [0.463] | -0.32 / +1.28 | 0.2155 / 0.7846 | 126 / +0.33 | 122 / +0.99 | +0.04 / 0.03 / 0.01 / True | 0.39 | False / False |
| KT12 | + | ABD | 15 | 2614 | 2563 | 0 | -0.16 [-0.60; +0.30] | [-0.72; +0.40] | -0.12 | -0.21 | 0.496 [0.482] | -0.38 / +0.03 | 0.7493 / 0.2508 | 1232 / -0.37 | 1331 / +0.04 | +0.02 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT12 | + | ABD | 30 | 2614 | 2528 | 0 | +0.14 [-0.48; +0.76] | [-0.59; +0.87] | -0.31 | -0.04 | 0.499 [0.485] | -0.23 / +0.38 | 0.3491 / 0.6510 | 1214 / -0.10 | 1314 / +0.35 | -0.01 / 0.01 / 0.01 / True | 0.87 | False / False |
| KT12 | + | AVR | 15 | 424 | 381 | 0 | +0.69 [-0.08; +1.49] | [-0.22; +1.62] | +0.29 | +0.66 | 0.522 [0.485] | +0.32 / +1.03 | 0.0498 / 0.9503 | 188 / +0.82 | 193 / +0.56 | +0.02 / 0.02 / 0.03 / True | 0.78 | False / False |
| KT12 | + | AVR | 30 | 424 | 377 | 0 | +0.73 [-0.40; +1.92] | [-0.55; +2.17] | +0.12 | +0.66 | 0.518 [0.480] | +0.13 / +1.16 | 0.1168 / 0.8833 | 185 / +0.88 | 192 / +0.59 | -0.08 / 0.01 / 0.02 / True | 0.56 | False / False |
| KT13 | + | ABD | 15 | 22222 | 21589 | 0 | +0.02 [-0.51; +0.53] | [-0.61; +0.65] | -0.54 | -0.28 | 0.499 [0.489] | -0.16 / +0.26 | 0.4692 / 0.5309 | 8407 / +0.25 | 13182 / -0.13 | -0.01 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT13 | + | ABD | 30 | 19279 | 18483 | 0 | +0.24 [-0.56; +1.09] | [-0.70; +1.29] | -0.85 | -0.27 | 0.503 [0.491] | -0.12 / +0.54 | 0.2787 / 0.7214 | 7378 / +0.54 | 11105 / +0.05 | +0.00 / 0.01 / 0.01 / True | 1.00 | False / False |
| KT13 | + | AVR | 15 | 3834 | 2869 | 0 | -0.05 [-0.57; +0.45] | [-0.68; +0.54] | -0.25 | -0.07 | 0.499 [0.481] | -0.20 / +0.24 | 0.5611 / 0.4390 | 1352 / -0.37 | 1517 / +0.25 | -0.01 / 0.02 / 0.03 / True | 1.00 | False / False |
| KT13 | + | AVR | 30 | 3430 | 2556 | 0 | +0.21 [-0.51; +1.00] | [-0.64; +1.18] | -0.30 | +0.12 | 0.501 [0.482] | -0.19 / +0.54 | 0.2926 / 0.7075 | 1208 / +0.22 | 1348 / +0.21 | +0.02 / 0.01 / 0.01 / True | 1.00 | False / False |

## 11. Ana modelin komutları (her blok için sırayla)

```
KASA_DIZIN=/tmp/kasa2 KASA_GIZLI=<gizli anahtar yolu> python KASA.py ac --blok 2024Q1 --hipotez KART_TUR2 --onkayit arastirma_cikti/kart2/KART_TUR2_ON_KAYIT.md --cikti /tmp/kasa2 --manifest arastirma_cikti/kasa/KASA2_MANIFEST.json
nohup python KART_TUR2.py olc --veri /tmp/kasa2/acik --cikti arastirma_cikti/kart2/2024Q1 --islem 4 > /tmp/k2_2024Q1.log 2>&1 &
```

Sıradaki bloklar: 2024Q2, 2024Q3, 2024Q4 (BAKIŞ 1), 2025Q1 ... 2025Q4 (BAKIŞ 2), 2026Q1 ... 2026Q4 (BAKIŞ 3). Her olc'tan sonra arastirma_cikti/kasa/KASA_DEFTERI.md ve çıktı klasörü commit edilir. KART_TUR2.py ve bu ön kayıt bu commit'ten sonra DEĞİŞMEZ.

## 12. KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı KV1 kovası (ATRP tercili x LQ3 x F15 çeyreği; sınırlar tezgah2_hazirlik.json), P2 havuzu, aynı geometri (R_H stop'suz, aynı E0 / H); kartın o günkü olay kümesi ve olayın kendisi eş dışı, >= 5 eş (OS.os_es); plasebo kapısı 200 tohum aynı gün rastgele P2 hissesi; KT00 / KT13 kontrol kartları; mekanik üstünlük yok (stop / hedef yok) |
| K2 | geleceğe bakma | EVET | bayraklar yalnız t ve öncesi barlarla; PREFIX TESTİ (2022-06-30 kesik, <= 2022-05-31 sinyal + bayrak + özellik + P2 olay kümeleri birebir; k2_prefix.json; tutmazsa DURUR); KASA 2 kapısı (en geç tarih <= açık kesik); açık hücreler dondurulmuş (H. bar <= 2023-12-31); eski olay / sonuç dosyaları okunmaz; sektör ve evren listesi bugünkü (K7 / sınır) |
| K3 | geçerli bar | EVET | OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0) + açılış kırpması; sinyal günü geçersiz bar ise olay düşer (oc_olay_hazirla); R_H yalnız geçerli barlar, 2H satır kuralı |
| K4 | tekilleştirme | EVET | Y1 60 gün tekil (OC), DS ANA 15 bar, BOFA 60 bar ayrılık, sonra kart x H tekil (>= H gün); n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan ve kırpılmış ortalama hücre tablosunda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla / os_kart_sinyal; boşluk <= 10 gün); eşler aynı gün açılışı |
| K6 | veri birimi | EVET | V_*2.pkl tek kip (auto_adjust; TEZGAH2_VERI); oranlar birimsiz; P2 fiyat / likidite eşiği Close x Kur (EUR); bölünme şüphesi havuz dışı (OS nedensel kuralı); BOFA veri kırığı kuralı aynen |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok; ABD 2000 aktif = 2025'in %31'i); dipteki kartlarda (KT02, KT07, KT08, KT09) yanlılık büyük; açık alt dönem işaretleri yukarı yanlı; raporda yazılı |
| K8 | örneklem ve dönem | EVET | hücre n >= 30 ve güç (yapay iz, +1 puan) >= 0,80 değilse ÖLÇÜLEMEDİ; güç tablosu (4 / 8 / 12 blokta beklenen n) ön kayıtta; iki karar ufku + iki karar pazarı + üç açık alt dönem; BH q 0,10 (bakışta / 3) m 24; üç bakış Bonferroni |
| K9 | ön kayıt | EVET | KART_TUR2_ON_KAYIT.md: K2_ESIK / K2_KART sha, KASA_KOD KART_TUR2.py sha, BAGIMLI_SHA tablosu, açık tablo / güç / prefix / olay sha'ları, karar kuralı, bakış takvimi, güç tablosu; sıra kod commit -> açık kuru koşu -> ön kayıt commit -> (ana model) blok aç -> olc; blok açıkken KASA.ks_onkayit_kapi + sha kapısı |
| K10 | ayrıştırma | UYGULANMAZ | ham haber / KAP / SEC ayrıştırması yok; yalnız OHLCV + sektor_ABD.csv |
| K11 | yeniden üretim | EVET | k2_yeniden: iki hücre (KT01 ABD R15 acik_d3, KT08 AVR R30 acik_d2) satır dosyasından düz pandas; blok koşusunda açık hücreler kuru koşu tablosuyla birebir; tutmazsa DURUR |
| K12 | ifade | EVET | etiketler yalnız karar kuralıyla; açık veri 'bilinen veri' diye ayrı; sayı ve yorum ayrı cümle; 'iz' sözü yalnız kural geçerse |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_k2 (test); defter / yasak modüllere dokunulmadı (bağımlı sha tablosu); e-posta / anahtar taraması (_k2_yaz); dış istek / indirme yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; kart ölçümü |

