# SD RAPOR — benzer şekil benzer devam mı; verinin kendi desenleri (2026-11-27)

Ön kayıt commit: 255859910f29a0d9e7cb6fbe53d93ee6d09f74b9 2026-11-27T05:39:34+00:00; kesim commit: 65ae08b0513cbf7837330982765cd8d1f8625f9a 2026-11-27T05:43:31+00:00; doğrulama 2026-11-27T05:43:42.906050+00:00 .. 2026-11-27T07:04:36.183576+00:00.
Evren bugün yaşayan hisseler (yukarı yanlı; ÜST - ALT ve IC kesit içi). KASA açılmadı (veri <= 2022-12-31).

## SONUÇ

### SINAMA 1, L20: ŞEKİL BİLGİ TAŞIMIYOR; tanımlayıcı B: HACİM EKLEMİYOR

ABD 2020-22: 385364 sorgu, 36 ay. IC(A) -0,001 [-0,014 / 0,012]; IC(0) -0,002 [-0,009 / 0,005]; IC(rastgele) -0,001 [-0,004 / 0,001]; IC(A) - IC(0) 0,001 [-0,012 / 0,013]; IC(B) -0,008 [-0,021 / 0,005]; IC(B) - IC(A) -0,007 [-0,015 / 0,001]. AVR 2020-22 (64755 sorgu): IC(A) -0,005 [-0,022 / 0,017], IC(0) 0,003 [-0,010 / 0,016], IC(rastgele) 0,004 [-0,002 / 0,010].

| grup (TAHMİN A) | n | Z15 | R15 % | HEDEF | AYNA | TOPLAM FARK % |
|---|---|---|---|---|---|---|
| UST | 38551 | 0,003 [-0,124 / 0,113] | 0,52 [-1,24 / 2,23] | 0,301 [0,272 / 0,331] | 0,298 [0,258 / 0,339] | 0,09 [-1,69 / 1,77] |
| ALT | 38520 | -0,007 [-0,146 / 0,102] | 0,41 [-1,32 / 2,00] | 0,312 [0,287 / 0,339] | 0,285 [0,248 / 0,321] | -0,04 [-1,75 / 1,48] |
| HEPSI | 385364 | -0,003 [-0,128 / 0,102] | 0,43 [-1,23 / 2,04] | 0,305 [0,279 / 0,333] | 0,290 [0,253 / 0,328] | -0,02 [-1,67 / 1,54] |
| ÜST - ALT | | 0,011 [-0,027 / 0,048] | 0,11 [-0,45 / 0,66] | -0,011 [-0,028 / 0,005] | 0,014 [-0,003 / 0,033] | 0,13 [-0,44 / 0,68] |

Yol benzerliği (ortalama korelasyon): komşu A -0,002 [-0,027 / 0,021], rastgele -0,000 [-0,027 / 0,023], 0 -0,002 [-0,028 / 0,020], B -0,006 [-0,033 / 0,019].
Şartlar: {'IC_A': False, 'A-0': False, 'UST-ALT': False, 'AVR': False}.

### SINAMA 1, L10 (ERKEN EVRE): ŞEKİL BİLGİ TAŞIMIYOR; tanımlayıcı B: HACİM EKLEMİYOR

ABD 2020-22: 386370 sorgu, 36 ay. IC(A) -0,006 [-0,017 / 0,004]; IC(0) -0,002 [-0,009 / 0,004]; IC(rastgele) 0,002 [-0,000 / 0,005]; IC(A) - IC(0) -0,004 [-0,015 / 0,007]; IC(B) -0,009 [-0,020 / 0,002]; IC(B) - IC(A) -0,003 [-0,008 / 0,003]. AVR 2020-22 (64790 sorgu): IC(A) 0,003 [-0,010 / 0,017], IC(0) 0,003 [-0,010 / 0,016], IC(rastgele) 0,000 [-0,007 / 0,007].

| grup (TAHMİN A) | n | Z15 | R15 % | HEDEF | AYNA | TOPLAM FARK % |
|---|---|---|---|---|---|---|
| UST | 38655 | 0,007 [-0,112 / 0,109] | 0,47 [-1,16 / 2,08] | 0,307 [0,278 / 0,337] | 0,291 [0,252 / 0,331] | 0,07 [-1,57 / 1,61] |
| ALT | 38620 | 0,016 [-0,115 / 0,123] | 0,81 [-0,91 / 2,52] | 0,316 [0,286 / 0,346] | 0,277 [0,241 / 0,312] | 0,37 [-1,38 / 2,00] |
| HEPSI | 386370 | -0,004 [-0,126 / 0,100] | 0,43 [-1,23 / 2,06] | 0,305 [0,278 / 0,333] | 0,290 [0,253 / 0,327] | -0,01 [-1,68 / 1,54] |
| ÜST - ALT | | -0,009 [-0,039 / 0,023] | -0,34 [-0,76 / 0,06] | -0,009 [-0,025 / 0,007] | 0,015 [-0,004 / 0,035] | -0,30 [-0,75 / 0,12] |

Yol benzerliği (ortalama korelasyon): komşu A -0,001 [-0,026 / 0,023], rastgele 0,000 [-0,026 / 0,024], 0 -0,003 [-0,028 / 0,020], B -0,005 [-0,032 / 0,021].
Şartlar: {'IC_A': False, 'A-0': False, 'UST-ALT': False, 'AVR': True}.

### SINAMA 2, L20: en iyi küme DESEN TUTMADI; en kötü küme DESEN TUTMADI; BH'den geçen: yok

| seçim | küme | şekil | keşif Z15 / n | doğr. Z15 | R15 % | TOPLAM FARK % | HEDEF | AYNA | ay / üst3 | AVR Z15 (n) | AVR 16-19 Z15 | p | BH q | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| İYİ 1 | 3 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %21'i, fitiller dengeli; bant %242 genişliyor; dip önceki 60 günün tepesinin 9.4 ATR altında; 120 günlük aralıkta %56 konumundan %20'e | 0,165 / 5577 | 0,051 [-0,189 / 0,189] | 4,78 [-1,90 / 9,69] | 4,65 [-1,75 / 9,51] | 0,318 | 0,216 | 36 / 0,39 | 0,068 (1144) | 0,115 | 0,2998 | 0,790 | TUTMADI |
| İYİ 2 | 28 | Kapanışlar üst bantta başlayıp alt bantta bitiyor; mum boyu bant genişliğinin %26'i, fitiller dengeli; bant %5 genişliyor; dip önceki 60 günün tepesinin 5.5 ATR altında; 120 günlük aralıkta %77 konumundan %50'e | 0,157 / 6882 | -0,042 [-0,220 / 0,137] | -0,30 [-2,71 / 2,38] | -0,76 [-3,24 / 1,96] | 0,289 | 0,303 | 36 / 0,18 | -0,010 (1075) | 0,078 | 0,6869 | 0,790 | TUTMADI |
| İYİ 3 | 59 | Kapanışlar orta ile alt bant arasında başlayıp ortada (SMA20 çevresinde) bitiyor; mum boyu bant genişliğinin %24'i, fitiller dengeli; bant %37 genişliyor; dip önceki 60 günün tepesinin 7.1 ATR altında; 120 günlük aralıkta %63 konumundan %52'e | 0,142 / 6002 | 0,016 [-0,193 / 0,172] | 0,56 [-2,07 / 2,79] | 0,02 [-2,55 / 2,25] | 0,288 | 0,292 | 36 / 0,22 | -0,026 (1004) | 0,130 | 0,4215 | 0,790 | TUTMADI |
| İYİ 4 | 55 | Kapanışlar ortada (SMA20 çevresinde) başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %23'i, fitiller dengeli; bant %135 genişliyor; dip önceki 60 günün tepesinin 8.2 ATR altında; 120 günlük aralıkta %65 konumundan %30'e | 0,139 / 6881 | 0,005 [-0,138 / 0,126] | 1,37 [-1,63 / 4,90] | 1,13 [-1,82 / 4,45] | 0,282 | 0,279 | 36 / 0,23 | -0,011 (1186) | 0,100 | 0,4455 | 0,790 | TUTMADI |
| İYİ 5 | 9 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %18'i, fitiller dengeli; bant %14 genişliyor; dip önceki 60 günün tepesinin 10.4 ATR altında; 120 günlük aralıkta %30 konumundan %23'e | 0,138 / 8402 | 0,006 [-0,191 / 0,150] | 1,35 [-3,05 / 5,36] | 1,24 [-3,00 / 4,92] | 0,303 | 0,246 | 36 / 0,34 | 0,024 (1797) | 0,107 | 0,4761 | 0,790 | TUTMADI |
| KÖTÜ 1 | 37 | Kapanışlar ortada (SMA20 çevresinde) başlayıp ortada (SMA20 çevresinde) bitiyor; mum boyu bant genişliğinin %34'i, fitiller dengeli; bant %24 daralıyor; dip önceki 60 günün tepesinin 6.6 ATR altında; 120 günlük aralıkta %54 konumundan %44'e | 0,027 / 3982 | 0,035 [-0,142 / 0,178] | 1,01 [-1,62 / 3,35] | 0,77 [-1,84 / 3,06] | 0,318 | 0,293 | 36 / 0,15 | -0,004 (726) | 0,141 | 0,6849 | 0,790 | TUTMADI |
| KÖTÜ 2 | 45 | Kapanışlar orta ile üst bant arasında başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %28'i, fitiller dengeli; bant %51 genişliyor; dip önceki 60 günün tepesinin 4.2 ATR altında; 120 günlük aralıkta %68 konumundan %82'e | 0,027 / 6911 | -0,014 [-0,174 / 0,123] | 0,13 [-2,04 / 2,44] | -0,68 [-2,89 / 1,59] | 0,290 | 0,329 | 36 / 0,18 | -0,031 (1038) | 0,058 | 0,4445 | 0,790 | TUTMADI |
| KÖTÜ 3 | 7 | Kapanışlar ortada (SMA20 çevresinde) başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %32'i, fitiller dengeli; bant %23 genişliyor; dip önceki 60 günün tepesinin 5.9 ATR altında; 120 günlük aralıkta %53 konumundan %74'e | 0,029 / 4971 | 0,055 [-0,072 / 0,170] | 1,15 [-0,76 / 2,96] | 0,53 [-1,41 / 2,32] | 0,332 | 0,294 | 36 / 0,15 | -0,028 (768) | 0,085 | 0,8066 | 0,807 | TUTMADI |
| KÖTÜ 4 | 56 | Kapanışlar ortada (SMA20 çevresinde) başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %30'i, fitiller dengeli; bant %0 daralıyor; dip önceki 60 günün tepesinin 7.0 ATR altında; 120 günlük aralıkta %44 konumundan %39'e | 0,029 / 4218 | 0,037 [-0,096 / 0,176] | 0,72 [-1,75 / 3,37] | 0,59 [-1,87 / 3,17] | 0,329 | 0,261 | 36 / 0,15 | 0,022 (739) | 0,090 | 0,7110 | 0,790 | TUTMADI |
| KÖTÜ 5 | 18 | Kapanışlar orta ile üst bant arasında başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %30'i, fitiller dengeli; bant %19 genişliyor; dip önceki 60 günün tepesinin 4.0 ATR altında; 120 günlük aralıkta %74 konumundan %84'e | 0,032 / 6337 | -0,002 [-0,158 / 0,119] | 0,49 [-1,41 / 2,20] | -0,35 [-2,25 / 1,34] | 0,282 | 0,336 | 36 / 0,18 | -0,037 (911) | 0,065 | 0,5065 | 0,790 | TUTMADI |

Cemal'in BENZİYOR dediği günlük bölgeler (L20): 34 / 36 atandı; ilk 5 küme [küme, n, pay, keşif sırası]: [[46, 7, 0.20588235294117646, 31], [51, 5, 0.14705882352941177, 16], [0, 4, 0.11764705882352941, 32], [58, 4, 0.11764705882352941, 24], [7, 3, 0.08823529411764706, 57]]; seçilen iyi 5 payı 0,00, kötü 5 payı 0,09. HAYIR (bilgi): ilk 5 [[51, 16, 0.27586206896551724, 16], [0, 9, 0.15517241379310345, 32], [58, 8, 0.13793103448275862, 24], [7, 5, 0.08620689655172414, 57], [26, 4, 0.06896551724137931, 19]].
- APPN_SOL: küme 30, keşif sırası 14 (keşif Z15 0,114, n 7885); doğrulama Z15 0,007 (n 7979); şekil: Kapanışlar alt bantta başlayıp orta ile üst bant arasında bitiyor; mum boyu bant genişliğinin %20'i, fitiller dengeli; bant %11 daralıyor; dip önceki 60 günün tepesinin 9.7 ATR altında; 120 günlük aralıkta %28 konumundan %41'e
- APPN_SAG: küme 51, keşif sırası 16 (keşif Z15 0,111, n 8244); doğrulama Z15 0,021 (n 7336); şekil: Kapanışlar alt bantta başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %22'i, fitiller dengeli; bant %20 genişliyor; dip önceki 60 günün tepesinin 8.8 ATR altında; 120 günlük aralıkta %31 konumundan %54'e

### SINAMA 2, L10: en iyi küme DESEN TUTMADI; en kötü küme DESEN TUTMADI; BH'den geçen: yok

| seçim | küme | şekil | keşif Z15 / n | doğr. Z15 | R15 % | TOPLAM FARK % | HEDEF | AYNA | ay / üst3 | AVR Z15 (n) | AVR 16-19 Z15 | p | BH q | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| İYİ 1 | 58 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %17'i, fitiller dengeli; bant %70 genişliyor; dip önceki 60 günün tepesinin 10.3 ATR altında; 120 günlük aralıkta %11 konumundan %10'e | 0,167 / 10122 | -0,013 [-0,112 / 0,088] | 0,33 [-1,81 / 2,04] | 0,45 [-1,46 / 2,10] | 0,272 | 0,255 | 36 / 0,38 | 0,024 (2029) | 0,115 | 0,6061 | 0,606 | TUTMADI |
| İYİ 2 | 36 | Kapanışlar ortada (SMA20 çevresinde) başlayıp alt bantta bitiyor; mum boyu bant genişliğinin %28'i, fitiller dengeli; bant %8 genişliyor; dip önceki 60 günün tepesinin 5.5 ATR altında; 120 günlük aralıkta %69 konumundan %55'e | 0,136 / 8019 | -0,013 [-0,149 / 0,118] | -0,15 [-1,95 / 1,67] | -0,69 [-2,54 / 1,14] | 0,303 | 0,289 | 36 / 0,20 | 0,030 (1271) | 0,129 | 0,5595 | 0,606 | TUTMADI |
| İYİ 3 | 28 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %23'i, fitiller dengeli; bant %9 daralıyor; dip önceki 60 günün tepesinin 5.4 ATR altında; 120 günlük aralıkta %62 konumundan %60'e | 0,132 / 8190 | 0,038 [-0,105 / 0,156] | 0,85 [-1,03 / 2,52] | 0,20 [-1,63 / 1,84] | 0,296 | 0,282 | 36 / 0,22 | -0,030 (1166) | 0,107 | 0,2648 | 0,606 | TUTMADI |
| İYİ 4 | 55 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %18'i, fitiller dengeli; bant %11 daralıyor; dip önceki 60 günün tepesinin 10.1 ATR altında; 120 günlük aralıkta %14 konumundan %9'e | 0,124 / 10841 | -0,005 [-0,138 / 0,118] | -0,14 [-2,72 / 2,46] | 0,20 [-2,30 / 2,71] | 0,293 | 0,266 | 36 / 0,25 | 0,041 (1867) | 0,144 | 0,5271 | 0,606 | TUTMADI |
| İYİ 5 | 54 | Kapanışlar alt bantta başlayıp orta ile alt bant arasında bitiyor; mum boyu bant genişliğinin %22'i, fitiller dengeli; bant %48 genişliyor; dip önceki 60 günün tepesinin 6.2 ATR altında; 120 günlük aralıkta %62 konumundan %54'e | 0,124 / 9523 | -0,020 [-0,196 / 0,127] | 0,09 [-1,90 / 1,88] | -0,60 [-2,51 / 1,19] | 0,286 | 0,304 | 36 / 0,24 | -0,029 (1489) | 0,092 | 0,5626 | 0,606 | TUTMADI |
| KÖTÜ 1 | 14 | Kapanışlar orta ile üst bant arasında başlayıp alt bantta bitiyor; mum boyu bant genişliğinin %37'i, fitiller dengeli; bant %18 genişliyor; dip önceki 60 günün tepesinin 6.4 ATR altında; 120 günlük aralıkta %58 konumundan %36'e | -0,001 / 3228 | -0,109 [-0,573 / 0,188] | 0,12 [-5,21 / 4,58] | -0,30 [-5,67 / 4,05] | 0,288 | 0,312 | 36 / 0,29 | -0,156 (525) | 0,069 | 0,3553 | 0,606 | TUTMADI |
| KÖTÜ 2 | 46 | Kapanışlar üst bantta başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %25'i, fitiller dengeli; bant %180 genişliyor; dip önceki 60 günün tepesinin 2.9 ATR altında; 120 günlük aralıkta %69 konumundan %86'e | 0,023 / 6372 | 0,011 [-0,140 / 0,139] | 0,42 [-2,00 / 2,74] | -0,38 [-2,78 / 1,91] | 0,291 | 0,329 | 36 / 0,21 | -0,051 (828) | 0,038 | 0,5814 | 0,606 | TUTMADI |
| KÖTÜ 3 | 16 | Kapanışlar üst bantta başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %22'i, fitiller dengeli; bant %44 genişliyor; dip önceki 60 günün tepesinin 2.1 ATR altında; 120 günlük aralıkta %84 konumundan %94'e | 0,040 / 12017 | -0,010 [-0,156 / 0,112] | 0,15 [-1,46 / 1,68] | -0,78 [-2,40 / 0,72] | 0,293 | 0,321 | 36 / 0,18 | -0,039 (1827) | 0,061 | 0,4596 | 0,606 | TUTMADI |
| KÖTÜ 4 | 39 | Kapanışlar ortada (SMA20 çevresinde) başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %34'i, fitiller dengeli; bant %15 genişliyor; dip önceki 60 günün tepesinin 4.1 ATR altında; 120 günlük aralıkta %68 konumundan %83'e | 0,041 / 5771 | 0,005 [-0,121 / 0,118] | 0,36 [-1,25 / 1,89] | -0,41 [-2,08 / 1,17] | 0,327 | 0,298 | 36 / 0,18 | -0,021 (775) | 0,052 | 0,5368 | 0,606 | TUTMADI |
| KÖTÜ 5 | 19 | Kapanışlar üst bantta başlayıp ortada (SMA20 çevresinde) bitiyor; mum boyu bant genişliğinin %19'i, fitiller dengeli; bant %1 daralıyor; dip önceki 60 günün tepesinin 2.2 ATR altında; 120 günlük aralıkta %90 konumundan %79'e | 0,043 / 11422 | 0,012 [-0,137 / 0,142] | 0,77 [-1,18 / 2,74] | 0,01 [-1,94 / 1,99] | 0,302 | 0,300 | 36 / 0,17 | -0,026 (1558) | 0,055 | 0,5837 | 0,606 | TUTMADI |

Cemal'in BENZİYOR dediği günlük bölgeler (L10): 34 / 36 atandı; ilk 5 küme [küme, n, pay, keşif sırası]: [[30, 11, 0.3235294117647059, 43], [48, 5, 0.14705882352941177, 42], [38, 4, 0.11764705882352941, 21], [6, 3, 0.08823529411764706, 47], [16, 3, 0.08823529411764706, 57]]; seçilen iyi 5 payı 0,00, kötü 5 payı 0,12. HAYIR (bilgi): ilk 5 [[38, 15, 0.2542372881355932, 21], [52, 7, 0.11864406779661017, 40], [37, 6, 0.1016949152542373, 29], [6, 5, 0.0847457627118644, 47], [30, 4, 0.06779661016949153, 43]].
- APPN_SOL: küme 37, keşif sırası 29 (keşif Z15 0,089, n 6236); doğrulama Z15 0,021 (n 6887); şekil: Kapanışlar orta ile alt bant arasında başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %26'i, fitiller dengeli; bant %23 daralıyor; dip önceki 60 günün tepesinin 9.3 ATR altında; 120 günlük aralıkta %15 konumundan %34'e
- APPN_SAG: küme 38, keşif sırası 21 (keşif Z15 0,097, n 6466); doğrulama Z15 0,024 (n 7139); şekil: Kapanışlar ortada (SMA20 çevresinde) başlayıp üst bantta bitiyor; mum boyu bant genişliğinin %26'i, fitiller dengeli; bant %2 genişliyor; dip önceki 60 günün tepesinin 8.6 ATR altında; 120 günlük aralıkta %20 konumundan %39'e

## SENTETİK

- Yakalama (kalıbın kümesine düşen POZ payı, gürültüye göre): {'0.00': 0.989010989010989, '0.10': 0.9975062344139651, '0.20': 0.994579945799458, '0.30': 0.9754098360655737}; hepsi 0,989; en kalabalık 3 küme 0,998
- Yanlış kabul (kalıbın kümesine düşen): {'N1': 0.0, 'N2': 0.0, 'N3': 4.100461301896463e-05}; ilk 3 küme: {'N1': 0.01226158038147139, 'N2': 0.0, 'N3': 0.03034341363403383}
- Kalıbın kümesi 31: keşif sırası 7 / 60, en iyi 5 içinde: False; kümede POZ payı 0,999
- IC(A) gömülü 0,286 [0,261 / 0,310]; ilişkisiz -0,010 [-0,024 / 0,003]; rastgele komşu (gömülü) -0,008 [-0,023 / 0,006]
- En iyi 5 küme: kalıbın erken evresi (pencere sonu olay bitişinden 1-15 bar önce) payı 0,961, tam kalıp payı 0,000; bileşim {'8': {'POZ-10': 482, 'N2-10': 117, 'N2-20': 2}, '2': {'POZ-5': 707, 'N2-5': 4, 'N2-35': 2}, '19': {'POZ-5': 726, 'N2-5': 12, 'N2-30': 3}, '22': {'POZ-10': 423, 'N2-10': 187, 'N1-10': 178}, '38': {'N1-10': 268, 'POZ+40': 1, 'POZ-40': 1}}


## KONTROL LİSTESİ

Ön kayıttaki tablo (14 madde) aynen geçerli; denetim kanıtı: komşu denetimi (aynı hisse / yakın / sonucu bilinmeyen komşu sayısı) L20 ABD: {'ayni_hisse': 0, 'yakin': 0, 'sonuc_bilinmiyor': 0, 'sorgudan_20_bar_once_degil': 0}; L20 AVR: {'ayni_hisse': 0, 'yakin': 0, 'sonuc_bilinmiyor': 0, 'sorgudan_20_bar_once_degil': 0}; L10 ABD: {'ayni_hisse': 0, 'yakin': 0, 'sonuc_bilinmiyor': 0, 'sorgudan_20_bar_once_degil': 0}; L10 AVR: {'ayni_hisse': 0, 'yakin': 0, 'sonuc_bilinmiyor': 0, 'sorgudan_20_bar_once_degil': 0}.

## HATA

- Sentetik ilk tasarımda +0,5 Z sürüklenme 15 bara yayılıyordu; sonraki pencerelerin (k + 5, k + 10) devamına taşıyıp 'kalıp' ile 'sürüklenmenin devamı'nı karıştırıyordu. Girişten sonraki barda tek sıçramaya çevrildi (gerçek veri görülmeden, ön kayıttan önce).
- sd_sayim komşu havuzu boyutunda indeks hatası (groupby etiketleri pozisyon yerine sorgu satırı sanılmıştı); ön kayıttan önce düzeltildi (yalnız sayım; ölçüm kodu sd_komsu doğruydu, testle sınandı).
- Ön kayıt sayım tablosunda hücre adlarındaki '|' Markdown tablosunu bozuyordu; ön kayıt commit'inden önce düzeltildi.
- Çakışma kapısı testinin ilk hali yanlış kurulmuştu (modül özniteliğini değiştirmek kapıyı tetiklemez); Colab exec senaryosuyla (bellekte aynı ad varken yükleme) yeniden yazıldı.
- Bağımsız yeniden üretimde keşif küme 3: n 5576 (modül 5577); bir pencere sınırda farklı kümeye düştü (modül standart tanımlayıcıyı float32'ye çevirip atıyor, bağımsız kod float64). Z15 aynı (0,165). Hükme etkisi yok.
- Uyarı (hata değil): k-ortalama L20 ve L10'da 300 adım tavanına ulaştı (atama tam durmadı); ön kayıtlı tavan; merkezler doğrulamada aynı kodla birebir yeniden üretildi (DUR kapısı geçti).
- Uyarı: Cemal'in 36 günlük EVET bölgesinden 2'si (BFRI 2022-04-07, PCILT 2022-03-23) TANIMSIZ: bölgeden önce 80 bar yok (yeni halka arz); 34 bölge atandı.

## SAPMA

- (yok) Ölçüm tanımı, eşik, K, küme sayısı, pencere uzunluğu değişmedi. Sentetik ek (Cemal'in kalıbı + N1 / N2 / N3) koordinatörün iletisiyle ön kayıttan ÖNCE koda girdi; gerçek sonucu etkilemez.
- Yalnız gösterim: sonuçtan sonra SD_DESENLER.pdf'te küme tarifi satırı sayfa kenarından taştığı için satır kaydırma eklendi (sd_desen_pdf; ölçüm kodu değişmedi; kod sha ön kayıttakinden farklı, yalnız bu satır).

## YENİDEN ÜRETİM

- Bağımsız kısa kod (/tmp/claude-0/.../scratchpad/sd_yeniden.py; SEKIL_DEVAM fonksiyonu kullanmaz; ham npz + sd_kesim.json merkezleri):
- (1) keşif küme 3 (L20): n 5576 / Z15 0,1646 (rapor 5577 / 0,165; 1 pencere sınır farkı, yukarıda HATA)
- (2) ABD L20 ÜST - ALT Z15: 0,0031 - (-0,0075) = 0,0106 (rapor 0,0106; birebir)
- (3) doğrulama küme 3 (L20): n 6393 / Z15 0,0515 (rapor birebir)
- (4) IC(A) L20 ABD: -0,0011 (rapor -0,0011; birebir)

## ÖNERİLEN DEFTER SATIRLARI

- Ç (SEKIL_DEVAM, 27 Kas): 'benzer şekil benzer devam' önermesi ABD 2020-22'de 385 bin pencerede sınandı: IC(A) L20 -0,001 [-0,015 / 0,012], L10 -0,006 [-0,017 / 0,004]; basit taban ve rastgele komşu ile aynı; hacim eklemedi. Hüküm iki uzunlukta ŞEKİL BİLGİ TAŞIMIYOR (güç yeterli). Kümeler: keşifin en iyi / en kötü 5 kümesinin hiçbiri doğrulamada tutmadı, BH'den geçen yok. Cemal'in BENZİYOR bölgeleri seçilen iyi kümelere düşmedi (pay 0).
- IK_ILERI: aynı komut 2023+ verisiyle (kasa açıldığında; kasa kuralı gereği tek önerme kasa açtırmaz) yeniden ölçülür; eşikler sabit.
- IK_HATA: sentetikte sürüklenmenin sonraki pencerelere taşması (tasarım hatası; düzeltildi, gerçek veri görülmeden).

## DOSYALAR

- /root/.kasa/ham/sekil_devam/ozellik_ABD.npz: 310f8ab209795618aeb9858f0fae4923062b607d34a4c0f9781792cccabcbae8
- /root/.kasa/ham/sekil_devam/ozellik_AVR.npz: 9c428a1b267cd238b2779196b4f3ddba91ac6de7475a78612f7f1504b9c28c4e
- /root/.kasa/ham/sekil_devam/cemal_tanim.pkl: fe47edf5e181b6cebf230b2f673c4c9ae0e358fb1cde9c1507a78695e667d740
- /root/.kasa/ham/sekil_devam/sayim.json: 2a7b7ebc5ccd45c584a8a652ea160f5c692aaded37b06eaa2f0577b0774edf91
- /root/.kasa/ham/sekil_devam/tahmin_ABD_L20.npz: 68ea0563aab0259e660d8a617439ae4acce9ca1e6abac7d1fad1c5778ffb39a3
- /root/.kasa/ham/sekil_devam/tahmin_ABD_L10.npz: 04a5fde219902dc142b8f9f4c15b4e6ce03ac92c4be5b1587fbe1a10959db9bb
- /root/.kasa/ham/sekil_devam/tahmin_AVR_L20.npz: f90b690ce485d8b2fa5aa388f6fc7fd800849979874c24f9e97424b9925b410a
- /root/.kasa/ham/sekil_devam/tahmin_AVR_L10.npz: 0b327434e6816fa831e822c42d0cb9f43b57cfec9f82025ac69c8c58a35d741c

