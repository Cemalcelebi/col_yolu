# COL Fitil Öbeği — TradingView'de kullanım (v1.0, 16 Kasım 2026)

Gösterge, FITIL_OBEK.py (Ç187, FO_ESIK) tanımının bar bar Pine çevirisidir ve kodun bulduğu BÜTÜN fitil öbeği günlerini grafikte gösterir. S+DÜZ ise Cemal'in 16 Kasım ek tanımıdır (FITIL_KOR 'duz').

## Ekleme
1. TradingView > alttaki **Pine Editor** > içini sil > `COL_FITIL_OBEK.pine` dosyasının tamamını yapıştır > **Kaydet** > **Grafiğe ekle**.
2. Türkçe harfler bozuk görünürse ('Ã–' gibi) aynı kodun Türkçe karaktersiz kopyasını yapıştır: `COL_FITIL_OBEK_ascii.pine` (kod birebir aynı; yalnız yorum ve yazılarda ç->c, ş->s vb.).
3. **Basic plan sınırı: grafikte en çok 2 gösterge.** Bu kod tek göstergedir (zemin, üçgen, kutu, tablo ayrı sayılmaz). S5 ya da S6 göstergesi zaten ekliyse ikisi birlikte 2 eder; üçüncüsü için birini kaldır.
4. Grafik **günlük** (1G) olmalı. Kodu yeniden yapıştırınca göstergeyi grafikten kaldırıp yeniden ekle.

## Renkler
- **Açık mavi zemin** = S+ (YUKARI öbek): son 10 geçerli mumda üst fitiller baskın, altlar fitilsiz (ASIM >= 0,20 VE alt fitilsiz mum payı >= 0,50).
- **Açık kırmızı zemin + mum üstünde küçük kırmızı üçgen** = S- (AŞAĞI öbek, ayna: ASIM <= -0,20 VE üst fitilsiz mum payı >= 0,50).
- **Koyu mavi zemin + mum altında küçük yeşil üçgen** = S+DÜZ: S+ VE düz dip ((en yüksek dip - en düşük dip) / medyan mum boyu <= 1,0) VE dipte (kapanış son 120 geçerli günün aralığının alt %25'inde).
- **Soluk mavi kutu + yeşil kesik çizgi**: art arda S+DÜZ günleri tek bölge; kutu pencerenin ilk mumundan (10 geçerli mum geri) başlar, çizgi bölgenin en düşük dibidir.
- Sağ üstteki **tablo**: son geçerli mumun ASIM, ALTYOK, USTYOK, düz dip oranı, konum120, küçük mum oranı (bilgi), S+ / S- / S+DÜZ durumu, grafikteki gün sayıları ve son S+DÜZ bölgesinin tarihleri.

## Girdiler
- 'Fitil öbeği tanımı' (k = 10, fitil yok 0,10, ASIM 0,20, fitilsiz pay 0,50) ve 'S+DÜZ ek tanımı' (düz dip 1,0, konum günü 120, konum 0,25) ölçümün değerleridir: **değiştirme**, değiştirirsen görünen artık ölçülen sinyal değildir.
- 'Bilgi': küçük mum k_m 0,75 ve ATR% 250 gün (en az 120): yalnız tabloda gösterilir, şart değildir.
- 'Görünüm': S+ / S- boyası, kutu ve tablo açılıp kapatılabilir; renkler değiştirilebilir.

## Bilinen farklar (ölçümle)
- Likidite süzgeci ve cetvelin 60 günlük tekilleştirmesi yok: gösterge şartın tuttuğu her günü boyar (sığ hissede de).
- Ölçüm V_BIST düzeltilmiş fiyatla yapıldı. Fitil payları oran olduğu için düzeltme S+ / S- günlerini neredeyse hiç değiştirmez; konum120 bölünme / bedelli düzeltmesine bağlıdır (TradingView verisi).
- 31.08.2026 fon krizi kesiği yok: sonrası da boyanır, ama ölçülmedi.
- FITIL_KOR'da 'dip bağlamı' = S6 taban içi YA DA konum120 <= 0,25; Pine'da yalnız konum120.
- Geçersiz mum (H = L, hacim 0, kilitli gün) hesaba hiç girmez; pencere geçerli mum sayar.
- **Açık (bugünkü) mumda işaret geçicidir**: seans içinde çıkıp kaybolabilir; ölçüm kapanışla yapılır, kapanmış mumdaki işarete bak.

## Doğrulama
Dosyanın sonunda TEHOL (Mayıs 2025), BINBN (23.12.2024 - 22.01.2025) ve PAPIL (14.11 - 12.12.2025) için gün gün beklenen boyalar var. Python aynası ile FITIL_OBEK.fo_hisse_sinyal beş BIST hissesinin (TEHOL, BINBN, PAPIL, FENER, YKSLN) bütün geçmişinde S+ ve S- günlerinde 0 farkla aynı.

**Bu gösterge aday gösterir, alım-satım sinyali değildir.** Ç187 kararı: S+ ve S- ÖLÇÜLEMEDİ, hiçbir karar hücresi tutmadı (RAPOR.md); S+DÜZ ölçümü FITIL_KOR'dadır.
