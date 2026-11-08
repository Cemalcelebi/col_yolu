# Kripto: büyük kısa vadeli yükselişleri (+%50 / +%100, 1-birkaç gün) tespit etme — akademik ve sektör kanıtı (Kasım 2026 itibarıyla)

Etiketler: [HAKEMLİ] = hakemli dergi/konferans; [ÇALIŞMA KAĞIDI] = arXiv/SSRN, hakemsiz; [SEKTÖR] = borsa/araştırma şirketi raporu, hakemsiz, çoğu zaman çıkar çatışmalı; [HABER] = ikincil aktarım.
Genel yanlılık uyarısı: Kripto örneklemlerinin çoğu CoinGecko/CMC'de "bugün hâlâ listelenen" tokenlardan kurulur → hayatta kalma yanlılığı (ölen tokenlar düşer, getiriler olduğundan iyi görünür). "Listeleme sonrası" çalışmalarında olay tarihi duyuru mu, işlem başlangıcı mı belirsizse ileriye bakma yanlılığı oluşur (fiyat duyurudan önce koşmuş olabilir).

## 1. Borsa listeleme etkisi ve yeni tokenların listeleme sonrası seyri

### Takeaway
Listeleme duyurusu/ilk günlerde kısa, pozitif bir anormal getiri var (eski akademik örneklerde ~%7, Coinbase'te Binance'ten büyük), ama primin çoğu duyurudan önce fiyatlanıyor ve 7-60 günde siliniyor. 2024-2025 kuşağı yeni tokenların ~%80-85'i TGE fiyatının altında; yüksek FDV'li açılışlar en kötü. Yani "listelemede al" perakende için ortalamada kaybettiren bir strateji; tek kullanılabilir şey çok kısa (saat-gün) pencere.

### Cited Findings
- Ante (2019) [ÇALIŞMA KAĞIDI, Blockchain Research Lab; 2018-19 listelemeleri]: listeleme gününde ortalama +%7,4 anormal getiri, 3 gün sonra +%9,2; etki borsaya göre çok değişken — [Blockchain Research Lab](https://www.blockchainresearchlab.org/de/2019/09/10/market-reaction-to-exchange-listings-of-cryptocurrencies-2/); rakamlar RockawayX'in literatür özetinde de aynı — [RockawayX](https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex)
- Li, Luo, Wang, Wei, "Cryptocurrency Exchange Listings" [HAKEMLİ, AFT 2025 genişletilmiş özet; tam metin SSRN 4715718]: Coinbase ve Binance'te kısa vadeli listeleme getirisi pozitif ve Coinbase'te anlamlı biçimde daha büyük; daha sıkı düzenlenen borsada listeleme getirisi daha yüksek (80 borsalık düzenleme endeksi); Binance'in kendi girişim kolunun fonladığı tokenların temelleri daha zayıf (Coinbase'te bu yok). Özet sayısal değer, örneklem dönemi vermiyor — [AFT 2025 / LIPIcs](https://drops.dagstuhl.de/storage/00lipics/lipics-vol354-aft2025/html/LIPIcs.AFT.2025.11/LIPIcs.AFT.2025.11.html)
- Four Pillars (Ponyo), "Binance Listing, Flash or Fade?" [SEKTÖR, 31 Ekim 2024; 2024'te Binance'te listelenen 32 token]: medyan getiri 1 gün +%1,0 (pozitif oran %53,1), 30 gün +%2,9 (%50,0), 6 ay −%60,0 (pozitif oran yalnız %9,5), yıl başından 28 Ekim'e −%56,4 (%12,5). Getiri hesaplama yöntemi ve 6 ay penceresinin n'i belirtilmemiş; anlamlılık testi yok — [Four Pillars](https://research.4pillars.io/en/research/binance-listing-flash-or-fade)
- RockawayX [SEKTÖR, tarih belirsiz (~2025); 2024 Binance/Bybit/MEXC USDT listelemeleri, CoinGecko piyasa değeri]: Bybit'te listeleme öncesi haftada yükseliş sonra kademeli satış ("söylentide al, haberde sat"); Binance'te 1-2 gün yükseliş, 7. güne kadar sönüyor, 30 günde ~sıfıra dönüş, 60 günde satış; MEXC'te 7 günden itibaren hafif ve sürekli düşüş. 7 günlük kademeli DiD'de Binance ve Bybit etkisi anlamlı ama güven aralıkları geniş; 30/60 gün DiD geniş aralık nedeniyle raporlanmamış. Binance listelemelerinin ~%26'sı >500 M$ piyasa değerinde, MEXC'te ~%3,6. Coinbase/Upbit/OKX veri erişimi yüzünden yok. Ayrıca vadeli (perp) işlemin spotla aynı anda açılmasının açığa satış baskısı yaratabileceğini not ediyor (ölçülmemiş) — [RockawayX](https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex)
- Animoca Research (Ouyang vd., 2024, "2024 Listing Performance Overview Jan-Sep") [SEKTÖR, yalnız ikincil aktarım]: CEX listelemesi sonrası ortalama −%49 düşüş; yöntem/örneklem aktaran kaynakta yok — [RockawayX aktarımı](https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex)
- Memento Research [SEKTÖR, 2025 TGE'leri, 118 token; haber aktarımı]: %84,7'si (100/118) TGE değerlemesinin altında; medyan FDV düşüşü −%71,1; eşit ağırlıklı sepet ~−%33, FDV ağırlıklı endeks −%61,5; ≥1 milyar $ FDV ile açılan 28 tokenın hiçbiri yeşil değil (medyan ~−%81); 25-200 M$ FDV aralığında %40 yeşil — [The Defiant](https://thedefiant.io/news/research-and-opinion/token-launches-with-low-fdvs-vastly-outperformed-hyped-debuts-in-2025-memento-research); [CryptoSlate](https://cryptoslate.com/heres-why-4-out-of-5-new-tokens-launches-crashed-this-year/)
- DWF Labs (Memento verisiyle) [SEKTÖR]: 2025 listelemelerinin >%80'i TGE altında, tipik düşüş ~90 günde %50-70 — [Whale Alert aktarımı](https://whale-alert.io/stories/ca8d01157f6a5c/DWF-Labs-80-of-2025-Tokens-Trade-Below-TGE-Institutional-Capital-Rotating-into-Public-Crypto-Stocks-and-Infrastructure)
- Arrakis Finance [SEKTÖR, 125 TGE + 25 kurucu anketi, 2025]: ~%85 açılış fiyatının altında; belirleyici olan piyasa zamanlaması değil erken satış baskısı; zayıf açılan 10 tokendan ancak 1'i toparlandı — [The Defiant](https://thedefiant.io/only-1-in-10-weak-token-launches-recovered-in-2025-arrakis)
- Upbit (Kore): hakemli olay çalışması bulunamadı. Haber/bloglar: duyurudan sonra fiyatın genelde ~2 saat içinde zirve yapıp düştüğü (BlockBeats gözlemi, kontrollü test değil) — [ChainCatcher](https://chaincatcher.com/en/article/2068840); 2021 AAVE/1INCH, ALGO/AUDIUS Upbit sıçramaları — [FXStreet](https://www.fxstreet.com/cryptocurrencies/news/algorand-and-audius-skyrocket-after-upbit-listing-emulating-the-coinbase-effect-202111181125); BIRB'de 24 saatte zirvede +%46,25, "Kore primi"ne bağlanıyor — [KuCoin](https://www.kucoin.com/news/articles/upbit-announces-listing-of-birb-liquidity-influx-from-korean-market-triggers-asset-volatility)
- The Tie: zaten 3+ büyük borsada olan tokenlar için Binance listelemesinin ne getirdiğini inceleyen not (içerik açılmadı) — [The Tie](https://www.thetie.io/insights/what-a-binance-listing-delivers-for-already-listed-tokens)

### Inferences
- Listeleme etkisi "duyuru → saatler/1-2 gün" penceresinde yaşıyor; perakende duyuruyu borsa API'sinden/duyuru kanalından saniyeler içinde göremiyorsa (botlar görüyor) ortalama giriş noktası zaten primin büyük kısmını kaçırıyor.
- 2024-2025'te yeni tokenların ezici çoğunluğu düştüğüne göre, "yeni listelenmiş tokenda büyük yeşil gün" taban oranda bir düşüş trendinin içindeki geçici sıçrama olma olasılığı yüksek; yüksek FDV / düşük dolaşım (low float) en olumsuz alt grup.
- Memento/DWF/Galaxy/Arrakis rakamları büyük ölçüde aynı 2025 kuşağına ait, bağımsız dört kanıt değil; DWF bir piyasa yapıcı (çıkar çatışması).
- Hayatta kalma: TGE çalışmaları büyük borsada listelenmiş projelerle sınırlı; DEX'te doğup ölen milyonlarca token dahil edilse ortalama daha da kötü olur.

### Gaps
- Coinbase etkisi için akademik büyüklük (gün 0 CAR) ve Binance–Coinbase farkının sayısı: Li-Luo-Wang-Wei tam metni (SSRN 4715718) okunamadı.
- Upbit/Bithumb/OKX listeleme duyurusu için hakemli olay çalışması bulunamadı; Kore primi (kimchi premium) ile listeleme getirisi arasındaki ilişkiyi ölçen çalışma bulunamadı.
- Kaiko, Galaxy, Keyrock, Binance Research'ün low-float/high-FDV raporlarının birincil metinleri bu turda açılamadı (Binance Research'ün 2024 "Low Float & High FDV" raporu bilinen ama doğrulanmadı).
- Binance Alpha, "önce vadeli sonra spot" listeleme düzeninin fiyat etkisini ölçen bir çalışma bulunamadı.

## 2. Pump-and-dump literatürü: tespit doğruluğu, öncü süre, sonrası

### Takeaway
Organize (Telegram) pompalar küçük (<20 M$), sığ tokenlarda, dakikalar süren, çoğu zaman yüzlerce yüzde sıçrayıp saatler içinde başlangıca dönen olaylar. Gerçek zamanlı tespit (piyasa alım emri "rush order" patlaması) ~25 saniyede F1 ≈ %94 veriyor ama bu bir kaçış/denetim aracı, alım sinyali değil: katılımcıların çoğu (organizatör hariç) para kaybediyor.

### Cited Findings
- Kamps & Kleinberg (2018), "To the moon" [HAKEMLİ, Crime Science 7:18]: fiyat+hacim anomali kuralı; parametreye göre 9.668 (gevşek), 2.150 (dengeli), 920 (sıkı) şüpheli olay; doğrulanmış etiket seti yok — [UCL Discovery](https://discovery.ucl.ac.uk/id/eprint/10069142/); [Crime Science tablo 5](https://crimesciencejournal.biomedcentral.com/articles/10.1186/s40163-018-0093-5/tables/5)
- Xu & Livshits, "The Anatomy of a Cryptocurrency Pump-and-Dump Scheme" [HAKEMLİ, USENIX Security 2019; Telegram, Haz 2018 – Şub 2019, 412 olay (v1: 220)]: hangi coinin pompalanacağını önceden tahmin eden random forest, örneklem içi ve dışı AUC > 0,9; kalibre strateji 11 haftada %60 (sıkı varsayımlar; erken sürümde 3 haftada %80) — [arXiv 1811.10109](https://arxiv.org/pdf/1811.10109)
- La Morgia, Mei, Sassi, Stefa (2020 arXiv; genişletilmiş "The Doge of Wall Street", ACM TOIT 2023) [HAKEMLİ, Tem 2017 – Oca 2021, 20 Telegram grubu, 4 borsa]: 1.108 olay (902 benzersiz); model 317 Binance olayı. En önemli özellik saniye-milisaniye bazında toplanan piyasa alım emri patlaması (StdRushOrders). 25 sn'lik dilimlerde Random Forest kesinlik %98,2, duyarlılık %91,2, F1 %94,5; Kamps-Kleinberg tabanı F1 %62,7. Tespit ~25 sn (temel karşılaştırma metinde 30 dk ve 1 saat diye tutarsız). Hedef coinler: piyasa değeri bilinen 264 coinin %71'i <20 M$, %22'si <1 M$; %83,5'i pompadan önceki 24 saatte <1 M$ hacim; medyan piyasa değeri Binance'te 25,6 M$. Pompa dakikalar sürer (BPS ort. ~5 dk); fiyat birkaç saatte başlangıca döner. "Kalabalık pompaları" (DOGE +%800/24s, XRP +%56/gün) farklı: saatler-günler sürer, bir ay sonra DOGE hâlâ ~+%500. İçeriden işlem izleri (OAX'ta başlangıçtan %41 yukarıda 44 BTC'lik satış emri); XRP'de dedektör 2 gün önce alarm verdi, planlı pompada alarm yok. Yanlış alarm: ETH 1.276 günde 24 alarm — [arXiv 2105.00733](https://arxiv.org/html/2105.00733v2); [arXiv 2005.06610](https://arxiv.org/html/2005.06610v2)
- Dhawan & Putniņš (2023), "A New Wolf in Town?" [HAKEMLİ, Review of Finance 27(3):935-975]: 7 ayda en az 355 vaka, 72 Telegram kanalı, 2 borsa; organizatör dışındaki katılımcıların çoğu kaybeder (negatif toplamlı oyun); katılımcılar hız/yeteneklerini abartıyor — [EconPapers](https://econpapers.repec.org/RePEc:oup:revfin:v:27:y:2023:i:3:p:935-975.); [UTS](https://www.uts.edu.au/news/2021/09/beware-wolf-cryptocurrency-markets)
- Li, Shin, Wang, "Cryptocurrency Pump-and-Dump Schemes" [HAKEMLİ, JFQA] — künye mevcut, bulgular bu turda okunamadı — [Cambridge/JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/cryptocurrency-pumpanddump-schemes/97149DCD519BAF838F269F98DC76D682)
- Karbalaii (Nis 2025), "Microstructure and Manipulation" [ÇALIŞMA KAĞIDI, Poloniex, 15 Ağu 2024 – 15 Şub 2025, 485 aday olay, dakikalık veri]: olayların %69,3'ünde pompa öncesi hacim var; pompa öncesi hacmin ~%70'i duyurudan önceki son 1 saatte; pompa birkaç dakika sürüp fiyat hemen eski düzeye dönüyor; modellenmiş içeriden kâr medyanı %92-127 (gerçekleşmiş değil, model alt sınırı); zamanlama konusunda metin içi tutarsızlık — [arXiv 2504.15790](https://arxiv.org/html/2504.15790v1)
- Mahrous & Di Pietro, "PumpSense" [ÇALIŞMA KAĞIDI, 2026]: bağımsız veri setinde daha düşük skorlar: LightGBM F1 0,79, BGE-M3 F1 0,83 — hakemlik durumu doğrulanmadı — [arXiv 2605.09431](https://arxiv.org/abs/2605.09431)
- Chainalysis Crypto Crime Report 2025 [SEKTÖR; haber aktarımı]: 2024'te başlatılan tokenların ~%4,52'si pump-and-dump örüntüsü gösterdi (2023: %3,59); >2-3 milyon token başlatıldı, ~%40-42'si DEX'te; şüpheli DEX havuzlarının ~%90'ı (bir kaynakta %94) havuzu açan adresçe "rug" edildi; aktaran kaynaklar arasında rakam çelişkisi var — [crypto.news](https://crypto.news/chainalysis-over-4-5-of-all-tokens-launched-in-2024-have-pump-and-dump-traits/); [Tekedia (çelişkili 3,59 aktarımı)](https://www.tekedia.com/3-59-of-tokens-launched-in-2024-showed-signs-of-pump-and-dump-schemes-chainalysis-report-reveals/)

### Inferences
- Organize pompanın "sonrası" yapısal olarak hızlı ve tam geri dönüş: dakikalar-saatler. Perakendenin günlük mumla gördüğü +%100'lük gün, bu tip bir olaysa çoğunlukla zirve zaten geçmiştir.
- Tespit modelleri yüksek F1'i olay-penceresi sınıflandırmasıyla alıyor (sınıf dengesi, aynı dönem içi çapraz doğrulama); gerçek zamanlı, olay oranı çok düşük ortamda kesinlik çok daha düşük olur (ETH'de bile 24 yanlış alarm). PumpSense'in bağımsız setteki düşük skoru bunu destekliyor.
- Kullanılabilir tarafı savunma: düşük piyasa değeri + sığ hacim + ani piyasa alım emri patlaması görülen yükselişte "kovalamama" filtresi.

### Gaps
- Li-Shin-Wang (JFQA) bulguları (pompa sonrası getiri, Bittrex politikasıyla doğal deney) açılamadı.
- 2024-2026 memecoin/launchpad (pump.fun vb.) pompaları için akademik tespit doğruluğu çalışması bulunamadı.

## 3. Mikroyapı ve dikkat sinyalleri (OI + negatif fonlama, spot/perp hacmi, emir defteri, borsa akışları, balina, sosyal hacim, Kore primi)

### Takeaway
Bu sinyallerin neredeyse tamamı için yayımlanmış, örneklem dışı test edilmiş isabet oranı bulunamadı; kanıt analist yorumu ve vaka anlatısı düzeyinde. Tek güçlü mikroyapı kanıtı pompa tespitindeki "piyasa alım emri patlaması" (saniye ölçeği, bkz. Bölüm 2).

### Cited Findings
- "Hızla artan açık pozisyon (OI) + negatif fonlama = sıkışma (short squeeze) kurulumu" tezi K33 / Arcane Research analist notlarından geliyor; K33 bu birleşimi "nispeten nadir" diyor, ama yayımlanmış isabet oranı yok; 2022 ve 2026 çağrıları vaka bazlı — [Cointelegraph](https://cointelegraph.com/news/bitcoin-price-analysis-sees-new-short-squeeze-as-open-interest-nears-25b); [Decrypt](https://decrypt.co/245666/bitcoin-setup-ripe-short-squeeze-mt-gox-shifts-850-million-btc); [CoinDesk 2022](https://hotfix.coindesk.com/markets/2022/04/27/bitcoins-derivative-data-suggests-potential-for-short-squeeze)
- RockawayX: spotla aynı anda perp açılması açığa satış baskısı yaratabilir, ön-sonra karşılaştırmayı bozabilir (ölçülmemiş) — [RockawayX](https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex)
- La Morgia vd.: sosyal sinyal örneği — DOGE kalabalık pompasından önceki 24 saatte Reddit gönderileri arttı; Musk tweet'inden ~13 dk sonra alarm — [arXiv 2105.00733](https://arxiv.org/html/2105.00733v2)
- Keyrock: kilit açılımlarından 14 veya 28 gün önce ağırlıklı hacim çoğu zaman zirve yapıyor (yükseliş değil, dağıtım işareti) — [Keyrock](https://keyrock.com/from-locked-to-liquidity-what-16000-token-unlocks-teach-us/)

### Inferences
- OI/fonlama, Santiment/LunarCrush sosyal hacim, Kaito "mindshare", borsa net akışı, balina birikimi: hepsi ticari ürün olarak pazarlanıyor; bu turda hiçbirinin bağımsız, maliyet sonrası, örneklem dışı backtest'i bulunamadı → "pazarlama iddiası" sınıfında tutulmalı.
- Sosyal hacim büyük ölçüde hareketle eşzamanlı ya da gecikmeli; öncü olduğu iddiası test edilmemiş.

### Gaps
- Fonlama oranı/OI'nin altcoin kesitinde getiri öngördüğünü gösteren hakemli çalışma bulunamadı (BTC dışı).
- Kimchi primi / Upbit hacim payının altcoin yükselişi öngördüğüne dair sistematik çalışma bulunamadı.
- Santiment, LunarCrush, Kaito'nun kendi yayımladığı isabet istatistikleri (varsa) açılamadı.

## 4. Arz mekaniği: kilit açılımları, airdrop satışı, piyasa yapıcı kredi + opsiyon yapıları

### Takeaway
Kilit açılımlarının ~%90'ı fiyata negatif baskı yapıyor, düşüş açılımdan ~30 gün önce başlıyor; en kötüsü ekip açılımları. Piyasa yapıcı "token kredisi + alım opsiyonu" yapıları gizli; listeleme sonrası sıçrama ve çöküşlerdeki rolü belgelenmiş vaka ve suçlamalara dayanıyor, sistematik ölçüm yok.

### Cited Findings
- Keyrock, "From Locked to Liquidity: What 16,000+ Token Unlocks Teach Us" [SEKTÖR, 2024; 40 token, 16.000+ açılım olayı; ±30 gün, ETH'ye göre normalize, dönem belirtilmemiş]: açılımların %90'ı büyüklük/türden bağımsız negatif baskı; düşüş son 30 günde başlar, son haftada hızlanır; ekip açılımı ~−%25 (APE 7 ayda −%77, ETH −%9); yatırımcı açılımları OTC/TWAP/hedge ile "kontrollü"; ekosistem açılımı ortalama +%1,18; büyük açılımlar (%5-10) küçüklere göre ~2,4 kat sert düşüş (taban belirsiz); >%10 "dev" açılımlar büyüklerden iyi ya da eşit; oynaklık ~14 günde söner; doğrusal açılım ani (cliff) açılımdan az bozucu. Metin payda konusunda (toplam arz / dolaşım arzı) tutarsız — [Keyrock](https://keyrock.com/from-locked-to-liquidity-what-16000-token-unlocks-teach-us/); [BeInCrypto](https://beincrypto.com/keyrock-research-token-unlocks/)
- Piyasa yapıcı kredi + opsiyon yapısı [HABER/SEKTÖR]: MM tokenları ödünç alır, fiyat yükselirse nakitle geri ödeme opsiyonu (kullanım fiyatı lansmanda sabit → gömülü alım opsiyonu); fiyat düşerse token iadesi; opsiyon dolaşım arzına göre büyükse kullanım fiyatı "mıknatıs" etkisi; koşullar açıklanmıyor; bazı sözleşmelerde listeleme sonrası ucuz alıp satma maddeleri iddia ediliyor; OM (Mantra) çöküşünün opsiyon vadesine bağlanması proje tarafından reddedildi — [Cointelegraph](https://cointelegraph.com/magazine/market-maker-deals-quietly-killing-crypto-projects); [Crypto Briefing](https://cryptobriefing.com/market-maker-token-loans-transparency-scrutiny/)
- Gotbit, manipülatör olarak anılan piyasa yapıcı — [ForkLog](https://forklog.com/en/after-gotbit-a-large-scam-syndicate-surfaces/)

### Inferences
- Yeni token için takvimdeki büyük ekip/yatırımcı açılımına 30 gün kala gelen +%100 gün, açılım öncesi dağıtım için likidite yaratıyor olabilir; Keyrock bulguları bu dönemde ortalamanın negatif olduğunu söylüyor.
- MM opsiyon kullanım fiyatları kamuya açık olmadığı için perakende bu bilgiyi gerçek zamanlı kullanamaz.

### Gaps
- Airdrop satış baskısını sistematik ölçen çalışma (ör. airdrop sonrası 30/90 gün getirileri) bu turda açılmadı.
- ABD DOJ/SEC "Operation Token Mirrors" (Ekim 2024; Gotbit, ZM Quant, CLS Global'e yönelik sahte token/wash trading davası) iddianame ayrıntıları bu turda birincil kaynaktan doğrulanamadı.
- The Tie'nin açılım çalışması açılamadı.

## 5. Taban oranlar: yeni listelenen tokenda ilk 3 ayda +%100 gün sıklığı ve sonrası (7/30/90 gün)

### Takeaway
Bu soruyu doğrudan ölçen (yeni token, ilk 3 ay, +%100 gün, sonraki 7/30/90 gün getiri dağılımı) bir akademik veya sektör çalışması bulunamadı. Dolaylı kanıt ters yönde: 2024-25 yeni tokenlarının ~%85'i TGE altında, 6 ayda medyan −%60 (Binance 2024).

### Cited Findings
- Dolaylı: Binance 2024 listelemeleri 6 ayda medyan −%60, pozitif oran %9,5 — [Four Pillars](https://research.4pillars.io/en/research/binance-listing-flash-or-fade)
- Dolaylı: 2025 TGE'leri medyan −%71; ~90 günde tipik −%50-70 — [The Defiant / Memento](https://thedefiant.io/news/research-and-opinion/token-launches-with-low-fdvs-vastly-outperformed-hyped-debuts-in-2025-memento-research); [DWF/Whale Alert](https://whale-alert.io/stories/ca8d01157f6a5c/DWF-Labs-80-of-2025-Tokens-Trade-Below-TGE-Institutional-Capital-Rotating-into-Public-Crypto-Stocks-and-Infrastructure)
- Dolaylı: organize pompalarda fiyat saatler içinde başlangıca döner — [arXiv 2105.00733](https://arxiv.org/html/2105.00733v2)

### Inferences
- Bu taban oran kendi verimizle (ör. CoinGecko/Binance kline, listeleme tarihine göre hizalı, ölen tokenlar dahil) ölçülmeli; literatürde hazır sayı yok. Ölçümde: giriş = sinyal gününden sonraki ilk açılış (ileriye bakmama), batan/delist olan tokenlar dahil (hayatta kalma), aynı gün listelenme yaşı eşli kontrol grubu.

### Gaps
- "Yeni tokenda +%100 gün sonrası getiri dağılımı" için hiçbir kaynak bulunamadı — açık araştırma boşluğu.

## 6. Günlük ufukta momentum mu geri dönüş mü; +%100 günleri kovalamak maliyet sonrası kârlı mı

### Takeaway
Kesitsel olarak kripto 1-4 haftalık momentum gösteriyor (Liu-Tsyvinski-Wu, JF 2022), ~1 ay sonra geri dönüş başlıyor (Dobrynskaya); haftalık geri dönüş küçük/sığ coinlerde, momentum büyük/likit coinlerde (Fičura). MAX (en yüksek günlük getiri) için bulgular çelişkili. Hiçbiri yeni tokenda tek +%100 günü kovalamanın maliyet ve kayma sonrası kârlı olduğunu göstermiyor; getiriler brüt.

### Cited Findings
- Liu, Tsyvinski, Wu (2022), "Common Risk Factors in Cryptocurrency" [HAKEMLİ, Journal of Finance 77(2):1133-1177; 2014-2018 civarı, >1 M$ piyasa değerli coinler]: uzun-kısa momentum haftalık fazla getiri 1 hafta %2,7, 2 hafta %3,3, 3 hafta %4,1, 4 hafta %2,5; piyasa+büyüklük+momentum 3 faktör modeli bunları açıklıyor; getiriler brüt; çok faktör denendiği için veri karıştırma (data snooping) uyarısı (CXO) — [NBER w25882](https://www.nber.org/papers/w25882.pdf); [Alpha Architect](https://alphaarchitect.com/factors-investing-in-cryptocurrency/); [CXO Advisory](https://cxoadvisory.com/size-effect/cryptocurrency-factor-model)
- Dobrynskaya (2023), "Cryptocurrency Momentum and Reversal" [HAKEMLİ, Journal of Alternative Investments 26:65-76]: ~2 haftaya kadar momentum, ~1 ay sonra güçlü geri dönüş (hisselere göre çok daha erken); geri dönüşü esas "geçmiş kaybedenler" sürüklüyor; standart kripto faktörleriyle açıklanmıyor — [HSE](https://www.hse.ru/en/news/research/559533243.html); [EconBiz](https://econbiz.de/Record/cryptocurrency-momentum-and-reversal-dobrynskaya-victoria/10014265388)
- Fičura (2023) [ÇALIŞMA KAĞIDI, VŠE Prag FFA WP 5:003]: haftalık geri dönüş yalnız küçük ve sığ coinlerde; büyük/likit coinlerde haftalık momentum — [IDEAS](https://ideas.repec.org/p/prg/jnlwps/v5y2023id5.003.html)
- Li, Urquhart, Wang, Zhang (2021), "MAX momentum in cryptocurrency markets" [HAKEMLİ, International Review of Financial Analysis 77]: geçmişte en yüksek günlük getirisi büyük olan coinler sonra da daha yüksek getiri (hisselerdeki MAX etkisinin tersi); piyasa koşulu ve duyarlılığa bağlı — [Reading](https://centaur.reading.ac.uk/99101); "Lottery-like preferences and the MAX effect" [HAKEMLİ, Financial Innovation 2021]: en yüksek–en düşük MAX ondalık farkı haftalık ham %3,03, risk düzeltmeli %1,99; aynı dergideki başka analiz MAX'ın oynaklığın vekili olabileceğini ve etkinin geçici olduğunu öne sürüyor (çelişkili) — [Springer](https://link.springer.com/10.1186/s40854-021-00291-9)

### Inferences
- Akademik momentum/MAX bulguları yerleşik, piyasa değeri eşikli (yaşayan) coin evreninde, haftalık portföy ve brüt getiriyle; yeni listelenmiş, sığ tokenda tek günlük +%100 kovalamaya genellenemez. Sığ coinlerde haftalık geri dönüş (Fičura) ve organize pompaların hızlı çöküşü, yeni tokenda kovalamanın aleyhine.
- Maliyet: yeni tokenlarda alış-satış farkı ve kayma yüzde birkaç olabilir; haftalık %2-4 brüt prim bunu kolayca yer. Bu konuyu ölçen bir çalışma bulunamadı.
- Hayatta kalma: LTW ve MAX çalışmalarında coinler CoinMarketCap'ten; delist olanların ele alınışı sonucu etkiler.

### Gaps
- Liu & Tsyvinski (2021, RFS) "Risks and Returns of Cryptocurrency" (zaman serisi momentumu, yatırımcı dikkati) bu turda açılmadı.
- Günlük ufukta, maliyet ve kayma sonrası, yeni tokenlarda "büyük yeşil günü al" stratejisini test eden çalışma bulunamadı.

---

## Kaynak listesi (özet)
Hakemli: Kamps & Kleinberg 2018 (Crime Science); Xu & Livshits 2019 (USENIX Security); La Morgia vd. 2023 (ACM TOIT); Dhawan & Putniņš 2023 (Review of Finance); Li-Shin-Wang (JFQA, okunamadı); Liu-Tsyvinski-Wu 2022 (JF); Dobrynskaya 2023 (JAI); Li-Urquhart-Wang-Zhang 2021 (IRFA); Financial Innovation 2021 MAX; Li-Luo-Wang-Wei 2025 (AFT).
Çalışma kağıdı: Ante 2019 (BRL); Fičura 2023; Karbalaii 2025 (arXiv 2504.15790); PumpSense 2026 (arXiv 2605.09431).
Sektör: Keyrock 2024 (açılımlar); Four Pillars 2024; RockawayX (~2025); Animoca 2024 (ikincil); Memento 2025; DWF Labs 2025; Arrakis 2025; Chainalysis 2025 raporu (ikincil); K33/Arcane analist notları.
