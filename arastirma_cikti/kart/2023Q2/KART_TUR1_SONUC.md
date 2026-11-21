# KART TURU 1 — sonuç (açık kesik 2023-06-30, açılmış blok 2: 2023Q1, 2023Q2)

KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test

Bakış: BİLGİ (karar bakışı değil). KASA kapısı: kesik 2023-06-30, dosyalar en geç {'/tmp/kasa/acik/V_ABD.pkl': '2023-06-30', '/tmp/kasa/acik/V_AVR.pkl': '2023-06-30', '/tmp/kasa/acik/V_BIST.pkl': '2023-06-27', '/tmp/kasa/acik/k34_yahoo.pkl': '2023-06-30'}. Çıktı en geç tarih: {'kt_satir.csv.gz': '2023-06-30', 'olculen_son_giris': {'15': '2023-06-09', '30': '2023-05-22', '45': '2023-04-28'}}.
Ön kayıt kapısı: {'onkayit': 'arastirma_cikti/kart/KART_TUR1_ON_KAYIT.md', 'commit': 'e0976cbd77685d0bafc6f8d31af2bb7b45739adf', 'commit_utc': '2026-11-21T12:50:23Z', 'kod': [{'yol': 'KART_TUR1.py', 'sha256': '334cc4f9bdafef0accf754b229626eb92010d519ba23dc8e9037a14f8713640b'}, {'yol': 'CETVEL2.py', 'sha256': '2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6'}], 'kontrol': True, 'bagimli': 16}.
Yeniden üretim (K11): TUTTU [{'hucre': 'KT01 ABD R15 acik', 'n': 8568, 'fark': -0.0018016196057328976, 'sira': 0.49553144909154473, 'esit': True}, {'hucre': 'KT08 AVR R30 acik', 'n': 1366, 'fark': 0.004191942747841824, 'sira': 0.5129707104271153, 'esit': True}].
Prefix (K2): Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

## Kart etiketleri

| Kart | Etiket | Neden | BH p |
|---|---|---|---|
| KT00 | KONTROL GÖRMEDİ | R15: ABD FARK -0.27 boot [-2.36; +1.69] n 635 T+ False, AVR FARK -0.02 boot [-1.67; +0.97] n 245 T+ False; R30: ABD FARK +0.58 boot [-1.69; +3.37] n 306 T+ False, AVR FARK -0.80 boot [-3.16; +1.06] n 133 T+ False | - |
| KT01 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 878 güç 0.77 | - |
| KT02 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 88 güç 0.29; AVR R15 n 9 güç 0.07; ABD R30 n 60 güç 0.09; AVR R30 n 6 güç 0.05 | - |
| KT03 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 plasebo kapısı düştü (ort -0.01 puan, pay 0.08); AVR R15 plasebo kapısı düştü (ort +0.00 puan, pay 0.11); ABD R30 n 770 güç 0.71 | - |
| KT04 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 383 güç 0.40; AVR R30 n 182 güç 0.53 | - |
| KT05 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R30 n 869 güç 0.77; AVR R30 plasebo kapısı düştü (ort +0.00 puan, pay 0.10) | - |
| KT06 | BİLGİ (ÖLÇÜLEMEDİ) | AVR R15 plasebo kapısı düştü (ort -0.01 puan, pay 0.09); ABD R30 n 448 güç 0.46; AVR R30 n 238 güç 0.65 | - |
| KT07 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 30 güç 0.12; AVR R15 n 5 güç 0.05; ABD R30 n 21 güç 0.05; AVR R30 n 3 güç 0.04 | - |
| KT08 | BİLGİ (ÖLÇÜLEMEDİ) | AVR R15 n 35 güç 0.18; ABD R30 n 208 güç 0.22; AVR R30 n 19 güç 0.08 | - |
| KT09 | BİLGİ (ÖLÇÜLEMEDİ) | ABD R15 n 15 güç 0.08; AVR R15 n 1 güç 0.04; ABD R30 n 13 güç 0.04; AVR R30 n 1 güç 0.03 | - |
| KT10 | BİLGİ (ÖLÇÜLEMEDİ) | R15 ters şartlar tuttu ama BH (q 0.1) geçmedi (p 0.0173) | ABD R30 n 895 güç 0.78 | - |

## Huni (olay sayıları; getirisiz)

```
{
 "ABD": {
  "Y1": {
   "sinyal": 25580,
   "girdi": 25580,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 74,
   "giris_gec": 0,
   "likidite_alt20": 3241,
   "bolunme_gecmis": 37,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 3280,
   "tekil": 12413,
   "y1_olay": 9813,
   "F_KT02": 438,
   "F_KT03": 8599,
   "F_KT04": 4297,
   "F_KT05": 9360,
   "F_KT06": 5561,
   "F_KT07": 182,
   "sure_sn": 88.0
  },
  "D9": {
   "durum": 555930,
   "c": 260750,
   "sure_sn": 38.7
  },
  "MOM": {
   "sinyal": 91607,
   "ana": 14646,
   "U": 7360,
   "A": 7286,
   "son_tarih": "2023-05-31",
   "pk": {
    "girdi": 91607,
    "olay_havuz": 73234,
    "U": 7360,
    "A": 7286,
    "ana": 14646
   }
  },
  "BOFA": {
   "hisse": 1368,
   "kurulum": 554,
   "son": "2023-06-30"
  },
  "DS": {
   "girdi": 214975,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 123,
   "giris_gec": 0,
   "likidite_alt20": 49671,
   "bolunme_gecmis": 3959,
   "evren_once": 0,
   "gecmis_eksik": 5,
   "havuz_az": 0,
   "havuz_disi": 53635,
   "tekil": 0,
   "ds_gun": 214975,
   "havuz_gun": 161217,
   "ana": 15563,
   "F_KT08": 5286,
   "sure_sn": 77.1
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 14646,
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
    "olcum_r15": 14646,
    "kova_yok": 0,
    "donem": {
     "acik": 13367,
     "birikimli": 1279
    }
   },
   "MOM|30": {
    "girdi": 14646,
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
    "tekil": 5983,
    "olcum_r15": 8527,
    "kova_yok": 0,
    "donem": {
     "acik": 7899,
     "birikimli": 764
    }
   },
   "MOM|45": {
    "girdi": 14646,
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
    "tekil": 8087,
    "olcum_r15": 6356,
    "kova_yok": 0,
    "donem": {
     "acik": 5979,
     "birikimli": 580
    }
   },
   "Y1|15": {
    "girdi": 9813,
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
    "olcum_r15": 9723,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1127
    }
   },
   "Y1|30": {
    "girdi": 9813,
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
    "olcum_r15": 9573,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1127
    }
   },
   "Y1|45": {
    "girdi": 9813,
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
    "olcum_r15": 9393,
    "kova_yok": 0,
    "donem": {
     "acik": 8686,
     "birikimli": 1127
    }
   },
   "DS|15": {
    "girdi": 15563,
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
    "olcum_r15": 15428,
    "kova_yok": 0,
    "donem": {
     "acik": 14061,
     "birikimli": 1261,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 15563,
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
    "tekil": 6358,
    "olcum_r15": 9051,
    "kova_yok": 0,
    "donem": {
     "acik": 8320,
     "birikimli": 743,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 15563,
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
    "tekil": 8469,
    "olcum_r15": 6874,
    "kova_yok": 0,
    "donem": {
     "acik": 6400,
     "birikimli": 552,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 554,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 337,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 364,
    "tekil": 0,
    "olcum_r15": 182,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 15
    }
   },
   "BOFA|30": {
    "girdi": 554,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 337,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 364,
    "tekil": 0,
    "olcum_r15": 180,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 15
    }
   },
   "BOFA|45": {
    "girdi": 554,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 337,
    "bolunme_gecmis": 24,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 364,
    "tekil": 0,
    "olcum_r15": 180,
    "kova_yok": 0,
    "donem": {
     "acik": 167,
     "birikimli": 15
    }
   },
   "D9|15": {
    "girdi": 260750,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 310,
    "giris_gec": 23,
    "likidite_alt20": 58151,
    "bolunme_gecmis": 2257,
    "evren_once": 0,
    "gecmis_eksik": 717,
    "havuz_az": 0,
    "havuz_disi": 61125,
    "tekil": 178835,
    "olcum_r15": 20222,
    "kova_yok": 559,
    "donem": {
     "acik": 18014,
     "birikimli": 1959,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 260750,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 310,
    "giris_gec": 23,
    "likidite_alt20": 58151,
    "bolunme_gecmis": 2257,
    "evren_once": 0,
    "gecmis_eksik": 717,
    "havuz_az": 0,
    "havuz_disi": 61125,
    "tekil": 186547,
    "olcum_r15": 12469,
    "kova_yok": 374,
    "donem": {
     "acik": 11241,
     "birikimli": 1182,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 260750,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 310,
    "giris_gec": 23,
    "likidite_alt20": 58151,
    "bolunme_gecmis": 2257,
    "evren_once": 0,
    "gecmis_eksik": 717,
    "havuz_az": 0,
    "havuz_disi": 61125,
    "tekil": 189165,
    "olcum_r15": 9808,
    "kova_yok": 346,
    "donem": {
     "acik": 8853,
     "birikimli": 1006,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 13621,
   "girdi": 13621,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 18,
   "giris_gec": 0,
   "likidite_alt20": 2075,
   "bolunme_gecmis": 6,
   "evren_once": 0,
   "gecmis_eksik": 7,
   "havuz_az": 0,
   "havuz_disi": 2088,
   "tekil": 6531,
   "y1_olay": 4984,
   "F_KT02": 99,
   "F_KT03": 4326,
   "F_KT04": 2446,
   "F_KT05": 4639,
   "F_KT06": 3102,
   "F_KT07": 42,
   "sure_sn": 43.3
  },
  "MOM": {
   "sinyal": 46612,
   "ana": 7368,
   "U": 3723,
   "A": 3645,
   "son_tarih": "2023-05-31",
   "pk": {
    "girdi": 46612,
    "olay_havuz": 36862,
    "U": 3723,
    "A": 3645,
    "ana": 7368
   }
  },
  "BOFA": {
   "hisse": 576,
   "kurulum": 33,
   "son": "2023-06-30"
  },
  "DS": {
   "girdi": 53297,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 24,
   "giris_gec": 0,
   "likidite_alt20": 2889,
   "bolunme_gecmis": 822,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3729,
   "tekil": 0,
   "ds_gun": 53297,
   "havuz_gun": 49544,
   "ana": 4977,
   "F_KT08": 2026,
   "sure_sn": 29.3
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 7368,
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
    "olcum_r15": 7368,
    "kova_yok": 0,
    "donem": {
     "acik": 6832,
     "birikimli": 536
    }
   },
   "MOM|30": {
    "girdi": 7368,
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
    "tekil": 2886,
    "olcum_r15": 4429,
    "kova_yok": 0,
    "donem": {
     "acik": 4144,
     "birikimli": 338
    }
   },
   "MOM|45": {
    "girdi": 7368,
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
    "tekil": 3869,
    "olcum_r15": 3412,
    "kova_yok": 0,
    "donem": {
     "acik": 3230,
     "birikimli": 269
    }
   },
   "Y1|15": {
    "girdi": 4984,
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
    "olcum_r15": 4951,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 488
    }
   },
   "Y1|30": {
    "girdi": 4984,
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
    "olcum_r15": 4899,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 488
    }
   },
   "Y1|45": {
    "girdi": 4984,
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
    "olcum_r15": 4828,
    "kova_yok": 0,
    "donem": {
     "acik": 4496,
     "birikimli": 488
    }
   },
   "DS|15": {
    "girdi": 4977,
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
    "olcum_r15": 4944,
    "kova_yok": 0,
    "donem": {
     "acik": 4562,
     "dis": 259,
     "birikimli": 156
    }
   },
   "DS|30": {
    "girdi": 4977,
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
    "tekil": 1977,
    "olcum_r15": 2965,
    "kova_yok": 0,
    "donem": {
     "acik": 2741,
     "dis": 163,
     "birikimli": 96
    }
   },
   "DS|45": {
    "girdi": 4977,
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
    "tekil": 2627,
    "olcum_r15": 2312,
    "kova_yok": 0,
    "donem": {
     "acik": 2148,
     "dis": 129,
     "birikimli": 73
    }
   },
   "BOFA|15": {
    "girdi": 33,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20
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
| KT00 | + | ABD | 15 | 642 | 635 | 7 | 0 | -0.27 [-2.36; +1.69] | -0.81 | 0.484 | -2.54 | 0.6216 | 0.98 | +0.00 / 0.08 / False | False / False |
| KT00 | + | ABD | 30 | 378 | 306 | 2 | 70 | +0.58 [-1.69; +3.37] | -1.90 | 0.496 | -2.19 | 0.4299 | 0.32 | -0.06 / 0.00 / True | False / False |
| KT00 | + | ABD | 45 | 283 | 191 | 0 | 92 | -0.56 [-2.69; +1.10] | -3.24 | 0.473 | -3.85 | 0.6801 | 0.15 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 271 | 245 | 26 | 0 | -0.02 [-1.67; +0.97] | +0.43 | 0.505 | -1.18 | 0.5156 | 0.87 | -0.01 / 0.09 / False | False / False |
| KT00 | + | AVR | 30 | 172 | 133 | 14 | 25 | -0.80 [-3.16; +1.06] | +0.06 | 0.489 | -3.77 | 0.8420 | 0.40 | +0.02 / 0.00 / True | False / False |
| KT00 | + | AVR | 45 | 142 | 92 | 6 | 44 | -3.83 [-8.11; +1.29] | -3.11 | 0.412 | -9.92 | 0.8856 | 0.23 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 1127 | 1025 | 12 | 90 | +0.24 [-0.12; +0.54] | -0.13 | 0.513 | -0.06 | 0.0899 | 1.00 | +0.02 / 0.05 / True | False / False |
| KT01 | + | ABD | 30 | 1127 | 878 | 9 | 240 | +0.40 [-0.18; +1.15] | -0.54 | 0.509 | -0.23 | 0.1534 | 0.77 | +0.02 / 0.00 / True | False / False |
| KT01 | + | ABD | 45 | 1127 | 698 | 9 | 420 | -0.41 [-1.07; +0.90] | -1.02 | 0.490 | -0.84 | 0.8092 | 0.49 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 488 | 431 | 24 | 33 | -0.07 [-0.91; +0.62] | -0.08 | 0.498 | -1.03 | 0.5643 | 0.99 | -0.04 / 0.07 / True | False / False |
| KT01 | + | AVR | 30 | 488 | 386 | 17 | 85 | +0.74 [+0.23; +1.18] | +0.41 | 0.525 | +0.16 | 0.0623 | 0.87 | -0.03 / 0.06 / True | True / False |
| KT01 | + | AVR | 45 | 488 | 322 | 10 | 156 | +0.21 [-0.42; +0.54] | -0.04 | 0.502 | -0.62 | 0.3687 | 0.72 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 147 | 109 | 20 | 18 | -0.38 [-6.15; +1.39] | -1.80 | 0.480 | -7.06 | 0.6573 | 0.46 | -0.04 / 0.00 / True | False / False |
| KT01 | + | BIST | 30 | 147 | 61 | 15 | 71 | -0.98 [-4.58; +5.56] | -3.30 | 0.481 | -4.91 | 0.7461 | 0.11 | -0.04 / 0.00 / True | False / False |
| KT01 | + | BIST | 45 | 147 | 49 | 13 | 85 | -0.91 [-9.38; +2.56] | -2.01 | 0.485 | - | 0.7443 | 0.07 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 92 | 88 | 0 | 4 | +1.09 [+0.22; +2.12] | -0.02 | 0.533 | +0.08 | 0.0484 | 0.29 | +0.05 / 0.00 / True | False / False |
| KT02 | + | ABD | 30 | 92 | 60 | 0 | 32 | +2.29 [+0.92; +4.20] | +1.74 | 0.579 | +1.27 | 0.0608 | 0.09 | +0.10 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 92 | 42 | 0 | 50 | -0.75 [-4.76; +1.30] | -0.69 | 0.512 | -1.83 | 0.7588 | 0.06 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 10 | 9 | 0 | 1 | +5.17 [-5.49; +10.66] | +8.70 | 0.762 | -5.94 | 0.1726 | 0.07 | +0.12 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 10 | 6 | 0 | 4 | +13.56 [+5.65; +19.08] | +15.10 | 0.870 | +3.28 | 0.0642 | 0.05 | +0.23 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 10 | 4 | 0 | 6 | +12.58 [-2.88; +28.04] | +16.29 | 0.743 | -10.75 | 0.1887 | 0.04 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 75 | 73 | 0 | 2 | +0.51 [-6.55; +1.97] | -1.08 | 0.505 | -10.11 | 0.3761 | 0.32 | +0.30 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 75 | 35 | 0 | 40 | -2.09 [-12.50; -1.20] | -3.97 | 0.458 | - | 1.0000 | 0.08 | +0.56 / 0.00 / False | False / False |
| KT02 | + | BIST | 45 | 75 | 26 | 0 | 49 | +0.39 [-11.10; +3.13] | -1.87 | 0.482 | - | 0.4948 | 0.05 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 985 | 899 | 8 | 78 | +0.19 [-0.10; +0.44] | -0.07 | 0.511 | -0.12 | 0.1104 | 1.00 | -0.01 / 0.08 / False | False / False |
| KT03 | + | ABD | 30 | 985 | 770 | 6 | 209 | +0.15 [-0.58; +1.01] | -0.64 | 0.502 | -0.40 | 0.4377 | 0.71 | -0.00 / 0.00 / True | False / False |
| KT03 | + | ABD | 45 | 985 | 616 | 6 | 363 | -0.47 [-1.13; +1.02] | -1.11 | 0.487 | -1.08 | 0.8176 | 0.43 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 416 | 367 | 20 | 29 | -0.09 [-1.26; +0.75] | -0.16 | 0.494 | -1.36 | 0.5412 | 0.97 | +0.00 / 0.11 / False | False / False |
| KT03 | + | AVR | 30 | 416 | 328 | 14 | 74 | +0.54 [-0.17; +1.15] | +0.24 | 0.514 | -0.35 | 0.1904 | 0.80 | -0.00 / 0.00 / True | False / False |
| KT03 | + | AVR | 45 | 416 | 272 | 8 | 136 | -0.22 [-0.90; +0.25] | -0.47 | 0.488 | -1.15 | 0.8770 | 0.64 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 138 | 102 | 19 | 17 | -0.43 [-6.05; +1.56] | -1.82 | 0.479 | -7.05 | 0.7181 | 0.44 | -0.15 / 0.00 / True | False / False |
| KT03 | + | BIST | 30 | 138 | 56 | 14 | 68 | -1.37 [-5.64; +5.56] | -3.83 | 0.469 | -6.33 | 0.8171 | 0.10 | -0.16 / 0.00 / True | False / False |
| KT03 | + | BIST | 45 | 138 | 45 | 13 | 80 | -1.37 [-9.54; +1.57] | -2.67 | 0.477 | - | 0.7489 | 0.06 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 474 | 435 | 4 | 35 | +0.47 [-0.40; +1.39] | +0.40 | 0.528 | -0.26 | 0.1764 | 0.90 | +0.00 / 0.04 / True | False / False |
| KT04 | + | ABD | 30 | 474 | 383 | 4 | 87 | -0.02 [-1.29; +1.51] | -0.44 | 0.510 | -1.28 | 0.5339 | 0.40 | +0.04 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 474 | 313 | 4 | 157 | -0.44 [-2.46; +2.68] | -0.66 | 0.489 | -3.36 | 0.6212 | 0.23 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 238 | 210 | 10 | 18 | -0.26 [-1.27; +0.63] | -0.27 | 0.493 | -1.33 | 0.7236 | 0.80 | +0.01 / 0.00 / True | False / False |
| KT04 | + | AVR | 30 | 238 | 182 | 7 | 49 | +0.05 [-0.22; +0.63] | +0.08 | 0.507 | -0.17 | 0.5116 | 0.53 | -0.05 / 0.00 / True | False / False |
| KT04 | + | AVR | 45 | 238 | 151 | 3 | 84 | -1.36 [-2.01; -0.21] | -1.52 | 0.459 | -1.78 | 0.9329 | 0.37 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 116 | 92 | 12 | 12 | +0.14 [-6.20; +2.40] | -1.67 | 0.497 | -8.02 | 0.3804 | 0.39 | +0.08 / 0.00 / True | False / False |
| KT04 | + | BIST | 30 | 116 | 50 | 9 | 57 | -1.18 [-6.40; +9.77] | -3.64 | 0.464 | -7.52 | 0.6916 | 0.10 | -0.08 / 0.00 / True | False / False |
| KT04 | + | BIST | 45 | 116 | 41 | 7 | 68 | -1.46 [-10.18; +1.69] | -2.01 | 0.475 | - | 0.7474 | 0.06 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 1115 | 1014 | 12 | 89 | +0.21 [-0.15; +0.51] | -0.14 | 0.512 | -0.10 | 0.1788 | 1.00 | -0.05 / 0.05 / True | False / False |
| KT05 | + | ABD | 30 | 1115 | 869 | 9 | 237 | +0.40 [-0.20; +1.30] | -0.63 | 0.509 | -0.26 | 0.1539 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT05 | + | ABD | 45 | 1115 | 689 | 9 | 417 | -0.40 [-1.06; +0.93] | -1.08 | 0.490 | -0.87 | 0.8151 | 0.48 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 479 | 426 | 21 | 32 | -0.03 [-0.85; +0.61] | -0.08 | 0.499 | -0.96 | 0.5403 | 0.99 | -0.02 / 0.04 / True | False / False |
| KT05 | + | AVR | 30 | 479 | 381 | 14 | 84 | +0.77 [+0.16; +1.24] | +0.40 | 0.526 | +0.14 | 0.0586 | 0.87 | +0.00 / 0.10 / False | False / False |
| KT05 | + | AVR | 45 | 479 | 318 | 7 | 154 | +0.25 [-0.48; +0.74] | -0.04 | 0.503 | -0.73 | 0.3690 | 0.72 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 145 | 107 | 20 | 18 | -0.55 [-6.15; +1.11] | -1.85 | 0.474 | -7.06 | 0.6492 | 0.46 | -0.02 / 0.00 / True | False / False |
| KT05 | + | BIST | 30 | 145 | 61 | 15 | 69 | -0.98 [-4.58; +8.46] | -3.30 | 0.481 | -4.91 | 0.7534 | 0.11 | -0.03 / 0.00 / True | False / False |
| KT05 | + | BIST | 45 | 145 | 49 | 13 | 83 | -0.91 [-9.38; +2.56] | -2.01 | 0.485 | - | 0.7476 | 0.07 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 608 | 539 | 3 | 66 | +0.25 [-0.22; +0.68] | -0.20 | 0.510 | -0.15 | 0.1843 | 0.95 | -0.06 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 608 | 448 | 2 | 158 | +0.47 [+0.01; +1.32] | -0.54 | 0.503 | -0.04 | 0.0937 | 0.46 | -0.05 / 0.00 / True | False / False |
| KT06 | + | ABD | 45 | 608 | 353 | 2 | 253 | -0.26 [-1.19; +0.40] | -0.93 | 0.483 | -0.77 | 0.7453 | 0.25 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 301 | 266 | 14 | 21 | -0.30 [-1.07; +0.37] | -0.59 | 0.479 | -1.14 | 0.7204 | 0.89 | -0.01 / 0.09 / False | False / False |
| KT06 | + | AVR | 30 | 301 | 238 | 10 | 53 | +0.81 [+0.44; +1.12] | +0.48 | 0.532 | +0.31 | 0.0314 | 0.65 | -0.00 / 0.00 / True | False / False |
| KT06 | + | AVR | 45 | 301 | 206 | 6 | 89 | -0.01 [-1.30; +0.54] | -0.06 | 0.493 | -2.81 | 0.5595 | 0.50 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 65 | 44 | 12 | 9 | +0.62 [-8.14; +3.44] | -1.27 | 0.513 | -11.40 | 0.3658 | 0.19 | -0.04 / 0.00 / True | False / False |
| KT06 | + | BIST | 30 | 65 | 23 | 9 | 33 | -1.25 [-7.98; +7.19] | -1.66 | 0.505 | -9.57 | 0.7548 | 0.06 | +0.33 / 0.00 / True | False / False |
| KT06 | + | BIST | 45 | 65 | 15 | 7 | 43 | +2.85 [-14.97; +9.95] | -0.55 | 0.528 | - | 0.3763 | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 31 | 30 | 0 | 1 | +0.64 [-2.28; +1.96] | +0.07 | 0.522 | -4.48 | 0.3131 | 0.12 | -0.05 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 31 | 21 | 0 | 10 | -1.65 [-5.10; +1.35] | -1.54 | 0.553 | - | 0.7607 | 0.05 | -0.00 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 31 | 14 | 0 | 17 | -8.52 [-13.40; -5.81] | -8.75 | 0.421 | - | 1.0000 | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 6 | 5 | 0 | 1 | +1.04 [-13.26; +10.57] | +3.61 | 0.586 | -15.91 | 0.5064 | 0.05 | -0.17 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 6 | 3 | 0 | 3 | +10.38 [-3.77; +17.45] | +10.31 | 0.740 | - | 0.4963 | 0.04 | -0.12 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 6 | 2 | 0 | 4 | -2.88 [-10.75; +5.00] | -2.88 | 0.486 | - | 0.7467 | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 56 | 55 | 0 | 1 | +1.28 [-5.48; +3.32] | -1.08 | 0.530 | -0.41 | 0.4328 | 0.24 | +0.20 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 56 | 23 | 0 | 33 | -3.88 [-15.49; -2.78] | -5.16 | 0.397 | - | 1.0000 | 0.06 | -0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 56 | 17 | 0 | 39 | -3.12 [-18.36; -1.08] | -5.88 | 0.407 | - | 1.0000 | 0.04 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 349 | 329 | 0 | 20 | +0.19 [-2.07; +2.18] | -1.24 | 0.492 | -1.24 | 0.5924 | 0.80 | +0.03 / 0.06 / True | False / False |
| KT08 | - | ABD | 30 | 242 | 208 | 0 | 34 | +0.67 [-2.86; +3.38] | -2.40 | 0.494 | -1.66 | 0.6459 | 0.22 | +0.10 / 0.00 / True | False / False |
| KT08 | - | ABD | 45 | 210 | 122 | 0 | 88 | -1.22 [-3.37; +2.57] | -7.44 | 0.458 | -3.42 | 0.1892 | 0.10 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 57 | 35 | 1 | 21 | +2.40 [-0.63; +8.58] | +2.02 | 0.574 | -0.40 | 0.8461 | 0.18 | -0.18 / 0.00 / True | False / False |
| KT08 | - | AVR | 30 | 41 | 19 | 1 | 21 | -1.54 [-5.10; +4.19] | +0.41 | 0.500 | -4.55 | 0.3066 | 0.08 | -0.04 / 0.00 / True | False / False |
| KT08 | - | AVR | 45 | 40 | 14 | 1 | 25 | -1.19 [-3.13; +7.80] | -3.17 | 0.457 | -2.24 | 0.3104 | 0.06 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 263 | 257 | 3 | 3 | +0.67 [-0.85; +1.45] | -0.09 | 0.530 | -0.77 | 0.7153 | 0.87 | +0.12 / 0.06 / True | False / False |
| KT08 | - | BIST | 30 | 146 | 125 | 2 | 19 | +1.05 [-0.03; +1.93] | -0.66 | 0.537 | +0.27 | 0.8740 | 0.18 | +0.39 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 86 | 34 | 1 | 51 | +1.28 [-0.40; +4.95] | +0.12 | 0.565 | - | 0.8777 | 0.06 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 15 | 15 | 0 | 0 | +2.76 [-10.62; +13.45] | +1.25 | 0.577 | -9.75 | 0.3723 | 0.08 | +0.03 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 15 | 13 | 0 | 2 | +9.51 [-0.39; +23.76] | +2.25 | 0.609 | -4.97 | 0.1238 | 0.04 | +0.24 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 15 | 13 | 0 | 2 | +26.89 [-2.66; +61.36] | +23.75 | 0.624 | -12.92 | 0.1828 | 0.04 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 1 | 1 | 0 | 0 | +38.52 [+38.52; +38.52] | +38.52 | 1.000 | - | 0.4971 | 0.04 | -0.46 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 1 | 1 | 0 | 0 | +44.15 [+44.15; +44.15] | +44.15 | 1.000 | - | 0.4971 | 0.03 | -0.43 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 1 | 1 | 0 | 0 | +13.32 [+13.32; +13.32] | +13.32 | 0.909 | - | 0.4971 | 0.03 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 1959 | 1709 | 15 | 235 | -0.36 [-0.80; -0.06] | -1.07 | 0.480 | -0.80 | 1.0000 | 1.00 | -0.02 / 0.06 / True | False / True |
| KT10 | + | ABD | 30 | 1182 | 895 | 11 | 276 | -0.63 [-2.18; +0.48] | -1.69 | 0.479 | -2.60 | 0.8080 | 0.78 | +0.00 / 0.00 / True | False / False |
| KT10 | + | ABD | 45 | 1006 | 681 | 6 | 319 | +0.06 [-2.05; +1.62] | -2.21 | 0.483 | -3.39 | 0.4999 | 0.48 | - / - / False | False / False |

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
| KT01 | + | ABD | 45 | 524 | 517 | 7 | 0 | -0.29 [-1.27; +1.65] | -0.93 | 0.493 | - | - | 0.37 | - / - / False | False / False |
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
| KT03 | + | ABD | 45 | 459 | 454 | 5 | 0 | -0.35 [-1.30; +1.84] | -0.96 | 0.490 | - | - | 0.32 | - / - / False | False / False |
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
| KT06 | + | ABD | 45 | 241 | 240 | 1 | 0 | -0.43 [-1.58; +0.79] | -0.69 | 0.490 | - | - | 0.18 | - / - / False | False / False |
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
| KT08 | - | BIST | 15 | 52 | 50 | 2 | 0 | +0.47 [-1.92; +1.36] | +0.24 | 0.562 | - | - | 0.22 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 35 | 34 | 1 | 0 | -0.03 [-0.88; +0.27] | -3.57 | 0.507 | - | - | 0.08 | - / - / False | False / False |
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
| KT00 | + | ABD | 30 | 202 | 132 | 0 | 70 | +3.19 [+0.91; +6.28] | +0.47 | 0.553 | - | - | 0.15 | - / - / False | False / False |
| KT00 | + | ABD | 45 | 149 | 57 | 0 | 92 | +1.58 [+1.58; +1.58] | -3.39 | 0.479 | - | - | 0.06 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 137 | 130 | 7 | 0 | +1.01 [+0.70; +1.21] | +1.17 | 0.556 | - | - | 0.58 | - / - / False | False / False |
| KT00 | + | AVR | 30 | 81 | 55 | 1 | 25 | +1.36 [+0.06; +2.17] | +1.56 | 0.540 | - | - | 0.18 | - / - / False | False / False |
| KT00 | + | AVR | 45 | 62 | 18 | 0 | 44 | -1.47 [-1.47; -1.47] | -0.25 | 0.469 | - | - | 0.07 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 603 | 508 | 5 | 90 | +0.28 [-0.02; +0.92] | -0.26 | 0.512 | - | - | 0.94 | - / - / False | False / False |
| KT01 | + | ABD | 30 | 603 | 361 | 2 | 240 | +0.45 [+0.14; +0.83] | -0.63 | 0.510 | - | - | 0.37 | - / - / False | False / False |
| KT01 | + | ABD | 45 | 603 | 181 | 2 | 420 | -0.75 [-0.75; -0.75] | -1.81 | 0.482 | - | - | 0.14 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 202 | 154 | 15 | 33 | +0.58 [-0.53; +0.80] | +0.27 | 0.526 | - | - | 0.66 | - / - / False | False / False |
| KT01 | + | AVR | 30 | 202 | 109 | 8 | 85 | +1.32 [+1.18; +1.46] | +0.14 | 0.541 | - | - | 0.33 | - / - / False | False / False |
| KT01 | + | AVR | 45 | 202 | 45 | 1 | 156 | -0.16 [-0.16; -0.16] | -1.78 | 0.455 | - | - | 0.12 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 124 | 91 | 15 | 18 | +0.72 [-3.69; +1.78] | -0.88 | 0.524 | - | - | 0.39 | - / - / False | False / False |
| KT01 | + | BIST | 30 | 124 | 43 | 10 | 71 | -1.16 [-3.12; -1.02] | -3.97 | 0.470 | - | - | 0.09 | - / - / False | False / False |
| KT01 | + | BIST | 45 | 124 | 31 | 8 | 85 | +2.56 [+2.56; +2.56] | -1.53 | 0.547 | - | - | 0.05 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 68 | 64 | 0 | 4 | +1.32 [+0.17; +2.68] | -0.10 | 0.529 | - | - | 0.22 | - / - / False | False / False |
| KT02 | + | ABD | 30 | 68 | 36 | 0 | 32 | +3.03 [+1.41; +4.66] | +5.72 | 0.607 | - | - | 0.07 | - / - / False | False / False |
| KT02 | + | ABD | 45 | 68 | 18 | 0 | 50 | +1.06 [+1.06; +1.06] | -0.03 | 0.568 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 7 | 6 | 0 | 1 | +7.06 [-10.61; +11.03] | +8.52 | 0.810 | - | - | 0.06 | - / - / False | False / False |
| KT02 | + | AVR | 30 | 7 | 3 | 0 | 4 | +15.08 [+10.33; +17.45] | +10.33 | 0.949 | - | - | 0.04 | - / - / False | False / False |
| KT02 | + | AVR | 45 | 7 | 1 | 0 | 6 | +5.00 [+5.00; +5.00] | +5.00 | 0.846 | - | - | 0.03 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 70 | 68 | 0 | 2 | +1.29 [-2.10; +2.40] | -0.36 | 0.540 | - | - | 0.29 | - / - / False | False / False |
| KT02 | + | BIST | 30 | 70 | 30 | 0 | 40 | -1.58 [-12.50; -1.20] | -4.15 | 0.465 | - | - | 0.07 | - / - / False | False / False |
| KT02 | + | BIST | 45 | 70 | 21 | 0 | 49 | +3.13 [+3.13; +3.13] | -1.71 | 0.535 | - | - | 0.05 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 526 | 445 | 3 | 78 | +0.15 [-0.06; +0.71] | -0.38 | 0.505 | - | - | 0.91 | - / - / False | False / False |
| KT03 | + | ABD | 30 | 526 | 316 | 1 | 209 | -0.00 [-0.15; +0.19] | -0.65 | 0.498 | - | - | 0.33 | - / - / False | False / False |
| KT03 | + | ABD | 45 | 526 | 162 | 1 | 363 | -0.79 [-0.79; -0.79] | -1.78 | 0.480 | - | - | 0.13 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 174 | 132 | 13 | 29 | +0.61 [-0.85; +1.05] | +0.55 | 0.527 | - | - | 0.59 | - / - / False | False / False |
| KT03 | + | AVR | 30 | 174 | 93 | 7 | 74 | +1.39 [+0.94; +1.77] | -0.10 | 0.537 | - | - | 0.29 | - / - / False | False / False |
| KT03 | + | AVR | 45 | 174 | 37 | 1 | 136 | -0.04 [-0.04; -0.04] | -3.30 | 0.459 | - | - | 0.11 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 117 | 86 | 14 | 17 | +0.56 [-3.69; +2.00] | -1.01 | 0.515 | - | - | 0.37 | - / - / False | False / False |
| KT03 | + | BIST | 30 | 117 | 40 | 9 | 68 | -1.52 [-3.12; -1.39] | -4.05 | 0.460 | - | - | 0.08 | - / - / False | False / False |
| KT03 | + | BIST | 45 | 117 | 29 | 8 | 80 | +1.57 [+1.57; +1.57] | -1.53 | 0.530 | - | - | 0.05 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 241 | 205 | 1 | 35 | +0.75 [-1.04; +2.79] | +0.42 | 0.533 | - | - | 0.59 | - / - / False | False / False |
| KT04 | + | ABD | 30 | 241 | 153 | 1 | 87 | -0.94 [-2.06; +0.55] | -0.87 | 0.490 | - | - | 0.17 | - / - / False | False / False |
| KT04 | + | ABD | 45 | 241 | 83 | 1 | 157 | -3.36 [-3.36; -3.36] | -5.50 | 0.440 | - | - | 0.08 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 111 | 85 | 8 | 18 | +0.49 [-0.55; +1.51] | +0.46 | 0.539 | - | - | 0.40 | - / - / False | False / False |
| KT04 | + | AVR | 30 | 111 | 57 | 5 | 49 | +0.57 [-0.21; +1.18] | -0.10 | 0.520 | - | - | 0.18 | - / - / False | False / False |
| KT04 | + | AVR | 45 | 111 | 26 | 1 | 84 | -1.84 [-1.84; -1.84] | -1.65 | 0.428 | - | - | 0.08 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 98 | 77 | 9 | 12 | +1.47 [-2.48; +2.91] | -0.33 | 0.549 | - | - | 0.33 | - / - / False | False / False |
| KT04 | + | BIST | 30 | 98 | 35 | 6 | 57 | -1.07 [-1.24; +4.79] | -3.97 | 0.464 | - | - | 0.08 | - / - / False | False / False |
| KT04 | + | BIST | 45 | 98 | 26 | 4 | 68 | +1.69 [+1.69; +1.69] | -0.59 | 0.540 | - | - | 0.05 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 597 | 503 | 5 | 89 | +0.27 [+0.01; +0.88] | -0.26 | 0.512 | - | - | 0.94 | - / - / False | False / False |
| KT05 | + | ABD | 30 | 597 | 358 | 2 | 237 | +0.48 [+0.18; +0.83] | -0.64 | 0.511 | - | - | 0.37 | - / - / False | False / False |
| KT05 | + | ABD | 45 | 597 | 178 | 2 | 417 | -0.66 [-0.66; -0.66] | -1.78 | 0.484 | - | - | 0.14 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 200 | 153 | 15 | 32 | +0.51 [-0.53; +0.78] | +0.25 | 0.523 | - | - | 0.66 | - / - / False | False / False |
| KT05 | + | AVR | 30 | 200 | 108 | 8 | 84 | +1.27 [+1.18; +1.36] | +0.08 | 0.538 | - | - | 0.33 | - / - / False | False / False |
| KT05 | + | AVR | 45 | 200 | 45 | 1 | 154 | -0.16 [-0.16; -0.16] | -1.78 | 0.455 | - | - | 0.12 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 122 | 89 | 15 | 18 | +0.54 [-3.69; +1.46] | -0.95 | 0.518 | - | - | 0.38 | - / - / False | False / False |
| KT05 | + | BIST | 30 | 122 | 43 | 10 | 69 | -1.16 [-3.12; -1.02] | -3.97 | 0.470 | - | - | 0.09 | - / - / False | False / False |
| KT05 | + | BIST | 45 | 122 | 31 | 8 | 83 | +2.56 [+2.56; +2.56] | -1.53 | 0.547 | - | - | 0.05 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 367 | 299 | 2 | 66 | +0.09 [-0.72; +1.02] | -0.61 | 0.499 | - | - | 0.76 | - / - / False | False / False |
| KT06 | + | ABD | 30 | 367 | 208 | 1 | 158 | +0.17 [+0.02; +0.40] | -1.03 | 0.485 | - | - | 0.22 | - / - / False | False / False |
| KT06 | + | ABD | 45 | 367 | 113 | 1 | 253 | +0.10 [+0.10; +0.10] | -2.20 | 0.469 | - | - | 0.10 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 117 | 87 | 9 | 21 | -0.26 [-1.20; +0.35] | -1.17 | 0.466 | - | - | 0.41 | - / - / False | False / False |
| KT06 | + | AVR | 30 | 117 | 59 | 5 | 53 | +0.76 [+0.11; +1.47] | -0.59 | 0.501 | - | - | 0.19 | - / - / False | False / False |
| KT06 | + | AVR | 45 | 117 | 27 | 1 | 89 | -2.81 [-2.81; -2.81] | -3.81 | 0.367 | - | - | 0.09 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 56 | 38 | 9 | 9 | +2.52 [+0.80; +21.00] | -0.50 | 0.573 | - | - | 0.17 | - / - / False | False / False |
| KT06 | + | BIST | 30 | 56 | 17 | 6 | 33 | -0.80 [-1.66; -0.75] | -1.66 | 0.500 | - | - | 0.06 | - / - / False | False / False |
| KT06 | + | BIST | 45 | 56 | 9 | 4 | 43 | +9.19 [+9.19; +9.19] | +4.55 | 0.634 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 22 | 21 | 0 | 1 | +0.42 [-4.48; +2.07] | +0.40 | 0.518 | - | - | 0.10 | - / - / False | False / False |
| KT07 | + | ABD | 30 | 22 | 12 | 0 | 10 | -3.91 [-5.10; -2.25] | -1.79 | 0.551 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | ABD | 45 | 22 | 5 | 0 | 17 | -13.40 [-13.40; -13.40] | -8.81 | 0.423 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 5 | 4 | 0 | 1 | +5.27 [-10.61; +11.03] | +6.63 | 0.732 | - | - | 0.05 | - / - / False | False / False |
| KT07 | + | AVR | 30 | 5 | 2 | 0 | 3 | +17.45 [+17.45; +17.45] | +17.45 | 0.923 | - | - | 0.04 | - / - / False | False / False |
| KT07 | + | AVR | 45 | 5 | 1 | 0 | 4 | +5.00 [+5.00; +5.00] | +5.00 | 0.846 | - | - | 0.03 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 54 | 53 | 0 | 1 | +1.84 [-0.41; +3.66] | -0.78 | 0.550 | - | - | 0.23 | - / - / False | False / False |
| KT07 | + | BIST | 30 | 54 | 21 | 0 | 33 | -2.78 [-2.78; -2.78] | -4.33 | 0.431 | - | - | 0.06 | - / - / False | False / False |
| KT07 | + | BIST | 45 | 54 | 15 | 0 | 39 | -1.08 [-1.08; -1.08] | -4.16 | 0.456 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 212 | 192 | 0 | 20 | -1.00 [-3.51; +3.80] | -1.79 | 0.484 | - | - | 0.57 | - / - / False | False / False |
| KT08 | - | ABD | 30 | 141 | 107 | 0 | 34 | -1.66 [-3.91; -0.21] | -3.55 | 0.474 | - | - | 0.13 | - / - / False | False / False |
| KT08 | - | ABD | 45 | 113 | 25 | 0 | 88 | -3.42 [-3.42; -3.42] | -8.30 | 0.437 | - | - | 0.05 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 42 | 21 | 0 | 21 | +2.39 [-1.93; +14.27] | +2.67 | 0.547 | - | - | 0.12 | - / - / False | False / False |
| KT08 | - | AVR | 30 | 30 | 8 | 1 | 21 | -3.95 [-8.40; +0.50] | -5.32 | 0.412 | - | - | 0.05 | - / - / False | False / False |
| KT08 | - | AVR | 45 | 28 | 3 | 0 | 25 | -4.03 [-4.03; -4.03] | -6.19 | 0.473 | - | - | 0.04 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 211 | 207 | 1 | 3 | +0.72 [-0.57; +1.48] | -0.32 | 0.522 | - | - | 0.78 | - / - / False | False / False |
| KT08 | - | BIST | 30 | 111 | 91 | 1 | 19 | +1.45 [+1.03; +2.45] | +0.02 | 0.548 | - | - | 0.14 | - / - / False | False / False |
| KT08 | - | BIST | 45 | 71 | 19 | 1 | 51 | +0.36 [+0.36; +0.36] | -0.35 | 0.554 | - | - | 0.05 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 6 | 6 | 0 | 0 | -9.75 [-24.09; -2.58] | -9.96 | 0.355 | - | - | 0.05 | - / - / False | False / False |
| KT09 | + | ABD | 30 | 6 | 4 | 0 | 2 | +9.91 [+9.91; +9.91] | +4.18 | 0.628 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | ABD | 45 | 6 | 4 | 0 | 2 | +60.98 [+60.98; +60.98] | +70.84 | 0.753 | - | - | 0.03 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | AVR | 30 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT09 | + | AVR | 45 | 0 | 0 | 0 | 0 | - [-; -] | - | - | - | - | - | - / - / False | False / False |
| KT10 | + | ABD | 15 | 953 | 716 | 2 | 235 | -0.80 [-1.12; -0.28] | -1.67 | 0.465 | - | - | 0.99 | - / - / False | False / False |
| KT10 | + | ABD | 30 | 511 | 234 | 1 | 276 | -2.60 [-3.24; -1.84] | -3.64 | 0.424 | - | - | 0.25 | - / - / False | False / False |
| KT10 | + | ABD | 45 | 525 | 206 | 0 | 319 | +1.75 [+1.75; +1.75] | -1.29 | 0.504 | - | - | 0.15 | - / - / False | False / False |

FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok.
