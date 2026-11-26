# MUM_IZI9 ÖN KAYIT (2026-11-26T08:52:03Z)

v6 = v5M ∧ K* ∧ D* ∧ BB* (Cemal: 'Mumlar küçük olmalı, dizilim muntazam olmalı, Bollinger daralması net olmalı'). Aday ölçüler ve eşik kuralı iş tanımında; eşikler etiketlere (iç örnek) oturtuldu. Bu dosya evren taramasından ve PDF'ten ÖNCE commit edilir; sonra kural değişmez.

## Mühürler

KOD9_SHA: 2129b71d2f4da6ad5f4f468d23626eaeca59039b882baeced8c8b5902e0fb116
ESIK9_SHA: 233dd7539de8faa111aee24f87739a78e888e310f6a536bf5d5ad81313d52cb1
ADAY9_SHA: fbd7655567a558ab9664117388eeccb5434675b82b190776b9dd4ec8be7dffe2
SENTETIK9_SHA: 4ee96f910c2e970a6a3fff422e65da1089b87866d19159d446fd576ceaa3ebf0
V5_KOD_SHA: 2bd267ad5057ef6e5571b92545224b3ce4a2ce0702b295653553237c9a62a6d3
V4_KOD_SHA: 6b3e2e4fa74f9cde3b4e99c1b47c8f4b9c31765cc604d478e5699bf2768cafbe
V3_KOD_SHA: 70fc2fb979c47b2a2bd5fb260e1fb1891e7b34268f49c4a4276f482b66a4eb69
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
E6_KOD_SHA: cc8c6c914d7ecaa02682eb9c302e63635e567a1d828f7416a0cbb6bdeb291f1d
ISARET8_SHA: 35fa2d718a76da2e5dbb5517465429d0f858d38a41bae17907b8e22b061d27bb

- MUM_IZI_V6.py commit'i: a42bcb0291c5ab723eebb5b6609138991c5d3076 2026-11-26T08:52:01+00:00

## Etiket kümesi: {"EVET": 6, "HAYIR": 18, "EVET_kaynak": {"set1": 3, "set3": 2, "set2": 1}, "HAYIR_kaynak": {"set3": 17, "set1": 1}, "set3_isaret": {"HAYIR": 17, "YOK": 4, "EVET": 2, "IKISI": 1}}

## Aday tablosu

| aday | yön | EVET min-maks | HAYIR medyan | şablon | eşik | reddedilen HAYIR payı |
|---|---|---|---|---|---|---|
| K1 | kucuk | 0.380..0.930 | 0.796 | 0.789 | 0.977 | 0.39 |
| K2 | kucuk | 0.177..0.396 | 0.197 | 0.303 | 0.415 | 0.00 |
| K3 | kucuk | 0.540..1.084 | 1.169 | - | 1.138 | 0.56 |
| K4 | kucuk | 0.015..0.570 | 0.602 | 0.789 | 0.829 | 0.06 |
| D1 | kucuk | 0.390..1.063 | 0.754 | 0.729 | 1.116 | 0.17 |
| D2 | buyuk | 0.633..0.893 | 0.720 | 0.811 | 0.602 | 0.00 |
| D3 | buyuk | 0.633..0.897 | 0.755 | 0.938 | 0.601 | 0.44 |
| D4 | kucuk | 0.276..1.349 | 0.402 | 0.966 | 1.416 | 0.00 |
| BB1 | kucuk | 0.122..0.838 | 0.781 | 0.708 | 0.880 | 0.33 |
| BB2 | kucuk | 0.115..0.700 | 0.438 | 0.603 | 0.735 | 0.06 |
| BB3 | kucuk | 0.008..0.742 | 0.412 | - | 0.779 | 0.11 |
| BB4 | ikili | 1.000..1.000 | 1.000 | 1.000 | 0.500 | 0.39 |

- Seçim: {"K": {"aday": "K3", "puan": 0.5555555555555556, "esik": 1.1377839406057206}, "D": {"aday": "D3", "puan": 0.4444444444444444, "esik": 0.6010556825199288}, "BB": {"aday": "BB4", "puan": 0.3888888888888889, "esik": 0.5}}
- v6 kapıları: {"K": {"aday": "K3", "esik": 1.1377839406057206, "yon": "kucuk"}, "D": {"aday": "D3", "esik": 0.6010556825199288, "yon": "buyuk"}, "BB": {"aday": "BB4", "esik": 0.5, "yon": "ikili"}}
- v6'nın birlikte reddettiği HAYIR payı: 0.889; EVET'lerin geçen payı: 1.000; durum: SEÇİLDİ
- Bilgi (set bazında v5M / v6 VAR ve Cemal'in yanıtı): {"set1": {"n": 24, "v5M_VAR": 4, "v6_VAR": 3, "v6_VAR_isaret": {"EVET": 3}, "v5M_VAR_isaret": {"EVET": 3, "HAYIR": 1}}, "set2": {"n": 37, "v5M_VAR": 1, "v6_VAR": 1, "v6_VAR_isaret": {"EVET": 1}, "v5M_VAR_isaret": {"EVET": 1}}, "set3": {"n": 24, "v5M_VAR": 24, "v6_VAR": 7, "v6_VAR_isaret": {"EVET": 2, "HAYIR": 2, "YOK": 2, "IKISI": 1}, "v5M_VAR_isaret": {"HAYIR": 17, "YOK": 4, "EVET": 2, "IKISI": 1}}}
- Şablon ölçüleri: {"k": 10, "K1": 0.7890791431569915, "K2": 0.3032373073512843, "K3": null, "K4": 0.7890791431569915, "D1": 0.7293004201905527, "D2": 0.8113189862819669, "D3": 0.9381469987618788, "D4": 0.9656602630813793, "BB1": 0.7082396961212073, "BB2": 0.6030531990973897, "BB3": null, "BB4": 1.0}

## Sentetik (v6)

- pozitif VAR: {'0.0': 0.44125, '0.1': 0.39, '0.2': 0.23} (bağlam {'dip': 0.4625, 'yatay': 0.245}; v5M 0.450)
- n1: kendi ölçüsü B (v5) ihlal payı 99.7 % -> GEÇERLİ; VAR 0.0 %
- n2: kendi ölçüsü M ihlal payı 100.0 % -> GEÇERLİ; VAR 0.0 %
- n5: kendi ölçüsü T ihlal payı 98.9 % -> GEÇERLİ; VAR 0.2 %
- n8: kendi ölçüsü çıkış gövdesi >= 1,2 (b) ihlal payı 86.0 % -> GEÇERLİ; VAR 23.4 %
- n9: kendi ölçüsü BB* ihlal payı 53.5 % -> KURGU GEÇERSİZ; VAR 21.4 %
- n10: kendi ölçüsü D* ihlal payı 53.0 % -> KURGU GEÇERSİZ; VAR 24.0 %
- rastgele: {'blok': {'n_bar': 205200, 'tekil': 38, 'VAR_1000': 0.18518518518518517}, 'ry': {'n_bar': 205200, 'tekil': 59, 'VAR_1000': 0.2875243664717349}}
- KABUL ÖLÇÜTÜ: GEÇMEDİ {"poz_g10": false, "neg": {"n1": true, "n2": true, "n5": true, "n8": false, "n9": "geçersiz kurgu (sayılmaz)", "n10": "geçersiz kurgu (sayılmaz)"}, "rastgele": {"blok": true, "ry": true}, "gecti": false}

## Uygulama kararları (iş tanımında açık bırakılanlar)

1. Bant genişliği K2 / BB1 / BB2 / BB3'te tam genişlik (üst bant - alt bant); 'b birimi' (K1, K4, D1) yarı genişlik (üst bant - SMA). BB3'te göreli genişlik = tam genişlik / SMA.
2. K3: bölge öncesi 60 bar (en az 20; yoksa tanımsız -> kapıyı geçmez). BB2: [max(19, bölge başı - 20), bölge sonu]; şablonda yalnız 20 mum. BB3: en dar günün o güne kadarki son 120 barı (geçerli en az 20), 'değer <= o gün' payı.
3. D1 adımları i = k..m-1 (çıkış mumunun kendi adımı dahil), her adım o mumun yarı genişliğiyle bölünür. D3 / D4 tırmanış = k+1..m-1 (en az 3 mum). D2 bölgenin bütün ardışık çiftleri.
4. Eşik: 'küçük iyi' en büyük x 1,05, 'büyük iyi' en küçük x 0,95 (çarpımsal %5). Tanımsız HAYIR ölçüsü 'reddedildi' sayılır; tanımsız EVET ölçüsü varsa aday geçersiz (olmadı).
5. Etiket kümesi doğrulandı: EVET 6 (MUM_IZI8 s5 / s8 + set 1'den 3 + set 2'den 1), HAYIR 18 (MUM_IZI8'den 17 + set 1'den 1). MUM_IZI8 sayfalarında anahtardaki k ile yeniden hesaplanan k ve v5M VAR birebir; önceki 61'de v5M mum_izi8_aday.csv ile birebir.
6. Tarama: bir son, bir uzunlukta v5M VAR VE seçilen kapılar geçiyorsa v6 VAR; tekil < 15 mum en yüksek v1 S. v5M'ye oran MUM_IZI8 taramasının (mum_izi8_tarama.json) sayılarıyla.
7. Onay: önceki ÜÇ setin (MUM_IZI4 / 6 / 8) hisseleri hariç; tohum 25112093; sayfa 1 kapak, 2 şablonda okuma, bölgeler 3'ten.
8. Sentetik n8: iş tanımındaki 'sentetik bantta ölçülerek kurulur' gereği KAT 6 / 9 / 13,5 / 20 sırayla (aynı tohum) denenir; ilk sürüm sabit 6 kattı ve kendi ölçüsünde %72,6'da geçerliydi (sayılmazdı); ölçerek kurulunca %86 (GEÇERLİ). Bu değişiklik ön kayıttan ÖNCE, n8'in VAR payına bakılarak değil kurgu tanımına göre yapıldı (iki koşunun VAR payları: 6 kat %27,1, ölçerek %23,4; ikisi de > %10).
9. n9 / n10 kendi ölçüsünde geçersiz çıktı (%53,5 / %53,0): seçilen BB* (BB4 = en dar noktanın yeri) 'daralma var mı / ne kadar' ölçmüyor, seçilen D* (D3 = kapanış yolunun doğrusallığı) aynı kapanış yolunu koruyan dağınık mum boylarını görmüyor. Bunlar kuralın zayıflığıdır; kural değişmez, raporda yazılır.

## Uyarılar (ön kayıtta yazılı)

- Eşikler 6 EVET sayfasına oturtuldu (iç örnek): v6'nın HAYIR'ların %89'unu reddetmesi ve EVET'lerin hepsini geçirmesi tanım gereği iyimser; gerçek sınama Cemal'in MUM_IZI9_ONAY işaretleri.
- 'Net Bollinger daralması' için seçilen ölçü BB4 (en dar noktanın bölgenin ortasında olması) daralmanın şiddetini ölçmüyor; şiddet ölçüleri BB1 (%33), BB2 (%6), BB3 (%11) daha az HAYIR reddetti.
- 'Küçük mum' için seçilen K3 (bölgenin medyan mum boyu / önceki 60 bar) tek dev çıkış mumunu yakalamıyor (sentetik n8 %23 VAR; K4 çıkış gövdesi HAYIR'ların yalnız %6'sını reddetti).

## Kural ve eşikler (V6_ESIK; sha yukarıda)

```
{
 "surum": "V6-1.0",
 "taban": "v5M = MUM_IZI_V5 'R4+M' (Y ∧ G1 ∧ G2 ∧ T ∧ I ∧ M) aynen; k = çıkış mumu (pencerenin ilk SMA üstü kapanışı); tırmanış = k+1..m-1",
 "olcu": {
  "K1": "bölgedeki (bütün mumlar) en büyük gövde |C - O| / (üst bant - SMA) (b birimi)",
  "K2": "medyan mum boyu (H - L) / bant genişliği (üst bant - alt bant), bölgenin bütün mumları",
  "K3": "bölgenin medyan mum boyu / bölgeden önceki 60 barın medyan mum boyu (en az 20 bar; şablonda ölçülemez -> şablon şartından muaf)",
  "K4": "çıkış mumunun gövdesi |C_k - O_k| / (üst bant_k - SMA_k)",
  "D1": "çıkış + tırmanışta (i = k..m-1) en büyük kapanış adımı |C_i - C_i-1| / (üst bant_i - SMA_i)",
  "D2": "bölgede ardışık mum örtüşmesi ortalaması (MI 'ortusme': ortak aralık / küçük mum boyu)",
  "D3": "tırmanış kapanışlarının (fiyat) sıra numarasına doğrusal uyumu R²",
  "D4": "tırmanışta mum boyu (H - L) değişkenliği: std (ddof 0) / ortalama",
  "BB1": "bölge içi en dar bant genişliği / bölgenin ilk 3 mumundaki ortalama bant genişliği",
  "BB2": "bölge içi en dar bant genişliği / [max(19, bölge başı - 20), bölge sonu] aralığındaki en geniş bant genişliği (şablonda yalnız görüntüdeki 20 mum)",
  "BB3": "en dar noktadaki (bant genişliği / SMA) değerinin o güne kadarki son 120 bardaki (geçerli, en az 20) yüzdeliği (değer <= o gün payı; şablonda ölçülemez -> muaf)",
  "BB4": "en dar noktanın bölge içindeki yeri (sıra / (m - 1)) 0,25-0,90 arasında (ikili)"
 },
 "yon": {
  "K1": "kucuk",
  "K2": "kucuk",
  "K3": "kucuk",
  "K4": "kucuk",
  "D1": "kucuk",
  "D2": "buyuk",
  "D3": "buyuk",
  "D4": "kucuk",
  "BB1": "kucuk",
  "BB2": "kucuk",
  "BB3": "kucuk",
  "BB4": "ikili"
 },
 "esik_kurali": "eşik = EVET sayfalarının ve (ölçülebiliyorsa) şablonun EN KÖTÜ değeri, %5 payla gevşetilir: 'küçük iyi' -> en büyük x 1,05; 'büyük iyi' -> en küçük x 0,95; ikili (BB4) ancak bütün EVET ve şablon sağlıyorsa aday. Bir EVET sayfasında ölçü tanımsızsa (geçmiş yetersiz) aday GEÇERSİZ",
 "pay": 0.05,
 "puan": "eşikle reddedilen HAYIR sayfası payı (tanımsız ölçü = reddedildi); sözcük başına en yüksek puanlı TEK aday (eşitlikte listedeki ilk); puan < 0,15 -> o sözcükte kapı YOK",
 "puan_en_az": 0.15,
 "dur": "v6 (v5M ∧ seçilen kapılar) HAYIR sayfalarının yarısından azını reddediyorsa DUR (PDF yok)",
 "dur_pay": 0.5,
 "etiket": "EVET = Cemal'in BENZİYOR dediği v5M sayfaları: MUM_IZI8_ONAY 'EVET' + önceki 61 etikette v5M VAR olup EVET; HAYIR = MUM_IZI8_ONAY 'HAYIR' + önceki 61'de v5M VAR olup HAYIR; IKISI / YOK / BELIRSIZ karar dışı. Pencere: MUM_IZI8 sayfalarında anahtardaki (son, m) ve k; önceki 61'de sayfanın kendi penceresi",
 "kural": "bir son, uzunluklardan (16-24) birinde pencere v5M VAR VE seçilen kapıların hepsini geçiyorsa v6 VAR; kapı ölçüsü tanımsızsa geçmez",
 "sentetik": {
  "kok": 25112091,
  "tohum": 200,
  "gurultu": [
   0.0,
   0.1,
   0.2
  ],
  "baglam": [
   "dip",
   "yatay"
  ],
  "uretec": [
   "blok",
   "ry"
  ],
  "tol": 3,
  "negatif": {
   "n1": "fitilsiz büyük gövde (MV n1)",
   "n2": "fitiller ters (MV n2)",
   "n5": "aynı mumlar yatay yol (MV p1)",
   "n8": "tek dev mumla çıkış: çıkış mumu açılışı önceki kapanış, gövdesi şablonun en büyük gövdesinin KAT katı; sonraki mumlar aynı fazla kadar yukarı. 'Sentetik bantta ölçülerek kurulur': KAT 6 / 9 / 13,5 / 20 sırayla denenir (aynı tohum), gömülü pencerenin kendi k'sındaki gövde >= 1,2 b olan ilk KAT alınır (hiçbiri değilse 20) (kendi ölçüsü: çıkış gövdesi >= 1,2 b)",
   "n9": "daralmasız: kalıbın önündeki 25 barda fiyat hareketleri ve mum boyları 3 kat (oynak dönem; gömme birimi de büyür): kendi ölçüsü BB* (yoksa BB1) eşiği bozuluyor mu",
   "n10": "dağınık: aynı kapanış yolu, her mumun boyu (O / H / L kapanışa göre) U(0,5, 3) katla çarpılır (tohumla): kendi ölçüsü D* (yoksa D4)"
  },
  "kendi_olcu": {
   "n1": "B (v5)",
   "n2": "M",
   "n5": "T",
   "n8": "çıkış gövdesi >= 1,2 (b)",
   "n9": "BB*",
   "n10": "D*"
  },
  "dogrulama": "gömülü pencerenin kendisinde (sentetik bant), pencerenin kendi k'sıyla; tohumların >= %80'inde ihlal -> GEÇERLİ, yoksa sayılmaz",
  "gecerli_pay": 0.8,
  "n9": {
   "bar": 25,
   "kat": 3.0
  },
  "n8_kat": [
   6.0,
   9.0,
   13.5,
   20.0
  ],
  "n10": [
   0.5,
   3.0
  ],
  "yanlis": {
   "seri": 200,
   "n": 1000
  },
  "kabul_olcutu": "%10 gürültüde pozitif VAR >= %40; geçerli negatiflerde VAR <= %10 (bütün gürültüler); rastgele seride tekil VAR <= 0,5 / 1.000 bar",
  "esik": {
   "poz": 0.4,
   "neg": 0.1,
   "rastgele": 0.5
  }
 },
 "tarama": {
  "gunluk": [
   "2016-01-01",
   "2022-12-31"
  ],
  "haftalik": [
   "2001-01-01",
   "2022-12-31"
  ],
  "evren": "MUM_IZI8 ile aynı (ETIKET2 P2 / BIST maskeleri)",
  "tekil": "< 15 mum zinciri, en yüksek v1 S'li hiza",
  "sayim": "v6 VAR (evren içi ve hepsi) pazar x dilim; v5M sayısına oranı (MUM_IZI8 taraması)"
 },
 "onay": {
  "tohum": 25112093,
  "gunluk": 12,
  "haftalik": 12,
  "bist_tavan": 4,
  "en_az": 8,
  "secim": "evren içi tekil v6 VAR olaylarından RASTGELE; önce haftalık sonra günlük; hisse başına bir; önceki üç setin (MUM_IZI4 / 6 / 8) hisseleri hariç; BIST dilim başına <= 4; dilimde 12'den az varsa hepsi; toplam < 8 -> DUR",
  "sayfa": "MUM_IZI8_ONAY düzeni + yeni üç sayı (küçük mum, dizilim, daralma)",
  "esik": "24'ün >= 19'u ✓"
 }
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşik EVET'lerden, puan HAYIR'lardan (iç örnek; ezber riski raporda); negatifler kendi ölçüsünde doğrulanır; rastgele seri tabanı; getiri yok |
| K2 | geleceğe bakma | EVET | bütün ölçüler pencere sonuna kadarki veriyle (K3 önceki 60 bar, BB2 önceki 20 bar, BB3 o güne kadarki 120 bar); test: seri t'de kesilince aynı; veri <= 2022-12-31 + KASA |
| K3 | geçerli bar | EVET | geçerli bar; haftalıkta eksik haftalı pencere atılır; BIST medyan üstü; ABD / AVR P2 |
| K4 | tekilleştirme | EVET | tekil < 15 mum (en yüksek v1 S); etiketlerde her sayfa bir kez (tekrar sayfaları dışarıda) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok |
| K6 | veri birimi | EVET | ölçüler oransal / b birimi |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; yalnız sayım ve görsel onay |
| K8 | örneklem ve dönem | EVET | EVET 6 / HAYIR 18 civarı (raporda doğrulanır): çok küçük; eşikler EVET'lere oturtuldu, gerçek sınama yeni PDF |
| K9 | ön kayıt | EVET | MUM_IZI9_ON_KAYIT.md: KOD9, ESIK9, ADAY9, SENTETIK9 sha + eski kod sha'ları; v6_kapi tarama öncesi |
| K10 | ayrıştırma | EVET | etiket şeması v4_etiket_oku ile (bilinmeyen değer DUR); MUM_IZI8 sayfalarında anahtardaki k ile yeniden hesaplanan k aynı ve v5M VAR (denetim) |
| K11 | yeniden üretim | EVET | v6_olcu_duz: tek pencerede 12 ölçü düz döngüyle; etiket sayfalarında vektörlü / döngü aynı |
| K12 | ifade | EVET | seçim önceden yazılı kuralla; 'iz' sözü yok; iç örnek uyarısı |
| K13 | süreç | EVET | çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

(ön kayıt anında yok)
