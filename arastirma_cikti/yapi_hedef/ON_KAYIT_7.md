# YAPI_HEDEF — ÖN KAYIT 7 (7. tur: PUAN — bütün Y1 bölgelerini puanlama, sızıntısız öğrenme, Y12)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 7. tur eklendi (YAPI_HEDEF_IS_TANIMI_7.md)

- YH_ESIK7_SHA: `14f11dee1c6c96e976f60357771c7bb2b312ce91ad99cde691dad7dd2410ff26` (7. tur: özellikler, NaN, yönler, tampon, model ayarları, plasebo, dilim, TUTAR, etiket, Y12)
- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (= ON_KAYIT_5.md YH_ESIK_SHA: Y1-Y11c, cetvel, karar ve etiket kuralı AYNEN)
- YH_KOD_SHA: `25ffb1f144fd86039788e67be48ba2cbdc00215782822bbdc5f0f9083177a43f` (YAPI_HEDEF.py)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json, 1. tur)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)
- PARMAK_SHA: `572530891942d26c168b398ecea19439b9d7385cad2dd3f7467740e28d8da770` (goz_etiket/parmak_Y1_p11.csv.gz; F19)
- S7_OZELLIK_SHA: `9463e08e6bb7eb95820eccc9be9dcb3a1d549312dc62cdcc657b2a2b02e6137d` (ozellik_Y1_s7.csv.gz; F20-F23)
- S9_OZELLIK_SHA: `c9a6a4e62673fcc56cc82550c915feed3be4b7235ada8a940d4de09ff0f28756` (ozellik_Y1_s9.csv.gz; F24-F29)
- G6_OLAY_SHA: `615f7f569f8c310dd79434757690e6e29e720ffec3faca0ebb323a591df55f9a` (olay_G6.csv.gz; ölçüm satırları + konum eşi)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (olay_Y1.csv.gz; regresyon)
- SKLEARN: `1.9.1` (numpy 2.5.3, pandas 3.0.5)
- ON_KAYIT_6: git 3833f78278, ?
- IS_TANIMI_7: git 5ac129a97b, ?
- ZAMAN (UTC): `2026-11-19 08:25:58 UTC`

Bu dosya 7. tur koşusundan ÖNCE yazıldı. Alt ajan hiçbir model eğitmedi, hiçbir puan / dilim / hedef payı / eş oranı / plasebo / AUC hesaplamadı ve okumadı: aşağıdaki sayılar yalnız satır kimlikleri, giriş tarihleri, ölçülebilirlik bayrağı ve özellik NaN oranlarıdır (getirisiz). `python YAPI_HEDEF.py puan7` bu dosyanın kontrol listesini, sha'larını, sklearn sürümünü ve git kaydını denetler; biri tutmazsa durur. Model ayarları ve eşikler sonuç görüldükten sonra değişmez (hiperparametre arama yok).

## İŞ TANIMI 7 §1-§4 (AYNEN)

### §1
- Satırlar: olay_Y1.csv.gz (26.663 Y1 olayı; ölçülebilir olanlar, olc). Hedef y = h5 (15 geçerli barda kapanış +%5 stop'tan önce; aynı cetvel). Eş payı es_h5 satırda.
- Özellikler X: F1-F18 (ozellik_Y1), F19 parmak (parmak_Y1_p11), F20-F23 (s7), F24-F29 (s9); pazar ve dönem ÖZELLİK DEĞİL (sızıntı / kayma); momentum x likidite kovası (eş kovası) özellik olarak ALINMAZ (eş payı zaten bunu kontrol ediyor); NaN -> medyan (eğitim kümesinden), ayrıca 'NaN bayrağı' sütunları.
- Hedefin alternatif biçimi (ikincil): y2 = h5 - es_h5 > 0 (eşini geçti mi).

### §2
- İki yön: (A) eğitim 2016-22 -> sınama 2023 + 2024-26; (B) eğitim 2023-26 -> sınama 2016-22. Ayrıca (C) yürüyen: her takvim yılı için yalnız önceki yıllarla eğit, o yılı sına (2019'dan itibaren; ilk eğitim 2016-18).
- Modeller (ikisi de): M1 lojistik regresyon (standartlaştırılmış, L2, C = 1,0); M2 gradyan artırmalı ağaç (sklearn HistGradientBoosting; max_depth 3, learning_rate 0,05, max_iter 300, early stopping eğitim içi %20 doğrulama). Hiperparametre arama YOK (önceden sabit).
- Pazarlar: birleşik model (ABD + AVR + BIST) VE pazar başına model; ikisi de raporlanır.
- PLASEBO: aynı model, y karıştırılmış (tohum 107, 20 tekrar): üst dilim P(+5) dağılımı; gerçek modelin üst dilim payı plasebo %95'inin üstünde mi.
- SIZINTI KAPISI: sınama kümesindeki hiçbir satırın tarihi eğitim kümesinin son tarihinden <= 60 gün sonra değil (tampon 60 gün: hedef penceresi + giriş); ayrıca hisse düzeyinde tampon gerekmez (eş günlük).

### §3
- Puan dilimleri: üst %10, üst %20, alt %20, tümü. Her dilimde: n, P(+5) olay, P eş (es_h5 ortalaması), KAT5 = olay / eş (ay kümeli bootstrap %95), stop payı, konum eşli KAT (F15 çeyreği); hücreler pazar x sınama dönemi.
- AUC (bilgi), kalibrasyon (10 kutu: tahmin vs gerçek).
- TUTAR (hücre): üst %20 diliminde n >= 30 VE KAT5 alt ucu > 1 VE plasebo %95 üstünde VE stop payı eşten büyük değil; etiket kuralı önceki turlar gibi (İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ; karar hücreleri ABD / AVR 2023 ve 2024-26 'bakılmış' notuyla; 2016-22 yönü (B) bağımsız sınama).
- 'HER SEÇİLEN YUKARI ÇIKSIN' tavanı: üst %5 diliminde P(+5) (en iyi durumda ulaşılan oran) açıkça yazılır.
- Özellik önemi (M2 permütasyon önemi, sınama kümesinde; bilgi): hangi özellikler puanı taşıyor; Cemal'in kurallarıyla (Ş1-Ş9) örtüşme.

### §4
- Üst %20 puan eşiği (eğitim kümesinden sabitlenir) -> Y12 seçicisi: sınama döneminde seçilen olaylar, aynı cetvel, huni tablosuna 'Y12 PUAN' satırı (İLERLEME tablosuna ekle). TUR 6 havuzu adayı (karar Cemal'in).
- Mahkeme (6. tur) ile bağ: seçilen üst dilim olaylarında mahkeme kural puanı ortalaması vs alt dilim (bilgi).

## TANIMLAR, MODEL AYARLARI ve EŞİKLER (YH_ESIK7; uygulama kararları dahil)

- SATIRLAR: olay_G6.csv.gz (26.663 Y1 olayı = olay_Y1.csv.gz satırları + konum eşi sütunları; h5 / es_h5 / st5 / es_st5 / n_es / tb_h5 / getiri / pl_h5 olay_Y1 ile eşit olmalı, değilse DUR); özellikler (pazar, sembol, tarih) ile 1:1 birleşir (eksik / fazla satır DUR); ölçülen satır = h5 ve es_h5 var (yh_hucre n'i); eğitim yalnız ölçülen satırlar; dilimler ölçülen sınama satırlarında.
- ÖZELLİKLER (30): F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19, F20, F21, F22, F22a, F23, F24, F25, F26, F27, F28, F29; F1-F18 (goz_etiket/ozellik_Y1), F19 (parmak_Y1_p11), F20-F23 (s7; F21 fiyat seviyesidir: iş tanımı listesinde olduğu için alındı, birimli), F24-F29 (s9); pazar, dönem, eş kovası (momentum x likidite) ÖZELLİK DEĞİL.
- NaN: NaN -> eğitim kümesinin medyanı (eğitimde hepsi NaN ise 0); ayrıca NaN bayrağı sütunu (0/1) şu özellikler için (tam tabloda NaN'ı olanlar; getirisiz): F2, F14, F25, F27, F28, F29; başka bir özellikte NaN çıkarsa DUR.
- HEDEF: h5 (15 geçerli barda kapanış +%5 stop'tan önce; 1. tur cetveli); ikincil: y2 = h5 - es_h5 > 0 (eşini geçti mi; BİLGİ: yalnız A / B, birleşik, M1 / M2; AUC ve üst %20 payı).
- TARİH: satır tarihi = giris (giriş günü; dönem = giriş günü dönemi).
- YÖN A: eğitim 2016-22 -> sınama 2023, 2024-26; YÖN B: eğitim 2023, 2024-26 -> sınama 2016-22; YÖN C: her takvim yılı Y (giriş yılı, 2019..2026) için eğitim = giriş yılı < Y olan ölçülen satırlar, sınama = giriş yılı Y.
- TAMPON (60 gün): eğitim satırlarından sınama satırlarının (bütün olay satırları, ölçülemeyenler dahil) herhangi birine giriş tarihi farkı <= 60 takvim günü olanlar ATILIR (purge); SIZINTI KAPISI: her model eğitiminden önce min |giris_sinama - giris_egitim| > 60 gün, değilse YHHata (DURUR); hisse düzeyinde ek tampon yok (eş günlük).
- M1: {"C": 1.0, "ad": "lojistik regresyon", "ceza": "L2 (sklearn varsayılanı)", "max_iter": 5000, "olcek": "StandardScaler (eğitim kümesinde)", "solver": "lbfgs"}.
- M2: {"ad": "HistGradientBoostingClassifier", "early_stopping": true, "learning_rate": 0.05, "max_depth": 3, "max_iter": 300, "n_iter_no_change": 10, "not": "erken durdurma doğrulaması eğitim içi %20 (sklearn tabakalı rastgele bölme, random_state 7)", "random_state": 7, "scoring": "loss", "validation_fraction": 0.2}.
- MODLAR: birleşik = ABD + AVR + BIST tek model; pazar = pazar başına ayrı model (eğitim ve sınama o pazarın satırları).
- PLASEBO: aynı model, aynı bölünme; eğitim y'si karıştırılır: rng = default_rng([107, tekrar, kat no, pazar no (birleşik 0; ABD 1, AVR 2, BIST 3)]).permutation(y); sınama puanları aynı dilim kuralıyla; hücre x dilim başına 20 P(+5) değeri; plasebo %95 = np.quantile(20 değer, 0,95) (doğrusal); gerçek > plasebo %95 -> 'plasebo üstü'.
- DİLİM: dilim grubu içinde (A / B: pazar x sınama dönemi; C: pazar x sınama yılı, sonra dönem hücrelerine toplanır) ölçülen satırların puanıyla: üst %q = puan >= np.quantile(puan, 1 - q); alt %20 = puan <= np.quantile(puan, 0,20); tümü = hücre.
- ÖLÇÜ: dilim x hücre (pazar x sınama dönemi): yh_hucre (n, P(+5) olay, P eş = es_h5 ort, KAT5 = Σh5 / Σes_h5 ay kümeli bootstrap %95 (YH_ESIK kat: 2000, tohum 27), stop payı st5 olay / eş, iki yarı) + yh_hucre_konum (konum eşli KAT, F15 çeyreği); AUC (bilgi, tümü satırında), kalibrasyon 10 kutu (puan çeyrek kutuları: ort tahmin vs ort h5; bilgi).
- TUTAR: hücre üst %20 diliminde: n >= 30 VE KAT5 %95 alt ucu > 1 VE üst %20 P(+5) > plasebo %95 VE stop payı (st5 olay) <= eş stop payı (es_st5 ort).
- ETİKET: hücre durumu yh_durum (n < 30 ÖLÇÜLEMEDİ; TUTAR; n >= 1.000 ya da güç >= %80 -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ; güç tablosu 1. tur) -> yh_etiket (karar hücreleri ABD / AVR 2023 ve 2024-26) -> yh_etiket3 (3. tur: BAKILMIŞ hücreler (Y1 hücreleri önceki turlarda görüldü) -> en fazla EMARE; dış sınama ABD / AVR 2016-22; TERS iki yönlü). Hücreler: 2023 ve 2024-26 yön A'dan, 2016-22 yön B'den (bağımsız sınama). ANA ETİKET = M2 birleşik; M1 birleşik, M1 / M2 pazar başı BİLGİ (çoklu karşılaştırma). Yön C BİLGİ (TUTAR bayrakları yazılır, etiket yok).
- TAVAN: üst %5 diliminde P(+5) ('her seçilen yukarı çıksın' tavanı) her hücre için yazılır.
- ÖNEM: sklearn permutation_importance sınama kümesinin ölçülen satırlarında (bilgi); Ş1-Ş9 / F14 / C8 eşlemesi yazılır (n_repeats 5, random_state 7, roc_auc; M2 birleşik, yön A ve B).
- Y12: Y12 PUAN seçicisi: eşik = eğitim kümesinin (purge sonrası, ölçülen) kendi puanlarının 0,80 çeyreği (eğitimden sabit); A modeliyle 2023 ve 2024-26 sınama olayları (bütün olay satırları; n = ölçülen), B modeliyle 2016-22; aynı 15 bar cetveli; İLERLEME tablosuna 'Y12 PUAN' satırı; TUR 6 havuzu adayı (karar Cemal'in).
- MAHKEME BAĞI: BİLGİ: yön A M2 birleşik sınama satırlarında 12 kural puanı (yh_m_kurallar ile aynı kurallar: Ş1-Ş9, F14, C8 (F16 = 0) özellik dosyalarından; C13 veriden _yh_c13 (son 250 bar, t'ye kadar)); üst %20 ortalaması vs alt %20 vs tümü, pazar başına.
- YENİDEN ÜRETİM: RAPOR_7 'YENİDEN ÜRETİM': iki hücre (ABD 2023 üst %20 yön A M2 birleşik; AVR 2016-22 üst %20 yön B M2 birleşik) puan_Y1.csv.gz + olay_G6.csv.gz'den bağımsız pandas koduyla (dilim yeniden, n / P olay / P eş) = puan7.json.

UYGULAMA YORUMLARI (iş tanımında açık değildi; ölçümden önce yazıldı): (1) §3 dilimleri sınama hücresi içinde sıralanır (değerlendirme); §4 Y12 eşiği eğitim kümesinden sabitlenir (karar kuralı); (2) tampon eğitim tarafında uygulanır (sınama hücreleri eksiksiz kalır); B'de eğitim sınamadan SONRA olduğu için tampon simetriktir (en yakın tarih uzaklığı); (3) 'plasebo %95'in üstünde' = gerçek üst %20 P(+5) > 20 plasebo değerinin 0,95 çeyreği; (4) 'stop payı eşten büyük değil' = st5 olay <= es_st5 ort (1. tur yh_hucre'nin kesin küçük şartından farklı: iş tanımı sözü); (5) ANA etiket M2 birleşik (Y12 de bu modelden); öteki üç model / mod bilgi; (6) yürüyen (C) dilimleri pazar x yıl içinde, dönem hücrelerine toplanarak raporlanır (2016-22 hücresi C'de yalnız 2019-22); (7) F21 fiyat seviyesi listede olduğu için alındı (birimli; K6 notu).

## GETİRİSİZ SAYIMLAR (satır kimliği + giriş tarihi + ölçülebilirlik; hedef değeri okunmadı)

Satır 26663, ölçülen 26508. Özellik NaN oranları: F2 %4,6, F14 %0,1, F25 %49,3, F27 %49,3, F28 %49,3, F29 %49,3 (öteki özelliklerde NaN yok).

| Yön / kat | eğitim (ölçülen, ham) | purge | eğitim | sınama olay | sınama ölçülen | min uzaklık (gün) | eğitim ABD / AVR / BIST | sınama ölçülen ABD / AVR / BIST |
|---|---|---|---|---|---|---|---|---|
| A | 15763 | 424 | 15339 | 10893 | 10745 | 61 | 8447 / 4357 / 2535 | 6123 / 2526 / 2096 |
| B | 10745 | 647 | 10098 | 15770 | 15763 | 61 | 5708 / 2300 / 2090 | 8682 / 4493 / 2588 |
| C2019 | 5800 | 133 | 5667 | 2956 | 2955 | 61 | 3084 / 1835 / 748 | 1642 / 832 / 481 |
| C2020 | 8755 | 556 | 8199 | 1931 | 1931 | 62 | 4479 / 2535 / 1185 | 1025 / 494 / 412 |
| C2021 | 10686 | 458 | 10228 | 3125 | 3125 | 61 | 5559 / 3072 / 1597 | 1832 / 840 / 453 |
| C2022 | 13811 | 372 | 13439 | 1953 | 1952 | 61 | 7454 / 3940 / 2045 | 1045 / 462 / 445 |
| C2023 | 15763 | 424 | 15339 | 3238 | 3236 | 61 | 8447 / 4357 / 2535 | 2040 / 815 / 381 |
| C2024 | 18999 | 606 | 18393 | 3062 | 3058 | 61 | 10333 / 5167 / 2893 | 1716 / 648 / 694 |
| C2025 | 22057 | 395 | 21662 | 2799 | 2796 | 63 | 12282 / 5893 / 3487 | 1543 / 667 / 586 |
| C2026 | 24853 | 377 | 24476 | 1794 | 1655 | 63 | 13780 / 6540 / 4156 | 824 / 396 / 435 |

Eğitim sayısı (model x mod x kat x (1 gerçek + 20 plasebo)): 1680.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban = aynı satırın eşi (es_h5: aynı giriş günü, aynı momentum x likidite kovası, aynı d / hedef / takip / 15 bar; 1. tur kodu, olay_G6 = olay_Y1 regresyonu DURUR) ve konum eşli KAT (F15 çeyreği); model plasebosu (y karıştırılmış, 20 tekrar, aynı bölünme ve dilim kuralı) üst dilimin mekanik üstünlüğünü (model esnekliği / dilim seçimi) dışlar; dilim hücre içinde (pazar x dönem) sıralanır: pazar / dönem taban farkı puana girmez; eş kovası özellik değil |
| K2 | geleceğe bakma | EVET | özellikler mühürlü dosyalardan (F1-F29 yalnız [.., t]; önceki turlarda prefix denetimleri: ozellik_denetim, parmak_denetim_p11, s7 / s9 denetim json); pazar / dönem özellik değil; NaN medyanı ve ölçekleme yalnız eğitim kümesinden; SIZINTI KAPISI her eğitimde min /giris_sinama - giris_egitim/ > 60 gün (hedef penceresi 15 bar <= 30 takvim günü + giriş), değilse DURUR (test: ihlal eden bölünme durur); Y12 eşiği eğitim puanlarından; C13 yalnız t'ye kadar |
| K3 | geçerli bar | EVET | satırlar 1. tur Y1 ölçümü (_yh_hazir: H > L, V > 0, kriz kesiği; 15 geçerli bar / 30 takvim günü); bu tur yeni bar ölçmez |
| K4 | tekilleştirme | EVET | Y1 olayları OC 60 gün tekil (1. tur); n = bağımsız olay; dilim hücrelerinde getiri ortalama + medyan (yh_hucre); yürüyen yılda her olay bir kez sınanır |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (1. tur cetveli; olay_G6 = olay_Y1 regresyonu) |
| K6 | veri birimi | EVET | ölçüler oran / sayı; F21 fiyat seviyesi (birimli, pazara göre farklı para): iş tanımı F20-F23 dediği için alındı, ön kayıtta yazılı; dilim pazar hücresi içinde; AVR yerel para |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; rapora yazılır |
| K8 | örneklem ve dönem | EVET | dilim x hücre n tabloda; n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; iki yön + yürüyen; karar hücreleri BAKILMIŞ -> en fazla EMARE; ANA = M2 birleşik, öteki üç model / mod BİLGİ (çoklu karşılaştırma); küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_7.md: YH_ESIK7_SHA (model ayarları, eşikler, tohumlar, tampon), YH_ESIK_SHA (= ON_KAYIT_5), kod / özellik / olay / güç sha, sklearn sürümü, getirisiz sayımlar; yh_kapi7 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt commit'i koşudan önce; hiperparametre arama yok; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız mühürlü özellik ve olay dosyaları (+ C13 için OHLCV) |
| K11 | yeniden üretim | EVET | puan_Y1.csv.gz (puan + dilim) + olay_Y12.csv.gz + puan7.json; RAPOR_7 'YENİDEN ÜRETİM' iki hücre bağımsız pandas koduyla; İLERLEME satırları satır dosyalarından |
| K12 | ifade | EVET | etiket yalnız 3. tur kuralıyla (en fazla EMARE); AUC / kalibrasyon / önem / mahkeme bağı / y2 'bilgi'; 'iz değil' yazılmaz; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _YH_ önekli, 7 ekli); yasak defter dosyalarına, GOZ_ETIKET.py'ye, tur/* içeriklerine dokunulmadı (git diff); e-posta / anahtar taraması (_yh_yaz); push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

