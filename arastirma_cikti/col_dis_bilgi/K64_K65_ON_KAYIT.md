# K64 + K65 — ÇÖL SİNYALİNE EK BİLGİ: ÖN KAYIT (ölçümden ÖNCE)

K64 v1.0 (2026-11-11): çöl sinyaline ek bilgi; K64 52 hafta zirvesi ailesi + K65 şirket kalitesi ailesi; S1 çöl içi üçte bir, S2 çöl dışı evren
Yazım zamanı: 2026-11-11 18:18:50 UTC (2026-11-11 21:18 TR)
ESIK_SHA256: a4c6da913a10fef1e8e237e0d169283eefd3a45a95cc06fe9361b378523540ca

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `kapsam` sayımı koşuldu: §12). `python -I K64.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- liste_bist_2016_22.csv.gz: sha256 fcb005778d673ea073830c826489a696dd27d2ccee258abfc23b92d7c890e3ca (1 dosya)
- liste_bist.csv.gz: sha256 aa063aceb770cbcc5e8e1c1a9de78756b118697ca27a9a7290ce7ba3a8f2a81c (1 dosya)
- k64_bist_temel: sha256 6e3ddb4c4c3843f21f198ffa32364aded3d06db0e8531648859f3b22fa4b9a10 (7553 dosya)
- K60_ON_KAYIT.md: sha256 eba12e1d060217f2c1fd4ffe5715382d29d343cd29004af5c69617b10b2218c0 (1 dosya)
- FON_IZI.py: sha256 ea0cc19f9b6514c50340df0e331c8d1a5e7961083918eefec45de6d7eb10ac7b (1 dosya)
- K60.py: sha256 d819f93082188688f5a3ed2a5d1bdb39735169125f292c62103b3e842ebd8e66 (1 dosya)
- COL_v1.py: sha256 13597d4209698a7edbeb4fb947c383ffa1c3c2d9eb715e33c5ef6902ce8987b8 (1 dosya)
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True). K60 mührü mühre girer.

## 0. Soru (Cemal'in isteği)
Çöl tanımı ve mevcut cetvel DEĞİŞMEZ. İki değişken ailesi (K64: 52 haftalık zirve; K65: şirket kalitesi) mevcut ÇÖL sinyaline EK BİLGİ taşıyor mu?
Her değişken tek tek ve çöl sinyaliyle etkileşimli sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.

## 1. Olay (çöl sinyali; tanımlar DEĞİŞTİRİLMEDEN içe alınır)
ÇÖL TANIMI ENVANTERİ (depoda çöl olayı üreten tanımlar):
- (i) K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, eşikler FI_K24 = {"seri": 5, "once": 10, "once_alt": 0.8, "delen_en_cok": 2, "bbw_oran": 0.7, "bbw_pencere": 15, "dusus": -0.3, "tekrar": 60}. Sinyal günü t: SMA20 üstündeki kapanış serisinin
  tam 5. günü; serinin önündeki 10 barın >= %80'i SMA20 altında; serideki mumların en çok 2'sinin dibi SMA20'yi deler;
  Bollinger genişliği son 15 barın en yükseğinin <= %70'i; son 15 barın dibi önceki 120 bar tepesinin en az %30 altında.
  K28 / K29 / K32 / K38-B (F1) / K41 / Ç118'de 'çöl' olarak, iki pazarda aynı kodla ve FI_OLCUT cetveliyle kullanıldı. **ANA olay tanımı budur.**
  Çöl başlangıcı b = t - 14 işlem günü (1. evrenin ve 15 barlık sıkışma penceresinin ilk barı). Giriş = hissenin t'den sonraki ilk işlem günü açılışı.
- (ii) Üretim tanımı — COL_v1.col_olc (SEGMENT_MOD = 'dip2': D13 dip kutusu; uzunluk >= 20 bar, yükseklik <= 6.0 ATR) + üretim kuralı GECER (clv >= -0.164,
  bant_son >= 0.509, ortaust >= 0.4) + AL: kapanış > tavan x 1.002. **İKİNCİL (sağlamlık) tanım:** tespit günleri her haftanın son işlem günü e (yalnız <= e barları;
  en az 300 bar); olay günü = e'den sonraki 60 bar içinde, kapanış tabanın altına inmeden önce, ilk AL kırılımı günü (COL_v1.tara kuralı); kırılımdan önce
  GECER tespiti olmalı. Çöl başlangıcı b = kutu başı (dip günü, 'bas_tarih'). Giriş = kırılımdan sonraki ilk işlem günü açılışı. Haftalık tespit ızgarası hesap
  süresi içindir (günlük ızgara ~5 kat süre); üretim de günde bir kez tarar, bu yüzden haftalık ızgara üretimin bulacağı kırılımların bir ALT KÜMESİNİ verir (beyan).
  İkincil tanım BH ailesine ve karara GİRMEZ; yalnız 'aynı yön mü' diye raporlanır.
- (iii) K51 COL_YOLU_ABD P1 ('çöl oluşurken': cy_olculer / cy_cekirdek / cy_imza / cy_sinyaller; L = 60, düşüş <= -%35, imza >= 3). Bu işte KULLANILMAZ: 'çöl bitiş / sinyal günü'
  değil oluşum günüdür, kendi evreni (batanlar örneklemi + likidite maskesi) ve kendi cetveli (üçlü bariyer) vardır.
TEKİLLEŞTİRME: aynı hissede 60 işlem günü içinde tekrarlanan sinyal tek olaydır; son TUTULAN sinyalden en az 60 işlem günü sonra gelen ilk sinyal tutulur
(ANA tanımda FI_K24 'tekrar' = 60 ile birebir aynı sonuç; kodda denetlenir).

## 2. Evren, veri ve bilgi tarihi
- Fiyat: BIST = V_BIST.pkl, ABD = V_ABD.pkl (islenmis-veri dalı; FON_IZI.fi_k1_veri çıktıları; K24 çöl cetvelinin ölçüldüğü evrenler). Fon krizi: 2026-08-31
  sonrası barlar atılır; 60 günlük penceresi bu tarihi aşan olay ölçülmez (FI_OLCUT 'kriz').
- ABD temel veri: K60 demeti (SEC XBRL frames 2009Q1-2026Q2 + EDGAR başvuru dizini), K60.py DEĞİŞTİRİLMEDEN içe alınır. BİLGİ TARİHİ kuralı K60_ON_KAYIT.md §3
  ile aynıdır: bir çeyreğin bilgi tarihi = çeyrek sonundan en az 15 gün sonraki ilk 10-Q / 10-K ailesi başvurusunun günü (yoksa yedek: çeyrek sonu + 90, mali yıl
  sonu + 120 gün); bir değer ancak bilgi tarihi < t ise kullanılır; ç0 = bilgi tarihi < t olan en son çeyrek (çeyrek sonu t'den en çok 200 gün önce), y0 = en son
  mali yıl (en çok 550 gün). V_ABD sembolü K60 demetinde yoksa temel veri YOK sayılır.
- BIST temel veri: KALEMLER İş Yatırım mali tablo servisi (MaliTablo, financialGroup XI_29, 2014-2026; `python K64.py indir`): {"Assets": "1BL", "StockholdersEquity": "2N", "Revenues": "3C", "GrossProfit": "3D", "OperatingIncomeLoss": "3DF", "NetIncomeLoss": "3L", "NetCashProvidedByUsedInOperatingActivities": "4C", "PaymentsToAcquirePropertyPlantAndEquipment": "4CAI"}.
  Gelir tablosu ve nakit akışı kümülatiftir; çeyrek = kümülatif farkı (aynı takvim yılı içinde). Satış geliri 0 / yok olan dönemde satış ve brüt kâr YOK sayılır.
  BİLGİ TARİHİ = KAP 'Finansal Rapor' listesinde (FON_IZI.fi_k28_liste_bist çıktıları; 2016-07 ->) aynı hisse-yıl-dönemin İLK yayın günü; KAP kaydı yoksa ya da dönem
  sonuna 5 günden yakınsa YEDEK: ara dönem sonu + 75 gün, yıl sonu + 100 gün. 'Bilgi tarihi < t' kuralı aynen (akşam yayınları için de güvenli).
  Banka / sigorta / faktoring gibi XI_29 şablonu dışındaki şirketlerde kalem YOK ('BIST VERİSİ YOK'; vekil uydurulmaz).
- BIST'te PAY_D (hisse sayısı değişimi) için 'BIST VERİSİ YOK': ödenmiş sermaye değişimi bedelsiz (seyrelme değil) ile bedelli / tahsisli artışı ayırmıyor; güvenilir
  bölünme düzeltmeli pay serisi yok. Vekil uydurulmadı.

## 3. Değişkenler (hepsi yalnız sinyal günü t ve öncesi bilgiyle; C = hissenin kendi işlem günlerindeki kapanış)
| kod | aile | tanım | kaynak / beklenti (bilgi) |
|---|---|---|---|
| Z52 | K64 | C(t) / max(C[t-251 .. t]) (son 252 işlem gününün en yüksek KAPANIŞI, t dahil; en az 200 gözlem). 1 = zirvede | George-Hwang 2004 (zirveye yakın = iyi) |
| D52 | K64 | C(t) / min(C[t-251 .. t]) (son 252 işlem gününün en düşük kapanışı; en az 200 gözlem). 1 = dipte | proje ölçüsü |
| HIZ | K64 | Z52(t) - Z52(t-20) (20 işlem gününde zirveye yaklaşma; ikisi de olmalı) | proje ölçüsü |
| DUSUS | K64 | çöl başlangıcı b gününde DD252(b) = C(b) / max(C[b-252 .. b-1]) - 1 (önceki 252 günün en yüksek kapanışından çöl başlangıç kapanışına; en az 200 gözlem). ANA tanımda b = t - 14 işlem günü (K24 1. evresinin ilk barı); İKİNCİL tanımda b = kutu başı (dip günü). Daha eksi = daha derin düşüş | Cemal'in tanımı: çöl düşüş sonrası dipte olur |
| GP | K65 | brüt kâr son 4 çeyrek / toplam varlık(ç0) (K60 GP_A) | Novy-Marx 2013 |
| OP | K65 | faaliyet kârı son 4 çeyrek / özkaynak(ç0); özkaynak > 0 (K60 OP_BE) | Fama-French 2006 |
| FCF | K65 | (işletme nakit akışı - maddi duran varlık yatırımı) / toplam varlık. ABD: son mali yıl y0 / varlık(y0 sonu) (çeyreklik nakit akışı önbellekte yok); BIST: son 4 çeyrek / varlık(ç0). İki kalem de olmalı | serbest nakit akışı verimi (varlığa göre) |
| BORC | K65 | toplam yükümlülük(ç0) / toplam varlık(ç0); yükümlülük = Liabilities, yoksa varlık - özkaynak | defter kaldıracı (düşük = sağlam) |
| SATIS_B | K65 | satış(ç0) / satış(ç0-4) - 1; ikisi de > 0 (K60 REV_YOY) | proje ölçüsü (K59 X1) |
| KAR_B | K65 | (net kâr son 4 çeyrek(ç0) - net kâr son 4 çeyrek(ç0-4)) / toplam varlık(ç0-4) | kâr büyümesi (varlığa göre) |
| PAY_D | K65 | ln(pay(t) / pay(t - 365 gün)); pay bölünme düzeltmeli, iki uç aynı kaynaktan; oran > 5 ya da < 1/5 ise veri yok (K60 NSI_1Y kuralı, günlük) | Pontiff-Woodgate 2008 (ihraç = kötü) |

K65 değişkenleri K60'ın 'o gün bilinen' okuyucusuyla (K60._K60Temel, K60.k60_pay, K60._k60_bol / _k60_ilk; gelir etiketleri K57_ABD_GELIR) hesaplanır; GP = K60 GP_A,
OP = K60 OP_BE, SATIS_B = K60 REV_YOY formülleridir (ay sonunda K60 ile birebir aynı; testte denetlenir). Beklenti sütunu bilgidir: her değişken İKİ YÖNDE sınanır.

## 4. S1 — 'etkileşim / ek katkı' (asıl soru)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen).
- İki sıra türü her değişken için hesaplanır; hangisinin KARAR sırası olduğu AİLE BAZINDA sabittir (aşağıda). Öteki sıra o değişkende 'sağlamlık, karar dışı'dır.
- 'EVREN' sırası: olayın değişken değerinin, AYNI GÜN o pazarda işlem gören ve o değişkeni hesaplanabilen bütün hisseler içindeki
  yüzdelik sırası = (küçük olan sayısı + 0,5 x eşit olan sayısı, kendisi dahil) / n (n >= 30). ÜST = sıra >= 2/3, ALT = sıra <= 1/3, ORTA = arası.
  (DUSUS ikincil tanımda çöl başlangıcı gününde okunur ve o günün evren sırasıyla sınıflanır.)
- 'İÇ' (çöl içi) sırası: olayın değerinin, sinyal günü [t - 365 gün, t] aralığındaki aynı pazar ve tanımın tekil çöl olayları (kendisi dahil) içindeki sırası
  (n >= 30; geleceğe bakmaz). ÜST / ALT eşikleri aynı (>= 2/3, <= 1/3).
- **KARAR SIRASI (aile bazında; ana oturum kararı, 11 Kasım 2026):** K64 ailesi (Z52, D52, HIZ, DUSUS) = **İÇ**; K65 ailesi (GP, OP, FCF, BORC, SATIS_B, KAR_B, PAY_D) = **EVREN**.
  K64 ailesinde EVREN, K65 ailesinde İÇ sırası 'sağlamlık, karar dışı' olarak raporlanır (karara ve BH ailesine GİRMEZ).
  GEREKÇE: çöl tanımı gereği düşmüş hissedir; evren sırası K64 ölçülerinde olayları ALT üçte birde topluyor (kapsam sayımı §12: DUSUS ABD 2022-2026 ÜST n = 27; Z52 ABD ÜST
  160 / 90 / 38) ve 'çöl İÇİNDE ayırıyor mu' sorusu evren sırasıyla ölçülemez kalıyor. Bu karar ölçümden ÖNCE, yalnız KAPSAM SAYIMI (olay sayıları) görülerek verildi:
  **kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı). Başka hiçbir eşik ya da kural değişmedi.
- Temel model = hücredeki BÜTÜN çöl olayları (değişkensiz). Her grup için FI_OLCUT ölçüleri (§6).
- ÜST - ALT = iki grubun ortalama eşli farklarının farkı; ay kümeli bootstrap (giriş ayları yerine koyarak çekilir, iki grup aynı çekilişle kurulur; 2000 çekiliş,
  tohum 64001; iki grubu da dolu çekiliş payı < %90 ise aralık yok); %95 aralık = 2.5 / 97.5 yüzdelikleri.
- **'EK KATKI VAR (yön ÜST)'** <=> n_ÜST >= 30 ve n_ALT >= 30 VE ÜST grubunun ortalama eşli farkı > temel modelin ortalama eşli farkı VE (ÜST - ALT) %95 alt sınırı > 0.
  **'EK KATKI VAR (yön ALT)'** ayna: ALT grubunun ortalama eşli farkı > temel VE (ÜST - ALT) %95 üst sınırı < 0.

## 5. S2 — 'tek başına' (bilgi)
Aynı değişkenin çöl DIŞI evrende, ANA çöl sinyali olan günlerde, evren içi ÜST / ALT üçte birindeki hisselerin (giriş = ertesi takvim günü açılışı) 60 günlük eşli
farkı ve ÜST - ALT (ay kümeli bootstrap; 2000 çekiliş, tohum 64002). 'Çöl dışı' = o gün ve önceki 59 işlem gününde tekil ANA çöl sinyali vermemiş hisse.
S2 karara girmez; 'değişken çölden bağımsız da çalışıyor mu' sorusunun cevabıdır.

## 6. Cetvel (FON_IZI FI_OLCUT aynen; fonksiyonlar çağrılır, kopyalanmaz)
FI_OLCUT = {"ufuk": 60, "mom": 60, "likit": 20, "mom_kova": 5, "likit_kova": 3, "kriz": "2026-08-31", "bootstrap": 2000, "tohum": 27, "slot": 10, "n_esik": 30, "port_n": 200, "port_yuzde": 0.9}.
- fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre: giriş = sinyalden sonraki ilk işlem günü açılışı; r60 = 60. gün kapanışı / giriş - 1; EŞLİ FARK = r60 - aynı giriş günü
  aynı 60 gün momentum beşliği x likidite üçlüsü hücresindeki öteki hisselerin ortalama r60'ı; ay kümeli bootstrap %95; hücre içi sıra; 10 yuvalı slot portföyü 200
  rastgele eş portföyün %90'ından büyük. HÜCRE TUTAR <=> n >= 30, aralığın alt ucu > 0, ortalama sıra > 0,50, portföy > rastgele %90.
- Eşli kontrol boyutları: aynı gün (dolayısıyla aynı ay), momentum, likidite (FI_OLCUT) + PİYASA KOŞULU katmanı: sinyal günü eşit ağırlıklı evren endeksi (günlük
  kapanış getirilerinin ortalaması) 200 günlük ortalamasının üstünde / altında; ÜST, ALT ve TEMEL grupları iki katmanda ayrı raporlanır (bilgi).
- Ek ufuk: r20 ve 20 günlük eşli fark aynı yöntemle (fi_olcut_panel ufuk = 20; bilgi).
- Raporlanan: n, ortalama ve medyan getiri (20 ve 60 gün), ortalama ve medyan eşli fark, %95 aralık, sıra, portföy, dört şart.
- MALİYET: gidiş-dönüş BIST 60 bp, ABD 20 bp (tek yön 30 / 10 bp) her olayın getirisinden ve eşli farkından düşülür; rastgele eş portföyler
  maliyetsiz bırakılır (tutucu). Uygulanabilirlik: giriş ertesi açılış; olay başına tek giriş; slot portföyü 10 yuva.

## 7. Hücreler ve KARAR
- Hücre = pazar (BIST, ABD) x dönem (giriş gününe göre): 2017-2021 (2017-01-01 .. 2021-12-31), 2022-2026 (2022-01-01 .. 2026-12-31), 2023-2026 (2023-01-01 .. 2026-12-31). Son iki dönem ÖRTÜŞÜR (2023-2026, 2022-2026'nın alt kümesi); bağımsız dönemler
  2017-2021 ve 2022-2026. 2023-2026 tutarlılık için ayrıca raporlanır, BH ailesine girmez.
- Karar birimi: (değişken, yön). ANA tanım (K24) ve değişkenin KARAR sırası ile (§4: K64 ailesi İÇ, K65 ailesi EVREN; kapsam sayımı görüldü, getiri görülmedi).
- Pazar kararı: **'ADAY'** <=> o pazarın iki bağımsız döneminin İKİSİNDE de aynı yönde 'EK KATKI VAR' ve ikisi de çoklu test düzeltmesinden geçiyor (§8).
  İki bağımsız dönemden birinde n_ÜST ya da n_ALT < 30 ise **'ÖLÇÜLEMEZ'** (az veri; 'İZ DEĞİL' ile karıştırılmaz). Aksi **'İZ DEĞİL'**.
- İŞARET: ölçülebilen bütün hücrelerde (iki pazar x üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı; bir hücrede işaret dönerse aday düşer ('İZ DEĞİL').
- Genel karar: karar pazarı ABD'dir (CLAUDE.md: BIST bilgi). ABD 'ADAY' ve işaret tutarlı -> **'ABD-ADAY'**. 'İZ' bu işte VERİLEMEZ: İZ = ABD'nin üç döneminde de
  'ek katkı VAR' + grubun FI_OLCUT dört şartı + aynısının Avrupa'da tutması; Avrupa temel verisi ve Avrupa çöl koşusu bu işte yok. Yalnız BIST 'ADAY' ->
  'BIST-ADAY (bilgi)'. Grubun dört şartı (maliyetsiz ve maliyetli) üç dönemde tutuyorsa ayrıca yazılır.

## 8. Çoklu test
Aile = ANA tanım, değişkenin KARAR sırası (§4: K64 ailesi İÇ, K65 ailesi EVREN; karar kapsam sayımı görülerek, getiri görülmeden verildi), ölçülebilen bütün (değişken x yön x pazar x bağımsız dönem) hipotezleri (en çok 11 x 2 x 2 x 2 - 4 = 84; BIST PAY_D yok).
p = 1 - Φ(±(ÜST - ALT) / bootstrap standart sapması) (tek yönlü). Benjamini-Hochberg q = %10 (K60.k60_bh); Bonferroni (p x m <= %10) bilgi olarak yazılır.

## 9. GÜÇ BEYANI
K58 (arastirma_cikti/k58_cetvel_sagla/K58_RAPOR.md): FI_OLCUT, 60 günde +%2'lik gerçek etkiyi n = 300 olayda yalnız %11, +%4'ü %45 olasılıkla yakalıyor. Çöl olayları
içinde üçte bir grupları daha da küçüktür (§12). Her hücrede n ve 'saptanabilir en küçük etki' (grup aralığının yarı genişliği; ÜST - ALT için aralık yarı genişliği)
raporlanır. 'İZ DEĞİL' yalnız ölçülebilen hücreler için söylenir; n < 30 olan hücre 'ÖLÇÜLEMEZ'dir. 'Ek katkı yok' sonucu 'etki yok' demek değildir; 'bu veriyle
gösterilemedi' demektir.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI (kaçınılamıyor): iki evren de yalnız BUGÜN işlem gören hisselerdir (V_BIST 2026-10, V_ABD 2026-10 listeleri). Batan / kottan çıkan şirketler yok;
  çöl (düşmüş hisse) ve düşük kalite grupları batmaya en açık gruplardır, bu grupların getirisi YUKARI yanlıdır. Kaliteli - kalitesiz farkı bu yüzden olduğundan
  KÜÇÜK görünebilir (kalitesizlerin batanları örneklemde yok). Eşli kontrol aynı evrenden seçildiği için yanlılığın bir kısmı farkta götürülür, tamamı değil.
- Yeniden sunum: SEC frames ve İş Yatırım değerleri ilk açıklanan değil, sonradan düzeltilmiş değer olabilir (tarih doğru, değer yeniden sunulmuş olabilir).
- BIST: TMS 29 (enflasyon muhasebesi; 2023 yıl sonu ve sonrası) kümülatif farklarını ve yıllık büyümeleri bozar (farklı satın alma gücü); bütün şirketleri birlikte
  etkilediği için sıra tabanlı gruplar kısmen korunur. Özel hesap dönemli şirketlerde (ör. spor kulüpleri) kümülatif farkı yanlış çeyrek verir. KAP listesi 2016-07
  öncesini kapsamaz (yedek kural). Fiyatlar fi_duzelt ile bölünme / bedelsiz düzeltmelidir; temettü düzeltmesi yok.
- ABD: yedek bilgi tarihi geç başvuranlarda geleceğe bakabilir (K60 beyanı). FCF yıllıktır (y0): çeyreklik nakit akışı önbellekte yok. V_ABD fiyatları temettü
  düzeltmelidir (Yahoo); 52 hafta ölçüleri düzeltilmiş kapanışla hesaplanır.
- K24 sinyali yalnız fiyatla tanımlıdır; sektör rüzgârı / katalizör şartı içermez (Cemal'in çöl tanımının tamamı değildir; cetvelde kullanılan ölçülebilir hâlidir).

## 11. SAPMA / BOŞLUK listesi (iş tanımına göre; en dar yorum)
BOŞLUK 1. DUSUS ANA tanımda 'çöl başlangıcı' = t - 14 işlem günü: K24 çöl başlangıcını ayrı bir gün olarak vermez; kuralın baktığı pencerenin ilk barı alındı.
BOŞLUK 2. Dönem = GİRİŞ gününe göre (FI_OLCUT alışkanlığı). 2017-2021 çöllerinin 252 günlük geçmişi için fiyat 2015-06'dan başlar (yeterli).
BOŞLUK 3. BORC = toplam yükümlülük / toplam varlık (iki pazarda aynı). 'Toplam finansal borç' ABD önbelleğinde yalnız uzun vadeli borç etiketiyle var (eksik); bu yüzden
  defter kaldıracı alındı. K60 LEV_MKT (yükümlülük / piyasa değeri) fiyat içerdiği için alınmadı.
BOŞLUK 4. FCF ABD'de yıllık (y0), BIST'te son 4 çeyrek. OP paydası özkaynak (K60 OP_BE); özkaynağı <= 0 olan şirkette OP yok.
BOŞLUK 5. KAR_B = TTM net kâr değişimi / dört çeyrek önceki toplam varlık. SATIS_B = son çeyrek satışının yıllık büyümesi (iki çeyrek de > 0).
BOŞLUK 6. PAY_D günlük sürüm: t ve t - 365 takvim günü (K60 NSI_1Y ay sonlarıyla 12 ay). BIST'te yok.
BOŞLUK 7. Evren sırası için 'uygun hisse' = o gün kapanışı olan ve değişkeni hesaplanabilen hisse (gelecekteki getirinin varlığına bakılmaz). Ek fiyat / likidite süzgeci yok
  (K24 çöl cetvelinde de yoktu); likidite eşli kontrolün boyutudur.
BOŞLUK 8. Piyasa koşulu endeksi eşit ağırlıklı evren getirisidir (XU100 / SPY değil); sinyal günü kapanışıyla bilinir.
BOŞLUK 9. İKİNCİL tanım haftalık tespit ızgarasıyla taranır (§1); ABD'de de üretim (BIST) sabitleriyle. Karara girmez.
BOŞLUK 10. ABD evreni V_ABD'dir (1.411 hisse; K24 cetvelinin evreni). K60'ın geniş evreni (4.666 hisse) bu işte kullanılmadı (penny / likit olmayan hisseler K24
  cetvelinde yoktu); istenirse ayrı ön kayıtla eklenir.
BOŞLUK 11. Maliyet sonrası şartta rastgele eş portföyler maliyetsizdir (tutucu). 20 günlük ölçüler bilgidir; karar 60 günlük eşli farkla verilir.
BOŞLUK 12. S2'de giriş birleşik takvimin ertesi günüdür (S1'de hissenin kendi ertesi işlem günü); S2 bilgi düzeyindedir.
BOŞLUK 13. fi_k24_tara içinde ileriye bakan SONUÇ sütunları (yon60, yon20, r120) hesaplanır; K64 bunları ALMAZ ve kullanmaz (fonksiyon değiştirilmediği için hesap sürer).
BOŞLUK 14. İşaret şartı: ölçülebilen hücrelerde nokta farkı tam sıfırsa işaret tutmaz sayılır.
SAPMA 15. KARAR SIRASI aile bazındadır (iş tanımındaki tek kural 'aynı gün evren içi sıra' idi): K64 ailesinde İÇ (çöl içi), K65 ailesinde EVREN. Gerekçe §4'te; karar
  ölçümden önce verildi: kapsam sayımı görüldü, getiri görülmedi. İşaret şartı ve dört şart sütunları da değişkenin karar sırasındaki hücrelerle hesaplanır.

## 12. Kapsam (yalnız SAYI; mühre girmez)
Kapsam sayımı (2026-11-11 18:18:13 UTC; `python -I K64.py kapsam`; yalnız SAYI: getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).

- ABD: 1411 hisse, takvim 2830 gün (2015-06-01 .. 2026-08-31); temel verisi olan hisse 1316, çeyrek kaydı 68620; bilgi tarihi gerçek kaynaktan (BIST: KAP yayın günü; ABD: EDGAR dizini) %99.6, kalanı yedek kural; K60 demetinde bulunan 1406 hisse. Evren hisse-günlerinde değişken doluluk: BORC %87, D52 %92, DUSUS %91, FCF %60, GP %47, HIZ %91, KAR_B %74, OP %59, PAY_D %82, SATIS_B %70, Z52 %92.
- BIST: 581 hisse, takvim 2863 gün (2015-06-01 .. 2026-08-31); temel verisi olan hisse 548, çeyrek kaydı 21111; bilgi tarihi gerçek kaynaktan (BIST: KAP yayın günü; ABD: EDGAR dizini) %80.6, kalanı yedek kural; kalem şablonu dışında kalan (banka / sigorta / finansman; BIST VERİSİ YOK) 33 hisse. Evren hisse-günlerinde değişken doluluk: BORC %91, D52 %91, DUSUS %90, FCF %72, GP %80, HIZ %90, KAR_B %74, OP %82, PAY_D %0, SATIS_B %78, Z52 %91.

**K24 olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay)

| pazar | dönem | ham | tekil | pencere |
|---|---|---|---|---|
| BIST | 2017-2021 | 1282 | 1157 | 1157 |
| BIST | 2022-2026 | 2147 | 1751 | 1651 |
| BIST | 2023-2026 | 1903 | 1538 | 1438 |
| ABD | 2017-2021 | 2928 | 2589 | 2589 |
| ABD | 2022-2026 | 4319 | 3721 | 3519 |
| ABD | 2023-2026 | 3091 | 2670 | 2468 |

**K24: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | BIST 2017-2021 | BIST 2022-2026 | BIST 2023-2026 | ABD 2017-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|---|---|---|
| Z52 | EVREN | 1130 / 114 / 636 | 1539 / 195 / 770 | 1345 / 184 / 646 | 2439 / 160 / 1779 | 3433 / 90 / 2312 | 2441 / 38 / 1791 |
| Z52 | İÇ | 1130 / 351 / 432 | 1539 / 545 / 526 | 1345 / 461 / 477 | 2439 / 799 / 834 | 3433 / 1102 / 1184 | 2441 / 828 / 781 |
| D52 | EVREN | 1130 / 313 / 407 | 1539 / 431 / 594 | 1345 / 382 / 515 | 2439 / 729 / 980 | 3433 / 972 / 1343 | 2441 / 695 / 1066 |
| D52 | İÇ | 1130 / 416 / 390 | 1539 / 499 / 556 | 1345 / 429 / 478 | 2439 / 996 / 680 | 3433 / 1084 / 1254 | 2441 / 891 / 772 |
| HIZ | EVREN | 1129 / 295 / 286 | 1528 / 429 / 380 | 1335 / 390 / 316 | 2427 / 779 / 619 | 3421 / 1063 / 831 | 2435 / 752 / 616 |
| HIZ | İÇ | 1129 / 387 / 347 | 1528 / 534 / 476 | 1335 / 451 / 414 | 2427 / 825 / 813 | 3421 / 1178 / 1093 | 2435 / 826 / 799 |
| DUSUS | EVREN | 1129 / 89 / 699 | 1533 / 94 / 928 | 1340 / 89 / 790 | 2430 / 129 / 1866 | 3424 / 27 / 2587 | 2438 / 11 / 2002 |
| DUSUS | İÇ | 1129 / 335 / 451 | 1533 / 545 / 499 | 1340 / 470 / 445 | 2430 / 821 / 826 | 3424 / 1093 / 1196 | 2438 / 832 / 799 |
| GP | EVREN | 914 / 288 / 321 | 1329 / 426 / 459 | 1177 / 384 / 404 | 1198 / 392 / 448 | 1727 / 604 / 601 | 1239 / 418 / 452 |
| GP | İÇ | 914 / 315 / 295 | 1329 / 444 / 456 | 1177 / 394 / 404 | 1198 / 388 / 411 | 1727 / 603 / 558 | 1239 / 423 / 407 |
| OP | EVREN | 937 / 293 / 349 | 1378 / 441 / 485 | 1220 / 394 / 428 | 1567 / 394 / 761 | 2355 / 578 / 1135 | 1710 / 382 / 861 |
| OP | İÇ | 937 / 344 / 290 | 1378 / 410 / 501 | 1220 / 355 / 452 | 1567 / 507 / 535 | 2355 / 830 / 739 | 1710 / 558 / 578 |
| FCF | EVREN | 936 / 299 / 329 | 1386 / 419 / 488 | 1224 / 370 / 428 | 1637 / 398 / 742 | 2429 / 666 / 1091 | 1755 / 446 / 830 |
| FCF | İÇ | 936 / 325 / 282 | 1386 / 442 / 481 | 1224 / 395 / 416 | 1637 / 521 / 563 | 2429 / 849 / 769 | 1755 / 585 / 604 |
| BORC | EVREN | 1046 / 364 / 320 | 1497 / 486 / 530 | 1315 / 425 / 466 | 2208 / 673 / 880 | 3170 / 978 / 1242 | 2242 / 691 / 910 |
| BORC | İÇ | 1046 / 341 / 344 | 1497 / 468 / 517 | 1315 / 408 / 454 | 2208 / 767 / 738 | 3170 / 1095 / 966 | 2242 / 754 / 745 |
| SATIS_B | EVREN | 895 / 265 / 336 | 1270 / 389 / 470 | 1131 / 363 / 406 | 1745 / 655 / 637 | 2503 / 956 / 916 | 1744 / 658 / 661 |
| SATIS_B | İÇ | 895 / 322 / 274 | 1270 / 341 / 474 | 1131 / 284 / 438 | 1745 / 592 / 577 | 2503 / 752 / 901 | 1744 / 556 / 598 |
| KAR_B | EVREN | 933 / 270 / 353 | 1235 / 390 / 451 | 1094 / 346 / 399 | 1854 / 617 / 807 | 2755 / 979 / 1146 | 2029 / 710 / 857 |
| KAR_B | İÇ | 933 / 336 / 302 | 1235 / 409 / 426 | 1094 / 343 / 388 | 1854 / 577 / 621 | 2755 / 882 / 877 | 2029 / 645 / 668 |
| PAY_D | EVREN | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 1968 / 868 / 503 | 2861 / 1308 / 687 | 2084 / 981 / 473 |
| PAY_D | İÇ | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 1968 / 682 / 634 | 2861 / 881 / 1045 | 2084 / 715 / 691 |

**D13 olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay)

| pazar | dönem | ham | tekil | pencere |
|---|---|---|---|---|
| BIST | 2017-2021 | 944 | 465 | 465 |
| BIST | 2022-2026 | 1160 | 543 | 538 |
| BIST | 2023-2026 | 1001 | 472 | 467 |
| ABD | 2017-2021 | 2606 | 1498 | 1498 |
| ABD | 2022-2026 | 3582 | 2084 | 1958 |
| ABD | 2023-2026 | 2674 | 1534 | 1408 |

**D13: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | BIST 2017-2021 | BIST 2022-2026 | BIST 2023-2026 | ABD 2017-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|---|---|---|
| Z52 | EVREN | 465 / 141 / 158 | 538 / 127 / 207 | 467 / 118 / 166 | 1498 / 262 / 717 | 1958 / 391 / 793 | 1408 / 231 / 628 |
| Z52 | İÇ | 465 / 150 / 159 | 538 / 197 / 176 | 467 / 165 / 159 | 1498 / 493 / 521 | 1958 / 614 / 704 | 1408 / 501 / 456 |
| D52 | EVREN | 465 / 104 / 186 | 538 / 86 / 238 | 467 / 83 / 189 | 1498 / 350 / 621 | 1958 / 519 / 687 | 1408 / 335 / 543 |
| D52 | İÇ | 465 / 153 / 145 | 538 / 175 / 205 | 467 / 156 / 178 | 1498 / 574 / 432 | 1958 / 607 / 687 | 1408 / 488 / 434 |
| HIZ | EVREN | 465 / 352 / 9 | 538 / 312 / 26 | 467 / 269 / 23 | 1498 / 1238 / 12 | 1958 / 1473 / 15 | 1408 / 1094 / 7 |
| HIZ | İÇ | 465 / 159 / 151 | 538 / 193 / 184 | 467 / 158 / 167 | 1498 / 529 / 504 | 1958 / 664 / 625 | 1408 / 473 / 478 |
| DUSUS | EVREN | 465 / 64 / 229 | 538 / 44 / 282 | 467 / 42 / 236 | 1497 / 70 / 1005 | 1958 / 141 / 1091 | 1408 / 78 / 840 |
| DUSUS | İÇ | 465 / 140 / 170 | 538 / 189 / 165 | 467 / 164 / 146 | 1497 / 492 / 521 | 1958 / 604 / 719 | 1408 / 493 / 471 |
| GP | EVREN | 378 / 117 / 143 | 463 / 157 / 157 | 405 / 142 / 136 | 722 / 247 / 235 | 970 / 321 / 320 | 714 / 238 / 226 |
| GP | İÇ | 378 / 124 / 111 | 463 / 144 / 177 | 405 / 123 / 157 | 722 / 242 / 246 | 970 / 324 / 306 | 714 / 237 / 225 |
| OP | EVREN | 392 / 116 / 131 | 474 / 161 / 172 | 414 / 147 / 148 | 945 / 268 / 360 | 1281 / 416 / 422 | 932 / 304 / 312 |
| OP | İÇ | 392 / 135 / 118 | 474 / 134 / 174 | 414 / 115 / 152 | 945 / 296 / 332 | 1281 / 444 / 417 | 932 / 308 / 315 |
| FCF | EVREN | 366 / 106 / 133 | 478 / 156 / 159 | 417 / 138 / 134 | 979 / 305 / 364 | 1284 / 422 / 441 | 928 / 302 / 321 |
| FCF | İÇ | 366 / 118 / 100 | 478 / 150 / 166 | 417 / 136 / 137 | 979 / 323 / 332 | 1284 / 438 / 414 | 928 / 312 / 303 |
| BORC | EVREN | 409 / 121 / 145 | 491 / 175 / 157 | 429 / 158 / 133 | 1316 / 412 / 479 | 1783 / 580 / 603 | 1295 / 420 / 447 |
| BORC | İÇ | 409 / 132 / 130 | 491 / 156 / 176 | 429 / 138 / 151 | 1316 / 442 / 446 | 1783 / 598 / 574 | 1295 / 425 / 431 |
| SATIS_B | EVREN | 375 / 124 / 109 | 454 / 131 / 172 | 396 / 118 / 148 | 1056 / 361 / 384 | 1509 / 452 / 567 | 1109 / 331 / 426 |
| SATIS_B | İÇ | 375 / 135 / 111 | 454 / 109 / 171 | 396 / 84 / 157 | 1056 / 389 / 343 | 1509 / 458 / 533 | 1109 / 342 / 384 |
| KAR_B | EVREN | 391 / 115 / 123 | 453 / 139 / 153 | 397 / 119 / 134 | 1170 / 403 / 440 | 1582 / 533 / 528 | 1165 / 385 / 395 |
| KAR_B | İÇ | 391 / 132 / 113 | 453 / 146 / 149 | 397 / 120 / 132 | 1170 / 397 / 412 | 1582 / 495 / 516 | 1165 / 349 / 396 |
| PAY_D | EVREN | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 1277 / 463 / 358 | 1728 / 570 / 572 | 1246 / 401 / 420 |
| PAY_D | İÇ | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 1277 / 440 / 420 | 1728 / 538 / 612 | 1246 / 399 / 417 |

K64 ailesinde EVREN sırasıyla (bu ailede sağlamlık, karar dışı) grubu n < 30 olan bağımsız dönem hücreleri: DUSUS ABD 2022-2026 (ÜST 27, ALT 2587).

ANA tanım, KARAR sırası (K64 ailesi İÇ, K65 ailesi EVREN), bağımsız dönemlerde grubu n < 30 olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler (pencereli olay sayısıyla; ölçülebilen olay daha az olabilir): yok. BIST PAY_D: BIST VERİSİ YOK.

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k64_olaylar.csv.gz (olay düzeyi), k64_s1.csv (hücre ölçüleri), k64_s1_fark.csv (ÜST - ALT, ek katkı), k64_s2.csv, k64_karar.csv,
k64_meta.json, K64_K65_RAPOR.md. Her değişken için raporda: veri kaynağı ve kapsamı, matematiksel tanım, örneklem, ortalama ve medyan getiri (20 ve 60 gün), eşli kontrol
farkı, güven aralığı, dönemler arası tutarlılık, maliyet sonrası sonuç, veri eksikleri, karar.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K64.py kos`  -> ölçüm + rapor (mühür, veri sha256, git doğrulanır)
3. `python K64.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K64_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13 / AL sabitleri) değişirse ESIK_SHA256 değişir ve koşu durur. Veri ya da
içe alınan kod dosyaları (FON_IZI.py, K60.py, COL_v1.py) değişirse sha256 tutmaz ve koşu durur.
