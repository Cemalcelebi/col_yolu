# BIST kapanış sapması: Yahoo (bizim veri) ve resmi kaynak

## Özet (düz Türkçe)

- **Cemal'in sayfası BURCE, 19.07.2019.** Bağımsız resmi kaynak İş Yatırım açık uç (HisseTekil, ham fiyat). Resmi değerler, hisse 10 ile bölünmüş ölçekte: kapanış 0,365, en düşük 0,365, en yüksek 0,48, önceki kapanış 0,440, değişim −%17,04, hacim 52,3 M TL = yaklaşık 117,3 M adet. Cemal'in grafiği (kapanış 0,365 / düşük 0,365 / yüksek 0,48 / değişim −%17,05 / hacim 117 M) bunun TAM karşılığı. Yahoo tablosu (kapanış 0,370, düşük 0,370, değişim −%15,14, hacim 112,8 M) ise resmi değerden ayrışıyor. Yani Cemal'in uygulaması resmi veriyi gösteriyor, bizim Yahoo tablosu o gün resmi kapanışı yakalamamış. Açılış tek başına karşılaştırılamadı: İş Yatırım açık uçta açılış alanı yok (HGDG_AOF ağırlıklı ortalama fiyattır, açılış değil). Cemal'in açılışı 0,437 = Yahoo açılışı.
- **Sapma her yerde değil, tek bir dönemde.** 30 hissede, 2016-2023, 58.659 hisse-günlük karşılaştırma: ayar günleri hariç günlük kapanış değişimi farkı > 0,5 puan olan gün payı %13,2; > 1 puan %4,9; > 2 puan %1,1. Ama bunların neredeyse hepsi 27.02.2018 - 26.01.2021 arasında. O dönemde > 0,5 / 1 / 2 puan payları %34,0 / %12,4 / %2,6; dönem dışında %0,9 / %0,6 / %0,3. 2016-2017 ve 2021-2023 (Şubat) boyunca bizim kapanış resmi kapanışla ve hacim resmi hacimle fiilen aynı.
- **Tahmin hükmü: KISMEN.** Sapma yaşandığı dönemde "Yahoo kapanış seansı işlemlerini almıyor" ile uyumlu (resmi hacim ortanca %1,6 daha büyük, kapanış farkları işaretsiz iki yönlü, çoğu fark günlerinde resmi kapanış Yahoo'nun gün aralığı içinde), ama bu KALICI bir Yahoo davranışı değil: aynı Yahoo verisi 2016-17 ve 2021-23'te resmi veriyle birebir. Kapanış seansı BIST'te Mart 2012'den beri var (ikincil kaynak, doğrulanmadı), yani "kapanış seansı yok" tek başına 2018-21 penceresini açıklamıyor; olan, Yahoo'nun BIST beslemesinin o pencerede kapanış seansını/son işlemleri dışlamasıdır (neden: Yahoo veri sağlayıcısı kaynaklı, kanıtsız).
- **Etki:** 15 barlık kapanıştan kapanışa getiride Yahoo-resmi farkın standart sapması tüm dönemde 0,47 puan; sapma penceresi içinde (başlangıç ve bitiş pencere içinde) 0,76 puan (ortanca mutlak 0,31, %90'ı 1,15 puan altı, %99'u 2,6); pencere dışında 0,10 puan (ortanca mutlak ≈ 0). %5 / %10 hedefli 15 barlık sınamalarda 2018-2020 verisi için bu gürültü küçük değil ama hedefin 1/10'u düzeyinde.
- **Üretim tarayıcısının veri kaynağı: Yahoo (yfinance).** BASLAT.py satır 47 `yf.download(k+'.IS', ..., auto_adjust=False)` ve satır 77 grup indirme; önbellek veri_1d_turkey.pkl buradan yazılır (satır 69, 107). gh_gunluk.py BASLAT'ı çalıştırır ve "Yahoo gecikmiş olabilir" uyarısı verir (satır 191). tvDatafeed kullanılmıyor. Yani günlük tarayıcı bugünkü Yahoo'yu kullanıyor; bu sınamada Yahoo'nun 2021 sonrası verisi resmiyle aynı çıktı, ama 2024-26 dönemi için bu sınama yapılamadı (veri kesiği 29.12.2023, ayrı doğrulama gerekir).

## Yöntem

- Resmi kaynak: İş Yatırım `HisseTekil` (HG_KAPANIS, HG_MIN, HG_MAX, HG_AOF, HG_HACIM ham fiyat; HGDG_KAPANIS bölünme ayarlı), 04.01.2016-29.12.2023. Diğer kaynaklar denenmedi: ilk kaynak (a) erişilebildi ve 19.07.2019'u tam doğruladı; (b) Borsa İstanbul bülteni, (c) Stooq, (d) investing denenmedi (gerek kalmadı; ikinci bağımsız kaynak YOK, bu bir sınır: tek kaynak).
- Yahoo ham: yfinance auto_adjust=False (bitiş 29.12.2023). V_BIST: /tmp/kasa/acik/V_BIST.pkl (temettü ayarlı; hacmi ayar katsayısıyla ölçeklenmiş: fiyat oranı x hacim oranı = 1, kontrol edildi).
- Örneklem: GOZ PDF'indeki 5 BIST hissesi (BURCE, LIDFA, AVHOL, TRMET, ENJSA) + V_BIST'ten tohum 20261122 ile 25 rastgele hisse (≥ 1.500 gün ve 20.12.2023'te işlem gören; atlanan aday yok). Seçilenler: SELEC, PETKM, ERSU, TRGYO, KLNMA, VANGD, TMSN, AKYHO, ARSAN, TRHOL, KONYA, AKBNK, DERIM, MEPET, PAGYO, OZKGY, EMNIS, TSKB, KAPLM, HATEK, KRONT, PSDTC, FROTO, PNSUT, ODAS. Toplam 58.854 ortak gün.
- Günlük değişim farkı = Yahoo değişimi − resmi değişim (puan), yalnız her iki kaynakta da önceki gün aynı tarihse. Geçerli bar: iki kaynakta hacim > 0 (K3). Ayar günü: resmi ham/ayarlı oran basamağı ya da Yahoo bölünmesi ±2 gün içinde veya Yahoo/resmi oran basamağı (> %3) VE |fark| > 2 puan; 79 gün hariç tutuldu. Seviye ölçüleri ayar günlerinin ±3 günü dışında, ölçek yerel (21 gün) ortanca Yahoo/resmi fiyat oranıyla.
- Sapma dönemi sınırları (27.02.2018 / 26.01.2021) veriden okunmuş betimleyici sınırlardır, ön kayıtlı değil.

## 19.07.2019 BURCE ve çevre (resmi ham fiyat / 10 = Cemal ölçeği)

| Tarih | Resmi kapanış | Resmi düşük | Resmi yüksek | Resmi değişim % | Yahoo kapanış | Yahoo düşük | Yahoo değişim % | Resmi hacim (adet, Yahoo birimi) | Yahoo hacim |
|---|---|---|---|---|---|---|---|---|---|
| 16.07 | 0,337 | 0,308 | 0,340 | +8,36 | 0,338 | 0,308 | +8,68 | 41,06 M | 40,12 M |
| 17.07 | 0,388 | 0,306 | 0,393 | +15,13 | 0,392 | 0,306 | +15,98 | 114,1 M | 112,7 M |
| 18.07 | 0,440 | 0,380 | 0,457 | +13,40 | 0,436 | 0,380 | +11,22 | 451,1 M | 445,0 M |
| **19.07** | **0,365** | **0,365** | **0,480** | **−17,04** | 0,370 | 0,370 | −15,14 | 117,3 M | 112,8 M |
| 22.07 | 0,395 | 0,360 | 0,423 | +8,23 | 0,399 | 0,360 | +7,84 | 10,80 M | 10,66 M |
| 23.07 | 0,375 | 0,365 | 0,397 | −5,08 | 0,375 | 0,365 | −6,02 | 6,43 M | 6,41 M |
| 24.07 | 0,360 | 0,338 | 0,374 | −4,00 | 0,360 | 0,338 | −4,00 | 4,50 M | 4,41 M |

Resmi kapanış Yahoo düşüğünün (0,370) ALTINDA: kapanış, sürekli seans aralığı dışında oluşmuş (19.07'de resmi düşük = resmi kapanış = 0,365). Ardışık günlerin çoğunda sapma küçük ama aynı yönlü hacim farkı (resmi %1-4 büyük) var. V_BIST günlük değişimleri Yahoo ham ile aynı (8,68 / 15,98 / 11,22 / −15,14).

## Tablolar

**(a) Günlük kapanış değişimi farkı payları (Yahoo ham − resmi, ayar günleri hariç)**

| Küme | n | > 0,5 puan | > 1 puan | > 2 puan |
|---|---|---|---|---|
| Tümü (30 hisse, 2016-23) | 58.659 | %13,2 | %4,9 | %1,1 |
| V_BIST − resmi (temettü günü hariç) | 58.647 | %13,1 | %4,9 | %1,1 |
| 27.02.2018-26.01.2021 | 21.681 | %34,0 | %12,4 | %2,6 |
| Dönem dışı | 36.978 | %0,9 | %0,6 | %0,3 |

Yıl yıl (Yahoo ham, > 0,5 / > 1 / > 2): 2016 %0,5 / %0,3 / %0,03; 2017 %0,01 / %0,01 / %0; 2018 %30,7 / %11,6 / %1,7; 2019 %38,6 / %14,6 / %3,5; 2020 %28,3 / %9,2 / %2,1; 2021 %1,6 / %0,7 / %0,1; 2022 %3,2 / %1,7 / %0,7; 2023 %0,8 / %0,8 / %0,7. Hisse bazında > 1 puan payı %1,3 (PETKM) ile %15,0 (TSKB) arası (tüm hisseler JSON'da `sonuc.hisse`). 2022-23'teki küçük paylar farklı türdür: Yahoo'nun tek tek bayat/kaymış günleri (örn. 10-11.05.2022 KAPLM, MEPET, ARSAN).

**(b) Kapanış seviyesi (Yahoo kapanış / yerel ölçek / resmi kapanış)**

| Dönem | n | |fark| < %0,2 | Yahoo büyük | Yahoo küçük | ortanca mutlak % | %90 mutlak % |
|---|---|---|---|---|---|---|
| Tümü | 57.301 | %83,1 | %8,8 | %8,1 | ≈ 0 | |
| Sapma dönemi | 21.151 | %55,3 | %23,1 | %21,7 | 0,15 | 0,80 |
| Dönem dışı | 36.150 | ≈ %99,6 | küçük | küçük | ≈ 0 | |

Fark işaretsiz: Yahoo kapanışı resmiden yüksek ve düşük çıkma payı eşit (%23 / %22). 15 barlık getiri farkı ortalaması ≈ 0 (−0,0002 puan): sistematik yönlü yanlılık yok, yalnız gürültü. Fark > 1 puan günlerinde Yahoo değişimi resmiden büyük olan pay %49,9.

**(c) Hacim oranı (resmi adet / Yahoo hacim)**

| Dönem | ortanca | %25 | %75 | %95 |
|---|---|---|---|---|
| Sapma dönemi | 1,016 | 1,005 | 1,037 | 1,131 |
| Dönem dışı | 1,000 | 1,000 | 1,000 | 1,0002 |

Sapma döneminde resmi hacim sistematik olarak büyük (ortanca %1,6; 2019'da yıllık ortanca %2,4); gün payı > %2 olan %16,5 (yalnız bu dönemde), resmi < %0,98 olan %1,3. Dönem dışında fark yok (oran 1,0000). V_BIST hacim kayması: fiyat oranı x hacim oranı = 1 (kontrol: sapma ≈ 1e-16).

**(d) Fark günlerinde kapanış-aralık ilişkisi**

| Küme | n | Resmi kapanış = resmi düşük | = resmi yüksek | Resmi kapanış Yahoo [L, H] dışında | Yahoo yüksek = resmi max | Yahoo düşük = resmi min |
|---|---|---|---|---|---|---|
| Tüm günler | 57.301 | %11,3 | %8,5 | %1,2 | %98,9 | %98,7 |
| |fark| > 1 puan | 2.802 | %14,7 | %11,9 | %12,2 | %91,8 | %89,9 |
| |fark| ≤ 0,5 puan | 49.680 | %11,3 | %8,4 | %0,3 | %99,6 | %99,6 |
| Sapma dönemi, |fark| > 1 | 2.606 | %14,8 | %12,3 | %11,0 | %92,4 | %90,9 |

Yani büyük fark günlerinde resmi kapanış çoğunlukla (%89) Yahoo'nun gün aralığı İÇİNDE; yalnız yaklaşık %11-12'sinde aralık dışında (19.07.2019 gibi). Resmi kapanışın gün dibi/tepesi olma payı fark günlerinde taban orandan hafif yüksek (%14,7 / %11,9 ve %11,3 / %8,5): kapanış seansı fiyatı uç değerlere biraz daha yatkın, ama farkın ana nedeni bu değil. Sapma döneminde Yahoo yüksek/düşük de %3 oranında resmi max/min'den ayrışıyor (%97,2 / %96,9 eşit; dönem dışında %99,9 / %99,8).

**(e) Açılış / yüksek / düşük eşitliği:** Açılış karşılaştırılamadı (resmi açılış alanı yok). Yüksek eşitliği (%0,5 tolerans) %98,9, düşük %98,7 (tümü); sapma dönemi %97,2 / %96,9; dönem dışı %99,9 / %99,8. Kapanış eşitliği tümü %91,7, sapma dönemi %78,4, dönem dışı %99,6.

**(f) Zaman içinde:** Yahoo-resmi farkı 2016-2017 yok; ilk fark günü payı 27-28.02.2018'de bir günde sıfırdan %14-28'e sıçradı ve 26.01.2021'de bir günde sıfıra döndü (27.01.2021 sonrası > %0). Bu tarihler bilinen bir BIST kural değişikliği tarihi olarak DOĞRULANMADI (arama yalnız kapanış seansının 2012'de başladığını ve tek fiyat yöntemini gösterdi; 2018 ya da 2021 kural değişikliği bulunamadı). Aşağıdaki hükme göre sınırlar BIST kuralından değil Yahoo beslemesinden gelir (varsayım).

## Tahmin hükmü: KISMEN

- Destekleyen: sapma döneminde resmi hacim sistematik büyük ve resmi kapanış bazı günlerde Yahoo aralığı dışında (BURCE 19.07.2019 örneği: resmi düşük = kapanış = 0,365 < Yahoo düşüğü 0,370); fark işaretsiz (kapanışın seans sonu işlemleriyle belirlendiği tutarlı).
- Desteklemeyen: aynı Yahoo verisi 2016-2017 ve 2021-2023'te hacim ve kapanışta resmiyle birebir; kapanış seansı 2012'den beri var ise "Yahoo kapanış seansını hiç içermiyor" doğru olamaz. Fark günlerinin %89'unda resmi kapanış Yahoo aralığı içinde, yani Yahoo'nun son işlem fiyatı ile resmi kapanış arasındaki fark tek başına aralık dışı kapanış değil.
- Başka açıklamalar (hepsi test edilmedi): Yahoo veri sağlayıcısının 2018-02-27 / 2021-01-26 arasında farklı seans tanımı (en olası); Yahoo'nun geç gelen düzeltmeleri (sapma dönemi dışındaki 2022-23 tekil günler); yuvarlama (kapanış farkı ≈ 0,1 tik düzeyinde çoğu gün, tek başına bunu açıklamaz). Neden kanıtlanmadı.

## HATA

- İlk çalıştırmada JSON'a V_BIST için 15 günlük SD 1,58 puan yazıldı; bu temettü ayarlı seriyle ham resmi seriyi karşılaştırmanın yapay sonucu (temettü günleri). 15 günlük SD için Yahoo ham değeri esas alındı, V_BIST satırı "temettü dahil" etiketli duruyor.
- `hacim_orani_resmi_bizim.ort` ve `hacim_orani_rejim_disi.ort` ortalaması çok büyük (91, 144): tek günlerde Yahoo hacmi ≈ 0'a yakın (oran patlıyor); ortalama kullanılmaz, ortanca ve çeyrekler kullanıldı.
- Sapma dönemi tarihleri sonuçlara bakılarak okundu (ön kayıt yok): betimleyici.
- Tek bağımsız kaynak (İş Yatırım); BIST bülteni / Stooq / investing denenmedi.
- 2022-23'te Yahoo tekil bayat günleri var (ayrı tür), tümü sayıma dahil.

## KONTROL LİSTESİ (K2, K3, K6, K10, K13)

| Madde | Cevap | Kanıt |
|---|---|---|
| K2 geleceğe bakma | UYGULANMAZ | Getiri/sinyal ölçümü yok; yalnız aynı gün iki kaynağın karşılaştırması. Tüm dış istekler bitiş ≤ 29.12.2023. |
| K3 geçerli bar | EVET | İki kaynakta hacim > 0 ve resmi hacim > 0 şart; bayat/hacimsiz günler çıkarıldı (`hisse_cerceve`). |
| K6 veri birimi | EVET | Ham resmi fiyat / Yahoo bölünme ayarlı: yerel ortanca ölçek (BURCE 0,1) ve ayar günleri (79 gün hariç) denetlendi; V_BIST fiyat x hacim değişmezi kontrol edildi (≈ 1e-16). Temettü ayarlı V_BIST için ayrı uyumsuzluk sayımı (12 gün). |
| K10 ayrıştırma | EVET | JSON alanları elle doğrulandı: BURCE 19.07.2019 resmi kapanış/min/max/hacim Cemal'in ekran değerleriyle eşleşti (0,365/0,365/0,48/117 M). Hacim = TL/ortalama fiyat (HG_HACIM TL işlem değeri, adet değil). |
| K13 süreç | EVET | Kod modülü değiştirilmedi; yeni dosyalar; e-posta/anahtar yok (genel istemci, anahtarsız uç noktalar); defter dosyalarına dokunulmadı. Çalışma zamanı yeniden başlatma: üretim kodu değişmedi. |
