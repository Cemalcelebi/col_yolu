# INTEM İLERİ TEST — RAPOR (INTEM_ILERI v1.0 (2026-11-14))

Koşu: 2026-11-14T14:18:31Z -> 2026-11-14T14:24:17Z (346 sn). Ön kayıt git: {'commit': 'bf0334defe64eaf945f7adeb817399863fc56f70', 'commit_zamani': '2026-11-14T14:18:21+00:00'}; modül git: {'commit': 'bf0334defe64eaf945f7adeb817399863fc56f70', 'commit_zamani': '2026-11-14T14:18:21+00:00'}.

## DÜZ DİL ÖZET

**Ç124 kuralı görülmemiş veride ÖLÇÜLEMEDİ (n ya da güç yetersiz; iddia kapanmaz).**

- Görülmemiş veri: yalnız ABD k34 ekinin 1465 hissesi (nakit yakan, bugün işlem gören, 2021+). Avrupa Ç124'te kullanıldığı için görülmemiş değil; AVR karar hücreleri boş.
- ORTAK CETVEL genel etiket (L = 20): **ÖLÇÜLEMEDİ**; olasılık etiketi **ÖLÇÜLEMEDİ**.
- ABD 2016-22 (keşif, bilgi): n 37, 60 gün eşli fark +4,2 puan [%95 -11,3, +19,4], medyan -8,2; 12 ayda +%100 eşlerin 0,85 katı, -%50 eşlerin 1,04 katı (n250 37) -> ÖLÇÜLEMEDİ.
- ABD 2023: n 26, 60 gün eşli fark -3,2 puan [%95 -19,8, +31,6], medyan -8,1; 12 ayda +%100 eşlerin 1,03 katı, -%50 eşlerin 1,02 katı (n250 26) -> ÖLÇÜLEMEDİ.
- ABD 2024-26: n 42, 60 gün eşli fark -7,5 puan [%95 -17,8, +2,9], medyan -10,5; 12 ayda +%100 eşlerin 0,58 katı, -%50 eşlerin 1,42 katı (n250 33) -> ÖLÇÜLEMEDİ.
- Ç124'ün kendi ölçüsü, 2016-26 (hepsi): 20 günde önce +%8 %47,6 (oynaklık eşli rastgele %44,9; fark +2,7 puan, %95 [-6,8, +12,2]), önce -%8 %49,5 (rastgele %48,7); n 105 -> Ç124 kuralıyla TUTMAZ (bilgi).
- Ç124'ün kendi ölçüsü, 2016-22: 20 günde önce +%8 %51,4 (oynaklık eşli rastgele %42,7; fark +8,6 puan, %95 [-7,6, +22,2]), önce -%8 %40,5 (rastgele %51,4); n 37 -> Ç124 kuralıyla TUTMAZ (bilgi).
- Ç124'ün kendi ölçüsü, 2023: 20 günde önce +%8 %42,3 (oynaklık eşli rastgele %41,5; fark +0,8 puan, %95 [-18,5, +20,0]), önce -%8 %57,7 (rastgele %51,2); n 26 -> Ç124 kuralıyla n < 30 (bilgi).
- Ç124'ün kendi ölçüsü, 2024-26: 20 günde önce +%8 %47,6 (oynaklık eşli rastgele %47,1; fark +0,5 puan, %95 [-13,7, +14,8]), önce -%8 %52,4 (rastgele %44,3); n 42 -> Ç124 kuralıyla TUTMAZ (bilgi).
- Eski Ç124 (görülmüş veri): ABD fark +11,2 puan (2016-22 +12,7 n 240; 2023 +3,1 n 26; 2024-26 +6,3 n 51), AVR +15,0.
- Hayatta kalma: görülmemiş hisseler bugün işlem gören nakit yakan şirketler; batanlar yok -> getiriler yukarı, -%50 olasılığı aşağı yanlı. Komisyon yok.

## Ç124 INTEM kuralı, görülmemiş ABD (L = 20, ana) — ORTAK CETVEL sonucu

Cetvel: ORTAK_CETVEL v1.0 (2026-11-14); CETVEL_SHA `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`; CETVEL_KOD_SHA `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`.

**GENEL ETİKET: ÖLÇÜLEMEDİ** · **OLASILIK ETİKETİ: ÖLÇÜLEMEDİ**

### Olay sayımı (düşmeler)

| Pazar | girdi | sembol yok | sinyal barı geçersiz | giriş yok | giriş geç | havuz dışı (likidite alt %20 / geçmiş bölünme / geçmiş eksik / evren öncesi / havuz < 30) | tekil | r60 ölçülemedi | eş < 3 |
|---|---|---|---|---|---|---|---|---|---|
| ABD | 740 | 0 | 0 | 0 | 0 | 540 (446 / 4 / 4 / 86 / 0) | 94 | 1 | 0 |

### Hücre tablosu (r60 eşli fark; FI dört şart + iki alt dönem)

| Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / plasebo p90 | yarı1 / yarı2 | güç (δ+%5) | durum |
|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | b | 37 | %4,2 [%-11,3, %19,4] | %-8,2 | 0,52 | %8 / %24 | %1,4 / %6,8 | %10 | ÖLÇÜLEMEDİ |
| ABD | 2023 | K | 26 | %-3,2 [%-19,8, %31,6] | %-8,1 | 0,46 | %15 / %55 | %-5,6 / %-0,7 | %0 | ÖLÇÜLEMEDİ |
| ABD | 2024-26 | K | 42 | %-7,5 [%-17,8, %2,9] | %-10,5 | 0,46 | %-20 / %71 | %-14,1 / %-0,9 | %10 | ÖLÇÜLEMEDİ |

### Olasılık tablosu (250 gün dokunma; eş katı karar, taban katı bilgi)

| Pazar | Dönem | n250 | P(+%100) olay / eş / taban | kat eş [%95] | kat taban | P(-%50) olay / eş / taban | kat eş [%95] | kat taban | 60g önce +%20 kat eş | 20g P(+%20 önce) / P(-%10 önce) olay (eş) | etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | 37 | %16,2 / %19,2 / %7,4 | 0,85 [0,00, 1,60] | 2,19 | %56,8 / %54,7 / %24,0 | 1,04 [0,79, 1,28] | 2,37 | 0,98 [0,44, 1,45] | %21,6 / %62,2 (%25,3 / %61,5) | YOK |
| ABD | 2023 | 26 | %38,5 / %37,4 / %19,2 | 1,03 [0,66, 1,69] | 2,00 | %30,8 / %30,3 / %13,0 | 1,02 [0,22, 1,36] | 2,36 | 0,82 [0,55, 1,77] | %26,9 / %65,4 (%24,9 / %55,1) | ÖLÇÜLEMEDİ |
| ABD | 2024-26 | 33 | %21,2 / %36,5 / %20,5 | 0,58 [0,29, 0,91] | 1,04 | %51,5 / %36,4 / %19,2 | 1,42 [1,04, 1,84] | 2,68 | 1,00 [0,58, 1,33] | %18,6 / %55,8 (%22,4 / %52,8) | YOK |

### Karar hücreleri

- ABD 2023: ÖLÇÜLEMEDİ
- ABD 2024-26: ÖLÇÜLEMEDİ
- AVR 2023: None
- AVR 2024-26: None

### Sınırlar (her raporda aynı)

- Hayatta kalma: evren bugün işlem gören hisseler (+ ABD k34 nakdi biten, yine bugün işlem gören); batanlar yok. Getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı.
- Komisyon / kayma yok; slot portföyü 10 yuva, 60 gün tut, sırayla.
- 31.08.2026 (fon krizi) sonrası fiyat yok; 250 gün dokunma ölçüsü en geç ~Ağustos 2025 girişlerini kapsar.
- Etiket kuralı OC_ESIK 'etiket' (İZ DEĞİL yalnız güç yeterliyken). Keşif 2016-22 ve BIST bilgi.

## Ç124'ün kendi ölçüsü (K45; bilgi, karar dışı; SAPMA-4 tam pencere)

| L | grup | n | +%8 önce olay / rastgele | fark [%95] | -%8 önce olay / rastgele | +%5 fark | +%12 fark | kutu yukarı olay / rast | yukarı çıkış sonra +%8 olay / rast (n) | koşullu fark [alt] | Ç124 kuralı |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 | 2016-26 (hepsi) | 105 | %47,6 / %44,9 | +2,7 [-6,8, +12,2] | %49,5 / %48,7 | +6,3 | +4,7 | %28,6 / %38,4 | %26,7 / %43,5 (30) | -16,9 [-33,5] | TUTMAZ |
| 20 | 2016-22 | 37 | %51,4 / %42,7 | +8,6 [-7,6, +22,2] | %40,5 / %51,4 | +18,9 | +2,4 | %27,0 / %32,4 | %40,0 / %42,5 (10) | -2,5 [-32,5] | TUTMAZ |
| 20 | 2023 | 26 | %42,3 / %41,5 | +0,8 [-18,5, +20,0] | %57,7 / %51,2 | -1,5 | +13,5 | %26,9 / %36,5 | %14,3 / %37,9 (7) | - [-] | n < 30 |
| 20 | 2024-26 | 42 | %47,6 / %47,1 | +0,5 [-13,7, +14,8] | %52,4 / %44,3 | -4,1 | +4,8 | %31,0 / %40,3 | %23,1 / %41,8 (13) | -18,7 [-41,8] | TUTMAZ |
| 10 | 2016-26 (hepsi) | 21 | %57,1 / %51,1 | +6,0 [-13,0, +25,0] | %33,3 / %44,4 | +3,5 | +0,8 | %42,9 / %38,2 | %33,3 / %46,8 (9) | - [-] | n < 30 |

## Eski sonuçlarla kıyas (IZ_KARNE metninden alıntı; yeniden ölçülmedi)

| Kayıt | Ne | Eski sonuç | metinde |
|---|---|---|---|
| Ç124 | 20 bar +%8 önce, ABD (oynaklık eşli rastgele) | ABD %54,9 / %43,2 (rastgele %43,7 / %43,2; fark +11,2 puan, aralık +6 .. +17) | EVET |
| Ç124 | 20 bar +%8 önce, AVR | AVR %50,4 / %41,9 (rastgele %35,5 / %35,9; +15,0, aralık +6 .. +24) | EVET |
| Ç124 | dönem sınaması ABD / AVR | fark ABD 2016-22 +12,7 (n 240), 2023 +3,1 (n 26), 2024-26 +6,3 (n 51); AVR 2016-22 +15,0 (n 92) | EVET |
| Ç124 | kutu yukarı kırılımında al kuralı | Kutu yukarı kırılımında al kuralı: ABD +10,9 (aralık 0'a değiyor), AVR +1,9 -> tutmadı | EVET |
| Ç123 | K44 60 gün eşli fark ABD 20 bar (2016-22 / 2023 / 2024-26) | ABD -%4 / -%9 / -%1 | EVET |

## Ç124 INTEM kuralı, görülmemiş ABD (L = 10, bilgi) — ORTAK CETVEL sonucu

Cetvel: ORTAK_CETVEL v1.0 (2026-11-14); CETVEL_SHA `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`; CETVEL_KOD_SHA `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`.

**GENEL ETİKET: ÖLÇÜLEMEDİ** · **OLASILIK ETİKETİ: ÖLÇÜLEMEDİ**

### Olay sayımı (düşmeler)

| Pazar | girdi | sembol yok | sinyal barı geçersiz | giriş yok | giriş geç | havuz dışı (likidite alt %20 / geçmiş bölünme / geçmiş eksik / evren öncesi / havuz < 30) | tekil | r60 ölçülemedi | eş < 3 |
|---|---|---|---|---|---|---|---|---|---|
| ABD | 53 | 0 | 0 | 0 | 0 | 31 (18 / 0 / 0 / 13 / 0) | 1 | 0 | 0 |

### Hücre tablosu (r60 eşli fark; FI dört şart + iki alt dönem)

| Pazar | Dönem | karar | n | ort fark [%95] | medyan | sıra | portföy / plasebo p90 | yarı1 / yarı2 | güç (δ+%5) | durum |
|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | b | 8 | %-8,2 [%-30,9, %0,6] | %-0,4 | 0,48 | %-14 / %6 | %-3,0 / %-13,3 | %0 | ÖLÇÜLEMEDİ |
| ABD | 2023 | K | 4 | %17,7 [%4,4, %37,8] | %23,1 | 0,72 | %13 / %17 | %29,7 / %5,8 | %0 | ÖLÇÜLEMEDİ |
| ABD | 2024-26 | K | 9 | %-15,6 [%-50,2, %13,1] | %-23,8 | 0,41 | %-7 / %26 | %-34,7 / %-0,4 | %0 | ÖLÇÜLEMEDİ |

### Olasılık tablosu (250 gün dokunma; eş katı karar, taban katı bilgi)

| Pazar | Dönem | n250 | P(+%100) olay / eş / taban | kat eş [%95] | kat taban | P(-%50) olay / eş / taban | kat eş [%95] | kat taban | 60g önce +%20 kat eş | 20g P(+%20 önce) / P(-%10 önce) olay (eş) | etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | 8 | %12,5 / %19,1 / %7,7 | 0,65 [0,00, 2,38] | 1,62 | %62,5 / %57,3 / %23,5 | 1,09 [0,36, 1,51] | 2,65 | 1,19 [0,87, 1,54] | %50,0 / %37,5 (%37,3 / %51,7) | ÖLÇÜLEMEDİ |
| ABD | 2023 | 4 | %75,0 / %37,8 / %19,6 | 1,98 [0,00, 2,59] | 3,83 | %0,0 / %30,2 / %12,8 | 0,00 [0,00, 0,00] | 0,00 | 2,23 [0,00, 3,32] | %25,0 / %0,0 (%22,3 / %55,1) | ÖLÇÜLEMEDİ |
| ABD | 2024-26 | 8 | %37,5 / %33,9 / %22,0 | 1,11 [0,35, 2,01] | 1,70 | %37,5 / %31,3 / %17,4 | 1,20 [0,00, 2,04] | 2,16 | 0,57 [0,00, 1,23] | %11,1 / %66,7 (%29,4 / %44,9) | ÖLÇÜLEMEDİ |

### Karar hücreleri

- ABD 2023: ÖLÇÜLEMEDİ
- ABD 2024-26: ÖLÇÜLEMEDİ
- AVR 2023: None
- AVR 2024-26: None

### Sınırlar (her raporda aynı)

- Hayatta kalma: evren bugün işlem gören hisseler (+ ABD k34 nakdi biten, yine bugün işlem gören); batanlar yok. Getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı.
- Komisyon / kayma yok; slot portföyü 10 yuva, 60 gün tut, sırayla.
- 31.08.2026 (fon krizi) sonrası fiyat yok; 250 gün dokunma ölçüsü en geç ~Ağustos 2025 girişlerini kapsar.
- Etiket kuralı OC_ESIK 'etiket' (İZ DEĞİL yalnız güç yeterliyken). Keşif 2016-22 ve BIST bilgi.

## Cetvel ve tarama

| L | Ç124 ABD eşleşme | yeniden üretilen | ortak |
|---|---|---|---|
| 20 | 317 | 317 | 317 |
| 10 | 39 | 39 | 39 |

Tarama: 1465 görülmemiş hisse; L20 1548097 pencere / 740 eşleşme; L10 1562370 / 53. Geleceğe bakma denetimi: 60 örnek, bozuk 0.

## Sınırlar

- Görülmemiş veri yalnız ABD k34 ekidir: nakit yakan küçük şirketler (Ç124'ün V_ABD evreninden farklı nüfus); Avrupa görülmüş olduğundan AVR karar hücreleri boş; kullanılmamış dönem yok. Gerçek ileri test (yeni zaman) Mart 2027+ verisi ister (IK_ILERI).
- Hayatta kalma: batanlar yok (Tiingo kullanılmadı); k34 hisseleri bugün işlem görenler.
- Mekanik: eşleşen bölgeler oynak (Ç124 dersi); OC eşleri 60 gün momentum x likiditeyle eşlenir, oynaklıkla eşlenmez; kendi ölçü oynaklık eşli tabanla.
- K45 rastgele havuzu V_ABD + k34 (Ç124'te V_ABD); 31.08.2026 kesiği nedeniyle tam pencere süzgeci (SAPMA-4).
- L = 10, dönem kırılımları ve kendi ölçü bilgi; çoklu karşılaştırma düzeltmesi yapılmadı, iddia üretmez.
