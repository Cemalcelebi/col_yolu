# ÇÖL YOLU — KOD DEVİR NOTU (Cemal'in başka bir Claude oturumundan getirdiği not; 17 Kas 2026; olduğu gibi)

Kaynak: Cemal'in yapıştırdığı metin (Colab, tek dosya, Plotly; THYAO 6 ay; swing high/low; detect_desert_zones). Bu repodaki üretim zinciri (COL_v1 / takip) ve ölçüm modülleri (S6_TABAN, FITIL_V2) ile ilişkisi: aşağıdaki 'Cemal'in çöl tanımı (bağlayıcı)' bölümü kural defterine girer; 'yanlış / çöpe' bölümü hata defteri dersleriyle örtüşür.

1) ELDEKİ KOD (Colab, tek dosya, Plotly)
- load_data (yfinance, THYAO.IS, 6mo), find_swings (left/right=3), detect_desert_zones, build_chart.
- Orijinalde çöl = sadece peak mumunun H/L'i; kırılım = high > tepe*1.01 (50 bar içinde).
- Chart'ta sadece mum + dikey çizgi vardı.

2) DOĞRU / KALSIN
- Swing high/low mantığı (>=, <=) çalışır.
- yfinance MultiIndex düzeltmesi şart: get_level_values(0).
- Plotly 3 katman: mum + hacim + swing işaretleri + bant (add_shape) + kırılım çizgisi.
- Kapanışla kırılım (close > tavan) high'dan daha güvenilir.
- Çıktıya her bölge için tarih/üst/alt/genişlik yazdırmak.

3) YANLIŞ / ÇÖPE
- "Çöl = sol dip→peak arası min(high)" tanımı YANLIŞ (varsayımdı). Çöl swing peak'ten türetilmez.
- Tek mumun H/L'i ile çöl bandı kurmak YANLIŞ.
- Sabit % eşik (%1 genişlik, %1 kırılım) YANLIŞ: eşikler hisse başına olmalı (ATR/kendi volatilitesi).
- Tek özelliğe bakmak YANLIŞ: bölge, dip, Bollinger sıkışması, küçük mum, doji, birikim izi, hacim kuruması BİRLİKTE ölçülmeli.

4) CEMAL'İN ÇÖL TANIMI (bağlayıcı)
- Çöl = DİPTE, düşüşten sonra aylarca süren sıkışma; fiyat tabanı savunur. Tepedeki sıkışma = dağıtım, çöl DEĞİL.
- Küçük mum = fitil dahil kısa mum (H−L), gövde değil.
- Peş peşe büyük mumla bölgeden çıkılıyorsa çöl değildir. BIST "dev mum" (~%10) çöl içinde ASLA sayılmaz.
- İniş mumları (bölgeye giren büyük mumlar) çöle dahil edilmez.
- Bölgeden azıcık çıkıp dönmek olur; uzağa çıkıp dönmek çöl değil.
- EN KRİTİK ÖZELLİK: doji. Dipteki kutuda 3–5 doji bile birikim/sıkışma işaretidir; ağırlık burada.
- Çöl bir yıla kadar uzayabilir, genişleyebilir, içinde sert silkelemeler olur.
- Bitişte çok küçük mumlar (3 veya 7-8 adet) görülebilir (esnek, zorunlu değil).
- Eğim/"kanama" gürültü; AL kuralı: dünkü aday + kapanış > tavan×1.002.
- Segmentin en düşük dibi kırılırsa segment oradan yeniden hesaplanmalı.
- Üç faz: (1) sıkışma, (2) kırılım sonrası SMA üstü raf, (3) bölgeye sert test sonra hareket. İki kutu: kutu1=çöl (SMA200 civarı iyi), kutu2=raf; ilk giriş kutu2 sonrası hafif silkelemede, bölge testi yukarı dönerse ekleme.
- Güçlü sektör rüzgârı/katalizör olmadan çöl aranmaz.
- Daha önce 732 kırılımda çöl şekli tek başına yazı-tura çıktı (%36 yukarı uçtu, %32 aşağı kırdı); yani şekil tek başına yetmez.

5) MİMARİ / ÇALIŞMA KURALLARI
- Tek dosya, üretim kalitesi, KURAL_MOTORU mimarisi, tam hata yönetimi + log. Basit/hızlı yama yok.
- Doğru kısımları koru, yanlışı değiştir; baştan yazıp çalışan mantığı kaybetme.
- Eşitlik/isim çakışması gibi basit hataları kod kendisi mekanik yakalasın (load-time çakışma kapısı).
- Sonuç çıkarken: bir ölçü bir testte + diğerinde − ise iz değil; küçük örneklemi "bulgu" diye sunma; tek izle karar yok.
- Tarayıcı yalnızca aday bulur; desen/göstergeye göre alım-satım yasak. ABD hissesinde önce sermaye yapısı kontrolü.
- Yeni test önbellekten okusun (Drive: col_tarayici/veri_1d_turkey.pkl), yeniden indirmesin.
- Cevaplar Türkçe, "yatırım tavsiyesi değildir" cümlesi yok.

## Ana model notu (17 Kas): bu repodaki karşılıkları
- Çöl tanımı, küçük mum = H-L, üç faz / iki kutu, rüzgârsız çöl aranmaz, tarayıcı yalnız aday bulur: CLAUDE.md'de zaten var (24 Ekim'den beri).
- 'Çöl şekli 732 kırılımda yazı-tura (%36 / %32)': bu repodaki K18 / K19 / Ç85-Ç94 bulgularıyla aynı yönde (çöl bitişi rastgele hisseden iyi değil).
- Doji kutusu (A13, DOJI_KUTU): BIST'te ölçüldü, iz değil (Ç indeks); 'en kritik özellik doji' iddiası ölçümle desteklenmedi; S6'da doji sayısı yok -> bilgi sütunu olarak eklenebilir.
- 'BIST dev mum (~%10) çöl içinde sayılmaz', 'iniş mumları dahil edilmez', 'azıcık çıkıp dönmek olur': S6 v1.1 kutusu bant + küçük mum şartıyla büyük mumu dışlar, geriye uzatma iniş mumlarını bant dışı kaldığı için almaz, bant toleransı girdi; 'dip kırılırsa yeniden hesap' = S6 KIRILDI -> yeni kutu. Dev mum (>= %9,5 BIST) için açık şart yok -> kural defterine 'kodda yok' olarak.
- AL kuralı 'kapanış > tavan x 1,002': üretim COL_v1 AL_PAY ile aynı mantık.
