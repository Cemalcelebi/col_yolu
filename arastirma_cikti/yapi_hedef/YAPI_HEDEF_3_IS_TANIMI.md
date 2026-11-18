# İŞ TANIMI: YAPI_HEDEF 3. tur — Cemal'in çöl tanımı: DÜŞÜŞ SONRASI DİPTE (Y9), şemsiye karşıtı (Y9c) (18 Kas 2026)

## 0. ÖN UÇUŞ KONTROL LİSTESİ
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


## 1. YASAKLAR ve DÜZEN
YAPI_HEDEF_IS_TANIMI.md §1 ve YAPI_HEDEF_2_IS_TANIMI.md §1 aynen (defter dosyalarına dokunma; `git add -A` yok; push yok; ön kayıt ayrı commit; eşik sonuçtan sonra oynatılmaz; Y1-Y8 regresyonu birebir). Raporda zorunlu başlıklar aynı.

## 2. GEREKÇE ve DÜRÜSTLÜK NOTU (ön kayda aynen)
Cemal (18 Kas, hakem PDF'ine bakarken): 'neredeyse çoğunda şemsiye şekli oluşmuş; bunlar yukarı kırılması beklenmemeli'. Ana model ön kayıtsız bir BAKIŞ yaptı (IK_HATA'ya yazıldı): ABD + AVR 2023 / 2024-26 Y1 olaylarında (n 8.649) F15 (120 gün konumu) >= 0,75 olanlar %58, <= 0,25 olanlar %7; dipte olanların +%5 payı %51,9 vs eş %44,2 (KAT5 1,17, n 586), tepedekilerin %34,3 vs %37,6 (0,91, n 5.011). Eşikler ÖNCEDEN VAR OLAN tanımlardan (FITIL_V2 bağlam DİP <= 0,25; dönüm >= %20 düşüş) alındı, ama bakış bu hücrelerin sonucunu gördü. Bu yüzden: ABD / AVR 2023 ve 2024-26 hücreleri bu koşuda 'bakılmış' sayılır ve raporda öyle işaretlenir; DIŞ SINAMA = 2016-22 (ABD, AVR) ve BIST (üç dönem) hücreleri (ana model bunlara BAKMADI). Karar etiketi bu kez şöyle: karar hücreleri aynı (ABD / AVR 2023, 2024-26) ama etiket en fazla EMARE; dış sınama hücrelerinde (2016-22 ABD / AVR) de aynı yön + kural tutarsa 'EMARE (dış sınama tuttu)'; Mart 2027 ileri test asıl karar.

## 3. DENEMELER (eşikler sabit)
Y9 DÜŞÜŞ SONRASI DİPTE: Y1 (S6 AL) olayı VE F15 <= 0,25 (son 120 barın aralığında kapanış konumu; t-1'e kadar) VE F17 <= -0,20 (bölge başı kapanışı / bölge öncesi 60 gün zirvesi - 1). Özellikler ozellik_Y1.csv.gz'den (t'ye kadar; aşama A prefix testi).
Y9b = Y9 + hat net (F1 >= 3) + gerçek kırılım (F11 >= 0,01) (Cemal'in E2 / E3'ü dip bağlamında).
Y9c TEPEDE (şemsiye karşıtı): Y1 olayı VE F15 >= 0,75. Yön + ile ölçülür (kodun yukarı kırılımı); beklenti yazılmaz; sonuç ters çıkarsa 'TERS EMARE' diye raporlanır (iki yönlü etiket: KAT5 üst uç < 1 ve iki yarı aynı yön).
Y9d ORTA (0,25 < F15 < 0,75) bilgi.
Aynı cetvel (15 bar, +%5 / +%10 stop'tan önce, takip stopu, eş + plasebo, güç tablosu); olasılık tablosu; huni (Y1 -> Y9 -> Y9b). Ek bilgi sütunu: eşlerin F15 dağılımı (eş kovası konumla eşlenmiyor; kontrol: aynı gün aynı kova VE F15 aynı çeyrekte olan eşler ile KAT5 — 'konum eşli KAT5' — bu satır zorunlu, çünkü dipte olmak tek başına momentum kovasıyla karışabilir).

## 4. ÇIKTI
YAPI_HEDEF.py'ye Y9 / Y9b / Y9c / Y9d (ozellik dosyasından okuyarak; dosya yoksa dur), ON_KAYIT_3.md (kontrol tablosu + kapı + §2 notu aynen), sonuc.json 'deneme' altına, RAPOR_3.md, olay_Y9*.csv.gz, testler (özellik birleştirme sembol + tarih eşleşmesi; konum eşli KAT hesabı; prefix). Komut: `OC_VERI=/tmp/veri python YAPI_HEDEF.py kos --deneme Y9,Y9b,Y9c,Y9d`.
