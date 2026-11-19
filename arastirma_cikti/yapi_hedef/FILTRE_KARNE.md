# FİLTRE KARNESİ (yürüyen sınama; YAPI_HEDEF 6. tur §B)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo. Üretim: 2026-11-19 07:46:32 UTC. Komut: `python YAPI_HEDEF.py filtrekarne` (her yeni ders / filtre eklendiğinde AYNI komutla yenilenir). Girdi: olay_Y1.csv.gz (h5, es_h5) + özellik dosyaları (F1-F29). Eşik seçmez; raporlamadır.

Tanım: Huni Y1 (adım 0) -> + filtre (kol sırasıyla; Ş1-Ş5 iki kolda ortak). Her adım x pazar x dönem: n = ölçülen olay (h5 ve eş h5 var), P olay = ort h5, P eş = ort es_h5, FARK = P olay - P eş, MARJİNAL = FARK(adım) - FARK(önceki adım). EĞİTİM 2016-22, SINAMA 2023-26 (2023 + 2024-26); tersi (eğitim 2023-26, sınama 2016-22) aynı iki sayıyı kullandığı için etiket simetriktir. Etiket: KATKI+ = marjinal > 0 iki dönemde VE adım n >= 30 iki dönemde; KATKI− = marjinal < 0 iki dönemde VE n >= 30 iki dönemde; değilse SORGULA (dönemler çelişiyor ya da n < 30). Değerler yüzde puan (FARK = P olay - P eş). Eğitim = 2016-22; sınama = 2023, 2024-26.

**SORGULANACAK FİLTRELER: F14 büyük resim [S7 kolu, SORGULA]; Ş8 yol almamış [S7 kolu, SORGULA]; Ş6 kazan dönüş [S7 kolu, SORGULA]; Ş5 alt fitil kısa [S7 kolu, KATKI−]; Ş4 küçük mum [S7 kolu, SORGULA]; Ş3 dip savunulmuş [S7 kolu, KATKI−]; Ş2 hat net [S7 kolu, KATKI−]; F14 büyük resim [U kolu, SORGULA]; Ş8 yol almamış [U kolu, SORGULA]; Ş7 yakın tavan gövdeli kırılım [U kolu, SORGULA]; Ş9 U dip [U kolu, SORGULA]; Ş5 alt fitil kısa [U kolu, KATKI−]; Ş4 küçük mum [U kolu, SORGULA]; Ş3 dip savunulmuş [U kolu, KATKI−]; Ş2 hat net [U kolu, KATKI−]**

## 1. Karar pazarı (ABD+AVR)

| Filtre | Kol | eğitim n | eğitim P olay / P eş | eğitim FARK | eğitim MARJİNAL | sınama n | sınama P olay / P eş | sınama FARK | sınama MARJİNAL | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| Y1 | S7 | 13175 | %32,8 / %33,5 | -0,6 | - | 8649 | %38,0 / %38,4 | -0,4 | - | - |
| Ş1 dipte | S7 | 435 | %50,1 / %46,4 | +3,7 | +4,4 | 452 | %54,4 / %45,6 | +8,8 | +9,2 | KATKI+ |
| Ş2 hat net | S7 | 257 | %47,1 / %45,5 | +1,6 | -2,1 | 283 | %54,1 / %45,7 | +8,4 | -0,4 | KATKI− |
| Ş3 dip savunulmuş | S7 | 220 | %46,4 / %45,6 | +0,8 | -0,8 | 260 | %53,5 / %45,9 | +7,5 | -0,9 | KATKI− |
| Ş4 küçük mum | S7 | 193 | %47,7 / %45,8 | +1,8 | +1,1 | 239 | %52,3 / %45,7 | +6,6 | -0,9 | SORGULA |
| Ş5 alt fitil kısa | S7 | 93 | %47,3 / %47,5 | -0,2 | -2,0 | 124 | %51,6 / %46,2 | +5,4 | -1,2 | KATKI− |
| Ş6 kazan dönüş | S7 | 74 | %48,6 / %49,1 | -0,4 | -0,3 | 97 | %52,6 / %44,8 | +7,8 | +2,4 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | S7 | 41 | %58,5 / %52,1 | +6,4 | +6,8 | 50 | %56,0 / %46,1 | +9,9 | +2,1 | KATKI+ |
| Ş8 yol almamış | S7 | 40 | %57,5 / %53,0 | +4,5 | -1,9 | 50 | %56,0 / %46,1 | +9,9 | +0,0 | SORGULA |
| F14 büyük resim | S7 | 9 | %55,6 / %48,6 | +6,9 | +2,4 | 15 | %66,7 / %44,0 | +22,6 | +12,7 | SORGULA |
| Y1 | U | 13175 | %32,8 / %33,5 | -0,6 | - | 8649 | %38,0 / %38,4 | -0,4 | - | - |
| Ş1 dipte | U | 435 | %50,1 / %46,4 | +3,7 | +4,4 | 452 | %54,4 / %45,6 | +8,8 | +9,2 | KATKI+ |
| Ş2 hat net | U | 257 | %47,1 / %45,5 | +1,6 | -2,1 | 283 | %54,1 / %45,7 | +8,4 | -0,4 | KATKI− |
| Ş3 dip savunulmuş | U | 220 | %46,4 / %45,6 | +0,8 | -0,8 | 260 | %53,5 / %45,9 | +7,5 | -0,9 | KATKI− |
| Ş4 küçük mum | U | 193 | %47,7 / %45,8 | +1,8 | +1,1 | 239 | %52,3 / %45,7 | +6,6 | -0,9 | SORGULA |
| Ş5 alt fitil kısa | U | 93 | %47,3 / %47,5 | -0,2 | -2,0 | 124 | %51,6 / %46,2 | +5,4 | -1,2 | KATKI− |
| Ş9 U dip | U | 14 | %71,4 / %51,6 | +19,8 | +20,0 | 9 | %55,6 / %41,2 | +14,4 | +8,9 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | U | 6 | %100,0 / %54,6 | +45,4 | +25,6 | 5 | %60,0 / %33,9 | +26,1 | +11,8 | SORGULA |
| Ş8 yol almamış | U | 6 | %100,0 / %54,6 | +45,4 | +0,0 | 5 | %60,0 / %33,9 | +26,1 | +0,0 | SORGULA |
| F14 büyük resim | U | 2 | %100,0 / %55,2 | +44,8 | -0,6 | 3 | %100,0 / %38,9 | +61,1 | +35,0 | SORGULA |

### TEK-ÇIKARMA (ABD+AVR): TAM kol kümesi (kolun bütün filtreleri) ve her filtre tek tek çıkarılınca: DELTA = FARK(tam - f) - FARK(tam), iki dönem; DELTA > 0 iki dönemde (n >= 30 iki dönemde) -> ZARAR VERİYOR; DELTA < 0 iki dönemde -> YARARLI; değilse BELİRSİZ

| Çıkarılan filtre | Kol | eğitim n tam / çıkarılmış | eğitim FARK tam -> çıkarılmış (DELTA) | sınama n tam / çıkarılmış | sınama FARK tam -> çıkarılmış (DELTA) | etiket |
|---|---|---|---|---|---|---|
| Ş1 dipte | S7 | 9 / 978 | +6,9 -> +0,0 (-6,9) | 15 / 663 | +22,6 -> -0,7 (-23,3) | BELİRSİZ |
| Ş2 hat net | S7 | 9 / 18 | +6,9 -> -3,5 (-10,4) | 15 / 22 | +22,6 -> +19,3 (-3,3) | BELİRSİZ |
| Ş3 dip savunulmuş | S7 | 9 / 9 | +6,9 -> +6,9 (+0,0) | 15 / 16 | +22,6 -> +25,3 (+2,7) | BELİRSİZ |
| Ş4 küçük mum | S7 | 9 / 9 | +6,9 -> +6,9 (+0,0) | 15 / 15 | +22,6 -> +22,6 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | S7 | 9 / 24 | +6,9 -> -2,7 (-9,6) | 15 / 34 | +22,6 -> +26,6 (+3,9) | BELİRSİZ |
| Ş6 kazan dönüş | S7 | 9 / 13 | +6,9 -> +4,8 (-2,1) | 15 / 17 | +22,6 -> +26,0 (+3,4) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 9 / 18 | +6,9 -> +0,5 (-6,4) | 15 / 28 | +22,6 -> +15,3 (-7,4) | BELİRSİZ |
| Ş8 yol almamış | S7 | 9 / 10 | +6,9 -> +14,4 (+7,5) | 15 / 15 | +22,6 -> +22,6 (+0,0) | BELİRSİZ |
| F14 büyük resim | S7 | 9 / 40 | +6,9 -> +4,5 (-2,4) | 15 / 50 | +22,6 -> +9,9 (-12,7) | BELİRSİZ |
| Ş1 dipte | U | 2 / 58 | +44,8 -> +9,7 (-35,1) | 3 / 57 | +61,1 -> +5,0 (-56,1) | BELİRSİZ |
| Ş2 hat net | U | 2 / 2 | +44,8 -> +44,8 (+0,0) | 3 / 3 | +61,1 -> +61,1 (+0,0) | BELİRSİZ |
| Ş3 dip savunulmuş | U | 2 / 2 | +44,8 -> +44,8 (+0,0) | 3 / 3 | +61,1 -> +61,1 (+0,0) | BELİRSİZ |
| Ş4 küçük mum | U | 2 / 2 | +44,8 -> +44,8 (+0,0) | 3 / 3 | +61,1 -> +61,1 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | U | 2 / 3 | +44,8 -> +12,1 (-32,7) | 3 / 3 | +61,1 -> +61,1 (+0,0) | BELİRSİZ |
| Ş9 U dip | U | 2 / 13 | +44,8 -> +4,8 (-40,0) | 3 / 17 | +61,1 -> +26,0 (-35,1) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | U | 2 / 5 | +44,8 -> +13,1 (-31,6) | 3 / 4 | +61,1 -> +55,4 (-5,8) | BELİRSİZ |
| Ş8 yol almamış | U | 2 / 2 | +44,8 -> +44,8 (+0,0) | 3 / 3 | +61,1 -> +61,1 (+0,0) | BELİRSİZ |
| F14 büyük resim | U | 2 / 6 | +44,8 -> +45,4 (+0,6) | 3 / 5 | +61,1 -> +26,1 (-35,0) | BELİRSİZ |

## ABD (bilgi)

| Filtre | Kol | eğitim n | eğitim P olay / P eş | eğitim FARK | eğitim MARJİNAL | sınama n | sınama P olay / P eş | sınama FARK | sınama MARJİNAL | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| Y1 | S7 | 8682 | %34,5 / %35,8 | -1,2 | - | 6123 | %41,4 / %41,4 | -0,0 | - | - |
| Ş1 dipte | S7 | 346 | %50,3 / %47,4 | +2,8 | +4,1 | 377 | %55,7 / %47,0 | +8,7 | +8,8 | KATKI+ |
| Ş2 hat net | S7 | 206 | %46,6 / %46,7 | -0,1 | -3,0 | 232 | %55,6 / %47,2 | +8,4 | -0,4 | KATKI− |
| Ş3 dip savunulmuş | S7 | 176 | %46,0 / %47,2 | -1,2 | -1,1 | 216 | %55,6 / %47,3 | +8,2 | -0,1 | KATKI− |
| Ş4 küçük mum | S7 | 152 | %48,0 / %47,2 | +0,9 | +2,1 | 198 | %54,0 / %46,9 | +7,2 | -1,1 | SORGULA |
| Ş5 alt fitil kısa | S7 | 71 | %46,5 / %49,0 | -2,5 | -3,4 | 99 | %53,5 / %47,0 | +6,6 | -0,6 | KATKI− |
| Ş6 kazan dönüş | S7 | 56 | %50,0 / %50,9 | -0,9 | +1,6 | 77 | %55,8 / %45,9 | +10,0 | +3,4 | KATKI+ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 32 | %56,2 / %54,0 | +2,3 | +3,2 | 38 | %60,5 / %49,2 | +11,3 | +1,3 | KATKI+ |
| Ş8 yol almamış | S7 | 31 | %54,8 / %55,2 | -0,3 | -2,6 | 38 | %60,5 / %49,2 | +11,3 | +0,0 | SORGULA |
| F14 büyük resim | S7 | 8 | %50,0 / %49,0 | +1,0 | +1,3 | 12 | %75,0 / %46,7 | +28,3 | +17,0 | SORGULA |
| Y1 | U | 8682 | %34,5 / %35,8 | -1,2 | - | 6123 | %41,4 / %41,4 | -0,0 | - | - |
| Ş1 dipte | U | 346 | %50,3 / %47,4 | +2,8 | +4,1 | 377 | %55,7 / %47,0 | +8,7 | +8,8 | KATKI+ |
| Ş2 hat net | U | 206 | %46,6 / %46,7 | -0,1 | -3,0 | 232 | %55,6 / %47,2 | +8,4 | -0,4 | KATKI− |
| Ş3 dip savunulmuş | U | 176 | %46,0 / %47,2 | -1,2 | -1,1 | 216 | %55,6 / %47,3 | +8,2 | -0,1 | KATKI− |
| Ş4 küçük mum | U | 152 | %48,0 / %47,2 | +0,9 | +2,1 | 198 | %54,0 / %46,9 | +7,2 | -1,1 | SORGULA |
| Ş5 alt fitil kısa | U | 71 | %46,5 / %49,0 | -2,5 | -3,4 | 99 | %53,5 / %47,0 | +6,6 | -0,6 | KATKI− |
| Ş9 U dip | U | 10 | %80,0 / %53,5 | +26,5 | +29,0 | 7 | %57,1 / %44,2 | +12,9 | +6,4 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | U | 4 | %100,0 / %61,6 | +38,4 | +11,9 | 3 | %66,7 / %36,1 | +30,6 | +17,7 | SORGULA |
| Ş8 yol almamış | U | 4 | %100,0 / %61,6 | +38,4 | +0,0 | 3 | %66,7 / %36,1 | +30,6 | +0,0 | SORGULA |
| F14 büyük resim | U | 1 | %100,0 / %64,6 | +35,4 | -3,0 | 2 | %100,0 / %40,3 | +59,7 | +29,1 | SORGULA |

Tek-çıkarma (ABD):

| Çıkarılan filtre | Kol | eğitim n tam / çıkarılmış | eğitim FARK tam -> çıkarılmış (DELTA) | sınama n tam / çıkarılmış | sınama FARK tam -> çıkarılmış (DELTA) | etiket |
|---|---|---|---|---|---|---|
| Ş1 dipte | S7 | 8 / 591 | +1,0 -> -0,3 (-1,3) | 12 / 461 | +28,3 -> +0,2 (-28,1) | BELİRSİZ |
| Ş2 hat net | S7 | 8 / 16 | +1,0 -> -4,2 (-5,2) | 12 / 17 | +28,3 -> +27,3 (-1,0) | BELİRSİZ |
| Ş3 dip savunulmuş | S7 | 8 / 8 | +1,0 -> +1,0 (+0,0) | 12 / 13 | +28,3 -> +31,2 (+2,9) | BELİRSİZ |
| Ş4 küçük mum | S7 | 8 / 8 | +1,0 -> +1,0 (+0,0) | 12 / 12 | +28,3 -> +28,3 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | S7 | 8 / 18 | +1,0 -> -6,0 (-7,0) | 12 / 28 | +28,3 -> +25,6 (-2,7) | BELİRSİZ |
| Ş6 kazan dönüş | S7 | 8 / 12 | +1,0 -> +0,7 (-0,3) | 12 / 13 | +28,3 -> +30,9 (+2,6) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 8 / 17 | +1,0 -> -2,7 (-3,7) | 12 / 25 | +28,3 -> +17,1 (-11,2) | BELİRSİZ |
| Ş8 yol almamış | S7 | 8 / 9 | +1,0 -> +10,0 (+9,0) | 12 / 12 | +28,3 -> +28,3 (+0,0) | BELİRSİZ |
| F14 büyük resim | S7 | 8 / 31 | +1,0 -> -0,3 (-1,3) | 12 / 38 | +28,3 -> +11,3 (-17,0) | BELİRSİZ |
| Ş1 dipte | U | 1 / 40 | +35,4 -> +11,1 (-24,2) | 2 / 35 | +59,7 -> +10,9 (-48,8) | BELİRSİZ |
| Ş2 hat net | U | 1 / 1 | +35,4 -> +35,4 (+0,0) | 2 / 2 | +59,7 -> +59,7 (+0,0) | BELİRSİZ |
| Ş3 dip savunulmuş | U | 1 / 1 | +35,4 -> +35,4 (+0,0) | 2 / 2 | +59,7 -> +59,7 (+0,0) | BELİRSİZ |
| Ş4 küçük mum | U | 1 / 1 | +35,4 -> +35,4 (+0,0) | 2 / 2 | +59,7 -> +59,7 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | U | 1 / 2 | +35,4 -> -9,0 (-44,4) | 2 / 2 | +59,7 -> +59,7 (+0,0) | BELİRSİZ |
| Ş9 U dip | U | 1 / 12 | +35,4 -> +0,7 (-34,7) | 2 / 13 | +59,7 -> +30,9 (-28,8) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | U | 1 / 4 | +35,4 -> +2,9 (-32,5) | 2 / 3 | +59,7 -> +52,5 (-7,2) | BELİRSİZ |
| Ş8 yol almamış | U | 1 / 1 | +35,4 -> +35,4 (+0,0) | 2 / 2 | +59,7 -> +59,7 (+0,0) | BELİRSİZ |
| F14 büyük resim | U | 1 / 4 | +35,4 -> +38,4 (+3,0) | 2 / 3 | +59,7 -> +30,6 (-29,1) | BELİRSİZ |

## AVR (bilgi)

| Filtre | Kol | eğitim n | eğitim P olay / P eş | eğitim FARK | eğitim MARJİNAL | sınama n | sınama P olay / P eş | sınama FARK | sınama MARJİNAL | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| Y1 | S7 | 4493 | %29,6 / %29,1 | +0,5 | - | 2526 | %29,6 / %31,0 | -1,4 | - | - |
| Ş1 dipte | S7 | 89 | %49,4 / %42,2 | +7,2 | +6,7 | 75 | %48,0 / %39,0 | +9,0 | +10,4 | KATKI+ |
| Ş2 hat net | S7 | 51 | %49,0 / %40,3 | +8,8 | +1,6 | 51 | %47,1 / %38,7 | +8,4 | -0,7 | SORGULA |
| Ş3 dip savunulmuş | S7 | 44 | %47,7 / %39,0 | +8,7 | -0,1 | 44 | %43,2 / %39,3 | +3,9 | -4,5 | KATKI− |
| Ş4 küçük mum | S7 | 41 | %46,3 / %40,9 | +5,4 | -3,2 | 41 | %43,9 / %40,0 | +3,9 | -0,0 | KATKI− |
| Ş5 alt fitil kısa | S7 | 22 | %50,0 / %42,6 | +7,4 | +1,9 | 25 | %44,0 / %43,0 | +1,0 | -2,9 | SORGULA |
| Ş6 kazan dönüş | S7 | 18 | %44,4 / %43,5 | +1,0 | -6,4 | 20 | %40,0 / %40,6 | -0,6 | -1,5 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | S7 | 9 | %66,7 / %45,5 | +21,1 | +20,1 | 12 | %41,7 / %36,1 | +5,5 | +6,1 | SORGULA |
| Ş8 yol almamış | S7 | 9 | %66,7 / %45,5 | +21,1 | +0,0 | 12 | %41,7 / %36,1 | +5,5 | +0,0 | SORGULA |
| F14 büyük resim | S7 | 1 | %100,0 / %45,8 | +54,2 | +33,0 | 3 | %33,3 / %33,3 | -0,0 | -5,5 | SORGULA |
| Y1 | U | 4493 | %29,6 / %29,1 | +0,5 | - | 2526 | %29,6 / %31,0 | -1,4 | - | - |
| Ş1 dipte | U | 89 | %49,4 / %42,2 | +7,2 | +6,7 | 75 | %48,0 / %39,0 | +9,0 | +10,4 | KATKI+ |
| Ş2 hat net | U | 51 | %49,0 / %40,3 | +8,8 | +1,6 | 51 | %47,1 / %38,7 | +8,4 | -0,7 | SORGULA |
| Ş3 dip savunulmuş | U | 44 | %47,7 / %39,0 | +8,7 | -0,1 | 44 | %43,2 / %39,3 | +3,9 | -4,5 | KATKI− |
| Ş4 küçük mum | U | 41 | %46,3 / %40,9 | +5,4 | -3,2 | 41 | %43,9 / %40,0 | +3,9 | -0,0 | KATKI− |
| Ş5 alt fitil kısa | U | 22 | %50,0 / %42,6 | +7,4 | +1,9 | 25 | %44,0 / %43,0 | +1,0 | -2,9 | SORGULA |
| Ş9 U dip | U | 4 | %50,0 / %46,9 | +3,1 | -4,3 | 2 | %50,0 / %30,6 | +19,4 | +18,5 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | U | 2 | %100,0 / %40,7 | +59,3 | +56,3 | 2 | %50,0 / %30,6 | +19,4 | +0,0 | SORGULA |
| Ş8 yol almamış | U | 2 | %100,0 / %40,7 | +59,3 | +0,0 | 2 | %50,0 / %30,6 | +19,4 | +0,0 | SORGULA |
| F14 büyük resim | U | 1 | %100,0 / %45,8 | +54,2 | -5,2 | 1 | %100,0 / %36,1 | +63,9 | +44,4 | SORGULA |

Tek-çıkarma (AVR):

| Çıkarılan filtre | Kol | eğitim n tam / çıkarılmış | eğitim FARK tam -> çıkarılmış (DELTA) | sınama n tam / çıkarılmış | sınama FARK tam -> çıkarılmış (DELTA) | etiket |
|---|---|---|---|---|---|---|
| Ş1 dipte | S7 | 1 / 387 | +54,2 -> +0,5 (-53,7) | 3 / 202 | -0,0 -> -2,6 (-2,6) | BELİRSİZ |
| Ş2 hat net | S7 | 1 / 2 | +54,2 -> +2,1 (-52,1) | 3 / 5 | -0,0 -> -7,9 (-7,9) | BELİRSİZ |
| Ş3 dip savunulmuş | S7 | 1 / 1 | +54,2 -> +54,2 (+0,0) | 3 / 3 | -0,0 -> -0,0 (+0,0) | BELİRSİZ |
| Ş4 küçük mum | S7 | 1 / 1 | +54,2 -> +54,2 (+0,0) | 3 / 3 | -0,0 -> -0,0 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | S7 | 1 / 6 | +54,2 -> +7,1 (-47,0) | 3 / 6 | -0,0 -> +31,1 (+31,1) | BELİRSİZ |
| Ş6 kazan dönüş | S7 | 1 / 1 | +54,2 -> +54,2 (+0,0) | 3 / 4 | -0,0 -> +10,2 (+10,2) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 1 / 1 | +54,2 -> +54,2 (+0,0) | 3 / 3 | -0,0 -> -0,0 (+0,0) | BELİRSİZ |
| Ş8 yol almamış | S7 | 1 / 1 | +54,2 -> +54,2 (+0,0) | 3 / 3 | -0,0 -> -0,0 (+0,0) | BELİRSİZ |
| F14 büyük resim | S7 | 1 / 9 | +54,2 -> +21,1 (-33,0) | 3 / 12 | -0,0 -> +5,5 (+5,5) | BELİRSİZ |
| Ş1 dipte | U | 1 / 18 | +54,2 -> +6,5 (-47,7) | 1 / 22 | +63,9 -> -4,4 (-68,3) | BELİRSİZ |
| Ş2 hat net | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| Ş3 dip savunulmuş | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| Ş4 küçük mum | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| Ş9 U dip | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 4 | +63,9 -> +10,2 (-53,7) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| Ş8 yol almamış | U | 1 / 1 | +54,2 -> +54,2 (+0,0) | 1 / 1 | +63,9 -> +63,9 (+0,0) | BELİRSİZ |
| F14 büyük resim | U | 1 / 2 | +54,2 -> +59,3 (+5,2) | 1 / 2 | +63,9 -> +19,4 (-44,4) | BELİRSİZ |

## BIST (bilgi)

| Filtre | Kol | eğitim n | eğitim P olay / P eş | eğitim FARK | eğitim MARJİNAL | sınama n | sınama P olay / P eş | sınama FARK | sınama MARJİNAL | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| Y1 | S7 | 2588 | %50,4 / %51,7 | -1,2 | - | 2096 | %51,6 / %52,4 | -0,8 | - | - |
| Ş1 dipte | S7 | 238 | %45,8 / %45,6 | +0,2 | +1,4 | 362 | %57,5 / %56,0 | +1,4 | +2,3 | KATKI+ |
| Ş2 hat net | S7 | 145 | %49,7 / %47,5 | +2,2 | +1,9 | 207 | %54,6 / %54,5 | +0,0 | -1,4 | SORGULA |
| Ş3 dip savunulmuş | S7 | 135 | %50,4 / %47,3 | +3,1 | +0,9 | 183 | %54,1 / %55,3 | -1,2 | -1,3 | SORGULA |
| Ş4 küçük mum | S7 | 135 | %50,4 / %47,3 | +3,1 | +0,0 | 182 | %53,8 / %55,1 | -1,3 | -0,0 | SORGULA |
| Ş5 alt fitil kısa | S7 | 85 | %51,8 / %46,5 | +5,3 | +2,2 | 150 | %52,0 / %53,9 | -1,9 | -0,6 | SORGULA |
| Ş6 kazan dönüş | S7 | 72 | %55,6 / %47,2 | +8,4 | +3,1 | 117 | %52,1 / %53,2 | -1,1 | +0,8 | KATKI+ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 40 | %55,0 / %48,0 | +7,0 | -1,3 | 71 | %47,9 / %52,4 | -4,5 | -3,4 | KATKI− |
| Ş8 yol almamış | S7 | 40 | %55,0 / %48,0 | +7,0 | +0,0 | 71 | %47,9 / %52,4 | -4,5 | +0,0 | SORGULA |
| F14 büyük resim | S7 | 14 | %57,1 / %48,7 | +8,4 | +1,4 | 39 | %46,2 / %51,4 | -5,2 | -0,7 | SORGULA |
| Y1 | U | 2588 | %50,4 / %51,7 | -1,2 | - | 2096 | %51,6 / %52,4 | -0,8 | - | - |
| Ş1 dipte | U | 238 | %45,8 / %45,6 | +0,2 | +1,4 | 362 | %57,5 / %56,0 | +1,4 | +2,3 | KATKI+ |
| Ş2 hat net | U | 145 | %49,7 / %47,5 | +2,2 | +1,9 | 207 | %54,6 / %54,5 | +0,0 | -1,4 | SORGULA |
| Ş3 dip savunulmuş | U | 135 | %50,4 / %47,3 | +3,1 | +0,9 | 183 | %54,1 / %55,3 | -1,2 | -1,3 | SORGULA |
| Ş4 küçük mum | U | 135 | %50,4 / %47,3 | +3,1 | +0,0 | 182 | %53,8 / %55,1 | -1,3 | -0,0 | SORGULA |
| Ş5 alt fitil kısa | U | 85 | %51,8 / %46,5 | +5,3 | +2,2 | 150 | %52,0 / %53,9 | -1,9 | -0,6 | SORGULA |
| Ş9 U dip | U | 6 | %50,0 / %49,3 | +0,7 | -4,6 | 10 | %70,0 / %71,2 | -1,2 | +0,7 | SORGULA |
| Ş7 yakın tavan gövdeli kırılım | U | 4 | %50,0 / %54,0 | -4,0 | -4,8 | 9 | %66,7 / %69,3 | -2,6 | -1,4 | SORGULA |
| Ş8 yol almamış | U | 4 | %50,0 / %54,0 | -4,0 | +0,0 | 9 | %66,7 / %69,3 | -2,6 | +0,0 | SORGULA |
| F14 büyük resim | U | 2 | %50,0 / %60,3 | -10,3 | -6,3 | 4 | %75,0 / %72,7 | +2,3 | +5,0 | SORGULA |

Tek-çıkarma (BIST):

| Çıkarılan filtre | Kol | eğitim n tam / çıkarılmış | eğitim FARK tam -> çıkarılmış (DELTA) | sınama n tam / çıkarılmış | sınama FARK tam -> çıkarılmış (DELTA) | etiket |
|---|---|---|---|---|---|---|
| Ş1 dipte | S7 | 14 / 321 | +8,4 -> -3,0 (-11,4) | 39 / 286 | -5,2 -> -2,5 (+2,7) | BELİRSİZ |
| Ş2 hat net | S7 | 14 / 22 | +8,4 -> +6,0 (-2,4) | 39 / 65 | -5,2 -> +0,4 (+5,6) | BELİRSİZ |
| Ş3 dip savunulmuş | S7 | 14 / 15 | +8,4 -> +10,5 (+2,1) | 39 / 45 | -5,2 -> -1,9 (+3,3) | BELİRSİZ |
| Ş4 küçük mum | S7 | 14 / 14 | +8,4 -> +8,4 (+0,0) | 39 / 39 | -5,2 -> -5,2 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | S7 | 14 / 29 | +8,4 -> -6,4 (-14,8) | 39 / 48 | -5,2 -> -4,6 (+0,6) | BELİRSİZ |
| Ş6 kazan dönüş | S7 | 14 / 17 | +8,4 -> +7,8 (-0,6) | 39 / 45 | -5,2 -> -3,5 (+1,7) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | S7 | 14 / 34 | +8,4 -> +7,7 (-0,7) | 39 / 74 | -5,2 -> -0,0 (+5,2) | BELİRSİZ |
| Ş8 yol almamış | S7 | 14 / 14 | +8,4 -> +8,4 (+0,0) | 39 / 39 | -5,2 -> -5,2 (+0,0) | BELİRSİZ |
| F14 büyük resim | S7 | 14 / 40 | +8,4 -> +7,0 (-1,4) | 39 / 71 | -5,2 -> -4,5 (+0,7) | BELİRSİZ |
| Ş1 dipte | U | 2 / 19 | -10,3 -> -5,2 (+5,1) | 4 / 32 | +2,3 -> +5,4 (+3,0) | BELİRSİZ |
| Ş2 hat net | U | 2 / 3 | -10,3 -> -17,5 (-7,2) | 4 / 7 | +2,3 -> +10,5 (+8,2) | BELİRSİZ |
| Ş3 dip savunulmuş | U | 2 / 2 | -10,3 -> -10,3 (+0,0) | 4 / 5 | +2,3 -> +5,1 (+2,7) | BELİRSİZ |
| Ş4 küçük mum | U | 2 / 2 | -10,3 -> -10,3 (+0,0) | 4 / 4 | +2,3 -> +2,3 (+0,0) | BELİRSİZ |
| Ş5 alt fitil kısa | U | 2 / 4 | -10,3 -> -39,5 (-29,2) | 4 / 5 | +2,3 -> +4,0 (+1,6) | BELİRSİZ |
| Ş9 U dip | U | 2 / 17 | -10,3 -> +7,8 (+18,2) | 4 / 45 | +2,3 -> -3,5 (-5,8) | BELİRSİZ |
| Ş7 yakın tavan gövdeli kırılım | U | 2 / 4 | -10,3 -> -0,0 (+10,3) | 4 / 5 | +2,3 -> +4,2 (+1,8) | BELİRSİZ |
| Ş8 yol almamış | U | 2 / 2 | -10,3 -> -10,3 (+0,0) | 4 / 4 | +2,3 -> +2,3 (+0,0) | BELİRSİZ |
| F14 büyük resim | U | 2 / 4 | -10,3 -> -4,0 (+6,3) | 4 / 9 | +2,3 -> -2,6 (-5,0) | BELİRSİZ |

Not: evren bugün işlem gören hisseler (hayatta kalma yanlılığı: P olay ve P eş yukarı yanlı; FARK'ta kısmen birbirini götürür). ABD / AVR 2023-26 hücreleri önceki turlarda görüldü (bakılmış); karne kural seçmez, sorgulanacak filtreleri işaretler.

