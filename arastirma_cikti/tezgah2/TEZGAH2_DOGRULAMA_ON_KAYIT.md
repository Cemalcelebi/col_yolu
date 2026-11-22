# TEZGÂH 2 DOĞRULAMA — ÖN KAYIT (2026-11-22 10:50:35 UTC)

Sürüm: TEZGAH2_DOGRULAMA v1.0 (2026-11-22). İş tanımı: arastirma_cikti/tezgah2/TEZGAH2_DOGRULAMA_IS_TANIMI.md (sha 3232b3906596e4792c8e47ef432f32a95fe91e6cd4dbf49ee30c4b5d12bc66a8).
Kod: TEZGAH2_DOGRULAMA.py git 5ec968f508e37734bbc480b36d579c26b0a10982 2026-11-22T10:46:39+00:00. Bu dosya koşudan ÖNCE commit edilir; t2_kapi git kaydını, değişmemişliği, sha'ları ve kontrol tablosunu denetler. İz aranmaz; yalnız doğrulama ve havuz seçimi. Bizim aylık getiri serileri henüz HESAPLANMADI (hazırlık getirisiz: kova sınırları, evren prefix testi, havuz sayımları).

Açık kesik: KASA 2 (/tmp/kasa2/acik/KASA_DURUM.json) 2023-12-31 (mühür 32d362ecaae2e2da); kasa_kapisi: V_ABD2.pkl en geç 2023-12-29; V_AVR2.pkl en geç 2023-12-29; referans: ref_kesik.pkl en geç 2023-12-31; yahoo_kesik.pkl en geç 2023-12-29; eurusd_kesik.pkl en geç 2023-12-29.

Veri yolu: OS.os_veri(pazar, '/tmp/kasa2/acik') -> OC.oc_veri(..., veri2='/nonexistent_os_k34_yok'): k34_yahoo KULLANILMAZ; V_ABD.pkl / V_AVR.pkl bu klasörde V_ABD2.pkl / V_AVR2.pkl'ye bağlantı (t2_kasa_kapi denetler).

## 1. HAVUZ ADAYLARI (iş tanımından AYNEN)

P1 = OLCU_SINAMA havuzu olduğu gibi (alt %20 likidite dışı, bölünme şüphesi dışı). P2 = P1 + ABD'de kapanış >= 2 $ (AVR'de >= 1 EUR karşılığı) + son 20 gün medyan işlem değeri >= 1 mn $ (AVR 1 mn EUR). P3 = P2 + son 250 barda |günlük getiri| > %50 olan ve 3 bar içinde en az yarısını geri veren (sıçra-geri dön) bir bar varsa o hisse-gün dışı (nedensel: yalnız d-1'e kadarki barlar).

İşlemsel tanım (kodda): P1: OS paneli: ok (d günü geçerli bar, kendi 80. geçerli barından sonra, momentum60 ve likidite sonlu, alt %20 likidite dışı, nedensel bölünme şüphesi dışı) VE H >= 0 (5 x 3 kova; günde >= 30 hisse).
P2: P1 VE d'den önceki son geçerli kapanış x Kur >= fiyat_min (ABD 2 USD; AVR 1 EUR; Kur = yerel -> EUR) VE Lq (C x V x Kur, d'den önceki 20 birleşik takvim gününün medyanı, en az 10 gün; OS paneli) >= likidite_min (ABD 1e6 USD; AVR 1e6 EUR).
P3: P2 VE değil SG: hissenin kendi geçerli barlarında (değer = Close x Kur) bar i sıçrama = |C_i / C_{i-1} - 1| > 0,50; geri dönüş = i+1..i+3 barlarının ilkinde (C_i - C_{i+k}) / (C_i - C_{i-1}) >= 0,50 (fiyat farkının en az yarısı geri), c = o ilk bar; hisse-gün d dışı <=> nb(d) (d'den önceki geçerli bar sayısı) [c+1, i+250] aralığında (onay barı c <= d-1 VE sıçrama barı son 250 bar içinde); birleşik takvimde satır (pos[c], pos[i+250]] (i+250 veri sonunu aşıyorsa sona kadar).

## 2. HÜKÜM KURALI (iş tanımından AYNEN)

HÜKÜM: DOĞRU = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa >= 0,90); KISMEN 0,40-0,70; UYUŞMUYOR < 0,40.

Kod: TD.td_hukum aynen (Pearson; DOĞRU eşiği geçilip işaret uyumu < %70 ise KISMEN; piyasa 0,40-0,90 KISMEN; n < 36 ay ÖLÇÜLEMEDİ).

## 3. HAVUZ SEÇİM KURALI (iş tanımından AYNEN)

HAVUZ SEÇİM KURALI (sonuç görülmeden): seçilen havuz = bütün ana serilerde (piyasa, momentum 2x3, dönüş 2x3; ABD üç dönem + AVR) DOĞRU olanlar arasında EN GENİŞ olan (P1 > P2 > P3 sırası: önce P1); hiçbiri tam geçmezse en çok seri geçen ve neden / hangi dönem düştüğü raporlanır.

İşlemsel: ana seriler = ABD piyasa EW (A1) ve işlem değeri ağırlıklı (A2), MOM 2x3 (A5), STREV 2x3 (A8) x üç alt dönem (d1 2001-07, d2 2008-15, d3 2016-23) + AVR piyasa LQ (E1) ve EW (E2), WML 2x3 (E3) x aynı üç alt dönem = havuz başına 21 hüküm. 'AVR' de üç dönemde sınanır (üç alt dönem ayrı ayrı şartı bütün serilere uygulanır). Yedek: en çok DOĞRU; eşitlikte geniş olan (P1 > P2 > P3). Onluk farkları (A3, A4, A6, A7, E4) ve 'tum' dönemi bilgi; seçime girmez.

Sonuç cümlesi: tek cümle (seçilen havuz): 12 ana çift x üç alt dönem hepsi DOĞRU ise 'geniş tezgâh yayımlanmış serileri izliyor'; biri UYUŞMUYOR ise 'geniş tezgâhta / evrende fark var' (hangi seri / dönem); aksi 'kısmen izliyor' (DOĞRU olmayanlar).

## 4. SERİLER VE DÖNEMLER

Dönemler (tutma ayı): tüm ['2000-07', '2023-12'], d1 ['2001-01', '2007-12'], d2 ['2008-01', '2015-12'], d3 ['2016-01', '2023-12']. TD_CIFT (A1-A8 ABD, E1-E4 AVR) aynen; 'havuz' maskesi yerine P1 / P2 / P3; getiri r = ay kapanışından ay kapanışına (AVR USD: Close x Kur x EURUSD ay son kuru); onluk / 2x3 / ağırlık tanımları TD_ESIK['bizim'] aynen.

| kod | bizim seri (havuz = P1 / P2 / P3) | referans | piyasa | açıklama |
|---|---|---|---|---|
| A1 | `ABD · havuz · r · PIYASA · - · EW` | `US_EWMKT` | E | ABD evren getirisi EW vs French EW piyasa (Prior_12_2 EW onlukları, firma ağırlıklı) |
| A2 | `ABD · havuz · r · PIYASA · - · LQ` | `US_MKT` | E | ABD evren getirisi LQ vs French piyasa (Mkt-RF + RF, VW) |
| A3 | `ABD · havuz · r · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | H | ABD MOM onluk üst - alt EW vs French Prior_12_2 EW Hi - Lo |
| A4 | `ABD · havuz · r · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | H | ABD MOM onluk üst - alt LQ vs French Prior_12_2 VW Hi - Lo |
| A5 | `ABD · havuz · r · MOM · 2X3 · LQ` | `US_MOM` | H | ABD MOM 2x3 (üst 30 - alt 30) LQ vs French Mom |
| A6 | `ABD · havuz · r · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | H | ABD STREV onluk alt - üst EW vs French Prior_1_0 EW Lo - Hi |
| A7 | `ABD · havuz · r · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | H | ABD STREV onluk alt - üst LQ vs French Prior_1_0 VW Lo - Hi |
| A8 | `ABD · havuz · r · STREV · 2X3 · LQ` | `US_STREV` | H | ABD STREV 2x3 (alt 30 - üst 30) LQ vs French ST_Rev |
| E1 | `AVR · havuz · r · PIYASA · - · LQ` | `EU_MKT` | E | AVR evren getirisi LQ (USD) vs French Avrupa piyasa (USD) |
| E2 | `AVR · havuz · r · PIYASA · - · EW` | `EU_MKT` | E | AVR evren getirisi EW (USD) vs French Avrupa piyasa (USD) |
| E3 | `AVR · havuz · r · MOM · 2X3 · LQ` | `EU_WML` | H | AVR MOM 2x3 LQ (USD) vs French Avrupa WML |
| E4 | `AVR · havuz · r · MOM · D10-D1 · EW` | `EU_WML` | H | AVR MOM onluk üst - alt EW (USD) vs French Avrupa WML |

Eski tezgâhla karşılaştırma: seçilen havuzun (ve bilgi olarak P1'in) A1-A8, E1-E4 serileri ile eski tezgâhın (Ç207, 1.380 ABD + 576 AVR hisse; tezgah_dogrulama.json 'seriler' ABD|havuz|r|...) aynı seriler arasında Pearson korelasyonu ve ortalama farkı, tutma ayı 2016-01..2023-12; eski hisse listesi açık kasa dışında olmadığı için yeni veride 1.401 ortak sembole kısıtlama yapılmaz.

Ek bilgi (karar dışı): seçilen havuzda yıl başına hisse-gün sayısı; likidite üst / alt yarı payı = o gün taban (geçerli bar, evrende, Lq sonlu) hisselerinin Lq medyanının üstünde / altında kalan havuz hisse-günleri payı. seçilen havuz, H = 15 ve 30: R_H (OS.os_olcu_matris: giriş barı açılışı E0, H. geçerli barın kapanışı / E0 - 1, 2H satır kuralı) her hisse-gün için; eş-farkı = R_H - aynı giriş günü d ve aynı KV1 kovasındaki (seçilen havuz içinde, KV1 >= 0, R_H sonlu) öteki hisselerin R_H ortalaması (kendisi hariç; en az 5 eş); dağılım: n, ortalama, standart sapma, IQR / 1,349, p01 / p05 / p50 / p95 / p99; pazar x alt dönem (giriş günü yılı: d1 2001-07, d2 2008-15, d3 2016-23); hipotez yok.

Yeniden üretim: ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu kullanmadan; TD.td_yeniden mantığı, ay listesi farklı): geçerli bar süzgeci, K55 + evren_disi fon listesi dışı, birleşik takvim ay sonu, MOM kendi bar indeksiyle, rank(first, pct), ceil onluk, ay kapanışı getirisi; fark < 1e-9 TUTAR; French ham satırı TD.td_french_elle; seriler ['ABD|tum|r|MOM|D10-D1|EW', 'ABD|tum|r|PIYASA|-|EW'], aylar ['2003-05', '2011-09', '2020-04'].

## 5. HAZIRLIK SONUCU (getirisiz; tezgah2_hazirlik.json)

### 5a. EVREN PREFIX TESTİ (kısa kesik 2015-06-30, uzun 2023-12-29; <= 2015-05-29)

| pazar | sonuç | toplam fark | gün | hisse kısa / uzun | P1 / P2 / P3 hisse-gün (önek) | maske farkları |
|---|---|---|---|---|---|---|
| ABD | TUTTU | 0 | 3875 | 2852 / 4606 | 5.707.162 / 4.388.056 / 4.380.097 | ok 0, ok_yeni 0, H 0, H_yeni 0, KV1 0, KV1_yeni 0, KV2 0, KV2_yeni 0, sup 0, sup_yeni 0, lik_alt 0, lik_alt_yeni 0, evren 0, evren_yeni 0, ATRP 0, F15 0, Lq 0, M 0, P1 0, P1_yeni 0, P2 0, P2_yeni 0, P3 0, P3_yeni 0, SG 0 |
| AVR | TUTTU | 0 | 3954 | 497 / 574 | 1.160.615 / 999.230 / 998.727 | ok 0, ok_yeni 0, H 0, H_yeni 0, KV1 0, KV1_yeni 0, KV2 0, KV2_yeni 0, sup 0, sup_yeni 0, lik_alt 0, lik_alt_yeni 0, evren 0, evren_yeni 0, ATRP 0, F15 0, Lq 0, M 0, P1 0, P1_yeni 0, P2 0, P2_yeni 0, P3 0, P3_yeni 0, SG 0 |

### 5b. KOVA SINIRLARI (OS kuralı, bu veride; koşuda aynı sayılar)

```json
{"ABD": {"KV1_ATRP": [0.02496298683654129, 0.0418801751616038], "KV1_F15": [0.23345296346069216, 0.5581271928100532, 0.8488934532165978], "KV2_ATRP": [0.016163776964023227, 0.02019036470281992, 0.023813416301810893, 0.027541828046980122, 0.03190153891659376, 0.03741502192832012, 0.04491618613970647, 0.05606622854287649, 0.07570716120270136], "n_KV1": 4566860, "n_KV2": 4603975}, "AVR": {"KV1_ATRP": [0.019559290051277323, 0.02836184453749112], "KV1_F15": [0.28224258561611526, 0.6103212224324032, 0.8709724126665116], "KV2_ATRP": [0.01414257576843198, 0.01664977468135037, 0.01884662016492124, 0.021040835322904967, 0.023425004721893142, 0.026190452694734502, 0.029632655074456452, 0.0344759377960784, 0.04331358912364459], "n_KV1": 748897, "n_KV2": 750428}}
```

### 5c. HAVUZ BAŞINA HİSSE SAYISI (yılda en az bir gün havuzda; günlük ortalama)

| pazar | havuz | 2000 | 2005 | 2010 | 2015 | 2020 | 2023 | toplam hisse |
|---|---|---|---|---|---|---|---|---|
| ABD | P1 | 1.256 (702) | 1.582 (1.369) | 1.860 (1.650) | 2.324 (2.050) | 3.214 (2.692) | 4.058 (3.395) | 4.382 |
| ABD | P2 | 765 (417) | 1.243 (1.023) | 1.525 (1.307) | 2.032 (1.754) | 2.914 (2.340) | 3.271 (2.710) | 4.053 |
| ABD | P3 | 760 (416) | 1.238 (1.022) | 1.517 (1.303) | 2.024 (1.753) | 2.824 (2.290) | 3.191 (2.687) | 3.944 |
| AVR | P1 | 218 (124) | 337 (280) | 395 (338) | 450 (385) | 499 (426) | 508 (448) | 548 |
| AVR | P2 | 182 (101) | 294 (241) | 335 (291) | 411 (364) | 492 (418) | 500 (438) | 537 |
| AVR | P3 | 182 (101) | 294 (241) | 335 (291) | 411 (364) | 492 (418) | 500 (438) | 537 |

## 6. REFERANS KAYNAK VE ERİŞİM

French (TEZGAH_DOGRULAMA ile aynı kesik dosya; indirme 2026-11-22 10:16:05 UTC; yedek: kullanılmadı):

| dosya | durum | sha256 |
|---|---|---|
| F-F_Research_Data_Factors_CSV.zip | açıldı | `b03d39e4bb253dda0f14893db3b78e64b40b8d6549a0fc0fd4111dae84c98618` |
| F-F_Momentum_Factor_CSV.zip | açıldı | `27ed60e5b2caa9ea334a261cddfa864a9926f6bf45e9677c95dfd835c5abb315` |
| F-F_ST_Reversal_Factor_CSV.zip | açıldı | `7ddb68bbaa507ec0b298ceaecf99e719ef051367d93de3d1f89150e3fbb61740` |
| 10_Portfolios_Prior_12_2_CSV.zip | açıldı | `688467caa28578a8dca70698537c4f03c406b246350b6f3e9c396e15e1e7964f` |
| 10_Portfolios_Prior_1_0_CSV.zip | açıldı | `9c82ae7be156e5958933b4c8b2a5c54d61191f02477f067929ff7b72f0127893` |
| Europe_3_Factors_CSV.zip | açıldı | `842332540d9c86681cbda628c6acc9d75d0c1563e364a2bf6a535072f651471e` |
| Europe_Mom_Factor_CSV.zip | açıldı | `ac254c7011515cc8b3c280dbe374fe8d05b6c5a5603cd7b17101c9fb2e3bdaa0` |

EURUSD: FRED DEXUSEU (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU), günlük USD / EUR, kimliksiz curl; indirme 2026-11-22 10:46:40 UTC; 6269 gün 1999-01-04..2023-12-29 (kesik); csv sha `cabc808213f550bb92e70ce8742fe476127f0eae52c5063c4ca3b6419d87301b`; Yahoo karşılaştırma: {'n_ay': 108, 'ilk': '2015-01', 'son': '2023-12', 'degisim_korelasyon': 0.9544589146337659, 'maks_seviye_fark_pct': 1.1264353462291932}.

## 7. SHA

| ad | sha256 |
|---|---|
| T2_ESIK_SHA | `0c9b1d2ce8f326e4db5f804bbf0acb01f4c345d60e9b297ebff0fd5293d8d980` |
| T2_KOD_SHA | `843b326cd53419c82a5e0eff593cbe615576c2fc0878da3e0a40d792088b4a91` |
| TD_KOD_SHA | `24232ab516bae5699306e9d9e60f5c24121421b7f1206a08a68a7fae7aeda702` |
| OS_KOD_SHA | `86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087` |
| OC_KOD_SHA | `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` |
| KASA_KOD_SHA | `3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b` |
| IS_TANIMI_SHA | `3232b3906596e4792c8e47ef432f32a95fe91e6cd4dbf49ee30c4b5d12bc66a8` |
| V_ABD2_SHA | `e892d27a9c5cf9d7cc672a32051cbe5e33ea5b1318a6fd44d1222c5453472c75` |
| V_AVR2_SHA | `a53320b65c7115c267d753c550b4fa677d298f531f4173f05b10f0b647fa33e1` |
| REF_KESIK_SHA | `61e94bdc781e6835474958848b631d6f1af0653b67ac61ba52b5c6ce903021fd` |
| YAHOO_KESIK_SHA | `6cd3d321d6a0e3c339b90176c1e798cd49a773b677641b636ef84d6d35a3a82b` |
| EURUSD_KESIK_SHA | `2433d994e71adbc749510fb9b6415b3e4272dea91b5fb120efc4702425575c71` |
| HAZIRLIK_SHA | `baba2309e2968828a60b78fa69505f241f6716dde113081b8c6f5fe934447ea8` |

## 8. TANIMLAR (T2_ESIK)

```json
{
 "surum": "T2-1.0",
 "kesik": "2023-12-31",
 "veri": {
  "klasor": "/tmp/kasa2/acik (V_ABD.pkl -> V_ABD2.pkl, V_AVR.pkl -> V_AVR2.pkl); başka fiyat kaynağı YOK",
  "yukle": "OS.os_veri(pazar, klasor) = OC.oc_veri(min_bar 1, abd_ek_aktif False, veri2 = '/nonexistent_os_k34_yok'): k34_yahoo KULLANILMAZ; geçerli bar süzgeci + ABD evren dışı (fon / ETF) listesi + açılış kırpması",
  "kapi": "KASA.kasa_kapisi(V_ABD2.pkl, V_AVR2.pkl; cikti /tmp/kasa2) + /tmp/kasa2/acik/KASA_DURUM.json açık kesik = 2023-12-31; referans pkl'leri (ref_kesik, yahoo_kesik, eurusd_kesik) aynı kesikle"
 },
 "havuz": {
  "metin": "P1 = OLCU_SINAMA havuzu olduğu gibi (alt %20 likidite dışı, bölünme şüphesi dışı). P2 = P1 + ABD'de kapanış >= 2 $ (AVR'de >= 1 EUR karşılığı) + son 20 gün medyan işlem değeri >= 1 mn $ (AVR 1 mn EUR). P3 = P2 + son 250 barda |günlük getiri| > %50 olan ve 3 bar içinde en az yarısını geri veren (sıçra-geri dön) bir bar varsa o hisse-gün dışı (nedensel: yalnız d-1'e kadarki barlar).",
  "P1": "OS paneli: ok (d günü geçerli bar, kendi 80. geçerli barından sonra, momentum60 ve likidite sonlu, alt %20 likidite dışı, nedensel bölünme şüphesi dışı) VE H >= 0 (5 x 3 kova; günde >= 30 hisse)",
  "P2": "P1 VE d'den önceki son geçerli kapanış x Kur >= fiyat_min (ABD 2 USD; AVR 1 EUR; Kur = yerel -> EUR) VE Lq (C x V x Kur, d'den önceki 20 birleşik takvim gününün medyanı, en az 10 gün; OS paneli) >= likidite_min (ABD 1e6 USD; AVR 1e6 EUR)",
  "P3": "P2 VE değil SG: hissenin kendi geçerli barlarında (değer = Close x Kur) bar i sıçrama = |C_i / C_{i-1} - 1| > 0,50; geri dönüş = i+1..i+3 barlarının ilkinde (C_i - C_{i+k}) / (C_i - C_{i-1}) >= 0,50 (fiyat farkının en az yarısı geri), c = o ilk bar; hisse-gün d dışı <=> nb(d) (d'den önceki geçerli bar sayısı) [c+1, i+250] aralığında (onay barı c <= d-1 VE sıçrama barı son 250 bar içinde); birleşik takvimde satır (pos[c], pos[i+250]] (i+250 veri sonunu aşıyorsa sona kadar)",
  "fiyat_min": {
   "ABD": 2.0,
   "AVR": 1.0
  },
  "likidite_min": {
   "ABD": 1000000.0,
   "AVR": 1000000.0
  },
  "sg": {
   "sicrama": 0.5,
   "geri_bar": 3,
   "geri_pay": 0.5,
   "pencere": 250
  },
  "sayim_yil": [
   2000,
   2005,
   2010,
   2015,
   2020,
   2023
  ],
  "kova_sinir": "KV1 / KV2 sınırları OS kuralıyla (os_kova_sinir: P1 havuzu, giriş 2016-22, getirisiz) BU veride hazırlıkta hesaplanır, tezgah2_hazirlik.json'a ve ön kayda yazılır, koşuda aynı sayılar verilir"
 },
 "prefix": {
  "kisa": "2015-06-30",
  "uzun": "2023-12-29",
  "son": "2015-05-29",
  "tanim": "iki kesikte panel: OS.os_prefix (ok, H, KV1, KV2, sup, lik_alt, evren, ATRP, F15, Lq, M, kart olay kümeleri) + P1 / P2 / P3 maskeleri; sinyal / havuz günü <= 2015-05-29 olan bütün hisse-günlerde fark 0 beklenir, değilse DURUR"
 },
 "donem": {
  "tum": [
   "2000-07",
   "2023-12"
  ],
  "d1": [
   "2001-01",
   "2007-12"
  ],
  "d2": [
   "2008-01",
   "2015-12"
  ],
  "d3": [
   "2016-01",
   "2023-12"
  ],
  "tarih": "TUTMA ayı (getirinin ölçüldüğü ay); ilk aylar 12-1 momentum için ısınma (MOM serileri ~2001-02'den)"
 },
 "seri": "TD_CIFT (A1-A8 ABD, E1-E4 AVR) aynen; 'havuz' maskesi yerine P1 / P2 / P3; getiri r = ay kapanışından ay kapanışına (AVR USD: Close x Kur x EURUSD ay son kuru); onluk / 2x3 / ağırlık tanımları TD_ESIK['bizim'] aynen",
 "eurusd": {
  "kaynak": "FRED DEXUSEU (https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXUSEU), günlük USD / EUR, kimliksiz curl",
  "ay": "ayın son geçerli gözlemi",
  "kesik": "<= 2023-12-31",
  "denetim": "Yahoo EURUSD=X (TD yahoo_kesik, 2015-23) ay sonu ile aylık değişim korelasyonu ve en büyük seviye farkı raporlanır (bilgi)"
 },
 "hukum": {
  "metin": "HÜKÜM: DOĞRU = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa >= 0,90); KISMEN 0,40-0,70; UYUŞMUYOR < 0,40.",
  "kod": "TD.td_hukum aynen (Pearson; DOĞRU eşiği geçilip işaret uyumu < %70 ise KISMEN; piyasa 0,40-0,90 KISMEN; n < 36 ay ÖLÇÜLEMEDİ)"
 },
 "secim": {
  "metin": "HAVUZ SEÇİM KURALI (sonuç görülmeden): seçilen havuz = bütün ana serilerde (piyasa, momentum 2x3, dönüş 2x3; ABD üç dönem + AVR) DOĞRU olanlar arasında EN GENİŞ olan (P1 > P2 > P3 sırası: önce P1); hiçbiri tam geçmezse en çok seri geçen ve neden / hangi dönem düştüğü raporlanır.",
  "kume": {
   "ABD": [
    "A1",
    "A2",
    "A5",
    "A8"
   ],
   "AVR": [
    "E1",
    "E2",
    "E3"
   ],
   "donem": [
    "d1",
    "d2",
    "d3"
   ]
  },
  "yorum": "ana seriler = ABD piyasa EW (A1) ve işlem değeri ağırlıklı (A2), MOM 2x3 (A5), STREV 2x3 (A8) x üç alt dönem (d1 2001-07, d2 2008-15, d3 2016-23) + AVR piyasa LQ (E1) ve EW (E2), WML 2x3 (E3) x aynı üç alt dönem = havuz başına 21 hüküm. 'AVR' de üç dönemde sınanır (üç alt dönem ayrı ayrı şartı bütün serilere uygulanır). Yedek: en çok DOĞRU; eşitlikte geniş olan (P1 > P2 > P3). Onluk farkları (A3, A4, A6, A7, E4) ve 'tum' dönemi bilgi; seçime girmez."
 },
 "sonuc": {
  "kural": "tek cümle (seçilen havuz): 12 ana çift x üç alt dönem hepsi DOĞRU ise 'geniş tezgâh yayımlanmış serileri izliyor'; biri UYUŞMUYOR ise 'geniş tezgâhta / evrende fark var' (hangi seri / dönem); aksi 'kısmen izliyor' (DOĞRU olmayanlar)"
 },
 "eski": {
  "tanim": "seçilen havuzun (ve bilgi olarak P1'in) A1-A8, E1-E4 serileri ile eski tezgâhın (Ç207, 1.380 ABD + 576 AVR hisse; tezgah_dogrulama.json 'seriler' ABD|havuz|r|...) aynı seriler arasında Pearson korelasyonu ve ortalama farkı, tutma ayı 2016-01..2023-12; eski hisse listesi açık kasa dışında olmadığı için yeni veride 1.401 ortak sembole kısıtlama yapılmaz"
 },
 "ek": {
  "sayim": "seçilen havuzda yıl başına hisse-gün sayısı; likidite üst / alt yarı payı = o gün taban (geçerli bar, evrende, Lq sonlu) hisselerinin Lq medyanının üstünde / altında kalan havuz hisse-günleri payı",
  "es_sd": "seçilen havuz, H = 15 ve 30: R_H (OS.os_olcu_matris: giriş barı açılışı E0, H. geçerli barın kapanışı / E0 - 1, 2H satır kuralı) her hisse-gün için; eş-farkı = R_H - aynı giriş günü d ve aynı KV1 kovasındaki (seçilen havuz içinde, KV1 >= 0, R_H sonlu) öteki hisselerin R_H ortalaması (kendisi hariç; en az 5 eş); dağılım: n, ortalama, standart sapma, IQR / 1,349, p01 / p05 / p50 / p95 / p99; pazar x alt dönem (giriş günü yılı: d1 2001-07, d2 2008-15, d3 2016-23); hipotez yok"
 },
 "yeniden": {
  "seri": [
   "ABD|tum|r|MOM|D10-D1|EW",
   "ABD|tum|r|PIYASA|-|EW"
  ],
  "ay": [
   "2003-05",
   "2011-09",
   "2020-04"
  ],
  "tanim": "ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu kullanmadan; TD.td_yeniden mantığı, ay listesi farklı): geçerli bar süzgeci, K55 + evren_disi fon listesi dışı, birleşik takvim ay sonu, MOM kendi bar indeksiyle, rank(first, pct), ceil onluk, ay kapanışı getirisi; fark < 1e-9 TUTAR; French ham satırı TD.td_french_elle"
 }
}
```

## 9. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | iz / sinyal sınaması yok; doğrulama: bizim aylık portföy serileri = yayımlanmış French serileriyle ay ay; dış referans kontrol yerine geçer; eş-farkı SD yalnız dağılım genişliği (OS eş kuralı: aynı gün, aynı KV1, kendisi hariç, >= 5 eş) |
| K2 | geleceğe bakma | EVET | sıralama t kapanışında bilinenle (MOM C_{k-21}/C_{k-252}, STREV C_k/C_{k-21}); havuz giriş günü d'de yalnız d-1'e kadarki barlarla (P2 fiyatı shift(1), Lq shift(1), P3 onay barı <= d-1); EVREN PREFIX TESTİ (2015-06-30 / 2023-12-29, <= 2015-05-29 fark 0) P1 / P2 / P3 dahil; KASA 2 kapısı hisse + referans pkl (2023-12-31) |
| K3 | geçerli bar | EVET | OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0); ay sonu t'de geçerli bar (os_kart_sinyal); P3 yalnız geçerli barların Close x Kur'u |
| K4 | tekilleştirme | UYGULANMAZ | olay yok; ay başına bir portföy getirisi; eş-farkı SD hisse-gün dağılımı (karar dışı, n bağımsız olay iddiası yok) |
| K5 | giriş fiyatı | EVET | birincil getiri French ile aynı kip (ay kapanışından ay kapanışına); eş-farkı R_H giriş barı açılışı E0'dan (OS) |
| K6 | veri birimi | EVET | V_*2.pkl tek kip (auto_adjust; TEZGAH2_VERI raporu); AVR Close x Kur (EUR) x EURUSD (FRED, ay son) = USD; P2 fiyat eşiği EUR karşılığı; P3 Close x Kur ile (Londra peni / sterlin birim sıçraması sayılmaz); French yüzde -> ondalık |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok; ABD 2000 aktif = 2025'in %31'i): seviye getirileri ve alt onluklar yukarı yanlı, 2000-15 daha çok; raporda yazılı; korelasyon / ortalama ayrı okunur |
| K8 | örneklem ve dönem | EVET | üç alt dönem (2001-07, 2008-15, 2016-23) ayrı hüküm; n < 36 ay ÖLÇÜLEMEDİ; havuz seçimi 21 hükmün hepsi |
| K9 | ön kayıt | EVET | T2_ESIK sha + kod sha + git commit, hazırlık json sha (kova sınırı, prefix), referans sha'ları ön kayıtta; sıra kod commit -> hazırlık (getirisiz) -> ön kayıt commit -> koşu; t2_kapi ön kaydın işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; havuz tanımı, hüküm ve seçim kuralı iş tanımından aynen |
| K10 | ayrıştırma | EVET | French ayrıştırma TD.td_french_ayristir (Ç207'de sınandı) + TD.td_french_elle ham satır 4 hücre; FRED CSV: başlık + tarih,değer; '.' / boş eksik; 3 satır ham metinden elle (rapor) |
| K11 | yeniden üretim | EVET | t2_yeniden: 2 seri x 3 ay ham V_ABD2.pkl'den düz pandas (OC / OS / TD kodu yok) + French 4 satır; tutmazsa rapor TUTMADI |
| K12 | ifade | EVET | iz iddiası yok; hüküm ve seçim yalnız önceden yazılı eşik / kuralla; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_t2; test); OS / TD / OC / KASA / TEZGAH2_VERI / defter / kart / kasa dosyalarına dokunulmadı; dış istek yalnız FRED (+ gerekirse French; kimlik yok, Tiingo yok); e-posta / anahtar taraması (_t2_yaz) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tezgâh doğrulaması |
