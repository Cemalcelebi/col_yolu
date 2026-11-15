# BofA alım listesi izi — sonuç (13 Kasım 2026)

## Düzeltme sonrası (ana model denetimi 13.11.2026)

Bu rapor, BofA liste verisi yeniden ayrıştırıldıktan sonra AYNI ön kayıt, aynı eşikler ve aynı tanımlarla yeniden koşuldu. Sapma gerekçesi: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi. Düzeltilenler: çok kurumlu haberlerde her tablonun kurumu tablodan önceki başlık / cümleden okunur (belirsiz -> BİLİNMİYOR, ölçüme girmez); hisse sütunundaki kurum adı satırları ('HSBC: -433 mn') düşer; aylık / dönemsel özet haberleri tur='aylik' / 'donemsel' (kapsam dışı); sayfada biriken günlük güncellemeler ('GÜNCELLEME 30 EYLÜL') kendi tarihini taşır (Eylül listesi Haziran tarihli sayılmaz); numaralı tek satırlık tablolar tek liste; haber sitelerinin ilgili haber kuşağı gövde dışı (kenar kuşağından 'SSAAT 56 TL' gibi satırlar BofA listesi sayılmaz). Liste mührü 7020587fbc90 -> 28014e1a3be8.

**KARAR: DEĞİŞMEDİ** — eski: ana kanıt yok / ikincil kanıt yok; yeni: ana kanıt yok / ikincil kanıt yok. Eski rapor ve JSON: /home/user/col_yolu/arastirma_cikti/bofa_izi/eski_v1.

| satır | ESKİ | YENİ |
|---|---|---|
| ANA (tutma dönemi) | n 1751, eşli fark +0,6% [-0,6%, +2,0%], sıra 0.51, portföy 3.10 / %90 5.20 | n 1789, eşli fark +0,6% [-0,5%, +1,9%], sıra 0.51, portföy 1.36 / %90 3.04 |
| yalnız lot sıralı | n 79, eşli fark -6,4% [-23,9%, +8,9%], sıra 0.50, portföy 1.49 / %90 2.92 | n 131, eşli fark +2,4% [-6,3%, +11,4%], sıra 0.54, portföy 2.00 / %90 2.59 |
| yalnız TL sıralı | n 1674, eşli fark +0,5% [-0,4%, +1,6%], sıra 0.51, portföy 1.16 / %90 3.18 | n 1667, eşli fark +0,3% [-0,6%, +1,4%], sıra 0.51, portföy 2.10 / %90 3.95 |
| düz yazı hariç | n 1623, eşli fark +0,7% [-0,5%, +2,1%], sıra 0.51, portföy 1.56 / %90 3.88 | n 1673, eşli fark +0,8% [-0,3%, +2,1%], sıra 0.51, portföy 3.03 / %90 3.49 |
| HSBC | n 586, eşli fark -2,1% [-4,2%, -0,1%], sıra 0.53, portföy 1.85 / %90 3.97, karar: kanıt yok | n 618, eşli fark -2,7% [-4,9%, -0,6%], sıra 0.53, portföy 1.14 / %90 3.11, karar: kanıt yok |
| TOPLU | n 2632, eşli fark -0,0% [-0,8%, +1,0%], sıra 0.51, portföy 1.71 / %90 4.46, karar: kanıt yok | n 2706, eşli fark -0,1% [-0,8%, +0,7%], sıra 0.51, portföy 1.94 / %90 6.04, karar: kanıt yok |
| Deutsche | n 11, eşli fark -35,5% [-53,7%, -13,6%], sıra 0.48, portföy 0.00 / %90 1.59, karar: kanıt yok | n 11, eşli fark -35,5% [-53,7%, -13,6%], sıra 0.48, portföy 0.00 / %90 1.59, karar: kanıt yok |
| ikincil 60 gün alım ilk 3 | n 411, eşli fark -0,8% [-3,8%, +2,3%], sıra 0.52, portföy 1.98 / %90 2.99 | n 411, eşli fark -0,6% [-3,6%, +2,4%], sıra 0.52, portföy 1.15 / %90 3.00 |
| 60 gün alım ilk 1 | n 196, eşli fark -1,6% [-5,4%, +2,6%], sıra 0.53, portföy 1.53 / %90 3.73 | n 198, eşli fark -1,6% [-5,3%, +2,6%], sıra 0.53, portföy 1.42 / %90 3.87 |
| 60 gün satış ilk 3 (ters) | n 403, eşli fark -0,8% [-3,3%, +1,7%], sıra 0.54, portföy 1.32 / %90 2.82 | n 402, eşli fark -0,7% [-3,3%, +1,8%], sıra 0.54, portföy 1.08 / %90 3.29 |
| liste haberi | 2774 | 2772 |
| dönem toplamı | 2099 | 2144 |
| ana A yarısı eşli fark | -0,6% | -0,5% |
| ana B yarısı eşli fark | +1,6% | +1,6% |
| BH ile reddedilen kod | 4 | 4 |

Soru: BofA (AKD kodu) alım listesinde ilk 3'te görünen BIST hissesi, BofA tutarken ve 60 gün içinde benzer hisselerden iyi gidiyor mu? Veri: 2772 BofA liste haberi, veri günleri 2023-04-17 – 2026-11-13 (896 işlem günü; 17 günde alım listesi yok). Fon krizi kuralı: çıkışı / penceresi 31.08.2026'yı aşan ana sonuca girmez.

**KARAR (ana, tutma dönemi): kanıt yok** — tutmayan: bootstrap alt uç <= 0; iki alt dönem aynı yönde (> 0) değil

**İkincil (FI_OLCUT 60 gün, alım ilk 3): kanıt yok** — tutmayan: ortalama eşli fark <= 0; alt uç <= 0; portföy rastgele %90'ı geçmedi; iki alt dönem aynı yönde (> 0) değil

## Özet (düz dil)

- BofA alım listesinde ilk 3'e giren hisse, BofA satış listesinde ilk 5'e girene kadar (medyan 3,00 işlem günü) benzer hisselerden ortalama +0,6% [-0,5%, +1,9%] ayrıştı (n 1789); 2023-24'te -0,5%, 2025-26'da +1,6%. Fark sıfırdan ayrılmıyor.
- 60 gün (FI_OLCUT): alım ilk 3 eşli fark -0,6% [-3,6%, +2,4%] (n 411); 20 günde +%50'ye dokunma %4 (eşlerin 1,16 katı), -%30'a dokunma %3 (1,12 kat).
- Lot sıralı listeler (PEKGY tipi kuruş hisseler, çoğu hisse.net): 60 günde eşli fark -6,1% [-10,3%, -0,7%] (n 84); tutma döneminde +2,4% [-6,3%, +11,4%] (n 131). İşaret ters: bu listelerde öne çıkan hisse benzerlerinden kötü gitmiş.
- Çökmüş hisse (250 gün tepesinden -%60): 60 gün eşli fark -18,5% [-39,1%, +1,1%] (n 11), 20 günde -%30'a dokunma %27 (8,88 kat). Örneklem küçük.
- Ters sınama (satış ilk 3): 60 gün eşli fark -0,7% [-3,3%, +1,8%]: satış listesi de bir şey söylemiyor.
- Öteki yabancı kodlar: HSBC tutma dönemi -2,7% [-4,9%, -0,6%] (n 618); bütün kodlar birlikte -0,1% [-0,8%, +0,7%] (n 2706). Citi, Deutsche, JPM, Goldman, UBS, Merrill, MS, Barclays, CS: arşivde liste yok ya da n < 30.
- Kriz dönemi (Eylül-Kasım 2026, BİLGİ): 217 BofA dönemi, 35 hâlâ açık; ortalama dönem getirisi -3,4%, eşli fark -0,1%.
- En erken: gün içi BofA listesi medyan 13:33'te (veri saati ~12:30-13:00), gün sonu listesi medyan 19:14'da yayımlanıyor; ücretsiz kaynakla en erken işlem gün içi haberle aynı gün kapanışta ya da ertesi açılışta mümkün.

## 1. BofA tutma dönemi (giriş: alım ilk 3 haberinden sonraki açılış; çıkış: satış ilk 5 haberinden sonraki açılış)

| satır | n | süre medyan (gün) | dönem getirisi ort. | eş ort. | eşli fark ort. [%95] | sıra | P(getiri >= +%50) | P(-%30 dokunma) | portföy / rastgele %90 | A / B fark |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA | 1789 | 3,00 | +2,4% | +1,9% | +0,6% [-0,5%, +1,9%] | 0,51 | %1 | %2 | +136% / +304% | -0,5% / +1,6% |
| çıkış: satış ilk 3, 2 ardışık | 517 | 20,00 | +14,4% | +11,2% | +3,2% [-3,5%, +11,6%] | 0,51 | %8 | %11 | +91% / +339% | +2,5% / +3,7% |
| yalnız lot sıralı listeler | 131 | 18,00 | +16,2% | +13,8% | +2,4% [-6,3%, +11,4%] | 0,54 | %12 | %10 | +200% / +259% | +32,0% / -2,6% |
| yalnız TL sıralı listeler | 1667 | 3,00 | +2,1% | +1,8% | +0,3% [-0,6%, +1,4%] | 0,51 | %1 | %2 | +210% / +395% | -0,6% / +1,2% |
| düz yazı hariç | 1673 | 3,00 | +2,7% | +1,9% | +0,8% [-0,3%, +2,1%] | 0,51 | %1 | %2 | +303% / +349% | -0,5% / +1,8% |
| ana: çökmüş (<= -%60) | 33 | 13,00 | -1,1% | +5,4% | -6,5% [-20,5%, +5,7%] | 0,48 | %3 | %24 | -4% / +43% | -3,2% / -7,6% |
| ana: diğer | 1741 | 3,00 | +2,5% | +1,8% | +0,7% [-0,4%, +2,1%] | 0,51 | %1 | %2 | +320% / +361% | -0,5% / +1,8% |
| ana: yalnız satışla kapanan | 1775 | 3,00 | +2,5% | +1,6% | +0,9% [-0,2%, +2,2%] | 0,51 | %1 | %2 | +161% / +456% | -0,2% / +1,9% |

Ana: toplam 2144 dönem; kesik içinde biten 1789; kesiği aşan 66, kriz sonrası açılan 217. Kapanış nedeni: {'satis': 1775, 'satis_gorulmedi_250': 14}. Süre (gün) %10/25/50/75/90: [1.0, 1.0, 3.0, 7.0, 19.0]. Giriş günü hacmi 0 olan (bayat fiyat) dönem: 16. Geç kalma (bizim giriş / BofA maliyeti - 1) medyan +0,6% (n 53). Dönem içi ort. en yüksek +8,8%, en düşük -4,7%.

FI_OLCUT dönem kırılımı (BİLGİ): tutma dönemi 2023: n 386, eşli fark -0,4% [-1,5%, +0,7%]; tutma dönemi 2024-26: n 1403, eşli fark +0,8% [-0,6%, +2,5%] | 60 gün 2023: n 101, eşli fark -4,8% [-10,4%, -0,1%]; 60 gün 2024-26: n 310, eşli fark +0,7% [-2,9%, +4,5%].

## 2. Olasılık tablosu (ikincil, 60 gün ölçütü; 20 gün olasılıkları dokunma, eş = aynı gün aynı hücre)

| olay | n (20g) | P(+%50, 20g) | kat | P(-%30, 20g) | kat | r20 ort. / eş | n (60g) | 60g eşli fark [%95] | sıra | portföy / rastgele %90 |
|---|---|---|---|---|---|---|---|---|---|---|
| alım ilk 3 (ana) | 458 | %4 | 1,16 | %3 | 1,12 | +2,6% / +2,1% | 411 | -0,6% [-3,6%, +2,4%] | 0,52 | +115% / +300% |
| alım ilk 1 | 215 | %1 | 0,25 | %1 | 0,53 | +1,2% / +2,7% | 198 | -1,6% [-5,3%, +2,6%] | 0,53 | +142% / +387% |
| alım ilk 5 | 653 | %5 | 1,31 | %3 | 0,92 | +3,1% / +1,7% | 589 | +2,3% [-0,9%, +5,9%] | 0,53 | +331% / +283% |
| ardışık 2+ gün ilk 3 | 126 | %0 | 0,00 | %1 | 0,40 | +1,7% / +2,7% | 117 | -0,5% [-4,7%, +3,8%] | 0,55 | +127% / +224% |
| alım ilk 3, çökmüş | 11 | %0 | 0,00 | %27 | 8,88 | -4,4% / +1,1% | 11 | -18,5% [-39,1%, +1,1%] | 0,36 | -15% / +15% |
| alım ilk 3, diğer | 416 | %4 | 1,03 | %2 | 0,75 | +2,8% / +2,0% | 393 | -0,0% [-3,3%, +3,4%] | 0,53 | +152% / +358% |
| SATIŞ ilk 3 (ters) | 444 | %3 | 0,78 | %3 | 1,03 | +2,5% / +3,1% | 402 | -0,7% [-3,3%, +1,8%] | 0,54 | +108% / +329% |
| lot listesi alım ilk 3 | 117 | %5 | 0,92 | %3 | 0,95 | +1,3% / +3,0% | 84 | -6,1% [-10,3%, -0,7%] | 0,45 | +53% / +187% |
| TL listesi alım ilk 3 | 454 | %4 | 1,09 | %3 | 0,99 | +2,9% / +2,1% | 407 | -0,1% [-3,5%, +3,6%] | 0,52 | +219% / +332% |
| haftalık alım ilk 3 (bilgi) | 238 | %0 | 0,13 | %3 | 0,89 | +1,4% / +1,5% | 211 | +3,7% [-3,1%, +14,2%] | 0,53 | +151% / +310% |

## 2b. Yabancı kodlar, aynı tutma dönemi ölçüsü (BH q = 0,10, m = 4)

| kod | birim | liste haberi | n dönem | süre medyan | getiri medyan / ort. | P(>= +%50) | P(-%30) | eşli fark [%95] | p | BH | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Barclays |  | 0 | veri yok | | | | | | | | |
| BofA | hepsi | 2772 | 1789 | 3,00 | -0,0% / +2,4% | %1 | %2 | +0,6% [-0,5%, +1,9%] | 0,18 | yok | kanıt yok |
| CS | hepsi | 0 | dönem yok | | | | | | | | |
| Citi | hepsi | 11 | 3 | 250,00 | -25,0% / -18,2% | %0 | %33 | -67,0% [—, —] | — | yok | kanıt yok |
| Deutsche | hepsi | 98 | 11 | 250,00 | -0,1% / +0,1% | %0 | %0 | -35,5% [-53,7%, -13,6%] | 1,00 | yok | kanıt yok |
| Goldman |  | 0 | veri yok | | | | | | | | |
| HSBC | hepsi | 1084 | 618 | 10,00 | +0,6% / +3,6% | %3 | %5 | -2,7% [-4,9%, -0,6%] | 0,99 | yok | kanıt yok |
| JPM |  | 0 | veri yok | | | | | | | | |
| MS |  | 0 | veri yok | | | | | | | | |
| Merrill | hepsi | 1 | 0 | — | — / — | — | — | — [—, —] | — | yok | kanıt yok |
| TOPLU | hepsi | 3960 | 2706 | 3,00 | +0,1% / +2,0% | %1 | %2 | -0,1% [-0,8%, +0,7%] | 0,55 | — | kanıt yok |
| UBS | hepsi | 1 | dönem yok | | | | | | | | |

Kriz dönemi AÇIK dönemler (kod hâlâ satış listesinde ilk 5'te göstermedi; bugüne getiri):

| kod | hisse | ilk alım haberi | giriş | bugüne | en düşük | BIST aynı gün -> bugün |
|---|---|---|---|---|---|---|
| BofA | BLCYT | 2026-09-03 15:00 | 2026-09-04 | -37,6% | -45,7% | -31,0% |
| BofA | TERA | 2026-09-15 19:38 | 2026-09-16 | -95,3% | -95,3% | -29,8% |
| BofA | BIGCH | 2026-09-15 18:20 | 2026-09-16 | -50,1% | -55,3% | -29,8% |
| BofA | DAPGM | 2026-09-21 18:30 | 2026-09-22 | -41,9% | -61,9% | -18,0% |
| BofA | SARAE | 2026-09-24 18:30 | 2026-09-25 | -6,3% | -42,0% | -15,8% |
| BofA | BALSU | 2026-10-01 12:36 | 2026-10-02 | -11,2% | -13,4% | -11,5% |
| BofA | PSGYO | 2026-10-01 12:36 | 2026-10-02 | -8,8% | -42,7% | -11,5% |
| BofA | MGROS | 2026-10-02 12:31 | 2026-10-05 | -7,6% | -20,8% | -12,6% |
| BofA | SKBNK | 2026-10-05 12:33 | 2026-10-06 | -25,2% | -45,5% | -12,6% |
| BofA | AEFES | 2026-10-06 12:43 | 2026-10-07 | -12,2% | -18,4% | -12,8% |
| BofA | ETYAT | 2026-10-16 10:50 | 2026-10-19 | -42,9% | -43,3% | -4,6% |
| BofA | DAGI | 2026-10-16 10:50 | 2026-10-19 | +0,8% | -15,3% | -4,6% |
| BofA | ODINE | 2026-10-20 12:31 | 2026-10-21 | -9,3% | -43,7% | -1,9% |
| BofA | ZOREN | 2026-10-21 19:37 | 2026-10-22 | +2,7% | -29,5% | +2,9% |
| BofA | KRDMA | 2026-10-22 11:46 | 2026-10-23 | -6,8% | -12,7% | +6,3% |
| … 55 daha (bofa_sonuc.json 'kurum' / 'kriz_acik') | | | | | | |

BİLGİ (gün içi listede aynı gün kapanıştan giriş, n 2): r5 +9,3%, r20 +9,1%, r60 +38,2% (aynı olayların ertesi açılış r60'ı +34,9%).

## 3. Kriz dönemi (giriş >= 01.09.2026; BİLGİ, karara girmez)

217 dönem (35 hâlâ açık: BofA satış listesinde ilk 5'te görülmedi). Ort. dönem getirisi -3,4% (medyan -1,0%), eş ort. -3,3%, eşli fark -0,1%; P(-%30 dokunma) %8, P(>= +%50) %1. Son veri 2026-11-13 (son bar gün içi olabilir).

| hisse | ilk alım haberi | sıra | BofA maliyet | giriş | çıkış / durum | dönem getirisi | eş | en düşük | en yüksek | bugüne | BIST aynı gün -> bugün |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KTLEV | 2026-09-04 12:40 (gun_ici) | 3 | — | 2026-09-07 | 2026-09-14 (satis) | -19,9% | +2,9% | -26,4% | +6,8% | -82,5% | -31,7% |
| TEHOL | 2026-09-08 12:03 (gun_ici) | 3 | — | 2026-09-09 | 2026-09-15 (satis) | +3,6% | -1,2% | -4,8% | +8,4% | -96,1% | -33,1% |
| PEKGY | 2026-09-08 15:00 (gun_ici) | 3 | 10,78 | 2026-09-09 | 2026-09-11 (satis) | +16,8% | -0,5% | +0,0% | +13,5% | -85,6% | -33,1% |
| TEHOL | 2026-09-15 12:35 (gun_ici) | 2 | — | 2026-09-16 | 2026-11-06 (satis) | -97,5% | -38,5% | -97,6% | +0,5% | -96,2% | -29,8% |
| PAHOL | 2026-09-15 12:00 (gun_ici) | 2 | 1,32 | 2026-09-16 | 2026-10-05 (satis) | -29,2% | -17,9% | -36,9% | +0,0% | -36,2% | -29,8% |
| KTLEV | 2026-10-01 18:33 (gun_sonu) | 2 | 10,39 | 2026-10-02 | 2026-10-14 (satis) | -24,9% | -8,9% | -37,9% | +1,1% | -25,8% | -11,5% |
| PAHOL | 2026-10-07 19:32 (gun_sonu) | 3 | 0,93 | 2026-10-08 | 2026-10-09 (satis) | +8,8% | +1,0% | -3,3% | +9,9% | -8,8% | -11,0% |
| PEKGY | 2026-10-16 19:49 (gun_sonu) | 3 | 1,09 | 2026-10-19 | 2026-10-26 (satis) | -33,1% | -26,1% | -40,4% | +6,6% | +11,0% | -4,6% |
| ODINE | 2026-10-20 12:31 (gun_ici) | 2 | — | 2026-10-21 | AÇIK (BofA tutuyor) | -12,9% | -8,8% | -43,7% | +29,1% | -9,3% | -1,9% |
| PEKGY | 2026-10-27 12:11 (gun_ici) | 1 | 0,83 | 2026-10-28 | 2026-11-12 (satis) | +48,8% | +17,5% | -23,3% | +46,5% | +75,6% | +9,2% |
| PAHOL | 2026-10-27 12:11 (gun_ici) | 3 | 0,87 | 2026-10-28 | 2026-11-06 (satis) | +0,0% | +3,3% | -18,2% | +7,8% | +7,8% | +9,2% |
| KTLEV | 2026-10-27 12:46 (gun_ici) | 1 | — | 2026-10-28 | 2026-11-03 (satis) | -22,2% | -8,8% | -20,5% | +0,2% | +76,8% | +9,2% |
| KTLEV | 2026-11-03 19:24 (gun_sonu) | 2 | — | 2026-11-04 | 2026-11-11 (satis) | +63,0% | +20,8% | -0,3% | +48,4% | +97,1% | +11,0% |
| PAHOL | 2026-11-06 12:19 (gun_ici) | 2 | 0,74 | 2026-11-09 | AÇIK (BofA tutuyor) | +3,8% | +0,6% | -2,6% | +6,4% | +6,4% | +2,5% |
| KARCL | 2026-11-10 14:23 (gun_ici) | 1 | — | 2026-11-11 | AÇIK (BofA tutuyor) | +17,6% | +9,1% | -5,0% | +9,9% | +20,9% | +1,3% |
| … 202 dönem daha (bofa_sonuc.json 'kriz') | | | | | | | | | | | |

## 4. En erken bilgi (hafta içi yayın saatleri, TR)

- gün içi liste: n 371, en erken 10:01, %10 12:24, medyan 13:33, %90 16:53.
- gün sonu liste: n 1850, en erken 00:38, %10 18:12, medyan 19:14, %90 20:46.
- haftalık: n 29, en erken 08:52, %10 12:34, medyan 19:16, %90 21:02.
- Gün içi listenin veri saati: medyan 12:46 (en erken 10:10); yayın gecikmesi medyan 19,32 dk (%10 0,83, %90 71,32).
- Ücretsiz en erken yol: hisse.net Google News site haritası (sitemaps/news-sitemap.xml; son ~100 haber, yayın dakikasıyla; hisse.net'te RSS yok, /rss 404). Rota Borsa'nın RSS'i var (rotaborsa.com/feed/), YatırımX'in yok. `BOFA_IZI.bi_izle_tur` hisse.net haritasını tek tur çeker, dakikada en çok 1 istek; zamanlanmadı. Ücretli AKD (ForInvest, Matriks) seans içinde canlıdır; abonelik başlatılmadı.

## 5. Sınırlar

AKD kodu kurum kimliği değildir (savcılık 'yabancı görünümlü yerli işlem' inceliyor). Arşiv haber sitesinin seçtiği günlerdir (her gün liste yok; eksik günler sayılır). Liste ilk 5 ile sınırlı: 'ilk 5'te görülmedi' satış olmadığı anlamına gelmez. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı yukarı). İşlem maliyeti yok.

Arşiv haber sitelerinin yazdığı listelerdir (2023-04-17 öncesi yok; liste çoğunlukla ilk 5 / ilk 10). Tek pazar (BIST): FI_OLCUT'un ABD / Avrupa karar hücreleri bu veride yoktur. Ana dışındaki satırlar çoklu denemedir.

Mühür 6b544f940e23; kapı {"commit": "b7943a196d6569b7a84132d4a3f8802c14853116", "commit_zamani": "2026-11-13T15:49:22+00:00"}; SAPMA: AYRIŞTIRMA DÜZELTMESİ (ana model denetimi 13.11): çok kurumlu haberlerde kurum etiketi, kurum adı hisse satırları, aylık özet haberleri; eşikler değişmedi.
