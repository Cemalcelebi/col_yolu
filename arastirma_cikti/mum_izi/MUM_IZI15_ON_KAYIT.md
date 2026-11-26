# MUM_IZI15 ÖN KAYIT (2026-11-26T11:45:43Z)

MUM_IZI EK 15: kopma ayrımı. mum_izi13_olay.csv satırları AYNEN (R15, es_R15, fark, sinif, zaman); yeni getiri hesabı yok, yalnız gruplama. Bu dosya gruplama tabloları hesaplanmadan ÖNCE commit edilir; R15 / fark sütunlarına bu aşamada bakılmadı (sayım yalnız sinif, zaman, hakem etiketi, olculdu, es_neden).

## Mühürler

KOD15_SHA: d5f19876109e86326c3bc5d4877a20a65711d38f34284494856bdccaeb6d10fd
EK15_SHA: cbbb6430e21474099f42930a139d5a96f69d418e698adf244c95b08cbe19f982
HAKEM_K1_SHA: 02b1d5a36b5662ca0bd3dc526dc8aad0190cd32117c600f1f781fc9c83970679
HAKEM_K2_SHA: 65f03f481fd0af736916e27e9228f92aedc7b385e7a311f1e7de319582a9838f
OLAY13_SHA: fc27c506ae981157f13b2aeb534e2c9c098a947ad0b158130f0c5845f73dcec8
ANAHTAR6_SHA: 12bdea2a22f5f6d38d213d998a2f9c62186038bbccda89332aa296f990850835

- MUM_IZI_GOZ2.py commit'i: 0aeb71a16ade6073fb8ddb5fdc7c6e6678116f2d 2026-11-26T11:45:41+00:00

## Tanımlar (iş tanımı 2. bölüm aynen; K15_EK, sha yukarıda)

```
{
 "surum": "K15-1.0",
 "kaynak": "mum_izi13_olay.csv (128 bölge; R15, es_R15, fark = R15 - es_R15, sinif, zaman AYNEN; yeni getiri hesabı yok)",
 "hakem": "mum_izi15_kopma_K1.json / _K2.json; anahtar (set, sayfa) = csv set ve sayfa; k KOPMUS / BASKI / BELIRSIZ, puan 0-10 (10 = net kopmuş)",
 "uzlasi": "iki hakem KOPMUS -> KOPMUS; ikisi BASKI -> BASKI; ötekiler KARISIK",
 "duyarlilik": {
  "tanim": "iki hakemin ortalama puanı >= 6 -> KOPMUS*, <= 4 -> BASKI*, arası ARA*",
  "ust": 6.0,
  "alt": 4.0
 },
 "aileler": {
  "ANA": [
   "EVET"
  ],
  "IKINCI": [
   "EVET",
   "KISMEN"
  ],
  "UCUNCU": [
   "EVET",
   "KISMEN",
   "HAYIR"
  ]
 },
 "zaman": [
  "haftalik",
  "gunluk",
  "birlikte"
 ],
 "hucre": "n (ölçülen), R15 ort / medyan, n_es, eşli fark ort / medyan, artıda payı (R15 > 0), eşinden iyi payı (fark > 0; eşi olanlarda)",
 "karsilastirma": {
  "tanim": "KOPMUS - BASKI (duyarlılıkta KOPMUS* - BASKI*) eşli fark ortalaması farkı; p = etiket permütasyonu (GZ.gz_perm), iki yönlü, 10.000, tohum 15 (her karşılaştırmada aynı tohum); bir grup boş ya da n < 2 -> 'karşılaştırma yapılamaz'",
  "perm": 10000,
  "tohum": 15,
  "n_min": 2
 },
 "okuma": "AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ <=> ANA (EVET) içinde KOPMUS eşli fark ortalaması > 0 VE KOPMUS - BASKI > 0, haftalıkta ve günlükte aynı yönde; biri hesaplanamazsa 'OKUNAMADI (karşılaştırma yapılamaz)'; uzlaşı ve duyarlılık ayrı okunur",
 "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK",
 "bilgi_spearman": "EVET bölgelerinde iki hakemin ortalama puanı ile eşli fark arasında Spearman korelasyonu (haftalık, günlük, birlikte)",
 "kappa": "Cohen kappa, üç sınıf (KOPMUS / BASKI / BELIRSIZ): 128 csv bölgesi (ana) ve hakemlerin bütün sayfaları (bilgi)",
 "tekrar": "set2 katman T sayfaları (MUM_IZI6_ETIKET 7, 8, 9, 20, 26, 28, 34, 46) = set1 bölgeleri (mum_izi6_anahtar.json zaman + sembol + tarih = csv set1 bolge_son); her hakemin iki bakışta aynı k vermesi ve puan farkı",
 "es_siniri": "eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240)"
}
```

## Getirisiz sayım: Cemal sınıfı x zaman x uzlaşı / duyarlılık (128 bölge)

| Cemal | zaman | KOPMUS | BASKI | KARISIK | KOPMUS* | BASKI* | ARA* |
|---|---|---|---|---|---|---|---|
| EVET | haftalik | 12 | 1 | 7 | 17 | 1 | 2 |
| EVET | gunluk | 10 | 0 | 6 | 15 | 0 | 1 |
| KISMEN | haftalik | 5 | 0 | 1 | 6 | 0 | 0 |
| KISMEN | gunluk | 5 | 0 | 5 | 8 | 0 | 2 |
| HAYIR | haftalik | 19 | 0 | 17 | 26 | 1 | 9 |
| HAYIR | gunluk | 19 | 8 | 13 | 27 | 10 | 3 |

- Uzlaşı toplam: {"KOPMUS": 70, "KARISIK": 49, "BASKI": 9}; duyarlılık: {"KOPMUS*": 99, "ARA*": 17, "BASKI*": 12}
- K1: {"KOPMUS": 87, "BASKI": 22, "BELIRSIZ": 19}; K2: {"KOPMUS": 80, "BELIRSIZ": 39, "BASKI": 9}
- Ölçülen 128 / 128; eşi olan 117 (es_neden boş).

## Hakem uyumu (getirisiz)

- 128 bölge, üç sınıf: uyum 0.711, kappa 0.442; çapraz tablo (K1|K2): {"KOPMUS|KOPMUS": 70, "KOPMUS|BASKI": 0, "KOPMUS|BELIRSIZ": 17, "BASKI|KOPMUS": 3, "BASKI|BASKI": 9, "BASKI|BELIRSIZ": 10, "BELIRSIZ|KOPMUS": 7, "BELIRSIZ|BASKI": 0, "BELIRSIZ|BELIRSIZ": 12}
- Bütün ortak sayfalar (bilgi, n 144): kappa 0.449
- Puanların Spearman'ı (K1 - K2, 128): 0.739

## Hakemin kendi tutarlılığı (set2 tekrar sayfaları = set1 bölgeleri)

- Eşleme: set2 s7 = set1 s23, set2 s8 = set1 s19, set2 s9 = set1 s16, set2 s20 = set1 s11, set2 s26 = set1 s9, set2 s28 = set1 s10, set2 s34 = set1 s26, set2 s46 = set1 s6 (mum_izi6_anahtar.json katman T; eski_sayfa ve csv bolge_son ile denetlendi)
- K1: aynı k 7 / 8; ortalama mutlak puan farkı 0.00
- K2: aynı k 8 / 8; ortalama mutlak puan farkı 0.00

## n < 2 olan karşılaştırmalar ('karşılaştırma yapılamaz' çıkacak)

- ANA|duyarlilik|birlikte
- ANA|duyarlilik|gunluk
- ANA|duyarlilik|haftalik
- ANA|uzlasi|birlikte
- ANA|uzlasi|gunluk
- ANA|uzlasi|haftalik
- IKINCI|duyarlilik|birlikte
- IKINCI|duyarlilik|gunluk
- IKINCI|duyarlilik|haftalik
- IKINCI|uzlasi|birlikte
- IKINCI|uzlasi|gunluk
- IKINCI|uzlasi|haftalik
- UCUNCU|uzlasi|haftalik

Grup n'leri (n = ölçülen, n_es = eşi olan):

```
{
"ANA|uzlasi|haftalik|KOPMUS": {
"n": 12,
"n_es": 10,
"n_lt2": false
},
"ANA|uzlasi|haftalik|BASKI": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"ANA|uzlasi|haftalik|KARISIK": {
"n": 7,
"n_es": 7,
"n_lt2": false
},
"ANA|uzlasi|gunluk|KOPMUS": {
"n": 10,
"n_es": 7,
"n_lt2": false
},
"ANA|uzlasi|gunluk|BASKI": {
"n": 0,
"n_es": 0,
"n_lt2": true
},
"ANA|uzlasi|gunluk|KARISIK": {
"n": 6,
"n_es": 5,
"n_lt2": false
},
"ANA|uzlasi|birlikte|KOPMUS": {
"n": 22,
"n_es": 17,
"n_lt2": false
},
"ANA|uzlasi|birlikte|BASKI": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"ANA|uzlasi|birlikte|KARISIK": {
"n": 13,
"n_es": 12,
"n_lt2": false
},
"ANA|duyarlilik|haftalik|KOPMUS*": {
"n": 17,
"n_es": 15,
"n_lt2": false
},
"ANA|duyarlilik|haftalik|BASKI*": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"ANA|duyarlilik|haftalik|ARA*": {
"n": 2,
"n_es": 2,
"n_lt2": false
},
"ANA|duyarlilik|gunluk|KOPMUS*": {
"n": 15,
"n_es": 11,
"n_lt2": false
},
"ANA|duyarlilik|gunluk|BASKI*": {
"n": 0,
"n_es": 0,
"n_lt2": true
},
"ANA|duyarlilik|gunluk|ARA*": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"ANA|duyarlilik|birlikte|KOPMUS*": {
"n": 32,
"n_es": 26,
"n_lt2": false
},
"ANA|duyarlilik|birlikte|BASKI*": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"ANA|duyarlilik|birlikte|ARA*": {
"n": 3,
"n_es": 3,
"n_lt2": false
},
"IKINCI|uzlasi|haftalik|KOPMUS": {
"n": 17,
"n_es": 15,
"n_lt2": false
},
"IKINCI|uzlasi|haftalik|BASKI": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"IKINCI|uzlasi|haftalik|KARISIK": {
"n": 8,
"n_es": 8,
"n_lt2": false
},
"IKINCI|uzlasi|gunluk|KOPMUS": {
"n": 15,
"n_es": 12,
"n_lt2": false
},
"IKINCI|uzlasi|gunluk|BASKI": {
"n": 0,
"n_es": 0,
"n_lt2": true
},
"IKINCI|uzlasi|gunluk|KARISIK": {
"n": 11,
"n_es": 9,
"n_lt2": false
},
"IKINCI|uzlasi|birlikte|KOPMUS": {
"n": 32,
"n_es": 27,
"n_lt2": false
},
"IKINCI|uzlasi|birlikte|BASKI": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"IKINCI|uzlasi|birlikte|KARISIK": {
"n": 19,
"n_es": 17,
"n_lt2": false
},
"IKINCI|duyarlilik|haftalik|KOPMUS*": {
"n": 23,
"n_es": 21,
"n_lt2": false
},
"IKINCI|duyarlilik|haftalik|BASKI*": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"IKINCI|duyarlilik|haftalik|ARA*": {
"n": 2,
"n_es": 2,
"n_lt2": false
},
"IKINCI|duyarlilik|gunluk|KOPMUS*": {
"n": 23,
"n_es": 19,
"n_lt2": false
},
"IKINCI|duyarlilik|gunluk|BASKI*": {
"n": 0,
"n_es": 0,
"n_lt2": true
},
"IKINCI|duyarlilik|gunluk|ARA*": {
"n": 3,
"n_es": 2,
"n_lt2": false
},
"IKINCI|duyarlilik|birlikte|KOPMUS*": {
"n": 46,
"n_es": 40,
"n_lt2": false
},
"IKINCI|duyarlilik|birlikte|BASKI*": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"IKINCI|duyarlilik|birlikte|ARA*": {
"n": 5,
"n_es": 4,
"n_lt2": false
},
"UCUNCU|uzlasi|haftalik|KOPMUS": {
"n": 36,
"n_es": 34,
"n_lt2": false
},
"UCUNCU|uzlasi|haftalik|BASKI": {
"n": 1,
"n_es": 1,
"n_lt2": true
},
"UCUNCU|uzlasi|haftalik|KARISIK": {
"n": 25,
"n_es": 23,
"n_lt2": false
},
"UCUNCU|uzlasi|gunluk|KOPMUS": {
"n": 34,
"n_es": 30,
"n_lt2": false
},
"UCUNCU|uzlasi|gunluk|BASKI": {
"n": 8,
"n_es": 8,
"n_lt2": false
},
"UCUNCU|uzlasi|gunluk|KARISIK": {
"n": 24,
"n_es": 21,
"n_lt2": false
},
"UCUNCU|uzlasi|birlikte|KOPMUS": {
"n": 70,
"n_es": 64,
"n_lt2": false
},
"UCUNCU|uzlasi|birlikte|BASKI": {
"n": 9,
"n_es": 9,
"n_lt2": false
},
"UCUNCU|uzlasi|birlikte|KARISIK": {
"n": 49,
"n_es": 44,
"n_lt2": false
},
"UCUNCU|duyarlilik|haftalik|KOPMUS*": {
"n": 49,
"n_es": 47,
"n_lt2": false
},
"UCUNCU|duyarlilik|haftalik|BASKI*": {
"n": 2,
"n_es": 2,
"n_lt2": false
},
"UCUNCU|duyarlilik|haftalik|ARA*": {
"n": 11,
"n_es": 9,
"n_lt2": false
},
"UCUNCU|duyarlilik|gunluk|KOPMUS*": {
"n": 50,
"n_es": 44,
"n_lt2": false
},
"UCUNCU|duyarlilik|gunluk|BASKI*": {
"n": 10,
"n_es": 10,
"n_lt2": false
},
"UCUNCU|duyarlilik|gunluk|ARA*": {
"n": 6,
"n_es": 5,
"n_lt2": false
},
"UCUNCU|duyarlilik|birlikte|KOPMUS*": {
"n": 99,
"n_es": 91,
"n_lt2": false
},
"UCUNCU|duyarlilik|birlikte|BASKI*": {
"n": 12,
"n_es": 12,
"n_lt2": false
},
"UCUNCU|duyarlilik|birlikte|ARA*": {
"n": 17,
"n_es": 14,
"n_lt2": false
}
}
```

## Önceden bilinen sonuçlar ve sınırlar (hesaptan önce, getirisiz sayımdan)

- ANA (EVET) tablosunda uzlaşı BASKI n_es haftalık 1, günlük 0; duyarlılık BASKI* haftalık 1, günlük 0: ANA'nın bütün KOPMUS - BASKI karşılaştırmaları 'karşılaştırma yapılamaz' çıkacak, okuma kuralı 'OKUNAMADI (karşılaştırma yapılamaz)' olacak. Grup / eşik DEĞİŞMEZ.
- İKİNCİ (EVET + KISMEN) de aynı nedenle yapılamaz. Yalnız ÜÇÜNCÜ (128 bölge) günlük ve birlikte satırlarında KOPMUS - BASKI hesaplanabilir (BASKI çoğu Cemal HAYIR günlük).
- Tekrar sayfalarında iki hakemin puanları birebir aynı (mutlak fark 0,00): hakem aynı görüntüyü tanımış olabilir; tutarlılık ölçüsü bu yüzden yukarı yanlı olabilir.
- Hakem bağımsızlığı kesin değil: iki hakem aynı geçici klasörü paylaştı, K2 ara notlarının ezildiğini bildirdi (raporda HATA).

## Ek BİLGİ satırı (önceden yazılı)

- EVET bölgelerinde iki hakemin ortalama puanı ile eşli fark arasında Spearman korelasyonu (haftalık, günlük, birlikte); karar vermez.

## Okuma kuralı (aynen)

- AYRIM YÖNÜ CEMAL'İN DEDİĞİ GİBİ <=> ANA (EVET) içinde KOPMUS eşli fark ortalaması > 0 VE KOPMUS - BASKI > 0, haftalıkta ve günlükte aynı yönde; biri hesaplanamazsa 'OKUNAMADI (karşılaştırma yapılamaz)'; uzlaşı ve duyarlılık ayrı okunur
- Etiket her durumda: BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK. Eşik / gruplama sonuca göre değişmez; değişirse SAPMA.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşli fark mum_izi13_olay.csv'den aynen (aynı giriş günü aynı kova CETVEL2 konum eşi); yeni eş yok; sınır: eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240) |
| K2 | geleceğe bakma | EVET | hakemler sonrasını görmedi (işaretsiz PDF bölge sonunda kesik; yasak liste hakem metninde); hakem json'ları hesaptan önce commit; SINIR: ölçüt Cemal sonrasını gördükten sonra söylendi -> GERİYE DÖNÜK |
| K3 | geçerli bar | EVET | geçerli bar kuralı MUM_IZI11 / 13 ölçümünde (MI.mi_veri H > L, V > 0); bu iş bar okumaz |
| K4 | tekilleştirme | EVET | 128 tekil bölge (GZ.gz_ornek K4 denetimi); set2 T tekrar sayfaları ayrı bölge sayılmaz, yalnız hakem tutarlılığında kullanılır |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (MUM_IZI11 tanımı, csv aynen) |
| K6 | veri birimi | EVET | getiriler oransal, csv aynen; pazarlar arası karşılaştırma eşli farkla |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | bütün gruplar n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; n < 2 grup 'karşılaştırma yapılamaz'; tek dönem (<= 2022), BH yok (karar yok) |
| K9 | ön kayıt | EVET | bu ön kayıt (KOD15 / EK15 / hakem / olay sha + getirisiz sayımlar) hesaptan önce commit; k15_kapi sha + commit + temiz ağaç denetler |
| K10 | ayrıştırma | EVET | hakem json şeması denetlenir (k ve puan aralığı; bilinmeyen değer DUR); (set, sayfa) eşleşmesi 128 / 128 değilse DUR; tekrar eşlemesi anahtardan |
| K11 | yeniden üretim | EVET | tablo sayılarından >= 2 hücre olay csv'sinden bağımsız pandas koduyla yeniden üretilir (rapor öncesi denetim) |
| K12 | ifade | EVET | 'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; okuma kuralı yalnız yön |
| K13 | süreç | EVET | çakışma kapısı korunur; çalışan komutlar değişmez (test); yasak defter dosyalarına dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez |

## SAPMA

(ön kayıt anında yok)
