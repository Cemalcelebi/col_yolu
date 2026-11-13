# BofA kendi maliyetinden kâr ediyor mu; haber sonrası yol var mı — sonuç (13 Kasım 2026)

## Düzeltme sonrası (ana model denetimi 13.11.2026)

Bu rapor, BofA liste verisi yeniden ayrıştırıldıktan sonra AYNI ön kayıt, aynı eşikler ve aynı tanımlarla yeniden koşuldu. Sapma gerekçesi: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi. Düzeltilenler: çok kurumlu haberlerde her tablonun kurumu tablodan önceki başlık / cümleden okunur (belirsiz -> BİLİNMİYOR, ölçüme girmez); hisse sütunundaki kurum adı satırları ('HSBC: -433 mn') düşer; aylık / dönemsel özet haberleri tur='aylik' / 'donemsel' (kapsam dışı); sayfada biriken günlük güncellemeler ('GÜNCELLEME 30 EYLÜL') kendi tarihini taşır (Eylül listesi Haziran tarihli sayılmaz); numaralı tek satırlık tablolar tek liste; haber sitelerinin ilgili haber kuşağı gövde dışı (kenar kuşağından 'SSAAT 56 TL' gibi satırlar BofA listesi sayılmaz). Liste mührü 7020587fbc90 -> 28014e1a3be8.

**KARAR: DEĞİŞMEDİ** — eski: yol yok (7 satırın hiçbiri bütün şartları geçmedi); yeni: yol yok (7 satırın hiçbiri bütün şartları geçmedi). Eski rapor ve JSON: /home/user/col_yolu/arastirma_cikti/bofa_izi/eski_v1.

| satır | ESKİ | YENİ |
|---|---|---|
| B TÜMÜ G1+C1 | n 1567, eşli fark +0,6% [-0,3%, +1,6%], sıra 0.51, portföy 2.90 / %90 3.57 | n 1620, eşli fark +0,6% [-0,3%, +1,6%], sıra 0.51, portföy 3.88 / %90 3.20 |
| B K2 G1+C1 | n 22, eşli fark +5,9% [-0,1%, +13,2%], sıra 0.61, portföy 0.16 / %90 0.12 | n 57, eşli fark +1,5% [-1,1%, +4,5%], sıra 0.53, portföy 0.21 / %90 0.24 |
| B K6 G1+C1 | n 33, eşli fark -6,4% [-13,3%, -0,5%], sıra 0.39, portföy -0.11 / %90 0.27 | n 87, eşli fark -0,8% [-5,1%, +2,3%], sıra 0.50, portföy 0.01 / %90 0.26 |
| B K1 G1+C1 | n 11, eşli fark +17,8% [-14,5%, +54,2%], sıra 0.48, portföy 0.32 / %90 0.17 | n 15, eşli fark +16,9% [-2,2%, +48,2%], sıra 0.61, portföy 0.35 / %90 0.19 |
| A 20 gün (BofA maliyetinden) | n 72, eşli fark +0,7%, medyan +3,2%, kâr oranı +56,9% | n 120, eşli fark -1,5%, medyan -3,9%, kâr oranı +39,2% |
| A 60 gün | n 72, eşli fark +1,3%, medyan +5,5%, kâr oranı +59,7% | n 79, eşli fark -0,3%, medyan +3,5%, kâr oranı +55,7% |
| A kriz sonrası 20 gün (BİLGİ) | n 87, eşli fark +1,2%, medyan -9,9%, kâr oranı +21,8% | n 194, eşli fark +0,5%, medyan -15,2%, kâr oranı +15,5% |
| FIFO (tüm) | n 86, medyan -2,2%, kâr oranı +36,0% | n 302, medyan -4,3%, kâr oranı +35,4% |
| FIFO eşleşen lot | 577622515.0 | 2430963616.0 |
| temizlik geçerli satır | 24350 | 24974 |
| kriz açık dönem | 31 | 30 |

Soru (Cemal, 13.11.2026): 'BofA bir hissede %40-80 zarar etmez; senin mantığın bunu alıyor mu? Bana bir yol gösterecekse ölç.' A: BofA'nın yayımlanan ortalama maliyetinden getiri (betimleyici). B: haber anında bilinen 6 koşulla haber sonrası giriş (ön kayıtlı karar).

## Özet (düz dil)

- BofA'nın yayımlanan maliyetinden (kesik içi, n 120 alım satırı, 70 hisse): 5 gün sonra medyan +0,5%, 20 gün sonra medyan -3,9% (kâr oranı %39, ortalama +0,2%), 60 gün sonra medyan +3,5% (kâr oranı %56, n 79). Aynı gün benzer hisselere göre 20 gün eşli fark ortalaması -1,5%, 60 gün -0,3%.
- Kriz sonrası (veri günü >= 01.09.2026, BİLGİ): BofA alımları 20 gün sonra kendi maliyetinden medyan -15,2%, kâr oranı %15, P(<= -%30) %23 (n 194); benzer hisselere göre eşli fark +0,5%.
- En iyi kırılım (n >= 20): 60 gün 'fiyat 10-50' eşli fark +6,3% (kâr oranı %65, n 23); en kötü: 60 gün 'fiyat >=50' -5,4% (kâr oranı %59, n 41). Kırılımlar çoklu karşılaştırmadır, BİLGİ.
- FIFO (yayımlanan lot listeleri, alım -> sonraki satış): 302 eşleşme, lot ağırlıklı gerçekleşen getiri -6,6%, medyan -4,3%, kârlı eşleşme %35, tutma medyan 15,00 gün; kesik içi 72 eşleşme, kriz sonrası 230 (BİLGİ). Kapsam düşük: alınan lotun %51'i yayımlanmış bir satışla eşlenebildi (denetim notu: bölüm 9).
- Haber sonrası giriş (Cemal'in yolu, G1 + C1, TÜMÜ): n 1620, eşli fark +0,6% [-0,3%, +1,6%], sıra 0,51; geç kalma (giriş / BofA maliyeti - 1) medyan +0,0% (n 46).
- 7 satır içinde (n >= 30) en yüksek eşli fark: K2 (kovalamama: G1 giriş fiyatı / tetik satırındaki BofA maliyeti - 1 <= +%5 (maliyet yazılı)) +1,5% [-1,1%, +4,5%], n 57; karar: yol yok.
- n < 30 (örneklem yetersiz, karar dışı): K1 +16,9% [-2,2%, +48,2%] n 15.
- KARAR: yol yok (7 satırın hiçbiri bütün şartları geçmedi). Karar en fazla BIST-ADAY olabilir (AKD verisi yalnız BIST'te; ABD / Avrupa hücresi yok).
- Kriz sonrası (01.09.2026'dan, BİLGİ): 202 BofA dönemi, 30 hâlâ açık (tablo bölüm 6).

## 1. A — BofA'nın kendi maliyetinden getirisi (alım satırları, pencere sonu <= 31.08.2026)

| kırılım | ufuk | n | kâr oranı | medyan | ortalama | P(>= +%30) | eş P | kat | P(<= -%30) | eş P | kat | eşli fark ort. / medyan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| birim TL | 5 | 64 | %59 | +1,6% | +3,0% | %0 | %1 | 0,00 | %0 | %0 | 0,00 | +1,8% / +0,5% |
| birim lot | 5 | 107 | %48 | -0,4% | +0,5% | %2 | %1 | 2,15 | %0 | %1 | 0,00 | +0,7% / -0,2% |
| cokmus | 5 | 21 | %33 | -2,2% | -2,0% | %0 | %1 | 0,00 | %0 | %0 | 0,00 | -0,8% / -1,8% |
| cokmus_degil | 5 | 147 | %54 | +1,3% | +1,9% | %1 | %1 | 1,47 | %0 | %0 | 0,00 | +1,3% / +0,3% |
| dönem 2023-24 | 5 | 0 | | | | | | | | | | |
| dönem 2025-26 | 5 | 171 | %52 | +0,5% | +1,4% | %1 | %1 | 1,30 | %0 | %0 | 0,00 | +1,1% / +0,2% |
| fiyat 10-50 | 5 | 49 | %55 | +1,3% | +1,8% | %0 | %1 | 0,00 | %0 | %1 | 0,00 | +1,6% / +0,5% |
| fiyat 2-10 | 5 | 41 | %54 | +0,5% | +2,1% | %5 | %1 | 5,67 | %0 | %0 | 0,00 | +1,9% / -0,3% |
| fiyat <2 | 5 | 36 | %53 | +1,0% | +1,2% | %0 | %1 | 0,00 | %0 | %0 | 0,00 | +1,6% / +1,2% |
| fiyat >=50 | 5 | 45 | %47 | -0,5% | +0,7% | %0 | %1 | 0,00 | %0 | %0 | 0,00 | -0,5% / -2,0% |
| gun_ici | 5 | 155 | %55 | +1,3% | +1,9% | %1 | %1 | 1,45 | %0 | %0 | 0,00 | +1,4% / +0,3% |
| gun_sonu | 5 | 16 | %25 | -4,0% | -2,8% | %0 | %1 | 0,00 | %0 | %1 | 0,00 | -1,9% / -2,1% |
| kriz_sonrasi (BİLGİ) | 5 | 262 | %29 | -3,1% | -4,0% | %2 | %1 | 1,81 | %2 | %5 | 0,48 | +1,2% / +1,2% |
| pay < %20 | 5 | 148 | %49 | -0,2% | +0,5% | %1 | %1 | 0,73 | %0 | %0 | 0,00 | +0,3% / -0,3% |
| pay >= %20 | 5 | 7 | %86 | +3,6% | +11,5% | %14 | %1 | 19,14 | %0 | %1 | 0,00 | +10,3% / +4,6% |
| pay yok | 5 | 16 | %69 | +4,9% | +6,1% | %0 | %1 | 0,00 | %0 | %0 | 0,00 | +4,7% / +3,1% |
| tum | 5 | 171 | %52 | +0,5% | +1,4% | %1 | %1 | 1,30 | %0 | %0 | 0,00 | +1,1% / +0,2% |
| birim TL | 20 | 64 | %56 | +3,2% | +4,7% | %8 | %6 | 1,24 | %2 | %1 | 1,07 | +0,4% / -0,4% |
| birim lot | 20 | 56 | %20 | -8,7% | -5,0% | %0 | %4 | 0,00 | %0 | %2 | 0,00 | -3,8% / -5,3% |
| cokmus | 20 | 15 | %13 | -12,0% | -11,5% | %0 | %4 | 0,00 | %7 | %2 | 2,82 | -11,2% / -8,0% |
| cokmus_degil | 20 | 102 | %42 | -2,3% | +1,4% | %4 | %5 | 0,72 | %0 | %2 | 0,00 | -0,5% / -3,4% |
| dönem 2023-24 | 20 | 0 | | | | | | | | | | |
| dönem 2025-26 | 20 | 120 | %39 | -3,9% | +0,2% | %4 | %5 | 0,77 | %1 | %2 | 0,43 | -1,5% / -3,6% |
| fiyat 10-50 | 20 | 36 | %47 | -1,6% | +1,1% | %6 | %5 | 1,14 | %3 | %3 | 1,12 | +0,2% / +1,4% |
| fiyat 2-10 | 20 | 24 | %25 | -5,6% | -2,7% | %0 | %6 | 0,00 | %0 | %2 | 0,00 | -3,4% / -5,9% |
| fiyat <2 | 20 | 17 | %12 | -7,2% | -4,9% | %6 | %4 | 1,67 | %0 | %2 | 0,00 | -3,3% / -4,6% |
| fiyat >=50 | 20 | 43 | %51 | +0,1% | +3,0% | %5 | %6 | 0,72 | %0 | %2 | 0,00 | -1,1% / -4,0% |
| gun_ici | 20 | 104 | %40 | -3,5% | +0,9% | %5 | %6 | 0,85 | %1 | %2 | 0,49 | -1,5% / -3,6% |
| gun_sonu | 20 | 16 | %31 | -6,6% | -4,6% | %0 | %3 | 0,00 | %0 | %2 | 0,00 | -1,6% / -2,5% |
| kriz_sonrasi (BİLGİ) | 20 | 194 | %15 | -15,2% | -17,6% | %0 | %0 | 0,00 | %23 | %19 | 1,22 | +0,5% / +1,1% |
| pay < %20 | 20 | 102 | %34 | -4,6% | -2,1% | %2 | %5 | 0,41 | %1 | %2 | 0,49 | -2,9% / -4,4% |
| pay >= %20 | 20 | 2 | %50 | +8,7% | +8,7% | %0 | %12 | 0,00 | %0 | %3 | 0,00 | +2,5% / +2,5% |
| pay yok | 20 | 16 | %69 | +11,9% | +13,3% | %19 | %8 | 2,27 | %0 | %1 | 0,00 | +6,9% / +4,0% |
| tum | 20 | 120 | %39 | -3,9% | +0,2% | %4 | %5 | 0,77 | %1 | %2 | 0,43 | -1,5% / -3,6% |
| birim TL | 60 | 64 | %62 | +9,0% | +16,8% | %14 | %19 | 0,75 | %2 | %3 | 0,46 | +2,5% / -4,7% |
| birim lot | 60 | 15 | %27 | -17,1% | -10,1% | %13 | %13 | 1,03 | %27 | %13 | 2,09 | -12,3% / -14,6% |
| cokmus | 60 | 6 | %17 | -15,8% | -17,9% | %0 | %12 | 0,00 | %17 | %10 | 1,73 | -26,9% / -21,7% |
| cokmus_degil | 60 | 71 | %58 | +7,1% | +11,8% | %14 | %18 | 0,79 | %6 | %5 | 1,18 | -0,1% / -5,3% |
| dönem 2023-24 | 60 | 0 | | | | | | | | | | |
| dönem 2025-26 | 60 | 79 | %56 | +3,5% | +11,7% | %14 | %18 | 0,79 | %6 | %5 | 1,23 | -0,3% / -6,5% |
| fiyat 10-50 | 60 | 23 | %65 | +11,5% | +18,1% | %22 | %17 | 1,29 | %9 | %5 | 1,81 | +6,3% / -3,2% |
| fiyat 2-10 | 60 | 10 | %20 | -15,8% | -12,6% | %0 | %15 | 0,00 | %10 | %9 | 1,11 | -19,3% / -17,8% |
| fiyat <2 | 60 | 5 | %60 | +7,9% | +52,0% | %20 | %16 | 1,29 | %20 | %11 | 1,89 | +48,8% / +7,5% |
| fiyat >=50 | 60 | 41 | %59 | +3,9% | +9,2% | %12 | %19 | 0,64 | %2 | %4 | 0,65 | -5,4% / -7,3% |
| gun_ici | 60 | 63 | %51 | +1,4% | +11,6% | %14 | %17 | 0,85 | %8 | %6 | 1,34 | +1,3% / -7,0% |
| gun_sonu | 60 | 16 | %75 | +14,6% | +12,0% | %12 | %21 | 0,59 | %0 | %2 | 0,00 | -6,6% / -4,4% |
| kriz_sonrasi (BİLGİ) | 60 | 0 | | | | | | | | | | |
| pay < %20 | 60 | 61 | %52 | +1,5% | +10,8% | %11 | %17 | 0,68 | %7 | %5 | 1,19 | -1,4% / -6,5% |
| pay >= %20 | 60 | 2 | %50 | -9,3% | -9,3% | %0 | %14 | 0,00 | %50 | %12 | 4,19 | -15,8% / -15,8% |
| pay yok | 60 | 16 | %69 | +12,9% | +17,9% | %25 | %21 | 1,20 | %0 | %3 | 0,00 | +6,0% / -2,6% |
| tum | 60 | 79 | %56 | +3,5% | +11,7% | %14 | %18 | 0,79 | %6 | %5 | 1,23 | -0,3% / -6,5% |

Pencere sayımı (ana / kesik aşan / kriz sonrası / pencere yok): 5 gün {"ana": 171, "kesik_asan": 10, "kriz_sonrasi": 262, "kriz_sonrasi_pencere_yok": 24}; 20 gün {"ana": 120, "kesik_asan": 61, "kriz_sonrasi": 194, "kriz_sonrasi_pencere_yok": 92}; 60 gün {"ana": 79, "kesik_asan": 88, "kriz_sonrasi_pencere_yok": 286, "pencere_yok": 14}.

Haftalık listeler (BİLGİ, haftalık maliyet): 5 gün n 21, medyan -1,2%, kâr oranı %43, eşli fark +0,8%; 20 gün n 21, medyan -6,5%, kâr oranı %29, eşli fark -5,4%; 60 gün n 11, medyan -16,2%, kâr oranı %36, eşli fark -7,1%.
Satış satırları (BİLGİ; işaretli: BofA sattıktan sonra fiyat düşerse +): 20 gün n 95, işaretli medyan +4,9%, kâr oranı %65, işaretli eşli fark +1,6%; 5 gün n 150, işaretli medyan +1,1%, kâr oranı %57, işaretli eşli fark +1,3%; 60 gün n 42, işaretli medyan -9,4%, kâr oranı %36, işaretli eşli fark -1,2%.

### FIFO: yayımlanan lot alımları -> sonraki yayımlanan lot satışları

Alım satırı 314, satış satırı 356; alınan 4750609440,01 lot, eşlenen 2430963616,00 (kapsam %51); eşleşmeyen satış 4284139092,31 lot (BofA'nın listede görünmeyen eski pozisyonu ya da açığa satış). Açıkta kalan alım: {"lot": 2319645824.01, "n": 153, "ret_lot_agirlik": -0.30318986526389663}.

| küme | eşleşme | hisse | lot ağırlıklı getiri | medyan | ortalama | kârlı (adet / lot) | tutma medyan (gün) | P(>= +%30) | P(<= -%30) |
|---|---|---|---|---|---|---|---|---|---|
| tum | 302 | 50 | -6,6% | -4,3% | -8,3% | %35 / %39 | 15,00 | %3 | %15 |
| kesik_ici | 72 | 26 | -0,3% | -0,6% | +1,1% | %44 / %52 | 8,00 | %4 | %0 |
| kriz_sonrasi | 230 | 44 | -8,9% | -7,5% | -11,3% | %33 / %35 | 17,00 | %3 | %20 |

FIFO hisse bazında (en çok eşlenen TL, BİLGİ): YKBNK 14 eşleşme, +1,3%, tutma 16,00 g; ISCTR 17 eşleşme, -0,5%, tutma 12,00 g; EREGL 9 eşleşme, -11,8%, tutma 16,00 g; SASA 28 eşleşme, -4,8%, tutma 11,50 g; THYAO 1 eşleşme, +1,7%, tutma 2,00 g; EKGYO 3 eşleşme, -5,5%, tutma 2,00 g; TRALT 5 eşleşme, -8,4%, tutma 41,00 g; PEKGY 10 eşleşme, -0,0%, tutma 4,50 g; AKBNK 1 eşleşme, -2,3%, tutma 7,00 g; KTLEV 7 eşleşme, -23,3%, tutma 11,00 g.

Hisse bazında 20 gün (en az 3 satır, BİLGİ): CANTE n 7 medyan -7,2% eşli -0,5%; ASELS n 4 medyan -0,1% eşli +0,3%; EREGL n 4 medyan -11,0% eşli -11,3%; ISCTR n 4 medyan +7,8% eşli +8,5%; KCHOL n 4 medyan -6,2% eşli -0,3%; PETKM n 4 medyan -3,3% eşli -2,9%; ADESE n 3 medyan -5,9% eşli -2,7%; EKGYO n 3 medyan +3,2% eşli +4,0%; FROTO n 3 medyan +18,1% eşli +3,3%; HEKTS n 3 medyan -6,3% eşli -5,0%; SAHOL n 3 medyan +10,0% eşli -1,0%; THYAO n 3 medyan +3,9% eşli -4,7%.

Kriz sonrası maliyetli alım satırları (BİLGİ, ilk 12 / 286): AGROT 2026-09-02 maliyet 1,99 r5 -0,8% r20 -35,0%; ALVES 2026-09-02 maliyet 1,31 r5 +1,7% r20 -57,2%; BTCIM 2026-09-02 maliyet 3,81 r5 +3,0% r20 -51,2%; CEMZY 2026-09-02 maliyet 14,18 r5 +5,8% r20 -59,8%; KTLEV 2026-09-02 maliyet 51,34 r5 -26,0% r20 -81,3%; THYAO 2026-09-03 maliyet 294,08 r5 +1,8% r20 -2,6%; ISCTR 2026-09-03 maliyet 13,03 r5 +5,4% r20 -4,0%; SASA 2026-09-03 maliyet 2,26 r5 +22,6% r20 -15,0%; ALVES 2026-09-03 maliyet 1,25 r5 -3,9% r20 -57,6%; BLCYT 2026-09-03 maliyet 2,23 r5 -1,4% r20 -21,6%; ENERY 2026-09-04 maliyet 10,68 r5 +14,0% r20 +27,7%; EREGL 2026-09-04 maliyet 36,86 r5 +6,9% r20 +0,4%.

## 2. B — KARAR TABLOSU (ANA yol G1C1: tetik gün içi haberi ve yayın veri gününde 17:30 TR'den önce -> veri günü KAPANIŞI (giriş anı 18:10); değilse yayından sonraki ilk işlem günü AÇILIŞI (bi_giris_gunu; giriş anı 10:00); çıkış BOFA_IZI tutma dönemi kuralı: G1 giriş anından SONRA yayımla...)

| satır | koşul | n | eşli fark ort. [%95] | sıra | portföy / rastgele %90 | A (2023-24) / B (2025-26) | p | BH | KARAR | tutmayan |
|---|---|---|---|---|---|---|---|---|---|---|
| K1 | BofA günlük hacim payı >= %20 (tetik satırında pay yazılı) | 15 | +16,9% [-2,2%, +48,2%] | 0,61 | +35% / +19% | — (n 0) / +16,9% (n 15) | 0,12 | yok | **yol yok** | n = 15 < 30 (örneklem yetersiz); BH q = 0,10 ile reddedilmedi |
| K2 | kovalamama: G1 giriş fiyatı / tetik satırındaki BofA maliyeti - 1 <= + | 57 | +1,5% [-1,1%, +4,5%] | 0,53 | +21% / +24% | — (n 0) / +1,5% (n 57) | 0,14 | yok | **yol yok** | bootstrap %95 alt uç <= 0; portföy rastgele eş portföylerin %90'ını geçmedi; iki alt dönemde de > 0 değil; BH q = 0,10 ile reddedilmedi |
| K3 | birikim: veri günü dahil son 5 işlem gününde (veri günü - 4 .. veri gü | 747 | +0,1% [-0,3%, +0,6%] | 0,51 | +105% / +133% | +0,2% (n 325) / +0,1% (n 422) | 0,25 | yok | **yol yok** | bootstrap %95 alt uç <= 0; portföy rastgele eş portföylerin %90'ını geçmedi; BH q = 0,10 ile reddedilmedi |
| K4 | dönüş: tetik yayınından ÖNCE ve veri gününden 20 işlem günü önceki gün | 1465 | +0,1% [-0,4%, +0,7%] | 0,51 | +261% / +337% | -0,3% (n 667) / +0,4% (n 798) | 0,38 | yok | **yol yok** | bootstrap %95 alt uç <= 0; portföy rastgele eş portföylerin %90'ını geçmedi; iki alt dönemde de > 0 değil; BH q = 0,10 ile reddedilmedi |
| K5 | çökmüş: G1 giriş gününden önceki kapanış / önceki 250 günün en yüksek  | 31 | -4,0% [-17,6%, +7,9%] | 0,51 | +1% / +33% | +2,6% (n 7) / -6,0% (n 24) | 0,73 | yok | **yol yok** | ortalama eşli fark <= 0; bootstrap %95 alt uç <= 0; portföy rastgele eş portföylerin %90'ını geçmedi; iki alt dönemde de > 0 değil; BH q = 0,10 ile reddedilmedi |
| K6 | lot sıralı liste (tetik satırı birim lot) | 87 | -0,8% [-5,1%, +2,3%] | 0,50 | +1% / +26% | — (n 0) / -0,8% (n 87) | 0,68 | yok | **yol yok** | ortalama eşli fark <= 0; bootstrap %95 alt uç <= 0; ortalama sıra <= 0,50; portföy rastgele eş portföylerin %90'ını geçmedi; iki alt dönemde de > 0 değil; BH q = 0,10 ile reddedilmedi |
| TUM | TÜMÜ (koşulsuz) | 1620 | +0,6% [-0,3%, +1,6%] | 0,51 | +388% / +320% | -0,1% (n 741) / +1,2% (n 879) | 0,11 | yok | **yol yok** | bootstrap %95 alt uç <= 0; iki alt dönemde de > 0 değil; BH q = 0,10 ile reddedilmedi |

## 3. OLASILIK TABLOSU (ana tablo; kat = olay / aynı gün aynı hücre eşleri)

| satır | dönem n | dönem getirisi ort. / medyan | P(dönem >= +%50) | eş | kat | P(dönemde -%30'a dokunma) | 20g n | P(+%50, 20g) | kat | P(-%30, 20g) | kat | r20 ort. / eş |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K1 | 15 | +23,2% / +0,9% | %7 | %3 | 2,01 | %7 | 12 | %0 | 0,00 | %0 | 0,00 | -0,9% / +1,1% |
| K2 | 57 | +2,9% / -0,6% | %4 | %1 | 2,84 | %2 | 43 | %2 | 0,60 | %0 | 0,00 | -0,7% / +2,4% |
| K3 | 747 | +0,9% / -0,2% | %0 | %0 | 0,51 | %0 | 212 | %1 | 0,42 | %2 | 0,68 | +1,6% / +2,1% |
| K4 | 1465 | +1,1% / +0,0% | %0 | %0 | 0,41 | %1 | 375 | %1 | 0,38 | %3 | 1,02 | +1,3% / +2,3% |
| K5 | 31 | +0,8% / -1,5% | %3 | %4 | 0,86 | %19 | 25 | %4 | 1,19 | %20 | 5,96 | -5,3% / +0,3% |
| K6 | 87 | -0,1% / -0,7% | %3 | %2 | 2,28 | %5 | 62 | %5 | 1,21 | %2 | 0,40 | -0,5% / -0,2% |
| TUM | 1620 | +2,5% / +0,0% | %1 | %1 | 1,14 | %2 | 533 | %4 | 1,11 | %3 | 0,90 | +2,5% / +1,9% |

12 ay +%100 olasılığı bu veride ölçülmedi (maliyetli listeler 2025-26, kriz kesiği): 20 gün ve dönem olasılıkları yazıldı.

## 4. Yol varyantları ve duyarlılık (BİLGİ; eşli fark ort. [%95], n)

| satır | G1C1 (ANA) | G1C2 (20 gün) | G2C1 (ertesi açılış) | G2C2 | düz yazı hariç (G1C1) | tamamlayıcı (koşul yok, G1C1) | süre medyan | geç kalma medyan |
|---|---|---|---|---|---|---|---|---|
| K1 | +16,9% [-2,2%, +48,2%] n 15 | -3,0% [-8,2%, +2,8%] n 13 | +14,3% [-1,9%, +39,8%] n 15 | -3,1% [-8,2%, +2,6%] n 13 | +16,9% [-2,2%, +48,2%] n 15 | +1,3% [-0,5%, +3,6%] n 85 | 5,00 | +0,3% |
| K2 | +1,5% [-1,1%, +4,5%] n 57 | -2,7% [-5,6%, +2,6%] n 50 | +1,0% [-1,6%, +4,3%] n 57 | -3,3% [-7,1%, +2,3%] n 50 | +1,5% [-1,1%, +4,5%] n 57 | -3,7% [-5,4%, -2,0%] n 2 | 7,00 | -0,1% |
| K3 | +0,1% [-0,3%, +0,6%] n 747 | +0,7% [-0,7%, +2,0%] n 720 | +0,1% [-0,3%, +0,6%] n 747 | +0,6% [-0,7%, +2,0%] n 720 | +0,1% [-0,3%, +0,5%] n 729 | +0,6% [-0,4%, +1,9%] n 1244 | 3,00 | -0,1% |
| K4 | +0,1% [-0,4%, +0,7%] n 1465 | +0,5% [-0,8%, +1,8%] n 1424 | +0,0% [-0,5%, +0,6%] n 1466 | +0,5% [-0,8%, +1,7%] n 1425 | +0,2% [-0,3%, +0,7%] n 1434 | +3,7% [-3,2%, +10,4%] n 193 | 3,00 | +0,1% |
| K5 | -4,0% [-17,6%, +7,9%] n 31 | -6,5% [-15,4%, -0,6%] n 33 | -4,5% [-18,0%, +7,7%] n 31 | -7,4% [-15,7%, -1,6%] n 33 | -2,6% [-17,6%, +9,3%] n 29 | +0,8% [-0,0%, +1,9%] n 1583 | 14,00 | -0,2% |
| K6 | -0,8% [-5,1%, +2,3%] n 87 | -1,5% [-4,3%, +1,1%] n 83 | -2,4% [-8,1%, +1,1%] n 88 | -2,7% [-5,5%, -0,0%] n 84 | +0,4% [-2,9%, +3,3%] n 81 | +0,7% [-0,2%, +1,8%] n 1554 | 6,00 | -0,0% |
| TUM | +0,6% [-0,3%, +1,6%] n 1620 | +0,3% [-0,9%, +1,5%] n 1601 | +0,5% [-0,3%, +1,6%] n 1621 | +0,3% [-0,9%, +1,4%] n 1602 | +0,7% [-0,1%, +1,6%] n 1583 | — | 3,00 | +0,0% |

## 5. İkincil: FI_OLCUT 60 gün (giriş ertesi açılış, 60 günde tek olay)

| satır | n (60g) | eşli fark [%95] | sıra | portföy / rastgele %90 | A / B | karar (ikincil) |
|---|---|---|---|---|---|---|
| K1 | 11 | -10,7% [-15,9%, -6,3%] | 0,41 | -4% / +22% | — / -10,7% | kanıt yok |
| K2 | 29 | -9,8% [-17,3%, +4,3%] | 0,43 | +13% / +67% | — / -9,8% | kanıt yok |
| K3 | 190 | -0,6% [-4,7%, +3,4%] | 0,54 | +270% / +265% | +0,9% / -2,2% | kanıt yok |
| K4 | 336 | -0,8% [-4,4%, +3,0%] | 0,52 | +206% / +331% | -2,7% / +1,5% | kanıt yok |
| K5 | 19 | -21,9% [-36,8%, -8,2%] | 0,35 | -31% / +26% | -22,8% / -21,5% | kanıt yok |
| K6 | 34 | -8,0% [-16,4%, +1,6%] | 0,42 | -0% / +51% | — / -8,0% | kanıt yok |
| TUM | 460 | -1,2% [-4,2%, +2,1%] | 0,51 | +302% / +418% | -2,6% / +0,2% | kanıt yok |

## 6. Kriz sonrası BofA dönemleri (giriş >= 01.09.2026, TÜMÜ, G1C1; BİLGİ, karara girmez). 202 dönem, 30 açık

| hisse | tetik haberi | tür / sıra / birim | BofA maliyet | giriş (tür) | durum | dönem getirisi | eş | en düşük | en yüksek | bugüne | koşullar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BLCYT | 2026-09-03 15:00 | gun_ici / 3 / lot | 2,23 | 2026-09-03 (kapanis) | AÇIK | -35,4% | -39,2% | -43,8% | +8,4% | -35,4% | 256 |
| TERA | 2026-09-15 19:38 | gun_sonu / 3 / TL | — | 2026-09-16 (acilis) | AÇIK | -95,3% | -36,7% | -95,3% | +0,1% | -95,3% | 4 |
| DAPGM | 2026-09-21 18:30 | gun_sonu / 3 / lot | 5,10 | 2026-09-22 (acilis) | AÇIK | -44,1% | -22,9% | -61,9% | +2,2% | -41,9% | 256 |
| BALSU | 2026-10-01 12:36 | gun_ici / 2 / lot | 7,18 | 2026-10-01 (kapanis) | AÇIK | -7,1% | -19,9% | -9,0% | +26,3% | -6,7% | 256 |
| PSGYO | 2026-10-01 12:36 | gun_ici / 3 / lot | 1,63 | 2026-10-01 (kapanis) | AÇIK | -13,5% | -19,8% | -42,4% | +5,3% | -8,2% | 246 |
| MGROS | 2026-10-02 12:31 | gun_ici / 3 / TL | — | 2026-10-02 (kapanis) | AÇIK | -7,8% | -11,4% | -20,9% | +1,5% | -7,7% | 34 |
| SKBNK | 2026-10-05 12:33 | gun_ici / 3 / lot | 5,12 | 2026-10-05 (kapanis) | AÇIK | -25,5% | -7,8% | -45,6% | +3,3% | -25,3% | 2456 |
| AEFES | 2026-10-06 12:45 | gun_ici / 2 / TL | — | 2026-10-06 (kapanis) | AÇIK | -11,6% | -8,5% | -17,8% | +1,0% | -11,6% | — |
| ODINE | 2026-10-20 12:31 | gun_ici / 2 / TL | — | 2026-10-20 (kapanis) | AÇIK | -10,3% | -12,7% | -42,0% | +33,0% | -6,5% | 5 |
| ZOREN | 2026-10-21 19:37 | gun_sonu / 3 / lot | 1,53 | 2026-10-22 (acilis) | AÇIK | +3,4% | +3,6% | -29,5% | +4,7% | +2,7% | 246 |
| SELEC | 2026-10-22 12:45 | gun_ici / 3 / TL | — | 2026-10-22 (kapanis) | AÇIK | +41,4% | +19,7% | -9,7% | +45,5% | +52,2% | 45 |
| INFO | 2026-10-28 15:00 | gun_ici / 2 / lot | 0,71 | 2026-10-28 (kapanis) | AÇIK | +34,8% | +25,9% | -25,8% | +30,3% | +33,3% | 2456 |
| PGSUS | 2026-11-05 12:36 | gun_ici / 3 / TL | — | 2026-11-05 (kapanis) | AÇIK | +11,7% | +2,9% | -2,8% | +14,8% | +11,9% | 4 |
| TAVHL | 2026-11-05 12:36 | gun_ici / 2 / TL | — | 2026-11-05 (kapanis) | AÇIK | +3,1% | +3,1% | -2,3% | +6,9% | +3,2% | 4 |
| PAHOL | 2026-11-06 12:19 | gun_ici / 2 / lot | 0,74 | 2026-11-06 (kapanis) | AÇIK | +5,2% | +3,8% | -1,3% | +7,8% | +7,8% | 2346 |
| FROTO | 2026-11-06 12:31 | gun_ici / 1 / TL | — | 2026-11-06 (kapanis) | AÇIK | +0,3% | +1,4% | -1,4% | +5,0% | +1,0% | 4 |
| TCELL | 2026-11-09 12:30 | gun_ici / 1 / TL | — | 2026-11-09 (kapanis) | AÇIK | +4,6% | -0,5% | +1,2% | +7,5% | +5,2% | 4 |
| THYAO | 2026-11-09 18:11 | gun_sonu / 1 / TL | — | 2026-11-10 (acilis) | AÇIK | +1,4% | -1,0% | -0,2% | +4,6% | +3,2% | 34 |
| MARTI | 2026-11-10 12:45 | gun_ici / 3 / lot | 1,31 | 2026-11-10 (kapanis) | AÇIK | -3,1% | +0,0% | -5,3% | +3,1% | -3,1% | 2456 |
| ASTOR | 2026-11-11 12:31 | gun_ici / 3 / TL | — | 2026-11-11 (kapanis) | AÇIK | +10,5% | +7,3% | -4,2% | +10,0% | +5,8% | 34 |
| TURSG | 2026-11-10 19:34 | gun_sonu / 1 / lot | 3,40 | 2026-11-11 (acilis) | AÇIK | -3,3% | +1,4% | -5,0% | +0,6% | -2,4% | 246 |
| KTLEV | 2026-11-11 13:12 | gun_ici / 2 / lot | 6,06 | 2026-11-11 (kapanis) | AÇIK | +18,1% | +7,2% | +5,2% | +10,0% | +20,9% | 23456 |
| EREGL | 2026-11-12 12:19 | gun_ici / 3 / TL | — | 2026-11-12 (kapanis) | AÇIK | -0,1% | +0,0% | -0,1% | +0,0% | +1,3% | 4 |
| SASA | 2026-11-12 12:39 | gun_ici / 1 / lot | 1,59 | 2026-11-12 (kapanis) | AÇIK | -0,6% | -0,3% | -0,6% | +0,0% | -0,6% | 12346 |
| FRIGO | 2026-11-12 09:32 | gun_sonu / 2 / lot | — | 2026-11-12 (acilis) | AÇIK | +3,7% | +0,9% | -0,5% | +3,7% | +1,9% | 46 |
| DUNYH | 2026-11-12 09:32 | gun_sonu / 1 / lot | — | 2026-11-12 (acilis) | AÇIK | -85,3% | +0,2% | +0,0% | +0,0% | -85,1% | 6 |
| BIMAS | 2026-11-12 18:12 | gun_sonu / 3 / TL | — | 2026-11-13 (acilis) | AÇIK | +0,0% | +0,0% | +0,0% | +0,0% | +0,9% | 4 |
| CANTE | 2026-11-13 12:58 | gun_ici / 2 / lot | 1,01 | 2026-11-13 (kapanis) | AÇIK | +0,0% | +0,0% | +0,0% | +0,0% | +0,0% | 246 |
| KCHOL | 2026-11-12 18:12 | gun_sonu / 2 / TL | — | 2026-11-13 (acilis) | AÇIK | +0,0% | +0,0% | +0,0% | +0,0% | +0,7% | 34 |
| GARAN | 2026-11-13 12:45 | gun_ici / 2 / TL | — | 2026-11-13 (kapanis) | AÇIK | +0,0% | +0,0% | +0,0% | +0,0% | +0,0% | 4 |
| … 172 dönem daha (bofa_kar_sonuc.json 'kriz') | | | | | | | | | | | |

## 7. Temizlik sayımı

Kapsam satırı 26444, geçerli 24974. Düşen (ilk tutmayan neden): {"esik_alti": 317, "fiyat_paneli_yok": 557, "maliyet_bant_disi": 40, "net_yok": 326, "veri_gunu_bar_yok": 230}; yön x neden {"alim/esik_alti": 191, "alim/fiyat_paneli_yok": 306, "alim/maliyet_bant_disi": 24, "alim/net_yok": 231, "alim/veri_gunu_bar_yok": 128, "satim/esik_alti": 126, "satim/fiyat_paneli_yok": 251, "satim/maliyet_bant_disi": 16, "satim/net_yok": 95, "satim/veri_gunu_bar_yok": 102}. Düz yazı satırı 831 (geçerli 396). Geçerli maliyetli: {"alim/TL": 182, "alim/lot": 388, "satim/TL": 151, "satim/lot": 425}; payı yazılı 1398. B tetik sayımı: {"K1": {"bilinmiyor": 2854, "evet": 33, "hayir": 247}, "K2": {"bilinmiyor": 2911, "evet": 214, "hayir": 9}, "K3": {"bilinmiyor": 0, "evet": 1473, "hayir": 1661}, "K4": {"bilinmiyor": 0, "evet": 2749, "hayir": 385}, "K5": {"bilinmiyor": 83, "evet": 89, "hayir": 2962}, "K6": {"bilinmiyor": 0, "evet": 248, "hayir": 2886}}.

## 8. Sınırlar

AKD kodu kurum kimliği değildir (müşteri akışı; BofA'nın kendi pozisyonu değil). Liste ilk 5-10 ile sınırlı: BofA'nın listede görünmeyen alım / satımları yok; FIFO yalnız yayımlanmış lot listeleriyle, kapsamı düşüktür. Maliyet yalnız bazı hisse.net / YatırımX listelerinde yazılı (çoğu 2025-26). Gün içi maliyet o saate kadarki ortalamadır. Fiyatlar Yahoo bölünme düzeltmeli: bölünme öncesi maliyet bant dışı kalır ve düşer. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı). İşlem maliyeti / kayma yok.

Kapsam dışı BofA satırları (haberdeki 2. ve sonraki listeler, aylık): {"blok_2_ve_sonrasi": 93, "maliyetli": 36, "satir": 205, "tur_disi": {"aylik": 103, "donemsel": 9}}.

AKD verisi yalnız BIST'te: CLAUDE.md karar hücreleri (ABD 2023 / 2024-26, Avrupa 2023 / 2024-26) bu soruda yoktur; en iyi sonuç 'BIST-ADAY' olur, İZ değildir. Kırılımlar ve varyantlar çoklu karşılaştırmadır.

Mühür f50d11088ccb; kapı {"commit": "fd3e980c7f87e46efb76d3be65fe67160c60c41b", "commit_zamani": "2026-11-13T16:38:19+00:00"}; SAPMA: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi. Son veri 2026-11-13.

## 9. Denetim notu (ölçümden sonra; gösterim, SAPMA değil; karar değişmez)

- 01.09.2026 11:40 hisse.net 'Bank of America Ağustos'ta bu BIST hisselerine milyarlar yatırdı' haberi AYLIK özettir; ayrıştırıcı gün içi liste ve 'lot' birimli okudu (tutarlar TL; maliyet Ağustos ortalaması). Etkisi: A'da 7 kriz sonrası satır, B'de 2 kriz sonrası tetik (TRALT, ASTOR; kesik dışı, karara girmez) ve FIFO'nun lot toplamları (alınan / eşleşmeyen lot ve kapsam şişkin). Bu haber hariç FIFO (denetim yeniden hesabı): 84 eşleşme, lot ağırlıklı -%3,2, medyan -%2,2, kârlı %37, kapsam %40; yine yalnız kriz sonrası. 17.06.2025 YatırımX 'TERA bastırıyor' gibi bazı lot etiketli satırlar da TL tutarı olabilir; lot ağırlıkları bu yüzden kaba.
- DUNYH (12.11.2026) giriş fiyatı bayat Yahoo fiyatı (giriş günü hacim 0, Ç171'de işaretlendi); -%85 gerçek değildir.
