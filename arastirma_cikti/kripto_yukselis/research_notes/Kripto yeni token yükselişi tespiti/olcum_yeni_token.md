# Yeni listelenen kripto tokenlarda +%50 / +%100 günlük hareketler: borsa verisiyle ölçüm (8 Kasım 2026 itibarıyla)

Bütün sayılar bu çalışmada borsaların açık API'lerinden indirilen günlük OHLCV ile Python'da hesaplandı; makale rakamı yok. Kodlar ve ham veri: /tmp/claude-0/-home-user-col-yolu/2d897341-a66f-57df-ba5e-2bfd9dd60c3c/scratchpad/kripto/ (indir.py, panel.py, olc.py; ham yanıtlar data/ altında, Python -I ile okundu). Ara çıktılar aynı klasörde: sonuc_temel.md, sonuc_s4.md, sonuc_ek.md, sonuc_ritual.md, evren_ham.csv, dislanan.csv, esikler.json (+ esikler_onkayit_*.json).

## S1 — Liste günü kapanışından gün 7 / 30 / 90 / 180 kapanışına getiri dağılımı

### Takeaway
759 yeni tokenda (2024-01-01 – 2026-09-30 arası listelenen, USDT spot) liste günü kapanışından sonra tipik yol aşağı: medyan getiri gün 7'de −%14, gün 30'da −%30, gün 90'da −%53, gün 180'de −%68; 180 günde tokenların %65'i −%50'nin altında, yalnız %16'sı artıda, %6,7'si +%100'ün üstünde. Bu rakamlar hayatta kalanlara dayanıyor (Gate/OKX'ten delist edilenler API listesinde yok), yani gerçek tablo daha da kötüdür.

### Cited Findings

#### Veri kaynağı ve erişim (tüm sorular için)
- api.binance.com HTTP 451 döndü ("Service unavailable from a restricted location"), Bybit HTTP 403 (CloudFront ülke engeli). Erişilebilen ve kullanılanlar: Binance kamu veri aynası data-api.binance.vision, OKX v5, Gate v4. RITUAL için ek olarak MEXC ve KuCoin. — [Binance data-api klines](https://data-api.binance.vision/api/v3/klines), [Binance exchangeInfo](https://data-api.binance.vision/api/v3/exchangeInfo), [OKX instruments](https://www.okx.com/api/v5/public/instruments?instType=SPOT), [OKX history-candles](https://www.okx.com/api/v5/market/history-candles), [Gate currency_pairs](https://api.gateio.ws/api/v4/spot/currency_pairs), [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)
- İndirilen evren listeleri: Binance 775 USDT çifti (518 TRADING, 257 BREAK = delist); OKX 466 USDT çifti (yalnız 'live'); Gate 2.039 USDT çifti (yalnız güncel listede olanlar). İlk mumu pencere içinde olan çift sayısı: Binance 281 (272 TRADING + 9 BREAK), OKX 245, Gate 1.323. — [Binance exchangeInfo](https://data-api.binance.vision/api/v3/exchangeInfo), [OKX instruments](https://www.okx.com/api/v5/public/instruments?instType=SPOT), [Gate currency_pairs](https://api.gateio.ws/api/v4/spot/currency_pairs)
- Binance delist (BREAK) çiftlerin geçmiş mumlarını hâlâ veriyor (örnek WAVESUSDT 2019 mumları döndü); OKX ve Gate listeleme uçları delist edilen çiftleri hiç göstermiyor, dolayısıyla bu iki borsada delist edilen tokenlar örneklemde YOK (hayatta kalma yanlılığı). Örneklemde serisi 7 Kasım'dan önce biten yalnız 3 token var (hepsi Binance BREAK). — [Binance klines WAVESUSDT](https://data-api.binance.vision/api/v3/klines?symbol=WAVESUSDT&interval=1d&startTime=0&limit=2)

#### Yöntem (tüm sorular için)
- Token = taban sembol (base). Üç borsadaki bütün listelemeleri birleştirildi; tokenın liste günü = üç borsa arasındaki en erken ilk günlük mum (UTC). Daha erken (2024 öncesi) bir listeleme varsa ve ortak günlerde kapanış oranı 0,67–1,5 arasındaysa (aynı token) token "yeni değil" sayılıp dışlandı; fiyatlar tutmuyorsa (aynı ticker, farklı token) ayrı token kabul edildi. Ana seri = en erken listelenen borsanın serisi (eşitlikte Binance > OKX > Gate). Ana seri dağılımı: Gate 625, Binance 105, OKX 29; 152 token Binance'te de listeli. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks), [Binance data-api klines](https://data-api.binance.vision/api/v3/klines), [OKX history-candles](https://www.okx.com/api/v5/market/history-candles)
- Gate'te buy_start'tan önceki mumlar çoğu zaman ön-piyasa (pre-market) fiyatı; buy_start'tan ≤120 gün önce başlayan mumlar ya da buy_start ±3 gün içinde ≥5 kat kırılma gösterenler kesildi (ör. HYPE, BLUM, HMSTR ön-piyasa artefaktları). buy_start'tan çok daha eski mumu olan Gate çiftleri (sıfırlanmış buy_start, yeniden listeleme) eski token sayıldı. — [Gate currency_pairs](https://api.gateio.ws/api/v4/spot/currency_pairs)
- Dışlananlar (812 base): Gate adı kaldıraçlı/xStock/Ondo/staked/wrapped/gold/dollar içeren 466; tokenlaşmış hisse ve pre-IPO tokenları 207 (2026'da Binance '…B', OKX 'X…', Gate '…G' sonekli hisse dalgası, elle gözden geçirildi) + 5 Ondo sepeti; düşük oynaklık/pegli (günlük log getiri std < %2) 65; 2024 öncesi listelemesi olan 41; stabil/sarılı 16; ticker değişimi 5 (AWE←STPT, SKY←MKR, D←DAR, PDA←PLA, TON=Toncoin); önekli kopya 3 (1000CAT, 1000CHEEMS, 1MBABYDOGE); fiyat ölçeği hatası 2 (LF, AARK: tek günde >100 kat); kaldıraçlı 2 (PENGU3L/3S). 30 mumdan az kalan olmadı (en kısa seri 39 gün). — [Gate currency_pairs](https://api.gateio.ws/api/v4/spot/currency_pairs), [Binance exchangeInfo](https://data-api.binance.vision/api/v3/exchangeInfo)
- Son evren: 759 token (liste yılı 2024: 328, 2025: 327, 2026 Oca–Eyl: 104), 454.984 token-gün (gün ≥1, kapanış-kapanış getirisi tanımlı), seriler 7 Kasım 2026 kapanışında kesildi. "Likit" alt grup = gün 1–30 medyan USDT işlem hacmi ≥ 250.000 olan 499 token. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)
- Getiri = gün h kapanışı / liste günü (ilk mum) kapanışı − 1; gün h'de mum yoksa en fazla 3 gün önceki kapanış. "ort_w" = %1/%99 kırpılmış ortalama (tek tük >10 kat hareketler ham ortalamayı bozuyor). — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

#### Tablo S1 (n = ufku 7 Kasım 2026'ya ulaşan token sayısı)

| Grup | Ufuk | n | Medyan | Ortalama | Ort. (kırpılmış) | % pozitif | % < −%50 | % > +%100 | p10 | p90 |
|---|---|---|---|---|---|---|---|---|---|---|
| Hepsi | 7 | 759 | −14,4% | +1,3% | −1,9% | 33,9% | 11,2% | 5,0% | −51,9% | +51,4% |
| Hepsi | 30 | 759 | −29,8% | −1,5% | −8,9% | 29,4% | 30,8% | 7,4% | −73,9% | +70,4% |
| Hepsi | 90 | 731 | −52,5% | −29,6% | −31,8% | 19,4% | 52,9% | 5,5% | −87,3% | +41,3% |
| Hepsi | 180 | 714 | −67,5% | −35,4% | −36,5% | 16,0% | 65,3% | 6,7% | −94,4% | +46,9% |
| Binance'te listeli | 7 | 152 | −14,2% | +16,3% | +5,7% | 33,6% | 5,3% | 6,6% | −41,3% | +59,5% |
| Binance'te listeli | 30 | 152 | −27,1% | +21,9% | +8,5% | 31,6% | 25,7% | 7,2% | −68,7% | +56,6% |
| Binance'te listeli | 90 | 150 | −49,6% | −29,6% | −33,1% | 20,7% | 49,3% | 2,7% | −80,9% | +24,1% |
| Binance'te listeli | 180 | 149 | −63,3% | −39,5% | −40,5% | 14,8% | 64,4% | 5,4% | −87,6% | +20,2% |
| Yalnız OKX/Gate | 90 | 581 | −54,9% | −29,7% | −31,2% | 19,1% | 53,9% | 6,2% | −89,8% | +48,5% |
| Yalnız OKX/Gate | 180 | 565 | −68,9% | −34,4% | −35,5% | 16,3% | 65,5% | 7,1% | −95,2% | +55,0% |
| Likit | 30 | 499 | −26,4% | +6,6% | −2,4% | 33,3% | 28,1% | 9,0% | −69,6% | +85,5% |
| Likit | 180 | 470 | −66,7% | −29,5% | −30,8% | 18,7% | 63,8% | 8,1% | −93,5% | +70,4% |
| Liste < 2025-07 | 180 | 478 | −64,7% | −35,6% | −36,2% | 16,5% | 63,2% | 6,3% | −93,4% | +51,1% |
| Liste ≥ 2025-07 | 180 | 236 | −71,8% | −35,2% | −35,5% | 14,8% | 69,5% | 7,6% | −95,7% | +36,2% |

- Delist edilen 3 token son kapanışla dahil edildiğinde sonuç değişmiyor (gün 180 medyan −%67,5, n=712). — [Binance data-api klines](https://data-api.binance.vision/api/v3/klines)

### Inferences
- Liste günü kapanışından alıp tutmak, tipik yeni token için 3–6 ayda yarıdan fazla değer kaybı demek; sağ kuyruk (%5–8'i +%100 üstü) ortalamayı medyandan çok yukarı çekiyor, yani "ortalama" yanıltıcı.
- Binance'te listeli tokenlarda sol kuyruk biraz daha ince (gün 7'de −%50 altı %5 vs %13), ama 90–180 günde medyan kayıp neredeyse aynı.
- 2025-07 sonrası listelenenler 90–180 günde daha kötü (medyan −%61 / −%72); bu dönem etkisi de olabilir (2026'nın ikinci yarısı).

### Gaps
- OKX ve Gate'ten delist edilmiş tokenlar API listelerinde yok; bu yüzden S1 bir hayatta kalanlar örneklemidir ve kayıplar küçümsenmektedir. Gate'in delist ettiği çift sayısı bilinmiyor.
- Bybit (403) ve api.binance.com (451) erişilemedi; MEXC/KuCoin gibi uzun kuyruk borsaları evrene alınmadı (yalnız RITUAL için kullanıldı). Liste günü = bu üç borsadaki ilk mum; token daha önce başka bir borsada işlem görmüş olabilir.
- Piyasa değeri (CoinGecko) eklenmedi; büyüklüğe göre kırılım yok.

## S2 — İlk 90 günde ve tüm geçmişte en az bir +%50 / +%100 kapanış-kapanış günü olan token sayısı; bu günler listeden kaç gün sonra olur

### Takeaway
759 tokenın %36'sı ilk 90 günde en az bir +%50 gün, %11'i en az bir +%100 gün yaşadı; tüm geçmişte bu oranlar %71 ve %32. Olay olasılığı listeden hemen sonra en yüksek (gün 1'de 1000 token-günde 18 adet +%100) ve ilk iki haftada hızla düşüp gün 30'dan sonra ~1/1000'de düzleşiyor; ama gün sayısı çok olduğu için olayların çoğu (+%100'lerin %76'sı) gün 90'dan sonra gerçekleşiyor.

### Cited Findings
- Tanım: r_t = kapanış_t / kapanış_(t−1) − 1 (UTC günlük mum, art arda iki gün varsa); +%50 olayı r ≥ 0,5, +%100 olayı r ≥ 1,0; gün 0 (liste günü) hariç. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks), [Binance data-api klines](https://data-api.binance.vision/api/v3/klines), [OKX history-candles](https://www.okx.com/api/v5/market/history-candles)

#### Tablo S2a (token sayısı ve oranı)

| Grup | Token | İlk 90 gün ≥1 kez +%50 | Tüm geçmiş +%50 | +%50 olay | İlk 90 gün ≥1 kez +%100 | Tüm geçmiş +%100 | +%100 olay | Token-gün |
|---|---|---|---|---|---|---|---|---|
| Hepsi | 759 | 276 (%36,4) | 540 (%71,1) | 1.692 | 84 (%11,1) | 245 (%32,3) | 407 | 454.984 |
| Binance'te listeli | 152 | 42 (%27,6) | 79 (%52,0) | 154 | 10 (%6,6) | 22 (%14,5) | 28 | 90.055 |
| Yalnız OKX/Gate | 607 | 234 (%38,6) | 461 (%75,9) | 1.538 | 74 (%12,2) | 223 (%36,7) | 379 | 364.929 |
| Likit | 499 | 188 (%37,7) | 345 (%69,1) | 1.025 | 55 (%11,0) | 151 (%30,3) | 247 | 292.413 |
| Liste < 2025-07 | 478 | 163 (%34,1) | 360 (%75,3) | 1.214 | 54 (%11,3) | 171 (%35,8) | 294 | 363.691 |
| Liste ≥ 2025-07 | 281 | 113 (%40,2) | 180 (%64,1) | 478 | 30 (%10,7) | 74 (%26,3) | 113 | 91.293 |

- Zamanlama: +%100 olaylarının listeden gün sayısı medyanı 249 (çeyrekler 99–421); tokenın İLK +%100 gününün medyanı 187 (çeyrekler 38–377), n=245 token. +%50 için tüm olay medyanı 232 (73–437), ilk olay medyanı 81 (12–250), n=540 token. (Tüm geçmiş uzunluğu tokenlara göre değiştiği için medyanlar uzun yaşayan tokenlara kayar; aşağıdaki tehlike oranı tablosu daha doğru okumadır.) — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

#### Tablo S2b (listeden gün kovasına göre olay sıklığı, 1000 token-günde; tüm evren)

| Gün kovası | Token-gün | +%50 olay | +%100 olay | +%50 / 1000 gün | +%100 / 1000 gün | +%50 olayların payı | +%100 olayların payı |
|---|---|---|---|---|---|---|---|
| 1 | 759 | 38 | 14 | 50,1 | 18,4 | %2,2 | %3,4 |
| 2–3 | 1.518 | 34 | 11 | 22,4 | 7,3 | %2,0 | %2,7 |
| 4–7 | 3.036 | 59 | 13 | 19,4 | 4,3 | %3,5 | %3,2 |
| 8–14 | 5.313 | 55 | 10 | 10,4 | 1,9 | %3,3 | %2,5 |
| 15–30 | 12.144 | 82 | 14 | 6,8 | 1,2 | %4,8 | %3,4 |
| 31–90 | 44.693 | 192 | 36 | 4,3 | 0,8 | %11,3 | %8,8 |
| 91–180 | 65.112 | 239 | 56 | 3,7 | 0,9 | %14,1 | %13,8 |
| 181–365 | 124.457 | 454 | 123 | 3,7 | 1,0 | %26,8 | %30,2 |
| 366+ | 197.952 | 539 | 130 | 2,7 | 0,7 | %31,9 | %31,9 |

- Likit alt grupta (499 token) aynı eğri daha dik: gün 1'de 1000 token-günde 66 adet +%50 ve 24 adet +%100; gün 8–14'te 11,7 ve 2,0; gün 31–90'da 3,9 ve 0,6. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

### Inferences
- +%100 kapanış günü, listeden sonraki ilk gün ortalama bir tokenın ~%2'sinde, ilk hafta boyunca günde %0,4–0,7'sinde, bir aydan sonra günde ~%0,1'inde görülür. "Erken dönem" etkisi ilk 2 haftayla sınırlı.
- Binance'te listeli tokenlarda +%100 gün çok daha seyrek (tüm geçmişte %14,5 vs yalnız OKX/Gate'te %36,7): büyük günlük patlamalar ağırlıkla küçük, Gate merkezli tokenların özelliği.

### Gaps
- Olaylar tek borsa (ana seri) kapanışıyla ölçüldü; ikinci borsada doğrulama sistematik yapılmadı. Ana serideki ≥10 kat ya da ≤ −%90 tek gün hareketleri (ACP, ACT, IMT, MANA3, ESPORTS, NAWS, SHM) elle doğrulanamadı; ACT (11.11.2024, Binance listelemesi günü, ~20 kat) bilinen gerçek bir olay. Bu uç değerler medyanları değil, yalnız ham ortalamaları etkiler.
- Gün içi (saatlik) +%100 hareketler sayılmadı; yalnız UTC günlük kapanışlar.

## S3 — Olay çalışması: +%100 (ve ayrıca +%50–100) günlerinden sonra getiriler

### Takeaway
+%100 kapanış gününden sonra tipik yol sert geri dönüş: ertesi gün açılıştan alınırsa medyan getiri +1 günde −%16, +3'te −%27, +7'de −%35, +30'da −%49; yalnız %16'sı 30 günde artıda, en kötü onda birlik dilim −%82'den kötü. Olay günü kapanışından almak neredeyse aynı (kripto 7/24, ertesi açılış ≈ kapanış). Aynı tokenların rastgele günlerine göre (30 günde medyan −%11) olay sonrası performans belirgin daha kötü.

### Cited Findings
- Giriş A = olay gününden sonraki günün açılışı, çıkış = gün t+k kapanışı (k=1 aynı gün kapanışı); Giriş B = olay günü kapanışı. p10 = en kötü onda birlik dilimin eşiği. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks), [Binance data-api klines](https://data-api.binance.vision/api/v3/klines), [OKX history-candles](https://www.okx.com/api/v5/market/history-candles)

#### Tablo S3a: +%100 günleri, giriş = ertesi gün açılışı

| Grup | k | n | Medyan | Ortalama | Ort. (kırpılmış) | % pozitif | % < −%50 | p10 (en kötü %10) | p90 |
|---|---|---|---|---|---|---|---|---|---|
| Tüm olaylar | 1 | 406 | −16,3% | −8,2% | −9,2% | 28,6% | 9,9% | −49,7% | +34,8% |
| Tüm olaylar | 3 | 404 | −27,0% | −10,0% | −11,6% | 25,2% | 19,6% | −61,5% | +48,5% |
| Tüm olaylar | 7 | 402 | −35,0% | −11,2% | −17,2% | 22,1% | 29,4% | −68,9% | +50,1% |
| Tüm olaylar | 30 | 383 | −49,5% | −12,3% | −21,0% | 16,2% | 48,3% | −81,9% | +37,4% |
| Tokenın ilk +%100 günü | 1 | 245 | −13,2% | −2,6% | −3,7% | 31,8% | 7,8% | −46,1% | +50,0% |
| Tokenın ilk +%100 günü | 7 | 243 | −31,5% | +0,5% | −7,1% | 25,9% | 25,9% | −65,5% | +67,5% |
| Tokenın ilk +%100 günü | 30 | 235 | −43,9% | +5,7% | −2,8% | 20,9% | 44,3% | −80,7% | +72,3% |
| Likit tokenlar | 1 | 247 | −14,7% | −7,2% | −8,7% | 30,8% | 7,7% | −44,3% | +36,2% |
| Likit tokenlar | 7 | 245 | −35,8% | −4,9% | −12,5% | 22,9% | 32,7% | −69,4% | +59,8% |
| Likit tokenlar | 30 | 231 | −49,9% | −5,3% | −16,2% | 16,9% | 49,8% | −82,9% | +39,1% |

#### Tablo S3b: +%100 günleri, giriş = olay günü kapanışı (tüm olaylar)

| k | n | Medyan | Ortalama | % pozitif | p10 |
|---|---|---|---|---|---|
| 1 | 406 | −16,3% | −8,2% | 29,1% | −50,8% |
| 3 | 404 | −26,6% | −10,0% | 25,0% | −62,2% |
| 7 | 402 | −35,0% | −11,2% | 21,6% | −69,1% |
| 30 | 383 | −49,2% | −11,8% | 16,2% | −81,9% |

#### Tablo S3c: +%50 ≤ r < +%100 günleri (ayrı küme), giriş = ertesi gün açılışı

| Grup | k | n | Medyan | Ortalama | % pozitif | p10 |
|---|---|---|---|---|---|---|
| Tüm olaylar | 1 | 1.286 | −8,5% | −2,5% | 33,1% | −28,9% |
| Tüm olaylar | 3 | 1.282 | −15,1% | −5,9% | 29,8% | −39,4% |
| Tüm olaylar | 7 | 1.275 | −19,5% | −4,5% | 28,5% | −47,1% |
| Tüm olaylar | 30 | 1.230 | −32,5% | −6,0% | 23,0% | −70,3% |
| Olay kapanışından giriş | 7 | 1.275 | −20,1% | −4,6% | 28,4% | −46,9% |
| Olay kapanışından giriş | 30 | 1.230 | −32,7% | −6,2% | 22,8% | −70,3% |

#### Tablo S3d: karşılaştırma ve alt gruplar (giriş = olay/gün kapanışı)

| Grup | k | n | Medyan | Ortalama | % pozitif | p10 |
|---|---|---|---|---|---|---|
| TABAN: tüm token-günleri (gün ≥1) | 1 | 454.225 | −0,4% | −0,1% | 43,4% | −7,6% |
| TABAN: tüm token-günleri | 7 | 449.671 | −2,8% | −0,5% | 38,4% | −21,1% |
| TABAN: tüm token-günleri | 30 | 432.214 | −11,1% | −0,8% | 32,8% | −44,2% |
| TABAN: gün 1–90 | 30 | 66.545 | −19,0% | −5,4% | 28,4% | −55,5% |
| +%100, olay günü hacmi ≥ 1M USDT | 1 | 168 | −11,3% | −4,8% | 37,5% | −42,5% |
| +%100, olay günü hacmi ≥ 1M USDT | 30 | 160 | −52,0% | −14,6% | 15,6% | −83,8% |
| +%100, olay günü hacmi < 1M USDT | 1 | 238 | −20,9% | −10,5% | 23,1% | −53,8% |
| +%100, listeden ≤ 30 gün | 7 | 62 | −30,7% | −2,8% | 17,7% | −67,3% |
| +%100, listeden ≤ 30 gün | 30 | 62 | −55,4% | −9,5% | 21,0% | −85,8% |
| +%100, Binance'te listeli token | 7 | 27 | −33,1% | +31,4% | 25,9% | −56,9% |
| +%100, Binance'te listeli token | 30 | 27 | −50,9% | −3,0% | 18,5% | −78,2% |

- +%100 günlerinin %24,6'sında ertesi gün kapanış-kapanış −%33 veya daha kötü (yani kazancın tamamı geri verilir), %10,3'ünde −%50 veya daha kötü (n=407). Olay günü kapanışı gün içi zirvenin medyan %78'inde (fitil bırakıyor). Olay günü işlem hacmi çeyrekleri: %10 26 bin, %25 82 bin, medyan 420 bin, %75 8,1 milyon, %90 29 milyon USDT — olayların yarısı çok ince piyasada. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

### Inferences
- +%100 gününden sonra ortalama "devam" yok; aksine tabana göre fazladan kayıp var (30 günde −%49 vs taban −%11, gün 1–90 tabanı −%19). Sağ kuyruk dar değil: 30 günde %6'sı bir kat daha artıyor, bu da ortalamaları medyandan çok yüksek tutuyor. Yani beklenen değer negatif, dağılım loto biletine benziyor.
- Hacimli (≥1M USDT) +%100 günlerinde ilk gün geri çekilmesi biraz daha hafif (−%11 vs −%21) ama 30 gün sonucu aynı (−%52).
- Binance tokenlarında n çok küçük (27–28 olay); bu grupta pozitif ortalama tek tük çok büyük devam hareketlerinden geliyor, sonuç değil.

### Gaps
- Olaylar aynı token içinde kümeleniyor (406 olay 245 tokenda); "tokenın ilk olayı" satırı bunu kısmen gideriyor, ama küme-bootstrap güven aralığı hesaplanmadı.
- Komisyon, kayma, ince defterde fiyat etkisi hesaba katılmadı; olay günü hacmi düşük olanlarda gerçek giriş fiyatı mumdaki fiyattan kötü olur.

## S4 — Olaydan önceki 1–10 günde yalnız OHLCV ile ölçülebilen sinyaller: olay günleri vs olay dışı günler, lift, eğitim/test

### Takeaway
Eğitim yarısında (listeleme < 1 Temmuz 2025; 478 token) seçilip test yarısında (listeleme ≥ 1 Temmuz 2025; 281 token) sınanan en güçlü tekli sinyal "önceki gün getirisi ≥ +%11,5": +%100 günü olasılığını taban %0,12'den %0,64'e çıkarıyor (test lift 5,4; eğitimde 4,9). İkinci sırada genişleyen aralık (son 3 gün / önceki 10 gün ≥ 1,86) ve hacim artışı (t−1 hacmi / önceki 7 gün ortalaması ≥ 1,85) var (test lift 2,3–2,7); ikisi birlikte lift 4,7. Lift'ler testte tutuyor, ama mutlak olasılık %1'in altında kalıyor ve bu sinyal günlerinde alım yapmak testte zarar ettiriyor (medyan 7 günlük getiri −%10 vs taban −%3). "Aralık sıkışması" değil, tersine aralık genişlemesi olayın habercisi.

### Cited Findings
- Özellikler (hepsi t−1 kapanışına kadar bilinen bilgiyle, olay günü t): d = listeden beri gün; vr1 = hacim_(t−1) / ortalama hacim_(t−8…t−2); vr3 = ortalama hacim_(t−3…t−1) / ortalama hacim_(t−10…t−4); dd = kapanış_(t−1) / o güne kadarki en yüksek kapanış − 1; ddh = aynı, fitil zirvesine göre; r_prev = r_(t−1); comp = ortalama (H−L)/C son 3 gün / önceki 10 gün (küçük = sıkışma, büyük = genişleme); yakin50 = son 10 günde +%50 gün var mı. Popülasyon: gün ≥2, getirisi tanımlı tüm token-günleri (rastgele örnek yerine tamamı). — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks), [Binance data-api klines](https://data-api.binance.vision/api/v3/klines)
- Eşik seçim kuralı (test yarısına bakılmadan, esikler.json'a zaman damgasıyla yazıldı; sha256 kaydı esikler_onkayit_*.json): her özellik için eğitim yüzdelik eşikleri (%5…%95), iki yön; destek ≥ %5 ve sinyalde ≥ 20 olay; en yüksek lift. Kombinasyon: seçilen tekli kuralların ikili VE'si, destek ≥ %2. İkinci set: yalnız d ≥ 8 günleri. Not: veri temizliğinden sonra (3 ticker değişimi tokenı çıkarıldı) aynı mekanik kural yeniden koşuldu; seçilen özellikler ve yönler ilk koşuyla aynı, eşikler 4. ondalıkta farklı (esikler_v1_ilk.json ve sonuc_s4_v1.md korunuyor). — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)
- Örneklem: eğitim 478 token, 363.213 token-gün, 285 adet +%100 ve 1.192 adet +%50 günü; test 281 token, 91.012 token-gün, 108 adet +%100 ve 462 adet +%50 günü. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

#### Tablo S4a: hedef +%100 günü, tüm günler (test tabanı %0,12; eğitim tabanı %0,08)

| Kural (eğitimde seçildi) | Eğitim destek | Eğitim P(olay\|sinyal) | Eğitim lift | Test destek | Test olay | Test P(olay\|sinyal) | Test lift | Test yakalama |
|---|---|---|---|---|---|---|---|---|
| Önceki gün getirisi ≥ +%11,5 | %5,0 | %0,39 | 4,91 | %5,4 | 31 | %0,64 | 5,36 | %29 |
| Aralık genişlemesi (son 3g/önceki 10g) ≥ 1,862 | %9,9 | %0,25 | 3,15 | %10,1 | 25 | %0,27 | 2,29 | %23 |
| Hacim oranı vr1 ≥ 1,845 | %10,0 | %0,22 | 2,82 | %11,7 | 34 | %0,32 | 2,68 | %31 |
| Hacim oranı vr3 ≥ 1,966 | %9,9 | %0,22 | 2,75 | %12,0 | 29 | %0,27 | 2,24 | %27 |
| Listeden beri gün ≤ 39 | %5,0 | %0,19 | 2,46 | %11,7 | 24 | %0,22 | 1,89 | %22 |
| Liste zirvesinden düşüş (fitil) ≤ −%99,26 | %15,0 | %0,16 | 2,08 | %6,9 | 13 | %0,21 | 1,74 | %12 |
| Liste zirvesinden düşüş (kapanış) ≤ −%99,22 | %10,0 | %0,15 | 1,96 | %3,9 | 7 | %0,20 | 1,66 | %6 |
| Aralık ≥ 1,862 VE vr1 ≥ 1,845 | %2,9 | %0,39 | 4,94 | %3,5 | 18 | %0,56 | 4,72 | %17 |

#### Tablo S4b: hedef +%50 günü, tüm günler (test tabanı %0,51; eğitim %0,33)

| Kural | Eğitim lift | Test destek | Test olay | Test P | Test lift | Test yakalama |
|---|---|---|---|---|---|---|
| Önceki gün getirisi ≥ +%11,5 | 5,44 | %5,4 | 124 | %2,54 | 5,01 | %27 |
| Listeden beri gün ≤ 39 | 2,77 | %11,7 | 104 | %0,97 | 1,92 | %23 |
| Aralık genişlemesi ≥ 1,862 | 2,58 | %10,1 | 111 | %1,21 | 2,38 | %24 |
| vr1 ≥ 1,845 | 2,36 | %11,7 | 131 | %1,23 | 2,42 | %28 |
| vr3 ≥ 1,966 | 2,29 | %12,0 | 124 | %1,14 | 2,24 | %27 |
| Zirveye yakın (kapanış düşüşü ≥ −%24) | 1,90 | %8,1 | 85 | %1,15 | 2,27 | %18 |
| Fitil düşüşü ≤ −%99,63 | 1,64 | %4,2 | 23 | %0,60 | 1,18 | %5 |
| Aralık ≥ 1,862 VE vr1 ≥ 1,845 | 3,98 | %3,5 | 63 | %1,96 | 3,86 | %14 |

- Yalnız d ≥ 8 günlerinde (ilk hafta dışarıda) aynı sıralama: +%100 için önceki gün getirisi ≥ +%11,4 test lift 6,09 (P %0,68, taban %0,11), aralık VE hacim 5,01, vr1 2,71; +%50 için önceki gün getirisi 5,22, aralık VE hacim 4,08. — [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)

#### Tablo S4c: olay günleri vs aynı tokenların rastgele olay-dışı günleri (tüm örnek; olay-dışı örnek n=7.860, 530 olay tokenından; +%100 n=393, +%50 n=1.654)

| Özellik | +%100 günü medyan | +%50 günü medyan | Rastgele olay-dışı gün medyan | +%100 p25 / p75 | Olay-dışı p25 / p75 |
|---|---|---|---|---|---|
| Listeden beri gün | 263 | 241 | 318 | 112 / 447 | 158 / 527 |
| vr1 (t−1 hacmi / önceki 7g) | 1,04 | 1,01 | 0,87 | 0,61 / 2,11 | 0,54 / 1,17 |
| vr3 (son 3g / önceki 7g) | 1,12 | 1,05 | 0,91 | 0,67 / 2,23 | 0,59 / 1,21 |
| Liste zirvesinden düşüş (kapanış) | −%92,2 | −%88,4 | −%89,5 | −%98,5 / −%69 | −%97,3 / −%71 |
| Liste zirvesinden düşüş (fitil) | −%96,0 | −%93,7 | −%93,8 | −%99,3 / −%82,5 | −%98,5 / −%81,5 |
| Önceki gün getirisi | +%0,4 | +%0,8 | −%0,4 | −%5,6 / +%12,3 | −%3,6 / +%2,2 |
| Aralık oranı (son 3g / önceki 10g) | 1,18 | 1,14 | 0,89 | 0,73 / 2,24 | 0,62 / 1,27 |
| Son 10 günde +%50 gün | 0 | 0 | 0 | 0 / 0 | 0 / 0 |

#### Tablo S4d: test yarısında sinyal gününün açılışında al (sinyal t−1 kapanışında bilinir), t+k−1 kapanışında sat

| Sinyal | k | n | Medyan | Ortalama | % pozitif | p10 | p90 |
|---|---|---|---|---|---|---|---|
| Önceki gün getirisi ≥ +%11,5 | 1 | 4.877 | −3,6% | −1,0% | 36,7% | −19,9% | +17,8% |
| Önceki gün getirisi ≥ +%11,5 | 7 | 4.810 | −9,7% | −1,3% | 33,3% | −37,9% | +33,5% |
| Aralık ≥ 1,86 | 7 | 9.054 | −3,8% | −1,7% | 36,5% | −28,1% | +20,2% |
| vr1 ≥ 1,84 | 7 | 10.513 | −4,3% | −0,7% | 36,2% | −27,6% | +20,4% |
| Aralık VE vr1 | 7 | 3.159 | −5,6% | −2,7% | 34,7% | −33,7% | +22,5% |
| TABAN: tüm test token-günleri | 1 | 91.012 | −0,4% | −0,1% | 43,3% | −8,0% | +6,8% |
| TABAN: tüm test token-günleri | 7 | 89.326 | −2,9% | −0,7% | 38,4% | −22,5% | +17,7% |

### Inferences
- Sinyaller gerçek ama zayıf: "dün zaten +%11'den fazla çıkmış, hacim ve aralık genişliyor" türü bir oynaklık rejimi ertesi gün +%100 ihtimalini ~5 katına çıkarıyor; yine de sinyal günlerinin %99'undan fazlasında +%100 olmuyor. Lift'lerin eğitimden teste korunması (4,9→5,4; 2,8→2,7; 4,9→4,7) bunun veri madenciliği artefaktı olmadığını, fakat aynı zamanda tahmin değil oynaklık ölçüsü olduğunu düşündürüyor.
- Sinyal günlerinde alım, tabandan daha kötü medyan getiri veriyor (S4d); yani sinyaller "patlama ihtimali" ile birlikte "geri dönüş riski"ni de büyütüyor. Bu ölçümden kârlı bir kural çıkmıyor.
- "Sıkışma sonrası patlama" (aralık daralması) bu veride desteklenmiyor: olay öncesi aralık oranı medyanı 1,18 (olay-dışı 0,89); en iyi eşik genişleme yönünde.
- Zirveden −%99'un üstünde çökmüş tokenlarda +%100 sıklığı ~2 kat (çok düşük fiyatlı, ince Gate tokenlarında yüzde hareketi kolay); bu ticari değil, mikro-yapı etkisi.

### Gaps
- Eğitim ve test yarısı tokenların listeleme tarihine göre bölündü; günler zaman olarak örtüşüyor (eğitim tokenlarının 2025–26 günleri de var), yani tam bir zaman dışı test değil.
- Lift'ler için güven aralığı hesaplanmadı; test olay sayıları küçük (7–34 olay/kural).
- Yalnız OHLCV kullanıldı; zincir üstü veri, unlock takvimi, borsa duyuruları, vadeli fonlama/açık pozisyon gibi muhtemelen daha güçlü değişkenler kapsam dışı.

## S5 — RITUAL/USDT'nin yeri

### Takeaway
RITUAL Binance, OKX ve (Bybit erişilemedi) incelenen büyük borsalarda yok; Gate'te 27 Ekim 2026, MEXC'te 26 Ekim 2026'da işleme açıldı (liste günü bu örneklemin penceresinin dışında, ölçüm anında 13 mumdan az). Ekran görüntüsündeki "+%99,88, 0,04164" bir 24 saatlik kayan değişim: Gate saatlik verisinde 24 saatlik değişim 8 Kasım 09:00–10:00 UTC'de +%102 / +%107'ye ulaştı (fiyat 0,0417–0,0426). UTC günlük kapanış-kapanış bazında hareket 8 Kasım'a düşüyor ve gün içinde (20:00 UTC) +%66 idi; gün kapanmadan +%100 sayılmaz. Öncesinde RITUAL listeden 12 gün sonra, liste zirvesine yakın (kapanışa göre −%5) ve önceki gün +%28,6 yükselmişti — eğitim yarısında seçilen "önceki gün ≥ +%11,5" sinyali açıktı (bu sinyalde test yarısında +%100 olasılığı %0,64).

### Cited Findings
- Listeleme: Gate RITUAL_USDT buy_start = 1793106000 (27.10.2026 13:00 UTC), ilk günlük mum 27.10.2026; MEXC RITUALUSDT ilk günlük mum 26.10.2026 (açılış 0,025, fitil 0,25 = açılış iğnesi, kapanış 0,02128). Binance exchangeInfo ve OKX enstrüman listesinde RITUAL yok. — [Gate currency_pairs](https://api.gateio.ws/api/v4/spot/currency_pairs), [Gate RITUAL 1d](https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1d&limit=60), [MEXC RITUAL 1d](https://api.mexc.com/api/v3/klines?symbol=RITUALUSDT&interval=1d&limit=60), [Binance exchangeInfo](https://data-api.binance.vision/api/v3/exchangeInfo), [OKX instruments](https://www.okx.com/api/v5/public/instruments?instType=SPOT)
- Gate günlük kapanışlar (UTC): 27.10 0,021386; 28.10 0,02076; 29.10 0,024217; 30.10 0,02111; 31.10 0,019407; 01.11 0,019716; 02.11 0,018901; 03.11 0,0258 (gün içi tepe 0,04194, hacim 2,7M USDT); 04.11 0,024074; 05.11 0,01915; 06.11 0,019017; 07.11 0,02446 (+%28,6, hacim 2,0M); 08.11 (kısmi, 20:xx UTC) son 0,0407, tepe 0,046, hacim 4,8M USDT. Gate 24s ticker (ölçüm anı): son 0,0407, değişim +%69,97, 24s tepe 0,046. — [Gate RITUAL 1d](https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1d&limit=60), [Gate RITUAL ticker](https://api.gateio.ws/api/v4/spot/tickers?currency_pair=RITUAL_USDT)
- Saatlik: 08.11 09:00 UTC kapanış 0,04173 (24s değişim +%102,1), 10:00 kapanış 0,0426 (24s +%107,0, saatlik tepe 0,046); ekran görüntüsündeki 0,04164 / +%99,88 bu saat aralığıyla uyumlu. MEXC'te aynı gün tepe 0,0468, MEXC 24s ticker +%68,5 (ölçüm anı). — [Gate RITUAL 1h](https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1h&limit=400), [MEXC RITUAL ticker](https://api.mexc.com/api/v3/ticker/24hr?symbol=RITUALUSDT)

#### Tablo S5: RITUAL'in olay öncesi özellikleri (t = 8 Kasım 2026 UTC; bilgiler 7 Kasım kapanışına kadar) ve örneklemdeki yüzdelik yeri

| Ölçü | RITUAL | 393 adet +%100 günü içinde yüzdelik | Tüm token-günleri içinde yüzdelik |
|---|---|---|---|
| Listeden beri gün (Gate ilk mumu) | 12 (MEXC'ten 13) | 8. | 2. |
| vr1: 7.11 hacmi / önceki 7 gün ort. | 1,79 | 70. | 89. |
| vr3: son 3 gün / önceki 7 gün | 1,17 | 52. | 72. |
| Liste zirvesinden düşüş, kapanış | −%5,2 | 94. (zirveye çok yakın) | 98. |
| Liste zirvesinden düşüş, Gate fitili | −%41,7 | 93. | 94. |
| Liste zirvesinden düşüş, MEXC açılış iğnesi (0,25) dahil | −%90,3 | — | — |
| Önceki gün getirisi (7.11) | +%28,6 | 88. | 99. |
| Aralık oranı (son 3g / önceki 10g) | 0,97 | 39. | 57. |
| Son 10 günde +%50 gün | yok (03.11 kapanış +%36, gün içi +%122) | — | — |

- Hareketin büyüklüğü: +%99,9'luk bir günlük getiri, örneklemdeki ilk 30 günün tüm token-günlerinin (n=22.770) yalnız %0,27'sinde aşıldı; +%50 olayları içinde 77. yüzdelikte. 8 Kasım'ın o anki kapanış-kapanış değeri (+%66,4) ilk 30 gün token-günlerinin %0,71'inde aşıldı, +%50 olayları içinde 40. yüzdelikte. — [Gate RITUAL 1d](https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1d&limit=60), [Gate candlesticks](https://api.gateio.ws/api/v4/spot/candlesticks)
- RITUAL'in eşik kurallarına göre durumu (7 Kasım kapanışında): önceki gün getirisi ≥ +%11,5 → AÇIK; vr1 ≥ 1,845 → kapalı (1,79, sınırda); aralık ≥ 1,86 → kapalı (0,97); listeden ≤ 39 gün → AÇIK. — [Gate RITUAL 1d](https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=RITUAL_USDT&interval=1d&limit=60)

### Inferences
- RITUAL tipik +%100 tokenından farklı bir profilde: örneklemdeki +%100 günlerinin medyan tokenı liste zirvesinden −%92 aşağıda ve listeden 263 gün sonra; RITUAL ise listeden 12 gün sonra ve kapanış zirvesine yakın. Bu, S2b'deki "ilk iki hafta" yüksek-tehlike bölgesine (gün 8–14'te 1000 token-günde ~1,9 adet +%100, ~10 adet +%50) düşüyor.
- Öncü işaretlerden yalnız "dün güçlü yükseliş" (ve erken gün) vardı; aralık genişlemesi yoktu, hacim artışı eşiğin hemen altındaydı. Test yarısına göre bu tip bir gün +%100 ile bitme olasılığı ~%0,6, +%50 ile ~%2,5.
- S3'e göre, +%100 kapanışlı bir günün ardından medyan yol 1 günde −%16, 7 günde −%35, 30 günde −%49; RITUAL'in 8 Kasım günü +%100 kapanırsa bu dağılıma girer (bu bir tahmin değil, örneklemin tarihsel dağılımıdır).

### Gaps
- 8 Kasım UTC günü ölçüm anında kapanmamıştı; günlük olay sınıflaması (r ≥ +%100 olup olmadığı) 9 Kasım 00:00 UTC'de netleşir.
- RITUAL'in proje/katalizör bilgisi (duyuru, unlock, airdrop) bu ölçümün kapsamı dışında; yalnız fiyat-hacim kullanıldı.
- RITUAL'in KuCoin günlük verisi indirildi ama analizde kullanılmadı; Bybit ve Binance Alpha listelemesi kontrol edilemedi.
