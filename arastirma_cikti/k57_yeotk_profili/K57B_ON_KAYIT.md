# K57-B ÖN KAYIT — V1 çevresinde önceden yazılı 3 devam (YEOTK profili, 'sıkı dosya')

Yazım zamanı: 2026-11-09 18:12:08 UTC (2026-11-09 21:12 TR) (K57-B ölçümünden ÖNCE; K57-B sonucu görülmedi). Sürüm: K57-B v1.0 (2026-11-09): V1 çevresinde önceden yazılı 3 devam (B1 geniş ABD evreni, B2 20 gün ufuk, B3 F3'süz)
K57B_SHA256: abc73b49f1df30c1d4fff698a154b08a9bef684e673d9dad7eaf801e77583457
(K57B_ESIK + FI_OLCUT + K57_ESIK + K57_ATLA sha256'sı. `python K57.py b_kos` bu mühürle başlar; biri değişirse koşu durur.)
K57 mührü (değişmeden): 2a6cc6f6d1fd52e7dc9e7711f580c145a3c87f59369b12e40c4052fe1ce4b1f0 (K57_ON_KAYIT.md; b_kos onu da doğrular).

## 1. Neden
K57 (Ç148, ön kayıt 2026-11-09 15:29 UTC) İZ DEĞİL verdi. Eşiğe en yakın hücre V1 = F7 (bilanço gününe güçlü tepki) + F1 (büyüme)
+ F2 (ivme) + F3 (bilanço), fiyat şartı (F6) YOK: ABD 2023 +%19,7 (n 7), ABD 2024-26 +%10,3 (n 31, aralık -%7,9..+%29,7, portföy %89,5),
BIST 2024-26 +%6,3 (n 96, portföy %99). F6 eklenince eksiye döndü. K57'nin 7. bölümündeki 3 devam (D1-D3) koşuldu, iz yok.
Bu üç deneme K57 sonucu görüldükten SONRA, kendi sonuçları görülmeden yazıldı (IZ_DEFTERI 9 Kas akşam satırı).

## 2. Ortak kurgu (K57 ile aynı; değişmez)
- Olay, tepki, giriş: K57 / K28 (fi_k28_olaylar). Giriş = tepki gününden sonraki ilk işlem günü açılışı. Fiyatlar 2026-08-31'de kesik.
- Süzgeçler K57_ESIK'teki tanımlarla: F7 'ear' D'ye kadar son 92 günde tepki günü biten olayların üst %20'ı VE ham
  >= +%5; F1 ABD çeyrek satışı yıllık >= +%25 (BIST kayan üst %40); F2 satış >= 1.4 x önceki iki
  çeyrek ortalaması VE kâr > 0 VE > önceki çeyrek; F3 ABD yükümlülük <= 3.0 x özkaynak (BIST net borç / özkaynak < 2.0).
  Temel değerlerin bilgi tarihi <= D (K57 kuralı).
- Ölçüt FI_OLCUT (değiştirilmeden): eşli fark (aynı gün, aynı 60 gün momentum beşliği x 20 gün likidite üçlüsü), ay kümeli bootstrap
  (2000) %95 aralık, hücre içi sıra, 10 yuvalı slot portföyü vs 200 eşli rastgele portföy.
- Hücreler (giriş gününe göre): ABD 2021-22 BİLGİ, ABD 2023 KARAR, ABD 2024-26 KARAR; BIST 2022-23 ve 2024-26 BİLGİ.

## 3. Üç deneme
- B1 'geniş ABD evreni' (V1, 60 gün): evren = önbellekteki SEC frames'te gelir (Revenues / RevenueFromContractWithCustomerExcludingAssessedTax /
  SalesRevenueNet) çeyreklik + NetIncomeLoss çeyreklik + StockholdersEquity anlık değeri olan VE company_tickers.json'da borsa kodu olan
  bütün şirketler (aynı CIK'nin ilk kodu, K57 eşlemesi). Günlük fiyat Yahoo chart API'sinden (https://query1.finance.yahoo.com/v8/finance/chart/{T}, period1 2020-01-01,
  period2 2026-09-01, interval 1d; tarayıcı User-Agent; ssl cafile /root/.ccr/ca-bundle.crt; çağrılar arasında 0.3 sn bekleme,
  3 iş parçacığı, 429/403'te geri çekilme, 4 deneme; önbellek /tmp/k57b_fiyat/). Fiyat bölünme + temettü düzeltmeli
  (adjclose / close oranı OHLC'ye uygulanır; V_ABD ile aynı biçim), 2026-08-31'de kesilir. Yalnız Yahoo instrumentType EQUITY ve en az
  150 işlem günü olanlar. Olay günleri K57 ile aynı kaynak (Nasdaq takvimi 2022-12 sonrası; SEC 10-Q / 10-K başvuru günü
  2021-01 .. 2022-11).
  LİKİDİTE TABANI: tepki gününde biten 20 işlem günlük (tepki günü dahil, en az 20 gözlem) medyan işlem değeri
  (Close x Volume, düzeltmeli fiyat) >= 1,000,000 $. Taban altı olaylar olay kümesine HİÇ girmez; F7'nin kayan eşiği taban üstü olaylardan
  hesaplanır. Eşler (FI_OLCUT eşleştirmesi) aynı geniş evrenin bütün hisselerinden (FI_OLCUT paneli değiştirilmeden; taban eşlere uygulanmaz).
  Tepki için piyasa medyanı geniş evrenden (fi_k28_olaylar).
  YAHOO ENGELİ: 25 ardışık hisse bütün denemelerden sonra inemezse indirme durur; B1 inen hisselerle koşulur ve kaç
  hisse indiği raporda yazılır.
- B2 '20 gün ufuk' (V1): FI_OLCUT ufku 20 işlem günü (r20 = 20. gün kapanışı / giriş açılışı - 1; eşli fark, aralık, sıra aynı; slot
  portföyü 10 yuva, 20 gün tut). Özgün evrenler (V_ABD, V_BIST) ve K57'nin olayları (olaylar_abd.csv, olaylar_bist.csv; K57 mühürlü koşusu).
- B3 'F3'süz' (F7 + F1 + F2, 60 gün): özgün evrenler ve K57 olayları.
- Denetim: B2 / B3 K57 olay dosyalarından okunur; koşu önce K57 ANA V1 hücrelerini aynı dosyalardan yeniden üretir (n ve ortalama eşli
  fark hucre.csv ile aynı olmalı), değilse durur.

## 4. Karar (değişmez)
Her deneme ayrı okunur: ABD 2023 ve ABD 2024-26 hücreleri FI_OLCUT dört şartıyla (n >= 30; ortalama eşli fark > 0 ve aralık alt ucu > 0;
sıra > 0,50; portföy > eşli rastgele %90). İkisi de tutarsa 'ABD-ADAY (AVRUPA VERİSİ YOK)' (Avrupa'da bilanço olay verisi
yok, İZ denemez); BIST de iki hücrede tutuyorsa '+ BIST' bilgisi. Aksi 'İZ DEĞİL'. BIST yalnız bilgi. Sonuç görüldükten sonra eşik değişmez.
Çoklu deneme: K57'de 5 varyant + 3 devam, burada 3 deneme daha; bir B denemesinden çıkan ABD-ADAY aday sayılır, örneklem dışı
(canlı) izleme olmadan üretim kuralına girmez.

## 5. Beklenti (önceden)
B1: n büyür (V_ABD 1.411 hayatta kalan yerine ~4.000+ şirket); küçük şirketlerin gürültüsü ortalamayı oynatır, aralık daralır.
B2: 20 günde bilanço sonrası sürüklenme (PEAD) daha görünür olabilir ama n aynı (ABD 2023 n 7 < 30: B2'de ABD 2023 tutamaz).
B3: F3 kalkınca n biraz büyür; bilanço zayıf şirketler girer. Üçünün de iki ABD hücresinde birden tutma olasılığı düşük.

## 6. K57-B de iz vermezse sıradaki 3 (önceden yazıldı; bu görevde KOŞULMAZ, ana oturum karar verir)
- C1: V1 + F4 (seyrelme yok) geniş ABD evreninde, 60 gün.
- C2: V1 geniş ABD evreninde, likidite tabanı 5 milyon $.
- C3: V1 geniş ABD evreninde, F7 yerine yalnız 'ear' üst %10 (ham şartı aynı).
