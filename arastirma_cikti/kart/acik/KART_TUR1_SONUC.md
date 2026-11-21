# KART TURU 1 — sonuç (açık kesik 2022-12-31, açılmış blok 0: yok)

KART_TUR1 v1.0 (2026-11-21): 11 kart (KT00 kontrol + KT01-KT10), CETVEL2 v2.2 R15 / R30 karar, R45 bilgi, KASA yürüyen ileri test

Bakış: YOK (açık veri kuru koşusu). KASA kapısı: kesik 2022-12-31, dosyalar en geç {'/tmp/kasa/acik/V_ABD.pkl': '2022-12-30', '/tmp/kasa/acik/V_AVR.pkl': '2022-12-30', '/tmp/kasa/acik/V_BIST.pkl': '2022-12-30', '/tmp/kasa/acik/k34_yahoo.pkl': '2022-12-30'}. Çıktı en geç tarih: {'kt_satir.csv.gz': '2022-12-30', 'olculen_son_giris': {'15': '2022-12-12', '30': '2022-11-18', '45': '2022-10-28'}}.
Ön kayıt kapısı: {'not': 'blok yok (açık veri kuru koşusu); ön kayıt kapısı aranmaz'}.
Yeniden üretim (K11): TUTTU [{'hucre': 'KT01 ABD R15 acik', 'n': 8487, 'fark': -0.0016504653145220996, 'sira': 0.49607712023658324, 'esit': True}, {'hucre': 'KT08 AVR R30 acik', 'n': 1356, 'fark': 0.004238056063584487, 'sira': 0.5128700166464286, 'esit': True}].
Prefix (K2): Y1|ABD 8/8, D9|ABD 8/8, MOM|ABD 8/8, BOFA|ABD 8/8, DS|ABD 8/8, Y1|AVR 8/8, MOM|AVR 8/8, BOFA|AVR 8/8, DS|AVR 8/8, Y1|BIST 8/8, DS|BIST 8/8.

## Kart etiketleri

| Kart | Etiket | Neden | BH p |
|---|---|---|---|
| KT00 | KONTROL (blok yok) | blok yok (yalnız açık veri) | - |
| KT01 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT02 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT03 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT04 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT05 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT06 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT07 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT08 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT09 | BİLGİ (blok yok; yalnız açık veri) |  | - |
| KT10 | BİLGİ (blok yok; yalnız açık veri) |  | - |

## Huni (olay sayıları; getirisiz)

```
{
 "ABD": {
  "Y1": {
   "sinyal": 22667,
   "girdi": 22667,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 4,
   "giris_gec": 0,
   "likidite_alt20": 2933,
   "bolunme_gecmis": 25,
   "evren_once": 0,
   "gecmis_eksik": 2,
   "havuz_az": 0,
   "havuz_disi": 2960,
   "tekil": 11017,
   "y1_olay": 8686,
   "F_KT02": 346,
   "F_KT03": 7614,
   "F_KT04": 3823,
   "F_KT05": 8245,
   "F_KT06": 4953,
   "F_KT07": 151,
   "sure_sn": 72.8
  },
  "D9": {
   "durum": 476557,
   "c": 234210,
   "sure_sn": 33.3
  },
  "MOM": {
   "sinyal": 83606,
   "ana": 13367,
   "U": 6718,
   "A": 6649,
   "son_tarih": "2022-11-30",
   "pk": {
    "girdi": 83606,
    "olay_havuz": 66837,
    "U": 6718,
    "A": 6649,
    "ana": 13367
   }
  },
  "BOFA": {
   "hisse": 1359,
   "kurulum": 508,
   "son": "2022-12-30"
  },
  "DS": {
   "girdi": 197352,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 236,
   "giris_gec": 0,
   "likidite_alt20": 45831,
   "bolunme_gecmis": 3532,
   "evren_once": 0,
   "gecmis_eksik": 5,
   "havuz_az": 0,
   "havuz_disi": 49368,
   "tekil": 0,
   "ds_gun": 197352,
   "havuz_gun": 147748,
   "ana": 14301,
   "F_KT08": 4936,
   "sure_sn": 73.0
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 13367,
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
    "olcum_r15": 13367,
    "kova_yok": 0,
    "donem": {
     "acik": 13367
    }
   },
   "MOM|30": {
    "girdi": 13367,
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
    "tekil": 5468,
    "olcum_r15": 7785,
    "kova_yok": 0,
    "donem": {
     "acik": 7899
    }
   },
   "MOM|45": {
    "girdi": 13367,
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
    "tekil": 7388,
    "olcum_r15": 5818,
    "kova_yok": 0,
    "donem": {
     "acik": 5979
    }
   },
   "Y1|15": {
    "girdi": 8686,
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
    "olcum_r15": 8605,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "Y1|30": {
    "girdi": 8686,
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
    "olcum_r15": 8510,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "Y1|45": {
    "girdi": 8686,
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
    "olcum_r15": 8433,
    "kova_yok": 0,
    "donem": {
     "acik": 8686
    }
   },
   "DS|15": {
    "girdi": 14301,
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
    "olcum_r15": 14087,
    "kova_yok": 0,
    "donem": {
     "acik": 14060,
     "dis": 241
    }
   },
   "DS|30": {
    "girdi": 14301,
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
    "tekil": 5840,
    "olcum_r15": 8239,
    "kova_yok": 0,
    "donem": {
     "acik": 8319,
     "dis": 142
    }
   },
   "DS|45": {
    "girdi": 14301,
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
    "tekil": 7760,
    "olcum_r15": 6287,
    "kova_yok": 0,
    "donem": {
     "acik": 6399,
     "dis": 142
    }
   },
   "BOFA|15": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 166,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "BOFA|30": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 159,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "BOFA|45": {
    "girdi": 508,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 8,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 310,
    "bolunme_gecmis": 20,
    "evren_once": 0,
    "gecmis_eksik": 3,
    "havuz_az": 0,
    "havuz_disi": 333,
    "tekil": 0,
    "olcum_r15": 152,
    "kova_yok": 0,
    "donem": {
     "acik": 167
    }
   },
   "D9|15": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 161888,
    "olcum_r15": 18324,
    "kova_yok": 556,
    "donem": {
     "acik": 18011,
     "dis": 484
    }
   },
   "D9|30": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 168823,
    "olcum_r15": 11383,
    "kova_yok": 372,
    "donem": {
     "acik": 11238,
     "dis": 322
    }
   },
   "D9|45": {
    "girdi": 234210,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 115,
    "giris_gec": 17,
    "likidite_alt20": 51154,
    "bolunme_gecmis": 1916,
    "evren_once": 0,
    "gecmis_eksik": 625,
    "havuz_az": 0,
    "havuz_disi": 53695,
    "tekil": 171264,
    "olcum_r15": 8908,
    "kova_yok": 344,
    "donem": {
     "acik": 8851,
     "dis": 268
    }
   }
  }
 },
 "AVR": {
  "Y1": {
   "sinyal": 12174,
   "girdi": 12174,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 2,
   "giris_gec": 0,
   "likidite_alt20": 1892,
   "bolunme_gecmis": 4,
   "evren_once": 0,
   "gecmis_eksik": 6,
   "havuz_az": 0,
   "havuz_disi": 1902,
   "tekil": 5773,
   "y1_olay": 4497,
   "F_KT02": 89,
   "F_KT03": 3911,
   "F_KT04": 2208,
   "F_KT05": 4161,
   "F_KT06": 2802,
   "F_KT07": 36,
   "sure_sn": 42.2
  },
  "MOM": {
   "sinyal": 43186,
   "ana": 6832,
   "U": 3452,
   "A": 3380,
   "son_tarih": "2022-11-30",
   "pk": {
    "girdi": 43186,
    "olay_havuz": 34183,
    "U": 3452,
    "A": 3380,
    "ana": 6832
   }
  },
  "BOFA": {
   "hisse": 575,
   "kurulum": 32,
   "son": "2022-12-30"
  },
  "DS": {
   "girdi": 51510,
   "sembol_yok": 0,
   "sinyal_bar_gecersiz": 0,
   "giris_yok": 35,
   "giris_gec": 0,
   "likidite_alt20": 2666,
   "bolunme_gecmis": 702,
   "evren_once": 0,
   "gecmis_eksik": 18,
   "havuz_az": 0,
   "havuz_disi": 3386,
   "tekil": 0,
   "ds_gun": 51510,
   "havuz_gun": 48089,
   "ana": 4821,
   "F_KT08": 1969,
   "sure_sn": 29.5
  },
  "cetvel": {
   "MOM|15": {
    "girdi": 6832,
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
    "olcum_r15": 6832,
    "kova_yok": 0,
    "donem": {
     "acik": 6832
    }
   },
   "MOM|30": {
    "girdi": 6832,
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
    "tekil": 2688,
    "olcum_r15": 4088,
    "kova_yok": 0,
    "donem": {
     "acik": 4144
    }
   },
   "MOM|45": {
    "girdi": 6832,
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
    "tekil": 3602,
    "olcum_r15": 3170,
    "kova_yok": 0,
    "donem": {
     "acik": 3230
    }
   },
   "Y1|15": {
    "girdi": 4497,
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
    "olcum_r15": 4456,
    "kova_yok": 0,
    "donem": {
     "acik": 4497
    }
   },
   "Y1|30": {
    "girdi": 4497,
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
    "olcum_r15": 4409,
    "kova_yok": 0,
    "donem": {
     "acik": 4497
    }
   },
   "Y1|45": {
    "girdi": 4497,
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
    "olcum_r15": 4352,
    "kova_yok": 0,
    "donem": {
     "acik": 4497
    }
   },
   "DS|15": {
    "girdi": 4821,
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
    "olcum_r15": 4777,
    "kova_yok": 0,
    "donem": {
     "acik": 4562,
     "dis": 259
    }
   },
   "DS|30": {
    "girdi": 4821,
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
    "tekil": 1917,
    "olcum_r15": 2854,
    "kova_yok": 0,
    "donem": {
     "acik": 2741,
     "dis": 163
    }
   },
   "DS|45": {
    "girdi": 4821,
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
    "tekil": 2544,
    "olcum_r15": 2219,
    "kova_yok": 0,
    "donem": {
     "acik": 2148,
     "dis": 129
    }
   },
   "BOFA|15": {
    "girdi": 32,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 9,
    "bolunme_gecmis": 3,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 12,
    "tekil": 0,
    "olcum_r15": 19,
    "kova_yok": 0,
    "donem": {
     "acik": 20
    }
   },
   "BOFA|30": {
    "girdi": 32,
    "sembol_yok": 0,
    "sinyal_bar_gecersiz": 0,
    "giris_yok": 0,
    "giris_gec": 0,
    "likidite_alt20": 9,
    "bolunme_gecmis": 3,
    "evren_once": 0,
    "gecmis_eksik": 0,
    "havuz_az": 0,
    "havuz_disi": 12,
    "tekil": 0,
    "olcum_r15": 19,
    "kova_yok": 0,
    "donem": {
     "acik":
```

## Hücre: acik

| Kart | Yön | Pazar | H | n bayrak | n | eşsiz | bekleyen | FARK puan [boot] | medyan | SIRA | L3O | p | güç | plasebo ort / pay / geçti | T+ / T- |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KT00 | + | ABD | 15 | 6718 | 6024 | 694 | 0 | +0.40 [-0.37; +1.14] | -0.13 | 0.502 | +0.04 | 0.1604 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT00 | + | ABD | 30 | 3948 | 3639 | 249 | 60 | +0.77 [-0.18; +1.75] | -0.63 | 0.503 | +0.35 | 0.0585 | 1.00 | -0.00 / 0.01 / True | False / False |
| KT00 | + | ABD | 45 | 2974 | 2716 | 172 | 86 | +1.07 [-0.07; +2.13] | -0.88 | 0.507 | +0.64 | 0.0380 | 0.99 | - / - / False | False / False |
| KT00 | + | AVR | 15 | 3452 | 2788 | 664 | 0 | +0.07 [-0.45; +0.57] | -0.12 | 0.499 | -0.11 | 0.3821 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT00 | + | AVR | 30 | 2104 | 1737 | 337 | 30 | -0.24 [-1.12; +0.58] | -0.58 | 0.489 | -0.60 | 0.7121 | 1.00 | -0.02 / 0.01 / True | False / False |
| KT00 | + | AVR | 45 | 1640 | 1351 | 261 | 28 | +0.43 [-0.52; +1.42] | +0.12 | 0.507 | +0.01 | 0.1983 | 1.00 | - / - / False | False / False |
| KT01 | + | ABD | 15 | 8686 | 8487 | 118 | 81 | -0.17 [-0.40; +0.07] | -0.18 | 0.496 | -0.27 | 0.9091 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | ABD | 30 | 8686 | 8394 | 116 | 176 | -0.25 [-0.58; +0.09] | -0.27 | 0.495 | -0.38 | 0.9183 | 1.00 | +0.01 / 0.01 / True | False / False |
| KT01 | + | ABD | 45 | 8686 | 8322 | 111 | 253 | -0.25 [-0.65; +0.15] | -0.44 | 0.496 | -0.39 | 0.8737 | 1.00 | - / - / False | False / False |
| KT01 | + | AVR | 15 | 4497 | 4177 | 279 | 41 | -0.02 [-0.23; +0.21] | -0.16 | 0.496 | -0.14 | 0.5787 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT01 | + | AVR | 30 | 4497 | 4134 | 275 | 88 | -0.16 [-0.48; +0.20] | -0.21 | 0.494 | -0.34 | 0.8096 | 1.00 | +0.01 / 0.03 / True | False / False |
| KT01 | + | AVR | 45 | 4497 | 4084 | 268 | 145 | -0.16 [-0.56; +0.27] | -0.40 | 0.494 | -0.36 | 0.7789 | 1.00 | - / - / False | False / False |
| KT01 | + | BIST | 15 | 2588 | 2171 | 400 | 17 | -0.81 [-1.30; -0.29] | -2.82 | 0.451 | -1.08 | 0.9975 | 1.00 | -0.01 / 0.03 / True | False / True |
| KT01 | + | BIST | 30 | 2588 | 2166 | 395 | 27 | -0.77 [-1.75; +0.30] | -3.43 | 0.475 | -1.25 | 0.9190 | 1.00 | -0.01 / 0.03 / True | False / False |
| KT01 | + | BIST | 45 | 2588 | 2144 | 387 | 57 | -0.82 [-2.07; +0.50] | -4.31 | 0.473 | -1.39 | 0.8909 | 0.93 | - / - / False | False / False |
| KT02 | + | ABD | 15 | 346 | 334 | 8 | 4 | -0.05 [-1.45; +1.38] | +0.17 | 0.507 | -0.57 | 0.5244 | 0.81 | -0.03 / 0.03 / True | False / False |
| KT02 | + | ABD | 30 | 346 | 331 | 8 | 7 | -1.20 [-6.73; +1.88] | +0.31 | 0.517 | -2.90 | 0.6395 | 0.34 | +0.08 / 0.00 / True | False / False |
| KT02 | + | ABD | 45 | 346 | 327 | 8 | 11 | -2.22 [-8.79; +1.58] | -0.27 | 0.500 | -4.07 | 0.7472 | 0.23 | - / - / False | False / False |
| KT02 | + | AVR | 15 | 89 | 78 | 11 | 0 | +0.49 [-1.51; +2.59] | +1.56 | 0.537 | -0.62 | 0.3264 | 0.37 | -0.03 / 0.00 / True | False / False |
| KT02 | + | AVR | 30 | 89 | 76 | 11 | 2 | +0.97 [-1.17; +3.41] | +1.05 | 0.519 | -0.39 | 0.2094 | 0.24 | -0.06 / 0.00 / True | False / False |
| KT02 | + | AVR | 45 | 89 | 73 | 11 | 5 | -0.28 [-3.73; +3.19] | -0.07 | 0.511 | -2.53 | 0.5570 | 0.19 | - / - / False | False / False |
| KT02 | + | BIST | 15 | 238 | 205 | 33 | 0 | -0.23 [-1.74; +1.62] | -2.69 | 0.445 | -1.16 | 0.5962 | 0.77 | -0.05 / 0.00 / True | False / False |
| KT02 | + | BIST | 30 | 238 | 205 | 33 | 0 | +0.02 [-2.21; +2.93] | -2.14 | 0.489 | -1.41 | 0.4923 | 0.28 | -0.04 / 0.00 / True | False / False |
| KT02 | + | BIST | 45 | 238 | 205 | 33 | 0 | +1.02 [-1.90; +4.20] | -2.80 | 0.500 | -0.70 | 0.2563 | 0.16 | - / - / False | False / False |
| KT03 | + | ABD | 15 | 7614 | 7445 | 102 | 67 | -0.20 [-0.44; +0.03] | -0.21 | 0.495 | -0.28 | 0.9438 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT03 | + | ABD | 30 | 7614 | 7361 | 101 | 152 | -0.25 [-0.61; +0.11] | -0.32 | 0.494 | -0.39 | 0.9148 | 1.00 | -0.14 / 0.03 / True | False / False |
| KT03 | + | ABD | 45 | 7614 | 7297 | 96 | 221 | -0.25 [-0.73; +0.18] | -0.50 | 0.496 | -0.39 | 0.8649 | 1.00 | - / - / False | False / False |
| KT03 | + | AVR | 15 | 3911 | 3622 | 249 | 40 | +0.03 [-0.19; +0.27] | -0.15 | 0.497 | -0.09 | 0.4064 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT03 | + | AVR | 30 | 3911 | 3586 | 247 | 78 | -0.13 [-0.48; +0.22] | -0.24 | 0.494 | -0.33 | 0.7614 | 1.00 | +0.01 / 0.07 / True | False / False |
| KT03 | + | AVR | 45 | 3911 | 3542 | 240 | 129 | -0.14 [-0.57; +0.27] | -0.47 | 0.493 | -0.35 | 0.7546 | 1.00 | - / - / False | False / False |
| KT03 | + | BIST | 15 | 2379 | 1999 | 366 | 14 | -0.64 [-1.18; -0.05] | -2.84 | 0.452 | -0.94 | 0.9861 | 1.00 | +0.02 / 0.02 / True | False / True |
| KT03 | + | BIST | 30 | 2379 | 1994 | 362 | 23 | -0.73 [-1.76; +0.37] | -3.49 | 0.475 | -1.25 | 0.8986 | 0.99 | +0.02 / 0.03 / True | False / False |
| KT03 | + | BIST | 45 | 2379 | 1973 | 355 | 51 | -0.64 [-1.91; +0.80] | -4.24 | 0.476 | -1.18 | 0.8113 | 0.91 | - / - / False | False / False |
| KT04 | + | ABD | 15 | 3823 | 3734 | 50 | 39 | -0.20 [-0.50; +0.16] | -0.06 | 0.498 | -0.36 | 0.8716 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT04 | + | ABD | 30 | 3823 | 3693 | 50 | 80 | -0.46 [-0.97; +0.05] | -0.30 | 0.494 | -0.62 | 0.9546 | 1.00 | +0.02 / 0.00 / True | False / False |
| KT04 | + | ABD | 45 | 3823 | 3651 | 45 | 127 | -0.65 [-1.27; -0.10] | -0.45 | 0.493 | -0.85 | 0.9852 | 1.00 | - / - / False | False / False |
| KT04 | + | AVR | 15 | 2208 | 2063 | 128 | 17 | -0.03 [-0.36; +0.32] | -0.19 | 0.491 | -0.20 | 0.5721 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT04 | + | AVR | 30 | 2208 | 2042 | 128 | 38 | -0.03 [-0.50; +0.48] | -0.21 | 0.496 | -0.28 | 0.5520 | 1.00 | +0.00 / 0.03 / True | False / False |
| KT04 | + | AVR | 45 | 2208 | 2027 | 125 | 56 | -0.04 [-0.57; +0.52] | -0.27 | 0.497 | -0.28 | 0.5533 | 1.00 | - / - / False | False / False |
| KT04 | + | BIST | 15 | 1572 | 1334 | 224 | 14 | -0.84 [-1.51; -0.13] | -2.93 | 0.450 | -1.18 | 0.9892 | 1.00 | +0.01 / 0.01 / True | False / True |
| KT04 | + | BIST | 30 | 1572 | 1330 | 221 | 21 | -0.70 [-1.80; +0.56] | -3.65 | 0.476 | -1.33 | 0.8724 | 0.95 | +0.02 / 0.02 / True | False / False |
| KT04 | + | BIST | 45 | 1572 | 1315 | 217 | 40 | -0.85 [-2.27; +0.76] | -4.41 | 0.470 | -1.49 | 0.8586 | 0.75 | - / - / False | False / False |
| KT05 | + | ABD | 15 | 8245 | 8062 | 106 | 77 | -0.18 [-0.41; +0.05] | -0.18 | 0.496 | -0.29 | 0.9155 | 1.00 | -0.01 / 0.06 / True | False / False |
| KT05 | + | ABD | 30 | 8245 | 7973 | 105 | 167 | -0.31 [-0.66; +0.04] | -0.32 | 0.493 | -0.45 | 0.9592 | 1.00 | -0.01 / 0.01 / True | False / False |
| KT05 | + | ABD | 45 | 8245 | 7908 | 102 | 235 | -0.34 [-0.79; +0.08] | -0.54 | 0.495 | -0.48 | 0.9337 | 1.00 | - / - / False | False / False |
| KT05 | + | AVR | 15 | 4161 | 3873 | 251 | 37 | +0.00 [-0.21; +0.24] | -0.13 | 0.497 | -0.12 | 0.4859 | 1.00 | +0.00 / 0.01 / True | False / False |
| KT05 | + | AVR | 30 | 4161 | 3832 | 249 | 80 | -0.14 [-0.48; +0.24] | -0.21 | 0.496 | -0.33 | 0.7619 | 1.00 | +0.00 / 0.02 / True | False / False |
| KT05 | + | AVR | 45 | 4161 | 3787 | 243 | 131 | -0.12 [-0.55; +0.30] | -0.34 | 0.496 | -0.33 | 0.6977 | 1.00 | - / - / False | False / False |
| KT05 | + | BIST | 15 | 2535 | 2125 | 394 | 16 | -0.83 [-1.35; -0.25] | -2.78 | 0.451 | -1.10 | 0.9978 | 1.00 | +0.01 / 0.03 / True | False / True |
| KT05 | + | BIST | 30 | 2535 | 2122 | 389 | 24 | -0.79 [-1.85; +0.34] | -3.51 | 0.475 | -1.27 | 0.9155 | 1.00 | +0.02 / 0.01 / True | False / False |
| KT05 | + | BIST | 45 | 2535 | 2100 | 381 | 54 | -0.87 [-2.10; +0.45] | -4.31 | 0.473 | -1.46 | 0.8926 | 0.92 | - / - / False | False / False |
| KT06 | + | ABD | 15 | 4953 | 4863 | 68 | 22 | -0.01 [-0.26; +0.26] | -0.08 | 0.500 | -0.13 | 0.5279 | 1.00 | -0.00 / 0.04 / True | False / False |
| KT06 | + | ABD | 30 | 4953 | 4808 | 66 | 79 | -0.06 [-0.41; +0.31] | -0.22 | 0.495 | -0.22 | 0.6409 | 1.00 | -0.03 / 0.03 / True | False / False |
| KT06 | + | ABD | 45 | 4953 | 4773 | 63 | 117 | -0.05 [-0.49; +0.39] | -0.27 | 0.498 | -0.24 | 0.5902 | 1.00 | - / - / False | False / False |
| KT06 | + | AVR | 15 | 2802 | 2603 | 172 | 27 | -0.02 [-0.28; +0.25] | -0.14 | 0.496 | -0.14 | 0.5753 | 1.00 | -0.01 / 0.04 / True | False / False |
| KT06 | + | AVR | 30 | 2802 | 2581 | 170 | 51 | -0.20 [-0.60; +0.24] | -0.27 | 0.494 | -0.42 | 0.8124 | 1.00 | +0.00 / 0.04 / True | False / False |
| KT06 | + | AVR | 45 | 2802 | 2542 | 164 | 96 | -0.16 [-0.64; +0.30] | -0.33 | 0.495 | -0.39 | 0.7437 | 1.00 | - / - / False | False / False |
| KT06 | + | BIST | 15 | 1626 | 1368 | 245 | 13 | -1.04 [-1.69; -0.35] | -2.86 | 0.442 | -1.36 | 0.9984 | 1.00 | +0.05 / 0.02 / True | False / True |
| KT06 | + | BIST | 30 | 1626 | 1366 | 244 | 16 | -1.38 [-2.48; -0.14] | -3.68 | 0.470 | -2.04 | 0.9844 | 0.96 | +0.05 / 0.03 / True | False / True |
| KT06 | + | BIST | 45 | 1626 | 1354 | 237 | 35 | -1.51 [-2.86; -0.15] | -4.07 | 0.467 | -2.15 | 0.9787 | 0.76 | - / - / False | False / False |
| KT07 | + | ABD | 15 | 151 | 145 | 5 | 1 | -0.40 [-2.13; +1.42] | -0.52 | 0.487 | -1.28 | 0.6675 | 0.45 | -0.06 / 0.00 / True | False / False |
| KT07 | + | ABD | 30 | 151 | 145 | 5 | 1 | -3.43 [-14.02; +2.19] | +0.34 | 0.512 | -5.89 | 0.6741 | 0.16 | -0.34 / 0.00 / True | False / False |
| KT07 | + | ABD | 45 | 151 | 143 | 5 | 3 | -6.13 [-19.24; +0.88] | -0.48 | 0.485 | -9.78 | 0.8972 | 0.12 | - / - / False | False / False |
| KT07 | + | AVR | 15 | 36 | 30 | 6 | 0 | +0.35 [-3.13; +4.02] | +0.66 | 0.518 | -1.54 | 0.4239 | 0.16 | +0.02 / 0.00 / True | False / False |
| KT07 | + | AVR | 30 | 36 | 30 | 6 | 0 | -0.33 [-3.82; +2.84] | +0.77 | 0.517 | -2.00 | 0.5704 | 0.11 | +0.03 / 0.00 / True | False / False |
| KT07 | + | AVR | 45 | 36 | 29 | 6 | 1 | +0.93 [-4.46; +5.70] | +1.27 | 0.534 | -3.00 | 0.3687 | 0.09 | - / - / False | False / False |
| KT07 | + | BIST | 15 | 129 | 108 | 21 | 0 | -0.16 [-2.00; +2.28] | -2.69 | 0.454 | -1.56 | 0.5619 | 0.46 | +0.10 / 0.00 / True | False / False |
| KT07 | + | BIST | 30 | 129 | 108 | 21 | 0 | -0.55 [-3.23; +2.72] | -2.29 | 0.496 | -2.45 | 0.6379 | 0.16 | +0.13 / 0.00 / True | False / False |
| KT07 | + | BIST | 45 | 129 | 108 | 21 | 0 | +0.54 [-3.11; +5.11] | -3.51 | 0.493 | -2.49 | 0.4119 | 0.10 | - / - / False | False / False |
| KT08 | - | ABD | 15 | 4835 | 4729 | 45 | 61 | -0.02 [-0.48; +0.54] | -0.05 | 0.508 | -0.28 | 0.4617 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT08 | - | ABD | 30 | 3430 | 3347 | 36 | 47 | -0.47 [-1.72; +0.82] | -0.83 | 0.500 | -0.81 | 0.4003 | 1.00 | +0.01 / 0.05 / True | False / False |
| KT08 | - | ABD | 45 | 2946 | 2845 | 30 | 71 | -1.23 [-3.65; +1.31] | -1.87 | 0.495 | -1.76 | 0.4069 | 0.99 | - / - / False | False / False |
| KT08 | - | AVR | 15 | 1838 | 1774 | 54 | 10 | +0.29 [-0.42; +1.11] | +0.35 | 0.515 | +0.05 | 0.7341 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | AVR | 30 | 1406 | 1356 | 40 | 10 | +0.42 [-0.71; +1.80] | +0.31 | 0.513 | +0.07 | 0.6945 | 1.00 | +0.04 / 0.03 / True | False / False |
| KT08 | - | AVR | 45 | 1266 | 1226 | 31 | 9 | +0.34 [-0.77; +1.93] | +0.20 | 0.510 | -0.28 | 0.6776 | 1.00 | - / - / False | False / False |
| KT08 | - | BIST | 15 | 721 | 653 | 67 | 1 | -0.73 [-1.85; +0.51] | -1.50 | 0.480 | -1.40 | 0.1229 | 1.00 | +0.02 / 0.04 / True | False / False |
| KT08 | - | BIST | 30 | 475 | 436 | 38 | 1 | -2.08 [-5.69; +0.94] | -2.89 | 0.469 | -3.28 | 0.1807 | 0.53 | +0.03 / 0.00 / True | False / False |
| KT08 | - | BIST | 45 | 400 | 364 | 34 | 2 | -3.83 [-9.60; +0.43] | -3.31 | 0.471 | -5.70 | 0.0979 | 0.26 | - / - / False | False / False |
| KT09 | + | ABD | 15 | 167 | 162 | 4 | 1 | +4.39 [-1.47; +9.67] | +1.31 | 0.537 | -0.38 | 0.1082 | 0.49 | +0.00 / 0.00 / True | False / False |
| KT09 | + | ABD | 30 | 167 | 155 | 4 | 8 | +6.67 [-2.13; +15.45] | +2.44 | 0.532 | -0.51 | 0.1109 | 0.17 | +0.01 / 0.00 / True | False / False |
| KT09 | + | ABD | 45 | 167 | 148 | 4 | 15 | +10.23 [-8.64; +33.84] | -1.38 | 0.512 | -6.15 | 0.3596 | 0.12 | - / - / False | False / False |
| KT09 | + | AVR | 15 | 20 | 19 | 0 | 1 | +2.31 [-10.77; +18.45] | -5.85 | 0.418 | -8.27 | 0.3755 | 0.11 | +0.08 / 0.00 / True | False / False |
| KT09 | + | AVR | 30 | 20 | 19 | 0 | 1 | +2.51 [-8.79; +14.66] | +0.51 | 0.520 | -5.01 | 0.3341 | 0.08 | +0.21 / 0.00 / True | False / False |
| KT09 | + | AVR | 45 | 20 | 19 | 0 | 1 | +1.07 [-12.55; +15.55] | -5.87 | 0.486 | -8.54 | 0.4330 | 0.07 | - / - / False | False / False |
| KT10 | + | ABD | 15 | 18011 | 17089 | 751 | 171 | -0.01 [-0.21; +0.22] | -0.33 | 0.496 | -0.11 | 0.5255 | 1.00 | +0.01 / 0.04 / True | False / False |
| KT10 | + | ABD | 30 | 11238 | 10596 | 465 | 177 | -0.10 [-0.58; +0.42] | -0.66 | 0.493 | -0.31 | 0.6431 | 1.00 | +0.00 / 0.00 / True | False / False |
| KT10 | + | ABD | 45 | 8851 | 8286 | 354 | 211 | -0.03 [-0.60; +0.60] | -0.72 | 0.500 | -0.30 | 0.5297 | 1.00 | - / - / False | False / False |

FARK = R_H - eş ortalaması (yüzde puan); boot = ay kümeli (birikimli hücrede bakışta %97,5); T+ / T- karar kuralındaki hücre şartları. Evren bugün işlem gören hisseler (hayatta kalma yanlılığı). Komisyon yok.
