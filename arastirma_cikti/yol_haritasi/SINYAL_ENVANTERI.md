# Sinyal envanteri: K60 ön kaydı için ölçüm öncesi kütüphane (11 Kasım 2026)

Yazan: alt ajan (araştırma + envanter). Ölçüm yapılmadı, fiyat indirilmedi, getiri hesaplanmadı. Dayanak: YOL_HARITASI_11Kas.md bölüm 3–5, EVREN_SECENEKLERI.md.

## 0. Okuma kılavuzu

- Kütüphane 120 satırdır: 116 sinyal test edilebilir, 4 sinyal ücretsiz veriyle hesaplanamaz (YOK) ve yalnız kayıt için durur.
- **Yön:** `+` = ölçü yüksekse beklenen getiri yüksek; `−` = ölçü yüksekse (ya da olay olduysa) beklenen getiri düşük (kaçınma); `?` = literatür yön vermiyor, iki yönlü test.
- **Büyüklük:** "OP" = özgün makaledeki uzun-kısa portföyün aylık % getirisi ve t değeri. Bu sayılar Chen-Zimmermann'ın açık kaynak belgesinden (SignalDoc.csv, [K1]) alındı, tek tek makaleden okunmadı. EW = eşit ağırlık, VW = değer ağırlığı. OP sayıları brüttür, çoğu 2000 öncesi örneklemdir ve çoğu al-sat (uzun − kısa) farkıdır; Cemal'in yalnız alım yapan hesabı bunun en fazla alım bacağını alır.
- **Yayın sonrası erime:** tek tek sinyal için çoğunlukla bilinmiyor. Genel kural: 97 sinyalde getiri örneklem dışında %26, yayın sonrasında %58 düşük (McLean-Pontiff 2016, özet sayfasından doğrulandı [K2]). Satırda ayrıca bilgi yoksa bu ortalama varsayılır.
- **Bizde var mı:**
  - `EVET` = islenmis-veri dalındaki ya da oturum önbelleğindeki veriyle bugün hesaplanır.
  - `EVET†` = bugün hesaplanır ama geçmişi kısa: SEC frames önbelleği 2020Q1–2026Q2 (7 etiket: Revenues, RevenueFromContractWithCustomerExcludingAssessedTax, SalesRevenueNet, NetIncomeLoss, StockholdersEquity, Liabilities, LiabilitiesAndStockholdersEquity = toplam varlık); pay sayısı, nakit ve faaliyet nakit akışı secfs özütünde 2021q1–2026q3. KEŞİF dönemi (2016–2021) için eski çeyrekler indirilmelidir (bölüm C, satır 1–2).
  - `EVET (sec_ozet)` = 3.262 CIK'lik K55 evreninin SEC başvuru geçmişi (form, başvuru günü, 8-K madde kodu); daha geniş evren için bölüm C satır 3.
  - `İNDİR` = ücretsiz indirilebilir; kaynak bölüm C'de.
  - `YOK` = ücretsiz kaynak yok ya da pratikte kurulamaz.
- **Batan yanlılığı:** yaşayanlar evreninde sonucun ne kadar şişebileceği (EVREN_SECENEKLERI bölüm 4 ile aynı mantık). Kaçınma (−) sinyallerinde yanlılık sinyalin ALEYHİNE çalışır: batanlar evrende yoksa kaçınmanın faydası küçük görünür.
- **Zaman kuralı (bütün satırlar):** temel veri başvuru günü (`filed`) + 1 işlem günü sonra bilinir sayılır; sinyal ay sonunda hesaplanır; giriş sonraki ayın ilk işlem günü açılışı.
- "doğrulanamadı" = bu oturumda birincil kaynaktan ya da güvenilir özetten teyit edilemedi; sayı uydurulmadı.

## A. Sinyal tablosu

### A1. Momentum ve dönüş (MOM)

| kod | aile | tanım (formül, pencere, gecikme) | yön | ana kaynak | literatürdeki büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| MOM_12_1 | MOM | kapanış(t−1 ay) / kapanış(t−12 ay) − 1; son ay atlanır | + | Jegadeesh-Titman 1993 JF | OP 1,31 / t 3,7 EW | günlük fiyat | EVET (K59 S1) | orta | K58: yaşayan evrende net +%8,5/yıl, t 2,10. Alım bacağında yanlılık düşük |
| MOM_6_1 | MOM | kapanış(t−1) / kapanış(t−6) − 1 | + | Jegadeesh-Titman 1993 JF | OP 0,84 / t 2,4 EW | günlük fiyat | EVET | orta | MOM_12_1 ile yüksek korelasyon; aile içi |
| MOM_INT_12_7 | MOM | t−12 .. t−7 ay getirisi | + | Novy-Marx 2012 JFE | OP 1,20 / t 5,8 VW | günlük fiyat | EVET | orta | "ara" momentum |
| MOM_RES_12_1 | MOM | 36 aylık FF3 regresyon artıklarının t−12..t−2 toplamı / artık std | + | Blitz-Huij-Martens 2011 J. Empirical Finance | OP 0,93 / t 8,2 EW | fiyat + French faktörleri | EVET | orta | çöküş riski ham momentumdan düşük (makalenin iddiası; doğrulanamadı) |
| HIGH52 | MOM | kapanış / son 252 gün en yüksek | + | George-Hwang 2004 JF | OP 0,45 / t 2,0 EW | günlük fiyat | EVET (K59 S9) | orta | |
| STREV_1M | MOM | geçen ayın getirisi | − | Jegadeesh 1990 JF | OP 1,99 / t 12,4 EW | günlük fiyat | EVET (K59 S2) | yüksek | devir çok yüksek; aylık devri %50 üstü stratejilerin azı maliyet sonrası kalır [K7] |
| LTREV_60_13 | MOM | t−60 .. t−13 ay getirisi | − | De Bondt-Thaler 1985 JF | OP t 3,3 EW | 5 yıl fiyat | EVET | yüksek | kaybeden bacağı batanlarla dolu; V_ABD 2015-06'dan: ilk sinyal 2020-06 |
| MOM_FIP | MOM | ID = işaret(R12-1) × (eksi gün payı − artı gün payı), 12-1 penceresi; düşük ID içinde MOM_12_1 | + | Da-Gurun-Warachka 2014 RFS | doğrulanamadı | günlük fiyat | EVET | orta | "yavaş pişen kurbağa": sürekli küçük haber |
| TREND_MA | MOM | 3–1000 günlük ortalama / fiyat oranlarının kesit regresyonuyla tahmin | + | Han-Zhou-Zhu 2016 JFE | OP 1,63 / t 15,0 EW | günlük fiyat | EVET | orta | karmaşık; basit ölçüyü geçmezse seçilmez |

### A2. Değer (VAL)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| BM | VAL | StockholdersEquity (en son bilinen) / piyasa değeri | + | Fama-French 1992 JF | OP 0,50 / t 5,7 EW | özkaynak, pay sayısı, fiyat | EVET† | orta | ucuz = sıkıntılı olabilir |
| EP | VAL | NetIncomeLoss son 4 çeyrek / piyasa değeri | + | Basu 1977 JF | OP 0,58 EW | net kâr, pay, fiyat | EVET† | orta | zarar edenler ayrı küme |
| SP | VAL | Revenues son 4 çeyrek / piyasa değeri | + | Barbee-Mukherji-Raines 1996 FAJ | OP t 2,5 EW | satış, pay, fiyat | EVET† | orta | |
| AM | VAL | toplam varlık / piyasa değeri | + | Fama-French 1992 JF | OP t 5,7 EW | varlık, pay, fiyat | EVET† | orta | |
| LEV_MKT | VAL | Liabilities / piyasa değeri | + | Bhandari 1988 JF | OP t 3,9 EW | borç, pay, fiyat | EVET† | yüksek | kaldıraç teması yinelemede zayıf (ikincil özet [K4b]) |
| CFP | VAL | faaliyet nakit akışı son 4 çeyrek / piyasa değeri | + | Desai-Rajgopal-Venkatachalam 2004 AR | OP 1,27 / t 2,8 EW | OCF, pay, fiyat | EVET† | orta | secfs 2021+ |
| EV_EBITDA | VAL | (piyasa değeri + borç − nakit) / (faaliyet kârı + amortisman) | − | Loughran-Wellman 2011 JFQA | OP 0,95 / t 6,5 EW | OperatingIncomeLoss, DepreciationDepletionAndAmortization, LongTermDebt, DebtCurrent, nakit | İNDİR | orta | |
| NET_PAYOUT_YLD | VAL | (temettü + geri alım − ihraç) son 4 çeyrek / piyasa değeri | + | Boudoukh et al. 2007 JF | OP 0,73 EW | PaymentsOfDividends, PaymentsForRepurchaseOfCommonStock, ProceedsFromIssuanceOfCommonStock | İNDİR | düşük | nakit akış kalemleri yıllık (bölüm C notu) |

### A3. Kârlılık ve kalite (PRF)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| ROE_TTM | PRF | NetIncomeLoss son 4 çeyrek / StockholdersEquity (> 0) | + | Haugen-Baker 1996 JFE | OP t 4,5 EW | net kâr, özkaynak | EVET† (K59 S5) | düşük | |
| ROA_Q | PRF | son çeyrek net kâr / bir önceki çeyrek toplam varlık | + | Balakrishnan-Bartov-Faurel 2010 JAE | OP 0,84 / t 6,5 EW | net kâr, varlık | EVET† | düşük | |
| D_ASSET_TURN | PRF | (satış / varlık) yıllık değişimi | + | Soliman 2008 AR | OP t 5,1 EW | satış, varlık | EVET† | düşük | |
| SALES_ACCEL | PRF | son çeyrek satış / önceki iki çeyrek ortalaması | + | proje ölçüsü (K59 S7); literatür karşılığı yok | doğrulanamadı | satış | EVET† | düşük | "şüpheli" etiketi: yayımlanmış kanıt yok |
| ACCRUALS | PRF | (net kâr − faaliyet nakit akışı) / ortalama varlık | − | Sloan 1996 AR | OP 0,87 / t 4,7 EW | net kâr, OCF, varlık | EVET† | düşük | 2000'lerde zayıfladığı bildirildi (doğrulanamadı) |
| GP_A | PRF | (satış − satışların maliyeti) / toplam varlık | + | Novy-Marx 2013 JFE | OP 0,31 / t 2,5 VW | GrossProfit ya da CostOfRevenue | İNDİR | düşük | VW'de de tutan az sayıdaki ölçüden |
| OP_BE | PRF | faaliyet kârı / özkaynak | + | Fama-French 2006 JFE | OP t 2,6 EW | OperatingIncomeLoss | İNDİR | düşük | |
| CBOP_A | PRF | (faaliyet kârı − işletme sermayesi tahakkukları) / varlık; yaklaşık: OCF / varlık | + | Ball-Gerakos-Linnainmaa-Nikolaev 2016 JFE | OP 0,47 / t 3,2 VW | OperatingIncomeLoss, OCF, alacak / stok / borç kalemleri | İNDİR | düşük | yaklaşık sürüm bugün (OCF / varlık, 2021+) |
| F_SCORE | PRF | Piotroski 9 ikili ölçü (kârlılık 4, kaldıraç / likidite 3, verim 2) | + | Piotroski 2000 JAR | OP 1,96 / t 5,6 VW (yüksek BM içinde) | OCF, AssetsCurrent, LiabilitiesCurrent, LongTermDebt, GrossProfit, pay | İNDİR | düşük | |
| NOA | PRF | (faaliyet varlıkları − faaliyet borçları) / önceki yıl varlık | − | Hirshleifer et al. 2004 JAE | OP 1,48 / t 8,5 EW | nakit, borç kalemleri | İNDİR | düşük | |
| OPLEV | PRF | (satışların maliyeti + SG&A) / varlık | + | Novy-Marx 2011 ROF | OP 0,51 / t 3,4 EW | CostOfRevenue, SellingGeneralAndAdministrativeExpense | İNDİR | orta | |
| RD_ME | PRF | Ar-Ge gideri son 4 çeyrek / piyasa değeri | + | Chan-Lakonishok-Sougiannis 2001 JF | OP 0,89 EW | ResearchAndDevelopmentExpense | İNDİR | yüksek | Ar-Ge yoğun küçükler çok batar |
| TAX_CHG | PRF | vergi giderinin yıllık değişimi / varlık | + | Thomas-Zhang 2011 JAR | OP 1,30 / t 11,3 EW | IncomeTaxExpenseBenefit | İNDİR | düşük | |

### A4. Yatırım ve ihraç (INV)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| ASSET_G | INV | toplam varlık(t) / toplam varlık(t − 1 yıl) − 1 | − | Cooper-Gulen-Schill 2008 JF | OP 1,73 / t 8,5 EW | varlık | EVET† | düşük | |
| NSI_1Y | INV | ln(bölünme düzeltmeli pay(t) / pay(t − 12 ay)) | − | Pontiff-Woodgate 2008 JF | OP t 7,1 EW | pay sayısı, bölünme | EVET† (K59 S6) | düşük | çok ihraç edenlerin %37'sinin bugün kodu yok (K34): kaçınma faydası eksik ölçülür |
| BE_G | INV | özkaynak yıllık büyümesi | − | Lockwood-Prombutr 2010 JFR | OP 0,80 / t 5,4 EW | özkaynak | EVET† | düşük | |
| NSI_5Y | INV | 5 yıllık pay değişimi (ln) | − | Daniel-Titman 2006 JF | OP t 4,4 EW | 2016+ pay sayısı | İNDİR | düşük | |
| NEF | INV | (hisse ihracı geliri − geri alım − temettü) / ortalama varlık | − | Bradshaw-Richardson-Sloan 2006 JAE | OP 0,93 / t 3,8 EW | ProceedsFromIssuanceOfCommonStock, PaymentsForRepurchaseOfCommonStock, PaymentsOfDividends | İNDİR | düşük | |
| NDF | INV | (borç ihracı − borç geri ödeme) / ortalama varlık | − | Bradshaw-Richardson-Sloan 2006 JAE | OP 0,68 / t 6,9 EW | ProceedsFromIssuanceOfLongTermDebt, RepaymentsOfLongTermDebt | İNDİR | düşük | etiket çeşitliliği yüksek |
| BUYBACK_YLD | INV | geri alım ödemesi son 4 çeyrek / piyasa değeri | + | Ikenberry-Lakonishok-Vermaelen 1995 JFE | OP 0,17 / t 1,9 EW; kalıcılık: Peyer-Vermaelen 2009 RFS (sayı doğrulanamadı) | PaymentsForRepurchaseOfCommonStock | İNDİR | düşük | |
| CAPEX_G | INV | yatırım harcamasının 2 yıllık büyümesi | − | Anderson-Garcia-Feijoo 2006 JF | OP 0,57 / t 5,1 EW | PaymentsToAcquirePropertyPlantAndEquipment | İNDİR | düşük | |
| INV_A | INV | (maddi duran varlık + stok) değişimi / önceki yıl varlık | − | Lyandres-Sun-Zhang 2008 RFS | OP 0,57 / t 7,1 EW | PropertyPlantAndEquipmentNet, InventoryNet | İNDİR | düşük | |
| INVTRY_G | INV | stok yıllık büyümesi / varlık | − | Thomas-Zhang 2002 RAS | OP 0,95 EW | InventoryNet | İNDİR | düşük | |
| HIRE_G | INV | çalışan sayısı yıllık büyümesi | − | Bazdresch-Belo-Lin 2014 JPE | OP 0,87 / t 5,8 EW | çalışan sayısı | YOK | — | XBRL'de düzenli etiket yok; 10-K metninden ayıklamak gerekir |

### A5. Kazanç sürprizi ve revizyonlar (EAR)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| EAR_ANN | EAR | bilanço günü çevresi (−1..+1) piyasaya göre getiri; son 63 işlem gününde açıklayanlar | + | Chan-Jegadeesh-Lakonishok 1996 JF | OP t 9,3 EW | bilanço günü, fiyat | EVET (K59 S4) | düşük | gün kaynağı: Nasdaq takvimi 2022-12+, öncesi 8-K 2.02 başvuru günü |
| SUE_SRW | EAR | (çeyrek kârı − 4 çeyrek önceki) / son 8 farkın std'si | + | Foster-Olsen-Shevlin 1984 AR; Bernard-Thomas 1989 JAR | OP 2,98 (birim / pencere doğrulanamadı) | net kâr | EVET† | düşük | 8 çeyrek geçmiş ister: 2022+ |
| REV_SURP | EAR | satış için aynı ölçü | + | Jegadeesh-Livnat 2006 JAE | doğrulanamadı | satış | EVET† | düşük | |
| EARN_STREAK | EAR | art arda aynı yönlü sürpriz sayısı (SUE_SRW işareti) | + | Loh-Warachka 2012 MS | OP 0,96 / t 9,5 EW (analist sürpriziyle) | net kâr | EVET† | düşük | özgün ölçü analist tahmini ister |
| SUE_ANALYST | EAR | (gerçekleşen − beklenti) / beklenti büyüklüğü | + | Bernard-Thomas 1989 JAR | doğrulanamadı | Nasdaq takvimi (sürpriz %) | EVET (2022-12+) | düşük | KEŞİF döneminde yok: yalnız KASA'da bilgi |
| EAR_VOL | EAR | bilanço günü hacmi / önceki 50 gün ortalaması | + | Garfinkel-Sokobin 2006 JAR | doğrulanamadı | hacim, bilanço günü | EVET | düşük | kapalı konu "hacim onayı"na dokunur (ana model kararı) |
| REC_UP | EAR | son 20 işlem gününde not yükseltme sayısı | + | Womack 1996 JF | alım: +%2,4, kısa ömürlü [K17] | Yahoo analist günlüğü | İNDİR | orta | K52: 310 bin kayıt, 2.515 hisse; tarihsel sürüm yok; revizyonlar fiyatı izliyor |
| REC_DOWN | EAR | son 20 işlem gününde not düşürme sayısı | − | Womack 1996 JF | satım: −%9,1, altı ay [K17] | Yahoo analist günlüğü | İNDİR | orta | kaçınma sinyali |
| PT_REV | EAR | hedef fiyat revizyonu (yeni / eski − 1), son 20 gün ortalaması | + | Brav-Lehavy 2003 JF | doğrulanamadı | Yahoo analist günlüğü | İNDİR | orta | hedef alanı eski kayıtlarda boş olabilir |
| N_ANALYST_CHG | EAR | 12 ayda not veren kurum sayısının değişimi | + | Scherbina 2008 ROF | OP 0,46 / t 3,3 VW (kapsam azalması −) | Yahoo analist günlüğü | İNDİR | orta | |
| EPS_REV | EAR | konsensüs EPS tahmin revizyonu | + | Chan-Jegadeesh-Lakonishok 1996 JF | OP t 4,1 EW | IBES | YOK | — | ücretli |
| GUIDANCE_UP | EAR | yönetim beklenti yükseltmesi | + | doğrulanamadı | doğrulanamadı | 8-K ek metni (EX-99) | YOK | — | sayı ayıklama metin işleme ister; pratikte kurulamaz |

### A6. Sahiplik ve içeridekiler (OWN)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| INS_BUY_90 | OWN | son 90 günde yönetici / yönetim kurulu açık piyasa alımı (Form 4 kod P): alıcı sayısı ve net değer / piyasa değeri | + | Lakonishok-Lee 2001 RFS; Jeng-Metrick-Zeckhauser 2003 REStat | alımlar yılda > %6 fazla getiri; satışlar anlamsız [K10] | Form 4 | EVET (k30_alim) | orta | etki küçük şirketlerde [K11] |
| INS_CLUSTER | OWN | 30 günde ≥ 3 farklı alıcı | + | doğrulanamadı | doğrulanamadı | Form 4 | EVET (k30_alim) | orta | eşik K31'den (önceden yazılı); özet dosyada alıcı kimliği yoksa ham veri indirilir |
| INS_OPP_BUY | OWN | "rutin olmayan" alım: kişi son 3 yılda aynı ayda işlem yapmamış | + | Cohen-Malloy-Pomorski 2012 JF | fırsatçı işlemler VW 82 bp/ay anormal; rutin ≈ 0 [K9] | Form 4, 2013+ | İNDİR | orta | |
| INS_SELL_90 | OWN | son 90 günde açık piyasa satışı (kod S, 10b5-1 hariç) ≥ 100 bin $ | − | Jeng-Metrick-Zeckhauser 2003 | anlamsız [K10] | Form 4 | İNDİR | düşük | 10b5-1 işareti 2023q2+; öncesi dipnot |
| INS_OPP_SELL | OWN | rutin olmayan satış | − | Cohen-Malloy-Pomorski 2012 JF | [K9] | Form 4 | İNDİR | düşük | |
| ACT_13D | OWN | son 60 günde ilk SC 13D başvurusu | + | Brav-Jiang-Partnoy-Thomas 2008 JF | (−20,+20) penceresinde ~%7; bir yıl geri dönüş yok [K12] | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | getirinin çoğu başvuru öncesi / günü: sonrası için sayı doğrulanamadı |
| IO_BREADTH_CHG | OWN | hisseyi tutan 13F kurumu sayısının çeyreklik değişimi / toplam kurum | + | Chen-Hong-Stein 2002 JFE | OP 0,67 / t 4,0 EW | 13F + CUSIP → sembol | İNDİR (zor) | orta | K31'de CUSIP eşlemesinde tıkandı |
| IO_CHG | OWN | kurumsal sahiplik payının çeyreklik değişimi | + | Nofsinger-Sias 1999 JF | doğrulanamadı | 13F + CUSIP → sembol | İNDİR (zor) | orta | 45 gün gecikmeli |
| SI_RATIO | OWN | açığa satış pozisyonu / pay sayısı | − | Dechow et al. 2001 JFE | OP 0,35 EW | FINRA açığa satış | İNDİR | düşük | 2017-12 öncesi yok |
| DTC | OWN | açığa satış pozisyonu / ortalama günlük hacim | − | Hong-Li-Ni-Scheinkman-Yan 2015 NBER | %1,2/ay EW, brüt, 1988–2012 [K13] | FINRA + hacim | İNDİR | düşük | kaçınma: üst %10 |
| SI_LOW | OWN | likit hisselerde en düşük açığa satış onluğu | + | Boehmer-Huszar-Jordan 2010 JFE | çalışma metni: ~%1,3–1,4/ay 4 faktör (yayın sayısı doğrulanamadı) [K14] | FINRA + hacim | İNDİR | düşük | yalnız alım yapan hesaba uygun |
| SHORT_VOL | OWN | borsa dışı açığa satış hacmi / toplam hacim, 5 gün ortalaması | − | Boehmer-Jones-Zhang 2008 JF | doğrulanamadı | FINRA Reg SHO günlük | İNDİR | düşük | piyasa yapıcı satışı ayrılmaz |

### A7. Risk ve piyango (RSK)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| VOL_60D | RSK | günlük getiri std, 60 gün (en az 40) | − | Ang-Hodrick-Xing-Zhang 2006 JF | OP 0,97 / t 2,9 VW | günlük fiyat | EVET (K59 S8) | yüksek | yüksek oynaklık ucu batanlarla dolu: yaşayan evrende etki küçük görünür |
| IVOL_FF3 | RSK | bir aylık günlük FF3 regresyon artığı std | − | Ang-Hodrick-Xing-Zhang 2006 JF | OP 1,06 / t 3,1 VW | fiyat + French günlük | EVET | yüksek | |
| BETA_BAB | RSK | beta = korelasyon(5 yıl) × oynaklık oranı (1 yıl); düşük beta | − | Frazzini-Pedersen 2014 JFE | OP 0,70 / t 7,1 (kaldıraçlı BAB) | fiyat + piyasa | EVET | orta | kaldıraçsız alım bacağı zayıf olabilir; 5 yıl geçmiş ister (ilk sinyal 2020-06) ya da pencere ön kayıtta 3 yıla sabitlenir |
| MAX5 | RSK | son ayın en yüksek 5 günlük getirisinin ortalaması | − | Bali-Cakici-Whitelaw 2011 JFE | OP 1,03 / t 2,8 VW | günlük fiyat | EVET | yüksek | "piyango" hisselerinden kaçınma |
| SKEW_TOT | RSK | günlük getiri çarpıklığı, 1 ay | − | Bali-Engle-Murray 2015 (kitap) | OP 0,47 / t 4,0 EW | günlük fiyat | EVET | orta | |
| ISKEW | RSK | FF3 artığının çarpıklığı | − | Bali-Engle-Murray 2015; Boyer-Mitton-Vorkink 2010 RFS | OP 0,45 / t 4,4 EW | fiyat + French | EVET | orta | |
| PRICE_LVL | RSK | ln(fiyat); düşük fiyat | − | Blume-Husic 1973 JF | OP t 2,9 EW | ham fiyat | EVET | yüksek | mikro hisse etkisi; maliyet yüksek |

### A8. Likidite ve mikro yapı (LIQ)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| SIZE_ME | LIQ | ln(piyasa değeri) | − | Banz 1981 JFE | OP 1,01 / t 3,1 EW | pay, fiyat | EVET† (K59 S3) | çok yüksek | K34: batanlarla etki üçte bire iniyor; boyut teması yinelemede zayıf [K4b] |
| AMIHUD | LIQ | ortalama (mutlak günlük getiri / işlem değeri), 12 ay | + | Amihud 2002 JFM | OP t 6,6 EW | fiyat, hacim | EVET | yüksek | sürtünme ailesi VW'de %96 başarısız [K3] |
| TURN_12M | LIQ | ortalama günlük hacim / pay sayısı, 12 ay | − | Datar-Naik-Radcliffe 1998 JFM | OP t 8,9 EW | hacim, pay | EVET† | orta | |
| DOLVOL | LIQ | ln(işlem değeri), t−2 ay | − | Brennan-Chordia-Subrahmanyam 1998 JFE | OP t 2,9 EW | fiyat, hacim | EVET | orta | |
| VOL_SHOCK | LIQ | son gün / hafta hacmi kendi 50 günlük dağılımının üst %10'unda | + | Gervais-Kaniel-Mingelgrin 2001 JF | sayı doğrulanamadı; yön + (izleyen ay) [K18] | hacim | EVET | orta | kapalı konu "hacim"e dokunur (ana model kararı) |
| SPREAD_CS | LIQ | günlük en yüksek / en düşükten alış-satış farkı tahmini | + | Corwin-Schultz 2012 JF | doğrulanamadı | günlük OHLC | EVET | orta | asıl kullanımı: maliyet tabanı |
| GAP_OVN | LIQ | son ayın gece (kapanış → açılış) getirisi toplamı | ? | Lou-Polk-Skouras 2019 JFE | gece ve gün içi bileşenler kendi içinde sürer, çapraz tersine döner; sayı doğrulanamadı [K19] | günlük açılış, kapanış | EVET | orta | açılış verisi kalitesi sınanmalı |

### A9. Mevsimsellik ve takvim (SEA)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| SEAS_1 | SEA | aynı takvim ayının geçen yılki getirisi | + | Heston-Sadka 2008 JFE | OP 1,15 / t 7,6 EW | 1 yıl fiyat | EVET | orta | mevsimsellik teması yinelemede zayıf [K4b] |
| SEAS_2_5 | SEA | aynı takvim ayının 2–5 yıl önceki ortalama getirisi | + | Heston-Sadka 2008 JFE | OP 0,67 / t 5,4 EW | 5 yıl fiyat | EVET | orta | V_ABD 2015-06'dan: ilk tam sinyal 2020 |
| EA_MONTH | SEA | bu ay bilanço açıklaması bekleniyor (geçen yıl aynı ay açıklamış) | + | Frazzini-Lamont 2007 NBER; Savor-Wilson 2016 JF | yıllık %9,9 anormal [K20] | bilanço günleri | EVET | düşük | bilanço günü riski taşır |
| TAXLOSS_JAN | SEA | 12 ayın en çok düşen onluğu, yalnız ocak ayı | + | Keim 1983 JFE | doğrulanamadı | fiyat | EVET | çok yüksek | küçük + kaybeden = batan yoğun |
| DIV_MONTH | SEA | bu ay temettü bekleniyor (3 / 6 / 12 ay önce ödemiş) | + | Hartzmark-Solomon 2013 JFE | OP 0,36 / t 16,2 EW | Yahoo temettü | İNDİR | düşük | |

### A10. Sıkıntı (DIS)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| RUNWAY | DIS | nakit / (−çeyreklik faaliyet nakit akışı) < 4 çeyrek | − | proje ölçüsü (K31 M3); literatür karşılığı doğrulanamadı | doğrulanamadı | nakit, OCF | EVET† (k31_fin) | çok yüksek | kaçınma; fayda yaşayan evrende eksik görünür |
| NT_LATE | DIS | son 60 günde NT 10-K / NT 10-Q başvurusu | − | Bartov-Konchitchki 2017 Accounting Horizons | başvuruda anlamlı düşüş; uzun pencere sayısı doğrulanamadı [K21] | SEC başvuru geçmişi | EVET (sec_ozet) | yüksek | |
| CHS_FAIL | DIS | Campbell-Hilscher-Szilagyi batma olasılığı (kâr, borç, nakit / piyasa değeri; getiri; oynaklık; boyut; fiyat) | − | Campbell-Hilscher-Szilagyi 2008 JF | OP 0,53 / t 1,4 (açık kanıt değil [K1]) | temel + fiyat | EVET† | çok yüksek | katsayılar makaleden sabit alınır |
| O_SCORE | DIS | Ohlson (1980) batma puanı | − | Dichev 1998 JF | OP 1,17 / t 3,4 EW | AssetsCurrent, LiabilitiesCurrent + eldekiler | İNDİR | çok yüksek | |
| Z_SCORE | DIS | Altman (1968) Z; düşük Z | − | Dichev 1998 JF | OP t 1,6 (açık kanıt değil [K1]) | işletme sermayesi, RetainedEarningsAccumulatedDeficit, faaliyet kârı | İNDİR | çok yüksek | |
| GC_FLAG | DIS | son 10-K / 10-Q'da "substantial doubt ... going concern" | − | Kausar-Taffler-Tan 2009 JAR | izleyen yıl −%14 (1993–2005); eşleştirince kayboluyor diyen çalışma var [K22] | EDGAR tam metin arama | İNDİR | çok yüksek | |

### A11. Kurumsal olaylar (EVT) — ayrıntı bölüm B'de

| kod | aile | tanım (aylık sinyal) | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| E_101 | EVT | son 20 işlem gününde 8-K madde 1.01 (önemli sözleşme) | ? | Lerman-Livnat 2010 RAS (8-K geneli) | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | 1.01 kredi sözleşmesini de kapsar: 2.03 / 3.02 ile birlikte gelenler ayrılır |
| E_201 | EVT | son 60 günde 8-K 2.01 (devralma tamamlandı; alıcı taraf) | − | doğrulanamadı | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | |
| E_205_206 | EVT | son 60 günde 8-K 2.05 / 2.06 (yeniden yapılanma / değer düşüklüğü) | ? | doğrulanamadı | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | orta | |
| E_301 | EVT | son 120 günde 8-K 3.01 (kottan çıkarma uyarısı) | − | Macey-O'Hara-Pompilio 2008 JLE | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | çok yüksek | |
| E_302 | EVT | son 60 günde 8-K 3.02 (kayıtsız hisse satışı) | − | Hertzel-Lemmon-Linck-Rees 2002 JF | duyuruda +, sonrasında − (sayı doğrulanamadı) [K23] | SEC başvuru geçmişi | EVET (sec_ozet) | yüksek | |
| E_401 | EVT | son 120 günde 8-K 4.01 (denetçi değişimi) | − | doğrulanamadı | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | orta | |
| E_402 | EVT | son 120 günde 8-K 4.02 (eski tablolara güvenilmez) | − | Palmrose-Richardson-Scholz 2004 JAE | duyuruda iki günde ~−%9 (ikincil kaynak); sonrası doğrulanamadı [K24] | SEC başvuru geçmişi | EVET (sec_ozet) | yüksek | nadir olay |
| E_502 | EVT | son 60 günde 8-K 5.02 (yönetici ayrılışı / ataması) | ? | doğrulanamadı | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | CEO / CFO ayrımı metin ister; yalnız madde kodu kaba |
| E_S3 | EVT | son 90 günde S-3 / S-3ASR (raf kaydı) | − | Loughran-Ritter 1995 JF | ihraç sonrası 5 yıl: yılda %7 (ikincil halka arz), %5 (ilk halka arz) [K25] | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | büyüklerde S-3ASR rutin: boyut süzgeci |
| E_424B5 | EVT | son 60 günde 424B5 (raftan satış; ATM dahil) | − | Loughran-Ritter 1995 JF; Billett-Floros-Garfinkel 2019 JFQA | [K25]; ATM için sayı doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | orta | 424B2 (banka notu) hariç |
| E_IPO_3Y | EVT | ilk halka arzdan sonraki ilk 3 yıl | − | Ritter 1991 JF | OP 0,85 / t 4,0 EW | 424B4 / ilk işlem günü | EVET (sec_ozet + fiyat) | yüksek | |
| E_LOCKUP | EVT | halka arz + 180 gün çevresi (−10..+10 gün) | − | Field-Hanka 2001 JF | 3 günde −%1,5; hacim kalıcı +%40 [K26] | 424B4 günü | EVET (sec_ozet) | düşük | kısa pencere: aylık cetvelde zayıf |
| E_MA_TARGET | EVT | hedef şirket: DEFM14A / SC 14D9 / SC TO-T sonrası, kapanışa kadar | + (küçük) | Mitchell-Pulvino 2001 JF | doğrulanamadı | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | sınırlı yukarı, anlaşma bozulursa sert düşüş; Cemal'in hedefine uymaz |
| E_TENDER_SELF | EVT | son 90 günde SC TO-I (şirketin kendi hisselerine çağrısı) | + | Lakonishok-Vermaelen 1990 JF; Peyer-Vermaelen 2009 RFS | kalıcı anormal getiri bildirildi (sayı doğrulanamadı) [K27] | SEC başvuru geçmişi | EVET (sec_ozet) | düşük | nadir |
| E_SPLIT | EVT | son 12 ayda ileri bölünme (≥ 2:1) | + | Ikenberry-Rankine-Stice 1996 JFQA | ilk yıl +%7,93, üç yıl +%12,15 (1.275 bölünme) [K28] | Yahoo bölünme | İNDİR | düşük | |
| E_RSPLIT | EVT | son 12 ayda ters bölünme | − | Kim-Klein-Rosenfeld 2008 Financial Management; Desai-Jain 1997 J. Business | 3 yıl anlamlı eksi; Desai-Jain: 1 yıl −%10,8, 3 yıl −%33,9 (ikincil alıntı) [K29] | Yahoo bölünme; 8-K 3.03 / 5.03 | İNDİR | çok yüksek | kaçınma |
| E_IDX_ADD | EVT | son 20 günde S&P 500'e ekleme duyurusu | + (sönmüş) | Greenwood-Sammon 2025 JF | 1990'lar %7,4 → son on yıl %1'in altı (çalışma metni) [K30] | Wikipedia değişiklik tablosu | İNDİR | düşük | etki kaybolmuş: düşük öncelik |
| E_SPINOFF | EVT | ayrılma (10-12B) sonrası ilk 24 ay, ayrılan şirket | + | Cusatis-Miles-Woolridge 1993 JFE | OP 2,08 / t 2,4 VW | EDGAR form dizini | İNDİR | orta | yeni CIK evrende yok: form.idx gerekir |
| E_DIV_INIT | EVT | son 12 ayda ilk temettü | + | Michaely-Thaler-Womack 1995 JF | OP 0,62 / t 3,4 EW | Yahoo temettü | İNDİR | düşük | |
| E_DIV_OMIT | EVT | son 12 ayda temettü kesme | − | Michaely-Thaler-Womack 1995 JF | OP 0,92 / t 6,3 EW | Yahoo temettü | İNDİR | orta | |

### A12. Sektör ve makro bağlantılar (SEC)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| IND_MOM_6 | SEC | sektörün (SIC 2 hane) son 6 ay eşit ağırlıklı getirisi | + | Moskowitz-Grinblatt 1999 JF | OP 0,43 / t 4,7 EW | fiyat + SIC (k35) | EVET | orta | kapalı konu "sektör ısısı"na dokunur (ana model kararı) |
| IND_LEAD_BIG | SEC | aynı sektörün en büyük %30 şirketinin geçen ay getirisi | + | Hou 2007 RFS | OP t 11,0 EW | fiyat, SIC, piyasa değeri | EVET† | orta | küçükler büyükleri gecikmeyle izler; %30 eşiği makaleden doğrulanamadı, ön kayıtta sabitlenir |
| COMM_LINK | SEC | sektörün emtia duyarlılığı (36 ay regresyon) × emtianın geçen ay getirisi | ? | doğrulanamadı (kesit düzeyinde yayımlanmış kanıt bulunamadı) | doğrulanamadı | fiyat, SIC, k36 emtia serileri | EVET | orta | "şüpheli / keşif" etiketi |
| IO_MOM_CUST | SEC | müşteri sektörlerinin geçen ay getirisi (BEA girdi-çıktı ağırlıklı) | + | Menzly-Ozbas 2010 JF | OP t 4,1 EW | BEA tabloları + SIC eşlemesi | İNDİR | orta | |
| IO_MOM_SUPP | SEC | tedarikçi sektörlerinin geçen ay getirisi | + | Menzly-Ozbas 2010 JF | OP t 5,0 EW | BEA tabloları + SIC eşlemesi | İNDİR | orta | |
| GEO_MOM | SEC | aynı kentte (eyalette) merkezli, başka sektördeki şirketlerin geçen ay getirisi | + | Parsons-Sabbatucci-Titman 2020 RFS | risk düzeltmeli yılda %5–6 [K31] | SEC adres alanı | İNDİR | orta | adres bugünkü adres: geçmişe bakma riski |
| CUST_MOM | SEC | şirketin adı açıklanan büyük müşterilerinin geçen ay getirisi | + | Cohen-Frazzini 2008 JF | OP 1,58 / t 3,8 VW | müşteri-tedarikçi eşlemesi (Compustat segment) | YOK | — | XBRL'de müşteri adı etiketli değil |

### A13. Metin (TXT)

| kod | aile | tanım | yön | ana kaynak | büyüklük | gereken veri | bizde var mı | batan | not |
|---|---|---|---|---|---|---|---|---|---|
| LAZY_SIM | TXT | bu yılın 10-K'sı ile geçen yılınki arasındaki benzerlik (kosinüs / Jaccard); düşük benzerlik = çok değişiklik | + (benzerlik yüksekse) | Cohen-Malloy-Nguyen 2020 JF | "değiştirmeyen − değiştiren" portföyü ayda 188 bp'ye kadar alfa (1995–2014) [K32] | 10-K / 10-Q tam metinleri | İNDİR (ağır) | orta | onlarca GB; ikinci tura bırakılabilir |
| TONE_NEG | TXT | 10-K'da Loughran-McDonald olumsuz sözcük payı | − | Loughran-McDonald 2011 JF | doğrulanamadı | LM 10-X özet dosyası | İNDİR | orta | lisans: ticari olmayan kullanım |
| TONE_CHG | TXT | olumsuz + belirsizlik + dava sözcük payının yıllık değişimi | − | Cohen-Malloy-Nguyen 2020 JF (dava / risk dili değişimi) | doğrulanamadı | LM 10-X özet dosyası | İNDİR | orta | LAZY_SIM'in ucuz vekili |

## B. Olay tablosu (olay → aylık sinyal)

Ortak kural: olay "son N günde oldu" bayrağına çevrilir; bayrak ay sonunda okunur.

Zaman damgası:
- **Kabul anı** = SEC `acceptanceDateTime` (doğu saati). 16:00'dan sonra ya da tatil günü kabul edilen başvuru ertesi işlem günü bilinir sayılır.
- Projedeki `sec_ozet.json` yalnız başvuru gününü (`filingDate`) tutuyor, kabul anını tutmuyor. Yeniden indirilene kadar muhafazakâr kural: bilgi günü = başvuru günü + 1 işlem günü.
- `form.idx` yalnız form türü, şirket, CIK, gün ve dosya yolunu verir; **8-K madde kodu orada yoktur**. Madde kodu `submissions` JSON'ındaki `items` alanından gelir.

Kaynak URL'leri:
- U1: `https://data.sec.gov/submissions/CIK##########.json` (form, filingDate, acceptanceDateTime, items); toplu: `https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip`
- U2: `https://www.sec.gov/Archives/edgar/full-index/{YYYY}/QTR{n}/form.idx`
- U3: `https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{YYYY}q{n}_form345.zip`
- U4: `https://www.sec.gov/files/dera/data/financial-statement-data-sets/{YYYY}q{n}.zip`
- U5: FINRA `https://cdn.finra.org/equity/otcmarket/biweekly/shrt{YYYYMMDD}.csv` ve API `POST https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest`

| olay | tanım (aylık sinyal) | kaynak | zaman damgası | yön | literatür |
|---|---|---|---|---|---|
| 8-K 1.01 önemli sözleşme | E_101: son 20 işlem günü | U1 `items` | kabul anı | ? | Lerman-Livnat 2010 (8-K geneli); madde özelinde doğrulanamadı |
| 8-K 1.03 iflas | sinyal değil: evren sınıflaması (K54) | U1 | kabul anı | — | — |
| 8-K 2.01 devralma tamamlandı | E_201: son 60 gün | U1 | kabul anı | − | doğrulanamadı |
| 8-K 2.02 sonuç açıklaması | sinyal değil: EAR_ANN, SUE, EA_MONTH için bilanço günü | U1 | kabul anı; 16:00 sonrası ise tepki günü ertesi gün | — | Chan-Jegadeesh-Lakonishok 1996 |
| 8-K 2.05 / 2.06 | E_205_206: son 60 gün | U1 | kabul anı | ? | doğrulanamadı |
| 8-K 3.01 kot uyarısı | E_301: son 120 gün | U1 | kabul anı | − | Macey-O'Hara-Pompilio 2008 (sayı doğrulanamadı) |
| 8-K 3.02 kayıtsız satış | E_302: son 60 gün | U1 | kabul anı | − | Hertzel et al. 2002 [K23] |
| 8-K 4.01 denetçi değişimi | E_401: son 120 gün | U1 | kabul anı | − | doğrulanamadı |
| 8-K 4.02 güvenilmez tablolar | E_402: son 120 gün | U1 | kabul anı | − | Palmrose et al. 2004 [K24] |
| 8-K 5.02 yönetici değişimi | E_502: son 60 gün | U1 | kabul anı | ? | doğrulanamadı |
| S-3 / S-3ASR raf kaydı | E_S3: son 90 gün | U1 ya da U2 | kabul anı | − | Loughran-Ritter 1995 [K25] |
| 424B5 raftan satış | E_424B5: son 60 gün | U1 ya da U2 | kabul anı | − | Loughran-Ritter 1995; Billett et al. 2019 |
| İlk halka arz | E_IPO_3Y, E_LOCKUP: 424B4 günü + 180 takvim günü | U1 ya da U2 | 424B4 başvuru günü | − | Ritter 1991; Field-Hanka 2001 [K26] |
| Bölünme / ters bölünme | E_SPLIT, E_RSPLIT: son 12 ay | Yahoo bölünme listesi; duyuru için 8-K 5.03 / 3.03 | bölünme günü (duyuru günü değil: daha geç ve güvenli) | + / − | Ikenberry et al. 1996 [K28]; Kim et al. 2008 [K29] |
| Endekse ekleme | E_IDX_ADD: son 20 gün | `https://en.wikipedia.org/wiki/List_of_S%26P_500_companies` (değişiklik tablosu) | tablodaki gün = yürürlük günü; duyuru günü ayrıca yok | + (sönmüş) | Greenwood-Sammon 2025 [K30] |
| Ayrılma (spin-off) | E_SPINOFF: ilk 24 ay | U2 (10-12B, 10-12B/A) + ilk fiyat günü | ilk işlem günü | + | Cusatis et al. 1993 |
| Birleşme hedefi | E_MA_TARGET | U1 (DEFM14A, SC 14D9, SC TO-T) | kabul anı | + (küçük) | Mitchell-Pulvino 2001 (sayı doğrulanamadı) |
| Şirketin kendi çağrısı | E_TENDER_SELF: son 90 gün | U1 (SC TO-I) | kabul anı | + | Peyer-Vermaelen 2009 [K27] |
| Geç başvuru | NT_LATE: son 60 gün | U1 (NT 10-K, NT 10-Q) | kabul anı | − | Bartov-Konchitchki 2017 [K21] |
| %5 üstü etkin ortak | ACT_13D: son 60 gün, ilk SC 13D | U1 | kabul anı (olaydan en çok 10 gün sonra; 2024'ten beri 5 iş günü, doğrulanamadı) | + | Brav et al. 2008 [K12] |
| İçeriden alım / satım | INS_*: son 90 gün | U3 (`FILING_DATE`) | başvuru günü + 1 işlem günü (işlem günü değil) | + / − | [K9], [K10], [K11] |
| Açığa satış pozisyonu | SI_RATIO, DTC, SI_LOW | U5 | ödeme günü + 12 takvim günü (K31 kuralı; yayın ~1 hafta sonra) | − / + | [K13], [K14] |
| Kayıtlı pay artışı | NSI_1Y (sürekli ölçü) | U4 ya da frames | 10-Q / 10-K başvuru günü + 1 | − | Pontiff-Woodgate 2008 |
| Süreklilik şüphesi | GC_FLAG | EDGAR tam metin arama | 10-K / 10-Q kabul anı | − | Kausar et al. 2009 [K22] |
| Temettü başlatma / kesme | E_DIV_INIT, E_DIV_OMIT | Yahoo temettü | hak düşüm günü (duyuru günü yok: daha geç ve güvenli) | + / − | Michaely et al. 1995 |
| Analist notu | REC_UP, REC_DOWN, PT_REV | Yahoo `upgrades_downgrades` | kayıt günü + 1 işlem günü | + / − | Womack 1996 [K17] |

## C. Veri planı (her "İNDİR" kaynağı)

SEC kuralı: saniyede en çok 10 istek; istek başlığında şirket adı + iletişim e-postası içeren User-Agent beklenir [K33]. Cemal'in e-postası yalnız `SEC_EPOSTA` ortam değişkeninden okunur, hiçbir dosyaya, günlüğe ya da rapora yazılmaz. Bu oturumda `SEC_EPOSTA` tanımlı değil: SEC indirmeleri Cemal değişkeni tanımlayınca yapılır. SEC içeriği kamu bilgisidir; izinsiz kopyalanabilir ve dağıtılabilir, kaynak gösterilmesi istenir [K34].

| # | kaynak | URL / uç | boyut | istek | hız sınırı | lisans; türetilmiş tablo islenmis-veri'ye konur mu | SEC e-posta UA |
|---|---|---|---|---|---|---|---|
| 1 | SEC XBRL frames: eldeki 7 etiketin 2014Q1–2019Q4 çeyrekleri + yeni etiketler | `https://data.sec.gov/api/xbrl/frames/us-gaap/{etiket}/USD/CY{yıl}Q{n}[I].json`; pay için `/shares/` | çerçeve başına ortalama 0,5 MB (önbellekte ölçüldü: 207 dosya, 103 MB) → ~0,8 GB | ~1.600 (10 anlık etiket × 50 çeyrek; 14 süreli etiket × 63 dönem; eldeki 7 etiketin eski dönemleri ~190) | 10 / sn (projede 8) | kamu; EVET | EVET |
| 2 | SEC finansal tablo veri setleri 2014q1–2020q4 (nakit akış kalemleri, pay sayısı) | U4 | çeyrek 14–122 MB (sayfadan); 2016–20 ~1,6 GB (K56 ölçümü) | 28 | 10 / sn | kamu; EVET (secfs biçiminde özüt) | EVET |
| 3 | SEC başvuru geçmişi: kabul anı + 8-K madde kodu, geniş evren | U1; şirket başına JSON ya da toplu zip | toplu zip boyutu doğrulanamadı (1 GB üstü beklenir); şirket başına 3.262 istek | 1 ya da ~3.300–6.000 | 10 / sn | kamu; EVET (sec_ozet v2: `acceptanceDateTime` eklenir) | EVET |
| 4 | EDGAR form dizini (10-12B, evren dışı CIK'ler) | U2 | çeyrek boyutu doğrulanamadı | ~51 (2014–2026) | 10 / sn | kamu; EVET | EVET |
| 5 | SEC içeriden işlem veri setleri | U3; 2006q1+ | 2016q1–2021q4 = 24 çeyrek ~248 MB (K56 ölçümü) | ~55 (2013q1–2026q3) | 10 / sn | kamu; EVET (özet). Ham zip repoya konmaz (27 Ekim kuralı) | EVET |
| 6 | SEC 13F veri setleri + CUSIP → sembol | `https://www.sec.gov/files/structureddata/data/form-13f-data-sets/{dönem}_form13f.zip` (2013q2+); eşleme OpenFIGI | dosya 37–96 MB (sayfadan); toplam ~3 GB | ~53 + eşleme istekleri | SEC 10 / sn; OpenFIGI sınırı doğrulanamadı | kamu; sembol düzeyinde toplam tablo EVET. CUSIP listesi repoya konmaz (lisans tartışması, K56) | EVET |
| 7 | FINRA açığa satış pozisyonu | U5; arşiv `https://otce.finra.org/otce/EquityShortInterest/staticArchives` | dosya ~3 MB, ayda 2; 2017-12+ ~210 dosya ≈ 0,6 GB | ~210 | doğrulanamadı | kullanım koşulu doğrulanamadı ("ticari olmayan kullanım" ifadesi var). Ham veri repoya KONMAZ; türetilmiş oran tablosu için karar gerekir | HAYIR |
| 8 | FINRA Reg SHO günlük açığa satış hacmi | `https://cdn.finra.org/equity/regsho/daily/CNMSshvol{YYYYMMDD}.txt` (2018-08+) | gün ~0,3 MB → ~0,6 GB | ~2.000 | doğrulanamadı | 7 ile aynı | HAYIR |
| 9 | Yahoo analist günlüğü | yfinance `Ticker(s).upgrades_downgrades` | küçük (K52: 310 bin kayıt) | ~3.300 | resmî sınır yok; 429 görülüyor | resmî olmayan uç; koşul belirsiz. Ham kayıt repoya konmaz; aylık sinyal tablosu için karar gerekir | HAYIR |
| 10 | Yahoo temettü ve bölünme | yfinance `Ticker(s).actions` | küçük | ~3.300 | 9 ile aynı | 9 ile aynı (fiyat paketi zaten Cemal kararıyla dalda) | HAYIR |
| 11 | EDGAR tam metin arama (süreklilik şüphesi) | `https://efts.sec.gov/LATEST/search-index?q="substantial doubt"&forms=10-K,10-Q&dateRange=custom&startdt=...&enddt=...` (belgelenmemiş uç; arayüz `https://www.sec.gov/edgar/search/`) | küçük (JSON) | çeyrek başına sayfalı; birkaç yüz | 10 / sn | kamu; EVET. Kapsam 2001+ [K35] | EVET |
| 12 | Loughran-McDonald 10-X özetleri | `https://sraf.nd.edu/sec-edgar-data/lm_10x_summaries/` (tek CSV, 1993–2024) | 188 MB | 1 | — | "ticari olmayan amaçla"; ticari kullanım için izin istenir [K36]. Gerçek parayla kullanım ticari sayılabilir: Cemal kararı. Repoya KONMAZ | HAYIR |
| 13 | 10-K / 10-Q tam metinleri (LAZY_SIM) | `https://www.sec.gov/Archives/edgar/data/{cik}/{adsh}.txt` | onlarca GB (tahmin; ölçülmedi) | ~100 bin+ | 10 / sn (≥ 3 saat) | kamu; yalnız benzerlik puanı tablosu EVET | EVET |
| 14 | BEA girdi-çıktı tabloları | `https://www.bea.gov/industry/input-output-accounts-data` (adres bu oturumda açılmadı: doğrulanamadı) | küçük | 1–3 | — | ABD kamu verisi; EVET | HAYIR |
| 15 | S&P 500 değişiklik tablosu | Wikipedia (yukarıda) | küçük | 1 | — | CC BY-SA; kaynak gösterilerek EVET | HAYIR |
| 16 | French faktörleri, 49 sektör tanımı | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html` | küçük | 3–5 | — | serbest erişim; K58 önbelleği var | HAYIR |
| 17 | Kıyas serileri (yanlılıksız): Chen-Zimmermann portföyleri, JKP faktörleri | `https://www.openassetpricing.com`, `https://jkpfactors.com` | küçük | birkaç | — | açık veri; kaynak gösterilir | HAYIR |

Üç uyarı:
1. **Nakit akış kalemleri frames'te çeyreklik eksik gelir.** Şirketler nakit akışını yılbaşından bugüne (6 ay, 9 ay) bildirir; frames yalnız ~91 günlük dönemleri "çeyrek" sayar. OCF, yatırım harcaması, geri alım, ihraç geliri için ya yıllık çerçeve (CY) kullanılır ya da satır 2'deki veri setinden fark alınır (secfs özütü bunu `qtrs` sütunuyla yapıyor). Öneri: nakit akış kalemleri satır 2'den, bilanço ve gelir kalemleri satır 1'den.
2. **Frames son bildirilen değeri verir** (sonradan düzeltilmiş olabilir); tarih özgün başvuru günüdür (K59 ön kaydındaki sınırla aynı).
3. **2016–2017 açığa satış pozisyonu ücretsiz yok.** SI ailesi KEŞİF'in yalnız 2018–2021 bölümünde ölçülür.

Önerilen yeni etiketler (satır 1–2): Assets, AssetsCurrent, LiabilitiesCurrent, CashAndCashEquivalentsAtCarryingValue, LongTermDebt, DebtCurrent, InventoryNet, PropertyPlantAndEquipmentNet, RetainedEarningsAccumulatedDeficit, CommonStockSharesOutstanding, GrossProfit, CostOfRevenue, OperatingIncomeLoss, SellingGeneralAndAdministrativeExpense, ResearchAndDevelopmentExpense, DepreciationDepletionAndAmortization, IncomeTaxExpenseBenefit, NetCashProvidedByUsedInOperatingActivities, PaymentsToAcquirePropertyPlantAndEquipment, PaymentsForRepurchaseOfCommonStock, ProceedsFromIssuanceOfCommonStock, PaymentsOfDividends, ProceedsFromIssuanceOfLongTermDebt, RepaymentsOfLongTermDebt.

## D. BIST'e uygulanabilirlik

BIST karar hücresi değil, bilgidir (28 Ekim kuralı); fon krizi kesimi 31.08.2026 geçerlidir. Eldeki BIST verisi: V_BIST (fiyat-hacim, 2016-09+), temel_duz.csv (562 hisse, 2022/12–2026/6 dönemleri; net_kar_q, satis_q, ozkaynak, fin_borc, nakit, net_borc, borc_oz), KAP finansal rapor günleri (2016-07+), KAP pay alım satım bildirimleri (2022-07+), K25 fon payı tabloları, sektor_BIST.csv.

| durum | sinyaller | açıklama |
|---|---|---|
| HESAPLANIR (fiyat-hacim) | MOM ailesinin tamamı, RSK ailesinin tamamı, AMIHUD, DOLVOL, VOL_SHOCK, SPREAD_CS, GAP_OVN, SEAS_1, SEAS_2_5, TAXLOSS_JAN, IND_MOM_6 | V_BIST + sektor_BIST.csv. IVOL / artık momentum için yerel piyasa faktörü kurulmalı (French faktörü yok). Tavan / taban sınırı MAX5 ve gece getirisini bozar |
| HESAPLANIR (temel_duz) | ROE_TTM, SUE_SRW, REV_SURP, EARN_STREAK, SALES_ACCEL, BE_G; net_borc / özkaynak ve nakit / fin_borc (kaldıraç, yerel ölçü) | yalnız 2022/12+ : KEŞİF dönemi yok, en fazla 2024–26 bilgisi. Enflasyon muhasebesi geçişi seriyi kırabilir (bu oturumda doğrulanamadı) |
| HESAPLANIR (KAP) | EAR_ANN, EA_MONTH (finansal rapor günü); INS_BUY_90, INS_CLUSTER, INS_SELL_90 (pay alım satım bildirimi); fon payı değişimi (IO_CHG'nin yerel karşılığı, K25) | K27, K28, K25 kodları hazır |
| YAKLAŞIK | BM, EP, SP, SIZE_ME, TURN_12M, IND_LEAD_BIG, CHS_FAIL | tarihsel pay sayısı yok (İş Yatırım sayfası yalnız bugünkü sermayeyi verir). Bedelsiz artış fiyat düzeltmesiyle giderilir; bedelli / tahsisli artış giderilemez |
| HESAPLANAMAZ (kalem yok) | AM, LEV_MKT, CFP, EV_EBITDA, NET_PAYOUT_YLD, ROA_Q, D_ASSET_TURN, ACCRUALS, GP_A, OP_BE, CBOP_A, F_SCORE, NOA, OPLEV, RD_ME, TAX_CHG, ASSET_G, NEF, NDF, BUYBACK_YLD, CAPEX_G, INV_A, INVTRY_G, RUNWAY, O_SCORE, Z_SCORE | temel_duz'da toplam varlık, toplam borç, brüt kâr, faaliyet kârı, nakit akışı, stok yok. KAP finansal tablolarından yeni özüt gerekir (ayrı iş) |
| HESAPLANAMAZ (veri yok) | NSI_1Y, NSI_5Y (bedelli / bedelsiz ayrımı yok: K57 notu), SI_RATIO, DTC, SI_LOW, SHORT_VOL, analist ailesi, 13F ailesi, ACT_13D, 8-K madde olayları, S-3 / 424B5, GC_FLAG, NT_LATE, TXT ailesi, IO_MOM, GEO_MOM | KAP "özel durum açıklaması" türleri (sermaye artırımı, pay geri alım, yeni iş ilişkisi) ile 8-K benzeri olay seti kurulabilir; bugün yok. Borsa İstanbul açığa satış verisi doğrulanamadı |

## E. Kütüphaneye ALINMAYANLAR ve bilinen yineleme başarısızlıkları

| ne | neden alınmadı |
|---|---|
| Analist EPS tahmini, revizyonu, dağılımı, uzun vade büyüme tahmini (IBES) | ücretli. Yahoo yalnız not değişikliği veriyor |
| Borsadan çıkış getirisi (CRSP) | ücretli; yokluğu küçüklük, dönüş ve sıkıntı ailesini şişirir (Shumway 1997). Çözüm: Tiingo (EVREN_SECENEKLERI) |
| Opsiyon ölçüleri (ima edilen oynaklık farkı, eğim, opsiyon / hisse hacmi) | OptionMetrics ücretli |
| Gün içi ölçüler (TAQ: emir akışı, PIN, gerçek alış-satış farkı, gün içi momentum) | ücretli; günlük vekiller alındı |
| Kredi notu değişimi, yönetişim endeksi, patent / atıf, emeklilik fonu açığı, reklam gideri | veri ücretli ya da XBRL'de düzensiz |
| Şirket düzeyi müşteri-tedarikçi, holding (segment) momentumu | segment / müşteri verisi ücretli (CUST_MOM satırı YOK olarak duruyor) |
| Takvim etkileri (ay dönümü, "mayısta sat", haftanın günü, tatil öncesi) | piyasa zamanlamasıdır, hisse seçmez; cetvel kesit cetveli |
| VIX / makro beta | projede kapalı konu (VIX / DXY) |
| Grafik şekli, formasyon | projede kapalı (90+ şekil ölçüsü; yol haritası "BIRAKILANLAR") |
| Makine öğrenmesi bileşikleri | sinyal değil yöntem; K60 önce tek sinyal ve aile bileşiği ölçer |

Bilinen yineleme sonuçları (K60 yorumunda kullanılacak):
- **Hou-Xue-Zhang 2020 (RFS):** 452 anomalinin %65'i NYSE kesim noktaları ve değer ağırlığıyla |t| ≥ 1,96 eşiğini geçemiyor; eşik 2,78 olunca %82'si. İşlem sürtünmesi ailesinin (likidite, oynaklık, hacim) %96'sı başarısız. Tutanların büyüklüğü de özgün makaledekinden küçük [K3]. Anlamı: A7 ve A8'deki EW sonuçları mikro hisse kaynaklı olabilir; likidite tabanı şart.
- **Green-Hand-Zhang 2017 (RFS):** 94 özellikten mikro hisseler dışında 1980–2014'te yalnız 12'si bağımsız bilgi taşıyor; 2003'ten sonra yalnız 2'si. Mikro hisse dışı korunma getirisi 2003 sonrası sıfırdan farksız [K5]. Anlamı: KEŞİF dönemimiz (2016–2021) zaten "zor" dönemdir; düşük başarı oranı beklenmelidir.
- **Jensen-Kelly-Pedersen 2023 (JF):** 153 faktör, 93 ülke; Bayesçi yaklaşımda yineleme oranı %82,4 [K4]. İkincil özete göre 13 temanın 10'unda oran %75 üstü; zayıf kalanlar mevsimsellik, kaldıraç, boyut [K4b]. Anlamı: aile (tema) düzeyinde okuma tek sinyalden sağlamdır; yol haritası kural 5 ile uyumlu.
- **McLean-Pontiff 2016 (JF):** yayın sonrası −%58 [K2]. Kütüphanedeki OP sayıları üst sınırdır.
- **Harvey-Liu-Zhu 2016 (RFS):** yeni keşif için t > 3,0 [K6]. Yol haritası kural 4 ile aynı.
- **Novy-Marx-Velikov 2016 (RFS):** aylık devri %50'nin altındaki anomalilerin çoğu maliyet sonrası kalıyor, üstündekilerin azı [K7]. Anlamı: STREV_1M, MAX5, VOL_SHOCK, SEAS_1 gibi yüksek devirli sinyaller maliyetli cetvelde büyük olasılıkla düşer.
- **Engelberg-McLean-Pontiff 2018 (JF):** anomali getirisi haber günlerinde %50, bilanço günlerinde 6 kat yüksek [K8]. Anlamı: bilanço merkezli sinyaller (EAR ailesi) ve bilanço takvimi önemlidir.
- **Chen-Zimmermann 2022:** özgün makalede açıkça anlamlı sinyallerin %98'i yeniden üretilebiliyor [K1]; aynı belge özgün makalede açık kanıt OLMAYAN ölçüleri de listeliyor: Altman Z (t 1,6), CHS batma olasılığı (t 1,4), aşağı yön betası (t 0,6), kâr marjı (t 1,0), ROIC (t 0,9), Kaplan-Zingales (t 1,1). Z_SCORE ve CHS_FAIL kütüphanede yalnız kaçınma süzgeci adayı olarak durur.

## F. Öncelik sırası: ilk 30

Ölçütler (eşit ağırlıkla, sayısal puan değil sıralama): (1) yayın sonrası ve VW sağlamlığı (HXZ, JKP, GHZ), (2) veri bugün elde, (3) batan yanlılığı düşük, (4) ayda 1–2 hisse alan küçük hesaba uygunluk (yalnız alım; kaçınma süzgeci de değerlidir; devir düşük).

| sıra | kod | neden |
|---|---|---|
| 1 | MOM_12_1 | en çok yinelenen; veri hazır; K58'de kalibre |
| 2 | EAR_ANN | bilanço tepkisi; batan yanlılığı düşük; Cemal'in "bilanço günü güçlü tepki" tanımı |
| 3 | ROE_TTM | kârlılık teması VW'de tutuyor; veri hazır |
| 4 | NSI_1Y | ihraç; kaçınma olarak değerli; veri hazır |
| 5 | HIGH52 | basit; veri hazır |
| 6 | ASSET_G | yatırım teması; veri hazır |
| 7 | SUE_SRW | PEAD'in temel sürümü; veri hazır |
| 8 | MOM_RES_12_1 | momentumun daha az çöken sürümü |
| 9 | INS_BUY_90 | ekonomik nedeni açık; küçük şirkette güçlü; veri hazır |
| 10 | GP_A | VW'de tutan kârlılık ölçüsü; tek etiket indirilir |
| 11 | ACCRUALS | kazanç kalitesi; 2021+ hazır |
| 12 | BM | değer teması; veri hazır |
| 13 | CFP | değerin nakit sürümü |
| 14 | ROA_Q | çeyreklik kârlılık; hazır |
| 15 | REV_SURP | satış sürprizi; hazır |
| 16 | IND_MOM_6 | Cemal'in "sektör rüzgârı" şartının ölçülmüş hali |
| 17 | MOM_INT_12_7 | momentum ailesi içi |
| 18 | VOL_60D | düşük oynaklık; hazır (yanlılık yüksek: bantla okunur) |
| 19 | BETA_BAB | düşük risk teması |
| 20 | MAX5 | piyango hisselerinden kaçınma süzgeci |
| 21 | NET_PAYOUT_YLD | geri alım + temettü − ihraç |
| 22 | F_SCORE | bileşik kalite |
| 23 | E_302 | kayıtsız satış: seyrelme kaçınması; veri hazır |
| 24 | E_424B5 | raftan satış: seyrelme kaçınması; veri hazır |
| 25 | RUNWAY | nakit tükenmesi kaçınması; veri hazır |
| 26 | INS_OPP_BUY | içeriden alımın rafine sürümü |
| 27 | DTC | açığa satış: kaçınma |
| 28 | SI_LOW | açığa satışın alım yönü |
| 29 | EA_MONTH | bilanço ayı primi |
| 30 | EP | değer ailesi içi |

İkinci dalga (31–60): kalan PRF ve INV satırları, analist ailesi, NT_LATE, ACT_13D, E_S3, E_RSPLIT, GC_FLAG, IND_LEAD_BIG, SEAS ailesi. Son dalga: 13F ailesi (eşleme çözülürse), TXT ailesi, IO_MOM, GEO_MOM, COMM_LINK.

## G. Ana modele notlar

- **Kapalı konu sınırı:** EAR_VOL ve VOL_SHOCK "hacim", IND_MOM_6 "sektör ısısı", TREND_MA "şekil" başlığına yakındır. Bunlar çöl giriş zamanlaması değil, portföy düzeyi literatür faktörleridir; yine de kütüphaneye alınıp alınmayacağı ana modelin / Cemal'in kararıdır.
- **Cemal kararı gereken:** (a) `SEC_EPOSTA` değişkeni (bütün SEC indirmeleri); (b) FINRA ve Yahoo'dan türetilmiş tabloların islenmis-veri'ye konması; (c) Loughran-McDonald verisinin gerçek parayla kullanımı.
- **Sayım:** 120 satır = bugün hesaplanır 70 (EVET 48 + EVET† 22, yani 22'sinin geçmişi kısa), İNDİR 46, YOK 4. İlk 30'un 24'ü bugün hesaplanır; 6'sı indirme ister (GP_A, NET_PAYOUT_YLD, F_SCORE, INS_OPP_BUY, DTC, SI_LOW).
- **K60 için asgari indirme:** bölüm C satır 1–3 ve 5. Bunlar olmadan temel veriye dayalı hiçbir sinyal KEŞİF'in 2016–2019 bölümünde ölçülemez.

## Kaynaklar (erişim 11 Kasım 2026)

- [K1] Chen, Zimmermann 2022, "Open Source Cross-Sectional Asset Pricing", Critical Finance Review 11(2): https://ideas.repec.org/a/now/jnlcfr/104.00000112.html ; sinyal belgesi: https://github.com/OpenSourceAP/CrossSection/blob/master/SignalDoc.csv ; veri: https://www.openassetpricing.com
- [K2] McLean, Pontiff 2016, JF 71(1): https://doi.org/10.1111/jofi.12365 (özet sayfası okundu)
- [K3] Hou, Xue, Zhang 2020, "Replicating Anomalies", RFS 33(5): https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html
- [K4] Jensen, Kelly, Pedersen 2023, JF 78(5): https://doi.org/10.1111/jofi.13249 ; veri: https://jkpfactors.com ; [K4b] ikincil özet: https://alphaarchitect.com/is-there-a-replication-crisis-in-finance/
- [K5] Green, Hand, Zhang 2017, RFS 30(12): https://ideas.repec.org/a/oup/rfinst/v30y2017i12p4389-4436..html
- [K6] Harvey, Liu, Zhu 2016, RFS 29(1): https://www.nber.org/papers/w20592
- [K7] Novy-Marx, Velikov 2016, RFS 29(1): https://www.nber.org/papers/w20721
- [K8] Engelberg, McLean, Pontiff 2018, JF 73(5): https://ideas.repec.org/a/bla/jfinan/v73y2018i5p1971-2001.html
- [K9] Cohen, Malloy, Pomorski 2012, JF 67(3): https://www.nber.org/papers/w16454 (sayı çalışma metni özetinden)
- [K10] Jeng, Metrick, Zeckhauser 2003, REStat 85(2): https://econpapers.repec.org/RePEc:tpr:restat:v:85:y:2003:i:2:p:453-471
- [K11] Lakonishok, Lee 2001, RFS 14(1): https://ideas.repec.org/a/oup/rfinst/v14y2001i1p79-111.html
- [K12] Brav, Jiang, Partnoy, Thomas 2008, JF 63(4): https://econpapers.repec.org/RePEc:bla:jfinan:v:63:y:2008:i:4:p:1729-1775 (sayı çalışma metni özetinden)
- [K13] Hong, Li, Ni, Scheinkman, Yan 2015, NBER 21166: https://www.nber.org/papers/w21166
- [K14] Boehmer, Huszar, Jordan 2010, JFE 96(1): https://ideas.repec.org/a/eee/jfinec/v96y2010i1p80-97.html
- [K17] Womack 1996, JF 51(1): https://ideas.repec.org/a/bla/jfinan/v51y1996i1p137-67.html
- [K18] Gervais, Kaniel, Mingelgrin 2001, JF 56(3): https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:877-919
- [K19] Lou, Polk, Skouras 2019, JFE 134(1): https://personal.lse.ac.uk/polk/research/TugOfWar.pdf
- [K20] Frazzini, Lamont 2007: https://www.nber.org/papers/w13090 ; Savor, Wilson 2016, JF 71(1) (özetten: yıllık %9,9)
- [K21] Bartov, Konchitchki 2017, Accounting Horizons 31(4): https://faculty.haas.berkeley.edu/yaniv/files/Papers_Publications/SEC-Filings-Regulatory-Deadlines-Capital-Market-Consequences_Bartov-Konchitchki_AH.pdf
- [K22] Kausar, Taffler, Tan 2009, JAR 47(1): https://econpapers.repec.org/RePEc:bla:joares:v:47:y:2009:i:1:p:213-239
- [K23] Hertzel, Lemmon, Linck, Rees 2002, JF 57(6): https://ideas.repec.org/a/bla/jfinan/v57y2002i6p2595-2617.html
- [K24] Palmrose, Richardson, Scholz 2004, JAE 37(1): https://econpapers.repec.org/RePEc:eee:jaecon:v:37:y:2004:i:1:p:59-89
- [K25] Loughran, Ritter 1995, JF 50(1): https://ideas.repec.org/a/bla/jfinan/v50y1995i1p23-51.html ; Billett, Floros, Garfinkel 2019, JFQA 54(3): https://ideas.repec.org/a/cup/jfinqa/v54y2019i03p1263-1283_00.html
- [K26] Field, Hanka 2001, JF 56(2): https://ideas.repec.org/a/bla/jfinan/v56y2001i2p471-500.html
- [K27] Peyer, Vermaelen 2009, RFS 22(4): https://ideas.repec.org/a/oup/rfinst/v22y2009i4p1693-1745.html
- [K28] Ikenberry, Rankine, Stice 1996, JFQA 31(3): https://ideas.repec.org/a/cup/jfinqa/v31y1996i03p357-375_00.html
- [K29] Kim, Klein, Rosenfeld 2008, Financial Management 37(2): https://ideas.repec.org/a/bla/finmgt/v37y2008i2p173-192.html
- [K30] Greenwood, Sammon 2025, JF 80(2): https://www.nber.org/papers/w30748 (sayılar çalışma metni sürümlerinde farklı: %7,4 ya da %7,6)
- [K31] Parsons, Sabbatucci, Titman 2020, RFS 33(10): https://ideas.repec.org/a/oup/rfinst/v33y2020i10p4721-4770..html
- [K32] Cohen, Malloy, Nguyen 2020, JF 75(3): https://www.nber.org/papers/w25084
- [K33] SEC, EDGAR verisine erişim: https://www.sec.gov/os/accessing-edgar-data ; API'ler: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- [K34] SEC, dağıtım politikası: https://www.sec.gov/privacy
- [K35] SEC, tam metin arama SSS: https://www.sec.gov/edgar/search/efts-faq.html
- [K36] Loughran-McDonald veri sayfası: https://sraf.nd.edu/sec-edgar-data/lm_10x_summaries/
- SEC veri setleri: https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets ; https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets ; https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
- FINRA: https://www.finra.org/finra-data/browse-catalog/equity-short-interest/files
- Künyesi bu oturumda doğrulanamayan (bellekten yazılan; Chen-Zimmermann belgesinde ve yukarıdaki listede olmayan) kaynaklar: Da-Gurun-Warachka 2014 RFS; Bernard-Thomas 1989 JAR; Garfinkel-Sokobin 2006 JAR; Brav-Lehavy 2003 JF; Nofsinger-Sias 1999 JF; Boehmer-Jones-Zhang 2008 JF; Boyer-Mitton-Vorkink 2010 RFS; Corwin-Schultz 2012 JF; Keim 1983 JFE; Macey-O'Hara-Pompilio 2008 JLE; Mitchell-Pulvino 2001 JF; Loughran-McDonald 2011 JF; Shumway 1997 JF (EVREN_SECENEKLERI'nde doğrulanmış). K60 ön kaydından önce künyeleri teyit edilmelidir.
- Proje içi: K56/mekanizma_raporu.py (kaynak boyutları), K57.py (frames etiketleri), islenmis-veri BENIOKU.md, IZ_KARNE Ç103, Ç135, Ç137, Ç139
