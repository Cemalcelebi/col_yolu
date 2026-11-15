# K59 — basit sinyaller, portföy cetveli v2: RAPOR

Ön kayıt: 2026-11-11 05:48:23 UTC (mühür 6fe8bb385667, dosya sha256 11560c74c315, git 9e04f3e953); koşu 2026-11-11 05:51:13 UTC → 2026-11-11 05:57:53 UTC. K59 v1.1 (2026-11-11): basit sinyaller (S1-S9, COMP4, COMP9) + DOSYA ailesi (DOSYA_Y, DOSYA_D, DOSYA_YD) + UCUZLUK koşullu testi x portföy cetveli v2 (K58 C + beta düzeltmeli alfa); ABD iki evren karar, BIST bilgi

## Düz dille
Cetvelin kendisi: 200 rastgele sinyalden maliyetli %0,0, maliyetsiz %1,5 'tutar' çıktı (eşik %5); cetvel v2 GÜVENİLİR. Önceden yazılı bileşik (COMP4) U1'de maliyetten sonra evrene göre yıllık fazlası -%1,6 (NW t -0,49, beta düzeltmeli alfa yıllık +%0,4, t 0,16; 66 ay): TUTMAZ (sağlanmayan şart: fazla NW t, alt dönem, son %30, alfa). Önceden yazılı bileşik (COMP4) U2'de maliyetten sonra evrene göre yıllık fazlası +%5,5 (NW t 2,30, beta düzeltmeli alfa yıllık +%6,1, t 2,87; 66 ay): TUTMAZ (sağlanmayan şart: son %30). Karar: TUTMAZ (U1 TUTMAZ, U2 TUTMAZ). Tekil sinyallerden ABD'de tutanlar (bilgi; seçim yapılmaz): U1 S1, U1 S3. BIST'te (bilgi) tutanlar: S9. DOSYA ailesi (YEOTK / DGXX mantığı, kendi başına): U1 DOSYA_Y TUTMAZ; U2 DOSYA_Y TUTMAZ; U1 DOSYA_D TUTMAZ; U2 DOSYA_D TUTMAZ; U1 DOSYA_YD TUTMAZ; U2 DOSYA_YD TUTMAZ. UCUZLUK (bilgi) U1: bileşiğin üst %20'sinde düşmüş yarı, zirveye yakın yarıdan yılda %2,6 eksik getirdi (NW t -0,56). UCUZLUK (bilgi) U2: bileşiğin üst %20'sinde düşmüş yarı, zirveye yakın yarıdan yılda %2,2 eksik getirdi (NW t -0,60).

## Karar (ön kayıt §4-§5)
- Cetvel v2: GÜVENİLİR (plasebo yanlış pozitif maliyetli %0,0, maliyetsiz %1,5).
- COMP4 kararı: TUTMAZ (U1 TUTMAZ, U2 TUTMAZ).
- DOSYA ailesi (kendi başına; karara girmez): U1 DOSYA_Y TUTMAZ; U2 DOSYA_Y TUTMAZ; U1 DOSYA_D TUTMAZ; U2 DOSYA_D TUTMAZ; U1 DOSYA_YD TUTMAZ; U2 DOSYA_YD TUTMAZ.
- İZ ilan edilemez: CLAUDE.md standardı (FI_OLCUT, ABD + Avrupa) değişmedi, Avrupa'da temel veri yok; standart değişikliği Cemal'in kararı.

Cetvel v2 şartları (maliyetten sonra): ortalama fazla > 0 ve NW t > 2.0; 3 alt dönemin en az 2'sinde > 0; son %30 ayda > 0;
alfa > 0 ve NW t(alfa) > 2.0. 'GÜÇLÜ' = iki t de > 2.8. 'küçük' = net yıllık fazla < +4 puan.

## U1 — V_ABD (islenmis-veri; bugün yaşayan ~1.400 ABD hissesi) (KARAR)
1411 hisse, 123 oluşum ayı (2016-05-31 .. 2026-07-31), ortalama uygun evren 1084 hisse; maliyet tek yön 10 bp; S3 ölçüsü (ay sayısı): {'islem_degeri': 123}. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%1625, +%300 üstü 7 / 133373 hisse-ay.

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 momentum 12-1 | 122 | 2016-06-30 | +%11,9 | 2,77 | +%0,60 / +%1,37 / +%1,00 | +%1,02 | +%8,8 | 2,09 | 1,17 | +%10,7 | 2,73 | 0,93 | -%25,8 | %60 | 109 | +%12,6 | 2,94 | 2,27 | TUTAR (yineleme) |
| S2 1 ay dönüş (geçen ayın en çok düşenleri) | 123 | 2016-05-31 | +%3,3 | 0,82 | +%0,47 / +%0,41 / -%0,06 | -%0,33 | -%4,4 | -1,33 | 1,44 | +%1,2 | 0,37 | 0,57 | -%48,7 | %175 | 108 | +%5,4 | 1,35 | -0,69 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| S3 küçüklük | 123 | 2016-05-31 | +%10,8 | 3,03 | +%0,10 / +%0,62 / +%1,98 | +%1,92 | +%6,4 | 2,22 | 1,25 | +%13,5 | 5,55 | 0,95 | -%35,8 | %54 | 108 | +%11,5 | 3,21 | 2,45 | TUTAR (yineleme) |
| S4 bilanço tepkisi (PEAD) | 66 | 2021-02-26 | -%2,5 | -0,61 | -%1,49 / +%0,10 / +%0,75 | +%0,58 | -%5,6 | -1,65 | 1,23 | +%3,9 | 1,67 | 0,32 | -%40,7 | %72 | 114 | -%1,6 | -0,40 | -1,39 | TUTMAZ (tutmayan: fazla NW t, alfa) |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 66 | 2021-02-26 | -%1,8 | -0,61 | +%0,73 / -%0,47 / -%0,73 | -%0,78 | +%0,6 | 0,27 | 0,82 | -%2,1 | -1,08 | 0,50 | -%25,8 | %21 | 91 | -%1,6 | -0,52 | 0,38 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S6 düşük net ihraç (yıllık pay değişimi) | 54 | 2022-02-28 | +%0,3 | 0,10 | -%0,11 / +%0,74 / -%0,55 | -%0,56 | +%0,9 | 0,27 | 0,97 | +%2,4 | 0,85 | 0,60 | -%22,4 | %36 | 98 | +%0,8 | 0,24 | 0,41 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S7 satış ivmesi (son çeyrek / önceki iki çeyrek ortalaması) | 68 | 2020-12-31 | +%3,6 | 1,27 | +%0,25 / +%0,59 / +%0,04 | -%0,07 | -%0,7 | -0,24 | 1,27 | +%5,9 | 1,82 | 0,62 | -%27,7 | %61 | 94 | +%4,3 | 1,53 | 0,03 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| S8 düşük oynaklık (60 gün) | 123 | 2016-05-31 | -%7,8 | -1,95 | -%0,03 / -%0,73 / -%1,19 | -%1,03 | +%0,5 | 0,19 | 0,52 | -%3,3 | -1,38 | 0,53 | -%27,7 | %53 | 108 | -%7,2 | -1,78 | 0,41 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S9 52 hafta zirvesine yakınlık | 123 | 2016-05-31 | -%5,9 | -1,85 | -%0,43 / -%0,40 / -%0,63 | -%0,45 | +%1,1 | 0,54 | 0,60 | -%1,8 | -1,03 | 0,63 | -%24,1 | %129 | 108 | -%4,3 | -1,36 | 1,31 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 66 | 2021-02-26 | -%1,6 | -0,49 | +%0,63 / -%0,24 / -%0,78 | -%0,77 | +%0,4 | 0,16 | 0,85 | -%2,7 | -1,28 | 0,49 | -%22,8 | %64 | 103 | -%0,8 | -0,25 | 0,46 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| COMP9 bileşik: dokuz sinyalin hepsi | 122 | 2016-06-30 | -%6,2 | -1,95 | -%0,41 / -%0,44 / -%0,71 | -%0,54 | -%1,1 | -0,37 | 0,71 | -%3,3 | -1,36 | 0,55 | -%33,1 | %89 | 109 | -%5,2 | -1,62 | -0,02 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 64 | 2021-04-30 | +%0,8 | 0,22 | +%0,40 / +%0,52 / -%0,73 | -%0,79 | +%1,4 | 0,39 | 0,96 | +%0,8 | 0,27 | 0,53 | -%26,5 | %65 | 87 | +%1,6 | 0,43 | 0,61 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| DOSYA_D DGXX tipi (vekil): sağlam bilanço + büyüme + düşmüş fiyat | 64 | 2021-04-30 | -%3,1 | -0,39 | -%2,10 / +%0,43 / +%0,97 | +%0,82 | -%9,2 | -1,48 | 1,46 | +%4,1 | 1,10 | 0,20 | -%57,4 | %55 | 82 | -%2,4 | -0,30 | -1,36 | TUTMAZ (tutmayan: fazla NW t, alfa) |
| DOSYA_YD DOSYA_Y + düşük kaldıraç | 64 | 2021-04-30 | +%0,5 | 0,13 | +%0,28 / +%0,22 / -%0,41 | -%0,48 | +%0,3 | 0,09 | 1,01 | +%2,2 | 0,80 | 0,48 | -%27,9 | %60 | 80 | +%1,2 | 0,35 | 0,31 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |

## U2 — geniş ABD evreni (K57-B Yahoo önbelleği; bugün yaşayan ~4.260 hisse) (KARAR)
4261 hisse, 68 oluşum ayı (2020-12-31 .. 2026-07-31), ortalama uygun evren 2146 hisse; maliyet tek yön 10 bp; S3 ölçüsü (ay sayısı): {'piyasa_degeri': 65, 'islem_degeri': 3}. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%1625, +%300 üstü 12 / 145962 hisse-ay.

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 momentum 12-1 | 67 | 2021-01-29 | -%2,8 | -0,54 | -%0,77 / -%0,22 / +%0,33 | +%0,07 | -%4,3 | -0,82 | 1,19 | -%5,4 | -1,25 | 0,07 | -%41,3 | %65 | 215 | -%2,0 | -0,39 | -0,67 | TUTMAZ (tutmayan: fazla NW t, alt dönem, alfa) |
| S2 1 ay dönüş (geçen ayın en çok düşenleri) | 68 | 2020-12-31 | -%10,4 | -1,54 | -%0,94 / -%0,17 / -%1,52 | -%1,39 | -%14,6 | -2,92 | 1,46 | -%10,3 | -1,35 | -0,14 | -%59,1 | %175 | 215 | -%8,3 | -1,23 | -2,50 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S3 küçüklük | 68 | 2020-12-31 | -%11,8 | -2,11 | -%0,91 / -%0,52 / -%1,53 | -%1,72 | -%14,6 | -3,17 | 1,31 | -%12,8 | -1,94 | -0,21 | -%59,2 | %71 | 192 | -%10,9 | -1,95 | -2,97 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S4 bilanço tepkisi (PEAD) | 66 | 2021-02-26 | -%2,3 | -0,75 | -%0,79 / -%0,16 / +%0,37 | +%0,13 | -%3,6 | -1,33 | 1,20 | -%5,9 | -2,16 | 0,03 | -%45,3 | %77 | 197 | -%1,4 | -0,45 | -0,98 | TUTMAZ (tutmayan: fazla NW t, alt dönem, alfa) |
| S5 kârlılık (son 4 çeyrek net kâr / özkaynak) | 66 | 2021-02-26 | +%5,4 | 1,99 | +%1,12 / +%0,27 / -%0,03 | -%0,05 | +%6,3 | 2,63 | 0,87 | -%1,5 | -0,75 | 0,48 | -%26,4 | %22 | 172 | +%5,7 | 2,08 | 2,73 | TUTMAZ (tutmayan: fazla NW t, son %30) |
| S6 düşük net ihraç (yıllık pay değişimi) | 54 | 2022-02-28 | +%1,9 | 0,78 | +%0,03 / +%0,57 / -%0,13 | -%0,13 | +%2,4 | 0,97 | 0,94 | -%1,9 | -0,71 | 0,35 | -%22,7 | %41 | 174 | +%2,4 | 0,99 | 1,17 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| S7 satış ivmesi (son çeyrek / önceki iki çeyrek ortalaması) | 68 | 2020-12-31 | -%4,0 | -1,97 | -%0,10 / -%0,39 / -%0,53 | -%0,46 | -%5,6 | -3,18 | 1,17 | -%5,6 | -1,58 | 0,08 | -%42,9 | %64 | 184 | -%3,3 | -1,58 | -2,74 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S8 düşük oynaklık (60 gün) | 68 | 2020-12-31 | -%0,6 | -0,10 | +%0,72 / -%0,12 / -%0,77 | -%0,59 | +%4,5 | 1,58 | 0,45 | -%5,2 | -1,98 | 0,42 | -%14,5 | %51 | 215 | +%0,1 | 0,01 | 1,81 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S9 52 hafta zirvesine yakınlık | 68 | 2020-12-31 | +%0,5 | 0,11 | +%0,52 / -%0,32 / -%0,07 | -%0,06 | +%4,0 | 1,41 | 0,62 | -%4,2 | -2,04 | 0,44 | -%19,8 | %120 | 215 | +%2,0 | 0,43 | 1,89 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| COMP4 bileşik: momentum + PEAD + kârlılık + düşük ihraç | 66 | 2021-02-26 | +%5,5 | 2,30 | +%0,92 / +%0,48 / -%0,03 | -%0,06 | +%6,1 | 2,87 | 0,91 | -%2,0 | -1,01 | 0,45 | -%25,0 | %66 | 188 | +%6,3 | 2,64 | 3,25 | TUTMAZ (tutmayan: son %30) |
| COMP9 bileşik: dokuz sinyalin hepsi | 68 | 2020-12-31 | +%3,2 | 0,70 | +%1,13 / +%0,35 / -%0,73 | -%0,74 | +%6,0 | 1,92 | 0,69 | -%2,7 | -1,11 | 0,58 | -%17,3 | %95 | 209 | +%4,3 | 0,95 | 2,28 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| DOSYA_Y YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme | 64 | 2021-04-30 | +%5,1 | 2,14 | +%0,61 / +%0,80 / -%0,14 | -%0,11 | +%5,3 | 2,28 | 0,96 | -%1,6 | -0,60 | 0,38 | -%26,8 | %64 | 171 | +%5,9 | 2,47 | 2,62 | TUTMAZ (tutmayan: son %30) |
| DOSYA_D DGXX tipi (vekil): sağlam bilanço + büyüme + düşmüş fiyat | 64 | 2021-04-30 | -%10,5 | -1,52 | -%2,45 / -%0,34 / +%0,25 | +%0,21 | -%12,5 | -2,28 | 1,35 | -%10,0 | -3,12 | -0,27 | -%66,7 | %58 | 167 | -%9,8 | -1,41 | -2,15 | TUTMAZ (tutmayan: fazla NW t, alt dönem, alfa) |
| DOSYA_YD DOSYA_Y + düşük kaldıraç | 64 | 2021-04-30 | +%4,4 | 1,95 | +%0,43 / +%0,83 / -%0,16 | -%0,10 | +%4,4 | 1,98 | 1,00 | -%1,2 | -0,45 | 0,33 | -%29,0 | %62 | 161 | +%5,1 | 2,28 | 2,32 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |

## BIST — V_BIST (islenmis-veri; bugün yaşayan ~580 hisse) (BİLGİ)
581 hisse, 123 oluşum ayı (2016-05-31 .. 2026-07-31), ortalama uygun evren 423 hisse; maliyet tek yön 30 bp; S3 ölçüsü (ay sayısı): {'islem_degeri': 123}. Veri denetimi (kırpma yok): en büyük tek hisse aylık getirisi +%702, +%300 üstü 21 / 52083 hisse-ay.

| Sinyal | Ay | İlk ay | Yıllık fazla (net) | NW t | Alt 1/2/3 | Son %30 | Alfa (yıllık) | t(alfa) | Beta | FF5+UMD alfa | t | Sharpe | En büyük düşüş | Devir | Hisse | Brüt fazla | Brüt NW t | Brüt t(alfa) | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 momentum 12-1 | 122 | 2016-06-30 | -%4,5 | -0,83 | -%0,11 / -%0,87 / -%0,13 | +%0,02 | -%1,8 | -0,28 | 0,95 | — | — | 1,42 | -%39,3 | %60 | 42 | -%2,2 | -0,41 | 0,06 | TUTMAZ (tutmayan: fazla NW t, alt dönem, alfa) |
| S2 1 ay dönüş (geçen ayın en çok düşenleri) | 123 | 2016-05-31 | -%22,0 | -4,31 | -%0,51 / -%2,52 / -%2,45 | -%2,36 | -%13,7 | -3,89 | 0,84 | — | — | 1,01 | -%34,5 | %180 | 42 | -%15,3 | -3,00 | -2,05 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S3 küçüklük | 123 | 2016-05-31 | +%33,6 | 2,19 | +%0,69 / +%5,08 / +%2,64 | +%3,09 | +%16,8 | 1,55 | 1,32 | — | — | 1,51 | -%19,3 | %38 | 42 | +%35,1 | 2,28 | 1,68 | TUTMAZ (tutmayan: alfa) |
| S8 düşük oynaklık (60 gün) | 123 | 2016-05-31 | -%12,8 | -1,75 | -%1,02 / -%1,78 / -%0,39 | -%0,22 | +%3,1 | 0,78 | 0,70 | — | — | 1,57 | -%23,5 | %75 | 42 | -%10,0 | -1,35 | 1,44 | TUTMAZ (tutmayan: fazla NW t, alt dönem, son %30, alfa) |
| S9 52 hafta zirvesine yakınlık | 123 | 2016-05-31 | +%16,6 | 2,83 | -%0,31 / +%2,71 / +%1,74 | +%1,92 | +%13,3 | 2,42 | 1,06 | — | — | 1,81 | -%27,5 | %121 | 42 | +%21,2 | 3,57 | 3,20 | TUTAR (yineleme) |
| COMP9 bileşik: dokuz sinyalin hepsi | 122 | 2016-06-30 | +%6,2 | 1,82 | +%0,13 / +%1,37 / +%0,04 | +%0,09 | +%13,2 | 3,85 | 0,87 | — | — | 1,96 | -%16,5 | %112 | 42 | +%10,4 | 3,04 | 5,00 | TUTMAZ (tutmayan: fazla NW t) |

## DOSYA ailesi (YEOTK / DGXX'i seçtiren mantık; ayrı aile, 3 ek deneme; PORTFÖY-ADAY kararına girmez)
Her bileşik kendi başına cetvel v2 ile etiketlenir; 'GÜÇLÜ' eşiği iki t de > 2.9 (12 deneme). DOSYA_D yalnız ölçülebilir kısmın vekilidir: gerçek DGXX seçimindeki 'SEC'e ekli bağlayıcı sözleşme' yapısal veride yok (K60). BIST'te ölçülmedi (temel veri yüklenmedi).

| Bileşik | Evren | Ay | İlk ay | Yıllık fazla (net) | NW t | Alfa (yıllık) | t(alfa) | FF5+UMD alfa | t | Hisse | Brüt fazla | Etiket |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DOSYA_Y (YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme) | U1 | 64 | 2021-04-30 | +%0,8 | 0,22 | +%1,4 | 0,39 | +%0,8 | 0,27 | 87 | +%1,6 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| DOSYA_Y (YEOTK tipi: ivmelenen, kârlı, seyrelmesiz büyüme) | U2 | 64 | 2021-04-30 | +%5,1 | 2,14 | +%5,3 | 2,28 | -%1,6 | -0,60 | 171 | +%5,9 | TUTMAZ (tutmayan: son %30) |
| DOSYA_D (DGXX tipi (vekil): sağlam bilanço + büyüme + düşmüş fiyat) | U1 | 64 | 2021-04-30 | -%3,1 | -0,39 | -%9,2 | -1,48 | +%4,1 | 1,10 | 82 | -%2,4 | TUTMAZ (tutmayan: fazla NW t, alfa) |
| DOSYA_D (DGXX tipi (vekil): sağlam bilanço + büyüme + düşmüş fiyat) | U2 | 64 | 2021-04-30 | -%10,5 | -1,52 | -%12,5 | -2,28 | -%10,0 | -3,12 | 167 | -%9,8 | TUTMAZ (tutmayan: fazla NW t, alt dönem, alfa) |
| DOSYA_YD (DOSYA_Y + düşük kaldıraç) | U1 | 64 | 2021-04-30 | +%0,5 | 0,13 | +%0,3 | 0,09 | +%2,2 | 0,80 | 80 | +%1,2 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |
| DOSYA_YD (DOSYA_Y + düşük kaldıraç) | U2 | 64 | 2021-04-30 | +%4,4 | 1,95 | +%4,4 | 1,98 | -%1,2 | -0,45 | 161 | +%5,1 | TUTMAZ (tutmayan: fazla NW t, son %30, alfa) |

## Koşullu test UCUZLUK (bilgi; karar yok)
COMP4 üst %20'si her ay S9'a göre ikiye bölündü: 'dusmus' = zirvesinden en uzak yarı, 'yakin' = zirveye en yakın yarı. İlk iki satır evrene göre fazla, 'fark' satırı iki uzun portföyün aylık net farkıdır (dusmus - yakin).

| Evren | Portföy | Ay | Yıllık fazla / fark (net) | NW t | Alfa (yıllık) | t(alfa) | Hisse | Devir | Brüt | Brüt NW t |
|---|---|---|---|---|---|---|---|---|---|---|
| U1 | dusmus | 66 | -%2,6 | -0,75 | -%2,9 | -0,93 | 103 | %100 | -%1,4 | -0,40 |
| U1 | yakin | 66 | -%0,0 | -0,01 | +%3,7 | 1,37 | 103 | %82 | +%1,0 | 0,27 |
| U1 | fark (dusmus - yakin) | 66 | -%2,6 | -0,56 | — | — | — | — | -%2,4 | -0,51 |
| U2 | dusmus | 66 | +%4,3 | 1,91 | +%4,1 | 1,83 | 187 | %101 | +%5,5 | 2,46 |
| U2 | yakin | 66 | +%6,5 | 2,06 | +%8,0 | 3,11 | 187 | %82 | +%7,5 | 2,37 |
| U2 | fark (dusmus - yakin) | 66 | -%2,2 | -0,60 | — | — | — | — | -%2,0 | -0,54 |

## Bağımsız sağlama (ayrı, basit kod; K59'un panel / sinyal / bileşik / portföy fonksiyonları kullanılmadan)
Yalnız veri yükleyicileri ortaktır. Fiyat, uygunluk, sinyaller, sıra ortalaması, üst %10, maliyet ve kıyas baştan hesaplandı.

| Evren | Sinyal | Ay (K59 / bağımsız) | Yıllık net fazla: K59 | Bağımsız kod | Fark | Aylık net getiri en büyük mutlak fark |
|---|---|---|---|---|---|---|
| U2 | COMP4 | 66 / 66 | +%5,490 | +%5,491 | +0.02 bp | 1.29e-05 |
| U2 | DOSYA_Y | 64 / 64 | +%5,100 | +%5,100 | +0.00 bp | 0.00e+00 |

## Plasebo (U2, 200 rastgele sinyal)
Yanlış pozitif: maliyetli %0,0, maliyetsiz %1,5 (eşik %5) -> cetvel v2 GÜVENİLİR. Brüt NW t ortalaması -0,09, en büyüğü 3,19; brüt t(alfa) en büyüğü 3,29.

## Kapsam (sinyali olan uygun hisse sayısı)
| Evren | Sinyal | İlk ay (>= eşik) | Ortalama hisse (o aydan sonra) |
|---|---|---|---|
| U1 | S1 | 2016-06-30 | 1087 |
| U1 | S2 | 2016-05-31 | 1084 |
| U1 | S3 | 2016-05-31 | 1084 |
| U1 | S4 | 2021-02-26 | 1139 |
| U1 | S5 | 2021-02-26 | 910 |
| U1 | S6 | 2022-02-28 | 981 |
| U1 | S7 | 2020-12-31 | 940 |
| U1 | S8 | 2016-05-31 | 1084 |
| U1 | S9 | 2016-05-31 | 1084 |
| U1 | COMP4 | 2021-02-26 | 1034 |
| U1 | COMP9 | 2016-06-30 | 1087 |
| U1 | DOSYA_Y | 2021-04-30 | 867 |
| U1 | DOSYA_D | 2021-04-30 | 822 |
| U1 | DOSYA_YD | 2021-04-30 | 795 |
| U1 | X1 | 2021-04-30 | 935 |
| U1 | X2 | 2020-06-30 | 965 |
| U1 | X3 | 2016-05-31 | 1084 |
| U2 | S1 | 2021-01-29 | 2150 |
| U2 | S2 | 2020-12-31 | 2146 |
| U2 | S3 | 2020-12-31 | 1917 |
| U2 | S4 | 2021-02-26 | 1969 |
| U2 | S5 | 2021-02-26 | 1722 |
| U2 | S6 | 2022-02-28 | 1743 |
| U2 | S7 | 2020-12-31 | 1843 |
| U2 | S8 | 2020-12-31 | 2146 |
| U2 | S9 | 2020-12-31 | 2146 |
| U2 | COMP4 | 2021-02-26 | 1877 |
| U2 | COMP9 | 2020-12-31 | 2089 |
| U2 | DOSYA_Y | 2021-04-30 | 1710 |
| U2 | DOSYA_D | 2021-04-30 | 1669 |
| U2 | DOSYA_YD | 2021-04-30 | 1614 |
| U2 | X1 | 2021-04-30 | 1826 |
| U2 | X2 | 2020-12-31 | 1841 |
| U2 | X3 | 2020-12-31 | 2146 |
| BIST | S1 | 2016-06-30 | 424 |
| BIST | S2 | 2016-05-31 | 423 |
| BIST | S3 | 2016-05-31 | 423 |
| BIST | S8 | 2016-05-31 | 423 |
| BIST | S9 | 2016-05-31 | 423 |
| BIST | COMP9 | 2016-06-30 | 424 |
| BIST | X3 | 2016-05-31 | 423 |

## Koşu notları
- yok

## Sınırlar
- Üç evren de yalnız bugün yaşayan hisseler (hayatta kalma yanlılığı); kıyas aynı yanlılığı taşır, fark kısmen silinir.
- U1 ve U2 bağımsız değil (ortak hisseler, S4-S7 ve COMP4 iki evrende de 2021-2026): 'iki evrende tutar' bağımsız yineleme sayılmaz.
- Temel veri SEC frames'in son bildirilen değerleridir (sonradan düzeltme olabilir); bilgi tarihi özgün başvuru günüdür.
- U1'de fiyat tabanı düzeltilmiş kapanışla, U2'de o günkü fiyatla uygulanır; S3 U1 / BIST'te işlem değeri, U2'de piyasa değeridir.
- Tutan sonuç İZ değildir; en fazla 'PORTFÖY-ADAY'.

## COMP4 tutmazsa önceden yazılı sıradaki üç deneme (koşulmadı; ana oturum karar verir)
- (a) yalnız küçük-orta hisseler (her ay uygun evrenin boyut medyanının altı), aynı sinyaller ve cetvel.
- (b) 3 ay tutma, örtüşen portföyler (her ay üçte biri yenilenir), aynı sinyaller ve cetvel.
- (c) French veri kütüphanesinde 2000-2026 momentum + kârlılık bileşiğinin yinelemesi (hayatta kalma yanlılığı yok).

## IZ_KARNE önerisi: Ç152 için kayıt metni (kaydı ana oturum işler)
```
_ik_k("Ç152", "2026-11-11", "K59 BASİT SİNYALLER: dokuz sürekli sinyal + önceden yazılı COMP4 bileşiği + DOSYA ailesi (YEOTK / DGXX mantığı) + UCUZLUK koşullu testi, aylık üst %10 portföy, portföy cetveli v2 (K58 C + beta düzeltmeli alfa), ABD iki evren + BIST bilgi", "K59.py, test_k59.py", "Basit, nedeni bilinen sürekli sinyaller ve sıra ortalaması bileşiği maliyetten sonra evreni geçiyor mu?", "Ön kayıt K59_ON_KAYIT.md (mühür 6fe8bb385667, ölçümden önce git kaydına işlendi); eşikler değişmedi", "", 0, cikti="arastirma_cikti/k59_basit_sinyaller/ (K59_ON_KAYIT.md, K59_RAPOR.md, sinyal_sonuc.csv, aylik_getiri.csv, plasebo.csv, kapsam.csv, ucuzluk.csv)", notu="Karar: TUTMAZ (U1 TUTMAZ, U2 TUTMAZ); cetvel v2 GÜVENİLİR (plasebo yanlış pozitif net %0,0, brüt %1,5); U1 COMP4 yıllık fazla -%1,6, NW t -0,49, t(alfa) 0,16, TUTMAZ; U2 COMP4 yıllık fazla +%5,5, NW t 2,30, t(alfa) 2,87, TUTMAZ. DOSYA ailesi: U1 DOSYA_Y TUTMAZ; U2 DOSYA_Y TUTMAZ; U1 DOSYA_D TUTMAZ; U2 DOSYA_D TUTMAZ; U1 DOSYA_YD TUTMAZ; U2 DOSYA_YD TUTMAZ. İZ ilan edilemez (standart değişikliği Cemal'in kararı); seviye 0."),
```
