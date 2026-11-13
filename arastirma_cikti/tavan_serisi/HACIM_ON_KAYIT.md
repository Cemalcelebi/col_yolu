# TAVAN SERİSİ / HACİM ÖN KAYDI (ölçümden önce)

TAVAN_SERISI hacim v1.0 (tavan_hacim_20261113): çökmüş BIST hissesinde devasa hacim barı (H1), dipte tavansız hacim (H2), taban fiyat (H3); ön kayıtlı. Yazılma 2026-11-13 11:56:36 UTC. Bu dosya git'e işlenmeden `python TAVAN_SERISI.py hacim kos` çalışmaz (mühür kapısı).

## Soru (Cemal, 13 Kasım 2026)

'Hepsi kumar değil. TEHOL'de devasa hacimli bir alım barı var; 1 liradaki hisseyi böyle hacim zıplatır; 1 liradan daha nereye düşer; 5 tavan = %61.' H1: çökmüş hissede devasa hacimli tavan barından sonra katılmak, aynı gün aynı derinlikte hacimsiz çökmüşlerden iyi mi? H2: dipte tavansız devasa hacim (birikim) aynı soruda. H3: 1 / 2 TL altındaki çökmüş hisse sonraki 60 / 120 / 250 günde yine de -%50'ye düşüyor mu?

## Tanımlar ve eşikler (TH_ESIK, değişmez)

```json
{
 "bilgi": "Eylül 2026 - son bar olayları (H1 / H2 ana tanım, giriş a; kontrol yok) ayrı tablo, karara girmez; sonuç penceresi tamamlanmamış ölçü 'açık'; son bar gün içiyse işaretlenir; bugüne kadar: son kapanış / giriş, girişten sonra en yüksek ve en düşük. İzlenen hisseler (TEHOL, PEKGY, IEYHO, DSTKF, OZATD, TRHOL): son 10 barın getirisi, hacim oranı, derinliği, H1 / H2 koşul işaretleri",
 "bilgi_bas": "2026-09-01",
 "bootstrap": {
  "B": 2000,
  "guven": [
   2.5,
   97.5
  ],
  "kume": "hisse (olaylar hisseleriyle birlikte çekilir)",
  "tohum": 20261113
 },
 "cokmus": {
  "duyarlilik": [
   -0.7,
   -0.6
  ],
  "esik": -0.8,
  "tanim": "derinlik = olay gününden ÖNCEKİ kendi barının kapanışı / o barın son 250 barlık en yüksek kapanışı - 1 (ts_tavan 'derinlik' bir bar geri); ÇÖKMÜŞ <=> derinlik <= eşik; tanımsızsa olay değil, kontrol değil"
 },
 "donem": [
  "2016-01-01",
  "2026-08-31"
 ],
 "donem_kirilim": {
  "2016-19": [
   "2016-01-01",
   "2019-12-31"
  ],
  "2020-22": [
   "2020-01-01",
   "2022-12-31"
  ],
  "2023-26.08": [
   "2023-01-01",
   "2026-08-31"
  ],
  "tanim": "dönem = olay günü t (H3'te ay başı günü)"
 },
 "giris": {
  "a": "ANA: t'den sonraki ilk kendi barı e'nin açılışı O_e; O yok / hacim 0 -> 'giriş yok' (sayılır); e tam kilitli tavansa 'dolum belirsiz' işareti (sonuç yine O_e'den)",
  "b": "t kapanışı C_t; t kilitli tavan (ts_tavan 'kilitli': O = H = C) ise 'alınamaz' (sayılır, ölçülmez)"
 },
 "grafik": {
  "adet": 3,
  "iyi": "H1 ANA, giriş a, r60 > 0",
  "kotu": "H1 ANA, giriş a, r60 <= 0",
  "once": 120,
  "sonra": 60,
  "tanim": "iyi ve kötü gruplarından (sembol, tarih) sırasıyla dizilip tohumlu rastgele 3'er olay; PNG /tmp/tavan/grafik (repoya girmez)",
  "tohum": 20261113
 },
 "h3": {
  "ay": "her hisse-ay: ayın ilk kendi işlem günü t (2016-01 .. kesik); ÇÖKMÜŞ <=> C_t / kendi son 250 barının en yüksek kapanışı - 1 <= -0,80 (ts_tavan 'derinlik', aynı gün)",
  "fiyat": "ekran fiyatı = Yahoo kapanış x sonraki bölünmeler çarpanı (o gün tahtada görünen fiyat)",
  "giris": "C_t; pencere t+1 .. t+h",
  "kova": [
   [
    0.0,
    1.0
   ],
   [
    1.0,
    2.0
   ],
   [
    2.0,
    5.0
   ],
   [
    5.0,
    null
   ]
  ],
  "olcu": "P(-%50'ye dokunma) 60 / 120 / 250 gün; en düşük nokta = min L[t+1 .. t+250] / C_t - 1 (medyan, %10, %25); BİLGİ: P(+%100, 250g), r250 medyan; karşılaştırma: aynı şart 2 TL ve üstü çökmüşler; ayrıca ÇÖKMEMİŞ 2 TL altı (BİLGİ); dönem kırılımı; hisse kümeli %95 aralık (oranlar). Karar yok.",
  "ufuk": [
   60,
   120,
   250
  ]
 },
 "hacim": {
  "duyarlilik": [
   5.0,
   20.0,
   50.0
  ],
  "kat": 10.0,
  "kontrol_ust": 3.0,
  "pencere": 20,
  "tanim": "hacim oranı = t günü hacmi / t'den önceki 20 kendi barının hacim medyanı; önceki 20 bar yoksa ya da medyan <= 0 ise tanımsız"
 },
 "hip": {
  "H1": {
   "getiri": "tavan",
   "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü tavan (ts_tavan; 13.03.2020'den >= +%9,5, öncesi >= +%19)"
  },
  "H1b": {
   "getiri": [
    0.05,
    0.25
   ],
   "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü kapanış getirisi >= +%5 (ve <= %25: kırık değil)"
  },
  "H2": {
   "getiri": [
    -0.05,
    0.05
   ],
   "tanim": "ÇÖKMÜŞ + hacim oranı >= kat + t günü kapanış getirisi -%5 .. +%5 (dipte birikim, tavansız)"
  }
 },
 "karar": {
  "ana": "H1|-0.80|10|a",
  "donem_min": 2,
  "donem_n_min": 10,
  "ikincil": "H2|-0.80|10|a",
  "metin": "H1 ANA (ÇÖKMÜŞ -%80, hacim >= 10x, tavan, giriş a) 'İZ ADAYI (BIST)' <=> n (60 gün farkı ölçülen olay) >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(+%61, 20g) olay >= 1,5 x kontrol (kontrol 0 ise olay > 0 yeter) VE P(-%50, 60g) olay <= 1,2 x kontrol (kontrol 0 ise olay da 0 olmalı) VE üç dönemin (2016-19 / 2020-22 / 2023-26.08; n >= 10 olanlar) en az ikisinde dönem medyan farkı > 0. Değilse 'KANIT YOK' ve tutmayan şartlar yazılır (n < 30: 'örneklem yetersiz', yine KANIT YOK). H2 ANA (hacim >= 10x, -%5..+%5, giriş a) aynı cümleyle İKİNCİL. Öteki hücreler (derinlik -%70 / -%60, kat 5 / 20 / 50, H1b, giriş b) BİLGİ: kural sonucu yazılır, kararı değiştirmez; kaç hücrenin geçtiği çoklu deneme olarak yazılır. H3 için yalnız sayı, karar yok.",
  "n_min": 30,
  "p50_kat": 1.2,
  "p61_kat": 1.5
 },
 "kontrol": {
  "fark": "olay başına fark = olay r60 - kontrol ortalama r60; kontrolü olmayan olay farkta dışarıda (sayılır)",
  "kova_ana": [
   -0.8,
   -0.85,
   -0.9
  ],
  "tanim": "her ÇÖKMÜŞ olay için: aynı t gününde aynı derinlik kovasında (ana -0,80: (-0,85, -0,80], (-0,90, -0,85], <= -0,90; -0,70 / -0,60'ta eşikten -1'e üç eşit dilim, ts_esik_gevsek), t günü hacim oranı tanımlı ve < 3 olan, giriş satırında işlem gören (a: O var ve hacim > 0; b: C_t var) bütün öteki hisseler; aynı giriş türüyle aynı ölçüler; kontrol değeri = kontrol hisselerinin ortalaması (oranlarda ortalama oran)"
 },
 "kriz": "2026-08-31",
 "olcu": {
  "dok": [
   [
    "up61_20",
    20,
    0.61
   ],
   [
    "up100_60",
    60,
    1.0
   ],
   [
    "dn50_60",
    60,
    -0.5
   ]
  ],
  "tanim": "giriş a satırı e: pencere e .. e+h-1, r_h = C(e+h-1) / O_e - 1; giriş b satırı t: pencere t+1 .. t+h, r_h = C(t+h) / C_t - 1 (iki girişte aynı son gün; takvim satırı, durdurmada son kapanış ileri taşınır). Dokunma: pencerede max H >= giriş x (1 + eşik) ya da min L <= giriş x (1 + eşik). +%61 = Cemal'in '5 tavan' (1,1^5 = 1,61). Yarış: 60 bar içinde ilk H >= 1,5 giriş mi ilk L <= 0,75 giriş mi; aynı gün ikisi 'aynı gün', hiçbiri 'yok'. Pencere kesiği (31.08.2026) aşan ölçü yok; pencerede veri kırığı (|günlük| > %25) varsa o ölçü yok (sayısı yazılır). En kötü %10: r60'ın 10. yüzdeliği ve en kötü %10 olayın ortalaması",
  "ufuk": [
   5,
   20,
   60
  ],
  "yaris": {
   "asagi": -0.25,
   "ufuk": 60,
   "yukari": 0.5
  }
 },
 "surum_etiket": "tavan_hacim_20261113",
 "tekil": {
  "gun": 20,
  "tanim": "aynı hisse ve aynı hücre (hipotez x derinlik eşiği x hacim katı) için bir olaydan sonraki 20 kendi barı içinde yeni olay sayılmaz (kronolojik, açgözlü); iki giriş türü aynı olayları kullanır"
 },
 "veri": "TAVAN_SERISI ile aynı Yahoo günlük önbellek (/tmp/tavan/yahoo, ts_fiyatlar); tavan = ts_tavan (TS_ESIK['tavan']: BIST marjı 12.03.2020'ye kadar ±%20, 13.03.2020'den ±%10; 1-2 TL'de fiyat adımı; |günlük| > %25 veri kırığı); derinlik = ts_tavan (kendi son 250 barının en yüksek kapanışı, kırıktan sonra yeniden dolar); takvim = ts_panel (en az 10 hisse); hacim = Yahoo adet (bölünme düzeltmeli)",
 "yanlilik": "evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker, özellikle H3'te -%50 olasılığını AŞAĞI); işlem maliyeti yok; kilitli tavanda giriş a'nın dolumu belirsiz; olaylar takvimde örtüşebilir (aynı gün birden çok hisse), aralık hisse kümeli"
}
```

Yeniden kullanılan TAVAN_SERISI tanımları (mühre dahil): tavan [["2000-01-01", "2020-03-12", 0.2], ["2020-03-13", "2099-12-31", 0.1]], kontrol kovaları [-0.8, -0.85, -0.9], fiyat adımları [[0.0, 0.01], [20.0, 0.02], [50.0, 0.05], [100.0, 0.1], [250.0, 0.25], [500.0, 0.5], [1000.0, 1.0], [2500.0, 2.5]].

## Karar cümlesi (önceden yazılı)

H1 ANA (ÇÖKMÜŞ -%80, hacim >= 10x, tavan, giriş a) 'İZ ADAYI (BIST)' <=> n (60 gün farkı ölçülen olay) >= 30 VE medyan 60 gün fark > 0 VE hisse kümeli bootstrap %95 alt uç > 0 VE P(+%61, 20g) olay >= 1,5 x kontrol (kontrol 0 ise olay > 0 yeter) VE P(-%50, 60g) olay <= 1,2 x kontrol (kontrol 0 ise olay da 0 olmalı) VE üç dönemin (2016-19 / 2020-22 / 2023-26.08; n >= 10 olanlar) en az ikisinde dönem medyan farkı > 0. Değilse 'KANIT YOK' ve tutmayan şartlar yazılır (n < 30: 'örneklem yetersiz', yine KANIT YOK). H2 ANA (hacim >= 10x, -%5..+%5, giriş a) aynı cümleyle İKİNCİL. Öteki hücreler (derinlik -%70 / -%60, kat 5 / 20 / 50, H1b, giriş b) BİLGİ: kural sonucu yazılır, kararı değiştirmez; kaç hücrenin geçtiği çoklu deneme olarak yazılır. H3 için yalnız sayı, karar yok.

Ölçülecekler (her hücre): n (hisse), P(20 günde +%61'e dokunma), P(60 günde +%100), P(60 günde -%50), önce +%50 mi önce -%25 mi (60 gün), 5 / 20 / 60 gün getiri medyan ve ortalama, en kötü %10, kontrol ve fark (hisse kümeli bootstrap %95), dönem kırılımı 2016-19 / 2020-22 / 2023-26.08. Fon krizi sonrası olaylar ayrı BİLGİ tablosu. Grafik: H1 ana tanımdan iyi / kötü gruplarından tohumlu 3'er örnek.

## Veri ve tanım sayımı (sonuç içermez)

- Fiyat: 630 hisse okundu, 0 eksik; son tarih 2026-11-13; manifest sha256 5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56.
- Test paneli (kesik 2026-08-31): 626 hisse, takvim 2015-01-01 - 2026-08-31.
- ANA hücre H1|-0.80|10|a: 12 olay (10 hisse), girişi olan 12. İKİNCİL H2|-0.80|10|a: 19 olay (13 hisse), girişi olan 19.
- Bütün hücreler (olay / girişi olan / hisse): H1|-0.80|10|a: 12 / 12 / 10; H1|-0.80|10|b: 12 / 11 / 10; H1|-0.80|5|a: 30 / 30 / 23; H1|-0.80|5|b: 30 / 30 / 23; H1|-0.80|20|a: 5 / 5 / 5; H1|-0.80|20|b: 5 / 5 / 5; H1|-0.80|50|a: 4 / 4 / 4; H1|-0.80|50|b: 4 / 4 / 4; H1|-0.70|10|a: 42 / 42 / 35; H1|-0.70|10|b: 42 / 41 / 35; H1|-0.70|5|a: 96 / 96 / 65; H1|-0.70|5|b: 96 / 93 / 65; H1|-0.70|20|a: 9 / 9 / 9; H1|-0.70|20|b: 9 / 9 / 9; H1|-0.70|50|a: 5 / 5 / 5; H1|-0.70|50|b: 5 / 5 / 5; H1|-0.60|10|a: 77 / 77 / 64; H1|-0.60|10|b: 77 / 72 / 64; H1|-0.60|5|a: 210 / 210 / 128; H1|-0.60|5|b: 210 / 201 / 128; H1|-0.60|20|a: 22 / 22 / 22; H1|-0.60|20|b: 22 / 21 / 22; H1|-0.60|50|a: 7 / 7 / 7; H1|-0.60|50|b: 7 / 7 / 7; H2|-0.80|10|a: 19 / 19 / 13; H2|-0.80|10|b: 19 / 19 / 13; H2|-0.80|5|a: 61 / 61 / 29; H2|-0.80|5|b: 61 / 61 / 29; H2|-0.80|20|a: 4 / 4 / 4; H2|-0.80|20|b: 4 / 4 / 4; H2|-0.80|50|a: 1 / 1 / 1; H2|-0.80|50|b: 1 / 1 / 1; H2|-0.70|10|a: 65 / 65 / 45; H2|-0.70|10|b: 65 / 65 / 45; H2|-0.70|5|a: 194 / 191 / 82; H2|-0.70|5|b: 194 / 194 / 82; H2|-0.70|20|a: 17 / 17 / 16; H2|-0.70|20|b: 17 / 17 / 16; H2|-0.70|50|a: 2 / 2 / 2; H2|-0.70|50|b: 2 / 2 / 2; H2|-0.60|10|a: 156 / 156 / 92; H2|-0.60|10|b: 156 / 156 / 92; H2|-0.60|5|a: 473 / 464 / 175; H2|-0.60|5|b: 473 / 473 / 175; H2|-0.60|20|a: 41 / 41 / 36; H2|-0.60|20|b: 41 / 41 / 36; H2|-0.60|50|a: 10 / 10 / 10; H2|-0.60|50|b: 10 / 10 / 10; H1b|-0.80|10|a: 26 / 26 / 16; H1b|-0.80|10|b: 26 / 25 / 16; H1b|-0.80|5|a: 63 / 63 / 31; H1b|-0.80|5|b: 63 / 63 / 31; H1b|-0.80|20|a: 11 / 11 / 7; H1b|-0.80|20|b: 11 / 11 / 7; H1b|-0.80|50|a: 4 / 4 / 4; H1b|-0.80|50|b: 4 / 4 / 4; H1b|-0.70|10|a: 90 / 87 / 52; H1b|-0.70|10|b: 90 / 89 / 52; H1b|-0.70|5|a: 214 / 210 / 92; H1b|-0.70|5|b: 214 / 211 / 92; H1b|-0.70|20|a: 27 / 27 / 20; H1b|-0.70|20|b: 27 / 27 / 20; H1b|-0.70|50|a: 6 / 6 / 6; H1b|-0.70|50|b: 6 / 6 / 6; H1b|-0.60|10|a: 196 / 193 / 112; H1b|-0.60|10|b: 196 / 192 / 112; H1b|-0.60|5|a: 489 / 484 / 189; H1b|-0.60|5|b: 489 / 481 / 189; H1b|-0.60|20|a: 62 / 62 / 46; H1b|-0.60|20|b: 62 / 61 / 46; H1b|-0.60|50|a: 11 / 11 / 11; H1b|-0.60|50|b: 11 / 11 / 11.

## Ön kayıttan önce görülenler (sonuç değil)

- TAVAN_RAPOR.md (aynı gün, ön kayıtlı): çökmüş hissede 1. tavandan sonra katılmak kontrolden iyi değil (k=1 KUMAR), k >= 2 örneklem az. Hacim koşulu o ölçümde yoktu.
- İzlenen altı hissenin (TEHOL, PEKGY, IEYHO, DSTKF, OZATD, TRHOL) son 10 barının getiri / hacim oranı / derinliği (tanım denetimi; ör. TEHOL 05.11.2026 hacim oranı ~4.300x, 09.11.2026 tavan + ~580x). Kilitli taban dizisinden çıkışta 20 gün medyan hacmi çok küçük olduğundan oranlar yüzlerce / binlerce kat çıkabiliyor: tanım bu hâliyle ölçülür, eşik değişmez.
- Yahoo hacminin bölünme düzeltmeli olduğu (bölünme günlerinde 20 gün medyan hacim oranı ~1; ör. AEFES 10:1 2025-06-26: 0,91) denetlendi.
- Olay sayıları (yukarıda). Getiri, dokunma oranı, kontrol farkı görülmedi.
- Sayımdan çıkan (sonuç değil): ANA hücrede yalnız 12 olay var (n < 30), bu yüzden ana karar büyük olasılıkla 'KANIT YOK (örneklem yetersiz)' çıkar. Yön bilgisi n >= 30 olan BİLGİ hücrelerinden (derinlik -%70 / -%60, kat 5 / 10, H1b, H2) okunur; bunlar kararı değiştirmez, kaç tanesinin kuralı geçtiği ve kaç tanesinin medyan fark aralığının tamamen 0'ın altında olduğu yazılır.

## Bilinen yanlılıklar

evren bugün işlem gören hisseler (batan / kotasyondan çıkan yok: hayatta kalma yanlılığı sonucu YUKARI çeker, özellikle H3'te -%50 olasılığını AŞAĞI); işlem maliyeti yok; kilitli tavanda giriş a'nın dolumu belirsiz; olaylar takvimde örtüşebilir (aynı gün birden çok hisse), aralık hisse kümeli

ESIK_SHA256: 65ff181df8d4d892478fb976be4d05df2ee3cac5ac6ca683ec71623043edc974
KOD_SHA256: 964148091a72f021e6d40372e8c2aeeeee74a582f21aba5cb9ce61e93aedba10
VERI_MANIFEST_SHA256: 5182947ec875fd59d89f61c25a24258bbdad4f376c15287fb5ffb4b50c9e2e56
