# GOZ_ETIKET — AŞAMA C RAPORU (ölçüm, eğitim, göz skoru, hakem seti)

GOZ_ETIKET v1.0 (2026-11-17): AŞAMA A örneklem (300, tohum 11) + kör PNG (t sonrası yok) + F1-F18 özellik + ön kayıt · GE_C_ESIK sha `f7031494f3f4e088…` · 2026-11-17 20:56:07 UTC

Etiketleyen bir DİL MODELİDİR (Cemal'in gözünün vekili); Cemal'in kendi etiketi değildir. Aşağıdaki her sonuç bu vekilin sonucudur.

## 1. ÖZET

- Etiket dağılımı (300): OLUR 6 · BELİRSİZ 51 · OLMAZ 243. Ölçü dışı (h5 / eş ölçülemedi): 0.
- ÖLÇÜ 1 (OLUR vs OLMAZ, ön kayıt): **ÖLÇÜLEMEDİ** (OLUR n 6 < 30).
- ÖLÇÜ 1b (SAPMA-1, OLMAZ-DEĞİL vs OLMAZ): **TUTMADI** (KAT5 alt uç > 1: hayır; +%5 payı farkı Fisher p < 0,05 ve yön: hayır; stop payı < eş: evet).
- EĞİTİM (OLMAZ-DEĞİL / OLMAZ, F1-F18 lojistik): 5 kat CV AUC (kat dışı havuz) 0,673; kat ortalaması 0,685 ± 0,052; etiket permütasyonu p 0,005 (permütasyon %95 0,595).
- GÖZ SKORU (üst beşte bir, YAPI_HEDEF karar kuralı): ETİKET **ÖLÇÜLEMEDİ** (bütün olaylar: ÖLÇÜLEMEDİ; dış örneklem: ÖLÇÜLEMEDİ).

## 2. SAPMA-1 (ölçümden önce yazıldı ve commit edildi; ON_KAYIT.md)

OLUR n = 6 < 30 olduğundan ölçü 1 kuralla ÖLÇÜLEMEDİ. Eklenen ölçü 1b: OLMAZ-DEĞİL (OLUR + BELİRSİZ) vs OLMAZ; eğitim hedefi OLMAZ-DEĞİL (1) / OLMAZ (0). Ayrıntı ve eşikler ON_KAYIT.md SAPMA-1 bölümünde.

## 3. ETİKET DAĞILIMI ve NEDEN KODU SIKLIĞI

| Karar | n |
|---|---|
| OLUR | 6 |
| BELİRSİZ | 51 |
| OLMAZ | 243 |

| Kod | n | açılım |
|---|---|---|
| C1+ | 37 | C1+ taban net (hat >= 3 dokunuş, aynı seviye, eğim aşağı değil): UYUYOR (lehte) |
| C1- | 4 | C1- taban net (hat >= 3 dokunuş, aynı seviye, eğim aşağı değil): UYMUYOR (aleyhte) |
| C2+ | 28 | C2+ dip savunulmuş (dipler kırılmamış, alçalan dip yok): UYUYOR (lehte) |
| C2- | 22 | C2- dip savunulmuş (dipler kırılmamış, alçalan dip yok): UYMUYOR (aleyhte) |
| C3+ | 41 | C3+ mumlar küçük (fitiller dahil, öncesine göre): UYUYOR (lehte) |
| C3- | 33 | C3- mumlar küçük (fitiller dahil, öncesine göre): UYMUYOR (aleyhte) |
| C4- | 17 | C4- mum şekli (alt fitil kısa, açılış dibe yakın): UYMUYOR (aleyhte) |
| C5+ | 95 | C5+ kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli): UYUYOR (lehte) |
| C5- | 147 | C5- kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli): UYMUYOR (aleyhte) |
| C6+ | 37 | C6+ büyük desen (120-250 bar yükselen / yatay; alçalan kanal değil): UYUYOR (lehte) |
| C6- | 112 | C6- büyük desen (120-250 bar yükselen / yatay; alçalan kanal değil): UYMUYOR (aleyhte) |
| C7+ | 11 | C7+ yapı boyu (düşüşe göre yeterli): UYUYOR (lehte) |
| C7- | 98 | C7- yapı boyu (düşüşe göre yeterli): UYMUYOR (aleyhte) |
| C8- | 19 | C8- kağıt hafızası (önceki benzer yapılar): UYMUYOR (aleyhte) |
| C9+ | 69 | C9+ kubbe / çanak (sağ kenar dönmüş): UYUYOR (lehte) |
| C10- | 76 | C10- yol almış (fiyat tabandan çoktan uzaklaşmış): UYMUYOR (aleyhte) |
| C11+ | 26 | C11+ stop uzaklığı (kapanış hattan %10 içinde): UYUYOR (lehte) |
| C11- | 173 | C11- stop uzaklığı (kapanış hattan %10 içinde): UYMUYOR (aleyhte) |
| C12- | 26 | C12- çekiştirme / oluşum yok (yapı yok): UYMUYOR (aleyhte) |
| C13- | 78 | C13- dev mum / şüphe (geçmişte dev tek mum): UYMUYOR (aleyhte) |

## 4. ÖLÇÜ 1 (ön kayıt) — OLUR vs OLMAZ

| Grup | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| OLUR | 6 | %0,0 | %30,1 | 0,00 [0,00; 0,00] | %0,0 | %33,3 / %36,0 | -%3,25 |
| OLMAZ | 243 | %38,7 | %40,9 | 0,94 [0,81; 1,08] | %14,8 | %33,7 / %27,6 | -%2,40 |

Fisher (+%5 payı, iki yönlü) p = 0,086. KARAR: **ÖLÇÜLEMEDİ** (OLUR n 6 < 30; olaylar tek tek aşağıda, bulgu değildir).

| No | pazar | dönem | +%5 | eş +%5 | stop önce | getiri |
|---|---|---|---|---|---|---|
| 2 | ABD | 2023 | 0 | %9,0 | 0 | %1,2 |
| 50 | AVR | 2024-26 | 0 | %17,2 | 0 | -%4,1 |
| 92 | AVR | 2024-26 | 0 | %51,7 | 1 | -%5,2 |
| 222 | ABD | 2023 | 0 | %21,0 | 1 | -%6,4 |
| 231 | AVR | 2023 | 0 | %45,2 | 0 | %1,6 |
| 255 | ABD | 2024-26 | 0 | %36,4 | 0 | -%2,4 |

## 5. ÖLÇÜ 1b (SAPMA-1) — OLMAZ-DEĞİL vs OLMAZ

| Grup | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| OLMAZ-DEĞİL | 57 | %29,8 | %38,8 | 0,77 [0,44; 1,05] | %10,5 | %15,8 / %20,7 | %0,31 |
| OLMAZ | 243 | %38,7 | %40,9 | 0,94 [0,81; 1,08] | %14,8 | %33,7 / %27,6 | -%2,40 |

Fisher (+%5 payı, iki yönlü) p = 0,227. Şartlar: KAT5 alt uç > 1 HAYIR; pay farkı (p < 0,05 ve yön) HAYIR; stop önce < eş EVET. KARAR: **TUTMADI**.

Pazar / dönem kırılımı (bilgi; hücreler küçük):

| Grup | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| ABD OLMAZ-DEĞİL | 24 | %33,3 | %44,3 | 0,75 [0,31; 1,12] | %12,5 | %16,7 / %25,3 | -%1,06 |
| ABD OLMAZ | 116 | %42,2 | %42,0 | 1,01 [0,83; 1,19] | %14,7 | %28,4 / %25,7 | -%0,68 |
| AVR OLMAZ-DEĞİL | 31 | %25,8 | %32,7 | 0,79 [0,30; 1,23] | %9,7 | %12,9 / %17,5 | %1,43 |
| AVR OLMAZ | 69 | %27,5 | %28,3 | 0,97 [0,58; 1,39] | %7,2 | %27,5 / %23,0 | -%4,70 |
| BIST OLMAZ-DEĞİL | 2 | %50,0 | %66,0 | 0,76 [0,00; 1,64] | %0,0 | %50,0 / %16,0 | -%2,38 |
| BIST OLMAZ | 58 | %44,8 | %53,8 | 0,83 [0,61; 1,06] | %24,1 | %51,7 / %36,8 | -%3,13 |
| 2023 OLMAZ-DEĞİL | 22 | %31,8 | %40,7 | 0,78 [0,00; 1,08] | %18,2 | %13,6 / %19,6 | %1,40 |
| 2023 OLMAZ | 98 | %29,6 | %40,0 | 0,74 [0,50; 0,93] | %15,3 | %33,7 / %28,1 | -%4,74 |
| 2024-26 OLMAZ-DEĞİL | 35 | %28,6 | %37,6 | 0,76 [0,35; 1,21] | %5,7 | %17,1 / %21,4 | -%2,12 |
| 2024-26 OLMAZ | 145 | %44,8 | %41,6 | 1,08 [0,92; 1,24] | %14,5 | %33,8 / %27,2 | -%0,33 |

Karar grubu başına (bilgi):

| Grup | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| OLUR | 6 | %0,0 | %30,1 | 0,00 [0,00; 0,00] | %0,0 | %33,3 / %36,0 | -%3,25 |
| BELİRSİZ | 51 | %33,3 | %39,8 | 0,84 [0,48; 1,15] | %11,8 | %13,7 / %18,9 | %0,57 |
| OLMAZ | 243 | %38,7 | %40,9 | 0,94 [0,81; 1,08] | %14,8 | %33,7 / %27,6 | -%2,40 |

## 6. ÖLÇÜ 2 — NEDEN KODLARI (bilgi; BH q 0,10, Fisher iki yönlü)

| Kod | açılım | n var / yok | +%5 var / yok | KAT5 var [%95] | stop önce var / yok | p | BH |
|---|---|---|---|---|---|---|---|
| C1+ | taban net (hat >= 3 dokunuş, aynı seviye, eğim aşağı değil) | 37 / 263 | %48,6 / %35,4 | 1,21 [0,84; 1,56] | %32,4 / %30,0 | 0,145 | - |
| C1- | taban net (hat >= 3 dokunuş, aynı seviye, eğim aşağı değil) | 4 / 296 (n az) | %25,0 / %37,2 | 0,90 [0,00; 1,74] | %25,0 / %30,4 | 1,000 | - |
| C2+ | dip savunulmuş (dipler kırılmamış, alçalan dip yok) | 28 / 272 (n az) | %35,7 / %37,1 | 0,98 [0,45; 1,51] | %17,9 / %31,6 | 1,000 | - |
| C2- | dip savunulmuş (dipler kırılmamış, alçalan dip yok) | 22 / 278 (n az) | %50,0 / %36,0 | 1,25 [0,85; 1,74] | %36,4 / %29,9 | 0,251 | - |
| C3+ | mumlar küçük (fitiller dahil, öncesine göre) | 41 / 259 | %31,7 / %37,8 | 0,77 [0,40; 1,15] | %36,6 / %29,3 | 0,491 | - |
| C3- | mumlar küçük (fitiller dahil, öncesine göre) | 33 / 267 | %33,3 / %37,5 | 0,89 [0,42; 1,37] | %39,4 / %29,2 | 0,706 | - |
| C4- | mum şekli (alt fitil kısa, açılış dibe yakın) | 17 / 283 (n az) | %23,5 / %37,8 | 0,68 [0,16; 1,38] | %41,2 / %29,7 | 0,306 | - |
| C5+ | kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli) | 95 / 205 | %32,6 / %39,0 | 0,83 [0,60; 1,03] | %26,3 / %32,2 | 0,306 | - |
| C5- | kırılım mumu belirgin (kapanış tavanı net aşmış, gövdeli) | 147 / 153 | %38,1 / %35,9 | 1,00 [0,77; 1,24] | %28,6 / %32,0 | 0,721 | - |
| C6+ | büyük desen (120-250 bar yükselen / yatay; alçalan kanal değil) | 37 / 263 | %16,2 / %39,9 | 0,52 [0,16; 0,95] | %18,9 / %31,9 | 0,006 | - |
| C6- | büyük desen (120-250 bar yükselen / yatay; alçalan kanal değil) | 112 / 188 | %44,6 / %32,4 | 0,96 [0,81; 1,12] | %33,9 / %28,2 | 0,036 | - |
| C7+ | yapı boyu (düşüşe göre yeterli) | 11 / 289 (n az) | %27,3 / %37,4 | 0,88 [0,00; 1,73] | %9,1 / %31,1 | 0,752 | - |
| C7- | yapı boyu (düşüşe göre yeterli) | 98 / 202 | %35,7 / %37,6 | 0,76 [0,57; 0,93] | %40,8 / %25,2 | 0,799 | - |
| C8- | kağıt hafızası (önceki benzer yapılar) | 19 / 281 (n az) | %42,1 / %36,7 | 1,19 [0,79; 1,82] | %31,6 / %30,2 | 0,631 | - |
| C9+ | kubbe / çanak (sağ kenar dönmüş) | 69 / 231 | %39,1 / %36,4 | 1,00 [0,69; 1,32] | %15,9 / %34,6 | 0,673 | - |
| C10- | yol almış (fiyat tabandan çoktan uzaklaşmış) | 76 / 224 | %34,2 / %37,9 | 0,91 [0,56; 1,24] | %25,0 / %32,1 | 0,585 | - |
| C11+ | stop uzaklığı (kapanış hattan %10 içinde) | 26 / 274 (n az) | %23,1 / %38,3 | 0,64 [0,19; 1,18] | %19,2 / %31,4 | 0,141 | - |
| C11- | stop uzaklığı (kapanış hattan %10 içinde) | 173 / 127 | %40,5 / %32,3 | 0,97 [0,81; 1,13] | %31,2 / %29,1 | 0,183 | - |
| C12- | çekiştirme / oluşum yok (yapı yok) | 26 / 274 (n az) | %30,8 / %37,6 | 0,81 [0,33; 1,53] | %3,8 / %32,8 | 0,532 | - |
| C13- | dev mum / şüphe (geçmişte dev tek mum) | 78 / 222 | %37,2 / %36,9 | 0,90 [0,68; 1,14] | %39,7 / %27,0 | 1,000 | - |

BH q 0,10 ile geçen kod sayısı: 0 / 20.

## 7. EĞİTİM — göz sayısal özelliklerden ne kadar öğrenilebiliyor

- Hedef OLMAZ-DEĞİL (1, n 57) / OLMAZ (0, n 243); F1-F18; medyan doldurma + standartlaştırma + L2 lojistik (C = 1); her kat dönüşümleri yalnız eğitim katından (sızıntı yok; test_goz_etiket).
- 5 kat CV AUC: kat dışı havuz 0,673; katlar 0,725, 0,716, 0,735, 0,648, 0,601; etiket permütasyonu (200) ortalaması 0,499, %95'i 0,595, p 0,005.
- Bilgi, §5 asıl hedef OLUR (n 6) / OLMAZ (n 243): CV AUC 0,598 — OLUR n 6: ÖLÇÜLEMEDİ.

Katsayılar (standart birim; + = OLMAZ-DEĞİL yönü; |katsayı| sırasıyla) ve tek özellik AUC (bilgi):

| F | tanım | katsayı | tek başına AUC |
|---|---|---|---|
| F8 | bölge boyu n | 0,614 | 0,686 |
| F9 | bant | -0,449 | 0,344 |
| F14 | büyük desen eğimi | -0,432 | 0,482 |
| F18 | stop uzaklığı | -0,410 | 0,322 |
| F15 | 120 gün konumu | 0,368 | 0,629 |
| F12 | kırılım mumu gövdesi / bölge medyan mumu | 0,263 | 0,534 |
| F4 | alt fitil payı medyanı | -0,173 | 0,557 |
| F6 | üst fitil payı medyanı | -0,166 | 0,454 |
| F16 | son 250 barda KIRILDI bölge sayısı | -0,155 | 0,411 |
| F13 | kırılım günü hacmi / bölge medyan hacmi | -0,146 | 0,441 |
| F5 | açılış-dip yakınlığı | 0,142 | 0,493 |
| F7 | yeşil mum payı | 0,110 | 0,578 |
| F1 | hat dokunuş sayısı | -0,097 | 0,520 |
| F11 | kırılım mumu payı | -0,076 | 0,485 |
| F10 | net | 0,071 | 0,541 |
| F2 | hat eğimi | -0,065 | 0,535 |
| F17 | bölge öncesi 60 gün düşüş | -0,017 | 0,636 |
| F3 | bölge mum boyu medyanı / ATR250 | 0,006 | 0,521 |

## 8. GÖZ SKORU — hücre tablosu (B5 = üst beşte bir; YAPI_HEDEF karar kuralı: n >= 30, KAT5 eş alt uç > 1, stop önce < eş, plasebo KAT5 alt uç > 1; tutmazsa n >= 1.000 ya da güç >= %80 -> DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ)

Beşte bir sınırları (26.663 olay): 0,057, 0,110, 0,187, 0,317.

### BÜTÜN OLAYLAR — etiket: ÖLÇÜLEMEDİ

| Hücre | B5 n | B5 +%5 / eş | KAT5 eş [%95] | plasebo KAT5 alt | stop önce B5 / eş | B1 n | B1 +%5 / eş | B1 KAT5 | B5 vs B1 Fisher p | güç | DURUM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD 2016-22 | 2060 | %20,8 / %30,3 | 0,69 [0,61; 0,76] | 0,59 | %15,0 / %21,3 | 1211 | %48,4 / %40,2 | 1,20 | < 0,001 | %97 | DESTEKLENMEDİ |
| ABD 2023 (karar) | 251 | %22,7 / %36,7 | 0,62 [0,52; 0,73] | 0,45 | %17,5 / %26,0 | 385 | %46,2 / %42,6 | 1,09 | < 0,001 | %11 | ÖLÇÜLEMEDİ |
| ABD 2024-26 (karar) | 671 | %26,8 / %38,2 | 0,70 [0,60; 0,79] | 0,71 | %18,8 / %28,0 | 775 | %50,3 / %45,8 | 1,10 | < 0,001 | %57 | ÖLÇÜLEMEDİ |
| AVR 2016-22 | 1523 | %20,6 / %24,9 | 0,83 [0,76; 0,89] | 0,64 | %13,2 / %18,9 | 222 | %44,1 / %35,7 | 1,24 | < 0,001 | %97 | DESTEKLENMEDİ |
| AVR 2023 (karar) | 185 | %23,8 / %29,9 | 0,79 [0,62; 1,01] | 0,48 | %10,3 / %19,3 | 62 | %41,9 / %29,5 | 1,42 | 0,009 | %11 | ÖLÇÜLEMEDİ |
| AVR 2024-26 (karar) | 538 | %19,1 / %29,0 | 0,66 [0,54; 0,79] | 0,50 | %11,5 / %19,6 | 123 | %45,5 / %35,4 | 1,29 | < 0,001 | %57 | ÖLÇÜLEMEDİ |
| BIST 2016-22 | 70 | %41,4 / %42,1 | 0,98 [0,74; 1,23] | 0,62 | %25,7 / %26,1 | 1400 | %50,4 / %51,7 | 0,97 | 0,178 | %2 | ÖLÇÜLEMEDİ |
| BIST 2023 | 2 | %100,0 / %79,9 | 1,25 [1,25; 1,25] | 1,00 | %0,0 / %17,7 | 220 | %49,1 / %53,3 | 0,92 | 0,244 | %0 | ÖLÇÜLEMEDİ |
| BIST 2024-26 | 12 | %25,0 / %43,7 | 0,57 [0,00; 1,47] | 0,00 | %33,3 / %48,2 | 893 | %52,2 / %53,1 | 0,98 | 0,081 | %0 | ÖLÇÜLEMEDİ |

### DIŞ ÖRNEKLEM (300 etiketli olay çıkarılmış) — etiket: ÖLÇÜLEMEDİ

| Hücre | B5 n | B5 +%5 / eş | KAT5 eş [%95] | plasebo KAT5 alt | stop önce B5 / eş | B1 n | B1 +%5 / eş | B1 KAT5 | B5 vs B1 Fisher p | güç | DURUM |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD 2016-22 | 2060 | %20,8 / %30,3 | 0,69 [0,61; 0,76] | 0,59 | %15,0 / %21,3 | 1211 | %48,4 / %40,2 | 1,20 | < 0,001 | %97 | DESTEKLENMEDİ |
| ABD 2023 (karar) | 238 | %23,5 / %36,2 | 0,65 [0,56; 0,75] | 0,46 | %17,2 / %26,0 | 372 | %46,8 / %42,7 | 1,10 | < 0,001 | %11 | ÖLÇÜLEMEDİ |
| ABD 2024-26 (karar) | 658 | %26,7 / %38,3 | 0,70 [0,60; 0,78] | 0,70 | %19,0 / %28,1 | 763 | %49,9 / %45,8 | 1,09 | < 0,001 | %57 | ÖLÇÜLEMEDİ |
| AVR 2016-22 | 1523 | %20,6 / %24,9 | 0,83 [0,76; 0,89] | 0,64 | %13,2 / %18,9 | 222 | %44,1 / %35,7 | 1,24 | < 0,001 | %97 | DESTEKLENMEDİ |
| AVR 2023 (karar) | 175 | %24,6 / %29,6 | 0,83 [0,67; 1,07] | 0,51 | %9,7 / %19,3 | 60 | %41,7 / %29,8 | 1,40 | 0,014 | %11 | ÖLÇÜLEMEDİ |
| AVR 2024-26 (karar) | 520 | %18,8 / %29,1 | 0,65 [0,53; 0,77] | 0,51 | %11,7 / %19,5 | 121 | %45,5 / %35,1 | 1,29 | < 0,001 | %57 | ÖLÇÜLEMEDİ |
| BIST 2016-22 | 70 | %41,4 / %42,1 | 0,98 [0,74; 1,23] | 0,62 | %25,7 / %26,1 | 1400 | %50,4 / %51,7 | 0,97 | 0,178 | %2 | ÖLÇÜLEMEDİ |
| BIST 2023 | 2 | %100,0 / %79,9 | 1,25 [1,25; 1,25] | 1,00 | %0,0 / %17,7 | 208 | %50,0 / %53,5 | 0,94 | 0,498 | %0 | ÖLÇÜLEMEDİ |
| BIST 2024-26 | 12 | %25,0 / %43,7 | 0,57 [0,00; 1,47] | 0,00 | %33,3 / %48,2 | 874 | %52,3 / %53,2 | 0,98 | 0,081 | %0 | ÖLÇÜLEMEDİ |

ETİKET (muhafazakâr olan): **ÖLÇÜLEMEDİ**.

## 9. OLASILIK TABLOSU (göz skoru beşte birleri; 15 bar, giriş t+1 açılış, stop hat x 0,98; eş = aynı gün aynı kova)

### Karar pazarları (ABD + AVR, 2023 + 2024-26)

| Beşli | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| B1 | 1345 | %48,3 | %43,2 | 1,12 [1,06; 1,18] | %24,7 | %36,6 / %29,0 | -%0,93 |
| B2 | 1836 | %45,0 | %39,6 | 1,14 [1,09; 1,18] | %18,5 | %31,9 / %27,0 | -%1,51 |
| B3 | 1953 | %41,0 | %38,9 | 1,05 [0,99; 1,11] | %14,9 | %24,6 / %25,5 | -%0,26 |
| B4 | 1870 | %33,4 | %37,1 | 0,90 [0,85; 0,96] | %9,0 | %20,7 / %24,0 | -%0,07 |
| B5 | 1645 | %23,3 | %34,0 | 0,69 [0,62; 0,75] | %4,7 | %15,3 / %24,0 | %0,02 |

### Aynı, 300 etiketli olay çıkarılmış (dış örneklem)

| Beşli | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| B1 | 1316 | %48,3 | %43,2 | 1,12 [1,05; 1,18] | %24,8 | %36,6 / %29,1 | -%0,96 |
| B2 | 1804 | %45,0 | %39,6 | 1,14 [1,09; 1,18] | %18,5 | %31,8 / %27,1 | -%1,51 |
| B3 | 1896 | %41,3 | %38,9 | 1,06 [1,00; 1,12] | %15,0 | %24,5 / %25,5 | -%0,23 |
| B4 | 1802 | %33,2 | %37,2 | 0,89 [0,84; 0,95] | %9,0 | %20,6 / %23,9 | -%0,12 |
| B5 | 1591 | %23,4 | %34,0 | 0,69 [0,63; 0,75] | %4,7 | %15,3 / %24,0 | %0,17 |

### Bütün olaylar (üç pazar, 2016-26; bilgi)

| Beşli | n | +%5 payı | eş +%5 | KAT5 [%95] | +%10 payı | stop önce olay / eş | getiri medyan (takip stoplu, bilgi) |
|---|---|---|---|---|---|---|---|
| B1 | 5291 | %49,4 | %46,5 | 1,06 [1,03; 1,10] | %27,6 | %35,1 / %29,6 | -%0,36 |
| B2 | 5299 | %45,9 | %41,8 | 1,10 [1,06; 1,14] | %20,9 | %31,4 / %27,7 | -%0,41 |
| B3 | 5304 | %39,8 | %38,6 | 1,03 [0,99; 1,07] | %14,8 | %25,8 / %25,3 | -%0,07 |
| B4 | 5302 | %31,7 | %34,8 | 0,91 [0,88; 0,95] | %9,5 | %21,0 / %23,3 | -%0,17 |
| B5 | 5312 | %21,9 | %30,1 | 0,73 [0,69; 0,76] | %4,4 | %14,7 / %21,6 | %0,54 |

KAT5 = olayın +%5 payı / aynı gün aynı kovadaki eşlerin +%5 payı (1 = eşle aynı). Olasılık tablosu 15 bar standardıdır (12 ay +%100 bu ölçüde yoktur).

Etiketli olayların skor beşlisi (eğitim içi; bilgi):

| Karar | B1 | B2 | B3 | B4 | B5 |
|---|---|---|---|---|---|
| OLUR | 0 | 0 | 1 | 1 | 4 |
| BELİRSİZ | 0 | 5 | 9 | 17 | 20 |
| OLMAZ | 60 | 46 | 57 | 50 | 30 |

## 10. VERİ DENETİMİ — dev fitil (No 274 ve 300 görsel)

- No 274: sinyalden -106 bar önce O 90,26 H 239,65 L 89,49 C 90,27; mum boyu / kapanış %166,3 (pencere medyanı %2,8); komşu barların en yüksek High'ı 94,66; High / max(O, C) = 2,65. Açılış, kapanış ve dip komşularla uyumlu, yalnız High sapık: tek alanlık VERİ HATASI (gerçek işlem değil).
- 300 görselin 1'inde 120 bar penceresinde şüpheli dev fitil (High / max(O, C) ya da min(O, C) / Low > 1,5) var; bunların 1'ünde etiketleyen C13- (dev mum / şüphe) yazmış. C13- toplam 78 (fitil > 1,5 olmayan 77; C13 eşiği göz kararıdır, 1,5 kat yalnız veri hatası adayı içindir).
| No | pazar | en büyük oran | bar | karar |
|---|---|---|---|---|
| 274 | AVR | 2,65 | -106.0 | OLMAZ |

## 11. SIZINTI DENETİMİ

- Etiketler sonuç görmeden: AŞAMA B kendi raporunda anahtar / olay dosyasını açmadığını yazdı; etiket.json AŞAMA C'de değiştirilmedi (ETIKET_SHA SAPMA-1'de mühürlü, kapı C denetler).
- Özellikler t'ye kadar: AŞAMA A prefix testi (koşuda pazar başına 10 olay + test_goz_etiket).
- Göz skoru 300 etiketli olay dışında ayrı raporlandı (§8 ve §9 'dış örneklem').
- CV: doldurma ve ölçek her katta yalnız eğitim katından (test_goz_etiket 'CV sızıntısı yok').

## 12. HAKEM SETİ

arastirma_cikti/goz_etiket/GOZ_HAKEM_SET.pdf (40 sayfa; 1-20 KÖR, 21-40 AÇIK; t sonrası yok, hisse adı yok); hakem_anahtar.json GİZLİ (sayfa -> örneklem no, aşama B kararı). Yanıt: hakem_cevap_sablon.csv doldurulur (sayfa, cevap, neden) ve `python GOZ_ETIKET.py hakem --cevap-dosya DOSYA` ile iki yarı ayrı raporlanır (kör: Cohen kappa + çapraz tablo; açık: doğru / yanlış, kural başına yanlış sayımı).

## 13. SINIRLAR

- 300 etiket; OLUR yalnız 6: asıl ölçü (OLUR) ve asıl eğitim hedefi ÖLÇÜLEMEDİ. Ölçü 1b ve eğitim SAPMA-1'dir (önceden yazılı ama ön kayıttan sonra).
- Etiketleyen bir dil modeli: Cemal'in gözünün vekilidir, Cemal'in kendi kararı değildir. Hakem seti bu vekilin Cemal'le ne kadar uyuştuğunu ölçmek içindir.
- Evren bugün işlem gören hisseler (hayatta kalma yanlılığı): hedef payları yukarı yanlı okunmalı; eşler aynı evrenden olduğu için KAT daha az etkilenir.
- Veri: tek alanlık dev fitil hataları var (§10); F-özellikleri oran / medyan olduğundan tek bar etkisi sınırlı, ama C13 etiketlerini etkileyebilir.
- Takip stoplu getiri bilgi satırıdır, karar ölçüsü değildir.

## 14. YORUM (AŞAMA C ajanı; sonuç görüldükten sonra, elle eklendi; `python GOZ_ETIKET.py rapor` bu bölümü yeniden üretmez)

Sayılar yukarıda; bu bölüm yorumdur.

- Ölçü 1b 'TUTMADI' sözü kod çıktısıdır; n 57 (< 1.000, güç yetersiz) olduğundan karar dili ÖLÇÜLEMEDİ'dir. Yön ters: OLMAZ-DEĞİL +%5 payı %29,8, OLMAZ %38,7 (p 0,23).
- Göz skoru YAPI_HEDEF kuralıyla ÖLÇÜLEMEDİ (karar hücrelerinde B5 n 185-671 < 1.000, güç < %80). Kural yalnız yukarı yönü sınar. Ters yönde tutarlı bir fark var: dört karar hücresinin dördünde B5 KAT5 < 1 (0,62-0,79), üçünde %95 üst uç < 1; dış örneklemde aynı; 2016-22 bilgi hücrelerinde (n >= 1.000) DESTEKLENMEDİ. Olasılık tablosu (karar pazarları) B1 -> B5: +%5 payı %48,3 -> %23,3, KAT5 1,12 -> 0,69; stop önce payı %36,6 -> %15,3 (eş %29,0 -> %24,0).
- Okuma (önerme, ölçülmüş iz değil): vekil göz 'uzun, dar bantlı, stop'a yakın, 120 gün tepesine yakın' bölgeleri seçiyor (F8 +, F9 -, F18 -, F15 +). Bunlar düşük oynaklıklı kurulumlar: 15 barda +%5'e daha az, stop'a da daha az gidiyor. Eş kovası (momentum x likidite) oynaklığı eşlemediği için ters KAT kısmen mekaniktir (K1). Sonradan bakış (bilgi, ön kayıtsız): skor ile F18 sıra korelasyonu -0,65; F18 beşte birleri içinde de yüksek skor beşlisinin KAT5'i düşük kaldı (0,64-0,88; düşük skor 1,08-1,56). Yani fark yalnız stop uzaklığı değil, ama oynaklık eşli bir kontrolle yeniden ölçülmeden yorum yapılmamalı.
- Sonuç: bu vekil etiketiyle 'Cemal'in gözü' 15 bar +%5 hedefinde eşlerinden iyi olay seçmiyor; seçtikleri eşlerden daha az hedef yapıyor (daha az stop'la). Bu, Cemal'in kendi gözü hakkında bir sonuç değildir; hakem seti vekilin Cemal'e ne kadar benzediğini ölçecek.
