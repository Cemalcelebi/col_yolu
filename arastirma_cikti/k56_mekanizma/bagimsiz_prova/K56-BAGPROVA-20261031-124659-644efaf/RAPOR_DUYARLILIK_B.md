# PROVA ikinci koşu (K56-BAGPROVA-20261031-124659-644efaf)

- commit 644efaf; kilit sha 24460794f9a6; evren sürümü 0d00d2c97608; süre 1.6 dk.
- Olay oranı (olay / likit satır): {"Y60": 0.00427, "Y120": 0.00163, "Y250": 0.00067}.

## Özet (sayılardan)

- A1 / B2 seçimsiz kontrol, satır: {'MEKANİK (gerçek + sentetik)': 6}; hücre: {'MEKANİK': 1}.
- GERÇEK ETKİ KALIYOR satırı: 0 / 6. d(ii) / d(i) medyanı 0.039 (d(i) medyanı -0.327, d(ii) medyanı -0.011).
- (iii) duyarlılık (olay dizisinden rastgele gün): {'GERÇEK ETKİ KALIYOR': 6}; (ii) ile sınıfı farklı satır 6. UYARI (v1.3-D): (iii) seçimsiz bir kontrol DEĞİLDİR; sıfır etkili yapay veride d(iii) ≈ d(i). '(iii) GERÇEK ETKİ KALIYOR' etiketi gerçek etki kanıtı sayılmaz.
- A3 bileşim, aralığı 0'ı dışlayan: Y250 once_13dg G1 > G7 (+0.060).
- B1 (K55 A, ilk geçiş) DUYARLILIK-B döneminde geçen satır 6 / 6; hücre {'DOĞRULAMA BEKLİYOR (A, ilk geçiş)': 1}. B1 geçişi seçim etkisi tekrarlandığında da olur; gerçek etki için belirleyici B2'dir (ön kayıt v1.2-B).
- B3 (K55 B, eşleşmiş ileri getiri) DUYARLILIK-B: {'TUTMAZ': 2}.

## A1 seçimsiz kontrol: satır sınıfları

| sinif_a1 | n |
|---|---|
| MEKANİK (gerçek + sentetik) | 6 |

Ufuk × sınıf:

| ufuk | MEKANİK (gerçek + sentetik) |
|---|---|
| Y120 | 2 |
| Y250 | 2 |
| Y60 | 2 |

## Hücre sınıfları (KEŞİF satırlarının çoğunluğu)

| hucre | satir | a1 | a1_iii | iii_farkli | b1_gecen | b1_durum |
|---|---|---|---|---|---|---|
| D01-S02 | 6 | MEKANİK | GERÇEK ETKİ KALIYOR | 6 | 6 | DOĞRULAMA BEKLİYOR (A, ilk geçiş) |

## Satırlar (d: (i) ilk geçiş, (ii) bütün nitelikli günler, (iii) rastgele gün)

| hucre | varyant | ufuk | i_n_olay | i_d | ii_n_olay | ii_d | ii_d_alt | ii_d_ust | iii_d | r_ii | sent_oran_faz0 | sinif_a1 | sinif_iii | ayr_d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/10 | Y120 | 946 | -0.356 | 28075 | -0.020 | -0.054 | 0.012 | -0.307 | 0.056 | 0.994 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.011 |
| D01-S02 | D01-S02/10 | Y250 | 243 | -0.457 | 10196 | 0.003 | -0.033 | 0.029 | -0.278 | -0.006 | 0.770 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.018 |
| D01-S02 | D01-S02/10 | Y60 | 2916 | -0.306 | 50040 | -0.013 | -0.036 | 0.006 | -0.256 | 0.043 | 0.943 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.003 |
| D01-S02 | D01-S02/20 | Y120 | 946 | -0.249 | 28075 | -0.008 | -0.044 | 0.031 | -0.227 | 0.034 | 1.352 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.001 |
| D01-S02 | D01-S02/20 | Y250 | 243 | -0.349 | 10196 | -0.006 | -0.061 | 0.050 | -0.343 | 0.017 | 0.905 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | 0.003 |
| D01-S02 | D01-S02/20 | Y60 | 2916 | -0.285 | 50040 | -0.046 | -0.081 | -0.004 | -0.289 | 0.162 | 1.079 | MEKANİK (gerçek + sentetik) | GERÇEK ETKİ KALIYOR | -0.045 |

## A3 haber ve birleşme bileşimi (G1 olay − G7 eş; ÖNCESİ sızıntısız, SONRASI açıklayıcı)

| ufuk | olcu | tur | n_olay | pay_g1 | pay_g7 | fark | fark_alt | fark_ust | karar |
|---|---|---|---|---|---|---|---|---|---|
| Y60 | once_8k | ÖNCESİ (sızıntısız) | 2731 | 0.585 | 0.586 | -0.001 | -0.021 | 0.020 | fark yok |
| Y60 | once_8k_202 | ÖNCESİ (sızıntısız) | 2731 | 0.329 | 0.320 | 0.009 | -0.013 | 0.031 | fark yok |
| Y60 | once_ihrac | ÖNCESİ (sızıntısız) | 2731 | 0.058 | 0.066 | -0.008 | -0.021 | 0.006 | fark yok |
| Y60 | once_13dg | ÖNCESİ (sızıntısız) | 2731 | 0.185 | 0.192 | -0.006 | -0.022 | 0.009 | fark yok |
| Y60 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 2731 | 0.153 | 0.153 | 0.000 | -0.021 | 0.019 | fark yok |
| Y60 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 2731 | 0.203 | 0.183 | 0.020 | -0.002 | 0.043 | fark yok |
| Y60 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 2731 | 0.047 | 0.051 | -0.004 | -0.013 | 0.007 | fark yok |
| Y60 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 2731 | 0.140 | 0.139 | 0.000 | -0.020 | 0.020 | fark yok |
| Y120 | once_8k | ÖNCESİ (sızıntısız) | 910 | 0.624 | 0.609 | 0.015 | -0.011 | 0.043 | fark yok |
| Y120 | once_8k_202 | ÖNCESİ (sızıntısız) | 910 | 0.332 | 0.310 | 0.022 | -0.001 | 0.050 | fark yok |
| Y120 | once_ihrac | ÖNCESİ (sızıntısız) | 910 | 0.062 | 0.072 | -0.011 | -0.026 | 0.006 | fark yok |
| Y120 | once_13dg | ÖNCESİ (sızıntısız) | 910 | 0.234 | 0.234 | 0.000 | -0.024 | 0.023 | fark yok |
| Y120 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 910 | 0.115 | 0.142 | -0.027 | -0.058 | 0.003 | fark yok |
| Y120 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 910 | 0.174 | 0.174 | -0.001 | -0.027 | 0.028 | fark yok |
| Y120 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 910 | 0.081 | 0.079 | 0.002 | -0.013 | 0.017 | fark yok |
| Y120 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 910 | 0.269 | 0.233 | 0.036 | -0.004 | 0.079 | fark yok |
| Y250 | once_8k | ÖNCESİ (sızıntısız) | 238 | 0.605 | 0.580 | 0.025 | -0.023 | 0.078 | fark yok |
| Y250 | once_8k_202 | ÖNCESİ (sızıntısız) | 238 | 0.315 | 0.281 | 0.034 | -0.021 | 0.090 | fark yok |
| Y250 | once_ihrac | ÖNCESİ (sızıntısız) | 238 | 0.055 | 0.077 | -0.022 | -0.045 | 0.011 | fark yok |
| Y250 | once_13dg | ÖNCESİ (sızıntısız) | 238 | 0.206 | 0.146 | 0.060 | 0.016 | 0.107 | G1 > G7 |
| Y250 | sonra_202 | SONRASI (açıklayıcı, öngörü değil) | 238 | 0.118 | 0.133 | -0.015 | -0.060 | 0.027 | fark yok |
| Y250 | sonra_haber | SONRASI (açıklayıcı, öngörü değil) | 238 | 0.147 | 0.153 | -0.006 | -0.070 | 0.048 | fark yok |
| Y250 | sonra_birlesme | SONRASI (açıklayıcı, öngörü değil) | 238 | 0.130 | 0.124 | 0.007 | -0.026 | 0.060 | fark yok |
| Y250 | sonra_ihrac | SONRASI (açıklayıcı, öngörü değil) | 238 | 0.374 | 0.374 | -0.000 | -0.070 | 0.081 | fark yok |

## B1 DUYARLILIK-B (A, ilk geçiş; KEŞİF satırlarıyla)

- geçen satır 6 / 6

| hucre | varyant | ufuk | kesif_d | i_d | i_d_alt | i_d_ust | i_auc | q_bh |
|---|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/10 | Y120 | -0.281 | -0.356 | -0.437 | -0.280 | 0.397 | 0.001 |
| D01-S02 | D01-S02/10 | Y250 | -0.378 | -0.457 | -0.604 | -0.359 | 0.381 | 0.001 |
| D01-S02 | D01-S02/10 | Y60 | -0.289 | -0.306 | -0.356 | -0.252 | 0.415 | 0.001 |
| D01-S02 | D01-S02/20 | Y120 | -0.211 | -0.249 | -0.320 | -0.173 | 0.428 | 0.001 |
| D01-S02 | D01-S02/20 | Y250 | -0.306 | -0.349 | -0.532 | -0.128 | 0.400 | 0.001 |
| D01-S02 | D01-S02/20 | Y60 | -0.235 | -0.285 | -0.369 | -0.208 | 0.420 | 0.001 |

## B3 DUYARLILIK-B (K55 B, eşleşmiş ileri)

| hucre | varyant | n | fark | fark_alt | net_fark | slot_rastgele_yuzdelik | karar |
|---|---|---|---|---|---|---|---|
| D01-S02 | D01-S02/10 | 9144 | -0.004 | -0.010 | -0.004 | 0.730 | TUTMAZ |
| D01-S02 | D01-S02/20 | 8105 | -0.003 | -0.011 | -0.003 | 0.280 | TUTMAZ |
