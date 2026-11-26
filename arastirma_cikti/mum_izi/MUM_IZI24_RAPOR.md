# MUM_IZI24 RAPOR — KODUN SEÇTİĞİ BÖLGELER (aday kuralı + mum boyu kapısı ORAN <= 0,70; göz onayı YOK), 15 mumluk sonrası

Tarih: 26 Kasım 2026. İş tanımı MUM_IZI24_IS_TANIMI.md; ön kayıt MUM_IZI24_ON_KAYIT.md (commit 536419b6c5dc71b812baf023a6139d53f578df30 2026-11-26T17:01:58+00:00); kod MUM_IZI_HAVUZ.py (commit ae2a235); olay satırları mum_izi24_olay.csv.gz (sha 7fd6439b8eebff16…), sonuç mum_izi24_sonuc.json.
Okuma sınırı: bu bölgeler KODUN seçtiği bölgelerdir, kalıbın kendisi değildir (Cemal'in göz onayında kodun gösterdiği 24 bölgenin %42'si BENZİYOR, %75'i BENZİYOR ya da KISMEN). Evren bugün yaşayan hisseler: bütün getiriler yukarı yanlı. Veri <= 2022-12-31; kasa açılmadı.

## SONUÇ

- KODUN SEÇTİĞİ BÖLGELER (ANA ÖRNEK, KAPILI): günlük 256 ölçülen / 231 eşli, haftalık 127 / 122. Eşli fark ortalaması günlük -0,85 puan [ay kümeli %95: -2,31; +0,60], haftalık -2,28 [-5,61; +1,06]; eşinden iyi payı günlük %42,0, haftalık %43,4. R15 ortalama / medyan günlük -0,13 / -0,63 %, haftalık +4,51 / +1,71 %.
- Karar hücrelerinin hepsi ÖLÇÜLEMEDİ (iki zaman dilimi, ANA ve duyarlılık). Günlükte ABD hücreleri n 63 / 75 ama güç 0,26 / 0,24 (< 0,80; 0,80 için 255 / 339 gerekir); AVR n 11 / 6; haftalıkta bütün karar hücreleri n < 30 (ABD 13 / 8, AVR 3 / 1). Hiçbir hücre TUTAR değil; en yakın günlük ABD 2020-22 (eşli fark +0,46 [-3,37; +3,11], sıra 0,497, slot yüzdeliği 0,21).
- GENEL: günlük ÖLÇÜLEMEDİ; haftalık ÖLÇÜLEMEDİ (eksik hücre: dördü de). Ön kayıtta 'beklenen ÖLÇÜLEMEDİ' yazılıydı.
- KAPI ETKİSİ (KAPILI - KAPISIZ eşli fark): günlük -0,88 puan [-2,44; +0,55], p 0,24; haftalık -1,03 [-5,37; +3,17], p 0,67. Mum boyu kapısı bu ölçüde eşe karşı bir üstünlük eklemiyor; yön hafif eksi, anlamlı değil.
- KAPISIZ kontrol (aday kuralının ORAN > 0,70 olayları; bilgi): günlük ABD 2016-19 n 1.616 eşli fark -0,13 [-0,68; +0,43], ABD 2020-22 n 1.468 +0,18 [-0,51; +0,82], AVR 2016-19 n 236 -0,44 [-1,04; +0,17]: güç >= 0,80 ile TUTMADI. Yani aday kuralının kendisi 15 günde eşinden ayrışmıyor (bu, yeterli güçle ölçülen tek sonuç).
- +%5 hedef: günlük KAPILI bölgelerin %50,4'ü 15 mumda +%5'i stop'tan önce gördü, eşli hedef payı +1,7 puan; haftalıkta %74,8, eşli -4,0 puan. Mutlak pay yüksek görünür ama eşler de aynı payı görüyor.
- BIST (bilgi): günlük 2016-19 n 31 eşli fark -2,05, 2020-22 n 45 -0,76; haftalık n 7 / 10 (-12,97 / -6,45). 2016 öncesi (bilgi): haftalık ABD n 70 -1,81 [-5,51; +1,91]; günlük 2016 öncesi olay yok (günlük veri 2015'ten başlıyor, ORAN için 120 bar gerekiyor).
- Duyarlılık (hariç bölgeler dahil): günlük n 273, eşli fark -0,95 [-2,37; +0,32]; haftalık n 136, -2,08 [-5,43; +1,28]; hüküm değişmedi (ÖLÇÜLEMEDİ).
- Okuma: kodun seçtiği bütün bölgelerde (göz ölçümündeki 36'nın yaklaşık 10 katı) 15 mumluk eşli fark sıfırın biraz altında; 'eşlerinden iyi gitti' diyecek bir sayı yok. Güç yetersiz olduğu için 'tutmadı' da yazılamaz. KASA açılmaz; tek iz değil, birleşik iz bileşeni adayı da değil.

## Makine

- ORTAK CETVEL fonksiyonları kullanıldı: C2.c2_hucre (FARK, medyan, SIRA, ay kümeli bootstrap YH.yh_d3_boot_l3o, ay kümeli işaret permütasyonu DS.ds_perm_p), C2.c2_guc / C2._c2_egri22_al (cetvel2_guc_v2.2 H 15) / C2.c2_guc_egri, C2.c2_panel22_al (eş paneli), BOFA_IZI.bi_slot (10 yuvalı slot); ölçü GZ.gz_olc_bir, eş GZ.gz_es_grup, geçit / +%5 G2.k17_gecit_bir / k17_dokunma, ORAN HK.hk_olay_oran.
- Kendi kurulanlar ve nedeni: (1) hüküm MU.mu_hukum değil, iş tanımının dört şartı (mu_hukum L3O, sıra bootstrap alt ucu ve plasebo TUTAR payı ister; iş tanımı şartları farklı); (2) 200 eşli rastgele portföy (C2.c2_plasebo hücre plasebosudur, slot portföyü değil): her olay yerine aynı gün aynı kovadan eş üyesi R'si; (3) haftalık güç eğrisi plasebodan (cetvel2'de 15 haftalık ufuk yok); (4) KAPI ETKİSİ için tabakalı (pazar x giriş ayı) permütasyon ve ay kümeli bootstrap (iki grup aynı aylarda bir arada; ay etiketini karıştırmak anlamsız olduğu için etiketler ay içinde karıştırıldı); (5) eş üyelerinin R'leri (hv_es_uye; gz_es_grup ile n_es ve es_R15 birebir denetlendi). Hepsi ön kayıtta yazılıydı.

## Yeniden üretim

- Olay csv'sinden bağımsız kısa kodla (pandas; kendi ay kümeli bootstrap'ım, tohum 1, B 4000): günlük ABD 2020-22 KAPILI ANA n 75, eşli fark +0,459 puan [-3,46; +3,08] (rapor +0,46 [-3,37; +3,11]; boot farkı tohum / B farkı), sıra 0,4967, +%5 payı %56,0, eşli hedef payı +9,0 puan: rapordakiyle aynı. Haftalık hepsi KAPILI ANA: eşli n 122, ölçülen 127, R15 ort +4,51 %, medyan +1,71 %, eşli fark -2,277, eşinden iyi %43,4: aynı. KAPI ETKİSİ günlük tum fark farkı -0,876 puan (231 / 4.056): aynı.
- Mekanik denetimler (kodda DUR): getirisiz geçit = gz_olc_bir; takvimler (bölge başı / sonu / giriş / 15. mum) iki aşamada aynı; haftalık k17_dokunma +%10 = GZ d10; hv_es_uye n_es ve es_R15 = gz_es_grup; eşli küme = getirisiz sayımdaki küme; SAYIM_SHA kos'ta yeniden hesaplanıp ön kayıtla aynı çıktı. Olay csv'si: en geç giriş ve 15. mum 2022-12-30; bütün girişler bölge sonundan sonra; KAPILI <=> ORAN <= 0,70 (en büyük KAPILI 0,69998, en küçük KAPISIZ 0,70012); hücre ataması giriş tarihine göre yeniden hesaplandı, aynı.
- Testler: python test_mum_izi_havuz.py (12 test geçti).

## Tablolar

### GUNLUK — KODUN SEÇTİĞİ BÖLGELER (ANA ÖRNEK, KAPILI)

| hücre | rol | n eşli | eşli fark ort [ay kümeli %95] | medyan | ort sıra | +%5 payı / eşli hedef payı | +%10 payı / eşli | slot yüzdeliği | güç | hüküm (neden) |
|---|---|---|---|---|---|---|---|---|---|---|
| ABD|d1619 | KARAR | 63 | -1,71 [-3,47; +0,38] | -1,32 | 0,438 | +32,8 / -4,3 | +17,2 / +4,0 | 0,03 | 0,26 | ÖLÇÜLEMEDİ (FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| ABD|d2022 | KARAR | 75 | +0,46 [-3,37; +3,11] | -0,07 | 0,497 | +56,0 / +9,0 | +38,7 / +12,4 | 0,21 | 0,24 | ÖLÇÜLEMEDİ (boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| AVR|d1619 | KARAR | 11 | -3,00 [-6,73; -0,28] | -0,27 | 0,371 | +36,4 / +3,8 | +0,0 / -6,7 | 0,01 | 0,09 | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| AVR|d2022 | KARAR | 6 | +1,18 [-2,44; +5,35] | +0,11 | 0,530 | +33,3 / +11,8 | +16,7 / +7,3 | 0,72 | 0,06 | ÖLÇÜLEMEDİ (n < 30; boot alt <= 0; slot <= %90) |
| BIST|d1619 | BİLGİ | 31 | -2,05 [-6,10; +1,80] | -0,89 | 0,477 | +61,5 / +3,9 | +35,9 / +5,5 | 0,05 | 0,18 | ÖLÇÜLEMEDİ (FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| BIST|d2022 | BİLGİ | 45 | -0,76 [-3,63; +2,93] | -3,52 | 0,451 | +59,0 / -5,3 | +37,7 / -0,6 | 0,30 | 0,19 | ÖLÇÜLEMEDİ (FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| ABD|o16 | BİLGİ | 0 | - [-; -] | - | - | - / - | - / - | - | - | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| AVR|o16 | BİLGİ | 0 | - [-; -] | - | - | - / - | - / - | - | - | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| BIST|o16 | BİLGİ | 0 | - [-; -] | - | - | - / - | - / - | - | - | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |

GENEL (gunluk, ANA): **ÖLÇÜLEMEDİ**; ölçülemeyen karar hücreleri: ABD|d1619, ABD|d2022, AVR|d1619, AVR|d2022. DUYARLILIK (hepsi dahil): ÖLÇÜLEMEDİ.

| hepsi birlikte | n eşli | n ölçülen | R15 ort / medyan | eşli fark ort [ay kümeli %95] | eşinden iyi payı | +%5 / eşli hedef | slot yüzdeliği | pazar |
|---|---|---|---|---|---|---|---|---|
| KAPILI | 231 | 256 | -0,13 / -0,63 | -0,85 [-2,31; +0,60] | 0,420 | +50,4 / +1,7 | 0,03 | {"ABD": 138, "BIST": 76, "AVR": 17} |
| KAPISIZ | 4056 | 4245 | +1,26 / +0,91 | +0,02 [-0,33; +0,36] | 0,478 | +53,4 / +2,4 | 0,85 | {"ABD": 3084, "BIST": 588, "AVR": 384} |
| KAPILI_DUY | 273 | 305 | -0,17 / -0,61 | -0,95 [-2,37; +0,32] | 0,410 | +49,5 / +1,1 | 0,01 | {"ABD": 172, "BIST": 81, "AVR": 20} |
| KAPISIZ_DUY | 4103 | 4295 | +1,24 / +0,89 | +0,01 [-0,34; +0,34] | 0,478 | +53,3 / +2,4 | 0,82 | {"ABD": 3121, "BIST": 592, "AVR": 390} |

| KAPI ETKİSİ (KAPILI - KAPISIZ, ANA) | n KAPILI / KAPISIZ | eşli fark KAPILI / KAPISIZ | fark farkı [ay kümeli %95] | p (tabakalı perm, iki yönlü) | eşinden iyi KAPILI / KAPISIZ |
|---|---|---|---|---|---|
| tum | 231 / 4056 | -0,85 / +0,02 | -0,88 [-2,44; +0,55] | 0,2380 | 0,420 / 0,478 |
| karar_birlikte | 155 / 3468 | -0,64 / -0,03 | -0,61 [-2,49; +1,24] | 0,4294 | 0,445 / 0,486 |
| ABD|d1619 | 63 / 1616 | -1,71 / -0,13 | -1,58 [-3,52; +0,56] | 0,1855 | 0,413 / 0,493 |
| ABD|d2022 | 75 / 1468 | +0,46 / +0,18 | +0,28 [-3,51; +2,88] | 0,8292 | 0,493 / 0,483 |
| AVR|d1619 | 11 / 236 | -3,00 / -0,44 | -2,55 [-6,43; +0,37] | 0,0433 | 0,273 / 0,453 |
| AVR|d2022 | 6 / 148 | +1,18 / -0,24 | +1,42 [-2,71; +6,42] | 0,5517 | 0,500 / 0,493 |

| KAPISIZ (bilgi) / DUYARLILIK KAPILI hücreleri | KAPISIZ n / fark / hüküm | KAPILI hepsi dahil n / fark [%95] / hüküm |
|---|---|---|
| ABD|d1619 | 1616 / -0,13 / TUTMADI | 76 / -1,63 [-2,93; +0,15] / ÖLÇÜLEMEDİ |
| ABD|d2022 | 1468 / +0,18 / TUTMADI | 96 / +0,02 [-3,46; +2,14] / ÖLÇÜLEMEDİ |
| AVR|d1619 | 236 / -0,44 / TUTMADI | 12 / -2,45 [-6,58; +0,16] / ÖLÇÜLEMEDİ |
| AVR|d2022 | 148 / -0,24 / ÖLÇÜLEMEDİ | 8 / -0,41 [-3,76; +3,40] / ÖLÇÜLEMEDİ |

### HAFTALIK — KODUN SEÇTİĞİ BÖLGELER (ANA ÖRNEK, KAPILI)

| hücre | rol | n eşli | eşli fark ort [ay kümeli %95] | medyan | ort sıra | +%5 payı / eşli hedef payı | +%10 payı / eşli | slot yüzdeliği | güç | hüküm (neden) |
|---|---|---|---|---|---|---|---|---|---|---|
| ABD|d1619 | KARAR | 13 | -3,11 [-9,17; +1,66] | -3,72 | 0,399 | +69,2 / -7,4 | +61,5 / +6,2 | 0,23 | 0,06 | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| ABD|d2022 | KARAR | 8 | +5,49 [-10,49; +27,47] | -0,70 | 0,517 | +75,0 / +11,2 | +62,5 / +17,7 | 0,71 | 0,03 | ÖLÇÜLEMEDİ (n < 30; boot alt <= 0; slot <= %90) |
| AVR|d1619 | KARAR | 3 | +3,16 [-4,36; +6,92] | +2,27 | 0,595 | +33,3 / -9,7 | +33,3 / +8,8 | 0,74 | 0,05 | ÖLÇÜLEMEDİ (n < 30; boot alt <= 0; slot <= %90) |
| AVR|d2022 | KARAR | 1 | -12,75 [-12,75; -12,75] | -12,75 | 0,133 | +100,0 / +33,3 | +100,0 / +60,0 | 0,14 | 0,04 | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| BIST|d1619 | BİLGİ | 7 | -12,97 [-27,69; +2,20] | -18,32 | 0,407 | +80,0 / -10,8 | +70,0 / -8,0 | 0,24 | 0,04 | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| BIST|d2022 | BİLGİ | 10 | -6,45 [-22,79; +16,75] | -9,68 | 0,455 | +90,9 / -6,2 | +90,9 / -0,9 | 0,35 | 0,03 | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| ABD|o16 | BİLGİ | 70 | -1,81 [-5,51; +1,91] | -0,47 | 0,486 | +73,2 / -5,7 | +52,1 / -5,3 | 0,46 | 0,19 | ÖLÇÜLEMEDİ (FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| AVR|o16 | BİLGİ | 10 | +0,42 [-4,92; +6,10] | -1,28 | 0,470 | +80,0 / +5,5 | +40,0 / -17,0 | 0,55 | 0,07 | ÖLÇÜLEMEDİ (n < 30; boot alt <= 0; SIRA <= 0,50; slot <= %90) |
| BIST|o16 | BİLGİ | 0 | - [-; -] | - | - | - / - | - / - | - | - | ÖLÇÜLEMEDİ (n < 30; FARK <= 0; boot alt <= 0; SIRA <= 0,50; slot <= %90) |

GENEL (haftalik, ANA): **ÖLÇÜLEMEDİ**; ölçülemeyen karar hücreleri: ABD|d1619, ABD|d2022, AVR|d1619, AVR|d2022. DUYARLILIK (hepsi dahil): ÖLÇÜLEMEDİ.

| hepsi birlikte | n eşli | n ölçülen | R15 ort / medyan | eşli fark ort [ay kümeli %95] | eşinden iyi payı | +%5 / eşli hedef | slot yüzdeliği | pazar |
|---|---|---|---|---|---|---|---|---|
| KAPILI | 122 | 127 | +4,51 / +1,71 | -2,28 [-5,61; +1,06] | 0,434 | +74,8 / -4,0 | 0,07 | {"ABD": 91, "BIST": 17, "AVR": 14} |
| KAPISIZ | 1088 | 1147 | +5,81 / +2,60 | -1,25 [-3,66; +1,10] | 0,434 | +77,2 / -2,4 | 0,10 | {"ABD": 839, "BIST": 146, "AVR": 103} |
| KAPILI_DUY | 136 | 141 | +6,38 / +1,71 | -2,08 [-5,43; +1,28] | 0,426 | +75,2 / -4,1 | 0,24 | {"ABD": 100, "BIST": 22, "AVR": 14} |
| KAPISIZ_DUY | 1131 | 1190 | +5,65 / +2,56 | -1,52 [-3,91; +0,73] | 0,433 | +77,1 / -2,7 | 0,01 | {"ABD": 876, "BIST": 148, "AVR": 107} |

| KAPI ETKİSİ (KAPILI - KAPISIZ, ANA) | n KAPILI / KAPISIZ | eşli fark KAPILI / KAPISIZ | fark farkı [ay kümeli %95] | p (tabakalı perm, iki yönlü) | eşinden iyi KAPILI / KAPISIZ |
|---|---|---|---|---|---|
| tum | 122 / 1088 | -2,28 / -1,25 | -1,03 [-5,37; +3,17] | 0,6749 | 0,434 / 0,434 |
| karar_birlikte | 25 / 486 | +0,01 / -0,37 | +0,38 [-7,23; +8,84] | 0,9100 | 0,440 / 0,455 |
| ABD|d1619 | 13 / 143 | -3,11 / -3,59 | +0,49 [-6,38; +6,64] | 0,9296 | 0,385 / 0,448 |
| ABD|d2022 | 8 / 288 | +5,49 / +1,19 | +4,30 [-13,66; +30,01] | 0,6115 | 0,500 / 0,462 |
| AVR|d1619 | 3 / 23 | +3,16 / +0,37 | +2,79 [-11,69; +11,83] | 0,8390 | 0,667 / 0,391 |
| AVR|d2022 | 1 / 32 | - / - | - [-; -] | - | - / - |

| KAPISIZ (bilgi) / DUYARLILIK KAPILI hücreleri | KAPISIZ n / fark / hüküm | KAPILI hepsi dahil n / fark [%95] / hüküm |
|---|---|---|
| ABD|d1619 | 143 / -3,59 / ÖLÇÜLEMEDİ | 14 / -2,27 [-7,60; +1,85] / ÖLÇÜLEMEDİ |
| ABD|d2022 | 288 / +1,19 / ÖLÇÜLEMEDİ | 8 / +5,49 [-10,13; +27,18] / ÖLÇÜLEMEDİ |
| AVR|d1619 | 23 / +0,37 / ÖLÇÜLEMEDİ | 3 / +3,16 [-4,36; +6,92] / ÖLÇÜLEMEDİ |
| AVR|d2022 | 32 / -0,58 / ÖLÇÜLEMEDİ | 1 / -12,75 [-12,75; -12,75] / ÖLÇÜLEMEDİ |

BH (q 0,10; bilgi): gunluk|KAPILI|ABD|d1619: p 0,9232, p_BH 1,0000; gunluk|KAPILI|ABD|d2022: p 0,4145, p_BH 1,0000; gunluk|KAPILI|AVR|d1619: p 0,9684, p_BH 1,0000; gunluk|KAPILI|AVR|d2022: p 0,3193, p_BH 1,0000; haftalik|KAPILI|ABD|d1619: p 0,8679, p_BH 1,0000; haftalik|KAPILI|ABD|d2022: p 0,3036, p_BH 1,0000; haftalik|KAPILI|AVR|d1619: p 0,5013, p_BH 1,0000; haftalik|KAPILI|AVR|d2022: p 1,0000, p_BH 1,0000

## KONTROL LİSTESİ

Ön kayıttaki tablo (14 madde; IZ_KARNE.ik_kontrol_kapisi geçti) aynen geçerli. Denetimde yeniden okundu: K1 eş + KAPISIZ kontrol + 200 eşli portföy uygulandı; K2 ORAN yalnız t'ye kadar (HK assert), giriş t + 1 açılış, veri <= 2022-12-31 (assert + KASA kapısı geçti); K4 havuz zaten tekil (15 bar kuralı 0 olay attı; havuzda aynı hissede en küçük ara 21 bar); K7 hayatta kalma yanlılığı yazıldı; K8 n < 30 hücreler ÖLÇÜLEMEDİ; K9 ön kayıt commit 536419b6c5dc71b812baf023a6139d53f578df30 2026-11-26T17:01:58+00:00 getirilerden önce, kos ön kayıt sha + SAYIM_SHA kapısından geçti; K11 iki hücre bağımsız üretildi; K12 başlık 'KODUN SEÇTİĞİ BÖLGELER', 'kalıbın sonucu' denmedi; K13 yasak dosyalara dokunulmadı, yalnız kendi yolları commit; K14 uygulanmaz. HAYIR olması gereken EVET bulunmadı.

## HATA

- (kod, etkisiz) Getirisiz sayımın 'beklenen' metni ilk taslakta n < 30 hücreler için de 'TUTAR olmazsa' diyordu (n < 30 hücre TUTAR olamaz); ön kayıttan ÖNCE düzeltildi; sayılara etkisi yok.
- Sonucu değiştiren hesap / veri / geleceğe bakma hatası bulunmadı.
- Not (hata değil, sınır): hariç listesinin 205 bölgesinden 60'ı v5M havuzunda yok (eski taramaların bölgeleri; tam eşleşme 142, yakın 15 olay hariç tutuldu); günlük güç cetvel2 eğrisi (DS olaylarının yayılımı) ile plasebo eğrisi farklı güç veriyor (ABD 2016-19: 0,26 / 0,49), ikisi de 0,80'in altında.
- Not (süreç): aynı çalışma ağacında başka alt ajan commit'leri (EK 25 iş tanımı) araya girdi; yalnız kendi yollarım commit edildi.

## SAPMA

Yok. Eşik, hücre, ölçü ve hüküm kuralı ön kayıttaki gibi uygulandı. İş tanımına göre yorum gerektiren üç nokta ön kayıtta (ölçümden önce) tanımlandı: hariç tutmaya 'aynı hisse, bölge sonu <= 15 bar' yakınlığı eklendi (sonrası örtüşür; etkisi günlük KAPILI 1, haftalık 0 olay); haftalık güç plasebo eğrisi; KAPI ETKİSİ tabakalı permütasyon.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç (MUM_IZI EK 24): 'KODUN SEÇTİĞİ BÖLGELER (aday kuralı v5M + mum boyu kapısı ORAN <= 0,70; göz onayı yok), 15 mum: günlük n 231 eşli fark -0,85 puan [-2,31; +0,60], haftalık n 122 -2,28 [-5,61; +1,06]; karar hücreleri ABD / AVR x 2016-19 / 2020-22 hepsi ÖLÇÜLEMEDİ (güç < 0,80 / n < 30); kapı etkisi günlük -0,88 (p 0,24), haftalık -1,03 (p 0,67); KAPISIZ aday kuralı günlük ABD / AVR 2016-19 ve ABD 2020-22 TUTMADI (güç >= 0,80). Karar: ÖLÇÜLEMEDİ (günlük, haftalık); kasa açılmaz; evren yukarı yanlı.'
- IK_ILERI: 'MUM_IZI EK 24 kodun seçtiği bölgeler: ÖLÇÜLEMEDİ (güç); aynı komut (MUM_IZI_HAVUZ kos), aynı eşik, daha geniş evrenle (batanlar dahil ABD + AVR) ya da kasa kuralı izin verdiğinde 2023-26 verisiyle yeniden; günlük güç 0,80 için gereken eşli n (cetvel2 eğrisi): ABD 2016-19 255, ABD 2020-22 339, AVR 2016-19 162, AVR 2020-22 208 (bugün 63 / 75 / 11 / 6).'
- IK_GOREV: 'EK 24 ölçüm: MUM_IZI_HAVUZ.py + test (ae2a235), ön kayıt (536419b), sonuç (bu commit).'
