# KART TURU 1 — sonuç (açık kesik 2023-12-31, açılmış blok 4: 2023Q1, 2023Q2, 2023Q3, 2023Q4)

KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test

Bakış: BAKIŞ 1: 2023Q1-2023Q4 birikimli. KASA kapısı: kesik 2023-12-31, dosyalar en geç {'/tmp/kasa/acik/V_ABD.pkl': '2023-12-29', '/tmp/kasa/acik/V_AVR.pkl': '2023-12-29', '/tmp/kasa/acik/V_BIST.pkl': '2023-12-29', '/tmp/kasa/acik/k34_yahoo.pkl': '2023-12-29'}. Çıktı en geç tarih: {'kt_satir.csv.gz': '2023-12-29', 'olculen_son_giris': {'15': '2023-12-11', '30': '2023-11-20', '45': '2023-10-27'}}.
Ön kayıt kapısı: {'onkayit': 'arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md', 'commit': 'e0976cbd77685d0bafc6f8d31af2bb7b45739adf', 'commit_utc': '2026-11-21T12:50:23Z', 'kod': [{'yol': 'KART_TUR1.py', 'sha256': '334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b'}, {'yol': 'CETVEL2.py', 'sha256': '2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6'}], 'kontrol': True, 'bagimli': 16}.
Yeniden üretim (K11): TUTTU [{'hucre': 'KT01 ABD R15 acik', 'n': 8568, 'fark': -0.0018016196057328976, 'sira': 0.49553144909154473, 'esit': True}, {'hucre': 'KT08 AVR R30 acik', 'n': 1366, 'fark': 0.004191942747841824, 'sira': 0.5129707104271153, 'esit': True}].
Prefix (K2): Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

## Kart etiketleri

| Kart | Etiket | Neden | BH p |
|---|---|---|---|
| KT00 | KONTROL GÖRMEDİ | R15: ABD FARK +0.70 boot [-1.19; +2.65] n 1269 T+ False, AVR FARK -0.46 boot [-1.79; +0.68] n 474 T+ False; R30: ABD FARK +0.07 boot [-1.82; +2.02] n 687 T+ False, AVR FARK -0.84 boot [-2.52; +0.91] n 277 T+ False | - |
| KT01 | ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz) | ABD R15 FARK -0.02 [-0.41; +0.29]; AVR R15 FARK -0.17 [-0.81; +0.49]; ABD R30 FARK +0.30 [-0.27; +1.05]; AVR R30 FARK +0.34 [-0.43; +0.92] | - |
| KT02 | ÖLÇÜLEMEDİ | ABD R15 n 138 güç 0.43; AVR R15 n 19 güç 0.11; ABD R30 n 131 güç 0.15; AVR R30 n 16 güç 0.08 | - |
| KT03 | ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz) | ABD R15 FARK -0.02 [-0.43; +0.28]; AVR R15 FARK -0.05 [-0.83; +0.64]; ABD R30 FARK +0.20 [-0.34; +0.93]; AVR R30 FARK +0.56 [+0.01; +1.27] | - |
| KT04 | ÖLÇÜLEMEDİ | ABD R30 n 875 güç 0.77 | - |
| KT05 | ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz) | ABD R15 FARK -0.07 [-0.50; +0.24]; AVR R15 FARK -0.21 [-0.82; +0.43]; ABD R30 FARK +0.23 [-0.33; +0.88]; AVR R30 FARK +0.31 [-0.53; +0.97] | - |
| KT06 | ÖLÇÜLEMEDİ | ABD R30 n 925 güç 0.80 | - |
| KT07 | ÖLÇÜLEMEDİ | ABD R15 n 52 güç 0.19; AVR R15 n 12 güç 0.08; ABD R30 n 50 güç 0.08; AVR R30 n 9 güç 0.06 | - |
| KT08 | ÖLÇÜLEMEDİ | AVR R15 n 181 güç 0.74; ABD R30 n 512 güç 0.51; AVR R30 n 127 güç 0.38 | - |
| KT09 | ÖLÇÜLEMEDİ | ABD R15 n 22 güç 0.10; AVR R15 n 3 güç 0.05; ABD R30 n 20 güç 0.05; AVR R30 n 3 güç 0.04 | - |
| KT10 | ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz) | ABD R15 FARK -0.10 [-0.50; +0.37]; ABD R30 FARK -0.25 [-1.31; +0.47] | - |

## Huni (olay sayıları; getirisiz)

```
{
 "ABD": {
  "Y1": {
   "sinyal": 28051,
   "girdi": 28051,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 5,
   "giris_gec": 0,
   "likidite_alt20": 3591,
   "bolunme_gecmis": 41,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 3634,
   "tekil": 13684,
   "y1_olay": 10728,
   "F_KT02": 492,
   "F_KT03": 9406,
   "F_KT04": 4846,
   "F_KT05": 10251,
   "F_KT06": 6092,
   "F_KT07": 204,
   "sure_sn": 101.1
  },
  "D9": {
   "durum": 649919,
   "c": 282319,
   "sure_sn": 38.6
  },
  "MOM": {
   "sinyal": 99683,
   "ana": 15936,
   "U": 8008,
   "A": 7928,
   "son_tarih": "2023-11-30",
   "pk": {
    "girdi": 99683,
    "olay_havuz": 79680,
    "U": 8008,
    "A": 7928,
    "ana": 15936
   }
  },
  "BOFA": {
   "hisse": 1380,
   "kurulum": 589,
   "son": "2023-12-29"
  },
  "DS": {
   "girdi": 233079,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 50,
   "giris_gec": 0,
   "likidite_alt20": 53532,
   "bolunme_gecmis": 4375,
   "evren_once": 0,
   "gecmis_eksik": 6,
   "havuz_az": 0,
   "havuz_disi": 57913,
   "tekil": 0,
   "ds_gun": 233079,
   "havuz_gun": 175116,
   "ana": 16812,
   "F_KT08": 5717,
   "sure_sn": 85.0
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 15936,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 15936,
    "kova_yok": 0,
    "donem": {
     "acik": 13367,
     "birikimli": 2569
    }
   },
   "MOM|30": {
    "girdi": 15936,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 6505,
    "olcum_r15": 9304,
    "kova_yok": 0,
    "donem": {
     "acik": 7899,
     "birikimli": 1532
    }
   },
   "MOM|45": {
    "girdi": 15936,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 8783,
    "olcum_r15": 6950,
    "kova_yok": 0,
    "donem": {
     "acik": 5979,
     "birikimli": 1174
    }
   },
   "Y1|15": {
    "girdi": 10728,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 10534,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 2042
    }
   },
   "Y1|30": {
    "girdi": 10728,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 10432,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 2042
    }
   },
   "Y1|45": {
    "girdi": 10728,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 10324,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 2042
    }
   },
   "DS|15": {
    "girdi": 16812,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 16761,
    "kova_yok": 0,
    "donem": {
     "acik": 14061,
     "birikimli": 2510,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 16812,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 6869,
    "olcum_r15": 9841,
    "kova_yok": 0,
    "donem": {
     "acik": 8320,
     "birikimli": 1481,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 16812,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 9164,
    "olcum_r15": 7501,
    "kova_yok": 0,
    "donem": {
     "acik": 6400,
     "birikimli": 1106,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 589,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 363,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 390,
    "tekil": 0,
    "olcum_r15": 189,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 22
    }
   },
   "BOFA|30": {
    "girdi": 589,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 363,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 390,
    "tekil": 0,
    "olcum_r15": 187,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 22
    }
   },
   "BOFA|45": {
    "girdi": 589,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 363,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 390,
    "tekil": 0,
    "olcum_r15": 187,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 22
    }
   },
   "D9|15": {
    "girdi": 282319,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 293,
    "giris_gec": 25,
    "likidite_alt20": 63603,
    "bolunme_gecmis": 2457,
    "evren_once": 0,
    "gecmis_eksik": 750,
    "havuz_az": 0,
    "havuz_disi": 66810,
    "tekil": 193084,
    "olcum_r15": 21841,
    "kova_yok": 563,
    "donem": {
     "acik": 18014,
     "birikimli": 3609,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 282319,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 293,
    "giris_gec": 25,
    "likidite_alt20": 63603,
    "bolunme_gecmis": 2457,
    "evren_once": 0,
    "gecmis_eksik": 750,
    "havuz_az": 0,
    "havuz_disi": 66810,
    "tekil": 201327,
    "olcum_r15": 13555,
    "kova_yok": 378,
    "donem": {
     "acik": 11241,
     "birikimli": 2301,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 282319,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 293,
    "giris_gec": 25,
    "likidite_alt20": 63603,
    "bolunme_gecmis": 2457,
    "evren_once": 0,
    "gecmis_eksik": 750,
    "havuz_az": 0,
    "havuz_disi": 66810,
    "tekil": 204211,
    "olcum_r15": 10655,
    "kova_yok": 350,
    "donem": {
     "acik": 8853,
     "birikimli": 1859,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 14447,
   "girdi": 14447,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 2,
   "giris_gec": 0,
   "likidite_alt20": 2197,
   "bolunme_gecmis": 6,
   "evren_once": 0,
   "gecmis_eksik": 7,
   "havuz_az": 0,
   "havuz_disi": 2210,
   "tekil": 6924,
   "y1_olay": 5311,
   "F_KT02": 109,
   "F_KT03": 4610,
   "F_KT04": 2636,
   "F_KT05": 4949,
   "F_KT06": 3280,
   "F_KT07": 49,
   "sure_sn": 50.5
  },
  "MOM": {
   "sinyal": 50045,
   "ana": 7916,
   "U": 4000,
   "A": 3916,
   "son_tarih": "2023-11-30",
   "pk": {
    "girdi": 50045,
    "olay_havuz": 39602,
    "U": 4000,
    "A": 3916,
    "ana": 7916
   }
  },
  "BOFA": {
   "hisse": 577,
   "kurulum": 35,
   "son": "2023-12-29"
  },
  "DS": {
   "girdi": 56586,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 18,
   "giris_gec": 0,
   "likidite_alt20": 3033,
   "bolunme_gecmis": 924,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3975,
   "tekil": 0,
   "ds_gun": 56586,
   "havuz_gun": 52593,
   "ana": 5267,
   "F_KT08": 2153,
   "sure_sn": 31.9
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 7916,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 7916,
    "kova_yok": 0,
    "donem": {
     "acik": 6832,
     "birikimli": 1084
    }
   },
   "MOM|30": {
    "girdi": 7916,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 3084,
    "olcum_r15": 4770,
    "kova_yok": 0,
    "donem": {
     "acik": 4144,
     "birikimli": 688
    }
   },
   "MOM|45": {
    "girdi": 7916,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 4151,
    "olcum_r15": 3678,
    "kova_yok": 0,
    "donem": {
     "acik": 3230,
     "birikimli": 535
    }
   },
   "Y1|15": {
    "girdi": 5311,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 5234,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 815
    }
   },
   "Y1|30": {
    "girdi": 5311,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 5194,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 815
    }
   },
   "Y1|45": {
    "girdi": 5311,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 5164,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 815
    }
   },
   "DS|15": {
    "girdi": 5267,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 0,
    "olcum_r15": 5246,
    "kova_yok": 0,
    "donem": {
     "acik": 4562,
     "birikimli": 446,
     "dis": 259
    }
   },
   "DS|30": {
    "girdi": 5267,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 2094,
    "olcum_r15": 3148,
    "kova_yok": 0,
    "donem": {
     "acik": 2741,
     "birikimli": 269,
     "dis": 163
    }
   },
   "DS|45": {
    "girdi": 5267,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 0,
    "bolunme_gecmis": 0,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 0,
    "tekil": 2782,
    "olcum_r15": 2441,
    "kova_yok": 0,
    "donem": {
     "acik": 2148,
     "birikimli": 208,
     "dis": 129
    }
   },
   "BOFA|15": {
    "girdi": 35,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
 
```

## Hücre: acik

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 6718 | 6024 | 694 | 0 | +0.40 [-0.46; +1.23] | -0.13 | 0.502 | +0.04 | 0.1604 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT00 | + | ABD | 30 | 3948 | 3699 | 249 | 0 | +0.72 [-0.31; +1.76] | -0.68 | 0.501 | +0.30 | 0.0710 | 1.00 | -0.00 / 0.01 / True | False / False |
| KT00 | + | ABD | 45 | 2974 | 2799 | 175 | 0 | +0.95 [-0.26; +2.21] | -1.03 | 0.504 | +0.52 | 0.0554 | 0.99 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 3452 | 2788 | 664 | 0 | +0.07 [-0.53; +0.62] | -0.12 | 0.499 | -0.11 | 0.3821 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT00 | + | AVR | 30 | 2104 | 1763 | 341 | 0 | -0.32 [-1.25; +0.62] | -0.63 | 0.486 | -0.68 | 0.7649 | 1.00 | -0.02 / 0.03 / True | False / False |
| KT00 | + | AVR | 45 | 1640 | 1375 | 265 | 0 | +0.40 [-0.75; +1.51] | +0.09 | 0.506 | -0.02 | 0.2191 | 1.00 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 8686 | 8568 | 118 | 0 | -0.18 [-0.46; +0.10] | -0.18 | 0.496 | -0.28 | 0.9264 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 30 | 8686 | 8568 | 118 | 0 | -0.30 [-0.71; +0.07] | -0.31 | 0.493 | -0.43 | 0.9505 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 45 | 8686 | 8568 | 118 | 0 | -0.24 [-0.73; +0.19] | -0.40 | 0.497 | -0.38 | 0.8731 | 1.00 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 4496 | 4217 | 279 | 0 | -0.03 [-0.26; +0.23] | -0.16 | 0.495 | -0.15 | 0.6160 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 4496 | 4217 | 279 | 0 | -0.15 [-0.51; +0.25] | -0.18 | 0.495 | -0.32 | 0.7917 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | AVR | 45 | 4496 | 4217 | 279 | 0 | -0.14 [-0.59; +0.31] | -0.36 | 0.494 | -0.33 | 0.7569 | 1.00 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 2588 | 2188 | 400 | 0 | -0.80 [-1.40; -0.19] | -2.81 | 0.451 | -1.07 | 0.9975 | 1.00 | -0.01 / 0.02 / True | False / True |
| KT01 | + | BIST | 30 | 2588 | 2188 | 400 | 0 | -0.76 [-1.82; +0.42] | -3.42 | 0.475 | -1.23 | 0.9194 | 1.00 | -0.01 / 0.02 / True | False / False |
| KT01 | + | BIST | 45 | 2588 | 2188 | 400 | 0 | -0.72 [-2.22; +0.74] | -4.30 | 0.475 | -1.27 | 0.8585 | 0.93 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 346 | 338 | 8 | 0 | -0.15 [-1.73; +1.51] | +0.13 | 0.505 | -0.67 | 0.5776 | 0.82 | -0.04 / 0.04 / True | False / False |
| KT02 | + | ABD | 30 | 346 | 338 | 8 | 0 | -1.41 [-7.75; +1.89] | +0.30 | 0.514 | -3.14 | 0.6881 | 0.35 | +0.07 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 346 | 338 | 8 | 0 | -2.41 [-9.79; +1.74] | -0.26 | 0.499 | -4.25 | 0.8065 | 0.24 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 89 | 78 | 11 | 0 | +0.49 [-1.88; +2.92] | +1.56 | 0.537 | -0.62 | 0.3265 | 0.37 | -0.04 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 89 | 78 | 11 | 0 | +0.66 [-1.88; +3.45] | +1.05 | 0.517 | -0.73 | 0.2936 | 0.24 | -0.05 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 89 | 78 | 11 | 0 | -0.34 [-4.38; +3.71] | -0.07 | 0.510 | -2.44 | 0.5774 | 0.20 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 238 | 205 | 33 | 0 | -0.23 [-1.87; +1.91] | -2.69 | 0.445 | -1.16 | 0.5962 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 238 | 205 | 33 | 0 | +0.02 [-2.33; +3.27] | -2.14 | 0.489 | -1.41 | 0.4923 | 0.28 | -0.04 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 238 | 205 | 33 | 0 | +1.02 [-2.23; +4.52] | -2.80 | 0.500 | -0.70 | 0.2563 | 0.16 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 7614 | 7512 | 102 | 0 | -0.21 [-0.47; +0.05] | -0.21 | 0.495 | -0.29 | 0.9531 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 30 | 7614 | 7512 | 102 | 0 | -0.29 [-0.71; +0.11] | -0.35 | 0.493 | -0.43 | 0.9403 | 1.00 | -0.14 / 0.02 / True | False / False |
| KT03 | + | ABD | 45 | 7614 | 7512 | 102 | 0 | -0.25 [-0.76; +0.21] | -0.48 | 0.496 | -0.38 | 0.8543 | 1.00 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 3910 | 3661 | 249 | 0 | +0.01 [-0.23; +0.29] | -0.15 | 0.496 | -0.10 | 0.4511 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT03 | + | AVR | 30 | 3910 | 3661 | 249 | 0 | -0.11 [-0.48; +0.30] | -0.21 | 0.495 | -0.31 | 0.7244 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT03 | + | AVR | 45 | 3910 | 3661 | 249 | 0 | -0.11 [-0.58; +0.38] | -0.44 | 0.494 | -0.31 | 0.7051 | 1.00 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 2379 | 2013 | 366 | 0 | -0.64 [-1.22; -0.00] | -2.83 | 0.452 | -0.93 | 0.9816 | 1.00 | +0.02 / 0.02 / True | False / True |
| KT03 | + | BIST | 30 | 2379 | 2013 | 366 | 0 | -0.72 [-1.89; +0.49] | -3.48 | 0.475 | -1.23 | 0.8973 | 0.99 | +0.02 / 0.03 / True | False / False |
| KT03 | + | BIST | 45 | 2379 | 2013 | 366 | 0 | -0.52 [-2.01; +1.00] | -4.16 | 0.477 | -1.04 | 0.7668 | 0.91 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 3823 | 3773 | 50 | 0 | -0.21 [-0.55; +0.19] | -0.10 | 0.497 | -0.37 | 0.8897 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT04 | + | ABD | 30 | 3823 | 3773 | 50 | 0 | -0.50 [-1.04; +0.06] | -0.32 | 0.492 | -0.66 | 0.9706 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT04 | + | ABD | 45 | 3823 | 3773 | 50 | 0 | -0.64 [-1.33; -0.01] | -0.45 | 0.493 | -0.84 | 0.9849 | 1.00 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 2208 | 2080 | 128 | 0 | -0.05 [-0.42; +0.38] | -0.19 | 0.490 | -0.22 | 0.6109 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT04 | + | AVR | 30 | 2208 | 2080 | 128 | 0 | -0.04 [-0.55; +0.57] | -0.21 | 0.495 | -0.28 | 0.5545 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT04 | + | AVR | 45 | 2208 | 2080 | 128 | 0 | -0.06 [-0.67; +0.55] | -0.29 | 0.496 | -0.30 | 0.5884 | 1.00 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 1572 | 1348 | 224 | 0 | -0.85 [-1.61; -0.07] | -2.93 | 0.450 | -1.18 | 0.9890 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT04 | + | BIST | 30 | 1572 | 1348 | 224 | 0 | -0.68 [-1.89; +0.71] | -3.58 | 0.476 | -1.31 | 0.8719 | 0.96 | +0.01 / 0.03 / True | False / False |
| KT04 | + | BIST | 45 | 1572 | 1348 | 224 | 0 | -0.70 [-2.35; +1.11] | -4.30 | 0.471 | -1.30 | 0.8162 | 0.76 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 8245 | 8139 | 106 | 0 | -0.20 [-0.47; +0.08] | -0.19 | 0.495 | -0.30 | 0.9312 | 1.00 | -0.01 / 0.05 / True | False / False |
| KT05 | + | ABD | 30 | 8245 | 8139 | 106 | 0 | -0.36 [-0.76; +0.04] | -0.35 | 0.492 | -0.50 | 0.9733 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT05 | + | ABD | 45 | 8245 | 8139 | 106 | 0 | -0.33 [-0.85; +0.11] | -0.51 | 0.495 | -0.47 | 0.9340 | 1.00 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 4160 | 3909 | 251 | 0 | -0.01 [-0.25; +0.27] | -0.13 | 0.497 | -0.13 | 0.5263 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 30 | 4160 | 3909 | 251 | 0 | -0.13 [-0.52; +0.34] | -0.18 | 0.496 | -0.32 | 0.7555 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 45 | 4160 | 3909 | 251 | 0 | -0.11 [-0.59; +0.37] | -0.34 | 0.496 | -0.32 | 0.6829 | 1.00 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 2535 | 2141 | 394 | 0 | -0.82 [-1.37; -0.16] | -2.77 | 0.451 | -1.08 | 0.9983 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT05 | + | BIST | 30 | 2535 | 2141 | 394 | 0 | -0.76 [-1.98; +0.49] | -3.48 | 0.475 | -1.24 | 0.9206 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT05 | + | BIST | 45 | 2535 | 2141 | 394 | 0 | -0.74 [-2.19; +0.80] | -4.30 | 0.475 | -1.31 | 0.8611 | 0.93 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 4953 | 4885 | 68 | 0 | -0.02 [-0.29; +0.31] | -0.09 | 0.499 | -0.14 | 0.5541 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 4953 | 4885 | 68 | 0 | -0.10 [-0.51; +0.31] | -0.24 | 0.494 | -0.26 | 0.7018 | 1.00 | -0.04 / 0.03 / True | False / False |
| KT06 | + | ABD | 45 | 4953 | 4885 | 68 | 0 | -0.05 [-0.55; +0.46] | -0.29 | 0.498 | -0.23 | 0.5758 | 1.00 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 2801 | 2629 | 172 | 0 | -0.03 [-0.32; +0.26] | -0.14 | 0.496 | -0.15 | 0.5993 | 1.00 | -0.01 / 0.03 / True | False / False |
| KT06 | + | AVR | 30 | 2801 | 2629 | 172 | 0 | -0.18 [-0.64; +0.31] | -0.24 | 0.494 | -0.39 | 0.7925 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 2801 | 2629 | 172 | 0 | -0.10 [-0.66; +0.45] | -0.31 | 0.496 | -0.32 | 0.6670 | 1.00 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 1626 | 1381 | 245 | 0 | -1.04 [-1.78; -0.25] | -2.86 | 0.443 | -1.36 | 0.9983 | 1.00 | +0.05 / 0.02 / True | False / True |
| KT06 | + | BIST | 30 | 1626 | 1381 | 245 | 0 | -1.38 [-2.58; +0.15] | -3.68 | 0.470 | -2.03 | 0.9851 | 0.96 | +0.05 / 0.03 / True | False / False |
| KT06 | + | BIST | 45 | 1626 | 1381 | 245 | 0 | -1.51 [-3.15; +0.13] | -4.13 | 0.467 | -2.14 | 0.9801 | 0.77 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 151 | 146 | 5 | 0 | -0.45 [-2.54; +1.64] | -0.57 | 0.486 | -1.32 | 0.6823 | 0.45 | -0.06 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 151 | 146 | 5 | 0 | -3.53 [-16.75; +2.46] | +0.32 | 0.510 | -6.01 | 0.6932 | 0.16 | -0.34 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 151 | 146 | 5 | 0 | -6.14 [-21.99; +1.28] | -0.40 | 0.486 | -9.67 | 0.9059 | 0.12 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 36 | 30 | 6 | 0 | +0.36 [-3.59; +4.60] | +0.86 | 0.518 | -1.53 | 0.4217 | 0.16 | +0.01 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 36 | 30 | 6 | 0 | -0.33 [-4.45; +3.20] | +0.77 | 0.517 | -2.00 | 0.5699 | 0.11 | +0.02 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 36 | 30 | 6 | 0 | +1.24 [-4.81; +6.86] | +1.30 | 0.538 | -2.45 | 0.3352 | 0.09 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 129 | 108 | 21 | 0 | -0.16 [-2.24; +2.79] | -2.69 | 0.454 | -1.56 | 0.5619 | 0.46 | +0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 129 | 108 | 21 | 0 | -0.55 [-3.73; +3.25] | -2.29 | 0.496 | -2.45 | 0.6379 | 0.16 | +0.13 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 129 | 108 | 21 | 0 | +0.54 [-3.52; +5.74] | -3.51 | 0.493 | -2.49 | 0.4119 | 0.10 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 4836 | 4791 | 45 | 0 | +0.05 [-0.48; +0.72] | -0.02 | 0.509 | -0.23 | 0.5693 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT08 | - | ABD | 30 | 3431 | 3395 | 36 | 0 | -0.41 [-1.78; +0.98] | -0.83 | 0.500 | -0.74 | 0.4235 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT08 | - | ABD | 45 | 2947 | 2917 | 30 | 0 | -1.16 [-3.80; +1.49] | -1.81 | 0.496 | -1.67 | 0.4330 | 0.99 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 1838 | 1784 | 54 | 0 | +0.29 [-0.53; +1.21] | +0.35 | 0.515 | +0.05 | 0.7364 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | AVR | 30 | 1406 | 1366 | 40 | 0 | +0.42 [-0.85; +2.01] | +0.32 | 0.513 | +0.06 | 0.6858 | 1.00 | +0.04 / 0.03 / True | False / False |
| KT08 | - | AVR | 45 | 1266 | 1235 | 31 | 0 | +0.32 [-0.92; +2.10] | +0.22 | 0.510 | -0.29 | 0.6629 | 1.00 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 721 | 653 | 68 | 0 | -0.73 [-2.02; +0.64] | -1.50 | 0.480 | -1.40 | 0.1229 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | BIST | 30 | 475 | 436 | 39 | 0 | -2.08 [-6.33; +1.29] | -2.89 | 0.469 | -3.28 | 0.1807 | 0.53 | +0.03 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 400 | 364 | 36 | 0 | -3.83 [-10.74; +0.65] | -3.31 | 0.471 | -5.70 | 0.0979 | 0.26 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 167 | 163 | 4 | 0 | +4.70 [-1.80; +10.74] | +1.44 | 0.540 | +0.06 | 0.0876 | 0.50 | +0.00 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 167 | 163 | 4 | 0 | +7.12 [-2.56; +17.82] | +1.18 | 0.526 | +0.74 | 0.0857 | 0.18 | +0.02 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 167 | 163 | 4 | 0 | +9.62 [-7.48; +35.67] | +0.58 | 0.512 | -4.95 | 0.3318 | 0.13 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 20 | 20 | 0 | 0 | +3.68 [-12.12; +21.09] | -5.40 | 0.447 | -6.03 | 0.3090 | 0.12 | +0.10 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 20 | 20 | 0 | 0 | +5.27 [-7.13; +20.87] | +2.27 | 0.542 | -2.84 | 0.1962 | 0.09 | +0.24 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 20 | 20 | 0 | 0 | +3.67 [-11.69; +20.88] | -2.79 | 0.510 | -5.05 | 0.3000 | 0.07 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 18014 | 17260 | 754 | 0 | -0.02 [-0.26; +0.24] | -0.33 | 0.496 | -0.12 | 0.5743 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT10 | + | ABD | 30 | 11241 | 10773 | 468 | 0 | -0.12 [-0.64; +0.47] | -0.67 | 0.492 | -0.33 | 0.6799 | 1.00 | +0.00 / 0.01 / True | False / False |
| KT10 | + | ABD | 45 | 8853 | 8495 | 358 | 0 | -0.04 [-0.69; +0.67] | -0.70 | 0.500 | -0.30 | 0.5440 | 1.00 | - / - / False | False / False |

## Hücre: birikimli

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 1290 | 1269 | 21 | 0 | +0.70 [-1.19; +2.65] | -0.24 | 0.501 | -0.59 | 0.2234 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT00 | + | ABD | 30 | 756 | 687 | 5 | 64 | +0.07 [-1.82; +2.02] | -1.16 | 0.503 | -1.31 | 0.4571 | 0.65 | -0.00 / 0.00 / True | False / False |
| KT00 | + | ABD | 45 | 580 | 480 | 0 | 100 | -0.90 [-2.71; +0.79] | -2.76 | 0.476 | -2.13 | 0.8365 | 0.34 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 548 | 474 | 74 | 0 | -0.46 [-1.79; +0.68] | -0.19 | 0.480 | -1.19 | 0.7797 | 0.99 | +0.00 / 0.06 / True | False / False |
| KT00 | + | AVR | 30 | 348 | 277 | 38 | 33 | -0.84 [-2.52; +0.91] | -0.02 | 0.488 | -2.04 | 0.8370 | 0.73 | +0.04 / 0.00 / True | False / False |
| KT00 | + | AVR | 45 | 270 | 208 | 20 | 42 | -1.50 [-4.43; +1.34] | -1.15 | 0.457 | -3.09 | 0.8162 | 0.51 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 2042 | 1835 | 13 | 194 | -0.02 [-0.41; +0.29] | -0.27 | 0.501 | -0.23 | 0.5238 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT01 | + | ABD | 30 | 2042 | 1733 | 13 | 296 | +0.30 [-0.27; +1.05] | -0.23 | 0.509 | -0.16 | 0.1558 | 0.98 | +0.00 / 0.04 / True | False / False |
| KT01 | + | ABD | 45 | 2042 | 1625 | 13 | 404 | -0.13 [-0.92; +0.97] | -0.71 | 0.500 | -0.78 | 0.6172 | 0.89 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 815 | 695 | 43 | 77 | -0.17 [-0.81; +0.49] | +0.01 | 0.499 | -0.63 | 0.6912 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 815 | 657 | 41 | 117 | +0.34 [-0.43; +0.92] | +0.28 | 0.515 | -0.04 | 0.1654 | 0.99 | -0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 45 | 815 | 629 | 39 | 147 | +0.10 [-0.48; +0.56] | +0.17 | 0.508 | -0.26 | 0.3476 | 0.96 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 381 | 303 | 69 | 9 | -1.19 [-2.92; -0.10] | -2.26 | 0.474 | -2.15 | 0.9635 | 0.93 | -0.12 / 0.04 / True | False / True |
| KT01 | + | BIST | 30 | 381 | 259 | 60 | 62 | -1.94 [-3.11; -0.28] | -3.97 | 0.475 | -2.82 | 0.9764 | 0.34 | -0.21 / 0.00 / True | False / False |
| KT01 | + | BIST | 45 | 381 | 250 | 55 | 76 | -3.14 [-7.74; +0.73] | -6.18 | 0.467 | -6.28 | 0.9325 | 0.19 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 146 | 138 | 0 | 8 | -0.03 [-2.18; +1.25] | -1.25 | 0.486 | -0.83 | 0.5239 | 0.43 | -0.00 / 0.00 / True | False / False |
| KT02 | + | ABD | 30 | 146 | 131 | 0 | 15 | +1.39 [-1.38; +2.98] | +1.26 | 0.547 | -0.60 | 0.1168 | 0.15 | -0.01 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 146 | 116 | 0 | 30 | -1.00 [-4.80; +0.33] | -0.69 | 0.500 | -2.75 | 0.9037 | 0.10 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 20 | 19 | 0 | 1 | +4.59 [-2.25; +8.67] | +6.45 | 0.682 | -1.16 | 0.0882 | 0.11 | +0.18 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 20 | 16 | 0 | 4 | +7.63 [+1.48; +13.98] | +3.71 | 0.664 | +2.19 | 0.0354 | 0.08 | +0.34 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 20 | 12 | 0 | 8 | +6.41 [-3.28; +19.81] | +4.85 | 0.609 | -2.70 | 0.1227 | 0.06 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 81 | 75 | 6 | 0 | -0.80 [-8.08; +0.24] | -1.62 | 0.491 | -6.18 | 0.8427 | 0.32 | +0.22 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 81 | 75 | 4 | 2 | -1.96 [-7.87; -1.09] | -5.31 | 0.463 | -9.02 | 1.0000 | 0.13 | +0.17 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 81 | 75 | 3 | 3 | -2.21 [-11.88; +3.09] | -5.25 | 0.461 | -5.68 | 0.7439 | 0.08 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 1792 | 1603 | 9 | 180 | -0.02 [-0.43; +0.28] | -0.32 | 0.500 | -0.23 | 0.5289 | 1.00 | -0.03 / 0.01 / True | False / False |
| KT03 | + | ABD | 30 | 1792 | 1510 | 9 | 273 | +0.20 [-0.34; +0.93] | -0.26 | 0.507 | -0.21 | 0.2524 | 0.96 | -0.01 / 0.01 / True | False / False |
| KT03 | + | ABD | 45 | 1792 | 1413 | 9 | 370 | -0.18 [-0.94; +0.94] | -0.75 | 0.497 | -0.86 | 0.6522 | 0.83 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 700 | 594 | 36 | 70 | -0.05 [-0.83; +0.64] | -0.00 | 0.501 | -0.61 | 0.5445 | 1.00 | -0.02 / 0.07 / True | False / False |
| KT03 | + | AVR | 30 | 700 | 558 | 34 | 108 | +0.56 [+0.01; +1.27] | +0.34 | 0.520 | +0.22 | 0.0343 | 0.97 | +0.00 / 0.07 / True | True / False |
| KT03 | + | AVR | 45 | 700 | 535 | 32 | 133 | +0.25 [-0.36; +0.77] | +0.31 | 0.512 | -0.13 | 0.1735 | 0.93 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 342 | 277 | 58 | 7 | -1.00 [-2.83; +0.34] | -2.56 | 0.476 | -1.95 | 0.8807 | 0.90 | -0.02 / 0.07 / True | False / False |
| KT03 | + | BIST | 30 | 342 | 237 | 50 | 55 | -1.54 [-3.11; +0.51] | -3.97 | 0.476 | -2.50 | 0.9394 | 0.32 | +0.02 / 0.00 / True | False / False |
| KT03 | + | BIST | 45 | 342 | 228 | 46 | 68 | -2.70 [-7.01; +1.49] | -5.92 | 0.470 | -5.84 | 0.9185 | 0.18 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 1023 | 917 | 5 | 101 | -0.19 [-0.93; +0.56] | -0.31 | 0.497 | -0.66 | 0.6803 | 1.00 | -0.00 / 0.06 / True | False / False |
| KT04 | + | ABD | 30 | 1023 | 875 | 5 | 143 | +0.06 [-1.01; +1.28] | -0.15 | 0.509 | -0.61 | 0.4594 | 0.77 | -0.01 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 1023 | 797 | 5 | 221 | -0.64 [-2.07; +1.27] | -1.28 | 0.486 | -1.70 | 0.7836 | 0.55 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 428 | 358 | 23 | 47 | -0.10 [-0.99; +0.64] | +0.09 | 0.495 | -0.61 | 0.6081 | 0.97 | -0.01 / 0.06 / True | False / False |
| KT04 | + | AVR | 30 | 428 | 337 | 23 | 68 | +0.23 [-0.27; +0.87] | +0.20 | 0.512 | -0.23 | 0.2307 | 0.82 | -0.04 / 0.01 / True | False / False |
| KT04 | + | AVR | 45 | 428 | 326 | 21 | 81 | -0.19 [-1.31; +1.33] | +0.14 | 0.496 | -1.10 | 0.6484 | 0.73 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 271 | 222 | 46 | 3 | -0.86 [-3.05; +0.72] | -2.19 | 0.479 | -2.34 | 0.8340 | 0.81 | +0.07 / 0.00 / True | False / False |
| KT04 | + | BIST | 30 | 271 | 198 | 40 | 33 | -1.52 [-3.29; +0.63] | -4.05 | 0.473 | -2.57 | 0.9261 | 0.27 | +0.06 / 0.00 / True | False / False |
| KT04 | + | BIST | 45 | 271 | 193 | 38 | 40 | -2.09 [-5.74; +1.25] | -6.14 | 0.471 | -4.81 | 0.9074 | 0.16 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 2006 | 1802 | 13 | 191 | -0.07 [-0.50; +0.24] | -0.31 | 0.500 | -0.29 | 0.5990 | 1.00 | -0.02 / 0.03 / True | False / False |
| KT05 | + | ABD | 30 | 2006 | 1709 | 13 | 284 | +0.23 [-0.33; +0.88] | -0.26 | 0.508 | -0.18 | 0.2026 | 0.98 | -0.03 / 0.06 / True | False / False |
| KT05 | + | ABD | 45 | 2006 | 1610 | 13 | 383 | -0.19 [-0.87; +0.81] | -0.80 | 0.499 | -0.78 | 0.6946 | 0.88 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 789 | 681 | 39 | 69 | -0.21 [-0.82; +0.43] | +0.00 | 0.497 | -0.69 | 0.7366 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT05 | + | AVR | 30 | 789 | 646 | 38 | 105 | +0.31 [-0.53; +0.97] | +0.27 | 0.514 | -0.14 | 0.1989 | 0.98 | +0.02 / 0.04 / True | False / False |
| KT05 | + | AVR | 45 | 789 | 621 | 36 | 132 | +0.10 [-0.53; +0.59] | +0.08 | 0.507 | -0.31 | 0.3635 | 0.96 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 379 | 301 | 69 | 9 | -1.25 [-2.79; -0.12] | -2.56 | 0.472 | -2.15 | 0.9843 | 0.92 | -0.10 / 0.03 / True | False / True |
| KT05 | + | BIST | 30 | 379 | 257 | 60 | 62 | -2.05 [-3.18; -0.19] | -3.97 | 0.472 | -2.98 | 0.9788 | 0.34 | -0.24 / 0.00 / True | False / False |
| KT05 | + | BIST | 45 | 379 | 248 | 55 | 76 | -3.34 [-8.06; +0.76] | -6.37 | 0.465 | -6.66 | 0.9427 | 0.19 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 1139 | 1003 | 3 | 133 | +0.14 [-0.16; +0.49] | -0.08 | 0.508 | -0.02 | 0.1796 | 1.00 | -0.04 / 0.01 / True | False / False |
| KT06 | + | ABD | 30 | 1139 | 925 | 3 | 211 | +0.44 [-0.24; +1.08] | -0.13 | 0.510 | +0.06 | 0.0845 | 0.80 | -0.04 / 0.00 / True | False / False |
| KT06 | + | ABD | 45 | 1139 | 874 | 3 | 262 | -0.10 [-1.15; +0.94] | -0.77 | 0.497 | -0.77 | 0.5921 | 0.59 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 479 | 418 | 22 | 39 | -0.44 [-1.05; +0.15] | -0.17 | 0.479 | -0.92 | 0.9195 | 0.98 | +0.01 / 0.04 / True | False / False |
| KT06 | + | AVR | 30 | 479 | 395 | 22 | 62 | +0.24 [-0.43; +0.72] | +0.12 | 0.513 | -0.23 | 0.2349 | 0.88 | -0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 479 | 378 | 20 | 81 | -0.00 [-0.78; +0.47] | -0.02 | 0.498 | -0.60 | 0.5043 | 0.80 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 184 | 141 | 38 | 5 | -1.20 [-3.40; +0.11] | -1.68 | 0.494 | -2.64 | 0.9471 | 0.59 | +0.03 / 0.00 / True | False / False |
| KT06 | + | BIST | 30 | 184 | 119 | 34 | 31 | -0.51 [-2.30; +1.77] | -2.91 | 0.509 | -1.49 | 0.7266 | 0.18 | -0.01 / 0.00 / True | False / False |
| KT06 | + | BIST | 45 | 184 | 115 | 33 | 36 | -2.15 [-8.19; +3.12] | -4.72 | 0.496 | -7.25 | 0.7948 | 0.11 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 53 | 52 | 0 | 1 | -1.72 [-5.49; +0.77] | -0.34 | 0.452 | -5.22 | 0.8910 | 0.19 | -0.06 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 53 | 50 | 0 | 3 | -1.92 [-6.30; +1.39] | -0.55 | 0.505 | -5.51 | 0.8810 | 0.08 | +0.02 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 53 | 42 | 0 | 11 | -5.79 [-12.31; -1.77] | -4.66 | 0.440 | -10.31 | 0.9902 | 0.06 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 13 | 12 | 0 | 1 | +2.68 [-5.67; +8.73] | +2.11 | 0.581 | -4.90 | 0.2475 | 0.08 | +0.07 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 13 | 9 | 0 | 4 | +5.34 [-3.04; +16.61] | +1.70 | 0.558 | -2.07 | 0.2439 | 0.06 | -0.24 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 13 | 8 | 0 | 5 | +1.28 [-10.30; +14.22] | -4.38 | 0.460 | -10.94 | 0.4429 | 0.05 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 58 | 56 | 2 | 0 | -0.35 [-8.49; +0.80] | -1.52 | 0.515 | -12.13 | 0.7479 | 0.24 | +0.14 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 58 | 56 | 1 | 1 | -2.06 [-9.13; +2.57] | -5.55 | 0.447 | -19.82 | 0.8768 | 0.10 | +0.26 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 58 | 56 | 1 | 1 | -2.92 [-12.90; -1.94] | -6.05 | 0.444 | -19.70 | 1.0000 | 0.07 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 780 | 772 | 2 | 6 | -0.07 [-1.08; +1.05] | -0.27 | 0.497 | -0.63 | 0.4435 | 0.99 | +0.02 / 0.05 / True | False / False |
| KT08 | - | ABD | 30 | 529 | 512 | 0 | 17 | +0.02 [-1.61; +1.90] | -0.91 | 0.496 | -0.96 | 0.5126 | 0.51 | +0.07 / 0.00 / True | False / False |
| KT08 | - | ABD | 45 | 448 | 394 | 2 | 52 | +0.92 [-0.85; +2.83] | -1.28 | 0.512 | -0.45 | 0.8046 | 0.28 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 184 | 181 | 1 | 2 | +0.59 [-0.49; +1.82] | +0.98 | 0.529 | +0.03 | 0.8632 | 0.74 | -0.02 / 0.00 / True | False / False |
| KT08 | - | AVR | 30 | 134 | 127 | 0 | 7 | +0.60 [-1.13; +1.58] | +1.33 | 0.530 | -0.58 | 0.7704 | 0.38 | -0.01 / 0.00 / True | False / False |
| KT08 | - | AVR | 45 | 121 | 101 | 1 | 19 | -0.49 [-3.98; +2.02] | +0.43 | 0.506 | -2.97 | 0.3588 | 0.25 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 326 | 262 | 13 | 51 | +0.46 [-4.25; +1.36] | -0.05 | 0.527 | -1.20 | 0.6217 | 0.88 | +0.04 / 0.07 / False | False / False |
| KT08 | - | BIST | 30 | 192 | 145 | 7 | 40 | +0.30 [-2.51; +1.62] | -1.33 | 0.530 | -0.24 | 0.6915 | 0.21 | +0.15 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 127 | 86 | 5 | 36 | -0.04 [-4.25; +3.74] | -0.85 | 0.552 | -4.54 | 0.4380 | 0.09 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 22 | 22 | 0 | 0 | -0.37 [-12.02; +10.43] | -0.24 | 0.489 | -9.77 | 0.5244 | 0.10 | +0.16 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 22 | 20 | 0 | 2 | +0.06 [-14.46; +11.78] | -2.96 | 0.444 | -13.74 | 0.4899 | 0.05 | +0.24 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 22 | 20 | 0 | 2 | +7.52 [-23.55; +38.00] | -4.62 | 0.446 | -23.78 | 0.3410 | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 3 | 3 | 0 | 0 | -0.35 [-33.25; +38.52] | -6.32 | 0.390 | - | 0.6226 | 0.05 | -0.32 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 3 | 3 | 0 | 0 | -20.32 [-89.16; +44.15] | -15.94 | 0.351 | - | 0.7541 | 0.04 | -0.32 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 3 | 2 | 0 | 1 | -13.65 [-40.63; +13.32] | -13.65 | 0.455 | - | 0.7496 | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 3609 | 3313 | 30 | 266 | -0.10 [-0.50; +0.37] | -0.53 | 0.496 | -0.37 | 0.6929 | 1.00 | -0.01 / 0.05 / True | False / False |
| KT10 | + | ABD | 30 | 2301 | 1972 | 20 | 309 | -0.25 [-1.31; +0.47] | -0.89 | 0.496 | -0.99 | 0.7452 | 0.99 | -0.00 / 0.06 / True | False / False |
| KT10 | + | ABD | 45 | 1859 | 1523 | 11 | 325 | -0.12 [-2.10; +1.64] | -1.44 | 0.491 | -1.53 | 0.5589 | 0.86 | - / - / False | False / False |

## Hücre: 2023Q1

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 320 | 313 | 7 | 0 | -1.96 [-4.61; +0.71] | -1.66 | 0.429 | - | - | 0.78 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 176 | 174 | 2 | 0 | -1.40 [-3.05; -0.21] | -2.70 | 0.453 | - | - | 0.19 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 134 | 134 | 0 | 0 | -1.47 [-3.85; +0.51] | -2.73 | 0.470 | - | - | 0.11 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 134 | 115 | 19 | 0 | -1.18 [-4.91; +0.45] | -1.87 | 0.448 | - | - | 0.52 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 91 | 78 | 13 | 0 | -2.32 [-5.48; -0.13] | -1.90 | 0.454 | - | - | 0.24 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 80 | 74 | 6 | 0 | -4.41 [-9.92; +3.90] | -4.31 | 0.398 | - | - | 0.19 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 524 | 517 | 7 | 0 | +0.20 [-0.77; +0.66] | +0.33 | 0.514 | - | - | 0.95 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 524 | 517 | 7 | 0 | +0.36 [-0.89; +2.09] | -0.50 | 0.507 | - | - | 0.52 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 524 | 517 | 7 | 0 | -0.29 [-1.26; +1.65] | -0.93 | 0.493 | - | - | 0.37 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 286 | 277 | 9 | 0 | -0.43 [-1.46; +0.48] | -0.35 | 0.482 | - | - | 0.91 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 286 | 277 | 9 | 0 | +0.50 [-0.43; +0.96] | +0.55 | 0.519 | - | - | 0.73 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 286 | 277 | 9 | 0 | +0.27 [-0.62; +0.63] | +0.33 | 0.510 | - | - | 0.65 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 23 | 18 | 5 | 0 | -5.93 [-8.35; +0.37] | -6.84 | 0.257 | - | - | 0.10 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 23 | 18 | 5 | 0 | -0.56 [-4.91; +10.77] | -1.87 | 0.507 | - | - | 0.06 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 23 | 18 | 5 | 0 | -6.89 [-9.38; -0.42] | -8.15 | 0.376 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 24 | 24 | 0 | 0 | +0.47 [-1.44; +2.89] | +0.19 | 0.544 | - | - | 0.11 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 24 | 24 | 0 | 0 | +1.18 [-0.32; +4.62] | -1.10 | 0.538 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 24 | 24 | 0 | 0 | -2.10 [-13.57; +2.39] | -0.69 | 0.470 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 3 | 3 | 0 | 0 | +1.41 [-15.91; +11.43] | +8.70 | 0.667 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 3 | 3 | 0 | 0 | +12.04 [-3.77; +20.02] | +19.86 | 0.792 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 3 | 3 | 0 | 0 | +15.11 [-10.75; +28.51] | +27.57 | 0.708 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 5 | 5 | 0 | 0 | -10.11 [-10.11; -10.11] | -9.61 | 0.034 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 5 | 5 | 0 | 0 | -5.13 [-5.13; -5.13] | -3.30 | 0.416 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 5 | 5 | 0 | 0 | -11.10 [-11.10; -11.10] | -14.87 | 0.261 | - | - | 0.03 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 459 | 454 | 5 | 0 | +0.24 [-0.63; +0.55] | +0.38 | 0.516 | - | - | 0.92 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 459 | 454 | 5 | 0 | +0.25 [-1.41; +2.10] | -0.51 | 0.505 | - | - | 0.46 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 459 | 454 | 5 | 0 | -0.35 [-1.29; +1.84] | -0.96 | 0.490 | - | - | 0.32 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 242 | 235 | 7 | 0 | -0.48 [-1.65; +0.75] | -0.56 | 0.476 | - | - | 0.85 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 242 | 235 | 7 | 0 | +0.20 [-0.95; +0.89] | +0.33 | 0.505 | - | - | 0.65 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 242 | 235 | 7 | 0 | -0.25 [-1.15; +0.36] | -0.02 | 0.493 | - | - | 0.56 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 21 | 16 | 5 | 0 | -5.78 [-8.58; +0.37] | -6.84 | 0.281 | - | - | 0.09 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 21 | 16 | 5 | 0 | -0.98 [-6.33; +10.77] | -1.87 | 0.489 | - | - | 0.06 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 21 | 16 | 5 | 0 | -6.69 [-9.54; -0.42] | -8.15 | 0.383 | - | - | 0.04 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 233 | 230 | 3 | 0 | +0.22 [-0.50; +0.43] | +0.36 | 0.523 | - | - | 0.65 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 233 | 230 | 3 | 0 | +0.59 [-0.69; +2.87] | +0.35 | 0.523 | - | - | 0.25 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 233 | 230 | 3 | 0 | +0.61 [-1.46; +3.36] | +0.21 | 0.507 | - | - | 0.17 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 127 | 125 | 2 | 0 | -0.76 [-2.27; -0.02] | -0.85 | 0.462 | - | - | 0.56 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 127 | 125 | 2 | 0 | -0.19 [-0.25; -0.16] | +0.20 | 0.501 | - | - | 0.38 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 127 | 125 | 2 | 0 | -1.26 [-2.19; +0.19] | -1.35 | 0.466 | - | - | 0.31 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 18 | 15 | 3 | 0 | -6.70 [-10.24; +0.37] | -6.54 | 0.231 | - | - | 0.08 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 18 | 15 | 3 | 0 | -1.42 [-7.52; +10.77] | -3.30 | 0.462 | - | - | 0.05 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 18 | 15 | 3 | 0 | -6.93 [-10.18; -0.42] | -10.72 | 0.362 | - | - | 0.04 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 518 | 511 | 7 | 0 | +0.15 [-0.92; +0.66] | +0.28 | 0.511 | - | - | 0.94 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 518 | 511 | 7 | 0 | +0.35 [-0.97; +2.09] | -0.56 | 0.507 | - | - | 0.51 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 518 | 511 | 7 | 0 | -0.30 [-1.29; +1.65] | -0.96 | 0.492 | - | - | 0.36 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 279 | 273 | 6 | 0 | -0.34 [-1.32; +0.61] | -0.32 | 0.485 | - | - | 0.90 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 279 | 273 | 6 | 0 | +0.58 [-0.46; +1.17] | +0.55 | 0.521 | - | - | 0.72 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 279 | 273 | 6 | 0 | +0.32 [-0.73; +0.87] | +0.33 | 0.511 | - | - | 0.64 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 23 | 18 | 5 | 0 | -5.93 [-8.35; +0.37] | -6.84 | 0.257 | - | - | 0.10 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 23 | 18 | 5 | 0 | -0.56 [-4.91; +10.77] | -1.87 | 0.507 | - | - | 0.06 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 23 | 18 | 5 | 0 | -6.89 [-9.38; -0.42] | -8.15 | 0.376 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 241 | 240 | 1 | 0 | +0.45 [+0.40; +0.48] | +0.23 | 0.523 | - | - | 0.67 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 241 | 240 | 1 | 0 | +0.74 [-0.10; +2.20] | +0.14 | 0.518 | - | - | 0.26 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 241 | 240 | 1 | 0 | -0.43 [-1.57; +0.79] | -0.69 | 0.490 | - | - | 0.18 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 184 | 179 | 5 | 0 | -0.32 [-1.40; +0.69] | -0.16 | 0.486 | - | - | 0.73 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 184 | 179 | 5 | 0 | +0.83 [+0.49; +1.12] | +0.95 | 0.542 | - | - | 0.52 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 184 | 179 | 5 | 0 | +0.41 [-0.13; +0.63] | +0.59 | 0.512 | - | - | 0.44 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 9 | 6 | 3 | 0 | -11.40 [-13.00; -8.19] | -11.37 | 0.138 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 9 | 6 | 3 | 0 | -2.50 [-9.57; +11.62] | -1.98 | 0.516 | - | - | 0.04 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 9 | 6 | 3 | 0 | -6.66 [-14.97; +9.95] | -8.51 | 0.369 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 9 | 9 | 0 | 0 | +1.15 [+1.15; +1.15] | -0.26 | 0.530 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 9 | 9 | 0 | 0 | +1.35 [+1.35; +1.35] | -1.54 | 0.556 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 9 | 9 | 0 | 0 | -5.81 [-5.81; -5.81] | -2.68 | 0.420 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 1 | 1 | 0 | 0 | -15.91 [-15.91; -15.91] | -15.91 | 0.000 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 1 | 1 | 0 | 0 | -3.77 [-3.77; -3.77] | -3.77 | 0.375 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 1 | 1 | 0 | 0 | -10.75 [-10.75; -10.75] | -10.75 | 0.125 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 2 | 2 | 0 | 0 | -13.78 [-13.78; -13.78] | -13.78 | 0.000 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 2 | 2 | 0 | 0 | -15.49 [-15.49; -15.49] | -15.49 | 0.038 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 45 | 2 | 2 | 0 | 0 | -18.36 [-18.36; -18.36] | -18.36 | 0.038 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 137 | 137 | 0 | 0 | +1.85 [-1.28; +6.99] | -0.98 | 0.502 | - | - | 0.43 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 101 | 101 | 0 | 0 | +3.14 [-2.84; +5.16] | +0.35 | 0.516 | - | - | 0.12 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 97 | 97 | 0 | 0 | -0.65 [-3.18; +5.71] | -7.20 | 0.464 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 15 | 14 | 1 | 0 | +2.40 [+1.08; +5.90] | +1.74 | 0.615 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 11 | 11 | 0 | 0 | +0.21 [-2.62; +12.84] | +2.71 | 0.565 | - | - | 0.06 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 12 | 11 | 1 | 0 | -0.41 [-2.24; +15.80] | -0.43 | 0.453 | - | - | 0.05 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 52 | 50 | 2 | 0 | +0.46 [-1.92; +1.35] | +0.24 | 0.561 | - | - | 0.22 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 35 | 34 | 1 | 0 | -0.04 [-0.88; +0.27] | -3.57 | 0.507 | - | - | 0.08 | - / - / False | False / False |
| KT08 | - | BIST | 45 | 15 | 15 | 0 | 0 | +2.45 [-0.40; +4.95] | +0.58 | 0.578 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 9 | 9 | 0 | 0 | +11.10 [-2.63; +18.05] | +8.64 | 0.725 | - | - | 0.06 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 9 | 9 | 0 | 0 | +9.34 [-4.97; +34.67] | +2.25 | 0.600 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 9 | 9 | 0 | 0 | +11.74 [-12.92; +62.13] | +4.88 | 0.567 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | +38.52 [+38.52; +38.52] | +38.52 | 1.000 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | +44.15 [+44.15; +44.15] | +44.15 | 1.000 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | +13.32 [+13.32; +13.32] | +13.32 | 0.909 | - | - | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1006 | 993 | 13 | 0 | -0.05 [-0.05; -0.04] | -0.71 | 0.491 | - | - | 1.00 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 671 | 661 | 10 | 0 | +0.07 [-0.67; +1.03] | -0.65 | 0.498 | - | - | 0.64 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 481 | 475 | 6 | 0 | -0.67 [-3.39; +1.41] | -2.45 | 0.474 | - | - | 0.34 | - / - / False | False / False |

## Hücre: 2023Q2

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 322 | 322 | 0 | 0 | +1.37 [-1.00; +3.08] | +0.50 | 0.537 | - | - | 0.80 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 202 | 202 | 0 | 0 | +1.13 [-2.75; +6.28] | -0.83 | 0.519 | - | - | 0.22 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 149 | 149 | 0 | 0 | +0.07 [-4.24; +2.09] | -3.39 | 0.477 | - | - | 0.12 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 137 | 130 | 7 | 0 | +1.01 [+0.70; +1.21] | +1.17 | 0.556 | - | - | 0.58 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 81 | 78 | 3 | 0 | +1.06 [+0.06; +2.17] | +1.03 | 0.540 | - | - | 0.24 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 62 | 60 | 2 | 0 | +0.52 [-1.47; +1.51] | +1.95 | 0.526 | - | - | 0.16 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 603 | 598 | 5 | 0 | +0.12 [-0.02; +0.26] | -0.30 | 0.510 | - | - | 0.97 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 603 | 598 | 5 | 0 | +0.57 [+0.14; +0.96] | -0.19 | 0.526 | - | - | 0.59 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 603 | 598 | 5 | 0 | +0.11 [-0.95; +0.65] | -0.13 | 0.518 | - | - | 0.42 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 202 | 185 | 17 | 0 | +0.38 [-0.57; +0.80] | +0.24 | 0.524 | - | - | 0.75 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 202 | 185 | 17 | 0 | +0.53 [-0.15; +1.18] | +0.14 | 0.523 | - | - | 0.53 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 202 | 185 | 17 | 0 | +0.16 [-0.70; +0.58] | -0.45 | 0.507 | - | - | 0.45 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 123 | 106 | 17 | 0 | -0.21 [-1.24; +0.05] | -1.01 | 0.516 | - | - | 0.45 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 123 | 106 | 17 | 0 | -1.98 [-3.48; -1.02] | -4.41 | 0.468 | - | - | 0.16 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 123 | 106 | 17 | 0 | -3.36 [-14.87; +2.99] | -5.60 | 0.483 | - | - | 0.10 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 68 | 68 | 0 | 0 | +0.86 [+0.18; +2.68] | -0.10 | 0.522 | - | - | 0.23 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 68 | 68 | 0 | 0 | +2.95 [+1.28; +4.66] | +4.97 | 0.598 | - | - | 0.09 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 68 | 68 | 0 | 0 | +0.23 [-0.75; +1.06] | +0.50 | 0.532 | - | - | 0.07 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 7 | 7 | 0 | 0 | +5.97 [-5.59; +11.03] | +7.39 | 0.758 | - | - | 0.06 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 7 | 7 | 0 | 0 | +5.80 [-2.14; +17.45] | +3.77 | 0.626 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 7 | 7 | 0 | 0 | +3.79 [-11.03; +21.22] | +4.69 | 0.587 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 69 | 69 | 0 | 0 | -0.01 [-2.90; +0.42] | -0.78 | 0.528 | - | - | 0.30 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 69 | 69 | 0 | 0 | -1.35 [-1.67; -0.19] | -5.31 | 0.473 | - | - | 0.12 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 69 | 69 | 0 | 0 | -1.27 [-7.28; +4.20] | -5.24 | 0.478 | - | - | 0.08 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 526 | 523 | 3 | 0 | +0.07 [-0.05; +0.22] | -0.41 | 0.506 | - | - | 0.95 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 526 | 523 | 3 | 0 | +0.19 [-0.15; +0.41] | -0.36 | 0.517 | - | - | 0.52 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 526 | 523 | 3 | 0 | -0.10 [-1.13; +0.51] | -0.49 | 0.512 | - | - | 0.37 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 174 | 160 | 14 | 0 | +0.38 [-0.78; +1.05] | +0.24 | 0.524 | - | - | 0.68 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 174 | 160 | 14 | 0 | +0.50 [-0.16; +0.94] | +0.04 | 0.524 | - | - | 0.47 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 174 | 160 | 14 | 0 | +0.42 [-0.51; +0.91] | -0.43 | 0.520 | - | - | 0.39 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 116 | 100 | 16 | 0 | -0.31 [-0.94; +0.21] | -1.25 | 0.511 | - | - | 0.43 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 116 | 100 | 16 | 0 | -1.78 [-2.43; -1.40] | -4.23 | 0.469 | - | - | 0.15 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 116 | 100 | 16 | 0 | -3.54 [-14.48; +1.28] | -5.92 | 0.481 | - | - | 0.10 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 241 | 240 | 1 | 0 | +0.47 [-1.05; +1.76] | -0.05 | 0.523 | - | - | 0.67 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 241 | 240 | 1 | 0 | -0.08 [-2.07; +1.15] | -0.35 | 0.520 | - | - | 0.26 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 241 | 240 | 1 | 0 | -0.99 [-3.40; +0.99] | -1.13 | 0.498 | - | - | 0.18 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 111 | 102 | 9 | 0 | +0.37 [-0.36; +1.51] | +0.30 | 0.532 | - | - | 0.47 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 111 | 102 | 9 | 0 | +0.39 [-0.58; +1.18] | +0.24 | 0.523 | - | - | 0.31 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 111 | 102 | 9 | 0 | -0.27 [-0.54; +0.09] | -0.52 | 0.501 | - | - | 0.26 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 97 | 87 | 10 | 0 | +0.23 [-1.56; +0.89] | -0.78 | 0.542 | - | - | 0.37 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 97 | 87 | 10 | 0 | -0.98 [-1.60; +1.24] | -3.97 | 0.483 | - | - | 0.14 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 97 | 87 | 10 | 0 | -1.11 [-4.66; +1.25] | -5.00 | 0.498 | - | - | 0.09 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 597 | 592 | 5 | 0 | +0.11 [+0.01; +0.22] | -0.30 | 0.511 | - | - | 0.97 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 597 | 592 | 5 | 0 | +0.52 [+0.18; +0.84] | -0.23 | 0.525 | - | - | 0.58 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 597 | 592 | 5 | 0 | +0.04 [-0.88; +0.51] | -0.26 | 0.517 | - | - | 0.42 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 200 | 183 | 17 | 0 | +0.30 [-0.66; +0.78] | +0.21 | 0.518 | - | - | 0.74 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 200 | 183 | 17 | 0 | +0.46 [-0.27; +1.18] | +0.10 | 0.519 | - | - | 0.53 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 200 | 183 | 17 | 0 | +0.10 [-0.82; +0.53] | -0.59 | 0.504 | - | - | 0.45 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 121 | 104 | 17 | 0 | -0.38 [-1.24; +0.04] | -1.25 | 0.511 | - | - | 0.44 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 121 | 104 | 17 | 0 | -2.26 [-3.48; -1.02] | -4.82 | 0.461 | - | - | 0.16 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 121 | 104 | 17 | 0 | -3.85 [-14.87; +2.99] | -6.05 | 0.478 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 367 | 365 | 2 | 0 | -0.09 [-0.72; +0.48] | -0.61 | 0.498 | - | - | 0.84 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 367 | 365 | 2 | 0 | +0.50 [+0.02; +0.78] | -0.36 | 0.513 | - | - | 0.38 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 367 | 365 | 2 | 0 | +0.01 [-0.94; +1.12] | -0.62 | 0.508 | - | - | 0.26 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 117 | 106 | 11 | 0 | -0.21 [-0.56; +0.35] | -0.68 | 0.482 | - | - | 0.49 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 117 | 106 | 11 | 0 | -0.03 [-0.70; +0.49] | -0.12 | 0.495 | - | - | 0.32 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 117 | 106 | 11 | 0 | -0.36 [-1.37; +0.99] | -1.27 | 0.479 | - | - | 0.26 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 55 | 45 | 10 | 0 | +0.06 [-0.87; +0.81] | -0.87 | 0.546 | - | - | 0.20 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 55 | 45 | 10 | 0 | +0.33 [-1.46; +6.24] | -4.49 | 0.500 | - | - | 0.09 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 55 | 45 | 10 | 0 | -0.46 [-6.81; +9.58] | -2.44 | 0.526 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 22 | 22 | 0 | 0 | +0.61 [-4.48; +2.13] | +0.75 | 0.524 | - | - | 0.10 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 22 | 22 | 0 | 0 | +0.45 [-3.03; +5.04] | +2.82 | 0.593 | - | - | 0.05 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 22 | 22 | 0 | 0 | -3.34 [-13.40; +1.53] | -1.20 | 0.514 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 5 | 5 | 0 | 0 | +4.11 [-5.59; +11.03] | +3.61 | 0.675 | - | - | 0.05 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 5 | 5 | 0 | 0 | +5.32 [-4.00; +17.45] | +3.77 | 0.530 | - | - | 0.05 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 5 | 5 | 0 | 0 | +3.20 [-11.03; +21.22] | -4.37 | 0.496 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 53 | 53 | 0 | 0 | +0.32 [-0.47; +0.98] | -1.08 | 0.539 | - | - | 0.23 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 53 | 53 | 0 | 0 | -1.05 [-2.79; +8.59] | -4.33 | 0.471 | - | - | 0.10 | - / - / False | False / False |
| KT07 | + | BIST | 45 | 53 | 53 | 0 | 0 | -1.97 [-2.34; -1.93] | -5.88 | 0.463 | - | - | 0.07 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 213 | 213 | 0 | 0 | -0.88 [-3.50; +1.28] | -1.38 | 0.485 | - | - | 0.61 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 142 | 142 | 0 | 0 | -1.16 [-3.91; +2.96] | -3.11 | 0.484 | - | - | 0.16 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 114 | 114 | 0 | 0 | -0.26 [-3.90; +1.27] | -1.19 | 0.499 | - | - | 0.10 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 42 | 42 | 0 | 0 | +1.18 [-1.93; +2.72] | -0.79 | 0.519 | - | - | 0.21 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 30 | 30 | 0 | 0 | -0.11 [-2.37; +0.50] | -0.61 | 0.482 | - | - | 0.11 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 28 | 28 | 0 | 0 | +0.82 [-3.11; +3.46] | +0.27 | 0.535 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 212 | 211 | 1 | 0 | +0.45 [-16.90; +1.38] | -0.45 | 0.518 | - | - | 0.79 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 112 | 111 | 1 | 0 | +0.40 [-16.52; +2.29] | -0.60 | 0.537 | - | - | 0.17 | - / - / False | False / False |
| KT08 | - | BIST | 45 | 72 | 71 | 1 | 0 | -0.56 [-4.54; +2.52] | -1.68 | 0.546 | - | - | 0.08 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 6 | 6 | 0 | 0 | -9.73 [-24.04; -2.58] | -9.90 | 0.355 | - | - | 0.05 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 6 | 6 | 0 | 0 | -0.78 [-22.15; +9.91] | -8.68 | 0.437 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 6 | 6 | 0 | 0 | +25.09 [-46.68; +60.98] | +21.32 | 0.503 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | AVR | 30 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | AVR | 45 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT10 | + | ABD | 15 | 952 | 950 | 2 | 0 | -0.67 [-1.13; -0.27] | -1.69 | 0.470 | - | - | 1.00 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 510 | 509 | 1 | 0 | -1.52 [-3.25; -0.81] | -2.96 | 0.462 | - | - | 0.51 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 524 | 523 | 1 | 0 | -1.24 [-4.55; +1.71] | -3.41 | 0.468 | - | - | 0.37 | - / - / False | False / False |

## Hücre: 2023Q3

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 324 | 320 | 4 | 0 | -0.03 [-2.54; +3.21] | -1.13 | 0.488 | - | - | 0.79 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 192 | 192 | 0 | 0 | -0.96 [-3.65; +1.79] | -1.69 | 0.496 | - | - | 0.21 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 142 | 142 | 0 | 0 | -0.63 [-4.20; +2.03] | -1.54 | 0.492 | - | - | 0.11 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 139 | 114 | 25 | 0 | -0.72 [-2.98; +2.51] | -0.31 | 0.470 | - | - | 0.52 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 90 | 80 | 10 | 0 | -1.16 [-4.55; +3.58] | +0.05 | 0.482 | - | - | 0.25 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 65 | 57 | 8 | 0 | -0.70 [-3.63; +3.26] | -2.19 | 0.441 | - | - | 0.15 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 435 | 435 | 0 | 0 | -0.61 [-1.04; +0.19] | -0.58 | 0.475 | - | - | 0.90 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 435 | 435 | 0 | 0 | -0.73 [-1.17; -0.50] | -1.07 | 0.476 | - | - | 0.44 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 435 | 435 | 0 | 0 | -1.19 [-1.84; -0.93] | -1.75 | 0.469 | - | - | 0.31 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 161 | 153 | 8 | 0 | -0.54 [-1.23; +1.68] | +0.23 | 0.497 | - | - | 0.66 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 161 | 153 | 8 | 0 | -0.24 [-1.74; +3.01] | -0.26 | 0.507 | - | - | 0.45 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 161 | 153 | 8 | 0 | -0.22 [-1.15; +0.91] | +0.82 | 0.503 | - | - | 0.38 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 129 | 106 | 23 | 0 | -2.14 [-4.25; -0.05] | -1.67 | 0.471 | - | - | 0.45 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 129 | 106 | 23 | 0 | -3.18 [-3.85; -2.48] | -4.15 | 0.469 | - | - | 0.16 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 129 | 106 | 23 | 0 | -4.35 [-9.23; -2.72] | -6.93 | 0.460 | - | - | 0.10 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 16 | 16 | 0 | 0 | +0.04 [-15.67; +1.63] | -1.75 | 0.437 | - | - | 0.08 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 16 | 16 | 0 | 0 | -0.17 [-24.14; +4.22] | +0.40 | 0.444 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 16 | 16 | 0 | 0 | -4.92 [-31.91; +0.80] | -5.89 | 0.401 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 2 | 2 | 0 | 0 | +0.46 [+0.46; +0.46] | +0.46 | 0.392 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 2 | 2 | 0 | 0 | -1.03 [-1.03; -1.03] | -1.03 | 0.496 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 2 | 2 | 0 | 0 | +2.51 [+2.51; +2.51] | +2.51 | 0.537 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 3 | 1 | 2 | 0 | -8.83 [-8.83; -8.83] | -8.83 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 3 | 1 | 2 | 0 | -28.47 [-28.47; -28.47] | -28.47 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 3 | 1 | 2 | 0 | -22.38 [-22.38; -22.38] | -22.38 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 373 | 373 | 0 | 0 | -0.58 [-1.16; +0.31] | -0.64 | 0.477 | - | - | 0.85 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 373 | 373 | 0 | 0 | -0.61 [-0.73; -0.23] | -1.17 | 0.478 | - | - | 0.39 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 373 | 373 | 0 | 0 | -1.06 [-1.17; -0.79] | -1.75 | 0.470 | - | - | 0.27 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 135 | 128 | 7 | 0 | +0.00 [-0.41; +1.16] | +0.36 | 0.512 | - | - | 0.57 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 135 | 128 | 7 | 0 | +0.97 [-0.19; +3.12] | +1.63 | 0.544 | - | - | 0.38 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 135 | 128 | 7 | 0 | +1.06 [+0.74; +1.65] | +1.77 | 0.538 | - | - | 0.32 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 115 | 94 | 21 | 0 | -2.14 [-5.06; +0.51] | -3.72 | 0.463 | - | - | 0.40 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 115 | 94 | 21 | 0 | -2.82 [-4.55; -1.11] | -4.48 | 0.467 | - | - | 0.15 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 115 | 94 | 21 | 0 | -3.72 [-8.56; -1.85] | -6.10 | 0.463 | - | - | 0.09 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 272 | 272 | 0 | 0 | -1.00 [-1.77; +0.43] | -0.61 | 0.459 | - | - | 0.72 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 272 | 272 | 0 | 0 | -1.29 [-1.78; +0.02] | -1.47 | 0.463 | - | - | 0.29 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 272 | 272 | 0 | 0 | -2.29 [-2.97; -1.07] | -2.57 | 0.443 | - | - | 0.20 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 92 | 87 | 5 | 0 | +0.37 [-0.86; +1.45] | +0.46 | 0.505 | - | - | 0.41 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 92 | 87 | 5 | 0 | +0.85 [-0.16; +1.76] | +1.24 | 0.532 | - | - | 0.27 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 92 | 87 | 5 | 0 | +1.60 [-2.21; +3.83] | +2.04 | 0.531 | - | - | 0.22 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 94 | 76 | 18 | 0 | -2.18 [-4.10; +0.10] | -2.45 | 0.471 | - | - | 0.33 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 94 | 76 | 18 | 0 | -3.54 [-5.22; -2.61] | -5.18 | 0.457 | - | - | 0.13 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 94 | 76 | 18 | 0 | -4.42 [-10.84; -2.27] | -6.93 | 0.461 | - | - | 0.08 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 433 | 433 | 0 | 0 | -0.61 [-1.10; +0.19] | -0.58 | 0.475 | - | - | 0.90 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 433 | 433 | 0 | 0 | -0.69 [-0.85; -0.50] | -1.10 | 0.476 | - | - | 0.44 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 433 | 433 | 0 | 0 | -1.12 [-1.47; -0.95] | -1.75 | 0.469 | - | - | 0.31 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 159 | 151 | 8 | 0 | -0.56 [-1.23; +1.68] | +0.23 | 0.499 | - | - | 0.65 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 159 | 151 | 8 | 0 | -0.25 [-1.74; +3.01] | -0.26 | 0.508 | - | - | 0.45 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 159 | 151 | 8 | 0 | -0.26 [-1.15; +0.83] | +0.78 | 0.503 | - | - | 0.37 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 129 | 106 | 23 | 0 | -2.14 [-4.25; -0.05] | -1.67 | 0.471 | - | - | 0.45 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 129 | 106 | 23 | 0 | -3.18 [-3.85; -2.48] | -4.15 | 0.469 | - | - | 0.16 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 129 | 106 | 23 | 0 | -4.35 [-9.23; -2.72] | -6.93 | 0.460 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 229 | 229 | 0 | 0 | +0.05 [-0.27; +0.91] | +0.05 | 0.505 | - | - | 0.64 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 229 | 229 | 0 | 0 | -0.21 [-2.74; +0.82] | -0.85 | 0.490 | - | - | 0.24 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 229 | 229 | 0 | 0 | -0.79 [-3.98; +0.27] | -1.54 | 0.474 | - | - | 0.17 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 87 | 84 | 3 | 0 | -0.81 [-1.09; +0.20] | +0.10 | 0.470 | - | - | 0.40 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 87 | 84 | 3 | 0 | -0.56 [-1.11; +0.21] | -0.30 | 0.490 | - | - | 0.26 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 87 | 84 | 3 | 0 | -0.14 [-2.86; +0.80] | +0.97 | 0.496 | - | - | 0.21 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 72 | 57 | 15 | 0 | -1.17 [-3.95; +0.63] | +0.10 | 0.501 | - | - | 0.25 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 72 | 57 | 15 | 0 | -1.31 [-4.29; -0.15] | -1.79 | 0.513 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 72 | 57 | 15 | 0 | -3.86 [-13.92; +1.08] | -6.01 | 0.479 | - | - | 0.07 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 8 | 8 | 0 | 0 | -4.87 [-15.67; +1.24] | -2.30 | 0.367 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 8 | 8 | 0 | 0 | -6.41 [-24.14; -1.73] | -4.65 | 0.377 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 8 | 8 | 0 | 0 | -13.44 [-39.03; -7.20] | -14.44 | 0.265 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 2 | 2 | 0 | 0 | +0.46 [+0.46; +0.46] | +0.46 | 0.392 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 2 | 2 | 0 | 0 | -1.03 [-1.03; -1.03] | -1.03 | 0.496 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 2 | 2 | 0 | 0 | +2.51 [+2.51; +2.51] | +2.51 | 0.537 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 1 | 1 | 0 | 0 | -8.83 [-8.83; -8.83] | -8.83 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 1 | 1 | 0 | 0 | -28.47 [-28.47; -28.47] | -28.47 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 45 | 1 | 1 | 0 | 0 | -22.38 [-22.38; -22.38] | -22.38 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 177 | 175 | 2 | 0 | +0.33 [-0.25; +5.56] | +0.85 | 0.517 | - | - | 0.53 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 122 | 122 | 0 | 0 | +0.10 [-0.18; +2.18] | +0.92 | 0.510 | - | - | 0.14 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 95 | 93 | 2 | 0 | +1.64 [-0.52; +9.86] | +2.53 | 0.545 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 47 | 47 | 0 | 0 | +0.00 [-1.43; +0.53] | +1.13 | 0.512 | - | - | 0.23 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 37 | 37 | 0 | 0 | -0.05 [-1.90; +1.53] | +1.06 | 0.540 | - | - | 0.13 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 30 | 30 | 0 | 0 | -4.88 [-5.59; -4.05] | -2.75 | 0.457 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 4 | 0 | 4 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | BIST | 30 | 2 | 0 | 2 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | BIST | 45 | 2 | 0 | 2 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 15 | 5 | 5 | 0 | 0 | -16.73 [-20.88; -11.77] | -14.74 | 0.095 | - | - | 0.05 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 5 | 5 | 0 | 0 | -15.64 [-17.38; -15.13] | -17.38 | 0.173 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 5 | 5 | 0 | 0 | -21.14 [-31.55; -13.27] | -24.50 | 0.159 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | -33.25 [-33.25; -33.25] | -33.25 | 0.000 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | -15.94 [-15.94; -15.94] | -15.94 | 0.053 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | -40.63 [-40.63; -40.63] | -40.63 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1092 | 1085 | 7 | 0 | +0.02 [-0.42; +0.45] | +0.07 | 0.513 | - | - | 1.00 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 693 | 690 | 3 | 0 | +0.87 [+0.52; +1.33] | +0.92 | 0.529 | - | - | 0.66 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 489 | 486 | 3 | 0 | +1.85 [+0.10; +3.54] | +1.29 | 0.542 | - | - | 0.34 | - / - / False | False / False |

## Hücre: 2023Q4

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 324 | 314 | 10 | 0 | +3.40 [-0.35; +6.48] | +1.61 | 0.549 | - | - | 0.79 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 186 | 119 | 3 | 64 | +2.06 [-0.30; +4.72] | +2.78 | 0.560 | - | - | 0.14 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 155 | 55 | 0 | 100 | -2.83 [-2.83; -2.83] | -3.00 | 0.445 | - | - | 0.06 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 138 | 115 | 23 | 0 | -1.13 [-2.72; +0.50] | -1.48 | 0.434 | - | - | 0.52 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 86 | 41 | 12 | 33 | -1.01 [-1.22; -0.70] | -1.63 | 0.466 | - | - | 0.14 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 63 | 17 | 4 | 42 | +1.39 [+1.39; +1.39] | +0.84 | 0.519 | - | - | 0.07 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 480 | 285 | 1 | 194 | +0.17 [-0.07; +0.30] | -0.31 | 0.498 | - | - | 0.74 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 480 | 183 | 1 | 296 | +1.65 [+0.56; +3.16] | +1.05 | 0.539 | - | - | 0.20 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 480 | 75 | 1 | 404 | +5.18 [+5.18; +5.18] | +2.84 | 0.583 | - | - | 0.08 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 166 | 80 | 9 | 77 | +0.17 [-1.22; +1.25] | +0.59 | 0.504 | - | - | 0.38 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 166 | 42 | 7 | 117 | +0.49 [-0.73; +1.16] | -0.58 | 0.478 | - | - | 0.14 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 166 | 14 | 5 | 147 | -0.42 [-0.42; -0.42] | +0.06 | 0.521 | - | - | 0.06 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 106 | 73 | 24 | 9 | -0.05 [-1.54; +0.32] | -4.25 | 0.469 | - | - | 0.32 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 106 | 29 | 15 | 62 | +1.93 [+1.66; +2.53] | -0.56 | 0.501 | - | - | 0.07 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 106 | 20 | 10 | 76 | +7.90 [+7.90; +7.90] | -7.13 | 0.499 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 38 | 30 | 0 | 8 | -2.48 [-7.47; +0.37] | -1.75 | 0.387 | - | - | 0.12 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 38 | 23 | 0 | 15 | -1.90 [-2.36; -1.61] | -3.93 | 0.477 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 38 | 8 | 0 | 30 | -0.35 [-0.35; -0.35] | -0.06 | 0.505 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 8 | 7 | 0 | 1 | +5.76 [-3.26; +7.27] | +6.45 | 0.695 | - | - | 0.06 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 8 | 4 | 0 | 4 | +11.87 [+11.87; +11.87] | +10.49 | 0.719 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 8 | 0 | 0 | 8 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT02 | + | BIST | 15 | 4 | 0 | 4 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT02 | + | BIST | 30 | 4 | 0 | 2 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT02 | + | BIST | 45 | 4 | 0 | 1 | 3 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT03 | + | ABD | 15 | 434 | 253 | 1 | 180 | +0.14 [-0.21; +0.52] | -0.39 | 0.489 | - | - | 0.69 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 434 | 160 | 1 | 273 | +1.97 [+0.80; +3.67] | +1.61 | 0.545 | - | - | 0.18 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 434 | 63 | 1 | 370 | +5.63 [+5.63; +5.63] | +2.84 | 0.587 | - | - | 0.07 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 149 | 71 | 8 | 70 | +0.32 [-1.22; +1.71] | +0.65 | 0.514 | - | - | 0.34 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 149 | 35 | 6 | 108 | +1.83 [-0.70; +3.32] | -0.28 | 0.506 | - | - | 0.12 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 149 | 12 | 4 | 133 | -0.85 [-0.85; -0.85] | -3.19 | 0.517 | - | - | 0.06 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 90 | 67 | 16 | 7 | +0.72 [-0.96; +1.57] | -3.54 | 0.488 | - | - | 0.29 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 90 | 27 | 8 | 55 | +3.48 [+2.53; +3.95] | +0.29 | 0.531 | - | - | 0.07 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 90 | 18 | 4 | 68 | +10.83 [+10.83; +10.83] | -3.67 | 0.519 | - | - | 0.05 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 277 | 175 | 1 | 101 | -0.37 [-1.79; +0.74] | -0.34 | 0.485 | - | - | 0.53 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 277 | 133 | 1 | 143 | +2.14 [+1.73; +2.68] | +1.62 | 0.558 | - | - | 0.15 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 277 | 55 | 1 | 221 | +3.82 [+3.82; +3.82] | +1.80 | 0.563 | - | - | 0.06 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 98 | 44 | 7 | 47 | -0.29 [-1.94; +1.70] | +0.46 | 0.485 | - | - | 0.22 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 98 | 23 | 7 | 68 | -0.54 [-1.34; +0.35] | -0.79 | 0.454 | - | - | 0.09 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 98 | 12 | 5 | 81 | -1.45 [-1.45; -1.45] | +0.06 | 0.513 | - | - | 0.06 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 62 | 44 | 15 | 3 | +1.27 [-3.64; +2.77] | -4.00 | 0.450 | - | - | 0.19 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 62 | 20 | 9 | 33 | +3.69 [+3.01; +5.70] | -1.55 | 0.504 | - | - | 0.06 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 62 | 15 | 7 | 40 | +8.89 [+8.89; +8.89] | -8.77 | 0.474 | - | - | 0.04 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 458 | 266 | 1 | 191 | -0.00 [-0.05; +0.07] | -0.32 | 0.494 | - | - | 0.71 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 458 | 173 | 1 | 284 | +1.15 [+0.27; +2.28] | +1.05 | 0.536 | - | - | 0.19 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 458 | 74 | 1 | 383 | +4.20 [+4.20; +4.20] | +2.76 | 0.577 | - | - | 0.07 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 151 | 74 | 8 | 69 | -0.26 [-1.66; +0.69] | +0.34 | 0.486 | - | - | 0.35 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 151 | 39 | 7 | 105 | -0.14 [-0.73; +0.23] | -0.60 | 0.465 | - | - | 0.14 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 151 | 14 | 5 | 132 | -0.42 [-0.42; -0.42] | +0.06 | 0.521 | - | - | 0.06 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 106 | 73 | 24 | 9 | -0.05 [-1.54; +0.32] | -4.25 | 0.469 | - | - | 0.32 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 106 | 29 | 15 | 62 | +1.93 [+1.66; +2.53] | -0.56 | 0.501 | - | - | 0.07 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 106 | 20 | 10 | 76 | +7.90 [+7.90; +7.90] | -7.13 | 0.499 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 302 | 169 | 0 | 133 | +0.32 [-0.34; +1.18] | +0.11 | 0.512 | - | - | 0.51 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 302 | 91 | 0 | 211 | +1.04 [-0.29; +2.66] | +0.98 | 0.525 | - | - | 0.11 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 302 | 40 | 0 | 262 | +4.86 [+4.86; +4.86] | +2.88 | 0.578 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 91 | 49 | 3 | 39 | -0.75 [-2.06; +0.30] | +0.51 | 0.465 | - | - | 0.24 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 91 | 26 | 3 | 62 | -0.08 [-2.12; +1.20] | -0.67 | 0.465 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 91 | 9 | 1 | 81 | -2.69 [-2.69; -2.69] | -1.44 | 0.475 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 48 | 33 | 10 | 5 | -1.12 [-6.96; +2.25] | -3.76 | 0.477 | - | - | 0.15 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 48 | 11 | 6 | 31 | +1.34 [-0.04; +3.77] | +0.91 | 0.518 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 48 | 7 | 5 | 36 | +4.76 [+4.76; +4.76] | -3.58 | 0.548 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 14 | 13 | 0 | 1 | -5.71 [-10.31; -1.73] | -3.63 | 0.328 | - | - | 0.07 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 14 | 11 | 0 | 3 | -6.08 [-8.31; -4.81] | -6.25 | 0.381 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 14 | 3 | 0 | 11 | -3.29 [-3.29; -3.29] | -5.18 | 0.417 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 5 | 4 | 0 | 1 | +6.64 [-3.26; +9.94] | +6.74 | 0.705 | - | - | 0.05 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 5 | 1 | 0 | 4 | +27.26 [+27.26; +27.26] | +27.26 | 1.000 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 5 | 0 | 0 | 5 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 15 | 2 | 0 | 2 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 30 | 2 | 0 | 1 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 45 | 2 | 0 | 1 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | ABD | 15 | 253 | 247 | 0 | 6 | -0.72 [-1.39; -0.36] | +0.34 | 0.491 | - | - | 0.68 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 164 | 147 | 0 | 17 | -1.03 [-4.51; -0.32] | -1.29 | 0.484 | - | - | 0.17 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 142 | 90 | 0 | 52 | +3.33 [+3.33; +3.33] | -0.72 | 0.546 | - | - | 0.08 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 80 | 78 | 0 | 2 | +0.29 [-2.20; +13.92] | +1.09 | 0.529 | - | - | 0.37 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 56 | 49 | 0 | 7 | +1.61 [+1.56; +2.27] | +2.91 | 0.545 | - | - | 0.16 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 51 | 32 | 0 | 19 | +2.44 [+2.44; +2.44] | +6.11 | 0.545 | - | - | 0.10 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 58 | 1 | 6 | 51 | +1.63 [+1.63; +1.63] | +1.63 | 0.625 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 43 | 0 | 3 | 40 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | BIST | 45 | 38 | 0 | 2 | 36 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 15 | 2 | 2 | 0 | 0 | +16.99 [+3.38; +30.60] | +16.99 | 0.811 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 45 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | -6.32 [-6.32; -6.32] | -6.32 | 0.171 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | -89.16 [-89.16; -89.16] | -89.16 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 45 | 1 | 0 | 0 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT10 | + | ABD | 15 | 559 | 285 | 8 | 266 | +1.12 [-1.62; +4.47] | +0.57 | 0.530 | - | - | 0.74 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 427 | 112 | 6 | 309 | -3.28 [-4.14; -1.77] | -3.92 | 0.430 | - | - | 0.13 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 365 | 39 | 1 | 325 | -3.00 [-3.00; -3.00] | -7.84 | 0.359 | - | - | 0.05 | - / - / False | False / False |

FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok.
