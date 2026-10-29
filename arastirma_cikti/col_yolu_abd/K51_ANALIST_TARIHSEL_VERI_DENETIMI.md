# K52 — ANALİST VERİSİ TARİHSEL DENETİMİ (v1.3, ön kayıt c33a10e)

Kaynak: Yahoo Finance analist not günlüğü (yfinance `upgrades_downgrades`), çekim 29 Ekim 2026. Ücretsiz; EPS revizyonu, gerekçe, analist kişi kimliği, rapor kimliği YOK.

## Kapsama (kaynak grubuna göre)

| deger | hisse | analist_kaydi_olan_hisse | kapsama_oran | kayit |
|---|---|---|---|---|
| K34_tiingo | 422 | 42 | +0.100 | 1116 |
| K34_yahoo | 1435 | 1074 | +0.748 | 50646 |
| V_ABD | 1410 | 1399 | +0.992 | 258806 |

## Yıl yıl kayıt, zaman damgası ve alan doluluğu

| deger | hisse | kayit | saat_var_oran | hedef_var_oran | eski_hedef_var_oran | eski_tavsiye_var_oran | olumlu_oran | olumsuz_oran |
|---|---|---|---|---|---|---|---|---|
| 2011 | 3 | 3 | +1.000 | +0.667 | +0.000 | +0.667 | +0.000 | +0.333 |
| 2012 | 805 | 7719 | +1.000 | +0.881 | +0.731 | +0.237 | +0.581 | +0.372 |
| 2013 | 879 | 8892 | +1.000 | +0.795 | +0.583 | +0.387 | +0.633 | +0.307 |
| 2014 | 926 | 9140 | +1.000 | +0.849 | +0.652 | +0.302 | +0.640 | +0.306 |
| 2015 | 1003 | 9401 | +1.000 | +0.777 | +0.585 | +0.318 | +0.538 | +0.402 |
| 2016 | 1053 | 9946 | +1.000 | +0.612 | +0.475 | +0.359 | +0.527 | +0.389 |
| 2017 | 1043 | 7176 | +1.000 | +0.633 | +0.464 | +0.386 | +0.610 | +0.297 |
| 2018 | 1166 | 12072 | +1.000 | +0.791 | +0.690 | +0.835 | +0.599 | +0.349 |
| 2019 | 1253 | 11190 | +1.000 | +0.822 | +0.629 | +0.403 | +0.604 | +0.342 |
| 2020 | 1447 | 21544 | +1.000 | +0.937 | +0.778 | +0.246 | +0.628 | +0.348 |
| 2021 | 1652 | 18958 | +1.000 | +0.946 | +0.720 | +0.243 | +0.724 | +0.220 |
| 2022 | 1786 | 26935 | +1.000 | +0.961 | +0.821 | +0.202 | +0.363 | +0.586 |
| 2023 | 1978 | 36620 | +1.000 | +0.973 | +0.715 | +0.606 | +0.456 | +0.339 |
| 2024 | 2143 | 44011 | +1.000 | +0.966 | +0.861 | +0.922 | +0.519 | +0.277 |
| 2025 | 2214 | 45511 | +1.000 | +0.974 | +0.906 | +0.938 | +0.497 | +0.366 |
| 2026 | 2207 | 41450 | +1.000 | +0.981 | +0.913 | +0.943 | +0.535 | +0.365 |

## Alanlar

| deger | kaynak | kayit | eksik_oran | baslangic | bitis |
|---|---|---|---|---|---|
| yayım tarih-saati | Yahoo not günlüğü | 310568 | +0.000 | 2011-12-08 | 2026-10-29 |
| kurum kimliği | Yahoo not günlüğü | 310568 | +0.000 | 2011-12-08 | 2026-10-29 |
| önceki tavsiye | Yahoo not günlüğü | 310568 | +0.382 | 2011-12-08 | 2026-10-29 |
| yeni tavsiye | Yahoo not günlüğü | 310568 | +0.000 | 2011-12-08 | 2026-10-29 |
| önceki hedef fiyat | Yahoo not günlüğü | 310568 | +0.223 | 2011-12-08 | 2026-10-29 |
| yeni hedef fiyat | Yahoo not günlüğü | 310568 | +0.081 | 2011-12-08 | 2026-10-29 |
| hedef fiyat revizyon yüzdesi | Yahoo not günlüğü | 310568 | +0.227 | 2011-12-08 | 2026-10-29 |
| EPS / kâr tahmini revizyonu | YOK (Yahoo günlüğünde bulunmuyor) |  | +1.000 |  |  |
| rapor gerekçesi ve riskler | YOK (Yahoo günlüğünde bulunmuyor) |  | +1.000 |  |  |
| analist kişi kimliği | YOK (Yahoo günlüğünde bulunmuyor) |  | +1.000 |  |  |
| rapor kimliği / tarihsel sürüm | YOK (Yahoo günlüğünde bulunmuyor) |  | +1.000 |  |  |

## Zaman sızıntısı ve güvenilirlik

- Kural: olay günü d için yalnız tarih <= d-1 kayıtları (saat dilimi belgelenmediğinden aynı gün kayıtları kullanılmadı). Giriş d+1 açılışı. Hedef fiyatlar kayıt anındaki değer; sonraki güncelleme kullanılmadı. Aynı kurum aynı tarih tek kayıt.
- Zaman damgası: kayıtların saat bilgisi olan payı yıl tablosundadır; saat 00:00 olan kayıtların gün içi sırası bilinmez. Saat dağılımı 10-16 UTC'de yoğundur (ABD piyasa öncesi notları), bu yüzden damga UTC kabul edildi; aynı gün kayıtları zaten dışarıda.
- Tarihsel sürüm: Yahoo günlüğü olay kaydıdır; geriye dönük yeniden yazılıp yazılmadığı doğrulanamaz. Bu yüzden sonuçlar 'sağlayıcı günlüğü doğru kabul edilerek' okunmalıdır.
- Hayatta kalma / seçilim: P1 ve P2 olaylarında sembolün d'den önce kaydı olan pay +0.942; kaydı olmayanlar G2b / G4b alt grubudur, olumsuz görüşle karıştırılmadı. Borsadan çıkmış şirketlerde veri çoğunlukla yoktur (yukarıdaki kaynak tablosu).
- Ölçülemeyen hipotez: H1 (EPS revizyonu) — alan yok; karar verilmedi.

