# MUM_IZI4 ÖN KAYIT (2026-11-25T11:17:54Z)

v2 tanımı (kapılar, eşik tablosu, sentetik sonuç, onay seçim kuralı) gerçek veride v2 BÖLGE SAYIMINDAN ÖNCE commit edilir (`mv_kapi`). Bu işte getiri / sonrası hesaplanmaz. Kapılar şablondan ve getirisiz açık veri ölçü dağılımından türetildi; v1 eşleşmelerinin getirisine bakılmadı.

## Mühürler

KOD4_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
ESIK4_SHA: 656584bafa35df1fbda028fa6ea3ca31f32ed0f2e0fd4c9cb9b7741f9bc7ab6f
KAPI_ESIK_SHA: 8b6cbdfc5d59ee0ac717862b1f2d3598ee1d59e23d1e13c6940cf88db5fe35cd
SENTETIK4_SHA: a6c72463ad2a9d7059410f483877fd8c167d100cfcb57c8fa4ae522d95f20731
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200

- MUM_IZI_V2.py commit'i: 0eec910e6a3eb76e9119689920f7a0109af7f304 2026-11-25T11:17:43+00:00

## Kapılar ve eşikler (MV_ESIK; sha yukarıda)

```
{
 "surum": "MV-1.0",
 "ek_olcu": {
  "mum_bant": "ortalama (H - L) / (üst - alt bant), mum başına oranların ortalaması",
  "govde_bant": "ortalama |C - O| / (üst - alt bant)",
  "max_mum_bant": "en büyük (H - L) / (üst - alt bant)",
  "max_govde_bant": "en büyük |C - O| / (üst - alt bant)",
  "not": "A3'ün 3 ölçüsü + k4'ün 'en büyük gövde / bant' ölçüsü; bant = o mumdaki Bollinger (20, 2) genişliği; şablonda görüntüden"
 },
 "dagilim": {
  "n": 20000,
  "L": [
   14,
   15,
   16,
   17,
   18,
   19,
   20,
   22,
   24
  ],
  "gunluk": {
   "veri": "MUM_IZI açık kopya (/tmp/mum_izi/acik; ABD + AVR + BIST; <= 2022-12-30)",
   "uclar": [
    "2016-01-01",
    "2022-12-31"
   ],
   "tohum": 25112041
  },
  "haftalik": {
   "veri": "MUM_IZI_HAFTALIK tam kopya haftalık bar (ABD + AVR + BIST; 2000-2022)",
   "uclar": [
    "2001-01-01",
    "2022-12-31"
   ],
   "tohum": 25112042,
   "eksik_hafta": "pencerede eksik hafta (ardışık ISO haftaları arasında boşluk) varsa pencere atılır"
  },
  "yontem": "MUM_IZI2 yöntemi: geçerli (hisse, pencere sonu) çiftleri üç pazar birleşik havuz, pencere başı >= 19 (bant tanımlı), yerine koymadan düzgün 20.000; tohum = taban + L; yüzdelik p = (#< + 0,5 #=) / N"
 },
 "kapilar": {
  "k1": {
   "ad": "uzun üst fitil",
   "olcu": [
    [
     "ust_fitil",
     "Y"
    ],
    [
     "uzun_ust_pay",
     "Y"
    ]
   ]
  },
  "k2": {
   "ad": "kısa alt fitil",
   "olcu": [
    [
     "alt_fitil",
     "D"
    ]
   ]
  },
  "k3": {
   "ad": "küçük gövde / doji",
   "olcu": [
    [
     "govde_oran",
     "D"
    ],
    [
     "doji_pay",
     "Y"
    ]
   ]
  },
  "k4": {
   "ad": "küçük mumlar (banda göre de)",
   "olcu": [
    [
     "kucuk_mum_pay",
     "Y"
    ]
   ],
   "ek": [
    [
     "mum_bant",
     1.25
    ],
    [
     "max_govde_bant",
     1.25
    ]
   ]
  },
  "k5": {
   "ad": "yükselen dipler",
   "olcu": [
    [
     "yuk_dip_pay",
     "Y"
    ]
   ]
  },
  "k6": {
   "ad": "alt banttan üst banda",
   "ham": [
    [
     "pB_bas",
     "<=",
     0.25
    ],
    [
     "pB_son",
     ">=",
     0.75
    ]
   ]
  },
  "k7": {
   "ad": "mumlar birbirine biniyor",
   "olcu": [
    [
     "ortusme",
     "Y"
    ]
   ]
  },
  "esik": "Y (yüksek uç): ölçü >= min(q_L(0,75), şablon değeri); D (düşük uç): ölçü <= max(q_L(0,25), şablon değeri); q_L = aynı zaman dilimi ve aynı pencere uzunluğu L dağılımı (tam şablonda bütün kapı değerleri uç dilimde olduğu için eşik = q_L; tepesizde govde_oran (p 0,30) ve yuk_dip_pay (p 0,62) uç dilimde değil -> eşik şablon değeri: şablon kendi kapısından geçer, daha sıradan pencere geçmez); k4 ek: mum_bant <= şablon x 1,25, max_govde_bant <= şablon x 1,25; k6 ham değer",
  "kabul": "v2 kabul = v1 S >= eşik (tam 0,59 / tepesiz 0,56, AYNEN) VE aynı penceredeki 7 kapının hepsi; t'de L uzunluklarından biri kabul edilirse olay, m = en büyük S'li kabul edilen L; aynı hissede 15 bar tekil (ilk)"
 },
 "karsi_ornek": {
  "n1": "aynı kapanış yolu, gövde = şablon ortalama mum boyu (yeşil / kırmızı kapanış yönüne göre), fitil yok",
  "n2": "aynı O / C, üst ve alt fitil yer değiştirmiş",
  "n3": "aynı kapanış, O / H / L kapanış etrafında 2 kat (mum boyu 2 x)",
  "p1": "şablonun mum biçimleri (O / H / L kapanışa göre), kapanış yolu yatay (ilk kapanışta sabit)",
  "p1b": "aynı mum biçimleri, kapanış yolu düşen (şablon kapanış değişimlerinin tersi)",
  "A4": "şablonun görüntüdeki bantlarıyla S ve üç bileşen"
 },
 "sentetik": {
  "kok": 25112043,
  "tohum": 200,
  "gurultu": [
   0.0,
   0.1,
   0.2
  ],
  "uretec": [
   "blok",
   "ry"
  ],
  "baglam": [
   "dip",
   "yatay",
   "tepe"
  ],
  "negatif": [
   "n1",
   "n2",
   "n3"
  ],
  "yanlis_seri": 200,
  "yanlis_n": 1000,
  "kabul_olcutu": "n1 / n2 / n3 gömülü serilerde v2 kabul payı (gerçek sonun +-3 barında) <= %5 HER BİRİNDE; rastgele seride v2 tekil kabul (1.000 bar başına) <= v1'in 1 / 5'i (iki üretici ayrı). Yakalama düşerse yazılır; kapılar gevşetilmez"
 },
 "say": {
  "gunluk": {
   "donem": {
    "d1619": [
     "2016-01-01",
     "2019-12-31"
    ],
    "d2022": [
     "2020-01-01",
     "2022-12-31"
    ]
   }
  },
  "haftalik": {
   "donem": {
    "h0107": [
     "2001-01-01",
     "2007-12-31"
    ],
    "h0815": [
     "2008-01-01",
     "2015-12-31"
    ],
    "h1622": [
     "2016-01-01",
     "2022-12-31"
    ]
   }
  },
  "evren": "ABD / AVR: TEZGAH2 P2 (giriş günü; KART_TUR2) ; BIST: hepsi; sayılar evren içi ve bütün (v1 ile aynı tanım); v1 oranı = v2 / v1 aynı hücre",
  "getiri": "HESAPLANMAZ"
 },
 "onay": {
  "tohum": 25112044,
  "haftalik": 12,
  "gunluk": 12,
  "once": 15,
  "secim": "v2 kabul edilen TAM şablon bölgeleri (evren içi) -> zaman dilimi başına hisse başına ilk olay -> tohumla RASTGELE (S'ye göre değil) 12 haftalık + 12 günlük; günlük listede haftalıkta seçilen hisseler dışarıda; sayfa sırası tohumla karıştırılır; 24'ten azsa hepsi",
  "sayfa": "solda Cemal'in kalıbı (şablon mumları + bant), sağda bölge (öncesi 15 mum, bölge kutulu, bölge sonunda kesik), Bollinger 20 + SMA20, hisse / tarih yok, altta ✓ benziyor / ✗ benzemiyor kutusu",
  "esik": "Cemal 24'ün >= 19'una ✓ derse (%80) tespit GEÇERLİ; değilse ✗ sayfalarındaki ortak neden bir sonraki kapı (bu işte ölçülmez)"
 }
}
```

Şablonun kendi kapıları: {'gunluk': {'tam': {'k1': True, 'k2': True, 'k3': True, 'k4': True, 'k5': True, 'k6': True, 'k7': True}, 'tepesiz': {'k1': True, 'k2': True, 'k3': True, 'k4': True, 'k5': True, 'k6': True, 'k7': True}}, 'haftalik': {'tam': {'k1': True, 'k2': True, 'k3': True, 'k4': True, 'k5': True, 'k6': True, 'k7': True}, 'tepesiz': {'k1': True, 'k2': True, 'k3': True, 'k4': True, 'k5': True, 'k6': True, 'k7': True}}}

Kapı eşik tablosu (tam, günlük, L 20): {"ust_fitil": 0.3108490886540124, "uzun_ust_pay": 0.25, "alt_fitil": 0.2305730344014381, "govde_oran": 0.4070980724918211, "doji_pay": 0.15, "kucuk_mum_pay": 0.35, "yuk_dip_pay": 0.5789473684210527, "ortusme": 0.7525612186591876, "mum_bant": 0.5142472717031331, "max_govde_bant": 0.4918612144590798}

## Sentetik v2 testi (C2; gerçek veriden önce)

- tam: yakalama v1 0.905 -> v2 0.192; n1 0.000 -> 0.000; n2 0.004 -> 0.000; n3 0.696 -> 0.071; rastgele 1.000 bar v1 / v2: blok 1.96 / 0.005, ry 3.35 / 0.005; KABUL ÖLÇÜTÜ GEÇMEDİ {'negatif_le_5': {'n1': True, 'n2': True, 'n3': False}, 'rastgele_le_1_5': {'blok': True, 'ry': True}, 'gecti': False}
- tepesiz: yakalama v1 0.911 -> v2 0.105; n1 0.002 -> 0.000; n2 0.016 -> 0.000; n3 0.754 -> 0.038; rastgele 1.000 bar v1 / v2: blok 5.52 / 0.029, ry 9.64 / 0.044; KABUL ÖLÇÜTÜ GEÇTİ {'negatif_le_5': {'n1': True, 'n2': True, 'n3': True}, 'rastgele_le_1_5': {'blok': True, 'ry': True}, 'gecti': True}

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | v2 sentetik testinde negatif kontroller (n1 / n2 / n3 aynı gidiş farklı mum yapısı) ve rastgele seri tabanı SAYIYLA; v1 ile yan yana; getiri / eş bu işte yok (bölge sayımı) |
| K2 | geleceğe bakma | EVET | kapı ölçüleri ve S pencere içi, t'ye kadarki barlar (MI.mi_bant / mi_ozellik); mv_prefix 30 olayda veri t'de kesilince kabul ve S aynı (assert); veri <= 2022-12-31 + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar süzgeci; haftalıkta eksik hafta içeren pencere atılır (bağımsız denetçi bulgusu, v2'de kural) |
| K4 | tekilleştirme | EVET | aynı hissede 15 bar (günlük) / 15 hafta tekil (ilk kabul) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri hesaplanmaz (bölge sayımı ve görsel onay) |
| K6 | veri birimi | EVET | ölçüler ölçek bağımsız; EK ölçüler mum / bant oranı; TEZGAH2 bölünme düzeltmeli fiyat |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; sayım bilgi; onay seti görsel (getiri yok) |
| K8 | örneklem ve dönem | EVET | sentetik 200 tohum / koşul; kabul ölçütü önceden; gerçek veride yalnız sayım (pazar x dönem) |
| K9 | ön kayıt | EVET | MUM_IZI4_ON_KAYIT.md: KOD4_SHA, ESIK4_SHA, kapı eşik tablosu sha, sentetik sonuç sha, onay seçim tohumu; gerçek veri sayımından ÖNCE commit; mv_kapi kontrol + sha + git |
| K10 | ayrıştırma | EVET | itiraz edilen bölge mum renk dizisiyle bulundu (15 / 15); onay PDF'i Cemal'in gözü (✓ / ✗) = görsel doğrulama |
| K11 | yeniden üretim | EVET | mv_tara_seri S'si kapısız durumda MI.mi_tara_seri ile birebir (test); 2 hücre sayımı olay dosyasından düz pandas |
| K12 | ifade | EVET | v1 sonuçları 'v1 dedektörünün bölgeleri için' diye yazılır; kalıp için hüküm yok (ÖLÇÜLEMEDİ); 'iz' sözü yok |
| K13 | süreç | EVET | çakışma kapısı; v1 dosyaları / defterler / UC_IZ2 değişmez; yalnız kendi yolları git add |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## SAPMA

(ön kayıt anında yok)
## Notlar (sayımdan önce)

- Sentetik kabul ölçütü TAM şablonda GEÇMEDİ (n3 = aynı gidiş, mumlar banda göre 2 kat: v2 kabul %7,1 > %5); tepesizde geçti. İş tanımı gereği kapılar gevşetilmedi; sayım ve onay seti bu v2 ile yapılır, rapor bunu yazar.
- v2 yakalama düştü: tam %90,5 -> %19,2, tepesiz %91,1 -> %10,5 (en çok 'tepe' bağlamında ve %20 gürültüde). Rastgele seride v2 kabulü v1'in ~1 / 400'ü.
- Onay seçimi yalnız tohumla (S'ye ve getiriye bakılmaz); onay PDF'inde hisse adı, tarih ve sonrası yok; anahtar ayrı json'da.
- Bu işte getiri / sonrası hesaplanmaz (v2 için).
