# İŞ TANIMI: GOZ_ETIKET `tur` — hakem turları programı, TUR 1 (18 Kas 2026)

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
GOZ_ETIKET_IS_TANIMI.md §2 aynen (defter dosyalarına dokunma; `git add -A` yok; push yok; PNG scratchpad). GOZ_ETIKET.py'nin çalışan kısmına dokunma; `tur` komutları EKLENİR. Testler test_goz_etiket.py'ye. CLAUDE.md 'Hakem turları' bölümü (ana model yazdı) program tanımıdır; aynen uygula.

## 2. KOMUTLAR
- `tur ac --no K`: örneklem (tohum 100 + K): olay_Y1 olaylarından ABD 20 + AVR 5 + BIST 5 = 30; 2023 / 2024-26 dönemleri; daha önce GOZ_ETIKET örneklemine (anahtar.json 300) ya da önceki turlara girmiş olaylar ve aynı hisseler hariç; sonuç sütunları okunmadan (usecols). Çıktı: arastirma_cikti/goz_etiket/tur/K/ altında TUR_K_KOR.pdf (30 sayfa: grafik 120 bar + S6 bölgesi + 'Cemal: ✓ OLUR / X OLMAZ / ? BELİRSİZ' satırı; sonrası ve hisse adı yok), tur_K_anahtar.json (gizli), tur_K_png/ (scratchpad).
- `tur model --no K --etiket DOSYA`: model etiketlerini (ayrı alt ajan yazar; biçim etiket.json ile aynı) alır, sha'sını tur_K_muhur.json'a yazar (Cemal'in yanıtı gelmeden commit).
- `tur olc --no K --cemal DOSYA`: Cemal'in yanıtı (JSON {sayfa: cevap}; ana model yazıya döker) + model etiketi + sonuçlar (olay_Y1 h5 / h10 / st5 / getiri): iki taraf için isabet tablosu, BAŞARI (CLAUDE.md tanımı), taban (eş payı), Fisher p, uyum (kappa), yanılınan sayfalar listesi (iki taraf), birikimli tablo (önceki turlar dahil). Çıktı TUR_K_SONUC.md ve TUR_DEFTERI.md (ekleme).
- Mühür / sıra denetimi: olc, model mühürünün Cemal yanıtı dosyasının git zamanından önce olduğunu denetler.

## 3. TUR 1 İŞİ (bu ajan)
(a) Komutları ve testleri yaz (örneklem dışlama; sonuç sütunu okunmuyor; PDF'te sonrası yok; mühür sırası; başarı hesabı elle doğrulama). (b) `tur ac --no 1` koş. (c) Commit (kod, test, PDF, anahtar; PNG hariç). Model etiketi ayrı ajan yapacak; sen yapma. Raporunda: SONUÇ (örneklem dağılımı, PDF yolu, sayfa sayısı), KONTROL LİSTESİ, HATA, ÖNERİLEN KAYIT, YENİDEN ÜRETİM.
