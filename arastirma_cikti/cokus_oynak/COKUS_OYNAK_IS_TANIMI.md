# İŞ TANIMI — ÇÖKÜŞ SONRASI OYNAK HİSSE (Cemal'in hipotezi, 16 Kas 2026) + bugünün piyango profili listesi

Cemal (16 Kas): "Fon yüzünden bütün hisseler %40'ın üstünde düştü; bundan sonra çok fazla düşmeyeceğini öngörüyorum. Normal zamanda risk çok yüksek olur; bu dönemde risk büyük değil ve gerçekten oynak bir hisse seçilince yükselme ihtimali çok yüksek olur."
HİPOTEZ H (ölçülecek): BIST'te geniş çöküşten sonra, en oynak (ve / ya da en çok düşmüş) hisseler sonraki 120 / 250 günde (a) +%100 olasılığında ötekilerden yüksek, (b) -%50 olasılığında ötekilerden YÜKSEK DEĞİL (Cemal: 'risk büyük değil'). İkisi birden tutarsa EMARE (iki çöküş = iki olay; İZ demek için az); yalnız (a) tutup (b) tutmazsa PİYANGO (çift kuyruk); (a) tutmazsa hipotez desteklenmedi. Etiket ÖLÇÜLEMEDİ: hücre n < 30.
Yazan: ana model. Yapan: alt ajan. Denetim: ana model (>= 2 hücre yeniden üretim). Ön kayıt: bu dosya + ajanın ÖN KAYIT bölümü (eşikler aşağıda, sonuç görülmeden; commit koşudan önce).

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
Defter dosyaları (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md) ve mevcut .py modülleri değişmez. git commit / push yok. E-posta / anahtar yok. Yeni dosyalar: COKUS_OYNAK.py (tek dosya; çakışma kapısı; ön kayıt / kos / rapor komutları; kontrol kapısı IZ_KARNE.ik_kontrol_kapisi), test_cokus_oynak.py, arastirma_cikti/cokus_oynak/ (ON_KAYIT.md, RAPOR.md, sonuc.json, olay csv.gz küçükse). Eşikler sonuç görüldükten sonra değişmez; sapma olursa SAPMA başlığıyla.

## 2. VERİ
- Geçmiş: V_BIST.pkl (scratchpad/veri; düzeltilmiş fiyat, 2016-2026-08; kriz kesiği 31.08.2026 -> 2026 çöküşünün SONUCU ölçülemez, yalnız 'bugün' listesi). Canlı: scratchpad/canli/bist_3y.pkl (yfinance, 16 Kas; bugünün listesi için). Geçerli bar H > L, hacim > 0. Hayatta kalma: evren bugün işlem görenler; 2018 / 2020'de batanlar yok -> sonuçlar yukarı yanlı, raporda yazılır (K7).
- Piyasa: XU100 (V_BIST'te varsa; yoksa evren medyanı). Çöküş tanımı (sabit): evren medyan 120 gün getirisi <= -%30 olan İLK gün = çöküş günü; sonraki çöküş için en az 250 gün ara. Beklenen olaylar: 2018 (Ağu-Eyl), 2020 (Mar), 2026 (Eyl-Ekim; sonuç yok). Çöküş günlerini raporda yaz; 2 olaydan az çıkarsa tanımı DEĞİŞTİRME, 'ÖLÇÜLEMEDİ' yaz.
- Giriş: çöküş gününden sonraki 5. işlem günü açılışı (K5; 'dip' bilinmez, sabit gecikme). Ek giriş (bilgi): çöküş gününden 20 gün sonra.

## 3. ÖLÇÜLER (giriş günü itibarıyla, yalnız geçmiş)
- Oynaklık σ250 = günlük log getiri std (250 bar); beşlik dilim (evren içinde, giriş günü).
- Düşüş: 250 gün zirvesinden düşüş; beşlik dilim.
- Likidite: 60 gün ort. işlem değeri; alt %20 hariç (cetvel).
- Küçüklük: işlem değeri sıralaması (piyasa değeri yok; raporda yaz).
- Fon lekesi 2026 için (K25 tablosu); 2018 / 2020 için yok.
- Sonuç: r120, r250 (kapanış / giriş - 1); önce +%100 (250 gün içinde kapanış >= 2 x giriş), önce -%50 (kapanış <= 0,5 x giriş); 60 gün MDD.

## 4. KARŞILAŞTIRMA (önceden yazılı)
Her çöküş olayı ayrı hücre + birleşik. σ250 en üst beşlik (OYNAK) vs orta üç beşlik (TABAN): P(+%100), P(-%50), medyan r250, ortalama r250; fark ve ay-kümesiz bootstrap %95 aralığı (hisse düzeyinde 1.000 yeniden örnekleme). Aynısı 'en çok düşmüş beşlik' için. Çapraz: OYNAK ve en çok düşmüş. Eşik: H(a) tutar = OYNAK P(+%100) - TABAN P(+%100) > 0 ve alt uç > 0; H(b) tutar = OYNAK P(-%50) - TABAN P(-%50) alt uç <= 0 (yani anlamlı yüksek değil). Katlar ve olasılık tablosu (CLAUDE.md 'olasılık tablosu' biçimi).
Kıyas için 'normal dönem' kontrolü: çöküş dışı rastgele 2 giriş günü (2017, 2023; sabit: her yılın ilk işlem günü) aynı tablo: oynak hissenin kuyrukları normal zamanda nasıl? Cemal'in 'normal zamanda risk yüksek, çöküşte değil' tezi buna karşılık.

## 5. BUGÜNÜN LİSTESİ (16 Kas 2026; ölçüm değil, aday listesi)
Canlı veriyle, 13 Kas karar günü: evren medyan 120 gün getirisi (çöküş eşiğini geçti mi yaz). Piyango profili: σ250 en üst beşlik VE zirveden >= %60 düşmüş VE likidite alt %20 dışı VE fon lekesi yok VE Uzak listede yok; sıralama σ250 (büyükten); ilk 15: sembol, σ250, düşüş, r60, likidite, fon, S6 durumu (S6_TABAN varsa), son 20 günde en büyük gün. Geçmiş testin sonucunu listenin başına yaz: '2018 / 2020'de bu profil: P(+%100) = x, P(-%50) = y'. Hiçbir isme 'al' deme.

## 6. RAPOR (RAPOR.md): ÖZET (bulgu) · ÇÖKÜŞ GÜNLERİ · OLASILIK TABLOSU (olay x dilim: n, P+100, P-50, medyan r250, kat, alt uç) · KARAR (EMARE / PİYANGO / DESTEKLENMEDİ / ÖLÇÜLEMEDİ; önceden yazılı kurala göre tek satır) · NORMAL DÖNEM KIYASI · BUGÜNÜN LİSTESİ · HAYATTA KALMA UYARISI · KONTROL LİSTESİ · HATA · ÖNERİLEN DEFTER METNİ (IK_KAYIT Ç satırı, IK_ILERI satırı: 2026 çöküşü sonucu Mart 2027 / Kasım 2027'de aynı komutla).
