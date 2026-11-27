# DJ ÖN KAYIT — aynı seviyede doji öbekleri: doji sayısına göre sonrası (2026-11-27T06:46:21Z)

İş tanımı DJ_IS_TANIMI.md (ana model). Bu dosya R15 / U2 / D2 / çıkış / P15 HİÇBİR hücrede hesaplanmadan ÖNCE commit + push edilir; tanımlar, eşikler, okuma ve hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (yukarı yanlı). KASA açılmaz (veri <= 2022-12-31).

## Mühürler

DJ_KOD_SHA: 72d92ca7ffc6f7825f5b207526c4ed8aafafe48c01810da3e4f543dab827e27e
DJ_ESIK_SHA: 94ffcc2e0b8f94f45ca2f40f6d2c6588b57b4ced9fdd3ca702c6e9fbfed589ac
DOSYA_olay_ANA_ABD.pkl: aa9605ad56b83241fc6489ee69941c41b52a1cacac2c9a3d43d1dd39c96f0131
DOSYA_olay_D15_ABD.pkl: b1ebf125afa6f51ab4ce99e018b6dc17a25e29f10e9a8d17b3e701c9198abc12
DOSYA_olay_HAFTA_ABD.pkl: 42006f2c145961a8c894a897b64afd3e9532ec81b7c6dbe2cafdb8c9d9699e58
DOSYA_taban_ABD.pkl: 6b74da0891b0e50862a818bdd81c27b0d79aa3a658178fe07171eabfa415ef85
DOSYA_uygun_ABD.json: ea9399fafc4559dcc7188070f25915085a64553ada804f25f4253dc521dea09b
DOSYA_KAYNAK_ham_ABD.npz: 41f317fbd7e8928226215683444b4319f1e8301dbcc5ac549cd80c5b59ace234
DOSYA_olay_ANA_AVR.pkl: 6027583488e2f77c002adde5d7b77b220c17df73e45aecef4ad045e17f6da2d9
DOSYA_olay_D15_AVR.pkl: ca625786f4cb912f212078c8d8e68bdc36bc8ac12032759d4e0f86b861dd0b2c
DOSYA_olay_HAFTA_AVR.pkl: b78d69d75bfb129dd58dce87f75175b042d848bc7cb2bcaf8543da74cb03d159
DOSYA_taban_AVR.pkl: 10d74b607fe390408c87558779484d29897125c280342cd22fd164cc936e5e15
DOSYA_uygun_AVR.json: 202caa698c2f68df5281640c8c31d75ce143eec8895a4024b7f682936acb0584
DOSYA_KAYNAK_ham_AVR.npz: bf3dfcf27019a243c7281e069a04ec43c733bf8d915feb60e67021d2a6572c0b
SAYIM_SHA: b3baec55d151a01ec1893eda3a4a3840ab4b161a9fb4f662390c87d3113e8935
IS_TANIMI_SHA: d6e2f48695f4a8ca02800f38520a3d2b4b51421bdb34a6bd8599f8a888a8c0e1

- Olay / taban dosyaları (repo dışı): /root/.kasa/ham/doji_obek (olay_*: getirisiz; getiri_* ölçümde ayrı dosya)

## Eşik sözlüğü (DJ_ESIK; sha yukarıda)

```json
{
 "surum": "DJ-1.0",
 "tohum": 2712,
 "tohum_tanim": "np.random.default_rng([2712, crc32(anahtar)]); bootstrap anahtarı satır adı; PDF örnek seçimi anahtar 'ornek|k'",
 "veri": "YUKSELIS_ONCESI ham bar deposu ham_{pazar}.npz (O/H/L/C hissenin kendi geçerli barları: MUM_IZI.mi_veri H > L, V > 0, O/H/L/C sonlu > 0; POS = birleşik takvim satırı; Op / Cl / P2 = pazar paneli; KART_TUR2.k2_panel P2 evreni); sha YO_ON_KAYIT.md 'DOJSA_ham_*' ile aynı olmalı (DUR)",
 "doji": {
  "govde": 0.1,
  "govde_D15": 0.15,
  "boy_oran": 0.5,
  "ort_boy_bar": 10,
  "adim_pencere": 20,
  "adim_kat": 3,
  "tanim": "DOJİ(t) <=> |C - O| <= govde x (H - L) VE (H - L) >= 0,5 x ORT_BOY(t) VE (H - L) > 0 VE ölü değil; ORT_BOY(t) = t - 10 .. t - 1 barlarının (H - L) medyanı (10 önceki bar yoksa doji değil); ÖLÜ = (a) geçersiz bar (veride yok: H <= L, V = 0, kilitli; MI.mi_veri), (b) FİYAT ADIMINA YAPIŞMIŞ: (H - L) <= 3 x ADIM(t), ADIM(t) = t - 19 .. t barlarının O/H/L/C değerlerinin sıralı farklarının en küçük pozitifi (> 1e-9 x C_t; 20 bar yoksa bu süzgeç uygulanmaz, doji zaten ORT_BOY şartından düşer); ayrıca öbek içinde iki doji arası takvim satırı farkı > 6 ise (arada kilitli / işlemsiz günler) bağlanmaz"
 },
 "seviye": "SEVİYE(t) = (O_t + C_t) / 2",
 "obek": {
  "ara_en_cok": 3,
  "takvim_ara_en_cok": 6,
  "bant_atr": 0.5,
  "atr": "ATR20(t) = ATRP20(t) x C_t (YO.yo_hisse_ozellik ATRP20: son 20 barın TR ortalaması)",
  "tanim": "dojiler sırayla gezilir; yeni doji d, açık öbeğe katılır <=> d - son_doji <= 3 (kendi geçerli bar sırası; aralarında en çok 2 mum) VE POS(d) - POS(son_doji) <= 6 VE maks(seviye) - min(seviye) (öbekteki bütün dojiler + d) <= 0,5 x ATR20(d) (sınır DAHİL; göreli 1e-12 pay) VE ATR20(d) sonlu; katılmazsa açık öbek biter ve d yeni öbeği başlatır (k = 1); öbek bandı = öbekteki dojilerin maks H / min L"
 },
 "olay": {
  "tanim": "olay = öbeğin k'inci dojisinin barı t (yalnız t'ye kadarki bilgi); k = 1 (öbeği başlatan doji: o an ikincisi yok = TEK DOJİ tabanı), k = 2, k = 3, k = 4+ (= öbeğin 4. dojisi; 5. ve sonraki dojiler yeni olay üretmez: her satırda bir öbek bir kez)",
  "uygunluk": "YO.yo_ornek_maske kuralları HER BAR için (adım 5 yerine 1): t + 15 hissenin verisinde; POS(t + 1) - POS(t) <= 10; POS(t + 15) - POS(t + 1) <= 29; giriş satırında P2; giriş tarihi 2016-01-01 .. 2022-12-31; 15. bar <= 2022-12-31; ATRP20(t) sonlu > 0"
 },
 "taban": "HERHANGİ GÜN = YO.yo_ornek_maske örnek günleri (hissenin her 5. geçerli barı; aynı uygunluk); T1 ve 'aynı hissenin rastgele günü' karşılıkları (hisse x hücre ortalaması) bu günlerden; olayın kendi hücresindeki hisse ortalaması yoksa olay düşer (sayılır)",
 "baglam": {
  "konum": [
   0.3333333333333333,
   0.6666666666666666
  ],
  "onceki_bar": 10,
  "tanim": "KONUM120 (YO; son 120 kapanış aralığında konum) < 1/3 DİPTE, < 2/3 ORTADA, aksi TEPEDE; ÖNCEKİ YÖN = C_t / C_{t-10} - 1 < 0 DÜŞÜŞ, > 0 YÜKSELİŞ (= 0 ya da yok: ikisine de girmez)"
 },
 "sonuc": {
  "ufuk": 15,
  "hedef_atr": 2.0,
  "stop_atr": 1.0,
  "cikis_ufuk": 15,
  "devam": 10,
  "devam_satir": 19,
  "R15": "C_{t+15} / E0 - 1, E0 = O_{t+1} (giriş = sonraki geçerli bar açılışı)",
  "SECIM": "R15 - P15(d) (d = giriş satırı; YO.yo_P15: P2 hisselerinin eşit ağırlıklı 15 satır getirisi)",
  "TOPLAM_FARK": "R15 - T1(hisse, hücre)",
  "U2": "barlar t + 1 .. t + 15: ilk High >= E0 (1 + 2 ATRP20_t) barı, ilk Low <= E0 (1 - 1 ATRP20_t) barından ÖNCE (aynı bar = stop önce; YO.yo_ilk_dokunma)",
  "D2": "ayna: ilk Low <= E0 (1 - 2 ATRP20_t), ilk High >= E0 (1 + 1 ATRP20_t)'den önce",
  "ASIMETRI": "(U2 - D2) - (p_h - q_h); p_h / q_h = aynı hissenin aynı hücredeki örnek günlerinin U2 / D2 ortalaması",
  "BUYUKLUK": "|R15| / (ATRP20_t x karekök 15); BUYUKLUK_FARK = BUYUKLUK - h_h (aynı hissenin örnek günleri); KAT = toplam BUYUKLUK / toplam h_h",
  "CIKIS": "barlar t + 1 .. t + 15 içinde ilk KAPANIŞ > bant üstü (YUKARI) ya da < bant altı (AŞAĞI); hiçbiri yoksa HİÇ; çıkış barı e",
  "DEVAM": "R10 = C_{e+10} / O_{e+1} - 1; DEVAM = R10 x (+1 yukarı, -1 aşağı); e + 10 verinin dışında ya da POS(e + 10) - POS(e + 1) > 19 ise yok (sayılır); bilgi: T10 = aynı hissenin örnek günlerinde C_{t+10} / O_{t+1} - 1 ortalaması (sürüklenme)",
  "DONUS": "ÖNCEKİ YÖN DÜŞÜŞ: dönüş = R15 > 0; YÜKSELİŞ: dönüş = R15 < 0; taban = aynı hücrenin örnek günlerinde aynı önceki yöndeki dönüş payı (havuz); DONUS_FARK = dönüş - taban"
 },
 "boot": {
  "B": 10000,
  "kume": "giriş ayı (YYYY-AA)",
  "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık, tohum 2712); oran / ortalama her tekrarda ağırlıklı toplamlardan; %95 = 2,5 / 97,5 yüzdelik (YO._q); k farkları (k - 1) aynı ağırlıklarla (iki grup aynı ay kümeleri); iki yönlü p = 2 x min(#(<= 0), #(>= 0)) / B (en çok 1; (1 + #) / (B + 1) düzeltmeli)"
 },
 "bh": {
  "q": 0.1,
  "aile": "k (1, 2, 3, 4+) x ölçü (TOPLAM_FARK, SECIM, ASIMETRI, BUYUKLUK_FARK, DEVAM_YUKARI, DEVAM_ASAGI, DONUS_DUSUS, DONUS_YUKSELIS) = 32 satır; satır p'si = ABD 2016-19 ve ABD 2020-22 iki yönlü p'lerinin büyüğü"
 },
 "hukum": {
  "n_min": 1000,
  "n_az": 30,
  "ARTI": "ABD iki dönemde TOPLAM FARK > 0 ve alt > 0 VE AVR iki dönemde nokta > 0 VE BH geçer",
  "EKSI": "ABD iki dönemde üst < 0 VE AVR iki dönemde nokta < 0 VE BH geçer",
  "sira": "ARTI / EKSİ > 'ABD İKİ DÖNEM, AVR UYMADI' (ABD şartı var, AVR işareti uymuyor) > 'BH GEÇMEDİ' (ABD + AVR şartı var, BH yok) > ÇELİŞKİLİ (iki dönem zıt yönde ayrışıyor) > TEK DÖNEM (yalnız bir ABD döneminde aralık sıfırı dışlıyor) > AYRIŞMIYOR (iki dönemde aralık sıfırı içeriyor ve iki dönemde n >= 1.000) > ÖLÇÜLEMEDİ (aralık sıfırı içeriyor, bir ABD döneminde n < 1.000)",
  "olcu": "aynı kural bütün ölçülere uygulanır (TOPLAM_FARK ana; SECIM, ASIMETRI, BUYUKLUK_FARK, DONUS_FARK, DEVAM satırları)",
  "DOZ": "'DOJİ SAYISI ETKİLİ' <=> üç ölçüden (TOPLAM_FARK, BUYUKLUK_FARK, YUKARI_CIKIS payı) en az biri için: (a) k = 1 -> 2 -> 3 -> 4+ nokta değerleri ABD iki döneminde de tek yönlü (art arda farkların hepsi > 0 ya da hepsi < 0) ve iki dönemde aynı yönde, VE (b) (k = 3 - k = 1) ya da (k = 4+ - k = 1) farkının aralığı iki ABD döneminde de sıfırı dışlıyor ve işareti (a)'daki yönle aynı; aksi 'DOJİ SAYISI ETKİSİZ' (bu tanımla)",
  "CIKIS": "'ÇIKIŞ DEVAM EDİYOR' <=> DEVAM (yukarı çıkış ve aşağı çıkış ayrı satır) > 0 ve alt > 0 iki ABD döneminde; 'ÇIKIŞ TERSE DÖNÜYOR (tuzak)' <=> iki dönemde üst < 0; aksi genel sıra (TEK DÖNEM / AYRIŞMIYOR / ÖLÇÜLEMEDİ)",
  "GENEL": "ARTI ya da EKSİ olan k satırı ya da DOJİ SAYISI ETKİLİ varsa 'AÇIK VERİDE EMARE (kasa açılmaz; KASA KURALI)'; yoksa 'DOJİ ÖBEĞİ SONRASI AYIRT EDİCİ DEĞİL (bu tanımla)'"
 },
 "bilgi": {
  "D15": "gövde <= 0,15 boy (öteki her şey aynı); TOPLAM FARK k başına (bilgi, hüküm yok)",
  "HAFTA": "haftalık mumlar günlük geçerli barlardan (W-FRI haftası: O ilk, H maks, L min, C son); aynı doji / öbek kuralı (bar = hafta, ATR20 haftalık, takvim satırı = hafta sırası); giriş = sonraki hafta açılışı; R15 = 15 hafta; T1 = hissenin aynı hücredeki bütün uygun haftaları; giriş haftasının ilk günlük satırında P2; 15 hafta <= 29 hafta satırı; giriş 2016-2022, 15. hafta <= 2022-12-31; bilgi"
 },
 "ornek": {
  "k_basina": 4,
  "sayilmayan": 2,
  "once": 60,
  "yakin": 8,
  "tanim": "ANA olaylardan (iki pazar, iki dönem) k = 2 / 3 / 4+ için tohumla rastgele 4'er; sayılmayan 2 örnek: (a) önceki dojiyle arası <= 3 bar ama seviye farkı > 0,5 ATR20 (SEVİYE FARKLI), (b) seviye farkı <= 0,5 ATR20 ama arası 4-6 bar (ARA UZAK); grafik olay barında biter (sonrası yok), yüzde ekseni olay kapanışına göre; altta yakın görünüm (öbek + önceki 8 mum); hisse adı / tarih yok (pazar ve dönem yazılır)"
 },
 "kesik": "veri en büyük tarihi <= 2022-12-31 (assert; npz tarih)",
 "sira": "kod + sentetik test -> getirisiz sayım + DJ_ORNEKLER.pdf -> ön kayıt commit + push -> ik_kontrol_kapisi -> ölçüm (bir kez) -> rapor"
}
```

## GETİRİSİZ SAYIM (R15 hesaplanmadı)

| hücre | uygun hisse-gün | k | olay | bin hisse-günde | farklı ay | en kalabalık 3 ay payı | hisse |
|---|---|---|---|---|---|---|---|
| ABD|d1619 | 2003073 | k=1 (tek doji) | 172344 | 86,04 | 48 | 0,073 | 2677 |
| ABD|d1619 | 2003073 | k=2 | 31114 | 15,53 | 48 | 0,078 | 2492 |
| ABD|d1619 | 2003073 | k=3 | 4990 | 2,49 | 48 | 0,087 | 1984 |
| ABD|d1619 | 2003073 | k=4+ | 844 | 0,42 | 48 | 0,117 | 668 |
| ABD|d2022 | 1958918 | k=1 (tek doji) | 163184 | 83,30 | 36 | 0,098 | 3700 |
| ABD|d2022 | 1958918 | k=2 | 26473 | 13,51 | 36 | 0,107 | 3435 |
| ABD|d2022 | 1958918 | k=3 | 3651 | 1,86 | 36 | 0,116 | 2076 |
| ABD|d2022 | 1958918 | k=4+ | 532 | 0,27 | 36 | 0,147 | 475 |
| AVR|d1619 | 402902 | k=1 (tek doji) | 34025 | 84,45 | 48 | 0,072 | 474 |
| AVR|d1619 | 402902 | k=2 | 6027 | 14,96 | 48 | 0,084 | 453 |
| AVR|d1619 | 402902 | k=3 | 951 | 2,36 | 48 | 0,103 | 387 |
| AVR|d1619 | 402902 | k=4+ | 140 | 0,35 | 46 | 0,157 | 114 |
| AVR|d2022 | 325208 | k=1 (tek doji) | 26799 | 82,41 | 36 | 0,098 | 512 |
| AVR|d2022 | 325208 | k=2 | 4332 | 13,32 | 36 | 0,109 | 495 |
| AVR|d2022 | 325208 | k=3 | 607 | 1,87 | 36 | 0,119 | 342 |
| AVR|d2022 | 325208 | k=4+ | 58 | 0,18 | 29 | 0,155 | 53 |

Öbek son uzunluğu dağılımı (öbek sayısı; BİLGİ): ABD|d1619: {'1': 141191, '2': 26143, '3': 4162, '4': 721, '5': 110, '6+': 17}; ABD|d2022: {'1': 136655, '2': 22859, '3': 3138, '4': 446, '5': 72, '6+': 14}; AVR|d1619: {'1': 27984, '2': 5083, '3': 816, '4': 105, '5': 32, '6+': 5}; AVR|d2022: {'1': 22459, '2': 3723, '3': 558, '4': 51, '5': 8}

Yeni öbek başlatan dojilerin önceki dojiye bağlanmama nedeni: ABD|d1619: {'ARA_UZAK': 149817, 'SEVIYE_FARKLI': 22527}; ABD|d2022: {'ARA_UZAK': 141261, 'SEVIYE_FARKLI': 21921, 'TAKVIM': 1, 'ILK': 1}; AVR|d1619: {'ARA_UZAK': 29555, 'SEVIYE_FARKLI': 4470}; AVR|d2022: {'ARA_UZAK': 23382, 'SEVIYE_FARKLI': 3416, 'ILK': 1}

Taban günlerinde doji payı: ABD|d1619: 0,1058; ABD|d2022: 0,0985; AVR|d1619: 0,1018; AVR|d2022: 0,0981

D15 kolu olay sayıları: ABD|d1619: k=1 (tek doji) 236574, k=2 60532, k=3 13658, k=4+ 3029; ABD|d2022: k=1 (tek doji) 226391, k=2 52229, k=3 10246, k=4+ 1950; AVR|d1619: k=1 (tek doji) 46729, k=2 11509, k=3 2472, k=4+ 510; AVR|d2022: k=1 (tek doji) 37259, k=2 8583, k=3 1651, k=4+ 282

HAFTA kolu olay sayıları: ABD|d1619: taban 415645, k=1 (tek doji) 33228, k=2 5632, k=3 825, k=4+ 97; ABD|d2022: taban 370948, k=1 (tek doji) 29754, k=2 5139, k=3 831, k=4+ 119; AVR|d1619: taban 82909, k=1 (tek doji) 6485, k=2 1119, k=3 173, k=4+ 24; AVR|d2022: taban 60956, k=1 (tek doji) 4828, k=2 811, k=3 121, k=4+ 16

## Yorum noktaları (ölçümden önce)

1. Kaynak veri YUKSELIS_ONCESI'nin bar deposudur (ham_*.npz; YO ön kaydındaki sha ile aynı): evren, geçerli bar, P2 ve takvim YO ile birebir; yeni veri indirilmez.
2. ORT_BOY 'önceki 10 bar' = t - 10 .. t - 1 (t hariç) medyanı; ATR20 = YO ATRP20 x C_t (t dahil son 20 barın TR ortalaması): t barı kapanışında bilinir.
3. 'Ölü / fiyat adımına yapışmış' bar: geçersiz barlar veride hiç yok (MI.mi_veri); ayrıca (H - L) <= 3 x ADIM (son 20 barın en küçük fiyat farkı) olan bar doji sayılmaz (MUM_IZI_UC 'fiyat adımına yapışmış H = L' kuralının genişletilmiş hali; eşik önceden).
4. 'Aralarında en çok 2 mum' = kendi geçerli bar sırası farkı <= 3; ek olarak takvim satırı farkı <= 6 (arada kilitli / işlemsiz günler varsa bağlanmaz).
5. Bant genişliği her yeni dojide o dojinin ATR20'si ile denetlenir (öbek bütün seviyeleri + yeni seviye); sınır dahil.
6. Bir doji öbeğe katılmazsa YENİ öbeği başlatır (k = 1); öbek bir kez bittikten sonra eski öbeğe geri dönülmez.
7. k = 4+ satırı = öbeğin 4. dojisi (öbek başına bir olay); 5. ve sonraki dojiler olay üretmez. k = 1 satırı = öbeği başlatan her doji (o an ikincisi bilinmiyor).
8. Aynı öbek k = 1, 2, 3, 4 satırlarının her birine bir kez girer; k satırları ayrı ölçülür (bağımsız değil); k farkları aynı ay ağırlıklarıyla.
9. Olay uygunluğu YO örnek kuralının her bar sürümü (dj_uygun; 5. barlarda YO.yo_ornek_maske ile birebir, test); ATRP20 sonlu > 0.
10. HERHANGİ GÜN tabanı = YO örnek günleri (her 5. bar); T1 / p_h / q_h / h_h / T10 hisse x hücre ortalamaları; olayın hissesinin o hücrede taban günü yoksa olay düşer (sayısı rapora).
11. +2 ATR / -1 ATR eşikleri E0'a göre oran olarak: hedef = E0 (1 + 2 ATRP20_t), stop = E0 (1 - ATRP20_t); ayna simetrik; aynı bar = stop önce (YO kuralı).
12. Hareket büyüklüğü KAT = olayların toplam |R15| / (ATRP20 x karekök 15) / aynı hisselerin rastgele gün ortalamalarının toplamı; BUYUKLUK_FARK = fark ortalaması (hüküm ve BH bu satırda).
13. Çıkış: barlar t + 1 .. t + 15 kapanışları; bant = olay anındaki öbek bandı (k doji); aynı kapanış hem üstte hem altta olamaz; HİÇ = 15 barda çıkış yok.
14. Çıkış devamı R10 = C_{e+10} / O_{e+1} - 1, çıkış yönüyle çarpılır; e + 10 verinin dışında ya da 20 takvim satırını aşıyorsa yok (sayılır); kesik zaten veride.
15. Çıkış devamı sürüklenmeden arındırılmış hali (DEVAM - yön x T10) BİLGİ satırıdır; hüküm iş tanımındaki ham devamla (> 0, alt > 0).
16. Önceki yön C_t / C_{t-10} - 1 işaretiyle; dönüş tabanı aynı hücrenin taban günlerinde aynı önceki yönün dönüş payı (havuz; hisseye göre değil).
17. Hüküm sırası ve BH ailesi DJ_ESIK['hukum'] / ['bh']: ARTI / EKSİ yalnız BH geçerse; aksi 'BH GEÇMEDİ'. AVR işareti iki AVR döneminde de.
18. DOZ kuralında 'tek yönlü' = k = 1 -> 2 -> 3 -> 4+ art arda üç farkın hepsi aynı işaretli (eşit = tek yönlü değil), iki ABD döneminde aynı yönde.
19. Bağlam (DİPTE / ORTADA / TEPEDE) ve D15, HAFTA kolları yalnız BİLGİ; hükmü değiştirmez; KONUM120 yoksa (120 bar yok) bağlam satırına girmez.
20. Haftalık kol: mumlar günlük geçerli barlardan; giriş haftasının ilk günlük satırında P2; haftalar arası boşluk (giriş) <= 2 hafta, 15 hafta <= 29 hafta satırı.
21. Evren bugün yaşayan hisseler: sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer.
22. Ölçüm bir kez koşar; getiri dosyası varsa kapı durur. Sonuçtan sonra yalnız gösterim değişebilir; aksi SAPMA.
23. Getirisiz sayım: k = 4+ ABD iki döneminde n < 1.000 (844 / 532): bu satırda aralık sıfırı içerirse hüküm ÖLÇÜLEMEDİ olur (iddia kapanmaz); AVR k = 4+ n 140 / 58 (bilgi; işaret yine okunur, n < 30 değil). DOZ kuralı k = 4+ nokta değerini n'ye bakmadan kullanır (kural önceden böyle).
24. Düşen (tabansız) olay sayısı ve DEVAM'ı ölçülemeyen çıkışlar rapora yazılır; dışlanır, yerine konmaz.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hissenin aynı hücredeki rastgele (her 5. bar) günleri: TOPLAM FARK = R15 - T1, U2 / D2 / büyüklük için p_h / q_h / h_h aynı hisseden; ATR ölçekli eşikler (oynaklığın mekanik etkisi ATRP20 ile ölçeklenir); D2 aynası ve asimetri mekanik üstünlüğü ölçer; tek doji (k = 1) ve herhangi gün iki taban; k farkları aynı ay ağırlıklarıyla; SEÇİM = R15 - PİYASA(t) |
| K2 | geleceğe bakma | EVET | doji / öbek / k t barına kadarki barlarla (test: t + 1 ve sonrası bozulunca olaylar aynı); ORT_BOY t - 10 .. t - 1; ATR20 ve ADIM t'ye kadar; sonuç sütunları ayrı fonksiyonda, yalnız kapıdan sonra; olay dosyası ile getiri dosyası ayrı; öbeğin son uzunluğu yalnız sayımda (bilgi); veri <= 2022-12-31 assert |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli barları (H > L, V > 0, O/H/L/C sonlu > 0); ölü / fiyat adımına yapışmış bar doji sayılmaz (ADIM kuralı, test); öbekte takvim satırı farkı > 6 bağlanmaz; 15 bar <= 30 takvim satırı; giriş P2 evreninde |
| K4 | tekilleştirme | EVET | öbek başına her k satırında bir olay (4+ = 4. doji; sonrakiler olay değil); olaylar örtüşebilir, çıkarım ay kümeli bootstrap; n ve farklı ay ayrı yazılır; medyan R15 yazılır; taban her 5. bar |
| K5 | giriş fiyatı | EVET | giriş = t + 1 barının açılışı; çıkış devamı çıkış barından sonraki açılıştan (e + 1); P15 de giriş satırından |
| K6 | veri birimi | EVET | OS / MI bölünme düzeltmeli açık kopya (YO ile aynı depo); getiriler oransal, yerel para; pazar içi karşılaştırma; eşikler ATR oranlı (birimden bağımsız); fiyat adımı kuralı birimden bağımsız (kendi fiyat farklarından) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler (hayatta kalma yanlılığı): sonuç yukarı yanlı; TOPLAM FARK aynı hisseye göre olduğu için yanlılık kısmen düşer; raporda yazılır; kasa açılmaz |
| K8 | örneklem ve dönem | EVET | n >= 1.000 değilse ÖLÇÜLEMEDİ (n < 30 'örneklem yetersiz'); iki ABD dönemi + iki AVR dönemi; BH q 0,10 (32 satır aile); en kalabalık 3 ay payı her satırda |
| K9 | ön kayıt | EVET | DJ_ON_KAYIT.md: DJ_KOD_SHA, DJ_ESIK_SHA, olay / taban dosya sha'ları, SAYIM_SHA, yorum noktaları; ölçüm kapısı: kontrol + sha + ön kayıt commit + push + kod temiz; getiri dosyası varsa ikinci koşu DURUR; eşikler sonuca göre değişmez |
| K10 | ayrıştırma | EVET | doji / öbek kuralı sentetik pozitif / negatif serilerle (yakalama >= %95, yanlış kabul <= %5); uygunluk maskesi YO.yo_ornek_maske ile 5. barlarda birebir; dokunma YO.yo_ilk_dokunma; kaynak npz sha YO ön kaydıyla aynı; PDF'te gerçek örnekler gözle denetlenir |
| K11 | yeniden üretim | EVET | rapordan önce >= 3 satır olay + getiri dosyalarından bağımsız kısa kodla yeniden üretilir; rapordaki sayılar dj_sonuc.json'dan basılır |
| K12 | ifade | EVET | 'emare / etkili' sözü yalnız hüküm kuralıyla; ABD tek dönem 'TEK DÖNEM'; sayı ile yorum ayrı cümlede; evren bugün yaşayanlar; fiyat değişimi gerçek kâr değil (komisyon / kayma yok) |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_dj); mevcut modüller ve defter dosyaları değişmez (yalnız import; SEKIL_DEVAM / WEB_DESEN içe alınmaz); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(yok; ölçümden sonra doldurulur)
