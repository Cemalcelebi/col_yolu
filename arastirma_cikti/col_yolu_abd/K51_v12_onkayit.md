# K51 v1.2 — ÖN KAYIT: K51 sonrası bağımsız denetim ve hipotez ayrıştırma (29 Ekim 2026, sonuç görülmeden)

Bu belge koşudan önce yazılıp git ile sabitlenir. Sonuç görüldükten sonra eşik, alt grup, rejim veya tanım değiştirilmez. Değişiklik gerekirse yeni sürüm numarasıyla ve gerekçesiyle eklenir.

## 0. İlkeler (Cemal'in 11 maddesi; hepsi kabul edildi)

- K51 kararı (**İZ DEĞİL**) bu çalışmayla değişmez. Amaç veri, ölçüm, rejim ve formasyon hipotezini ayırarak başarısızlığın nedenini belirlemektir. Yeni model yok.
- **2023 ve 2024-26 bağımsız test değildir** (K51'de görüldü). Üç dönemde birden (2016-22, 2023, 2024-26) tutma şartı yalnız **sağlamlık kontrolü**dür. Olumlu çıksa bile bulgu **KEŞİFSEL** etiketlenir.
- **İleri doğrulama dönemi (önceden tanımlı):** sinyal günü 2026-09-01 ve sonrası (fon krizi istisnası Cemal'in kararıyla kalkınca), etiketler 60 işlem günü sonra tamamlanır; ilk değerlendirme en erken Mart 2027, n ≥ 30 olunca. Bu dönem bu çalışmada hiç kullanılmaz.
- Her hipotez iki yönde de raporlanır (kuantum ilkesi): etki anlamlı eksiyse "TERS YÖN" yazılır; bu da bilgidir, karar değildir.

## 1. Veri ve evren (K51 ile aynı; değişiklik yok)

- Kaynaklar: V_ABD (bugün işlem gören, 1.410 yüklenen), K34 Yahoo (nakdi biten 1.435), K34 Tiingo (batan örneklemi 422; ağırlık 1,83). Evren girişi: V_ABD için seri başı; K34 için ilk SEC nakit pisti bildirimi (point-in-time). Fiyatlar 31.08.2026'da kesik.
- Likidite ve maliyet: K51 ile aynı (kapanış ≥ 1 $, 20 gün medyan işlem değeri ≥ 1 M$ ve pazar içi 20. yüzdelik üstü; komisyon tek yön %0,05; kayma = 0,25 × son 20 gün medyan gün aralığı, [%0,05, %2]; gidiş-dönüş iki kat).
- Etiket (birincil): üçlü bariyer +%20 / −%10 / 60 işlem günü; giriş sinyalden sonraki ilk açılış; gün içi High/Low; boşlukta açılış fiyatı; aynı gün ikisi = zarar ve "belirsiz" işaretli.
- Borsadan çıkış (ana senaryo): seri vadeden önce biterse son kapanışta çıkış; son 60 gün eksiyse ek −%30 (varsayımsal, Shumway 1997). Bu gerçek delist getirisi değildir.

## 2. Veri bütünlüğü denetimi (K51_VERI_DENETIMI.md)

- V1 Sayı uzlaşması: 3.267 işlenen tekil sembol (= 1.410 + 1.435 + 422), 2.752 en az bir gün likidite süzgecinden geçen sembol, 4 yinelenen K34 sembolü (BG, RDUS, SBGI, ZYME: **aynı kodu sonradan başka şirket (farklı CIK) almış**; yüklemede ikincisi atlanıyor). Tiingo dosyasında iki şirketin geçmişinin birleşip birleşmediği tarih aralığıyla denetlenir. Şirket kimliği (CIK) ile sembol kimliği ayrı sütunlarda yazılır.
- V2 Point-in-time evren tablosu: sembol, CIK (varsa), kaynak, evren girişi, girişin dayanağı, ilk / son fiyat günü, çıkış türü.
- V3 2016-20 eğitim evreni yalnız bugün işlem görenlerden oluşur; bu dönem için eksik evren doldurulmaz, etkisi hücre hücre raporlanır.
- V4 Çıkış sınıflaması (tahmin, kesin değil): seri 2026-08-01'den önce bitenler; son 60 gün getirisi ≤ −%50 ya da son kapanış < 1 $ → "batma benzeri"; son 60 gün ≥ 0 → "satın alma / birleşme benzeri"; arası "belirsiz çıkış". Tiingo örneklemi tam batan evreni değildir (438 / ~800 adayın 450'si çekilebildi).
- V5 Delist duyarlılığı: ek kayıp senaryoları −%30 (ana), %0, −%100; uygulandığı hisseler = serisi vadeden önce biten ve son 60 gün getirisi eksi olanlar; baz fiyat = serinin son kapanışı; uygulama günü = serinin son günü. Her senaryoda P1 / P2 / HT hücreleri yeniden hesaplanır.
- V6 Ham ve düzeltilmiş fiyat: Tiingo serilerinde (ham + düzeltilmiş ikisi de var) aynı olaylar ham fiyatla yeniden etiketlenir; etiket uyuşma oranı ve fark yazılır. Yahoo serileri yalnız düzeltilmiş olduğundan bu test yalnız Tiingo altkümesinde yapılabilir; sınır açıkça yazılır.
- V7 Eski ve yeni kod: 29 Ekim denetim düzeltmelerinden önceki sürüm **b3835d8** (v1.1 ön kayıt) ile düzeltilmiş sürüm (3346f03 ve sonrası) aynı veride koşulur; olay sayısı, etiket sayısı ve H1 hücreleri yan yana. Eski koşunun tam çıktısı saklanmadığı için yeniden üretilir; yeniden üretilemeyen kısım bildirilir.

## 3. Kırılganlık (K51_KIRILGANLIK.md)

- Kaynak grupları: hayatta kalan (V_ABD), sıkıntılı (K34 Yahoo), batan (K34 Tiingo). Bu bilgi hiçbir sinyal süzgecinde kullanılmaz; yalnız raporda ayrılır.
- Hisse katkısı: en çok katkı veren 20 hisse çıkarılınca fark; hisse başına eşit ağırlıklı fark; katkı dağılımı (ilk 10 / 20 / 50 hissenin payı).
- Yıllar 2023, 2024, 2025, 2026 (2026 kısmi: sinyal ≤ 05.06.2026, "kısmi" işaretli).
- Güven aralıkları: ay kümeli (ana) ve hisse × çeyrek kümeli (duyarlılık), ikisi de yazılır.
- Örtüşme: aynı hissede 60 gün içinde tekrar eden sinyal payı, aynı günde birden çok sinyal payı.

## 4. Hipotezler (K51_HIPOTEZ_KARARLARI.csv)

Ortak tanımlar:
- **İsabet farkı** = (1/n) Σ_i [ y_i − ȳ_kontrol(i) ], y_i ∈ {0,1} olayın üst bariyer etiketi, ȳ_kontrol(i) = olay i'nin eşleşmiş kontrollerinin y ortalaması (en çok 5 kontrol, eşit ağırlık). Aynı kontrol hisse-günü birden çok olaya düşebilir; bu kümelenme ay kümeli bootstrap ile aralığa yansır, ayrıca tekrar kullanılan kontrol payı raporlanır.
- **Net fark** = (1/n) Σ_i [ net_i − net̄_kontrol(i) ], net = brüt bariyer getirisi − gidiş-dönüş maliyeti (aynı kural olay ve kontrolde).
- **Eşleştirme** (yalnız sinyal günü bilinen bilgi): aynı gün t; likit (uygun) ve olay kümesinin kendisi dışında (aynı hisse ±40 gün); aynı 60 gün oynaklık ondalığı (gün içi); aynı 20 gün işlem değeri üçte biri (gün içi); |dd250 farkı| ≤ 0,10 (250 gün tepesinden düşüş); aynı trend işareti (kapanış SMA200 üstü / altı); sektör biliniyorsa aynı sektör. Adaylar arasından standartlaştırılmış (dd250, vol60, log_dv20, r60, ar20) uzaklığa göre en yakın 5. Hiç kontrol bulunamayan olay düşer; düşen pay, 1-4 kontrolle eşleşen pay ve kontrol tekrar kullanım payı raporlanır. Tohum 512; bootstrap 2000.
- **Karar koşulları (ayrı ayrı, hepsi gerekli, her dönemde):** n ≥ 30; isabet farkı ≥ +0,05; ay kümeli %95 alt uç > 0; net fark > 0. Dönemler: 2016-22 (geliştirme), 2023, 2024-26 (sağlamlık; bağımsız değil). "DESTEKLENİYOR (KEŞİFSEL)" = üç dönemde de tutar; "DESTEKLENMİYOR" = en az birinde tutmaz; "YETERSİZ ÖRNEKLEM" = bir dönemde n < 30 (olumlu karar çıkarılmaz; hücreler birleştirilmez); "TERS YÖN" = bir dönemde fark ≤ −0,05 ve üst uç < 0 (bilgi).
- **Çoklu test:** beş hipotez bir aile; her hipotezin 2023-26 (birleşik) tek yönlü bootstrap p'si Holm ile düzeltilir; karar koşullarına ek olarak Holm p < 0,05 aranır. Hiyerarşi: H-A ana hipotezdir; H-B ve H-C H-A'nın altındadır (H-A tutmasa da raporlanır ama "İZ" olamaz); H-D ve H-E bağımsızdır.

| Kod | Olay (giriş = ertesi açılış) | Kontrol | Yön |
|---|---|---|---|
| H-A | ÇEK: sert düşüş (60 gün dibi / önceki 190 gün tepesi ≤ −%35) + yataylaşma çekirdeği (dipte, savunma, dar bant); imza şartı YOK; hissede 40 günde tek | Eşleşmiş genel kontrol (ÇEK dışı likit hisse-günler) | ÇEK > kontrol |
| H-B | P1 (ÇEK + ≥ 3 imza: küçük mum, Bollinger daralması, doji artışı, hacim kuruması) | ÇEK içinden imza ≤ 1 olan günler (ES), aynı eşleştirme ama tarih ±10 işlem günü, en yakın 3 | P1 > ES (küçük mum ek bilgi taşır) |
| H-C | ÇEK ∧ hacim kuruması (hacim_ok = 1) | ÇEK ∧ hacim_ok = 0, öteki üç imza sayısı eşit, aynı eşleştirme ±10 gün, en yakın 3 | hacim kuruması > kurumama |
| H-D | HT: hacim ≥ 20 × önceki 20 gün medyanı ve gün getirisi ≤ −%9,5 (hissede 40 günde tek) | Eşleşmiş genel kontrol (H-A ile aynı yöntem) | HT > kontrol; ayrıca bağımsızlık: HT olaylarının aynı hissede önceki 60 günde ÇEK bulunan payı < %50 olmalı |
| H-E | P1, rejime göre | Eşleşmiş genel kontrol (H-A yöntemi) | Rejim sayısı 2, sinyal gününde bilinen: AYI = SPY kapanışı 200 gün ortalamasının altında, BOĞA = üstünde. Hücre = rejim × dönem; her hücrede n, etki, aralık; n < 30 "yetersiz". Rejimler birleştirilmez. |

- H-A için ek: eşleşmiş kontrol yerine K51 tabanı (aynı gün aynı oynaklık ondalığı ortalaması) da yazılır (bilgi).

## 5. Resmî cetvel (CLAUDE.md, 28 Ekim 2026 sürümü)

- FI_OLCUT (FON_IZI.py v1.39): giriş olay sonrası ilk açılış, r60 = 60. gün kapanışı / giriş − 1; eşli fark = r60 − aynı gün aynı 60 gün momentum beşlisi × likidite üçlüsündeki öteki hisselerin ortalaması; hücre tutar: n ≥ 30, ortalama eşli fark > 0 ve ay kümeli %95 alt uç > 0, sıra > 0,50, 10 yuvalı 60 gün portföy 200 rastgele portföyün %90'ından büyük. İZ = ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26 dört hücre. Evren: yalnız bugün işlem gören hisseler (FON_IZI eşli panel) — **bu, resmî cetvelin bilinen sınırlamasıdır**.
- K51 resmî cetvel sonucu (cy_fi_olcut.csv): P1, P2, HT için İZ DEĞİL. Bu çalışmada yeniden koşulmaz; beş hipotezin sonucu ayrı tabloda yazılır; ikisi karıştırılmaz. Hipotezler olumlu çıksa bile İZ için resmî cetvel ve ileri doğrulama gerekir.

## 6. Testler ve çıktı bütünlüğü

- test_col_yolu_abd.py'ye eklenir: eşleştirme yalnız sinyal gününe kadar bilgi kullanır (gelecek sızıntısı sentetik testi); eşleştirme tekrarı aynı tohumla aynı kontrolleri verir; sembol tekilliği; delist senaryoları (−30 / 0 / −100) beklenen getirileri verir; ham / düzeltilmiş etiket karşılaştırma fonksiyonu; maliyet hesabı; eski-yeni kod karşılaştırma fonksiyonu çalışır.
- Çıktılar (arastirma_cikti/col_yolu_abd ve Drive COLAB_VERILER/OUTPUT/COL_YOLU_ABD): K51_VERI_DENETIMI.md, K51_KIRILGANLIK.md, K51_ESLESMIS_KONTROL.csv, K51_HIPOTEZ_KARARLARI.csv, K51_TEKRAR_URETIM.md (kod commit'i, veri sürümü, parametreler, tohum, test sonuçları, dosya özetleri sha256).
