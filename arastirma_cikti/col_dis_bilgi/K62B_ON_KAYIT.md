# K62-B — BİLANÇO SÜRPRİZİ ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU: ÖN KAYIT (ölçümden ÖNCE)

K62-B v1.0 (2026-11-12): bilanço sürprizi (K62 SUETF / EAR, çöl günü bilinen son açıklama) çöl sinyaline ek bilgi; K64 tasarımı aynen, BIST + ABD
Yazım zamanı: 2026-11-12 04:42:12 UTC (2026-11-12 07:42 TR)
ESIK_SHA256: 2686fef68b917d6c85ac4529678d421b967c27a42768eabe5ce1c5b6e4d62541

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark / CAR hesaplanmadan yazıldı (yalnız `kapsam` sayımı koşuldu: §12). `python -I K62B.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez. Tasarım K64_K65_ON_KAYIT.md ile aynıdır
(K64.py fonksiyonları içe alınır, kopyalanmaz; K64.py değişmez); değişken tanımları K62'den (K62_ON_KAYIT.md; K62.py fonksiyonları içe alınır, K62.py değişmez).
K64 SONUÇ dosyaları (K64_K65_RAPOR.md, k64_s1*.csv, k64_karar.csv) bu iş tasarlanırken OKUNMADI.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- k62_veri: sha256 d35b377408b45ccdf7a55229e44f6b411d34143d1dc67a19e5ae848ca1e3220c (2138 dosya)
- K60_ON_KAYIT.md: sha256 eba12e1d060217f2c1fd4ffe5715382d29d343cd29004af5c69617b10b2218c0 (1 dosya)
- K64_K65_ON_KAYIT.md: sha256 0d2e34ab9f6d825636425c1a9897eab6b8fe4e0f18defd49a393f6fd3cd3a73e (1 dosya)
- K62_ON_KAYIT.md: sha256 084a91bd5d9dca5fa9f0cdf18cf6bf7e02e2d71643d7b92f1ecac36a73b4f680 (1 dosya)
- FON_IZI.py: sha256 ea0cc19f9b6514c50340df0e331c8d1a5e7961083918eefec45de6d7eb10ac7b (1 dosya)
- K60.py: sha256 d819f93082188688f5a3ed2a5d1bdb39735169125f292c62103b3e842ebd8e66 (1 dosya)
- K59.py: sha256 a302656f957d9b99149873ebc0880798d694d03341da1559af79d460b491c655 (1 dosya)
- COL_v1.py: sha256 13597d4209698a7edbeb4fb947c383ffa1c3c2d9eb715e33c5ef6902ce8987b8 (1 dosya)
- K64.py: sha256 0255e8b2902228e20665a439e8df529cf4521bbee4ed24d248c1977e08577653 (1 dosya)
- K62.py: sha256 e6d0573134f59018390e58d83a8ac1a71a83570913dabbdef4ae171f2e4e1063 (1 dosya)
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...; ABD temel tablosu, pay, bölünme) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True).
K64, K62 ve K60 mühürleri bu işin mührüne girer.

## 0. Soru (Cemal'in ana sorusu)
Bilanço sürprizi ÇÖL sinyaline ek bilgi taşıyor mu? Çöl tanımı ve cetvel DEĞİŞMEZ. Değişkenler K62'nin (Ahlatcıoğlu & Okay 2021 birebir tekrarı) iki sürpriz ölçüsüdür,
çöl sinyal günü t'de BİLİNEN son açıklamaya göre. Her değişken İKİ YÖNDE sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.

## 1. Olay (K64_K65_ON_KAYIT.md §1 AYNEN; K64.k64_olay_k24 / k64_olay_d13 çağrılır)
- ANA: K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, FI_K24 = {"seri": 5, "once": 10, "once_alt": 0.8, "delen_en_cok": 2, "bbw_oran": 0.7, "bbw_pencere": 15, "dusus": -0.3, "tekrar": 60}. Sinyal günü t; giriş = hissenin t'den sonraki ilk işlem
  günü açılışı. TEKİLLEŞTİRME: son TUTULAN sinyalden en az 60 işlem günü sonra gelen ilk sinyal (FI_K24 'tekrar' = 60 ile birebir).
- İKİNCİL (sağlamlık; BH ailesine ve karara GİRMEZ): üretim D13 + AL kırılımı (K64 §1 (ii) aynen; gerçek veride K64'ün ara önbelleği).
- Evren: V_BIST.pkl (581) ve V_ABD.pkl (1.411) (islenmis-veri dalı; K24 cetvelinin evrenleri). Fon krizi: 2026-08-31 sonrası barlar atılır; penceresi aşan olay ölçülmez.

## 2. Açıklama, değer ve BİLGİ TARİHİ
- BIST açıklamaları: K62 verisi (KAP 'Finansal Rapor' bildirim sınıfı FR, 2009-06 -> 2026-08; her hisse-mali yıl-çeyreğin İLK yayını; İş Yatırım fiyat / piyasa
  değeri / mali tablo, kotasyondan çıkanlar dahil). SUETF ve EAR K62.k62_olay_tablosu ile BİREBİR aynı formülle (testte denetlenir). TMS 29 KİRLİ çeyrekler
  (2022Ç4, 2023Ç4, 2024Ç1, 2024Ç2, 2024Ç3, 2024Ç4, 2025Ç4; K62 SAPMA 9 / B3): o açıklamanın SUETF'i YOK (EAR'ı var).
- ABD açıklamaları: K60 demeti (SEC XBRL frames + EDGAR başvuru dizini), V_ABD sembolleri. Açıklama günü = K60 BİLGİ TARİHİ: çeyrek sonundan en az 15 gün sonraki
  ilk 10-Q / 10-K başvurusunun günü; yalnız GERÇEK başvuru günü olan çeyrekler (bilgi_kaynak [1]); yedek kural günü (çeyrek sonu + 90 / 120)
  açıklama günü değildir, o çeyrek açıklama sayılmaz. **SAPMA**: şirketlerin çoğu bilançoyu basın bülteniyle (8-K) 10-Q / 10-K'dan GÜNLER önce açıklar; burada
  açıklama günü başvuru günüdür (EAR penceresi asıl tepkiyi kaçırabilir; SUETF'in bilinme günü tutucudur).
- ta = açıklama gününe eşit ya da sonraki ilk işlem günü (açıklama saati kullanılmaz); KARAR GÜNÜ = ta + 1 işlem günü (EAR o günün kapanışında bilinir).
- **KURAL**: t günü bir hissenin değeri, karar günü < t olan EN SON açıklamanın değeridir; ancak o açıklamanın günü t'den en çok 90 takvim günü önceyse.
  Değilse (ya da hiç açıklama yoksa) değer YOK ve olay 'son 90 günde açıklama yok' sınıfındadır (bilgi). Son açıklamanın değeri yoksa (veri eksik / TMS 29 kirli)
  daha eskiye GİDİLMEZ: değer YOK. Aynı karar gününde birden çok açıklama varsa dönemi en geç olan.

## 3. Değişkenler
| kod | tanım | kaynak |
|---|---|---|
| SUETF_C | t'de bilinen son açıklamanın SUETF'i = (E_q - E_{q-4}) / MV_q (K62 tanımı). E = çeyreklik net kâr (BIST: İş Yatırım ana ortaklık payı, birikimli farkı; ABD: SEC NetIncomeLoss çeyreklik), MV_q = çeyrek sonu piyasa değeri. BIST'te TMS 29 kirli çeyreğin (K62 B3) değeri YOK | Ahlatcıoğlu & Okay 2021; K62 (BIST PEAD) |
| EAR_C | t'de bilinen son açıklamanın EAR'ı = prod[ta-1, ta+1](1 + R_i) - prod(1 + R_p); p = 2x3 büyüklük-DD/PD portföyü (Haziran sonu; K62 kuralı); ta = açıklama gününe eşit ya da sonraki ilk işlem günü | Ahlatcıoğlu & Okay 2021; K62 (BIST PEAD) |

- SUETF ayrıntısı: BIST E = İş Yatırım net dönem kârı ana ortaklık payı (birikimli farkı), MV_q = çeyrek son işlem günü PD (İş Yatırım); ABD E = SEC NetIncomeLoss
  çeyreklik (K60 temel tablosu; türetilmiş 4. çeyrek dahil), E_(q-4) aynı tablonun dört çeyrek önceki değeri, MV_q = çeyrek sonuna eşit ya da önceki son işlem günü
  (en çok 10 gün geride) bölünme düzeltmeli kapanış (5 güne kadar ileri taşıma) x o gün bilinen pay (K60.k60_pay; bugünkü birim).
- EAR ayrıntısı: BIST K62 aynen (2x3 portföy: Haziran sonu PD 2 kova x önceki yıl sonu özkaynak / Aralık PD 3 kova; günlük eşit ağırlık; portföyde günlük getirisi
  olan en az 5 hisse; [ta-1, ta+1] getirilerinin en az 2/3'ü). ABD: aynı K62.k62_portfoy_ata / k62_hazirla kuralı; PD = kapanış x pay (Haziran ve Aralık son işlem
  günü); defter değeri = takvim yılı Y-1'de biten mali yılın SEC özkaynağı, BİLGİ TARİHİ Y Haziran sonundan önce (aksi portföy dışı); evren = V_ABD sembolleri
  (K60 demetindeki fiyatla); günlük getiri = düzeltilmiş kapanış (temettü dahil). Bu yüzden ABD'de 'eşit ağırlıklı evren' yedeğine gerek kalmadı.
- ÇÖL + SÜRPRİZ (bilgi; karara girmez): son açıklamanın SUETF ve EAR sınıfı K62 C kuralıyla (K62.k62_tertil_onsel; önceki çeyreğin karar günü bilinen
  1/3 - 2/3 kesimleri, pazarın bütün açıklamaları; BIST SUETF'te kirli çeyrek havuz olamaz); ikisi de üst üçte bir = CS. Bilgi grupları: CS, CS_DEGIL (ikisi de
  sınıflı ama CS değil), YOK90 (son 90 günde açıklama yok). Her biri FI_OLCUT ölçüleriyle raporlanır.

## 4. S1 — 'ek katkı' (K64 §4 aynen; K64.k64_s1)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen). Değeri olmayan olay ÜST / ALT gruplarına girmez (TEMEL'de kalır).
- EVREN sırası: aynı gün o pazarda işlem gören ve değeri olan hisseler içinde (küçük + 0,5 x eşit) / n (n >= 30); İÇ sırası: [t - 365 gün, t] aralığındaki
  aynı pazar ve tanımın tekil çöl olayları içinde (n >= 30). ÜST >= 2/3, ALT <= 1/3.
- **KARAR SIRASI** (değişken başına; mekanik kural, eşikleri kapsam koşulmadan yazıldı: ANA tanım, iki pazar, iki bağımsız dönem, EVREN sırasıyla ÜST ve ALT pencereli
  olay sayısı; bir hücrede küçük grup < 30 ya da küçük / büyük < 0.5 ise 'toplanma'; herhangi bir hücrede toplanma -> İÇ, yoksa EVREN):
  SUETF_C = **EVREN (aynı gün evren içi sıra)**, EAR_C = **İÇ (çöl içi sıra)**. Öteki sıra 'sağlamlık, karar dışı'.
  **Kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı; §12'deki sayılar).
- Temel model = hücredeki BÜTÜN çöl olayları. ÜST - ALT: ay kümeli bootstrap (2000 çekiliş, tohum 62201; geçerli çekiliş payı < %90 ise aralık yok).
- 'EK KATKI VAR (yön ÜST)' <=> n_ÜST >= 30 ve n_ALT >= 30 VE ÜST ortalama eşli farkı > temel VE (ÜST - ALT) %95 alt sınırı > 0; ALT ayna.

## 5. S2 — 'tek başına' (bilgi; K64 §5 aynen, K64.k64_s2; tohum 62202)

## 6. Cetvel (FON_IZI FI_OLCUT aynen; K64.k64_olc / k64_hucre)
FI_OLCUT = {"ufuk": 60, "mom": 60, "likit": 20, "mom_kova": 5, "likit_kova": 3, "kriz": "2026-08-31", "bootstrap": 2000, "tohum": 27, "slot": 10, "n_esik": 30, "port_n": 200, "port_yuzde": 0.9}.
Eşli fark (60 gün), ay kümeli %95, hücre içi sıra, slot portföyü; HÜCRE TUTAR <=> n >= 30, alt uç > 0, sıra > 0,50, portföy > rastgele %90. Piyasa koşulu katmanı (eşit
ağırlıklı evren endeksi 200 gün ortalamasının üstü / altı; bilgi), 20 günlük ek ufuk (bilgi). MALİYET gidiş-dönüş BIST %0.6, ABD %0.2
(her olaydan düşülür; rastgele eşler maliyetsiz: tutucu).

## 7. Hücreler ve KARAR (K64 §7 aynen; K64.k64_karar)
- Hücre = pazar (BIST, ABD) x dönem (GİRİŞ gününe göre): 2017-2021 (2017-01-01 .. 2021-12-31), 2022-2026 (2022-01-01 .. 2026-12-31), 2023-2026 (2023-01-01 .. 2026-12-31). Bağımsız: 2017-2021, 2022-2026; 2023-2026 tutarlılık (BH ailesine girmez).
- Pazar kararı 'ADAY' <=> iki bağımsız dönemde aynı yönde 'EK KATKI VAR' ve BH'den geçiyor; bir bağımsız dönemde n_ÜST ya da n_ALT < 30 -> 'ÖLÇÜLEMEZ'; aksi 'İZ DEĞİL'.
- İŞARET: ölçülebilen bütün hücrelerde (iki pazar x üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı.
- Genel karar: karar pazarı ABD; ABD 'ADAY' ve işaret tutarlı -> **'ABD-ADAY'** (en fazla; İZ için Avrupa olay verisi yok); yalnız BIST 'ADAY' -> 'BIST-ADAY (bilgi)'.

## 8. Çoklu test
Aile = ANA tanım, değişkenin KARAR sırası, ölçülebilen bütün (değişken x yön x pazar x bağımsız dönem) hipotezleri (en çok 16). p = 1 - Φ(±(ÜST - ALT) / bootstrap sd)
(tek yönlü). Benjamini-Hochberg q = %10 (K60.k60_bh); Bonferroni bilgi.

## 9. GÜÇ BEYANI
K58: FI_OLCUT 60 günde +%2'lik gerçek etkiyi n = 300 olayda %11, +%4'ü %45 olasılıkla yakalar. Üçte bir grupları daha küçüktür ve değişkenin değeri yalnız son 90 günde
açıklaması olan olaylarda vardır (§12). 'Ek katkı yok' = bu veriyle gösterilemedi; 'ÖLÇÜLEMEZ' = n < 30.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI: çöl evrenleri (V_BIST, V_ABD) yalnız bugün işlem görenlerdir. BIST açıklama ve EAR portföyü verisi (K62) kotasyondan çıkanları da içerir; ABD
  EAR portföyü yalnız V_ABD sembolleridir (yaşayanlar).
- YENİDEN SUNUM: İş Yatırım yıllık değerleri sonradan düzeltilmiş (K62 SAPMA 9; kanıtlı); SEC frames değerleri de düzeltilmiş olabilir (tarih doğru, değer değil).
- ABD açıklama günü 10-Q / 10-K başvuru günüdür (basın bülteni değil; §2).
- BIST açıklaması akşam yayımlanır (çoğu 18:00 sonrası); ta = yayın günü (işlem günüyse) olduğundan EAR penceresi ertesi günü kapsar; karar günü ta + 1 kapanışıdır,
  yani bilgi akşam yayınında bile çöl gününden önce piyasada.

## 11. SAPMA / BOŞLUK listesi (en dar yorum)
SAPMA 1. ABD açıklama günü = 10-Q / 10-K başvuru günü (iş tanımındaki gibi; basın bülteni çoğu zaman daha erken).
SAPMA 2. BIST SUETF'te TMS 29 kirli çeyrekler YOK; son açıklama kirliyse değer yok (daha eskiye gidilmez).
SAPMA 3. ABD 2x3 portföy kurulabildi (SEC özkaynağı + K60 pay); eşit ağırlıklı evren yedeği kullanılmadı. Portföy evreni V_ABD (1.411), K62 BIST'te bütün KAP / İş Yatırım evreni.
SAPMA 4. BIST'te çöl fiyatları V_BIST (fi_duzelt; bölünme / bedelsiz düzeltmeli, temettüsüz), açıklama değerleri İş Yatırım (temettü düzeltmeli) fiyatından: iki kaynak.
BOŞLUK 1. '90 takvim günü' açıklama günü (ann) ile t arasındadır; karar günü < t ayrıca şarttır.
BOŞLUK 2. ABD çeyrek etiketi (çeyrek içi tertil grubu) = dönem sonu tarihinin takvim çeyreği; mali çeyrek değil.
BOŞLUK 3. ABD MV_q: çeyrek sonu günü bilinen pay bir önceki başvurunun kapak sayısıdır (K60 kuralı; pay o çeyreğin raporunda değil).
BOŞLUK 4. ABD defter değeri için birden çok mali yıl aynı takvim yılında biterse sonuncusu.
BOŞLUK 5. Bilgi grupları (CS, CS_DEGIL, YOK90) yalnız ANA tanım ve HEPSİ rejiminde; BH ailesine ve karara girmez.
BOŞLUK 6. Bir olayın son açıklaması 90 günden eskiyse ya da değeri yoksa o değişken için grupsuzdur; TEMEL model her zaman bütün çöl olaylarıdır (K64 kuralı).
BOŞLUK 7. ABD açıklama günü fiyat takviminin dışındaysa (ilk günden önce ya da sonraki ilk işlem günü 10 günden uzak) karar günü ve EAR yok (açıklama kullanılmaz).
BOŞLUK 8. ABD açıklama tablosunda 2009-2010 başvuruları da vardır (K60 demeti 2010-01-04'ten); çöl olayları 2015-06'dan başladığı için 90 gün kuralıyla kullanılmazlar.

## 12. Kapsam (yalnız SAYI; mühre girmez)
Kapsam sayımı (2026-11-12 04:41:45 UTC; `python -I K62B.py kapsam`; yalnız SAYI: getiri, eşli fark, CAR, FI_OLCUT paneli hesaplanmadı).

- ABD: 1411 hisse, takvim 2830 gün (2015-06-01 .. 2026-08-31); açıklama tablosu 68323 (2009-03-18 .. 2026-09-14); SUETF'i olan 50907, EAR'ı olan 47243, TMS 29 kirli 0; K60 demetinde 1406; gerçek başvuru günlü çeyrek 68323, yedek kural günlü (açıklama sayılmayan) 297; 2x3 portföylü gün 3813. Evren hisse-günlerinde değişken doluluk: EAR_C %64, SUETF_C %68.
- BIST: 581 hisse, takvim 2863 gün (2015-06-01 .. 2026-08-31); açıklama tablosu 29700 (2009-06-01 .. 2026-08-31); SUETF'i olan 23424, EAR'ı olan 25926, TMS 29 kirli 3918; K62 verisinde de olan hisse 580. Evren hisse-günlerinde değişken doluluk: EAR_C %78, SUETF_C %67.

**K24 olayları** (ham / tekil / pencere = 60 günlük penceresi 31.08.2026'dan önce biten tekil olay; son 90 gün = pencereli olaylardan karar günü t'den önce, açıklaması t'den en çok 90 gün önce olan; hiç = t'den önce hiç açıklaması olmayan)

| pazar | dönem | ham | tekil | pencere | son 90 gün | yok (90 gün) | hiç | TMS 29 kirli | ÇÖL+SÜRPRİZ / sınıflı |
|---|---|---|---|---|---|---|---|---|---|
| BIST | 2017-2021 | 1282 | 1157 | 1157 | 1058 (%91) | 99 | 13 | 0 | 111 / 938 |
| BIST | 2022-2026 | 2147 | 1751 | 1651 | 1408 (%85) | 243 | 15 | 573 | 76 / 668 |
| BIST | 2023-2026 | 1903 | 1538 | 1438 | 1215 (%84) | 223 | 12 | 573 | 57 / 508 |
| ABD | 2017-2021 | 2928 | 2589 | 2589 | 2128 (%82) | 461 | 309 | 0 | 166 / 1492 |
| ABD | 2022-2026 | 4319 | 3721 | 3519 | 2925 (%83) | 594 | 281 | 0 | 215 / 2170 |
| ABD | 2023-2026 | 3091 | 2670 | 2468 | 2117 (%86) | 351 | 183 | 0 | 163 / 1625 |

**K24: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | BIST 2017-2021 | BIST 2022-2026 | BIST 2023-2026 | ABD 2017-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|---|---|---|
| SUETF_C | EVREN | 1006 / 272 / 399 | 808 / 207 / 313 | 625 / 161 / 233 | 1818 / 573 / 834 | 2537 / 858 / 1058 | 1868 / 645 / 789 |
| SUETF_C | İÇ | 1006 / 335 / 319 | 808 / 271 / 272 | 625 / 199 / 208 | 1818 / 601 / 598 | 2537 / 832 / 866 | 1868 / 616 / 630 |
| EAR_C | EVREN | 976 / 270 / 386 | 1247 / 357 / 504 | 1083 / 316 / 429 | 1618 / 471 / 752 | 2343 / 592 / 1218 | 1740 / 421 / 958 |
| EAR_C | İÇ | 976 / 339 / 314 | 1247 / 387 / 455 | 1083 / 345 / 387 | 1618 / 550 / 529 | 2343 / 775 / 803 | 1740 / 571 / 621 |

**D13 olayları** (ham / tekil / pencere = 60 günlük penceresi 31.08.2026'dan önce biten tekil olay; son 90 gün = pencereli olaylardan karar günü t'den önce, açıklaması t'den en çok 90 gün önce olan; hiç = t'den önce hiç açıklaması olmayan; D13'te yalnız GECER)

| pazar | dönem | ham | tekil | pencere | son 90 gün | yok (90 gün) | hiç | TMS 29 kirli | ÇÖL+SÜRPRİZ / sınıflı |
|---|---|---|---|---|---|---|---|---|---|
| BIST | 2017-2021 | 726 | 465 | 465 | 404 (%87) | 61 | 3 | 0 | 38 / 387 |
| BIST | 2022-2026 | 855 | 543 | 538 | 457 (%85) | 81 | 1 | 177 | 26 / 203 |
| BIST | 2023-2026 | 752 | 472 | 467 | 397 (%85) | 70 | 1 | 177 | 15 / 144 |
| ABD | 2017-2021 | 2372 | 1498 | 1498 | 1227 (%82) | 271 | 127 | 0 | 104 / 940 |
| ABD | 2022-2026 | 3278 | 2084 | 1958 | 1647 (%84) | 311 | 115 | 0 | 119 / 1249 |
| ABD | 2023-2026 | 2430 | 1534 | 1408 | 1194 (%85) | 214 | 78 | 0 | 94 / 925 |

**D13: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | BIST 2017-2021 | BIST 2022-2026 | BIST 2023-2026 | ABD 2017-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|---|---|---|
| SUETF_C | EVREN | 395 / 136 / 138 | 277 / 76 / 98 | 218 / 59 / 76 | 1053 / 356 / 404 | 1405 / 452 / 485 | 1031 / 332 / 372 |
| SUETF_C | İÇ | 395 / 127 / 124 | 277 / 86 / 91 | 218 / 64 / 71 | 1053 / 364 / 361 | 1405 / 453 / 490 | 1031 / 349 / 360 |
| EAR_C | EVREN | 393 / 110 / 123 | 447 / 125 / 135 | 388 / 114 / 118 | 1027 / 295 / 404 | 1373 / 350 / 545 | 1003 / 246 / 424 |
| EAR_C | İÇ | 393 / 126 / 130 | 447 / 131 / 163 | 388 / 117 / 140 | 1027 / 348 / 336 | 1373 / 455 / 472 | 1003 / 325 / 351 |

**Karar sırası seçim kuralı uygulaması** (ANA tanım, iki pazar, bağımsız dönemler, EVREN sırası; toplanma = küçük grup < 30 ya da küçük / büyük < 0.5): SUETF_C BIST 2017-2021 ÜST 272 / ALT 399 (oran 0.68); EAR_C BIST 2017-2021 ÜST 270 / ALT 386 (oran 0.70); SUETF_C BIST 2022-2026 ÜST 207 / ALT 313 (oran 0.66); EAR_C BIST 2022-2026 ÜST 357 / ALT 504 (oran 0.71); SUETF_C ABD 2017-2021 ÜST 573 / ALT 834 (oran 0.69); EAR_C ABD 2017-2021 ÜST 471 / ALT 752 (oran 0.63); SUETF_C ABD 2022-2026 ÜST 858 / ALT 1058 (oran 0.81); EAR_C ABD 2022-2026 ÜST 592 / ALT 1218 (oran 0.49, TOPLANMA). Kuralın sonucu: **EAR_C: İÇ**, **SUETF_C: EVREN**.

ANA tanım, KARAR sırası, bağımsız dönemlerde grubu n < 30 olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler (pencereli olay sayısıyla; ölçülebilen olay daha az olabilir): yok.

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k62b_olaylar.csv.gz, k62b_s1.csv, k62b_s1_fark.csv, k62b_s2.csv, k62b_karar.csv, k62b_bilgi.csv, k62b_meta.json, K62B_RAPOR.md.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K62B.py kos`  -> ölçüm + rapor (mühür, veri sha256, git doğrulanır)
3. `python K62B.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K62B_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13, K64 mührü, K62 mührü) değişirse ESIK_SHA256 değişir ve koşu durur. Veri ya da
içe alınan kod / ön kayıt dosyaları değişirse sha256 tutmaz ve koşu durur.
