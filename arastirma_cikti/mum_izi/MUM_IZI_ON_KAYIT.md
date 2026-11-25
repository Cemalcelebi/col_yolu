# MUM_IZI ÖN KAYIT (2026-11-25T09:47:37Z)

Gerçek veri taraması (E) bu dosya commit edildikten SONRA koşar; `mi_kapi` bu dosyadaki sha'ları, kontrol tablosunu ve git kaydını denetler.
Bu ana kadar gerçek veride (2016-22 ABD / AVR / BIST) hiçbir pencere puanlanmadı; sentetik üretici yalnız ABD 2005-2014 barlarını kullandı.

## Mühürler

KOD_SHA: 16759a795d91fdf35b229656cd4bcfccc690c553215e93e52cc5c34ed3c3e63f
ESIK_SHA: fbbdbdddea6d6f3f4af7b4cc3ceebe7aa8326302edc6ce1b628a0b46f3faa58d
SABLON_SHA: 86ff7603dea2602d10c4710f362b0d7185c9dc4d95ade7b580f8eb7240cdb612
SENTETIK_SHA: e49f24acc9cfa21554560997b61748f3f0d5963c6d8561aaa46e4b8b1d2c5b77

- Kod commit'i: ba19953ebecd6d4e2ed1d36d9fc415d69369186f 2026-11-25T09:47:32+00:00
- Görüntü sha: e026311cf66b199a4c313225aa3a127458567269d236ee66c6d344530a1a539f
- Açık kopya: ABD 81899ab74c2fe7bd (4450 hisse, 2015-01-02..2022-12-30), AVR 45cfdd5e0d24a960 (572, 2015-01-01..2022-12-30), BIST 08b6228ddc3ecdc3 (475, 2015-06-01..2022-12-30); KASA kapısı kesik 2022-12-31
- Üretici havuzu: 300 ABD hissesi, 699480 bar (2005-01-01..2014-12-31), sha 8dc22a9eb5148d94

## Şablon (sayısallaştırma)

- Bölge mumu 20 (renk YKYYKYKKYKYKYYYYKYYY), tepe mumu 3 -> TAM L = 20, TEPESİZ L = 17
- Pencere uzunlukları: tam [16, 18, 20, 22, 24], tepesiz [14, 15, 17, 19, 20]
- Sınıflar: {'BOLGE': 20, 'BAGLAM': 3, 'GIZLI': 1, 'KESIK': 1}

## Eşik (sentetik testten; gerçek veriye bakılarak DEĞİŞMEZ)

- TAM: S eşiği = 0.59 (kök A %20 gürültü yakalama 82.7 %, n 1200); kök B (tekrar) %20 gürültü yakalama 83.6 %; yanlış alarm (tekil / 1.000 bar) blok 1.98, rastgele yürüyüş 3.27; tau [1.3041, 0.4633, 1.8745]
- TEPESIZ: S eşiği = 0.56 (kök A %20 gürültü yakalama 85.2 %, n 1200); kök B (tekrar) %20 gürültü yakalama 84.1 %; yanlış alarm (tekil / 1.000 bar) blok 5.63, rastgele yürüyüş 9.43; tau [1.1869, 0.4514, 1.6382]

## Tanımlar (MI_ESIK; sha yukarıda)

```
{
 "surum": "MI-1.0",
 "goruntu": {
  "boyut": [
   1080,
   2400
  ],
  "fiyat_satir": [
   380,
   1200
  ],
  "renk": {
   "yesil": "G-R > 60, G-B > 30, G > 110",
   "kirmizi": "R > 170, G < 105, B < 100, R-G > 90",
   "turuncu": "R >= 225, 95 <= G <= 175, B <= 150, R-B >= 90; 4 aşındırma + 8 genişletme (kalın çizgi çekirdeği)",
   "fitil": "max(R,G,B) < 190, B-R >= 3, |R-G| <= 14 (mavi-gri); tarih kesikli çizgisi nötr gri (B = R) olduğu için dışarıda",
   "doji": "kırmızımsı R-(G+B)/2 >= 20 ya da yeşilimsi G-(R+B)/2 >= 15, merkezden 4-11 piksel yanda (fitil dışı)",
   "bant": "|R-G| <= 10, 5 <= B-R <= 28, 170 <= R <= 230 (lavanta)"
  },
  "izgara": "katı gövde sütun öbekleri (genişlik >= 20 px) -> merkezler -> x = a + b k en küçük kareler (b ilk tahmin ardışık fark medyanı)",
  "govde_satir_min": 4,
  "fitil_bosluk": 2,
  "fitil_yari": 3,
  "govde_yari": 10,
  "bant_yari": [
   14,
   22
  ],
  "bant_izleme_tol": 6,
  "konum": "İÇ = mumun sütununda turuncu çekirdek hem tepenin üstünde hem dibin altında VE merkez pikseli turuncu değil; ÇİZGİ = merkez turuncu; DIŞ = öteki. Bölge = İÇ mumlar (görüntü kenarında kesilen mum KESİK, bölgeye girmez); bölgenin solundaki DIŞ / ÇİZGİ mumlar BAĞLAM (gövdesi hiç görünmeyen çizgi mumu GİZLİ, ölçülmez)",
  "y": "fiyat_px = 2400 - satır (y yukarı pozitif)"
 },
 "sablon": {
  "tam": "bölgenin bütün tam görünen mumları (İÇ)",
  "tepe": "bölge sonundaki ardışık High > üst bant mumları (üst bant yürüyüşü); TEPESİZ şablon = bunlar çıkarılmış ilk mumlar",
  "esneme": [
   0.8,
   0.9,
   1.0,
   1.1,
   1.2
  ]
 },
 "benzerlik": {
  "bant": {
   "n": 20,
   "k": 2.0,
   "std": "ddof 0 (anakütle)"
  },
  "dizi": "pencere mumları birim u = ort(H-L), seviye = ort((H+L)/2); z = (X - seviye) / u, X = O / H / L / C; pencere L mumuna doğrusal yeniden örneklenir (esneme); D_dizi = kök(ort (z - z*)^2) (birim: ortalama mum boyu)",
  "bant_dizi": "%B = (C - alt) / (üst - alt) (üst = alt ise 0,5); D_bant = kök(ort (%B - %B*)^2)",
  "ozellik_alt": [
   "ust_fitil",
   "alt_fitil",
   "ust_alt_log",
   "govde_oran",
   "kucuk_mum_pay",
   "yuk_dip_pay",
   "kapanis_egim",
   "kapanis_r2",
   "pB_bas",
   "pB_son",
   "sma_ustu_pay",
   "bant_gen_oran_log"
  ],
  "oz": "D_oz = kök(ort ((F - F*) / sd)^2) ozellik_alt üzerinde; sd = rastgele (blok bootstrap) pencerelerde IQR / 1,349 (0 ise std)",
  "S": "S = exp(-(D_dizi / tau_dizi + D_bant / tau_bant + D_oz / tau_oz) / 3); tau = rastgele pencerelerin medyan uzaklığı (kalibrasyon) -> rastgele pencere S ~ e^-1 = 0,37, birebir şablon S = 1",
  "uc_bilesen": "S her pencere sonu t için t'ye kadarki barlardan; pencere uzunlukları L x esneme (yuvarlak, tekil); t'de en büyük S",
  "hizalama": "sabit hizalama + doğrusal yeniden örnekleme (DTW değil): DTW her dizini serbest bükerek rastgele diziyi de şablona yaklaştırır (yanlış alarm), hesap yükü milyonlarca pencerede ağır; esneme +-%20 açık uzunluk ızgarasıyla aranır",
  "kalibrasyon": {
   "seri": 400,
   "n": 320,
   "pencere": 20000,
   "kok": 7700
  }
 },
 "sentetik": {
  "uretec": [
   "blok",
   "ry"
  ],
  "baglam": [
   "dip",
   "yatay",
   "tepe"
  ],
  "gurultu": [
   0.0,
   0.1,
   0.2,
   0.3
  ],
  "tohum": 200,
  "olcek": [
   0.5,
   2.0
  ],
  "olcek_dagilim": "log-düzgün",
  "esneme": [
   0.8,
   1.2
  ],
  "esneme_dagilim": "düzgün",
  "konum_tol": 3,
  "seri_on": 200,
  "seri_son": 60,
  "baglam_bar": 40,
  "baglam_egim": 0.005,
  "blok": 5,
  "ry": {
   "sigma": [
    0.01,
    0.03
   ],
   "bosluk_kat": 0.25,
   "fitil_kat": 0.5
  },
  "yanlis": {
   "seri": 200,
   "n": 1000,
   "tekil": 15
  },
  "kok": {
   "A": 25112026,
   "B": 25112027
  },
  "esik": {
   "gurultu": 0.2,
   "yakalama": 0.8,
   "izgara": 0.01,
   "kural": "kök A, %20 gürültü, üç bağlam x iki üretici birleşik (1.200 tohum): yakalama >= %80 veren EN YÜKSEK S (0,01 ızgara); tam ve tepesiz ayrı; kök B aynı eşikle TEKRAR (yalnız rapor)"
  },
  "birebir": "yakalanan tohumlarda bulunan pencerenin ölçüleri ile gömülü (gerçek) pencerenin ölçüleri arasında ort |fark| / sd ve Pearson r (MI_OZELLIK, bağlam ölçüleri hariç)"
 },
 "uretec_havuz": {
  "pazar": "ABD",
  "donem": [
   "2005-01-01",
   "2014-12-31"
  ],
  "hisse": 300,
  "min_bar": 1000,
  "min_fiyat": 5.0,
  "tohum": 2511,
  "tanim": "TEZGAH2 V_ABD2 geçerli barları (H > L, V > 0); mum tanımlayıcıları: log boşluk O/C(-1), log gövde C/O, log üst fitil H/max(O,C), log alt fitil min(O,C)/L; |log| > 0,3 olan bar (bölünme / hata) havuz dışı"
 },
 "gercek": {
  "pazar_karar": [
   "ABD",
   "AVR"
  ],
  "pazar_bilgi": [
   "BIST"
  ],
  "veri_bas": "2015-01-01",
  "tarama": [
   "2016-01-01",
   "2022-12-31"
  ],
  "tekil": 15,
  "konum_bar": 120,
  "konum_pay": 0.03,
  "konum_tanim": "TEPE: C(t) >= 0,97 x son 120 barın (t dahil) en yüksek kapanışı; DİP: değilse ve C(t) <= 1,03 x en düşük kapanış; ORTA: öteki; KISA: 120 bar yok. BAŞKA YERDE = DİP + ORTA",
  "havuz": "ABD / AVR: TEZGAH2 P2 (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1; giriş günü d'de) VE CETVEL2 v2.2 havuzu (c2_olay tekil 15). BIST: yalnız CETVEL2 v2.2 havuzu (P2 BIST'te tanımlı değil; bilgi)",
  "donem": {
   "d1619": [
    "2016-01-01",
    "2019-12-31"
   ],
   "d2022": [
    "2020-01-01",
    "2022-12-31"
   ]
  },
  "ufuk": 15,
  "es_min": 5,
  "stop_carpan": 0.98,
  "h5_es_sayi": 20,
  "h5_es_kok": 2513,
  "plasebo_tohum": 200,
  "yon": "?",
  "prefix_n": 30,
  "prefix_kok": 2514,
  "duz_n": 20,
  "gorsel": {
   "tepe": 6,
   "baska": 6,
   "rastgele": 8,
   "once": 20,
   "sonra": 15,
   "tohum": 2512
  }
 },
 "karar_kurali": "BİLGİ ETİKETİ (şablon başına, 'hepsi' grubu, yön '?'): (1) dört karar hücresinin (ABD d1619 / d2022, AVR d1619 / d2022) dördünde C2 hükmü aynı yönde TUTAR (C2.c2_hucre: n >= 30, güç >= 0,80, FARK yönlü, boot ucu, SIRA, L3O) VE c2_plasebo o yönde geçti -> 'BİRLEŞİK İZ BİLEŞENİ ADAYI' (KASA KURALI: tek iz, kasa açılmaz); (2) değilse dört hücrede n >= 30 ve güç >= 0,80 -> 'İZ DEĞİL'; (3) değilse en az bir hücre TUTAR -> 'EMARE'; (4) değilse 'ÖLÇÜLEMEDİ'. BENZERLİK: gerçek tekil eşleşme sıklığı (1.000 bar başına) / sentetik rastgele (aynı eşik, aynı tekil) oranı yazılır; hüküm yok. KONUM: tepe / başka yerde payları yazılır; hüküm yok."
}
```

## Karar / bilgi kuralı (önceden yazılı)

BİLGİ ETİKETİ (şablon başına, 'hepsi' grubu, yön '?'): (1) dört karar hücresinin (ABD d1619 / d2022, AVR d1619 / d2022) dördünde C2 hükmü aynı yönde TUTAR (C2.c2_hucre: n >= 30, güç >= 0,80, FARK yönlü, boot ucu, SIRA, L3O) VE c2_plasebo o yönde geçti -> 'BİRLEŞİK İZ BİLEŞENİ ADAYI' (KASA KURALI: tek iz, kasa açılmaz); (2) değilse dört hücrede n >= 30 ve güç >= 0,80 -> 'İZ DEĞİL'; (3) değilse en az bir hücre TUTAR -> 'EMARE'; (4) değilse 'ÖLÇÜLEMEDİ'. BENZERLİK: gerçek tekil eşleşme sıklığı (1.000 bar başına) / sentetik rastgele (aynı eşik, aynı tekil) oranı yazılır; hüküm yok. KONUM: tepe / başka yerde payları yazılır; hüküm yok.

Sonrası (R15, +%5) yalnız BİLGİ satırıdır; ana çıktı benzerlik sıklığı ve konumdur. KASA KURALI: tek iz -> kasa açılmaz.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = CETVEL2 v2.2 konum eşi (C2.c2_es: aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün aynı şablonun bütün olayları dışı); plasebo şans tabanı SAYIYLA: C2.c2_plasebo 200 tohum her karar hücresinde (aynı gün rastgele havuz hissesi, aynı cetvel); +%5 payı eşi = aynı gün aynı kovadan 20 rastgele üye, AYNI geometri (kendi son m barının en düşük Low x 0,98 stop); benzerlik sıklığının tabanı = sentetik rastgele seriler (blok bootstrap + rastgele yürüyüş, aynı eşik) |
| K2 | geleceğe bakma | EVET | S(t) yalnız t'ye kadarki barlar (bant SMA20 / std20 kendi barına kadar; pencere [t-m+1, t]); konum son 120 bar t dahil; mi_prefix: 30 rastgele olayda veri t'de kesilince S(t) aynı (assert); açık kopya <= 2022-12-31 + KASA.kasa_kapisi; üretici havuzu 2005-2014 (karar hücreleri 2016-22 dışı); eşik sentetikten, gerçek veriden önce |
| K3 | geçerli bar | EVET | gerçek veri OS.os_veri / OC.oc_veri_hazirla geçerli bar süzgeci (H > L, V > 0, O/H/L/C > 0); pencereler hissenin kendi geçerli barlarında; sentetik barlar H >= max(O,C) > min(O,C) >= L > 0 (test) |
| K4 | tekilleştirme | EVET | aynı hissede aynı şablon için eşiği geçen pencere sonları 15 geçerli bar tekil (ilk kalır); C2.c2_olay tekil 15 (birleşik takvim); sentetik yanlış alarm da 15 bar tekil sayılır (ham pencere sayısı ayrıca) |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş - 1; +%5 YH.yh_sim (kapanışla, takip stoplu) c2_bilgi üzerinden |
| K6 | veri birimi | EVET | TEZGAH2 V_ABD2 / V_AVR2 (yfinance auto_adjust, bölünme düzeltmeli; AVR Kur sütunu likiditede); S ölçek bağımsız (oranlar, mum boyu birimi); BIST V_BIST (fi_k1_veri) bilgi |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (TEZGAH2 ABD 5.394 / AVR 578 sembolden 2015-22'de verisi olan ABD 4.450, AVR 572; BIST 475): batanlar yok -> sonrası yukarı yanlı; olay ve eş aynı evrenden (yanlılık ikisine aynı); raporda yazılı |
| K8 | örneklem ve dönem | EVET | iki dönem (d1619, d2022) x iki karar pazarı ayrı hücre; n < 30 ÖLÇÜLEMEDİ; güç C2 eğrisi; sentetik koşul başına 200 tohum, iki bağımsız kök; tam ve tepesiz iki şablon = iki aile (sonrası yalnız bilgi, BH gerekmez; p'ler yazılır) |
| K9 | ön kayıt | EVET | MUM_IZI_ON_KAYIT.md: KOD_SHA, ESIK_SHA, SABLON_SHA, SENTETIK_SHA (eşik), açık kopya sha'ları; ön kayıt commit'i gerçek veri taramasından önce; mi_kapi kos'tan önce ik_kontrol_kapisi + sha + git (commit'li ve değişmemiş) denetler |
| K10 | ayrıştırma | EVET | sayısallaştırma: bindirme PNG (bütün mumlar) + 3 rastgele mumun yakın plan elle doğrulama PNG'si (mum_izi_elle_dogrulama.png); mum sayısı (20 iç) ve renk dizisi görüntüden elle sayımla karşılaştırılır (test_mum_izi) |
| K11 | yeniden üretim | EVET | mi_duz_S: 20 rastgele olayda S düz döngüyle (vektörsüz) yeniden; mi_yeniden: 2 hücre (ABD d1619, AVR d2022 tam iz) olay satır dosyasından düz pandas ile n / ort FARK / +%5 payı; tutmazsa rapor TUTMADI |
| K12 | ifade | EVET | 'iz' sözü yalnız karar kuralı geçerse; benzerlik / konum hükümsüz sayı; R15 (fiyat değişimi) ile kâr / zarar ayrı; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mi); yasak dosyalar (defterler, kural_defteri) ve UC_IZ2 dosyalarına dokunulmaz; yalnız kendi yolları git add; veri3 / /tmp/veri yalnız okunur; e-posta / anahtar taraması (mi_sizinti); ücretli servis yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tespit / benzerlik ölçümü; alım-satım önerisi yok |

## SAPMA

(ön kayıt anında yok; gerçek veriden sonra zorunlu sapma olursa raporda SAPMA başlığıyla yazılır)
## Elle doğrulama (K10, gerçek veriden önce)

- Mum sayısı: görüntüde turuncu dairenin içinde elle 20 mum; kod 20. Renk dizisi elle YKYYKYKKYKYKYYYYKYYY = kod; doji (gövdesi çizgi) 5, 8, 17, 20 = kod (test_mum_izi.test_sayisallastirma_elle).
- Rastgele 3 mum (2, 3, 5; tohum 2515) yakın planda (mum_izi_elle_dogrulama.png, solda ham, sağda bindirme): gövde üst / alt, fitil üst / alt ve üç bant noktası görüntüyle gözle örtüşüyor (fark en çok 1-2 piksel).
- Bindirme (mum_izi_bindirme.png): 20 bölge + 3 bağlam mumunda gövde çerçevesi ve fitil çizgisi görüntüdeki mumla çakışıyor. 18. mumun alt bant noktası turuncu çizginin altında (iki yandaki gözlenen sütunlar arasında doğrusal ara değer; `bant_alt_ara` = True).
- Gizli mum (0): turuncu çizginin altında, gövdesi görünmüyor -> ölçülmez. Kesik mum (21): görüntü kenarında, yalnız gövdesinin solu görünüyor -> şablona girmez. Bağlam büyük kırmızı mumun (−1) fitilleri çizgi altında: bağlam ölçüleri alt sınırdır.

## Varsayımlar

- Grafik gün içi (22 Kas ile 24 K arasında 12 mum -> 4 saatlik, 7/24 piyasa). İz ölçek bağımsız (birim = ortalama mum boyu, zaman esnemesi +-%20) kurulur ve GÜNLÜK veriye uygulanır.
- Fiyat ekseninde etiket yok: bütün ölçüler piksel ve ortalama mum boyu biriminde (y yukarı pozitif). Hacim çubukları ve MACD çok soluk / kısmi; parmak izine girmez.
