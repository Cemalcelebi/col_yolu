# SIKISMA_YENIDEN — DUYARLILIK ÖN KAYDI

SIKISMA_YENIDEN duyarlilik v1.0 (2026-11-14)

- MÜHÜR (SY_DUY sha256): `ac472e8b1e91b904f61f6a2efa35321255461bfa980ad996fbd86d7eefe9c5bf`
- KOD (SIKISMA_YENIDEN.py sha256): `ecc369cd01edacfcf965713dddb18cf9baeacca32a4d3994558c58ebc6cd19ae`
- ZAMAN (UTC): `2026-11-14 10:48:05 UTC`
- Taban tanımlar Ç174 SY_ESIK (mühür `1eb406a20091e4cb54c6cf3986f27f36e5c5ba3cbc61868ba83be53d8e7105b0`); bu çalışma BİLGİDİR, Ç174 kararı değişmez.
- Bu dosya ölçümden ÖNCE commit + push edilir; `python SIKISMA_YENIDEN.py duyarlilik` kontrol kapısı + mühür + kod sha + git kapısı geçmezse durur.

## Soru (Cemal'in itirazı, 14 Kas 2026)
"Gözüm küçük mumlardan sonra gelen mumları neden büyük görsün ki?" Hangi büyük mum ölçeğinde (k x REF) ve hangi sıkışma uzunluğunda (p) sıkışma sonrası gün aralığı eşlerden büyük çıkıyor (çıkıyorsa)? Ayrıca 'göz ne görür': ilk 20 günün en büyük mumu sıkışma mumunun kaç katı.

## Tanımlar (SY_DUY)

- Büyük mum: t+a..t+b içinde en az bir günün TR/C_önceki >= k x REF (TR = max(H, C_önceki) - min(L, C_önceki)); k ∈ [1.5, 2.0, 2.5, 3.0, 4.0]; ufuk {'20': [1, 20], '5': [1, 5]}.
- REF ATR250: t-249..t ortalama TR/C_önceki (Ç174 ile aynı; sıkışma dönemi dahil)
- REF ATR60: t-p-60..t-p-1 ortalama TR/C_önceki (60 gün, sıkışma penceresi HARİÇ; p=10 için t-70..t-11)
- REF ATR_sik: sıkışma penceresi ortalama TR/C_önceki (t-p+1..t; GÖRELİ, tanımsal: sıkışma tanımı bunu küçük yapar; yalnız kıyas, yorum dışı)
- Sıkışma (p ∈ [10, 20, 40, 60]): ort(TR/C_önceki, son p gün) <= TR/C'nin t-p-249..t-p yüzdelik %20'si VE (max C - min C)/C_t (son p gün) <= bant x sqrt(p/10); p=10 Ç174 S1 ile birebir aynı (koşuda mekanik denetlenir); aynı hissede yeni olay en az 20 bar sonra; bant SY_ESIK S1 bandı (BIST %8, ABD/AVR %6) x sqrt(p/10); başlangıç i >= 250 + p (geçerli bar sırası).
- Geçerli satır: Ç174 'uygun' (likidite alt %20 dışı, 260 bar geçmiş, 20 gün gelecek barı var, bölünme şüphesi dışı) VE p için yüzdelik ile ATR60 tanımlı.
- Eş 1: Ç174 eşi: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (hucA), p sıkışma koşulu yanlış, geçerli.
- Eş 2: EK KONTROL (Ç175 önerisi): aynı gün, aynı pazar, (ort TR/C son p gün / ATR250) oranının gün içi 20'liği x likidite üçlüsü, p sıkışma koşulu yanlış, geçerli (p=10'da oran = ATR10 / ATR250).
- En az 3 eş; olay her eş kümesinde ayrı ayrı en az 3 eşle kalır (iki kümede n farklı olabilir).
- Ölçü: KAT = olay oranı / eş oranı (eş oranı = olay başına aynı hücre eş ortalaması); ay kümeli bootstrap %95; bootstrap 2000 tekrar, küme olay ayı (t); iki yönlü bootstrap p = 2 x min(P(KAT_b <= 1), P(KAT_b >= 1)), en az 1/n.
- Dönemler: [['2016-22', '2016-01-01', '2022-12-31'], ['2023', '2023-01-01', '2023-12-31'], ['2024-26', '2024-01-01', '2026-08-31']] + birleşik {'2023+': ['2023', '2024-26']}. Ana okuma: ABD ve AVR, 2023 / 2024-26 / 2023+ (bilgi); BIST ve 2016-22 bilgi.
- Çoklu karşılaştırma: BH q 0.1; aile: REF ATR250 ve ATR60, üç ayrı dönem (2023+ hariç), iki eş kümesi, bütün k, ufuk, p, pazar (5x2x2x4x2x3x3 = 1440 sınama). BH yalnız BİLGİ; hiçbir hücre tek başına bulgu değildir; karar Ç174'tedir.
- Yön etiketi: n < 30 ÖLÇÜLEMEDİ; alt95 > 1 'KAT>1'; üst95 < 1 'KAT<1'; değilse 'belirsiz' (etiket bilgi, karar değil).
- Dağılım R_sik: ilk 20 günün en büyük TR/C_önceki / sıkışma penceresi ort TR/C_önceki (Cemal'in gözü: küçük mumlardan sonra gelen mum)
- Dağılım R_250: ilk 20 günün en büyük TR/C_önceki / ATR250
- Dağılım R_60: ilk 20 günün en büyük TR/C_önceki / ATR60
- Dağılım es_agirlik: eş dağılımı: her olayın hücresindeki eşler 1 / (hücre eş sayısı) ağırlıkla (her olay toplam 1 ağırlık)
- Ç174 tutarlılık (durdurucu): p=10, eş1, ufuk 20: k=3 ATR250 = Ç174 B1; k=3 ATR_sik = Ç174 B0; ufuk 5, k=3 ATR250 = Ç174 B1_5; her pazar x dönemde n, olay oranı, eş oranı, KAT sikisma_sonuc.json ile 1e-9 içinde aynı olmalı, değilse koşu durur.
- Görsel örnek: Ç174 S1 olayları (p=10, eş1 ile en az 3 eş), ABD ['2023', '2024-26']; 20 olay + 20 eş, tohum 27; her seçilen olay için aynı gün, aynı hucA hücresindeki eşlerden (S1 koşulu yanlış, geçerli) rastgele bir hisse-gün; 40 grafik aynı tohumla karıştırılır; numara 1-40; 'olay' / 'eş' etiketi yalnız anahtarda; 120 bar önce + 20 bar sonra; ln(1,10) = 40 piksel; son 10 gün (t-9..t) gri gölge; t ile t+1 arası kesikli dikey çizgi; alt panel günlük TR/C_önceki (%) çubukları; yatay çizgiler 2 x ve 3 x ATR250(t).
- Bağımsız yeniden üretilecek hücreler (önceden): [{"pazar": "ABD", "p": 10, "ref": "ATR250", "k": 2.0, "ufuk": "20", "es": "es1", "donem": "2023+"}, {"pazar": "AVR", "p": 40, "ref": "ATR60", "k": 3.0, "ufuk": "20", "es": "es2", "donem": "2024-26"}].

## Eşik sözlüğü (SY_DUY, kararlı JSON)

```json
{
 "ana": "ABD ve AVR, 2023 / 2024-26 / 2023+ (bilgi); BIST ve 2016-22 bilgi",
 "bh": {
  "aile": "REF ATR250 ve ATR60, üç ayrı dönem (2023+ hariç), iki eş kümesi, bütün k, ufuk, p, pazar (5x2x2x4x2x3x3 = 1440 sınama)",
  "not": "BH yalnız BİLGİ; hiçbir hücre tek başına bulgu değildir; karar Ç174'tedir",
  "q": 0.1
 },
 "birlesik": {
  "2023+": [
   "2023",
   "2024-26"
  ]
 },
 "bootstrap": {
  "guven": [
   0.025,
   0.975
  ],
  "kume": "olay ayı (t)",
  "n": 2000,
  "p": "iki yönlü bootstrap p = 2 x min(P(KAT_b <= 1), P(KAT_b >= 1)), en az 1/n",
  "tohum": 1476
 },
 "buyuk_tanim": "t+a..t+b içinde en az bir günün TR/C_önceki >= k x REF (TR = max(H, C_önceki) - min(L, C_önceki))",
 "c174_muhur": "1eb406a20091e4cb54c6cf3986f27f36e5c5ba3cbc61868ba83be53d8e7105b0",
 "dagilim_olcu": {
  "R_250": "ilk 20 günün en büyük TR/C_önceki / ATR250",
  "R_60": "ilk 20 günün en büyük TR/C_önceki / ATR60",
  "R_sik": "ilk 20 günün en büyük TR/C_önceki / sıkışma penceresi ort TR/C_önceki (Cemal'in gözü: küçük mumlardan sonra gelen mum)",
  "es_agirlik": "eş dağılımı: her olayın hücresindeki eşler 1 / (hücre eş sayısı) ağırlıkla (her olay toplam 1 ağırlık)",
  "yuzdelik": [
   0.25,
   0.5,
   0.75
  ]
 },
 "denetim_hucre": [
  {
   "donem": "2023+",
   "es": "es1",
   "k": 2.0,
   "p": 10,
   "pazar": "ABD",
   "ref": "ATR250",
   "ufuk": "20"
  },
  {
   "donem": "2024-26",
   "es": "es2",
   "k": 3.0,
   "p": 40,
   "pazar": "AVR",
   "ref": "ATR60",
   "ufuk": "20"
  }
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
 "es": {
  "es1": "Ç174 eşi: aynı gün, aynı pazar, σ250 ondalığı x likidite üçlüsü (hucA), p sıkışma koşulu yanlış, geçerli",
  "es2": "EK KONTROL (Ç175 önerisi): aynı gün, aynı pazar, (ort TR/C son p gün / ATR250) oranının gün içi 20'liği x likidite üçlüsü, p sıkışma koşulu yanlış, geçerli (p=10'da oran = ATR10 / ATR250)",
  "min_es": 3,
  "olay_secimi": "olay her eş kümesinde ayrı ayrı en az 3 eşle kalır (iki kümede n farklı olabilir)",
  "oran_kova": 20
 },
 "gecerli": "Ç174 'uygun' (likidite alt %20 dışı, 260 bar geçmiş, 20 gün gelecek barı var, bölünme şüphesi dışı) VE p için yüzdelik ile ATR60 tanımlı",
 "grafik": {
  "alt_panel": "günlük TR/C_önceki (%) çubukları; yatay çizgiler 2 x ve 3 x ATR250(t)",
  "alt_px": 210,
  "donem": [
   "2023",
   "2024-26"
  ],
  "dpi": 100,
  "es_secimi": "her seçilen olay için aynı gün, aynı hucA hücresindeki eşlerden (S1 koşulu yanlış, geçerli) rastgele bir hisse-gün",
  "esik": [
   2.0,
   3.0
  ],
  "fiyat_max_px": 760,
  "fiyat_min_px": 260,
  "genislik": 1200,
  "golge": "son 10 gün (t-9..t) gri gölge; t ile t+1 arası kesikli dikey çizgi",
  "kume": "Ç174 S1 olayları (p=10, eş1 ile en az 3 eş)",
  "n_es": 20,
  "n_olay": 20,
  "normal": "fiyat / C_t x 100, ln ekseni",
  "once": 120,
  "pazar": "ABD",
  "px_ln110": 40,
  "sira": "40 grafik aynı tohumla karıştırılır; numara 1-40; 'olay' / 'eş' etiketi yalnız anahtarda",
  "sonra": 20,
  "tohum": 27
 },
 "k": [
  1.5,
  2.0,
  2.5,
  3.0,
  4.0
 ],
 "olcu": "KAT = olay oranı / eş oranı (eş oranı = olay başına aynı hücre eş ortalaması); ay kümeli bootstrap %95",
 "pencere": [
  10,
  20,
  40,
  60
 ],
 "ref": {
  "ATR250": "t-249..t ortalama TR/C_önceki (Ç174 ile aynı; sıkışma dönemi dahil)",
  "ATR60": "t-p-60..t-p-1 ortalama TR/C_önceki (60 gün, sıkışma penceresi HARİÇ; p=10 için t-70..t-11)",
  "ATR_sik": "sıkışma penceresi ortalama TR/C_önceki (t-p+1..t; GÖRELİ, tanımsal: sıkışma tanımı bunu küçük yapar; yalnız kıyas, yorum dışı)"
 },
 "sikisma": {
  "ara": 20,
  "bant": "SY_ESIK S1 bandı (BIST %8, ABD/AVR %6) x sqrt(p/10)",
  "bas": "i >= 250 + p (geçerli bar sırası)",
  "dagilim": 250,
  "tanim": "ort(TR/C_önceki, son p gün) <= TR/C'nin t-p-249..t-p yüzdelik %20'si VE (max C - min C)/C_t (son p gün) <= bant x sqrt(p/10); p=10 Ç174 S1 ile birebir aynı (koşuda mekanik denetlenir); aynı hissede yeni olay en az 20 bar sonra",
  "yuzdelik": 0.2
 },
 "surum": "SIKISMA_YENIDEN duyarlilik v1.0 (2026-11-14)",
 "tutarlilik_c174": "p=10, eş1, ufuk 20: k=3 ATR250 = Ç174 B1; k=3 ATR_sik = Ç174 B0; ufuk 5, k=3 ATR250 = Ç174 B1_5; her pazar x dönemde n, olay oranı, eş oranı, KAT sikisma_sonuc.json ile 1e-9 içinde aynı olmalı, değilse koşu durur",
 "ufuk": {
  "20": [
   1,
   20
  ],
  "5": [
   1,
   5
  ]
 },
 "yon": "n < 30 ÖLÇÜLEMEDİ; alt95 > 1 'KAT>1'; üst95 < 1 'KAT<1'; değilse 'belirsiz' (etiket bilgi, karar değil)"
}
```

## Olay SAYIMI (sonuç hesaplanmadan; en az 3 eşi olan olay)

| Pazar | p | olay (geçerli, tümü) | eş1 2016-22 | eş1 2023 | eş1 2024-26 | eş2 2016-22 | eş2 2023 | eş2 2024-26 |
|---|---|---|---|---|---|---|---|---|
| BIST | 10 | 6097 | 3196 | 327 | 2529 | 1443 | 203 | 1479 |
| BIST | 20 | 2266 | 1183 | 94 | 975 | 662 | 61 | 695 |
| BIST | 40 | 751 | 429 | 8 | 309 | 286 | 7 | 256 |
| BIST | 60 | 419 | 240 | 1 | 173 | 170 | 1 | 145 |
| ABD | 10 | 15413 | 9540 | 3476 | 2392 | 7626 | 3245 | 2270 |
| ABD | 20 | 5292 | 3547 | 1287 | 458 | 3136 | 1275 | 458 |
| ABD | 40 | 1927 | 1396 | 437 | 94 | 1325 | 437 | 94 |
| ABD | 60 | 1207 | 885 | 285 | 37 | 870 | 285 | 37 |
| AVR | 10 | 8292 | 5401 | 1566 | 1266 | 2963 | 818 | 903 |
| AVR | 20 | 3094 | 2168 | 655 | 260 | 1465 | 480 | 244 |
| AVR | 40 | 1242 | 898 | 267 | 74 | 691 | 220 | 71 |
| AVR | 60 | 865 | 667 | 153 | 42 | 528 | 139 | 42 |

## Sınırlar (önceden)
- Evren bugünün listesi (batanlar yok). Bilanço takvimi yok. Uzun pencerede (p=40, 60) olaylar aynı uzun sıkışmanın ardışık günleri olabilir (20 bar ara; ay kümeli bootstrap bunu kısmen taşır).
- Sıkışma koşulu p günlük ORTALAMAYI tek gün dağılımının %20 yüzdeliğiyle kıyaslar: uzun p'de pencerenin yalnız bir kısmı dar olsa da koşul doğru olabilir (sentetik testte 60 günlük dar bölgede p=60 koşulu dar bölgenin ~15. gününde doğru oldu); yani p = 'en az p gün dar' değil, 'son p günün ortalaması dar'dır.
- Ç174 tutarlılık farkı ~1e-11 olabilir: sikisma_sonuc.json pandas to_json 10 basamak yazar; eşik 1e-9.
- ATR_sik REF göreli ve tanımsaldır (sıkışma tanımı onu küçük yapar); yalnız 'göz' kıyası, yorum dışı.
- 5 k x 3 REF x 2 ufuk x 4 p x 2 eş x 3 pazar x 4 dönem = 2.880 satır: tek hücre bulgu değildir.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş1 = Ç174 eşi (aynı gün/pazar, σ250 ondalığı x likidite üçlüsü, p sıkışma dışı); eş2 = aynı gün, (ort TR/C son p / ATR250) 20'liği x likidite üçlüsü (sıkışmanın ATR250'yi düşürmesinden gelen mekanik farkı dengeler); aynı büyük mum tanımı eşlere de uygulanır; ATR_sik göreli/tanımsal: yorum dışı |
| K2 | geleceğe bakma | EVET | sy_duy_gecmis yalnız t'ye kadar (sıkışma, ATR250, ATR60, oran); büyük mum sy_duy_sonuc'ta t+1..t+20; test_sikisma_yeniden.py 12) kesme testi; hücreler t günü kesiti; ATR60 t-p-60..t-p-1 |
| K3 | geçerli bar | EVET | sy_veri_hazirla (Ç174): H>L ve V>0 olmayan bar atılır; günlük veri; fiyat kesiği 31.08.2026 |
| K4 | tekilleştirme | EVET | aynı hissede olay en az 20 bar arayla (her p için); n = olay sayısı; ay kümeli bootstrap; dağılımlarda medyan + %25-75 |
| K5 | giriş fiyatı | UYGULANMAZ | getiri / işlem yok; yalnız t kapanışındaki bilgiyle t+1..t+20 gün aralığı olasılığı ve dağılımı |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş fiyat; TR yüzde (TR / önceki kapanış) her REF için aynı birim; bölünme şüphesi Ç174 sy_bolunme_supheli ile dışarıda |
| K7 | hayatta kalma | EVET | evren bugünün listesi (batanlar yok); raporda yazılı; büyük gün olasılığı olay ve eşte birlikte etkilenir, KAT yönü yazılı sınır |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem (+2023+); n<30 ÖLÇÜLEMEDİ; 1440 sınamalık aile BH q 0,10 yalnız bilgi; hiçbir hücre tek başına bulgu değil; karar Ç174 |
| K9 | ön kayıt | EVET | SY_DUY sha256 mühür + SIKISMA_YENIDEN.py sha256 + olay SAYIMI (sonuçsuz) DUYARLILIK_ON_KAYIT.md'de; commit + push sonra `duyarlilik`; kos öncesi kontrol kapısı + mühür + kod sha + git kapısı; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV; 2 grafik ham veriden elle doğrulanır (rapor denetim) |
| K11 | yeniden üretim | EVET | p=10 Ç174 hücreleri koşu içinde mekanik eşitlik denetimi (durdurucu); 2 hücre (SY_DUY denetim_hucre) satır dosyasından bağımsız kodla yeniden üretilir |
| K12 | ifade | EVET | 'bulgu / iz' sözü yok: duyarlılık bilgidir; KAT>1 / KAT<1 yalnız güven aralığı etiketi; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_sy korunur; yasak defter dosyalarına dokunulmaz (git diff); e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; yalnız ölçüm |
