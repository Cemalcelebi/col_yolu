# MUM_IZI EK 16 — İŞ B sayfa raporu (26 Kasım 2026)

İş tanımı: MUM_IZI16_IS_TANIMI.md, bölüm 0 ve 2 (B1-B5). Bu iş yalnız ÇİZİM altyapısıdır: ölçüm / getiri / sonrası yok; İŞ A dosyalarına (MUM_IZI_GOZ2.py, test_mum_izi13.py, mum_izi16_*) dokunulmadı.

## Sonuç

- Yeni seçenek: `python MUM_IZI_HAKEM.py onay --hakem <A> <B> <C> <D> --hakem2 <hakem2> --aday <aday klasörü> --ad MUM_IZI14 --kapak "<eski kapak, aynen>" --olcek [--cikti KLASÖR]`
  Çıktı: `<ad>_ONAY_OLCEKLI.pdf` + `<ad>_onay_olcekli.json`. Eski `<ad>_ONAY.pdf` / `<ad>_onay_anahtar.json` yalnız okunur.
- `--olcek` verilmezse kod yolu hiç değişmedi (eski `_hk_sayfa` / `hk_onay` gövdesi aynen); MUM_IZI12 ve MUM_IZI14 onayları yeniden kuruldu, PDF sha'ları mühürlüyle birebir (test).
- B1 yüzde ekseni: sağda, 0 = bölgenin son kapanışı (kalın çizgi); adım {0,1 0,2 0,25 0,5 1 2 2,5 5 10 20 25 50 100 200 250 500} içinden 4-8 çizgi veren en küçüğü; ince noktalı kılavuz. Fiyat / tarih / hisse yok.
- B2 sağlam sınır: pencere barlarının O/H/L/C %2-%98 dilimi ∪ bölge barlarının L/H'si, ±%4 pay. Bölgedeki Bollinger bandı için çerçeve her yönde en çok bu açıklığın %15'i kadar genişler (bkz. SAPMA). Taşan mum: koyu kırmızı ▲/▼ (her kesilen mumda); taşan bant: mor ▲/▼ (her kesik parçada bir).
- B3 alt satır: 'Bölgede ortalama mum boyu: %x · bu hissenin önceki 120 mumunda: %y' + 'oran z'. Tanım İŞ A ile aynı: (H-L)/C medyanı; önceki = bölge başından önceki en çok 120 bar, en az 40 (yoksa 'yetersiz', oran yok; 40-119 bar varsa satırda gerçek sayı yazılır). Yalnız bölge sonu t'ye kadarki barlar: fonksiyon diziyi t+1'de keser, assert + test (t'den sonraki barlar bozulunca sonuç ve sayfa ölçü kaydı aynı).
- B4 üç kutu: '✓ benziyor', 'K kısmen', '× benzemiyor' (her biri sayfa genişliğinin ~%29'u; yalnız --olcek sayfasında).
- B5 set: MUM_IZI14_ONAY_OLCEKLI.pdf, 18 sayfa (kapak + 17), sha 79aef4477c0f9b2212b18a532001c048dc1d3eee8e60ab0254fac4aca63fda4f; aynı 17 bölge, aynı sayfa sırası ve 'Sayfa N' numaraları. Kapılar (DUR): eski anahtar var; hakem / 2. hakem / aday anahtarı sha'ları eski anahtardakiyle aynı; eski PDF sha = anahtardaki pdf_sha; kapak eski kapakla aynı; seçim yeniden kurulunca her sayfanın bölge kimliği (yeni_sayfa, aday_sayfa, zaman, pazar, sembol, bolge_bas, bolge_son, pencere) eski anahtarla birebir. Kapak = eski kapak + 'Bu sürümde sağda yüzde ekseni var: mumların gerçek boyu görünür. Önceki (ölçeksiz) dosya yerine bunu işaretle. Kısmen için K kutusu eklendi.'
- MUM_IZI14_onay_olcekli.json: yeni pdf sha, eski anahtar sha (7f783321…6474, değişmedi), eski pdf sha (584b0db8…9bf7, değişmedi), bölge kimliği eşit = true, eşik sha, sayfa başına ölçüler (boy, önceki, oran, eksen adımı, kesilen sayıları). Hisse adı / tarih yok (test).
- 17 bölgede B3 sayıları: mum boyu %1,76 / %6,23 / %18,42 (en küçük / medyan / en büyük); önceki %1,76 / %5,88 / %15,64; oran 0,71 / 0,97 / 1,98 (16 bölge; 1 bölgede önceki 23 bar < 40, oran yok). İŞ A'nın BOY_MUTLAK / BOY_OZ sayılarıyla sonradan karşılaştırılacak.
- Göz sağlaması (PNG, 80-110 dpi; eski PDF'in aynı sayfalarıyla yan yana): 
  - Günlük bir sayfa: eski sayfada bölge öncesindeki alt bant çerçeveyi aşağı çekmiş, mumlar sayfanın üst üçte birine sıkışmıştı; yeni sayfada mumlar çerçeveyi dolduruyor, eksen -%15..0 (adım 2,5), taşan alt bant tek mor işaretle.
  - Haftalık bir sayfa: eski sayfada bölge öncesindeki iki dev fitil (yukarı / aşağı) ölçeği ezmiş, bölge mumları çizgi gibiydi; yenide iki fitil kesik ve koyu kırmızı ▲ / ▼ ile işaretli, bölge mumları okunur, eksen -%20..+%20.
  - Haftalık bir sayfa (sert düşüş sonrası): ölçek eskisine yakın, eksen -%60..+%60 (adım 20); bölgede mum boyu %15,6 ile satırda yazılı.
  - Üçünde de turuncu bölge kutusu aynı barları kapsıyor (kutu bölge barlarının L-H açıklığı; bölge barı hiçbir zaman kesilmez), üç kutu var, eksen yazıları 14 pt, alt satır 14 pt.

## Testler

test_mum_izi10.py: 25 / 25 (19 eski + 6 yeni): mum boyu tanımı ve geleceğe bakmama; sağlam sınır (bölge dışı dev fitil kesilir, bölge içi kesilmez, bant genişlemesi sınırlı) ve eksen adımı (6.400 açıklıkta 4-8 çizgi, 0 dahil); sayfa çizimi geleceğe bakmaz; --olcek olmadan MUM_IZI14 onayı birebir (pdf sha + anahtar sayfaları); ölçekli basım uçtan uca (18 sayfa, kimlik eşit, json'da hisse / tarih yok, pdf sha = repodaki json; dört kapı DUR: çıktı var, kapak farklı, kimlik farklı, hakem dosyası eksik; eski anahtar sha değişmez); repodaki ölçekli dosyalar (sha'lar, mühür sabitleri). Çakışma kapısı testi geçer.

## KONTROL LİSTESİ

| Madde | Durum | Kanıt / gerekçe |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm yok; yalnız sayfa çizimi |
| K2 geleceğe bakma | EVET | sayfa ve B3 sayıları yalnız t'ye kadarki barlar (`d.iloc[:t+1]`, `hk_boy_olcu` assert); test: t sonrası bozulunca sonuç aynı |
| K3 geçerli bar | EVET | (H-L)/C sonlu değilse ya da C <= 0 ise dışarıda; H = L / hacim 0 barı ayrıca atılmaz (İŞ A tanımıyla aynı kalsın diye; bkz. kısıt) |
| K4 tekilleştirme | UYGULANMAZ | set değişmedi (17 bölge, eski anahtarla birebir) |
| K5 giriş fiyatı | UYGULANMAZ | getiri yok |
| K6 veri birimi | EVET | yüzde ekseni ve boy oranı birimden bağımsız (oran); veri mevcut mv_veri ile |
| K7 hayatta kalma | UYGULANMAZ | ölçüm yok |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok; 17 bölgenin sayıları yalnız betimleme |
| K9 ön kayıt | EVET | sayfa kuralı iş tanımında (9f81e38) önceden; eşikler HK_ESIK_OLCEK'te, sha json'da |
| K10 ayrıştırma | EVET | bölge kimliği eski anahtarla alan alan denetlendi; 3 sayfa + kapak gözle |
| K11 yeniden üretim | EVET | ölçekli PDF iki ayrı koşuda aynı sha; test yeniden kurup repodaki sha ile karşılaştırır |
| K12 ifade | EVET | sayfada yorum / beklenti yok; B3 satırı yalnız tanım |
| K13 süreç | EVET | çakışma kapısı korundu; yasak dosyalara ve İŞ A dosyalarına dokunulmadı; yalnız kendi yollar; mühür dosyaları sha ile önce / sonra aynı; e-posta / anahtar yok |
| K14 boyut | UYGULANMAZ | öneri işi değil |

Kod değişti: Colab'da kullanılacaksa çalışma zamanını yeniden başlat.

## SAPMA

- B2: iş tanımı sınırı yalnız barlarla kurar ('bunu aşan bantlar kesilir'). Harfiyen uygulanınca 17 sayfanın çoğunda bölgedeki alt ya da üst bant çerçeve dışında kaldı (ör. bir sayfada bölgenin alt bandı tümüyle kesik); kalıbın bant ölçütü ('daralma', 'üst bandı alttan izleme') görünmez oluyordu. Çözüm: bölgedeki bant için çerçeve her yönde en çok %15 genişler (mum ölçeği en çok ~%30 küçülür); bundan fazlası yine kesilir ve işaretlenir. Bu yüzden dev fitil kesimi 17 sayfanın 2'sinde kaldı (ilk, harfiyen sürümde 13'ünde birkaç fitil kesiliyordu). Ana model isterse `bant_pay` = 0 ile harfiyen sürüm üretilir (tek eşik).
- Adım listesi: 'yuvarlak' adım için 7,5 / 1,5 / 3 gibi adımlar ilk denemeden sonra çıkarıldı (sayfa görülmeden önce eşik değil, gösterim kararı).

## HATA

- Test hatası (düzeltildi): uçtan uca testte json'da 'sembol' sözcüğü aranıyordu; json'daki 'bolge_kimligi.alanlar' listesi alan adı olarak 'sembol' içerdiği için test kaldı. Hisse adı sızıntısı yoktu; test sayfa kayıtlarında 'sembol' anahtarı ve 17 hisse kodunun json'da geçmemesi olarak düzeltildi.
- İfade: B3 satırındaki 'ortalama mum boyu' sözü iş tanımındaki metindir; hesap medyandır (İŞ A tanımı). Ana model isterse 'tipik' ya da 'ortanca' olarak değiştirilebilir.

## Kalan kısıt

- Eksen yazıları 14 pt (A4 genişliğinde); telefonda sayfa genişliğine sığdırınca okunur ama küçük; daha büyük yazı için grafik daralır.
- Bant kesilen sayfalarda (bölge dışı) mor işaret parça başına bir tane; bandın nereye gittiği görünmez.
- H = L (kilitli) barlar B3 hesabında 0 boy olarak kalır (İŞ A ile aynı tanım için); BIST tavan / taban serilerinde boyu küçük gösterebilir.
