# MUM_IZI EK 27 İŞ TANIMI — UÇLAR: en küçük mumlu ve fitil şartları en radikal bölgeler; her ölçünün ucu ve hepsi birden; rastgele gün + piyasa tahmini ölçüsüyle (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas, EK 25 sonucundan sonra; yazdığı gibi): "Ben en küçük mumlar mumla dan oluşan olanları bulup ölçmek daha doğrusu bütün zorunlu fitilerin en radikal olan bölgeleri bulup tet etmek bulbuste her şeyi dene". Ana modelin okuması: şartları eşikten geçenleri değil, şartların EN UÇ olduğu bölgeleri (en küçük mumlar; fitil şartları en radikal) bul ve test et; bu çerçevede her şeyi dene.

Mantık: kalıp gerçekse doz - yanıt beklenir: şart ne kadar uçtaysa sonrası o kadar iyi olmalı. Bugüne kadar eşikten geçenler ölçüldü (Ç251, Ç254: lehte işaret yok). Not: '90'dan fazla şekil ölçüsü' kapalı konudur; bu iş Cemal'in açık isteğiyle ve en çok 12 ölçüyle yapılır.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut MUM_IZI*.py modülleri ve testleri (yalnız import), cemal_*.json. `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- KASA AÇILMAZ: veri <= 2022-12-31 (assert); 15 mumluk penceresi kesiği aşan olay ölçülmez. Geleceğe bakma yok: bütün ölçüler pencerenin son barına kadarki veriden; giriş = pencereden sonraki ilk geçerli bar açılışı. Geçerli bar kuralı (K3) MUM_IZI_GOZ ile aynı; kilitli / hacimsiz / fiyat adımına yapışmış (pencerede H = L olan bar payı > %20) pencereler ATILIR ve sayısı yazılır (en küçük mum ararken en büyük tuzak budur).
- Yeni tek dosya MUM_IZI_UC.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_mum_izi_uc.py. Sıra: kod + sentetik test -> GETİRİSİZ SAYIM -> ön kayıt MUM_IZI27_ON_KAYIT.md (kod sha, eşik sözlüğü sha, kesim değerleri, sayımlar, `python IZ_KARNE.py kontrol` tablosu) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> hesap -> rapor. Hiçbir tanım sonuca göre değişmez; değişirse SAPMA.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ (OLASILIK TABLOSU dahil), ÖNERİLEN DEFTER SATIRLARI.

## 1. Pencereler (iki evren; ikisi de günlük ve haftalık ayrı)
- E1 İSKELET: aday kuralının iskelet olayları (R4: yapı + dipte gel-git + yeşil kalıcı çıkış + tırmanış + bant içinde; mum biçimi kapıları M ve mum boyu kapısı OLMADAN); MUM_IZI8 taramasındaki R4 VAR, evren içi olaylar; aynı hissede 15 bar tekil. (Kod bu iskeleti hem çöküş dibinde hem geri çekilmede görüyor: Ç252.)
- E2 HER PENCERE: yapı şartı yok; her hissede 16 barlık pencereler, pencere sonu her 15 barda bir (örtüşmesiz); evren içi (P2 havuzu) ve önceki 120 barı olanlar.
- Dönem / pazar: ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22 (giriş tarihine göre); BIST ve 2016 öncesi BİLGİ.

## 2. Ölçüler (12; her biri sürekli; 'uç yön' sabit)
Pencere barlarından (son üçte bir ayrıca yazılanlar hariç pencerenin tamamı):
1. BOY_YUZDE_ORAN = (H - L) / C medyanı / önceki 120 barın medyanı (uç: KÜÇÜK).
2. BOY_GRAFIK_ORAN = (H - L) medyanı (fiyat birimi) / önceki 120 barın (H - L) medyanı (uç: KÜÇÜK; gözün gördüğü boy: Ç253).
3. BOY_MUTLAK = (H - L) / C medyanı, % (uç: KÜÇÜK).
4. GOVDE_ORAN = |C - O| / C medyanı / önceki 120 barın medyanı (uç: KÜÇÜK).
5. GOVDE_BOY = |C - O| / (H - L) medyanı (uç: KÜÇÜK).
6. UST_FITIL = üst fitil / (H - L) medyanı (uç: BÜYÜK).
7. ALT_FITIL = alt fitil / (H - L) medyanı (uç: KÜÇÜK).
8. UST_ALT_PAY = üst fitili alt fitilinden uzun olan mum payı (uç: BÜYÜK).
9. SON_UST_FITIL = ölçü 6, yalnız pencerenin son üçte biri (uç: BÜYÜK).
10. DARALMA = Bollinger (20, 2) genişliğinin pencere başından sonuna değişimi (uç: en çok DARALAN).
11. BANT_SON = son üçte birde (kapanış - SMA20) / (üst bant - SMA20) medyanı (uç: 1'e en yakın ve 1'in altında; ölçü = -|deger - 0,85|; 'ipin altına asılmış').
12. ONCEKI_DUSUS = pencereden önceki 60 barın en yükseğinden pencere dibine düşüş % (uç: en DERİN; 'çöküş dibi' tipi).
Bileşikler: (B1) KUCUK_MUM = ölçü 1-5'in uç yönlü yüzdelik sıralarının ortalaması; (B2) FITIL = ölçü 6-9'un; (B3) HEPSI = ölçü 1-11'in; (B4) HEPSI_VE = ölçü 1, 5, 6, 7, 10, 11'in her biri kendi uç %30'unda (hepsi birden).

## 3. Uç tanımı ve keşif / doğrulama (çoklu deneme koruması)
- Kesim değerleri YALNIZ KEŞİF örneğinden (ABD 2016-19; evren ve zaman dilimi başına) hesaplanır ve öteki hücrelere aynen uygulanır: UÇ10 = uç yönde en uç %10; UÇ2 = en uç %2; ayrıca beşlikler (doz - yanıt).
- KEŞİF = ABD 2016-19. DOĞRULAMA = ABD 2020-22 (ana), AVR 2016-19 ve AVR 2020-22 (yön).
- Aile = 16 (12 ölçü + 4 bileşik) x 2 uç x 2 evren x 2 zaman dilimi = 128 deneme; BH q 0,10 doğrulama p'lerine uygulanır.

## 4. Sonuç ölçüleri (Cemal'in ölçütü önce)
- TOPLAM FARK = R15 - T1 (T1 = aynı hissenin aynı dönemdeki bütün giriş günlerinin R15 ortalaması; E2'de hisse-dönem ortalaması bir kez hesaplanır): 'rastgele güne göre kârlılık'.
- ZAMANLAMA = PİYASA(t) - dönem piyasa ortalaması (PİYASA(t) = o gün pazarın bütün hisselerinin R15 ortalaması): 'uç bölgeler görüldüğünde piyasa yükseliyor mu'.
- SEÇİM = R15 - PİYASA(t).
- HEDEF: +%5 (ve +%10) stop'tan önce payı (stop = pencere dibi x 0,98) ve aynı hissenin rastgele günlerindeki payı (rastgele günde stop = önceki 16 barın dibi x 0,98; hisse-dönem başına 200 çekim, tohum 27); KAT = pay / taban payı.
- Çıkarım: AY KÜMELİ bootstrap %95 (10.000; tohum 27); her satırda n, farklı ay sayısı, en kalabalık 3 ay payı.
- Takvim (yalnız B3 ve B4 için, E2, günlük): son 5 günde UÇ10 olay sayısı = 0 / 1-5 / 6+ iken pazarın sonraki 15 günü (EK 25 2b kalıbı).

## 5. Hüküm (önceden)
- Bir (ölçü, uç, evren, zaman dilimi) satırı 'TUTAR' <=> KEŞİF'te TOPLAM FARK > 0 ve ay kümeli alt ucu > 0 VE ABD 2020-22'de n >= 30, farklı ay >= 12, TOPLAM FARK > 0 ve alt ucu > 0 VE BH q 0,10'u geçer VE AVR'nin iki döneminde TOPLAM FARK işareti artı (n >= 10 olanlarda). 'TEK DÖNEM' = yalnız biri. 'TERS' = doğrulamada üst ucu < 0. Ötekiler: n / ay yetmiyorsa 'ÖLÇÜLEMEDİ', yetiyorsa 'TUTMADI'.
- DOZ - YANIT: beşlik sırası ile TOPLAM FARK ortalamasının sıra ilişkisi (keşif ve doğrulamada ayrı); 'uç ne kadar radikalse o kadar iyi' <=> ikisinde de tek yönlü artış (5 beşlikte Spearman >= 0,9).
- GENEL: en az bir satır TUTAR ise 'AÇIK VERİDE ADAY (kasa açılmaz; ileri test)'; hiçbiri TUTAR değil ama TEK DÖNEM varsa 'TUTARSIZ'; hiçbiri yoksa ve güç yeterliyse (E2'de UÇ10 hücreleri n >= 1.000) 'UÇLARDA İZ YOK (E2)'; E1 için n küçükse 'ÖLÇÜLEMEDİ'.
- Evren bugün yaşayanlar (yukarı yanlı); tek hisse çarpıklığı için medyan ve artıda payı da yazılır.

## 6. Çıktılar
MUM_IZI_UC.py, test_mum_izi_uc.py; arastirma_cikti/mum_izi/MUM_IZI27_ON_KAYIT.md, MUM_IZI27_RAPOR.md (OLASILIK TABLOSU: satır = ölçü x uç; sütunlar = n, +%5 payı, taban payı, KAT, TOPLAM FARK [aralık], hüküm; keşif ve doğrulama yan yana), mum_izi27_sonuc.json, mum_izi27_ozet.csv (bütün satırlar). Olay dosyası büyükse repoya girmez (/root/.kasa/ham/mum_izi27 altında kalır; raporda yolu ve sha'sı). Ayrıca Cemal için tek sayfalık özet görsel: arastirma_cikti/mum_izi/MUM_IZI27_OZET.png (telefon ekranı; düz dil; her ölçü için 'en uç %10' ve 'en uç %2' bölgelerin rastgele güne göre farkı, keşif ve doğrulama yan yana çubuk; hüküm etiketi).
