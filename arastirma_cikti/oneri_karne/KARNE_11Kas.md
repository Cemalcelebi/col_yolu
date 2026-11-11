# Öneri / izleme karnesi — 11 Kas 2026 (ERKEN KARNE, KANIT DEĞİL)

Son kapanışlar: ABD 10 Kas 2026, BIST 10 Kas 2026. Kaynak: Yahoo günlük kapanış. Üreten: `python karne.py`.
İki rapordaki ve 9 Kas canlı taramalardaki **her ad** burada; alınmayanlar ve elenenler dahil.

## 1. Grup özeti

**ABD** (endeks: IWM; sepet: emsal sepeti (7))

| Grup | Ref. | n | Ort. | Medyan | IWM | Sepet | Ort. fazla (endeks) | Endeksi geçen | Sepeti geçen | Medyan en büyük düşüş |
|---|---|---|---|---|---|---|---|---|---|---|
| izleme 1-3 | 3 Kas | 3 | −%12,1 | −%15,4 | +%0,3 | −%10,5 | −%12,4 | 0 / 3 | 1 / 3 | −%23,2 |
| mevcut dörtlü | 3 Kas | 4 | −%2,3 | −%9,1 | +%0,3 | −%10,5 | −%2,6 | 1 / 4 | 2 / 4 | −%20,2 |
| elenenler | 3 Kas | 12 | −%11,1 | −%12,8 | +%0,3 | −%10,5 | −%11,4 | 4 / 12 | 5 / 12 | −%18,0 |
| diğer taranan | 3 Kas | 9 | −%13,9 | −%10,6 | +%0,3 | −%10,5 | −%14,2 | 1 / 9 | 4 / 9 | −%18,6 |
| emsal sepeti | 3 Kas | 7 | −%10,5 | −%9,3 | +%0,3 | −%10,5 | −%10,8 | 0 / 7 | 4 / 7 | −%20,4 |
| canlı tarama 9 Kas | 9 Kas | 2 | −%0,5 | −%0,5 | −%0,7 | −%1,9 | +%0,2 | 2 / 2 | 2 / 2 | −%0,5 |

**BIST** (endeks: XU100; sepet: karnedeki bütün BIST adları (eş ağırlık))

| Grup | Ref. | n | Ort. | Medyan | XU100 | Sepet | Ort. fazla (endeks) | Endeksi geçen | Sepeti geçen | Medyan en büyük düşüş |
|---|---|---|---|---|---|---|---|---|---|---|
| izleme 1-3 | 4 Kas | 3 | +%5,3 | +%7,5 | +%1,6 | +%7,3 | +%3,7 | 2 / 3 | 2 / 3 | −%4,1 |
| izleme listesi | 4 Kas | 7 | +%2,9 | +%2,1 | +%1,6 | +%7,3 | +%1,3 | 4 / 7 | 2 / 7 | −%4,5 |
| elenenler | 4 Kas | 26 | +%8,9 | +%4,2 | +%1,6 | +%7,3 | +%7,3 | 16 / 26 | 9 / 26 | −%3,2 |
| referans | 4 Kas | 1 | −%5,2 | −%5,2 | +%1,6 | +%7,3 | −%6,8 | 0 / 1 | 0 / 1 | −%9,9 |
| diğer taranan | 4 Kas | 3 | +%3,6 | +%3,7 | +%1,6 | +%7,3 | +%2,0 | 3 / 3 | 0 / 3 | −%4,2 |
| canlı tarama 9 Kas | 9 Kas | 2 | +%4,3 | +%4,3 | −%0,4 | −%1,9 | +%4,8 | 1 / 2 | 2 / 2 | −%0,7 |

n = ölçülen / toplam ad. İsabet = karşılaştırmayı geçen ad sayısı. 'mevcut dörtlü' izleme 1-3 ve elenenlerle örtüşür (DGXX, AIB, VIVO).
Duyarlılık: ABD elenenler, raporun §1 kısa listesi + NUAI, SLNH (POLA, BEEM, NVVE hariç): n = 9, ort. −%6,3, medyan −%8,8.

## 2. Alınan iki ad

| Ad | Rapor ref. kapanışı | Son kapanış | Rapordan beri | Endeks / sepet | Fazla (endeks / sepet) | En büyük düşüş | Alımdan beri |
|---|---|---|---|---|---|---|---|
| DGXX | 2,27 $ (3 Kas) | 2,16 $ (10 Kas) | −%4,8 | +%0,3 / −%10,5 | −%5,1 / +%5,7 | −%16,3 | +%7,5 (2,01 $'den) |
| YEOTK | 24,32 TL (4 Kas) | 28,00 TL (10 Kas) | +%15,1 | +%1,6 / +%7,3 | +%13,5 / +%7,8 | −%4,1 | +%9,2 (25,64 TL'den; endeks +%1,6) |

- DGXX: ort. maliyet 2,01 $ (Midas ekranı); alım günleri bilinmiyor, endeks karşılaştırması yok; sepet dibinden (5 Kas kapanışı) beri DGXX +%13,7, sepet +%15,4.
- YEOTK: maliyet bildirilmedi; alım günü (6 Kas, tavan) kapanışı vekil alındı.

## 3. Dürüstlük notu (önce bunu oku)

- **Pencere çok kısa:** ABD 3 Kas → 10 Kas: 5 işlem günü, ABD 9 Kas → 10 Kas: 1 işlem günü, BIST 4 Kas → 10 Kas: 4 işlem günü, BIST 9 Kas → 10 Kas: 1 işlem günü. Bu sürede hiçbir tez sınanmış olmaz.
- **n çok küçük:** izleme 1-3 grubunda pazar başına 3 ad var; tek bir ad ortalamayı belirler.
- **ABD, ortak hareket:** 3 Kas kapanışından beri IWM +%0,3, emsal sepeti (7) −%10,5. Sepetin pencere içi dibi 5 Kas (−%22,5); dipten beri sepet +%15,4, IWM +%3,5. Dipten ya da dip yakınından alınan her ad bu ortak tepkiyle artıda görünür; karşılaştırmayı aşmayan getiri seçimin değil pazarın getirisidir.
- **BIST, ortak hareket:** 4 Kas kapanışından beri XU100 +%1,6, karnedeki bütün BIST adları (eş ağırlık) +%7,3. Adların çoğu birlikte hareket etti; karşılaştırmayı aşmayan getiri seçimin değil pazarın getirisidir.
- **ABD, izleme 1-3 eksi elenenler:** fark −%1,0 puan (n = 3 ve 12, 5 gün). Bu penceredeki adlar arası dağılım (std) %19,9; farkın standart hatası %12,8; z = −0,1 (2'nin altı şanstan ayrılmaz). Aylık std %20-25 varsayımıyla aynı pencerede standart hata %6,3-%7,9. Bu büyüklükte bir fark her ay gerçekten olsaydı bile, ayda 3 adla ayırt etmek için yaklaşık 1.294-2.021 ay gerekirdi.
- **BIST, izleme 1-3 eksi elenenler:** fark −%3,6 puan (n = 3 ve 26, 4 gün). Bu penceredeki adlar arası dağılım (std) %12,3; farkın standart hatası %7,5; z = −0,5 (2'nin altı şanstan ayrılmaz). Aylık std %20-25 varsayımıyla aynı pencerede standart hata %5,3-%6,7. Bu büyüklükte bir fark her ay gerçekten olsaydı bile, ayda 3 adla ayırt etmek için yaklaşık 91-141 ay gerekirdi.
- **Kapsam:** 76 satırın hepsi ölçüldü; eksik ya da işlemi durmuş ad yok.
- **Sonuç:** bu tablo bir yön göstergesi değil, ayda bir güncellenecek kaydın ilk satırıdır. Hiçbir grup farkı şanstan ayrılmıyor.

**Fark şanstan ne zaman ayrılır? (basit hesap)** Gereken seçim-ay sayısı N = (2,8 × σ / Δ)²; σ = bir mikro-cap'in aylık getirisinin adlar arası std'si, Δ = seçilenlerin aylık fazla getirisi, 2,8 = %5 anlamlılık + %80 güç. İki küçük grup birbiriyle kıyaslanırsa N iki katına çıkar.

| σ (aylık) | Δ (aylık fazla) | N (endekse karşı) | N (iki küçük grup, grup başına) | Ayda 2 seçimle | Ayda 3 seçimle |
|---|---|---|---|---|---|
| %20,0 | %5,0 / ay | 126 | 251 | 63 ay | 42 ay |
| %20,0 | %10,0 / ay | 32 | 63 | 16 ay | 11 ay |
| %20,0 | %20,0 / ay | 8 | 16 | 4 ay | 3 ay |
| %25,0 | %5,0 / ay | 196 | 392 | 98 ay | 66 ay |
| %25,0 | %10,0 / ay | 49 | 98 | 25 ay | 17 ay |
| %25,0 | %20,0 / ay | 13 | 25 | 7 ay | 5 ay |

Aynı sektördeki adlar birlikte oynar; bağımsız gözlem sayısı ad sayısından azdır, süreler alt sınırdır. Aylık 5 puanlık gerçek bir üstünlük bile yıllarca veri ister; ancak 20 puan / ay gibi çok büyük bir fark bir yıl içinde görünür.

## 4. Ad ad tablo

**ABD** (son kapanış 10 Kas; para $)

| Ad | Rol | Ref. | Ref. kapanış | Son kapanış | Getiri | IWM | Fazla (endeks) | Fazla (sepet) | En büyük düşüş |
|---|---|---|---|---|---|---|---|---|---|
| DGXX | izleme 1-3, mevcut dörtlü | 3 Kas | 2,27 | 2,16 | −%4,8 | +%0,3 | −%5,1 | +%5,7 | −%16,3 |
| DUOT | izleme 1-3 | 3 Kas | 6,16 | 5,21 | −%15,4 | +%0,3 | −%15,7 | −%4,9 | −%23,2 |
| AIB | izleme 1-3, mevcut dörtlü | 3 Kas | 0,87 | 0,73 | −%16,1 | +%0,3 | −%16,4 | −%5,6 | −%24,1 |
| QMLS | mevcut dörtlü | 3 Kas | 3,54 | 3,07 | −%13,3 | +%0,3 | −%13,6 | −%2,7 | −%24,0 |
| VIVO | mevcut dörtlü, elenenler | 3 Kas | 1,60 | 2,00 | +%25,0 | +%0,3 | +%24,7 | +%35,5 | −%5,0 |
| GPUS | elenenler | 3 Kas | 0,17 | 0,19 | +%11,8 | +%0,3 | +%11,5 | +%22,3 | −%17,6 |
| BGDE | elenenler | 3 Kas | 3,15 | 3,20 | +%1,6 | +%0,3 | +%1,3 | +%12,1 | −%16,2 |
| DRK | elenenler | 3 Kas | 1,86 | 1,63 | −%11,9 | +%0,3 | −%12,1 | −%1,3 | −%15,6 |
| PWCM | elenenler | 3 Kas | 0,57 | 0,48 | −%16,5 | +%0,3 | −%16,8 | −%6,0 | −%18,4 |
| SGRX | elenenler | 3 Kas | 0,76 | 0,39 | −%48,4 | +%0,3 | −%48,7 | −%37,9 | −%48,4 |
| SOBR | elenenler | 3 Kas | 0,04 | 0,05 | +%16,3 | +%0,3 | +%16,0 | +%26,8 | %0,0 |
| POLA | elenenler | 3 Kas | 0,52 | 0,30 | −%42,3 | +%0,3 | −%42,6 | −%31,8 | −%42,3 |
| BEEM | elenenler | 3 Kas | 0,80 | 0,69 | −%13,7 | +%0,3 | −%14,0 | −%3,1 | −%13,7 |
| NVVE | elenenler | 3 Kas | 0,76 | 0,60 | −%20,9 | +%0,3 | −%21,2 | −%10,4 | −%20,9 |
| NUAI | elenenler | 3 Kas | 2,78 | 2,07 | −%25,5 | +%0,3 | −%25,8 | −%15,0 | −%41,4 |
| SLNH | elenenler | 3 Kas | 0,57 | 0,52 | −%8,8 | +%0,3 | −%9,1 | +%1,8 | −%19,3 |
| HOST | diğer taranan | 3 Kas | 2,59 | 1,85 | −%28,6 | +%0,3 | −%28,9 | −%18,0 | −%29,0 |
| SLNG | diğer taranan | 3 Kas | 4,32 | 3,81 | −%11,8 | +%0,3 | −%12,1 | −%1,3 | −%17,1 |
| VIP | diğer taranan | 3 Kas | 1,18 | 0,97 | −%17,8 | +%0,3 | −%18,1 | −%7,3 | −%18,6 |
| TSSI | diğer taranan | 3 Kas | 7,03 | 6,96 | −%1,0 | +%0,3 | −%1,3 | +%9,5 | −%15,4 |
| IPWR | diğer taranan | 3 Kas | 2,47 | 2,26 | −%8,5 | +%0,3 | −%8,8 | +%2,0 | −%16,6 |
| TGEN | diğer taranan | 3 Kas | 1,88 | 1,68 | −%10,6 | +%0,3 | −%10,9 | −%0,1 | −%18,6 |
| PPSI | diğer taranan | 3 Kas | 2,46 | 2,22 | −%9,8 | +%0,3 | −%10,0 | +%0,8 | −%9,8 |
| ZSQR | diğer taranan | 3 Kas | 3,73 | 2,30 | −%38,3 | +%0,3 | −%38,6 | −%27,8 | −%38,3 |
| AGPU | diğer taranan | 3 Kas | 7,56 | 7,64 | +%1,1 | +%0,3 | +%0,8 | +%11,6 | −%20,0 |
| CRWV | emsal sepeti | 3 Kas | 53,74 | 48,73 | −%9,3 | +%0,3 | −%9,6 | +%1,2 | −%18,8 |
| NBIS | emsal sepeti | 3 Kas | 151,64 | 134,00 | −%11,6 | +%0,3 | −%11,9 | −%1,1 | −%20,6 |
| APLD | emsal sepeti | 3 Kas | 17,81 | 16,68 | −%6,3 | +%0,3 | −%6,6 | +%4,2 | −%20,4 |
| IREN | emsal sepeti | 3 Kas | 24,46 | 19,73 | −%19,3 | +%0,3 | −%19,6 | −%8,8 | −%26,3 |
| WULF | emsal sepeti | 3 Kas | 12,53 | 12,56 | +%0,2 | +%0,3 | %0,0 | +%10,8 | −%19,6 |
| CIFR | emsal sepeti | 3 Kas | 8,12 | 6,53 | −%19,6 | +%0,3 | −%19,9 | −%9,0 | −%31,7 |
| CORZ | emsal sepeti | 3 Kas | 14,24 | 13,13 | −%7,8 | +%0,3 | −%8,1 | +%2,7 | −%20,1 |
| CENX | canlı tarama 9 Kas | 9 Kas | 36,62 | 36,42 | −%0,5 | −%0,7 | +%0,1 | +%1,4 | −%0,5 |
| AEHR | canlı tarama 9 Kas | 9 Kas | 59,81 | 59,57 | −%0,4 | −%0,7 | +%0,3 | +%1,5 | −%0,4 |

**BIST** (son kapanış 10 Kas; para TL; bütün adlarda 10 Kas kapanışı Yahoo son fiyat alanından (kapanış çubuğu henüz boş))

| Ad | Rol | Ref. | Ref. kapanış | Son kapanış | Getiri | XU100 | Fazla (endeks) | Fazla (sepet) | En büyük düşüş |
|---|---|---|---|---|---|---|---|---|---|
| YEOTK | izleme 1-3 | 4 Kas | 24,32 | 28,00 | +%15,1 | +%1,6 | +%13,5 | +%7,8 | −%4,1 |
| GWIND | izleme 1-3 | 4 Kas | 17,95 | 19,29 | +%7,5 | +%1,6 | +%5,9 | +%0,2 | −%0,2 |
| EUPWR | izleme 1-3 | 4 Kas | 43,02 | 40,14 | −%6,7 | +%1,6 | −%8,3 | −%14,0 | −%10,0 |
| GESAN | izleme listesi | 4 Kas | 35,56 | 34,14 | −%4,0 | +%1,6 | −%5,6 | −%11,3 | −%10,0 |
| ORGE | izleme listesi | 4 Kas | 18,45 | 19,96 | +%8,2 | +%1,6 | +%6,6 | +%0,9 | −%4,5 |
| VBTYZ | izleme listesi | 4 Kas | 20,80 | 21,24 | +%2,1 | +%1,6 | +%0,5 | −%5,2 | −%4,2 |
| FORTE | izleme listesi | 4 Kas | 77,70 | 86,85 | +%11,8 | +%1,6 | +%10,2 | +%4,5 | −%1,4 |
| INDES | izleme listesi | 4 Kas | 11,09 | 10,71 | −%3,4 | +%1,6 | −%5,0 | −%10,7 | −%9,9 |
| CWENE | izleme listesi | 4 Kas | 16,36 | 16,09 | −%1,7 | +%1,6 | −%3,3 | −%8,9 | −%11,5 |
| ULUSE | izleme listesi | 4 Kas | 138,00 | 147,60 | +%7,0 | +%1,6 | +%5,4 | −%0,3 | −%3,3 |
| KONTR | elenenler | 4 Kas | 2,43 | 2,41 | −%0,8 | +%1,6 | −%2,4 | −%8,1 | −%10,1 |
| ODINE | elenenler | 4 Kas | 52,95 | 61,90 | +%16,9 | +%1,6 | +%15,3 | +%9,6 | −%3,0 |
| ANELE | elenenler | 4 Kas | 5,69 | 8,30 | +%45,9 | +%1,6 | +%44,3 | +%38,6 | %0,0 |
| MANAS | elenenler | 4 Kas | 1,85 | 2,69 | +%45,4 | +%1,6 | +%43,8 | +%38,1 | %0,0 |
| IEYHO | elenenler | 4 Kas | 5,84 | 7,32 | +%25,3 | +%1,6 | +%23,7 | +%18,0 | %0,0 |
| GEREL | elenenler | 4 Kas | 21,90 | 22,12 | +%1,0 | +%1,6 | −%0,6 | −%6,3 | −%1,4 |
| NETAS | elenenler | 4 Kas | 69,30 | 64,90 | −%6,3 | +%1,6 | −%8,0 | −%13,6 | −%10,0 |
| SMRTG | elenenler | 4 Kas | 3,80 | 4,16 | +%9,5 | +%1,6 | +%7,9 | +%2,2 | −%6,5 |
| MAGEN | elenenler | 4 Kas | 4,82 | 5,63 | +%16,8 | +%1,6 | +%15,2 | +%9,5 | %0,0 |
| ESEN | elenenler | 4 Kas | 1,97 | 2,08 | +%5,6 | +%1,6 | +%4,0 | −%1,7 | −%4,1 |
| EMKEL | elenenler | 4 Kas | 4,86 | 5,23 | +%7,6 | +%1,6 | +%6,0 | +%0,3 | −%0,8 |
| PAPIL | elenenler | 4 Kas | 5,65 | 5,89 | +%4,2 | +%1,6 | +%2,6 | −%3,0 | −%4,7 |
| MIATK | elenenler | 4 Kas | 24,28 | 24,18 | −%0,4 | +%1,6 | −%2,0 | −%7,7 | −%2,0 |
| ARENA | elenenler | 4 Kas | 11,52 | 12,20 | +%5,9 | +%1,6 | +%4,3 | −%1,4 | −%2,9 |
| LINK | elenenler | 4 Kas | 2,70 | 2,79 | +%3,3 | +%1,6 | +%1,7 | −%4,0 | −%4,1 |
| EDATA | elenenler | 4 Kas | 2,98 | 3,54 | +%18,8 | +%1,6 | +%17,2 | +%11,5 | −%1,0 |
| INGRM | elenenler | 4 Kas | 206,00 | 212,90 | +%3,3 | +%1,6 | +%1,7 | −%3,9 | −%4,5 |
| ALFAS | elenenler | 4 Kas | 23,00 | 24,36 | +%5,9 | +%1,6 | +%4,3 | −%1,4 | −%5,9 |
| SAYAS | elenenler | 4 Kas | 32,68 | 40,64 | +%24,4 | +%1,6 | +%22,8 | +%17,1 | %0,0 |
| KRONT | elenenler | 4 Kas | 16,92 | 16,63 | −%1,7 | +%1,6 | −%3,3 | −%9,0 | −%7,6 |
| ATATP | elenenler | 4 Kas | 213,00 | 214,00 | +%0,5 | +%1,6 | −%1,1 | −%6,8 | −%5,5 |
| FONET | elenenler | 4 Kas | 3,82 | 3,98 | +%4,2 | +%1,6 | +%2,6 | −%3,1 | −%2,5 |
| KFEIN | elenenler | 4 Kas | 5,14 | 5,16 | +%0,4 | +%1,6 | −%1,2 | −%6,9 | −%2,6 |
| ESCOM | elenenler | 4 Kas | 3,62 | 3,61 | −%0,3 | +%1,6 | −%1,9 | −%7,6 | −%3,7 |
| DGATE | elenenler | 4 Kas | 45,60 | 44,64 | −%2,1 | +%1,6 | −%3,7 | −%9,4 | −%10,0 |
| PENTA | elenenler | 4 Kas | 9,00 | 8,83 | −%1,9 | +%1,6 | −%3,5 | −%9,2 | −%3,5 |
| ASTOR | referans | 4 Kas | 165,70 | 157,10 | −%5,2 | +%1,6 | −%6,8 | −%12,5 | −%9,9 |
| ARDYZ | diğer taranan | 4 Kas | 53,80 | 55,80 | +%3,7 | +%1,6 | +%2,1 | −%3,6 | −%10,0 |
| TCELL | diğer taranan | 4 Kas | 93,95 | 97,75 | +%4,0 | +%1,6 | +%2,4 | −%3,2 | −%4,2 |
| TTKOM | diğer taranan | 4 Kas | 48,90 | 50,45 | +%3,2 | +%1,6 | +%1,6 | −%4,1 | −%2,3 |
| PNLSN | canlı tarama 9 Kas | 9 Kas | 30,60 | 33,66 | +%10,0 | −%0,4 | +%10,4 | +%11,9 | %0,0 |
| FORTE | canlı tarama 9 Kas | 9 Kas | 88,05 | 86,85 | −%1,4 | −%0,4 | −%0,9 | +%0,6 | −%1,4 |

## 5. Yöntem

- Getiri = son kapanış / referans kapanışı − 1 (Yahoo düzeltilmiş kapanış: bölünme ve temettü dahil; tabloda görünen fiyat ham kapanış).
- Referans günü: ABD raporu 3 Kas, BIST raporu 4 Kas, canlı taramalar 9 Kas kapanışı.
- Karşılaştırma aynı pencerede: ABD için IWM ve 7'li emsal sepeti (CRWV, NBIS, APLD, IREN, WULF, CIFR, CORZ; eş ağırlık); BIST için XU100 ve karnedeki bütün BIST adlarının eş ağırlıklı ortalaması.
- En büyük düşüş: pencere içinde kapanıştan kapanışa tepe-dip (gün içi fitiller yok).
- ABD elenenler listesi raporun §9'undaki tam listedir (POLA, BEEM, NVVE dahil); 'diğer taranan' = raporda tabloda olup sıralamaya girmeyen adlar.
- Roller ve tarihler karne.py içindeki KR_KURAL'dadır; yeni öneri oraya bir satır olarak eklenir.

