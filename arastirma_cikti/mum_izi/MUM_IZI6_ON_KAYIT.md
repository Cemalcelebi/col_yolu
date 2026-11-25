# MUM_IZI6 ÖN KAYIT (2026-11-25T14:56:09Z)

Etiket seti 2: yeni ölçü yok; donmuş MUM_IZI_V3 ölçüleri. Bu dosya evren taramasından, seçimden ve PDF'ten ÖNCE commit edilir. Sınamalar (T1-T4) Cemal'in işaret dosyası (cemal_mum_izi6_etiket.json) gelince `python MUM_IZI_ETIKET2.py olc` ile AYNEN koşulur; eşikler sonuca göre değişmez.

## Mühürler

KOD6_SHA: cc8c6c914d7ecaa02682eb9c302e63635e567a1d828f7416a0cbb6bdeb291f1d
ESIK6_SHA: 4f544d473ee64ed522b3583f51ca62fea017a8f87f8ef1b82267edf5b1ea7fb1
V3_KOD_SHA: 70fc2fb979c47b2a2bd5fb260e1fb1891e7b34268f49c4a4276f482b66a4eb69
ESIK5_SHA: 0a46827a22295a4fb60c46233d036619a014bf40ab6899716c98f7ac5d19101c
DAGILIM5_JSON_SHA: 1f9e7a62dc27c4f742a67034f8971dfe12e078fb02e2cb3f86439834401b7dd5
DAGILIM_GUNLUK_PKL_SHA: 43c5c98f71340649ee6d91b4865f849f778dac9de5c60acf588263dfe653249f
DAGILIM_HAFTALIK_PKL_SHA: aacce3c017838cd05170cbf52cf84840828616fb1f53b1ad278dd1384dbea3d1
MI_KOD_SHA: 370d582043567440101ade832d560f4a3eebf7a764eb758f634a8811cfd288b9
MH_KOD_SHA: 8f7440d199dfcf018f838da77da5cf0eabd89062fdc67cf26a0a5678ed4da200
MV_KOD_SHA: 1bb586cb825b8b437b97df4ec193a682bc626ecc796e9130d27e4906b68d81dc

- MUM_IZI_ETIKET2.py commit'i: d4bd96981723fc273d5b8a429f3cdc793463d8b6 2026-11-25T14:56:09+00:00
- Dağılım pkl dosyaları /tmp'de (repoda değil); MUM_IZI_V3.py v3_dagilim ile aynı tohumlarla yeniden üretilir; pkl ile mum_izi5_dagilim.json (n, tau1) uyumu denetlendi.

## Seçim kuralı, tohumlar, sınamalar (E6_ESIK; sha yukarıda)

```
{
 "surum": "E6-1.0",
 "olcu": "donmuş MUM_IZI_V3: F1 / F2 / F3 (v3_ozet + v3_aileler), D3 (v3_D3, mum_izi5_dagilim.json tau), yüzdelik = MV.mv_pct(V3 rastgele pencere dağılımı, aynı zaman dilimi); v1 S = MV.mv_S_bilesen(MUM_IZI tam şablon, kalibre). Yeni ölçü yok",
 "pencere": {
  "birim": "(hisse, pencere sonu, uzunluk m); m = V3 uzunlukları 16 / 18 / 20 / 22 / 24",
  "gunluk": [
   "2016-01-01",
   "2022-12-31"
  ],
  "haftalik": [
   "2001-01-01",
   "2022-12-31"
  ],
  "bas_min": 19,
  "gecerli": "MI.mi_veri geçerli bar; pencere başı >= 19 (bant); haftalıkta pencerenin 2..m. barında boşluk (eksik hafta) yok; üst bant > SMA"
 },
 "evren": {
  "ABD_AVR": "giriş günü TEZGAH2 P2 üyeliği (MH.mh_p2 ile aynı kural, hisse başına vektörlü: sonraki geçerli bar <= 10 gün, P2 ve hücre >= 0, sinyal barı geçersiz değil); günlük -> /tmp/mum_izi/acik, haftalık 2001-15 -> /tmp/mum_izi/haftalik/p1, 2016-22 -> /tmp/mum_izi/acik; vektörlü maske MH.mh_p2 ile her (zaman dilimi, pazar, parça) için 2.000 rastgele (hisse, tarih) çiftinde birebir sınanır (fark -> DUR)",
  "BIST": "pencere sonu barının işlem değeri (Close x Volume) aynı gün (günlük) / aynı ISO haftası (haftalık) BIST kesit medyanının üstünde",
  "haric": "önceki 24 sayfanın (MUM_IZI4_ONAY) hisseleri"
 },
 "katman": {
  "K1": {
   "alt": null,
   "ust": 0.005,
   "n": 16
  },
  "K2": {
   "alt": 0.005,
   "ust": 0.05,
   "n": 12
  },
  "K3": {
   "alt": 0.05,
   "ust": 0.2,
   "n": 6
  },
  "K4": {
   "alt": "rastgele",
   "ust": "rastgele",
   "n": 6
  },
  "kural": "F1 yüzdeliği alt < p <= ust (K1: p <= 0,005); K4 = evren içi bütün pencereler"
 },
 "secim": {
  "yari": "her katmanda n / 2 günlük + n / 2 haftalık",
  "bist_tavan": "katman x zaman dilimi başına en çok floor((n / 2) / 3) BIST (katman başına <= üçte bir)",
  "yontem": "katman içi RASTGELE: her hisse için evren içi katman pencerelerinden biri düzgün rastgele (hisse tohumu = md5(tohum|zaman|pazar|sembol|katman)); sonra hisseler katmandaki pencere sayısıyla orantılı olasılıkla, yerine koymadan, tek tek çekilir (= katman pencereleri arasında düzgün çekim, hisse başına bir); sıra K1, K2, K3, K4; her katmanda önce günlük sonra haftalık; bir hisse sette bir kez (günlük ve haftalık dahil); BIST tavanı dolunca BIST hisseleri o katman x zaman diliminde çekilmez",
  "tekrar": "önceki 24 sayfadan Cemal'in EVET dediklerinden rastgele 4 + HAYIR dediklerinden rastgele 4 (cemal_mum_izi4_onay.json 'isaret'); aynı bölge, aynı çizim",
  "sira": "48 sayfa tohumla karışık; PDF sayfa 1 kapak, bölgeler PDF sayfa 2-49; sayfada yazan numara = PDF sayfa numarası"
 },
 "tohum": {
  "secim": 25112061,
  "tekrar": 25112062,
  "sira": 25112063,
  "boot": 25112064,
  "t4_cv": 25112065,
  "t4_null": 25112066,
  "p2_dogrulama": 25112067
 },
 "sayfa": "MUM_IZI4_ONAY ile birebir: solda 'Senin kalıbın' (şablon + bant), sağda 'Sayfa N: bulunan bölge (günlük / haftalık mum)' (öncesi 15 mum, turuncu kutu, bölge sonunda kesik), Bollinger 20 + SMA20 (kesik), hisse / tarih / sonrası yok, altta ✓ benziyor / ✗ benzemiyor kutuları",
 "kapak": "Kodun üç denemesi de gözünle uyuşmadı. Bu set kodun değil senin gözünün ölçümü: 48 bölge; bir kısmı kalıbına yakın, bir kısmı uzak, bir kısmı rastgele; 8'i daha önce gördüklerin. Her sayfada benziyorsa ✓ kutusuna, benzemiyorsa × kutusuna X koy. İstersen benzeyen sayfada benzeten 2-3 mumu daire içine al.",
 "etiket": {
  "dosya": "cemal_mum_izi6_etiket.json",
  "sema": {
   "sayfalar": {
    "<PDF sayfa no, metin>": {
     "isaret": "EVET | HAYIR | YOK | IKISI | BELIRSIZ",
     "kutu_disi": "metin",
     "guven": "metin"
    }
   }
  },
  "anlam": "EVET = benziyor (1), HAYIR = benzemiyor (0); YOK / IKISI / BELIRSIZ = karar değil (sınamalardan çıkar, sayılır); başka değer -> DUR",
  "numara": "PDF sayfa numarası (2-49); 1 kapak (yok sayılır); 1-49 dışı anahtar -> DUR"
 },
 "T1": {
  "tanim": "8 tekrar sayfasında yeni işaret = önceki işaret (EVET / HAYIR) sayısı; karar olmayan yeni işaret 'aynı değil' sayılır (ayrıca yazılır)",
  "hukum": {
   "tutarli": 7,
   "kismen": 5
  },
  "metin": ">= 7 / 8 tutarlı; 5-6 kısmen; <= 4 tutarsız (tutarsızsa hiçbir formül tutturamaz)"
 },
 "T2": {
  "tanim": "40 yeni sayfada donmuş F1'in AUC'si = P(F1 benziyor < F1 benzemiyor) + 0,5 eşit; bootstrap %95 (grup içi, B 5000); tam permütasyon p (sıra toplamının tam dağılımı, tek yönlü)",
  "en_az": 3,
  "B": 5000,
  "hukum": "en az 3 EVET ve 3 HAYIR yoksa ÖLÇÜLEMEDİ; AUC >= 0,80 VE alt uç >= 0,65 -> UYUMLU; değilse AUC >= 0,65 -> KISMEN; AUC < 0,65 -> UYUMSUZ",
  "esik": {
   "uyumlu": 0.8,
   "alt_uc": 0.65,
   "kismen": 0.65
  },
  "katman": "katman başına EVET payı (karar verilmiş sayfalar içinde); 'sıra tutuyor' = K1 >= K2 >= K3 >= K4 ve K1 > K4; 'tam sıra' = kesin büyük"
 },
 "T3": {
  "tanim": "bilgi: D3, F2, F3, F1 evre parçası, F1 dizi parçası, v1 S (büyük = benzer) için aynı AUC / %95 / p (40 yeni); F1 ve hepsi günlük / haftalık ayrı"
 },
 "T4": {
  "tanim": "bilgi, EZBER RİSKLİ: 64 etiket (önceki 24 sayfa ilk işaretleriyle + 40 yeni); girdi 12 v3 parçası (F1 dizi, F1 evre, F2: 4 fark + işaret uyumu, F3: 4 fark + uzun üst fitil uyumu) + 39 ölçü (MI_OZELLIK 35 + MV EK 4; şablondan mutlak fark) = 51; kat içi standartlaştırma; L2 lojistik (lambda 1, kesişim cezasız, IRLS); tabakalı 5 kat x 50 tekrar çapraz doğrulama, kat dışı tahminlerle AUC; yalnız CV AUC (ortalama ve %2,5-%97,5) + etiket karıştırma tabanı (200 karıştırma x 5 tekrar) raporlanır",
  "lambda": 1.0,
  "kat": 5,
  "tekrar": 50,
  "null": 200,
  "null_tekrar": 5
 },
 "sonrasi": "T2 UYUMLU -> v4 (F1 eşiği + sentetik negatiflerden geçen zorunlu kapılar; yeni ön kayıt), sonra en benzer bölgelerle onay; KISMEN / UYUMSUZ -> karar Cemal'in"
}
```

## Uygulamada verilen kararlar (iş tanımında açık bırakılanlar)

1. Pencere = (hisse, son, m), m = V3 uzunlukları (16 / 18 / 20 / 22 / 24); her pencerenin kendi F1 yüzdeliği (V3 dağılımı uzunlukları birleşik).
2. Katman içi 'rastgele': katmandaki evren içi pencereler arasında düzgün; hisse başına bir (iki aşamalı: hisse ~ pencere sayısı, hisse içinde düzgün).
3. BIST tavanı katman x zaman dilimi başına floor((n / 2) / 3): K1 2 + 2, K2 2 + 2, K3 1 + 1, K4 1 + 1 (katman başına üçte birin altında).
4. Haftalık BIST likiditesi ISO haftası kesit medyanıyla (haftanın son günleri hisseden hisseye değişir).
5. ABD / AVR P2: MH.mh_p2 kuralının vektörlü hali; tarama başında her parça için 2.000 çiftte MH.mh_p2 ile birebir denetlenir (fark -> DUR).
6. T1'de karar olmayan yeni işaret 'aynı değil' sayılır. T2'de en az 3 EVET ve 3 HAYIR yoksa ÖLÇÜLEMEDİ. T2 hükmünde AUC >= 0,80 ama alt uç < 0,65 ise KISMEN.
7. T4'te önceki 24 sayfa İLK işaretleriyle (MUM_IZI4); tekrar sayfalarının yeni işareti yalnız T1'de.
8. Bütün sayfa ölçüleri (F1-F3, D3, parçalar, 39 ölçü, v1 S) PDF adımında anahtara yazılır: Cemal'in işaretinden ÖNCE donar.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban = katman K4 (evrenden düzgün rastgele pencere) ve önceki işaretlerle tekrar (T1); AUC permütasyon / bootstrap; T4 etiket karıştırma tabanı; getiri / eş yok |
| K2 | geleceğe bakma | EVET | F1 her mumun kendi gününe kadarki bantla (V3); seçilen 40 pencerede veri pencere sonunda kesilince F1 aynı (e6_prefix); veri <= 2022-12-31 + KASA kapısı; etiketler set üretiminden SONRA gelir; ön kayıt tarama ve PDF'ten önce commit |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar; haftalıkta eksik haftalı pencere atılır (V3 kuralı); BIST işlem değeri kesit medyanı üstü; ABD / AVR P2 |
| K4 | tekilleştirme | EVET | hisse başına bir sayfa (günlük ve haftalık birlikte); önceki 24 sayfanın hisseleri hariç |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok |
| K6 | veri birimi | EVET | b birimi ölçek bağımsız; BIST işlem değeri aynı para biriminde kesit medyanıyla |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; yalnız görsel etiket (getiri yok) |
| K8 | örneklem ve dönem | EVET | 40 yeni + 8 tekrar; en az 3 EVET / 3 HAYIR yoksa ÖLÇÜLEMEDİ; aralık raporda; T4 EZBER RİSKLİ yalnız bilgi |
| K9 | ön kayıt | EVET | MUM_IZI6_ON_KAYIT.md: KOD6_SHA, ESIK6_SHA, V3 / MI / MH / MV kod sha, ESIK5_SHA, dağılım pkl sha; e6_kapi (kontrol + sha + git) tarama ve olc öncesi; anahtar sha tarama json'unda, olc onu denetler |
| K10 | ayrıştırma | EVET | etiket şeması önceden yazılı (sayfalar -> no -> isaret); bilinmeyen değer / numara DUR; P2 vektörlü maske MH.mh_p2 ile 2.000 çiftte birebir |
| K11 | yeniden üretim | EVET | seçilen sayfaların F1 / F2 / F3'ü V3.v3_duz ile düz döngüde yeniden; tekrar sayfalarında v1 S = MUM_IZI4 anahtarındaki S; AUC iki yoldan |
| K12 | ifade | EVET | hüküm yalnız önceden yazılı eşiklerle; rapor ve commit mesajında sayfa -> katman / etiket eşlemesi yok; 'iz' sözü yok |
| K13 | süreç | EVET | çakışma kapısı; v1 / v2 / v3 / defterler / kural_defteri / UC_IZ2 değişmez; yalnız kendi yolları commit |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## Notlar (ön kayıttan önce yapılanlar)

- Kuru koşu (yalnız kod sınaması): bu ön kayıttan ÖNCE, kapı yamalı bir betikle, pazar başına 70 rastgele hisselik alt evrende tarama -> seçim -> PDF -> rapor -> SAHTE (rastgele) etiketle olc zinciri /tmp altında koşuldu. Amaç komutların uçtan uca çalıştığını görmek; P2 vektörlü maske 6 parçada 2.000'er çiftte MH.mh_p2 ile birebir (fark 0). Kuru koşunun seçimi gerçek seçim değildir (alt evren); sahte etiket sonucu sonuç değildir; hiçbiri kullanılmaz. Cemal'in yeni işareti yok.
- Tekrar sayfası seçimi önceki işaret dosyasını (cemal_mum_izi4_onay.json) okur (iş tanımı izin veriyor); seçim tohumla.

## SAPMA

(ön kayıt anında yok)
