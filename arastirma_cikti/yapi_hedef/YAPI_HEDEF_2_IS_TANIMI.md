# İŞ TANIMI: YAPI_HEDEF 2. tur — Cemal'in değerlendirmesinden kurulan Y6 / Y7 / Y8 (17 Kas 2026 akşam)

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
YAPI_HEDEF_IS_TANIMI.md §1 aynen (defter dosyalarına dokunma; `git add -A` yok; push yok; ön kayıt ayrı commit, ölçüm ikinci commit; eşik sonuçtan sonra oynatılmaz, zorunlu sapma SAPMA-n diye ön kayda, koşmadan önce). YAPI_HEDEF.py'nin ÇALIŞAN kısmına dokunma; yeni denemeler YH_ESIK['denemeler'] ve sinyal fonksiyonlarına EKLENİR (Y1-Y5 sonuçları değişmemeli: regresyon testi = Y1 ABD 2023 n 2040 KAT5 0,9752 aynen). Kod sha, eşik sha ön kayıtta. Raporda zorunlu başlıklar: SONUÇ, KONTROL LİSTESİ, HATA, ÖNERİLEN KAYIT, YENİDEN ÜRETİM KOMUTU.

## 2. KAYNAK
arastirma_cikti/yapi_hedef/CEMAL_DEGERLENDIRME_2026-11-17.md (E1-E11 ve §4), RAPOR.md, YAPI_HEDEF.py. Cemal'in notları sonuç görülerek yazıldı: beklenti yazılmaz, etiket önceden yazılı kuralla (YAPI_HEDEF karar kuralı aynen).

## 3. DENEMELER (eşikler sabit; aşağıdaki sayılar ön kayıt değerleridir)
Y6 = Y1 (S6 AL) + dört şart:
 (a) HAT NET (E2): bölge içinde Low <= hat x 1,015 olan bar sayısı >= 3 VE bu dokunuşların ilkinin Low'u <= sonuncusunun Low'u x 1,0 değil, tam ifade: son dokunuş Low'u >= ilk dokunuş Low'u x 0,99 (eğim aşağı değil);
 (b) GERÇEK KIRILIM (E3): C_t > tavan x 1,01 VE (H_t - L_t) >= bölge içi (H - L) medyanı;
 (c) STOP UZAKLIĞI (E5a): giriş (t+1 açılış) / hat - 1 <= 0,10 (giriş bilinmeden t'de: C_t / hat - 1 <= 0,10 ile ön ele; ölçümde gerçek giriş ile yeniden denetlenir, aşanlar 'stop uzak' sayımına düşer);
 (d) BÜYÜK DESEN ALÇALAN DEĞİL (E1): son 250 barda ardışık 25 barlık pencerelerin Low minimumlarına (10 nokta) doğru uyumu; eğim (son / ilk - 1) >= -0,05 (yoksa sinyal yok). 250 bar yoksa (d) UYGULANMAZ ve ek sütun 'buyuk_desen=NA'.
Y7 = Y3 + kazan şartları (E4) + E5a:
 (a) İKİ KENAR: pencerenin ilk üçte birinin dibi >= orta üçte birin dibi x 1,05 VE son üçte birinin dibi >= orta dip x 1,05;
 (b) DİPTE KÜÇÜK MUM: orta üçte birde (H - L) medyanı <= 0,9 x ATR250 (ATR250 pencere öncesi 250 bar; yoksa 120);
 (c) DİP SAVUNMASI: pencere dibi x 1,015 altında Low'u olan bar sayısı >= 3;
 (d) E5a stop uzaklığı <= 0,10.
Y8 = Y6 + CEMAL HAFIZASI (E7): son 250 barda [t-250, t-1] KIRILDI ile biten S6 bölgesi (kapanış < dip x 0,98) YOKSA olay; varsa düşer. Ek bilgi satırı Y8b: tersine, patlamış yapısı OLANLAR (aleyhte şart; karşılaştırma için).
Bilgi varyantı (karar satırı değil): Y6 ve Y7 için stop0 = max(hat x 0,98, giriş x 0,95) (E5b) ile hedef / stop payları ayrı sütunda.
Her deneme: aynı cetvel (15 bar, +%5 / +%10 stop'tan önce, takip stopu, eş + plasebo, hücreler, karar kuralı, güç tablosu). Olay sayımı tablosunda her şartın kaç olay düşürdüğü yazılır (Y1 -> Y6 huni).

## 4. ÇIKTI
Aynı klasör: ON_KAYIT_2.md (kontrol tablosu + kapı), sonuc.json'a 'deneme' altında Y6 / Y7 / Y8 (Y1-Y5 korunur), RAPOR.md'ye bölüm (ya da RAPOR_2.md), olay_Y6..Y8.csv.gz. test_yapi_hedef.py'ye yeni şartların birim testleri (hat dokunuş sayımı, kırılım payı, iki kenar, büyük desen eğimi, hafıza; prefix değişmezliği). Komut: `OC_VERI=/tmp/veri python YAPI_HEDEF.py kos --deneme Y6,Y7,Y8`.
