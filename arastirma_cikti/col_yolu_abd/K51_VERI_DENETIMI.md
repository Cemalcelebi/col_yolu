# K51 — VERİ BÜTÜNLÜĞÜ DENETİMİ (v1.2, ön kayıt 8e99902)

K51 kararı değişmez. Bu belge veri evreninin sınırlarını belgeler.

## V1 Sayı uzlaşması

| Sayı | Değer | Açıklama |
|---|---|---|
| İşlenen tekil sembol (ABD) | 3267 | V_ABD 1410 + K34 Yahoo 1435 + K34 Tiingo 422; örtüşme yok (aynı sembol iki kez yüklenmez) |
| Likidite süzgecinden en az bir gün geçen | 2752 | bu çalışmanın paneli; K51 raporundaki 2.752 bu sayıdır |
| Hiç likit günü olmayan | 515 | işlem değeri < 1 M$ ya da pazar içi alt %20, fiyat < 1 $, evren girişi geç |
| Panel satırı (likit hisse-gün, etiketli) | 3175671 | |
| Yinelenen K34 sembolü | 4 | aynı kod, FARKLI CIK (kod sonradan başka şirkete geçmiş); yüklemede ikinci şirket atlandı |

| cik | sembol | kaynak | ilk_giris | batan | w |
|---|---|---|---|---|---|
| 1144519 | BG | tiingo | 2021-02-22 | True | +1.831 |
| 1996862 | BG | yahoo | 2026-04-30 | False | +1.000 |
| 912603 | RDUS | tiingo | 2021-01-08 | True | +1.831 |
| 1428522 | RDUS | tiingo | 2022-05-06 | True | +1.831 |
| 912752 | SBGI | tiingo | 2022-03-02 | True | +1.831 |
| 1971213 | SBGI | yahoo | 2024-08-12 | False | +1.000 |
| 1403752 | ZYME | tiingo | 2022-08-05 | True | +1.831 |
| 1937653 | ZYME | yahoo | 2022-11-09 | False | +1.000 |

Şirket kimliği (CIK) ve sembol kimliği K51_EVREN_PIT.csv'de ayrı sütunlardadır. Fiyat verisi sembole bağlıdır; CIK yalnız K34 şirketlerinde bilinir.

## V2 Point-in-time evren tablosu

K51_EVREN_PIT.csv (3267 satır): sembol, CIK, kaynak, evren girişi ve dayanağı, ilk / son fiyat günü, son kapanış, son 60 gün getirisi, çıkış türü tahmini, son SEC bildirimi, kod yeniden kullanımı şüphesi.

## V3 2016-20 eğitim evreni

- Evrene 2021 öncesi giren hisse: 1203 (hepsi V_ABD = bugün işlem görenler). K34 girişleri 2021-01-08 ve sonrası.
- 2016-20 dönemi yalnız hayatta kalanlardan oluşur; doldurulmadı. Bu dönemin hücreleri bu yüzden iyimser olabilir; kaynak kırılımı K51_KIRILGANLIK.md'de.

## V4 Çıkış sınıflaması (tahmin; gerçek delist nedeni değil)

| kaynak | cikis_turu_tahmin | sec_bildirimi_suruyor | n |
|---|---|---|---|
| K34_tiingo | batma benzeri | False | 50 |
| K34_tiingo | batma benzeri | True | 1 |
| K34_tiingo | belirsiz çıkış | False | 27 |
| K34_tiingo | işlem görüyor | False | 153 |
| K34_tiingo | işlem görüyor | True | 12 |
| K34_tiingo | satın alma / birleşme benzeri | False | 171 |
| K34_tiingo | satın alma / birleşme benzeri | True | 8 |
| K34_yahoo | işlem görüyor | False | 96 |
| K34_yahoo | işlem görüyor | True | 1339 |
| V_ABD | işlem görüyor | False | 993 |
| V_ABD | işlem görüyor | True | 417 |

- 'sec_bildirimi_suruyor' = şirketin (yüklenen CIK) son 10-K / 10-Q bildirimi 31.08.2026'dan en çok 120 gün önce ya da sonra: şirket yaşıyor. Tiingo serisi sürüp şirket bildirim vermiyorsa kod başka şirkete geçmiş olabilir (V8).
- Yinelenen 4 sembolde (BG, RDUS, SBGI, ZYME) iki CIK aynı şirketin yeniden kaydı (yeniden yapılanma / yer değişimi) ya da kodun yeni şirkete geçişi olabilir; K34 evreninde 'batan' sayılıp 1,83 ağırlık almışlardır, seri bugün sürüyor.

- Kural: seri 2026-08-01'den önce bitiyorsa çıkış; son 60 gün getirisi <= -50% ya da son kapanış < 1.0 $ -> 'batma benzeri'; son 60 gün >= 0 -> 'satın alma / birleşme benzeri'; arası 'belirsiz çıkış'.
- Tiingo örneklemi tam batan evreni DEĞİLDİR: SEC nakit pisti olan ve kodu kapakta bulunan şirketlerden 450'lik rastgele örneklem (K34, ağırlık 1,83); K34 dışındaki (nakit sorunu olmayan) batanlar evrende yoktur.
- Kod yeniden kullanımı şüphesi (Tiingo / Yahoo serisi şirketin son SEC bildiriminden 120 günden fazla sürüyor ve seri bugün devam ediyor): 249 hisse. Bu serilerde eski şirketin fiyatları, kodu sonradan alan şirketin fiyatlarıyla birleşmiş olabilir (V8 senaryosu).

## V5 / V6 / V8 Duyarlılık senaryoları (olay isabeti - K51 tabanı; ağırlıklı)

Senaryolar varsayımsaldır: 'ana' = seri vadeden önce bitince son kapanış, son 60 gün eksiyse ek -%30; 'delist %0' = ek kayıp yok; 'delist -%100' = tam kayıp; 'V8 kod kesme' = K34 serisi son SEC bildirimi + 120 günde kesilir (kesilen seri borsadan çıkmış sayılır), yalnız kesmeden önceki olaylar. Baz fiyat = serinin son kapanışı; uygulama günü = serinin son günü.

| kume | donem | senaryo | n | isabet | taban | fark | fark_alt | fark_ust | net | etkilenen_olay | seri_sonunda_cikan_olay |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 2016-22 | ana (-%30) | 1415 | +0.286 | +0.268 | +0.018 | -0.005 | +0.042 | -0.026 | 0 | 27 |
| P1 | 2016-22 | delist %0 | 1415 | +0.286 | +0.268 | +0.018 | -0.004 | +0.043 | -0.026 | 0 | 27 |
| P1 | 2016-22 | delist -%100 | 1415 | +0.286 | +0.268 | +0.018 | -0.003 | +0.041 | -0.026 | 0 | 27 |
| P1 | 2016-22 | V8 kod kesme | 1415 | +0.286 | +0.268 | +0.018 | -0.005 | +0.042 | -0.026 | 0 | 27 |
| P1 | 2023 | ana (-%30) | 906 | +0.313 | +0.288 | +0.025 | -0.006 | +0.060 | -0.018 | 0 | 42 |
| P1 | 2023 | delist %0 | 906 | +0.313 | +0.288 | +0.025 | -0.006 | +0.058 | -0.018 | 0 | 42 |
| P1 | 2023 | delist -%100 | 906 | +0.313 | +0.288 | +0.025 | -0.005 | +0.058 | -0.018 | 0 | 42 |
| P1 | 2023 | V8 kod kesme | 905 | +0.311 | +0.287 | +0.024 | -0.005 | +0.060 | -0.019 | 0 | 42 |
| P1 | 2024-26 | ana (-%30) | 1316 | +0.357 | +0.333 | +0.024 | +0.001 | +0.049 | -0.011 | 0 | 23 |
| P1 | 2024-26 | delist %0 | 1316 | +0.357 | +0.333 | +0.024 | +0.000 | +0.050 | -0.011 | 0 | 23 |
| P1 | 2024-26 | delist -%100 | 1316 | +0.357 | +0.333 | +0.024 | +0.000 | +0.050 | -0.011 | 0 | 23 |
| P1 | 2024-26 | V8 kod kesme | 1300 | +0.356 | +0.334 | +0.022 | -0.003 | +0.049 | -0.011 | 0 | 23 |
| P2 | 2016-22 | ana (-%30) | 571 | +0.255 | +0.269 | -0.013 | -0.045 | +0.020 | -0.022 | 0 | 9 |
| P2 | 2016-22 | delist %0 | 571 | +0.255 | +0.269 | -0.013 | -0.047 | +0.018 | -0.022 | 0 | 9 |
| P2 | 2016-22 | delist -%100 | 571 | +0.255 | +0.269 | -0.013 | -0.045 | +0.019 | -0.022 | 0 | 9 |
| P2 | 2016-22 | V8 kod kesme | 571 | +0.252 | +0.268 | -0.016 | -0.048 | +0.015 | -0.027 | 2 | 9 |
| P2 | 2023 | ana (-%30) | 476 | +0.286 | +0.276 | +0.010 | -0.026 | +0.057 | -0.020 | 0 | 25 |
| P2 | 2023 | delist %0 | 476 | +0.286 | +0.276 | +0.010 | -0.026 | +0.057 | -0.020 | 0 | 25 |
| P2 | 2023 | delist -%100 | 476 | +0.286 | +0.276 | +0.010 | -0.026 | +0.059 | -0.020 | 0 | 25 |
| P2 | 2023 | V8 kod kesme | 475 | +0.283 | +0.275 | +0.008 | -0.027 | +0.055 | -0.021 | 0 | 25 |
| P2 | 2024-26 | ana (-%30) | 667 | +0.324 | +0.318 | +0.006 | -0.018 | +0.036 | -0.021 | 0 | 13 |
| P2 | 2024-26 | delist %0 | 667 | +0.324 | +0.318 | +0.006 | -0.019 | +0.035 | -0.021 | 0 | 13 |
| P2 | 2024-26 | delist -%100 | 667 | +0.324 | +0.318 | +0.006 | -0.017 | +0.035 | -0.021 | 0 | 13 |
| P2 | 2024-26 | V8 kod kesme | 661 | +0.326 | +0.318 | +0.008 | -0.018 | +0.038 | -0.021 | 0 | 13 |
| HT | 2016-22 | ana (-%30) | 163 | +0.340 | +0.305 | +0.035 | -0.048 | +0.121 | -0.013 | 0 | 9 |
| HT | 2016-22 | delist %0 | 163 | +0.340 | +0.305 | +0.035 | -0.050 | +0.124 | -0.013 | 0 | 9 |
| HT | 2016-22 | delist -%100 | 163 | +0.340 | +0.305 | +0.035 | -0.049 | +0.118 | -0.013 | 0 | 9 |
| HT | 2016-22 | V8 kod kesme | 162 | +0.342 | +0.303 | +0.039 | -0.047 | +0.121 | -0.012 | 0 | 9 |
| HT | 2023 | ana (-%30) | 58 | +0.276 | +0.331 | -0.055 | -0.143 | +0.037 | -0.045 | 0 | 5 |
| HT | 2023 | delist %0 | 58 | +0.276 | +0.331 | -0.055 | -0.148 | +0.033 | -0.045 | 0 | 5 |
| HT | 2023 | delist -%100 | 58 | +0.276 | +0.331 | -0.055 | -0.151 | +0.031 | -0.045 | 0 | 5 |
| HT | 2023 | V8 kod kesme | 57 | +0.264 | +0.325 | -0.061 | -0.154 | +0.036 | -0.048 | 0 | 5 |
| HT | 2024-26 | ana (-%30) | 191 | +0.331 | +0.343 | -0.012 | -0.061 | +0.039 | -0.027 | 0 | 4 |
| HT | 2024-26 | delist %0 | 191 | +0.331 | +0.343 | -0.012 | -0.062 | +0.040 | -0.027 | 0 | 4 |
| HT | 2024-26 | delist -%100 | 191 | +0.331 | +0.343 | -0.012 | -0.060 | +0.043 | -0.027 | 0 | 4 |
| HT | 2024-26 | V8 kod kesme | 191 | +0.331 | +0.344 | -0.013 | -0.060 | +0.045 | -0.027 | 0 | 4 |

- 'etkilenen_olay' = senaryoda net getirisi değişen olay sayısı; 'seri_sonunda_cikan_olay' = serisi 01.08.2026'dan önce biten hissedeki olay sayısı (delist kuralının uygulanabildiği küme). Üst bariyer etiketi (y) delist cezasından etkilenmez; yalnız net getiri etkilenir.

## V6 Ham ve düzeltilmiş fiyat (yalnız Tiingo altkümesi; Yahoo serileri yalnız düzeltilmiş)

- Tiingo hisse 253, likit satır 80510: ham fiyatla etiket uyumu +0.997; olay satırı 280: uyum +0.996.
- Sınır: düzeltilmiş fiyatla bariyer, temettü ve bölünme sonrası gerçek işlem fiyatından sapabilir; Yahoo altkümesinde ölçülemedi. Temettü, düşüş sonrası küçük hisselerde azdır.

## V7 Eski kod (29 Ekim düzeltmelerinden önce) ve yeni kod

- eski kod b3835d8 aynı veride yeniden koşuldu (3267 hisse); CNN / LSTM / meta koşulmadı (olay ve taban kıyası)
- Olay tespiti iki sürümde aynıdır; farklar taban (ağırlık, belirsiz, batan bayrağı) ve piyasa kıyasındadır.

| kod | kume | donem | n | isabet | taban | fark | fark_alt | net |
|---|---|---|---|---|---|---|---|---|
| eski_b3835d8 | P1 | 2016-22 | 1415 | +0.284 | +0.268 | +0.016 | -0.006 | -0.026 |
| eski_b3835d8 | P1 | 2023 | 906 | +0.318 | +0.286 | +0.031 | -0.001 | -0.016 |
| eski_b3835d8 | P1 | 2024-26 | 1316 | +0.359 | +0.334 | +0.025 | +0.001 | -0.011 |
| eski_b3835d8 | P2 | 2016-22 | 571 | +0.250 | +0.268 | -0.017 | -0.048 | -0.026 |
| eski_b3835d8 | P2 | 2023 | 476 | +0.286 | +0.274 | +0.012 | -0.019 | -0.020 |
| eski_b3835d8 | P2 | 2024-26 | 667 | +0.327 | +0.320 | +0.007 | -0.018 | -0.020 |
| eski_b3835d8 | ES | 2016-22 | 2316 | +0.299 | +0.289 | +0.009 | -0.009 | -0.025 |
| eski_b3835d8 | ES | 2023 | 896 | +0.312 | +0.314 | -0.001 | -0.025 | -0.021 |
| eski_b3835d8 | ES | 2024-26 | 2382 | +0.340 | +0.335 | +0.005 | -0.020 | -0.008 |
| eski_b3835d8 | HT | 2016-22 | 163 | +0.337 | +0.309 | +0.028 | -0.056 | -0.013 |
| eski_b3835d8 | HT | 2023 | 58 | +0.293 | +0.338 | -0.045 | -0.138 | -0.040 |
| eski_b3835d8 | HT | 2024-26 | 191 | +0.335 | +0.345 | -0.009 | -0.057 | -0.027 |
| yeni_v1.2 | P1 | 2016-22 | 1415 | +0.286 | +0.268 | +0.018 | -0.005 | -0.026 |
| yeni_v1.2 | P1 | 2023 | 906 | +0.313 | +0.288 | +0.025 | -0.006 | -0.018 |
| yeni_v1.2 | P1 | 2024-26 | 1316 | +0.357 | +0.333 | +0.024 | +0.000 | -0.011 |
| yeni_v1.2 | P2 | 2016-22 | 571 | +0.255 | +0.269 | -0.013 | -0.045 | -0.022 |
| yeni_v1.2 | P2 | 2023 | 476 | +0.286 | +0.276 | +0.010 | -0.025 | -0.020 |
| yeni_v1.2 | P2 | 2024-26 | 667 | +0.324 | +0.318 | +0.006 | -0.017 | -0.021 |
| yeni_v1.2 | ES | 2016-22 | 2316 | +0.300 | +0.289 | +0.010 | -0.010 | -0.025 |
| yeni_v1.2 | ES | 2023 | 896 | +0.311 | +0.313 | -0.002 | -0.028 | -0.021 |
| yeni_v1.2 | ES | 2024-26 | 2382 | +0.342 | +0.334 | +0.008 | -0.017 | -0.007 |
| yeni_v1.2 | HT | 2016-22 | 163 | +0.340 | +0.305 | +0.035 | -0.053 | -0.013 |
| yeni_v1.2 | HT | 2023 | 58 | +0.276 | +0.331 | -0.055 | -0.145 | -0.045 |
| yeni_v1.2 | HT | 2024-26 | 191 | +0.331 | +0.343 | -0.012 | -0.061 | -0.027 |
