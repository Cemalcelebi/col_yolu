# İŞ TANIMI: GOZ_ETIKET — Cemal'in gözüyle etiketle, ölç, metrik çıkar (17 Kas 2026 akşam)

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


## 1. AMAÇ (Cemal, 17 Kas akşam)
'Benim nasıl karar aldığımı biliyorsun: mum dizilimi, taban oluşumu, taban savunması, mumların küçüklüğü, alt fitil kısa, açılış ile dip neredeyse yakın. Kodun bulduğu bütün bölgeleri sen olur / olmaz + neden diye etiketle, koda aktar, eğit, metrik çıkar.' Üç aşama, üç ayrı alt ajan (etiketleyen ile ölçen ayrı; etiketleyen SONRASINI GÖRMEZ).

## 2. YASAKLAR ve DÜZEN
YAPI_HEDEF_IS_TANIMI.md §1 aynen (defter dosyalarına dokunma; `git add -A` yok; push yok; ön kayıt ayrı commit; eşik sonuçtan sonra oynatılmaz). Görseller ve büyük dosyalar repoya girmez (scratchpad: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/goz_etiket/). Yeni modül GOZ_ETIKET.py (tek dosya, çakışma kapısı, test_goz_etiket.py). Çıktı klasörü arastirma_cikti/goz_etiket/.

## 3. AŞAMA A — ÖRNEKLEM, GÖRSEL, SAYISAL ÖZELLİK, ÖN KAYIT (alt ajan A)
- Kaynak olaylar: arastirma_cikti/yapi_hedef/olay_Y1.csv.gz (S6 TABAN AL, 26.663 olay; sütunlar: pazar, sembol, tarih (sinyal t), giris, hat, tavan, n, h5, h10, st5, es_h5 ...). Veri /tmp/veri (OC_VERI).
- ÖRNEKLEM: tohum 11; 2023 ve 2024-26 dönemlerinden, pazar x dönem katmanlı: ABD 2023 60, ABD 2024-26 80, AVR 2023 40, AVR 2024-26 60, BIST 2023 20, BIST 2024-26 40 = 300 olay; aynı sembolden en çok 2. Seçim SONUÇ SÜTUNLARINA BAKMADAN (yalnız kimlik sütunları yüklenir; kod bunu garanti eder ve testte gösterilir).
- GÖRSEL: her olay için PNG (1200x800): sinyal günü t dahil son 120 bar (t'den SONRASI YOK), mum + hacim, S6 bölgesi (mavi alan), tavan ve hat çizgisi, fiyat ekseni gerçek fiyat, başlıkta yalnız 'No k' (hisse adı, tarih, pazar YOK; kör). Anahtar: arastirma_cikti/goz_etiket/anahtar.json (no -> sembol, pazar, tarih; GİZLİ: etiketleyen açmaz). PNG'ler /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/goz_etiket/png/ altında.
- SAYISAL ÖZELLİKLER (bütün 26.663 Y1 olayı için, yalnız t'ye kadar; arastirma_cikti/goz_etiket/ozellik_Y1.csv.gz): F1 hat dokunuş sayısı (bölgede Low <= hat x 1,015), F2 hat eğimi (son / ilk dokunuş Low - 1), F3 bölge mum boyu medyanı / ATR250 (öncesi), F4 alt fitil payı medyanı (bölge mumları; (min(O,C) - L) / (H - L)), F5 açılış-dip yakınlığı: bölge mumlarında (O - L) / (H - L) medyanı, F6 üst fitil payı medyanı, F7 yeşil mum payı, F8 bölge boyu n, F9 bant (tavan / hat - 1), F10 net (son kapanış / ilk kapanış - 1), F11 kırılım mumu payı (C_t / tavan - 1), F12 kırılım mumu gövdesi / bölge medyan mumu, F13 kırılım günü hacim / bölge medyan hacmi, F14 büyük desen eğimi (250 bar, 25 barlık dip noktaları doğru eğimi), F15 120 gün konumu, F16 son 250 barda KIRILDI bölge sayısı, F17 bölge öncesi 60 gün düşüş (bölge başı kapanış / önceki 60 gün zirvesi - 1), F18 stop uzaklığı (C_t / hat - 1). Hepsi t'ye kadar; prefix değişmezliği testi.
- ÖN KAYIT (ON_KAYIT.md, kontrol tablosu + ik_kontrol_kapisi): aşağıdaki §5 ölçüm planı ve eşikleri aynen; AYRI COMMIT (etiketleme başlamadan).

## 4. AŞAMA B — ETİKETLEME (alt ajan B; anahtarı ve olay dosyasını AÇMAZ, yalnız PNG'leri ve bu bölümü okur)
Her PNG için Cemal'in gözüyle karar: OLUR (tam girilir) / OLMAZ / BELİRSİZ + neden kodları (birden çok) + 1-5 güven. CEMAL'İN GÖZÜ (kaynak: CEMAL_COL_KURALLARI K1-K42, KOR2_DERS_CEMAL D1-D14, CEMAL_DEGERLENDIRME E1-E11):
- C1 TABAN NET: hat en az 3 dokunuşla, aynı seviyede, eğimi aşağı değil; 1-2 mumluk hat = OLMAZ.
- C2 DİP SAVUNULMUŞ: dipler kırılmamış, alçalan dipler zinciri yok; yeni dip öncekinin altındaysa OLMAZ.
- C3 MUMLAR KÜÇÜK: bölge mumları öncesine göre küçük (fitiller dahil); dağınık / büyük mumlu pencere OLMAZ.
- C4 MUM ŞEKLİ: alt fitil kısa / yok, açılış dibe yakın, üst fitil biraz uzun olabilir (has yukarı mumları); tersi (üst fitilsiz, uzun alt fitil dişleri) zayıf.
- C5 KIRILIM MUMU BELİRGİN: kapanış tavanı net aşmış, gövdeli; tavana dokunan mum = giriş yok.
- C6 BÜYÜK DESEN: 120-250 barlık resim alçalan kanal / şemsiye ise küçük taban OLMAZ; yükselen ya da yatay büyük taban OLUR'a destek.
- C7 YAPI BOYU: düşüşe göre yeterli (çok küçük yapı güven vermez); 3-5 günlük yapı ancak kurum girişiyle ve küçük hedefle.
- C8 KAĞIT HAFIZASI: ekranda önceki benzer yapı patlamışsa OLMAZ; önceki yapılar hedefe gittiyse destek.
- C9 KUBBE: dipler kazan (çanak) şeklinde ve sağ kenar dönmüşse OLUR; şemsiye OLMAZ; dönüş görülmeden BELİRSİZ.
- C10 YOL ALMIŞ: fiyat tabandan çoktan uzaklaşmışsa kovalama yok (OLMAZ).
- C11 STOP UZAKLIĞI: kapanış hattan %10'dan uzaksa işlem yok.
- C12 ÇEKİŞTİRME / OLUŞUM YOK: yapı yok, yol ara kesiti = BELİRSİZ.
- C13 DEV MUM / ŞÜPHE: geçmişte dev tek mum = riskli.
Çıktı: arastirma_cikti/goz_etiket/etiket.json: {no: {karar, nedenler: [C..], guven, not (tek cümle)}}. 300 PNG'nin hepsi; etiketleyen her 50'de ilerleme yazar. Etiketleyen 'sonrası' hakkında hiçbir bilgiye sahip değildir ve tahmin yazmaz.

## 5. AŞAMA C — ÖLÇÜM ve EĞİTİM (alt ajan C; etiket.json + anahtar + olay_Y1 + ozellik_Y1)
- Birleştir: etiket x olay sonucu (h5, h10, st5, es_h5, es_st5, getiri).
- ÖLÇÜ 1 (önceden yazılı): OLUR grubunun +%5 payı vs OLMAZ grubunun +%5 payı (Fisher); OLUR KAT5 = Σ h5 / Σ es_h5 (ay kümeli bootstrap %95); OLMAZ KAT5 aynı; P(stop önce) OLUR / OLMAZ / eş. Pazar birleşik (n küçük); pazar bazlı bilgi. TUTAR = OLUR KAT5 alt uç > 1 VE OLUR +%5 payı > OLMAZ +%5 payı (Fisher p < 0,05) VE OLUR stop payı < eş. n OLUR < 30 ise ÖLÇÜLEMEDİ.
- ÖLÇÜ 2 (neden kodları): her C kodu için var / yok +%5 payı ve KAT5 (bilgi, BH q 0,10).
- EĞİTİM (önceden yazılı): F1-F18 ile lojistik regresyon, hedef = OLUR (1) / OLMAZ (0) (BELİRSİZ dışarı); 5 katlı çapraz doğrulama AUC (göz ne kadar sayısal özellikten öğrenilebiliyor); eğitilen model bütün 26.663 Y1 olayına uygulanır: 'GÖZ SKORU'. Üst beşte bir (skor) vs alt beşte bir: +%5 payı, KAT5 (eşli), stop payı; karar hücreleri (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) YAPI_HEDEF karar kuralıyla; etiket İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ aynı kurallarla. Üst beşte bir n >= 1.000 olan hücrelerde güç yeterli sayılır.
- Sızıntı denetimi: etiketlerin sonuç görmeden verildiği (aşama B ajanı anahtar / olay dosyası açmadı: dosya erişim günlüğü + B'nin raporu), özelliklerin t'ye kadar olduğu (prefix testi), skorun eğitimde kullanılan 300 olay dışında da raporlandığı (dış örneklem ayrı satır).
- RAPOR.md: özet, etiket dağılımı (OLUR / OLMAZ / BELİRSİZ, neden kodu sıklığı), ölçü 1-2 tabloları, eğitim (katsayılar: hangi özellik gözü en çok açıklıyor; AUC), göz skoru hücre tablosu, olasılık tablosu, karar, sınırlar (300 etiket, etiketleyen bir dil modeli = Cemal'in gözünün vekili; Cemal'in kendi etiketi değil). HAKEM PDF'İ (Cemal, 17 Kas akşam: 'tarafsız hakem olayım'): 40 sayfa, iki yarı, sonrası hiçbir sayfada yok, hisse adı yok: (1) sayfa 1-20 KÖR: yalnız grafik; Cemal OLUR / OLMAZ + neden yazar; sonra aşama B etiketiyle uyum ölçülür (Cohen kappa + çapraz tablo); (2) sayfa 21-40 AÇIK: grafik + aşama B'nin kararı + neden kodları + tek cümle notu; Cemal 'doğru / yanlış + neden' yazar; hangi C kuralının yanlış uygulandığı sayılır. Sayfalar 300 etiketli olaydan tohum 13 ile, OLUR / OLMAZ / BELİRSİZ dengeli (her yarıda 8 / 8 / 4) seçilir. Dosya: arastirma_cikti/goz_etiket/GOZ_HAKEM_SET.pdf + hakem_anahtar.json (gizli). Cemal'in yanıtı gelince `python GOZ_ETIKET.py hakem --cevap-dosya` ile iki yarı ayrı raporlanır.

## 6. RAPOR BAŞLIKLARI (her ajan)
SONUÇ, KONTROL LİSTESİ (14 madde; B için yalnız K2 / K12 / K13), HATA, ÖNERİLEN KAYIT, YENİDEN ÜRETİM KOMUTU.
