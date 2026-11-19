# S7 MAHKEME (S7 PDF'i 50 olay; No = PDF sırası)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 6. tur §C MAHKEME (getirisiz: h5 / stop / getiri OKUNMADI). Üretim: 2026-11-19 07:43:15 UTC.

Kurallar (12; NaN = ✗): Ş1 F15 <= 0,25 VE F17 <= -0,20; Ş2 F1 >= 3; Ş3 F2 >= -0,01; Ş4 F3 <= 0,90; Ş5 F4 <= 0,25; Ş6 F20 >= 0; Ş9 altı alt şart (Y11); Ş7 F22 > 0 VE F22a < 0 VE F23 >= 0,50; Ş8 F18 <= 0,20; F14 >= 0; C8 F16 = 0 (son 250 barda KIRILDI bölge sayısı); C13 max |C_k / C_k-1 - 1| (son 250 bar, k = t-249..t) <= 4 x ATR250 (ort TR / C_önceki, aynı 250 bar; 250 bar yoksa NaN = tutmaz). NaN = ✗.

Önceki adaylar: (a) S6 (s6_taban, kesik veri) bölgeleri, seçilenin bölgesi hariç, son barı [t-250, t-1] içinde ve bitişi t'ye kadar bilinen: AL (t_k = al günü; bölge = GE bölgesi), KIRILDI (t_k = kırılma günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = TAVAN(t_k-1)), ZAMAN AŞIMI / sönme (t_k = kutunun son günü; bölge [kutu_sol, t_k-1], hat = kutu_alt(t_k), tavan = kutu_ust(t_k)); (b) Ş9 çanak: t_k = t-5, t-10, ..., t-120; Ş9 t_k'da TUTARSA aday; bölge = Ş9 penceresi [t_k-40, t_k-1], hat = min Low, tavan = max High[t_k-15, t_k-1].

## ÖZET

- Olay 50; mahkeme kurulan 50; ÖNCEKİ BÖLGE DAHA UYGUN: **5** / 50; seçilen bölge her kurala uyuyor: 1 / 50; seçilen bölge özellik dosyasıyla eşit: 50 / 50.
- En sık eksik kurallar (seçilen bölgede): Ş9 U dip 44, F14 büyük resim 39, C8 kağıt hafızası 24, C13 dev mum yok 21.
- Mahkeme kurulamayan: yok.

| No | Pazar | seçilen puan | önceki aday sayısı | en iyi önceki aday (bar, tür, puan) | karar |
|---|---|---|---|---|---|
| 1 | ABD | 10/12 | 2 | bar -105, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 2 | ABD | 10/12 | 3 | bar -90, AL, 8/12 | SEÇİM TUTARLI |
| 3 | ABD | 10/12 | 9 | bar -197, AL, 10/12 | SEÇİM TUTARLI |
| 4 | ABD | 9/12 | 8 | bar -202, ZAMAN AŞIMI, 8/12 | SEÇİM TUTARLI |
| 5 | ABD | 9/12 | 8 | bar -85, AL, 9/12 | SEÇİM TUTARLI |
| 6 | ABD | 8/12 | 5 | bar -218, AL, 9/12 | ÖNCEKİ BÖLGE DAHA UYGUN |
| 7 | ABD | 9/12 | 5 | bar -54, AL, 7/12 | SEÇİM TUTARLI |
| 8 | ABD | 9/12 | 4 | bar -77, AL, 7/12 | SEÇİM TUTARLI |
| 9 | ABD | 9/12 | 4 | bar -95, Ş9 ÇANAK, 9/12 | SEÇİM TUTARLI |
| 10 | ABD | 8/12 | 5 | bar -10, Ş9 ÇANAK, 9/12 | ÖNCEKİ BÖLGE DAHA UYGUN |
| 11 | ABD | 9/12 | 5 | bar -73, AL, 8/12 | SEÇİM TUTARLI |
| 12 | ABD | 10/12 | 8 | bar -35, KIRILDI, 8/12 | SEÇİM TUTARLI |
| 13 | ABD | 11/12 | 3 | bar -40, Ş9 ÇANAK, 7/12 | SEÇİM TUTARLI |
| 14 | ABD | 11/12 | 2 | bar -10, Ş9 ÇANAK, 7/12 | SEÇİM TUTARLI |
| 15 | ABD | 9/12 | 4 | bar -65, AL, 8/12 | SEÇİM TUTARLI |
| 16 | ABD | 10/12 | 7 | bar -160, AL, 10/12 | SEÇİM TUTARLI |
| 17 | ABD | 9/12 | 7 | bar -219, ZAMAN AŞIMI, 9/12 | SEÇİM TUTARLI |
| 18 | ABD | 8/12 | 4 | bar -18, KIRILDI, 9/12 | ÖNCEKİ BÖLGE DAHA UYGUN |
| 19 | ABD | 9/12 | 9 | bar -184, AL, 9/12 | SEÇİM TUTARLI |
| 20 | ABD | 10/12 | 0 | - | SEÇİM TUTARLI |
| 21 | ABD | 10/12 | 9 | bar -221, AL, 10/12 | SEÇİM TUTARLI |
| 22 | ABD | 10/12 | 7 | bar -187, KIRILDI, 7/12 | SEÇİM TUTARLI |
| 23 | ABD | 9/12 | 4 | bar -125, KIRILDI, 6/12 | SEÇİM TUTARLI |
| 24 | ABD | 9/12 | 9 | bar -237, ZAMAN AŞIMI, 7/12 | SEÇİM TUTARLI |
| 25 | ABD | 9/12 | 6 | bar -133, KIRILDI, 8/12 | SEÇİM TUTARLI |
| 26 | ABD | 10/12 | 6 | bar -157, ZAMAN AŞIMI, 8/12 | SEÇİM TUTARLI |
| 27 | ABD | 11/12 | 7 | bar -138, ZAMAN AŞIMI, 8/12 | SEÇİM TUTARLI |
| 28 | ABD | 8/12 | 7 | bar -90, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 29 | ABD | 9/12 | 4 | bar -244, AL, 9/12 | SEÇİM TUTARLI |
| 30 | ABD | 9/12 | 4 | bar -232, AL, 8/12 | SEÇİM TUTARLI |
| 31 | ABD | 10/12 | 5 | bar -115, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 32 | AVR | 12/12 | 3 | bar -79, AL, 10/12 | SEÇİM TUTARLI |
| 33 | AVR | 9/12 | 1 | bar -103, AL, 7/12 | SEÇİM TUTARLI |
| 34 | AVR | 8/12 | 5 | bar -30, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 35 | AVR | 9/12 | 8 | bar -93, AL, 7/12 | SEÇİM TUTARLI |
| 36 | AVR | 10/12 | 9 | bar -45, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 37 | AVR | 9/12 | 8 | bar -171, KIRILDI, 8/12 | SEÇİM TUTARLI |
| 38 | AVR | 10/12 | 3 | bar -187, AL, 9/12 | SEÇİM TUTARLI |
| 39 | AVR | 9/12 | 4 | bar -32, KIRILDI, 8/12 | SEÇİM TUTARLI |
| 40 | AVR | 9/12 | 7 | bar -90, Ş9 ÇANAK, 10/12 | ÖNCEKİ BÖLGE DAHA UYGUN |
| 41 | BIST | 10/12 | 0 | - | SEÇİM TUTARLI |
| 42 | BIST | 10/12 | 4 | bar -30, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |
| 43 | BIST | 9/12 | 3 | bar -185, AL, 8/12 | SEÇİM TUTARLI |
| 44 | BIST | 10/12 | 6 | bar -59, KIRILDI, 10/12 | SEÇİM TUTARLI |
| 45 | BIST | 9/12 | 3 | bar -104, ZAMAN AŞIMI, 8/12 | SEÇİM TUTARLI |
| 46 | BIST | 10/12 | 4 | bar -69, AL, 10/12 | SEÇİM TUTARLI |
| 47 | BIST | 10/12 | 4 | bar -20, Ş9 ÇANAK, 11/12 | ÖNCEKİ BÖLGE DAHA UYGUN |
| 48 | BIST | 9/12 | 8 | bar -250, KIRILDI, 7/12 | SEÇİM TUTARLI |
| 49 | BIST | 9/12 | 6 | bar -153, AL, 9/12 | SEÇİM TUTARLI |
| 50 | BIST | 10/12 | 2 | bar -40, Ş9 ÇANAK, 8/12 | SEÇİM TUTARLI |

## OLAY SAYFALARI

### No 1 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -105)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,12, F17 %-37,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-7,7 |
| Ş2 hat net | ✓ | F1 5 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %1,0 | >= -%1 | ✓ F2 %0,5 |
| Ş4 küçük mum | ✓ | F3 0,76 | <= 0,90 | ✓ F3 0,89 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 | ✓ F4 0,21 |
| Ş6 kazan dönüş | ✓ | F20 %2,2 | >= %0 | ✓ F20 %10,3 |
| Ş9 U dip | ✓ | a/ATR 0,008, x* 0,69, R² 0,88, sol 5,89, sağ 1,17, argmin-x* 1,0 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,009, x* 0,34, R² 0,78, sol 1,58, sağ 5,85, argmin-x* 2,7 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,3, F22a %-0,1, F23 0,53 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,2, F22a %-2,6, F23 0,88 |
| Ş8 yol almamış | ✓ | F18 %9,5 | <= %20 | ✗ F18 %29,8 |
| F14 büyük resim | ✗ | F14 %-11,3 | >= %0 | ✗ F14 - |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 5,5 | <= 4 | ✗ en büyük günlük getiri / ATR - |

Önceki adaylar (2; [t-250, t-1]): bar -110 Ş9 ÇANAK 5/12; bar -105 Ş9 ÇANAK 8/12


### No 2 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -90)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,19, F17 %-23,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %0,2 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %1,2 | >= -%1 | ✓ F2 %-0,9 |
| Ş4 küçük mum | ✓ | F3 0,84 | <= 0,90 | ✓ F3 0,58 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 | ✗ F4 0,29 |
| Ş6 kazan dönüş | ✓ | F20 %3,6 | >= %0 | ✗ F20 %-0,2 |
| Ş9 U dip | ✗ | a/ATR 0,016, x* 0,86, R² 0,84, sol 18,25, sağ 0,49, argmin-x* -8,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,21, R² 0,59, sol 0,24, sağ 3,55, argmin-x* 9,0 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,3, F22a %-3,0, F23 0,85 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %1,2, F22a %-1,6, F23 0,95 |
| Ş8 yol almamış | ✓ | F18 %6,5 | <= %20 | ✓ F18 %7,8 |
| F14 büyük resim | ✓ | F14 %23,4 | >= %0 | ✓ F14 %28,7 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 7,2 | <= 4 | ✓ en büyük günlük getiri / ATR 3,5 |

Önceki adaylar (3; [t-250, t-1]): bar -105 AL 8/12; bar -90 AL 8/12; bar -29 ZAMAN AŞIMI 6/12


### No 3 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 10/12, bar -197)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-21,9 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,96, F17 %-8,8 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 6 |
| Ş3 dip savunulmuş | ✓ | F2 %1,5 | >= -%1 | ✓ F2 %0,8 |
| Ş4 küçük mum | ✓ | F3 0,74 | <= 0,90 | ✓ F3 0,59 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✓ F4 0,20 |
| Ş6 kazan dönüş | ✓ | F20 %1,5 | >= %0 | ✓ F20 %6,6 |
| Ş9 U dip | ✗ | a/ATR 0,007, x* 0,90, R² 0,85, sol 9,05, sağ 0,10, argmin-x* -2,2 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,005, x* -, R² 0,70, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,4, F22a %-1,5, F23 0,74 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %1,3, F22a %-1,4, F23 0,61 |
| Ş8 yol almamış | ✓ | F18 %9,3 | <= %20 | ✓ F18 %8,7 |
| F14 büyük resim | ✗ | F14 %-15,1 | >= %0 | ✓ F14 %33,2 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,2 | <= 4 | ✓ en büyük günlük getiri / ATR 2,2 |

Önceki adaylar (9; [t-250, t-1]): bar -233 AL 8/12; bar -197 AL 10/12; bar -130 AL 8/12; bar -108 AL 9/12; bar -100 Ş9 ÇANAK 9/12; bar -95 Ş9 ÇANAK 7/12; bar -64 ZAMAN AŞIMI 7/12; bar -40 Ş9 ÇANAK 8/12; bar -35 Ş9 ÇANAK 8/12


### No 4 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -202)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,25, F17 %-23,2 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,82, F17 %-4,5 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,3 | >= -%1 | ✓ F2 %1,1 |
| Ş4 küçük mum | ✓ | F3 0,84 | <= 0,90 | ✓ F3 0,84 |
| Ş5 alt fitil kısa | ✓ | F4 0,21 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %0,9 | >= %0 | ✓ F20 %1,1 |
| Ş9 U dip | ✗ | a/ATR 0,008, x* 0,76, R² 0,89, sol 7,22, sağ 0,74, argmin-x* -10,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,002, x* -, R² 0,78, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,6, F22a %-1,2, F23 0,50 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-10,2, F22a %-4,6, F23 0,76 |
| Ş8 yol almamış | ✓ | F18 %12,6 | <= %20 | ✓ F18 %1,9 |
| F14 büyük resim | ✓ | F14 %60,9 | >= %0 | ✓ F14 %118,9 |
| C8 kağıt hafızası | ✗ | F16 2 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,9 | <= 4 | ✓ en büyük günlük getiri / ATR 3,9 |

Önceki adaylar (8; [t-250, t-1]): bar -234 ZAMAN AŞIMI 6/12; bar -202 ZAMAN AŞIMI 8/12; bar -170 KIRILDI 7/12; bar -155 AL 6/12; bar -121 AL 6/12; bar -97 KIRILDI 6/12; bar -70 Ş9 ÇANAK 5/12; bar -34 ZAMAN AŞIMI 5/12


### No 5 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -85)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,16, F17 %-28,4 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,62, F17 %-11,8 |
| Ş2 hat net | ✓ | F1 8 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,2 | >= -%1 | ✓ F2 %1,1 |
| Ş4 küçük mum | ✓ | F3 0,80 | <= 0,90 | ✓ F3 0,67 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,19 |
| Ş6 kazan dönüş | ✓ | F20 %1,2 | >= %0 | ✓ F20 %1,1 |
| Ş9 U dip | ✗ | a/ATR 0,003, x* 0,85, R² 0,82, sol 3,70, sağ 0,12, argmin-x* -10,0 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,003, x* -, R² 0,65, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,4, F22a %-2,2, F23 0,55 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %5,3, F22a %-4,2, F23 0,97 |
| Ş8 yol almamış | ✓ | F18 %8,6 | <= %20 | ✓ F18 %16,5 |
| F14 büyük resim | ✗ | F14 %-13,2 | >= %0 | ✓ F14 %49,6 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,2 | <= 4 | ✓ en büyük günlük getiri / ATR 3,7 |

Önceki adaylar (8; [t-250, t-1]): bar -247 AL 8/12; bar -215 AL 8/12; bar -180 KIRILDI 9/12; bar -157 AL 6/12; bar -112 AL 9/12; bar -100 ZAMAN AŞIMI 6/12; bar -85 AL 9/12; bar -41 ZAMAN AŞIMI 7/12


### No 6 (ABD)

**KARAR: ÖNCEKİ BÖLGE DAHA UYGUN: bar -218 (AL), puan 9/12 vs seçilen 8/12; seçilenin tutmadığı kurallar: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok; önceki adayın tutmadığı: Ş1 dipte, Ş5 alt fitil kısa, Ş9 U dip**

Seçilen bölge (bar 0, AL): puan 8/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,14, F17 %-28,1 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,82, F17 %-8,6 |
| Ş2 hat net | ✓ | F1 5 | >= 3 | ✓ F1 10 |
| Ş3 dip savunulmuş | ✓ | F2 %0,1 | >= -%1 | ✓ F2 %-0,7 |
| Ş4 küçük mum | ✓ | F3 0,87 | <= 0,90 | ✓ F3 0,70 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✗ F4 0,25 |
| Ş6 kazan dönüş | ✓ | F20 %5,0 | >= %0 | ✓ F20 %0,7 |
| Ş9 U dip | ✗ | a/ATR 0,008, x* 0,61, R² 0,65, sol 4,59, sağ 1,84, argmin-x* -13,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,000, x* -, R² 0,02, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,0, F22a %-4,4, F23 0,98 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,0, F22a %-2,4, F23 0,74 |
| Ş8 yol almamış | ✓ | F18 %13,0 | <= %20 | ✓ F18 %11,6 |
| F14 büyük resim | ✗ | F14 %-33,1 | >= %0 | ✓ F14 %24,4 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 6,7 | <= 4 | ✓ en büyük günlük getiri / ATR 2,6 |

Önceki adaylar (5; [t-250, t-1]): bar -218 AL 9/12; bar -190 AL 8/12; bar -75 Ş9 ÇANAK 8/12; bar -64 AL 7/12; bar -53 KIRILDI 7/12


### No 7 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -54)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,13, F17 %-48,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-5,2 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,5 | >= -%1 | ✓ F2 %0,2 |
| Ş4 küçük mum | ✓ | F3 0,84 | <= 0,90 | ✓ F3 0,70 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 | ✓ F4 0,12 |
| Ş6 kazan dönüş | ✓ | F20 %6,5 | >= %0 | ✓ F20 %0,5 |
| Ş9 U dip | ✗ | a/ATR 0,017, x* 0,80, R² 0,89, sol 16,38, sağ 0,97, argmin-x* -6,4 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,008, x* -, R² 0,80, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %3,3, F22a %-1,7, F23 0,92 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %1,9, F22a %-1,1, F23 0,77 |
| Ş8 yol almamış | ✓ | F18 %12,5 | <= %20 | ✓ F18 %13,6 |
| F14 büyük resim | ✗ | F14 %-5,5 | >= %0 | ✗ F14 %-9,3 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 5,7 | <= 4 | ✗ en büyük günlük getiri / ATR 4,6 |

Önceki adaylar (5; [t-250, t-1]): bar -247 ZAMAN AŞIMI 5/12; bar -184 ZAMAN AŞIMI 6/12; bar -111 AL 6/12; bar -87 AL 4/12; bar -54 AL 7/12


### No 8 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -77)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,18, F17 %-39,7 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,46, F17 %-9,6 |
| Ş2 hat net | ✓ | F1 6 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,3 | >= -%1 | ✓ F2 %0,1 |
| Ş4 küçük mum | ✓ | F3 0,80 | <= 0,90 | ✓ F3 0,81 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %4,9 | >= %0 | ✓ F20 %4,6 |
| Ş9 U dip | ✗ | a/ATR 0,005, x* 0,57, R² 0,53, sol 2,36, sağ 1,37, argmin-x* -14,1 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,000, x* -0,46, R² 0,36, sol 0,00, sağ 1,45, argmin-x* 24,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,1, F22a %-3,0, F23 0,84 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,9, F22a %-4,7, F23 0,92 |
| Ş8 yol almamış | ✓ | F18 %14,0 | <= %20 | ✓ F18 %12,9 |
| F14 büyük resim | ✗ | F14 %-47,4 | >= %0 | ✗ F14 %-32,9 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,4 | <= 4 | ✗ en büyük günlük getiri / ATR 5,7 |

Önceki adaylar (4; [t-250, t-1]): bar -214 KIRILDI 6/12; bar -120 Ş9 ÇANAK 3/12; bar -104 AL 6/12; bar -77 AL 7/12


### No 9 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -95)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-32,5 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,35, F17 %-17,5 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,8 | >= -%1 | ✓ F2 %1,3 |
| Ş4 küçük mum | ✓ | F3 0,84 | <= 0,90 | ✓ F3 0,78 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✓ F4 0,19 |
| Ş6 kazan dönüş | ✓ | F20 %7,4 | >= %0 | ✓ F20 %8,7 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 0,62, R² 0,09, sol 0,82, sağ 0,31, argmin-x* 5,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,008, x* 0,43, R² 0,55, sol 2,13, sağ 3,69, argmin-x* -2,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,3, F22a %-0,1, F23 0,59 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-12,1, F22a %-8,5, F23 0,92 |
| Ş8 yol almamış | ✓ | F18 %13,3 | <= %20 | ✓ F18 %7,6 |
| F14 büyük resim | ✗ | F14 %-29,3 | >= %0 | ✓ F14 %10,0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 6,7 | <= 4 | ✗ en büyük günlük getiri / ATR 5,2 |

Önceki adaylar (4; [t-250, t-1]): bar -240 AL 5/12; bar -221 ZAMAN AŞIMI 4/12; bar -125 ZAMAN AŞIMI 8/12; bar -95 Ş9 ÇANAK 9/12


### No 10 (ABD)

**KARAR: ÖNCEKİ BÖLGE DAHA UYGUN: bar -10 (Ş9 ÇANAK), puan 9/12 vs seçilen 8/12; seçilenin tutmadığı kurallar: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok; önceki adayın tutmadığı: Ş7 yakın tavan gövdeli kırılım, C8 kağıt hafızası, C13 dev mum yok**

Seçilen bölge (bar 0, AL): puan 8/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,13, F17 %-43,0 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,04, F17 %-36,8 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,2 | >= -%1 | ✓ F2 %-0,2 |
| Ş4 küçük mum | ✓ | F3 0,73 | <= 0,90 | ✓ F3 0,72 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 | ✓ F4 0,19 |
| Ş6 kazan dönüş | ✓ | F20 %0,2 | >= %0 | ✓ F20 %3,5 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 0,21, R² 0,32, sol 0,06, sağ 0,85, argmin-x* 8,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,006, x* 0,60, R² 0,76, sol 3,39, sağ 1,53, argmin-x* 3,7 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,4, F22a %-1,2, F23 0,98 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-4,9, F22a %-2,6, F23 0,51 |
| Ş8 yol almamış | ✓ | F18 %14,3 | <= %20 | ✓ F18 %5,4 |
| F14 büyük resim | ✗ | F14 %-4,4 | >= %0 | ✓ F14 %7,9 |
| C8 kağıt hafızası | ✗ | F16 3 | = 0 | ✗ F16 3 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 6,6 | <= 4 | ✗ en büyük günlük getiri / ATR 6,6 |

Önceki adaylar (5; [t-250, t-1]): bar -153 KIRILDI 6/12; bar -118 ZAMAN AŞIMI 3/12; bar -94 KIRILDI 4/12; bar -54 KIRILDI 4/12; bar -10 Ş9 ÇANAK 9/12


### No 11 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -73)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,24, F17 %-21,5 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,23, F17 %-27,7 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 8 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,1 | >= -%1 | ✓ F2 %1,1 |
| Ş4 küçük mum | ✓ | F3 0,88 | <= 0,90 | ✗ F3 0,90 |
| Ş5 alt fitil kısa | ✓ | F4 0,20 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %0,2 | >= %0 | ✓ F20 %4,9 |
| Ş9 U dip | ✗ | a/ATR -0,010, x* -, R² 0,48, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,011, x* 0,60, R² 0,75, sol 6,24, sağ 2,83, argmin-x* -9,3 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,1, F22a %-5,5, F23 0,77 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,1, F22a %-1,8, F23 0,56 |
| Ş8 yol almamış | ✓ | F18 %8,8 | <= %20 | ✓ F18 %12,4 |
| F14 büyük resim | ✗ | F14 %-40,9 | >= %0 | ✗ F14 %-43,6 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 3 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,1 | <= 4 | ✓ en büyük günlük getiri / ATR 2,7 |

Önceki adaylar (5; [t-250, t-1]): bar -159 KIRILDI 4/12; bar -124 ZAMAN AŞIMI 5/12; bar -73 AL 8/12; bar -25 Ş9 ÇANAK 4/12; bar -20 Ş9 ÇANAK 4/12


### No 12 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -35)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,20, F17 %-42,8 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,00, F17 %-31,9 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %-1,0 | >= -%1 | ✓ F2 %-0,4 |
| Ş4 küçük mum | ✓ | F3 0,61 | <= 0,90 | ✓ F3 0,67 |
| Ş5 alt fitil kısa | ✓ | F4 0,21 | <= 0,25 | ✗ F4 0,30 |
| Ş6 kazan dönüş | ✓ | F20 %13,0 | >= %0 | ✓ F20 %1,1 |
| Ş9 U dip | ✓ | a/ATR 0,007, x* 0,68, R² 0,75, sol 4,88, sağ 1,09, argmin-x* -2,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,91, R² 0,86, sol 5,09, sağ 0,05, argmin-x* -2,6 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,5, F22a %-4,8, F23 0,55 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-18,1, F22a %-10,7, F23 0,57 |
| Ş8 yol almamış | ✓ | F18 %13,6 | <= %20 | ✓ F18 %-8,0 |
| F14 büyük resim | ✓ | F14 %90,3 | >= %0 | ✓ F14 %200,9 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 5,9 | <= 4 | ✗ en büyük günlük getiri / ATR 5,7 |

Önceki adaylar (8; [t-250, t-1]): bar -186 AL 7/12; bar -136 ZAMAN AŞIMI 5/12; bar -124 ZAMAN AŞIMI 5/12; bar -110 Ş9 ÇANAK 6/12; bar -105 Ş9 ÇANAK 6/12; bar -104 ZAMAN AŞIMI 6/12; bar -66 ZAMAN AŞIMI 7/12; bar -35 KIRILDI 8/12


### No 13 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 11/12 >= en iyi önceki aday 7/12, bar -40)**

Seçilen bölge (bar 0, AL): puan 11/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,25, F17 %-30,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,41, F17 %-2,1 |
| Ş2 hat net | ✓ | F1 5 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,5 | >= -%1 | ✓ F2 %-0,8 |
| Ş4 küçük mum | ✓ | F3 0,75 | <= 0,90 | ✓ F3 0,78 |
| Ş5 alt fitil kısa | ✓ | F4 0,21 | <= 0,25 | ✗ F4 0,32 |
| Ş6 kazan dönüş | ✓ | F20 %1,9 | >= %0 | ✓ F20 %2,9 |
| Ş9 U dip | ✗ | a/ATR 0,003, x* 0,93, R² 0,60, sol 3,74, sağ 0,02, argmin-x* -16,4 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,008, x* 0,51, R² 0,69, sol 3,32, sağ 3,09, argmin-x* 0,2 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,4, F22a %-1,7, F23 0,68 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-12,1, F22a %-11,2, F23 0,33 |
| Ş8 yol almamış | ✓ | F18 %12,4 | <= %20 | ✓ F18 %8,5 |
| F14 büyük resim | ✓ | F14 %11,6 | >= %0 | ✗ F14 - |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,5 | <= 4 | ✗ en büyük günlük getiri / ATR - |

Önceki adaylar (3; [t-250, t-1]): bar -80 Ş9 ÇANAK 7/12; bar -45 Ş9 ÇANAK 7/12; bar -40 Ş9 ÇANAK 7/12


### No 14 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 11/12 >= en iyi önceki aday 7/12, bar -10)**

Seçilen bölge (bar 0, AL): puan 11/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,23, F17 %-27,9 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,19, F17 %-14,9 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✗ F1 1 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,4 | >= -%1 | ✓ F2 %0,0 |
| Ş4 küçük mum | ✓ | F3 0,35 | <= 0,90 | ✓ F3 0,53 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 | ✗ F4 0,31 |
| Ş6 kazan dönüş | ✓ | F20 %0,6 | >= %0 | ✓ F20 %5,5 |
| Ş9 U dip | ✗ | a/ATR 0,003, x* 0,60, R² 0,52, sol 1,67, sağ 0,72, argmin-x* -8,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,005, x* 0,72, R² 0,91, sol 4,22, sağ 0,65, argmin-x* -3,0 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,3, F22a %-1,9, F23 0,70 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-3,2, F22a %-4,7, F23 0,29 |
| Ş8 yol almamış | ✓ | F18 %9,2 | <= %20 | ✓ F18 %11,1 |
| F14 büyük resim | ✓ | F14 %36,5 | >= %0 | ✓ F14 %28,5 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 4,0 | <= 4 | ✓ en büyük günlük getiri / ATR 3,9 |

Önceki adaylar (2; [t-250, t-1]): bar -148 AL 5/12; bar -10 Ş9 ÇANAK 7/12


### No 15 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -65)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,23, F17 %-26,1 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,55, F17 %-22,9 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,2 | >= -%1 | ✓ F2 %0,6 |
| Ş4 küçük mum | ✓ | F3 0,63 | <= 0,90 | ✓ F3 0,78 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✓ F4 0,17 |
| Ş6 kazan dönüş | ✓ | F20 %5,6 | >= %0 | ✓ F20 %1,9 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 1,17, R² 0,63, sol 2,99, sağ 0,00, argmin-x* -18,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,000, x* -, R² 0,32, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,4, F22a %-2,3, F23 0,60 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %1,4, F22a %-4,3, F23 0,85 |
| Ş8 yol almamış | ✓ | F18 %11,4 | <= %20 | ✓ F18 %12,6 |
| F14 büyük resim | ✗ | F14 %-40,0 | >= %0 | ✗ F14 %-48,9 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,3 | <= 4 | ✗ en büyük günlük getiri / ATR 4,4 |

Önceki adaylar (4; [t-250, t-1]): bar -216 AL 7/12; bar -194 ZAMAN AŞIMI 3/12; bar -171 ZAMAN AŞIMI 5/12; bar -65 AL 8/12


### No 16 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 10/12, bar -160)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,16, F17 %-33,7 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,83, F17 %-12,7 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,1 | >= -%1 | ✓ F2 %0,1 |
| Ş4 küçük mum | ✓ | F3 0,82 | <= 0,90 | ✓ F3 0,64 |
| Ş5 alt fitil kısa | ✓ | F4 0,15 | <= 0,25 | ✓ F4 0,21 |
| Ş6 kazan dönüş | ✓ | F20 %4,4 | >= %0 | ✓ F20 %0,2 |
| Ş9 U dip | ✗ | a/ATR 0,007, x* 0,86, R² 0,80, sol 7,46, sağ 0,21, argmin-x* -10,4 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,006, x* 0,50, R² 0,49, sol 2,27, sağ 2,30, argmin-x* -2,4 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,6, F22a %-3,7, F23 0,71 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,6, F22a %-3,0, F23 0,73 |
| Ş8 yol almamış | ✓ | F18 %10,1 | <= %20 | ✓ F18 %10,7 |
| F14 büyük resim | ✓ | F14 %13,7 | >= %0 | ✓ F14 %87,9 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,2 | <= 4 | ✓ en büyük günlük getiri / ATR 3,9 |

Önceki adaylar (7; [t-250, t-1]): bar -230 KIRILDI 6/12; bar -194 AL 6/12; bar -160 AL 10/12; bar -94 ZAMAN AŞIMI 7/12; bar -35 Ş9 ÇANAK 7/12; bar -30 Ş9 ÇANAK 7/12; bar -27 ZAMAN AŞIMI 6/12


### No 17 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -219)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,25, F17 %-37,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,65, F17 %-23,3 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,7 | >= -%1 | ✓ F2 %-0,8 |
| Ş4 küçük mum | ✓ | F3 0,75 | <= 0,90 | ✓ F3 0,56 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,21 |
| Ş6 kazan dönüş | ✓ | F20 %5,6 | >= %0 | ✓ F20 %4,4 |
| Ş9 U dip | ✗ | a/ATR 0,008, x* 0,50, R² 0,46, sol 2,94, sağ 2,99, argmin-x* -9,4 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,003, x* -, R² 0,61, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,2, F22a %-1,5, F23 0,60 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-9,4, F22a %-7,8, F23 0,56 |
| Ş8 yol almamış | ✓ | F18 %16,5 | <= %20 | ✓ F18 %2,4 |
| F14 büyük resim | ✗ | F14 %-8,1 | >= %0 | ✓ F14 %12,9 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,3 | <= 4 | ✓ en büyük günlük getiri / ATR 2,9 |

Önceki adaylar (7; [t-250, t-1]): bar -219 ZAMAN AŞIMI 9/12; bar -201 KIRILDI 8/12; bar -170 ZAMAN AŞIMI 6/12; bar -136 AL 8/12; bar -50 Ş9 ÇANAK 5/12; bar -45 Ş9 ÇANAK 6/12; bar -40 Ş9 ÇANAK 5/12


### No 18 (ABD)

**KARAR: ÖNCEKİ BÖLGE DAHA UYGUN: bar -18 (KIRILDI), puan 9/12 vs seçilen 8/12; seçilenin tutmadığı kurallar: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok; önceki adayın tutmadığı: Ş7 yakın tavan gövdeli kırılım, F14 büyük resim, C13 dev mum yok**

Seçilen bölge (bar 0, AL): puan 8/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,10, F17 %-21,8 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,03, F17 %-49,3 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,9 | >= -%1 | ✓ F2 %1,1 |
| Ş4 küçük mum | ✓ | F3 0,44 | <= 0,90 | ✓ F3 0,62 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✓ F4 0,20 |
| Ş6 kazan dönüş | ✓ | F20 %6,2 | >= %0 | ✓ F20 %3,0 |
| Ş9 U dip | ✗ | a/ATR -0,002, x* -, R² 0,21, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,005, x* 0,60, R² 0,77, sol 2,77, sağ 1,27, argmin-x* -3,3 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,7, F22a %-2,5, F23 0,79 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,1, F22a %-8,2, F23 0,83 |
| Ş8 yol almamış | ✓ | F18 %9,5 | <= %20 | ✓ F18 %-1,8 |
| F14 büyük resim | ✗ | F14 %-41,5 | >= %0 | ✗ F14 %-34,9 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,5 | <= 4 | ✗ en büyük günlük getiri / ATR 4,3 |

Önceki adaylar (4; [t-250, t-1]): bar -134 AL 9/12; bar -49 ZAMAN AŞIMI 7/12; bar -20 Ş9 ÇANAK 8/12; bar -18 KIRILDI 9/12


### No 19 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -184)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-27,5 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,95, F17 %0,0 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 6 |
| Ş3 dip savunulmuş | ✓ | F2 %1,4 | >= -%1 | ✓ F2 %0,6 |
| Ş4 küçük mum | ✓ | F3 0,67 | <= 0,90 | ✓ F3 0,62 |
| Ş5 alt fitil kısa | ✓ | F4 0,17 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %2,5 | >= %0 | ✓ F20 %9,1 |
| Ş9 U dip | ✗ | a/ATR -0,000, x* -, R² 0,56, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,002, x* -, R² 0,84, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,2, F22a %-1,0, F23 0,55 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %3,1, F22a %-1,9, F23 0,86 |
| Ş8 yol almamış | ✓ | F18 %12,9 | <= %20 | ✓ F18 %10,5 |
| F14 büyük resim | ✓ | F14 %102,2 | >= %0 | ✓ F14 %1,6 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 2 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,3 | <= 4 | ✓ en büyük günlük getiri / ATR 2,9 |

Önceki adaylar (9; [t-250, t-1]): bar -234 ZAMAN AŞIMI 7/12; bar -196 AL 7/12; bar -184 AL 9/12; bar -175 AL 7/12; bar -151 AL 8/12; bar -101 AL 5/12; bar -73 ZAMAN AŞIMI 3/12; bar -50 ZAMAN AŞIMI 3/12; bar -16 KIRILDI 7/12


### No 20 (ABD)

**KARAR: SEÇİM TUTARLI (önceki aday yok)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik |
|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-27,8 | F15 <= 0,25 VE F17 <= -%20 |
| Ş2 hat net | ✓ | F1 4 | >= 3 |
| Ş3 dip savunulmuş | ✓ | F2 %1,2 | >= -%1 |
| Ş4 küçük mum | ✓ | F3 0,56 | <= 0,90 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 |
| Ş6 kazan dönüş | ✓ | F20 %4,7 | >= %0 |
| Ş9 U dip | ✗ | a/ATR -0,001, x* -, R² 0,74, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,5, F22a %-3,6, F23 0,72 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 |
| Ş8 yol almamış | ✓ | F18 %9,3 | <= %20 |
| F14 büyük resim | ✗ | F14 %-49,7 | >= %0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,8 | <= 4 |

Önceki adaylar (0; [t-250, t-1]): yok


### No 21 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 10/12, bar -221)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,18, F17 %-23,3 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-4,0 |
| Ş2 hat net | ✓ | F1 6 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %0,2 | >= -%1 | ✓ F2 %0,0 |
| Ş4 küçük mum | ✓ | F3 0,62 | <= 0,90 | ✓ F3 0,77 |
| Ş5 alt fitil kısa | ✓ | F4 0,22 | <= 0,25 | ✗ F4 0,29 |
| Ş6 kazan dönüş | ✓ | F20 %4,8 | >= %0 | ✓ F20 %5,4 |
| Ş9 U dip | ✗ | a/ATR 0,009, x* 0,81, R² 0,85, sol 8,55, sağ 0,46, argmin-x* -5,6 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,005, x* 0,40, R² 0,60, sol 1,22, sağ 2,64, argmin-x* -1,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,3, F22a %-0,6, F23 0,54 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,8, F22a %-0,3, F23 0,58 |
| Ş8 yol almamış | ✓ | F18 %8,8 | <= %20 | ✓ F18 %18,0 |
| F14 büyük resim | ✓ | F14 %1,4 | >= %0 | ✓ F14 %156,3 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,7 | <= 4 | ✓ en büyük günlük getiri / ATR 3,8 |

Önceki adaylar (9; [t-250, t-1]): bar -221 AL 10/12; bar -213 ZAMAN AŞIMI 6/12; bar -186 KIRILDI 7/12; bar -176 AL 8/12; bar -158 AL 6/12; bar -137 AL 7/12; bar -124 AL 5/12; bar -60 ZAMAN AŞIMI 7/12; bar -26 ZAMAN AŞIMI 7/12


### No 22 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 7/12, bar -187)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,14, F17 %-28,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,34, F17 %-11,7 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,6 | >= -%1 | ✓ F2 %-0,1 |
| Ş4 küçük mum | ✓ | F3 0,73 | <= 0,90 | ✓ F3 0,50 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✗ F4 0,28 |
| Ş6 kazan dönüş | ✓ | F20 %10,5 | >= %0 | ✓ F20 %2,9 |
| Ş9 U dip | ✓ | a/ATR 0,008, x* 0,66, R² 0,82, sol 5,26, sağ 1,40, argmin-x* 0,3 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,36, R² 0,60, sol 0,85, sağ 2,77, argmin-x* 1,1 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,0, F22a %-2,4, F23 0,89 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,3, F22a %-11,3, F23 0,51 |
| Ş8 yol almamış | ✓ | F18 %9,6 | <= %20 | ✓ F18 %-3,3 |
| F14 büyük resim | ✗ | F14 %-37,5 | >= %0 | ✓ F14 %181,7 |
| C8 kağıt hafızası | ✗ | F16 2 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,3 | <= 4 | ✗ en büyük günlük getiri / ATR 11,2 |

Önceki adaylar (7; [t-250, t-1]): bar -227 ZAMAN AŞIMI 5/12; bar -187 KIRILDI 7/12; bar -177 ZAMAN AŞIMI 5/12; bar -122 ZAMAN AŞIMI 5/12; bar -91 AL 6/12; bar -45 Ş9 ÇANAK 5/12; bar -38 KIRILDI 5/12


### No 23 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 6/12, bar -125)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,13, F17 %-45,1 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,02, F17 %-30,6 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,7 | >= -%1 | ✗ F2 %-1,0 |
| Ş4 küçük mum | ✓ | F3 0,80 | <= 0,90 | ✓ F3 0,79 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 | ✓ F4 0,20 |
| Ş6 kazan dönüş | ✓ | F20 %2,6 | >= %0 | ✗ F20 %-1,6 |
| Ş9 U dip | ✗ | a/ATR -0,001, x* -, R² 0,66, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,46, R² 0,26, sol 1,17, sağ 1,55, argmin-x* -10,1 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,7, F22a %-4,9, F23 0,69 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,5, F22a %-10,3, F23 0,67 |
| Ş8 yol almamış | ✓ | F18 %14,6 | <= %20 | ✓ F18 %-4,4 |
| F14 büyük resim | ✗ | F14 %-52,4 | >= %0 | ✗ F14 %-46,2 |
| C8 kağıt hafızası | ✗ | F16 3 | = 0 | ✗ F16 4 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,9 | <= 4 | ✓ en büyük günlük getiri / ATR 2,6 |

Önceki adaylar (4; [t-250, t-1]): bar -212 KIRILDI 6/12; bar -186 KIRILDI 6/12; bar -125 KIRILDI 6/12; bar -95 Ş9 ÇANAK 5/12


### No 24 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -237)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,14, F17 %-32,5 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,44, F17 %-1,8 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✗ F1 0 |
| Ş3 dip savunulmuş | ✓ | F2 %1,2 | >= -%1 | ✗ F2 - |
| Ş4 küçük mum | ✓ | F3 0,86 | <= 0,90 | ✓ F3 0,76 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✓ F4 0,19 |
| Ş6 kazan dönüş | ✓ | F20 %2,8 | >= %0 | ✓ F20 %1,5 |
| Ş9 U dip | ✗ | a/ATR 0,003, x* 0,98, R² 0,70, sol 4,86, sağ 0,00, argmin-x* -10,2 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,002, x* -, R² 0,56, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,7, F22a %-0,2, F23 0,63 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-8,8, F22a %-8,1, F23 0,36 |
| Ş8 yol almamış | ✓ | F18 %13,8 | <= %20 | ✓ F18 %2,1 |
| F14 büyük resim | ✗ | F14 %-35,5 | >= %0 | ✓ F14 %31,7 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,3 | <= 4 | ✓ en büyük günlük getiri / ATR 2,3 |

Önceki adaylar (9; [t-250, t-1]): bar -248 AL 7/12; bar -237 ZAMAN AŞIMI 7/12; bar -168 KIRILDI 6/12; bar -146 ZAMAN AŞIMI 6/12; bar -136 ZAMAN AŞIMI 6/12; bar -75 Ş9 ÇANAK 6/12; bar -70 Ş9 ÇANAK 6/12; bar -65 ZAMAN AŞIMI 6/12; bar -30 Ş9 ÇANAK 5/12


### No 25 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -133)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,17, F17 %-44,3 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,00, F17 %-37,0 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,3 | >= -%1 | ✓ F2 %0,4 |
| Ş4 küçük mum | ✓ | F3 0,73 | <= 0,90 | ✓ F3 0,46 |
| Ş5 alt fitil kısa | ✓ | F4 0,22 | <= 0,25 | ✗ F4 0,28 |
| Ş6 kazan dönüş | ✓ | F20 %0,3 | >= %0 | ✓ F20 %0,4 |
| Ş9 U dip | ✗ | a/ATR 0,000, x* 1,84, R² 0,34, sol 1,39, sağ 0,00, argmin-x* -55,8 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,71, R² 0,85, sol 2,91, sağ 0,47, argmin-x* -2,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,7, F22a %-1,8, F23 0,80 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-12,7, F22a %-10,8, F23 0,28 |
| Ş8 yol almamış | ✓ | F18 %17,7 | <= %20 | ✓ F18 %-1,9 |
| F14 büyük resim | ✗ | F14 %-71,4 | >= %0 | ✓ F14 %8,4 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,5 | <= 4 | ✗ en büyük günlük getiri / ATR 4,3 |

Önceki adaylar (6; [t-250, t-1]): bar -201 ZAMAN AŞIMI 7/12; bar -188 AL 8/12; bar -133 KIRILDI 8/12; bar -104 ZAMAN AŞIMI 6/12; bar -70 Ş9 ÇANAK 7/12; bar -27 ZAMAN AŞIMI 6/12


### No 26 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -157)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-29,4 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,11, F17 %-22,5 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,8 | >= -%1 | ✓ F2 %0,2 |
| Ş4 küçük mum | ✓ | F3 0,87 | <= 0,90 | ✓ F3 0,87 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✓ F4 0,13 |
| Ş6 kazan dönüş | ✓ | F20 %5,9 | >= %0 | ✗ F20 %-0,2 |
| Ş9 U dip | ✗ | a/ATR 0,000, x* 29,04, R² 0,39, sol 3,05, sağ 0,00, argmin-x* -1103,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,005, x* -, R² 0,58, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,6, F22a %-1,5, F23 0,87 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-11,3, F22a %-11,1, F23 0,07 |
| Ş8 yol almamış | ✓ | F18 %12,3 | <= %20 | ✓ F18 %1,4 |
| F14 büyük resim | ✗ | F14 %-47,0 | >= %0 | ✓ F14 %24,6 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✗ F16 1 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,1 | <= 4 | ✓ en büyük günlük getiri / ATR 3,6 |

Önceki adaylar (6; [t-250, t-1]): bar -239 AL 6/12; bar -179 AL 6/12; bar -166 ZAMAN AŞIMI 6/12; bar -157 ZAMAN AŞIMI 8/12; bar -132 ZAMAN AŞIMI 5/12; bar -100 Ş9 ÇANAK 5/12


### No 27 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 11/12 >= en iyi önceki aday 8/12, bar -138)**

Seçilen bölge (bar 0, AL): puan 11/12; her kurala uyuyor mu: HAYIR (eksik: F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,19, F17 %-29,7 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,12, F17 %-20,6 |
| Ş2 hat net | ✓ | F1 5 | >= 3 | ✗ F1 1 |
| Ş3 dip savunulmuş | ✓ | F2 %0,0 | >= -%1 | ✓ F2 %0,0 |
| Ş4 küçük mum | ✓ | F3 0,86 | <= 0,90 | ✓ F3 0,83 |
| Ş5 alt fitil kısa | ✓ | F4 0,17 | <= 0,25 | ✓ F4 0,09 |
| Ş6 kazan dönüş | ✓ | F20 %3,1 | >= %0 | ✓ F20 %5,9 |
| Ş9 U dip | ✓ | a/ATR 0,007, x* 0,66, R² 0,83, sol 4,74, sağ 1,27, argmin-x* 3,3 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,005, x* 0,65, R² 0,65, sol 3,45, sağ 1,00, argmin-x* 0,7 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,5, F22a %-4,8, F23 0,73 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-7,6, F22a %-7,6, F23 0,02 |
| Ş8 yol almamış | ✓ | F18 %13,6 | <= %20 | ✓ F18 %3,8 |
| F14 büyük resim | ✗ | F14 %-38,0 | >= %0 | ✗ F14 %-23,1 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✗ F16 3 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,6 | <= 4 | ✓ en büyük günlük getiri / ATR 3,0 |

Önceki adaylar (7; [t-250, t-1]): bar -230 AL 8/12; bar -211 AL 5/12; bar -181 AL 7/12; bar -138 ZAMAN AŞIMI 8/12; bar -105 Ş9 ÇANAK 5/12; bar -100 Ş9 ÇANAK 5/12; bar -63 ZAMAN AŞIMI 5/12


### No 28 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 8/12 >= en iyi önceki aday 8/12, bar -90)**

Seçilen bölge (bar 0, AL): puan 8/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,24, F17 %-39,6 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,08, F17 %-38,1 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✗ F1 1 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,6 | >= -%1 | ✓ F2 %0,0 |
| Ş4 küçük mum | ✓ | F3 0,58 | <= 0,90 | ✓ F3 0,89 |
| Ş5 alt fitil kısa | ✓ | F4 0,21 | <= 0,25 | ✓ F4 0,20 |
| Ş6 kazan dönüş | ✓ | F20 %0,7 | >= %0 | ✓ F20 %9,0 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 0,48, R² 0,11, sol 0,51, sağ 0,61, argmin-x* -8,6 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,004, x* 0,41, R² 0,46, sol 1,07, sağ 2,14, argmin-x* -0,2 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %4,1, F22a %-8,1, F23 0,85 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-24,4, F22a %-16,2, F23 0,62 |
| Ş8 yol almamış | ✓ | F18 %15,1 | <= %20 | ✓ F18 %14,4 |
| F14 büyük resim | ✗ | F14 %-68,8 | >= %0 | ✗ F14 %-23,3 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,2 | <= 4 | ✗ en büyük günlük getiri / ATR 4,0 |

Önceki adaylar (7; [t-250, t-1]): bar -130 ZAMAN AŞIMI 8/12; bar -100 Ş9 ÇANAK 7/12; bar -95 Ş9 ÇANAK 7/12; bar -90 Ş9 ÇANAK 8/12; bar -42 KIRILDI 7/12; bar -20 ZAMAN AŞIMI 5/12; bar -10 Ş9 ÇANAK 6/12


### No 29 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -244)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-26,9 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,84, F17 %2,8 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,5 | >= -%1 | ✓ F2 %1,3 |
| Ş4 küçük mum | ✓ | F3 0,89 | <= 0,90 | ✓ F3 0,59 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %2,6 | >= %0 | ✓ F20 %0,9 |
| Ş9 U dip | ✗ | a/ATR 0,013, x* 0,69, R² 0,84, sol 9,75, sağ 1,88, argmin-x* 6,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,007, x* 0,53, R² 0,72, sol 2,76, sağ 2,22, argmin-x* -10,6 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,1, F22a %-4,4, F23 0,75 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %5,9, F22a %3,1, F23 0,48 |
| Ş8 yol almamış | ✓ | F18 %12,4 | <= %20 | ✓ F18 %17,5 |
| F14 büyük resim | ✗ | F14 %-33,9 | >= %0 | ✓ F14 %22,2 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,8 | <= 4 | ✓ en büyük günlük getiri / ATR 3,1 |

Önceki adaylar (4; [t-250, t-1]): bar -244 AL 9/12; bar -220 AL 7/12; bar -197 ZAMAN AŞIMI 8/12; bar -37 ZAMAN AŞIMI 7/12


### No 30 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -232)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,23, F17 %-33,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-4,2 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,1 | >= -%1 | ✓ F2 %0,9 |
| Ş4 küçük mum | ✓ | F3 0,82 | <= 0,90 | ✓ F3 0,70 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 | ✗ F4 0,28 |
| Ş6 kazan dönüş | ✓ | F20 %3,7 | >= %0 | ✓ F20 %2,0 |
| Ş9 U dip | ✗ | a/ATR 0,013, x* 0,75, R² 0,78, sol 11,36, sağ 1,29, argmin-x* -8,2 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,000, x* -6,11, R² 0,77, sol 0,00, sağ 7,20, argmin-x* 244,4 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,3, F22a %-0,2, F23 0,70 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %1,6, F22a %0,5, F23 0,35 |
| Ş8 yol almamış | ✓ | F18 %15,1 | <= %20 | ✓ F18 %9,4 |
| F14 büyük resim | ✗ | F14 %-54,7 | >= %0 | ✓ F14 %46,3 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,5 | <= 4 | ✓ en büyük günlük getiri / ATR 2,0 |

Önceki adaylar (4; [t-250, t-1]): bar -232 AL 8/12; bar -100 Ş9 ÇANAK 7/12; bar -95 Ş9 ÇANAK 7/12; bar -67 AL 7/12


### No 31 (ABD)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -115)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,24, F17 %-42,5 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,25, F17 %-24,3 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✗ F1 2 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,8 | >= -%1 | ✓ F2 %-0,9 |
| Ş4 küçük mum | ✓ | F3 0,82 | <= 0,90 | ✗ F3 1,28 |
| Ş5 alt fitil kısa | ✓ | F4 0,09 | <= 0,25 | ✓ F4 0,17 |
| Ş6 kazan dönüş | ✓ | F20 %4,2 | >= %0 | ✓ F20 %6,0 |
| Ş9 U dip | ✗ | a/ATR 0,009, x* 0,66, R² 0,88, sol 6,21, sağ 1,59, argmin-x* -5,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,009, x* 0,62, R² 0,77, sol 5,24, sağ 1,94, argmin-x* 4,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %5,4, F22a %-1,0, F23 0,81 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-1,9, F22a %-3,9, F23 0,70 |
| Ş8 yol almamış | ✓ | F18 %18,0 | <= %20 | ✗ F18 %22,8 |
| F14 büyük resim | ✗ | F14 %-53,0 | >= %0 | ✓ F14 %4,3 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,6 | <= 4 | ✓ en büyük günlük getiri / ATR 2,1 |

Önceki adaylar (5; [t-250, t-1]): bar -115 Ş9 ÇANAK 8/12; bar -75 Ş9 ÇANAK 6/12; bar -70 Ş9 ÇANAK 5/12; bar -65 Ş9 ÇANAK 6/12; bar -57 ZAMAN AŞIMI 6/12


### No 32 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 12/12 >= en iyi önceki aday 10/12, bar -79)**

Seçilen bölge (bar 0, AL): puan 12/12; her kurala uyuyor mu: EVET

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,19, F17 %-32,3 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,85, F17 %-12,8 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %1,0 | >= -%1 | ✓ F2 %1,1 |
| Ş4 küçük mum | ✓ | F3 0,76 | <= 0,90 | ✓ F3 0,64 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,18 |
| Ş6 kazan dönüş | ✓ | F20 %1,4 | >= %0 | ✓ F20 %3,4 |
| Ş9 U dip | ✓ | a/ATR 0,007, x* 0,73, R² 0,85, sol 5,41, sağ 0,70, argmin-x* -0,7 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,003, x* 0,63, R² 0,46, sol 1,64, sağ 0,58, argmin-x* -13,4 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %4,1, F22a %-2,9, F23 0,67 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %2,0, F22a %-1,6, F23 1,00 |
| Ş8 yol almamış | ✓ | F18 %12,4 | <= %20 | ✓ F18 %10,2 |
| F14 büyük resim | ✓ | F14 %67,5 | >= %0 | ✓ F14 %203,4 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,8 | <= 4 | ✓ en büyük günlük getiri / ATR 3,7 |

Önceki adaylar (3; [t-250, t-1]): bar -155 AL 9/12; bar -79 AL 10/12; bar -51 ZAMAN AŞIMI 5/12


### No 33 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -103)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-39,4 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-0,4 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✗ F1 2 |
| Ş3 dip savunulmuş | ✓ | F2 %0,1 | >= -%1 | ✓ F2 %1,0 |
| Ş4 küçük mum | ✓ | F3 0,90 | <= 0,90 | ✓ F3 0,63 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,23 |
| Ş6 kazan dönüş | ✓ | F20 %4,3 | >= %0 | ✗ F20 %-2,8 |
| Ş9 U dip | ✗ | a/ATR -0,003, x* -, R² 0,78, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,001, x* -, R² 0,34, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,2, F22a %-3,1, F23 0,87 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %2,2, F22a %-0,0, F23 0,36 |
| Ş8 yol almamış | ✓ | F18 %11,5 | <= %20 | ✓ F18 %10,9 |
| F14 büyük resim | ✗ | F14 %-20,3 | >= %0 | ✓ F14 %145,7 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 6,6 | <= 4 | ✓ en büyük günlük getiri / ATR 2,9 |

Önceki adaylar (1; [t-250, t-1]): bar -103 AL 7/12


### No 34 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 8/12 >= en iyi önceki aday 8/12, bar -30)**

Seçilen bölge (bar 0, AL): puan 8/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,12, F17 %-20,1 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,18, F17 %-23,0 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 7 |
| Ş3 dip savunulmuş | ✓ | F2 %0,1 | >= -%1 | ✓ F2 %-0,7 |
| Ş4 küçük mum | ✓ | F3 0,90 | <= 0,90 | ✗ F3 1,04 |
| Ş5 alt fitil kısa | ✓ | F4 0,18 | <= 0,25 | ✓ F4 0,09 |
| Ş6 kazan dönüş | ✓ | F20 %0,1 | >= %0 | ✓ F20 %3,6 |
| Ş9 U dip | ✗ | a/ATR 0,002, x* 1,86, R² 0,84, sol 7,07, sağ 0,00, argmin-x* -46,7 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,009, x* 0,46, R² 0,53, sol 3,04, sağ 4,08, argmin-x* -0,1 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,6, F22a %-2,9, F23 0,90 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,3, F22a %-12,6, F23 0,26 |
| Ş8 yol almamış | ✓ | F18 %6,7 | <= %20 | ✓ F18 %10,1 |
| F14 büyük resim | ✗ | F14 %-6,1 | >= %0 | ✓ F14 %14,8 |
| C8 kağıt hafızası | ✗ | F16 2 | = 0 | ✗ F16 2 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 6,5 | <= 4 | ✗ en büyük günlük getiri / ATR 7,7 |

Önceki adaylar (5; [t-250, t-1]): bar -206 AL 5/12; bar -135 AL 7/12; bar -105 KIRILDI 8/12; bar -75 KIRILDI 8/12; bar -30 Ş9 ÇANAK 8/12


### No 35 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -93)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-26,4 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,90, F17 %-7,2 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 7 |
| Ş3 dip savunulmuş | ✓ | F2 %0,2 | >= -%1 | ✓ F2 %0,5 |
| Ş4 küçük mum | ✓ | F3 0,86 | <= 0,90 | ✓ F3 0,76 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✓ F4 0,16 |
| Ş6 kazan dönüş | ✓ | F20 %0,5 | >= %0 | ✗ F20 %-0,3 |
| Ş9 U dip | ✗ | a/ATR 0,003, x* 0,94, R² 0,63, sol 4,12, sağ 0,01, argmin-x* -12,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,009, x* -, R² 0,63, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,5, F22a %-2,2, F23 0,74 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %3,6, F22a %-2,7, F23 0,81 |
| Ş8 yol almamış | ✓ | F18 %9,8 | <= %20 | ✓ F18 %8,9 |
| F14 büyük resim | ✗ | F14 %-3,2 | >= %0 | ✗ F14 %-30,1 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 4,0 | <= 4 | ✗ en büyük günlük getiri / ATR 7,9 |

Önceki adaylar (8; [t-250, t-1]): bar -220 AL 5/12; bar -194 AL 7/12; bar -175 ZAMAN AŞIMI 4/12; bar -148 ZAMAN AŞIMI 5/12; bar -120 Ş9 ÇANAK 4/12; bar -115 Ş9 ÇANAK 4/12; bar -93 AL 7/12; bar -72 ZAMAN AŞIMI 2/12


### No 36 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -45)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,12, F17 %-26,3 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,39, F17 %-6,5 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,8 | >= -%1 | ✓ F2 %0,6 |
| Ş4 küçük mum | ✓ | F3 0,87 | <= 0,90 | ✓ F3 0,81 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 | ✗ F4 0,28 |
| Ş6 kazan dönüş | ✓ | F20 %2,8 | >= %0 | ✓ F20 %3,9 |
| Ş9 U dip | ✗ | a/ATR 0,005, x* 1,37, R² 0,82, sol 11,93, sağ 0,00, argmin-x* -28,2 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,011, x* 0,51, R² 0,83, sol 4,31, sağ 3,94, argmin-x* -0,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,0, F22a %-1,3, F23 0,65 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-2,5, F22a %-2,6, F23 0,05 |
| Ş8 yol almamış | ✓ | F18 %6,2 | <= %20 | ✓ F18 %11,3 |
| F14 büyük resim | ✗ | F14 %-8,1 | >= %0 | ✗ F14 %-10,7 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,3 | <= 4 | ✓ en büyük günlük getiri / ATR 2,4 |

Önceki adaylar (9; [t-250, t-1]): bar -227 ZAMAN AŞIMI 7/12; bar -182 ZAMAN AŞIMI 7/12; bar -135 AL 7/12; bar -114 ZAMAN AŞIMI 6/12; bar -95 Ş9 ÇANAK 8/12; bar -90 Ş9 ÇANAK 8/12; bar -50 Ş9 ÇANAK 8/12; bar -45 Ş9 ÇANAK 8/12; bar -40 ZAMAN AŞIMI 7/12


### No 37 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -171)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: F14 büyük resim, C8 kağıt hafızası, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,21, F17 %-33,2 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,00, F17 %-1,3 |
| Ş2 hat net | ✓ | F1 6 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,2 | >= -%1 | ✓ F2 %0,3 |
| Ş4 küçük mum | ✓ | F3 0,86 | <= 0,90 | ✓ F3 0,73 |
| Ş5 alt fitil kısa | ✓ | F4 0,24 | <= 0,25 | ✗ F4 0,26 |
| Ş6 kazan dönüş | ✓ | F20 %6,8 | >= %0 | ✓ F20 %0,3 |
| Ş9 U dip | ✓ | a/ATR 0,007, x* 0,48, R² 0,66, sol 2,39, sağ 2,70, argmin-x* -2,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,001, x* -, R² 0,46, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %3,0, F22a %-0,4, F23 0,90 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-11,2, F22a %-10,8, F23 0,12 |
| Ş8 yol almamış | ✓ | F18 %14,6 | <= %20 | ✓ F18 %-5,3 |
| F14 büyük resim | ✗ | F14 %-34,2 | >= %0 | ✓ F14 %16,0 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 9,7 | <= 4 | ✓ en büyük günlük getiri / ATR 4,0 |

Önceki adaylar (8; [t-250, t-1]): bar -171 KIRILDI 8/12; bar -133 AL 6/12; bar -109 AL 3/12; bar -105 Ş9 ÇANAK 6/12; bar -65 Ş9 ÇANAK 7/12; bar -47 ZAMAN AŞIMI 7/12; bar -10 Ş9 ÇANAK 5/12; bar -5 Ş9 ÇANAK 6/12


### No 38 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 9/12, bar -187)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,25, F17 %-23,2 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 1,00, F17 %-3,5 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 5 |
| Ş3 dip savunulmuş | ✓ | F2 %0,5 | >= -%1 | ✓ F2 %0,2 |
| Ş4 küçük mum | ✓ | F3 0,83 | <= 0,90 | ✓ F3 0,89 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✓ F4 0,25 |
| Ş6 kazan dönüş | ✓ | F20 %0,5 | >= %0 | ✗ F20 %-1,9 |
| Ş9 U dip | ✗ | a/ATR 0,002, x* 1,23, R² 0,87, sol 4,41, sağ 0,00, argmin-x* -17,1 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,27, R² 0,34, sol 0,38, sağ 2,89, argmin-x* 6,7 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,3, F22a %-4,1, F23 0,67 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,5, F22a %-4,2, F23 1,00 |
| Ş8 yol almamış | ✓ | F18 %12,4 | <= %20 | ✓ F18 %7,6 |
| F14 büyük resim | ✗ | F14 %-17,2 | >= %0 | ✓ F14 %17,2 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,3 | <= 4 | ✓ en büyük günlük getiri / ATR 3,0 |

Önceki adaylar (3; [t-250, t-1]): bar -187 AL 9/12; bar -177 ZAMAN AŞIMI 6/12; bar -116 ZAMAN AŞIMI 7/12


### No 39 (AVR)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -32)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,23, F17 %-24,4 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,00, F17 %-23,0 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,2 | >= -%1 | ✓ F2 %-0,2 |
| Ş4 küçük mum | ✓ | F3 0,65 | <= 0,90 | ✓ F3 0,62 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✗ F4 0,34 |
| Ş6 kazan dönüş | ✓ | F20 %1,4 | >= %0 | ✓ F20 %1,1 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 0,71, R² 0,33, sol 0,93, sağ 0,15, argmin-x* -3,8 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,004, x* 0,90, R² 0,82, sol 4,43, sağ 0,05, argmin-x* -9,3 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,7, F22a %-6,5, F23 0,83 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-11,5, F22a %-7,0, F23 0,77 |
| Ş8 yol almamış | ✓ | F18 %11,9 | <= %20 | ✓ F18 %-2,3 |
| F14 büyük resim | ✗ | F14 %-29,4 | >= %0 | ✗ F14 %-24,4 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,4 | <= 4 | ✓ en büyük günlük getiri / ATR 3,2 |

Önceki adaylar (4; [t-250, t-1]): bar -242 AL 7/12; bar -82 AL 6/12; bar -63 ZAMAN AŞIMI 6/12; bar -32 KIRILDI 8/12


### No 40 (AVR)

**KARAR: ÖNCEKİ BÖLGE DAHA UYGUN: bar -90 (Ş9 ÇANAK), puan 10/12 vs seçilen 9/12; seçilenin tutmadığı kurallar: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası; önceki adayın tutmadığı: Ş1 dipte, C8 kağıt hafızası**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,20, F17 %-30,2 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,95, F17 %-5,1 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,4 | >= -%1 | ✓ F2 %-0,5 |
| Ş4 küçük mum | ✓ | F3 0,87 | <= 0,90 | ✓ F3 0,55 |
| Ş5 alt fitil kısa | ✓ | F4 0,22 | <= 0,25 | ✓ F4 0,21 |
| Ş6 kazan dönüş | ✓ | F20 %0,9 | >= %0 | ✓ F20 %5,7 |
| Ş9 U dip | ✗ | a/ATR 0,011, x* 0,64, R² 0,80, sol 6,68, sağ 2,10, argmin-x* -10,0 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,004, x* 0,62, R² 0,48, sol 2,20, sağ 0,84, argmin-x* 2,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,9, F22a %-1,3, F23 0,71 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,6, F22a %-1,5, F23 0,72 |
| Ş8 yol almamış | ✓ | F18 %11,3 | <= %20 | ✓ F18 %13,7 |
| F14 büyük resim | ✗ | F14 %-10,1 | >= %0 | ✓ F14 %34,7 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✗ F16 2 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,8 | <= 4 | ✓ en büyük günlük getiri / ATR 2,3 |

Önceki adaylar (7; [t-250, t-1]): bar -216 ZAMAN AŞIMI 4/12; bar -203 ZAMAN AŞIMI 4/12; bar -160 AL 7/12; bar -116 KIRILDI 7/12; bar -90 Ş9 ÇANAK 10/12; bar -85 Ş9 ÇANAK 9/12; bar -80 Ş9 ÇANAK 9/12


### No 41 (BIST)

**KARAR: SEÇİM TUTARLI (önceki aday yok)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik |
|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,19, F17 %-25,7 | F15 <= 0,25 VE F17 <= -%20 |
| Ş2 hat net | ✓ | F1 3 | >= 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,0 | >= -%1 |
| Ş4 küçük mum | ✓ | F3 0,64 | <= 0,90 |
| Ş5 alt fitil kısa | ✓ | F4 0,19 | <= 0,25 |
| Ş6 kazan dönüş | ✓ | F20 %4,3 | >= %0 |
| Ş9 U dip | ✗ | a/ATR 0,007, x* 0,65, R² 0,77, sol 4,67, sağ 1,32, argmin-x* -13,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %4,7, F22a %-6,2, F23 0,68 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 |
| Ş8 yol almamış | ✓ | F18 %19,5 | <= %20 |
| F14 büyük resim | ✗ | F14 %-30,3 | >= %0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 3,2 | <= 4 |

Önceki adaylar (0; [t-250, t-1]): yok


### No 42 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -30)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,08, F17 %-29,4 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,17, F17 %-48,0 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✗ F1 1 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,9 | >= -%1 | ✓ F2 %0,0 |
| Ş4 küçük mum | ✓ | F3 0,52 | <= 0,90 | ✓ F3 0,90 |
| Ş5 alt fitil kısa | ✓ | F4 0,23 | <= 0,25 | ✓ F4 0,19 |
| Ş6 kazan dönüş | ✓ | F20 %3,8 | >= %0 | ✓ F20 %10,2 |
| Ş9 U dip | ✗ | a/ATR 0,006, x* 0,79, R² 0,92, sol 5,42, sağ 0,38, argmin-x* -0,8 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,008, x* 0,43, R² 0,59, sol 2,24, sağ 3,85, argmin-x* -3,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,7, F22a %-3,3, F23 0,60 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-27,9, F22a %-25,3, F23 0,83 |
| Ş8 yol almamış | ✓ | F18 %11,9 | <= %20 | ✗ F18 %31,7 |
| F14 büyük resim | ✗ | F14 %-65,8 | >= %0 | ✗ F14 %-40,3 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,6 | <= 4 | ✓ en büyük günlük getiri / ATR 2,6 |

Önceki adaylar (4; [t-250, t-1]): bar -81 ZAMAN AŞIMI 8/12; bar -40 Ş9 ÇANAK 6/12; bar -35 Ş9 ÇANAK 6/12; bar -30 Ş9 ÇANAK 8/12


### No 43 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -185)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,15, F17 %-33,1 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,11, F17 %-55,5 |
| Ş2 hat net | ✓ | F1 18 | >= 3 | ✓ F1 8 |
| Ş3 dip savunulmuş | ✓ | F2 %0,4 | >= -%1 | ✓ F2 %-0,9 |
| Ş4 küçük mum | ✓ | F3 0,38 | <= 0,90 | ✓ F3 0,64 |
| Ş5 alt fitil kısa | ✓ | F4 0,20 | <= 0,25 | ✓ F4 0,24 |
| Ş6 kazan dönüş | ✓ | F20 %1,2 | >= %0 | ✗ F20 %-1,0 |
| Ş9 U dip | ✗ | a/ATR 0,001, x* 0,49, R² 0,33, sol 0,46, sağ 0,50, argmin-x* 1,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,027, x* 0,64, R² 0,78, sol 16,50, sağ 5,41, argmin-x* -8,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %2,5, F22a %-0,5, F23 0,63 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %0,6, F22a %-1,3, F23 0,65 |
| Ş8 yol almamış | ✓ | F18 %8,4 | <= %20 | ✓ F18 %11,3 |
| F14 büyük resim | ✗ | F14 %-7,0 | >= %0 | ✗ F14 %-28,0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 5,0 | <= 4 | ✗ en büyük günlük getiri / ATR 4,6 |

Önceki adaylar (3; [t-250, t-1]): bar -185 AL 8/12; bar -128 ZAMAN AŞIMI 6/12; bar -49 ZAMAN AŞIMI 5/12


### No 44 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 10/12, bar -59)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,19, F17 %-26,4 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,00, F17 %-25,6 |
| Ş2 hat net | ✓ | F1 3 | >= 3 | ✓ F1 11 |
| Ş3 dip savunulmuş | ✓ | F2 %0,9 | >= -%1 | ✓ F2 %-0,5 |
| Ş4 küçük mum | ✓ | F3 0,56 | <= 0,90 | ✓ F3 0,48 |
| Ş5 alt fitil kısa | ✓ | F4 0,16 | <= 0,25 | ✓ F4 0,09 |
| Ş6 kazan dönüş | ✓ | F20 %1,3 | >= %0 | ✓ F20 %0,5 |
| Ş9 U dip | ✗ | a/ATR 0,002, x* 0,66, R² 0,53, sol 1,49, sağ 0,38, argmin-x* -9,9 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,002, x* 1,13, R² 0,57, sol 3,82, sağ 0,00, argmin-x* -23,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,7, F22a %-1,4, F23 0,88 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-14,9, F22a %-8,1, F23 0,99 |
| Ş8 yol almamış | ✓ | F18 %12,2 | <= %20 | ✓ F18 %-6,0 |
| F14 büyük resim | ✓ | F14 %0,6 | >= %0 | ✓ F14 %70,1 |
| C8 kağıt hafızası | ✗ | F16 2 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,2 | <= 4 | ✓ en büyük günlük getiri / ATR 2,0 |

Önceki adaylar (6; [t-250, t-1]): bar -242 AL 10/12; bar -146 AL 10/12; bar -125 ZAMAN AŞIMI 8/12; bar -103 ZAMAN AŞIMI 8/12; bar -59 KIRILDI 10/12; bar -25 KIRILDI 9/12


### No 45 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 8/12, bar -104)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-32,2 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,05, F17 %-19,6 |
| Ş2 hat net | ✓ | F1 6 | >= 3 | ✓ F1 7 |
| Ş3 dip savunulmuş | ✓ | F2 %1,1 | >= -%1 | ✓ F2 %0,3 |
| Ş4 küçük mum | ✓ | F3 0,46 | <= 0,90 | ✓ F3 0,60 |
| Ş5 alt fitil kısa | ✓ | F4 0,15 | <= 0,25 | ✓ F4 0,14 |
| Ş6 kazan dönüş | ✓ | F20 %2,3 | >= %0 | ✓ F20 %17,8 |
| Ş9 U dip | ✗ | a/ATR 0,000, x* 0,52, R² 0,05, sol 0,20, sağ 0,17, argmin-x* 6,6 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,001, x* 0,67, R² 0,16, sol 0,83, sağ 0,20, argmin-x* 0,8 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,3, F22a %-5,6, F23 0,74 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,5, F22a %-9,4, F23 0,90 |
| Ş8 yol almamış | ✓ | F18 %14,6 | <= %20 | ✓ F18 %3,4 |
| F14 büyük resim | ✗ | F14 %-13,0 | >= %0 | ✓ F14 %2914,6 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 8,3 | <= 4 | ✗ en büyük günlük getiri / ATR 7,4 |

Önceki adaylar (3; [t-250, t-1]): bar -243 ZAMAN AŞIMI 8/12; bar -104 ZAMAN AŞIMI 8/12; bar -62 ZAMAN AŞIMI 6/12


### No 46 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 10/12, bar -69)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-36,5 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,45, F17 %-2,2 |
| Ş2 hat net | ✓ | F1 7 | >= 3 | ✓ F1 6 |
| Ş3 dip savunulmuş | ✓ | F2 %0,6 | >= -%1 | ✓ F2 %-0,5 |
| Ş4 küçük mum | ✓ | F3 0,46 | <= 0,90 | ✓ F3 0,64 |
| Ş5 alt fitil kısa | ✓ | F4 0,25 | <= 0,25 | ✓ F4 0,22 |
| Ş6 kazan dönüş | ✓ | F20 %0,0 | >= %0 | ✓ F20 %0,5 |
| Ş9 U dip | ✗ | a/ATR -0,000, x* -, R² 0,30, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,000, x* -3,63, R² 0,81, sol 0,00, sağ 4,52, argmin-x* 150,6 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,7, F22a %-1,1, F23 0,71 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %2,9, F22a %-1,2, F23 0,83 |
| Ş8 yol almamış | ✓ | F18 %13,4 | <= %20 | ✓ F18 %15,7 |
| F14 büyük resim | ✗ | F14 %-20,6 | >= %0 | ✓ F14 %7,0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 1,9 | <= 4 | ✓ en büyük günlük getiri / ATR 1,8 |

Önceki adaylar (4; [t-250, t-1]): bar -234 ZAMAN AŞIMI 8/12; bar -94 AL 8/12; bar -69 AL 10/12; bar -15 Ş9 ÇANAK 7/12


### No 47 (BIST)

**KARAR: ÖNCEKİ BÖLGE DAHA UYGUN: bar -20 (Ş9 ÇANAK), puan 11/12 vs seçilen 10/12; seçilenin tutmadığı kurallar: Ş9 U dip, F14 büyük resim; önceki adayın tutmadığı: Ş7 yakın tavan gövdeli kırılım**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,11, F17 %-27,5 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,04, F17 %-41,1 |
| Ş2 hat net | ✓ | F1 4 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %-0,4 | >= -%1 | ✓ F2 %0,8 |
| Ş4 küçük mum | ✓ | F3 0,46 | <= 0,90 | ✓ F3 0,62 |
| Ş5 alt fitil kısa | ✓ | F4 0,22 | <= 0,25 | ✓ F4 0,16 |
| Ş6 kazan dönüş | ✓ | F20 %3,5 | >= %0 | ✓ F20 %10,5 |
| Ş9 U dip | ✗ | a/ATR -0,004, x* -, R² 0,28, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,009, x* 0,48, R² 0,67, sol 2,98, sağ 3,59, argmin-x* -1,6 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %1,4, F22a %-4,1, F23 0,65 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-18,3, F22a %-9,7, F23 0,81 |
| Ş8 yol almamış | ✓ | F18 %11,0 | <= %20 | ✓ F18 %8,6 |
| F14 büyük resim | ✗ | F14 %-22,0 | >= %0 | ✓ F14 %7,0 |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 1,7 | <= 4 | ✓ en büyük günlük getiri / ATR 1,7 |

Önceki adaylar (4; [t-250, t-1]): bar -65 ZAMAN AŞIMI 10/12; bar -30 Ş9 ÇANAK 10/12; bar -25 Ş9 ÇANAK 11/12; bar -20 Ş9 ÇANAK 11/12


### No 48 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 7/12, bar -250)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,24, F17 %-23,8 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,38, F17 %1,0 |
| Ş2 hat net | ✓ | F1 5 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,4 | >= -%1 | ✓ F2 %-0,1 |
| Ş4 küçük mum | ✓ | F3 0,80 | <= 0,90 | ✓ F3 0,69 |
| Ş5 alt fitil kısa | ✓ | F4 0,13 | <= 0,25 | ✗ F4 0,40 |
| Ş6 kazan dönüş | ✓ | F20 %3,4 | >= %0 | ✗ F20 %-2,4 |
| Ş9 U dip | ✗ | a/ATR 0,005, x* 1,22, R² 0,74, sol 9,92, sağ 0,00, argmin-x* -25,5 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR -0,001, x* -, R² 0,30, sol -, sağ -, argmin-x* - |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %0,6, F22a %-0,6, F23 0,75 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-13,9, F22a %-15,4, F23 0,57 |
| Ş8 yol almamış | ✓ | F18 %8,8 | <= %20 | ✓ F18 %-7,2 |
| F14 büyük resim | ✗ | F14 %-14,1 | >= %0 | ✓ F14 %65,7 |
| C8 kağıt hafızası | ✗ | F16 1 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,3 | <= 4 | ✓ en büyük günlük getiri / ATR 2,8 |

Önceki adaylar (8; [t-250, t-1]): bar -250 KIRILDI 7/12; bar -200 ZAMAN AŞIMI 6/12; bar -110 Ş9 ÇANAK 6/12; bar -86 ZAMAN AŞIMI 5/12; bar -80 Ş9 ÇANAK 5/12; bar -75 Ş9 ÇANAK 5/12; bar -70 Ş9 ÇANAK 6/12; bar -24 ZAMAN AŞIMI 6/12


### No 49 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 9/12 >= en iyi önceki aday 9/12, bar -153)**

Seçilen bölge (bar 0, AL): puan 9/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, F14 büyük resim, C8 kağıt hafızası)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,22, F17 %-31,9 | F15 <= 0,25 VE F17 <= -%20 | ✓ F15 0,21, F17 %-27,5 |
| Ş2 hat net | ✓ | F1 10 | >= 3 | ✓ F1 4 |
| Ş3 dip savunulmuş | ✓ | F2 %0,3 | >= -%1 | ✓ F2 %0,1 |
| Ş4 küçük mum | ✓ | F3 0,59 | <= 0,90 | ✓ F3 0,62 |
| Ş5 alt fitil kısa | ✓ | F4 0,21 | <= 0,25 | ✗ F4 0,34 |
| Ş6 kazan dönüş | ✓ | F20 %0,6 | >= %0 | ✗ F20 %-0,8 |
| Ş9 U dip | ✗ | a/ATR 0,002, x* 0,76, R² 0,50, sol 1,95, sağ 0,19, argmin-x* -19,7 | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✗ a/ATR 0,002, x* 0,63, R² 0,39, sol 1,07, sağ 0,37, argmin-x* -11,5 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %3,6, F22a %-1,7, F23 0,88 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✓ F22 %1,4, F22a %-5,6, F23 1,00 |
| Ş8 yol almamış | ✓ | F18 %12,3 | <= %20 | ✓ F18 %17,0 |
| F14 büyük resim | ✗ | F14 %-25,2 | >= %0 | ✓ F14 %39,3 |
| C8 kağıt hafızası | ✗ | F16 2 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✓ | en büyük günlük getiri / ATR 2,0 | <= 4 | ✓ en büyük günlük getiri / ATR 2,8 |

Önceki adaylar (6; [t-250, t-1]): bar -167 ZAMAN AŞIMI 9/12; bar -153 AL 9/12; bar -90 AL 8/12; bar -80 Ş9 ÇANAK 7/12; bar -54 KIRILDI 8/12; bar -31 KIRILDI 7/12


### No 50 (BIST)

**KARAR: SEÇİM TUTARLI (seçilen 10/12 >= en iyi önceki aday 8/12, bar -40)**

Seçilen bölge (bar 0, AL): puan 10/12; her kurala uyuyor mu: HAYIR (eksik: Ş9 U dip, C13 dev mum yok)

| Kural | seçilen | değer | eşik | en iyi önceki aday |
|---|---|---|---|---|
| Ş1 dipte | ✓ | F15 0,17, F17 %-52,6 | F15 <= 0,25 VE F17 <= -%20 | ✗ F15 0,00, F17 %-18,6 |
| Ş2 hat net | ✓ | F1 13 | >= 3 | ✓ F1 3 |
| Ş3 dip savunulmuş | ✓ | F2 %0,0 | >= -%1 | ✓ F2 %0,8 |
| Ş4 küçük mum | ✓ | F3 0,40 | <= 0,90 | ✓ F3 0,74 |
| Ş5 alt fitil kısa | ✓ | F4 0,22 | <= 0,25 | ✓ F4 0,10 |
| Ş6 kazan dönüş | ✓ | F20 %1,8 | >= %0 | ✓ F20 %1,8 |
| Ş9 U dip | ✗ | a/ATR -0,001, x* -, R² 0,69, sol -, sağ -, argmin-x* - | a > 0; x* 0,20..0,75; R² >= 0,40; sol >= 1; sağ >= 0,5; mutlak(argmin-x*) <= 5 | ✓ a/ATR 0,018, x* 0,71, R² 0,88, sol 13,67, sağ 2,19, argmin-x* -1,9 |
| Ş7 yakın tavan gövdeli kırılım | ✓ | F22 %3,5, F22a %-1,8, F23 0,68 | F22 > 0 VE F22a < 0 VE F23 >= 0,50 | ✗ F22 %-25,7, F22a %-24,9, F23 0,14 |
| Ş8 yol almamış | ✓ | F18 %13,6 | <= %20 | ✓ F18 %-2,3 |
| F14 büyük resim | ✓ | F14 %24,9 | >= %0 | ✗ F14 - |
| C8 kağıt hafızası | ✓ | F16 0 | = 0 | ✓ F16 0 |
| C13 dev mum yok | ✗ | en büyük günlük getiri / ATR 5,5 | <= 4 | ✗ en büyük günlük getiri / ATR - |

Önceki adaylar (2; [t-250, t-1]): bar -100 Ş9 ÇANAK 6/12; bar -40 Ş9 ÇANAK 8/12


