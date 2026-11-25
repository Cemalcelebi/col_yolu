# MACD_UYUM — KASA KÖR SINAMASI ÖN KAYIT (T: derin toplam uyumsuzluk; KASA açılmadan ÖNCE)

Yazan: ana model, 2026-11-25 (TR 08:5x). Cemal'in onayı (25 Kas 08:47): "Aç".
Bu dosyanın ana bölümü (tanım, ölçü, karar) kasa açılmadan önce commit edilir ve sonra DEĞİŞMEZ. Teknik ek (sha'lar, kontrol tablosu, getirisiz sayımlar) alt ajan tarafından kasa açılmadan önce EK olarak eklenir.

## Hipotez (tek; değiştirilmez)
T = U1 olayı VE PFc <= -0,10 VE MRc >= 0,30.
- U1: Ç217 MACD_UYUM tanımı aynen (MU_ESIK, YH_ESIK8; DİPTE, Ş10, F68, olay günü kuralı, 15 bar tekil).
- Zincir: UYUM_Z_ON_KAYIT tanımı (önceki U1 olayı en çok 60 geçerli bar önce ve Low(L2) daha düşükse sıra + 1). Zincir 2022 ve öncesindeki (açık) olaylardan başlayabilir.
- PFc, MRc: UYUM_T_ON_KAYIT tanımı (zincirin ilk olayının L1 dibi ve o dipteki MACD'ye göre).
- Eş: CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı pazar, ATRP x likidite x F15 kovası, kovadaki bütün hisseler, en az 5) + K20 temiz eş (ES_ON_KAYIT: eşin giriş gününden önceki 20 barda ham U1 durumu varsa dışarıda).
- Giriş t+1 açılış; R15 = 15. geçerli bar kapanışı / giriş − 1.

## Kasa
- Bloklar: 2023Q1 .. 2024Q4 (8 blok), hipotez adı MACD_UYUM_T, bir kez. 2025 blokları AÇILMAZ.
- Olay dönemi: giriş günü 2023-01-01 .. 2024-12-31 ve R15 penceresi 2024-12-31'i aşmayan olaylar.
- Hücreler: ABD (2023-24), AVR (2023-24) = karar; BIST bilgi. Yıl ayrımı (2023 / 2024) bilgi.

## Ölçüler
- Ö1 (ANA; Cemal 25 Kas: 'asıl iz, eşler içinde en çok zıplayanı bulmaktır'): ÜST10 = olayın temiz eşleri içindeki sırası >= 0,90 olan olay payı; ALT10 = sıra <= 0,10 payı. Ay kümeli bootstrap %95 (B 2000, giriş ayı).
- Ö2: R15 temiz eş FARK (olay − eş ortalaması), ay kümeli boot %95; SIRA ortalaması; C2.c2_hucre + MU.mu_hukum (plasebo hariç) hükmü.
- Ö3 (bilgi): piyasa yukarı (eş ortalaması > 0) ve aşağı günlerde ÜST10 / ALT10; +%5 hedef ve stop payları olay / eş; kontrol Tz (T dışındaki U1 olayları) aynı ölçüler.

## Karar kuralı (sonuçtan sonra değişmez)
- TUTTU ⇔ (a) ABD + AVR birleşik ÜST10 payının boot %95 alt ucu > 0,10 VE (b) birleşik ÜST10 > ALT10 VE (c) ABD'de ve AVR'de ayrı ayrı ÜST10 nokta payı > 0,10 VE (d) birleşik R15 FARK > 0.
- KISMEN ⇔ (b), (c), (d) tutuyor ama (a) tutmuyor (yön doğru, kanıt yetersiz).
- TUTMADI ⇔ aksi.
- Birleşik olay sayısı < 100 ise hüküm ÖLÇÜLEMEDİ (yön yine yazılır).
- Açık veri beklentisi (2016-22, ABD + AVR, n 669): ÜST10 %16,6 [13,7; 19,7], ALT10 %14,5, FARK +0,4 .. +1,6 puan. Bu sayılar keşiftir (7-8. bakış); kasa sonucu onlardan bağımsız okunur.
- Sonuç ne olursa olsun yazılır; kasa bu hipotez için ikinci kez açılmaz; tanım / eşik düzeltmesi yapılmaz.
- Evren yalnız bugün işlem görenler: sonuç yukarı yanlı (K7). Komisyon / kayma yok. Tek başına alım-satım kuralı değildir (tarayıcı yalnız aday bulur).

---

## EK (alt ajan, 2026-11-25 ~06:00 UTC; kasa / yerel mühür KURULMADAN ve ölçümden ÖNCE; ana bölüme dokunulmadı)

### Kod ve eşik sha'ları (bu commit'ten sonra DEĞİŞMEZ)
KASA_HIPOTEZ: MACD_UYUM_T
KASA_KOD: MACD_UYUM_KASA.py 47f9690a55a9b62767acbfd217eb7594625a35f75c50b9f76088c77c092eecf7
KASA_KOD: MACD_UYUM.py a8b37d06e9d8efee749f5b30dd26932d081fcc6d02f468cf94acb71b68fffbd0
KASA_KOD: MACD_UYUM_ES.py cf11efdb57c4c78bcf0b45dd41d9b14d321939d13fe429aa19138105ab6685a8
KASA_KOD: CETVEL2.py 2c0fd9b9968515f1acea03da31cb550b9d7e0d837391139e1194da6eb39530e6
KASA_KOD: KASA.py 3db7b60d44bee8234c7c41e42ba7a8c3a3fc43803222a1f7e06adc154d41805b
- test_macd_uyum_kasa.py 8eadf3853acb51a86d192bc2f9030546de3c6cc50b60eb7165f2af339625062d (8 sentetik test geçti)
- MK_ESIK sha a5e6a45859d0175e89c747bad22563c0b8eec14f34f6a6a5c3462623849fea6b; MU_ESIK d53e8cf81ba4…; ES_ESIK cead08e439b0…; C2_ESIK22 df651ccbcd31…; YH_ESIK8 d28e8257274a…; cetvel2_esik_v2.2.json f45e68ed49de…; cetvel2_guc_v2.2.json 95528165cb5c… (tam değerler kasa_t_dogrulama.json 'sha').
- Bağımlı: YAPI_HEDEF.py 812d188c20a6…, ORTAK_CETVEL.py 7bd6f6db4bbc…, POZITIF_KONTROL.py 896a70ed7044…, DUSUS_SONRASI.py b3b3a2154c68….
- Komut: `python MACD_UYUM_KASA.py olc --veri <yerel mühür açık kısmı>` (aynı çıktı klasörüne ikinci koşu DURUR).

### Doğrulama (açık veri /tmp/kasa/acik, en geç 2022-12-30; `python MACD_UYUM_KASA.py dogrula`; 142 sn; kasa_t_dogrulama.json)
- U1 olayları = uyum_olay.csv.gz: ABD 4716 / 4716, AVR 1798 / 1798, BIST 1486 / 1486 (tarih, i, L1, L2 birebir; sayılar göreli 1e-10, dosya 12 anlamlı basamak).
- Zincir = uyum_zincir.csv.gz birebir; PFc / MRc = uyum_toplam.csv.gz (mutlak fark <= 1e-9; dosya biçimi). 8000 / 8000.
- Eş satırları = es_satir.csv.gz: ABD 3266, AVR 1499, BIST 1073 (dönem, n_es, n_es_temiz birebir; r15, es_r15_temiz, sira_temiz, fark_temiz göreli 1e-9). h5 / st5 / es_h5 / es_st5 = uyum_satir.csv.gz U1.
- T hücreleri = uyum_t_sonuc.json (12 / 12 hücre; n, FARK, boot alt, SIRA, hüküm; Ç223 tohumları 900 + 10 x pazar + dönem): T ABD d2022 n 357, FARK +1,36; AVR d1619 n 64, +1,60; ABD d1619 156 +0,39; AVR d2022 92 +0,57.
- ÜST10 / ALT10 (ABD + AVR, d1619 + d2022): n 669, ÜST10 %16,59, ALT10 %14,50 = uyum_ust10_bilgi.json birebir. Boot aralığı bu kodda [13,8; 19,6] (bilgi dosyası [13,7; 19,7]: tohum farkı, nokta değerler aynı).
- Kuru koşu (kasa yolu, açık veride, giriş penceresi bellekte 2021-22'ye çekilerek, geçici klasör /tmp/mk_kuru; dosya değişmedi): uçtan uca çalıştı; prefix 30 / 30 x 3 pazar; K11 tuttu. Bu sayılar keşif verisidir, kasa sonucu değildir.

### Uygulama yorumları (kasa açılmadan önce)
1. KASA yolu bu oturumda KURULAMIYOR: KASA_GIZLI (gizli anahtar) ortamda yok; `KASA.py ac` çalışamaz. Ayrıca KASA.py ac mantığına göre 2023Q1-Q4 (mühür 4a7fbad…) ve 2024Q1-Q4 (32d362…) blokları KART_TUR1 / KART_TUR2 için zaten açılmış; yeni hipotez için yalnız 'kayıt' satırı yazılabilir ve bu da ön kayıt commit'i ilk açılıştan (21-22 Kas) önce olmayı ister; bu ön kayıt 25 Kas: anahtar olsa da ac DURURDU. Bu yüzden KASA_DEFTERI.md'ye satır YAZILMAYACAK (elle de yazılmaz).
2. İzinli tek alternatif uygulanır: 'YEREL MÜHÜR'. islenmis-veri fce5d94 (KASA 1 ve Ç217 ile aynı kaynak) /tmp altında açılır, KASA.ks_muhurle ile kesik 2024-12-31 mühürlenir (açık anahtar arastirma_cikti/kasa/kasa_acik_anahtar.pem; manifest repo DIŞINDA); 2025+ bloklar şifreli kalır (gizli anahtar yok, açılamaz); tam kaynak mühürden hemen sonra silinir. Ölçüm yalnız açık kısımdan (<= 2024-12-31), kasa_kapisi ile denetlenir. Ham pkl'den doğrudan 2023+ okuma YOK. Açık kısmın 2022-12-31'e kadarki satırlarının /tmp/kasa/acik ile aynı olduğu denetlenir.
3. KASA 2 (32d362…) farklı, tazelenmiş bir kaynakla (V_ABD2 / V_AVR2, 2026-11-20) kurulmuştu; yerel mühür KASA 1 kaynağını (fce5d94) kullanır. 2024 fiyatlarında küçük fark olabilir; tanım değişmez.
4. Olay örneklemi: U1 olayları bütün veride (2015+) taranır, zincir geçmişi 2022 ve öncesinden gelir; c2_olay (OC giriş t+1 açılış, havuz, tekil 15) sonrası giriş 2023-01-01 .. 2024-12-31; R15 sonlu (15. geçerli bar veri sonunu aşmaz) ve temiz eş >= 5 olanlar ölçülür (Ç223 hücre tanımıyla aynı: dropna r15, es_r15_temiz).
5. Ö1 boot: MU.mu_sira_boot (ay kümeli, multinomial, B 2000, %2,5 / %97,5) 0/1 göstergesine uygulanır; tohumlar MK_ESIK['tohum'] (sonuçtan önce sabit).
6. Ö2: ABD ve AVR hücreleri c2_hucre + mu_hukum (plasebo hariç, güç eğrisi: hücre adı 'k2324' eğride yok -> 'acik' eğrisi). Birleşik (ABD + AVR) hücre için güç eğrisi yok: FARK, boot, SIRA bilgi olarak yazılır, hüküm ÖLÇÜLEMEDİ görünür; karar kuralının (d) maddesi birleşik FARK NOKTA değeridir.
7. Karar kuralı mk_karar'da harfiyen: '>' kesin büyük (ör. ÜST10 tam 0,10 ise (c) tutmaz). BIST ve yıl ayrımı yalnız bilgi.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt; HAYIR ya da boş = kos çalışmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı ATRP x likidite x F15 kovası, en az 5) + K20 temiz eş (ES.es_kirli_cift / es_es aynen); ÜST10 eş içi sıra; kontrol Tz (T dışı U1) aynı ölçülerle; 200 eş plasebo koşulmuyor (hüküm plasebo hariç, yazılı) |
| K2 | geleceğe bakma | EVET | zincir yalnız önceki olaylardan (mk_zincir; test_zincir_gecmis); mk_prefix pazar başına 30 KASA olayı veri t'de kesilip U1 + zincir + PFc + MRc + T yeniden; kasa_kapisi kesik 2024-12-31, 2025+ hiç yüklenmez (yerel mühür) |
| K3 | geçerli bar | EVET | YH._yh_hazir (H > L, V > 0) üzerinden MU.mu_hisse; eş havuzu CETVEL2 (P ok, R15 sonlu) aynen |
| K4 | tekilleştirme | EVET | U1: dip başına ilk gün + 15 bar; c2_olay tekil 15; her olay bir kez; FARK yanında medyan raporlanır |
| K5 | giriş fiyatı | EVET | giriş t+1 açılış (OC / c2_olay); R15 = 15. geçerli bar kapanışı / giriş - 1 |
| K6 | veri birimi | EVET | tek kaynak islenmis-veri fce5d94 (KASA 1 ile aynı); oran ölçüleri (R15, SIRA, PFc, MRc); 2022'ye kadarki satırlar /tmp/kasa/acik ile denetlenir |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler; batanlar yok; sonuç yukarı yanlı okunur (rapor ve ana bölümde yazılı) |
| K8 | örneklem ve dönem | EVET | birleşik n < 100 ÖLÇÜLEMEDİ; hücre n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; 2023 / 2024 ayrı bilgi; tek önceden yazılı karar (BH gerekmez); açık verideki 7-8 bakış yazılı |
| K9 | ön kayıt | EVET | ana bölüm 2aedf2e (05:48 UTC); bu EK + kod sha'ları yerel mühürden ve ölçümden önce commit; mk_olc ik_kontrol_kapisi çağırır; eşik / tohum MK_ESIK sha a5e6a458… |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırması yok; yalnız OHLCV pkl ve Ç217 / Ç222 / Ç223 satır dosyaları (doğrulamada birebir) |
| K11 | yeniden üretim | EVET | mk_yeniden: birleşik T ÜST10 / ALT10 / n ve ABD T FARK / n kasa_t_satir.csv.gz'den düz pandas ile (göreli 1e-9); tutmazsa DURUR |
| K12 | ifade | EVET | karar yalnız ön kayıttaki kuralla (mk_karar); yıl / piyasa / BIST bilgi, hüküm taşımaz; sayı ile yorum ayrı; alım-satım önerisi yok |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_mk, test); MU / ES / CETVEL2 / KASA / IZ_KARNE değişmez (sha yukarıda); KASA_DEFTERI elle yazılmaz; push yok; gizli anahtar aranmaz / kullanılmaz |
| K14 | boyut (gerçek para) | UYGULANMAZ | alım-satım önerisi yok; ölçüm |
