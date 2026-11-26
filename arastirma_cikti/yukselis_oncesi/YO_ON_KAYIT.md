# YO ÖN KAYIT — yükseliş trendinden önce hangi bölge var: geriye bakış (keşif) + ileriye doğru sınama (2026-11-26T20:28:53Z)

İş tanımı YO_IS_TANIMI.md (ana model). Bu dosya Y10 / Y5 / D10 / R15 / P15 HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, okuma ve hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (yukarı yanlı, iki taraf için de). KASA açılmaz (veri <= 2022-12-31). HACİM KULLANILMAZ (P2 likidite süzgeci dışında).

## Mühürler

YO_KOD_SHA: 344fa104b62dc71119d4ba39791312cb0a721101e1c18195524c58cac0822ad8
YO_ESIK_SHA: cea9bfb9261b0bfdc1d08de3c352c0d5cc6130c84823026243da68e790c0e199
DOSYA_ozellik_ABD.pkl: 9e470d0658ccca89c17edc320b250397ce3d5f3c265e52dd831767cc46d84ca8
DOSYA_piyasa_ABD.pkl: de1cb9a2af4dd6e34ab90258d82186203b00ff2d8073ecd3769c762f0d2b8479
DOSYA_ham_ABD.npz: 41f317fbd7e8928226215683444b4319f1e8301dbcc5ac549cd80c5b59ace234
DOSYA_ozellik_AVR.pkl: daa33b4c6ba06dee2f1c300a1797f4a7e9d9e4ab113a865240d56fd44393e09f
DOSYA_piyasa_AVR.pkl: 53b5013074841ca0075bfbc901602b67e07b0afd3087eac0c6a453f9d1f82634
DOSYA_ham_AVR.npz: bf3dfcf27019a243c7281e069a04ec43c733bf8d915feb60e67021d2a6572c0b
SAYIM_SHA: 4b2228c246e676d6f3901063bc6f6577692079b12b73347af780ab854f7b439a
IS_TANIMI_SHA: 7f255cc74dbad38e27edb44b5a224e5fbd83866a9ed2c981af266e435ab5f475

- Panel dosyaları (repo dışı): /root/.kasa/ham/yukselis_oncesi (ozellik_*.pkl = örnek satırları + özellikler, piyasa_*.pkl = pazar-gün özellikleri, ham_*.npz = sonuç için bar deposu; sonuç sütunu YOK)

## GETİRİSİZ SAYIM (Y / R15 / P15 hesaplanmadı)

| hücre | hisse-gün | farklı ay | en kalabalık 3 ay payı | hisse | pazar-gün | ay (pazar-gün) |
|---|---|---|---|---|---|---|
| ABD|d1619 | 400337 | 48 | 0,078 | 2735 | 1006 | 48 |
| ABD|d2022 | 391113 | 36 | 0,105 | 3754 | 742 | 36 |
| AVR|d1619 | 80675 | 48 | 0,071 | 481 | 1025 | 48 |
| AVR|d2022 | 64958 | 36 | 0,094 | 516 | 759 | 36 |

### Özelliklerin eksik payı (%) ve dağılımı (ABD 2016-19: %2 / %10 / %50 / %90 / %98 yüzdelikleri)

| özellik | aile | eksik ABD 16-19 | eksik ABD 20-22 | eksik AVR 16-19 | eksik AVR 20-22 | %2 | %10 | %50 | %90 | %98 |
|---|---|---|---|---|---|---|---|---|---|---|
| MIKRO | MIKRO | 0,0 | 0,0 | 0,0 | 0,0 | 1,0000 | 2,0000 | 4,0000 | 6,0000 | 7,0000 |
| RS_UZAK | RS_DIP | 0,0 | 0,0 | 0,0 | 0,0 | -0,3690 | -0,2154 | -0,0673 | -0,0056 | 0,0000 |
| RS_DIP_BIR | RS_DIP | 0,5 | 1,0 | 0,2 | 0,2 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 1,0000 |
| GEN50 | GENISLIK | 0,0 | 0,0 | 0,0 | 0,0 | 0,1306 | 0,3264 | 0,6175 | 0,7714 | 0,8709 |
| GEN50_D10 | GENISLIK | 0,0 | 0,0 | 0,1 | 0,0 | -0,2992 | -0,1787 | 0,0038 | 0,2056 | 0,3355 |
| OYN_SIRA | OYN_SIRA | 0,0 | 0,0 | 0,0 | 0,0 | 0,0200 | 0,1001 | 0,5002 | 0,9000 | 0,9800 |
| MA_KOD | MA_DIZI | 1,6 | 3,0 | 0,7 | 0,6 | 0,0000 | 0,0000 | 2,0000 | 3,0000 | 3,0000 |
| MA_EGIM_DEG | MA_DIZI | 0,0 | 0,0 | 0,0 | 0,0 | -0,0976 | -0,0471 | -0,0014 | 0,0489 | 0,1050 |
| ZIRVE_BAR | DD_SURE | 2,3 | 4,4 | 0,9 | 0,9 | 0,0000 | 2,0000 | 77,0000 | 236,0000 | 249,0000 |
| ZIRVE_DUSUS | DD_SURE | 2,3 | 4,4 | 0,9 | 0,9 | -0,6046 | -0,3838 | -0,1069 | -0,0072 | 0,0000 |
| DIP_BAR | DD_SURE | 2,3 | 4,4 | 0,9 | 0,9 | 0,0000 | 0,0000 | 12,0000 | 101,0000 | 165,0000 |
| DIP_HIZ | DD_SURE | 2,3 | 4,4 | 0,9 | 0,9 | 0,0000 | 0,0000 | 0,2820 | 1,2598 | 2,8675 |
| CLV10 | CLV | 0,0 | 0,0 | 0,0 | 0,0 | 0,3010 | 0,3794 | 0,5097 | 0,6395 | 0,7167 |
| CLV_FARK | CLV | 0,0 | 0,0 | 0,0 | 0,0 | -0,2345 | -0,1463 | -0,0003 | 0,1462 | 0,2371 |
| YUKSELEN_DIP | YUKSELEN_DIP | 0,0 | 0,0 | 0,0 | 0,0 | 0,0000 | 0,0000 | 1,0000 | 3,0000 | 5,0000 |
| MOM_12_1 | KONTROL | 2,4 | 4,5 | 1,0 | 1,0 | -0,5293 | -0,2747 | 0,0904 | 0,5489 | 1,2698 |
| F15 | KONTROL | 0,0 | 0,0 | 0,0 | 0,0 | -0,1913 | -0,0889 | 0,0088 | 0,1049 | 0,2262 |
| KONUM120 | KONTROL | 0,5 | 1,0 | 0,2 | 0,2 | 0,0000 | 0,0942 | 0,6365 | 0,9827 | 1,0000 |
| ATRP20 | KONTROL | 0,0 | 0,0 | 0,0 | 0,0 | 0,0108 | 0,0146 | 0,0254 | 0,0508 | 0,0808 |
| BOY_YUZDE_ORAN | KONTROL | 0,7 | 1,3 | 0,3 | 0,3 | 0,6278 | 0,7367 | 0,9728 | 1,3943 | 1,7848 |
| ONCEKI_DUSUS | KONTROL | 0,0 | 0,0 | 0,0 | 0,0 | -0,4902 | -0,3136 | -0,1216 | -0,0362 | -0,0144 |

### Piyasa özelliklerinin eksik payı (%)

| özellik | ABD 16-19 | ABD 20-22 | AVR 16-19 | AVR 20-22 |
|---|---|---|---|---|
| GEN20 | 0,0 | 0,0 | 0,1 | 0,0 |
| GEN50 | 0,0 | 0,0 | 0,1 | 0,0 |
| GEN200 | 0,0 | 0,0 | 0,1 | 0,0 |
| GEN20_D5 | 0,0 | 0,0 | 0,2 | 0,0 |
| GEN20_D10 | 0,0 | 0,0 | 0,2 | 0,0 |
| GEN50_D5 | 0,0 | 0,0 | 0,2 | 0,0 |
| GEN50_D10 | 0,0 | 0,0 | 0,2 | 0,0 |
| GEN200_D5 | 0,0 | 0,0 | 0,2 | 0,0 |
| GEN200_D10 | 0,0 | 0,0 | 0,2 | 0,0 |
| PAZ_R20 | 0,0 | 0,0 | 0,0 | 0,0 |
| PAZ_R60 | 0,0 | 0,0 | 0,0 | 0,0 |
| PAZ_DD60 | 0,0 | 0,0 | 0,0 | 0,0 |
| DIP20_PAY | 0,0 | 0,0 | 0,1 | 0,0 |
| YENI_ZD | 0,0 | 0,0 | 0,1 | 0,0 |
| KESIT_SD | 0,0 | 0,0 | 0,1 | 0,0 |
| ATRP_MED_SIRA | 0,0 | 0,0 | 0,1 | 0,0 |

### Özellikler arası sıra ilişkisi (Spearman; ABD 2016-19)

| | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 MIKRO | 1,00 | 0,32 | -0,03 | 0,15 | 0,01 | -0,14 | 0,31 | 0,01 | -0,21 | 0,32 | -0,05 | -0,07 | 0,20 | 0,01 | 0,16 | 0,15 | 0,21 | 0,38 | -0,20 | -0,15 | 0,34 |
| 2 RS_UZAK | 0,32 | 1,00 | 0,18 | -0,03 | -0,03 | -0,40 | 0,53 | 0,14 | -0,34 | 0,68 | -0,09 | -0,16 | 0,34 | 0,12 | 0,26 | 0,18 | 0,52 | 0,74 | -0,42 | -0,13 | 0,69 |
| 3 RS_DIP_BIR | -0,03 | 0,18 | 1,00 | -0,15 | -0,05 | -0,06 | -0,11 | 0,01 | 0,09 | -0,08 | 0,06 | 0,03 | -0,01 | 0,01 | -0,01 | -0,09 | 0,01 | -0,12 | 0,01 | 0,10 | -0,05 |
| 4 GEN50 | 0,15 | -0,03 | -0,15 | 1,00 | 0,44 | 0,00 | 0,14 | 0,12 | -0,05 | 0,17 | 0,08 | 0,02 | 0,23 | 0,11 | 0,20 | -0,01 | 0,32 | 0,28 | -0,18 | -0,37 | 0,22 |
| 5 GEN50_D10 | 0,01 | -0,03 | -0,05 | 0,44 | 1,00 | 0,00 | -0,07 | 0,22 | 0,00 | 0,05 | 0,04 | 0,11 | 0,27 | 0,30 | 0,09 | -0,05 | 0,29 | 0,10 | 0,01 | 0,04 | -0,06 |
| 6 OYN_SIRA | -0,14 | -0,40 | -0,06 | 0,00 | 0,00 | 1,00 | -0,23 | -0,02 | 0,24 | -0,53 | 0,11 | 0,30 | -0,09 | 0,00 | -0,05 | -0,12 | -0,02 | -0,25 | 0,83 | 0,08 | -0,61 |
| 7 MA_KOD | 0,31 | 0,53 | -0,11 | 0,14 | -0,07 | -0,23 | 1,00 | -0,10 | -0,60 | 0,75 | -0,27 | -0,23 | 0,12 | -0,12 | 0,19 | 0,53 | 0,18 | 0,75 | -0,32 | -0,21 | 0,67 |
| 8 MA_EGIM_DEG | 0,01 | 0,14 | 0,01 | 0,12 | 0,22 | -0,02 | -0,10 | 1,00 | 0,01 | 0,09 | 0,06 | 0,01 | 0,30 | 0,37 | 0,27 | -0,15 | 0,61 | 0,13 | -0,06 | -0,00 | 0,00 |
| 9 ZIRVE_BAR | -0,21 | -0,34 | 0,09 | -0,05 | 0,00 | 0,24 | -0,60 | 0,01 | 1,00 | -0,72 | 0,75 | 0,28 | -0,12 | 0,02 | -0,12 | -0,70 | -0,14 | -0,50 | 0,28 | 0,01 | -0,44 |
| 10 ZIRVE_DUSUS | 0,32 | 0,68 | -0,08 | 0,17 | 0,05 | -0,53 | 0,75 | 0,09 | -0,72 | 1,00 | -0,38 | -0,31 | 0,29 | 0,07 | 0,23 | 0,55 | 0,38 | 0,81 | -0,61 | -0,18 | 0,78 |
| 11 DIP_BAR | -0,05 | -0,09 | 0,06 | 0,08 | 0,04 | 0,11 | -0,27 | 0,06 | 0,75 | -0,38 | 1,00 | 0,21 | 0,02 | 0,05 | -0,01 | -0,44 | 0,05 | -0,16 | 0,07 | -0,16 | -0,15 |
| 12 DIP_HIZ | -0,07 | -0,16 | 0,03 | 0,02 | 0,11 | 0,30 | -0,23 | 0,01 | 0,28 | -0,31 | 0,21 | 1,00 | 0,07 | 0,12 | -0,08 | -0,15 | 0,07 | -0,14 | 0,32 | 0,12 | -0,34 |
| 13 CLV10 | 0,20 | 0,34 | -0,01 | 0,23 | 0,27 | -0,09 | 0,12 | 0,30 | -0,12 | 0,29 | 0,02 | 0,07 | 1,00 | 0,83 | 0,20 | 0,02 | 0,52 | 0,39 | -0,15 | -0,09 | 0,18 |
| 14 CLV_FARK | 0,01 | 0,12 | 0,01 | 0,11 | 0,30 | 0,00 | -0,12 | 0,37 | 0,02 | 0,07 | 0,05 | 0,12 | 0,83 | 1,00 | 0,08 | -0,07 | 0,40 | 0,12 | -0,02 | 0,04 | -0,09 |
| 15 YUKSELEN_DIP | 0,16 | 0,26 | -0,01 | 0,20 | 0,09 | -0,05 | 0,19 | 0,27 | -0,12 | 0,23 | -0,01 | -0,08 | 0,20 | 0,08 | 1,00 | 0,01 | 0,39 | 0,30 | -0,13 | -0,14 | 0,27 |
| 16 MOM_12_1 | 0,15 | 0,18 | -0,09 | -0,01 | -0,05 | -0,12 | 0,53 | -0,15 | -0,70 | 0,55 | -0,44 | -0,15 | 0,02 | -0,07 | 0,01 | 1,00 | -0,02 | 0,35 | -0,16 | -0,03 | 0,29 |
| 17 F15 | 0,21 | 0,52 | 0,01 | 0,32 | 0,29 | -0,02 | 0,18 | 0,61 | -0,14 | 0,38 | 0,05 | 0,07 | 0,52 | 0,40 | 0,39 | -0,02 | 1,00 | 0,55 | -0,13 | -0,12 | 0,26 |
| 18 KONUM120 | 0,38 | 0,74 | -0,12 | 0,28 | 0,10 | -0,25 | 0,75 | 0,13 | -0,50 | 0,81 | -0,16 | -0,14 | 0,39 | 0,12 | 0,30 | 0,35 | 0,55 | 1,00 | -0,37 | -0,28 | 0,73 |
| 19 ATRP20 | -0,20 | -0,42 | 0,01 | -0,18 | 0,01 | 0,83 | -0,32 | -0,06 | 0,28 | -0,61 | 0,07 | 0,32 | -0,15 | -0,02 | -0,13 | -0,16 | -0,13 | -0,37 | 1,00 | 0,35 | -0,71 |
| 20 BOY_YUZDE_ORAN | -0,15 | -0,13 | 0,10 | -0,37 | 0,04 | 0,08 | -0,21 | -0,00 | 0,01 | -0,18 | -0,16 | 0,12 | -0,09 | 0,04 | -0,14 | -0,03 | -0,12 | -0,28 | 0,35 | 1,00 | -0,32 |
| 21 ONCEKI_DUSUS | 0,34 | 0,69 | -0,05 | 0,22 | -0,06 | -0,61 | 0,67 | 0,00 | -0,44 | 0,78 | -0,15 | -0,34 | 0,18 | -0,09 | 0,27 | 0,29 | 0,26 | 0,73 | -0,71 | -0,32 | 1,00 |

- |rho| >= 0,70 olan çiftler: RS_UZAK - KONUM120 0,74; OYN_SIRA - ATRP20 0,83; MA_KOD - ZIRVE_DUSUS 0,75; MA_KOD - KONUM120 0,75; ZIRVE_BAR - ZIRVE_DUSUS -0,72; ZIRVE_BAR - DIP_BAR 0,75; ZIRVE_DUSUS - KONUM120 0,81; ZIRVE_DUSUS - ONCEKI_DUSUS 0,78; CLV10 - CLV_FARK 0,83; KONUM120 - ONCEKI_DUSUS 0,73; ATRP20 - ONCEKI_DUSUS -0,71

## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)

1. Birim hisse-gün t = hissenin kendi geçerli bar indeksi k, k % 5 == 0 (0'dan); t takvim satırı değil, hissenin barıdır. Giriş = k + 1 barının açılışı; 15 geçerli bar giriş barı dahil (k + 1 .. k + 15; MUM_IZI_GOZ.gz_olc_bir gibi giriş barının High / Low'u sayılır).
2. Aynı barda hedef ve stop: STOP ÖNCE (Y10 / Y5 = 0; D10 aynasında da 'stop' = +%5 önce, D10 = 0). Bu kötümser kural iki yönde aynıdır; ASİMETRİ'de iki taraf da aynı kuralla sayılır.
3. Evren = giriş barı satırında TEZGÂH 2 P2 (KART_TUR2.k2_panel; MUM_IZI_HAKEM / MH.mh_p2 ile aynı 'giriş günü' üyeliği). BIST'te P2 yok: BIST hesaplanmaz (iş tanımında yalnız bilgi).
4. Dönem giriş tarihine göre (HV.hv_hucre_ad). 2016 öncesi giriş yok; özellikler 2015 verisini geçmiş olarak kullanır (veri 2015-01-02'de başlar: MOM_12_1 / DD_SURE / SMA200 2016 başında eksik olabilir, eksik payı sayımda).
5. Kontrol özellikleri repodaki tanımlarla: KONUM120 = OLCU_SINAMA._os_atrp_f15 'f15' (repoda adı F15 = 120 barlık konum); iş tanımındaki F15 = '15 barlık geçmiş getiri' (C_k / C_{k-15} - 1; repoda bu adla başka tanım yok, iş tanımı uygulandı); MOM_12_1 = OLCU_SINAMA kart MOM (C_{k-21} / C_{k-252} - 1; K60'ın aylık MOM_12_1'inin günlük karşılığı); ATRP20 = UC_IZ2.uc2_ret_atrp formülü (20 bar TR ortalaması / C; OS kovasındaki ATRP14 değil, iş tanımı ATRP20 dedi).
6. EK 27 ölçüleri (BOY_YUZDE_ORAN, ONCEKI_DUSUS) MUM_IZI27_IS_TANIMI.md 2. bölüm metninden kuruldu (MUM_IZI_UC.py içe alınmadı): pencere = t'de biten 16 bar (EK 27 E2 'her pencere' genişliği); 'önceki 120 bar' = k-135 .. k-16; ONCEKI_DUSUS = pencere dibi (min Low) / önceki 60 barın (k-75 .. k-16) en yükseği (maks High) - 1.
7. RS_DIP ailesi: göreli güç = hisse kapanışı / pazar eşit ağırlıklı endeksi L (P2 kümesi günlük getirilerinden); 'fiyatın 120 barlık konumu' sütunu KONUM120 kontrolüyle aynı tanım olduğundan ayrı satır yazılmaz; 'birlikte' = RS_DIP_BIR bayrağı. GENISLIK ailesi hisse satırlarında GEN50 ve GEN50_D10; öteki genişlik düzeyleri piyasa özellikleridir.
8. MA_DIZI 'sıralama kodu' sıralı tamsayı (0-3) olarak kodlandı; MA_KOD ve RS_DIP_BIR bayrak satırıdır (uç = yönün uç kategorisi; uç %10 / %2 ayrımı yok; gerçek pay yazılır). Tamsayı özelliklerde (MIKRO, YUKSELEN_DIP, ZIRVE_BAR, DIP_BAR) yüzdelik eşiği eşitleri içerir; uç payı %10'dan büyük olabilir (yazılır).
9. Yön: ADIM 1'de eşli SMD işareti (> 0 BÜYÜK, < 0 KÜÇÜK); AUC bilgi. Kesimler: ABD 2020-22 keşfin SAYISAL kesimleriyle (gerçek ileri sınama); AVR hücreleri AVR'nin fiyat ölçeği / oynaklık düzeyi farklı olduğu için aynı yüzdelik DÜZEYLERİNİN AVR 2016-19 ÖZELLİK dağılımındaki değerleriyle (getirisiz; ADIM 1'de, AVR sonucu görülmeden yo_kesim.json'a yazılır). ATRP beşlik sınırları ve kontrol / basit puan kesimleri de aynı kural.
10. Popülasyon her satırda özelliği sonlu ve ATRP20 sonlu olan hisse-günler; taban (P(Y10), ATRP beşliği oranları) bu kümeden. TOPLAM FARK için hisse ortalaması hissenin o hücredeki BÜTÜN örnek günlerinden (özellik eksik olanlar dahil).
11. Bootstrap kümesi giriş ayı; B = 10.000; tohum 28 (+ satır anahtarı crc32). BH p'si ABD 2020-22 KAT için tek yönlü bootstrap p'si ((1 + #KAT* <= 1) / (B + 1)); hisse ailesi 40 satır (21 sütun; RS_DIP_BIR ve MA_KOD tek), piyasa ailesi 32 satır ayrı. BİRLEŞİM ve PUAN BH ailesine girmez (tek sınama; p <= 0,10).
12. Hükümde 'AVR yönü' = AVR 2016-19 ve 2020-22'nin İKİSİNDE (KAT - 1), ASİMETRİ, TOPLAM FARK nokta değerlerinin > 0 olması (n >= 30); aralık aranmaz. 'YALNIZ OYNAKLIK' = ham KAT alt ucu iki ABD döneminde > 1 ama ATRP içi KAT alt ucu <= 1 ya da ASİMETRİ <= 0 (birinde). 'TEK DÖNEM' raporda 'ileriye doğru tutmadı' diye okunur.
13. Piyasa birimi pazar-gün (her satır; 15 günlük pencereler örtüşür, çıkarım ay kümeli). Piyasa satırında ÖLÇÜLEMEDİ = uç gün < 30 ya da farklı ay < 12 (hisse satırının n >= 1.000 şartı piyasa için konamaz: dönem başına ~750-1.000 gün); piyasa 'AVR yönü' AVR hücresinde >= 10 uç günle. P15'te olay dışlaması yok.
14. BİRLEŞİM adayı keşif uç %10 satırıyla (doğrulama görülmeden): tek başına keşifte üç alt uç şartını geçen sütunlar; çift seçimi keşif KAT'ıyla (bootstrap 200, yalnız nokta değer kullanılır). BASİT PUAN: L1 lojistik lambda 0,001 sabit (ayar yok); KONTROL PUANI: Newton lojistik (cezasız).
15. Kontrolü geçme: TUTAR satırının ABD 2020-22 uç kümesinde KAT, ATRP beşliği yerine kontrol puanı beşliğiyle (keşif sınırları) > 1 ve alt ucu > 1.
16. KALICI (30 bar +%20 / -%8) ve Y5 yalnız bilgi; hükme girmez. SEÇİM = R15 - P15(d) bilgi.

## Tanımlar (YO_ESIK; sha yukarıda)

```
{
 "surum": "YO-1.0",
 "tohum": 28,
 "tohum_tanim": "np.random.default_rng([28, crc32(anahtar)]); eşleşme anahtarı 'esle', bootstrap anahtarı satır adı; sıra bağımsız, tekrarlanabilir",
 "veri": "MUM_IZI.mi_veri(pazar, MUM_IZI_V2.MV_YOL['gunluk']) (OS.os_veri: geçerli bar O/H/L/C > 0 sonlu, H > L, V > 0; ABD evren dışı fon listesi; DS açılış kırpması); ABD, AVR; BIST hesaplanmaz (P2 tanımsız; iş tanımında bilgi)",
 "evren": "TEZGÂH 2 P2 havuzu: KART_TUR2.k2_panel(Vd, pazar) -> P2[d, j] (d = birleşik takvim satırı; d - 1'e kadarki bilgi); hisse-gün t örneklemde <=> giriş barı t + 1'in satırında P2",
 "ornek": {
  "adim": 5,
  "tanim": "hissenin kendi geçerli bar indeksi k (0'dan) k % 5 == 0; giriş barı k + 1 ile k arasında <= 10 birleşik takvim satırı (OS giriş azami boşluğu); k + 15 hissenin verisinde ve k + 1 .. k + 15 barları <= 30 birleşik takvim satırında (2H kuralı); giriş tarihi 2016-01-01 .. 2022-12-31; 15. bar <= 2022-12-31",
  "giris_bosluk": 10,
  "pencere_satir": 30
 },
 "hucre": {
  "tanim": "giriş tarihine göre MUM_IZI_HAVUZ.hv_hucre_ad (d1619 = 2016-19, d2022 = 2020-22)",
  "kesif": "ABD|d1619",
  "dogrulama": "ABD|d2022",
  "avr": [
   "AVR|d1619",
   "AVR|d2022"
  ]
 },
 "yukselis": {
  "ufuk": 15,
  "Y10": [
   0.1,
   0.05
  ],
  "Y5": [
   0.05,
   0.05
  ],
  "D10": [
   0.1,
   0.05
  ],
  "tanim": "giriş E0 = t + 1 barının açılışı; barlar t + 1 .. t + 15 (giriş barı dahil, GZ gibi); Y10: ilk High >= E0 x 1,10 barı, ilk Low <= E0 x 0,95 barından ÖNCE; Y5 aynı (+%5 / -%5); D10 (ayna): ilk Low <= E0 x 0,90 barı, ilk High >= E0 x 1,05 barından ÖNCE; aynı barda iki sınır = STOP ÖNCE (Y10 / Y5 / D10 = 0; kötümser, iki yönde aynı); R15 = t + 15 kapanışı / E0 - 1; KALICI (bilgi) = 30 barda +%20, -%8'den önce (aynı kural; k + 30 yoksa ya da > 60 satır ise NaN)",
  "KALICI": [
   0.2,
   0.08,
   30
  ]
 },
 "piyasa": {
  "en_az_hisse": 5,
  "esik_YP": 0.05,
  "esik_DP": -0.05,
  "kume_en_az": 30,
  "P15": "P15(d) = d satırında P2 ve açılışı sonlu > 0 olan bütün hisselerin [d, d + 14] satırlarındaki son geçerli kapanış / açılış(d) - 1 eşit ağırlıklı ortalaması (hv25_piyasa_R mantığı; olay dışlaması yok); < 5 hisse ise yok; hisse-gün için d = giriş barının satırı",
  "endeks": "pazar endeksi L: r(t) = P2[t] hisselerinin Cl[t] / Cf[t - 1] - 1 ortalaması (Cf = kapanış 5 satıra kadar ileri taşınmış; < 5 hisse ise r = 0); L = birikimli çarpım",
  "gun": "piyasa birimi pazar-gün t (her satır; örtüşmeli), giriş satırı d = t + 1, dönem d tarihine göre; d + 14 veri içinde; özellikler t satırına kadar; kesit kümesi A_t = P2[t] ve değer sonlu, >= 30 hisse"
 },
 "ozellik": {
  "MIKRO": "son 60 barda (u_i = C_i > C_{i-1}, i = k-59..k; k >= 60) art arda en az 3 yükselen kapanış serisi sayısı (pencere başında kesilen seri pencere içi uzunluğuyla)",
  "RS_UZAK": "RS = C_k / L(satır_k); RS_k / maks(RS_{k-59..k}) - 1 (<= 0)",
  "RS_DIP_BIR": "bayrak: KONUM120 < 0,5 VE RS_UZAK >= -0,03 ('fiyat alt yarıda, göreli güç zirveye %3 içinde'); RS_DIP ailesinin konum sütunu KONUM120 ile aynı tanım olduğu için ayrı satır yazılmaz (kontrolde)",
  "GEN50": "pazarda SMA50 üstündeki hisse payı (t satırı; A_t kümesi; her hisseye aynı gün aynı değer)",
  "GEN50_D10": "GEN50(t) - GEN50(t - 10 satır)",
  "OYN_SIRA": "OYN60 = son 60 günlük log getirinin std'si (ddof 1, kendi barları); t satırında A_t kümesindeki yüzdelik sırası ((küçük + 0,5 eşit) / n)",
  "MA_KOD": "sıralama kodu (SMA20 > SMA50) + (SMA50 > SMA200) + (SMA20 > SMA200) ∈ {0,1,2,3} (3 = tam yukarı dizi, 0 = tam aşağı); kendi kapanışları",
  "MA_EGIM_DEG": "SMA20 eğimi e_k = SMA20_k / SMA20_{k-10} - 1; değişim = e_k - e_{k-10}",
  "ZIRVE_BAR": "son 250 barın en yüksek kapanışından (son kez görüldüğü bar) bu yana bar sayısı",
  "ZIRVE_DUSUS": "C_k / maks250 - 1",
  "DIP_BAR": "zirveden k'ye en düşük kapanışın (son kez) barından bu yana bar sayısı",
  "DIP_HIZ": "(C_k / C_dip - 1) / maks(DIP_BAR, 1) x 100 (% / bar)",
  "CLV10": "son 10 barda (C - L) / (H - L) ortalaması",
  "CLV_FARK": "CLV10 - önceki 30 barın (k-39 .. k-10) ortalaması",
  "YUKSELEN_DIP": "yerel dip i: L_i < L_{i-1}, L_i < L_{i-2}, L_i <= L_{i+1}, L_i <= L_{i+2} (i + 2 <= k); pencere i ∈ [k-57, k-2]; son dipten geriye art arda yükselen dip sayısı (eşit kırar; pencere içiyle sınırlı)",
  "MOM_12_1": "C_{k-21} / C_{k-252} - 1 (OLCU_SINAMA kart MOM tanımı; kendi barları)",
  "F15": "C_k / C_{k-15} - 1 (iş tanımı: 15 barlık geçmiş getiri)",
  "KONUM120": "OLCU_SINAMA._os_atrp_f15 'f15' (son 120 kapanışın aralığında konum; repoda adı F15, burada KONUM120)",
  "ATRP20": "son 20 barın TR (önceki kapanışla; ilk bar H - L) ortalaması / C_k (UC_IZ2.uc2_ret_atrp formülü)",
  "BOY_YUZDE_ORAN": "EK 27 ölçü 1 (iş tanımı metninden): (H - L) / C medyanı son 16 bar / önceki 120 bar (k-135 .. k-16) medyanı",
  "ONCEKI_DUSUS": "EK 27 ölçü 12 (iş tanımı metninden): min L_{k-15..k} / maks H_{k-75..k-16} - 1 (pencere 16 bar, önceki 60 bar)"
 },
 "piyasa_ozellik": {
  "GEN20/GEN50/GEN200": "A_t kümesinde C > SMA(n) (kendi barları) payı",
  "_D5/_D10": "düzey(t) - düzey(t - 5 / 10 satır)",
  "PAZ_R20/PAZ_R60": "L(t) / L(t - 20 / 60) - 1",
  "PAZ_DD60": "L(t) / maks L(t-59 .. t) - 1",
  "DIP20_PAY": "A_t'de C_k <= min C_{k-19..k} payı (20 günlük dipte)",
  "YENI_ZD": "60 günlük kapanış zirvesinde olan pay - 60 günlük dipte olan pay",
  "KESIT_SD": "A_t'de C_k / C_{k-20} - 1 kesit std'si (ddof 1)",
  "ATRP_MED_SIRA": "A_t'de ATRP20 medyanı; bu medyanın önceki 250 satırdaki (t dahil, >= 60 değer) kendi geçmişinde yüzdelik sırası"
 },
 "adim1": {
  "es": 5,
  "tanim": "KEŞİF (ABD 2016-19) Y10 = 1 hisse-günleri; kontroller aynı t tarihi, aynı ATRP20 beşliği (keşif beşlik sınırları), Y10 = 0; olay başına 5 (yerine koymadan; < 5 ise hepsi; 0 ise olay düşer); gruplar (tarih, beşlik) sırasıyla, olaylar sembol sırasıyla; tohum 28",
  "smd": "(ort_olay - ort_kontrol) / sqrt((var_olay + var_kontrol) / 2) (kontroller satır olarak); özelliği sonlu olay ve en az bir sonlu kontrolü olan olaylar",
  "auc": "eşli AUC = olay başına kendi kontrollerine göre [1(x_o > x_k) + 0,5 1(=)] ortalaması, olaylar üzerinden ortalama",
  "yon": "SMD > 0 -> BÜYÜK, < 0 -> KÜÇÜK (= 0 ya da yok -> BÜYÜK, not)",
  "piyasa": "ABD keşif günleri: YP = 1 günleri ile öteki günler (eşsiz) SMD ve AUC (Mann-Whitney); yön aynı kural"
 },
 "kesim": {
  "uc": [
   0.1,
   0.02
  ],
  "besli": [
   0.2,
   0.4,
   0.6,
   0.8
  ],
  "tanim": "BÜYÜK yönde uç = değer >= keşif dağılımının %90 (%98) yüzdeliği; KÜÇÜK yönde <= %10 (%2) (eşitler dahil; gerçek pay yazılır); bayraklar (RS_DIP_BIR, MA_KOD) tek satır: yönün uç kategorisi; ATRP20 beşlik sınırları keşif dağılımının %20/40/60/80'i; ABD 2020-22 KEŞİFİN sayısal kesimleriyle; AVR hücreleri aynı yüzdelik DÜZEYLERİNİN AVR 2016-19 ÖZELLİK dağılımındaki (getirisiz) değerleriyle (ATRP beşlik sınırları dahil); piyasa özellikleri aynı kural (pazar-gün dağılımı)",
  "nump": "np.quantile (doğrusal)"
 },
 "olcu": {
  "populasyon": "hücrede özelliği sonlu VE ATRP20 sonlu hisse-günler (taban da bu küme)",
  "KAT_HAM": "P(Y10 | uç) / P(Y10) (hücre)",
  "KAT": "ATRP içi: sum(Y10 uçta) / sum(p_q(i)) uçta, p_q = hücrede ATRP beşliği q'nun P(Y10)'u (= beşliklerin olay ağırlıklı ortalama oranı)",
  "ASIMETRI": "[P(Y10) - P(D10)] uçta - sum_q (n_uq / n_u) [P(Y10 | q) - P(D10 | q)]",
  "TOPLAM_FARK": "R15 - aynı hissenin aynı hücredeki bütün örnek günlerinin R15 ortalaması (uç satırların ortalaması)",
  "SECIM": "R15 - P15(d) (bilgi)",
  "KAT_PUAN": "KAT ile aynı, ATRP beşliği yerine KONTROL PUANI beşliği (kontrolü geçme)",
  "bilgi": "Y5 KAT, KALICI payı, medyan R15"
 },
 "boot": {
  "B": 10000,
  "kume": "giriş ayı (YYYY-AA)",
  "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık); oranlar / KAT her tekrarda ağırlıklı toplamlardan; %95 = 2,5 / 97,5 yüzdelik; TOPLAM FARK'ta hisse ortalaması sabit",
  "p": "tek yönlü p = (1 + #(KAT* <= 1)) / (B + 1) (doğrulama ABD 2020-22)"
 },
 "bh": {
  "q": 0.1,
  "aile": "hisse satırları: 21 sütun x 2 uç (bayraklar tek) = 40 satır; p = ABD 2020-22 KAT p'si; piyasa satırları ayrı aile (16 x 2)"
 },
 "hukum": {
  "n_min": 1000,
  "ay_min": 12,
  "TUTAR": "KEŞİF ve ABD 2020-22'de: n >= 1000 VE farklı ay >= 12 VE KAT > 1 ve alt > 1 VE ASİMETRİ > 0 ve alt > 0 VE TOPLAM FARK > 0 ve alt > 0; VE BH (q 0,10) geçer VE AVR 2016-19 ve 2020-22'nin İKİSİNDE (KAT - 1), ASİMETRİ, TOPLAM FARK nokta değerleri > 0 (AVR hücresinde n >= 30)",
  "sira": "ÖLÇÜLEMEDİ (keşif ya da ABD 2020-22 n < 1000 ya da ay < 12) > TUTAR > YALNIZ OYNAKLIK > TEK DÖNEM > TERS > TUTMADI",
  "YALNIZ_OYNAKLIK": "KAT_HAM alt > 1 keşifte ve ABD 2020-22'de, ama ikisinden birinde KAT alt <= 1 ya da ASİMETRİ <= 0",
  "TEK_DONEM": "üç şart (KAT, ASİMETRİ, TOPLAM FARK alt uçları) keşif ve ABD 2020-22'den yalnız birinde (= ileriye doğru 'tutmadı' sayılır)",
  "TERS": "ABD 2020-22'de KAT üst < 1 VE ASİMETRİ üst < 0",
  "TUTMADI": "ötekiler (iki dönemde geçip BH / AVR'de kalan dahil)",
  "KONTROL": "TUTAR satırı ABD 2020-22'de KAT_PUAN > 1 ve alt > 1 -> KONTROLÜ GEÇER; değilse 'BİLİNENİN TEKRARI'",
  "piyasa": "aynı kalıp: keşif ve ABD 2020-22'de n >= 30 gün VE ay >= 12 VE KAT = P(YP | uç) / P(YP) > 1 ve alt > 1 VE ASİMETRİ = [P(YP) - P(DP)] uç - taban > 0 ve alt > 0 VE P15 farkı (uç - bütün günler) > 0 ve alt > 0 VE AVR iki dönemde üç nokta işareti > 0; BH ayrı aile",
  "GENEL": "en az bir hisse satırı TUTAR ve KONTROLÜ GEÇER ise 'AÇIK VERİDE ADAY (kasa açılmaz; KASA KURALI: tek iz kasa açmaz; ileri test)'; aksi 'YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde)'"
 },
 "birlesim": {
  "en_cok": 2,
  "tanim": "aday = tek başına KEŞİF uç %10 (bayrakta bayrak) satırı n >= 1000, ay >= 12, KAT alt > 1, ASİMETRİ alt > 0, TOPLAM FARK alt > 0 olan sütunlar; >= 2 aday varsa farklı iki sütunun uçlarının kesişimi (n >= 1000) içinden keşif KAT'ı en büyük çift; doğrulamada bir kez; < 2 aday ise birleşim kurulmaz"
 },
 "puan": {
  "L1_lambda": 0.001,
  "iter": 400,
  "tanim": "keşifte L1 lojistik Y10 ~ 21 hisse özelliği (keşif ort / std ile standart; eksik = 0), ortalama log kaybı + lambda |w|_1 (sabit kesişim cezasız), FISTA 400 adım; puan uç %10 / %2 = keşif puan dağılımının %90 / %98'i (AVR: AVR 2016-19 puan dağılımı); doğrulamada bir kez; 'karmaşık olan en iyi tek özelliği geçmiyorsa seçilmez' = ABD 2020-22 KAT'ı en iyi tek satırın ABD 2020-22 KAT'ından büyük VE TUTAR",
  "kontrol_model": "keşifte lojistik (Newton) Y10 ~ MOM_12_1 + F15 + KONUM120 + ATRP20 (standart, eksik = 0); KONTROL PUANI beşlik sınırları keşiften"
 },
 "kesik": "veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her pazar) + KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl, '2022-12-31')",
 "sira": "kod + sentetik test -> getirisiz sayım -> ön kayıt commit + push -> ik_kontrol_kapisi -> ADIM 1 (yalnız ABD 2016-19 sonuçları) -> yo_kesim.json + YO_KESIM.md commit + push -> ADIM 2 (bir kez) -> rapor"
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hücre (pazar x dönem) aynı evren; ATRP içi KAT ve ASİMETRİ aynı ATRP beşliğiyle (oynaklığın mekanik etkisi dışlanır); ADIM 1 kontrolleri aynı gün aynı ATRP beşliği; TOPLAM FARK aynı hissenin aynı dönem ortalamasına göre; kontrol özellikleri (MOM_12_1, F15, KONUM120, ATRP20, EK 27 ölçüleri) ve kontrol puanı beşliği içinde KAT (bilinenin tekrarı denetimi); D10 aynası mekanik üstünlüğü ölçer |
| K2 | geleceğe bakma | EVET | her özellik k barına kadarki barlardan (test: k + 1 ve sonrası bozulunca değerler aynı); piyasa özellikleri t satırına kadar; P2 d - 1'e kadar; giriş k + 1 açılışı; Y / R15 ayrı fonksiyonda ve ADIM 1'de yalnız ABD 2016-19 (assert); kesimler yalnız keşiften (assert); veri <= 2022-12-31 assert + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0, O/H/L/C sonlu > 0); bütün ölçüler hissenin kendi geçerli barlarında; 15 bar <= 30 takvim satırı; P2 bölünme / likidite alt %20 / fiyat-likidite alt sınırı dışı |
| K4 | tekilleştirme | EVET | hisse başına her 5 barda bir t (örtüşme azaltılır, kalkmaz); çıkarım ay kümeli bootstrap (günler bağımsız sayılmaz); n hisse-gün ve farklı ay ayrı yazılır; medyan R15 bilgi |
| K5 | giriş fiyatı | EVET | giriş = t + 1 barının açılışı (t kapanışı değil); P15 de d = t + 1 açılışından |
| K6 | veri birimi | EVET | OS / MI bölünme düzeltmeli açık kopya; getiriler oransal, yerel para; pazar içi karşılaştırma; P2 bölünme şüphesi günlerini dışlar |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı, iki taraf (Y10 ve D10) için de; raporda yazılır; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n >= 1.000 ve farklı ay >= 12 olmayan satır ÖLÇÜLEMEDİ; iki dönem + iki pazar; BH q 0,10 (40 satır aile); en kalabalık 3 ay payı her satırda |
| K9 | ön kayıt | EVET | YO_ON_KAYIT.md: YO_KOD_SHA, YO_ESIK_SHA, panel dosya sha'ları, SAYIM_SHA + getirisiz sayım + yorum noktaları; ADIM 1 ön kayıt commit + push'tan sonra (kapı: kontrol + sha + commit + temiz ağaç); ADIM 2 yo_kesim.json commit'inden sonra (kapı); ikinci koşu durur |
| K10 | ayrıştırma | EVET | panel şeması (sütunlar) ve satır sayıları ön kayıttakiyle aynı (sayım sha); özellik tanımları sentetik elle hesaplanmış örneklerle; dokunma mantığı MUM_IZI_GOZ.gz_olc_bir ile rastgele sentetik serilerde birebir |
| K11 | yeniden üretim | EVET | keşif satırları ADIM 1 ve ADIM 2'de aynı kodla (eşit olmalı, DUR); rapordan önce >= 3 satır panel dosyalarından bağımsız kısa kodla yeniden üretilir |
| K12 | ifade | EVET | 'iz / aday' sözü yalnız hüküm kuralıyla; oynaklıkla açıklanan satır 'YALNIZ OYNAKLIK'; keşifte iyi doğrulamada değil -> 'TEK DÖNEM (tutmadı)'; sayı ile yorum ayrı cümlede; evren bugün yaşayanlar |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_yo); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(ön kayıt anında yok)
