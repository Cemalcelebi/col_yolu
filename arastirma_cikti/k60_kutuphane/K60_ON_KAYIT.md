# K60 ÖN KAYIT — sinyal kütüphanesi, iki cetvel (portföy v2 + olasılık tablosu), üç dönem

Yazım zamanı: 2026-11-11 12:09:42 UTC (2026-11-11 15:09 TR) (ölçümden ÖNCE; gerçek veride hiçbir sinyale bağlı getiri, olasılık ya da t hesaplanmadı, sonuç görülmedi). Sürüm: K60 v1.0 (2026-11-11): sinyal kütüphanesi x iki cetvel (R1 portföy cetveli v2, R2 olasılık tablosu), KEŞİF / DOĞRULAMA / KASA, Benjamini-Hochberg + plasebo; geniş ABD evreni (yalnız yaşayanlar)
ESIK_SHA256: e1749249eeb8540fbeb8f2f5564fa5ff5d9f3dfb3c5d2dab681b65d515c80ba0
(K60_ESIK'in (kütüphane tanımları, dönemler, cetveller, çoklu deneme ve karar kuralları) + K59 cetvel v2 / French, K58 French dosya adları,
K57 gelir etiket sırası ve K60_veri uygunluk / kesik tanımlarının sha256'sı. `python -I K60.py kos --donem ...` bu mühürle, aşağıdaki veri
sha256'larıyla ve bu dosya git'e işlenmiş, sonradan değişmemişse başlar; biri tutmazsa koşu durur.)

## Veri (sha256; her koşunun başında yeniden hesaplanır)
- k60_fiyat: sha256 a795410c999b166d8e8e12a20d638b2ad07ec63ec963b5334f0d6abe99470408 (4755 dosya)
- k60_secframes: sha256 995fb342cbfe782b70adf17439ed537f4d574856460056e4bf477b9c47f0dd8b (1781 dosya)
- eski_secframes: sha256 aca462674de19f06ec4f9e98767d6a5bb2735fb61598bbcc4591271b738dd0c7 (206 dosya)
- company_tickers.json: sha256 6f9cc4500a98fb4c048328d7df392ed48c092613ec0c3e93cd6c7a3502886074 (1 dosya)
- k35_sic.csv: sha256 1ac089db38678ef6d62b0e22562822f21d90fce6d96845dd4ea8d52e98ec52c9 (1 dosya)
- F-F_Research_Data_Factors_daily_CSV.zip: sha256 96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89 (1 dosya)
- F-F_Research_Data_5_Factors_2x3_CSV.zip: sha256 17d7a575e71d6764a70ddec3f8d887756c0eebf3a60f64d6ba95d2adde3fed26 (1 dosya)
- F-F_Momentum_Factor_CSV.zip: sha256 27ed60e5b2caa9ea334a261cddfa864a9926f6bf45e9677c95dfd835c5abb315 (1 dosya)
k60_fiyat ve k60_secframes = K60_veri manifestinin klasör özeti (ada göre sıralı 'dosya adı:sha256' satırlarının sha256'sı; her dosya diskten
yeniden özetlenir). eski_secframes = K59 girdisi olan /tmp/secframes'ten okunan çerçeveler (aynı kural). k35_sic.csv = git'teki dosyanın
özeti (origin/islenmis-veri:k35/k35_sic.csv). SEC'e ve başka hiçbir yere istek atılmaz; önbellek eksikse ya da indirme durumu 'tamam' değilse koşu durur.

## 0. Soru, hedef çıktı, sınır
Soru: ölçülebilir hangi özellik büyük kazananların ve büyük kaybedenlerin OLASILIĞINI değiştiriyor, hangisi maliyetten sonra fazla getiri
bırakıyor? Hedef çıktı (CLAUDE.md 'Sonuç dili'): OLASILIK TABLOSU = her seçilmiş özellik için taban oran, P(12 ayda >= +%100), kaç kat (lift)
ve aralığı, aynısı -%50 için, dönem dönem. Ortalama getiri (R1) ikinci sırada raporlanır.
İZ ilan EDİLEMEZ: CLAUDE.md standardı (FI_OLCUT; ABD + Avrupa dört hücre) değişmedi; bu çalışma yalnız ABD, yalnız yaşayanlar. K60'ın
verebileceği en yüksek etiketler 'K60-İZ ADAYI', 'K60-OLASILIK İZİ', 'K60-KAÇINMA İZİ' (§7); standart değişikliği Cemal'in kararıdır.
Bu ön kayıttan ÖNCE görülmüş ilgili sonuçlar (kör olmayan kısım): K58 / K59 / K59-B (momentum, kârlılık, COMP4, DOSYA_Y 2016-26 ve 2021-26
dönemlerinde, başka evrenlerde ve yalnız R1 ile ölçüldü; COMP4 PORTFÖY-ADAY çıkmadı). K60 evreni (2010'dan Yahoo, 3000+ hisse), dönemleri
(KEŞİF 2012-2021) ve R2 cetveli yenidir; MOM_12_1, ROE_TTM, NSI_1Y, SALES_ACCEL, VOL_60D, HIGH52, STREV_1M, SIZE_ME, COMP4, DOSYA_Y satırlarının
2016 / 2021 sonrası R1 davranışı kısmen bilinmektedir: bu 10 satır R1 için tam kör sayılmaz (raporda 'kör değil' diye yazılır). R2 hiçbir satırda görülmedi.
Faz 1'de gerçek veride yalnız `kapsam` koşuldu (hisse / ay / sinyal başına SAYI; §12).

## 1. Kütüphane (77 sinyal ölçülür; 44 envanter satırı bu turda ölçülmez)
Kaynak: arastirma_cikti/yol_haritasi/SINYAL_ENVANTERI.md. Listede olmayan sinyal sonradan EKLENMEZ (yol haritası §5 kural 1); eklenecekse yeni tur.
Simgeler: t = oluşum ayının son işlem günü, m = o ayın sırası; A = temettü + bölünme düzeltmeli kapanış (Yahoo adjclose), C = bölünme
düzeltmeli kapanış; ay sonu değerleri en çok 5 gün ileri taşınır. ç0 = bilgi tarihi < t olan en son çeyrek (çeyrek sonu t'den en çok
200 gün önce); y0 = bilgi tarihi < t olan en son mali yıl (yıl sonu t'den en çok 550 gün önce). 'son 4 çeyrek' = ç0 .. ç0-3 toplamı
(dördü de bilinmeli). Gelir = K57 etiket sırası (Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet); bir formüldeki bütün çeyrekleri aynı etiketten olan ilk
etiket. Toplam varlık = Assets, yoksa LiabilitiesAndStockholdersEquity. Toplam yükümlülük = Liabilities, yoksa varlık - özkaynak. Uzun vadeli
borç = LongTermDebt, yoksa LongTermDebtNoncurrent. Satışların maliyeti = CostOfRevenue, yoksa CostOfGoodsAndServicesSold. Temettü =
PaymentsOfDividends, yoksa PaymentsOfDividendsCommonStock. PD (piyasa değeri) = C(t) x pay sayısı (bugünkü pay biriminde; §3).
yön: '+' = ölçü yüksekse beklenen getiri yüksek; '-' = düşük; '?' = iki yönlü. 'ÜST uç' = beklenen yöne göre en iyi %10; 'ALT uç' = en kötü %10.

| kod | aile | yön | tür | tanım (formül, pencere) | kaynak |
|---|---|---|---|---|---|
| MOM_12_1 | MOM | + | surekli | A(m-1) / A(m-12) - 1 | Jegadeesh-Titman 1993 |
| MOM_6_1 | MOM | + | surekli | A(m-1) / A(m-6) - 1 | Jegadeesh-Titman 1993 |
| MOM_INT_12_7 | MOM | + | surekli | A(m-6) / A(m-12) - 1 (t-12 .. t-7 ayları) | Novy-Marx 2012 |
| MOM_RES_12_1 | MOM | + | surekli | 36 aylık (m-35 .. m, hepsi dolu) aylık fazla getirinin French MKT-RF, SMB, HML üzerine sabitli EKK artıkları; m-11 .. m-1 artıklarının toplamı / aynı 11 artığın std'si (ddof 1) | Blitz-Huij-Martens 2011 |
| HIGH52 | MOM | + | surekli | C(t) / son 252 işlem gününün en yüksek gün içi fiyatı (en az 200 gözlem) | George-Hwang 2004 |
| STREV_1M | MOM | - | surekli | A(m) / A(m-1) - 1 (geçen ayın getirisi) | Jegadeesh 1990 |
| LTREV_60_13 | MOM | - | surekli | A(m-12) / A(m-60) - 1 | De Bondt-Thaler 1985 |
| MOM_FIP | MOM | + | surekli | ay içi yüzdelik sıra ortalaması: MOM_12_1 ve süreklilik = işaret(MOM_12_1) x (artı gün payı - eksi gün payı), günler (m-12 ay sonu, m-1 ay sonu], en az 200 gün; ikisi de olmalı | Da-Gurun-Warachka 2014 |
| TREND_MA | MOM | + | surekli | x_L = L günlük ortalama C / C(t), L = 3, 5, 10, 20, 50, 100, 200; her ay k: getiri(k) ~ x_L(k-1) kesit EKK'si (k-1'de uygun hisseler); sinyal(m) = Σ_L [son 12 ayın (m-11 .. m) katsayı ortalaması] x x_L(m) | Han-Zhou-Zhu 2016 |
| BM | VAL | + | surekli | StockholdersEquity(ç0) / PD; özkaynak > 0 | Fama-French 1992 |
| EP | VAL | + | surekli | NetIncomeLoss son 4 çeyrek toplamı / PD | Basu 1977 |
| SP | VAL | + | surekli | gelir son 4 çeyrek toplamı / PD | Barbee-Mukherji-Raines 1996 |
| AM | VAL | + | surekli | toplam varlık(ç0) / PD | Fama-French 1992 |
| LEV_MKT | VAL | + | surekli | toplam yükümlülük(ç0) / PD | Bhandari 1988 |
| CFP | VAL | + | surekli | faaliyet nakit akışı (y0, yıllık) / PD | Desai-Rajgopal-Venkatachalam 2004 |
| EV_EBITDA | VAL | - | surekli | (PD + uzun vadeli borç(ç0; yoksa 0) - nakit(ç0; yoksa 0)) / (OperatingIncomeLoss son 4 çeyrek + amortisman (y0, yıllık)); payda > 0 şart | Loughran-Wellman 2011 |
| NET_PAYOUT_YLD | VAL | + | surekli | (temettü + geri alım - hisse ihracı geliri) (y0, yıllık; olmayan kalem 0; y0'da faaliyet nakit akışı olmalı) / PD | Boudoukh et al. 2007 |
| ROE_TTM | PRF | + | surekli | NetIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); özkaynak > 0 | Haugen-Baker 1996 |
| ROA_Q | PRF | + | surekli | NetIncomeLoss(ç0) / toplam varlık(ç0-1) | Balakrishnan-Bartov-Faurel 2010 |
| D_ASSET_TURN | PRF | + | surekli | gelir 4ç(ç0) / varlık(ç0) - gelir 4ç(ç0-4) / varlık(ç0-4) | Soliman 2008 |
| SALES_ACCEL | PRF | + | surekli | gelir(ç0) / [gelir(ç0-1) + gelir(ç0-2)] / 2; payda > 0 (K59 S7) | proje ölçüsü (şüpheli: yayımlanmış kanıt yok) |
| ACCRUALS | PRF | - | surekli | (net kâr(y0) - faaliyet nakit akışı(y0)) / [varlık(y0 sonu) + varlık(y0-1 sonu)] / 2 | Sloan 1996 |
| GP_A | PRF | + | surekli | brüt kâr son 4 çeyrek / varlık(ç0); brüt kâr = GrossProfit, yoksa gelir - satışların maliyeti | Novy-Marx 2013 |
| OP_BE | PRF | + | surekli | OperatingIncomeLoss son 4 çeyrek / StockholdersEquity(ç0); özkaynak > 0 | Fama-French 2006 |
| CBOP_A | PRF | + | surekli | faaliyet nakit akışı(y0) / varlık(y0 sonu) (yaklaşık sürüm) | Ball et al. 2016 |
| F_SCORE | PRF | + | surekli | Piotroski 9 ikili ölçü, yıllık (y0, y0-1): ROA > 0; OCF > 0; ΔROA > 0; OCF > net kâr; Δ(uzun vadeli borç / varlık) < 0; Δ(dönen varlık / kısa vadeli yükümlülük) > 0; hisse ihracı geliri <= 0 ya da yok; Δ brüt marj > 0; Δ(gelir / varlık) > 0. En az 7 ölçü hesaplanabilmeli; puan = toplam x 9 / hesaplanan sayı; eşitlik ROA ile bozulur (+0,001 x kırpılmış ROA) | Piotroski 2000 |
| NOA | PRF | - | surekli | (uzun vadeli borç(ç0; yoksa 0) + özkaynak(ç0) - nakit(ç0)) / varlık(ç0-4) (yaklaşık) | Hirshleifer et al. 2004 |
| OPLEV | PRF | + | surekli | (gelir 4ç - OperatingIncomeLoss 4ç) / varlık(ç0) (toplam faaliyet gideri / varlık) | Novy-Marx 2011 |
| RD_ME | PRF | + | surekli | ResearchAndDevelopmentExpense son 4 çeyrek / PD; yalnız Ar-Ge bildirenler | Chan-Lakonishok-Sougiannis 2001 |
| TAX_CHG | PRF | + | surekli | (IncomeTaxExpenseBenefit(ç0) - (ç0-4)) / varlık(ç0-4) | Thomas-Zhang 2011 |
| ASSET_G | INV | - | surekli | varlık(ç0) / varlık(ç0-4) - 1 | Cooper-Gulen-Schill 2008 |
| NSI_1Y | INV | - | surekli | ln(pay(t) / pay(t - 12 ay)); pay bölünme düzeltmeli, iki uç aynı kaynaktan; oran > 5 ya da < 1/5 ise veri yok | Pontiff-Woodgate 2008 |
| BE_G | INV | - | surekli | özkaynak(ç0) / özkaynak(ç0-4) - 1; ikisi de > 0 | Lockwood-Prombutr 2010 |
| NSI_5Y | INV | - | surekli | ln(pay(t) / pay(t - 60 ay)); oran > 20 ya da < 1/20 ise veri yok | Daniel-Titman 2006 |
| NEF | INV | - | surekli | (hisse ihracı geliri - geri alım - temettü) (y0; olmayan kalem 0) / [varlık(y0 sonu) + varlık(y0-1 sonu)] / 2 | Bradshaw-Richardson-Sloan 2006 |
| NDF_BS | INV | - | surekli | (uzun vadeli borç(ç0) - (ç0-4)) / [varlık(ç0) + varlık(ç0-4)] / 2 (bilanço yaklaşımı) | Bradshaw-Richardson-Sloan 2006 |
| BUYBACK_YLD | INV | + | surekli | geri alım ödemesi (y0; yoksa 0, y0'da faaliyet nakit akışı olmalı) / PD | Ikenberry-Lakonishok-Vermaelen 1995 |
| CAPEX_G | INV | - | surekli | yatırım harcaması(y0) / [(y0-1) + (y0-2)] / 2 - 1; payda > 0 | Anderson-Garcia-Feijoo 2006 |
| EAR_ANN | EAR | + | surekli | açıklama günü VEKİLİ d* = 10-Q / 10-K başvuru gününe kadarki 30 takvim günü içindeki (başvuru günü dahil) EN SON 8-K günü, yoksa başvuru günü. Tepki = d*'den önceki, d* ve sonraki işlem günlerinin bileşik getirisi - aynı günlerde French piyasa getirisi. Penceresi t'ye kadar bitmiş ve son 63 işlem günü içindeki EN SON olayın tepkisi | Chan-Jegadeesh-Lakonishok 1996 |
| EAR_FILE | EAR | + | surekli | EAR_ANN ile aynı, olay günü 10-Q / 10-K başvuru gününün kendisi (K59 S4'ün 2021-22 tanımı) | Chan-Jegadeesh-Lakonishok 1996 |
| SUE_SRW | EAR | + | surekli | (net kâr(ç0) - net kâr(ç0-4)) / son 8 yıllık farkın (ç0 .. ç0-7) std'si (ddof 1) | Foster-Olsen-Shevlin 1984 |
| REV_SURP | EAR | + | surekli | SUE_SRW'nin gelirle hesaplanmışı | Jegadeesh-Livnat 2006 |
| EARN_STREAK | EAR | + | surekli | art arda aynı işaretli yıllık net kâr farkı sayısı (ç0'dan geriye, en çok 8), işaretli | Loh-Warachka 2012 |
| EAR_VOL | EAR | + | surekli | d* günündeki hacim / önceki 50 işlem gününün ortalama hacmi (en az 30); son 63 işlem günü içindeki en son olay | Garfinkel-Sokobin 2006 |
| VOL_60D | RSK | - | surekli | son 60 işlem gününün günlük getiri std'si (en az 40) | Ang-Hodrick-Xing-Zhang 2006 |
| IVOL_FF3 | RSK | - | surekli | t'nin takvim ayındaki günlük fazla getirinin French günlük MKT-RF, SMB, HML üzerine EKK artıklarının std'si (en az 15 gün) | Ang-Hodrick-Xing-Zhang 2006 |
| BETA_BAB | RSK | - | surekli | korelasyon(hisse, piyasa; son 1260 gün, en az 504) x σ_hisse / σ_piyasa (son 252 gün, en az 120); günlük basit getiri, piyasa = French MKT | Frazzini-Pedersen 2014 |
| MAX5 | RSK | - | surekli | t'nin takvim ayındaki en yüksek 5 günlük getirinin ortalaması (en az 15 gün) | Bali-Cakici-Whitelaw 2011 |
| SKEW_TOT | RSK | - | surekli | t'nin takvim ayındaki günlük getirilerin çarpıklığı (en az 15 gün) | Bali-Engle-Murray 2015 |
| ISKEW | RSK | - | surekli | IVOL_FF3 artıklarının çarpıklığı | Boyer-Mitton-Vorkink 2010 |
| PRICE_LVL | RSK | - | surekli | ln(o günkü fiyat) (ölçü yüksek = pahalı; beklenen yön düşük fiyat lehine) | Blume-Husic 1973 |
| SIZE_ME | LIQ | - | surekli | ln(PD) | Banz 1981 |
| AMIHUD | LIQ | + | surekli | son 252 işlem gününde (en az 150) ortalama |günlük getiri| / (C x hacim); işlem değeri 0 olan gün dışarıda | Amihud 2002 |
| TURN_12M | LIQ | - | surekli | son 252 işlem gününün (en az 150) ortalama hacmi / pay sayısı (ikisi de bugünkü pay biriminde) | Datar-Naik-Radcliffe 1998 |
| DOLVOL | LIQ | - | surekli | ln(m-1 ayının ortalama günlük işlem değeri) | Brennan-Chordia-Subrahmanyam 1998 |
| VOL_SHOCK | LIQ | + | surekli | son 5 işlem gününün ortalama hacmi / ondan önceki 50 günün ortalama hacmi (en az 3 ve 30 gözlem) | Gervais-Kaniel-Mingelgrin 2001 |
| SPREAD_CS | LIQ | + | surekli | Corwin-Schultz alış-satış farkı tahmini, t'nin takvim ayındaki günlük çiftlerin ortalaması (eksi tahmin 0; en az 12 çift) | Corwin-Schultz 2012 |
| GAP_OVN | LIQ | ? | surekli | t'nin takvim ayındaki gece getirilerinin toplamı Σ ln(açılış(g) / C(g-1)) (en az 15 gün) | Lou-Polk-Skouras 2019 |
| SEAS_1 | SEA | + | surekli | m-11 ayının getirisi (gelecek ayla aynı takvim ayı, bir yıl önce) | Heston-Sadka 2008 |
| SEAS_2_5 | SEA | + | surekli | m-23, m-35, m-47, m-59 aylarının getiri ortalaması (dördü de olmalı) | Heston-Sadka 2008 |
| EA_MONTH | SEA | + | bayrak | gelecek ayla aynı takvim ayında bir yıl önce açıklama günü vekili d* var (o aya kadar en az bir 10-Q / 10-K başvurusu olmalı) | Frazzini-Lamont 2007 |
| DIV_MONTH | SEA | + | bayrak | gelecek aydan 3, 6 ya da 12 ay önceki takvim ayında temettü hak düşüm günü var | Hartzmark-Solomon 2013 |
| RUNWAY | DIS | - | surekli | nakit tüketim hızı = -faaliyet nakit akışı(y0) / nakit(ç0); nakit > 0 (yüksek = hızlı tüketim; yıllık sürüm) | proje ölçüsü (K31 M3) |
| NT_LATE | DIS | - | bayrak | son 60 takvim gününde (t hariç) NT 10-K / NT 10-Q başvurusu | Bartov-Konchitchki 2017 |
| CHS_FAIL | DIS | - | surekli | Campbell-Hilscher-Szilagyi 12 ay ufuklu batma logiti (katsayılar makaleden sabit; girdiler ay içinde %5 / %95'te kırpılır) | Campbell-Hilscher-Szilagyi 2008 |
| O_SCORE | DIS | - | surekli | Ohlson (1980) batma puanı, yıllık (y0, y0-1); FFO yerine faaliyet nakit akışı | Dichev 1998 |
| IND_MOM_6 | SEC | + | surekli | aynı SIC 2 hane sektöründeki uygun hisselerin (en az 5) A(m) / A(m-6) - 1 eşit ağırlıklı ortalaması | Moskowitz-Grinblatt 1999 |
| IND_LEAD_BIG | SEC | + | surekli | aynı SIC 2 hane sektöründe (PD'si olan en az 10 uygun hisse) m-1 ay sonu PD'sine göre en büyük %30'un m ayı getirisi ortalaması; yalnız kalan %70'e atanır | Hou 2007 |
| ACT_13D | OWN | + | bayrak | son 60 takvim gününde SC 13D / SCHEDULE 13D (değişiklik hariç) başvurusu | Brav et al. 2008 |
| E_S3 | EVT | - | bayrak | son 90 takvim gününde S-3 / S-3ASR | Loughran-Ritter 1995 |
| E_424B5 | EVT | - | bayrak | son 60 takvim gününde 424B5 | Loughran-Ritter 1995; Billett et al. 2019 |
| E_TENDER_SELF | EVT | + | bayrak | son 90 takvim gününde SC TO-I | Peyer-Vermaelen 2009 |
| E_IPO_3Y | EVT | - | bayrak | ilk işlem günü (Yahoo) t'den en çok 1095 gün önce | Ritter 1991 |
| E_SPLIT | EVT | + | bayrak | son 365 günde oranı >= 2 olan ileri bölünme | Ikenberry-Rankine-Stice 1996 |
| E_RSPLIT | EVT | - | bayrak | son 365 günde ters bölünme (oran < 1) | Kim-Klein-Rosenfeld 2008 |
| E_DIV_INIT | EVT | + | bayrak | son 365 günde temettü var, ondan önceki 730 günde yok (fiyat geçmişi en az 1095 gün) | Michaely-Thaler-Womack 1995 |
| E_DIV_OMIT | EVT | - | bayrak | (t-730, t-365] aralığında en az 2 temettü var, son 365 günde yok | Michaely-Thaler-Womack 1995 |

Aile başına sayım:

| aile | ölçülen | bu turda ölçülmeyen |
|---|---|---|
| MOM | 9 | 0 |
| VAL | 8 | 0 |
| PRF | 13 | 0 |
| INV | 8 | 3 |
| EAR | 6 | 7 |
| RSK | 7 | 0 |
| LIQ | 7 | 0 |
| SEA | 4 | 1 |
| DIS | 4 | 2 |
| SEC | 2 | 5 |
| OWN | 1 | 11 |
| EVT | 8 | 12 |
| TXT | 0 | 3 |

Bu turda ÖLÇÜLMEYEN satırlar (DALGA 2 = K61, başka indirme ister; YOK = ücretsiz veri yok; ÖLÇÜLEMEZ = bu evren / cetvelle anlamsız):
- INV_A (INV): DALGA 2: PropertyPlantAndEquipmentNet, InventoryNet etiketleri inmedi
- INVTRY_G (INV): DALGA 2: InventoryNet inmedi
- HIRE_G (INV): YOK: XBRL'de düzenli etiket yok
- SUE_ANALYST (EAR): DALGA 2: Nasdaq takvimi 2022-12+; KEŞİF'te yok
- REC_UP (EAR): DALGA 2: Yahoo analist günlüğü
- REC_DOWN (EAR): DALGA 2: Yahoo analist günlüğü
- PT_REV (EAR): DALGA 2: Yahoo analist günlüğü
- N_ANALYST_CHG (EAR): DALGA 2: Yahoo analist günlüğü
- EPS_REV (EAR): YOK: IBES ücretli
- GUIDANCE_UP (EAR): YOK: metin
- INS_BUY_90 (OWN): DALGA 2: Form 4 (2012-2020 inmedi)
- INS_CLUSTER (OWN): DALGA 2: Form 4
- INS_OPP_BUY (OWN): DALGA 2: Form 4
- INS_SELL_90 (OWN): DALGA 2: Form 4
- INS_OPP_SELL (OWN): DALGA 2: Form 4
- IO_BREADTH_CHG (OWN): DALGA 2: 13F + CUSIP
- IO_CHG (OWN): DALGA 2: 13F + CUSIP
- SI_RATIO (OWN): DALGA 2: FINRA açığa satış
- DTC (OWN): DALGA 2: FINRA açığa satış
- SI_LOW (OWN): DALGA 2: FINRA açığa satış
- SHORT_VOL (OWN): DALGA 2: FINRA Reg SHO
- TAXLOSS_JAN (SEA): BU CETVELLE ÖLÇÜLEMEZ: yılda tek oluşum ayı (KEŞİF'te 10 gözlem < 36)
- Z_SCORE (DIS): DALGA 2: RetainedEarningsAccumulatedDeficit inmedi
- GC_FLAG (DIS): DALGA 2: EDGAR tam metin arama
- E_101 (EVT): DALGA 2: 8-K madde kodu
- E_201 (EVT): DALGA 2: 8-K madde kodu
- E_205_206 (EVT): DALGA 2: 8-K madde kodu
- E_301 (EVT): DALGA 2: 8-K madde kodu
- E_302 (EVT): DALGA 2: 8-K madde kodu
- E_401 (EVT): DALGA 2: 8-K madde kodu
- E_402 (EVT): DALGA 2: 8-K madde kodu
- E_502 (EVT): DALGA 2: 8-K madde kodu
- E_LOCKUP (EVT): BU EVRENDE ÖLÇÜLEMEZ: 252 gün geçmiş şartı halka arz + 180 gün penceresini dışarıda bırakır
- E_MA_TARGET (EVT): BU EVRENDE ÖLÇÜLEMEZ: devralınan şirket bugün yaşamıyor (yalnız yaşayanlar)
- E_IDX_ADD (EVT): DALGA 2: S&P 500 değişiklik tablosu
- E_SPINOFF (EVT): DALGA 2: 10-12B + evren dışı CIK eşlemesi
- COMM_LINK (SEC): DALGA 2: tanım belirsiz ('şüpheli'), k36 serilerinin bilgi tarihi denetlenmedi
- IO_MOM_CUST (SEC): DALGA 2: BEA girdi-çıktı tabloları
- IO_MOM_SUPP (SEC): DALGA 2: BEA girdi-çıktı tabloları
- GEO_MOM (SEC): DALGA 2: SEC adres alanı
- CUST_MOM (SEC): YOK: müşteri eşlemesi ücretli
- LAZY_SIM (TXT): DALGA 2: 10-K tam metinleri
- TONE_NEG (TXT): DALGA 2: Loughran-McDonald özetleri
- TONE_CHG (TXT): DALGA 2: Loughran-McDonald özetleri

Bileşikler (ölçümden önce yazıldı; seçim yok). Yöntem K59 ile aynı: üyelerin ay içi yüzdelik sıralarının ((sıra - 0,5) / n; uygun ve o
üyesi olan hisseler arasında, beklenen yön uygulanmış, eşitlikte ortalama sıra) ortalaması; hissenin en az 'min' üyede değeri olmalı.
AİLE bileşiğine ailenin SÜREKLİ ve yönü belli üyeleri girer (bayrak ve '?' sinyaller girmez); OWN ve EVT aileleri yalnız bayraktan oluştuğu
için bileşikleri yoktur. Ek bileşen REV_YOY: gelir(ç0) / gelir(ç0-4) - 1; ikisi de > 0 (K59 X1). Yalnız DOSYA_Y üyesidir; tek başına ÖLÇÜLMEZ.
- AILE_MOM (AİLE): MOM_12_1, MOM_6_1, MOM_INT_12_7, MOM_RES_12_1, HIGH52, STREV_1M, LTREV_60_13, MOM_FIP, TREND_MA; en az 5 üye.
- AILE_VAL (AİLE): BM, EP, SP, AM, LEV_MKT, CFP, EV_EBITDA, NET_PAYOUT_YLD; en az 4 üye.
- AILE_PRF (AİLE): ROE_TTM, ROA_Q, D_ASSET_TURN, SALES_ACCEL, ACCRUALS, GP_A, OP_BE, CBOP_A, F_SCORE, NOA, OPLEV, RD_ME, TAX_CHG; en az 7 üye.
- AILE_INV (AİLE): ASSET_G, NSI_1Y, BE_G, NSI_5Y, NEF, NDF_BS, BUYBACK_YLD, CAPEX_G; en az 4 üye.
- AILE_EAR (AİLE): EAR_ANN, EAR_FILE, SUE_SRW, REV_SURP, EARN_STREAK, EAR_VOL; en az 3 üye.
- AILE_RSK (AİLE): VOL_60D, IVOL_FF3, BETA_BAB, MAX5, SKEW_TOT, ISKEW, PRICE_LVL; en az 4 üye.
- AILE_LIQ (AİLE): SIZE_ME, AMIHUD, TURN_12M, DOLVOL, VOL_SHOCK, SPREAD_CS; en az 3 üye.
- AILE_SEA (AİLE): SEAS_1, SEAS_2_5; en az 1 üye.
- AILE_DIS (AİLE): RUNWAY, CHS_FAIL, O_SCORE; en az 2 üye.
- AILE_SEC (AİLE): IND_MOM_6, IND_LEAD_BIG; en az 1 üye.
- COMP4 (K59): MOM_12_1, EAR_ANN, ROE_TTM, NSI_1Y; en az 3 üye.
- DOSYA_Y (K59): SALES_ACCEL, REV_YOY, ROE_TTM, NSI_1Y, EAR_ANN; en az 4 üye.

## 2. Dönemler (OLUŞUM ayına göre)
- KEŞİF 2012-01 .. 2021-12; DOĞRULAMA 2022-01 .. 2023-12; KASA 2024-01 .. ileri penceresi 2026-08-31'e kadar biten son oluşum ayı
  (R1: 1 ay; R2: 12 / 6 / 3 ay; pencere sonu veri kesiğini aşan oluşum ayı ÖLÇÜLMEZ).
- Fon krizi kesiği: fiyatlar 2026-08-31'de kesilir (CLAUDE.md, 27 Ekim 2026).

## 3. Evren ve zaman kuralları
- Evren: K60_veri fiyat önbelleği (K57-B evren tablosu + V_ABD; yalnız BUGÜN borsa kodu olan şirketler). Yahoo düzeltilmiş kapanışı <= 0 olan
  günler yok sayılır. Tür EQUITY; Yahoo'nun geçmişini
  kırptığı hisseler ('kırpık': ilk verilen gün ilk işlem gününden 10 günden fazla sonra) kural gereği DIŞARIDA. En az 3000 hisse
  yüklenemezse koşu durur. İşlem takvimi = hisselerin en az %20 x medyan kadarının işlem gördüğü günler.
- UYGUNLUK (her ay sonu t, yalnız t ve öncesi bilgi; K59 U2 ile aynı eşikler): t'ye kadar en az 252 günlük kapanış; o günkü fiyat
  (C x t'den sonraki bölünmelerin çarpımı) >= 2 $; son 20 işlem gününün (en az 15 gözlem) medyan işlem değeri (C x hacim) >= 1 milyon $;
  ay sonu m ve m-1 kapanışı var. Uygun hisse < 100 olan ay atlanır.
- BİLGİ TARİHİ (gerçek başvuru günü): EDGAR çeyreklik başvuru dizini (master.gz, 2009Q1-2026Q3) İNDİ ve kullanılır. Frames yanıtında
  başvuru günü ve dizinde dönem alanı olmadığı için eşleme kuralı: bir çeyreğin bilgi tarihi = şirketin, çeyrek sonundan en az 15 gün SONRA
  yaptığı ilk dönemsel başvurunun günü (ilk 15 gündeki başvuru geciken önceki dönemin başvurusu sayılır); çeyrek sonu şirketin bir mali yıl sonuna ±10 gün yakınsa form 10-K, 10-KT, 10-K405, 10-KSB, 20-F, 40-F, değilse 10-Q, 10-QT, 10-QSB
  (düzeltme başvuruları /A sayılmaz; şirketin hiç yıllık çerçevesi yoksa iki aileden ilk gelen). Eşleşen başvuru yoksa YEDEK: çeyrek sonu + 90 gün,
  mali yıl sonu + 120 gün. Yıllık kalemler ve yıllıktan türetilen 4. çeyrek = o mali yılın 10-K gününde bilinir. Bir değer ancak
  bilgi tarihi < t ise (başvuru + 1 işlem günü kuralı) kullanılır.
- 4. çeyrek: çeyreklik çerçevede yoksa yıl - önceki üç çeyrek (yıllık süre 350-380 gün ve üç çeyrek de doluysa).
- PAY SAYISI: kapak sayfası sayısı (dei EntityCommonStockSharesOutstanding; tarihi kapak günü, bilgi tarihi = kapak gününden sonraki (dahil) ilk
  dönemsel başvuru, yoksa kapak günü + 60 gün; kapak günü t'den en çok 400 gün önce). Kapak sayısı x kapak gününden SONRAKİ bölünmelerin çarpımı
  = bugünkü pay birimi (Yahoo kapanışı ve hacmi de bu birimdedir). Kapak sayısı olmayan hisselerde yedek: bilanço pay sayısı
  (CommonStockSharesOutstanding, ç0), o da yoksa ağırlıklı ortalama seyreltilmiş pay (ç0); yedekler YALNIZ Yahoo'da hiç bölünme kaydı
  olmayan hisselerde kullanılır (frames eski dönem pay sayılarını bölünme sonrası yeniden bildirilmiş haliyle verebilir).
- İşlem zamanı: sinyal t kapanışında hesaplanır; R1 ay sonu kapanışından sonraki ay sonu kapanışına (K59 / K58 ile aynı), R2 ay sonu
  kapanışından h ay sonraki ay sonu kapanışına; getiri temettü dahil (A).

## 4. Cetvel R1 — portföy cetveli v2 (K59 ile aynı; K59.k59_cetvel_v2 ve K58.k58_portfoy çağrılır)
- Portföy: sinyali olan uygun hisselerin ÜST ucu (sayı = max(1, yuvarla(0.1 x sinyali olan uygun hisse))), eşit ağırlık, aylık dengeleme, 1 ay
  tutma, maliyet tek yön 10 bp x devir. Kıyas = BÜTÜN uygun evrenin eşit ağırlıklı getirisi. Aykırı getiri kırpması YOK.
- İstatistikler dönemin kendi ayları içinde: net fazla ortalaması ve NW t (gecikme 6); ardışık 3 alt dönemin en az 2'sinde fazla > 0;
  son %30 ayda fazla > 0; beta düzeltmeli alfa (portföy = alfa + beta x kıyas) ve NW t(alfa). 'cetvel v2 TUTAR' = K59'daki dört şart
  (t eşiği 2.0); her dönemde ayrı sütun olarak raporlanır. En az ölçüm ayı: KEŞİF 36, DOĞRULAMA 18, KASA 18.
- Ölçüm ayları: sürekli sinyalde dönemin içinde sinyali olan uygun hisse sayısının ilk kez >= 100 olduğu aydan dönem sonuna (K59 kuralı);
  bayrakta bayraklı uygun hisse >= 10 olan aylar.
- R1 istatistiği = t(alfa) (net). p değeri iki yönlü normal yaklaşımı. Bilgi sütunları: FF5 + UMD alfası, Sharpe, en büyük düşüş, devir,
  brüt (maliyetsiz) karşılıklar, en büyük üç katkı (hisse ve toplam getiri katkısındaki payı).

## 5. Cetvel R2 — OLASILIK TABLOSU
- Her sinyalin ÜST ve ALT ucu (bayrakta bayraklı grup) için, R1 ile aynı ölçüm aylarında (ileri penceresi veride biten aylar): h ay ileri
  toplam getiri F_h = A(m+h) / A(m) - 1 (m+h ay sonunda son 5 işlem gününde fiyatı olmayan hisse-ay dışarıda). ANA ufuk 12 ay; 6, 3 ay bilgi.
- P(F >= +%100), P(F >= +%50), P(F <= -%50), ortalama ve medyan F; aynıları BÜTÜN uygun evren için aynı aylarda (taban oran). Olasılık =
  hisse-ay havuzunda olay sayısı / hisse-ay sayısı (ay ağırlığı = o ayki hisse sayısı). LIFT = P(uç) / P(evren).
- Belirsizlik: ay kümeli DAİRESEL blok bootstrap; blok 12 ay, 500 çekiliş, tohum 60002 (çekiliş dizini yalnız ay sayısına bağlı; bütün sinyaller
  ve plasebolar aynı çekilişleri kullanır); %95 aralık = lift çekilişlerinin %2.5 ve %97.5 dilimleri. Örtüşen 12 aylık pencereler
  KABUL EDİLİR: komşu ayların sonuçları bağımlıdır, blok boyu bu yüzden 12 aydır; aralık yine de dar kalabilir (plasebo ile sınanır).
- p değeri (lift > 1): p_z = 1 - Φ(ln(lift) / sd(ln(lift çekilişleri))); ayrıca yüzdelik p = (1 + #(çekiliş lift <= 1)) / (çekiliş + 1) raporlanır.
- Ölçülebilirlik: en az 12 oluşum ayı ve uçta en az 200 hisse-ay.

## 6. KEŞİF: çoklu deneme muhasebesi ve seçim
- R1 ailesi (yaklaşık 90 hipotez; ölçülemeyenler düşer): yönü belli sürekli sinyallerin ve bileşiklerin ÜST ucu, '?' sinyallerin iki ucu,
  bayrakların bayraklı grubu. p = iki yönlü p(t(alfa)). Benjamini-Hochberg, yanlış keşif oranı %10.
- R2 ailesi (yaklaşık 166 hipotez): BÜTÜN sinyal ve bileşiklerin iki ucu (bayrakta bayraklı grup); çünkü beklenen yön ortalama getiri içindir,
  sağ kuyruk olasılığı için değil (piyango tipi hisselerde ikisi ters düşebilir). p = '+%100 lift > 1' p_z. BH %10.
- R2K ailesi (kaçınma; aynı satırlar): p = '-%50 lift > 1' p_z. BH %10.
- PLASEBO: 200 rastgele sinyal (her ay uygun hisselere rastgele sıra; numpy default_rng(60100 + i)), ÜST uç, iki cetvelden de geçer.
  'Plasebo en büyüğü' = 200 plasebo istatistiğinden, ailenin hipotez sayısı kadar (yerine koyarak) çekilen kümenin en büyüğü; 2000 tekrar
  (tohum 60003); eşik = bu en büyüklerin %95'lik dilimi. Plasebo istatistiği: R1'de BRÜT t(alfa) (artı yön için en büyüğü, eksi yön için
  -(brüt t)'nin en büyüğü), R2'de +%100 lift, R2K'de -%50 lift. Neden brüt: rastgele portföy her ay baştan kurulur (devir ~%180), net t'si
  maliyet yüzünden hep eksidir ve kıyas olmaz; 'bilgisiz ve maliyetsiz' portföyün t dağılımı (sıfır çevresinde) doğru kıyastır. Sinyalin
  kendisi artı yönde NET t(alfa)'sıyla bu eşiği aşmalıdır (daha sıkı); eksi yönde sinyalin BRÜT t'si kullanılır (tutulmayacak bir portföyün
  işlem maliyeti onun 'kötülüğü' sayılmaz).
  placebo.csv'de plasebo dağılımı ve eşikler yazılır. Cetvel sağlaması: plasebonun 'cetvel v2 TUTAR' oranı (net ya da brüt) > %5 ise
  R1 yolu KAPANIR (hüküm yok); plasebonun 'lift alt sınırı > 1' oranı > %5 ise raporda 'R2 aralığı dar' diye yazılır (seçim plasebo
  en büyüğü eşiğiyle zaten korunur).
- KEŞİF-SEÇİLİ ⇔ (R1 ARTI: BH'den geçer VE net t(alfa) > plasebo brüt t en büyüğü eşiği, YA DA net t(alfa) > 3.0) YA DA (R1 EKSİ: BH'den geçer VE
  -(brüt t(alfa)) > plasebo eşiği, YA DA brüt t(alfa) < -3.0) YA DA (R2: BH'den geçer VE +%100 lift > plasebo eşiği) YA DA (R2K: BH'den geçer VE
  -%50 lift > plasebo eşiği). Seçim (sinyal, uç) çifti içindir; R1 yolunda yön (artı / eksi) secili.json'a yazılır.
- secili.json = seçilenler + eşikler + §8 model katsayıları; `dogrulama` ancak bu dosya git'e işlendikten sonra başlar.
- Nedeni yazılamayan sinyal (SALES_ACCEL, RUNWAY: proje ölçüsü; yayımlanmış kanıt yok) seçilse de 'şüpheli' işaretlenir (yol haritası §5 kural 6).

## 7. DOĞRULAMA, KASA ve etiketler
- DOĞRULAMA'ya girenler: KEŞİF-SEÇİLİ (sinyal, uç) çiftleri + BÜTÜN bileşiklerin iki ucu (seçilmemiş bileşik 'AİLE BİLGİSİ'dir, etiket alamaz).
- Geçme kuralları (dönemin kendi ayları; aynı uç = aynı yön):
  R1: net ortalama fazla > 0 VE alfa > 0 VE net t(alfa) > 1.65 (24 ay kısa; önceden yazılı tek yönlü eşik) VE net t(alfa) > aynı dönemin 200
      plasebosunun BRÜT t(alfa)'larının %95'lik dilimi (kalibrasyon şartı: kısa dönemde NW t şişebilir). KEŞİF'te yönü EKSİ seçilen çiftte ayna kural BRÜT değerlerle: brüt fazla < 0
      VE brüt alfa < 0 VE brüt t(alfa) < -1.65 VE brüt t(alfa) < plasebo brüt t'lerinin %5'lik dilimi (bilgi).
  R2: +%100 lift %95 aralığının alt sınırı > 1 VE lift > aynı dönemin plasebo lift'lerinin %95'lik dilimi.
  R2K: -%50 lift alt sınırı > 1 VE lift > plasebo -%50 lift'lerinin %95'lik dilimi.
  DOĞRULAMA'dan GEÇER ⇔ R1 ya da R2 ya da R2K geçer. Geçenler dogrulama_gecen.json'a yazılır.
- KASA: yalnız DOĞRULAMA'dan geçenler; TEK AÇILIŞ (kasa_acildi.json işareti ölçümden önce yazılır; ikinci `kos --donem kasa` durur);
  geçme kuralları aynı. KASA ancak dogrulama_gecen.json git'e işlendikten sonra açılır.
- ETİKETLER (yalnız KEŞİF-SEÇİLİ çiftler):
  'K60-İZ ADAYI' ⇔ KEŞİF'te R1 yolundan artı yönle seçildi VE DOĞRULAMA R1 geçti VE KASA R1 geçti.
  'K60-OLASILIK İZİ' ⇔ KEŞİF'te R2 yolundan seçildi VE DOĞRULAMA R2 geçti VE KASA R2 geçti (+%100 olasılığını artırır).
  'K60-KAÇINMA İZİ' ⇔ üç döneme de girdi VE üçünde de -%50 lift alt sınırı > 1 (KEŞİF'te ayrıca R2K yolundan seçilmiş olmalı). Yalnız
      yaşayanlar evreninde batanlar yok: ölçülen -%50 olasılığı ve lift ALT SINIRDIR (gerçek kaçınma faydası daha büyük olabilir).
  'K60-R1 TERS (bilgi)' ⇔ R1 yolundan eksi yönle seçildi ve iki dönemde de ayna kural tuttu (uç evrenin gerisinde kalıyor; kaçınma bilgisi).
  Hiçbiri İZ değildir (§0).

## 8. Birleşik olasılık modeli (BİLGİ; önceden yazıldı, ayar yok)
Lojistik regresyon, KEŞİF'te: hedef = F_12 >= +%100; girdiler = 10 aile bileşiği (AILE_MOM, AILE_VAL, AILE_PRF, AILE_INV, AILE_EAR, AILE_RSK, AILE_LIQ, AILE_SEA, AILE_DIS, AILE_SEC; yüzdelik sıra ortalaması, eksik
değer 0.5); gözlem = KEŞİF oluşum aylarındaki bütün uygun hisse-aylar. Kestirim: Newton (IRLS), en çok 50 tur, sırt cezası 1e-06
(yalnız sayısal kararlılık). Katsayılar secili.json'da DONDURULUR; DOĞRULAMA ve KASA'da aynen uygulanır. Raporlanır: tahmin olasılığı
onluklarına göre kalibrasyon (tahmin ve gerçekleşen oran) ve aylık üst %10'un +%100 lift'i (R2 ile aynı bootstrap). KEŞİF değerleri örneklem
içidir. Etiket ya da karar rolü yoktur.

## 9. Yanlılık beyanı
1. YALNIZ YAŞAYANLAR (EVREN_SECENEKLERI.md §4): batan / devralınan şirket yok. En çok etkilenenler: kaybeden olasılıkları (P(<= -%50) eksik
   ölçülür: gerçek -%100'ler yok), küçüklük, düşük fiyat, sıkıntı ve likidite aileleri (açıklık 'çok yüksek'); momentumun alım bacağı ve
   kârlılık / düşük ihraç 'düşük'. P(+%100) taban oranı yukarı yanlıdır (hayatta kalanlar). Geriye gidildikçe evren '16 yıl hayatta kalmış'
   şirketlere yaslanır (2012'de ~1.200, 2026'da ~2.700 uygun hisse).
2. Frames şirketin EN SON bildirdiği değeri verir (yeniden sunum sızıntısı); tarih gerçek ilk başvuru günüdür. Dizin eşlemesi dönem alanı
   olmadan yapılır (§3); geç başvuranlarda yedek kural geleceğe bakabilir (kapsam §12'de yedek payı yazılıdır).
3. XBRL kapsamı 2009-2011'de kademeli açılır (küçük şirketler 2011 ortasından sonra); temel sinyallerin KEŞİF'in ilk yıllarındaki kapsamı
   eksiktir (§12 'ilk ölçüm ayı').
4. Yahoo: kırpık geçmişli hisseler kural gereği dışarıda; düzeltme katsayıları indirme günündeki haliyledir; tekil hatalı gün temizliği yok.
5. AYKIRILAR TUTULUR (GME tipi): kırpma yok; seçilen her çift için en büyük üç katkı (R1: getiri katkısı; R2: +%100 olayı sayısı) yazılır.
6. CIK - borsa kodu eşlemesi ve SIC kodu bugünkü haliyledir.
7. Dönemler oluşum ayına göredir; KEŞİF'in son 11 oluşum ayının 12 aylık pencereleri 2022'ye, DOĞRULAMA'nınkiler 2024'e taşar: komşu
   dönemler tam bağımsız değildir.
8. Kalibre maliyet yalnız 10 bp / yön; küçük hisselerde gerçek alış-satış farkı daha büyüktür (SPREAD_CS bilgi verir).

## 10. Çıktılar (arastirma_cikti/k60_kutuphane/)
kapsam.csv, kapsam_ozet.json; kesif_r1.csv, kesif_r2.csv, kesif_aylik.csv (R1 aylık getiriler), kesif_r2_aylik.csv (R2 aylık sayımlar: her
sayı buradan yeniden üretilebilir), placebo.csv, secili.json (git'e işlenir), kesif_meta.json; dogrulama_r1.csv, dogrulama_r2.csv,
dogrulama_aylik.csv, dogrulama_r2_aylik.csv, dogrulama_gecen.json (git'e işlenir), dogrulama_meta.json; kasa_r1.csv, kasa_r2.csv,
kasa_aylik.csv, kasa_r2_aylik.csv, kasa_acildi.json, kasa_meta.json; model_kalibrasyon.csv; olasilik_tablosu.md (ana, okunur sonuç: seçilmiş
her çift için dönem dönem taban oran, P(+%100), lift ve aralığı, aynısı -%50 için); K60_RAPOR.md.

## 11. BOŞLUK listesi (iş tanımında açık bırakılan ya da veriden ötürü doldurulan yerler; hepsi ölçümden önce yazıldı)
BOŞLUK 1. KEŞİF başlangıcı: yol haritası §5 '2016' diyordu; iş tanımı 2012-01 (XBRL kapsamı 2011Q2'den tam; 120 ay). 2012-01 uygulanır.
BOŞLUK 2. Bilgi tarihi eşlemesi (§3): dizinde dönem alanı yok; 'mali yıl sonu çeyreği -> 10-K ailesi, öteki -> 10-Q ailesi, çeyrek sonundan en az
  15 gün sonraki ilk başvuru' kuralı. Hiç eşleşmeyenlerde iş tanımındaki yedek (+90 / +120 gün). Eşleşen başvuru çok geç ise (halka arz öncesi
  dönemler, form türü farklı şirketler) bilgi tarihi geç kalır: tutucu yöndedir (veri bayatlar, geleceğe bakılmaz).
BOŞLUK 3. R1 'aynen K59': giriş ay sonu kapanışıdır (envanterdeki 'sonraki ayın ilk günü açılışı' kuralı yerine K59 cetveli); 1 ay getirisi
  K58 gibi sınırsız ileri taşımalı son fiyattan, R2 getirisi m+h ay sonunda taze fiyat şartıyla hesaplanır.
BOŞLUK 4. R1 istatistiği: iş tanımı KEŞİF'te 'alfa t', DOĞRULAMA'da 'fazla > 0, t > 1,65' diyor; ikisinde de t(alfa) kullanılır ve
  DOĞRULAMA / KASA'da ayrıca net fazla > 0 ve alfa > 0 istenir (daha sıkı okuma) + plasebo kalibrasyon şartı (§7; ek, sıkılaştırır).
BOŞLUK 5. R2 p değeri: 500 çekilişte yüzdelik p en az 1/501'dir; ~166 hipotezli BH'de birinci sıra eşiği bundan küçüktür. Bu yüzden BH'ye
  giren p, bootstrap standart hatasıyla normal yaklaşımdır (p_z); yüzdelik p ayrıca raporlanır.
BOŞLUK 6. R2 ailesinde iki uç birden test edilir (2 hipotez / sinyal); kaçınma için ayrı BH ailesi (R2K) ve ayrı plasebo eşiği vardır;
  yoksa yalnız kaybeden olasılığını artıran bir özellik DOĞRULAMA'ya giremezdi.
BOŞLUK 7. 'Plasebo en büyüğünün %95'i': 200 plasebodan hipotez sayısı kadar yerine koyarak çekilen kümelerin en büyüğünün dağılımı (§6). Pratikte
  eşik 200 plasebonun en büyüğüne yakındır.
BOŞLUK 8. '|t| > 3.0' yalnız R1 t(alfa) içindir (artı yönde net, eksi yönde brüt t); eksi yönle seçilen çift 'K60-R1 TERS (bilgi)' adayıdır,
  'K60-İZ ADAYI' olamaz. BH'ye giren p her iki yön için de net t(alfa)'nın iki yönlü p'sidir.
BOŞLUK 9. Bayrak (0 / 1) sinyallerde onluk kurulamaz: portföy = bayraklı uygun hisselerin tamamı (ay başına en az 10); beklenen yön '+' ise ÜST,
  '-' ise ALT uç sayılır; karşı uç kurulmaz. Ara verilen aylardan sonra devir, tutulan son ağırlıklara göre hesaplanır (maliyet hafif eksik).
BOŞLUK 10. Eşitlik bozma: aynı değerli hisseler arasında onluk sınırı sabit tohumlu rastgele sırayla bozulur (default_rng(60001); bütün sinyaller
  aynı sıra matrisini kullanır). Eşitliği olmayan sinyalde sonuç K59 (kod sırası) ile aynıdır.
BOŞLUK 11. Bileşik kuralları (§1): en az üye = ailenin sürekli üye sayısının yarısı (yukarı yuvarlanmış; iki üyeli ailede 1: bileşim zamanla değişebilir); COMP4 ve DOSYA_Y'de K59'daki S4 yerine EAR_ANN
  (K60'ta Nasdaq takvimi yok), S6 yerine NSI_1Y (K60 pay tanımı), X1 yerine REV_YOY.
BOŞLUK 12. Açıklama günü: 8-K madde kodu (2.02) inmedi; EAR_ANN, EAR_VOL, EA_MONTH için gün VEKİLİ kullanılır (§1 tanım); EAR_FILE aynı
  ölçünün başvuru günü sürümüdür. İkisi de EAR ailesinde ayrı hipotez sayılır.
BOŞLUK 13. Yaklaşık tanımlar (etiket eksikliği / yalnız yıllık nakit akışı yüzünden; §1'de yazılı): EV_EBITDA (kısa vadeli borç yok), NOA, OPLEV
  (SG&A yerine gelir - faaliyet kârı), NDF_BS (bilanço farkı), CBOP_A (OCF / varlık), RUNWAY (yıllık OCF; sürekli ölçü), ACCRUALS / CFP / NEF /
  BUYBACK_YLD / NET_PAYOUT_YLD / CAPEX_G / F_SCORE / O_SCORE yıllık, O_SCORE'da FFO yerine OCF ve fiyat düzeyi düzeltmesi yok (ay içi sıra
  değişmez), CHS_FAIL'de çeyrek kârları bugünkü (t) piyasa değerli toplam varlığa bölünür, RSIZE paydası uygun evrenin toplam PD'si, BETA_BAB
  günlük basit getiriyle ve 1'e büzme yapılmadan, TREND_MA 200 güne kadar gecikmelerle, MOM_FIP çift sıralama yerine sıra ortalaması,
  VOL_SHOCK ikili yerine sürekli oran, IVOL / ISKEW için French GÜNLÜK 3 faktör dosyası (11 Kasım'da indirildi; sha256 yukarıda).
BOŞLUK 14. Bu turda ölçülemeyen üç envanter satırı (TAXLOSS_JAN, E_LOCKUP, E_MA_TARGET) ve DALGA 2 listesi §1'de.
BOŞLUK 15. KASA'da 12 ay ufuklu R2 yalnız ~20 oluşum ayıdır; blok bootstrap dairesel olduğu için hesaplanır ama aralık güvenilirliği düşüktür
  (plasebo dilim şartı bunun için). Tek açılış işareti silinmez; çökme olursa yeniden açma kararı ana oturumundur ve raporda yazılır.
BOŞLUK 16. KASA'nın ön şartı olarak dogrulama_gecen.json'ın da git'e işlenmiş olması istenir (iş tanımında yalnız secili.json vardı; ek).
BOŞLUK 17. Kapalı konulara komşu sinyaller (EAR_VOL, VOL_SHOCK: 'hacim'; IND_MOM_6, IND_LEAD_BIG: 'sektör ısısı'; TREND_MA: 'şekil') çöl giriş
  zamanlaması değil, portföy düzeyi literatür faktörleri olarak kütüphanededir (iş tanımı: envanterin hesaplanabilen bütün satırları).
BOŞLUK 18. Lojistik modelde eksik bileşik 0.5 (nötr sıra) ile doldurulur; kalibrasyon onlukları dönem havuzunda eşit sayılıdır.
BOŞLUK 19. Ortalama ve medyan F, hisse-ay havuzundadır (ay ortalaması değil).
BOŞLUK 20. KEŞİF yeniden koşulursa secili.json bayt bayt aynı çıkmalıdır; değilse koşu durur ve dosyaya dokunulmaz.
BOŞLUK 21. Plasebo kıyas istatistiği R1'de BRÜT t(alfa)'dır (§6 gerekçe); sinyal artı yönde NET t'siyle sınanır. İş tanımındaki 'plasebo en büyük
  |t|'si iki yöne ayrıldı (artı: en büyük brüt t; eksi: en büyük -(brüt t)).
BOŞLUK 22. Bayrak alt sınırı (ay başına bayraklı hisse) kapsam sayımından SONRA, yalnız SAYILARA bakılarak 10 olarak sabitlendi (ilk taslakta 20 idi:
  NT_LATE, E_SPLIT, E_RSPLIT, E_DIV_INIT KEŞİF'te 36 aya ulaşamıyordu). Hiçbir getiri ya da olasılık görülmedi. E_TENDER_SELF yine de ölçülemez
  (ayda ~4 hisse): tabloda 'ölçülemedi' çıkar.
BOŞLUK 23. Veri temizliği yalnız şudur: Yahoo düzeltilmiş kapanışı <= 0 olan günler yok sayılır (sayımda görüldü: getiri tanımsız / sonsuz).
  Başka kırpma, uç değer atma ya da hatalı gün düzeltmesi YOK; uçlar raporda sayılır (ay getirisi > +%300, 12 ay getirisi > +%1000).
BOŞLUK 24. Her koşunun meta dosyasına K60.py'nin sha256'sı ve kütüphane sürümleri yazılır; KEŞİF'ten sonra kod değişirse DOĞRULAMA / KASA
  meta dosyasına ve rapora not düşer (koşu durmaz: hata düzeltmesi gerekebilir; değişikliği ana oturum denetler).
BOŞLUK 25. SIC kodu yalnız islenmis-veri k35 tablosundaki şirketlerde var (kapsam §12); SEC ailesi yalnız bu hisselerde ölçülür.

## 12. Kapsam (yalnız sayım; mühre girmez)
Faz 1 kapsam sayımı (2026-11-11 12:09:25 UTC; `python -I K60.py kapsam`; yalnız hisse / ay SAYILARI: getiri, olasılık, t hesaplanmadı).
Yüklenen hisse 4666 (dışarıda: kırpık 29, tür dışı 5, fiyatı yok 55); CIK'i olan 4665, SIC'i olan 2844; işlem günü 4190 (2010-01-04 .. 2026-08-31), ay sonu 200.
Bilgi tarihi kaynağı: çeyrek kayıtlarının %98.9'i, yıllık kayıtların %99.9'i EDGAR dizininden (gerçek başvuru günü), kalanı yedek kuraldan; yıllıktan türetilen 4. çeyrek 164252. Pay sayısı kaynağı (uygun hisse-ay, KEŞİF): kapak (dei) %85.3, bilanço %0.6, ağırlıklı ortalama %3.6, yok %10.5.
- KEŞİF: oluşum ayı R1 120 (2012-01-31 .. 2021-12-31), R2 12 ay 120 (son 2021-12-31), 6 ay 120, 3 ay 120; uygun evren ortalama 1642 (1190 - 2306); uygun hisse-aylarda bilinen çeyrek payı %92, bilinen mali yıl payı %94
- DOĞRULAMA: oluşum ayı R1 24 (2022-01-31 .. 2023-12-29), R2 12 ay 24 (son 2023-12-29), 6 ay 24, 3 ay 24; uygun evren ortalama 2274 (2219 - 2353); uygun hisse-aylarda bilinen çeyrek payı %93, bilinen mali yıl payı %96
- KASA: oluşum ayı R1 31 (2024-01-31 .. 2026-07-31), R2 12 ay 20 (son 2025-08-29), 6 ay 26, 3 ay 29; uygun evren ortalama 2516 (2319 - 2745); uygun hisse-aylarda bilinen çeyrek payı %93, bilinen mali yıl payı %96

'ay' = R1'de ölçülebilen oluşum ayı sayısı (sürekli sinyal: sinyali olan uygun hisse >= min_sinyal olan ilk aydan sona; bayrak: bayraklı hisse >= min_bayrak olan aylar); 'ort. hisse' = o aylarda sinyali olan (bayrakta: bayraklı) uygun hisse ortalaması.

| sinyal | aile | tür | KEŞİF ay / ort. hisse | DOĞRULAMA | KASA | KEŞİF ilk ölçüm ayı |
|---|---|---|---|---|---|---|
| MOM_12_1 | MOM | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| MOM_6_1 | MOM | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| MOM_INT_12_7 | MOM | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| MOM_RES_12_1 | MOM | surekli | 108 / 1556 | 24 / 1995 | 31 / 2401 | 2013-01-31 |
| HIGH52 | MOM | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| STREV_1M | MOM | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| LTREV_60_13 | MOM | surekli | 84 / 1506 | 24 / 1825 | 31 / 2126 | 2015-01-30 |
| MOM_FIP | MOM | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| TREND_MA | MOM | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| BM | VAL | surekli | 120 / 1304 | 24 / 1804 | 31 / 1981 | 2012-01-31 |
| EP | VAL | surekli | 120 / 1266 | 24 / 1810 | 31 / 2017 | 2012-01-31 |
| SP | VAL | surekli | 120 / 1134 | 24 / 1696 | 31 / 1878 | 2012-01-31 |
| AM | VAL | surekli | 120 / 1424 | 24 / 1981 | 31 / 2199 | 2012-01-31 |
| LEV_MKT | VAL | surekli | 120 / 1400 | 24 / 1962 | 31 / 2178 | 2012-01-31 |
| CFP | VAL | surekli | 120 / 1295 | 24 / 1982 | 31 / 2190 | 2012-01-31 |
| EV_EBITDA | VAL | surekli | 120 / 643 | 24 / 819 | 31 / 901 | 2012-01-31 |
| NET_PAYOUT_YLD | VAL | surekli | 120 / 1295 | 24 / 1982 | 31 / 2190 | 2012-01-31 |
| ROE_TTM | PRF | surekli | 120 / 1224 | 24 / 1745 | 31 / 1933 | 2012-01-31 |
| ROA_Q | PRF | surekli | 120 / 1356 | 24 / 1949 | 31 / 2183 | 2012-01-31 |
| D_ASSET_TURN | PRF | surekli | 120 / 1078 | 24 / 1721 | 31 / 1943 | 2012-01-31 |
| SALES_ACCEL | PRF | surekli | 120 / 1217 | 24 / 1820 | 31 / 2016 | 2012-01-31 |
| ACCRUALS | PRF | surekli | 120 / 1265 | 24 / 2033 | 31 / 2286 | 2012-01-31 |
| GP_A | PRF | surekli | 120 / 852 | 24 / 1204 | 31 / 1315 | 2012-01-31 |
| OP_BE | PRF | surekli | 120 / 1061 | 24 / 1491 | 31 / 1640 | 2012-01-31 |
| CBOP_A | PRF | surekli | 120 / 1372 | 24 / 2130 | 31 / 2365 | 2012-01-31 |
| F_SCORE | PRF | surekli | 120 / 1193 | 24 / 1961 | 31 / 2213 | 2012-01-31 |
| NOA | PRF | surekli | 120 / 1317 | 24 / 1780 | 31 / 1983 | 2012-01-31 |
| OPLEV | PRF | surekli | 120 / 993 | 24 / 1512 | 31 / 1681 | 2012-01-31 |
| RD_ME | PRF | surekli | 120 / 389 | 24 / 654 | 31 / 753 | 2012-01-31 |
| TAX_CHG | PRF | surekli | 120 / 1335 | 24 / 1878 | 31 / 2076 | 2012-01-31 |
| ASSET_G | INV | surekli | 120 / 1475 | 24 / 2079 | 31 / 2324 | 2012-01-31 |
| NSI_1Y | INV | surekli | 120 / 1401 | 24 / 1976 | 31 / 2223 | 2012-01-31 |
| BE_G | INV | surekli | 120 / 1316 | 24 / 1844 | 31 / 2055 | 2012-01-31 |
| NSI_5Y | INV | surekli | 84 / 1160 | 24 / 1570 | 31 / 1800 | 2015-01-30 |
| NEF | INV | surekli | 120 / 1356 | 24 / 2104 | 31 / 2354 | 2012-01-31 |
| NDF_BS | INV | surekli | 120 / 784 | 24 / 1140 | 31 / 1291 | 2012-01-31 |
| BUYBACK_YLD | INV | surekli | 120 / 1295 | 24 / 1982 | 31 / 2190 | 2012-01-31 |
| CAPEX_G | INV | surekli | 120 / 1079 | 24 / 1523 | 31 / 1685 | 2012-01-31 |
| EAR_ANN | EAR | surekli | 120 / 1354 | 24 / 1942 | 31 / 2177 | 2012-01-31 |
| EAR_FILE | EAR | surekli | 120 / 1432 | 24 / 2013 | 31 / 2239 | 2012-01-31 |
| SUE_SRW | EAR | surekli | 119 / 1151 | 24 / 1722 | 31 / 2015 | 2012-02-29 |
| REV_SURP | EAR | surekli | 119 / 880 | 24 / 1583 | 31 / 1849 | 2012-02-29 |
| EARN_STREAK | EAR | surekli | 120 / 1340 | 24 / 1935 | 31 / 2165 | 2012-01-31 |
| EAR_VOL | EAR | surekli | 120 / 1354 | 24 / 1942 | 31 / 2177 | 2012-01-31 |
| VOL_60D | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| IVOL_FF3 | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| BETA_BAB | RSK | surekli | 120 / 1577 | 24 / 2130 | 31 / 2464 | 2012-01-31 |
| MAX5 | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| SKEW_TOT | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| ISKEW | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| PRICE_LVL | RSK | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| SIZE_ME | LIQ | surekli | 120 / 1471 | 24 / 2068 | 31 / 2295 | 2012-01-31 |
| AMIHUD | LIQ | surekli | 120 / 1641 | 24 / 2273 | 31 / 2515 | 2012-01-31 |
| TURN_12M | LIQ | surekli | 120 / 1471 | 24 / 2068 | 31 / 2295 | 2012-01-31 |
| DOLVOL | LIQ | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| VOL_SHOCK | LIQ | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| SPREAD_CS | LIQ | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| GAP_OVN | LIQ | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| SEAS_1 | SEA | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| SEAS_2_5 | SEA | surekli | 84 / 1506 | 24 / 1825 | 31 / 2126 | 2015-01-30 |
| EA_MONTH | SEA | bayrak | 120 / 498 | 24 / 699 | 31 / 815 | 2012-01-31 |
| DIV_MONTH | SEA | bayrak | 120 / 393 | 24 / 471 | 31 / 520 | 2012-01-31 |
| RUNWAY | DIS | surekli | 120 / 1259 | 24 / 1842 | 31 / 2042 | 2012-01-31 |
| NT_LATE | DIS | bayrak | 47 / 16 | 16 / 19 | 20 / 23 | 2013-03-28 |
| CHS_FAIL | DIS | surekli | 120 / 1137 | 24 / 1558 | 31 / 1726 | 2012-01-31 |
| O_SCORE | DIS | surekli | 120 / 1004 | 24 / 1647 | 31 / 1882 | 2012-01-31 |
| IND_MOM_6 | SEC | surekli | 120 / 1114 | 24 / 1587 | 31 / 1774 | 2012-01-31 |
| IND_LEAD_BIG | SEC | surekli | 120 / 609 | 24 / 927 | 31 / 1046 | 2012-01-31 |
| ACT_13D | OWN | bayrak | 114 / 23 | 24 / 26 | 31 / 32 | 2012-01-31 |
| E_S3 | EVT | bayrak | 120 / 103 | 24 / 123 | 31 / 165 | 2012-01-31 |
| E_424B5 | EVT | bayrak | 120 / 97 | 24 / 89 | 31 / 141 | 2012-01-31 |
| E_TENDER_SELF | EVT | bayrak | 5 / 12 | 1 / 10 | — | 2013-02-28 |
| E_IPO_3Y | EVT | bayrak | 120 / 127 | 24 / 279 | 31 / 115 | 2012-01-31 |
| E_SPLIT | EVT | bayrak | 102 / 22 | 23 / 17 | 31 / 18 | 2012-01-31 |
| E_RSPLIT | EVT | bayrak | 64 / 18 | 24 / 17 | 31 / 43 | 2013-11-29 |
| E_DIV_INIT | EVT | bayrak | 106 / 27 | 24 / 30 | 31 / 34 | 2013-01-31 |
| E_DIV_OMIT | EVT | bayrak | 30 / 35 | — | 21 / 12 | 2016-08-31 |
| AILE_MOM | AİLE | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| AILE_VAL | AİLE | surekli | 120 / 1411 | 24 / 1973 | 31 / 2188 | 2012-01-31 |
| AILE_PRF | AİLE | surekli | 120 / 1285 | 24 / 1924 | 31 / 2135 | 2012-01-31 |
| AILE_INV | AİLE | surekli | 120 / 1450 | 24 / 2073 | 31 / 2329 | 2012-01-31 |
| AILE_EAR | AİLE | surekli | 120 / 1450 | 24 / 2073 | 31 / 2312 | 2012-01-31 |
| AILE_RSK | AİLE | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| AILE_LIQ | AİLE | surekli | 120 / 1642 | 24 / 2274 | 31 / 2516 | 2012-01-31 |
| AILE_SEA | AİLE | surekli | 120 / 1642 | 24 / 2273 | 31 / 2516 | 2012-01-31 |
| AILE_DIS | AİLE | surekli | 120 / 1143 | 24 / 1717 | 31 / 1928 | 2012-01-31 |
| AILE_SEC | AİLE | surekli | 120 / 1114 | 24 / 1587 | 31 / 1774 | 2012-01-31 |
| COMP4 | K59 | surekli | 120 / 1432 | 24 / 2019 | 31 / 2256 | 2012-01-31 |
| DOSYA_Y | K59 | surekli | 120 / 1162 | 24 / 1750 | 31 / 1945 | 2012-01-31 |

## 13. Değişmezlik ve komut sırası
Yukarıdaki bütün eşikler, tanımlar, dönemler ve karar kuralları sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi
gerekirse ön kayıt değişmez, düzeltme raporda ayrıca yazılır.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `cd /home/user/col_yolu && python -I K60.py kos --donem kesif`  -> kesif_*.csv, placebo.csv, secili.json
3. (ana oturum) secili.json'ı denetler ve git'e işler.
4. `python -I K60.py kos --donem dogrulama`  -> dogrulama_*.csv, dogrulama_gecen.json
5. (ana oturum) dogrulama_gecen.json'ı denetler ve git'e işler.
6. `python -I K60.py kos --donem kasa`  (TEK AÇILIŞ) -> kasa_*.csv
7. `python K60.py rapor`  -> olasilik_tablosu.md, K60_RAPOR.md
