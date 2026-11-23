# DİP SAVUNMASI v7 (DS7) — SONUÇ (iki kör set, 80 sayfa)

Üretim: 2026-11-23T20:38:21Z (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: 2026-11-23T20:38:19Z (UTC). Mühür denetimi: ds7_anahtar.json, ds7.py, ds6.py, ds5.py, DS7_ESIK, kural kaynağı, DS7_ONAY.pdf ve ds7_onay_anahtar.json sha'ları DS7_ON_KAYIT ile aynı; 80 sayfanın P1-P4, TREND, KIRILIM, TREND_Z, KIRILIM_Z ve V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.

Karar: birleşik 79 (Cemal VAR 30); işaretsiz / '?' (karar dışı): 1 ['set 2 / 39'].

## HÜKÜM (V1, ön kayıttaki eşikle): **GEÇERSİZ** — birleşik kappa 0.230, %95 [0.007, 0.441]

Sınır: kural Cemal'in DS5_ONAY / DS6_ONAY işaretlerinden kuruldu ve iki set önceki DS3-DS6 işlerinde kullanıldı; sonuç YARI BAĞIMSIZDIR. Kesin hüküm yalnız Cemal'in görsel onayı (DS7_ONAY.pdf) + bağımsız üçüncü kör setle.

NOT: V1 kappa set 1 0.294, set 2 0.165: İKİ SETTE DE < 0,40.

## Kappa tablosu

| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |
|---|---|---|---|---|---|---|---|---|
| V1 | set 1 | 40 | 10 | 0.700 | 0.294 | [-0.023, 0.595] | [-0.095, 0.660] | ayrı rapor |
| V1 | set 2 | 39 | 11 | 0.615 | 0.165 | [-0.139, 0.458] | [-0.211, 0.522] | ayrı rapor |
| V1 | birleşik | 79 | 21 | 0.658 | 0.230 | [0.007, 0.441] | [-0.039, 0.486] | GEÇERSİZ |
| V2 | set 1 | 40 | 8 | 0.650 | 0.146 | [-0.154, 0.461] | [-0.221, 0.521] | bilgi |
| V2 | set 2 | 39 | 7 | 0.615 | 0.131 | [-0.147, 0.406] | [-0.193, 0.468] | bilgi |
| V2 | birleşik | 79 | 15 | 0.633 | 0.137 | [-0.064, 0.341] | [-0.109, 0.386] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| V3 | set 1 | 40 | 19 | 0.625 | 0.239 | [-0.059, 0.511] | [-0.125, 0.580] | bilgi |
| V3 | set 2 | 39 | 21 | 0.667 | 0.342 | [0.046, 0.599] | [-0.025, 0.688] | bilgi |
| V3 | birleşik | 79 | 40 | 0.646 | 0.293 | [0.085, 0.493] | [0.041, 0.537] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| DS6_V1 | set 1 | 40 | 4 | 0.650 | 0.079 | [-0.149, 0.342] | [-0.187, 0.407] | bilgi |
| DS6_V1 | set 2 | 39 | 5 | 0.564 | -0.006 | [-0.241, 0.235] | [-0.293, 0.297] | bilgi |
| DS6_V1 | birleşik | 79 | 9 | 0.608 | 0.036 | [-0.130, 0.211] | [-0.157, 0.261] | BİLGİ (önceki kural) |
| DS5_V1 | set 1 | 40 | 8 | 0.700 | 0.268 | [-0.039, 0.571] | [-0.095, 0.628] | bilgi |
| DS5_V1 | set 2 | 39 | 12 | 0.590 | 0.119 | [-0.191, 0.423] | [-0.259, 0.484] | bilgi |
| DS5_V1 | birleşik | 79 | 20 | 0.646 | 0.196 | [-0.020, 0.407] | [-0.063, 0.454] | BİLGİ (önceki kural) |
| GOVDE_1 | set 1 | 40 | 23 | 0.675 | 0.378 | [0.116, 0.646] | [0.050, 0.698] | bilgi |
| GOVDE_1 | set 2 | 39 | 26 | 0.641 | 0.323 | [0.062, 0.586] | [0.008, 0.636] | bilgi |
| GOVDE_1 | birleşik | 79 | 49 | 0.658 | 0.354 | [0.174, 0.530] | [0.140, 0.579] | BİLGİ (önceki kural) |

V1 = dip / mavi (P1 ∧ P2' ∧ P3 ∧ P4) ∧ TREND (dayanıklı ana trend düşüyor) ∧ KIRILIM (C_t > T(t)); V2 = aynı, saf zarfla; V3 = yalnız dip / mavi. DS6_V1 / DS5_V1 = önceki kurallar (mühürlü). GOVDE_1 = G4_fitil_govde_arasi <= 0.4046040192474485 (eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem).

HÜKÜM kuralı (ön kayıt): V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (kural Cemal'in DS5_ONAY / DS6_ONAY işaretlerinden kuruldu; set 1 / set 2 sayfaları önceki DS3-DS6 işlerinde kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı (DS7_ONAY.pdf) + bağımsız üçüncü kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).

## 2x2

**V1 birleşik**: Cemal VAR + kod VAR 12; Cemal YOK + kod YOK 40; Cemal YOK + kod VAR 9; Cemal VAR + kod YOK 18

**V2 birleşik**: Cemal VAR + kod VAR 8; Cemal YOK + kod YOK 42; Cemal YOK + kod VAR 7; Cemal VAR + kod YOK 22

**V3 birleşik**: Cemal VAR + kod VAR 21; Cemal YOK + kod YOK 30; Cemal YOK + kod VAR 19; Cemal VAR + kod YOK 9

**V1 set 1**: Cemal VAR + kod VAR 6; Cemal YOK + kod YOK 22; Cemal YOK + kod VAR 4; Cemal VAR + kod YOK 8

**V1 set 2**: Cemal VAR + kod VAR 6; Cemal YOK + kod YOK 18; Cemal YOK + kod VAR 5; Cemal VAR + kod YOK 10

## Cemal VAR dediği halde kodun (V1) YOK dediği sayfalarda düşen parça

Sayfa 18. Düşen parça sayımı (bir sayfada birden çok olabilir): P1 1; P2 2; P3 8; P4 0; TREND 1; KIRILIM 15. Yalnız bu parça düştü: P1 0; P2 0; P3 3; P4 0; TREND 0; KIRILIM 9.

Cemal YOK / kod V1 VAR: 9 sayfa ['set 1 / 9', 'set 1 / 21', 'set 1 / 28', 'set 1 / 31', 'set 2 / 2', 'set 2 / 12', 'set 2 / 22', 'set 2 / 28', 'set 2 / 36'].

## V1 uyuşmayan sayfalar

| sayfa | Cemal | V1 | V2 | V3 | DS6 | DS5 | GOVDE_1 | dip yaşı | düşüş | mavi düşüş (ATR) | dokunuş (ilk / ikinci) | dip sonrası en düşük Low (ATR) | i0 / dayanıklı j (dokunuş; affedilen) / zarf j* | C_t / T(t) - 1 | ilk kırılım / üst kapanış | düşen parça | kodun gördüğü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set 1 / 5 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 10 | %81 | 0.00 | 1 (1 / 0) | +0.66 | t-75 / t-41 (1; 0) / t-41 | %-7.2 | - / 0 | P3, KIRILIM | P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); KIRILIM son kapanış ana çizginin altında (%-7.2) |
| set 1 / 9 | YOK | VAR | VAR | VAR | YOK | YOK | VAR | 99 | %30 | 0.22 | 14 (9 / 5) | +0.15 | t-102 / yok (0; 0) / t-99 | - | t-98 / 99 | - | not: dayanıklı çizgi yok (saf zarf kullanıldı) |
| set 1 / 12 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 32 | %64 | 0.00 | 5 (0 / 5) | +1.24 | t-119 / t-43 (2; 0) / t-118 | %+31.2 | t-26 / 27 | P3 | P3 takip yok (dokunuş 5: ilk yarı 0, ikinci yarı 5) |
| set 1 / 17 | VAR | YOK | YOK | VAR | YOK | YOK | VAR | 21 | %137 | 0.00 | 6 (2 / 4) | +0.49 | t-87 / t-57 (1; 0) / t-56 | %-20.0 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-20.0) |
| set 1 / 19 | VAR | YOK | YOK | VAR | YOK | YOK | VAR | 14 | %51 | 0.00 | 5 (2 / 3) | +0.13 | t-117 / t-40 (2; 0) / t-40 | %-16.3 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-16.3) |
| set 1 / 20 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 24 | %134 | 2.12 | 1 (1 / 0) | +0.09 | t-114 / t-29 (2; 1) / t-88 | %-9.8 | - / 0 | P2, P3, KIRILIM | P2 mavi çizgi 2.12 ATR aşağı (> 0,5); P3 takip yok (dokunuş 1: ilk yarı 1, ikinci yarı 0); KIRILIM son kapanış ana çizginin altında (%-9.8) |
| set 1 / 21 | YOK | VAR | VAR | VAR | VAR | VAR | VAR | 55 | %59 | 0.00 | 4 (1 / 3) | +0.09 | t-102 / t-62 (3; 0) / t-59 | %+43.3 | t-45 / 46 | - | altı parça da DOĞRU (kod VAR) |
| set 1 / 28 | YOK | VAR | VAR | VAR | YOK | VAR | YOK | 31 | %50 | 0.00 | 7 (1 / 6) | +0.89 | t-78 / yok (0; 0) / t-47 | %+42.7 | t-28 / 29 | - | not: dayanıklı çizgi yok (saf zarf kullanıldı) |
| set 1 / 31 | YOK | VAR | VAR | VAR | YOK | YOK | VAR | 80 | %97 | 0.24 | 4 (1 / 3) | +0.02 | t-113 / yok (0; 0) / t-112 | %+297.3 | t-61 / 62 | - | not: dayanıklı çizgi yok (saf zarf kullanıldı) |
| set 1 / 34 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 68 | %163 | 0.00 | 12 (0 / 12) | +0.88 | t-119 / t-112 (1; 0) / t-112 | %-45.4 | - / 0 | P3, KIRILIM | P3 takip yok (dokunuş 12: ilk yarı 0, ikinci yarı 12); KIRILIM son kapanış ana çizginin altında (%-45.4) |
| set 1 / 39 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 43 | %93 | 0.00 | 4 (4 / 0) | +0.07 | t-73 / t-57 (1; 1) / t-44 | - | t-42 / 43 | P3 | P3 takip yok (dokunuş 4: ilk yarı 4, ikinci yarı 0) |
| set 1 / 40 | VAR | YOK | YOK | VAR | YOK | YOK | VAR | 12 | %71 | 0.08 | 5 (4 / 1) | +0.03 | t-83 / t-42 (2; 0) / t-41 | %-10.8 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-10.8) |
| set 2 / 2 | YOK | VAR | VAR | VAR | VAR | VAR | YOK | 57 | %78 | 0.00 | 6 (4 / 2) | +0.14 | t-87 / t-70 (2; 0) / t-79 | %+82.3 | t-43 / 44 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 3 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 44 | %50 | 11.36 | 2 (2 / 0) | +0.05 | t-117 / t-51 (6; 0) / t-76 | %-8.6 | - / 0 | P2, P3, KIRILIM | P2 mavi çizgi 11.36 ATR aşağı (> 0,5); P3 takip yok (dokunuş 2: ilk yarı 2, ikinci yarı 0); KIRILIM son kapanış ana çizginin altında (%-8.6) |
| set 2 / 9 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 28 | %163 | 0.13 | 3 (3 / 0) | +0.00 | t-113 / t-71 (2; 0) / t-71 | %-10.0 | - / 0 | P3, KIRILIM | P3 takip yok (dokunuş 3: ilk yarı 3, ikinci yarı 0); KIRILIM son kapanış ana çizginin altında (%-10.0) |
| set 2 / 10 | VAR | YOK | YOK | VAR | YOK | YOK | VAR | 18 | %71 | 0.00 | 9 (6 / 3) | +0.09 | t-50 / yok (0; 0) / t-40 | %-28.2 | - / 0 | KIRILIM | not: dayanıklı çizgi yok (saf zarf kullanıldı); KIRILIM son kapanış ana çizginin altında (%-28.2) |
| set 2 / 12 | YOK | VAR | VAR | VAR | YOK | VAR | YOK | 26 | %163 | 0.00 | 10 (1 / 9) | +0.24 | t-118 / t-45 (1; 0) / t-43 | %+41.2 | t-18 / 19 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 14 | VAR | YOK | YOK | VAR | YOK | YOK | VAR | 23 | %50 | 0.00 | 11 (1 / 10) | +0.67 | t-71 / t-54 (2; 0) / t-53 | %-16.8 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-16.8) |
| set 2 / 15 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 78 | %98 | 0.00 | 15 (0 / 15) | +0.37 | t-114 / t-90 (1; 0) / t-90 | %+2412.3 | t-76 / 77 | P3 | P3 takip yok (dokunuş 15: ilk yarı 0, ikinci yarı 15) |
| set 2 / 18 | VAR | YOK | YOK | VAR | YOK | VAR | VAR | 34 | %49 | 0.00 | 5 (1 / 4) | +0.41 | t-107 / t-94 (1; 0) / t-94 | %-13.2 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-13.2) |
| set 2 / 19 | VAR | YOK | YOK | VAR | YOK | VAR | VAR | 37 | %103 | 0.00 | 12 (2 / 10) | +0.08 | t-70 / t-59 (1; 0) / t-59 | %-32.8 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-32.8) |
| set 2 / 22 | YOK | VAR | VAR | VAR | VAR | VAR | VAR | 27 | %150 | 0.00 | 7 (4 / 3) | +0.12 | t-105 / t-37 (1; 0) / t-37 | %+22.0 | t-10 / 8 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 27 | VAR | YOK | YOK | YOK | YOK | YOK | VAR | 119 | %nan | 0.00 | 8 (4 / 4) | +0.64 | - | - | - / 0 | P1, TREND, KIRILIM | P1 düşüş yok (- < %20); TREND ana çizgi düşmüyor (d'den önce mum yok); KIRILIM son kapanış ana çizginin altında |
| set 2 / 28 | YOK | VAR | YOK | VAR | YOK | YOK | YOK | 12 | %82 | 0.00 | 5 (4 / 1) | +0.57 | t-75 / t-17 (1; 0) / t-72 | %+0.2 | t+0 / 1 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 30 | VAR | YOK | YOK | VAR | YOK | VAR | VAR | 17 | %38 | 0.00 | 10 (5 / 5) | +0.36 | t-84 / t-36 (1; 0) / t-82 | %-3.0 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-3.0) |
| set 2 / 36 | YOK | VAR | YOK | VAR | VAR | VAR | VAR | 12 | %191 | 0.00 | 4 (1 / 3) | +0.22 | t-116 / t-28 (2; 1) / t-104 | %+21.8 | t-8 / 9 | - | altı parça da DOĞRU (kod VAR) |
| set 2 / 37 | VAR | YOK | YOK | VAR | YOK | YOK | YOK | 14 | %29 | 0.00 | 11 (5 / 6) | +0.41 | t-61 / t-24 (4; 1) / t-45 | %-7.2 | - / 0 | KIRILIM | KIRILIM son kapanış ana çizginin altında (%-7.2) |

## Karşılaştırma: aynı sayfalarda DS6 V1, DS5 V1 ve GOVDE_1

- V1_DS6_V1: karar 79 sayfada iki kod 65 sayfada aynı yanıt (kodlar arası kappa 0.445); V1 doğru / öteki yanlış 9; öteki doğru / V1 yanlış 5.
- V1_DS5_V1: karar 79 sayfada iki kod 66 sayfada aynı yanıt (kodlar arası kappa 0.572); V1 doğru / öteki yanlış 7; öteki doğru / V1 yanlış 6.
- V1_GOVDE_1: karar 79 sayfada iki kod 37 sayfada aynı yanıt (kodlar arası kappa 0.044); V1 doğru / öteki yanlış 21; öteki doğru / V1 yanlış 21.

DS7 V1 ile DS6 V1'in ayrıldığı sayfalar: set 1 / 2 (Cemal YOK; DS6 VAR -> DS7 YOK; düşen KIRILIM), set 1 / 9 (Cemal YOK; DS6 YOK -> DS7 VAR; düşen -), set 1 / 14 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 1 / 26 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 1 / 28 (Cemal YOK; DS6 YOK -> DS7 VAR; düşen -), set 1 / 31 (Cemal YOK; DS6 YOK -> DS7 VAR; düşen -), set 1 / 32 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 1 / 37 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 2 / 12 (Cemal YOK; DS6 YOK -> DS7 VAR; düşen -), set 2 / 21 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 2 / 25 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 2 / 28 (Cemal YOK; DS6 YOK -> DS7 VAR; düşen -), set 2 / 32 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -), set 2 / 38 (Cemal VAR; DS6 YOK -> DS7 VAR; düşen -)

## DS6_ONAY sayfalarında v7 cevabı (BİLGİ; Cemal'in DS6_ONAY işaretleri tanım geri bildirimi)

İşaretli 17 sayfada v7 V1 Cemal'in genel hükmüyle uyumlu: **7 / 17** (YANLIŞ dediği 8 sayfada 2 itiraz giderildi; DOĞRU dediği 9 sayfada 5 korundu). Karşılaştırma: v6 aynı 17 sayfada 9 / 17 uyumluydu.

| sayfa | pazar | Cemal (DS6_ONAY) | v6 V1 | v7 V1 | v7 V2 | v7 V3 | Cemal'in beklediği | uyumlu | etiket | i0 / dayanıklı j (dokunuş; affedilen) / zarf j* | C_t / T(t) - 1 | ilk kırılım | v7 düşen parça | Cemal'in yazısı |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | YANLIŞ | YOK | VAR | YOK | VAR | VAR | EVET | itiraz giderildi | t-88 / t-29 (2; 2) / t-87 | %+40.8 | t-14 | - | DİP VAR / X kırd(ı)? (son kelime okunamadı) |
| 2 | ABD | İŞARETSİZ | YOK | YOK | YOK | VAR | - | - | işaretsiz | t-108 / t-61 (1; 0) / t-61 | %-12.6 | - | KIRILIM |  |
| 3 | ABD | DOĞRU | YOK | YOK | YOK | VAR | YOK | EVET | korundu | t-82 / t-63 (1; 0) / t-80 | %-18.0 | - | KIRILIM |  |
| 4 | ABD | YANLIŞ | YOK | YOK | YOK | VAR | VAR | HAYIR | itiraz sürüyor | t-80 / t-59 (2; 0) / t-54 | %-21.7 | - | KIRILIM |  |
| 5 | ABD | DOĞRU | YOK | VAR | VAR | VAR | YOK | HAYIR | DİKKAT: bozuldu | t-87 / t-63 (1; 0) / t-62 | %+22.2 | t-3 | - |  |
| 6 | ABD | İŞARETSİZ | YOK | YOK | YOK | VAR | - | - | işaretsiz | t-74 / t-47 (1; 0) / t-46 | %-24.0 | - | KIRILIM |  |
| 7 | ABD | DOĞRU | YOK | YOK | YOK | VAR | YOK | EVET | korundu | t-67 / yok (0; 0) / t-61 | %-18.4 | - | KIRILIM |  |
| 8 | ABD | YANLIŞ | YOK | YOK | YOK | VAR | VAR | HAYIR | itiraz sürüyor | t-115 / t-48 (1; 0) / t-114 | %-10.1 | - | KIRILIM | 1 / 2 / 3 / 2 ve 3 ara trend |
| 9 | ABD | DOĞRU | VAR | VAR | YOK | VAR | VAR | EVET | korundu | t-58 / t-31 (1; 0) / t-52 | %+51.3 | t-15 | - |  |
| 10 | ABD | DOĞRU | VAR | VAR | VAR | VAR | VAR | EVET | korundu | t-93 / t-21 (1; 0) / t-48 | %+50.0 | t-10 | - |  |
| 11 | ABD | İŞARETSİZ | YOK | VAR | YOK | VAR | - | - | işaretsiz (yanıt değişti) | t-46 / t-25 (1; 1) / t-38 | %+39.8 | t-18 | - |  |
| 12 | ABD | YANLIŞ | YOK | YOK | YOK | VAR | VAR | HAYIR | itiraz sürüyor | t-70 / t-51 (1; 0) / t-51 | %-28.4 | - | KIRILIM |  |
| 13 | AVR | DOĞRU | YOK | VAR | VAR | VAR | YOK | HAYIR | DİKKAT: bozuldu | t-67 / yok (0; 0) / t-20 | %+78.9 | t-19 | - |  |
| 14 | BIST | İŞARETSİZ | YOK | YOK | YOK | VAR | - | - | işaretsiz | t-100 / t-78 (1; 0) / t-77 | %-18.0 | - | KIRILIM |  |
| 15 | BIST | İŞARETSİZ | YOK | VAR | VAR | VAR | - | - | işaretsiz (yanıt değişti) | t-67 / t-51 (1; 1) / t-48 | %+24.2 | t-13 | - |  |
| 16 | AVR | YANLIŞ | YOK | VAR | YOK | VAR | VAR | EVET | itiraz giderildi | t-68 / t-36 (1; 1) / t-65 | %+125.1 | t-20 | - |  |
| 17 | AVR | YANLIŞ | YOK | YOK | YOK | YOK | VAR | HAYIR | itiraz sürüyor | t-80 / t-62 (1; 0) / t-62 | %-16.7 | - | P2, KIRILIM |  |
| 18 | AVR | İŞARETSİZ | YOK | VAR | YOK | VAR | - | - | işaretsiz (yanıt değişti) | t-107 / t-29 (2; 1) / t-65 | %+2.8 | t-1 | - |  |
| 19 | ABD | İŞARETSİZ | YOK | YOK | YOK | YOK | - | - | işaretsiz | t-116 / t-89 (2; 0) / t-102 | %-25.6 | - | P3, KIRILIM |  |
| 20 | ABD | DOĞRU | YOK | YOK | YOK | YOK | YOK | EVET | korundu | t-119 / t-49 (3; 0) / t-45 | %+17.9 | t-18 | P3 |  |
| 21 | ABD | YANLIŞ | YOK | YOK | YOK | YOK | VAR | HAYIR | itiraz sürüyor | t-102 / t-43 (1; 0) / t-95 | %+51.0 | t-33 | P2, P3 |  |
| 22 | ABD | YANLIŞ | YOK | YOK | YOK | VAR | VAR | HAYIR | itiraz sürüyor | t-118 / t-48 (1; 0) / t-46 | %-18.0 | - | KIRILIM |  |
| 23 | AVR | DOĞRU | VAR | YOK | YOK | VAR | VAR | HAYIR | DİKKAT: bozuldu | t-119 / t-107 (1; 0) / t-117 | %-14.1 | - | KIRILIM |  |
| 24 | ABD | DOĞRU | YOK | VAR | VAR | VAR | YOK | HAYIR | DİKKAT: bozuldu | t-66 / t-32 (1; 0) / t-32 | %+6.5 | t-1 | - |  |
| 25 | ABD | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-94 / t-47 (3; 0) / t-31 | %+41.9 | t-20 | - |  |
| 26 | ABD | İŞARETSİZ | VAR | VAR | YOK | VAR | - | - | işaretsiz | t-59 / t-24 (1; 0) / t-58 | %+8.6 | t-7 | - |  |
| 27 | BIST | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-104 / yok (0; 0) / t-40 | %+nan | t-38 | - |  |
| 28 | ABD | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-102 / t-29 (1; 0) / t-29 | %+11.3 | t-14 | - |  |
| 29 | ABD | İŞARETSİZ | VAR | VAR | YOK | VAR | - | - | işaretsiz | t-115 / t-61 (1; 0) / t-113 | %+nan | t-50 | - |  |
| 30 | ABD | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-54 / t-24 (1; 0) / t-22 | %+51.0 | t-16 | - |  |
| 31 | ABD | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-116 / t-67 (1; 0) / t-67 | %+91.6 | t-46 | - |  |
| 32 | AVR | İŞARETSİZ | VAR | VAR | VAR | VAR | - | - | işaretsiz | t-71 / t-14 (4; 0) / t-47 | %+7.3 | t-7 | - |  |
| 33 | ABD | İŞARETSİZ | YOK | YOK | YOK | YOK | - | - | işaretsiz | t-112 / t-94 (1; 0) / t-111 | %+45.5 | t-48 | P2, P3 |  |
| 34 | ABD | İŞARETSİZ | YOK | VAR | VAR | VAR | - | - | işaretsiz (yanıt değişti) | t-84 / t-60 (1; 1) / t-68 | %+338.0 | t-50 | - |  |
| 35 | ABD | İŞARETSİZ | YOK | VAR | YOK | VAR | - | - | işaretsiz (yanıt değişti) | t-119 / t-66 (2; 1) / t-117 | %+nan | t-53 | - |  |
| 36 | ABD | İŞARETSİZ | YOK | YOK | YOK | VAR | - | - | işaretsiz | t-56 / t-30 (1; 0) / t-28 | %-5.8 | - | KIRILIM |  |

Havuz (bilgi; 2849 olay): V1 VAR {"ABD": 396, "AVR": 26, "BIST": 42} (toplam 464); V2 344; V3 1110; v6 V1 210.

Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural iş tanımından, kör set etiketlerine bakmadan sabitlendi ve önce sentetik serilerde sınandı.
