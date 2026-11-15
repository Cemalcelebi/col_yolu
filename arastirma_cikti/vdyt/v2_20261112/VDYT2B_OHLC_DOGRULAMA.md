# VDYT2-B — Tiingo batan şirket OHLC doğrulaması (İŞ 1; yalnız önbellek, yeni istek yok)

Üretim: 2026-11-12 20:25:16 UTC (`python KOR_TEST.py ohlc`). Tiingo fiyat değerleri lisans gereği bu dosyada TABLO olarak yok; yalnız sayımlar, oranlar ve birkaç tekil karşılaştırma değeri. Örnek grafikler (Form 25 öncesi son 120 bar, mum + hacim) /tmp/vdyt2b/ohlc_ornek/ (repoya girmez).

## SONUÇ: Tiingo batanlarda OHLC: **KISMEN**

- Batan şirketin borsa dönemi OHLC'si: VAR 8 / KISMEN 3 / YOK 1 (12 sembol).
  - SIVBQ: KISMEN — Form 25 öncesi 12 donuk bar (O = H = L = C = önceki kapanış: işlem durması dolgusu ya da işlemsiz gün; bir kısmı hacimli, bar temizliği atmaz) ayıklanmalı
  - BBBYQ: VAR — tam
  - RADCQ: VAR — tam
  - WEWKQ: KISMEN — Form 25 öncesi 11 donuk bar (O = H = L = C = önceki kapanış: işlem durması dolgusu ya da işlemsiz gün; bir kısmı hacimli, bar temizliği atmaz) ayıklanmalı
  - SHLDQ: VAR — tam
  - HTZGQ: VAR — tam
  - REVRQ: VAR — tam
  - YELLQ: VAR — tam
  - DNR: VAR — tam
  - GNC: VAR — tam
  - SUNE: YOK — kayıt bugünkü SUNation (eski CSI) serisi; SunEdison fiyatı yok
  - CHK: KISMEN — eski şirket 2021-02-09'a kadar tam; sonrasında donuk dolgu + 2024-10-04 tek yabancı bar (kesilmeli)
- Hüküm kuralı (betimleyici; bu iş için veri keşfinden sonra yazıldı, ön kayıtlı DEĞİL; pilot kararı KISMEN değişmez): VAR = Form 25 öncesi >= 252 bar, OHLCV dolu >= %99, iç tutarlılık ihlali 0, sıfır / negatif fiyat 0, düzeltme katsayısı olay dışında değişmiyor, donuk dolgu <= 3 bar ve kayıt batan şirketi taşıyor; KISMEN = taşıyor ama temizlik gerekiyor; YOK = batan şirketin fiyatı kayıtta yok. Genel: VAR >= 10 -> VAR; VAR + KISMEN >= 8 -> KISMEN; aksi YOK.

## 1. Sembol tablosu (sayılar)

| kod | tür | pilot | bar | ilk | son | Form 25 öncesi bar | OHLCV dolu | iç ihlal | sıfır/neg | hacim 0 payı | donuk bar (F25 öncesi / hacimli) | son 60: H=L payı | son 60: medyan (H-L)/C | aralık oranı son60 / 1 yıl önce | OTC H=L payı | sıçrama (F25 önce / sonra / geri dönen) | > 15 gün boşluk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SIVBQ | Q | kaldı | 3.874 | 2010-01-04 | 2026-08-31 | 3.354 | 1,000 | 0 | 0 | 0,037 | 12 (165 toplam / 21 hacimli) | 0,200 | 0,0431 | 1,03 | 0,310 | 1 / 4 / 2 | 1 |
| BBBYQ | Q | GEÇTİ | 3.459 | 2010-01-04 | 2023-09-29 | 3.400 | 1,000 | 0 | 0 | 0,000 | 0 (0 toplam / 0 hacimli) | 0,000 | 0,1755 | 1,88 | 0,000 | 0 / 0 / 0 | 0 |
| RADCQ | Q | kaldı | 3.829 | 2010-01-04 | 2026-08-31 | 3.480 | 1,000 | 0 | 0 | 0,036 | 1 (144 toplam / 6 hacimli) | 0,017 | 0,1627 | 2,28 | 0,413 | 0 / 2 / 1 | 1 |
| WEWKQ | Q | GEÇTİ | 915 | 2020-10-21 | 2024-06-11 | 777 | 1,000 | 0 | 0 | 0,003 | 11 (16 toplam / 13 hacimli) | 0,033 | 0,1499 | 1,85 | 0,058 | 0 / 0 / 0 | 0 |
| SHLDQ | Q | GEÇTİ | 3.230 | 2010-01-04 | 2022-10-31 | 2.234 | 1,000 | 0 | 0 | 0,000 | 0 (34 toplam / 34 hacimli) | 0,000 | 0,1529 | 2,80 | 0,067 | 0 / 0 / 0 | 0 |
| HTZGQ | Q | GEÇTİ | 2.893 | 2010-01-04 | 2021-06-30 | 2.726 | 1,000 | 0 | 0 | 0,000 | 0 (0 toplam / 0 hacimli) | 0,000 | 0,0656 | 1,88 | 0,000 | 0 / 0 / 0 | 0 |
| REVRQ | Q | GEÇTİ | 3.371 | 2010-01-04 | 2023-05-24 | 3.223 | 1,000 | 0 | 0 | 0,005 | 0 (17 toplam / 0 hacimli) | 0,000 | 0,0846 | 2,21 | 0,115 | 0 / 0 / 0 | 0 |
| YELLQ | Q | kaldı | 4.147 | 2010-01-04 | 2026-07-01 | 3.443 | 1,000 | 0 | 0 | 0,003 | 0 (160 toplam / 148 hacimli) | 0,000 | 0,2039 | 2,88 | 0,331 | 0 / 27 / 7 | 0 |
| DNR | BORSA | GEÇTİ | 2.662 | 2010-01-04 | 2020-07-30 | 2.662 | 1,000 | 0 | 0 | 0,000 | 2 (2 toplam / 1 hacimli) | 0,033 | 0,0874 | 1,19 | - | 0 / 0 / 0 | 0 |
| GNC | BORSA | GEÇTİ | 2.327 | 2011-04-01 | 2020-06-30 | 2.327 | 1,000 | 0 | 0 | 0,000 | 1 (1 toplam / 1 hacimli) | 0,017 | 0,1158 | 1,87 | - | 0 / 0 / 0 | 0 |
| SUNE | YENIDEN | kaldı | 4.190 | 2010-01-04 | 2026-08-31 | 1.596 | 1,000 | 0 | 0 | 0,000 | 1 (3 toplam / 3 hacimli) | 0,000 | 0,0291 | 1,19 | 0,002 | 0 / 0 / 0 | 0 |
| CHK | YENIDEN | kaldı | 2.809 | 2010-01-04 | 2024-10-04 | 2.653 | 1,000 | 0 | 0 | 0,004 | 1 (14 toplam / 2 hacimli) | 0,017 | 0,1556 | 2,85 | 0,090 | 0 / 1 / 0 | 1 |

## 2. Düzeltilmiş alanlar (adjOpen / adjHigh / adjLow / adjClose) ve bölünme / temettü katsayısı

| kod | adj alanları dolu | O/H/L/C aynı gün katsayı farkı (gün; maks) | katsayı değişen gün | olay dışı değişim | olay günü (bölünme / temettü) | olayda beklenen orandan sapma > %0,5 |
|---|---|---|---|---|---|---|
| SIVBQ | evet | 0 (0,00000000) | 0 | 0 | 0 (0 / 0) | 0 |
| BBBYQ | evet | 0 (0,00000000) | 16 | 0 | 16 (0 / 16) | 0 |
| RADCQ | evet | 0 (0,00000000) | 1 | 0 | 1 (1 / 0) | 0 |
| WEWKQ | evet | 0 (0,00000000) | 1 | 0 | 1 (1 / 0) | 0 |
| SHLDQ | evet | 0 (0,00000000) | 1 | 0 | 1 (0 / 1) | 1 |
| HTZGQ | evet | 0 (0,00000000) | 2 | 0 | 2 (2 / 0) | 0 |
| REVRQ | evet | 0 (0,00000000) | 0 | 0 | 0 (0 / 0) | 0 |
| YELLQ | evet | 0 (0,00000000) | 2 | 0 | 2 (2 / 0) | 0 |
| DNR | evet | 0 (0,00000000) | 7 | 0 | 7 (0 / 7) | 0 |
| GNC | evet | 0 (0,00000000) | 20 | 0 | 20 (0 / 20) | 0 |
| SUNE | evet | 0 (0,00000000) | 47 | 0 | 47 (4 / 43) | 1 |
| CHK | evet | 0 (0,00000000) | 23 | 0 | 23 (1 / 22) | 0 |

Olay günü sapmaları (bölünme / temettü dışında katsayı hiç değişmiyor; bölünmelerin hepsi beklenen oranla aynı): SHLDQ 2014-04-07 (sapma -1,3 %); SUNE 2021-10-18 (sapma 1,5 %) — bunlar özel dağıtım (spin-off / özel temettü) günleri; Tiingo farklı referans fiyat kullanıyor.

Sıçrama günleri (|günlük ln getiri| > ln 10, bölünme günü değil):
- SIVBQ: 2023-03-28, 2024-03-05, 2024-03-06, 2024-03-11, 2024-03-12
- RADCQ: 2024-06-21, 2024-06-24
- YELLQ: 2025-08-21, 2025-08-22, 2025-10-29, 2025-10-30, 2025-12-23, 2025-12-24, 2026-01-26, 2026-01-27, 2026-03-09, 2026-03-16, 2026-03-31, 2026-04-02
- CHK: 2024-10-04

## 3. Bağımsız kaynakla karşılaştırma

- SUNE k60 yahoo: ortak 4.190 gün (2010-01-04 .. 2026-08-31); medyan |oran - 1| açılış 0,000000, yüksek 0,000000, düşük 0,000000, kapanış 0,000000; %1 içinde pay A/Y/D/K 0,974 / 0,976 / 0,976 / 0,973; kapanış getiri korelasyonu 0,9932.
- SUNE k34 yahoo: ortak 1.485 gün (2020-10-01 .. 2026-08-31); medyan |oran - 1| açılış 0,000000, yüksek 0,000000, düşük 0,000000, kapanış 0,000000; %1 içinde pay A/Y/D/K 0,754 / 0,756 / 0,754 / 0,747; kapanış getiri korelasyonu 0,9856.
- SUNE SunEdison dönemi: Form 25 öncesi 18 ayda 379 bar, medyan günlük işlem değeri 55689 $ (SunEdison bu dönemde günde yüz milyonlarca dolar işlem gören bir NYSE hissesiydi; seri bugünkü SUNation / eski CSI'nin küçük hacimli serisi). Tiingo SUNE kaydı yukarıdaki Yahoo SUNE ile 2010'dan beri aynı: SunEdison fiyatı bu kayıtta YOK (pilotta ayrı NYSE 1995-2016 kaydı listede görünüyordu; API kodu yeni kayda çözüyor).
- CHK: eski şirketin son gerçek barı 2021-02-09; 2021-02-10 ve sonrası 14 bar, bunların 13'i donuk dolgu, hacimli bar 2; en uzun boşluk 1.313 takvim günü. Yeni şirket (bugün EXE) bu kayıtta YOK; kayıt KARIŞIK değil, eski şirketi taşıyor.
  - Tekil karşılaştırma 2024-10-04: Tiingo CHK kapanış 81,46 $ (hacim 844); k60 EXE aynı gün açılış / yüksek / düşük / kapanış 84,93 / 86,00 / 84,55 / 85,63 $ -> EXE gün aralığında: hayır (yabancı bar).
- SIVB 2023-03-09: Tiingo kapanış 106,04 $ = basın kapanışı 106,04 $; aynı gün açılış / yüksek / düşük 176,55 / 177,75 / 100,00 $ (önceki kapanış 267,83 $; açılış / yüksek / düşük için yerelde bağımsız kaynak YOK, iç tutarlılık geçti). İşlem durması (2023-03-10 .. 03-27) 12 bar, 12'i donuk dolgu (4'i hacimli: VDYT bar temizliği hacimsiz barı atar, hacimli donuk barı ATMAZ).

## 4. Ne demek (Cemal için)

- Batan şirketlerin çoğunda borsa dönemi açılış / yüksek / düşük / kapanış / hacim tam ve kendi içinde tutarlı; mum grafiği çizilebilir, G5 hesaplanabilir.
- İki tuzak var: (1) işlem durması günleri aynı fiyatla 'donuk' doldurulmuş (bazıları küçük hacimli); bunlar sessiz bölge gibi görünür, temizlenmeden kullanılmamalı. (2) Kod yeniden kullanımında Tiingo kodu BUGÜNKÜ kayda bağlıyor: SUNE'de SunEdison yok; CHK'de eski şirket var ama sonuna yabancı bir bar eklenmiş. B testinde yinelenen kodlar zaten atılıyor (VDYT2-B 2.2 kural 3).
- Bağımsız sağlama sınırlı: kapanış (SIVB) ve tam OHLC (SUNE, yalnız bugünkü şirket) tuttu; batan şirketlerin açılış / yüksek / düşük değerleri için yerelde ikinci kaynak yok.
