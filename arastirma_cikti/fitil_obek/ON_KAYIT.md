# FITIL_OBEK — ÖN KAYIT

FITIL_OBEK v1.0 (2026-11-16): fitil öbeği (S+ alt fitilsiz / S- üst fitilsiz), ORTAK CETVEL v1.0 ile

- FO_ESIK_SHA: `1ca5faf0ea7d59a7dcbd34fec464dad28e095f9ca0874ce75954b7268bcbebd5`
- FO_KOD_SHA: `dc9646f5418e531ae10e7dcec78a7d756b6cf2d1fca89808daf81262899616bd`
- IS_TANIMI_SHA: `0e2d5d95f7a3a36bbed49e5d38001425f2bb288dc2c3a0d8236fffac58c3f760` (git 99bdc76cc2, 2026-11-16T19:47:17+00:00)
- ZAMAN (UTC): `2026-11-16 20:06:22 UTC`

Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı, getirisiz). `kos` kontrol listesi, cetvel üç sha'sı, FO_ESIK / kod sha'sı ve iş tanımının git kaydı tutmazsa durur. Eşikler sonuç görülünce değişmez.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Tanım (iş tanımı §2; sabit)

- Bar: geçerli bar (OC.oc_veri temiz: H > L, V > 0, fiyat > 0); R = H - L; alt = (min(O,C) - L) / R; üst = (H - max(O,C)) / R; gövde = |C - O| / R. Fitil yok eşiği 0.1.
- Pencere: son k geçerli bar (t dahil, rolling; yalnız t'ye kadar bilgi). A = ortalama alt, U = ortalama üst, ASIM = U - A; ALTYOK = alt < 0,10 bar payı; USTYOK = üst < 0,10 bar payı.
- S+ (YUKARI öbek) k=10: ASIM >= 0.2 VE ALTYOK >= 0.5.
- S- (AŞAĞI öbek) k=10: ASIM <= -0.2 VE USTYOK >= 0.5.
- KUCUK: KUCUK = pencere medyanı (R / C) <= 0,75 x ATR%250; ATR%250 = t'de biten 250 geçerli barın (en az 120) ortalama TR / C; TR = max(H, önceki geçerli kapanış) - min(L, önceki geçerli kapanış).
- Onda birlik: aynı gün (t), aynı pazarda k=10 ASIM'i tanımlı hisseler arasında yüzdelik sıra (rank pct, ortalama bağ); > 0,90 -> S+ onda; <= 0,10 -> S- onda (50 hissede 5 / 5); o gün en az 30 hisse (yalnız t günü bilinen).
- Olay: DURUM GÜNLERİ: şartın t (pencerenin son günü) kapanışında doğru olduğu her geçerli bar OC.oc_olc'a verilir; giriş t'den sonraki ilk geçerli açılış, tekilleştirme 60 gün (cetvel: ilk durum günü tutulur).

Satırlar:

- SP_k10: S+ (YUKARI öbek) k=10: ASIM >= 0,20 VE ALTYOK >= 0,50 [ANA]
- SM_k10: S- (AŞAĞI öbek) k=10: ASIM <= -0,20 VE USTYOK >= 0,50 [ANA]
- SP_k5: S+ k=5 [bilgi]
- SM_k5: S- k=5 [bilgi]
- SP_k15: S+ k=15 [bilgi]
- SM_k15: S- k=15 [bilgi]
- SP_kucuk: S+ k=10 VE KUCUK [bilgi]
- SM_kucuk: S- k=10 VE KUCUK [bilgi]
- SP_onda: S+ yalnız ASIM üst %10 (k=10, günlük kesit) [bilgi]
- SM_onda: S- yalnız ASIM alt %10 (k=10, günlük kesit) [bilgi]

## Karar kuralı (önceden yazılı)

- S+: S+ beklenen yön yukarı: hücre durumu ORTAK_CETVEL oc_hucre 'tutar' (dört şart + iki yarı > 0) ve oc_hucre_durum.
- S-: S- beklenen yön aşağı (kaçınma, AYNA; fark = eşli - olay): n >= 30; ortalama eşli fark < 0 VE ay kümeli %95 ÜST uç < 0; ortalama hücre içi sıra < 0,50; slot portföyü < 200 plasebo portföyün %10 yüzdeliği (p10); iki yarının ortalama eşli farkı da < 0. Durum: n < 30 ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 ya da güç(n, δ 5) >= %80) -> TUTMADI; aksi ÖLÇÜLEMEDİ (OC.oc_hucre_durum, tutar yerine ayna şart).
- Etiket: S+ ve S- AYRI: OC.oc_etiket (karar hücreleri ABD 2023 / 2024-26, AVR 2023 / 2024-26; BIST bilgi) ile; cetvelin 'İZ DEĞİL' etiketi bu işte 'DESTEKLENMEDİ' olarak yazılır (güç yeterli, tutmadı). EMARE = en az bir karar hücresi TUTAR ama dördü değil.
- Ters yön: bilgi: her ana satır için TERS yön de aynı kuralla yazılır (S+ için ayna, S- için cetvel); karar değildir.
- Olasılık: bilgi: S- için -%50 eş katının alt ucu > 1 VE +%100 eş katının üst ucu < 1 -> 'AŞAĞI SEÇİCİ' (karar dışı); cetvelin olasılık etiketi (SEÇİCİ / PİYANGO / YOK) iki satırda da aynen yazılır.
- Çoklu karşılaştırma: ana karar yalnız SP_k10 ve SM_k10 (çoklu düzeltme yok; iki ayrı ön kayıtlı soru); 8 bilgi satırı x 4 karar hücresi = 32 test; p = beklenen yönde ay kümeli bootstrap (2000, tohum 27, oc_hucre ile aynı örnekleme): S+ için (1 + #ortalama <= 0) / 2001, S- için (1 + #ortalama >= 0) / 2001; Benjamini-Hochberg q 0,10; n < 30 hücre teste girmez.

## Örnek doğrulama (tanım değiştirilmez; tutmazsa hangi şart olduğu raporda)

- PAPIL: BIST 2025-11-13 .. 2025-12-09, beklenen SP_k10
- DGXX: ABD 2026-10-27 .. 2026-11-13, beklenen SM_k10 (V_ABD 2026-10-22'de bitiyor ve oc_veri 31.08.2026'da keser: yalnız örnek için yfinance (auto_adjust=False, 2026-06-01 .. 2026-11-13; 16 Kas yarım bar alınmaz); ölçüme girmez)
- FENER: BIST 2025-10-14 .. 2025-11-07, beklenen bilgi
- DESA: BIST 2021-10-27 .. 2021-12-23, beklenen bilgi
- YKSLN: BIST 2026-03-19 .. 2026-05-15, beklenen bilgi

## Veri

- V_ABD.pkl sha256: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl sha256: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- ABD oc_veri notu: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- AVR oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- BIST oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı

## OLAY SAYIMI (getirisiz; durum günü sinyal tarihine, olay giriş tarihine göre dönem)

| Satır | Pazar | durum günü 2016-22 / 2023 / 2024-26 | OLAY (cetvel sonrası, giriş dönemi) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |
|---|---|---|---|---|---|
| SP_k10 | ABD | 30004 / 6243 / 14768 | 4367 / 889 / 2557 | 20447 | 24339 |
| SP_k10 | AVR | 34299 / 6727 / 18565 | 3485 / 649 / 1880 | 26955 | 30780 |
| SP_k10 | BIST | 35461 / 5851 / 32285 | 3728 / 719 / 2888 | 59275 | 9622 |
| SM_k10 | ABD | 39409 / 5199 / 12343 | 5975 / 928 / 2465 | 27445 | 22863 |
| SM_k10 | AVR | 47905 / 4923 / 13506 | 4583 / 592 / 1749 | 34489 | 31830 |
| SM_k10 | BIST | 35269 / 3131 / 6572 | 2070 / 292 / 570 | 21231 | 26518 |
| SP_k5 | ABD | 66177 / 13235 / 32877 | 11638 / 2260 / 6037 | 53999 | 41751 |
| SP_k5 | AVR | 57690 / 10170 / 28319 | 7062 / 1171 / 3279 | 51089 | 40343 |
| SP_k5 | BIST | 48508 / 8212 / 39008 | 5581 / 1034 / 3740 | 71348 | 17877 |
| SM_k5 | ABD | 81829 / 12119 / 29987 | 13459 / 2178 / 6016 | 66943 | 40415 |
| SM_k5 | AVR | 73627 / 8279 / 23334 | 7924 / 1116 / 3153 | 60660 | 42303 |
| SM_k5 | BIST | 48622 / 5164 / 12287 | 4000 / 654 / 1593 | 30649 | 35531 |
| SP_k15 | ABD | 10331 / 2194 / 4160 | 991 / 221 / 628 | 4529 | 10873 |
| SP_k15 | AVR | 17067 / 3299 / 9093 | 1249 / 283 / 854 | 10300 | 19129 |
| SP_k15 | BIST | 17254 / 2653 / 17585 | 1908 / 368 / 1774 | 30500 | 4222 |
| SM_k15 | ABD | 13378 / 1416 / 3493 | 1570 / 188 / 617 | 6510 | 10346 |
| SM_k15 | AVR | 26512 / 2204 / 5903 | 1936 / 242 / 708 | 14770 | 20994 |
| SM_k15 | BIST | 24328 / 1723 / 3310 | 1108 / 119 / 240 | 13169 | 19050 |
| SP_kucuk | ABD | 11058 / 3211 / 4255 | 1942 / 576 / 858 | 6492 | 8770 |
| SP_kucuk | AVR | 11110 / 2766 / 5114 | 1657 / 422 / 823 | 8048 | 8541 |
| SP_kucuk | BIST | 16360 / 1912 / 13387 | 2192 / 390 / 1755 | 23341 | 4032 |
| SM_kucuk | ABD | 16852 / 2567 / 3945 | 3074 / 591 / 970 | 9898 | 8899 |
| SM_kucuk | AVR | 18350 / 2415 / 3925 | 2317 / 401 / 754 | 11638 | 10459 |
| SM_kucuk | BIST | 17092 / 623 / 2820 | 1057 / 59 / 246 | 6922 | 12505 |
| SP_onda | ABD | 194086 / 34202 / 94076 | 14922 / 2647 / 7556 | 198363 | 110708 |
| SP_onda | AVR | 95900 / 14618 / 39095 | 7181 / 1059 / 2911 | 88428 | 61391 |
| SP_onda | BIST | 66535 / 12141 / 37630 | 5029 / 967 / 2959 | 96290 | 15359 |
| SM_onda | ABD | 192516 / 33977 / 93477 | 15388 / 2781 / 7817 | 216128 | 89551 |
| SM_onda | AVR | 94313 / 14365 / 38524 | 7224 / 1117 / 3126 | 95284 | 51615 |
| SM_onda | BIST | 64950 / 11922 / 36988 | 3549 / 724 / 2097 | 58488 | 53281 |

Kural: hücre n < 30 ise ÖLÇÜLEMEDİ; güç yetersizse DESTEKLENMEDİ denmez.

## SAPMA / sınır (sonuç görülmeden yazıldı)

- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD'dir (oc_veri notunda); güç tablosu ABD + k34 ile üretilmişti (cetvel), aynen kullanılır.
- ON_KAYIT.md'yi alt ajan git'e işleyemez (commit yasak): iş tanımı koşudan önce işlendi (yukarıdaki commit); bu dosyanın sha'sı ve yazım zamanı sonuc.json'a yazılır, kos zamanı ondan sonradır. oc_kapi git=False ile, ORTAK_CETVEL.py / güç tablosu / iş tanımı git kaydı ayrıca denetlenir. Ana model ON_KAYIT.md'yi işlerken sha'yı karşılaştırır.
- Kısa vadeli dönüş / oynaklık eşlenmez (cetvel yalnız 60 gün momentum x likidite eşler): S+ (kapanış dipte) / S- (kapanış tepede) ile son günlerin getirisi ilişkili olabilir; yorumda sınır.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, aynı giriş (ertesi açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy aynı gün aynı hücreden. Mekanik üstünlük: sinyal yalnız t'ye kadar mum şekli; giriş t+1 açılışı olduğu için t kapanış konumu getiriyi mekanik üretmez; kısa vadeli dönüş (üst fitilli = kapanış dipte) eşlenmez, raporda sınır olarak yazılır |
| K2 | geleceğe bakma | EVET | pencere ölçüleri rolling (geriye), ATR%250 t'de biter, onda sırası yalnız t günü; kos fo_gelecek_denetimi her pazarda 40 (+4 onda) rastgele olayda seriyi t'de kesip sinyali yeniden hesaplar, tutmazsa DURUR; test 'geleceğe bakma' |
| K3 | geçerli bar | EVET | sinyal OC.oc_veri temiz barlarıyla (H>L, V>0, fiyat > 0; geçersiz bar veriden atılır, pencereye girmez); DGXX örneğinde 16 Kas (seans içi yarım bar) alınmaz |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücrede medyan da yazılır |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); sinyal t kapanışında biter |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); fitil payları oran, birimden bağımsız; bölünme şüphesi cetvelde (geçmiş pencere); DGXX örneği ham (auto_adjust=False) ama yalnız fitil payı, birim etkisiz |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD 1.411 hisse); batanlar yok; raporda 'getiriler yukarı, -%50 olasılığı aşağı yanlı' notu |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı; DESTEKLENMEDİ yalnız güç yeterliyken; bilgi satırları BH q 0,10; olay sayımı bu ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | FO_ESIK sha + FITIL_OBEK.py sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce git'e işlendi (99bdc76); kos ik_kontrol_kapisi + OC.oc_kapi + fo_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; örnek bölgelerde fitil payları ham bardan elle yeniden hesaplanır (rapor) |
| K11 | yeniden üretim | EVET | ana olay satırları arastirma_cikti/fitil_obek/olay_ana.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | etiketler yalnız oc_etiket / ayna kuralı; 'iz / emare' sözü yalnız kural geçerse; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fo; defter dosyaları ve mevcut .py modülleri yalnız okunur (git status); e-posta / anahtar taraması testte ve raporda; ücretli veri yok; commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yön ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## Test

`python test_fitil_obek.py` (sentetik: fitil payları elle, pencere / kural, onda kesiti, geleceğe bakma kesme testi, ayna kuralı, BH, cetvel çağrısı, kapı, e-posta / anahtar taraması).
