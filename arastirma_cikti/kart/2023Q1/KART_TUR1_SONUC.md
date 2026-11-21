# KART TURU 1 — sonuç (açık kesik 2023-03-31, açılmış blok 1: 2023Q1)

KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test

Bakış: BİLGİ (karar bakışı değil). KASA kapısı: kesik 2023-03-31, dosyalar en geç {'/tmp/kasa/acik/V_ABD.pkl': '2023-03-31', '/tmp/kasa/acik/V_AVR.pkl': '2023-03-31', '/tmp/kasa/acik/V_BIST.pkl': '2023-03-31', '/tmp/kasa/acik/k34_yahoo.pkl': '2023-03-31'}. Çıktı en geç tarih: {'kt_satir.csv.gz': '2023-03-31', 'olculen_son_giris': {'15': '2023-03-13', '30': '2023-02-20', '45': '2023-01-27'}}.
Ön kayıt kapısı: {'onkayit': 'arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md', 'commit': 'e0976cbd77685d0bafc6f8d31af2bb7b45739adf', 'commit_utc': '2026-11-21T12:50:23Z', 'kod': [{'yol': 'KART_TUR1.py', 'sha256': '334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b'}, {'yol': 'CETVEL2.py', 'sha256': '2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6'}], 'kontrol': True, 'bagimli': 16}.
Yeniden üretim (K11): TUTTU [{'hucre': 'KT01 ABD R15 acik', 'n': 8568, 'fark': -0.0018021516425521743, 'sira': 0.49552873573246126, 'esit': True}, {'hucre': 'KT08 AVR R30 acik', 'n': 1366, 'fark': 0.004191942747841824, 'sira': 0.5129707104271153, 'esit': True}].
Prefix (K2): Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

## Kart etiketleri

| Kart | Etiket | Neden | BH p |
|---|---|---|---|
| KT00 | KONTROL GÖRMEDİ | R15: ABD FARK -2.04 boot [-4.62; +0.50] n 312 T+ False, AVR FARK -1.18 boot [-4.91; +0.45] n 115 T+ False; R30: ABD FARK -1.39 boot [-3.05; -0.16] n 122 T+ False, AVR FARK -1.79 boot [-5.48; -0.13] n 45 T+ False | - |
| KT01 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 400 güç 0.41; AVR R30 n 205 güç 0.58 | - |
| KT02 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 23 güç 0.10; AVR R15 n 3 güç 0.05; ABD R30 n 22 güç 0.05; AVR R30 n 2 güç 0.04 | - |
| KT03 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 360 güç 0.37; AVR R30 n 179 güç 0.52 | - |
| KT04 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 202 güç 0.59; AVR R15 n 116 güç 0.53; ABD R30 n 171 güç 0.19; AVR R30 n 100 güç 0.31 | - |
| KT05 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 395 güç 0.41; AVR R30 n 202 güç 0.58 | - |
| KT06 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 218 güç 0.62; AVR R15 n 163 güç 0.69; ABD R30 n 188 güç 0.20; AVR R30 n 133 güç 0.40 | - |
| KT07 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 9 güç 0.06; AVR R15 n 1 güç 0.04; ABD R30 n 9 güç 0.04; AVR R30 n 1 güç 0.03 | - |
| KT08 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 64 güç 0.22; AVR R15 n 5 güç 0.05; ABD R30 n 14 güç 0.04; AVR R30 n 3 güç 0.04 | - |
| KT09 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 8 güç 0.06; AVR R15 n 1 güç 0.04; ABD R30 n 6 güç 0.04; AVR R30 n 1 güç 0.03 | - |
| KT10 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 374 güç 0.39 | - |

## Huni (olay sayıları; getirisiz)

```
{
 "ABD": {
  "Y1": {
   "sinyal": 24036,
   "girdi": 24036,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 86,
   "giris_gec": 0,
   "likidite_alt20": 3069,
   "bolunme_gecmis": 31,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 3102,
   "tekil": 11638,
   "y1_olay": 9210,
   "F_KT02": 370,
   "F_KT03": 8073,
   "F_KT04": 4056,
   "F_KT05": 8763,
   "F_KT06": 5194,
   "F_KT07": 160,
   "sure_sn": 95.2
  },
  "D9": {
   "durum": 512924,
   "c": 246897,
   "sure_sn": 37.8
  },
  "MOM": {
   "sinyal": 87595,
   "ana": 14003,
   "U": 7037,
   "A": 6966,
   "son_tarih": "2023-02-28",
   "pk": {
    "girdi": 87595,
    "olay_havuz": 70020,
    "U": 7037,
    "A": 6966,
    "ana": 14003
   }
  },
  "BOFA": {
   "hisse": 1364,
   "kurulum": 535,
   "son": "2023-03-31"
  },
  "DS": {
   "girdi": 204898,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 125,
   "giris_gec": 0,
   "likidite_alt20": 47655,
   "bolunme_gecmis": 3883,
   "evren_once": 0,
   "gecmis_eksik": 5,
   "havuz_az": 0,
   "havuz_disi": 51543,
   "tekil": 0,
   "ds_gun": 204898,
   "havuz_gun": 153230,
   "ana": 14824,
   "F_KT08": 5074,
   "sure_sn": 94.7
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 14003,
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
    "olcum_r15": 14003,
    "kova_yok": 0,
    "donem": {
     "acik": 13367,
     "birikimli": 636
    }
   },
   "MOM|30": {
    "girdi": 14003,
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
    "tekil": 5736,
    "olcum_r15": 8143,
    "kova_yok": 0,
    "donem": {
     "acik": 7899,
     "birikimli": 368
    }
   },
   "MOM|45": {
    "girdi": 14003,
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
    "tekil": 7755,
    "olcum_r15": 6081,
    "kova_yok": 0,
    "donem": {
     "acik": 5979,
     "birikimli": 269
    }
   },
   "Y1|15": {
    "girdi": 9210,
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
    "olcum_r15": 9150,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 524
    }
   },
   "Y1|30": {
    "girdi": 9210,
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
    "olcum_r15": 9089,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 524
    }
   },
   "Y1|45": {
    "girdi": 9210,
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
    "olcum_r15": 8956,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 524
    }
   },
   "DS|15": {
    "girdi": 14824,
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
    "olcum_r15": 14658,
    "kova_yok": 0,
    "donem": {
     "acik": 14061,
     "birikimli": 522,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 14824,
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
    "tekil": 6036,
    "olcum_r15": 8588,
    "kova_yok": 0,
    "donem": {
     "acik": 8320,
     "birikimli": 326,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 14824,
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
    "tekil": 8012,
    "olcum_r15": 6606,
    "kova_yok": 0,
    "donem": {
     "acik": 6400,
     "birikimli": 270,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 535,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 325,
    "bolunme_gecmis": 23,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 351,
    "tekil": 0,
    "olcum_r15": 175,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 9
    }
   },
   "BOFA|30": {
    "girdi": 535,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 325,
    "bolunme_gecmis": 23,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 351,
    "tekil": 0,
    "olcum_r15": 173,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 9
    }
   },
   "BOFA|45": {
    "girdi": 535,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 325,
    "bolunme_gecmis": 23,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 351,
    "tekil": 0,
    "olcum_r15": 171,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 9
    }
   },
   "D9|15": {
    "girdi": 246897,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 304,
    "giris_gec": 20,
    "likidite_alt20": 53971,
    "bolunme_gecmis": 2095,
    "evren_once": 0,
    "gecmis_eksik": 648,
    "havuz_az": 0,
    "havuz_disi": 56714,
    "tekil": 170353,
    "olcum_r15": 19255,
    "kova_yok": 557,
    "donem": {
     "acik": 18015,
     "birikimli": 1007,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 246897,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 304,
    "giris_gec": 20,
    "likidite_alt20": 53971,
    "bolunme_gecmis": 2095,
    "evren_once": 0,
    "gecmis_eksik": 648,
    "havuz_az": 0,
    "havuz_disi": 56714,
    "tekil": 177624,
    "olcum_r15": 11941,
    "kova_yok": 373,
    "donem": {
     "acik": 11241,
     "birikimli": 672,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 246897,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 304,
    "giris_gec": 20,
    "likidite_alt20": 53971,
    "bolunme_gecmis": 2095,
    "evren_once": 0,
    "gecmis_eksik": 648,
    "havuz_az": 0,
    "havuz_disi": 56714,
    "tekil": 180256,
    "olcum_r15": 9235,
    "kova_yok": 345,
    "donem": {
     "acik": 8853,
     "birikimli": 482,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 13073,
   "girdi": 13073,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 20,
   "giris_gec": 0,
   "likidite_alt20": 2002,
   "bolunme_gecmis": 5,
   "evren_once": 0,
   "gecmis_eksik": 7,
   "havuz_az": 0,
   "havuz_disi": 2014,
   "tekil": 6257,
   "y1_olay": 4782,
   "F_KT02": 92,
   "F_KT03": 4152,
   "F_KT04": 2335,
   "F_KT05": 4439,
   "F_KT06": 2985,
   "F_KT07": 37,
   "sure_sn": 53.9
  },
  "MOM": {
   "sinyal": 44899,
   "ana": 7097,
   "U": 3586,
   "A": 3511,
   "son_tarih": "2023-02-28",
   "pk": {
    "girdi": 44899,
    "olay_havuz": 35505,
    "U": 3586,
    "A": 3511,
    "ana": 7097
   }
  },
  "BOFA": {
   "hisse": 575,
   "kurulum": 33,
   "son": "2023-03-31"
  },
  "DS": {
   "girdi": 52240,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 13,
   "giris_gec": 0,
   "likidite_alt20": 2772,
   "bolunme_gecmis": 753,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3543,
   "tekil": 0,
   "ds_gun": 52240,
   "havuz_gun": 48684,
   "ana": 4881,
   "F_KT08": 1984,
   "sure_sn": 38.6
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 7097,
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
    "olcum_r15": 7097,
    "kova_yok": 0,
    "donem": {
     "acik": 6832,
     "birikimli": 265
    }
   },
   "MOM|30": {
    "girdi": 7097,
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
    "tekil": 2777,
    "olcum_r15": 4255,
    "kova_yok": 0,
    "donem": {
     "acik": 4144,
     "birikimli": 176
    }
   },
   "MOM|45": {
    "girdi": 7097,
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
    "tekil": 3721,
    "olcum_r15": 3277,
    "kova_yok": 0,
    "donem": {
     "acik": 3230,
     "birikimli": 146
    }
   },
   "Y1|15": {
    "girdi": 4782,
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
    "olcum_r15": 4755,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 286
    }
   },
   "Y1|30": {
    "girdi": 4782,
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
    "olcum_r15": 4707,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 286
    }
   },
   "Y1|45": {
    "girdi": 4782,
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
    "olcum_r15": 4615,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 286
    }
   },
   "DS|15": {
    "girdi": 4881,
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
    "olcum_r15": 4863,
    "kova_yok": 0,
    "donem": {
     "acik": 4562,
     "dis": 259,
     "birikimli": 60
    }
   },
   "DS|30": {
    "girdi": 4881,
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
    "tekil": 1942,
    "olcum_r15": 2920,
    "kova_yok": 0,
    "donem": {
     "acik": 2741,
     "dis": 163,
     "birikimli": 35
    }
   },
   "DS|45": {
    "girdi": 4881,
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
    "tekil": 2573,
    "olcum_r15": 2288,
    "kova_yok": 0,
    "donem": {
     "acik": 2148,
     "dis": 129,
     "birikimli": 31
    }
   },
   "BOFA|15": {
    "girdi": 33,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 9,
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
| KT01 | + | ABD | 15 | 8686 | 8568 | 118 | 0 | -0.18 [-0.42; +0.06] | -0.18 | 0.496 | -0.28 | 0.9266 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 30 | 8686 | 8568 | 118 | 0 | -0.30 [-0.64; +0.01] | -0.31 | 0.493 | -0.43 | 0.9505 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 45 | 8686 | 8568 | 118 | 0 | -0.24 [-0.66; +0.15] | -0.40 | 0.497 | -0.38 | 0.8731 | 1.00 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 4496 | 4217 | 279 | 0 | -0.03 [-0.24; +0.20] | -0.16 | 0.495 | -0.15 | 0.6160 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 4496 | 4217 | 279 | 0 | -0.15 [-0.47; +0.19] | -0.18 | 0.495 | -0.32 | 0.7917 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | AVR | 45 | 4496 | 4217 | 279 | 0 | -0.14 [-0.54; +0.26] | -0.36 | 0.494 | -0.33 | 0.7569 | 1.00 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 2588 | 2188 | 400 | 0 | -0.80 [-1.33; -0.29] | -2.81 | 0.451 | -1.07 | 0.9975 | 1.00 | -0.01 / 0.02 / True | False / True |
| KT01 | + | BIST | 30 | 2588 | 2188 | 400 | 0 | -0.76 [-1.70; +0.28] | -3.42 | 0.475 | -1.23 | 0.9194 | 1.00 | -0.01 / 0.02 / True | False / False |
| KT01 | + | BIST | 45 | 2588 | 2188 | 400 | 0 | -0.72 [-2.02; +0.57] | -4.30 | 0.475 | -1.27 | 0.8585 | 0.93 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 346 | 338 | 8 | 0 | -0.15 [-1.58; +1.30] | +0.13 | 0.505 | -0.67 | 0.5780 | 0.82 | -0.04 / 0.04 / True | False / False |
| KT02 | + | ABD | 30 | 346 | 338 | 8 | 0 | -1.41 [-6.70; +1.70] | +0.30 | 0.514 | -3.14 | 0.6880 | 0.35 | +0.08 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 346 | 338 | 8 | 0 | -2.41 [-8.57; +1.27] | -0.26 | 0.499 | -4.25 | 0.8064 | 0.24 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 89 | 78 | 11 | 0 | +0.49 [-1.50; +2.59] | +1.56 | 0.537 | -0.62 | 0.3265 | 0.37 | -0.04 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 89 | 78 | 11 | 0 | +0.66 [-1.57; +3.14] | +1.05 | 0.517 | -0.73 | 0.2936 | 0.24 | -0.05 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 89 | 78 | 11 | 0 | -0.34 [-3.74; +3.18] | -0.07 | 0.510 | -2.44 | 0.5774 | 0.20 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 238 | 205 | 33 | 0 | -0.23 [-1.74; +1.62] | -2.69 | 0.445 | -1.16 | 0.5962 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 238 | 205 | 33 | 0 | +0.02 [-2.21; +2.93] | -2.14 | 0.489 | -1.41 | 0.4923 | 0.28 | -0.04 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 238 | 205 | 33 | 0 | +1.02 [-1.90; +4.20] | -2.80 | 0.500 | -0.70 | 0.2563 | 0.16 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 7614 | 7512 | 102 | 0 | -0.21 [-0.44; +0.02] | -0.21 | 0.495 | -0.29 | 0.9531 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 30 | 7614 | 7512 | 102 | 0 | -0.29 [-0.65; +0.07] | -0.35 | 0.493 | -0.43 | 0.9403 | 1.00 | -0.14 / 0.01 / True | False / False |
| KT03 | + | ABD | 45 | 7614 | 7512 | 102 | 0 | -0.25 [-0.70; +0.17] | -0.48 | 0.496 | -0.38 | 0.8544 | 1.00 | - / - / False | False / False |
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
| KT05 | + | ABD | 15 | 8245 | 8139 | 106 | 0 | -0.20 [-0.44; +0.04] | -0.19 | 0.495 | -0.30 | 0.9312 | 1.00 | -0.01 / 0.06 / True | False / False |
| KT05 | + | ABD | 30 | 8245 | 8139 | 106 | 0 | -0.36 [-0.71; +0.00] | -0.35 | 0.492 | -0.50 | 0.9732 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT05 | + | ABD | 45 | 8245 | 8139 | 106 | 0 | -0.33 [-0.76; +0.07] | -0.51 | 0.495 | -0.47 | 0.9341 | 1.00 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 4160 | 3909 | 251 | 0 | -0.01 [-0.22; +0.23] | -0.13 | 0.497 | -0.13 | 0.5263 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 30 | 4160 | 3909 | 251 | 0 | -0.13 [-0.47; +0.27] | -0.18 | 0.496 | -0.32 | 0.7555 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 45 | 4160 | 3909 | 251 | 0 | -0.11 [-0.53; +0.32] | -0.34 | 0.496 | -0.32 | 0.6829 | 1.00 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 2535 | 2141 | 394 | 0 | -0.82 [-1.30; -0.27] | -2.77 | 0.451 | -1.08 | 0.9983 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT05 | + | BIST | 30 | 2535 | 2141 | 394 | 0 | -0.76 [-1.86; +0.34] | -3.48 | 0.475 | -1.24 | 0.9206 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT05 | + | BIST | 45 | 2535 | 2141 | 394 | 0 | -0.74 [-2.00; +0.60] | -4.30 | 0.475 | -1.31 | 0.8611 | 0.93 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 4953 | 4885 | 68 | 0 | -0.02 [-0.27; +0.25] | -0.09 | 0.499 | -0.14 | 0.5540 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 4953 | 4885 | 68 | 0 | -0.10 [-0.45; +0.26] | -0.24 | 0.494 | -0.26 | 0.7018 | 1.00 | -0.04 / 0.03 / True | False / False |
| KT06 | + | ABD | 45 | 4953 | 4885 | 68 | 0 | -0.05 [-0.48; +0.40] | -0.29 | 0.498 | -0.23 | 0.5758 | 1.00 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 2801 | 2629 | 172 | 0 | -0.03 [-0.28; +0.23] | -0.14 | 0.496 | -0.15 | 0.5993 | 1.00 | -0.01 / 0.03 / True | False / False |
| KT06 | + | AVR | 30 | 2801 | 2629 | 172 | 0 | -0.18 [-0.59; +0.25] | -0.24 | 0.494 | -0.39 | 0.7925 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 2801 | 2629 | 172 | 0 | -0.10 [-0.56; +0.38] | -0.31 | 0.496 | -0.32 | 0.6670 | 1.00 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 1626 | 1381 | 245 | 0 | -1.04 [-1.67; -0.32] | -2.86 | 0.443 | -1.36 | 0.9983 | 1.00 | +0.05 / 0.02 / True | False / True |
| KT06 | + | BIST | 30 | 1626 | 1381 | 245 | 0 | -1.38 [-2.47; -0.12] | -3.68 | 0.470 | -2.03 | 0.9851 | 0.96 | +0.05 / 0.03 / True | False / True |
| KT06 | + | BIST | 45 | 1626 | 1381 | 245 | 0 | -1.51 [-2.97; -0.08] | -4.13 | 0.467 | -2.14 | 0.9801 | 0.77 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 151 | 146 | 5 | 0 | -0.45 [-2.34; +1.39] | -0.57 | 0.486 | -1.32 | 0.6824 | 0.45 | -0.07 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 151 | 146 | 5 | 0 | -3.53 [-14.50; +2.14] | +0.32 | 0.510 | -6.01 | 0.6928 | 0.16 | -0.35 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 151 | 146 | 5 | 0 | -6.13 [-19.32; +0.86] | -0.40 | 0.486 | -9.67 | 0.9059 | 0.12 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 36 | 30 | 6 | 0 | +0.36 [-3.13; +4.02] | +0.86 | 0.518 | -1.53 | 0.4217 | 0.16 | +0.01 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 36 | 30 | 6 | 0 | -0.33 [-3.81; +2.84] | +0.77 | 0.517 | -2.00 | 0.5699 | 0.11 | +0.02 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 36 | 30 | 6 | 0 | +1.24 [-3.82; +6.11] | +1.30 | 0.538 | -2.45 | 0.3352 | 0.09 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 129 | 108 | 21 | 0 | -0.16 [-2.00; +2.28] | -2.69 | 0.454 | -1.56 | 0.5619 | 0.46 | +0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 129 | 108 | 21 | 0 | -0.55 [-3.23; +2.72] | -2.29 | 0.496 | -2.45 | 0.6379 | 0.16 | +0.13 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 129 | 108 | 21 | 0 | +0.54 [-3.11; +5.11] | -3.51 | 0.493 | -2.49 | 0.4119 | 0.10 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 4836 | 4791 | 45 | 0 | +0.05 [-0.43; +0.62] | -0.02 | 0.509 | -0.23 | 0.5694 | 1.00 | +0.00 / 0.05 / True | False / False |
| KT08 | - | ABD | 30 | 3431 | 3395 | 36 | 0 | -0.41 [-1.61; +0.87] | -0.83 | 0.500 | -0.74 | 0.4238 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT08 | - | ABD | 45 | 2947 | 2917 | 30 | 0 | -1.16 [-3.51; +1.32] | -1.81 | 0.496 | -1.67 | 0.4330 | 0.99 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 1838 | 1784 | 54 | 0 | +0.29 [-0.42; +1.11] | +0.35 | 0.515 | +0.05 | 0.7364 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | AVR | 30 | 1406 | 1366 | 40 | 0 | +0.42 [-0.71; +1.89] | +0.32 | 0.513 | +0.06 | 0.6858 | 1.00 | +0.04 / 0.03 / True | False / False |
| KT08 | - | AVR | 45 | 1266 | 1235 | 31 | 0 | +0.32 [-0.80; +1.94] | +0.22 | 0.510 | -0.29 | 0.6629 | 1.00 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 721 | 653 | 68 | 0 | -0.73 [-1.85; +0.51] | -1.50 | 0.480 | -1.40 | 0.1229 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | BIST | 30 | 475 | 436 | 39 | 0 | -2.08 [-5.69; +0.94] | -2.89 | 0.469 | -3.28 | 0.1807 | 0.53 | +0.03 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 400 | 364 | 36 | 0 | -3.83 [-9.60; +0.43] | -3.31 | 0.471 | -5.70 | 0.0979 | 0.26 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 167 | 163 | 4 | 0 | +4.70 [-1.09; +9.97] | +1.44 | 0.540 | +0.06 | 0.0876 | 0.50 | +0.00 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 167 | 163 | 4 | 0 | +7.12 [-1.31; +16.24] | +1.18 | 0.526 | +0.74 | 0.0858 | 0.18 | +0.02 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 167 | 163 | 4 | 0 | +9.62 [-6.34; +31.68] | +0.58 | 0.512 | -4.96 | 0.3319 | 0.13 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 20 | 20 | 0 | 0 | +3.68 [-10.28; +19.16] | -5.40 | 0.447 | -6.03 | 0.3090 | 0.12 | +0.10 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 20 | 20 | 0 | 0 | +5.27 [-6.04; +18.56] | +2.27 | 0.542 | -2.84 | 0.1962 | 0.09 | +0.24 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 20 | 20 | 0 | 0 | +3.67 [-10.09; +18.76] | -2.79 | 0.510 | -5.05 | 0.3000 | 0.07 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 18015 | 17262 | 753 | 0 | -0.02 [-0.23; +0.20] | -0.33 | 0.496 | -0.12 | 0.5767 | 1.00 | +0.01 / 0.06 / True | False / False |
| KT10 | + | ABD | 30 | 11241 | 10773 | 468 | 0 | -0.12 [-0.59; +0.39] | -0.67 | 0.492 | -0.33 | 0.6800 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT10 | + | ABD | 45 | 8853 | 8495 | 358 | 0 | -0.04 [-0.61; +0.58] | -0.70 | 0.500 | -0.30 | 0.5442 | 1.00 | - / - / False | False / False |

## Hücre: birikimli

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 319 | 312 | 7 | 0 | -2.04 [-4.62; +0.50] | -1.67 | 0.428 | - | 0.8754 | 0.78 | -0.02 / 0.00 / True | False / False |
| KT00 | + | ABD | 30 | 176 | 122 | 0 | 54 | -1.39 [-3.05; -0.16] | -3.22 | 0.446 | - | 1.0000 | 0.14 | -0.19 / 0.00 / True | False / False |
| KT00 | + | ABD | 45 | 134 | 46 | 0 | 88 | -1.29 [-1.29; -1.29] | -3.00 | 0.465 | - | 1.0000 | 0.06 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 134 | 115 | 19 | 0 | -1.18 [-4.91; +0.45] | -1.87 | 0.448 | - | 0.7533 | 0.52 | -0.02 / 0.00 / True | False / False |
| KT00 | + | AVR | 30 | 91 | 45 | 10 | 36 | -1.79 [-5.48; -0.13] | -1.40 | 0.487 | - | 1.0000 | 0.15 | -0.07 / 0.00 / True | False / False |
| KT00 | + | AVR | 45 | 80 | 22 | 4 | 54 | -9.92 [-9.92; -9.92] | -11.73 | 0.237 | - | 1.0000 | 0.08 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 524 | 461 | 3 | 60 | +0.54 [+0.34; +1.34] | +0.43 | 0.527 | - | 0.1219 | 0.92 | +0.08 / 0.00 / True | False / False |
| KT01 | + | ABD | 30 | 524 | 400 | 3 | 121 | +0.68 [+0.01; +2.23] | -0.54 | 0.516 | - | 0.2463 | 0.41 | +0.10 / 0.00 / True | False / False |
| KT01 | + | ABD | 45 | 524 | 267 | 3 | 254 | -0.68 [-0.68; -0.68] | -2.02 | 0.489 | - | 1.0000 | 0.19 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 286 | 251 | 8 | 27 | -0.38 [-1.46; +0.48] | -0.35 | 0.488 | - | 0.7545 | 0.87 | -0.02 / 0.00 / True | False / False |
| KT01 | + | AVR | 30 | 286 | 205 | 6 | 75 | +0.83 [+0.64; +0.96] | +0.85 | 0.533 | - | 0.2454 | 0.58 | -0.01 / 0.00 / True | False / False |
| KT01 | + | AVR | 45 | 286 | 118 | 1 | 167 | +0.63 [+0.63; +0.63] | +0.19 | 0.518 | - | 0.4909 | 0.29 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 23 | 10 | 1 | 12 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | 0.7490 | 0.07 | -0.15 / 0.00 / True | False / False |
| KT01 | + | BIST | 30 | 23 | 5 | 0 | 18 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | 0.5012 | 0.04 | -0.13 / 0.00 / True | False / False |
| KT01 | + | BIST | 45 | 23 | 5 | 0 | 18 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | 1.0000 | 0.03 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 24 | 23 | 0 | 1 | +0.40 [-4.82; +2.88] | -0.26 | 0.536 | - | 0.3777 | 0.10 | +0.07 / 0.00 / True | False / False |
| KT02 | + | ABD | 30 | 24 | 22 | 0 | 2 | +0.85 [-0.53; +1.16] | -1.58 | 0.523 | - | 0.4903 | 0.05 | +0.01 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 24 | 17 | 0 | 7 | -2.17 [-2.17; -2.17] | -2.68 | 0.452 | - | 1.0000 | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 3 | 3 | 0 | 0 | +1.41 [-15.91; +11.43] | +8.70 | 0.667 | - | 0.4938 | 0.05 | +0.23 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 3 | 2 | 0 | 1 | +8.12 [-3.77; +20.02] | +8.12 | 0.688 | - | 0.5050 | 0.04 | -0.03 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 3 | 1 | 0 | 2 | +27.57 [+27.57; +27.57] | +27.57 | 1.000 | - | 0.4944 | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 5 | 1 | 0 | 4 | -9.63 [-9.63; -9.63] | -9.63 | 0.000 | - | 1.0000 | 0.03 | +0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 5 | 0 | 0 | 5 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT02 | + | BIST | 45 | 5 | 0 | 0 | 5 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT03 | + | ABD | 15 | 459 | 409 | 3 | 47 | +0.53 [+0.38; +1.50] | +0.42 | 0.525 | - | 0.1228 | 0.88 | -0.03 / 0.00 / True | False / False |
| KT03 | + | ABD | 30 | 459 | 360 | 3 | 96 | +0.61 [-0.07; +2.20] | -0.68 | 0.514 | - | 0.5022 | 0.37 | -0.02 / 0.00 / True | False / False |
| KT03 | + | ABD | 45 | 459 | 241 | 3 | 215 | -0.96 [-0.96; -0.96] | -2.24 | 0.484 | - | 1.0000 | 0.18 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 242 | 216 | 6 | 20 | -0.40 [-1.65; +0.75] | -0.41 | 0.483 | - | 0.7476 | 0.82 | -0.01 / 0.00 / True | False / False |
| KT03 | + | AVR | 30 | 242 | 179 | 4 | 59 | +0.59 [+0.19; +0.89] | +0.59 | 0.521 | - | 0.2458 | 0.52 | +0.01 / 0.00 / True | False / False |
| KT03 | + | AVR | 45 | 242 | 104 | 1 | 137 | +0.36 [+0.36; +0.36] | -0.01 | 0.505 | - | 0.4952 | 0.26 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 21 | 10 | 1 | 10 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | 0.7601 | 0.07 | +0.05 / 0.00 / True | False / False |
| KT03 | + | BIST | 30 | 21 | 5 | 0 | 16 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | 0.4945 | 0.04 | -0.21 / 0.00 / True | False / False |
| KT03 | + | BIST | 45 | 21 | 5 | 0 | 16 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | 1.0000 | 0.03 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 233 | 202 | 2 | 29 | +0.69 [+0.42; +2.63] | +0.48 | 0.539 | - | 0.1290 | 0.59 | +0.00 / 0.00 / True | False / False |
| KT04 | + | ABD | 30 | 233 | 171 | 2 | 60 | +0.50 [-0.68; +2.94] | +0.28 | 0.526 | - | 0.4914 | 0.19 | +0.02 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 233 | 109 | 2 | 122 | -1.41 [-1.41; -1.41] | -2.44 | 0.471 | - | 1.0000 | 0.09 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 127 | 116 | 1 | 10 | -0.80 [-2.27; -0.02] | -0.76 | 0.461 | - | 1.0000 | 0.53 | -0.02 / 0.00 / True | False / False |
| KT04 | + | AVR | 30 | 127 | 100 | 0 | 27 | -0.13 [-0.16; -0.08] | +0.64 | 0.495 | - | 1.0000 | 0.31 | -0.13 / 0.00 / True | False / False |
| KT04 | + | AVR | 45 | 127 | 64 | 0 | 63 | -1.78 [-1.78; -1.78] | -1.06 | 0.461 | - | 1.0000 | 0.17 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 18 | 9 | 0 | 9 | -2.63 [-6.39; +0.37] | -4.98 | 0.338 | - | 0.7525 | 0.06 | -0.37 / 0.00 / True | False / False |
| KT04 | + | BIST | 30 | 18 | 5 | 0 | 13 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | 0.5040 | 0.04 | -0.99 / 0.00 / False | False / False |
| KT04 | + | BIST | 45 | 18 | 5 | 0 | 13 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | 1.0000 | 0.03 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 518 | 455 | 3 | 60 | +0.49 [+0.30; +1.05] | +0.38 | 0.524 | - | 0.1235 | 0.92 | -0.03 / 0.00 / True | False / False |
| KT05 | + | ABD | 30 | 518 | 395 | 3 | 120 | +0.69 [+0.01; +2.23] | -0.66 | 0.516 | - | 0.2440 | 0.41 | -0.03 / 0.00 / True | False / False |
| KT05 | + | ABD | 45 | 518 | 262 | 3 | 253 | -0.70 [-0.70; -0.70] | -2.14 | 0.488 | - | 1.0000 | 0.19 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 279 | 248 | 5 | 26 | -0.27 [-1.32; +0.61] | -0.27 | 0.491 | - | 0.7557 | 0.87 | -0.00 / 0.00 / True | False / False |
| KT05 | + | AVR | 30 | 279 | 202 | 3 | 74 | +0.93 [+0.62; +1.17] | +1.04 | 0.536 | - | 0.2437 | 0.58 | +0.05 / 0.00 / True | False / False |
| KT05 | + | AVR | 45 | 279 | 115 | 1 | 163 | +0.87 [+0.87; +0.87] | +0.31 | 0.524 | - | 0.4948 | 0.29 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 23 | 10 | 1 | 12 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | 0.7535 | 0.07 | +0.06 / 0.00 / True | False / False |
| KT05 | + | BIST | 30 | 23 | 5 | 0 | 18 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | 0.4970 | 0.04 | -0.36 / 0.00 / True | False / False |
| KT05 | + | BIST | 45 | 23 | 5 | 0 | 18 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | 1.0000 | 0.03 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 241 | 218 | 0 | 23 | +0.54 [+0.46; +1.16] | +0.23 | 0.524 | - | 0.1272 | 0.62 | -0.11 / 0.00 / True | False / False |
| KT06 | + | ABD | 30 | 241 | 188 | 0 | 53 | +0.77 [-0.10; +2.37] | -0.29 | 0.516 | - | 0.4998 | 0.20 | -0.13 / 0.00 / True | False / False |
| KT06 | + | ABD | 45 | 241 | 114 | 0 | 127 | -0.46 [-0.46; -0.46] | -0.89 | 0.492 | - | 1.0000 | 0.10 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 184 | 163 | 4 | 17 | -0.29 [-1.40; +0.69] | -0.16 | 0.491 | - | 0.6262 | 0.69 | -0.03 / 0.00 / True | False / False |
| KT06 | + | AVR | 30 | 184 | 133 | 4 | 47 | +0.99 [+0.82; +1.12] | +1.28 | 0.554 | - | 0.2467 | 0.40 | -0.05 / 0.00 / True | False / False |
| KT06 | + | AVR | 45 | 184 | 74 | 0 | 110 | +0.63 [+0.63; +0.63] | -0.03 | 0.504 | - | 0.5063 | 0.19 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 9 | 2 | 0 | 7 | -8.19 [-8.19; -8.19] | -8.19 | 0.346 | - | 1.0000 | 0.04 | +0.46 / 0.00 / True | False / False |
| KT06 | + | BIST | 30 | 9 | 2 | 0 | 7 | +11.62 [+11.62; +11.62] | +11.62 | 0.868 | - | 0.4971 | 0.03 | +0.88 / 0.00 / False | False / False |
| KT06 | + | BIST | 45 | 9 | 2 | 0 | 7 | +9.95 [+9.95; +9.95] | +9.95 | 0.781 | - | 0.4971 | 0.03 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 9 | 9 | 0 | 0 | +1.16 [+1.16; +1.16] | -0.26 | 0.532 | - | 0.4952 | 0.06 | -0.24 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 9 | 9 | 0 | 0 | +1.40 [+1.40; +1.40] | -1.54 | 0.559 | - | 0.4952 | 0.04 | -0.40 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 9 | 9 | 0 | 0 | -5.81 [-5.81; -5.81] | -2.68 | 0.419 | - | 1.0000 | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 1 | 1 | 0 | 0 | -15.91 [-15.91; -15.91] | -15.91 | 0.000 | - | 1.0000 | 0.04 | +0.15 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 1 | 1 | 0 | 0 | -3.77 [-3.77; -3.77] | -3.77 | 0.375 | - | 1.0000 | 0.03 | +0.27 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 1 | 0 | 0 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 15 | 2 | 1 | 0 | 1 | -9.63 [-9.63; -9.63] | -9.63 | 0.000 | - | 1.0000 | 0.03 | +1.38 / 0.00 / False | False / False |
| KT07 | + | BIST | 30 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 45 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | ABD | 15 | 137 | 64 | 0 | 73 | +1.61 [-1.28; +6.99] | -2.82 | 0.437 | - | 0.7510 | 0.22 | +0.00 / 0.00 / True | False / False |
| KT08 | - | ABD | 30 | 101 | 14 | 0 | 87 | +6.33 [+5.16; +10.63] | +5.53 | 0.562 | - | 1.0000 | 0.04 | -0.38 / 0.00 / True | False / False |
| KT08 | - | ABD | 45 | 97 | 10 | 0 | 87 | +6.04 [+6.04; +6.04] | -4.46 | 0.526 | - | 1.0000 | 0.04 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 15 | 5 | 1 | 9 | +4.55 [-0.09; +5.90] | +1.46 | 0.724 | - | 0.8692 | 0.05 | -0.21 / 0.00 / True | False / False |
| KT08 | - | AVR | 30 | 11 | 3 | 0 | 8 | +7.75 [+5.20; +12.84] | +5.26 | 0.905 | - | 1.0000 | 0.04 | +0.05 / 0.00 / True | False / False |
| KT08 | - | AVR | 45 | 12 | 1 | 1 | 10 | +15.80 [+15.80; +15.80] | +15.80 | 0.750 | - | 1.0000 | 0.03 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 54 | 16 | 2 | 36 | -0.99 [-1.65; +8.46] | -1.58 | 0.520 | - | 0.3809 | 0.09 | -0.47 / 0.00 / True | False / False |
| KT08 | - | BIST | 30 | 36 | 9 | 1 | 26 | -0.76 [-0.76; -0.76] | -5.13 | 0.501 | - | 0.4946 | 0.05 | -0.47 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 16 | 0 | 0 | 16 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 15 | 9 | 8 | 0 | 1 | +10.84 [-2.63; +22.42] | +6.06 | 0.693 | - | 0.2491 | 0.06 | +0.14 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 9 | 6 | 0 | 3 | +2.95 [-5.96; +7.40] | +1.86 | 0.551 | - | 0.5007 | 0.04 | +0.15 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 9 | 4 | 0 | 5 | +5.03 [+5.03; +5.03] | +14.31 | 0.606 | - | 0.4961 | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | +38.52 [+38.52; +38.52] | +38.52 | 1.000 | - | 0.4971 | 0.04 | -0.46 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | +44.15 [+44.15; +44.15] | +44.15 | 1.000 | - | 0.4971 | 0.03 | -0.43 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | +13.32 [+13.32; +13.32] | +13.32 | 0.909 | - | 0.4971 | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1007 | 746 | 10 | 251 | -0.08 [-0.30; -0.03] | -0.50 | 0.498 | - | 1.0000 | 0.99 | -0.05 / 0.00 / True | False / False |
| KT10 | + | ABD | 30 | 672 | 374 | 4 | 294 | +0.49 [-0.28; +1.14] | -0.23 | 0.505 | - | 0.5044 | 0.39 | -0.05 / 0.00 / True | False / False |
| KT10 | + | ABD | 45 | 482 | 112 | 2 | 368 | +1.92 [+1.92; +1.92] | -2.16 | 0.494 | - | 0.4960 | 0.10 | - / - / False | False / False |

## Hücre: 2023Q1

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 319 | 312 | 7 | 0 | -2.04 [-4.62; +0.50] | -1.67 | 0.428 | - | - | 0.78 | - / - / False | False / False |
| KT00 | + | ABD | 30 | 176 | 122 | 0 | 54 | -1.39 [-3.05; -0.16] | -3.22 | 0.446 | - | - | 0.14 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 134 | 46 | 0 | 88 | -1.29 [-1.29; -1.29] | -3.00 | 0.465 | - | - | 0.06 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 134 | 115 | 19 | 0 | -1.18 [-4.91; +0.45] | -1.87 | 0.448 | - | - | 0.52 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 91 | 45 | 10 | 36 | -1.79 [-5.48; -0.13] | -1.40 | 0.487 | - | - | 0.15 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 80 | 22 | 4 | 54 | -9.92 [-9.92; -9.92] | -11.73 | 0.237 | - | - | 0.08 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 524 | 461 | 3 | 60 | +0.54 [+0.34; +1.34] | +0.43 | 0.527 | - | - | 0.92 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 524 | 400 | 3 | 121 | +0.68 [+0.01; +2.23] | -0.54 | 0.516 | - | - | 0.41 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 524 | 267 | 3 | 254 | -0.68 [-0.68; -0.68] | -2.02 | 0.489 | - | - | 0.19 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 286 | 251 | 8 | 27 | -0.38 [-1.46; +0.48] | -0.35 | 0.488 | - | - | 0.87 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 286 | 205 | 6 | 75 | +0.83 [+0.64; +0.96] | +0.85 | 0.533 | - | - | 0.58 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 286 | 118 | 1 | 167 | +0.63 [+0.63; +0.63] | +0.19 | 0.518 | - | - | 0.29 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 23 | 10 | 1 | 12 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | - | 0.07 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 23 | 5 | 0 | 18 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | - | 0.04 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 23 | 5 | 0 | 18 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 24 | 23 | 0 | 1 | +0.40 [-4.82; +2.88] | -0.26 | 0.536 | - | - | 0.10 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 24 | 22 | 0 | 2 | +0.85 [-0.53; +1.16] | -1.58 | 0.523 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 24 | 17 | 0 | 7 | -2.17 [-2.17; -2.17] | -2.68 | 0.452 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 3 | 3 | 0 | 0 | +1.41 [-15.91; +11.43] | +8.70 | 0.667 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 3 | 2 | 0 | 1 | +8.12 [-3.77; +20.02] | +8.12 | 0.688 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 3 | 1 | 0 | 2 | +27.57 [+27.57; +27.57] | +27.57 | 1.000 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 5 | 1 | 0 | 4 | -9.63 [-9.63; -9.63] | -9.63 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 5 | 0 | 0 | 5 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT02 | + | BIST | 45 | 5 | 0 | 0 | 5 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT03 | + | ABD | 15 | 459 | 409 | 3 | 47 | +0.53 [+0.38; +1.50] | +0.42 | 0.525 | - | - | 0.88 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 459 | 360 | 3 | 96 | +0.61 [-0.07; +2.20] | -0.68 | 0.514 | - | - | 0.37 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 459 | 241 | 3 | 215 | -0.96 [-0.96; -0.96] | -2.24 | 0.484 | - | - | 0.18 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 242 | 216 | 6 | 20 | -0.40 [-1.65; +0.75] | -0.41 | 0.483 | - | - | 0.82 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 242 | 179 | 4 | 59 | +0.59 [+0.19; +0.89] | +0.59 | 0.521 | - | - | 0.52 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 242 | 104 | 1 | 137 | +0.36 [+0.36; +0.36] | -0.01 | 0.505 | - | - | 0.26 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 21 | 10 | 1 | 10 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | - | 0.07 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 21 | 5 | 0 | 16 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | - | 0.04 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 21 | 5 | 0 | 16 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | - | 0.03 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 233 | 202 | 2 | 29 | +0.69 [+0.42; +2.63] | +0.48 | 0.539 | - | - | 0.59 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 233 | 171 | 2 | 60 | +0.50 [-0.68; +2.94] | +0.28 | 0.526 | - | - | 0.19 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 233 | 109 | 2 | 122 | -1.41 [-1.41; -1.41] | -2.44 | 0.471 | - | - | 0.09 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 127 | 116 | 1 | 10 | -0.80 [-2.27; -0.02] | -0.76 | 0.461 | - | - | 0.53 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 127 | 100 | 0 | 27 | -0.13 [-0.16; -0.08] | +0.64 | 0.495 | - | - | 0.31 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 127 | 64 | 0 | 63 | -1.78 [-1.78; -1.78] | -1.06 | 0.461 | - | - | 0.17 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 18 | 9 | 0 | 9 | -2.63 [-6.39; +0.37] | -4.98 | 0.338 | - | - | 0.06 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 18 | 5 | 0 | 13 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | - | 0.04 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 18 | 5 | 0 | 13 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | - | 0.03 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 518 | 455 | 3 | 60 | +0.49 [+0.30; +1.05] | +0.38 | 0.524 | - | - | 0.92 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 518 | 395 | 3 | 120 | +0.69 [+0.01; +2.23] | -0.66 | 0.516 | - | - | 0.41 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 518 | 262 | 3 | 253 | -0.70 [-0.70; -0.70] | -2.14 | 0.488 | - | - | 0.19 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 279 | 248 | 5 | 26 | -0.27 [-1.32; +0.61] | -0.27 | 0.491 | - | - | 0.87 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 279 | 202 | 3 | 74 | +0.93 [+0.62; +1.17] | +1.04 | 0.536 | - | - | 0.58 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 279 | 115 | 1 | 163 | +0.87 [+0.87; +0.87] | +0.31 | 0.524 | - | - | 0.29 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 23 | 10 | 1 | 12 | -3.17 [-6.71; +0.37] | -5.76 | 0.325 | - | - | 0.07 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 23 | 5 | 0 | 18 | +10.77 [+10.77; +10.77] | +23.89 | 0.729 | - | - | 0.04 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 23 | 5 | 0 | 18 | -0.42 [-0.42; -0.42] | +4.26 | 0.570 | - | - | 0.03 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 241 | 218 | 0 | 23 | +0.54 [+0.46; +1.16] | +0.23 | 0.524 | - | - | 0.62 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 241 | 188 | 0 | 53 | +0.77 [-0.10; +2.37] | -0.29 | 0.516 | - | - | 0.20 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 241 | 114 | 0 | 127 | -0.46 [-0.46; -0.46] | -0.89 | 0.492 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 184 | 163 | 4 | 17 | -0.29 [-1.40; +0.69] | -0.16 | 0.491 | - | - | 0.69 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 184 | 133 | 4 | 47 | +0.99 [+0.82; +1.12] | +1.28 | 0.554 | - | - | 0.40 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 184 | 74 | 0 | 110 | +0.63 [+0.63; +0.63] | -0.03 | 0.504 | - | - | 0.19 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 9 | 2 | 0 | 7 | -8.19 [-8.19; -8.19] | -8.19 | 0.346 | - | - | 0.04 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 9 | 2 | 0 | 7 | +11.62 [+11.62; +11.62] | +11.62 | 0.868 | - | - | 0.03 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 9 | 2 | 0 | 7 | +9.95 [+9.95; +9.95] | +9.95 | 0.781 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 9 | 9 | 0 | 0 | +1.16 [+1.16; +1.16] | -0.26 | 0.532 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 9 | 9 | 0 | 0 | +1.40 [+1.40; +1.40] | -1.54 | 0.559 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 9 | 9 | 0 | 0 | -5.81 [-5.81; -5.81] | -2.68 | 0.419 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 1 | 1 | 0 | 0 | -15.91 [-15.91; -15.91] | -15.91 | 0.000 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 1 | 1 | 0 | 0 | -3.77 [-3.77; -3.77] | -3.77 | 0.375 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 1 | 0 | 0 | 1 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 15 | 2 | 1 | 0 | 1 | -9.63 [-9.63; -9.63] | -9.63 | 0.000 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT07 | + | BIST | 45 | 2 | 0 | 0 | 2 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT08 | - | ABD | 15 | 137 | 64 | 0 | 73 | +1.61 [-1.28; +6.99] | -2.82 | 0.437 | - | - | 0.22 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 101 | 14 | 0 | 87 | +6.33 [+5.16; +10.63] | +5.53 | 0.562 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 97 | 10 | 0 | 87 | +6.04 [+6.04; +6.04] | -4.46 | 0.526 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 15 | 5 | 1 | 9 | +4.55 [-0.09; +5.90] | +1.46 | 0.724 | - | - | 0.05 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 11 | 3 | 0 | 8 | +7.75 [+5.20; +12.84] | +5.26 | 0.905 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 12 | 1 | 1 | 10 | +15.80 [+15.80; +15.80] | +15.80 | 0.750 | - | - | 0.03 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 54 | 16 | 2 | 36 | -0.99 [-1.65; +8.46] | -1.58 | 0.520 | - | - | 0.09 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 36 | 9 | 1 | 26 | -0.76 [-0.76; -0.76] | -5.13 | 0.501 | - | - | 0.05 | - / - / False | False / False |
| KT08 | - | BIST | 45 | 16 | 0 | 0 | 16 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | ABD | 15 | 9 | 8 | 0 | 1 | +10.84 [-2.63; +22.42] | +6.06 | 0.693 | - | - | 0.06 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 9 | 6 | 0 | 3 | +2.95 [-5.96; +7.40] | +1.86 | 0.551 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 9 | 4 | 0 | 5 | +5.03 [+5.03; +5.03] | +14.31 | 0.606 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | +38.52 [+38.52; +38.52] | +38.52 | 1.000 | - | - | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | +44.15 [+44.15; +44.15] | +44.15 | 1.000 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | +13.32 [+13.32; +13.32] | +13.32 | 0.909 | - | - | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1007 | 746 | 10 | 251 | -0.08 [-0.30; -0.03] | -0.50 | 0.498 | - | - | 0.99 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 672 | 374 | 4 | 294 | +0.49 [-0.28; +1.14] | -0.23 | 0.505 | - | - | 0.39 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 482 | 112 | 2 | 368 | +1.92 [+1.92; +1.92] | -2.16 | 0.494 | - | - | 0.10 | - / - / False | False / False |

FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok.
