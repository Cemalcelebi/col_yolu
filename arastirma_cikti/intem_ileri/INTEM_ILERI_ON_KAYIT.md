# INTEM İLERİ TEST — ÖN KAYIT (INTEM_ILERI v1.0 (2026-11-14))

Yazım: 2026-11-14T14:18:07Z. Bu dosya ölçümden ÖNCE yazıldı. Bu modülde görülmemiş veride hiçbir getiri / eşli fark / olasılık / K45 hedef oranı HESAPLANMADI; yalnız Ç124 cetveli yeniden üretildi, görülmemiş hisseler tarandı ve olaylar sayıldı. Ön kayıt + modül commit + push edilir, SONRA `python INTEM_ILERI.py kos`.

Cemal (14 Kas 2026): "önceki aşamalardan çıkan kuralları DEĞİŞTİRMEDEN, görülmemiş veride dene"; "her aşamada aynı ölçüm kriterleri; sonucu beğenmediğimiz için eşikle oynanmaz".

İleri test edilecek başka kural yok: Aşama 2 (K24 iki evre çöl) ve Aşama 4 (düzgün dip vs çöl) ORTAK CETVEL ile ÖLÇÜLEMEDİ / TUTMADI çıktı, kural üretmedi; Aşama 3 (D9) sonucu gelirse ana model ayrı iş açar. Konu: sıkışma ailesindeki tek EMARE Ç124.

## 1. Kural (DEĞİŞMEZ; FON_IZI içe alınır)

- K44 INTEM parmak izi: `fi_k23_parmak(d, L)` sekiz ölçü (dusus, egim, mum, konum, rsi, bbw, hacim, yesil); INTEM 2026-10-09 bitişli L = 20 (ana) ve L = 10 (bilgi) barlık pencere.
- K44 birebir eşleşme: sekiz ölçünün pazar havuzundaki yüzdeliği INTEM yüzdeliğinin +-band içinde (ABD Ç124: 0,125). Cetvel = Ç124 ABD havuzu (V_ABD ham, bütün L barlık pencereler); görülmemiş pencereler bu SABİT cetvele göre yüzdeliğe çevrilir.
- K45 kendi ölçüsü: girişten (açılış) ilk +-%5 / 8 / 12 hangisi önce (20 gün, High / Low); kutu (son 10 bar) çıkışı; yukarı çıkışta +%8 / -%8 koşullu; oynaklık eşli rastgele taban (10 tohum).

```json
{"FI_K44": {"ayri": 60, "band": 0.125, "band_genis": 0.2, "bitis": "2026-10-09", "esik": 0.2, "n_min": 30, "olcu": ["dusus", "egim", "mum", "konum", "rsi", "bbw", "hacim", "yesil"], "pencere": [20, 10], "sembol": "INTEM", "ufuk": [20, 60, 120]}, "FI_K45": {"ana_esik": 0.08, "bekle": 20, "esik": [0.05, 0.08, 0.12], "fark_esik": 0.1, "kutu_bar": 10, "n_min": 30, "tohum_n": 10}}
```

INTEM hedef ölçüleri ve Ç124 ABD cetvelindeki hedef yüzdelikleri:

| L | dusus | egim | mum | konum | rsi | bbw | hacim | yesil |
|---|---|---|---|---|---|---|---|---|
| 20 ölçü | -0.4182 | -0.0091 | 1.4199 | 0.1649 | 33.6717 | 0.6875 | 0.6709 | 0.3500 |
| 20 yüzdelik | 0.1713 | 0.0819 | 0.9307 | 0.1718 | 0.0771 | 0.4072 | 0.0766 | 0.1171 |
| 20 ham aralık (Ç124 eşleşmelerinde min..maks, bilgi) | -0.628..-0.312 | -0.0311..-0.00418 | 1.2..68.4 | 0.0437..0.296 | 18.5..40.7 | 0.575..0.798 | 0.116..0.802 | 0.1..0.4 |
| 10 ölçü | -0.4182 | 0.0003 | 1.1054 | 0.3730 | 33.6717 | 0.6875 | 0.4692 | 0.5000 |
| 10 yüzdelik | 0.1468 | 0.4906 | 0.6750 | 0.3670 | 0.0775 | 0.2368 | 0.0153 | 0.5227 |
| 10 ham aralık (Ç124 eşleşmelerinde min..maks, bilgi) | -0.684..-0.314 | -0.00187..0.00234 | 1.02..1.22 | 0.235..0.516 | 28.2..40.6 | 0.554..0.795 | 0.291..0.728 | 0.5..0.5 |

## 2. Görülmemiş veri (tam liste)

- (a) Avrupa: YOK: Ç124 V_AVR'yi kullandı (k44_eslesme AVR 117 + 271 eşleşme, Ç124 notu 'AVR 2016-22 +15,0 (n 92)'); görülmüş veri.
- (b) ABD: OC.oc_veri('ABD') kaynağı 'k34_yahoo' olan hisseler (V_ABD'de olmayan k34 nakdi biten şirketler); Ç124 havuzunda ve eşleşmelerinde yok (k44_eslesme ABD sembollerinden hiçbiri k34-yalnız değil); evrene k34_evren ilk_giris gününden itibaren (OC 'evren_once' süzgeci), 2021-01 .. 2026-08-31. Sayı: 1465 hisse (Ç124 evreni V_ABD 1411 hisse; k44_eslesme ABD sembolleriyle kesişim 0, denetlendi).
- (c) Dönem: YOK: Ç124 verisi 2015-06-01 .. 2026-10 (kriz sonrası dahil); kullanılmamış dönem yok.
- Örtüşme: V_ABD hisseleri (Ç124 evreni) ölçüme GİRMEZ; görülmemiş k34 hisseleri yalnız sinyal kaynağıdır; eş / plasebo havuzu OC'nin bütün ABD havuzudur (V_ABD + k34; kontrol grubu, sinyal değil).

**Görülmemiş veri yalnız (b): ABD k34 ekindeki nakit yakan, bugün işlem gören 2021+ şirketler. Avrupa görülmüş olduğu için AVR karar hücreleri bu ileri testte BOŞTUR; en iyi etiket 'EMARE (ABD-ADAY; AVR verisi yok)' olabilir.**

Ç124 yeniden üretimi (cetvelin doğru kurulduğunun kanıtı):

| L | Ç124 ABD eşleşme | yeniden üretilen | ortak | INTEM izi k44_parmak ile aynı |
|---|---|---|---|---|
| 20 | 317 | 317 | 317 | EVET |
| 10 | 39 | 39 | 39 | EVET |

## 3. Mühür satırları

### ORTAK CETVEL (aynen; OC.oc_kapi_satirlari())

CETVEL_SHA: `4763c4586262b7a60c55fbe43d9b21855b0a2afd9e579331984d3fba8b48491e`
CETVEL_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb`
GUC_SHA: `7921963e925e86a1913abf8ac4131932003f1b82cebf29a8d28310e08a49a3bd`

### Bu aşama

II_ESIK_SHA: `fdfe6f1dd434f5f07fc00a5f31760c286da8e68aa96ed2511528fa4abdda6c3f`
FI_PARAM_SHA: `14d74613cf7546b4e90a81238b075a8f1f11f351f5e3cd07b859c2fd8072f92c`
FI_KOD_SHA: `36dc4936c55c3ac74bc8eb6c092dfa9be74a406b293f7ee5d7541dbee39ac85d`
II_KOD_SHA: `ceacc5f6e3ca2677f76cef05415d12253c03cc9f488cd283909128402be30913`
HEDEF_CETVEL_SHA: `81cd77c1e0c8b0279f56f8d5f2cd922fe89e25e6c1b01886115fd1c4c1794a32`
OLAY_SHA: `e3b9f318a4fd0ec179618983bf79fbe24cc15da3be94f2c4a09cc81cbf8a0eaa`

- FI_PARAM_SHA = sha256(FI_K44 + FI_K45 + FI_K23 kanonik JSON); FI_KOD_SHA = sha256(fi_k23_parmak, fi_k44_havuz, fi_k44_yuzdelik, fi_k44_eslesme, fi_k27_tekil, fi_k45_ilk_hedef, fi_k45_kutu_cikis, fi_k45_olc, fi_k45_rastgele_oynak, fon_izi_k45 kaynak kodu); II_KOD_SHA = sha256(INTEM_ILERI.py bayt); HEDEF_CETVEL_SHA = sha256(INTEM ölçüleri, hedef yüzdelikleri, bant, havuz n); OLAY_SHA = sha256(pencere, sembol, sinyal tarihi sıralı csv). kos hepsini yeniden hesaplar; biri farklıysa DURUR.

### II_ESIK (tam metin)

```json
{
 "band": {
  "10": 0.125,
  "20": 0.125
 },
 "band_kaynak": "Ç124 ABD eşleşmelerinin bandı (k44_eslesme.csv, ABD L20 ve L10: 0,125); band_genis kuralı (eşleşme < 30 -> 0,20) Ç124 havuzunda tetiklenmedi, ileri testte bant Ç124'teki değerinde DONDURULUR",
 "cetvel": "Ç124 ABD havuzu: FON_IZI.fi_k44_havuz(V_ABD ham, L) (bütün hisselerin bütün L barlık pencereleri, süzgeçsiz); INTEM hedefi fi_k23_parmak(V_BIST ham INTEM, L) 2026-10-09 satırı; hedef yüzdelik fi_k44_yuzdelik(cetvel, hedef); görülmemiş pencerelerin yüzdeliği fi_k44_yuzdelik(cetvel, pencereler)",
 "cetvel_dogrula": "onkayit ve kos: cetvel + Ç124 adımları (ertesi birleşik takvim günü giriş, fi_k27_tekil 60) V_ABD'de k44_eslesme.csv ABD satırlarını (L20 317, L10 39) BİREBİR üretmeli; INTEM izi k44_parmak.csv ile aynı olmalı; değilse DURUR",
 "eski_kayit": [
  "Ç123",
  "Ç124",
  "Ç175"
 ],
 "gelecek_denetim": {
  "ornek": 60,
  "tanim": "kos: rastgele 60 sinyal; seri t'de kesilir, aynı tarama; t'de eşleşme ve aynı 8 ölçü yoksa koşu DURUR",
  "tohum": 124
 },
 "gorulmemis": {
  "a_avrupa": "YOK: Ç124 V_AVR'yi kullandı (k44_eslesme AVR 117 + 271 eşleşme, Ç124 notu 'AVR 2016-22 +15,0 (n 92)'); görülmüş veri",
  "b_abd": "OC.oc_veri('ABD') kaynağı 'k34_yahoo' olan hisseler (V_ABD'de olmayan k34 nakdi biten şirketler); Ç124 havuzunda ve eşleşmelerinde yok (k44_eslesme ABD sembollerinden hiçbiri k34-yalnız değil); evrene k34_evren ilk_giris gününden itibaren (OC 'evren_once' süzgeci), 2021-01 .. 2026-08-31",
  "c_donem": "YOK: Ç124 verisi 2015-06-01 .. 2026-10 (kriz sonrası dahil); kullanılmamış dönem yok",
  "ortusme": "V_ABD hisseleri (Ç124 evreni) ölçüme GİRMEZ; görülmemiş k34 hisseleri yalnız sinyal kaynağıdır; eş / plasebo havuzu OC'nin bütün ABD havuzudur (V_ABD + k34; kontrol grubu, sinyal değil)"
 },
 "k45": {
  "donem": "OC dönemi (giriş günü): hepsi (2021-26) + 2016-22 / 2023 / 2024-26 ayrı",
  "kural_kiyas": "Ç124 kendi kuralı: n >= 30, fark8 >= +10 puan ve bootstrap alt uç > 0 (ABD + AVR birleşik idi; burada yalnız ABD, bilgi)",
  "tam_pencere": 41,
  "veri": "OC.oc_veri('ABD')['V'] (temiz; V_ABD + k34 bütün seriler; rastgele havuz = bütün ABD, Ç124'te V_ABD'ydi)"
 },
 "karar": "OC_ESIK 'etiket' (oc_etiket) yalnız L=20 olaylarıyla (tek ana hipotez; çoklu karşılaştırma yok); AVR'de görülmemiş veri yok -> en iyi etiket 'EMARE (ABD-ADAY; AVR verisi yok)'. L=10, kendi ölçüsü ve dönem kırılımları BİLGİ (iddia üretmez). İleri test cümlesi: ABD 2023 ve 2024-26 karar hücrelerinin ikisi TUTAR -> 'tuttu (ABD-ADAY)'; bir hücre TUTAR -> 'kısmen (EMARE)'; TUTAR yok ve hücreler TUTMADI (güç yeterli) -> 'tutmadı (İZ DEĞİL)'; aksi 'ölçülemedi (ÖLÇÜLEMEDİ)'",
 "kural": "FON_IZI FI_K44 (parmak izi + birebir eşleşme) + FI_K45 (kendi ölçüsü); ikisi de DEĞİŞMEZ (sha ön kayıtta)",
 "pencere_ana": 20,
 "pencere_bilgi": 10,
 "sapma": [
  "SAPMA-1 (geleceğe bakma): fi_k23_parmak 'n < L + 200 -> boş' şartı serinin TOPLAM uzunluğuna bakar; yalnız t gününde hissenin kendi takviminde >= L + 200 barı (t dahil; pencere indeksi i >= L + 199) olan pencereler alınır (t'de kesilen seriyle aynı tespit).",
  "SAPMA-2 (veri): görülmemiş hisseler OC temiz verisinde taranır (H>L, V>0, fiyat>0 olmayan bar atılmış; 31.08.2026 kesiği); Ç124 ham veride tarardı. Cetvel (Ç124 havuzu) Ç124 gibi HAM V_ABD'den kurulur (birebir yeniden üretim için).",
  "SAPMA-3 (olay ve tekilleştirme): olay = eşleşen pencerenin bitiş günü t; giriş ve tekilleştirme OC kuralıyla (t'den sonraki ilk geçerli bar açılışı; 60 birleşik takvim gününde tek). Ç124 fi_k27_tekil (hissenin 60 barı) kullanırdı. Kendi ölçüsü (K45) AYNI olay kümesinde (OC olay tablosu: sembol, giris) ölçülür.",
  "SAPMA-4 (kriz kesiği, kendi ölçü): fiyat 31.08.2026'da kesildiği için K45 ölçüsü yalnız giriş + 41 bar (20 gün hedef + 20 gün koşullu + 1) hissenin verisinde olan olaylarda; oynaklık eşli rastgele satırlara AYNI tam pencere süzgeci uygulanır (Ç124'te veri Eki 2026'ya uzandığından kesik etkisi yoktu). İstatistik (oranlar, fark, bootstrap tohum 45 / 46, 2000) fon_izi_k45 ile birebir."
 ],
 "surum": "1.0"
}
```

## 4. Sapmalar (sonuç görülmeden)

- SAPMA-1 (geleceğe bakma): fi_k23_parmak 'n < L + 200 -> boş' şartı serinin TOPLAM uzunluğuna bakar; yalnız t gününde hissenin kendi takviminde >= L + 200 barı (t dahil; pencere indeksi i >= L + 199) olan pencereler alınır (t'de kesilen seriyle aynı tespit).
- SAPMA-2 (veri): görülmemiş hisseler OC temiz verisinde taranır (H>L, V>0, fiyat>0 olmayan bar atılmış; 31.08.2026 kesiği); Ç124 ham veride tarardı. Cetvel (Ç124 havuzu) Ç124 gibi HAM V_ABD'den kurulur (birebir yeniden üretim için).
- SAPMA-3 (olay ve tekilleştirme): olay = eşleşen pencerenin bitiş günü t; giriş ve tekilleştirme OC kuralıyla (t'den sonraki ilk geçerli bar açılışı; 60 birleşik takvim gününde tek). Ç124 fi_k27_tekil (hissenin 60 barı) kullanırdı. Kendi ölçüsü (K45) AYNI olay kümesinde (OC olay tablosu: sembol, giris) ölçülür.
- SAPMA-4 (kriz kesiği, kendi ölçü): fiyat 31.08.2026'da kesildiği için K45 ölçüsü yalnız giriş + 41 bar (20 gün hedef + 20 gün koşullu + 1) hissenin verisinde olan olaylarda; oynaklık eşli rastgele satırlara AYNI tam pencere süzgeci uygulanır (Ç124'te veri Eki 2026'ya uzandığından kesik etkisi yoktu). İstatistik (oranlar, fark, bootstrap tohum 45 / 46, 2000) fon_izi_k45 ile birebir.

Ham (k34_yahoo temizlenmemiş) / temiz (OC) eşleşme sayısı (SAPMA-2 etkisi; getiri yok): L20 ham 768 / temiz 740; L10 ham 56 / temiz 53

## 5. Ölçüm ve karar

- Ana: L = 20 sinyalleri -> `OC.oc_olc(olaylar, {'ABD': panel})`; rapor `OC.oc_rapor`. Bilgi: L = 10 aynı yolla.
- Karar: OC_ESIK 'etiket' (oc_etiket) yalnız L=20 olaylarıyla (tek ana hipotez; çoklu karşılaştırma yok); AVR'de görülmemiş veri yok -> en iyi etiket 'EMARE (ABD-ADAY; AVR verisi yok)'. L=10, kendi ölçüsü ve dönem kırılımları BİLGİ (iddia üretmez). İleri test cümlesi: ABD 2023 ve 2024-26 karar hücrelerinin ikisi TUTAR -> 'tuttu (ABD-ADAY)'; bir hücre TUTAR -> 'kısmen (EMARE)'; TUTAR yok ve hücreler TUTMADI (güç yeterli) -> 'tutmadı (İZ DEĞİL)'; aksi 'ölçülemedi (ÖLÇÜLEMEDİ)'.
- Kendi ölçüsü (bilgi): OC.oc_veri('ABD')['V'] (temiz; V_ABD + k34 bütün seriler; rastgele havuz = bütün ABD, Ç124'te V_ABD'ydi); OC dönemi (giriş günü): hepsi (2021-26) + 2016-22 / 2023 / 2024-26 ayrı; Ç124 kendi kuralı: n >= 30, fark8 >= +10 puan ve bootstrap alt uç > 0 (ABD + AVR birleşik idi; burada yalnız ABD, bilgi).
- Eski sonuçlar (yeniden ölçülmez; IZ_KARNE metninden alıntı):

  - Ç124: 20 bar +%8 önce, ABD (oynaklık eşli rastgele): "ABD %54,9 / %43,2 (rastgele %43,7 / %43,2; fark +11,2 puan, aralık +6 .. +17)" (IZ_KARNE metninde: EVET)
  - Ç124: 20 bar +%8 önce, AVR: "AVR %50,4 / %41,9 (rastgele %35,5 / %35,9; +15,0, aralık +6 .. +24)" (IZ_KARNE metninde: EVET)
  - Ç124: dönem sınaması ABD / AVR: "fark ABD 2016-22 +12,7 (n 240), 2023 +3,1 (n 26), 2024-26 +6,3 (n 51); AVR 2016-22 +15,0 (n 92)" (IZ_KARNE metninde: EVET)
  - Ç124: kutu yukarı kırılımında al kuralı: "Kutu yukarı kırılımında al kuralı: ABD +10,9 (aralık 0'a değiyor), AVR +1,9 -> tutmadı" (IZ_KARNE metninde: EVET)
  - Ç123: K44 60 gün eşli fark ABD 20 bar (2016-22 / 2023 / 2024-26): "ABD -%4 / -%9 / -%1" (IZ_KARNE metninde: EVET)

## 6. OLAY SAYIMI (getiri hesaplanmadan)

Tarama: 1465 görülmemiş hisse, okunamayan 0; L20: 1548097 pencere, 740 eşleşen pencere; L10: 1562370 pencere, 53 eşleşen pencere

Eşleşen pencereler, sinyal günü t'ye göre dönem (tekilleştirme öncesi):

| L | 2016-22 | 2023 | 2024-26 | dışı | toplam |
|---|---|---|---|---|---|
| 20 | 345 | 144 | 251 | 0 | 740 |
| 10 | 25 | 10 | 18 | 0 | 53 |

OC süzgeçlerinden sonra bağımsız olay (giriş dönemi; ORTAK CETVEL oc_olay_hazirla; ölçüme girecek n; r60 ölçülemeyenler kos'ta ayrıca düşer):

| L | 2016-22 | 2023 | 2024-26 | toplam | düşmeler |
|---|---|---|---|---|---|
| 20 | 37 | 26 | 43 | 106 | girdi 740; likidite_alt20 446, bolunme_gecmis 4, evren_once 86, gecmis_eksik 4, havuz_disi 540, tekil 94 |
| 10 | 8 | 4 | 9 | 21 | girdi 53; likidite_alt20 18, evren_once 13, havuz_disi 31, tekil 1 |

K45 kendi ölçüsüne girecek olay (SAPMA-4 tam pencere):

| L | 2016-22 | 2023 | 2024-26 | toplam |
|---|---|---|---|---|
| 20 | 37 | 26 | 42 | 105 |
| 10 | 8 | 4 | 9 | 21 |

Beklenen güç (OC güç tablosu, δ +%5, OC sonrası n; L = 20 karar hücreleri):

| Hücre | n | güç % | n < 30 ise |
|---|---|---|---|
| ABD 2023 | 26 | 0 | ÖLÇÜLEMEDİ (önceden belli) |
| ABD 2024-26 | 43 | 10 | - |
| AVR 2023 / 2024-26 | 0 | 0 | görülmemiş veri yok |

Not: güç tablosuna göre n < 1.000 iken 'TUTMADI' (İZ DEĞİL) yazılamaz; TUTAR olmayan hücre ÖLÇÜLEMEDİ olur.

Veri notları: k34_yahoo eklendi: 1472 hisse (evrene ilk_giris gününden itibaren; bugün işlem görenler, batan YOK); evren dışı (fon / ETF) çıkarılan: 7 ['BTCW', 'DBA', 'DBB', 'DBO', 'UNG', 'UNL', 'UUP']; hayatta kalma: evren bugün işlem gören hisseler; getiriler yukarı, -%50 olasılığı aşağı yanlı okunmalı

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | OC eşleri (aynı giriş günü, aynı pazar, 60 gün momentum beşliği x 20 gün likidite üçlüsü; 200 plasebo portföy); kendi ölçüsünde OYNAKLIK EŞLİ rastgele taban (aynı yıl, aynı 20 gün oynaklık dilimi +-0,05; H065 dersi). Mekanik üstünlük: eşleşen bölgeler oynak (Ç124: 20 günde +-%8'e ulaşan %98) -> ana karar OC 60 gün eşli farkla; kendi ölçü oynaklık eşli |
| K2 | geleceğe bakma | EVET | fi_k23_parmak yalnız geriye bakan pencereler (rolling / ewm / shift); 'n < L+200' toplam uzunluk şartı SAPMA-1 ile t'ye indirildi; cetvel Ç124'te dondurulmuş sabit (ham ölçü aralıkları), görülmemiş verinin sonucundan bağımsız; kos'ta 60 sinyal seri t'de kesilerek yeniden taranır (test_intem_ileri 'gelecek' + gerçek veri denetimi); k34 evrene ilk_giris'ten (OC) |
| K3 | geçerli bar | EVET | görülmemiş hisseler OC temiz verisinde taranır (H>L, V>0 olmayan bar atılmış; SAPMA-2); OC sinyal barı geçersizse olay düşer; K45 High / Low yalnız geçerli barlarda |
| K4 | tekilleştirme | EVET | OC 60 birleşik takvim günü tekilleştirme (SAPMA-3); n bağımsız olay; hücrede medyan; K45 aynı olay kümesi |
| K5 | giriş fiyatı | EVET | giriş = OC: t'den sonraki ilk geçerli bar AÇILIŞI (pencere t kapanışında biter); K45 de bu açılıştan |
| K6 | veri birimi | EVET | tek kip: V_ABD / k34_yahoo düzeltilmiş fiyat (OC); oranlar birimden bağımsız; OC geçmiş bölünme şüphesi süzgeci; ABD tek pazar (USD) |
| K7 | hayatta kalma | EVET | k34 nakdi biten şirketler BUGÜN işlem görenler (batanlar YOK, Tiingo YOK) -> getiriler yukarı, -%50 olasılığı aşağı yanlı; raporda yazılır; görülmemiş evren nakit yakan küçük şirketler (Ç124 evreninden farklı nüfus) -> sınır |
| K8 | örneklem ve dönem | EVET | OC hücreleri (n < 30 ÖLÇÜLEMEDİ; iki yarı aynı yön; İZ DEĞİL yalnız n >= 1.000 ya da güç %80); tek ana hipotez (L20) -> BH gerekmez; L10 / kendi ölçü / dönem bilgi; olay sayımı ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | II_ESIK sha + FI_K44 / FI_K45 sha + FON_IZI kural kodu sha + INTEM_ILERI.py sha + hedef / cetvel sha + olay sha + OC üç satırı ön kayıtta; ön kayıt ve modül commit + push SONRA kos; kos git kapısı + sha eşitliği; eşik yok, sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber / KAP ayrıştırma yok; yalnız OHLCV; Ç124 eşleşmeleri ham csv'den birebir yeniden üretilir; 3 olay ham veriden elle (rapor) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/intem_ileri/intem_olay.csv.gz; >= 2 hücre bağımsız kodla yeniden üretilir; eski sayılar IZ_KARNE metninden alıntı (denetlenir) |
| K12 | ifade | EVET | etiketler yalnız OC kuralıyla; fiyat değişimi (komisyon yok); kendi ölçü ve L10 'bilgi', iddia değil; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_ii; yasak dosyalara dokunulmaz (git diff --stat); e-posta / anahtar taraması testte; ücretli veri yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ileri test ölçümü |

## Test

`python test_intem_ileri.py` (sentetik: eşleşme = FON_IZI fi_k44_eslesme; sabit cetvel; geleceğe bakma: seri t'de kesilince aynı tespit; SAPMA-1; ii_k45 = fon_izi_k45 birebir; tam pencere süzgeci; cetvel çağrısı OC.oc_olc; kapı; çakışma kapısı; e-posta / anahtar yok).
