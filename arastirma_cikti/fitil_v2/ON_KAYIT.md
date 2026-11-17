# FITIL_V2 — ÖN KAYIT (S+ v2 'TAM GİRİLİR')

FITIL_V2 v1.0 (2026-11-17): S+ v2 'TAM GİRİLİR' (şekil + savunma hattı + dönüm + yol almamış + tepede değil), ORTAK CETVEL v1.0 ile

- V2_ESIK_SHA: `78407c0d8463853f17afd2828af52f25357afa66709bc5adf5ca2a3e6cda0366` (V2_ESIK + V2_SECIM)
- V2_KOD_SHA: `376ee0544aea97133a67cb614a824d0e395f86ec778f94bbbebbfc6d8a7802fc`
- IS_TANIMI_SHA: `2a70e55ea41fa6d734d6ce89572086f3f99d884536bdde0c88dcb19f4f00b2be` (git 22d7e502c4, 2026-11-17T07:26:40+00:00)
- TASARIM_SHA: `51df22a41326bf05878bb930bcf2cfa42550961a6f82a717056e13b23130611a`
- KOR_ANAHTAR_SHA: `75ccc5f77c13150ef061578702ef6ce0ea1995458412c21d7b89142954b1401b`
- KOR_CEVAP_SHA: `a86b207b03f8660cb780f91b1e6bfb6458d979de9a1b662b56a1082538b88de8`
- SECIM_JSON: `{"dusus": 0.2, "duz": null, "hatTol": 0.02, "no": "N30", "sekil": "S+", "yol": 0.1}`
- ZAMAN (UTC): `2026-11-17 07:48:43 UTC`

Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı ve okunmadı (yalnız olay sayımı, getirisiz). `kos` kontrol listesi, cetvel üç sha'sı, V2_ESIK / kod / tasarım / iş tanımı sha'sı ve bu dosyanın git kaydı tutmazsa durur. Eşikler sonuç görülünce değişmez.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Tanım ve SEÇİLEN eşikler (tasarım sınaması, TASARIM.md)

- Bar: geçerli bar (OC.oc_veri temiz: O/H/L/C > 0, H > L, V > 0; FO.fo_bar ayrıca süzer); R = H - L; alt / üst fitil payı FO.fo_bar.
- Pencere: W = t dahil son 10 geçerli bar (rolling, yalnız t'ye kadar). ASIM = ort(üst) - ort(alt), ALTYOK = alt < 0,10 bar payı (FO.fo_pencere).
- Seçilen nokta: N30: şekil S+ (ASIM >= 0,20, ALTYOK >= 0,50), düz kapalı, hatTol 0,02, düşüş >= 0,2, yol <= 0,1.
- (1) ŞEKİL: ASIM >= 0.20 VE ALTYOK >= 0.50.
- (2) SAVUNMA HATTI: SAVUNMA HATTI: HAT = min(Low, W); düz = (max(Low, W) - HAT) / medyan(R, W) <= duz (kapalı ise şart yok); sağlam = min(Close, W) >= HAT x (1 - tol) (tanım gereği doğru) VE HAT >= min(Low, W'den önceki 30 geçerli bar) x (1 - tol) VE C_t >= HAT; duz = kapalı, tol = 0.02.
- (3) DÖNÜM: DÖNÜM: 1 - C_t / max(Close, W'den önceki 60 geçerli bar) >= dusus; dusus = 0.2.
- (4) YOL ALMAMIŞ: YOL ALMAMIŞ: C_t <= HAT x (1 + yol) VE C_t <= max(High, W \ {t}) (t HARİÇ önceki 9 pencere barının en yüksek High'ı: bugün pencere tepesini kapanışla kırmamış; SAPMA-1, ana model kararı 17 Kas); yol = 0.1.
- (5) TEPEDE DEĞİL: TEPEDE DEĞİL: C_t <= max(Close, t dahil son 120 geçerli bar) x (1 - 0,15).
- TAM GİRİLİR = (1) VE (2) VE (3) VE (4) VE (5); tanımsız ölçü (yetersiz geçmiş) = şart tutmaz.
- BAĞLAM: EK (Cemal, 17 Kas; ön kayıttan önce, sonuç görülmeden): KONUM = (C_t - min(Low, t dahil 250 geçerli bar)) / (max(High, 250) - min(Low, 250)); DİP = KONUM <= 0,25 VE C_t <= max(Close, 120 geçerli bar) x (1 - 0,15); TEPE = KONUM >= 0,75; ORTA = ikisi de değil (yolun ortası); 250 bar yoksa TANIMSIZ (hiçbir sınıfa girmez). Eşikler sabit, ızgaraya girmez.
- Çıkış bilgisi: HAT x 0,98 altı kapanış = STOP (K8); max(High, W) üstü kapanış = KIRILIM; t+1 .. t+60 geçerli barda hangisi önce.

Satırlar:

- TAM_DIP: TAM GİRİLİR VE bağlam DİP [ANA] (Cemal: 'dipte risk alınır, stop bellidir')
- TAM: TAM GİRİLİR = (1)-(5), bağlam fark etmez [bilgi]
- TAM_ORTA: TAM VE bağlam ORTA [bilgi] (Cemal: 'yolun ortasında güven olmaz')
- TAM_TEPE: TAM VE bağlam TEPE [bilgi]
- S1: (1) şekil tek başına (= Ç187 S+ seçilen şekil eşiğiyle) [bilgi]
- S12: (1) + (2) [bilgi]
- S123: (1) + (2) + (3) [bilgi]
- SM_TEPE: AYNA: bağlam TEPE VE S- (FITIL_OBEK ters öbek: ASIM <= -0,20 VE USTYOK >= 0,50) = 'ÇIK' [bilgi; kaçınma, beklenen yön -]

- Olay: DURUM GÜNLERİ: şartın t kapanışında doğru olduğu her geçerli bar OC.oc_olc'a verilir; giriş t'den sonraki ilk geçerli açılış; tekilleştirme 60 gün (cetvel: ilk durum günü tutulur).

## Karar kuralı (önceden yazılı)

- ANA: TAM_DIP satırı ORTAK CETVEL v1.0: hücre TUTAR = dört şart + iki yarı > 0 (oc_hucre); durum oc_hucre_durum; genel etiket FO.fo_etiket(+) = OC.oc_etiket ve cetvelin 'İZ DEĞİL'i 'DESTEKLENMEDİ' (Ç187 ile aynı): İZ (dört karar hücresi ABD / AVR x 2023 / 2024-26 TUTAR) / EMARE (en az biri) / ÖLÇÜLEMEDİ (güç yetersiz) / DESTEKLENMEDİ (güç yeterli, tutmadı). BIST bilgi; 2016-22 keşif bilgi.
- BİLGİ: TAM, TAM_ORTA, TAM_TEPE, S1, S12, S123 (beklenen yön +, cetvel TUTAR) ve SM_TEPE (beklenen yön -, AYNA kaçınma şartı FO.fo_kacinma: n >= 30, ort < 0 ve üst uç < 0, sıra < 0,50, portföy < p10, iki yarı < 0; etiket FO.fo_etiket(-)); 7 satır x 4 karar hücresi = 28 test; p = beklenen yönde ay kümeli bootstrap (FO.fo_p); Benjamini-Hochberg q 0,10; n < 30 hücre teste girmez.
- Olasılık: olasılık tablosu (P +%100 / -%50 eş ve taban katları, 250 gün) cetvelden aynen; etiket SEÇİCİ / PİYANGO / YOK.
- Kırılım / stop: bilgi: cetvel olaylarında (tekil) t+1 .. t+60 geçerli barda önce KIRILIM (C > max(High, W)) mı STOP (C < HAT x 0,98) mı; pazar x dönem payları; 60 bar yoksa ÖLÇÜLMEZ.
- Geleceğe bakma denetimi: kos: her pazarda rastgele 40 TAM_DIP durum gününde seri t'de kesilip ölçüler yeniden hesaplanır; TAM_DIP ve bağlam aynı olmalı; tutmazsa koşu DURUR.

## KÖR SET 2 (önceden yazılı)

- TAM grubu: kodun TAM_DIP (TAM GİRİLİR + bağlam DİP) dediği durum günlerinden rastgele (her hisse setin tamamında bir kez); DEĞİL grubu: (1) şekil VAR ama TAM_DIP YOK günlerinden rastgele (anahtarda düşüren şart ve bağlam); sayfa = t'de biten 10 mum + öncesi 120 mum (EK, Cemal 17 Kas: bağlam görünsün), sonrası yok, adsız, tarihsiz; sıra karışık (tohum).
- Grup: TAM BIST 15 + ABD 15; DEĞİL BIST 5 + ABD 5; tarih 2016-01-01 .. 2026-08-31; tohum 1717.
- Soru: E = tam girilir (son mumda stoplu girerdim) · H = girmem · B = belirsiz.
- Karar: TAM sayfalarında E payı >= 0,60 VE TAM - DEĞİL E payı farkı >= 0,30 -> 'GÖZLE UYUMLU'; TAM E payı < 0,40 -> 'GÖZLE UYUMSUZ'; aksi 'KISMİ'. Fisher kesin p bilgi. Sonuç (r20 / r60 / önce kırılım-stop) yalnız bilgi; n küçük, bulgu değil.

## Veri

- V_ABD.pkl sha256: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl sha256: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- ABD oc_veri notu: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- AVR oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- BIST oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı

## OLAY SAYIMI (getirisiz; durum günü sinyal tarihine, olay giriş tarihine göre dönem)

| Satır | Pazar | hisse | durum günü 2016-22 / 2023 / 2024-26 | OLAY (tekil, giriş dönemi) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |
|---|---|---|---|---|---|---|
| TAM_DIP | ABD | 607 | 2138 / 424 / 1056 | 283 / 47 / 212 | 676 | 2399 |
| TAM_DIP | AVR | 271 | 782 / 206 / 705 | 156 / 34 / 135 | 584 | 787 |
| TAM_DIP | BIST | 431 | 1387 / 388 / 2556 | 296 / 101 / 483 | 2845 | 584 |
| TAM | ABD | 783 | 3180 / 690 / 1643 | 442 / 76 / 365 | 1089 | 3606 |
| TAM | AVR | 325 | 1235 / 278 / 943 | 242 / 43 / 172 | 892 | 1160 |
| TAM | BIST | 548 | 3892 / 1610 / 5579 | 832 / 350 / 1019 | 7618 | 1247 |
| TAM_ORTA | ABD | 425 | 685 / 256 / 570 | 140 / 32 / 162 | 324 | 853 |
| TAM_ORTA | AVR | 163 | 406 / 72 / 226 | 96 / 11 / 44 | 249 | 304 |
| TAM_ORTA | BIST | 500 | 2145 / 1127 / 2751 | 500 / 260 / 577 | 4052 | 628 |
| TAM_TEPE | ABD | 1 | 0 / 0 / 2 | 0 / 0 / 1 | 1 | 0 |
| TAM_TEPE | AVR | 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 | 0 |
| TAM_TEPE | BIST | 1 | 1 / 0 / 0 | 1 / 0 / 0 | 0 | 0 |
| S1 | ABD | 1407 | 30004 / 6243 / 14768 | 4367 / 889 / 2557 | 20447 | 24339 |
| S1 | AVR | 580 | 34299 / 6727 / 18565 | 3485 / 649 / 1880 | 26955 | 30780 |
| S1 | BIST | 581 | 35461 / 5851 / 32285 | 3728 / 719 / 2888 | 59275 | 9622 |
| S12 | ABD | 1402 | 23703 / 4817 / 12174 | 3838 / 764 / 2291 | 16433 | 18213 |
| S12 | AVR | 580 | 28924 / 5383 / 15378 | 3167 / 595 / 1735 | 21902 | 25583 |
| S12 | BIST | 580 | 30453 / 4671 / 23584 | 3502 / 665 / 2590 | 47386 | 6286 |
| S123 | ABD | 863 | 4729 / 971 / 2359 | 549 / 98 / 437 | 1600 | 5618 |
| S123 | AVR | 336 | 1543 / 325 / 1029 | 276 / 50 / 185 | 1038 | 1414 |
| S123 | BIST | 557 | 4680 / 1984 / 6472 | 921 / 378 / 1092 | 9417 | 1501 |
| SM_TEPE | ABD | 1193 | 14103 / 867 / 4625 | 2810 / 230 / 1138 | 11603 | 3813 |
| SM_TEPE | AVR | 572 | 21378 / 1589 / 7459 | 2200 / 266 / 1015 | 15318 | 11633 |
| SM_TEPE | BIST | 441 | 7626 / 898 / 2316 | 731 / 123 / 301 | 5187 | 4481 |

### Bağlam dağılımı (durum günü; DİP / ORTA / TEPE / TANIMSIZ)

| Satır | Pazar | DİP | ORTA | TEPE | TANIMSIZ |
|---|---|---|---|---|---|
| TAM | ABD | 3618 | 1511 | 2 | 455 |
| TAM | AVR | 1697 | 704 | 0 | 116 |
| TAM | BIST | 4331 | 6023 | 1 | 749 |
| S1 | ABD | 13509 | 21235 | 11013 | 7056 |
| S1 | AVR | 10135 | 31039 | 17088 | 5880 |
| S1 | BIST | 17056 | 36652 | 12563 | 10265 |
| S12 | ABD | 8380 | 17739 | 10749 | 4858 |
| S12 | AVR | 6036 | 25968 | 16707 | 4609 |
| S12 | BIST | 10809 | 30372 | 12329 | 7181 |
| S123 | ABD | 5036 | 2227 | 4 | 1073 |
| S123 | AVR | 1904 | 872 | 0 | 197 |
| S123 | BIST | 4817 | 7228 | 5 | 1340 |

### Çöl nadir mi? (TAM_DIP = ana satır; hisse-yıl)

| Pazar | dönem | ölçülebilir hisse-gün | hisse-yıl (/ 252) | TAM_DIP durum günü | TAM_DIP olay (tekil) | durum günü / hisse-yıl | olay / hisse-yıl |
|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | 1738006 | 6897 | 2138 | 283 | 0,310 | 0,041 |
| ABD | 2023 | 334700 | 1328 | 424 | 47 | 0,319 | 0,035 |
| ABD | 2024-26 | 926965 | 3678 | 1056 | 212 | 0,287 | 0,058 |
| AVR | 2016-22 | 932562 | 3701 | 782 | 156 | 0,211 | 0,042 |
| AVR | 2023 | 144043 | 572 | 206 | 34 | 0,360 | 0,059 |
| AVR | 2024-26 | 388076 | 1540 | 705 | 135 | 0,458 | 0,088 |
| BIST | 2016-22 | 593392 | 2355 | 1387 | 296 | 0,589 | 0,126 |
| BIST | 2023 | 112353 | 446 | 388 | 101 | 0,870 | 0,227 |
| BIST | 2024-26 | 351821 | 1396 | 2556 | 483 | 1,831 | 0,346 |

| Pazar | takvim yılı: ölçülebilir hisse-yıl (>= 60 ölçülebilir gün) / en az bir TAM_DIP günü olan / pay |
|---|---|
| ABD | 2016: 906 / 45 / 5,0%; 2017: 938 / 63 / 6,7%; 2018: 973 / 94 / 9,7%; 2019: 1029 / 89 / 8,6%; 2020: 1084 / 63 / 5,8%; 2021: 1163 / 46 / 4,0%; 2022: 1304 / 219 / 16,8%; 2023: 1346 / 122 / 9,1%; 2024: 1374 / 125 / 9,1%; 2025: 1401 / 134 / 9,6%; 2026: 1410 / 97 / 6,9% |
| AVR | 2016: 501 / 20 / 4,0%; 2017: 514 / 8 / 1,6%; 2018: 523 / 39 / 7,5%; 2019: 534 / 34 / 6,4%; 2020: 544 / 38 / 7,0%; 2021: 550 / 11 / 2,0%; 2022: 569 / 90 / 15,8%; 2023: 574 / 53 / 9,2%; 2024: 576 / 69 / 12,0%; 2025: 578 / 61 / 10,6%; 2026: 579 / 46 / 7,9% |
| BIST | 2016: 312 / 26 / 8,3%; 2017: 346 / 27 / 7,8%; 2018: 357 / 102 / 28,6%; 2019: 370 / 43 / 11,6%; 2020: 376 / 5 / 1,3%; 2021: 381 / 63 / 16,5%; 2022: 421 / 66 / 15,7%; 2023: 467 / 99 / 21,2%; 2024: 498 / 131 / 26,3%; 2025: 565 / 182 / 32,2%; 2026: 579 / 167 / 28,8% |

Kural: hücre n < 30 ise ÖLÇÜLEMEDİ; güç yetersizse DESTEKLENMEDİ denmez.

## SAPMA / sınır (sonuç görülmeden yazıldı)

- SAPMA-1 (ana model kararı, 17 Kas; tasarımdan önce, getiri görülmeden): iş tanımı §2 (4)'teki 'C_t < max(High, W)' W t'yi içerdiği için neredeyse boştu (yalnız C_t = H_t = pencere tepesi iken düşer; alt ajan HATA 1). Yeni kural: C_t <= max(High, W \ {t}) (t hariç önceki 9 pencere barı). İlk yarı aynı. TASARIM aynı 72 noktalı ızgara ve aynı mekanik seçim kuralıyla yeniden koşuldu; bu ön kayıt onun üzerine yazıldı.
- SÜREÇ NOTU (alt ajan HATA 4): AŞAMA 1 keşfinde kor_anahtar.json'un ilk ~4 KB'si `head` ile okunurken ilk ~11 sayfanın r20 / r60 değerleri ekrana geldi. Tasarım kodu bu alanları okumaz (test 'etiketlerde r20 / r60 alanı yok'); eşik seçimi önceden yazılı mekanik puan + sadelik kuralıyla yapıldı. Yine de AŞAMA 1 getiri yasağına süreç ihlalidir.
- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD'dir (oc_veri notunda).
- Tasarım seti küçük ve Ç187 S+ / S- sayfalarından geldi; seçilen eşik tanım kalibrasyonudur, bulgu değildir.
- (3) ve (5) düşmüş hisseleri seçer: hayatta kalma yanlılığı (bugün işlem görenler) bu satırda getiriyi yukarı itebilir; kısa vadeli dönüş eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler).
- ON_KAYIT.md'yi alt ajan git'e işleyemez: ana model işler; `kos` git kaydını ister (--gitsiz yalnız SAPMA olarak yazılır).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: (3) dönüm (60 bar tepeden >= %10-20 düşmüş) ve (5) tepede değil sinyali düşük 60 gün momentumlu hisselere iter; eşler aynı momentum beşliğinden olduğu için bu fark eşlenir; kısa vadeli dönüş / oynaklık eşlenmez (raporda sınır) |
| K2 | geleceğe bakma | EVET | bütün ölçüler rolling geriye (fv_olcu: W, önceki 30 / 60 / 120 / 250 bar t'de biter; bağlam KONUM t dahil 250 bar); etiket seti Cemal'in t'de biten sayfaları; kos fv_gelecek_denetimi her pazarda 40 TAM_DIP gününde (bağlam dahil) seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma' (rastgele seride kesme = tam seri, bütün günler); tasarımda getiri / r20 / r60 hiç okunmadı (anahtarın r alanları atlanır) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz barlar (H>L, V>0, fiyat > 0; geçersiz bar atılır, pencereye girmez) + FO.fo_bar ikinci süzgeç; DGXX etiketi yfinance'ta 16 Kas (seans içi yarım bar) alınmaz ve aynı süzgeçten geçer |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir (ilk gün); n bağımsız olay; hücrede medyan da yazılır; ön kayıt OLAY SAYIMI durum günü ve tekil olayı ayrı verir |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter; kör set r20 / r60 de t+1 açılışından |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); bütün şartlar oran (fitil payı, HAT'a göre %, tepeye göre %), birimden bağımsız; bölünme şüphesi cetvelde geçmiş pencerede havuz dışı; DGXX etiketi ham (auto_adjust=False), yalnız etiket |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı, -%50 olasılığı aşağı yanlı' notu; (3) dönüm ve (5) tepede değil düşmüş hisseleri seçtiği için hayatta kalma yanlılığı bu işte daha büyük olabilir |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; tasarım seti küçük (19 + 10 sayfa + 5 aralık): eşik seçimi bulgu değil, yalnız tanım kalibrasyonu; olay sayımı getirisiz |
| K9 | ön kayıt | EVET | V2_ESIK sha + V2_SECIM + FITIL_V2.py sha + TASARIM.md sha + kör anahtar / cevap sha + cetvel üç sha + veri sha bu dosyada; ızgara (72 nokta) ve sadelik sırası tasarımdan önce kodda yazılı; iş tanımı git'te (22d7e50); kos ik_kontrol_kapisi + OC.oc_kapi + fv_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; etiket sayfaları kor_anahtar.json'dan (sembol / tarih) mekanik; 3 sayfa (PAPIL No 3, LIDER No 26, EPLAS No 41) ham V_BIST'ten bağımsız kodla yeniden hesaplandı: ASIM / ALTYOK / HAT / düşüş / yol / tepe / düz TASARIM tablosuyla aynı |
| K11 | yeniden üretim | EVET | ana olay satırları /tmp/fitil_v2/olay_TAM_DIP.csv.gz (bağlam ve kırılım sütunlu); rapor >= 2 hücreyi bağımsız kodla yeniden üretir (ana model denetimi); tasarım tablosu her etiketin ölçü değerlerini yazar (elle yeniden hesaplanabilir) |
| K12 | ifade | EVET | etiketler yalnız FO.fo_etiket / oc_etiket kuralıyla; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok; kör set sorusu 'tam girilir mi', alım tavsiyesi değil |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fv; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar taraması testte ve her yazımda; ücretli veri yok; commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tanım ölçümü ve kör set (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## Test

`python test_fitil_v2.py` (sentetik: ölçüler elle, her şart tek tek düşürülür, geleceğe bakma kesme testi, ızgara 72 / sadelik, etiket seti sayıları, puan, kırılım / stop, kör cevap ayrıştırma / karar, kapı, e-posta / anahtar taraması, kör sayfa ad / tarih sızıntısı).
