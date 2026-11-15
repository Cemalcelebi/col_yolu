# İŞ TANIMI — S6 TABAN: Cemal'in çöl kurallarından çalışan algoritma (Python referans + tasarım sınaması) ve Pine göstergesi

Yazan: ana model, 15 Kas 2026. Yapan: alt ajan A (yazıcı). Denetleyen: alt ajan B (bağımsız; Pine sözdizimi + Python birebirliği) ve ana model.
Cemal (15 Kas): "şimdi yeniden bu yeni yazdığın metriklerden koşan bir Pine yaz; burada artık hata görmek istemiyorum." Kurallar: arastirma_cikti/sikisma_obek/CEMAL_COL_KURALLARI.md (K1-K8, K6b) ve 16 etiket tablosu. ÖNCE BUNU OKU.

## 0. ÖN UÇUŞ KONTROLÜ (zorunlu)
ÖN UÇUŞ KONTROLÜ (zorunlu; hata defterinden): kod yazmaya başlamadan önce oku, ön kayıt dosyasına KONTROL LİSTESİ tablosunu (`python IZ_KARNE.py kontrol`) doldurarak koy, raporunda 'HATA' başlığıyla bulduğun her hatayı ayrı listele.
- K1 kontrol grubu: Eşler aynı giriş günü, aynı momentum x likidite hücresi, aynı giriş / çıkış geometrisi mi; taban rastgele olay sağlamasıyla (200 eş portföy) mi? Mekanik üstünlük (sinyal tanımının kendiliğinden ürettiği fark) dışlandı mı? [geçmiş: 22 kez (H005, H006, H026-H032, H055, H064, H100...)]
- K2 geleceğe bakma: Her girdi alanının bilgi tarihi <= karar günü ve bu KODDA mekanik denetleniyor mu? Satır tarihi mi (sayfa / haber tarihi değil)? Etiket, evren listesi, sektör karar günündeki haliyle mi? [geçmiş: 12 kez (H003, H016, H034, H051, H130...)]
- K3 geçerli bar: H>L ve V>0 olmayan bar sinyal ya da ölçü üretmiyor mu; hacim 0 gün fiyatı bayat sayılıyor mu; seans açıkken yarım bar atılıyor mu? [geçmiş: 2 kez aynı hata (H004, H037), H134, H141]
- K4 tekilleştirme: Aynı hissede olay 60 günde bir mi; n bağımsız olay sayısı mı; aynı işlem bir kez mi sayılıyor; ortalama yanında medyan var mı? [geçmiş: H006 (n 4-5 kat şişkin), H014]
- K5 giriş fiyatı: Giriş = sinyalden (yayın saatinden) sonraki ilk işlem fiyatı mı (ertesi açılış), sinyal günü kapanışı değil mi? [geçmiş: H005, 60 gün ufuk itirazı]
- K6 veri birimi: Fiyat tek kipte mi (ekran fiyatı ya da düzeltilmiş, karışık değil); birim (lot / TL, peni / sterlin, 100x), bölünme marjı (12.03.2020 öncesi +-%20), bedelsiz denetlendi mi; yeni pazar birim denetiminden geçti mi? [geçmiş: veri 34 satır (H007, H017, H060...)]
- K7 hayatta kalma: Evren bugünün listesi mi? Batanlar / kottan çıkanlar yoksa raporda yazılı ve sonuç 'yukarı yanlı' okunuyor mu? [geçmiş: 8 kez (H008, H057, H142...)]
- K8 örneklem ve dönem: n < 30 'örneklem yetersiz' ve olaylar tek tek listeli mi; iki alt dönem aynı yönde mi; çoklu karşılaştırma BH ile mi; küçük örneklemden 'bulgu' denmiyor mu? [geçmiş: H010, Ç169 n 11, K1 / K2 n < 30]
- K9 ön kayıt: Tanım + eşik sözlüğü + kod sha ön kayıtta; ön kayıt commit zamanı < koşu zamanı; sonuçtan sonra yalnız gösterim değişti, aksi SAPMA; eşik sonuca göre oynanmadı mı? [geçmiş: H079, H097 (ön kayıt geç commit)]
- K10 ayrıştırma: Ham kaynaktan rastgele >= 3 satır elle doğrulandı mı; haber türü (günlük / aylık / dönemsel), kurum etiketi (çok kurumlu haber), kenar kuşağı çöpü, güncelleme damgası, kurum adı hisse satırı dört ayrı denetim maddesi olarak kontrol edildi mi? [geçmiş: 5 kez tek günde (H128-H132, H136)]
- K11 yeniden üretim: Raporlanan >= 2 hücre satır dosyasından bağımsız kodla yeniden üretildi mi; metindeki sıra / tarih / sayı ham kayıtla aynı mı? [geçmiş: H136 (PEKGY 1. / 4.), H137 (blok filtresi)]
- K12 ifade: Fiyat değişimi ile gerçekleşen kâr / zarar ayrı mı; aracı kurum akışı ile kurum pozisyonu ayrı mı; 'anlamlı / ters / iz / emare' sözü yalnız bu liste geçince mi; sayı ile yorum ayrı cümlede mi? [geçmiş: yanlış yorum 16 satır (H133, H135...)]
- K13 süreç: Çakışma kapısı korundu mu; kod değiştiyse 'çalışma zamanını yeniden başlat' yazıldı mı; e-posta / anahtar sızıntı taraması yapıldı mı; kota / ücret / yeni dal Cemal onayıyla mı; yasak defter dosyalarına dokunulmadı mı? [geçmiş: süreç 21 satır (H019, H021, H143...)]
- K14 boyut (gerçek para): Öneri işinde boyut tavanı, zarardaki isme ekleme yasağı, olay bazlı çıkış ve 2x kuralı alımdan önce yazılı mı; taban oranlar (10x ~%1) yazılı mı? [geçmiş: karar-boyut 6 satır (H012, H013)]

## 1. YASAKLAR
- Dokunma: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, COL_v1.py, takip.py, SIKISMA_OBEK.py, SIKISMA_YENIDEN.py, ORTAK_CETVEL.py, mevcut test dosyaları, COL_S5_OBEK*.pine (S5 olduğu gibi kalır).
- git commit / push / stash / checkout yok. E-posta / anahtar yok. Ücretli veri yok.
- Yeni dosyalar YALNIZ: S6_TABAN.py (repo kökü; tek dosya, KURAL_MOTORU düzeni, çakışma kapısı, loglama, tam hata yakalama), test_s6_taban.py, arastirma_cikti/sikisma_s6/ altında: S6_TASARIM.md (tasarım sınaması raporu), s6_tasarim.json, COL_S6_TABAN.pine, COL_S6_TABAN_ascii.pine, PINE_S6_NASIL.md.
- Bu bir TASARIM ve GÖZ ARACI işidir; getiri / iz iddiası YOK (ölçüm sonra, ayrı ön kayıtla). Eşik ızgarası aşağıda önceden yazılı; ızgaranın tamamı raporlanır, seçim gerekçesi yazılır (yalnız tutan hücre gösterilmez).

## 2. ALGORİTMA (S6; her bar t için yalnız t ve öncesi; geçerli bar = H > L ve hacim > 0; Python ve Pine BİREBİR aynı tanım)
Girdiler (varsayılan; ızgara §4): nMin = 8, nMax = 70, bantMax, netMax, kM, dipTol, kirTol = 0,02, atrGun = 250, konumGun = 120, smaGun = 50.
Pencere W(t, n) = son n geçerli bar [t-n+1, t]. Pencere ŞARTLARI:
  (1) BANT: maxHigh(W) / minLow(W) - 1 <= bantMax. (Cemal K2: kısa bölgede %5-8, uzun tabanda %20'ye kadar.)
  (2) SAKİN: |C_t / C_{t-n+1} - 1| <= netMax. (K3.)
  (3) DİP SAVUNULUR: pencerenin ilk yarısının en düşük Low'u = L1, ikinci yarısının en düşük Low'u = L2; L2 >= L1 x (1 - dipTol). (K4: kayan düşüş kanalı elenir.)
  (4) KÜÇÜK MUM: medyan((H-L)/C, W) <= kM x ATR%_250(t) (ATR% = ortalama TR / önceki kapanış, 250 geçerli bar). (K5: gevşek.)
  (5) DARALMA: pencerenin ortalama (H-L)/C değeri, pencereden ÖNCEKİ 60 geçerli barın ortalamasının <= daralmaOran katı (varsayılan 0,9) — "daralma gözle görünür" (K4). Izgarada daralmaOran {0,8; 0,9; kapalı}.
TABAN(t) = şartları sağlayan EN BÜYÜK n (nMax'tan nMin'e doğru ilk tutan). Yoksa taban yok. Taban varsa: başlangıç = t-n+1, TAVAN = maxHigh(W) (tavan mumu = o High'ın barı; K6b), DİP = minLow(W).
Sınıf (bilgi, kuralı değiştirmez): DİP = C_t 120 gün aralığının alt çeyreğinde ve tepeden >= %10 aşağıda; YOL = C_t > SMA50 ve SMA50 yükseliyor; ikisi de değilse ORTA.
AL MUMU (K6): t-1'de taban var (n >= nMin) ve C_t > TAVAN(t-1) -> AL işareti; bölge t'de biter (kutu t'yi içerir). Bilgi olarak al mumunun boyu (H-L)/C ve hacim / 20 gün ortalama hacim yazılır.
TABAN KIRILDI (K8): t-1'de taban var ve C_t < DİP(t-1) x (1 - kirTol) -> KIRILDI işareti; bölge biter.
BÖLGE SÜREKLİLİĞİ: ardışık barlarda taban başlangıcı aynı (ya da ±2 bar) ise aynı bölge; başlangıç değişirse yeni bölge. Çizimde bir bölge = tek kutu [başlangıç, bitiş], tavan ve dip çizgileri, AL / KIRILDI işareti, bölge uzunluğu.
Sonuç olarak bölge uzunluğu nMin..nMax arasında kalır (tek mumluk bölge imkânsız), sınırlar mumlardan gelir (bant + dip + sakin), eğimli pencere elenir, kayan kanal elenir.

## 3. PYTHON REFERANS (S6_TABAN.py)
- s6_taban(d, prm) -> DataFrame (her bar: n, bas, tavan, dip, sinif, al, kirildi, bolge_id, ölçüler). Vektörleştirme serbest ama tanım yukarıdaki gibi; Pine ile birebirlik için 'geçerli bar' dizisi ve aynı sıralama.
- Önek değişmezliği testi (FON_IZI test 63 gibi): d.iloc[:T] ile tam serinin T-1 ve öncesi satırları birebir (al / kirildi dahil). Geleceğe bakma sıfır.
- Komutlar: `python S6_TABAN.py tasarim` (etiket sınaması + ızgara + evren sayımı -> S6_TASARIM.md, s6_tasarim.json), `python S6_TABAN.py liste <SEMBOL> <bas> <son>` (bölge listesi), `python S6_TABAN.py pine` (Pine'ı üretmez; Pine'daki sabitleri ve etiket beklenen çıktısını yazdırır). Veri: V_BIST.pkl (/tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/veri/V_BIST.pkl; yoksa islenmis-veri dalından vpac), SIKISMA_YENIDEN.sy_veri_hazirla(d, SY.SY_ESIK) ile geçerli barlar (düzeltilmiş fiyat; TradingView ADJ açık olduğunda aynı).
- test_s6_taban.py: sentetik (sakin taban -> bulunur; eğimli pencere -> yok; kayan kanal -> yok; tek mum sıçrama -> bölge bitmez / AL; taban kırılımı), önek değişmezliği, nMin / nMax sınırları, çakışma kapısı.

## 4. TASARIM SINAMASI (önceden yazılı; sonuç görülmeden)
Etiketler (CEMAL_COL_KURALLARI.md tablosu; Cemal aralıkları fotoğraftan yaklaşık olanlar 'yaklaşık' işaretli):
  DOĞRU bölge (S6 bölgesi olmalı; örtüşme = kesişim / Cemal aralığı >= 0,5): FENER 2025-10-14..11-07; CCOLA 2025-10-02..15; ENJSA 2021-10-26..11-16 ('tamamı': Kasım kümesi, yaklaşık 2021-10-20..12-05); ENJSA 2025-02 (yaklaşık 2025-01-20..02-18); ENJSA 2025-05-08..06-27; DESA 2021-10-27..12-23 (uzun seçenek 2022-02-02); KNFRT yaklaşık 2022-06-15..09-13 (al mumu 2022-09-14); TUCLK yaklaşık 2025-06-10..08-21 (al mumu 2025-08-22); YKSLN yaklaşık 2026-03-19..05-15 (giriş mumu Mayıs; stop Temmuz); PAPIL küçük taban 2025-11-13..12-10 (al 2025-12-11 kapanışla); PAPIL büyük taban 2025-10-27..2026-03-02 (tavan 6 Kas 20,32; kapanışla kırılım 2 Mar 2026 = zirve; BİLGİ).
  YANLIŞ (S6 bölgesi olmamalı ya da o gün bölge bitmiş olmalı): ENJSA pencere 2021-08-11..09-01 (net +%8,0); ENJSA 2021-09-28..10-18 (net +%9,7); TUCLK 2026-07-24..08-13 (kayan düşüş); ENJSA 2025-07-28..09-12 (bant %23; S5 dışıydı, Cemal'in ilk işaretlediği bölgeydi: S6'da bantMax 0,20 ile de dışarıda kalır; BİLGİ olarak yaz).
  AL MUMU: KNFRT 2022-09-14 (±3 bar), TUCLK 2025-08-22 (±3), PAPIL 2025-12-11 (±1), DESA (taban bitişi: 2021-12-23 ya da 2022-02-02 civarı kırılım var mı yaz).
Izgara (hepsi raporlanır): bantMax {0,12; 0,20}, netMax {0,03; 0,05; 0,08}, kM {0,75; 0,90; 1,00}, dipTol {0,02; 0,05}, daralmaOran {0,8; 0,9; kapalı} = 108 nokta. Puan = doğru bulunan + yanlış elenen + al mumu tutan; eşitlikte en sade (daralma kapalı, dipTol 0,05, kM 0,90, netMax 0,05, bantMax 0,20'ye en yakın) seçilir. Seçimden SONRA 'ters sınama': rastgele 40 hisse-tarih noktasında S6 bölge oranı (çöl nadir olmalı; raporda).
Evren sayımı: V_BIST 2016-26'da hisse-yıl başına S6 bölge sayısı ve AL sayısı, bölge uzunluğu dağılımı, sınıf dağılımı.

## 5. PINE (COL_S6_TABAN.pine, Pine v5; v1.1-1.3 S5 dosyasındaki derlenen kalıpları kullan)
- indicator("COL S6 Taban", overlay=true, max_boxes_count=500, max_lines_count=500, max_labels_count=500).
- Geçerli bar dizileri (H, L, C, O, bar_index, time; en çok 400 tutulur), ATR%250, SMA50, 120 gün aralığı. Her barda n = nMax..nMin döngüsü: pencere şartları (1)-(5) aynı tanım; ilk tutan n taban. Önceki bar tabanı saklanır (var): AL ve KIRILDI kontrolü.
- Çizim: bölge kutusu (başlangıç aynı kaldıkça uzar; AL / KIRILDI ile kapanır; renk sınıfa göre: DİP mavi, YOL turuncu, ORTA gri), tavan çizgisi (kutu içinde yatay, tavan mumunun High'ı), AL üçgeni (yeşil, text "AL"), KIRILDI işareti (kırmızı x). Tablo: n, başlangıç tarihi, tavan, dip, bant %, net %, medyan mum / ATR, daralma oranı, dip savunması, sınıf, durum (açık / AL / KIRILDI).
- Girdiler: §2 varsayılanları = tasarım sınamasının seçtiği değerler; her şart için 'göster / kapat' yok (tek kural seti), yalnız sayısal eşikler ve renkler.
- Kesin sözdizimi disiplini: sarmalı satır yok, tab yok, her değişkenin tipi açık, na kontrolü na(x), box / line / label işlemleri yerel blokta serbest, plotshape / bgcolor / plot global, döngülerde `for n = nMax to nMin by -1` yerine `for k = 0 to nMax - nMin` + `n = nMax - k` kullan (geri sayım tuzağı), string biçimleme str.tostring(x, "#.0"), `break` kullanımı v1.2'de derlendi. Dosya sonuna etiketlerden 6 tanesi için BEKLENEN çıktı yorumu (başlangıç, bitiş, AL günü) yaz; Cemal grafikle karşılaştırır.
- ASCII kopya (eşleme: ç->c Ç->C ğ->g Ğ->G ı->i İ->I ö->o Ö->O ş->s Ş->S ü->u Ü->U â->a σ->s –/—->- ’‘->' “”->" ×->x ≤-><= ≥->>= →->-> ≈->~ ±->+-) ve doğrulama (ASCII dışı 0; yorum / dize dışı kod birebir).
- PINE_S6_NASIL.md: ekleme (Basic plan 2 gösterge), ayarlar, renkler, tablo, bilinen farklar (likidite süzgeci yok; TradingView verisi; kriz kesiği yok).

## 6. TESLİM VE RAPOR (S6_TASARIM.md; zorunlu başlıklar)
ÖZET (bulgu dili) · ALGORİTMA (son hâli, eşikler) · ETİKET TABLOSU (her etiket: S6 başlangıç-bitiş, örtüşme, AL günü, sonuç ✓/✗) · IZGARA (108 nokta özet + seçim gerekçesi) · TERS SINAMA ve EVREN SAYIMI · ÖNEK DEĞİŞMEZLİĞİ · PINE (dosya, riskli satırlar, beklenen çıktı) · KONTROL LİSTESİ (K1-K14) · HATA (bulduğun her hata) · ÖNERİLEN DEFTER METNİ (IK_GOREV satırı; ana model işler) · DOKUNULAN DOSYALAR.
Son mesajda: etiket tablosu, seçilen eşikler, evren sayımı, test sonucu, git status --short.
