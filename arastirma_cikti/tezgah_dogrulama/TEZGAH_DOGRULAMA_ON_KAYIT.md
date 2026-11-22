# TEZGÂH DOĞRULAMA — ÖN KAYIT (2026-11-22 10:16:56 UTC)

Sürüm: TEZGAH_DOGRULAMA v1.0 (2026-11-22). İş tanımı: arastirma_cikti/tezgah_dogrulama/TEZGAH_DOGRULAMA_IS_TANIMI.md (sha 6dc4e7bba0826a6ecfd8432262a07d4c74c22f6160034bb9a3f8e1dae7b3734f).
Kod: TEZGAH_DOGRULAMA.py git e624a120495991a3cb7e61544ac8513bd4406724 2026-11-22T10:16:54+00:00. Bu dosya koşudan ÖNCE commit edilir; td_kapi git kaydını, değişmemişliği, sha'ları ve kontrol tablosunu denetler. İz aranmaz; yalnız doğrulama. Bizim seriler henüz HESAPLANMADI (referans indirildi ve ayrıştırıldı; bizim panel / portföy koşusu ön kayıttan sonra).

## 1. HÜKÜM KURALI (iş tanımından AYNEN)

TEZGÂH DOĞRU (o seri için) = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa serisi için korelasyon >= 0,90); KISMEN = 0,40-0,70; UYUŞMUYOR = < 0,40 -> neden araştırılır (evren farkı: büyük-likit yaşayan hisseler; onluk tanımı; ağırlık; veri hatası) ve tek tek sınanır (ör. yalnız en büyük 500 hisse; yalnız French'in değer ağırlıklı serisi).

Yorum (kodda): korelasyon = Pearson; DOĞRU eşiği (0,70 / piyasa 0,90) geçilip işaret uyumu < %70 ise KISMEN; piyasa serisinde 0,40-0,90 KISMEN; n < 36 ay ÖLÇÜLEMEDİ; onluk seviye serileri (D1..D10) piyasa benzeri sayılır (0,90).

## 2. SONUÇ KURALI (tek cümle)

(1) ABD ana çiftlerinin (A1-A8) hepsi DOĞRU ise 'tezgâh yayımlanmış seriyi izliyor'; biri UYUŞMUYOR ise 'tezgâhta / evrende fark var' (teşhis tablosuna bakılır); aksi 'kısmen izliyor'. (2) Dönem: French Mom ve ST_Rev 2016-23 ortalamasının t'si |t| < 2 ise 'yayımlanmış veride de bu dönemde sıfırdan ayrışmıyor (dönemin gerçeği)'; t >= 2 iken bizimki < 2 ise 'evren farkı'. Tek cümle bu iki parçadan kurulur.

## 3. ÇİFTLER (önceden yazılı)

| kod | bizim seri | referans | piyasa | açıklama |
|---|---|---|---|---|
| A1 | `ABD · havuz · r · PIYASA · - · EW` | `US_EWMKT` | E | ABD evren getirisi EW vs French EW piyasa (Prior_12_2 EW onlukları, firma ağırlıklı) |
| A2 | `ABD · havuz · r · PIYASA · - · LQ` | `US_MKT` | E | ABD evren getirisi LQ vs French piyasa (Mkt-RF + RF, VW) |
| A3 | `ABD · havuz · r · MOM · D10-D1 · EW` | `US_P12_EW_FARK` | H | ABD MOM onluk üst - alt EW vs French Prior_12_2 EW Hi - Lo |
| A4 | `ABD · havuz · r · MOM · D10-D1 · LQ` | `US_P12_VW_FARK` | H | ABD MOM onluk üst - alt LQ vs French Prior_12_2 VW Hi - Lo |
| A5 | `ABD · havuz · r · MOM · 2X3 · LQ` | `US_MOM` | H | ABD MOM 2x3 (üst 30 - alt 30) LQ vs French Mom |
| A6 | `ABD · havuz · r · STREV · D1-D10 · EW` | `US_P1_EW_FARK` | H | ABD STREV onluk alt - üst EW vs French Prior_1_0 EW Lo - Hi |
| A7 | `ABD · havuz · r · STREV · D1-D10 · LQ` | `US_P1_VW_FARK` | H | ABD STREV onluk alt - üst LQ vs French Prior_1_0 VW Lo - Hi |
| A8 | `ABD · havuz · r · STREV · 2X3 · LQ` | `US_STREV` | H | ABD STREV 2x3 (alt 30 - üst 30) LQ vs French ST_Rev |
| E1 | `AVR · havuz · r · PIYASA · - · LQ` | `EU_MKT` | E | AVR evren getirisi LQ (USD) vs French Avrupa piyasa (USD) |
| E2 | `AVR · havuz · r · PIYASA · - · EW` | `EU_MKT` | E | AVR evren getirisi EW (USD) vs French Avrupa piyasa (USD) |
| E3 | `AVR · havuz · r · MOM · 2X3 · LQ` | `EU_WML` | H | AVR MOM 2x3 LQ (USD) vs French Avrupa WML |
| E4 | `AVR · havuz · r · MOM · D10-D1 · EW` | `EU_WML` | H | AVR MOM onluk üst - alt EW (USD) vs French Avrupa WML |

Teşhis sürümleri (her ana çift için, hükümden bağımsız hep hesaplanır): her ana çift için ÖNCEDEN yazılı ve hükümden bağımsız HER ZAMAN hesaplanan sürümler: (a) maske 'buyuk' (ABD ilk 500 / AVR ilk 200 Lq); (b) maske 'tum'; (c) EW <-> LQ ve French EW <-> VW çaprazı; (d) OS kipi getiri r_os; (e) AVR EUR (kur çevirimsiz).
Bilgi: ABD MOM ve STREV onluk seviyeleri D1..D10 (EW vs French EW, LQ vs French VW; piyasa eşiği).

## 4. TANIMLAR (TD_ESIK)

```json
{
 "surum": "TD1.0",
 "kesik": "2023-12-31",
 "yahoo_son": "2023-12-29",
 "pencere": {
  "karsilastirma": [
   "2016-01",
   "2023-12"
  ],
  "ref_eski": [
   "2000-01",
   "2015-12"
  ],
  "ref_yeni": [
   "2016-01",
   "2023-12"
  ],
  "alt": {
   "d1": [
    "2016-01",
    "2019-12"
   ],
   "d2": [
    "2020-01",
    "2023-12"
   ]
  },
  "tarih": "TUTMA ayı (getirinin ölçüldüğü ay)"
 },
 "french": {
  "kok": "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/",
  "dosya": [
   "F-F_Research_Data_Factors_CSV.zip",
   "F-F_Momentum_Factor_CSV.zip",
   "F-F_ST_Reversal_Factor_CSV.zip",
   "10_Portfolios_Prior_12_2_CSV.zip",
   "10_Portfolios_Prior_1_0_CSV.zip",
   "Europe_3_Factors_CSV.zip",
   "Europe_Mom_Factor_CSV.zip"
  ],
  "eksik": [
   -99.99,
   -999.0
  ],
  "birim": "yüzde -> ondalık (/100); firma sayısı ham",
  "tanim": "ABD: CRSP (NYSE / AMEX / NASDAQ), onluklar NYSE kırılımıyla, Mom ve ST_Rev 2x3 (NYSE medyan büyüklük x 30/70 önceki getiri) değer ağırlıklı; EW piyasa = Prior_12_2 eşit ağırlıklı onlukların firma sayısıyla ağırlıklı ortalaması (o ay sıralamaya giren bütün hisselerin eşit ağırlıklı getirisi); Avrupa: 16 gelişmiş Avrupa ülkesi, USD"
 },
 "yedek": {
  "fon": [
   "SPY",
   "RSP",
   "IWM",
   "MTUM",
   "VLUE",
   "USMV",
   "VGK"
  ],
  "kosul": "French dosyalarından biri bile açılmazsa o referans yerine fon vekili (MTUM - SPY momentum; RSP eşit ağırlıklı piyasa); French açıldıysa indirilmez"
 },
 "yahoo": {
  "hisse": [
   "AAPL",
   "MSFT",
   "AMZN",
   "GOOGL",
   "META",
   "NVDA",
   "JPM",
   "XOM",
   "JNJ",
   "PG",
   "V",
   "UNH",
   "HD",
   "CVX",
   "KO",
   "PEP",
   "MRK",
   "WMT",
   "BAC",
   "CSCO",
   "INTC",
   "PFE",
   "T",
   "VZ",
   "DIS",
   "ORCL",
   "ABBV",
   "COST",
   "MCD",
   "NKE"
  ],
  "e2_sayi": 20,
  "kur": "EURUSD=X",
  "bas": "2015-01-01",
  "tanim": "yfinance download(auto_adjust=False, günlük), Close ve Adj Close; E2 = listedeki sırayla bizim evrende olan ilk 20"
 },
 "bizim": {
  "panel": "OS.os_veri + OS.os_panel (kova sınırları olcu_sinama/os_sinir.json) + OS.os_kart_sinyal: ay sonu t = birleşik takvimde ayın son günü, hissenin t'de geçerli barı; MOM = C_{k-21} / C_{k-252} - 1 (12-1), STREV = C_k / C_{k-21} - 1 (önceki ay); havuz = giriş günü (t'den sonraki ilk geçerli bar) OS havuzunda (ok ve H >= 0)",
  "getiri": {
   "r": "AY KAPANIŞI: tutma ayı m+1'deki son geçerli kapanış / t kapanışı - 1 (French gibi kapanıştan kapanışa); AVR: kapanış x Kur (EUR) x EURUSD (ay son kuru) = USD (French Avrupa USD)",
   "r_os": "OS klasik kipi: t+1 açılış E0, 21. geçerli barın kapanışı / E0 - 1 (OS.os_olcu_hesap H 21; yerel para); bilgi"
  },
  "agirlik": {
   "EW": "eşit",
   "LQ": "Lq (OS paneli: C x V x Kur önceki 20 günün medyanı, t dahil) ile ağırlıklı = piyasa değeri yok, işlem değeri vekili"
  },
  "onluk": "t kesitinde maske VE sinyal sonlu hisseler arasında rank(first, pct) (sembol sırası); onluk = ceil(pct x 10); sıralama getiriden ÖNCE (getirisi olmayan hisse sıralamada kalır, portföy ortalamasına girmez)",
  "iki_uc": "2x3: büyüklük = Lq maske kesiti medyanının üstü / altı; sinyal pct <= 0,30 alt, > 0,70 üst; altı portföy LQ ağırlıklı; faktör = (küçük üst + büyük üst) / 2 - (küçük alt + büyük alt) / 2 (STREV: alt - üst); 'U30A30_EW' = eşit ağırlıklı üst %30 - alt %30",
  "maske": {
   "havuz": "OS havuzu (birincil)",
   "tum": "havuz şartı yok (t'de geçerli bar, sinyal sonlu)",
   "buyuk": "havuz VE t kesitinde Lq sırası ilk N (ABD 500, AVR 200)"
  },
  "buyuk_n": {
   "ABD": 500,
   "AVR": 200
  }
 },
 "karsilastir": {
  "olcu": "Pearson (hüküm) ve Spearman korelasyonu, eğim b (bizim = a + b x referans, EKK), işaret uyumu payı (aynı ay aynı işaret; sıfır = uyumsuz), ortalama ve t (ort / (sd / kök n)) ikisi için; en çok ayrışan 10 ay = |bizim - referans| en büyük",
  "n_min": 36
 },
 "hukum": {
  "metin": "TEZGÂH DOĞRU (o seri için) = korelasyon >= 0,70 ve işaret uyumu >= %70 (piyasa serisi için korelasyon >= 0,90); KISMEN = 0,40-0,70; UYUŞMUYOR = < 0,40 -> neden araştırılır (evren farkı: büyük-likit yaşayan hisseler; onluk tanımı; ağırlık; veri hatası) ve tek tek sınanır (ör. yalnız en büyük 500 hisse; yalnız French'in değer ağırlıklı serisi).",
  "yorum": "korelasyon = Pearson; DOĞRU eşiği (0,70 / piyasa 0,90) geçilip işaret uyumu < %70 ise KISMEN; piyasa serisinde 0,40-0,90 KISMEN; n < 36 ay ÖLÇÜLEMEDİ; onluk seviye serileri (D1..D10) piyasa benzeri sayılır (0,90)",
  "dogru": 0.7,
  "dogru_piyasa": 0.9,
  "isaret": 0.7,
  "kismen": 0.4
 },
 "teshis": "her ana çift için ÖNCEDEN yazılı ve hükümden bağımsız HER ZAMAN hesaplanan sürümler: (a) maske 'buyuk' (ABD ilk 500 / AVR ilk 200 Lq); (b) maske 'tum'; (c) EW <-> LQ ve French EW <-> VW çaprazı; (d) OS kipi getiri r_os; (e) AVR EUR (kur çevirimsiz)",
 "sonuc": {
  "kural": "(1) ABD ana çiftlerinin (A1-A8) hepsi DOĞRU ise 'tezgâh yayımlanmış seriyi izliyor'; biri UYUŞMUYOR ise 'tezgâhta / evrende fark var' (teşhis tablosuna bakılır); aksi 'kısmen izliyor'. (2) Dönem: French Mom ve ST_Rev 2016-23 ortalamasının t'si |t| < 2 ise 'yayımlanmış veride de bu dönemde sıfırdan ayrışmıyor (dönemin gerçeği)'; t >= 2 iken bizimki < 2 ise 'evren farkı'. Tek cümle bu iki parçadan kurulur."
 },
 "e1": {
  "tanim": "ABD (AVR bilgi): hissenin ardışık iki geçerli barı (birleşik takvimde <= 5 gün arayla), gün t OS havuzunda (ok); gece = O_t / C_{t-1} - 1, gün içi = C_t / O_t - 1 (O: OS açılış kırpması sonrası); gün başına kesit ortalaması (EW ve LQ), yıl başına gün ortalaması (baz puan) ve yıllık toplam (%); beklenen: gece > 0, gün içi ~ 0 (bilgi)"
 },
 "e2": {
  "tanim": "20 hisse: bizim ay kapanışı getirisi (os_veri Close) ile Yahoo Adj Close ve Close ay sonu getirisi, 2016-01..2023-12; Pearson >= 0,99 beklenir; ort fark (bizim - Adj) ~0 ise bizim kapanış temettü ayarlı, ~ -temettü verimi ise yalnız bölünme ayarlı",
  "esik": 0.99
 },
 "yeniden": {
  "seri": [
   "ABD|tum|r|MOM|D10-D1|EW",
   "ABD|tum|r|PIYASA|-|EW"
  ],
  "ay": [
   "2017-03",
   "2020-04",
   "2023-06"
  ],
  "tanim": "ham V_ABD.pkl'den düz pandas (OC / OS kodu kullanmadan): geçerli bar süzgeci, K55 fon listesi dışı, birleşik takvim ay sonu, MOM kendi bar indeksiyle, rank(first, pct) sembol sırası, ceil onluk, ay kapanışı getirisi; fark < 1e-9 TUTAR"
 }
}
```

## 5. REFERANS KAYNAK VE ERİŞİM

İndirme zamanı 2026-11-22 10:16:05 UTC; yedek: kullanılmadı (French açıldı).

| dosya | durum | bayt | sha256 |
|---|---|---|---|
| F-F_Research_Data_Factors_CSV.zip | açıldı | 13078 | `b03d39e4bb253dda0f14893db3b78e64b40b8d6549a0fc0fd4111dae84c98618` |
| F-F_Momentum_Factor_CSV.zip | açıldı | 5603 | `27ed60e5b2caa9ea334a261cddfa864a9926f6bf45e9677c95dfd835c5abb315` |
| F-F_ST_Reversal_Factor_CSV.zip | açıldı | 5576 | `7ddb68bbaa507ec0b298ceaecf99e719ef051367d93de3d1f89150e3fbb61740` |
| 10_Portfolios_Prior_12_2_CSV.zip | açıldı | 119215 | `688467caa28578a8dca70698537c4f03c406b246350b6f3e9c396e15e1e7964f` |
| 10_Portfolios_Prior_1_0_CSV.zip | açıldı | 120824 | `9c82ae7be156e5958933b4c8b2a5c54d61191f02477f067929ff7b72f0127893` |
| Europe_3_Factors_CSV.zip | açıldı | 4993 | `842332540d9c86681cbda628c6acc9d75d0c1563e364a2bf6a535072f651471e` |
| Europe_Mom_Factor_CSV.zip | açıldı | 2247 | `ac254c7011515cc8b3c280dbe374fe8d05b6c5a5603cd7b17101c9fb2e3bdaa0` |

Yahoo (E2 hisseleri + EURUSD=X): açıldı; sembol 31; en geç 2023-12-29; eksik [].

Referans serileri (kesik 2023-12): US_MKT 1926-07..2023-12; US_RF 1926-07..2023-12; US_MOM 1927-01..2023-12; US_STREV 1926-02..2023-12; US_P12_VW_D1 1927-01..2023-12; US_P12_EW_D1 1927-01..2023-12; US_P12_VW_D2 1927-01..2023-12; US_P12_EW_D2 1927-01..2023-12 ...

## 6. SHA

| ad | sha256 |
|---|---|
| TD_ESIK_SHA | `06ea1b28181158116ad903240c844ea28c0798a534dcb1d1c977ab2d94cfdffd` |
| TD_KOD_SHA | `5e4e374fed70a7f4bde5d16233108c2b3722da3f41f261ad64e2684cb98fff4a` |
| OS_KOD_SHA | `86c8402136e0b77f9e95d5f75556251728ae48f59647cc6f97d91cf38eead087` |
| OC_KOD_SHA | `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` |
| KASA_KOD_SHA | `3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b` |
| IS_TANIMI_SHA | `6dc4e7bba0826a6ecfd8432262a07d4c74c22f6160034bb9a3f8e1dae7b3734f` |
| OS_SINIR_SHA | `fefc82566205194f00ea80882523b111d4d0414575db21943ef6ba523e4bb506` |
| V_ABD_SHA | `7c343a5dcbb96d6d33a22096b48d6fb7223b6a7c0ae6eaaf43002193d9810c91` |
| V_AVR_SHA | `349ac0b0ec7bb2ff5498e6f8fb876a9e5bdcd3a9b88b11807ab7976a4f5f0830` |
| REF_KESIK_SHA | `61e94bdc781e6835474958848b631d6f1af0653b67ac61ba52b5c6ce903021fd` |
| YAHOO_KESIK_SHA | `6cd3d321d6a0e3c339b90176c1e798cd49a773b677641b636ef84d6d35a3a82b` |

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | iz / sinyal sınaması yok; doğrulama: bizim aylık portföy serileri = yayımlanmış referans serilerle ay ay; 'kontrol grubu' yerine dış referans (French); eş kurulumu kullanılmaz |
| K2 | geleceğe bakma | EVET | sıralama t kapanışında bilinenle (MOM C_{k-21}/C_{k-252}, STREV C_k/C_{k-21}, Lq t dahil önceki 20 gün); getiri t+1 ayında; onluk sırası getiriden önce; KASA kapısı hisse pkl + referans kesik pkl (2023-12-31); referans 2023-12 sonrası atılır |
| K3 | geçerli bar | EVET | OS.os_veri -> OC.oc_veri_hazirla geçerli bar (O/H/L/C > 0, H > L, V > 0); ay sonu t'de geçerli bar şartı (os_kart_sinyal) |
| K4 | tekilleştirme | UYGULANMAZ | olay yok; ay başına bir portföy getirisi (aylık seri, n = ay); tekrar sayım yok |
| K5 | giriş fiyatı | EVET | birincil getiri French ile aynı kip (ay kapanışından ay kapanışına); OS kipi (t+1 açılış) ayrıca r_os olarak raporlanır |
| K6 | veri birimi | EVET | V_*.pkl tek kip; E2 ile Yahoo Adj Close / Close'a karşı kip ölçülür; AVR Kur (yerel -> EUR) x EURUSD = USD (French Avrupa USD); French yüzde -> ondalık, -99,99 / -999 eksik |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): seviye getirileri yukarı yanlı, alt onluklar (MOM alt, STREV alt) yukarı yanlı -> MOM farkı aşağı, STREV farkı yukarı yanlı okunur; raporda yazılı; teşhis 'buyuk' maskesi |
| K8 | örneklem ve dönem | EVET | 96 tutma ayı (MOM ABD ~90); n < 36 ay ÖLÇÜLEMEDİ; iki alt dönem (2016-19, 2020-23) ayrı; referans 2000-15 vs 2016-23 |
| K9 | ön kayıt | EVET | TD_ESIK sha + kod sha + git commit, referans dosya sha'ları ön kayıtta; sıra kod commit -> ön kayıt commit -> koşu; td_kapi ön kaydın işlenmiş + değişmemiş + sha eşit + ik_kontrol_kapisi; hüküm kuralı iş tanımından aynen |
| K10 | ayrıştırma | EVET | French CSV ayrıştırma: bölüm başlığı + 6 haneli ay satırı; sütun sayısı başlıkla eşit; ham dosyadan rastgele 3 satır elle (rapor) ve test_tezgah_dogrulama; yıllık (4 haneli) satırlar alınmaz |
| K11 | yeniden üretim | EVET | td_yeniden: iki seri x 3 ay ham pkl'den düz pandas (OC / OS kodu yok); French 3 satır ham metinden |
| K12 | ifade | EVET | iz iddiası yok; hüküm yalnız önceden yazılı eşikle; sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_td; test); OS / OC / KASA / defter / kart / kasa / tezgah2 dosyalarına dokunulmadı; dış istek yalnız French + Yahoo (kimlik yok, Tiingo yok); e-posta / anahtar taraması (_td_yaz) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; tezgâh doğrulaması |
