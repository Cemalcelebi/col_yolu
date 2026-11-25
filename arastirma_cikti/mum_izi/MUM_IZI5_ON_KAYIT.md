# MUM_IZI5 ÖN KAYIT (2026-11-25T14:28:03Z)

v3 tanımı Cemal'in sözünden ve iş tanımındaki sabit tanımdan kuruldu. Cemal'in işaret dosyası (cemal_mum_izi4_onay.json) ve işaretli PDF bu dosya commit edilene kadar AÇILMADI; iş tanımındaki sayfa numaraları tanımda kullanılmadı. Sınama (C) bu commit'ten sonra; sonra tanım değişmez.

## Mühürler

KOD5_SHA: 344943d3ce93ba65c658cd0192a51262c9fda9c4147176b191480f6b0e8eb06b
ESIK5_SHA: 0a46827a22295a4fb60c46233d036619a014bf40ab6899716c98f7ac5d19101c
DAGILIM5_SHA: 1f9e7a62dc27c4f742a67034f8971dfe12e078fb02e2cb3f86439834401b7dd5
SENTETIK5_SHA: 99d7f4b05ce7c97e813ec4be66a334c1a4e846ed55e4634eb1bea27576b9724c
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc

- MUM_IZI_V3.py commit'i: 27e440e292e4fa691eb2efc71fd3f92a444844ac 2026-11-25T14:27:51+00:00

## Uygulamada verilen kararlar (iş tanımında açık bırakılanlar; işaretlerden önce)

1. Yalnız 'tam' şablon (20 mum; Cemal'in kalıbı); 'tepesiz' şablon v3'te kullanılmaz. Pencere uzunlukları 16, 18, 20, 22, 24 (v1 tam şablonun uzunlukları); bir pencere sonunda en küçük D3 seçilir.
2. Mum başına b ölçüleri hissenin kendi m mumunda hesaplanır, sonra 20 konuma doğrusal yeniden örneklenir (ardışık ilişkiler 19 konuma); 0 / 1 'uzun üst fitil' bayrağı en yakın konumla.
3. Evreler ham konum oranıyla: ilk < 1/3, orta, son >= 2/3. 'Gövde SMA üstünde' = gövde ortası (bO + bC) / 2 > 0.
4. F1 = (konum başına |bC|, |bO|, |bH|, |bL| farkının ortalaması + 6 evre değerinin farkının ortalaması) / 2.
5. F2 = (4 dizinin (açılış - önceki kapanış, kapanış değişimi, gövde, açılış önceki gövdenin içinde mi) mutlak fark ortalaması + (1 - işaret uyumu)) / 2; işaret uyumu = (kapanış değişimi işareti aynı payı + gövde işareti aynı payı) / 2.
6. F3 = (4 dizinin (üst fitil, alt fitil b biriminde; üst / alt fitil mum boyuna oranla) mutlak fark ortalaması + (1 - 'uzun üst fitil aynı konumda' payı)) / 2; uzun üst fitil = üst fitil >= mum boyunun yarısı.
7. Şablonun b koordinatı görüntüden okunan bantlarla (mum_izi_mumlar BU / BO); hissede her mumun kendi gününe kadarki Bollinger (20, 2; std ddof 0). Üst bant = SMA ise pencere geçersiz.
8. tau ve %20 eşiği: her uzunluk için 4.000 rastgele gerçek pencere (toplam 20.000; ABD + AVR + BIST birleşik havuz, yerine koymadan düzgün); günlük 2016-22 tohum 25112051 + L, haftalık 2001-22 tohum 25112052 + L, eksik haftalı pencere atılır.
9. Aday = F1 <= q1 ve F2 <= q2 ve F3 <= q3 (aynı zaman diliminin dağılımı). D3 ağırlıkları 0,5 / 0,25 / 0,25. Tekil = aynı hissede birbirine < 15 mum aday sonları zinciri, en küçük D3.
10. Sentetik: kök 25112053, 200 tohum x (blok, ry) x (dip, yatay, tepe) x gürültü (0; 0,1; 0,2) (MI üreteci ve gömmesi: ölçek 0,5-2, esneme 0,8-1,2); başarı = gerçek pencere sonunun +-3 barında aday. n4 = aynı şablon mumları, gömmeden önceki 10 barda bar başına -%3 sert düşüş (doğal eğim silinir); n5 = MV 'p1' (aynı mum biçimleri, yatay kapanış yolu). Rastgele: 200 seri x 1.060 bar her üretici; tekil aday / 1.000 bar. Sentetikte tau / q günlük dağılımdan.
11. Sınama (C): sayfadaki bölgenin kendi penceresi (v2 anahtarındaki hisse, son tarih, m; zaman dilimi); AUC = P(D3 benziyor < D3 benzemiyor) + 0,5 eşit; tam permütasyon p (bütün etiket atamaları, tek yönlü); grup içi bootstrap B 5000 tohum 25112054. Aynı tablo F1, F2, F3, v1 S ve v1 bileşenleri için (bilgi). Sayfa numarası: anahtar PDF sayfası (3-26); işaret dosyası 24'ten büyük numara içeriyorsa PDF numarası, 3'ten küçük içeriyorsa bölge numarası (PDF - 2) sayılır; ikisi de değilse komut durur ve kaydırma elle verilir (SAPMA'ya yazılır).
12. Tarama (D; yalnız C hükmü UYUMLU / KISMEN): ABD / AVR P2 (MH.mh_p2; haftalıkta 2001-15 parçası p1, 2016-22 p2), BIST pencere sonu işlem değeri o günkü BIST medyanının üstünde. Onay: tohum 25112055, en küçük D3'ten hisse başına bir, günlük 12 + haftalık 12, BIST dilim başına <= 3, sayfa sırası karışık.

## v3 tanımı (MV3_ESIK; sha yukarıda)

```
{
 "surum": "MV3-1.0",
 "koordinat": "b = (fiyat - SMA20) / (üst bant - SMA20): SMA 0, üst bant +1, alt bant -1; her mum kendi günündeki Bollinger (20, 2; std ddof 0) ile, yalnız o güne kadarki barlar (MI.mi_bant); üst bant = SMA ise pencere geçersiz. Şablonda bantlar görüntüden (mum_izi_mumlar BU / BO)",
 "uzunluklar": [
  16,
  18,
  20,
  22,
  24
 ],
 "konum": 20,
 "eslem": "mum başına ölçüler hissenin kendi m mumunda hesaplanır, sonra konum oranıyla 20 konuma doğrusal yeniden örneklenir (ardışık ilişkiler 19 konuma); ikili bayraklar (uzun üst fitil) en yakın konumla",
 "F1": "konum dizisi: 20 konumda bC, bO, bH, bL ile şablon arasındaki mutlak farkların ortalaması (dizi farkı) VE evre farkı: mumlar konum oranıyla üçe ayrılır (ilk < 1/3, orta, son >= 2/3), her üçte birde ortalama bC ve gövde ortası SMA üstünde payı ((bO + bC) / 2 > 0); 6 değerin şablonla mutlak farkının ortalaması. F1 = (dizi farkı + evre farkı) / 2",
 "F2": "mumların birbirine göre açılış / kapanışı: konum başına açılışın önceki kapanışa göre yeri (bO_i - bC_i-1), kapanış değişimi (bC_i - bC_i-1), gövde (bC_i - bO_i), açılış önceki gövdenin içinde mi (0 / 1); dört dizinin şablonla mutlak farkı ortalaması A2; işaret uyumu U2 = (kapanış değişimi işareti aynı payı + gövde işareti aynı payı) / 2. F2 = (A2 + (1 - U2)) / 2",
 "F3": "fitil: konum başına üst fitil ve alt fitil b biriminde ve mum boyuna oranla (4 dizi), şablonla mutlak fark ortalaması A3; uzun üst fitil (üst fitil >= boyun yarısı) bayrağı aynı konumlarda payı U3. F3 = (A3 + (1 - U3)) / 2",
 "dagilim": {
  "n": 20000,
  "L": "her uzunluk (16 / 18 / 20 / 22 / 24) için 4.000 pencere, birleşik",
  "gunluk": {
   "uclar": [
    "2016-01-01",
    "2022-12-31"
   ],
   "tohum": 25112051
  },
  "haftalik": {
   "uclar": [
    "2001-01-01",
    "2022-12-31"
   ],
   "tohum": 25112052
  },
  "yontem": "MUM_IZI2 / v2 yöntemi: geçerli (hisse, pencere sonu) çiftleri ABD + AVR + BIST birleşik havuz, pencere başı >= 19, haftalıkta eksik haftalı pencere atılır; yerine koymadan düzgün; tau_k = F_k medyanı; aday eşiği q_k = F_k'nın 0,20 yüzdeliği"
 },
 "aday": "TELAFİ YASAĞI: pencere aday <=> F1 <= q1 VE F2 <= q2 VE F3 <= q3 (aynı zaman dilimi dağılımında en iyi %20)",
 "D3": {
  "agirlik": [
   0.5,
   0.25,
   0.25
  ],
  "tanim": "D3 = 0,5 F1 / tau1 + 0,25 F2 / tau2 + 0,25 F3 / tau3 (küçük = benzer); t'de uzunluklar içinde en küçük"
 },
 "tekil": "aynı hissede aday pencere sonları birbirine < 15 mum olan zincir = bir küme; olay = kümenin en küçük D3'lü hizası",
 "sentetik": {
  "kok": 25112053,
  "tohum": 200,
  "gurultu": [
   0.0,
   0.1,
   0.2
  ],
  "baglam": [
   "dip",
   "yatay",
   "tepe"
  ],
  "uretec": [
   "blok",
   "ry"
  ],
  "tol": 3,
  "negatif": {
   "n1": "fitilsiz büyük gövde (MV.mv_karsi_ornek n1)",
   "n2": "fitiller ters (n2)",
   "n3": "mumlar 2 kat (n3)",
   "n4": "AYNI şablon mumları, gömmeden hemen önce sert düşüş (10 bar, bar başına -%3; doğal eğim silinir): bant geniş ve çöküyor",
   "n5": "aynı mum biçimleri, yatay kapanış yolu (MV.mv_karsi_ornek p1)"
  },
  "n4": {
   "bar": 10,
   "egim": -0.03
  },
  "yanlis": {
   "seri": 200,
   "n": 1000
  },
  "kabul_olcutu": "%10 gürültüde pozitif aday payı (gerçek sonun +-3 barında aday) >= %70 (üç bağlam x iki üretici birleşik); n1-n5 her birinde aday payı <= %5 (bütün gürültüler birleşik); rastgele seride tekil aday <= 0,5 / 1.000 bar (iki üretici ayrı). Geçmezse yazılır; tanım gevşetilmez / sıkılaştırılmaz",
  "dagilim": "sentetikte tau ve q günlük gerçek dağılımdan"
 },
 "sinama": {
  "etiket": "cemal_mum_izi4_onay.json 'isaret' alanı (ön kayıt commit'inden SONRA açılır; 24 sayfa) + mum_izi4_onay_anahtar.json (sayfa -> hisse / tarih / m / zaman)",
  "pencere": "sayfadaki bölgenin kendisi (aynı uzunluk m, aynı son); D3 ve aileler o pencerede",
  "auc": "P(D3 benziyor < D3 benzemiyor) + 0,5 eşit",
  "p": "tam permütasyon (C(n, n_benziyor) bütün etiket atamaları), tek yönlü",
  "boot": {
   "B": 5000,
   "tohum": 25112054,
   "tanim": "grup içi yeniden örnekleme"
  },
  "hukum": {
   "UYUMLU": 0.8,
   "KISMEN": 0.65
  },
  "bilgi": "aynı AUC v1 S (büyük = benzer) için; v2 bütün sayfaları kabul ettiği için ayırt edemez",
  "isaretsiz": "işaretsiz sayfa dışarıda"
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
  "evren": "ABD / AVR: TEZGAH2 P2 (giriş günü; MH.mh_p2); BIST: geçerli bar ve pencere sonu günü işlem değeri (C x V) o günkü BIST medyanının üstünde",
  "sayim": "aday (tekil) sayısı pazar x zaman dilimi; Cemal'in BENZİYOR sayfalarının medyan D3'ünden küçük D3'lü aday sayısı"
 },
 "onay": {
  "tohum": 25112055,
  "gunluk": 12,
  "haftalik": 12,
  "bist_max": 3,
  "once": 15,
  "secim": "evren içi tekil adaylar, en küçük D3'ten, hisse başına bir (iki zaman dilimi birlikte), zaman dilimi başına 12, BIST dilim başına en çok 3; sayfa sırası tohumla karışık; hisse / tarih / sonrası yok",
  "esik": "24'ün >= 19'u ✓ -> tespit GEÇERLİ; değilse v3 de geçersiz (karar Cemal'in)"
 }
}
```

## Dağılım (tau, en iyi %20 eşikleri)

- gunluk: n 20000, tau [0.6855, 0.4451, 0.3669], q20 [0.4874, 0.3978, 0.3285], rastgele pencerede aday payı 1.26 %, aile korelasyonları {'F1_F2': 0.22431129096068808, 'F1_F3': 0.0045219532605650795, 'F2_F3': 0.050620689488820904}
- haftalik: n 20000, tau [0.68, 0.4356, 0.3636], q20 [0.4874, 0.3887, 0.3275], rastgele pencerede aday payı 1.26 %, aile korelasyonları {'F1_F2': 0.24387868620302872, 'F1_F3': 0.011237800207083606, 'F2_F3': 0.04418828671181883}

## Sentetik (B; işaretlerden bağımsız)

- pozitif aday payı: {'0.0': 0.7208333333333333, '0.1': 0.7016666666666667, '0.2': 0.645} (bağlam {'dip': 0.95, 'tepe': 0.3575, 'yatay': 0.76})
- n1: aday 6.5 %
- n2: aday 26.1 %
- n3: aday 59.1 %
- n4: aday 98.0 %
- n5: aday 13.0 %
- rastgele: {'blok': {'aday_1000': 17.202729044834307, 'n_bar': 205200}, 'ry': {'aday_1000': 19.819688109161792, 'n_bar': 205200}}
- KABUL ÖLÇÜTÜ: GEÇMEDİ {'poz_g10_ge_70': True, 'neg_le_5': {'n1': False, 'n2': False, 'n3': False, 'n4': False, 'n5': False}, 'rastgele_le_05': {'blok': False, 'ry': False}, 'gecti': False}
- Okuma: pozitifler %10 gürültüde %70,2 ile ölçütü kıl payı geçiyor (dip bağlamında %95, tepe bağlamında %36); negatiflerin HİÇBİRİ <= %5 değil: n4 (sert düşüş sonrası aynı mumlar) %98, n3 (2 kat mum) %59, n2 (ters fitil) %26, n5 (yatay yol) %13, n1 (fitilsiz büyük gövde) %6,5; rastgele seride 17-20 tekil aday / 1.000 bar (ölçüt 0,5). Tanı (yalnız bilgi): 'en iyi %20' eşiği her ailede gevşek; üç aile birlikte rastgele gerçek pencerelerin %1,26'sını aday yapıyor. n4'te b dizisi şablonunkine dip bağlamındaki kadar yakın kalıyor: kalıbın kendi yükselişi bandı kendisi belirliyor, önceki sert düşüş b koordinatını beklendiği gibi kaydırmıyor.
- Kural gereği (iş tanımı B): ölçüt geçmedi diye tanım gevşetilmez / sıkılaştırılmaz; 'aday' kuralı ayırt etmiyor. C bölümü (işaretlerle sınama) D3 SIRALAMASINI sınar ve iş tanımındaki sırayla koşulur; D yalnız C hükmü UYUMLU / KISMEN ise. Sentetik geçmediği için D'de bulunacak 'aday' sayıları 'kalıbın tekrar sayısı' diye OKUNMAZ; yalnız 'dedektörün bulduğu bölgeler'.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | negatif kontroller sentetikte SAYIYLA (n1-n5 + rastgele seri), kabul ölçütü önceden; işaretlerle sınamada permütasyon p ve bootstrap aralığı; getiri / eş bu işte yok |
| K2 | geleceğe bakma | EVET | b koordinatı her mumun kendi gününe kadarki SMA / bant ile; pencere ölçüleri t'ye kadar; v3_prefix 30 olayda veri t'de kesilince D3 aynı; veri <= 2022-12-31 + KASA kapısı; işaretler ön kayıttan sonra açılır (git sırası raporda) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (MV.mv_haftalik_panel); BIST'te işlem değeri günlük medyan üstü |
| K4 | tekilleştirme | EVET | aynı hissede < 15 mum zincir = bir olay (kümenin en küçük D3'ü) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri hesaplanmaz |
| K6 | veri birimi | EVET | b birimi bant genişliğine oranlı, ölçek bağımsız; TEZGAH2 bölünme düzeltmeli fiyat |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; sayım ve görsel onay (getiri yok) |
| K8 | örneklem ve dönem | EVET | 24 etiketle (ana model 25 Kas: işaretsiz sayfa için sözlü yanıt; 'isaret' alanı) AUC: aralık geniş, raporda yazılır; sentetik 200 tohum / koşul; hüküm eşikleri önceden |
| K9 | ön kayıt | EVET | MUM_IZI5_ON_KAYIT.md: KOD5_SHA, ESIK5_SHA, DAGILIM5_SHA, SENTETIK5_SHA + MI / MH / MV sha; işaretler ön kayıt commit'inden sonra; v3_kapi kontrol + sha + git |
| K10 | ayrıştırma | EVET | işaretli sayfaların penceresi v2 anahtarındaki (sayfa -> hisse / tarih / m) pencereyle birebir; şablon v3 uzaklığı 0 (test) |
| K11 | yeniden üretim | EVET | v3_duz: 5 pencerede F1 / F2 / F3 düz döngüyle yeniden; AUC iki yoldan (çift sayım ve sıra toplamı) aynı |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı AUC eşikleriyle; 'iz' sözü yok; getiri yok |
| K13 | süreç | EVET | çakışma kapısı; v1 / v2 / defterler / UC_IZ2 değişmez; işaret dosyası mühürlü sırayla |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

- 25 Kas 14:22 (ön kayıttan ÖNCE): ana model işaretsiz kalan sayfa için Cemal'in sözlü yanıtını işaret dosyasına işledi (commit 062f14b) ve C'nin 24 etiketle koşulmasını istedi. Bu commit'in MESAJI ('işaretsiz sayfa 5 hiç benzemiyor') 'git log' ile görüldü: bir sayfanın etiketi ön kayıttan önce öğrenildi. O anda v3 tanımı ve sentetik kod (MUM_IZI_V3.py) yazılmış ve sınanmıştı; bu bilgiden sonra kodda yalnız işaret ayrıştırıcısının 'isaret' alanını öncelemesi ve '23 etiket' metinleri değişti; tanım (aileler, ağırlıklar, eşikler) değişmedi. İşaret dosyasının kendisi ve işaretli PDF açılmadı.
- K11 satırındaki '5 pencere' testte 6 pencere (test_vektor_duz_ayni).
- EK SAPMA (25 Kas 14:29, ön kayıt commit'i 04389a9'dan ve işaret dosyasının ilk açılışından (14:28:58Z) SONRA, sınamadan ÖNCE): işaret dosyası sayfa numarasını anahtar, değeri sözlük ({"sayfalar": {"3": {"isaret": "HAYIR", ...}}}) tutuyor; ayrıştırıcı (v3_etiket_oku) bu biçimi tanımıyordu ('çözülemedi' ile dururdu). Yalnız bu fonksiyona 2 satır eklendi (sayı anahtarlı sözlükte 'isaret' alanı); v3 tanımı değişmedi: ESIK5_SHA aynı (0a46827a...), aileler / D3 / tarama kodu aynı (git diff 2 satır). Yeni kod mührü:
KOD5_SHA: 70fc2fb979c47b2a2bd5fb260e1fb1891e7b34268f49c4a4276f482b66a4eb69
- Okunan etiketler: sayfa 3-26: EVET 7, HAYIR 17 (sayfa 5 sözlü yanıtla), YOK yalnız kapak sayfaları 1-2. Sayfa numarası PDF numarası (en büyük 26 > 24: önceden yazılı kurala göre kaydırma 0).
