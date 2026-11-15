# S6 TABAN — TASARIM SINAMASI (15 Kasım 2026)

Üreten: `python S6_TABAN.py tasarim` (S6_TABAN v1.0 (2026-11-15): Cemal'in çöl kuralları -> taban bölgesi (bant, sakin, dip savunulur, küçük mum, daralma) + al mumu / taban kırılımı). Veri: V_BIST.pkl (düzeltilmiş fiyat), geçerli barlar SY.sy_veri_hazirla. Bu bir tasarım ve göz aracıdır: getiri / iz ölçülmedi.

## ÖZET

- Seçilen eşikler: bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma kapalı (nMin 8, nMax 70, kirTol 0,02).
- Bu noktada 16 puanlı etiketten 13 / 16 tutuyor: DOĞRU bölge 9/10, YANLIŞ elenen 2/3, AL mumu 2/3.
- 108 noktanın en yüksek puanı 13/16; bu puanı 10 nokta alıyor; seçim sadelik sırasıyla.
- Evren (V_BIST 2016-26, 4735 hisse-yıl): hisse-yıl başına 6,90 bölge, 3,30 AL; bölge uzunluğu medyan 14 bar (%10-%90: 9-33).
- Ters sınama: rastgele 40 hisse-tarihin %22 kadarı o gün açık bir S6 bölgesinde (kutu içinde: %52); bütün ölçülür barlarda ortalama %28. Bu tanımla çöl NADİR DEĞİL (açık bar oranı > %10; aşağıda aday sıklığı).

## ALGORİTMA (son hâli)

```
TANIM (her geçerli bar t için yalnız t ve öncesi; geçerli bar = H > L ve V > 0; i = t'nin geçerli bar sırası, 0'dan):
  Ölçülür bar: i >= atrGun (ATR% için 250 tam TR/C_önceki değeri). Pencere W(t, n) = son n geçerli bar [i-n+1, i].
  (1) BANT    max H(W) / min L(W) - 1 <= bantMax
  (2) SAKİN   |C_i / C_{i-n+1} - 1| <= netMax
  (3) DİP     h = n // 2; L1 = min L ilk h bar [i-n+1, i-n+h]; L2 = min L son n-h bar [i-n+h+1, i]; L2 >= L1 x (1 - dipTol)
  (4) MUM     medyan((H-L)/C, W) <= kM x ATR%  (ATR% = ort(TR / önceki geçerli C) son atrGun geçerli bar [i-atrGun+1, i])
  (5) DARALMA ort((H-L)/C, W) <= daralmaOran x ort((H-L)/C, [i-n-daralmaGun+1, i-n]) ; daralmaOran = 0 -> şart yok (kapalı)
  TABAN(t) = şartları sağlayan EN BÜYÜK n (nMax'tan nMin'e, ilk tutan). bas = i-n+1, TAVAN = max H(W) (tavan mumu = o High'ın İLK barı), DİP = min L(W).
  SINIF (bilgi): DİP = konum120 = (C - min C) / (max C - min C) (son 120 geçerli kapanış) <= 0,25 VE C / max C - 1 <= -%10;
                 YOL = C > SMA50 VE SMA50_i > SMA50_{i-20}; ikisi de değilse ORTA (öncelik DİP > YOL > ORTA).
  DURUM MAKİNESİ (Python ve Pine birebir; sıra önemli):
    AL_i = TABAN(i-1) var VE C_i > TAVAN(i-1). KIRILDI_i = TABAN(i-1) var VE AL değil VE C_i < DİP(i-1) x (1 - kirTol)  (iş tanımının harfi).
    AL / KIRILDI: açık bölge varsa i'de biter (kutu i'yi içerir; üst / alt i ile değişmez); i hiçbir bölgeye girmez. Açık bölge yoksa (önceki bar
    tabanlı ama bölgede değil: art arda ikinci AL ya da AL / KIRILDI sonrası kutu nMin bar dolmadan) işaret 'bölgesiz' basılır (AL_BOLGESIZ).
    Değilse ve TABAN(i) var:
       acik                                  -> AYNI bölge (pencere açık bölgeye değiyor; başlangıç ileri / geri oynasa da: 'bitişik parçalar tek bölge', K2)
       acik değil, son bölge kendiliğinden söndü (AL / KIRILDI değil) ve bas_i <= son bölgenin son barı -> SÖNEN BÖLGE SÜRER (aynı kutu)
       aksi -> YENİ bölge (sınıf = açılış barının sınıfı); sinir = önceki bölgenin son barı (yoksa -1; AL / KIRILDI'dan sonra o bar);
               yeni bölge yalnız i - max(bas_i, sinir + 1) + 1 >= nMin ise açılır (kırpılmış kutu en az nMin bar), değilse bar bölgesiz (KISA)
       kutu: sol = min(max(bas, sinir + 1)) (kutular üst üste binmez), sağ = i, üst = max TAVAN, alt = min DİP (bölgenin barları boyunca)
    Değilse acik ise bölge SÖNER (son bar i-1; durum SÖNDÜ).
    (surTol >= 0 yalnız Python BİLGİ kipi: iş tanımının harfi 'başlangıç en çok surTol bar ileri kayarsa aynı bölge, yoksa yeni bölge'; Pine'da yok.)
```

Sabitler: nMin = 8, nMax = 70, kirTol = 0.02, atrGun = 250, daralmaGun = 60, konumGun = 120, smaGun = 50, smaEgimGun = 20, dipKonum = 0.25, dipDusus = -0.1, surTol = -1, hacimGun = 20.

İş tanımında açık bırakılan noktalar (kod ve Pine'da aynı karar): (i) yarılar h = n // 2 (tek n'de fazladan bar ikinci yarıda); (ii) ölçülür bar i >= 250 (ATR% tam); (iii) tavan mumu = pencerede en yüksek High'ın İLK barı; (iv) SÜREKLİLİK (iş tanımından SAPMA, gerekçe HATA bölümünde): açık bölgede taban sürdükçe başlangıç ne kadar oynarsa oynasın aynı bölge (pencereler birleşir); iş tanımının harfi (±2 bar) BİLGİ olarak aşağıda ayrıca koşuldu; yeni kutu önceki bölgenin son barını geçmez; (v) taban bir gün kaybolup pencere eski bölgenin son barına dokunarak dönerse aynı bölge sürer (K2 'bitişik parçalar tek bölge'); (vi) AL / KIRILDI iş tanımının harfiyle: önceki barda taban varsa (bölge şartı yok; ilk sürümdeki 'kilit' ve 'açık bölge' şartları kaldırıldı, HATA bölümü); AL / KIRILDI barı hiçbir bölgeye girmez, sonraki kutu o bardan sonra başlar; (vii) önceki bar tabanlı ama açık bölge yoksa AL 'bölgesiz' işarettir (kutusuz); yeni kutu kırpıldıktan sonra en az nMin bar olmalı; (viii) sınıf için 120 gün aralığı ve SMA50 geçerli bar kapanışlarıyla, 'SMA50 yükseliyor' = SMA50_t > SMA50_t-20 (S5 ile aynı).

## ETİKET TABLOSU (seçilen eşikler)

| etiket | Cemal aralığı / günü | S6 bölgesi (en çok örten) | örtüşme | AL günü | sonuç |
|---|---|---|---|---|---|
| D1 FENER 2025-10 | 2025-10-14 .. 2025-11-07 | 2025-10-07 .. 2025-11-11 (25 bar, DIP, AL) | 1,00 (birleşim 1,00) | 2025-11-11 | ✓ |
| D2 CCOLA 2025-10 | 2025-10-02 .. 2025-10-15 | 2025-07-02 .. 2025-10-20 (78 bar, ORTA, AL) | 1,00 (birleşim 1,00) | 2025-10-20 | ✓ |
| D3 ENJSA 2021-11 (tamamı) | 2021-10-26 .. 2021-11-16 | 2021-10-19 .. 2021-11-18 (22 bar, YOL, AL) | 1,00 (birleşim 1,00) | 2021-11-18 | ✓ |
| D4 ENJSA 2025-02 | 2025-01-20 .. 2025-02-18 (yaklaşık) | 2024-11-11 .. 2025-02-26 (77 bar, ORTA, SONDU) | 1,00 (birleşim 1,00) | - | ✓ |
| D5 ENJSA 2025-05/06 | 2025-05-08 .. 2025-06-27 | 2025-04-22 .. 2025-06-30 (45 bar, DIP, AL) | 1,00 (birleşim 1,00) | 2025-06-30 | ✓ |
| D6 DESA 2021-10/12 | 2021-10-27 .. 2021-12-23 | 2021-11-04 .. 2021-12-06 (23 bar, DIP, AL) | 0,56 (birleşim 0,63) | 2021-12-06 | ✓ |
| D7 KNFRT 2022-06/09 | 2022-06-15 .. 2022-09-13 (yaklaşık) | 2022-07-25 .. 2022-08-08 (11 bar, YOL, AL) | 0,18 (birleşim 0,35) | 2022-08-08 | ✗ |
| D8 TUCLK 2025-06/08 | 2025-06-10 .. 2025-08-21 (yaklaşık) | 2025-06-18 .. 2025-08-06 (35 bar, YOL, AL) | 0,67 (birleşim 0,92) | 2025-08-06 | ✓ |
| D9 YKSLN 2026-03/05 | 2026-03-19 .. 2026-05-15 (yaklaşık) | 2026-02-24 .. 2026-05-08 (51 bar, DIP, AL) | 0,90 (birleşim 0,90) | 2026-05-08 | ✓ |
| D10 PAPIL küçük taban | 2025-11-13 .. 2025-12-10 | 2025-11-11 .. 2025-12-11 (23 bar, DIP, AL) | 1,00 (birleşim 1,00) | 2025-12-11 | ✓ |
| Y1 ENJSA 2021-08/09 (net +%8,0) | 2021-08-11 .. 2021-09-01 | 2021-05-21 .. 2021-08-27 (66 bar, YOL, AL) | 0,87 (birleşim 1,00) | 2021-08-27; 2021-09-01 günü bölge kapalı | ✓ |
| Y2 ENJSA 2021-09/10 (net +%9,7) | 2021-09-28 .. 2021-10-18 | 2021-08-31 .. 2021-10-18 (35 bar, YOL, AL) | 1,00 (birleşim 1,00) | 2021-10-18; 2021-10-18 günü bölge kapalı | ✓ |
| Y3 TUCLK 2026-07/08 (kayan düşüş) | 2026-07-24 .. 2026-08-13 | 2026-07-29 .. 2026-08-25 (20 bar, DIP, AL) | 0,80 (birleşim 1,00) | 2026-08-25; 2026-08-13 günü bölge AÇIK | ✗ |
| A1 KNFRT al mumu 2022-09-14 | 2022-09-14 ±3 | - | - | AL yok | ✗ |
| A2 TUCLK al mumu 2025-08-22 | 2025-08-22 ±3 | - | - | 2025-08-22 | ✓ |
| A3 PAPIL al mumu 2025-12-11 | 2025-12-11 ±1 | - | - | 2025-12-11 | ✓ |
| B1 PAPIL büyük taban (bilgi) | 2025-10-27 .. 2026-03-02 | 2025-11-11 .. 2025-12-11 (23 bar, DIP, AL) | 0,26 (birleşim 0,62) | 2025-12-11 | bilgi ✗ |
| B2 ENJSA 2025-07/09 bant %23 (bilgi) | 2025-07-28 .. 2025-09-12 | 2025-07-18 .. 2025-08-13 (19 bar, YOL, AL) | 0,37 (birleşim 0,37) | 2025-08-13; 2025-09-12 günü bölge kapalı | bilgi ✓ |
| B3 DESA taban bitişi (bilgi) | 2021-12-23 ±3 | - | - | AL yok, 2. tarih (2022-02-02) ±3: 2022-02-03; civar işaretler: 2021-12-06 AL, 2022-02-03 AL | bilgi ✗ |

Örtüşme = en çok örten TEK bölge kutusunun Cemal aralığıyla kesişimi / Cemal aralığı (geçerli bar); birleşim = bütün bölgelerin birlikte örttüğü pay (bilgi). YANLIŞ etiketlerde ✓ = örtüşme < 0,5 ya da aralığın son günü (S5 karar günü) bölge açık değil (elendi). AL etiketinde ✓ = etiket gününe ±tol geçerli bar içinde AL.

## IZGARA (108 nokta, tamamı)

Seçim kuralı: puan = DOĞRU bulunan (10) + YANLIŞ elenen (3) + AL mumu tutan (3); en yüksek puan; eşitlikte EN SADE: sözlük sırasıyla (daralma kapalı -> 0, 0,9 -> 1, 0,8 -> 2), |dipTol - 0,05|, |kM - 0,90|, |netMax - 0,05|, |bantMax - 0,20| en küçük.

Puan dağılımı: 13/16: 10 nokta, 12/16: 29 nokta, 11/16: 13 nokta, 10/16: 20 nokta, 9/16: 20 nokta, 8/16: 12 nokta, 7/16: 4 nokta.

En yüksek puanlı 10 nokta: bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma kapalı; bant 0,12 · net 0,03 · kM 1,00 · dipTol 0,05 · daralma kapalı; bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,02 · daralma kapalı; bant 0,12 · net 0,03 · kM 1,00 · dipTol 0,02 · daralma kapalı; bant 0,20 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma 0,9; bant 0,20 · net 0,03 · kM 1,00 · dipTol 0,05 · daralma 0,9; bant 0,20 · net 0,05 · kM 0,90 · dipTol 0,02 · daralma 0,9; bant 0,20 · net 0,03 · kM 0,90 · dipTol 0,02 · daralma 0,9; bant 0,20 · net 0,05 · kM 1,00 · dipTol 0,02 · daralma 0,9; bant 0,20 · net 0,03 · kM 1,00 · dipTol 0,02 · daralma 0,9.

Etiket başına tutan nokta sayısı (108 içinde): D1: 108; D2: 72; D3: 108; D4: 72; D5: 72; D6: 48; D7: 0; D8: 108; D9: 108; D10: 108; Y1: 108; Y2: 75; Y3: 0; A1: 0; A2: 66; A3: 72; B1: 0; B2: 104; B3: 0.

| # | bantMax | netMax | kM | dipTol | daralma | puan | DOĞRU | YANLIŞ | AL | tutmayan puanlı etiketler |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0,12 | 0,03 | 0,75 | 0,02 | 0,8 | 8 | 5 | 2 | 1 | D2, D4, D5, D6, D7, Y3, A1, A2 |
| 2 | 0,12 | 0,03 | 0,75 | 0,02 | 0,9 | 10 | 7 | 2 | 1 | D5, D6, D7, Y3, A1, A2 |
| 3 | 0,12 | 0,03 | 0,75 | 0,02 | kapalı | 10 | 7 | 2 | 1 | D5, D6, D7, Y3, A1, A2 |
| 4 | 0,12 | 0,03 | 0,75 | 0,05 | 0,8 | 8 | 5 | 2 | 1 | D2, D4, D5, D6, D7, Y3, A1, A2 |
| 5 | 0,12 | 0,03 | 0,75 | 0,05 | 0,9 | 10 | 7 | 2 | 1 | D5, D6, D7, Y3, A1, A2 |
| 6 | 0,12 | 0,03 | 0,75 | 0,05 | kapalı | 10 | 7 | 2 | 1 | D5, D6, D7, Y3, A1, A2 |
| 7 | 0,12 | 0,03 | 0,90 | 0,02 | 0,8 | 9 | 6 | 2 | 1 | D2, D4, D6, D7, Y3, A1, A2 |
| 8 | 0,12 | 0,03 | 0,90 | 0,02 | 0,9 | 11 | 8 | 2 | 1 | D6, D7, Y3, A1, A2 |
| 9 | 0,12 | 0,03 | 0,90 | 0,02 | kapalı | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 10 | 0,12 | 0,03 | 0,90 | 0,05 | 0,8 | 9 | 6 | 2 | 1 | D2, D4, D6, D7, Y3, A1, A2 |
| 11 | 0,12 | 0,03 | 0,90 | 0,05 | 0,9 | 11 | 8 | 2 | 1 | D6, D7, Y3, A1, A2 |
| 12 **seçilen** | 0,12 | 0,03 | 0,90 | 0,05 | kapalı | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 13 | 0,12 | 0,03 | 1,00 | 0,02 | 0,8 | 9 | 6 | 2 | 1 | D2, D4, D6, D7, Y3, A1, A2 |
| 14 | 0,12 | 0,03 | 1,00 | 0,02 | 0,9 | 11 | 8 | 2 | 1 | D6, D7, Y3, A1, A2 |
| 15 | 0,12 | 0,03 | 1,00 | 0,02 | kapalı | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 16 | 0,12 | 0,03 | 1,00 | 0,05 | 0,8 | 9 | 6 | 2 | 1 | D2, D4, D6, D7, Y3, A1, A2 |
| 17 | 0,12 | 0,03 | 1,00 | 0,05 | 0,9 | 11 | 8 | 2 | 1 | D6, D7, Y3, A1, A2 |
| 18 | 0,12 | 0,03 | 1,00 | 0,05 | kapalı | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 19 | 0,12 | 0,05 | 0,75 | 0,02 | 0,8 | 7 | 5 | 2 | 0 | D2, D4, D5, D6, D7, Y3, A1, A2, A3 |
| 20 | 0,12 | 0,05 | 0,75 | 0,02 | 0,9 | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 21 | 0,12 | 0,05 | 0,75 | 0,02 | kapalı | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 22 | 0,12 | 0,05 | 0,75 | 0,05 | 0,8 | 7 | 5 | 2 | 0 | D2, D4, D5, D6, D7, Y3, A1, A2, A3 |
| 23 | 0,12 | 0,05 | 0,75 | 0,05 | 0,9 | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 24 | 0,12 | 0,05 | 0,75 | 0,05 | kapalı | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 25 | 0,12 | 0,05 | 0,90 | 0,02 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 26 | 0,12 | 0,05 | 0,90 | 0,02 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 27 | 0,12 | 0,05 | 0,90 | 0,02 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 28 | 0,12 | 0,05 | 0,90 | 0,05 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 29 | 0,12 | 0,05 | 0,90 | 0,05 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 30 | 0,12 | 0,05 | 0,90 | 0,05 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 31 | 0,12 | 0,05 | 1,00 | 0,02 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 32 | 0,12 | 0,05 | 1,00 | 0,02 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 33 | 0,12 | 0,05 | 1,00 | 0,02 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 34 | 0,12 | 0,05 | 1,00 | 0,05 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 35 | 0,12 | 0,05 | 1,00 | 0,05 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 36 | 0,12 | 0,05 | 1,00 | 0,05 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 37 | 0,12 | 0,08 | 0,75 | 0,02 | 0,8 | 7 | 5 | 2 | 0 | D2, D4, D5, D6, D7, Y3, A1, A2, A3 |
| 38 | 0,12 | 0,08 | 0,75 | 0,02 | 0,9 | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 39 | 0,12 | 0,08 | 0,75 | 0,02 | kapalı | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 40 | 0,12 | 0,08 | 0,75 | 0,05 | 0,8 | 7 | 5 | 2 | 0 | D2, D4, D5, D6, D7, Y3, A1, A2, A3 |
| 41 | 0,12 | 0,08 | 0,75 | 0,05 | 0,9 | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 42 | 0,12 | 0,08 | 0,75 | 0,05 | kapalı | 9 | 7 | 2 | 0 | D5, D6, D7, Y3, A1, A2, A3 |
| 43 | 0,12 | 0,08 | 0,90 | 0,02 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 44 | 0,12 | 0,08 | 0,90 | 0,02 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 45 | 0,12 | 0,08 | 0,90 | 0,02 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 46 | 0,12 | 0,08 | 0,90 | 0,05 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 47 | 0,12 | 0,08 | 0,90 | 0,05 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 48 | 0,12 | 0,08 | 0,90 | 0,05 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 49 | 0,12 | 0,08 | 1,00 | 0,02 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 50 | 0,12 | 0,08 | 1,00 | 0,02 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 51 | 0,12 | 0,08 | 1,00 | 0,02 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 52 | 0,12 | 0,08 | 1,00 | 0,05 | 0,8 | 8 | 6 | 2 | 0 | D2, D4, D6, D7, Y3, A1, A2, A3 |
| 53 | 0,12 | 0,08 | 1,00 | 0,05 | 0,9 | 10 | 8 | 2 | 0 | D6, D7, Y3, A1, A2, A3 |
| 54 | 0,12 | 0,08 | 1,00 | 0,05 | kapalı | 12 | 9 | 2 | 1 | D7, Y3, A1, A3 |
| 55 | 0,20 | 0,03 | 0,75 | 0,02 | 0,8 | 9 | 5 | 2 | 2 | D2, D4, D5, D6, D7, Y3, A1 |
| 56 | 0,20 | 0,03 | 0,75 | 0,02 | 0,9 | 12 | 8 | 2 | 2 | D5, D7, Y3, A1 |
| 57 | 0,20 | 0,03 | 0,75 | 0,02 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 58 | 0,20 | 0,03 | 0,75 | 0,05 | 0,8 | 9 | 5 | 2 | 2 | D2, D4, D5, D6, D7, Y3, A1 |
| 59 | 0,20 | 0,03 | 0,75 | 0,05 | 0,9 | 12 | 8 | 2 | 2 | D5, D7, Y3, A1 |
| 60 | 0,20 | 0,03 | 0,75 | 0,05 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 61 | 0,20 | 0,03 | 0,90 | 0,02 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 62 | 0,20 | 0,03 | 0,90 | 0,02 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 63 | 0,20 | 0,03 | 0,90 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 64 | 0,20 | 0,03 | 0,90 | 0,05 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 65 | 0,20 | 0,03 | 0,90 | 0,05 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 66 | 0,20 | 0,03 | 0,90 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 67 | 0,20 | 0,03 | 1,00 | 0,02 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 68 | 0,20 | 0,03 | 1,00 | 0,02 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 69 | 0,20 | 0,03 | 1,00 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 70 | 0,20 | 0,03 | 1,00 | 0,05 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 71 | 0,20 | 0,03 | 1,00 | 0,05 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 72 | 0,20 | 0,03 | 1,00 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 73 | 0,20 | 0,05 | 0,75 | 0,02 | 0,8 | 9 | 5 | 2 | 2 | D2, D4, D5, D6, D7, Y3, A1 |
| 74 | 0,20 | 0,05 | 0,75 | 0,02 | 0,9 | 12 | 8 | 2 | 2 | D5, D7, Y3, A1 |
| 75 | 0,20 | 0,05 | 0,75 | 0,02 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 76 | 0,20 | 0,05 | 0,75 | 0,05 | 0,8 | 9 | 5 | 2 | 2 | D2, D4, D5, D6, D7, Y3, A1 |
| 77 | 0,20 | 0,05 | 0,75 | 0,05 | 0,9 | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 78 | 0,20 | 0,05 | 0,75 | 0,05 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 79 | 0,20 | 0,05 | 0,90 | 0,02 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 80 | 0,20 | 0,05 | 0,90 | 0,02 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 81 | 0,20 | 0,05 | 0,90 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 82 | 0,20 | 0,05 | 0,90 | 0,05 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 83 | 0,20 | 0,05 | 0,90 | 0,05 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 84 | 0,20 | 0,05 | 0,90 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 85 | 0,20 | 0,05 | 1,00 | 0,02 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 86 | 0,20 | 0,05 | 1,00 | 0,02 | 0,9 | 13 | 9 | 2 | 2 | D7, Y3, A1 |
| 87 | 0,20 | 0,05 | 1,00 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 88 | 0,20 | 0,05 | 1,00 | 0,05 | 0,8 | 10 | 6 | 2 | 2 | D2, D4, D6, D7, Y3, A1 |
| 89 | 0,20 | 0,05 | 1,00 | 0,05 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 90 | 0,20 | 0,05 | 1,00 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 91 | 0,20 | 0,08 | 0,75 | 0,02 | 0,8 | 8 | 5 | 1 | 2 | D2, D4, D5, D6, D7, Y2, Y3, A1 |
| 92 | 0,20 | 0,08 | 0,75 | 0,02 | 0,9 | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 93 | 0,20 | 0,08 | 0,75 | 0,02 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 94 | 0,20 | 0,08 | 0,75 | 0,05 | 0,8 | 8 | 5 | 1 | 2 | D2, D4, D5, D6, D7, Y2, Y3, A1 |
| 95 | 0,20 | 0,08 | 0,75 | 0,05 | 0,9 | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 96 | 0,20 | 0,08 | 0,75 | 0,05 | kapalı | 11 | 8 | 1 | 2 | D5, D7, Y2, Y3, A1 |
| 97 | 0,20 | 0,08 | 0,90 | 0,02 | 0,8 | 9 | 6 | 1 | 2 | D2, D4, D6, D7, Y2, Y3, A1 |
| 98 | 0,20 | 0,08 | 0,90 | 0,02 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 99 | 0,20 | 0,08 | 0,90 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 100 | 0,20 | 0,08 | 0,90 | 0,05 | 0,8 | 9 | 6 | 1 | 2 | D2, D4, D6, D7, Y2, Y3, A1 |
| 101 | 0,20 | 0,08 | 0,90 | 0,05 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 102 | 0,20 | 0,08 | 0,90 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 103 | 0,20 | 0,08 | 1,00 | 0,02 | 0,8 | 9 | 6 | 1 | 2 | D2, D4, D6, D7, Y2, Y3, A1 |
| 104 | 0,20 | 0,08 | 1,00 | 0,02 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 105 | 0,20 | 0,08 | 1,00 | 0,02 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 106 | 0,20 | 0,08 | 1,00 | 0,05 | 0,8 | 9 | 6 | 1 | 2 | D2, D4, D6, D7, Y2, Y3, A1 |
| 107 | 0,20 | 0,08 | 1,00 | 0,05 | 0,9 | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |
| 108 | 0,20 | 0,08 | 1,00 | 0,05 | kapalı | 12 | 9 | 1 | 2 | D7, Y2, Y3, A1 |

## SÜREKLİLİK KURALI: seçilen (birleşim) ile iş tanımının harfi (±2 bar) — seçilen eşiklerde, 8 etiket hissesinin tamamında

| kip | puan /16 | bölge sayısı | kutusu üst üste binen çift | tutmayan puanlı etiketler |
|---|---|---|---|---|
| birlesim (seçilen) | 13 | 572 | 0 | D7, Y3, A1 |
| is_tanimi_harfi_2bar | 13 | 862 | 584 | D7, Y3, A1 |

## TERS SINAMA ve EVREN SAYIMI (seçilen eşikler; V_BIST 2016-01-01 .. 2026-08-31, ölçülür barlar)

- Hisse-yıl: 4735; bölge (açılış yılına göre): 32668; AL: 15625.
- Bütün AL işaretleri 18400 (bunun 2775 tanesi bölgesiz: önceki bar tabanlı ama açık bölge yok — art arda AL ya da AL / KIRILDI sonrası kutu 8 bar dolmadan; kutusuz üçgen); KIRILDI işaretleri 5635.
- Hisse-yıl başına bölge 6,90, AL 3,30 (bölgeyi kapatan AL). Hisse-yıl başına bölge sayısı dağılımı: 0: 31, 1: 83, 2: 112, 3: 223, 4: 398, 5: 578, 6+: 3310.
- Bölge uzunluğu (geçerli bar, kutu sol..sağ): min 8, %10 9, %25 10, medyan 14, %75 22, %90 33, en çok 206. Kovalar: 8-14: 16727, 15-29: 11740, 30-49: 3162, 50-70: 699, 71-100: 257, 101-1000000: 83.
- Sınıf (açılış günü): DIP: 9983, ORTA: 10440, YOL: 12245. Bitiş: ACIK: 205, AL: 15625, KIRILDI: 5246, SONDU: 11592.
- Yıllara göre (hisse / bölge / AL): 2016: 325 / 1545 / 607; 2017: 354 / 2517 / 1391; 2018: 359 / 2581 / 822; 2019: 371 / 3047 / 1609; 2020: 377 / 2389 / 1316; 2021: 385 / 2970 / 1315; 2022: 437 / 3170 / 1829; 2023: 473 / 2771 / 1152; 2024: 506 / 4383 / 1998; 2025: 568 / 4367 / 2127; 2026: 580 / 2928 / 1459.
- Hisse başına ortalama: ölçülür barların %28,4 kadarı o gün açık bölgede, %55,0 kadarı sonradan çizilen bir kutunun içinde.
- Ters sınama (tohum 615, 40 rastgele hisse-tarih): o gün açık bölge %22, kutu içinde %52.

BİLGİ (seçimi değiştirmez): en yüksek puanlı 10 noktanın evrende sıklığı (aynı evren ve dönem).

| eşikler | bölge / hisse-yıl | AL / hisse-yıl | açık bar oranı (bütün barlar havuzu) | uzunluk medyan | uzunluk %90 |
|---|---|---|---|---|---|
| bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma kapalı **seçilen** | 6,90 | 3,30 | %30,0 | 14 | 33 |
| bant 0,12 · net 0,03 · kM 1,00 · dipTol 0,05 · daralma kapalı | 7,23 | 3,51 | %31,8 | 14 | 33 |
| bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,02 · daralma kapalı | 6,83 | 3,17 | %27,7 | 14 | 32 |
| bant 0,12 · net 0,03 · kM 1,00 · dipTol 0,02 · daralma kapalı | 7,18 | 3,38 | %29,5 | 14 | 32 |
| bant 0,20 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma 0,9 | 6,20 | 2,91 | %34,8 | 17 | 44 |
| bant 0,20 · net 0,03 · kM 1,00 · dipTol 0,05 · daralma 0,9 | 6,40 | 3,02 | %36,0 | 17 | 44 |
| bant 0,20 · net 0,05 · kM 0,90 · dipTol 0,02 · daralma 0,9 | 6,44 | 3,20 | %34,9 | 17 | 43 |
| bant 0,20 · net 0,03 · kM 0,90 · dipTol 0,02 · daralma 0,9 | 6,20 | 2,82 | %31,6 | 17 | 42 |
| bant 0,20 · net 0,05 · kM 1,00 · dipTol 0,02 · daralma 0,9 | 6,65 | 3,32 | %36,2 | 17 | 43 |
| bant 0,20 · net 0,03 · kM 1,00 · dipTol 0,02 · daralma 0,9 | 6,41 | 2,92 | %32,8 | 17 | 42 |

Ters sınama noktaları:

| sembol | tarih | o gün açık bölge | kutu içinde | taban n |
|---|---|---|---|---|
| EDIP | 2025-12-05 | - | evet | - |
| SUMAS | 2021-05-17 | - | - | - |
| KLNMA | 2020-05-08 | - | - | - |
| INFO | 2020-03-23 | evet | evet | 9 |
| DMSAS | 2024-05-21 | evet | evet | 11 |
| YYAPI | 2024-08-06 | - | - | - |
| GLRYH | 2019-01-16 | - | evet | - |
| KRDMD | 2020-01-15 | - | - | - |
| NETAS | 2026-02-04 | - | evet | - |
| SANKO | 2025-09-05 | - | - | - |
| ASTOR | 2026-05-21 | - | - | - |
| RYGYO | 2022-10-26 | - | - | - |
| FADE | 2022-07-28 | - | - | - |
| ETYAT | 2021-01-26 | - | - | - |
| ELITE | 2024-04-25 | evet | evet | 9 |
| EUYO | 2021-01-27 | evet | evet | - |
| TATGD | 2019-10-17 | - | evet | - |
| RUZYE | 2025-07-23 | - | - | - |
| DERIM | 2022-03-03 | - | evet | - |
| IZFAS | 2021-12-28 | - | - | - |
| EGSER | 2018-11-08 | - | evet | - |
| PRKAB | 2016-06-29 | - | evet | 45 |
| GMTAS | 2024-10-11 | - | evet | - |
| MAVI | 2025-03-10 | - | evet | - |
| BANVT | 2018-04-03 | - | - | - |
| INTEM | 2023-01-26 | - | - | - |
| BIZIM | 2024-10-14 | - | evet | - |
| CASA | 2019-10-10 | evet | evet | 22 |
| BIMAS | 2023-06-09 | - | - | - |
| ASUZU | 2026-07-23 | evet | evet | 10 |
| GLRYH | 2017-11-10 | - | - | - |
| DOAS | 2019-06-17 | - | evet | 11 |
| ANSGR | 2019-02-21 | evet | evet | 32 |
| GATEG | 2023-11-07 | - | - | - |
| ALKIM | 2018-01-31 | evet | evet | 16 |
| EKIZ | 2022-11-08 | - | - | - |
| ELITE | 2024-11-14 | - | evet | - |
| TRMET | 2018-05-07 | - | - | - |
| EMKEL | 2026-04-21 | - | - | - |
| GOODY | 2024-06-26 | evet | evet | 13 |

Not: evren bugünün listesi (hayatta kalma yanlılığı); likidite süzgeci yok; sayım ölçüm değildir.

<!-- ELLE YAZILAN BÖLÜMLER (s6_tasarim yeniden yazarken bu satırdan sonrasını korur) -->

## ETİKET NOTLARI (seçilen noktada; sayılar yukarıdaki tablodan ve ham veriden)

- **D7 / A1 KNFRT tutmuyor (108 noktanın hiçbirinde)**: V_BIST'te 2022 Haziran-Temmuz'da taban yok (medyan mum ATR'nin üstünde; 20-21 Tem'de +%15 sıçrama). Cemal'in aralığında (15 Haz - 13 Eyl) fiyat 4,2'den 7,7'ye çıkıyor (bant ~%80): fotoğraftaki taban ile V_BIST düzeltilmiş fiyatı uyuşmuyor görünüyor. Kod Ağustos'ta iki kısa kutu buluyor (25 Tem - 8 Ağu AL 8 Ağu; 16-29 Ağu AL 29 Ağu); 14 Eyl'de AL yok.
- **Y3 TUCLK kayan düşüş elenmiyor (108 noktanın hiçbirinde)**: kayma Haziran-Temmuz'da (kapanış 4,55 -> 3,76); 29 Tem - 13 Ağu kendi içinde düz (net -%0,3 .. +%1,6, dip savunması +%1,4 .. +%1,9, medyan mum ATR'nin 0,5-0,7'si). S6 penceresi kısa olduğu için öncesindeki kaymayı görmüyor; daralma şartı (0,8 / 0,9) da elemiyor. 'Düşüş sonrası' ile 'kayan kanal' ayrımı için pencere öncesine bakan bir şart gerekir (iş tanımında yok; öneri: ana model kararı).
- **Y1 / Y2 zayıf tutuyor**: iki pencere de bir S6 kutusunun içinde (örtüşme 0,87 / 1,00). 'Elendi' sayılmaları yalnız kuralın ikinci yarısından: kutu S5 karar gününde ya da önce AL ile kapanmış (Y1: AL 27 Ağu 2021; Y2: AL 18 Eki 2021, S5 karar gününün kendisi). Yani eğimli bu pencereleri S6 'taban + AL' olarak görüyor.
- **A2 TUCLK tutuyor, ama ilk AL erken**: ilk kutu 18 Haz - 6 Ağu 2025, AL 6 Ağu (kapanış 5,778 > pencere tavanı 5,708, Haziran'dan). Fiyat tabana döndü, yeni kutu 7-22 Ağu, AL 22 Ağu (Cemal'in al mumu). Göstergede iki üçgen görünür.
- **A3 PAPIL tutuyor**: kutu 11 Kas - 11 Ara 2025, tavan 16,96, 11 Ara kapanışı 17,01 -> AL. Cemal'in K6b notu: sonraki yükseliş +%8 ile söndü (K6b'den; burada getiri ölçülmedi).
- **D6 DESA sınırda (0,56)**: kutu 4 Kas - 6 Ara 2021 (AL 6 Ara); ikinci kutu 24 Ara 2021 - 3 Şub 2022, AL 3 Şub (Cemal'in uzun seçeneği 2 Şub'a bir bar). B3 bilgi: 23 Ara ±3'te AL yok.
- **D2 CCOLA / D4 ENJSA**: kutular 78 / 77 bar ve ORTA sınıf; Cemal aralığını tamamen içeriyor ama çok daha uzun (birleşim kuralı ile taban oynadıkça kutu büyür).
- **B1 PAPIL büyük taban**: bant %12 ile tek bölge olmuyor (en çok örten kutu %26). Büyük çöller bant > %12 ister; seçilen nokta küçük tabanları seçiyor.

## SÜRÜM KAYDI (sonuç görüldükten sonra yapılan tanım düzeltmeleri; eşik değerleri hiç değişmedi)

| sürüm | değişiklik | en yüksek puan | seçilen (bant / net / kM / dipTol / daralma) | DOĞRU / YANLIŞ / AL | evren bölge, AL / hisse-yıl |
|---|---|---|---|---|---|
| v0 | ilk kod: YANLIŞ = yalnız 'örtüşme < 0,5'; AL / KIRILDI yalnız açık bölgeden + 'kilit' (yeni bölge AL barından sonra başlar) | 11 | 0,20 / 0,03 / 0,90 / 0,02 / 0,9 | 9 / 1 / 1 | koşulmadı |
| v1 | YANLIŞ kuralı iş tanımına göre tamamlandı ('ya da o gün bölge bitmiş') | 12 | 0,12 / 0,05 / 0,90 / 0,05 / kapalı | 9 / 3 / 0 | 6,63 / 3,34 |
| v2 | AL / KIRILDI iş tanımının harfine döndü (önceki barda taban yeter; kilit ve 'açık bölge' şartı kaldırıldı); yeni kutu önceki bölgenin son barını geçmez (kırpma hatası testle bulundu, düzeltildi) | 13 | 0,12 / 0,03 / 0,90 / 0,05 / kapalı | 9 / 2 / 2 | 7,55 / 3,63 (kutu en kısa 1 bar) |
| v3 (son) | kırpılmış yeni kutu en az nMin bar (iş tanımı 'bölge uzunluğu nMin..nMax') | 13 | 0,12 / 0,03 / 0,90 / 0,05 / kapalı | 9 / 2 / 2 | 6,90 / 3,30 (kutu en kısa 8 bar) |

v2'deki AL düzeltmesi A1-A3'ün 0/3 olduğu GÖRÜLDÜKTEN sonra yapıldı; gerekçe iş tanımının harfidir (AL = 't-1'de taban var ve C_t > TAVAN(t-1)'), ama sıralama SAPMA riskidir: ana model değerlendirmeli. v1 dosyaları ayrıca saklanmadı; sayılar koşu çıktısından yazıldı.

## ÖNEK DEĞİŞMEZLİĞİ

- test_s6_taban.py: sentetik seride her 7 barda bir kesim (d.iloc[:T]) ve gerçek PAPIL'de her 37 barda bir kesim: n, bas, tavan, dip, tavan mumu, al, kirildi, bolge_id, durum, kutu sol / sağ / üst / alt ve sınıf sütunları tam seriyle birebir (fark 0). T sonrası fiyatlar x1,7 bozulunca ilk 520 satır aynı.
- Kutunun SOL kenarı geriye büyüyebilir (taban eski mumları kattıkça); bu çizimdir ve satırda o günkü değerdir (önek testine dahil). Etiket kıyasında kullanılan kutu, verinin sonundaki son hâlidir (geriye bakış; yalnız göz kıyası).
- Python ile Pine birebirliği: `s6_pine_ayna` Pine döngüsünün satır satır Python çevirisidir (dizi tamponu, sonek max / min, n'i nMax'tan aşağı tarama ve break, tembel şart sırası, medyan için sıralama, sınıf döngüleri, durum makinesi). Vektörel `s6_taban` ile 5 sentetik (daralma açık / kapalı, AL, KIRILDI, sıçrama) ve 4 gerçek hissede (ENJSA, PAPIL, TUCLK bant 0,20 + daralma 0,8, KNFRT) n, tavan, dip, al, kirildi, bolge_id, kutu ve sınıf birebir aynı.
- test_s6_taban.py sonucu: 50/50 TAMAM (S6_VERI scratchpad verisiyle).

## PINE

- Dosyalar: `COL_S6_TABAN.pine` (Pine v5, v1.0, 423 satır), `COL_S6_TABAN_ascii.pine` (`python S6_TABAN.py ascii`: ASCII dışı karakter 0, yorum / dize dışındaki kod birebir, satır numaraları aynı), `PINE_S6_NASIL.md`.
- Girdi varsayılanları = S6_PRM (test 14 mekanik denetler: 16 alan). Sözdizimi denetimi (test): tab yok, 'by -1' geri sayan döngü yok, plotshape / plot / bgcolor global, //@version=5 + overlay.
- İki gözden geçirme yapıldı (derleyici yok). İkincide düzeltilenler: tablo 11. satırdaki anlamsız iç içe üçlü ifade, AL hacmi na koruması, runtime.error şartlarının Python doğrulamasıyla eşitlenmesi, PAPIL beklenen çıktı yorumundaki yanlış açıklama.
- RİSKLİ SATIRLAR (ilk yapıştırmada bakılacak; satır numaraları Türkçe dosyada, ASCII'de aynı):
  - 60-61 `runtime.error` (global `if barstate.isfirst` içinde; uzun koşul).
  - 170-171 `array.new_float(nMax + 1, na)` (başlangıç değeri na).
  - 182, 211 `int(nn / 2)` (int bölmesi; int() ile aşağı yuvarlanır, iki durumda da doğru).
  - 207-210 döngü içinde her n için yeni dizi + `array.sort` (performans; S5'te benzer kalıp derlendi).
  - 219 `break` (iç içe if içinde; S5 v1.2'de derlendi).
  - 287, 291, 300 `math.max` / `math.min` int argümanla `var int`'e atama.
  - 304, 306 `idxOf` (kullanıcı fonksiyonu int dizi alıp int döndürür).
  - 312 `box.new(..., text=..., text_size=..., text_color=..., text_halign=..., text_valign=...)` (kutu yazısı parametreleri; S5'te kullanılmadı).
  - 323, 327 `box.set_left`, `box.set_text`; 328-329 `line.set_xy1` / `line.set_xy2` (S5'te kullanılmadı).
  - 341 `table.new(..., 2, 15, ...)` (15 satır).
  - 354-355 `na(x) or x == 0 ? na : ...` (üçlü ifade önceliği: koşul bütün 'or' ifadesi).
- Bilinen farklar: likidite süzgeci yok; TradingView verisi (eksik / fazla bar, düzeltme farkı); geçmiş 250 bardan kısa yüklenirse ilk bölgeler farklı; kriz kesiği yok; eşik sınırında toplama sırası farkı (son ondalık).
- BEKLENEN ÇIKTI: dosya sonunda 6 etiket (D7 KNFRT, D8 TUCLK, D10 PAPIL, D5 ENJSA, D6 DESA, Y3 TUCLK) için kutu başlangıç / bitiş / AL günü (`python S6_TABAN.py pine` ile üretildi).

## KONTROL LİSTESİ (K1-K14)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | tasarım / göz aracı; getiri ve eş karşılaştırması yok (ölçüm sonra, ayrı ön kayıtla, eşli taban + 200 rastgele eş portföy ile) |
| K2 | geleceğe bakma | EVET | s6_taban her bar t için yalnız t ve öncesi; test_s6_taban.py önek değişmezliği (d.iloc[:T] ile tam serinin ilk T satırı birebir, al / kirildi / bolge_id dahil) ve t sonrası bozma testi; kutunun sol kenarı (min bas) yalnız çizim / etiket kıyası |
| K3 | geçerli bar | EVET | SY.sy_veri_hazirla: H>L, V>0, C>0, O>0 olmayan bar atılır; bütün pencereler geçerli bar dizisinde; Pine aynı 'gecerli' süzgeci |
| K4 | tekilleştirme | EVET | bölge = durum makinesi bölgesi (bir bölge bir kez sayılır); AL / KIRILDI bölge başına en çok bir kez; evren sayımı bölge açılış yılına göre |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok; AL günü yalnız işaret (ölçüm işinde giriş = AL barından sonraki ilk açılış yazılacak) |
| K6 | veri birimi | EVET | tek kip: V_BIST düzeltilmiş fiyat (TradingView ADJ açık ile aynı); mum ve ATR yüzde; PAPIL tavanı 20,32 veriyle denetlendi |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_BIST 581 hisse): batanlar yok; evren sayımı yukarı / aşağı yanlı olabilir, raporda yazılı |
| K8 | örneklem ve dönem | EVET | 16 etiket küçük örneklem: sonuç 'bulgu' değil, tasarım uyumu; ızgaranın 108 noktası tamamı raporlanır; aşırı uyum riski yazılı |
| K9 | ön kayıt | EVET | ızgara, puan ve sadelik kuralı iş tanımında (commit 2460e39) koşudan önce; S6_IZGARA birebir; eşik değerleri hiç değişmedi. UYARI: tanımda üç düzeltme ilk koşulardan SONRA yapıldı (YANLIŞ kuralının ikinci yarısı, AL kuralının harfe dönmesi, kutu >= nMin); hepsi iş tanımının harfine yaklaştırma, sürüm sürüm sonuçları S6_TASARIM.md 'SÜRÜM KAYDI'nda |
| K10 | ayrıştırma | UYGULANMAZ | metin ayrıştırma yok; etiket tarihleri CEMAL_COL_KURALLARI.md'den elle girildi ve raporda tek tek yazılı |
| K11 | yeniden üretim | EVET | test_s6_taban.py: vektörel s6_taban ile Pine aynası döngü (s6_pine_ayna) 4 gerçek hissede birebir; D8 / D6 örtüşmesi (0,673 / 0,561) ve DESA 2021-12-06 AL (tavan 1,0458, kapanış 1,0743), TUCLK 2025-08-05 tavanı ham OHLC'den bağımsız kodla yeniden üretildi |
| K12 | ifade | EVET | getiri / iz / emare sözü yok; 'tasarım uyumu' ve 'göz aracı' dili; PAPIL büyük taban başarısız kırılım uyarısı yazılı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_s6; yasak dosyalara dokunulmadı (git status); e-posta taraması çıktıda; commit yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## HATA

1. (Yazıcı, düzeltildi) YANLIŞ etiket kuralının ikinci yarısı ('ya da o gün bölge bitmiş olmalı') ilk kodda yoktu; seçim 11 -> 12 puan, seçilen nokta değişti. Ders: etiket kuralı kodlanınca iş tanımındaki cümleyle satır satır eşlenmeli.
2. (Yazıcı, düzeltildi, SAPMA riski) AL / KIRILDI'ya iş tanımında olmayan iki şart eklemiştim ('önceki bar açık bölgede' ve 'kilit': yeni bölge AL barından sonra başlar). A1-A3 0/3 görüldükten sonra harfe dönüldü; 12 -> 13 puan, netMax 0,05 -> 0,03. Ders: yorum gereken yerde iş tanımına ek şart koymadan önce yazılı karar, sonuçtan önce.
3. (Yazıcı, testle bulundu, düzeltildi) Yeni bölge açılırken kırpma `rBas = b` sonra `min(rBas, max(b, sinir+1))` = b kaldığı için kutular üst üste biniyordu ('kutular üst üste binmez' testi yakaladı). Python, ayna ve Pine üçünde düzeltildi.
4. (Yazıcı, düzeltildi) Kırpılmış kutu 1 bara kadar düşebiliyordu (evren sayımında en kısa 1); iş tanımı 'bölge uzunluğu nMin..nMax' diyor: yeni kutu kırpıldıktan sonra en az nMin bar olunca açılıyor. Gerçek veri testine 'her kutu >= nMin' eklendi.
5. (Yazıcı, yazımda düzeltildi) Pine beklenen çıktı yorumunda PAPIL için '10 Ara büyük mumu tavanı 17,16'ya çıkardı' yazmıştım; yanlış: 17,16 = 10 Kas High'ı (pencere geriye uzamıştı). Ham veriyle denetlenip düzeltildi; v2'den sonra PAPIL AL 11 Ara oldu, yorum yeniden yazıldı. Ders: grafik yorumu yazmadan önce ham OHLC ile denetle.
6. (Yazıcı, test kurulumu) Sentetik 'eğimli' ve 'AL' testlerinde beklenti yanlış kurulmuştu (pencere düşüşün sonuna uzanıyor; tavan 470. bardan değil pencereden). Kod değil test düzeltildi; ayna / vektörel sınıf sütunu farkı (ölçülmeyen barlar) da testle bulundu, sınıf yalnız ölçülür barda yazılıyor.
7. (İş tanımı, SAPMA) Süreklilik kuralının harfi (başlangıç ±2 bar) 8 etiket hissesinde 584 üst üste binen kutu çifti üretiyor (aynı tabanda 'sakin' şartı başlangıcı ileri geri oynatıyor; KNFRT Eki 2022'de 3 iç içe kutu). Seçilen: açık bölge taban sürdükçe tek bölge (birleşim) + kutular üst üste binmez; etiket puanı ikisinde de 13. Ana model onayı gerekir.
8. (Etiket / veri, açık) KNFRT etiketi V_BIST fiyatıyla uyuşmuyor görünüyor (aralıkta fiyat ~%80 yükseliyor); D7 ve A1 108 noktanın hiçbirinde tutmuyor. Cemal'in grafiği (bedelsiz / düzeltme?) ile V_BIST yan yana denetlenmeli.
9. (Tasarım bulgusu) Çöl bu tanımla nadir değil: BIST'te hisse başına yılda ~6,9 bölge, ölçülür barların ~%28'i açık bölgede; en yüksek puanlı 10 noktanın hepsi aynı mertebede (6,2-7,2 bölge / hisse-yıl). Ters sınama 'çöl nadir olmalı' beklentisini karşılamıyor; seçim kuralı (etiket puanı) sıklığı cezalandırmıyor.

## ÖNERİLEN DEFTER METNİ (IK_GOREV; ana model işler)

15 Kas 2026 | S6 TABAN (Cemal'in çöl kuralları -> taban algoritması + Pine) | S6_TABAN.py (Python referans, Pine aynası) + test_s6_taban.py 50/50; COL_S6_TABAN.pine v1.0 + ASCII + PINE_S6_NASIL.md | Tasarım sınaması 108 nokta: en yüksek 13/16 (10 nokta); seçilen bant 0,12 · net 0,03 · kM 0,90 · dipTol 0,05 · daralma kapalı. Tutmayan: D7 KNFRT taban, A1 KNFRT al mumu, Y3 TUCLK kayan düşüş (üçü 108 noktanın hiçbirinde tutmuyor). Evren BIST 2016-26: hisse-yıl başına 6,9 bölge, 3,3 AL; açık bar ~%28 (çöl nadir değil). Sapmalar: süreklilik birleşim kuralı (harfi 584 üst üste kutu), AL kuralı sonuç görüldükten sonra harfe döndü. Getiri ölçülmedi; Pine derleyicisiz, TradingView ilk yapıştırma denetimi AÇIK.

IK_HATA önerileri: madde 1, 2, 3, 4, 5 (yazıcı hataları; 2 SAPMA riski), 7 (iş tanımı belirsizliği), 8 (etiket / veri uyuşmazlığı, açık).

## DOKUNULAN DOSYALAR

- Yeni: `S6_TABAN.py`, `test_s6_taban.py`, `arastirma_cikti/sikisma_s6/S6_TASARIM.md`, `arastirma_cikti/sikisma_s6/s6_tasarim.json`, `arastirma_cikti/sikisma_s6/COL_S6_TABAN.pine`, `arastirma_cikti/sikisma_s6/COL_S6_TABAN_ascii.pine`, `arastirma_cikti/sikisma_s6/PINE_S6_NASIL.md`.
- Değişmeyen (yasak listesi): IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, COL_v1.py, takip.py, SIKISMA_OBEK.py, SIKISMA_YENIDEN.py, ORTAK_CETVEL.py, mevcut testler, COL_S5_OBEK*.pine. Commit yok.
- Geçici: scratchpad (v0 json / md kopyası, koşu günlüğü); repoya girmez.
