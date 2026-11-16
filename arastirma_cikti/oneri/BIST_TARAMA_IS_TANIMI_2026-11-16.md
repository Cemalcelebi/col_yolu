# İŞ TANIMI — BIST CANLI TARAMA (16 Kasım 2026; öneri modülü TARAMA kapısı; Cemal: '5.900 TL ile riski seven biri olarak hangi hisse')

Yazan: ana model. Yapan: alt ajan (tarama). Sonra ayrı alt ajan: DOSYA kapısı (KAP). Ana model: RİSK kapısı ve denetim.
DÜRÜSTLÜK: BIST'te ölçülmüş iz YOK (IZ_DEFTERI). S6 / S5 göz aracıdır; sektör rüzgârı ABD'de EMARE (bilinen etki), BIST'te ölçülmedi; üretim D13 İZ DEĞİL. Bu tarama 'ölçülmüş sinyal yok' notuyla ADAY sıralamasıdır, öneri değildir. Taban oranlar: 12 ayda ikiye katlanma %4-7, yarıya inme %6-7; oynak havuzda %9-16 / %17-21 (ONERI_DEFTERI risk süzgeci).

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
- Dokunma: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md ve .py modülleri (yalnız import / oku). git commit / push yok. E-posta / anahtar yok. Ücretli veri yok.
- Yeni dosyalar yalnız arastirma_cikti/oneri/ altında: BIST_TARAMA_2026-11-16.md, bist_tarama_2026-11-16.csv, tarama_kosu.py (koşu betiği; tek dosya, hata yakalama, log).
- Veri: yfinance (kuruldu; proxy üzerinden çalışıyor, 16 Kas 2026 barı geliyor) ile sektor_BIST.csv'deki semboller (+'.IS'), 3 yıl günlük, auto_adjust=False; scratchpad'e pkl (sembol -> OHLCV DataFrame). Hacim 0 / H=L barları geçerli bar sayma. İndirme hatalarını listele. Bugün (16 Kas) seans açık olabilir: 16 Kas barı YARIM olabilir -> karar son TAM bar (13 Kas) ile; 16 Kas barı 'bilgi' olarak ayrı sütunda.

## 2. ÖLÇÜLER (her hisse; yalnız karar günü ve öncesi)
1. S6 TABAN (S6_TABAN.s6_taban, seçilen eşikler, değiştirme): açık bölge var mı; n; bant; net; sınıf; tavan; tavana uzaklık (C / tavan - 1); son 10 barda AL var mı (kırılım yeni), son 10 barda KIRILDI var mı.
2. S5 (SIKISMA_OBEK.so_s5 'BIST'): son 20 barda karar günü var mı; sınıf.
3. Sektör rüzgârı (D9_YENIDEN.d9_ruzgar_ref ile COL_v1 tanımı; sektor_BIST.csv alt_bist): ruz, sepet, rüzgâr bayrağı. Üretim raporunda (rapor/son_rapor.txt 13 Kas) rüzgârlı sektör 0, piyasa medyanı 60g -%33: bunu rapora yaz.
4. Üretim D13 adayı (rapor/son_rapor.txt BEKLE: ONCSM, METRO, ALBRK, HUNER, EGEGY, ULUFA) bayrağı.
5. Fon lekesi: scratchpad/veri/G.pkl / oran.pkl / dol.pkl (K25 fon tabloları; yapıyı koddan / FON_IZI'den anla) ile son raporda tasfiye fonu payı > 0 olan hisse -> LEKE. ONERI_DEFTERI 'Uzak' listesi (TEHOL, PEKGY, ODINE, ANELE, MANAS, IEYHO, GUNDG, DSTKF, OZATD, TRHOL, SKYLP) -> HARİÇ. 30 Kas MSCI çıkarması listesi (TEHOL, PEKGY, IEYHO, LYDHO, ALKLC, ODINE) -> bayrak.
6. Likidite: 20 gün ortalama işlem değeri (TL); evrenin alt %20'si HARİÇ (cetvel kuralı); 5.900 TL alım için fiili sorun yok, yaz.
7. Konum: 60 / 120 / 250 gün getiri, 120 gün aralığında konum, 250 gün zirvesinden düşüş, ATR%250, 20 günde en büyük hacimli günün getirisi (bilanço tepkisi vekili; 3Ç26 bilançoları Ekim-Kasım'da geldi), son 5 gün hacim / 60 gün hacim.
8. Piyasa bağlamı: XU100 (XU100.IS) 60 / 120 gün getiri ve 250 gün zirvesinden düşüş; BIST fon krizi (31 Ağu 2026 sonrası) notu.

## 3. SIRALAMA (önceden yazılı, sonuç görülmeden; değiştirme)
ŞART (hepsi): LEKE yok, Uzak listede değil, likidite alt %20'de değil, son 10 barda KIRILDI yok.
PUAN: S6 açık bölge +2; S6 AL son 10 bar +2 (bölge kapanmış ama kırılım taze); S5 karar son 20 bar +1; sektör rüzgârı +1; tavana uzaklık [-%5, +%3] (kırılım eşiğine yakın) +1; 250 gün zirvesinden düşüş >= %30 (Cemal: 'tepeden düşmüş') +1; 20 günde en büyük hacimli gün getirisi >= +%5 (bilanço tepkisi vekili) +1. Eşitlikte likidite yüksek olan üstte.
Çıktı: ilk 15 + Cemal'in izleme listesi (PNLSN, FORTE, GWIND, EUPWR, SEGMN, TKNKA, GIPTA, SVGYO, KARCL, YEOTK, HDFGS, SKBNK) aynı ölçülerle ayrı tablo (puanlı). YEOTK Cemal'in mevcut pozisyonu / tezi: ölçülerini yaz.

## 4. RAPOR (BIST_TARAMA_2026-11-16.md)
ÖZET (bulgu dili: kaç hisse tarandı, kaç şartı geçti, ilk 5 ve puanları, piyasa bağlamı) · TABLO (ilk 15, bütün ölçüler) · İZLEME LİSTESİ TABLOSU · HARİÇ TUTULANLAR (leke / uzak / likidite / kırıldı sayıları) · VERİ NOTU (indirme hataları, yarım bar) · KONTROL LİSTESİ (K1-K14) · HATA · 'ÖLÇÜLMÜŞ SİNYAL YOK' uyarısı ve taban oranlar · DOSYA kapısı için ilk 5 aday listesi (KAP'ta bakılacaklar: 3Ç26 gelir / kâr ivmesi, sözleşme, nakit, borç, seyrelme / bedelli, going concern, fon / tedbir / SPK lekesi).
