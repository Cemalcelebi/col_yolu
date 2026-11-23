# GÖZ UYUM KÖR SETİ — ÖN KAYIT (Cemal işaretlemeden ÖNCE mühürlenir)

Üretim: 2026-11-23T05:20:22Z (UTC). Soru (Cemal, 23.11.2026): kodun 'dip savunması' bayrağı (Ş3) Cemal'in gözüyle örtüşüyor mu? Bu aşama getiri ÖLÇMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/goz_uyum_anahtar.json` sha256: `f6d4b18a7138860aa001d7dfc0a2fb3c57ad2064c1c497a6887171b0a34ad4d7`
- PDF: `arastirma_cikti/goz_uyum/GOZ_UYUM_KOR.pdf` sha256: `6a58038a9b160fbd04f77c26ad33d3265598cb45e878c4dc605b792348d89503`
- kod: `arastirma_cikti/goz_uyum/goz_uyum.py` sha256: `828258b1f24d45bcb683eb74172bbbdb14b2aa41b4a41560b44af0f941a3456a`
- eşik sözlüğü (GU_ESIK) sha256: `3c0c8df99d93287f009cc2b8cb4819d88f006b43054d9adea3de8cab8e239c68`
- iş tanımı: `arastirma_cikti/goz_uyum/GOZ_UYUM_IS_TANIMI.md` sha256: `4943842b6099ebd38c5dafdf6551a2e575aa26d22143400f1b6f599ff193d4f1`
- bağımlı kod: GOZ_ETIKET.py `76d5c76b3a545ed5`, YAPI_HEDEF.py `812d188c20a64e27`

## 2. Örneklem (tohum 20261123)
Olay = Y1 (S6 taban kırılımı, aynı hissede 60 bar tekil) ∧ Ş1 (F15 <= 0,25 ∧ F17 <= -0,20); P2 benzeri likidite (ABD fiyat >= 2 $, 20 gün medyan işlem değeri >= 1 mn $; AVR 1 EUR / 1 mn EUR; BIST >= 5 mn TL).
Dönem: ABD / AVR 2001-01-01..2023-06-30; BIST 2016-01-01..2017-12-31 ve 2021-03-01..2023-06-30 (Yahoo BIST kapanış sapma penceresi 27.02.2018-26.01.2021 dışı).
40 sayfa: ABD 30, AVR 5, BIST 5; tabaka Ş3 x Ş5, hücre başına 10; aynı hisseden en çok 1; sinyal günleri arası >= 30 gün; sayfa sırası rastgele.
Tabaka dağılımı (Ş3, Ş5, pazar -> sayfa): {"S3=False S5=False ABD": 7, "S3=False S5=False AVR": 2, "S3=False S5=False BIST": 1, "S3=False S5=True ABD": 8, "S3=False S5=True AVR": 1, "S3=False S5=True BIST": 1, "S3=True S5=False ABD": 7, "S3=True S5=False AVR": 1, "S3=True S5=False BIST": 2, "S3=True S5=True ABD": 8, "S3=True S5=True AVR": 1, "S3=True S5=True BIST": 1}
Notlar: []

## 3. ÖLÇÜ (önceden yazılı, değişmez)
- Model etiketi (kodun yanıtı): ANA = Ş3 (VAR = F2 >= -0,01), İKİNCİL-1 = Ş5 (VAR = F4 <= 0,25), İKİNCİL-2 = Ş3 ∧ Ş5.
- Cemal'in VAR / YOK işaretleri ile her model etiketi arasında: uyum yüzdesi ve Cohen kappa (2x2: VAR / YOK); '?' karar dışı, sayısı ayrıca yazılır; kappa'nın bootstrap %95 aralığı (B 5000, tohum 20261124, sayfa yeniden örneklemesi).
- HÜKÜM (ANA için; ikincil ikisi bilgi): kappa >= 0,60 TANIM GEÇERLİ; 0,40-0,60 KISMEN; < 0,40 TANIM GEÇERSİZ. Karar sayısı < 30 ise hüküm 'ÖLÇÜLEMEDİ' yazılır (K8).
- İKİNCİ ADIM (bu işte YAPILMAZ) kappa < 0,60 ise: Cemal'in işaretleri hedef, anahtardaki özellikler aday; her aday için tek eşikli kural (eşik = 40 sayfada VAR / YOK ayrımını en iyi yapan) ve ikinci bağımsız 40 sayfalık kör sette sınama; kappa >= 0,60 olmadan getiri ölçümü yok.
- Eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 4. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kodun bayrağı arasında uyum ölçülür) |
| K2 | geleceğe bakma | EVET | veri sinyal çağı sonunda KESİK (df.index <= pencere sonu) ve grafik her sayfada t'de kesilerek çizilir (_gu_pencere); S6 ve F1-F23 nedensel; ek özellikler dilim i + 1 ile sınırlı; test: goz_uyum.py testler komutu prefix değişmezliği |
| K3 | geçerli bar | EVET | GE.ge_hazir (YAPI_HEDEF._yh_hazir = H>L, V>0, O/H/L/C>0) geçerli bar; likidite hesabı geçerli bar dizisinde; sinyal günü p >= 130 |
| K4 | tekilleştirme | EVET | aynı hissede 60 bar tekil (_gu_isci), seçimde aynı (pazar, sembol) en çok 1 sayfa ve sinyal günleri arası >= 30 gün (gu_sec_df) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (düzeltilmiş fiyat; YAPI_HEDEF ile aynı); AVR likidite Close x Kur (EUR); oranlar birimsiz; ABD evren dışı 7 fon çıkarıldı |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); bu iş görsel uyum sınaması, getiri iddiası yok; raporda yazılı |
| K8 | örneklem ve dönem | EVET | n = 40 sayfa küçük örneklem: karar n >= 30 değilse kappa 'ÖLÇÜLEMEDİ' kuralı olc'ta uygulanır; '?' karar dışı sayılır; kappa bootstrap aralığı (B 5000) ile; hüküm eşikleri ön kayıtta sabit; dönem: ABD / AVR 2001-2023, BIST 2016-17 + 2021-23 (sapma penceresi dışı) |
| K9 | ön kayıt | EVET | GU_ESIK sha + goz_uyum.py sha + anahtar sha + PDF sha ve hüküm kuralı ön kayıtta; bu dosya Cemal işaretlemeden ÖNCE commit; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | tohum 20261123 ile anahtar aynı komutla yeniden üretilir; olc komutu anahtardan tabloyu yeniden kurar |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle (>= 0,60 / 0,40-0,60 / < 0,40) |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_GU + test; yasak dosyalar (defter, mevcut .py, kart / kart2 / kasa) değiştirilmedi (git status); e-posta taraması _yaz / _jyaz; kod değiştiyse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 5. Git kaydı (bu dosyanın yazıldığı an; commit sonrası `git log` ile doğrulanır)
- anahtar: (henüz commit yok)
