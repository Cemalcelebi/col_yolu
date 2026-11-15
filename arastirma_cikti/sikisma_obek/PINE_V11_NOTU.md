# COL_S5_OBEK.pine v1.1 notu (15 Kasım 2026)

- Sorun (Cemal, ekran görüntüsü): v1.0 yalnız şartın tuttuğu GÜNÜ boyuyordu; grafikte 1-4 mumluk 'bölgeler' ve yan yana iki ayrı bant çıkıyordu.
- Cemal'in kuralı: bölge en az 8 mum (5 alt sınır), çoğu 60 muma kadar; tek mumluk bölge yok; bitişik parçalar tek bölge.
- v1.1: bölge KUTU ile çizilir. Karar gününde (önceki 19 geçerli barda S5 yok) kutu, son p = 15 geçerli barın ilkinin gerçek bar_index'inden (geçerli bar dizisi `aIdx`) bugüne açılır; üst = pencere en yüksek High, alt = en düşük Low; DİP mavi, YOL ÜSTÜ turuncu (renk karar günündeki sınıf). Aynı bölgede (son S5 gününden < 20 geçerli bar) S5 yeniden tutunca aynı kutu sağa uzar, üst / alt genişler. Kutu en az 15 geçerli bardır.
- Eski günlük zemin boyası 'S5 günlerini zemin boya' (gosterZemin) ile isteğe bağlı, varsayılan kapalı. Üçgen (karar günü) aynı. Tabloya 'son bölge / bölge uzunluğu (bar)' satırı eklendi (tarih aralığı, grafik bar sayısı, geçerli bar sayısı, sınıf).
- S5 ölçüm tanımı (eşikler, p = 15, a..e, sınıflar, karar günü) DEĞİŞMEDİ; yalnız çizim değişti. Dosya sonundaki beklenen günler artık kutunun içindedir.
- COL_S5_OBEK_ascii.pine yeniden üretildi: ASCII dışı karakter 0, yorum / dize dışındaki kod birebir aynı.
- Derleyici yok: kod TradingView'de ilk yapıştırmada denetlenmeli (hata çıkarsa satır numarasıyla bildirilecek).

## v1.2 (15 Kasım 2026)

- Sorun (Cemal, ENJSA ekran görüntüsü, v1.1): kutu 15 mumla sabit çizildiği için sınırlar rastgele görünüyordu; kutunun hemen ÖNCESİNDEKİ bir küçük mum ve hemen SONRASINDAKİ iki küçük mum kutunun fiyat bandının içinde olduğu hâlde dışarıda kaldı. Cemal'in gözünde bölge = aynı bant içinde kalan ardışık küçük mumların tamamı; sınırlar mumlardan gelir, sayıdan değil.
- Yeni girdiler (Görünüm): `genislet` ('Kutuyu banda göre genişlet (v1.2)', varsayılan açık; kapalıysa v1.1 birebir), `bantTol` ('Bant toleransı (%)', oran, varsayılan 0), `uzunEnCok` ('Bölge en çok (bar)', varsayılan 60).
- Bant = karar günündeki 15 barlık pencerenin en yüksek High / en düşük Low'u, x (1 +/- bantTol).
- GERİYE: kutu açılırken pencerenin ilk geçerli barından geriye, geçerli bar dizilerinde (aH / aL / aIdx / aZmn) High <= üst ve Low >= alt olan ardışık barlar bölgeye katılır; ilk bant dışı barda, önceki kutunun sağ kenarında ya da toplam uzunluk 60 geçerli bar olunca durur. Bant geriye genişlemede değişmez. Sol kenar ve tablo başlangıç tarihi buna göre.
- İLERİYE: kutu açıkken her geçerli bar bant içindeyse ya da o gün S5 tutuyorsa kutu sağa uzar (S5 gününde üst / alt pencere High / Low'uyla genişler, bant da genişler); bant dışı ve S5 değilse kutu KAPANIR (sağ kenar son içerideki bar); 60 geçerli barda da kapanır. Kapanmış kutu bir daha uzamaz.
- Kapanmış kutudan sonra gelen S5 günü (ara < 20 olsa bile) YENİ kutu açar; üçgen yine yalnız karar gününde (ara >= 20). Bu, v1.1'deki 'son S5 gününden < 20 bar ise aynı kutu' kuralının yerine geçer. Karar günü açık bir kutunun içinde gelirse eski kutu o günü almadan kapanır, yeni kutu açılır.
- Tablo: 'bant üst / alt (tolerans)' satırı ve bölge durumu (AÇIK / KAPANDI / v1.1 modu) eklendi; 'son bölge' satırının bitiş tarihi artık kutunun son barıdır.
- Karar günü ve S5 ölçümü DEĞİŞMEDİ. Kutunun sağ kenarı (ve geriye genişleme) gösterimdir, sonradan belli olur; işlem kararı üçgen günündedir.
- Bilinen görsel durum: kapanan kutudan kısa süre sonra açılan yeni kutunun 15 barlık penceresi önceki kutuyla üst üste binebilir (pencere her zaman tam çizilir; yalnız geriye genişleme önceki kutuyu geçmez).
- COL_S5_OBEK_ascii.pine yeniden üretildi: ASCII dışı karakter 0, yorum / dize dışındaki kod birebir aynı (501 satır).
- Derleyici yok: v1.2 TradingView'de ilk yapıştırmada denetlenmeli.
