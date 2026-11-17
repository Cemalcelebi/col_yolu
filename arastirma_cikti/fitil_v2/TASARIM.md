# FITIL_V2 — TASARIM SINAMASI (AŞAMA 1; getirisiz)

FITIL_V2 v1.0 (2026-11-17): S+ v2 'TAM GİRİLİR' (şekil + savunma hattı + dönüm + yol almamış + tepede değil), ORTAK CETVEL v1.0 ile

- ZAMAN (UTC): `2026-11-17 07:46:23 UTC`
- TASARIM_KOD_SHA: `376ee0544aea97133a67cb614a824d0e395f86ec778f94bbbebbfc6d8a7802fc`
- KOR_ANAHTAR_SHA: `75ccc5f77c13150ef061578702ef6ce0ea1995458412c21d7b89142954b1401b` (yalnız sayfa / pazar / sembol / tarih / grup okundu; r20 / r60 OKUNMADI)
- KOR_CEVAP_SHA: `a86b207b03f8660cb780f91b1e6bfb6458d979de9a1b662b56a1082538b88de8`

Bu sınama hiçbir getiri / eş farkı / sonraki fiyat hesaplamadı ve okumadı; yalnız Cemal'in t'de biten sayfaları ve örnek aralıkları üzerinde şartların doğru / yanlış olduğu sayıldı. Izgara (72 nokta), puan ve eşitlik bozma (sadelik) kuralı koşudan önce kodda yazılıydı.

## Etiket seti

- E-GİRİŞ (POZİTİF, sayfa günü TAM beklenir): sayfa 3, 6, 9, 16, 17, 22, 26
- E-ŞEKİL ((1) VAR ama TAM YOK beklenir): sayfa 20, 21, 24, 25, 28, 35, 37, 38, 41, 44, 45, 47
- NEGATİF sayfa (TAM YOK beklenir; H + S- sayfalarında E olmayan): 1, 2, 4, 7, 13, 15, 33, 46, 48, 50
- ÖRNEK+ (aralıkta en az bir TAM günü): TEHOL 2025-05-06..2025-05-28; BINBN 2024-12-23..2025-01-13; PAPIL 2025-11-14..2025-11-26
- NEGATİF aralık (hiç TAM günü yok): TEHOL 2024-12-01..2025-02-28; DGXX 2026-10-01..2026-11-13
- Puan: PUAN = (E-GİRİŞ sayfalarında sayfa günü TAM) + (3 örnek aralıkta en az bir TAM günü) + (NEGATİF sayfalarda sayfa günü TAM YOK) + (NEGATİF aralıklarda hiç TAM günü yok) + (E-ŞEKİL sayfalarında sayfa günü (1) VAR VE TAM YOK); en çok 7 + 3 + 10 + 2 + 12 = 34.
- Eşitlik: Eşit puanda en sade nokta (sözlük sırası, önceden yazıldı): (i) düz şartı kapalı > 1,5 > 1,0 (şart yok / daha az bağlayıcı); (ii) şekil S+ (Ç187 tanımı, yeni sayı yok) > gevşek; (iii) hatTol 0,02 (stop marjı ile aynı sayı) > 0,03; (iv) dusus 0,10 > 0,15 > 0,20 (en az bağlayıcı); (v) yol 0,10 > 0,05 (daha az bağlayıcı).

Veri: ABD ALM: 1607 bar, 2015-07-17 .. 2026-08-31; ABD DGXX: 721 bar, 2024-01-02 .. 2026-11-13; ABD GBCI: 2830 bar, 2015-06-01 .. 2026-08-31; ABD HSIC: 2830 bar, 2015-06-01 .. 2026-08-31; ABD LBTYA: 2830 bar, 2015-06-01 .. 2026-08-31; ABD LHX: 2830 bar, 2015-06-01 .. 2026-08-31; ABD MARA: 2829 bar, 2015-06-01 .. 2026-08-31; ABD MKTX: 2830 bar, 2015-06-01 .. 2026-08-31; ABD MLI: 2830 bar, 2015-06-01 .. 2026-08-31; ABD NAVI: 2830 bar, 2015-06-01 .. 2026-08-31; ABD OGN: 1330 bar, 2021-05-14 .. 2026-08-31; ABD PLTR: 1486 bar, 2020-09-30 .. 2026-08-31; ABD SMMT: 2770 bar, 2015-06-01 .. 2026-08-31; BIST ANSGR: 2812 bar, 2015-06-01 .. 2026-08-31; BIST BESLR: 2813 bar, 2015-06-01 .. 2026-08-31; BIST BINBN: 472 bar, 2024-10-11 .. 2026-08-31; BIST DOGUB: 2808 bar, 2015-06-01 .. 2026-08-31; BIST EPLAS: 2613 bar, 2015-06-02 .. 2026-08-31; BIST ETYAT: 2802 bar, 2015-06-01 .. 2026-08-31; BIST GLCVY: 1214 bar, 2021-10-21 .. 2026-08-31; BIST GOLTS: 2815 bar, 2015-06-01 .. 2026-08-31; BIST GOODY: 2814 bar, 2015-06-01 .. 2026-08-31; BIST GSRAY: 2811 bar, 2015-06-01 .. 2026-08-31; BIST ISMEN: 2811 bar, 2015-06-01 .. 2026-08-31; BIST LIDER: 1097 bar, 2022-04-05 .. 2026-08-31; BIST PAPIL: 1662 bar, 2019-12-30 .. 2026-08-31; BIST RTALB: 2783 bar, 2015-06-01 .. 2026-08-31; BIST SNPAM: 2598 bar, 2015-06-01 .. 2026-08-31; BIST SONME: 2749 bar, 2015-06-01 .. 2026-08-31; BIST TEHOL: 2796 bar, 2015-06-01 .. 2026-08-31; BIST TLMAN: 2146 bar, 2018-01-24 .. 2026-08-31; BIST TTKOM: 2816 bar, 2015-06-01 .. 2026-08-31

## SEÇİLEN NOKTA

**N30: şekil S+ (ASIM >= 0,20, ALTYOK >= 0,50), düz kapalı, hatTol 0,02, düşüş >= 0,2, yol <= 0,1**

Puan 25 / 34: E-GİRİŞ 5 / 7, örnek 2 / 3, NEGATİF sayfa elenen 9 / 10, NEGATİF aralık elenen 2 / 2, E-ŞEKİL (1) var TAM yok 7 / 12. Aynı puanlı nokta sayısı 2 (N30, N66); sadelik sırasıyla ilki seçildi.

SECIM_JSON: `{"dusus": 0.2, "duz": null, "hatTol": 0.02, "no": "N30", "sekil": "S+", "yol": 0.1}`

## ETİKET x SEÇİLEN NOKTA (✓ şart tuttu, · tutmadı; sayfa günü t)

| Etiket | Sınıf | Cemal | (1) | (2) | (3) | (4) | (5) | TAM | doğru mu | düşüren şart | BAĞLAM (konum 250) | TAM_DIP | ASIM / ALTYOK | düz | HAT / önceki 30 dip | düşüş (60 bar tepesinden) | yol (C / HAT) | 120 bar tepesinden aşağı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BIST No 3 (SPD) | E-GIRIS | E: dönüm mumları; daha aşağı yok; dip savunması; stoplu girilir | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | EVET | - | DİP (0,16) | ✓ | 0,31 / 0,50 | 0,78 | +2,9% | +23,0% | +3,3% | +61,0% |
| ABD No 6 (SPD) | E-GIRIS | E: 9'un aynısı | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | EVET | - | DİP (0,00) | ✓ | 0,40 / 0,80 | 0,57 | +2,7% | +50,9% | +0,0% | +57,6% |
| BIST No 9 (SP_ic) | E-GIRIS | E: tam ders gibi; aşağı gitme durmuş; akümülasyon; kim alıyor önemli (kur | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | EVET | - | DİP (0,22) | ✓ | 0,32 / 0,60 | 1,07 | -0,2% | +26,5% | +1,4% | +33,0% |
| BIST No 16 (SP_ic) | E-GIRIS | E: yukarı E | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | EVET | - | DİP (0,16) | ✓ | 0,23 / 0,90 | 4,00 | +1,5% | +26,8% | +5,4% | +46,6% |
| BIST No 17 (SP_ic) | E-GIRIS | E: E, yukarı gider, sert değil | ✓ | ✓ | · | ✓ | ✓ | · | HAYIR | (3) | DİP (0,10) | · | 0,23 / 0,60 | 2,25 | +3,3% | +13,2% | +7,7% | +17,5% |
| BIST No 22 (SP_ic) | E-GIRIS | E: tam istenen; aşağı gidişin son mumları 'son nokta' diyor; kesin zıplam | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | EVET | - | DİP (0,22) | ✓ | 0,45 / 0,50 | 1,91 | +0,6% | +22,5% | +3,0% | +24,3% |
| BIST No 26 (SP_dis) | E-GIRIS | E: E; yüksek dip ve yüksek tepe, yukarı zorlar | ✓ | ✓ | ✓ | · | ✓ | · | HAYIR | (4) hattan uzak | ORTA (0,59) | · | 0,22 / 0,90 | 2,67 | +9,6% | +24,3% | +25,1% | +24,3% |
| TEHOL 2025-05-06..2025-05-28 | ORNEK+ | - | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 | 16 gün | EVET | TAM günleri: 2025-05-06, 2025-05-07, 2025-05-08, 2025-05-09, 2025-05-12, 2025-05-13, 2025-05-14, 2025-05-15 | aralık günleri ORTA 16; TAM günleri ORTA 16 | 0 gün | | | | | | |
| BINBN 2024-12-23..2025-01-13 | ORNEK+ | - | 15/15 | 15/15 | 0/15 | 15/15 | 0/15 | 0 gün | HAYIR | en yakın gün 2024-12-23: (3) geçmiş yetersiz (ölçü tanımsız), (5) geçmiş yetersiz (ölçü tanımsız) | aralık günleri TANIMSIZ 15; TAM günleri - | 0 gün | | | | | | |
| PAPIL 2025-11-14..2025-11-26 | ORNEK+ | - | 9/9 | 9/9 | 9/9 | 9/9 | 9/9 | 9 gün | EVET | TAM günleri: 2025-11-14, 2025-11-17, 2025-11-18, 2025-11-19, 2025-11-20, 2025-11-21, 2025-11-24, 2025-11-25 | aralık günleri DİP 9; TAM günleri DİP 9 | 9 gün | | | | | | |
| BIST No 20 (SP_dis) | E-SEKIL | E: 21 gibi; son büyük mum gelmiş; içindeysem %70 satılır | ✓ | ✓ | · | · | · | · | EVET | (3), (4) hattan uzak, pencere tepesini kırmış, (5) | TEPE (1,00) | · | 0,25 / 0,70 | 1,91 | +12,6% | -11,9% | +22,4% | +0,0% |
| BIST No 21 (SP_dis) | E-SEKIL | E: sol mumlar yukarı demiş, olay olmuş | ✓ | ✓ | · | · | · | · | EVET | (3), (4) hattan uzak, (5) | TEPE (0,94) | · | 0,22 / 0,60 | 3,27 | +26,6% | -17,2% | +18,6% | +0,0% |
| ABD No 24 (SP_dis) | E-SEKIL | E: E mumları, eğim yukarı; son büyük mumdan sonra ters dönme ihtimali; yo | ✓ | ✓ | · | · | · | · | EVET | (3), (4) pencere tepesini kırmış, (5) | TEPE (0,99) | · | 0,25 / 0,60 | 6,58 | +3,2% | -3,7% | +7,3% | +0,0% |
| BIST No 25 (SM) | E-SEKIL | E: taban mumları E; zaten yol almış, daha çıkar, yukarı stopla izlerim | · | ✓ | · | · | ✓ | · | HAYIR | (1), (3), (4) hattan uzak | ORTA (0,74) | · | -0,22 / 0,50 | 4,93 | +122,8% | -48,5% | +22,2% | +15,7% |
| ABD No 28 (SM) | E-SEKIL | E: E ama aşağıya | · | · | ✓ | · | ✓ | · | HAYIR | (1), (2) yeni dip / hat kırık, (4) hattan uzak | DİP (0,13) | · | -0,20 / 0,50 | 3,17 | -33,6% | +43,1% | +13,1% | +43,1% |
| BIST No 35 (SM) | E-SEKIL | E: E ama ters gidecekken dönmüş yukarı | · | ✓ | · | ✓ | · | · | HAYIR | (1), (3), (5) | ORTA (0,29) | · | -0,28 / 0,20 | 1,33 | +8,6% | +5,7% | +4,8% | +10,8% |
| BIST No 37 (SM) | E-SEKIL | E: E ama aşağıya; üst savunma hattı kırılmış, belirsizlik, girmem | · | ✓ | · | ✓ | · | · | HAYIR | (1), (3), (5) | ORTA (0,71) | · | -0,20 / 0,10 | 2,43 | +7,2% | +10,2% | +5,3% | +10,7% |
| ABD No 38 (SP_dis) | E-SEKIL | E: E ama ters aşağıya gidecek | ✓ | ✓ | · | ✓ | ✓ | · | EVET | (3) | DİP (0,06) | · | 0,20 / 0,50 | 3,97 | +2,2% | +13,1% | +0,1% | +16,2% |
| BIST No 41 (SP_ic) | E-SEKIL | E: E ancak savunulan bölge kırılmış | ✓ | · | ✓ | ✓ | ✓ | · | EVET | (2) yeni dip / hat kırık | DİP (0,17) | · | 0,29 / 0,50 | 2,32 | -2,4% | +31,8% | +0,0% | +34,3% |
| BIST No 44 (SPD) | E-SEKIL | E:  | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | HAYIR | - | ORTA (0,36) | · | 0,23 / 0,50 | 0,87 | +0,9% | +43,3% | +3,9% | +43,3% |
| ABD No 45 (SP_ic) | E-SEKIL | E:  | ✓ | · | ✓ | ✓ | ✓ | · | EVET | (2) yeni dip / hat kırık | DİP (0,00) | · | 0,21 / 0,70 | 2,00 | -2,4% | +41,5% | +2,5% | +57,0% |
| BIST No 47 (SP_dis) | E-SEKIL | E:  | ✓ | ✓ | · | ✓ | ✓ | · | EVET | (3) | ORTA (0,47) | · | 0,20 / 0,80 | 2,31 | +10,0% | +12,2% | +7,5% | +22,2% |
| ABD No 1 (SP_dis) | NEG | H: tepe mumlar düşeceğini göstermiş; olmuş; dahası var | ✓ | · | ✓ | ✓ | ✓ | · | EVET | (2) yeni dip / hat kırık | DİP (0,00) | · | 0,21 / 0,60 | 5,72 | -17,9% | +30,8% | +0,2% | +33,8% |
| BIST No 2 (SP_ic) | NEG | H: dönüş mumları değil; yön aşağı | ✓ | ✓ | · | ✓ | ✓ | · | EVET | (3) | ORTA (0,39) | · | 0,31 / 0,50 | 1,77 | +2,6% | +19,7% | +1,8% | +23,8% |
| ABD No 4 (SM) | NEG | H: bayağı düşmüş, devamı var; yön mumları, dönüm mumları değil | · | · | ✓ | ✓ | ✓ | · | EVET | (1), (2) yeni dip / hat kırık | DİP (0,05) | · | -0,20 / 0,10 | 2,36 | -6,6% | +33,4% | +6,4% | +47,8% |
| ABD No 7 (SM) | NEG | B: yukarı devam gösterir ama alım noktası değil | · | ✓ | · | ✓ | · | · | EVET | (1), (3), (5) | TEPE (0,85) | · | -0,24 / 0,20 | 2,99 | +17,8% | +5,5% | +6,1% | +5,5% |
| ABD No 13 (SM) | NEG | B: B; yukarı eğimli; yol var mı göstermiyor | · | ✓ | · | ✓ | · | · | EVET | (1), (3), (5) | ORTA (0,61) | · | -0,22 / 0,20 | 3,43 | +0,2% | +2,7% | +7,8% | +2,7% |
| ABD No 15 (SP_ic) | NEG | H: girmem | ✓ | ✓ | · | ✓ | · | · | EVET | (3), (5) | ORTA (0,40) | · | 0,24 / 0,60 | 0,96 | +1,9% | +8,4% | +2,4% | +12,4% |
| BIST No 33 (SM) | NEG | B: stabil coin grafiği gibi; normalde çok yatay gitmeli (harf yok -> B) | · | ✓ | · | ✓ | · | · | EVET | (1), (3), (5) | ORTA (0,50) | · | -0,38 / 0,20 | 0,50 | +8,4% | +0,9% | +1,9% | +0,9% |
| ABD No 46 (SP_ic) | NEG | H:  | ✓ | ✓ | ✓ | ✓ | ✓ | TAM | HAYIR | - | DİP (0,11) | ✓ | 0,23 / 0,50 | 1,43 | +16,0% | +26,7% | +0,8% | +40,2% |
| BIST No 48 (SM) | NEG | B:  | · | ✓ | ✓ | ✓ | ✓ | · | EVET | (1) | DİP (0,07) | · | -0,20 / 0,80 | 7,00 | +9,6% | +21,5% | +1,6% | +28,1% |
| ABD No 50 (SM) | NEG | B:  | · | · | ✓ | ✓ | ✓ | · | EVET | (1), (2) yeni dip / hat kırık | ORTA (0,26) | · | -0,29 / 0,50 | 11,00 | -26,4% | +58,7% | +5,2% | +58,7% |
| TEHOL 2024-12-01..2025-02-28 | NEG-ARALIK | - | 0/64 | 64/64 | 20/64 | 10/64 | 30/64 | 0 gün | EVET | en yakın gün 2024-12-02: (1) | aralık günleri TEPE 32, ORTA 18, DİP 14; TAM günleri - | 0 gün | | | | | | |
| DGXX 2026-10-01..2026-11-13 | NEG-ARALIK | - | 0/32 | 5/32 | 32/32 | 21/32 | 32/32 | 0 gün | EVET | en yakın gün 2026-10-01: (1) | aralık günleri DİP 29, ORTA 3; TAM günleri - | 0 gün | | | | | | |

BAĞLAM (EK, sonuç görülmeden; ızgaraya ve puana girmez): EK (Cemal, 17 Kas; ön kayıttan önce, sonuç görülmeden): KONUM = (C_t - min(Low, t dahil 250 geçerli bar)) / (max(High, 250) - min(Low, 250)); DİP = KONUM <= 0,25 VE C_t <= max(Close, 120 geçerli bar) x (1 - 0,15); TEPE = KONUM >= 0,75; ORTA = ikisi de değil (yolun ortası); 250 bar yoksa TANIMSIZ (hiçbir sınıfa girmez). Eşikler sabit, ızgaraya girmez.
E-GİRİŞ sayfaları ve 3 örneğin bağlamı: No 3 DİP; No 6 DİP; No 9 DİP; No 16 DİP; No 17 DİP; No 22 DİP; No 26 ORTA; TEHOL TAM günleri ORTA 16 (aralık: ORTA 16); BINBN TAM günleri yok (aralık: TANIMSIZ 15); PAPIL TAM günleri DİP 9 (aralık: DİP 9).
Seçilen noktada TAM_DIP (ana satır) etiket setinde: E-GİRİŞ 5 / 7, örnek aralıkta TAM_DIP günü olan 1 / 3, NEGATİF sayfada TAM_DIP 1 / 10, E-ŞEKİL sayfada TAM_DIP 0 / 12 (bilgi).

Aralık satırlarında (1)-(5) sütunu = şartın tuttuğu gün / aralıktaki gün; TAM yoksa 'en yakın gün' en çok şartın tuttuğu ilk gündür.

## IZGARA ÖZETİ (72 nokta)

- Puan dağılımı: en düşük 20, medyan 23, en yüksek 25; en yüksek puanlı nokta sayısı 2.
- Bileşen tavanları (her bileşenin 72 noktadaki en yüksek değeri): yakalanan_E_GIRIS 6, yakalanan_ORNEK 2, elenen_NEG 10, elenen_NEG_ARALIK 2, sekil_E_SEKIL 7

| Nokta | şekil | düz | hatTol | düşüş | yol | E-GİRİŞ /7 | örnek /3 | NEG sayfa /10 | NEG aralık /2 | E-ŞEKİL /12 | PUAN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N30 **SEÇİLEN** | S+ | kapalı | 0.02 | 0.2 | 0.1 | 5 | 2 | 9 | 2 | 7 | 25 |
| N66 | gevsek | kapalı | 0.02 | 0.2 | 0.1 | 5 | 2 | 9 | 2 | 7 | 25 |
| N28 | S+ | kapalı | 0.02 | 0.15 | 0.1 | 5 | 2 | 8 | 2 | 7 | 24 |
| N29 | S+ | kapalı | 0.02 | 0.2 | 0.05 | 4 | 2 | 9 | 2 | 7 | 24 |
| N64 | gevsek | kapalı | 0.02 | 0.15 | 0.1 | 5 | 2 | 8 | 2 | 7 | 24 |
| N65 | gevsek | kapalı | 0.02 | 0.2 | 0.05 | 4 | 2 | 9 | 2 | 7 | 24 |
| N26 | S+ | kapalı | 0.02 | 0.1 | 0.1 | 6 | 2 | 8 | 2 | 5 | 23 |
| N27 | S+ | kapalı | 0.02 | 0.15 | 0.05 | 4 | 2 | 8 | 2 | 7 | 23 |
| N36 | S+ | kapalı | 0.03 | 0.2 | 0.1 | 5 | 2 | 9 | 2 | 5 | 23 |
| N62 | gevsek | kapalı | 0.02 | 0.1 | 0.1 | 6 | 2 | 8 | 2 | 5 | 23 |
| N63 | gevsek | kapalı | 0.02 | 0.15 | 0.05 | 4 | 2 | 8 | 2 | 7 | 23 |
| N72 | gevsek | kapalı | 0.03 | 0.2 | 0.1 | 5 | 2 | 9 | 2 | 5 | 23 |
| N14 | S+ | 1.5 | 0.02 | 0.1 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N13 | S+ | 1.5 | 0.02 | 0.1 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N16 | S+ | 1.5 | 0.02 | 0.15 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N15 | S+ | 1.5 | 0.02 | 0.15 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N18 | S+ | 1.5 | 0.02 | 0.2 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N17 | S+ | 1.5 | 0.02 | 0.2 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N20 | S+ | 1.5 | 0.03 | 0.1 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N19 | S+ | 1.5 | 0.03 | 0.1 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N22 | S+ | 1.5 | 0.03 | 0.15 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N21 | S+ | 1.5 | 0.03 | 0.15 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N24 | S+ | 1.5 | 0.03 | 0.2 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N23 | S+ | 1.5 | 0.03 | 0.2 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N50 | gevsek | 1.5 | 0.02 | 0.1 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N49 | gevsek | 1.5 | 0.02 | 0.1 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N52 | gevsek | 1.5 | 0.02 | 0.15 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N51 | gevsek | 1.5 | 0.02 | 0.15 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N54 | gevsek | 1.5 | 0.02 | 0.2 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N53 | gevsek | 1.5 | 0.02 | 0.2 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N56 | gevsek | 1.5 | 0.03 | 0.1 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N55 | gevsek | 1.5 | 0.03 | 0.1 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N58 | gevsek | 1.5 | 0.03 | 0.15 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N57 | gevsek | 1.5 | 0.03 | 0.15 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N60 | gevsek | 1.5 | 0.03 | 0.2 | 0.1 | 3 | 2 | 9 | 2 | 7 | 23 |
| N59 | gevsek | 1.5 | 0.03 | 0.2 | 0.05 | 3 | 2 | 9 | 2 | 7 | 23 |
| N02 | S+ | 1.0 | 0.02 | 0.1 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N01 | S+ | 1.0 | 0.02 | 0.1 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N04 | S+ | 1.0 | 0.02 | 0.15 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N03 | S+ | 1.0 | 0.02 | 0.15 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N06 | S+ | 1.0 | 0.02 | 0.2 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N05 | S+ | 1.0 | 0.02 | 0.2 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N08 | S+ | 1.0 | 0.03 | 0.1 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N07 | S+ | 1.0 | 0.03 | 0.1 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N10 | S+ | 1.0 | 0.03 | 0.15 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N09 | S+ | 1.0 | 0.03 | 0.15 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N12 | S+ | 1.0 | 0.03 | 0.2 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N11 | S+ | 1.0 | 0.03 | 0.2 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N38 | gevsek | 1.0 | 0.02 | 0.1 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N37 | gevsek | 1.0 | 0.02 | 0.1 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N40 | gevsek | 1.0 | 0.02 | 0.15 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N39 | gevsek | 1.0 | 0.02 | 0.15 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N42 | gevsek | 1.0 | 0.02 | 0.2 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N41 | gevsek | 1.0 | 0.02 | 0.2 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N44 | gevsek | 1.0 | 0.03 | 0.1 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N43 | gevsek | 1.0 | 0.03 | 0.1 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N46 | gevsek | 1.0 | 0.03 | 0.15 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N45 | gevsek | 1.0 | 0.03 | 0.15 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N48 | gevsek | 1.0 | 0.03 | 0.2 | 0.1 | 2 | 2 | 10 | 2 | 7 | 23 |
| N47 | gevsek | 1.0 | 0.03 | 0.2 | 0.05 | 2 | 2 | 10 | 2 | 7 | 23 |
| N25 | S+ | kapalı | 0.02 | 0.1 | 0.05 | 4 | 2 | 8 | 2 | 6 | 22 |
| N34 | S+ | kapalı | 0.03 | 0.15 | 0.1 | 5 | 2 | 8 | 2 | 5 | 22 |
| N35 | S+ | kapalı | 0.03 | 0.2 | 0.05 | 4 | 2 | 9 | 2 | 5 | 22 |
| N61 | gevsek | kapalı | 0.02 | 0.1 | 0.05 | 4 | 2 | 8 | 2 | 6 | 22 |
| N70 | gevsek | kapalı | 0.03 | 0.15 | 0.1 | 5 | 2 | 8 | 2 | 5 | 22 |
| N71 | gevsek | kapalı | 0.03 | 0.2 | 0.05 | 4 | 2 | 9 | 2 | 5 | 22 |
| N32 | S+ | kapalı | 0.03 | 0.1 | 0.1 | 6 | 2 | 8 | 2 | 3 | 21 |
| N33 | S+ | kapalı | 0.03 | 0.15 | 0.05 | 4 | 2 | 8 | 2 | 5 | 21 |
| N68 | gevsek | kapalı | 0.03 | 0.1 | 0.1 | 6 | 2 | 8 | 2 | 3 | 21 |
| N69 | gevsek | kapalı | 0.03 | 0.15 | 0.05 | 4 | 2 | 8 | 2 | 5 | 21 |
| N31 | S+ | kapalı | 0.03 | 0.1 | 0.05 | 4 | 2 | 8 | 2 | 4 | 20 |
| N67 | gevsek | kapalı | 0.03 | 0.1 | 0.05 | 4 | 2 | 8 | 2 | 4 | 20 |

## SINIR

- Etiket seti küçük (7 E-GİRİŞ + 3 örnek pozitif, 12 E-ŞEKİL, 10 + 2 negatif) ve sayfalar Ç187 S+ / S- seçiminden geldi: eşik seçimi tanımın Cemal'in gözüne uydurulmasıdır, bulgu değildir; ölçüm AŞAMA 2'de etiket setinin dışındaki bütün evrende ve önceden yazılı kuralla yapılır.
- Cemal'in E-GİRİŞ notları (dönüm / akümülasyon / stoplu girilir) savunma hattı ve düşüş bağlamı ister; E-ŞEKİL notları (yol almış / hat kırık / aşağı) TAM'ın eleyeceği durumlardır. Tablodaki düşüren şart sütunu bunun ne kadar tuttuğunu gösterir.
