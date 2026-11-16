# İŞ TANIMI — FİTİL ÖBEĞİ (Cemal'in hipotezi, 16 Kas 2026): alt fitilsiz / üst fitilli mum öbeği yukarı, üst fitilsiz / alt fitilli öbek aşağı mı götürür?

Cemal: "PAPIL'de alt fitil yok, üst fitil biraz uzun mumlar öbek olunca has yukarı çıkma mumları; DGXX'te tersi (üst fitil yok, aşağı sert dişler) ve fiyat 2,50'den 2'nin altına düştü." Ana model DGXX'te doğruladı (27 Eki - 13 Kas: alt fitil medyan 0,28 > üst 0,18; 16 Kas üst fitilsiz, 2,02). Hipotez H: son k barda fitil asimetrisi (alt fitil payı eksi üst fitil payı) yönü öngörür: ALT FİTİLSİZ öbek (üst fitiller uzun) -> sonraki 20 / 60 günde eşlerden iyi; ÜST FİTİLSİZ öbek -> eşlerden kötü. Not: Cemal'in okuması klasik 'kapanış dipte = satış' okumasının tersi; test iki yönü de ölçer.
Ön kayıt: bu dosya (commit koşudan önce) + ajanın ON_KAYIT.md (kontrol listesi 14 satır, olay sayımı, kod sha). Eşik sonuç görülünce değişmez.

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
Defter dosyaları ve mevcut .py modülleri değişmez; git commit / push yok; e-posta / anahtar yok. Yeni: FITIL_OBEK.py (tek dosya; çakışma kapısı; onkayit / kos / rapor; IZ_KARNE.ik_kontrol_kapisi + ORTAK_CETVEL.oc_kapi), test_fitil_obek.py, arastirma_cikti/fitil_obek/{ON_KAYIT.md, RAPOR.md, sonuc.json, olay csv.gz (küçükse)}. Cetvel ORTAK_CETVEL v1.0 (oc_veri, oc_olc, oc_hucre; eşli fark 60 gün, dört şart, olasılık tablosu) DEĞİŞMEZ. Kapalı konu 'tek göstergeye göre alım' açılmaz: bu bir yön / parmak izi ölçümüdür, kural tanımı önceden sabit.

## 2. TANIM (sabit)
Geçerli bar (H > L, V > 0). Her bar: aralık R = H - L; alt = (min(O,C) - L) / R; üst = (H - max(O,C)) / R; gövde = |C - O| / R.
Öbek penceresi k = 10 geçerli bar (ek bilgi: k = 5 ve 15). Pencere ölçüleri: A = ortalama alt, U = ortalama üst, ASİM = U - A (pozitif = üst fitiller baskın = Cemal'in 'yukarı' öbeği), ALTYOK = alt < 0,10 olan bar payı, USTYOK = üst < 0,10 olan bar payı, KUCUK = pencere medyan R / C <= 0,75 x ATR%250 (Cemal'in öbekleri küçük mumlu; bilgi olarak şartlı / şartsız iki satır).
Sinyal günleri (t = pencerenin son günü; giriş ertesi açılış; hisse başına 60 günde tek olay = cetvel tekilleştirmesi):
  S+ (YUKARI öbek): ASİM >= 0,20 VE ALTYOK >= 0,50 (yarıdan çoğu alt fitilsiz) — pencere son günü.
  S- (AŞAĞI öbek): ASİM <= -0,20 VE USTYOK >= 0,50.
  Bilgi: S+ ve S- yalnız ASİM onda birlik (üst / alt %10) ile; KUCUK şartlı sürümler; k = 5 / 15.
Beklenen yön: S+ eşli fark > 0 (dört şart), S- eşli fark < 0 (ters yön; cetvelde 'kaçınma' olarak ölçülür: fark = eşli - olay). Karar hücreleri: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 (CLAUDE.md); BIST bilgi. Etiket: İZ (dört hücre), EMARE, ÖLÇÜLEMEDİ (n < 30 ya da güç yetersiz), DESTEKLENMEDİ (güç yeterli, tutmadı). S+ ve S- ayrı etiket.
Çoklu karşılaştırma: ana karar yalnız S+ ve S- (k=10); bilgi satırları BH q 0,10 ile.

## 3. VERİ
ORTAK_CETVEL.oc_veri ile V_BIST / V_ABD / V_AVR (scratchpad/veri; k34_yahoo scratchpad/veri2 yoksa yalnız V_ABD ile ve raporda yaz), kriz kesiği 31.08.2026, likidite alt %20 hariç (cetvel). Hayatta kalma yanlılığı raporda.

## 4. ÖRNEK DOĞRULAMA
PAPIL 2025-11-13..12-09 penceresinde S+ tutuyor mu (hangi gün); DGXX (k34 verisinde varsa) 2026-10-27..11-13'te S- tutuyor mu; tutmuyorsa hangi şart; tanım değiştirilmez, raporda yazılır. Ek: FENER, DESA, YKSLN doğru bölgelerinde S+ var mı (önceki parmak izi tablosuna göre beklenmez; bilgi).

## 5. RAPOR (RAPOR.md): ÖZET (bulgu dili) · TANIM · OLAY SAYIMI (hücre başına n) · HÜCRE TABLOSU (S+ / S- x pazar x dönem: n, eşli fark, alt uç, sıra, portföy, dört şart, güç, durum) · OLASILIK TABLOSU (P+%100 / P-%50 katları, 250 gün) · BİLGİ SATIRLARI (k, KUCUK, onda birlik) · ÖRNEK DOĞRULAMA · KARAR (önceden yazılı etiket kuralı) · KONTROL LİSTESİ · HATA · ÖNERİLEN DEFTER METNİ (IK_KAYIT Ç, IK_ILERI, IK_GOREV).
