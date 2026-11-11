# K63 — VERİ ERİŞİM ARAŞTIRMASI: analist revizyonu, emir akışı, hisse ödünç

Erişim tarihi (bütün URL'ler için): 2026-11-11. Sinyal testi ve getiri hesabı YOK; yalnız "hangi veri nerede, ne kadar geriye, kaça" sorusu.
Örnek dosyalar: /tmp/k63_ornek (32 MB; repoya konmadı). Servislere kayıt olunmadı, anahtar / e-posta gönderilmedi, SEC'e istek atılmadı.

Güven etiketleri: **[DENENDİ]** = uç nokta bu oturumda çağrıldı, dönen dosya okundu. **[LİSTE]** = sağlayıcının kendi sayfasından okunan liste fiyatı / belge. **[İKİNCİL]** = üçüncü taraf site, forum ya da arama özeti. **[GENEL]** = yaygın bilinen, bu çalışmada doğrulanmadı. **[BULUNAMADI]** = arandı, kanıt yok.

---

## 1. Özet (bir sayfa)

| Aile | Pazar | Ücretsiz tarihsel veri | En iyi ücretsiz kaynak | En ucuz uygulanabilir ücretli yol |
|---|---|---|---|---|
| A. Analist revizyonu | ABD | **KISMEN** | (1) Yahoo not günlüğü: tavsiye + hedef fiyat değişikliği, 2011-12'den beri, K52'de zaten çekildi (310.568 kayıt). (2) Alpha Vantage EARNINGS_ESTIMATES: her mali çeyrek / yıl için donmuş konsensüs EPS (ortalama, en yüksek, en düşük, analist sayısı, 7/30/60/90 gün önceki ortalama, 7 ve 30 günde yukarı / aşağı revizyon sayısı), 2017-06'dan beri [DENENDİ, demo anahtar, IBM] | Alpha Vantage 49,99 $/ay, tek ay (ücretsiz katman günde 25 istek: 4.700 hisse = 188 gün). Analist bazında tarih damgalı tam seri (I/B/E/S) kurumsal, fiyat yayımlanmıyor |
| A. Analist revizyonu | BIST | **YOK** | Yalnız güncel anlık görüntü: İş Yatırım takip listesi, 54 hisse (öneri, hedef fiyat, öneri tarihi) [DENENDİ]. Tarihsel seri ücretsiz yok | EODHD 59,99 $/ay: BIST için Earnings Trend alanının dolu olduğu DOĞRULANAMADI. Ayrıca yapısal sınır: aracı kurum kapsamı ~50-100 büyük hisse; çöl evreninin (küçük hisseler) çoğunda analist yok |
| B. Emir akışı | ABD | **KISMEN** | IEX HIST: TOPS 2016-12-12'den, DEEP 2017-05-15'ten bugüne ücretsiz pcap [DENENDİ]; ama yalnız IEX borsası ve toplam ~20 TB. FINRA Reg SHO günlük açığa satış hacmi 2009-08'den [DENENDİ] (emir akışı değil) | Alpaca ücretsiz hesap: 2016'dan beri tarihsel işlem + kotasyon, son 15 dakika hariç, 200 istek/dk [LİSTE; hesap gerektirir, denenmedi]. Ücretli: Massive (eski Polygon) Developer 79 $/ay (işlemler, 10 yıl), Advanced 199 $/ay (kotasyon, 20+ yıl); Databento kullanım bazlı, 125 $ ücretsiz kredi |
| B. Emir akışı | BIST | **YOK** | Günlük bülten (VWAP, sözleşme sayısı, açılış / kapanış seansı hacmi, açığa satış) 2015-12'den CSV [DENENDİ]; kademe / işlem bazında veri değil | Borsa İstanbul DataStore emir / işlem defteri: fiyat sayfası 503 verdi, fiyat DOĞRULANAMADI |
| C. Hisse ödünç | ABD | **KISMEN** | FINRA açık pozisyon (short interest) 2017-12-29'dan, iki haftada bir, borsa + OTC [DENENDİ]; Reg SHO günlük 2009-08'den [DENENDİ]; SEC teslim edilmeyenler (FTD) 2004'ten [İKİNCİL, istek atılmadı]. Ödünç ücreti / ödünç alınabilir adet / kullanım oranı: ücretsiz tarihsel YOK | IBorrowDesk API 29 $/ay (5.000 birim; 1 birim = 1 hisse × 365 gün; IBKR ücret, iade, kullanılabilir adet, 2015-07-13'ten günlük) [DENENDİ: /coverage]. Kullanım oranı (utilization) yalnız kurumsal kaynaklarda (S&P / DataLend / FIS) ya da ORTEX tahmini (49-149 $/ay) |
| C. Hisse ödünç | BIST | **KISMEN** | Takasbank ÖPP günlük bülten 26.02.2008'den: kıymet bazında en düşük / en yüksek / ortalama oran, adet, piyasa değeri, sözleşme sayısı; Excel dışa aktarım [DENENDİ]. Günlük bültende açığa satış hacmi [DENENDİ] | Ücretli seçenek gerekmiyor; sınır veride: açığa satış 2020'den beri yalnız BIST-30/50'de, Şubat 2023 - Aralık 2024 ve 2025-2026'nın bazı aylarında tamamen sıfır; ÖPP günde 35-90 kıymet |

En önemli üç sonuç:
1. ABD'de **açığa satış pozisyonu ve günlük açığa satış hacmi** bugün, ücretsiz, anahtarsız ölçülebilir (2017-12 / 2018-08 sonrası).
2. ABD'de **EPS revizyonu** için ilk kez ücretsiz bir tarihsel kaynak bulundu (Alpha Vantage / EODHD çeyreklik donmuş görüntü, 2017-06+), ama görüntünün alındığı gün dosyada yazmıyor: sızıntı riski ayrıca sınanmalı.
3. BIST'te üç ailenin hiçbiri çöl evreni (küçük hisseler) için kullanılabilir tarihsel veri vermiyor: analist kapsamı yok, kademe verisi ücretli / belirsiz, açığa satış 2020'den beri küçük hisselerde yasak.

---

## 2. Sağlayıcı tabloları

### 2A. Analist revizyonları

| Sağlayıcı | BIST | Tarihsel derinlik / nokta-zaman | Alanlar | Fiyat | Erişim, kısıt | Güven |
|---|---|---|---|---|---|---|
| I/B/E/S (LSEG; WRDS üzerinden) | var (küresel) | ABD 1976+, dünya 1987+; analist bazında günlük kayıt (Detail History) = gerçek nokta-zaman | analist bazında EPS / gelir tahmini, konsensüs, dağılım, tavsiye, hedef fiyat | yayımlanmıyor; WRDS yalnız kurum / üniversite | toplu dosya; bireysel erişim yok | [İKİNCİL] lseg.com/en/data-catalogue/company-data/ibes-estimates ; BIST kapsamı [GENEL] |
| FactSet, Bloomberg, S&P Capital IQ, Visible Alpha | var | nokta-zaman konsensüs | tam set | yayımlanmıyor; kurumsal | terminal / veri akışı | [GENEL]; fiyat [BULUNAMADI] |
| Zacks (Nasdaq Data Link) | yok | tarihsel konsensüs veri setleri var | EPS tahmini, sürpriz, tavsiye | [BULUNAMADI] | toplu dosya / API | [BULUNAMADI] |
| Estimize | yok | kitle kaynaklı tahmin | EPS / gelir | [BULUNAMADI] | araştırılamadı | [BULUNAMADI] |
| Yahoo Finance `upgradeDowngradeHistory` | BIST için denenemedi (bugün 429) | ABD: 2011-12-08'den olay günlüğü (K52: 310.568 kayıt, yılda ~2.200 hisse) | kurum, eski / yeni tavsiye, eski / yeni hedef fiyat, tarih-saat | ücretsiz | resmî olmayan uç; geriye dönük yeniden yazım doğrulanamaz | repo: arastirma_cikti/col_yolu_abd/K51_ANALIST_TARIHSEL_VERI_DENETIMI.md |
| Yahoo `earningsTrend` / `epsRevisions` | denenemedi | yalnız güncel anlık görüntü (şimdi, 7/30/60/90 gün önce); tarih serisi yok | EPS ortalama / alt / üst, analist sayısı, yukarı / aşağı revizyon sayısı | ücretsiz | bu oturumda `getcrumb` 429 "Too Many Requests" döndü; iki kez denendi | [DENENDİ: 429] |
| Alpha Vantage `EARNINGS_ESTIMATES` | [BULUNAMADI] (demo anahtar yalnız IBM) | 2017-06-30'dan beri her mali çeyrek ve yıl için bir donmuş görüntü; görüntü günü yazmıyor | aşağıda 3.1 | ücretsiz 25 istek/gün; 49,99 $/ay 75 istek/dk | API (JSON); belge "premium" demiyor | [DENENDİ] + [LİSTE] alphavantage.co/documentation , /premium |
| EODHD `fundamentals` → `Earnings::Trend` | Istanbul borsası listede; Trend alanının BIST'te dolu olduğu [BULUNAMADI] | AAPL için 2017-06-30'dan 42 dönem; AV ile aynı alan yapısı (aynı kaynak olması muhtemel) | 3.1 | Fundamentals 59,99 $/ay; All-in-one 99,99 $/ay; ücretsiz 20 çağrı/gün (temel veri 10 çağrı sayılır) | API; toplu uç ayrı | [DENENDİ, demo: AAPL] + [LİSTE] eodhd.com/pricing |
| EODHD `AnalystRatings` | ? | yalnız güncel (Rating, TargetPrice, StrongBuy…StrongSell sayıları) | 7 alan | aynı | | [DENENDİ] |
| Finnhub | yok / belirsiz | fiyat sayfası JS ile yükleniyor, okunamadı; ücretsiz katmanda tavsiye eğilimi ve son 4 çeyrek sürpriz olduğu ikincil kaynakta; EPS tahmini / hedef fiyat / not değişikliği ücretli plan | recommendation, price-target, upgrade-downgrade, eps-estimate | [BULUNAMADI] | API, anahtar şart | [İKİNCİL] nexusfi.com/d/data-providers/finnhub |
| Financial Modeling Prep | üst planda küresel | analist tahmini, hedef fiyat, tarihsel not (grades) uçları var; derinlik doğrulanamadı | | plan fiyatları okunamadı (sayfa 403); ücretsiz 250 çağrı/gün [İKİNCİL] | `apikey=demo` 401 döndü [DENENDİ] | [İKİNCİL] |
| Massive (eski Polygon) + Benzinga analist notları | yok | 2012'den beri (bir yerde "13+ yıl") | not değişikliği, hedef fiyat, kurum | 99 $/ay, bireysel kullanım | API | [LİSTE] massive.com/pricing ; massive.com/docs/rest/partners/benzinga/analyst-ratings |
| Benzinga (doğrudan) | yok | | | [BULUNAMADI] | | |
| Tiingo, Nasdaq Data Link (Zacks dışı) | yok | analist tahmini ürünü bulunamadı | | | | [BULUNAMADI] |
| MarketBeat, TipRanks, Seeking Alpha, Koyfin | TipRanks'te TR hisse sayfaları var | tüketici siteleri; yapılandırılmış tarihsel indirme [BULUNAMADI] | | abonelik | ekran; toplu indirme lisansa aykırı olabilir | [BULUNAMADI] |
| İş Yatırım takip listesi | 54 hisse | yalnız güncel; arşiv (Wayback) bu oturumda denenemedi (bağlantı kesildi) | Kod, Öneri, Hedef Fiyat, Getiri Potansiyeli, Öneri Tarihi, Kapanış, Piyasa Değeri | ücretsiz | HTML tablo | [DENENDİ] isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/takip-listesi.aspx |
| Fintables | var | hedef fiyat / tahmin içeriği ve geçmişi doğrulanamadı (sayfa 403) | | Trade 149 TL/ay, Fon 299 TL/ay | ekran | [İKİNCİL] fintables.com/abone-ol |
| Matriks | var | tarihsel analist verisi [BULUNAMADI] | | Gold terminal 515 TL, PC IQ 980 TL, Veri Analitikleri 300 TL+KDV, MKK takas 65 TL+KDV (aylık, aracı kurum listesi) | terminal | [İKİNCİL] infoyatirim.com/hakkimizda/ucretler |
| Foreks, Finnet, Rasyonet, Investing.com, Bloomberg HT | var | [BULUNAMADI] | | | | [BULUNAMADI] |
| KAP | analist verisi yok | KAP şirket bildirimi platformudur; analist tahmini yayımlamaz (Takasbank ÖPP bültenleri KAP'ta da çıkıyor) | | ücretsiz | | [GENEL] |
| Borsa İstanbul DataStore | analist verisi yok | borsa verisi satar | | | | [GENEL] |

### 2B. Emir akışı

| Sağlayıcı | Alanlar | Tarihsel derinlik | Boyut | Fiyat | Bireysel erişim | Güven |
|---|---|---|---|---|---|---|
| IEX HIST (TOPS, DEEP, DPLS, DPLC) | TOPS: IEX en iyi alış / satış + işlemler. DEEP: IEX fiyat kademesi derinliği + işlemler. Ham pcap | TOPS 2016-12-12, DEEP 2017-05-15, DPLS 2024-10-01, DPLC 2026-08-07; son gün 2026-11-10 | DEEP toplam 9,9 TB; 2019'da 266 GB/yıl, 2022'de 1.162 GB, 2026'da (217 gün) 2.762 GB; günlük 0,7-13 GB | ücretsiz | evet; ama yalnız IEX borsasındaki emirler (toplam hacmin küçük bir bölümü) | [DENENDİ] iextrading.com/api/1.0/hist |
| Alpaca Market Data | işlemler, kotasyonlar (en iyi alış / satış + büyüklük), barlar | 2016'dan | API sayfalama | Basic ücretsiz (200 istek/dk, "son 15 dakika" kısıtı, gerçek zamanlı yalnız IEX); Algo Trader Plus 99 $/ay (10.000 istek/dk) | evet, hesap gerekir; denenmedi | [LİSTE] docs.alpaca.markets/docs/about-market-data-api |
| Massive (eski Polygon) | işlemler, kotasyonlar (NBBO), düz dosyalar | Starter 5 yıl; Developer 10 yıl + işlemler; Advanced 20+ yıl + kotasyon | | 29 / 79 / 199 $/ay | evet | Advanced [LİSTE]; diğerleri [İKİNCİL] apicostcalc.com/blog/polygon-massive-rebrand-api-pricing.html |
| Databento (Nasdaq TotalView-ITCH ve diğerleri) | emir bazında (MBO), 10 kademe (MBP-10), en iyi kademe, işlemler, kapanış dengesizliği | ITCH 2018-05-01'den [İKİNCİL, 2022 duyurusu] | boyuta göre faturalanır | kullanım bazlı; 125 $ ücretsiz kredi; Standard 199 $/ay (L1 1 yıl, L2/L3 1 ay); GB fiyatı doğrulanamadı (2022'de 0,45 $/GB'den başlıyordu) | evet | [LİSTE] databento.com/pricing ; GB fiyatı [İKİNCİL] |
| NYSE TAQ (WRDS) | bütün ABD işlemleri + kotasyonları | 1993+ | TB | kurumsal | hayır | [GENEL] |
| LOBSTER | Nasdaq emir defteri yeniden kurulumu | [BULUNAMADI] | | [BULUNAMADI]; akademik topluluğa hizmet veriyor | belirsiz | [İKİNCİL] |
| Kibot / FirstRate Data / Algoseek | tik işlem + kotasyon | FirstRate 2010'dan | | Kibot 45-145 $/sembol; FirstRate kaynaklar çelişkili (15-50 $ / 300-400 $); Algoseek 5.000 $+/yıl | evet (Algoseek hariç) | [İKİNCİL] |
| Tiingo IEX | | | | | | [BULUNAMADI] (araştırılamadı) |
| FINRA Reg SHO günlük | Date, Symbol, ShortVolume, ShortExemptVolume, TotalVolume, Market | borsa bazlı dosyalar (FNSQ, FNYX, FORF) 2009-08-03'ten; birleşik CNMS 2018-08-01'den | gün başına 0,25-0,55 MB | ücretsiz | evet | [DENENDİ] cdn.finra.org/equity/regsho/daily/ |
| SEC MIDAS | borsa bazında iptal / işlem oranları; "Metrics by Individual Security" 4.800+ menkul | 2012 Ç1 - 2025 Ç3 | | ücretsiz | evet; alan ayrıntısı doğrulanmadı (SEC'e istek atılmadı) | [İKİNCİL] sec.gov/data-research/sec-markets-data/marketstructuredata-exchange |
| Borsa İstanbul DataStore (emir / işlem defteri, BISTECH ITCH) | emir bazında veri | [BULUNAMADI] | | arama özeti: "Intraday Order Book Information 150 TL / ay / pazar" (akademik olmayan liste); sayfa 503 verdi, DOĞRULANAMADI; ITCH için "Borsa ile iletişime geçin" | belirsiz; akademik dilekçe örneği var | [İKİNCİL] borsaistanbul.com/sayfa/2816 |
| Matriks / Foreks derinlik | canlı derinlik | tarihsel indirme [BULUNAMADI] | | terminal aboneliği | | [BULUNAMADI] |
| AKD (aracı kurum dağılımı), takas | günlük, aracı kurum bazında | tarihsel ücretsiz kaynak [BULUNAMADI] | | Fintables: "MKK Verileri" lisansı ister; Matriks MKK takas 65 TL+KDV/ay | lisanslı | [İKİNCİL] fintables.com/araci-kurumlar/KVY/takas-analizi |
| MKK Veri Analiz Platformu (VAP) | yabancı sahiplik oranı vb. 225 metrik | hisse bazında geçmiş serinin ücretsiz olduğu doğrulanamadı | | | | [İKİNCİL] |
| Borsa İstanbul günlük bülten (thb) | 3.4'e bak | 2005'ten dosya var; CSV biçimi 2015-12-01'den | gün başına 0,05-0,33 MB zip | ücretsiz | evet | [DENENDİ] |

### 2C. Hisse ödünç

| Sağlayıcı | Alanlar | Tarihsel derinlik | Fiyat | Erişim | Güven |
|---|---|---|---|---|---|
| S&P Global Securities Finance (Markit), FIS Astec, DataLend (EquiLend), S3 Partners | ödünç ücreti, kullanım oranı, ödünç verilebilir stok, ödünçteki miktar | 2000'lerden | yayımlanmıyor; kurumsal | veri akışı | [GENEL]; fiyat [BULUNAMADI] |
| ORTEX | tahmini açığa satış, ödünç maliyeti, kullanım oranı (kendi modeli, resmî kayıt değil) | [BULUNAMADI] | Basic 49 $/ay, Advanced 149 $/ay; API / toplu veri fiyatı yok | ekran, Excel eklentisi, API | [İKİNCİL] public.ortex.com |
| Fintel | açığa satış geçmişi (ücretsiz), ödünç oranı (ücretli) | [BULUNAMADI] | 50-250 $/ay bandı | ekran / API | [İKİNCİL] lambdafin.com/articles/best-short-interest-tracking-tools-2026 |
| Interactive Brokers shortstock FTP | ödünç ücreti, iade, kullanılabilir adet (anlık dosya; arşiv tutmaz) | yok (yalnız o an) | ücretsiz | FTP (kullanıcı adı shortstock); bu ortamdan FTP bağlantısı kurulamadı | [DENENDİ: bağlanamadı] ibkb.interactivebrokers.com/article/2024 |
| IBorrowDesk (IBKR arşivi) | günlük ücret, iade, kullanılabilir adet (açılış / en yüksek / en düşük / kapanış); 15 dakikalık okumalar | günlük 2015-07-13'ten; 15 dakikalık 2026-07-17'den | API planı 29 $/ay, 5.000 birim dahil; 1 birim = 1 hisse × 365 gün; ek birim paketi fiyatı okunamadı | API (anahtar); site içi uçlar otomatik istemciyi 403 ile reddediyor | [DENENDİ] iborrowdesk.com/api/v2/coverage ; iborrowdesk.com/llms.txt |
| QuantConnect "US Equities Short Availability" | ödünç alınabilir adet, ücret oranı, iade oranı (IBKR sağlayıcısı) | 2018-01'den, 10.500 hisse, günlük | sayfada yazmıyor | QuantConnect içinde | [LİSTE] quantconnect.com/docs/v2/writing-algorithms/datasets/quantconnect/us-equities-short-availability |
| GitHub / Kaggle IBKR arşivleri | | | | açık arşiv [BULUNAMADI]; EliteTrader'da 2017'den beri 15 dakikalık özel arşiv teklifi var (kişisel satış) | [İKİNCİL] |
| FINRA açık pozisyon (short interest) | 3.2'ye bak | 2017-12-29'dan (daha eski dosyalar 403) | ücretsiz | CDN dosyası + anahtarsız API | [DENENDİ] |
| Nasdaq / NYSE açık pozisyon sayfaları | | | | api.nasdaq.com isteği HTTP/2 hatasıyla kesildi; doğrulanamadı | [DENENDİ: hata] |
| FINRA Reg SHO günlük | 2B'ye bak | 2009-08 / 2018-08 | ücretsiz | | [DENENDİ] |
| SEC teslim edilmeyenler (FTD) | ödeme tarihi, CUSIP, sembol, bakiye adedi, ad, fiyat (boru ayraçlı metin) | Şubat 2004'ten; Temmuz 2009'dan beri ayda iki dosya; 16.09.2008'den beri eşiksiz | ücretsiz | dosya; SEC iletişimli User-Agent ister, istek atılmadı | [İKİNCİL] sec.gov/data/foiadocsfailsdatahtm |
| WRDS (Markit Securities Finance eklentisi) | | | kurumsal | | [GENEL] |
| Takasbank ÖPP günlük bülten | 3.5'e bak | 26.02.2008'den | ücretsiz | web formu + Excel dışa aktarım | [DENENDİ] |
| Takasbank ÖPP açık işlemler | Kıymet Kodu, Kıymet Grubu, Vade, Vade Türü, Adet, Piyasa Değeri | tarih aralığı formu; en eski tarih denenmedi | ücretsiz | web formu + Excel | [DENENDİ, 10.11.2026] |
| Borsa İstanbul açığa satış (haftalık `acigasat.zip`) | İşlem Kodu, Enstrüman Tipi, Pazar, İşlem Hacmi (TL), İşlem Miktarı, En Düşük / En Yüksek Fiyat | yalnız son hafta (02-06.11.2026: 50 hisse) | ücretsiz | zip / xlsx | [DENENDİ] |
| Borsa İstanbul günlük bülten içindeki açığa satış | 3.4'e bak | 2015-12-01'den CSV | ücretsiz | | [DENENDİ] |

---

## 3. Gerçekten denenen uç noktalar

### 3.1 Analist tahmini (demo anahtarlar; kayıt yok)
- `https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo` → 200, 42 kayıt (40 çeyrek + 2 yıl), dönem sonu tarihleri 2017-06-30 … 2027-12-31. Alanlar: date, horizon, eps_estimate_average / high / low / analyst_count, eps_estimate_average_7 / 30 / 60 / 90_days_ago, eps_estimate_revision_up / down_trailing_7_days, _30_days, revenue_estimate_average / high / low / analyst_count. 90 gün önceki ortalama 42 kayıtta da dolu; "aşağı revizyon" alanları %45-60 dolu (boş = sıfır olabilir, belgede yazmıyor).
  - Örnek: IBM 2020-03-31 çeyreği → ortalama 1,79; 7 gün önce 1,84; 30 gün önce 1,94; 90 gün önce 2,15; analist 11. Yani görüntü bilanço açıklamasından hemen önce donmuş görünüyor (tek örnek; görüntü günü dosyada YOK).
- `https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&filter=Earnings::Trend` → 200, 42 dönem, 2017-06-30 … 2028-09-30. Alanlar: period (0q, +1q, 0y, +1y), growth, earningsEstimateAvg / Low / High / YearAgoEps / NumberOfAnalysts / Growth, revenueEstimate…, epsTrendCurrent / 7 / 30 / 60 / 90daysAgo, epsRevisionsUpLast7days / 30days, epsRevisionsDownLast7days / 30days.
- `…filter=AnalystRatings` → yalnız güncel: Rating, TargetPrice, StrongBuy, Buy, Hold, Sell, StrongSell.
- `https://financialmodelingprep.com/stable/analyst-estimates?symbol=AAPL&apikey=demo` → 401 "Invalid API KEY".
- Yahoo `query1.finance.yahoo.com/v1/test/getcrumb` → "Too Many Requests" (iki ayrı denemede). quoteSummary (AAPL, THYAO.IS) bu yüzden çağrılamadı. Farklı tarayıcı kimliğiyle yeniden deneme izin sistemi tarafından engellendi; zorlanmadı. BIST hissesi için Yahoo analist modüllerinin ne döndürdüğü bu oturumda ÖLÇÜLEMEDİ.
- İş Yatırım takip listesi → 200; 54 hisse; öneri tarihlerinin 47'si 2026, 6'sı 2025.

### 3.2 FINRA açık pozisyon (short interest)
- `https://cdn.finra.org/equity/otcmarket/biweekly/shrtYYYYMMDD.csv` (boru ayraçlı). En eski erişilen: **shrt20171229.csv**; 20171215 ve öncesi (2010, 2014, 2015, 2016, 2017 denemeleri) 403.
- Sütunlar: accountingYearMonthNumber, symbolCode, issueName, issuerServicesGroupExchangeCode, marketClassCode, currentShortPositionQuantity, previousShortPositionQuantity, stockSplitFlag, averageDailyVolumeQuantity, daysToCoverQuantity, revisionFlag, changePercent, changePreviousNumber, settlementDate.
- Kapsam: 2018-01-12 dosyası 15.579 satır (OTC 7.222, NYSE 3.099, Nasdaq 2.352+860, ARCA 1.448…); 2026-10-15 dosyası 22.537 satır. Dosya 1,5-2,7 MB.
- Anahtarsız API: `POST https://api.finra.org/data/group/otcMarket/name/consolidatedShortInterest` (symbolCode + settlementDate süzgeci) → AAPL 2017-12-29 var, 2017-12-15 ve öncesi boş.

### 3.3 FINRA Reg SHO günlük açığa satış hacmi
- `https://cdn.finra.org/equity/regsho/daily/CNMSshvolYYYYMMDD.txt`: en eski **2018-08-01** (20180731 ve öncesi 403). Borsa bazlı dosyalar `FNSQshvol`, `FNYXshvol`, `FORFshvol`: **2009-08-03**'ten var; `FNQCshvol` 2022'de var, 2017'de yok.
- Sütunlar: Date|Symbol|ShortVolume|ShortExemptVolume|TotalVolume|Market (2009-2010 dosyalarında ShortExemptVolume yok).
- Uyarı: yalnız FINRA raporlama tesislerine bildirilen (borsa dışı) işlemleri kapsar; borsa içi açığa satış yok. API (`regShoDaily`) yalnız son dönem: 2026-11-09 dolu, 2025-11-10 boş.

### 3.4 Borsa İstanbul günlük bülten ve açığa satış
- Dosya yolları listesi: `https://www.borsaistanbul.com/files/DataFilePaths.zip` (VerilerDosyaIsimleri.xlsx). Bülten: `/data/thb/YYYY/AA/thbYYYYAAGG1.zip`; haftalık açığa satış: `/datum/acigasat.zip`.
- thb erişimi: 2005-01-03, 2009-06-01, 2013-03-01 (xls); **2015-12-01'den CSV**; 2026-11-10 var.
- 2026-11-10 CSV: 57 sütun, 9.524 satır (631 pay satırı). Başlıca alanlar: önceki kapanış, açılış, en düşük / en yüksek, kapanış, bekleyen en iyi alış / satış (fiyat), A.O.F (VWAP), toplam işlem hacmi / adedi / sözleşme sayısı, açılış seansı ve kapanış seansı hacim / miktar / sözleşme, kapanış fiyatından işlemler, **açığa satış en düşük / en yüksek fiyat, A.O.F, hacim, adet, sözleşme sayısı**, özel işlem bildirimi, orta nokta işlemleri, BIST 100 / 30 üyeliği, brüt takas bayrağı.
- 30 günlük örneklemde açığa satışı olan pay sayısı: 2016-06 161/420; 2017-06 177/410; 2019-10 219/410; 2020-01 224/409; **2020-06 0**; 2020-10 30; 2021-06 49; 2022-10 50; 2023-01 43; **2023-03 → 2024-10 hep 0**; 2025-01 50; 2025-06 0; 2025-10 49; 2026-01 50; **2026-03 ve 2026-06 0**; 2026-08-31 50. Sonuç: 2020'den beri açığa satış verisi yalnız BIST-30/50 için var, yasak dönemlerinde tamamen yok.

### 3.5 Takasbank Ödünç Pay Piyasası
- Sayfa: `https://www.takasbank.com.tr/tr/istatistikler/odunc-pay-piyasasi-opp/opp-gunluk-bulten` (tarih aralığı formu; giriş gerekmez). Excel: `/plugins/ExcelExportOPSPDailyNewsletter?startDate=YYYYMMDD&endDate=YYYYMMDD&lang=T&language=tr`.
- Sütunlar: İşlem Tarihi, Valör, Gün Sayısı, Kıymet Grubu, Kıymet Kodu, Grup, Min. Oran, Max. Oran, Ort. Oran, Adet, Piyasa Değeri (TL), Piyasa Değeri (USD), Sözleşme Sayısı.
- Denenen tarihler: 26.02.2008 (29 kıymet), 03.01.2012 (34), 03-06.01.2017 (91), Ocak 2017 tek istekte bütün ay (22 gün, 1.452 satır, 174 kıymet; 355 satır BIST-100 dışı), 10.11.2026 (35 kıymet, oran %2,9-5,0). 01-02.06.2023 ve 03-04.06.2024 sorguları tablo döndürmedi (açığa satış yasağı dönemi); Excel ucu bu tarihlerde boş yanıt verdi.
- Belirsiz: "Oran" biriminin tanımı belgeden doğrulanmadı (2008-2017 örneklerinde 75, 100, 200 gibi değerler var).

### 3.6 IEX HIST
- `https://iextrading.com/api/1.0/hist` → 200, 2.509 gün. Bir DEEP dosyasının ilk 64 KB'ı indirildi (206, gzip pcap): bağlantılar çalışıyor.
- Yıllık DEEP boyutu (GB): 2017 110 (164 gün), 2018 340, 2019 266, 2020 264, 2021 709, 2022 1.162, 2023 1.000, 2024 1.146, 2025 2.160, 2026 2.762 (217 gün).

### 3.7 Diğer
- IBorrowDesk `/api/v2/coverage` → `daily_earliest_available 2015-07-13`, `max_symbols 100`, `unit_days 365`. `/api/ticker/AAPL` → 403 (otomatik istemci reddi).
- IBKR FTP (port 21) → bağlantı kurulamadı (bu ortamın ağı).
- Borsa İstanbul `sayfa/2816` (tarihsel veri satışı) → 503 / boş yanıt; DataStore ana sayfası yalnız JS kabuğu.
- web.archive.org → bağlantı kesildi; İş Yatırım sayfasının arşiv derinliği ölçülemedi.

---

## 4. Hesaplanabilir ölçüler

| Ölçü | Gereken veri | ABD: hangi kaynakla | BIST: hangi kaynakla |
|---|---|---|---|
| OFI (en iyi kademe emir akışı dengesizliği) | en iyi alış / satış fiyatı + büyüklüğü, olay bazında | Alpaca kotasyonları (ücretsiz hesap, 2016+); Massive Advanced 199 $; Databento en iyi kademe; IEX TOPS (ücretsiz ama yalnız IEX) | yalnız DataStore emir defteri (fiyat belirsiz) → bugün HESAPLANAMAZ |
| Gerçekleşen alış-satış dengesizliği (işaretli işlem) | işlem + o andaki kotasyon | Alpaca işlem + kotasyon; Massive Developer (yalnız işlem, tik kuralı) / Advanced; Databento; IEX TOPS / DEEP (yalnız IEX) | DataStore işlem defteri → bugün HESAPLANAMAZ |
| Derinlik oranı (alış / satış derinliği) | çok kademeli defter | IEX DEEP (ücretsiz, yalnız IEX defteri); Databento 10 kademe / emir bazında (ücretli); LOBSTER | DataStore emir defteri → HESAPLANAMAZ. Bültendeki "bekleyen en iyi alış / satış" yalnız kapanış fiyatı, büyüklük yok |
| Satış emri geri çekilmesi (iptal) | emir bazında mesajlar | Databento emir bazında (ITCH); IEX DEEP kademe güncellemelerinden dolaylı; SEC MIDAS menkul bazında iptal / işlem oranı (ücretsiz, alanlar doğrulanmadı) | BISTECH ITCH / DataStore → HESAPLANAMAZ |
| Günlük açığa satış hacmi oranı | günlük açığa satış + toplam hacim | FINRA Reg SHO: 2018-08+ birleşik, 2009-08+ borsa bazlı (borsa dışı işlemler) — ÜCRETSİZ, HEMEN | Günlük bülten: 2015-12 → 2020-02 arası ~160-220 hissede; sonrası yalnız BIST-30/50 |
| Açık pozisyon / dolaşım, kapatma günü | iki haftalık açık pozisyon | FINRA 2017-12-29+ — ÜCRETSİZ, HEMEN | yok (Türkiye'de açık pozisyon yayını bulunamadı) |
| Teslim edilmeyenler | FTD dosyaları | SEC 2004+ — ücretsiz (iletişimli User-Agent şartı; Cemal'in izni gerekir) | yok |
| Ödünç ücreti, kullanılabilir adet | ödünç piyasası verisi | ücretsiz tarihsel YOK; IBorrowDesk API (29 $/ay, 2015-07+) | Takasbank ÖPP oranı ve adedi 2008+ — ÜCRETSİZ, ama günde 35-90 kıymet |
| Kullanım oranı (utilization) | ödünç verilebilir stok | yalnız kurumsal (S&P, DataLend, FIS) ya da ORTEX tahmini | ÖPP açık işlemler / dolaşımdaki pay ile kaba bir vekil kurulabilir; gerçek kullanım oranı YOK |
| EPS revizyonu (çeyrek öncesi 30 / 90 gün) | donmuş konsensüs görüntüsü | Alpha Vantage / EODHD 2017-06+ | VERİ YOK (doğrulanamadı) |
| Tavsiye / hedef fiyat değişikliği | olay günlüğü | Yahoo 2011-12+ (repoda) | VERİ YOK (tarihsel) |
| Tahmin dağılımı (en yüksek − en düşük) / analist sayısı | konsensüs özeti | Alpha Vantage / EODHD (high, low, analyst_count); standart sapma yok | VERİ YOK |

---

## 5. Önerilen sıradaki adımlar (ücretsiz, hemen)

| # | Adım | Ne ölçülür | İndirme | Süre (kibar hızla) |
|---|---|---|---|---|
| 1 | FINRA açık pozisyon 2017-12-29 → 2026-08-31 | açık pozisyon / hacim, kapatma günü, iki haftalık değişim; çöl olayından önceki son yayın | ~208 dosya × 1,5-2,7 MB ≈ 0,45 GB | ~10 dk |
| 2 | FINRA Reg SHO CNMS 2018-08-01 → 2026-08-31 (2017 için FNSQ + FNYX + FORF) | günlük açığa satış hacmi oranı, çöl içinde 20 / 60 günlük ortalaması | ~2.030 dosya × 0,25-0,55 MB ≈ 0,8 GB | ~30 dk |
| 3 | Borsa İstanbul günlük bülten 2015-12-01 → 2026-08-31 | VWAP, sözleşme sayısı (ortalama işlem büyüklüğü), açılış / kapanış seansı payı; açığa satış oranı yalnız 2015-12 → 2020-02 ve BIST-50 | ~2.690 dosya ≈ 0,35 GB | ~30 dk |
| 4 | Takasbank ÖPP 2008 → 2026 (aylık aralıklarla Excel) | ödünç oranı, ödünç adedi / hacim; yalnız ÖPP'de işlem gören kıymetler | ~225 istek × ~0,1 MB ≈ 25 MB | ~30 dk (sunucu art arda istekte boş yanıt verdi; yavaş çekilmeli) |
| 5 | Alpha Vantage EPS görüntüsü: önce ücretsiz 25 hisselik pilot (günde 25 istek) | görüntü gününün bilanço gününden önce olduğunun sınanması (bilanço tarihleri repodaki k34 / SEC verisiyle) | 25 × ~40 KB | 1 gün |
| 6 | IEX DEEP pilot: 2019'dan 20 gün | derinlik oranı ve iptal ölçülerinin küçük hisselerde dolu olup olmadığı (IEX'te işlem var mı) | ~20 GB | birkaç saat |

SEC teslim edilmeyenler (FTD) için Cemal'in e-postalı User-Agent izni gerekir (CLAUDE.md SEC kuralı); bu çalışmada dokunulmadı.

---

## 6. Cemal'in karar vermesi gereken ücretli / hesap gerektiren seçenekler

| Seçenek | Maliyet | Ne kazandırır | Not |
|---|---|---|---|
| Alpha Vantage premium, tek ay | 49,99 $ [LİSTE] | 4.700 ABD hissesi için 2017-06+ çeyreklik EPS revizyon görüntüsü (~2 saatte iner) | önce adım 5 pilotu; BIST kapsamı bilinmiyor |
| Alpaca ücretsiz hesap | 0 $ (kayıt gerekir) | 2016+ işlem ve kotasyon → OFI ve işaretli işlem dengesizliği; olay pencereleriyle sınırlı çekim | hesap Cemal adına açılır; koşullar okunmalı |
| IBorrowDesk API | 29 $/ay, 5.000 birim [LİSTE: llms.txt] | IBKR ödünç ücreti ve kullanılabilir adet, 2015-07+ günlük | tüm evren × 2017-2026 ≈ 47.000 birim (ek paket fiyatı okunamadı); yalnız çöl olayı olan hisse-yıllar seçilirse 1-2 ay yeter |
| Massive (eski Polygon) Developer / Advanced | 79 / 199 $/ay | bütün ABD işlemleri (10 yıl) / kotasyonlar (20+ yıl), düz dosya | Developer fiyatı ikincil kaynak |
| Massive + Benzinga analist notları | 99 $/ay [LİSTE] | 2012+ not ve hedef fiyat değişiklikleri | Yahoo günlüğüyle büyük ölçüde örtüşür; EPS tahmini yok |
| Databento | 125 $ ücretsiz kredi, sonra kullanım bazlı | Nasdaq emir bazında veri (iptal, derinlik) 2018-05+ | GB fiyatı doğrulanmadı; kayıt gerekir |
| EODHD Fundamentals | 59,99 $/ay [LİSTE] | Alpha Vantage ile aynı yapıda EPS görüntüsü + toplu uç; BIST olasılığı | BIST'te alanın dolu olduğu doğrulanamadı; satın almadan önce desteğe sorulmalı |
| ORTEX | 49 / 149 $/ay | tahmini ödünç maliyeti ve kullanım oranı | model tahmini; tarihsel dışa aktarım koşulu belirsiz |
| Borsa İstanbul DataStore emir / işlem defteri | belirsiz | BIST'te tek gerçek emir akışı kaynağı | fiyat sayfası açılmadı; Borsa'ya yazılması gerekir |
| Fintables / Matriks (MKK takas, AKD) | 149-980 TL/ay + lisans | günlük takas / AKD ekranı | tarihsel toplu indirme doğrulanamadı |
| I/B/E/S, FactSet, Bloomberg, S&P Securities Finance, DataLend, TAQ | kurumsal | tam nokta-zaman veri | bireysel bütçeyle erişilemez |

---

## 7. Belirsiz kalanlar

- Yahoo analist modüllerinin BIST hissesinde ne döndürdüğü (429 yüzünden ölçülemedi).
- Alpha Vantage / EODHD donmuş görüntüsünün tam alındığı gün; BIST kapsamı; Alpha Vantage'ın borsadan çıkmış hisseleri verip vermediği.
- Finnhub ve FMP plan fiyatları ve tarihsel derinlikleri (sayfalar okunamadı).
- Borsa İstanbul DataStore ürün adları, fiyat listesi, akademik indirim (sayfa 503).
- Takasbank "Oran" birimi; ÖPP dışındaki (aracı kurum içi) ödünç işlemleri hiçbir kaynakta yok.
- Databento GB fiyatı; LOBSTER koşulları; Kibot / FirstRate fiyatları (kaynaklar çelişkili).
- Zacks, Estimize, Tiingo, Koyfin, MarketBeat, TipRanks, Seeking Alpha, Foreks, Finnet, Rasyonet, Investing.com, Bloomberg HT: yapılandırılmış tarihsel analist verisi için kanıt bulunamadı.
- SEC MIDAS menkul bazındaki dosyaların alanları ve FTD dosyalarının güncel son tarihi (SEC'e istek atılmadı).
- Nasdaq / NYSE'nin 2017-12 öncesi açık pozisyon arşivi (ücretsiz kaynak bulunamadı; repo notu "2016-2017 ücretsiz yok" ile uyumlu).
