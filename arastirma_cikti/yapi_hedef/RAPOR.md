# YAPI_HEDEF — RAPOR

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo. Koşu: 2026-11-17 11:01:57 UTC (Y1, Y2, Y3, Y4, Y5). Ön kayıt: 2026-11-17 11:01:36 UTC (git 84490eadee).

## 1. ÖZET (etiket önceden yazılı kuralla)

| Deneme | yön | ETİKET | karar hücreleri (ABD 2023 · ABD 2024-26 · AVR 2023 · AVR 2024-26) |
|---|---|---|---|
| Y1 S6 TABAN AL | + | **ÖLÇÜLEMEDİ** | DESTEKLENMEDİ (n 2040, KAT5 0,98) · DESTEKLENMEDİ (n 4083, KAT5 1,01) · ÖLÇÜLEMEDİ (n 815, KAT5 0,99) · DESTEKLENMEDİ (n 1711, KAT5 0,94) |
| Y2 S+ v2 TAM_DIP | + | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ (n 45, KAT5 0,98) · ÖLÇÜLEMEDİ (n 207, KAT5 1,03) · ÖLÇÜLEMEDİ (n 34, KAT5 1,43) · ÖLÇÜLEMEDİ (n 133, KAT5 1,13) |
| Y3 KAZAN + DÖNÜŞ | + | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ (n 939, KAT5 1,14) · DESTEKLENMEDİ (n 1983, KAT5 1,07) · ÖLÇÜLEMEDİ (n 190, KAT5 1,29) · ÖLÇÜLEMEDİ (n 470, KAT5 1,15) |
| Y4 Y1 + KAĞIT HAFIZASI | + | **ÖLÇÜLEMEDİ** | DESTEKLENMEDİ (n 1549, KAT5 0,96) · DESTEKLENMEDİ (n 3248, KAT5 1,00) · ÖLÇÜLEMEDİ (n 665, KAT5 0,93) · DESTEKLENMEDİ (n 1348, KAT5 0,87) |
| Y5 DÜZ TAVAN SAT | - | **ÖLÇÜLEMEDİ** | ÖLÇÜLEMEDİ (n 280, KAT5 1,13) · ÖLÇÜLEMEDİ (n 934, KAT5 1,11) · ÖLÇÜLEMEDİ (n 86, KAT5 1,28) · ÖLÇÜLEMEDİ (n 267, KAT5 1,07) |

Karar kuralı: hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar). Durum: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.

## 2. TANIM

- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].

- **Y1 S6 TABAN AL**: S6_TABAN.s6_taban (SY.sy_veri_hazirla girdisi) 'al' günleri (AL ve AL_BOLGESIZ) = taban kırılım mumu (C_t > TAVAN(t-1)); hat = bölge dibi: durum AL ise kutu_alt (açık bölgenin as-of t alt kenarı), AL_BOLGESIZ ise DİP(t-1) (bir önceki barın taban penceresinin en düşük Low'u).
- **Y2 S+ v2 TAM_DIP**: arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz (sembol, pazar, tarih) olayları; hat = FITIL_V2.fv_olcu HAT (t dahil son 10 geçerli barın en düşük Low'u; yeniden hesaplanır); giriş dosyadaki 'giris' ile aynı olmalı (sayım).
- **Y3 KAZAN + DÖNÜŞ**: t için pencere W = [t-n, t-1] (n geçerli bar, t hariç), n = 20..60: (a) Low serisine 2. derece en küçük kareler uyumunun x^2 katsayısı a > 0; (b) sağ kenar dibi min L(son 5 bar of W) > orta üçte bir dibi min L(W[n//3 : 2n//3]) x 1,03; (c) son kapanış C_{t-1} > dip + (tavan - dip) / 2, dip = min L(W), tavan = max H(W); (d) kırılım C_t > tavan. (a)-(d) tutan EN BÜYÜK n seçilir; hat = dip(W). Bağlam: C_t <= max(C, t dahil son 120 geçerli bar) x 0,85.
- **Y4 Y1 + KAĞIT HAFIZASI**: Y1 olayı t, hafıza = (son 250 barda [t-250, t-1] AL ile biten S6 bölgelerinden (durum AL; a + 15 <= t, sonucu t'de bilinen) a+1 .. a+15 kapanışlarından biri >= açılış(a+1) x 1,05 olanlar) - (son 250 barda KIRILDI ile biten bölgeler); hafıza >= 0 -> Y4 (yalnız geçmiş, t'ye kadar).
- **Y5 DÜZ TAVAN SAT**: TAVAN(t-1): pencere W = [t-n, t-1], n = 8..70: bant max H / min L - 1 <= 0,12; net |C_{t-1} / C_{t-n} - 1| <= 0,03; yüksekler düz (S6 dip savunmasının aynası): max H(ikinci yarı) <= max H(ilk yarı, n//2 bar) x 1,05; önceki yükseliş: C_{t-n-1} / min C(son 60 bar, t-n-1 dahil) - 1 >= 0,20; tutan EN BÜYÜK n. Konum: (C_{t-1} - min C120) / (max C120 - min C120) >= 0,75 (t-1 dahil 120 geçerli kapanış). SAT_t = C_t < min L(W) x 0,98. stop0 = max H(W) x 1,02; hedef -%5 / -%10 (yön -).

## 3. OLAY SAYIMI

| Deneme | Pazar | girdi | havuz dışı | tekil | giriş stop ötesi | 15 bar yok | eş < 3 | plasebo yok | geleceğe bakma denetimi |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | ABD | 37969 | 5214 | 17869 | 13 | 63 | 0 | 0 | 5 TUTTU |
| Y1 | AVR | 18783 | 2969 | 8750 | 3 | 32 | 0 | 0 | 5 TUTTU |
| Y1 | BIST | 10242 | 2460 | 3051 | 0 | 44 | 0 | 0 | 5 TUTTU |
| Y2 | ABD | 542 | 0 | 0 | 11 | 4 | 0 | 0 | 5 TUTTU |
| Y2 | AVR | 326 | 0 | 0 | 2 | 1 | 0 | 1 | 5 TUTTU |
| Y2 | BIST | 880 | 0 | 0 | 9 | 32 | 0 | 0 | 5 TUTTU |
| Y3 | ABD | 30010 | 8250 | 14517 | 5 | 55 | 0 | 70 | 5 TUTTU |
| Y3 | AVR | 7632 | 1214 | 4136 | 0 | 6 | 0 | 78 | 5 TUTTU |
| Y3 | BIST | 9560 | 2142 | 4550 | 0 | 34 | 0 | 7 | 5 TUTTU |
| Y4 | ABD | 30855 | 4002 | 14697 | 7 | 58 | 0 | 0 | 5 TUTTU |
| Y4 | AVR | 16034 | 2552 | 7522 | 3 | 25 | 0 | 0 | 5 TUTTU |
| Y4 | BIST | 7807 | 1873 | 2274 | 0 | 33 | 0 | 0 | 5 TUTTU |
| Y5 | ABD | 3615 | 492 | 255 | 1 | 12 | 0 | 12 | 5 TUTTU |
| Y5 | AVR | 1066 | 149 | 58 | 0 | 7 | 0 | 25 | 5 TUTTU |
| Y5 | BIST | 1182 | 147 | 61 | 0 | 4 | 0 | 14 | 5 TUTTU |

## 4. HÜCRE TABLOSU (karar sütunu kapanış; KAT = olay / eş, ay kümeli %95)

| Deneme | Hücre | n | P(+5) olay / eş | KAT5 [%95] | P(stop önce) olay / eş | plasebo P(+5) | plasebo KAT5 [%95] | şartlar n·kat·stop·plasebo | güç | DURUM |
|---|---|---|---|---|---|---|---|---|---|---|
| Y1 | ABD 2016-22 | 8682 | %34,5 / %35,8 | 0,97 [0,93, 1,01] | %25,5 / %25,4 | %39,0 | 0,88 [0,81, 0,97] | ✓··· | %100 | DESTEKLENMEDİ |
| Y1 | ABD 2023 (karar) | 2040 | %39,0 / %40,0 | 0,98 [0,91, 1,03] | %28,2 / %27,6 | %42,9 | 0,91 [0,70, 1,11] | ✓··· | %97 | DESTEKLENMEDİ |
| Y1 | ABD 2024-26 (karar) | 4083 | %42,6 / %42,2 | 1,01 [0,98, 1,05] | %27,1 / %28,4 | %44,6 | 0,96 [0,88, 1,02] | ✓·✓· | %100 | DESTEKLENMEDİ |
| Y1 | AVR 2016-22 | 4493 | %29,6 / %29,1 | 1,02 [0,97, 1,08] | %19,4 / %19,7 | %34,7 | 0,85 [0,78, 0,93] | ✓·✓· | %100 | DESTEKLENMEDİ |
| Y1 | AVR 2023 (karar) | 815 | %29,7 / %30,1 | 0,99 [0,89, 1,11] | %22,3 / %21,0 | %35,2 | 0,84 [0,60, 1,13] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y1 | AVR 2024-26 (karar) | 1711 | %29,6 / %31,4 | 0,94 [0,87, 1,01] | %19,5 / %19,5 | %34,2 | 0,86 [0,75, 0,97] | ✓··· | %97 | DESTEKLENMEDİ |
| Y1 | BIST 2016-22 | 2588 | %50,4 / %51,7 | 0,98 [0,94, 1,02] | %28,3 / %26,3 | %50,7 | 0,99 [0,90, 1,10] | ✓··· | %97 | DESTEKLENMEDİ |
| Y1 | BIST 2023 | 381 | %53,0 / %54,2 | 0,98 [0,90, 1,03] | %44,1 / %42,1 | %53,8 | 0,99 [0,65, 1,31] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y1 | BIST 2024-26 | 1715 | %51,3 / %52,0 | 0,99 [0,93, 1,04] | %35,3 / %35,0 | %51,4 | 1,00 [0,83, 1,18] | ✓··· | %97 | DESTEKLENMEDİ |
| Y2 | ABD 2016-22 | 275 | %39,3 / %42,5 | 0,92 [0,83, 1,03] | %50,2 / %45,2 | %39,6 | 0,99 [0,81, 1,20] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | ABD 2023 (karar) | 45 | %46,7 / %47,7 | 0,98 [0,77, 1,39] | %44,4 / %40,0 | %40,0 | 1,17 [0,79, 2,50] | ✓··· | %2 | ÖLÇÜLEMEDİ |
| Y2 | ABD 2024-26 (karar) | 207 | %43,5 / %42,4 | 1,03 [0,85, 1,21] | %48,8 / %45,6 | %45,9 | 0,95 [0,77, 1,14] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | AVR 2016-22 | 155 | %33,5 / %37,3 | 0,90 [0,76, 1,06] | %54,2 / %46,8 | %38,7 | 0,87 [0,62, 1,18] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | AVR 2023 (karar) | 34 | %58,8 / %41,0 | 1,43 [0,84, 2,25] | %35,3 / %40,8 | %26,5 | 2,22 [1,50, 4,50] | ✓·✓✓ | %2 | ÖLÇÜLEMEDİ |
| Y2 | AVR 2024-26 (karar) | 133 | %36,1 / %32,0 | 1,13 [0,89, 1,36] | %46,6 / %45,0 | %36,1 | 1,00 [0,75, 1,29] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | BIST 2016-22 | 292 | %42,1 / %42,9 | 0,98 [0,83, 1,09] | %45,9 / %42,0 | %43,2 | 0,98 [0,72, 1,24] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | BIST 2023 | 101 | %28,7 / %34,4 | 0,83 [0,55, 1,07] | %69,3 / %62,8 | %41,6 | 0,69 [0,30, 1,33] | ✓··· | %11 | ÖLÇÜLEMEDİ |
| Y2 | BIST 2024-26 | 446 | %38,3 / %40,2 | 0,95 [0,85, 1,05] | %52,0 / %51,7 | %45,7 | 0,84 [0,67, 1,07] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y3 | ABD 2016-22 | 4186 | %48,3 / %46,2 | 1,05 [1,00, 1,10] | %37,4 / %31,5 | %44,8 | 1,08 [0,94, 1,21] | ✓✓·· | %100 | DESTEKLENMEDİ |
| Y3 | ABD 2023 (karar) | 939 | %55,2 / %48,2 | 1,14 [1,02, 1,21] | %29,7 / %24,2 | %46,1 | 1,20 [0,86, 1,41] | ✓✓·· | %57 | ÖLÇÜLEMEDİ |
| Y3 | ABD 2024-26 (karar) | 1983 | %47,7 / %44,7 | 1,07 [1,02, 1,12] | %39,0 / %32,0 | %49,0 | 0,97 [0,87, 1,06] | ✓✓·· | %97 | DESTEKLENMEDİ |
| Y3 | AVR 2016-22 | 1537 | %44,4 / %41,9 | 1,06 [0,99, 1,15] | %32,5 / %24,7 | %37,0 | 1,20 [0,97, 1,40] | ✓··· | %97 | DESTEKLENMEDİ |
| Y3 | AVR 2023 (karar) | 190 | %42,6 / %33,1 | 1,29 [1,13, 1,66] | %26,8 / %20,0 | %38,4 | 1,11 [0,79, 1,34] | ✓✓·· | %11 | ÖLÇÜLEMEDİ |
| Y3 | AVR 2024-26 (karar) | 470 | %42,1 / %36,7 | 1,15 [1,02, 1,33] | %31,7 / %21,7 | %41,1 | 1,03 [0,83, 1,24] | ✓✓·· | %57 | ÖLÇÜLEMEDİ |
| Y3 | BIST 2016-22 | 1348 | %50,1 / %52,0 | 0,97 [0,91, 1,02] | %32,3 / %26,3 | %50,4 | 1,00 [0,85, 1,13] | ✓··· | %97 | DESTEKLENMEDİ |
| Y3 | BIST 2023 | 432 | %50,9 / %57,4 | 0,89 [0,75, 0,97] | %45,6 / %39,2 | %54,9 | 0,93 [0,45, 1,31] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y3 | BIST 2024-26 | 1044 | %57,5 / %57,4 | 1,00 [0,96, 1,07] | %31,6 / %29,0 | %50,2 | 1,15 [0,89, 1,34] | ✓··· | %97 | DESTEKLENMEDİ |
| Y4 | ABD 2016-22 | 7291 | %33,5 / %35,4 | 0,95 [0,91, 0,99] | %24,5 / %25,3 | %38,3 | 0,88 [0,79, 0,96] | ✓·✓· | %100 | DESTEKLENMEDİ |
| Y4 | ABD 2023 (karar) | 1549 | %38,0 / %39,7 | 0,96 [0,88, 1,03] | %27,1 / %27,6 | %41,8 | 0,91 [0,68, 1,19] | ✓·✓· | %97 | DESTEKLENMEDİ |
| Y4 | ABD 2024-26 (karar) | 3248 | %42,2 / %42,1 | 1,00 [0,97, 1,04] | %26,6 / %28,5 | %42,3 | 1,00 [0,92, 1,07] | ✓·✓· | %100 | DESTEKLENMEDİ |
| Y4 | AVR 2016-22 | 3910 | %28,8 / %28,7 | 1,00 [0,95, 1,06] | %18,9 / %19,5 | %34,5 | 0,83 [0,76, 0,91] | ✓·✓· | %100 | DESTEKLENMEDİ |
| Y4 | AVR 2023 (karar) | 665 | %28,1 / %30,1 | 0,93 [0,83, 1,10] | %20,9 / %20,8 | %37,3 | 0,75 [0,55, 0,97] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y4 | AVR 2024-26 (karar) | 1348 | %27,1 / %31,2 | 0,87 [0,78, 0,95] | %18,5 / %19,2 | %34,7 | 0,78 [0,66, 0,91] | ✓·✓· | %97 | DESTEKLENMEDİ |
| Y4 | BIST 2016-22 | 1994 | %50,7 / %52,0 | 0,97 [0,93, 1,02] | %29,1 / %26,7 | %50,2 | 1,01 [0,91, 1,11] | ✓··· | %97 | DESTEKLENMEDİ |
| Y4 | BIST 2023 | 316 | %52,2 / %53,3 | 0,98 [0,90, 1,03] | %44,9 / %43,3 | %55,1 | 0,95 [0,67, 1,21] | ✓··· | %57 | ÖLÇÜLEMEDİ |
| Y4 | BIST 2024-26 | 1315 | %51,1 / %51,8 | 0,99 [0,92, 1,06] | %35,1 / %35,5 | %51,9 | 0,98 [0,82, 1,16] | ✓·✓· | %97 | DESTEKLENMEDİ |
| Y5 | ABD 2016-22 | 1627 | %39,8 / %33,4 | 1,19 [1,10, 1,30] | %37,9 / %33,9 | %39,1 | 1,02 [0,90, 1,16] | ✓✓·· | %96 | DESTEKLENMEDİ |
| Y5 | ABD 2023 (karar) | 280 | %46,1 / %40,6 | 1,13 [0,94, 1,35] | %35,0 / %31,4 | %37,9 | 1,22 [0,94, 1,40] | ✓··· | %10 | ÖLÇÜLEMEDİ |
| Y5 | ABD 2024-26 (karar) | 934 | %39,7 / %35,9 | 1,11 [1,00, 1,21] | %39,4 / %34,6 | %38,1 | 1,04 [0,89, 1,21] | ✓✓·· | %52 | ÖLÇÜLEMEDİ |
| Y5 | AVR 2016-22 | 473 | %32,6 / %28,0 | 1,16 [1,03, 1,33] | %35,1 / %27,1 | %33,6 | 0,97 [0,75, 1,21] | ✓✓·· | %52 | ÖLÇÜLEMEDİ |
| Y5 | AVR 2023 (karar) | 86 | %43,0 / %33,7 | 1,28 [0,89, 1,47] | %27,9 / %23,8 | %34,9 | 1,23 [0,70, 1,55] | ✓··· | %2 | ÖLÇÜLEMEDİ |
| Y5 | AVR 2024-26 (karar) | 267 | %33,7 / %31,5 | 1,07 [0,91, 1,20] | %35,2 / %28,8 | %31,5 | 1,07 [0,72, 1,49] | ✓··· | %10 | ÖLÇÜLEMEDİ |
| Y5 | BIST 2016-22 | 591 | %45,0 / %40,0 | 1,12 [1,03, 1,23] | %44,2 / %46,9 | %37,7 | 1,19 [0,96, 1,45] | ✓✓✓· | %52 | ÖLÇÜLEMEDİ |
| Y5 | BIST 2023 | 105 | %48,6 / %54,9 | 0,89 [0,57, 1,06] | %48,6 / %42,7 | %48,6 | 1,00 [0,41, 1,60] | ✓··· | %10 | ÖLÇÜLEMEDİ |
| Y5 | BIST 2024-26 | 257 | %55,6 / %49,7 | 1,12 [1,01, 1,24] | %37,0 / %43,2 | %42,4 | 1,31 [1,07, 1,58] | ✓✓✓✓ | %10 | TUTAR |

## 5. OLASILIK TABLOSU (Cemal'in biçimi: olay / eş / taban; KAT = olay / eş [%95])

| Deneme | Hücre | n | P(+5 önce) olay / eş / taban | KAT | P(+10 önce) olay / eş / taban | KAT | P(stop önce) olay / eş / taban | KAT |
|---|---|---|---|---|---|---|---|---|
| Y1 | ABD 2016-22 | 8682 | %34,5 / %35,8 / %36,5 | 0,97 [0,93, 1,01] | %12,3 / %13,4 / %13,9 | 0,92 [0,85, 1,00] | %25,5 / %25,4 / %26,1 | 1,00 [0,95, 1,05] |
| Y1 | ABD 2023 | 2040 | %39,0 / %40,0 / %41,0 | 0,98 [0,91, 1,03] | %15,7 / %16,8 / %17,9 | 0,93 [0,82, 1,02] | %28,2 / %27,6 / %27,7 | 1,02 [0,95, 1,10] |
| Y1 | ABD 2024-26 | 4083 | %42,6 / %42,2 / %42,5 | 1,01 [0,98, 1,05] | %16,7 / %18,4 / %18,7 | 0,90 [0,85, 0,96] | %27,1 / %28,4 / %29,1 | 0,95 [0,91, 1,00] |
| Y1 | AVR 2016-22 | 4493 | %29,6 / %29,1 / %29,6 | 1,02 [0,97, 1,08] | %9,1 / %7,9 / %8,3 | 1,16 [1,04, 1,30] | %19,4 / %19,7 / %20,0 | 0,99 [0,93, 1,05] |
| Y1 | AVR 2023 | 815 | %29,7 / %30,1 / %29,6 | 0,99 [0,89, 1,11] | %8,6 / %9,0 / %8,9 | 0,96 [0,75, 1,15] | %22,3 / %21,0 / %21,2 | 1,07 [0,96, 1,20] |
| Y1 | AVR 2024-26 | 1711 | %29,6 / %31,4 / %31,8 | 0,94 [0,87, 1,01] | %8,1 / %9,5 / %9,9 | 0,85 [0,73, 0,99] | %19,5 / %19,5 / %20,1 | 1,00 [0,93, 1,07] |
| Y1 | BIST 2016-22 | 2588 | %50,4 / %51,7 / %51,6 | 0,98 [0,94, 1,02] | %30,8 / %30,5 / %30,3 | 1,01 [0,95, 1,07] | %28,3 / %26,3 / %26,9 | 1,07 [1,01, 1,14] |
| Y1 | BIST 2023 | 381 | %53,0 / %54,2 / %54,8 | 0,98 [0,90, 1,03] | %36,5 / %36,3 / %36,2 | 1,01 [0,90, 1,07] | %44,1 / %42,1 / %41,7 | 1,05 [0,98, 1,11] |
| Y1 | BIST 2024-26 | 1715 | %51,3 / %52,0 / %51,8 | 0,99 [0,93, 1,04] | %27,8 / %29,1 / %29,4 | 0,96 [0,88, 1,03] | %35,3 / %35,0 / %35,5 | 1,01 [0,93, 1,07] |
| Y2 | ABD 2016-22 | 275 | %39,3 / %42,5 / %36,8 | 0,92 [0,83, 1,03] | %17,1 / %19,8 / %14,7 | 0,86 [0,67, 1,04] | %50,2 / %45,2 / %43,6 | 1,11 [1,01, 1,23] |
| Y2 | ABD 2023 | 45 | %46,7 / %47,7 / %44,0 | 0,98 [0,77, 1,39] | %28,9 / %26,8 / %21,1 | 1,08 [0,76, 1,52] | %44,4 / %40,0 / %38,4 | 1,11 [0,88, 1,34] |
| Y2 | ABD 2024-26 | 207 | %43,5 / %42,4 / %39,6 | 1,03 [0,85, 1,21] | %24,6 / %20,8 / %18,0 | 1,19 [0,91, 1,49] | %48,8 / %45,6 / %41,2 | 1,07 [0,91, 1,22] |
| Y2 | AVR 2016-22 | 155 | %33,5 / %37,3 / %34,5 | 0,90 [0,76, 1,06] | %14,2 / %16,9 / %12,5 | 0,84 [0,59, 1,07] | %54,2 / %46,8 / %40,9 | 1,16 [1,01, 1,35] |
| Y2 | AVR 2023 | 34 | %58,8 / %41,0 / %34,2 | 1,43 [0,84, 2,25] | %23,5 / %16,5 / %10,7 | 1,42 [0,47, 2,70] | %35,3 / %40,8 / %35,9 | 0,86 [0,54, 1,34] |
| Y2 | AVR 2024-26 | 133 | %36,1 / %32,0 / %30,0 | 1,13 [0,89, 1,36] | %18,0 / %11,2 / %9,4 | 1,62 [1,10, 2,13] | %46,6 / %45,0 / %39,0 | 1,04 [0,89, 1,21] |
| Y2 | BIST 2016-22 | 292 | %42,1 / %42,9 / %43,1 | 0,98 [0,83, 1,09] | %23,3 / %23,1 / %23,9 | 1,01 [0,79, 1,19] | %45,9 / %42,0 / %41,7 | 1,09 [0,99, 1,23] |
| Y2 | BIST 2023 | 101 | %28,7 / %34,4 / %36,6 | 0,83 [0,55, 1,07] | %20,8 / %23,3 / %25,2 | 0,89 [0,27, 1,20] | %69,3 / %62,8 / %61,1 | 1,10 [1,04, 1,32] |
| Y2 | BIST 2024-26 | 446 | %38,3 / %40,2 / %42,2 | 0,95 [0,85, 1,05] | %17,7 / %20,9 / %23,5 | 0,85 [0,70, 1,01] | %52,0 / %51,7 / %50,7 | 1,01 [0,91, 1,09] |
| Y3 | ABD 2016-22 | 4186 | %48,3 / %46,2 / %44,4 | 1,05 [1,00, 1,10] | %23,9 / %20,9 / %19,2 | 1,15 [1,06, 1,27] | %37,4 / %31,5 / %29,3 | 1,19 [1,14, 1,25] |
| Y3 | ABD 2023 | 939 | %55,2 / %48,2 / %46,0 | 1,14 [1,02, 1,21] | %31,8 / %22,8 / %20,4 | 1,39 [1,23, 1,51] | %29,7 / %24,2 / %23,1 | 1,23 [1,12, 1,35] |
| Y3 | ABD 2024-26 | 1983 | %47,7 / %44,7 / %43,8 | 1,07 [1,02, 1,12] | %25,6 / %21,4 / %20,5 | 1,20 [1,08, 1,35] | %39,0 / %32,0 / %29,7 | 1,22 [1,15, 1,31] |
| Y3 | AVR 2016-22 | 1537 | %44,4 / %41,9 / %39,4 | 1,06 [0,99, 1,15] | %18,2 / %15,9 / %14,0 | 1,14 [1,01, 1,35] | %32,5 / %24,7 / %23,4 | 1,31 [1,21, 1,45] |
| Y3 | AVR 2023 | 190 | %42,6 / %33,1 / %32,2 | 1,29 [1,13, 1,66] | %18,9 / %10,3 / %9,1 | 1,85 [1,35, 2,89] | %26,8 / %20,0 / %18,3 | 1,34 [1,03, 1,70] |
| Y3 | AVR 2024-26 | 470 | %42,1 / %36,7 / %35,5 | 1,15 [1,02, 1,33] | %17,9 / %12,2 / %11,3 | 1,46 [1,21, 1,75] | %31,7 / %21,7 / %19,2 | 1,46 [1,25, 1,70] |
| Y3 | BIST 2016-22 | 1348 | %50,1 / %52,0 / %52,4 | 0,97 [0,91, 1,02] | %28,7 / %29,7 / %30,5 | 0,97 [0,89, 1,10] | %32,3 / %26,3 / %27,3 | 1,23 [1,11, 1,39] |
| Y3 | BIST 2023 | 432 | %50,9 / %57,4 / %57,3 | 0,89 [0,75, 0,97] | %29,4 / %36,3 / %37,0 | 0,81 [0,75, 0,97] | %45,6 / %39,2 / %39,7 | 1,16 [1,05, 1,37] |
| Y3 | BIST 2024-26 | 1044 | %57,5 / %57,4 / %57,7 | 1,00 [0,96, 1,07] | %32,6 / %34,0 / %35,0 | 0,96 [0,90, 1,08] | %31,6 / %29,0 / %29,7 | 1,09 [0,98, 1,22] |
| Y4 | ABD 2016-22 | 7291 | %33,5 / %35,4 / %36,5 | 0,95 [0,91, 0,99] | %11,6 / %13,1 / %13,9 | 0,89 [0,82, 0,97] | %24,5 / %25,3 / %26,0 | 0,97 [0,92, 1,02] |
| Y4 | ABD 2023 | 1549 | %38,0 / %39,7 / %41,1 | 0,96 [0,88, 1,03] | %14,6 / %16,4 / %17,9 | 0,89 [0,79, 0,96] | %27,1 / %27,6 / %27,8 | 0,98 [0,91, 1,05] |
| Y4 | ABD 2024-26 | 3248 | %42,2 / %42,1 / %42,5 | 1,00 [0,97, 1,04] | %16,6 / %18,5 / %18,8 | 0,90 [0,83, 0,96] | %26,6 / %28,5 / %29,4 | 0,93 [0,87, 0,99] |
| Y4 | AVR 2016-22 | 3910 | %28,8 / %28,7 / %29,3 | 1,00 [0,95, 1,06] | %8,4 / %7,7 / %8,2 | 1,08 [0,96, 1,22] | %18,9 / %19,5 / %19,8 | 0,97 [0,91, 1,04] |
| Y4 | AVR 2023 | 665 | %28,1 / %30,1 / %29,7 | 0,93 [0,83, 1,10] | %7,2 / %8,8 / %8,8 | 0,82 [0,68, 1,06] | %20,9 / %20,8 / %21,2 | 1,00 [0,85, 1,20] |
| Y4 | AVR 2024-26 | 1348 | %27,1 / %31,2 / %31,6 | 0,87 [0,78, 0,95] | %7,2 / %9,3 / %9,8 | 0,77 [0,63, 0,93] | %18,5 / %19,2 / %20,0 | 0,96 [0,88, 1,04] |
| Y4 | BIST 2016-22 | 1994 | %50,7 / %52,0 / %51,5 | 0,97 [0,93, 1,02] | %31,2 / %30,9 / %30,5 | 1,01 [0,95, 1,08] | %29,1 / %26,7 / %27,4 | 1,09 [1,01, 1,17] |
| Y4 | BIST 2023 | 316 | %52,2 / %53,3 / %53,9 | 0,98 [0,90, 1,03] | %35,8 / %35,8 / %35,4 | 1,00 [0,91, 1,10] | %44,9 / %43,3 / %42,7 | 1,04 [0,96, 1,11] |
| Y4 | BIST 2024-26 | 1315 | %51,1 / %51,8 / %51,3 | 0,99 [0,92, 1,06] | %28,4 / %28,8 / %29,1 | 0,98 [0,90, 1,07] | %35,1 / %35,5 / %36,0 | 0,99 [0,92, 1,05] |
| Y5 | ABD 2016-22 | 1627 | %39,8 / %33,4 / %34,4 | 1,19 [1,10, 1,30] | %16,3 / %13,3 / %14,0 | 1,23 [1,07, 1,41] | %37,9 / %33,9 / %33,6 | 1,12 [1,05, 1,19] |
| Y5 | ABD 2023 | 280 | %46,1 / %40,6 / %41,4 | 1,13 [0,94, 1,35] | %16,1 / %15,5 / %16,5 | 1,04 [0,69, 1,37] | %35,0 / %31,4 / %31,0 | 1,11 [0,87, 1,36] |
| Y5 | ABD 2024-26 | 934 | %39,7 / %35,9 / %36,4 | 1,11 [1,00, 1,21] | %15,7 / %14,9 / %15,0 | 1,06 [0,83, 1,26] | %39,4 / %34,6 / %35,7 | 1,14 [1,05, 1,22] |
| Y5 | AVR 2016-22 | 473 | %32,6 / %28,0 / %29,5 | 1,16 [1,03, 1,33] | %14,0 / %9,6 / %10,3 | 1,46 [1,10, 1,99] | %35,1 / %27,1 / %26,9 | 1,30 [1,11, 1,50] |
| Y5 | AVR 2023 | 86 | %43,0 / %33,7 / %33,3 | 1,28 [0,89, 1,47] | %16,3 / %9,0 / %9,5 | 1,80 [0,94, 3,25] | %27,9 / %23,8 / %24,5 | 1,17 [0,67, 2,49] |
| Y5 | AVR 2024-26 | 267 | %33,7 / %31,5 / %31,7 | 1,07 [0,91, 1,20] | %11,6 / %10,6 / %10,8 | 1,09 [0,73, 1,36] | %35,2 / %28,8 / %28,4 | 1,22 [1,04, 1,49] |
| Y5 | BIST 2016-22 | 591 | %45,0 / %40,0 / %38,4 | 1,12 [1,03, 1,23] | %21,3 / %18,7 / %18,1 | 1,14 [0,99, 1,32] | %44,2 / %46,9 / %46,6 | 0,94 [0,86, 1,02] |
| Y5 | BIST 2023 | 105 | %48,6 / %54,9 / %55,5 | 0,89 [0,57, 1,06] | %29,5 / %33,2 / %33,2 | 0,89 [0,36, 1,16] | %48,6 / %42,7 / %41,9 | 1,14 [0,92, 1,35] |
| Y5 | BIST 2024-26 | 257 | %55,6 / %49,7 / %48,9 | 1,12 [1,01, 1,24] | %28,4 / %24,9 / %22,3 | 1,14 [0,95, 1,39] | %37,0 / %43,2 / %41,3 | 0,86 [0,72, 0,99] |

## 6. BİLGİ: High ile hedef, iki yarı, takip stoplu getiri, çıkış

| Deneme | Hücre | KAT5 High [%95] | KAT10 High | KAT5 yarı 1 / yarı 2 | getiri ort / medyan | kazanan | çıkış barı ort / med | çıkış türü | d medyan |
|---|---|---|---|---|---|---|---|---|---|
| Y1 | ABD 2016-22 | 0,98 [0,95, 1,02] | 0,92 | 0,98 / 0,95 | %0,5 / %-0,2 | %49 | 26,2 / 21 | stop 7238, ters 288, zaman 1156 | %11,9 |
| Y1 | ABD 2023 | 0,96 [0,90, 1,02] | 0,93 | 1,04 / 0,91 | %0,6 / %-0,5 | %48 | 23,2 / 18 | stop 1802, ters 40, zaman 198 | %12,5 |
| Y1 | ABD 2024-26 | 1,00 [0,97, 1,03] | 0,91 | 0,99 / 1,03 | %0,9 / %-0,3 | %49 | 22,1 / 17 | kesik 52, stop 3659, stop_kesik 9, ters 80, zaman 283 | %12,1 |
| Y1 | AVR 2016-22 | 1,01 [0,96, 1,06] | 1,10 | 1,00 / 1,03 | %0,7 / %0,2 | %51 | 30,8 / 27 | stop 3481, ters 161, zaman 851 | %11,3 |
| Y1 | AVR 2023 | 0,98 [0,90, 1,08] | 1,00 | 0,94 / 1,04 | %-0,4 / %-1,5 | %45 | 27,4 / 23 | stop 695, ters 28, zaman 92 | %12,1 |
| Y1 | AVR 2024-26 | 1,00 [0,94, 1,05] | 0,90 | 0,98 / 0,90 | %0,6 / %-0,3 | %49 | 28,8 / 24 | kesik 63, stop 1342, ters 50, zaman 256 | %11,4 |
| Y1 | BIST 2016-22 | 1,00 [0,98, 1,04] | 0,99 | 0,97 / 0,98 | %4,6 / %0,9 | %53 | 18,3 / 14 | stop 2473, ters 23, zaman 92 | %13,4 |
| Y1 | BIST 2023 | 1,04 [0,98, 1,13] | 1,00 | 1,00 / 0,96 | %3,3 / %-1,7 | %46 | 11,9 / 9 | stop 376, zaman 5 | %13,8 |
| Y1 | BIST 2024-26 | 1,00 [0,97, 1,03] | 0,98 | 1,00 / 0,97 | %1,7 / %-0,1 | %49 | 14,4 / 11 | kesik 12, stop 1686, stop_kesik 2, ters 3, zaman 12 | %13,3 |
| Y2 | ABD 2016-22 | 1,02 [0,92, 1,13] | 0,89 | 0,96 / 0,89 | %0,1 / %-2,5 | %36 | 12,0 / 7 | stop 268, ters 1, zaman 6 | %5,4 |
| Y2 | ABD 2023 | 1,14 [0,88, 1,33] | 1,17 | 1,18 / 0,87 | %5,8 / %-0,1 | %47 | 19,8 / 9 | stop 40, zaman 5 | %4,6 |
| Y2 | ABD 2024-26 | 0,98 [0,83, 1,15] | 1,10 | 1,18 / 0,90 | %0,1 / %-2,6 | %40 | 10,8 / 7 | kesik 1, stop 205, zaman 1 | %5,1 |
| Y2 | AVR 2016-22 | 0,90 [0,76, 1,05] | 0,86 | 0,86 / 0,96 | %-0,9 / %-2,8 | %34 | 13,5 / 8 | stop 153, zaman 2 | %4,9 |
| Y2 | AVR 2023 | 1,28 [0,96, 1,77] | 1,37 | 1,85 / 1,07 | %2,1 / %1,2 | %59 | 13,7 / 11 | stop 34 | %4,2 |
| Y2 | AVR 2024-26 | 1,13 [0,92, 1,33] | 1,29 | 1,25 / 1,01 | %-0,2 / %-2,4 | %37 | 15,7 / 10 | stop 126, zaman 7 | %3,7 |
| Y2 | BIST 2016-22 | 1,01 [0,90, 1,10] | 1,05 | 1,08 / 0,91 | %1,2 / %-2,6 | %42 | 14,4 / 11 | stop 287, ters 1, zaman 4 | %5,3 |
| Y2 | BIST 2023 | 0,91 [0,77, 0,96] | 0,89 | 0,90 / 0,81 | %1,0 / %-3,8 | %28 | 8,0 / 5 | stop 101 | %4,4 |
| Y2 | BIST 2024-26 | 0,98 [0,91, 1,05] | 0,99 | 0,96 / 0,95 | %1,1 / %-2,8 | %37 | 10,8 / 8 | kesik 1, stop 441, ters 1, zaman 3 | %4,2 |
| Y3 | ABD 2016-22 | 1,06 [1,02, 1,11] | 1,16 | 1,03 / 1,06 | %-0,4 / %-1,8 | %44 | 15,3 / 11 | stop 4012, ters 34, zaman 140 | %20,7 |
| Y3 | ABD 2023 | 1,15 [1,06, 1,20] | 1,35 | 1,09 / 1,19 | %2,9 / %0,8 | %54 | 17,8 / 13 | stop 902, ters 4, zaman 33 | %19,8 |
| Y3 | ABD 2024-26 | 1,09 [1,04, 1,16] | 1,18 | 1,04 / 1,09 | %0,3 / %-2,3 | %43 | 14,2 / 10 | kesik 27, stop 1893, stop_kesik 4, ters 6, zaman 53 | %21,3 |
| Y3 | AVR 2016-22 | 1,08 [1,02, 1,14] | 1,11 | 1,01 / 1,10 | %0,0 / %-0,8 | %46 | 18,9 / 14 | stop 1425, ters 23, zaman 89 | %17,5 |
| Y3 | AVR 2023 | 1,16 [0,99, 1,46] | 1,48 | 1,26 / 1,30 | %1,0 / %0,4 | %52 | 21,8 / 17 | stop 181, ters 2, zaman 7 | %15,9 |
| Y3 | AVR 2024-26 | 1,21 [1,11, 1,35] | 1,33 | 1,19 / 1,10 | %-0,0 / %-1,9 | %46 | 19,3 / 14 | kesik 14, stop 433, stop_kesik 1, ters 3, zaman 19 | %16,1 |
| Y3 | BIST 2016-22 | 0,98 [0,93, 1,03] | 0,95 | 0,98 / 0,95 | %2,8 / %0,0 | %49 | 16,2 / 11 | stop 1299, ters 6, zaman 43 | %21,0 |
| Y3 | BIST 2023 | 0,99 [0,92, 1,12] | 0,91 | 0,87 / 0,91 | %4,3 / %-1,6 | %45 | 11,2 / 8 | stop 425, zaman 7 | %24,9 |
| Y3 | BIST 2024-26 | 1,02 [0,99, 1,07] | 0,99 | 1,01 / 0,99 | %2,5 / %0,6 | %53 | 14,5 / 11 | kesik 1, stop 1035, stop_kesik 1, ters 3, zaman 4 | %20,1 |
| Y4 | ABD 2016-22 | 0,97 [0,93, 1,01] | 0,89 | 0,95 / 0,95 | %0,6 / %-0,1 | %50 | 27,0 / 22 | stop 6016, ters 256, zaman 1019 | %11,8 |
| Y4 | ABD 2023 | 0,95 [0,88, 1,01] | 0,89 | 1,01 / 0,91 | %0,7 / %-0,5 | %48 | 23,6 / 18 | stop 1365, ters 31, zaman 153 | %12,4 |
| Y4 | ABD 2024-26 | 0,99 [0,96, 1,02] | 0,91 | 0,98 / 1,03 | %1,0 / %-0,1 | %50 | 22,6 / 17 | kesik 43, stop 2897, stop_kesik 7, ters 59, zaman 242 | %12,1 |
| Y4 | AVR 2016-22 | 1,00 [0,94, 1,06] | 1,05 | 0,99 / 1,01 | %0,7 / %0,2 | %51 | 31,3 / 27 | stop 2984, ters 152, zaman 774 | %11,2 |
| Y4 | AVR 2023 | 0,95 [0,87, 1,08] | 0,85 | 0,86 / 1,02 | %-0,1 / %-1,0 | %47 | 28,7 / 25 | stop 555, ters 24, zaman 86 | %12,0 |
| Y4 | AVR 2024-26 | 0,92 [0,86, 0,98] | 0,80 | 0,93 / 0,81 | %0,7 / %-0,1 | %50 | 30,2 / 26 | kesik 58, stop 1028, ters 41, zaman 221 | %11,3 |
| Y4 | BIST 2016-22 | 1,01 [0,98, 1,05] | 1,00 | 0,98 / 0,97 | %4,3 / %0,8 | %53 | 18,1 / 14 | stop 1912, ters 17, zaman 65 | %13,4 |
| Y4 | BIST 2023 | 1,04 [1,00, 1,10] | 1,01 | 1,02 / 0,93 | %3,7 / %-2,0 | %45 | 12,0 / 9 | stop 312, zaman 4 | %13,5 |
| Y4 | BIST 2024-26 | 1,01 [0,97, 1,06] | 0,96 | 1,03 / 0,94 | %1,7 / %-0,4 | %48 | 14,5 / 11 | kesik 11, stop 1287, stop_kesik 2, ters 3, zaman 12 | %13,3 |
| Y5 | ABD 2016-22 | 1,17 [1,10, 1,27] | 1,22 | 1,37 / 1,05 | %-1,1 / %-3,0 | %40 | 15,9 / 12 | stop 1592, ters 10, zaman 25 | %15,4 |
| Y5 | ABD 2023 | 1,10 [0,94, 1,27] | 1,04 | 1,27 / 1,00 | %0,4 / %0,4 | %51 | 18,7 / 15 | stop 266, zaman 14 | %16,7 |
| Y5 | ABD 2024-26 | 1,11 [1,03, 1,19] | 1,07 | 1,27 / 0,97 | %-1,7 / %-3,5 | %40 | 15,8 / 13 | kesik 13, stop 901, ters 3, zaman 17 | %15,7 |
| Y5 | AVR 2016-22 | 1,25 [1,13, 1,40] | 1,33 | 1,24 / 1,10 | %-0,6 / %-3,3 | %38 | 18,9 / 14 | stop 450, ters 3, zaman 20 | %14,6 |
| Y5 | AVR 2023 | 1,30 [0,92, 1,48] | 1,67 | 1,33 / 1,21 | %-0,8 / %-1,0 | %45 | 19,9 / 14 | stop 81, ters 1, zaman 4 | %15,1 |
| Y5 | AVR 2024-26 | 1,10 [0,99, 1,23] | 1,23 | 1,10 / 1,04 | %-0,7 / %-1,9 | %43 | 20,5 / 15 | kesik 3, stop 248, ters 6, zaman 10 | %15,3 |
| Y5 | BIST 2016-22 | 1,10 [1,03, 1,18] | 1,12 | 1,21 / 1,03 | %-2,3 / %-3,6 | %38 | 12,1 / 9 | stop 586, zaman 5 | %16,5 |
| Y5 | BIST 2023 | 0,91 [0,79, 1,01] | 0,99 | 0,87 / 0,89 | %-2,1 / %-4,0 | %44 | 8,9 / 7 | stop 105 | %16,4 |
| Y5 | BIST 2024-26 | 1,07 [0,97, 1,16] | 1,10 | 1,08 / 1,16 | %-0,7 / %-0,7 | %45 | 12,7 / 10 | kesik 2, stop 255 | %16,0 |

## 7. ÇOKLU KARŞILAŞTIRMA (bilgi; KAT5 bootstrap p, BH q 0,10, karar hücreleri)

| Deneme | Hücre | p | BH geçer |
|---|---|---|---|
| Y1 | ABD 2023 | 0,791 | hayır |
| Y1 | ABD 2024-26 | 0,263 | hayır |
| Y1 | AVR 2023 | 0,597 | hayır |
| Y1 | AVR 2024-26 | 0,953 | hayır |
| Y2 | ABD 2023 | 0,563 | hayır |
| Y2 | ABD 2024-26 | 0,362 | hayır |
| Y2 | AVR 2023 | 0,072 | hayır |
| Y2 | AVR 2024-26 | 0,140 | hayır |
| Y3 | ABD 2023 | 0,018 | evet |
| Y3 | ABD 2024-26 | 0,004 | evet |
| Y3 | AVR 2023 | 0,000 | evet |
| Y3 | AVR 2024-26 | 0,011 | evet |
| Y4 | ABD 2023 | 0,870 | hayır |
| Y4 | ABD 2024-26 | 0,432 | hayır |
| Y4 | AVR 2023 | 0,822 | hayır |
| Y4 | AVR 2024-26 | 0,999 | hayır |
| Y5 | ABD 2023 | 0,083 | hayır |
| Y5 | ABD 2024-26 | 0,025 | evet |
| Y5 | AVR 2023 | 0,088 | hayır |
| Y5 | AVR 2024-26 | 0,181 | hayır |

## 8. VERİ SINIRLARI

- ABD: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 1411
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 580
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı; hisse 581
- Komisyon / kayma yok; stop çıkışı ertesi açılış. Takip stopu geçici kural; getiri bilgi.
- Hayatta kalma: batan / kottan çıkan hisse yok; hedef payları yukarı, stop payları aşağı yanlı okunmalı (eş ve plasebo aynı evrenden).

## 9. YENİDEN ÜRETİM (satır dosyasından iki hücre)

```
python - <<'EOF'
import pandas as pd
for d, p, q in [('Y1', 'ABD', '2023'), ('Y1', 'AVR', '2024-26')]:
    x = pd.read_csv(f'arastirma_cikti/yapi_hedef/olay_{d}.csv.gz'); x = x[(x.pazar == p) & (x.donem == q) & x.h5.notna() & x.es_h5.notna()]
    print(d, p, q, len(x), round(x.h5.sum() / x.es_h5.sum(), 4), round(x.st5.mean(), 4), round(x.es_st5.mean(), 4), round(x[x.pl_h5.notna()].h5.sum() / x.pl_h5.sum(), 4))
EOF
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı OC momentum beşliği x likidite üçlüsü kovası, olay hissesi hariç, AYNI giriş (t+1 açılış) / AYNI d ile stop0 / aynı hedefler / aynı takip kuralı / aynı 15 bar (yh_sim tek fonksiyon); taban = aynı gün bütün havuz; plasebo = aynı hisse rastgele gün aynı kural (hisse etkisi); mekanik üstünlük: d eşlere aynen verilir (stop uzaklığı farkı dışlandı), kırılım mumunun kendisi (t) ölçüye girmez (giriş t+1 açılış); güç simülasyonu KAT_ref 1,0 = yanlış pozitif payı |
| K2 | geleceğe bakma | EVET | sinyaller yalnız t ve öncesiyle (S6 durum makinesi nedensel; Y3 / Y5 pencereleri t-1'de biter, t yalnız kırılım kapanışı; Y4 hafızası a + 15 <= t şartıyla); test_yapi_hedef 'geleceğe bakma' bütün günlerde kesik seri = tam seri; koşuda her deneme x pazar 5 rastgele olay kesik veriyle yeniden üretilir (yh_gelecek_denetimi, tutmazsa DURUR); hedef / stop yalnız giriş ve sonrası fiyatla |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla + SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0 olmayan bar atılır; bütün pencereler geçerli bar dizisinde; 15 bar ve takip yalnız geçerli bar; sinyal günü geçersiz bar olamaz (veriden atılmış) |
| K4 | tekilleştirme | EVET | OC.oc_olay_hazirla: aynı hissede 60 birleşik takvim gününde tek olay (deneme başına); n = bağımsız olay; hücre tablosunda getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC); eş ve plasebo da kendi giriş günlerinin açılışı; stop çıkışı ertesi açılış; test 'giriş ertesi açılış' |
| K6 | veri birimi | EVET | tek kip V_*.pkl (fi_k1_veri düzeltilmiş fiyat); hedef / stop / d oran (birimden bağımsız); AVR yerel para, likidite kovası EUR (OC Kur); bölünme şüphesi geçmiş penceresinde havuz dışı (OC); ileri 15 barda dışlama yok (OC kuralı: sonuca göre seçim olurdu) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, k34 / Tiingo yok; V_AVR, V_BIST); batanlar yok -> hedef payı yukarı, stop payı aşağı yanlı; eş ve plasebo aynı evrenden olduğu için KAT'ta yanlılık kısmen birbirini götürür; rapora yazılır |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem (2016-22 / 2023 / 2024-26); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80 (guc_tablosu.json); iki yarı KAT (bilgi); 5 deneme x 4 karar hücresi BH q 0,10 (bilgi); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | YH_ESIK sha256 + YAPI_HEDEF.py / ORTAK_CETVEL.py / S6_TABAN.py / FITIL_V2.py sha256 + güç tablosu sha256 + Y2 olay dosyası sha256 ON_KAYIT.md'de; yh_kapi hepsini + ON_KAYIT ve kodun git'e işlenmiş / değişmemiş olmasını + IZ_KARNE.ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit (ölçümden önce); eşik sonuca göre oynanmaz; sapma SAPMA-n olarak koşudan önce |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV; Y2 olay dosyası FITIL_V2 kos çıktısı (sha ön kayıtta, giriş günü OC ile yeniden üretilir ve dosyadakiyle karşılaştırılır) |
| K11 | yeniden üretim | EVET | olay_Y*.csv.gz satır dosyaları (olay + eş + taban + plasebo göstergeleri); RAPOR.md 'YENİDEN ÜRETİM' bölümünde iki hücrenin KAT'ı satır dosyasından 5 satırlık bağımsız komutla; test KAT = OC.oc_kat |
| K12 | ifade | EVET | etiketler yalnız YH_ESIK['etiket'] kuralıyla (İZ / EMARE / DESTEKLENMEDİ / ÖLÇÜLEMEDİ); 'iz değil' yazılmaz; hedef payı fiyat dokunuşu, getiri komisyonsuz fiyat değişimi; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_yh; yasak defter dosyalarına dokunulmaz (git diff ile denetim); e-posta / anahtar taraması (test + yazım öncesi _yh_sizinti); ücretli veri yok; push yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm (yapı kuralları hedef payı) |
