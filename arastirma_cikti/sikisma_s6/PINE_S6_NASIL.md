# COL S6 Taban — TradingView'e ekleme ve okuma (v1.1, 16 Kasım 2026; v1.0: 15 Kasım)

**v1.1'de yeni (S7 fikirleri):** (1) küçük mum ölçüsünün ATR% referansı artık pencereden ÖNCEKİ 250 mum (tabanın kendi küçük mumları referansı küçültmez);
(2) Bollinger daralması şartı: BB(20, 2σ) genişliği son 250 günün en dar %30'unda değilse taban yok; (3) **mor elmas** = kutunun ilk bilindiği gün
(ONAY); kutunun ondan önceki kısmı **kesik kenarlı soluk** (o günlerde bilinmiyordu, sonradan geriye uzatıldı), sonrası dolu; (4) **SÖNME**: taban bir gün
kaybolursa ve AL / KIRILDI yoksa kutu kenarı griye döner, mumun üstünde küçük gri **'sonme'** etiketi çıkar (aynı taban dönerse etiket silinir, kutu sürer);
(5) kutunun altında ilk .. son mum tarihi. Eski davranış için (4) referans ve (6) BB girdilerini kapat (v1.0 kipi: eski sonuçlarla birebir).

Dosya: `arastirma_cikti/sikisma_s6/COL_S6_TABAN.pine` (Türkçe yazılar). Türkçe karakterde sorun çıkarsa aynı kodun ASCII kopyası:
`COL_S6_TABAN_ascii.pine` (yalnız yorum ve yazılardaki harfler değişik; kod birebir aynı, `python S6_TABAN.py ascii` doğrular).
Python karşılığı `S6_TABAN.py`; tanım ve eşikler iki yerde aynıdır. Bu bir göz aracıdır: getiri ya da iz iddiası yoktur.

## Ekleme
1. TradingView'de günlük grafiği aç (sembol `BIST:...`). Grafiğin sağ altındaki **ADJ** (temettü / bölünme düzeltmesi) AÇIK olsun: Python düzeltilmiş fiyatla çalışır.
2. Alttaki **Pine Düzenleyici**'yi aç, **Yeni → Boş gösterge**, içindekini sil, dosyanın tamamını yapıştır, **Kaydet**, **Grafiğe ekle**.
3. Basic planda grafikte en çok 2 gösterge durur: S5 ile birlikte S6 sığar; başka bir gösterge açıksa birini kaldır.
4. Derleyici bizde yok: hata çıkarsa ekrandaki satır numarası ve iletiyi aynen yaz (ASCII kopyada da aynı satır numaraları geçerlidir).

## Ne çizer
- **Kutu** = taban bölgesi. Sol kenar tabanın ilk mumu, sağ kenar son mumu; üst / alt = tabanın tavan / dip çizgileri. Kesik kenarlı soluk kısım: mor elmastan
  (onay günü) önceki mumlar, yani kutu sonradan geriye uzatılmış kısım; dolu kısım onay gününden sonrası. Karar için dolu kısma bak. Renk açılış günündeki sınıf: **mavi DİP** (120 günlük aralığın alt çeyreği, tepeden en az %10 aşağı), **turuncu YOL** (fiyat yükselen SMA50 üstünde), **gri ORTA**. Kutunun sol üstünde uzunluk (bar).
- **Yeşil yatay çizgi** = tavan: tabanın en yüksek High'ı (tavan mumu), kutunun sağ kenarına kadar.
- **Yeşil üçgen "AL"** = önceki gün taban vardı ve bugün KAPANIŞ tavanın üstünde. Kutu o mumda kapanır, kenarı yeşil olur. AL'dan sonraki yeni kutu en az 8 mum dolunca çizilir; o arada (ya da art arda ikinci günde) gelen üçgen kutusuz olabilir.
- **Kırmızı x "KIRILDI"** = önceki gün taban vardı ve bugün kapanış dibin %2 altında. Kutu kırmızı kenarla kapanır.
- Taban bir gün kaybolursa kutu o gün durur: kenar gri, mumun üstünde gri 'sonme' etiketi ("söndü"). Ertesi günlerde aynı taban dönerse etiket silinir, kenar eski rengine döner, aynı kutu uzar.
- **Mor elmas** (mumun altında) = onay günü: kutu ilk bu gün en az 8 mumla çizilebildi. Elmastan önceki kutu kısmı o gün bilinmiyordu.
- Kutunun altındaki gri küçük yazı = kutunun ilk ve son mumunun tarihi (Görünüm grubundan kapatılabilir).
- Kutu sağa doğru büyür; sol kenarı da taban geriye doğru büyüdükçe sola kayabilir (eski mumlar tabana katılınca). Kararı kutunun SAĞ kenarı verir; sol kenar sonradan belli olur.

## Tablo (sağ üst, son mum için)
n (taban uzunluğu), pencere başlangıcı, tavan / dip, (1) bant, (2) net değişim (son / ilk kapanış), (3) dip savunması (ikinci yarı dibi / ilk yarı dibi - 1), (4) medyan mum / ATR% (v1.1: pencere öncesi referans), (5) daralma oranı (şart kapalıysa bilgi), sınıf (bugün / bölge açılışı), durum (AÇIK / AL / KIRILDI / söndü ve tarihi), son bölge (tarih aralığı, bar), son AL mumunun boyu ve hacmi (önceki 20 günün ortalamasının kaç katı), geçerli bar sayısı, ATR% (son 250), onay günü (son bölge), (6) BB yüzdeliği (bugün; şart açıksa eşik yazılı).

## Ayarlar (varsayılanlar = tasarım sınamasının seçtiği değerler; S6_TASARIM.md)
| girdi | varsayılan | anlamı |
|---|---|---|
| nMin / nMax | 8 / 70 | en kısa taban ve en uzun pencere (geçerli mum) |
| (1) Bant | 0,12 | en yüksek High / en düşük Low - 1 en çok %12 |
| (2) Sakin | 0,03 | son kapanış / pencerenin ilk kapanışı - 1, mutlak en çok %3 |
| (3) Dip toleransı | 0,05 | ikinci yarının dibi ilk yarının dibinin en çok %5 altında |
| (4) Küçük mum kM | 0,90 | medyan mum boyu (fitil dahil, H-L / C) <= 0,90 x ATR% (250 gün) |
| (5) Daralma | 0 (kapalı) | 0'dan büyükse: pencerenin ortalama mumu <= oran x önceki 60 günün ortalaması |
| (4) ATR% referansı pencereden önce | açık | v1.1: referans = pencereden önceki 250 mum (en az 120); kapalı = v1.0 (son 250 mum, pencere dahil) |
| (6) Bollinger daralması | açık, 0,30 | v1.1: BB(20, 2σ) genişliği, önceki 250 günün genişliklerine göre yüzdeliği <= 0,30 (en dar %30); kapalı = v1.0 |
| Kırılım toleransı | 0,02 | kapanış < dip x 0,98 ise KIRILDI |
| ATR% günü / daralma günü / konum / SMA / SMA eğimi / hacim | 250 / 60 / 120 / 50 / 20 / 20 | Python ile aynı kalması için değiştirme |
Renkler ve tablo "Görünüm" grubundadır. Eşikleri değiştirirsen grafik Python listesiyle (`python S6_TABAN.py liste SEMBOL BAS SON`) artık aynı olmaz.

## Bilinen farklar (Python listesiyle karşılaştırırken)
- **Likidite süzgeci yok**: Python'daki ölçüm işlerinde olan likidite alt %20 süzgeci göstergede yok (tasarım sayımında da yok).
- **TradingView verisi**: Python V_BIST (Yahoo, düzeltilmiş). Barlar eksik / fazla ya da düzeltme farklı olabilir; o zaman bölge tarihleri bir iki gün kayar. Hacmi 0 olan ya da High = Low olan mum ikisinde de atlanır.
- **Geçmiş uzunluğu**: gösterge ilk 250 geçerli mumu yalnız ATR için kullanır, tabanı 251. mumdan sonra arar. TradingView daha kısa geçmiş yüklerse ilk bölgeler farklı başlar; birkaç ay sonra aynı olur.
- **Kriz kesiği yok**: Python verisi 31.08.2026'da kesilir (fon krizi); gösterge sonrasını da çizer.
- **Eşitlik sınırı**: bir şart tam sınırdaysa (ör. bant tam %12,000) Python ile Pine'ın toplama sırası farkı en son ondalıkta ayrışabilir; pratikte görülmez.
- Dosyanın sonunda 6 etiket için BEKLENEN kutular yazılıdır (V_BIST ile); grafikte farklı görürsen önce günlük grafik / ADJ / varsayılan girdileri denetle.

## Okurken dikkat (tasarım sınamasından)
- AL üçgeni, önceki günün taban penceresindeki en yüksek High'ın kapanışla aşıldığı gündür. Tasarım sınamasında PAPIL 11 Ara 2025 ve TUCLK 22 Ağu 2025 al mumları tuttu; TUCLK'ta bundan önce 6 Ağu'da erken bir üçgen daha var (fiyat tabana döndü, yeni kutu açıldı). KNFRT 14 Eyl 2022'de üçgen yok. Ayrıntı S6_TASARIM.md.
- PAPIL büyük taban (Eki 2025 - Mar 2026) bant %12 ile tek bölge olmaz (bilgi etiketi); tavan kırılımı tek başına alım nedeni değildir (K6b uyarısı).
- Kutular sık çıkar: v1.0'da BIST'te hisse başına yılda ~6,9 bölge, günlerin ~%30'unda açık bir kutu vardı; v1.1'de (BB şartıyla) ~4,2 bölge ve ~%18. Hâlâ nadir değil. Kutu "aday"dır; Cemal'in gözü ve sektör rüzgârı olmadan çöl sayılmaz.

## v1.1 alınmayanlar (S7 metninden)
- ±%1 kırılım payı: S6'da AL = kapanış > tavan (pay yok), KIRILDI = kapanış < dip x 0,98 kalır.
- En uzun pencere 80: S6'da nMax 70 kalır.
- Eğim şartı: S6'da yok; yerine (2) sakin şartı (net değişim) var.
- Getiri etiketi: S6'da zaten yok (göz aracı; getiri ölçülmez).

## Bağımsız denetim notları (15 Kas 2026, ana model)
- AL ve KIRILDI işaretleri son mum KAPANINCA kesinleşir; seans içinde açık mumda geçici görünüp kaybolabilir. Günlük kapanıştan sonra bak (üretimdeki 'yarım bar' dersi).
- Yeşil yatay çizgi = AL eşiği (tavan mumunun High'ı); kutunun üst kenarı = bölgenin en yüksek noktası; ikisi farklı olabilir.
- Bölge 400 geçerli barı aşarsa kutunun sol kenarı yanlış çizilebilir (BIST'te 2016-26'da en uzun bölge 206 bar; tetiklenmedi).
- SIKLIK UYARISI (v1.0): bu kural setiyle (bant %12, net %3, küçük mum 0,90 x ATR, en az 8 mum) BIST'te hisse-yıl başına ~7 bölge ve ~3 AL çıkar; barların %28'i açık bölgede. v1.1 (BB 0,30 ile): ~4,2 bölge, ~1,9 AL, açık bar ~%18. Çöl nadir değil. Daha az bölge için ayarlardan nMin'i 15'e, bantMax'ı 0,08'e çekebilirsin; her değişiklik gösterimdir, ölçüm değil.
- Bölge sürekliliği: taban sürdükçe aynı bölge (ana model onayı; iş tanımındaki '±2 bar' kuralı üst üste binen kutular üretiyordu).
