# D9_AVR — ÖN KAYIT (Ç181c devamı: sektör rüzgârı Avrupa'da)

D9_AVR v1.0 (2026-11-15): D9b sektör rüzgârı AVRUPA'da (sektor_AVR.csv 'ust'), D9_YENIDEN v1.0 + ORTAK CETVEL v1.0

- D9A_ESIK_SHA: `1ed4193a94f888f9485ff7ea5ed0b54c7938a6f89385244e443973c5a39f0101`
- D9_PARAM_SHA: `73dde4dbed813dc26779d522cbf2d74173571eabaf5f6b0ba0b72c30583e85e8`
- D9A_KOD_SHA: `c7d10777805cd9969ffe02ad56b74d2ea49faa84a5db48dd7ad45fe3e7fbc3b0`
- D9_YENIDEN_SHA: `a759d916915f2fc97f8258933fc5ce7d1b2cb8f6036691e1531e5d140c6bb80c`
- COL_V1_SHA (bilgi; kapı değil): `a575a6404810457d651339f787c0d9589ba02994bb8ab09131b2bfc5902e64e5`
- SEKTOR_AVR_SHA: `8d916a20792dd70db297483b85bbc3a06cd21597eae5f3220c5d48cde08e1175`
- ESLESME_SHA: `d8a687d4ab7391bde208bf2a7d5d11f73e7c89fb4000f5a5e6f9b7edd9fd444c`
- V_AVR_SHA: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`
- ZAMAN (UTC): `2026-11-15 11:12:46 UTC`

Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı). `kos` bu dosya, D9_AVR.py, sektor_AVR.csv, eşleme md, tercil json ve D9_YENIDEN.py git'e işlenmiş ve değişmemiş değilse, sha'lardan biri tutmazsa ya da KONTROL LİSTESİ eksikse durur. COL_v1.py sha'sı yalnız bilgidir (T8 üretim ekranı işi COL_v1'i ayrıca değiştirebilir); D9 / rüzgâr D9_YENIDEN'deki birebir kopyalarla hesaplanır ve kapı D9_PARAM == COL_v1 sabitlerini (d9_param_denetle) ayrıca denetler.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Soru

Ç181c: 'yalnız sektör rüzgârı' (RÜZGÂR VE D9 DEĞİL) ABD 2024-26'da dört şartın üçünü tuttu, ABD 2023 alt uç -0,3; AVR'de sektör listesi yoktu. Aynı sinyal, aynı cetvel, aynı eşiklerle AVR 2023 ve AVR 2024-26'da tutuyor mu? Literatür: sektör momentumu bilinen etkidir (Moskowitz-Grinblatt 1999); sonuç yeni iz sayılmaz, 'bilinen etki' etiketi taşır.

## Tanım (D9_YENIDEN v1.0'dan birebir; yalnız AVR sektör kaynağı eklendi)

```json
{
 "RUZ_BAYAT": 5,
 "RUZ_ESIK": 0.1,
 "RUZ_GERI": 60,
 "RUZ_MIN_UYE": 4,
 "RUZ_MUTLAK": 0.0,
 "UZUN_BANT": 1.5,
 "UZUN_KONUM": 0.5,
 "UZUN_MUM": 0.04,
 "UZUN_W": 250
}
```

- D9 = COL_v1 uzun_col_olc (W 250 / 125; bant <= 1,50; mum <= 0,04; konum <= 0,50). RÜZGÂR = COL_v1 sektor_ruzgar: ruz = sepet (aynı sınıfın öteki üyeleri, en az 4, eşit ağırlık, 60 bar getirisi) - piyasa (AVR taze hisselerinin 60 bar getiri MEDYANI) >= 0,10 VE sepet > 0.
- Satırlar: {"a": "D9 (uzun çöl; 12ay ya da 6ay)", "b": "D9 VE RÜZGÂR (D9b; üretim ruzgar_listesi)", "c": "RÜZGÂR VE D9 DEĞİL (rüzgârın kendi katkısı)"}
- Olay: DURUM GÜNLERİ: sinyal koşulunun t kapanışında doğru olduğu her işlem günü (t = hissenin kendi barı, yalnız t'ye kadar bilgi) OC.oc_olc'a verilir; tekilleştirme (60 gün) ve giriş (ertesi geçerli açılış) cetvelindir. Üretim ekranı (T8) durumu her gün gösterdiği için durum günü seçildi (ilk gün değil); uzun durumda ~60 günde bir olay düşer.
- Veri: OC.oc_veri temiz bar (H>L, V>0; 31.08.2026 kesik) — sinyal de bu barlarla hesaplanır (üretim ham veriyle hesaplar; K3)
- SEKTÖR SÜTUNU (sabit): sektor_AVR.csv **'ust'** = ICB süpersektör (21 sınıf: 20 ICB + 'Investment Trusts' fon sınıfı). BIST 'alt_bist' (~30 sınıf) kabalığına yakın; ABD 'endustri' daha incedir (sınıf başına daha az, daha benzer hisse). Bu fark sonuç okunurken yazılır. İkinci sütunla (ham 'sektor') ikinci koşu YOK.
- Piyasa: AVR evreninin tamamı (fonlar dahil) taze hisselerinin medyanı (COL_v1 tanımı). Fon sınıfı rüzgâr hesabına kendi sınıfı olarak girer.
- Dönemler (cetvel): [["2016-22", "2016-01-01", "2022-12-31"], ["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-08-31"]]; kriz kesiği 2026-08-31 (fiyat kesik; 60 gün penceresi aşan olay ölçülmez). Karar hücreleri: AVR 2023, AVR 2024-26; 2016-22 keşif / bilgi.
- Evren: V_AVR.pkl 581 sembol (oc_veri sonrası 580); hayatta kalma: bugün işlem görenler.

## ÖNCEDEN YAZILI KARAR (sonuç görülmeden)

- Karar satırı: (c) RÜZGÂR VE D9 DEĞİL.
- Hücre: hücre durumu ORTAK_CETVEL oc_hucre_durum == 'TUTAR' (FI dört şart: n >= 30, ort eşli fark > 0 ve ay kümeli %95 alt uç > 0, sıra > 0,50, portföy > plasebo p90; + cetvelin iki alt yarı şartı) — Ç181a/b/c ile aynı cetvel kuralı; 'tutar4' bilgi olarak yazılır.
- AVR 2023 ve AVR 2024-26 ikisi de TUTAR -> 'Ç181c EMARE GÜÇLENDİ (4 karar hücresinin 3'ü; ABD 2023 alt uç -0,3 olduğu için İZ DEĞİL, bilinen etki)'.
- biri TUTAR -> 'EMARE (değişmedi), tek pazar tek dönem'.
- hiçbiri TUTAR değil ve ikisi de TUTMADI (güç yeterli) -> 'EMARE ZAYIFLADI: rüzgâr Avrupa'da görünmüyor'.
- hiçbiri TUTAR değil ve en az biri ÖLÇÜLEMEDİ (n < 30 ya da güç yetersiz) -> 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ' (İZ DEĞİL / zayıfladı sözü güç yetersizken kullanılmaz; CLAUDE.md emin olma yolu).
- (a): satır (a) D9 AVR Ç181a'da ölçüldü (İZ DEĞİL): yalnız tutarlılık — olay sayımı D9_YENIDEN ön kaydındaki AVR (a) satırıyla AYNI beklenir; koşuda AVR 2023 / 2024-26 n D9_YENIDEN sonucuyla aynı beklenir; farklıysa HATA.
- (b): satır (b) D9 VE RÜZGÂR AVR: BİLGİ; hücre n < 1.000 ise ÖLÇÜLEMEDİ yazılır (karar değil).
- Bilgi: (c) 'Investment Trusts hariç' alt sayım ve ölçüm yalnız bilgi (karar hücresi değişmez); süre / tercil alt grupları bilgi.
- eşik, sektör sütunu ('ust') ve satır tanımları sonuca göre oynanmaz; ikinci sütunla (ham 'sektor') ikinci koşu YOK; sapma olursa SAPMA.

## SAPMA / AÇIKLAMA (sonuç görülmeden yazıldı)

- İş tanımı 'OC dört şartı' diyor; cetvelin hücre durumu 'TUTAR' dört şarta ek iki alt yarı şartını da ister (oc_hucre 'tutar'). Ç181a/b/c ile aynı cetvel kuralı kullanıldı; 'tutar4' (yalnız dört şart) raporda bilgi olarak yazılır. Karar 'TUTAR'a göredir.
- İş tanımındaki üç sonuç dalına dördüncü dal eklendi: hiçbir hücre TUTAR değil ve biri ÖLÇÜLEMEDİ ise 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ' (güç yetersizken 'zayıfladı' denmez; CLAUDE.md emin olma yolu).
- D9_YENIDEN.d9_gelecek_denetimi AVR sektörünü global sözlükten okuduğu için AVR'de rüzgârı denetleyemez; aynı mantık d9a_gelecek_denetimi olarak AVR sözlüğüyle koşar (D9_YENIDEN değişmez).
- d9_tercil.json'da AVR satırı yok (Ç181'de AVR rüzgârı yoktu): AVR tercil sınırları bu ön kayıtta, AVR RÜZGÂR durum günlerinin ruz değerlerinden (getiri yok) aynı kuralla hesaplandı ve d9_avr_tercil.json'a yazıldı.

## Sektör listesi (sektor_AVR.csv 'ust'; eşleme: sektor_AVR_eslesme.md, sha yukarıda)

| ust | üye | rüzgâr alabilir mi (öteki üye >= 4) |
|---|---|---|
| Automobiles and Parts | 11 | EVET |
| Banks | 27 | EVET |
| Basic Resources | 15 | EVET |
| Chemicals | 18 | EVET |
| Construction and Materials | 24 | EVET |
| Consumer Products and Services | 27 | EVET |
| Energy | 15 | EVET |
| Financial Services | 38 | EVET |
| Food, Beverage and Tobacco | 20 | EVET |
| Health Care | 33 | EVET |
| Industrial Goods and Services | 95 | EVET |
| Insurance | 21 | EVET |
| Investment Trusts | 77 | EVET |
| Media | 14 | EVET |
| Personal Care, Drug and Grocery Stores | 8 | EVET |
| Real Estate | 27 | EVET |
| Retail | 26 | EVET |
| Technology | 22 | EVET |
| Telecommunications | 17 | EVET |
| Travel and Leisure | 23 | EVET |
| Utilities | 23 | EVET |

- Sektörü boş sembol: 0. Fon sınıfı 'Investment Trusts': 77 sembol (işletme değil fon).

### Eşleme tablosu (ham ad -> ust)

| ham | ust | hisse (V_AVR) |
|---|---|---|
| Automobiles and Parts | Automobiles and Parts | 11 |
| Banking | Banks | 1 |
| Banks | Banks | 26 |
| Basic Resources | Basic Resources | 12 |
| Industrial Metals and Mining | Basic Resources | 2 |
| Precious Metals and Mining | Basic Resources | 1 |
| Chemicals | Chemicals | 18 |
| Construction | Construction and Materials | 1 |
| Construction & Materials | Construction and Materials | 6 |
| Construction and Materials | Construction and Materials | 16 |
| Engineering and Construction | Construction and Materials | 1 |
| Consumer Products and Services | Consumer Products and Services | 21 |
| Consumer Staples | Consumer Products and Services | 1 |
| Home Construction | Consumer Products and Services | 2 |
| Household goods & home construction | Consumer Products and Services | 1 |
| Leisure Goods | Consumer Products and Services | 1 |
| Personal Goods | Consumer Products and Services | 1 |
| Alternative Energy | Energy | 1 |
| Energy | Energy | 10 |
| Oil & Gas Producers | Energy | 3 |
| Oil, Gas and Coal | Energy | 1 |
| Financial Services | Financial Services | 34 |
| General Financial | Financial Services | 3 |
| Investment Banking and Brokerage Services | Financial Services | 1 |
| Beverages | Food, Beverage and Tobacco | 1 |
| Food Producers | Food, Beverage and Tobacco | 4 |
| Food, Beverage and Tobacco | Food, Beverage and Tobacco | 15 |
| Health Care | Health Care | 29 |
| Health Care Equipment & Services | Health Care | 1 |
| Pharmaceuticals & Biotechnology | Health Care | 2 |
| Pharmaceuticals and Biotechnology | Health Care | 1 |
| Aerospace & Defence | Industrial Goods and Services | 3 |
| Electronic & Electrical Equipment | Industrial Goods and Services | 3 |
| General Industrials | Industrial Goods and Services | 2 |
| Industrial Engineering | Industrial Goods and Services | 3 |
| Industrial Goods and Services | Industrial Goods and Services | 71 |
| Industrial Support Services | Industrial Goods and Services | 1 |
| Industrial Transportation | Industrial Goods and Services | 2 |
| Industrials | Industrial Goods and Services | 1 |
| Support Services | Industrial Goods and Services | 9 |
| Insurance | Insurance | 19 |
| Life Insurance | Insurance | 1 |
| Nonlife Insurance | Insurance | 1 |
| Collective Investments | Investment Trusts | 3 |
| Equity Investments | Investment Trusts | 3 |
| Hedge Funds | Investment Trusts | 1 |
| Investment Trusts | Investment Trusts | 70 |
| Media | Media | 14 |
| Food & Drug Retailers | Personal Care, Drug and Grocery Stores | 2 |
| Personal Care, Drug and Grocery Stores | Personal Care, Drug and Grocery Stores | 5 |
| Personal Products | Personal Care, Drug and Grocery Stores | 1 |
| Real Estate | Real Estate | 17 |
| Real Estate Investment & Services | Real Estate | 2 |
| Real Estate Investment Trusts | Real Estate | 8 |
| Retail | Retail | 15 |
| Retailers | Retail | 11 |
| Consumer Digital Services | Technology | 1 |
| Software & Computer Services | Technology | 2 |
| Software and Computer Services | Technology | 3 |
| Technology | Technology | 16 |
| Telecomms | Telecommunications | 2 |
| Telecommunications | Telecommunications | 15 |
| Travel & Leisure | Travel and Leisure | 5 |
| Travel and Leisure | Travel and Leisure | 17 |
| Travel and leisure | Travel and Leisure | 1 |
| Electricity | Utilities | 1 |
| Gas, Water & Multiutilities | Utilities | 1 |
| Utilities | Utilities | 21 |

Wikipedia tamamlamaları: ATCO-A.ST -> Industrial Goods and Services; ERIC-B.ST -> Telecommunications; BT.A.L -> Telecommunications

## Bilgi (karar dışı) alt gruplar

- Çöl süresi: aynı üç eşikle (bant, mum, konum; önceki 500 bar) W = 125 / 190 / 250: >=12 ay = 250 tutar; 9-12 = 250 tutmaz, 190 tutar; 6-9 = yalnız 125 tutar (yalnız (a) olaylarında; karar dışı)
- Rüzgâr şiddeti: ruz tercilleri: sınırlar her pazarın RÜZGÂR durum günlerinin (2016-01-01 .. 2026-08-31) ruz değerlerinin 1/3 ve 2/3 yüzdeliği, ön kayıtta sayıyla yazılır; (b) ve (c) olaylarına aynı sınırlar; karar dışı
- AVR tercil sınırları (ruz, sonuç görülmeden): AVR: 0.1190 / 0.1531
- (c) 'Investment Trusts hariç': (c) tekil olaylarından fon sembolleri çıkarılarak (bilgi).

## K6 veri denetimi: günlük kapanış oranı >= 1,8 ya da <= 1/1,8 (temiz barlar; getiri ölçüsü değil)

18 gün: AMRQ.L 2021-02-10 x0.553, AVON.L 2021-11-12 x0.487, DOCM.SW 2025-05-05 x0.493, ELM.L 2020-03-19 x2.237, ELUX-B.ST 2026-05-19 x0.542, FGP.L 2020-03-16 x0.522, GDWN.L 2026-03-23 x0.522, HOLN.SW 2025-06-16 x0.516, ORSTED.CO 2025-09-08 x0.551, PTEC.L 2025-05-08 x0.403, ROSE.L 2025-06-11 x0.543, VIV.PA 2024-12-09 x0.222, VPLAY-B.ST 2023-06-05 x0.373, VPLAY-B.ST 2023-07-20 x0.513, VPLAY-B.ST 2023-12-01 x0.256, VPLAY-B.ST 2024-01-16 x2.734, WLN.PA 2023-10-25 x0.408, XPP.L 2023-10-02 x0.482. 100x birim kayması yok; bölünme / şirket ayrılması / sermaye artırımı sıçramaları düzeltilmedi (sinyal tanımı değişmez; BIST / ABD ile aynı işlem).

## OLAY SAYIMI (getiri hesaplanmadan)

| Satır | Pazar | durum günü 2016-22 / 2023 / 2024-26 | OLAY (cetvel sonrası, girişe göre) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |
|---|---|---|---|---|---|
| a | AVR | 227259 / 70100 / 140717 | 4023 / 1102 / 2264 | 356730 | 73777 |
| b | AVR | 7368 / 1616 / 4134 | 420 / 110 / 218 | 11279 | 1091 |
| c | AVR | 25298 / 3084 / 13959 | 1214 / 125 / 509 | 35580 | 5871 |

(b) / (c) 'Investment Trusts hariç' olay sayımı (girişe göre dönem 2016-22 / 2023 / 2024-26; bilgi):

- (b) hariç: 420 / 110 / 218; fon olayı: 0 / 0 / 0
- (c) hariç: 1214 / 125 / 509; fon olayı: 0 / 0 / 0

Süre sınıfları ve tercil sayıları (olay, girişe göre dönem):

```json
{
 "a": {
  "AVR": {
   "sure": {
    "6-9": {
     "2016-22": 1500,
     "2023": 242,
     "2024-26": 453
    },
    "9-12": {
     "2016-22": 630,
     "2023": 184,
     "2024-26": 224
    },
    ">=12": {
     "2016-22": 1893,
     "2023": 676,
     "2024-26": 1587
    }
   }
  }
 },
 "b": {
  "AVR": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 307,
     "2023": 80,
     "2024-26": 169
    },
    "T2 orta": {
     "2016-22": 72,
     "2023": 28,
     "2024-26": 28
    },
    "T3 güçlü": {
     "2016-22": 41,
     "2023": 2,
     "2024-26": 21
    }
   }
  }
 },
 "c": {
  "AVR": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 928,
     "2023": 89,
     "2024-26": 400
    },
    "T2 orta": {
     "2016-22": 150,
     "2023": 29,
     "2024-26": 56
    },
    "T3 güçlü": {
     "2016-22": 136,
     "2023": 7,
     "2024-26": 53
    }
   }
  }
 }
}
```

## GÜÇ ÖN BİLGİSİ (getiri yok; cetvel güç tablosu guc_tablosu.json, δ = +%5, OC.oc_guc_bak; hücre n'i r60 / eş düşmesiyle olay sayısından biraz küçük olabilir)

| Satır | Hücre | olay | güç (δ +%5) | 'TUTMADI' yazılabilir mi (n >= 1.000 ya da güç >= %80) |
|---|---|---|---|---|
| b | AVR 2023 | 110 | 29.0% | HAYIR: TUTAR değilse ÖLÇÜLEMEDİ |
| b | AVR 2024-26 | 218 | 29.0% | HAYIR: TUTAR değilse ÖLÇÜLEMEDİ |
| c | AVR 2023 | 125 | 29.0% | HAYIR: TUTAR değilse ÖLÇÜLEMEDİ |
| c | AVR 2024-26 | 509 | 51.5% | HAYIR: TUTAR değilse ÖLÇÜLEMEDİ |

Sonuç görülmeden not: (c) iki karar hücresinde de güç yetersizse karar kuralının 'EMARE ZAYIFLADI' dalına ulaşılamaz; olası sonuçlar GÜÇLENDİ / değişmedi (tek hücre TUTAR) / 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ'. Eşik ve kural bu yüzden değiştirilmez.

(a) tutarlılık (D9_YENIDEN ön kaydı AVR (a) satırı ile): **AYNI** — D9_YENIDEN {'durum_gunu': {'2016-22': 227259, '2023': 70100, '2024-26': 140717}, 'olay': {'2016-22': 4023, '2023': 1102, '2024-26': 2264}, 'tekil': 356730, 'havuz_disi': 73777}, D9_AVR {'durum_gunu': {'2016-22': 227259, '2023': 70100, '2024-26': 140717}, 'olay': {'2016-22': 4023, '2023': 1102, '2024-26': 2264}, 'tekil': 356730, 'havuz_disi': 73777}

Kural: bir hücrede n < 30 ise ÖLÇÜLEMEDİ yazılır, 'iz değil' denmez (cetvel oc_hucre_durum).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc (D9_YENIDEN.d9_olc_satir): aynı giriş günü, aynı pazar (AVR), 60 gün momentum beşliği x 20 gün likidite (EUR, Kur sütunu) üçlüsü, aynı açılış girişi / 60. gün çıkışı; 200 plasebo portföy. Mekanik üstünlük: (c) rüzgâr SEKTÖR momentumudur; hisse momentumu eşlenir, sektör momentumu eşlenmez -> sonuç 'bilinen etki' (Moskowitz-Grinblatt 1999) okunur, yeni iz sayılmaz |
| K2 | geleceğe bakma | EVET | D9 t'ye kadar barlarla (rolling, geriye), rüzgâr t'ye kadar kapanışlarla; kos d9a_gelecek_denetimi 30 rastgele olayda seriyi t'de keser, COL_v1 kopyası (d9_uzun_ref / d9_ruzgar_ref) AVR sektör sözlüğüyle aynı D9 / ruz değerini mekanik denetler; test_d9_avr 'geleceğe bakma'. SINIR: sektor_AVR.csv BUGÜNÜN listesi (Wikipedia 2026 bileşenleri ve bugünkü ICB sınıfı), karar günündeki sektör değil; sınıf değişimi nadir ama etiket sabit varsayılır (K7 ile birlikte yazılır) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz bar (H>L, V>0, O/H/L/C > 0, 31.08.2026 kesik) üzerinden sinyal ve rüzgâr paneli; geçersiz bar olay günü olamaz (cetvel 'sinyal barı geçersiz' sayımı) |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücre tablosunda medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); sinyal t kapanışında |
| K6 | veri birimi | EVET | tek kip V_AVR.pkl (fi_k1_veri düzeltilmiş, yerel para; .L peni); rüzgâr ve D9 oranlardan (birimden bağımsız); likidite EUR (Kur). Ön kayıtta günlük >= 1,8x sıçrama listesi (temiz barlarda 18 gün, 100x birim kayması YOK; bölünme / şirket ayrılması örn. VIV.PA 09.12.2024, HOLN.SW 16.06.2025) yazılı; düzeltilmez (sinyal tanımı değişmez; BIST / ABD ile aynı işlem), sepet ortalamasını 60 gün etkileyebilir -> sınır olarak raporda |
| K7 | hayatta kalma | EVET | evren BUGÜN işlem gören STOXX 600 + FTSE 250 üyeleri (581 sembol); batan / endeksten çıkan YOK -> getiriler yukarı, -%50 olasılığı aşağı yanlı okunur; sektör etiketi de bugünkü (K2 notu). Büyük hisselerde yanlılık küçük (CLAUDE.md) |
| K8 | örneklem ve dönem | EVET | AVR x 3 dönem (2016-22 keşif bilgi; 2023, 2024-26 karar); n < 30 ÖLÇÜLEMEDİ; İZ DEĞİL / zayıfladı yalnız güç yeterliyken; 3 satır, tek sektör sütunu (ikinci koşu yok); olay sayımı ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | D9A_ESIK (eşleme dahil) sha, D9_PARAM sha, D9_AVR.py / D9_YENIDEN.py sha (COL_v1.py sha bilgi), sektor_AVR.csv + eşleme md sha, V_AVR.pkl sha, cetvel üç sha ön kayıtta; kos IZ_KARNE.ik_kontrol_kapisi + OC.oc_kapi + d9a_onkayit_dogrula (git işlenmiş / değişmemiş; sha eşit) geçmezse durur; karar kuralı sonuçtan önce yazılı |
| K10 | ayrıştırma | EVET | ayrıştırma: Wikipedia bileşen listesi (islenmis-veri avr/evren_avr_ham.csv) -> sektör; 3 boş sektör Wikipedia STOXX Europe 600 satırından elle doğrulandı (D9A_WIKI); her ham ad tek ust'a (D9A_ESLESME; test); rastgele 3 satır elle denetlendi (rapor); haber / kurum etiketi maddeleri uygulanmaz (metin yok). SINIR: FTSE 250 etiketleri isimden: bazı fonlar 'Financial Services' / 'Energy' etiketli (3IN, INPP, SEQI, SOI, PPET, GCP, VEIL, VOF, SEIT), Man Group 'Investment Trusts' etiketli; etikete dokunulmadı (eşleme md) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/d9_avr/olay_<satır>.csv.gz + durum.csv.gz; hücre özeti arastirma_cikti/d9_avr/d9_avr_hucre.csv; >= 2 hücre bağımsız denetçi tarafından yeniden üretilir (ana model işi) |
| K12 | ifade | EVET | etiketler yalnız oc_hucre_durum / oc_etiket ve önceden yazılı karar kuralı; 'bilinen etki' etiketi; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_d9a; D9_YENIDEN / ORTAK_CETVEL / COL_v1 / IZ_KARNE / defterler yalnız okunur (git status denetimi); D9_YENIDEN.D9_ESIK kalıcı değişmez (derin kopya; test); e-posta / anahtar taraması testte; ücretli veri yok (Wikipedia + islenmis-veri) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm (T8 üretim ekranı kararı Cemal'in) |

## Test

`python test_d9_avr.py` (sektor_AVR.csv V_AVR ile birebir ve eşleme tutarlı; sentetik AVR akışı b / c boş değil; D9_YENIDEN BIST / ABD / AVR davranışı değişmedi; kontrol kapısı eksik satırda durur; e-posta / anahtar taraması) ve `python test_d9_yeniden.py` (değişmeden geçer).
