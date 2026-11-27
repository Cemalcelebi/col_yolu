# COL_SKOR6 İŞ TANIMI — eski çöl skoru (GEN10_COL_OGREN v5: altı ölçü) örneklem dışında: kitaplıktaki çölleri tanıyor mu, yüksek skordan sonra ne oluyor (27 Kasım 2026)

Yazan: ana model. Cemal (27 Kas; eski kodu GEN10_COL_OGREN.py v5'i yapıştırarak): "Eski çalışmalarda şu şekilde bir kod vardı belki sana yol gösterir bilmiyorum işte". Kodun özü: bir BÖLGEYİ altı ölçüyle puanlar: F1 doji oranı (ana; doji = gövde / boy < 0,40), F2 Bollinger genişliğinin daralması, F3 daralmanın yüksekten başlaması, F4 fiyat sıkışması, F5 sol bacak düşüşü, F6 hacim azalması (bölge hacmi / önceki 200 barın ortalaması). 20 bölgelik elle seçilmiş kitaplık (BIST 2024-26); etiket = bölge bitişinden sonraki 20 barda en yüksek fiyat >= +%10 ('sağ bacak'); ağırlıklar ve eşik AYNI 20 örnekten öğrenilip AYNI 20 örnekte sınanıyor.
Ana modelin okuması: (1) Cemal'in 'çöl'ü tek bir mum şartı değil, altı ölçünün birlikte PUANI; (2) eski kodun doğruluk testi örneklem içi olduğu için bir şey söylemiyor; (3) doğru sınama: aynı puanı hiç görmediği veride koşmak. Defterde: col_ogren v1.3 (9 Eki; 9.419 çöl) 'doji ayırmadı, yeniden doğrulanmalı' notu açık; Ç38-Ç39 doji kutusu BIST'te yukarı için iz değil; ABD hiç koşulmadı. Bu iş o açığı kapatır. Hacim bu puanın parçası olduğu için kullanılır.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import; SEKIL_DEVAM.py, WEB_DESEN.py, DOJI_OBEK.py'den import ETME). `git add -A` / `commit -a` yasak.
- KASA: ölçüm verisi <= 2022-12-31 (assert). TEK İSTİSNA (yalnız tespit; getiri YOK): kitaplıktaki 20 bölgenin altı ölçüsü ve puanı, bölge bitiş tarihine kadarki BIST verisinden hesaplanır (2024-26); bu bölgelerin SONRASI hesaplanmaz, çizilmez, yazılmaz (kodda ayrı fonksiyon + assert).
- Geleceğe bakma yok: puan pencerenin son barına kadarki veriyle; giriş = sonraki geçerli bar açılışı. Evren, veri yükleme, geçerli bar, ATRP20, T1, PİYASA(t), 'önce hangisine dokundu', ay kümeli bootstrap: YUKSELIS_ONCESI / MUM_IZI_HAVUZ ile aynı; kilitli / fiyat adımına yapışmış pencereler atılır (MUM_IZI_UC kuralı; doji sayarken en büyük tuzak).
- Yeni tek dosya COL_SKOR6.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_col_skor6.py; çıktılar arastirma_cikti/col_skor6/.
- Sıra: kod + test -> GETİRİSİZ SAYIM + KİTAPLIK TESPİTİ (2. bölüm) -> ön kayıt CS_ON_KAYIT.md (kod sha, eşik sözlüğü sha, sayımlar, kitaplık sonucu, `python IZ_KARNE.py kontrol` tablosu) commit + push (getiri dosyası üretilmeden ÖNCE; özellik ve getiri dosyaları ayrı) -> `IZ_KARNE.ik_kontrol_kapisi` -> KEŞİF (ABD 2016-19: yalnız 'öğrenilmiş ağırlık' kolu için) -> ağırlıklar CS_KESIM.md'ye commit + push -> ölçüm -> rapor. Hiçbir tanım sonuca göre değişmez.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Altı ölçü ve puan (eski koddaki tanımlar AYNEN)
Pencere (bölge) uzunlukları L = 20, 40, 80 bar (kitaplıktaki bölgeler 5-190 bar; ayrı ayrı); her hissede her 5 barda bir pencere sonu.
- F1 f_doji_orani = penceredeki mumlardan gövde / boy < 0,40 olanların payı.
- F2 f_bbw_daralma = (pencere başındaki BBW - pencere içi en küçük BBW) / pencere başındaki BBW; BBW = (4 x 20 günlük standart sapma) / 20 günlük ortalama (kapanıştan).
- F3 f_bbw_baslangic = kırp(pencere başındaki BBW / 0,6; 0..1).
- F4 f_fiyat_sikisma = kırp(1 - (pencere en yüksek H - en düşük L) / ikisinin ortası; 0..1).
- F5 f_sol_dusus = kırp((pencereden önceki 30 barın en yükseği - pencere dibi) / o en yüksek; 0..1).
- F6 f_vol_azalma = kırp(1 - pencere ortalama hacmi / pencereden önceki 200 barın ortalama hacmi; 0..1) (önceki en az 20 bar).
- PUAN_ESIT = altı ölçünün (0..1) ortalaması x 100. PUAN_OGR = eski koddaki yöntemle öğrenilmiş ağırlıklarla (ağırlık = |etiketi 1 olanların ortalaması - 0 olanların ortalaması| / standart sapma, toplamı 1'e ölçeklenir), ağırlıklar YALNIZ ABD 2016-19'dan (eski etiketle) öğrenilir ve öteki dönemlere aynen uygulanır. Ayrıca her ölçü tek başına.
- ÜST DİLİM kesimleri (uç %10 ve %2; beşlikler) pazar ve L başına ABD 2016-19'dan (AVR ve BIST için kendi 2016-19'undan), sabit.

## 2. KİTAPLIK TESPİTİ (Cemal'in kendi 20 çölü; yalnız puan; sonrası yok)
Eski koddaki KITAPLIK listesi (sembol, col_bas, col_bit; 20 satır) koda aynen yazılır. Her bölge için altı ölçü ve PUAN_ESIT, bölgenin kendi başlangıç - bitişiyle hesaplanır ve BIST 2016-22 pencerelerinin (L'si en yakın olan) puan dağılımındaki yüzdelik sırası verilir. ÖLÇÜ: kitaplık bölgelerinin kaçı puanın üst %10'unda, kaçı üst %30'unda, kaçı medyanın altında; ölçü ölçü aynı. Bu, puanın Cemal'in çöl dediği şeyi tanıyıp tanımadığının sınamasıdır (tanımıyorsa 3. bölümün sonucu 'kodun puanı' diye okunur, 'Cemal'in çölü' diye değil). Veri yoksa (sembol panelde yok / tarih aralığı kapsanmıyor) o satır 'veri yok'.

## 3. Ölçüm (ABD ve AVR karar; BIST bilgi; 2016-19 ve 2020-22)
- ESKİ ETİKET (aynen): SAG10 = pencere son kapanışına göre sonraki 20 barda en yüksek fiyat >= +%10. Aynası: SOL10 = en düşük fiyat <= -%10.
- OYNAKLIK TUZAĞI (K60 / Ç255 dersi; zorunlu): SAG10 oynaklıkla mekanik artar. Her şey ATRP20 beşliği içinde okunur: KAT = P(SAG10 | üst dilim, beşlik) / P(SAG10 | beşlik), olay ağırlıklı; ASİMETRİ = [P(SAG10) - P(SOL10)] üst dilimde eksi aynı beşlikte tabanda.
- Cemal'in ölçütü: R15 ve TOPLAM FARK = R15 - T1 (aynı hissenin rastgele günü); +2 ATR'ye, önce -1 ATR görmeden ulaşma payı ve aynası; SEÇİM = R15 - PİYASA(t).
- Her PUAN kolu (ESIT, OGR) ve her tek ölçü için üst %10, üst %2 ve beşlikler (doz - yanıt); L = 20 / 40 / 80 ayrı.
- Çıkarım: ay kümeli bootstrap %95 (10.000; tohum 2713); n, farklı ay. Aile = (2 puan + 6 ölçü) x 2 uç x 3 uzunluk; BH q 0,10.
- HÜKÜM (satır başına; önceden): 'TUTAR' <=> ABD'nin iki döneminde de ATRP içi KAT > 1 ve alt ucu > 1 VE ASİMETRİ > 0 ve alt ucu > 0 VE TOPLAM FARK > 0 ve alt ucu > 0 VE AVR'nin iki döneminde üç ölçünün işareti aynı yönde VE BH'yi geçer. 'YALNIZ OYNAKLIK' = ham KAT > 1 ama ATRP içinde değil ya da ASİMETRİ <= 0. 'TEK DÖNEM', 'TERS', 'TUTMADI', 'ÖLÇÜLEMEDİ' (n < 1.000 ya da farklı ay < 12).
- Evren bugün yaşayanlar (yukarı yanlı).

## 4. Çıktılar
COL_SKOR6.py, test_col_skor6.py; arastirma_cikti/col_skor6/: CS_ON_KAYIT.md, CS_KESIM.md, CS_RAPOR.md (iki tablo: KİTAPLIK TESPİTİ; OLASILIK TABLOSU), cs_sonuc.json, cs_ozet.csv. Görsel yok (iz çıkarsa ana model ayrıca ister). Büyük dosyalar repoya girmez (/root/.kasa/ham/col_skor6).
