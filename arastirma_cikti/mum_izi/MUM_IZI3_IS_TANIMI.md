# MUM_IZI EK 3 İŞ TANIMI — aynı kalıp HAFTALIK mumlarda, evrenler ayrı, sonrası; Cemal görecek (25 Kasım 2026)

Yazan: ana model. Cemal (25 Kas): "İz değil dediğin parmak izi kalıbına HAFTALIK mumlarda uyan bölgeleri çıkar; mümkünse ayrı evrende olsunlar; bu kalıba TAM uyan bölgelere sahip hisseler sonrasında ne yapmışlar, bakayım göreyim."

Kalıp = MUM_IZI birinci parmak izi (ORNEK_25Kas; tam L = 20 ve tepesiz L = 17 şablon). Günlük mumda İZ DEĞİL çıktı (Ç227). Bu iş aynı kalıbın haftalık mumda taranması ve sonrasının GÖSTERİLMESİDİR: ikinci bir bakış olduğu için sonuç BİLGİ'dir; kasa açılmaz (tek iz, KASA KURALI).

## Kurallar
- MUM_IZI_IS_TANIMI.md kuralları aynen (ön uçuş K1-K14, yasak defter dosyaları, yalnız kendi yollarını commit, veri <= 2022-12-31 assert, eşik oynanmaz). Şablon, 33 ölçü, benzerlik puanı S ve eşikler (tam 0,59 / tepesiz 0,56) AYNEN; haftalık için yeniden ayar YOK.
- TAM UYAN (önceden sabit) = S >= eşik + 0,10 (tam >= 0,69, tepesiz >= 0,66).
- Ön kayıt (MUM_IZI3_ON_KAYIT.md: haftalık bar tanımı, eşikler, hücreler, ufuk, eş, PDF seçim kuralı, kod sha, KONTROL LİSTESİ) tarama ve sonrası hesabından ÖNCE commit; kapı geçmeden koşu yok.

## 1. Haftalık bar
- Günlük açık veriden (aynı fiyat kipi): hafta = ISO takvim haftası; O = haftanın ilk geçerli gününün açılışı, H = en yüksek, L = en düşük, C = son geçerli günün kapanışı, V = toplam. Geçerli günü olmayan hafta yok sayılır; H > L olmayan hafta geçersiz (pencerede geçersiz hafta varsa pencere atılır).
- Bollinger (20, 2) ve SMA20 haftalık barlardan, yalnız o haftaya kadarki barlarla (K2). Pencerenin son haftası TAMAMLANMIŞ olmalı (son günü <= 2022-12-30 ve haftanın son işlem günü veride).
- Test (sentetik): günlük -> haftalık O / H / L / C / V doğru; yarım hafta; tatil haftası; veri t haftasında kesilince S(t) değişmiyor (prefix).

## 2. Evrenler (AYRI raporlanır) ve hücreler
- ABD ve AVR: TEZGÂH 2, P2 havuzu (bölge sonu gününde P2); BIST: V_BIST (bilgi).
- AYRI EVREN (günlük taramada hiç kullanılmayan örnek): bölge sonu 2001-2015 (ABD h0107 = 2001-07, h0815 = 2008-15; AVR aynı). KARŞILAŞTIRMA: bölge sonu 2016-22 (h1622; günlük taramayla aynı dönem, farklı zaman dilimi). BIST: verinin kapsadığı dönem(ler) aynı sınırlarla.
- Tekil: aynı hissede 15 hafta (ilk kalır).

## 3. Sonrası (BİLGİ)
- Giriş = bölgenin son haftasından sonraki ilk geçerli günün açılışı (K5). Ufuk 15 HAFTALIK mum (UFUK 15 MUM kuralı, mumun kendi zaman diliminde): R15h = 15. haftalık barın kapanışı / giriş - 1. Ayrıca 15 hafta içinde en yüksek (max High / giriş - 1), en derin (min Low / giriş - 1), +%5 / +%10 / +%20'ye stop'tan önce dokunma payı (stop = bölgenin en düşük Low'u x 0,98). 30 hafta R30h bilgi. Penceresi 2022-12-31'i aşan olay ölçülmez (sayısı yazılır).
- Eş: aynı giriş günü, aynı kova (CETVEL2 v2.2 konum eşi; >= 5 eş; aynı gün kalıp olayı olan hisseler dışlanır), AYNI takvim aralığında aynı ölçüler; eşli fark, SIRA, ay kümeli boot %95; plasebo şans tabanı 200 tekrar SAYIYLA. Hücre başına: n, ortalama, MEDYAN, olay vs eş. S >= eşik ve TAM UYAN ayrı satır.
- Etiket: c2 hükmü yazılır (TUTAR / TUTMADI / ÖLÇÜLEMEDİ; n < 30 'örneklem yetersiz'), ama bu ikinci bakıştır: BH aile = (tam, tepesiz) x (eşik, TAM UYAN) x hücreler; 'iz' sözü kullanılmaz. K7: evren bugün yaşayanlar (özellikle 2001-15'te yukarı yanlı; olaya ve eşe aynı biner).

## 4. Cemal'in göreceği dosya: MUM_IZI3_HAFTALIK.pdf
- Sayfa 1 (tek sayfa, düz dil): kaç bölge bulundu (evren x dönem), sonrası tablosu (olay vs eş: 15 haftada ortalama / medyan getiri, +%10 / +%20 dokunma payı, stop payı), bir cümle okuma.
- Sayfa 2: Cemal'in grafiği + kodun şablonu (bindirme).
- Sonra 40 bölge sayfası. SEÇİM KURALI (ön kayıtta; sonuca göre DEĞİL, yalnız S'ye göre): tam şablonda en yüksek S'li bölgeler: AYRI EVREN ABD 10 + AVR 6; 2016-22 ABD 6 + AVR 4 + BIST 6; + bütün eşleşmelerden rastgele 8 (tohum ön kayıtta). Aynı hisse en çok bir kez.
- Her sayfa: haftalık mum grafiği, bölge kutulu, Bollinger (20) + SMA20, bölgeden önce 40 hafta, sonra 30 hafta (veri kesiği aşılmaz; eksikse yazılır), hisse kodu + tarih AÇIK (kör set değil), S, sonrası 15 hafta getirisi ve eş ortalaması, en yüksek / en derin. Okunaklı (telefon): sayfa başına tek grafik.
- Ayrıca mum_izi3_olay.csv.gz: bütün eşleşmeler (pazar, sembol, bölge başı / sonu, şablon, S, tam_uyan, hücre, R15h, eş R15h, max, min, dokunma bayrakları).

## 5. Çıktılar
arastirma_cikti/mum_izi/: MUM_IZI3_ON_KAYIT.md, MUM_IZI3_RAPOR.md (SONUÇ, EVREN x DÖNEM tabloları, KONTROL LİSTESİ, HATA, SAPMA, ÖNERİLEN DEFTER SATIRLARI), mum_izi3_sonuc.json, mum_izi3_olay.csv.gz, MUM_IZI3_HAFTALIK.pdf. Kod: MUM_IZI.py'ye yeni alt komutlar (haftalik_hazirla / haftalik_kos / haftalik_pdf) ya da tek ayrı dosya MUM_IZI_HAFTALIK.py (MUM_IZI fonksiyonlarını içe aktarır); test eklenir.
