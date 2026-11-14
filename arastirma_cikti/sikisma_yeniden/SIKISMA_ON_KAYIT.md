# SIKISMA_YENIDEN — ÖN KAYIT

SIKISMA_YENIDEN v1.0 (2026-11-14): sıkışma -> büyük hareket (A haberci, B zaman, C yönsüz stoplu işlem); bağımsız yeniden ölçüm

- MÜHÜR (SY_ESIK sha256): `1eb406a20091e4cb54c6cf3986f27f36e5c5ba3cbc61868ba83be53d8e7105b0`
- KOD (SIKISMA_YENIDEN.py sha256): `db4459456d38e0ebecdf72ddf510aa2abfee9487886582f1e664dd3b39ffb9af`
- ZAMAN (UTC): `2026-11-14 08:38:55 UTC`
- Bu dosya ölçümden ÖNCE yazılır ve commit + push edilir; `kos` bu dosya git'te işlenmiş ve değişmemiş değilse, mühür ya da kod sha farklıysa durur.
- Bağımsızlık: eski VDYT / VDYT2 rapor ve sonuçları okunmadı; tanımlar yalnız iş tanımından.

## Soru
Sıkışmadan sonra büyük hareket geliyor mu (hissenin OLAĞAN ölçüsüyle, göreli değil), ne zaman, yönsüz stoplu kırılım işlemi eşlerden iyi mi. Yön tahmini yok.

## Tanımlar (SY_ESIK)

- **S1**: ort(TR/C_önceki, son 10 gün) <= TR/C'nin önceki 250 gündeki (t-259..t-10) %20 yüzdeliği VE (max C - min C)/C_t (son 10 gün) <= bant; aynı hissede yeni olay en az 20 bar sonra. Bant: BIST %8, ABD/AVR %6.
- **S2**: Bollinger genişliği 4*std20(C)/ort20(C); son 250 gün içindeki yüzdelik sırası (t dahil) <= %10; aynı hissede yeni olay en az 20 bar sonra.
- **S3**: son 20 gün ort |ln getiri|; son 250 gün değerleri içindeki yüzdelik sırası (t dahil) <= %15 (sıra pct; 'altı' = <=); aynı hissede yeni olay en az 20 bar sonra.
- **Sert düşüş alt kümesi**: C_t / max(C, t-120..t) - 1 <= -%30 (Cemal'in çölü; ayrı alt küme, eşler de aynı şartla)
- **B1**: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t ortalama TR/C_önceki; sıkışma dönemi dahil)
- **B2**: max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)
- **B3**: |ln(C_t+20 / C_t)| >= 2 x σ250 x √20
- **B0**: t+1..t+20 içinde bir günün TR/C_önceki >= 3 x son 10 gün ort TR/C (göreli; tanımsal, yalnız bilgi)
- ATR birimi: ATR yüzde cinsinden (TR / önceki kapanış): 250 günde fiyat değişince mutlak ATR yanlı olur (K6 birim)
- Geçerli bar: H>L ve V>0; en az 260 bar geçmiş; fiyat kesiği 2026-08-31.
- Likidite: önceki 20 gün medyan C*V (AVR: *Kur, EUR); gün kesitinde alt %20 dışarıda; üçlü kova.
- Bölünme şüphesi: ANA: |günlük| > %25, 10 gün sonra sıçramanın en az yarısı duruyor, önceki 10 gün düz (öncekinin yarısından az hareket; geri dönüş bacağı sayılmaz) VE oran bir bölünme oranına (ya da tersine) ±%4 yakın; KATI (duyarlılık): oran şartı yok. Şüpheli günü [t-260, t+41] içinde olan hisse-gün olay ve eş havuzundan birlikte çıkar.
- Eşleme (A): aynı gün, aynı pazar, σ250 ondalığı (10) x likidite üçlüsü (3), sıkışma koşulu (S) yanlış olan hisse-günler; en az 3 eş.
- Eşleme (C): aynı gün (t), aynı pazar, 60 gün momentum beşliği x likidite üçlüsü (FI_OLCUT hücresi), S1 koşulu yanlış; aynı işlem kuralı.
- Rastgele gün (K-b): aynı hisse, aynı takvim yılı, uygun (eligible) günler, 200 çekiliş.
- Bootstrap: 2000 tekrar, küme = olay ayı (t).
- (B) zaman: pencereler [[1, 5], [6, 10], [11, 15], [16, 20]]; süre = S1 koşulunun t'de biten kesintisiz gün sayısı (eşitlik çok olduğu için ondalık yerine sabit kovalar); kovalar [[1, 1], [2, 3], [4, 6], [7, 10], [11, 20], [21, 100000]]; UZUN/KISA = run>=11 / run 1-3.
- (B) model: özellikler ['ln(sure)', 'ln(ort10 TR/C / ATR250%)', 'ln(ort hacim 10 / ort hacim 50)', 'ln(bant10)'] + σ250 ondalığı; hedef B1_5 (t+1..t+5); eğitim <= 2022-12-31 (hedef penceresi aşmasın diye 10 gün pay), test >= 2023-01-01; taban eğitimde aynı σ250 ondalığının 5 gün B1 oranı; 1 - Brier(model) / Brier(taban); ay kümeli bootstrap; alt uç > 0 => 'zaman tahmini var'. Bilanço takvimi YOK (veri yok): zaman tahmini bilanço gününü bilmeden yapılır.
- (C) işlem: t+1..t+20 içinde C > bant_üst*1,01 (uzun) ya da C < bant_alt*0,99 (kısa) ilk kapanış j; giriş Open(j+1); stop öteki kenar (gün içi; açılış stopun ötesindeyse açılış); çıkış stop ya da girişten 20. bar kapanışı; kısa getiri = 1 - çıkış/giriş; P(+%20 önce) / P(-%10 önce): giriş sonrası 20 barda lehte %20 ile aleyhte %10'dan hangisi önce (aynı gün = aleyhte), stop yok sayılır. Komisyon / kayma YOK.
- Dönemler: [['2016-22', '2016-01-01', '2022-12-31'], ['2023', '2023-01-01', '2023-12-31'], ['2024-26', '2024-01-01', '2026-08-31']] (keşif 2016-22; doğrulama 2023 ve 2024-26/08).
- Karar (A): hücre: n<30 ÖLÇÜLEMEDİ; n>=300: alt>1 TUTAR, üst<1 TERS, değilse TUTMADI; 30<=n<300: alt>1 EMARE (güç sınırlı), değilse ÖLÇÜLEMEDİ
- Karar (C): hücre: FI_OLCUT dört şart (n>=30, ort eşli fark>0 ve ay kümeli alt95>0, sıra>0,50, slot portföy > 200 rastgele eş portföyün %90'ı); tutmazsa n>=300 TUTMADI, n<300 ÖLÇÜLEMEDİ
- İZ: İZ = ABD 2023 + ABD 2024-26 + AVR 2023 + AVR 2024-26 dördü TUTAR ve keşif (2016-22) ABD ile AVR aynı yön; BIST bilgi
- Yorumlama sırası: ANA = S1 x B1. S2, S3, B2, B3, B0, KATI bölünme filtresi duyarlılıktır; karar etiketini değiştirmez.

## Eşik sözlüğü (SY_ESIK, kararlı JSON)

```json
{
 "B": {
  "atr_birim": "ATR yüzde cinsinden (TR / önceki kapanış): 250 günde fiyat değişince mutlak ATR yanlı olur (K6 birim)",
  "atr_gun": 250,
  "b0_kat": 3.0,
  "b1_kat": 3.0,
  "b2_kat": 3.0,
  "b2_min": 0.15,
  "b3_kat": 2.0,
  "sig_gun": 250,
  "tanim": {
   "B0": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x son 10 gün ort TR/C (göreli; tanımsal, yalnız bilgi)",
   "B1": "t+1..t+20 içinde bir günün TR/C_önceki >= 3 x ATR250% (t-249..t ortalama TR/C_önceki; sıkışma dönemi dahil)",
   "B2": "max_k |ln(C_t+k / C_t)|, k=1..20 >= max(%15, 3 x σ250 x √20)",
   "B3": "|ln(C_t+20 / C_t)| >= 2 x σ250 x √20"
  },
  "ufuk": 20
 },
 "C": {
  "bant_gun": 10,
  "bekle": 20,
  "gelecek_bar": 41,
  "hedef": 0.2,
  "maliyet": 0.0,
  "n_esik": 30,
  "port_n": 200,
  "port_yuzde": 0.9,
  "slot": 10,
  "tanim": "t+1..t+20 içinde C > bant_üst*1,01 (uzun) ya da C < bant_alt*0,99 (kısa) ilk kapanış j; giriş Open(j+1); stop öteki kenar (gün içi; açılış stopun ötesindeyse açılış); çıkış stop ya da girişten 20. bar kapanışı; kısa getiri = 1 - çıkış/giriş; P(+%20 önce) / P(-%10 önce): giriş sonrası 20 barda lehte %20 ile aleyhte %10'dan hangisi önce (aynı gün = aleyhte), stop yok sayılır",
  "tasma": 0.01,
  "ters": 0.1,
  "tut": 20
 },
 "S1": {
  "ara": 20,
  "bant": {
   "ABD": 0.06,
   "AVR": 0.06,
   "BIST": 0.08
  },
  "dagilim": 250,
  "pencere": 10,
  "tanim": "ort(TR/C_önceki, son 10 gün) <= TR/C'nin önceki 250 gündeki (t-259..t-10) %20 yüzdeliği VE (max C - min C)/C_t (son 10 gün) <= bant",
  "yuzdelik": 0.2
 },
 "S2": {
  "ara": 20,
  "bb_gun": 20,
  "bb_k": 2.0,
  "dagilim": 250,
  "tanim": "Bollinger genişliği 4*std20(C)/ort20(C); son 250 gün içindeki yüzdelik sırası (t dahil) <= %10",
  "yuzdelik": 0.1
 },
 "S3": {
  "ara": 20,
  "dagilim": 250,
  "gun": 20,
  "tanim": "son 20 gün ort |ln getiri|; son 250 gün değerleri içindeki yüzdelik sırası (t dahil) <= %15 (sıra pct; 'altı' = <=)",
  "yuzdelik": 0.15
 },
 "bilgi_pazar": [
  "BIST"
 ],
 "bolunme": {
  "esik": 0.25,
  "geri_gun": 10,
  "geri_pay": 0.5,
  "oran_tol": 0.04,
  "oranlar": [
   1.5,
   2,
   3,
   4,
   5,
   6,
   8,
   10,
   15,
   20,
   25,
   30,
   40,
   50,
   100
  ],
  "pencere": [
   -260,
   41
  ],
  "tanim": "ANA: |günlük| > %25, 10 gün sonra sıçramanın en az yarısı duruyor, önceki 10 gün düz (öncekinin yarısından az hareket; geri dönüş bacağı sayılmaz) VE oran bir bölünme oranına (ya da tersine) ±%4 yakın; KATI (duyarlılık): oran şartı yok. Şüpheli günü [t-260, t+41] içinde olan hisse-gün olay ve eş havuzundan birlikte çıkar."
 },
 "bootstrap": {
  "guven": [
   0.025,
   0.975
  ],
  "kume": "olay ayı (t)",
  "n": 2000,
  "tohum": 1414
 },
 "dogrulama": [
  "2023",
  "2024-26"
 ],
 "donem": [
  [
   "2016-22",
   "2016-01-01",
   "2022-12-31"
  ],
  [
   "2023",
   "2023-01-01",
   "2023-12-31"
  ],
  [
   "2024-26",
   "2024-01-01",
   "2026-08-31"
  ]
 ],
 "dusus": {
  "esik": -0.3,
  "gun": 120,
  "tanim": "C_t / max(C, t-120..t) - 1 <= -%30 (Cemal'in çölü; ayrı alt küme, eşler de aynı şartla)"
 },
 "eslesme": {
  "A": "aynı gün, aynı pazar, σ250 ondalığı (10) x likidite üçlüsü (3), sıkışma koşulu (S) yanlış olan hisse-günler",
  "C": "aynı gün (t), aynı pazar, 60 gün momentum beşliği x likidite üçlüsü (FI_OLCUT hücresi), S1 koşulu yanlış; aynı işlem kuralı",
  "min_es": 3,
  "mom_gun": 60,
  "mom_kova": 5,
  "oyn_kova": 10
 },
 "gecerli_bar": "H>L ve V>0",
 "gecmis_min": 260,
 "karar": {
  "A": "hücre: n<30 ÖLÇÜLEMEDİ; n>=300: alt>1 TUTAR, üst<1 TERS, değilse TUTMADI; 30<=n<300: alt>1 EMARE (güç sınırlı), değilse ÖLÇÜLEMEDİ",
  "C": "hücre: FI_OLCUT dört şart (n>=30, ort eşli fark>0 ve ay kümeli alt95>0, sıra>0,50, slot portföy > 200 rastgele eş portföyün %90'ı); tutmazsa n>=300 TUTMADI, n<300 ÖLÇÜLEMEDİ",
  "iz": "İZ = ABD 2023 + ABD 2024-26 + AVR 2023 + AVR 2024-26 dördü TUTAR ve keşif (2016-22) ABD ile AVR aynı yön; BIST bilgi",
  "n_guc": 300,
  "n_min": 30
 },
 "karar_donem": [
  "2023",
  "2024-26"
 ],
 "karar_pazar": [
  "ABD",
  "AVR"
 ],
 "kesif": "2016-22",
 "kriz": "2026-08-31",
 "likidite": {
  "alt_kesik": 0.2,
  "gun": 20,
  "kova": 3,
  "olcu": "önceki 20 gün medyan C*V (AVR: *Kur, EUR)"
 },
 "rastgele_gun": {
  "cekilis": 200,
  "takvim": "aynı hisse, aynı takvim yılı, uygun (eligible) günler"
 },
 "zaman": {
  "kisa": [
   1,
   3
  ],
  "model": {
   "egit_son": "2022-12-31",
   "hedef": "B1_5 (t+1..t+5)",
   "orneklem": "S1 koşulu doğru, uygun bütün hisse-günler",
   "ozellik": [
    "ln(sure)",
    "ln(ort10 TR/C / ATR250%)",
    "ln(ort hacim 10 / ort hacim 50)",
    "ln(bant10)"
   ],
   "ridge": 0.0001,
   "skill": "1 - Brier(model) / Brier(taban); ay kümeli bootstrap; alt uç > 0 => 'zaman tahmini var'",
   "taban": "eğitimde aynı σ250 ondalığının 5 gün B1 oranı",
   "test_bas": "2023-01-01"
  },
  "pencere": [
   [
    1,
    5
   ],
   [
    6,
    10
   ],
   [
    11,
    15
   ],
   [
    16,
    20
   ]
  ],
  "sure_kova": [
   [
    1,
    1
   ],
   [
    2,
    3
   ],
   [
    4,
    6
   ],
   [
    7,
    10
   ],
   [
    11,
    20
   ],
   [
    21,
    100000
   ]
  ],
  "sure_tanim": "S1 koşulunun t'de biten kesintisiz gün sayısı (eşitlik çok olduğu için ondalık yerine sabit kovalar)",
  "tehlike_ufuk": 5,
  "uzun": [
   11,
   100000
  ]
 }
}
```

## Veri

- V_BIST.pkl sha256: `bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51`
- V_ABD.pkl sha256: `82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e`
- V_AVR.pkl sha256: `0b53f4aa20beca3f05f8c904919a2e104f76a18d41dce40342f6dd2bd30e98f2`

## Olay SAYIMI (sonuç / getiri hesaplanmadan; uygun = likidite, geçmiş, 20 gün gelecek barı var, bölünme şüphesi dışı)

| Pazar | Tanım | 2016-22 | 2023 | 2024-26 |
|---|---|---|---|---|
| BIST | S1 | 3239 | 327 | 2531 |
| BIST | S1 sert düşüş | 674 | 116 | 768 |
| BIST | S2 | 5984 | 1045 | 4362 |
| BIST | S3 | 6701 | 957 | 5280 |
| BIST | S1 (C için 41 bar gelecek) | 3239 | 327 | 2448 |
| ABD | S1 | 9545 | 3476 | 2392 |
| ABD | S1 sert düşüş | 205 | 147 | 123 |
| ABD | S2 | 19311 | 5377 | 9715 |
| ABD | S3 | 22304 | 7168 | 10634 |
| ABD | S1 (C için 41 bar gelecek) | 9545 | 3476 | 2375 |
| AVR | S1 | 5450 | 1576 | 1266 |
| AVR | S1 sert düşüş | 34 | 22 | 19 |
| AVR | S2 | 10514 | 2313 | 4296 |
| AVR | S3 | 12180 | 3094 | 4800 |
| AVR | S1 (C için 41 bar gelecek) | 5450 | 1576 | 1253 |

| Pazar | hisse | uygun hisse-gün | bölünme şüpheli (ANA) dışlanan gün | KATI şüpheli gün |
|---|---|---|---|---|
| BIST | 581 | 827221 | 13505 | 47161 |
| ABD | 1410 | 2321165 | 86924 | 407382 |
| AVR | 579 | 1153042 | 9550 | 41825 |

## Sınırlar (önceden)
- Evren bugünün listesi: batan / kottan çıkan hisseler yok (hayatta kalma yanlılığı).
- Bilanço takvimi yok: büyük günlerin bir kısmı bilanço günüdür; model bunu bilmez.
- Komisyon, kayma, açığa satış maliyeti yok.
- BIST verisi düzeltilmiş (fi_duzelt); ABD/AVR Yahoo düzeltilmiş fiyat.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | (A) eş = aynı gün/pazar, σ250 ondalığı x likidite üçlüsü, sıkışma dışı; aynı B tanımı (sy_es_ortalama). Rastgele gün (200 çekiliş, aynı hisse aynı yıl). (C) eş aynı t, momentum beşliği x likidite üçlüsü, aynı giriş/stop/çıkış kuralı, 200 rastgele eş portföy. Mekanik üstünlük: ATR250 sıkışmayı içerir, B0 tanımsal (yalnız bilgi) |
| K2 | geleceğe bakma | EVET | geçmiş özellikler sy_gecmis yalnız t'ye kadar; kos'ta sy_gelecek_denetimi 40 olayda seriyi t'de kesip aynı tespiti mekanik denetler; test_sikisma_yeniden.py kesme testi; likidite t-1'e kadar; hücreler t günü kesitinden |
| K3 | geçerli bar | EVET | sy_veri_hazirla: H>L ve V>0 olmayan bar atılır (bayat fiyat); günlük veri, yarım bar yok (kesik 31.08.2026) |
| K4 | tekilleştirme | EVET | aynı hissede olay en az 20 bar arayla (iş tanımı; 60 değil, sıkışma olayı için iş tanımında 20); n = olay sayısı; tehlike analizinde bütün sıkışık günler kullanılır ve ay kümeli bootstrap ile; ortalama yanında medyan (C) yazılır |
| K5 | giriş fiyatı | EVET | (C) giriş = kırılım kapanışından sonraki ilk bar açılışı (Open j+1); (A)/(B) getiri değil olasılık, t kapanışı karar anı |
| K6 | veri birimi | EVET | tek kip: fi_k1_veri düzeltilmiş fiyat; ATR yüzde (TR/C önceki); AVR likidite EUR (Kur); bölünme şüphesi sy_bolunme_supheli ile çıkarılır (ANA + KATI duyarlılık) |
| K7 | hayatta kalma | EVET | evren bugünün listesi (V_*.pkl): batanlar yok; raporda yazılı; büyük hareket olasılığı batanlar yokken AŞAĞI yanlı olabilir, işlem getirisi yukarı yanlı |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem (2016-22 keşif, 2023, 2024-26/08); n<30 ÖLÇÜLEMEDİ, n>=300 güç; iki doğrulama dönemi aynı yön şartı; çoklu ölçü (B1 ana; B2/B3/S2/S3 duyarlılık, karar yalnız B1/S1) |
| K9 | ön kayıt | EVET | SY_ESIK sha256 mühür + kod sha256 ön kayıtta; ön kayıt commit+push sonra kos; kos git kapısı (commit'li ve değişmemiş) + kod sha eşitliği; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV. Ham veriden 3 olay elle doğrulanır (rapor denetim bölümü) |
| K11 | yeniden üretim | EVET | iki hücre /tmp/sikisma satır CSV'sinden bağımsız kodla yeniden üretilir; 3 olay ham veriden elle (rapor denetim) |
| K12 | ifade | EVET | 'İZ / EMARE' yalnız karar kuralı geçince; büyük hareket olasılığı ile işlem getirisi ayrı tablolarda; komisyon yok yazılır |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_sy; yasak dosyalara dokunulmaz (git diff denetimi); e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yalnız ölçüm (yön tahmini yok, öneri yok) |
