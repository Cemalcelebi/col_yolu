# MUM_IZI2 ÖN KAYIT (2026-11-25T10:15:25Z)

Ortak nokta hesabı (yüzdelik dağılımları, karşılaştırma, şans tabanı, birleşik kural) bu dosya commit edildikten SONRA koşar (`mi2_kapi`).
Bu ana kadar yalnız ENSRI görüntüsü sayısallaştırıldı; açık veride hiçbir pencere ölçülmedi.

## Mühürler

KOD2_SHA: c4c1019af0eb23095ddb96e2ace420cfc10421cddd60c9f556efe5d8fc6bc8ac
ESIK2_SHA: d1247a098546c6876c13785d3047e13f4fb412f1c2c21bfa9576ab54f3d54a33
SAYISAL2_SHA: a0eff63cbd85b1c6166df459a35804af11ae6c5d855b344927651cd0fa3a077e
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9

- MUM_IZI2.py commit'i: d13bc9c128e67fad9e91de0642bd3fe3a11c3556 2026-11-25T10:15:15+00:00
- Görüntü sha: de155d4f01718f424b96a1647ee7e313a880ae750eb9f95696027bf98e1a7d76

## Sayısallaştırma (görüntüden)

- 12 mum, renk YKKYKKKKYYYY; kenarda kırpık: {'12': 'SAG_KIRPIK'}; alt bandı panel altında kalan mumlar [1, 2] (E: ilk 4 görünür mumdan doğrusal, eğim 0.345 TL / mum; T: panel tabanı 0.080 TL)
- TL kalibrasyonu: 13 etiket, TL = 10.58716 + -0.0080084 x satır; en büyük artık 0.0037 TL (0.46 px); ızgara satırı farkı en çok 1.5 px
- Notlar: Üstte 'Piyasa Fiyatı ₺2,23' yazıyor, mumlar ~₺4 düzeyinde: çelişki yalnız not edildi (neden aranmadı, veriye bakılmadı). Orta bant (SMA20) çizgisi görünmüyor: orta = (üst + alt) / 2 TÜRETİLDİ. Mum aralığı AYLIK varsayıldı ('5Y' görünüm, yıl etiketleri arası ~3 mum); 12 mum ~ 1 yıl; bant 20 mumdan kısa geçmişle çizilmiş olabilir.

## Yüzdelik dağılımı nasıl kuruldu (ölçümden önce yazıldı)

```
{
 "pazar": [
  "ABD",
  "AVR",
  "BIST"
 ],
 "veri": "MUM_IZI açık kopya (/tmp/mum_izi/acik, <= 2022-12-30), MI.mi_veri yükleyicisi",
 "tarama": [
  "2016-01-01",
  "2022-12-31"
 ],
 "n": 20000,
 "L": [
  20,
  12
 ],
 "tohum": {
  "20": 25112031,
  "12": 25112032
 },
 "tanim": "geçerli (hisse, pencere sonu e) çiftleri üç pazar birleşik havuz: e tarama aralığında, pencere başı bandın tanımlı olduğu ilk bardan (19) sonra; havuzdan yerine koymadan düzgün 20.000; ölçüler MI.mi_ozellik + MI.mi_bant (SMA20, 2 std)",
 "yuzdelik": "p = (#{x < v} + 0,5 #{x = v}) / N"
}
```

## Ortak nokta, şans tabanı, S, birleşik kural (sabit; sonuca göre oynanmaz)

```
{
 "ortak": {
  "yuksek": 0.75,
  "dusuk": 0.25,
  "guclu_yuksek": 0.9,
  "guclu_dusuk": 0.1,
  "sinif": "GÜÇLÜ ORTAK: p1, p2 >= 0,90 ya da ikisi <= 0,10; ORTAK: ikisi >= 0,75 ya da ikisi <= 0,25 (güçlü değil); ZIT: biri >= 0,75 öteki <= 0,25; AYRI: kalan; BELİRSİZ: bant senaryosuna göre sınıf değişiyor. p1 = iz 1 (MUM_IZI tam şablonu, L 20) L 20 dağılımında; p2 = iz 2 (ENSRI, L 12) L 12 dağılımında"
 },
 "S": "iz 2'ye iz 1 şablonu: MUM_IZI pencere uzunlukları 16..24 (esneme +-%20); L 12 bu aralıkta değilse 'S UYGULANAMAZ' ve ölçü uzaklığı bileşeni D_oz (MI.mi_mesafe ölçü kısmı, kalibrasyon sd'si) ile D_oz / tau_oz verilir; ayrıca rastgele L 12 dağılım pencerelerinin iz 1'e D_oz değerleri içinde iz 2'nin yüzdeliği",
 "sans": {
  "cift": 5000,
  "tohum": {
   "20": 25112033,
   "12": 25112034
  },
  "tanim": "aynı havuzdan bağımsız 5.000 L 20 ve 5.000 L 12 pencere, sırayla eşlenir (5.000 çift); her çiftte aynı yüzdelik ve sınıf kuralıyla (aynı ölçü kümesi: BELİRSİZ ölçüler dışarıda) GÜÇLÜ ORTAK, ORTAK (güçlü dahil) ve ZIT sayısı; ortalama, %95 üst sınır (0,95 yüzdelik) ve iki izin sayısına eşit ya da büyük çift payı. 'Ortak nokta çok' sözü yalnız iki izin ORTAK sayısı %95 üst sınırı AŞARSA"
 },
 "birlesik": {
  "L": [
   12,
   20
  ],
  "tekil": 15,
  "kural": "GÜÇLÜ ORTAK + ORTAK ölçülerin HEPSİ aynı uçta: YÜKSEK -> ölçü >= q_L(0,75), DÜŞÜK -> ölçü <= q_L(0,25); q_L = q_12 + (q_20 - q_12) (L - 12) / 8 (L 12 ve L 20 dağılımlarının yüzdelikleri arasında doğrusal); pencere sonu t'de L = 12..20'den en az biri kuralı taşırsa olay, m = en kısa uygun L; aynı hissede 15 geçerli bar tekil; tarama 2016-22 ABD / AVR / BIST",
  "sonrasi": "MI.mi_sonrasi AYNEN: ABD / AVR P2 + CETVEL2 v2.2 konum eşi, R15 eşli fark, +%5 (stop = pencere en düşük Low x 0,98) vs 20 eş, plasebo 200 tohum (karar pazarı, 'hepsi'); konum MI.mi_konum_seri; n < 30 hücre 'örneklem yetersiz'",
  "etiket": "EZBER RİSKLİ (iki örnekten türetildi); karar etiketi VERİLMEZ, kasa açılmaz"
 },
 "bant": {
  "orta": "SMA20 çizgisi görünmüyor -> orta = (üst + alt) / 2 (TÜRETİLDİ)",
  "gorunmeyen_alt": "alt bant çizgisi fiyat panelinin tabanının ALTINDA kalan mumlar: iki senaryo. E = görünür ilk 4 mumun alt bant değerinden doğrusal ekstrapolasyon; T = panel tabanının TL değeri (alt bandın en yüksek olabileceği yer). Bir ölçünün ORTAK sınıfı iki senaryoda aynı değilse BELİRSİZ: sayıma ve birleşik kurala girmez. Ana değer E"
 },
 "olcu": "MI.MI_OZELLIK 35 ölçü AYNEN (iş tanımı '33' diyor; MUM_IZI'de 35 ölçü + 3 bağlam ölçüsü var; bağlam ölçüleri ENSRI'de bölge öncesi olmadığı için dışarıda)"
}
```

## Tohumlar

- dağılım L20 25112031, L12 25112032; şans L20 25112033, L12 25112034 (çift eşleme permütasyonu 25112040); elle doğrulama 2518; prefix 2519; birleşik plasebo / eş MUM_IZI tohumları (MI_ESIK['gercek'])

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | ortak nokta tabanı = şans tabanı SAYIYLA (5.000 rastgele L20 / L12 pencere çifti, aynı kural, ortalama ve %95 üst sınır); birleşik kural sonrası MI.mi_sonrasi: CETVEL2 v2.2 konum eşi (aynı gün aynı kova >= 5 eş), +%5 eşi aynı geometri, plasebo 200 tohum |
| K2 | geleceğe bakma | EVET | ENSRI yalnız görüntüden (2024-25 gerçek fiyat OKUNMAZ); dağılım / şans / birleşik kural açık kopya <= 2022-12-30 (KASA kapısı MI.mi_kasa_kapi); pencere ölçüleri yalnız t'ye kadarki barlar (MI.mi_bant / mi_ozellik prefix testli); birleşik olayda prefix denetimi (mi2_prefix, 30 olay) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar süzgeci (H > L, V > 0); sayısallaştırmada her bölge mumu H >= max(O,C), L <= min(O,C) denetimi |
| K4 | tekilleştirme | EVET | birleşik kural olayları aynı hissede 15 geçerli bar tekil (MI._mi_tekil) + C2.c2_olay tekil 15; dağılım pencereleri tekilsiz (yüzdelik tabanı, olay değil) |
| K5 | giriş fiyatı | EVET | giriş t + 1 açılış (MI.mi_sonrasi -> OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1 |
| K6 | veri birimi | EVET | ENSRI TL ekseni doğrusal kalibrasyon (13 etiket, artık yazılır); ölçüler ölçek bağımsız (oran, mum boyu birimi); gerçek veri TEZGAH2 bölünme düzeltmeli açık kopya |
| K7 | hayatta kalma | EVET | açık kopya bugün işlem gören hisseler (ABD 4.450, AVR 572, BIST 475): sonrası yukarı yanlı, olay ve eş aynı evren; ENSRI tek hisse, halka arz sonrası kısa geçmiş (bant 12 aylık mumla) |
| K8 | örneklem ve dönem | EVET | birleşik kural hücreleri pazar x dönem (d1619 / d2022); n < 30 'örneklem yetersiz'; iki örnekten türetilen kural EZBER RİSKLİ; karar etiketi yok |
| K9 | ön kayıt | EVET | MUM_IZI2_ON_KAYIT.md: KOD2_SHA, ESIK2_SHA, SAYISAL2_SHA, MI_KOD_SHA, dağılım tohumları; ön kayıt commit'i ortak nokta hesabından ÖNCE; mi2_kapi kontrol kapısı + sha + git denetler |
| K10 | ayrıştırma | EVET | bindirme PNG (12 mum) + 3 rastgele mumun yakın plan elle doğrulama PNG'si; mum sayısı ve renk dizisi elle sayımla (test_mum_izi2); TL kalibrasyon artığı ve ızgara satırı sağlaması |
| K11 | yeniden üretim | EVET | mi2_yeniden: iki ölçünün (ust_fitil, kapanis_egim) iz 2 değeri düz döngüyle; iki ölçünün yüzdeliği dağılım dosyasından düz pandas ile; birleşik kural 10 olayda kuralın düz yeniden denetimi |
| K12 | ifade | EVET | 'ortak nokta çok' sözü yalnız şans tabanı aşılırsa; birleşik kural EZBER RİSKLİ, karar yok; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mi2); MUM_IZI.py ve defter / UC_IZ2 dosyaları değişmez; yalnız kendi yolları git add |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; benzerlik / ortak nokta ölçümü |

## SAPMA

(ön kayıt anında yok)
## Elle doğrulama (K10, ortak nokta hesabından önce)

- Mum sayısı: görüntüde elle 12, kod 12. Renk dizisi elle YKKYKKKKYYYY = kod; 6. mumun gövdesi çizgi (doji) = kod; 2, 10, 11. mumların gövdesi ince (doji değil, ölçüde gövde / boy küçük).
- Rastgele 3 mum (5, 6, 7; tohum 2518) yakın planda (mum_izi2_elle_dogrulama.png): gövde ve fitil uçları görüntüyle gözle örtüşüyor (fark en çok 1-2 piksel).
- Bindirme (mum_izi2_bindirme.png): 12 mumun gövde çerçevesi ve fitil çizgisi, üst / alt bant noktaları ve 13 TL etiketi (kırmızı çentik) görüntüyle çakışıyor. 12. mumun gövdesinin sağ ~5 pikseli grafik kenarında kırpık; gövde üst / alt ve fitil ölçülebiliyor.
- İlk mum (1) kesik DEĞİL (gövdesi tam görünüyor).

## Varsayımlar

- Mum aralığı AYLIK ('5Y' görünümü; yıl etiketleri arası ~3 mum). 12 mum ~ 1 yıl. İz ölçek bağımsız; açık veri GÜNLÜK pencerelerle karşılaştırılır (iz 1 de 4 saatlikten günlüğe uygulanmıştı).
- Bant çizgileri Bollinger üst / alt kabul edildi (iş tanımı); orta çizgi türetildi. Kısa geçmiş nedeniyle bant 20 aydan az mumla çizilmiş olabilir.
- Ölçü sayısı 35 (MI.MI_OZELLIK); iş tanımındaki '33' MUM_IZI'deki sayıyla uyuşmuyor; bütün 35 ölçü aynen kullanılır (SAPMA 1 olarak raporda).
