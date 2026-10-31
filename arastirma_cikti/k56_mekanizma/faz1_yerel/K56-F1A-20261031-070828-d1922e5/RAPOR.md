# K56-F1A FAZ 1 YEREL ANALİZLER (KEŞİF 2016-21; keşif verisi yeniden kullanımı) (K56-F1A-20261031-070828-d1922e5)

- commit d1922e5; kilit sha 43d25ae2039d; evren sürümü 0d00d2c97608; süre 18.9 dk.
- Olay oranı (olay / likit satır): {"Y60": 0.00376, "Y120": 0.00192, "Y250": 0.00095}.
- Kalibre sentetik (duyarlılık, bilgisiz yapay veri): tek spek sınıfları {('kalibre_gjr', 'MEKANIK_ACIKLAR'): 119, ('kalibre_gjr', 'MEKANIK_IZ_YOK'): 6, ('kalibre_sicrama', 'MEKANIK_ACIKLAR'): 116, ('kalibre_sicrama', 'MEKANIK_IZ_YOK'): 8, ('kalibre_sicrama', 'TERS_ISARET'): 1}; sentetik / gerçek d oranı medyanı {'kalibre_gjr': 1.45, 'kalibre_sicrama': 1.41}; yapay olay oranı {'kalibre_gjr': {'Y60': 0.00242, 'Y120': 0.00097, 'Y250': 0.00029}, 'kalibre_sicrama': {'Y60': 0.00189, 'Y120': 0.00073, 'Y250': 0.00023}} (gerçeğin altında: kalibrasyon kuyrukları tam üretmiyor).
- A3 SONRASI sütunları AÇIKLAYICIDIR (olaydan sonraki bilgi); hiçbir sinyalde kullanılmaz. ÖNCESİ yalnız t0−1'e kadar başvurular (sızıntı kapısı).

## Özet (sayılardan)

- A1 / B2 seçimsiz kontrol, satır: {'MEKANİK (gerçek + sentetik)': 104, 'MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor)': 12, 'TERS KALINTI': 7, 'KISMEN MEKANİK': 2}; hücre: {'MEKANİK': 22, 'TERS KALINTI': 2, 'KISMEN MEKANİK': 1}.
- GERÇEK ETKİ KALIYOR satırı: 0 / 125. d(ii) / d(i) medyanı 0.039 (d(i) medyanı -0.265, d(ii) medyanı -0.014).
- (iii) duyarlılık (olay dizisinden rastgele gün): {'GERÇEK ETKİ KALIYOR': 123, 'KISMEN MEKANİK': 2}; (ii) ile sınıfı farklı satır 125.
- Açıklayıcı tanı (ön kayıt dışı, karar değiştirmez): olay dizisinin bütün günleri d medyanı -0.016; olay dizisi DIŞINDAKİ nitelikli günler d medyanı -0.013 (işareti d(i)'ye ters satır 50 / 125). (iii) yalnız ilk günün seçimini kaldırır; olayın başlattığı dizinin (yükseliş epizodunun ilk dizisi) seçimini kaldırmaz. Bir günün nitelikli olup olmayacağı sorusunun karşılığı (ii)'dir.
- A2 kalan etki: 9 satır; en az bir denetimin AÇIKLADIĞI (küçülme >= 0,50) satır 2; denetim başına AÇIKLAR sayısı {M03a: 0, M03b: 0, M16a: 1, M16b: 2, M18: 0}. (Küçük d(ii)'de küçülme oranı oynaktır.)
- A3 bileşim, aralığı 0'ı dışlayan: Y60 once_8k_202 G1 > G7 (+0.015); Y60 sonra_birlesme G1 < G7 (-0.021); Y120 sonra_ihrac G1 > G7 (+0.066); Y250 once_8k G1 > G7 (+0.051); Y250 sonra_ihrac G1 > G7 (+0.100).

## A1 seçimsiz kontrol: satır sınıfları

| sinif_a1 | n |
|---|---|
| MEKANİK (gerçek + sentetik) | 104 |
| MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | 12 |
| TERS KALINTI | 7 |
| KISMEN MEKANİK | 2 |

Ufuk × sınıf:

| ufuk | KISMEN MEKANİK | MEKANİK (gerçek + sentetik) | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | TERS KALINTI |
|---|---|---|---|---|
| Y120 | 0 | 34 | 0 | 4 |
| Y250 | 1 | 43 | 12 | 3 |
| Y60 | 1 | 27 | 0 | 0 |

## Hücre sınıfları (KEŞİF satırlarının çoğunluğu)

| hucre | satir | a1 | a1_iii | iii_farkli |
|---|---|---|---|---|
| D01-S02 | 11 | MEKANİK | GERÇEK ETKİ KALIYOR | 11 |
| D01-S05 | 3 | MEKANİK | GERÇEK ETKİ KALIYOR | 3 |
| D01-S07 | 2 | MEKANİK | GERÇEK ETKİ KALIYOR | 2 |
| D01-S08 | 2 | MEKANİK | GERÇEK ETKİ KALIYOR | 2 |
| D01-S10 | 1 | MEKANİK | GERÇEK ETKİ KALIYOR | 1 |
| D02-S02 | 10 | MEKANİK | GERÇEK ETKİ KALIYOR | 10 |
| D02-S05 | 3 | MEKANİK | GERÇEK ETKİ KALIYOR | 3 |
| D02-S06 | 4 | MEKANİK | GERÇEK ETKİ KALIYOR | 4 |
| D02-S08 | 12 | MEKANİK | GERÇEK ETKİ KALIYOR | 12 |
| D03-S02 | 5 | MEKANİK | GERÇEK ETKİ KALIYOR | 5 |
| D04-S04 | 1 | KISMEN MEKANİK | GERÇEK ETKİ KALIYOR | 1 |
| D04-S06 | 2 | MEKANİK | GERÇEK ETKİ KALIYOR | 2 |
| D05-S01 | 7 | MEKANİK | GERÇEK ETKİ KALIYOR | 7 |
| D05-S02 | 8 | MEKANİK | GERÇEK ETKİ KALIYOR | 8 |
| D05-S03 | 3 | MEKANİK | GERÇEK ETKİ KALIYOR | 3 |
| D05-S04 | 6 | MEKANİK | GERÇEK ETKİ KALIYOR | 6 |
| D05-S08 | 7 | MEKANİK | GERÇEK ETKİ KALIYOR | 7 |
| D06-S01 | 9 | MEKANİK | GERÇEK ETKİ KALIYOR | 9 |
| D06-S03 | 12 | MEKANİK | GERÇEK ETKİ KALIYOR | 12 |
| D06-S04 | 6 | MEKANİK | GERÇEK ETKİ KALIYOR | 6 |
| D06-S05 | 1 | MEKANİK | GERÇEK ETKİ KALIYOR | 1 |
| D06-S09 | 5 | MEKANİK | GERÇEK ETKİ KALIYOR | 5 |
| D10-S02 | 1 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 1 |
| D10-S09 | 3 | MEKANİK | GERÇEK ETKİ KALIYOR | 3 |
| D10-S10 | 1 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 1 |

## Satırlar (d: (i) ilk geçiş, (ii) bütün nitelikli günler, (iii) rastgele gün)

| hucre | varyant | ufuk | i_n_olay | i_d | ii_n_olay | ii_d | ii_d_alt | ii_d_ust | iii_d | r_ii | sent_oran_faz0 | sinif_a1 | sinif_iii | ayr_d | tani_dizi_d | tani_dis_d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/10 | Y120 | 2062 | -0.281 | 77125 | -0.015 | -0.044 | 0.013 | -0.271 | 0.054 | 0.994 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.025 | -0.029 | -0.005 |
| D01-S02 | D01-S02/10 | Y250 | 895 | -0.378 | 55079 | -0.007 | -0.027 | 0.012 | -0.302 | 0.019 | 0.770 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.021 | -0.023 | 0.001 |
| D01-S02 | D01-S02/10 | Y60 | 4292 | -0.289 | 88842 | -0.036 | -0.061 | -0.011 | -0.255 | 0.125 | 0.943 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.047 | -0.036 | -0.035 |
| D01-S02 | D01-S02/20 | Y120 | 2062 | -0.211 | 77125 | -0.030 | -0.059 | 0.000 | -0.237 | 0.144 | 1.352 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.045 | -0.041 | -0.022 |
| D01-S02 | D01-S02/20 | Y250 | 895 | -0.306 | 55079 | -0.018 | -0.068 | 0.026 | -0.253 | 0.060 | 0.905 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.035 | -0.052 | -0.001 |
| D01-S02 | D01-S02/20 | Y60 | 4292 | -0.235 | 88842 | -0.049 | -0.086 | -0.015 | -0.253 | 0.210 | 1.079 | KISMEN MEKANİK | GERÇEK ETKİ KALIYOR | -0.062 | -0.081 | -0.021 |
| D01-S02 | D01-S02/40 | Y120 | 2062 | -0.221 | 77125 | -0.012 | -0.043 | 0.020 | -0.267 | 0.053 | 1.263 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.009 | -0.046 | 0.012 |
| D01-S02 | D01-S02/5 | Y120 | 2062 | -0.255 | 77125 | -0.010 | -0.025 | 0.007 | -0.124 | 0.038 | 1.100 | MEKANİK (gerçek + sentetik) | KISMEN MEKANİK | -0.011 | 0.002 | -0.018 |
| D01-S02 | D01-S02/5 | Y250 | 895 | -0.360 | 55079 | -0.009 | -0.021 | 0.006 | -0.170 | 0.024 | 0.891 | MEKANİK (gerçek + sentetik) | KISMEN MEKANİK | -0.009 | -0.004 | -0.011 |
| D01-S02 | D01-S02/5 | Y60 | 4292 | -0.251 | 88842 | -0.016 | -0.029 | -0.003 | -0.157 | 0.064 | 1.088 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.018 | -0.000 | -0.029 |
| D01-S02 | D01-S02/60 | Y120 | 2062 | -0.235 | 77125 | 0.001 | -0.035 | 0.037 | -0.234 | -0.004 | 1.076 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.027 | -0.055 | 0.040 |
| D01-S05 | D01-S05/20 | Y250 | 895 | -0.218 | 55079 | -0.017 | -0.047 | 0.020 | -0.172 | 0.076 | 0.453 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | -0.040 | -0.044 | -0.002 |
| D01-S05 | D01-S05/40 | Y250 | 895 | -0.246 | 55079 | -0.021 | -0.054 | 0.022 | -0.205 | 0.086 | 0.352 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | -0.033 | -0.074 | 0.007 |
| D01-S05 | D01-S05/60 | Y250 | 895 | -0.236 | 55079 | -0.012 | -0.046 | 0.038 | -0.193 | 0.050 | 0.430 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | -0.029 | -0.070 | 0.018 |
| D01-S07 | D01-S07/10 | Y250 | 895 | -0.224 | 55079 | -0.006 | -0.026 | 0.013 | -0.175 | 0.027 | 0.963 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.002 | -0.060 | 0.022 |
| D01-S07 | D01-S07/5 | Y250 | 895 | -0.218 | 55079 | -0.009 | -0.026 | 0.007 | -0.137 | 0.043 | 0.956 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.010 | -0.047 | 0.010 |
| D01-S08 | D01-S08/20 | Y250 | 895 | -0.230 | 55079 | -0.017 | -0.051 | 0.031 | -0.227 | 0.074 | 1.601 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.016 | 0.008 | -0.030 |
| D01-S08 | D01-S08/20 | Y60 | 4292 | -0.215 | 88842 | -0.033 | -0.062 | -0.000 | -0.201 | 0.154 | 1.096 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.042 | -0.006 | -0.056 |
| D01-S10 | D01-S10/20 | Y250 | 895 | 0.303 | 55079 | -0.007 | -0.039 | 0.029 | 0.310 | -0.022 | 0.516 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.008 | 0.069 | -0.046 |
| D02-S02 | D02-S02/10 | Y120 | 2062 | 0.282 | 77125 | -0.003 | -0.033 | 0.026 | 0.277 | -0.010 | 1.614 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.004 | -0.014 | 0.005 |
| D02-S02 | D02-S02/10 | Y250 | 895 | 0.375 | 55079 | 0.002 | -0.035 | 0.032 | 0.345 | 0.005 | 1.366 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.002 | -0.021 | 0.013 |
| D02-S02 | D02-S02/10 | Y60 | 4292 | 0.292 | 88842 | 0.018 | -0.007 | 0.042 | 0.276 | 0.060 | 1.294 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.025 | 0.023 | 0.013 |
| D02-S02 | D02-S02/20 | Y120 | 2062 | 0.212 | 77125 | -0.021 | -0.058 | 0.014 | 0.218 | -0.097 | 1.895 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.031 | -0.022 | -0.019 |
| D02-S02 | D02-S02/20 | Y250 | 895 | 0.312 | 55079 | -0.006 | -0.053 | 0.032 | 0.279 | -0.018 | 1.572 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.024 | -0.027 | 0.006 |
| D02-S02 | D02-S02/20 | Y60 | 4292 | 0.213 | 88842 | -0.001 | -0.034 | 0.029 | 0.227 | -0.005 | 1.405 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.004 | 0.020 | -0.019 |
| D02-S02 | D02-S02/40 | Y250 | 895 | 0.256 | 55079 | -0.023 | -0.083 | 0.021 | 0.264 | -0.090 | 1.778 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.058 | -0.046 | -0.011 |
| D02-S02 | D02-S02/5 | Y120 | 2062 | 0.285 | 77125 | 0.007 | -0.020 | 0.032 | 0.231 | 0.025 | 1.729 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.007 | -0.012 | 0.020 |
| D02-S02 | D02-S02/5 | Y250 | 895 | 0.363 | 55079 | 0.008 | -0.026 | 0.034 | 0.340 | 0.022 | 1.483 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.004 | -0.015 | 0.020 |
| D02-S02 | D02-S02/5 | Y60 | 4292 | 0.319 | 88842 | 0.022 | 0.003 | 0.039 | 0.282 | 0.067 | 1.356 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.024 | 0.012 | 0.029 |
| D02-S05 | D02-S05/20 | Y250 | 895 | 0.263 | 55079 | 0.015 | -0.010 | 0.053 | 0.191 | 0.059 | 0.229 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.023 | 0.060 | -0.008 |
| D02-S05 | D02-S05/40 | Y250 | 895 | 0.226 | 55079 | -0.005 | -0.038 | 0.044 | 0.191 | -0.022 | 0.007 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.016 | 0.052 | -0.034 |
| D02-S05 | D02-S05/60 | Y250 | 895 | 0.209 | 55079 | -0.013 | -0.051 | 0.043 | 0.198 | -0.063 | -0.144 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.003 | 0.053 | -0.047 |
| D02-S06 | D02-S06/10 | Y250 | 895 | 0.317 | 55079 | 0.023 | 0.000 | 0.050 | 0.223 | 0.073 | 0.323 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.031 | 0.078 | -0.005 |
| D02-S06 | D02-S06/20 | Y250 | 895 | 0.335 | 55079 | 0.034 | 0.003 | 0.072 | 0.269 | 0.102 | 0.197 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.045 | 0.100 | -0.001 |
| D02-S06 | D02-S06/40 | Y250 | 895 | 0.307 | 55079 | 0.049 | 0.004 | 0.107 | 0.276 | 0.158 | 0.117 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.069 | 0.118 | 0.012 |
| D02-S06 | D02-S06/60 | Y250 | 895 | 0.283 | 55079 | 0.046 | 0.001 | 0.108 | 0.278 | 0.162 | 0.057 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | 0.057 | 0.117 | 0.008 |
| D02-S08 | D02-S08/10 | Y120 | 2062 | -0.401 | 77125 | 0.033 | 0.002 | 0.067 | -0.365 | -0.082 | 1.468 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 0.031 | -0.053 | 0.092 |
| D02-S08 | D02-S08/10 | Y250 | 895 | -0.631 | 55079 | 0.014 | -0.014 | 0.043 | -0.500 | -0.022 | 1.015 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.011 | -0.073 | 0.059 |
| D02-S08 | D02-S08/10 | Y60 | 4292 | -0.364 | 88842 | 0.009 | -0.012 | 0.034 | -0.311 | -0.026 | 1.333 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.001 | -0.081 | 0.087 |
| D02-S08 | D02-S08/20 | Y120 | 2062 | -0.316 | 77125 | 0.047 | 0.011 | 0.084 | -0.324 | -0.148 | 1.691 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 0.050 | -0.051 | 0.113 |
| D02-S08 | D02-S08/20 | Y250 | 895 | -0.583 | 55079 | 0.014 | -0.021 | 0.050 | -0.501 | -0.023 | 1.042 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.012 | -0.087 | 0.065 |
| D02-S08 | D02-S08/20 | Y60 | 4292 | -0.280 | 88842 | 0.009 | -0.018 | 0.041 | -0.284 | -0.034 | 1.453 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.002 | -0.095 | 0.098 |
| D02-S08 | D02-S08/40 | Y120 | 2062 | -0.220 | 77125 | 0.081 | 0.041 | 0.125 | -0.257 | -0.366 | 1.933 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 0.092 | -0.019 | 0.148 |
| D02-S08 | D02-S08/40 | Y250 | 895 | -0.502 | 55079 | 0.017 | -0.021 | 0.064 | -0.478 | -0.033 | 1.147 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.012 | -0.094 | 0.074 |
| D02-S08 | D02-S08/5 | Y120 | 2062 | -0.411 | 77125 | 0.025 | -0.001 | 0.052 | -0.320 | -0.061 | 1.473 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.023 | -0.045 | 0.073 |
| D02-S08 | D02-S08/5 | Y250 | 895 | -0.650 | 55079 | 0.007 | -0.018 | 0.030 | -0.465 | -0.010 | 0.971 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.005 | -0.070 | 0.046 |
| D02-S08 | D02-S08/5 | Y60 | 4292 | -0.386 | 88842 | 0.011 | -0.007 | 0.032 | -0.284 | -0.029 | 1.373 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.006 | -0.059 | 0.071 |
| D02-S08 | D02-S08/60 | Y250 | 895 | -0.456 | 55079 | 0.035 | -0.015 | 0.102 | -0.426 | -0.076 | 1.109 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.040 | -0.086 | 0.096 |
| D03-S02 | D03-S02/20 | Y120 | 2062 | 0.252 | 77125 | -0.017 | -0.051 | 0.012 | 0.261 | -0.068 | 1.958 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.016 | 0.015 | -0.039 |
| D03-S02 | D03-S02/20 | Y250 | 895 | 0.375 | 55079 | -0.000 | -0.051 | 0.041 | 0.328 | -0.000 | 1.621 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.006 | 0.020 | -0.010 |
| D03-S02 | D03-S02/20 | Y60 | 4292 | 0.220 | 88842 | 0.001 | -0.027 | 0.029 | 0.211 | 0.005 | 1.670 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.010 | 0.049 | -0.040 |
| D03-S02 | D03-S02/40 | Y250 | 895 | 0.370 | 55079 | -0.014 | -0.079 | 0.026 | 0.322 | -0.038 | 1.451 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.017 | 0.039 | -0.041 |
| D03-S02 | D03-S02/60 | Y250 | 895 | 0.328 | 55079 | -0.042 | -0.115 | 0.005 | 0.276 | -0.129 | 1.490 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.050 | 0.021 | -0.074 |
| D04-S04 | D04-S04/tek | Y250 | 895 | -0.264 | 55079 | -0.076 | -0.117 | -0.038 | -0.163 | 0.287 | 0.239 | KISMEN MEKANİK | GERÇEK ETKİ KALIYOR | -0.109 | -0.088 | -0.068 |
| D04-S06 | D04-S06/tek | Y120 | 2062 | -0.211 | 77125 | -0.024 | -0.044 | -0.005 | -0.170 | 0.114 | 1.397 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.028 | -0.092 | 0.024 |
| D04-S06 | D04-S06/tek | Y250 | 895 | -0.315 | 55079 | -0.017 | -0.042 | 0.008 | -0.217 | 0.053 | 0.751 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.017 | -0.069 | 0.011 |
| D05-S01 | D05-S01/10 | Y120 | 2062 | -0.277 | 77125 | -0.016 | -0.052 | 0.019 | -0.247 | 0.059 | 1.347 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.013 | -0.015 | -0.017 |
| D05-S01 | D05-S01/10 | Y250 | 895 | -0.371 | 55079 | -0.019 | -0.050 | 0.021 | -0.280 | 0.052 | 1.182 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.006 | -0.024 | -0.016 |
| D05-S01 | D05-S01/10 | Y60 | 4292 | -0.274 | 88842 | -0.029 | -0.056 | 0.000 | -0.250 | 0.107 | 1.181 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.025 | -0.027 | -0.030 |
| D05-S01 | D05-S01/20 | Y120 | 2062 | -0.224 | 77125 | -0.018 | -0.062 | 0.032 | -0.231 | 0.080 | 1.421 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.005 | -0.024 | -0.013 |
| D05-S01 | D05-S01/5 | Y120 | 2062 | -0.304 | 77125 | -0.011 | -0.040 | 0.017 | -0.209 | 0.037 | 1.352 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.010 | 0.000 | -0.019 |
| D05-S01 | D05-S01/5 | Y250 | 895 | -0.405 | 55079 | -0.016 | -0.040 | 0.017 | -0.275 | 0.039 | 1.153 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.006 | -0.008 | -0.020 |
| D05-S01 | D05-S01/5 | Y60 | 4292 | -0.324 | 88842 | -0.028 | -0.052 | -0.004 | -0.256 | 0.087 | 1.182 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.026 | -0.016 | -0.038 |
| D05-S02 | D05-S02/10 | Y120 | 2062 | -0.350 | 77125 | -0.004 | -0.041 | 0.032 | -0.325 | 0.010 | 1.246 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.000 | -0.010 | 0.001 |
| D05-S02 | D05-S02/10 | Y250 | 895 | -0.453 | 55079 | -0.020 | -0.052 | 0.019 | -0.398 | 0.045 | 1.125 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.009 | -0.031 | -0.015 |
| D05-S02 | D05-S02/10 | Y60 | 4292 | -0.336 | 88842 | -0.020 | -0.050 | 0.013 | -0.296 | 0.058 | 1.122 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.021 | -0.021 | -0.018 |
| D05-S02 | D05-S02/20 | Y120 | 2062 | -0.260 | 77125 | 0.007 | -0.040 | 0.056 | -0.271 | -0.026 | 1.450 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.019 | -0.000 | 0.012 |
| D05-S02 | D05-S02/20 | Y60 | 4292 | -0.240 | 88842 | -0.004 | -0.042 | 0.039 | -0.238 | 0.016 | 1.230 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.001 | -0.020 | 0.011 |
| D05-S02 | D05-S02/5 | Y120 | 2062 | -0.391 | 77125 | -0.006 | -0.036 | 0.027 | -0.273 | 0.015 | 1.226 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.005 | 0.002 | -0.011 |
| D05-S02 | D05-S02/5 | Y250 | 895 | -0.494 | 55079 | -0.020 | -0.043 | 0.011 | -0.295 | 0.040 | 1.121 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.013 | -0.015 | -0.022 |
| D05-S02 | D05-S02/5 | Y60 | 4292 | -0.396 | 88842 | -0.023 | -0.045 | 0.003 | -0.319 | 0.058 | 1.128 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.025 | -0.008 | -0.035 |
| D05-S03 | D05-S03/10 | Y250 | 895 | 0.389 | 55079 | -0.048 | -0.096 | 0.001 | 0.291 | -0.124 | 0.222 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | -0.045 | 0.020 | -0.082 |
| D05-S03 | D05-S03/20 | Y250 | 895 | 0.345 | 55079 | -0.069 | -0.118 | -0.014 | 0.275 | -0.201 | 0.172 | TERS KALINTI | GERÇEK ETKİ KALIYOR | -0.062 | 0.001 | -0.104 |
| D05-S03 | D05-S03/5 | Y250 | 895 | 0.410 | 55079 | -0.037 | -0.083 | 0.009 | 0.265 | -0.089 | 0.357 | MEKANİK (gerçek veri; sentetik DGP yeniden üretmiyor) | GERÇEK ETKİ KALIYOR | -0.038 | 0.023 | -0.067 |
| D05-S04 | D05-S04/10 | Y120 | 2062 | -0.235 | 77125 | -0.013 | -0.042 | 0.017 | -0.205 | 0.056 | 1.404 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.008 | -0.006 | -0.018 |
| D05-S04 | D05-S04/10 | Y250 | 895 | -0.317 | 55079 | -0.012 | -0.039 | 0.024 | -0.269 | 0.038 | 1.266 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.003 | -0.030 | -0.002 |
| D05-S04 | D05-S04/10 | Y60 | 4292 | -0.237 | 88842 | -0.028 | -0.051 | -0.003 | -0.210 | 0.116 | 1.252 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.028 | -0.027 | -0.027 |
| D05-S04 | D05-S04/5 | Y120 | 2062 | -0.242 | 77125 | -0.009 | -0.032 | 0.016 | -0.160 | 0.036 | 1.495 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.006 | 0.007 | -0.019 |
| D05-S04 | D05-S04/5 | Y250 | 895 | -0.336 | 55079 | -0.011 | -0.031 | 0.018 | -0.198 | 0.032 | 1.245 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.001 | -0.014 | -0.009 |
| D05-S04 | D05-S04/5 | Y60 | 4292 | -0.268 | 88842 | -0.027 | -0.045 | -0.007 | -0.194 | 0.100 | 1.301 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.026 | -0.016 | -0.035 |
| D05-S08 | D05-S08/10 | Y120 | 2062 | -0.302 | 77125 | -0.014 | -0.043 | 0.016 | -0.263 | 0.046 | 1.417 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.011 | -0.003 | -0.021 |
| D05-S08 | D05-S08/10 | Y250 | 895 | -0.348 | 55079 | -0.029 | -0.051 | -0.001 | -0.320 | 0.082 | 1.485 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.023 | -0.025 | -0.030 |
| D05-S08 | D05-S08/10 | Y60 | 4292 | -0.286 | 88842 | -0.027 | -0.050 | -0.003 | -0.256 | 0.093 | 1.303 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.035 | -0.035 | -0.018 |
| D05-S08 | D05-S08/20 | Y120 | 2062 | -0.219 | 77125 | -0.006 | -0.041 | 0.032 | -0.220 | 0.026 | 1.726 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.004 | 0.009 | -0.016 |
| D05-S08 | D05-S08/5 | Y120 | 2062 | -0.333 | 77125 | -0.015 | -0.040 | 0.011 | -0.222 | 0.046 | 1.401 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.015 | -0.002 | -0.024 |
| D05-S08 | D05-S08/5 | Y250 | 895 | -0.390 | 55079 | -0.028 | -0.047 | -0.003 | -0.269 | 0.071 | 1.404 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.024 | -0.020 | -0.031 |
| D05-S08 | D05-S08/5 | Y60 | 4292 | -0.336 | 88842 | -0.028 | -0.044 | -0.009 | -0.265 | 0.083 | 1.284 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.031 | -0.020 | -0.034 |
| D06-S01 | D06-S01/10 | Y120 | 2062 | -0.346 | 77125 | -0.029 | -0.060 | 0.004 | -0.351 | 0.084 | 1.279 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.040 | -0.041 | -0.020 |
| D06-S01 | D06-S01/10 | Y250 | 895 | -0.456 | 55079 | -0.018 | -0.051 | 0.014 | -0.403 | 0.040 | 1.006 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.037 | -0.033 | -0.010 |
| D06-S01 | D06-S01/10 | Y60 | 4292 | -0.382 | 88842 | -0.057 | -0.089 | -0.026 | -0.352 | 0.150 | 1.084 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.074 | -0.077 | -0.039 |
| D06-S01 | D06-S01/20 | Y120 | 2062 | -0.233 | 77125 | -0.031 | -0.061 | 0.002 | -0.263 | 0.132 | 1.557 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.038 | -0.047 | -0.018 |
| D06-S01 | D06-S01/20 | Y250 | 895 | -0.350 | 55079 | -0.026 | -0.081 | 0.021 | -0.357 | 0.075 | 1.062 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.039 | -0.055 | -0.011 |
| D06-S01 | D06-S01/20 | Y60 | 4292 | -0.270 | 88842 | -0.052 | -0.089 | -0.015 | -0.288 | 0.192 | 1.200 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.065 | -0.096 | -0.013 |
| D06-S01 | D06-S01/5 | Y120 | 2062 | -0.394 | 77125 | -0.025 | -0.051 | 0.005 | -0.327 | 0.064 | 1.275 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.034 | -0.018 | -0.030 |
| D06-S01 | D06-S01/5 | Y250 | 895 | -0.527 | 55079 | -0.018 | -0.044 | 0.009 | -0.340 | 0.034 | 1.013 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.028 | -0.014 | -0.019 |
| D06-S01 | D06-S01/5 | Y60 | 4292 | -0.433 | 88842 | -0.049 | -0.071 | -0.025 | -0.363 | 0.114 | 1.110 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.061 | -0.046 | -0.050 |
| D06-S03 | D06-S03/10 | Y120 | 2062 | -0.335 | 77125 | -0.010 | -0.036 | 0.020 | -0.354 | 0.030 | 1.492 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.013 | 0.004 | -0.020 |
| D06-S03 | D06-S03/10 | Y250 | 895 | -0.432 | 55079 | -0.022 | -0.058 | 0.024 | -0.390 | 0.050 | 1.363 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.029 | -0.005 | -0.030 |
| D06-S03 | D06-S03/10 | Y60 | 4292 | -0.339 | 88842 | -0.029 | -0.057 | -0.000 | -0.315 | 0.087 | 1.193 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.040 | -0.025 | -0.032 |
| D06-S03 | D06-S03/20 | Y120 | 2062 | -0.235 | 77125 | 0.000 | -0.028 | 0.035 | -0.284 | -0.002 | 1.876 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.004 | 0.028 | -0.019 |
| D06-S03 | D06-S03/20 | Y250 | 895 | -0.372 | 55079 | -0.028 | -0.082 | 0.036 | -0.373 | 0.074 | 1.494 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.027 | -0.011 | -0.036 |
| D06-S03 | D06-S03/20 | Y60 | 4292 | -0.248 | 88842 | -0.014 | -0.047 | 0.027 | -0.262 | 0.055 | 1.263 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.022 | -0.027 | -0.002 |
| D06-S03 | D06-S03/40 | Y120 | 2062 | -0.220 | 77125 | 0.017 | -0.015 | 0.061 | -0.246 | -0.079 | 1.552 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.041 | 0.042 | -0.000 |
| D06-S03 | D06-S03/40 | Y250 | 895 | -0.334 | 55079 | -0.033 | -0.095 | 0.059 | -0.344 | 0.097 | 1.546 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.012 | -0.006 | -0.046 |
| D06-S03 | D06-S03/5 | Y120 | 2062 | -0.388 | 77125 | -0.012 | -0.036 | 0.013 | -0.301 | 0.032 | 1.387 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.014 | 0.012 | -0.028 |
| D06-S03 | D06-S03/5 | Y250 | 895 | -0.499 | 55079 | -0.018 | -0.046 | 0.018 | -0.380 | 0.035 | 1.257 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.021 | 0.007 | -0.030 |
| D06-S03 | D06-S03/5 | Y60 | 4292 | -0.391 | 88842 | -0.029 | -0.050 | -0.007 | -0.329 | 0.073 | 1.196 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.036 | -0.010 | -0.044 |
| D06-S03 | D06-S03/60 | Y250 | 895 | -0.254 | 55079 | -0.022 | -0.095 | 0.077 | -0.271 | 0.087 | 1.776 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.001 | 0.023 | -0.045 |
| D06-S04 | D06-S04/20 | Y120 | 1711 | -0.265 | 72082 | -0.019 | -0.053 | 0.017 | -0.243 | 0.073 | 1.127 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.015 | -0.031 | -0.011 |
| D06-S04 | D06-S04/20 | Y250 | 722 | -0.305 | 52255 | -0.030 | -0.071 | 0.018 | -0.230 | 0.099 | 1.136 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.024 | -0.051 | -0.019 |
| D06-S04 | D06-S04/40 | Y120 | 1695 | -0.238 | 69668 | -0.005 | -0.043 | 0.037 | -0.241 | 0.020 | 1.182 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.015 | -0.037 | 0.016 |
| D06-S04 | D06-S04/40 | Y250 | 715 | -0.316 | 50785 | -0.045 | -0.098 | 0.019 | -0.268 | 0.144 | 1.069 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.036 | -0.074 | -0.031 |
| D06-S04 | D06-S04/60 | Y120 | 1680 | -0.236 | 67924 | -0.000 | -0.039 | 0.038 | -0.225 | 0.002 | 1.068 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.021 | -0.060 | 0.037 |
| D06-S04 | D06-S04/60 | Y250 | 712 | -0.306 | 49719 | -0.052 | -0.109 | 0.024 | -0.266 | 0.171 | 1.067 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.040 | -0.082 | -0.037 |
| D06-S05 | D06-S05/tek | Y250 | 895 | -0.279 | 55079 | 0.007 | -0.038 | 0.073 | -0.264 | -0.027 | 1.464 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.039 | 0.018 | 0.002 |
| D06-S09 | D06-S09/20 | Y120 | 2062 | -0.281 | 77125 | 0.022 | -0.018 | 0.067 | -0.334 | -0.077 | 1.623 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.033 | 0.029 | 0.016 |
| D06-S09 | D06-S09/20 | Y250 | 895 | -0.435 | 55079 | -0.004 | -0.061 | 0.071 | -0.435 | 0.009 | 1.308 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.008 | -0.004 | -0.004 |
| D06-S09 | D06-S09/20 | Y60 | 4292 | -0.278 | 88842 | -0.014 | -0.054 | 0.029 | -0.295 | 0.051 | 1.182 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.017 | -0.033 | 0.002 |
| D06-S09 | D06-S09/60 | Y120 | 2062 | -0.205 | 77125 | 0.082 | 0.028 | 0.140 | -0.205 | -0.398 | 1.336 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 0.113 | 0.103 | 0.065 |
| D06-S09 | D06-S09/60 | Y250 | 895 | -0.363 | 55079 | 0.025 | -0.052 | 0.143 | -0.339 | -0.068 | 1.278 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.060 | 0.028 | 0.022 |
| D10-S02 | D10-S02/tek | Y250 | 895 | -0.254 | 55079 | 0.075 | 0.041 | 0.110 | -0.235 | -0.296 | 0.672 | TERS KALINTI | GERÇEK ETKİ KALIYOR | 0.070 | 0.026 | 0.099 |
| D10-S09 | D10-S09/tek | Y120 | 2062 | 0.230 | 77125 | -0.014 | -0.055 | 0.020 | 0.273 | -0.063 | 1.930 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.020 | -0.039 | 0.003 |
| D10-S09 | D10-S09/tek | Y250 | 895 | 0.371 | 55079 | 0.011 | -0.057 | 0.060 | 0.372 | 0.029 | 1.606 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.004 | 0.001 | 0.016 |
| D10-S09 | D10-S09/tek | Y60 | 4292 | 0.252 | 88842 | 0.011 | -0.029 | 0.046 | 0.260 | 0.043 | 1.226 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.020 | 0.015 | 0.007 |
| D10-S10 | D10-S10/tek | Y250 | 895 | 0.350 | 55079 | -0.063 | -0.106 | -0.021 | 0.273 | -0.180 | 0.395 | TERS KALINTI | GERÇEK ETKİ KALIYOR | -0.073 | 0.008 | -0.098 |

## A2 kalan etki denetimi (küçülme = 1 − |d_denetim| / |d(ii)|; >= 0,50 açıklar, 0,25-0,50 kısmen, < 0,25 açıklamaz)

| hucre | varyant | ufuk | ii_d | a2_M03a_kuculme | a2_M03b_kuculme | a2_M16a_kuculme | a2_M16b_kuculme | a2_M18_kuculme |
|---|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/20 | Y60 | -0.049 | 0.020 | -0.124 | 0.050 | 0.113 | 0.092 |
| D02-S08 | D02-S08/10 | Y120 | 0.033 | 0.036 | -0.105 | 0.546 | 0.675 | -0.965 |
| D02-S08 | D02-S08/20 | Y120 | 0.047 | -0.024 | -0.074 | 0.374 | 0.579 | -0.654 |
| D02-S08 | D02-S08/40 | Y120 | 0.081 | -0.025 | 0.038 | 0.293 | 0.369 | -0.076 |
| D04-S04 | D04-S04/tek | Y250 | -0.076 | -0.094 | 0.315 | 0.181 | -0.216 | 0.025 |
| D05-S03 | D05-S03/20 | Y250 | -0.069 | -0.031 | -0.488 | 0.191 | 0.345 | -0.081 |
| D06-S09 | D06-S09/60 | Y120 | 0.082 | -0.024 | 0.007 | 0.245 | 0.043 | 0.143 |
| D10-S02 | D10-S02/tek | Y250 | 0.075 | -0.009 | -0.740 | -0.111 | 0.266 | -0.668 |
| D10-S10 | D10-S10/tek | Y250 | -0.063 | -0.046 | 0.176 | 0.323 | 0.313 | 0.227 |

## A3 haber ve birleşme bileşimi (G1 olay − G7 eş; ÖNCESİ sızıntısız, SONRASI açıklayıcı)

| ufuk | olcu | tur | n_olay | pay_g1 | pay_g7 | fark | fark_alt | fark_ust | karar |
|---|---|---|---|---|---|---|---|---|---|
| Y60 | once_8k | ÖNCESİ (sızıntısız) | 3349 | 0.603 | 0.587 | 0.016 | -0.005 | 0.040 | fark yok |
| Y60 | once_8k_202 | ÖNCESİ (sızıntısız) | 3349 | 0.324 | 0.308 | 0.015 | 0.001 | 0.031 | G1 > G7 |
| Y60 | once_ihrac | ÖNCESİ (sızıntısız) | 3349 | 0.074 | 0.067 | 0.007 | -0.004 | 0.017 | fark yok |
| Y60 | once_13dg | ÖNCESİ (sızıntısız) | 3349 | 0.212 | 0.216 | -0.004 | -0.017 | 0.009 | fark yok |
| Y60 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 3349 | 0.121 | 0.113 | 0.008 | -0.013 | 0.032 | fark yok |
| Y60 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 3349 | 0.200 | 0.196 | 0.003 | -0.015 | 0.020 | fark yok |
| Y60 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 3349 | 0.067 | 0.088 | -0.021 | -0.033 | -0.010 | G1 < G7 |
| Y60 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 3349 | 0.171 | 0.156 | 0.015 | -0.006 | 0.033 | fark yok |
| Y120 | once_8k | ÖNCESİ (sızıntısız) | 1639 | 0.595 | 0.590 | 0.005 | -0.021 | 0.035 | fark yok |
| Y120 | once_8k_202 | ÖNCESİ (sızıntısız) | 1639 | 0.314 | 0.311 | 0.003 | -0.027 | 0.041 | fark yok |
| Y120 | once_ihrac | ÖNCESİ (sızıntısız) | 1639 | 0.076 | 0.070 | 0.006 | -0.008 | 0.024 | fark yok |
| Y120 | once_13dg | ÖNCESİ (sızıntısız) | 1639 | 0.245 | 0.241 | 0.004 | -0.018 | 0.024 | fark yok |
| Y120 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 1639 | 0.127 | 0.121 | 0.006 | -0.014 | 0.028 | fark yok |
| Y120 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 1639 | 0.220 | 0.229 | -0.009 | -0.032 | 0.016 | fark yok |
| Y120 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 1639 | 0.109 | 0.115 | -0.005 | -0.030 | 0.014 | fark yok |
| Y120 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 1639 | 0.314 | 0.248 | 0.066 | 0.041 | 0.090 | G1 > G7 |
| Y250 | once_8k | ÖNCESİ (sızıntısız) | 727 | 0.673 | 0.621 | 0.051 | 0.003 | 0.088 | G1 > G7 |
| Y250 | once_8k_202 | ÖNCESİ (sızıntısız) | 727 | 0.352 | 0.363 | -0.011 | -0.037 | 0.033 | fark yok |
| Y250 | once_ihrac | ÖNCESİ (sızıntısız) | 727 | 0.089 | 0.080 | 0.009 | -0.015 | 0.059 | fark yok |
| Y250 | once_13dg | ÖNCESİ (sızıntısız) | 727 | 0.367 | 0.354 | 0.013 | -0.012 | 0.059 | fark yok |
| Y250 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 727 | 0.100 | 0.098 | 0.002 | -0.035 | 0.024 | fark yok |
| Y250 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 727 | 0.281 | 0.254 | 0.027 | -0.005 | 0.046 | fark yok |
| Y250 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 727 | 0.179 | 0.191 | -0.012 | -0.048 | 0.028 | fark yok |
| Y250 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 727 | 0.527 | 0.427 | 0.100 | 0.055 | 0.173 | G1 > G7 |
