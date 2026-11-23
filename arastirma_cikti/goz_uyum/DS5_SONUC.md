# DİP SAVUNMASI v5 (DS5) — SONUÇ (iki kör set, 80 sayfa)

Üretim: 2026-11-23T18:59:34Z (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: 2026-11-23T18:59:32Z (UTC). Mühür denetimi: ds5_anahtar.json, ds5.py, DS5_ESIK, kural kaynağı, DS5_ONAY.pdf ve ds5_onay_anahtar.json sha'ları DS5_ON_KAYIT ile aynı; 80 sayfanın P1-P5 ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.

Karar: birleşik 79 (Cemal VAR 30); işaretsiz / '?' (karar dışı): 1 ['set 2 / 39'].

## HÜKÜM (V1, ön kayıttaki eşikle): **GEÇERSİZ** — birleşik kappa 0.196, %95 [-0.020, 0.403]

Sınır: Cemal tarifini DS4 görselini görerek verdi ve iki set önceki DS3 / DS4 işlerinde kullanıldı; bu yüzden sonuç YARI BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in görsel onayı (DS5_ONAY.pdf) + üçüncü bağımsız kör setle.

NOT: V1 kappa set 1 0.268, set 2 0.119: İKİ SETTE DE < 0,40.

## Kappa tablosu

| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |
|---|---|---|---|---|---|---|---|---|
| V1 | set 1 | 40 | 8 | 0.700 | 0.268 | [-0.048, 0.562] | [-0.131, 0.627] | ayrı rapor |
| V1 | set 2 | 39 | 12 | 0.590 | 0.119 | [-0.188, 0.423] | [-0.258, 0.480] | ayrı rapor |
| V1 | birleşik | 79 | 20 | 0.646 | 0.196 | [-0.020, 0.403] | [-0.076, 0.453] | GEÇERSİZ |
| V2 | set 1 | 40 | 6 | 0.700 | 0.241 | [-0.059, 0.527] | [-0.139, 0.600] | bilgi |
| V2 | set 2 | 39 | 8 | 0.590 | 0.082 | [-0.192, 0.376] | [-0.247, 0.437] | bilgi |
| V2 | birleşik | 79 | 14 | 0.646 | 0.161 | [-0.042, 0.360] | [-0.080, 0.410] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| V3 | set 1 | 40 | 16 | 0.650 | 0.255 | [-0.059, 0.536] | [-0.136, 0.598] | bilgi |
| V3 | set 2 | 39 | 20 | 0.692 | 0.387 | [0.093, 0.646] | [0.023, 0.698] | bilgi |
| V3 | birleşik | 79 | 36 | 0.671 | 0.327 | [0.116, 0.529] | [0.068, 0.565] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| GOVDE_1 | set 1 | 40 | 23 | 0.675 | 0.378 | [0.133, 0.612] | [0.074, 0.662] | bilgi |
| GOVDE_1 | set 2 | 39 | 26 | 0.641 | 0.323 | [0.077, 0.562] | [0.023, 0.630] | bilgi |
| GOVDE_1 | birleşik | 79 | 49 | 0.658 | 0.354 | [0.173, 0.531] | [0.129, 0.574] | BİLGİ (önceki kural) |
| DS4_V1 | set 1 | 40 | 9 | 0.675 | 0.222 | [-0.098, 0.525] | [-0.159, 0.588] | bilgi |
| DS4_V1 | set 2 | 39 | 9 | 0.564 | 0.035 | [-0.247, 0.327] | [-0.306, 0.388] | bilgi |
| DS4_V1 | birleşik | 79 | 18 | 0.620 | 0.126 | [-0.085, 0.336] | [-0.130, 0.388] | BİLGİ (önceki kural) |
| DS3_V1 | set 1 | 40 | 3 | 0.625 | -0.007 | [-0.192, 0.214] | [-0.231, 0.269] | bilgi |
| DS3_V1 | set 2 | 39 | 6 | 0.436 | -0.288 | [-0.461, -0.102] | [-0.506, -0.051] | bilgi |
| DS3_V1 | birleşik | 79 | 9 | 0.532 | -0.150 | [-0.280, -0.009] | [-0.313, 0.028] | BİLGİ (önceki kural) |

V1 = P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5 (ANA); V2 = V1 ∧ alt fitil küçük; V3 = P1 ∧ P2 ∧ P3 ∧ P4 (P5 yok, basit tepki dahil). GOVDE_1 = G4_fitil_govde_arasi <= 0.4046040192474485 (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem); DS4_V1 = ds4_anahtar.json mühürlü V1; DS3_V1 = ds3_anahtar.json mühürlü V1.

HÜKÜM kuralı (ön kayıt): V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS4 görselini görerek verdi; set 1 / set 2 sayfaları daha önce DS3 / DS4 çalışmalarında kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).

## 2x2

**V1 birleşik**: Cemal VAR + kod VAR 11; Cemal YOK + kod YOK 40; Cemal YOK + kod VAR 9; Cemal VAR + kod YOK 19

**V2 birleşik**: Cemal VAR + kod VAR 8; Cemal YOK + kod YOK 43; Cemal YOK + kod VAR 6; Cemal VAR + kod YOK 22

**V3 birleşik**: Cemal VAR + kod VAR 20; Cemal YOK + kod YOK 33; Cemal YOK + kod VAR 16; Cemal VAR + kod YOK 10

**V1 set 1**: Cemal VAR + kod VAR 5; Cemal YOK + kod YOK 23; Cemal YOK + kod VAR 3; Cemal VAR + kod YOK 9

**V1 set 2**: Cemal VAR + kod VAR 6; Cemal YOK + kod YOK 17; Cemal YOK + kod VAR 6; Cemal VAR + kod YOK 10

## Cemal VAR dediği halde kodun (V1) YOK dediği sayfalarda düşen parça

Sayfa 19. Düşen parça sayımı (bir sayfada birden çok olabilir): P1 1; P2 4; P3 8; P4 0; P5 14. Yalnız bu parça düştü: P1 0; P2 0; P3 4; P4 0; P5 9.

Cemal YOK / kod V1 VAR: 9 sayfa ['set 1 / 2', 'set 1 / 21', 'set 1 / 28', 'set 2 / 2', 'set 2 / 8', 'set 2 / 12', 'set 2 / 22', 'set 2 / 24', 'set 2 / 36'].

## V1 uyuşmayan sayfalar

| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | DS4_V1 | DS3_V1 | dip yaşı (mum) | düşüş | eğim (ATR / 20) | dokunuş (ilk / ikinci) | dip sonrası en düşük Low (ATR) | kırılım (t'ye göre) / üst kapanış | düşen parça | kodun gördüğü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set 1 / 2 | YOK | VAR | YOK | VAR | YOK | YOK | YOK | 28 | %46 | +0.04 | 3 (1 / 2) | +0.05 | t-26 / 27 | - | beş parça da DOĞRU (kod VAR) |
| set 1 / 5 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 10 | %81 | +0.00 | 1 (1 / 0) | +0.66 | t-9 / 10 | P3, P5 | P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); P5 kırılımdan sonra çizgiye dokunuş yok |
| set 1 / 12 | VAR | YOK | YOK | YOK | VAR | VAR | YOK | 32 | %64 | +1.03 | 5 (0 / 5) | +1.24 | t-26 / 27 | P3 | P3 takip yok (dokunuş 5: ilk yarı 0, ikinci yarı 5) |
| set 1 / 17 | VAR | YOK | YOK | VAR | VAR | VAR | YOK | 21 | %137 | +0.82 | 6 (2 / 4) | +0.49 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 1 / 19 | VAR | YOK | YOK | VAR | VAR | YOK | YOK | 14 | %51 | +0.15 | 5 (2 / 3) | +0.13 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 1 / 20 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 24 | %134 | -1.77 | 1 (1 / 0) | +0.09 | - / 0 | P2, P3, P5 | P2 çizgi alçalan (-1.77 ATR / 20 mum); P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 1 / 21 | YOK | VAR | VAR | VAR | VAR | YOK | YOK | 55 | %59 | -0.00 | 4 (1 / 3) | +0.09 | t-45 / 46 | - | beş parça da DOĞRU (kod VAR) |
| set 1 / 28 | YOK | VAR | VAR | VAR | YOK | VAR | YOK | 31 | %50 | +0.63 | 7 (1 / 6) | +0.89 | t-30 / 31 | - | beş parça da DOĞRU (kod VAR) |
| set 1 / 34 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 68 | %163 | +0.34 | 12 (0 / 12) | +0.88 | t-67 / 68 | P3 | P3 takip yok (dokunuş 12: ilk yarı 0, ikinci yarı 12) |
| set 1 / 37 | VAR | YOK | YOK | VAR | VAR | VAR | YOK | 22 | %68 | +0.50 | 9 (3 / 6) | +0.30 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 1 / 39 | VAR | YOK | YOK | YOK | VAR | VAR | YOK | 43 | %93 | +0.00 | 4 (4 / 0) | +0.07 | t-42 / 43 | P3 | P3 takip yok (dokunuş 4: ilk yarı 4, ikinci yarı 0) |
| set 1 / 40 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 12 | %71 | -0.13 | 5 (4 / 1) | +0.03 | - / 0 | P2, P5 | P2 çizgi alçalan (-0.13 ATR / 20 mum); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 2 | YOK | VAR | VAR | VAR | YOK | YOK | YOK | 57 | %78 | +0.26 | 6 (4 / 2) | +0.14 | t-43 / 44 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 3 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 44 | %50 | -5.17 | 2 (2 / 0) | +0.05 | - / 0 | P2, P3, P5 | P2 çizgi alçalan (-5.17 ATR / 20 mum); P3 takip yok (dokunuş 2: ilk yarı 2, ikinci yarı 0); P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 8 | YOK | VAR | VAR | VAR | VAR | VAR | YOK | 12 | %69 | +2.18 | 7 (3 / 4) | +0.23 | t-7 / 5 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 9 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 28 | %163 | -0.09 | 3 (3 / 0) | +0.00 | t-24 / 19 | P2, P3 | P2 çizgi alçalan (-0.09 ATR / 20 mum); P3 takip yok (dokunuş 3: ilk yarı 3, ikinci yarı 0) |
| set 2 / 10 | VAR | YOK | YOK | VAR | VAR | YOK | YOK | 18 | %71 | +0.58 | 9 (6 / 3) | +0.09 | - / 0 | P5 | P5 H1'den sonra pivot tepe yok |
| set 2 / 12 | YOK | VAR | YOK | VAR | YOK | YOK | YOK | 26 | %163 | +0.24 | 10 (1 / 9) | +0.24 | t-15 / 10 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 14 | VAR | YOK | YOK | VAR | VAR | YOK | YOK | 23 | %50 | +0.89 | 11 (1 / 10) | +0.67 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |
| set 2 / 15 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 78 | %98 | +0.02 | 15 (0 / 15) | +0.37 | t-76 / 77 | P3 | P3 takip yok (dokunuş 15: ilk yarı 0, ikinci yarı 15) |
| set 2 / 21 | VAR | YOK | YOK | VAR | YOK | VAR | YOK | 14 | %49 | +0.59 | 4 (2 / 2) | +0.62 | t+0 / 1 | P5 | P5 düşen çizginin üstünde 1 kapanış (< 3) |
| set 2 / 22 | YOK | VAR | VAR | VAR | VAR | YOK | YOK | 27 | %150 | +0.07 | 7 (4 / 3) | +0.12 | t-10 / 8 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 24 | YOK | VAR | YOK | VAR | YOK | VAR | YOK | 13 | %96 | +1.45 | 8 (1 / 7) | +0.70 | t-12 / 13 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 27 | VAR | YOK | YOK | YOK | VAR | YOK | YOK | 119 | %nan | +0.92 | 8 (4 / 4) | +0.64 | - / 0 | P1, P5 | P1 düşüş yok (- < %20); P5 d'den önce onaylı pivot tepe yok |
| set 2 / 29 | VAR | YOK | YOK | VAR | VAR | YOK | YOK | 20 | %78 | +0.54 | 9 (6 / 3) | +0.04 | t-1 / 2 | P5 | P5 düşen çizginin üstünde 2 kapanış (< 3) |
| set 2 / 32 | VAR | YOK | YOK | VAR | VAR | YOK | YOK | 85 | %167 | -0.03 | 5 (2 / 3) | +0.42 | - / 0 | P5 | P5 H1'den sonra pivot tepe yok |
| set 2 / 36 | YOK | VAR | VAR | VAR | VAR | VAR | YOK | 12 | %191 | +2.32 | 4 (1 / 3) | +0.22 | t-8 / 9 | - | beş parça da DOĞRU (kod VAR) |
| set 2 / 37 | VAR | YOK | YOK | VAR | YOK | YOK | YOK | 14 | %29 | +0.65 | 11 (5 / 6) | +0.41 | - / 0 | P5 | P5 düşen çizginin üstünde 0 kapanış (< 3) |

## Karşılaştırma: aynı sayfalarda önceki kurallar

- V1_GOVDE_1: karar 79 sayfada iki kod 36 sayfada aynı yanıt (kodlar arası kappa 0.027); V1 doğru / öteki yanlış 21; öteki doğru / V1 yanlış 22.
- V1_DS4_V1: karar 79 sayfada iki kod 57 sayfada aynı yanıt (kodlar arası kappa 0.238); V1 doğru / öteki yanlış 12; öteki doğru / V1 yanlış 10.
- V1_DS3_V1: karar 79 sayfada iki kod 52 sayfada aynı yanıt (kodlar arası kappa -0.105); V1 doğru / öteki yanlış 18; öteki doğru / V1 yanlış 9.

Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in tarifinden etiketlere bakmadan sabitlendi ve önce sentetik serilerde sınandı (DS3 / DS4 dersi).
