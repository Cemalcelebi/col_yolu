# DİP SAVUNMASI v4 (DS4) — SONUÇ (iki kör set, 80 sayfa)

Üretim: 2026-11-23T18:36:25Z (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: 2026-11-23T18:36:23Z (UTC). Mühür denetimi: ds4_anahtar.json, ds4.py, DS4_ESIK, kural kaynağı, DS4_ONAY.pdf ve ds4_onay_anahtar.json sha'ları DS4_ON_KAYIT ile aynı; 80 sayfanın P1 / P2 / P3 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.

Karar: birleşik 79 (Cemal VAR 30); işaretsiz / '?' (karar dışı): 1 ['set 2 / 39'].

## HÜKÜM (V1, ön kayıttaki eşikle): **GEÇERSİZ** — birleşik kappa 0.126, %95 [-0.084, 0.336]

Sınır: Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek verdi; bu yüzden sonuç YARI BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in görsel onayı (DS4_ONAY.pdf) + üçüncü bağımsız kör setle.

NOT: V1 kappa set 1 0.222, set 2 0.035: İKİ SETTE DE < 0,40.

## Kappa tablosu

| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |
|---|---|---|---|---|---|---|---|---|
| V1 | set 1 | 40 | 9 | 0.675 | 0.222 | [-0.097, 0.525] | [-0.154, 0.583] | ayrı rapor |
| V1 | set 2 | 39 | 9 | 0.564 | 0.035 | [-0.250, 0.327] | [-0.304, 0.398] | ayrı rapor |
| V1 | birleşik | 79 | 18 | 0.620 | 0.126 | [-0.084, 0.336] | [-0.124, 0.383] | GEÇERSİZ |
| V2 | set 1 | 40 | 13 | 0.575 | 0.050 | [-0.257, 0.360] | [-0.315, 0.429] | bilgi |
| V2 | set 2 | 39 | 10 | 0.590 | 0.101 | [-0.198, 0.400] | [-0.263, 0.464] | bilgi |
| V2 | birleşik | 79 | 23 | 0.582 | 0.071 | [-0.144, 0.284] | [-0.187, 0.341] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| V3 | set 1 | 40 | 24 | 0.650 | 0.340 | [0.080, 0.600] | [0.020, 0.648] | bilgi |
| V3 | set 2 | 39 | 27 | 0.410 | -0.103 | [-0.373, 0.156] | [-0.438, 0.212] | bilgi |
| V3 | birleşik | 79 | 51 | 0.532 | 0.125 | [-0.065, 0.313] | [-0.099, 0.350] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| GOVDE_1 | set 1 | 40 | 23 | 0.675 | 0.378 | [0.128, 0.645] | [0.066, 0.700] | bilgi |
| GOVDE_1 | set 2 | 39 | 26 | 0.641 | 0.323 | [0.062, 0.586] | [0.015, 0.643] | bilgi |
| GOVDE_1 | birleşik | 79 | 49 | 0.658 | 0.354 | [0.176, 0.530] | [0.135, 0.568] | BİLGİ (önceki kural) |
| DS3_V1 | set 1 | 40 | 3 | 0.625 | -0.007 | [-0.191, 0.219] | [-0.231, 0.280] | bilgi |
| DS3_V1 | set 2 | 39 | 6 | 0.436 | -0.288 | [-0.456, -0.101] | [-0.496, -0.051] | bilgi |
| DS3_V1 | birleşik | 79 | 9 | 0.532 | -0.150 | [-0.281, -0.006] | [-0.314, 0.026] | BİLGİ (önceki kural) |

V1 = P1 ∧ P2 ∧ P3 (ANA); V2 = P1 ∧ P3; V3 = P1 ∧ P2 ∧ P3(i). GOVDE_1 = G4_fitil_govde_arasi <= 0.4046040192474485 (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem); DS3_V1 = ds3_anahtar.json mühürlü V1.

HÜKÜM kuralı (ön kayıt): V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek verdi; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).

## 2x2

**V1 birleşik**: Cemal VAR + kod VAR 9; Cemal YOK + kod YOK 40; Cemal YOK + kod VAR 9; Cemal VAR + kod YOK 21

**V2 birleşik**: Cemal VAR + kod VAR 10; Cemal YOK + kod YOK 36; Cemal YOK + kod VAR 13; Cemal VAR + kod YOK 20

**V3 birleşik**: Cemal VAR + kod VAR 22; Cemal YOK + kod YOK 20; Cemal YOK + kod VAR 29; Cemal VAR + kod YOK 8

**V1 set 1**: Cemal VAR + kod VAR 5; Cemal YOK + kod YOK 22; Cemal YOK + kod VAR 4; Cemal VAR + kod YOK 9

**V1 set 2**: Cemal VAR + kod VAR 4; Cemal YOK + kod YOK 18; Cemal YOK + kod VAR 5; Cemal VAR + kod YOK 12

## Cemal VAR dediği halde kodun YOK dediği sayfalarda düşen parça

| varyant | sayfa | düşen parça sayımı (bir sayfada birden çok olabilir) | yalnız bu parça düştü |
|---|---|---|---|
| V1 | 21 | P1 1; P2 8; P3(i) 0; P3(ii) 15; P3(iii) 9 | P1 0; P2 1; P3(i) 0; P3(ii) 7; P3(iii) 3 |
| V2 | 20 | P1 1; P3(i) 0; P3(ii) 15; P3(iii) 9 | P1 1; P3(i) 0; P3(ii) 10; P3(iii) 4 |
| V3 | 8 | P1 1; P2 8; P3(i) 0 | P1 0; P2 7; P3(i) 0 |

Cemal YOK / kod V1 VAR: 9 sayfa ['set 1 / 13', 'set 1 / 28', 'set 1 / 36', 'set 1 / 38', 'set 2 / 8', 'set 2 / 24', 'set 2 / 26', 'set 2 / 33', 'set 2 / 36'].

## V1 uyuşmayan sayfalar

| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | DS3_V1 | dip yaşı (mum) | düşüş | kırılım (t'ye göre) | dönüş dipleri (ATR) | düşen parça | kodun gördüğü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set 1 / 5 | VAR | YOK | YOK | VAR | VAR | YOK | 10 | %81 | t-9 | - | P3(ii) | P3(ii) dip sonrası onaylı pivot dip yok |
| set 1 / 7 | VAR | YOK | YOK | VAR | YOK | YOK | 32 | %51 | t-30 | 0.13, 0.32, 0.31, 0.27 | P3(ii) | P3(ii) pivot dip dibe yapışık (en yakın 0.13 ATR <= 0,5) |
| set 1 / 13 | YOK | VAR | VAR | VAR | YOK | YOK | 12 | %76 | t-9 | 1.38 | - | üç parça da DOĞRU (kod VAR) |
| set 1 / 14 | VAR | YOK | YOK | VAR | VAR | YOK | 70 | %112 | t-54 | 0.92, 1.39, 0.36, 2.04, 1.51, 1.03 | P3(ii) | P3(ii) pivot dip dibe yapışık (en yakın 0.36 ATR <= 0,5) |
| set 1 / 19 | VAR | YOK | YOK | VAR | VAR | YOK | 14 | %51 | t+0 | 0.13 | P3(ii) | P3(ii) pivot dip dibe yapışık (en yakın 0.13 ATR <= 0,5) |
| set 1 / 20 | VAR | YOK | YOK | YOK | VAR | YOK | 24 | %134 | - | 0.09, 0.24 | P2, P3(ii) | P2 d'den sonra hiçbir kapanış düşen çizginin üstünde değil; P3(ii) pivot dip dibe yapışık (en yakın 0.09 ATR <= 0,5) |
| set 1 / 26 | VAR | YOK | YOK | VAR | VAR | YOK | 45 | %131 | t-44 | 1.33, 0.70, 0.53 | P3(iii) | P3(iii) son pivot dip ilkinden düşük |
| set 1 / 28 | YOK | VAR | VAR | VAR | YOK | YOK | 31 | %50 | t-30 | 0.89, 0.89, 1.33 | - | üç parça da DOĞRU (kod VAR) |
| set 1 / 32 | VAR | YOK | YOK | VAR | YOK | VAR | 11 | %62 | t-3 | - | P3(ii) | P3(ii) dip sonrası onaylı pivot dip yok |
| set 1 / 34 | VAR | YOK | YOK | VAR | VAR | YOK | 68 | %163 | t-67 | 2.06, 3.48, 3.19, 0.88, 0.92, 1.57 | P3(iii) | P3(iii) son pivot dip ilkinden düşük |
| set 1 / 36 | YOK | VAR | VAR | VAR | YOK | YOK | 21 | %48 | t+0 | 1.44 | - | üç parça da DOĞRU (kod VAR) |
| set 1 / 38 | YOK | VAR | VAR | VAR | YOK | YOK | 37 | %70 | t-34 | 2.49, 2.28, 2.60, 2.71 | - | üç parça da DOĞRU (kod VAR) |
| set 1 / 40 | VAR | YOK | YOK | YOK | VAR | YOK | 12 | %71 | - | 0.03 | P2, P3(ii) | P2 d'den sonra hiçbir kapanış düşen çizginin üstünde değil; P3(ii) pivot dip dibe yapışık (en yakın 0.03 ATR <= 0,5) |
| set 2 / 3 | VAR | YOK | YOK | YOK | VAR | YOK | 44 | %50 | - | 1.41, 0.05, 0.85 | P2, P3(ii), P3(iii) | P2 d'den sonra hiçbir kapanış düşen çizginin üstünde değil; P3(ii) pivot dip dibe yapışık (en yakın 0.05 ATR <= 0,5); P3(iii) son pivot dip ilkinden düşük |
| set 2 / 8 | YOK | VAR | VAR | VAR | VAR | YOK | 12 | %69 | t-7 | 0.88 | - | üç parça da DOĞRU (kod VAR) |
| set 2 / 9 | VAR | YOK | YOK | VAR | VAR | YOK | 28 | %163 | t-24 | 0.03, 0.96, 1.08 | P3(ii) | P3(ii) pivot dip dibe yapışık (en yakın 0.03 ATR <= 0,5) |
| set 2 / 10 | VAR | YOK | YOK | YOK | VAR | YOK | 18 | %71 | - | 0.25 | P2, P3(ii) | P2 H1'den sonra pivot tepe yok; P3(ii) pivot dip dibe yapışık (en yakın 0.25 ATR <= 0,5) |
| set 2 / 14 | VAR | YOK | YOK | YOK | VAR | YOK | 23 | %50 | - | 0.78, 0.67 | P2, P3(iii) | P2 d'den sonra hiçbir kapanış düşen çizginin üstünde değil; P3(iii) son pivot dip ilkinden düşük |
| set 2 / 15 | VAR | YOK | YOK | VAR | VAR | YOK | 78 | %98 | t-76 | 3.53, 2.71, 2.81, 1.47, 1.26, 0.87, 0.58, 0.37 | P3(ii), P3(iii) | P3(ii) pivot dip dibe yapışık (en yakın 0.37 ATR <= 0,5); P3(iii) son pivot dip ilkinden düşük |
| set 2 / 18 | VAR | YOK | YOK | VAR | VAR | YOK | 34 | %49 | t-24 | 0.41, 1.34, 0.54, 0.97 | P3(ii) | P3(ii) pivot dip dibe yapışık (en yakın 0.41 ATR <= 0,5) |
| set 2 / 19 | VAR | YOK | YOK | VAR | VAR | YOK | 37 | %103 | t-13 | 0.78, 0.26, 0.16 | P3(ii), P3(iii) | P3(ii) pivot dip dibe yapışık (en yakın 0.16 ATR <= 0,5); P3(iii) son pivot dip ilkinden düşük |
| set 2 / 24 | YOK | VAR | VAR | VAR | YOK | YOK | 13 | %96 | t-12 | 0.70 | - | üç parça da DOĞRU (kod VAR) |
| set 2 / 25 | VAR | YOK | YOK | VAR | VAR | YOK | 29 | %160 | t-28 | 1.11, 0.72, 1.04 | P3(iii) | P3(iii) son pivot dip ilkinden düşük |
| set 2 / 26 | YOK | VAR | VAR | VAR | VAR | YOK | 33 | %67 | t-1 | 1.33, 1.36, 1.38 | - | üç parça da DOĞRU (kod VAR) |
| set 2 / 27 | VAR | YOK | YOK | YOK | VAR | YOK | 119 | %nan | - | 0.64, 21.91, 23.00, 16.64, 14.73, 10.91, 15.09, 7.64, 4.45 | P1, P2 | P1 düşüş yok (- < %20); P2 d'den önce onaylı pivot tepe yok |
| set 2 / 29 | VAR | YOK | YOK | VAR | VAR | YOK | 20 | %78 | t-1 | 0.46, 0.38 | P3(ii), P3(iii) | P3(ii) pivot dip dibe yapışık (en yakın 0.38 ATR <= 0,5); P3(iii) son pivot dip ilkinden düşük |
| set 2 / 32 | VAR | YOK | YOK | YOK | VAR | YOK | 85 | %167 | - | 2.40, 2.31, 2.38, 1.38, 1.58, 2.89, 0.48, 0.80 | P2, P3(ii), P3(iii) | P2 H1'den sonra pivot tepe yok; P3(ii) pivot dip dibe yapışık (en yakın 0.48 ATR <= 0,5); P3(iii) son pivot dip ilkinden düşük |
| set 2 / 33 | YOK | VAR | VAR | VAR | YOK | YOK | 18 | %55 | t-17 | 0.62, 0.93 | - | üç parça da DOĞRU (kod VAR) |
| set 2 / 36 | YOK | VAR | VAR | VAR | VAR | YOK | 12 | %191 | t-8 | 1.09 | - | üç parça da DOĞRU (kod VAR) |
| set 2 / 37 | VAR | YOK | VAR | YOK | YOK | YOK | 14 | %29 | - | 0.78 | P2 | P2 d'den sonra hiçbir kapanış düşen çizginin üstünde değil |

## Karşılaştırma: aynı sayfalarda önceki kurallar

- V1_GOVDE_1: karar 79 sayfada iki kod 34 sayfada aynı yanıt (kodlar arası kappa -0.007); V1 doğru / öteki yanlış 21; öteki doğru / V1 yanlış 24.
- V1_DS3_V1: karar 79 sayfada iki kod 52 sayfada aynı yanıt (kodlar arası kappa -0.179); V1 doğru / öteki yanlış 17; öteki doğru / V1 yanlış 10.

Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in tarifinden etiketlere bakmadan sabitlendi ve önce sentetik serilerde sınandı (DS3 dersi).
