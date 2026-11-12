# KÖR TEST ÖN KAYIT — VDYT2 G5 sessiz bölge dedektörü ile insan gözü (kor_vdyt2_20261112) — ölçümden (Cemal'in işaretlerinden) ÖNCE

Yazım zamanı: 2026-11-12 20:24:21 UTC
ESIK_SHA256: 6a99e21a9095bdef121e3710774d748b9907d5997a70f9d1a4962fa495e3162b
KOD_SHA256: 84de36826450ae300bcb72dda29062a3df40821d669ed72561e55f16e2ff39ac
VDYT2_KOD_SHA256: e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741
VDYT_KOD_SHA256: 10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d
ANAHTAR_SHA256: 73da87f12549b013e89b7dd24f11fdbc51c474ea1559410ad528e5ea049b6319
MANIFEST_SHA256: 7d609ffafcb8544132a727d47786a36c26fed3ba465f851c8fe3b000265d6664
Sürüm: KOR_TEST v1.0 (kor_vdyt2_20261112): İş 1 Tiingo OHLC doğrulaması + İş 2 insan gözü kör testi (ön kayıt; ölçüm Cemal'in işaretlerinden sonra)

Bu dosya ve KOR_TEST.py git'e işlenmeden, eşik mührü / kod / anahtar / manifest sha256'sı tutmadan `olc` ÇALIŞMAZ (KorHata, çıkış 1). Cevap anahtarı (/tmp/kor_test_vdyt2/anahtar.json) Cemal işaretlemeden repoya KONMAZ; `olc` onu sha256 denetiminden sonra kor_test_anahtar.json olarak kopyalar. Sonuç görüldükten sonra tanım, eşik, set ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır.

## 0. Amaç (Cemal, 12 Kasım 2026, aynen)
'Tiingo'nun borsadan silinmiş şirketler için geçmiş OHLC verisi sağlayabildiği örneklerle doğrulanmalı. İlk örneklerde algoritmanın insan gözünün gördüğü sıkışma bölgelerini yakaladığına dair ölçülebilir işaret bulunmalı. Veri dalını kalıcılaştırmak için acele etmeyelim; önce sinyalin varlığını doğrulayalım; sonra Aralık kotasını yalnızca bu test için kullanalım.'
- Soru: VDYT2 G5 dedektörünün 'küçük mumlu sessiz bölge' dediği günleri insan gözü de sessiz bölge olarak görüyor mu, bölge dışı günleri görmüyor mu?
- Bu test yalnız BÖLGE TANIMININ insan gözüyle uyumunu ölçer; getiri, yön ya da genişleme tahmini ölçmez (VDYT2 kararları, Ç163 ve VDYT2-B değişmez).

## 1. Set (40 grafik; kural ve tohum önceden, KOR_ESIK)
- G5 (ANA, 16: BIST 8 + ABD 8): VDYT2 satir_<pazar>_G5.csv.gz (/tmp/vdyt2/kasa; wf klasöründekiyle içerik aynı), kaynak GERCEK, karar yaşı 10-30 (VDYT2 karar yaşları 10 / 15 / 20 / 30; P1 olsun olmasın). Karar günü açık bir G5 bölgesinin içinde (tespit <= t < bitiş; VDYT2.py fonksiyonlarıyla yeniden hesaplanıp doğrulanır).
- KONTROL (16: BIST 8 + ABD 8): aynı pazarın kontrol_<pazar>_G5.csv.gz DIŞARI satırları (aynı hisse / yıl / NATR ondalığı, bölge dışı, geçerli) VE [t-29, t] hiçbir G5 bölgesinin [bas, bit] aralığıyla kesişmez (sağ uçta son 30 mumda dedektörün bölgesi yok). İlk geçişte G5 grubunun hisseleri dışarıda (tercih).
- BATAN (8: 4 G5 + 4 kontrol): Tiingo pilot önbelleğinde pilotu GEÇEN 7 seri (BBBYQ, WEWKQ, SHLDQ, HTZGQ, REVRQ, DNR, GNC); VDYT2-B ile aynı temizlik (V2B.v2b_tiingo_df -> V1.vdyt_bar_temizle -> 2010-01-01 .. 2026-08-31); G5 durumu ve bölgeler V2.v2_olculer + V2.v2_bolgeler ile (VDYT2.py DEĞİŞMEDİ); karar günü < Form 25-NSE günü; uygunluk: ABD VDYT kuralı yeniden: bar no >= 252, ekrandaki (ham) kapanış >= 2 $, 20 gün medyan işlem değeri (min 10 gün) >= 1 mn $; t >= 260; panel (kesit) kurulmaz. BATAN_G5 = açık G5 bölgesinde yaş 10-30, geçerli; BATAN_KONTROL = bölge dışı, [t-29, t]'de bölge yok, geçerli (sözde yaş 10). Önce farklı hisse; yetmezse aynı hisseden >= 120 bar uzak ikinci gün. Yetmezse bulunan sayı yazılır (uydurma yok).
- Seçim: numpy default_rng([20261118, grup no]) permütasyonu sırasıyla aday gezilir (aday listesi sembol, t sıralı); G5 BIST 0, G5 ABD 1, KONTROL BIST 10, KONTROL ABD 11, BATAN_G5 20, BATAN_KONTROL 21; grafik numaraları default_rng([20261118, 99]) permütasyonu. Her grupta farklı hisse. Aday atlanır <=> hizalama tutmaz / 120 barlık pencerede > 15 takvim günü boşluk / bölge doğrulaması tutmaz.
- Aday listesi sha256 (sembol, tarih, t, yaş; CSV):
  - BATAN_G5: 7427462697d0e77b15cb43caaccdc398b7d3914050ec42830f487b2705461577 (116 aday)
  - BATAN_KONTROL: 63ecc6f83f02960dbf95237e80ae050939531d2e127c597441fbd16c813dd9ba (9.193 aday)
  - G5_ABD: d22775e9eb216d608f8f9c3fd996e8853aa3de796911eee74eb5d58ca9b3d918 (36.675 aday)
  - G5_BIST: 04e0023eb839559e2e242d2be393a6773a7de915c79f3fa595f9b5194d8d437e (9.138 aday)
  - KONTROL_ABD: 83dc8eaa6ab985ae5083f7dad068087781c72e9fcaab1dd56332158831026f62 (94.529 aday)
  - KONTROL_BIST: af31300b0a787e36b114ccd6368fd5c1f34261cbc746524b76cf2e752112c1d1 (16.210 aday)
- Bulunan: {"BATAN_G5": 4, "BATAN_KONTROL": 4, "G5": 16, "KONTROL": 16}
- VDYT2 tablo sha256 (kasa klasörü; dosya / açılmış içerik; wf klasöründeki aynı adlı tablonun açılmış içeriği aynı mı):
  - bolge_ABD_G5.csv.gz: dosya 875f9e57ee13c893f50f1222d07b9564b171b5a774de407fc0f01fd707df557c / içerik bc125ad4d5d5b89c90005abe7053205710abee2e2087bcb6528806dd03f811e5 (wf içerik aynı: evet)
  - bolge_BIST_G5.csv.gz: dosya b607d16f45ab90e25e6bfb0f5829ef77bc63b34aad35ba199da544181e5cb3f4 / içerik 499cd37423e741793f31fcf82229d645c935d212afa7098386572999daba994a (wf içerik aynı: evet)
  - kontrol_ABD_G5.csv.gz: dosya 49fe47158dc33be255c719ef6bb28eeeee31ab1422d45df14cb55699ee444fcd / içerik b7ab81562dd318a24da50e158fc0476642e5624ff9227f7c883c271872b5c172 (wf içerik aynı: evet)
  - kontrol_BIST_G5.csv.gz: dosya b2edcf2daa9da77f56e4cd3e944ccedeffcce3155cd4e1be63ed79f032d4e775 / içerik adf68c34deb815115c1c0a152356227e78e32dda1efc8b05cff2f26c47052de0 (wf içerik aynı: evet)
  - satir_ABD_G5.csv.gz: dosya 4442315afb90ce8a4ee35949ea40e5d5cdfdcad2b53fd02b6cf7120ca31ddfcf / içerik c65928af4b6f3ba011e0e6e24d963e33680eb24db88c0f2c046d25863c01c1a7 (wf içerik aynı: evet)
  - satir_BIST_G5.csv.gz: dosya 6ee1ac3a46968932beb716c916c01abf53c60e4e360614a1b56aa830aafcf1c8 / içerik a3474c6d9fc6811a4cf10d5ff6d58c5795ec2c794ee26380bc9a325685bcd119 (wf içerik aynı: evet)

## 2. Grafik
- Karar gününe kadar son 120 işlem günü; karar günü SAĞ UÇTA (x = 0); karar gününden sonraki hiçbir bar yok. Mum gövdesi + fitil (yukarı #26a69a, aşağı #ef5350), altta hacim paneli (payı 0.25). Fiyat fiyat / karar günü kapanışı x 100 (fiyat düzeyi hisseyi / pazarı ele vermez). yalnız eksen sayıları (x: gün sırası, y: normalize fiyat); hacim ekseni sayısız; başlık / etiket / çizgi / ızgara YOK. 1200x800 piksel, 110 dpi, PNG üst verisinde yazılım bilgisi yok.
- Grafik sayısı 40; en büyük dosya 27.606 bayt, ortalama 24278 bayt. Klasör /tmp/kor_test_vdyt2/grafik/ (repoya girmez; batan grafikleri Tiingo verisi). Manifest (numara, dosya, sha256; GRUP BİLGİSİ YOK): /tmp/kor_test_vdyt2/manifest.json.

## 3. Cemal'e soru (her grafik)
- Soru 1 (ANA): 'Grafiğin sağ ucunda (son 10-30 mumda) küçük mumlu, dar bantlı sessiz bir bölge görüyor musun?' Cevap: EVET / HAYIR / EMİN DEĞİLİM.
- Soru 2 (BİLGİ): 'Bölgenin altında savunulan bir destek (tekrar tekrar test edilen dip) görüyor musun? (isteğe bağlı)' Cevap: EVET / HAYIR.
- Cevap dosyası: numara -> cevap (JSON {"1": {"bolge": "EVET", "destek": "HAYIR"}} ya da satır başına '1 EVET HAYIR'); 40 numaranın hepsi gerekli; şablon /tmp/kor_test_vdyt2/cevap_sablon.json.

## 4. Ölçüler (önceden)
- ANA karşılaştırma: G5 (16) ile KONTROL (16). Algoritma etiketi: G5 = 1, KONTROL = 0. İnsan etiketi: EVET = 1, HAYIR = 0; EMİN DEĞİLİM ayrı sayılır ve oranlarda PAYDADAN ÇIKAR (ANA); sağlama olarak HAYIR'a eklenmiş hali de yazılır (BİLGİ).
- p_G5 = EVET / (EVET + HAYIR) G5 grubunda; p_K aynısı KONTROL'de; Wilson %95 aralıkları; fark = p_G5 - p_K, %95 aralığı Newcombe hibrit Wilson (ANA) ve hisse kümeli bootstrap (B = 2000, tohum 20261119; BİLGİ).
- Fisher kesin testi (2x2: grup x EVET / HAYIR) İKİ YÖNLÜ p (karar); tek yönlü (G5 > KONTROL) p BİLGİ.
- Cohen kappa (algoritma G5 / değil ile insan EVET / HAYIR; EMİN DEĞİLİM hariç).
- Duyarlılık ve kesinlik (insan etiketi doğru kabul edilerek): duyarlılık = insanın EVET dediklerinin G5 payı; kesinlik = G5 dediklerinin insan EVET payı; özgüllük de yazılır.
- BİLGİ: BATAN alt grubu ayrı (BATAN_G5 / BATAN_KONTROL; n küçük); 40 grafiğin tümünde kappa; pazar (BIST / ABD) kırılımı; Soru 2 (destek) ile G4 (gövde tabanı savunma hattı) durumunun uyumu ve kappası.

## 5. KARAR KURALI (önceden)
- BAŞARILI <=> p_G5 >= 0,70 VE p_K <= 0,35 VE kappa >= 0,40 VE Fisher iki yönlü p < 0,05.
- ZAYIF İŞARET <=> BAŞARILI değil VE p_G5 >= 0,60 VE fark > 0,0.
- İŞARET YOK <=> aksi. VERİ YETERSİZ (G5 ya da KONTROL grubunda EVET + HAYIR < 8) İŞARET YOK sayılır.
- BATAN alt grubu ve destek sorusu karara girmez (BİLGİ).

## 6. KARAR KULLANIMI (Cemal'in sırası; önceden)
- BAŞARILI ya da ZAYIF İŞARET -> Aralık Tiingo kotası YALNIZ VDYT2-B testi B için kullanılır; İŞARET YOK (VERİ YETERSİZ dahil) -> B'ye kota harcanmaz, dedektör önce düzeltilir (yeni ön kayıtla).
- Tiingo'ya bu testte istek yok; Aralık kotası ancak bu karardan sonra ve yalnız VDYT2-B testi B için kullanılır. Veri dalı kalıcılaştırılmaz (Cemal: 'acele etmeyelim').

## 7. Yanlılık ve sınırlar (beyan)
- 40 grafik küçük örneklemdir; sonuç 'bulgu' değil, dedektörün insan gözüyle uyumuna dair İLK işarettir.
- Tek değerlendirici (Cemal): değerlendiriciler arası uyum ölçülmez. Cemal VDYT2'nin G5 tanımını biliyor; grafikte grup bilgisi olmadığı için kör.
- KONTROL günleri 'sağ uçta son 30 mumda bölge yok' koşuluyla seçildi: soru da son 10-30 mumu sorduğu için bu, soruyla dedektörün aynı pencereye bakmasını sağlar; bölge dışı ama bölgeye yakın günler (dedektörün sınır davranışı) bu testte ölçülmez.
- Fiyat normalize edildi (karar günü kapanışı = 100); hacim ekseni sayısız: düzey / pazar bilgisi gizli. Fiyat ekseni doğrusal.
- BATAN uygunluğu tek hisse kuralıyla (kesit paneli kurulmadan); BATAN_KONTROL NATR ondalığıyla eşlenmedi.

## EK. Eşik sözlüğü (mühür = sha256 of sıralı JSON; VDYT2 sessiz / bölge / büyük mum / geçerlilik eşikleri dahil)

```json
{
 "grafik": {
  "asagi": "#ef5350",
  "bar": 120,
  "dpi": 110,
  "font": 12,
  "govde_en": 0.7,
  "hacim_pay": 0.25,
  "hedef_kb": 150,
  "metin": "yalnız eksen sayıları (x: gün sırası, y: normalize fiyat); hacim ekseni sayısız; başlık / etiket / çizgi / ızgara YOK",
  "normal": "fiyat / karar günü kapanışı x 100",
  "piksel": [
   1200,
   800
  ],
  "x_tik": [
   -120,
   -100,
   -80,
   -60,
   -40,
   -20,
   0
  ],
  "yukari": "#26a69a"
 },
 "karar_kullanimi": "BAŞARILI ya da ZAYIF İŞARET -> Aralık Tiingo kotası YALNIZ VDYT2-B testi B için kullanılır; İŞARET YOK (VERİ YETERSİZ dahil) -> B'ye kota harcanmaz, dedektör önce düzeltilir (yeni ön kayıtla).",
 "olcum": {
  "ana_gruplar": [
   "G5",
   "KONTROL"
  ],
  "basari": {
   "fisher": "iki_yonlu",
   "fisher_p_max": 0.05,
   "g5_evet_min": 0.7,
   "kappa_min": 0.4,
   "kontrol_evet_max": 0.35
  },
  "bilgi_gruplar": [
   "BATAN_G5",
   "BATAN_KONTROL"
  ],
  "bootstrap": {
   "B": 2000,
   "kume": "hisse",
   "tohum": 20261119
  },
  "destek": "insan destek EVET / HAYIR ile G4 (gövde tabanı) durumu: uyum ve kappa (BİLGİ)",
  "emin": "EMİN DEĞİLİM oranlarda paydadan çıkar (ANA); sağlama: HAYIR'a eklenmiş hali (BİLGİ)",
  "fark_araligi": "Newcombe hibrit Wilson (yöntem 10) ANA; hisse kümeli bootstrap BİLGİ",
  "guven": 0.95,
  "min_payda": 8,
  "z": 1.959963984540054,
  "zayif": {
   "fark_min": 0.0,
   "g5_evet_min": 0.6
  }
 },
 "set": {
  "BATAN_G5": 4,
  "BATAN_KONTROL": 4,
  "G5": {
   "ABD": 8,
   "BIST": 8
  },
  "KONTROL": {
   "ABD": 8,
   "BIST": 8
  },
  "batan": {
   "karar_once_f25": true,
   "kontrol_yas": 10,
   "semboller": [
    "BBBYQ",
    "WEWKQ",
    "SHLDQ",
    "HTZGQ",
    "REVRQ",
    "DNR",
    "GNC"
   ],
   "tekrar_izni": true,
   "uygunluk": "ABD VDYT kuralı yeniden: bar no >= 252, ekrandaki (ham) kapanış >= 2 $, 20 gün medyan işlem değeri (min 10 gün) >= 1 mn $; t >= 260; panel (kesit) kurulmaz"
  },
  "farkli_hisse": true,
  "g5_kaynak": "GERCEK",
  "kontrol_kaynak": "DISARI",
  "pencere_kopuk_yok": true,
  "sag_bosluk": 30,
  "yas": [
   10,
   30
  ]
 },
 "soru": {
  "bolge": "Grafiğin sağ ucunda (son 10-30 mumda) küçük mumlu, dar bantlı sessiz bir bölge görüyor musun?",
  "bolge_cevap": [
   "EVET",
   "HAYIR",
   "EMİN DEĞİLİM"
  ],
  "destek": "Bölgenin altında savunulan bir destek (tekrar tekrar test edilen dip) görüyor musun? (isteğe bağlı)",
  "destek_cevap": [
   "EVET",
   "HAYIR"
  ]
 },
 "surum_etiket": "kor_vdyt2_20261112",
 "tohum": 20261118,
 "vdyt2": {
  "kod_sha256": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",
  "tanim": "G5",
  "vdyt_kod_sha256": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d"
 }
}
```
