# GÖVDE TEPKİSİ — İKİNCİ KÖR SET — SONUÇ

Üretim: 2026-11-23T17:09:36Z (UTC). Mühür denetimi: govde_anahtar, govde.py, GV_ESIK ve tanim2_anahtar sha'ları ön kayıtlarla aynı.

Sayfa 40; karar (VAR / YOK) 39 (Cemal VAR 16); '?' (karar dışı) 1.

- GOVDE_1: VAR ⇔ G4_fitil_govde_arasi <= 0.4046040192474485
- GOVDE_2: VAR ⇔ GOVDE_1 VE Ş3 (G4_fitil_govde_arasi <= 0.4046040192474485 VE F2 >= -0,01)
- Karşılaştırma: ADAY_1 / ADAY_2 / KONTROL (tanim2 mührü)

NOT: ikinci set GOVDE'ye göre tabakalanmadı; GOVDE ikinci sette ikincil adaydır.

| model | kod VAR | uyum | kappa | %95 aralık (B 5000) | hüküm |
|---|---|---|---|---|---|
| GOVDE_1 | 26 | 0.641 | 0.323 | [0.066, 0.585] | GEÇERSİZ |
| GOVDE_2 | 15 | 0.667 | 0.305 | [-0.011, 0.588] | GEÇERSİZ |
| ADAY_1 | 19 | 0.615 | 0.227 | [-0.088, 0.528] | karşılaştırma (tanim2 mührü; hüküm TANIM2_SONUC'ta) |
| ADAY_2 | 20 | 0.590 | 0.183 | [-0.131, 0.479] | karşılaştırma (tanim2 mührü; hüküm TANIM2_SONUC'ta) |
| KONTROL | 19 | 0.564 | 0.124 | [-0.188, 0.421] | karşılaştırma (tanim2 mührü; hüküm TANIM2_SONUC'ta) |

HÜKÜM kuralı (ön kayıt): ikinci sette GOVDE_1 (ve GOVDE_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. ADAY_1 / ADAY_2 / KONTROL (tanim2 mührü) karşılaştırma için yazılır.

### GOVDE_1: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 14 |
| Cemal YOK + kod YOK | 11 |
| Cemal YOK + kod VAR | 12 |
| Cemal VAR + kod YOK | 2 |

Uyuşmayan sayfalar (14): [1, 5, 6, 8, 16, 17, 21, 22, 26, 34, 35, 36, 37, 40]

### GOVDE_2: 2x2

| | sayı |
|---|---|
| Cemal VAR + kod VAR | 9 |
| Cemal YOK + kod YOK | 17 |
| Cemal YOK + kod VAR | 6 |
| Cemal VAR + kod YOK | 7 |

Uyuşmayan sayfalar (13): [1, 5, 6, 8, 14, 15, 17, 21, 23, 25, 29, 36, 37]

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

