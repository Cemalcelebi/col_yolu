# ÇÖKÜŞ SONRASI OYNAK HİSSE — ÖN KAYIT (COKUS_OYNAK v1.0 (16 Kas 2026))

Zaman (UTC): 2026-11-16T13:13:43.943733+00:00. İş tanımı: COKUS_OYNAK_IS_TANIMI.md (commit 69fbed0). Bu dosya getiri hesaplanmadan yazıldı: yalnız çöküş günü SAYIMI.
Git commit alt ajana yasak: bu dosyanın commit'i ana modelde; kos mühür / kod sha denetler.

## MÜHÜR

- CO_ESIK sha256: `302eaeada2b3525bedbf34f47b34f5e125155a826e8b2bebe50176ca63ddf4df`
- COKUS_OYNAK.py sha256: `f8da008ed67f594d8555e9f38d2199d213690333164532dc7215be7455975cf5`
- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- G.pkl sha256: `cdde36f074df0a435274ffbb19ed4734b0291964db7e8093acd2a9e623c9fc3c`
- dol.pkl sha256: `fcdcf8344d08de62856dd7654b8efe28b38f78c7c5ff22e5a8b15fa77eb20d3c`
- canlı bist_3y.pkl sha256: `9d504294860cd699849147deaeb4957bc7f0f15ebacb5d7c61a423d3f637cb70`

## EŞİKLER (CO_ESIK; sonuç görüldükten sonra değişmez)

```json
{
 "kriz": "2026-08-31",
 "gecerli_bar": "H>L ve V>0 ve O,C>0 ve sonlu",
 "cokus": {
  "gun": 120,
  "esik": -0.3,
  "ara": 250,
  "min_hisse": 50,
  "tanim": "evren medyan 120 işlem günü getirisi (ortak takvim, kapanış en çok 10 gün ileri taşınır, t'de geçerli barı olan hisse) <= -%30 olan İLK gün; sonraki çöküş için en az 250 işlem günü ara. Tespit kesiksiz veriyle (yalnız geçmiş fiyat); sonuç kesik veriyle."
 },
 "giris_gecikme": 5,
 "giris_gecikme_ek": 20,
 "giris_tolerans": 5,
 "bayat_gun": 5,
 "sigma_gun": 250,
 "zirve_gun": 250,
 "likidite_gun": 60,
 "likidite_alt": 0.2,
 "r_kisa": 60,
 "ufuk": 250,
 "ufuk_kisa": 120,
 "mdd_gun": 60,
 "yukari": 1.0,
 "asagi": -0.5,
 "dilim": {
  "OYNAK": "σ250 sıra yüzdeliği > 0,80 (likidite süzgecinden sonra, giriş günü evreni)",
  "TABAN": "σ250 sıra yüzdeliği (0,20, 0,80]",
  "DUSMUS": "250 gün zirveden düşüş sıra yüzdeliği <= 0,20 (en çok düşmüş beşlik)",
  "TABAN_D": "düşüş sıra yüzdeliği (0,20, 0,80]",
  "CAPRAZ": "OYNAK ve DUSMUS (taban: TABAN)",
  "PROFIL": "OYNAK ve zirveden düşüş <= -%60 (bugünün piyango profili; bilgi, taban: TABAN)"
 },
 "bolunme": "SIKISMA_YENIDEN.sy_bolunme_supheli ANA kuralı; şüpheli günü [giriş-260 bar, giriş+250 takvim günü] içinde olan hisse olaydan çıkar (sayılır, yazılır)",
 "bootstrap": {
  "n": 1000,
  "tohum": 20261116,
  "duzey": "hisse; birleşikte olay içinde katmanlı",
  "yuzde": [
   2.5,
   97.5
  ]
 },
 "permutasyon": {
  "n": 1000,
  "tohum": 20261117,
  "tanim": "olay içinde OYNAK / TABAN etiketleri karıştırılır (bilgi)"
 },
 "bilgi_olay": {
  "2018B": "2018-08-20",
  "2020B": "2020-03-19",
  "tanim": "BİLGİ, karar dışı (olay sayımından sonra, getiri görülmeden eklendi): ana tanım 2018 ve 2020'yi çöküş saymadı (2018 yıl en düşük medyan r120 -%28,5; 2020 -%1,7). Bu günler yılın en düşük medyan r120 günüdür, yani GERİYE BAKARAK seçildi (dip o gün bilinmezdi); aynı +5 gün girişiyle aynı tablo, etiket yalnız bilgi"
 },
 "normal": {
  "yillar": [
   2017,
   2023
  ],
  "giris": "yılın ilk ortak takvim işlem günü açılışı (karar = önceki işlem günü)"
 },
 "karar_kurali": {
  "birincil": "OYNAK vs TABAN, birleşik (iki tamamlanmış çöküş), ana giriş (+5 gün)",
  "Ha": "birleşik P(+%100) farkı > 0 VE bootstrap %95 alt uç > 0 VE her çöküş olayında nokta fark > 0",
  "Hb": "birleşik P(-%50) farkının bootstrap %95 alt ucu <= 0 (anlamlı yüksek değil)",
  "etiket": "Ha ve Hb -> EMARE; Ha ve Hb değil -> PİYANGO; Ha değil -> DESTEKLENMEDİ; tamamlanmış çöküş < 2 ya da herhangi olayda OYNAK veya TABAN n < 30 -> ÖLÇÜLEMEDİ",
  "ikincil": "DUSMUS ve CAPRAZ aynı kuralla ayrı etiket (bilgi); üç (a) testinin tek yönlü bootstrap p'leri BH ile (bilgi)",
  "not": "iki çöküş = iki olay: tutsa bile İZ denmez, en fazla EMARE"
 },
 "bugun": {
  "tarih": "2026-11-16",
  "karar": "2026-11-13",
  "dusus_esik": -0.6,
  "uzak": [
   "TEHOL",
   "PEKGY",
   "ODINE",
   "ANELE",
   "MANAS",
   "IEYHO",
   "GUNDG",
   "DSTKF",
   "OZATD",
   "TRHOL",
   "SKYLP"
  ],
  "ilk": 15,
  "son_gun": 20,
  "profil": "σ250 en üst beşlik (likidite süzgecinden sonra) VE 250 gün zirveden >= %60 düşmüş VE likidite alt %20 dışı VE fon lekesi (son fon raporunda tasfiye fonu pozisyonu) yok VE Uzak listede yok; sıra σ250 büyükten"
 }
}
```

## OLAY SAYIMI (getirisiz)

Ortak takvim 2015-06-01 .. 2026-10-22 (2855 gün, en az 50 hisseli gün). Evren medyan 120 gün getirisinin en düşük değeri: -0.380 (2026-10-22).

| Çöküş günü | Medyan r120 | Hisse | Giriş (+5) | Sonuç ölçülür |
|---|---|---|---|---|
| 2023-05-22 | -0.303 | 464 | 2023-05-29 | EVET |
| 2026-10-13 | -0.316 | 561 | 2026-10-20 | HAYIR (kriz kesiği / ufuk) |

Sonucu ölçülebilir çöküş sayısı: 1. Karar kuralı gereği < 2 ise birincil etiket ÖLÇÜLEMEDİ olur (tanım değiştirilmez; iş tanımının beklediği 2018 / 2020 ana tanımda çöküş değildir).
Getiri görülmeden eklenen BİLGİ hücreleri (karar dışı): CO_ESIK['bilgi_olay'] — 2018-08-20 ve 2020-03-19 (yılın en düşük medyan r120 günü; geriye bakarak seçildi). Normal dönem 2023 girişi (2023-01-02) 250 gün penceresi 2023 çöküşünü içerir; kıyas buna göre okunur.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban = aynı giriş günü, aynı evren (likidite süzgeci sonrası) σ250 orta üç beşlik; aynı giriş açılışı ve 250 gün geometrisi; mekanik üstünlük: yüksek σ iki kuyruğu birden büyütür, bu yüzden normal dönem (2017, 2023) aynı tabloyla kıyaslanır; olasılık ölçüsünde portföy yerine olay içi permütasyon (1000) |
| K2 | geleceğe bakma | EVET | ölçüler yalnız karar günü (giriş-1) ve öncesi barlardan (co_hisse_olay içinde x.index.max() <= karar mekanik denetim, COHata); çöküş günü yalnız geçmiş 120 gün; fon tablosu bilinme <= karar denetimi (co_fon_leke); evren bugünün listesi (K7) |
| K3 | geçerli bar | EVET | geçerli bar H>L, V>0, O,C>0 (co_gecerli); karar gününden 5 işlem gününden eski son bar -> hisse dışarıda; bugünün listesi 13 Kas tam bar (16 Kas yarım bar atılır) |
| K4 | tekilleştirme | EVET | çöküşler arası en az 250 işlem günü; her hisse olay başına bir kez; n = hisse sayısı; ortalama yanında medyan r250 |
| K5 | giriş fiyatı | EVET | giriş = çöküş + 5. işlem günü AÇILIŞI (karar günü kapanışı değil); bar yoksa 5 gün içindeki ilk geçerli açılış |
| K6 | veri birimi | EVET | V_BIST tek kip düzeltilmiş fiyat; bölünme şüphesi SY.sy_bolunme_supheli ANA ile [giriş-260 bar, ufuk sonu] içinde olan hisse çıkar ve sayısı yazılır; likidite TL (dilim içi sıralama, birim farkı etkilemez) |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_BIST 581); 2018 / 2020 batanları yok -> P(-%50) aşağı, P(+%100) yukarı yanlı; RAPOR'da HAYATTA KALMA UYARISI bölümü |
| K8 | örneklem ve dönem | EVET | hücre n < 30 -> ÖLÇÜLEMEDİ; iki çöküş ayrı hücre + birleşik, Ha her olayda aynı yön şartı; üç (a) testi BH (bilgi); iki olay = en fazla EMARE |
| K9 | ön kayıt | EVET | iş tanımı commit 69fbed0 koşudan önce; CO_ESIK sha256 mühürü + kod sha + veri sha ON_KAYIT.md'de, kos mühür farklıysa durur; git commit alt ajana yasak -> ON_KAYIT commit'i ana modelde (zaman damgası dosyada) |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırması yok; yalnız fiyat-hacim; fon tablosu FON_IZI.FI_TASFIYE_RE ile mevcut ayrıştırılmış G.pkl'den |
| K11 | yeniden üretim | EVET | olay satırları csv.gz'ye yazılır; test_cokus_oynak.py en az iki hücreyi (2018 ve 2020 OYNAK P100 / M50) satır dosyasından bağımsız yeniden üretir |
| K12 | ifade | EVET | fiyat değişimi (kapanış / giriş) ile gerçekleşen kâr ayrı; 'emare / piyango' yalnız önceden yazılı kuralla; sayı ve yorum ayrı cümle; hiçbir isme alım dili yok |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_co); defter dosyaları ve mevcut .py değişmez; e-posta / anahtar taraması testte; commit / push yok; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri işi değil, aday listesi; boyut / çıkış kuralı yok, alım dili yok; taban oran (3 yılda 10x ~%1-1,85) RAPOR'da yazılı |
