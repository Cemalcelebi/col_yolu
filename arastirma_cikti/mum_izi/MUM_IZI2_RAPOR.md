# MUM_IZI2 RAPOR (2026-11-25T10:22:56Z)

Sürüm: MUM_IZI2 v1.0 (2026-11-25): ENSRI parmak izi + MUM_IZI tam iziyle ortak noktalar (yüzdelik) + şans tabanı + birleşik kural (bilgi)

## SONUÇ (düz dil)

- İki grafik 35 ölçünün 13'ünde ortak uçta (6'sı GÜÇLÜ). Rastgele iki pencerede bu sayı ortalama 4,5, %95 üst sınırı 12: iki iz tabanı az farkla aşıyor (rastgele çiftlerin %4,1'i >= 13; GÜÇLÜ ortak 6 için %1,3). Ortak olan MUM YAPISI: uzun üst fitil, küçük gövde / doji, kısa alt fitil, birbirine binen mumlar, yükselen dip, üst bandı delen fitiller. Ortak olmayan GİDİŞ: ilk iz alt banttan üst banda düzgün yükseliyor (R² 0,84), ENSRI yatay (R² 0,14) ve üst banttan başlıyor (4 ZIT ölçü).
- Ölçüler birbirine bağlı (dört ölçü aynı üst fitil özelliğini ölçüyor), bu yüzden "çok ortak nokta" sözü yalnız taban aşımı kadar güçlü; bağımsız ortak özellik sayısı ~6-7.
- Ortak 13 ölçüyü birlikte taşıyan pencereler açık veride seyrek (ABD 1.000 günde 0,11) ve TEPEDE yığılıyor (ABD %34, AVR %60, BIST %39; rastgele gün %19 / %27 / %16). 15 mum sonrası eşinden ayrışmıyor (n 105 / 49 ABD, güç yetersiz). EZBER RİSKLİ, karar yok.

## PARMAK İZİ 2 (ENSRI, 12 aylık mum; birim = ortalama mum boyu)

1. Küçük gövdeler: ortalama gövde boyun %23'ü (açık verideki rastgele 12'li pencerelerin %0,4'ünden küçük); 12 mumun 5'i doji (gövde < boyun %10'u).
2. Uzun üst fitiller: üst fitil boyun %55'i (rastgele pencerelerin %99,9'undan uzun); 12 mumun 6'sında üst fitil boyun yarısından uzun; üst fitiller toplamı alt fitillerin ~2,6 katı.
3. Kısa alt fitiller: boyun %22'si; dipten (8. mum) sonra %15.
4. Gidiş yatay: kapanış doğrusu eğimi -0,02 boy / mum, R² 0,14; en yüksek mum 2., en düşük 8.; net hareket +0,48 boy.
5. Dipler çoğunlukla yükseliyor (%64), tepeler yükselmiyor (%45).
6. Mumlar birbirine çok biniyor (ortak aralık %84; rastgelenin %91'inden fazla) = dar bir kutuda sıkışma.
7. Bant konumu: fiyat üst banttan başlıyor (%B ilk 3 mum 1,01), son 3 mumda 0,68; bütün kapanışlar (türetilmiş) orta bandın üstünde; 12 mumun 5'inde fitil üst bandı deliyor.
8. Bant çok geniş (ilk 3 mumda 4,6 boy) ve daralıyor (log oran -0,46): alt bant hızla yükseliyor (orta bant eğimi +0,19 boy / mum). Alt bant 1-2. mumda görünmüyor (iki senaryo; hiçbir ölçünün sınıfı değişmedi).

## SAYISALLAŞTIRMA

- 12 mum, renk YKKYKKKKYYYY, kenar: {'12': 'SAG_KIRPIK'}; alt bandı görünmeyen mumlar [1, 2]
- TL = 10.5872 + -0.008008 x satır (13 etiket); en büyük artık 0.0037 TL = 0.46 px; ızgara farkı 1.5 px
- Elle doğrulama: [{'i': 5, 'renk': 'K', 'doji_cizgi': False, 'govde_ust': 774, 'govde_alt': 819, 'fitil_ust': 770, 'fitil_alt': 846, 'O': 4.389, 'H': 4.421, 'L': 3.812, 'C': 4.028}, {'i': 6, 'renk': 'K', 'doji_cizgi': True, 'govde_ust': 819, 'govde_alt': 819, 'fitil_ust': 670, 'fitil_alt': 852, 'O': 4.028, 'H': 5.222, 'L': 3.764, 'C': 4.028}, {'i': 7, 'renk': 'K', 'doji_cizgi': False, 'govde_ust': 820, 'govde_alt': 837, 'fitil_ust': 800, 'fitil_alt': 845, 'O': 4.02, 'H': 4.18, 'L': 3.82, 'C': 3.884}]

## ORTAK NOKTALAR

GÜÇLÜ ORTAK 6, ORTAK (güçlü dahil) 13, ZIT 4, AYRI 18, BELİRSİZ 0 (toplam 35 ölçü)

| ölçü | düz dil | iz 1 | iz 2 | p1 | p2 | sınıf |
|---|---|---|---|---|---|---|
| boy_cv | mum boyu değişkenliği (std / ortalama boy) | 0.780 | 0.409 | 0.942 | 0.584 | AYRI |
| govde_oran | ortalama gövde / boy | 0.379 | 0.227 | 0.137 | 0.004 | ORTAK (DÜŞÜK) |
| ust_fitil | ortalama üst fitil / boy | 0.419 | 0.554 | 0.985 | 0.999 | GÜÇLÜ ORTAK (YÜKSEK) |
| alt_fitil | ortalama alt fitil / boy | 0.203 | 0.219 | 0.133 | 0.239 | ORTAK (DÜŞÜK) |
| ust_alt_log | üst fitil baskınlığı: log(toplam üst fitil / toplam alt fitil) | 1.085 | 0.959 | 0.995 | 0.982 | GÜÇLÜ ORTAK (YÜKSEK) |
| yesil_pay | yeşil (C > O) mum payı | 0.600 | 0.500 | 0.845 | 0.573 | AYRI |
| doji_pay | doji payı (gövde / boy < 0,10) | 0.300 | 0.417 | 0.973 | 0.990 | GÜÇLÜ ORTAK (YÜKSEK) |
| uzun_ust_pay | uzun üst fitilli mum payı (üst fitil >= boyun yarısı) | 0.450 | 0.500 | 0.987 | 0.984 | GÜÇLÜ ORTAK (YÜKSEK) |
| buyuk_mum_pay | büyük mum payı (boy >= 1,5 x ortalama) | 0.200 | 0.167 | 0.910 | 0.758 | ORTAK (YÜKSEK) |
| kucuk_mum_pay | küçük mum payı (boy <= 0,7 x ortalama) | 0.550 | 0.250 | 0.977 | 0.549 | AYRI |
| yuk_dip_pay | yükselen dip payı (L > önceki L) | 0.632 | 0.636 | 0.820 | 0.762 | ORTAK (YÜKSEK) |
| yuk_tepe_pay | yükselen tepe payı (H > önceki H) | 0.684 | 0.455 | 0.944 | 0.447 | AYRI |
| yuk_kapanis_pay | yükselen kapanış payı | 0.632 | 0.455 | 0.883 | 0.420 | AYRI |
| ortusme | ardışık mumların örtüşme oranı (ortak aralık / küçük boy) | 0.811 | 0.841 | 0.902 | 0.913 | GÜÇLÜ ORTAK (YÜKSEK) |
| govde_orta_egim | gövde ortası eğimi (mum boyu / mum) | 0.115 | -0.027 | 0.737 | 0.425 | AYRI |
| kapanis_egim | kapanış doğrusu eğimi (mum boyu / mum) | 0.116 | -0.024 | 0.739 | 0.433 | AYRI |
| kapanis_r2 | kapanış doğrusu R^2 (düzgün yürüyüş) | 0.845 | 0.142 | 0.918 | 0.244 | ZIT |
| net_hareket | net hareket: (son kapanış - ilk açılış) / boy | 2.282 | 0.484 | 0.755 | 0.567 | AYRI |
| dipten_yukselis | dipten yükseliş: (son kapanış - en düşük) / boy | 3.072 | 1.181 | 0.662 | 0.361 | AYRI |
| dip_konum | en düşük mumun yeri (0 = baş, 1 = son) | 0.105 | 0.636 | 0.251 | 0.635 | AYRI |
| tepe_konum | en yüksek mumun yeri (0 = baş, 1 = son) | 0.947 | 0.091 | 0.837 | 0.218 | ZIT |
| dip_sonrasi_alt_fitil | dipten sonraki mumlarda ortalama alt fitil / boy | 0.208 | 0.155 | 0.245 | 0.148 | ORTAK (DÜŞÜK) |
| dip_sonrasi_ust_fitil | dipten sonraki mumlarda ortalama üst fitil / boy | 0.453 | 0.669 | 0.951 | 0.990 | GÜÇLÜ ORTAK (YÜKSEK) |
| pB_bas | ilk 3 mumda kapanışın bant içi yeri %B (0 alt bant, 1 üst bant) | 0.061 | 1.006 | 0.070 | 0.954 | ZIT |
| pB_son | son 3 mumda %B | 0.987 | 0.683 | 0.940 | 0.643 | AYRI |
| pB_egim | %B eğimi (mum başına) | 0.053 | -0.039 | 0.981 | 0.177 | ZIT |
| sma_ustu_pay | kapanışı SMA20 üstünde olan mum payı | 0.500 | 1.000 | 0.472 | 0.901 | AYRI |
| sma_mesafe_son | son kapanışın SMA20'ye uzaklığı (mum boyu) | 1.351 | 0.895 | 0.775 | 0.690 | AYRI |
| sma_gecis_konum | SMA20 üstüne kalıcı geçişin yeri (0 baş, 1 = hiç / son) | 0.500 | 0.000 | 0.227 | 0.099 | ORTAK (DÜŞÜK) |
| bant_gen_bas | ilk 3 mumda bant genişliği / mum boyu | 2.538 | 4.599 | 0.170 | 0.571 | AYRI |
| bant_gen_oran_log | bant açılması: log(son 3 genişlik / ilk 3 genişlik) | 0.074 | -0.464 | 0.544 | 0.172 | AYRI |
| bant_dar_konum | bandın en dar olduğu yer (0 baş, 1 son) | 0.632 | 0.909 | 0.585 | 0.713 | AYRI |
| sma_egim | SMA20 eğimi (mum boyu / mum) | -0.017 | 0.188 | 0.413 | 0.900 | AYRI |
| ust_bant_asim_pay | High > üst bant mum payı | 0.400 | 0.417 | 0.926 | 0.880 | ORTAK (YÜKSEK) |
| alt_bant_asim_pay | Low < alt bant mum payı | 0.150 | 0.000 | 0.660 | 0.279 | AYRI |

S: {'S': 'UYGULANAMAZ', 'neden': 'iz 2 L = 12, iz 1 şablon pencereleri [16, 18, 20, 22, 24] (esneme +-%20) dışında', 'D_oz': 1.50958987417407, 'D_oz_tau': 0.8053163579788419, 'tau_oz': 1.8745302504009629, 'rastgele_L12_D_oz_yuzdelik': 0.1835, 'rastgele_L12_D_oz_medyan': 1.8914301235147999}

## ŞANS TABANI

- 5000 rastgele çift, 35 ölçü: ORTAK (güçlü dahil) ort 4.51, %95 üst 12, iki iz 13 (rastgele çiftlerin %4.1'i >= bu sayı)
- GÜÇLÜ ORTAK ort 0.66, %95 üst 3, iki iz 6 (pay %1.3)
- ZIT ort 4.65, %95 üst 12, iki iz 4

## BİRLEŞİK KURAL (BİLGİ, EZBER RİSKLİ)

Kural: [{'olcu': 'govde_oran', 'uc': 'DÜŞÜK', 'q12': 0.3942182831551485, 'q20': 0.4060072732786557}, {'olcu': 'ust_fitil', 'uc': 'YÜKSEK', 'q12': 0.3200836641069086, 'q20': 0.3114578722969248}, {'olcu': 'alt_fitil', 'uc': 'DÜŞÜK', 'q12': 0.22152543344152387, 'q20': 0.2304879654400212}, {'olcu': 'ust_alt_log', 'uc': 'YÜKSEK', 'q12': 0.2610102114230503, 'q20': 0.2121929673633774}, {'olcu': 'doji_pay', 'uc': 'YÜKSEK', 'q12': 0.16666666666666666, 'q20': 0.15}, {'olcu': 'uzun_ust_pay', 'uc': 'YÜKSEK', 'q12': 0.25, 'q20': 0.25}, {'olcu': 'buyuk_mum_pay', 'uc': 'YÜKSEK', 'q12': 0.16666666666666666, 'q20': 0.15}, {'olcu': 'yuk_dip_pay', 'uc': 'YÜKSEK', 'q12': 0.6363636363636364, 'q20': 0.5789473684210527}, {'olcu': 'ortusme', 'uc': 'YÜKSEK', 'q12': 0.7676900978100333, 'q20': 0.7539895975226452}, {'olcu': 'dip_sonrasi_alt_fitil', 'uc': 'DÜŞÜK', 'q12': 0.19515849484493614, 'q20': 0.2097192786904759}, {'olcu': 'dip_sonrasi_ust_fitil', 'uc': 'YÜKSEK', 'q12': 0.34367562308551125, 'q20': 0.33054476679744993}, {'olcu': 'sma_gecis_konum', 'uc': 'DÜŞÜK', 'q12': 0.25, 'q20': 0.55}, {'olcu': 'ust_bant_asim_pay', 'uc': 'YÜKSEK', 'q12': 0.25, 'q20': 0.25}]

- ABD: 640 olay / 5964623 gün (0.11 / 1.000), konum {'TEPE': 218, 'DIP': 1, 'ORTA': 394, 'KISA': 27, 'tepe_pay': 0.340625, 'baska_pay': 0.6171875}, prefix {'n': 30, 'bozuk': 0, 'tuttu': True}
- AVR: 87 olay / 946381 gün (0.09 / 1.000), konum {'TEPE': 52, 'DIP': 0, 'ORTA': 34, 'KISA': 1, 'tepe_pay': 0.5977011494252874, 'baska_pay': 0.39080459770114945}, prefix {'n': 30, 'bozuk': 0, 'tuttu': True}
- BIST: 521 olay / 658371 gün (0.79 / 1.000), konum {'TEPE': 204, 'DIP': 0, 'ORTA': 297, 'KISA': 20, 'tepe_pay': 0.3915547024952015, 'baska_pay': 0.5700575815738963}, prefix {'n': 30, 'bozuk': 0, 'tuttu': True}

| hücre | n | R15 eşli fark | boot %95 | SIRA | güç | +%5 olay | +%5 eş | plasebo fark / TUTAR payı | C2 hüküm (bilgi) |
|---|---|---|---|---|---|---|---|---|---|
| ABD|birlesik|hepsi|d1619 | 105 | %2.45 | %-3.33..%9.69 | 0.476 | 0.41 | %30 | %39 | %0.06 / %0 | ÖLÇÜLEMEDİ |
| ABD|birlesik|hepsi|d2022 | 49 | %-2.05 | %-6.71..%3.12 | 0.476 | 0.17 | %39 | %38 | %0.09 / %0 | ÖLÇÜLEMEDİ |
| ABD|birlesik|tepe|d1619 | 57 | %3.70 | %-3.72..%15.22 | 0.457 | 0.24 | %21 | %34 | - / - | ÖLÇÜLEMEDİ |
| ABD|birlesik|tepe|d2022 | 18 | %-0.00 | %-4.18..%3.79 | 0.495 | 0.08 | %33 | %36 | - / - | örneklem yetersiz |
| ABD|birlesik|baska|d1619 | 48 | %0.96 | %-5.37..%8.82 | 0.498 | 0.21 | %42 | %44 | - / - | ÖLÇÜLEMEDİ |
| ABD|birlesik|baska|d2022 | 31 | %-3.25 | %-9.04..%3.57 | 0.464 | 0.12 | %42 | %39 | - / - | ÖLÇÜLEMEDİ |
| ABD|birlesik|dip|d1619 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |
| ABD|birlesik|dip|d2022 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |
| AVR|birlesik|hepsi|d1619 | 13 | %0.64 | %-2.06..%4.31 | 0.532 | 0.10 | %38 | %19 | %-0.01 / %0 | örneklem yetersiz |
| AVR|birlesik|hepsi|d2022 | 5 | %-4.53 | %-11.15..%2.09 | 0.389 | 0.05 | %0 | %46 | %0.25 / %0 | örneklem yetersiz |
| AVR|birlesik|tepe|d1619 | 10 | %1.32 | %-1.93..%5.92 | 0.559 | 0.09 | %40 | %14 | - / - | örneklem yetersiz |
| AVR|birlesik|tepe|d2022 | 2 | %0.54 | %-5.09..%6.16 | 0.618 | 0.04 | %0 | %26 | - / - | örneklem yetersiz |
| AVR|birlesik|baska|d1619 | 3 | %-1.65 | %-5.27..%0.62 | 0.444 | 0.05 | %33 | %36 | - / - | örneklem yetersiz |
| AVR|birlesik|baska|d2022 | 3 | %-7.91 | %-13.55..%1.61 | 0.237 | 0.05 | %0 | %60 | - / - | örneklem yetersiz |
| AVR|birlesik|dip|d1619 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |
| AVR|birlesik|dip|d2022 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |
| BIST|birlesik|hepsi|d1619 | 204 | %-1.56 | %-3.48..%0.52 | 0.486 | 0.91 | %47 | %47 | - / - | TUTMADI |
| BIST|birlesik|hepsi|d2022 | 173 | %2.16 | %-0.73..%5.10 | 0.542 | 0.63 | %69 | %63 | - / - | ÖLÇÜLEMEDİ |
| BIST|birlesik|tepe|d1619 | 81 | %-2.08 | %-4.76..%1.97 | 0.473 | 0.46 | %57 | %58 | - / - | ÖLÇÜLEMEDİ |
| BIST|birlesik|tepe|d2022 | 75 | %3.64 | %-1.44..%9.06 | 0.543 | 0.30 | %73 | %64 | - / - | ÖLÇÜLEMEDİ |
| BIST|birlesik|baska|d1619 | 123 | %-1.22 | %-3.06..%1.04 | 0.495 | 0.67 | %40 | %40 | - / - | ÖLÇÜLEMEDİ |
| BIST|birlesik|baska|d2022 | 98 | %1.03 | %-1.50..%3.06 | 0.540 | 0.39 | %65 | %63 | - / - | ÖLÇÜLEMEDİ |
| BIST|birlesik|dip|d1619 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |
| BIST|birlesik|dip|d2022 | 0 | - | -..- | - | - | - | - | - / - | örneklem yetersiz |

Yeniden üretim (K11): {'ust_fitil': {'duz': 0.5543388031248284, 'kod': 0.554338803058639}, 'kapanis_egim': {'duz': -0.023653400412271056, 'kod': -0.023653400423938663}, 'p_ust_fitil': {'duz': [0.9849, 0.9988], 'kod': [0.9849, 0.9988]}, 'p_pB_son': {'duz': [0.94035, 0.643], 'kod': [0.94035, 0.643]}, 'kural_10_olay_ihlal': 0, 'tuttu': True}
Kapı: {'kontrol': {'gecti': True}, 'onkayit_commit': '9fc9759b25e5cc1ed9ffcdd3dc2d0212bf6a6341 2026-11-25T10:15:31+00:00', 'KOD2_SHA': 'c4c1019af0eb23095ddb96e2ace420cfc10421cddd60c9f556efe5d8fc6bc8ac', 'ESIK2_SHA': 'd1247a098546c6876c13785d3047e13f4fb412f1c2c21bfa9576ab54f3d54a33', 'SAYISAL2_SHA': 'a0eff63cbd85b1c6166df459a35804af11ae6c5d855b344927651cd0fa3a077e', 'MI_KOD_SHA': '370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9'}
KASA: {'kesik': '2022-12-31', 'dosya': {'/tmp/mum_izi/acik/V_ABD.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_AVR.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_BIST.pkl': '2022-12-30'}}

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | ortak nokta tabanı = şans tabanı SAYIYLA (5.000 rastgele L20 / L12 pencere çifti, aynı kural, ortalama ve %95 üst sınır); birleşik kural sonrası MI.mi_sonrasi: CETVEL2 v2.2 konum eşi (aynı gün aynı kova >= 5 eş), +%5 eşi aynı geometri, plasebo 200 tohum |
| K2 | geleceğe bakma | EVET | ENSRI yalnız görüntüden (2024-25 gerçek fiyat OKUNMAZ); dağılım / şans / birleşik kural açık kopya <= 2022-12-30 (KASA kapısı MI.mi_kasa_kapi); pencere ölçüleri yalnız t'ye kadarki barlar (MI.mi_bant / mi_ozellik prefix testli); birleşik olayda prefix denetimi (mi2_prefix, 30 olay) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar süzgeci (H > L, V > 0); sayısallaştırmada her bölge mumu H >= max(O,C), L <= min(O,C) denetimi |
| K4 | tekilleştirme | EVET | birleşik kural olayları aynı hissede 15 geçerli bar tekil (MI._mi_tekil) + C2.c2_olay tekil 15; dağılım pencereleri tekilsiz (yüzdelik tabanı, olay değil) |
| K5 | giriş fiyatı | EVET | giriş t + 1 açılış (MI.mi_sonrasi -> OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1 |
| K6 | veri birimi | EVET | ENSRI TL ekseni doğrusal kalibrasyon (13 etiket, artık yazılır); ölçüler ölçek bağımsız (oran, mum boyu birimi); gerçek veri TEZGAH2 bölünme düzeltmeli açık kopya |
| K7 | hayatta kalma | EVET | açık kopya bugün işlem gören hisseler (ABD 4.450, AVR 572, BIST 475): sonrası yukarı yanlı, olay ve eş aynı evren; ENSRI tek hisse, halka arz sonrası kısa geçmiş (bant 12 aylık mumla) |
| K8 | örneklem ve dönem | EVET | birleşik kural hücreleri pazar x dönem (d1619 / d2022); n < 30 'örneklem yetersiz'; iki örnekten türetilen kural EZBER RİSKLİ; karar etiketi yok |
| K9 | ön kayıt | EVET | MUM_IZI2_ON_KAYIT.md: KOD2_SHA, ESIK2_SHA, SAYISAL2_SHA, MI_KOD_SHA, dağılım tohumları; ön kayıt commit'i ortak nokta hesabından ÖNCE; mi2_kapi kontrol kapısı + sha + git denetler |
| K10 | ayrıştırma | EVET | bindirme PNG (12 mum) + 3 rastgele mumun yakın plan elle doğrulama PNG'si; mum sayısı ve renk dizisi elle sayımla (test_mum_izi2); TL kalibrasyon artığı ve ızgara satırı sağlaması |
| K11 | yeniden üretim | EVET | mi2_yeniden: iki ölçünün (ust_fitil, kapanis_egim) iz 2 değeri düz döngüyle; iki ölçünün yüzdeliği dağılım dosyasından düz pandas ile; birleşik kural 10 olayda kuralın düz yeniden denetimi |
| K12 | ifade | EVET | 'ortak nokta çok' sözü yalnız şans tabanı aşılırsa; birleşik kural EZBER RİSKLİ, karar yok; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mi2); MUM_IZI.py ve defter / UC_IZ2 dosyaları değişmez; yalnız kendi yolları git add |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; benzerlik / ortak nokta ölçümü |

Uygulama kanıtı: kapı geçti (ön kayıt 9fc9759, KOD2 / ESIK2 / SAYISAL2 / MI_KOD sha = ön kayıt); prefix 3 x 30 birleşik olayda kural kararı aynı; iki ölçü düz döngüyle ve iki yüzdelik düz pandas ile birebir; 10 birleşik olayda kural ihlali 0; test_mum_izi2 7 / 7, test_mum_izi 14 / 14.

## HATA

1. Sayısallaştırma (ön kayıttan önce): ızgaranın görüntü dışındaki noktası (x = -34) negatif dilim indeksiyle neredeyse bütün sütunları bant izlemesinden dışladı; bant bulunamadı. Düzeltme: dilim sınırları kırpıldı, ızgara yalnız görüntü içi.
2. Ayrıştırma (önce): ENSRI bant çizgisinin çekirdeği ilk görüntüdekinden koyu (R ~169); MUM_IZI bant maskesi kaçırıyordu. ENSRI için ayrı lavanta maskesi (R 150-215) + 1 piksellik dikey boşluk kapatma.
3. Hesap (kuru koşu): mum tablosu csv'si 4 ondalıkla yazılıyordu; düz yeniden hesapta 1e-5 fark. Düzeltme: %.10g.
4. İş tanımı "33 ölçü" diyor; MUM_IZI'de 35 ölçü (+ 3 bağlam) var. 35 ölçü aynen kullanıldı (SAPMA 1).

## SAPMA

1. Ölçü sayısı 35 (iş tanımında 33): MUM_IZI'nin bütün MI_OZELLIK ölçüleri, tanım değişmeden.
2. Fiyat etiketi değerleri (₺6,50 .. ₺0,50) görüntüden göz okumasıyla verildi (OCR yok); satırları kodla bulundu, ızgara satırlarıyla sağlandı (en çok 1,5 px).
3. Birleşik kural sonrasında MI.mi_sonrasi'nin tepe / başka / dip alt grupları da hesaplandı (bilgi; ön kayıtta 'hepsi' esas).

## COMMIT'LER (UTC)

- d13bc9c 2026-11-25T10:15:15Z: MUM_IZI2 kod + ENSRI sayısallaştırma (ortak nokta hesabından önce)
- 9fc9759 2026-11-25T10:15:31Z: ön kayıt
- kos 10:15:36Z - 10:20:53Z; sonuç commit'i bu raporla

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- Ç (taslak): "MUM_IZI EK 2 (ENSRI, aylık 12 mum): parmak izi 2 (küçük gövde %23, üst fitil %55, 5 / 12 doji, yatay R² 0,14, üst banttan başlıyor) ve iz 1 ile ortak noktalar: 35 ölçüde GÜÇLÜ ORTAK 6, ORTAK 13, ZIT 4 (şans tabanı ort 4,5, %95 üst 12; GÜÇLÜ ort 0,7, %95 üst 3) -> ortak MUM YAPISI (üst fitil, doji, kısa alt fitil, örtüşme, yükselen dip), ayrı GİDİŞ (iz 1 yükselen, iz 2 yatay). S uygulanamaz (L 12), ölçü uzaklığı rastgele L12 pencerelerin %18'inden yakın. Birleşik kural (13 ölçü; bilgi, EZBER RİSKLİ): ABD 640 / AVR 87 / BIST 521 olay, tepede %34 / %60 / %39 (taban %19 / %27 / %16), R15 eşli fark eşten ayrışmıyor, güç yetersiz. Kasa yok. Commit d13bc9c / 9fc9759 / sonuç."
- IK_GOREV: "2026-11-25 | MUM_IZI EK 2 (ENSRI parmak izi + ortak noktalar) | ortak mum yapısı tabanı az farkla aşıyor (13 vs %95 üst 12), gidiş zıt; birleşik kural tepelerde yığılıyor, sonrası ayrışmıyor (bilgi) | MUM_IZI2.py, test_mum_izi2.py 7 / 7, arastirma_cikti/mum_izi/MUM_IZI2_*"
- IK_HATA: yukarıdaki HATA 1-4 (ayrıştırma x 2, hesap, iletişim / iş tanımı sayısı).
- IK_ACIK: "Ortak mum yapısı (üst fitil + doji + kısa alt fitil + örtüşme) TEK BAŞINA (gidişten bağımsız) bir ölçü olarak ön kayıtla sınanabilir; iki örnekten türediği için ileri test (yeni Cemal grafikleriyle) gerekir."
