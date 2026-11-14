# ORTAK CETVEL — ÖN KAYIT (ORTAK_CETVEL v1.0 (2026-11-14))

Yazım: 2026-11-14 13:25:10 UTC. Bu dosya ölçümden ÖNCE yazıldı; hiçbir sinyal bu cetvelle henüz ölçülmedi (yalnız sentetik test + güç simülasyonu).

**Bu cetvel dört aşamada değiştirilmez; değişirse yeni cetvel sürümü ve bütün aşamalar yeniden koşulur.**

Dört aşama (Cemal, 14 Kas 2026): (1) K24 iki evre çöl; (2) D9 uzun çöl + rüzgâr; (3) düzgün dip vs çöl ayrımı; (4) INTEM ileri test. Her aşama `import ORTAK_CETVEL as OC` ile bu modülü içe alır, kendi ön kaydına aşağıdaki üç satırı AYNEN koyar ve koşmadan önce `OC.oc_kapi(<aşama ön kaydı>)` çağırır; sha'lardan biri tutmazsa ya da ön kayıt git'e işlenmemişse koşu durur.

## Mühür satırları (aşama ön kayıtlarına aynen kopyalanır)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

- CETVEL_SHA = sha256(OC_ESIK kanonik JSON, sort_keys); CETVEL_KOD_SHA = sha256(ORTAK_CETVEL.py bayt); GUC_SHA = sha256(guc_tablosu.json).

## Güç özeti (gerçek ABD 2023-26 eş farkı dağılımı; beş şartlı hücre kuralı)

| n | δ %0 | δ %2 | δ %5 | δ %10 |
|---|---|---|---|---|
| 30 | %0,5 | %2,5 | %10,5 | %37,5 |
| 100 | %2,5 | %10,0 | %29,0 | %91,0 |
| 300 | %0,5 | %11,0 | %51,5 | %96,5 |
| 1000 | %1,5 | %19,0 | %65,0 | %98,5 |
| 3000 | %0,0 | %24,5 | %60,0 | %97,0 |

K58 tutarlılık: dört şartlı güç δ +%2, n <= 300 en yüksek %11,0 (K58 <= %11) -> TUTARLI. Ayrıntı GUC_TABLOSU.md.

## OC_ESIK (tam metin; mühürlü)

```json
{
 "bilgi_pazar": [
  "BIST"
 ],
 "bolunme": {
  "aktif": true,
  "esik": 0.25,
  "gecmis_pencere": [
   -61,
   -1
  ],
  "geri_gun": 10,
  "geri_pay": 0.5,
  "ileri": "UYGULANMAZ: ileri ölçü penceresinde şüphe dışlama sonuca göre seçimdir (gerçek ±%33-50 / 2 kat günleri siler; ABD 2023-25 havuzunda 250 gün penceresinin %5'i, k34'te %9'u); veri fi_k1_veri düzeltilmiş, FON_IZI r60'ı da dışlamaz",
  "oran_tol": 0.04,
  "oranlar": [
   1.5,
   2,
   3,
   4,
   5,
   6,
   8,
   10,
   15,
   20,
   25,
   30,
   40,
   50,
   100
  ],
  "tanim": "SIKISMA_YENIDEN ANA kuralı (sy_bolunme_supheli ile aynı): |günlük basit getiri| > %25, 10 gün sonra sıçramanın en az yarısı duruyor, önceki 10 gün düz VE |ln getiri| bir bölünme oranının ln'ine ±0,04 yakın (en küçük oran 1,5 olduğu için iş tanımındaki '|ln| > ln 1,25' ile aynı günleri seçer). Geçmiş penceresinde [d-61, d-1] şüpheli günü olan hisse o gün havuzdan (olay + eş) çıkar (momentum / likidite bozulmasın). İleri pencerede dışlama YOK (bkz. 'ileri')."
 },
 "donem": [
  [
   "2016-22",
   "2016-01-01",
   "2022-12-31"
  ],
  [
   "2023",
   "2023-01-01",
   "2023-12-31"
  ],
  [
   "2024-26",
   "2024-01-01",
   "2026-08-31"
  ]
 ],
 "donem_tarih": "giriş günü",
 "esli": {
  "havuz": "gecmis",
  "likit": 20,
  "likit_kova": 3,
  "min_es": 3,
  "min_havuz": 30,
  "mom": 60,
  "mom_kova": 5,
  "tanim": "FON_IZI FI_OLCUT ile aynı: giriş günü d; momentum = C(d-1)/C(d-61)-1 (kapanış en çok 5 gün ileri taşınır); likidite = önceki 20 gün medyan C*V; o gün havuzdaki hisseler arasında sıra (rank first) -> 5 momentum x 3 likidite kovası (qcut); eş = aynı gün, aynı kova, olay hissesi hariç, o ölçüde ölçülebilir hisseler; en az 3 eş. HAVUZ 'gecmis': kovalar yalnız d günü bilinenlerle (geçerli bar, momentum, likidite, alt %20 dışı, geçmiş bölünme dışı) kurulur; FON_IZI'de havuz ileri r60'ı olan hisselerle kurulur (ileri bilgi). Gelecek tam olduğunda ikisi birebir aynıdır (test)."
 },
 "etiket": {
  "genel": "İZ = dört karar hücresi TUTAR (BIST 2023 + 2024-26 da TUTAR ise 'İZ + BIST'); EMARE = en az bir karar hücresi TUTAR ama dördü değil (tek pazar / tek dönem; AVR'de veri yoksa ve ABD iki dönem TUTAR -> 'EMARE (ABD-ADAY; AVR verisi yok)'); İZ DEĞİL = hiçbir karar hücresi TUTMAZ ve verisi olan bütün karar hücreleri TUTMADI (güç yeterli); ÖLÇÜLEMEDİ = öteki durumlar (TUTAR yok ama en az bir karar hücresi güçsüz). Keşif 2016-22 ve BIST bilgi.",
  "guc_bak": "güç tablosunda hücre n'inden küçük ya da eşit en büyük n satırı (muhafazakâr); n < 30 -> güç 0",
  "guc_delta_ref": 0.05,
  "guc_esik": 0.8,
  "hucre": "n < 30 ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, δ=+%5) >= %80) -> TUTMADI; değilse ÖLÇÜLEMEDİ",
  "n_yeter": 1000,
  "olasilik": "hücre: n_250 < 30 ÖLÇÜLEMEDİ; +%100 eş katının alt ucu > 1 VE -%50 eş katının üst ucu < 1 -> SEÇİCİ; ikisinin de alt ucu > 1 -> PİYANGO; aksi YOK. Genel: dört karar hücresi aynı (SEÇİCİ ya da PİYANGO) ise o; herhangi bir karar hücresi ÖLÇÜLEMEDİ ise ÖLÇÜLEMEDİ; aksi YOK."
 },
 "gecerli_bar": "O, H, L, C > 0 ve sonlu, H > L, V > 0 (değilse bar veriden atılır: bayat fiyat sinyal / ölçü üretmez)",
 "guc": {
  "bas": "2023-01-01",
  "delta": [
   0.0,
   0.02,
   0.05,
   0.1
  ],
  "k58_kontrol": {
   "delta": 0.02,
   "k58_ust": 0.11,
   "n_max": 300,
   "pay": 0.05,
   "tanim": "dört şartlı güç (δ +%2, n <= 300) K58'in bulduğu en yüksek değeri (%11) + 5 puan aşmamalı"
  },
  "kaynak": "ABD (V_ABD + k34), giriş 2023-01-01 .. 2026-06-30, havuzda olan, r60'ı ölçülebilir ve en az 3 eşi olan rastgele hisse-gün (yerine koymadan); olayın r60'ına δ eklenir, eşler dokunulmaz (K58 k58_delta_ekle ile aynı); güç = hücrenin TUTTUĞU tekrar payı",
  "n": [
   30,
   100,
   300,
   1000,
   3000
  ],
  "sentetik_ay": 42,
  "sentetik_es": 20,
  "sigma_varsayim": 0.25,
  "son": "2026-06-30",
  "tekrar": 200,
  "tohum": 1477
 },
 "hucre_karar": {
  "n_esik": 30,
  "port_yuzde": 0.9,
  "sira_esik": 0.5,
  "tanim": "TUTAR = (1) n >= 30; (2) ortalama eşli fark > 0 VE ay kümeli %95 alt uç > 0; (3) ortalama hücre içi sıra > 0,50; (4) slot portföyü > 200 plasebo portföyün %90 yüzdeliği; (5) İKİ ALT DÖNEM AYNI YÖN: hücre olayları giriş sırasıyla iki yarıya (ilk floor(n/2) / kalan) bölünür, iki yarının ortalama eşli farkı da > 0. (1)-(4) FON_IZI FI_OLCUT dört şartıdır."
 },
 "karar_donem": [
  "2023",
  "2024-26"
 ],
 "karar_pazar": [
  "ABD",
  "AVR"
 ],
 "kesif_donem": "2016-22",
 "kriz": "2026-08-31",
 "likidite": {
  "alt_kesik": 0.2,
  "gun": 20,
  "kesit": "giriş günü, geçerli barı ve sonlu likiditesi olan pazar hisseleri; alt %20 havuzdan ve olaydan çıkar",
  "min_gun": 10,
  "olcu": "C*V (AVR: *Kur, EUR); giriş gününden ÖNCEKİ 20 birleşik takvim gününün medyanı (shift 1)"
 },
 "olay": {
  "girdi": "DataFrame[sembol, tarih (sinyal günü t; yalnız t'ye kadar bilgi), pazar]",
  "giris": "t'den sonraki ilk GEÇERLİ bar (hissenin kendi takvimi) AÇILIŞI; t ile giriş arası en çok 10 birleşik takvim işlem günü",
  "giris_azami_bosluk": 10,
  "sinyal_bar": "t hissenin ham verisinde bir bar ise geçerli olmalı (H>L, V>0); t bar değilse (hafta sonu haber) serbest",
  "tekil": "aynı hissede, geçmiş bilgili süzgeçlerden (geçerli bar, havuz üyeliği) SONRA, giriş günü sırasıyla ilk olay tutulur; sonraki olay birleşik takvimde >= 60 işlem günü sonra olmalı; ölçüm düşmeleri (kriz kesiği, ileri bölünme) tekilleştirmeyi etkilemez",
  "tekil_gun": 60
 },
 "olcu": {
  "bilgi_ufuk": 20,
  "bootstrap": 2000,
  "cikis": "giriş + 59 birleşik takvim günü kapanışı (yoksa en çok 5 gün önceki son kapanış; FON_IZI ile aynı)",
  "dokunma_asagi": -0.5,
  "dokunma_tanim": "giriş günü dahil ufuk kadar birleşik takvim gününde geçerli barların High / Low'u giriş açılışına göre; aynı gün iki eşik = aşağı önce sayılır; ufuk kriz kesiğini ya da hissenin son barını (5 gün pay) aşarsa ölçülmez",
  "dokunma_ufuk": 250,
  "dokunma_yukari": 1.0,
  "guven": [
   0.025,
   0.975
  ],
  "kat": "KAT = Σ olay göstergesi / Σ olayın eş oranı (eş: aynı gün aynı hücre); TABAN KAT = Σ olay / Σ aynı gün bütün havuz oranı (olay hissesi hariç); %95 aralık ay kümeli bootstrap (2000, tohum 27)",
  "kume": "giriş ayı",
  "once_asagi": -0.1,
  "once_ufuk": 60,
  "once_yukari": 0.2,
  "port_n": 200,
  "port_yuzde": 0.9,
  "slot": 10,
  "slot_takvim_carpan": 1.45,
  "tohum": 27,
  "ufuk": 60
 },
 "pazar": [
  "ABD",
  "AVR",
  "BIST"
 ],
 "surum": "1.0",
 "veri": {
  "abd_ek": "k34_yahoo (nakdi biten, bugün işlem gören 2.246 şirket; V_ABD'de olmayanlar eklenir, evrene k34_evren ilk_giris gününden itibaren girer; 'batanlar dahil' SAYILMAZ)",
  "abd_ek_aktif": true,
  "evren_disi": "ABD: evren_disi_ABD.csv (varsa) + K55_EVREN_DISI.csv 'fon_evren_disi' satırları (ETF / fon) çıkar",
  "min_bar": 80,
  "tiingo": false
 }
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı momentum beşliği x likidite üçlüsü (FI_OLCUT; test_ortak_cetvel FON_IZI ile birebir), aynı giriş (açılış) / çıkış (60. gün) geometrisi; plasebo 200 portföy aynı gün aynı hücreden rastgele hisse; güç simülasyonu rastgele hisse-gün (δ=0 yanlış pozitif payı tabloda). Mekanik üstünlük: sinyal tanımı her aşamanın ön kaydında ayrıca yazılır |
| K2 | geleceğe bakma | EVET | havuz 'gecmis': kovalar yalnız d günü bilinenle (FON_IZI'deki ileri r60 şartı kaldırıldı); momentum d-1'e, likidite d-1'e kadar; test 'geleceğe bakma': seri d'de kesilince hücre etiketleri aynı (fi kipinde aynı DEĞİL, test gösterir); sınır: bölünme şüphesi tespiti 10 gün sonrasını kullanır (veri temizliği, raporda) |
| K3 | geçerli bar | EVET | oc_veri_hazirla: H>L, V>0, O/H/L/C>0 olmayan bar atılır; sinyal günü barı geçersizse olay düşer (sayımda); dokunma ölçüleri yalnız geçerli bar |
| K4 | tekilleştirme | EVET | oc_olay_hazirla: aynı hissede 60 birleşik takvim işlem gününde tek olay (geçmiş bilgili süzgeçlerden sonra); n = bağımsız olay; hücre tablosunda ortalama yanında medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (hissenin kendi takvimi; en çok 10 gün boşluk); test 'giriş ertesi açılış' |
| K6 | veri birimi | EVET | tek kip: fi_k1_veri düzeltilmiş fiyat (V_*.pkl); getiri oranı birimden bağımsız; AVR likidite *Kur (EUR); bölünme şüphesi (SIKISMA_YENIDEN ANA) geçmiş pencerede [d-61, d-1] dışarıda (sayımda ayrı); ileri pencerede dışlama yok (sonuca göre seçim olurdu; şüphelilerin %70'i 1,5 kat oranlı gerçek günlük hareket); 100x pens / sterlin sıçraması oran listesinde (100) |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*) + ABD k34 nakdi biten (yine bugün işlem gören; batanlar YOK, Tiingo YOK); raporda 'hayatta kalma yanlılığı: getiriler yukarı, -%50 olasılığı aşağı yanlı' notu her oc_rapor'da basılır |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki alt dönem (hücre yarıları) aynı yön şartı; İZ DEĞİL yalnız güç yeterliyken (n >= 1.000 ya da güç %80, guc_tablosu.json); çoklu karşılaştırma: aşama ön kaydında yazılır |
| K9 | ön kayıt | EVET | OC_ESIK sha256 + kod sha256 + güç tablosu sha256 CETVEL_ON_KAYIT.md'de; oc_kapi üçünü + git işlenmiş/değişmemiş + IZ_KARNE.ik_kontrol_kapisi denetler, tutmazsa durur (test 'kapı'); eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV; aşama modülü olay kaynağını kendi ön kaydında denetler |
| K11 | yeniden üretim | EVET | oc_olc olay satırlarını (_esler hariç) döndürür; aşama raporu >= 2 hücreyi satır dosyasından bağımsız yeniden üretir; bu işte güç tablosunun 2 satırı ham csv'den yeniden üretildi (GUC_TABLOSU.md) |
| K12 | ifade | EVET | etiketler (İZ / İZ DEĞİL / ÖLÇÜLEMEDİ / EMARE / SEÇİCİ / PİYANGO) yalnız oc_etiket kuralıyla; fiyat değişimi ile işlem kârı ayrı (komisyon yok yazılır); sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_oc; yasak dosyalara dokunulmaz (git diff); e-posta / anahtar taraması testte; ücretli veri / Tiingo yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm cetveli |

## Test

`python test_ortak_cetvel.py` (sentetik; tekilleştirme, ertesi açılış, FON_IZI ile hücre etiketleri birebir, bootstrap determinizmi, plasebo, olasılık tablosu, etiket kuralları, kapı, geleceğe bakma kesme testi, e-posta / anahtar taraması).
