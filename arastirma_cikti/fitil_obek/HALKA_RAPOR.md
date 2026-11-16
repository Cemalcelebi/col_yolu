# FITIL_KOR — HALKA RAPORU (fitil öbeği: hata nerede?)

Ön kayıt yazım 2026-11-16 21:05:30 UTC (sha `7349e099d6af3b5a5b1f211dace19a6292bed56f99b7251103129efe63e93200`; git: İŞLENMEDİ (gitsiz koşu; ön kayıt sha 7349e099d6af…, yazım 2026-11-16 21:05:30 UTC)); iş tanımı git cbf1cc5cd9 (2026-11-16T20:28:12+00:00); koşu 2026-11-16 21:05:35 UTC; süre 945.5 sn. Geleceğe bakma denetimi: ABD 40 olay TUTTU, AVR 40 olay TUTTU, BIST 40 olay TUTTU.

## ÖZET (bulgu dili; hangi halkada ne çıktı)

- HALKA 1 (tanım bağlamı) — KIRIK, ama beklenen yönde değil: önceden yazılı 'taban içi' tanımı (S6 açık bölge, sınıf DİP, as-of t) Cemal'in üç S+ örneğinin ÜÇÜNÜ de dışarıda bırakıyor. PAPIL: S+ 14-26 Kas'ta yanıyor, S6 bölgesi ancak 3 Ara'da onaylanıyor (kutu geriye 11 Kas'a uzuyor ama o gün bilinmiyordu). TEHOL Mayıs 2025: S6 bölgesi AÇIK (5-29 May) ama sınıfı ORTA (10 kat yükselişten sonra geri çekilme; DİP değil). BINBN: hisse S6 için ölçülür değil (250 geçerli bar yok). Yani Cemal'in deseni 'dipteki taban' değil; çoğunlukla yükseliş / geri çekilme sonrası sıkışma.
- HALKA 1 ölçümü: taban içi S+ eşlerden ayrışmıyor (karar hücreleri n 60 / 110 / 76 / 175; eşli fark -1,6% / +0,8% / +0,6% / -1,1%, hepsinin aralığı 0'ı kapsıyor; etiket ÖLÇÜLEMEDİ, güç yetersiz). Taban içi S+ olmayan günlerden de ayrışmıyor (fark -1,0% / +1,7% / +1,1% / -0,4%; TÜM 2023-26 -0,1% [-2,2%, +2,7%]). Varyantlar (gevşek, sıkı, küçük mum) aynı: AYRIŞMAZ / ÖLÇÜLEMEDİ.
- HALKA 3 (doğrulama ölçüsü) — ölçü değişince sonuç Cemal'in yönüne dönmüyor: r20 eşli fark taban içi S+ vs kontrol TÜM 2023-26 +0,0% [-0,6%, +0,8%]. Kırılımda S+ sonrası 'önce tavan' oranı kontrolden DÜŞÜK: karar hücrelerinde -12,7 / -1,3 / -6,9 / -6,9 puan (tek tek anlamsız), TÜM 2023-26 -6,6 puan [-14,6; +1,8]; ters yön: 'önce dip' oranı +6,0 puan. S- aynası da ters: S- sonrası 'önce dip' oranı kontrolden -7,1 puan düşük. Yani fitil asimetrisi kırılım ölçüsünde Cemal'in beklediğinin tersine hafif bir eğilim gösteriyor (anlamlı değil).
- EK S+DÜZ (düz dip): dip bağlamıyla n çok küçük (karar hücreleri 11 / 24 / 29 / 77; ÖLÇÜLEMEDİ). Bağlamsız varyant SPDb ABD 2024-26'da TUTAR (n 80, +6,7% [+1,6%, +12,3%], sıra 0,61) -> etiket EMARE (tek hücre); ama ABD 2023 / AVR iki dönem tutmuyor, BIST 2024-26 -1,2%, ve aynı olaylarda 10 mum kutusu kırılımı TERS (önce yukarı oranı kontrolden -15,6 puan [-26,5; -4,4]; TÜM -9,1 puan [-14,4; -3,6]). SPDb kalibrasyon sonrası eklenmiş bir bilgi varyantıdır, çok sayıda varyant içinde tek hücre: bulgu değil, ileri test adayı.
- Cemal örnekleri (n 3; bilgi): kodun S+'ı üç örnekte de yanıyor (PAPIL 10 gün, TEHOL Mayıs 17 / 18 gün, BINBN 16 / 25 gün) -> ALGILAMA bu üç örnekte çalışıyor. Sonrası güçlü: pencere sonu girişle r60 eşli fark PAPIL +19,1%, TEHOL +44,8%, BINBN +162,7% (üç tek olay; seçilmiş örnek, bulgu değil). DGXX'te S- hiç yanmıyor (ASIM -0,25'e iniyor ama üst fitilsiz bar payı yetmiyor).
- TANI (önceden yazılı okuma): (1) HALKA 1 ölçümünde taban içi S+ TUTMADI / AYRIŞMADI -> 'hata bağlamda' kanıtı yok; ama tanımın bağlamı Cemal'in örneklerini kapsamıyor, yani bu ölçüm Cemal'in desenini sınamadı. (2) HALKA 3: r20 ve kırılım da ayrışmıyor -> 'hata ölçüde' kanıtı yok. (3) Kalan: HALKA 2 kör seti (Cemal'in gözü) ve bağlamın yeniden tanımı (dip değil, yükseliş sonrası sıkışma / geri çekilme; S6 sınıf ORTA / YOL dahil, onay gecikmesiz). Bu ikinci nokta yeni ön kayıt ister.

## HALKA 1 — TANIM BAĞLAMI (S+ yalnız S6 TABAN İÇİNDE)

(a) r60 eşli fark (ORTAK_CETVEL; hücre: n, ortalama eşli fark [%95], sıra, durum beklenen yönde). Etiket Ç187 kuralı.

| Satır | etiket | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|
| SP_ic | ÖLÇÜLEMEDİ | n 60, -1,6% [-5,2%, +3,8%], sıra 0,49, ÖLÇÜLEMEDİ | n 110, +0,8% [-3,8%, +7,6%], sıra 0,52, ÖLÇÜLEMEDİ | n 76, +0,6% [-2,0%, +3,0%], sıra 0,51, ÖLÇÜLEMEDİ | n 175, -1,1% [-2,2%, +0,2%], sıra 0,48, ÖLÇÜLEMEDİ | n 64, -3,6% [-8,4%, +14,9%], sıra 0,45, ÖLÇÜLEMEDİ | n 399, +0,4% [-3,6%, +6,3%], sıra 0,49, ÖLÇÜLEMEDİ |
| SM_ic | ÖLÇÜLEMEDİ | n 57, -2,7% [-7,9%, +3,6%], sıra 0,46, ÖLÇÜLEMEDİ | n 85, +1,4% [-3,6%, +6,7%], sıra 0,53, ÖLÇÜLEMEDİ | n 33, -2,6% [-8,2%, +2,2%], sıra 0,46, ÖLÇÜLEMEDİ | n 88, +0,3% [-1,5%, +2,0%], sıra 0,50, ÖLÇÜLEMEDİ | n 2, -4,9% [-33,5%, +23,7%], sıra 0,51, ÖLÇÜLEMEDİ | n 34, -0,8% [-7,4%, +5,1%], sıra 0,51, ÖLÇÜLEMEDİ |
| SP_dis | ÖLÇÜLEMEDİ | n 861, +0,3% [-1,1%, +1,4%], sıra 0,50, ÖLÇÜLEMEDİ | n 2117, +0,3% [-1,2%, +1,7%], sıra 0,50, TUTMADI | n 617, -0,3% [-1,3%, +0,6%], sıra 0,49, ÖLÇÜLEMEDİ | n 1685, -0,3% [-1,1%, +0,5%], sıra 0,49, TUTMADI | n 669, -0,0% [-2,7%, +2,8%], sıra 0,49, ÖLÇÜLEMEDİ | n 2369, -0,5% [-2,0%, +1,1%], sıra 0,49, TUTMADI |
| SM_dis | ÖLÇÜLEMEDİ | n 893, +0,2% [-0,9%, +1,1%], sıra 0,50, ÖLÇÜLEMEDİ | n 2305, -0,5% [-1,9%, +0,9%], sıra 0,50, TUTMADI | n 582, +0,3% [-0,8%, +1,6%], sıra 0,50, ÖLÇÜLEMEDİ | n 1533, -0,2% [-0,8%, +0,5%], sıra 0,49, TUTMADI | n 276, -2,4% [-8,4%, +3,0%], sıra 0,48, ÖLÇÜLEMEDİ | n 498, +1,3% [-2,6%, +5,8%], sıra 0,49, ÖLÇÜLEMEDİ |
| SP_tum | ÖLÇÜLEMEDİ | n 880, +0,2% [-1,1%, +1,4%], sıra 0,50, ÖLÇÜLEMEDİ | n 2160, +0,3% [-1,1%, +1,7%], sıra 0,50, TUTMADI | n 646, +0,0% [-0,8%, +0,8%], sıra 0,51, ÖLÇÜLEMEDİ | n 1730, -0,3% [-1,1%, +0,5%], sıra 0,49, TUTMADI | n 674, -0,3% [-2,5%, +2,0%], sıra 0,49, ÖLÇÜLEMEDİ | n 2428, -0,6% [-2,1%, +0,9%], sıra 0,49, TUTMADI |
| SM_tum | ÖLÇÜLEMEDİ | n 922, -0,0% [-1,0%, +0,9%], sıra 0,50, ÖLÇÜLEMEDİ | n 2350, -0,4% [-1,8%, +0,9%], sıra 0,50, TUTMADI | n 590, +0,3% [-0,9%, +1,7%], sıra 0,50, ÖLÇÜLEMEDİ | n 1555, -0,2% [-0,9%, +0,4%], sıra 0,49, TUTMADI | n 277, -2,5% [-8,6%, +3,0%], sıra 0,48, ÖLÇÜLEMEDİ | n 510, +1,5% [-2,4%, +5,7%], sıra 0,49, ÖLÇÜLEMEDİ |
| K_SP | ÖLÇÜLEMEDİ | n 908, -0,6% [-2,2%, +0,8%], sıra 0,50, ÖLÇÜLEMEDİ | n 1771, -1,0% [-2,1%, +0,1%], sıra 0,50, TUTMADI | n 389, -0,5% [-1,3%, +0,3%], sıra 0,49, ÖLÇÜLEMEDİ | n 793, -0,6% [-1,6%, +0,4%], sıra 0,49, ÖLÇÜLEMEDİ | n 237, +2,5% [-4,6%, +9,4%], sıra 0,50, ÖLÇÜLEMEDİ | n 1226, +1,2% [-0,5%, +3,1%], sıra 0,51, TUTMADI |
| K_SM | ÖLÇÜLEMEDİ | n 911, -0,6% [-2,3%, +0,8%], sıra 0,50, ÖLÇÜLEMEDİ | n 1773, -0,9% [-2,1%, +0,2%], sıra 0,50, TUTMADI | n 391, -0,7% [-1,5%, +0,2%], sıra 0,49, ÖLÇÜLEMEDİ | n 801, -0,7% [-1,7%, +0,3%], sıra 0,49, ÖLÇÜLEMEDİ | n 242, +2,0% [-5,8%, +8,1%], sıra 0,50, ÖLÇÜLEMEDİ | n 1250, +1,4% [-0,3%, +3,4%], sıra 0,51, TUTMADI |
| K_SP_r | ÖLÇÜLEMEDİ | n 851, -0,7% [-1,7%, +0,3%], sıra 0,50, ÖLÇÜLEMEDİ | n 1662, -0,7% [-2,0%, +0,4%], sıra 0,50, TUTMADI | n 344, -0,5% [-1,5%, +0,8%], sıra 0,49, ÖLÇÜLEMEDİ | n 709, -0,9% [-1,8%, -0,1%], sıra 0,49, ÖLÇÜLEMEDİ | n 234, +2,1% [-5,5%, +10,3%], sıra 0,50, ÖLÇÜLEMEDİ | n 1096, +1,7% [-0,3%, +3,9%], sıra 0,52, TUTMADI |
| K_SM_r | ÖLÇÜLEMEDİ | n 852, -0,7% [-1,6%, +0,3%], sıra 0,50, ÖLÇÜLEMEDİ | n 1662, -0,5% [-1,8%, +0,7%], sıra 0,50, TUTMADI | n 338, -1,0% [-2,0%, +0,3%], sıra 0,48, ÖLÇÜLEMEDİ | n 719, -0,8% [-1,7%, +0,1%], sıra 0,49, ÖLÇÜLEMEDİ | n 236, +1,6% [-4,4%, +6,4%], sıra 0,50, ÖLÇÜLEMEDİ | n 1113, +1,5% [-0,6%, +3,8%], sıra 0,51, TUTMADI |
| SPg_ic | ÖLÇÜLEMEDİ | n 245, +0,2% [-2,1%, +2,9%], sıra 0,51, ÖLÇÜLEMEDİ | n 481, -0,8% [-2,9%, +1,1%], sıra 0,50, ÖLÇÜLEMEDİ | n 194, -0,8% [-1,8%, +0,3%], sıra 0,48, ÖLÇÜLEMEDİ | n 409, -0,6% [-1,9%, +0,9%], sıra 0,50, ÖLÇÜLEMEDİ | n 132, -1,9% [-7,5%, +2,3%], sıra 0,47, ÖLÇÜLEMEDİ | n 773, +0,9% [-1,8%, +4,0%], sıra 0,52, ÖLÇÜLEMEDİ |
| SPs_ic | ÖLÇÜLEMEDİ | n 7, +13,9% [-2,6%, +37,3%], sıra 0,64, ÖLÇÜLEMEDİ | n 19, -6,7% [-13,5%, +2,2%], sıra 0,42, ÖLÇÜLEMEDİ | n 23, +1,7% [-3,7%, +4,6%], sıra 0,53, ÖLÇÜLEMEDİ | n 40, +2,2% [-0,5%, +4,9%], sıra 0,59, ÖLÇÜLEMEDİ | n 17, +2,6% [-7,0%, +91,3%], sıra 0,47, ÖLÇÜLEMEDİ | n 110, +9,5% [-3,4%, +32,1%], sıra 0,50, ÖLÇÜLEMEDİ |
| SPk_ic | ÖLÇÜLEMEDİ | n 44, -0,1% [-3,8%, +6,8%], sıra 0,51, ÖLÇÜLEMEDİ | n 57, -0,9% [-6,2%, +7,4%], sıra 0,51, ÖLÇÜLEMEDİ | n 48, +0,3% [-3,8%, +3,5%], sıra 0,51, ÖLÇÜLEMEDİ | n 83, -3,6% [-6,4%, -0,9%], sıra 0,44, ÖLÇÜLEMEDİ | n 57, -5,1% [-8,9%, +1,3%], sıra 0,46, ÖLÇÜLEMEDİ | n 349, +0,7% [-3,5%, +6,1%], sıra 0,49, ÖLÇÜLEMEDİ |
| SPD | ÖLÇÜLEMEDİ | n 11, -0,9% [-11,6%, +8,7%], sıra 0,44, ÖLÇÜLEMEDİ | n 24, +9,4% [+1,7%, +17,9%], sıra 0,64, ÖLÇÜLEMEDİ | n 29, -3,2% [-5,3%, -1,0%], sıra 0,44, ÖLÇÜLEMEDİ | n 77, -0,3% [-3,3%, +3,4%], sıra 0,47, ÖLÇÜLEMEDİ | n 18, -3,5% [-14,1%, +10,3%], sıra 0,50, ÖLÇÜLEMEDİ | n 161, -2,2% [-6,4%, +1,9%], sıra 0,47, ÖLÇÜLEMEDİ |
| SPD07 | ÖLÇÜLEMEDİ | n 1, -8,4% [-8,4%, -8,4%], sıra 0,26, ÖLÇÜLEMEDİ | n 3, +6,4% [+6,4%, +6,4%], sıra 0,60, ÖLÇÜLEMEDİ | n 8, -2,2% [-7,9%, +0,6%], sıra 0,45, ÖLÇÜLEMEDİ | n 18, +1,6% [-3,1%, +5,8%], sıra 0,54, ÖLÇÜLEMEDİ | n 0 | n 33, -3,6% [-10,9%, +5,0%], sıra 0,48, ÖLÇÜLEMEDİ |
| SPD15 | ÖLÇÜLEMEDİ | n 62, -3,3% [-8,7%, +1,6%], sıra 0,45, ÖLÇÜLEMEDİ | n 153, -1,8% [-6,2%, +2,6%], sıra 0,48, ÖLÇÜLEMEDİ | n 97, +1,5% [-0,7%, +3,2%], sıra 0,54, ÖLÇÜLEMEDİ | n 234, -0,3% [-2,1%, +1,7%], sıra 0,49, ÖLÇÜLEMEDİ | n 89, -6,4% [-13,2%, -2,0%], sıra 0,45, ÖLÇÜLEMEDİ | n 454, +0,3% [-2,9%, +5,5%], sıra 0,48, ÖLÇÜLEMEDİ |
| K_DUZ | ÖLÇÜLEMEDİ | n 450, -0,5% [-2,4%, +1,7%], sıra 0,50, ÖLÇÜLEMEDİ | n 1066, +1,1% [-0,8%, +3,0%], sıra 0,51, TUTMADI | n 225, -1,3% [-2,7%, +0,2%], sıra 0,47, ÖLÇÜLEMEDİ | n 509, -0,8% [-2,1%, +0,7%], sıra 0,48, ÖLÇÜLEMEDİ | n 143, -3,4% [-7,5%, +1,0%], sıra 0,48, ÖLÇÜLEMEDİ | n 615, +0,8% [-2,0%, +4,3%], sıra 0,51, ÖLÇÜLEMEDİ |
| SPDb | EMARE (ABD 2024-26) | n 36, +3,9% [-1,9%, +14,2%], sıra 0,53, ÖLÇÜLEMEDİ | n 80, +6,7% [+1,6%, +12,3%], sıra 0,61, TUTAR | n 77, -1,3% [-3,2%, +0,2%], sıra 0,49, ÖLÇÜLEMEDİ | n 253, +0,4% [-1,1%, +2,0%], sıra 0,50, ÖLÇÜLEMEDİ | n 80, -2,1% [-12,4%, +6,7%], sıra 0,50, ÖLÇÜLEMEDİ | n 405, -1,2% [-5,4%, +3,0%], sıra 0,49, ÖLÇÜLEMEDİ |
| K_DUZb | ÖLÇÜLEMEDİ | n 1372, +1,0% [-0,3%, +2,7%], sıra 0,51, TUTMADI | n 3531, +0,8% [-0,3%, +1,8%], sıra 0,50, TUTMADI | n 675, +0,3% [-0,8%, +1,3%], sıra 0,50, ÖLÇÜLEMEDİ | n 1771, +0,3% [-0,4%, +0,9%], sıra 0,51, TUTMADI | n 534, -1,6% [-4,4%, +0,9%], sıra 0,50, ÖLÇÜLEMEDİ | n 1805, +1,8% [+0,0%, +3,9%], sıra 0,52, TUTMADI |

(b) taban içi S+ vs taban içi S+ OLMAYAN günler (eşli farkların farkı; iki grup ayrı ay kümeli bootstrap %95). S- ayna.

| Karşılaştırma | genel | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 | TÜM 2023-26 |
|---|---|---|---|---|---|---|---|---|
| SP_ic-K_SP | AYRIŞMAZ | -1,0% [-5,0%, +4,3%] (60/908) AYRIŞMAZ | +1,7% [-2,9%, +8,8%] (110/1771) AYRIŞMAZ | +1,1% [-1,7%, +3,8%] (76/389) AYRIŞMAZ | -0,4% [-2,0%, +1,2%] (175/793) AYRIŞMAZ | -6,1% [-14,8%, +15,6%] (64/237) AYRIŞMAZ | -0,8% [-5,4%, +5,6%] (399/1226) AYRIŞMAZ | -0,1% [-2,2%, +2,7%] (884/5324) AYRIŞMAZ |
| SP_ic-K_SP_r | AYRIŞMAZ | -0,9% [-4,9%, +4,3%] (60/851) AYRIŞMAZ | +1,5% [-3,2%, +8,5%] (110/1662) AYRIŞMAZ | +1,1% [-1,9%, +3,8%] (76/344) AYRIŞMAZ | -0,1% [-1,6%, +1,4%] (175/709) AYRIŞMAZ | -5,7% [-14,9%, +16,2%] (64/234) AYRIŞMAZ | -1,3% [-5,9%, +4,7%] (399/1096) AYRIŞMAZ | -0,2% [-2,2%, +2,7%] (884/4896) AYRIŞMAZ |
| SM_ic-K_SM | AYRIŞMAZ | -2,0% [-7,3%, +4,5%] (57/911) AYRIŞMAZ | +2,3% [-2,8%, +7,2%] (85/1773) AYRIŞMAZ | -1,9% [-7,8%, +2,9%] (33/391) AYRIŞMAZ | +1,0% [-0,9%, +3,1%] (88/801) AYRIŞMAZ | -6,9% [-39,0%, +25,8%] (2/242) ÖLÇÜLEMEDİ | -2,2% [-9,0%, +4,2%] (34/1250) AYRIŞMAZ | -0,3% [-2,6%, +2,0%] (299/5368) AYRIŞMAZ |
| SM_ic-K_SM_r | AYRIŞMAZ | -1,9% [-7,3%, +4,3%] (57/852) AYRIŞMAZ | +1,9% [-3,3%, +6,6%] (85/1662) AYRIŞMAZ | -1,6% [-7,2%, +3,4%] (33/338) AYRIŞMAZ | +1,0% [-1,0%, +3,0%] (88/719) AYRIŞMAZ | -6,5% [-37,8%, +25,6%] (2/236) ÖLÇÜLEMEDİ | -2,3% [-9,1%, +4,1%] (34/1113) AYRIŞMAZ | -0,4% [-2,7%, +2,0%] (299/4920) AYRIŞMAZ |
| SPg_ic-K_SP | AYRIŞMAZ | +0,8% [-2,0%, +4,0%] (245/908) AYRIŞMAZ | +0,2% [-2,2%, +2,4%] (481/1771) AYRIŞMAZ | -0,3% [-1,6%, +1,0%] (194/389) AYRIŞMAZ | +0,0% [-1,7%, +1,9%] (409/793) AYRIŞMAZ | -4,4% [-13,0%, +4,0%] (132/237) AYRIŞMAZ | -0,3% [-3,7%, +3,2%] (773/1226) AYRIŞMAZ | +0,0% [-1,2%, +1,3%] (2234/5324) AYRIŞMAZ |
| SPs_ic-K_SP | AYRIŞMAZ | +14,5% [-2,1%, +42,8%] (7/908) ÖLÇÜLEMEDİ | -5,8% [-12,9%, +3,6%] (19/1771) ÖLÇÜLEMEDİ | +2,2% [-3,2%, +5,2%] (23/389) ÖLÇÜLEMEDİ | +2,8% [-0,1%, +5,7%] (40/793) AYRIŞMAZ | +0,1% [-12,7%, +81,7%] (17/237) ÖLÇÜLEMEDİ | +8,3% [-5,3%, +30,8%] (110/1226) AYRIŞMAZ | +5,6% [-1,2%, +16,5%] (216/5324) AYRIŞMAZ |
| SPk_ic-K_SP | AYRIŞMAZ | +0,5% [-3,6%, +8,1%] (44/908) AYRIŞMAZ | +0,1% [-5,2%, +8,7%] (57/1771) AYRIŞMAZ | +0,8% [-3,6%, +3,9%] (48/389) AYRIŞMAZ | -2,9% [-6,1%, -0,1%] (83/793) AYRIŞMAZ | -7,6% [-15,4%, +1,6%] (57/237) AYRIŞMAZ | -0,6% [-5,2%, +5,1%] (349/1226) AYRIŞMAZ | -0,5% [-2,9%, +2,9%] (638/5324) AYRIŞMAZ |
| SPD-K_SP | AYRIŞMAZ | -0,3% [-10,9%, +10,7%] (11/908) ÖLÇÜLEMEDİ | +10,4% [+2,9%, +19,0%] (24/1771) ÖLÇÜLEMEDİ | -2,7% [-5,0%, -0,4%] (29/389) ÖLÇÜLEMEDİ | +0,3% [-3,0%, +4,2%] (77/793) AYRIŞMAZ | -6,0% [-18,7%, +9,8%] (18/237) ÖLÇÜLEMEDİ | -3,4% [-8,1%, +1,0%] (161/1226) AYRIŞMAZ | -0,8% [-3,5%, +1,9%] (320/5324) AYRIŞMAZ |
| SPD-K_DUZ | AYRIŞMAZ | -0,4% [-11,2%, +10,7%] (11/450) ÖLÇÜLEMEDİ | +8,3% [+0,5%, +17,1%] (24/1066) ÖLÇÜLEMEDİ | -1,8% [-4,6%, +0,8%] (29/225) ÖLÇÜLEMEDİ | +0,4% [-3,0%, +4,4%] (77/509) AYRIŞMAZ | -0,2% [-11,3%, +14,7%] (18/143) ÖLÇÜLEMEDİ | -3,0% [-8,8%, +2,0%] (161/615) AYRIŞMAZ | -1,1% [-3,9%, +1,6%] (320/3008) AYRIŞMAZ |
| SPD07-K_DUZ | ÖLÇÜLEMEDİ | -7,9% [-10,1%, -6,0%] (1/450) ÖLÇÜLEMEDİ | +5,2% [+3,4%, +7,1%] (3/1066) ÖLÇÜLEMEDİ | -0,9% [-6,5%, +2,4%] (8/225) ÖLÇÜLEMEDİ | +2,4% [-2,6%, +6,7%] (18/509) ÖLÇÜLEMEDİ | - [-, -] (0/143) ÖLÇÜLEMEDİ | -4,5% [-12,9%, +4,5%] (33/615) AYRIŞMAZ | -1,7% [-5,7%, +2,8%] (63/3008) AYRIŞMAZ |
| SPD15-K_DUZ | KISMİ (AVR 2023) | -2,8% [-8,8%, +2,5%] (62/450) AYRIŞMAZ | -3,0% [-7,8%, +1,8%] (153/1066) AYRIŞMAZ | +2,8% [+0,1%, +5,0%] (97/225) AYRIŞIR | +0,5% [-1,9%, +2,9%] (234/509) AYRIŞMAZ | -3,1% [-10,8%, +3,1%] (89/143) AYRIŞMAZ | -0,5% [-5,5%, +5,1%] (454/615) AYRIŞMAZ | -0,9% [-2,6%, +1,2%] (1089/3008) AYRIŞMAZ |
| SPDb-K_DUZb | KISMİ (ABD 2024-26) | +2,9% [-3,2%, +13,5%] (36/1372) AYRIŞMAZ | +5,9% [+1,0%, +11,5%] (80/3531) AYRIŞIR | -1,6% [-3,8%, +0,2%] (77/675) AYRIŞMAZ | +0,1% [-1,5%, +1,8%] (253/1771) AYRIŞMAZ | -0,5% [-10,9%, +8,8%] (80/534) AYRIŞMAZ | -3,0% [-7,7%, +1,6%] (405/1805) AYRIŞMAZ | -0,7% [-2,7%, +1,4%] (931/9688) AYRIŞMAZ |

## HALKA 3 — DOĞRULAMA ÖLÇÜSÜ (r20 ve 'önce tavan mı, dip mi')

r20 eşli fark (cetvel mekaniği, ufuk 20; 'tutar' bilgi):

| Satır | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|
| SP_ic | n 60, +0,6% [-1,2%, +2,4%], sıra 0,52, - | n 118, +0,1% [-2,3%, +3,5%], sıra 0,51, - | n 76, +0,6% [-0,9%, +1,9%], sıra 0,53, - | n 182, -0,3% [-1,2%, +0,7%], sıra 0,50, - | n 64, +0,2% [-1,6%, +2,4%], sıra 0,51, - | n 452, -0,8% [-1,9%, +0,2%], sıra 0,48, - |
| SP_tum | n 880, +0,5% [-0,1%, +1,0%], sıra 0,51, - | n 2431, +0,1% [-0,5%, +0,7%], sıra 0,49, - | n 646, -0,1% [-0,4%, +0,3%], sıra 0,50, - | n 1798, -0,2% [-0,5%, +0,1%], sıra 0,50, - | n 674, +0,1% [-0,6%, +0,9%], sıra 0,50, - | n 2619, +0,3% [-0,3%, +1,0%], sıra 0,50, - |
| K_SP | n 908, -0,7% [-1,6%, +0,2%], sıra 0,49, - | n 1864, -0,8% [-1,4%, -0,1%], sıra 0,49, - | n 389, +0,1% [-0,6%, +0,7%], sıra 0,50, - | n 851, -0,3% [-0,9%, +0,3%], sıra 0,48, - | n 237, +0,6% [-2,7%, +2,2%], sıra 0,51, - | n 1338, +0,1% [-0,6%, +0,7%], sıra 0,50, - |
| SM_ic | n 57, -0,2% [-4,1%, +3,6%], sıra 0,50, - | n 87, -0,5% [-2,9%, +1,8%], sıra 0,48, - | n 33, +0,0% [-3,0%, +3,0%], sıra 0,50, - | n 91, +0,6% [-1,1%, +2,3%], sıra 0,52, - | n 2, +4,6% [-11,9%, +21,2%], sıra 0,55, - | n 35, -2,4% [-6,3%, -0,0%], sıra 0,44, - |
| SM_tum | n 922, +0,2% [-0,5%, +0,8%], sıra 0,51, - | n 2405, +0,3% [-0,3%, +0,8%], sıra 0,51, - | n 590, +0,1% [-0,6%, +0,9%], sıra 0,51, - | n 1713, +0,0% [-0,3%, +0,4%], sıra 0,50, - | n 277, -0,6% [-3,0%, +2,6%], sıra 0,47, - | n 538, +0,4% [-0,8%, +1,6%], sıra 0,49, - |
| K_SM | n 911, -0,7% [-1,6%, +0,2%], sıra 0,49, - | n 1866, -0,8% [-1,5%, -0,1%], sıra 0,49, - | n 391, +0,2% [-0,6%, +0,8%], sıra 0,50, - | n 859, -0,3% [-0,8%, +0,3%], sıra 0,48, - | n 242, +0,8% [-3,0%, +2,4%], sıra 0,51, - | n 1367, +0,1% [-0,5%, +0,8%], sıra 0,51, - |
| SPD | n 11, +0,5% [-3,4%, +2,6%], sıra 0,50, - | n 28, +0,4% [-3,9%, +6,1%], sıra 0,50, - | n 29, -1,2% [-3,8%, +1,2%], sıra 0,49, - | n 80, +1,3% [-0,8%, +3,9%], sıra 0,51, - | n 18, +3,0% [-4,0%, +12,9%], sıra 0,53, - | n 193, -1,4% [-3,5%, +0,7%], sıra 0,45, - |
| K_DUZ | n 450, -0,1% [-1,1%, +1,1%], sıra 0,50, - | n 1131, +0,1% [-0,8%, +0,9%], sıra 0,50, - | n 225, +0,6% [-0,4%, +1,9%], sıra 0,51, - | n 541, +0,5% [-0,5%, +1,7%], sıra 0,51, - | n 143, -2,8% [-4,2%, -1,3%], sıra 0,44, - | n 699, +0,4% [-0,5%, +1,4%], sıra 0,50, - |

r20 fark (b):

| Karşılaştırma | genel | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 | TÜM 2023-26 |
|---|---|---|---|---|---|---|---|---|
| SP_ic-K_SP | AYRIŞMAZ | +1,3% [-0,9%, +3,2%] (60/908) AYRIŞMAZ | +0,9% [-1,7%, +4,4%] (118/1864) AYRIŞMAZ | +0,5% [-1,1%, +2,1%] (76/389) AYRIŞMAZ | +0,0% [-1,1%, +1,1%] (182/851) AYRIŞMAZ | -0,5% [-3,0%, +3,1%] (64/237) AYRIŞMAZ | -0,9% [-2,2%, +0,5%] (452/1338) AYRIŞMAZ | +0,0% [-0,6%, +0,8%] (952/5587) AYRIŞMAZ |
| SM_ic-K_SM | AYRIŞMAZ | +0,5% [-3,4%, +4,6%] (57/911) AYRIŞMAZ | +0,3% [-2,1%, +2,8%] (87/1866) AYRIŞMAZ | -0,1% [-3,3%, +3,1%] (33/391) AYRIŞMAZ | +0,9% [-0,9%, +2,7%] (91/859) AYRIŞMAZ | +3,9% [-13,8%, +22,4%] (2/242) ÖLÇÜLEMEDİ | -2,5% [-6,3%, -0,1%] (35/1367) AYRIŞIR | +0,1% [-1,1%, +1,3%] (305/5636) AYRIŞMAZ |
| SPD-K_DUZ | AYRIŞMAZ | +0,6% [-3,3%, +2,8%] (11/450) ÖLÇÜLEMEDİ | +0,4% [-4,0%, +6,2%] (28/1131) ÖLÇÜLEMEDİ | -1,8% [-4,7%, +0,8%] (29/225) ÖLÇÜLEMEDİ | +0,8% [-1,6%, +3,4%] (80/541) AYRIŞMAZ | +5,8% [-1,4%, +16,5%] (18/143) ÖLÇÜLEMEDİ | -1,9% [-4,1%, +0,6%] (193/699) AYRIŞMAZ | -0,5% [-1,9%, +1,1%] (359/3189) AYRIŞMAZ |

Kırılım: 60 geçerli bar içinde önce S6 tavanı (kapanış) = YUKARI / önce dip x 0,98 altı (kapanış) = AŞAĞI. Oranlar (n ölçülen olay):

| Satır | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|
| SP_ic | n 60: Y +45% / A +55% / yok +0% | n 110: Y +52% / A +45% / yok +3% | n 76: Y +45% / A +50% / yok +5% | n 174: Y +45% / A +52% / yok +3% | n 64: Y +34% / A +66% / yok +0% | n 399: Y +52% / A +48% / yok +0% |
| K_SP | n 908: Y +58% / A +42% / yok +0% | n 1771: Y +53% / A +46% / yok +0% | n 389: Y +52% / A +45% / yok +3% | n 792: Y +52% / A +46% / yok +2% | n 237: Y +47% / A +53% / yok +0% | n 1225: Y +59% / A +40% / yok +0% |
| K_SP_r | n 851: Y +60% / A +40% / yok +0% | n 1662: Y +53% / A +47% / yok +0% | n 344: Y +53% / A +45% / yok +2% | n 708: Y +52% / A +47% / yok +2% | n 234: Y +46% / A +54% / yok +0% | n 1095: Y +61% / A +38% / yok +0% |
| SM_ic | n 57: Y +60% / A +40% / yok +0% | n 85: Y +60% / A +39% / yok +1% | n 33: Y +61% / A +36% / yok +3% | n 88: Y +55% / A +36% / yok +9% | n 2: Y +50% / A +50% / yok +0% | n 34: Y +68% / A +32% / yok +0% |
| K_SM | n 911: Y +58% / A +42% / yok +0% | n 1773: Y +53% / A +46% / yok +0% | n 391: Y +52% / A +45% / yok +3% | n 799: Y +51% / A +47% / yok +2% | n 242: Y +46% / A +54% / yok +0% | n 1249: Y +59% / A +40% / yok +0% |
| K_SM_r | n 852: Y +60% / A +40% / yok +0% | n 1662: Y +53% / A +47% / yok +0% | n 338: Y +50% / A +48% / yok +2% | n 718: Y +51% / A +47% / yok +2% | n 236: Y +46% / A +54% / yok +0% | n 1112: Y +60% / A +39% / yok +0% |
| SPg_ic | n 245: Y +50% / A +50% / yok +0% | n 481: Y +52% / A +46% / yok +2% | n 194: Y +46% / A +51% / yok +4% | n 407: Y +48% / A +50% / yok +2% | n 132: Y +43% / A +57% / yok +0% | n 773: Y +56% / A +43% / yok +0% |
| SPs_ic | n 7: Y +57% / A +43% / yok +0% | n 19: Y +37% / A +63% / yok +0% | n 23: Y +57% / A +30% / yok +13% | n 40: Y +52% / A +45% / yok +2% | n 17: Y +24% / A +76% / yok +0% | n 110: Y +53% / A +47% / yok +0% |
| SPk_ic | n 44: Y +36% / A +64% / yok +0% | n 57: Y +56% / A +42% / yok +2% | n 48: Y +44% / A +52% / yok +4% | n 83: Y +45% / A +52% / yok +4% | n 57: Y +33% / A +67% / yok +0% | n 349: Y +53% / A +47% / yok +0% |
| SPD (10 mum kutu) | n 11: Y +64% / A +36% / yok +0% | n 24: Y +29% / A +71% / yok +0% | n 29: Y +66% / A +34% / yok +0% | n 77: Y +44% / A +52% / yok +4% | n 18: Y +44% / A +56% / yok +0% | n 160: Y +44% / A +56% / yok +0% |
| SPD07 (10 mum kutu) | n 1: Y +100% / A +0% / yok +0% | n 3: Y +33% / A +67% / yok +0% | n 8: Y +50% / A +50% / yok +0% | n 18: Y +44% / A +56% / yok +0% | - | n 32: Y +38% / A +62% / yok +0% |
| SPD15 (10 mum kutu) | n 62: Y +48% / A +52% / yok +0% | n 153: Y +46% / A +54% / yok +0% | n 97: Y +54% / A +46% / yok +0% | n 234: Y +48% / A +49% / yok +3% | n 89: Y +51% / A +49% / yok +0% | n 453: Y +46% / A +54% / yok +0% |
| K_DUZ (10 mum kutu) | n 450: Y +56% / A +44% / yok +0% | n 1066: Y +53% / A +47% / yok +0% | n 225: Y +52% / A +48% / yok +0% | n 509: Y +54% / A +45% / yok +1% | n 143: Y +55% / A +45% / yok +0% | n 615: Y +50% / A +50% / yok +0% |
| SPDb (10 mum kutu) | n 36: Y +56% / A +44% / yok +0% | n 80: Y +44% / A +56% / yok +0% | n 77: Y +65% / A +34% / yok +1% | n 253: Y +53% / A +44% / yok +3% | n 80: Y +41% / A +59% / yok +0% | n 404: Y +46% / A +54% / yok +0% |
| K_DUZb (10 mum kutu) | n 1372: Y +57% / A +43% / yok +0% | n 3531: Y +59% / A +41% / yok +0% | n 675: Y +59% / A +41% / yok +0% | n 1770: Y +61% / A +38% / yok +1% | n 534: Y +57% / A +43% / yok +0% | n 1806: Y +55% / A +45% / yok +0% |
| SP_ic (10 mum kutu) | n 60: Y +52% / A +48% / yok +0% | n 110: Y +56% / A +44% / yok +0% | n 76: Y +53% / A +47% / yok +0% | n 174: Y +51% / A +49% / yok +0% | n 64: Y +34% / A +66% / yok +0% | n 399: Y +51% / A +48% / yok +1% |
| K_SP (10 mum kutu) | n 908: Y +62% / A +38% / yok +0% | n 1771: Y +55% / A +45% / yok +0% | n 389: Y +59% / A +41% / yok +1% | n 792: Y +56% / A +44% / yok +0% | n 237: Y +41% / A +59% / yok +0% | n 1225: Y +60% / A +40% / yok +0% |

Kırılım oran farkı (S+ YUKARI vs kontrol; S- AŞAĞI vs kontrol = ANA; ters yön bilgi):

| Karşılaştırma | genel | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 | TÜM 2023-26 |
|---|---|---|---|---|---|---|---|---|
| SP_ic-K_SP YUKARI [ANA] | AYRIŞMAZ | -12,7% [-35,9%, +9,6%] (60/908) AYRIŞMAZ | -1,3% [-11,0%, +10,7%] (110/1771) AYRIŞMAZ | -6,9% [-21,8%, +9,4%] (76/389) AYRIŞMAZ | -6,9% [-18,4%, +5,3%] (174/792) AYRIŞMAZ | -12,5% [-53,6%, +47,9%] (64/237) AYRIŞMAZ | -7,5% [-24,5%, +8,0%] (399/1225) AYRIŞMAZ | -6,6% [-14,6%, +1,8%] (883/5322) AYRIŞMAZ |
| SP_ic-K_SP_r YUKARI | AYRIŞMAZ | -14,7% [-38,3%, +8,0%] (60/851) AYRIŞMAZ | -1,3% [-11,2%, +11,2%] (110/1662) AYRIŞMAZ | -8,8% [-25,0%, +8,4%] (76/344) AYRIŞMAZ | -6,7% [-17,9%, +5,5%] (174/708) AYRIŞMAZ | -11,8% [-50,0%, +47,6%] (64/234) AYRIŞMAZ | -9,6% [-27,0%, +7,1%] (399/1095) AYRIŞMAZ | -7,4% [-15,4%, +1,3%] (883/4894) AYRIŞMAZ |
| SM_ic-K_SM ASAGI [ANA] | AYRIŞMAZ | -1,7% [-20,7%, +16,1%] (57/911) AYRIŞMAZ | -7,5% [-22,4%, +9,5%] (85/1773) AYRIŞMAZ | -8,9% [-26,4%, +9,2%] (33/391) AYRIŞMAZ | -10,4% [-22,6%, -0,4%] (88/799) AYRIŞMAZ | -4,1% [-64,8%, +73,4%] (2/242) ÖLÇÜLEMEDİ | -7,9% [-25,1%, +16,0%] (34/1249) AYRIŞMAZ | -7,1% [-14,9%, +0,7%] (299/5365) AYRIŞMAZ |
| SM_ic-K_SM_r ASAGI | AYRIŞMAZ | +0,2% [-19,6%, +19,5%] (57/852) AYRIŞMAZ | -7,8% [-23,0%, +9,4%] (85/1662) AYRIŞMAZ | -11,6% [-31,0%, +9,3%] (33/338) AYRIŞMAZ | -11,0% [-23,0%, -1,1%] (88/718) AYRIŞMAZ | -3,8% [-64,4%, +73,1%] (2/236) ÖLÇÜLEMEDİ | -6,9% [-25,1%, +17,5%] (34/1112) AYRIŞMAZ | -6,9% [-15,2%, +1,1%] (299/4918) AYRIŞMAZ |
| SP_ic-K_SP ASAGI | AYRIŞMAZ | +13,1% [-9,0%, +36,2%] (60/908) AYRIŞMAZ | -1,0% [-14,0%, +9,1%] (110/1771) AYRIŞMAZ | +4,8% [-9,4%, +18,9%] (76/389) AYRIŞMAZ | +6,3% [-5,9%, +17,3%] (174/792) AYRIŞMAZ | +12,5% [-47,9%, +53,6%] (64/237) AYRIŞMAZ | +7,5% [-8,2%, +24,5%] (399/1225) AYRIŞMAZ | +6,0% [-2,4%, +13,8%] (883/5322) AYRIŞMAZ |
| SM_ic-K_SM YUKARI | AYRIŞMAZ | +2,1% [-15,8%, +21,1%] (57/911) AYRIŞMAZ | +6,8% [-9,4%, +20,6%] (85/1773) AYRIŞMAZ | +8,9% [-9,1%, +27,7%] (33/391) AYRIŞMAZ | +3,7% [-9,6%, +16,3%] (88/799) AYRIŞMAZ | +4,1% [-73,4%, +64,8%] (2/242) ÖLÇÜLEMEDİ | +8,2% [-15,8%, +25,3%] (34/1249) AYRIŞMAZ | +4,6% [-3,8%, +12,8%] (299/5365) AYRIŞMAZ |
| SPD-K_SP YUKARI (10 mum kutu) | AYRIŞMAZ | +1,7% [-13,8%, +17,5%] (11/908) ÖLÇÜLEMEDİ | -25,9% [-44,9%, -2,3%] (24/1771) ÖLÇÜLEMEDİ | +6,6% [-13,9%, +25,9%] (29/389) ÖLÇÜLEMEDİ | -11,5% [-21,6%, +0,0%] (77/792) AYRIŞMAZ | +3,1% [-47,0%, +43,8%] (18/237) ÖLÇÜLEMEDİ | -15,3% [-31,0%, -0,8%] (160/1225) AYRIŞMAZ | -11,3% [-19,0%, -3,1%] (319/5322) AYRIŞMAZ |
| SPD-K_DUZ YUKARI (10 mum kutu) | AYRIŞMAZ | +7,2% [-8,0%, +23,4%] (11/450) ÖLÇÜLEMEDİ | -24,1% [-42,2%, -1,5%] (24/1066) ÖLÇÜLEMEDİ | +14,0% [-8,1%, +34,2%] (29/225) ÖLÇÜLEMEDİ | -9,9% [-19,0%, +0,6%] (77/509) AYRIŞMAZ | -10,8% [-50,2%, +39,9%] (18/143) ÖLÇÜLEMEDİ | -5,9% [-19,9%, +7,4%] (160/615) AYRIŞMAZ | -7,5% [-15,0%, +0,3%] (319/3008) AYRIŞMAZ |
| SPD07-K_DUZ YUKARI (10 mum kutu) | ÖLÇÜLEMEDİ | +43,6% [+30,9%, +55,0%] (1/450) ÖLÇÜLEMEDİ | -19,9% [-25,2%, -15,3%] (3/1066) ÖLÇÜLEMEDİ | -1,6% [-35,9%, +24,8%] (8/225) ÖLÇÜLEMEDİ | -9,6% [-30,9%, +11,3%] (18/509) ÖLÇÜLEMEDİ | - [-, -] (0/143) ÖLÇÜLEMEDİ | -12,7% [-33,8%, +10,5%] (32/615) AYRIŞMAZ | -11,3% [-23,7%, +2,0%] (62/3008) AYRIŞMAZ |
| SPD15-K_DUZ YUKARI (10 mum kutu) | AYRIŞMAZ | -8,1% [-27,1%, +14,9%] (62/450) AYRIŞMAZ | -6,9% [-15,9%, +3,7%] (153/1066) AYRIŞMAZ | +2,1% [-14,7%, +16,2%] (97/225) AYRIŞMAZ | -6,2% [-14,0%, +1,5%] (234/509) AYRIŞMAZ | -4,7% [-43,2%, +40,4%] (89/143) AYRIŞMAZ | -4,3% [-17,8%, +7,9%] (453/615) AYRIŞMAZ | -5,6% [-12,1%, +1,1%] (1088/3008) AYRIŞMAZ |
| SPDb-K_DUZb YUKARI (10 mum kutu) | AYRIŞMAZ | -1,4% [-18,9%, +16,6%] (36/1372) AYRIŞMAZ | -15,6% [-26,5%, -4,4%] (80/3531) AYRIŞMAZ | +6,1% [-14,8%, +21,2%] (77/675) AYRIŞMAZ | -7,9% [-14,7%, -0,8%] (253/1770) AYRIŞMAZ | -15,5% [-34,6%, +5,3%] (80/534) AYRIŞMAZ | -9,3% [-18,0%, -0,8%] (404/1806) AYRIŞMAZ | -9,1% [-14,4%, -3,6%] (930/9688) AYRIŞMAZ |
| SP_ic-K_SP YUKARI (10 mum kutu) | AYRIŞMAZ | -10,2% [-34,3%, +12,1%] (60/908) AYRIŞMAZ | +1,3% [-8,5%, +15,1%] (110/1771) AYRIŞMAZ | -6,2% [-19,5%, +6,8%] (76/389) AYRIŞMAZ | -5,1% [-15,0%, +5,5%] (174/792) AYRIŞMAZ | -7,0% [-49,1%, +53,3%] (64/237) AYRIŞMAZ | -8,3% [-24,4%, +6,9%] (399/1225) AYRIŞMAZ | -6,3% [-13,9%, +1,9%] (883/5322) AYRIŞMAZ |

Genel S+ (tavan / dip yok; bilgi): cetvel once20 (60 günde önce +%20, -%10'dan önce) olay oranı / eş oranı:

| Satır | ABD 2023 | ABD 2024-26 | AVR 2023 | AVR 2024-26 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|
| SP_ic | n 60: +25% / +26% | n 110: +34% / +27% | n 76: +13% / +12% | n 175: +15% / +16% | n 64: +20% / +20% | n 399: +39% / +39% |
| SP_dis | n 861: +23% / +23% | n 2117: +25% / +25% | n 617: +12% / +11% | n 1685: +16% / +16% | n 669: +38% / +38% | n 2369: +38% / +37% |
| SP_tum | n 880: +22% / +23% | n 2160: +26% / +26% | n 646: +12% / +12% | n 1730: +16% / +16% | n 674: +37% / +37% | n 2428: +38% / +37% |
| K_SP | n 908: +31% / +30% | n 1771: +26% / +26% | n 389: +15% / +15% | n 793: +20% / +18% | n 237: +33% / +32% | n 1226: +43% / +42% |
| SM_ic | n 57: +21% / +24% | n 85: +32% / +28% | n 33: +15% / +12% | n 88: +17% / +16% | n 2: +0% / +38% | n 34: +44% / +48% |
| SM_tum | n 922: +26% / +27% | n 2350: +25% / +26% | n 590: +10% / +11% | n 1556: +13% / +15% | n 277: +35% / +37% | n 510: +36% / +42% |
| K_SM | n 911: +31% / +30% | n 1773: +25% / +26% | n 391: +15% / +15% | n 801: +20% / +18% | n 242: +31% / +30% | n 1250: +43% / +42% |

## CEMAL ÖRNEKLERİ (HALKA 1 ve 3; n küçük, BİLGİ)

| Örnek | pencere | S+ günleri | gevşek / sıkı / küçük S+ | S- günleri | S6 taban içi günleri |
|---|---|---|---|---|---|
| PAPIL | 2025-11-13 .. 2025-12-09 | 2025-11-14, 2025-11-17, 2025-11-18, 2025-11-19, 2025-11-20, 2025-11-21, 2025-11-24, 2025-11-25, 2025-11-26, 2025-12-08 | 18 / 1 / 7 gün | yok | 2025-12-03, 2025-12-04, 2025-12-05, 2025-12-08, 2025-12-09 |
| TEHOL_2505 | 2025-05-02 .. 2025-05-28 | 2025-05-05, 2025-05-06, 2025-05-07, 2025-05-08, 2025-05-09, 2025-05-12, 2025-05-13, 2025-05-14, 2025-05-15, 2025-05-16, 2025-05-20, 2025-05-21, 2025-05-22, 2025-05-23, 2025-05-26, 2025-05-27, 2025-05-28 | 18 / 13 / 14 gün | yok | YOK (taban açık değil) |
| BINBN | 2024-12-17 .. 2025-01-21 | 2024-12-23, 2024-12-24, 2024-12-25, 2024-12-26, 2024-12-27, 2024-12-30, 2024-12-31, 2025-01-02, 2025-01-03, 2025-01-06, 2025-01-07, 2025-01-08, 2025-01-09, 2025-01-10, 2025-01-13, 2025-01-21 | 20 / 8 / 0 gün | yok | YOK (taban açık değil) |
| TEHOL_bolge | 2025-03-03 .. 2025-05-28 | 2025-04-24, 2025-04-25, 2025-05-05, 2025-05-06, 2025-05-07, 2025-05-08, 2025-05-09, 2025-05-12, 2025-05-13, 2025-05-14, 2025-05-15, 2025-05-16, 2025-05-20, 2025-05-21, 2025-05-22, 2025-05-23, 2025-05-26, 2025-05-27, 2025-05-28 | 26 / 13 / 14 gün | yok | YOK (taban açık değil) |

| Örnek | olay | t | giriş | taban içi | r60 / eşli fark | r20 / eşli fark | kırılım |
|---|---|---|---|---|---|---|---|
| PAPIL | ilk_SP | 2025-11-14 | 2025-11-17 | hayır | +16,5% / +2,9% | +15,7% / +12,8% | UYGULANMAZ |
| PAPIL | son_gun | 2025-12-09 | 2025-12-10 | EVET | +16,2% / +19,1% | +5,9% / +6,0% | YUKARI |
| TEHOL_2505 | ilk_SP | 2025-05-05 | 2025-05-06 | hayır | +20,9% / +3,0% | +6,1% / +13,0% | UYGULANMAZ |
| TEHOL_2505 | son_gun | 2025-05-28 | 2025-05-29 | hayır | +100,0% / +44,8% | +15,5% / +14,1% | UYGULANMAZ |
| BINBN | ilk_SP | 2024-12-23 | - | hayır | - / - | - / - | UYGULANMAZ |
| BINBN | son_gun | 2025-01-21 | 2025-01-22 | hayır | +158,5% / +162,7% | +8,8% / +16,4% | UYGULANMAZ |
| TEHOL_bolge | ilk_SP | 2025-04-24 | 2025-04-25 | hayır | +6,2% / -12,5% | -1,1% / -3,2% | UYGULANMAZ |
| TEHOL_bolge | son_gun | 2025-05-28 | 2025-05-29 | hayır | +100,0% / +44,8% | +15,5% / +14,1% | UYGULANMAZ |

## HALKA 2 — ALGILAMA (kör set hazır)

- FITIL_KOR_SET.pdf: 56 sayfa (1 açıklama + 5 kalibrasyon + 50 kör grafik); PDF sha `03d89fb570a3726717dd8a828e99cc06e81b1b736ee28e1c9a59c91317c1c551`.
- Kör grafik dağılımı (anahtar gizli; yalnız sayım): SM ABD 5, SM BIST 5, SPD ABD 5, SPD BIST 5, SP_dis ABD 7, SP_dis BIST 8, SP_ic ABD 8, SP_ic BIST 7.
- Değerlendirme komutu: `python FITIL_KOR.py olc --cevap "1:E,2:H,3:B,..."` (50 numaranın hepsi; E / H / B).
- Okuma kuralı (önceden yazılı): olc: E payı (B hariç payda ve B dahil ikisi de yazılır). 'ALGILAMA SAĞLAM' = S+ E payı >= 0,60 VE S+ E payı - S- E payı >= 0,30; 'ALGILAMA KIRIK' = S+ E payı < 0,40; arası 'KISMİ'. Taban içi / dışı E payı ve Fisher kesin p bilgi; n küçük (30 / 10): 'bulgu' değil, tanı.

Kalibrasyon sayfaları (kodun ölçtüğü):

| Hisse | pencere | mum | alt fitilsiz payı | üst fitilsiz payı | alt medyan | üst medyan | kapanış konumu medyan | yeşil payı | ASIM min / maks | S+ gün | S- gün | taban içi gün |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PAPIL | 2025-11-13 .. 2025-12-09 | 19 | 0,47 | 0,11 | 0,12 | 0,44 | 0,17 | 0,26 | 0,11 / 0,33 | 2025-11-14, 2025-11-17, 2025-11-18, 2025-11-19, 2025-11-20, 2025-11-21, 2025-11-24, 2025-11-25, 2025-11-26, 2025-12-08 (g/s/k 18/1/7) | yok | 2025-12-03, 2025-12-04, 2025-12-05, 2025-12-08, 2025-12-09 |
| TEHOL_2505 | 2025-05-02 .. 2025-05-28 | 18 | 0,78 | 0,00 | 0,03 | 0,66 | 0,04 | 0,17 | 0,25 / 0,62 | 2025-05-05, 2025-05-06, 2025-05-07, 2025-05-08, 2025-05-09, 2025-05-12, 2025-05-13, 2025-05-14, 2025-05-15, 2025-05-16, 2025-05-20, 2025-05-21, 2025-05-22, 2025-05-23, 2025-05-26, 2025-05-27, 2025-05-28 (g/s/k 18/13/14) | yok | yok |
| TEHOL_bolge | 2025-03-03 .. 2025-05-28 | 56 | 0,48 | 0,23 | 0,10 | 0,33 | 0,24 | 0,45 | -0,13 / 0,62 | 2025-04-24, 2025-04-25, 2025-05-05, 2025-05-06, 2025-05-07, 2025-05-08, 2025-05-09, 2025-05-12, 2025-05-13, 2025-05-14, 2025-05-15, 2025-05-16, 2025-05-20, 2025-05-21, 2025-05-22, 2025-05-23, 2025-05-26, 2025-05-27, 2025-05-28 (g/s/k 26/13/14) | yok | yok |
| BINBN | 2024-12-17 .. 2025-01-21 | 25 | 0,52 | 0,08 | 0,09 | 0,59 | 0,11 | 0,20 | 0,08 / 0,56 | 2024-12-23, 2024-12-24, 2024-12-25, 2024-12-26, 2024-12-27, 2024-12-30, 2024-12-31, 2025-01-02, 2025-01-03, 2025-01-06, 2025-01-07, 2025-01-08, 2025-01-09, 2025-01-10, 2025-01-13, 2025-01-21 (g/s/k 20/8/0) | yok | yok |
| DGXX | 2026-10-20 .. 2026-11-16 | 19 | 0,05 | 0,26 | 0,27 | 0,20 | 0,41 | 0,26 | -0,25 / 0,05 | yok (g/s/k 0/0/0) | yok | yok |

## VERİ ve SINIRLAR

- ABD: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 1411
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 580
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 581
- Hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, AŞAĞI kırılım oranı aşağı yanlı okunmalı. Komisyon yok; 31.08.2026 sonrası yok.
- r20 hücrelerinde güç tablosu uygulanmaz ('tutar' bilgi). Kırılım yalnız taban içi (tavan / dip tanımlı) olaylarda.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | (a) eşler YALNIZ ORTAK_CETVEL.oc_olc (aynı giriş günü, 60 gün momentum beşlisi x 20 gün likidite üçlüsü, 200 plasebo); (b) kontrol = TABAN İÇİ ama S+ olmayan günler (aynı S6 bölge ailesi, aynı cetvel mekaniği) + bölge başına tek rastgele gün (K_SP_r, konum dengesi); kırılım kontrolü aynı bölge kutusu. Mekanik üstünlük: S+ kapanış dipte -> giriş t+1 açılış; kırılım tavanı t günü dahil kutu, t kapanışı tavanın altında (S6 AL tanımı) |
| K2 | geleceğe bakma | EVET | fitil pencereleri rolling (geriye); S6 durum makinesi sıralı (as-of t: bölge, sınıf = onay günü sınıfı, kutu t'ye kadar); kos fk_gelecek_denetimi her pazarda 40 olayda seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; kör sayfada t'den sonra bar çizilmez (test) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz barları (H>L, V>0, fiyat > 0); geçersiz bar sinyal / ölçü üretmez; DGXX kalibrasyonunda 16 Kas seans içi yarım bar atılır |
| K4 | tekilleştirme | EVET | cetvel oc_olay_hazirla aynı hissede 60 gün tekilleştirir (n bağımsız olay); kırılım cetvelin tekil olaylarında; kör sette aynı hisse bir kez; hücrede medyan da yazılır |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (cetvel); kırılım t+1 kapanışından itibaren; kör anahtarı sonucu da t+1 açılış |
| K6 | veri birimi | EVET | tek kip V_*.pkl düzeltilmiş fiyat (fi_k1_veri); fitil payları ve oransal eksen birimden bağımsız; DGXX ham (auto_adjust=False) yalnız kalibrasyon, fitil payı birim etkisiz |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı yanlı' notu; kırılımda AŞAĞI oranı aşağı yanlı okunur |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı (cetvel); varyantlar bilgi; kör set 30 + 10 küçük n: 'tanı', bulgu değil; olay sayımı bu ön kayıtta getirisiz |
| K9 | ön kayıt | EVET | FK_ESIK sha + FITIL_KOR.py sha + FO_ESIK sha + S6_PRM sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce git'e işlendi; kos / kor ik_kontrol_kapisi + oc_kapi + fk_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; kalibrasyon sayfalarında fitil payları ham bardan yazılır |
| K11 | yeniden üretim | EVET | olay satırları FK_SATIR klasöründe (olay_<satır>_<r>.csv.gz); >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | etiketler yalnız önceden yazılı kurallarla; 'iz / emare' sözü yalnız kural geçerse; sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok; kör PDF'te hisse / tarih / sonuç yok |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fk; defter dosyaları ve mevcut .py modülleri yalnız import (git status); e-posta / anahtar taraması (ön kayıt, sonuç, rapor, anahtar); commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tanı ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## DENETİM (K11; bağımsız kod scratchpad fk_den/fk_yeniden.py, FITIL_KOR fonksiyonları kullanılmadan)

- h1b SP_ic-K_SP ABD 2024-26 (n 110 / 1771, fark +0,01738), AVR 2024-26 (175 / 793, -0,00437), SPD-K_DUZ ABD 2024-26 (24 / 1066, +0,08291): olay csv'den yeniden üretildi, rapor ile aynı.
- Kırılım YUKARI oran farkı SP_ic-K_SP ABD 2024-26 (-0,0126) ve BIST 2024-26 (-0,0755): aynı.
- 6 olay (BIST GEDIK, KAYSE, PETUN; ABD KMI, TKO, RPRX) ham V_*.pkl'den: giriş günü, giriş açılışı ve kırılım (S6 kutusu, elle kural) aynı.
- Geleceğe bakma denetimi koşu içinde her pazarda 40 olay TUTTU; test 40 / 40.

## HATA

- H-a (süreç): ön kayıt üç kez yazıldı, hepsi ölçüm sonucu görülmeden: v0 (20:45) yazıldıktan sonra Cemal'in TEHOL düzeltmesi (Şubat 2026 etiketi kaldırıldı, bölge 2024-12 .. 2025-05-28) ve S+DÜZ ek tanımı geldi -> v1 (20:54); kör set ilk koşuda SPD grubu havuz süzgecine eklenmediği için durdu (0 < 5) ve kos 2 dakikada (sonuç dosyası yokken) durduruldu -> kod düzeltildi, v2 (20:58). v0 / v1 kopyaları scratchpad'de (KOR_SET_ON_KAYIT_v0.md, _v1.md). Ders: ek tanımlar gelince kör seti ve kos'u aynı ön kayıttan sonra başlat; ek grup eklerken bütün süzgeç listelerini tara.
- H-b (yanlış yorum riski / tanım): önceden yazılı 'taban içi' tanımı (DİP sınıfı, as-of onay, 250 bar şartı) Cemal'in üç örneğini de dışarıda bıraktı; bu kalibrasyon ön kayıttan önce görülebilirdi (PAPIL as-of onay 3 Ara) ama tanım iş tanımının harfine göre bırakıldı. Ders: bağlam tanımı önce etiketli örneklerde sınanmalı (kalibrasyon kapısı), sonra ölçülmeli.
- H-c (tanım, bilgi): coordinator'ın S+DÜZ tanımındaki 'dip bağlamı' (konum120 <= 0,25 ya da taban içi) TEHOL Mayıs ve BINBN'yi dışarıda bıraktı (kalibrasyonda görüldü, getiri görülmeden); bu yüzden bağlamsız bilgi varyantı SPDb / K_DUZb eklendi. SPDb'nin tek tutan hücresi bu eklemeden doğan çoklu karşılaştırma içinde okunmalı.
- H-d (test): kör sayfa testinin ilk sürümü gri zemin dikdörtgenini mum saydı (51 vs 50); test düzeltildi (kod değil).
- H-e (gösterim): kalibrasyon sayfalarında üst açıklama ve alt özet satırı A4 yatay genişliği aşıp sağda kesiliyor; sayılar raporda ve anahtarda tam. Kör set bir kez üretildiği için (tohum, anahtar) yeniden basılmadı.
- H-f (veri): BINBN ilk S+ günü (23 Ara 2024) cetvel havuzunun dışında kaldı (geçmiş eksik: 60 gün momentum yok, yeni hisse); yalnız pencere sonu olayı ölçüldü.
- H-g (ölçü farkı, hata değil): ana modelin 'ASİM ort' değerleri (TEHOL 0,56, BINBN 0,42, PAPIL 0,26) bar düzeyi üst - alt ortalaması; kalibrasyon sayfasındaki ASIM k10 yuvarlanan pencere ortalaması (TEHOL 0,25 .. 0,62); karşılaştırırken aynı ölçü kullanılmalı.

## ÖNERİLEN DEFTER METNİ (ana model işler)

Ç188 FİTİL ÖBEĞİ ÜÇ HALKA (FITIL_KOR.py; ön kayıt KOR_SET_ON_KAYIT.md sha 7349e099d6af…, yazım 21:05:30 UTC, koşu 21:05:35 UTC, gitsiz): HALKA 1 taban içi S+ (S6 DİP, as-of) eşlerden ve taban içi S+ olmayan günlerden ayrışmadı (karar hücreleri n 60-175, ÖLÇÜLEMEDİ / AYRIŞMAZ); HALKA 3 r20 ve 'önce tavan mı dip mi' ölçüsü de ayrışmadı, kırılımda S+ sonrası önce-tavan oranı kontrolden -6,6 puan (anlamsız, ters yön). Tanım bağlamı Cemal'in üç örneğini (PAPIL as-of onay geç, TEHOL Mayıs 2025 S6 sınıfı ORTA, BINBN 250 bar yok) kapsamıyor: bağlam yeniden tanımlanmalı (yükseliş / geri çekilme sonrası sıkışma). Kodun S+'ı üç örnekte de yanıyor (algılama örneklerde çalışıyor); DGXX'te S- yanmıyor. EK S+DÜZ: dipte n küçük (ÖLÇÜLEMEDİ); bağlamsız SPDb ABD 2024-26 TUTAR (n 80, +6,7%) ama kırılımda ters: EMARE değil, ileri test adayı. HALKA 2 kör set hazır (FITIL_KOR_SET.pdf 56 sayfa: 1 açıklama + 5 kalibrasyon + 50 kör; anahtar kor_anahtar.json gizli); Cemal yanıtı -> `python FITIL_KOR.py olc --cevap "1:E,..."`. İleri test: kör set yanıtı; yeni bağlam tanımıyla yeni ön kayıt.
