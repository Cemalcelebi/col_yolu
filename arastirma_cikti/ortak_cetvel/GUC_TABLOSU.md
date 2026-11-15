# ORTAK CETVEL — GÜÇ TABLOSU (ORTAK_CETVEL v1.0 (2026-11-14))

Üretim 2026-11-14 13:24:59 UTC; cetvel sha `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`; kod sha `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`.
Kaynak: ABD (V_ABD + k34), giriş 2023-01-01 .. 2026-06-30, havuzda olan, r60'ı ölçülebilir ve en az 3 eşi olan rastgele hisse-gün (yerine koymadan); olayın r60'ına δ eklenir, eşler dokunulmaz (K58 k58_delta_ekle ile aynı); güç = hücrenin TUTTUĞU tekrar payı. Uygun hisse-gün: 1717110. Tekrar 200 (tohum 1477).
GÜÇ = beş şartlı hücre kuralının (FI dört şart + iki alt dönem aynı yön) tuttuğu tekrar payı; 'güç4' = yalnız FI dört şart.

## Gerçek eş farkı dağılımı (ABD 2023-26)

| n | δ %0 güç / güç4 | δ %2 güç / güç4 | δ %5 güç / güç4 | δ %10 güç / güç4 | %95 yarı genişlik | ay |
|---|---|---|---|---|---|---|
| 30 | %0,5 / %1,0 | %2,5 / %3,5 | %10,5 / %11,0 | %37,5 / %38,5 | %12,5 | 21 |
| 100 | %2,5 / %2,5 | %10,0 / %10,0 | %29,0 / %29,5 | %91,0 / %91,0 | %6,4 | 38 |
| 300 | %0,5 / %0,5 | %11,0 / %11,0 | %51,5 / %51,5 | %96,5 / %96,5 | %4,0 | 42 |
| 1000 | %1,5 / %1,5 | %19,0 / %19,0 | %65,0 / %65,0 | %98,5 / %98,5 | %2,3 | 42 |
| 3000 | %0,0 / %0,0 | %24,5 / %24,5 | %60,0 / %60,0 | %97,0 / %97,0 | %1,3 | 42 |

Şart başına geçme payı (δ = +%5):

| n | fark+alt uç | sıra | portföy | iki yarı | güç |
|---|---|---|---|---|---|
| 30 | %11,0 | %92,0 | %27,0 | %48,0 | %10,5 |
| 100 | %33,0 | %99,5 | %47,5 | %74,5 | %29,0 |
| 300 | %79,5 | %100,0 | %54,0 | %94,5 | %51,5 |
| 1000 | %99,5 | %100,0 | %65,0 | %99,5 | %65,0 |
| 3000 | %100,0 | %100,0 | %60,0 | %100,0 | %60,0 |

## Varsayım: normal, σ = %25 (veri yoksa yedek)

| n | δ %0 güç / güç4 | δ %2 güç / güç4 | δ %5 güç / güç4 | δ %10 güç / güç4 | %95 yarı genişlik | ay |
|---|---|---|---|---|---|---|
| 30 | %6,0 / %6,0 | %11,0 / %11,5 | %23,0 / %23,5 | %59,5 / %61,0 | %8,8 | 22 |
| 100 | %4,0 / %4,0 | %11,5 / %11,5 | %49,5 / %49,5 | %98,0 / %98,0 | %4,9 | 38 |
| 300 | %2,0 / %2,0 | %16,0 / %16,0 | %74,5 / %74,5 | %99,5 / %99,5 | %2,8 | 42 |
| 1000 | %1,0 / %1,0 | %24,5 / %25,0 | %76,0 / %76,0 | %99,5 / %99,5 | %1,6 | 42 |
| 3000 | %2,0 / %2,0 | %35,0 / %35,0 | %81,0 / %81,0 | %100,0 / %100,0 | %0,9 | 42 |

Şart başına geçme payı (δ = +%5):

| n | fark+alt uç | sıra | portföy | iki yarı | güç |
|---|---|---|---|---|---|
| 30 | %24,0 | %82,5 | %42,0 | %61,0 | %23,0 |
| 100 | %54,0 | %99,0 | %70,5 | %86,0 | %49,5 |
| 300 | %92,0 | %100,0 | %77,5 | %99,0 | %74,5 |
| 1000 | %100,0 | %100,0 | %76,0 | %100,0 | %76,0 |
| 3000 | %100,0 | %100,0 | %81,0 | %100,0 | %81,0 |

## K58 tutarlılık

Dört şartlı güç, δ +%2, n <= 300: en yüksek %11,0 (K58: <= %11; pay 5 puan) -> TUTARLI. Not: K58 plasebo olayları 2016-26'ya yayıyordu (daha çok ay, daha dar aralık); burada 2023-26 (karar dönemleri), bu yüzden güç K58'den düşük ya da eşit beklenir.

## Yeniden üretim (ham csv'den bağımsız; K11)

- n 300, δ %5: ham satırların ham istatistiklerinden (ort fark, alt uç, sıra, portföy, p90, yarılar) yeniden %51,5; özet tablo %51,5 -> AYNI
- n 1000, δ %2: ham satırların ham istatistiklerinden (ort fark, alt uç, sıra, portföy, p90, yarılar) yeniden %19,0; özet tablo %19,0 -> AYNI

## Okuma

- Etiket kuralı (OC_ESIK etiket): hücre 'güç yeterli' = n >= 1.000 YA DA bu tablodaki güç(n, δ = +%5) >= %80 (n'den küçük ya da eşit en büyük satır). Değilse tutmayan hücre İZ DEĞİL değil ÖLÇÜLEMEDİ yazılır.
- δ = 0 satırı yanlış pozitif payıdır (rastgele olayların hücreyi tutturma oranı).
