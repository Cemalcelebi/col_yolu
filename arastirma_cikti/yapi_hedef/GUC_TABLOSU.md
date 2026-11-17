# YAPI_HEDEF — GÜÇ TABLOSU

Üreten: `python YAPI_HEDEF.py guc` (YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo); 2026-11-17 10:57:55 UTC; YH_ESIK_SHA `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b`.

ABD giriş 2023-01-01 .. 2026-06-30 havuzda (ok, kova) rastgele hisse-gün (6.000, yerine koymadan); her biri için olay göstergeleri, eş oranları (aynı gün aynı kova, min 3) ve plasebo (aynı hisse aynı dönem rastgele gün) gerçek fiyatla ve sabit d ile hesaplanır. Tekrar: n olay çekilir; KAT_ref > 1 ise h5 = 0 olan olaylar q = (KAT_ref Σ eş - Σ h5) / (n - Σ h5) olasılıkla h5 = 1 (st5 = 0) yapılır; hücre TUTAR kuralı (4 şart; bootstrap ay kümeli 2000, vektör) uygulanır; güç = TUTAR payı. KAT_ref = 1,0 enjeksiyonsuz (yanlış pozitif payı).

Havuz (rastgele hisse-gün; olay = rastgele gün, yani taban):

| yön | d | n | P(+5 önce) olay | eş | plasebo | P(stop önce) olay | eş |
|---|---|---|---|---|---|---|---|
| -1 | 0.03 | 6000 | %33,4 | %32,7 | %32,6 | %54,4 | %54,8 |
| -1 | 0.06 | 6000 | %38,0 | %37,3 | %37,5 | %38,9 | %39,1 |
| -1 | 0.10 | 6000 | %39,2 | %38,4 | %39,2 | %34,2 | %34,7 |
| 1 | 0.03 | 6000 | %35,8 | %35,5 | %35,9 | %51,8 | %51,3 |
| 1 | 0.06 | 6000 | %40,7 | %41,0 | %41,9 | %35,6 | %34,7 |
| 1 | 0.10 | 6000 | %42,2 | %42,2 | %43,0 | %30,8 | %30,1 |

## Yön +: güç (TUTAR payı); sütun KAT_ref / d

| n | KAT 1,00 d %3 | KAT 1,00 d %6 | KAT 1,00 d %10 | KAT 1,25 d %3 | KAT 1,25 d %6 | KAT 1,25 d %10 | KAT 1,50 d %3 | KAT 1,50 d %6 | KAT 1,50 d %10 |
|---|---|---|---|---|---|---|---|---|---|
| 30 | %0 | %0 | %0 | %2 | %6 | %4 | %20 | %28 | %36 |
| 100 | %0 | %0 | %1 | %11 | %23 | %20 | %70 | %81 | %82 |
| 300 | %0 | %0 | %1 | %57 | %62 | %65 | %100 | %100 | %100 |
| 1000 | %1 | %0 | %0 | %97 | %98 | %99 | %100 | %100 | %100 |
| 3000 | %0 | %0 | %0 | %100 | %100 | %100 | %100 | %100 | %100 |

## Yön -: güç (TUTAR payı); sütun KAT_ref / d

| n | KAT 1,00 d %3 | KAT 1,00 d %6 | KAT 1,00 d %10 | KAT 1,25 d %3 | KAT 1,25 d %6 | KAT 1,25 d %10 | KAT 1,50 d %3 | KAT 1,50 d %6 | KAT 1,50 d %10 |
|---|---|---|---|---|---|---|---|---|---|
| 30 | %1 | %0 | %0 | %2 | %5 | %4 | %24 | %28 | %21 |
| 100 | %2 | %0 | %0 | %10 | %18 | %18 | %69 | %71 | %70 |
| 300 | %2 | %0 | %0 | %52 | %58 | %56 | %99 | %100 | %99 |
| 1000 | %1 | %2 | %0 | %96 | %100 | %98 | %100 | %100 | %100 |
| 3000 | %0 | %0 | %0 | %100 | %100 | %100 | %100 | %100 | %100 |

KAT_ref 1,00 sütunu yanlış pozitif payıdır (enjeksiyon yok). Etiket için KAT 1,25 sütunlarının EN KÜÇÜĞÜ kullanılır.
