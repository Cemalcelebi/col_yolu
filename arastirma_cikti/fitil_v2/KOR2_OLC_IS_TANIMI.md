# İŞ TANIMI: FITIL_V2 kör set 2 kısmi yanıt değerlendirmesi (17 Kas 2026, ana model -> alt ajan)

## 0. ÖN UÇUŞ KONTROL LİSTESİ (okumadan kod yazma)
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
- IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, KURAL_DEFTERI_TASLAK.md, CEMAL_COL_KURALLARI.md dosyalarına DOKUNMA. Önerdiğin kayıt metnini raporuna yaz.
- `git add -A` YOK; yalnız adlı dosyalar. Commit at, push ETME.
- Eşik / anahtar / tohum değiştirme. kor2_anahtar.json yalnız fv_olc'nin yazdığı 'olc' alanıyla değişir.
- arastirma_cikti/fitil_v2/kor2_cevap_cemal.json ana modelin yazdığı Cemal yanıt dosyasıdır; içeriğini DEĞİŞTİRME, yalnız oku.

## 2. DURUM
- Cemal kör set 2 PDF'ini (40 sayfa) el yazısıyla işaretledi. Ana model yanıtları arastirma_cikti/fitil_v2/kor2_cevap_cemal.json dosyasına döktü: 'yanit' -> no -> {etiket E/H/B/'-', tur açık/çıkarım/yanıtsız, cemal_notu, ders}. 26 sayfa yanıtlı (E 2, H 13, B 11), 14 sayfa yanıtsız ('-': 4, 6, 20 ve 30-40).
- FITIL_V2.fv_cevap_ayristir 40 yanıtın hepsini zorunlu kılıyor; kısmi yanıt kabul etmiyor. Bu yüzden `olc` koşamıyor.

## 3. İŞ
(a) FITIL_V2.py: fv_cevap_ayristir'a yanıtsız sayfa kabulü ekle: '-' etiketi (örn. '4:-') ve `eksik_izin=True` ile eksik numaralar yanıtsız sayılır. fv_olc'ye `--cevap-dosya <json>` seçeneği ekle: kor2_cevap_cemal.json'u okur, etiketleri alır. Yanıtsız sayfalar paylardan ÇIKARILIR (n = yanıtlı), çıktıya 'yanitsiz' listesi ve sayısı yazılır. Mevcut davranış (tam yanıt, metin) bozulmasın; çakışma kapısı korunsun. Kod üretim kalitesinde, baştan yazma, yalnız bu iki noktaya dokun.
(b) fv_olc çıktısına ek: (i) 'tur' kırılımı: açık / çıkarım ayrı E-H-B payları (TAM ve DEĞİL); (ii) Cemal etiketi x anahtar grubu çapraz tablosu (E/H/B/- x TAM/DEGIL); (iii) Cemal H dediği TAM sayfalarının ve B dediklerinin r20 / r60 medyanı ve KIRILIM / STOP payı (sonuc_bilgi zaten E/H/B için var; yanıtsızları dışarıda tut). Karar kuralı (fv_kor_karar) DEĞİŞMEZ; yalnız yanıtlı n üzerinden hesaplanır ve çıktıya 'n_yanitli' eklenir.
(c) test_fitil_v2.py'ye en az 4 kontrol: '-' ayrıştırma, eksik_izin, dosyadan okuma, yanıtsız dışlama (paylar). Bütün test dosyası geçsin (`python test_fitil_v2.py`).
(d) Koş: `python FITIL_V2.py olc --cevap-dosya arastirma_cikti/fitil_v2/kor2_cevap_cemal.json`; sonra `python FITIL_V2.py rapor` (RAPOR.md KÖR SET 2 bölümü dolsun; rapor fonksiyonu kor2'de n_yanitli ve yanıtsız sayısını da yazsın).
(e) Commit (adlı dosyalar: FITIL_V2.py, test_fitil_v2.py, arastirma_cikti/fitil_v2/kor2_anahtar.json, sonuc.json, RAPOR.md). Push yok.

## 4. RAPOR (zorunlu başlıklar)
- SONUÇ: karar etiketi, TAM / DEĞİL E-H-B sayıları (yanıtlı n), açık / çıkarım kırılımı, çapraz tablo, H/B sayfalarının r20 / r60 medyanı ve stop payı. Sayılar çıktı dosyasından (sonuc.json 'kor2').
- KONTROL LİSTESİ: 14 madde EVET / UYGULANMAZ + kanıt (bu iş ölçüm değil değerlendirme; K9 ön kayıt: kör set ön kaydı ON_KAYIT.md, karar kuralı değişmedi).
- HATA: bulduğun her hata ayrı satır (yoksa 'yok').
- ÖNERİLEN KAYIT: IZ_KARNE görev satırı için 2-3 cümle.
