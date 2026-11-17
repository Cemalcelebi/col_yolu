# İŞ TANIMI: YAPI_HEDEF — yapı kurallarının yeni test standardıyla ilk ölçümü (17 Kas 2026, ana model -> alt ajan)

## 0. ÖN UÇUŞ KONTROL LİSTESİ (kod yazmadan oku; ön kayıtta doldur)
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
- IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md dosyalarına DOKUNMA; kayıt önerini raporuna yaz.
- `git add -A` YOK; adlı dosyalar. Commit at, push ETME. ÖN KAYIT (ON_KAYIT.md + eşik sha + kod sha) ölçüm koşmadan ÖNCE ayrı commit; ölçüm ikinci commit. Eşik sonuç görüldükten sonra oynatılmaz; zorunlu sapma varsa SAPMA-n diye ön kayda yaz, koşmadan önce.
- Tek dosya, üretim kalitesi, çakışma kapısı (yüklenirken bellekteki adı ezerse dur), tam hata yakalama, loglama. test_yapi_hedef.py yaz; bütün kontroller geçsin.
- Token / anahtar / e-posta koda ve rapora girmez. Veri dosyaları repoya girmez (olay csv.gz'ler küçükse arastirma_cikti/yapi_hedef/ altında kalabilir; > 5 MB ise scratchpad).
- Raporunda zorunlu başlıklar: SONUÇ, KONTROL LİSTESİ (14 madde EVET / UYGULANMAZ + kanıt), HATA (bulduğun her hata ayrı satır), ÖNERİLEN KAYIT, YENİDEN ÜRETİM KOMUTU (ana model en az 2 hücreyi satır dosyasından yeniden üretecek).

## 2. CEMAL'İN YENİ TEST STANDARDI (CLAUDE.md 'YENİ TEST STANDARDI, YAPI KURALLARI İÇİN' ve 'UFUK 15 MUM', 'SON DERS'; arastirma_cikti/fitil_v2/KOR2_DERS_CEMAL.md D1-D14 oku)
- 60 gün testi yapı kuralları için KAPANDI. Kod oluşumu görür; giriş = kırılım mumu (dip tavanı / taban kırılınca hedef başlar). Ölçümde giriş = kırılım gününden sonraki ilk geçerli barın AÇILIŞI.
- HEDEF: +%5 ve +%10 (giriş fiyatına göre, kapanışla ya da High ile ayrı sütun; karar sütunu KAPANIŞ), stop'tan ÖNCE, 15 geçerli bar içinde. 'Önce hangisi' mantığı FITIL_V2.fv_kirilim / ORTAK_CETVEL._oc_once ile aynı tür.
- STOP (geçici kural, Cemal 'son kural değil'): stop0 = yapı dibi x 0,98 (hat); +%5 kapanışla gelince stop = giriş x 1,02; +%10 gelince stop = giriş x 1,07; ayrıca takip: stop = max(stop, giriş sonrası en yüksek kapanış x 0,93). Çıkış = stop (ertesi açılış) ya da yeni TERS OLUŞUM (düz tavan SAT mumu: son 10-30 barda bant <= %6 tavan bölgesi sonra kapanış < bölge dibi x 0,98) ya da 60 bar zaman tavanı (bilgi). Takip stoplu getiri ve çıkışa kadar bar sayısı bilgi sütunlarıdır.
- KONTROL GRUBU (K1, zorunlu): eşli hedef payı = aynı giriş günü, aynı momentum beşliği x likidite üçlüsü kovasındaki (ORTAK_CETVEL oc_panel kovaları) öteki hisselere AYNI mekanik kural (giriş t+1 açılış, stop0 = giriş x (1 - d) ile d = olayın hat uzaklığı, aynı hedefler, 15 bar). Olay hedef payı / eş hedef payı = KAT; ay kümeli bootstrap %95 (ORTAK_CETVEL oc_kat gibi). İkinci kontrol: aynı hisse, rastgele gün (sayı = olay sayısı, aynı dönem), aynı kural (plasebo).
- HÜCRELER: karar ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26; bilgi BIST 2023, BIST 2024-26, 2016-22 (varsa). Fon krizi kesiği 31.08.2026 (15 barlık pencere bu tarihi aşan olay ölçülmez). Hayatta kalma notu rapora.
- KARAR KURALI (önceden yazılı, değişmez): bir hücre TUTAR = n >= 30 VE +%5 KAT'ın bootstrap alt ucu > 1 VE önce-stop payı eşlerinkinden küçük VE plasebo KAT alt ucu > 1. Etiket: dört karar hücresi tutarsa İZ; iki-üç hücre ya da tek pazar tutarsa EMARE; güç yetersizken (hücre n < 1.000 ve güç simülasyonu < %80) tutmayana ÖLÇÜLEMEDİ; güç yeterli ve tutmayana DESTEKLENMEDİ. 'İz değil' sözü yazılmaz.
- OLASILIK TABLOSU çıktısı (Cemal'in istediği biçim): her satır x hücre için P(+%5 önce), P(+%10 önce), P(stop önce) olay / eş / taban, KAT [%95].

## 3. DENEMELER (hepsi ön kayıtta; sonuç görülmeden sabit; 'birkaç deneme' = Cemal)
Y1 S6 TABAN AL: S6_TABAN.s6_taban (prm varsayılan v1.1) 'al' günleri = taban kırılım mumu; hat = bölge dibi. Veri: SY.sy_veri_hazirla girdisi (S6_TABAN.py'deki akışı oku).
Y2 S+ v2 TAM_DIP: arastirma_cikti/fitil_v2/olay_TAM_DIP.csv.gz olayları (sembol, pazar, tarih, giris); hat = FITIL_V2 HAT (yeniden hesaplanır: 10 bar dibi). Giriş olay günü + 1 açılış (dosyadaki 'giris').
Y3 KAZAN + DÖNÜŞ (D3 + D4, yeni): pencere n = 20..60 bar Low serisine 2. derece uyum a > 0 VE sağ kenar dibi (son 5 bar) > orta üçte birin dibi x 1,03 VE son kapanış > pencere orta noktası (dip + (tavan - dip) / 2) VE kırılım = kapanış > pencere tavanı (önceki n barın max High, t hariç); hat = pencere dibi. Bağlam: 120 gün zirvesinden >= %15 aşağı (tepede değil).
Y4 Y1 + KAĞIT HAFIZASI (D8): son 250 barda önceki S6 bölgelerinden AL sonrası 15 barda +%5 görenler eksi KIRILDI olanlar >= 0 (yalnız geçmiş; t'ye kadar).
Y5 DÜZ TAVAN SAT (D2 / D9, yön AŞAĞI): S6 bant / net şartlarının aynası (yüksekler düz, bant <= %12, net <= %3, n 8..70) + 120 gün konumu >= 0,75 + önceki 60 günde >= %20 yükseliş; SAT = kapanış < bölge dibi x 0,98; hedef -%5 / -%10, stop bölge tavanı x 1,02. Aynı cetvel, yön eksi.
Her deneme için ayrı satır; Y1-Y4 yön +, Y5 yön -. Eşik tablosu YH_ESIK tek sözlükte, sha ön kayıtta.

## 4. VERİ
- /tmp/veri boş. Açma: `git worktree add /tmp/iv origin/islenmis-veri` (varsa atla) ve `python FON_IZI.py vpac /tmp/iv/veri /tmp/veri` (V_BIST.pkl, V_ABD.pkl, V_AVR.pkl). ORTAK_CETVEL.oc_veri(pazar) ile yükle (OC_VERI=/tmp/veri). Evren dışı ETF listesi oc_veri içinde uygulanıyor; doğrula.
- Geçerli bar: kilitli / hacimsiz bar sinyal ve giriş günü sayılmaz (K3; ORTAK_CETVEL'deki geçerli bar tanımını kullan). Bölünme şüphesi oc_bolunme_supheli.
- Veri birimi (K6): AVR yerel para; hedef yüzde olduğu için kur gerekmez, likidite kovasında EUR (Kur sütunu) ORTAK_CETVEL'de hazır.

## 5. ÇIKTI
- Modül: YAPI_HEDEF.py (komutlar: `onkayit`, `kos [--deneme Y1,...]`, `rapor`, `guc`); test_yapi_hedef.py.
- Klasör: arastirma_cikti/yapi_hedef/: ON_KAYIT.md (kontrol tablosu + IZ_KARNE.ik_kontrol_kapisi çağrısı koşudan önce), sonuc.json, RAPOR.md (özet, tanım, olay sayımı, hücre tablosu, OLASILIK TABLOSU, kırılım / stop, karar, veri sınırları, kontrol listesi), olay_Y*.csv.gz satır dosyaları.
- Geleceğe bakma denetimi (K2): rastgele 5 olay için prefix (t'ye kadar kesilmiş veri) ile aynı sinyalin çıktığını testte göster; hat ve hedef yalnız t sonrası fiyatla.
- Yeniden üretim (K11): raporda en az iki hücrenin sayısını satır dosyasından 5 satırlık komutla üretme yolu.
- Süre: büyük koşu ise paralel (ORTAK_CETVEL islem) ve ilerleme logu; 2 saati aşacaksa önce ABD + AVR 2024-26 hücreleriyle koş, raporla, kalanını ikinci koşu.
