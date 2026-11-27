# ES_YENIDEN ÖN KAYIT — eski 'iz değil'lerin rastgele güne göre yeniden okunması, birinci parti (27 Kasım 2026)

Kod: ES_YENIDEN.py sha 0395f3665dba328e (eşik / kayıt tanımı sha 59a863bad008a0a6). İş tanımı: ES_YENIDEN_IS_TANIMI.md. Bu dosya ölçümden ÖNCE commit + push edilir; ölçüm (`python ES_YENIDEN.py olcum`) bu dosyanın commit'ini, push'unu, kontrol kapısını ve kod sha'sını denetler, BİR KEZ koşar. Bu bir AYNI VERİDE YENİDEN OKUMADIR (kör değil).

## 1. Seçim (getirisiz)

Kural: envanter Liste 1 sırası (envanterin 'Dosya satırı' sütunu, büyükten küçüğe = olay sayısı sırası), kapalı konu değil, kayıt tarihi < 2026-11-26, olay >= 300, dosya okunabilir ve giriş kuralı sabit ufuklu; en çok 20; aynı olay kümesini paylaşan kayıtlar tek satır.

| # | Ç | Ad | Kaynak veri | Kural | H | Veri kesiği | Hücreler (giriş günü) | Olay satırı | Paylaşan |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Ç209 | KART TUR 2 (geniş tezgâh, KASA 2): 14 kart | V2 (ABD, AVR) | gecerli | 15 | 2024-12-31 | acik_d1 2001-01-01..2007-12-31; acik_d2 2008-01-01..2015-12-31; acik_d3 2016-01-01..2023-12-31; blok 2024-01-01..2024-12-31 | 493952 | — |
| 2 | Ç205 | KART TUR 1 (KASA yürüyen ileri test): 11 kart | V (ABD, AVR) | gecerli | 15 | 2023-12-31 | acik 2016-01-01..2022-12-31; birikimli 2023-01-01..2023-12-31 | 104444 | — |
| 3 | Ç206 | ÖLÇÜ SINAMASI: bilinen etki bacakları (MOM, STREV, HIGH52) | V (ABD, AVR) | gecerli | 15 | 2023-12-31 | d1 2016-01-01..2019-12-31; d2 2020-01-01..2023-12-31 | 60707 | — |
| 4 | Ç226 | ÜÇ İZ BİRLİKTE BİLANÇO OLAYINDA (UC_IZ2) | V2 (ABD) | gecerli | 60 | 2022-12-31 | d1619 2016-01-01..2019-12-31; d2022 2020-01-01..2022-12-31 | 29464 | — |
| 5 | Ç204 | CETVEL2 R15 yeniden koşusu (Y1 tabanı + Ç194-Ç202 hipotezleri + hakem turu kolları) | V (ABD, AVR, BIST) | gecerli | 15 | 2026-08-31 | egitim 2016-01-01..2022-12-31; sinama 2023-01-01..2026-08-31 | 681788 | Ç202, Ç190, Ç192, Ç193, Ç194, Ç195, Ç196, Ç197, Ç198, Ç199, Ç201 |
| 6 | Ç191 | YAPI_HEDEF 2. tur: Y6 / Y8 / Y8B (Y7 n = 0) | V (ABD, AVR, BIST) | gecerli | 15 | 2026-08-31 | 2016-22 2016-01-01..2022-12-31; 2023 2023-01-01..2023-12-31; 2024-26 2024-01-01..2026-08-31 | 4530 | — |
| 7 | Ç99 | KAP içeriden alım (K27): net alım, büyük alım, çölde alım | V (BIST) | fi_olcut | 60 | 2026-08-31 | 2023 2023-01-01..2023-12-31; 2024-26 2024-01-01..2026-08-31 | 839 | — |
| 8 | Ç189 | S+ v2 TAM GİRİLİR (TAM_DIP) | V (ABD, AVR, BIST) | oc | 60 | 2026-08-31 | 2016-22 2016-01-01..2022-12-31; 2023 2023-01-01..2023-12-31; 2024-26 2024-01-01..2026-08-31 | 1747 | — |

Kaynak tanımları (giriş kuralı / ufuk / hücre kayıttan):

- Ç209: KART_TUR2.K2_ESIK['hucre'] (acik_d1/d2/d3) + KASA_DEFTERI 2024Q1-Q4; ufuk 15 = ilk karar ufku (15 / 30); R = dosya 'R'; durum 'olculdu' + 'essiz' (eşsiz olay da olaydır; eş yalnız E tabanının şartı). Eski hüküm: ÖLÇÜLEMEDİ (KART TUR 2; 12 kart) / açık veride kartların FARK'ı ~0.
- Ç205: KART_TUR1.KT_ESIK['hucre'] (acik 2016-22, blok_bas 2023-01-01; KASA 2023Q1-Q4 açık); ufuk 15; kart bayrakları F_U (KT00) ve F_KT01-F_KT10; R = dosya 'r15'. Eski hüküm: ÖLÇÜLEMEDİ (KART TUR 1; hiçbir kart tutmadı).
- Ç206: OLCU_SINAMA.OS_ESIK['donem'] (d1 2016-19, d2 2020-23; açık veri <= 2023-12-31); H 15 = ilk ufuk (15 / 30 / 60); kol = 'bacak'; R = dosya 'R'. Eski hüküm: HİÇBİR ÖLÇÜ GEÇMEDİ 0 / 36 (hat testi).
- Ç226: UC_IZ2.UC2_ESIK['donem'] + UC2_KESIK 2022-12-31; ufuk R60 = ilk karar ufku (R60, R15); kol = R / B / İ izi var (== 1) ve N >= 2 (birlikte); R = dosya 'R60'. Eski hüküm: İZ DEĞİL (güç yeterli).
- Ç204: CETVEL2.C2_ESIK['donem'] (egitim 2016-22, sinama 2023-01-01..2026-08-31); R15 (STOP YOK); kol = yk_TABAN 'Y1' (bütün satırlar), yk_TABAN_DS 'DS_ANA', öteki dosyalarda F_* == 1; R = dosya 'r15'. Eski hüküm: İZ DEĞİL / ÖLÇÜLEMEDİ (124 hipotez; KATKI+ 0, KATKI− 0).
- Ç191: YAPI_HEDEF: giriş = kırılım mumundan sonraki ilk geçerli bar açılışı ('giris'), 15 bar ufuk; dosyada R15 yok -> CETVEL2 R15 tanımıyla fiyattan (Ç204 yeniden koşu tanımı); kol = 'deneme' (Y6, Y8, Y8B). Eski hüküm: ÖLÇÜLEMEDİ (YAPI_HEDEF 2. tur Y6-Y8; yön aleyhte).
- Ç99: FON_IZI K27 FI_OLCUT (donem 2023 / 2024-26; giriş = 'giris' açılışı, r60); kol = 'olay' alim / buyuk / col_alim ('satim' beklenen yönü eksi olduğu için alınmadı); R = dosya 'r60'. Eski hüküm: İçeriden alım bildirimi olumlu bilgi taşımıyor (eşlerin gerisinde).
- Ç189: FITIL_V2 -> ORTAK_CETVEL r60 (OC.oc_panel: geçerli barlar, birleşik takvim, giriş açılışı -> 60. takvim satırı kapanışı, 5 gün ffill, kriz 2026-08-31); hücre = pazar x 'donem'; R = dosya 'r60'. Eski hüküm: ÖLÇÜLEMEDİ (TAM_DIP; hiçbir hücrede alt uç > 0).
- Paylaşılan küme (Ç204): Ç204 yeniden koşusu Ç194-Ç202'nin olaylarını CETVEL2 R15 ile yeniden ölçtü (yk_C194..C202); Ç190 Y1 = yk_TABAN; Ç192 (OLUR etiketi) ve Ç197-Ç199 (puan / devir) Y1 kümesinin alt kümeleri (yk_C197-C199); Ç193 Y9 = Ç196 G2 (yk_C196 F_S1 ailesi).

Atlananlar (Liste 1 sırasıyla):

| Ç | Neden |
|---|---|
| Ç255 | tarih 2026-11-26 >= 26 Kasım (zaten rastgele güne göre / iş tanımı dışı) |
| Ç47 | kapalı konu (Öbek/D13 (COL_OZET) |
| Ç72 | olay kümesi kapalı Ç47 (D13 / Öbek, COL_OZET kapanan) ile aynı; giriş kuralı (alim_a / alim_b) dosyada sabit ufuklu değil |
| Ç91 | kapalı konu (Stop/çıkış ve 90+ (COL_OZET K19) |
| Ç92 | kapalı konu (Sağ ayak / çöl (COL_OZET K19-K20) |
| Ç93 | kapalı konu (Sağ ayak (COL_OZET) |
| Ç49 | kapalı konu (MUM_SUKUN (COL_OZET) |
| Ç227 | kapalı konu (Tespit geçerliliği yasağı (CLAUDE.md 25 Kas)) |
| Ç44 | kapalı konu (Öbek ek şart (COL_OZET kapanan) |
| Ç65 | kapalı konu (KAP fon girişi (COL_OZET) |
| Ç66 | kapalı konu (KAP fon yoğunlaşma (COL_OZET) |
| Ç50 | kapalı konu (MUM_SUKUN (COL_OZET) |
| Ç85 | kapalı konu (K18 vaka profili (COL_OZET) |
| Ç86 | kapalı konu (K18) |
| Ç87 | kapalı konu (K18) |
| Ç88 | kapalı konu (K18) |
| Ç89 | kapalı konu (K18) |
| Ç90 | kapalı konu (K18 + sektör rüzgârı) |
| Ç128 | kapalı konu (90+ şekil (kapalı) |
| Ç229 | kapalı konu (Tespit geçerliliği) |
| Ç136 | çıktı bariyer isabeti / değişken çıkışlı net getiri (y, net); sabit H ufuklu getiri yok, T1 aynı kuralla kurulamaz |
| Ç96 | kapalı konu (İki evre (COL_OZET) |
| Ç273 | tarih 2026-11-27 >= 26 Kasım (zaten rastgele güne göre / iş tanımı dışı) |
| Ç57 | kapalı konu (FON_IZI v1.1 (COL_OZET) |
| Ç138 | kapalı konu (90+ şekil (kapalı) |
| Ç146 | olay kümesi kapalı Ç138 (K55, 90+ şekil ölçüsü) ile aynı (K55_OLAYLAR) |
| Ç134 | çıktı bariyer isabeti / değişken çıkışlı net getiri (K51 eşleşmiş kontrol); sabit H ufuklu getiri yok |
| Ç55 | kapalı konu (FON_IZI v1.0-1.1 (COL_OZET) |
| Ç56 | kapalı konu (FON_IZI v1.1 (COL_OZET) |
| Ç132 | çıktı bariyer isabeti / değişken çıkışlı net getiri (K51 cy_olay); sabit H ufuklu getiri yok |
| Ç133 | Ç132 ile aynı olay dosyası (cy_olay) ve aynı bariyer çıkışı; sabit H ufuklu getiri yok |
| Ç78 | kapalı konu (K17 iki yuvarlama (COL_OZET) |
| Ç79 | kapalı konu (K17) |
| Ç80 | kapalı konu (K17) |
| Ç81 | kapalı konu (K17) |
| Ç82 | kapalı konu (K17 + sektör rüzgârı) |
| Ç83 | kapalı konu (K17) |
| Ç68 | kapalı konu (K13/K14-15 (COL_OZET) |
| Ç41 | işlemler değişken çıkışlı (hedef / 120 bar; 'getiri' işlem getirisi); sabit H ufuklu getiri yok |
| Ç38 | çıktı kutu sonrası en büyük yukarı / aşağı sapma (up / dn), getiri değil; 'ref' tanımı dosyada belirsiz; ABD olay dosyası yok |
| Ç39 | Ç38 ile aynı dosya ve aynı belirsiz çıktı (up / dn) |
| Ç97 | olay sayısı 19-24 (< 300) |
| Ç94 | kapalı konu (Giriş zamanlaması (COL_OZET) |
| Ç251 | tarih 2026-11-26 >= 26 Kasım (zaten rastgele güne göre / iş tanımı dışı) |
| Ç129 | kapalı konu (90+ şekil (kapalı) |
| Ç98 | giriş kutu tavanında bekleyen alış emri (alis_tarih, fiyat düzeyli giriş); t+1 açılış kuralı değil, T1 aynı kuralla kurulamaz |
| Ç73 | kapalı konu (K13b düzgün dip (COL_OZET) |
| Ç74 | kapalı konu (K13b) |
| Ç75 | kapalı konu (K13b) |
| Ç77 | kapalı konu (K13b (COL_OZET) |
| Ç228 | kapalı konu (Tespit geçerliliği) |
| Ç67 | kapalı konu (K13/K14-15 (COL_OZET: TEK CETVEL) |
| Ç69 | kapalı konu (K13) |
| Ç76 | kapalı konu (K13b (COL_OZET) |
| Ç230 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç231 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç232 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç233 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç234 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç235 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç236 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç239 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç240 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç241 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç243 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç244 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç245 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç246 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç248 | kapalı konu (Tespit geçerliliği (CLAUDE.md 25 Kas)) |
| Ç250 | tarih 2026-11-26 >= 26 Kasım (zaten rastgele güne göre / iş tanımı dışı) |
| Ç100 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç102 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç103 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç106 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç107 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç111 | kapalı konu (Sektör ısısı (kapalı) |
| Ç123 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç124 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç135 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç137 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç148 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç149 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç150 | olay sayısı < 300 ya da sayılmadı (None) |
| Ç158 | olay sayısı < 300 ya da sayılmadı (None) |

## 2. Getirisiz sayım (kayıt x kol x hücre: n / ayrı ay)

n = dosyada R'si sonlu olan olay (R dosyada yoksa giriş günü kayıtlı olay); ölçümde ayrıca T1 ve PİYASA tanımlı olmalı (raporda son n).

### Ç209 (14 kol; kaynak sha k2_satir.csv.gz 6fe7d5e8f300c5df)

| Kol | ABD acik_d1 | ABD acik_d2 | ABD acik_d3 | ABD blok | AVR acik_d1 | AVR acik_d2 | AVR acik_d3 | AVR blok |
|---|---|---|---|---|---|---|---|---|
| KT00 | 7664 / 83 | 13559 / 96 | 21631 / 96 | 3389 / 12 | 1765 / 84 | 2871 / 96 | 3888 / 96 | 543 / 12 |
| KT01 | 11025 / 84 | 18253 / 94 | 27210 / 95 | 4216 / 12 | 2464 / 84 | 4046 / 94 | 5088 / 95 | 617 / 12 |
| KT02 | 425 / 73 | 599 / 86 | 1533 / 92 | 202 / 12 | 32 / 22 | 87 / 41 | 103 / 46 | 15 / 7 |
| KT03 | 9586 / 84 | 15733 / 94 | 23898 / 95 | 3742 / 12 | 2168 / 84 | 3542 / 93 | 4415 / 95 | 547 / 12 |
| KT04 | 5454 / 84 | 7052 / 93 | 12321 / 95 | 2091 / 12 | 995 / 81 | 1809 / 93 | 2513 / 93 | 358 / 12 |
| KT05 | 10365 / 84 | 17317 / 94 | 26094 / 95 | 4045 / 12 | 2294 / 84 | 3797 / 94 | 4751 / 94 | 553 / 12 |
| KT06 | 6973 / 84 | 10806 / 94 | 15427 / 95 | 2206 / 12 | 1546 / 81 | 2523 / 93 | 3142 / 94 | 380 / 12 |
| KT07 | 188 / 61 | 228 / 70 | 661 / 86 | 91 / 11 | 7 / 7 | 32 / 21 | 46 / 30 | 9 / 6 |
| KT08 | 3875 / 84 | 8787 / 96 | 17569 / 96 | 1915 / 12 | 787 / 59 | 1660 / 89 | 1926 / 92 | 158 / 11 |
| KT09 | 140 / 37 | 246 / 54 | 969 / 83 | 94 / 12 | 17 / 12 | 21 / 8 | 20 / 16 | — |
| KT10 | 7223 / 84 | 11086 / 96 | 24899 / 96 | 5413 / 12 | — | — | — | — |
| KT11 | 582 / 76 | 943 / 88 | 1545 / 90 | 242 / 12 | 127 / 53 | 216 / 64 | 271 / 76 | 43 / 11 |
| KT12 | 860 / 83 | 1373 / 91 | 2567 / 94 | 420 / 12 | 160 / 61 | 272 / 77 | 417 / 87 | 56 / 12 |
| KT13 | 7799 / 84 | 13728 / 96 | 22222 / 96 | 3431 / 12 | 1766 / 84 | 2808 / 96 | 3834 / 96 | 535 / 12 |

### Ç205 (11 kol; kaynak sha kt_satir.csv.gz 936947f1dea453b2)

| Kol | ABD acik | ABD birikimli | AVR acik | AVR birikimli |
|---|---|---|---|---|
| KT00 | 6718 / 79 | 1290 / 12 | 3452 / 84 | 548 / 12 |
| KT01 | 8686 / 77 | 1848 / 12 | 4496 / 83 | 738 / 12 |
| KT02 | 346 / 64 | 138 / 12 | 89 / 37 | 19 / 9 |
| KT03 | 7614 / 77 | 1612 / 12 | 3910 / 83 | 630 / 12 |
| KT04 | 3823 / 77 | 922 / 12 | 2208 / 80 | 381 / 12 |
| KT05 | 8245 / 77 | 1815 / 12 | 4160 / 82 | 720 / 12 |
| KT06 | 4953 / 77 | 1006 / 12 | 2801 / 82 | 440 / 12 |
| KT07 | 151 / 46 | 52 / 10 | 36 / 24 | 12 / 7 |
| KT08 | 4836 / 84 | 774 / 12 | 1838 / 81 | 182 / 12 |
| KT09 | 167 / 39 | 22 / 10 | 20 / 15 | 3 / 3 |
| KT10 | 18014 / 84 | 3343 / 12 | — | — |

### Ç206 (5 kol; kaynak sha os_kart_olay_ABD_H15.csv.gz fa54600afcd11a76, os_kart_olay_AVR_H15.csv.gz ef0e8e331714ddaf)

| Kol | ABD d1 | ABD d2 | AVR d1 | AVR d2 |
|---|---|---|---|---|
| HIGH52+ | 3318 / 43 | 4656 / 48 | 1940 / 48 | 2058 / 48 |
| MOM+ | 3316 / 43 | 4655 / 48 | 1940 / 48 | 2058 / 48 |
| MOM- | 3278 / 43 | 4612 / 48 | 1894 / 48 | 2017 / 48 |
| STREV+ | 3701 / 48 | 4748 / 48 | 1919 / 48 | 2028 / 48 |
| STREV- | 3740 / 48 | 4795 / 48 | 1962 / 48 | 2072 / 48 |

### Ç226 (4 kol; kaynak sha uc_iz2_satir.csv.gz 5259d363be69c874)

| Kol | ABD d1619 | ABD d2022 |
|---|---|---|
| B_var | 8342 / 48 | 5588 / 34 |
| I_var | 4176 / 48 | 4038 / 34 |
| N_ge2 | 1677 / 48 | 1511 / 33 |
| R_var | 973 / 45 | 1996 / 33 |

### Ç204 (130 kol; kaynak sha yk_TABAN.csv.gz 9888c8e862e3f8e7, yk_TABAN_DS.csv.gz ef779e45a08d9813, yk_C194.csv.gz 3e899f634b724302, yk_C195.csv.gz caceb205db05557a, yk_C196.csv.gz 43a024b7a741e408, yk_C197.csv.gz d8436748f16fcf27, yk_C198.csv.gz a31201dfc042f9b4, yk_C199.csv.gz 14b9792bdf31d1f9, yk_C200.csv.gz b3a3d320e44d851e, yk_C201.csv.gz 0d9cdb29d29a8700, yk_C202.csv.gz 4da8f3ec95130ecd, yk_TUR.csv.gz 545614867ffe8e2f)

| Kol | ABD egitim | ABD sinama | AVR egitim | AVR sinama | BIST egitim | BIST sinama |
|---|---|---|---|---|---|---|
| C194:Y10 | 31 / 18 | 38 / 22 | 9 / 8 | 12 / 10 | 40 / 21 | 71 / 22 |
| C194:Y10b | 8 / 8 | 12 / 10 | 1 / 1 | 3 / 2 | 14 / 10 | 39 / 15 |
| C194:Y10c | 873 / 77 | 749 / 44 | 566 / 77 | 363 / 43 | 486 / 70 | 432 / 42 |
| C195:Y11 | 20 / 14 | 18 / 14 | 6 / 6 | 3 / 3 | 10 / 8 | 12 / 5 |
| C195:Y11b | 4 / 4 | 3 / 3 | 2 / 2 | 2 / 2 | 4 / 4 | 9 / 5 |
| C195:Y11c | 464 / 69 | 354 / 41 | 231 / 65 | 161 / 38 | 141 / 44 | 155 / 29 |
| C196:B_F14 | 100 / 45 | 137 / 38 | 22 / 18 | 17 / 12 | 113 / 41 | 228 / 36 |
| C196:B_S2 | 206 / 55 | 232 / 43 | 51 / 27 | 51 / 28 | 145 / 46 | 207 / 32 |
| C196:B_S3 | 303 / 61 | 345 / 44 | 80 / 35 | 67 / 32 | 217 / 53 | 320 / 38 |
| C196:B_S4 | 310 / 63 | 353 / 44 | 78 / 35 | 70 / 32 | 236 / 53 | 359 / 39 |
| C196:B_S5 | 171 / 48 | 164 / 37 | 38 / 25 | 43 / 27 | 141 / 42 | 295 / 39 |
| C196:B_S6 | 271 / 60 | 262 / 44 | 76 / 31 | 53 / 29 | 198 / 48 | 276 / 36 |
| C196:B_S7 | 176 / 58 | 169 / 39 | 52 / 30 | 47 / 27 | 129 / 40 | 184 / 32 |
| C196:B_S8 | 342 / 63 | 374 / 44 | 89 / 37 | 75 / 33 | 233 / 52 | 360 / 39 |
| C196:B_S9 | 31 / 21 | 23 / 15 | 11 / 10 | 5 / 5 | 16 / 12 | 31 / 13 |
| C196:F14 | 6058 / 77 | 3911 / 44 | 2936 / 82 | 1597 / 44 | 1764 / 79 | 1449 / 44 |
| C196:G1 | 5346 / 77 | 3262 / 44 | 2683 / 82 | 1423 / 44 | 1363 / 79 | 858 / 44 |
| C196:G2 | 346 / 64 | 377 / 44 | 89 / 37 | 75 / 33 | 238 / 53 | 362 / 39 |
| C196:G2u | 31 / 21 | 23 / 15 | 11 / 10 | 5 / 5 | 16 / 12 | 31 / 13 |
| C196:S1 | 346 / 64 | 377 / 44 | 89 / 37 | 75 / 33 | 238 / 53 | 362 / 39 |
| C196:S2 | 5024 / 77 | 3847 / 44 | 2723 / 83 | 1558 / 44 | 1572 / 79 | 1240 / 44 |
| C196:S3 | 7614 / 77 | 5450 / 44 | 3910 / 83 | 2205 / 44 | 2379 / 79 | 1896 / 44 |
| C196:S4 | 8245 / 77 | 5811 / 44 | 4160 / 82 | 2347 / 44 | 2535 / 79 | 2066 / 44 |
| C196:S5 | 3823 / 77 | 2965 / 44 | 2208 / 80 | 1362 / 44 | 1572 / 78 | 1548 / 43 |
| C196:S6 | 6960 / 77 | 4817 / 44 | 3621 / 81 | 2087 / 44 | 2193 / 78 | 1632 / 44 |
| C196:S7 | 4953 / 77 | 3348 / 44 | 2801 / 82 | 1511 / 44 | 1626 / 78 | 1227 / 43 |
| C196:S8 | 8539 / 77 | 5953 / 44 | 4456 / 83 | 2490 / 44 | 2467 / 79 | 2044 / 44 |
| C196:S9 | 464 / 69 | 354 / 41 | 231 / 65 | 161 / 38 | 141 / 44 | 155 / 29 |
| C197:P_AB_alt20 | 1737 / 76 | 1225 / 44 | 899 / 82 | 506 / 43 | 518 / 71 | 420 / 41 |
| C197:P_AB_ust20 | 1737 / 75 | 1225 / 44 | 899 / 80 | 506 / 44 | 518 / 73 | 420 / 43 |
| C197:P_C_alt20 | 1110 / 46 | 1226 / 43 | 527 / 45 | 507 / 44 | 360 / 45 | 421 / 41 |
| C197:P_C_ust20 | 1110 / 45 | 1226 / 44 | 527 / 45 | 507 / 44 | 360 / 46 | 421 / 43 |
| C198:D1_E1_A | 3281 / 77 | 2004 / 44 | 1687 / 81 | 873 / 44 | 1125 / 78 | 774 / 43 |
| C198:D1_E1_B | 176 / 54 | 154 / 40 | 40 / 26 | 33 / 22 | 132 / 43 | 181 / 31 |
| C198:D1_E1t_A | 5405 / 77 | 4128 / 44 | 2809 / 82 | 1653 / 44 | 1463 / 79 | 1322 / 44 |
| C198:D1_E1t_B | 170 / 53 | 223 / 42 | 49 / 24 | 42 / 23 | 106 / 35 | 181 / 35 |
| C198:D1_E2_A | 6874 / 77 | 5049 / 44 | 3154 / 83 | 1823 / 44 | 2170 / 79 | 1904 / 44 |
| C198:D1_E2_B | 214 / 57 | 273 / 43 | 47 / 31 | 37 / 24 | 176 / 50 | 285 / 38 |
| C198:D1_E2t_A | 1811 / 74 | 1082 / 43 | 1337 / 78 | 698 / 44 | 418 / 70 | 192 / 35 |
| C198:D1_E2t_B | 132 / 44 | 104 / 35 | 42 / 17 | 38 / 19 | 62 / 30 | 77 / 24 |
| C198:D1_W1_A | 1978 / 75 | 1305 / 44 | 1060 / 78 | 515 / 44 | 572 / 73 | 426 / 42 |
| C198:D1_W1_B | 53 / 33 | 59 / 26 | 15 / 14 | 6 / 6 | 56 / 31 | 85 / 24 |
| C198:D1_W1t_A | 1978 / 75 | 1485 / 43 | 1060 / 79 | 617 / 44 | 572 / 77 | 478 / 44 |
| C198:D1_W1t_B | 84 / 43 | 100 / 32 | 31 / 18 | 27 / 17 | 54 / 27 | 70 / 22 |
| C198:D1_W2D_A | 1752 / 73 | 1181 / 43 | 973 / 79 | 545 / 44 | 469 / 69 | 310 / 37 |
| C198:D1_W2D_B | 51 / 31 | 70 / 27 | 15 / 11 | 22 / 15 | 43 / 23 | 63 / 19 |
| C198:D1_W2Dt_A | 1752 / 77 | 1318 / 44 | 973 / 79 | 599 / 44 | 469 / 71 | 255 / 42 |
| C198:D1_W2Dt_B | 51 / 23 | 36 / 22 | 8 / 6 | 10 / 9 | 48 / 18 | 25 / 15 |
| C198:D1_W2_A | 1752 / 77 | 1253 / 44 | 973 / 77 | 587 / 44 | 469 / 71 | 265 / 43 |
| C198:D1_W2_B | 37 / 17 | 23 / 15 | 4 / 2 | 10 / 9 | 34 / 17 | 22 / 13 |
| C198:D1_W2t_A | 1752 / 77 | 1301 / 43 | 973 / 81 | 532 / 44 | 469 / 70 | 346 / 38 |
| C198:D1_W2t_B | 78 / 44 | 102 / 35 | 22 / 18 | 26 / 17 | 49 / 25 | 82 / 22 |
| C198:D1_W3_A | 1752 / 77 | 1053 / 43 | 973 / 79 | 419 / 44 | 469 / 63 | 185 / 38 |
| C198:D1_W3_B | 20 / 15 | 18 / 13 | 7 / 6 | 9 / 7 | 25 / 16 | 8 / 7 |
| C198:D1_W3t_A | 1752 / 75 | 1154 / 44 | 973 / 79 | 612 / 44 | 469 / 68 | 402 / 39 |
| C198:D1_W3t_B | 78 / 43 | 92 / 33 | 21 / 16 | 24 / 18 | 64 / 28 | 98 / 21 |
| C198:D1_W4_A | 1756 / 77 | 1053 / 44 | 1180 / 80 | 673 / 44 | 608 / 76 | 461 / 42 |
| C198:D1_W4_B | 59 / 35 | 51 / 26 | 22 / 17 | 17 / 14 | 45 / 24 | 68 / 23 |
| C198:D1_W4t_A | 1450 / 76 | 869 / 44 | 986 / 78 | 595 / 43 | 469 / 71 | 155 / 39 |
| C198:D1_W4t_B | 29 / 26 | 43 / 26 | 7 / 7 | 13 / 11 | 54 / 28 | 33 / 15 |
| C198:D1_W5a_A | 1752 / 77 | 1327 / 44 | 973 / 81 | 575 / 43 | 469 / 75 | 309 / 41 |
| C198:D1_W5a_B | 76 / 39 | 86 / 35 | 16 / 12 | 21 / 13 | 44 / 21 | 47 / 19 |
| C198:D1_W5b_A | 2172 / 77 | 1457 / 44 | 1124 / 80 | 703 / 43 | 647 / 74 | 395 / 41 |
| C198:D1_W5b_B | 70 / 36 | 58 / 27 | 21 / 15 | 20 / 16 | 70 / 31 | 68 / 21 |
| C198:D1_W6_A | 2172 / 77 | 1191 / 43 | 1124 / 79 | 571 / 44 | 647 / 70 | 382 / 40 |
| C198:D1_W6_B | 17 / 14 | 13 / 9 | 4 / 4 | 4 / 4 | 24 / 15 | 13 / 9 |
| C198:D1_W6t_A | 2172 / 77 | 1965 / 44 | 1124 / 80 | 709 / 44 | 647 / 77 | 719 / 43 |
| C198:D1_W6t_B | 256 / 56 | 271 / 43 | 59 / 29 | 56 / 27 | 120 / 43 | 230 / 35 |
| C199:D2_AYK_A | 2172 / 76 | 1797 / 44 | 1124 / 80 | 604 / 43 | 647 / 77 | 662 / 43 |
| C199:D2_AYK_B | 157 / 48 | 202 / 43 | 41 / 24 | 36 / 24 | 101 / 35 | 184 / 35 |
| C199:D2_AY_A | 1813 / 74 | 1443 / 43 | 823 / 76 | 454 / 42 | 465 / 70 | 641 / 43 |
| C199:D2_AY_B | 74 / 36 | 118 / 35 | 10 / 9 | 19 / 14 | 77 / 28 | 130 / 30 |
| C199:D2_DT_A | 1753 / 75 | 1134 / 44 | 1046 / 81 | 639 / 42 | 396 / 66 | 190 / 36 |
| C199:D2_DT_B | 24 / 18 | 22 / 17 | 6 / 6 | 5 / 5 | 33 / 21 | 16 / 6 |
| C199:D2_NR7_A | 1164 / 77 | 755 / 44 | 612 / 78 | 310 / 43 | 381 / 73 | 315 / 40 |
| C199:D2_NR7_B | 48 / 28 | 63 / 31 | 13 / 12 | 6 / 6 | 44 / 24 | 52 / 18 |
| C199:D2_PP_A | 4195 / 77 | 3016 / 44 | 2175 / 81 | 1156 / 44 | 2265 / 78 | 1707 / 44 |
| C199:D2_PP_B | 150 / 51 | 163 / 40 | 42 / 28 | 39 / 23 | 208 / 52 | 300 / 38 |
| C199:D2_RV_A | 587 / 75 | 317 / 44 | 585 / 74 | 277 / 42 | 1091 / 76 | 532 / 43 |
| C199:D2_RV_B | 18 / 15 | 11 / 9 | 12 / 10 | 5 / 5 | 112 / 45 | 106 / 28 |
| C199:D2_VCP_A | 24 / 20 | 20 / 15 | 12 / 12 | 4 / 4 | 9 / 9 | 14 / 8 |
| C199:D2_VCP_B | — | 1 / 1 | — | — | — | — |
| C199:D2_W1_A | 1978 / 75 | 1305 / 44 | 1060 / 78 | 515 / 44 | 572 / 73 | 426 / 42 |
| C199:D2_W1_B | 53 / 33 | 59 / 26 | 15 / 14 | 6 / 6 | 56 / 31 | 85 / 24 |
| C199:D2_W2D_A | 1752 / 73 | 1181 / 43 | 973 / 79 | 545 / 44 | 469 / 69 | 310 / 37 |
| C199:D2_W2D_B | 51 / 31 | 70 / 27 | 15 / 11 | 22 / 15 | 43 / 23 | 63 / 19 |
| C199:D2_W2_A | 1752 / 77 | 1253 / 44 | 973 / 77 | 587 / 44 | 469 / 71 | 265 / 43 |
| C199:D2_W2_B | 37 / 17 | 23 / 15 | 4 / 2 | 10 / 9 | 34 / 17 | 22 / 13 |
| C200:D3_AYK_A | 2172 / 76 | 1797 / 44 | 1124 / 80 | 604 / 43 | 647 / 77 | 662 / 43 |
| C200:D3_AYK_B | 157 / 48 | 202 / 43 | 41 / 24 | 36 / 24 | 101 / 35 | 184 / 35 |
| C200:D3_NR7_A | 1164 / 77 | 755 / 44 | 612 / 78 | 310 / 43 | 381 / 73 | 315 / 40 |
| C200:D3_NR7_B | 48 / 28 | 63 / 31 | 13 / 12 | 6 / 6 | 44 / 24 | 52 / 18 |
| C200:D3_W1_A | 1978 / 75 | 1305 / 44 | 1060 / 78 | 515 / 44 | 572 / 73 | 426 / 42 |
| C200:D3_W1_B | 53 / 33 | 59 / 26 | 15 / 14 | 6 / 6 | 56 / 31 | 85 / 24 |
| C200:D3_W2D_A | 1752 / 73 | 1181 / 43 | 973 / 79 | 545 / 44 | 469 / 69 | 310 / 37 |
| C200:D3_W2D_B | 51 / 31 | 70 / 27 | 15 / 11 | 22 / 15 | 43 / 23 | 63 / 19 |
| C201:Y13 | 712 / 76 | 606 / 44 | 360 / 76 | 234 / 43 | 312 / 64 | 345 / 37 |
| C201:Y13b | 123 / 46 | 131 / 41 | 28 / 20 | 24 / 17 | 98 / 35 | 150 / 30 |
| C201:Y13c | 685 / 74 | 590 / 44 | 346 / 75 | 231 / 43 | 310 / 64 | 343 / 37 |
| C202:DS01 | 2813 / 84 | 1680 / 41 | 913 / 79 | 285 / 41 | 590 / 68 | 871 / 42 |
| C202:DS02 | 1253 / 76 | 819 / 42 | 449 / 71 | 131 / 38 | 283 / 27 | 191 / 21 |
| C202:DS03 | 1407 / 84 | 1556 / 42 | 457 / 77 | 305 / 42 | 295 / 69 | 431 / 41 |
| C202:DS04 | 1604 / 82 | 1082 / 42 | 319 / 66 | 181 / 39 | 159 / 54 | 77 / 30 |
| C202:DS05 | 5721 / 84 | 4274 / 42 | 2058 / 84 | 902 / 42 | 876 / 80 | 1299 / 42 |
| C202:DS06 | 351 / 73 | 239 / 42 | 97 / 38 | 38 / 23 | 54 / 31 | 108 / 30 |
| C202:DS07 | 416 / 70 | 327 / 39 | 130 / 41 | 63 / 29 | 55 / 28 | 157 / 34 |
| C202:DS08 | 11096 / 83 | 7734 / 42 | 4092 / 84 | 1725 / 42 | 1701 / 74 | 3339 / 42 |
| C202:DS09 | 3450 / 84 | 2330 / 42 | 1322 / 80 | 525 / 41 | 890 / 76 | 1380 / 42 |
| C202:DS10 | 3815 / 79 | 2513 / 41 | 1644 / 82 | 515 / 41 | 733 / 69 | 993 / 42 |
| C202:DS11 | 7715 / 84 | 5199 / 42 | 2618 / 84 | 1017 / 42 | 1624 / 80 | 2922 / 42 |
| C202:DS12 | 1038 / 84 | 751 / 41 | 325 / 58 | 131 / 39 | 199 / 52 | 442 / 41 |
| C202:DS13 | 332 / 67 | 218 / 38 | 144 / 47 | 46 / 20 | 81 / 29 | 186 / 31 |
| C202:DS14 | 74 / 34 | 40 / 28 | 17 / 11 | 13 / 12 | 17 / 12 | 33 / 17 |
| C202:DS15 | 1 / 1 | — | — | 1 / 1 | 1 / 1 | 2 / 2 |
| C202:DS16 | 1206 / 84 | 1283 / 42 | 460 / 77 | 333 / 41 | 134 / 47 | 232 / 38 |
| C202:DS17 | 3516 / 84 | 2488 / 42 | 1141 / 81 | 393 / 41 | 737 / 67 | 1343 / 42 |
| C202:DS18 | 2889 / 84 | 1864 / 42 | 997 / 74 | 330 / 41 | 622 / 62 | 1157 / 40 |
| C202:DS19 | 1014 / 83 | 732 / 42 | 317 / 71 | 139 / 41 | 245 / 46 | 255 / 38 |
| C202:DS20 | 4019 / 84 | 2463 / 42 | 1530 / 76 | 566 / 42 | 778 / 70 | 1260 / 41 |
| C202:DS21 | 2878 / 84 | 1947 / 42 | 952 / 74 | 503 / 42 | 573 / 62 | 690 / 41 |
| C202:DS22 | 117 / 49 | 100 / 33 | 28 / 21 | 23 / 16 | 31 / 23 | 61 / 20 |
| C202:DS23 | 2520 / 84 | 1909 / 42 | 1182 / 80 | 487 / 42 | 597 / 72 | 1155 / 42 |
| C202:DS25 | 2666 / 84 | 1838 / 42 | 890 / 73 | 357 / 42 | 393 / 61 | 956 / 42 |
| C202:DS28 | 2769 / 75 | 1796 / 42 | 504 / 59 | 197 / 42 | 472 / 65 | 684 / 42 |
| DS_ANA | 14061 / 84 | 9950 / 42 | 4562 / 84 | 1912 / 42 | 2947 / 81 | 5823 / 42 |
| TUR:T_CEMAL_OLMAZ | 6 / 5 | 1 / 1 | — | — | 5 / 3 | 5 / 4 |
| TUR:T_CEMAL_OLUR | 5 / 4 | 7 / 5 | 2 / 2 | 2 / 2 | 7 / 7 | 9 / 8 |
| TUR:T_MODEL_OLMAZ | 12 / 10 | 11 / 9 | 3 / 3 | 5 / 5 | 12 / 9 | 17 / 10 |
| TUR:T_MODEL_OLUR | 3 / 3 | 1 / 1 | 1 / 1 | — | 4 / 4 | 11 / 6 |
| Y1 | 8686 / 77 | 6132 / 44 | 4496 / 83 | 2526 / 44 | 2588 / 79 | 2096 / 44 |

### Ç191 (3 kol; kaynak sha olay_Y6.csv.gz 0493a4c81a15a792, olay_Y8.csv.gz 5f28d602766025eb, olay_Y8B.csv.gz c63636ba586a863e)

| Kol | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|---|
| Y6 | 867 / 73 | 163 / 12 | 314 / 30 | 522 / 80 | 80 / 11 | 184 / 32 | 87 / 40 | 5 / 3 | 42 / 19 |
| Y8 | 694 / 72 | 93 / 10 | 198 / 29 | 426 / 77 | 52 / 10 | 139 / 32 | 46 / 30 | 4 / 3 | 24 / 13 |
| Y8B | 175 / 56 | 70 / 11 | 116 / 29 | 96 / 47 | 28 / 8 | 45 / 22 | 41 / 26 | 1 / 1 | 18 / 13 |

### Ç99 (3 kol; kaynak sha k27_olay.csv 6c38266593f3d8d4)

| Kol | BIST 2023 | BIST 2024-26 |
|---|---|---|
| alim | 201 / 12 | 418 / 29 |
| buyuk | 12 / 6 | 30 / 17 |
| col_alim | 36 / 8 | 62 / 25 |

### Ç189 (1 kol; kaynak sha olay_TAM_DIP.csv.gz ac6f4a72550e4aec)

| Kol | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|---|
| TAM_DIP | 283 / 63 | 47 / 11 | 187 / 29 | 156 / 50 | 34 / 10 | 132 / 29 | 296 / 61 | 101 / 9 | 387 / 28 |

## 3. Giriş kuralı sağlaması (dosya R'si = aynı kural ve veriden fiyattan R; rastgele <= 500 olay, |fark| < 1e-6)

| Ç | Pazar | Örneklem | Fiyatta bulunan | Birebir |
|---|---|---|---|---|
| Ç209 | ABD | 500 | 500 | 497 |
| Ç209 | AVR | 500 | 500 | 498 |
| Ç205 | ABD | 500 | 500 | 500 |
| Ç205 | AVR | 500 | 500 | 499 |
| Ç206 | ABD | 500 | 500 | 500 |
| Ç206 | AVR | 500 | 500 | 500 |
| Ç226 | ABD | 500 | 500 | 500 |
| Ç204 | ABD | 500 | 500 | 500 |
| Ç204 | AVR | 500 | 500 | 500 |
| Ç204 | BIST | 500 | 500 | 500 |
| Ç191 | ABD | 2690 | 2682 | R dosyada yok (fiyattan) |
| Ç191 | AVR | 1572 | 1566 | R dosyada yok (fiyattan) |
| Ç191 | BIST | 268 | 266 | R dosyada yok (fiyattan) |
| Ç99 | BIST | 500 | 500 | 500 |
| Ç189 | ABD | 500 | 500 | 500 |
| Ç189 | AVR | 322 | 322 | 322 |
| Ç189 | BIST | 500 | 500 | 500 |

## 4. Ölçü ve karar (iş tanımı 2. bölüm AYNEN; önceden)

- R = dosyadaki H ufuklu getiri (yoksa aynı kuralla fiyattan). T1 = aynı hissenin hücre dönemindeki BÜTÜN günlerinde (olay günleri dahil) aynı kuralla R_H ortalaması. PİYASA(t) = giriş günü t'de pazarın evrenindeki (kaynak veri dosyasındaki bütün hisseler) giriş yapılabilen bütün hisselerin R_H eşit ağırlıklı ortalaması (en az 30 hisse). T2 = PİYASA'nın hücre dönemindeki bütün günlerinin ortalaması.
- TOPLAM = R - T1; ZAMANLAMA = PİYASA(t) - T2; SEÇİM = TOPLAM - ZAMANLAMA. Hücre = kaydın kendi pazar x dönem hücresi. Ay kümeli bootstrap %95 (2.000, tohum 11), tek yönlü p = (1 + #(tekrar <= 0)) / (B + 1); ayrı ay sayısı; eski hüküm ve eski eşli fark (dosyanın fark sütunu, varsa) yan sütunda. Olay T1 ya da PİYASA tanımsızsa ölçülmez (sayısı raporda).
- KARAR: ZAMANLAMA ADAYI <=> kol x kaydın n >= 100 olan hücrelerinin HEPSİNDE (en az 2 hücre) ZAMANLAMA GA alt ucu > 0 VE her n >= 100 hücrede ayrı ay >= 12; TOPLAM ADAYI aynı kuralla TOPLAM için. Birleşik p = n >= 100 hücrelerin tek yönlü bootstrap p'lerinin EN BÜYÜĞÜ (kesişim-birleşim sınaması). BH ailesi = ölçülebilir (>= 2 hücre n >= 100, ay >= 12) BÜTÜN kollar (ZAMANLAMA ve TOPLAM ayrı aile); q <= 0,10 geçen aday = ADAY, geçemeyen = EMARE. n >= 100 hücresi 2'den az ya da bir n >= 100 hücrede ay < 12 = ÖLÇÜLEMEDİ; aksi = YOK. Bilgi: bütün n >= 100 hücrelerde üst uç < 0 = EKSİ (ters).
- Karar birimi = kayıt x kol (bir kaydın her kolu ayrı hipotezdir; kayıt satırı kollarının sayımıdır).
- Uyarılar (raporda zorunlu): aynı veride yeniden okuma (kör değil); yaşayan evren (yukarı yanlı); zamanlama farkı olayların belirli piyasa dönemlerine yığılmasından gelebilir (ay kümesi ve ay sayısı şartı bu yüzden). Kayıtların bir kısmı (Ç204'teki Cemal kuralları) görsel onaydan geçmemiş dedektörlerdir: sonuçlar 'dedektörün bulduğu bölgeler' diye sınırlı okunur.
- Bağımsız yeniden üretim: ölçümden sonra iki kayıt-hücre satır dosyasından düz pandas ile (TOPLAM / ZAMANLAMA / SEÇİM ortalaması ve n).

## 5. KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hissenin aynı hücre dönemindeki BÜTÜN günleri (T1) ve aynı gün evren ortalaması (PİYASA); aynı giriş / çıkış geometrisi (kaydın kendi kuralı, stop / hedef yok: mekanik üstünlük yok); eşli taban zaten eski kayıtta (eski fark yan sütunda) |
| K2 | geleceğe bakma | EVET | olay kümeleri kayıtların mühürlü dosyalarından aynen; veri kayıt kesiğinde kesilir (es_veri assert); giriş > kesik olay durur; T1 / PİYASA yalnız giriş sonrası H bar (sonuç değişkeni, karar girdisi değil) |
| K3 | geçerli bar | EVET | gecerli kuralında giriş ve sayılan barlar High > Low ve Volume > 0 (CETVEL2 R_H); fi_olcut FON_IZI.fi_olcut_panel aynen; sağlama dosya R'si ile birebir oranı ön kayıtta |
| K4 | tekilleştirme | EVET | olay kümesi kaydın kendi tekilleştirmesiyle aynen (yeniden süzülmez); n = dosyadaki olay satırı; hücrede ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş = dosyanın 'giris' günü açılışı (sinyalden sonraki ilk işlem günü), kapanış değil; T1 aynı kuralla |
| K6 | veri birimi | EVET | fiyat kaydın kendi veri dosyası (V_* ya da V_*2, tek kip); AVR yerel para; bölünme düzeltmesi kaynak paketlerde yapılmış |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_*); geniş evren V_*2 batanları kısmen içerir; raporda 'yukarı yanlı' uyarısı zorunlu |
| K8 | örneklem ve dönem | EVET | karar hücreleri n >= 100 ve ayrı ay >= 12; n < 100 hücre karara girmez (bilgi); BH q 0,10 bütün ölçülebilir kollarda |
| K9 | ön kayıt | EVET | seçim, sayım, sağlama, karar kuralı ve kod sha bu dosyada; bu dosya commit + push edildikten sonra ölçüm (olcum kapısı commit zamanını ve kod sha'yı denetler); eşik sonuçtan sonra değişmez, değişirse SAPMA |
| K10 | ayrıştırma | EVET | dosya sütunları okuyucularda zorunlu (eksikse durur); sağlama: rastgele 500 olayda dosya R'si = fiyattan R; haber ayrıştırma yok |
| K11 | yeniden üretim | EVET | ölçümden sonra iki kayıt-hücre satır dosyasından bağımsız kodla (düz pandas) yeniden üretilir ve raporda yazılır |
| K12 | ifade | EVET | 'iz' sözü yok; en fazla ZAMANLAMA / TOPLAM ADAYI (aynı veride yeniden okuma; ileri test gerekir); sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı modül sonunda; yasak defter dosyalarına dokunulmaz (git diff denetimi); yalnız kendi yollar commit; e-posta / anahtar taraması çıktılarda |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para kararı yok; yalnız eski kayıtların yeniden okunması |
