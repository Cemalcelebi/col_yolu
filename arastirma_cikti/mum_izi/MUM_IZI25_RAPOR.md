# MUM_IZI25 RAPOR — KODUN SEÇTİĞİ BÖLGELER: rastgele gün tabanı (mutlak kârlılık), zamanlama / seçim ayrımı, piyasa tahmini (takvim zamanı)

Tarih: 26 Kasım 2026. İş tanımı MUM_IZI25_IS_TANIMI.md (1, 2, 2b, 3. bölüm) + MUM_IZI23_EK_KURAL.md GÜNCELLEME. Kod MUM_IZI_HAVUZ.py (commit 7f3e5d5; EK 25 komutları sayim25 / onkayit25 / kos25 / rapor25), ön kayıt MUM_IZI25_ON_KAYIT.md (commit d8b9470fceee8d98366f1fa75b7493f09ac75bb8 2026-11-26T17:31:33+00:00; getirilerden önce, push'lu), sonuç mum_izi25_sonuc.json, satırlar mum_izi25_olay.csv.gz (sha 112f3479c25ec2c5…; olay satırları + 70.000 T2 çekimi + 5.274 takvim günü).
Okuma sınırı: bölgeler KODUN seçtiği bölgelerdir (aday kuralı v5M + mum boyu kapısı), kalıbın kendisi değildir. Evren bugün yaşayan hisseler: olay da taban da yukarı yanlı. Dönem içi piyasa yönü tabanda da var (T1 / T2 / PİYASA aynı dönemden). Veri <= 2022-12-31; kasa açılmadı. Farklar yüzde puan; aralıklar ay kümeli bootstrap %95 (10.000).

Tanımlar (kısa): T1 = aynı hissenin aynı dönemde rastgele 200 günü (bilinen bölgelere <= 14 bar yakın günler hariç, aynı m, aynı stop / giriş / 15 mum); T2 = aynı pazar / dönem / zaman diliminde rastgele 5.000 (hisse, gün), stop 20 bar; PİYASA(t) = aynı giriş gününde pazarın bütün hisselerinin (olaylılar hariç) aynı pencere getirisi. TOPLAM FARK = R15 - T1; ZAMANLAMA = PİYASA(t) - T2; SEÇİM = R15 - PİYASA(t) (R15 - T2 = ZAMANLAMA + SEÇİM, olay başına denetlendi).

## SONUÇ

- KODUN SEÇTİĞİ BÖLGELER (KAPILI ana örnek), GÜNLÜK, hepsi birlikte: n 256, 61 farklı ay, en kalabalık 3 ay %21. R15 ort -0,13 % / medyan -0,63 %; aynı hissenin rastgele günü (T1) +1,86 %; herhangi bölge (T2) +2,20 %; aynı günün piyasası +1,94 %. TOPLAM FARK (T1) -1,99 puan [-4,03; -0,15]: okuma kuralına göre RASTGELE GÜNDEN KÖTÜ. ZAMANLAMA -0,27 [-1,61; +1,18]: AYRIŞMIYOR. SEÇİM -2,06 [-3,69; -0,54]: SEÇİM -. +%5 stop'tan önce: olay %50,4, T1 %53,6, T2 %54,5.
- Bu sayıların anlamı: kodun seçtiği günlük bölgeler, aynı hissenin rastgele bir gününden 15 mumda yaklaşık 2 puan geride kaldı. Bölgeler piyasanın daha çok yükseldiği zamanlara denk gelmedi (zamanlama yaklaşık sıfır); geri kalış hisse tarafında. EK 24'ün eşli farkı (aynı gün aynı kova) -0,85 idi; kovasız seçim farkı -2,06: farkın bir kısmını kova (momentum / oynaklık / likidite) açıklıyor.
- Karar hücreleri (günlük): ABD 2016-19 n 64 (25 ay, ilk 3 ay %42): TOPLAM -2,09 [-4,88; +1,42], ZAMANLAMA -0,90 [-2,45; +0,73], SEÇİM -1,66 [-3,82; +1,18], +%5 %32,8 / %44,0 / %45,4: AYRIŞMIYOR. ABD 2020-22 n 75 (17 ay, ilk 3 ay %48): TOPLAM -0,85 [-6,74; +3,13], ZAMANLAMA -0,50 [-3,10; +1,89], SEÇİM -0,19 [-4,41; +2,78], +%5 %56,0 / %53,5 / %54,6: AYRIŞMIYOR. AVR 2016-19 n 11, AVR 2020-22 n 6: ÖLÇÜLEMEDİ. İki ABD hücresi de 'az sayıda döneme dayanıyor' (ilk 3 ay payı > %30).
- HAFTALIK, hepsi birlikte: n 127, 79 ay, ilk 3 ay %12. R15 +4,51 / +1,71 %; T1 +7,15; T2 +7,27; PİYASA +7,59. TOPLAM FARK -2,64 [-7,97; +2,39]: AYRIŞMIYOR. ZAMANLAMA +0,32 [-2,88; +3,87]: AYRIŞMIYOR. SEÇİM -3,08 [-6,17; -0,01]: SEÇİM -. +%5: %74,8 / %73,4 / %73,5. Haftalık karar hücreleri n 13 / 8 / 3 / 1: ÖLÇÜLEMEDİ. 2016 öncesi ABD (bilgi) n 71: TOPLAM -5,02 [-9,76; -0,38].
- Haftalıkta R15 artı (+4,5 %) görünür, ama aynı hissenin rastgele 15 haftası daha çok (+7,2 %) kazandırmış: 'mutlak artı' bu bölgelere özgü değil, dönemin ve evrenin (bugün yaşayanlar) genel yükselişi.
- KAPISIZ kontrol (aynı aday kuralı, ORAN > 0,70): günlük n 4.245 (83 ay) R15 +1,26 %, TOPLAM +0,09 [-0,93; +1,05], ZAMANLAMA -0,08 [-1,41; +1,16], SEÇİM -0,08 [-0,60; +0,42]: hepsi AYRIŞMIYOR; +%5 %53,4 / %48,3 / %50,5. Haftalık n 1.147: TOPLAM +1,06 [-3,41; +5,38], ZAMANLAMA +2,48 [-1,83; +6,46], SEÇİM -3,54 [-6,36; -0,93]. Kapı ne zamanlama ne kârlılık katıyor; günlükte KAPILI (-1,99) KAPISIZ'dan (+0,09) kötü yönde (bu fark ön kayıtta test olarak yazılmadı; bilgi).
- Duyarlılık (hariç bölgeler dahil, KAPILI hepsi): günlük n 305, TOPLAM -2,04 [-3,86; -0,40] (RASTGELE GÜNDEN KÖTÜ), ZAMANLAMA -0,28, SEÇİM -2,03; haftalık n 141 TOPLAM -0,88 [-6,33; +4,62]. Yön aynı.
- GÖZ ÖLÇÜMÜ (set 6-9, zaman dilimleri birlikte; Cemal'in sınıfı): BENZİYOR n 26 (20 ay): R15 +7,58 / +0,84 %, T1 +4,54, TOPLAM +3,04 [-7,68; +15,56]: AYRIŞMIYOR (ÖRNEKLEM YETERSİZ); eşli okuma -4,25 [-8,67; -0,39] SONRASI KÖTÜ. KISMEN n 24 (23 ay): R15 +3,23 / -3,53 %, TOPLAM -0,06 [-8,63; +13,19]: AYRIŞMIYOR (ÖY); eşli +1,30 GÖSTERİLEMEDİ. BENZEMİYOR n 25 (17 ay): R15 -2,21 / -0,27 %, TOPLAM -3,08 [-9,11; +1,01]: AYRIŞMIYOR (ÖY); eşli -3,58 GÖSTERİLEMEDİ.
- Kapı havuzu (set 7-9): BENZİYOR n 22 TOPLAM +2,70 [-9,75; +16,90]; KISMEN n 17 +2,27 [-8,74; +20,40]; BENZEMİYOR n 19 +0,61 [-2,22; +2,59]; hepsi AYRIŞMIYOR (ÖY). Günlükte BENZİYOR set 6-9 n 19: TOPLAM -5,38 [-10,17; -1,02] (RASTGELE GÜNDEN KÖTÜ, ÖY); BENZİYOR'un artı ortalaması haftalık 7 bölgeden geliyor (R15 +33 %, 5 ay; 2022-08 BIST üç bölge).
- KISMEN KABUL KURALI: KISMEN 'MUTLAK KÂRLI' değil (aralık sıfırı içeriyor) -> KISMEN KABUL SAYILMAZ (set 7-9'da da aynı); n 24 < 30: ÖRNEKLEM YETERSİZ. Eşli okuma da GÖSTERİLEMEDİ: iki okuma ayrışmıyor. BENZİYOR da rastgele güne göre 'mutlak kârlı' değil.
- PİYASA TAHMİNİ (2b; ABD, KAPILI ana sayı): 2016-19 SAYI = 0: 813 gün, PİYASA15 +1,23 / +1,38 %, artı %69; SAYI 1-2: 166 gün +0,72 / +0,76 %, %63; SAYI >= 3: 27 gün +0,33 / +0,89 %, %59; (>= 1) - (= 0) -0,56 [-1,60; +0,49], (>= 3) - (= 0) -0,90 [-3,81; +2,26]. 2020-22: 560 / 144 / 38 gün; +1,21 / -0,41 / +0,95 %; artı %59 / %46 / %50; (>= 1) - (= 0) -1,34 [-3,87; +1,30], (>= 3) -0,27 [-3,95; +2,86]. Birlikte: (>= 1) - (= 0) -0,94 [-2,19; +0,31]. Okuma: GÖSTERİLEMEDİ (iki dönemde de yön eksi, aralık sıfırı içeriyor).
- AVR (KAPILI): 2016-19 974 / 51 / 0 gün, +0,76 / +0,61 %, fark -0,15 [-2,06; +1,51]; 2020-22 729 / 30 / 0, +0,35 / -2,01 %, fark -2,36 [-4,95; +0,00]; SAYI >= 3 günü yok: GÖSTERİLEMEDİ. KAPISIZ sayısıyla ABD -0,91 [-1,91; +0,38] / +0,49 [-3,90; +3,10], AVR -0,40 / -0,36: GÖSTERİLEMEDİ. BIST (bilgi) +0,90 / +0,66: GÖSTERİLEMEDİ.
- Basit bilgi satırı (pazar son 20 günde %5'ten fazla düşmüş): ABD 2016-19 74 gün PİYASA15 +3,71 / +2,27 %, artı %74, öteki günlerden +2,79 [+0,04; +5,77]; 2020-22 132 gün -0,09 / +1,05 %, -1,19 [-4,04; +1,71]. AVR +1,20 [-0,80; +4,61] / +0,56 [-2,01; +3,35]. Yapılı günlerin yalnız %2'si (ABD; AVR ve BIST %0) böyle bir düşüşün ardından geliyor: bu bölgeler pazar düşüşlerinden sonra değil, sakin pazarda görülüyor; 'düşüş sonrası toparlanma' bilgisini taşımıyorlar.
- Genel okuma: kodun seçtiği bölgeler rastgele günden mutlak olarak kârlı değil (günlükte biraz kötü), görüldükleri zaman piyasa daha çok yükselmiyor ve bölge sayısı pazarın sonraki 15 gününü öncelemiyor. Cemal'in itirazının sorduğu 'eşli fark zamanlamayı siliyor mu' sorusunun yanıtı bu verilerde: zamanlama katkısı yaklaşık sıfır; eşli farkın gizlediği bir zamanlama kazancı görünmedi. Kasa açılmaz; iz değil, ölçüm 'kodun seçtiği bölgeler' ile sınırlı.

## Yeniden üretim

- Olay csv'sinden bağımsız kısa kodla (pandas; kendi ay kümeli bootstrap'ım, tohum 1, B 4.000; T2 = T2_CEKIM satırlarından hücre ortalaması): günlük KAPILI ANA hepsi n 256, 61 ay, R15 -0,128 %, T1 +1,863 %, T2 +2,203 %, PİYASA +1,936 %, TOPLAM -1,99 [-4,04; -0,17] (rapor [-4,03; -0,15]), SEÇİM -2,06 [-3,68; -0,58], ZAMANLAMA -0,27, +%5 %50,4 / %53,6: aynı. Göz set 6-9 KISMEN n 24 TOPLAM -0,06 [-8,6; +12,7]: aynı. 2b ABD KAPILI 2016-19: 813 / 166 / 27 gün, PİYASA15 +1,232 / (>= 1) +0,670, fark -0,562: aynı.
- T1 makinesinden bağımsız: iki olayda (günlük ABD ACCO 2019-04-17; haftalık AVR EDEN.PA 2018-01-19) uygun günler gz_olc_bir döngüsüyle tek tek yeniden bulundu (862 / 180 gün, csv ile aynı) ve aynı tohumla çekilen 200 / 180 günün R15 ortalaması GZ.gz_olc_bir ile +1,2614 % / +8,3995 %: csv ile aynı.
- Mekanik denetimler (kodda DUR): EK 24 / EK 23 satırlarında t = takvim, giriş / 15. mum tarihi, E0, stop (getirisiz aşama) ve R15 / d5 / d10 (hesap) hv25_olc_dizi ile birebir; R15 - T2 = ZAMANLAMA + SEÇİM; SAYIM25_SHA kos'ta yeniden hesaplanıp ön kayıtla aynı çıktı; ön kayıt sha'ları, commit ve temiz ağaç kapısı geçti; KASA kapısı geçti.
- Testler: python test_mum_izi_havuz.py (22 test geçti; 10'u EK 25: 15 bar yakınlık dışlaması, dönem sınırı, pencere kesiği, rastgele gün stop'u, gz_olc_bir eşitliği günlük + haftalık, tohum 2511, PİYASA(t)'de olaylı hisse dışlaması, SAYI(g) geleceğe bakmaz, ay kümeli bootstrap + T2 belirsizliği, EK 24 fonksiyon kaynakları / eşikleri / olay csv sha'sı değişmedi, sentetik uçtan uca).

## Tablolar

### KAPILI — GUNLUK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 256 | 61 | 0,21 | -0,13 / -0,63 | +1,86 | +2,20 | +1,94 | -1,99 [-4,03; -0,15] | -2,33 [-4,44; -0,37] | -0,27 [-1,61; +1,18] | -2,06 [-3,69; -0,54] | -0,85 (231) | +50,4 / +53,6 / +54,5 | RASTGELE GÜNDEN KÖTÜ; AYRIŞMIYOR; SEÇİM - |
| ABD|d1619 | 64 | 25 | 0,42 | -1,31 / -1,94 | +0,78 | +1,25 | +0,35 | -2,09 [-4,88; +1,42] | -2,56 [-5,56; +0,97] | -0,90 [-2,45; +0,73] | -1,66 [-3,82; +1,18] | -1,71 (63) | +32,8 / +44,0 / +45,4 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| ABD|d2022 | 75 | 17 | 0,48 | +0,14 / +0,67 | +0,99 | +0,82 | +0,32 | -0,85 [-6,74; +3,13] | -0,69 [-6,65; +3,74] | -0,50 [-3,10; +1,89] | -0,19 [-4,41; +2,78] | +0,46 (75) | +56,0 / +53,5 / +54,6 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| AVR|d1619 | 11 | 9 | 0,45 | -1,41 / +1,38 | +0,60 | +0,70 | +1,24 | -2,01 [-6,90; +1,61] | -2,11 [-7,22; +1,63] | +0,54 [-1,27; +1,84] | -2,64 [-6,14; -0,01] | -3,00 (11) | +36,4 / +35,0 / +34,6 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d2022 | 6 | 6 | 0,50 | +0,67 / -0,95 | +0,62 | -0,24 | -2,56 | +0,05 [-3,18; +3,89] | +0,91 [-2,53; +5,08] | -2,32 [-5,06; +0,25] | +3,23 [-0,23; +6,44] | +1,18 (6) | +33,3 / +37,9 / +41,7 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d1619 | 39 | 22 | 0,28 | -0,71 / -1,04 | +1,63 | +1,65 | +3,20 | -2,34 [-6,65; +1,38] | -2,36 [-6,11; +1,06] | +1,55 [-1,25; +4,49] | -3,91 [-7,42; -0,56] | -2,05 (31) | +61,5 / +55,5 / +55,9 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |
| BIST|d2022 | 61 | 16 | 0,43 | +1,31 / -1,59 | +4,57 | +5,76 | +5,34 | -3,26 [-7,93; +1,16] | -4,45 [-9,61; +0,64] | -0,42 [-4,96; +4,20] | -4,03 [-6,55; -1,68] | -0,76 (45) | +59,0 / +67,6 / +67,7 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM -; az sayıda döneme dayanıyor |
| ABD|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| AVR|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPILI — HAFTALIK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 127 | 79 | 0,12 | +4,51 / +1,71 | +7,15 | +7,27 | +7,59 | -2,64 [-7,97; +2,39] | -2,76 [-7,13; +1,52] | +0,32 [-2,88; +3,87] | -3,08 [-6,17; -0,01] | -2,28 (122) | +74,8 / +73,4 / +73,5 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |
| ABD|d1619 | 13 | 11 | 0,38 | +1,57 / +1,77 | +5,04 | +4,71 | +4,24 | -3,48 [-10,67; +1,90] | -3,14 [-10,97; +3,34] | -0,46 [-4,84; +3,98] | -2,68 [-9,88; +3,11] | -3,11 (13) | +69,2 / +73,5 / +72,8 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| ABD|d2022 | 8 | 7 | 0,50 | +1,38 / -9,80 | +17,80 | +5,77 | -3,90 | -16,42 [-56,27; +27,27] | -4,39 [-28,21; +26,35] | -9,66 [-18,70; +0,18] | +5,27 [-14,22; +33,16] | +5,49 (8) | +75,0 / +75,0 / +72,8 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d1619 | 3 | 2 | 1,00 | +4,63 / +4,21 | +4,57 | +2,88 | +2,30 | +0,06 [-0,38; +0,94] | +1,75 [-2,52; +4,66] | -0,58 [-3,65; +4,04] | +2,33 [-3,90; +5,44] | +3,16 (3) | +33,3 / +65,2 / +67,9 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d2022 | 1 | 1 | 1,00 | -8,73 / -8,73 | +3,29 | +1,58 | +0,85 | -12,02 [-12,02; -12,02] | -10,31 [-13,59; -6,98] | -0,74 [-4,01; +2,60] | -9,57 [-9,57; -9,57] | -12,75 (1) | +100,0 / +72,6 / +67,0 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d1619 | 10 | 8 | 0,50 | +14,34 / +13,15 | +6,89 | +9,87 | +26,35 | +7,45 [-19,65; +26,51] | +4,47 [-22,61; +24,15] | +16,48 [-0,42; +29,76] | -12,01 [-24,85; -3,11] | -12,97 (7) | +80,0 / +76,2 / +76,3 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d2022 | 11 | 7 | 0,64 | +32,41 / +18,42 | +22,92 | +30,49 | +38,80 | +9,50 [-16,46; +36,31] | +1,92 [-24,26; +23,09] | +8,32 [-16,06; +28,26] | -6,39 [-15,39; +3,25] | -6,45 (10) | +90,9 / +77,8 / +84,9 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| ABD|o16 | 71 | 43 | 0,20 | -0,19 / -0,69 | +4,83 | +4,65 | +2,73 | -5,02 [-9,76; -0,38] | -4,84 [-9,82; -0,02] | -1,92 [-4,81; +1,00] | -2,92 [-7,00; +1,00] | -1,81 (70) | +73,2 / +73,2 / +72,5 | RASTGELE GÜNDEN KÖTÜ; AYRIŞMIYOR; AYRIŞMIYOR |
| AVR|o16 | 10 | 10 | 0,30 | +4,99 / +1,66 | +1,91 | +4,12 | +4,74 | +3,07 [-2,69; +9,87] | +0,87 [-4,66; +7,37] | +0,62 [-3,02; +4,32] | +0,25 [-4,84; +5,44] | +0,42 (10) | +80,0 / +67,6 / +70,0 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPILI — BIRLIKTE (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 383 | 115 | 0,14 | +1,41 / -0,32 | +3,62 | +3,88 | +3,81 | -2,21 [-4,50; +0,03] | -2,47 [-4,49; -0,49] | -0,07 [-1,55; +1,54] | -2,40 [-3,97; -0,92] | -1,34 (353) | +58,5 / +60,2 / +60,8 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |

### KAPISIZ — GUNLUK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 4245 | 83 | 0,12 | +1,26 / +0,91 | +1,17 | +1,41 | +1,34 | +0,09 [-0,93; +1,05] | -0,15 [-1,43; +1,04] | -0,08 [-1,41; +1,16] | -0,08 [-0,60; +0,42] | +0,02 (4056) | +53,4 / +48,3 / +50,5 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| ABD|d1619 | 1626 | 48 | 0,18 | +0,84 / +1,10 | +1,06 | +1,25 | +1,16 | -0,23 [-1,55; +0,89] | -0,42 [-2,05; +0,98] | -0,09 [-1,51; +1,18] | -0,33 [-1,06; +0,34] | -0,13 (1616) | +47,1 / +43,2 / +45,4 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| ABD|d2022 | 1484 | 35 | 0,28 | +0,79 / +0,58 | +0,65 | +0,82 | +0,53 | +0,14 [-1,97; +2,02] | -0,04 [-2,79; +2,62] | -0,29 [-3,22; +2,58] | +0,25 [-0,88; +1,26] | +0,18 (1468) | +57,0 / +51,0 / +54,6 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| AVR|d1619 | 260 | 45 | 0,23 | +0,12 / +0,52 | +0,61 | +0,70 | +0,64 | -0,49 [-1,40; +0,36] | -0,58 [-1,66; +0,42] | -0,06 [-0,96; +0,77] | -0,53 [-1,19; +0,17] | -0,44 (236) | +33,8 / +35,0 / +34,6 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| AVR|d2022 | 162 | 32 | 0,23 | -0,79 / -0,27 | +0,21 | -0,24 | -0,45 | -1,00 [-2,80; +0,69] | -0,54 [-2,72; +1,64] | -0,21 [-2,27; +1,92] | -0,33 [-1,79; +0,88] | -0,24 (148) | +43,8 / +42,3 / +41,7 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| BIST|d1619 | 370 | 46 | 0,22 | +2,00 / +0,58 | +1,32 | +1,65 | +2,29 | +0,68 [-2,32; +4,01] | +0,35 [-2,96; +3,81] | +0,65 [-1,51; +2,83] | -0,29 [-1,81; +1,35] | +0,43 (298) | +65,1 / +54,4 / +55,9 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| BIST|d2022 | 343 | 33 | 0,24 | +6,34 / +5,02 | +4,65 | +5,76 | +5,97 | +1,69 [-1,68; +4,60] | +0,58 [-3,50; +4,30] | +0,21 [-3,26; +3,36] | +0,37 [-1,22; +1,79] | +0,20 (290) | +74,6 / +67,2 / +67,7 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| ABD|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| AVR|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPISIZ — HAFTALIK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 1147 | 193 | 0,21 | +5,81 / +2,60 | +4,76 | +6,87 | +9,35 | +1,06 [-3,41; +5,38] | -1,05 [-5,68; +3,73] | +2,48 [-1,83; +6,46] | -3,54 [-6,36; -0,93] | -1,25 (1088) | +77,2 / +72,4 / +73,3 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |
| ABD|d1619 | 143 | 39 | 0,20 | -2,79 / -3,35 | +2,89 | +4,71 | +0,84 | -5,68 [-9,50; -1,53] | -7,49 [-12,39; -2,40] | -3,87 [-8,68; +0,73] | -3,62 [-6,73; -0,28] | -3,59 (143) | +70,6 / +70,8 / +72,8 | RASTGELE GÜNDEN KÖTÜ; AYRIŞMIYOR; SEÇİM - |
| ABD|d2022 | 288 | 27 | 0,59 | +11,68 / +8,42 | +3,06 | +5,77 | +13,46 | +8,62 [-5,56; +17,26] | +5,91 [-8,85; +16,46] | +7,69 [-3,44; +15,97] | -1,78 [-8,79; +3,92] | +1,19 (288) | +85,8 / +71,7 / +72,8 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| AVR|d1619 | 25 | 18 | 0,32 | +2,03 / +3,17 | +1,11 | +2,88 | +1,39 | +0,92 [-6,45; +10,24] | -0,85 [-8,58; +7,82] | -1,49 [-5,03; +1,96] | +0,64 [-6,87; +10,07] | +0,37 (23) | +68,0 / +65,0 / +67,9 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d2022 | 41 | 16 | 0,63 | +5,94 / +6,25 | +1,11 | +1,58 | +6,15 | +4,83 [-3,86; +9,19] | +4,35 [-4,70; +9,45] | +4,57 [-1,60; +9,97] | -0,21 [-6,45; +3,63] | -0,58 (32) | +75,6 / +62,0 / +67,0 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| BIST|d1619 | 102 | 31 | 0,32 | +13,33 / +6,01 | +6,08 | +9,87 | +20,51 | +7,26 [-6,81; +18,42] | +3,46 [-10,35; +14,70] | +10,63 [-3,21; +21,91] | -7,17 [-11,61; -1,17] | -4,71 (85) | +85,3 / +75,0 / +76,3 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM -; az sayıda döneme dayanıyor |
| BIST|d2022 | 73 | 20 | 0,56 | +18,38 / +9,36 | +20,37 | +30,49 | +38,71 | -2,00 [-14,08; +9,29] | -12,11 [-26,69; +3,21] | +8,23 [-15,77; +22,90] | -20,34 [-29,62; +0,45] | -6,48 (61) | +87,7 / +82,5 / +84,9 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| ABD|o16 | 413 | 110 | 0,19 | +1,39 / +1,00 | +4,40 | +4,65 | +3,09 | -3,01 [-6,84; +0,53] | -3,26 [-7,39; +0,62] | -1,56 [-5,27; +1,99] | -1,70 [-4,15; +0,54] | -0,82 (408) | +71,7 / +72,9 / +72,5 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| AVR|o16 | 62 | 40 | 0,23 | +2,17 / +2,94 | +2,64 | +4,12 | +4,04 | -0,47 [-4,16; +2,93] | -1,94 [-5,89; +1,67] | -0,08 [-4,32; +3,99] | -1,86 [-5,49; +1,22] | -0,93 (48) | +69,4 / +69,6 / +70,0 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPISIZ — BIRLIKTE (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 5392 | 201 | 0,10 | +2,23 / +1,09 | +1,93 | +2,57 | +3,04 | +0,30 [-1,00; +1,65] | -0,34 [-1,80; +1,08] | +0,47 [-0,96; +1,90] | -0,81 [-1,57; -0,16] | -0,24 (5144) | +58,5 / +53,4 / +55,4 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |

### KAPILI_DUY — GUNLUK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 305 | 63 | 0,22 | -0,17 / -0,61 | +1,87 | +2,14 | +1,86 | -2,04 [-3,86; -0,40] | -2,32 [-4,30; -0,46] | -0,28 [-1,61; +1,13] | -2,03 [-3,47; -0,69] | -0,95 (273) | +49,5 / +53,3 / +54,3 | RASTGELE GÜNDEN KÖTÜ; AYRIŞMIYOR; SEÇİM - |
| ABD|d1619 | 77 | 25 | 0,43 | -1,23 / -1,58 | +0,87 | +1,25 | +0,39 | -2,10 [-4,20; +0,87] | -2,48 [-4,83; +0,57] | -0,87 [-2,27; +0,56] | -1,61 [-3,24; +0,72] | -1,63 (76) | +28,6 / +43,4 / +45,4 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| ABD|d2022 | 97 | 17 | 0,54 | -0,16 / +0,00 | +0,79 | +0,82 | +0,46 | -0,95 [-6,21; +2,16] | -0,98 [-6,54; +2,69] | -0,36 [-2,99; +2,11] | -0,62 [-4,23; +1,72] | +0,02 (96) | +56,7 / +53,3 / +54,6 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR; az sayıda döneme dayanıyor |
| AVR|d1619 | 12 | 9 | 0,50 | -0,92 / +2,14 | +0,67 | +0,70 | +1,29 | -1,59 [-6,81; +1,73] | -1,62 [-7,00; +1,93] | +0,59 [-1,13; +1,80] | -2,22 [-6,02; +0,20] | -2,45 (12) | +33,3 / +36,2 / +34,6 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d2022 | 8 | 8 | 0,38 | -0,10 / -1,51 | +0,53 | -0,24 | -1,35 | -0,63 [-3,02; +2,54] | +0,14 [-2,67; +3,60] | -1,10 [-3,83; +1,78] | +1,25 [-2,32; +4,71] | -0,41 (8) | +25,0 / +34,4 / +41,7 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d1619 | 41 | 24 | 0,27 | -0,54 / -0,86 | +1,68 | +1,65 | +3,02 | -2,22 [-6,17; +1,25] | -2,19 [-5,73; +1,07] | +1,37 [-1,33; +4,26] | -3,56 [-6,87; -0,31] | -1,79 (32) | +63,4 / +55,5 / +55,9 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |
| BIST|d2022 | 70 | 17 | 0,41 | +1,30 / -0,81 | +4,93 | +5,76 | +5,21 | -3,63 [-8,02; +0,48] | -4,46 [-9,34; +0,39] | -0,55 [-4,95; +3,80] | -3,91 [-6,04; -1,85] | -1,00 (49) | +60,0 / +67,9 / +67,7 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM -; az sayıda döneme dayanıyor |
| ABD|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| AVR|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPILI_DUY — HAFTALIK (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 141 | 85 | 0,11 | +6,38 / +1,71 | +7,26 | +7,78 | +8,80 | -0,88 [-6,33; +4,62] | -1,39 [-6,06; +3,37] | +1,03 [-2,93; +5,37] | -2,42 [-5,47; +0,97] | -2,08 (136) | +75,2 / +73,2 / +73,8 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| ABD|d1619 | 14 | 11 | 0,43 | +2,04 / +1,92 | +4,74 | +4,71 | +4,25 | -2,70 [-8,68; +2,01] | -2,67 [-9,67; +3,37] | -0,45 [-4,75; +3,74] | -2,21 [-8,52; +3,20] | -2,27 (14) | +71,4 / +74,0 / +72,8 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| ABD|d2022 | 8 | 7 | 0,50 | +1,38 / -9,80 | +17,80 | +5,77 | -3,90 | -16,42 [-56,69; +27,60] | -4,39 [-28,12; +26,14] | -9,66 [-18,69; +0,05] | +5,27 [-14,22; +32,76] | +5,49 (8) | +75,0 / +75,0 / +72,8 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d1619 | 3 | 2 | 1,00 | +4,63 / +4,21 | +4,57 | +2,88 | +2,30 | +0,06 [-0,38; +0,94] | +1,75 [-2,46; +4,66] | -0,58 [-3,60; +4,10] | +2,33 [-3,90; +5,44] | +3,16 (3) | +33,3 / +65,2 / +67,9 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| AVR|d2022 | 1 | 1 | 1,00 | -8,73 / -8,73 | +3,29 | +1,58 | +0,85 | -12,02 [-12,02; -12,02] | -10,31 [-13,59; -6,98] | -0,74 [-4,01; +2,60] | -9,57 [-9,57; -9,57] | -12,75 (1) | +100,0 / +72,6 / +67,0 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d1619 | 11 | 8 | 0,55 | +15,83 / +20,07 | +9,49 | +9,87 | +28,38 | +6,34 [-19,42; +22,33] | +5,95 [-21,62; +23,84] | +18,51 [-0,01; +31,67] | -12,55 [-24,84; -4,64] | -13,23 (8) | +81,8 / +76,6 / +76,3 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| BIST|d2022 | 15 | 8 | 0,53 | +39,22 / +24,62 | +19,93 | +30,49 | +45,87 | +19,29 [-6,73; +42,02] | +8,73 [-16,17; +28,39] | +15,39 [-10,95; +37,50] | -6,65 [-14,82; +2,76] | -8,09 (14) | +93,3 / +77,4 / +84,9 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; az sayıda döneme dayanıyor |
| ABD|o16 | 79 | 48 | 0,19 | +0,54 / -1,25 | +4,75 | +4,65 | +1,99 | -4,21 [-9,29; +1,31] | -4,10 [-9,45; +1,69] | -2,66 [-5,51; +0,29] | -1,45 [-5,74; +3,16] | -0,99 (78) | +72,2 / +72,7 / +72,5 | AYRIŞMIYOR; AYRIŞMIYOR; AYRIŞMIYOR |
| AVR|o16 | 10 | 10 | 0,30 | +4,99 / +1,66 | +1,91 | +4,12 | +4,74 | +3,07 [-2,69; +10,02] | +0,87 [-4,52; +7,42] | +0,62 [-2,93; +4,29] | +0,25 [-4,76; +5,67] | +0,42 (10) | +80,0 / +67,6 / +70,0 | ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ; ÖLÇÜLEMEDİ |
| BIST|o16 | 0 | - | - | - | - | - | - | - | - | - | - | - | - | - |

### KAPILI_DUY — BIRLIKTE (KODUN SEÇTİĞİ BÖLGELER)

| hücre | n | farklı ay | ilk 3 ay payı | R15 ort / medyan | T1 ort | T2 ort | PİYASA(t) ort | TOPLAM FARK (T1) [%95] | TOPLAM FARK (T2) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | EK 24 eşli fark (n) | +%5: olay / T1 / T2 | okuma (mutlak; zamanlama; seçim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hepsi | 446 | 122 | 0,15 | +1,90 / -0,29 | +3,57 | +3,92 | +4,06 | -1,67 [-3,89; +0,52] | -2,03 [-4,10; +0,00] | +0,13 [-1,47; +1,84] | -2,16 [-3,55; -0,75] | -1,33 (409) | +57,6 / +59,6 / +60,5 | AYRIŞMIYOR; AYRIŞMIYOR; SEÇİM - |

### GÖZ ÖLÇÜMÜ GOZ_6_9 (sınıf = Cemal'in işareti)

| zaman | sınıf | n | farklı ay | R15 ort / medyan | T1 ort | TOPLAM FARK (T1) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | +%5 olay / T1 | okuma (aralık kuralı) | eşli fark (EK 23 kuralı) [%95] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| birlikte | BENZİYOR | 26 | 20 | +7,58 / +0,84 | +4,54 | +3,04 [-7,68; +15,56] | +5,78 [-2,56; +17,24] | -4,24 [-7,69; -0,15] | +61,5 / +59,4 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -4,25 [-8,67; -0,39] SONRASI KÖTÜ (n 23) |
| birlikte | KISMEN | 24 | 23 | +3,23 / -3,53 | +3,29 | -0,06 [-8,63; +13,19] | -0,72 [-4,57; +3,83] | +1,35 [-6,26; +13,10] | +41,7 / +57,3 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +1,30 [-5,78; +12,03] GÖSTERİLEMEDİ (n 21) |
| birlikte | BENZEMİYOR | 25 | 17 | -2,21 / -0,27 | +0,88 | -3,08 [-9,11; +1,01] | -0,65 [-2,74; +1,28] | -3,45 [-8,46; -0,07] | +48,0 / +53,8 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -3,58 [-8,22; +0,39] GÖSTERİLEMEDİ (n 24) |
| gunluk | BENZİYOR | 19 | 16 | -1,77 / -1,58 | +3,61 | -5,38 [-10,17; -1,02] | -0,92 [-3,05; +1,14] | -3,33 [-6,32; -0,27] | +52,6 / +53,8 | RASTGELE GÜNDEN KÖTÜ (ÖRNEKLEM YETERSİZ) | -3,21 [-6,29; -0,03] SONRASI KÖTÜ (n 16) |
| gunluk | KISMEN | 16 | 15 | -2,74 / -3,53 | +1,03 | -3,78 [-8,22; +0,70] | -0,14 [-2,01; +1,77] | -3,90 [-8,06; +0,64] | +25,0 / +51,0 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -3,24 [-7,13; +0,73] GÖSTERİLEMEDİ (n 14) |
| gunluk | BENZEMİYOR | 20 | 13 | -1,07 / +0,12 | +1,19 | -2,26 [-8,82; +1,18] | -1,00 [-3,38; +1,01] | -1,21 [-5,78; +1,23] | +40,0 / +48,9 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -1,55 [-5,21; +1,91] GÖSTERİLEMEDİ (n 19) |
| haftalik | BENZİYOR | 7 | 5 | +32,97 / +23,13 | +7,06 | +25,90 [-4,20; +46,64] | +23,97 [-6,28; +46,16] | -6,72 [-14,95; +8,08] | +85,7 / +74,7 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -6,63 [-18,38; +3,86] GÖSTERİLEMEDİ (n 7) |
| haftalik | KISMEN | 8 | 8 | +15,18 / -1,50 | +7,82 | +7,37 [-15,35; +42,86] | -1,89 [-12,16; +11,36] | +11,83 [-7,97; +42,33] | +75,0 / +70,0 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +10,38 [-8,38; +38,74] GÖSTERİLEMEDİ (n 7) |
| haftalik | BENZEMİYOR | 5 | 5 | -6,74 / -2,09 | -0,37 | -6,37 [-23,53; +6,98] | +0,74 [-4,16; +6,37] | -12,38 [-25,86; -0,73] | +80,0 / +73,3 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -11,29 [-25,20; +0,68] GÖSTERİLEMEDİ (n 5) |

### GÖZ ÖLÇÜMÜ GOZ_7_9 (sınıf = Cemal'in işareti)

| zaman | sınıf | n | farklı ay | R15 ort / medyan | T1 ort | TOPLAM FARK (T1) [%95] | ZAMANLAMA [%95] | SEÇİM [%95] | +%5 olay / T1 | okuma (aralık kuralı) | eşli fark (EK 23 kuralı) [%95] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| birlikte | BENZİYOR | 22 | 16 | +7,96 / -0,25 | +5,26 | +2,70 [-9,75; +16,90] | +5,91 [-3,51; +18,50] | -4,41 [-7,66; -0,69] | +59,1 / +58,2 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -4,84 [-9,52; -0,91] SONRASI KÖTÜ (n 19) |
| birlikte | KISMEN | 17 | 16 | +6,20 / -0,79 | +3,93 | +2,27 [-8,74; +20,40] | +0,60 [-4,32; +6,68] | +2,88 [-7,13; +19,47] | +41,2 / +56,1 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +2,38 [-6,99; +16,68] GÖSTERİLEMEDİ (n 15) |
| birlikte | BENZEMİYOR | 19 | 13 | +2,06 / +0,72 | +1,45 | +0,61 [-2,22; +2,59] | -0,19 [-1,71; +1,37] | +0,73 [-1,24; +2,17] | +52,6 / +52,6 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +0,64 [-2,03; +3,45] GÖSTERİLEMEDİ (n 18) |
| gunluk | BENZİYOR | 18 | 15 | -1,21 / -1,04 | +3,95 | -5,16 [-10,24; -0,61] | -1,12 [-3,32; +1,00] | -2,64 [-5,41; +0,22] | +55,6 / +54,3 | RASTGELE GÜNDEN KÖTÜ (ÖRNEKLEM YETERSİZ) | -2,54 [-5,49; +0,58] GÖSTERİLEMEDİ (n 15) |
| gunluk | KISMEN | 12 | 11 | -2,09 / -2,11 | +1,01 | -3,10 [-8,30; +2,60] | -0,19 [-2,35; +2,02] | -3,38 [-8,48; +2,34] | +25,0 / +50,5 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -2,18 [-6,78; +2,55] GÖSTERİLEMEDİ (n 10) |
| gunluk | BENZEMİYOR | 17 | 11 | +1,94 / +0,72 | +1,25 | +0,69 [-2,27; +2,46] | +0,13 [-1,37; +1,81] | +0,67 [-1,61; +2,24] | +47,1 / +49,5 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +0,53 [-2,18; +3,45] GÖSTERİLEMEDİ (n 16) |
| haftalik | BENZİYOR | 4 | 2 | +49,23 / +59,32 | +11,15 | +38,08 [-14,66; +55,66] | +37,57 [-11,58; +60,45] | -12,36 [-15,04; -4,35] | +75,0 / +76,0 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | -13,49 [-27,08; -0,39] SONRASI KÖTÜ (n 4) |
| haftalik | KISMEN | 5 | 5 | +26,09 / +1,03 | +10,94 | +15,15 [-17,83; +69,84] | +2,49 [-12,76; +21,54] | +17,91 [-10,86; +65,10] | +80,0 / +69,6 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +11,49 [-12,97; +51,24] GÖSTERİLEMEDİ (n 5) |
| haftalik | BENZEMİYOR | 2 | 2 | +3,05 / +3,05 | +3,17 | -0,12 [-7,57; +7,34] | -2,89 [-6,57; +1,73] | +1,27 [-1,27; +3,81] | +100,0 / +78,3 | AYRIŞMIYOR (ÖRNEKLEM YETERSİZ) | +1,50 [-5,58; +8,58] GÖSTERİLEMEDİ (n 2) |

KISMEN KABUL: {"set_6_9": false, "set_7_9_bilgi": false, "n_6_9": 24, "orneklem_yetersiz_6_9": true}

### PİYASA TAHMİNİ ABD — SAYI kaynağı KAPILI (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 813 / +1,23 / +1,38 / 0,69 | 166 / +0,72 / +0,76 / 0,63 | 27 / +0,33 / +0,89 / 0,59 | -0,56 [-1,60; +0,49] | -0,90 [-3,81; +2,26] |
| d2022 | 560 / +1,21 / +1,06 / 0,59 | 144 / -0,41 / -0,68 / 0,46 | 38 / +0,95 / +0,06 / 0,50 | -1,34 [-3,87; +1,30] | -0,27 [-3,95; +2,86] |
| birlikte | 1373 / +1,22 / +1,27 / 0,65 | 310 / +0,20 / +0,37 / 0,55 | 65 / +0,69 / +0,37 / 0,54 | -0,94 [-2,19; +0,31] | -0,53 [-2,72; +1,46] |

### PİYASA TAHMİNİ ABD — SAYI kaynağı KAPISIZ (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 73 / +1,97 / +2,04 / 0,82 | 214 / +1,90 / +1,65 / 0,69 | 719 / +0,81 / +1,03 / 0,66 | -0,91 [-1,91; +0,38] | -1,16 [-2,24; +0,18] |
| d2022 | 74 / +0,45 / +0,16 / 0,53 | 127 / +2,64 / +1,76 / 0,60 | 541 / +0,53 / +0,79 / 0,55 | +0,49 [-3,90; +3,10] | +0,09 [-4,33; +3,01] |
| birlikte | 147 / +1,20 / +1,31 / 0,67 | 341 / +2,17 / +1,66 / 0,66 | 1260 / +0,69 / +0,97 / 0,62 | -0,20 [-2,23; +1,43] | -0,51 [-2,59; +1,20] |

### PİYASA TAHMİNİ ABD — SAYI kaynağı KAPILI_DUY (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 796 / +1,26 / +1,43 / 0,70 | 165 / +0,68 / +0,67 / 0,62 | 45 / +0,36 / +0,78 / 0,62 | -0,65 [-1,69; +0,39] | -0,90 [-2,44; +1,20] |
| d2022 | 539 / +1,24 / +1,11 / 0,59 | 158 / -0,37 / -0,48 / 0,47 | 45 / +1,10 / -0,10 / 0,49 | -1,28 [-3,84; +1,36] | -0,13 [-3,96; +3,21] |
| birlikte | 1335 / +1,25 / +1,35 / 0,65 | 323 / +0,16 / +0,21 / 0,54 | 90 / +0,73 / +0,59 / 0,56 | -0,96 [-2,21; +0,28] | -0,52 [-2,28; +1,28] |

#### ABD — pazar son 20 günde %5'ten fazla düşmüş günler (DUS20 < -0,05)

| dönem | gün | PİYASA15 ort / medyan / artı payı | öteki günler ort | DÜŞÜŞ - öteki [%95] | DÜŞÜŞ içinde (>= 1) - (= 0) [%95] | DÜŞÜŞ dışında (>= 1) - (= 0) [%95] | SAYI >= 1 günlerinin DÜŞÜŞ payı |
|---|---|---|---|---|---|---|---|
| d1619 | 74 | +3,71 / +2,27 / 0,74 | +0,92 | +2,79 [+0,04; +5,77] | +0,13 [-3,34; +3,01] | -0,42 [-1,47; +0,61] | 0,02 |
| d2022 | 132 | -0,09 / +1,05 / 0,56 | +1,10 | -1,19 [-4,04; +1,71] | -6,05 [-11,87; -0,35] | -1,64 [-4,29; +1,11] | 0,02 |
| birlikte | 206 | +1,27 / +1,49 / 0,63 | +0,99 | +0,29 [-1,76; +2,59] | -0,28 [-10,50; +3,21] | -0,94 [-2,18; +0,31] | 0,02 |

### PİYASA TAHMİNİ AVR — SAYI kaynağı KAPILI (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 974 / +0,76 / +0,96 / 0,66 | 51 / +0,61 / +1,20 / 0,73 | 0 / - / - / - | -0,15 [-2,06; +1,51] | - |
| d2022 | 729 / +0,35 / +0,77 / 0,59 | 30 / -2,01 / -1,11 / 0,33 | 0 / - / - / - | -2,36 [-4,95; +0,00] | - |
| birlikte | 1703 / +0,58 / +0,87 / 0,63 | 81 / -0,36 / +0,32 / 0,58 | 0 / - / - / - | -0,94 [-2,49; +0,55] | - |

### PİYASA TAHMİNİ AVR — SAYI kaynağı KAPISIZ (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 463 / +0,97 / +1,06 / 0,68 | 399 / +0,66 / +1,01 / 0,67 | 163 / +0,36 / +0,82 / 0,60 | -0,40 [-1,06; +0,27] | -0,62 [-1,71; +0,37] |
| d2022 | 349 / +0,45 / +0,97 / 0,60 | 318 / +0,08 / +0,65 / 0,58 | 92 / +0,10 / +0,11 / 0,50 | -0,36 [-1,62; +0,89] | -0,35 [-2,38; +1,83] |
| birlikte | 812 / +0,75 / +0,98 / 0,65 | 717 / +0,40 / +0,82 / 0,63 | 255 / +0,26 / +0,47 / 0,56 | -0,38 [-1,03; +0,28] | -0,48 [-1,56; +0,58] |

### PİYASA TAHMİNİ AVR — SAYI kaynağı KAPILI_DUY (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 971 / +0,76 / +0,95 / 0,66 | 54 / +0,69 / +1,39 / 0,74 | 0 / - / - / - | -0,06 [-1,98; +1,59] | - |
| d2022 | 719 / +0,32 / +0,75 / 0,59 | 40 / -0,95 / -0,21 / 0,45 | 0 / - / - / - | -1,27 [-3,74; +1,13] | - |
| birlikte | 1690 / +0,57 / +0,86 / 0,63 | 94 / -0,01 / +0,51 / 0,62 | 0 / - / - / - | -0,58 [-2,05; +0,79] | - |

#### AVR — pazar son 20 günde %5'ten fazla düşmüş günler (DUS20 < -0,05)

| dönem | gün | PİYASA15 ort / medyan / artı payı | öteki günler ort | DÜŞÜŞ - öteki [%95] | DÜŞÜŞ içinde (>= 1) - (= 0) [%95] | DÜŞÜŞ dışında (>= 1) - (= 0) [%95] | SAYI >= 1 günlerinin DÜŞÜŞ payı |
|---|---|---|---|---|---|---|---|
| d1619 | 54 | +1,89 / +0,99 / 0,63 | +0,69 | +1,20 [-0,80; +4,61] | - | -0,08 [-1,91; +1,62] | 0,00 |
| d2022 | 98 | +0,75 / +2,67 / 0,64 | +0,18 | +0,56 [-2,01; +3,35] | - | -2,30 [-4,73; +0,06] | 0,00 |
| birlikte | 152 | +1,15 / +1,50 / 0,64 | +0,48 | +0,67 [-1,04; +2,66] | - | -0,89 [-2,43; +0,62] | 0,00 |

### PİYASA TAHMİNİ BIST — SAYI kaynağı KAPILI (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 863 / +1,59 / +1,95 / 0,67 | 128 / +2,36 / +1,92 / 0,64 | 12 / +3,91 / +2,97 / 0,92 | +0,90 [-1,04; +3,26] | +2,32 [-0,03; +15,12] |
| d2022 | 588 / +4,89 / +4,92 / 0,72 | 114 / +5,49 / +6,57 / 0,71 | 37 / +5,74 / +4,11 / 0,86 | +0,66 [-2,90; +4,58] | +0,85 [-3,60; +6,45] |
| birlikte | 1451 / +2,93 / +2,76 / 0,69 | 242 / +3,83 / +2,74 / 0,67 | 49 / +5,29 / +3,97 / 0,88 | +1,15 [-0,90; +3,34] | +2,37 [-0,76; +6,37] |

### PİYASA TAHMİNİ BIST — SAYI kaynağı KAPISIZ (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 424 / +1,35 / +1,84 / 0,64 | 348 / +1,60 / +1,67 / 0,67 | 231 / +2,54 / +2,95 / 0,71 | +0,62 [-0,84; +2,27] | +1,19 [-1,13; +3,79] |
| d2022 | 233 / +5,00 / +6,06 / 0,75 | 290 / +4,64 / +3,75 / 0,67 | 216 / +5,57 / +5,17 / 0,79 | +0,04 [-2,73; +3,35] | +0,58 [-2,88; +4,22] |
| birlikte | 657 / +2,65 / +2,77 / 0,68 | 638 / +2,99 / +2,21 / 0,67 | 447 / +4,01 / +3,64 / 0,74 | +0,76 [-0,82; +2,42] | +1,36 [-0,82; +3,46] |

### PİYASA TAHMİNİ BIST — SAYI kaynağı KAPILI_DUY (okuma: GÖSTERİLEMEDİ)

| dönem | SAYI = 0: gün / ort / medyan / artı | SAYI = 1-2 | SAYI >= 3 | (>= 1) - (= 0) [ay kümeli %95] | (>= 3) - (= 0) [%95] |
|---|---|---|---|---|---|
| d1619 | 853 / +1,61 / +1,95 / 0,67 | 138 / +2,16 / +1,92 / 0,63 | 12 / +3,91 / +2,97 / 0,92 | +0,69 [-1,13; +2,87] | +2,30 [-0,07; +15,00] |
| d2022 | 575 / +4,99 / +5,11 / 0,73 | 123 / +5,04 / +5,81 / 0,68 | 41 / +5,48 / +4,08 / 0,88 | +0,16 [-3,34; +3,95] | +0,49 [-3,80; +6,16] |
| birlikte | 1428 / +2,97 / +2,78 / 0,69 | 261 / +3,52 / +2,60 / 0,66 | 53 / +5,13 / +3,63 / 0,89 | +0,82 [-1,21; +2,96] | +2,15 [-0,75; +6,04] |

#### BIST — pazar son 20 günde %5'ten fazla düşmüş günler (DUS20 < -0,05)

| dönem | gün | PİYASA15 ort / medyan / artı payı | öteki günler ort | DÜŞÜŞ - öteki [%95] | DÜŞÜŞ içinde (>= 1) - (= 0) [%95] | DÜŞÜŞ dışında (>= 1) - (= 0) [%95] | SAYI >= 1 günlerinin DÜŞÜŞ payı |
|---|---|---|---|---|---|---|---|
| d1619 | 98 | +2,28 / +3,69 / 0,68 | +1,65 | +0,62 [-3,25; +4,30] | - | +0,99 [-0,89; +3,27] | 0,00 |
| d2022 | 69 | +5,41 / +3,63 / 0,62 | +4,99 | +0,43 [-4,75; +4,35] | - | +0,73 [-2,98; +4,53] | 0,00 |
| birlikte | 167 | +3,57 / +3,63 / 0,66 | +3,07 | +0,50 [-2,88; +3,61] | - | +1,23 [-0,81; +3,42] | 0,00 |

PİYASA TAHMİNİ GENEL (ABD KAPILI; AVR ile): GÖSTERİLEMEDİ

T2 hücreleri: gunluk|ABD|d1619: n 5000, ort +1,25, medyan +0,51, +%5 +45,4; gunluk|ABD|d2022: n 5000, ort +0,82, medyan +0,00, +%5 +54,6; gunluk|AVR|d1619: n 5000, ort +0,70, medyan +0,52, +%5 +34,6; gunluk|AVR|d2022: n 5000, ort -0,24, medyan +0,00, +%5 +41,7; gunluk|BIST|d1619: n 5000, ort +1,65, medyan +0,00, +%5 +55,9; gunluk|BIST|d2022: n 5000, ort +5,76, medyan +2,28, +%5 +67,7; haftalik|ABD|d1619: n 5000, ort +4,71, medyan +2,53, +%5 +72,8; haftalik|ABD|d2022: n 5000, ort +5,77, medyan -0,08, +%5 +72,8; haftalik|ABD|o16: n 5000, ort +4,65, medyan +2,80, +%5 +72,5; haftalik|AVR|d1619: n 5000, ort +2,88, medyan +2,93, +%5 +67,9; haftalik|AVR|d2022: n 5000, ort +1,58, medyan +0,93, +%5 +67,0; haftalik|AVR|o16: n 5000, ort +4,12, medyan +3,26, +%5 +70,0; haftalik|BIST|d1619: n 5000, ort +9,87, medyan +2,11, +%5 +76,3; haftalik|BIST|d2022: n 5000, ort +30,49, medyan +12,38, +%5 +84,9

## KONTROL LİSTESİ

Ön kayıttaki tablo (14 madde; IZ_KARNE.ik_kontrol_kapisi geçti) aynen geçerli. Denetimde yeniden okundu: K1 üç taban (T1, T2, PİYASA(t)) + EK 24 eşli fark + KAPISIZ kontrol + düşüş günü satırı uygulandı; K2 giriş bölge sonundan sonra, rastgele gün stop'u t'ye kadar, SAYI(g) yalnız bölge sonu <= g (test), veri <= 2022-12-31 (assert + KASA); K4 rastgele günler bilinen bölgelere <= 14 bar yakınsa dışlandı, T1 yerine koymadan; K7 hayatta kalma yanlılığı yazıldı; K8 n >= 30 ve ay >= 12 şartı, ilk 3 ay payı her tabloda, göz sınıflarında ÖRNEKLEM YETERSİZ; K9 ön kayıt commit d8b9470 getirilerden önce; K11 iki hücre + T1 makinesi bağımsız üretildi; K12 başlık 'KODUN SEÇTİĞİ BÖLGELER', 'kalıbın sonucu' denmedi; K13 yasak dosyalara dokunulmadı, EK 24 fonksiyonları / çıktıları değişmedi (test), yalnız kendi yolları commit; K14 uygulanmaz. HAYIR olması gereken EVET bulunmadı.

## HATA

- (kod, etkisiz) Getirisiz denetimde E0 / stop karşılaştırması ilk taslakta göreli 1e-5 toleranslıydı; EK 24 csv'si fiyatları 6 ondalıkla yazdığı için düşük fiyatlı BIST hissesinde (SASA 2016-11-24, E0 0,0208) yanlış DUR verdi; mutlak 6e-7 (yuvarlama payı) toleransa çevrildi. Ön kayıttan ve bütün getirilerden ÖNCE düzeltildi; sayılara etkisi yok.
- Sonucu değiştiren hesap / veri / geleceğe bakma hatası bulunmadı.
- Not (sınır): T2'de giriş <= stop (20 bar dibi x 0,98) olan günler çekilmedi (olaylarla aynı ölçülebilirlik); PİYASA(t)'de bu şart yok. ZAMANLAMA bu küçük seçim farkını içerir.
- Not (süreç): commit'lerin sonuna oturumun atama satırı (Co-Authored-By: Claude Opus 5.5) yazıldı; iş tanımı 'Claude Fable 5.2' satırını istemişti (sistem atama kuralı öncelikli). Ana model gerekirse düzeltir.

## SAPMA

Yok. Tanım, eşik ve okuma kuralları ön kayıttaki gibi uygulandı. İş tanımında yorum gerektiren 10 nokta ön kayıtta (ölçümden önce) yazıldı: '15 bardan yakın' = |fark| <= 14 ve bilinen bölgeler kümesi; T1 dönemi giriş tarihine göre; rastgele gün geçerliliği; T1 200 çekim (KAPISIZ dahil, 50'ye inilmedi); T2 belirsizliğinin bootstrap'a katılması; PİYASA(t) verisi / dışlaması; TAM küme; göz sınıf sütunu ve KISMEN KABUL kararının set 6-9 ile verilmesi; 2b SAYI kaynağı (KAPILI ANA), takvim ve düşüş tanımı; 'iki pazarda' koşulu.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç (MUM_IZI EK 25): 'KODUN SEÇTİĞİ BÖLGELER, rastgele gün tabanı: günlük KAPILI ana n 256 (61 ay) R15 -0,13 %, aynı hisse rastgele gün +1,86 %; TOPLAM FARK -1,99 puan [-4,03; -0,15] RASTGELE GÜNDEN KÖTÜ; ZAMANLAMA -0,27 [-1,61; +1,18] AYRIŞMIYOR; SEÇİM -2,06 [-3,69; -0,54]; haftalık n 127 TOPLAM -2,64 [-7,97; +2,39] AYRIŞMIYOR; karar hücreleri ABD 2016-19 / 2020-22 AYRIŞMIYOR (az sayıda döneme dayanıyor), AVR ÖLÇÜLEMEDİ; KAPISIZ AYRIŞMIYOR. Göz ölçümü (set 6-9): BENZİYOR / KISMEN / BENZEMİYOR TOPLAM +3,04 / -0,06 / -3,08, hepsi AYRIŞMIYOR (ÖY); KISMEN KABUL SAYILMAZ. Piyasa tahmini: ABD (SAYI >= 1) - (SAYI = 0) PİYASA15 -0,56 [-1,60; +0,49] / -1,34 [-3,87; +1,30], AVR -0,15 / -2,36: GÖSTERİLEMEDİ. Karar: bölgeler rastgele güne göre mutlak kârlı değil, zamanlama yok, piyasayı öncelemiyor; kasa açılmaz; evren yukarı yanlı.'
- IK_ILERI: 'MUM_IZI EK 25 piyasa tahmini GÖSTERİLEMEDİ (yön eksi) ve günlük TOPLAM FARK RASTGELE GÜNDEN KÖTÜ: aynı komut (MUM_IZI_HAVUZ kos25), aynı eşik, kasa kuralı izin verdiğinde 2023-26 verisiyle ya da batanlar dahil evrenle yeniden.'
- IK_GOREV: 'EK 25 ölçüm: kod 7f3e5d5, ön kayıt d8b9470, sonuç (bu commit).'
- IK_HATA (etkisiz): 'EK 25 getirisiz denetimde göreli tolerans csv 6 ondalık yuvarlamasıyla çakıştı (SASA); ön kayıttan önce mutlak toleransa çevrildi.'
