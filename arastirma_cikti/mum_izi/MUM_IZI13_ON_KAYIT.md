# MUM_IZI13 ÖN KAYIT (2026-11-26T11:17:03Z)

MUM_IZI11_ON_KAYIT tanımları AYNEN (MUM_IZI_GOZ.py GZ_ESIK; ESIK11_SHA aşağıda; giriş, ufuk 15 mum, stop, dokunma, R30, CETVEL2 konum eşi, tablolar, permütasyon). Ek: set 5 = MUM_IZI12_ONAY 24 bölge. Bu dosya set 5'in getirileri hesaplanmadan ÖNCE commit edilir.

## Mühürler

KOD13_SHA: 73879d50d941e0fb939de0a8687184c74f3817f7cd3c5b18f25b3bcf93a2fc0e
EK13_SHA: f87dc6955ebad9306d117a5815bc59f129b9332dcc1dd559c886cad247f93447
GZ_KOD_SHA: f0b0381a4eabe14a015dc6eb929fcc34a1d95d2a399412cc05a5620c4ffb68d5
ESIK11_SHA: ea7535ce7ba59c64e6c5e934aa3722cbedb3786ddfe1f52d05b676d8bb315d75
ISARET_SET5_SHA: 0f152583da716ea0bc7935f2c394bb0b616d1ccd552c770a2e2ec35b6d22b4c1
ANAHTAR_SET5_SHA: 47a93df34cfab876911cb368e07da3eab3dec7188c1354c33654c223a9978286
SONUC11_SHA: 923e5cec9c64bfa6b8836898072c4688f4664f4deea444a8a29d570e1d0a0967
OLAY11_SHA: 038ca81f5e863dd73798b464bf1fdd200790965feca0372c6407149c0a70e1a6

- MUM_IZI_GOZ2.py commit'i: 8ae5ecf982bb89a2cc823201da6bd4a4a13eb607 2026-11-26T11:17:03+00:00

## Üç rapor satırı ailesi

- (i) İLK BAKIŞ = set 1-4: MUM_IZI11 sonucu (mum_izi11_sonuc.json), DEĞİŞMEZ.
- (ii) İKİNCİ BAKIŞ = yalnız set 5: ilk bakıştan bağımsız yeni örnek. Soru: ilk bakıştaki yön tekrar ediyor mu (haftalıkta EVET eşlerin ve HAYIR'ın gerisinde: EVET eşli fark -%16,2, EVET - HAYIR eşli -15,7 puan; günlükte belirgin fark yok: EVET - HAYIR eşli +5,7 puan, p 0,29). 'Aynı yön' = ilgili farkın İŞARETİ aynı.
- (iii) BİRLEŞİK = set 1-5 (128 bölge). Eş dışlama kümesi 128 olayla kurulur; set 1-4 olaylarının değerleri MUM_IZI11 ile karşılaştırılır, fark varsa yazılır.
- Ek ölçü: EVET - eş (EVET'lerin eşli farkı 0'dan farklı mı): olay bootstrap %95 + işaret çevirme permütasyonu (iki yönlü, 10.000, tohum 25112131); EVET + KISMEN ve HAYIR için de aynı (bilgi).

## Sınıf sayıları (getirisiz)

- Set 5: {"toplam": 24, "sinif": {"EVET": 11, "KISMEN": 8, "HAYIR": 5}, "set_sinif": {"set5|EVET": 11, "set5|HAYIR": 5, "set5|KISMEN": 8}, "sinif_zaman": {"EVET|gunluk": 5, "EVET|haftalik": 6, "HAYIR|gunluk": 4, "HAYIR|haftalik": 1, "KISMEN|gunluk": 5, "KISMEN|haftalik": 3}, "set_sinif_zaman": {"set5|EVET|gunluk": 5, "set5|EVET|haftalik": 6, "set5|HAYIR|gunluk": 4, "set5|HAYIR|haftalik": 1, "set5|KISMEN|gunluk": 5, "set5|KISMEN|haftalik": 3}, "pazar": {"EVET|ABD": 9, "EVET|AVR": 1, "EVET|BIST": 1, "HAYIR|ABD": 5, "KISMEN|ABD": 7, "KISMEN|AVR": 1}, "tekrar_degisen": 0}
- Birleşik (set 1-5): {"toplam": 128, "sinif": {"HAYIR": 76, "EVET": 36, "KISMEN": 16}, "set_sinif": {"set1|EVET": 7, "set1|HAYIR": 17, "set2|EVET": 9, "set2|HAYIR": 28, "set3|EVET": 2, "set3|HAYIR": 17, "set4|EVET": 7, "set4|HAYIR": 9, "set4|KISMEN": 8, "set5|EVET": 11, "set5|HAYIR": 5, "set5|KISMEN": 8}, "sinif_zaman": {"EVET|gunluk": 16, "EVET|haftalik": 20, "HAYIR|gunluk": 40, "HAYIR|haftalik": 36, "KISMEN|gunluk": 10, "KISMEN|haftalik": 6}, "set_sinif_zaman": {"set1|EVET|gunluk": 5, "set1|EVET|haftalik": 2, "set1|HAYIR|gunluk": 7, "set1|HAYIR|haftalik": 10, "set2|EVET|gunluk": 3, "set2|EVET|haftalik": 6, "set2|HAYIR|gunluk": 16, "set2|HAYIR|haftalik": 12, "set3|EVET|gunluk": 1, "set3|EVET|haftalik": 1, "set3|HAYIR|gunluk": 8, "set3|HAYIR|haftalik": 9, "set4|EVET|gunluk": 2, "set4|EVET|haftalik": 5, "set4|HAYIR|gunluk": 5, "set4|HAYIR|haftalik": 4, "set4|KISMEN|gunluk": 5, "set4|KISMEN|haftalik": 3, "set5|EVET|gunluk": 5, "set5|EVET|haftalik": 6, "set5|HAYIR|gunluk": 4, "set5|HAYIR|haftalik": 1, "set5|KISMEN|gunluk": 5, "set5|KISMEN|haftalik": 3}, "pazar": {"EVET|ABD": 22, "EVET|AVR": 6, "EVET|BIST": 8, "HAYIR|ABD": 56, "HAYIR|AVR": 10, "HAYIR|BIST": 10, "KISMEN|ABD": 14, "KISMEN|AVR": 1, "KISMEN|BIST": 1}, "tekrar_degisen": 2}

## Örneklem özeti (düz)

- Set 5: 24 bölge: EVET 11 (günlük 5, haftalık 6), KISMEN 8 (5 / 3), HAYIR 5 (4 / 1). Pazar: ABD 21, AVR 2, BIST 1.
- Birleşik (set 1-5): 128 bölge: EVET 36, KISMEN 16, HAYIR 76. Setler arasında aynı bölge yok (denetlendi).
- Set 5'in bütün hücreleri n < 30 ('örneklem yetersiz'); HAYIR haftalık n 1 (karşılaştırma yapılamayabilir: permütasyon en az 2'şer olay ister).

## Uygulama kararları

1. Kod: MUM_IZI_GOZ2.py, MUM_IZI_GOZ.py fonksiyonlarını DEĞİŞTİRMEDEN çağırır (gz_ornek, gz_olc, gz_es, gz_tablolar); set 5 satırları set 4 biçiminde eklenir.
2. Birleşik koşuda set 1-4 olayları yeniden hesaplanır (aynı gün eş dışlama kümesine set 5 olayları da girer); değerler MUM_IZI11 olay dosyasıyla karşılaştırılır, farklı satır sayısı yazılır. İLK BAKIŞ tablosu MUM_IZI11 json'undan aynen alınır.
3. 'Aynı yön' = farkın işareti; p ve büyüklük ayrıca yazılır.

## Ek tanımlar (G2_EK; sha yukarıda)

```
{
 "surum": "G2-1.0",
 "tanim": "MUM_IZI_GOZ GZ_ESIK aynen (ESIK11_SHA ön kayıtta)",
 "set5": "MUM_IZI12_ONAY (s2-25; anahtar: yeni_sayfa, bolge_bas (ilk barın tarihi), bolge_son, pencere); işaret EVET / KISMEN / HAYIR",
 "aileler": {
  "ilk_bakis": "set 1-4: MUM_IZI11 sonucu (mum_izi11_sonuc.json), değişmez",
  "ikinci_bakis": "yalnız set 5 (yeni, bağımsız örnek)",
  "birlesik": "set 1-5 (eş dışlama kümesi 128 olayla; set 1-4 olayları MUM_IZI11 ile karşılaştırılır, fark yazılır)"
 },
 "evet_es": {
  "tanim": "EVET (ve EVET + KISMEN) eşli farkının ortalaması; %95 olay bootstrap (GZ ile aynı); p = işaret çevirme permütasyonu (eşli farkların işaretleri rastgele çevrilir), iki yönlü, 10.000, tohum 25112131",
  "perm": 10000,
  "tohum": 25112131
 },
 "yon": "ilk bakışla aynı yön mü: her dilimde EVET - HAYIR eşli fark farkının ve EVET eşli farkının İŞARETİ ilk bakışla aynı mı (büyüklük / p değil)"
}
```

## KONTROL LİSTESİ (MUM_IZI11 ile aynı; K8: set 5 hücreleri n < 30)

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
