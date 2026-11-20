# POZİTİF KONTROL — ÖN KAYIT (2026-11-20 21:29:56 UTC)

POZITIF_KONTROL v1.0 (2026-11-20): 15 bar cetveli pozitif kontrol (yapay iz, momentum 12-1, bilanço sonrası sürüklenme, örnekler). Bu dosya ölçümden ÖNCE yazıldı ve git'e işlendi; pk_kapi PK_ESIK ve kod sha'larını, cetvel sha'larının DS_ON_KAYIT.md ile eşitliğini, git kaydını ve IZ_KARNE.ik_kontrol_kapisi'ni denetler; biri tutmazsa koşu DURUR. Sonuç (h5 / getiri) bu dosya yazılırken hesaplanmadı.

- PK_ESIK_SHA: `e8397e5f5edd3ff0ea6f3082dad8d6fc6d2ebfa3af661e109a7e0e2c869f5231`
- PK_KOD_SHA: `eaad69da47f825695e05ef09d413837ca5d67189111a8616ac663d2cd01dec15`
- DS_KOD_SHA: `b3b3a2154c68d77f61dcd7d2246262bd08753e4ee3735a78b83659ba9ca46ddf`
- YH_KOD_SHA: `812d188c20a64e27f351764ec462969b352322b7763181e696e24dca392ea95e`
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d`
- DS_ESIK_SHA: `052ac9c4439cf5eaa3679c3d2ae9ba6389021321008d474015a2b7e9af208a9d`
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9`
- OC_ESIK_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
- DS_ESIK_JSON_SHA: `80305c746420876283e425d28632f503c695ea00136700b8c03d74bb678ca83d`
- V_ABD_SHA: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR_SHA: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST_SHA: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- CETVEL = DS ön kaydı: DS_KOD_SHA, YH_KOD_SHA, OC_KOD_SHA, S6_KOD_SHA, DS_ESIK_SHA, YH_ESIK_SHA, OC_ESIK_SHA, DS_ESIK_JSON_SHA

## 1. TASARIM (PK_ESIK; iş tanımı commit 4505d5c)

- surum: PK1.0
- cetvel: DUSUS_SONRASI ds_olc / ds_es_topla / ds_hucre / ds_perm_p (DS_ESIK: boot 2000 ay kümeli, güç delta 0,05 R 1000, perm 10000) + YAPI_HEDEF yh_sim / yh_getiri (YH_ESIK['olcu']: ufuk 15, hedef +%5 / +%10 kapanışla, stop0 = hat x 0,98, kilit / takip) AYNEN; hat = son 20 geçerli bar en düşük Low (t dahil); giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); eş = aynı giriş günü, aynı kova (ATRP tercili x OC likidite üçlüsü), özelliği 0, 15 barı ölçülebilir, olayın stop uzaklığı d ile; en az 3
- alfa: 0.05
- donem:
-   egitim: ['2016-01-01', '2022-12-31']
-   sinama: ['2023-01-01', '2026-08-31']
-   not: A: DS dönemleri ve ambargosu AYNEN (ds_esik.json). B: ambargo yok (eşikler sonuç kullanmaz: momentum kesitsel sıra; PEAD onda sınırları eğitim tepkilerinden, getirisiz)
- A:
-   pazar: ['ABD', 'AVR']
-   hucre: ['egitim', 'sinama']
-   n: [30, 100, 300, 1000, 'yari']
-   delta: [0.0, 0.01, 0.02, 0.03, 0.05]
-   tohum_sayi: 20
-   tohum: 3101
-   ufuk: 15
-   n_azami_pay: 0.6666666666666666
-   olay: DS ANA olayları (ds_hazirla(pazar, esik_json = ds_esik.json) + ds_olc; DS koşusundaki küme ve eşler), h5 ölçülebilir ve DS içi eşi (>= 3) olan olaylar havuzu; her tohum x n x hücre: havuzdan yerine koymadan n 'tutan' (yari = havuzun yarısı); öteki olaylar F = 0 (eş adayı)
-   surukleme: yalnız tutan olayların penceresi (birleşik takvim, giriş barı satır 0, 30 satır): k. geçerli bar (k = 0 giriş barı) Close / High / Low x (1 + delta x min(k + 1, 15) / 15); açılış (giriş fiyatı) ve stop0 değişmez; yh_sim yeniden; eşler, taban ve güç tabanı (es_h5_hepsi) DOKUNULMAZ
-   yakala: FARK > 0 VE boot %95 alt > 0 VE p (ds_perm_p, tek yönlü '+') < 0,05; bilgi: iki yönlü p ile aynı şart; dört hücre (ABD + AVR x eğitim + sınama) birlikte yakalama (aynı tohum)
-   plasebo: delta = 0: yanlış pozitif payı (beklenen tek yönlü <= %5)
- B:
-   pazar: ['ABD']
-   bilgi_pazar: ['AVR']
-   onda: [0.1, 0.9]
-   B1:
-     ad: 12-1 momentum
-     olay: ay sonu t = birleşik takvimde ayın son işlem günü; MOM_12_1 = C(t-21) / C(t-252) - 1 (hissenin kendi geçerli barları, t'de geçerli bar, >= 252 bar geçmiş); OC.oc_olay_hazirla (havuz, giriş t+1 açılış) sonrası aynı t'deki hisseler arasında sıra (rank first, pct): üst onda (> 0,90) U, alt onda (<= 0,10) A; ötekiler orta (eş adayı)
-     yon:
-       U: +
-       A: -
-       UA: +
-   B2:
-     ad: bilanço sonrası sürüklenme (PEAD)
-     kaynak: sec_ozet 8-K madde 2.02 başvuru tarihleri (K55)
-     olay: bilgi barı b0 = başvuru gününden SONRAKİ ilk geçerli bar (DS sınıf II ile aynı); t = b0; tepki = C(b0) / C(b0-2) - 1 - (E(b0) / E(b0-2) - 1), E = evren eşit ağırlık endeksi (DS.ds_baglam); aynı (hisse, t) bir kez; onda sınırları eğitim (giriş 2016-22) olaylarının tepkisinden (getirisiz) q10 / q90; U = tepki >= q90, A = tepki <= q10; ANA = U ya da A, aynı hissede >= 15 birleşik takvim günü arayla ilk; eş adayı = aynı giriş günü havuzdaki öteki hisseler
-     yon:
-       U: +
-       A: -
-       UA: +
-   kod: F_<B>U: U = 1, A = NaN, öteki = 0 (eş = orta); F_<B>A: A = 1, U = NaN, öteki = 0; F_<B>UA: U = 1, A = 0, öteki NaN (doğrudan üst - alt; eş = aynı gün aynı kova alt onda)
-   kova: ATRP tercili (ATR14 / C, t; tercil sınırları eğitim ANA olaylarından) x OC likidite üçlüsü (H[d] % 3) - DS ile aynı
-   uc_cetvel: (1) 15 bar h5 FARK (ds_hucre); (2) aynı olay ve AYNI eşlerde stop'suz 15 bar kapanış getirisi r15 = C(15. geçerli bar) / giriş açılışı - 1, fark = r15 - eş ort r15; (3) OC r60 eşli fark (oc_esli: aynı gün, aynı momentum beşliği x likidite üçlüsü). Hepsi aynı istatistik: ay kümeli boot (yh_d3_boot_l3o) ve ay kümeli işaret permütasyonu (ds_perm_p) önceden yazılı yönle; U - A yayılımı ay kümeli ortak bootstrap
-   olcu_birim: h5 FARK yüzde puan (+%5 stop'tan önce payı farkı); r15 ve r60 farkı getiri yüzdesi
- C:
-   bist: [['TEHOL-24', 'TEHOL', '2024-12-12'], ['TEHOL-25', 'TEHOL', '2025-05-28'], ['BINBN-24', 'BINBN', '2025-01-21'], ['KTLEV-24', 'KTLEV', '2024-10-15']]
-   bist_kural: sinyal günü = kutu sonu (Cemal etiketi, FON_IZI FI_K18_VAKA / CEMAL_COL_KURALLARI) - 5 .. + 60 geçerli bar penceresinde ilk S6 'al' günü (YH.yh_s6_hisse; hat = Y1 hattı: kutu_alt ya da DİP(t-1)); yoksa ilk C_t > max(H, t-120 .. t-1) günü (hat = son 20 bar en düşük Low); ikisi de yoksa 'sinyal yok'. 'KETLV' veride KTLEV
-   ekim: [['CAPR', '2026-10-22', 'ALKT', 15.08, 13.28], ['ARRY', '2026-10-21', 'RARE', 16.02, 13.8], ['AXGN', '2026-10-22', 'ALKT', 15.08, 13.28], ['TDOC', '2026-10-21', 'RARE', 16.02, 13.8], ['JBLU', '2026-10-23', 'FNF', 41.24, 37.69], ['LQDA', '2026-10-23', 'FNF', 41.24, 37.69]]
-   ekim_kural: giriş = ESLER_2026-10-22 giriş günü açılışı; t = önceki geçerli bar; (a) kendi hattı: hat = son 20 bar en düşük Low (t dahil), stop0 = hat x 0,98; (b) ESLER geometrisi: stop0 = giriş x (1 - adayın d), d = 1 - aday stop0 / aday giriş (CANLI_SONUC); veri /tmp/veri_canli (kriz kesiği yalnız bu bilgi satırında aşılır)
- yeniden_uretim:
-   A: ['ABD', 'sinama', 300, 0.03, 0]
-   B: ['B1U', 'sinama']
-   elle_n: 50
-   elle_es_n: 5
-   tohum: 3109

## 2. ÖNCEDEN YAZILI OKUMA KURALI

- A: cetvel bir (n, delta) noktasında 'görür' = o pazar x hücrede 20 tohumun >= %80'inde yakalama. Plasebo (delta 0) yanlış pozitif payı > %10 ise cetvel 'gevşek' yazılır.
- B: bilinen etki 'görünür' = bir cetvelde eğitim VE sınama hücrelerinde fark beklenen yönde ve p < 0,05 (U: +, A: -, UA: +). Cetvel duyarlılığı: aynı olaylarda h5 FARK z (fark / boot yarı genişliği) ile r15 ve r60 z'si yan yana.
- SONUÇ: HAYIR = A'da gerçek boyutta (yari) delta +%5 bile dört hücrede >= %80 yakalanmıyor; EVET = A'da bir delta'da yakalanıyor VE B'de en az bir bilinen etki (kod) h5 cetvelinde görünür; KISMEN = A'da yakalanıyor ama hiçbir bilinen etki h5'te görünmüyor (r15 / r60'ta görünüp görünmediği ayrıca yazılır). 'Daha duyarlı cetvel' = aynı olaylarda |fark| / boot yarı genişliği büyük olan.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = DS ile aynı: aynı giriş günü, aynı kova (ATRP tercili x OC likidite üçlüsü), F == 0, olayın d'si ile aynı 15 bar kuralı (ds_olc / ds_es_topla, kopya yok); A'da sürüklenme yalnız tutan olayın kendi penceresine eklenir, eşler dokunulmaz; B'de U ve A orta eşlere karşı ayrı + doğrudan U-A; mekanik üstünlük: sürüklenme dışında olay ile eş aynı süreçten (A plasebo delta 0) |
| K2 | geleceğe bakma | EVET | MOM t'de bitmiş barlardan (t-21, t-252); PEAD tepkisi b0 kapanışına kadar, giriş b0+1 açılışı; PEAD onda sınırları eğitimden (getirisiz) sabit; ATRP / hat t'de; test_pozitif_kontrol prefix: veri t'de kesilince MOM / tepki / ATRP / hat aynı |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) + DS açılış kırpması (ds_veri); 15 bar yalnız geçerli barlar (yh_sim); sinyal günü geçerli bar (oc_olay_hazirla) |
| K4 | tekilleştirme | EVET | A: DS ANA olayları (15 gün tekil); B1 ay sonu (aynı hissede >= ~21 bar arayla); B2 ANA >= 15 bar arayla, aynı (hisse, t) bir kez; n = ölçülen olay; boot / permütasyon birimi giriş ayı; medyan raporda (B) |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (oc_olay_hazirla d; yh_sim satır 0); C Ekim: ESLER giriş günü açılışı |
| K6 | veri birimi | EVET | V_*.pkl tek kip (fi_k1_veri düzeltilmiş); oranlar birimsiz; AVR likidite x Kur; geçmiş bölünme şüphesi havuz dışı (OC); C Ekim verisi /tmp/veri_canli aynı kip (CANLI_SONUC ile aynı kaynak) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, V_AVR 580); yanlılık hem olaya hem eşe; raporda yazılır; A'da sürüklenme bilinen değer olduğu için yanlılıktan bağımsız |
| K8 | örneklem ve dönem | EVET | A: 20 tohum x 5 n x 5 delta x 2 pazar x 2 hücre, n 30..yarı; B: eğitim 2016-22 / sınama 2023-26 ayrı; n < 30 hücre ÖLÇÜLEMEDİ yazılır; C n = 1 / örnek: bulgu denmez, tek tek okunur |
| K9 | ön kayıt | EVET | POZITIF_KONTROL_ON_KAYIT.md: PK_ESIK sha, kod sha, cetvel sha'ları (DS_ON_KAYIT ile eşit), veri sha; pk_kapi ön kayıt git'te işlenmiş ve değişmemiş + ik_kontrol_kapisi denetler; tasarım iş tanımından (commit 4505d5c) önce yazıldı, sonuç görülmeden |
| K10 | ayrıştırma | EVET | sec_ozet 8-K madde alanı virgülle ayrılır (DS._ds_sec_olay ile aynı ayrıştırma, kopya yok); bilgi barı başvuru günü sonrası ilk geçerli bar; 3 ham satır ön kayıtta gösterilir |
| K11 | yeniden üretim | EVET | A bir hücre (ABD sınama n 300 delta +%3 tohum 0) ve B bir hücre (B1U sınama) satır dosyasından düz pandas ile; A'da 50 tutan olayın sürüklenmiş h5'i, B'de 50 olayın h5 / r15'i ve 5 olayın eş h5'i yh_sim'den bağımsız düz döngüyle |
| K12 | ifade | EVET | bu iş cetvel sınaması; 'iz' iddiası yok; yakalama payı, FARK ve p ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_pk; pk_ / PK_ önekleri dışında ezme DURUR; test); DS / YH / OC değişmedi (sha = DS ön kaydı); defter dosyalarına dokunulmadı; e-posta / anahtar taraması (YH._yh_yaz); dış servis yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; cetvel sınaması |
