# CETVEL2 — ÖN KAYIT v2.1 (2026-11-21 09:32:56 UTC)

CETVEL2 v2.1 (2026-11-21): R15 konum eşli fark (bütün evren), plasebo kapısı (200 tohum), güç eğrisi; pozitif kontrol v2. Bu dosya pozitif kontrol koşusundan ÖNCE yazıldı ve git'e işlendi; c2_kapi C2_ESIK / kod / girdi sha'larını, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Kova sınırları getirisiz havuz dağılımından, güç eğrisi yalnız FARK yayılımından (ortalama kullanılmaz) hesaplandı; hiçbir hücre FARK'ı / p'si bu dosya yazılırken hesaplanmadı.

ÖNCEKİ SÜRÜM: CETVEL2_ON_KAYIT.md (v2.0, commit 62c16c9) + CETVEL2_POZITIF_KONTROL.md (v2.0 koşusu, commit 0fc7c95) (silinmedi). DÜZELTME: v2.0 KUSUR (iii): 20 tohumlu kapılar kaba (plasebo kapısı <= 1/20 doğru ayarlı hücrede ~%9-15 şansla düşer; tek n hücresinde >= 3/20 32 denemede şansla); sıfır verisiyle 100 tohumlu tanıda cetvel hafif gevşek (%1-7, ort ~%3,5). Plasebo 200 tohum (eşikler aynı), (iii) n >= 100 birleşik. R15 / eş / kova / TUTAR / güç aynı (C2_ESIK['duzeltme_v21'])

- C2_ESIK_SHA: `c44d76dd5da1d42c358f5bc1a9db3a34ee826c2c142d3113239248023637ff03`
- C2_KOD_SHA: `0650879da905b432c7ff3f1cda673eed9d42c3480630ccf2353ebdd178983319`
- PK_KOD_SHA: `896a70ed704442531a0a4d747dff23fe241ac623b4c3a192114395baa5876fd6`
- DS_KOD_SHA: `b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf`
- YH_KOD_SHA: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e`
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
- DS_ESIK_SHA: `052ac9c4439cf5eaa3679c3d2ae9ba6389021321008d474015a2b7e9af208a9d`
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9`
- OC_ESIK_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
- V_ABD_SHA: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR_SHA: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST_SHA: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- DS_OLAY_SHA: `66794c356e733c8dc3e037246f62389d089a0f85febd844754fbb52852c8e98d`
- PK_B_OLAY_SHA: `fe2509100f2ac3fac0ade06a224a4b6f8710c7de4d25da777fdcbc34efd57c30`
- PK_JSON_SHA: `973bc2f3003d150030f21a92423875c73385a99f3abbc00d2fd9a31304e03fd9`
- C2_ESIK_JSON_SHA: `17833e1ceb278b1598923585e9fb1d8b8c42118d538ce36f898463a3c9352dd7`
- C2_GUC_JSON_SHA: `b0a2a2ddae454088b01b92dfd4567e9b28f06a6cd051e2b4cb144e6ce18e2677`
- C2_PREFIX_SHA: `52b46fac898fd5a497ced530d2931848d0479f309948ab03b688bd88d654c1f6`

## 1. CETVEL2 TANIMI (iş tanımı bölüm 2, AYNEN; ana model ön kaydı, commit ca5d2a8)

Girdi: olay listesi (pazar, sembol, sinyal günü t, isteğe bağlı özellik bayrakları). Fiyat: /tmp/veri/V_ABD.pkl, V_AVR.pkl, V_BIST.pkl (ORTAK_CETVEL.oc_veri; aynı geçerli bar ve likidite kuralları).
- Giriş E0 = t'den sonraki ilk geçerli bar AÇILIŞI (K5). Olay t'de bilinir; prefix testi (K2).
- KARAR ÖLÇÜSÜ R15 = 15. geçerli barın kapanışı / E0 − 1 (stop yok). 15 bar yoksa ölçülmez (kriz kesiği 31.08.2026, K8).
- EŞ (konum eşli, bütün evren): aynı giriş günü, aynı pazar, aynı KOVA = ATRP(14) tercili x 20 gün işlem değeri üçlüsü x F15 (120 gün konumu, t dahil) çeyreği; eş kümesinden olay kümesindeki hisseler (aynı deneme) çıkarılır; en az 5 eş yoksa olay 'eşsiz' (ölçülmez; sayısı yazılır). Terciller / üçlüler / çeyrekler EĞİTİM döneminde (2016-22) pazar başına sabitlenir, sayı olarak ön kayıtta.
- FARK = R15(olay) − ortalama R15(eş). SIRA = olayın R15'inin eş dağılımındaki yüzdeliği (0-1). Hücre (pazar x dönem): n, ortalama FARK, medyan FARK, ortalama SIRA, ay kümeli bootstrap %95 (B 2000), ay kümeli işaret permütasyon p (tek yönlü, beklenen yöne göre; iki yönlü işaretli hipotezlerde iki yönlü), L3O (en iyi 3 ay çıkınca ortalama FARK).
- HÜCRE TUTAR: n >= 30 VE güç >= 0,80 (R15 ile güç eğrisi: bölüm 3 A'dan hücre sigma'sı) VE ortalama FARK > 0 VE boot alt ucu > 0 VE ortalama SIRA > 0,50 VE L3O > 0 (beklenen yön − ise işaretler ters).
- PLASEBO KAPISI (hücre başına, ön kayıtta): rastgele etiketli olay kümesi (aynı n, aynı dönem dağılımı, 20 tohum): ortalama FARK mutlak değeri < 0,5 puan VE 'tutar' payı <= %7. Kapıyı geçmeyen hücre KARAR VERMEZ (BİLGİ); nedeni araştırılır ve yazılır (AVR sınama şüpheli: eş sayısı, kova boşluğu, aynı gün az hisse).
- ETİKET (karne v3 mantığı): KATKI+ = ABD ve AVR'de, eğitim ve sınamada dört hücre TUTAR (plasebo kapısını geçen hücrelerle); KATKI− = dört hücrede ters yönde tutar; SORGULA = bazı hücreler tutar; ÖLÇÜLEMEDİ = n / güç yetersiz; ÇELİŞKİLİ = eğitim ile sınama ters işaret (boot aralıkları ayrık). BIST bilgi. Çoklu test: aynı ön kayıttaki hipotez sayısı m ile BH q 0,10 (sınama hücresi p'leri üzerinden; m sabit).
- BİLGİ SÜTUNLARI (karar dışı, eski sonuçlarla kıyas için): h5 / st5 (eski cetvel: stop dip x 0,98), ATR stop kolu (stop = E0 − 2 x ATR14(t); hedef +%5 stop'tan önce, 15 bar), r60 eşli fark (ORTAK_CETVEL tanımı), R15 medyanı.

## 2. UYGULAMA AYRINTILARI (C2_ESIK; sha yukarıda)

- surum: C2.1
- duzeltme_v21: v2.0 pozitif kontrolü (CETVEL2_POZITIF_KONTROL.md) KUSUR verdi: (iii) A RAST delta 0 ABD eğitim n 1000 3 / 20 tohum. Neden (yalnız sıfır verisiyle, 100 tohumlu tanı): cetvel hafif gevşek (sıfırda yakalama %1-7, ort ~%3,5; nominal %2,5) ve 20 tohumlu kapılar kaba: plasebo kapısı (<= %7 = en çok 1 / 20) doğru ayarlı hücrede bile ~%9-15 şansla düşer, (iii) tek (n) hücresinde > %10 (>= 3 / 20) 32 denemede şansla tetiklenir. DÜZELTME: plasebo tohum 20 -> 200 (eşikler AYNI); (iii) n >= 100 tohumları birleşik (80 tohum-hücre) > %10. R15, eş, kova, TUTAR, güç, etiket DEĞİŞMEDİ
- veri: DUSUS_SONRASI.ds_veri (OC.oc_veri, evren dışı listesi, k34 YÜKLENMEZ, açılış H-L kırpması) + OC.oc_panel (kip 'gecmis'): geçerli bar (O/H/L/C > 0, H > L, V > 0), havuz (momentum / likidite bilinir, alt %20 likidite dışı, geçmiş bölünme şüphesi dışı), kriz kesiği 31.08.2026
- giris: OC.oc_olay_hazirla: t'den sonraki ilk geçerli bar AÇILIŞI E0 (t ile giriş arası <= 10 takvim günü; giriş günü havuzda)
- tekil_gun: 15
- tekil: aynı hissede olaylar giriş günü sırasıyla, birleşik takvimde >= 15 işlem günü arayla (OC tekil kuralı, tekil_gun 15 = ufuk; olay kümesi bütün bayraklar için aynı)
- ufuk: 15
- pencere_azami: 30
- r15: R15 = 15. geçerli barın (giriş barı 1.) kapanışı / E0 - 1; giriş satırından itibaren 30 birleşik takvim satırında 15 geçerli bar yoksa NaN (POZITIF_KONTROL.pk_r15 ile aynı; stop YOK)
- donem:
-   egitim: ['2016-01-01', '2022-12-31']
-   sinama: ['2023-01-01', '2026-08-31']
-   tarih: giriş günü; ambargo yok (kova sınırları getirisiz havuz dağılımından)
- kova:
-   atrp_gun: 14
-   atrp_q: [0.3333333333333333, 0.6666666666666666]
-   f15_gun: 120
-   f15_q: [0.25, 0.5, 0.75]
-   tanim: kova = ATRP tercili x 3 + likidite üçlüsü, x 4 + F15 çeyreği (36 kova). ATRP_t = ort TR [t-13, t] / C_t (PK.pk_seri; DS ile aynı), d gününde hissenin d'den önceki son geçerli barı (t) değeri. F15_t = (C_t - min C) / (max C - min C), t dahil son 120 geçerli kapanış (YH.yh_f15_panel; d'den önceki son geçerli bar). Likidite üçlüsü = OC.oc_panel H % 3 (giriş günü havuz kesitinde önceki 20 gün medyan C x V (x Kur) sırası; para birimi enflasyonu yüzünden sabit TL / $ sınırı kullanılmaz: günlük kesit üçlüsü, sınırlar her gün havuzun 1/3 ve 2/3'ü). ATRP tercil ve F15 çeyrek SINIRLARI pazar başına EĞİTİM (giriş 2016-22) havuz hisse-günlerinden (OC ok VE H >= 0 VE ATRP / F15 sonlu; getirisiz) numpy quantile (doğrusal); sayı olarak cetvel2_esik.json ve ön kayıtta; sınama aynı sayılarla. F15 kovası: f <= q1 -> 0, <= q2 -> 1, <= q3 -> 2, değilse 3
- es_min: 5
- es: aynı giriş günü d, aynı pazar, aynı kova; havuzda (OC ok, H >= 0), R15'i ölçülebilir; aynı denemenin (hipotez bayrağı 1 olan) o gün olay olan hisseleri ve olayın kendisi çıkarılır; en az 5 eş (yoksa 'eşsiz', ölçülmez, sayısı yazılır)
- fark: FARK = R15(olay) - ort R15(eş); SIRA = (#eş R15 < olay + 0,5 #eş = olay) / #eş
- boot:
-   B: 2000
-   alt: 0.025
-   ust: 0.975
-   tohum: 2111
-   birim: giriş ayı (YH.yh_d3_boot_l3o; L3O = en olumlu 3 ay çıkınca)
- perm:
-   R: 10000
-   tohum: 2113
-   tanim: DS.ds_perm_p (ay kümeli işaret permütasyonu); yön '+' / '-' tek yönlü, '?' iki yönlü
- guc:
-   delta: 0.02
-   z: 1.959963984540054
-   esik: 0.8
-   n: [30, 100, 300, 1000, 3000]
-   R: 1000
-   tohum: 2112
-   tanim: pazar x dönem hücre sigma eğrisi: DS ANA olaylarının (ds_olay.csv.gz; tek tek eşlenmiş, deneme = olayın kendisi) FARK'ından n olay yerine koymadan R kez (n <= N / 2), sigma(n) = std(ort FARK); ln sigma = a + b ln n en küçük kareler; güç(n) = Phi(delta / sigma(n) - z); delta = +0,02 (R15 +2 puan getiri). Güç < 0,80 hücre ÖLÇÜLEMEDİ. Getiri ortalaması kullanılmaz (yalnız yayılım)
- hucre:
-   n_min: 30
-   sira: 0.5
-   tutar: n >= 30 VE güç >= 0,80 VE ort FARK > 0 VE boot alt > 0 VE ort SIRA > 0,50 VE L3O > 0 (beklenen yön '-' ise: FARK < 0 VE boot üst < 0 VE SIRA < 0,50 VE L3O(-) < 0; '?' iki yönden biri)
- plasebo:
-   tohum_sayi: 200
-   tohum: 2114
-   fark_mutlak: 0.005
-   tutar_pay: 0.07
-   tanim: hücrenin ölçülen her olayı yerine AYNI GİRİŞ GÜNÜ havuzdan rastgele bir hisse (gün içinde yerine koymadan; R15 ölçülebilir, kovası var) -> aynı cetvel (eşler, en az 5, boot, SIRA, L3O, güç) -> 200 tohum (v2.1; v2.0 20). KAPI GEÇER = |200 tohum ortalama FARK| < 0,005 (0,5 puan) VE TUTAR payı (hipotezin yönünde; '?' iki yön) <= %7. Geçmeyen hücre KARAR VERMEZ (BİLGİ); nedeni yazılır
- etiket:
-   tanim: karar hücreleri ABD x {eğitim, sınama}, AVR x {eğitim, sınama}; sıra: (1) ÇELİŞKİLİ = bir karar pazarında eğitim ve sınama boot aralıkları sıfırın zıt taraflarında (ayrık); (2) ÖLÇÜLEMEDİ = bir karar hücresinde n < 30 ya da güç < 0,80; (3) KATKI+ = dört karar hücresi plasebo kapısını geçer VE beklenen yönde TUTAR ('-' yönlü hipotezde 'TUTAR' ters işaretlerle; '?' hipotezde dördü aynı yönde); KATKI− = dört hücre ters yönde TUTAR; (4) SORGULA = öteki durumlar (bazı hücreler tutar ya da plasebo kapısı düşen karar hücresi var ya da hiçbiri tutmadı; sayı yanında yazılır). KATKI± yalnız BH geçerse; geçmezse 'SORGULA (BH)'. BIST BİLGİ
-   bh:
-     q: 0.1
-     p: hipotez p = max(p ABD sınama, p AVR sınama) (önceden yazılı yön; n < 30 hücrede p = 1); m = c2_olc'ye verilen hipotez sayısı (ya da m_bh)
- bilgi:
-   h5: eski cetvel: YH.yh_sim, stop0 = hat x 0,98 (hat = son 20 geçerli bar en düşük Low, t dahil), +%5 kapanışla stop'tan önce (h5 / st5 / h10)
-   atr: ATR stop kolu: stop0 = E0 - 2 x ATR14(t), +%5 stop'tan önce, 15 bar (h5_atr / st5_atr)
-   r60: OC.oc_esli r60 eşli fark (aynı gün, aynı momentum beşliği x likidite üçlüsü)
-   r15_med: hücre R15 medyanı
- A:
-   pazar: ['ABD', 'AVR', 'BIST']
-   karar_pazar: ['ABD', 'AVR']
-   n: [30, 100, 300, 1000, 'yari']
-   delta: [0.0, 0.01, 0.02, 0.03, 0.05]
-   tohum_sayi: 20
-   tohum: 2121
-   n_azami_pay: 0.6666666666666666
-   olay: DS ANA olayları (ds_olay.csv.gz: pazar, sembol, tarih; c2_olay ile giriş + kova + R15); havuz = hücrede R15 ölçülebilir ve tek başına (deneme = kendisi) >= 5 eşi olan olaylar; her tohum x n x hücre havuzdan yerine koymadan n 'tutan' (yari = havuzun yarısı; n > 2/3 havuz ise ölçülmez)
-   taban:
-     DS: tutan = seçilen DS olayları (delta 0 = DS olaylarının kendi konum eşli FARK'ı; saf sıfır değil)
-     RAST: tutan = her seçilen DS olayının giriş gününde havuzdan rastgele hisse (gün içinde yerine koymadan; c2_plasebo ile aynı çekiliş); delta 0 = SAF PLASEBO
-   surukleme: tutan olayın R15'i (1 + R15) x (1 + delta) - 1 (15. barda +delta doğrusal sürüklenmenin kapanış etkisi; E0 değişmez); eşler dokunulmaz (deneme = tutan küme)
-   yakala: hücre TUTAR şartları güç HARİÇ (n >= 30, FARK > 0, boot alt > 0, SIRA > 0,50, L3O > 0); ayrıca güç dahil TUTAR ve p (tek yönlü '+') < 0,05 bilgi
- B:
-   kaynak: POZITIF_KONTROL pk_b_olay.csv.gz (aynı ANA olaylar: B1 momentum 12-1 ay sonu ABD + AVR, B2 PEAD ABD; U üst onda, A alt onda) ve pozitif_kontrol.json h5 FARK'ı (yan yana)
-   hipotez:
-     B1U: ['U', '+']
-     B1A: ['A', '-']
-     B2U: ['U', '+']
-     B2A: ['A', '-']
-   pazar:
-     B1: ['ABD', 'AVR']
-     B2: ['ABD']
-   karar_pazar: ['ABD']
-   bilgi_pazar: ['AVR']
- C:
-   n: ['tam', 100, 300]
-   tohum: 2131
-   tanim: plasebo kapısı her pazar x dönem hücresinde DS ANA olay günleriyle (tam n ve n 100 / 300 rastgele alt küme günleri) ve B hücrelerinde (c2_olc); AVR sınama tanısı: günlük havuz büyüklüğü, eş sayısı, eşsiz payı, dolu kova sayısı
- sonuc_kurali:
-   KUSUR: (i) B1A (momentum alt onda) ABD eğitim ya da sınama hücresinde R15 FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı ABD eğitim / sınama DS hücrelerinden (tam n) birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR hücresinde n >= 100 tohumları BİRLEŞİK (100 / 300 / 1000 / yarı x 20 tohum) > %10 (v2.1; v2.0 tek n hücresi). KUSUR -> nedeni yazılır, cetvel düzeltilir, ön kayıt v2.2, yeniden koşu (en çok 2 tur)
-   EVET: KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin her birinde bir n'de >= %80 yakalama VE B'de bir + etki (B1U ya da B2U) ABD eğitim ve sınamada FARK > 0 ve en az birinde boot alt > 0 VE bir - etki (B1A ya da B2A) ABD eğitim ve sınamada FARK < 0
-   KISMEN: KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)
-   HAYIR: KUSUR var (iki düzeltme turundan sonra da)
- yeniden_uretim:
-   elle_r15: 50
-   elle_es: 5
-   tohum: 2141
-   tanim: c2_b_olay satır dosyasından iki hücre (B1U ABD sınama, B1A ABD eğitim) ortalama FARK / SIRA düz pandas ile; 50 olayın R15'i ham veriden düz döngüyle; 5 olayın eş ortalaması bütün evren üzerinde düz döngüyle (kova elle)

## 3. EĞİTİM DÖNEMİNDE SABİTLENEN KOVA SINIRLARI (sayı; cetvel2_esik.json)

| pazar | ATRP t1 | ATRP t2 | F15 q1 | F15 q2 | F15 q3 | eğitim havuz hisse-gün | likidite |
|---|---|---|---|---|---|---|---|
| ABD | 0.022713 | 0.036047 | 0.285417 | 0.616971 | 0.876991 | 1513661 | OC H % 3 (günlük kesit) |
| AVR | 0.019577 | 0.028393 | 0.282253 | 0.610589 | 0.871181 | 753886 | OC H % 3 (günlük kesit) |
| BIST | 0.033376 | 0.048387 | 0.263721 | 0.578442 | 0.848691 | 510386 | OC H % 3 (günlük kesit) |

## 4. GÜÇ EĞRİSİ (cetvel2_guc.json; delta +0,02 R15; sigma(n) = exp(a + b ln n); güç = Phi(delta / sigma - 1,96))

| pazar | dönem | N (DS ANA, eşli) | sd (olay) | a | b | n = 30 | 100 | 300 | 1000 | 3000 | güç >= 0,80 için en küçük n |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | egitim | 13873 | 0,1349 | -1,8976 | -0,5228 | 0,12 | 0,32 | 0,75 | 1,00 | 1,00 | 340 |
| ABD | sinama | 9938 | 0,1477 | -1,7745 | -0,5340 | 0,11 | 0,28 | 0,70 | 1,00 | 1,00 | 380 |
| AVR | egitim | 4363 | 0,1092 | -2,0989 | -0,5341 | 0,17 | 0,48 | 0,93 | 1,00 | 1,00 | 210 |
| AVR | sinama | 1861 | 0,1042 | -2,0807 | -0,5465 | 0,18 | 0,51 | 0,95 | 1,00 | 1,00 | 190 |
| BIST | egitim | 2416 | 0,1150 | -1,8850 | -0,5705 | 0,15 | 0,45 | 0,93 | 1,00 | 1,00 | 220 |
| BIST | sinama | 5433 | 0,1178 | -2,0293 | -0,5270 | 0,15 | 0,41 | 0,87 | 1,00 | 1,00 | 260 |

## 5. PREFIX (K2; cetvel2_prefix.json)

- ABD: 30 olay, bozuk 0
- AVR: 30 olay, bozuk 0
- BIST: 30 olay, bozuk 0

## 6. PLASEBO KAPISI EŞİKLERİ

- |ortalama FARK| < 0.005 (0,5 puan) VE TUTAR payı <= 0.07 (200 tohum); geçmeyen hücre KARAR VERMEZ.

## 7. ÖNCEDEN YAZILI SONUÇ KURALI (pozitif kontrol v2)

- KUSUR: (i) B1A (momentum alt onda) ABD eğitim ya da sınama hücresinde R15 FARK > 0 VE boot alt > 0; ya da (ii) plasebo kapısı ABD eğitim / sınama DS hücrelerinden (tam n) birinde düşer; ya da (iii) A RAST tabanı delta 0 yakalama payı (güç hariç) bir ABD / AVR hücresinde n >= 100 tohumları BİRLEŞİK (100 / 300 / 1000 / yarı x 20 tohum) > %10 (v2.1; v2.0 tek n hücresi). KUSUR -> nedeni yazılır, cetvel düzeltilir, ön kayıt v2.2, yeniden koşu (en çok 2 tur)
- EVET: KUSUR yok VE A RAST tabanında delta +%2'de dört karar hücresinin her birinde bir n'de >= %80 yakalama VE B'de bir + etki (B1U ya da B2U) ABD eğitim ve sınamada FARK > 0 ve en az birinde boot alt > 0 VE bir - etki (B1A ya da B2A) ABD eğitim ve sınamada FARK < 0
- KISMEN: KUSUR yok ama EVET şartlarından biri eksik (hangisi yazılır)
- HAYIR: KUSUR var (iki düzeltme turundan sonra da)

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = aynı giriş günü, aynı pazar, aynı kova (ATRP tercili x OC likidite üçlüsü x F15 çeyreği), bütün evren havuzu, aynı geometri (R15 stop'suz, aynı E0 kuralı); aynı denemenin o günkü olayları ve olayın kendisi eş dışı; en az 5 eş (c2_es); taban rastgele olay sağlaması = plasebo kapısı (aynı gün rastgele havuz hissesi, 20 tohum; c2_plasebo); mekanik üstünlük: stop / hedef yok, R15 olay ve eşte aynı tanım (h5'in oynaklık ödülü yok) |
| K2 | geleceğe bakma | EVET | kova girdileri (ATRP_t, F15_t, likidite) giriş gününden ÖNCEKİ son geçerli barda; c2_prefix: her pazarda 30 rastgele olayda veri t'de kesilince ATRP / F15 / hat aynı (rtol 1e-9; cetvel2_prefix.json, tutmazsa DURUR); kova sınırları eğitim havuzundan getirisiz; R15 yalnız giriş açılışından sonrası |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması; R15 yalnız geçerli barlar (hissenin kendi takvimi); sinyal günü geçersiz bar ise olay düşer (oc_olay_hazirla) |
| K4 | tekilleştirme | EVET | olaylar aynı hissede >= 15 işlem günü arayla (tekil_gun 15 = ufuk; örtüşmeyen 15 bar); n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan FARK raporda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (oc_olay_hazirla d; R15 paydası P['Op'][d, j]); eşler aynı gün açılışı |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş); R15 / ATRP / F15 oran (birimsiz); likidite üçlüsü günlük kesit sırası (TL enflasyonu etkisiz; AVR x Kur); geçmiş bölünme şüphesi havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580, V_BIST); yanlılık hem olaya hem eşe; raporda yazılır |
| K8 | örneklem ve dönem | EVET | eğitim 2016-22 / sınama 2023-01 .. 2026-08 ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç eğrisi (delta +2 puan, %80) ile n yeterliliği; BH q 0,10 (m sabit); A: 20 tohum x 5 n x 5 delta |
| K9 | ön kayıt | EVET | CETVEL2_ON_KAYIT_v2.1.md (v2.0 CETVEL2_ON_KAYIT.md silinmedi; düzeltme C2_ESIK['duzeltme_v21']): C2_ESIK sha, CETVEL2.py sha, kova sınırları (sayı), güç eğrisi, DS / YH / OC / PK sha'ları, girdi dosyası sha'ları; c2_kapi ön kaydın git'te işlenmiş ve değişmemiş olduğunu + ik_kontrol_kapisi'ni denetler; sıra kod commit -> ön kayıt commit -> koşu; tasarım iş tanımından (ca5d2a8) sonuç görülmeden |
| K10 | ayrıştırma | UYGULANMAZ | ham haber / KAP / SEC ayrıştırması yok; olay kümeleri önceki koşuların satır dosyalarından (ds_olay.csv.gz, pk_b_olay.csv.gz) okunur, sayıları huni'de karşılaştırılır |
| K11 | yeniden üretim | EVET | c2_yeniden: B1U ABD sınama ve B1A ABD eğitim hücreleri satır dosyasından düz pandas; 50 olayın R15'i ham veriden düz döngüyle; 5 olayın eş ortalaması bütün evren üzerinde düz döngüyle (kova elle); tutmazsa koşu TUTMADI |
| K12 | ifade | EVET | bu iş cetvel sınaması; 'iz' iddiası yok; FARK, SIRA, p, yakalama payı ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_c2; c2_ / C2_ önekleri dışında ezme DURUR; test); DS / YH / OC / PK değişmedi (sha ön kayıtta); defter dosyalarına dokunulmadı; e-posta / anahtar taraması (YH._yh_yaz); dış servis yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; cetvel sınaması |
