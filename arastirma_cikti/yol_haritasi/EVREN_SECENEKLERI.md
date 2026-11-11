# Batanlar dahil ABD evreni: seçenek notu (11 Kasım 2026)

Amaç: K59 aylık portföy testleri (2016–2026) için borsadan çıkanları son getirileriyle içeren evren. Ölçüm yapılmadı, fiyat indirilmedi.

## 1. Eldeki durum

| Kalem | Sayı | Nerede |
|---|---|---|
| V_ABD (yalnız yaşayanlar) | 1.410 | islenmis-veri, veri/ |
| K34 Yahoo (nakdi biten, yalnız yaşayanlar) | 2.246 (K54 evreninde 1.435) | veri2/ |
| K34: bugün kodu olmayan şirket (2021–26) | 1.303 (306 işlem görmüyor, 173 Tiingo'da eşleşmedi, 824 geçerli) | k34/k34_eski_kod.csv |
| Tiingo'dan fiyatı inen (Ekim kotası) | 450; K54 evrenine giren 422 | fiyat repoda YOK (lisans); liste k34/k34_orneklem.csv |
| K54 sınıfları (Ç137, 3.267 sembol) | 3.001 yaşayan, 159 birleşme, 79 belirsiz, 19 iflas, 9 kod yeniden kullanımı | K54_SIRKET_DURUMU.csv |
| EVREN2 adayı (Ç142) | 490 (199 K34 kalanı + 291 Tiingo listesinden 2016–21 biten; havuz 1.795) | k56_mekanizma/evren_v2/ |
| Tiingo listesinde 2016 – Ağu 2026 biten adi hisse biçimli borsa sembolü | 4.010 (serisi ≥ 465 gün: 3.342) | k55/supported_tickers.csv (29 Eki) |

Önemli:
- K54'teki 266 çıkışın hepsi Tiingo serisinden; V_ABD ve Yahoo'da çıkış 0. Bu oturumda batan fiyatı sıfır.
- .env yok, ortamda TIINGO_TOKEN yok (yalnız ad tarandı). EVREN2 günlüğünde Tiingo isteği 0: 490 aday inmedi.
- 450 Tiingo csv'si Drive'da ad aramasında bulunamadı; yeniden inmesi gerekir.
- 2016–2020 batan kimliği yalnız Tiingo listesinde; SEC finansal özeti 2021'de başlıyor.

## 2. Kaynaklar (Kasım 2026)

| Kaynak | Ücret | Batan kapsamı | Lisans / repo | İş yükü |
|---|---|---|---|---|
| Tiingo ücretsiz | 0 $ | var (projede sınandı), 30+ yıl | yalnız iç kullanım; repoya konmaz | kod hazır; 50 istek/saat, 1.000/gün, 500 sembol/ay |
| Tiingo Power | 30 $/ay | aynı | aynı | kod hazır; 10.000 istek/saat, 110.485 sembol/ay |
| EODHD | 19,99 $/ay (ücretsiz: 20 istek/gün, 1 yıl) | 26.000+ ABD sembolü, çoğu 2000'den | kişisel; depolama şartı doğrulanamadı | yeni indirici + kod eşleme |
| Massive (eski Polygon) | 0 / 29 / 79 / 199 $ | pasif semboller her planda | bireysel | ücretsizde ~2 yıl geçmiş (3. taraf bilgisi); yeni indirici |
| Alpha Vantage | 0 $ (25 istek/gün); 49,99 $/ay | liste var, fiyat kapsamı doğrulanamadı | — | elverişsiz |
| Sharadar SEP (Nasdaq Data Link) | fiyat açık değil (giriş gerekli) | var, 1998'den | kişisel lisans | yeni indirici |
| Norgate Platinum | ~630–790 $/yıl (kaynaklar çelişkili) | var, 1990'dan | abonelik bitince erişim biter | Colab'a uymaz |
| Yahoo, Stooq | 0 $ | YOK (27 Eki sınaması: SIVB, FRC, WEWK boş) | — | — |
| SEC (8-K 1.03, 25-NSE) | 0 $ | kimlik ve tarih var, FİYAT YOK | kamu verisi | kod hazır (K54, K56) |

## 3. Üç seçenek (ucuzdan pahalıya)

| # | Seçenek | Para | Süre ve istek | Cemal'den gereken |
|---|---|---|---|---|
| 1 | Yaklaşık sınır, yeni fiyat yok | 0 $ | 3–4 saat ajan; SEC'e ~60 arama + ~4.000 başvuru özeti (~15 dk) | yalnız SEC e-postası (SEC_EPOSTA) |
| 2 | Tiingo ücretsiz | 0 $ | 490 aday = 980 istek ≈ 22 saat, bir ayın kotası; 450 K34 serisi yeniden +1 ay; 2.000 isim 4 ay; 3.342 + 450 isim 8 ay | "Tiingo anahtarını .env'e koy" (TIINGO_TOKEN) |
| 3 | Tiingo Power, tek ay | 30 $ | 3.342 + 450 isim ≈ 7.600 istek, indirme 1 saatten kısa; kimlik doğrulama + evren v2 ~1 gün ajan | hesabı Power'a yükselt, anahtarı .env'e koy, ay sonunda iptal et |

Seçenek 1: Tiingo listesi + 25-NSE + 8-K 1.03 ile her yıl bitenler K54 kuralıyla sınıflanır; iflas −%100, birleşme ek kayıp 0 (son fiyat ≈ anlaşma bedeli), belirsiz −%30 / −%100. Sınırı: fiyatı olmayan şirket sinyalle seçilemez; çıktı düzeltilmiş getiri değil, K59'a eklenen "en kötü durum" bandıdır (yıllık iflas payı × −%100). K56 ön kaydı "delist getirisi uydurulmaz" der; bant ayrı ön kayıtla, bilgi olarak yazılır.

Öneri: 1 hemen; kalıcı çözüm 3 (30 $, Kasım'da biter, mevcut kod çalışır); ödeme istenmezse 2. İnen csv'ler Drive'da zip olarak saklanır, repoya konmaz.

## 4. Hangi sinyal ailesi ne kadar açık

| Aile | Açıklık | Dayanak |
|---|---|---|
| Küçüklük | ÇOK YÜKSEK | Shumway ve Warther (1999): Nasdaq'ta eksik çıkış getirisi −%55; düzeltilince küçüklük etkisi kalmıyor. Proje K34: etki üçte bir eriyor. |
| Momentum | ORTA (al-sat'ta yüksek, yalnız alımda düşük) | Eisdorfer (2008): momentum kârının ~%40'ı çıkan şirketlerden, çoğu iflas eden kaybedenlerden (satış bacağı). |
| Kârlılık | DÜŞÜK (alım bacağı) | Beaver, McNichols, Price (2007): çıkışlar ölçünün en alt onda birinde yığılır; çıkış getirisi eklenince kazanç ve nakit akışı stratejileri güçlenir. |
| PEAD | DÜŞÜK | Doğrudan kaynak bulunamadı; aynı mantık (çıkanlar kötü haber ucunda). K54: delist bandı P1 / P2'yi 4 ondalıkta oynatmadı. |
| Düşük ihraç | DÜŞÜK (alım bacağı) | Çıkarım: çok ihraç edenler nakdi biten küçüklerdir; K34'te bunların 1.303 / 3.564'ünün (%37) bugün kodu yok. |

K59 için anlamı:
- En açık: geniş Yahoo evreni (K34 Yahoo = nakdi bitip hayatta kalanlar) ve eşit ağırlıklı, küçük şirkete yaslanan portföyler.
- Kıyas (evren ortalaması) da yaşayanlarla şişer; kârlı / az ihraç eden portföylerin farkı olduğundan küçük görünebilir.
- V_ABD daha az açık, ama hiç batan içermez.

## Kaynaklar (erişim 11 Kasım 2026)

- Tiingo fiyat ve sınırlar: https://www.tiingo.com/about/pricing
- EODHD fiyat: https://eodhd.com/pricing ; batan kapsamı: https://eodhd.com/financial-academy/financial-faq/historical-stock-prices-for-delisted-companies
- Massive pasif semboller: https://massive.com/knowledge-base/article/what-does-polygon-do-with-delisted-tickers ; fiyat: https://massive.com/pricing
- Alpha Vantage: https://www.alphavantage.co/premium/
- Sharadar: https://www.quantrocket.com/pricing/data/sharadar
- Norgate: https://norgatedata.com/stockmarketpackages.php
- Yahoo sınırı: https://marketparquet.com/guides/yfinance-limitations-backtesting
- Shumway (1997): https://ideas.repec.org/a/bla/jfinan/v52y1997i1p327-40.html
- Shumway ve Warther (1999): https://ideas.repec.org/a/bla/jfinan/v54y1999i6p2361-2379.html
- Eisdorfer (2008): https://ideas.repec.org/a/eee/finmar/v11y2008i2p160-179.html
- Beaver, McNichols, Price (2007): https://ideas.repec.org/a/eee/jaecon/v43y2007i2-3p341-368.html
- Proje: IZ_KARNE Ç107, Ç137, Ç142; islenmis-veri BENIOKU.md
