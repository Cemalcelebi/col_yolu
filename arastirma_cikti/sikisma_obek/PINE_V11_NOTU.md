# COL_S5_OBEK.pine v1.1 notu (15 Kasım 2026)

- Sorun (Cemal, ekran görüntüsü): v1.0 yalnız şartın tuttuğu GÜNÜ boyuyordu; grafikte 1-4 mumluk 'bölgeler' ve yan yana iki ayrı bant çıkıyordu.
- Cemal'in kuralı: bölge en az 8 mum (5 alt sınır), çoğu 60 muma kadar; tek mumluk bölge yok; bitişik parçalar tek bölge.
- v1.1: bölge KUTU ile çizilir. Karar gününde (önceki 19 geçerli barda S5 yok) kutu, son p = 15 geçerli barın ilkinin gerçek bar_index'inden (geçerli bar dizisi `aIdx`) bugüne açılır; üst = pencere en yüksek High, alt = en düşük Low; DİP mavi, YOL ÜSTÜ turuncu (renk karar günündeki sınıf). Aynı bölgede (son S5 gününden < 20 geçerli bar) S5 yeniden tutunca aynı kutu sağa uzar, üst / alt genişler. Kutu en az 15 geçerli bardır.
- Eski günlük zemin boyası 'S5 günlerini zemin boya' (gosterZemin) ile isteğe bağlı, varsayılan kapalı. Üçgen (karar günü) aynı. Tabloya 'son bölge / bölge uzunluğu (bar)' satırı eklendi (tarih aralığı, grafik bar sayısı, geçerli bar sayısı, sınıf).
- S5 ölçüm tanımı (eşikler, p = 15, a..e, sınıflar, karar günü) DEĞİŞMEDİ; yalnız çizim değişti. Dosya sonundaki beklenen günler artık kutunun içindedir.
- COL_S5_OBEK_ascii.pine yeniden üretildi: ASCII dışı karakter 0, yorum / dize dışındaki kod birebir aynı.
- Derleyici yok: kod TradingView'de ilk yapıştırmada denetlenmeli (hata çıkarsa satır numarasıyla bildirilecek).
