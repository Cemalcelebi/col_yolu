# GÖZ UYUM KÖR SETİ — SONUÇ

Üretim: 2026-11-23T16:11:45Z (UTC). Mühür denetimi: anahtar, PDF ve GU_ESIK sha'ları ön kayıtla aynı.

Sayfa 40; karar (VAR / YOK) 40; '?' (karar dışı) 0.

## Uyum tablosu

| model | uyum | kappa | %95 aralık (B 5000) | hüküm |
|---|---|---|---|---|
| ANA (Ş3 (F2 >= -0,01)) | 0.700 | 0.400 | [0.111, 0.652] | TANIM GEÇERSİZ |
| IKINCIL-1 (Ş5 (F4 <= 0,25)) | 0.600 | 0.200 | [-0.086, 0.472] | TANIM GEÇERSİZ |
| IKINCIL-2 (Ş3 ∧ Ş5) | 0.700 | 0.294 | [-0.027, 0.594] | TANIM GEÇERSİZ |

Hüküm yalnız ANA için bağlayıcıdır (ön kayıt); ikincil iki satır bilgidir. Kappa >= 0,60 TANIM GEÇERLİ; 0,40-0,60 KISMEN; < 0,40 TANIM GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ.

### ANA: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 11 |
| Cemal YOK + kod YOK | 17 |
| Cemal YOK + kod VAR | 9 |
| Cemal VAR + kod YOK | 3 |

Uyuşmayan sayfalar (12): [1, 3, 6, 10, 12, 18, 24, 26, 29, 33, 36, 38]

### IKINCIL-1: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 9 |
| Cemal YOK + kod YOK | 15 |
| Cemal YOK + kod VAR | 11 |
| Cemal VAR + kod YOK | 5 |

Uyuşmayan sayfalar (16): [2, 7, 10, 11, 13, 14, 15, 16, 18, 19, 21, 24, 31, 32, 36, 40]

### IKINCIL-2: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 6 |
| Cemal YOK + kod YOK | 22 |
| Cemal YOK + kod VAR | 4 |
| Cemal VAR + kod YOK | 8 |

Uyuşmayan sayfalar (12): [3, 7, 10, 12, 14, 18, 19, 24, 26, 32, 36, 40]

## Bilgi: ANA uyumu pazar ve hücre bazında (küçük n; hüküm değil)

| grup | n | uyum |
|---|---|---|
| ABD | 30 | 0.667 |
| AVR | 5 | 0.800 |
| BIST | 5 | 0.800 |
| S3=False S5=False (Cemal VAR 0) | 10 | 1.000 |
| S3=False S5=True (Cemal VAR 3) | 10 | 0.700 |
| S3=True S5=False (Cemal VAR 5) | 10 | 0.500 |
| S3=True S5=True (Cemal VAR 6) | 10 | 0.600 |

## Uyuşmayan sayfaların kodu gördüğü değerler (ANA)

| sayfa | pazar | Cemal | kod (Ş3) | F2 | F4 | Ş5 |
|---|---|---|---|---|---|---|
| 1 | ABD | YOK | VAR | 0.002 | 0.409 | YOK |
| 3 | ABD | VAR | YOK | -0.012 | 0.140 | VAR |
| 6 | BIST | YOK | VAR | 0.003 | 0.315 | YOK |
| 10 | ABD | YOK | VAR | 0.006 | 0.225 | VAR |
| 12 | ABD | VAR | YOK | -0.011 | 0.205 | VAR |
| 18 | ABD | YOK | VAR | -0.006 | 0.076 | VAR |
| 24 | ABD | YOK | VAR | 0.004 | 0.227 | VAR |
| 26 | ABD | VAR | YOK | -0.012 | 0.195 | VAR |
| 29 | ABD | YOK | VAR | 0.012 | 0.307 | YOK |
| 33 | ABD | YOK | VAR | 0.000 | 0.288 | YOK |
| 36 | ABD | YOK | VAR | 0.005 | 0.082 | VAR |
| 38 | AVR | YOK | VAR | 0.007 | 0.283 | YOK |

Sonraki adım (ön kayıt): (bu işte YAPILMAZ) kappa < 0,60 ise: Cemal'in işaretleri hedef, anahtardaki özellikler aday; her aday için tek eşikli kural (eşik = 40 sayfada VAR / YOK ayrımını en iyi yapan) ve ikinci bağımsız 40 sayfalık kör sette sınama; kappa >= 0,60 olmadan getiri ölçümü yok.
