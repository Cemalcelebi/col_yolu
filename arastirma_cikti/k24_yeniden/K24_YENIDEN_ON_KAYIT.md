# K24 İKİ EVRE ÇÖL — YENİDEN ÖLÇÜM ÖN KAYDI (K24_YENIDEN v1.0 (2026-11-14))

Yazım: 2026-11-14T13:37:08Z. Bu dosya ölçümden ÖNCE yazıldı. Bu modülde hiçbir getiri / eşli fark / olasılık HESAPLANMADI; yalnız sinyal tarandı ve sayıldı. Ön kayıt + modül commit + push edilir, SONRA `python K24_YENIDEN.py kos`.

Cemal (14 Kas 2026): "temel çöl yapısının tespit başarısını ölç"; "her aşamada aynı ölçüm kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz".

## 1. Sinyal tanımı (DEĞİŞMEZ; FON_IZI.fi_k24_tara içe alınır, kopyalanmaz)

t günü SMA20 üstündeki kapanış serisi tam 5'e ulaşır (2. evre dizilme teyidi); serinin öncesindeki 10 barın >= %80'i SMA20 altında kapanmış (1. evre); serideki 5 mumun en fazla 2'sinin dibi SMA20'yi deler; BB genişliği (4σ / SMA20) son 15 barın en yükseğinin <= %70'i (sıkışma); son 15 barın dibi önceki 120 bar tepesinin <= -%30 altında (düşüş sonrası); aynı hissede 60 barda tek. (FON_IZI 'K24 iki evre kuralı' açıklaması, Ç96; eşikler MANAS'ın iki bölgesinden, 25 Eki.)

```json
{"bbw_oran": 0.7, "bbw_pencere": 15, "delen_en_cok": 2, "dusus": -0.3, "once": 10, "once_alt": 0.8, "seri": 5, "tekrar": 60}
```

## 2. Mühür satırları

### ORTAK CETVEL (aynen; OC.oc_kapi_satirlari())

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

### Bu aşama

KY_ESIK_SHA: `4e0dd0ab87aeb24291cd25b3b1b0d5e42bad3a38bcffc13d0e09e677f7042a06`
FI_K24_SHA: `673497e82815147daf97f594380349e93b011d08cf0d987a30795de4d11bfc20`
FI_K24_KOD_SHA: `d6cf765ab3fdbf30da4f8f45851f5142dec9194e88a384b021f528e47b954df5`
KY_KOD_SHA: `4e8737d0c928d01d2ac24ce27ef4fb9e4204166628982821bc4326bf18fb0484`
OLAY_SHA: `7c1bcc51079ff0cb60f2d7f3c39efff321422d6c89208cb40f9584ff729c110d`
TERCIL: `23.000000` `35.000000`

- FI_K24_SHA = sha256(FI_K24 kanonik JSON); FI_K24_KOD_SHA = sha256(inspect.getsource(fi_k24_tara) + getsource(_fi_k23_yon) + FI_K23); KY_KOD_SHA = sha256(K24_YENIDEN.py bayt); OLAY_SHA = sha256(pazar, sembol, sinyal tarihi sıralı csv). kos bunların hepsini yeniden hesaplar; biri farklıysa DURUR.

## 3. Sapmalar (sonuç görülmeden)

- SAPMA-1 (geleceğe bakma): fi_k24_tara 'n < 200 -> boş' şartı serinin toplam uzunluğuna bakar; yalnız t gününde hissenin kendi takviminde >= 200 barı (t dahil) olan sinyaller alınır. Böylece tespit, seri t'de kesildiğinde yapılan tespitle birebir aynıdır.
- SAPMA-2 (veri): tarama OC temiz verisinde (OC K3: H>L, V>0, fiyat > 0 olmayan bar atılır); FON_IZI K24 eskiden ham fi_k1_veri'de tarardı. FI_K24 parametreleri ve fi_k24_tara kodu DEĞİŞMEZ.

Ham (temizlenmemiş V_*.pkl, k34 yok) / temiz (OC) sinyal sayısı (SAPMA-2 etkisi; getiri yok):

| Pazar | ham V_*.pkl | OC temiz (ABD: + k34) |
|---|---|---|
| ABD | 6380 | 10791 |
| AVR | 1646 | 1624 |
| BIST | 2942 | 2800 |

## 4. Ölçüm ve karar (ORTAK CETVEL; kendi ölçü / eşik yok)

- Olay = (sembol, sinyal günü t, pazar) -> `OC.oc_olc(olaylar, V)`; rapor `OC.oc_rapor`. Pazarlar ABD (+k34), AVR, BIST; dönemler 2016-22 keşif, 2023, 2024-26/08 (OC dönemi GİRİŞ gününe göre atar).
- Karar: OC_ESIK 'etiket' (oc_etiket); tek hipotez (bir sinyal) -> çoklu karşılaştırma düzeltmesi yok; alt küme tabloları BİLGİ (karar dışı, iddia üretmez).
- Eski sonuçlarla kıyas (bilgi; yeniden ölçülmez, IZ_KARNE kayıtlarından okunur):

  - Ç96: K24 ilk ölçüm (eski tek cetvel: 60 gün önce +%15 oranı, kural / eşli kat): "ABD 2023 0,92, ABD 2024-26 0,97" (IZ_KARNE metninde: EVET)
  - Ç113: FI_OLCUT eşli fark ABD 2023 / 2024-26, AVR 2023 / 2024-26, BIST 2023 / 2024-26: "çöl K24 +%3,1 (aralık artı) / -%0,5, +%0,4 / +%0,5" (IZ_KARNE metninde: EVET)
  - Ç118: ABD çöl sinyali sayısı ve eşli fark: "6.912 çöl sinyali" (IZ_KARNE metninde: EVET)
  - Ç122: ham fark (eşit ağırlıklı piyasaya göre) ABD 2016-22 / 2023 / 2024-26: "çöl K24 -%0,8 / +%5,1 / +%1,0" (IZ_KARNE metninde: EVET)

## 5. Ek bilgi tabloları (karar dışı; her alt küme OC.oc_olc ile, cetvel içi)

- 1. evre süresi L1: 1. evre süresi L1 = serinin ilk barı a = t-4'ten geriye, SMA20 üstünde >= 3 ardışık kapanışlık son dizinin bittiği bar j'den a-1'e kadar bar sayısı (a-1-j); böyle dizi yoksa SMA20'nin ilk geçerli barından (19) a-1'e kadar. (fi_k24_tara'nın kendi 'seri' sayacı: c > SMA20 ardışık kapanış sayısı; yalnız t ve öncesi.)
- Tercil: kesikler L1'in ABD 2016-22 (keşif) sinyallerindeki 1/3 ve 2/3 yüzdeliği (np.quantile, linear); ön kayıtta sayı olarak yazılır, bütün pazar / dönemlere aynı kesik uygulanır: kısa <= q1 < orta <= q2 < uzun. Kesikler (ABD 2016-22 sinyallerinden): q1 = 23.00 bar, q2 = 35.00 bar.
- Derinlik: fi_k24_tara 'dusus' (son 15 barın dibi / önceki 120 bar tepesi - 1); kova (alt, üst]: alt < dusus <= üst; kovalar -%30..-%50, -%50..-%70, <-%70.

## 6. OLAY SAYIMI (getiri hesaplanmadan; sinyal günü t'ye göre dönem; OC giriş gününe göre atar, sınırda birkaç olay kayabilir)

| Pazar | 2016-22 | 2023 | 2024-26 | dışı | toplam |
|---|---|---|---|---|---|
| ABD | 4699 | 1507 | 4585 | 0 | 10791 |
| AVR | 1102 | 128 | 382 | 12 | 1624 |
| BIST | 1372 | 472 | 956 | 0 | 2800 |

Tarama sayımı:

| Pazar | hisse | kural (tüm) | SAPMA-1 düşen | sinyal | okunamayan hisse |
|---|---|---|---|---|---|
| ABD | 2876 | 11947 | 1156 | 10791 | 0 |
| AVR | 580 | 1684 | 60 | 1624 | 0 |
| BIST | 581 | 3014 | 214 | 2800 | 0 |

L1 tercil sayımı:

| Pazar | Dönem | kısa | orta | uzun |
|---|---|---|---|---|
| ABD | 2016-22 | 1605 | 1593 | 1501 |
| ABD | 2023 | 515 | 427 | 565 |
| ABD | 2024-26 | 1983 | 1164 | 1438 |
| AVR | 2016-22 | 303 | 430 | 369 |
| AVR | 2023 | 47 | 33 | 48 |
| AVR | 2024-26 | 127 | 121 | 134 |
| BIST | 2016-22 | 526 | 429 | 417 |
| BIST | 2023 | 176 | 111 | 185 |
| BIST | 2024-26 | 384 | 318 | 254 |

Derinlik kova sayımı:

| Pazar | Dönem | -%30..-%50 | -%50..-%70 | <-%70 |
|---|---|---|---|---|
| ABD | 2016-22 | 2792 | 1361 | 546 |
| ABD | 2023 | 795 | 444 | 268 |
| ABD | 2024-26 | 2376 | 1359 | 850 |
| AVR | 2016-22 | 872 | 201 | 29 |
| AVR | 2023 | 109 | 18 | 1 |
| AVR | 2024-26 | 345 | 33 | 4 |
| BIST | 2016-22 | 1053 | 292 | 27 |
| BIST | 2023 | 276 | 189 | 7 |
| BIST | 2024-26 | 788 | 148 | 20 |

Beklenen güç (OC güç tablosu, δ +%5; sinyal sayısıyla; OC süzgeçleri n'i düşürür, gerçek güç raporda):

| Pazar | Dönem | sinyal n | güç % |
|---|---|---|---|
| ABD | 2023 | 1507 | 65 |
| ABD | 2024-26 | 4585 | 60 |
| AVR | 2023 | 128 | 29 |
| AVR | 2024-26 | 382 | 52 |

Ç175 tahmini ABD ~6.900 sinyal (eski Ç118: 6.912). Bu taramada ABD 2023 + 2024-26 (sinyal günü) = 6092; ABD tüm dönem 10791 (k34 nakdi biten 1.472 hisse eklendi; 2016-22 dahil).

Veri notları:

- ABD: k34_yahoo eklendi: 1472 hisse (evrene ilk_giris gününden itibaren; bugün işlem görenler, batan YOK); evren dışı (fon / ETF) çıkarılan: 7 ['BTCW', 'DBA', 'DBB', 'DBO', 'UNG', 'UNL', 'UUP']; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- AVR: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- BIST: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = OC (aynı giriş günü, aynı pazar, aynı 60 gün momentum beşliği x 20 gün likidite üçlüsü; plasebo 200 portföy). Mekanik üstünlük: K24 sinyali 'SMA20 üstünde 5 kapanış' ister (kısa vadeli yükseliş) ve '-%30 düşüş' ister; eşler 60 gün momentumla eşlenir, 5 gün getirisiyle eşlenmez -> kısa vadeli dönüş / devam etkisi sinyale karışabilir (raporda sınır) |
| K2 | geleceğe bakma | EVET | fi_k24_tara yalnız geriye bakan pencereler (SMA20, std20, 120 bar tepe, 10 bar 1. evre); 'n < 200' toplam uzunluk şartı SAPMA-1 ile t'ye kadar 200 bara indirildi; test_k24_yeniden 'gelecek' + kos'ta gerçek veride 60 sinyal/pazar kesme denetimi; tercil kesikleri yalnız ABD 2016-22 (keşif) sinyallerinden, ön kayıtta sabit |
| K3 | geçerli bar | EVET | tarama OC temiz verisinde (OC oc_veri_hazirla: H>L, V>0, fiyat>0 olmayan bar atılır; SAPMA-2); OC sinyal barı geçersizse olay düşer |
| K4 | tekilleştirme | EVET | fi_k24_tara 'tekrar' 60 bar (kural günleri arası) + OC 60 birleşik takvim günü tekilleştirme; n bağımsız olay; hücrede medyan |
| K5 | giriş fiyatı | EVET | giriş = OC: t'den sonraki ilk geçerli bar açılışı (sinyal t kapanışında oluşur) |
| K6 | veri birimi | EVET | tek kip: V_*.pkl düzeltilmiş fiyat; OC bölünme şüphesi geçmiş penceresi; AVR likidite EUR (OC); getiri oranı birimden bağımsız |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler + ABD k34 nakdi biten (yine bugün işlem gören); batanlar YOK -> getiriler yukarı, -%50 olasılığı aşağı yanlı; raporda yazılır |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; OC iki yarı aynı yön şartı; İZ DEĞİL yalnız güç yeterliyken (n >= 1.000 ya da güç %80); tek hipotez -> BH gerekmez; alt kümeler bilgi |
| K9 | ön kayıt | EVET | KY_ESIK sha + FI_K24 sha + fi_k24_tara kaynak sha + K24_YENIDEN.py sha + OC üç satırı + olay sha ön kayıtta; ön kayıt ve modül commit + push SONRA kos; kos git kapısı + sha eşitliği; eşik yok, sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber / KAP ayrıştırma yok; yalnız OHLCV; ham veriden 3 olay elle doğrulanır (denetim, raporda) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/k24_yeniden/k24_olay.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir; 3 olay ham veriden elle |
| K12 | ifade | EVET | etiketler yalnız OC kuralıyla; fiyat değişimi (komisyon yok) yazılır; alt küme tabloları 'bilgi', iddia değil |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_ky; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## Test

`python test_k24_yeniden.py` (sentetik: sinyal tespiti FON_IZI ile birebir; geleceğe bakma: seri t'de kesilince aynı tespit; SAPMA-1; L1 elle; kova; cetvel çağrısı; kapı; çakışma kapısı; e-posta / anahtar yok).
