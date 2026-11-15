# DIP_COL_AYRIM — ÖN KAYIT (DIP_COL_AYRIM v1.0 (2026-11-14))

Yazım: 2026-11-14 13:41:00 UTC. Bu dosya ölçümden ÖNCE yazıldı: yalnız sinyaller tarandı ve sayıldı; hiçbir getiri / olasılık hesaplanmadı.

Soru (Cemal, 14 Kas 2026): çöl formasyonuyla gerçek dip oluşumunu birbirinden ayırabiliyor muyuz?

## Tanım

- dip16 = `FON_IZI.fi_k13_tara(V, FI_K16_GEVSEK)` (Ç75 düzgün dip gevşek), dip17 = `FON_IZI.fi_k17_tara(V, FI_K17_ESIK)` (Ç78 iki yuvarlama Y1), col = `FON_IZI.fi_k24_tara(d, FI_K24)` kural günleri (K24 iki evre). Kod DEĞİŞTİRİLMEDİ; FON_IZI içe alınır.
- 'Gerçek dip' = dip16 ya da dip17; 'çöl' = col. Sinyal günü t; giriş t'den sonraki ilk geçerli bar açılışı (ORTAK_CETVEL).
- Kümeler (gerçek zamanlı, yalnız [t-60, t]): A yalnız dip, B yalnız çöl, C ikisi (geç olan sinyal günü), D aynı gün rastgele 'hiçbiri' (bilgi).
- AYRIM kuralı: DCA_TASARIM 'ayrim' (aşağıda tam metin). Karar hücreleri ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26; BIST bilgi; 2016-22 keşif.
- Zorunlu düzeltme (sonuç görülmeden): FON_IZI tarayıcıları seri TOPLAM uzunluğu < 400 / 200 ise hisseyi atlar (geleceğe bakma); burada sinyal ancak bar konumu i >= 399 (dip) / 199 (çöl) ise tutulur.

## Mühür satırları

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`
DCA_PARAM_SHA: `9b01d72c39ff18b0687663d02246cc76ceeefe792bfd5cbe8cef6cf36e6ec53b`
DCA_TASARIM_SHA: `6c4256471ac0eda9a18a8473ecc0de4c08890bc67c60d16520bfbb33b2526fca`
DCA_KOD_SHA: `3e3a974acc080288440a8e396463dab9fa44b9abf82e259405e4d696ccbbb884`
SINYAL_SHA: `98a437a78c6f4bffe3de139910ff3fd153041b702128a0c02bf702d046057e74`

- DCA_PARAM_SHA = sha256(FI_K16_GEVSEK, FI_K17_ESIK, FI_K24 + tarayıcı fonksiyonlarının kaynak sha'sı; JSON sort_keys). DCA_KOD_SHA = sha256(DIP_COL_AYRIM.py). SINYAL_SHA = sha256(sıralı sinyal tablosu CSV; pazar, sembol, tarih, tur, i).

## Parametre sözlüğü (FON_IZI'den)

```json
{
 "FI_K16_GEVSEK": {
  "bant": 10.0,
  "bar": [
   30,
   80
  ],
  "dip_taban": 0.2,
  "dusus": -0.4,
  "egim": [
   -9.0,
   9.0
  ],
  "mum": 99.0,
  "u": 0.0
 },
 "FI_K17_ESIK": {
  "bar": [
   25,
   120
  ],
  "derin": [
   -0.3,
   -0.05
  ],
  "dusus": -0.4,
  "m_son": 5,
  "r2": 0.4,
  "tepe": [
   0.15,
   0.85
  ],
  "ust_dip": 1.03,
  "yan": 10
 },
 "FI_K24": {
  "bbw_oran": 0.7,
  "bbw_pencere": 15,
  "delen_en_cok": 2,
  "dusus": -0.3,
  "once": 10,
  "once_alt": 0.8,
  "seri": 5,
  "tekrar": 60
 },
 "kaynak_sha": {
  "_fi_k17_parabol": "6eecf7fa06b1247315b562be5d038c03feb318d9be6578648230c459db9be7b9",
  "_fi_k23_yon": "9c1396552086293d5f4f5c8a89acd59acac64275ed58e1b27160fa56daac9272",
  "fi_k13_olc": "c5c1e5cdffc7cb621b2b2e0922ae6a03adea955fbcbf9a36fefc79fe60e56d84",
  "fi_k13_tara": "608561d448398dc3c080f5f63cdf18dcf367333df6f84370d83d710d055de023",
  "fi_k17_olc": "a0df75286583f0f37d802afdb826a780076e7f5b5a49ba244ae115fcb903840b",
  "fi_k17_tara": "5e98d65fac5b2b6a2c5602afd5d2554228460ef2821e6f380facc27072979b6f",
  "fi_k24_tara": "eca60a7d4c07df59e94c3e791984821c233c46aecc6d2f0b96d78bb263134c05"
 }
}
```

## Tasarım (DCA_TASARIM; mühürlü)

```json
{
 "D_deneme": 200,
 "D_tohum": 1414,
 "ayrim": {
  "bootstrap": "OC_ESIK olcu bootstrap (2000), tohum 27, guven [0.025, 0.975]",
  "coklu": "karar dört hücre x iki referansın KESİŞİMİ (hepsi tutmalı; intersection-union): BH gerekmez; EMARE yalnız bilgi",
  "fark_r60": "ortalama eşli fark farkı C - ref, aynı ay kümeli ortak bootstrap (bilgi)",
  "genel": "4 karar hücresi VAR -> AYRIM VAR; >= 1 VAR -> EMARE (AYRIM; hücreler); 4 hücre YOK -> AYRIM YOK; aksi ÖLÇÜLEMEDİ",
  "hucre_var": "up100 kat farkı alt95 > 0 (A'ya ve B'ye karşı) VE dn50 kat farkı alt95 > 0 değil (A'ya ve B'ye karşı)",
  "hucre_yok": "VAR değil VE C n250 >= OC_ESIK etiket n_yeter (1.000) VE A, B n250 >= 30",
  "kume": "giriş ayı; C ve ref'in aylarının birleşimi yerine koyarak çekilir, iki kümenin seçilen aylardaki toplamlarıyla KAT_C - KAT_ref",
  "olcu": [
   "up100",
   "dn50"
  ],
  "olculemedi": "C, A ya da B n250 < 30; ya da VAR değil ve C n250 < 1.000",
  "ref": [
   "A",
   "B"
  ]
 },
 "gecmis_asgari": {
  "col": 200,
  "dip16": 400,
  "dip17": 400,
  "tanim": "FON_IZI tarayıcıları seri uzunluğu (gelecek dahil) < 400 / 200 ise hisseyi atlar; burada sinyal ancak bar konumu i >= asgari-1 ise tutulur (t günü geçmişi yeterli): geleceğe bakma düzeltmesi, sonuç görülmeden"
 },
 "kume": {
  "A": "dip t, [t-60, t] çöl yok",
  "B": "çöl t, [t-60, t] dip yok",
  "C": "t'de bir tür, [t-60, t] öteki tür; aynı (sembol, gün) tek",
  "D": "A ∪ B ∪ C ham sinyal günü başına aynı gün aynı pazar rastgele hisse: o gün geçerli bar, [t-60, t] hiçbir sinyal yok, evren_bas <= t; en çok 200 deneme; tohum 1414 + pazar sırası",
  "DIP_TUM": "bütün dip sinyalleri (A ∪ C'nin dip günleri); yalnız uzaklık kovası bilgisi"
 },
 "pazar": [
  "ABD",
  "AVR",
  "BIST"
 ],
 "pencere": 60,
 "pencere_tanim": "hissenin kendi geçerli bar takviminde [i-60, i] (dahil): t günü i'de öteki türün sinyali bu aralıkta varsa C",
 "sinyal": {
  "col": "FON_IZI.fi_k24_tara(d, FON_IZI.FI_K24) kural == True tarih günü (K24 iki evre)",
  "dip": [
   "dip16",
   "dip17"
  ],
  "dip16": "FON_IZI.fi_k13_tara(V, FON_IZI.FI_K16_GEVSEK) bilgi günü (Ç75)",
  "dip17": "FON_IZI.fi_k17_tara(V, FON_IZI.FI_K17_ESIK) bilgi günü (Ç78, K17 Y1)",
  "veri": "ORTAK_CETVEL.oc_veri temiz seriler (geçerli bar süzgeci, kriz kesiği) üzerinde tarama"
 },
 "surum": "1.0",
 "uzaklik_kova": [
  [
   0,
   10
  ],
  [
   11,
   30
  ],
  [
   31,
   60
  ],
  [
   61,
   120
  ],
  [
   121,
   250
  ],
  [
   251,
   null
  ]
 ],
 "uzaklik_tanim": "dip sinyali i ile en yakın ÖNCEKİ (<= i) çöl sinyali arasındaki bar; hiç yoksa son kova; yalnız bilgi (ABD + AVR, 2023 + 2024-26 birlikte)"
}
```

## OLAY SAYIMI (getiri hesaplanmadan; ham sinyal günü dönemine göre; oc_olc tekilleştirmesinden ÖNCE)

| pazar | donem | dip16 | dip17 | col | A | B | C | DIP_TUM | C_col_gec |
|---|---|---|---|---|---|---|---|---|---|
| ABD | 2016-22 | 1576 | 1516 | 4699 | 1795 | 4258 | 1725 | 3075 | 441 |
| ABD | 2023 | 1172 | 787 | 1507 | 1328 | 1202 | 930 | 1952 | 305 |
| ABD | 2024-26 | 2958 | 2057 | 4585 | 3207 | 3836 | 2535 | 4983 | 749 |
| ABD | tümü | 5706 | 4360 | 10791 | 6330 | 9296 | 5190 | 10010 | 1495 |
| AVR | 2016-22 | 190 | 398 | 1102 | 300 | 1034 | 356 | 584 | 68 |
| AVR | 2023 | 14 | 23 | 128 | 18 | 122 | 24 | 37 | 6 |
| AVR | 2024-26 | 67 | 83 | 382 | 79 | 365 | 85 | 148 | 17 |
| AVR | tümü | 271 | 504 | 1624 | 397 | 1533 | 465 | 769 | 91 |
| BIST | 2016-22 | 323 | 343 | 1372 | 410 | 1286 | 340 | 662 | 86 |
| BIST | 2023 | 217 | 170 | 472 | 166 | 416 | 277 | 385 | 56 |
| BIST | 2024-26 | 201 | 188 | 956 | 214 | 891 | 235 | 389 | 65 |
| BIST | tümü | 741 | 701 | 2800 | 790 | 2593 | 852 | 1436 | 207 |

- C_col_gec: C olaylarından çöl sinyalinin geç geldiği (dip önce, çöl sonra) olanlar; kalanı dip geç.
- Not: bir dip olayı A sayılıp 60 gün içinde gelen çölle C de olabilir (gerçek zamanlı sınıf).

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = ORTAK_CETVEL oc_olc (aynı giriş günü, aynı pazar, momentum beşlisi x likidite üçlüsü; 200 plasebo portföy); her küme AYNI cetvelle; AYRIM kümeler arası kat farkıdır (C vs A, C vs B), ikisi de eşe göre kat; mekanik üstünlük: C tanımı (iki sinyal 60 günde) çöküş sonrası bağlamı seçer, A ve B de çöküş sonrası (dip16/dip17 >= %40 düşüş, K24 >= %30 düşüş): bağlam benzer; D aynı gün rastgele hisse (bilgi) |
| K2 | geleceğe bakma | EVET | tarayıcılar t'de yalnız <= t barlarını kullanır; seri uzunluğu şartı (FON_IZI n < 400 / 200) geleceğe bakıyordu -> bar konumu i >= 399 / 199 süzgeci; küme sınıfı yalnız [t-60, t]; test_dip_col_ayrim 'kesme' testi (sentetik) + kos'ta gerçek ABD örnekleminde seri t'de kesilince sinyal aynı (dca_gelecek_denetim) |
| K3 | geçerli bar | EVET | tarama OC.oc_veri temiz seriler üzerinde (H>L, V>0, O/H/L/C>0); sinyal barı geçersizse oc_olay_hazirla düşürür |
| K4 | tekilleştirme | EVET | her küme oc_olc içinde hissede 60 işlem gününde tek olay; C içinde aynı (sembol, gün) tek; n = bağımsız olay; medyan raporda |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (oc_olay_hazirla) |
| K6 | veri birimi | EVET | tek kip fi_k1_veri düzeltilmiş V_*.pkl (+k34_yahoo); getiri oranı; AVR likidite EUR; bölünme şüphesi OC geçmiş penceresi |
| K7 | hayatta kalma | EVET | evren bugün işlem görenler (+ ABD k34 nakdi biten, yine yaşayan); batanlar yok; raporda 'yukarı yanlı / -%50 aşağı yanlı' |
| K8 | örneklem ve dönem | EVET | 3 pazar x 3 dönem; n < 30 ÖLÇÜLEMEDİ; ayrım YOK yalnız C n250 >= 1.000; kesişim kuralı (BH gerekmez, ön kayıtta); olay sayıları ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | ön kayıtta CETVEL / KOD / GÜÇ sha (oc_kapi_satirlari), DCA_PARAM_SHA (FI_K16_GEVSEK, FI_K17_ESIK, FI_K24 + tarayıcı kaynak kodu), DCA_TASARIM_SHA, DCA_KOD_SHA, SINYAL_SHA; kos önce oc_kapi + dca_kapi (git işlenmiş, değişmemiş) çağırır |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV; 3 olay ham veriden elle denetimde yeniden hesaplanır |
| K11 | yeniden üretim | EVET | satır verisi /tmp/dip_col_ayrim/olay_<küme>.csv.gz; rapor sonrası >= 2 hücre (C ve A ABD 2024-26) bağımsız kodla yeniden üretilir; ayrım bootstrap'ı satır verisinden |
| K12 | ifade | EVET | etiketler yalnız oc_etiket / oc_olasilik_etiket ve ön kayıtlı ayrım kuralıyla; fiyat değişimi, komisyon yok; sayı / yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_dca; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; ücretli veri / Tiingo yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## Test

`python test_dip_col_ayrim.py` (sentetik: sinyal tespiti, kümeleme, geleceğe bakma kesme testi, cetvel çağrısı, ayrım kuralı, kapı, çakışma kapısı, e-posta / anahtar taraması).
