# D9_YENIDEN — ÖN KAYIT

D9_YENIDEN v1.0 (2026-11-14): COL_v1 D9 uzun çöl + D9b sektör rüzgârı, ORTAK CETVEL v1.0 ile

- D9_ESIK_SHA: `88c5a0477587bf342127a59a32703784e5948b24530dd6d0de7c72e3b9808774`
- D9_PARAM_SHA: `73dde4dbed813dc26779d522cbf2d74173571eabaf5f6b0ba0b72c30583e85e8`
- D9_KOD_SHA: `a759d916915f2fc97f8258933fc5ce7d1b2cb8f6036691e1531e5d140c6bb80c`
- COL_V1_SHA: `13597d4209698a7edbeb4fb947c383ffa1c3c2d9eb715e33c5ef6902ce8987b8`
- ZAMAN (UTC): `2026-11-14 13:45:52 UTC`

Bu dosya ölçümden ÖNCE yazıldı; hiçbir getiri / eş farkı / olasılık hesaplanmadı (yalnız olay sayımı). `kos` bu dosya git'e işlenmiş ve değişmemiş değilse, sha'lardan biri tutmazsa ya da D9_PARAM COL_v1 sabitlerinden farklıysa durur.

## Cetvel mühür satırları (ORTAK_CETVEL; aynen)

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

## Soru

Cemal: 'uzun süren sıkışmanın ve rüzgâr etkisinin tespit performansını ölç'. Ç37 D9 uzun çöl + D9b rüzgâr (üretim ekranı T8) ORTAK CETVEL ile: eş farkı, slot portföy / plasebo, olasılık tablosu (+%100 / -%50, 250 gün).

## Sinyal tanımı (COL_v1.py'den birebir; parametreler)

```json
{
 "RUZ_BAYAT": 5,
 "RUZ_ESIK": 0.1,
 "RUZ_GERI": 60,
 "RUZ_MIN_UYE": 4,
 "RUZ_MUTLAK": 0.0,
 "UZUN_BANT": 1.5,
 "UZUN_KONUM": 0.5,
 "UZUN_MUM": 0.04,
 "UZUN_W": 250
}
```

- D9 = uzun_col_olc(t)['uzun'] in {12ay, 6ay}: W = 250 (önce) / 125 bar; t'ye kadar en az W + 200 bar; kapanış %95 / %5 <= 1,50; ort TR / ort kapanış <= 0,04; pencere medyanı önceki 500 barın (Low min .. High max) aralığında <= 0,50.
- RÜZGÂR (D9b / D10a) = sektor_ruzgar(t): ruz = sepet (alt sektörün öteki üyeleri, en az 4, eşit ağırlık) - piyasa (taze hisselerin 60 bar getiri MEDYANI) >= 0,10 VE sepet > 0; taze = son bar ortak son tarihten en çok 5 iş günü eski; 60 bar başlangıcı t0 = taze hisselerin 61. son bar tarihlerinin medyanı.
- Satırlar: {"a": "D9 (uzun çöl; 12ay ya da 6ay)", "b": "D9 VE RÜZGÂR (D9b; üretim ruzgar_listesi)", "c": "RÜZGÂR VE D9 DEĞİL (rüzgârın kendi katkısı)"}
- Olay: DURUM GÜNLERİ: sinyal koşulunun t kapanışında doğru olduğu her işlem günü (t = hissenin kendi barı, yalnız t'ye kadar bilgi) OC.oc_olc'a verilir; tekilleştirme (60 gün) ve giriş (ertesi geçerli açılış) cetvelindir. Üretim ekranı (T8) durumu her gün gösterdiği için durum günü seçildi (ilk gün değil); uzun durumda ~60 günde bir olay düşer.
- Veri: OC.oc_veri temiz bar (H>L, V>0; 31.08.2026 kesik) — sinyal de bu barlarla hesaplanır (üretim ham veriyle hesaplar; K3)
- Sektör: BIST sektor_BIST.csv 'alt_bist'; ABD sektor_ABD.csv 'endustri'. COL_v1 sektor_tablosu 'alt_bist' yoksa 'alt' okur; ABD dosyasında ikisi de yok -> 'endustri' (alt sektör karşılığı). Sektör listesi bugünkü (K2 sınırı: sektör ataması karar günündeki hali değil; sınıf değişimi nadir)
- Piyasa: pazarın (oc_veri evreni; ABD'de k34 hisseleri evren_bas gününden itibaren) taze hisselerinin 60 bar getiri MEDYANI (COL_v1 sektor_ruzgar; iş tanımındaki 'eşit ağırlıklı günlük ortalama' yerine COL_v1 tanımı korundu: sinyal değiştirilmez)
- ABD k34 hisseleri evren_bas (k34_evren ilk_giris) gününden önce rüzgâr hesabına ve olaya girmez
- AVR: yalnız (a); (b) / (c) için 'AVRUPA VERİSİ YOK' (sektör listesi yok); karar en fazla ABD-ADAY
- Çoklu karşılaştırma: 3 ana satır; her satırın kararı ORTAK CETVEL dört karar hücresi kuralıyla; alt gruplar (süre, tercil) yalnız bilgi, etiketleri karar değildir

## SAPMA (sonuç görülmeden yazıldı)

- İş tanımı 'piyasa = pazarın eşit ağırlıklı günlük ortalaması' diyor; COL_v1 sektor_ruzgar piyasayı 60 bar getirilerinin MEDYANI olarak hesaplar. 'Sinyal tanımı değiştirilmez' kuralı öncelikli: COL_v1 medyanı kullanıldı.
- COL_v1'de ABD sektör sütunu tanımlı değil (sektor_tablosu 'alt_bist' / 'alt' arar, sektor_ABD.csv'de ikisi de yok): ABD için 'endustri' seçildi (BIST alt endekslerinin karşılığı, alt sektör). ABD k34 hisselerinin çoğu sektör listesinde yok: piyasa medyanına girer, rüzgâr alamaz.
- Üretim sinyali ham veriyle hesaplar; burada cetvelin temiz barları (H>L, V>0) kullanıldı (K3).
- Fon süzgeci (D8, Eylül 2026) ölçüm penceresi dışında (kriz kesiği 31.08.2026): uygulanmadı.

## Bilgi (karar dışı) alt gruplar

- Çöl süresi: aynı üç eşikle (bant, mum, konum; önceki 500 bar) W = 125 / 190 / 250: >=12 ay = 250 tutar; 9-12 = 250 tutmaz, 190 tutar; 6-9 = yalnız 125 tutar (yalnız (a) olaylarında; karar dışı)
- Rüzgâr şiddeti: ruz tercilleri: sınırlar her pazarın RÜZGÂR durum günlerinin (2016-01-01 .. 2026-08-31) ruz değerlerinin 1/3 ve 2/3 yüzdeliği, ön kayıtta sayıyla yazılır; (b) ve (c) olaylarına aynı sınırlar; karar dışı
- Tercil sınırları (ruz, sonuç görülmeden): ABD: 0.1402 / 0.2222; BIST: 0.1375 / 0.2065

## Veri sha256

- V_BIST.pkl: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- V_ABD.pkl: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`

## OLAY SAYIMI (getiri hesaplanmadan)

| Satır | Pazar | durum günü 2016-22 / 2023 / 2024-26 | OLAY (cetvel sonrası, girişe göre) 2016-22 / 2023 / 2024-26 | tekil düşen | havuz dışı |
|---|---|---|---|---|---|
| a | ABD | 242347 / 125253 / 260643 | 4696 / 2399 / 4896 | 577069 | 38866 |
| a | AVR | 227259 / 70100 / 140717 | 4023 / 1102 / 2264 | 356730 | 73777 |
| a | BIST | 109130 / 672 / 59213 | 1947 / 6 / 1012 | 126372 | 39537 |
| b | ABD | 21312 / 17444 / 45622 | 1023 / 870 / 1707 | 78976 | 1734 |
| b | AVR | - | AVRUPA VERİSİ YOK (sektör listesi yok) | - | - |
| b | BIST | 24192 / 111 / 15741 | 828 / 2 / 434 | 28850 | 9913 |
| c | ABD | 229632 / 48060 / 221027 | 7933 / 2002 / 6632 | 439067 | 46972 |
| c | AVR | - | AVRUPA VERİSİ YOK (sektör listesi yok) | - | - |
| c | BIST | 154985 / 35415 / 90278 | 3959 / 943 / 2322 | 219526 | 56507 |

Süre sınıfları ve tercil sayıları (olay, girişe göre dönem):

```json
{
 "a": {
  "ABD": {
   "sure": {
    "6-9": {
     "2016-22": 2104,
     "2023": 812,
     "2024-26": 1438
    },
    "9-12": {
     "2016-22": 677,
     "2023": 446,
     "2024-26": 566
    },
    ">=12": {
     "2016-22": 1915,
     "2023": 1141,
     "2024-26": 2892
    }
   }
  },
  "AVR": {
   "sure": {
    "6-9": {
     "2016-22": 1500,
     "2023": 242,
     "2024-26": 453
    },
    "9-12": {
     "2016-22": 630,
     "2023": 184,
     "2024-26": 224
    },
    ">=12": {
     "2016-22": 1893,
     "2023": 676,
     "2024-26": 1587
    }
   }
  },
  "BIST": {
   "sure": {
    "6-9": {
     "2016-22": 868,
     "2023": 6,
     "2024-26": 456
    },
    "9-12": {
     "2016-22": 312,
     "2023": 0,
     "2024-26": 176
    },
    ">=12": {
     "2016-22": 767,
     "2023": 0,
     "2024-26": 380
    }
   }
  }
 },
 "b": {
  "ABD": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 782,
     "2023": 721,
     "2024-26": 1287
    },
    "T2 orta": {
     "2016-22": 162,
     "2023": 110,
     "2024-26": 241
    },
    "T3 güçlü": {
     "2016-22": 79,
     "2023": 39,
     "2024-26": 179
    }
   }
  },
  "BIST": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 617,
     "2023": 1,
     "2024-26": 329
    },
    "T2 orta": {
     "2016-22": 153,
     "2023": 1,
     "2024-26": 57
    },
    "T3 güçlü": {
     "2016-22": 58,
     "2023": 0,
     "2024-26": 48
    }
   }
  }
 },
 "c": {
  "ABD": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 5739,
     "2023": 1681,
     "2024-26": 4425
    },
    "T2 orta": {
     "2016-22": 1331,
     "2023": 270,
     "2024-26": 1054
    },
    "T3 güçlü": {
     "2016-22": 863,
     "2023": 51,
     "2024-26": 1153
    }
   }
  },
  "BIST": {
   "tercil": {
    "T1 zayıf": {
     "2016-22": 2586,
     "2023": 656,
     "2024-26": 1630
    },
    "T2 orta": {
     "2016-22": 764,
     "2023": 104,
     "2024-26": 331
    },
    "T3 güçlü": {
     "2016-22": 609,
     "2023": 183,
     "2024-26": 361
    }
   }
  }
 }
}
```

Kural: bir hücrede n < 30 ise ÖLÇÜLEMEDİ yazılır, 'iz değil' denmez (cetvel oc_hucre_durum).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc: aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü, aynı giriş (açılış) / çıkış (60. gün) geometrisi; 200 plasebo portföy. Mekanik üstünlük: D9 dar bant + dip konumu düşük oynaklık / düşük momentum seçer, eş kovası momentumu eşler; oynaklık eşlenmez (raporda sınır). (c) rüzgâr sektör momentumudur; hisse momentumu eşlenir, sektör momentumu eşlenmez (yorumda yazılır) |
| K2 | geleceğe bakma | EVET | D9 t'ye kadar barlarla (rolling, geriye); rüzgâr t'ye kadar kapanışlarla (t0 taze hisselerin geçmiş tarihleri); kos d9_gelecek_denetimi 30 rastgele olayda seriyi t'de kesip COL_v1 kopyasıyla aynı D9 / ruz değerini mekanik denetler; test 'geleceğe bakma'. Sınır: sektör listesi bugünkü |
| K3 | geçerli bar | EVET | OC.oc_veri temiz bar (H>L, V>0, fiyat > 0) üzerinden sinyal; geçersiz bar sinyal günü olamaz (cetvel sayımında 'sinyal barı geçersiz') |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücre tablosunda medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); sinyal t kapanışında hesaplanır |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat (V_*.pkl); D9 oranları birimden bağımsız; bölünme şüphesi cetvelde (geçmiş penceresi); pencere içi bölünme bant ölçüsünü bozabilir (düzeltilmiş veride küçük) |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (+ ABD k34 nakdi biten); batanlar yok; oc_rapor notu: getiriler yukarı, -%50 olasılığı aşağı yanlı |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ ('iz değil' denmez); iki alt dönem şartı cetvelde; İZ DEĞİL yalnız güç yeterliyken; olay sayımı ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | D9_ESIK sha + D9_PARAM sha + D9_YENIDEN.py sha + COL_v1.py sha + cetvel üç sha ön kayıtta; kos OC.oc_kapi + d9_onkayit_dogrula (git işlenmiş / değişmemiş, sha eşit, D9_PARAM == COL_v1 sabitleri) geçmezse durur |
| K10 | ayrıştırma | UYGULANMAZ | metin / KAP ayrıştırma yok; yalnız OHLCV + iki sektör csv'si; 3 olay ham veriden elle doğrulanır (rapor DENETİM) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/d9_yeniden/olay_<satır>.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir (rapor DENETİM) |
| K12 | ifade | EVET | etiketler yalnız oc_etiket / oc_olasilik_etiket; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_d9; yasak dosyalar (COL_v1, ORTAK_CETVEL, IZ_KARNE, defterler) yalnız okunur, git diff denetimi; e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; T8 için öneri yalnız 'kalsın / kaldırılsın' (karar Cemal'in) |

## Test

`python test_d9_yeniden.py` (sentetik: D9 / rüzgâr kopyası COL_v1 ile birebir, vektörlü sürüm kopyayla birebir, geleceğe bakma kesme testi, D9_PARAM == COL_v1 sabitleri, cetvel çağrısı, kapı, e-posta / anahtar taraması).
