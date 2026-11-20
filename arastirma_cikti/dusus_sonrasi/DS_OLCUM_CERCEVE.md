# DÜŞÜŞ SONRASI PARMAK İZİ — ÖLÇÜM ÇERÇEVESİ (taslak, 20 Kasım 2026; hipotezler gelmeden yazıldı)

Amaç: web araştırması (DS_IS_TANIMI, kol A-D) + eleştiri süzgecinden geçen YENİ hipotezleri tek ön kayıtla, sabit eşikle, iki pazarda ve iki dönemde ölçmek.
Bu çerçeve hipotezlerden bağımsızdır ve sonuç görülmeden yazıldı; hipotez listesi ve eşikleri DS_ON_KAYIT.md'ye eklenir (ayrı commit, koşudan önce).

## 1. Olay kümesi (DS olayı)
- Günlük bar, hisse-gün t. ŞART: (a) C_t / max(C, son 120 geçerli bar) − 1 <= −0,30 (tepeden en az %30 düşüş); (b) F15_t <= 0,25 (120 gün aralığının alt çeyreği; GOZ_ETIKET tanımı, t dahil); (c) likidite: son 20 gün medyan işlem değeri >= 1 mn $ (ABD), 1 mn EUR (AVR, Kur sütunu), 5 mn TL (BIST) (K3 geçerli bar, K6 birim); (d) C_t >= 2 $ (ABD) (penny süzgeci, k60 kuralıyla aynı); (e) kriz kesiği: BIST / genel giriş <= 2026-08-31 − 15 bar (FI_OLCUT 'kriz').
- Tekilleştirme (K4): aynı hissede ardışık DS günleri bir 'dönem'; ölçüm hisse-gün bazında ama eş kurulumunda aynı gün eş sayılmaz, hücre özetinde ay kümeli bootstrap + L3O (YAPI_HEDEF karne v3). Tek hisse en çok 1 olay / 15 bar (ilk gün alınır) ANA; bütün günler BİLGİ.
- Hipotez özelliği X_t yalnız t'ye kadar bilinen veriden (K2); olay verisi için 'duyuru / başvuru günü + 1 işlem günü' kuralı (SINYAL_ENVANTERI zaman kuralı). Prefix testi: veri t'de kesilince aynı değer.

## 2. Cetvel (karar) — UFUK 15 MUM (Cemal, 17 Kas) — YAPI_HEDEF 15 bar makinesi (yh_getiri, yh_hucre, yh_etiket karne v3)
- Giriş = t+1 geçerli bar açılışı; stop0 = hat x 0,98 (hat = DS dibi: son 20 gün en düşük L); hedef +%5 ve +%10, 15 geçerli bar; h5 = hedef stop'tan önce görüldü payı; st5 = stop önce; takip stoplu getiri ve çıkış barı BİLGİ.
- EŞ: aynı giriş günü, aynı pazar, DS kümesi içinde özelliği tutmayan olaylar (karne v3 'aynı gün aynı kova'; kova = ATRP tercili x likidite üçlüsü). FARK = h5(özellik tutan) − h5(eş). Ayrıca 'DS dışı eş' (aynı gün, aynı kova, DS olmayan hisse) BİLGİ: DS kümesinin kendisi bir iz mi?
- Bilgi cetvelleri: 60 gün r60 eşli fark (ORTAK_CETVEL), 250 gün +%100 / −%50 olasılık tablosu (katlar).

## 3. Hücreler ve karar
- Pazar x dönem: ABD ve AVR karar; BIST bilgi. Dönem: eğitim 2016-22 (keşif), sınama 2023-26/08 (ambargo 60 bar; karne v3). ABD ve AVR ayrı n >= 30 (güç < 0,80 ise ÖLÇÜLEMEDİ).
- Etiket (karne v3 ile aynı): KATKI+ = iki dönemde ve iki pazarda FARK > 0, ay kümeli bootstrap %95 alt ucu > 0 (sınama), stop payı eşten büyük değil, ATRP tercil şartı; KATKI− = iki dönemde de eksi (güç yeterliyse); SORGULA; ÖLÇÜLEMEDİ.
- Çoklu test: hipotez sayısı m için Benjamini-Hochberg q 0,10 (sınama hücresi p değerleri; ay kümeli permütasyon). BH listesi ön kayıtta sabit; sonradan hipotez eklenmez.
- Yön çelişkisi: bir hipotez eğitimde + sınamada − ise 'çelişkili', iz değil (CLAUDE.md test standardı).

## 4. Çıktılar
- arastirma_cikti/dusus_sonrasi/DS_ON_KAYIT.md: kontrol tablosu K1-K14 (EVET / UYGULANMAZ + kanıt), hipotez tablosu (kod, tanım, pencere, SABİT eşik, yön, kaynak), huni (getirisiz: DS olay sayısı pazar x dönem, hipotez tutan olay sayısı), cetvel sha (YAPI_HEDEF yh_esik_sha + bu dosyanın sha'sı), git mühür. IZ_KARNE.ik_kontrol_kapisi(onkayit) koşudan önce.
- DS_RAPOR.md: tablo (hipotez | pazar | eğitim n / FARK | sınama n / FARK | stop olay / eş | BH p | etiket), YENİDEN ÜRETİM >= 2 hücre, olasılık tablosu (bilgi), HATA, KONTROL LİSTESİ. ds_sonuc.json, ds_olay.csv.gz (satır verisi; bağımsız denetçi için).
- Kod: DUSUS_SONRASI.py (tek dosya, Colab; çakışma kapısı; YAPI_HEDEF ve ORTAK_CETVEL'i içe alır, kopyalamaz); test_dusus_sonrasi.py (sentetik veri: DS olayı tespiti, prefix, eş kurulumu, BH).
- Üç bağımsız lens (devir düzeni): yeniden üretim, sızıntı / kontrol listesi, çürütme (en iyi 5 sembol çıkınca, dönem alt bölmeleri, ATRP tercilleri).

## 5. Hipotez girişi (DS_ON_KAYIT'a; buraya değil)
Kaynak: WEB_A..D + eleştiri (DS_ELESTIRI.md). Şart: YENİ (envanterde yok), bizde EVET veriyle, t'de bilinir, 15 bar ölçülebilir, kapalı konu değil. Eşik kaynaktan; kaynakta yoksa eğitim döneminde medyan / üst çeyrek (sonuç görülmeden, eğitim verisinden sabitlenir ve yazılır).
