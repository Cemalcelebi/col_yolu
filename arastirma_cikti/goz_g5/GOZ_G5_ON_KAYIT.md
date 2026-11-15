# GOZ_G5 ÖN KAYIT — G5 x Cemal'in mevcut göz etiketleri (goz_g5_20261113)

Yazıldı: 2026-11-13 11:09:21 UTC. Ölçümden ÖNCE yazıldı; G5 hiçbir etiket bölgesinde hesaplanmadı. Eşikler aşağıdaki sözlükte, sonuca göre değişmez.

ESIK_SHA256: f4e6b492a4369ace6ee53975f78cbddec53360018fefb52ca65c8ceb2fbc547c
KOD_SHA256: 30444f65de2382540f6c4fa87a5b333f1bdc9bcd5dbe58fb6bda2b8a4902b756
VDYT2_KOD_SHA256: e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741
VDYT_KOD_SHA256: 10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d
VERI: /tmp/veri/V_BIST.pkl sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51

## Soru
Kör testte Cemal G5 grafiklerinde hiçbir belirti görmedi (Ç166). Burada yeni işaret istenmeden G5, Cemal'in daha önce elle verdiği çöl etiketlerine karşı
sınanır: (A) G5 Cemal'in çöllerinin içinde rastgele pencerelerden daha sık mı yanıyor; (B) gözün gördüğünü hangi basit ölçü yakalıyor; (C) bulunan ölçü
ikinci bir Cemal etiket setinde tutuyor mu.

## Etiketler (yalnız Cemal'in gözle verdikleri)
- kalibre_etiketler.csv: `7c9c6c27031b4575bf29141eb79d0dbdd38c15551465949305bd9b91c1fb9ca9`
- goz_esle/etiket_2026-10-20.csv: `b5474aa7d8dc6f6bf67b46a2da8fdb562f75a76947a77e90af6e705500f01b99`
- goz_esle/etiket_obek_ARZUM.csv: `ffc60f7c0ce3a8d9251e1e8c3766dac70ee138565dd2e1cc4c65db546e1b94b9`

Sayım (etiket dosyaları ve veri kapsamı; G5 / ölçü yok): {"ana": {"COL": 30, "OLUMSUZ": 8}, "c": {"DEGIL": 22, "OBEK": 3}, "c_cikarilan_ortusme": [], "veri_disi": ["PEKER_20250227"], "kesikten_tasan": ["GARFA_20260731"], "c_veri_disi": [], "ana_hisse": 33, "c_hisse": 21}

- ANA: kalibre_etiketler.csv — Cemal 18 Eylül 2026 (COL_OZET §7 'Cemal'in gözle işaretlediği 29 çöl + 8 olumsuz'; dosyada PEKER ile 30 COL, PEKER veride yok).
- C: goz_esle/etiket_2026-10-20.csv (21 kutu, 'cemal' sütunu: hepsi DEĞİL; COL_OZET §9.8 '21 kutunun HİÇBİRİ çöl değil') ve
  goz_esle/etiket_obek_ARZUM.csv (Cemal'in ARZUM öbek etiketleri: 3 OBEK, 1 DEĞİL 'düşen bıçak'). Öbek küçük ölçekli desendir (çöl değil): OBEK yakalaması
  yalnız BİLGİ. C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi): yalnız şekil ölçülür, getiri ölçülmez.
- DIŞARIDA: COL_GOZ (arastirma_cikti/col_goz/, 746 kutu, 45 ÇÖL / 105 SINIR): bu sınıflar Claude'un gözüdür ('benim'). Cemal'in 22 Ekim EVET / HAYIR kararları
  (col_goz_cemal_2024_26.csv, 150 kutu) repoda yok; ayrıca o kararlar sinyal sonrası atılıma göre verilmişti (COL_OZET §9.8). Kullanılmaz.

## Test A — G5 göze uyuyor mu
Bölge = serinin [bas, son] işlem günleri (test serisi, kesik 31.08.2026; kesikten taşan bölge kırpılır ve sayılır). G5 = VDYT2.py'deki hali (V2.v2_olculer
'durum'['G5']), değiştirilmeden; her gün yalnız o gün ve öncesine bakar. Yakaladı = bölge içi G5 gün oranı >= 0,50 (ANA); en az 1 gün (BİLGİ).
Gruplar: COL, OLUMSUZ, RASTGELE (her COL bölgesine aynı hisseden aynı uzunlukta 20 pencere; 2022-01-01 sonrası, seri başından >= 260 bar, hiçbir Cemal
etiketiyle kesişmez; tohum 20261113). Karar (nokta tahmini): G5 GÖZE UYUYOR <=> yak(COL) >= 0,70 VE >= 2 x yak(RASTGELE) VE > yak(OLUMSUZ); ZAYIF <=>
yak(COL) >= 0,50 VE > 1,5 x yak(RASTGELE); değilse UYMUYOR. Hisse kümeli bootstrap (2000, tohum 20261114) %95 aralık. G5'in geçmişi yetmeyen günleri
dedektörün kendi davranışıyla YANLIŞ (ANA); tanımlı gün oranı >= 0,50 bölgelerle yeniden hesap BİLGİ.

## Test B — basit ölçüler
10 ölçü (tanımlar sözlükte): aralik_kapanis, aralik_atr, kapanis_bant, govde_atr, uzunluk (RASTGELE ile tanım gereği eşit), dusus120, hacim_oran,
sma50_egim, dip_savunma, konum250. AUC (COL vs RASTGELE; yön tam örneklemden), hisse dışarıda bırakmalı (LOSO) AUC (yön eğitimden), COL vs OLUMSUZ
yönlü AUC. GÖZ ÖLÇÜSÜ ADAYI <=> LOSO AUC >= 0,80 VE AUC(COL vs OLUMSUZ) >= 0,70. Kural (yalnız aday varsa): aday tek başına ve aday + öteki bir ölçü (VE);
eşik COL'un %20 / %80 yüzdeliği (yöne göre); LOSO J = yakalama - yanlış alarm; iki ölçülü kural ancak J'si tekini >= 0,05 geçerse. Karmaşık model yok.

## Test C — bağımsız sağlama
B'nin seçilen kuralı tam ana setten eşikle C setine aynen uygulanır (canlı seri). C TUTTU <=> geçme(DEĞİL) <= 0,30 VE <= LOSO yakalama(COL) - 0,30;
OBEK yakalaması BİLGİ. B'de aday yoksa 'C YAPILMADI (B'de aday yok)'; G5'in C setindeki yakalaması her durumda BİLGİ.

## Grafik (gösterim, karar dışı)
3 COL bölgesi + 3 RASTGELE pencere (tohum 20261115), bölge sonundan 20 bar sonrasına kadar 250 bar, KOR_TEST v1.1 kor_ciz_fig11 (ortak log ölçek), bölge
gölgeli, G5 günleri altta; hisse adı yok; /tmp/goz_g5/grafik (repoya girmez).

## Kapı
`python GOZ_G5.py kos` ancak bu dosya git'e işlenmiş ve değişmemişse, ESIK_SHA256 ve KOD_SHA256 tutuyorsa, VDYT2.py / VDYT.py sha256'ları yukarıdakiyle
aynıysa çalışır (kod değişirse yalnız `--sapma` gerekçesiyle; gerekçe sonuca yazılır).

## Eşik sözlüğü (GOZ_ESIK)
```json
{
 "A": {
  "bilgi_en_az_gun": 1,
  "bootstrap": {
   "B": 2000,
   "guven": [
    2.5,
    97.5
   ],
   "kume": "hisse (COL, OLUMSUZ ve RASTGELE satırları hisseleriyle birlikte çekilir)",
   "tohum": 20261114
  },
  "karar": {
   "metin": "G5 GÖZE UYUYOR <=> yak(COL) >= 0,70 VE yak(COL) >= 2 x yak(RASTGELE) VE yak(COL) > yak(OLUMSUZ); ZAYIF <=> yak(COL) >= 0,50 VE yak(COL) > 1,5 x yak(RASTGELE); değilse UYMUYOR (nokta tahminleri)",
   "uyuyor": {
    "col_min": 0.7,
    "olumsuz_ustu": true,
    "rastgele_kat": 2.0
   },
   "zayif": {
    "col_min": 0.5,
    "rastgele_kat": 1.5
   }
  },
  "rastgele": {
   "bas_tarih": "2022-01-01",
   "ilk_bar": 260,
   "kural": "her COL bölgesi için aynı hisseden, aynı işlem günü uzunluğunda, başı >= bas_tarih ve >= ilk_bar, sonu <= seri sonu (test kesiği), tarih aralığı hiçbir Cemal etiketiyle (ana + C setleri, COL / OLUMSUZ / DEĞİL / OBEK) kesişmeyen pencereler; başlangıçlar uygun başlangıçlardan tekrarsız düzgün çekilir (tohum = sha256(tohum|sembol|bas)); uygun < n ise hepsi alınır (sayılır)",
   "n": 20,
   "tohum": 20261113
  },
  "yakalama_pay": 0.5
 },
 "B": {
  "aday": {
   "loso_rastgele_min": 0.8,
   "metin": "GÖZ ÖLÇÜSÜ ADAYI <=> LOSO AUC(COL vs RASTGELE) >= 0,80 VE yönlü AUC(COL vs OLUMSUZ) >= 0,70",
   "olumsuz_min": 0.7
  },
  "atr_min": 60,
  "atr_n": 250,
  "auc": "P(COL > karşı) + 0,5 P(eşit) (Mann-Whitney); NaN satır o ölçüde dışarıda",
  "dip": {
   "ayrim": 5,
   "k": 3
  },
  "dusus_min": 60,
  "dusus_n": 120,
  "hacim_min": 60,
  "hacim_n": 250,
  "konum_min": 120,
  "konum_n": 250,
  "kural": {
   "adaylar": "her aday ölçü tek başına + her aday ölçü ile öteki 9 ölçüden biri (VE)",
   "en_fazla_olcu": 2,
   "esik": "yön +1: değer >= COL'un %20 yüzdeliği; yön -1: değer <= COL'un %80 yüzdeliği (eğitim COL satırlarından)",
   "loso": "eşik ve yön dışarıdaki hisse hariç eğitimden; J = yakalama(COL) - geçme(RASTGELE), dışarıdaki hisselerde havuzlu",
   "sart": "yalnız en az bir tek ölçü aday çıkarsa",
   "secim": "en yüksek J'li tek ölçü kuralı; iki ölçülü kural ancak J'si en iyi tek ölçününkini >= 0,05 geçerse seçilir (basit önce)",
   "yuzdelik": [
    20,
    80
   ]
  },
  "loso": "her COL hissesi sırayla dışarıda: yön (+1 büyük = çöl / -1) kalan hisselerin COL vs RASTGELE AUC'sinden (>= 0,5 -> +1); dışarıdaki hissenin COL ve RASTGELE satırları yön x değer ile puanlanır; bütün dışarıdaki puanlar havuzlanıp AUC",
  "olculer": [
   "aralik_kapanis",
   "aralik_atr",
   "kapanis_bant",
   "govde_atr",
   "uzunluk",
   "dusus120",
   "hacim_oran",
   "sma50_egim",
   "dip_savunma",
   "konum250"
  ],
  "olumsuz_auc": "COL vs OLUMSUZ AUC, yön tam örneklem COL vs RASTGELE yönüyle sabit (yönlü AUC)",
  "sma": 50,
  "tanim": {
   "aralik_atr": "bölge içi medyan (H-L) / ATR250 (ATR250 = bölge başından ÖNCEKİ en çok 250 günün ortalama gerçek aralığı, en az 60 gün)",
   "aralik_kapanis": "bölge içi medyan (H-L)/Kapanış",
   "dip_savunma": "bölge içi en düşük 3 dip (Low'lar küçükten büyüğe, seçilenlerden >= 5 bar uzak olan alınır) arasındaki uzaklık (maks-min) / ATR250; 3 dip bulunamazsa NaN",
   "dusus120": "bölge başından önceki gün kapanışı / önceki 120 günün en yüksek kapanışı - 1 (en az 60 gün)",
   "govde_atr": "bölge içi medyan |C-O| / ATR250",
   "hacim_oran": "bölge medyan hacmi / bölgeden önceki 250 gün medyan hacmi (en az 60 gün, payda > 0)",
   "kapanis_bant": "(bölge maks kapanış - min kapanış) / bölge medyan kapanış",
   "konum250": "(bölge medyan kapanışı - 250 günlük min Low) / (250 günlük maks High - min Low); 250 gün bölge sonunda biter (en az 120 gün)",
   "sma50_egim": "100 x ln(SMA50[son] / SMA50[bas]) / max(son-bas, 1) (bar başına %)",
   "uzunluk": "bölge işlem günü sayısı (RASTGELE aynı uzunlukta: COL vs RASTGELE AUC tanım gereği 0,50)"
  }
 },
 "C": {
  "esik": "seçilen kuralın tam ana setten (bütün COL) eşik ve yönü, aynen",
  "g5_bilgi": "G5 yakalaması (Test A tanımı) C setinde her durumda BİLGİ olarak yazılır",
  "karar": {
   "degil_max": 0.3,
   "fark_min": 0.3,
   "metin": "C TUTTU <=> geçme(DEĞİL) <= 0,30 VE geçme(DEĞİL) <= LOSO yakalama(COL) - 0,30; değilse C TUTMADI; OBEK yakalaması BİLGİ (n küçük)"
  },
  "kriz_notu": "C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi): yalnız şekil ölçülür, getiri yok; karar dışı sayılmaz ama raporda belirtilir",
  "sart": "Test B'de seçilen kural varsa; yoksa 'C YAPILMADI (B'de aday yok)'"
 },
 "etiket": {
  "ana": {
   "dosya": "kalibre_etiketler.csv",
   "kaynak": "Cemal gözle, 18 Eylül 2026 (COL_OZET §7)",
   "siniflar": {
    "COL": "COL",
    "OLUMSUZ": "OLUMSUZ"
   }
  },
  "c": {
   "dosyalar": [
    "goz_esle/etiket_2026-10-20.csv",
    "goz_esle/etiket_obek_ARZUM.csv"
   ],
   "kaynak": "Cemal gözle, 21 Ekim 2026 (COL_OZET §9.8)",
   "ortusme": "kalibre setiyle aynı hisse ve kesişen tarihli kutu C'den çıkarılır",
   "sinif": "etiket_2026-10-20 'cemal' sütunu 'DEGIL' ile başlıyorsa DEGIL; etiket_obek_ARZUM 'cemal' 'OBEK' ile başlıyorsa OBEK, 'DEGIL' ise DEGIL"
  },
  "disarida": "COL_GOZ (arastirma_cikti/col_goz): 'benim' sınıfları Claude'un gözü; Cemal'in 150 kutuluk EVET / HAYIR dosyası repoda yok",
  "gun": "bölge = serinin [bas, son] (dahil) aralığındaki işlem günleri; hafta sonu tarihleri sorun değil; 0 gün = VERİ DIŞI (sayılır, dışarıda)"
 },
 "grafik": {
  "bar": 250,
  "cizim": "KOR_TEST v1.1 kor_ciz_fig11 (ortak log ölçek)",
  "col": 3,
  "isaret": "bölge açık sarı gölge; G5 günleri fiyat panelinin altında siyah çizgi; hisse adı / tarih / başlık yok",
  "klasor": "/tmp/goz_g5/grafik",
  "rastgele": 3,
  "sag_ek": 20,
  "secim": "COL: COL bölgelerinden tohumlu sırayla ilk 3; RASTGELE: bütün rastgele pencerelerden tohumlu sırayla ilk 3 (önce farklı hisse); kor_pencere11 penceresi (en az 120 kesintisiz bar) kurulamayan atlanır",
  "tohum": 20261115
 },
 "surum_etiket": "goz_g5_20261113",
 "vdyt2": {
  "durum": "G5",
  "fiyat_ana": "V2.v2_fiyat('BIST') test serisi (kesik 2026-08-31)",
  "fiyat_c": "V2.v2_fiyat('BIST', canli=True) (veri sonu; C seti BİLGİ)",
  "kod_sha256": "e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741",
  "tanim": "G1 küçük mum VE G2 dar bant VE (G3 tepe/dip eğimi YA DA G4 gövde savunma hattı); V2.v2_olculer, değiştirilmeden",
  "tanimsiz": "G5'in geçmişi yetmeyen günleri (ATRref / bant referansı NaN) dedektörün kendi davranışıyla YANLIŞ sayılır (ANA); tanımlı gün oranı >= 0,50 olan bölgelerle yeniden hesap BİLGİ",
  "vdyt_kod_sha256": "10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d"
 }
}
```
