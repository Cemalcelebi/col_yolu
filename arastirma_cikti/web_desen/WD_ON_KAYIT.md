# WD_ON_KAYIT — web desenleri: gerçek veride sonrası ölçümünden ÖNCE (2026-11-27 06:19)

Sürüm: WEB_DESEN v1.0 (2026-11-27): web desenleri, yapay sınama + gerçek veride sonrası. İş tanımı: WD_IS_TANIMI.md. Sonuç dosyası (wd_sonuc.json) bu ön kayıt commit + push edilmeden üretilmez (kapı).

## Mühürler
WD_KOD_SHA: d0489c44f59a393349d1e7ea791e5ebace699170278200d84777fb5eea9b850f
WD_ESIK_SHA: 19f51f2d5732ecce895b71719ed09ea4f592d25c46d958048b147dce2e7ebe14
DOSYA_olay_ABD.pkl: b75285eec29a4dcf590eeba5f6e9ea262dce09ba0d69d6f0f91cbb3419f040a1
DOSYA_YO_ham_ABD.npz: 41f317fbd7e8928226215683444b4319f1e8301dbcc5ac549cd80c5b59ace234
DOSYA_YO_ozellik_ABD.pkl: 9e470d0658ccca89c17edc320b250397ce3d5f3c265e52dd831767cc46d84ca8
DOSYA_olay_AVR.pkl: d374781cdad50e2538aaf1db691103b245993ebeddc6634dbe2daea0ca9a05c2
DOSYA_YO_ham_AVR.npz: bf3dfcf27019a243c7281e069a04ec43c733bf8d915feb60e67021d2a6572c0b
DOSYA_YO_ozellik_AVR.pkl: daa33b4c6ba06dee2f1c300a1797f4a7e9d9e4ab113a865240d56fd44393e09f
SAYIM_SHA: 91a8cf2c2bdf3e04a872d6fd09acc964f67b91425199fd8aeeaa82db8f9a5f08
SENTETIK_SHA: 3c906ea9739ab7b2e600f473e1df1846d2702613d4d30e68598c600c158516ce

## Eşik sözlüğü (WD_ESIK, sabit)
```json
{
 "surum": "WD-1.0",
 "ortak": {
  "ort_boy": 10,
  "atr": 20,
  "uc_pencere": 20,
  "uc_yas": 4,
  "uc_yas_w3": 3,
  "baglam": 10,
  "tanim": "boy = H - L; gövde = |C - O|; üst fitil = H - max(O, C); alt fitil = min(O, C) - L; ORT_BOY(i) = i'den önceki 10 barın boy medyanı (desenin İLK barının ORT_BOY'u bütün desen mumları için); ATR(i) = TR'nin (önceki kapanışla; ilk bar H - L) i dahil 20 bar ortalaması (YO ATRP20 x C); PL(i) / PH(i) = i'den önceki 20 barın (i-20 .. i-1) en düşük L / en yüksek H'si; YAŞ = i - (bu ucun SON görüldüğü bar); YAŞ < 4 ise (W3'te < 3) PL / PH yok sayılır (olay yok); DÜŞÜŞ bağlamı(ilk) = C[ilk-1] < C[ilk-11]; YÜKSELİŞ = C[ilk-1] > C[ilk-11]; yerel dip i: L_i < L_{i-1}, L_i < L_{i-2}, L_i <= L_{i+1}, L_i <= L_{i+2} (YO YUKSELEN_DIP tanımı); yerel tepe aynası; yerel uç yalnız i + 2 barı tamamlandıktan sonra kullanılır"
 },
 "W1": {
  "tepe_pay": 0.25,
  "tanim": "art arda 3 yeşil (C > O) mum a, b, c; her birinin boyu > ORT_BOY(a); C_a < C_b < C_c; her mumda H - C <= 0,25 x boy; O_b ∈ [O_a, C_a] ve O_c ∈ [O_b, C_b] (sınır dahil); DÜŞÜŞ(a). Giriş c'den sonraki açılış; stop L_a. W1T aynası (kırmızı, C - L <= 0,25 boy, kapanışlar düşen, açılış önceki gövde içinde, YÜKSELİŞ(a), stop H_a)"
 },
 "W2": {
  "fitil_pay": 0.5,
  "stop_atr": 0.1,
  "tanim": "L_t < PL_t ve C_t > PL_t ve alt fitil >= 0,5 x boy (YAŞ >= 4). Giriş t + 1 açılış; stop L_t - 0,1 ATR_t. W2T aynası (stop H_t + 0,1 ATR_t)"
 },
 "W2E": {
  "atr_pay": 0.25,
  "ara_fark": 4,
  "tanim": "W2 + t'den önceki 20 barda (t-20 .. t-1; i + 2 <= t - 1) |L_i - PL_t| <= 0,25 ATR_t olan yerel dipler içinde indeks farkı >= 4 ('aralarında en az 3 bar') olan en az iki dip. W2TE aynası"
 },
 "W3": {
  "tik": 0.999,
  "tanim": "t: C_t <= PL_t (YAŞ >= 3); t + 1: H_{t+1} >= PL_t ise giriş = O_{t+1} >= PL_t ise O_{t+1}, değilse PL_t; ulaşmazsa olay yok (girişsiz aday). Stop = min(L_t, L_{t+1}) x 0,999. W3T aynası (C_t >= PH_t; L_{t+1} <= PH_t; giriş O_{t+1} <= PH ise açılış, değilse PH; stop max(H_t, H_{t+1}) x 1,001)"
 },
 "W4": {
  "bos_bar": 10,
  "test_bar": 5,
  "tanim": "W2T olayı s; seviye = s'den önce tamamlanmış son yerel dibin L'si (i + 2 <= s - 1); yapı kırılımı b = s+1 .. s+10 içinde ilk C_b < seviye; giriş e = b+1 .. b+5 içinde ilk H_e >= seviye: giriş = O_e >= seviye ise O_e (açılış seviyeyi geçmiş), değilse seviye (satış). Stop H_s. W4Y aynası (W2 olayı, son yerel tepe H'si, C_b > seviye, L_e <= seviye, giriş O_e <= seviye ise O_e değilse seviye, stop L_s)"
 },
 "W5": {
  "geri_bar": 3,
  "tanim": "t: C_t > PH_t (YAŞ >= 4); u = t+1 .. t+3 içinde ilk C_u < PH_t; giriş u + 1 açılışında satış; stop = max(H_t .. H_u). W5Y aynası (C_t < PL_t, C_u > PL_t, alış, stop min(L_t .. L_u))"
 },
 "W6": {
  "alt_govde": 2.0,
  "ust_pay": 0.1,
  "boy_ort": 0.8,
  "dip_bar": 10,
  "tanim": "alt fitil >= 2 x gövde; üst fitil <= 0,1 x boy; boy >= 0,8 x ORT_BOY(t); L_t = min(L_{t-9..t}); DÜŞÜŞ(t). Giriş t + 1 açılış; stop L_t. W6T aynası (üst fitil >= 2 x gövde; alt fitil <= 0,1 boy; H_t = max(H_{t-9..t}); YÜKSELİŞ(t); stop H_t)"
 },
 "W7": {
  "hacim_kat": 2.0,
  "hacim_pencere": 20,
  "kapanis_pay": 0.5,
  "dip_bar": 20,
  "tanim": "DÜŞÜŞ(t); L_t = min(L_{t-19..t}); V_t >= 2 x medyan(V_{t-20..t-1}); (C - L) / boy >= 0,5. Giriş t + 1 açılış; stop L_t. W7D: ayrıca boy <= ORT_BOY(t). W7T: YÜKSELİŞ(t); H_t = max(H_{t-19..t}); aynı hacim şartı; (C - L) / boy <= 0,5; stop H_t"
 },
 "filtre": {
  "sira": [
   "GIRIS_YOK",
   "STOP_TERS",
   "BOSLUK",
   "UFUK_KESIK",
   "DONEM_DISI",
   "EVREN_DISI",
   "KILITLI",
   "T1_YOK",
   "TEKIL"
  ],
  "giris_bosluk": 10,
  "pencere_satir": 30,
  "kilitli_pay": 0.2,
  "tekil_bar": 5,
  "t1_en_az": 30,
  "tanim": "GIRIS_YOK: giriş barı veride yok; STOP_TERS: giriş stopun yanlış tarafında ya da R = 0; BOSLUK: giriş barı satırı - sinyal barı satırı > 10 birleşik takvim satırı; UFUK_KESIK: e + 14 barı yok, tarihi > 2022-12-31 ya da e .. e+14 > 30 takvim satırı; DONEM_DISI: giriş 2016-01-01 .. 2022-12-31 dışında; EVREN_DISI: giriş satırında P2 değil (YO evreni); KILITLI: desenin ilk barı .. giriş barı takvim aralığında ham veride geçersiz bar payı (MUM_IZI_UC.uc_kilitli_pay) > 0,20; T1_YOK: aynı hisse aynı hücrede YO örnek günü < 30; TEKIL: aynı hisse aynı kolda önceki tutulan olayın giriş barından < 5 bar sonra giriş"
 },
 "olcu": {
  "ufuk": 15,
  "atr_hedef": 2.0,
  "atr_stop": 1.0,
  "R_hedef": 2.0,
  "yon_bar": 10,
  "tanim": "barlar e .. e+14 (giriş barı dahil; YO gibi); R15 = C[e+14] / giriş - 1; TOPLAM FARK = yön x (R15 - T1), T1 = aynı hissenin aynı hücredeki YO örnek günlerinin (k % 5 == 0, P2) R15 ortalaması (giriş O[k+1], C[k+15]); SEÇİM = yön x (R15 - P15(e satırı)) (YO.yo_P15); ATR HEDEFİ = yönde giriş ± 2 x ATR(e-1)'e ters yönde 1 x ATR(e-1) görmeden ulaşma (aynı barda ikisi = STOP ÖNCE); taban = aynı hissenin aynı hücredeki örnek günlerinde (giriş O[k+1], ATR(k)) aynı yöndeki pay; KAT = Σ isabet / Σ taban(hisse-hücre); KAYNAK STOPU: R = |giriş - stop|, hedef giriş ± 2R, stop seviyesi; aynı bar = stop önce; taban = aynı hissenin aynı hücredeki örnek günlerinde aynı R / giriş oranıyla pay; R KATI = yön x (çıkış - giriş) / R, çıkış = stopa ilk dokunulan bar (e'den sonraki barda açılış stopun ötesindeyse açılış) yoksa C[e+14]; 10 GÜN YÖN (bilgi) = yön x (C[e+9] - giriş) > 0; taban aynı hissenin örnek günlerinde C[k+10] / O[k+1] - 1 yönde"
 },
 "boot": {
  "B": 10000,
  "tohum": 2711,
  "kume": "giriş ayı (YYYY-AA)",
  "tanim": "ay kümeli bootstrap: aylar yerine koyarak (multinomial ağırlık, kol x hücre başına bir W; np.random.default_rng([2711, crc32(kol|hücre)])); ortalama ve KAT her tekrarda ağırlıklı toplamlardan; %95 = 2,5 / 97,5 yüzdelik; T1 / taban sabit",
  "p": "tek yönlü p = (1 + #(istatistik* <= sıfır noktası)) / (B + 1); sıfır noktası TOPLAM FARK'ta 0, KAT'ta 1"
 },
 "bh": {
  "q": 0.1,
  "aile": "17 desen kolu; kol p'si = max(p_TF ABD 2016-19, p_TF ABD 2020-22, p_KAT ABD 2016-19, p_KAT ABD 2020-22) (kesişim-birleşim)"
 },
 "hukum": {
  "n_min": 300,
  "ay_min": 12,
  "avr_n": 100,
  "sira": "ÖLÇÜLEMEDİ (ABD hücrelerinden birinde n < 300 ya da farklı ay < 12) > TUTAR > TERS > TEK DÖNEM > TUTMADI",
  "TUTAR": "ABD 2016-19 ve 2020-22'de TOPLAM FARK > 0 ve alt > 0 VE ATR KAT > 1 ve alt > 1 VE AVR iki dönemde (n >= 100 olan hücrelerde) TOPLAM FARK nokta değeri > 0 VE BH (q 0,10) geçer",
  "TERS": "ABD iki dönemde de TOPLAM FARK üst ucu < 0",
  "TEK_DONEM": "ABD şartları (TF ve KAT alt uçları) yalnız bir dönemde",
  "TUTMADI": "ötekiler (ABD iki dönemde geçip AVR / BH'de kalan dahil)",
  "avr_not": "AVR hücresi n < 100 ise o hücre şartı aranmaz ve 'AVR n < 100' notu yazılır"
 },
 "sentetik": {
  "olcek": [
   5.0,
   50.0,
   500.0
  ],
  "oyn": [
   0.004,
   0.008
  ],
  "tohum_sayi": 25,
  "gurultu": [
   0.0,
   0.1,
   0.2
  ],
  "hedef_yakala": 0.9,
  "hedef_kabul": 0.05,
  "rastgele": {
   "seri": 200,
   "uzunluk": 300
  },
  "tanim": "pozitif: desen şeması gibi kurulmuş yapay mumlar rastgele yürüyüşe gömülü; gürültü = desen barlarının O/H/L/C'sine N(0, g x boy) (sonra H = max, L = min); yakalama = beklenen giriş barında o kolun olayı; negatif (yakın ama değil): desen bölgesinde (ilk bar .. beklenen giriş + 2) o kolun herhangi bir olayı = yanlış kabul; rastgele seri: 1000 barda olay sıklığı (gerçek veriyle yan yana)"
 },
 "kesik": "veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi her pazar) + KASA.kasa_kapisi(V_ABD.pkl, V_AVR.pkl, '2022-12-31')",
 "sira": "kod + sentetik + yapay PDF -> getirisiz sayım -> ön kayıt commit + push -> ik_kontrol_kapisi -> ölçüm (bir kez) -> rapor + gerçek örnek PDF"
}
```

## SENTETİK (yapay pozitif / negatif; gerçek veri görülmeden)

| kol | yakalama %0 | %10 | %20 | yanlış kabul en çok (%0) | en çok (her gürültü) | negatif tipleri (%0 kabul) | rastgele 1000 barda | hedef |
|---|---|---|---|---|---|---|---|---|
| W1 | 100 | 80 | 40 | 0 | 8 | bosluk: 0; fitil: 0; yukselis: 0 | 0,83 | TUTTU |
| W1T | 100 | 80 | 36 | 0 | 12 | bosluk: 0; fitil: 0; yukselis: 0 | 0,77 | TUTTU |
| W2 | 100 | 96 | 64 | 0 | 4 | kapanis_disari: 0; kisa_fitil: 0 | 3,12 | TUTTU |
| W2T | 100 | 88 | 68 | 0 | 4 | kapanis_disari: 0; kisa_fitil: 0 | 3,23 | TUTTU |
| W2E | 100 | 92 | 72 | 0 | 0 | esit_degil: 0; tek_dip: 0 | 0,57 | TUTTU |
| W2TE | 100 | 76 | 64 | 0 | 0 | esit_degil: 0; tek_dip: 0 | 0,53 | TUTTU |
| W3 | 100 | 92 | 68 | 0 | 28 | ulasmadi: 0; fitil_kapanis: 0 | 12,43 | TUTTU |
| W3T | 100 | 100 | 76 | 0 | 40 | ulasmadi: 0; fitil_kapanis: 0 | 11,42 | TUTTU |
| W4 | 100 | 84 | 52 | 2 | 38 | bos_yok: 2; gercek_kirilim: 0 | 0,65 | TUTTU |
| W4Y | 100 | 88 | 80 | 2 | 46 | bos_yok: 0; gercek_kirilim: 2 | 0,47 | TUTTU |
| W5 | 100 | 96 | 88 | 0 | 48 | gercek_kirilim: 0; sadece_fitil: 0 | 7,63 | TUTTU |
| W5Y | 100 | 100 | 76 | 0 | 40 | gercek_kirilim: 0; sadece_fitil: 0 | 8,48 | TUTTU |
| W6 | 100 | 76 | 48 | 0 | 8 | yukselis: 0; ust_fitil: 0 | 1,60 | TUTTU |
| W6T | 100 | 80 | 44 | 0 | 8 | yukselis: 0; ust_fitil: 0 | 1,88 | TUTTU |
| W7 | 100 | 72 | 56 | 0 | 4 | dipte_kapanis: 0; dusuk_hacim: 0 | 0,23 | TUTTU |
| W7D | 100 | 84 | 48 | 0 | 0 | genis: 0; dipte_kapanis: 0 | 0,08 | TUTTU |
| W7T | 100 | 72 | 64 | 0 | 8 | dipte_kapanis: 0; dusuk_hacim: 0 | 0,12 | TUTTU |

## GETİRİSİZ SAYIM (filtre + tekil sonrası olay; n / farklı ay / en kalabalık 3 ay payı)

| kol | yön | ABD 2016-19 | ABD 2020-22 | AVR 2016-19 | AVR 2020-22 | 1000 barda ham (ABD / AVR) | rastgele seri 1000 barda |
|---|---|---|---|---|---|---|---|
| W1 | + | 509 / 47 / 15 | 560 / 36 / 37 | 113 / 38 / 20 | 97 / 28 / 26 | 0,30 / 0,30 | 0,83 |
| W1T | - | 919 / 47 / 18 | 807 / 35 / 32 | 229 / 44 / 24 | 166 / 35 / 21 | 0,46 / 0,59 | 0,77 |
| W2 | + | 9422 / 48 / 11 | 10498 / 36 / 19 | 2080 / 48 / 12 | 1688 / 36 / 15 | 5,55 / 5,44 | 3,12 |
| W2T | - | 11859 / 48 / 9 | 11055 / 36 / 12 | 2617 / 48 / 11 | 1863 / 36 / 13 | 6,00 / 6,20 | 3,23 |
| W2E | + | 1697 / 48 / 12 | 1707 / 36 / 15 | 367 / 47 / 15 | 309 / 35 / 16 | 1,09 / 1,03 | 0,57 |
| W2TE | - | 2259 / 48 / 10 | 1926 / 36 / 14 | 485 / 48 / 14 | 369 / 36 / 17 | 1,14 / 1,27 | 0,53 |
| W3 | + | 19603 / 48 / 16 | 21065 / 36 / 16 | 4101 / 48 / 14 | 3662 / 36 / 19 | 11,41 / 11,18 | 12,43 |
| W3T | - | 26681 / 48 / 10 | 23622 / 36 / 13 | 5529 / 48 / 9 | 4034 / 36 / 14 | 12,45 / 13,41 | 11,42 |
| W4 | - | 2131 / 48 / 11 | 1987 / 36 / 16 | 496 / 48 / 11 | 361 / 34 / 17 | 1,08 / 1,15 | 0,65 |
| W4Y | + | 1949 / 48 / 12 | 1987 / 36 / 17 | 445 / 46 / 11 | 331 / 34 / 20 | 1,03 / 1,10 | 0,47 |
| W5 | - | 18062 / 48 / 10 | 17027 / 36 / 13 | 3672 / 48 / 10 | 2789 / 36 / 14 | 8,39 / 8,67 | 7,63 |
| W5Y | + | 14058 / 48 / 14 | 15043 / 36 / 16 | 2989 / 48 / 12 | 2573 / 36 / 16 | 7,33 / 7,78 | 8,48 |
| W6 | + | 8149 / 48 / 12 | 9422 / 36 / 27 | 1817 / 48 / 13 | 1625 / 36 / 20 | 5,69 / 5,31 | 1,60 |
| W6T | - | 9240 / 48 / 10 | 9316 / 36 / 13 | 2174 / 48 / 10 | 1629 / 36 / 14 | 5,52 / 5,93 | 1,88 |
| W7 | + | 9708 / 48 / 17 | 10789 / 36 / 30 | 1863 / 48 / 20 | 1988 / 36 / 33 | 7,87 / 6,50 | 0,23 |
| W7D | + | 1535 / 48 / 15 | 2145 / 36 / 27 | 253 / 47 / 18 | 349 / 35 / 29 | 1,56 / 1,14 | 0,08 |
| W7T | - | 11068 / 48 / 11 | 10538 / 36 / 17 | 1842 / 48 / 10 | 1333 / 36 / 17 | 8,59 / 6,00 | 0,12 |

### Filtre atmaları (ham aday -> atılan; sıra WD_ESIK filtre)

| pazar | kol | ham aday | GIRIS_YOK | STOP_TERS | BOSLUK | UFUK_KESIK | DONEM_DISI | EVREN_DISI | KILITLI | T1_YOK | TEKIL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ABD | W1 | 1987 | 3 | 6 | 2 | 24 | 251 | 577 | 0 | 14 | 41 |
| ABD | W1T | 3025 | 0 | 13 | 1 | 42 | 212 | 910 | 0 | 42 | 79 |
| ABD | W2 | 36824 | 51 | 836 | 14 | 730 | 3595 | 11203 | 1 | 307 | 167 |
| ABD | W2T | 39830 | 10 | 896 | 7 | 429 | 3117 | 11966 | 4 | 282 | 205 |
| ABD | W2E | 7257 | 9 | 158 | 1 | 175 | 738 | 2701 | 0 | 56 | 15 |
| ABD | W2TE | 7583 | 1 | 175 | 3 | 82 | 677 | 2402 | 2 | 40 | 16 |
| ABD | W3 | 75682 | 0 | 0 | 0 | 1750 | 7074 | 23959 | 3 | 770 | 1458 |
| ABD | W3T | 82590 | 0 | 0 | 0 | 1306 | 7437 | 21179 | 6 | 518 | 1841 |
| ABD | W4 | 7159 | 0 | 26 | 0 | 119 | 619 | 2181 | 1 | 61 | 34 |
| ABD | W4Y | 6804 | 0 | 30 | 0 | 85 | 651 | 2030 | 0 | 38 | 34 |
| ABD | W5 | 55669 | 13 | 1079 | 34 | 786 | 4963 | 12948 | 3 | 375 | 379 |
| ABD | W5Y | 48644 | 25 | 844 | 23 | 966 | 4679 | 12294 | 2 | 422 | 288 |
| ABD | W6 | 37715 | 25 | 1586 | 34 | 990 | 3759 | 12808 | 4 | 337 | 601 |
| ABD | W6T | 36642 | 13 | 1251 | 16 | 698 | 2611 | 12573 | 4 | 278 | 642 |
| ABD | W7 | 52229 | 60 | 2403 | 37 | 1835 | 5031 | 20253 | 4 | 380 | 1729 |
| ABD | W7D | 10350 | 19 | 1009 | 15 | 630 | 779 | 3962 | 1 | 92 | 163 |
| ABD | W7T | 56960 | 22 | 2533 | 37 | 1101 | 3994 | 25108 | 3 | 600 | 1956 |
| AVR | W1 | 324 | 0 | 2 | 0 | 2 | 22 | 76 | 0 | 0 | 12 |
| AVR | W1T | 629 | 0 | 1 | 0 | 1 | 63 | 137 | 0 | 7 | 25 |
| AVR | W2 | 5823 | 1 | 153 | 0 | 68 | 572 | 1215 | 2 | 15 | 29 |
| AVR | W2T | 6638 | 1 | 167 | 0 | 48 | 598 | 1262 | 5 | 30 | 47 |
| AVR | W2E | 1108 | 0 | 27 | 0 | 12 | 93 | 296 | 0 | 2 | 2 |
| AVR | W2TE | 1358 | 0 | 30 | 0 | 10 | 116 | 339 | 0 | 5 | 4 |
| AVR | W3 | 11978 | 0 | 0 | 0 | 131 | 1234 | 2491 | 3 | 49 | 307 |
| AVR | W3T | 14362 | 0 | 0 | 0 | 78 | 1539 | 2749 | 11 | 72 | 350 |
| AVR | W4 | 1232 | 0 | 3 | 0 | 16 | 126 | 218 | 0 | 7 | 5 |
| AVR | W4Y | 1175 | 0 | 4 | 0 | 7 | 111 | 265 | 0 | 4 | 8 |
| AVR | W5 | 9286 | 1 | 225 | 1 | 49 | 939 | 1490 | 13 | 38 | 69 |
| AVR | W5Y | 8336 | 0 | 161 | 0 | 120 | 959 | 1435 | 4 | 28 | 67 |
| AVR | W6 | 5693 | 0 | 205 | 0 | 65 | 619 | 1216 | 2 | 30 | 114 |
| AVR | W6T | 6350 | 2 | 272 | 0 | 38 | 613 | 1460 | 3 | 34 | 125 |
| AVR | W7 | 6959 | 0 | 269 | 0 | 108 | 624 | 1768 | 4 | 30 | 305 |
| AVR | W7D | 1216 | 0 | 112 | 0 | 35 | 78 | 367 | 1 | 4 | 17 |
| AVR | W7T | 6430 | 0 | 378 | 1 | 37 | 598 | 2035 | 4 | 40 | 162 |

### Girişi gerçekleşmeyen adaylar (W3 / W4 / W5; tarama aşamasında, tarih / evren filtresinden önce)

- ABD W3: {"girissiz": 50905, "veri_sonu": 21}
- ABD W3T: {"girissiz": 61140, "veri_sonu": 41}
- ABD W4: {"bos_yok": 30346, "test_yok": 2227, "veri_sonu": 97, "seviye_yok": 1}
- ABD W4Y: {"bos_yok": 27409, "test_yok": 2229, "veri_sonu": 381, "seviye_yok": 1}
- ABD W5: {"girissiz": 60262, "veri_sonu": 84}
- ABD W5Y: {"girissiz": 52238, "veri_sonu": 66}
- AVR W3: {"girissiz": 8039, "veri_sonu": 6}
- AVR W3T: {"girissiz": 10325}
- AVR W4: {"bos_yok": 5033, "test_yok": 354, "veri_sonu": 19}
- AVR W4Y: {"bos_yok": 4175, "test_yok": 438, "veri_sonu": 35}
- AVR W5: {"girissiz": 10686, "veri_sonu": 8}
- AVR W5Y: {"girissiz": 8328, "veri_sonu": 8}

## Yorum noktaları (ölçümden ÖNCE sabit)

1. PL / PH YAŞI: 'uç en az 4 seans eski' = önceki 20 barın en düşüğünün (eşitlerde SON görüldüğü bar) indeksi t - 4 ya da daha eski; değilse o bar için PL yok sayılır (olay yok). W3'te 3.
2. ORT_BOY: desenin İLK barından önceki 10 barın boy medyanı; üç mumlu desende üç mum da aynı ORT_BOY ile karşılaştırılır (desen mumları kendi eşiğini şişirmez).
3. BAĞLAM: DÜŞÜŞ = C[ilk-1] < C[ilk-11] (iş tanımı 'desenin ilk barından önceki kapanış, ondan 10 bar önceki kapanışın altında'); W6 / W7'de ilk = t.
4. W1 'açılış önceki gövde içinde': O_b ∈ [O_a, C_a], O_c ∈ [O_b, C_b] (sınır dahil). 'Kapanışlar yükselen' kesin (<).
5. W2E 'aralarında en az 3 bar' = iki dip indeks farkı >= 4; yerel dip i + 2 <= t - 1 (süpürme barından önce tamamlanmış); tolerans ATR_t ile.
6. W3 'ulaşırsa giriş' gün içi sıra varsayımı: t + 1 barında H >= PL ise giriş olmuş sayılır; açılış PL'nin üstünde (>=) ise açılış fiyatıyla, değilse PL'de. 1 tik = %0,1 (x 0,999 / x 1,001; iş tanımı). Stop t + 1'in TAM gün dibini kullanır (kaynağın kuralı; giriş anında bilinmeyebilir: R'yi büyütür, +2R'yi zorlaştırır).
7. W4 KIRILAN SEVİYE: süpürme barı s'den ÖNCE tamamlanmış (i + 2 <= s - 1) en son yerel dibin L'si (W4Y'de en son yerel tepenin H'si); geri bakış sınırı yok. Yapı kırılımı = s+1 .. s+10 içinde İLK kapanış seviyenin ötesinde; geri test = kırılımdan sonraki 5 bar içinde İLK seviyeye dokunuş; açılış seviyeyi geçmişse (W4: O >= seviye; W4Y: O <= seviye) açılışta. Süpürmeden girişe kadar fiyatın stopun (süpürme mumu ucunun) ötesine geçmesi olayı İPTAL ETMEZ (pozisyon yok; iş tanımı şart koymuyor); giriş stopun yanlış tarafındaysa STOP_TERS ile atılır.
8. W3 / W3T, W5 / W5Y rastgele yürüyüşte de gerçek veridekine yakın sıklıkta çıkıyor (1000 barda ~8-13): bu kollar mekanik tanımdır, dedektör 'ayırt edici kalıp' bulmuyor; sonuç yalnız 'bu kurala göre işlem' olarak okunur.
9. W5: 'sonraki 1-3 bar' = t+1 .. t+3; ilk geri kapanış barı u; giriş u + 1 açılışı; stop = H_t .. H_u en yükseği (W5Y: en düşük L).
10. W6 'L son 10 barın en düşüğü' = L_t <= min(L_{t-9..t}) (t dahil); W7'de 20. W7T 'kapanış alt yarıda' = (C - L) / boy <= 0,5 (W7'nin >= 0,5 aynası).
11. W7 hacim: V_t >= 2 x medyan(V_{t-20..t-1}) (t hariç). Hacim, MI.mi_veri günlük açık kopyasının Volume sütunu (YO paneliyle bar bar eşit; assert). Hacim verisi VAR (iki pazarda); W7 kolları ölçülür.
12. GİRİŞ BARI DAHİL: sonuç barları e .. e+14 (YO gibi giriş barı dahil). Bar içi girişlerde (W3 / W4) giriş barının H / L'si girişten önce de oluşmuş olabilir: aynı barda hedef ve stop = STOP ÖNCE (kötümser; iki yönde aynı). Giriş barında stopa dokunuş da sayılır (kötümser).
13. ATR HEDEFİ: ATR(e-1) (giriş barından önceki son tamamlanmış bar); taban günlerinde ATR(k) (giriş k + 1); taban hissenin aynı hücredeki YO örnek günleri (k % 5 == 0, P2), giriş açılışta.
14. +2R TABANI: olayın R / giriş oranı r ile aynı hissenin aynı hücredeki örnek günlerinde H >= O(1 + 2r) önce mi L <= O(1 - r) önce mi (aşağıda ayna).
15. R KATI: stopa ilk dokunulan bar; o bar e'den sonraysa ve açılışı stopun ötesindeyse çıkış açılışta (boşluk kaybı), değilse stop seviyesinde; dokunulmazsa C[e+14].
16. 10 GÜN YÖN: yön x (C[e+9] - giriş) > 0 (giriş barı 1. gün). Bulkowski'nin %82-84 / %78-79 / %60 / %59'u 'kırılım yönü' oranıdır; bizim ölçü aynı değil, yalnız yan yana yazılır.
17. TOPLAM FARK / SEÇİM / ATR / +2R / R katı yön düzeltmeli (aşağı desende işaret çevrilir). SEÇİM'de P15 giriş satırının açılışından (bar içi girişte de).
18. BH: kol p'si = dört ABD p'sinin en büyüğü (TF ve KAT, iki dönem; kesişim-birleşim). Aile 17 kol. p = (1 + #(boot <= sıfır)) / (B + 1).
19. AVR şartı yalnız n >= 100 hücrede; n < 100 hücrede şart aranmaz, 'AVR n < 100' notu yazılır. ÖLÇÜLEMEDİ yalnız ABD hücreleriyle (n < 300 ya da ay < 12).
20. TEKİL: aynı hisse aynı kolda giriş barı farkı < 5 olan ikinci olay atılır (giriş barına göre, filtrelerden sonra). Kollar arası örtüşme atılmaz (ayrı ölçülür).
21. KİLİTLİ: desenin ilk barının tarihi .. giriş barının tarihi takvim aralığında ham veride geçersiz bar payı > 0,20 -> atılır (MUM_IZI_UC.uc_kilitli_pay).
22. Evren bugün yaşayan hisseler: aşağı yönlü desenlerin aleyhine, yukarı yönlülerin lehine; T1 aynı evrenden olduğu için TOPLAM FARK bu yanlılığı kısmen giderir.

## Hüküm (önceden; iş tanımı 3. bölüm)

- ABD 2016-19 ve 2020-22'de TOPLAM FARK > 0 ve alt > 0 VE ATR KAT > 1 ve alt > 1 VE AVR iki dönemde (n >= 100 olan hücrelerde) TOPLAM FARK nokta değeri > 0 VE BH (q 0,10) geçer
- TERS: ABD iki dönemde de TOPLAM FARK üst ucu < 0
- TEK DÖNEM: ABD şartları (TF ve KAT alt uçları) yalnız bir dönemde
- sıra: ÖLÇÜLEMEDİ (ABD hücrelerinden birinde n < 300 ya da farklı ay < 12) > TUTAR > TERS > TEK DÖNEM > TUTMADI

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hisse aynı hücre (pazar x dönem) YO örnek günleri: TOPLAM FARK = hissenin kendi dönem ortalamasına göre (T1); ATR hedefi KAT ve +2R payı aynı hissenin rastgele günleriyle, +2R tabanında aynı R / giriş oranı (desen stopunun mekanik etkisi dışlanır); SEÇİM aynı gün piyasa P15'i; aşağı desenlerde işaret çevrilir |
| K2 | geleceğe bakma | EVET | her dedektör yalnız giriş barına kadarki veriyle (test: giriş barından sonraki barlar bozulunca ve seri kesilince olaylar aynı); yerel uç i + 2 tamamlanınca (test); PL / PH önceki 20 bar; ATR hedefinde ATR(e-1); sonuç fonksiyonları ayrı ve yalnız ölçüm kapısından sonra; veri <= 2022-12-31 assert + KASA kapısı |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0, fiyat sonlu > 0); kilitli / hacimsiz / fiyat adımına yapışmış bar payı > 0,20 olan desen penceresi atılır (MUM_IZI_UC.uc_kilitli_pay); 15 bar <= 30 takvim satırı; giriş boşluğu <= 10 satır |
| K4 | tekilleştirme | EVET | aynı hisse aynı kolda 5 bar içindeki ikinci olay atılır (atılan sayı yazılır); çıkarım ay kümeli bootstrap; n olay ve farklı ay ayrı; en kalabalık 3 ay payı; medyan R15 ve medyan R katı bilgi |
| K5 | giriş fiyatı | EVET | giriş = sinyal barından sonraki açılış (W1, W2, W5, W6, W7); W3 / W4'te kaynak kuralı: seviyeye dokunulunca seviyede, açılış seviyeyi geçmişse açılışta (test); sinyal barı kapanışı kullanılmaz |
| K6 | veri birimi | EVET | YO paneli (OS / MI bölünme düzeltmeli açık kopya); getiriler oransal, yerel para; pazar içi taban; hacim yalnız hisse içi oran (W7) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: sonuç yukarı yanlı; aşağı yönlü desenlerin aleyhine, yukarı yönlülerin lehine; raporda yazılır |
| K8 | örneklem ve dönem | EVET | n < 300 ya da farklı ay < 12 -> ÖLÇÜLEMEDİ; ABD iki dönem + AVR iki dönem; BH q 0,10 (17 kol); AVR n < 100 hücrede şart aranmaz (not) |
| K9 | ön kayıt | EVET | WD_ON_KAYIT.md: WD_KOD_SHA, WD_ESIK_SHA, olay dosyası ve YO panel sha'ları, SAYIM_SHA, sentetik sonuçları; ölçüm kapısı: kontrol + sha + commit + temiz ağaç + KASA; ikinci koşu durur; eşikler sonuçtan sonra değişmez |
| K10 | ayrıştırma | EVET | hacim sütunu ve kapanışlar YO panel deposuyla bar bar eşit (assert); olay dosyası şeması sayımda; dedektörler elle kurulmuş yapay seriler ve pozitif / negatif sentetik setle sınandı |
| K11 | yeniden üretim | EVET | rapordan önce >= 3 satır (kol x hücre) olay dosyası + ham panelden bağımsız kısa kodla yeniden üretilir; fark DUR |
| K12 | ifade | EVET | 'TUTAR' yalnız hüküm kuralının bütün şartları sağlanınca; Bulkowski oranları 'kırılım yönü' oranıdır, bizim 10 gün yön payı ile yan yana ama aynı ölçü değil; sayı ile yorum ayrı cümlede; evren notu |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_wd); mevcut modüller ve defter dosyaları değişmez (yalnız import); yalnız kendi yolları commit; sızıntı taraması MI._mi_yaz; SEKIL_DEVAM'a dokunulmaz / import edilmez; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |
