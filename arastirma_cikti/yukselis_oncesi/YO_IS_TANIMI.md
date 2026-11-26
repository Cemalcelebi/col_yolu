# YUKSELIS_ONCESI İŞ TANIMI — yükseliş trendinden önce hangi bölge var: yükselişten geriye bakış, sonra ileriye doğru sınama (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas; yazdığı gibi): "Sende artık bir şeyleri kendi bulma gerekir yani şunu düşün hangi bölge bir yukselis trendin öncesinde var"; önceki sözleri: "asıl derdimiz piyasanın yükselişini tahmin etmek"; "ben sadece görüntüye bakıyorum belki görüntüde bir iz yok başka verilerde var".

Önceki işler (özet; tekrar edilmez): Ç12 (yükselişten geriye, eski, ileri sınama yok), Ç182 (tek günlük büyük mumdan geriye: küçük mumlu sessiz bölge büyük mum olasılığını DÜŞÜRÜYOR; yön bilgisi yok), Ç204 (15 bar ufkunda 124 hipotez: İZ DEĞİL), Ç205 / Ç209 (kart turları: tutan yok), K60 (olasılık izlerinin hepsi oynaklık etkisi), Ç251 / Ç254 (kodun seçtiği mum bölgeleri: rastgele günden kötü). BOŞLUK: kalıcı yükseliş (çok günlü trend) için olay tabanlı, eşli kontrollü geriye bakış + ileri sınama hiç yapılmadı; aşağıdaki sekiz özellik ailesi kayıtta yok.
Hacim, sektör ısısı, VIX / DXY kapalı konudur: bu işte KULLANILMAZ (Cemal 'aç' derse ayrı ek).

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, mevcut modüller ve testleri (yalnız import). `git add -A` / `commit -a` yasak; yalnız kendi yolların. Başka bir alt ajan MUM_IZI_UC.py / mum_izi27_* üzerinde çalışıyor: dokunma.
- KASA AÇILMAZ: veri <= 2022-12-31 (assert); 15 barlık penceresi kesiği aşan giriş ölçülmez. Geleceğe bakma yok: bütün özellikler t gününe kadarki veriden; giriş t + 1 açılış. Geçerli bar kuralı (K3), evren (TEZGÂH 2 P2 havuzu) ve veri yükleme MUM_IZI_HAVUZ / MUM_IZI_GOZ ile aynı.
- Yeni tek dosya YUKSELIS_ONCESI.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_yukselis_oncesi.py; çıktılar arastirma_cikti/yukselis_oncesi/.
- Sıra: kod + sentetik test -> GETİRİSİZ SAYIM -> ön kayıt YO_ON_KAYIT.md (kod sha, eşik sözlüğü sha, sayımlar, `python IZ_KARNE.py kontrol` tablosu) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> ADIM 1 (yalnız KEŞİF verisi) -> kesimler ve yönler YO_KESIM.md'ye yazılıp commit + push (DOĞRULAMA verisine bakılmadan) -> ADIM 2 (doğrulama) -> rapor. Hiçbir tanım sonuca göre değişmez; değişirse SAPMA.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ (OLASILIK TABLOSU), ÖNERİLEN DEFTER SATIRLARI.

## 1. Yükseliş tanımı (sabit; günlük mum; hisse-gün birimi)
- Y10 (ANA) = t + 1 açılışından sonraki 15 geçerli barda fiyat +%10'a, girişin %5 altına inmeden ulaşır ('temiz yükseliş').
- Y5 (ikinci) = +%5'e, %5 altına inmeden. D10 (ayna; denetim) = -%10'a, girişin %5 üstüne çıkmadan iner.
- R15 = 15. bar kapanışı / giriş - 1. KALICI (bilgi) = 30 barda +%20'ye, %8 altına inmeden.
- PİYASA: P15(t) = pazarın (ABD; AVR ayrı) bütün evren hisselerinin t + 1 açılışından 15. güne eşit ağırlıklı ortalama getirisi; YP = P15 >= +%5 ('piyasa yükselişi'); DP = P15 <= -%5.
- Örnekleme: her hissede her 5 barda bir t (örtüşme azaltılır); dönemler ABD 2016-19 (KEŞİF), ABD 2020-22 (DOĞRULAMA ana), AVR 2016-19 ve 2020-22 (yön doğrulaması); BIST bilgi.

## 2. Özellikler (t günü; hacim yok; 'yeni' = kayıtta hiç bakılmamış)
YENİ: (1) MIKRO = son 60 barda art arda en az 3 yükselen kapanış serisi sayısı; (2) RS_DIP = hisse / pazar ortalaması oranının 60 barlık en yükseğine uzaklığı VE fiyatın 120 barlık aralıktaki konumu (ikisi ayrı sütun + birlikte: 'fiyat alt yarıda, göreli güç zirveye %3 içinde'); (3) GENISLIK = pazarda SMA50 üstündeki hisse payı ve 10 günlük değişimi (her hisse için aynı gün aynı değer); (4) OYN_SIRA = 60 günlük oynaklığın o gün evrendeki yüzdelik sırası; (5) MA_DIZI = SMA20 / SMA50 / SMA200 sıralama kodu ve SMA20 eğiminin 10 günlük değişimi; (6) DD_SURE = 250 barlık zirveden bu yana bar sayısı, zirveden düşüş %, dipten bu yana bar sayısı ve dipten toparlanma hızı (% / bar); (7) CLV = son 10 barda (C - L) / (H - L) ortalaması ve önceki 30 bara göre farkı; (8) YUKSELEN_DIP = son 60 barda 5 barlık yerel diplerden art arda yükselen dip sayısı.
KONTROL (bilinenler; yeni bir şeyin bunlardan fazlasını söyleyip söylemediğini görmek için): MOM_12_1, F15 (15 barlık geçmiş getiri), KONUM120, ATRP20 (oynaklık), önceki EK 27 ölçülerinden BOY_YUZDE_ORAN ve ONCEKI_DUSUS (aynı tanım).
PİYASA özellikleri (pazar-gün birimi): genişlik düzeyleri (SMA20 / 50 / 200 üstü pay) ve 5 / 10 günlük değişimleri, pazarın 20 / 60 günlük getirisi ve 60 günlük zirveden düşüşü, 20 günlük dipte olan hisse payı, yeni 60 günlük zirve - dip farkı, kesit dağılımı (o günkü 20 günlük getirilerin standart sapması), medyan ATRP yüzdelik sırası.

## 3. ADIM 1 — GERİYE BAKIŞ (yalnız KEŞİF: ABD 2016-19)
- Y10 = 1 olan hisse-günler ile eşli kontroller (aynı gün, aynı ATRP beşliği, Y10 = 0; olay başına 5 kontrol, tohum 28): her özellikte standartlaştırılmış ortalama farkı ve AUC; ay kümeli bootstrap.
- Her özellik için YÖN (yükseliş öncesinde büyük mü küçük mü) ve kesimler (uç %10 ve uç %2; beşlikler) YALNIZ keşiften belirlenir ve YO_KESIM.md'ye yazılır.
- Piyasa düzeyi: YP = 1 günleri ile öteki günler için aynı karşılaştırma (ay kümeli).

## 4. ADIM 2 — İLERİYE DOĞRU SINAMA (keşif kesimleriyle; doğrulama ABD 2020-22 ve AVR)
- OYNAKLIK TUZAĞI (K60 dersi; zorunlu): 'yukarı +%10' olasılığı oynaklıkla mekanik artar. Bu yüzden her ölçü ATRP beşliği İÇİNDE okunur: KAT = P(Y10 | uç, ATRP beşliği) / P(Y10 | ATRP beşliği), beşliklerin olay ağırlıklı ortalaması; ASİMETRİ = [P(Y10) - P(D10)] uçta eksi aynı ATRP beşliğinde tabanda; TOPLAM FARK = R15 - aynı hissenin aynı dönemdeki bütün günlerinin R15 ortalaması; SEÇİM = R15 - P15(t).
- Çıkarım: ay kümeli bootstrap %95 (10.000; tohum 28); her satırda n, farklı ay, en kalabalık 3 ay payı. Aile = (8 yeni özellik ailesinin sütunları + kontroller) x 2 uç; BH q 0,10 doğrulama p'lerine.
- HÜKÜM (satır başına): 'TUTAR' <=> keşifte ve ABD 2020-22'de KAT > 1 ve alt ucu > 1 VE ASİMETRİ > 0 ve alt ucu > 0 VE TOPLAM FARK > 0 ve alt ucu > 0 VE BH'yi geçer VE AVR'nin iki döneminde üç ölçünün işareti aynı yönde. 'YALNIZ OYNAKLIK' = KAT ham olarak > 1 ama ATRP içinde değil ya da ASİMETRİ <= 0. 'TEK DÖNEM', 'TERS', 'TUTMADI', 'ÖLÇÜLEMEDİ' (n < 1.000 ya da farklı ay < 12) ayrıca.
- KONTROLÜ GEÇME ŞARTI: TUTAR çıkan yeni özellik, MOM_12_1 + F15 + KONUM120 + ATRP ile kurulan basit lojistik modelin puanı sabit tutulunca (puan beşliği içinde) hâlâ KAT > 1 veriyor mu; vermiyorsa 'BİLİNENİN TEKRARI'.
- BİRLEŞİM (en çok iki özellik; yalnız tek başına en az TEK DÖNEM olanlardan; keşifte seçilir, doğrulamada bir kez sınanır) ve BASİT PUAN (keşifte L1 lojistik; doğrulamada üst %10 / %2): karmaşık olan en iyi tek özelliği geçmiyorsa seçilmez.
- PİYASA TAHMİNİ: piyasa özelliklerinin uç %10 günlerinde P(YP), P(DP) ve P15 ortalaması; taban ile fark (ay kümeli; dönemler ayrı); hüküm kuralı aynı kalıpla (KAT, P(YP) - P(DP) asimetrisi, P15 farkı; iki dönem + AVR yön).
- GENEL: en az bir satır TUTAR ve KONTROLÜ GEÇER ise 'AÇIK VERİDE ADAY (kasa açılmaz; KASA KURALI: tek iz kasa açmaz; ileri test)'; aksi halde 'YÜKSELİŞ ÖNCESİNDE AYIRT EDİCİ ÖZELLİK BULUNAMADI (bu özellik kümesinde)' ve en yakın üç satır + sıradaki üç deneme yazılır.
- Evren bugün yaşayanlar: yukarı yanlı; iki taraf için de geçerli.

## 5. Çıktılar
YUKSELIS_ONCESI.py, test_yukselis_oncesi.py; arastirma_cikti/yukselis_oncesi/: YO_ON_KAYIT.md, YO_KESIM.md, YO_RAPOR.md (OLASILIK TABLOSU: satır = özellik x uç; sütunlar = keşif ve doğrulamada n, P(Y10), taban, KAT [aralık], ASİMETRİ, TOPLAM FARK, hüküm), yo_sonuc.json, yo_ozet.csv; Cemal için tek sayfalık görsel YO_OZET.png (telefon; düz dil: 'yükselişten önce en çok ne vardı' sıralaması ve 'ileriye doğru sınayınca hangisi tuttu'). Büyük panel dosyaları repoya girmez (/root/.kasa/ham/yukselis_oncesi; raporda yol + sha256).
