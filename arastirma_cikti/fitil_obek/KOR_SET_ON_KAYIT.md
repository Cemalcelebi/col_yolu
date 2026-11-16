# FITIL_KOR — ÖN KAYIT (fitil öbeği: hata nerede? üç halka)

FITIL_KOR v1.0 (2026-11-16): fitil öbeği üç halka (tanım bağlamı / doğrulama ölçüsü / algılama kör seti)

- FK_ESIK_SHA: `7f100663df1e8a6f1c21927c73b5b63b393a7ca7e011acd567e3992a9aa57e98`
- FK_KOD_SHA: `be4f883e5bfe64df54da2e810631103ba4cbed90a2c64bd9725c2554015d307d`
- FO_ESIK_SHA: `1ca5faf0ea7d59a7dcbd34fec464dad28e095f9ca0874ce75954b7268bcbebd5`
- S6_PRM_SHA: `f54deadbbfde54519150ca0c3a25eca5872ef20f70b14a5eaf61d18d0b13b696`
- IS_TANIMI_SHA: `051cbf1d68d02f87d01567cc354335554b92f9df47f36dcc1da4b3c01e84cdb3`
- İş tanımı git: cbf1cc5cd9 (2026-11-16T20:28:12+00:00)
- ZAMAN (UTC): `2026-11-16 21:05:30 UTC`

Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / kırılım hesaplanmadı (yalnız durum günü ve cetvel tekil olay sayımı, getirisiz). `kos` / `kor` kontrol listesi, cetvel üç sha'sı, yukarıdaki beş sha ve iş tanımının git kaydı tutmazsa durur. Eşikler sonuç görülünce değişmez.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Tanım (sabit)

- Fitil: Ç187 FITIL_OBEK.FO_ESIK aynen (fo_bar / fo_pencere / fo_kural; k = 10): S+ = ASIM >= 0,20 VE ALTYOK >= 0,50; S- = ASIM <= -0,20 VE USTYOK >= 0,50; KUCUK = pencere medyanı R/C <= 0,75 x ATR%250.
- S6: S6_TABAN.s6_taban, v1.1 varsayılanları (S6_PRM; parametre verilmez); girdi oc_veri temiz barları (geçerli bar, kriz kesiği).
- TABAN İÇİ: TABAN İÇİ (t, as-of t): S6 ölçülür bar (i >= 250) VE bolge_id >= 0 VE durum YENI / SURER / YENIDEN (bölge t'de açık; AL / KIRILDI günü bölge biter, sayılmaz) VE bölgenin sınıfı (bölgenin ilk barı = onay günündeki 'sinif') DIP.
- TABAN DIŞI: TABAN DIŞI (t): S6 ölçülür bar VE TABAN İÇİ değil (bölge yok, bölge YOL / ORTA sınıfı, AL / KIRILDI günü).
- Ölçülür: bütün satırlar S6 ölçülür barlarda (ilk 250 geçerli bar dışarıda); ABD evren_bas öncesi atılır.
- Varyantlar: gevşek {'asim_min': 0.1, 'altyok_min': 0.4}, sıkı {'asim_min': 0.3, 'altyok_min': 0.6}, küçük: S+ k=10 VE KUCUK.
- S+DÜZ: EK TANIM (Cemal 16 Kas sözlü, ön kayıttan önce): DÜZ DİP = son 10 geçerli bar (t dahil) Low yayılımı (max L - min L) / medyan(H - L) <= 1,0 (0,7 ve 1,5 bilgi); DİP BAĞLAMI = TABAN İÇİ YA DA konum120 = (C - min C) / (max C - min C) son 120 geçerli kapanış <= 0,25; S+DÜZ = S+ (k=10) VE DÜZ DİP VE DİP BAĞLAMI; K_DUZ = DÜZ DİP VE DİP BAĞLAMI VE S+ değil (düz dip tek başına mı iş yapıyor).
- Kırılım 10 mum kutusu: EK (S+DÜZ): aynı kural, kutu = t'de biten 10 geçerli barın max High / min Low (taban dışında da tanımlı); S+DÜZ vs K_SP ve vs K_DUZ (düz dip tek başına), SP_ic vs K_SP bilgi; karar biçimi kirilim_karar ile aynı, BİLGİ.
- Kör set ek: EK (Cemal 16 Kas, ön kayıttan önce): S+DÜZ havuzundan 10 ek sayfa (ABD 5, BIST 5), toplam 50; SPD grubu seçimde en sonda; olc kararı ilk 30 S+ vs 10 S- ile; SPD E payı bilgi.
- Olay: durum günleri ORTAK_CETVEL.oc_olc'a verilir (giriş t'den sonraki ilk geçerli açılış; aynı hissede 60 gün tekilleştirme: ilk gün).

Satırlar:

- SP_ic: S+ TABAN İÇİ [HALKA 1 ANA]
- SM_ic: S- TABAN İÇİ [HALKA 1 ANA, ayna]
- SP_dis: S+ TABAN DIŞI [bilgi]
- SM_dis: S- TABAN DIŞI [bilgi]
- SP_tum: S+ bütün ölçülür günler (Ç187 SP_k10, S6 ölçülür süzgeciyle) [bilgi / HALKA 3 genel]
- SM_tum: S- bütün ölçülür günler [bilgi / HALKA 3 genel]
- K_SP: TABAN İÇİ ve S+ OLMAYAN günler [HALKA 1 (b) kontrol; HALKA 3 kontrol]
- K_SM: TABAN İÇİ ve S- OLMAYAN günler [S- kontrol]
- K_SP_r: K_SP'den her bölgede tek RASTGELE gün (tohum 187; bölge içi konum dengesi) [bilgi kontrol]
- K_SM_r: K_SM'den her bölgede tek RASTGELE gün (tohum 187) [bilgi kontrol]
- SPg_ic: S+ gevşek (ASIM >= 0,10, ALTYOK >= 0,40) TABAN İÇİ [bilgi]
- SPs_ic: S+ sıkı (ASIM >= 0,30, ALTYOK >= 0,60) TABAN İÇİ [bilgi]
- SPk_ic: S+ VE küçük mum (KUCUK) TABAN İÇİ [bilgi]
- SPD: S+DÜZ (S+ VE düz dip <= 1,0 VE dip bağlamı) [EK; bilgi + ayrı satır]
- SPD07: S+DÜZ eşik 0,7 [bilgi]
- SPD15: S+DÜZ eşik 1,5 [bilgi]
- K_DUZ: düz dip (<= 1,0) VE dip bağlamı VE S+ değil [S+DÜZ kontrolü]
- SPDb: S+ VE düz dip (<= 1,0), dip bağlamı ŞARTSIZ [bilgi; kalibrasyonda TEHOL May 2025 / BINBN dip bağlamını geçmedi (konum120 > 0,25, taban yok), getiri görülmeden eklendi]
- K_DUZb: düz dip (<= 1,0) VE S+ değil, bağlam şartsız [SPDb kontrolü]

r60 (cetvel) satırları: SP_ic, SM_ic, SP_dis, SM_dis, SP_tum, SM_tum, K_SP, K_SM, K_SP_r, K_SM_r, SPg_ic, SPs_ic, SPk_ic, SPD, SPD07, SPD15, K_DUZ, SPDb, K_DUZb. r20 satırları: SP_ic, SP_tum, K_SP, SM_ic, SM_tum, K_SM, SPD, K_DUZ.

## HALKA 1 karar kuralı (önceden yazılı)

- (a) taban içi S+ vs eşler: FITIL_OBEK.fo_etiket (Ç187 kuralı aynen; karar hücreleri ABD / AVR x 2023 / 2024-26, BIST bilgi); S- ayna.
- (b) taban içi S+ vs K_SP (eşli farkların farkı): hücre AYRIŞIR = iki grup n >= 30, fark > 0 VE %95 alt uç > 0; AYRIŞMAZ = n >= 30 ve şart tutmadı; n < 30 ÖLÇÜLEMEDİ. S- ayna: fark < 0 VE üst uç < 0. Genel: dört karar hücresi AYRIŞIR -> 'KONTROLDEN AYRIŞIR'; en az biri -> 'KISMİ (hücreler)'; hiçbiri -> 'AYRIŞMAZ'.
- Varyant: SPg_ic / SPs_ic / SPk_ic: (a) ile aynı etiket, BİLGİ (çoklu: 3 varyant; karar değildir).
- Fark bootstrap: iki grup (A olay, B kontrol) AYRI ay kümeli yeniden örnekleme (her grupta kendi ayları, yerine koyarak); fark = ort(A) - ort(B); %95 = 2,5 / 97,5 yüzdelik (n 2000, tohum 27, küme giriş ayı).

## HALKA 3 kuralı (önceden yazılı)

- r20: OC_ESIK kopyası, yalnız olcu.ufuk = 20: r20 = giriş + 19 birleşik takvim günü kapanışı / giriş açılışı - 1; eşler, havuz, tekilleştirme aynı; slot tutma 29 gün. Hücre: ortalama eşli fark, %95, sıra, oc_hucre 'tutar' (5 şart) BİLGİ (güç tablosu r60 için yazıldı; r20'de 'TUTMADI' etiketi kullanılmaz). r20 fark (b): SP_ic - K_SP, SM_ic - K_SM, aynı bootstrap.
- Kırılım: TABAN İÇİ olay (cetvel tekil olayları, r60 koşusunun olay satırları): t'deki bölge kutusu (kutu_ust = tavan, kutu_alt = dip; as-of t). t'den sonraki 60 geçerli bar (hissenin kendi barları; t+1 .. t+60) kapanışları: ilk C > tavan barı -> YUKARI; ilk C < dip x 0,98 barı -> AŞAĞI; hangisi önce; ikisi de yoksa YOK. 60 bar kriz kesiğinden (31.08.2026) ya da hissenin son barından önce dolmuyorsa olay ÖLÇÜLMEZ. Dönem = cetvel dönemi (giriş).
- Kırılım kararı: S+: YUKARI oranı(SP_ic) - YUKARI oranı(K_SP); hücre AYRIŞIR = iki grup n >= 30, fark > 0 VE %95 alt uç > 0. S- ayna: AŞAĞI oranı(SM_ic) - AŞAĞI oranı(K_SM) > 0 VE alt uç > 0. Genel etiket h1_karar.b ile aynı biçim.
- Genel S+: TABAN DIŞI / genel S+ için tavan / dip yok -> kırılım UYGULANMAZ; genel için cetvelin 'once20' (60 gün +%20 önce -%10) olay oranı vs eş oranı BİLGİ.

## HALKA 2 kör set (önceden yazılı)

- Seçim: havuz = o grubun durum günleri (SP_ic: S+ ve TABAN İÇİ; SP_dis: S+ ve TABAN DIŞI; SM: S- bütün ölçülür günler), t en az 50 geçerli barın sonu; gün düzeyinde eşit olasılıklı rastgele (tohum 1116, grup ve pazar sırası: SP_ic ABD, SP_ic BIST, SP_dis ABD, SP_dis BIST, SM ABD, SM BIST); aynı hisse sette bir kez; 50 sayfa (EK S+DÜZ 10 dahil) karıştırılır (aynı tohum).
- Grup / pazar: {'SP_ic': {'ABD': 8, 'BIST': 7}, 'SP_dis': {'ABD': 7, 'BIST': 8}, 'SM': {'ABD': 5, 'BIST': 5}, 'SPD': {'ABD': 5, 'BIST': 5}}.
- Sayfa: bir sayfa = pencere (son 10 mum, gri zemin) + öncesi 40 mum; SONRASI YOK; hisse adı / tarih / pazar / fiyat rakamı yok; fiyat ekseni oransal (pencereden önceki son kapanış = 0 %); hacim altta; numara 'No k'.
- Yanıt: E = benim mumum, H = değil, B = belirsiz.
- Okuma: olc: E payı (B hariç payda ve B dahil ikisi de yazılır). 'ALGILAMA SAĞLAM' = S+ E payı >= 0,60 VE S+ E payı - S- E payı >= 0,30; 'ALGILAMA KIRIK' = S+ E payı < 0,40; arası 'KISMİ'. Taban içi / dışı E payı ve Fisher kesin p bilgi; n küçük (30 / 10): 'bulgu' değil, tanı.
- Kalibrasyon (kör sete girmez; adlı, tarihli): PAPIL BIST 2025-11-13 .. 2025-12-09 (oc_veri V_BIST); TEHOL_2505 BIST 2025-05-02 .. 2025-05-28 (oc_veri V_BIST; Cemal düzeltmesi (16 Kas): bölge 2024-12-01 .. 2025-05-28, parmak izi Mayıs 2025); TEHOL_bolge BIST 2025-03-03 .. 2025-05-28 (oc_veri V_BIST; bağlam (Mart-Nisan yatay + Mayıs): S6 tabanı açık mı); BINBN BIST 2024-12-17 .. 2025-01-21 (oc_veri V_BIST; Cemal 'en net olan'); DGXX ABD 2026-10-20 .. 2026-11-16 (yfinance (auto_adjust=False, 2025-01-01 ..; V_ABD 31.08.2026'da kesik); 16 Kas seans içi yarım bar ATILIR (K3); ölçüme girmez).

## EK ÖRNEKLER (Cemal 16 Kas; ön kayıttan önce geldi, sonuç görülmeden eklendi)

- EK ÖRNEKLER (Cemal 16 Kas; sonuç görülmeden eklendi; TEHOL Şubat 2026 etiketi Cemal düzeltmesiyle KALDIRILDI, TEHOL bölgesi 2024-12-01 .. 2025-05-28, parmak izi Mayıs 2025; S+ beklenen: PAPIL, TEHOL Mayıs 2025, BINBN; S- beklenen: DGXX): her BIST kalibrasyon penceresi için olay t = (i) pencerenin İLK S+ (k10) günü (yoksa yazılmaz) ve (ii) pencerenin SON günü; her olay için cetvel r60 ve r20 eşli fark (tek olay, oc_olc; tekilleştirme olay başına ayrı), taban içi mi, taban içiyse kırılım (h3 tanımı); pencerede S+ / gevşek / sıkı / küçük S+ günleri ve S6 taban içi günleri. n küçük: BİLGİ, karar değildir.
- Pencereler: PAPIL 2025-11-13 .. 2025-12-09; TEHOL_2505 2025-05-02 .. 2025-05-28; BINBN 2024-12-17 .. 2025-01-21; TEHOL_bolge 2025-03-03 .. 2025-05-28. Hepsi adlı kalibrasyon sayfası olarak da basılır (fitil payları altta).

## Tanı okuması ve beklenti (önceden yazılı)

- HALKA tanısı (önceden yazılı okuma): (1) taban içi S+ (a) ya da (b) karar hücrelerinde TUTAR / AYRIŞIR ise ve Ç187 genel S+ tutmadıysa -> hata HALKA 1'de (bağlam); (2) r20 ya da kırılım AYRIŞIR, r60 ayrışmazsa -> hata HALKA 3'te (ölçü); (3) ikisi de hayırsa -> tanım bağlamı ve ölçü değişikliği sonucu değiştirmiyor; kalan HALKA 2 (algılama), kör setle Cemal'in gözüyle sınanır. Beklenti (Cemal): taban içi S+ eşlerden ve kontrolden iyi; YUKARI oranı S+'ta yüksek; S- ayna. EK: S+DÜZ (düz dip + dip bağlamı) için beklenti: 10 mum kutusunda YUKARI oranı K_SP ve K_DUZ'dan yüksek, r60 eşli fark > 0 (bilgi).

## Veri

- V_ABD.pkl sha256: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl sha256: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- ABD oc_veri notu: k34_yahoo ya da k34_evren.csv yok: ABD evreni yalnız V_ABD; evren dışı (fon / ETF) çıkarılan: 0 []; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- AVR oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı
- BIST oc_veri notu: hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı

## SAYIM (getirisiz; durum günü sinyal tarihine, cetvel tekil olay giriş tarihine göre dönem)

| Satır | Pazar | durum günü | OLAY (tekil, havuzda) 2016-22 / 2023 / 2024-26 |
|---|---|---|---|
| SP_ic | ABD | 1737 | 180 / 60 / 119 |
| SP_ic | AVR | 2157 | 160 / 76 / 185 |
| SP_ic | BIST | 4887 | 413 / 64 / 492 |
| SM_ic | ABD | 1097 | 116 / 57 / 87 |
| SM_ic | AVR | 1407 | 184 / 33 / 94 |
| SM_ic | BIST | 2565 | 192 / 2 / 36 |
| SP_dis | ABD | 43980 | 4027 / 861 / 2495 |
| SP_dis | AVR | 56063 | 3417 / 617 / 1830 |
| SP_dis | BIST | 61333 | 3323 / 669 / 2643 |
| SM_dis | ABD | 49719 | 5465 / 893 / 2401 |
| SM_dis | AVR | 62711 | 4481 / 582 / 1724 |
| SM_dis | BIST | 36629 | 1830 / 276 / 544 |
| SP_tum | ABD | 45717 | 4086 / 880 / 2537 |
| SP_tum | AVR | 58220 | 3465 / 646 / 1876 |
| SP_tum | BIST | 66220 | 3413 / 674 / 2721 |
| SM_tum | ABD | 50816 | 5511 / 922 / 2448 |
| SM_tum | AVR | 64118 | 4537 / 590 / 1747 |
| SM_tum | BIST | 39194 | 1880 / 277 / 556 |
| K_SP | ABD | 79192 | 2883 / 908 / 1905 |
| K_SP | AVR | 41875 | 1577 / 389 / 874 |
| K_SP | BIST | 60249 | 1637 / 237 / 1420 |
| K_SM | ABD | 79832 | 2888 / 911 / 1907 |
| K_SM | AVR | 42625 | 1574 / 391 / 883 |
| K_SM | BIST | 62571 | 1640 / 242 / 1452 |
| K_SP_r | ABD | 9896 | 2672 / 851 / 1790 |
| K_SP_r | AVR | 4024 | 1431 / 344 / 786 |
| K_SP_r | BIST | 6515 | 1428 / 234 / 1281 |
| K_SM_r | ABD | 9926 | 2691 / 852 / 1793 |
| K_SM_r | AVR | 4039 | 1427 / 338 / 800 |
| K_SM_r | BIST | 6602 | 1431 / 236 / 1305 |
| SPg_ic | ABD | 7994 | 786 / 245 / 528 |
| SPg_ic | AVR | 7357 | 536 / 194 / 435 |
| SPg_ic | BIST | 14810 | 805 / 132 / 914 |
| SPs_ic | ABD | 323 | 22 / 7 / 20 |
| SPs_ic | AVR | 484 | 32 / 23 / 42 |
| SPs_ic | BIST | 989 | 132 / 17 / 143 |
| SPk_ic | ABD | 1038 | 107 / 44 / 59 |
| SPk_ic | AVR | 983 | 95 / 48 / 85 |
| SPk_ic | BIST | 4233 | 372 / 57 / 431 |
| SPD | ABD | 951 | 43 / 11 / 30 |
| SPD | AVR | 1421 | 68 / 29 / 81 |
| SPD | BIST | 1176 | 195 / 18 / 209 |
| SPD07 | ABD | 255 | 4 / 1 / 4 |
| SPD07 | AVR | 500 | 11 / 8 / 20 |
| SPD07 | BIST | 268 | 61 / 0 / 42 |
| SPD15 | ABD | 3268 | 275 / 62 / 182 |
| SPD15 | AVR | 4226 | 295 / 97 / 253 |
| SPD15 | BIST | 4455 | 440 / 89 / 575 |
| K_DUZ | ABD | 18328 | 1736 / 450 / 1149 |
| K_DUZ | AVR | 11758 | 1101 / 225 / 557 |
| K_DUZ | BIST | 13275 | 1228 / 143 / 766 |
| SPDb | ABD | 2186 | 172 / 36 / 105 |
| SPDb | AVR | 6249 | 320 / 77 / 279 |
| SPDb | BIST | 3400 | 653 / 80 / 495 |
| K_DUZb | ABD | 60739 | 7112 / 1372 / 3854 |
| K_DUZb | AVR | 58432 | 4499 / 675 / 1973 |
| K_DUZb | BIST | 40995 | 3828 / 534 / 2066 |

Kural: hücre n < 30 ise ÖLÇÜLEMEDİ.

## SAPMA / sınır (sonuç görülmeden yazıldı)

- Ön kaydı alt ajan git'e işleyemez (commit yasak): iş tanımı koşudan önce işlendi; bu dosyanın sha'sı ve yazım zamanı halka_sonuc.json'a yazılır, kos zamanı ondan sonradır (--gitsiz). Ana model işlerken sha'yı karşılaştırır.
- k34_yahoo (veri2) yoksa ABD evreni yalnız V_ABD (oc_veri notu).
- Kontrol K_SP cetvel tekilleştirmesiyle bölgenin ilk günlerine yığılır (S+ günü bölgede daha geç olabilir): bu yüzden bölge başına tek rastgele gün K_SP_r bilgi kontrolü olarak yazılır.
- r20 hücrelerinde güç tablosu (r60) uygulanmaz; 'TUTAR' bilgi.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | (a) eşler YALNIZ ORTAK_CETVEL.oc_olc (aynı giriş günü, 60 gün momentum beşlisi x 20 gün likidite üçlüsü, 200 plasebo); (b) kontrol = TABAN İÇİ ama S+ olmayan günler (aynı S6 bölge ailesi, aynı cetvel mekaniği) + bölge başına tek rastgele gün (K_SP_r, konum dengesi); kırılım kontrolü aynı bölge kutusu. Mekanik üstünlük: S+ kapanış dipte -> giriş t+1 açılış; kırılım tavanı t günü dahil kutu, t kapanışı tavanın altında (S6 AL tanımı) |
| K2 | geleceğe bakma | EVET | fitil pencereleri rolling (geriye); S6 durum makinesi sıralı (as-of t: bölge, sınıf = onay günü sınıfı, kutu t'ye kadar); kos fk_gelecek_denetimi her pazarda 40 olayda seriyi t'de kesip yeniden hesaplar, tutmazsa DURUR; kör sayfada t'den sonra bar çizilmez (test) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz barları (H>L, V>0, fiyat > 0); geçersiz bar sinyal / ölçü üretmez; DGXX kalibrasyonunda 16 Kas seans içi yarım bar atılır |
| K4 | tekilleştirme | EVET | cetvel oc_olay_hazirla aynı hissede 60 gün tekilleştirir (n bağımsız olay); kırılım cetvelin tekil olaylarında; kör sette aynı hisse bir kez; hücrede medyan da yazılır |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (cetvel); kırılım t+1 kapanışından itibaren; kör anahtarı sonucu da t+1 açılış |
| K6 | veri birimi | EVET | tek kip V_*.pkl düzeltilmiş fiyat (fi_k1_veri); fitil payları ve oransal eksen birimden bağımsız; DGXX ham (auto_adjust=False) yalnız kalibrasyon, fitil payı birim etkisiz |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (V_*; k34_yahoo yoksa ABD yalnız V_ABD); batanlar yok; raporda 'getiriler yukarı yanlı' notu; kırılımda AŞAĞI oranı aşağı yanlı okunur |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; iki yarı şartı (cetvel); varyantlar bilgi; kör set 30 + 10 küçük n: 'tanı', bulgu değil; olay sayımı bu ön kayıtta getirisiz |
| K9 | ön kayıt | EVET | FK_ESIK sha + FITIL_KOR.py sha + FO_ESIK sha + S6_PRM sha + cetvel üç sha + veri sha bu dosyada; iş tanımı koşudan önce git'e işlendi; kos / kor ik_kontrol_kapisi + oc_kapi + fk_onkayit_dogrula geçmezse durur; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV; kalibrasyon sayfalarında fitil payları ham bardan yazılır |
| K11 | yeniden üretim | EVET | olay satırları FK_SATIR klasöründe (olay_<satır>_<r>.csv.gz); >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | etiketler yalnız önceden yazılı kurallarla; 'iz / emare' sözü yalnız kural geçerse; sayı ve yorum ayrı cümle; 'al' / 'öneri' dili yok; kör PDF'te hisse / tarih / sonuç yok |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_fk; defter dosyaları ve mevcut .py modülleri yalnız import (git status); e-posta / anahtar taraması (ön kayıt, sonuç, rapor, anahtar); commit / push ana modelin |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tanı ölçümü (kapalı konu 'tek göstergeye göre alım' açılmaz) |

## Test

`python test_fitil_kor.py` (sentetik: taban içi tanımı, geleceğe bakma kesme, kırılım, fark bootstrap, kör sayfada ad / tarih / sonrası yok, yanıt ayrıştırma ve Fisher, kapı, e-posta / anahtar taraması).
