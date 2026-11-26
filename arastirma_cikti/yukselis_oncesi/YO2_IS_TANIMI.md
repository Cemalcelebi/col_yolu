# YUKSELIS_ONCESI EK 2 İŞ TANIMI — GERİYE DOĞRU DOĞRULAMA: 2016-22'de tutarlı yön veren üç şey, hiç bakılmamış 2000-2015 verisinde bir kez (26 Kasım 2026)

Yazan: ana model. Cemal: "Çok fazla filtre yürütme; ilk etapta bir mum yapısı, bir konum, bir şey bul; sonrası gelir." Bugünkü üç büyük ölçümde (Ç254, Ç255, Ç256) şart yığmadan, tek başına, iki dönemde aynı yönü veren yalnız üç şey çıktı; hiçbiri hüküm kuralını geçmedi, çünkü hepsi az sayıda takvim dönemine dayanıyor:
- H1 (hisse, ARTI): öncesinde DERİN DÜŞÜŞ olan bölgeden sonra 15 gün getirisi hissenin rastgele gününden yüksek (en derin %10: +0,7 / +0,8 puan; beşlikler tek yönlü).
- H2 (hisse, EKSİ): mumları olağanından KÜÇÜK bölgeden sonra getiri rastgele günden düşük (en küçük %10: -0,85 / -1,95 puan; beşlikler tek yönlü).
- H3 (piyasa, ARTI): pazarda uzun ortalamasının üstündeki hisse payı ÇOK DÜŞÜKKEN sonraki 15 günde piyasanın +%5 yapma olasılığı tabandan yüksek (2016-19 %37,6 / taban %8,4; 2020-22 %35,8 / %25,1).
Bu iş başka hiçbir şey denemez: üç varsayım, sabit yön, sabit kesim, yeni veri, tek sınama.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import; YUKSELIS_ONCESI.py'ye EKLEME yapılır, çalışan kısma ve eski çıktılara dokunmadan). `git add -A` / `commit -a` yasak.
- KASA AÇILMAZ: 2023 ve sonrası kullanılmaz (assert). Geleceğe bakma yok. Hacim kullanılmaz.
- Sıra: kod + test -> GETİRİSİZ SAYIM ve KESİMLER (kesimler yalnız 2016-22 haftalık verisinden; 2000-2015 getirilerine bakılmadan) -> ön kayıt YO2_ON_KAYIT.md (kod sha, kesimler, sayımlar, kontrol tablosu) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> ADIM 0 -> ADIM 1 -> rapor. Hiçbir tanım sonuca göre değişmez.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Veri ve haftalık tanımlar (sabit)
- Haftalık barlar (TEZGÂH 2 haftalık havuzu; ABD ana; AVR varsa yön). Günlük veri 2015'te başladığı için bu sınama HAFTALIK ölçekle yapılır: 15 işlem günü = 3 hafta.
- Pencere = son 3 hafta (t dahil). Giriş = t + 1 haftasının açılışı. R3 = t + 3 haftasının kapanışı / giriş - 1. T1 = aynı hissenin aynı dönemdeki bütün haftalarının R3 ortalaması. TOPLAM FARK = R3 - T1. Hedef: 3 haftada +%5'e, pencere dibinin %2 altına inmeden (haftalık barla; aynı haftada iki sınır: kötümser).
- DUSUS_W = pencereden önceki 12 haftanın en yükseğinden pencere dibine düşüş %. BOY_W = pencerenin (H - L) / C medyanı / önceki 24 haftanın medyanı (en az 12 hafta).
- PİYASA: P3(t) = evrenin eşit ağırlıklı ortalama R3'ü; ayrıca hayatta kalma yanlılığı olmayan bir ölçü olarak ENDEKS: yerelde SPY / S&P 500 haftalık serisi varsa o (yoksa bağlı Tiingo servisinden SPY günlük fiyatları indirilip haftalığa çevrilir; dosya repoya girmez); G40(t) = evrende kapanışı 40 haftalık ortalamasının üstünde olan hisse payı.
- Kesimler (2016-22 haftalık verisinden, sabit sayı olarak ön kayda yazılır): DUSUS_W en derin %10; BOY_W en küçük %10; G40 en düşük %10.

## 2. ADIM 0 — ölçek sağlaması (2016-22; görülmüş veri; bilgi)
Haftalık tanımlarla 2016-19 ve 2020-22'de H1, H2, H3 aynı yönü veriyor mu (günlük sonuçların haftalık karşılığı). Bir varsayım haftalık ölçekte iki dönemin birinde bile ters yön verirse o varsayım için ADIM 1 'ÖLÇEK UYMADI' diye okunur (yine hesaplanır, ayrı etiketle).

## 3. ADIM 1 — 2000-2015 (hiç bakılmamış; tek sınama)
- H1: DUSUS_W uç %10 pencerelerde TOPLAM FARK ortalaması; H2: BOY_W uç %10 pencerelerde TOPLAM FARK; ikisi için +%5 hedef payı ve aynı hissenin rastgele haftalarındaki payı (KAT).
- H3: G40 <= kesim olan haftalardan sonra P3 ve ENDEKS 3 haftalık getirisi; P(>= +%5), P(<= -%5); öteki haftalarla fark.
- Çıkarım: ÇEYREK KÜMELİ bootstrap %95 (10.000; tohum 2000); her satırda n, farklı çeyrek sayısı, AYRI DÖNEM sayısı (H3 için: düşük genişlik haftalarının, aralarında en az 8 hafta olan öbekleri) ve en kalabalık 3 çeyreğin payı. Alt dönemler bilgi: 2000-07, 2008-15.
- HÜKÜM (önceden): H1 'DOĞRULANDI' <=> 2000-2015'te TOPLAM FARK > 0 ve çeyrek kümeli alt ucu > 0 VE iki alt dönemde işaret artı; H2 'DOĞRULANDI' <=> TOPLAM FARK < 0 ve üst ucu < 0 VE iki alt dönemde işaret eksi; H3 'DOĞRULANDI' <=> ENDEKS ile ölçülen 3 haftalık getiri farkı > 0 ve alt ucu > 0 VE P(>= +%5) farkı > 0 VE ayrı dönem sayısı >= 4. Aralık sıfırı içeriyorsa 'GÖSTERİLEMEDİ'; işaret tersse 'TERS'; ayrı dönem < 4 ya da n yetersizse 'ÖLÇÜLEMEDİ'.
- HAYATTA KALMA UYARISI (zorunlu, rapora ve özete yazılır): evren bugün yaşayan hisseler; 2000-2015'te derin düşüşten sonra batanlar veride yok, bu H1'i ve evren ortalamasıyla ölçülen H3'ü YUKARI çeker. Bu yüzden H3 hükmü ENDEKS ile verilir; H1 için 'DOĞRULANDI' çıksa bile etiket 'YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)' olur. H1'in düşüş tarafı da yazılır: uç pencerelerde 3 haftada -%20'den kötü olanların payı ve tabanı.
- Sonuç ne olursa olsun kasa açılmaz; DOĞRULANDI çıkan varsayım IK_ILERI adayı ve 'birleşik iz bileşeni adayı' olur.

## 4. Çıktılar
YUKSELIS_ONCESI.py (ek komutlar) + test; arastirma_cikti/yukselis_oncesi/: YO2_ON_KAYIT.md, YO2_RAPOR.md, yo2_sonuc.json, yo2_ozet.csv. Görsel yok.
