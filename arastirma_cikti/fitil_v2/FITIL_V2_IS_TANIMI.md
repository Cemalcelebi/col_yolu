# İŞ TANIMI — S+ v2 'TAM GİRİLİR' (Cemal, 17 Kas: 'kod bu kurallar eşiğinde tam girilir dediklerini, sonrasının verisini görmeden seç; kodu beni test ettiğin gibi test et')

Amaç: Cemal'in kör set notlarından çıkan kurallarla (CEMAL_COL_KURALLARI.md K10-K15) kodun 'tam girilir' günlerini YALNIZ o güne kadarki veriyle seçmesi; sonucun (60 gün, eşli) kapalı koşulması; sonra açılıp ORTAK CETVEL ile ölçülmesi; ayrıca kodun seçtiklerinden kör set (Cemal'e).
İKİ AŞAMA: AŞAMA 1 tasarım sınaması (etiketli sette eşik seçimi; ızgara önceden) + ön kayıt -> DUR (ana model commit eder). AŞAMA 2 'koş': evren ölçümü + kör set 2.

## 0. ÖN UÇUŞ KONTROLÜ
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
Defter dosyaları, FITIL_OBEK.py, FITIL_KOR.py, S6_TABAN.py, ORTAK_CETVEL.py, SIKISMA_*.py değişmez (import serbest). git commit / push yok. E-posta / anahtar yok. 'Al' / 'öneri' dili yok. Yeni: FITIL_V2.py (tek dosya; çakışma kapısı; tasarim / onkayit / kos / korset / olc komutları; IZ_KARNE.ik_kontrol_kapisi + ORTAK_CETVEL.oc_kapi), test_fitil_v2.py, arastirma_cikti/fitil_v2/{TASARIM.md, ON_KAYIT.md, RAPOR.md, sonuc.json, FITIL_V2_KOR_SET.pdf, kor2_anahtar.json}. Eşikler ızgara dışında ve sonuç görülünce değişmez.

## 2. S+ v2 TANIMI (her gün t, yalnız t ve öncesi; geçerli bar H > L, V > 0)
Pencere W = son k = 10 geçerli bar. Ölçüler (FITIL_OBEK ile aynı): alt, üst, ASİM = ort(üst) - ort(alt), ALTYOK payı.
  (1) ŞEKİL: ASİM >= 0,20 VE ALTYOK >= 0,50 (S+; ızgara: gevşek 0,10 / 0,40).
  (2) SAVUNMA HATTI: HAT = min(Low, W). Düz: (max(L, W) - min(L, W)) / medyan(R, W) <= duzEsik (ızgara 1,0 / 1,5 / kapalı). Sağlam: W içinde hiçbir kapanış HAT x (1 - hatTol) altında değil (tanım gereği) VE HAT >= önceki 30 geçerli barın en düşük Low'u x (1 - hatTol) (yeni dip yapmıyor; hatTol ızgara 0,02 / 0,03) VE C_t >= HAT (bugün hat üstünde).
  (3) DÖNÜM BAĞLAMI (düşüşün son mumları): W'den önceki 60 geçerli barın en yüksek kapanışına göre C_t düşüş >= dususEsik (ızgara 0,10 / 0,15 / 0,20).
  (4) YOL ALMAMIŞ: C_t <= HAT x (1 + yolEsik) (ızgara 0,05 / 0,10) VE C_t < max(High, W) (henüz pencere tepesini kırmamış).
  (5) TEPEDE DEĞİL: C_t <= 120 geçerli gün en yüksek kapanışı x (1 - 0,15) (sabit).
  TAM GİRİLİR günü = (1)-(5) birlikte; hisse başına 60 günde tek olay (cetvel tekilleştirmesi: ilk gün). Giriş = ertesi geçerli açılış. Çıkış bilgi: HAT x (1 - 0,02) altı kapanış 'stop' (K8), pencere tepesi üstü kapanış 'kırılım'.
Bilgi satırları: (1) tek başına (= Ç187 S+), (1)+(2), (1)+(2)+(3); hepsi ayrı satır (çoklu karşılaştırma: ana karar yalnız TAM; bilgi BH q 0,10).

## 3. AŞAMA 1 — TASARIM SINAMASI (etiketli set; getiri bakılmaz)
Etiket seti: Cemal'in E dediği kör set sayfaları (kor_anahtar.json + kor_cevap_cemal.json; 19 sayfa; pencere son günü = sayfa tarihi) = POZİTİF; H dediği 5 sayfa + S- sayfalarında E demedikleri = NEGATİF; ayrıca Cemal'in üç örneği POZİTİF: TEHOL 2025-05-06..28 (herhangi bir gün), BINBN 2024-12-23..2025-01-13, PAPIL 2025-11-14..26; TEHOL Ara 2024 - Şub 2025 yükseliş bacağı NEGATİF; DGXX Eki-Kas 2026 NEGATİF. Not: Cemal'in E notlarının çoğu 'şekil evet ama giriş değil' (yol almış / hat kırık / aşağı): bu yüzden POZİTİF'i ikiye ayır: E-GİRİŞ (notunda 'girerdim / stoplu girilir / dönüm / akümülasyon / yukarı': sayfa 3, 9, 6, 22, 16, 17, 26) ve E-ŞEKİL (öteki E'ler). Hedef: E-GİRİŞ + 3 örnek yakalansın (TAM günü aralıkta var), E-ŞEKİL'de (1) tutsun ama TAM tutmasın (hat kırık / yol almış), NEGATİF'te TAM tutmasın. Izgara (3 x 2 x 2 x 3 x 2 = 72 nokta) puanı: E-GİRİŞ + 3 örnek doğru + NEGATİF elenen + E-ŞEKİL'de (1) var ama TAM yok; eşitlikte en sade. Tablo: her etiket x seçilen nokta (hangi şart düşürdü). TASARIM.md + ön kayıt (ON_KAYIT.md: eşikler, sha'lar, kontrol listesi, OLAY SAYIMI getirisiz: evrende TAM günü sayısı hücre başına; çöl nadir mi: hisse-yıl başına TAM sayısı) -> DUR.

## 4. AŞAMA 2 — KOŞ (ana model 'koş' deyince)
- ORTAK CETVEL v1.0: TAM satırı (ve bilgi satırları) ABD / AVR / BIST x 2023 / 2024-26 (+ 2016-22 keşif bilgi); eşli fark 60 gün, dört şart, olasılık tablosu (P +%100 / -%50 katları); 'önce kırılım mı stop mu' oranı (K6 / K8); etiket kuralı Ç187 ile aynı (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ), BIST bilgi. Hayatta kalma yanlılığı raporda.
- KÖR SET 2 (Cemal'e): kodun TAM dediği günlerden rastgele 30 (BIST 15 + ABD 15; 2016-2026-08; her hisse bir kez) + 10 'şekil var ama TAM değil' (hangi şart düşürdü anahtarda) = 40 sayfa, karışık; pencere + öncesi 40 mum, sonrası yok, adsız; anahtar gizli (sayfa -> hisse, tarih, grup, r20, r60, önce kırılım / stop). `python FITIL_V2.py olc --cevap "1:E,..."`.
- RAPOR.md: ÖZET (bulgu dili) · TANIM ve eşikler · TASARIM sonucu · OLAY SAYIMI · HÜCRE TABLOSU · OLASILIK TABLOSU · KIRILIM / STOP ORANLARI · KARAR (önceden yazılı) · KÖR SET 2 · KONTROL LİSTESİ · HATA · ÖNERİLEN DEFTER METNİ (IK_KAYIT Ç, IK_ILERI, IK_GOREV).
