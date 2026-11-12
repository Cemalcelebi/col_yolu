# Alpha Vantage ücretsiz pilot (demo anahtarı) — kapsam ve kalite

Tarih: 2026-11-12. Yalnız herkese açık `apikey=demo` ile, belgede yazan örnek adreslerle denendi. Kayıt yok, anahtar yok, e-posta / kişisel bilgi gönderilmedi, SEC'e istek yok. Sinyal testi ve getiri hesabı YOK.
Ham yanıtlar: `/tmp/av_pilot/ham/` (24 yanıt), istek günlüğü `/tmp/av_pilot/istek_gunlugu.tsv`, belge kopyaları `/tmp/av_pilot/belge/` (documentation, premium, support), çapraz denetim `/tmp/av_pilot/capraz/`, haber saati doğrulama sayfaları `/tmp/av_pilot/dogrulama/`. Repoya veri konmadı.

## 0. Kısa sonuç

- **Haber + duyarlılık (NEWS_SENTIMENT) artık ÜCRETLİ.** Belge (12 Kas 2026) ucu "Trending Premium" diye işaretliyor: "this is a premium API function". Demo anahtarı bu ucu yalnız belgedeki iki örnek adres için veriyor. Parametre değişince (limit=1000, time_from 2022, topics) "demo yalnız tanıtım içindir" yanıtı geliyor (4/4 deneme). Ücretsiz anahtar haber geçmişini AÇMAZ. Bu, belgeden çıkan bir sonuç; ücretsiz anahtarla tek istekte doğrulanmalı.
- **Haberin en eski tarihi ölçülemedi.** Demo 2022 / 2018 / 2015 penceresini kabul etmedi. Belgedeki örnek (`time_from=20220410T0130&limit=1000`, COIN + BTC + USD) yalnız 28 haber döndürdü ve en eskisi **2026-07-03**. Yani bu sorguda arşiv 2022'ye uzanmadı. Arşiv mi kısa, yoksa demo yanıtı mı kırpılmış, ayırt edilemedi.
- **Bilanço geçmişi (EARNINGS) iyi kalitede.** IBM için 123 çeyrek var (1996-04 → 2026-10), açıklama saati (öncesi / sonrası) dolu. Yahoo ile 99/99 aynı gün ve aynı EPS, EDGAR 8-K ile 71/71 aynı gün. Ama bu veri zaten elimizdeki Yahoo takvimiyle aynı (aşağıda §3); yeni bilgi getirmiyor.
- **Delist listesi (LISTING_STATUS state=delisted) ücretsiz uç ve tarihli, ama EKSİK.** 2014-07-10 görüntüsünde yalnız **431** kayıt var (425 hisse; delist günü 1997 → 2014-07-09, 2009+ 422). Aynı dönemde EDGAR'da Form 25 / 25-NSE veren tekil CIK sayısı **3.199**; bu bir üst sınır, çünkü borç ve imtiyazlı pay da içinde. Bilinen 10 delistten 4'ü listede (HNZ, NYX, VMED, CVH); 6'sı eksik (DELL, MOLX, BMC, LIFE, LEAP, SFD). OTC yok. **Fiyat da yok:** TIME_SERIES_DAILY tam geçmiş (outputsize=full) artık ücretli, ücretsiz katman yalnız son 100 günü veriyor. Delist listesi Tiingo'nun yerini tutmaz.
- **BIST kapsamı yok.** MARKET_STATUS 16 bölge listeliyor, Türkiye / İstanbul aralarında yok. Belgede `.IST` / `.IS` soneki yok. Haber örneklerinde Türk kaynağı yok (32 kaynak alanı). KAP'la örtüşme yok.
- **Ücretsiz katman günde 25 istek** (premium sayfası ve SSS). 4.700 hisse için tek uç ≈ 188 gün sürer. Ücretli en ucuz paket 49,99 $ / ay (dakikada 75 istek, günlük sınır yok); onunla tek uç ≈ 63 dakika.

## 1. NEWS_SENTIMENT (haber, tarih, duyarlılık)

| ölçü | sonuç |
|---|---|
| demo ile çalıştı mı | Yalnız belgedeki iki adresle çalıştı: `tickers=AAPL` ve belge örneği (ham, virgül / iki nokta kodlanmadan). Değiştirilen 4 sorgu reddedildi. |
| erişim katmanı | **Premium** (belge: "Market News & Sentiment Trending Premium"). |
| alanlar | `title, url, time_published (YYYYMMDDTHHMMSS), authors, summary, banner_image, source, category_within_source, source_domain, topics[{topic, relevance_score}], overall_sentiment_score / label, ticker_sentiment[{ticker, relevance_score, ticker_sentiment_score / label}]`. Üst düzeyde `items` ile skor tanımları var. |
| sayfa | Varsayılan 50 haber; belgeye göre `limit=1000` en çok. Demo 1000'ü yalnız belge örneğinde kabul etti, orada da 28 sonuç döndü. |
| sıralama | Varsayılan LATEST (yeniden eskiye); AAPL yanıtında doğrulandı. Belgeye göre EARLIEST ve RELEVANCE da var (denenemedi). |
| zaman aralığı | AAPL: 50 haber, 2026-11-10 13:41 → 2026-11-12 06:42 UTC (yaklaşık 41 saat). Belge örneği: 28 haber, 2026-07-03 → 2026-11-11. 2022, 2018 ve 2015 pencereleri **denenemedi** (demo reddi). |
| kaynak dağılımı | AAPL: 28 kaynak. İlk sıralar Investing.com Canada 7, Benzinga 6, TradingView 3, BigGo 3, MarketBeat 3, CoinMarketCap 2. Belge örneği: 4 kaynak (Motley Fool 11, Cointelegraph 8, Decrypt 7, Zacks 2). |
| tekrar | URL tekrarı 0/50 ve 0/28. Aynı başlık 0/50 ve 1/28 (iki ayrı URL'de aynı haber). |
| zaman damgası doğruluğu | Kaynak sayfanın `datePublished` değeriyle karşılaştırıldı (4 haber doğrulandı, 1'i doğrulanamadı). Damga **UTC**. Fool 13:35:00Z, Cointelegraph 17:48:35Z ve Decrypt 21:46:03: üçü saniyesine kadar aynı. Macworld'de yayın 13:54:22Z, AV damgası 14:27:43; AV, **33 dakika sonraki** güncelleme saatini (14:27:04Z) almış. Benzinga sayfası 403 verdi: doğrulanamadı. Sonuç: damga çoğunlukla yayın anı, ama bazen güncelleme anı. Gün içi olay çalışmasında ±1 saat pay bırakılmalı. |
| ilgi (relevance) kalitesi | AAPL sorgusunda 50 haberin 26'sının başlığında Apple / AAPL geçmiyor, ama hepsinde AAPL ilgisi ≥ 0,56 (medyan 0,71). İlk haber bir CoinMarketCap "tokenized stock" tanıtım sayfası (ilgi 0,71). İlgi skoru şişkin, haber dışı sayfalar da giriyor. |
| şema tutarlılığı | `topics` alanı AAPL yanıtında kod biçiminde (`technology`), belge örneğinde görünen adla (`Finance`, `Economy - Monetary`) geliyor. Aynı uçta iki biçim var; ayrıştırırken eşleme gerekir. |
| duyarlılık nasıl üretiliyor | Belgede yöntem yok. Yalnız eşikler yazıyor (≤ −0,35 Bearish … ≥ 0,35 Bullish) ve "AI / ML ile üretilir" deniyor (Alpha Intelligence). Kara kutu; model sürümü ve tarihi yok. |
| geriye dönük doldurma / sonradan değişme | Belgede hiçbir şey yazmıyor (sürüm, yeniden skorlama, arşiv başlangıcı yok). Skorların geçmiş haberler için sonradan, bugünkü modelle üretilmiş olma riski açık. Skor "o gün bilinen bilgi" sayılamaz. |
| bilanço günü yoğunluğu | AAPL penceresinde (41 saat) AAPL bilançosu yok, ölçülemedi. Belge örneğinde COIN bilanço günü ve ertesi günü (2026-07-30 ve 10-29, ikisi de 16:00 ET; Yahoo takvimi) 28 haberin 3'ünü topluyor (%10,7). Düzgün dağılımda beklenen yaklaşık %3 (132 günün 4'ü). İki haber bilanço görüşmesi dökümü. n = 3: **bulgu değil**, yalnız yönü tutarlı. |
| kota ve süre (4.700 hisse × 2017-2026) | Ücretsiz katmanda **mümkün değil** (uç premium). Premium'da: arşivin 2017'ye uzandığı varsayılırsa AAPL ≈ 29 haber / gün, yani yaklaşık 105 bin haber ve ~105 istek eder. Küçük hisseler 1-3 istek. Toplam ≈ 10-20 bin istek, dakikada 75 istekle **≈ 2,5-4,5 saat**, yani 1 aylık 49,99 $ paketin içinde kalır. Ücretsiz 25 / gün izin verseydi bile 400-800 gün sürerdi. |

## 2. Bilanço ve olay uçları (demo: yalnız IBM)

| uç | demo | alanlar | tarih aralığı (IBM) | kalite / risk |
|---|---|---|---|---|
| EARNINGS | çalıştı | çeyreklik: `fiscalDateEnding, reportedDate, reportedEPS, estimatedEPS, surprise, surprisePercentage, reportTime`; yıllık EPS | 123 çeyrek, 1996-04-17 → 2026-10-21; 31 yıl | reportTime dolu (102 post / 21 pre); IBM 2014-10-20'yi gerçekte de sabah açıkladı. Tahmin ve sürpriz 123/123 dolu. Sürpriz yuvarlanmış EPS'ten hesaplanıyor: IBM'de 8 çeyrekte AV %0, Yahoo ±%0,04-0,36 veriyor. |
| EARNINGS_ESTIMATES | çalıştı | 18 alan (ortalama / en yüksek / en düşük EPS, analist sayısı, 7 / 30 / 60 / 90 gün önceki ortalama, 7 ve 30 günde yukarı / aşağı revizyon, gelir tahmini) | 42 kayıt: 40 çeyrek + 2 yıl, 2017-06-30 → 2027-12-31 | **Görüntü günü yok** (K63 ile aynı). Kapanmış 38 çeyreğin 27'sinde ortalama, EARNINGS estimatedEPS'e ≤ 0,01 yakın; yani bilanço gününe yakın donmuş görünüyor. 11'inde fark 0,02-0,15. "Aşağı revizyon" alanları %48-57 dolu; boşluk sıfır mı eksik mi, belgede yazmıyor. |
| EARNINGS_CALENDAR | çalıştı | `symbol, name, reportDate, fiscalDateEnding, estimate, currency, timeOfTheDay` (CSV) | yalnız **ileriye**: 3 aylık listede 1.578 hisse, 2026-11-11 → 2027-02-09 (Kas 1.193, Ara 276, Oca 69, Şub 40) | Eksik: IBM'in 2027-01-27 bilançosu (Yahoo'da var) 3 aylık listede yok. `symbol=IBM&horizon=12month` 0 satır döndü. Saat 1.082/1.578 boş. Geçmiş takvim yok. |
| INSIDER_TRANSACTIONS | çalıştı | `transaction_date, ticker, executive, executive_title, security_type, acquisition_or_disposal (A/M/S/F/G/P/I/J), shares, share_price` | 3.685 satır, 2013-05-29 → 2026-09-30 | **Başvuru (SEC kabul) günü yok**, yalnız işlem günü var. Form 4 iki iş günü sonra yayımlanabildiği için geleceğe bakma riski var. Elimizdeki SEC Form 4 (k30, 2022+) bu açıdan üstün. IBM'de açık piyasa alımı (P) yalnız 42 satır. |
| LISTING_STATUS (aktif) | çalıştı | `symbol, name, exchange, assetType, ipoDate, delistingDate, status` (CSV) | bugün 14.523 kayıt: 8.605 hisse, 5.918 ETF; NASDAQ / NYSE / AMEX / BATS / ARCA | OTC yok. k60 evrenimizin (4.757 kod) %84'ü listede, eksik 741 kodun çoğu OTC (CYDY, FNMA, KBLB…). Nasdaq bilanço listesindeki kodların %98'i listede. |
| LISTING_STATUS (delist) | çalıştı (yalnız `date=2014-07-10`) | aynı | 431 kayıt; delist 1997-04 → 2014-07-09 (2009: 39, 2010: 43, 2011: 79, 2012: 55, 2013: 145, 2014 / 6 ay: 61) | **Eksik:** 2009-01 → 2014-07 arasında EDGAR Form 25 / 25-NSE veren tekil CIK 3.199; AV'de 422. Bilinen 10 delistin 4'ü listede. Bugünkü tam delist listesi (`state=delisted`, tarihsiz) demo ile **denenemedi**; ücretsiz anahtarla 1 istekte alınır. |
| DIVIDENDS | çalıştı | `ex_dividend_date, declaration_date, record_date, payment_date, amount` | 112 kayıt, 1999-02 → 2026-11 | Duyuru günü (declaration) yalnız 2020-08 sonrasında dolu (87/112 boş). Yahoo'da zaten var. |
| SPLITS | çalıştı | `effective_date, split_factor` | 2 kayıt (1999, 2021 Kyndryl 1,046) | Yahoo'da zaten var. |
| IPO_CALENDAR | çalıştı | `symbol, name, ipoDate, priceRange, currency, exchange` | yalnız ileriye: 5 kayıt, 2026-11-12 → 11-13 | Geçmiş yok, bu iş için değersiz. |
| OVERVIEW | çalıştı (demo) | 55 alan (sektör, CIK, değerleme, analist dağılımı, hedef fiyat…) | yalnız bugünkü görüntü | Artık **premium**. Tarihçe yok. |
| EARNINGS_CALL_TRANSCRIPT | çalıştı | `symbol, quarter, transcript[{speaker, title, content, sentiment}]` | 2024Q1'de 37 konuşma bölümü; belgeye göre 2010Q1+ | Görüşme tarihi / saati yok; bilanço günüyle eşlemek gerekir. Konuşma başına duyarlılık kara kutu. 4.700 × 67 çeyrek ≈ 315 bin istek: ücretsiz katmanda imkânsız, 75 / dk ile ≈ 70 saat. |
| TIME_SERIES_DAILY | compact çalıştı (100 gün); full yalnız demoda (6.799 gün, 1999-11-01 → 2026-11-11, ham, ABD/Doğu saati) | OHLCV | — | **full artık premium.** Ücretsiz katman yalnız son 100 gün; tarihsel fiyat için kullanılamaz. |
| SYMBOL_SEARCH / MARKET_STATUS | çalıştı (tesco, BA) | — | — | Bölgeler: ABD, Kanada, İngiltere, Almanya, Fransa, İspanya, Portekiz, Japonya, Hindistan, Çin, Hong Kong, Brezilya, Meksika, Güney Afrika. **Türkiye yok.** |

Önemli uyarı: demo anahtarı premium uçları (NEWS_SENTIMENT, OVERVIEW, TIME_SERIES_DAILY full) da veriyor. Bu yüzden "demo ile çalıştı" demek "ücretsiz anahtarla çalışır" demek değildir; erişim katmanı belgeden okundu.

## 3. Kendi verimizle çapraz denetim (IBM; AAPL bilançosu demo dışı)

Dosya: `/tmp/av_pilot/capraz/ibm_av_yahoo_nasdaq_edgar.csv`. Kaynaklar: AV EARNINGS ↔ Yahoo takvimi (`/tmp/k67_yahoo/takvim/IBM.html.gz`, K67 ayrıştırıcısıyla) ↔ Nasdaq takvimi (`/tmp/pead/liste_abd.csv.gz`) ↔ EDGAR ana dizin (`/tmp/k60_secframes/edgar_master_*`, 2009Q1-2026Q3, yerel).

| karşılaştırma | sonuç |
|---|---|
| AV reportedDate ↔ Yahoo günü | 99 eşleşme, **99/99 aynı gün** (Yahoo 100 satırla sınırlı, 2002+; 2009+ 72/72) |
| AV ↔ Nasdaq günü (2022-12 → 2026-10) | 16/16 aynı gün |
| AV ↔ EDGAR 8-K (±3 gün içinde en yakın) | 2009+ **71/71 aynı gün**; eşleşmeyen tek kayıt 2026-10-21, çünkü EDGAR dizinimiz 2026Q3'te bitiyor |
| AV bilanço günü → 10-Q / 10-K başvurusu | n = 71, gecikme medyanı 8 gün (en az 1, en çok 40). 10-Q günü bilanço gününün **vekili olarak kötü**; 8-K günü iyi vekil. |
| reportedEPS = Yahoo gerçekleşen | 99/99 (±0,01) |
| estimatedEPS = Yahoo tahmin | 98/99 |
| sürpriz % (AV − Yahoo) | medyan −0,006 puan; 1 puandan büyük fark 0/99. İşaret 91/99 aynı; ayrışan 8'in hepsi AV %0 / Yahoo küçük sapma (yuvarlama). |
| sürpriz % (AV − Nasdaq) | 15 eşleşme: 5'i aynı, fark −1,39 … +2,59 puan. Nasdaq başka bir konsensüs kullanıyor. |
| açıklama saati (AV reportTime ↔ Yahoo saat) | 99/99 uyumlu: 16:00 ve 15 / 17 → post-market (96), 07:00 → pre-market (3) |
| AV haberi ↔ bilanço günü | AAPL penceresinde bilanço yok, ölçülemedi. COIN: §1'deki 3/28. |

Sonuç: AV EARNINGS ile Yahoo takvimi **aynı veri** (aynı tahmin kaynağı). AV'nin artısı 1996'ya kadar inmesi ve Yahoo'daki 100 satır sınırının olmaması. Nasdaq takviminden farkı, açıklama saatinin dolu olması (Nasdaq'ta %99 boş). Yahoo takvimi (K67 indirme kodu var, ücretsiz) 1.410'dan 4.700 hisseye genişletilirse aynı bilgi AV'siz elde edilir.

## 4. BIST / KAP örtüşmesi

- AV'de BIST yok: MARKET_STATUS 16 bölgede Türkiye yok; belgedeki sonek örnekleri `.LON .TRT .TRV .DEX .BSE .SHH .SHZ` ve `.IST` / `.IS` yok. Haber örneklerinde Türk kaynağı yok. SYMBOL_SEARCH ile BIST kodu (THYAO vb.) aramak demo ile **denenemedi; ücretsiz anahtarla denenmeli** (3 istek). Beklenti: sonuç gelmez.
- KAP verimiz: Finansal Rapor 2009-06+ (K62, 106.852 kayıt, yayın saatli), içeriden işlem 2022-07+ (6.637 bildirim) ve pead BIST listeleri. AV bunların hiçbirine karşılık vermez. **KAP özel durum açıklamaları (ÖDA: sözleşme, ihale, ortaklık, dava…) eksiği AV ile kapanmaz.** VDYT'de BIST "habersiz" grubu kirli kalır.
- Örtüşme özeti: BIST bilanço günü = KAP (var, AV gereksiz). BIST haber / duyarlılık: AV'de yok, KAP ÖDA'da da yok. BIST delist: K62 İş Yatırım (92 çıkmış hisse), AV'de yok.

## 5. Sonuç tablosu

| uç | demo | alanlar | tarih (ilk-son) | kalite / risk | ücretsiz anahtarla 4.700 hisse | VDYT katkısı | öneri |
|---|---|---|---|---|---|---|---|
| NEWS_SENTIMENT | yalnız 2 belge örneği | haber, UTC saat, kaynak, konu, genel ve hisse duyarlılığı, ilgi | demo: 2026-07-03 → 2026-11-12; geçmiş ölçülemedi | premium; ilgi şişkin (26/50 başlık konu dışı); skor kara kutu, sonradan üretilmiş olabilir; damga 3/4 tam, 1/4 +33 dk | **imkânsız** (premium). Ücretli: ≈ 10-20 bin istek, ≈ 3-5 saat | K1 haberli / habersiz (ABD), E1 / E2 pencerelerinde haber sayısı | **ücretli gerekli.** Önce 1 ay 49,99 $ ile arşivin başlangıcı ölçülmeli; 2022 öncesine inmiyorsa VDYT dönemini kapsamaz. Karar Cemal'de. |
| EARNINGS | çalıştı | gün, saat (pre / post), EPS, tahmin, sürpriz | 1996 → 2026 | Yahoo ile birebir; EDGAR 8-K ile aynı gün | 4.700 istek = **188 gün** | bilanço sürprizi, A planlı olay saati | **gereksiz.** Aynı veri Yahoo takviminden ücretsiz gelir (K67 kodu); yalnız Yahoo'da olmayan hisseler için tamamlayıcı. |
| EARNINGS_ESTIMATES | çalıştı | konsensüs, revizyon, analist sayısı | 2017-06 → 2027-12 | görüntü günü yok; 27/38 çeyrek bilanço gününe yakın donmuş | 188 gün | revizyon (K67'de VERİ YOK idi) | ücretsiz anahtarla **25 hisselik pilot** (1 gün); tam set için ücretli 1 ay (≈ 63 dk) |
| EARNINGS_CALENDAR | çalıştı | ileriye takvim | yalnız +3 / 6 / 12 ay | eksik (IBM yok; 12 ay sorgusu boş) | 1 istek | yok (geçmiş yok) | gereksiz |
| INSIDER_TRANSACTIONS | çalıştı | işlem günü, kişi, kod, adet, fiyat | 2013-05 → 2026-09 | başvuru günü yok, geleceğe bakma riski | 188 gün | B olay (ABD içeriden) | gereksiz: SEC Form 4 (k30) daha iyi; 2013-2021 gerekirse SEC'ten ücretsiz |
| LISTING_STATUS delisted | çalıştı (yalnız 2014-07-10 görüntüsü) | kod, ad, borsa, IPO günü, delist günü | 1997 → bugün | eksik (2009-14: 422 vs EDGAR 3.199 CIK üst sınır; bilinen 4/10); OTC yok; **fiyat yok** | 1 istek (bugünkü tam liste) + yıllık görüntüler 17 istek | delist listesi (yaşayan yanlılığı ölçüsü) | **ücretsiz anahtarla al** (1-18 istek, 1 gün). Ama Tiingo'nun yerini tutmaz (fiyat yok, liste eksik). |
| LISTING_STATUS aktif (tarihli) | çalıştı | aynı | 2010 → bugün | OTC yok | yıllık 17 istek | zamanı geldiğinde evren (point-in-time) | ücretsiz anahtarla al (delistle birlikte) |
| DIVIDENDS / SPLITS | çalıştı | ex / duyuru / ödeme günü, oran | 1999 → 2026 | duyuru günü 2020-08 sonrası | 9.400 istek = 376 gün | A planlı olay (duyuru günü) | gereksiz (Yahoo var); duyuru günü yalnız 2020+ |
| EARNINGS_CALL_TRANSCRIPT | çalıştı | konuşma metni, konuşma başına duyarlılık | 2010Q1+ (belge) | tarih yok; skor kara kutu | ≈ 315 bin istek, imkânsız | (ileride metin analizi) | şimdilik gereksiz |
| TIME_SERIES_DAILY | compact çalıştı | OHLCV | ücretsiz: son 100 gün | full premium | — | yok | gereksiz (Yahoo / k60 var) |
| OVERVIEW / IPO_CALENDAR | çalıştı | bugünkü görüntü / ileri IPO | bugün | premium / geçmiş yok | — | yok | gereksiz |
| BIST (herhangi bir uç) | denenemedi | — | — | MARKET_STATUS'ta Türkiye yok | 3 istek (doğrulama) | — | gereksiz (kapsam yok) |

## 6. Ücretsiz anahtarla tam pilot (önerilirse)

Toplam yaklaşık 45 istek, ücretsiz katmanda 2 gün (günde 25 istek; istekler arası ≥ 15 sn):
- Gün 1 (25): NEWS_SENTIMENT AAPL (1: premium kapısını doğrula; kabul ederse 2018-01 penceresi +1). LISTING_STATUS state=delisted, bugünkü tam liste (1; kaç ABD hissesi, hangi yıllar). LISTING_STATUS aktif, 2010-2026 her 2 Ocak (17). SYMBOL_SEARCH THYAO / ASELSAN / Turkcell (3). TIME_SERIES_DAILY THYAO.IST ve THYAO.IS (2).
- Gün 2 (~20): EARNINGS 5 delist hisse (AV batan şirketin geçmişini tutuyor mu?). TIME_SERIES_DAILY 1 delist hisse (batan şirket fiyatı var mı?). EARNINGS_ESTIMATES 5 hisse (Yahoo eps_tahmin ile görüntü günü sınaması). EARNINGS AAPL + 5 küçük hisse (Yahoo / EDGAR ile gün ve saat uyumu).
- Tam veri: tek uç × 4.700 hisse = 188 gün (ücretsiz). Haber premium olduğu için ücretsiz katmanda hiç yapılamaz. Ücretli 1 ay (49,99 $, dakikada 75 istek) EARNINGS + ESTIMATES + NEWS'ü yaklaşık 5-7 saatte indirir. Bu ücret ve abonelik kararı Cemal'in.

## 7. Cemal'e not: ücretsiz anahtar

- Anahtarı yalnız sen alırsın: alphavantage.co/support/#api-key sayfasındaki formu kendi bilginle doldur (Claude kayıt yapmaz, anahtar istemez). Anahtar ücretsizdir; günde 25 istek verir. Haber / duyarlılık bu anahtarla AÇILMAZ (belgeye göre premium).
- Anahtarı reponun kökündeki `.env` dosyasına (git dışında) şu adla tek satır yaz: `ALPHAVANTAGE_API_KEY=...`. Colab'da Drive `col_tarayici/.env`.
- Kod anahtarı yalnız ortam değişkeninden okur (`os.environ["ALPHAVANTAGE_API_KEY"]`, yoksa `.env`'den yükler). Anahtar koda, rapora, günlüğe ve repoya asla yazılmaz; istek günlüğünde `apikey` alanı silinir.
- Anahtar konunca §6'daki 2 günlük pilot koşulur. Sonuç: haber uçu kapalı mı, delist listesi kaç hisse, AV batan şirket fiyatı veriyor mu, BIST var mı.

## 8. Kaynaklar

- alphavantage.co/documentation (indirildi 2026-11-12 08:03 UTC; NEWS_SENTIMENT, OVERVIEW, TIME_SERIES_DAILY full ve DAILY_ADJUSTED "premium"; LISTING_STATUS "date > 2010-01-01 desteklenir")
- alphavantage.co/premium (ücretsiz 25 istek / gün; aylık 49,99 / 99,99 / 149,99 / 199,99 / 249,99 $; yıllık 499-2.499 $)
- alphavantage.co/support (SSS: ücretsiz 25 istek / gün; doğrulanmış açık kaynak / eğitim projelerine sınırsız)
- Haber saati doğrulaması: fool.com, cointelegraph.com, decrypt.co, macworld.com sayfa meta verisi (`datePublished`, `dateModified`); benzinga.com 403.
