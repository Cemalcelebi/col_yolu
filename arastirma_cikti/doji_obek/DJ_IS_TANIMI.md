# DOJI_OBEK İŞ TANIMI — aynı fiyat seviyesinde, bir-iki mum arayla oluşan doji öbekleri: sayısı ve sonrasında fiyatın seyri (27 Kasım 2026)

Yazan: ana model. Cemal (27 Kas; yazdığı gibi): "Aklıma yeni bir hipotez geldi doji mumları bir bölgede test edilsin bu bölge tespiti rahat mı devil mi bir bölgede bir iki mum aralıkla fiyatın bir seviyesinden oluşturduğu doji sayıları ve diji sayılarından sonraki fiyatın seyri bakalım". Ana modelin okuması: bir bölgede, aralarında bir-iki mum olacak şekilde, AYNI fiyat seviyesinde oluşan dojileri say; doji sayısına göre sonrasında fiyat ne yapıyor.
Önceki kayıt: 'doji oranı' eski çöl sisteminde bir ölçüydü; 'doji çıkış' ve 'doji-tolerans' (n 21) kapalı; aynı seviyede doji ÖBEĞİ ve sayısına göre sonrası hiç ölçülmedi. Tespit basit ve kesin kurallıdır (aşağıda).

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import; SEKIL_DEVAM.py ve WEB_DESEN.py'den import ETME: başka alt ajanlar çalışıyor). `git add -A` / `commit -a` yasak.
- KASA AÇILMAZ: veri <= 2022-12-31 (assert). Geleceğe bakma yok: öbek, k'inci dojinin barında, yalnız o bara kadarki veriyle tanınır; giriş = sonraki geçerli bar açılışı. Evren, veri yükleme, geçerli bar, ATRP20, T1, PİYASA(t), 'önce hangisine dokundu' mantığı, ay kümeli bootstrap: YUKSELIS_ONCESI / MUM_IZI_HAVUZ ile aynı.
- Yeni tek dosya DOJI_OBEK.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_doji_obek.py; çıktılar arastirma_cikti/doji_obek/.
- Sıra: kod + sentetik test -> GETİRİSİZ SAYIM + DJ_ORNEKLER.pdf (commit + push; hazır olunca ana modele tek satır ara mesaj: SendMessage to "main") -> ön kayıt DJ_ON_KAYIT.md (kod sha, eşik sözlüğü sha, sayımlar, `python IZ_KARNE.py kontrol` tablosu) commit + push (getiri dosyası üretilmeden ÖNCE; olay dosyası ile getiri dosyası ayrı) -> `IZ_KARNE.ik_kontrol_kapisi` -> ölçüm -> rapor. Eşikler sonuca göre değişmez.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Tanımlar (günlük mum ANA; haftalık BİLGİ; sabit)
- DOJİ: gövde |C - O| <= 0,10 x boy (H - L) VE boy >= 0,5 x ORT_BOY (ORT_BOY = önceki 10 barın boy medyanı; ölü / fiyat adımına yapışmış barlar doji sayılmaz) VE boy > 0. Kol D15: gövde <= 0,15 x boy (bilgi).
- DOJİ SEVİYESİ = (O + C) / 2.
- ÖBEK: art arda gelen dojiler arasında en çok 2 mum var (iki dojinin bar sırası farkı <= 3) VE öbekteki bütün doji seviyeleri 0,5 ATR20 genişliğinde bir bandın içinde ('aynı fiyat seviyesi'). Öbek, ilk dojiden başlar; şartı bozan bir doji gelirse ya da 3 bardan uzun doji gelmezse biter.
- SAYI k: öbekteki doji sayısı. OLAY: öbeğin k'inci dojisinin barı; k = 2, 3, 4+ için ayrı olaylar (aynı öbek büyüdükçe k = 2 olayı, sonra k = 3 olayı ... üretir; her olay yalnız o bara kadarki bilgiyle). Karşılaştırma tabanı TEK DOJİ (k = 1: öbek başlatmış ama henüz ikincisi gelmemiş doji) ve HERHANGİ GÜN.
- ÖBEK BANDI: öbekteki dojilerin en yüksek H'si ve en düşük L'si (çıkış yönü için).
- BAĞLAM (yalnız bilgi kırılımı; şart değil): KONUM120 üçte birlikleri (dipte / ortada / tepede) ve önceki 10 barın yönü (düşüş / yükseliş).

## 2. Sentetik test (zorunlu)
POZİTİF: aynı seviyede, 1-2 mum arayla 2 / 3 / 4 doji gömülmüş yapay seri. NEGATİF: farklı seviyelerde dojiler (seviye farkı > 0,5 ATR); aralarında 3'ten çok mum olan dojiler; gövdesi küçük ama boyu çok küçük (ölü) barlar; küçük gövdeli ama gövde / boy > 0,10 olan mumlar; rastgele seri. Yakalama >= %95, yanlış kabul <= %5 (tutmazsa kod hatası aranır; eşik değişmez).

## 3. Ölçüm (sabit)
- Hücreler: ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22. Her k için ve tek doji tabanı için:
  - SIKLIK: olay sayısı; bin hisse-günde kaç tane; öbeklerin k dağılımı (tespit ne kadar kolay / seyrek: Cemal'in sorusu).
  - YÖN: R15; TOPLAM FARK = R15 - T1 (aynı hissenin rastgele günü); SEÇİM = R15 - PİYASA(t); +2 ATR'ye, önce -1 ATR görmeden ulaşma payı ve aynası (-2 ATR, önce +1 görmeden); ikisinin farkı (asimetri) ve aynı hissenin rastgele günlerindeki karşılıkları.
  - HAREKETİN BÜYÜKLÜĞÜ: |R15| / (ATRP20 x karekök 15) ortalaması ve rastgele gün karşılığı (dojiden sonra hareket büyüyor mu küçülüyor mu).
  - ÇIKIŞ YÖNÜ: sonraki 15 barda fiyat ÖBEK BANDINI önce hangi yönden kapanışla aşıyor (yukarı / aşağı / hiç); çıkıştan sonraki 10 barın getirisi çıkış yönünde mi (devam) ters mi (tuzak); çıkış barından sonraki açılıştan ölçülür.
  - ÖNCEKİ YÖNE GÖRE: önceki 10 bar düşüşse sonrası dönüş mü devam mı (R15'in işareti önceki yönün tersi olan pay); yükselişse aynı.
  - DOZ - YANIT: k = 1, 2, 3, 4+ sırasıyla yukarıdaki ölçüler (doji sayısı arttıkça ne değişiyor).
- Çıkarım: ay kümeli bootstrap %95 (10.000; tohum 2712); her satırda n, farklı ay.
- HÜKÜM (önceden; iki yönlü, çünkü varsayım yön söylemiyor): k başına 'ARTI' <=> ABD'nin iki döneminde TOPLAM FARK > 0 ve alt ucu > 0 VE AVR'de işaret artı; 'EKSİ' <=> iki dönemde üst ucu < 0 VE AVR eksi; 'TEK DÖNEM'; aralık sıfırı içeriyorsa 'AYRIŞMIYOR' (n >= 1.000 ise güç yeterli; değilse 'ÖLÇÜLEMEDİ'). 'DOJİ SAYISI ETKİLİ' <=> k = 1'den 4+'ya TOPLAM FARK (ya da hareket büyüklüğü, ya da yukarı çıkış payı) iki dönemde de tek yönlü değişiyor VE k = 3 ya da 4+ ile tek doji arasındaki fark sıfırdan ayrışıyor. Çıkış yönü için: 'ÇIKIŞ DEVAM EDİYOR' <=> çıkıştan sonraki 10 bar getirisi çıkış yönünde > 0 ve alt ucu > 0, iki dönemde. Aile (k x ölçü) için BH q 0,10.
- Evren bugün yaşayanlar (yukarı yanlı).

## 4. Çıktılar
DOJI_OBEK.py, test_doji_obek.py; arastirma_cikti/doji_obek/: DJ_ORNEKLER.pdf (Cemal için; kapakta kuralın düz Türkçe üç satırı ve sıklık sayıları; sonra k = 2, 3, 4+ için gerçek veriden rastgele 4'er örnek: yüzde eksenli, öncesi 60 bar, dojiler işaretli, öbek bandı çizili, SONRASI YOK; ayrıca 2 'sayılmayan' örnek ve nedeni), DJ_ON_KAYIT.md, DJ_RAPOR.md, dj_sonuc.json, dj_ozet.csv. Büyük dosyalar repoya girmez (/root/.kasa/ham/doji_obek).
