# Yeni token sıçraması önceden görünmüyor, kovalayan kaybediyor

Değerlendirme tarihi: 8 Kasım 2026.
Kaynak etiketleri: **[HAKEMLİ]** hakemli dergi/konferans. **[ÇK]** hakemsiz çalışma kağıdı. **[SEKTÖR]** şirket araştırması, hakemsiz, çoğu zaman çıkar çatışmalı. **[BORSA]** borsa duyurusu veya blogu. **[AGG]** veri toplayıcı (CoinMarketCap, CoinGecko). **[MEDYA]** haber. **[SOSYAL]** kullanıcı yazısı. **[ÖLÇÜM]** bu çalışmada borsa API'lerinden indirilen günlük veriyle hesaplandı (8 Kasım 2026).

## 1. Kısa cevap

- **Güvenilir önceden tespit yok.** En iyi sinyal "dün ≥ +%11,5 yükseldi". Bu sinyal ertesi gün +%100 olasılığını yaklaşık 5 katına çıkarıyor. Ama olasılık yine yalnız **%0,64**. Sinyal günlerinin %99'undan fazlasında +%100 olmuyor. [ÖLÇÜM, 759 token, test yarısı]
- **Ne kadar önce:** en fazla 1 gün. Sinyal önceki günün kapanışında görülüyor. Bu bir tahmin değil, "oynaklık arttı" ölçüsü.
- **Ne kadar nadir:** listeden 1 ay sonra +%100 kapanış günü, 1.000 token-günde yaklaşık 1 kez (%0,1) görülüyor. En sık listeden sonraki ilk gün: 1.000'de 18. [ÖLÇÜM]
- **Sonrası:** +%100 gününün ertesi açılışında alan kişi medyan olarak 1 günde **−%16**, 7 günde **−%35**, 30 günde **−%49** kaybediyor. 30 gün sonra yalnız %16'sı artıda. [ÖLÇÜM]
- **Kovalamak kazandırmıyor.** Sinyal gününde almak da, +%100 gününden sonra almak da ortalama günden kötü sonuç veriyor. Literatür de aynı yönde: 2025'te yeni tokenların yaklaşık **%85'i** açılış fiyatının altında [SEKTÖR, 2025].
- **Ritual'da doğrulanmış bir haber yok.** Ekrandaki +%99,88, 24 saatlik kayan değişim. Gate saatlik verisinde 8 Kasım 09:00–10:00 UTC'de +%102–107'ye ulaştı. UTC günlük bazda gün içinde +%66'ydı. [ÖLÇÜM]
- **Proje kuralına göre: İZ DEĞİL.** Sinyal örneklem dışında tutuyor ama para kazandırmıyor.

## 2. Ritual düşük float'lu, haber olmadan sıçradı

### Proje
Ritual, yapay zekâ odaklı, EVM uyumlu bir Katman-1 ağı. Eski Polychain ortakları Niraj Pant ve Akilesh Potti 2023'te kurdu. Kasım 2023'te Archetype liderliğinde **25 milyon $** topladı ([The Block](https://www.theblock.co/news/deals/2023-11-08-decentralized-ai-compute-platform-ritual-closes-25-million-fundraise-262114), [MEDYA], 08.11.2023). Lansman öncesi toplam fon 30 milyon $'ın üzerinde ([Phemex](https://phemex.com/news/article/ritual-launches-ai-layer-1-mainnet-and-ritual-token-price-dives-72-from-high-101259), [MEDYA], 27.10.2026). Değerleme bulunamadı.

### TGE ve arz yapısı
TGE ve ana ağ aynı gün açıldı: **26 Ekim 2026**.

| Kalem | Değer | Kaynak |
|---|---|---|
| Başlangıç arzı | 10 milyar, sabit tavan yok, ~%5/yıl enflasyon | [BORSA] KuCoin blog, 27.10.2026 |
| Açılışta dolaşım | 1,8 milyar = **%18** (düşük float) | [BORSA] KuCoin blog |
| Ekip / yatırımcı payı | %29 / %11,3; en az 1 yıl kilitli (~Ekim 2027) | [BORSA] KuCoin blog |
| Airdrop | 50 milyon (%0,5), yalnız 852 cüzdan | [BORSA] KuCoin blog; [MEDYA] Phemex |
| Piyasa değeri / FDV (08.11) | 74,8 milyon $ / 415,4 milyon $ | [AGG] CMC |
| Piyasa değeri / FDV oranı | 0,18 | [AGG] CoinGecko, 08.11.2026 |

Tokenomik kaynağı: [KuCoin blog](https://www.kucoin.com/blog/ritual-mainnet-ritual-tokenomics-airdrop). Yakın vadede kilit açılımı yok. Yani yükselişin arkasında unlock baskısı veya bitişi yok.

Çıkarım (doğrulanmadı): 1,8 milyarın büyük kısmı vakıf ve ekosistem cüzdanında. Piyasada gerçekten dönen arz muhtemelen çok daha küçük. Küçük hacim, büyük fiyat hareketi yaratabilir.

### Listelemeler

| Borsa | Tarih | Kaynak |
|---|---|---|
| Coinbase spot (RITUAL-USD) | Yol haritası 16.09; işlem 26.10.2026 | [MEDYA] [Crypto Briefing](https://cryptobriefing.com/coinbase-enables-ritual-token-spot-trading/) |
| MEXC spot | 26.10.2026 | [ÖLÇÜM] MEXC API; [BORSA] KuCoin blog |
| Gate spot | 27.10.2026 13:00 UTC | [ÖLÇÜM] Gate API |
| KuCoin spot | 28.10.2026 10:00 UTC | [BORSA] [KuCoin duyuru](https://www.kucoin.com/news/flash/kucoin-launches-ritual-ritual-listing-campaign-with-2-3m-ritual-giveaway) |
| Vadeli (perp) | Yalnız MEXC Futures, Ourbit, KCEX | [AGG] CoinGecko, 08.11.2026 |
| Binance, Upbit, Bithumb, Bybit, OKX | Duyuru bulunamadı | Arama + [AGG] CoinGecko |

8 Kasım'da spot hacmin **%77'si Gate'te**, %21'i Coinbase'te ([CoinGecko](https://www.coingecko.com/en/coins/ritual), [AGG]). Yükselişten önce büyük bir borsa duyurusu yok. "Upbit etkisi" bu vakada desteklenmiyor.

### Fiyat yolu

| Tarih | Olay | Kaynak |
|---|---|---|
| 26.10 | Açılış ~0,07 $, zirve 0,08–0,09 $ | [AGG] CMC; [MEDYA] Phemex |
| 27.10 | 0,0226 $, zirveden −%72 | [MEDYA] Phemex |
| 02.11 | Dip 0,01694 $ (CMC); Gate kapanışı 0,0189 $ | [AGG] CMC; [ÖLÇÜM] |
| 03.11 | Gate'te gün içi +%122 (tepe 0,0419), kapanış yalnız +%36 | [ÖLÇÜM] |
| 05–06.11 | Kapanış ~0,019 $, yani 03.11 sıçraması tamamen silindi | [ÖLÇÜM] |
| 07.11 | Kapanış 0,02446 $, **+%28,6**, hacim 2,0 milyon $ | [ÖLÇÜM] |
| 08.11 | 09:00–10:00 UTC 0,0417–0,0426 $, 24 saatlik değişim +%102–107; tepe 0,046 $ | [ÖLÇÜM] Gate saatlik |
| 08.11 (20:00 UTC) | 0,0407 $; UTC günlük değişim +%66,4 | [ÖLÇÜM] |

Ekrandaki **0,04164 / +%99,88**, bir "son 24 saat" değişimi. Hesap: 0,04164 / 1,9988 ≈ 0,0208 $ referans fiyat. Bu, Gate'in 8 Kasım 09–10 UTC saatleriyle uyumlu. UTC günlük kapanışa göre gün +%100 değil. Günün kesin sonucu 9 Kasım 00:00 UTC'de belli olur.

Not: 3 Kasım'daki ilk sıçrama önemli bir ders. Gün içinde fiyat ikiye katlandı, kapanışta kazancın çoğu gitti, iki günde başa döndü.

### Katalizör bulunamadı
CMC'de hareket için açıklama yok ([CMC](https://coinmarketcap.com/currencies/ritual/), [AGG], 08.11.2026). 6–8 Kasım için haber araması sonuç vermedi. Vadeli açık pozisyon 534 bin $, piyasa değerinin **%0,73'ü**. Fonlama pozitif (+%0,026 / 8 saat). Yani longlar shortlara ödüyor; short squeeze kanıtı yok ([CoinGecko](https://www.coingecko.com/en/coins/ritual), [AGG]). KuCoin Square yazıları yalnız teknik anlatı kullanıyor [SOSYAL]. En olası açıklama mikro yapı: ince likidite, tek borsada toplanmış hacim, küçük gerçek arz. Bu bir çıkarım, kanıt değil.

## 3. Literatür: listeleme primi kısa, yeni tokenlar çoğunlukla düşüyor

### Listeleme etkisi ve yeni token getirileri

| Bulgu | Tür, tarih | Kaynak |
|---|---|---|
| Listeleme günü ort. +%7,4 anormal getiri, 3 günde +%9,2 | [ÇK], 2018–19 verisi | [Ante 2019](https://www.blockchainresearchlab.org/de/2019/09/10/market-reaction-to-exchange-listings-of-cryptocurrencies-2/) |
| Coinbase listeleme getirisi Binance'ten anlamlı büyük | [HAKEMLİ], AFT 2025 (sayı verilmiyor) | [Li-Luo-Wang-Wei](https://drops.dagstuhl.de/storage/00lipics/lipics-vol354-aft2025/html/LIPIcs.AFT.2025.11/LIPIcs.AFT.2025.11.html) |
| Binance 2024 listelemeleri (32 token): medyan 1 gün +%1, 30 gün +%2,9, 6 ay **−%60** (pozitif oran %9,5) | [SEKTÖR], 31.10.2024 | [Four Pillars](https://research.4pillars.io/en/research/binance-listing-flash-or-fade) |
| Binance'te 1–2 gün yükseliş, 7. güne kadar sönüyor; Bybit'te "söylentide al, haberde sat" | [SEKTÖR], ~2025 | [RockawayX](https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex) |
| 2025 TGE'leri (118 token): %84,7'si TGE altında; medyan FDV −%71; ≥1 milyar $ FDV ile açılan 28 tokenın hiçbiri yeşil değil; 25–200 milyon $ FDV'de %40 yeşil | [SEKTÖR], 2025 | [The Defiant / Memento](https://thedefiant.io/news/research-and-opinion/token-launches-with-low-fdvs-vastly-outperformed-hyped-debuts-in-2025-memento-research) |
| Zayıf açılan 10 tokendan yalnız 1'i toparlandı (~%85 açılış altında) | [SEKTÖR], 2025 | [The Defiant / Arrakis](https://thedefiant.io/only-1-in-10-weak-token-launches-recovered-in-2025-arrakis) |
| Upbit duyurusundan sonra fiyat genelde ~2 saatte zirve yapıp düşüyor | [MEDYA] gözlem, kontrollü test yok | [ChainCatcher](https://chaincatcher.com/en/article/2068840) |

Not: Memento, DWF, Arrakis rakamları aynı 2025 kuşağına ait. Bağımsız kanıt sayılmaz. DWF bir piyasa yapıcı, çıkar çatışması var.

### Pump-and-dump

| Bulgu | Tür, tarih | Kaynak |
|---|---|---|
| Hedef coinlerin %71'i <20 milyon $ piyasa değerli; pompa dakikalar sürer, fiyat birkaç saatte başa döner | [HAKEMLİ], ACM TOIT 2023 | [La Morgia vd.](https://arxiv.org/html/2105.00733v2) |
| Piyasa alım emri patlamasıyla ~25 saniyede tespit, F1 %94,5 | [HAKEMLİ], aynı çalışma | [La Morgia vd.](https://arxiv.org/html/2105.00733v2) |
| Bağımsız veri setinde tespit skoru düşüyor (F1 0,79–0,83) | [ÇK], 2026 | [PumpSense](https://arxiv.org/abs/2605.09431) |
| Organizatör dışındaki katılımcıların çoğu kaybediyor | [HAKEMLİ], Review of Finance 2023 | [Dhawan & Putniņš](https://econpapers.repec.org/RePEc:oup:revfin:v:27:y:2023:i:3:p:935-975.) |
| 2024'te başlatılan tokenların ~%4,5'i pump-and-dump örüntüsü gösterdi | [SEKTÖR], ikincil aktarım, rakamlar çelişkili | [crypto.news / Chainalysis](https://crypto.news/chainalysis-over-4-5-of-all-tokens-launched-in-2024-have-pump-and-dump-traits/) |

Tespit modeli bir kaçış aracıdır, alım sinyali değil. Günlük mumda +%100'ü gören kişi çoğu zaman zirveyi kaçırmıştır.

### Kilit açılımları
16.000'den fazla açılımın **%90'ı** fiyata negatif baskı yapıyor. Düşüş açılımdan ~30 gün önce başlıyor. Ekip açılımlarında ~−%25 ([Keyrock](https://keyrock.com/from-locked-to-liquidity-what-16000-token-unlocks-teach-us/), [SEKTÖR], 2024). Yaklaşan büyük açılım bir alım işareti değil, kaçınma işareti.

### Momentum ve geri dönüş

| Bulgu | Tür | Kaynak |
|---|---|---|
| 1–4 haftalık momentum, haftalık brüt %2,5–4,1 | [HAKEMLİ], Journal of Finance 2022 | [Liu-Tsyvinski-Wu](https://www.nber.org/papers/w25882.pdf) |
| ~2 haftaya kadar momentum, ~1 ay sonra güçlü geri dönüş | [HAKEMLİ], J. Alternative Investments 2023 | [Dobrynskaya](https://www.hse.ru/en/news/research/559533243.html) |
| Haftalık geri dönüş küçük ve sığ coinlerde | [ÇK], 2023 | [Fičura](https://ideas.repec.org/p/prg/jnlwps/v5y2023id5.003.html) |
| MAX etkisi (en büyük günlük getiri) için bulgular çelişkili | [HAKEMLİ], IRFA 2021; Financial Innovation 2021 | [Li-Urquhart vd.](https://centaur.reading.ac.uk/99101), [Springer](https://link.springer.com/10.1186/s40854-021-00291-9) |

Bu çalışmalar yerleşik coinlerde, haftalık portföyle, brüt getiriyle yapıldı. Yeni ve sığ tokenda tek +%100 günü kovalamaya genellenemez.

**Açık boşluk:** "yeni tokenda +%100 gününden sonra ne olur" sorusunu doğrudan ölçen bir çalışma bulunamadı. OI/fonlama, sosyal hacim, balina akışı için örneklem dışı test edilmiş isabet oranı da bulunamadı. Bu yüzden kendi ölçümümüzü yaptık.

## 4. Kendi ölçümümüz: 759 tokenda +%100 günü nadir ve sonrası düşüş

### Veri ve yöntem [ÖLÇÜM, 8 Kasım 2026]
- Kaynak: Binance kamu veri aynası (data-api.binance.vision), OKX v5, Gate v4 açık API'leri. Günlük USDT spot mumları.
- Evren: 1 Ocak 2024 – 30 Eylül 2026 arası listelenen **759 token**, 454.984 token-gün. Seriler 7 Kasım 2026'da kesildi.
- Dışlananlar: tokenlaşmış hisseler, kaldıraçlı, sabit/sarılı tokenlar, 2024 öncesi listelemesi olanlar (812 sembol).
- Liste günü = üç borsadaki en erken günlük mum.
- **Hayatta kalma yanlılığı:** OKX ve Gate API'leri delist edilen çiftleri göstermiyor. Batan tokenlar örneklemde yok. Gerçek tablo aşağıdakinden daha kötüdür.

### S1. Liste günü kapanışından alıp tutmak

| Ufuk | n | Medyan | % pozitif | % < −%50 | % > +%100 |
|---|---|---|---|---|---|
| 7 gün | 759 | −%14,4 | %33,9 | %11,2 | %5,0 |
| 30 gün | 759 | −%29,8 | %29,4 | %30,8 | %7,4 |
| 90 gün | 731 | −%52,5 | %19,4 | %52,9 | %5,5 |
| 180 gün | 714 | −%67,5 | %16,0 | %65,3 | %6,7 |

Tipik yeni token 6 ayda değerinin üçte ikisini kaybediyor. Binance'te listelilerde 180 gün medyanı −%63,3. Ortalama yanıltıcı: %5–8'lik dev kazananlar ortalamayı yukarı çekiyor.

### S2. +%50 ve +%100 günleri ne sıklıkta, ne zaman

| Ölçü | +%50 günü | +%100 günü |
|---|---|---|
| İlk 90 günde en az bir kez yaşayan token | %36,4 | %11,1 |
| Tüm geçmişte en az bir kez yaşayan token | %71,1 | %32,3 |
| Toplam olay | 1.692 | 407 |
| Binance'te listeli tokenlarda (tüm geçmiş) | %52,0 | %14,5 |
| Yalnız OKX/Gate'te (tüm geçmiş) | %75,9 | %36,7 |

| Listeden gün | +%50 / 1.000 token-gün | +%100 / 1.000 token-gün |
|---|---|---|
| 1 | 50,1 | 18,4 |
| 2–3 | 22,4 | 7,3 |
| 4–7 | 19,4 | 4,3 |
| 8–14 | 10,4 | 1,9 |
| 15–30 | 6,8 | 1,2 |
| 31–90 | 4,3 | 0,8 |
| 91–365 | 3,7 | 0,9–1,0 |
| 366+ | 2,7 | 0,7 |

Olasılık ilk iki haftada yüksek, sonra günde ~%0,1'e iniyor. Gün sayısı çok olduğu için +%100 olaylarının **%76'sı 90. günden sonra** oluyor. Büyük günlük patlamalar ağırlıkla küçük, Gate merkezli tokenlarda.

### S3. +%100 gününden sonra ne oluyor

Giriş: olaydan sonraki günün açılışı.

| Tutma | n | Medyan | % pozitif | En kötü %10 | En iyi %10 |
|---|---|---|---|---|---|
| 1 gün | 406 | **−%16,3** | %28,6 | −%49,7 | +%34,8 |
| 3 gün | 404 | −%27,0 | %25,2 | −%61,5 | +%48,5 |
| 7 gün | 402 | **−%35,0** | %22,1 | −%68,9 | +%50,1 |
| 30 gün | 383 | **−%49,5** | %16,2 | −%81,9 | +%37,4 |

Karşılaştırma:
- Aynı evrende rastgele bir günden 30 gün tutma: medyan **−%11,1**.
- +%50–100 günlerinden sonra 30 gün: medyan −%32,5.
- Listeden ≤30 gün içindeki +%100 günleri, 30 gün sonra: medyan −%55,4 (n=62).
- +%100 günlerinin **%24,6'sında** ertesi gün kazancın tamamı geri veriliyor.
- Olay günlerinin yarısında hacim 420 bin $'ın altında. Piyasa çok ince.

### S4. Öncü sinyaller: eğitim ve test

Eşikler eğitim yarısında (listeleme < 1 Temmuz 2025; 478 token) seçildi. Test yarısına bakılmadan dosyaya, zaman damgası ve sha256 ile kaydedildi. Sonra test yarısında (listeleme ≥ 1 Temmuz 2025; 281 token) sınandı. Hedef: ertesi gün +%100. Test tabanı **%0,12**.

| Sinyal (t−1 kapanışında bilinir) | Eğitim lift | Test P(+%100) | Test lift | Yakaladığı olay payı |
|---|---|---|---|---|
| Önceki gün getirisi ≥ +%11,5 | 4,91 | **%0,64** | **5,36** | %29 |
| Hacim oranı ≥ 1,85 (dün / önceki 7 gün) | 2,82 | %0,32 | 2,68 | %31 |
| Aralık genişlemesi ≥ 1,86 (son 3 gün / önceki 10 gün) | 3,15 | %0,27 | 2,29 | %23 |
| Aralık VE hacim | 4,94 | %0,56 | 4,72 | %17 |
| Listeden ≤ 39 gün | 2,46 | %0,22 | 1,89 | %22 |

Lift'ler eğitimden teste korunuyor. Veri madenciliği artefaktı değil. Ama mutlak olasılık %1'in altında.

"Sıkışmadan patlama" desteklenmiyor. Olaydan önce mum aralığı daralmıyor, **genişliyor** (medyan 1,18; olay dışı günlerde 0,89).

Sinyal gününde alım (test yarısı, sinyal günü açılışında al):

| Sinyal | Tutma | n | Medyan | % pozitif |
|---|---|---|---|---|
| Önceki gün ≥ +%11,5 | 1 gün | 4.877 | −%3,6 | %36,7 |
| Önceki gün ≥ +%11,5 | 7 gün | 4.810 | **−%9,7** | %33,3 |
| Aralık VE hacim | 7 gün | 3.159 | −%5,6 | %34,7 |
| TABAN (tüm günler) | 7 gün | 89.326 | **−%2,9** | %38,4 |

Sinyal, patlama ihtimaliyle birlikte geri dönüş riskini de büyütüyor. Sinyal gününde almak tabandan kötü.

## 5. Ritual tipik +%100 tokenına benzemiyor

| Ölçü (7 Kasım kapanışı) | Ritual | +%100 günleri içinde yüzdelik | Tipik +%100 günü |
|---|---|---|---|
| Listeden beri gün | 12 | 8. | 263 |
| Önceki gün getirisi | **+%28,6** | 88. | +%0,4 |
| Hacim oranı (vr1) | 1,79 (eşik 1,85, kapalı) | 70. | 1,04 |
| Aralık oranı | 0,97 (eşik 1,86, kapalı) | 39. | 1,18 |
| Gate kapanış zirvesinden uzaklık | −%5,2 | 94. | −%92,2 |

[ÖLÇÜM, 8 Kasım 2026]. Not: CMC'nin ATH'si 0,09 $ (Coinbase, 26.10). MEXC'te açılış iğnesi 0,25 $. Bunlar dahil edilirse Ritual zirveden %55–90 aşağıda. Gate kapanışları ise 27.10'dan başladığı için zirveye yakın görünüyor.

Ritual'da 7 Kasım akşamı açık olan sinyaller: "önceki gün ≥ +%11,5" ve "listeden ≤ 39 gün". Bu tip bir günün +%100 ile bitme olasılığı testte **~%0,6**, +%50 ile bitme olasılığı ~%2,5. Hareketin büyüklüğü de nadir: +%99,9'luk günlük getiri, ilk 30 günün token-günlerinin yalnız **%0,27'sinde** aşıldı. Ritual, "ilk iki hafta" yüksek riskli bölgesinde (gün 8–14'te 1.000 token-günde ~1,9 adet +%100).

Ritual 8 Kasım'ı +%100 kapanışla bitirirse S3 dağılımına girer: tarihsel medyan 1 günde −%16, 30 günde −%49. Bu Ritual için bir tahmin değil. Geçmiş olayların dağılımı.

## 6. Pratik sonuç: kovalamak neden kaybettiriyor

### Neden zarar ettiriyor
- **Zamanlama:** Listeleme primi dakikalar-saatler içinde fiyatlanıyor [HAKEMLİ, La Morgia vd.; MEDYA, Upbit gözlemi]. Ekranda +%100'ü gördüğünüzde hareketin çoğu bitmiş.
- **Geri dönüş:** +%100 gününden sonra medyan 30 günde −%49 [ÖLÇÜM].
- **Taban oran:** Yeni tokenların çoğu zaten düşüyor. 180 günde medyan −%67,5 [ÖLÇÜM]; 2025 TGE'lerinin %84,7'si TGE altında [SEKTÖR].
- **İnce piyasa:** Olayların yarısında günlük hacim 420 bin $'ın altında. Gerçek alış fiyatınız mumdaki fiyattan kötü olur [ÖLÇÜM]. Komisyon ve kayma hesaba katılmadı; gerçek sonuç daha kötü.
- **Ritual örneği:** 3 Kasım'da gün içi +%122 oldu. İki gün sonra fiyat başlangıca döndü [ÖLÇÜM].

### Yine de oynamak isteyen için
- **Olasılık:** Sinyal varken bile ertesi gün +%100 olasılığı **%1'in altında** (%0,64).
- **Beklenen sonuç:** Sinyal gününde almak 7 günde medyan −%9,7. +%100 gününden sonra almak 30 günde medyan −%49.
- **Kârlı bir koşul bulunamadı.** Ölçtüğümüz hiçbir koşulda medyan pozitif değil.
- **Boyut:** Tamamen sıfırlanmasını kabul ettiğiniz bir tutar. En kötü %10'luk dilimde 30 günde −%82'den kötü sonuç var. Bu bir piyango bileti gibi düşünülmeli.

### İzlenebilecek yapısal işaretler (hiçbiri test edilmedi)

| İşaret | Literatür ne diyor | Yön |
|---|---|---|
| Düşük FDV açılış | 25–200 milyon $ FDV'de %40 yeşil; ≥1 milyar $'da hiç yeşil yok [SEKTÖR, Memento 2025] | Kaçınma filtresi: yüksek FDV'den uzak dur |
| Düşük float | Ritual'da %18; sistematik test bulunamadı | Belirsiz |
| Yaklaşan kilit açılımı | %90 negatif, düşüş ~30 gün önce başlar [SEKTÖR, Keyrock 2024] | Satış/kaçınma işareti |
| Coinbase / Binance / Upbit listeleme duyurusu | Prim kısa; Coinbase'te daha büyük [HAKEMLİ, AFT 2025]; Upbit ~2 saatte zirve [MEDYA] | Yalnız saniye-dakika ölçeğinde; botlar önde |

Bu işaretler bizim ölçümümüzde test edilmedi. Ölçüm yalnız fiyat ve hacimle yapıldı.

## 7. Proje kuralına göre karar: İZ DEĞİL

Proje kuralı: bir iz, önceden kaydedilmiş eşiklerle, örneklem dışı testte tutmalı ve para kazandırmalıdır.

| Şart | Sonuç |
|---|---|
| Eşik önceden kaydedildi mi | Evet (eğitim yarısı, zaman damgası + sha256) |
| Lift testte tutuyor mu | Evet (4,9 → 5,4) |
| Mutlak olasılık işe yarar mı | Hayır (%0,64) |
| Sinyal gününde alım tabanı geçiyor mu | **Hayır** (7 gün medyan −%9,7, taban −%2,9) |
| +%100 sonrası alım tabanı geçiyor mu | **Hayır** (30 gün −%49, taban −%11) |

**Karar: İZ DEĞİL.** Sinyal bir oynaklık ölçüsü. Alım-satım sinyali olarak kullanılamaz. Kullanılabilecek tek tarafı savunma: "son günlerde sert yükselmiş, yeni, ince tokenı kovalama" filtresi.

## 8. Sınırlar

- api.binance.com (HTTP 451) ve Bybit (HTTP 403) erişilemedi. Binance kamu veri aynası kullanıldı.
- OKX ve Gate'ten delist edilen tokenlar örneklemde yok. Kayıplar küçümseniyor.
- MEXC, KuCoin gibi uzun kuyruk borsaları evrene alınmadı (yalnız Ritual için kullanıldı).
- Komisyon, alış-satış farkı ve kayma hesaba katılmadı.
- Lift'ler ve getiriler için güven aralığı hesaplanmadı. Test olay sayıları küçük (kural başına 7–34 olay).
- Eğitim/test ayrımı listeleme tarihine göre. Günler zamanda örtüşüyor; tam zaman dışı test değil.
- Olaylar aynı tokenlarda kümeleniyor (406 olay, 245 token).
- Saatlik veri yalnız Ritual'da kullanıldı. Diğer tokenlarda gün içi +%100'ler sayılmadı.
- Zincir üstü veri, unlock takvimi, duyuru zamanları, fonlama/açık pozisyon serisi ölçülmedi.
- Ritual: resmi site ve X hesabı okunamadı. Coinglass, Coinalyze, saatlik vadeli verisi bulunamadı. 8 Kasım UTC günü ölçüm anında kapanmamıştı.
- Piyasa değeri kırılımı yapılmadı.

## 9. Kaynaklar

**Hakemli**
- La Morgia vd., "The Doge of Wall Street", ACM TOIT 2023: https://arxiv.org/html/2105.00733v2
- Dhawan & Putniņš, Review of Finance 2023: https://econpapers.repec.org/RePEc:oup:revfin:v:27:y:2023:i:3:p:935-975.
- Li, Luo, Wang, Wei, "Cryptocurrency Exchange Listings", AFT 2025: https://drops.dagstuhl.de/storage/00lipics/lipics-vol354-aft2025/html/LIPIcs.AFT.2025.11/LIPIcs.AFT.2025.11.html
- Liu, Tsyvinski, Wu, Journal of Finance 2022: https://www.nber.org/papers/w25882.pdf
- Dobrynskaya, J. Alternative Investments 2023: https://www.hse.ru/en/news/research/559533243.html
- Li, Urquhart, Wang, Zhang, IRFA 2021: https://centaur.reading.ac.uk/99101 ; Financial Innovation 2021: https://link.springer.com/10.1186/s40854-021-00291-9

**Çalışma kağıdı**
- Ante 2019: https://www.blockchainresearchlab.org/de/2019/09/10/market-reaction-to-exchange-listings-of-cryptocurrencies-2/
- Fičura 2023: https://ideas.repec.org/p/prg/jnlwps/v5y2023id5.003.html
- PumpSense 2026: https://arxiv.org/abs/2605.09431

**Sektör**
- Four Pillars, 31.10.2024: https://research.4pillars.io/en/research/binance-listing-flash-or-fade
- RockawayX (~2025): https://rockawayx.com/insights/bullish-or-bearish-what-really-happens-when-tokens-list-on-a-cex
- Memento (The Defiant, 2025): https://thedefiant.io/news/research-and-opinion/token-launches-with-low-fdvs-vastly-outperformed-hyped-debuts-in-2025-memento-research
- Arrakis (The Defiant, 2025): https://thedefiant.io/only-1-in-10-weak-token-launches-recovered-in-2025-arrakis
- Keyrock, açılımlar (2024): https://keyrock.com/from-locked-to-liquidity-what-16000-token-unlocks-teach-us/
- Chainalysis 2025 (ikincil): https://crypto.news/chainalysis-over-4-5-of-all-tokens-launched-in-2024-have-pump-and-dump-traits/

**Borsa**
- KuCoin blog, Ritual tokenomik (27.10.2026): https://www.kucoin.com/blog/ritual-mainnet-ritual-tokenomics-airdrop
- KuCoin listeleme duyurusu (28.10.2026): https://www.kucoin.com/news/flash/kucoin-launches-ritual-ritual-listing-campaign-with-2-3m-ritual-giveaway

**Medya ve sosyal**
- Phemex (27.10.2026): https://phemex.com/news/article/ritual-launches-ai-layer-1-mainnet-and-ritual-token-price-dives-72-from-high-101259
- Crypto Briefing, Coinbase (26.10.2026): https://cryptobriefing.com/coinbase-enables-ritual-token-spot-trading/
- The Block (08.11.2023): https://www.theblock.co/news/deals/2023-11-08-decentralized-ai-compute-platform-ritual-closes-25-million-fundraise-262114
- ChainCatcher, Upbit gözlemi: https://chaincatcher.com/en/article/2068840
- KuCoin Square (07.11.2026, sosyal): https://www.kucoin.com/square/post/content_6aef423d760f86000742ab29

**Veri toplayıcı (08.11.2026)**
- CoinMarketCap: https://coinmarketcap.com/currencies/ritual/
- CoinGecko: https://www.coingecko.com/en/coins/ritual

**Kendi ölçüm (borsa API'leri, 8 Kasım 2026)**
- Binance veri aynası: https://data-api.binance.vision/api/v3/klines ve /exchangeInfo
- OKX: https://www.okx.com/api/v5/market/history-candles ve /public/instruments
- Gate: https://api.gateio.ws/api/v4/spot/candlesticks ve /spot/currency_pairs
- Ritual: Gate günlük/saatlik https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1h&limit=400 ; MEXC https://api.mexc.com/api/v3/klines?symbol=RITUALUSDT&interval=1d&limit=60
- Kod ve ara çıktılar: /tmp/claude-0/-home-user-col-yolu/2d897341-a66f-57df-ba5e-2bfd9dd60c3c/scratchpad/kripto/ (indir.py, panel.py, olc.py, esikler.json, esikler_onkayit_*.json)
