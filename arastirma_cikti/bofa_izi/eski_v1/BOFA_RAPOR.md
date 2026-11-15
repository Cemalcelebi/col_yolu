# BofA alım listesi izi — sonuç (13 Kasım 2026)

Soru: BofA (AKD kodu) alım listesinde ilk 3'te görünen BIST hissesi, BofA tutarken ve 60 gün içinde benzer hisselerden iyi gidiyor mu? Veri: 2774 BofA liste haberi, veri günleri 2023-04-17 – 2026-11-13 (896 işlem günü; 17 günde alım listesi yok). Fon krizi kuralı: çıkışı / penceresi 31.08.2026'yı aşan ana sonuca girmez.

**KARAR (ana, tutma dönemi): kanıt yok** — tutmayan: bootstrap alt uç <= 0; iki alt dönem aynı yönde (> 0) değil

**İkincil (FI_OLCUT 60 gün, alım ilk 3): kanıt yok** — tutmayan: ortalama eşli fark <= 0; alt uç <= 0; portföy rastgele %90'ı geçmedi; iki alt dönem aynı yönde (> 0) değil

## Özet (düz dil)

- BofA alım listesinde ilk 3'e giren hisse, BofA satış listesinde ilk 5'e girene kadar (medyan 3,00 işlem günü) benzer hisselerden ortalama +0,6% [-0,6%, +2,0%] ayrıştı (n 1751); 2023-24'te -0,6%, 2025-26'da +1,6%. Fark sıfırdan ayrılmıyor.
- 60 gün (FI_OLCUT): alım ilk 3 eşli fark -0,8% [-3,8%, +2,3%] (n 411); 20 günde +%50'ye dokunma %4 (eşlerin 1,16 katı), -%30'a dokunma %3 (1,13 kat).
- Lot sıralı listeler (PEKGY tipi kuruş hisseler, çoğu hisse.net): 60 günde eşli fark -10,3% [-15,0%, -5,2%] (n 76); tutma döneminde -6,4% [-23,9%, +8,9%] (n 79). İşaret ters: bu listelerde öne çıkan hisse benzerlerinden kötü gitmiş.
- Çökmüş hisse (250 gün tepesinden -%60): 60 gün eşli fark -18,5% [-39,1%, +1,1%] (n 11), 20 günde -%30'a dokunma %27 (8,88 kat). Örneklem küçük.
- Ters sınama (satış ilk 3): 60 gün eşli fark -0,8% [-3,3%, +1,7%]: satış listesi de bir şey söylemiyor.
- Öteki yabancı kodlar: HSBC tutma dönemi -2,1% [-4,2%, -0,1%] (n 586); bütün kodlar birlikte -0,0% [-0,8%, +1,0%] (n 2632). Citi, Deutsche, JPM, Goldman, UBS, Merrill, MS, Barclays, CS: arşivde liste yok ya da n < 30.
- Kriz dönemi (Eylül-Kasım 2026, BİLGİ): 197 BofA dönemi, 34 hâlâ açık; ortalama dönem getirisi -3,5%, eşli fark +0,4%.
- En erken: gün içi BofA listesi medyan 13:41'te (veri saati ~12:30-13:00), gün sonu listesi medyan 19:13'da yayımlanıyor; ücretsiz kaynakla en erken işlem gün içi haberle aynı gün kapanışta ya da ertesi açılışta mümkün.

## 1. BofA tutma dönemi (giriş: alım ilk 3 haberinden sonraki açılış; çıkış: satış ilk 5 haberinden sonraki açılış)

| satır | n | süre medyan (gün) | dönem getirisi ort. | eş ort. | eşli fark ort. [%95] | sıra | P(getiri >= +%50) | P(-%30 dokunma) | portföy / rastgele %90 | A / B fark |
|---|---|---|---|---|---|---|---|---|---|---|
| ANA | 1751 | 3,00 | +2,4% | +1,8% | +0,6% [-0,6%, +2,0%] | 0,51 | %1 | %2 | +310% / +520% | -0,6% / +1,6% |
| çıkış: satış ilk 3, 2 ardışık | 515 | 21,00 | +14,3% | +12,3% | +2,0% [-5,1%, +10,8%] | 0,52 | %8 | %11 | +96% / +311% | +2,3% / +1,8% |
| yalnız lot sıralı listeler | 79 | 60,00 | +18,8% | +25,2% | -6,4% [-23,9%, +8,9%] | 0,50 | %15 | %19 | +149% / +292% | +26,1% / -16,7% |
| yalnız TL sıralı listeler | 1674 | 3,00 | +2,2% | +1,7% | +0,5% [-0,4%, +1,6%] | 0,51 | %1 | %2 | +116% / +318% | -0,4% / +1,4% |
| düz yazı hariç | 1623 | 3,00 | +2,6% | +1,9% | +0,7% [-0,5%, +2,1%] | 0,51 | %1 | %2 | +156% / +388% | -0,5% / +1,8% |
| ana: çökmüş (<= -%60) | 23 | 24,00 | -2,9% | +8,8% | -11,8% [-29,1%, +4,8%] | 0,44 | %4 | %35 | -7% / +50% | -4,0% / -15,9% |
| ana: diğer | 1713 | 3,00 | +2,5% | +1,7% | +0,8% [-0,4%, +2,2%] | 0,51 | %1 | %2 | +364% / +464% | -0,5% / +2,0% |
| ana: yalnız satışla kapanan | 1736 | 3,00 | +2,5% | +1,6% | +0,9% [-0,2%, +2,4%] | 0,51 | %1 | %2 | +344% / +456% | -0,2% / +1,9% |

Ana: toplam 2099 dönem; kesik içinde biten 1751; kesiği aşan 65, kriz sonrası açılan 197. Kapanış nedeni: {'satis': 1736, 'satis_gorulmedi_250': 15}. Süre (gün) %10/25/50/75/90: [1.0, 1.0, 3.0, 7.0, 18.0]. Giriş günü hacmi 0 olan (bayat fiyat) dönem: 18. Geç kalma (bizim giriş / BofA maliyeti - 1) medyan +0,3% (n 30). Dönem içi ort. en yüksek +8,9%, en düşük -4,7%.

FI_OLCUT dönem kırılımı (BİLGİ): tutma dönemi 2023: n 387, eşli fark -0,4% [-1,5%, +0,7%]; tutma dönemi 2024-26: n 1364, eşli fark +0,9% [-0,7%, +2,8%] | 60 gün 2023: n 101, eşli fark -4,8% [-10,4%, -0,1%]; 60 gün 2024-26: n 310, eşli fark +0,5% [-3,1%, +4,2%].

## 2. Olasılık tablosu (ikincil, 60 gün ölçütü; 20 gün olasılıkları dokunma, eş = aynı gün aynı hücre)

| olay | n (20g) | P(+%50, 20g) | kat | P(-%30, 20g) | kat | r20 ort. / eş | n (60g) | 60g eşli fark [%95] | sıra | portföy / rastgele %90 |
|---|---|---|---|---|---|---|---|---|---|---|
| alım ilk 3 (ana) | 458 | %4 | 1,16 | %3 | 1,13 | +2,5% / +2,1% | 411 | -0,8% [-3,8%, +2,3%] | 0,52 | +198% / +299% |
| alım ilk 1 | 215 | %1 | 0,25 | %1 | 0,53 | +1,2% / +2,7% | 196 | -1,6% [-5,4%, +2,6%] | 0,53 | +153% / +373% |
| alım ilk 5 | 651 | %4 | 1,26 | %3 | 0,98 | +3,0% / +1,8% | 585 | +2,2% [-1,1%, +5,8%] | 0,52 | +119% / +254% |
| ardışık 2+ gün ilk 3 | 126 | %0 | 0,00 | %1 | 0,40 | +1,8% / +2,6% | 117 | -0,5% [-4,7%, +3,7%] | 0,55 | +127% / +233% |
| alım ilk 3, çökmüş | 11 | %0 | 0,00 | %27 | 8,88 | -4,4% / +1,1% | 11 | -18,5% [-39,1%, +1,1%] | 0,36 | -15% / +17% |
| alım ilk 3, diğer | 416 | %4 | 1,03 | %2 | 0,75 | +2,7% / +2,0% | 393 | -0,2% [-3,4%, +3,1%] | 0,52 | +292% / +348% |
| SATIŞ ilk 3 (ters) | 442 | %3 | 0,79 | %3 | 1,03 | +2,5% / +3,1% | 403 | -0,8% [-3,3%, +1,7%] | 0,54 | +132% / +282% |
| lot listesi alım ilk 3 | 88 | %3 | 0,53 | %6 | 1,52 | +1,0% / +5,3% | 76 | -10,3% [-15,0%, -5,2%] | 0,41 | +9% / +169% |
| TL listesi alım ilk 3 | 450 | %4 | 1,10 | %3 | 1,01 | +3,0% / +2,2% | 403 | -0,0% [-3,4%, +3,6%] | 0,53 | +157% / +325% |
| haftalık alım ilk 3 (bilgi) | 238 | %0 | 0,13 | %3 | 0,89 | +1,4% / +1,5% | 211 | +3,7% [-3,1%, +14,2%] | 0,53 | +147% / +296% |

## 2b. Yabancı kodlar, aynı tutma dönemi ölçüsü (BH q = 0,10, m = 4)

| kod | birim | liste haberi | n dönem | süre medyan | getiri medyan / ort. | P(>= +%50) | P(-%30) | eşli fark [%95] | p | BH | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Barclays |  | 0 | veri yok | | | | | | | | |
| BofA | hepsi | 2774 | 1751 | 3,00 | +0,0% / +2,4% | %1 | %2 | +0,6% [-0,6%, +2,0%] | 0,19 | yok | kanıt yok |
| CS | hepsi | 0 | dönem yok | | | | | | | | |
| Citi | hepsi | 12 | 3 | 250,00 | -25,0% / -18,2% | %0 | %33 | -67,0% [—, —] | — | yok | kanıt yok |
| Deutsche | hepsi | 104 | 11 | 250,00 | -0,1% / +0,1% | %0 | %0 | -35,5% [-53,7%, -13,6%] | 1,00 | yok | kanıt yok |
| Goldman | hepsi | 1 | dönem yok | | | | | | | | |
| HSBC | hepsi | 1026 | 586 | 10,00 | +0,7% / +3,8% | %3 | %5 | -2,1% [-4,2%, -0,1%] | 0,98 | yok | kanıt yok |
| JPM | hepsi | 1 | 0 | — | — / — | — | — | — [—, —] | — | yok | kanıt yok |
| MS |  | 0 | veri yok | | | | | | | | |
| Merrill | hepsi | 3 | 0 | — | — / — | — | — | — [—, —] | — | yok | kanıt yok |
| TOPLU | hepsi | 3918 | 2632 | 3,00 | +0,1% / +2,0% | %1 | %2 | -0,0% [-0,8%, +1,0%] | 0,50 | — | kanıt yok |
| UBS | hepsi | 1 | dönem yok | | | | | | | | |

Kriz dönemi AÇIK dönemler (kod hâlâ satış listesinde ilk 5'te göstermedi; bugüne getiri):

| kod | hisse | ilk alım haberi | giriş | bugüne | en düşük | BIST aynı gün -> bugün |
|---|---|---|---|---|---|---|
| BofA | ENTRA | 2026-09-09 19:37 | 2026-09-10 | +5,4% | -16,2% | -33,2% |
| BofA | TERA | 2026-09-15 19:38 | 2026-09-16 | -95,3% | -95,3% | -29,8% |
| BofA | BIGCH | 2026-09-15 18:20 | 2026-09-16 | -50,1% | -55,3% | -29,8% |
| BofA | DAPGM | 2026-10-01 12:36 | 2026-10-02 | -6,5% | -38,7% | -11,5% |
| BofA | BALSU | 2026-10-01 12:36 | 2026-10-02 | -11,2% | -13,4% | -11,5% |
| BofA | MGROS | 2026-10-02 12:31 | 2026-10-05 | -7,6% | -20,8% | -12,6% |
| BofA | NETGL | 2026-10-02 11:33 | 2026-10-05 | -17,9% | -42,3% | -12,6% |
| BofA | SELEC | 2026-10-02 11:33 | 2026-10-05 | +34,4% | -25,4% | -12,6% |
| BofA | SKBNK | 2026-10-05 12:33 | 2026-10-06 | -25,2% | -45,5% | -12,6% |
| BofA | AEFES | 2026-10-06 12:43 | 2026-10-07 | -12,2% | -18,4% | -12,8% |
| BofA | ETYAT | 2026-10-16 10:50 | 2026-10-19 | -42,9% | -43,3% | -4,6% |
| BofA | DAGI | 2026-10-16 10:50 | 2026-10-19 | +0,8% | -15,3% | -4,6% |
| BofA | ODINE | 2026-10-20 12:31 | 2026-10-21 | -9,3% | -43,7% | -1,9% |
| BofA | ZOREN | 2026-10-21 19:37 | 2026-10-22 | +2,7% | -29,5% | +2,9% |
| BofA | KRDMA | 2026-10-22 11:46 | 2026-10-23 | -6,8% | -12,7% | +6,3% |
| … 53 daha (bofa_sonuc.json 'kurum' / 'kriz_acik') | | | | | | |

BİLGİ (gün içi listede aynı gün kapanıştan giriş, n 2): r5 +9,3%, r20 +9,1%, r60 +38,2% (aynı olayların ertesi açılış r60'ı +34,9%).

## 3. Kriz dönemi (giriş >= 01.09.2026; BİLGİ, karara girmez)

197 dönem (34 hâlâ açık: BofA satış listesinde ilk 5'te görülmedi). Ort. dönem getirisi -3,5% (medyan -1,2%), eş ort. -3,7%, eşli fark +0,4%; P(-%30 dokunma) %7, P(>= +%50) %1. Son veri 2026-11-13 (son bar gün içi olabilir).

| hisse | ilk alım haberi | sıra | BofA maliyet | giriş | çıkış / durum | dönem getirisi | eş | en düşük | en yüksek | bugüne | BIST aynı gün -> bugün |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KTLEV | 2026-09-04 12:40 (gun_ici) | 3 | — | 2026-09-07 | 2026-09-14 (satis) | -19,9% | +2,9% | -26,4% | +6,8% | -82,5% | -31,7% |
| TEHOL | 2026-09-08 12:03 (gun_ici) | 3 | — | 2026-09-09 | 2026-09-15 (satis) | +3,6% | -1,2% | -4,8% | +8,4% | -96,1% | -33,1% |
| TEHOL | 2026-09-15 12:35 (gun_ici) | 2 | — | 2026-09-16 | 2026-11-06 (satis) | -97,5% | -38,5% | -97,6% | +0,5% | -96,2% | -29,8% |
| KTLEV | 2026-10-01 18:33 (gun_sonu) | 2 | 10,39 | 2026-10-02 | 2026-10-14 (satis) | -24,9% | -8,9% | -37,9% | +1,1% | -25,8% | -11,5% |
| PAHOL | 2026-10-07 19:32 (gun_sonu) | 3 | 0,93 | 2026-10-08 | 2026-10-09 (satis) | +8,8% | +1,0% | -3,3% | +9,9% | -8,8% | -11,0% |
| PEKGY | 2026-10-16 19:49 (gun_sonu) | 3 | 1,09 | 2026-10-19 | 2026-10-26 (satis) | -33,1% | -26,1% | -40,4% | +6,6% | +11,0% | -4,6% |
| ODINE | 2026-10-20 12:31 (gun_ici) | 2 | — | 2026-10-21 | AÇIK (BofA tutuyor) | -12,9% | -8,8% | -43,7% | +29,1% | -9,3% | -1,9% |
| KTLEV | 2026-10-27 12:46 (gun_ici) | 1 | — | 2026-10-28 | 2026-11-03 (satis) | -22,2% | -8,8% | -20,5% | +0,2% | +76,8% | +9,2% |
| PAHOL | 2026-10-27 12:11 (gun_ici) | 3 | 0,87 | 2026-10-28 | 2026-11-06 (satis) | +0,0% | +3,3% | -18,2% | +7,8% | +7,8% | +9,2% |
| PEKGY | 2026-10-27 12:11 (gun_ici) | 1 | 0,83 | 2026-10-28 | 2026-11-12 (satis) | +48,8% | +17,5% | -23,3% | +46,5% | +75,6% | +9,2% |
| KTLEV | 2026-11-03 19:24 (gun_sonu) | 2 | — | 2026-11-04 | 2026-11-11 (satis) | +63,0% | +20,8% | -0,3% | +48,4% | +97,1% | +11,0% |
| PAHOL | 2026-11-06 12:19 (gun_ici) | 2 | 0,74 | 2026-11-09 | AÇIK (BofA tutuyor) | +3,8% | +0,6% | -2,6% | +6,4% | +6,4% | +2,5% |
| KARCL | 2026-11-10 14:23 (gun_ici) | 1 | — | 2026-11-11 | AÇIK (BofA tutuyor) | +17,6% | +9,1% | -5,0% | +9,9% | +20,9% | +1,3% |
| KTLEV | 2026-11-11 13:12 (gun_ici) | 2 | 6,06 | 2026-11-12 | AÇIK (BofA tutuyor) | +11,7% | +5,9% | -0,5% | +4,0% | +14,4% | +2,3% |
| TERA | 2026-08-31 12:30 (gun_ici) | 1 | — | 2026-09-01 | 2026-09-07 (satis) | +3,6% | -1,1% | -0,4% | +4,1% | -94,3% | -33,4% |
| … 182 dönem daha (bofa_sonuc.json 'kriz') | | | | | | | | | | | |

## 4. En erken bilgi (hafta içi yayın saatleri, TR)

- gün içi liste: n 424, en erken 09:30, %10 12:20, medyan 13:41, %90 17:13.
- gün sonu liste: n 1891, en erken 00:38, %10 18:12, medyan 19:13, %90 20:46.
- haftalık: n 30, en erken 08:52, %10 11:40, medyan 19:15, %90 21:01.
- Gün içi listenin veri saati: medyan 12:50 (en erken 10:10); yayın gecikmesi medyan 19,33 dk (%10 0,83, %90 72,69).
- Ücretsiz en erken yol: hisse.net Google News site haritası (sitemaps/news-sitemap.xml; son ~100 haber, yayın dakikasıyla; hisse.net'te RSS yok, /rss 404). Rota Borsa'nın RSS'i var (rotaborsa.com/feed/), YatırımX'in yok. `BOFA_IZI.bi_izle_tur` hisse.net haritasını tek tur çeker, dakikada en çok 1 istek; zamanlanmadı. Ücretli AKD (ForInvest, Matriks) seans içinde canlıdır; abonelik başlatılmadı.

## 5. Sınırlar

AKD kodu kurum kimliği değildir (savcılık 'yabancı görünümlü yerli işlem' inceliyor). Arşiv haber sitesinin seçtiği günlerdir (her gün liste yok; eksik günler sayılır). Liste ilk 5 ile sınırlı: 'ilk 5'te görülmedi' satış olmadığı anlamına gelmez. Fiyat evreni bugün işlem gören hisseler (hayatta kalma yanlılığı yukarı). İşlem maliyeti yok.

Arşiv haber sitelerinin yazdığı listelerdir (2023-04-17 öncesi yok; liste çoğunlukla ilk 5 / ilk 10). Tek pazar (BIST): FI_OLCUT'un ABD / Avrupa karar hücreleri bu veride yoktur. Ana dışındaki satırlar çoklu denemedir.

Mühür 6b544f940e23; kapı {"commit": "b7943a196d6569b7a84132d4a3f8802c14853116", "commit_zamani": "2026-11-13T15:49:22+00:00"}; SAPMA: Yalnız gösterim: giriş günü hacmi 0 (askı / bayat Yahoo fiyatı) olan dönemler kriz tablosunda işaretlenir ve ana dönemde sayılır (DUNYH 12.11 -%85 bayat fiyat). Eşik, tanım, örneklem ve karar değişmedi..
