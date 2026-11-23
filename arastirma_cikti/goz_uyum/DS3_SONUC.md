# DİP SAVUNMASI v3 (DS3) — SONUÇ (iki kör set, 80 sayfa)

Üretim: 2026-11-23T18:09:55Z (UTC). Etiket dosyaları (cemal_isaret.json, cemal_isaret2.json) bu komutla açıldı: 2026-11-23T18:09:53Z (UTC). Mühür denetimi: ds3_anahtar.json, ds3.py, DS3_ESIK ve kural kaynağı sha'ları DS3_ON_KAYIT ile aynı; 80 sayfanın V1 / V2 / V3 yanıtı veriden yeniden hesaplandı, mühürle aynı. GETİRİ YOK.

Karar: birleşik 79 (Cemal VAR 30); işaretsiz / '?' (karar dışı): 1 ['set 2 / 39'].

## HÜKÜM (V1, ön kayıttaki eşikle): **GEÇERSİZ** — birleşik kappa -0.150, %95 [-0.281, -0.006]

NOT: V1 kappa set 1 -0.007, set 2 -0.288: İKİ SETTE DE < 0,40 (iki set aynı yönde düşük; 'tutarsız' değil).

## Kappa tablosu

| model | küme | karar | kod VAR | uyum | kappa | %95 aralık | %98,33 (Bonferroni 3) | hüküm |
|---|---|---|---|---|---|---|---|---|
| V1 | set 1 | 40 | 3 | 0.625 | -0.007 | [-0.191, 0.219] | [-0.231, 0.280] | ayrı rapor |
| V1 | set 2 | 39 | 6 | 0.436 | -0.288 | [-0.456, -0.101] | [-0.496, -0.051] | ayrı rapor |
| V1 | birleşik | 79 | 9 | 0.532 | -0.150 | [-0.281, -0.006] | [-0.314, 0.026] | GEÇERSİZ |
| V2 | set 1 | 40 | 24 | 0.550 | 0.151 | [-0.130, 0.412] | [-0.177, 0.466] | bilgi |
| V2 | set 2 | 39 | 18 | 0.538 | 0.064 | [-0.251, 0.369] | [-0.320, 0.430] | bilgi |
| V2 | birleşik | 79 | 42 | 0.544 | 0.102 | [-0.108, 0.308] | [-0.153, 0.357] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| V3 | set 1 | 40 | 7 | 0.525 | -0.180 | [-0.383, 0.068] | [-0.417, 0.124] | bilgi |
| V3 | set 2 | 39 | 11 | 0.410 | -0.280 | [-0.517, 0.006] | [-0.567, 0.080] | bilgi |
| V3 | birleşik | 79 | 18 | 0.468 | -0.223 | [-0.390, -0.037] | [-0.417, 0.006] | BİLGİ (Bonferroni alt uç ile: GEÇERSİZ) |
| GOVDE_1 | set 1 | 40 | 23 | 0.675 | 0.378 | [0.128, 0.645] | [0.066, 0.700] | bilgi |
| GOVDE_1 | set 2 | 39 | 26 | 0.641 | 0.323 | [0.062, 0.586] | [0.015, 0.643] | bilgi |
| GOVDE_1 | birleşik | 79 | 49 | 0.658 | 0.354 | [0.176, 0.530] | [0.135, 0.568] | BİLGİ (önceki kural) |

V1 = a ∧ b ∧ c ∧ d (ANA); V2 = a ∧ b ∧ c1 ∧ d; V3 = a ∧ b ∧ c. GOVDE_1 = G4_fitil_govde_arasi <= 0.4046040192474485 (önceki en iyi; eşiği set 1 etiketleriyle seçildi -> set 1'de iç-örneklem, yalnız bilgi).

HÜKÜM kuralı (ön kayıt): V1 (ANA): iki set birleşik Cemal kararlarıyla (işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı ayrı da raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33) verilir, hüküm sözü yalnız V1 için.

## 2x2 (birleşik)

**V1**: Cemal VAR + kod VAR 1; Cemal YOK + kod YOK 41; Cemal YOK + kod VAR 8; Cemal VAR + kod YOK 29

**V2**: Cemal VAR + kod VAR 18; Cemal YOK + kod YOK 25; Cemal YOK + kod VAR 24; Cemal VAR + kod YOK 12

**V3**: Cemal VAR + kod VAR 3; Cemal YOK + kod YOK 34; Cemal YOK + kod VAR 15; Cemal VAR + kod YOK 27

**V1 set 1**: Cemal VAR + kod VAR 1; Cemal YOK + kod YOK 24; Cemal YOK + kod VAR 2; Cemal VAR + kod YOK 13

**V1 set 2**: Cemal VAR + kod VAR 0; Cemal YOK + kod YOK 17; Cemal YOK + kod VAR 6; Cemal VAR + kod YOK 16

## Cemal VAR dediği halde kodun YOK dediği sayfalarda düşen parça

| varyant | sayfa | düşen parça sayımı (bir sayfada birden çok olabilir) | yalnız bu parça düştü |
|---|---|---|---|
| V1 | 29 | (a) düşüş yok 0; (c1) dip delinmiş 0; (c2) hat iniyor 4; (c3) gövdeler hattın altında 27; (d) fitil küçülmüyor 12 | (a) düşüş yok 0; (c1) dip delinmiş 0; (c2) hat iniyor 0; (c3) gövdeler hattın altında 13; (d) fitil küçülmüyor 2 |
| V2 | 12 | (a) düşüş yok 0; (c1) dip delinmiş 0; (d) fitil küçülmüyor 12 | (a) düşüş yok 0; (c1) dip delinmiş 0; (d) fitil küçülmüyor 12 |
| V3 | 27 | (a) düşüş yok 0; (c1) dip delinmiş 0; (c2) hat iniyor 4; (c3) gövdeler hattın altında 27 | (a) düşüş yok 0; (c1) dip delinmiş 0; (c2) hat iniyor 0; (c3) gövdeler hattın altında 23 |

## V1 uyuşmayan sayfalar ve (a)-(d) değerleri

| sayfa | Cemal | V1 | V2 | V3 | GOVDE_1 | m | düşüş | dip sonrası en düşük Low | hat eğimi (ATR/mum) | gövde hattın üstünde | w ilk 1/3 -> son 1/3 (eğim) | kod neden YOK / ne gördü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| set 1 / 1 | YOK | VAR | VAR | VAR | VAR | 16 | %73 | +0.5% | +0.113 | %94 | 0.41 -> 0.18 (-0.0190) | dört parça da DOĞRU (kod VAR) |
| set 1 / 3 | VAR | YOK | VAR | YOK | VAR | 22 | %55 | +1.6% | +0.038 | %59 | 0.11 -> 0.04 (-0.0058) | gövdeler hattın üstünde değil (%59 < %80) |
| set 1 / 5 | VAR | YOK | VAR | YOK | VAR | 10 | %63 | +2.4% | +0.256 | %60 | 0.37 -> 0.22 (-0.0254) | gövdeler hattın üstünde değil (%60 < %80) |
| set 1 / 6 | YOK | VAR | VAR | VAR | VAR | 8 | %45 | +0.2% | +0.257 | %100 | 0.36 -> 0.30 (-0.0244) | dört parça da DOĞRU (kod VAR) |
| set 1 / 7 | VAR | YOK | VAR | YOK | YOK | 32 | %51 | +0.8% | +0.003 | %69 | 0.24 -> 0.20 (-0.0022) | gövdeler hattın üstünde değil (%69 < %80) |
| set 1 / 12 | VAR | YOK | YOK | YOK | VAR | 32 | %39 | +4.0% | +0.016 | %62 | 0.08 -> 0.12 (+0.0018) | gövdeler hattın üstünde değil (%62 < %80); fitil küçülmüyor (w eğim +0.0018, ilk 1/3 0.08 -> son 1/3 0.12) |
| set 1 / 14 | VAR | YOK | VAR | YOK | VAR | 42 | %94 | +1.7% | -0.039 | %52 | 0.19 -> 0.19 (-0.0002) | hat iniyor (eğim -0.039 ATR/mum); gövdeler hattın üstünde değil (%52 < %80) |
| set 1 / 17 | VAR | YOK | VAR | YOK | VAR | 21 | %109 | +4.6% | +0.013 | %71 | 0.15 -> 0.13 (-0.0024) | gövdeler hattın üstünde değil (%71 < %80) |
| set 1 / 19 | VAR | YOK | YOK | YOK | VAR | 14 | %39 | +0.4% | +0.046 | %71 | 0.19 -> 0.28 (+0.0066) | gövdeler hattın üstünde değil (%71 < %80); fitil küçülmüyor (w eğim +0.0066, ilk 1/3 0.19 -> son 1/3 0.28) |
| set 1 / 20 | VAR | YOK | YOK | YOK | VAR | 24 | %88 | +0.8% | +0.010 | %50 | 0.09 -> 0.13 (+0.0026) | gövdeler hattın üstünde değil (%50 < %80); fitil küçülmüyor (w eğim +0.0026, ilk 1/3 0.09 -> son 1/3 0.13) |
| set 1 / 26 | VAR | YOK | VAR | YOK | VAR | 45 | %131 | +1.8% | -0.018 | %40 | 0.28 -> 0.17 (-0.0025) | hat iniyor (eğim -0.018 ATR/mum); gövdeler hattın üstünde değil (%40 < %80) |
| set 1 / 34 | VAR | YOK | VAR | YOK | VAR | 31 | %50 | +0.4% | +0.013 | %61 | 0.14 -> 0.10 (-0.0031) | gövdeler hattın üstünde değil (%61 < %80) |
| set 1 / 37 | VAR | YOK | VAR | YOK | VAR | 22 | %68 | +1.7% | +0.017 | %64 | 0.25 -> 0.16 (-0.0072) | gövdeler hattın üstünde değil (%64 < %80) |
| set 1 / 39 | VAR | YOK | VAR | YOK | VAR | 43 | %93 | +0.4% | +0.020 | %58 | 0.23 -> 0.22 (-0.0014) | gövdeler hattın üstünde değil (%58 < %80) |
| set 1 / 40 | VAR | YOK | YOK | YOK | VAR | 12 | %60 | +0.2% | +0.030 | %67 | 0.23 -> 0.27 (+0.0032) | gövdeler hattın üstünde değil (%67 < %80); fitil küçülmüyor (w eğim +0.0032, ilk 1/3 0.23 -> son 1/3 0.27) |
| set 2 / 1 | YOK | VAR | VAR | VAR | VAR | 7 | %51 | +0.1% | +0.297 | %100 | 0.37 -> 0.12 (-0.0460) | dört parça da DOĞRU (kod VAR) |
| set 2 / 3 | VAR | YOK | VAR | YOK | VAR | 44 | %46 | +0.3% | -0.025 | %73 | 0.28 -> 0.13 (-0.0053) | hat iniyor (eğim -0.025 ATR/mum); gövdeler hattın üstünde değil (%73 < %80) |
| set 2 / 4 | YOK | VAR | VAR | VAR | YOK | 12 | %45 | +1.2% | +0.134 | %83 | 0.26 -> 0.19 (-0.0059) | dört parça da DOĞRU (kod VAR) |
| set 2 / 5 | YOK | VAR | VAR | VAR | VAR | 5 | %62 | +0.4% | +0.405 | %100 | 0.35 -> 0.12 (-0.0694) | dört parça da DOĞRU (kod VAR) |
| set 2 / 9 | VAR | YOK | VAR | YOK | VAR | 28 | %132 | +0.0% | +0.036 | %61 | 0.23 -> 0.09 (-0.0078) | gövdeler hattın üstünde değil (%61 < %80) |
| set 2 / 10 | VAR | YOK | YOK | YOK | VAR | 18 | %71 | +0.4% | +0.052 | %78 | 0.11 -> 0.23 (+0.0120) | gövdeler hattın üstünde değil (%78 < %80); fitil küçülmüyor (w eğim +0.0120, ilk 1/3 0.11 -> son 1/3 0.23) |
| set 2 / 14 | VAR | YOK | YOK | VAR | VAR | 23 | %50 | +3.5% | +0.009 | %87 | 0.12 -> 0.17 (+0.0028) | fitil küçülmüyor (w eğim +0.0028, ilk 1/3 0.12 -> son 1/3 0.17) |
| set 2 / 15 | VAR | YOK | YOK | VAR | VAR | 6 | %54 | +0.3% | +0.005 | %100 | 0.22 -> 0.16 (+0.0078) | fitil küçülmüyor (w eğim +0.0078, ilk 1/3 0.22 -> son 1/3 0.16) |
| set 2 / 18 | VAR | YOK | YOK | YOK | VAR | 34 | %47 | +1.2% | +0.014 | %71 | 0.22 -> 0.22 (+0.0004) | gövdeler hattın üstünde değil (%71 < %80); fitil küçülmüyor (w eğim +0.0004, ilk 1/3 0.22 -> son 1/3 0.22) |
| set 2 / 19 | VAR | YOK | VAR | YOK | VAR | 37 | %103 | +0.7% | -0.014 | %62 | 0.15 -> 0.14 (-0.0006) | hat iniyor (eğim -0.014 ATR/mum); gövdeler hattın üstünde değil (%62 < %80) |
| set 2 / 20 | YOK | VAR | VAR | VAR | YOK | 8 | %74 | +0.7% | +0.198 | %88 | 0.62 -> 0.15 (-0.0850) | dört parça da DOĞRU (kod VAR) |
| set 2 / 21 | VAR | YOK | YOK | YOK | YOK | 14 | %37 | +2.1% | +0.047 | %79 | 0.07 -> 0.10 (+0.0064) | gövdeler hattın üstünde değil (%79 < %80); fitil küçülmüyor (w eğim +0.0064, ilk 1/3 0.07 -> son 1/3 0.10) |
| set 2 / 23 | VAR | YOK | VAR | YOK | VAR | 16 | %55 | +0.5% | +0.069 | %62 | 0.32 -> 0.28 (-0.0013) | gövdeler hattın üstünde değil (%62 < %80) |
| set 2 / 25 | VAR | YOK | VAR | YOK | VAR | 29 | %126 | +2.6% | +0.022 | %72 | 0.31 -> 0.25 (-0.0037) | gövdeler hattın üstünde değil (%72 < %80) |
| set 2 / 27 | VAR | YOK | VAR | YOK | VAR | 13 | %73 | +0.2% | +0.058 | %77 | 0.21 -> 0.11 (-0.0118) | gövdeler hattın üstünde değil (%77 < %80) |
| set 2 / 28 | YOK | VAR | VAR | VAR | YOK | 12 | %81 | +4.5% | +0.090 | %83 | 0.25 -> 0.18 (-0.0094) | dört parça da DOĞRU (kod VAR) |
| set 2 / 29 | VAR | YOK | YOK | YOK | VAR | 20 | %57 | +0.2% | +0.039 | %65 | 0.15 -> 0.24 (+0.0031) | gövdeler hattın üstünde değil (%65 < %80); fitil küçülmüyor (w eğim +0.0031, ilk 1/3 0.15 -> son 1/3 0.24) |
| set 2 / 30 | VAR | YOK | YOK | YOK | VAR | 17 | %29 | +1.2% | +0.084 | %59 | 0.06 -> 0.18 (+0.0086) | gövdeler hattın üstünde değil (%59 < %80); fitil küçülmüyor (w eğim +0.0086, ilk 1/3 0.06 -> son 1/3 0.18) |
| set 2 / 32 | VAR | YOK | VAR | YOK | VAR | 22 | %89 | +2.1% | +0.034 | %73 | 0.19 -> 0.12 (-0.0035) | gövdeler hattın üstünde değil (%73 < %80) |
| set 2 / 34 | YOK | VAR | VAR | VAR | VAR | 6 | %57 | +3.3% | +0.300 | %83 | 0.28 -> 0.11 (-0.0354) | dört parça da DOĞRU (kod VAR) |
| set 2 / 37 | VAR | YOK | VAR | YOK | YOK | 14 | %29 | +1.6% | +0.045 | %79 | 0.31 -> 0.11 (-0.0184) | gövdeler hattın üstünde değil (%79 < %80) |
| set 2 / 38 | VAR | YOK | YOK | YOK | VAR | 18 | %63 | +3.4% | +0.085 | %56 | 0.13 -> 0.20 (+0.0028) | gövdeler hattın üstünde değil (%56 < %80); fitil küçülmüyor (w eğim +0.0028, ilk 1/3 0.13 -> son 1/3 0.20) |

## Ek bilgi: V1 ile GOVDE_1 aynı sayfalarda

Karar 79 sayfada iki kod 31 sayfada aynı yanıtı verdi (iki kod arası kappa -0.025); V1 doğru / GOVDE_1 yanlış 19 sayfa; GOVDE_1 doğru / V1 yanlış 29 sayfa.

Not: uyum Cemal'in gözüyle uyumdur; getiri ölçülmedi. Kural Cemal'in cümlesinden etiketlere bakmadan sabitlendi (Ç211 dersi).
