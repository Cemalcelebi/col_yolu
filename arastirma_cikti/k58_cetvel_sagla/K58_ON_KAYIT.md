# K58 ÖN KAYIT — cetvel sağlaması (ölçüm aletinin kalibrasyonu)

Yazım zamanı: 2026-11-10 19:19:52 UTC (2026-11-10 22:19 TR) (ölçümden ÖNCE; gerçek getiriler üzerinde hiçbir ölçüm koşulmadı). Sürüm: K58 v1.0 (2026-11-10): cetvel sağlaması (FI_OLCUT gücü, French pozitif kontrol, portföy cetveli kalibrasyonu, C4 trend filtresi)
ESIK_SHA256: 5aec67198fe98771d8b8f20db6dbbfea5fe6a047ff8101948a050a311e83e347
(K58_ESIK + FI_OLCUT'un sha256'sı. `python -I K58.py kos` bu mühürle başlar; eşik değişirse koşu durur.)
Veri: V_ABD.pkl sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e; V_BIST.pkl sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51

## 0. Soru
~150 çalışmada iz çıkmadı. Hipotez: 'hiçbir şey bulamamamızın nedeni piyasa değil ölçüm aletimiz'. Ana model denetimi (K57 hücreleri):
FI_OLCUT 60 gün eşli farkının %95 aralık yarı genişliği n <= 30'da ≈ %17, n 30-100'de ≈ %13, n 300-1000'de ≈ %3,4, n > 1000'de ≈ %2,3.
Gerçekçi sağlam anomaliler 60 günde ≈ %1-3. Ayrıca 60 gün momentum x likidite eşlemesi bilinen etkileri tasarım gereği siler (K42).
K58 aleti bilinen girdilerle sınar; yeni iz aramaz.

## A. FI_OLCUT GÜCÜ (gerçek ABD paneli, plasebo olay + bilinen δ)
- Panel: V_ABD.pkl, FON_IZI fi_olcut_panel (FI_OLCUT değiştirilmeden; kod içe alınır, kopyalanmaz).
- Plasebo olay: rastgele (gün, hisse) hücresi; giriş günü 2016-01-01 .. 2026-08-31 (kriz kesiği 2026-08-31: r60 penceresi kesiği aşan
  olay zaten 'ok' değildir). Geçerli hücre = FI 'ok' (r60, momentum, likidite, açılış var) VE aynı gün aynı momentum x likidite
  hücresinde en az 3 eş (fi_olcut_olay'ın eş şartı). Bütün geçerli hücreler arasından eşit olasılıkla, yerine koymadan çekilir
  (uzun geçmişli hisse daha çok çıkar; gerçek olaylar gibi).
- n ∈ [30, 100, 300, 1000, 3000]; δ ∈ ['0%', '1%', '2%', '4%', '8%', '16%']; her (n, tekrar) için olay kümesi BİR KEZ çekilir ve bütün δ'larda
  aynı küme kullanılır (ortak rastgele sayı). Tohum = numpy default_rng([58, n, tekrar]). 200 tekrar.
- δ enjeksiyonu: olayın r60'ına δ eklenir (eşler dokunulmadan): r60' = r60 + δ, fark' = r60' - eşli r60, sıra' = eşlerin r60'ından
  küçük olanların payı (eşitlik yarım) r60' ile yeniden; slot portföyü r60' ile, rastgele eş portföyleri eşlerin değişmemiş r60'ı ile.
- Hücre testi: FON_IZI fi_olcut_hucre (bootstrap 2000, tohum 27, slot 10, 200 rastgele portföy) ve
  TUTAR kararı FON_IZI fi_olcut_karar ile (dört karar hücresi aynı sonuçla doldurulur; 'İZ' dönerse hücre TUTAR): n >= 30,
  ortalama eşli fark > 0 ve %95 alt uç > 0, sıra > 0,50, portföy > rastgele %90.
- GÜÇ(n, δ) = tutan tekrar payı; δ = 0 yanlış pozitif oranı. Bilgi: şart başına geçme payı, ortalama aralık yarı genişliği
  ((üst - alt) / 2), dört hücrenin birlikte tutma olasılığı ≈ güç^4 (bağımsızlık varsayımıyla; gerçek İZ kararı dört hücre ister).
- Not: plasebo olaylar on yıla yayılır (gerçek karar hücresi bir-üç yıl); ay kümeli aralık ay sayısına bağlıdır, bu yüzden buradaki güç
  gerçek hücreninkinden İYİMSER (üst sınır) okunur.

## B. POZİTİF KONTROL: Kenneth French veri kütüphanesi (hayatta kalma yanlılığı yok)
- Dosyalar: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip ve F-F_Momentum_Factor_CSV.zip (aylık, %); /tmp/k58_french/ altına inerler,
  güvenilmeyen veri: zip açılmaz, bellekte okunur, ayrıştırma ayrı `python -I` alt sürecinde boş bir klasörde.
- Faktörler: MKT_RF, SMB, HML, RMW, CMA, UMD (UMD = 'Mom'). Aylık bölüm alınır, yıllık bölüm atılır; [-99.99, -999.0] eksik sayılır.
- Dönemler: 1963-2026, 2000-2026, 2000-09, 2010-19, 2020-26. Her faktör x dönem: aylık ortalama %, yıllık (x12), t (ortalama / (sd / √T)),
  Newey-West t (gecikme 6), Sharpe (ortalama / sd x √12; faktörler zaten fazla getiri), artı ay payı.
- İşaret tutarlılığı: alt dönemlerde (2000-09, 2010-19, 2020-26) ortalaması > 0 olanların sayısı ve tam dönemle aynı işaret.
- BİLGİ: portföy cetvelinin (C) şartları 2000-2026 dönemine uzun-kısa faktörlere uygulanır (ortalama > 0, NW t > 2.0,
  3 alt dönemin en az 2'sinde > 0, son %30 ayda > 0). Karar rolü yok; 'bilinen etki cetvelden geçer mi'.
- Beklenti (önceden): MKT-RF, RMW, UMD 1963-2026'da t > 2; HML ve SMB 2000 sonrası zayıf; UMD 2020-26'da zayıf/eksi olabilir.

## C. PORTFÖY CETVELİ (önerilen; burada kalibre edilir, benimsenmez)
- Panel: V_ABD ve V_BIST (fi_k1_veri çıktısı), günlük kapanış 2026-08-31'de kesik (iki pazar için aynı FI_OLCUT kesiği).
- Ay sonu = her ayın panel takvimindeki son işlem günü. Ay sonu kapanışı = o güne kadar son kapanış (en çok 5 gün ileri taşıma).
  Ay getirisi (k -> k+1) = sonraki ay sonu kapanışı (sınırsız ileri taşıma: işlem görmeyen hisse son fiyatında kalır) / ay sonu kapanışı - 1.
- Evren U(k) = ay sonu k, k-1 ve k-12 kapanışı olan hisseler (bütün sinyaller için aynı; yalnız k ve öncesi bilgi).
  U < 50 olan ay atlanır. Oluşum ayları: ay sonu >= 2016-01-01 ve sonraki ay sonu <= kesik.
- Sinyal ay sonu k'da yalnız k ve öncesi kapanışlarla hesaplanır (GELECEĞE BAKMA YOK; test_k58 sınar). İşlem ay sonu kapanışında.
- Portföy: U içinde sinyale göre en üst %10 (sayı = max(1, yuvarla(0.1 x |U|))), eşit ağırlık, aylık yeniden dengeleme.
  Maliyet tek yön ABD 10 bp, BIST 30 bp: maliyet = oran x devir, devir = Σ|w_yeni - w_kaymış|
  (ilk ay alım = 1). Kıyas: U'nun eşit ağırlıklı getirisi (maliyetsiz; strateji için sert).
- İstatistik: aylık fazla e = net portföy - kıyas. Yıllık fazla = 12 x ortalama e; Newey-West t (gecikme 6); portföy Sharpe
  (net, rf = 0, x √12) ve bilgi oranı (ort e / sd e x √12).
- CETVEL TUTAR ⇔ (1) tam örneklemde ortalama e > 0 VE NW t > 2.0; (2) ayların ardışık eşit 3 parçasının
  en az 2'sinde ortalama e > 0; (3) son %30 ayda (yukarı yuvarlanmış) ortalama e > 0 (örneklem dışı).
- C1 POZİTİF KONTROL: 12-1 momentum = kapanış(k-1) / kapanış(k-12) - 1 (ay sonları).
- C2 PLASEBO: 200 rastgele sinyal (her ay U içinde rastgele sıra; tohum 5800 + i). Yanlış pozitif oranı = TUTAN payı,
  hem maliyetli (cetvelin kendisi) hem maliyetsiz (brüt) cetvelle. Maliyet yüksek devirli rastgele portföyü zaten cezalandırdığı için
  karar (D2) BRÜT orana bakar (daha sert olanı; düşük devirli gerçek sinyal maliyetle elenmez).
- C3: K57 V1 benzeri olay kuralının aylık sinyale çevrilmesi K58'in KAPSAMINDA DEĞİL.
- HAYATTA KALMA: V_ABD yalnız bugün yaşayan hisseler (survivors); evren ve portföy aynı yanlılığı taşır, fark kısmen silinir ama sıfır
  değildir (batanlar momentum kaybedenlerinde yoğun). Yanlılıksız kontrol B'dir (French).

## C4. TREND FİLTRESİ (Cemal: 'SMA üstüne atılımla kazanılır mı?'; ana oturum ek işi, ölçümden önce)
- (a) ENDEKS DÜZEYİ: SPY (ABD) ve XU100.IS (BIST), Yahoo chart API günlük veri (1990-01-01 .. 2026-09-01), 2026-08-31'de kesik.
  SPY temettü düzeltmeli (adjclose oranı açılış ve kapanışa); XU100 fiyat endeksi (temettüsüz; iki strateji için aynı). Endeks
  günlük kapanış oranı 1/1000 - 1/10 ya da 10 - 1000 aralığında ise sıfır atma / yeniden tabanlama sayılır,
  önceki seri o oranla ölçeklenir ve raporda yazılır.
  Kural: gün t kapanışı > SMA200(t) (t dahil son 200 kapanış) ise ELDE, değilse NAKİT (getiri 0; faiz yok: filtre aleyhine).
  İşlem ertesi gün AÇILIŞINDA; maliyet tek yön ABD 10 bp / BIST 30 bp. Gece getirisi (kapanış t-1 -> açılış t)
  önceki gün pozisyonuyla, gün içi (açılış t -> kapanış t) yeni pozisyonla kazanılır. Al-tut: hep elde.
  Dönem: SPY 2000-01-01 .. 2026-08-31; XU100 verinin başladığı yıldan (SMA200'ün tanımlı olduğu ilk takvim yılı başı) .. 2026-08-31;
  alt dönemler 2000-09, 2010-19, 2020-26 (verinin olduğu kadar). Ölçüler: yıllık getiri (bileşik, 252 gün), en büyük
  düşüş (MDD), Sharpe (günlük, rf = 0, x √252), piyasada kalma payı, işlem sayısı.
  KARAR (tam dönem, endeks başına): 'RİSK FİLTRESİ OLARAK TUTAR' ⇔ filtre yıllık getirisi al-tut'un %90'ından az değil
  (al-tut yıllık getirisi <= 0 ise filtre >= al-tut) VE |MDD filtre| <= (1 - 0.3333) x |MDD al-tut| (en az 1/3 küçük). Aksi 'TUTMAZ'.
- (b) HİSSE DÜZEYİ (C'nin evreni, ay sonları, maliyeti ve PORTFÖY CETVELİ şartlarıyla; üst %10 değil, şartı sağlayan bütün hisseler eşit ağırlık):
  C4b-1 'SMA200 üstü': ay sonu kapanışı > günlük SMA200.
  C4b-2 'atılım': ay sonu kapanışı > SMA200 VE kapanış > SMA20 ve > SMA50 VE önceki 20 işlem gününün en az birinde
  kapanış SMA20 ya da SMA50'nin üstünde DEĞİLDİ (son 20 günde ikisinin üstüne çıkmış).
  SMA'lar günlük kapanıştan (5 gün ileri taşımalı), tam pencere şart. Şartı sağlayan hisse yoksa ay nakit (getiri 0).
  KARAR: portföy cetvelinin (C) üç şartı, pazar başına (ABD karar, BIST bilgi).
  BİLGİ (karar rolü yok): eşli plasebo = her ay aynı sayıda hisse U'dan rastgele (200 tekrar, tohum 5900 + i);
  sinyalin NW t'sinin plasebo dağılımındaki yüzdeliği (geniş tutulan portföyde üst %10 plasebosu kıyaslanamaz).

## D. KARAR KURALLARI (şimdi yazıldı; sonuçtan sonra değişmez)
1. FI_OLCUT gücü δ = +%2 ve n <= 300 (n ∈ [30, 100, 300]) için en yüksek değer < %20 ise
   BULGU olarak yazılır: 'FI_OLCUT küçük etkiyi göremiyor'.
2. Portföy cetveli ABD'de C1 momentumu kabul ederse (maliyetli) VE C2 plasebo yanlış pozitif oranı (brüt; maliyetli de ayrıca) <= %5
   ise 'KALİBRE ADAY STANDART' olarak yazılır. BIST bilgi olarak raporlanır. Benimsemek Cemal'in kararıdır (CLAUDE.md test standardı değişikliği).
   C1 ABD'de tutmazsa ve French UMD 2010-19 / 2020-26'da da zayıfsa başarısızlık döneme yazılır; yine de benimseme önerilmez.
3. C4a: endeks başına yukarıdaki risk filtresi kuralı. C4b: portföy cetveli şartları. Tutan C4 sonucu İZ değildir; CLAUDE.md test standardı
   (FI_OLCUT, ABD + AVR) değişmedikçe yalnız 'cetvel C altında tutar' diye raporlanır.
4. Yukarıdaki bütün eşikler sabittir; sonuç görüldükten sonra değiştirilmez. Kod hatası düzeltmesi gerekirse ön kayıt değişmez, düzeltme
   raporda ayrıca yazılır.

## E. Beklenti (önceden)
A: δ = 0'da yanlış pozitif ≈ %0-3; n = 30-300'de δ = +%2 gücü düşük (< %20) beklenir, n = 3000'de δ = +%2 orta-yüksek. C1: ABD 2016-26
momentum zayıf dönem (2020-22 çöküşleri); cetvelin kabul etmemesi olası. C2: brüt yanlış pozitif ≈ %2-5. C4a: SPY'de MDD belirgin küçülür,
getiri al-tut'un %90'ının altında kalabilir; XU100'de TL enflasyonu yüzünden filtre uzun süre elde kalır. C4b: belirsiz.

## F. Faz 2 komutu (ön kayıt git'e işlendikten SONRA)
`cd /home/user/col_yolu && python -I K58.py kos --bolum hepsi --islem 4`
