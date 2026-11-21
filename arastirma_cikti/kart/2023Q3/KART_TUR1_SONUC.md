# KART TURU 1 — sonuç (açık kesik 2023-09-30, açılmış blok 3: 2023Q1, 2023Q2, 2023Q3)

KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test

Bakış: BİLGİ (karar bakışı değil). KASA kapısı: kesik 2023-09-30, dosyalar en geç {'/tmp/kasa/acik/V_ABD.pkl': '2023-09-29', '/tmp/kasa/acik/V_AVR.pkl': '2023-09-29', '/tmp/kasa/acik/V_BIST.pkl': '2023-09-29', '/tmp/kasa/acik/k34_yahoo.pkl': '2023-09-29'}. Çıktı en geç tarih: {'kt_satir.csv.gz': '2023-09-29', 'olculen_son_giris': {'15': '2023-09-11', '30': '2023-08-21', '45': '2023-07-31'}}.
Ön kayıt kapısı: {'onkayit': 'arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md', 'commit': 'e0976cbd77685d0bafc6f8d31af2bb7b45739adf', 'commit_utc': '2026-11-21T12:50:23Z', 'kod': [{'yol': 'KART_TUR1.py', 'sha256': '334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b'}, {'yol': 'CETVEL2.py', 'sha256': '2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6'}], 'kontrol': True, 'bagimli': 16}.
Yeniden üretim (K11): TUTTU [{'hucre': 'KT01 ABD R15 acik', 'n': 8568, 'fark': -0.0018016196057328976, 'sira': 0.49553144909154473, 'esit': True}, {'hucre': 'KT08 AVR R30 acik', 'n': 1366, 'fark': 0.004191942747841824, 'sira': 0.5129707104271153, 'esit': True}].
Prefix (K2): Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

## Kart etiketleri

| Kart | Etiket | Neden | BH p |
|---|---|---|---|
| KT00 | KONTROL GÖRMEDİ | R15: ABD FARK -0.22 boot [-1.91; +1.45] n 954 T+ False, AVR FARK -0.24 boot [-1.59; +0.93] n 359 T+ False; R30: ABD FARK -0.30 boot [-2.16; +1.80] n 502 T+ False, AVR FARK -0.71 boot [-2.79; +1.21] n 210 T+ False | - |
| KT01 | BİLGİ (ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)) | ABD R15 FARK -0.11 [-0.55; +0.23]; AVR R15 FARK -0.17 [-0.82; +0.54]; ABD R30 FARK +0.23 [-0.29; +0.81]; AVR R30 FARK +0.26 [-0.57; +0.88] | - |
| KT02 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 107 güç 0.35; AVR R15 n 12 güç 0.08; ABD R30 n 106 güç 0.13; AVR R30 n 12 güç 0.06 | - |
| KT03 | BİLGİ (ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)) | ABD R15 FARK -0.10 [-0.58; +0.25]; AVR R15 FARK -0.08 [-0.86; +0.63]; ABD R30 FARK +0.07 [-0.41; +0.67]; AVR R30 FARK +0.33 [-0.13; +0.82] | - |
| KT04 | BİLGİ (ÖLÇÜLEMEDİ) | AVR R15 plasebo kapısı düştü (ort -0.01 puan, pay 0.08); ABD R30 n 649 güç 0.63; AVR R30 n 274 güç 0.72 | - |
| KT05 | BİLGİ (ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)) | ABD R15 FARK -0.13 [-0.58; +0.22]; AVR R15 FARK -0.16 [-0.82; +0.49]; ABD R30 FARK +0.21 [-0.28; +0.78]; AVR R30 FARK +0.27 [-0.52; +0.92] | - |
| KT06 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 763 güç 0.71 | - |
| KT07 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 39 güç 0.15; AVR R15 n 8 güç 0.07; ABD R30 n 38 güç 0.07; AVR R30 n 8 güç 0.05 | - |
| KT08 | BİLGİ (ÖLÇÜLEMEDİ) | AVR R15 n 84 güç 0.40; ABD R30 n 284 güç 0.30; AVR R30 n 53 güç 0.17 | - |
| KT09 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 19 güç 0.09; AVR R15 n 2 güç 0.04; ABD R30 n 19 güç 0.05; AVR R30 n 2 güç 0.04 | - |
| KT10 | BİLGİ (ÖLÇÜLEMEDİ (KT00 görmedi: cetvel / ufuk yetersiz)) | ABD R15 FARK -0.22 [-0.54; +0.08]; ABD R30 FARK -0.23 [-1.10; +0.43] | - |

## Huni (olay sayıları; getirisiz)

```
{
 "ABD": {
  "Y1": {
   "sinyal": 27004,
   "girdi": 27004,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 4,
   "giris_gec": 0,
   "likidite_alt20": 3442,
   "bolunme_gecmis": 40,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 3484,
   "tekil": 13268,
   "y1_olay": 10248,
   "F_KT02": 454,
   "F_KT03": 8972,
   "F_KT04": 4569,
   "F_KT05": 9793,
   "F_KT06": 5790,
   "F_KT07": 190,
   "sure_sn": 91.8
  },
  "D9": {
   "durum": 606184,
   "c": 275584,
   "sure_sn": 37.8
  },
  "MOM": {
   "sinyal": 95634,
   "ana": 15290,
   "U": 7683,
   "A": 7607,
   "son_tarih": "2023-08-31",
   "pk": {
    "girdi": 95634,
    "olay_havuz": 76456,
    "U": 7683,
    "A": 7607,
    "ana": 15290
   }
  },
  "BOFA": {
   "hisse": 1374,
   "kurulum": 571,
   "son": "2023-09-29"
  },
  "DS": {
   "girdi": 221979,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 187,
   "giris_gec": 0,
   "likidite_alt20": 51278,
   "bolunme_gecmis": 4122,
   "evren_once": 0,
   "gecmis_eksik": 5,
   "havuz_az": 0,
   "havuz_disi": 55405,
   "tekil": 0,
   "ds_gun": 221979,
   "havuz_gun": 166387,
   "ana": 16051,
   "F_KT08": 5465,
   "sure_sn": 82.1
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 15290,
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
    "olcum_r15": 15290,
    "kova_yok": 0,
    "donem": {
     "acik": 13367,
     "birikimli": 1923
    }
   },
   "MOM|30": {
    "girdi": 15290,
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
    "tekil": 6240,
    "olcum_r15": 8917,
    "kova_yok": 0,
    "donem": {
     "acik": 7899,
     "birikimli": 1151
    }
   },
   "MOM|45": {
    "girdi": 15290,
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
    "tekil": 8443,
    "olcum_r15": 6664,
    "kova_yok": 0,
    "donem": {
     "acik": 5979,
     "birikimli": 868
    }
   },
   "Y1|15": {
    "girdi": 10248,
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
    "olcum_r15": 10200,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1562
    }
   },
   "Y1|30": {
    "girdi": 10248,
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
    "olcum_r15": 10119,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1562
    }
   },
   "Y1|45": {
    "girdi": 10248,
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
    "olcum_r15": 10053,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1562
    }
   },
   "DS|15": {
    "girdi": 16051,
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
    "olcum_r15": 15888,
    "kova_yok": 0,
    "donem": {
     "acik": 14061,
     "birikimli": 1749,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 16051,
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
    "tekil": 6543,
    "olcum_r15": 9342,
    "kova_yok": 0,
    "donem": {
     "acik": 8320,
     "birikimli": 1046,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 16051,
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
    "tekil": 8725,
    "olcum_r15": 7133,
    "kova_yok": 0,
    "donem": {
     "acik": 6400,
     "birikimli": 784,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 571,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 347,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 374,
    "tekil": 0,
    "olcum_r15": 186,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 20
    }
   },
   "BOFA|30": {
    "girdi": 571,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 347,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 374,
    "tekil": 0,
    "olcum_r15": 186,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 20
    }
   },
   "BOFA|45": {
    "girdi": 571,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 10,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 347,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 374,
    "tekil": 0,
    "olcum_r15": 184,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 20
    }
   },
   "D9|15": {
    "girdi": 275584,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 124,
    "giris_gec": 25,
    "likidite_alt20": 61906,
    "bolunme_gecmis": 2363,
    "evren_once": 0,
    "gecmis_eksik": 743,
    "havuz_az": 0,
    "havuz_disi": 65012,
    "tekil": 188878,
    "olcum_r15": 21414,
    "kova_yok": 560,
    "donem": {
     "acik": 18014,
     "birikimli": 3047,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 275584,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 124,
    "giris_gec": 25,
    "likidite_alt20": 61906,
    "bolunme_gecmis": 2363,
    "evren_once": 0,
    "gecmis_eksik": 743,
    "havuz_az": 0,
    "havuz_disi": 65012,
    "tekil": 196987,
    "olcum_r15": 13215,
    "kova_yok": 375,
    "donem": {
     "acik": 11241,
     "birikimli": 1873,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 275584,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 124,
    "giris_gec": 25,
    "likidite_alt20": 61906,
    "bolunme_gecmis": 2363,
    "evren_once": 0,
    "gecmis_eksik": 743,
    "havuz_az": 0,
    "havuz_disi": 65012,
    "tekil": 199809,
    "olcum_r15": 10270,
    "kova_yok": 347,
    "donem": {
     "acik": 8853,
     "birikimli": 1493,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 14100,
   "girdi": 14100,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 6,
   "giris_gec": 0,
   "likidite_alt20": 2149,
   "bolunme_gecmis": 6,
   "evren_once": 0,
   "gecmis_eksik": 7,
   "havuz_az": 0,
   "havuz_disi": 2162,
   "tekil": 6787,
   "y1_olay": 5145,
   "F_KT02": 101,
   "F_KT03": 4461,
   "F_KT04": 2538,
   "F_KT05": 4798,
   "F_KT06": 3189,
   "F_KT07": 44,
   "sure_sn": 45.2
  },
  "MOM": {
   "sinyal": 48326,
   "ana": 7643,
   "U": 3862,
   "A": 3781,
   "son_tarih": "2023-08-31",
   "pk": {
    "girdi": 48326,
    "olay_havuz": 38231,
    "U": 3862,
    "A": 3781,
    "ana": 7643
   }
  },
  "BOFA": {
   "hisse": 576,
   "kurulum": 34,
   "son": "2023-09-29"
  },
  "DS": {
   "girdi": 54446,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 28,
   "giris_gec": 0,
   "likidite_alt20": 2921,
   "bolunme_gecmis": 873,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3812,
   "tekil": 0,
   "ds_gun": 54446,
   "havuz_gun": 50606,
   "ana": 5084,
   "F_KT08": 2073,
   "sure_sn": 30.1
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 7643,
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
    "olcum_r15": 7643,
    "kova_yok": 0,
    "donem": {
     "acik": 6832,
     "birikimli": 811
    }
   },
   "MOM|30": {
    "girdi": 7643,
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
    "tekil": 2981,
    "olcum_r15": 4598,
    "kova_yok": 0,
    "donem": {
     "acik": 4144,
     "birikimli": 518
    }
   },
   "MOM|45": {
    "girdi": 7643,
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
    "tekil": 4006,
    "olcum_r15": 3546,
    "kova_yok": 0,
    "donem": {
     "acik": 3230,
     "birikimli": 407
    }
   },
   "Y1|15": {
    "girdi": 5145,
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
    "olcum_r15": 5106,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 649
    }
   },
   "Y1|30": {
    "girdi": 5145,
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
    "olcum_r15": 5087,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 649
    }
   },
   "Y1|45": {
    "girdi": 5145,
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
    "olcum_r15": 5069,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 649
    }
   },
   "DS|15": {
    "girdi": 5084,
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
    "olcum_r15": 5051,
    "kova_yok": 0,
    "donem": {
     "acik": 4562,
     "birikimli": 263,
     "dis": 259
    }
   },
   "DS|30": {
    "girdi": 5084,
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
    "tekil": 2016,
    "olcum_r15": 3027,
    "kova_yok": 0,
    "donem": {
     "acik": 2741,
     "birikimli": 164,
     "dis": 163
    }
   },
   "DS|45": {
    "girdi": 5084,
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
    "tekil": 2686,
    "olcum_r15": 2357,
    "kova_yok": 0,
    "donem": {
     "acik": 2148,
     "dis": 129,
     "birikimli": 121
    }
   },
   "BOFA|15": {
    "girdi": 34,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "
```

## Hücre: acik

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 6718 | 6024 | 694 | 0 | +0.40 [-0.37; +1.14] | -0.13 | 0.502 | +0.04 | 0.1604 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT00 | + | ABD | 30 | 3948 | 3699 | 249 | 0 | +0.72 [-0.17; +1.62] | -0.68 | 0.501 | +0.30 | 0.0710 | 1.00 | -0.00 / 0.01 / True | False / False |
| KT00 | + | ABD | 45 | 2974 | 2799 | 175 | 0 | +0.95 [-0.10; +1.99] | -1.03 | 0.504 | +0.52 | 0.0554 | 0.99 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 3452 | 2788 | 664 | 0 | +0.07 [-0.45; +0.57] | -0.12 | 0.499 | -0.11 | 0.3821 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT00 | + | AVR | 30 | 2104 | 1763 | 341 | 0 | -0.32 [-1.15; +0.50] | -0.63 | 0.486 | -0.68 | 0.7649 | 1.00 | -0.02 / 0.03 / True | False / False |
| KT00 | + | AVR | 45 | 1640 | 1375 | 265 | 0 | +0.40 [-0.61; +1.40] | +0.09 | 0.506 | -0.02 | 0.2191 | 1.00 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 8686 | 8568 | 118 | 0 | -0.18 [-0.42; +0.06] | -0.18 | 0.496 | -0.28 | 0.9264 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 30 | 8686 | 8568 | 118 | 0 | -0.30 [-0.64; +0.01] | -0.31 | 0.493 | -0.43 | 0.9505 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 45 | 8686 | 8568 | 118 | 0 | -0.24 [-0.66; +0.15] | -0.40 | 0.497 | -0.38 | 0.8731 | 1.00 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 4496 | 4217 | 279 | 0 | -0.03 [-0.24; +0.20] | -0.16 | 0.495 | -0.15 | 0.6160 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 4496 | 4217 | 279 | 0 | -0.15 [-0.47; +0.19] | -0.18 | 0.495 | -0.32 | 0.7917 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | AVR | 45 | 4496 | 4217 | 279 | 0 | -0.14 [-0.54; +0.26] | -0.36 | 0.494 | -0.33 | 0.7569 | 1.00 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 2588 | 2188 | 400 | 0 | -0.80 [-1.33; -0.29] | -2.81 | 0.451 | -1.07 | 0.9975 | 1.00 | -0.01 / 0.02 / True | False / True |
| KT01 | + | BIST | 30 | 2588 | 2188 | 400 | 0 | -0.76 [-1.70; +0.28] | -3.42 | 0.475 | -1.23 | 0.9194 | 1.00 | -0.01 / 0.02 / True | False / False |
| KT01 | + | BIST | 45 | 2588 | 2188 | 400 | 0 | -0.72 [-2.02; +0.57] | -4.30 | 0.475 | -1.27 | 0.8585 | 0.93 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 346 | 338 | 8 | 0 | -0.15 [-1.58; +1.30] | +0.13 | 0.505 | -0.67 | 0.5776 | 0.82 | -0.04 / 0.04 / True | False / False |
| KT02 | + | ABD | 30 | 346 | 338 | 8 | 0 | -1.41 [-6.70; +1.70] | +0.30 | 0.514 | -3.14 | 0.6881 | 0.35 | +0.07 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 346 | 338 | 8 | 0 | -2.41 [-8.57; +1.27] | -0.26 | 0.499 | -4.25 | 0.8065 | 0.24 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 89 | 78 | 11 | 0 | +0.49 [-1.50; +2.59] | +1.56 | 0.537 | -0.62 | 0.3265 | 0.37 | -0.04 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 89 | 78 | 11 | 0 | +0.66 [-1.57; +3.14] | +1.05 | 0.517 | -0.73 | 0.2936 | 0.24 | -0.05 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 89 | 78 | 11 | 0 | -0.34 [-3.74; +3.18] | -0.07 | 0.510 | -2.44 | 0.5774 | 0.20 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 238 | 205 | 33 | 0 | -0.23 [-1.74; +1.62] | -2.69 | 0.445 | -1.16 | 0.5962 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 238 | 205 | 33 | 0 | +0.02 [-2.21; +2.93] | -2.14 | 0.489 | -1.41 | 0.4923 | 0.28 | -0.04 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 238 | 205 | 33 | 0 | +1.02 [-1.90; +4.20] | -2.80 | 0.500 | -0.70 | 0.2563 | 0.16 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 7614 | 7512 | 102 | 0 | -0.21 [-0.44; +0.02] | -0.21 | 0.495 | -0.29 | 0.9531 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 30 | 7614 | 7512 | 102 | 0 | -0.29 [-0.65; +0.07] | -0.35 | 0.493 | -0.43 | 0.9403 | 1.00 | -0.14 / 0.02 / True | False / False |
| KT03 | + | ABD | 45 | 7614 | 7512 | 102 | 0 | -0.25 [-0.70; +0.17] | -0.48 | 0.496 | -0.38 | 0.8543 | 1.00 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 3910 | 3661 | 249 | 0 | +0.01 [-0.20; +0.25] | -0.15 | 0.496 | -0.10 | 0.4511 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT03 | + | AVR | 30 | 3910 | 3661 | 249 | 0 | -0.11 [-0.45; +0.24] | -0.21 | 0.495 | -0.31 | 0.7244 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT03 | + | AVR | 45 | 3910 | 3661 | 249 | 0 | -0.11 [-0.51; +0.31] | -0.44 | 0.494 | -0.31 | 0.7051 | 1.00 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 2379 | 2013 | 366 | 0 | -0.64 [-1.14; -0.08] | -2.83 | 0.452 | -0.93 | 0.9816 | 1.00 | +0.02 / 0.02 / True | False / True |
| KT03 | + | BIST | 30 | 2379 | 2013 | 366 | 0 | -0.72 [-1.75; +0.34] | -3.48 | 0.475 | -1.23 | 0.8973 | 0.99 | +0.02 / 0.03 / True | False / False |
| KT03 | + | BIST | 45 | 2379 | 2013 | 366 | 0 | -0.52 [-1.82; +0.82] | -4.16 | 0.477 | -1.04 | 0.7668 | 0.91 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 3823 | 3773 | 50 | 0 | -0.21 [-0.51; +0.14] | -0.10 | 0.497 | -0.37 | 0.8897 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT04 | + | ABD | 30 | 3823 | 3773 | 50 | 0 | -0.50 [-0.96; +0.01] | -0.32 | 0.492 | -0.66 | 0.9706 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT04 | + | ABD | 45 | 3823 | 3773 | 50 | 0 | -0.64 [-1.23; -0.09] | -0.45 | 0.493 | -0.84 | 0.9849 | 1.00 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 2208 | 2080 | 128 | 0 | -0.05 [-0.37; +0.31] | -0.19 | 0.490 | -0.22 | 0.6109 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT04 | + | AVR | 30 | 2208 | 2080 | 128 | 0 | -0.04 [-0.50; +0.46] | -0.21 | 0.495 | -0.28 | 0.5545 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT04 | + | AVR | 45 | 2208 | 2080 | 128 | 0 | -0.06 [-0.59; +0.47] | -0.29 | 0.496 | -0.30 | 0.5884 | 1.00 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 1572 | 1348 | 224 | 0 | -0.85 [-1.53; -0.15] | -2.93 | 0.450 | -1.18 | 0.9890 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT04 | + | BIST | 30 | 1572 | 1348 | 224 | 0 | -0.68 [-1.74; +0.52] | -3.58 | 0.476 | -1.31 | 0.8719 | 0.96 | +0.01 / 0.03 / True | False / False |
| KT04 | + | BIST | 45 | 1572 | 1348 | 224 | 0 | -0.70 [-2.11; +0.83] | -4.30 | 0.471 | -1.30 | 0.8162 | 0.76 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 8245 | 8139 | 106 | 0 | -0.20 [-0.44; +0.04] | -0.19 | 0.495 | -0.30 | 0.9312 | 1.00 | -0.01 / 0.05 / True | False / False |
| KT05 | + | ABD | 30 | 8245 | 8139 | 106 | 0 | -0.36 [-0.71; +0.00] | -0.35 | 0.492 | -0.50 | 0.9733 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT05 | + | ABD | 45 | 8245 | 8139 | 106 | 0 | -0.33 [-0.76; +0.07] | -0.51 | 0.495 | -0.47 | 0.9340 | 1.00 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 4160 | 3909 | 251 | 0 | -0.01 [-0.22; +0.23] | -0.13 | 0.497 | -0.13 | 0.5263 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 30 | 4160 | 3909 | 251 | 0 | -0.13 [-0.47; +0.27] | -0.18 | 0.496 | -0.32 | 0.7555 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 45 | 4160 | 3909 | 251 | 0 | -0.11 [-0.53; +0.32] | -0.34 | 0.496 | -0.32 | 0.6829 | 1.00 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 2535 | 2141 | 394 | 0 | -0.82 [-1.30; -0.27] | -2.77 | 0.451 | -1.08 | 0.9983 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT05 | + | BIST | 30 | 2535 | 2141 | 394 | 0 | -0.76 [-1.86; +0.34] | -3.48 | 0.475 | -1.24 | 0.9206 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT05 | + | BIST | 45 | 2535 | 2141 | 394 | 0 | -0.74 [-2.00; +0.60] | -4.30 | 0.475 | -1.31 | 0.8611 | 0.93 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 4953 | 4885 | 68 | 0 | -0.02 [-0.27; +0.25] | -0.09 | 0.499 | -0.14 | 0.5541 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 4953 | 4885 | 68 | 0 | -0.10 [-0.45; +0.26] | -0.24 | 0.494 | -0.26 | 0.7018 | 1.00 | -0.04 / 0.03 / True | False / False |
| KT06 | + | ABD | 45 | 4953 | 4885 | 68 | 0 | -0.05 [-0.48; +0.40] | -0.29 | 0.498 | -0.23 | 0.5758 | 1.00 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 2801 | 2629 | 172 | 0 | -0.03 [-0.28; +0.23] | -0.14 | 0.496 | -0.15 | 0.5993 | 1.00 | -0.01 / 0.03 / True | False / False |
| KT06 | + | AVR | 30 | 2801 | 2629 | 172 | 0 | -0.18 [-0.59; +0.25] | -0.24 | 0.494 | -0.39 | 0.7925 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 2801 | 2629 | 172 | 0 | -0.10 [-0.56; +0.38] | -0.31 | 0.496 | -0.32 | 0.6670 | 1.00 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 1626 | 1381 | 245 | 0 | -1.04 [-1.67; -0.32] | -2.86 | 0.443 | -1.36 | 0.9983 | 1.00 | +0.05 / 0.02 / True | False / True |
| KT06 | + | BIST | 30 | 1626 | 1381 | 245 | 0 | -1.38 [-2.47; -0.12] | -3.68 | 0.470 | -2.03 | 0.9851 | 0.96 | +0.05 / 0.03 / True | False / True |
| KT06 | + | BIST | 45 | 1626 | 1381 | 245 | 0 | -1.51 [-2.97; -0.08] | -4.13 | 0.467 | -2.14 | 0.9801 | 0.77 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 151 | 146 | 5 | 0 | -0.45 [-2.34; +1.39] | -0.57 | 0.486 | -1.32 | 0.6823 | 0.45 | -0.06 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 151 | 146 | 5 | 0 | -3.53 [-14.50; +2.14] | +0.32 | 0.510 | -6.01 | 0.6932 | 0.16 | -0.34 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 151 | 146 | 5 | 0 | -6.14 [-19.32; +0.85] | -0.40 | 0.486 | -9.67 | 0.9059 | 0.12 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 36 | 30 | 6 | 0 | +0.36 [-3.13; +4.02] | +0.86 | 0.518 | -1.53 | 0.4217 | 0.16 | +0.01 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 36 | 30 | 6 | 0 | -0.33 [-3.81; +2.84] | +0.77 | 0.517 | -2.00 | 0.5699 | 0.11 | +0.02 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 36 | 30 | 6 | 0 | +1.24 [-3.82; +6.11] | +1.30 | 0.538 | -2.45 | 0.3352 | 0.09 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 129 | 108 | 21 | 0 | -0.16 [-2.00; +2.28] | -2.69 | 0.454 | -1.56 | 0.5619 | 0.46 | +0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 129 | 108 | 21 | 0 | -0.55 [-3.23; +2.72] | -2.29 | 0.496 | -2.45 | 0.6379 | 0.16 | +0.13 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 129 | 108 | 21 | 0 | +0.54 [-3.11; +5.11] | -3.51 | 0.493 | -2.49 | 0.4119 | 0.10 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 4836 | 4791 | 45 | 0 | +0.05 [-0.43; +0.62] | -0.02 | 0.509 | -0.23 | 0.5693 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT08 | - | ABD | 30 | 3431 | 3395 | 36 | 0 | -0.41 [-1.61; +0.87] | -0.83 | 0.500 | -0.74 | 0.4235 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT08 | - | ABD | 45 | 2947 | 2917 | 30 | 0 | -1.16 [-3.51; +1.32] | -1.81 | 0.496 | -1.67 | 0.4330 | 0.99 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 1838 | 1784 | 54 | 0 | +0.29 [-0.42; +1.11] | +0.35 | 0.515 | +0.05 | 0.7364 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | AVR | 30 | 1406 | 1366 | 40 | 0 | +0.42 [-0.71; +1.89] | +0.32 | 0.513 | +0.06 | 0.6858 | 1.00 | +0.04 / 0.03 / True | False / False |
| KT08 | - | AVR | 45 | 1266 | 1235 | 31 | 0 | +0.32 [-0.80; +1.94] | +0.22 | 0.510 | -0.29 | 0.6629 | 1.00 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 721 | 653 | 68 | 0 | -0.73 [-1.85; +0.51] | -1.50 | 0.480 | -1.40 | 0.1229 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | BIST | 30 | 475 | 436 | 39 | 0 | -2.08 [-5.69; +0.94] | -2.89 | 0.469 | -3.28 | 0.1807 | 0.53 | +0.03 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 400 | 364 | 36 | 0 | -3.83 [-9.60; +0.43] | -3.31 | 0.471 | -5.70 | 0.0979 | 0.26 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 167 | 163 | 4 | 0 | +4.70 [-1.09; +9.97] | +1.44 | 0.540 | +0.06 | 0.0876 | 0.50 | +0.00 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 167 | 163 | 4 | 0 | +7.12 [-1.31; +16.24] | +1.18 | 0.526 | +0.74 | 0.0857 | 0.18 | +0.02 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 167 | 163 | 4 | 0 | +9.62 [-6.34; +31.68] | +0.58 | 0.512 | -4.95 | 0.3318 | 0.13 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 20 | 20 | 0 | 0 | +3.68 [-10.28; +19.16] | -5.40 | 0.447 | -6.03 | 0.3090 | 0.12 | +0.10 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 20 | 20 | 0 | 0 | +5.27 [-6.04; +18.56] | +2.27 | 0.542 | -2.84 | 0.1962 | 0.09 | +0.24 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 20 | 20 | 0 | 0 | +3.67 [-10.09; +18.76] | -2.79 | 0.510 | -5.05 | 0.3000 | 0.07 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 18014 | 17260 | 754 | 0 | -0.02 [-0.23; +0.20] | -0.33 | 0.496 | -0.12 | 0.5743 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT10 | + | ABD | 30 | 11241 | 10773 | 468 | 0 | -0.12 [-0.59; +0.39] | -0.67 | 0.492 | -0.33 | 0.6799 | 1.00 | +0.00 / 0.01 / True | False / False |
| KT10 | + | ABD | 45 | 8853 | 8495 | 358 | 0 | -0.04 [-0.61; +0.58] | -0.70 | 0.500 | -0.30 | 0.5440 | 1.00 | - / - / False | False / False |

## Hücre: birikimli

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 965 | 954 | 11 | 0 | -0.22 [-1.91; +1.45] | -0.92 | 0.485 | -1.74 | 0.5969 | 1.00 | +0.02 / 0.06 / True | False / False |
| KT00 | + | ABD | 30 | 569 | 502 | 2 | 65 | -0.30 [-2.16; +1.80] | -1.94 | 0.493 | -2.18 | 0.5977 | 0.51 | -0.04 / 0.00 / True | False / False |
| KT00 | + | ABD | 45 | 424 | 341 | 0 | 83 | -1.26 [-3.24; +0.71] | -3.24 | 0.470 | -3.42 | 0.8706 | 0.24 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 410 | 359 | 51 | 0 | -0.24 [-1.59; +0.93] | -0.02 | 0.494 | -1.22 | 0.6401 | 0.97 | -0.02 / 0.04 / True | False / False |
| KT00 | + | AVR | 30 | 262 | 210 | 22 | 30 | -0.71 [-2.79; +1.21] | +0.10 | 0.499 | -2.45 | 0.7438 | 0.59 | +0.04 / 0.00 / True | False / False |
| KT00 | + | AVR | 45 | 207 | 158 | 11 | 38 | -2.06 [-5.22; +1.11] | -1.31 | 0.448 | -4.71 | 0.8196 | 0.39 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 1562 | 1502 | 12 | 48 | -0.11 [-0.55; +0.23] | -0.32 | 0.500 | -0.45 | 0.6480 | 1.00 | +0.01 / 0.06 / True | False / False |
| KT01 | + | ABD | 30 | 1562 | 1421 | 12 | 129 | +0.23 [-0.29; +0.81] | -0.42 | 0.508 | -0.31 | 0.2266 | 0.94 | +0.00 / 0.05 / True | False / False |
| KT01 | + | ABD | 45 | 1562 | 1355 | 12 | 195 | -0.24 [-0.91; +0.50] | -0.76 | 0.500 | -0.96 | 0.7462 | 0.81 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 649 | 576 | 34 | 39 | -0.17 [-0.82; +0.54] | -0.00 | 0.502 | -0.78 | 0.6594 | 1.00 | -0.02 / 0.06 / True | False / False |
| KT01 | + | AVR | 30 | 649 | 561 | 30 | 58 | +0.26 [-0.57; +0.88] | +0.28 | 0.515 | -0.21 | 0.2618 | 0.97 | -0.03 / 0.04 / True | False / False |
| KT01 | + | AVR | 45 | 649 | 543 | 30 | 76 | -0.00 [-0.63; +0.47] | -0.11 | 0.504 | -0.64 | 0.5218 | 0.93 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 276 | 208 | 44 | 24 | -1.48 [-3.54; -0.24] | -1.99 | 0.470 | -3.17 | 0.9393 | 0.78 | -0.18 / 0.00 / True | False / False |
| KT01 | + | BIST | 30 | 276 | 184 | 43 | 49 | -2.06 [-3.15; -0.77] | -4.05 | 0.476 | -3.06 | 0.9844 | 0.25 | -0.35 / 0.00 / True | False / False |
| KT01 | + | BIST | 45 | 276 | 149 | 33 | 94 | -4.73 [-10.94; +0.14] | -7.07 | 0.463 | -11.17 | 0.9700 | 0.13 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 108 | 107 | 0 | 1 | +0.71 [-0.18; +1.72] | -0.05 | 0.518 | -0.07 | 0.1015 | 0.35 | +0.04 / 0.00 / True | False / False |
| KT02 | + | ABD | 30 | 108 | 106 | 0 | 2 | +2.45 [+0.86; +3.64] | +1.92 | 0.571 | +0.70 | 0.0297 | 0.13 | +0.08 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 108 | 105 | 0 | 3 | -0.23 [-1.48; +0.65] | -0.58 | 0.513 | -1.44 | 0.6703 | 0.09 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 12 | 12 | 0 | 0 | +3.91 [-3.25; +9.53] | +5.50 | 0.674 | -2.91 | 0.1655 | 0.08 | +0.19 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 12 | 12 | 0 | 0 | +6.22 [+0.60; +14.53] | +3.71 | 0.646 | -0.02 | 0.0737 | 0.06 | +0.28 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 12 | 12 | 0 | 0 | +6.41 [-2.26; +17.27] | +4.85 | 0.609 | -2.70 | 0.1227 | 0.06 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 77 | 75 | 2 | 0 | -0.80 [-6.90; +0.19] | -1.62 | 0.491 | -6.18 | 0.8427 | 0.32 | +0.22 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 77 | 75 | 2 | 0 | -1.96 [-6.08; -1.23] | -5.31 | 0.463 | -9.02 | 1.0000 | 0.13 | +0.17 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 77 | 75 | 0 | 2 | -2.21 [-11.08; +2.71] | -5.25 | 0.461 | -5.68 | 0.7439 | 0.08 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 1358 | 1306 | 8 | 44 | -0.10 [-0.58; +0.25] | -0.33 | 0.500 | -0.43 | 0.6144 | 1.00 | -0.02 / 0.03 / True | False / False |
| KT03 | + | ABD | 30 | 1358 | 1234 | 8 | 116 | +0.07 [-0.41; +0.67] | -0.48 | 0.505 | -0.37 | 0.4118 | 0.91 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 45 | 1358 | 1179 | 8 | 171 | -0.37 [-0.91; +0.41] | -0.93 | 0.497 | -1.11 | 0.7965 | 0.75 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 551 | 490 | 28 | 33 | -0.08 [-0.86; +0.63] | -0.05 | 0.502 | -0.79 | 0.5662 | 0.99 | -0.02 / 0.06 / True | False / False |
| KT03 | + | AVR | 30 | 551 | 475 | 25 | 51 | +0.33 [-0.13; +0.82] | +0.27 | 0.515 | -0.09 | 0.1457 | 0.93 | -0.00 / 0.06 / True | False / False |
| KT03 | + | AVR | 45 | 551 | 459 | 25 | 67 | +0.10 [-0.42; +0.54] | +0.06 | 0.506 | -0.40 | 0.3596 | 0.88 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 253 | 189 | 41 | 23 | -1.40 [-3.71; -0.15] | -2.56 | 0.468 | -2.99 | 0.9671 | 0.73 | -0.00 / 0.00 / True | False / False |
| KT03 | + | BIST | 30 | 253 | 167 | 40 | 46 | -1.60 [-2.80; -0.28] | -3.97 | 0.478 | -2.74 | 0.9743 | 0.23 | -0.03 / 0.00 / True | False / False |
| KT03 | + | BIST | 45 | 253 | 137 | 31 | 85 | -4.63 [-10.97; -0.94] | -6.93 | 0.462 | -10.93 | 0.9719 | 0.12 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 746 | 707 | 4 | 35 | -0.28 [-1.08; +0.60] | -0.41 | 0.495 | -1.02 | 0.7069 | 0.99 | -0.00 / 0.03 / True | False / False |
| KT04 | + | ABD | 30 | 746 | 649 | 4 | 93 | -0.30 [-1.19; +0.98] | -0.64 | 0.500 | -1.23 | 0.6754 | 0.63 | -0.00 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 746 | 601 | 4 | 141 | -0.74 [-2.14; +1.12] | -1.34 | 0.488 | -2.08 | 0.7834 | 0.42 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 330 | 283 | 16 | 31 | +0.06 [-0.77; +0.85] | +0.10 | 0.506 | -0.47 | 0.4381 | 0.91 | -0.01 / 0.08 / False | False / False |
| KT04 | + | AVR | 30 | 330 | 274 | 13 | 43 | +0.32 [-0.22; +0.97] | +0.27 | 0.518 | -0.26 | 0.1878 | 0.72 | -0.03 / 0.00 / True | False / False |
| KT04 | + | AVR | 45 | 330 | 266 | 13 | 51 | -0.16 [-1.31; +1.50] | -0.26 | 0.498 | -1.28 | 0.6070 | 0.63 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 210 | 160 | 30 | 20 | -1.32 [-4.00; +0.21] | -1.89 | 0.480 | -3.65 | 0.8930 | 0.65 | -0.01 / 0.00 / True | False / False |
| KT04 | + | BIST | 30 | 210 | 143 | 29 | 38 | -1.50 [-3.10; +0.45] | -4.13 | 0.478 | -2.73 | 0.9222 | 0.21 | -0.00 / 0.00 / True | False / False |
| KT04 | + | BIST | 45 | 210 | 120 | 22 | 68 | -3.30 [-8.42; -0.30] | -6.05 | 0.471 | -8.53 | 0.9672 | 0.11 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 1548 | 1488 | 12 | 48 | -0.13 [-0.58; +0.22] | -0.34 | 0.499 | -0.46 | 0.6741 | 1.00 | -0.04 / 0.03 / True | False / False |
| KT05 | + | ABD | 30 | 1548 | 1407 | 12 | 129 | +0.21 [-0.28; +0.78] | -0.49 | 0.508 | -0.29 | 0.2416 | 0.94 | -0.05 / 0.06 / True | False / False |
| KT05 | + | ABD | 45 | 1548 | 1342 | 12 | 194 | -0.28 [-0.81; +0.42] | -0.82 | 0.499 | -0.96 | 0.7672 | 0.81 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 638 | 569 | 31 | 38 | -0.16 [-0.82; +0.49] | -0.01 | 0.502 | -0.78 | 0.6614 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT05 | + | AVR | 30 | 638 | 555 | 27 | 56 | +0.27 [-0.52; +0.92] | +0.27 | 0.515 | -0.26 | 0.2602 | 0.97 | +0.02 / 0.04 / True | False / False |
| KT05 | + | AVR | 45 | 638 | 537 | 27 | 74 | +0.00 [-0.68; +0.53] | -0.19 | 0.503 | -0.69 | 0.4964 | 0.93 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 274 | 206 | 44 | 24 | -1.58 [-3.61; -0.44] | -2.14 | 0.467 | -3.17 | 0.9761 | 0.78 | -0.16 / 0.00 / True | False / False |
| KT05 | + | BIST | 30 | 274 | 182 | 43 | 49 | -2.22 [-3.23; -0.90] | -4.23 | 0.473 | -3.37 | 0.9846 | 0.25 | -0.28 / 0.00 / True | False / False |
| KT05 | + | BIST | 45 | 274 | 147 | 33 | 94 | -5.10 [-10.89; -0.07] | -7.63 | 0.459 | -11.17 | 0.9703 | 0.13 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 837 | 804 | 3 | 30 | +0.07 [-0.29; +0.39] | -0.26 | 0.506 | -0.18 | 0.3398 | 0.99 | -0.06 / 0.02 / True | False / False |
| KT06 | + | ABD | 30 | 837 | 763 | 3 | 71 | +0.59 [+0.21; +1.08] | -0.24 | 0.513 | +0.23 | 0.0138 | 0.71 | -0.05 / 0.00 / True | False / False |
| KT06 | + | ABD | 45 | 837 | 732 | 3 | 102 | -0.07 [-0.67; +0.56] | -0.62 | 0.503 | -0.76 | 0.5874 | 0.51 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 388 | 343 | 19 | 26 | -0.36 [-0.97; +0.23] | -0.16 | 0.486 | -0.86 | 0.8155 | 0.96 | +0.01 / 0.07 / True | False / False |
| KT06 | + | AVR | 30 | 388 | 336 | 17 | 35 | +0.29 [-0.39; +0.76] | +0.36 | 0.521 | -0.33 | 0.2229 | 0.81 | -0.01 / 0.00 / True | False / False |
| KT06 | + | AVR | 45 | 388 | 326 | 18 | 44 | +0.05 [-0.62; +0.53] | -0.15 | 0.500 | -0.70 | 0.4464 | 0.73 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 136 | 99 | 28 | 9 | -0.99 [-3.53; +0.13] | -1.50 | 0.495 | -2.95 | 0.9135 | 0.42 | +0.06 / 0.00 / True | False / False |
| KT06 | + | BIST | 30 | 136 | 89 | 27 | 20 | -0.92 [-2.93; +1.66] | -3.30 | 0.493 | -2.40 | 0.7947 | 0.14 | -0.03 / 0.00 / True | False / False |
| KT06 | + | BIST | 45 | 136 | 64 | 18 | 54 | -3.77 [-11.57; +4.15] | -4.74 | 0.488 | -9.55 | 0.8180 | 0.08 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 39 | 39 | 0 | 0 | -0.39 [-3.77; +1.55] | -0.05 | 0.493 | -4.72 | 0.6302 | 0.15 | -0.10 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 39 | 38 | 0 | 1 | -0.33 [-4.08; +2.40] | +1.32 | 0.550 | -4.26 | 0.5920 | 0.07 | -0.01 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 39 | 37 | 0 | 2 | -4.57 [-9.26; -0.79] | -3.35 | 0.465 | -10.02 | 0.9663 | 0.05 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 8 | 8 | 0 | 0 | +0.69 [-6.74; +8.04] | +0.46 | 0.520 | -9.03 | 0.4790 | 0.07 | -0.16 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 8 | 8 | 0 | 0 | +2.60 [-3.27; +10.98] | -1.03 | 0.502 | -1.59 | 0.5030 | 0.05 | -0.24 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 8 | 8 | 0 | 0 | +1.28 [-10.00; +13.51] | -4.38 | 0.460 | -10.94 | 0.4429 | 0.05 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 56 | 56 | 0 | 0 | -0.35 [-7.46; +0.66] | -1.52 | 0.515 | -12.13 | 0.7479 | 0.24 | +0.14 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 56 | 56 | 0 | 0 | -2.06 [-8.45; +1.05] | -5.55 | 0.447 | -19.82 | 0.8768 | 0.10 | +0.26 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 56 | 56 | 0 | 0 | -2.92 [-12.58; -1.95] | -6.05 | 0.444 | -19.70 | 1.0000 | 0.07 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 528 | 442 | 2 | 84 | +0.36 [-1.15; +1.94] | -0.46 | 0.503 | -0.60 | 0.6758 | 0.91 | +0.04 / 0.07 / True | False / False |
| KT08 | - | ABD | 30 | 365 | 284 | 0 | 81 | +0.56 [-1.81; +2.74] | -1.04 | 0.502 | -1.36 | 0.6525 | 0.30 | +0.06 / 0.00 / True | False / False |
| KT08 | - | ABD | 45 | 306 | 218 | 0 | 88 | -0.11 [-1.67; +2.32] | -3.53 | 0.490 | -1.71 | 0.4677 | 0.16 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 104 | 84 | 1 | 19 | +0.67 [-0.88; +2.03] | +0.07 | 0.519 | -0.95 | 0.6678 | 0.40 | -0.06 / 0.00 / True | False / False |
| KT08 | - | AVR | 30 | 78 | 53 | 0 | 25 | -0.61 [-2.24; +0.91] | -0.48 | 0.500 | -2.15 | 0.2374 | 0.17 | -0.01 / 0.00 / True | False / False |
| KT08 | - | AVR | 45 | 70 | 43 | 1 | 26 | +0.04 [-2.42; +2.74] | -0.21 | 0.497 | -2.72 | 0.5350 | 0.12 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 268 | 261 | 6 | 1 | +0.46 [-2.16; +1.28] | -0.06 | 0.526 | -1.21 | 0.6059 | 0.88 | +0.04 / 0.07 / False | False / False |
| KT08 | - | BIST | 30 | 149 | 145 | 3 | 1 | +0.30 [-1.53; +1.53] | -1.33 | 0.530 | -0.24 | 0.6915 | 0.21 | +0.15 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 89 | 86 | 2 | 1 | -0.04 [-3.79; +3.43] | -0.85 | 0.552 | -4.54 | 0.4380 | 0.09 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 20 | 19 | 0 | 1 | -1.61 [-14.12; +8.61] | -1.33 | 0.476 | -13.04 | 0.6192 | 0.09 | +0.14 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 20 | 19 | 0 | 1 | +0.97 [-10.70; +12.01] | -2.93 | 0.468 | -13.36 | 0.4598 | 0.05 | +0.30 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 20 | 17 | 0 | 3 | +12.27 [-20.04; +40.74] | +2.92 | 0.496 | -25.67 | 0.3009 | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 2 | 2 | 0 | 0 | +2.63 [-33.25; +38.52] | +2.63 | 0.500 | - | 0.4993 | 0.04 | -0.65 / 0.00 / False | False / False |
| KT09 | + | AVR | 30 | 2 | 2 | 0 | 0 | +14.10 [-15.94; +44.15] | +14.10 | 0.526 | - | 0.4993 | 0.04 | -0.51 / 0.00 / False | False / False |
| KT09 | + | AVR | 45 | 2 | 2 | 0 | 0 | -13.65 [-40.63; +13.32] | -13.65 | 0.455 | - | 0.7496 | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 3047 | 2895 | 21 | 131 | -0.22 [-0.54; +0.08] | -0.67 | 0.492 | -0.42 | 0.8824 | 1.00 | -0.02 / 0.05 / True | False / False |
| KT10 | + | ABD | 30 | 1873 | 1638 | 14 | 221 | -0.23 [-1.10; +0.43] | -0.97 | 0.495 | -1.07 | 0.7173 | 0.97 | +0.00 / 0.07 / True | False / False |
| KT10 | + | ABD | 45 | 1493 | 1141 | 8 | 344 | -0.76 [-2.50; +0.77] | -2.45 | 0.478 | -2.25 | 0.8073 | 0.73 | - / - / False | False / False |

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
| KT02 | + | ABD | 15 | 68 | 68 | 0 | 0 | +0.85 [+0.18; +2.68] | -0.10 | 0.521 | - | - | 0.23 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 68 | 68 | 0 | 0 | +2.95 [+1.28; +4.66] | +4.97 | 0.598 | - | - | 0.09 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 68 | 68 | 0 | 0 | +0.23 [-0.75; +1.06] | +0.50 | 0.532 | - | - | 0.07 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 7 | 7 | 0 | 0 | +5.97 [-5.59; +11.03] | +7.39 | 0.758 | - | - | 0.06 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 7 | 7 | 0 | 0 | +5.80 [-2.14; +17.45] | +3.77 | 0.626 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 7 | 7 | 0 | 0 | +3.79 [-11.03; +21.22] | +4.69 | 0.587 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 69 | 69 | 0 | 0 | -0.01 [-2.90; +0.42] | -0.78 | 0.528 | - | - | 0.30 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 69 | 69 | 0 | 0 | -1.35 [-1.67; -0.19] | -5.31 | 0.473 | - | - | 0.12 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 69 | 69 | 0 | 0 | -1.27 [-7.28; +4.20] | -5.24 | 0.478 | - | - | 0.08 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 526 | 523 | 3 | 0 | +0.07 [-0.05; +0.22] | -0.41 | 0.506 | - | - | 0.95 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 526 | 523 | 3 | 0 | +0.19 [-0.15; +0.40] | -0.36 | 0.517 | - | - | 0.52 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 526 | 523 | 3 | 0 | -0.10 [-1.13; +0.50] | -0.49 | 0.512 | - | - | 0.37 | - / - / False | False / False |
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
| KT05 | + | ABD | 45 | 597 | 592 | 5 | 0 | +0.03 [-0.88; +0.50] | -0.26 | 0.517 | - | - | 0.42 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 200 | 183 | 17 | 0 | +0.30 [-0.66; +0.78] | +0.21 | 0.518 | - | - | 0.74 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 200 | 183 | 17 | 0 | +0.46 [-0.27; +1.18] | +0.10 | 0.519 | - | - | 0.53 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 200 | 183 | 17 | 0 | +0.10 [-0.82; +0.53] | -0.59 | 0.504 | - | - | 0.45 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 121 | 104 | 17 | 0 | -0.38 [-1.24; +0.04] | -1.25 | 0.511 | - | - | 0.44 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 121 | 104 | 17 | 0 | -2.26 [-3.48; -1.02] | -4.82 | 0.461 | - | - | 0.16 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 121 | 104 | 17 | 0 | -3.85 [-14.87; +2.99] | -6.05 | 0.478 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 367 | 365 | 2 | 0 | -0.09 [-0.72; +0.48] | -0.61 | 0.498 | - | - | 0.84 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 367 | 365 | 2 | 0 | +0.50 [+0.02; +0.78] | -0.36 | 0.513 | - | - | 0.38 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 367 | 365 | 2 | 0 | +0.01 [-0.94; +1.11] | -0.62 | 0.508 | - | - | 0.26 | - / - / False | False / False |
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
| KT08 | - | ABD | 15 | 213 | 213 | 0 | 0 | -0.88 [-3.50; +1.25] | -1.38 | 0.485 | - | - | 0.61 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 142 | 142 | 0 | 0 | -1.17 [-3.91; +2.85] | -3.11 | 0.484 | - | - | 0.16 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 114 | 114 | 0 | 0 | -0.26 [-3.90; +1.26] | -1.19 | 0.499 | - | - | 0.10 | - / - / False | False / False |
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
| KT10 | + | ABD | 15 | 952 | 950 | 2 | 0 | -0.66 [-1.13; -0.26] | -1.69 | 0.470 | - | - | 1.00 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 510 | 509 | 1 | 0 | -1.52 [-3.25; -0.81] | -2.89 | 0.462 | - | - | 0.51 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 524 | 523 | 1 | 0 | -1.24 [-4.55; +1.71] | -3.41 | 0.468 | - | - | 0.37 | - / - / False | False / False |

## Hücre: 2023Q3

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 323 | 319 | 4 | 0 | -0.11 [-2.54; +3.21] | -1.13 | 0.486 | - | - | 0.79 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 191 | 126 | 0 | 65 | -1.06 [-3.65; +1.79] | -1.69 | 0.506 | - | - | 0.15 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 141 | 58 | 0 | 83 | -4.20 [-4.20; -4.20] | -3.37 | 0.451 | - | - | 0.07 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 139 | 114 | 25 | 0 | -0.72 [-2.98; +2.51] | -0.31 | 0.470 | - | - | 0.52 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 90 | 54 | 6 | 30 | -0.94 [-4.55; +3.58] | +0.38 | 0.507 | - | - | 0.18 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 65 | 24 | 3 | 38 | -1.25 [-1.25; -1.25] | -3.07 | 0.411 | - | - | 0.08 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 435 | 387 | 0 | 48 | -0.86 [-1.04; -0.27] | -0.92 | 0.466 | - | - | 0.87 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 435 | 306 | 0 | 129 | -0.68 [-0.75; -0.67] | -0.95 | 0.476 | - | - | 0.32 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 435 | 240 | 0 | 195 | -0.98 [-0.98; -0.98] | -1.79 | 0.473 | - | - | 0.18 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 161 | 114 | 8 | 39 | -0.44 [-1.23; +1.68] | +0.27 | 0.515 | - | - | 0.52 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 161 | 99 | 4 | 58 | -0.96 [-1.74; +2.82] | -0.72 | 0.490 | - | - | 0.30 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 161 | 81 | 4 | 76 | -1.30 [-1.30; -1.30] | -1.16 | 0.475 | - | - | 0.21 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 130 | 84 | 22 | 24 | -2.13 [-7.33; -0.05] | -3.55 | 0.456 | - | - | 0.36 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 130 | 60 | 21 | 49 | -2.64 [-3.43; -2.07] | -4.22 | 0.481 | - | - | 0.11 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 130 | 25 | 11 | 94 | -9.00 [-9.00; -9.00] | -11.85 | 0.438 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 16 | 15 | 0 | 1 | +0.45 [-15.67; +1.63] | -0.05 | 0.458 | - | - | 0.08 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 16 | 14 | 0 | 2 | +2.20 [-24.14; +4.22] | +0.90 | 0.492 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 16 | 13 | 0 | 3 | +0.80 [+0.80; +0.80] | -4.68 | 0.492 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 2 | 2 | 0 | 0 | +0.46 [+0.46; +0.46] | +0.46 | 0.392 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 2 | 2 | 0 | 0 | -1.03 [-1.03; -1.03] | -1.03 | 0.496 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 2 | 2 | 0 | 0 | +2.51 [+2.51; +2.51] | +2.51 | 0.537 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 3 | 1 | 2 | 0 | -8.83 [-8.83; -8.83] | -8.83 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 3 | 1 | 2 | 0 | -28.47 [-28.47; -28.47] | -28.47 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 3 | 1 | 0 | 2 | -22.38 [-22.38; -22.38] | -22.38 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 373 | 329 | 0 | 44 | -0.84 [-1.35; +0.32] | -1.12 | 0.466 | - | - | 0.80 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 373 | 257 | 0 | 116 | -0.49 [-0.73; +0.60] | -1.02 | 0.479 | - | - | 0.27 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 373 | 202 | 0 | 171 | -1.08 [-1.08; -1.08] | -2.28 | 0.471 | - | - | 0.15 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 135 | 95 | 7 | 33 | +0.11 [-0.41; +1.41] | +0.62 | 0.531 | - | - | 0.44 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 135 | 80 | 4 | 51 | +0.40 [-0.19; +2.94] | +1.10 | 0.527 | - | - | 0.25 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 135 | 64 | 4 | 67 | +0.58 [+0.58; +0.58] | +1.45 | 0.521 | - | - | 0.17 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 116 | 73 | 20 | 23 | -1.94 [-8.35; +0.51] | -4.98 | 0.450 | - | - | 0.32 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 116 | 51 | 19 | 46 | -1.44 [-3.05; -0.31] | -3.92 | 0.493 | - | - | 0.10 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 116 | 21 | 10 | 85 | -8.28 [-8.28; -8.28] | -10.22 | 0.430 | - | - | 0.05 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 272 | 237 | 0 | 35 | -1.51 [-1.77; -0.90] | -1.15 | 0.439 | - | - | 0.66 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 272 | 179 | 0 | 93 | -1.72 [-1.77; -1.70] | -1.55 | 0.444 | - | - | 0.20 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 272 | 131 | 0 | 141 | -2.66 [-2.66; -2.66] | -3.35 | 0.436 | - | - | 0.11 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 92 | 56 | 5 | 31 | +1.33 [+1.18; +2.22] | +1.20 | 0.556 | - | - | 0.27 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 92 | 47 | 2 | 43 | +1.53 [+0.16; +1.76] | +1.70 | 0.551 | - | - | 0.16 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 92 | 39 | 2 | 51 | +3.65 [+3.65; +3.65] | +2.38 | 0.592 | - | - | 0.11 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 95 | 58 | 17 | 20 | -2.24 [-7.25; +0.10] | -3.74 | 0.452 | - | - | 0.25 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 95 | 41 | 16 | 38 | -2.64 [-5.22; -0.62] | -4.62 | 0.474 | - | - | 0.09 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 95 | 18 | 9 | 68 | -10.84 [-10.84; -10.84] | -13.01 | 0.433 | - | - | 0.05 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 433 | 385 | 0 | 48 | -0.85 [-1.10; -0.08] | -0.92 | 0.466 | - | - | 0.86 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 433 | 304 | 0 | 129 | -0.62 [-0.71; -0.24] | -0.95 | 0.476 | - | - | 0.32 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 433 | 239 | 0 | 194 | -1.00 [-1.00; -1.00] | -1.82 | 0.472 | - | - | 0.18 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 159 | 113 | 8 | 38 | -0.48 [-1.23; +1.68] | +0.23 | 0.514 | - | - | 0.52 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 159 | 99 | 4 | 56 | -0.96 [-1.74; +2.82] | -0.72 | 0.490 | - | - | 0.30 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 159 | 81 | 4 | 74 | -1.30 [-1.30; -1.30] | -1.16 | 0.475 | - | - | 0.21 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 130 | 84 | 22 | 24 | -2.13 [-7.33; -0.05] | -3.55 | 0.456 | - | - | 0.36 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 130 | 60 | 21 | 49 | -2.64 [-3.43; -2.07] | -4.22 | 0.481 | - | - | 0.11 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 130 | 25 | 11 | 94 | -9.00 [-9.00; -9.00] | -11.85 | 0.438 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 229 | 199 | 0 | 30 | -0.09 [-1.92; +0.91] | -0.27 | 0.501 | - | - | 0.58 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 229 | 158 | 0 | 71 | +0.55 [+0.43; +1.07] | -0.34 | 0.505 | - | - | 0.18 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 229 | 127 | 0 | 102 | +0.39 [+0.39; +0.39] | +0.10 | 0.510 | - | - | 0.11 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 87 | 58 | 3 | 26 | -0.76 [-1.09; +0.20] | +0.20 | 0.491 | - | - | 0.28 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 87 | 51 | 1 | 35 | -0.91 [-1.11; +0.07] | -0.08 | 0.503 | - | - | 0.17 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 87 | 41 | 2 | 44 | -0.48 [-0.48; -0.48] | -0.50 | 0.498 | - | - | 0.12 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 72 | 48 | 15 | 9 | -0.68 [-4.13; +0.63] | +0.24 | 0.492 | - | - | 0.21 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 72 | 38 | 14 | 20 | -2.14 [-4.29; -1.02] | -3.08 | 0.481 | - | - | 0.08 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 72 | 13 | 5 | 54 | -13.92 [-13.92; -13.92] | -14.17 | 0.411 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 8 | 8 | 0 | 0 | -4.87 [-15.67; +1.24] | -2.30 | 0.367 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 8 | 7 | 0 | 1 | -4.93 [-24.14; -1.73] | +1.26 | 0.408 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 8 | 6 | 0 | 2 | -7.20 [-7.20; -7.20] | -8.29 | 0.350 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 2 | 2 | 0 | 0 | +0.46 [+0.46; +0.46] | +0.46 | 0.392 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 2 | 2 | 0 | 0 | -1.03 [-1.03; -1.03] | -1.03 | 0.496 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 2 | 2 | 0 | 0 | +2.51 [+2.51; +2.51] | +2.51 | 0.537 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 1 | 1 | 0 | 0 | -8.83 [-8.83; -8.83] | -8.83 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 1 | 1 | 0 | 0 | -28.47 [-28.47; -28.47] | -28.47 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 45 | 1 | 1 | 0 | 0 | -22.38 [-22.38; -22.38] | -22.38 | 0.222 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 178 | 92 | 2 | 84 | +1.04 [+0.19; +5.56] | +1.46 | 0.544 | - | - | 0.30 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 122 | 41 | 0 | 81 | +0.24 [-0.30; +2.18] | +2.77 | 0.531 | - | - | 0.07 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 95 | 7 | 0 | 88 | +9.86 [+9.86; +9.86] | +14.46 | 0.702 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 47 | 28 | 0 | 19 | -0.96 [-1.91; -0.33] | -0.50 | 0.470 | - | - | 0.15 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 37 | 12 | 0 | 25 | -2.60 [-3.35; -1.10] | -1.57 | 0.482 | - | - | 0.06 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 30 | 4 | 0 | 26 | -4.14 [-4.14; -4.14] | -2.64 | 0.350 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 4 | 0 | 3 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | BIST | 30 | 2 | 0 | 1 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | BIST | 45 | 2 | 0 | 1 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 15 | 5 | 4 | 0 | 1 | -18.01 [-20.96; -15.07] | -18.59 | 0.094 | - | - | 0.05 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 5 | 4 | 0 | 1 | -15.24 [-15.29; -15.20] | -15.20 | 0.216 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 5 | 2 | 0 | 3 | -23.80 [-23.80; -23.80] | -23.80 | 0.156 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | -33.25 [-33.25; -33.25] | -33.25 | 0.000 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | -15.94 [-15.94; -15.94] | -15.94 | 0.053 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | -40.63 [-40.63; -40.63] | -40.63 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1089 | 952 | 6 | 131 | +0.05 [-0.40; +0.54] | +0.18 | 0.516 | - | - | 1.00 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 692 | 468 | 3 | 221 | +0.75 [+0.55; +1.07] | +0.69 | 0.528 | - | - | 0.48 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 488 | 143 | 1 | 344 | +0.71 [+0.71; +0.71] | -0.16 | 0.523 | - | - | 0.12 | - / - / False | False / False |

FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok.
