# YAPI_HEDEF — ÖN KAYIT 8 (8. tur: Ş10 MACD pozitif uyumsuzluk; Y13 / Y13b / Y13c; karne v3, sınama dönemleri ayrı)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 8. tur eklendi (YAPI_HEDEF_IS_TANIMI_8.md). Kodlayıcı alt ajan. Bu dosya koşudan ÖNCE yazıldı; aşağıdaki sayılar yalnız satır kimliği, dönem, giriş tarihi, özellik bayrakları ve Cemal sayfa sayılarıdır (getirisiz: h5 / es_h5 / st5 / getiri okunmadı; Cemal sayfalarında Ş10 hesaplanmadı).

- YH_ESIK8_SHA: `d28e8257274a85e0301d262d5808e51460fb944f4e5dd56a5f7ade762b03b09c` (8. tur: MACD, dip, Ş10 eşikleri, denemeler, karne v3 hücreleri, BH, Cemal, prefix)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md: Y1-Y11c, 15 bar cetveli, hücre / etiket kuralı AYNEN)
- YH_ESIK6_SHA: `6f05f68cd07560e407c7d1b06431990704b79441c51f4e09bbddfafba4086410` (= ON_KAYIT_6.md)
- YH_ESIK7_SHA: `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26` (= ON_KAYIT_7.md; Y12)
- YH_ESIK_D3_SHA: `0b168445d9882171a1e389169779f710df0b5ec3f529803da786220472136179` (= DEVIR_3_ON_KAYIT.md; karne v3)
- YH_KOD_SHA: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- GE_FN_SHA: `9b6c86fdd23a34b653a611d34cc97a145f41d92c061d2e4665dec85e45f669e6` (GOZ_ETIKET ge_s6 + ge_bolge + ge_ozellik_bar + GE_ESIK 'ozellik' kaynak metni)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json, 1. tur)
- S10_OZELLIK_SHA: `7b75a0ee61f5ccfad8f36e8ff9e76de38c2371179f33dd7879275597371dd00f` (ozellik_Y1_s10.csv.gz; F65-F68, tL2, s65, s66, S10)
- S10_DENETIM_SHA: `09898f68addee360991bf305722af0c5ceeaa50806ba2e8d7d64a16b74909de8` (ozellik_Y1_s10_denetim.json; prefix)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F7 / F10 / F13 / F15 / F17)
- D2_OZELLIK_SHA: `9f164d91401fc025ac8c6db19d65e1c104a3e9a01491383d89636c02f2ffbbdc` (ozellik_Y1_d2.csv.gz; F55 ATRP)
- D3_ESIK_JSON_SHA: `c4a57e438d078737e95f1fdb15d8dad617ceb3c003ea58e578456f78fcf0cc40` (devir3_esik.json; tabaka tercilleri + ambargo; = DEVIR_3_ON_KAYIT)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; regresyon)
- Y9_OLAY_SHA: `56aa6101aba25cddd66dedddcba3d536a05b8e0850b727f015ef3cec295d5809` (olay_Y9.csv.gz; kol B)
- V_ABD_SHA: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e` (V_ABD.pkl)
- V_AVR_SHA: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2` (V_AVR.pkl)
- V_BIST_SHA: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51` (V_BIST.pkl)
- HUNI8_SHA: `3559b198270f984e97a1c454eb6a8ed985c40abec8063d1aa5b36afbb5e3e5a5` (aşağıdaki getirisiz huni; koşuda yeniden hesaplanır, aynı değilse DURUR)
- IS_TANIMI_8: git 80e661c967, 2026-11-20T01:01:49+00:00
- ZAMAN (UTC): `2026-11-20 01:52:14 UTC`

`python YAPI_HEDEF.py kos8` bu dosyanın kontrol listesini, sha'larını, önceki mühürleri (regresyon) ve git kaydını denetler; biri tutmazsa durur. Eşikler iş tanımı §1 AYNEN; sonuç görüldükten sonra değişmez. İkinci koşu durur (sonuc.json'da Y13 varsa).

## İŞ TANIMI 8 §1-§4 (AYNEN)

## 1. Ş10 TANIMI (sabit; sonuç görülünce değişmez)
- MACD(12, 26, 9) kapanış üzerinden: MACD çizgisi = EMA12 − EMA26; sinyal = EMA9(MACD); histogram = MACD − sinyal. EMA'lar [t-250, t] geçerli barlarla (ge_hazir: H > L, V > 0, kriz kesiği), ilk 35 bar ısınma.
- Salınım dipleri: [t-60, t-1] içinde Low'un 5 bar sağ / 5 bar sol yerel minimumu (eşitlikte ilk bar). L2 = t'ye en yakın dip (t-1'e kadar; sağ 5 bar da t'den önce olmalı: yani L2 <= t-6), L1 = L2'den en az 8 bar önceki bir önceki dip (yoksa Ş10 NaN = tutmaz).
- F65 FİYAT ŞARTI: Low(L2) <= Low(L1) x 1,01 (ikinci dip birinciye eşit ya da daha aşağı).
- F66 MACD ŞARTI: MACD(L2) > MACD(L1) VE MACD(L2) < 0 (sıfırın altında, dipte); F66 değeri = (MACD(L2) − MACD(L1)) / Close(L2) (normalize).
- F67 = L2 − L1 (bar); F68 = t barında MACD > sinyal (dönüş teyidi; 0 / 1).
- Ş10 TUTAR ⇔ F65 VE F66 > 0. Ş10t (bilgi) = Ş10 VE F68 = 1.
- Histogram sürümü (bilgi): F66h = hist(L2) − hist(L1) > 0.

## 2. DENEMELER (yön +, giriş t+1 açılış, hat / stop0 Y1 ile aynı)
- Y13 = Y1 olayı ∧ Ş10 (kol A); Y13b = Y9 (dipte) ∧ Ş10 (kol B); Y13c = Y13 ∧ F68 (bilgi). Karşılaştırma: Y1 ∧ NOT Ş10 (uyumsuzluk yok) aynı hücrelerde (bilgi).
- Huni getirisiz ön kayıtta (Y1 -> L1/L2 var -> F65 -> F66 -> Ş10 -> + F68), pazar x dönem.

## 3. ÖLÇÜM: aynı 15 bar cetveli (h5 / es_h5 / st5, KAT5 ay kümeli %95, konum eşli KAT, plasebo); KARNE v3 (60 bar ambargo iki yönde, ABD / AVR ayrı n >= 30, ay kümeli bootstrap alt ucu > 0, leave-3-out, stop payı eşten büyük değil, K1 tabakası F10 / F15 / F7 / F55 ATRP / F13 tercilleri, ters yön bilgi); sınama dönemleri 2023 ve 2024-26 AYRI hücre; karar hücreleri ABD / AVR 2023 ve 2024-26 (bakılmış değil: bu özellik ilk kez ölçülüyor; ama aynı olaylar üzerinde 7 tur ölçüm yapıldığı notu), dış sınama 2016-22, BIST bilgi; etiket kuralı yh_etiket (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ + TERS); BH aile 'bh_tur8' (Y13 / Y13b x 4 hücre, n >= 30). Regresyon: Y1-Y12 eşik sha'ları aynen; Y13* satırları olay_Y1 ile 9 sütunda eşit. Ön kayıt kapısı GE_FN_SHA ve V_*.pkl sha'larını da mühürler (Devir 3 dersi).
## 4. CEMAL UYUMU (bilgi; h5 okunmaz): Ş10'un Cemal'in etiketlediği sayfalarda (hakem KÖR 19, TUR 1, 2, 4, 6) tutma payı x OLUR / OLMAZ; TUR 6'da Cemal'in 'sert düşüş' dediği 5, 9, 30 ve 'iyi' dediği sayfalarda Ş10 var mı (bilgi).

## TANIMLAR ve EŞİKLER (YH_ESIK8; uygulama kararları dahil)

- MACD: {"hizli": 12, "isinma": 35, "pencere": 250, "sinyal": 9, "tanim": "MACD = EMA12(C) - EMA26(C); sinyal = EMA9(MACD); histogram = MACD - sinyal. t için EMA'lar YALNIZ [t-250, t] geçerli barlarıyla (pandas ewm(span, adjust=False): ilk değer tohum); pencerenin ilk 35 barı ısınma (MACD / sinyal NaN). t < 250 ise pencere serinin başından (t-250 yok); ısınma aynı kural", "yavas": 26}
- DIP: {"L1_min_ara": 8, "pencere": 60, "sag": 5, "sol": 5, "tanim": "salınım dibi k: [t-60, t-1] içinde Low'un 5 sol / 5 sağ yerel minimumu; komşular da pencerede (k in [t-55, t-6]); Low_k < min(Low_k-5..k-1) (sol KATI) VE Low_k <= min(Low_k+1..k+5) (sağ eşit izinli): eşit dizide ilk bar dip olur. L2 = t'ye en yakın dip (L2 <= t-6); L1 = L2 - 8'e kadar (L1 <= L2 - 8) en yakın önceki dip; yoksa Ş10 NaN = tutmaz. t < 60 geçerli bar -> NaN"}
- ESIK: {"F65": "s65 = Low(L2) <= Low(L1) x 1,01 (ikili; F65 = Low(L2) / Low(L1) - 1 bilgi sayısı)", "F65_ust": 0.01, "F66": "s66 = MACD(L2) > MACD(L1) VE MACD(L2) < 0 (ikili); F66 = (MACD(L2) - MACD(L1)) / Close(L2); F66m = MACD(L2) / Close(L2)", "F66_alt_acik": 0.0, "F66h": "BİLGİ: (hist(L2) - hist(L1)) / Close(L2) > 0 (histogram sürümü)", "F66m_ust_acik": 0.0, "F67": "L2 - L1 (bar)", "F68": 1.0, "F68_tanim": "t barında MACD > sinyal (0 / 1; dönüş teyidi)", "S10": "Ş10 TUTAR <=> s65 VE s66 (F66 > 0 VE F66m < 0); Ş10t (bilgi) = Ş10 VE F68 = 1", "tL2": "t - L2 (bar; bilgi)"}
- KOL: {"A": "Y1 (bütün olay_Y1.csv.gz satırları)", "B": "Y9 = Y1 VE Ş1 (F15 <= 0,25 VE F17 <= -0,20; goz_etiket/ozellik_Y1; olay_Y9.csv.gz ile küme eşitliği DURUR)"}
- OLCU: "1. tur 15 bar cetveli AYNEN (yh_olc_pazar -> yh_olay_olc, yh_sim; eş: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hedef / takip / 15 bar; plasebo aynı hisse rastgele gün, tohum deneme no = _yh_deneme_no); konum eşli KAT (F15 çeyreği; yh_konum_es_olc); hücre TUTAR / durum / etiket yh_hucre / yh_durum / yh_etiket (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ) + TERS (yh_ters, iki yönlü); karar hücreleri ABD / AVR 2023 ve 2024-26 (bakılmış DEĞİL: Ş10 ilk kez ölçülüyor; aynı Y1 olaylarında 7 tur ölçüm yapıldı notu); dış sınama ABD / AVR 2016-22; BIST bilgi; Y13c bilgi"
- BH: {"aile": "bh_tur8", "q": 0.1, "satir": "Y13 / Y13b x 4 karar hücresi, yalnız n >= 30; p = h5_p (ay kümeli bootstrap KAT5 <= 1 payı)"}
- DENEMELER: {"Y13": {"ad": "Y1 olayı + Ş10 MACD pozitif uyumsuzluk (kol A)", "kol": "A", "sartlar": ["S10"], "yon": 1}, "Y13b": {"ad": "Y9 (Y1 + Ş1 dipte) + Ş10 (kol B)", "kol": "B", "sartlar": ["S10"], "yon": 1}, "Y13c": {"ad": "Y13 + F68 MACD > sinyal (bilgi)", "bilgi": true, "kol": "A", "sartlar": ["S10", "F68"], "yon": 1}}
- KARNE SURUM: karne v3 (DEVİR 3) + sınama dönemleri AYRI hücre
- KARNE ADAY: {"NS10": {"ad": "ters: Y1 VE NOT Ş10 (uyumsuzluk yok)", "tur": "ters"}, "S10": {"ad": "Ş10", "tur": "ana"}, "S10t": {"ad": "Ş10 VE F68 (Y13c)", "tur": "bilgi"}}
- KARNE HUCRE: {"2016-22": "dış sınama (BİLGİ): dönem 2016-22 VE giriş <= ambargo yon2_sinama_son_izinli (2023 başından 60 bar önce)", "2023": "dönem 2023 VE giriş >= devir3_esik.json ambargo yon1_sinama_ilk_izinli (2016-22 sonundan 60 bar sonra)", "2024-26": "dönem 2024-26"}
- KARNE AMBARGO: devir3_esik.json 'ambargo' AYNEN (60 bar, pazar takvimi; iki yön); kol tabanı aynı hücre ve ambargoyla
- KARNE PAZAR: ["ABD", "AVR", "BIST", "ABD+AVR"]
- KARNE KARAR_PAZAR: ["ABD", "AVR"]
- KARNE N_MIN: 30
- KARNE N_KESIN: 1000
- KARNE BOOT: {"B": 2000, "alt": 0.025, "birim": "giriş ayı (YYYY-MM)", "tohum": 1981, "ust": 0.975}
- KARNE GUC: {"R": 1000, "delta": 0.05, "esik": 0.8, "not": "BİLGİ (karar kapısı değil)", "tohum": 1982, "z": 1.959963984540054}
- KARNE TABAKA: {"atrp": "F55", "oz": ["F10", "F15", "F7", "F55", "F13"], "tanim": "tercil sınırları devir3_esik.json 'tabaka' AYNEN (pazar içi 2016-22 Y1). GENEL: MARJ (Ş10 VE kol VE tabaka) - (kol VE tabaka), karar pazarları havuzu (ABD + AVR) x hücre (2023, 2024-26); n >= 30 olan bir tabakada MARJ <= 0 ise KATKI+ -> SORGULA. ATRP: HER karar pazarı x HER hücre x HER F55 tercilinde MARJ sonlu VE > 0 (n = 0 tutmaz)"}
- KARNE OLCU: FARK = ort h5 - ort es_h5 (aynı satır eşi); MARJ = FARK(Ş10 VE kol) - FARK(kol) aynı pazar x hücre x ambargo; stop: ort st5 / ort es_st5; satırlar olay_Y1.csv.gz (yeniden simülasyon yok)
- KARNE ETIKET: kol A ve kol B AYRI; karar pazarları ABD ve AVR AYRI; karar hücreleri 2023 ve 2024-26 AYRI. ÖLÇÜLEMEDİ = bir karar hücresinde n < 30. KATKI+ = her karar hücresinde FARK > 0 VE MARJ > 0 VE MARJ ay kümeli bootstrap %95 alt ucu > 0 VE leave-3-out MARJ > 0 VE st5 olay <= es_st5 eş; VE genel tabaka şartı; VE ATRP şartı. KATKI− = her karar hücresinde MARJ < 0 VE bootstrap %95 üst ucu < 0. Değilse SORGULA. 2016-22 dış sınama, BIST, ABD+AVR, S10t / NS10 BİLGİ
- KARNE KARAR: KATKI+ ilk ölçüm (Ş10 daha önce görülmedi) ama aynı Y1 olaylarında 7 tur ölçüm yapıldı; kesin karar Mart 2027 ileri testi; KATKI− bir karar hücresi n < 1.000 ise kesin değil; ÖLÇÜLEMEDİ iddia kapatmaz
- KARNE YENIDEN_URETIM: ["B", "ABD", "2024-26"]
- CEMAL: {"set": ["hakem (KÖR)", "TUR 1", "TUR 2", "TUR 4", "TUR 6"], "tanim": "sayfa (pazar, sembol, tarih) için Ş10 / F68 veriden yeniden hesaplanır (yh_s10_bar; yalnız t'ye kadar); h5 OKUNMAZ; Cemal OLUR / OLMAZ / BELİRSİZ x Ş10 tutar / tutmaz + Fisher (bilgi). TUR 6 'sert düşüş' = iş tanımındaki 5, 9, 30; 'iyi' = tur_6_cemal_notlar.json'da B = OLUR ve notu 'İYİ' geçen sayfalar", "tur6_iyi": [4, 26, 27, 29, 31, 32, 35, 38, 39, 40], "tur6_sert": [5, 9, 30]}
- PREFIX: özellik dosyası üretiminde pazar başına 25 rastgele Y1 olayı: veri t'de kesilince ve [t-300, t] diliminde = tam veri (rtol 1e-9); değilse DURUR
- GELECEK: koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali (aynı stop0, son sinyal t) + F65-F68 yeniden = dosya (rtol 1e-5; ikili bayraklar aynı); değilse DURUR
- YENİDEN ÜRETİM: RAPOR_8 'YENİDEN ÜRETİM': (1) Y13 ABD 2023 n / P olay / P eş / KAT5 olay_Y13.csv.gz'den düz pandas; (2) karne kol B ABD 2024-26 n / FARK / MARJ olay_Y1 + ozellik_Y1_s10 + ozellik_Y1'den düz pandas; (1) göreli fark > 1e-5 (satır dosyası 6 anlamlı basamak), (2) fark > 1e-9 ise DURUR

UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden önce yazıldı): (1) dip komşuları da [t-60, t-1] penceresinde (k in [t-55, t-6]); (2) 'eşitlikte ilk bar' = sol komşularda katı küçük, sağ komşularda eşit izinli; (3) L1 = L2 - 8'e kadar en yakın önceki dip (iki dip arası en az 8 bar); (4) MACD(L1) pencerenin ısınmasına düşerse (t < 250 kısa seri) NaN = tutmaz; (5) Ş10 bayrakları tam duyarlıkla hesaplanıp 0 / 1 yazılır (F65 sayısı 6 basamakla yalnız bilgi; maske bayraktan); (6) 1. tur cetvelinin 2023 hücresi dönem hücresidir (ambargo yok: kural öğrenilmiyor); karne v3'te 2023 hücresi ambargoludur (devir3_esik.json yon1_sinama_ilk_izinli) ve 2016-22 dış sınaması yon2_sinama_son_izinli'ye kadar; (7) karne v3 kol B karar pazarları da ABD ve AVR (iş tanımı: 'ABD / AVR ayrı n >= 30'); güç BİLGİ; (8) ANA etiket yh_etiket (İZ olabilir: karar hücreleri bakılmış değil) + TERS (yh_ters, iki yönlü kural yh_etiket3'ten); 1. tur cetveli ile karne v3 ayrı raporlanır; (9) Y13c ve Ş10t bilgi; (10) Ş10 var / yok tablosu olay_Y1 satırlarından (bilgi).

## GETİRİSİZ HUNİ (olay sayısı; kol A = Y1, kol B = Y9 dipte)

| Kol | Aşama | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | Y1 olayı (kol) | 8686 | 2042 | 4153 | 4496 | 815 | 1743 | 2588 | 381 | 1759 |
| A | L1 / L2 var | 8308 | 1969 | 3971 | 4313 | 777 | 1666 | 2458 | 348 | 1693 |
| A | + F65 fiyat eşit / daha derin | 3377 | 982 | 1632 | 1768 | 388 | 696 | 1148 | 167 | 950 |
| A | + F66 MACD daha yukarı ve < 0 = Ş10 | 712 | 227 | 385 | 360 | 77 | 158 | 312 | 50 | 306 |
| A | + F68 MACD > sinyal (Y13c) | 685 | 221 | 375 | 346 | 77 | 155 | 310 | 50 | 304 |
| A | (ayrı) NOT Ş10 (uyumsuzluk yok) | 7974 | 1815 | 3768 | 4136 | 738 | 1585 | 2276 | 331 | 1453 |
| A | (ayrı) F66 tek başına (s66) | 1628 | 512 | 862 | 795 | 153 | 331 | 661 | 98 | 583 |
| B | Y1 olayı (kol) | 346 | 146 | 232 | 89 | 20 | 55 | 238 | 81 | 297 |
| B | L1 / L2 var | 338 | 139 | 229 | 86 | 20 | 54 | 238 | 80 | 292 |
| B | + F65 fiyat eşit / daha derin | 244 | 97 | 152 | 59 | 15 | 38 | 161 | 61 | 242 |
| B | + F66 MACD daha yukarı ve < 0 = Ş10 | 123 | 43 | 89 | 28 | 5 | 19 | 98 | 35 | 121 |
| B | + F68 MACD > sinyal (Y13c) | 123 | 43 | 89 | 28 | 5 | 19 | 97 | 35 | 121 |
| B | (ayrı) NOT Ş10 (uyumsuzluk yok) | 223 | 103 | 143 | 61 | 15 | 36 | 140 | 46 | 176 |
| B | (ayrı) F66 tek başına (s66) | 208 | 77 | 151 | 54 | 9 | 32 | 166 | 53 | 163 |

## ÖZELLİK DOSYASI DENETİMİ (prefix; getirisiz)

- ABD: 14881 olay; prefix 25 / 25 tuttu; Ş10 1324; NaN {'F65': 633, 'F66': 633, 'F66m': 633, 'F66h': 633, 'F67': 633, 'F68': 0, 'tL2': 10}
- AVR: 7054 olay; prefix 25 / 25 tuttu; Ş10 595; NaN {'F65': 298, 'F66': 298, 'F66m': 298, 'F66h': 298, 'F67': 298, 'F68': 0, 'tL2': 5}
- BIST: 4728 olay; prefix 25 / 25 tuttu; Ş10 668; NaN {'F65': 229, 'F66': 229, 'F66m': 229, 'F66h': 229, 'F67': 229, 'F68': 0, 'tL2': 14}

## CEMAL SAYFALARI (yalnız sayı; Ş10 hesaplanmadı)

- set başına sayfa: {'TUR 1': 30, 'TUR 2': 30, 'TUR 4': 40, 'TUR 6': 22, 'hakem (KÖR)': 19}
- Cemal etiketi: {'OLUR': 69, 'OLMAZ': 39, 'BELİRSİZ': 33}
- TUR 6 sert düşüş sayfaları: [5, 9, 30]; 'iyi' sayfaları: [4, 26, 27, 29, 31, 32, 35, 38, 39, 40]

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc: aynı giriş günü, aynı OC momentum x likidite kovası, aynı d / hedef / takip / 15 bar); konum eşli KAT (F15 çeyreği); karne v3 MARJ kol tabanına göre aynı pazar x hücre x ambargo, K1 TABAKA F10 / F15 / F7 / F55 ATRP / F13 tercilleri (devir3_esik.json AYNEN), ATRP şartı; ters satır Y1 VE NOT Ş10 aynı hücrelerde |
| K2 | geleceğe bakma | EVET | F65-F68 yalnız [t-250, t] geçerli barlarından (dipler [t-60, t-1], L2 <= t-6, F68 t barı = sinyal günü kapanışı; giriş t+1 açılış); özellik dosyasında pazar başına 25 olay veri t'de kesilince ve [t-300, t] diliminde = tam (denetim json, DURUR); koşuda deneme x pazar 5 olay kesik veriden Y1 sinyali + F65-F68 yeniden (DURUR); Cemal sayfalarında Ş10 yalnız t'ye kadar; tercil / ambargo eşikleri devir3_esik.json (getirisiz, mühürlü) |
| K3 | geçerli bar | EVET | geçerli bar süzgeci _yh_hazir = SY.sy_veri_hazirla (H > L, V > 0, O/H/L/C > 0, kriz kesiği 31.08.2026); EMA, dip ve bar sayıları geçerli bar sırasıyla; 60 bar yoksa / ısınma (35) dolmadıysa NaN = tutmaz |
| K4 | tekilleştirme | EVET | Y13* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (DURUR); n bağımsız olay; getiri ortalama + medyan; bootstrap birimi giriş ayı |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); Y13* ölçülen satırları olay_Y1.csv.gz ile 9 sütunda eşit (h5 / h10 / st5 / es_h5 / es_h10 / es_st5 / n_es / tb_h5 / getiri; DURUR) |
| K6 | veri birimi | EVET | V_*.pkl tek kip (Open / High / Low / Close / Volume); MACD fiyat birimli, F66 / F66m / F66h Close(L2)'ye bölünerek birimsiz; F65 oran; AVR yerel para (hisse içi oran); V_ABD / V_AVR / V_BIST sha ön kayıtta |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan / kottan çıkan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (kol B) yanlılık daha büyük olabilir; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | huni ön kayıtta (getirisiz; Y1 -> L1/L2 var -> F65 -> F66 = Ş10 -> + F68, pazar x dönem, kol A / B); n < 30 ÖLÇÜLEMEDİ ve karne n < 30 olayları listelenir; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; 2023 ve 2024-26 AYRI hücre, ABD ve AVR AYRI; BH 'bh_tur8' (Y13 / Y13b x 4, n >= 30, q 0,10); aynı Y1 olaylarında 7 tur ölçüm notu; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_8.md: YH_ESIK8_SHA + YH_ESIK / ESIK6 / ESIK7 / ESIK_D3 (önceki mühürlere eşit, DURUR) + kod / OC / S6 / GE_FN / güç + ozellik_Y1_s10 / denetim / ozellik_Y1 / ozellik_Y1_d2 / devir3_esik / olay_Y1 / olay_Y9 + V_ABD / V_AVR / V_BIST.pkl sha + HUNI8_SHA; yh_kapi8 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i koşudan ÖNCE; ikinci koşu DURUR; eşikler iş tanımı §1 AYNEN, sonuç görülünce değişmez |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV (V_*.pkl) ve mühürlü özellik / olay dosyaları; Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ) |
| K11 | yeniden üretim | EVET | olay_Y13*.csv.gz satır dosyaları + sonuc.json 'tur8'; RAPOR_8 'YENİDEN ÜRETİM' iki hücre (Y13 ABD 2023 olay dosyasından, göreli 1e-5; karne kol B ABD 2024-26 ham csv'lerden, 1e-9) bağımsız düz pandas koduyla, tutmazsa DURUR |
| K12 | ifade | EVET | etiket yalnız önceden yazılı kurallarla (yh_etiket + TERS; karne v3 KATKI+ / KATKI− / SORGULA / ÖLÇÜLEMEDİ / BİLGİ); Y13c, Ş10 var-yok tablosu, Cemal uyumu 'bilgi'; 'iz değil' ÖLÇÜLEMEDİ için yazılmaz; h5 hedef payı (stop'tan önce +%5), getiri değil; sayı ile yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_s10 / yh_t8 / yh_y8 / YH_ESIK8 / _YH_S10 / YH_KONTROL_8 önekli; tek değişiklik yh_olc_pazar deneme no -> _yh_deneme_no, Y1-Y11c için aynı değer); yasak defter dosyalarına, GOZ_ETIKET.py'ye, tur/* içeriklerine, üretim zincirine dokunulmadı (git diff --stat); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |
