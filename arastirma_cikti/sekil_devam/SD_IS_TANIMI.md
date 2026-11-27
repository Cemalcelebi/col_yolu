# SEKIL_DEVAM İŞ TANIMI — benzer şekiller benzer devam getiriyor mu; veri kendi desenlerini bulsun (27 Kasım 2026)

Yazan: ana model. Cemal (27 Kas; ana modelin 'hattı kapat' önerisine; yazdığı gibi): "Sen iste bir İki şeye bakıyorsun çıkmadı üstüne toprak örtelim huyun kötü hiç meraklı ve araştırmacı yönün yok bence sen hâlâ hata yapıyorsun görmediğin bir şeyler vardır neden bu mumların yapıları farklı olsun desen oluştursun ve benzeri şekillerde aynı alış satışları barındırma olasılığı çok fazla". Ana modelin okuması: (1) erken kapatıyorsun; (2) hâlâ görmediğin hatalar var; (3) ÖNERME: mum yapıları sebepsiz farklılaşmaz; benzer şekiller aynı alış-satışı barındırır.

Ana modelin kendi ölçümlerindeki KÖR NOKTALAR (itiraz haklı; bu iş bunları kapatmak için):
- K1 GİRİŞ YERİ: bugüne kadarki bütün ölçümler bölge BİTTİKTEN sonra girdi; Cemal'in kalıbı tırmanışı da içeriyor (kodun bölgeleri dipten ~%20 yükseldikten sonra bitiyor): kalıbın parası bölgenin İÇİNDE olabilir; erken evreden (ilk yarı) sonrası hiç ölçülmedi.
- K2 CETVEL: mumlar yüzdeyle ölçüldü; göz grafikteki boyu ve banda göre konumu görüyor (Ç253). Banda göre konum dizisi (v3) soldaki dibi seçen tek sürümdü ve hiç taranmadı.
- K3 ÖNERMENİN KENDİSİ hiç sınanmadı: 'şekil benzerse devamı da benzer mi' sorusu, tek bir kalıp için değil BÜTÜN şekiller için sorulabilir.
- K4 HACİM: 'alış-satış' ölçülmeden yalnız fiyat şekline bakıldı (hacim defterde kapalı konuydu; Cemal'in bu cümlesi bu iş için açma sayıldı, ayrı kol olarak).
- K5 SÖZ - GÖZ: sözlü şartlardan kurulan dedektörler Cemal'in gözünü hiç tutmadı (en çok %50); bu yüzden bugüne kadar sınanan şey Cemal'in kalıbı değil, ana modelin vekilleriydi. Bu işte şart yazılmaz; şekli veri tanımlar.
- (Kapsam dışı, kayıt için: Cemal'in ilk örneği 4 saatlik grafiktendi; günlük / haftalık hisse mumu aynı davranışı taşımayabilir; 4 saatlik veri yerelde yok.)
'KNN' ve '90+ şekil ölçüsü' kapalı konulardır; bu iş Cemal'in açık isteğiyle ve yalnız burada tanımlanan iki tanımlayıcıyla yapılır.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import). `git add -A` / `commit -a` yasak.
- KASA AÇILMAZ: veri <= 2022-12-31 (assert). Geleceğe bakma yok: tanımlayıcı yalnız pencere barlarından ve öncesinden; komşular YALNIZ geçmişten (sorgu penceresinden en az 20 bar önce bitmiş pencereler) ve başka hisselerden aranır; giriş = pencereden sonraki ilk geçerli bar açılışı. Geçerli bar / evren / veri yükleme YUKSELIS_ONCESI ve MUM_IZI_HAVUZ ile aynı; kilitli / fiyat adımına yapışmış pencereler atılır (MUM_IZI_UC kuralı).
- Yeni tek dosya SEKIL_DEVAM.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_sekil_devam.py; çıktılar arastirma_cikti/sekil_devam/.
- Sıra: kod + sentetik test (zorunlu: içine bilinen bir 'şekil -> devam' ilişkisi gömülmüş sentetik veride yöntem ilişkiyi BULMALI; ilişkisiz rastgele yürüyüşte BULMAMALI; ikisi de testte) -> GETİRİSİZ SAYIM -> ön kayıt SD_ON_KAYIT.md (kod sha, parametre sözlüğü sha, sayımlar, `python IZ_KARNE.py kontrol` tablosu) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> KEŞİF (ABD 2016-19) -> küme merkezleri ve seçilen kümeler SD_KESIM.md'ye commit + push -> DOĞRULAMA (ABD 2020-22; AVR) -> rapor. Özellik dosyası ile sonuç (getiri) dosyası AYRI tutulur; ön kayıt commit'i sonuç dosyası üretilmeden ÖNCE atılır.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Pencere, tanımlayıcı, devam (sabit)
- Pencere uzunlukları: L20 (20 bar; Cemal'in bölge uzunluğu) ve L10 (10 bar; ERKEN EVRE: kör nokta K1). Günlük; her hissede her 5 barda bir pencere sonu. Dönem: ABD 2016-19 (KEŞİF / komşu havuzu), ABD 2020-22 (DOĞRULAMA; komşular 2016'dan sorgu gününe kadarki geçmişten), AVR aynı kalıpla yön doğrulaması.
- TANIMLAYICI A (banda göre konum; Cemal'in 'ilk nerede sonra nerede; açılış kapanış; fitil' sözü): her bar için O, H, L, C'nin bant koordinatı b = (fiyat - SMA20) / (2 sigma20), [-3, +3] kırpılır: L x 4 sayı. Ek 4 sayı: pencere içi bant genişliği değişimi, pencereden önceki 60 barın en yükseğinden pencere dibine düşüş (ATR birimi), pencere başı ve sonu KONUM120.
- TANIMLAYICI B (A + alış-satış): A + her bar için göreli hacim = log(hacim / önceki 60 barın medyan hacmi), [-3, +3] kırpılır: L sayı daha.
- TANIMLAYICI 0 (basit taban): yalnız 3 sayı: son barın bant koordinatı, F15 (15 barlık geçmiş getiri / ATRP), KONUM120.
- DEVAM (oynaklıktan arındırılmış): Z15 = (15. bar kapanışı / giriş - 1) / (ATRP20 x karekök 15); yol: 15 barın kümülatif getirisi aynı ölçekle; HEDEF = +2 ATRP'ye, önce -1 ATRP görmeden ulaşmak (kötümser: aynı barda ikisi varsa stop); AYNA = -2 ATRP'ye, önce +1 görmeden.
- Benzerlik: standartlaştırılmış tanımlayıcıda Öklid uzaklığı; K = 50 en yakın komşu.

## 2. SINAMA 1 — ÖNERME: benzer şekil, benzer devam mı
- Her doğrulama penceresi için TAHMİN = komşularının ortalama Z15'i. IC = TAHMİN ile gerçekleşen Z15 arasındaki sıra ilişkisi (her ay ayrı hesaplanır, ayların ortalaması; ay kümeli bootstrap %95; 10.000; tohum 271).
- Aynı hesap TANIMLAYICI 0 ile (basit taban) ve rastgele komşularla (şans tabanı).
- TAHMİN'in üst %10 ve alt %10 pencereleri: gerçekleşen Z15 ortalaması, yüzde getirisi (R15), HEDEF ve AYNA payları; ÜST - ALT farkı; rastgele güne göre TOPLAM FARK (YUKSELIS_ONCESI tanımı).
- YOL BENZERLİĞİ: bir pencerenin devam yolu ile komşularının ortalama devam yolu arasındaki korelasyonun ortalaması; rastgele komşularla aynı sayı.
- HÜKÜM (önceden): 'ŞEKİL BİLGİ TAŞIYOR' <=> ABD 2020-22'de IC(A) > 0 ve alt ucu > 0 VE IC(A) - IC(0) > 0 ve alt ucu > 0 VE ÜST - ALT Z15 farkı > 0 ve alt ucu > 0 VE AVR'de IC(A) işareti artı. 'BASİT KONUMDAN FAZLASI YOK' <=> IC(A) > 0 ama IC(A) - IC(0) aralığı sıfırı içeriyor. 'ŞEKİL BİLGİ TAŞIMIYOR' <=> IC(A) aralığı sıfırı içeriyor ya da eksi (n büyük: güç yeterli). Aynısı L10 için ayrı (ERKEN EVRE) ve TANIMLAYICI B için ayrı ('HACİM EKLİYOR' <=> IC(B) - IC(A) > 0 ve alt ucu > 0).

## 3. SINAMA 2 — VERİ KENDİ DESENLERİNİ BULSUN
- KEŞİF'te tanımlayıcı A (L20) ile k-ortalama, 60 küme (tohum 272; ayrıca L10 için 60). Her kümenin KEŞİF ortalama Z15'i; EN İYİ 5 ve EN KÖTÜ 5 küme seçilir, merkezleri ve seçim SD_KESIM.md'ye yazılır.
- DOĞRULAMA: 2020-22 pencereleri en yakın merkeze atanır; seçilen 10 küme için n, Z15, R15, HEDEF / AYNA payı, TOPLAM FARK [ay kümeli %95]; farklı ay, en kalabalık 3 ay payı. 'DESEN TUTTU' <=> keşifte seçilen EN İYİ küme doğrulamada Z15 > 0 ve alt ucu > 0 VE TOPLAM FARK > 0 ve alt ucu > 0 VE AVR'de işaret artı (EN KÖTÜ için tersi). 10 küme için BH q 0,10.
- CEMAL'İN BÖLGELERİ NEREDE: Cemal'in BENZİYOR dediği bölgeler (mum_izi23_olay.csv; günlük olanlar) hangi kümelere düşüyor (sayım; küme sırasıyla birlikte); soldaki dip örneği (APPN 07.05-07.06.2021) ve sağdaki (16.08-07.09.2021) hangi kümede.
- GÖRSEL (Cemal için): SD_DESENLER.pdf: seçilen 10 kümenin her biri bir sayfa: küme merkezinin mum grafiği gibi çizimi (bant koordinatında; Bollinger çizgileriyle) + o kümeden rastgele 6 gerçek örnek (yüzde eksenli, öncesiyle; hisse adı yazılabilir; sonrası YOK) + tek satır: keşif ve doğrulama sonucu ('tuttu / tutmadı'); kapakta SINAMA 1'in tek cümlelik sonucu. Telefon ekranı; düz dil.

## 4. Çıktılar
SEKIL_DEVAM.py, test_sekil_devam.py; arastirma_cikti/sekil_devam/: SD_ON_KAYIT.md, SD_KESIM.md, SD_RAPOR.md, sd_sonuc.json, sd_ozet.csv, SD_DESENLER.pdf. Büyük dosyalar repoya girmez (/root/.kasa/ham/sekil_devam; raporda yol + sha256).
