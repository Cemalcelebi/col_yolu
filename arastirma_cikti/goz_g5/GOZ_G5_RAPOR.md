# GOZ_G5 — G5 dedektörü Cemal'in gözle işaretlediği çöllere uyuyor mu? (goz_g5_20261113)

Koşu 2026-11-13 11:09:31 UTC → 2026-11-13 11:09:36 UTC; ön kayıt commit a8e6509653df (2026-11-13T11:09:25+00:00), mühür f4e6b492a436.

## Sonuç

- **Test A: UYMUYOR.** G5, Cemal'in 29 çöl bölgesinin 1'ini yakalıyor (%3); aynı hisselerin rastgele pencerelerinde %1, Cemal'in 'olumsuz' bölgelerinde %25.
- **Test B:** hiçbir basit ölçü aday eşiğini (LOSO AUC >= 0,80 ve olumsuza karşı >= 0,70) geçmedi.
- **Test C:** C YAPILMADI (B'de aday yok).

Düz dille: G5, Cemal'in çöl bölgelerindeki günlerin ortalama %5'inde yanıyor (rastgele pencerelerde %3, olumsuzlarda %15). En iyi basit ölçüler (kapanış bandı (maks-min)/medyan 0,77, gövde / önceki ATR250 0,77, 250 günlük aralıkta konum 0,77) çölü aynı hissenin rastgele penceresinden kısmen ayırıyor, ama Cemal'in 'olumsuz' dediği bölgelerden ayıramıyor (olumsuza karşı AUC 0,41, 0,50, 0,68).

## Test A — G5 bölgenin en az yarısında yanıyor mu

| grup | bölge | hisse | yakalama (>= %50 gün) | %95 aralık (hisse kümeli) | en az 1 gün | G5 gün payı ort. | tanımsız bölge |
|---|---|---|---|---|---|---|---|
| Cemal ÇÖL | 29 | 25 | 0,03 | [0,00; 0,11] | 0,48 | 0,05 | 1 |
| Cemal OLUMSUZ | 8 | 8 | 0,25 | [0,00; 0,60] | 0,50 | 0,15 | 0 |
| RASTGELE (aynı hisse, aynı uzunluk) | 580 | 25 | 0,01 | [0,00; 0,01] | 0,25 | 0,03 | 0 |
| C seti DEĞİL (bilgi) | 22 | 21 | 0,00 | — | 0,32 | 0,03 | 0 |
| C seti ÖBEK (bilgi) | 3 | 1 | 0,00 | — | 0,33 | 0,01 | 0 |

COL − RASTGELE farkı aralığı [-0,01; 0,10]; COL / RASTGELE katı 6,67 (aralık [0,00; 40,00]); COL − OLUMSUZ [-0,57; 0,06].
Bilgi: 'en az 1 gün' tanımıyla karar UYMUYOR; yalnız G5'i tanımlı bölgelerde yakalama COL 0,04 (n 28), RASTGELE 0,01 (n 580).
Karar kuralı: G5 GÖZE UYUYOR <=> yak(COL) >= 0,70 VE yak(COL) >= 2 x yak(RASTGELE) VE yak(COL) > yak(OLUMSUZ); ZAYIF <=> yak(COL) >= 0,50 VE yak(COL) > 1,5 x yak(RASTGELE); değilse UYMUYOR (nokta tahminleri).

## Test B — gözün gördüğünü hangi basit ölçü ayırıyor

AUC 0,50 = ayırmıyor, 1,00 = tam ayırıyor (yönlü). LOSO = her hisse sırayla dışarıda, yön kalanlardan.

| ölçü | yön (çöl ...) | AUC çöl vs rastgele | LOSO AUC | AUC çöl vs olumsuz | medyan çöl / rastgele / olumsuz | aday |
|---|---|---|---|---|---|---|
| kapanış bandı (maks-min)/medyan | küçük | 0,77 | 0,77 | 0,41 | 0,148 / 0,261 / 0,136 | hayır |
| gövde / önceki ATR250 | küçük | 0,77 | 0,77 | 0,50 | 0,227 / 0,386 / 0,207 | hayır |
| 250 günlük aralıkta konum | küçük | 0,77 | 0,77 | 0,68 | 0,162 / 0,441 / 0,316 | hayır |
| mum boyu / önceki ATR250 | küçük | 0,75 | 0,75 | 0,54 | 0,570 / 0,867 / 0,602 | hayır |
| önceki 120 günde tepeden düşüş | küçük | 0,73 | 0,73 | 0,44 | -0,300 / -0,184 / -0,325 | hayır |
| SMA50 eğimi (%/gün) | küçük | 0,72 | 0,72 | 0,50 | -0,138 / 0,080 / -0,266 | hayır |
| 3 dip yakınlığı / ATR250 | küçük | 0,71 | 0,71 | 0,42 | 0,768 / 1,366 / 0,627 | hayır |
| mum boyu / fiyat (medyan H-L / C) | küçük | 0,65 | 0,65 | 0,49 | 0,032 / 0,040 / 0,031 | hayır |
| hacim / önceki 250 gün | küçük | 0,59 | 0,59 | 0,50 | 0,835 / 0,983 / 0,783 | hayır |
| bölge uzunluğu (gün) | büyük | 0,50 | 0,50 | 0,48 | 34,000 / 34,000 / 34,000 | hayır |

## Test C — ikinci Cemal etiket seti

C YAPILMADI (B'de aday yok). Bilgi: G5 C setindeki 22 DEĞİL kutunun %0'ini, 3 öbeğin %0'ini yakalıyor.
C kutularının çoğu 31.08.2026 sonrası (fon krizi dönemi; yalnız şekil). COL_GOZ kutuları kullanılmadı: sınıflar Claude'un gözü, Cemal'in 22 Ekim EVET / HAYIR dosyası repoda yok.

## Kapsam

Satırlar: {'COL': 29, 'C_DEGIL': 22, 'C_OBEK': 3, 'OLUMSUZ': 8, 'RASTGELE': 580}. Veri dışı: PEKER_20250227 (hisse veride yok). Kırpılan: GARFA_20260731 (22 gün). 20'den az rastgele pencere: yok. C'den çıkarılan (ana setle kesişen): yok.

