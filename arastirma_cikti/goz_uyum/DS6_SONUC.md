# DİP SAVUNMASI v6 (DS6) — SONUÇ (iki kör set, 80 sayfa)

Üretim: 2026-11-23T19:42:36Z (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: 2026-11-23T19:42:35Z (UTC). Mühür denetimi: ds6_anahtar.json, ds6.py, ds5.py, DS6_ESIK, kural kaynağı, DS6_ONAY.pdf ve ds6_onay_anahtar.json sha'ları DS6_ON_KAYIT ile aynı; 80 sayfanın P1-P5, D2 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.

Karar: birleşik 79 (Cemal VAR 30); işaretsiz / '?' (karar dışı): 1 ['set 2 / 39'].

## HÜKÜM (V1, ön kayıttaki eşikle): **GEÇERSİZ** — birleşik kappa 0.036, %95 [-0.121, 0.221]

Sınır: düzeltme Cemal'in DS5_ONAY işaretlerinden yapıldı ve iki set önceki DS3-DS5 işlerinde kullanıldı; sonuç YARI BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in görsel onayı (DS6_ONAY.pdf) + üçüncü bağımsız kör setle.

NOT: V1 kappa set 1 0.079, set 2 -0.006: İKİ SETTE DE < 0,40.

## Kappa tablosu

| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |
|---|---|---|---|---|---|---|---|---|
| V1 | set 1 | 40 | 4 | 0.650 | 0.079 | [-0.149, 0.336] | [-0.193, 0.414] | ayrı rapor |
| V1 | set 2 | 39 | 5 | 0.564 | -0.006 | [-0.237, 0.235] | [-0.281, 0.289] | ayrı rapor |
| V1 | birleşik | 79 | 9 | 0.608 | 0.036 | [-0.121, 0.221] | [-0.155, 0.261] | GEÇERSİZ |
| V2 | set 1 | 40 | 6 | 0.700 | 0.241 | [-0.046, 0.536] | [-0.119, 0.610] | bilgi |
| V2 | set 2 | 39 | 5 | 0.564 | -0.006 | [-0.237, 0.235] | [-0.281, 0.289] | bilgi |
| V2 | birleşik | 79 | 11 | 0.633 | 0.112 | [-0.067, 0.306] | [-0.105, 0.351] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| V3 | set 1 | 40 | 8 | 0.700 | 0.268 | [-0.036, 0.565] | [-0.100, 0.637] | bilgi |
| V3 | set 2 | 39 | 12 | 0.590 | 0.119 | [-0.188, 0.421] | [-0.248, 0.477] | bilgi |
| V3 | birleşik | 79 | 20 | 0.646 | 0.196 | [-0.017, 0.406] | [-0.065, 0.445] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| GOVDE_1 | set 1 | 40 | 23 | 0.675 | 0.378 | [0.115, 0.614] | [0.074, 0.668] | bilgi |
| GOVDE_1 | set 2 | 39 | 26 | 0.641 | 0.323 | [0.069, 0.562] | [0.015, 0.640] | bilgi |
| GOVDE_1 | birleşik | 79 | 49 | 0.658 | 0.354 | [0.183, 0.533] | [0.144, 0.569] | BİLGİ (önceki kural) |

V1 = P1 ∧ P2' ∧ P3 ∧ P4 ∧ P5' (ANA; P5' = D2 temiz ∧ P5 kırılım); V2 = V1 ama D2 yok; V3 = DS5 V1. GOVDE_1 = G4_fitil_govde_arasi <= 0.4046040192474485 (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem).

HÜKÜM kuralı (ön kayıt): V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (düzeltme Cemal'in DS5_ONAY işaretlerinden; set 1 / set 2 sayfaları önceki DS3-DS5 işlerinde kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı (DS6_ONAY.pdf) + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).

## 2x2

**V1 birleşik**: Cemal VAR + kod VAR 4; Cemal YOK + kod YOK 44; Cemal YOK + kod VAR 5; Cemal VAR + kod YOK 26

**V2 birleşik**: Cemal VAR + kod VAR 6; Cemal YOK + kod YOK 44; Cemal YOK + kod VAR 5; Cemal VAR + kod YOK 24

**V3 birleşik**: Cemal VAR + kod VAR 11; Cemal YOK + kod YOK 40; Cemal YOK + kod VAR 9; Cemal VAR + kod YOK 19

**V1 set 1**: Cemal VAR + kod VAR 2; Cemal YOK + kod YOK 24; Cemal YOK + kod VAR 2; Cemal VAR + kod YOK 12

**V1 set 2**: Cemal VAR + kod VAR 2; Cemal YOK + kod YOK 20; Cemal YOK + kod VAR 3; Cemal VAR + kod YOK 14

## Cemal VAR dediği halde kodun (V1) YOK dediği sayfalarda düşen parça

Sayfa 26. Düşen parça sayımı (bir sayfada birden çok olabilir): P1 1; P2 2; P3 8; P4 0; D2 6; P5 21. Yalnız bu parça düştü: P1 0; P2 0; P3 3; P4 0; D2 2; P5 13.

Cemal YOK / kod V1 VAR: 5 sayfa ['set 1 / 2', 'set 1 / 21', 'set 2 / 2', 'set 2 / 22', 'set 2 / 36'].

## V1 uyuşmayan sayfalar

| sayfa | Cemal | V1 | V2 | V3 (DS5) | GOVDE_1 | dip yaşı | düşüş | mavi düşüş (ATR) | dokunuş (ilk / ikinci) | dip sonrası en düşük Low (ATR) | kırmızı: tepe dok. / geçerli / sahte | kırılım / üst kapanış | düşen parça | kodun gördüğü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set 1 / 2 | YOK | VAR | VAR | VAR | YOK | 28 | %46 | 0.00 | 3 (1 / 2) | +0.05 | 3 / evet / 0 | t-13 / 6 | - | altı parça da DOĞRU (kod VAR) |
| set 1 / 5 | VAR | YOK | YOK | YOK | VAR | 10 | %81 | 0.00 | 1 (1 / 0) | +0.66 | 2 / evet / 0 | - / 0 | P3, P5 | P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 12 | VAR | YOK | YOK | YOK | VAR | 32 | %64 | 0.00 | 5 (0 / 5) | +1.24 | 2 / evet / 0 | t-26 / 27 | P3 | P3 takip yok (dokunuş 5: ilk yarı 0, ikinci yarı 5) |
| set 1 / 14 | VAR | YOK | VAR | VAR | VAR | 70 | %112 | 0.00 | 10 (4 / 6) | +0.36 | 2 / hayır / 1 | t-54 / 53 | D2 | D2 kapanışla kesilmemiş çizgi yok: kirli çizgi (sahte kırılım 1) |
| set 1 / 17 | VAR | YOK | YOK | YOK | VAR | 21 | %137 | 0.00 | 6 (2 / 4) | +0.49 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 19 | VAR | YOK | YOK | YOK | VAR | 14 | %51 | 0.00 | 5 (2 / 3) | +0.13 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 20 | VAR | YOK | YOK | YOK | VAR | 24 | %134 | 2.12 | 1 (1 / 0) | +0.09 | 2 / evet / 0 | - / 0 | P2, P3, P5 | P2 mavi çizgi 2.12 ATR aşağı (> 0,5); P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 21 | YOK | VAR | VAR | VAR | VAR | 55 | %59 | 0.00 | 4 (1 / 3) | +0.09 | 4 / evet / 0 | t-45 / 46 | - | altı parça da DOĞRU (kod VAR) |
| set 1 / 26 | VAR | YOK | VAR | VAR | VAR | 45 | %131 | 0.00 | 3 (1 / 2) | +0.40 | 2 / hayır / 1 | t-44 / 45 | D2 | D2 kapanışla kesilmemiş çizgi yok: kirli çizgi (sahte kırılım 1) |
| set 1 / 32 | VAR | YOK | YOK | VAR | YOK | 11 | %62 | 0.00 | 9 (3 / 6) | +0.69 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 34 | VAR | YOK | YOK | YOK | VAR | 68 | %163 | 0.00 | 12 (0 / 12) | +0.88 | 2 / evet / 0 | t-54 / 14 | P3 | P3 takip yok (dokunuş 12: ilk yarı 0, ikinci yarı 12) |
| set 1 / 37 | VAR | YOK | YOK | YOK | VAR | 22 | %68 | 0.00 | 9 (3 / 6) | +0.30 | 3 / evet / 0 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 1 / 39 | VAR | YOK | YOK | YOK | VAR | 43 | %93 | 0.00 | 4 (4 / 0) | +0.07 | 2 / hayır / 2 | - / 0 | P3, D2, P5 | P3 takip yok (dokunuş 4: ilk yarı 4, ikinci yarı 0); D2 kapanışla kesilmemiş çizgi yok: kirli çizgi (sahte kırılım 2); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 40 | VAR | YOK | YOK | YOK | VAR | 12 | %71 | 0.08 | 5 (4 / 1) | +0.03 | 3 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 2 | YOK | VAR | VAR | VAR | YOK | 57 | %78 | 0.00 | 6 (4 / 2) | +0.14 | 3 / evet / 0 | t-43 / 43 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 3 | VAR | YOK | YOK | YOK | VAR | 44 | %50 | 11.36 | 2 (2 / 0) | +0.05 | 6 / evet / 0 | - / 0 | P2, P3, P5 | P2 mavi çizgi 11.36 ATR aşağı (> 0,5); P3 takip yok (dokunuş 2: ilk yarı 2, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 9 | VAR | YOK | YOK | YOK | VAR | 28 | %163 | 0.13 | 3 (3 / 0) | +0.00 | 3 / evet / 0 | - / 0 | P3, P5 | P3 takip yok (dokunuş 3: ilk yarı 3, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 10 | VAR | YOK | YOK | YOK | VAR | 18 | %71 | 0.00 | 9 (6 / 3) | +0.09 | 0 / hayır / 0 | - / 0 | D2, P5 | D2 düşen çizgi yok; P5 alçalan pivot tepe çifti yok (düşen çizgi yok) |
| set 2 / 14 | VAR | YOK | YOK | YOK | VAR | 23 | %50 | 0.00 | 11 (1 / 10) | +0.67 | 3 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 15 | VAR | YOK | YOK | YOK | VAR | 78 | %98 | 0.00 | 15 (0 / 15) | +0.37 | 2 / evet / 0 | t-76 / 77 | P3 | P3 takip yok (dokunuş 15: ilk yarı 0, ikinci yarı 15) |
| set 2 / 18 | VAR | YOK | YOK | VAR | VAR | 34 | %49 | 0.00 | 5 (1 / 4) | +0.41 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 19 | VAR | YOK | YOK | VAR | VAR | 37 | %103 | 0.00 | 12 (2 / 10) | +0.08 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 21 | VAR | YOK | YOK | YOK | YOK | 14 | %49 | 0.00 | 4 (2 / 2) | +0.62 | 2 / evet / 0 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 2 / 22 | YOK | VAR | VAR | VAR | VAR | 27 | %150 | 0.00 | 7 (4 / 3) | +0.12 | 2 / evet / 0 | t-10 / 8 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 25 | VAR | YOK | YOK | VAR | VAR | 29 | %160 | 0.00 | 4 (2 / 2) | +0.46 | 2 / evet / 0 | t-8 / 9 | P5 | P5 kırılımdan sonra mavi çizgiye dokunuş yok |
| set 2 / 27 | VAR | YOK | YOK | YOK | VAR | 119 | %nan | 0.00 | 8 (4 / 4) | +0.64 | 0 / hayır / 0 | - / 0 | P1, D2, P5 | P1 düşüş yok (- < %20); D2 düşen çizgi yok; P5 alçalan pivot tepe çifti yok (düşen çizgi yok) |
| set 2 / 30 | VAR | YOK | YOK | VAR | VAR | 17 | %38 | 0.00 | 10 (5 / 5) | +0.36 | 2 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 32 | VAR | YOK | YOK | YOK | VAR | 85 | %167 | 0.14 | 5 (2 / 3) | +0.42 | 0 / hayır / 0 | - / 0 | D2, P5 | D2 düşen çizgi yok; P5 alçalan pivot tepe çifti yok (düşen çizgi yok) |
| set 2 / 36 | YOK | VAR | VAR | VAR | VAR | 12 | %191 | 0.00 | 4 (1 / 3) | +0.22 | 2 / evet / 0 | t-8 / 9 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 37 | VAR | YOK | YOK | YOK | YOK | 14 | %29 | 0.00 | 11 (5 / 6) | +0.41 | 3 / evet / 0 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 38 | VAR | YOK | YOK | VAR | VAR | 18 | %100 | 0.00 | 7 (3 / 4) | +0.56 | 3 / evet / 0 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |

## Karşılaştırma: aynı sayfalarda DS5 V1 (= V3) ve GOVDE_1

- V1_V3: karar 79 sayfada iki kod 66 sayfada aynı yanıt (kodlar arası kappa 0.468); V1 doğru / öteki yanlış 5; öteki doğru / V1 yanlış 8.
- V1_GOVDE_1: karar 79 sayfada iki kod 33 sayfada aynı yanıt (kodlar arası kappa 0.018); V1 doğru / öteki yanlış 21; öteki doğru / V1 yanlış 25.

DS6 V1 ile DS5 V1'in ayrıldığı sayfalar: set 1 / 14 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen D2), set 1 / 26 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen D2), set 1 / 28 (Cemal YOK; DS5 VAR -> DS6 YOK; düşen D2,P5), set 1 / 32 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 8 (Cemal YOK; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 12 (Cemal YOK; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 18 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 19 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 24 (Cemal YOK; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 25 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 29 (Cemal VAR; DS5 YOK -> DS6 VAR; düşen -), set 2 / 30 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5), set 2 / 38 (Cemal VAR; DS5 VAR -> DS6 YOK; düşen P5)

## DS5_ONAY'ın 24 sayfasında cevap değişimi (BİLGİ; Cemal'in DS5_ONAY işaretleri tanım geri bildirimi)

| sayfa | pazar | Cemal (DS5_ONAY) | v5 V1 | v6 V1 | v6 V2 | V değişti | kırmızı çizgi değişti | sahte / geçerli | mavi düşüş (ATR) | v6 düşen parça | etiket | Cemal'in çizimi (betim) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | DOĞRU | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | DİKKAT: Cemal'in DOĞRU dediği yanıt değişti | Kutu: büyük X DOĞRU ÇİZGİ üzerinde. Grafiğe çizim yok. |
| 2 | ABD | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | bilgi (yanıt değişti) | Kutu işaretsiz. Grafikte soldan (170,490) sağa yukarı kısa kırmızı çizgi, orta H1-H2 hattında dikey çizgi ve ok; sağ üstte 'Sahte' yazısı ve '?'; son mumlarda 2 küçük daire/nokta. Düşen çizginin ortadaki kırılımını sahte bulmuş, hat zayıf. |
| 3 | ABD | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | bilgi (yanıt değişti) | Kutu işaretsiz. Sol-üst H1 sonrası tepe bölgesinde ∧/yukarı ok çizimi (çizgiyi sahte kırılım gibi gösteriyor), sağ-orta sarı bölgede büyük '?'. Mavi çizgiye dokunmamış. |
| 4 | ABD | YANLIŞ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | itiraz yanıtı değişti | Sayfa boyunca büyük X (kutuya değil alta), kutu işaretsiz ama ret. Düşen çizgi boyunca 2-3 tepede ∧ biçimli sahte kırılım kıvrımları (sol-üst 180-450, orta 400-570); sağ altta son mumlarda ok-spiral. Düşen çizgi/sahte kırılımlar itiraz. |
| 5 | ABD | DOĞRU | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | DİKKAT: Cemal'in DOĞRU dediği yanıt değişti | X DOĞRU ÇİZGİ üzerinde. Grafiğe çizim yok. |
| 6 | ABD | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | bilgi (yanıt değişti) | Kutu işaretsiz. Soldan alt (95,675) yükselen uzun çizgi, orta-üstte (430-500,395) ok ile tepe bölgesine; H1 sonrası tepeler; ortada '?' ve dikey kısa çizgi. Düşen çizgi yerine farklı/yükselen çizgi çizmiş, çizgiyi sorguluyor. |
| 7 | ABD | DOĞRU | VAR | YOK | YOK | EVET | evet | 1 / hayır | 0.00 | D2, P5 | DİKKAT: Cemal'in DOĞRU dediği yanıt değişti | X DOĞRU ÇİZGİ üzerinde. Grafiğe çizim yok. |
| 8 | ABD | YANLIŞ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | itiraz yanıtı değişti | Büyük X sonuç satırı ve YANLIŞ kutusu üzerinde, ayrıca 'Çizgi yatay/yukarı' satırı yanında kısa çizgi. Grafikte soldan (100,655) yükselen eğri ile orta tepeye (445,460) ok-döngü, altta '?' kıvrımı. Düşen çizgi (H1-H2) ve mavi eğim itiraz. |
| 9 | ABD | DOĞRU | VAR | VAR | VAR | - | hayır | 0 / evet | 0.00 | - | korundu | X DOĞRU ÇİZGİ üzerinde. Grafikte orta-solda küçük V/✓ benzeri çizim (330-410,515-685). |
| 10 | ABD | DOĞRU | VAR | VAR | VAR | - | evet | 0 / evet | 0.00 | - | korundu | X DOĞRU ÇİZGİ üzerinde ve grafikte sol-altta büyük ✓. |
| 11 | ABD | DOĞRU | VAR | YOK | YOK | EVET | evet | 3 / hayır | 0.00 | D2, P5 | DİKKAT: Cemal'in DOĞRU dediği yanıt değişti | X DOĞRU ÇİZGİ üzerinde. Grafiğe çizim yok. |
| 12 | ABD | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | bilgi (yanıt değişti) | Kutu işaretsiz. H1 sonrası tepe bölgesinde (380-450,190-310) daire, sağında '?' ve kesik çizgi. Düşen çizgiyi/tepe öbeğini sorguluyor. |
| 13 | AVR | YANLIŞ | VAR | YOK | YOK | EVET | evet | 1 / hayır | 0.00 | D2, P5 | itiraz yanıtı değişti | X YANLIŞ kutusu üzerinde. Grafikte soldan (45,365) başlayıp sağ alta (715,715) inen uzun farklı düşen çizgi (kodun H1-H2'sinden daha geniş/soldan); ayrıca H1-H2 hattı alta ok gibi uzatılmış, 'VAR' yazısına ok. Düşen çizgi yanlış. |
| 14 | BIST | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 0 / evet | 0.00 | P5 | bilgi (yanıt değişti) | Kutu işaretsiz. Sol-üst tepe mumlarında daire + ∧ işareti, H2 bölgesinde yay, son mumlarda büyük daire (dip sonrası ilk yükseliş mumları); alt yarıda büyük yazı 'Net değil' ve üstünde çarpı. Kod çizimleri net değil. |
| 15 | BIST | İŞARETSİZ | VAR | YOK | YOK | EVET | evet | 2 / hayır | 0.00 | D2, P5 | bilgi (yanıt değişti) | Hiç işaret/çizim yok. |
| 16 | AVR | İŞARETSİZ | VAR | YOK | VAR | EVET | evet | 2 / hayır | 0.00 | D2 | bilgi (yanıt değişti) | Hiç işaret/çizim yok. |
| 17 | AVR | İŞARETSİZ | YOK | YOK | YOK | - | evet | 0 / evet | 0.91 | P2, P5 | bilgi | Kutu işaretsiz. Sol-üst tepe mumlarında daire, sarı bölgenin ilk mumlarında daire (540-645,455-550) ve kısa çizgi; sayfaya büyük 'Net değil' yazısı. Dip/mavi çizgi net değil. |
| 18 | AVR | İŞARETSİZ | YOK | YOK | YOK | - | evet | 0 / evet | 0.00 | P5 | bilgi | Kutu işaretsiz. Dairelenmiş iki yer: sol-üstte düşen çizgiyi kıran tepe mumları ('1') ve sağdaki son kırılım mumları ('2'); yazı: '1 ve 2 nin fark yok' (okuma: 1 ve 2'nin farkı yok). Yani kırılım var, kod YOK demiş. |
| 19 | ABD | DOĞRU | YOK | YOK | YOK | - | evet | 0 / evet | 0.00 | P3, P5 | korundu | X DOĞRU ÇİZGİ üzerinde. Grafikte orta-üstten (460,235) aşağı (480,495) kancalı ok: düşen çizgiye/dibe doğru. |
| 20 | ABD | DOĞRU | YOK | YOK | YOK | - | evet | 0 / evet | 0.00 | P3 | korundu | X DOĞRU ÇİZGİ üzerinde. Grafikte tek nokta. |
| 21 | ABD | DOĞRU | YOK | YOK | YOK | - | evet | 0 / evet | 2.82 | P2, P3, P5 | korundu | X DOĞRU ÇİZGİ üzerinde. Sağ altta dibin altından geçip sağa çıkan dalgalı döngü çizgisi (435-720,680-745), mavi (aşağı eğimli) çizgi bölgesi. |
| 22 | ABD | YANLIŞ | YOK | YOK | YOK | - | evet | 0 / hayır | 0.46 | D2, P5 | yanıt aynı (çizgi değişti) | X YANLIŞ kutusu üzerinde (iki çapraz çizgi). Grafikte soldan (260,565) tepe (480,380) ok, dikey ok: ortadaki yukarı tepe bölgesine; düşüş mumlarının tepesi H1 olmalı gibi. |
| 23 | AVR | İŞARETSİZ | YOK | VAR | VAR | EVET | hayır | 0 / evet | 0.28 | - | bilgi (yanıt değişti) | Kutu işaretsiz. Büyük yazı üstte 'Şekil doğru'(okuma) ve altta 'ama mavi yok(?)...' (kısmen sayfa dışı); orta alta ve sağda kırmızı kalın çizgi/ok, son mumlarda yukarı ok (610,700 -> 720,655). Şekil doğru ama mavi çizgi sorunlu. |
| 24 | ABD | DOĞRU | YOK | YOK | YOK | - | hayır | 0 / evet | 0.00 | P5 | korundu | X DOĞRU ÇİZGİ üzerinde. Grafiğe çizim yok. |

Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural düzeltmeleri iş tanımından, kör set etiketlerine bakmadan sabitlendi ve önce sentetik serilerde sınandı.
