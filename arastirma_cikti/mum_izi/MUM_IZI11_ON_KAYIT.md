# MUM_IZI11 ÖN KAYIT (2026-11-26T09:53:22Z)

Göz ölçümü: Cemal'in etiketi tespit sayılır; bölgelerin sonrası ölçülür. Bu dosya GETİRİLER HESAPLANMADAN önce commit edilir; tanımlar sonra değişmez. Sonuç bilgi: n < 30 hücre 'örneklem yetersiz'; 'iz / tuttu' sözü yok; kasa açılmaz.

## Mühürler

KOD11_SHA: ffff865717b0e8e6d150895d5602551801831149b3a9847e196ae8ab66971394
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
ISARET_SET1_SHA: fb624d983dd8698ccd27475dc5aac321f57c8634a59db548279cd8b7758895a8
ANAHTAR_SET1_SHA: 2da80dab164d8a937ee916617cc73dd5a65ac8adbe4f0630c07b25f8834e352c
ISARET_SET2_SHA: cff06ba0a743582489999576e77f0b0a19e9272c709faaffc1f13afb389f17df
ANAHTAR_SET2_SHA: 12bdea2a22f5f6d38d213d998a2f9c62186038bbccda89332aa296f990850835
ISARET_SET3_SHA: 35fa2d718a76da2e5dbb5517465429d0f858d38a41bae17907b8e22b061d27bb
ANAHTAR_SET3_SHA: 6083f0d088f648cefd6591dea806da8715c121a90bbec616943ab319bf29f56c
ISARET_SET4_SHA: d02173f194bb37b7464df78f71016bd22a4d232fafc7f2a60a6bebf8c9a7c835
ANAHTAR_SET4_SHA: c259d11ea69e0f8b1f40f9869221aa15c9121c3e959822af5ccdc1dc3d455bfe

- MUM_IZI_GOZ.py commit'i: 66b043ed038651251ee2f1f969bcaf69034f004d 2026-11-26T09:53:21+00:00

## Örneklem (getirisiz sayım)

- {"toplam": 104, "sinif": {"HAYIR": 71, "EVET": 25, "KISMEN": 8}, "set_sinif": {"set1|EVET": 7, "set1|HAYIR": 17, "set2|EVET": 9, "set2|HAYIR": 28, "set3|EVET": 2, "set3|HAYIR": 17, "set4|EVET": 7, "set4|HAYIR": 9, "set4|KISMEN": 8}, "sinif_zaman": {"EVET|gunluk": 11, "EVET|haftalik": 14, "HAYIR|gunluk": 36, "HAYIR|haftalik": 35, "KISMEN|gunluk": 5, "KISMEN|haftalik": 3}, "set_sinif_zaman": {"set1|EVET|gunluk": 5, "set1|EVET|haftalik": 2, "set1|HAYIR|gunluk": 7, "set1|HAYIR|haftalik": 10, "set2|EVET|gunluk": 3, "set2|EVET|haftalik": 6, "set2|HAYIR|gunluk": 16, "set2|HAYIR|haftalik": 12, "set3|EVET|gunluk": 1, "set3|EVET|haftalik": 1, "set3|HAYIR|gunluk": 8, "set3|HAYIR|haftalik": 9, "set4|EVET|gunluk": 2, "set4|EVET|haftalik": 5, "set4|HAYIR|gunluk": 5, "set4|HAYIR|haftalik": 4, "set4|KISMEN|gunluk": 5, "set4|KISMEN|haftalik": 3}, "pazar": {"EVET|ABD": 13, "EVET|AVR": 5, "EVET|BIST": 7, "HAYIR|ABD": 51, "HAYIR|AVR": 10, "HAYIR|BIST": 10, "KISMEN|ABD": 7, "KISMEN|BIST": 1}, "tekrar_degisen": 2}

## Örneklem özeti (düz)

- 104 bölge (tekrarlar ayrı değil): EVET 25 (günlük 11, haftalık 14), KISMEN 8 (günlük 5, haftalık 3), HAYIR 71 (günlük 36, haftalık 35).
- Setler: set1 EVET 7 / HAYIR 17; set2 EVET 9 / HAYIR 28 (tekrar 8 sayfa dışarıda; karar dışı 3); set3 EVET 2 / HAYIR 17 (karar dışı 5); set4 EVET 7 / KISMEN 8 / HAYIR 9.
- Tekrar sayfalarında yanıtı değişen 2 bölge: duyarlılık satırı 'son işaretle'.
- Bütün sınıf x zaman dilimi hücreleri n < 30: hepsi 'örneklem yetersiz' etiketi taşıyacak (önceden bilinen).

## Uygulama kararları

1. Günlük olaylar açık kopya günlük veriyle (2015-2022), haftalık olaylar MUM_IZI_HAFTALIK tam günlük veriden kurulan ISO haftalarıyla; bölge ve stop kendi zaman diliminde, dokunma / stop sırası günlük barlarla.
2. Eş paneli: günlük -> açık kopya; haftalık -> bölge sonu <= 2015-12-31 ise p1 (2000-2016), değilse açık kopya (MUM_IZI_HAFTALIK kuralı); BIST'in p1 paneli yok (2015 öncesi BIST haftalık bölge eşsiz kalır).
3. Permütasyon iki yönlü (fark ortalamasının mutlak değeri); bootstrap olay düzeyinde, ortalama ve medyan için.
4. PDF'te haftalık bölgeler haftalık mumlarla, günlükler günlük mumlarla çizilir; 30 mum sonrası veri kesiğini aşmaz.

## Tanımlar (GZ_ESIK; sha yukarıda)

```
{
 "surum": "GZ-1.0",
 "ornek": {
  "setler": "set1 MUM_IZI4_ONAY (s3-26), set2 MUM_IZI6_ETIKET (s2-49), set3 MUM_IZI8_ONAY (s3-26), set4 MUM_IZI10_ONAY (s2-25)",
  "isaret": "EVET / KISMEN / HAYIR karar; IKISI / YOK / BELIRSIZ karar dışı (çıkar); başka değer -> DUR",
  "tekrar": "set2'nin katman 'T' sayfaları set1 bölgelerinin tekrarıdır: ayrı bölge sayılmaz, İLK işaret (set1) geçerli; duyarlılık satırı: o bölgeler set2'deki SON işaretle (karar dışıysa ilk işaret)",
  "bolge": "anahtardaki hisse, zaman dilimi, bölge sonu ve uzunluk (set4'te bölge başı / sonu / pencere)"
 },
 "olcu": {
  "giris": "bölgenin son mumundan sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk geçerli günü; o haftalık barın açılışı)",
  "ufuk": 15,
  "R15": "15. mumun kapanışı / giriş - 1 (giriş mumu 1. mum; haftalıkta 15. haftanın son geçerli günü)",
  "max_min": "giriş günü .. 15. mumun son günü arasında günlük en yüksek High / giriş - 1 ve en düşük Low / giriş - 1",
  "stop": "bölgenin (kendi zaman diliminde) en düşük Low'u x 0,98; giriş <= stop ise olay ölçülmez (sayısı yazılır); stop payı = ufukta günlük Low <= stop",
  "dokunma": "günlük sırayla High >= giriş x (1 + hedef) olan ilk gün stop gününden ÖNCE (aynı gün = stop önce)",
  "hedef": {
   "gunluk": [
    0.05,
    0.1
   ],
   "haftalik": [
    0.1,
    0.2
   ]
  },
  "stop_carpan": 0.98,
  "bilgi": 30,
  "veri": {
   "gunluk": "MUM_IZI açık kopya (/tmp/mum_izi/acik, 2015-2022, günlük)",
   "haftalik": "MUM_IZI_HAFTALIK tam (2000-2022, günlük -> ISO hafta)"
  },
  "kesik": "15. mumun son günü <= 2022-12-30 değilse ölçülmez (ufuk kesik; sayısı yazılır); R30 aynı kuralla"
 },
 "es": {
  "tanim": "CETVEL2 v2.2 paneli (c2_panel22_al, önbelleksiz): aynı giriş günü d, aynı kova KV[d] (ATRP tercili x likidite üçlüsü x F15 çeyreği; KV >= 0), olay hissesi ve aynı gün başka örneklem olayı olan hisseler dışı, d'de geçerli açılış; R = olayın 15. mum son günündeki (ya da öncesindeki son geçerli) kapanış / d açılışı - 1 (AYNI takvim aralığı); eşin stop'u = olayın bölge takvim aralığında eşin en düşük Low'u x 0,98 (giriş > stop olanlar); eş dokunma / stop payları aynı kuralla",
  "min": 5,
  "panel": "günlük olaylar: açık kopya paneli; haftalık olaylar: bölge sonu <= 2015-12-31 ise p1 paneli (/tmp/mum_izi/haftalik/p1, 2000-2016), değilse açık kopya paneli; panelde olmayan / kovasız / eşi < 5 olay eşli tabloya girmez (sayısı yazılır)",
  "fark": "eşli fark = R15 - eş ortalaması"
 },
 "tablo": {
  "hucre": "sınıf (EVET, KISMEN, HAYIR, EVET+KISMEN) x zaman dilimi (günlük, haftalık)",
  "B": 5000,
  "tohum_boot": 25112111,
  "olcu": "n, R15 ortalama ve medyan, eş ortalaması, eşli fark ortalama ve medyan + olay bootstrap %95 (yerine koyarak, B 5000), artıda kapanan pay (R15 > 0), dokunma payları, stop payı, en yüksek / en derin medyanı, R30 ortalama (bilgi)",
  "n_az": 30,
  "etiket": "n < 30 -> 'örneklem yetersiz'",
  "karsilastirma": "her zaman diliminde EVET - HAYIR (R15 ortalaması ve eşli fark ortalaması) + permütasyon p (iki yönlü, 10.000, tohum 25112112); ayrıca (EVET + KISMEN) - HAYIR",
  "perm": 10000,
  "tohum_perm": 25112112,
  "bilgi": "pazar dağılımı; BIST ayrı satır; iki zaman dilimi birleşik eşli fark satırı; tekrar duyarlılığı (son işaretle)"
 },
 "pdf": {
  "sayfa1": "düz dil tablo (EVET / KISMEN / BENZEMİYOR x günlük / haftalık: n, kaçı artıda, ortalama ve medyan getiri, eş ortalaması, +%10'a kaçı dokundu, kaçı stop) + 'Sayılar az (N < 30): bu bir sonuç değil, ilk bakış.'",
  "bolge": "BENZİYOR bölgeleri (önce haftalık sonra günlük; tarih sırası), sonra KISMEN: öncesi 15 mum + bölge (turuncu kutu) + sonrası 30 mum (veri kesiğini aşmaz), Bollinger 20 + SMA20, giriş / stop / 15. mum çizgileri, hisse kodu + tarih AÇIK, altında R15, eş ortalaması, en yüksek / en derin"
 }
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü aynı kova (CETVEL2 v2.2 konum eşi) aynı takvim aralığı, aynı stop geometrisi; HAYIR sınıfı aynı seçim hattından doğal kontrol |
| K2 | geleceğe bakma | EVET | Cemal bölgeleri sonrasını görmeden işaretledi (PDF'ler bölge sonunda kesik); bölgeler kodun o güne kadarki veriyle seçtikleri; giriş bölgeden SONRAKİ barın açılışı; eş kovası giriş günü bilgisiyle; veri <= 2022-12-31 + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0); haftalık barlar tamamlanmış ISO haftaları (MH) |
| K4 | tekilleştirme | EVET | tekrar sayfaları ayrı bölge değil (ilk işaret); setler arasında hisse tekrarı yok (onay seçimleri önceki setlerin hisselerini dışladı; denetlenir) |
| K5 | giriş fiyatı | EVET | giriş = sonraki ilk geçerli barın açılışı (haftalıkta sonraki haftanın ilk günü açılışı); giriş <= stop olay ölçülmez |
| K6 | veri birimi | EVET | TEZGAH2 / MI bölünme düzeltmeli fiyatlar; getiriler oransal; BIST TL, ABD USD, AVR yerel para (karşılaştırma eşli farkla) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | sınıf x zaman dilimi hücrelerinin çoğu n < 30: 'örneklem yetersiz' etiketi; karşılaştırma permütasyonla |
| K9 | ön kayıt | EVET | MUM_IZI11_ON_KAYIT.md: KOD11 / ESIK11 / etiket ve anahtar sha'ları + sınıf sayıları; getiriler bu commit'ten sonra; gz_kapi |
| K10 | ayrıştırma | EVET | etiket şeması (isaret; bilinmeyen değer DUR); anahtar alanları (set4: bolge_bas / bolge_son / pencere); bölge başı veriden yeniden hesaplanıp set4'te anahtarla denetlenir |
| K11 | yeniden üretim | EVET | olay ölçüleri 2 olayda düz döngüyle yeniden; tablo sayıları csv'den yeniden üretilir (test) |
| K12 | ifade | EVET | 'iz / tuttu' sözü yok; n < 30 'örneklem yetersiz'; sonuç 'ilk bakış' |
| K13 | süreç | EVET | çakışma kapısı; eski kodlar / defterler / UC_IZ2 değişmez; yalnız kendi yolları commit |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

(ön kayıt anında yok)
- EK SAPMA (26 Kas 09:54, ön kayıt cf5ad8d'den sonra, GETİRİ HESAPLANMADAN): ilk 'kos' denemesi K10 denetiminde durdu: set1-3'te boş olan 'bolge_bas_anahtar' alanı DataFrame'de NaN olunca 'dolu' sayıldı (NaN doğru-değerli). Yalnız bu koşul satırı düzeltildi (alan metinse denetle); tanımlar (ESIK11_SHA) aynı; komut durduğu için hiçbir getiri yazılmadı / görülmedi. Yeni kod mührü:
KOD11_SHA: e018fdf4a58650d7f2841f524ccc37094918a9287cfbd45fd3f8706fbbed05c0
