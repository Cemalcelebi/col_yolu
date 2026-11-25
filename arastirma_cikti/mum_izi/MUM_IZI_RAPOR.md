# MUM_IZI RAPOR (2026-11-25T10:00:52Z)

Sürüm: MUM_IZI v1.0 (2026-11-25): ORNEK_25Kas parmak izi + sentetik tutturma + açık veride benzerlik / konum / sonrası (bilgi)

## SONUÇ

- TAM iz: etiket İZ DEĞİL; S eşiği 0.59
- TEPESIZ iz: etiket İZ DEĞİL; S eşiği 0.56

Düz dille (sayılar aşağıdaki tablolardan; "puan" = yüzde puanı):

- Cemal'in görsel okuması büyük ölçüde DOĞRU: dipten (3. mum) sonra mumlar küçük, üst fitiller alt fitillerin yaklaşık 3 katı (ortalama üst fitil boyun %42'si, alt %20), dipler çoğunlukla yükseliyor (%63), fiyat alt banttan (%B 0,06) üst banda (%B 0,99) yürüyor, son 3 mum üst bandın dışında. Tek düzeltme: bant başta dar DEĞİL; ortada (13. mum) daralıyor, sonra açılıyor.
- Kod bu izi sentetik seride buluyor: %20 gürültüde tam iz %83, tepesiz iz %85 yakalama (dipten sonra gelen bağlamda %97, tepe bağlamında %63-69); iki bağımsız tekrar aynı (±%2).
- Ama iz NADİR DEĞİL: aynı eşikle rastgele (rastgele yürüyüş) seride de 1.000 barda 3,3 (tam) / 9,4 (tepesiz) kez çıkıyor; gerçek veride ABD 3,3 / 7,6, AVR 2,6 / 6,7, BIST 6,1 / 10,4. Gerçek / rastgele oranı 0,7-1,9 (BIST tam 3,1 blok tabanına göre). Hisse başına yılda ABD 0,83, AVR 0,66, BIST 1,53 kez (tam iz).
- Konum: eşleşmelerin %19'u (ABD) / %31'i (AVR) / %12'si (BIST) tepede; rastgele bir günün tepede olma payı %19 / %27 / %16. Yani iz tepeye ÖZGÜ değil; eşleşmelerin %69-86'sı "başka yerde" (neredeyse hepsi ORTA; DİP < %1, çünkü iz dipten yükselişle biter).
- Sonrası (bilgi): 15 mumda eşlerinden ayrışmıyor. R15 eşli fark dört karar hücresinde -0,25..-0,05 puan (tam), -0,17..-0,05 puan (tepesiz), güven aralıkları 0'ı kesiyor, SIRA 0,49-0,50; +%5 (stop'tan önce) payı olay %27-45, eş %27-44 (fark +0,1..+1,3 puan, sınanmadı). Plasebo (200 rastgele küme) TUTAR payı %4-8 = şans tabanı. Güç 1,00 (n 692-13.640) -> İZ DEĞİL. Kasa açılmadı (KASA KURALI; zaten tek iz bile tutmadı).

## SAYISALLAŞTIRMA

- Bölge mumu 20, renk dizisi YKYYKYKKYKYKYYYYKYYY (Y yeşil, K kırmızı); tepe mumu 3; sınıflar {'BOLGE': 20, 'BAGLAM': 3, 'GIZLI': 1, 'KESIK': 1}
- Izgara: x = 50.54 + 45.129 k (piksel)
- Elle doğrulama mumları: [{'i': 2, 'x': 231.05849268841405, 'renk': 'K', 'doji_cizgi': False, 'govde_ust': 875, 'govde_alt': 936, 'fitil_ust': 868, 'fitil_alt': 947, 'bant_ust': 694.0, 'bant_orta': 803.6, 'bant_alt': 912.5}, {'i': 3, 'x': 276.18757030371216, 'renk': 'Y', 'doji_cizgi': False, 'govde_ust': 901, 'govde_alt': 948, 'fitil_ust': 842, 'fitil_alt': 960, 'bant_ust': 693.9, 'bant_orta': 809.6, 'bant_alt': 925.5}, {'i': 5, 'x': 366.4457255343083, 'renk': 'K', 'doji_cizgi': True, 'govde_ust': 854, 'govde_alt': 857, 'fitil_ust': 825, 'fitil_alt': 876, 'bant_ust': 706.2, 'bant_orta': 819.3, 'bant_alt': 932.3}]

## PARMAK İZİ

| ölçü | düz dil | tam | tepesiz |
|---|---|---|---|
| boy_cv | mum boyu değişkenliği (std / ortalama boy) | 0.78 | 0.70 |
| govde_oran | ortalama gövde / boy | 0.38 | 0.42 |
| ust_fitil | ortalama üst fitil / boy | 0.42 | 0.39 |
| alt_fitil | ortalama alt fitil / boy | 0.20 | 0.20 |
| ust_alt_log | üst fitil baskınlığı: log(toplam üst fitil / toplam alt fitil) | 1.09 | 0.98 |
| yesil_pay | yeşil (C > O) mum payı | 0.60 | 0.59 |
| doji_pay | doji payı (gövde / boy < 0,10) | 0.30 | 0.24 |
| uzun_ust_pay | uzun üst fitilli mum payı (üst fitil >= boyun yarısı) | 0.45 | 0.41 |
| buyuk_mum_pay | büyük mum payı (boy >= 1,5 x ortalama) | 0.20 | 0.24 |
| kucuk_mum_pay | küçük mum payı (boy <= 0,7 x ortalama) | 0.55 | 0.53 |
| yuk_dip_pay | yükselen dip payı (L > önceki L) | 0.63 | 0.56 |
| yuk_tepe_pay | yükselen tepe payı (H > önceki H) | 0.68 | 0.69 |
| yuk_kapanis_pay | yükselen kapanış payı | 0.63 | 0.56 |
| ortusme | ardışık mumların örtüşme oranı (ortak aralık / küçük boy) | 0.81 | 0.82 |
| govde_orta_egim | gövde ortası eğimi (mum boyu / mum) | 0.11 | 0.12 |
| kapanis_egim | kapanış doğrusu eğimi (mum boyu / mum) | 0.12 | 0.11 |
| kapanis_r2 | kapanış doğrusu R^2 (düzgün yürüyüş) | 0.84 | 0.75 |
| net_hareket | net hareket: (son kapanış - ilk açılış) / boy | 2.28 | 1.72 |
| dipten_yukselis | dipten yükseliş: (son kapanış - en düşük) / boy | 3.07 | 2.64 |
| dip_konum | en düşük mumun yeri (0 = baş, 1 = son) | 0.11 | 0.12 |
| tepe_konum | en yüksek mumun yeri (0 = baş, 1 = son) | 0.95 | 0.44 |
| dip_sonrasi_alt_fitil | dipten sonraki mumlarda ortalama alt fitil / boy | 0.21 | 0.20 |
| dip_sonrasi_ust_fitil | dipten sonraki mumlarda ortalama üst fitil / boy | 0.45 | 0.42 |
| pB_bas | ilk 3 mumda kapanışın bant içi yeri %B (0 alt bant, 1 üst bant) | 0.06 | 0.06 |
| pB_son | son 3 mumda %B | 0.99 | 0.90 |
| pB_egim | %B eğimi (mum başına) | 0.05 | 0.06 |
| sma_ustu_pay | kapanışı SMA20 üstünde olan mum payı | 0.50 | 0.41 |
| sma_mesafe_son | son kapanışın SMA20'ye uzaklığı (mum boyu) | 1.35 | 0.95 |
| sma_gecis_konum | SMA20 üstüne kalıcı geçişin yeri (0 baş, 1 = hiç / son) | 0.50 | 0.59 |
| bant_gen_bas | ilk 3 mumda bant genişliği / mum boyu | 2.54 | 2.94 |
| bant_gen_oran_log | bant açılması: log(son 3 genişlik / ilk 3 genişlik) | 0.07 | -0.18 |
| bant_dar_konum | bandın en dar olduğu yer (0 baş, 1 son) | 0.63 | 0.75 |
| sma_egim | SMA20 eğimi (mum boyu / mum) | -0.02 | -0.04 |
| ust_bant_asim_pay | High > üst bant mum payı | 0.40 | 0.29 |
| alt_bant_asim_pay | Low < alt bant mum payı | 0.15 | 0.18 |
| baglam_kirmizi_boy | bölge öncesi büyük kırmızı mumun boyu / bölge ortalama boyu | 1.04 | 1.04 |
| baglam_kirmizi_govde | büyük kırmızı mumun gövdesi / bölge ortalama boyu | 1.04 | 1.04 |
| baglam_dusus | bağlam en yüksek High'dan bölge en düşük Low'a düşüş / bölge ortalama boyu | 1.98 | 1.98 |

Görsel okuma:

- dipten sonra küçük mumlar: dip mumu 3. mum; sonraki 17 mumun %59'i ortalama boyun altında -> DOĞRU
- uzun üst fitiller: ort üst fitil / boy 0.42; üst fitil >= boyun yarısı olan mum 9 / 20 -> DOĞRU
- kısa alt fitiller: ort alt fitil / boy 0.20 (üst 0.42); dipten sonra alt fitil 0.21 -> DOĞRU
- yükselen dipler: yükselen dip payı 0.63; dipten sonra 0.69 -> DOĞRU
- alt banttan SMA20 üstüne geçiş: %B ilk 3 mum 0.06, son 3 mum 0.99; kalıcı SMA üstü geçiş 0.50 konumunda -> DOĞRU
- üst banda yürüyüş: son 3 mumun High'ı üst bandın üstünde; %B son 3 = 0.99 -> DOĞRU
- bant önce dar, sonra açılıyor: bant genişliği (mum boyu): ilk 3 mum 2.54, en dar 1.80 (13. mum, konum 0.63), son 3 mum 2.73; en dar / ilk 3 = 0.71, son 3 / en dar = 1.52 -> KISMEN
- %B dizisi (mum mum): 0.18 -0.11 0.11 0.41 0.34 0.47 0.32 0.32 0.46 0.45 0.82 0.68 0.76 0.90 0.96 0.88 0.86 1.01 1.00 0.95 -> -

## SENTETİK TEST

- kök A tam: yakalama gürültü 0.0: %95, 0.1: %92, 0.2: %83, 0.3: %74; %20 bağlam dip: %97, yatay: %88, tepe: %62; yanlış alarm tekil / 1.000 bar blok 1.98, ry 3.27; birebir (%20) |fark| / sd 0.28, r 0.83, aynı pencere %47
- kök A tepesiz: yakalama gürültü 0.0: %96, 0.1: %94, 0.2: %85, 0.3: %78; %20 bağlam dip: %97, yatay: %90, tepe: %69; yanlış alarm tekil / 1.000 bar blok 5.63, ry 9.43; birebir (%20) |fark| / sd 0.22, r 0.87, aynı pencere %60
- kök B tam: yakalama gürültü 0.0: %92, 0.1: %91, 0.2: %84, 0.3: %72; %20 bağlam dip: %98, yatay: %88, tepe: %64; yanlış alarm tekil / 1.000 bar blok 2.08, ry 3.46; birebir (%20) |fark| / sd 0.25, r 0.85, aynı pencere %52
- kök B tepesiz: yakalama gürültü 0.0: %96, 0.1: %94, 0.2: %84, 0.3: %77; %20 bağlam dip: %97, yatay: %87, tepe: %68; yanlış alarm tekil / 1.000 bar blok 5.74, ry 9.55; birebir (%20) |fark| / sd 0.21, r 0.88, aynı pencere %62

## GERÇEK VERİ

| şablon | pazar | eşleşme / 1.000 bar | hisse-yıl başına | gerçek / blok | gerçek / ry | tepede | başka yerde |
|---|---|---|---|---|---|---|---|
| tam | ABD | 3.276 | 0.826 | 1.65 | 1.00 | %19 | %79 |
| tam | AVR | 2.600 | 0.655 | 1.31 | 0.80 | %31 | %69 |
| tam | BIST | 6.087 | 1.534 | 3.07 | 1.86 | %12 | %86 |
| tepesiz | ABD | 7.619 | 1.920 | 1.35 | 0.81 | %14 | %84 |
| tepesiz | AVR | 6.660 | 1.678 | 1.18 | 0.71 | %24 | %76 |
| tepesiz | BIST | 10.352 | 2.609 | 1.84 | 1.10 | %8 | %90 |

Sonrası (BİLGİ):

| şablon | pazar | hücre | grup | n | R15 eşli fark | boot %95 | SIRA | güç | +%5 olay | +%5 eş | plasebo fark / TUTAR payı | hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tam | ABD | d1619 | hepsi | 5512 | %-0.18 | %-0.50..%0.12 | 0.489 | 1.00 | %36 | %35 | %0.01 / %8 | TUTMADI |
| tam | ABD | d2022 | hepsi | 4998 | %-0.05 | %-0.53..%0.45 | 0.497 | 1.00 | %44 | %43 | %-0.03 / %7 | TUTMADI |
| tam | ABD | d1619 | tepe | 1466 | %-0.19 | %-0.53..%0.17 | 0.495 | 1.00 | %29 | %29 | - / - | TUTMADI |
| tam | ABD | d2022 | tepe | 897 | %0.60 | %-0.28..%1.34 | 0.527 | 1.00 | %39 | %38 | - / - | TUTMADI |
| tam | ABD | d1619 | baska | 4046 | %-0.18 | %-0.54..%0.19 | 0.486 | 1.00 | %38 | %38 | - / - | TUTMADI |
| tam | ABD | d2022 | baska | 4101 | %-0.19 | %-0.71..%0.33 | 0.491 | 1.00 | %45 | %44 | - / - | TUTMADI |
| tam | ABD | d1619 | dip | 23 | %-0.45 | %-2.46..%1.60 | 0.511 | 0.12 | %17 | %34 | - / - | ÖLÇÜLEMEDİ |
| tam | ABD | d2022 | dip | 30 | %-2.01 | %-5.39..%-0.18 | 0.549 | 0.12 | %17 | %19 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | ABD | d1619 | hepsi | 13640 | %-0.12 | %-0.39..%0.17 | 0.495 | 1.00 | %38 | %37 | %0.01 / %5 | TUTMADI |
| tepesiz | ABD | d2022 | hepsi | 12767 | %-0.17 | %-0.61..%0.23 | 0.500 | 1.00 | %45 | %44 | %0.03 / %8 | TUTMADI |
| tepesiz | ABD | d1619 | tepe | 2745 | %0.03 | %-0.33..%0.41 | 0.502 | 1.00 | %28 | %29 | - / - | TUTMADI |
| tepesiz | ABD | d2022 | tepe | 1451 | %0.12 | %-0.50..%0.66 | 0.513 | 1.00 | %37 | %37 | - / - | TUTMADI |
| tepesiz | ABD | d1619 | baska | 10895 | %-0.15 | %-0.45..%0.14 | 0.493 | 1.00 | %40 | %39 | - / - | TUTMADI |
| tepesiz | ABD | d2022 | baska | 11316 | %-0.21 | %-0.67..%0.21 | 0.498 | 1.00 | %46 | %45 | - / - | TUTMADI |
| tepesiz | ABD | d1619 | dip | 188 | %-0.03 | %-0.71..%0.67 | 0.499 | 0.66 | %22 | %31 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | ABD | d2022 | dip | 108 | %-0.82 | %-2.53..%0.81 | 0.464 | 0.33 | %27 | %28 | - / - | ÖLÇÜLEMEDİ |
| tam | AVR | d1619 | hepsi | 873 | %-0.21 | %-0.59..%0.15 | 0.490 | 1.00 | %28 | %27 | %-0.01 / %4 | TUTMADI |
| tam | AVR | d2022 | hepsi | 692 | %-0.25 | %-0.88..%0.38 | 0.489 | 1.00 | %35 | %34 | %-0.01 / %5 | TUTMADI |
| tam | AVR | d1619 | tepe | 296 | %-0.24 | %-0.80..%0.37 | 0.490 | 0.97 | %24 | %22 | - / - | TUTMADI |
| tam | AVR | d2022 | tepe | 180 | %-0.69 | %-1.89..%0.57 | 0.460 | 0.73 | %27 | %27 | - / - | ÖLÇÜLEMEDİ |
| tam | AVR | d1619 | baska | 577 | %-0.20 | %-0.67..%0.25 | 0.489 | 1.00 | %29 | %29 | - / - | TUTMADI |
| tam | AVR | d2022 | baska | 512 | %-0.09 | %-0.80..%0.67 | 0.499 | 1.00 | %37 | %36 | - / - | TUTMADI |
| tam | AVR | d1619 | dip | 9 | %0.33 | %-0.41..%1.34 | 0.554 | 0.08 | %11 | %23 | - / - | ÖLÇÜLEMEDİ |
| tam | AVR | d2022 | dip | 2 | %-0.96 | %-2.18..%0.26 | 0.444 | 0.04 | %0 | %22 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | AVR | d1619 | hepsi | 2314 | %-0.05 | %-0.28..%0.16 | 0.495 | 1.00 | %27 | %27 | %0.00 / %6 | TUTMADI |
| tepesiz | AVR | d2022 | hepsi | 1882 | %-0.09 | %-0.41..%0.19 | 0.500 | 1.00 | %37 | %37 | %0.01 / %8 | TUTMADI |
| tepesiz | AVR | d1619 | tepe | 594 | %-0.21 | %-0.65..%0.24 | 0.488 | 1.00 | %20 | %23 | - / - | TUTMADI |
| tepesiz | AVR | d2022 | tepe | 362 | %0.48 | %-0.12..%1.14 | 0.527 | 0.97 | %28 | %29 | - / - | TUTMADI |
| tepesiz | AVR | d1619 | baska | 1720 | %0.01 | %-0.25..%0.25 | 0.498 | 1.00 | %30 | %29 | - / - | TUTMADI |
| tepesiz | AVR | d2022 | baska | 1520 | %-0.23 | %-0.58..%0.09 | 0.494 | 1.00 | %39 | %39 | - / - | TUTMADI |
| tepesiz | AVR | d1619 | dip | 59 | %-0.16 | %-0.84..%0.55 | 0.482 | 0.36 | %14 | %20 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | AVR | d2022 | dip | 16 | %0.10 | %-1.12..%1.33 | 0.500 | 0.10 | %31 | %25 | - / - | ÖLÇÜLEMEDİ |
| tam | BIST | d1619 | hepsi | 1565 | %0.25 | %-0.31..%0.88 | 0.495 | 1.00 | %45 | %44 | - / - | TUTMADI |
| tam | BIST | d2022 | hepsi | 1354 | %-0.20 | %-1.13..%0.80 | 0.489 | 1.00 | %60 | %58 | - / - | TUTMADI |
| tam | BIST | d1619 | tepe | 167 | %1.31 | %-1.29..%3.15 | 0.534 | 0.83 | %59 | %54 | - / - | TUTMADI |
| tam | BIST | d2022 | tepe | 172 | %-1.16 | %-3.57..%2.01 | 0.469 | 0.63 | %63 | %62 | - / - | ÖLÇÜLEMEDİ |
| tam | BIST | d1619 | baska | 1398 | %0.13 | %-0.40..%0.70 | 0.490 | 1.00 | %44 | %43 | - / - | TUTMADI |
| tam | BIST | d2022 | baska | 1182 | %-0.06 | %-1.08..%1.01 | 0.492 | 1.00 | %59 | %57 | - / - | TUTMADI |
| tam | BIST | d1619 | dip | 7 | %2.38 | %-0.34..%5.85 | 0.690 | 0.06 | %57 | %45 | - / - | ÖLÇÜLEMEDİ |
| tam | BIST | d2022 | dip | 3 | %1.13 | %-1.80..%5.22 | 0.662 | 0.04 | %33 | %30 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | BIST | d1619 | hepsi | 2733 | %0.11 | %-0.24..%0.47 | 0.494 | 1.00 | %44 | %42 | - / - | TUTMADI |
| tepesiz | BIST | d2022 | hepsi | 2227 | %0.50 | %-0.42..%1.92 | 0.499 | 1.00 | %58 | %56 | - / - | TUTMADI |
| tepesiz | BIST | d1619 | tepe | 165 | %0.12 | %-1.60..%1.83 | 0.504 | 0.82 | %55 | %50 | - / - | TUTMADI |
| tepesiz | BIST | d2022 | tepe | 188 | %-0.00 | %-1.94..%2.47 | 0.514 | 0.67 | %65 | %64 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | BIST | d1619 | baska | 2568 | %0.11 | %-0.25..%0.47 | 0.493 | 1.00 | %43 | %42 | - / - | TUTMADI |
| tepesiz | BIST | d2022 | baska | 2039 | %0.54 | %-0.47..%2.15 | 0.498 | 1.00 | %58 | %55 | - / - | TUTMADI |
| tepesiz | BIST | d1619 | dip | 32 | %0.34 | %-1.51..%2.27 | 0.547 | 0.18 | %39 | %30 | - / - | ÖLÇÜLEMEDİ |
| tepesiz | BIST | d2022 | dip | 21 | %-1.24 | %-3.86..%1.10 | 0.475 | 0.11 | %52 | %43 | - / - | ÖLÇÜLEMEDİ |

## DOĞRULAMA

- prefix (K2): {'ABD': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'AVR': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}, 'BIST': {'n': 30, 'en_buyuk_fark': 0.0, 'tuttu': True}}
- düz S (K11): {'ABD': {'n': 20, 'en_buyuk_fark': 2.220446049250313e-16, 'tuttu': True}, 'AVR': {'n': 20, 'en_buyuk_fark': 3.3306690738754696e-16, 'tuttu': True}, 'BIST': {'n': 20, 'en_buyuk_fark': 8.881784197001252e-16, 'tuttu': True}}
- 2 hücre yeniden üretim (K11): {'ABD|d1619': {'duz': {'n': 5512, 'fark': -0.0018232768930691217, 'h5': 0.35784313725490197}, 'json': {'n': 5512, 'fark': -0.0018232768932456198, 'h5': 0.35784313725490197}, 'tuttu': True}, 'AVR|d2022': {'duz': {'n': 692, 'fark': -0.0024546259052882955, 'h5': 0.3468208092485549}, 'json': {'n': 692, 'fark': -0.0024546259052083143, 'h5': 0.3468208092485549}, 'tuttu': True}, 'tuttu': True}
- KASA: {'kesik': '2022-12-31', 'dosya': {'/tmp/mum_izi/acik/V_ABD.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_AVR.pkl': '2022-12-30', '/tmp/mum_izi/acik/V_BIST.pkl': '2022-12-30'}}
- en geç tarih: 2022-12-30

## EK BİLGİ: konum tabanı (ön kayıtta yoktu; SAPMA 2)

Taranan bütün pencere sonu günlerinde (2016-22) rastgele bir günün konumu (mum_izi_konum_taban.json; n = tarama paydası):

| pazar | n gün | TEPE | DİP | ORTA | eşleşme TEPE (tam / tepesiz) | eşleşme DİP (tam / tepesiz) |
|---|---|---|---|---|---|---|
| ABD | 5.912.137 | %19,1 | %10,3 | %68,2 | %19,0 / %13,6 | %0,6 / %1,3 |
| AVR | 944.062 | %27,4 | %11,4 | %60,6 | %30,5 / %23,7 | %0,8 / %2,3 |
| BIST | 654.496 | %15,8 | %8,9 | %73,5 | %12,1 / %8,0 | %0,3 / %1,2 |

Okuma: tam izin tepede bulunma payı rastgele günle aynı (ABD %19,0 / %19,1); tepesiz iz tepede tabandan az. DİP payının çok düşük olması tanım gereği (iz dipten yükselişle biter; pencere sonu artık dipte değildir).

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = CETVEL2 v2.2 konum eşi (C2.c2_es: aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün aynı şablonun bütün olayları dışı); plasebo şans tabanı SAYIYLA: C2.c2_plasebo 200 tohum her karar hücresinde (aynı gün rastgele havuz hissesi, aynı cetvel); +%5 payı eşi = aynı gün aynı kovadan 20 rastgele üye, AYNI geometri (kendi son m barının en düşük Low x 0,98 stop); benzerlik sıklığının tabanı = sentetik rastgele seriler (blok bootstrap + rastgele yürüyüş, aynı eşik) |
| K2 | geleceğe bakma | EVET | S(t) yalnız t'ye kadarki barlar (bant SMA20 / std20 kendi barına kadar; pencere [t-m+1, t]); konum son 120 bar t dahil; mi_prefix: 30 rastgele olayda veri t'de kesilince S(t) aynı (assert); açık kopya <= 2022-12-31 + KASA.kasa_kapisi; üretici havuzu 2005-2014 (karar hücreleri 2016-22 dışı); eşik sentetikten, gerçek veriden önce |
| K3 | geçerli bar | EVET | gerçek veri OS.os_veri / OC.oc_veri_hazirla geçerli bar süzgeci (H > L, V > 0, O/H/L/C > 0); pencereler hissenin kendi geçerli barlarında; sentetik barlar H >= max(O,C) > min(O,C) >= L > 0 (test) |
| K4 | tekilleştirme | EVET | aynı hissede aynı şablon için eşiği geçen pencere sonları 15 geçerli bar tekil (ilk kalır); C2.c2_olay tekil 15 (birleşik takvim); sentetik yanlış alarm da 15 bar tekil sayılır (ham pencere sayısı ayrıca) |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1; +%5 YH.yh_sim (kapanışla, takip stoplu) c2_bilgi üzerinden |
| K6 | veri birimi | EVET | TEZGAH2 V_ABD2 / V_AVR2 (yfinance auto_adjust, bölünme düzeltmeli; AVR Kur sütunu likiditede); S ölçek bağımsız (oranlar, mum boyu birimi); BIST V_BIST (fi_k1_veri) bilgi |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (TEZGAH2 ABD 5.394 / AVR 578 sembolden 2015-22'de verisi olan ABD 4.450, AVR 572; BIST 475): batanlar yok -> sonrası yukarı yanlı; olay ve eş aynı evrenden (yanlılık ikisine aynı); raporda yazılı |
| K8 | örneklem ve dönem | EVET | iki dönem (d1619, d2022) x iki karar pazarı ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç C2 eğrisi; sentetik koşul başına 200 tohum, iki bağımsız kök; tam ve tepesiz iki şablon = iki aile (sonrası yalnız bilgi, BH gerekmez; p'ler yazılır) |
| K9 | ön kayıt | EVET | MUM_IZI_ON_KAYIT.md: KOD_SHA, ESIK_SHA, SABLON_SHA, SENTETIK_SHA (eşik), açık kopya sha'ları; ön kayıt commit'i gerçek veri taramasından önce; mi_kapi kos'tan önce ik_kontrol_kapisi + sha + git (commit'li ve değişmemiş) denetler |
| K10 | ayrıştırma | EVET | sayısallaştırma: bindirme PNG (bütün mumlar) + 3 rastgele mumun yakın plan elle doğrulama PNG'si (mum_izi_elle_dogrulama.png); mum sayısı (20 iç) ve renk dizisi görüntüden elle sayımla karşılaştırılır (test_mum_izi) |
| K11 | yeniden üretim | EVET | mi_duz_S: 20 rastgele olayda S düz döngüyle (vektörsüz) yeniden; mi_yeniden: 2 hücre (ABD d1619, AVR d2022 tam iz) olay satır dosyasından düz pandas ile n / ort FARK / +%5 payı; tutmazsa rapor TUTMADI |
| K12 | ifade | EVET | 'iz' sözü yalnız karar kuralı geçerse; benzerlik / konum hükümsüz sayı; R15 (fiyat değişimi) ile kâr / zarar ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mi); yasak dosyalar (defterler, kural_defteri) ve UC_IZ2 dosyalarına dokunulmaz; yalnız kendi yolları git add; veri3 / /tmp/veri yalnız okunur; e-posta / anahtar taraması (mi_sizinti); ücretli servis yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tespit / benzerlik ölçümü; alım-satım önerisi yok |

Uygulama kanıtı: kapı geçti (sonuc.json `kapi`: kontrol True, ön kayıt commit 91a31a9, KOD_SHA 16759a79… = ön kayıt); prefix 3 x 30 olayda fark 0; düz S 3 x 20 olayda en büyük fark 9e-16; 2 hücre (ABD d1619, AVR d2022 tam) düz pandas = json; ayrıca bağımsız sağlama (bu rapor için, ayrı betik): 3 hücre (ABD d2022 tepesiz, AVR d1619 tam, ABD d2022 tam) n / FARK / SIRA / +%5 / eş +%5 birebir; 8 rastgele ölçülen olayda R15 ve pencere dibi ham açık kopyadan düz döngüyle (fark < 1e-10); tekil olay sayıları ve tepe payları satır dosyası = json.

## HATA

1. Ayrıştırma (gerçek veriden önce): bant izlemenin ilk sürümünde fitil kenarı pikselleri (açık mavi-gri) lavanta bant maskesine girdi; orta bant 682-772 px arasında, alt bant solda kayboldu (NaN). Düzeltme: mum merkezinin ±6 pikseli dışarıda, 10 pikselden uzun dikey koşu fitil sayılır, görünmeyen aralıkta tolerans büyür. Etki: yok (sayısallaştırma tamamlanmadan yakalandı).
2. Hesap (gerçek veriden önce): şablon ilk sürümde LOG fiyat uzayında gömülüyordu; piksel (doğrusal) şablonla gürültüsüz gömmede 0,23 mum boyuna kadar sapma (test_mum_izi yakaladı). Düzeltme: doğrusal fiyat uzayında gömme (fark 2e-14). Bu yüzden ilk tam sentetik koşu atıldı; eşik ikinci koşudan (son kod, 5 tohumla yeniden üretim birebir).
3. Yanlış yorum riski (önce): birebir tutturma korelasyonu ilk sürümde merkezlenmemiş ölçü vektöründe 0,9998 çıkıyordu (ölçü düzeyi farkı korelasyonu şişirir). Düzeltme: ölçü başına ortalamadan merkezlenmiş z ile (r 0,83-0,88).
4. Süreç (kuru koşu): OLCU_SINAMA.os_veri BIST'i tanımıyor; kuru koşuda durdu. Düzeltme: BIST CETVEL2.c2_veri ile (mi_veri).
5. Süreç (kuru koşu): P2 üyeliği olay satır dosyasına taşınmıyordu; eklendi (`p2` sütunu).
6. Süreç: ikinci sentetik koşu, ilki bitmeden aynı günlük dosyasına yazacak şekilde başlatıldı (log karışık). Sonuç json'u ikinci (son kod) koşudan; 5 tohumluk yeniden koşu birebir aynı.
7. Süreç: .gitignore *.csv / *.png; iş tanımındaki zorunlu küçük çıktılar (mum / parmak izi / sentetik tablo csv, bindirme ve elle doğrulama PNG) `git add -f` ile eklendi.
8. Sunum (kos'tan sonra): eşleşme grafiklerinin başlıkları sayfaya sığmıyordu; başlık iki satıra bölündü -> SAPMA 1.

## SAPMA

1. kos (09:48-09:58 UTC) ön kayıttaki KOD_SHA 16759a79… ile koştu. Kos'tan SONRA MUM_IZI.py'de yalnız (a) mi_gorsel eşleşme başlığı iki satıra bölündü, (b) mi_konum_taban (ek bilgi) ve `konum_taban` komutu eklendi. Ölçüm / tarama / eşik kodu değişmedi; yeni KOD_SHA 370d5820… Kapı bundan sonra ikinci kos'u zaten durdurur (sonuç var).
2. Konum tabanı (rastgele günün TEPE / DİP / ORTA payı) ön kayıtta yoktu; sonradan BİLGİ olarak eklendi, hüküm yok.
3. Ön kayıtta "dört karar hücresi" etiket kuralı yön '?' ile yazıldı; plasebo yalnız 'hepsi' grubunda koştu (tepe / başka alt grupları plasebosuz bilgi) — ön kayıtla aynı, sapma değil, not.

## COMMIT'LER (UTC)

- ba19953 2026-11-25T09:47:32Z: kod + sayısallaştırma + sentetik test + açık kopya özeti (gerçek veri taranmadan)
- 91a31a9 2026-11-25T09:47:53Z: ön kayıt (sha'lar, eşik, KONTROL LİSTESİ, elle doğrulama)
- kos başlangıcı 2026-11-25T09:48:03Z, bitişi 09:57:49Z (sonuc.json); sonuç commit'i bu raporla birlikte (git log -- arastirma_cikti/mum_izi/mum_izi_sonuc.json)

## ÖNERİLEN DEFTER SATIRLARI (ana model işler; alt ajan deftere dokunmadı)

- Ç kaydı (taslak): "MUM_IZI (25 Kas, Cemal'in ORNEK_25Kas 4s grafiği): turuncu dairedeki 20 mumun parmak izi (35 ölçü + 3 bağlam; elle sayımla birebir) ve tespit kodu (S = dizi + %B + 12 ölçü uzaklığı). Görsel okuma doğru (küçük mum, üst fitil ~3 x alt, yükselen dip %63, %B 0,06 -> 0,99), 'bant önce dar' kısmen (ortada daralıyor). Sentetik (iki kök, 200 tohum / koşul): S eşiği tam 0,59 / tepesiz 0,56, %20 gürültüde yakalama %83 / %85 (dip bağlamı %97, tepe bağlamı %63-69), yanlış alarm 2,0-3,3 / 5,6-9,4 tekil / 1.000 bar. Açık veri (<= 2022): eşleşme hisse-yıl başına ABD 0,83, AVR 0,66, BIST 1,53 (tam); gerçek / rastgele 0,8-1,9 (BIST blok 3,1); tepede %19 / %31 / %12 = rastgele gün tabanı %19 / %27 / %16; R15 eşli fark -0,25..-0,05 puan, +%5 payı eşle aynı (+0,1..+1,3 puan, sınanmadı), plasebo TUTAR %4-8. KARAR: İZ DEĞİL (tam ve tepesiz; n 692-13.640, güç 1,00). Kasa açılmadı. Commit ba19953 / 91a31a9 / sonuç."
- IK_GOREV: "2026-11-25 | MUM_IZI (Cemal'in işaretli mum bölgesi parmak izi + sentetik tutturma + açık veride benzerlik) | İZ DEĞİL (tam / tepesiz); görsel okuma doğru, iz rastgele sıklıkta, tepeye özgü değil | arastirma_cikti/mum_izi/ (MUM_IZI_RAPOR.md, MUM_IZI_GORSEL.pdf), MUM_IZI.py, test_mum_izi.py 14 / 14"
- IK_HATA (8 satır, yukarıdaki HATA 1-8; tür: ayrıştırma, hesap, yanlış yorum, süreç x 4, sunum / sapma). Ders: piksel şablonu doğrusal uzayda gömülür; korelasyon merkezlenmiş vektörde; kuru koşu (sentetik panel) gerçek veriden önce hattın bütün dallarını (BIST) yakalar.
- IK_ACIK: (a) +%5 payında olay lehine küçük ama 8 / 8 karar hücresinde aynı yönde fark (+0,1..+1,3 puan) ön kayıtlı test DEĞİL; olası neden stop uzaklığı (iz penceresinin dibi girişten daha uzak). İstenirse ön kayıtla 'stop uzaklığı eşlenmiş eş' testi. (b) İz 4 saatlik grafikten alındı, günlük veride ölçüldü; gün içi (4s) veri olursa aynı şablon ve eşikle yeniden ölçüm (IK_ILERI adayı). (c) Tek iz: KASA KURALI gereği kasa açılmaz; birleşik iz bileşeni adayı da değil (İZ DEĞİL).
