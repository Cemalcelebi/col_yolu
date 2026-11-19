# YAPI_HEDEF — RAPOR 5 (5. tur: Ş9 'U DİP + PARABOLİK DEVAM' Y11 / Y11b + Y11c bilgi; konum eşli KAT; TUR 4 kuru sayım T1.5)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo. Koşu: 2026-11-19 04:21:07 UTC (Y11, Y11b, Y11c). Ön kayıt 5: 2026-11-19 04:20:51 UTC (git 146e2785b7).

## 1. SONUÇ (etiket önceden yazılı kuralla; EN FAZLA EMARE: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ)

| Deneme | ETİKET (5. tur = 3. tur kuralı) | kural etiketi | İKİ YÖNLÜ (TERS) | dış sınama ABD / AVR 2016-22 | karar hücreleri: durum (n, KAT5, konum eşli KAT5 [n], plasebo KAT5) — ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26 |
|---|---|---|---|---|---|
| Y11 U DİP ÇEKİRDEK | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ | TERS YOK (TERS karar hücresi 0) | ÖLÇÜLEMEDİ / ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (n 3, KAT5 1,06, konum 0,94 [3], plasebo 0,50) · ÖLÇÜLEMEDİ (n 15, KAT5 1,37, konum 1,29 [14], plasebo 2,25) · ÖLÇÜLEMEDİ (n 1, KAT5 0,00, konum 0,00 [1], plasebo -) · ÖLÇÜLEMEDİ (n 2, KAT5 1,59, konum 1,43 [2], plasebo -) |
| Y11b S7 v2 (Ş6 yerine Ş9) | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ | TERS YOK (TERS karar hücresi 0) | ÖLÇÜLEMEDİ / ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (n 0, KAT5 -, konum - [0], plasebo -) · ÖLÇÜLEMEDİ (n 3, KAT5 1,85, konum 1,09 [2], plasebo 1,00) · ÖLÇÜLEMEDİ (n 1, KAT5 0,00, konum 0,00 [1], plasebo 0,00) · ÖLÇÜLEMEDİ (n 1, KAT5 2,77, konum 2,75 [1], plasebo -) |
| Y11c Ş9 TEK BAŞINA (bilgi, konumsuz) (BİLGİ, karar değil) | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ | TERS YOK (TERS karar hücresi 0) | ÖLÇÜLEMEDİ / ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ (n 143, KAT5 0,94, konum 0,96 [143], plasebo 1,00) · ÖLÇÜLEMEDİ (n 211, KAT5 1,07, konum 1,11 [208], plasebo 0,99) · ÖLÇÜLEMEDİ (n 52, KAT5 0,84, konum 0,88 [50], plasebo 0,87) · ÖLÇÜLEMEDİ (n 109, KAT5 1,06, konum 1,05 [106], plasebo 1,13) |

Etiket kuralı (3. tur, AYNEN): Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar.
TERS: hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1.

DÜRÜSTLÜK: ABD / AVR 2023 ve 2024-26 hücreleri BAKILMIŞ (Y11 / Y11b Y9'un alt kümesi; Y9 hücreleri 3. turda görüldü). Dış sınama (2016-22 ABD / AVR) ve BIST hücreleri kısmen bakılmış (Y9 alt kümesi): Y9'un 2016-22 ve BIST hücreleri 3. tur raporunda görüldü. Asıl karar Mart 2027 ileri testidir (kriz sonrası veri, aynı eşik).

## 2. TASARIM KONTROLÜ (ön kayıttan ÖNCE, sonuç okunmadan; tasarim5.json)

Kayıt 1 (2026-11-19 03:57:29 UTC; eşik F25 [0.2, 0.75], F26 >= 0.4, F27 >= 1.0, F28 >= 0.5, |F29| <= 5.0): (a) No 38 Ş9'u GEÇMEDİ (istenen); (b) TUR 2 kazan sayfaları 2 / 4 geçti (en az 3 istenir) -> TUTMADI.

| Olay | F24 a/ATR | F25 x*/39 | F26 R² | F27 sol derinlik | F28 sağ kalkış | F29 argmin - x* | alt şartlar a·b·c·d·e·f | Ş9 |
|---|---|---|---|---|---|---|---|---|
| S7 PDF No 38 (AVR 2016-22, AVR 7.) | 0,002 | 1,234 | 0,874 | 4,415 | 0,000 | -17,107 | ✓·✓✓·· | tutmaz |
| TUR 2 sayfa 1 | -0,003 | - | 0,372 | - | - | - | ······ | tutmaz |
| TUR 2 sayfa 3 | -0,005 | - | 0,803 | - | - | - | ··✓··· | tutmaz |
| TUR 2 sayfa 11 | 0,005 | 0,585 | 0,487 | 2,637 | 1,329 | -2,809 | ✓✓✓✓✓✓ | TUTAR |
| TUR 2 sayfa 22 | 0,005 | 0,530 | 0,541 | 2,132 | 1,680 | -3,660 | ✓✓✓✓✓✓ | TUTAR |

AYAR KULLANILMADI — gerekçe: (b) 2 / 4: TUR 2 sayfa 1 ve 3'te son 40 barın Low uyumunda a < 0 (F24 -0,003 / -0,005: şemsiye, x* tanımsız). İzinli tek ayar yalnız F26_min (0,30..0,50) ve F25_alt (0,15..0,25); ikisi de F24 > 0 şartını değiştiremez, bu iki sayfa hiçbir izinli ayarda geçemez (en iyi 2 / 4). Ayar KULLANILMADI; iş tanımı §2 eşikleri kilitlendi. (a) No 38 geçmedi (F25 1,23 > 0,75; F28 0,00 < 0,5; |F29| 17,1 > 5). Tanı (bilgi, eşiği değiştirmez): sayfa 1 ve 3'te 60-80 barlık pencerede a > 0 (U 40 bardan uzun).

Özet: No 38 Ş9'u GEÇMEDİ; TUR 2 kazan sayfaları 2 / 4 geçti; ayar YAPILMADI.

## 3. HUNİ (getirisiz)

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y1 olayı (özellik satırı) | 14881 | 8686 / 2042 / 4153 | 7054 | 4496 / 815 / 1743 | 4728 | 2588 / 381 / 1759 |
| + Ş1 DİPTE | 724 | 346 / 146 / 232 | 164 | 89 / 20 / 55 | 616 | 238 / 81 / 297 |
| + Ş2 HAT NET | 439 | 206 / 93 / 140 | 102 | 51 / 15 / 36 | 365 | 145 / 42 / 178 |
| + Ş9 U DİP = Y11 | 38 | 20 / 3 / 15 | 9 | 6 / 1 / 2 | 22 | 10 / 0 / 12 |
| (ayrı) Y10 = Ş1-Ş8 | 69 | 31 / 13 / 25 | 21 | 9 / 6 / 6 | 116 | 40 / 14 / 62 |
| (ayrı) Y10, Ş6 çıkar (Ş1-Ş5, Ş7, Ş8) | 86 | 38 / 18 / 30 | 25 | 11 / 7 / 7 | 136 | 46 / 15 / 75 |
| (ayrı) + Ş9 = Y11b | 7 | 4 / 0 / 3 | 4 | 2 / 1 / 1 | 13 | 4 / 0 / 9 |
| (ayrı) Y1 + Ş9 = Y11c (bilgi) | 823 | 464 / 143 / 216 | 392 | 231 / 52 / 109 | 297 | 141 / 14 / 142 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: Ş9 tutmayan 14058, F24 <= 0 / NaN 7451, F25 [0,20, 0,75] dışı / NaN 10997, F26 < 0,40 / NaN 3983, F27 < 1 / NaN 10636, F28 < 0,5 / NaN 9799, |F29| > 5 / NaN 12397, F24 NaN 0, F25 NaN 7451, F26 NaN 0, F27 NaN 7451, F28 NaN 7451, F29 NaN 7451; AVR: Ş9 tutmayan 6662, F24 <= 0 / NaN 3602, F25 [0,20, 0,75] dışı / NaN 5208, F26 < 0,40 / NaN 1896, F27 < 1 / NaN 5316, F28 < 0,5 / NaN 4524, |F29| > 5 / NaN 5855, F24 NaN 0, F25 NaN 3602, F26 NaN 0, F27 NaN 3602, F28 NaN 3602, F29 NaN 3602; BIST: Ş9 tutmayan 4431, F24 <= 0 / NaN 2093, F25 [0,20, 0,75] dışı / NaN 3378, F26 < 0,40 / NaN 1272, F27 < 1 / NaN 2946, F28 < 0,5 / NaN 3233, |F29| > 5 / NaN 3867, F24 NaN 0, F25 NaN 2093, F26 NaN 0, F27 NaN 2093, F28 NaN 2093, F29 NaN 2093.

Ölçülen n (OC tekil -> E5a giriş denetimi 'stop_uzak' -> 15 bar ve eş >= 3; karar n'i): Y11: ABD 2016-22 20, ABD 2023 3, ABD 2024-26 15, AVR 2016-22 6, AVR 2023 1, AVR 2024-26 2, BIST 2016-22 10, BIST 2023 0, BIST 2024-26 12; Y11b: ABD 2016-22 4, ABD 2023 0, ABD 2024-26 3, AVR 2016-22 2, AVR 2023 1, AVR 2024-26 1, BIST 2016-22 4, BIST 2023 0, BIST 2024-26 9; Y11c: ABD 2016-22 464, ABD 2023 143, ABD 2024-26 211, AVR 2016-22 231, AVR 2023 52, AVR 2024-26 109, BIST 2016-22 141, BIST 2023 14, BIST 2024-26 141.

Y1 eşleşmesi: ABD: Y1 olay 14881 = özellik satırı 14881 (eşleşen 14881); AVR: Y1 olay 7054 = özellik satırı 7054 (eşleşen 7054); BIST: Y1 olay 4728 = özellik satırı 4728 (eşleşen 4728).

## 4. OLAY SAYIMI ve DENETİMLER

| Deneme | Pazar | girdi | düşen (giriş / havuz / tekil) | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma (5 olay, F1-F29) | F15 çeyrek uyumu | Y1 regresyonu (satır) |
|---|---|---|---|---|---|---|---|---|---|---|
| Y11 | ABD | 38 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 38 |
| Y11 | AVR | 9 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 9 |
| Y11 | BIST | 22 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 22 |
| Y11b | ABD | 7 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 7 |
| Y11b | AVR | 4 | 0 | 0 | 0 | 0 | 0 | 4 TUTTU | %100.0 | EŞİT 4 |
| Y11b | BIST | 13 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 13 |
| Y11c | ABD | 823 | 0 | 0 | 5 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 823 |
| Y11c | AVR | 392 | 0 | 0 | 0 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 392 |
| Y11c | BIST | 297 | 0 | 0 | 1 | 0 | 0 | 5 TUTTU | %100.0 | EŞİT 297 |

## 5. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95)

| Deneme | Hücre | İŞARET | n | P(+5) olay / eş | KAT5 [%95] | P(stop önce) olay / eş | plasebo KAT5 [%95] | şartlar n·kat·stop·plasebo | güç | DURUM | TERS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Y11 | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 20 | %60,0 / %46,7 | 1,28 [0,97, 1,66] | %35,0 / %29,4 | 1,33 [0,78, 2,60] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | ABD 2023 (karar) | BAKILMIŞ | 3 | %33,3 / %31,5 | 1,06 [0,00, 4,00] | %33,3 / %43,7 | 0,50 [0,00, 1,00] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | ABD 2024-26 (karar) | BAKILMIŞ | 15 | %60,0 / %43,9 | 1,37 [0,70, 2,23] | %26,7 / %35,2 | 2,25 [0,86, 10,00] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 6 | %33,3 / %48,7 | 0,68 [0,00, 1,84] | %33,3 / %5,5 | 1,00 [0,00, 4,00] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | AVR 2023 (karar) | BAKILMIŞ | 1 | %0,0 / %25,0 | 0,00 [0,00, 0,00] | %100,0 / %29,2 | - [-, -] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | AVR 2024-26 (karar) | BAKILMIŞ | 2 | %50,0 / %31,4 | 1,59 [0,00, 2,77] | %0,0 / %16,4 | - [-, -] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 10 | %30,0 / %50,4 | 0,60 [0,18, 1,05] | %20,0 / %20,5 | 0,43 [0,12, 0,75] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11 | BIST 2023 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 0 | - | - | - | - | - | - | ÖLÇÜLEMEDİ | - |
| Y11 | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 12 | %75,0 / %73,8 | 1,02 [0,61, 1,44] | %0,0 / %10,2 | 1,50 [0,56, 3,75] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 4 | %100,0 / %61,6 | 1,62 [1,16, 3,18] | %0,0 / %21,3 | 4,00 [1,33, 4,00] | ·✓✓✓ | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | ABD 2023 (karar) | BAKILMIŞ | 0 | - | - | - | - | - | - | ÖLÇÜLEMEDİ | - |
| Y11b | ABD 2024-26 (karar) | BAKILMIŞ | 3 | %66,7 / %36,1 | 1,85 [0,00, 5,71] | %33,3 / %40,6 | 1,00 [1,00, 1,00] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 2 | %100,0 / %40,7 | 2,46 [2,18, 2,82] | %0,0 / %5,8 | - [-, -] | ·✓✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | AVR 2023 (karar) | BAKILMIŞ | 1 | %0,0 / %25,0 | 0,00 [0,00, 0,00] | %100,0 / %29,2 | 0,00 [0,00, 0,00] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | AVR 2024-26 (karar) | BAKILMIŞ | 1 | %100,0 / %36,1 | 2,77 [2,77, 2,77] | %0,0 / %19,4 | - [-, -] | ·✓✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 4 | %50,0 / %54,0 | 0,93 [0,00, 1,64] | %50,0 / %26,5 | 1,00 [0,00, 3,00] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2023 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 0 | - | - | - | - | - | - | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 9 | %66,7 / %69,3 | 0,96 [0,57, 1,48] | %0,0 / %12,1 | 1,20 [0,71, 2,50] | ··✓· | %0 | ÖLÇÜLEMEDİ | - |
| Y11c | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 464 | %38,1 / %35,3 | 1,08 [0,94, 1,26] | %26,3 / %25,4 | 0,89 [0,76, 1,05] | ✓··· | %57 | ÖLÇÜLEMEDİ | - |
| Y11c | ABD 2023 (karar) | BAKILMIŞ | 143 | %35,0 / %37,1 | 0,94 [0,74, 1,13] | %25,9 / %26,6 | 1,00 [0,62, 1,70] | ✓·✓· | %11 | ÖLÇÜLEMEDİ | - |
| Y11c | ABD 2024-26 (karar) | BAKILMIŞ | 211 | %43,6 / %40,8 | 1,07 [0,94, 1,27] | %30,3 / %31,8 | 0,99 [0,78, 1,22] | ✓·✓· | %11 | ÖLÇÜLEMEDİ | - |
| Y11c | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 231 | %35,5 / %32,3 | 1,10 [0,90, 1,30] | %14,3 / %18,1 | 1,12 [0,80, 1,52] | ✓·✓· | %11 | ÖLÇÜLEMEDİ | - |
| Y11c | AVR 2023 (karar) | BAKILMIŞ | 52 | %25,0 / %29,9 | 0,84 [0,54, 1,28] | %26,9 / %19,5 | 0,87 [0,56, 1,23] | ✓··· | %2 | ÖLÇÜLEMEDİ | - |
| Y11c | AVR 2024-26 (karar) | BAKILMIŞ | 109 | %31,2 / %29,5 | 1,06 [0,85, 1,33] | %21,1 / %21,5 | 1,13 [0,77, 1,89] | ✓·✓· | %11 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | %46,1 / %48,8 | 0,95 [0,74, 1,12] | %27,0 / %25,8 | 1,10 [0,80, 1,43] | ✓··· | %11 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2023 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 14 | %28,6 / %38,2 | 0,75 [0,00, 1,11] | %71,4 / %60,3 | 0,50 [0,00, 1,00] | ···· | %0 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | %74,5 / %66,8 | 1,11 [0,99, 1,31] | %16,3 / %21,3 | 1,40 [1,00, 1,72] | ✓·✓· | %11 | ÖLÇÜLEMEDİ | - |

## 6. KONUM EŞLİ KAT (zorunlu; eş = aynı gün, aynı kova VE F15 aynı çeyrek)

| Deneme | Hücre | İŞARET | n (1. tur eş) | KAT5 (1. tur eş) | n (konum eş) | P(+5) olay / konum eş | KAT5 konum [%95] | P(stop önce) olay / konum eş | olay F15 ort | eş F15 ort / medyan | eşlerin olay çeyreğinde payı |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Y11 | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 20 | 1,28 | 20 | %60,0 / %50,3 | 1,19 [0,87, 1,55] | %35,0 / %30,8 | 0,19 | 0,28 / 0,26 | %51,3 |
| Y11 | ABD 2023 | BAKILMIŞ | 3 | 1,06 | 3 | %33,3 / %35,5 | 0,94 [0,00, 2,86] | %33,3 / %41,0 | 0,22 | 0,18 / 0,14 | %69,1 |
| Y11 | ABD 2024-26 | BAKILMIŞ | 15 | 1,37 | 14 | %57,1 / %44,2 | 1,29 [0,61, 2,04] | %28,6 / %35,0 | 0,19 | 0,23 / 0,18 | %63,0 |
| Y11 | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 6 | 0,68 | 5 | %40,0 / %51,9 | 0,77 [0,00, 2,37] | %40,0 / %5,2 | 0,20 | 0,32 / 0,29 | %46,3 |
| Y11 | AVR 2023 | BAKILMIŞ | 1 | 0,00 | 1 | %0,0 / %27,3 | 0,00 [0,00, 0,00] | %100,0 / %36,4 | 0,20 | 0,22 / 0,25 | %45,8 |
| Y11 | AVR 2024-26 | BAKILMIŞ | 2 | 1,59 | 2 | %50,0 / %34,8 | 1,43 [0,00, 2,75] | %0,0 / %22,7 | 0,17 | 0,45 / 0,42 | %25,3 |
| Y11 | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 10 | 0,60 | 9 | %33,3 / %46,0 | 0,72 [0,20, 1,34] | %22,2 / %22,9 | 0,18 | 0,32 / 0,25 | %50,4 |
| Y11 | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 12 | 1,02 | 12 | %75,0 / %79,9 | 0,94 [0,58, 1,22] | %0,0 / %6,4 | 0,18 | 0,27 / 0,26 | %49,8 |
| Y11b | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 4 | 1,62 | 4 | %100,0 / %64,5 | 1,55 [1,17, 2,39] | %0,0 / %20,1 | 0,16 | 0,24 / 0,14 | %64,6 |
| Y11b | ABD 2024-26 | BAKILMIŞ | 3 | 1,85 | 2 | %50,0 / %45,9 | 1,09 [0,00, 1,68] | %50,0 / %34,7 | 0,20 | 0,32 / 0,19 | %49,5 |
| Y11b | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 2 | 2,46 | 2 | %100,0 / %35,8 | 2,79 [1,60, 11,00] | %0,0 / %4,5 | 0,20 | 0,38 / 0,38 | %34,4 |
| Y11b | AVR 2023 | BAKILMIŞ | 1 | 0,00 | 1 | %0,0 / %27,3 | 0,00 [0,00, 0,00] | %100,0 / %36,4 | 0,20 | 0,22 / 0,25 | %45,8 |
| Y11b | AVR 2024-26 | BAKILMIŞ | 1 | 2,77 | 1 | %100,0 / %36,4 | 2,75 [2,75, 2,75] | %0,0 / %45,5 | 0,23 | 0,43 / 0,38 | %30,6 |
| Y11b | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 4 | 0,93 | 4 | %50,0 / %52,1 | 0,96 [0,00, 1,88] | %50,0 / %27,9 | 0,17 | 0,37 / 0,26 | %44,5 |
| Y11b | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 9 | 0,96 | 9 | %66,7 / %76,0 | 0,88 [0,53, 1,22] | %0,0 / %7,7 | 0,17 | 0,26 / 0,25 | %52,2 |
| Y11c | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 464 | 1,08 | 452 | %38,1 / %35,0 | 1,09 [0,95, 1,24] | %26,5 / %25,3 | 0,65 | 0,59 / 0,65 | %45,5 |
| Y11c | ABD 2023 | BAKILMIŞ | 143 | 0,94 | 143 | %35,0 / %36,5 | 0,96 [0,75, 1,13] | %25,9 / %27,0 | 0,64 | 0,58 / 0,60 | %43,0 |
| Y11c | ABD 2024-26 | BAKILMIŞ | 211 | 1,07 | 208 | %43,8 / %39,5 | 1,11 [0,98, 1,31] | %30,3 / %32,1 | 0,61 | 0,55 / 0,61 | %44,3 |
| Y11c | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 231 | 1,10 | 216 | %35,6 / %31,7 | 1,12 [0,91, 1,33] | %13,9 / %17,1 | 0,64 | 0,57 / 0,57 | %47,1 |
| Y11c | AVR 2023 | BAKILMIŞ | 52 | 0,84 | 50 | %24,0 / %27,2 | 0,88 [0,54, 1,30] | %28,0 / %20,8 | 0,66 | 0,64 / 0,68 | %49,1 |
| Y11c | AVR 2024-26 | BAKILMIŞ | 109 | 1,06 | 106 | %31,1 / %29,6 | 1,05 [0,83, 1,37] | %21,7 / %21,5 | 0,63 | 0,57 / 0,60 | %43,2 |
| Y11c | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | 0,95 | 123 | %44,7 / %49,9 | 0,90 [0,68, 1,10] | %28,5 / %25,2 | 0,55 | 0,50 / 0,50 | %41,8 |
| Y11c | BIST 2023 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 14 | 0,75 | 13 | %23,1 / %36,2 | 0,64 [0,00, 1,00] | %76,9 / %62,4 | 0,62 | 0,61 / 0,66 | %49,7 |
| Y11c | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | 1,11 | 133 | %74,4 / %67,0 | 1,11 [0,97, 1,35] | %15,8 / %21,9 | 0,42 | 0,40 / 0,35 | %41,1 |

## 7. OLASILIK TABLOSU (olay / eş / taban; KAT = olay / eş [%95])

| Deneme | Hücre | İŞARET | n | P(+5 önce) olay / eş / taban | KAT | P(+10 önce) olay / eş / taban | KAT | P(stop önce) olay / eş / taban | KAT |
|---|---|---|---|---|---|---|---|---|---|
| Y11 | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 20 | %60,0 / %46,7 / %43,1 | 1,28 [0,97, 1,66] | %40,0 / %23,6 / %16,7 | 1,69 [0,94, 2,84] | %35,0 / %29,4 / %22,2 | 1,19 [0,65, 1,71] |
| Y11 | ABD 2023 | BAKILMIŞ | 3 | %33,3 / %31,5 / %22,5 | 1,06 [0,00, 4,00] | %33,3 / %14,1 / %9,4 | 2,36 [0,00, 8,89] | %33,3 / %43,7 / %39,3 | 0,76 [0,00, 2,00] |
| Y11 | ABD 2024-26 | BAKILMIŞ | 15 | %60,0 / %43,9 / %43,9 | 1,37 [0,70, 2,23] | %26,7 / %20,7 / %19,2 | 1,29 [0,00, 2,27] | %26,7 / %35,2 / %32,5 | 0,76 [0,00, 1,42] |
| Y11 | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 6 | %33,3 / %48,7 / %43,0 | 0,68 [0,00, 1,84] | %0,0 / %18,6 / %18,0 | 0,00 [0,00, 0,00] | %33,3 / %5,5 / %10,4 | 6,04 [0,00, 12,74] |
| Y11 | AVR 2023 | BAKILMIŞ | 1 | %0,0 / %25,0 / %17,9 | 0,00 [0,00, 0,00] | %0,0 / %8,3 / %6,1 | 0,00 [0,00, 0,00] | %100,0 / %29,2 / %24,3 | 3,43 [3,43, 3,43] |
| Y11 | AVR 2024-26 | BAKILMIŞ | 2 | %50,0 / %31,4 / %24,4 | 1,59 [0,00, 2,77] | %50,0 / %11,7 / %6,5 | 4,29 [0,00, 6,00] | %0,0 / %16,4 / %18,1 | 0,00 [0,00, 0,00] |
| Y11 | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 10 | %30,0 / %50,4 / %55,6 | 0,60 [0,18, 1,05] | %20,0 / %29,2 / %32,1 | 0,69 [0,00, 1,62] | %20,0 / %20,5 / %22,7 | 0,97 [0,00, 1,56] |
| Y11 | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 12 | %75,0 / %73,8 / %69,7 | 1,02 [0,61, 1,44] | %41,7 / %46,7 / %45,0 | 0,89 [0,00, 1,52] | %0,0 / %10,2 / %14,4 | 0,00 [0,00, 0,00] |
| Y11b | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 4 | %100,0 / %61,6 / %50,7 | 1,62 [1,16, 3,18] | %50,0 / %41,1 / %22,5 | 1,22 [0,00, 4,50] | %0,0 / %21,3 / %18,5 | 0,00 [0,00, 0,00] |
| Y11b | ABD 2024-26 | BAKILMIŞ | 3 | %66,7 / %36,1 / %41,3 | 1,85 [0,00, 5,71] | %33,3 / %22,5 / %19,3 | 1,48 [0,00, 2,10] | %33,3 / %40,6 / %33,8 | 0,82 [0,00, 2,47] |
| Y11b | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 2 | %100,0 / %40,7 / %27,0 | 2,46 [2,18, 2,82] | %0,0 / %5,3 / %6,2 | 0,00 [0,00, 0,00] | %0,0 / %5,8 / %11,5 | 0,00 [0,00, 0,00] |
| Y11b | AVR 2023 | BAKILMIŞ | 1 | %0,0 / %25,0 / %17,9 | 0,00 [0,00, 0,00] | %0,0 / %8,3 / %6,1 | 0,00 [0,00, 0,00] | %100,0 / %29,2 / %24,3 | 3,43 [3,43, 3,43] |
| Y11b | AVR 2024-26 | BAKILMIŞ | 1 | %100,0 / %36,1 / %18,4 | 2,77 [2,77, 2,77] | %100,0 / %16,7 / %3,9 | 6,00 [6,00, 6,00] | %0,0 / %19,4 / %20,8 | 0,00 [0,00, 0,00] |
| Y11b | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 4 | %50,0 / %54,0 / %55,7 | 0,93 [0,00, 1,64] | %50,0 / %36,5 / %34,3 | 1,37 [0,00, 3,54] | %50,0 / %26,5 / %29,9 | 1,88 [0,00, 4,39] |
| Y11b | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 9 | %66,7 / %69,3 / %63,0 | 0,96 [0,57, 1,48] | %33,3 / %39,9 / %38,0 | 0,84 [0,00, 1,68] | %0,0 / %12,1 / %17,4 | 0,00 [0,00, 0,00] |
| Y11c | ABD 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 464 | %38,1 / %35,3 / %35,7 | 1,08 [0,94, 1,26] | %15,5 / %12,9 / %13,3 | 1,21 [0,97, 1,47] | %26,3 / %25,4 / %26,4 | 1,03 [0,87, 1,24] |
| Y11c | ABD 2023 | BAKILMIŞ | 143 | %35,0 / %37,1 / %40,0 | 0,94 [0,74, 1,13] | %14,7 / %15,3 / %17,6 | 0,96 [0,67, 1,19] | %25,9 / %26,6 / %28,7 | 0,97 [0,74, 1,25] |
| Y11c | ABD 2024-26 | BAKILMIŞ | 211 | %43,6 / %40,8 / %41,6 | 1,07 [0,94, 1,27] | %21,8 / %17,4 / %18,3 | 1,25 [0,95, 1,55] | %30,3 / %31,8 / %32,8 | 0,95 [0,75, 1,11] |
| Y11c | AVR 2016-22 | DIŞ SINAMA, kısmen bakılmış (Y9 alt kümesi) | 231 | %35,5 / %32,3 / %32,0 | 1,10 [0,90, 1,30] | %13,9 / %9,7 / %9,1 | 1,43 [1,06, 1,92] | %14,3 / %18,1 / %18,6 | 0,79 [0,57, 1,06] |
| Y11c | AVR 2023 | BAKILMIŞ | 52 | %25,0 / %29,9 / %27,0 | 0,84 [0,54, 1,28] | %7,7 / %8,7 / %8,5 | 0,89 [0,00, 1,60] | %26,9 / %19,5 / %21,9 | 1,38 [0,72, 1,87] |
| Y11c | AVR 2024-26 | BAKILMIŞ | 109 | %31,2 / %29,5 / %31,1 | 1,06 [0,85, 1,33] | %7,3 / %8,2 / %9,3 | 0,89 [0,41, 1,63] | %21,1 / %21,5 / %20,6 | 0,98 [0,65, 1,28] |
| Y11c | BIST 2016-22 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | %46,1 / %48,8 / %52,5 | 0,95 [0,74, 1,12] | %25,5 / %26,7 / %30,2 | 0,95 [0,64, 1,23] | %27,0 / %25,8 / %26,1 | 1,05 [0,82, 1,28] |
| Y11c | BIST 2023 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 14 | %28,6 / %38,2 / %37,1 | 0,75 [0,00, 1,11] | %14,3 / %22,3 / %21,9 | 0,64 [0,00, 1,44] | %71,4 / %60,3 / %60,6 | 1,18 [0,97, 1,80] |
| Y11c | BIST 2024-26 | BIST bilgi, kısmen bakılmış (Y9 alt kümesi) | 141 | %74,5 / %66,8 / %65,8 | 1,11 [0,99, 1,31] | %46,8 / %42,4 / %42,5 | 1,11 [0,92, 1,34] | %16,3 / %21,3 / %23,4 | 0,77 [0,50, 1,00] |

## 8. DIŞ SINAMA (2016-22 ABD / AVR; kısmen bakılmış (Y9 alt kümesi))

| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop) olay / eş | plasebo KAT5 alt | konum KAT5 [%95] | yarı 1 / yarı 2 | DURUM | TERS |
|---|---|---|---|---|---|---|---|---|---|---|
| Y11 | ABD 2016-22 | 20 | %60,0 / %46,7 | 1,28 [0,97, 1,66] | %35,0 / %29,4 | 0,78 | 1,19 [0,87, 1,55] | 1,37 / 1,20 | ÖLÇÜLEMEDİ | - |
| Y11 | AVR 2016-22 | 6 | %33,3 / %48,7 | 0,68 [0,00, 1,84] | %33,3 / %5,5 | 0,00 | 0,77 [0,00, 2,37] | 1,84 / 0,00 | ÖLÇÜLEMEDİ | - |
| Y11b | ABD 2016-22 | 4 | %100,0 / %61,6 | 1,62 [1,16, 3,18] | %0,0 / %21,3 | 1,33 | 1,55 [1,17, 2,39] | 2,45 / 1,21 | ÖLÇÜLEMEDİ | - |
| Y11b | AVR 2016-22 | 2 | %100,0 / %40,7 | 2,46 [2,18, 2,82] | %0,0 / %5,8 | - | 2,79 [1,60, 11,00] | 2,18 / 2,82 | ÖLÇÜLEMEDİ | - |
| Y11c | ABD 2016-22 | 464 | %38,1 / %35,3 | 1,08 [0,94, 1,26] | %26,3 / %25,4 | 0,76 | 1,09 [0,95, 1,24] | 1,09 / 1,07 | ÖLÇÜLEMEDİ | - |
| Y11c | AVR 2016-22 | 231 | %35,5 / %32,3 | 1,10 [0,90, 1,30] | %14,3 / %18,1 | 0,80 | 1,12 [0,91, 1,33] | 0,97 / 1,20 | ÖLÇÜLEMEDİ | - |

Dış sınama kararı: Y11: TUTAR hayır, TERS hayır; Y11b: TUTAR hayır, TERS hayır; Y11c: TUTAR hayır, TERS hayır.

## 9. BIST (bilgi; ayrı başlık; karar değil; kısmen bakılmış (Y9 alt kümesi))

| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop) olay / eş | plasebo KAT5 alt | konum KAT5 [%95] | yarı 1 / yarı 2 | DURUM | TERS |
|---|---|---|---|---|---|---|---|---|---|---|
| Y11 | BIST 2016-22 | 10 | %30,0 / %50,4 | 0,60 [0,18, 1,05] | %20,0 / %20,5 | 0,12 | 0,72 [0,20, 1,34] | 0,38 / 0,82 | ÖLÇÜLEMEDİ | - |
| Y11 | BIST 2023 | 0 | - / - | - [-, -] | - / - | - | - [-, -] | - / - | ÖLÇÜLEMEDİ | - |
| Y11 | BIST 2024-26 | 12 | %75,0 / %73,8 | 1,02 [0,61, 1,44] | %0,0 / %10,2 | 0,56 | 0,94 [0,58, 1,22] | 1,08 / 0,94 | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2016-22 | 4 | %50,0 / %54,0 | 0,93 [0,00, 1,64] | %50,0 / %26,5 | 0,00 | 0,96 [0,00, 1,88] | 1,31 / 0,71 | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2023 | 0 | - / - | - [-, -] | - / - | - | - [-, -] | - / - | ÖLÇÜLEMEDİ | - |
| Y11b | BIST 2024-26 | 9 | %66,7 / %69,3 | 0,96 [0,57, 1,48] | %0,0 / %12,1 | 0,71 | 0,88 [0,53, 1,22] | 0,79 / 1,08 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2016-22 | 141 | %46,1 / %48,8 | 0,95 [0,74, 1,12] | %27,0 / %25,8 | 0,80 | 0,90 [0,68, 1,10] | 0,75 / 1,08 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2023 | 14 | %28,6 / %38,2 | 0,75 [0,00, 1,11] | %71,4 / %60,3 | 0,00 | 0,64 [0,00, 1,00] | 0,66 / 0,87 | ÖLÇÜLEMEDİ | - |
| Y11c | BIST 2024-26 | 141 | %74,5 / %66,8 | 1,11 [0,99, 1,31] | %16,3 / %21,3 | 1,00 | 1,11 [0,97, 1,35] | 1,07 / 1,17 | ÖLÇÜLEMEDİ | - |

## 10. İKİ YÖNLÜ ETİKET (TERS EMARE kuralı; karar hücreleri)

| Deneme | Hücre | n | KAT5 [%95] | üst < 1 | yarı 1 / yarı 2 | TERS |
|---|---|---|---|---|---|---|
| Y11 | ABD 2023 | 3 | 1,06 [0,00, 4,00] | hayır | 0,00 / 1,98 | - |
| Y11 | ABD 2024-26 | 15 | 1,37 [0,70, 2,23] | hayır | 1,00 / 1,67 | - |
| Y11 | AVR 2023 | 1 | 0,00 [0,00, 0,00] | evet | - / 0,00 | - |
| Y11 | AVR 2024-26 | 2 | 1,59 [0,00, 2,77] | hayır | 2,77 / 0,00 | - |
| Y11 | **ters etiket** | | | | | **TERS YOK (TERS karar hücresi 0)** |
| Y11b | ABD 2023 | 0 | - [-, -] | hayır | - / - | - |
| Y11b | ABD 2024-26 | 3 | 1,85 [0,00, 5,71] | hayır | 5,71 / 1,10 | - |
| Y11b | AVR 2023 | 1 | 0,00 [0,00, 0,00] | evet | - / 0,00 | - |
| Y11b | AVR 2024-26 | 1 | 2,77 [2,77, 2,77] | hayır | - / 2,77 | - |
| Y11b | **ters etiket** | | | | | **TERS YOK (TERS karar hücresi 0)** |
| Y11c | ABD 2023 | 143 | 0,94 [0,74, 1,13] | hayır | 0,89 / 0,98 | - |
| Y11c | ABD 2024-26 | 211 | 1,07 [0,94, 1,27] | hayır | 1,04 / 1,10 | - |
| Y11c | AVR 2023 | 52 | 0,84 [0,54, 1,28] | hayır | 0,69 / 1,03 | - |
| Y11c | AVR 2024-26 | 109 | 1,06 [0,85, 1,33] | hayır | 1,20 / 0,94 | - |
| Y11c | **ters etiket** | | | | | **TERS YOK (TERS karar hücresi 0)** |

## 11. BİLGİ: High ile hedef, takip stoplu getiri, çıkış

| Deneme | Hücre | KAT5 High [%95] | KAT10 High | getiri ort / medyan | kazanan | çıkış barı ort / med | çıkış türü | d medyan |
|---|---|---|---|---|---|---|---|---|
| Y11 | ABD 2016-22 | 1,07 [0,79, 1,38] | 1,40 | %2,0 / %0,3 | %55 | 16,9 / 12 | stop 20 | %11,9 |
| Y11 | ABD 2023 | 1,60 [0,00, 3,08] | 1,63 | %6,4 / %15,2 | %67 | 16,3 / 7 | stop 3 | %17,0 |
| Y11 | ABD 2024-26 | 1,32 [0,77, 2,08] | 1,70 | %1,0 / %0,8 | %53 | 14,6 / 12 | stop 14, ters 1 | %12,3 |
| Y11 | AVR 2016-22 | 0,89 [0,24, 1,61] | 0,00 | %0,8 / %1,0 | %67 | 19,2 / 18 | stop 6 | %10,9 |
| Y11 | AVR 2023 | 0,00 [0,00, 0,00] | 0,00 | %-4,2 / %-4,2 | %0 | 11,0 / 11 | stop 1 | %9,7 |
| Y11 | AVR 2024-26 | 1,15 [0,00, 2,00] | 3,10 | %5,1 / %5,1 | %50 | 15,5 / 16 | kesik 1, stop 1 | %11,0 |
| Y11 | BIST 2016-22 | 0,49 [0,16, 0,85] | 0,85 | %-0,5 / %-4,8 | %40 | 22,1 / 19 | stop 10 | %13,1 |
| Y11 | BIST 2024-26 | 0,89 [0,52, 1,18] | 1,11 | %9,6 / %6,1 | %100 | 20,6 / 20 | stop 12 | %13,6 |
| Y11b | ABD 2016-22 | 1,46 [1,08, 2,76] | 1,05 | %4,9 / %4,2 | %100 | 13,0 / 14 | stop 4 | %12,0 |
| Y11b | ABD 2024-26 | 2,09 [1,27, 4,44] | 1,20 | %0,8 / %0,8 | %67 | 9,0 / 11 | stop 3 | %12,2 |
| Y11b | AVR 2016-22 | 2,10 [2,00, 2,21] | 0,00 | %1,6 / %1,6 | %100 | 13,5 / 14 | stop 2 | %13,4 |
| Y11b | AVR 2023 | 0,00 [0,00, 0,00] | 0,00 | %-4,2 / %-4,2 | %0 | 11,0 / 11 | stop 1 | %9,7 |
| Y11b | AVR 2024-26 | 2,00 [2,00, 2,00] | 4,50 | %11,5 / %11,5 | %100 | 12,0 / 12 | stop 1 | %11,0 |
| Y11b | BIST 2016-22 | 0,75 [0,00, 1,33] | 1,26 | %-1,2 / %0,9 | %50 | 11,2 / 12 | stop 4 | %13,1 |
| Y11b | BIST 2024-26 | 0,82 [0,47, 1,18] | 1,02 | %7,9 / %2,2 | %100 | 16,2 / 12 | stop 9 | %14,0 |
| Y11c | ABD 2016-22 | 1,07 [0,93, 1,23] | 1,18 | %0,3 / %-1,4 | %47 | 24,5 / 19 | stop 404, ters 12, zaman 48 | %12,2 |
| Y11c | ABD 2023 | 1,08 [0,94, 1,21] | 0,90 | %0,0 / %-1,9 | %47 | 23,8 / 17 | stop 124, ters 3, zaman 16 | %12,5 |
| Y11c | ABD 2024-26 | 1,14 [1,02, 1,31] | 1,13 | %0,6 / %0,0 | %50 | 20,5 / 15 | kesik 1, stop 192, ters 4, zaman 14 | %12,2 |
| Y11c | AVR 2016-22 | 1,05 [0,89, 1,23] | 1,27 | %1,6 / %1,1 | %57 | 31,5 / 26 | stop 179, ters 5, zaman 47 | %11,4 |
| Y11c | AVR 2023 | 0,83 [0,59, 1,11] | 0,66 | %-0,2 / %-1,5 | %48 | 27,4 / 24 | stop 46, zaman 6 | %12,1 |
| Y11c | AVR 2024-26 | 1,18 [0,96, 1,43] | 1,01 | %-0,3 / %-1,3 | %48 | 27,2 / 22 | kesik 3, stop 92, ters 3, zaman 11 | %11,7 |
| Y11c | BIST 2016-22 | 0,94 [0,81, 1,06] | 0,90 | %5,4 / %0,5 | %51 | 20,3 / 17 | stop 133, ters 2, zaman 6 | %13,1 |
| Y11c | BIST 2023 | 1,26 [0,49, 1,58] | 0,48 | %-0,4 / %-4,5 | %21 | 10,1 / 6 | stop 14 | %14,9 |
| Y11c | BIST 2024-26 | 1,03 [0,88, 1,18] | 1,09 | %6,9 / %3,6 | %71 | 16,6 / 15 | stop 140, ters 1 | %13,4 |

## 12. ÇOKLU KARŞILAŞTIRMA (bilgi; Y11 / Y11b karar hücreleri KAT5 bootstrap p = P(KAT <= 1), BH q 0,10 YALNIZ n >= 30 hücreler; aile 'bh_tur5')

| Deneme | Hücre | n | p | BH geçer |
|---|---|---|---|---|
| Y11 | ABD 2023 | 3 | - | BH dışı (n < 30) |
| Y11 | ABD 2024-26 | 15 | - | BH dışı (n < 30) |
| Y11 | AVR 2023 | 1 | - | BH dışı (n < 30) |
| Y11 | AVR 2024-26 | 2 | - | BH dışı (n < 30) |
| Y11b | ABD 2023 | 0 | - | BH dışı (n < 30) |
| Y11b | ABD 2024-26 | 3 | - | BH dışı (n < 30) |
| Y11b | AVR 2023 | 1 | - | BH dışı (n < 30) |
| Y11b | AVR 2024-26 | 1 | - | BH dışı (n < 30) |

## 13. CEMAL'İN GÖZÜYLE UYUM (bilgi; ölçümden bağımsız, sonuç h5 OKUNMAZ; yalnız etiket ve özellik)

Sayfa: 79 (TUR 1 30, TUR 2 30, hakem (KÖR) 19); Cemal: OLUR 37, OLMAZ 22, BELİRSİZ 20. Hakem setinde yalnız KÖR yarı. n küçük: Fisher p bilgi.

| Küme | Deneme | OLUR: tutar / tutmaz | OLMAZ: tutar / tutmaz | BELİRSİZ: tutar / tutmaz | tutanlarda OLUR payı | tutmayanlarda OLUR payı | Fisher p (OLUR / OLMAZ x tutar) |
|---|---|---|---|---|---|---|---|
| hepsi | Y11 | 1 / 36 | 0 / 22 | 0 / 20 | %100,0 (1/1) | %62,1 (36/58) | 1,000 |
| hepsi | Y11b | 0 / 37 | 0 / 22 | 0 / 20 | - (0/0) | %62,7 (37/59) | 1,000 |
| hepsi | Y11c | 6 / 31 | 1 / 21 | 2 / 18 | %85,7 (6/7) | %59,6 (31/52) | 0,240 |
| TUR 1 | Y11 | 0 / 13 | 0 / 9 | 0 / 8 | - (0/0) | %59,1 (13/22) | 1,000 |
| TUR 1 | Y11b | 0 / 13 | 0 / 9 | 0 / 8 | - (0/0) | %59,1 (13/22) | 1,000 |
| TUR 1 | Y11c | 1 / 12 | 1 / 8 | 0 / 8 | %50,0 (1/2) | %60,0 (12/20) | 1,000 |
| TUR 2 | Y11 | 1 / 14 | 0 / 4 | 0 / 11 | %100,0 (1/1) | %77,8 (14/18) | 1,000 |
| TUR 2 | Y11b | 0 / 15 | 0 / 4 | 0 / 11 | - (0/0) | %78,9 (15/19) | 1,000 |
| TUR 2 | Y11c | 3 / 12 | 0 / 4 | 2 / 9 | %100,0 (3/3) | %75,0 (12/16) | 1,000 |
| hakem (KÖR) | Y11 | 0 / 9 | 0 / 9 | 0 / 1 | - (0/0) | %50,0 (9/18) | 1,000 |
| hakem (KÖR) | Y11b | 0 / 9 | 0 / 9 | 0 / 1 | - (0/0) | %50,0 (9/18) | 1,000 |
| hakem (KÖR) | Y11c | 2 / 7 | 0 / 9 | 0 / 1 | %100,0 (2/2) | %43,8 (7/16) | 0,471 |

Şart başına (bütün sayfalar; OLUR payı = OLUR / (OLUR + OLMAZ)):

| Şart | tutan sayfa | tutanlarda karar (OLUR+OLMAZ) / OLUR payı | tutmayanlarda karar / OLUR payı | Fisher p |
|---|---|---|---|---|
| Ş1 | 6 | 5 / %80,0 | 54 / %61,1 | 0,641 |
| Ş2 | 47 | 34 / %64,7 | 25 / %60,0 | 0,789 |
| Ş3 | 65 | 49 / %65,3 | 10 / %50,0 | 0,477 |
| Ş4 | 75 | 55 / %65,5 | 4 / %25,0 | 0,141 |
| Ş5 | 43 | 33 / %72,7 | 26 / %50,0 | 0,105 |
| Ş6 | 65 | 50 / %60,0 | 9 / %77,8 | 0,461 |
| Ş7 | 45 | 34 / %61,8 | 25 / %64,0 | 1,000 |
| Ş8 | 78 | 58 / %62,1 | 1 / %100,0 | 1,000 |
| Ş9 | 9 | 7 / %85,7 | 52 / %59,6 | 0,240 |
| F14 | 52 | 39 / %61,5 | 20 / %65,0 | 1,000 |

S7 PDF'inin 50 olayında Ş9 tutan: 6 (ABD 4 / 31, AVR 2 / 9, BIST 0 / 10); No 38 Ş9 tutmaz; tutan No: 1, 12, 22, 27, 32, 37; F24-F29 hepsi NaN olay 0.

## 14. TUR 4 KURU SAYIM (GOZ_ETIKET T1.5 = T1.4, deneme Y11; `tur ac --no 4` KOŞULMADI; dosya yazılmadı)

Sürüm T1.5 (tur no 4); kota ABD 20, AVR 5, BIST 5.

| Pazar x dönem | uygun Y11 olayı (giriş <= kriz - 30 g) | gösterilmemiş |
|---|---|---|
| ABD 2023 | 3 | 3 |
| ABD 2024-26 | 15 | 12 |
| AVR 2023 | 1 | 1 |
| AVR 2024-26 | 1 | 1 |
| BIST 2023 | 0 | 0 |
| BIST 2024-26 | 12 | 11 |

Gösterilmemiş hisse (pazar başına, turda hisse en çok 1): ABD 15, AVR 2, BIST 11.
Kuru örneklem: DURDU (kota dolmadı; kota düşürülmez, ana model karar verir) (tur 4 katman ABD: kota 20 dolmadı (15; uygun 15)).

## 15. İLERLEME (satır dosyalarından; hücre başına n ve P(+5) olay / eş; h5 ve eş h5 ölçülebilir olaylar)

| Deneme | ABD 2016-22 | ABD 2023 | ABD 2024-26 | AVR 2016-22 | AVR 2023 | AVR 2024-26 | BIST 2016-22 | BIST 2023 | BIST 2024-26 |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | 8682: %34,5 / %35,8 | 2040: %39,0 / %40,0 | 4083: %42,6 / %42,2 | 4493: %29,6 / %29,1 | 815: %29,7 / %30,1 | 1711: %29,6 / %31,4 | 2588: %50,4 / %51,7 | 381: %53,0 / %54,2 | 1715: %51,3 / %52,0 |
| Y9 | 346: %50,3 / %47,4 | 146: %58,2 / %50,5 | 231: %54,1 / %44,7 | 89: %49,4 / %42,2 | 20: %55,0 / %39,2 | 55: %45,5 / %38,9 | 238: %45,8 / %45,6 | 81: %60,5 / %57,2 | 281: %56,6 / %55,7 |
| Y9b | 97: %51,5 / %47,6 | 52: %53,8 / %51,7 | 73: %58,9 / %46,1 | 18: %61,1 / %40,2 | 7: %57,1 / %32,1 | 15: %46,7 / %33,1 | 87: %49,4 / %47,4 | 34: %58,8 / %53,9 | 93: %51,6 / %55,6 |
| Y10 | 31: %54,8 / %55,2 | 13: %61,5 / %61,4 | 25: %60,0 / %42,9 | 9: %66,7 / %45,5 | 6: %33,3 / %39,9 | 6: %50,0 / %32,4 | 40: %55,0 / %48,0 | 14: %42,9 / %42,5 | 57: %49,1 / %54,8 |
| Y11 | 20: %60,0 / %46,7 | 3: %33,3 / %31,5 | 15: %60,0 / %43,9 | 6: %33,3 / %48,7 | 1: %0,0 / %25,0 | 2: %50,0 / %31,4 | 10: %30,0 / %50,4 | 0 | 12: %75,0 / %73,8 |
| Y11b | 4: %100,0 / %61,6 | 0 | 3: %66,7 / %36,1 | 2: %100,0 / %40,7 | 1: %0,0 / %25,0 | 1: %100,0 / %36,1 | 4: %50,0 / %54,0 | 0 | 9: %66,7 / %69,3 |

Satır dosyasından yeniden hesap = sonuc.json hücresi (n, P olay, P eş): TUTTU (hepsi).

## 16. VERİ SINIRLARI

- ABD: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 1411
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 580
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 581
- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.
- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı; DİPTE (Ş1) olaylarda bu yanlılık daha büyük olabilir (eş ve plasebo aynı evrenden).
- Sonradan bilgi: Ş9 Cemal'in S7 PDF'i No 38 ve TUR 2 sayfalarına bakılarak yazıldı; ABD / AVR 2023 ve 2024-26 bakılmış; 2016-22 ve BIST kısmen bakılmış (Y9 alt kümesi).

## 17. YENİDEN ÜRETİM (satır dosyasından iki hücre; biri konum eşli)

```
python - <<'EOF'
import pandas as pd
for d, p, q in [('Y11c', 'ABD', '2024-26'), ('Y11', 'ABD', '2016-22')]:
    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q)]
    a = x[x.h5.notna() & x.es_h5.notna()]; b = x[x.h5.notna() & x.k_es_h5.notna()]
    print(d, p, q, len(a), round(a.h5.sum() / a.es_h5.sum(), 4), round(a.st5.mean(), 4), round(a.es_st5.mean(), 4), len(b), round(b.h5.sum() / b.k_es_h5.sum(), 4))
EOF
```

Satır dosyası 5 MB'ı aşarsa scratch yolundadır (sonuc.json 'satir_dosya').

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); hat ve stop0 Y1 ile aynı (yalnız olay kümesi değişir); konum eşli KAT (yh_konum_es_olc): eşin F15'i olayın çeyreğinde (Ş1 dipte şartı momentum kovasıyla karışmasın); plasebo aynı hisse rastgele gün; güç tablosu 1. turunki |
| K2 | geleceğe bakma | EVET | F1-F23 4. turun mühürlü dosyalarından; F24-F29 yalnız [t-291, t-1] (yh_s9_ozellik; t barı girmez; dosya üretiminde pazar başına 25 rastgele olay t'de kesik veriyle ve [t-291, t] kesitiyle yeniden = tam: denetim json); koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 + F24-F29 yeniden = dosya, yoksa DURUR (yh_gelecek5); giriş t+1 açılış; eşin F15'i giriş gününden önceki son geçerli bar |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); Ş9 penceresi (40) ve ATR (250, en az 120) geçerli bar sayımıyla; 40 bar ya da ATR yoksa NaN = tutmaz |
| K4 | tekilleştirme | EVET | Y11* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); Ş9 yalnız t'den önceki Low'lar; regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; F24 / F27 / F28 fiyat farkı / ATR (ATR = göreli ATR250 x pencerenin ortalama kapanışı: birimsiz), F25 / F26 oran, F29 bar; AVR yerel para (birimden bağımsız) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Ş1) olaylarda batan hisse eksikliği daha büyük olabilir -> Y11 / Y11b hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | huni ön kayıtta (getirisiz, Y1 -> Ş1 -> Ş2 -> Ş9; Y10 -> Ş6 çıkar -> Ş9; Y1 -> Ş9; pazar x dönem); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; Y11 / Y11b x 4 karar hücresi BH q 0,10 yalnız n >= 30 hücreler (aile 'bh_tur5'); Y11c bilgi; bakılmış hücreler işaretli, etiket en fazla EMARE; dış sınama / BIST 'kısmen bakılmış (Y9 alt kümesi)'; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_5.md: YH_ESIK sha (yeni), ESIK_TUR4_SHA (= ON_KAYIT_4.md YH_ESIK_SHA: Y1-Y10c eşikleri aynen), ESIK_TUR3/2/1_SHA, kod / OC / S6 / FV / GE kod / güç / Y2 sha, OZELLIK_SHA, S7_OZELLIK_SHA, S9_OZELLIK_SHA, TASARIM5_SHA, Y1_OLAY_SHA; yh_kapi5 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; tasarım kontrolü (No 38 + TUR 2 kazan sayfaları) ön kayıttan ÖNCE, h5 / st5 / getiri okunmadan, bir kez; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler iş tanımı §2 (tasarım ayarı dışında) AYNEN |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve özellik dosyaları (sha mühürlü; deneme x pazar 5 olay ham veriden yeniden hesaplanıp karşılaştırılır); Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ) |
| K11 | yeniden üretim | EVET | olay_Y11*.csv.gz satır dosyaları; RAPOR_5.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; İLERLEME tablosu satır dosyalarından yeniden hesaplanır ve sonuc.json hücreleriyle karşılaştırılır; Y1 regresyonu: ölçülen her Y11* satırı olay_Y1.csv.gz satırına eşit (DURUR) |
| K12 | ifade | EVET | etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS EMARE iki yönlü kural); Y11c 'bilgi'; Cemal uyum tablosu 'bilgi' (n küçük); 'iz değil' yazılmaz; 'bağımsız' sözü yerine 'kısmen bakılmış (Y9 alt kümesi)'; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y11 önekli); yasak defter dosyalarına ve tur/1-3 klasörlerine dokunulmadı (git diff); e-posta / anahtar taraması (_yh_yaz); push yok; `tur ac --no 4` KOŞULMADI (yalnız T1.5 kuru örneklem sayımı); kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## HATA

(yok)
