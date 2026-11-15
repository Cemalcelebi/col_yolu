# VDYT2-B ÖN KAYIT — VDYT2 sağlaması: A) mutlak hareket, B) batanlar dahil (v2b_20261112) — ölçümden ÖNCE

Yazım zamanı: 2026-11-12 17:40:06 UTC (2026-11-12 20:40 TR)
ESIK_SHA256: 279d7f9f7064c8700db6be53a850bd697547d5c1dca6b8dda0d2bb3b16a73994
KOD_SHA256: dcc0148ad4a62d3993e1287cd8b09137a097a4290dbc8dcc7f58f5227ef957ca
VDYT2_KOD_SHA256: e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741
VDYT_KOD_SHA256: 10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d
VDYT2_ESIK_SHA256: 3051e5b8ddd99c7c42e36f106bdaede734e8dac5ed6588029c5d50bc2274f5a8
LISTE_SHA256: 94499b18b6a160121aaaa3e31894c8bbc1ad4d2887417356f5d988de29e598dc
Sürüm: VDYT2-B v1.0 (v2b_20261112): Faz 1 (ön kayıt, kod + sentetik test, yalnız sayım; Tiingo fiyat isteği yok); ölçüm Faz 2'de

Bu dosya, VDYT2B.py ve örneklem listesi (vdyt2b_orneklem.tsv) git'e işlenmeden; eşik mührü, VDYT2B.py sha256'sı, VDYT2.py / VDYT.py sha256'ları (VDYT2 ön
kaydındakiyle aynı), VDYT2 ara tablo sha256'ları (A) ve liste sha256'sı (B) tutmadan `kos`, `pilot` ve `cek` ÇALIŞMAZ (Vdyt2bHata, çıkış 1). Sonuç görüldükten
sonra tanım, eşik, evren, örneklem, kontrol ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır ve ön kayıt yeniden işlenir.

## 0. Amaç ve sınır
- Cemal (12 Kasım 2026, aynen): 'İkisini de yap. Önce bir saatlik ön kayıt ve ölçütleri sabitleme; sonra veri çekme ve test. Özellikle başarısız örnekleri
  dışarıda bırakmayalım. Aksi hâlde yalnızca başarılı hisseleri inceleyerek sistemi olduğundan iyi sanabiliriz.'
- Bu iş bir SAĞLAMADIR. VDYT2 sonuçları (WF ve KASA raporları) ve IZ_KARNE Ç163 kararı ((1) bölgeyi bulmak BAŞARILI; (2) genişleme zamanı ve (3) yön
  BAŞARISIZ) DEĞİŞMEZ. VDYT2.py ve VDYT.py içe aktarılır, değiştirilmez. KASA bu işte yeniden 'açılmaz': VDYT2'de açılmış KASA dönemi (2024-01-01 -> 2026-08-31)
  aynı veriyle sağlama için kullanılır (yeni karar değil).
- Yalnız başarı (1) sağlanır. (2) ve (3) mutlak etiketle YENİDEN ÖLÇÜLMEZ (yalnız yön payı BİLGİ). Sonuç doğrulanmış sinyal değildir.

## 1. A — MUTLAK HAREKET SAĞLAMASI (başarı (1) için)
Gerekçe: VDYT2'de büyük hareket (BH1) bölgenin kendi küçük mumlarına göre tanımlıydı (büyük mum = TR >= 2,5 x bölge medyan TR); sessiz bölgede referans küçük
olduğu için 'bölge sonrası büyük mum' kısmen mekanik olabilir. A'da etiket bölgeden BAĞIMSIZ ve mutlaktır.
- σ[t] = t'ye kadar (t dahil) son 250 barın günlük ln getirisinin std'si (ddof 1, en az 200 geçerli getiri). ATR250[t] = son 250 barın ortalama gerçek
  aralığı (TR = max(H-L, |H-C[-1]|, |L-C[-1]|); en az 200). İkisi de YALNIZ t ve öncesinden (bölge kullanılmaz).
- MA1 (ANA): max_k=1..20 |ln(C[t+k] / C[t])| >= max(ln 1,15; 3 x σ[t] x √20). Yön = eşiği İLK aşan günün işareti. ('%15' ln ölçeğinde simetrik:
  yukarı +%15, aşağı -%13,1 basit getiri.)
- MA2 (BİLGİ): |ln(C[t+20] / C[t])| >= 2 x σ[t] x √20 (yalnız uç nokta). Yön = uç nokta işareti.
- MA3 (BİLGİ): max_k=1..20 TR[t+k] >= 3 x ATR250[t]. Yön = ilk büyük TR gününün C - C[-1] işareti.
- Ölçülemez (NaN): t + 20 > son bar, (t, t+20] içinde kopukluk (> 15 takvim günü; V1.vdyt_kopuk), σ / ATR250 tanımsız.
- Satırlar: VDYT2 (1)'in satırlarının AYNISI (yeniden hesaplanmaz): /tmp/vdyt2/kasa/satir_<pazar>_<tanım>.csv.gz ve kontrol_<pazar>_<tanım>.csv.gz (VDYT2
  `kos --asama kasa` ara çıktısı; wf klasöründekilerle içerik sha256'sı aynı, ön kayıt anında denetlendi; içerik sha256'ları EK-1). Satır kümesi: VDYT2 (1)
  kuralı (karar günü dönemde, son20 <= dönem sonu, y20 ölçülebilir) VE MA etiketi ölçülebilir. Hizalama denetimi: her satırda tarih == temiz fiyat serisinin
  t. barı (V2.v2_fiyat; VDYT2 ile aynı kesikli seri); tek satır tutmazsa koşu durur.
- Kontroller VDYT2 ile aynı: DIŞARI (tabaka sembol x yıl x NATR ondalığı) ve RASTGELE (tabaka yıl x yaş); kontrol, tabaka içinde gerçeğin dağılımına
  yeniden ağırlıklanır; hisse kümeli bootstrap B = 2000, tohum 20261112, %95.
- KARAR (1)-MUTLAK: ANA hücre = tanım G5, ön koşul P1, etiket MA1. BAŞARILI <=> gerçek oran - DIŞARI oranı > 0 ve %95 alt > 0 VE gerçek - RASTGELE > 0 ve
  alt > 0; WF (2019-2023) VE KASA'da; BIST ve ABD AYRI. n < 30 ya da tanımsız -> VERİ YOK. P0 / P2, öteki 15 tanım (AILE / ALT), MA2, MA3 ve aynı
  satırlarda BH1 (Y20) BİLGİ. Yön payı (MA hareketlerinde yukarı payı; gerçek / DIŞARI / RASTGELE) BİLGİ.

## 2. B — BATANLAR DAHİL SAĞLAMA (Tiingo ücretsiz katman; yalnız ABD)
### 2.1 Doğrulama pilotu (12 sembol; çekimden önce)
Tiingo'nun borsadan silinmiş şirketlerin fiyat geçmişini eksiksiz verdiği VARSAYILMAZ. supported_tickers listesinde (aşağıdaki 'liste' sütunu) görülen:
Tiingo iflas eden şirketin bütün geçmişini çoğunlukla bugünkü OTC 'Q' kodu altında tutuyor (SIVBQ PINK 1990-03-26 -> ; BBBYQ; RADCQ), bazen borsa dönemini ayrı
kayıtta bırakıyor (DNR NYSE -> 2020-07-30 ve DNRCQ PINK 2020-07-31 ->), kod yeniden kullanımında iki kayıt açıyor (SUNE NYSE 1995-2016 ve SUNE NASDAQ) ya da tek
kayıtta iki hisseyi birleştirmiş olabiliyor (CHK 1993-2024: 2020 iflasında eski hisse iptal, 2021-02-10 yeni hisse aynı kodla). Pilot bunları sınar.
Bilinen tarih = EDGAR Form 25-NSE (borsanın kotasyondan çıkarma bildirimi) tarihi, YEREL EDGAR dizininden (SEC'e istek yok).

| kod | şirket | CIK | Form 25-NSE | tür | Tiingo listesi |
|---|---|---|---|---|---|
| SIVBQ | SVB Financial Group | 719739 | 2023-05-02 | Q | PINK 1990-03-26 .. 2026-11-11 |
| BBBYQ | Bed Bath & Beyond | 886158 | 2023-07-10 | Q | PINK 1992-06-05 .. 2023-09-29 |
| RADCQ | Rite Aid | 84129 | 2023-10-31 | Q | PINK 1984-12-17 .. 2026-11-11 |
| WEWKQ | WeWork | 1813756 | 2023-11-22 | Q | EXPM 2020-10-21 .. 2024-06-11 |
| SHLDQ | Sears Holdings | 1310067 | 2018-11-15 | Q | EXPM 2003-05-01 .. 2022-10-31 (SHLD bugün ETF) |
| HTZGQ | Hertz Global (eski hisse) | 1657853 | 2020-10-30 | Q | PINK 2006-11-16 .. 2021-06-30 |
| REVRQ | Revlon | 887921 | 2022-10-21 | Q | PINK 1996-02-29 .. 2023-05-24 |
| YELLQ | Yellow Corp | 716006 | 2023-09-08 | Q | OTCMKTS 1986-07-09 .. 2026-07-01 |
| DNR | Denbury Resources | 945764 | 2020-08-17 | BORSA | NYSE 1995-09-06 .. 2020-07-30 (DNRCQ ayrı) |
| GNC | GNC Holdings | 1502034 | 2020-07-01 | BORSA | NYSE 2011-04-01 .. 2020-06-30 (GNCIQ ayrı) |
| SUNE | SunEdison (kod bugün SUNation) | 945436 | 2016-05-06 | YENIDEN | iki kayıt: NYSE 1995-07-13 .. 2016-04-21 ve NASDAQ 1990-03-26 .. 2026-11-11 |
| CHK | Chesapeake Energy (2020 iflas; eski hisse 2021-02-09 iptal, yeni hisse 2021-02-10, aynı kod) | 895126 | 2020-07-20 | YENIDEN | NASDAQ 1993-02-16 .. 2024-10-04; CHKAQ NYSE 2021-03-17 .. 2021-05-17; EXE 2021-02-10 .. |

Tür: Q = bütün geçmiş bugünkü OTC Q kodunda; BORSA = borsa dönemi ayrı kayıt; YENIDEN = kod yeniden kullanımı (karışma sınaması).
Pilot ölçütleri (sembol başına; önceden):
- K1 seri: HTTP 200 ve kapanışı > 0 en az 252 bar.
- K2 son gün: BORSA: son bar ∈ [F25 - 60 iş günü, F25 + 10 iş günü] (borsa önce işlemi askıya alır, Form 25 sonra gelir; arada haftalar olabilir); Q: son bar >=
  F25 - 60 iş günü VE [F25 - 60, F25 + 10] iş günü penceresinde en az 1 bar (borsa dönemi kotasyondan çıkışa kadar seride); YENIDEN: F25 - 60 iş gününden
  önceki 60 iş gününde bar var (eski şirketin dönemi seride).
- K3 boşluk: A = (BORSA: son bar; Q / YENIDEN: F25 - 60 iş günü); [A - 60 iş günü, A] penceresinde eksik iş günü <= 5 ve en uzun boşluk <= 5 iş günü (ABD
  federal tatil takvimi).
- K4 kaba tutarlılık (kaynak varsa; yoksa DEĞERLENDİRİLMEDİ, karara girmez): SIVBQ 2023-03-09 ham kapanışı basında bildirilen 106,04 $'ın ±%10'u içinde;
  SUNE Tiingo serisi ↔ k34_yahoo SUNE (bugünkü şirket) ve CHK ↔ k60_fiyat EXE (yeni hisse, 2021-02-10 -> 2024-10): ortak günlerde günlük ln getiri
  korelasyonu >= 0,90 ve |kapanış oranı - 1| medyanı <= %2 (bölünme düzeltmeli). (SUNE / CHK'de K4'ün tutması 'yeni şirketin serisi Tiingo kodunda' demektir;
  karışma K6 ile ölçülür.)
- K5 OHLCV: barların >= %95'inde açılış / yüksek / düşük / kapanış / hacim dolu, yüksek >= düşük, kapanış > 0.
- K6 karışma: YENIDEN: seri hem eski (yeni_bas'tan önceki 250 iş günü) hem yeni (sonraki 250 iş günü) dönemi içeriyorsa arada >= 30 iş günü boşluk olmalı
  (ayırt edilebilir); değilse KARIŞIK. Diğerleri: bölünme günü olmayan |günlük ln getiri| > ln 10 sıçrama yok.
- Sembol GEÇTİ <=> K1 VE K2 VE K3 VE K5 VE K6 VE (K4 değerlendirildiyse K4).
- PİLOT KARARI: GÜVENİLİR <=> >= 10 / 12 geçti; KISMEN <=> 7-9; GÜVENİLMEZ <=> <= 6. İki YENIDEN sembolünün ikisi de KARIŞIK ise karar en çok KISMEN.
  Q türünün HİÇBİRİ geçmezse OTCQ kaynağı B'den çıkarılır (beyan). GÜVENİLMEZ ise B testinin geri kalanı (çekim ve koşu) KOŞULMAZ; raporda yazılır.
### 2.2 Evren (supported_tickers; fiyat isteği YOK; kurallar sırasıyla, sayımlar EK-2)
1. assetType Stock, priceCurrency USD.
2. Kod ^[A-Z]{1,5}$ (nokta / tire / rakam yok: imtiyazlı, sınıf, birim); 5 harfli kodlarda son harf F G H I M N O P R S T U V W X Y Z ise atılır (yabancı,
   tahvil, imtiyazlı, hak, fayda payı, varant, birim, when-issued, fon, ADR); Q (iflas) ve A-E, J-L kalır.
3. Aynı kod listede birden çok Stock kaydıyla geçiyorsa (kod yeniden kullanımı; API'nin hangi seriyi vereceği belirsiz) bütün kayıtları atılır.
4. k60 evreninde (bugün yaşayan, VDYT2'de zaten olan) kod atılır.
5. BORSA kaynağı: exchange ∈ {NYSE, NASDAQ, NYSE MKT, AMEX}, endDate ∈ [2019-02-01, 2026-06-30], startDate <= endDate - 400 gün.
6. OTCQ kaynağı: exchange ∈ {PINK, OTCMKTS, EXPM, OTCGREY, OTCQB, OTCQX, OTCBB, OTCCE, OTCD}, kod ^[A-Z]{3,4}Q$ (iflas eki), endDate >= 2019-02-01,
   startDate <= min(endDate - 400 gün, 2025-06-30). AYRIK OTC dönemi (ilk 3 harfi aynı bir borsa kaydının endDate'i Q kaydının startDate'inden en çok 10 gün
   uzakta: borsa dönemi BORSA kaynağında) atılır.
7. SPAC kabuğu (çekim öncesi): kod + 'U' ya da kod + '-U' birim kaydı var VE birimin endDate'i >= kodun endDate'i - 30 gün (kabuk birleşmeden tasfiye /
   kapanış) -> atılır. Birleşip sonra yaşayan ya da batan şirket (birimi erken biten) KALIR.
### 2.3 Tabakalama ve örneklem (çekimden ÖNCE; liste dosyası vdyt2b_orneklem.tsv, sha256 başlıkta)
- Tabaka = kaynak (BORSA / OTCQ) x endDate yılı (OTCQ'da endDate > 2026-06-30 ise 'OTC_HALA': bugün de OTC'de kotalı). Son piyasa değeri / son fiyat listede
  yok (fiyat isteği gerekir) -> tabakaya girmez.
- ANA 450 (orantılı dağıtım, en büyük kalan; her dolu tabakada en az 1) + YEDEK 38 (kalan evrenden orantılı). Tabaka içinde sıra: numpy default_rng(20261117 +
  tabaka sırası) permütasyonu (tabakalar adla sıralı; tabaka içinde kodlar adla sıralı). İlk n_h ANA, sonraki y_h YEDEK.
- YEDEK yalnız aynı tabakada VERİ YOK (HTTP 404 / boş / temiz bar < 252) olan ANA sembolün yerine, sırayla kullanılır. Başka hiçbir nedenle (sonuç, getiri,
  etiket) yedek kullanılmaz; hiçbir sembol sonuç görülerek çıkarılmaz.
### 2.4 Çekim sonrası kurallar (önceden; etiket / sonuç görülmeden uygulanır; hepsi raporda sembol sembol listelenir)
- D1 VERİ YOK: HTTP 404 / boş / temiz bar < 252 -> yedekle değiştirilir.
- D2 SPAC KALIBI: ham kapanışların >= %80'i [9, 11] $ aralığında -> SPAC kabuğu: evren dışı, değiştirilmez.
- D4 KOD DEĞİŞİKLİĞİ: son 60 barın günlük ln getirisi bir k60 serisiyle (ortak gün >= 55) korelasyon >= 0,98 VE ln(kapanış oranı) std <= 0,01 -> aynı şirket
  yaşayan evrende (ör. CHK -> EXE): evren dışı, değiştirilmez (çift sayımı önler).
- D3: VDYT uygunluğunu (>= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $) hiç sağlamayan sembol ÇIKARILMAZ (evrenin üyesidir; satırı
  olmaz, ağırlık paydasında kalır).
- Fiyat: Tiingo ham OHLCV + splitFactor -> bölünme düzeltmeli seri = ham / (gelecekteki bölünme oranlarının çarpımı), hacim x aynı çarpım (Yahoo / k60 ile aynı
  tür: bölünme düzeltmeli, temettü düzeltmesiz); ekrandaki fiyat = ham kapanış (meta 'bolunme' ile V1.vdyt_bolunme_carpan aynı sonucu verir). V1.vdyt_bar_temizle
  + 2010-01-01 .. 2026-08-31 kesiti (VDYT2 ABD ile aynı).
- Ağırlık (ters olasılık): tabaka h için w_h = N_h / m_h; m_h = h'de verisi gelen örneklem sayısı (D2 ve D4 dahil: evren dışı payı N_h'yi aynı oranda küçültür).
  Yaşayan (k60) satırlar w = 1.
### 2.5 B işlemi ve karar
- Batan satırları VDYT2 kodu ile üretilir (V2._v2_hisse_is; tanım YALNIZ G5; kip 'kos'; DIŞARI ve RASTGELE kontrolleri dahil, aynı tohum kuralı). ABD paneli
  (uygunluk, NATR ondalığı, tertiller) k60 + batan örneklemi BİRLİKTE kurulur (V1.vdyt_panel). Yaşayan satırlar VDYT2 tablolarından AYNEN alınır (yeniden
  hesaplanmaz). Olay özellikleri batanlarda boş (VDYT2 olay kaynakları yaşayanlar için; makro olaylar var): yalnız (2) / (3) modellerini etkiler, burada model yok.
- Etiketler: y20 (BH1; VDYT2 ile aynı) ve MA1 (A ile aynı). Satır kümesi A ile aynı kural (VDYT2 (1) satırı VE MA1 ölçülebilir; iki etiket aynı satırlarda).
- (a) yalnız batanlar (ağırlıklı): gerçek / DIŞARI / RASTGELE oranları ve farkları (BİLGİ; n küçük olabilir).
- (b) BİRLEŞİK evren (yaşayan w = 1 + batan w_h): (1)-BATANLAR DAHİL BAŞARILI <=> G5, P1: gerçek - DIŞARI > 0 ve alt > 0 VE gerçek - RASTGELE > 0 ve alt > 0;
  WF VE KASA. y20 ve MA1 ayrı sütun. Ağırlıklı karşılaştırma: tabaka içinde kontrol ağırlığı = w x (Σw_gerçek / Σw_kontrol); ağırlıklar 1 iken VDYT2'nin
  v2_oran_karsilastir'ı ile birebir aynı (test).
- Batanlarda (2) / (3) BİLGİ: y20 = 1 satırlarında yukarı payı, r20 ve MAE ortalaması (ağırlıklı), yaşayanlarla yan yana.

## 3. İstek bütçesi ve takvim (Tiingo ücretsiz katman: ayda 500 farklı sembol, saatte 50, günde 1.000 istek)
- Kodda sert sınırlar: saatte en çok 45 istek, günde en çok 900, takvim ayı (UTC) içinde en çok 500 farklı sembol. Kalıcı sayaç /tmp/vdyt2b/tiingo_sayac.json
  (istek gönderilmeden ÖNCE kaydedilir); sınıra gelince bekler, ay sınırında durur. 429 -> 15 dk bekle, art arda 3 kez -> dur. Önbellek /tmp/vdyt2b/tiingo/
  (repoya veri YOK; Tiingo lisansı). Önbellekte olan sembol yeniden istenmez.
- Pilot: 12 istek (12 farklı sembol; birkaç dakika). Örneklem: 450 ANA (SHLDQ ve YELLQ hem pilotta hem örneklemde: önbellekten, ek istek yok) -> 448 istek +
  en çok 38 yedek. Ay toplamı en çok 12 + 448 + 38 = 498 farklı sembol (< 500). Saatte 45 ile ~10-11 saat (günlük 900 sınırı bağlamaz). Çekim kaldığı yerden
  sürer.
- Anahtar YALNIZ ortamdan (TIINGO_API_KEY); yoksa istek 'Authorization: Token proxy' başlığıyla gider (oturumun ağ vekili gerçek anahtarı enjekte edebilir).
  Anahtar URL'ye, loga, önbelleğe, sayaca ya da çıktıya yazılmaz (test).

## 4. Yanlılık beyanı
- Tiingo kapsamı: 2010-2014 çıkışları listede az (envanter); bu iş 2019+ çıkışları kullanır. Borsadan düşüp OTC'de Q eki almadan işlem gören (iflassız
  kotasyondan çıkma: fiyat < 1 $, rapor gecikmesi) şirketler OTC listesinde ayırt edilemez -> KAPSANMAZ (yalnız borsa kaydı ölü olanlar BORSA kaynağında).
- Kod yeniden kullanımı: listede yinelenen kodlar atılır; tek kayıtta iki hisseyi birleştiren seri (CHK türü) ayırt edilemeyebilir -> pilot K6 ve D4 ile kısmen;
  kalan risk beyan. Kopukluk (> 15 takvim günü boşluk) VDYT2 kuralıyla zaten etiketi bölmez (NaN).
- OTC dönemi: uygunluk (fiyat >= 2 $, işlem değeri >= 1 mn $) OTC barlarının çoğunu dışarıda bırakır; batan satırlarının çoğu borsa dönemindendir.
- Temettü düzeltmesi yok (k60 ile aynı tür); bölünme düzeltmesi Tiingo splitFactor'dan.
- Kapalı uçlu fon / NYSE ADR'leri listede ad olmadığı için ayıklanamaz (5 harfli F / Y elenir; 4 harfli ADR kalır).
- Yaşayan evren k60'tır (Tiingo aktif evreninin 2024'te ~%70'i; envanter): birleşik evren 'bütün ABD' değil 'k60 + batan örneklemi'dir.
- Örneklem: evrenin ~%20'si (450 / 2.219); batan sonuçlarının belirsizliği hisse kümeli bootstrap'ta (ağırlıklı) görünür.
- A'da satırlar ve kontroller VDYT2'den aynen: VDYT2'nin yaşayan evren yanlılığı A'da da vardır (A'nın sorusu etiketin mekanikliğidir).

## 5. SAPMA / BOŞLUK (iş tanımına göre; ölçümden önce)
1. B evreninde endDate alt sınırı 2016-01-01 değil 2019-02-01: 2016-2018 çıkışlarının karar satırları 2019 öncesindedir; başarı (1) yalnız WF test yılları
   (2019-2023) ve KASA'da ölçüldüğü için katkıları SIFIR olurdu (ayda 500 sembollük bütçe boşa gider). Sayıları (2016-01 .. 2019-01 arası biten borsa kaydı)
   EK-2'de bilgi olarak yazıldı.
2. B evrenine OTCQ kaynağı eklendi ('exchange NYSE / NASDAQ / NYSE MKT' süzgeci tek başına iflas edenlerin çoğunu dışarıda bırakırdı: Tiingo bunların
   geçmişini bugünkü OTC Q kodunda tutuyor). 'Bugün işlem görmeyen' = 'bugün borsada işlem görmeyen'; OTC_HALA tabakası bugün OTC'de kotalı.
3. Tabakalama endDate yılı x kaynak (son piyasa değeri / son fiyat listede yok; fiyat isteği gerekir).
4. SPAC / fon / ADR / imtiyazlı / varant elemesi ad ile yapılamadı (listede şirket adı yok): kod kuralları + SPAC birim kuralı (çekim öncesi) + SPAC fiyat
   kalıbı (çekim sonrası) + kod değişikliği kuralı D4 (çekim sonrası).
5. Pilot listesi iş tanımındaki öneriden değişti: LK (yabancı ADR; örneklemde ADR elenir) ve FRC (banka: Form 25-NSE EDGAR'da yok, bilinen tarih yerelden
   doğrulanamaz) yerine HTZGQ, REVRQ, YELLQ, DNR, GNC. SIVB / BBBY / RAD / WE / SHLD Tiingo'da Q kodlarıyla (SIVBQ, BBBYQ, RADCQ, WEWKQ, SHLDQ). Son gün
   ölçütü '±10 iş günü' yerine [F25 - 60, F25 + 10] iş günü (bilinen tarih Form 25-NSE; askı ondan önce).
6. Pilot K4 kaynağı yalnız 3 sembolde var (SIVBQ basın kapanışı, SUNE k34 Yahoo, CHK ↔ k60 EXE); diğerlerinde DEĞERLENDİRİLMEDİ.
7. B yalnız ANA tanım G5 (AILE / ALT yok) ve etiketler y20 + MA1 (MA2 / MA3 yok).
8. B'de batan satırlarının kesit ondalıkları birleşik panelde (k60 + batan örneklemi); yaşayan satırlar VDYT2 tablolarından aynen (birleşik panelde batan payı
   küçük; yaşayan satırların ondalığı değişmez).
9. A satırları VDYT2 ara tablolarından (yeniden hesaplanmaz; içerik sha256 EK-1). Tablolar kaybolursa VDYT2 kodu aynı veriyle (tohumlu) aynı tabloyu üretir;
   sha256 tutmalı (tutmazsa SAPMA).
10. A ve B satır kümesi: VDYT2 (1) satırları ∩ MA1 ölçülebilir (aynı satırlarda BH1 bilgi olarak yeniden hesaplanır; VDYT2 raporundaki BH1 sayılarından biraz az).
11. MA1 eşiği ln ölçeğinde simetrik (ln 1,15); σ penceresi t'yi içerir (C_t kapanışında bilinir).
12. SHLDQ ve YELLQ hem pilotta hem örneklemde (tohumlu seçim; önbellek; ek istek yok; örneklemde diğer semboller gibi işlenir).
13. Kapsam sayımı (EK-3) ön kayıttan hemen önce AYNI kodla yapıldı (vdyt2b_kapsam_A.json 'kod_sha256' = KOD_SHA256; değilse ret sebebi, ana oturum denetler).
14. `kos --test B` için pilot ve çekim dosyaları (vdyt2b_pilot.json, vdyt2b_cek_durum.json) çıktı klasörüne yazılır; Tiingo fiyatı içermez (yalnız durum,
    tarih, ölçüt sonucu; pilotta birkaç kapanış değeri).
15. BOŞLUK: batanlarda olay verisi yok; ABD dışı batan yok (BIST batanları VDYT2'de BIST_K62 ile bilgi olarak var); Tiingo listesi günlük değişir (sha256
    başlıkta; Faz 2 aynı liste dosyasıyla).

## 6. Faz 2 komutları
1. (ana oturum) bu dosyayı, VDYT2B.py'yi, test_vdyt2b.py'yi, vdyt2b_orneklem.tsv / vdyt2b_evren_sayim.json / vdyt2b_kapsam_A.json'u denetler, git'e işler.
2. `python -I VDYT2B.py kos --test A` -> vdyt2b_sonuc_A.json + VDYT2B_RAPOR_A.md (Tiingo gerekmez; ret kapısı: mühür, kodlar, tablo sha256, git).
3. TIINGO_API_KEY ortamda (ya da ağ vekili başlığı) -> `python VDYT2B.py pilot` (12 istek) -> vdyt2b_pilot.json (GÜVENİLİR / KISMEN / GÜVENİLMEZ).
4. Pilot GÜVENİLİR / KISMEN ise `python VDYT2B.py cek` (arka planda, ~10-11 saat; kaldığı yerden sürer; `--en-cok N` ile parçalı) -> vdyt2b_cek_durum.json.
5. `python -I VDYT2B.py kos --test B` -> vdyt2b_sonuc_B.json + VDYT2B_RAPOR_B.md. 6. `python VDYT2B.py rapor --test A|B` raporu JSON'dan yeniden yazar.

## 7. Değişmezlik
VDYT2B_ESIK değişirse ESIK_SHA256; VDYT2B.py değişirse KOD_SHA256; VDYT2.py / VDYT.py / VDYT2 eşikleri değişirse VDYT2_* satırları; VDYT2 tabloları değişirse
EK-1; liste değişirse LISTE_SHA256 tutmaz -> `kos` / `pilot` / `cek` durur.

## EK-1. VDYT2 ara tablo içerik sha256'ları (A; `kos --test A` yeniden hesaplar, farklıysa ret)

- kontrol_ABD_G1.csv.gz: sha256 7a79cbf9631712fc03b8ba1b0613c30d29d2eb64e6a22cfa473d771b9f9944a4
- kontrol_ABD_G1_e0.5.csv.gz: sha256 c210e88734293d5b280b6faf479466488e3a572126020d3e251555665cf5d393
- kontrol_ABD_G1_e0.7.csv.gz: sha256 42c753880bd2e1129ae597c436daa44926474221e5c847feb79a121638ee7d13
- kontrol_ABD_G2.csv.gz: sha256 76e5a982c4d3dc49b63f74116336f66ad6781fdce4207e174e88358d6289b7e5
- kontrol_ABD_G3.csv.gz: sha256 2e18eff4bd75aa4b37e4009dbc816002ee8a6fc7a9f9b4c8ff749e05d1b7fc67
- kontrol_ABD_G4.csv.gz: sha256 386bc7db3a8e6ec8a3ee315f64a37b6e13c6a6e2285bab941b6eaece97d5fa62
- kontrol_ABD_G5.csv.gz: sha256 b7ab81562dd318a24da50e158fc0476642e5624ff9227f7c883c271872b5c172
- kontrol_ABD_G5_g0.4.csv.gz: sha256 de4f0c518b9233d07d199ccbb11c1867123fee616a8c9f8d44badaab28090f0d
- kontrol_ABD_G5_g0.6.csv.gz: sha256 e1b5939f6b775e95d9ac14dda6c36ad47c6e5ffb7709dfc197309dc71b93a096
- kontrol_ABD_G5f.csv.gz: sha256 13a23fe4814e8a8272eb914c636162289deb5d04df51e756d04efe11a843e7b8
- kontrol_ABD_G5k.csv.gz: sha256 ceb364642d00c837d9861012603fca3b063ec4b7d2cae65441185cceb1920bb8
- kontrol_ABD_T1.csv.gz: sha256 6a14f12c26a69919e09a1977a0c387b3aa1580ef8f1914e73483f909526a989c
- kontrol_ABD_T2.csv.gz: sha256 a15bdd3eff56a6a6808c212c3b8426d6847ac49073e236e520dd1e3adeff91ed
- kontrol_ABD_T3.csv.gz: sha256 02c881d86608ad3049f540b6eb920a752f40efa0a3f38c3aa707857f2625c08a
- kontrol_ABD_T4.csv.gz: sha256 a7eef5a7f4144fef50e1ae6c89981c9c152012d90582177689e9f0d4fa46f63f
- kontrol_ABD_T5.csv.gz: sha256 38d9f4db41c5f726a87da1aefc3a6a24b8a90d63b1ef86161942bafa0616d4af
- kontrol_BIST_G1.csv.gz: sha256 7692681e04cb0938327baf5bb83117ddf75beb093fb84d219072d3696509cd26
- kontrol_BIST_G1_e0.5.csv.gz: sha256 ba0b2b36b4018aa4249e6b52bd41c852f29e18ae4b9b959b9e2eb4143f6fa377
- kontrol_BIST_G1_e0.7.csv.gz: sha256 3d39ca47055f44835569839936ce509dc6f061fe7a392a05ca5e9409368e5003
- kontrol_BIST_G2.csv.gz: sha256 0574db8155b4260a8eac2554fb7457f17443401d56453bace672d8b5f4f7f2bd
- kontrol_BIST_G3.csv.gz: sha256 add9cb290559c91c80e4ca5ad02d08abe90d1e634a796938dc842afdd14e2046
- kontrol_BIST_G4.csv.gz: sha256 f353bf5f79dc03702302c939d2ce92c7114c87f79b60b21432b3fb0969c1e67c
- kontrol_BIST_G5.csv.gz: sha256 adf68c34deb815115c1c0a152356227e78e32dda1efc8b05cff2f26c47052de0
- kontrol_BIST_G5_g0.4.csv.gz: sha256 6394e977c4de2c5fcd50fbb3c731cda2f30498d7f7870a7066e09d3317310b6c
- kontrol_BIST_G5_g0.6.csv.gz: sha256 21507b397dcfb58870c27a889168853138243192c882881b0e4dbdb8203b19a1
- kontrol_BIST_G5f.csv.gz: sha256 1684dbe155f4ba4772afe58dc0abfe23e9aba37a252dd322b5fbba4d86a56134
- kontrol_BIST_G5k.csv.gz: sha256 c8161d70de00a9be6e38f115b11497d657236eaf36015894489b0977c60e3658
- kontrol_BIST_T1.csv.gz: sha256 cf326ab8377150694d732efe28ce6275b4fc2559e070ea83f8918069e998529f
- kontrol_BIST_T2.csv.gz: sha256 9b883cda7cf6a5951500e8babaeb61a879bafacc025eec376c5683f5cfecc4c6
- kontrol_BIST_T3.csv.gz: sha256 bbd6ed207e06540056d38d742e21bffe8dac8d0a48cd696a28cb8aab91b7d681
- kontrol_BIST_T4.csv.gz: sha256 d77a9986cb0b09582f8676709d78cae4d5b3e91ba7bb733dae21a9ee503bcd55
- kontrol_BIST_T5.csv.gz: sha256 c84a24c458d875198bf364cb19aeabdd3a972bf580aeee07a9cb9b1239049475
- satir_ABD_G1.csv.gz: sha256 098aae261bcd07315e7a0df2a148b32a67f964de17ace0fe04548ea5b78ab6b7
- satir_ABD_G1_e0.5.csv.gz: sha256 e713d2d73f0086294aa75994360400b256cc14ebbdf63e7a3152645a4f6ff328
- satir_ABD_G1_e0.7.csv.gz: sha256 d7858045af81162bd6c4f5ab88f3a8ea4b00523b5396d19409b3b80a287bbccc
- satir_ABD_G2.csv.gz: sha256 9972f3d9675e913b51f4f4c401dd8d35b49cae792b19782b8723488754ed96de
- satir_ABD_G3.csv.gz: sha256 80bc02c1ba9d3b277a6cc2a3d8ffa9c071fd72fe718850153b7a8fd12d5fb229
- satir_ABD_G4.csv.gz: sha256 c12cc1e7c79e8cc48916933c7bf12656cbb19ee50b5916d57be9fdf9575b2e45
- satir_ABD_G5.csv.gz: sha256 c65928af4b6f3ba011e0e6e24d963e33680eb24db88c0f2c046d25863c01c1a7
- satir_ABD_G5_g0.4.csv.gz: sha256 5cbf50a9c08a96753ebd95f6e57afea36520c0c1cb1a3161cdeb9c04664c2366
- satir_ABD_G5_g0.6.csv.gz: sha256 8c1d7f0ef0c4c5430a91bb46c1aef7a8ba22185ab83cb7a9e3cd871677eec0aa
- satir_ABD_G5f.csv.gz: sha256 3685a653bb4dbaecf52052ad0809fda83cdcefcfd79bf1d3e284b569d77140b6
- satir_ABD_G5k.csv.gz: sha256 b780fe38325496f1a67c290ac5e2d242472045f7c01099e22686923cd0a1554e
- satir_ABD_T1.csv.gz: sha256 10b6d844f4fcd516e2f2e75cb55e91f9817563c0a4534f349e1b1f481ca54f0c
- satir_ABD_T2.csv.gz: sha256 da9ae3a8fab81757dd068598fbd0b76b4b48321239eac447017944f60a19bf23
- satir_ABD_T3.csv.gz: sha256 3d86b64ff8c6549a500fddf0c6b90c2783bf348625d0ab019f366d51ddfc028d
- satir_ABD_T4.csv.gz: sha256 a24065e2427b94b82172081a95cf7870bc1c71722bfef72d5f291cb31d63202a
- satir_ABD_T5.csv.gz: sha256 62c8bc1cb372ac651f652b206557c0605786d409f727b713cd9eb7fac8a377de
- satir_BIST_G1.csv.gz: sha256 afd9f7e355d423edb7e708f922875b79f312628dcc83852ac4026dd37e1f42ee
- satir_BIST_G1_e0.5.csv.gz: sha256 5a855c83d7b768bad9ad0ee9c79a6c2fae962f86d1b977a6fc7238a46907bfef
- satir_BIST_G1_e0.7.csv.gz: sha256 cd962703305ea22740e869307df4825bf2dc35899e1fc196a8f57de8313f8794
- satir_BIST_G2.csv.gz: sha256 47a0c659d3863acbb0168466d9b97b58b6248585cbd98708e5cc189e4b60b9e3
- satir_BIST_G3.csv.gz: sha256 7a7a9f622cca6c9e2b029fb40b416fe7e4d4a1145d12dfeb32a4a68331a93cac
- satir_BIST_G4.csv.gz: sha256 ddf815923d5fb45db131820fc821728c77da7ca3983d7293d806f5a62ae73338
- satir_BIST_G5.csv.gz: sha256 a3474c6d9fc6811a4cf10d5ff6d58c5795ec2c794ee26380bc9a325685bcd119
- satir_BIST_G5_g0.4.csv.gz: sha256 f2cf16d9da0ff0ba1cb05f003eb39bbbd7b792dccedd6d9a20a6892664f5955e
- satir_BIST_G5_g0.6.csv.gz: sha256 c3a98e0f871d8f49e99d08ed046c35056824d24c52b1f4d6f47e0ab58f76640e
- satir_BIST_G5f.csv.gz: sha256 5fa161f08439a1631d7f0677c36a87bbbf28471ada8ac1cb1456a9aa70f09cbe
- satir_BIST_G5k.csv.gz: sha256 1156589abf1b3baf1738bf3e9bad8deec3db05261aa71c95799f40ac1a334e66
- satir_BIST_T1.csv.gz: sha256 a55fc3dec69e8db48fe7c325a616a22ce103197fc2a886e2972ea552ce9f3a5a
- satir_BIST_T2.csv.gz: sha256 5153974fd66f3eee3e24c104df976a5dc5021b2f26d0d7f38228392721be9b5a
- satir_BIST_T3.csv.gz: sha256 a82c5d26cdf62385e8744f7ee481c14db042dda3366e2f0614207f81913cbb0e
- satir_BIST_T4.csv.gz: sha256 55699c40d649b78b3a64f66c5278bce1409a60b0e73cffe0c581ae00ae732561
- satir_BIST_T5.csv.gz: sha256 15264ed4b037a39cce7933d9a4c0f7388bbf4508b64c73495ea9b70e20b3de31

## EK-2. B evren sayımı (`liste`, 2026-11-12 17:27:43 UTC; supported_tickers sha256 3d33d870111072d8a87de8a3f73cb3b30f00ec928fa517846ae29b614822f800, listedeki en son endDate 2026-11-12)

- 1_stock_usd: 43012
- 2_kod_atilan: 22607
- 3_yinelenen_kod_atilan_kayit: 1608
- 4_k60_atilan: 4289
- 5_borsa: 2142
- 5_borsa_bilgi_2016_2019_bitis: 1076
- 6_otcq: 551
- 6_otcq_aday: 570
- 6_otcq_ayrik_atilan: 19
- 7_spac_kabugu_atilan: {"BORSA": 471, "OTCQ": 3}
- evren: 2219
- evren_kaynak: {"BORSA": 1671, "OTCQ": 548}
- liste_satir: 109272

| tabaka | evren N_h | örneklem n_h | yedek | ağırlık N_h / n_h |
|---|---|---|---|---|
| BORSA / 2019 | 212 | 43 | 3 | 4,93 |
| BORSA / 2020 | 193 | 39 | 3 | 4,95 |
| BORSA / 2021 | 256 | 52 | 4 | 4,92 |
| BORSA / 2022 | 219 | 45 | 3 | 4,87 |
| BORSA / 2023 | 239 | 49 | 4 | 4,88 |
| BORSA / 2024 | 195 | 40 | 3 | 4,88 |
| BORSA / 2025 | 222 | 45 | 4 | 4,93 |
| BORSA / 2026 | 135 | 27 | 2 | 5,00 |
| OTCQ / 2019 | 49 | 10 | 1 | 4,90 |
| OTCQ / 2020 | 46 | 9 | 1 | 5,11 |
| OTCQ / 2021 | 31 | 6 | 1 | 5,17 |
| OTCQ / 2022 | 23 | 5 | 1 | 4,60 |
| OTCQ / 2023 | 51 | 10 | 1 | 5,10 |
| OTCQ / 2024 | 66 | 13 | 1 | 5,08 |
| OTCQ / 2025 | 35 | 7 | 1 | 5,00 |
| OTCQ / 2026 | 16 | 3 | 1 | 5,33 |
| OTCQ / OTC_HALA | 231 | 47 | 4 | 4,91 |

Toplam: evren 2.219, örneklem 450 + yedek 38; liste dosyası vdyt2b_orneklem.tsv (sha256 94499b18b6a160121aaaa3e31894c8bbc1ad4d2887417356f5d988de29e598dc).

## EK-3. A kapsamı (YALNIZ SAYI; `python -I VDYT2B.py kapsam`, 2026-11-12 17:39:57 UTC; kod dcc0148ad4a6)

| pazar | dönem | kaynak | VDYT2 (1) satırı G5 P1 | MA1 ölçülebilir | MA3 ölçülebilir | hisse | VDYT2 satırı G5 P0 | MA1 ölçülebilir P0 |
|---|---|---|---|---|---|---|---|---|
| BIST | WF | GERCEK | 1.600 | 1.600 | 1.600 | 304 | 3.803 | 3.803 |
| BIST | WF | DISARI | 3.120 | 3.120 | 3.120 | 319 | 11.909 | 11.909 |
| BIST | WF | RASTGELE | 1.597 | 1.597 | 1.597 | 304 | 7.009 | 7.009 |
| BIST | KASA | GERCEK | 1.349 | 1.349 | 1.349 | 325 | 2.964 | 2.964 |
| BIST | KASA | DISARI | 2.730 | 2.730 | 2.730 | 347 | 9.410 | 9.410 |
| BIST | KASA | RASTGELE | 1.175 | 1.175 | 1.175 | 282 | 5.163 | 5.163 |
| ABD | WF | GERCEK | 4.857 | 4.857 | 4.857 | 1.178 | 16.182 | 16.182 |
| ABD | WF | DISARI | 15.126 | 15.126 | 15.126 | 1.563 | 61.873 | 61.873 |
| ABD | WF | RASTGELE | 5.310 | 5.310 | 5.310 | 1.340 | 22.579 | 22.579 |
| ABD | KASA | GERCEK | 2.610 | 2.610 | 2.610 | 841 | 5.765 | 5.765 |
| ABD | KASA | DISARI | 7.209 | 7.209 | 7.209 | 1.025 | 21.458 | 21.458 |
| ABD | KASA | RASTGELE | 3.058 | 3.058 | 3.058 | 928 | 13.978 | 13.978 |

## EK-4. Eşik sözlüğü (mühür = sha256 of sıralı JSON)

```json
{
 "A": {
  "MA1": {
   "k_sigma": 3.0,
   "olcu": "max_k |ln(C[t+k]/C[t])|, k = 1..20 >= max(ln(1+taban), k_sigma x sigma x sqrt(20))",
   "taban_yuzde": 0.15
  },
  "MA2": {
   "k_sigma": 2.0,
   "olcu": "|ln(C[t+20]/C[t])| >= k_sigma x sigma x sqrt(20)"
  },
  "MA3": {
   "k_atr": 3.0,
   "olcu": "max_k TR[t+k], k = 1..20 >= k_atr x ATR250[t]"
  },
  "ana_etiket": "MA1",
  "ana_onkosul": "P1",
  "ana_tanim": "G5",
  "atr_min": 200,
  "atr_n": 250,
  "bh1_ayni_satir_tanim": [
   "G5"
  ],
  "bilgi_etiket": [
   "MA2",
   "MA3"
  ],
  "kontrol": {
   "DISARI": [
    "sembol",
    "yil",
    "natr_d"
   ],
   "RASTGELE": [
    "yil",
    "yas"
   ]
  },
  "ma23_tanim": [
   "G5"
  ],
  "pazarlar": [
   "BIST",
   "ABD"
  ],
  "satir": "VDYT2 (1) satırları aynen (tarih dönemde, son20 <= dönem sonu, y20 ölçülebilir) VE MA etiketi ölçülebilir (t+20 veri içinde, (t, t+20] kopukluk yok, sigma / ATR250 tanımlı)",
  "sigma_min": 200,
  "sigma_n": 250,
  "tablolar": [
   "satir",
   "kontrol"
  ],
  "ufuk": 20,
  "yon": "ilk eşiği aşan taraf (MA1: ilk aşan günün ln işareti; MA2: uç nokta işareti; MA3: ilk büyük TR gününün C - C[-1] işareti)"
 },
 "B": {
  "agirlik": "tabaka h: w_h = N_h / m_h (m_h = h'de verisi gelen örneklem sayısı; SPAC kalıbı ve kod değişikliği dahil: evren dışı payı N_h'yi aynı oranda küçültür); yaşayan (k60) satırlar w = 1",
  "bilgi": [
   "yalnız batanlar: gerçek / DIŞARI / RASTGELE oranları (ağırlıklı)",
   "batanlarda (2) / (3) bilgi: y20 = 1 satırlarda yukarı payı, r20 ortalaması, MAE"
  ],
  "cekim_sonrasi": {
   "D1_veri_yok": "HTTP 404 / boş / temiz bar < 252 -> VERİ YOK (yedekle değiştirilir; raporda listelenir)",
   "D2_spac_kalibi": {
    "aralik": [
     9.0,
     11.0
    ],
    "kural": "ham kapanışların >= %80'i [9, 11] $ aralığında -> SPAC kabuğu (evren dışı; değiştirilmez; raporda listelenir)",
    "pay": 0.8
   },
   "D3_uygun_gun_yok": "VDYT uygunluğu (>= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $) hiç sağlanmayan sembol ÇIKARILMAZ (evrenin üyesidir; satırı olmaz, ağırlık paydasında kalır)",
   "D4_yeniden_ad": {
    "korelasyon": 0.98,
    "kural": "son 60 barın günlük ln getirisi bir k60 serisiyle (ortak gün >= 55) korelasyon >= 0,98 VE ln(kapanış oranı) std <= 0,01 -> KOD DEĞİŞİKLİĞİ (aynı şirket yaşayan evrende; ör. CHK -> EXE) -> evren dışı (değiştirilmez; raporda listelenir)",
    "min_ortak": 55,
    "oran_std": 0.01,
    "son_bar": 60
   },
   "fiyat": "Tiingo ham açılış / yüksek / düşük / kapanış / hacim + splitFactor: bölünme düzeltmeli seri = ham / (gelecekteki bölünme oranlarının çarpımı) (Yahoo / k60 ile aynı tür: bölünme düzeltmeli, temettü düzeltmesiz); hacim x aynı çarpım; ekrandaki fiyat = ham kapanış (meta 'bolunme' ile V1.vdyt_bolunme_carpan aynı sonucu verir); V1.vdyt_bar_temizle + 2010-01-01 .. 2026-08-31 kesiti"
  },
  "etiket": [
   "y20",
   "MA1"
  ],
  "evren": {
   "asset": "Stock",
   "ayrik_otc_gun": 10,
   "bes_harf_at": "FGHIMNOPRSTUVWXYZ",
   "borsa": [
    "NYSE",
    "NASDAQ",
    "NYSE MKT",
    "AMEX"
   ],
   "k60_klasor": "/tmp/k60_fiyat",
   "kod_regex": "^[A-Z]{1,5}$",
   "kural": [
    "1 tür: assetType Stock, priceCurrency USD",
    "2 kod: ^[A-Z]{1,5}$ (nokta / tire / rakam yok: imtiyazlı, sınıf, birim); 5 harfli kodlarda son harf F G H I M N O P R S T U V W X Y Z ise atılır (yabancı, tahvil, imtiyazlı, hak, fayda payı, varant, birim, when-issued, fon, ADR); Q (iflas) ve A-E, J-L kalır",
    "3 yinelenen kod: aynı kod listede birden çok Stock kaydıyla geçiyorsa (kod yeniden kullanımı; API hangi seriyi verir belirsiz) atılır",
    "4 k60'ta olan kod atılır (yaşayan evren zaten VDYT2'de)",
    "5 BORSA kaynağı: exchange ∈ borsa, endDate ∈ [son_bas, son_bit], startDate <= endDate - 400 gün",
    "6 OTCQ kaynağı: exchange ∈ otc, kod ^[A-Z]{3,4}Q$ (iflas eki), endDate >= son_bas, startDate <= min(endDate - 400 gün, otcq_bas_ust); AYRIK OTC dönemi (ilk 3 harfi aynı bir borsa kaydının endDate'i Q kaydının startDate'inden en çok 10 gün önce / sonra) atılır (borsa dönemi BORSA kaynağında)",
    "7 SPAC kabuğu (çekim öncesi): kod + U ya da kod + -U birim kaydı varsa VE birimin endDate'i >= kodun endDate'i - 30 gün (birleşmeden önce tasfiye / birleşme yok) atılır; birleşip yaşayan / sonra batan şirket (birimi erken biten) KALIR"
   ],
   "min_omur_gun": 400,
   "otc": [
    "PINK",
    "OTCMKTS",
    "EXPM",
    "OTCGREY",
    "OTCQB",
    "OTCQX",
    "OTCBB",
    "OTCCE",
    "OTCD"
   ],
   "otcq_bas_ust": "2025-06-30",
   "otcq_regex": "^[A-Z]{3,4}Q$",
   "para": "USD",
   "son_bas": "2019-02-01",
   "son_bit": "2026-06-30",
   "spac_unite_ek": [
    "U",
    "-U"
   ],
   "spac_unite_gun": 30
  },
  "kolon": [
   "sembol",
   "kaynak",
   "t",
   "tarih",
   "yil",
   "yas",
   "natr_d",
   "P1",
   "P2",
   "y20",
   "son20",
   "yon",
   "r20",
   "mae",
   "ma1",
   "ma1_yon",
   "w"
  ],
  "onkosul": [
   "P0",
   "P1",
   "P2"
  ],
  "orneklem": {
   "dagitim": "orantılı, en büyük kalan; N_h > 0 ise en az 1",
   "n": 450,
   "otcq_hala": "OTCQ'da endDate > son_bit ise son_yil = 'OTC_HALA' (hâlâ OTC'de işlem görüyor)",
   "sira": "tabaka içinde numpy default_rng(tohum + tabaka sırası) permütasyonu; ilk n_h ANA, sonraki y_h YEDEK",
   "tabaka": [
    "kaynak",
    "son_yil"
   ],
   "tohum": 20261117,
   "yedek": 38,
   "yedek_kural": "YEDEK yalnız aynı tabakada VERİ YOK (HTTP 404 / boş / temiz bar < 252) olan ANA sembolün yerine, sırayla; başka hiçbir nedenle (sonuç, getiri, etiket) yedek kullanılmaz ve sembol çıkarılmaz"
  },
  "panel": "ABD paneli k60 + batan örneklemi BİRLİKTE (V1.vdyt_panel; uygunluk, NATR ondalığı, tertiller); batan satırları bu panelle V2._v2_hisse_is (tanım yalnız G5); yaşayan satırlar VDYT2 tablolarından AYNEN (yeniden hesaplanmaz)",
  "pilot": {
   "basin_kapanis": {
    "SIVBQ": [
     [
      "2023-03-09",
      106.04,
      "basın: SVB hissesi 9 Mart 2023'te %60 düşüşle 106,04 $ kapandı"
     ]
    ]
   },
   "karar": {
    "gecti": "K1 VE K2 VE K3 VE K5 VE K6 VE (K4 değerlendirildiyse K4)",
    "guvenilir_min": 10,
    "kismen_min": 7,
    "q_hepsi_kaldi": "Q türünün HİÇBİRİ geçmezse OTCQ tabakası B'den çıkarılır (beyan; örneklemden düşer, ağırlıkta yer almaz)",
    "yeniden_karisik": "iki YENIDEN sembolünün ikisi de KARIŞIK ise karar en çok KISMEN"
   },
   "kos_izin": [
    "GÜVENİLİR",
    "KISMEN"
   ],
   "olcut": {
    "K1_seri": "HTTP 200 ve kapanışı > 0 en az 252 bar",
    "K2_son_gun": "BORSA: son bar ∈ [F25 - 60 iş günü, F25 + 10 iş günü] (borsa önce işlemi durdurur, Form 25 sonra; Kural 12d2-2); Q: son bar >= F25 - 60 iş günü ve seride [F25 - 60, F25 + 10] iş günü penceresinde en az 1 bar (borsa dönemi kotasyondan çıkışa kadar seride); YENIDEN: seride F25 - 60 iş gününden önceki 60 iş gününde bar var (eski şirketin dönemi seride)",
    "K3_bosluk": "A = (BORSA: son bar; Q / YENIDEN: F25 - 60 iş günü); [A - 60 iş günü, A] penceresinde eksik iş günü <= 5 ve en uzun boşluk <= 5 iş günü (iş günü: ABD federal tatil takvimi)",
    "K4_tutarlilik": "kaynak varsa: basın kapanışı ±%10 içinde (bölünmesiz ham kapanış); Yahoo örtüşmesi: ortak günlerde günlük log getiri korelasyonu >= 0,90 ve |kapanış oranı - 1| medyanı <= %2 (bölünme düzeltmeli); kaynak yoksa DEĞERLENDİRİLMEDİ (karara girmez)",
    "K5_ohlcv": "barların >= %95'inde açılış / yüksek / düşük / kapanış / hacim dolu ve yüksek >= düşük ve kapanış > 0",
    "K6_karisma": "YENIDEN: seri hem eski (yeni_bas'tan önceki 250 iş günü) hem yeni dönemi (yeni_bas'tan sonraki 250 iş günü) içeriyorsa aralarında >= 30 iş günü boşluk olmalı (ayırt edilebilir); yoksa KARIŞIK. Diğerleri: bölünme günü olmayan |günlük ln getiri| > ln 10 sıçrama yok"
   },
   "semboller": [
    {
     "cik": 719739,
     "f25": "2023-05-02",
     "kod": "SIVBQ",
     "liste": "PINK 1990-03-26 .. 2026-11-11",
     "sirket": "SVB Financial Group",
     "tur": "Q"
    },
    {
     "cik": 886158,
     "f25": "2023-07-10",
     "kod": "BBBYQ",
     "liste": "PINK 1992-06-05 .. 2023-09-29",
     "sirket": "Bed Bath & Beyond",
     "tur": "Q"
    },
    {
     "cik": 84129,
     "f25": "2023-10-31",
     "kod": "RADCQ",
     "liste": "PINK 1984-12-17 .. 2026-11-11",
     "sirket": "Rite Aid",
     "tur": "Q"
    },
    {
     "cik": 1813756,
     "f25": "2023-11-22",
     "kod": "WEWKQ",
     "liste": "EXPM 2020-10-21 .. 2024-06-11",
     "sirket": "WeWork",
     "tur": "Q"
    },
    {
     "cik": 1310067,
     "f25": "2018-11-15",
     "kod": "SHLDQ",
     "liste": "EXPM 2003-05-01 .. 2022-10-31 (SHLD bugün ETF)",
     "sirket": "Sears Holdings",
     "tur": "Q"
    },
    {
     "cik": 1657853,
     "f25": "2020-10-30",
     "kod": "HTZGQ",
     "liste": "PINK 2006-11-16 .. 2021-06-30",
     "sirket": "Hertz Global (eski hisse)",
     "tur": "Q"
    },
    {
     "cik": 887921,
     "f25": "2022-10-21",
     "kod": "REVRQ",
     "liste": "PINK 1996-02-29 .. 2023-05-24",
     "sirket": "Revlon",
     "tur": "Q"
    },
    {
     "cik": 716006,
     "f25": "2023-09-08",
     "kod": "YELLQ",
     "liste": "OTCMKTS 1986-07-09 .. 2026-07-01",
     "sirket": "Yellow Corp",
     "tur": "Q"
    },
    {
     "cik": 945764,
     "f25": "2020-08-17",
     "kod": "DNR",
     "liste": "NYSE 1995-09-06 .. 2020-07-30 (DNRCQ ayrı)",
     "sirket": "Denbury Resources",
     "tur": "BORSA"
    },
    {
     "cik": 1502034,
     "f25": "2020-07-01",
     "kod": "GNC",
     "liste": "NYSE 2011-04-01 .. 2020-06-30 (GNCIQ ayrı)",
     "sirket": "GNC Holdings",
     "tur": "BORSA"
    },
    {
     "cik": 945436,
     "f25": "2016-05-06",
     "kod": "SUNE",
     "liste": "iki kayıt: NYSE 1995-07-13 .. 2016-04-21 ve NASDAQ 1990-03-26 .. 2026-11-11",
     "sirket": "SunEdison (kod bugün SUNation)",
     "tur": "YENIDEN",
     "yahoo_karsilastir": "k34_yahoo SUNE (bugünkü şirket)",
     "yeni_bas": "2016-04-22"
    },
    {
     "cik": 895126,
     "f25": "2020-07-20",
     "kod": "CHK",
     "liste": "NASDAQ 1993-02-16 .. 2024-10-04; CHKAQ NYSE 2021-03-17 .. 2021-05-17; EXE 2021-02-10 ..",
     "sirket": "Chesapeake Energy (2020 iflas; eski hisse 2021-02-09 iptal, yeni hisse 2021-02-10, aynı kod)",
     "tur": "YENIDEN",
     "yahoo_karsilastir": "k60_fiyat EXE (yeni hisse; 2021-02-10 .. 2024-10-01 örtüşme)",
     "yeni_bas": "2021-02-10"
    }
   ]
  },
  "tanim": "G5",
  "tiingo": {
   "anahtar_ortam": "TIINGO_API_KEY",
   "anahtar_yok": "proxy",
   "art_arda_429_dur": 3,
   "ay_sembol": 500,
   "baslangic": "2010-01-01",
   "bekle_429": 900,
   "bitis": "2026-08-31",
   "fiyat_url": "https://api.tiingo.com/tiingo/daily/{kod}/prices",
   "gun_istek": 900,
   "liste_url": "https://apimedia.tiingo.com/docs/tiingo/daily/supported_tickers.zip",
   "saat_istek": 45,
   "zaman_asimi": 60
  }
 },
 "basari": {
  "bootstrap": 2000,
  "guven": [
   2.5,
   97.5
  ],
  "kume": "hisse",
  "tohum": 20261112
 },
 "donem": {
  "kasa": [
   "2024-01-01",
   "2026-08-31"
  ],
  "wf": [
   "2019-01-01",
   "2023-12-31"
  ]
 },
 "karar": {
  "A": "(1)-MUTLAK BAŞARILI <=> ANA (G5, P1), etiket MA1: gerçek - DIŞARI (tabakalı) fark > 0 ve %95 alt > 0 VE gerçek - RASTGELE fark > 0 ve alt > 0; WF'de VE KASA'da; BIST ve ABD AYRI. n < 30 ya da tek sınıf -> VERİ YOK",
  "B": "(1)-BATANLAR DAHİL BAŞARILI <=> ABD, ANA (G5, P1), birleşik ağırlıklı evren: aynı kural (iki kontrol, WF VE KASA); etiket y20 (BH1; VDYT2 ile aynı) ve MA1 ayrı sütun"
 },
 "kesik": "2026-08-31",
 "surum_etiket": "v2b_20261112",
 "vdyt2": {
  "esik_sha": "3051e5b8ddd99c7c42e36f106bdaede734e8dac5ed6588029c5d50bc2274f5a8",
  "karar": "Ç163: (1) BAŞARILI, (2) ve (3) BAŞARISIZ (DEĞİŞMEZ)",
  "kod_sha": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",
  "onkayit_commit": "f13b96e",
  "vdyt_kod_sha": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d"
 }
}
```
