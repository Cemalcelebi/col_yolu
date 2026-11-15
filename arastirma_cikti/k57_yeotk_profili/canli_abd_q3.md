# K57 canlı ABD Q3 2026 taraması: YEOTK profili

Hazırlanma: 9 Kasım 2026 (Pazartesi). Kod: scratchpad abd_q3/hesap_ana.py. Bütün satırlar: canli_abd_q3_tablo.csv (2.128 şirket, 14'ü fon/ETF bayraklı ve sıralamada dışarıda).

## 0. Kısa sonuç (düz dil)
- **Dokuz şartın hepsini tutan tek hisse var: CENX (Century Aluminum).** Gelir yıllık +%52, net kâr Q2'den yüksek (302,6 > 249,3 M$), sermaye artırımı ve borçla finansman izi yok, rapordan önce tepeden −%57 ve 90 günde −%41 düşmüştü, rapor ertesi gün +%11 çıktı. Ama büyümenin kaynağı yeni bir iş değil: İzlanda'daki fabrikanın 2. hattı yeniden çalıştı. Şirket Q4 için daha düşük bir kâr (FAVÖK) bekliyor. Yani YEOTK'taki gibi "isimli yeni sözleşme" hikâyesi yok.
- **YEOTK'un harfiyen iki şartını ("Q3 geliri > ilk yarı toplamı" ve "Q3 kârı > ilk yarı toplamı") tutan 12 ABD şirketi var. Hiçbiri gerçek ivme değil.** Biyoteknoloji şirketlerinin tek seferlik lisans ve kilometre taşı gelirleri (KROS, NRIX, ALEC, FHTX, XNCR), mevsimsel işler (PRM yangın söndürücü, JAKK oyuncak, PRSU turizm, MRNA aşı), değerleme kârı (IONQ, NXTT) ve BUR. Bu şart ABD'de mevsimselliği ve tek seferlik geliri ayıklamıyor. Anlamlı olan **yıllık büyüme ile çeyrek ivmesinin birlikte** bakılmasıdır.
- **En YEOTK benzeri aday ölçüme tam girmedi: AEHR (Aehr Test Systems).** Gelir yıllık +%200 ve çeyrekte +%75, GAAP kârı zarardan kâra döndü. Fiyat 6 Kasım'da tepeden −%64 ve 90 günde −%48. Rapor ertesi 3 Kasım'da +%26,5 çıktı, 5 Kasım'da −%19 geri verdi. Finansman (ATM) taraması SEC engeli yüzünden yapılamadı. Bkz. §6.
- **İzleme listesinin hiçbiri profile uymuyor.** WULF, CORZ, APLD, IREN ve CIFR'ın hepsi kaldıraç (Y/Ö > 3 ya da özkaynak negatif) ve 24 aylık finansman şartından kalıyor. DGXX, AIB, QMLS ve DUOT Q3 raporunu henüz vermedi; NBIS 6-K ile raporluyor ve XBRL frame'lerinde yok.
- **Piyasa bağlamı:** SPY tepeden −%5,6, IWM −%10,3 (6 Kas). 100M–5B $ evreninde medyan hisse tepeden −%27 aşağıda ve hisselerin %46'sı −%30 şartını tutuyor. Yani "tepeden düşmüş" şartı bu dönemde ayırt edici değil. Ayıran şartlar ivme, kâr, finansman ve tepki.
- **Bu çalışma iz testi değildir.** Tek dönemli, canlı bir aday listesidir. FI_OLCUT eşli testi yapılmadı; sonuç "bulgu" diye sunulamaz.

## 1. Veri durumu: SEC engeli
- **SEC XBRL frames** (us-gaap Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet, NetIncomeLoss; CY2026Q3/Q2/Q1, CY2025Q4/Q3; anlık CY2026Q3I StockholdersEquity, Liabilities, LiabilitiesAndStockholdersEquity; dei EntityCommonStockSharesOutstanding CY2026Q3I/Q2I/CY2025Q3I). Önceki deneme 9 Kas 2026 13:46 UTC'de indirdi ve bu çalışma onları yeniden kullandı. SalesRevenueNet 2026 frame'leri boş döndü (404).
- **SEC submissions** (dosyalama tarihi, kabul saati, 8-K 2.02, 424B ve 3.02 sayımı): 13:48–13:53 UTC'de yalnız önceki denemenin 291 aday CIK'i için indi (286'sı Q3 tablosunda).
- **Bu oturumda SEC'e yeni istek gitmedi.** 15:15 ve 15:26 UTC'de, istenen User-Agent ile (`col-yolu-arastirma/1.0 (+https://github.com/cemalcelebi/col_yolu)`) data.sec.gov ve www.sec.gov **403 "Your Request Originates from an Undeclared Automated Tool"** döndü. Önceki deneme kuraldışı bir UA ile indirmişti; www.sec.gov'daki company_tickers.json da "Request Rate Threshold Exceeded" sayfası olarak inmişti. Engel muhtemelen ondan. SEC, UA'da "company specific information" (fiilen e-posta) istiyor. Kişisel e-posta kullanılmadı ve engel aşılmaya çalışılmadı. CIK→ticker eşlemesi için repo kopyası company_tickers_repo.json (10.429 kayıt) kullanıldı.
- **Fiyatlar:** Yahoo chart v8, 1 yıllık günlük veri. 291 hisse 13:48–13:51 UTC'de, kalan ~1.730 hisse 15:17–15:40 UTC'de indi. Karışık indirme yüzünden **bütün seriler 6 Kas 2026 kapanışında kesildi** (son tam seans). 5 ticker 404 döndü. SPY ve IWM bağlam için ayrıca indi.
- **Kapsam:** CY2026Q2'de gelir bildiren 3.536 şirketin 2.128'i (%60) 9 Kas sabahı Q3 frame'indeydi. 1.573'ü henüz yok: hızlandırılmamış dosyalayıcıların Q3 10-Q son günü 16 Kas 2026, ayrıca frame güncellemesi gecikmeli. **Küçük şirketlerin çoğu bu taramada eksik.**

## 2. Yöntem ve eşikler (sonuç görülmeden sabitlendi)
- **Gelir etiketi:** CIK başına Q3'te ilk bulunan etiket (Revenues → RFCWC → SalesRevenueNet). Diğer dönemlerde aynı etiket yoksa sıradaki etiket kullanıldı (`tag_karisik` bayrağı). Frame dönemleri takvim çeyreğine hizalı; mali yılı farklı şirketlerde (ör. Ağustos sonu) Q3 = en yakın takvim çeyreği.
- **İvme** = Q3 / ort(Q1, Q2 2026). Biri eksikse mevcut olanla hesaplandı (`ivme_payda_n`). Mali yılı Mayıs veya Haziran'da biten şirketlerin takvim Q2'si 10-K içinde kaldığı için genelde eksik (APLD, IREN, AEHR, KMT, SCSC, TLRY). ⚑ = ivme > 5: önceki çeyrekler ~0, tek seferlik gelir şüphesi.
- **Piyasa değeri (PD)** = 6 Kas kapanışı × kapak sayfası pay sayısı (CY2026Q3I, yoksa Q2I). Çok sınıflı paylarda eksik sayılabilir. Evren 100M–5B $; 5–20B $ ayrı listede.
- **Olay günü:** Q3 10-Q'dan önceki 60 gün içindeki son 8-K kalem 2.02'nin (sonuç duyurusu) SEC kabul saati, yoksa 10-Q kabul saati. SEC zaman damgası UTC'dir: 8-K 2.02 kabullerinin saat dağılımı 10–12 Z ve 20–21 Z'de yığılıyor, yani seans öncesi 07:00 ET ve seans sonrası 16:05 ET. ET'ye çevrildi (1 Kas'tan önce UTC−4, sonra UTC−5). Kabul 16:00 ET'den sonraysa tepki seansı ertesi gün, değilse aynı gün.
- **Tepki** = tepki seansı kapanışı / önceki kapanış − 1. **Brief'teki harfiyen tanım** (10-Q dosyalama tarihinden sonraki ilk seans / önceki kapanış) ayrıca `tepki_brief_10q` sütununda. İkisi ayrışabiliyor: ABD'de sonuç 8-K ile, 10-Q çoğu zaman günler sonra gelir. Örnek GERN: olay günü +%16, harfiyen −%12. CIFR: −%6 ve +%18.
- **Tepeden düşüş** = olay öncesi kapanış / olaydan önceki en yüksek gün içi fiyat − 1 (geçmiş ~11 ay; Yahoo 1y aralığı). **90g** = olay öncesi kapanış / 90 takvim günü önceki kapanış − 1. Olay tarihi bilinmeyenlerde 6 Kas kapanışı kullanıldı (`K78_kaynak`).

| Ölçüt | Eşik | YEOTK'taki karşılığı |
|---|---|---|
| K1 | Gelir Q3/Q3'25 − 1 > %20 | güçlü satış büyümesi |
| K2 | İvme > 1,20 | Q3 > H1 (harfiyen = ivme > 2; ayrı bayrak `yeotk_q3_gt_h1_gelir`) |
| K3 | Net kâr Q3 > 0 ve > Q2 | Q3 kârı > H1 (harfiyen ayrı bayrak `yeotk_q3_gt_h1_kar`) |
| K4 | Özkaynak > 0 ve Yükümlülük/Özkaynak ≤ 3 | sağlam bilanço |
| K5 | Pay sayısı yıllık ≤ +%10 | nakit seyrelme yok (12 ay) |
| K6 | 24 ayda (9.11.2024–9.11.2026) 424B1/2/3/4/5/7 = 0 ve 8-K 3.02 = 0 | 24 ay seyrelme yok, zehirli finansman yok (yalnız 286 adayda ölçülebildi) |
| K7 | Tepeden ≤ −%30 | −%54 |
| K8 | 90g < 0 | −%38 |
| K9 | Tepki ≥ +%10 | tavan |

- **Puan** = tutan ölçüt sayısı (0–9). Ölçülemeyen ölçüt boş kalır, puana girmez (`olculen_kriter`). **Sıralama:** puan, sonra ivme.

## 3. Huni (fon/ETF hariç 2.108 şirket, ardışık)
| Adım | Kalan | Tek başına tutan |
|---|---|---|
| Q3 2026 gelir frame'de | 2.108 | – |
| ticker eşleşti | 2.006 | 2.006 |
| fiyat + PD hesaplandı | 1.699 | 1.699 |
| PD 100M–5B $ | 891 | 891 |
| K1 gelir YoY > %20 | 221 | 554 |
| K2 ivme > 1,2 | 91 | 323 |
| K3 kâr > 0 ve > Q2 | 43 | 803 |
| K4 özk > 0, Y/Ö ≤ 3 | 28 | 1.425 |
| K5 pay YoY ≤ %10 | 17 | 1.476 |
| K6 finansman temiz (24 ay) | 14 | 103 (yalnız 286 ölçüldü) |
| K7 tepeden ≤ −%30 | 7 | 784 |
| K8 90g < 0 | 6 | 1.257 |
| K9 tepki ≥ +%10 | **1 (CENX)** | 41 |

- Temel beşliği (K1–K5) tutan: bütün boylarda 95, 100M–5B $'da 27. Submissions'ı olmayan ama K1–K5'in hepsini tutan 100M–5B şirketi yok, yani K6 ve K9'un ölçülememesi temel beşli adayını düşürmedi.
- Harfiyen YEOTK (Q3 gelir > H1 **ve** Q3 kâr > H1): 12 şirket (§0).

## 4. İlk 25 (PD 100M–5B $, puana sonra ivmeye göre)
Kaynak: SEC frames (Q3 2026 10-Q/10-K XBRL), SEC submissions, Yahoo (6 Kas 2026 kapanışına kadar). Para birimi $. "424B/3.02" = 24 ayda prospektüs eki / 8-K 3.02 sayısı. "10-Q harfiyen" = brief tanımıyla tepki. Puan = tutan/ölçülen.

| # | Ticker | Şirket | PD $M | Gelir Q3 $M | YoY | İvme | Kâr Q3 $M | Kâr Q2 $M | Y/Ö | Pay YoY | 424B/3.02 (24 ay) | Tepeden | 90g | Olay günü | Tepki | 10-Q harfiyen | Puan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CENX | Century Aluminum Company | 3,313 | 961.2 | +52% | 1.37 | 302.6 | 249.3 | 0.85 | +6% | 0/0 | -57% | -41% | 2026-11-06 | +11% | +11% | 9/9 |
| 2 | KROS | KEROS THERAPEUTICS, INC. ⚑ | 184 | 40.0 | +183% | 2500.56 | 14.2 | -28.7 | 0.10 | -36% | 0/0 | -58% | -15% | 2026-11-06 | -1% | -1% | 8/9 |
| 3 | LMB | LIMBACH HOLDINGS, INC. | 627 | 230.5 | +25% | 1.48 | 9.4 | 4.7 | 1.77 | +1% | 0/0 | -57% | +0% | 2026-11-04 | +16% | +16% | 8/9 |
| 4 | MXL | MaxLinear, Inc. | 4,475 | 218.1 | +72% | 1.43 | 28.9 | 1.8 | 0.72 | +4% | 0/0 | -49% | -9% | 2026-10-23 | -3% | -3% | 8/9 |
| 5 | RUN | Sunrun Inc. | 2,415 | 1,099.5 | +52% | 1.38 | 153.2 | 115.2 | 5.03 | +4% | 0/0 | -60% | -6% | 2026-11-05 | +12% | +12% | 8/9 |
| 6 | ECVT | Ecovyst Inc. | 1,139 | 308.6 | +51% | 1.33 | 18.2 | 7.9 | 1.34 | -5% | 0/0 | -34% | -9% | 2026-11-05 | +2% | +3% | 8/9 |
| 7 | ECG | Everus Construction Group, I | 3,912 | 1,384.2 | +40% | 1.22 | 91.9 | 83.9 | 2.13 | +0% | 0/0 | -34% | -20% | 2026-11-04 | -29% |  | 8/9 |
| 8 | MYRG | MYR GROUP INC. | 4,094 | 1,259.0 | +32% | 1.21 | 60.0 | 49.9 | 1.57 | +0% | 0/0 | -44% | -15% | 2026-10-29 | +1% | +1% | 8/9 |
| 9 | TMDX | TransMedics Group, Inc. | 3,065 | 203.0 | +41% | 1.12 | 17.1 | 14.7 | 1.76 | +2% | 0/0 | -56% | -18% | 2026-11-06 | +28% | +28% | 8/9 |
| 10 | GERN | GERON CORP | 638 | 60.2 | +27% | 1.10 | 1.4 | -16.7 | 1.33 | +1% | 0/0 | -54% | -43% | 2026-11-04 | +16% | -12% | 8/9 |
| 11 | TRC | TEJON RANCH CO. | 461 | 22.6 | +89% | 1.90 | 3.3 | 2.6 | 0.31 | +1% | 0/0 | -24% | -1% | 2026-11-05 | +3% | +1% | 7/9 |
| 12 | PGEN | PRECIGEN, INC. | 1,603 | 74.1 | +2438% | 1.90 | 35.8 | 20.1 | 1.53 | +1% | 0/2 | -44% | -27% | 2026-11-05 | -17% | -17% | 7/9 |
| 13 | KNF | Knife River Corporation | 3,201 | 1,275.6 | +6% | 1.89 | 137.9 | 43.9 | 1.45 | +0% | 0/0 | -40% | -17% | 2026-11-03 | +1% | +6% | 7/9 |
| 14 | AGIO | AGIOS PHARMACEUTICALS, INC. | 1,759 | 55.4 | +330% | 1.69 | -65.0 | -100.7 | 0.09 | +3% | 0/0 | -32% | -2% | 2026-11-05 | -10% | +4% | 7/9 |
| 15 | BKSY | BLACKSKY TECHNOLOGY INC | 883 | 42.8 | +118% | 1.58 | 18.5 | -20.8 | 1.24 | +15% | 2/1 | -68% | -40% | 2026-11-05 | +14% | +12% | 7/9 |
| 16 | PSIX | POWER SOLUTIONS INTERNATIONA | 903 | 202.1 | -1% | 1.44 | 29.9 | 16.9 | 0.96 | +0% | 0/0 | -66% | -12% | 2026-11-06 | +9% | +9% | 7/9 |
| 17 | VNDA | VANDA PHARMACEUTICALS INC. | 231 | 69.8 | +24% | 1.37 | -22.6 | -62.5 | 0.91 | +2% | 0/0 | -60% | -23% | 2026-10-29 | +1% | -6% | 7/9 |
| 18 | PRKS | United Parks & Resorts Inc. | 1,817 | 506.5 | -1% | 1.33 | 80.0 | 63.3 | -5.95 | -17% | 0/0 | -32% | -23% | 2026-11-05 | +11% |  | 7/9 |
| 19 | WINA | WINMARK CORPORATION | 944 | 27.9 | +23% | 1.30 | 11.8 | 10.4 | -2.20 | -0% | 0/0 | -42% | -25% | 2026-10-14 | +6% | +5% | 7/9 |
| 20 | ASLE | AerSale Corporation | 219 | 91.6 | +29% | 1.29 | -15.0 | -5.6 | 0.67 | +1% | 0/0 | -39% | -18% | 2026-11-06 | -5% |  | 7/9 |
| 21 | GRNT | GRANITE RIDGE RESOURCES, INC | 698 | 177.2 | +57% | 1.28 | -10.1 | 30.0 | 1.34 | +1% | 0/0 | -24% | -4% | 2026-11-06 | +13% | +13% | 7/9 |
| 22 | DIOD | DIODES INC /DEL/ | 3,535 | 532.6 | +36% | 1.25 | 43.7 | 46.6 | 0.55 | -1% | 0/1 | -46% | -35% | 2026-11-06 | +13% | +13% | 7/9 |
| 23 | PANL | PANGAEA LOGISTICS SOLUTIONS  | 496 | 219.1 | +30% | 1.22 | 38.3 | 10.2 | 1.07 | +1% | 0/0 | -22% | -1% | 2026-11-06 | +3% | +3% | 7/9 |
| 24 | GNK | GENCO SHIPPING & TRADING LIM | 1,133 | 151.9 | +90% | 1.21 | 38.0 | 16.6 | 0.49 | +1% | 0/0 | -13% | -2% | 2026-11-05 | +2% | +2% | 7/9 |
| 25 | ACNT | Ascent Industries Co. | 124 | 27.1 | +38% | 1.20 | 1.4 | 0.7 | 0.33 | -4% | 0/0 | -23% | -10% | 2026-11-05 | -1% | -1% | 7/9 |

- 8 puanın altındakiler 7 puanla eşit; sıralamayı ivme belirliyor. 26. sıradan sonra 7 puanlı başka şirketler de var (CSV).
- KROS ⚑: Q1 ve Q2 geliri ~0, ivme anlamsız. Pay −%36: 2025'teki sermaye iadesinin etkisi olabilir (doğrulanmadı).

## 5. 5–20B $ listesi (ilk 10)
| # | Ticker | Şirket | PD $M | Gelir Q3 $M | YoY | İvme | Kâr Q3 $M | Kâr Q2 $M | Y/Ö | Pay YoY | 424B/3.02 (24 ay) | Tepeden | 90g | Olay günü | Tepki | 10-Q harfiyen | Puan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | CORT | CORCEPT THERAPEUTICS INC | 7,964 | 340.5 | +64% | 1.62 | 126.8 | 43.0 | 0.24 | +4% | 0/0 | -35% | -26% | 2026-11-04 | -3% | -3% | 8/9 |
| 2 | TTMI | TTM TECHNOLOGIES, INC. | 7,009 | 1,203.9 | +60% | 1.30 | 84.8 | 83.0 | 1.72 | +2% | 0/0 | -54% | -29% | 2026-10-22 | -28% | -3% | 8/9 |
| 3 | NBIX | NEUROCRINE BIOSCIENCES, INC. | 16,664 | 1,122.7 | +41% | 1.27 | 206.5 | 144.4 | 0.45 | +2% | 0/0 | -22% | -12% | 2026-11-03 | +13% | +13% | 8/9 |
| 4 | MKSI | MKS INC. | 13,001 | 1,413.0 | +43% | 1.21 | 236.0 | 175.0 | 1.81 | +1% | 0/0 | -56% | -33% | 2026-11-05 | -9% | +9% | 8/9 |
| 5 | KRMN | KARMAN HOLDINGS INC. | 6,045 | 201.6 | +66% | 1.21 | 20.9 | 14.0 | 2.72 | +0% | 4/0 | -73% | -45% | 2026-11-06 | +42% |  | 8/9 |
| 6 | SEZL | SEZZLE INC. | 5,048 | 166.5 | +43% | 1.17 | 47.8 | 40.8 | 0.73 | -1% | 0/0 | -30% | -23% | 2026-11-05 | +13% | -4% | 8/9 |
| 7 | IONQ | IONQ, INC. | 14,107 | 173.8 | +336% | 2.40 | 564.0 | -1,867.7 | 0.57 | +22% | 19/11 | -64% | -41% | 2026-11-06 | +23% | +23% | 7/9 |
| 8 | STRL | STERLING INFRASTRUCTURE, INC | 7,712 | 1,563.9 | +127% | 1.57 | 214.9 | 155.8 | 1.28 | -1% | 0/1 | -61% | -33% | 2026-10-29 | -4% | -7% | 7/9 |
| 9 | LSCC | Lattice Semiconductor Corp | 14,937 | 291.0 | +118% | 1.56 | 11.2 | 19.4 | 0.84 | +4% | 0/2 | -39% | -31% | 2026-11-03 | +11% | +1% | 7/9 |
| 10 | PTGX | PROTAGONIST THERAPEUTICS, IN | 8,618 | 274.4 | +5724% | 1.29 | 220.0 | 162.8 | 0.06 | +4% | 0/0 | -16% | -7% | 2026-11-06 | -2% |  | 7/9 |

- IONQ harfiyen YEOTK şartlarını tutuyor ama 24 ayda 19 adet 424B ve 11 adet 8-K 3.02 var, pay +%22. Q3 kârı (564 M$) Q2'deki −1,87 milyar $ zararın tersine dönmesi. Faaliyet kârı değil, değerleme kalemi olması muhtemel (doğrulanmadı). Profil dışı.
- KRMN: tepki +%42, tepeden −%73, ama 24 ayda 4 adet 424B var (K6 ✗).

## 6. Ölçüme tam girmeyen olası adaylar (submissions yok → K6 ve K9 boş)
Mali yılı Mayıs veya Haziran'da biten şirketler önceki denemenin aday listesine girmemişti (eski kod Q1 ve Q2'nin ikisini de şart koşuyordu). SEC engeli yüzünden submissions indirilemedi. Olay günleri aşağıda ikincil kaynak ve Yahoo hacim sıçramasıyla belirlendi.

| Ticker | PD $M | Gelir YoY | İvme (yalnız Q1) | Kâr Q3 $M | Y/Ö | Pay YoY | Tepeden (6 Kas) | 90g (6 Kas) | Olay ve tepki (Yahoo) | Not |
|---|---|---|---|---|---|---|---|---|---|---|
| AEHR | 1.757 | +%201 | 3,20 | 7,2 | 0,17 | +%9 | −%64 | −%48 | 3 Kas +%26,5; 5 Kas −%19,2 | Mali Q1 FY27 (25 Eyl'de biten çeyrek). Gelir 33,0 M$, çeyrekte +%75, GAAP kârı 7,2 M$ (geçen yıl −2,1 M$). Sipariş 46,7 M$, FY27 hedefi 150 M$. [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0001040470/000165495426009385/aehr_ex991.htm), [Finviz/basın bülteni](https://finviz.com/news/413485/aehr-test-systems-reports-record-first-quarter-fiscal-2027-revenue-of-330-million-raises-full-year-revenue-outlook-to-150-million-triple-fiscal-2026-revenue). **Finansman (ATM) doğrulanamadı.** |
| KMT | 1.772 | +%54 | 1,30 | 271,6 | 1,10 | +%1 | −%48 | −%31 | 4 Kas −%13,9 | Satış +%54 (organik), ama kârı tungsten fiyat zamanlaması şişirdi; altyapı segmenti zayıf. [Finviz/basın bülteni](https://finviz.com/news/415149/kennametal-announces-fiscal-2027-first-quarter-results) |
| SCSC | 870 | +%30 | 1,25 | 8,7 | 1,44 | −%7 | −%36 | −%22 | 5 Kas −%20,9 (hacimden) | doğrulanmadı |
| TLRY | 432 | +%23 | 1,24 | −43,1 | 0,44 | −%87 (ters bölünme olası) | −%81 | −%36 | 4 Kas +%11,7 (hacimden) | zarar, profil dışı |
| PBH | 2.037 | +%23 | 1,27 | 25,3 (Q2 29,2) | 1,43 | −%1 | −%40 | −%22 | 4 Kas +%7,5, 5 Kas −%16,8 | K3 ✗, doğrulanmadı |

## 7. İlk 10'un ikincil kaynak kontrolü (tek kaynak; arama özetleri, ana metinler açılmadı)
| # | Ticker | Büyüme organik mi? | Finansman | Kaynak |
|---|---|---|---|---|
| 1 | CENX | Organik ama **yeniden başlatma etkisi**: satış 961,2 M$ (Q2'den +209,1 M$), İzlanda Grundartangi 2. hattı yeniden çalıştı. Kâr 302,6 M$ (Q2'den +53,3 M$); sigorta gelirleri azaldı. Şirketin Q4 düzeltilmiş FAVÖK beklentisi 275–300 M$ (Q3: 331,6 M$) | SEC: 424B 0, 3.02 0; 24 ayda 1 S-3 ve 1 borç 8-K'sı (1.01+2.03). Hisseye çevrilebilir tahvil (konvertibl) bilgisi doğrulanmadı | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0000949157/000162828026071024/a20260930q3ex991earningsre.htm), [finsee](https://finsee.ai/earnings/cenx/2026/q3/en/) |
| 2 | KROS | **Tek seferlik**: 40 M$ Takeda lisans ve kilometre taşı geliri; 9 aylık gelir 40,4 M$ (geçen yıl 243,7 M$) | SEC: 0/0. Nakit 259,5 M$ | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0001664710/000166471026000065/exhibit991q32026.htm) |
| 3 | LMB | Kısmen satın alma: gelir +%25 (230,5 M$), bunun 19,3 M$'ı CYMCOR (Ağu) ve 1901 (Eyl) satın almalarından. Kâr +%8 | SEC: 0/0. Toplam borç 36 M$'dan 155 M$'a çıktı, satın alma finansmanı (Panabee) | [capital.com](https://capital.com/en-gb/news/limbach-q3-net-income-rises-8-to-9-45-million-q3), [StockStory](https://stockstory.org/us/stocks/nasdaq/lmb/news/earnings-call/lmb-q3-2026-deep-dive-organic-growth-resumes-as-acquisitions-broaden-capabilities) |
| 4 | MXL | Organik: gelir 218,1 M$, yıllık +%72, çeyrekte +%29; altyapı (optik veri merkezi) +%210. Faaliyet nakit akışı −13,6 M$ | SEC: 0/0. Kredi limiti 200 M$'a yükseltildi. Konvertibl doğrulanmadı | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0001288469/000128846926000060/a09302026exhibit991.htm), [Earnings Whispers](https://www.earningswhispers.com/article/MXL/r327) |
| 5 | RUN | **Muhasebe ve satış modeli değişikliği**: sistem satışları +%134, sistemler 3. tarafa satılıyor. Abone eklemesi −%24 | SEC: 0/0, ama Y/Ö 5,0 (K4 ✗); nakit üretim hedefi düşürüldü | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0001469367/000162828026070143/exhibit991q326.htm), [pv-tech](https://www.pv-tech.org/sunrun-reaches-5gwh-storage-milestone-as-q3-solar-installations-fall-15-year-on-year/) |
| 6 | ECVT | **Satın alma ve maliyet yansıtması**: satış +%51 (308,6 M$). İçinde Calabrian satın alması (30.06.2026) ve ~67 M$ sülfür maliyeti yansıtması var. Düzeltilmiş FAVÖK yalnız +%6 | SEC: 0/0 | [Placera/basın bülteni](https://www.placera.se/pressmeddelanden/ecovyst-ecovyst-reports-third-quarter-2026-results-and-raises-2026-outlook-20261105) |
| 7 | ECG | Organik %36 (gelir +%40, ~1,38 milyar $), kâr +%61; veri merkezi talebi. **Tepki −%29 (4 Kas), nedeni bakılmadı** | SEC: 0/0 | [Finviz/basın bülteni](https://finviz.com/news/414928/everus-reports-third-quarter-2026-results-raises-2026-guidance) |
| 8 | MYRG | Gelir +%32 (1,26 milyar $), kâr +%87. Valley ve Comet satın almalarına 324,8 M$ nakit ödendi; organik pay verilmedi | SEC: 0/0. 100 M$ geri alım | [Finviz/basın bülteni](https://finviz.com/news/410573/myr-group-inc-announces-third-quarter-and-first-nine-months-2026-results-board-approves-new-100-million-share-repurchase-program) |
| 9 | TMDX | Gelir +%41, organik %35 (PAD Aviation katkısı). Kâr yıllık düştü (17,1 M$; geçen yıl 24,3 M$) | **460 M$ %1,5 konvertibl (vade 2028) duruyor** (10-Q). SEC 424B 0 | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm), [SEC 10-Q Q3](https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449827/tmdx-20260930.htm) |
| 10 | GERN | Organik ilaç satışı (RYTELO 60,1 M$, yıllık +%27, çeyrekte +%5); ilk çeyreklik kâr 1,35 M$. İvme 1,10 (K2 ✗). IMpactMF denemesi durduruldu | SEC: 424B 0, 3.02 0; 1 S-3 (raf kaydı) | [SEC 8-K ex99.1](https://www.sec.gov/Archives/edgar/data/0000886744/000119312526446203/d188608dex991.htm), [capital.com](https://capital.com/en-int/news/geron-swings-to-q3-2026-net-profit-of-1-35-million) |

- **İlk 10'un özeti:** "Gerçek iş + organik ivme + temiz finansman" üçlüsüne en yakın olanlar MXL (tepki −%3) ve ECG (tepki −%29). Fiyat ve tepki şartlarını da tutan tek isim CENX; onun büyümesi de fabrika yeniden başlatması. KROS, RUN ve ECVT'nin büyümesi tek seferlik, muhasebe kaynaklı ya da satın almadan geliyor.
- **Doğrulanamayanlar:** konvertibl ve ATM programları için yalnız SEC form sayımı var (24 ayda 424B ve 3.02). 144A konvertibller 424B üretmez; 8-K 1.01+2.03 sayıları CSV'de (`fin_8K101_203_24ay`) ama türü ayrılmadı. ECG'nin −%29'unun nedeni bakılmadı. Arama özetleri ikincil kaynaktır; rakamlar SEC frame değerleriyle (CENX 302,6; KROS 14,2; LMB 9,45; ECG 91,9; MYRG 60,0; TMDX 17,1; GERN 1,35 M$) tutarlı.

## 8. İzleme listesi (aynı ölçütler)
| # | Ticker | Şirket | PD $M | Gelir Q3 $M | YoY | İvme | Kâr Q3 $M | Kâr Q2 $M | Y/Ö | Pay YoY | 424B/3.02 (24 ay) | Tepeden | 90g | Olay günü | Tepki | 10-Q harfiyen | Puan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WULF | TERAWULF INC. | 5,702 | 76.2 | +51% | 1.94 | 709.9 | -939.9 | 8.36 | +20% | 6/3 | -66% | -41% | 2026-11-06 | +13% |  | 6/9 |
| 2 | CORZ | Core Scientific, Inc./tx | 3,789 | 232.9 | +187% | 1.67 | 1,178.1 | -1,155.3 | -6.44 | +4% | 14/2 | -58% | -39% | 2026-11-05 | -11% | +3% | 6/9 |
| 3 | APLD | APPLIED DIGITAL CORPORATION | 4,702 | 341.9 | +322% | 2.70 | -184.1 |  | 4.93 | +8% | 5/10 | -53% | -26% | 2026-10-08 | +0% | +0% | 5/8 |
| 4 | IREN | IREN Limited | – | 228.0 | -5% | 1.57 | -263.0 |  | 3.03 |  | 4/3 | -75% | -56% | 2026-11-06 | +20% | +20% | 4/7 |
| 5 | CIFR | Cipher Digital Inc. | 2,987 | 26.7 | -63% | 0.89 | 31.6 | -267.5 | 11.73 | +16% | 5/4 | -76% | -67% | 2026-11-02 | -6% | +18% | 3/9 |

| Ticker | Durum (9 Kas 2026, SEC submissions 13:5x UTC) |
|---|---|
| DGXX | **Henüz yok.** Son 10-Q 14.08.2026 (Q2); Q3 raporu 13 Kas'ta bekleniyor. 24 ay: 424B5 (08.05.2026), S-3 (09.04 ve 17.07.2026) + S-3/A (11.09.2026). Raf kaydı hazır, ATM/seyrelme riski (K6 ✗) |
| AIB | **Henüz yok** (Q2 10-Q 13.08.2026). Halka arz 424B4 08.06.2026; 424B3 17.02.2026; 8-K 11.09.2026 kalem 1.01, 2.01 ve 2.03 (satın alma + borç) |
| QMLS | **Henüz yok** (Q2 10-Q 25.08, 10-Q/A 28.08.2026). Halka arz 424B4 15.07.2026 |
| DUOT | **Henüz yok** (geçen yıl Q3 10-Q 13.11.2025). 2026'da 3 adet 424B5 (26.02, 02.03, 17.06) → seyrelme, K6 ✗ |
| NBIS | Yabancı özel ihraççı (6-K/20-F), XBRL frame'lerinde yok; Q3 6-K'sı submissions'ta görülmedi. 424B5: 10.09, 12.09 ve 12.11.2025 |
| WULF | 6/9. Kâr Q3 +710 M$, Q2 −940 M$ (büyük ihtimalle türev/varant değerlemesi, doğrulanmadı). Y/Ö 8,4; pay +%20; 424B 6, 3.02 3. Tepki +%12,8 (6 Kas). PD 5,7 milyar $ |
| CORZ | 6/9. **Özkaynak negatif** (−1,09 milyar $). Kâr dalgalanması +1,18 / −1,16 milyar $; 424B 14. Tepki −%10,8 |
| APLD | 5/8. Mali Q1 FY27 (31.08). Gelir +%322, kâr −184 M$; Y/Ö 4,9; 8-K 3.02 10 adet. Tepki +%0,2 (08.10) |
| IREN | 4/7. Gelir −%5 yıllık, kâr −263 M$; pay verisi frame'de yok (PD hesaplanamadı); 424B 4, 3.02 3. Tepki +%20,0 (06.11) |
| CIFR | 3/9. Gelir −%63 yıllık; Y/Ö 11,7; 424B 5, 3.02 4. Tepki olay gününde −%5,9, harfiyen tanımla +%18,4 |

**Sonuç:** Rapor veren beş madenci veya veri merkezi hissesinin hiçbiri YEOTK profilinde değil. Ortak sorunlar kaldıraç ve sürekli hisse ihracıyla finansman. Kâr satırları değerleme dalgalanması.

## 9. Boşluklar ve sıradaki adımlar
1. **SEC engeli (karar gerekli):** SEC, UA'da kurumsal iletişim bilgisi (fiilen e-posta) istiyor. Kural gereği Cemal'in e-postası yalnız Form 4 indirmesinde kullanılıyor. Engel kalkmazsa şunlar yapılamıyor: (a) ~1.800 şirketin submissions verisi (K6 ve olay günü); (b) 24 aylık seyrelme için CY2024Q3I pay frame'i (K5 yalnız 12 ay); (c) companyfacts ile mali Q4 türetme (APLD, IREN, AEHR, KMT ivmesi); (d) 2025 Q1 ve Q2 frame'leriyle mevsimsellik ayıklaması.
2. **Kapsam:** Q2 raporcularının %40'ı (1.573) henüz Q3 frame'inde yok. Küçük şirketlerin 10-Q son günü **16 Kas 2026**. Tarama 17 Kas'tan sonra aynı kodla yinelenmeli.
3. **Mevsimsellik:** "Q3 > H1" ABD'de mevsimsel ve tek seferlik işleri seçiyor. Ölçüt, Q3'26/H1'26 oranının Q3'25/H1'25 oranına bölünmüş hâline çevrilmeli; bunun için 2025 Q1 ve Q2 frame'leri gerekiyor (SEC).
4. **İsimli sözleşme / gerçek iş** ölçülmedi: XBRL'de yok. 8-K kalem 1.01 metni okunmalı.
5. **Fon krizi:** 31.08.2026 sonrası olağanüstü dönem (CLAUDE.md). Bu liste canlı izleme içindir, FI_OLCUT testine girmez.
