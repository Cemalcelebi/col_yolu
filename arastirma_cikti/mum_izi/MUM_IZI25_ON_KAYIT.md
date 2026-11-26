# MUM_IZI25 ÖN KAYIT — KODUN SEÇTİĞİ BÖLGELER: rastgele gün tabanı, zamanlama / seçim, piyasa tahmini (2026-11-26T17:31:18Z)

İş tanımı MUM_IZI25_IS_TANIMI.md (1, 2, 2b, 3. bölüm) ve MUM_IZI23_EK_KURAL.md GÜNCELLEME. Bu dosya rastgele gün, T2, PİYASA(t) ve PİYASA15 getirileri hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler ve okuma kuralları sonra değişmez (değişirse SAPMA). Olay R15'leri EK 24 / EK 23 çıktılarından (daha önce yayımlandı); bu dosyadaki sayım getirisizdir. Evren bugün yaşayan hisseler (olay da taban da yukarı yanlı). Dönem içi piyasa yönü tabanda da var. KASA açılmaz (veri <= 2022-12-31).

## Mühürler

KOD25_SHA: 5889c8f670e8f905f6b38fa772b95751949d20b74c8d70b14625fdd9ce9094e1
ESIK25_SHA: d11c6d2f3154b8be0c332f46ed5113257e5fa285923fff818a27046aa038b207
ESIK24_SHA: 9ed1542a127183edfe8a014173ef4bc37b9222a17a5bdf741c4770552fc585eb
GZ_KOD_SHA: f0b0381a4eabe14a015dc6eb929fcc34a1d95d2a399412cc05a5620c4ffb68d5
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
OLAY24_SHA: 7fd6439b8eebff16ce8ff37d633a358a5ee7629bd92c9c05af0f76ec486ac96a
SONUC24_SHA: 09f08fd27bf9192c5fb0a88d3765bd17194de6a3073932ee1b98347119acf140
OLAY23_SHA: 856c2bdce461003e5ff342fde2f8e7e6c15b95f877e8e9fef9e98467752fcbd8
IS_TANIMI25_SHA: 48d20ed3dd4f7928151643bcdea3d9b149d92d62b676b906a6d54f001cba8a54
EK_KURAL23_SHA: f09092c47c5bcb27ea9913d05af4c57ab7927c35a748fc3880aab2741b5ce94f
SAYIM25_SHA: d8a4cc2c4b181a64e8db9deb7c7308ba43493cd8d54723acf6869a67de063683

- MUM_IZI_HAVUZ.py commit'i: 7f3e5d5545d2e73819d0c5c2087f4c0f032f5806 2026-11-26T17:29:50+00:00

## GETİRİSİZ SAYIM (yalnız olay / gün sayıları, uygun gün sayıları, takvim durumları; getiri hesaplanmadı)

### Örneklem x hücre (ölçülen olaylar; giriş ayına göre)

| örneklem | zaman | hücre | n (ölçülen) | farklı ay | en kalabalık 3 ay payı (aylar) | T1 uygun < 30 |
|---|---|---|---|---|---|---|
| KAPILI | gunluk | hepsi | 256 | 61 | 0,207 (2020-10 26, 2021-08 14, 2016-06 13) | 0 |
| KAPILI | gunluk | ABD|d1619 | 64 | 25 | 0,422 (2016-06 12, 2018-05 8, 2019-04 7) | 0 |
| KAPILI | gunluk | ABD|d2022 | 75 | 17 | 0,480 (2020-10 19, 2021-06 9, 2020-07 8) | 0 |
| KAPILI | gunluk | AVR|d1619 | 11 | 9 | 0,455 (2017-09 2, 2017-02 2, 2019-03 1) | 0 |
| KAPILI | gunluk | AVR|d2022 | 6 | 6 | 0,500 (2022-01 1, 2020-09 1, 2020-08 1) | 0 |
| KAPILI | gunluk | BIST|d1619 | 39 | 22 | 0,282 (2019-01 5, 2019-02 3, 2019-11 3) | 0 |
| KAPILI | gunluk | BIST|d2022 | 61 | 16 | 0,426 (2021-08 11, 2020-09 8, 2020-10 7) | 0 |
| KAPILI | gunluk | ABD|o16 | 0 | 0 | - () | 0 |
| KAPILI | gunluk | AVR|o16 | 0 | 0 | - () | 0 |
| KAPILI | gunluk | BIST|o16 | 0 | 0 | - () | 0 |
| KAPILI | haftalik | hepsi | 127 | 79 | 0,118 (2005-08 6, 2010-04 5, 2004-12 4) | 0 |
| KAPILI | haftalik | ABD|d1619 | 13 | 11 | 0,385 (2017-04 2, 2017-10 2, 2017-02 1) | 0 |
| KAPILI | haftalik | ABD|d2022 | 8 | 7 | 0,500 (2022-04 2, 2021-03 1, 2020-02 1) | 0 |
| KAPILI | haftalik | AVR|d1619 | 3 | 2 | 1,000 (2018-01 2, 2017-07 1) | 0 |
| KAPILI | haftalik | AVR|d2022 | 1 | 1 | 1,000 (2021-09 1) | 0 |
| KAPILI | haftalik | BIST|d1619 | 10 | 8 | 0,500 (2019-11 2, 2019-09 2, 2017-08 1) | 0 |
| KAPILI | haftalik | BIST|d2022 | 11 | 7 | 0,636 (2022-07 3, 2022-09 2, 2022-05 2) | 0 |
| KAPILI | haftalik | ABD|o16 | 71 | 43 | 0,197 (2005-08 6, 2010-04 4, 2005-01 4) | 0 |
| KAPILI | haftalik | AVR|o16 | 10 | 10 | 0,300 (2004-11 1, 2009-11 1, 2005-02 1) | 0 |
| KAPILI | haftalik | BIST|o16 | 0 | 0 | - () | 0 |
| KAPILI_DUY | gunluk | hepsi | 305 | 63 | 0,223 (2020-10 36, 2016-06 16, 2021-08 16) | 0 |
| KAPILI_DUY | gunluk | ABD|d1619 | 77 | 25 | 0,429 (2016-06 15, 2019-04 10, 2018-05 8) | 0 |
| KAPILI_DUY | gunluk | ABD|d2022 | 97 | 17 | 0,536 (2020-10 29, 2021-06 12, 2020-07 11) | 0 |
| KAPILI_DUY | gunluk | AVR|d1619 | 12 | 9 | 0,500 (2017-02 3, 2017-09 2, 2019-03 1) | 0 |
| KAPILI_DUY | gunluk | AVR|d2022 | 8 | 8 | 0,375 (2022-01 1, 2021-06 1, 2020-09 1) | 0 |
| KAPILI_DUY | gunluk | BIST|d1619 | 41 | 24 | 0,268 (2019-01 5, 2019-02 3, 2019-11 3) | 0 |
| KAPILI_DUY | gunluk | BIST|d2022 | 70 | 17 | 0,414 (2021-08 12, 2022-03 9, 2020-09 8) | 0 |
| KAPILI_DUY | gunluk | ABD|o16 | 0 | 0 | - () | 0 |
| KAPILI_DUY | gunluk | AVR|o16 | 0 | 0 | - () | 0 |
| KAPILI_DUY | gunluk | BIST|o16 | 0 | 0 | - () | 0 |
| KAPILI_DUY | haftalik | hepsi | 141 | 85 | 0,113 (2005-08 6, 2010-04 6, 2004-12 4) | 0 |
| KAPILI_DUY | haftalik | ABD|d1619 | 14 | 11 | 0,429 (2017-04 2, 2017-10 2, 2017-12 2) | 0 |
| KAPILI_DUY | haftalik | ABD|d2022 | 8 | 7 | 0,500 (2022-04 2, 2021-03 1, 2020-02 1) | 0 |
| KAPILI_DUY | haftalik | AVR|d1619 | 3 | 2 | 1,000 (2018-01 2, 2017-07 1) | 0 |
| KAPILI_DUY | haftalik | AVR|d2022 | 1 | 1 | 1,000 (2021-09 1) | 0 |
| KAPILI_DUY | haftalik | BIST|d1619 | 11 | 8 | 0,545 (2019-09 3, 2019-11 2, 2017-08 1) | 0 |
| KAPILI_DUY | haftalik | BIST|d2022 | 15 | 8 | 0,533 (2022-08 3, 2022-07 3, 2021-11 2) | 0 |
| KAPILI_DUY | haftalik | ABD|o16 | 79 | 48 | 0,190 (2005-08 6, 2010-04 5, 2005-01 4) | 0 |
| KAPILI_DUY | haftalik | AVR|o16 | 10 | 10 | 0,300 (2004-11 1, 2009-11 1, 2005-02 1) | 0 |
| KAPILI_DUY | haftalik | BIST|o16 | 0 | 0 | - () | 0 |
| KAPISIZ | gunluk | hepsi | 4245 | 83 | 0,119 (2021-10 193, 2020-10 159, 2019-01 152) | 0 |
| KAPISIZ | gunluk | ABD|d1619 | 1626 | 48 | 0,184 (2019-01 111, 2019-10 109, 2017-09 79) | 0 |
| KAPISIZ | gunluk | ABD|d2022 | 1484 | 35 | 0,283 (2021-10 169, 2020-10 146, 2022-01 105) | 0 |
| KAPISIZ | gunluk | AVR|d1619 | 260 | 45 | 0,227 (2017-12 23, 2019-01 20, 2018-11 16) | 0 |
| KAPISIZ | gunluk | AVR|d2022 | 162 | 32 | 0,235 (2022-01 18, 2021-04 11, 2022-03 9) | 0 |
| KAPISIZ | gunluk | BIST|d1619 | 370 | 46 | 0,222 (2017-12 30, 2019-09 28, 2019-11 24) | 0 |
| KAPISIZ | gunluk | BIST|d2022 | 343 | 33 | 0,245 (2022-03 41, 2020-01 23, 2021-11 20) | 0 |
| KAPISIZ | gunluk | ABD|o16 | 0 | 0 | - () | 0 |
| KAPISIZ | gunluk | AVR|o16 | 0 | 0 | - () | 0 |
| KAPISIZ | gunluk | BIST|o16 | 0 | 0 | - () | 0 |
| KAPISIZ | haftalik | hepsi | 1147 | 193 | 0,206 (2020-08 120, 2020-07 79, 2008-06 37) | 0 |
| KAPISIZ | haftalik | ABD|d1619 | 143 | 39 | 0,196 (2017-01 10, 2018-08 9, 2018-01 9) | 0 |
| KAPISIZ | haftalik | ABD|d2022 | 288 | 27 | 0,587 (2020-08 103, 2020-07 40, 2020-09 26) | 0 |
| KAPISIZ | haftalik | AVR|d1619 | 25 | 18 | 0,320 (2016-06 3, 2019-04 3, 2017-12 2) | 0 |
| KAPISIZ | haftalik | AVR|d2022 | 41 | 16 | 0,634 (2020-08 12, 2020-07 10, 2020-09 4) | 0 |
| KAPISIZ | haftalik | BIST|d1619 | 102 | 31 | 0,324 (2019-09 17, 2019-11 8, 2017-04 8) | 0 |
| KAPISIZ | haftalik | BIST|d2022 | 73 | 20 | 0,562 (2020-07 29, 2021-12 6, 2020-06 6) | 0 |
| KAPISIZ | haftalik | ABD|o16 | 413 | 110 | 0,194 (2008-06 33, 2006-11 25, 2005-07 22) | 0 |
| KAPISIZ | haftalik | AVR|o16 | 62 | 40 | 0,226 (2006-11 7, 2008-06 4, 2009-07 3) | 0 |
| KAPISIZ | haftalik | BIST|o16 | 0 | 0 | - () | 0 |
| GOZ_6_9 | gunluk | BENZİYOR | 19 | 16 | 0,316 (2022-04 2, 2020-10 2, 2021-09 2) | 0 |
| GOZ_6_9 | gunluk | KISMEN | 16 | 15 | 0,250 (2020-10 2, 2017-12 1, 2019-01 1) | 0 |
| GOZ_6_9 | gunluk | BENZEMİYOR | 20 | 13 | 0,500 (2020-10 6, 2018-08 2, 2021-06 2) | 0 |
| GOZ_6_9 | haftalik | BENZİYOR | 7 | 5 | 0,714 (2022-08 3, 2001-05 1, 2009-05 1) | 0 |
| GOZ_6_9 | haftalik | KISMEN | 8 | 8 | 0,375 (2007-11 1, 2005-01 1, 2006-11 1) | 0 |
| GOZ_6_9 | haftalik | BENZEMİYOR | 5 | 5 | 0,600 (2021-02 1, 2017-02 1, 2019-10 1) | 0 |
| GOZ_6_9 | birlikte | BENZİYOR | 26 | 20 | 0,308 (2022-08 4, 2022-04 2, 2020-10 2) | 0 |
| GOZ_6_9 | birlikte | KISMEN | 24 | 23 | 0,167 (2020-10 2, 2007-11 1, 2017-12 1) | 0 |
| GOZ_6_9 | birlikte | BENZEMİYOR | 25 | 17 | 0,400 (2020-10 6, 2017-02 2, 2018-08 2) | 0 |
| GOZ_7_9 | gunluk | BENZİYOR | 18 | 15 | 0,333 (2022-04 2, 2020-10 2, 2021-09 2) | 0 |
| GOZ_7_9 | gunluk | KISMEN | 12 | 11 | 0,333 (2020-10 2, 2021-09 1, 2022-03 1) | 0 |
| GOZ_7_9 | gunluk | BENZEMİYOR | 17 | 11 | 0,529 (2020-10 6, 2021-06 2, 2018-08 1) | 0 |
| GOZ_7_9 | haftalik | BENZİYOR | 4 | 2 | 1,000 (2022-08 3, 2010-04 1) | 0 |
| GOZ_7_9 | haftalik | KISMEN | 5 | 5 | 0,600 (2006-01 1, 2019-09 1, 2004-01 1) | 0 |
| GOZ_7_9 | haftalik | BENZEMİYOR | 2 | 2 | 1,000 (2017-12 1, 2011-03 1) | 0 |
| GOZ_7_9 | birlikte | BENZİYOR | 22 | 16 | 0,364 (2022-08 4, 2022-04 2, 2020-10 2) | 0 |
| GOZ_7_9 | birlikte | KISMEN | 17 | 16 | 0,235 (2020-10 2, 2021-09 1, 2022-03 1) | 0 |
| GOZ_7_9 | birlikte | BENZEMİYOR | 19 | 13 | 0,474 (2020-10 6, 2021-06 2, 2018-08 1) | 0 |

### T1: olay başına çekilebilen (uygun) gün sayısı

| örneklem / zaman | n | en az | %10 | medyan | %90 | en çok | < 30 | < 200 |
|---|---|---|---|---|---|---|---|---|
| KAPILI|gunluk | 256 | 91 | 624 | 708 | 973 | 992 | 0 | 3 |
| KAPILI|haftalik | 127 | 39 | 113 | 717 | 786 | 790 | 0 | 47 |
| KAPILI_DUY|gunluk | 305 | 91 | 619 | 708 | 974 | 992 | 0 | 4 |
| KAPILI_DUY|haftalik | 141 | 39 | 113 | 722 | 787 | 791 | 0 | 53 |
| KAPISIZ|gunluk | 4245 | 80 | 649 | 827 | 975 | 993 | 0 | 8 |
| KAPISIZ|haftalik | 1147 | 33 | 111 | 180 | 786 | 790 | 0 | 674 |

### T2: uygun (hisse, gün) çiftleri

| T2 hücresi | uygun (hisse, gün) çifti | hisse |
|---|---|---|
| gunluk|ABD|d1619 | 2954660 | 3494 |
| gunluk|ABD|d2022 | 2792998 | 4401 |
| gunluk|AVR|d1619 | 512995 | 544 |
| gunluk|AVR|d2022 | 407862 | 571 |
| gunluk|BIST|d1619 | 337762 | 377 |
| gunluk|BIST|d2022 | 284189 | 466 |
| haftalik|ABD|d1619 | 632214 | 3458 |
| haftalik|ABD|d2022 | 527249 | 4302 |
| haftalik|ABD|o16 | 1645072 | 2844 |
| haftalik|AVR|d1619 | 107599 | 540 |
| haftalik|AVR|d2022 | 76654 | 569 |
| haftalik|AVR|o16 | 322067 | 500 |
| haftalik|BIST|d1619 | 71266 | 377 |
| haftalik|BIST|d2022 | 53353 | 448 |

### Takvim (2b, günlük): SAYI durumlarına göre gün sayısı

| pazar | SAYI kaynağı | olay | dönem | SAYI = 0 gün | SAYI = 1-2 gün | SAYI >= 3 gün |
|---|---|---|---|---|---|---|
| ABD | KAPILI | 139 | d1619 | 813 | 166 | 27 |
| ABD | KAPILI | 139 | d2022 | 560 | 144 | 38 |
| ABD | KAPILI_DUY | 175 | d1619 | 796 | 165 | 45 |
| ABD | KAPILI_DUY | 175 | d2022 | 539 | 158 | 45 |
| ABD | KAPISIZ | 3113 | d1619 | 73 | 214 | 719 |
| ABD | KAPISIZ | 3113 | d2022 | 74 | 127 | 541 |
| AVR | KAPILI | 17 | d1619 | 974 | 51 | 0 |
| AVR | KAPILI | 17 | d2022 | 729 | 30 | 0 |
| AVR | KAPILI_DUY | 20 | d1619 | 971 | 54 | 0 |
| AVR | KAPILI_DUY | 20 | d2022 | 719 | 40 | 0 |
| AVR | KAPISIZ | 423 | d1619 | 463 | 399 | 163 |
| AVR | KAPISIZ | 423 | d2022 | 349 | 318 | 92 |
| BIST | KAPILI | 100 | d1619 | 863 | 128 | 12 |
| BIST | KAPILI | 100 | d2022 | 588 | 114 | 37 |
| BIST | KAPILI_DUY | 111 | d1619 | 853 | 138 | 12 |
| BIST | KAPILI_DUY | 111 | d2022 | 575 | 123 | 41 |
| BIST | KAPISIZ | 715 | d1619 | 424 | 348 | 231 |
| BIST | KAPISIZ | 715 | d2022 | 233 | 290 | 216 |

- Blok: {"gunluk|ABD": {"hisse": 4441, "takvim_gun": 2014}, "gunluk|AVR": {"hisse": 571, "takvim_gun": 2055}, "gunluk|BIST": {"hisse": 467, "takvim_gun": 1906}, "haftalik|ABD": {"hisse": 4441, "takvim_gun": 5787}, "haftalik|AVR": {"hisse": 572, "takvim_gun": 5905}, "haftalik|BIST": {"hisse": 467, "takvim_gun": 1906}}

## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)

1. '15 bardan yakın' = rastgele giriş barı ile bilinen bir bölgenin giriş barı arasında |fark| <= 14 bar (15 mumluk pencereler örtüşür); bilinen bölgeler = EK 24 havuzunun BÜTÜN olayları (KAPILI + KAPISIZ + ORAN_YOK, hariç dahil, ölçülemeyenler dahil) + göz ölçümü 205 bölge, aynı hisse ve aynı zaman dilimi.
2. T1 'aynı dönem' = olayın giriş tarihine göre dönemi (2016 öncesi / 2016-19 / 2020-22); rastgele girişin tarihi dönem içinde, 15. mumu dönem dışına taşabilir (olaylarla aynı kural), ama 2022-12-31'i aşamaz.
3. Rastgele gün 'geçerli' = giriş açılışı sonlu, > 0 ve > stop (olayın ölçülebilirlik kuralı aynen; giriş <= stop olan gün çekilmez). Yerine koymadan çekim; T1 için olay başına 200 (KAPISIZ dahil; vektörle hesaplandığı için 50'ye inilmedi); uygun < 30 ise olay T1'siz kalır ve sayılır.
4. T2 stop m = 20 (iş tanımı); T2 rastgele çiftleri de aynı dışlama ve ölçülebilirlik kuralıyla; T2 hücresi = zaman dilimi x pazar x dönem; T2 belirsizliği ay kümeli bootstrap'a katılır (T2 çekimleri kendi giriş aylarıyla, olaylardan bağımsız).
5. PİYASA(t): olayla aynı veri bloğu (günlükte günlük açık veri, haftalıkta haftalık bloğun günlük verisi), olayın giriş günü açılışında işlem gören bütün hisseler, olayın 15. mum gününe kadar son geçerli kapanış (gz_es_grup R tanımı, kova / stop yok), olayın hissesi ve AYNI GÜN girişli bilinen bölgesi olan hisseler hariç (iki zaman dilimi birlikte); günlükte 15. mum günü ile haftalıkta 15. haftanın son günü olayınki.
6. Tablolar TAM kümeyle (R15, T1, PİYASA(t), T2 hepsi olan olaylar); TOPLAM_T2 = ZAMANLAMA + SEÇİM özdeşliği olay başına denetlenir. 'Hepsi birlikte' her olayı kendi hücresinin T2'siyle karşılaştırır.
7. Göz ölçümü sınıfı 'sinif' sütunu (EVET = BENZİYOR, KISMEN, HAYIR = BENZEMİYOR); set 8 s11 duyarlılığı (sinif_duy) kullanılmaz. KISMEN KABUL kararı set 6-9 (zaman dilimleri birlikte) ile; set 7-9 bilgi. Göz satırlarının d5'i 'd5_tum' (haftalıkta günlük veriyle aynı kural).
8. 2b SAYI ana = KAPILI ANA günlük olaylar (EK 24 ana örnekle tutarlı; ölçülebilirlikten bağımsız sayılır); KAPILI hepsi duyarlılık, KAPISIZ ANA kontrol. Takvim = pazarın günlük verisindeki işlem günlerinin birleşimi; 'son 5 işlem günü' = takvimde g - 4 .. g; PİYASA15'te olay dışlaması YOK (iş tanımı 'bütün hisseler'); bootstrap kümesi g'nin ayı; dönem g + 1 tarihine göre.
9. 'Pazar son 20 günde %5'ten fazla düşmüş' = DUS20(g) < -0,05 (eşit ağırlıklı, kapanış en çok 5 gün ileri taşınır); bilgi satırı olarak DÜŞÜŞ günleri içinde / dışında (SAYI >= 1) - (SAYI = 0) da yazılır (hükme girmez).
10. Okuma etiketleri iş tanımı 3. bölüm ve 2b aynen; 'iki pazarda' için AVR'de de iki dönemde alt ucu > 0 aranır; iki dönemde de üst ucu < 0 ise 'GÖSTERİLEMEDİ (ters yönde)'. Ortalama yanında medyan; okuma ortalama ve ay kümeli aralıkla.

## Tanımlar (HV25_ESIK; sha yukarıda)

```
{
 "surum": "HV25-1.0",
 "tohum": 2511,
 "tohum_tanim": "np.random.default_rng([2511, tür, crc32(anahtar)]); tür 1 = T1 (anahtar 'zaman|pazar|sembol|tarih|kaynak'), 2 = T2 (anahtar 'zaman|pazar|dönem'), 3 = olay bootstrap'ı (anahtar tablo adı), 4 = T2 bootstrap'ı (anahtar 'zaman|pazar|dönem'), 5 = takvim bootstrap'ı (anahtar tablo adı); sıra bağımsız, tekrarlanabilir",
 "olcu": {
  "tanim": "olay ölçüsü GZ.gz_olc_bir AYNEN (EK 24 satırları; R15 / d5 / d10 olay csv'sinden; hv25_olc_dizi aynı tanımı vektörle yeniden üretir, olay satırlarıyla R15 / E0 / stop / d5 / d10 birebir, değilse DUR); rastgele gün aynı tanım: karar barı t (bölge sonunun yerine), giriş = t + 1 barının açılışı (haftalıkta haftanın ilk günü), R15 = t + 15 barının kapanışı / giriş - 1, stop = t - m + 1 .. t barlarının dibi x 0,98, hedef +%5 / +%10 günlük High >= giriş x (1 + x) ilk gün, Low <= stop ilk günden ÖNCE (aynı gün stop önce; GZ / G2.k17_dokunma aynen)",
  "ufuk": 15,
  "stop_carpan": 0.98
 },
 "uygun": {
  "tanim": "rastgele karar barı t uygun <=> t - m + 1 >= 0; t + 15 veri içinde ve t + 15 barının tarihi <= 2022-12-31 (pencere kesiği); giriş tarihi (t + 1 barının ilk günü) olayın DÖNEMİ içinde (giriş tarihine göre; 15. mum dönem dışına taşabilir, olaylarla aynı); giriş açılışı sonlu, > 0 ve > stop (olaylarla aynı ölçülebilirlik); |(t + 1) - k| >= 15 her k için, k = aynı hisse aynı zaman diliminde BİLİNEN BÖLGELERİN giriş barları (EK 24 havuzunun bütün olayları: KAPILI + KAPISIZ + ORAN_YOK, hariç dahil, ölçülemeyenler dahil; k = bölge sonu barı + 1) + göz ölçümü 205 bölge; '15 bardan yakın' = |fark| <= 14 (15 mumluk pencereler örtüşür)",
  "yakin_bar": 15
 },
 "T1": {
  "cekim": 200,
  "en_az": 30,
  "yerine_koyma": false,
  "tanim": "olay başına aynı hisse, aynı zaman dilimi, aynı dönem, aynı m: uygun barlardan yerine koymadan 200 (uygun < 200 ise hepsi); uygun < 30 ise T1 yok (olay T1 tablolarına girmez; sayısı yazılır); T1_R15 = çekimlerin R15 ortalaması, T1_d5 / T1_d10 = hedef payları; çekim sayısı KAPISIZ dahil her olayda 200 (hesap vektörle; 50'ye inilmedi)"
 },
 "T2": {
  "cekim": 5000,
  "m": 20,
  "yerine_koyma": false,
  "tanim": "hücre (zaman dilimi x pazar x dönem) başına evrenin bütün (hisse, karar barı) uygun çiftlerinden (m = 20, aynı uygunluk ve dışlama kuralı) yerine koymadan 5.000 (az ise hepsi); R15 ortalaması / medyanı, +%5 / +%10 payı; hücre başına tek sayı; belirsizliği ay kümeli bootstrap ile (çekimlerin giriş ayları) farka katılır"
 },
 "piyasa": {
  "en_az_hisse": 5,
  "tanim": "PİYASA(t) = aynı pazarın (aynı veri: günlükte günlük açık veri, haftalıkta haftalık blok günlük verisi) olayın giriş günü açılışında işlem gören (açılış sonlu > 0) bütün hisselerinin, olayın giriş gününden olayın 15. mum gününe kadar R'si (son geçerli kapanış / giriş açılışı - 1; gz_es_grup'un R tanımı, kovasız) eşit ağırlıklı ortalaması; hariç: olayın hissesi ve o pazarda AYNI GÜN girişli bilinen bölgesi olan hisseler (EK 24 havuzunun bütün olayları, iki zaman dilimi + göz 205); stop / kova şartı yok; < 5 hisse ise yok"
 },
 "fark": {
  "TOPLAM_T1": "R15 - T1_R15 (olay başına)",
  "TOPLAM_T2": "R15 - T2(hücre)",
  "ZAMANLAMA": "PİYASA(t) - T2(hücre)",
  "SECIM": "R15 - PİYASA(t)",
  "ozdeslik": "TOPLAM_T2 = ZAMANLAMA + SECIM (olay başına; denetim 1e-12, değilse DUR)",
  "tam_kume": "tablolar R15, T1, PİYASA(t) ve T2 hepsi olan olaylarla (TAM küme); dışarıda kalanlar sayılır; EK 24 eşli farkı (fark) aynı kümenin eşli olaylarında yanında yazılır"
 },
 "boot": {
  "B": 10000,
  "kume": "giriş ayı (YYYY-AA)",
  "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık), ortalama = ağırlıklı toplam / ağırlıklı sayı; T2 içeren farklarda her tekrarda T2 de kendi çekimlerinin giriş ayları üzerinden bağımsız yeniden örneklenir; %95 = 2,5 / 97,5 yüzdelik"
 },
 "ornek": {
  "KAPILI": "EK 24 KAPILI ANA (ana örnek)",
  "KAPILI_DUY": "EK 24 KAPILI hepsi (hariç dahil; duyarlılık)",
  "KAPISIZ": "EK 24 KAPISIZ ANA (kontrol)",
  "GOZ_6_9": "mum_izi23_olay.csv set6-set9 (gerçek ölçekle işaretlenen), sınıf = 'sinif' sütunu (EVET = BENZİYOR, KISMEN, HAYIR = BENZEMİYOR), zaman dilimleri birlikte (ayrıca zaman dilimine göre bilgi)",
  "GOZ_7_9": "set7-set9 (kapı havuzu), aynı sınıflar"
 },
 "hucre": {
  "karar": [
   "ABD|d1619",
   "ABD|d2022",
   "AVR|d1619",
   "AVR|d2022"
  ],
  "bilgi": [
   "BIST|d1619",
   "BIST|d2022",
   "ABD|o16",
   "AVR|o16",
   "BIST|o16"
  ],
  "atama": "giriş tarihine göre (HV_ESIK['hucre']['donem']); ayrıca zaman dilimine göre 'hepsi birlikte'"
 },
 "okuma": {
  "MUTLAK_KARLI": "n >= 30 VE farklı ay >= 12 VE TOPLAM FARK (T1) ort > 0 ve ay kümeli alt ucu > 0; aralık sıfırı içeriyorsa AYRIŞMIYOR; üst ucu < 0 ise RASTGELE GÜNDEN KÖTÜ; n ya da ay yetmezse ÖLÇÜLEMEDİ",
  "ZAMANLAMA": "aynı n / ay şartıyla ZAMANLAMA ort > 0 ve alt ucu > 0 -> ZAMANLAMA VAR; üst ucu < 0 -> ZAMANLAMA TERS (bilgi); aralık sıfırı içeriyorsa AYRIŞMIYOR",
  "SECIM": "bilgi: aynı kural, etiket SEÇİM + / SEÇİM - / AYRIŞMIYOR",
  "az_donem": "en kalabalık 3 ayın olay payı > 0,30 -> 'az sayıda döneme dayanıyor' notu",
  "n_min": 30,
  "ay_min": 12,
  "az_donem_pay": 0.3
 },
 "goz": {
  "kismen_kabul": "KISMEN sınıfı (set 6-9, zaman dilimleri birlikte) TOPLAM FARK (T1) ay kümeli %95 aralık kuralıyla 'MUTLAK KÂRLI' (alt ucu > 0; n ve ay şartı aranmaz; n < 30 -> 'ÖRNEKLEM YETERSİZ' notu) <=> KISMEN KABUL; set 7-9 aynı kuralla BİLGİ (ayrışırsa ikisi de yazılır)",
  "esli": "MUM_IZI23_EK_KURAL eşli okuma (bilgi): sınıfın EK 23 eşli farkı (csv 'fark') ortalaması, basit bootstrap %95 (10.000, tohum 2311): alt > 0 SONRASI İYİ, üst < 0 SONRASI KÖTÜ, aksi GÖSTERİLEMEDİ",
  "tohum_esli": 2311
 },
 "takvim": {
  "pazar": [
   "ABD",
   "AVR",
   "BIST"
  ],
  "karar_pazar": [
   "ABD",
   "AVR"
  ],
  "zaman": "gunluk",
  "takvim": "pazarın günlük verisindeki bütün işlem günlerinin birleşimi (sıralı)",
  "SAYI": "SAYI(g) = bölge sonu tarihi takvimde g - 4 .. g aralığında (son 5 işlem günü, g dahil; bölge sonu <= g) olan olay sayısı; ana: KAPILI ANA günlük olaylar (ölçülebilirlikten bağımsız); duyarlılık: KAPILI hepsi; kontrol: KAPISIZ ANA",
  "PIYASA15": "PİYASA15(g) = g + 1 (takvimde sonraki gün) açılışında işlem gören bütün hisselerin (olay dışlaması YOK) g + 1 .. g + 15 takvim günlerinde son geçerli kapanış / g + 1 açılışı - 1, eşit ağırlıklı ortalama; < 5 hisse ise gün yok",
  "gun": "g + 1 giriş tarihi 2016-01-01 .. 2022-12-31 ve g + 15 takvim günü tarihi <= 2022-12-31; g >= 20; dönem g + 1 tarihine göre (2016-19, 2020-22); bootstrap kümesi g'nin ayı",
  "durum": [
   "SAYI = 0",
   "SAYI = 1-2",
   "SAYI >= 3"
  ],
  "farklar": [
   "(SAYI >= 1) - (SAYI = 0)",
   "(SAYI >= 3) - (SAYI = 0)"
  ],
  "dusus": "DUS20(g) = bütün hisselerin (kapanış 5 güne kadar ileri taşınmış) Kapanış(g) / Kapanış(g - 20) - 1 eşit ağırlıklı ortalaması; DÜŞÜŞ günü <=> DUS20 < -0,05; satır: DÜŞÜŞ günlerinde PİYASA15 (gün, ort, medyan, artı payı) ve DÜŞÜŞ - öteki günler farkı [ay kümeli %95]; bilgi: DÜŞÜŞ günleri içinde ve dışında ayrı (SAYI >= 1) - (SAYI = 0)",
  "okuma": "ABD'de iki dönemde de (SAYI >= 1) - (SAYI = 0) > 0 ve alt ucu > 0 -> 'PİYASA YÜKSELİŞİNİ ÖNCELİYOR' (AVR'de de iki dönemde alt ucu > 0 ise 'iki pazarda'); yalnız bir dönemde -> 'TEK DÖNEM'; aksi -> 'GÖSTERİLEMEDİ' (iki dönemde de üst ucu < 0 ise 'GÖSTERİLEMEDİ (ters yönde)'); AVR ve BIST kendi satırında aynı kuralla (bilgi); KAPISIZ sayısıyla aynı tablo (kontrol)"
 },
 "kesik": "veri en büyük tarihi <= 2022-12-31 (hv_kesik_kapi her blok) + KASA.kasa_kapisi (EK 24 ile aynı dosyalar); rastgele gün ve takvim günü 15. barı <= 2022-12-31"
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | üç taban önceden sabit: T1 aynı hisse rastgele gün (aynı dönem, aynı m, aynı stop / giriş / ufuk geometrisi), T2 aynı pazar / dönem / zaman dilimi rastgele (hisse, gün), PİYASA(t) aynı giriş günü bütün pazar (olaylı hisseler hariç); EK 24 eşli farkı (aynı gün aynı kova) yanında yazılır; KAPISIZ aynı aday kuralının kontrolü; DÜŞÜŞ günü satırı mekanik üstünlük (düşüş sonrası toparlanma) kontrolü |
| K2 | geleceğe bakma | EVET | olay girişi bölge sonundan sonraki bar açılışı (EK 24); rastgele günde stop t'ye kadarki m bar; takvimde SAYI(g) yalnız bölge sonu <= g (test); PİYASA15 g + 1 açılışından; DUS20 g'ye kadar; veri <= 2022-12-31 assert + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0) aynen; haftalık tamamlanmış ISO haftaları (MV.mv_haftalik_panel); rastgele gün girişinde açılış sonlu > 0 |
| K4 | tekilleştirme | EVET | olaylar EK 24'te tekil (15 bar); rastgele günler bilinen bölgelerin girişine <= 14 bar yakınsa dışlanır; T1 çekimi yerine koymadan; ortalama yanında medyan; çıkarım ay kümeli (günler / olaylar bağımsız sayılmaz) |
| K5 | giriş fiyatı | EVET | giriş = sonraki ilk bar açılışı (olay, rastgele gün, takvim g + 1); giriş <= stop ölçülmez (olay ve rastgele gün aynı) |
| K6 | veri birimi | EVET | MI bölünme düzeltmeli fiyatlar (EK 24 aynen); getiriler oransal, yerel para; pazar içi karşılaştırma |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: olay da taban da yukarı yanlı; rastgele gün tabanı aynı evrenden olduğu için yanlılık farkta kısmen düşer, kalkmaz; raporda yazılır; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n >= 30 VE farklı ay >= 12 şartı (okuma); en kalabalık 3 ay payı her tabloda; iki dönem ve iki pazar ayrı; göz sınıfları n < 30 -> ÖRNEKLEM YETERSİZ; küçük hücreden 'bulgu' denmez |
| K9 | ön kayıt | EVET | MUM_IZI25_ON_KAYIT.md: KOD25_SHA, ESIK25_SHA, girdi sha'ları, SAYIM25_SHA + getirisiz sayım + yorum noktaları; hesap ön kayıt commit + push'tan sonra; hv25_kapi: ik_kontrol_kapisi + sha + commit + temiz ağaç + sayım eşitliği |
| K10 | ayrıştırma | EVET | girdi şeması (sütunlar) denetlenir; EK 24 satırında t = takvimde bölge sonu (DUR); göz satırlarında bölge sonu takvimde (DUR); getirisiz aşamada giriş / 15. mum tarihi, E0 ve stop olay satırlarıyla birebir (DUR); hesapta R15 / d5 / d10 birebir (DUR) |
| K11 | yeniden üretim | EVET | hv25_olc_dizi = gz_olc_bir (sentetik test + bütün olay satırları); TOPLAM_T2 = ZAMANLAMA + SECIM (DUR); rapordan önce >= 2 hücre olay csv'sinden bağımsız kısa kodla yeniden üretilir |
| K12 | ifade | EVET | başlık 'KODUN SEÇTİĞİ BÖLGELER'; 'kalıbın sonucu' denmez; 'mutlak kârlı / zamanlama var' yalnız okuma kuralıyla; sayı ile yorum ayrı cümlede; dönem içi piyasa yönü tabanda da var |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_hv) korunur; EK 24 fonksiyonları ve çıktıları değişmez (test); MUM_IZI_HAKEM / GOZ / GOZ2 ve defter dosyaları değişmez; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(ön kayıt anında yok)
