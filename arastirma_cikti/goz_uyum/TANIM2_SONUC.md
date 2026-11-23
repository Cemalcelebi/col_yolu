# TANIM ADIMI 2 — İKİNCİ KÖR SET — SONUÇ

Üretim: 2026-11-23T17:09:36Z (UTC). Mühür denetimi: anahtar, PDF, keşif ve TZ_ESIK sha'ları ön kayıtla aynı.

Sayfa 40; karar (VAR / YOK) 39 (Cemal VAR 16); '?' (karar dışı) 1.

- ADAY_1: VAR ⇔ dip_bolge_n >= 18.5
- ADAY_2: dip_bolge_n: son 40 barda dip bölgesi (alt %20) bar sayısı VEYA F2: hat eğimi (son / ilk dokunuş Low - 1)
- KONTROL: eski Ş3 (F2 >= -0,01)

| model | uyum | kappa | %95 aralık (B 5000) | hüküm |
|---|---|---|---|---|
| ADAY_1 | 0.615 | 0.227 | [-0.088, 0.528] | GEÇERSİZ |
| ADAY_2 | 0.590 | 0.183 | [-0.131, 0.479] | GEÇERSİZ |
| KONTROL | 0.564 | 0.124 | [-0.188, 0.421] | karşılaştırma (hüküm yok) |

HÜKÜM kuralı (ön kayıt): ikinci sette ADAY_1 (ve varsa ADAY_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ (getiri ölçümüne geçilir, kasa açılır); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN (üçüncü tur: ilk iki setin 80 sayfası birleşik keşif, üçüncü bağımsız set); < 0,40 GEÇERSİZ (Cemal'le görüşme: neye baktığını çizimle anlatması); karar sayısı < 30 ise ÖLÇÜLEMEDİ. KONTROL (eski Ş3) kappa'sı karşılaştırma için yazılır.

### ADAY_1: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 10 |
| Cemal YOK + kod YOK | 14 |
| Cemal YOK + kod VAR | 9 |
| Cemal VAR + kod YOK | 6 |

Uyuşmayan sayfalar (15): [3, 6, 7, 8, 9, 13, 17, 18, 20, 22, 23, 25, 34, 35, 38]

### ADAY_2: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 10 |
| Cemal YOK + kod YOK | 13 |
| Cemal YOK + kod VAR | 10 |
| Cemal VAR + kod YOK | 6 |

Uyuşmayan sayfalar (16): [2, 3, 6, 7, 8, 9, 13, 17, 18, 20, 22, 23, 25, 34, 35, 38]

### KONTROL: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 9 |
| Cemal YOK + kod YOK | 13 |
| Cemal YOK + kod VAR | 10 |
| Cemal VAR + kod YOK | 7 |

Uyuşmayan sayfalar (17): [1, 2, 4, 5, 6, 8, 14, 15, 17, 20, 21, 23, 25, 28, 29, 36, 37]

## Bilgi: ADAY_1 uyumu pazar ve hücre bazında (küçük n; hüküm değil)

| grup | n | uyum |
|---|---|---|
| ABD | 32 | 0.562 |
| AVR | 2 | 0.500 |
| BIST | 5 | 1.000 |
| A1=False S3=False (Cemal VAR 2) | 10 | 0.800 |
| A1=False S3=True (Cemal VAR 4) | 10 | 0.600 |
| A1=True S3=False (Cemal VAR 5) | 10 | 0.500 |
| A1=True S3=True (Cemal VAR 5) | 9 | 0.556 |
