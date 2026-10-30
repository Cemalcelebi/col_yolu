# K55 — DALLANMALI İZ ARAMA: ARAŞTIRMA PLANI (30 Ekim 2026; ONAY BEKLİYOR, kod yazılmadı, koşu yok)

Cemal'in "Kuantum dallanmalı iz arama sistemi" talimatının ilk teslimatı. Bu belge plan ve veri gereksinimidir; onaylanmadan büyük koşu başlamaz. K51 / K52 / K53 / K54 çıktıları ve kodları değişmedi; arşiv noktası main dalındaki 83e5de8 commit'idir (yerel etiket `k51-k54-arsiv-2026-10-30`; etiket gönderimi bu oturumda 403 ile reddedildi, commit kaydı yeterlidir).

## 0. Özet (telefonda okunacak kısım)

- Çalışma hipotezi: büyük yükselişlerden önce ölçülebilir bir davranış değişimi olabilir, ama doğru yerde / ölçekte / değişkenle aranmamış olabilir. Kanıtlanmış sayılmaz; başlangıç varsayımı.
- 10 ana dal, 100 hücre tanımlandı (bölüm 4). Her hücrede: soru, değişken tanımı, veri, yöntem, durum notu (yeni mi, eski çalışmayla çakışıyor mu, kapalı konu mu, veri var mı).
- 100 hücrenin 71'i yalnız günlük OHLCV + endeks ile ölçülebilir (D01-D06, D10'un çoğu); 29'u ek veri ister (D07 SEC finansal tablolar 2021+, D08 SEC başvuruları / 13F, D09 makro seriler).
- Eski çalışmayla **doğrudan çakışan** 9 hücre var (bölüm 7); bunlar yeniden koşulmaz, yalnız "bilinen etki" kıyası olarak kalır. **Kapalı konuya** dokunan 6 hücre (VIX / DXY / faiz makro, hacim onayı, BB daralması) yalnız Cemal onayıyla açılır.
- Önerilen sıra: Faz 1 OHLCV dalları (D01-D06, D10 OHLCV hücreleri; ~80 hücre), Faz 2 SEC dalları (D07, D08), Faz 3 makro (D09), Faz 4 dallanma + bağımsız dönem.
- Maliyet: para 0 (bütün veriler ücretsiz; Tiingo kotası yalnız batan evreni için Kasım). Geliştirme: Faz 1 için ortak panel + 6 modül + testler; hesap süresi hücre başına 1-4 dk, Faz 1 toplam 3-5 saat koşu.
- Karar gereken 6 madde bölüm 8'de.

## 1. Çerçeve: ne aranıyor, ne aranmıyor

- Aranan: büyük yükselişten ÖNCE, yalnız o güne kadar bilinen veriden üretilen, yükselmeyen eşlerde görülmeyen, yıllar arası tekrarlanan davranış değişimi.
- Aranmayan: eski göstergelerin yeni adla sunulması (CMF, OBV, MFI, RSI, MACD, Bollinger, KNN, şekil adları). Bir hücrenin değişkeni eski bir göstergeyle korelasyonu |ρ| > 0,8 çıkarsa hücre "eski gösterge vekili" diye işaretlenir ve bağımsız bilgi iddiası düşer (bölüm 2.7).
- K51'in ölçüleri (vol60, dd250, log_dv20, r60, ar20, küçük mum imzası, hacim kuruması, hacimli taban, çekirdek sıkışma) yeni hücre değildir; yalnız eşleştirme / kontrol değişkeni olarak kullanılır.
- Alım-satım kuralı, stop, portföy bu planda yok (bölüm 2.9): önce izin tahmin gücü, iz doğrulanırsa işlem sistemi ayrı plan.

## 2. Bütün hücrelerde ortak kurallar (sabit; sonuç görüldükten sonra değişmez)

2.1 Evren
- ABD fonsuz evren: 3.260 sembol (V_ABD 1.408 + K34 Yahoo 1.435 + K34 Tiingo batan 422 − 7 fon; `evren_disi_ABD.csv`). K54 sınıfları (iflas / birleşme / sembol değişimi) etiketlerde aynen uygulanır (iflas −%100, birleşme ek kayıp yok, 4b kesim).
- Avrupa (V_AVR 561) doğrulama pazarı; BIST bilgi. Karar hücreleri CLAUDE.md gereği ABD + AVR.
- Fon krizi kesimi: fiyat 31.08.2026'da biter; en geç olay Haziran 2026 başı.
- Hayatta kalma: batanlar 422'lik Tiingo örneklemiyle sınırlı; eksik batıklar Kasım kotası sonrası eklenirse panel yeniden kurulur (sürüm numarası değişir).

2.2 Dönemler (kronolojik, kilitli)
- KEŞİF: 2016-06 → 2021-12 (özellik keşfi, eşik seçimi, dallanma kararları yalnız burada).
- İÇ DOĞRULAMA: 2022-01 → 2023-12 (KEŞİF'ten çıkan adayların ilk sınavı; dallanma kararında kullanılmaz).
- BAĞIMSIZ: 2024-01 → 2026-06 (kilitli; bir hücre ailesi için EN FAZLA BİR KEZ açılır, "DOĞRULAMA BEKLİYOR" durumuna gelen adaylar için).
- İLERİ: sinyal ≥ 01.09.2026, değerlendirme ≥ Mart 2027.
- Purging 60 işlem günü (olay penceresi), embargo 10 gün; özellik t gününe kadar, giriş t+1 açılış.

2.3 Olay tanımları (geriye doğru yöntem; sabit, keşif amaçlı)
- Y60: 60 işlem gününde +%30 (giriş ertesi açılıştan en yüksek kapanışa değil, 60. gün kapanışına; ayrıca "yolda +%30'a değdi" bilgi sütunu).
- Y120: 120 günde +%50. Y250: 250 günde +%100.
- Olay günü = yükselişin başladığı gün (pencerenin ilk günü). Bir hissede aynı pencere içinde yalnız ilk olay. Olay başına öncesi pencereler: 5, 10, 20, 40, 60 gün.
- Karşılaştırma: aynı gün aynı oynaklık ondalığı × likidite üçlüsü × sektör × rejim içinde yükselmeyen hisseler (k = 5 en yakın; dd250 ±0,10).

2.4 Üç yöntem (her hücrede, veri el verdiğince)
- A. Olay öncesi davranış: değişkenin olay öncesi 5/10/20/40/60 gün dağılımı vs aynı tarihli olmayanlar; ölçü = standartlaştırılmış fark (Cohen d) ve AUC.
- B. Eşleşmiş kontrol (ileriye doğru): değişkenin üst / alt beşte biri sinyal sayılır; sinyal günü FI_OLCUT eşli fark r60 (ay kümeli bootstrap, hisse × çeyrek kümeli ikinci aralık), 10 yuvalı slot portföyü rastgele sağlaması.
- C. Değişim noktası: hissenin kendi 250 günlük geçmişine göre CUSUM / kayan z-skoru; değişim tarihi ile olay tarihi arasındaki gecikme ve yükselmeyenlerde değişim sıklığı (yanlış pozitif).
- Üç yöntem aynı veriyi kullanır; üç bağımsız kanıt sayılmaz. Tutarlılık puanı 0-3 yalnız sıralama içindir.

2.5 Ölçütler (hücre × dönem)
- n ≥ 30 olay (yöntem A) / n ≥ 30 sinyal (B); altı VERİ YETERSİZ.
- Etki: |d| ≥ 0,20 (A) VEYA eşli fark ≥ +0,05 ve ay kümeli alt uç > 0 (B).
- Tekrar: işaret yıl yıl aynı (keşif döneminde en az 5 / 6 yıl).
- Rejim: BOĞA ve AYI alt kümelerinde işaret aynı (n ≥ 30 olan rejimlerde).
- Yanlış pozitif: sinyal günlerinin olay olmayan payı; taban oranına göre lift ≥ 1,3.
- Maliyet: eşli fark komisyon + kayma sonrası > 0 (K51 maliyet modeli).
- Veri kalitesi: hücre değişkeninin eksik payı < %20; aksi halde VERİ YETERSİZ.

2.6 Çoklu test
- Aile = ana dal (10 aile). Keşif döneminde her hücre için p (bootstrap) kaydedilir; aile içinde BH-FDR %10. Hücre içindeki varyantlar (pencere 5/10/20/40/60, olay Y60/Y120/Y250, beşte bir / onda bir) Holm ile düzeltilir; "en iyi varyant" raporlanır ama karar düzeltilmiş p ile.
- Bütün varyantlar `K55_VARYANTLAR.csv`'de saklanır; başarısızlar silinmez. Deflated Sharpe / PBO yalnız DOĞRULAMA BEKLİYOR adayları için.

2.7 Eski göstergeyle örtüşme denetimi
- Her hücre değişkeni, 20 eski gösterge (CMF, OBV, MFI, RSI, MACD, BB genişliği, ATR, momentum 12-1, 1 ay tersine dönüş, vol60, dd250, log_dv20, r60, ar20, imza, hacim kuruması, HT, K48 ilk 3 bileşen) ile korelasyon tablosuna girer. |ρ| > 0,8 → "vekil", bağımsız bilgi iddiası yok.

2.8 Durumlar ve dallanma
- KEŞİF: keşif döneminde 2.5 ölçütleri geçti (FDR sonrası). → 10 alt hücre açılır (bölüm 5 şablonu), yine yalnız keşif döneminde.
- DERİNLEŞTİR: alt hücrelerin ≥ 3'ünde etki kalıyor ve neden açıklanabiliyor.
- DOĞRULAMA BEKLİYOR: iç doğrulama (2022-23) ölçütleri geçti; bağımsız dönem açılmadı.
- DOĞRULANDI: bağımsız dönemde (2024-26) ve AVR'de ölçütler geçti (bir kez açılır).
- REDDEDİLDİ: herhangi bir aşamada ölçüt altı; kayıt kalır, zorlanmaz.
- VERİ YETERSİZ: n < 30 ya da eksik payı > %20.

2.9 Stop ve işlem modeli
- Bu planda yok. K51'in stoplu / stopsuz testleri tarihsel kayıt. DOĞRULANDI çıkan iz için ayrı işlem planı: stop fiyatı ≠ gerçekleşen fiyat, gap / durdurma / delist, aynı mumda stop ve hedef belirsizse kötümser varsayım, komisyon + kayma.

## 3. Veri envanteri ve kalite denetimi

| Veri | Kaynak / dosya | Kapsam | Dönem | Dallar | Durum |
|---|---|---|---|---|---|
| ABD günlük OHLCV | V_ABD.pkl, k34_yahoo.pkl, Tiingo csv (islenmis-veri) | 3.260 sembol (fonsuz) | 2015-06 → 2026-08 | D01-D06, D10 | hazır; K54 sınıfları var |
| AVR / BIST OHLCV | V_AVR.pkl, V_BIST.pkl | 561 / 574 | 2015 → 2026-08 | doğrulama / bilgi | hazır |
| Endeksler | endeks.pkl: SPY, IWM, ^STOXX, XU100 | 4 seri | 2015-06 → 2026-08 | D06, D09 | hazır; sektör ETF'leri yok (Yahoo'dan ücretsiz eklenir) |
| Sektör | sektor_ABD.csv, k35_sic.csv | evren | sabit | eşleştirme, D06, D07 | hazır |
| Emtia / kur / faiz | k36/surucu.pkl: altın, gümüş, petrol, bakır, çelik, alüminyum, buğday, USDTRY, ^TNX, CDS (TR) | 10 seri | 2015 → 2026-10 | D09 | hazır; HY spread, 2y / 3m faiz, DXY, VIX yok (FRED / Yahoo ücretsiz; VIX / DXY kapalı konu) |
| SEC finansal tablolar | secfs/fs_2021q1..2026q3.csv.gz (islenmis-veri) | 10-K / 10-Q kalemleri | 2021-01 → 2026-09 | D07, D08 (pay, geri alım) | hazır; 2021 öncesi YOK → D07 keşif dönemi 2021-23, doğrulama 2024-26 (n küçük riski) |
| Nakit / OCF / pist özeti | k31_fin.pkl, k34_bildirim.pkl | 5.743 sembol | 2021 → 2026-09 | D07 | hazır (K31 / K34'te kullanıldı) |
| Form 4 açık piyasa alımları | k30_alim.pkl | 994 sembol | 2022-01 → 2026-03 | D08 | hazır; satışlar ve 2022 öncesi YOK (fi_k30_indir ile yeniden iner, e-posta UA) |
| SEC başvuru geçmişi özeti | k54 sec_ozet.json (form, tarih, 8-K maddeleri, eski adlar) | 3.262 CIK, 2001 → 2026 | tüm | D08 (S-1, 424B, S-3, 8-K 2.03 / 3.02 / 5.02), D07 zamanlama | **yalnız oturum geçici alanında (105 MB)**; repoya islenmis-veri dalına konması Cemal'in izniyle (karar 8.3) |
| Analist not günlüğü | analist/yahoo_grades.pkl | Yahoo kapsamı (hayatta kalanlar) | 2016 → 2026 | D07-S06 (yalnız kıyas) | hazır; K52 / K53'te denendi |
| Bilanço sürprizi | k28_X_abd.pkl | ABD takvimi | 2022-12 → 2026-10 | D07 kıyas | hazır; Ç100 / Ç118'de denendi |
| 13F kurumsal sahiplik | yok | — | — | D08-S03 | VERİ GEREK: SEC 13F toplu (ücretsiz, ~GB, çeyreklik, 45 gün gecikme) |
| Açığa satış / short interest | finra_si (kısmi, oturum alanı) | ? | 2023+ | D08 ek | kapsam denetlenecek; FINRA ücretsiz |
| Gün içi / emir akışı | yok (k40 yalnız endeks saatlik, 2023-11+) | — | — | D05 | YOK; D05 yalnız OHLCV vekilleriyle, açıkça işaretli |

Kalite denetimi (koşudan önce, `veri_kalitesi.py`): sembol başına boşluk / sıfır hacim / bölünme sıçraması taraması (K51 v1.2 V1-V8 yeniden), SEC tablolarında bildirim tarihi (filed) kullanımı (dönem sonu değil), Form 4 ve 13F'te yayın gecikmesi, K54 sınıf ve kesim tarihleri, fon krizi kesimi, evren dışı listesi. Çıktı: `K55_VERI_KAPSAMI.md` (dal başına kapsam, eksik payı, dönem).

## 4. On ana dal ve 100 hücre

Sütunlar: kimlik | soru | değişken (tanım; hepsi t gününe kadar) | veri | yöntem | not. Yöntem: A olay öncesi, B eşleşmiş ileri, C değişim noktası. Not: YENİ = daha önce ölçülmedi; ESKİ Çxx = o çalışmada ölçüldü (yeniden koşulmaz, kıyas); KAPALI = COL_OZET kapalı konu (onay gerekir); VEKİL = gerçek veri yok, OHLCV vekili.

### D01 — Fiyat davranışı (OHLCV; maliyet düşük; 10 hücre, 10 × 5 pencere × 3 olay = 150 varyant)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D01-S01 | Dip ne kadar sürede oluştu? | 250 günlük dibin ±%3 bandında geçirilen gün sayısı ve dipten bu yana gün | OHLCV | A B C | YENİ (K51 çekirdeği süreyi ölçmedi) |
| D01-S02 | Düşüş hızı değişiyor mu? | log fiyat 20 gün eğimi − 60 gün eğimi (ivme), düşüşün yavaşlaması | OHLCV | A B C | YENİ |
| D01-S03 | Dip kaç kez test edilip savunuldu? | 120 günde dibin ±%2'sine inip altında kapanmayan gün sayısı | OHLCV | A B | YENİ |
| D01-S04 | Alt fitiller büyüyor mu? | 20 gün toplam alt fitil / toplam üst fitil | OHLCV | A B C | YENİ (K7 küçük alım mumu farklı: tek mum) |
| D01-S05 | Getiri asimetrisi | 60 gün getiri çarpıklığı; yukarı gün ortalama getirisi / aşağı gün ortalama getirisi | OHLCV | A B | YENİ |
| D01-S06 | Dar alanda kalma süresi | 20 gün aralığı (H−L)/C'nin 250 gün en düşük %10'unda ardışık gün sayısı | OHLCV | A B C | KISMEN ESKİ: K51 imza ölçü, burada SÜRE; vekil denetimi şart |
| D01-S07 | Mum dizisinin sırası | 10 gün kapanış yön dizisinin entropisi ve en uzun aynı yön serisi | OHLCV | A B | YENİ |
| D01-S08 | Önceki sert düşüşe tepki | 20 gündeki en büyük düşüş gününden sonraki 5 günde geri alınan pay | OHLCV | A B | YENİ |
| D01-S09 | Direnç aşınması | 60 gün tepesine uzaklık ve tepeye %3 yaklaşıp geri çekilme sayısı | OHLCV | A B | YENİ |
| D01-S10 | Hisse kendi normalinden saptı mı? | son 20 gün getiri dağılımının önceki 120 güne KS uzaklığı | OHLCV | A C | YENİ (anomali) |

### D02 — Hacim ve işlem akışı (OHLCV; maliyet düşük)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D02-S01 | Hacim fiyattan önce mi değişiyor? | hacim20 / hacim120 değişimi, |r20| < %3 koşuluyla | OHLCV | A B C | YENİ |
| D02-S02 | Düşüş günleri hacmi payı | 20 gün toplam hacimde aşağı günlerin payı | OHLCV | A B | YENİ (OBV / CMF ile vekil denetimi) |
| D02-S03 | Aynı hacme fiyat tepkisi değişiyor mu? | |r| / işlem değeri (Amihud) 20 gün / 120 gün oranı | OHLCV | A B C | bilinen ölçü (Amihud), değişimi YENİ |
| D02-S04 | Yukarı / aşağı gün hacim farkı | medyan hacim(yukarı) / medyan hacim(aşağı) 40 gün | OHLCV | A B | YENİ |
| D02-S05 | Hacim zamana nasıl yayılmış? | 60 gün hacim Gini katsayısı | OHLCV | A B | YENİ |
| D02-S06 | Olağan dışı hacimler kümeleniyor mu? | hacim > 2 × medyan günleri arası gün sayısı, ardışıklık | OHLCV | A B | YENİ |
| D02-S07 | Hacim artıyor fiyat ilerlemiyor (emilim) | hacim20 z-skoru > 1 VE |r20| < %3 | OHLCV | A B | YENİ |
| D02-S08 | Hacim azalıyor fiyat düşmüyor (satıcı tükenmesi) | hacim20 z < −1 VE r20 ≥ 0 | OHLCV | A B | KISMEN ESKİ: K51 H-C hacim kuruması; koşullu biçimi YENİ |
| D02-S09 | Hacim–oynaklık bağı | 60 gün korelasyon(|r|, hacim) ve 120 güne göre değişimi | OHLCV | A B C | YENİ |
| D02-S10 | Evren içinde ilgi artıyor mu? | günlük işlem değeri evren yüzdeliğinin 60 gün değişimi | OHLCV | A B | YENİ |

### D03 — Volatilite ve risk rejimi (OHLCV)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D03-S01 | Kısa vol uzun vole göre nerede? | vol20 / vol250 ve bu oranın 250 gün yüzdeliği | OHLCV | A B C | KISMEN ESKİ: vol60 K51 kontrolü; oran YENİ; BB daralması KAPALI (BB kullanılmaz) |
| D03-S02 | Aşağı vol mü yukarı vol mü? | 60 gün aşağı yarı-varyans / yukarı yarı-varyans | OHLCV | A B | YENİ |
| D03-S03 | Vol kümelenmesi | |r| 1. gecikme otokorelasyonu 60 gün | OHLCV | A B | YENİ |
| D03-S04 | Daralma ne hızda? | vol20'nin 60 gün içinde en düşük yüzdeliğe iniş süresi | OHLCV | A B | YENİ |
| D03-S05 | Vol artışı fiyattan önce mi? | aralık (H−L) değişimi ile |r| arasındaki öncü-gecikme (±5 gün çapraz korelasyon) | OHLCV | A C | YENİ |
| D03-S06 | Hareket verimliliği | ATR20 toplamı / |20 gün net hareket| | OHLCV | A B | YENİ (Kaufman verimlilik oranına benzer; vekil denetimi) |
| D03-S07 | Beklenen vs gerçekleşen vol | hisse bazlı opsiyon IV YOK; vekil: piyasa VIX × beta − gerçekleşen | — | — | VERİ YOK + KAPALI (VIX); koşulmaz, onayla açılır |
| D03-S08 | Boşluk volatilitesi | 20 günde açılış boşluklarının toplam varyansa katkısı | OHLCV | A B | YENİ |
| D03-S09 | Uzun düşük vol sonrası ilk sıçrama yönü | vol250 yüzdeliği < 10 ve ≥ 60 gün sürmüş; sonraki ilk > 2σ günün yönü | OHLCV | A B | YENİ |
| D03-S10 | Aşağı vol zamanla azalıyor mu? | aşağı yarı-varyans 60 gün / 120 gün oranı | OHLCV | A B C | YENİ |

### D04 — Zaman ve süre davranışı (OHLCV)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D04-S01 | Düşüş süresi / dipte kalma süresi | 250 gün tepesinden dibe gün sayısı / dipten bugüne gün sayısı | OHLCV | A B | YENİ |
| D04-S02 | Hisse geçmişte ne hızda toparlandı? | önceki ≥ %20 düşüşlerden %50 geri alma süreleri medyanı | OHLCV | A B | YENİ |
| D04-S03 | Dip testleri sıklaşıyor mu? | ardışık dip testleri arası gün sayısının eğilimi | OHLCV | A B | YENİ |
| D04-S04 | Büyük hareketler arası boşluk | |r| > 2σ günleri arası süre dağılımı (ortalama, son boşluk) | OHLCV | A B | YENİ |
| D04-S05 | Önce hacim mi fiyat mı? | 60 günde ilk hacim olayı (> 2 × medyan) ile ilk fiyat olayı (> 2σ) arasındaki işaretli gün farkı | OHLCV | A | YENİ |
| D04-S06 | Kanalda bekleme süresi | fiyatın 20 gün kanalı içinde kalma süresi; hazard oranı (süre uzadıkça çıkış olasılığı) | OHLCV | A B | YENİ (sağkalım analizi) |
| D04-S07 | Takvim | haftanın günü, ay içi hafta, çeyrek sonu | OHLCV | A | bilgi; düşük öncelik; tek başına iz sayılmaz |
| D04-S08 | Uzun hareketsizlik sonrası hareket olasılığı | |r20| < %5 ve aralık düşük hâlinin süresi → sonraki 20 gün |hareket| | OHLCV | A B | YENİ |
| D04-S09 | Değişimlerin sırası | hacim, aralık, fiyat serilerinde CUSUM değişim tarihleri sırası (ör. hacim → vol → fiyat) | OHLCV | C | YENİ (D10-S06 ile birlikte) |
| D04-S10 | Olaylar takvimde kümeleniyor mu? | Y60 / Y120 olaylarının yıl-ay dağılımı, taban ayarı | OHLCV | A | bilgi; taban düzeltmesi için |

### D05 — Piyasa mikro yapısı (yalnız günlük OHLCV; emir akışı YOK, hepsi VEKİL olarak işaretli)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D05-S01 | Kapanış gün içi nerede? | (C−L)/(H−L) 20 gün ortalaması | OHLCV | A B C | YENİ |
| D05-S02 | Gövde yönü ve payı | (C−O)/(H−L) 20 gün ortalaması | OHLCV | A B | YENİ |
| D05-S03 | Gün içi aralık | (H−L)/C 20 gün / 120 gün | OHLCV | A B | KISMEN ESKİ (K51 imza aralık tabanlı); oran YENİ |
| D05-S04 | Kapanışa doğru davranış | gün içi veri YOK; vekil: C > (H+L)/2 günlerin payı | OHLCV | A B | VEKİL |
| D05-S05 | Boşluklar | 20 günde açılış boşluğu sayısı / yönü, kapanan boşluk payı | OHLCV | A B | YENİ |
| D05-S06 | Bir dolar hacim fiyatı ne kadar oynatıyor? | 60 gün |r| / log işlem değeri regresyon eğimi (Kyle λ vekili), eşlere göre | OHLCV | A B | VEKİL; D02-S03 ile korelasyon denetimi |
| D05-S07 | Yüksek hacimli güne ertesi gün tepki | hacim > 2 × medyan günlerinden sonraki 3 gün devam / geri dönüş oranı | OHLCV | A B | YENİ |
| D05-S08 | Alış–satış dengesizliği | işaretli hacim vekili: hacim × işaret(C−O) 20 gün toplamı / toplam hacim | OHLCV | A B | VEKİL (tick verisi yok; OBV ile vekil denetimi) |
| D05-S09 | Düşük fiyat etkisi | fiyat < 5 $ ve lot etkisi; kontrol değişkeni | OHLCV | B | kontrol; tek başına iz değil |
| D05-S10 | Gün içi tersine dönüş | açılış yönü ≠ kapanış yönü günlerin 20 gün payı | OHLCV | A B | YENİ |

### D06 — Göreli güç ve piyasa içindeki konum (OHLCV + endeks + sektör)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D06-S01 | Göreli güç ivmesi | (hisse − SPY) 20 gün getirisi − aynı farkın 60 gün getirisi | OHLCV, SPY | A B C | bilinen etki (momentum, Ç121) ile kıyas zorunlu; kısa ivme YENİ |
| D06-S02 | Piyasa düşerken direnç | SPY < −%1 günlerinde hissenin ortalama getirisi (60 gün) | OHLCV, SPY | A B | YENİ |
| D06-S03 | Sektörden ayrışma | hisse − sektör sepeti 20 gün getirisi | OHLCV, sektör | A B | KISMEN ESKİ (Ç117 sektör rüzgârı sektör düzeyinde); hisse ayrışması YENİ |
| D06-S04 | Sektör içi sıra değişimi | 60 gün getirisi sektör içi yüzdeliğinin 20 gündeki değişimi | OHLCV, sektör | A B | YENİ |
| D06-S05 | Endeksten önce dip | hissenin 60 gün dip tarihi − SPY dip tarihi (gün) | OHLCV, SPY | A | YENİ |
| D06-S06 | Göreli güç değişim noktası | RS serisinde CUSUM değişim tarihi, olaya gecikmesi | OHLCV, SPY | C | YENİ |
| D06-S07 | Düşüşte sınırlı kayıp | aşağı beta (SPY < 0 günleri) 120 gün | OHLCV, SPY | A B | YENİ |
| D06-S08 | Yükselişte güçlenen tepki | yukarı beta − aşağı beta | OHLCV, SPY | A B | YENİ |
| D06-S09 | Küçüklere göre konum | IWM'ye göre 20 / 60 gün göreli getiri | OHLCV, IWM | A B | YENİ |
| D06-S10 | Korelasyon kopuşu | hisse–SPY 60 gün korelasyonu − 250 gün korelasyonu | OHLCV, SPY | A B C | YENİ |

### D07 — Şirket ve temel veriler (SEC FS 2021q1-2026q3; yalnız bildirim tarihinden sonra bilinir; keşif 2021-23, bağımsız 2024-26)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D07-S01 | Satış büyümesi değişimi | yıllık satış büyümesi (son 4 çeyrek) ve çeyreklik ivme | secfs | A B | YENİ (ABD); n sınırlı |
| D07-S02 | Kârlılık değişimi | faaliyet marjı son çeyrek − önceki 4 çeyrek ortalaması | secfs | A B | YENİ |
| D07-S03 | Nakit akışı işareti | OCF negatiften pozitife dönüş (son 2 çeyrek) | k31_fin, secfs | A B | KISMEN ESKİ (Ç106 nakit tükenmesi grubu); işaret dönüşü YENİ |
| D07-S04 | Borçluluk | toplam borç / varlık değişimi (2 çeyrek) | secfs | A B | YENİ |
| D07-S05 | Brüt marj ivmesi | brüt marj 2 çeyrek değişimi | secfs | A B | YENİ |
| D07-S06 | Faaliyet kaldıracı | satış değişimi − faaliyet gideri değişimi | secfs | A B | YENİ |
| D07-S07 | Şirket − sektör farkı | şirket satış büyümesi − sektör (SIC 2 hane) medyanı | secfs, k35 | A B | YENİ |
| D07-S08 | Temel mi fiyat mı önce? | iyileşme bildirimi öncesi 20 gün fiyat tepkisi; bildirim sonrası 60 gün | secfs, OHLCV | A | YENİ (bilanço sürprizi Ç100 / Ç118 kıyas) |
| D07-S09 | Tahakkuk kalitesi | (net kâr − OCF) / varlık | secfs | A B | YENİ |
| D07-S10 | Yatırım harcaması değişimi | capex / satış 2 çeyrek değişimi | secfs | A B | YENİ |

### D08 — Sahiplik, sermaye ve kurumsal hareketler (SEC başvuruları; kapsam ve yayın tarihi denetimi zorunlu; eksik kayıt sıfır değil)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D08-S01 | İçeriden alım kümelenmesi | 30 günde farklı yöneticilerden alım sayısı, toplam tutar / piyasa değeri | k30_alim (2022-01+) | A B | KISMEN ESKİ (Ç102 K30 tek alım); kümelenme YENİ; 2022 öncesi YOK |
| D08-S02 | İçeriden satış yoğunluğu | Form 4 satış tutarı / sahiplik | Form 4 satışlar | A B | VERİ GEREK (fi_k30_indir satış dahil yeniden indirme, e-posta UA) |
| D08-S03 | Kurumsal sahiplik değişimi | 13F toplam kurumsal pay değişimi (45 gün gecikmeli) | 13F | A B | VERİ GEREK (SEC toplu 13F; büyük indirme, karar 8.4) |
| D08-S04 | Seyrelme | hisse sayısı 4 çeyrek değişimi (dei pay) | secfs, k31 pay | A B | KISMEN ESKİ (Ç103 seyrelme); eşli ölçüt ile YENİ |
| D08-S05 | Sermaye artırımı bildirimi | S-3 / 424B / 8-K 3.02 başvuru tarihi, son 120 gün | sec_ozet (k54) | A B | YENİ; sec_ozet repoya konmalı (karar 8.3) |
| D08-S06 | Kilit açılma | S-1 / 424B4 tarihi + 180 gün penceresi | sec_ozet | A B | YENİ |
| D08-S07 | Halka arz yaşı | ilk S-1 / 424B4'ten bu yana gün; genç halka arz davranışı | sec_ozet | A B | KISMEN ESKİ (BIST genç halka arz açık madde); ABD YENİ |
| D08-S08 | Geri alım | secfs 'PaymentsForRepurchaseOfCommonStock' / piyasa değeri | secfs | A B | YENİ (BIST B1 geri alım Ç26 farklı pazar) |
| D08-S09 | Sermaye yapısı değişimi | 8-K madde 2.03 (borç) / 3.02 (hisse) / 1.01 sözleşme sıklığı | sec_ozet | A B | YENİ |
| D08-S10 | Haber yoğunluğu | 60 günde 8-K sayısı ve madde çeşitliliği | sec_ozet | A B | YENİ |

### D09 — Sektör, makro ve dış etkenler (k36 sürücüler + endeks; KAPALI konu uyarısı: tek başına makro sinyal Ç05'te 'tutarsız' bulundu; burada yalnız KOŞUL / etkileşim olarak)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D09-S01 | Faiz ortamı koşulu | ^TNX 60 gün değişimi; hissenin faiz duyarlılığı (beta) | k36 | B (koşul) | KAPALI (US10Y tek başına); koşul olarak onayla |
| D09-S02 | Dolar / likidite koşulu | DXY YOK; EURUSD, USDTRY var | k36, Yahoo | B (koşul) | KAPALI (DXY); onayla; DXY ücretsiz indirilebilir |
| D09-S03 | Sektör döngüsü | sektör sepeti 120 gün momentumu ve dönüş noktası | OHLCV, sektör | B | ESKİ Ç117 / Ç108-111 (rüzgâr); yeniden koşulmaz, koşul olarak |
| D09-S04 | Emtia → hisse gecikmesi | sektörün emtiası (altın, petrol, bakır, çelik, buğday, gaz) değişim noktası → sektör hisseleri değişim noktası gecikmesi | k36 | C | KISMEN ESKİ (Ç110 rüzgârın sebebi); gecikme YENİ |
| D09-S05 | Sektörler arası para geçişi | 11 sektör sepeti göreli getiri sıralamasının 20 gün değişimi; lider değişimi | OHLCV, sektör | A B | YENİ |
| D09-S06 | Endeks rejimi koşulu | SPY 200 gün üstü / altı; hücre etkileri rejime göre ayrı | SPY | koşul | K51 kontrolü; koşul |
| D09-S07 | Stres sonrası | SPY 20 gün düşüşü > %10 dönemlerinde düşük aşağı betalı hisselerin sonraki 60 günü | SPY, OHLCV | A B | YENİ |
| D09-S08 | Makro değişim noktası → hisse | faiz / emtia CUSUM tarihleri ile hisse değişim noktaları gecikmesi | k36, OHLCV | C | YENİ |
| D09-S09 | Kredi riski koşulu | HY spread (FRED) değişimi; CDS (TR) ABD için uygun değil | FRED | B (koşul) | VERİ GEREK (ücretsiz); KAPALI'ya yakın, onayla |
| D09-S10 | Aynı şoka farklı tepki | büyük SPY günlerinde hisse tepkilerinin dağılımı ve hissenin konumu (dispersion) | SPY, OHLCV | A B | YENİ |

### D10 — Değişkenlerin birlikte davranışı (D01-D09 değişkenlerinden; sıra, gecikme, koşullu etki; korelasyon değil)

| Kimlik | Soru | Değişken | Veri | Yöntem | Not |
|---|---|---|---|---|---|
| D10-S01 | Fiyat düşerken hacim farklı | r20 < 0 VE aşağı gün hacim payı düşük (D02-S02 alt beşte bir) | OHLCV | A B | YENİ |
| D10-S02 | Vol düşerken göreli güç yükseliyor | D03-S01 alt beşte bir VE D06-S01 üst beşte bir | OHLCV, SPY | A B | YENİ |
| D10-S03 | Piyasa düşerken hisse yatay | D06-S02 üst beşte bir VE D01-S06 dar alan | OHLCV, SPY | A B | YENİ |
| D10-S04 | Uzun hareketsizlik + hacim yapısı değişimi | D04-S08 süresi uzun VE D02-S05 Gini değişimi | OHLCV | A B | YENİ |
| D10-S05 | Temel iyileşiyor fiyat tepkisiz | D07-S02 / S03 iyileşme VE 20 gün fiyat tepkisi < %3 | secfs, OHLCV | A B | YENİ; 2021+ |
| D10-S06 | Değişim sırası | D04-S09 sıralarından belirli dizi (hacim → vol → fiyat) olay öncesinde daha sık mı | OHLCV | C | YENİ |
| D10-S07 | İçeriden alım + dar alan + sektör | D08-S01 VE D01-S06 VE D09-S03 | k30, OHLCV | A B | KISMEN ESKİ (Ç99 / Ç102 çölde içeriden alım); üçlü YENİ, 2022+ |
| D10-S08 | Koşullu etki | her D01-D06 hücresi × (likidite üçlüsü, büyüklük, fiyat < 5 $) etkileşimi | OHLCV | B | YENİ; dallanma şablonunun bir parçası |
| D10-S09 | Lider–takipçi gecikmesi | sektör liderinin (işlem değeri üst üçte bir) 20 gün getirisi → hissenin sonraki 20 günü | OHLCV, sektör | A B | KISMEN ESKİ (Ç111 büyükler önce); hisse düzeyinde gecikme YENİ |
| D10-S10 | Çok değişkenli sapma | D01-D06 değişken vektörünün hissenin 250 gün geçmişine Mahalanobis uzaklığı | OHLCV | A C | YENİ (makine öğrenmesi değil, anomali) |

## 5. Dallanma şablonu (KEŞİF olan hücre için 10 alt hücre; sabit, hücreye göre uyarlanır)

A düşüş günleri / B yatay / C yükseliş günleri (olay öncesi 20 gün rejimi); D düşük vol / E yüksek vol (vol250 yüzdeliği); F küçük / G büyük (işlem değeri üçlüsü); H endekse göre güçlü / I zayıf (D06-S01 işareti); J zaman ölçeği (pencere 5 / 10 / 20 / 40 / 60 ve haftalık). Her alt hücre ana bulgunun nedenini sorar; yalnız keşif döneminde; FDR aile = ana hücre.

## 6. Çalışma sırası, modüller, maliyet

| Faz | İçerik | Girdi | Hesap | Geliştirme |
|---|---|---|---|---|
| 0 | Arşiv (commit 83e5de8, yapıldı) + `veri_kalitesi.py` + ortak panel (`evren.py`, `olay_tanimlari.py`) + sentetik birim testleri + 50 hisselik gerçek deneme | mevcut veri | 10 dk | 1 oturum |
| 1 | D01-D06 + D10 OHLCV hücreleri (80 hücre; 150 varyant / dal) | OHLCV, endeks, sektör | hücre 1-4 dk (3,2 M satır panel, 2.000 bootstrap) → 3-5 saat | 3-4 oturum (dal başına modül + test) |
| 2 | D07, D08 (SEC) | secfs, k31, k30, sec_ozet | 1-2 saat | 2 oturum + veri indirme (Form 4 satış ~2 saat, 13F ~GB) |
| 3 | D09 (makro koşullar; onaylı hücreler) | k36, FRED / Yahoo | 1 saat | 1 oturum |
| 4 | Dallanma (KEŞİF hücreleri × 10), iç doğrulama, bağımsız dönem (bir kez), AVR çoğaltma, rapor | — | adaya göre | 2 oturum |

Modüller (her biri bağımsız, ortak panel bir kez): evren.py, veri_kalitesi.py, olay_tanimlari.py, dal01_fiyat.py … dal10_birlesik.py, dallanma_motoru.py, istatistik.py (bootstrap, FDR, Holm, DSR), ileri_dogrulama.py, raporlama.py. Çakışma kapısı her modülde. Her koşu: koşu kimliği (tarih + commit + veri sürümü sha256), `K55_HUCRE_SONUC.csv`, `K55_VARYANTLAR.csv` (başarısızlar dahil), `K55_ADAYLAR.md` (KEŞİF / DERİNLEŞTİR / DOĞRULAMA BEKLİYOR), `K55_VERI_KAPSAMI.md`, `K55_COKLU_TEST.csv`, `K55_RAPOR.md`.

Not: CLAUDE.md "tek dosya" kuralı ile talimattaki modüler yapı çelişir; öneri: `K55/` klasöründe modüller + tek giriş `K55.py` (Colab'da tek exec), testi `test_k55.py`. Karar 8.1.

## 7. Eski çalışmalarla çakışmalar ve kapalı konular (dürüst liste)

- Yeniden koşulmayan, yalnız kıyas: D09-S03 (sektör rüzgârı Ç117), D09-S04 kısmen (Ç110), D07-S03 kısmen (Ç106), D08-S01 kısmen (Ç102), D08-S04 kısmen (Ç103), D10-S07 kısmen (Ç99 / Ç102), D06-S01 (momentum Ç121 kıyası), D01-S06 / D05-S03 (K51 imza), D02-S08 (K51 H-C). Bu hücrelerde yalnız YENİ olan boyut (süre, koşul, gecikme, kümelenme) ölçülür.
- Kapalı konular (COL_OZET): VIX / DXY / US10Y tek başına (D03-S07, D09-S01, S02, S09), hacim onayı ve giriş zamanlaması (bu planda yok), BB daralması (kullanılmaz), 90+ şekil ölçüsü (şekil adı yok), KNN (yok), stop (bölüm 2.9). Kapalı hücreler yalnız koşul / etkileşim olarak ve Cemal onayıyla açılır.
- K48 / K49 / K50 geniş makine ölçüleri (204 ölçü) ile örtüşme: 2.7 korelasyon denetimi; K48 ilk 3 bileşeni kıyas listesinde.

## 8. Karar gereken maddeler (onay için)

1. Kod yapısı: `K55/` klasöründe modüller + tek giriş `K55.py` (öneri) mi, yoksa CLAUDE.md'ye uygun tek dosya mı?
2. Dönem kilidi: keşif 2016-21, iç doğrulama 2022-23, bağımsız 2024-26 (bir kez açılır) — onay. Alternatif: bağımsız = 2025-01 → 2026-06.
3. SEC başvuru özeti (sec_ozet.json, 105 MB) ve Tiingo sembol listesi islenmis-veri dalına konsun mu? (Yoksa her oturumda e-posta UA ile yeniden iner, ~1 saat.)
4. 13F kurumsal sahiplik toplu indirme (ücretsiz, büyük) ve Form 4 satışlarının indirilmesi: Faz 2 için izin.
5. Kapalı konu hücreleri (D03-S07, D09-S01, S02, S09): koşul olarak açılsın mı, kapalı mı kalsın? Öneri: kapalı kalsın; D09-S06 rejim ve D09-S05 rotasyon yeter.
6. Olay tanımları (Y60 +%30, Y120 +%50, Y250 +%100) ve ölçütler (bölüm 2.5) — onayla kilitlenir; sonra değişmez.

Onay gelince: Faz 0 (veri kalitesi + ortak panel + testler + 50 hisselik deneme) tek oturumda; sonra Faz 1 dal dal, her dal sonunda karşılaştırmalı rapor.
