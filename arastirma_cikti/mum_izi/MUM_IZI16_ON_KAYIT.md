# MUM_IZI16 ÖN KAYIT (2026-11-26T12:15:39Z)

MUM_IZI EK 16 İŞ A: ölçek. Ölçüler yalnız bölge ve öncesi barlarından; mum_izi13_olay.csv'nin getiri sütunlarına (R15, es_R15, fark, ...) bu aşamada BAKILMADI (csv yalnız getirisiz sütunlarla okundu: set, set_ad, sayfa, isaret, sinif, sinif_son, zaman, pazar, sembol, bolge_bas, bolge_son, m, olculdu, neden, es_neden). Bu dosya sonrası tabloları hesaplanmadan ÖNCE commit edilir.

## Mühürler

KOD16_SHA: 08d1938bd863cb7c7e2ff6e8762a2335a130c9f403c56cc00734f7c911c93295
EK16_SHA: 5d78d66976d3dd63239194bc33a0be8aa8701d8778c37e54d0b79b7990edb06a
OLAY13_SHA: fc27c506ae981157f13b2aeb534e2c9c098a947ad0b158130f0c5845f73dcec8
SONRASI13_PDF_SHA: a4cf20e0136cf600e05652e7d3305e836a533ce9eb3b617de63e662b04a1f5f7
ANAHTAR8_SHA: 6083f0d088f648cefd6591dea806da8715c121a90bbec616943ab319bf29f56c
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
V5_KOD_SHA: 2bd267ad5057ef6e5571b92545224b3ce4a2ce0702b295653553237c9a62a6d3

- MUM_IZI_GOZ2.py commit'i: 9b96b3bcd6da962492df8b7f74103611b26d51a4 2026-11-26T12:13:58+00:00

## Tanımlar (iş tanımı 1. bölüm; K16_EK, sha yukarıda)

```
{
 "surum": "K16-1.0",
 "kaynak": "mum_izi13_olay.csv (128 bölge); A1 ve grup sayımı yalnız getirisiz sütunlarla (usecols: K16_GETIRISIZ); R15 / es_R15 / fark ön kayıt commit'inden SONRA okunur (aynen; yeni getiri hesabı yok)",
 "veri": "bölge barları mumun kendi zaman diliminde: günlük MV.mv_veri('gunluk') (açık kopya), haftalık MV.mv_veri('haftalik') (MH tam -> ISO hafta); onay sayfalarının kullandığı yol; bölge = bolge_son barında biten m bar; bolge_bas csv ile denetlenir (uyuşmazsa DUR)",
 "olcu": {
  "r": "r = (H - L) / C (her bar)",
  "BOY_MUTLAK": "bölge barlarında r medyanı x 100 (%)",
  "BOY_OZ": "ANA ÖLÇÜ: bölge r medyanı / bölgeden hemen önceki en çok 120 barın r medyanı; önceki sonlu bar < 40 ise boş (NaN). < 1: hisse kendi olağanından sakin",
  "SON_BOY_OZ": "bölgenin son ceil(m / 3) barının r medyanı / aynı payda (BOY_OZ paydası)",
  "BOY_BANT": "bölge barlarında (H - L) / (BU - BA) medyanı; Bollinger 20, 2 sigma (MI.mi_bant: yalnız o güne kadarki kapanışlar); bant genişliği sonlu ve > 0 barlar",
  "BOY_SAYFA": "bölge barlarında (H - L) medyanı / onay sayfasındaki büyük grafiğin dikey açıklığı (y1 - y0). y sınırları sayfayı çizen fonksiyonla aynı yoldan yeniden üretilir: pencere = bölgeden önceki 15 bar + bölge (bölge sonunda kesik), MV._mv_ciz (mumlar + Bollinger 20 + SMA20 + bölge kutusu; matplotlib otomatik ölçek); set3 (MUM_IZI8_ONAY, V5.v5_onay) ayrıca V5._v5_okuma_ciz (y = [lo - 0,2 (hi - lo), hi + 0,05 (hi - lo)], kutusuz); set1 MV.mv_onay, set2 ETIKET2, set4 / set5 HAKEM._hk_sayfa (kutulu) aynı MV._mv_ciz yolu",
  "SISME": "sayfanın dikey açıklığı / bölgenin (en yüksek H - en düşük L) açıklığı",
  "gelecek": "her bölgenin dizileri bolge_son barında KESİLİR (o bar dahil) ve ölçü yalnız bu kesik diziden hesaplanır; sonraki bar kullanılmaz (assert + test)"
 },
 "A1": {
  "spearman": "128 bölgede BOY_SAYFA ile BOY_MUTLAK ve BOY_OZ (iki değer sonlu olanlar); zaman dilimi ayrı satır bilgi",
  "terciller": "'sayfada küçük ama kendi geçmişine göre büyük' = BOY_SAYFA <= 128 bölgenin 1/3 dilimi (np.quantile, doğrusal) VE BOY_OZ >= 2/3 dilimi",
  "sinif": "EVET / KISMEN / HAYIR x günlük / haftalık (+ birlikte): n ve 6 ölçünün medyanı; EVET - HAYIR medyan farkı + Mann-Whitney U (iki yönlü, scipy varsayılan yöntem)",
  "notlu": {
   "pdf": "MUM_IZI13_SONRASI.pdf",
   "fiziksel_sayfa": [
    4,
    5,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14
   ],
   "eslesme": "sayfa başlığı (sınıf · sembol (pazar) · zaman · bölge bas .. son) pypdf ile okunur; csv set5 satırına sembol + zaman + bölge başı + sonu ile BİREBİR (tek satır) eşlenir; değilse DUR"
  }
 },
 "A2": {
  "gruplar": {
   "EVET": [
    "EVET"
   ],
   "EVET+KISMEN": [
    "EVET",
    "KISMEN"
   ],
   "HEPSI": [
    "EVET",
    "KISMEN",
    "HAYIR"
   ]
  },
  "zaman": [
   "gunluk",
   "haftalik"
  ],
  "aile": "5 ölçü (BOY_OZ, BOY_MUTLAK, SON_BOY_OZ, BOY_BANT, BOY_SAYFA) x 2 zaman dilimi; SISME A2'ye girmez (sayfa özelliği, mum boyu değil)",
  "spearman": "ölçü ile eşli fark (fark sütunu) arasında Spearman (olculdu, fark ve ölçü sonlu; n < 3 -> boş)",
  "bolme": "grup x zaman dilimi içinde ölçünün (sonlu değerler) medyanı; KÜÇÜK = ölçü <= medyan, BÜYÜK = ölçü > medyan; ölçüsü boş bölge yarıya girmez",
  "hucre": "her yarı: n (ölçülen), n_es, R15 ort / medyan, artıda payı (R15 > 0), eşli fark ort / medyan, eşinden iyi payı (fark > 0) (k15_hucre aynen)",
  "fark": "KÜÇÜK - BÜYÜK eşli fark ortalaması farkı; p = etiket permütasyonu GZ.gz_perm, iki yönlü, 10.000, tohum 16 (her karşılaştırmada aynı); bir yarıda n_es < 2 -> 'karşılaştırma yapılamaz'",
  "perm": 10000,
  "tohum": 16,
  "n_min": 2,
  "bh": "aile içi (5 ölçü x 2 zaman) Benjamini-Hochberg düzeltilmiş p, yalnız bilgi"
 },
 "okuma": "'YÖN CEMAL'İN DEDİĞİ GİBİ' <=> ANA ÖLÇÜDE (BOY_OZ) EVET bölgelerinde KÜÇÜK yarının eşli fark ortalaması > BÜYÜK yarının, günlükte VE haftalıkta; biri hesaplanamazsa 'OKUNAMADI'; öteki ölçüler bilgi (çoklu karşılaştırma)",
 "etiket": "BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK",
 "sinir": "Cemal sonrasını gördü ve gerçek grafiğe yalnız gitmeyenlerde baktı -> sonrası tablosu GERİYE DÖNÜK; eşler bölgenin kendi koşusuyla eşlenmedi (Ç229 / Ç240)"
}
```

Yorum notu (ön kayıt anında): iş tanımı A2 ailesini '5 ölçü x 2 zaman dilimi' diye sayar; altı ölçüden SISME (sayfa açıklığı / bölge açıklığı: bir sayfa özelliği, mum boyu değil) A2 dışında tutuldu, A1'de olgu olarak raporlanır.

## A1 OLGU (getirisiz)

### Spearman (BOY_SAYFA ile gerçek boy)

| ilişki | zaman | n | Spearman rho | p (bilgi) |
|---|---|---|---|---|
| BOY_SAYFA~BOY_MUTLAK | birlikte | 128 | -0,051 | 0,5689 |
| BOY_SAYFA~BOY_OZ | birlikte | 126 | -0,023 | 0,7988 |
| BOY_SAYFA~BOY_MUTLAK | gunluk | 66 | -0,069 | 0,5813 |
| BOY_SAYFA~BOY_OZ | gunluk | 66 | 0,061 | 0,6260 |
| BOY_SAYFA~BOY_MUTLAK | haftalik | 62 | -0,349 | 0,0055 |
| BOY_SAYFA~BOY_OZ | haftalik | 60 | -0,146 | 0,2648 |

### 'Sayfada küçük ama kendi geçmişine göre büyük'

- İki ölçüsü de dolu 126 bölge; BOY_SAYFA 1/3 dilimi 0,0664, BOY_OZ 2/3 dilimi 1,217: **14 bölge** ({"EVET|gunluk": 1, "EVET|haftalik": 4, "HAYIR|gunluk": 4, "HAYIR|haftalik": 2, "KISMEN|gunluk": 1, "KISMEN|haftalik": 2}).

### Cemal sınıfına göre ölçü medyanları

| sınıf | zaman | n | BOY_MUTLAK | BOY_OZ | SON_BOY_OZ | BOY_BANT | BOY_SAYFA | SISME |
|---|---|---|---|---|---|---|---|---|
| EVET | gunluk | 16 | 3,377 | 0,839 | 0,815 | 0,198 | 0,065 | 2,949 |
| EVET | haftalik | 20 | 10,284 | 1,137 | 1,038 | 0,205 | 0,073 | 2,384 |
| EVET | birlikte | 36 | 5,311 | 1,004 | 0,917 | 0,201 | 0,065 | 2,660 |
| KISMEN | gunluk | 10 | 1,959 | 0,959 | 0,902 | 0,198 | 0,064 | 2,663 |
| KISMEN | haftalik | 6 | 11,485 | 1,167 | 0,984 | 0,174 | 0,061 | 3,699 |
| KISMEN | birlikte | 16 | 2,974 | 1,075 | 0,942 | 0,174 | 0,063 | 3,052 |
| HAYIR | gunluk | 40 | 2,539 | 1,065 | 1,044 | 0,196 | 0,100 | 1,764 |
| HAYIR | haftalik | 36 | 7,786 | 1,207 | 1,064 | 0,195 | 0,105 | 1,633 |
| HAYIR | birlikte | 76 | 4,524 | 1,075 | 1,051 | 0,196 | 0,104 | 1,706 |

### EVET - HAYIR (Mann-Whitney U, iki yönlü)

| ölçü | zaman | n EVET | n HAYIR | medyan EVET | medyan HAYIR | fark | Mann-Whitney p |
|---|---|---|---|---|---|---|---|
| BOY_MUTLAK | gunluk | 16 | 40 | 3,377 | 2,539 | 0,838 | 0,3597 |
| BOY_OZ | gunluk | 16 | 40 | 0,839 | 1,065 | -0,225 | 0,0045 |
| SON_BOY_OZ | gunluk | 16 | 40 | 0,815 | 1,044 | -0,229 | 0,0103 |
| BOY_BANT | gunluk | 16 | 40 | 0,198 | 0,196 | 0,001 | 0,7926 |
| BOY_SAYFA | gunluk | 16 | 40 | 0,065 | 0,100 | -0,036 | 0,0108 |
| SISME | gunluk | 16 | 40 | 2,949 | 1,764 | 1,184 | 0,0431 |
| BOY_MUTLAK | haftalik | 20 | 36 | 10,284 | 7,786 | 2,498 | 0,3973 |
| BOY_OZ | haftalik | 18 | 36 | 1,137 | 1,207 | -0,070 | 0,6398 |
| SON_BOY_OZ | haftalik | 18 | 36 | 1,038 | 1,064 | -0,025 | 0,9634 |
| BOY_BANT | haftalik | 20 | 36 | 0,205 | 0,195 | 0,010 | 0,1795 |
| BOY_SAYFA | haftalik | 20 | 36 | 0,073 | 0,105 | -0,032 | 0,0025 |
| SISME | haftalik | 20 | 36 | 2,384 | 1,633 | 0,751 | 0,0445 |
| BOY_MUTLAK | birlikte | 36 | 76 | 5,311 | 4,524 | 0,787 | 0,2049 |
| BOY_OZ | birlikte | 34 | 76 | 1,004 | 1,075 | -0,071 | 0,2252 |
| SON_BOY_OZ | birlikte | 34 | 76 | 0,917 | 1,051 | -0,134 | 0,0847 |
| BOY_BANT | birlikte | 36 | 76 | 0,201 | 0,196 | 0,006 | 0,4834 |
| BOY_SAYFA | birlikte | 36 | 76 | 0,065 | 0,104 | -0,038 | 0,0001 |
| SISME | birlikte | 36 | 76 | 2,660 | 1,706 | 0,955 | 0,0046 |

- Boş ölçü sayısı (128'de): {"BOY_MUTLAK": 0, "BOY_OZ": 2, "SON_BOY_OZ": 2, "BOY_BANT": 0, "BOY_SAYFA": 0, "SISME": 0}

### Cemal'in not yazdığı on bölge (MUM_IZI13_SONRASI fiziksel sayfa 4, 5, 7-14; getiri bu tabloda yok)

| fiziksel sayfa | sınıf | sembol | zaman | bölge | BOY_MUTLAK % | BOY_OZ | SON_BOY_OZ | BOY_BANT | BOY_SAYFA | SISME |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | EVET | TRMET | haftalik | 2016-01-11 .. 2016-04-29 | 10,00 | - | - | 0,14 | 0,042 | 5,88 |
| 5 | EVET | SLDB | haftalik | 2019-07-08 .. 2019-10-25 | 18,52 | 1,11 | 1,04 | 0,20 | 0,039 | 4,95 |
| 7 | EVET | TOON | haftalik | 2020-08-31 .. 2021-02-12 | 20,20 | 1,09 | 0,86 | 0,19 | 0,020 | 7,13 |
| 8 | EVET | SIG | gunluk | 2017-12-04 .. 2017-12-27 | 3,47 | 1,08 | 1,21 | 0,06 | 0,038 | 4,82 |
| 9 | EVET | SANM | gunluk | 2017-12-07 .. 2018-01-04 | 1,68 | 0,77 | 0,63 | 0,11 | 0,043 | 3,21 |
| 10 | EVET | NCMI | gunluk | 2018-03-28 .. 2018-04-19 | 3,01 | 0,87 | 0,71 | 0,15 | 0,041 | 4,78 |
| 11 | EVET | ALNY | gunluk | 2018-04-24 .. 2018-05-18 | 3,28 | 0,87 | 0,82 | 0,29 | 0,031 | 5,23 |
| 12 | EVET | EBAY | gunluk | 2019-12-03 .. 2019-12-26 | 1,12 | 0,76 | 0,71 | 0,27 | 0,051 | 3,74 |
| 13 | KISMEN | EFOR | haftalik | 2008-02-04 .. 2008-05-23 | 11,12 | 1,22 | 0,87 | 0,17 | 0,071 | 2,91 |
| 14 | KISMEN | IESC | haftalik | 2008-01-28 .. 2008-06-06 | 12,40 | 1,12 | 1,08 | 0,20 | 0,072 | 3,42 |

## A2 grupları: getirisiz sayım (yarıların n'i; n = ölçülen, n_es = eşi olan)

| grup | ölçü | zaman | n bölge | medyan | KÜÇÜK n / n_es | BÜYÜK n / n_es |
|---|---|---|---|---|---|---|
| EVET | BOY_OZ | gunluk | 16 | 0,839 | 8 / 4 | 8 / 8 |
| EVET | BOY_OZ | haftalik | 20 | 1,137 | 9 / 8 | 9 / 9 |
| EVET | BOY_MUTLAK | gunluk | 16 | 3,377 | 8 / 6 | 8 / 6 |
| EVET | BOY_MUTLAK | haftalik | 20 | 10,284 | 10 / 8 | 10 / 10 |
| EVET | SON_BOY_OZ | gunluk | 16 | 0,815 | 8 / 5 | 8 / 7 |
| EVET | SON_BOY_OZ | haftalik | 20 | 1,038 | 9 / 8 | 9 / 9 |
| EVET | BOY_BANT | gunluk | 16 | 0,198 | 8 / 6 | 8 / 6 |
| EVET | BOY_BANT | haftalik | 20 | 0,205 | 10 / 8 | 10 / 10 |
| EVET | BOY_SAYFA | gunluk | 16 | 0,065 | 8 / 7 | 8 / 5 |
| EVET | BOY_SAYFA | haftalik | 20 | 0,073 | 10 / 9 | 10 / 9 |
| EVET+KISMEN | BOY_OZ | gunluk | 26 | 0,871 | 13 / 9 | 13 / 12 |
| EVET+KISMEN | BOY_OZ | haftalik | 26 | 1,137 | 12 / 11 | 12 / 12 |
| EVET+KISMEN | BOY_MUTLAK | gunluk | 26 | 2,907 | 13 / 11 | 13 / 10 |
| EVET+KISMEN | BOY_MUTLAK | haftalik | 26 | 10,842 | 13 / 11 | 13 / 13 |
| EVET+KISMEN | SON_BOY_OZ | gunluk | 26 | 0,815 | 13 / 10 | 13 / 11 |
| EVET+KISMEN | SON_BOY_OZ | haftalik | 26 | 1,038 | 12 / 11 | 12 / 12 |
| EVET+KISMEN | BOY_BANT | gunluk | 26 | 0,198 | 13 / 11 | 13 / 10 |
| EVET+KISMEN | BOY_BANT | haftalik | 26 | 0,201 | 13 / 11 | 13 / 13 |
| EVET+KISMEN | BOY_SAYFA | gunluk | 26 | 0,064 | 13 / 12 | 13 / 9 |
| EVET+KISMEN | BOY_SAYFA | haftalik | 26 | 0,066 | 13 / 12 | 13 / 12 |
| HEPSI | BOY_OZ | gunluk | 66 | 0,983 | 33 / 28 | 33 / 31 |
| HEPSI | BOY_OZ | haftalik | 62 | 1,137 | 30 / 28 | 30 / 29 |
| HEPSI | BOY_MUTLAK | gunluk | 66 | 2,707 | 33 / 32 | 33 / 27 |
| HEPSI | BOY_MUTLAK | haftalik | 62 | 8,717 | 31 / 29 | 31 / 29 |
| HEPSI | SON_BOY_OZ | gunluk | 66 | 0,990 | 33 / 29 | 33 / 30 |
| HEPSI | SON_BOY_OZ | haftalik | 62 | 1,039 | 30 / 29 | 30 / 28 |
| HEPSI | BOY_BANT | gunluk | 66 | 0,196 | 33 / 31 | 33 / 28 |
| HEPSI | BOY_BANT | haftalik | 62 | 0,198 | 31 / 29 | 31 / 29 |
| HEPSI | BOY_SAYFA | gunluk | 66 | 0,075 | 33 / 31 | 33 / 28 |
| HEPSI | BOY_SAYFA | haftalik | 62 | 0,089 | 31 / 30 | 31 / 28 |

## Okuma kuralı (aynen)

- 'YÖN CEMAL'İN DEDİĞİ GİBİ' <=> ANA ÖLÇÜDE (BOY_OZ) EVET bölgelerinde KÜÇÜK yarının eşli fark ortalaması > BÜYÜK yarının, günlükte VE haftalıkta; biri hesaplanamazsa 'OKUNAMADI'; öteki ölçüler bilgi (çoklu karşılaştırma)
- Etiket her durumda: BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK. Grup / eşik / ana ölçü sonuca göre değişmez; değişirse SAPMA.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşli fark mum_izi13_olay.csv'den aynen (aynı giriş günü aynı kova CETVEL2 konum eşi); yeni eş yok; sınır: eşler bölgenin kendi koşusuyla eşlenmedi |
| K2 | geleceğe bakma | EVET | ölçüler bolge_son barında kesilmiş diziden (k16_olcu_bir / k16_sayfa_ylim; assert + sentetik test: sonraki barlar değişince ölçü aynı); 120 bar öncesi penceresi bölgeyi içermez; A1 / grup sayımı getirisiz sütunlarla (usecols); SINIR: ölçüt Cemal sonrasını gördükten sonra söylendi -> GERİYE DÖNÜK |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0); haftalık tamamlanmış ISO haftaları (MH); r = (H - L) / C sonlu barlar |
| K4 | tekilleştirme | EVET | 128 tekil bölge (csv; (set, sayfa) ve (zaman, sembol, bolge_son) tekilliği denetlenir) |
| K5 | giriş fiyatı | EVET | giriş = bölgeden sonraki ilk geçerli barın açılışı (MUM_IZI11 tanımı, csv aynen); bu iş giriş hesaplamaz |
| K6 | veri birimi | EVET | ölçüler birimsiz oran ((H - L) / C, bant ve sayfa oranları); bölünme düzeltmeli MI fiyatları; getiriler csv aynen |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı); sonuç bilgi, kasa açılmaz |
| K8 | örneklem ve dönem | EVET | bütün yarılar n < 30: etiket 'BİLGİ; ÖRNEKLEM YETERSİZ; GERİYE DÖNÜK'; tek dönem (<= 2022); aile içi BH bilgi; karar yok |
| K9 | ön kayıt | EVET | bu ön kayıt (KOD16 / EK16 / olay13 / pdf / anahtar sha + A1 olgu tabloları + grup sayıları) sonrası okunmadan ÖNCE commit; k16_kapi sha + commit + temiz ağaç denetler |
| K10 | ayrıştırma | EVET | notlu on sayfa pdf başlığından ayrıştırılır ve csv ile birebir eşlenir (DUR); bölge başı veriden yeniden hesaplanıp csv ile denetlenir; set3 'k' anahtardan sayfa + sembol + tarih denetimiyle |
| K11 | yeniden üretim | EVET | rapor öncesi >= 2 hücre olay csv'sinden bağımsız pandas koduyla yeniden üretilir; BOY_MUTLAK / BOY_OZ iki bölgede düz döngüyle yeniden hesaplanır |
| K12 | ifade | EVET | 'iz / tuttu / anlamlı' sözü yok; sayı ile yorum ayrı; okuma kuralı yalnız yön |
| K13 | süreç | EVET | çakışma kapısı korunur; çalışan komutlar değişmez (test); yasak defter dosyalarına ve MUM_IZI_HAKEM.py'ye dokunulmaz; yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez |

## SAPMA

(ön kayıt anında yok)
