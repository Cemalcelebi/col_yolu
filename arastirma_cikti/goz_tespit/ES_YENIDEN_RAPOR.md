# ES_YENIDEN RAPOR — eski 'iz değil'lerin aynı hissenin bütün günlerine göre yeniden okunması, birinci parti (27 Kasım 2026)

Ön kayıt: ES_YENIDEN_ON_KAYIT.md (commit bc32ed7a3e32108217d0b360bf23153d141e2099 2026-11-27T19:50:00+00:00); ölçüm bir kez (2026-11-27T19:50:07Z - 2026-11-27T19:52:16Z); kod sha 0395f3665dba328e. Birim yüzde puan (H ufuklu getiri farkı). GA = ay kümeli bootstrap %95. Bu AYNI VERİDE YENİDEN OKUMADIR (kör değil): hiçbir satır 'iz' değildir; en fazla ADAY (ileri test gerekir).

## SONUÇ

BH aileleri: ZAMANLAMA 130 kol, TOPLAM 130 kol (ölçülebilir kollar).

- ZAMANLAMA: aday / emare yok
- TOPLAM: aday / emare yok

Kayıt özeti (kol sayıları, ZAMANLAMA kararı / TOPLAM kararı):

| Ç | Ad | H | Kol | ZAM ADAY | ZAM EMARE | ZAM EKSİ | ZAM YOK | ÖLÇÜLEMEDİ | TOP ADAY | TOP EMARE | TOP EKSİ | Eski hüküm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ç209 | KART TUR 2 (geniş tezgâh, KASA 2): 14 kart | 15 | 14 | 0 | 0 | 0 | 13 | 1 | 0 | 0 | 0 | ÖLÇÜLEMEDİ (KART TUR 2; 12 kart) / açık veride kartların FARK'ı ~0 |
| Ç205 | KART TUR 1 (KASA yürüyen ileri test): 11 kart | 15 | 11 | 0 | 0 | 0 | 9 | 2 | 0 | 0 | 0 | ÖLÇÜLEMEDİ (KART TUR 1; hiçbir kart tutmadı) |
| Ç206 | ÖLÇÜ SINAMASI: bilinen etki bacakları (MOM, STREV, HIGH52) | 15 | 5 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | HİÇBİR ÖLÇÜ GEÇMEDİ 0 / 36 (hat testi) |
| Ç226 | ÜÇ İZ BİRLİKTE BİLANÇO OLAYINDA (UC_IZ2) | 60 | 4 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | İZ DEĞİL (güç yeterli) |
| Ç204 | CETVEL2 R15 yeniden koşusu (Y1 tabanı + Ç194-Ç202 hipotezleri + hakem turu kolları) | 15 | 130 | 0 | 0 | 0 | 95 | 35 | 0 | 0 | 0 | İZ DEĞİL / ÖLÇÜLEMEDİ (124 hipotez; KATKI+ 0, KATKI− 0) |
| Ç191 | YAPI_HEDEF 2. tur: Y6 / Y8 / Y8B (Y7 n = 0) | 15 | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | ÖLÇÜLEMEDİ (YAPI_HEDEF 2. tur Y6-Y8; yön aleyhte) |
| Ç99 | KAP içeriden alım (K27): net alım, büyük alım, çölde alım | 60 | 3 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | İçeriden alım bildirimi olumlu bilgi taşımıyor (eşlerin gerisinde) |
| Ç189 | S+ v2 TAM GİRİLİR (TAM_DIP) | 60 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | ÖLÇÜLEMEDİ (TAM_DIP; hiçbir hücrede alt uç > 0) |

## KONTROL LİSTESİ

- Ön kayıttaki tablo (K1-K13 EVET, K14 UYGULANMAZ) ölçümden önce `IZ_KARNE.ik_kontrol_kapisi` ile geçti (ölçüm kapısı içinde yeniden çağrıldı).
- Ölçümden sonra yeniden okundu: K1 taban aynı hissenin bütün günleri + aynı gün evren ortalaması (aynı geometri) — TUTTU; K2 her kayıt kendi kesiğinde (geniş evren 2024-12-31 / 2022-12-31; V 2023-12-31 / 2026-08-31) — TUTTU; K3 geçerli bar kuralı sağlamada birebir — TUTTU; K11 iki hücre bağımsız üretildi — TUTTU; K12 'iz' sözü yok — TUTTU; K13 yasak dosyalar değişmedi (git diff boş), sızıntı taraması temiz — TUTTU.
- K4 notu: olay kümeleri kayıtların kendi tekilleştirmesiyle alındı; Ç209'da eşsiz ('essiz') olaylar da olay sayıldı (ön kayıtta yazılı).

## HATA

- HATA 1 (kurgu, bu çalışma; düzeltildi ölçümden önce): ilk kayıt tanımında Ç189 (TAM_DIP) giriş kuralı FI_OLCUT sanıldı; giriş kuralı sağlaması AVR 283 / 322, BIST 405 / 500 birebir verdi. FITIL_V2 ORTAK_CETVEL r60 kullanıyormuş (yalnız geçerli barlar, OC.oc_panel takvimi); kural 'oc' eklendi, sağlama 322 / 322, 500 / 500 (commit 165ad20, ön kayıttan önce).
- HATA 2 (iş tanımı / envanter ifadesi): iş tanımı 'olay sayısı büyükten küçüğe' diyor; envanterin sıralama sütunu 'Dosya satırı' (kart dosyalarında hisse-gün satırı, Ç99'da satış bildirimleri dahil 1.908 satır; ölçülen alım olayı 759). Sıra envanter sütunuyla alındı; seçilen 8 kaydın gerçek olay sayıları ön kayıtta.
- HATA 3 (envanter işareti): envanterin 'Kapalı konu' sütunu Ç72 ve Ç146'yı '—' gösteriyor, ama olay kümeleri kapalı Ç47 (D13) ve Ç138 (K55) ile aynı. İkisi kapalı küme sayılıp atlandı (ön kayıtta neden yazılı).
- HATA 4 (ortam): /tmp/veri boştu; /root/.kasa/ham/veri altındaki sembolik bağlar boş hedefe gidiyordu. Veri islenmis-veri paketinden (`python FON_IZI.py vpac /tmp/iv/veri /tmp/veri`) açıldı; yeni indirme yok.
- Mesaj ile iş tanımı arasında çelişki yok; mesajda adı geçen GOZ_TESPIT k2rej yardımcısı kendi G40 paneline bağlı olduğu için içe alınmadı, aynı gün evren ortalaması küçük testli yardımcıyla (es_piyasa) yazıldı; bootstrap KISA_UFUK.ku_boot, BH MUM_IZI_HAVUZ._hv_bh, FI_OLCUT / ORTAK_CETVEL panelleri içe alındı.

## SAPMA

- Yok. Ölçüm bir kez koştu (kapı: ön kayıt commit bc32ed7, push, kontrol kapısı, kod sha 0395f3665dba328e, eşik sha 59a863bad008a0a6). Sonuç görüldükten sonra kod, eşik, seçim değişmedi; rapor mevcut `rapor` komutuyla üretildi.

## YENİDEN ÜRETİM

- Bağımsız kod (ES_YENIDEN fonksiyonları kullanılmadan, düz pandas; ham V_ABD / V_BIST'ten R, T1, PİYASA, T2 yeniden):
- Ç191 Y6 ABD 2016-22 (geçerli bar R15, fiyattan): bağımsız n 867, ay 73, TOPLAM -1,0416, ZAMANLAMA -1,3586, SEÇİM +0,3170; ES_YENIDEN aynı (birebir).
- Ç99 alım BIST 2024-26 (FI_OLCUT r60, R dosyadan): bağımsız n 418, ay 29, TOPLAM -3,2964, ZAMANLAMA +0,0746, SEÇİM -3,3710; ES_YENIDEN aynı (birebir).
- Giriş kuralı sağlaması (ön kayıt 3. bölüm): seçilen 8 kaydın dosya R'si aynı kural ve veriden fiyattan R ile 497-500 / 500 birebir (Ç191'de R dosyada yok, fiyattan).

## UYARILAR

- AYNI VERİDE YENİDEN OKUMA: bu kayıtların verisi ve sonuçları daha önce görülmüştü; kör değil. Hiçbir satır iz değildir.
- YAŞAYAN EVREN: V_* bugün işlem gören hisseler (yukarı yanlı); geniş evren V_*2 batanları kısmen içerir.
- ZAMANLAMA yığılma uyarısı: olaylar belli piyasa dönemlerine yığılırsa ZAMANLAMA o dönemlerin piyasasıdır; bu yüzden ay kümeli aralık ve ay >= 12 şartı. Kısa hücrelerde (2023, 2024 blok = 12 ay) aralıklar geniş.
- TOPLAM / SEÇİM tabanı: T1 hissenin dönemdeki BÜTÜN günleridir (iş tanımı); eski kayıtların olayları likidite / fiyat / evrene giriş şartlarından geçmişti, T1 ise bu şartları taşımayan günleri de içeriyor. Kart ve Y1 kollarında SEÇİM'in ABD'de sistemli eksi çıkması (çoğu -0,3..-1,2 puan) kısmen bu farktan gelebilir; SEÇİM eksi değerleri 'kötü seçim' diye okunmamalı.
- Ç204'teki Cemal kuralı kolları (S7, Ş9, Ş10, Ş1 vb.) görsel onaydan geçmemiş dedektörlerdir: sayılar 'dedektörün bulduğu bölgeler' içindir, kalıbın sonucu değildir.
- Ç206 bir hat testidir (bilinen etki bacakları MOM / STREV / HIGH52); hükmü 'iz değil' değil 'ölçü geçmedi'.
- OKUMA (sayılar): ZAMANLAMA ADAYI 0, TOPLAM ADAYI 0, EMARE 0; 171 kolun 130'u ölçülebilir, 41'i ÖLÇÜLEMEDİ (n >= 100 hücre < 2 ya da bir hücrede ay < 12). En küçük birleşik p: ZAMANLAMA 0,187 (Ç204 DS07), TOPLAM 0,184 (Ç204 DS13); BH q hepsinde 1,0.
- OKUMA (yön): Ç204'ün düşüş sonrası (DS, Ç202 kümesi) kollarının 15'inde ZAMANLAMA bütün n >= 100 hücrelerde artı (çoğu +0,5..+2,5 puan; DS_ANA +0,07..+1,04 altı hücrede), ama her kolda en az bir hücrenin alt ucu < 0. Kart (Ç209, Ç205), ölçü sınaması (Ç206), bilanço (Ç226) kollarında ZAMANLAMA ~0 (-0,8..+0,3). Ç191 Y6 / Y8 / Y8B ABD 2016-22'de ZAMANLAMA eksi ve aralığı sıfırın altında (-1,36 [-2,32; -0,54]); Ç189 BIST 2016-22 -5,06 [-8,69; -1,04].
- OKUMA (tek hücre, karar değil): Ç189 TAM_DIP BIST 2024-26 TOPLAM +5,87 [+0,15; +12,26] (n 387, 28 ay) ama kayıt ÖLÇÜLEMEDİ (BIST 2023 9 ay); Ç204 DS_ANA AVR sınama TOPLAM +1,73 [+0,47; +3,00] (n 1.912) ama ABD / BIST hücrelerinde aralık sıfırı kesiyor.

## ÖNERİLEN DEFTER SATIRLARI

- IK_KAYIT (taslak, ana model yazar): Ç278 | 2026-11-27 | ES_YENIDEN.py | 'Eski iz değillerin aynı hisse bütün günleri tabanıyla yeniden okunması, 1. parti (8 kayıt, 171 kol: Ç209, Ç205, Ç206, Ç226, Ç204 (+Ç190-Ç202), Ç191, Ç99, Ç189)' | sonuç: ZAMANLAMA ADAYI 0, TOPLAM ADAYI 0, EMARE 0 / 130 ölçülebilir kol (BH ailesi 130; en küçük p 0,18); DS ailesinde ZAMANLAMA yönü artı ama aralık sıfırı kesiyor; eski E hükümleri bu tabanla da değişmedi | çıktı arastirma_cikti/goz_tespit/ES_YENIDEN_RAPOR.md, es_yeniden_ozet.json; satırlar /root/.kasa/ham/es_yeniden/.
- IK_GOREV (taslak): 27 Kas | ES_YENIDEN 1. parti | 8 kayıt yeniden okundu, aday yok; kod 05924aa / 165ad20, ön kayıt bc32ed7, ölçüm 19:50-19:52 UTC; test 13 / 13; iki hücre bağımsız birebir.
- IK_ILERI (taslak): Ç204 DS ailesi ZAMANLAMA (aynı komut, aynı eşik: n >= 100 hücrelerin hepsinde GA alt > 0, ay >= 12, BH q 0,10) | veri kesiği 2026-08-31 | sonraki test: kriz sonrası 2027 ilk yarı verisi geldiğinde (Mart 2027) yalnız yeni dönem hücresiyle.
- IK_HATA (taslak): (a) 27 Kas | ES_YENIDEN | Ç189 giriş kuralı FI_OLCUT sanıldı, gerçekte ORTAK_CETVEL (geçerli bar takvimi) | tür kurgu | bulan: giriş kuralı sağlaması | etki yok (ön kayıttan önce düzeltildi) | ders: kayıt R'si fiyattan birebir sağlanmadan kural kilitlenmez. (b) 27 Kas | ES_OLCUT_ENVANTER | Ç72 / Ç146 kapalı küme işareti eksik | tür süreç | etki yok (atlandı). (c) 27 Kas | ES_YENIDEN_IS_TANIMI | 'olay sayısı' sırası envanterde 'dosya satırı' | tür ifade.
- Sonraki parti için öneri (ana model kararı): Liste 2a'daki 17 kayıt (IK_SINYAL + V_BIST / KAP'tan üretilebilir) çoğu kapalı konu; açık kalanlar için aynı ES_YENIDEN okuyucusu eklenebilir. T1'in uygunluk şartlı sürümü (yalnız kaydın evren şartını geçen günler) ayrı ön kayıtla denenebilir (TOPLAM / SEÇİM tabanı uyarısı).

## TABLO: kayıt x kol x hücre

n / ay = ölçülen olay / ayrı ay; değerler yüzde puan ort [GA]; eski fark = dosyanın eşli fark sütunu ortalaması (varsa).

### Ç209 — KART TUR 2 (geniş tezgâh, KASA 2): 14 kart (H 15, gecerli; eski: ÖLÇÜLEMEDİ (KART TUR 2; 12 kart) / açık veride kartların FARK'ı ~0)

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| KT00 | ABD acik_d1 | 7664 / 83 | -1.67 [-2.95; -0.42] | -0.49 [-1.37; +0.36] | -1.19 [-1.87; -0.50] | +0.12 | YOK | YOK |
| KT00 | ABD acik_d2 | 13559 / 96 | -1.15 [-2.44; +0.06] | -0.41 [-1.49; +0.64] | -0.74 [-1.32; -0.18] | +0.07 | YOK | YOK |
| KT00 | ABD acik_d3 | 21627 / 96 | -1.60 [-3.30; -0.00] | -0.46 [-1.83; +0.85] | -1.14 [-1.90; -0.41] | +0.18 | YOK | YOK |
| KT00 | ABD blok | 3388 / 12 | -3.69 [-7.41; -0.25] | -0.81 [-3.18; +1.54] | -2.88 [-4.73; -1.26] | +0.42 | YOK | YOK |
| KT00 | AVR acik_d1 | 1765 / 84 | -0.91 [-2.06; +0.21] | -0.24 [-1.23; +0.70] | -0.67 [-1.21; -0.11] | +0.30 | YOK | YOK |
| KT00 | AVR acik_d2 | 2871 / 96 | -0.39 [-1.42; +0.65] | -0.32 [-1.28; +0.62] | -0.07 [-0.59; +0.47] | +0.45 | YOK | YOK |
| KT00 | AVR acik_d3 | 3888 / 96 | -0.53 [-1.49; +0.28] | +0.06 [-0.92; +0.89] | -0.59 [-1.13; -0.09] | -0.09 | YOK | YOK |
| KT00 | AVR blok | 543 / 12 | -1.45 [-3.07; +0.22] | -0.75 [-1.79; +0.49] | -0.70 [-1.82; +0.35] | +0.84 | YOK | YOK |
| KT01 | ABD acik_d1 | 11025 / 84 | -0.60 [-1.21; -0.01] | +0.03 [-0.69; +0.70] | -0.63 [-0.92; -0.35] | -0.11 | YOK | YOK |
| KT01 | ABD acik_d2 | 18253 / 94 | -0.31 [-0.99; +0.35] | +0.07 [-0.72; +0.79] | -0.38 [-0.58; -0.16] | +0.03 | YOK | YOK |
| KT01 | ABD acik_d3 | 27210 / 95 | -0.94 [-1.61; -0.28] | -0.19 [-1.11; +0.75] | -0.75 [-1.36; -0.26] | -0.23 | YOK | YOK |
| KT01 | ABD blok | 4216 / 12 | -0.62 [-1.30; -0.01] | -0.34 [-1.32; +0.68] | -0.28 [-1.04; +0.58] | -0.00 | YOK | YOK |
| KT01 | AVR acik_d1 | 2464 / 84 | -0.08 [-0.72; +0.47] | +0.21 [-0.37; +0.71] | -0.29 [-0.61; -0.01] | +0.13 | YOK | YOK |
| KT01 | AVR acik_d2 | 4046 / 94 | -0.39 [-1.21; +0.38] | -0.08 [-0.79; +0.61] | -0.31 [-0.58; -0.05] | -0.06 | YOK | YOK |
| KT01 | AVR acik_d3 | 5088 / 95 | -0.37 [-0.90; +0.12] | -0.20 [-0.72; +0.28] | -0.17 [-0.37; +0.04] | -0.02 | YOK | YOK |
| KT01 | AVR blok | 617 / 12 | -0.57 [-1.51; +0.31] | -0.13 [-0.89; +0.57] | -0.44 [-0.89; +0.00] | +0.03 | YOK | YOK |
| KT02 | ABD acik_d1 | 425 / 73 | -0.42 [-2.10; +1.19] | +0.50 [-0.52; +1.43] | -0.92 [-2.05; +0.22] | -0.60 | YOK | YOK |
| KT02 | ABD acik_d2 | 599 / 86 | +0.20 [-1.36; +1.67] | +0.10 [-0.94; +1.05] | +0.10 [-0.79; +0.96] | -0.05 | YOK | YOK |
| KT02 | ABD acik_d3 | 1533 / 92 | -0.75 [-2.56; +0.81] | +0.09 [-1.28; +1.47] | -0.84 [-1.70; -0.09] | -0.89 | YOK | YOK |
| KT02 | ABD blok | 202 / 12 | +1.61 [-0.41; +4.02] | -0.57 [-1.76; +0.64] | +2.19 [+0.51; +3.75] | +0.97 | YOK | YOK |
| KT02 | AVR acik_d1 | 32 / 22 | -1.16 [-3.95; +1.24] | -0.21 [-1.62; +0.98] | -0.95 [-3.08; +0.83] | -1.33 | YOK | YOK |
| KT02 | AVR acik_d2 | 87 / 41 | -0.41 [-5.24; +4.00] | -0.58 [-2.88; +1.79] | +0.16 [-2.74; +2.99] | -1.00 | YOK | YOK |
| KT02 | AVR acik_d3 | 103 / 46 | +1.02 [-0.71; +2.61] | +0.05 [-1.23; +1.30] | +0.98 [-0.61; +2.49] | +1.12 | YOK | YOK |
| KT02 | AVR blok | 15 / 7 | +0.68 [-1.62; +3.43] | +0.22 [-0.77; +1.05] | +0.46 [-1.82; +3.13] | -1.23 | YOK | YOK |
| KT03 | ABD acik_d1 | 9586 / 84 | -0.56 [-1.20; +0.03] | +0.02 [-0.69; +0.69] | -0.58 [-0.87; -0.30] | -0.05 | YOK | YOK |
| KT03 | ABD acik_d2 | 15733 / 94 | -0.30 [-1.00; +0.37] | +0.09 [-0.68; +0.83] | -0.39 [-0.61; -0.17] | +0.01 | YOK | YOK |
| KT03 | ABD acik_d3 | 23898 / 95 | -0.95 [-1.63; -0.27] | -0.17 [-1.10; +0.77] | -0.78 [-1.40; -0.30] | -0.24 | YOK | YOK |
| KT03 | ABD blok | 3742 / 12 | -0.62 [-1.30; -0.00] | -0.37 [-1.37; +0.65] | -0.25 [-1.03; +0.64] | +0.08 | YOK | YOK |
| KT03 | AVR acik_d1 | 2168 / 84 | -0.04 [-0.67; +0.53] | +0.26 [-0.33; +0.76] | -0.30 [-0.65; +0.02] | +0.14 | YOK | YOK |
| KT03 | AVR acik_d2 | 3542 / 93 | -0.57 [-1.36; +0.20] | -0.14 [-0.83; +0.56] | -0.42 [-0.71; -0.17] | -0.12 | YOK | YOK |
| KT03 | AVR acik_d3 | 4415 / 95 | -0.31 [-0.85; +0.19] | -0.19 [-0.70; +0.29] | -0.12 [-0.35; +0.11] | +0.03 | YOK | YOK |
| KT03 | AVR blok | 547 / 12 | -0.79 [-1.73; +0.05] | -0.16 [-0.92; +0.55] | -0.63 [-1.03; -0.25] | -0.19 | YOK | YOK |
| KT04 | ABD acik_d1 | 5454 / 84 | -0.59 [-1.25; +0.04] | +0.01 [-0.72; +0.72] | -0.60 [-0.94; -0.26] | -0.06 | YOK | YOK |
| KT04 | ABD acik_d2 | 7052 / 93 | -0.33 [-1.09; +0.36] | +0.08 [-0.70; +0.80] | -0.41 [-0.62; -0.19] | -0.02 | YOK | YOK |
| KT04 | ABD acik_d3 | 12321 / 95 | -1.05 [-1.77; -0.31] | -0.38 [-1.38; +0.65] | -0.67 [-1.32; -0.16] | -0.21 | YOK | YOK |
| KT04 | ABD blok | 2091 / 12 | -0.70 [-1.58; +0.03] | -0.53 [-1.51; +0.55] | -0.17 [-0.96; +0.69] | +0.07 | YOK | YOK |
| KT04 | AVR acik_d1 | 995 / 81 | -0.27 [-0.91; +0.30] | +0.12 [-0.51; +0.64] | -0.40 [-0.79; +0.00] | -0.11 | YOK | YOK |
| KT04 | AVR acik_d2 | 1809 / 93 | -0.36 [-1.25; +0.54] | +0.04 [-0.74; +0.83] | -0.41 [-0.74; -0.08] | -0.13 | YOK | YOK |
| KT04 | AVR acik_d3 | 2513 / 93 | -0.38 [-0.97; +0.18] | -0.31 [-0.87; +0.19] | -0.07 [-0.39; +0.26] | -0.01 | YOK | YOK |
| KT04 | AVR blok | 358 / 12 | -0.34 [-1.32; +0.57] | -0.16 [-0.94; +0.59] | -0.18 [-0.90; +0.42] | +0.07 | YOK | YOK |
| KT05 | ABD acik_d1 | 10365 / 84 | -0.63 [-1.27; -0.03] | +0.04 [-0.69; +0.73] | -0.67 [-0.96; -0.39] | -0.13 | YOK | YOK |
| KT05 | ABD acik_d2 | 17317 / 94 | -0.27 [-0.97; +0.40] | +0.12 [-0.67; +0.85] | -0.39 [-0.59; -0.17] | +0.03 | YOK | YOK |
| KT05 | ABD acik_d3 | 26094 / 95 | -0.98 [-1.65; -0.32] | -0.20 [-1.14; +0.76] | -0.78 [-1.41; -0.29] | -0.25 | YOK | YOK |
| KT05 | ABD blok | 4045 / 12 | -0.62 [-1.30; +0.00] | -0.34 [-1.32; +0.67] | -0.28 [-1.06; +0.62] | +0.03 | YOK | YOK |
| KT05 | AVR acik_d1 | 2294 / 84 | -0.07 [-0.73; +0.51] | +0.24 [-0.34; +0.74] | -0.30 [-0.64; -0.01] | +0.12 | YOK | YOK |
| KT05 | AVR acik_d2 | 3797 / 94 | -0.39 [-1.21; +0.41] | -0.05 [-0.75; +0.66] | -0.34 [-0.62; -0.08] | -0.08 | YOK | YOK |
| KT05 | AVR acik_d3 | 4751 / 94 | -0.39 [-0.93; +0.10] | -0.21 [-0.75; +0.26] | -0.18 [-0.39; +0.04] | +0.00 | YOK | YOK |
| KT05 | AVR blok | 553 / 12 | -0.53 [-1.55; +0.42] | -0.14 [-0.93; +0.56] | -0.39 [-0.88; +0.10] | +0.14 | YOK | YOK |
| KT06 | ABD acik_d1 | 6973 / 84 | -0.69 [-1.33; -0.11] | +0.10 [-0.64; +0.81] | -0.79 [-1.10; -0.49] | -0.21 | YOK | YOK |
| KT06 | ABD acik_d2 | 10806 / 94 | -0.45 [-1.12; +0.17] | -0.00 [-0.76; +0.69] | -0.45 [-0.67; -0.21] | -0.03 | YOK | YOK |
| KT06 | ABD acik_d3 | 15427 / 95 | -0.95 [-1.60; -0.28] | -0.31 [-1.21; +0.59] | -0.63 [-1.22; -0.17] | -0.17 | YOK | YOK |
| KT06 | ABD blok | 2206 / 12 | -1.04 [-1.85; -0.30] | -0.57 [-1.75; +0.62] | -0.47 [-1.30; +0.50] | -0.30 | YOK | YOK |
| KT06 | AVR acik_d1 | 1546 / 81 | -0.06 [-0.69; +0.47] | +0.24 [-0.38; +0.76] | -0.30 [-0.69; +0.04] | +0.14 | YOK | YOK |
| KT06 | AVR acik_d2 | 2523 / 93 | -0.25 [-1.07; +0.55] | -0.06 [-0.75; +0.63] | -0.18 [-0.49; +0.11] | +0.01 | YOK | YOK |
| KT06 | AVR acik_d3 | 3142 / 94 | -0.42 [-1.00; +0.12] | -0.19 [-0.70; +0.29] | -0.23 [-0.52; +0.04] | -0.06 | YOK | YOK |
| KT06 | AVR blok | 380 / 12 | -0.06 [-1.15; +0.96] | -0.04 [-0.83; +0.67] | -0.03 [-0.47; +0.50] | +0.51 | YOK | YOK |
| KT07 | ABD acik_d1 | 188 / 61 | +0.30 [-1.46; +1.92] | +0.55 [-0.60; +1.59] | -0.25 [-1.59; +1.07] | -0.23 | YOK | YOK |
| KT07 | ABD acik_d2 | 228 / 70 | +0.40 [-1.31; +2.09] | +0.33 [-0.64; +1.22] | +0.07 [-1.26; +1.44] | -0.31 | YOK | YOK |
| KT07 | ABD acik_d3 | 661 / 86 | -0.69 [-2.49; +0.93] | +0.01 [-1.31; +1.30] | -0.70 [-1.62; +0.19] | -1.10 | YOK | YOK |
| KT07 | ABD blok | 91 / 11 | +0.48 [-2.07; +2.70] | -0.61 [-1.47; +0.48] | +1.09 [-1.27; +3.15] | +1.11 | YOK | YOK |
| KT07 | AVR acik_d1 | 7 / 7 | -1.13 [-7.15; +3.55] | -0.39 [-3.03; +1.90] | -0.74 [-7.65; +4.18] | -1.29 | YOK | YOK |
| KT07 | AVR acik_d2 | 32 / 21 | +1.77 [-4.82; +7.93] | +0.22 [-2.22; +2.62] | +1.55 [-2.88; +5.72] | +0.51 | YOK | YOK |
| KT07 | AVR acik_d3 | 46 / 30 | +0.81 [-2.15; +3.66] | -0.23 [-1.64; +1.08] | +1.04 [-1.63; +3.47] | +0.87 | YOK | YOK |
| KT07 | AVR blok | 9 / 6 | +2.92 [+0.14; +5.68] | -0.06 [-0.91; +0.88] | +2.98 [-0.37; +6.16] | +1.46 | YOK | YOK |
| KT08 | ABD acik_d1 | 3875 / 84 | +0.25 [-1.73; +2.50] | -0.53 [-1.62; +0.77] | +0.78 [-0.32; +1.87] | +0.40 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | ABD acik_d2 | 8787 / 96 | +0.78 [-2.34; +4.05] | -0.07 [-2.54; +2.54] | +0.85 [+0.04; +1.72] | +0.28 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | ABD acik_d3 | 17559 / 96 | -0.71 [-2.63; +1.30] | -0.58 [-2.09; +1.00] | -0.13 [-0.78; +0.53] | -0.03 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | ABD blok | 1913 / 12 | +3.62 [+1.09; +6.38] | +1.10 [-0.11; +2.30] | +2.52 [-0.27; +6.10] | +0.70 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | AVR acik_d1 | 787 / 59 | +0.19 [-2.41; +3.17] | -0.87 [-2.47; +1.03] | +1.06 [-0.10; +2.38] | +0.50 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | AVR acik_d2 | 1660 / 89 | +0.02 [-3.02; +3.59] | -0.93 [-3.26; +1.86] | +0.95 [-0.12; +2.04] | +0.39 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | AVR acik_d3 | 1926 / 92 | +0.85 [-1.08; +3.34] | -0.02 [-1.42; +1.75] | +0.87 [+0.17; +1.67] | +0.26 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | AVR blok | 158 / 11 | +1.82 [-0.06; +3.51] | +0.61 [-0.21; +1.41] | +1.20 [-0.43; +2.55] | -0.63 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT09 | ABD acik_d1 | 140 / 37 | -1.74 [-7.77; +5.86] | -0.40 [-1.86; +1.36] | -1.34 [-6.40; +5.17] | -0.29 | YOK | YOK |
| KT09 | ABD acik_d2 | 246 / 54 | +3.32 [-6.10; +13.91] | +0.50 [-3.89; +4.96] | +2.82 [-2.92; +8.94] | +1.71 | YOK | YOK |
| KT09 | ABD acik_d3 | 968 / 83 | -0.27 [-5.04; +4.43] | -0.81 [-2.61; +1.35] | +0.54 [-2.73; +3.64] | +0.66 | YOK | YOK |
| KT09 | ABD blok | 94 / 12 | -0.69 [-4.66; +3.45] | -0.12 [-1.22; +0.95] | -0.57 [-4.02; +3.30] | -2.74 | YOK | YOK |
| KT09 | AVR acik_d1 | 17 / 12 | +2.63 [-10.17; +15.62] | +0.42 [-3.34; +3.99] | +2.22 [-7.80; +12.56] | +2.50 | YOK | YOK |
| KT09 | AVR acik_d2 | 21 / 8 | +2.34 [-10.64; +19.70] | +0.58 [-5.41; +7.78] | +1.76 [-5.90; +13.42] | +2.88 | YOK | YOK |
| KT09 | AVR acik_d3 | 20 / 16 | +3.96 [-10.25; +22.07] | +2.10 [+0.05; +4.33] | +1.86 [-11.48; +18.43] | -0.69 | YOK | YOK |
| KT10 | ABD acik_d1 | 7223 / 84 | -0.63 [-1.34; +0.13] | -0.05 [-0.79; +0.67] | -0.58 [-1.02; -0.12] | -0.07 | YOK | YOK |
| KT10 | ABD acik_d2 | 11086 / 96 | -0.66 [-1.75; +0.35] | -0.15 [-1.45; +1.06] | -0.51 [-0.98; -0.03] | +0.11 | YOK | YOK |
| KT10 | ABD acik_d3 | 24899 / 96 | -1.30 [-2.35; -0.25] | -0.17 [-1.39; +1.12] | -1.13 [-1.63; -0.65] | +0.08 | YOK | YOK |
| KT10 | ABD blok | 5413 / 12 | -1.30 [-3.02; +0.08] | -0.22 [-1.40; +0.79] | -1.08 [-1.85; -0.46] | +0.47 | YOK | YOK |
| KT11 | ABD acik_d1 | 582 / 76 | -0.84 [-1.94; +0.17] | -0.19 [-1.13; +0.77] | -0.65 [-1.37; +0.02] | -0.37 | YOK | YOK |
| KT11 | ABD acik_d2 | 943 / 88 | +0.38 [-0.80; +1.52] | +0.23 [-0.77; +1.13] | +0.15 [-0.44; +0.82] | +0.53 | YOK | YOK |
| KT11 | ABD acik_d3 | 1545 / 90 | -0.37 [-1.27; +0.50] | -0.69 [-1.90; +0.38] | +0.32 [-0.38; +1.09] | +0.17 | YOK | YOK |
| KT11 | ABD blok | 242 / 12 | -0.14 [-1.12; +1.77] | -2.02 [-2.98; +0.07] | +1.88 [+0.12; +2.91] | +0.98 | YOK | YOK |
| KT11 | AVR acik_d1 | 127 / 53 | +0.15 [-1.35; +1.52] | -0.25 [-1.31; +0.69] | +0.40 [-0.56; +1.36] | +0.99 | YOK | YOK |
| KT11 | AVR acik_d2 | 216 / 64 | +0.98 [-0.22; +2.04] | +0.57 [-0.42; +1.50] | +0.41 [-0.21; +0.99] | +0.45 | YOK | YOK |
| KT11 | AVR acik_d3 | 271 / 76 | +0.91 [-0.11; +1.93] | -0.07 [-0.84; +0.66] | +0.97 [+0.03; +1.99] | +1.14 | YOK | YOK |
| KT11 | AVR blok | 43 / 11 | +0.40 [-1.50; +1.82] | -0.27 [-1.03; +0.44] | +0.67 [-0.99; +2.09] | +0.71 | YOK | YOK |
| KT12 | ABD acik_d1 | 860 / 83 | -0.79 [-1.82; +0.11] | +0.14 [-0.69; +0.86] | -0.93 [-1.53; -0.23] | -0.46 | YOK | YOK |
| KT12 | ABD acik_d2 | 1373 / 91 | -0.21 [-1.10; +0.75] | -0.19 [-1.02; +0.62] | -0.02 [-0.53; +0.50] | +0.33 | YOK | YOK |
| KT12 | ABD acik_d3 | 2567 / 94 | -0.42 [-1.46; +0.60] | -0.29 [-1.39; +0.82] | -0.13 [-0.70; +0.49] | -0.16 | YOK | YOK |
| KT12 | ABD blok | 420 / 12 | -0.45 [-1.39; +0.75] | -1.14 [-2.20; +0.21] | +0.69 [-0.29; +1.46] | -0.10 | YOK | YOK |
| KT12 | AVR acik_d1 | 160 / 61 | +0.61 [-0.43; +1.69] | +0.00 [-0.81; +0.77] | +0.61 [-0.20; +1.50] | +0.48 | YOK | YOK |
| KT12 | AVR acik_d2 | 272 / 77 | -1.32 [-2.76; -0.10] | -0.23 [-1.13; +0.64] | -1.10 [-2.23; -0.08] | -1.16 | YOK | YOK |
| KT12 | AVR acik_d3 | 417 / 87 | +0.45 [-0.31; +1.19] | -0.28 [-0.99; +0.42] | +0.74 [+0.02; +1.43] | +0.69 | YOK | YOK |
| KT12 | AVR blok | 56 / 12 | -0.15 [-2.03; +1.79] | +0.15 [-0.63; +0.84] | -0.30 [-1.75; +1.33] | -0.84 | YOK | YOK |
| KT13 | ABD acik_d1 | 7799 / 84 | -0.55 [-1.96; +0.86] | -0.41 [-1.26; +0.43] | -0.13 [-0.84; +0.64] | +0.40 | YOK | YOK |
| KT13 | ABD acik_d2 | 13728 / 96 | -0.47 [-2.00; +0.96] | -0.41 [-1.49; +0.63] | -0.06 [-0.65; +0.51] | +0.18 | YOK | YOK |
| KT13 | ABD acik_d3 | 22211 / 96 | -1.17 [-3.11; +0.71] | -0.48 [-1.86; +0.84] | -0.69 [-1.42; +0.00] | +0.02 | YOK | YOK |
| KT13 | ABD blok | 3429 / 12 | -1.02 [-5.16; +3.67] | -0.81 [-3.18; +1.54] | -0.21 [-2.37; +2.60] | -0.28 | YOK | YOK |
| KT13 | AVR acik_d1 | 1766 / 84 | -0.54 [-1.90; +0.86] | -0.24 [-1.20; +0.71] | -0.31 [-0.96; +0.47] | +0.11 | YOK | YOK |
| KT13 | AVR acik_d2 | 2808 / 96 | -0.38 [-1.82; +1.01] | -0.31 [-1.28; +0.62] | -0.07 [-0.68; +0.51] | -0.71 | YOK | YOK |
| KT13 | AVR acik_d3 | 3834 / 96 | +0.04 [-1.42; +1.29] | +0.07 [-0.91; +0.89] | -0.03 [-0.58; +0.49] | -0.05 | YOK | YOK |
| KT13 | AVR blok | 535 / 12 | -1.12 [-2.55; +0.36] | -0.75 [-1.79; +0.49] | -0.36 [-1.07; +0.41] | -1.25 | YOK | YOK |

### Ç205 — KART TUR 1 (KASA yürüyen ileri test): 11 kart (H 15, gecerli; eski: ÖLÇÜLEMEDİ (KART TUR 1; hiçbir kart tutmadı))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| KT00 | ABD acik | 6718 / 79 | -1.85 [-3.63; -0.05] | -0.50 [-2.13; +1.18] | -1.35 [-2.51; -0.28] | +0.40 | YOK | YOK |
| KT00 | ABD birikimli | 1290 / 12 | -2.17 [-6.49; +2.18] | -0.02 [-3.59; +3.66] | -2.16 [-3.79; -0.51] | +0.70 | YOK | YOK |
| KT00 | AVR acik | 3452 / 84 | -0.51 [-1.53; +0.42] | +0.05 [-0.97; +0.98] | -0.57 [-1.13; -0.04] | +0.07 | YOK | YOK |
| KT00 | AVR birikimli | 548 / 12 | -1.60 [-3.77; +0.45] | +0.17 [-2.24; +2.65] | -1.76 [-2.95; -0.63] | -0.46 | YOK | YOK |
| KT01 | ABD acik | 8686 / 77 | -1.01 [-1.74; -0.29] | -0.34 [-1.54; +0.97] | -0.66 [-1.65; +0.06] | -0.18 | YOK | YOK |
| KT01 | ABD birikimli | 1848 / 12 | -0.47 [-2.77; +1.66] | +0.27 [-2.46; +2.71] | -0.74 [-1.18; -0.20] | -0.02 | YOK | YOK |
| KT01 | AVR acik | 4496 / 83 | -0.35 [-0.83; +0.09] | -0.18 [-0.69; +0.30] | -0.17 [-0.40; +0.07] | -0.03 | YOK | YOK |
| KT01 | AVR birikimli | 738 / 12 | -0.73 [-2.43; +1.13] | -0.36 [-1.84; +1.25] | -0.37 [-0.77; +0.03] | -0.17 | YOK | YOK |
| KT02 | ABD acik | 346 / 64 | +0.58 [-2.13; +2.75] | +0.54 [-1.82; +2.65] | +0.04 [-1.22; +1.30] | -0.15 | YOK | YOK |
| KT02 | ABD birikimli | 138 / 12 | +3.28 [-0.06; +5.99] | +1.63 [-0.73; +3.75] | +1.65 [-0.01; +2.86] | -0.03 | YOK | YOK |
| KT02 | AVR acik | 89 / 37 | +0.31 [-1.66; +2.01] | +0.08 [-1.49; +1.62] | +0.23 [-1.31; +1.86] | +0.49 | YOK | YOK |
| KT02 | AVR birikimli | 19 / 9 | +5.18 [-0.66; +8.55] | +0.43 [-1.48; +1.72] | +4.75 [-0.64; +8.26] | +4.59 | YOK | YOK |
| KT03 | ABD acik | 7614 / 77 | -1.06 [-1.79; -0.35] | -0.33 [-1.50; +0.95] | -0.74 [-1.68; -0.04] | -0.21 | YOK | YOK |
| KT03 | ABD birikimli | 1612 / 12 | -0.41 [-2.81; +1.77] | +0.31 [-2.47; +2.77] | -0.71 [-1.16; -0.17] | -0.02 | YOK | YOK |
| KT03 | AVR acik | 3910 / 83 | -0.31 [-0.76; +0.13] | -0.18 [-0.69; +0.29] | -0.13 [-0.37; +0.13] | +0.01 | YOK | YOK |
| KT03 | AVR birikimli | 630 / 12 | -0.57 [-2.49; +1.47] | -0.33 [-1.87; +1.32] | -0.25 [-0.85; +0.26] | -0.05 | YOK | YOK |
| KT04 | ABD acik | 3823 / 77 | -1.22 [-2.15; -0.36] | -0.57 [-1.92; +0.88] | -0.64 [-1.69; +0.19] | -0.21 | YOK | YOK |
| KT04 | ABD birikimli | 922 / 12 | -1.20 [-3.41; +1.07] | -0.41 [-2.97; +2.14] | -0.79 [-1.49; -0.12] | -0.19 | YOK | YOK |
| KT04 | AVR acik | 2208 / 80 | -0.40 [-0.97; +0.13] | -0.30 [-0.83; +0.21] | -0.10 [-0.48; +0.27] | -0.05 | YOK | YOK |
| KT04 | AVR birikimli | 381 / 12 | -0.52 [-2.50; +1.37] | -0.32 [-1.82; +1.28] | -0.21 [-0.97; +0.41] | -0.10 | YOK | YOK |
| KT05 | ABD acik | 8245 / 77 | -1.07 [-1.79; -0.37] | -0.37 [-1.58; +0.98] | -0.70 [-1.73; +0.04] | -0.20 | YOK | YOK |
| KT05 | ABD birikimli | 1815 / 12 | -0.59 [-2.88; +1.49] | +0.21 [-2.52; +2.65] | -0.80 [-1.29; -0.23] | -0.07 | YOK | YOK |
| KT05 | AVR acik | 4160 / 82 | -0.38 [-0.89; +0.08] | -0.19 [-0.71; +0.29] | -0.19 [-0.44; +0.04] | -0.01 | YOK | YOK |
| KT05 | AVR birikimli | 720 / 12 | -0.82 [-2.52; +1.07] | -0.40 [-1.86; +1.19] | -0.41 [-0.83; -0.01] | -0.21 | YOK | YOK |
| KT06 | ABD acik | 4953 / 77 | -0.93 [-1.63; -0.22] | -0.54 [-1.61; +0.56] | -0.39 [-1.10; +0.24] | -0.02 | YOK | YOK |
| KT06 | ABD birikimli | 1006 / 12 | -0.20 [-2.41; +1.78] | +0.31 [-2.29; +2.66] | -0.51 [-1.00; +0.09] | +0.14 | YOK | YOK |
| KT06 | AVR acik | 2801 / 82 | -0.38 [-0.97; +0.10] | -0.18 [-0.71; +0.29] | -0.20 [-0.51; +0.09] | -0.03 | YOK | YOK |
| KT06 | AVR birikimli | 440 / 12 | -1.04 [-2.83; +0.99] | -0.39 [-1.92; +1.31] | -0.65 [-1.14; -0.19] | -0.44 | YOK | YOK |
| KT07 | ABD acik | 151 / 46 | +0.84 [-1.92; +2.95] | +0.59 [-1.83; +2.44] | +0.25 [-1.28; +1.89] | -0.45 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT07 | ABD birikimli | 52 / 10 | +3.40 [-1.11; +7.09] | +2.32 [+0.08; +4.27] | +1.08 [-1.90; +3.60] | -1.72 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT07 | AVR acik | 36 / 24 | -0.04 [-3.36; +2.93] | -0.22 [-1.70; +1.15] | +0.18 [-2.56; +2.86] | +0.36 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT07 | AVR birikimli | 12 / 7 | +3.91 [-3.22; +9.04] | +0.74 [-0.60; +2.18] | +3.17 [-3.18; +7.76] | +2.68 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT08 | ABD acik | 4836 / 84 | -0.50 [-2.80; +2.17] | -0.20 [-2.15; +2.12] | -0.30 [-1.52; +0.85] | +0.05 | YOK | YOK |
| KT08 | ABD birikimli | 774 / 12 | +2.19 [-1.17; +5.45] | +0.50 [-1.90; +2.64] | +1.69 [+0.35; +3.05] | -0.07 | YOK | YOK |
| KT08 | AVR acik | 1838 / 81 | +0.85 [-1.20; +3.53] | -0.06 [-1.51; +1.86] | +0.91 [+0.15; +1.83] | +0.29 | YOK | YOK |
| KT08 | AVR birikimli | 182 / 12 | +3.61 [+0.73; +5.70] | +0.86 [-0.90; +1.99] | +2.75 [+1.15; +4.51] | +0.59 | YOK | YOK |
| KT09 | ABD acik | 167 / 39 | +4.02 [-6.33; +13.73] | +0.34 [-4.03; +5.13] | +3.68 [-3.51; +9.44] | +4.70 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT09 | ABD birikimli | 22 / 10 | -0.28 [-13.28; +15.40] | +0.11 [-3.20; +3.65] | -0.38 [-11.10; +12.13] | -0.37 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT09 | AVR acik | 20 / 15 | +9.10 [-6.25; +27.09] | +2.10 [-0.45; +4.51] | +7.00 [-7.07; +24.09] | +3.68 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT09 | AVR birikimli | 3 / 3 | +9.17 [-13.62; +32.53] | +2.86 [+1.11; +4.78] | +6.31 [-18.40; +31.43] | -0.35 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| KT10 | ABD acik | 18014 / 84 | -1.16 [-2.26; -0.16] | -0.01 [-1.45; +1.69] | -1.15 [-2.18; -0.47] | -0.02 | YOK | YOK |
| KT10 | ABD birikimli | 3343 / 12 | -1.88 [-4.08; +0.36] | -0.84 [-3.21; +1.57] | -1.03 [-1.53; -0.57] | -0.10 | YOK | YOK |

### Ç206 — ÖLÇÜ SINAMASI: bilinen etki bacakları (MOM, STREV, HIGH52) (H 15, gecerli; eski: HİÇBİR ÖLÇÜ GEÇMEDİ 0 / 36 (hat testi))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| HIGH52+ | ABD d1 | 3318 / 43 | -0.52 [-1.54; +0.39] | -0.25 [-1.67; +1.05] | -0.27 [-0.90; +0.36] | -0.17 | YOK | YOK |
| HIGH52+ | ABD d2 | 4656 / 48 | -1.60 [-3.25; -0.08] | -0.59 [-2.96; +1.88] | -1.01 [-2.63; +0.37] | -0.03 | YOK | YOK |
| HIGH52+ | AVR d1 | 1940 / 48 | -0.58 [-1.12; -0.08] | -0.01 [-0.78; +0.72] | -0.57 [-1.04; -0.12] | -0.43 | YOK | YOK |
| HIGH52+ | AVR d2 | 2058 / 48 | +0.19 [-1.13; +1.29] | +0.15 [-1.61; +1.69] | +0.04 [-0.81; +0.87] | +0.43 | YOK | YOK |
| MOM+ | ABD d1 | 3316 / 43 | -0.76 [-2.73; +0.98] | -0.25 [-1.67; +1.05] | -0.52 [-1.49; +0.39] | +0.22 | YOK | YOK |
| MOM+ | ABD d2 | 4655 / 48 | -3.70 [-6.46; -0.90] | -0.59 [-2.96; +1.89] | -3.11 [-4.75; -1.51] | +0.64 | YOK | YOK |
| MOM+ | AVR d1 | 1940 / 48 | -0.82 [-1.75; +0.03] | -0.01 [-0.79; +0.73] | -0.81 [-1.38; -0.25] | +0.05 | YOK | YOK |
| MOM+ | AVR d2 | 2058 / 48 | -0.61 [-2.21; +0.77] | +0.15 [-1.61; +1.69] | -0.76 [-1.59; -0.01] | -0.04 | YOK | YOK |
| MOM- | ABD d1 | 3278 / 43 | +0.99 [-0.91; +2.78] | -0.24 [-1.66; +1.05] | +1.23 [+0.48; +2.00] | +0.39 | YOK | YOK |
| MOM- | ABD d2 | 4612 / 48 | -1.13 [-4.32; +1.96] | -0.58 [-2.95; +1.90] | -0.55 [-1.99; +0.81] | -0.09 | YOK | YOK |
| MOM- | AVR d1 | 1894 / 48 | +0.98 [-0.30; +2.22] | +0.01 [-0.78; +0.75] | +0.98 [+0.23; +1.74] | +0.71 | YOK | YOK |
| MOM- | AVR d2 | 2017 / 48 | +0.57 [-2.05; +3.24] | +0.12 [-1.67; +1.67] | +0.45 [-0.73; +1.91] | +0.33 | YOK | YOK |
| STREV+ | ABD d1 | 3701 / 48 | +0.63 [-1.35; +2.35] | -0.35 [-1.77; +0.79] | +0.97 [+0.22; +1.70] | +0.69 | YOK | YOK |
| STREV+ | ABD d2 | 4748 / 48 | -2.29 [-5.47; +0.58] | -0.60 [-2.99; +1.89] | -1.68 [-3.10; -0.39] | -0.67 | YOK | YOK |
| STREV+ | AVR d1 | 1919 / 48 | +0.55 [-0.63; +1.68] | -0.01 [-0.78; +0.72] | +0.56 [-0.00; +1.13] | +0.26 | YOK | YOK |
| STREV+ | AVR d2 | 2028 / 48 | -0.22 [-2.74; +2.08] | +0.13 [-1.65; +1.68] | -0.35 [-1.29; +0.49] | -0.26 | YOK | YOK |
| STREV- | ABD d1 | 3740 / 48 | -0.60 [-2.32; +0.84] | -0.35 [-1.78; +0.79] | -0.25 [-0.91; +0.44] | -0.07 | YOK | YOK |
| STREV- | ABD d2 | 4795 / 48 | -1.72 [-4.04; +0.60] | -0.60 [-2.99; +1.89] | -1.12 [-2.29; +0.01] | +0.38 | YOK | YOK |
| STREV- | AVR d1 | 1962 / 48 | -0.35 [-1.27; +0.55] | +0.00 [-0.78; +0.74] | -0.35 [-0.83; +0.12] | +0.17 | YOK | YOK |
| STREV- | AVR d2 | 2072 / 48 | +0.27 [-1.41; +1.87] | +0.10 [-1.68; +1.65] | +0.17 [-0.42; +0.74] | +0.44 | YOK | YOK |

### Ç226 — ÜÇ İZ BİRLİKTE BİLANÇO OLAYINDA (UC_IZ2) (H 60, gecerli; eski: İZ DEĞİL (güç yeterli))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| B_var | ABD d1619 | 8342 / 48 | -0.82 [-2.69; +0.97] | +0.15 [-1.74; +1.99] | -0.97 [-1.77; -0.23] | -0.02 | YOK | YOK |
| B_var | ABD d2022 | 5588 / 34 | -5.39 [-10.26; +0.38] | -3.55 [-9.88; +4.53] | -1.83 [-5.01; +0.42] | -0.32 | YOK | YOK |
| I_var | ABD d1619 | 4176 / 48 | +1.18 [-0.98; +3.37] | +0.62 [-1.20; +2.41] | +0.57 [-0.21; +1.37] | +0.34 | YOK | YOK |
| I_var | ABD d2022 | 4038 / 34 | -0.43 [-6.49; +5.69] | +0.68 [-6.68; +8.66] | -1.11 [-4.04; +1.68] | -0.71 | YOK | YOK |
| N_ge2 | ABD d1619 | 1677 / 48 | +0.52 [-1.79; +2.58] | +0.19 [-1.67; +1.96] | +0.33 [-0.69; +1.33] | +0.80 | YOK | YOK |
| N_ge2 | ABD d2022 | 1511 / 33 | -5.05 [-10.86; +1.89] | -2.11 [-8.47; +6.05] | -2.93 [-6.83; +0.53] | +1.36 | YOK | YOK |
| R_var | ABD d1619 | 973 / 45 | -0.70 [-3.10; +1.64] | -0.45 [-2.30; +1.28] | -0.25 [-1.78; +1.13] | +1.39 | YOK | YOK |
| R_var | ABD d2022 | 1996 / 33 | -8.19 [-15.34; -0.03] | -1.15 [-7.95; +7.39] | -7.04 [-11.83; -2.64] | +1.37 | YOK | YOK |

### Ç204 — CETVEL2 R15 yeniden koşusu (Y1 tabanı + Ç194-Ç202 hipotezleri + hakem turu kolları) (H 15, gecerli; eski: İZ DEĞİL / ÖLÇÜLEMEDİ (124 hipotez; KATKI+ 0, KATKI− 0))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| C194:Y10 | ABD egitim | 31 / 18 | +1.93 [-3.84; +6.68] | +1.85 [-0.44; +3.98] | +0.08 [-5.96; +4.98] | -1.52 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10 | ABD sinama | 38 / 22 | +1.64 [-1.99; +4.87] | +1.31 [-0.08; +2.62] | +0.33 [-2.93; +3.77] | +0.15 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10 | AVR egitim | 9 / 8 | +0.89 [-4.92; +4.71] | +0.46 [-0.73; +1.51] | +0.43 [-4.49; +4.09] | +0.36 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10 | AVR sinama | 12 / 10 | +2.35 [-2.19; +8.31] | -0.06 [-1.04; +1.21] | +2.41 [-1.74; +7.53] | +2.42 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10 | BIST egitim | 40 / 21 | -0.04 [-3.81; +4.08] | -0.90 [-3.41; +1.72] | +0.87 [-2.41; +4.65] | -0.89 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10 | BIST sinama | 71 / 22 | -1.35 [-6.70; +3.09] | -0.24 [-4.58; +3.36] | -1.12 [-3.26; +1.07] | -2.40 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | ABD egitim | 8 / 8 | -1.56 [-9.17; +5.61] | +0.59 [-0.72; +1.86] | -2.15 [-10.42; +5.09] | -5.14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | ABD sinama | 12 / 10 | +1.21 [-3.75; +5.95] | +0.60 [-1.43; +2.77] | +0.61 [-3.21; +4.70] | +2.05 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | AVR egitim | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | AVR sinama | 3 / 2 | -0.68 [-4.20; +6.34] | -1.11 [-1.24; -1.05] | +0.43 [-3.15; +7.58] | -5.59 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | BIST egitim | 14 / 10 | +1.33 [-4.12; +6.94] | +0.61 [-2.71; +4.59] | +0.72 [-4.48; +5.23] | +0.02 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10b | BIST sinama | 39 / 15 | -3.45 [-10.91; +3.06] | -0.74 [-7.10; +4.70] | -2.72 [-6.58; -0.11] | -2.76 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C194:Y10c | ABD egitim | 873 / 77 | -0.93 [-1.85; -0.00] | -0.75 [-1.90; +0.37] | -0.17 [-1.06; +0.66] | -0.07 | YOK | YOK |
| C194:Y10c | ABD sinama | 749 / 44 | -0.73 [-1.73; +0.19] | -0.21 [-1.32; +0.84] | -0.52 [-1.24; +0.17] | -0.51 | YOK | YOK |
| C194:Y10c | AVR egitim | 566 / 77 | -0.44 [-1.29; +0.35] | -0.30 [-0.89; +0.21] | -0.14 [-0.72; +0.42] | +0.12 | YOK | YOK |
| C194:Y10c | AVR sinama | 363 / 43 | +0.39 [-0.50; +1.27] | +0.03 [-0.65; +0.67] | +0.36 [-0.21; +0.90] | +0.66 | YOK | YOK |
| C194:Y10c | BIST egitim | 486 / 70 | -0.32 [-2.13; +1.24] | +1.26 [-0.38; +2.73] | -1.58 [-2.54; -0.72] | -1.62 | YOK | YOK |
| C194:Y10c | BIST sinama | 432 / 42 | -0.42 [-3.49; +2.58] | +0.24 [-2.29; +2.50] | -0.67 [-1.92; +0.50] | -1.22 | YOK | YOK |
| C195:Y11 | ABD egitim | 20 / 14 | +0.63 [-5.44; +6.59] | +1.40 [-0.88; +3.35] | -0.78 [-6.16; +4.02] | -1.47 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11 | ABD sinama | 18 / 14 | -0.15 [-7.38; +8.85] | -1.88 [-4.54; +0.89] | +1.73 [-4.52; +10.41] | +1.85 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11 | AVR egitim | 6 / 6 | -0.65 [-3.46; +2.39] | +3.27 [+0.43; +6.79] | -3.92 [-10.07; +1.98] | -5.11 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11 | AVR sinama | 3 / 3 | -0.70 [-5.23; +6.34] | -1.09 [-2.28; +0.25] | +0.38 [-3.48; +7.58] | -1.27 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11 | BIST egitim | 10 / 8 | -3.73 [-7.96; +1.17] | +0.06 [-3.32; +4.46] | -3.79 [-8.84; +1.36] | -5.49 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11 | BIST sinama | 12 / 5 | +8.02 [+1.28; +14.94] | +7.34 [+2.55; +12.30] | +0.68 [-2.17; +7.61] | -3.90 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | ABD egitim | 4 / 4 | +8.12 [+0.29; +14.01] | +1.17 [-2.53; +4.70] | +6.96 [-0.98; +11.51] | +3.20 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | ABD sinama | 3 / 3 | -6.00 [-20.79; +5.65] | -0.41 [-6.84; +3.59] | -5.59 [-13.95; +2.06] | -3.24 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | AVR egitim | 2 / 2 | +3.11 [+0.33; +5.90] | +0.09 [-1.00; +1.18] | +3.02 [-0.85; +6.90] | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | AVR sinama | 2 / 2 | +0.56 [-5.23; +6.34] | -1.76 [-2.28; -1.24] | +2.31 [-2.95; +7.58] | +0.62 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | BIST egitim | 4 / 4 | -1.89 [-11.66; +6.94] | -1.87 [-7.78; +5.80] | -0.03 [-7.53; +10.26] | -10.46 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11b | BIST sinama | 9 / 5 | +6.38 [+1.28; +15.29] | +5.20 [+2.55; +10.26] | +1.18 [-3.77; +8.88] | -4.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C195:Y11c | ABD egitim | 464 / 69 | -0.80 [-1.81; +0.18] | -1.20 [-2.81; +0.16] | +0.40 [-0.91; +1.72] | +0.11 | YOK | YOK |
| C195:Y11c | ABD sinama | 354 / 41 | -0.72 [-2.01; +0.88] | -0.81 [-2.14; +0.81] | +0.09 [-0.69; +0.90] | -0.06 | YOK | YOK |
| C195:Y11c | AVR egitim | 231 / 65 | +0.47 [-0.56; +1.48] | +0.06 [-0.77; +0.82] | +0.42 [-0.52; +1.41] | +0.53 | YOK | YOK |
| C195:Y11c | AVR sinama | 161 / 38 | -0.17 [-1.21; +0.89] | -0.30 [-1.17; +0.44] | +0.12 [-0.88; +1.13] | +0.30 | YOK | YOK |
| C195:Y11c | BIST egitim | 141 / 44 | +0.13 [-3.06; +3.33] | +0.54 [-1.74; +2.57] | -0.41 [-2.66; +2.23] | -0.76 | YOK | YOK |
| C195:Y11c | BIST sinama | 155 / 29 | +4.83 [-2.39; +10.21] | +4.01 [-1.87; +8.57] | +0.82 [-1.27; +2.46] | +0.14 | YOK | YOK |
| C196:B_F14 | ABD egitim | 100 / 45 | -2.27 [-4.67; +0.16] | -0.34 [-1.67; +1.02] | -1.93 [-3.98; +0.21] | -2.22 | YOK | YOK |
| C196:B_F14 | ABD sinama | 137 / 38 | +1.48 [-1.62; +4.82] | +0.29 [-0.68; +1.15] | +1.19 [-1.64; +4.22] | +1.94 | YOK | YOK |
| C196:B_F14 | AVR egitim | 22 / 18 | +1.62 [-0.89; +4.18] | -0.06 [-1.61; +1.61] | +1.68 [-1.82; +5.03] | +1.09 | YOK | YOK |
| C196:B_F14 | AVR sinama | 17 / 12 | +6.05 [+0.12; +12.50] | +0.11 [-0.75; +1.18] | +5.94 [+0.05; +12.35] | +5.15 | YOK | YOK |
| C196:B_F14 | BIST egitim | 113 / 41 | -1.79 [-4.40; +1.25] | -0.68 [-2.43; +1.44] | -1.11 [-3.57; +1.24] | -0.24 | YOK | YOK |
| C196:B_F14 | BIST sinama | 228 / 36 | -0.32 [-6.24; +5.16] | +0.47 [-4.72; +4.65] | -0.79 [-3.46; +2.00] | -0.77 | YOK | YOK |
| C196:B_S2 | ABD egitim | 206 / 55 | +0.40 [-2.76; +3.21] | +0.57 [-1.77; +2.71] | -0.17 [-1.97; +1.38] | -0.76 | YOK | YOK |
| C196:B_S2 | ABD sinama | 232 / 43 | +0.44 [-1.78; +2.39] | +0.48 [-0.65; +1.50] | -0.04 [-1.57; +1.52] | -0.14 | YOK | YOK |
| C196:B_S2 | AVR egitim | 51 / 27 | +0.32 [-2.01; +2.48] | +0.09 [-1.35; +1.64] | +0.23 [-1.91; +2.44] | +0.82 | YOK | YOK |
| C196:B_S2 | AVR sinama | 51 / 28 | +1.05 [-2.55; +4.81] | +0.04 [-0.75; +0.70] | +1.01 [-2.48; +4.59] | +1.04 | YOK | YOK |
| C196:B_S2 | BIST egitim | 145 / 46 | -0.95 [-3.43; +1.95] | -0.87 [-2.41; +0.78] | -0.08 [-2.11; +2.23] | -0.40 | YOK | YOK |
| C196:B_S2 | BIST sinama | 207 / 32 | -0.46 [-6.13; +4.48] | +0.33 [-3.46; +3.66] | -0.79 [-3.59; +1.80] | -1.52 | YOK | YOK |
| C196:B_S3 | ABD egitim | 303 / 61 | +0.91 [-2.08; +3.29] | +0.59 [-1.97; +2.82] | +0.32 [-1.03; +1.83] | +0.09 | YOK | YOK |
| C196:B_S3 | ABD sinama | 345 / 44 | +1.05 [-0.86; +3.10] | +0.49 [-0.55; +1.55] | +0.56 [-0.77; +2.08] | +0.44 | YOK | YOK |
| C196:B_S3 | AVR egitim | 80 / 35 | +0.43 [-1.49; +2.25] | +0.06 [-1.39; +1.44] | +0.36 [-1.44; +2.31] | +0.81 | YOK | YOK |
| C196:B_S3 | AVR sinama | 67 / 32 | +0.22 [-3.21; +3.47] | +0.24 [-0.46; +0.83] | -0.02 [-3.28; +3.22] | +0.31 | YOK | YOK |
| C196:B_S3 | BIST egitim | 217 / 53 | -0.98 [-3.49; +1.71] | -1.12 [-2.63; +0.54] | +0.14 [-1.76; +2.36] | -0.03 | YOK | YOK |
| C196:B_S3 | BIST sinama | 320 / 38 | +0.33 [-4.74; +4.25] | +0.51 [-3.74; +3.68] | -0.18 [-1.97; +1.53] | -0.30 | YOK | YOK |
| C196:B_S4 | ABD egitim | 310 / 63 | +0.49 [-2.19; +2.75] | +0.53 [-1.67; +2.46] | -0.03 [-1.49; +1.27] | -0.16 | YOK | YOK |
| C196:B_S4 | ABD sinama | 353 / 44 | +0.90 [-0.98; +2.90] | +0.42 [-0.58; +1.41] | +0.48 [-0.80; +1.99] | +0.42 | YOK | YOK |
| C196:B_S4 | AVR egitim | 78 / 35 | +0.15 [-1.78; +1.88] | +0.32 [-1.15; +1.80] | -0.17 [-1.95; +1.61] | -0.05 | YOK | YOK |
| C196:B_S4 | AVR sinama | 70 / 32 | +0.42 [-2.45; +3.37] | +0.31 [-0.17; +0.74] | +0.12 [-2.65; +2.99] | +0.59 | YOK | YOK |
| C196:B_S4 | BIST egitim | 236 / 53 | -1.30 [-3.83; +1.34] | -1.20 [-2.72; +0.42] | -0.10 [-1.91; +2.00] | -0.25 | YOK | YOK |
| C196:B_S4 | BIST sinama | 359 / 39 | -0.08 [-5.01; +3.88] | +0.44 [-3.61; +3.54] | -0.52 [-2.38; +1.26] | -0.79 | YOK | YOK |
| C196:B_S5 | ABD egitim | 171 / 48 | +0.81 [-1.72; +2.78] | +0.68 [-1.45; +2.50] | +0.14 [-1.30; +1.76] | -0.58 | YOK | YOK |
| C196:B_S5 | ABD sinama | 164 / 37 | +1.21 [-1.04; +3.23] | +0.49 [-0.58; +1.56] | +0.72 [-0.92; +2.20] | +0.68 | YOK | YOK |
| C196:B_S5 | AVR egitim | 38 / 25 | -0.51 [-3.70; +2.38] | -0.32 [-1.83; +1.06] | -0.19 [-2.74; +2.37] | -0.01 | YOK | YOK |
| C196:B_S5 | AVR sinama | 43 / 27 | +0.72 [-2.05; +3.21] | +0.41 [-0.45; +1.18] | +0.31 [-2.03; +2.46] | +0.78 | YOK | YOK |
| C196:B_S5 | BIST egitim | 141 / 42 | -1.01 [-4.04; +2.41] | -1.41 [-3.09; +0.68] | +0.40 [-2.02; +3.09] | -0.45 | YOK | YOK |
| C196:B_S5 | BIST sinama | 295 / 39 | -0.49 [-5.56; +3.40] | +0.30 [-3.88; +3.42] | -0.79 [-2.43; +0.51] | -1.18 | YOK | YOK |
| C196:B_S6 | ABD egitim | 271 / 60 | +0.92 [-1.98; +3.21] | +0.65 [-1.80; +2.76] | +0.27 [-1.35; +1.77] | -0.01 | YOK | YOK |
| C196:B_S6 | ABD sinama | 262 / 44 | +1.43 [-0.55; +3.53] | +0.42 [-0.56; +1.33] | +1.00 [-0.62; +2.81] | +1.29 | YOK | YOK |
| C196:B_S6 | AVR egitim | 76 / 31 | -0.27 [-2.47; +1.70] | +0.02 [-1.74; +1.74] | -0.29 [-2.12; +1.56] | -0.05 | YOK | YOK |
| C196:B_S6 | AVR sinama | 53 / 29 | +1.26 [-2.41; +4.85] | +0.38 [-0.32; +0.99] | +0.88 [-2.68; +4.37] | +1.50 | YOK | YOK |
| C196:B_S6 | BIST egitim | 198 / 48 | -1.34 [-3.62; +1.29] | -1.08 [-2.60; +0.57] | -0.26 [-2.31; +1.96] | -0.27 | YOK | YOK |
| C196:B_S6 | BIST sinama | 276 / 36 | +0.38 [-4.83; +4.63] | +0.61 [-3.79; +4.13] | -0.23 [-2.04; +1.66] | -0.63 | YOK | YOK |
| C196:B_S7 | ABD egitim | 176 / 58 | +2.04 [-0.41; +3.98] | +0.30 [-1.60; +2.15] | +1.74 [+0.14; +3.45] | +1.56 | YOK | YOK |
| C196:B_S7 | ABD sinama | 169 / 39 | +1.52 [-0.40; +3.39] | +0.51 [-0.60; +1.50] | +1.01 [-0.46; +2.52] | +0.64 | YOK | YOK |
| C196:B_S7 | AVR egitim | 52 / 30 | +0.84 [-1.37; +2.75] | +0.57 [-1.01; +2.05] | +0.27 [-2.13; +2.35] | +0.42 | YOK | YOK |
| C196:B_S7 | AVR sinama | 47 / 27 | +1.15 [-2.17; +4.51] | +0.33 [-0.16; +0.84] | +0.82 [-2.33; +4.00] | +1.47 | YOK | YOK |
| C196:B_S7 | BIST egitim | 129 / 40 | -0.12 [-3.14; +3.12] | -0.86 [-2.52; +1.05] | +0.74 [-2.01; +3.78] | +0.03 | YOK | YOK |
| C196:B_S7 | BIST sinama | 184 / 32 | +0.10 [-4.36; +3.87] | +0.93 [-2.46; +3.90] | -0.83 [-3.06; +1.45] | -1.35 | YOK | YOK |
| C196:B_S8 | ABD egitim | 342 / 63 | +0.76 [-1.74; +2.87] | +0.61 [-1.77; +2.62] | +0.16 [-1.11; +1.42] | -0.05 | YOK | YOK |
| C196:B_S8 | ABD sinama | 374 / 44 | +1.13 [-0.71; +3.04] | +0.49 [-0.49; +1.45] | +0.64 [-0.63; +2.04] | +0.56 | YOK | YOK |
| C196:B_S8 | AVR egitim | 89 / 37 | +0.31 [-1.66; +2.01] | +0.08 [-1.49; +1.62] | +0.23 [-1.31; +1.86] | +0.49 | YOK | YOK |
| C196:B_S8 | AVR sinama | 75 / 33 | +0.49 [-2.28; +3.38] | +0.25 [-0.37; +0.81] | +0.24 [-2.40; +2.97] | +0.66 | YOK | YOK |
| C196:B_S8 | BIST egitim | 233 / 52 | -1.07 [-3.46; +1.58] | -1.20 [-2.75; +0.46] | +0.13 [-1.65; +2.28] | -0.08 | YOK | YOK |
| C196:B_S8 | BIST sinama | 360 / 39 | +0.03 [-4.88; +3.98] | +0.46 [-3.60; +3.54] | -0.43 [-2.32; +1.37] | -0.72 | YOK | YOK |
| C196:B_S9 | ABD egitim | 31 / 21 | +0.32 [-5.58; +5.25] | +0.60 [-1.18; +2.42] | -0.28 [-5.39; +4.02] | -0.80 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:B_S9 | ABD sinama | 23 / 15 | +0.49 [-4.56; +6.94] | -1.78 [-3.75; +0.41] | +2.27 [-2.37; +8.60] | +2.17 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:B_S9 | AVR egitim | 11 / 10 | +1.17 [-1.41; +4.43] | +0.99 [-2.10; +3.82] | +0.19 [-4.35; +4.90] | +1.04 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:B_S9 | AVR sinama | 5 / 5 | -3.46 [-13.35; +5.07] | -0.01 [-1.56; +2.02] | -3.45 [-13.32; +4.15] | -3.61 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:B_S9 | BIST egitim | 16 / 12 | -2.63 [-6.20; +2.93] | -0.17 [-2.51; +3.46] | -2.46 [-5.86; +2.24] | -2.93 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:B_S9 | BIST sinama | 31 / 13 | +6.93 [+0.57; +12.48] | +4.73 [-2.65; +9.31] | +2.20 [-1.60; +10.22] | -1.24 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:F14 | ABD egitim | 6058 / 77 | -0.89 [-1.54; -0.27] | -0.48 [-1.48; +0.55] | -0.41 [-1.30; +0.28] | — | YOK | YOK |
| C196:F14 | ABD sinama | 3911 / 44 | -0.50 [-1.16; +0.13] | -0.18 [-1.10; +0.66] | -0.31 [-0.84; +0.21] | — | YOK | YOK |
| C196:F14 | AVR egitim | 2936 / 82 | -0.22 [-0.70; +0.21] | -0.14 [-0.66; +0.31] | -0.07 [-0.35; +0.21] | — | YOK | YOK |
| C196:F14 | AVR sinama | 1597 / 44 | -0.56 [-1.04; -0.06] | -0.34 [-0.83; +0.14] | -0.21 [-0.53; +0.10] | — | YOK | YOK |
| C196:F14 | BIST egitim | 1764 / 79 | +1.05 [-0.71; +2.89] | +1.79 [+0.05; +3.49] | -0.73 [-1.55; +0.10] | — | YOK | YOK |
| C196:F14 | BIST sinama | 1449 / 44 | -0.98 [-4.23; +2.10] | +0.20 [-2.54; +2.77] | -1.18 [-2.33; +0.03] | — | YOK | YOK |
| C196:G1 | ABD egitim | 5346 / 77 | -0.89 [-1.57; -0.24] | -0.50 [-1.50; +0.55] | -0.38 [-1.32; +0.33] | +0.00 | YOK | YOK |
| C196:G1 | ABD sinama | 3262 / 44 | -0.55 [-1.25; +0.11] | -0.23 [-1.14; +0.64] | -0.33 [-0.97; +0.31] | +0.13 | YOK | YOK |
| C196:G1 | AVR egitim | 2683 / 82 | -0.23 [-0.75; +0.21] | -0.17 [-0.68; +0.30] | -0.07 [-0.35; +0.22] | +0.16 | YOK | YOK |
| C196:G1 | AVR sinama | 1423 / 44 | -0.71 [-1.20; -0.23] | -0.38 [-0.87; +0.11] | -0.33 [-0.67; -0.02] | +0.06 | YOK | YOK |
| C196:G1 | BIST egitim | 1363 / 79 | +2.03 [+0.06; +3.96] | +2.31 [+0.37; +4.17] | -0.28 [-1.19; +0.71] | -0.24 | YOK | YOK |
| C196:G1 | BIST sinama | 858 / 44 | -1.64 [-3.98; +0.92] | -0.50 [-2.47; +1.59] | -1.14 [-2.43; +0.26] | -1.06 | YOK | YOK |
| C196:G2 | ABD egitim | 346 / 64 | +0.58 [-2.13; +2.75] | +0.54 [-1.82; +2.65] | +0.04 [-1.22; +1.30] | -0.15 | YOK | YOK |
| C196:G2 | ABD sinama | 377 / 44 | +1.00 [-0.84; +2.93] | +0.50 [-0.49; +1.48] | +0.50 [-0.73; +1.95] | +0.41 | YOK | YOK |
| C196:G2 | AVR egitim | 89 / 37 | +0.31 [-1.66; +2.01] | +0.08 [-1.49; +1.62] | +0.23 [-1.31; +1.86] | +0.49 | YOK | YOK |
| C196:G2 | AVR sinama | 75 / 33 | +0.49 [-2.28; +3.38] | +0.25 [-0.37; +0.81] | +0.24 [-2.40; +2.97] | +0.66 | YOK | YOK |
| C196:G2 | BIST egitim | 238 / 53 | -1.29 [-3.79; +1.32] | -1.21 [-2.72; +0.39] | -0.07 [-1.85; +2.00] | -0.23 | YOK | YOK |
| C196:G2 | BIST sinama | 362 / 39 | +0.01 [-4.88; +3.93] | +0.48 [-3.58; +3.56] | -0.47 [-2.33; +1.28] | -0.75 | YOK | YOK |
| C196:G2u | ABD egitim | 31 / 21 | +0.32 [-5.58; +5.25] | +0.60 [-1.18; +2.42] | -0.28 [-5.39; +4.02] | -0.80 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:G2u | ABD sinama | 23 / 15 | +0.49 [-4.56; +6.94] | -1.78 [-3.75; +0.41] | +2.27 [-2.37; +8.60] | +2.17 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:G2u | AVR egitim | 11 / 10 | +1.17 [-1.41; +4.43] | +0.99 [-2.10; +3.82] | +0.19 [-4.35; +4.90] | +1.04 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:G2u | AVR sinama | 5 / 5 | -3.46 [-13.35; +5.07] | -0.01 [-1.56; +2.02] | -3.45 [-13.32; +4.15] | -3.61 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:G2u | BIST egitim | 16 / 12 | -2.63 [-6.20; +2.93] | -0.17 [-2.51; +3.46] | -2.46 [-5.86; +2.24] | -2.93 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:G2u | BIST sinama | 31 / 13 | +6.93 [+0.57; +12.48] | +4.73 [-2.65; +9.31] | +2.20 [-1.60; +10.22] | -1.24 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C196:S1 | ABD egitim | 346 / 64 | +0.58 [-2.13; +2.75] | +0.54 [-1.82; +2.65] | +0.04 [-1.22; +1.30] | — | YOK | YOK |
| C196:S1 | ABD sinama | 377 / 44 | +1.00 [-0.84; +2.93] | +0.50 [-0.49; +1.48] | +0.50 [-0.73; +1.95] | — | YOK | YOK |
| C196:S1 | AVR egitim | 89 / 37 | +0.31 [-1.66; +2.01] | +0.08 [-1.49; +1.62] | +0.23 [-1.31; +1.86] | — | YOK | YOK |
| C196:S1 | AVR sinama | 75 / 33 | +0.49 [-2.28; +3.38] | +0.25 [-0.37; +0.81] | +0.24 [-2.40; +2.97] | — | YOK | YOK |
| C196:S1 | BIST egitim | 238 / 53 | -1.29 [-3.79; +1.32] | -1.21 [-2.72; +0.39] | -0.07 [-1.85; +2.00] | — | YOK | YOK |
| C196:S1 | BIST sinama | 362 / 39 | +0.01 [-4.88; +3.93] | +0.48 [-3.58; +3.56] | -0.47 [-2.33; +1.28] | — | YOK | YOK |
| C196:S2 | ABD egitim | 5024 / 77 | -1.00 [-1.68; -0.32] | -0.23 [-1.46; +1.16] | -0.76 [-1.81; +0.02] | — | YOK | YOK |
| C196:S2 | ABD sinama | 3847 / 44 | -0.20 [-1.01; +0.62] | +0.09 [-0.89; +1.09] | -0.29 [-0.75; +0.19] | — | YOK | YOK |
| C196:S2 | AVR egitim | 2723 / 83 | -0.29 [-0.78; +0.18] | -0.23 [-0.75; +0.23] | -0.05 [-0.30; +0.22] | — | YOK | YOK |
| C196:S2 | AVR sinama | 1558 / 44 | -0.31 [-1.06; +0.48] | -0.16 [-0.74; +0.40] | -0.15 [-0.56; +0.28] | — | YOK | YOK |
| C196:S2 | BIST egitim | 1572 / 79 | +0.25 [-1.22; +1.72] | +1.22 [-0.27; +2.74] | -0.97 [-1.67; -0.22] | — | YOK | YOK |
| C196:S2 | BIST sinama | 1240 / 44 | -0.74 [-3.58; +2.09] | +0.07 [-2.28; +2.38] | -0.81 [-1.86; +0.24] | — | YOK | YOK |
| C196:S3 | ABD egitim | 7614 / 77 | -1.06 [-1.79; -0.35] | -0.33 [-1.50; +0.95] | -0.74 [-1.68; -0.04] | — | YOK | YOK |
| C196:S3 | ABD sinama | 5450 / 44 | -0.37 [-1.17; +0.45] | +0.03 [-0.94; +1.00] | -0.40 [-0.78; +0.01] | — | YOK | YOK |
| C196:S3 | AVR egitim | 3910 / 83 | -0.31 [-0.76; +0.13] | -0.18 [-0.69; +0.29] | -0.13 [-0.37; +0.13] | — | YOK | YOK |
| C196:S3 | AVR sinama | 2205 / 44 | -0.45 [-1.11; +0.27] | -0.19 [-0.77; +0.38] | -0.27 [-0.60; +0.07] | — | YOK | YOK |
| C196:S3 | BIST egitim | 2379 / 79 | +0.34 [-1.11; +1.93] | +1.10 [-0.38; +2.62] | -0.75 [-1.37; -0.12] | — | YOK | YOK |
| C196:S3 | BIST sinama | 1896 / 44 | -0.66 [-3.36; +2.04] | +0.09 [-2.27; +2.41] | -0.75 [-1.63; +0.12] | — | YOK | YOK |
| C196:S4 | ABD egitim | 8245 / 77 | -1.07 [-1.79; -0.37] | -0.37 [-1.58; +0.98] | -0.70 [-1.73; +0.04] | — | YOK | YOK |
| C196:S4 | ABD sinama | 5811 / 44 | -0.39 [-1.18; +0.44] | +0.02 [-0.96; +1.00] | -0.41 [-0.79; +0.00] | — | YOK | YOK |
| C196:S4 | AVR egitim | 4160 / 82 | -0.38 [-0.89; +0.08] | -0.19 [-0.71; +0.29] | -0.19 [-0.44; +0.04] | — | YOK | YOK |
| C196:S4 | AVR sinama | 2347 / 44 | -0.47 [-1.12; +0.25] | -0.24 [-0.82; +0.35] | -0.23 [-0.53; +0.06] | — | YOK | YOK |
| C196:S4 | BIST egitim | 2535 / 79 | +0.24 [-1.26; +1.77] | +1.14 [-0.36; +2.69] | -0.90 [-1.51; -0.27] | — | YOK | YOK |
| C196:S4 | BIST sinama | 2066 / 44 | -0.87 [-3.56; +1.86] | +0.07 [-2.33; +2.42] | -0.94 [-1.80; -0.05] | — | YOK | YOK |
| C196:S5 | ABD egitim | 3823 / 77 | -1.22 [-2.15; -0.36] | -0.57 [-1.92; +0.88] | -0.64 [-1.69; +0.19] | — | YOK | YOK |
| C196:S5 | ABD sinama | 2965 / 44 | -0.67 [-1.53; +0.20] | -0.24 [-1.26; +0.77] | -0.42 [-0.92; +0.04] | — | YOK | YOK |
| C196:S5 | AVR egitim | 2208 / 80 | -0.40 [-0.97; +0.13] | -0.30 [-0.83; +0.21] | -0.10 [-0.48; +0.27] | — | YOK | YOK |
| C196:S5 | AVR sinama | 1362 / 44 | -0.30 [-1.02; +0.41] | -0.17 [-0.77; +0.41] | -0.13 [-0.55; +0.25] | — | YOK | YOK |
| C196:S5 | BIST egitim | 1572 / 78 | +0.16 [-1.50; +1.80] | +1.16 [-0.43; +2.71] | -0.99 [-1.90; -0.10] | — | YOK | YOK |
| C196:S5 | BIST sinama | 1548 / 43 | -0.71 [-3.50; +1.94] | +0.09 [-2.31; +2.31] | -0.80 [-1.75; +0.04] | — | YOK | YOK |
| C196:S6 | ABD egitim | 6960 / 77 | -1.10 [-1.82; -0.40] | -0.62 [-1.63; +0.35] | -0.49 [-1.12; +0.08] | — | YOK | YOK |
| C196:S6 | ABD sinama | 4817 / 44 | -0.43 [-1.22; +0.38] | +0.01 [-0.97; +0.99] | -0.45 [-0.86; -0.02] | — | YOK | YOK |
| C196:S6 | AVR egitim | 3621 / 81 | -0.45 [-1.00; +0.06] | -0.25 [-0.83; +0.28] | -0.19 [-0.46; +0.06] | — | YOK | YOK |
| C196:S6 | AVR sinama | 2087 / 44 | -0.35 [-1.01; +0.34] | -0.18 [-0.78; +0.42] | -0.18 [-0.45; +0.12] | — | YOK | YOK |
| C196:S6 | BIST egitim | 2193 / 78 | +0.24 [-1.25; +1.79] | +1.08 [-0.43; +2.61] | -0.84 [-1.53; -0.13] | — | YOK | YOK |
| C196:S6 | BIST sinama | 1632 / 44 | -0.92 [-3.79; +1.93] | -0.02 [-2.56; +2.44] | -0.90 [-1.83; +0.08] | — | YOK | YOK |
| C196:S7 | ABD egitim | 4953 / 77 | -0.93 [-1.63; -0.22] | -0.54 [-1.61; +0.56] | -0.39 [-1.10; +0.24] | — | YOK | YOK |
| C196:S7 | ABD sinama | 3348 / 44 | -0.36 [-1.08; +0.35] | +0.04 [-0.93; +0.96] | -0.39 [-0.79; +0.04] | — | YOK | YOK |
| C196:S7 | AVR egitim | 2801 / 82 | -0.38 [-0.97; +0.10] | -0.18 [-0.71; +0.29] | -0.20 [-0.51; +0.09] | — | YOK | YOK |
| C196:S7 | AVR sinama | 1511 / 44 | -0.29 [-1.00; +0.47] | -0.17 [-0.77; +0.41] | -0.12 [-0.43; +0.21] | — | YOK | YOK |
| C196:S7 | BIST egitim | 1626 / 78 | +0.39 [-1.11; +1.92] | +1.25 [-0.24; +2.73] | -0.86 [-1.60; -0.09] | — | YOK | YOK |
| C196:S7 | BIST sinama | 1227 / 43 | -0.51 [-3.21; +1.98] | +0.45 [-1.91; +2.62] | -0.95 [-1.91; -0.05] | — | YOK | YOK |
| C196:S8 | ABD egitim | 8539 / 77 | -1.01 [-1.72; -0.30] | -0.36 [-1.54; +0.93] | -0.66 [-1.62; +0.05] | — | YOK | YOK |
| C196:S8 | ABD sinama | 5953 / 44 | -0.29 [-1.07; +0.53] | +0.04 [-0.93; +1.00] | -0.32 [-0.70; +0.09] | — | YOK | YOK |
| C196:S8 | AVR egitim | 4456 / 83 | -0.36 [-0.84; +0.10] | -0.18 [-0.69; +0.30] | -0.18 [-0.40; +0.07] | — | YOK | YOK |
| C196:S8 | AVR sinama | 2490 / 44 | -0.41 [-1.05; +0.27] | -0.19 [-0.76; +0.38] | -0.22 [-0.51; +0.07] | — | YOK | YOK |
| C196:S8 | BIST egitim | 2467 / 79 | +0.23 [-1.30; +1.76] | +1.13 [-0.39; +2.68] | -0.90 [-1.51; -0.29] | — | YOK | YOK |
| C196:S8 | BIST sinama | 2044 / 44 | -0.70 [-3.35; +1.95] | +0.07 [-2.31; +2.42] | -0.77 [-1.62; +0.10] | — | YOK | YOK |
| C196:S9 | ABD egitim | 464 / 69 | -0.80 [-1.81; +0.18] | -1.20 [-2.81; +0.16] | +0.40 [-0.91; +1.72] | — | YOK | YOK |
| C196:S9 | ABD sinama | 354 / 41 | -0.72 [-2.01; +0.88] | -0.81 [-2.14; +0.81] | +0.09 [-0.69; +0.90] | — | YOK | YOK |
| C196:S9 | AVR egitim | 231 / 65 | +0.47 [-0.56; +1.48] | +0.06 [-0.77; +0.82] | +0.42 [-0.52; +1.41] | — | YOK | YOK |
| C196:S9 | AVR sinama | 161 / 38 | -0.17 [-1.21; +0.89] | -0.30 [-1.17; +0.44] | +0.12 [-0.88; +1.13] | — | YOK | YOK |
| C196:S9 | BIST egitim | 141 / 44 | +0.13 [-3.06; +3.33] | +0.54 [-1.74; +2.57] | -0.41 [-2.66; +2.23] | — | YOK | YOK |
| C196:S9 | BIST sinama | 155 / 29 | +4.83 [-2.39; +10.21] | +4.01 [-1.87; +8.57] | +0.82 [-1.27; +2.46] | — | YOK | YOK |
| C197:P_AB_alt20 | ABD egitim | 1737 / 76 | -0.77 [-1.37; -0.21] | -0.65 [-1.46; +0.18] | -0.12 [-0.75; +0.40] | -0.14 | YOK | YOK |
| C197:P_AB_alt20 | ABD sinama | 1225 / 44 | -0.57 [-1.20; +0.01] | -0.33 [-1.33; +0.64] | -0.24 [-0.95; +0.50] | -0.06 | YOK | YOK |
| C197:P_AB_alt20 | AVR egitim | 899 / 82 | -0.43 [-1.01; +0.09] | -0.29 [-0.88; +0.21] | -0.14 [-0.48; +0.21] | -0.16 | YOK | YOK |
| C197:P_AB_alt20 | AVR sinama | 506 / 43 | -0.37 [-0.84; +0.16] | -0.25 [-0.82; +0.33] | -0.12 [-0.58; +0.38] | -0.04 | YOK | YOK |
| C197:P_AB_alt20 | BIST egitim | 518 / 71 | -0.23 [-1.79; +1.34] | +0.39 [-1.06; +1.70] | -0.62 [-1.46; +0.22] | -0.67 | YOK | YOK |
| C197:P_AB_alt20 | BIST sinama | 420 / 41 | -1.90 [-4.83; +0.93] | -0.26 [-2.80; +2.23] | -1.64 [-2.66; -0.67] | -2.17 | YOK | YOK |
| C197:P_AB_ust20 | ABD egitim | 1737 / 75 | -1.49 [-2.99; -0.08] | +0.10 [-1.51; +1.77] | -1.59 [-2.98; -0.30] | -0.13 | YOK | YOK |
| C197:P_AB_ust20 | ABD sinama | 1225 / 44 | -0.78 [-2.20; +0.57] | +0.08 [-0.91; +1.06] | -0.86 [-1.82; +0.10] | -0.59 | YOK | YOK |
| C197:P_AB_ust20 | AVR egitim | 899 / 80 | -0.27 [-1.12; +0.48] | -0.21 [-0.89; +0.44] | -0.06 [-0.55; +0.43] | +0.22 | YOK | YOK |
| C197:P_AB_ust20 | AVR sinama | 506 / 44 | -0.05 [-1.06; +1.06] | +0.05 [-0.49; +0.58] | -0.10 [-0.81; +0.71] | +0.14 | YOK | YOK |
| C197:P_AB_ust20 | BIST egitim | 518 / 73 | -1.07 [-3.11; +1.13] | +0.64 [-1.09; +2.44] | -1.70 [-2.96; -0.43] | -1.50 | YOK | YOK |
| C197:P_AB_ust20 | BIST sinama | 420 / 43 | -0.97 [-4.35; +2.55] | -0.28 [-2.88; +2.13] | -0.69 [-2.40; +1.15] | -0.37 | YOK | YOK |
| C197:P_C_alt20 | ABD egitim | 1110 / 46 | -1.27 [-2.56; -0.24] | -1.45 [-3.12; +0.10] | +0.18 [-0.89; +1.24] | -0.13 | YOK | YOK |
| C197:P_C_alt20 | ABD sinama | 1226 / 43 | -0.57 [-1.18; -0.00] | -0.37 [-1.47; +0.61] | -0.20 [-0.91; +0.55] | -0.02 | YOK | YOK |
| C197:P_C_alt20 | AVR egitim | 527 / 45 | -0.53 [-1.41; +0.20] | -0.58 [-1.50; +0.23] | +0.05 [-0.45; +0.54] | -0.05 | YOK | YOK |
| C197:P_C_alt20 | AVR sinama | 507 / 44 | -0.49 [-0.99; +0.06] | -0.27 [-0.87; +0.28] | -0.22 [-0.74; +0.34] | -0.12 | YOK | YOK |
| C197:P_C_alt20 | BIST egitim | 360 / 45 | +1.77 [-0.51; +3.87] | +2.13 [-0.00; +4.18] | -0.36 [-1.88; +1.21] | -0.34 | YOK | YOK |
| C197:P_C_alt20 | BIST sinama | 421 / 41 | -0.76 [-4.00; +2.29] | +0.17 [-2.46; +2.74] | -0.93 [-2.09; +0.19] | -1.17 | YOK | YOK |
| C197:P_C_ust20 | ABD egitim | 1110 / 45 | -0.94 [-2.62; +0.57] | +0.42 [-1.43; +2.58] | -1.36 [-3.19; +0.19] | -0.19 | YOK | YOK |
| C197:P_C_ust20 | ABD sinama | 1226 / 44 | -0.67 [-2.08; +0.78] | +0.10 [-0.92; +1.11] | -0.76 [-1.72; +0.29] | -0.53 | YOK | YOK |
| C197:P_C_ust20 | AVR egitim | 527 / 45 | -0.58 [-1.73; +0.54] | +0.17 [-0.58; +0.87] | -0.75 [-1.57; +0.08] | -0.62 | YOK | YOK |
| C197:P_C_ust20 | AVR sinama | 507 / 44 | +0.43 [-0.58; +1.52] | -0.05 [-0.56; +0.46] | +0.48 [-0.21; +1.21] | +0.79 | YOK | YOK |
| C197:P_C_ust20 | BIST egitim | 360 / 46 | +0.23 [-2.44; +3.00] | +2.25 [-0.21; +4.54] | -2.02 [-3.57; -0.25] | -1.30 | YOK | YOK |
| C197:P_C_ust20 | BIST sinama | 421 / 43 | -1.73 [-4.67; +1.09] | -0.05 [-2.58; +2.22] | -1.68 [-2.83; -0.37] | -1.78 | YOK | YOK |
| C198:D1_E1_A | ABD egitim | 3281 / 77 | -0.71 [-1.42; -0.02] | -0.31 [-1.30; +0.67] | -0.40 [-1.15; +0.25] | -0.06 | YOK | YOK |
| C198:D1_E1_A | ABD sinama | 2004 / 44 | -0.44 [-1.27; +0.36] | -0.08 [-1.14; +0.94] | -0.36 [-0.86; +0.15] | -0.06 | YOK | YOK |
| C198:D1_E1_A | AVR egitim | 1687 / 81 | -0.19 [-0.74; +0.32] | -0.21 [-0.75; +0.31] | +0.02 [-0.34; +0.36] | +0.13 | YOK | YOK |
| C198:D1_E1_A | AVR sinama | 873 / 44 | -0.14 [-0.93; +0.69] | -0.21 [-0.88; +0.49] | +0.07 [-0.29; +0.48] | +0.28 | YOK | YOK |
| C198:D1_E1_A | BIST egitim | 1125 / 78 | +0.66 [-1.03; +2.32] | +1.43 [-0.28; +3.09] | -0.77 [-1.86; +0.32] | -0.95 | YOK | YOK |
| C198:D1_E1_A | BIST sinama | 774 / 43 | +0.12 [-3.51; +3.72] | +0.84 [-2.20; +3.53] | -0.72 [-2.17; +0.63] | -0.55 | YOK | YOK |
| C198:D1_E1_B | ABD egitim | 176 / 54 | +0.77 [-2.21; +3.40] | +0.60 [-1.37; +2.46] | +0.17 [-1.71; +1.79] | -0.09 | YOK | YOK |
| C198:D1_E1_B | ABD sinama | 154 / 40 | +1.82 [-0.41; +4.10] | +0.37 [-0.64; +1.38] | +1.45 [-0.61; +3.54] | +1.59 | YOK | YOK |
| C198:D1_E1_B | AVR egitim | 40 / 26 | +0.08 [-2.53; +2.29] | +0.28 [-1.22; +1.51] | -0.20 [-2.56; +2.19] | +0.12 | YOK | YOK |
| C198:D1_E1_B | AVR sinama | 33 / 22 | +2.01 [-2.52; +7.06] | +0.17 [-0.38; +0.78] | +1.84 [-2.58; +6.82] | +2.59 | YOK | YOK |
| C198:D1_E1_B | BIST egitim | 132 / 43 | -1.20 [-3.65; +1.37] | -0.98 [-2.69; +0.90] | -0.22 [-2.66; +2.27] | -0.44 | YOK | YOK |
| C198:D1_E1_B | BIST sinama | 181 / 31 | +0.40 [-5.54; +5.76] | +0.42 [-4.51; +4.77] | -0.01 [-2.39; +2.09] | -0.50 | YOK | YOK |
| C198:D1_E1t_A | ABD egitim | 5405 / 77 | -1.18 [-2.01; -0.39] | -0.36 [-1.71; +1.17] | -0.82 [-1.99; +0.00] | -0.25 | YOK | YOK |
| C198:D1_E1t_A | ABD sinama | 4128 / 44 | -0.29 [-1.11; +0.56] | +0.08 [-0.92; +1.03] | -0.37 [-0.78; +0.06] | -0.09 | YOK | YOK |
| C198:D1_E1t_A | AVR egitim | 2809 / 82 | -0.45 [-1.03; +0.05] | -0.17 [-0.77; +0.33] | -0.28 [-0.54; -0.03] | -0.13 | YOK | YOK |
| C198:D1_E1t_A | AVR sinama | 1653 / 44 | -0.58 [-1.21; +0.09] | -0.19 [-0.73; +0.33] | -0.39 [-0.76; -0.02] | -0.20 | YOK | YOK |
| C198:D1_E1t_A | BIST egitim | 1463 / 79 | -0.09 [-1.74; +1.48] | +0.83 [-0.64; +2.34] | -0.92 [-1.65; -0.25] | -0.72 | YOK | YOK |
| C198:D1_E1t_A | BIST sinama | 1322 / 44 | -1.39 [-3.67; +1.00] | -0.38 [-2.40; +1.82] | -1.01 [-1.86; -0.16] | -0.99 | YOK | YOK |
| C198:D1_E1t_B | ABD egitim | 170 / 53 | +0.38 [-2.96; +2.74] | +0.48 [-2.78; +3.04] | -0.10 [-1.97; +1.94] | -0.24 | YOK | YOK |
| C198:D1_E1t_B | ABD sinama | 223 / 42 | +0.44 [-1.69; +2.56] | +0.59 [-0.55; +1.70] | -0.15 [-1.43; +1.18] | -0.44 | YOK | YOK |
| C198:D1_E1t_B | AVR egitim | 49 / 24 | +0.50 [-2.04; +2.75] | -0.08 [-1.79; +1.73] | +0.58 [-1.44; +2.80] | +0.84 | YOK | YOK |
| C198:D1_E1t_B | AVR sinama | 42 / 23 | -0.69 [-3.65; +1.72] | +0.32 [-0.61; +1.01] | -1.01 [-3.67; +1.38] | -0.79 | YOK | YOK |
| C198:D1_E1t_B | BIST egitim | 106 / 35 | -1.39 [-4.34; +2.23] | -1.51 [-3.00; +0.04] | +0.12 [-2.08; +2.96] | +0.01 | YOK | YOK |
| C198:D1_E1t_B | BIST sinama | 181 / 35 | -0.38 [-4.43; +2.95] | +0.55 [-2.34; +3.02] | -0.93 [-3.04; +0.94] | -0.99 | YOK | YOK |
| C198:D1_E2_A | ABD egitim | 6874 / 77 | -1.13 [-1.88; -0.43] | -0.20 [-1.48; +1.25] | -0.93 [-2.10; -0.09] | -0.26 | YOK | YOK |
| C198:D1_E2_A | ABD sinama | 5049 / 44 | -0.36 [-1.19; +0.48] | +0.01 [-0.98; +0.98] | -0.37 [-0.77; +0.04] | -0.03 | YOK | YOK |
| C198:D1_E2_A | AVR egitim | 3154 / 83 | -0.39 [-0.92; +0.14] | -0.07 [-0.58; +0.42] | -0.32 [-0.62; -0.01] | -0.12 | YOK | YOK |
| C198:D1_E2_A | AVR sinama | 1823 / 44 | -0.34 [-1.07; +0.47] | -0.25 [-0.87; +0.40] | -0.09 [-0.41; +0.26] | +0.10 | YOK | YOK |
| C198:D1_E2_A | BIST egitim | 2170 / 79 | +0.42 [-1.04; +1.98] | +1.30 [-0.31; +2.93] | -0.88 [-1.59; -0.14] | -0.77 | YOK | YOK |
| C198:D1_E2_A | BIST sinama | 1904 / 44 | -1.02 [-3.73; +1.79] | +0.01 [-2.37; +2.39] | -1.02 [-1.93; -0.09] | -0.98 | YOK | YOK |
| C198:D1_E2_B | ABD egitim | 214 / 57 | -0.30 [-3.39; +2.28] | +0.57 [-1.44; +2.41] | -0.87 [-2.87; +0.89] | -1.17 | YOK | YOK |
| C198:D1_E2_B | ABD sinama | 273 / 43 | +1.68 [-0.33; +3.75] | +0.59 [-0.46; +1.60] | +1.10 [-0.37; +2.72] | +1.21 | YOK | YOK |
| C198:D1_E2_B | AVR egitim | 47 / 31 | -0.39 [-2.39; +1.54] | -0.08 [-0.94; +0.65] | -0.31 [-2.35; +1.67] | +0.00 | YOK | YOK |
| C198:D1_E2_B | AVR sinama | 37 / 24 | +1.41 [-4.08; +5.99] | +0.02 [-0.95; +0.96] | +1.39 [-3.93; +5.91] | +1.30 | YOK | YOK |
| C198:D1_E2_B | BIST egitim | 176 / 50 | -0.85 [-3.23; +2.15] | -1.47 [-2.95; +0.17] | +0.62 [-1.53; +3.18] | +0.52 | YOK | YOK |
| C198:D1_E2_B | BIST sinama | 285 / 38 | -0.42 [-5.85; +4.04] | +0.49 [-4.14; +4.03] | -0.91 [-3.14; +1.15] | -1.07 | YOK | YOK |
| C198:D1_E2t_A | ABD egitim | 1811 / 74 | -0.54 [-1.56; +0.45] | -0.88 [-2.18; +0.42] | +0.34 [-0.19; +0.93] | +0.13 | YOK | YOK |
| C198:D1_E2t_A | ABD sinama | 1082 / 43 | -0.24 [-1.03; +0.52] | +0.11 [-1.16; +1.17] | -0.35 [-1.08; +0.48] | -0.34 | YOK | YOK |
| C198:D1_E2t_A | AVR egitim | 1337 / 78 | -0.27 [-0.87; +0.27] | -0.43 [-1.10; +0.17] | +0.16 [-0.14; +0.49] | +0.16 | YOK | YOK |
| C198:D1_E2t_A | AVR sinama | 698 / 44 | -0.66 [-1.28; -0.07] | -0.08 [-0.63; +0.42] | -0.58 [-1.04; -0.14] | -0.36 | YOK | YOK |
| C198:D1_E2t_A | BIST egitim | 418 / 70 | -0.74 [-2.85; +1.47] | -0.01 [-1.42; +1.38] | -0.74 [-2.03; +0.72] | -1.04 | YOK | YOK |
| C198:D1_E2t_A | BIST sinama | 192 / 35 | +1.02 [-2.19; +3.90] | +0.74 [-2.10; +3.33] | +0.28 [-1.52; +2.22] | +0.63 | YOK | YOK |
| C198:D1_E2t_B | ABD egitim | 132 / 44 | +2.01 [-0.73; +3.97] | +0.49 [-2.85; +3.15] | +1.52 [+0.23; +3.31] | +1.54 | YOK | YOK |
| C198:D1_E2t_B | ABD sinama | 104 / 35 | -0.78 [-3.06; +1.54] | +0.28 [-0.95; +1.41] | -1.06 [-2.87; +0.86] | -1.71 | YOK | YOK |
| C198:D1_E2t_B | AVR egitim | 42 / 17 | +1.10 [-1.85; +4.05] | +0.26 [-2.68; +2.85] | +0.83 [-1.38; +4.04] | +1.03 | YOK | YOK |
| C198:D1_E2t_B | AVR sinama | 38 / 19 | -0.40 [-3.03; +1.83] | +0.48 [-0.17; +1.05] | -0.88 [-3.19; +0.98] | +0.03 | YOK | YOK |
| C198:D1_E2t_B | BIST egitim | 62 / 30 | -2.53 [-6.99; +1.72] | -0.49 [-2.55; +1.46] | -2.04 [-5.69; +1.33] | -2.09 | YOK | YOK |
| C198:D1_E2t_B | BIST sinama | 77 / 24 | +1.61 [-3.17; +5.34] | +0.45 [-3.49; +2.99] | +1.17 [-1.30; +4.03] | +0.51 | YOK | YOK |
| C198:D1_W1_A | ABD egitim | 1978 / 75 | -1.01 [-1.78; -0.36] | -0.60 [-1.56; +0.34] | -0.40 [-1.28; +0.32] | -0.16 | YOK | YOK |
| C198:D1_W1_A | ABD sinama | 1305 / 44 | +0.28 [-0.72; +1.17] | +0.55 [-0.65; +1.59] | -0.27 [-0.72; +0.32] | +0.51 | YOK | YOK |
| C198:D1_W1_A | AVR egitim | 1060 / 78 | -0.32 [-0.97; +0.25] | -0.11 [-0.61; +0.35] | -0.21 [-0.62; +0.18] | -0.18 | YOK | YOK |
| C198:D1_W1_A | AVR sinama | 515 / 44 | -0.36 [-1.24; +0.58] | -0.21 [-0.94; +0.57] | -0.15 [-0.70; +0.36] | -0.09 | YOK | YOK |
| C198:D1_W1_A | BIST egitim | 572 / 73 | +0.81 [-1.25; +3.01] | +1.38 [-0.24; +2.98] | -0.56 [-1.68; +0.70] | -0.51 | YOK | YOK |
| C198:D1_W1_A | BIST sinama | 426 / 42 | -2.12 [-5.91; +1.39] | -0.23 [-3.85; +3.15] | -1.89 [-3.08; -0.58] | -1.76 | YOK | YOK |
| C198:D1_W1_B | ABD egitim | 53 / 33 | +0.61 [-2.29; +3.06] | +0.10 [-1.90; +1.96] | +0.51 [-1.89; +2.99] | +0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1_B | ABD sinama | 59 / 26 | -0.09 [-4.20; +4.33] | +1.05 [-0.16; +2.14] | -1.14 [-4.68; +2.97] | -0.34 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1_B | AVR egitim | 15 / 14 | -0.07 [-4.35; +3.38] | +0.26 [-0.68; +1.17] | -0.33 [-4.52; +3.22] | +0.66 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1_B | AVR sinama | 6 / 6 | +1.51 [-4.01; +7.32] | -0.01 [-1.56; +1.66] | +1.52 [-2.89; +5.93] | +1.70 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1_B | BIST egitim | 56 / 31 | -2.66 [-5.58; +0.65] | -1.27 [-3.03; +0.83] | -1.40 [-3.79; +1.57] | -0.87 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1_B | BIST sinama | 85 / 24 | -0.90 [-6.19; +4.22] | +0.09 [-5.38; +5.02] | -0.99 [-2.50; +0.79] | -0.75 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_A | ABD egitim | 1978 / 75 | -0.73 [-1.64; +0.15] | -0.27 [-1.58; +1.17] | -0.46 [-1.64; +0.47] | -0.29 | YOK | YOK |
| C198:D1_W1t_A | ABD sinama | 1485 / 43 | -0.37 [-1.34; +0.47] | -0.18 [-1.16; +0.69] | -0.19 [-0.74; +0.29] | -0.14 | YOK | YOK |
| C198:D1_W1t_A | AVR egitim | 1060 / 79 | -0.09 [-0.74; +0.52] | -0.06 [-0.67; +0.50] | -0.04 [-0.38; +0.33] | +0.10 | YOK | YOK |
| C198:D1_W1t_A | AVR sinama | 617 / 44 | -0.60 [-1.37; +0.14] | -0.26 [-0.84; +0.27] | -0.34 [-0.86; +0.20] | -0.03 | YOK | YOK |
| C198:D1_W1t_A | BIST egitim | 572 / 77 | -1.14 [-2.89; +0.50] | +0.86 [-0.77; +2.44] | -2.00 [-3.12; -0.95] | -1.44 | YOK | YOK |
| C198:D1_W1t_A | BIST sinama | 478 / 44 | -0.42 [-2.96; +2.43] | -0.10 [-2.04; +1.91] | -0.32 [-1.68; +1.25] | -0.62 | YOK | YOK |
| C198:D1_W1t_B | ABD egitim | 84 / 43 | -0.88 [-3.73; +1.70] | +0.07 [-1.90; +1.76] | -0.95 [-3.76; +1.76] | -1.48 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_B | ABD sinama | 100 / 32 | +0.04 [-2.42; +2.39] | +0.30 [-1.21; +1.72] | -0.26 [-1.83; +1.37] | -1.28 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_B | AVR egitim | 31 / 18 | +0.09 [-3.52; +3.07] | +1.05 [-1.21; +3.23] | -0.97 [-3.73; +1.99] | -1.84 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_B | AVR sinama | 27 / 17 | +0.50 [-3.54; +3.91] | +0.23 [-1.01; +1.15] | +0.26 [-3.41; +3.37] | +0.53 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_B | BIST egitim | 54 / 27 | -1.69 [-5.28; +1.68] | +0.23 [-1.72; +2.40] | -1.92 [-5.08; +1.12] | -1.48 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W1t_B | BIST sinama | 70 / 22 | +2.97 [-5.52; +9.74] | +1.64 [-2.38; +4.38] | +1.33 [-4.45; +6.72] | -0.10 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_A | ABD egitim | 1752 / 73 | -0.93 [-1.74; -0.09] | -0.25 [-1.72; +1.33] | -0.68 [-2.13; +0.55] | -0.46 | YOK | YOK |
| C198:D1_W2D_A | ABD sinama | 1181 / 43 | +0.29 [-0.65; +1.22] | +0.30 [-0.89; +1.39] | -0.01 [-0.79; +0.94] | +0.27 | YOK | YOK |
| C198:D1_W2D_A | AVR egitim | 973 / 79 | -0.34 [-0.93; +0.21] | -0.15 [-0.67; +0.33] | -0.19 [-0.59; +0.23] | -0.05 | YOK | YOK |
| C198:D1_W2D_A | AVR sinama | 545 / 44 | -0.60 [-1.46; +0.25] | -0.52 [-1.08; +0.08] | -0.09 [-0.74; +0.52] | +0.11 | YOK | YOK |
| C198:D1_W2D_A | BIST egitim | 469 / 69 | -0.31 [-2.18; +1.32] | +1.11 [-0.40; +2.50] | -1.42 [-2.66; -0.09] | -1.91 | YOK | YOK |
| C198:D1_W2D_A | BIST sinama | 310 / 37 | -1.13 [-5.11; +2.04] | -0.75 [-3.17; +1.26] | -0.39 [-2.43; +1.66] | -0.59 | YOK | YOK |
| C198:D1_W2D_B | ABD egitim | 51 / 31 | -0.36 [-3.82; +3.28] | -0.77 [-2.32; +0.88] | +0.41 [-2.53; +3.59] | -0.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_B | ABD sinama | 70 / 27 | -0.32 [-4.83; +3.99] | -0.11 [-1.43; +1.12] | -0.21 [-3.71; +3.62] | -0.32 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_B | AVR egitim | 15 / 11 | +0.38 [-4.00; +4.43] | -1.17 [-2.07; -0.29] | +1.55 [-2.67; +5.56] | +1.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_B | AVR sinama | 22 / 15 | +3.78 [-0.94; +8.93] | +0.14 [-0.61; +0.78] | +3.64 [-0.81; +8.88] | +4.82 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_B | BIST egitim | 43 / 23 | +1.39 [-3.86; +7.16] | -0.61 [-3.10; +2.17] | +1.99 [-3.26; +8.30] | +1.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2D_B | BIST sinama | 63 / 19 | +0.61 [-7.42; +8.28] | -0.01 [-3.61; +2.32] | +0.62 [-5.19; +7.10] | +0.47 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_A | ABD egitim | 1752 / 77 | -0.31 [-1.17; +0.46] | -0.00 [-1.19; +1.16] | -0.31 [-0.92; +0.27] | +0.08 | YOK | YOK |
| C198:D1_W2Dt_A | ABD sinama | 1318 / 44 | -0.40 [-1.48; +0.64] | -0.22 [-1.45; +0.93] | -0.17 [-0.60; +0.28] | +0.04 | YOK | YOK |
| C198:D1_W2Dt_A | AVR egitim | 973 / 79 | -0.32 [-0.92; +0.22] | -0.15 [-0.79; +0.40] | -0.17 [-0.62; +0.28] | +0.15 | YOK | YOK |
| C198:D1_W2Dt_A | AVR sinama | 599 / 44 | -0.14 [-0.93; +0.62] | -0.08 [-0.73; +0.52] | -0.06 [-0.57; +0.50] | -0.02 | YOK | YOK |
| C198:D1_W2Dt_A | BIST egitim | 469 / 71 | +1.01 [-1.13; +3.07] | +0.84 [-0.77; +2.39] | +0.17 [-1.03; +1.38] | -0.09 | YOK | YOK |
| C198:D1_W2Dt_A | BIST sinama | 255 / 42 | +0.78 [-2.60; +4.05] | +0.70 [-2.21; +3.29] | +0.08 [-1.38; +1.50] | +0.06 | YOK | YOK |
| C198:D1_W2Dt_B | ABD egitim | 51 / 23 | +1.74 [-3.43; +4.05] | +1.26 [-3.66; +4.00] | +0.48 [-1.64; +3.75] | +1.10 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_B | ABD sinama | 36 / 22 | +1.20 [-2.29; +4.69] | +0.63 [-0.93; +2.18] | +0.57 [-1.95; +3.30] | -0.33 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_B | AVR egitim | 8 / 6 | +2.02 [-3.46; +5.21] | +0.61 [-3.47; +3.17] | +1.40 [-3.24; +5.97] | +2.66 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_B | AVR sinama | 10 / 9 | +0.99 [-5.89; +6.26] | -0.21 [-2.74; +1.52] | +1.20 [-4.20; +5.53] | +0.79 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_B | BIST egitim | 48 / 18 | -1.15 [-3.60; +1.24] | -1.11 [-3.17; +0.70] | -0.04 [-2.03; +2.75] | -0.89 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2Dt_B | BIST sinama | 25 / 15 | +1.75 [-5.89; +7.57] | +3.22 [-2.07; +7.08] | -1.47 [-6.49; +2.73] | -1.04 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_A | ABD egitim | 1752 / 77 | -0.41 [-1.21; +0.31] | +0.01 [-1.21; +1.22] | -0.42 [-1.17; +0.22] | +0.06 | YOK | YOK |
| C198:D1_W2_A | ABD sinama | 1253 / 44 | -0.35 [-1.31; +0.59] | -0.02 [-1.21; +1.12] | -0.33 [-0.80; +0.13] | -0.06 | YOK | YOK |
| C198:D1_W2_A | AVR egitim | 973 / 77 | -0.37 [-1.03; +0.26] | -0.22 [-0.84; +0.36] | -0.15 [-0.64; +0.33] | +0.13 | YOK | YOK |
| C198:D1_W2_A | AVR sinama | 587 / 44 | -0.38 [-1.21; +0.40] | -0.09 [-0.81; +0.57] | -0.29 [-0.77; +0.24] | -0.09 | YOK | YOK |
| C198:D1_W2_A | BIST egitim | 469 / 71 | +1.10 [-1.04; +3.10] | +0.96 [-0.62; +2.46] | +0.14 [-1.02; +1.27] | -0.43 | YOK | YOK |
| C198:D1_W2_A | BIST sinama | 265 / 43 | +1.43 [-2.69; +5.57] | +1.17 [-1.88; +3.96] | +0.26 [-1.74; +2.11] | +0.59 | YOK | YOK |
| C198:D1_W2_B | ABD egitim | 37 / 17 | +1.62 [-3.67; +4.01] | +1.16 [-5.16; +4.09] | +0.46 [-1.51; +4.40] | +1.42 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_B | ABD sinama | 23 / 15 | +1.30 [-3.65; +5.49] | +0.94 [-0.54; +2.28] | +0.37 [-3.56; +4.01] | -0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_B | AVR egitim | 4 / 2 | +4.89 [+2.77; +5.60] | +3.50 [+2.83; +5.53] | +1.39 [-2.76; +2.77] | +1.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_B | AVR sinama | 10 / 9 | +0.99 [-5.89; +6.26] | -0.21 [-2.74; +1.52] | +1.20 [-4.20; +5.53] | +0.79 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_B | BIST egitim | 34 / 17 | -2.49 [-4.56; -0.25] | -1.39 [-3.34; +0.41] | -1.10 [-2.69; +0.95] | -1.88 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2_B | BIST sinama | 22 / 13 | +3.65 [-5.55; +11.04] | +3.35 [-3.30; +8.44] | +0.31 [-4.33; +4.11] | +0.14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_A | ABD egitim | 1752 / 77 | -0.98 [-1.81; -0.18] | -0.36 [-1.60; +0.93] | -0.62 [-1.82; +0.40] | -0.37 | YOK | YOK |
| C198:D1_W2t_A | ABD sinama | 1301 / 43 | +0.25 [-0.55; +1.07] | +0.18 [-0.89; +1.22] | +0.07 [-0.59; +0.78] | +0.23 | YOK | YOK |
| C198:D1_W2t_A | AVR egitim | 973 / 81 | -0.09 [-0.63; +0.50] | -0.15 [-0.70; +0.37] | +0.06 [-0.30; +0.44] | +0.15 | YOK | YOK |
| C198:D1_W2t_A | AVR sinama | 532 / 44 | -0.23 [-1.05; +0.66] | -0.39 [-0.97; +0.24] | +0.16 [-0.42; +0.73] | +0.37 | YOK | YOK |
| C198:D1_W2t_A | BIST egitim | 469 / 70 | -0.36 [-2.40; +1.47] | +0.91 [-0.64; +2.42] | -1.27 [-2.63; +0.01] | -1.45 | YOK | YOK |
| C198:D1_W2t_A | BIST sinama | 346 / 38 | -0.82 [-4.47; +2.58] | -0.76 [-3.17; +1.18] | -0.05 [-1.76; +2.18] | -0.02 | YOK | YOK |
| C198:D1_W2t_B | ABD egitim | 78 / 44 | +0.29 [-2.09; +2.85] | -0.40 [-1.59; +0.76] | +0.70 [-1.58; +3.01] | +0.09 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_B | ABD sinama | 102 / 35 | -0.46 [-3.40; +2.67] | -0.10 [-1.09; +1.00] | -0.37 [-2.61; +2.17] | -0.39 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_B | AVR egitim | 22 / 18 | +1.08 [-2.45; +4.54] | -0.85 [-1.66; -0.04] | +1.92 [-1.65; +5.48] | +1.95 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_B | AVR sinama | 26 / 17 | +2.43 [-2.10; +6.49] | +0.01 [-0.70; +0.58] | +2.42 [-1.73; +6.43] | +3.28 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_B | BIST egitim | 49 / 25 | -0.00 [-4.85; +6.00] | -0.70 [-2.55; +1.85] | +0.70 [-3.60; +5.79] | +1.37 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W2t_B | BIST sinama | 82 / 22 | -0.65 [-7.57; +6.22] | -0.75 [-4.62; +1.90] | +0.11 [-4.70; +5.56] | -0.13 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_A | ABD egitim | 1752 / 77 | -0.42 [-1.08; +0.22] | -0.15 [-1.18; +0.83] | -0.27 [-1.02; +0.45] | +0.14 | YOK | YOK |
| C198:D1_W3_A | ABD sinama | 1053 / 43 | -0.69 [-1.45; -0.03] | -0.09 [-1.20; +0.91] | -0.60 [-1.18; +0.02] | -0.16 | YOK | YOK |
| C198:D1_W3_A | AVR egitim | 973 / 79 | -0.21 [-0.75; +0.31] | +0.13 [-0.35; +0.63] | -0.34 [-0.70; +0.03] | -0.21 | YOK | YOK |
| C198:D1_W3_A | AVR sinama | 419 / 44 | -0.85 [-1.65; -0.01] | -0.49 [-1.24; +0.26] | -0.36 [-0.84; +0.11] | -0.10 | YOK | YOK |
| C198:D1_W3_A | BIST egitim | 469 / 63 | +0.68 [-1.42; +2.61] | +2.44 [+0.45; +4.15] | -1.76 [-2.99; -0.37] | -1.82 | YOK | YOK |
| C198:D1_W3_A | BIST sinama | 185 / 38 | -0.23 [-3.78; +3.69] | +1.06 [-1.68; +3.57] | -1.29 [-3.28; +1.24] | -0.09 | YOK | YOK |
| C198:D1_W3_B | ABD egitim | 20 / 15 | +2.53 [-0.34; +5.76] | -0.28 [-2.39; +1.60] | +2.82 [-0.82; +7.51] | +3.32 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_B | ABD sinama | 18 / 13 | -1.80 [-4.98; +1.83] | +1.80 [+0.51; +2.72] | -3.60 [-6.39; -0.10] | -1.02 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_B | AVR egitim | 7 / 6 | -0.33 [-1.50; +1.28] | +0.51 [-0.70; +1.78] | -0.84 [-1.88; +0.67] | -0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_B | AVR sinama | 9 / 7 | -1.09 [-8.05; +3.20] | +0.49 [-2.10; +2.01] | -1.58 [-8.75; +3.19] | -3.06 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_B | BIST egitim | 25 / 16 | -4.55 [-7.52; -1.54] | -0.15 [-2.78; +2.63] | -4.40 [-6.53; -2.19] | -2.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3_B | BIST sinama | 8 / 7 | -0.99 [-9.51; +6.86] | -0.23 [-4.68; +3.48] | -0.75 [-6.77; +4.09] | -1.69 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_A | ABD egitim | 1752 / 75 | -0.76 [-1.57; +0.04] | -0.18 [-1.68; +1.67] | -0.58 [-2.08; +0.55] | -0.20 | YOK | YOK |
| C198:D1_W3t_A | ABD sinama | 1154 / 44 | +0.06 [-1.00; +1.02] | +0.21 [-0.91; +1.32] | -0.15 [-0.82; +0.49] | +0.00 | YOK | YOK |
| C198:D1_W3t_A | AVR egitim | 973 / 79 | -0.74 [-1.51; -0.09] | -0.57 [-1.27; +0.04] | -0.16 [-0.64; +0.31] | -0.02 | YOK | YOK |
| C198:D1_W3t_A | AVR sinama | 612 / 44 | +0.09 [-0.69; +0.94] | -0.25 [-0.82; +0.35] | +0.34 [-0.22; +0.91] | +0.62 | YOK | YOK |
| C198:D1_W3t_A | BIST egitim | 469 / 68 | -0.34 [-2.37; +1.64] | -0.47 [-2.04; +1.09] | +0.13 [-0.86; +1.14] | -0.64 | YOK | YOK |
| C198:D1_W3t_A | BIST sinama | 402 / 39 | +0.84 [-2.67; +3.95] | +0.12 [-2.58; +2.35] | +0.72 [-1.08; +2.52] | +0.47 | YOK | YOK |
| C198:D1_W3t_B | ABD egitim | 78 / 43 | +0.53 [-1.86; +2.67] | +0.47 [-1.07; +2.01] | +0.06 [-2.25; +2.20] | -0.44 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_B | ABD sinama | 92 / 33 | +1.06 [-2.07; +4.26] | +0.84 [-0.19; +1.83] | +0.22 [-2.50; +3.24] | -0.25 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_B | AVR egitim | 21 / 16 | -1.67 [-6.33; +2.83] | -0.77 [-2.93; +1.50] | -0.90 [-5.11; +3.00] | -0.88 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_B | AVR sinama | 24 / 18 | +2.48 [-2.75; +7.80] | -0.19 [-1.34; +0.74] | +2.67 [-2.06; +7.62] | +3.02 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_B | BIST egitim | 64 / 28 | +0.40 [-2.76; +4.24] | -1.55 [-3.64; +0.58] | +1.96 [-0.70; +5.41] | +0.61 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W3t_B | BIST sinama | 98 / 21 | +3.39 [-2.90; +8.01] | +1.44 [-1.97; +3.45] | +1.95 [-2.20; +5.73] | +1.35 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_A | ABD egitim | 1756 / 77 | -0.90 [-1.63; -0.17] | -0.35 [-1.43; +0.84] | -0.55 [-1.50; +0.23] | -0.17 | YOK | YOK |
| C198:D1_W4_A | ABD sinama | 1053 / 44 | +0.02 [-0.67; +0.70] | +0.15 [-0.84; +1.10] | -0.13 [-0.68; +0.46] | -0.02 | YOK | YOK |
| C198:D1_W4_A | AVR egitim | 1180 / 80 | -0.36 [-0.94; +0.22] | -0.15 [-0.64; +0.31] | -0.20 [-0.52; +0.10] | +0.04 | YOK | YOK |
| C198:D1_W4_A | AVR sinama | 673 / 44 | -0.42 [-1.19; +0.41] | -0.28 [-0.88; +0.27] | -0.14 [-0.57; +0.33] | +0.08 | YOK | YOK |
| C198:D1_W4_A | BIST egitim | 608 / 76 | +0.73 [-1.00; +2.35] | +0.82 [-0.73; +2.39] | -0.09 [-1.24; +0.99] | -0.13 | YOK | YOK |
| C198:D1_W4_A | BIST sinama | 461 / 42 | -0.92 [-3.36; +1.51] | -0.71 [-2.85; +1.41] | -0.21 [-1.20; +0.76] | -0.15 | YOK | YOK |
| C198:D1_W4_B | ABD egitim | 59 / 35 | -0.22 [-3.07; +2.39] | -0.55 [-3.17; +1.85] | +0.34 [-2.18; +3.09] | -0.33 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_B | ABD sinama | 51 / 26 | +0.81 [-2.24; +3.37] | +1.19 [+0.27; +2.08] | -0.38 [-2.91; +1.78] | -0.34 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_B | AVR egitim | 22 / 17 | -0.36 [-3.96; +3.07] | +0.86 [-1.49; +3.08] | -1.22 [-3.57; +2.07] | -0.60 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_B | AVR sinama | 17 / 14 | +0.52 [-3.17; +5.43] | +1.01 [+0.29; +1.77] | -0.48 [-3.90; +3.93] | +0.17 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_B | BIST egitim | 45 / 24 | -2.23 [-5.32; +1.38] | -2.15 [-3.84; -0.46] | -0.09 [-2.74; +3.51] | -0.10 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4_B | BIST sinama | 68 / 23 | -0.44 [-5.55; +3.74] | +0.01 [-4.17; +3.06] | -0.45 [-2.73; +1.95] | +0.01 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_A | ABD egitim | 1450 / 76 | -0.57 [-1.20; +0.06] | -0.32 [-1.30; +0.95] | -0.24 [-1.15; +0.44] | -0.18 | YOK | YOK |
| C198:D1_W4t_A | ABD sinama | 869 / 44 | -0.05 [-0.77; +0.66] | +0.00 [-1.00; +1.06] | -0.05 [-0.78; +0.61] | +0.06 | YOK | YOK |
| C198:D1_W4t_A | AVR egitim | 986 / 78 | -0.10 [-0.60; +0.38] | -0.06 [-0.58; +0.46] | -0.04 [-0.38; +0.28] | +0.04 | YOK | YOK |
| C198:D1_W4t_A | AVR sinama | 595 / 43 | -0.39 [-1.00; +0.19] | -0.35 [-0.91; +0.21] | -0.04 [-0.54; +0.37] | +0.30 | YOK | YOK |
| C198:D1_W4t_A | BIST egitim | 469 / 71 | -0.88 [-2.58; +0.86] | +0.67 [-0.73; +2.07] | -1.55 [-2.69; -0.22] | -1.32 | YOK | YOK |
| C198:D1_W4t_A | BIST sinama | 155 / 39 | +0.81 [-3.46; +4.98] | +0.77 [-1.80; +2.98] | +0.04 [-2.62; +3.46] | +0.02 | YOK | YOK |
| C198:D1_W4t_B | ABD egitim | 29 / 26 | +1.64 [-2.05; +5.48] | -0.06 [-1.69; +1.51] | +1.70 [-2.01; +5.95] | +1.87 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_B | ABD sinama | 43 / 26 | -2.33 [-4.88; +0.80] | -0.45 [-2.26; +1.21] | -1.88 [-4.01; +0.56] | -1.14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_B | AVR egitim | 7 / 7 | +2.63 [+1.40; +4.15] | -0.08 [-1.70; +0.97] | +2.72 [+0.79; +4.69] | +1.61 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_B | AVR sinama | 13 / 11 | -1.35 [-5.08; +2.27] | -0.79 [-3.19; +0.95] | -0.56 [-3.98; +3.43] | -0.52 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_B | BIST egitim | 54 / 28 | -1.04 [-4.90; +3.18] | -0.94 [-3.08; +0.90] | -0.11 [-2.79; +3.22] | -0.84 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W4t_B | BIST sinama | 33 / 15 | +3.76 [-6.23; +12.78] | +0.84 [-3.14; +3.69] | +2.93 [-4.16; +10.49] | +1.86 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_A | ABD egitim | 1752 / 77 | -0.70 [-1.61; +0.11] | -0.49 [-1.56; +0.63] | -0.21 [-1.18; +0.62] | +0.05 | YOK | YOK |
| C198:D1_W5a_A | ABD sinama | 1327 / 44 | -0.27 [-1.09; +0.53] | -0.13 [-1.19; +0.94] | -0.13 [-0.64; +0.37] | +0.06 | YOK | YOK |
| C198:D1_W5a_A | AVR egitim | 973 / 81 | -0.10 [-0.84; +0.53] | -0.13 [-0.76; +0.45] | +0.03 [-0.39; +0.42] | +0.12 | YOK | YOK |
| C198:D1_W5a_A | AVR sinama | 575 / 43 | +0.15 [-0.68; +0.93] | -0.16 [-0.77; +0.45] | +0.31 [-0.23; +0.85] | +0.36 | YOK | YOK |
| C198:D1_W5a_A | BIST egitim | 469 / 75 | -1.05 [-2.76; +0.66] | +0.55 [-0.95; +1.99] | -1.60 [-2.70; -0.40] | -1.62 | YOK | YOK |
| C198:D1_W5a_A | BIST sinama | 309 / 41 | -1.10 [-4.16; +1.65] | -0.38 [-2.68; +1.77] | -0.72 [-1.96; +0.38] | -0.77 | YOK | YOK |
| C198:D1_W5a_B | ABD egitim | 76 / 39 | +0.19 [-2.65; +2.57] | +0.39 [-1.88; +2.50] | -0.20 [-2.31; +1.99] | -0.39 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_B | ABD sinama | 86 / 35 | +0.51 [-2.74; +4.03] | +0.04 [-1.01; +1.03] | +0.47 [-2.21; +3.46] | +0.27 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_B | AVR egitim | 16 / 12 | +1.13 [-2.35; +4.41] | +0.61 [-2.18; +3.61] | +0.52 [-1.88; +3.97] | -0.28 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_B | AVR sinama | 21 / 13 | +4.27 [+0.56; +6.81] | +0.37 [-0.80; +1.13] | +3.90 [+0.83; +6.37] | +5.06 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_B | BIST egitim | 44 / 21 | +0.18 [-3.06; +4.42] | -2.41 [-4.59; -0.23] | +2.59 [-0.56; +7.12] | +3.46 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5a_B | BIST sinama | 47 / 19 | +1.49 [-3.37; +5.14] | +0.94 [-2.15; +3.52] | +0.55 [-2.34; +3.03] | +0.85 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_A | ABD egitim | 2172 / 77 | -1.28 [-2.06; -0.53] | -0.78 [-1.60; -0.04] | -0.50 [-1.20; +0.16] | -0.30 | YOK | YOK |
| C198:D1_W5b_A | ABD sinama | 1457 / 44 | -0.53 [-1.46; +0.37] | -0.23 [-1.29; +0.82] | -0.30 [-0.91; +0.29] | -0.06 | YOK | YOK |
| C198:D1_W5b_A | AVR egitim | 1124 / 80 | -0.08 [-0.69; +0.53] | -0.20 [-0.75; +0.32] | +0.13 [-0.21; +0.44] | +0.27 | YOK | YOK |
| C198:D1_W5b_A | AVR sinama | 703 / 43 | -0.28 [-1.20; +0.62] | -0.14 [-0.91; +0.61] | -0.14 [-0.72; +0.43] | +0.10 | YOK | YOK |
| C198:D1_W5b_A | BIST egitim | 647 / 74 | +0.18 [-1.60; +2.00] | +0.64 [-0.83; +2.19] | -0.46 [-1.48; +0.55] | -1.01 | YOK | YOK |
| C198:D1_W5b_A | BIST sinama | 395 / 41 | -1.24 [-3.98; +1.61] | +0.02 [-2.63; +2.65] | -1.26 [-2.94; +0.21] | -1.02 | YOK | YOK |
| C198:D1_W5b_B | ABD egitim | 70 / 36 | +0.07 [-3.27; +3.28] | +1.07 [-0.46; +2.66] | -1.00 [-3.66; +1.75] | -0.92 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_B | ABD sinama | 58 / 27 | +1.09 [-3.04; +5.11] | +0.19 [-1.05; +1.46] | +0.90 [-2.65; +4.17] | +1.22 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_B | AVR egitim | 21 / 15 | -0.89 [-4.98; +2.56] | +0.18 [-2.25; +2.27] | -1.08 [-3.68; +1.48] | -0.92 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_B | AVR sinama | 20 / 16 | -1.62 [-5.75; +2.87] | -0.19 [-1.30; +0.57] | -1.43 [-5.69; +3.22] | -0.67 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_B | BIST egitim | 70 / 31 | -0.47 [-3.23; +3.50] | -1.71 [-3.40; +0.13] | +1.24 [-1.15; +4.70] | +0.81 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W5b_B | BIST sinama | 68 / 21 | -0.58 [-5.84; +4.02] | +0.27 [-4.80; +4.71] | -0.85 [-3.28; +1.32] | -0.92 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_A | ABD egitim | 2172 / 77 | -1.27 [-2.07; -0.51] | -0.90 [-1.71; -0.09] | -0.38 [-1.05; +0.24] | -0.16 | YOK | YOK |
| C198:D1_W6_A | ABD sinama | 1191 / 43 | -0.36 [-1.07; +0.29] | -0.17 [-1.32; +0.87] | -0.20 [-0.88; +0.54] | +0.02 | YOK | YOK |
| C198:D1_W6_A | AVR egitim | 1124 / 79 | -0.38 [-0.90; +0.10] | -0.25 [-0.72; +0.21] | -0.13 [-0.42; +0.15] | -0.01 | YOK | YOK |
| C198:D1_W6_A | AVR sinama | 571 / 44 | -0.54 [-1.23; +0.24] | -0.23 [-0.91; +0.37] | -0.31 [-0.80; +0.30] | -0.02 | YOK | YOK |
| C198:D1_W6_A | BIST egitim | 647 / 70 | +1.61 [-0.32; +3.52] | +1.69 [+0.07; +3.22] | -0.08 [-1.21; +1.04] | -0.35 | YOK | YOK |
| C198:D1_W6_A | BIST sinama | 382 / 40 | -0.79 [-3.46; +1.85] | +1.11 [-1.88; +3.87] | -1.91 [-3.35; -0.37] | -1.79 | YOK | YOK |
| C198:D1_W6_B | ABD egitim | 17 / 14 | -0.09 [-5.25; +6.62] | -2.13 [-5.18; +1.03] | +2.05 [-2.38; +7.91] | +1.95 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_B | ABD sinama | 13 / 9 | +2.06 [-3.71; +7.83] | -0.14 [-2.02; +1.90] | +2.20 [-4.00; +8.04] | +1.93 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_B | AVR egitim | 4 / 4 | -3.20 [-6.58; +2.83] | -0.59 [-0.87; -0.31] | -2.61 [-6.14; +3.65] | -5.89 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_B | AVR sinama | 4 / 4 | +2.88 [-6.12; +11.74] | +1.62 [+0.29; +2.95] | +1.26 [-6.07; +8.66] | -0.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_B | BIST egitim | 24 / 15 | +1.38 [-2.33; +5.75] | +0.28 [-2.38; +3.22] | +1.10 [-4.28; +7.05] | +3.20 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6_B | BIST sinama | 13 / 9 | +2.33 [-3.67; +6.60] | +4.65 [+0.04; +8.64] | -2.31 [-8.06; +3.00] | -0.92 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C198:D1_W6t_A | ABD egitim | 2172 / 77 | -0.71 [-1.93; +0.38] | +0.41 [-1.23; +2.13] | -1.12 [-2.40; -0.15] | -0.26 | YOK | YOK |
| C198:D1_W6t_A | ABD sinama | 1965 / 44 | -0.41 [-1.59; +0.84] | +0.19 [-0.94; +1.31] | -0.60 [-1.09; -0.07] | -0.19 | YOK | YOK |
| C198:D1_W6t_A | AVR egitim | 1124 / 80 | -0.20 [-1.09; +0.63] | -0.08 [-0.75; +0.61] | -0.13 [-0.64; +0.37] | -0.08 | YOK | YOK |
| C198:D1_W6t_A | AVR sinama | 709 / 44 | -0.69 [-1.60; +0.23] | -0.10 [-0.64; +0.43] | -0.59 [-1.21; +0.07] | -0.42 | YOK | YOK |
| C198:D1_W6t_A | BIST egitim | 647 / 77 | -1.71 [-3.31; -0.18] | +0.65 [-0.90; +2.22] | -2.36 [-3.63; -1.25] | -2.24 | YOK | YOK |
| C198:D1_W6t_A | BIST sinama | 719 / 43 | -2.36 [-5.43; +0.58] | -0.74 [-3.16; +1.55] | -1.62 [-3.08; -0.10] | -1.46 | YOK | YOK |
| C198:D1_W6t_B | ABD egitim | 256 / 56 | +0.49 [-2.82; +2.80] | +0.90 [-1.75; +3.00] | -0.42 [-1.95; +0.97] | -0.49 | YOK | YOK |
| C198:D1_W6t_B | ABD sinama | 271 / 43 | +0.39 [-1.74; +2.40] | +0.63 [-0.56; +1.75] | -0.25 [-1.74; +1.36] | -0.32 | YOK | YOK |
| C198:D1_W6t_B | AVR egitim | 59 / 29 | +0.97 [-0.82; +2.65] | +0.37 [-1.17; +1.80] | +0.60 [-1.03; +2.50] | +0.33 | YOK | YOK |
| C198:D1_W6t_B | AVR sinama | 56 / 27 | +1.20 [-2.23; +4.55] | +0.48 [-0.09; +1.02] | +0.72 [-2.55; +3.99] | +1.34 | YOK | YOK |
| C198:D1_W6t_B | BIST egitim | 120 / 43 | -1.50 [-4.19; +0.83] | -1.08 [-2.82; +0.49] | -0.42 [-2.58; +1.41] | -0.91 | YOK | YOK |
| C198:D1_W6t_B | BIST sinama | 230 / 35 | -0.89 [-5.91; +3.70] | -0.30 [-4.16; +3.00] | -0.60 [-3.00; +1.98] | -0.63 | YOK | YOK |
| C199:D2_AYK_A | ABD egitim | 2172 / 76 | -1.19 [-2.21; -0.25] | -0.06 [-1.37; +1.52] | -1.12 [-2.39; -0.11] | -0.28 | YOK | YOK |
| C199:D2_AYK_A | ABD sinama | 1797 / 44 | -0.36 [-1.56; +0.95] | +0.16 [-0.98; +1.38] | -0.51 [-1.05; -0.01] | -0.12 | YOK | YOK |
| C199:D2_AYK_A | AVR egitim | 1124 / 80 | -0.26 [-0.97; +0.43] | -0.11 [-0.67; +0.48] | -0.15 [-0.61; +0.30] | -0.09 | YOK | YOK |
| C199:D2_AYK_A | AVR sinama | 604 / 43 | -0.52 [-1.47; +0.41] | -0.07 [-0.66; +0.53] | -0.45 [-1.14; +0.19] | -0.17 | YOK | YOK |
| C199:D2_AYK_A | BIST egitim | 647 / 77 | -0.87 [-2.66; +0.93] | +0.46 [-1.28; +2.17] | -1.34 [-2.27; -0.47] | -0.50 | YOK | YOK |
| C199:D2_AYK_A | BIST sinama | 662 / 43 | -2.07 [-4.97; +1.01] | -0.82 [-3.39; +1.84] | -1.25 [-2.33; -0.06] | -1.06 | YOK | YOK |
| C199:D2_AYK_B | ABD egitim | 157 / 48 | -1.33 [-3.97; +1.13] | +0.88 [-1.08; +2.90] | -2.21 [-3.84; -0.43] | -2.35 | YOK | YOK |
| C199:D2_AYK_B | ABD sinama | 202 / 43 | +0.59 [-2.08; +2.76] | +0.28 [-0.95; +1.45] | +0.30 [-1.58; +1.96] | +0.22 | YOK | YOK |
| C199:D2_AYK_B | AVR egitim | 41 / 24 | -0.24 [-3.04; +1.95] | -0.03 [-2.02; +1.72] | -0.21 [-2.45; +1.94] | -0.78 | YOK | YOK |
| C199:D2_AYK_B | AVR sinama | 36 / 24 | +1.99 [-2.85; +6.47] | +0.36 [-0.24; +0.94] | +1.63 [-3.00; +5.90] | +1.70 | YOK | YOK |
| C199:D2_AYK_B | BIST egitim | 101 / 35 | -0.42 [-3.89; +3.23] | -1.40 [-3.27; +0.38] | +0.98 [-2.00; +4.21] | +0.91 | YOK | YOK |
| C199:D2_AYK_B | BIST sinama | 184 / 35 | -1.45 [-6.70; +3.52] | -0.36 [-4.94; +3.74] | -1.10 [-3.50; +1.94] | -0.64 | YOK | YOK |
| C199:D2_AY_A | ABD egitim | 1813 / 74 | -2.02 [-2.96; -1.06] | -0.85 [-1.62; +0.00] | -1.16 [-1.98; -0.41] | -0.62 | YOK | YOK |
| C199:D2_AY_A | ABD sinama | 1443 / 43 | -0.67 [-1.84; +0.47] | -0.12 [-1.34; +1.08] | -0.55 [-1.19; +0.01] | -0.06 | YOK | YOK |
| C199:D2_AY_A | AVR egitim | 823 / 76 | -0.57 [-1.15; -0.04] | -0.22 [-0.79; +0.32] | -0.35 [-0.72; +0.07] | -0.20 | YOK | YOK |
| C199:D2_AY_A | AVR sinama | 454 / 42 | -0.53 [-1.48; +0.51] | -0.09 [-0.85; +0.66] | -0.44 [-1.02; +0.15] | -0.36 | YOK | YOK |
| C199:D2_AY_A | BIST egitim | 465 / 70 | +0.55 [-1.59; +2.73] | +1.50 [-0.45; +3.47] | -0.95 [-2.13; +0.36] | -0.58 | YOK | YOK |
| C199:D2_AY_A | BIST sinama | 641 / 43 | -1.36 [-4.73; +2.08] | -0.25 [-2.97; +2.44] | -1.11 [-2.68; +0.31] | -0.66 | YOK | YOK |
| C199:D2_AY_B | ABD egitim | 74 / 36 | -1.87 [-6.67; +2.75] | +0.28 [-1.55; +2.12] | -2.15 [-5.97; +1.40] | -2.38 | YOK | YOK |
| C199:D2_AY_B | ABD sinama | 118 / 35 | +0.72 [-2.46; +3.66] | +0.26 [-0.82; +1.31] | +0.46 [-2.19; +2.85] | +0.22 | YOK | YOK |
| C199:D2_AY_B | AVR egitim | 10 / 9 | -2.05 [-7.14; +3.95] | -0.11 [-1.29; +1.26] | -1.94 [-6.60; +3.75] | -1.37 | YOK | YOK |
| C199:D2_AY_B | AVR sinama | 19 / 14 | +2.01 [-4.99; +8.90] | +0.32 [-0.81; +1.40] | +1.69 [-5.24; +8.71] | +1.75 | YOK | YOK |
| C199:D2_AY_B | BIST egitim | 77 / 28 | -1.52 [-3.91; +2.37] | -1.20 [-2.80; +0.85] | -0.32 [-2.40; +2.86] | -0.48 | YOK | YOK |
| C199:D2_AY_B | BIST sinama | 130 / 30 | -1.32 [-6.99; +4.26] | +0.10 [-3.87; +3.89] | -1.42 [-4.20; +1.22] | -2.13 | YOK | YOK |
| C199:D2_DT_A | ABD egitim | 1753 / 75 | -0.68 [-1.34; -0.04] | -0.28 [-1.25; +0.92] | -0.40 [-1.45; +0.48] | -0.23 | YOK | YOK |
| C199:D2_DT_A | ABD sinama | 1134 / 44 | +0.28 [-0.61; +1.16] | +0.39 [-0.81; +1.64] | -0.11 [-0.83; +0.64] | +0.21 | YOK | YOK |
| C199:D2_DT_A | AVR egitim | 1046 / 81 | -0.15 [-0.71; +0.40] | -0.14 [-0.66; +0.34] | -0.01 [-0.42; +0.40] | +0.15 | YOK | YOK |
| C199:D2_DT_A | AVR sinama | 639 / 42 | -0.25 [-1.02; +0.56] | -0.12 [-0.76; +0.53] | -0.13 [-0.50; +0.26] | +0.00 | YOK | YOK |
| C199:D2_DT_A | BIST egitim | 396 / 66 | +0.17 [-1.46; +2.01] | +1.35 [-0.09; +2.93] | -1.18 [-2.27; -0.11] | -1.15 | YOK | YOK |
| C199:D2_DT_A | BIST sinama | 190 / 36 | -1.56 [-4.75; +0.96] | -0.75 [-2.99; +1.26] | -0.81 [-2.33; +0.56] | -0.47 | YOK | YOK |
| C199:D2_DT_B | ABD egitim | 24 / 18 | -2.51 [-6.21; +2.37] | -2.03 [-5.20; +1.50] | -0.48 [-4.37; +2.92] | -0.73 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_DT_B | ABD sinama | 22 / 17 | +1.11 [-3.03; +6.78] | +0.68 [-1.33; +2.37] | +0.43 [-3.78; +7.01] | +0.91 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_DT_B | AVR egitim | 6 / 6 | +3.82 [-4.86; +11.50] | -2.65 [-4.98; -0.40] | +6.47 [-3.45; +14.20] | +6.77 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_DT_B | AVR sinama | 5 / 5 | -0.86 [-9.90; +7.59] | -0.95 [-5.39; +2.07] | +0.08 [-5.55; +6.45] | -1.59 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_DT_B | BIST egitim | 33 / 21 | -1.99 [-7.80; +4.72] | -0.59 [-3.19; +2.67] | -1.40 [-5.18; +3.61] | -1.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_DT_B | BIST sinama | 16 / 6 | +0.17 [-2.73; +2.80] | +0.29 [-4.90; +3.19] | -0.12 [-2.25; +4.68] | -0.41 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_A | ABD egitim | 1164 / 77 | -0.99 [-1.93; -0.17] | -0.92 [-2.03; +0.16] | -0.07 [-0.83; +0.62] | +0.05 | YOK | YOK |
| C199:D2_NR7_A | ABD sinama | 755 / 44 | -0.28 [-1.31; +0.72] | -0.08 [-1.14; +0.87] | -0.20 [-0.82; +0.40] | +0.28 | YOK | YOK |
| C199:D2_NR7_A | AVR egitim | 612 / 78 | -0.18 [-0.84; +0.44] | -0.10 [-0.76; +0.52] | -0.08 [-0.62; +0.49] | -0.08 | YOK | YOK |
| C199:D2_NR7_A | AVR sinama | 310 / 43 | -0.65 [-1.42; +0.19] | -0.03 [-0.55; +0.51] | -0.62 [-1.16; -0.09] | -0.44 | YOK | YOK |
| C199:D2_NR7_A | BIST egitim | 381 / 73 | +0.82 [-1.26; +2.99] | +0.76 [-0.80; +2.31] | +0.06 [-1.49; +1.59] | +0.08 | YOK | YOK |
| C199:D2_NR7_A | BIST sinama | 315 / 40 | -1.61 [-4.54; +1.48] | -0.58 [-3.20; +2.20] | -1.03 [-2.28; +0.22] | -1.17 | YOK | YOK |
| C199:D2_NR7_B | ABD egitim | 48 / 28 | -0.66 [-5.60; +3.55] | -0.09 [-3.12; +2.47] | -0.57 [-4.07; +3.28] | -0.46 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_B | ABD sinama | 63 / 31 | -0.01 [-4.15; +3.63] | +0.05 [-1.77; +1.50] | -0.06 [-2.95; +2.78] | -0.03 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_B | AVR egitim | 13 / 12 | -1.96 [-5.28; +1.91] | +2.16 [-0.58; +5.34] | -4.12 [-9.45; +0.96] | -5.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_B | AVR sinama | 6 / 6 | -0.48 [-7.12; +4.65] | -1.32 [-4.99; +1.38] | +0.83 [-2.45; +3.90] | -0.01 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_B | BIST egitim | 44 / 24 | +0.05 [-3.34; +4.19] | -1.03 [-3.08; +0.82] | +1.08 [-2.00; +5.31] | +1.29 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_NR7_B | BIST sinama | 52 / 18 | -5.08 [-10.35; +1.42] | -2.73 [-7.76; +2.91] | -2.34 [-5.06; +0.58] | -1.63 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_PP_A | ABD egitim | 4195 / 77 | -1.26 [-2.09; -0.46] | -0.24 [-1.50; +1.19] | -1.02 [-2.14; -0.15] | -0.31 | YOK | YOK |
| C199:D2_PP_A | ABD sinama | 3016 / 44 | -0.50 [-1.33; +0.32] | +0.02 [-1.07; +1.07] | -0.52 [-0.99; -0.03] | -0.21 | YOK | YOK |
| C199:D2_PP_A | AVR egitim | 2175 / 81 | -0.46 [-1.09; +0.13] | -0.27 [-0.85; +0.26] | -0.19 [-0.47; +0.09] | +0.03 | YOK | YOK |
| C199:D2_PP_A | AVR sinama | 1156 / 44 | -0.56 [-1.31; +0.27] | -0.24 [-0.85; +0.36] | -0.32 [-0.82; +0.20] | -0.06 | YOK | YOK |
| C199:D2_PP_A | BIST egitim | 2265 / 78 | +0.46 [-1.08; +2.01] | +1.31 [-0.26; +2.80] | -0.85 [-1.52; -0.18] | -0.76 | YOK | YOK |
| C199:D2_PP_A | BIST sinama | 1707 / 44 | -1.11 [-3.92; +1.63] | -0.09 [-2.49; +2.24] | -1.02 [-1.90; -0.12] | -0.92 | YOK | YOK |
| C199:D2_PP_B | ABD egitim | 150 / 51 | +0.83 [-2.71; +3.90] | +0.43 [-1.69; +2.42] | +0.40 [-2.08; +2.93] | +0.29 | YOK | YOK |
| C199:D2_PP_B | ABD sinama | 163 / 40 | +1.11 [-1.45; +3.67] | +0.65 [-0.47; +1.68] | +0.47 [-1.48; +2.44] | +0.33 | YOK | YOK |
| C199:D2_PP_B | AVR egitim | 42 / 28 | +0.46 [-2.09; +2.68] | -0.45 [-1.56; +0.65] | +0.91 [-1.07; +2.93] | +1.88 | YOK | YOK |
| C199:D2_PP_B | AVR sinama | 39 / 23 | +0.41 [-3.72; +5.08] | +0.08 [-0.72; +0.71] | +0.33 [-3.66; +4.94] | +1.28 | YOK | YOK |
| C199:D2_PP_B | BIST egitim | 208 / 52 | -1.33 [-3.86; +1.62] | -1.11 [-2.60; +0.52] | -0.22 [-2.19; +2.18] | -0.21 | YOK | YOK |
| C199:D2_PP_B | BIST sinama | 300 / 38 | -0.43 [-5.84; +3.92] | +0.02 [-4.44; +3.42] | -0.45 [-2.54; +1.49] | -0.91 | YOK | YOK |
| C199:D2_RV_A | ABD egitim | 587 / 75 | -1.41 [-2.71; -0.36] | -0.52 [-1.21; +0.17] | -0.90 [-2.11; +0.05] | -0.69 | YOK | YOK |
| C199:D2_RV_A | ABD sinama | 317 / 44 | -1.58 [-2.87; -0.36] | -0.28 [-1.40; +0.75] | -1.30 [-2.40; -0.19] | -1.24 | YOK | YOK |
| C199:D2_RV_A | AVR egitim | 585 / 74 | -0.80 [-1.80; +0.06] | -0.34 [-1.17; +0.28] | -0.45 [-0.97; +0.07] | -0.40 | YOK | YOK |
| C199:D2_RV_A | AVR sinama | 277 / 42 | -0.07 [-1.18; +1.09] | -0.51 [-1.23; +0.20] | +0.44 [-0.25; +1.14] | +0.47 | YOK | YOK |
| C199:D2_RV_A | BIST egitim | 1091 / 76 | -0.05 [-1.52; +1.44] | +0.71 [-0.62; +2.09] | -0.76 [-1.63; +0.22] | -0.86 | YOK | YOK |
| C199:D2_RV_A | BIST sinama | 532 / 43 | -2.15 [-4.91; +0.53] | -0.60 [-2.73; +1.34] | -1.55 [-2.83; -0.17] | -1.33 | YOK | YOK |
| C199:D2_RV_B | ABD egitim | 18 / 15 | -0.09 [-4.29; +3.73] | +1.18 [-0.74; +2.90] | -1.27 [-6.49; +3.48] | -0.81 | YOK | YOK |
| C199:D2_RV_B | ABD sinama | 11 / 9 | +3.33 [-3.28; +9.42] | +1.61 [-0.74; +4.54] | +1.72 [-5.60; +8.82] | +1.39 | YOK | YOK |
| C199:D2_RV_B | AVR egitim | 12 / 10 | +0.02 [-4.24; +4.72] | +0.25 [-1.36; +2.00] | -0.22 [-3.46; +3.40] | +1.92 | YOK | YOK |
| C199:D2_RV_B | AVR sinama | 5 / 5 | -6.55 [-16.77; +2.32] | -0.05 [-0.74; +0.74] | -6.51 [-16.68; +2.27] | -4.51 | YOK | YOK |
| C199:D2_RV_B | BIST egitim | 112 / 45 | -2.54 [-5.56; +0.64] | -1.57 [-3.10; +0.03] | -0.97 [-3.27; +1.43] | -0.82 | YOK | YOK |
| C199:D2_RV_B | BIST sinama | 106 / 28 | -2.37 [-7.92; +2.81] | -1.45 [-4.79; +1.43] | -0.92 [-4.80; +2.68] | -1.44 | YOK | YOK |
| C199:D2_VCP_A | ABD egitim | 24 / 20 | -0.39 [-3.83; +3.18] | -0.72 [-2.54; +1.11] | +0.33 [-2.54; +3.23] | +0.13 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_A | ABD sinama | 20 / 15 | -1.17 [-6.28; +4.09] | -0.28 [-2.58; +1.64] | -0.90 [-5.07; +4.31] | +1.36 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_A | AVR egitim | 12 / 12 | -1.33 [-4.42; +2.20] | -0.75 [-3.47; +2.21] | -0.58 [-3.87; +2.66] | -1.39 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_A | AVR sinama | 4 / 4 | -8.87 [-13.92; -3.82] | +0.05 [-3.23; +1.90] | -8.92 [-12.66; -5.41] | -9.95 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_A | BIST egitim | 9 / 9 | +8.88 [+0.45; +18.74] | +3.84 [-0.14; +8.56] | +5.05 [-1.64; +13.20] | +0.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_A | BIST sinama | 14 / 8 | -2.03 [-11.79; +6.92] | +0.66 [-4.98; +6.00] | -2.69 [-7.88; +2.47] | -0.98 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_VCP_B | ABD sinama | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_A | ABD egitim | 1978 / 75 | -1.01 [-1.78; -0.36] | -0.60 [-1.56; +0.34] | -0.40 [-1.28; +0.32] | -0.16 | YOK | YOK |
| C199:D2_W1_A | ABD sinama | 1305 / 44 | +0.28 [-0.72; +1.17] | +0.55 [-0.65; +1.59] | -0.27 [-0.72; +0.32] | +0.51 | YOK | YOK |
| C199:D2_W1_A | AVR egitim | 1060 / 78 | -0.32 [-0.97; +0.25] | -0.11 [-0.61; +0.35] | -0.21 [-0.62; +0.18] | -0.18 | YOK | YOK |
| C199:D2_W1_A | AVR sinama | 515 / 44 | -0.36 [-1.24; +0.58] | -0.21 [-0.94; +0.57] | -0.15 [-0.70; +0.36] | -0.09 | YOK | YOK |
| C199:D2_W1_A | BIST egitim | 572 / 73 | +0.81 [-1.25; +3.01] | +1.38 [-0.24; +2.98] | -0.56 [-1.68; +0.70] | -0.51 | YOK | YOK |
| C199:D2_W1_A | BIST sinama | 426 / 42 | -2.12 [-5.91; +1.39] | -0.23 [-3.85; +3.15] | -1.89 [-3.08; -0.58] | -1.76 | YOK | YOK |
| C199:D2_W1_B | ABD egitim | 53 / 33 | +0.61 [-2.29; +3.06] | +0.10 [-1.90; +1.96] | +0.51 [-1.89; +2.99] | +0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_B | ABD sinama | 59 / 26 | -0.09 [-4.20; +4.33] | +1.05 [-0.16; +2.14] | -1.14 [-4.68; +2.97] | -0.34 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_B | AVR egitim | 15 / 14 | -0.07 [-4.35; +3.38] | +0.26 [-0.68; +1.17] | -0.33 [-4.52; +3.22] | +0.66 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_B | AVR sinama | 6 / 6 | +1.51 [-4.01; +7.32] | -0.01 [-1.56; +1.66] | +1.52 [-2.89; +5.93] | +1.70 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_B | BIST egitim | 56 / 31 | -2.66 [-5.58; +0.65] | -1.27 [-3.03; +0.83] | -1.40 [-3.79; +1.57] | -0.87 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W1_B | BIST sinama | 85 / 24 | -0.90 [-6.19; +4.22] | +0.09 [-5.38; +5.02] | -0.99 [-2.50; +0.79] | -0.75 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_A | ABD egitim | 1752 / 73 | -0.93 [-1.74; -0.09] | -0.25 [-1.72; +1.33] | -0.68 [-2.13; +0.55] | -0.46 | YOK | YOK |
| C199:D2_W2D_A | ABD sinama | 1181 / 43 | +0.29 [-0.65; +1.22] | +0.30 [-0.89; +1.39] | -0.01 [-0.79; +0.94] | +0.27 | YOK | YOK |
| C199:D2_W2D_A | AVR egitim | 973 / 79 | -0.34 [-0.93; +0.21] | -0.15 [-0.67; +0.33] | -0.19 [-0.59; +0.23] | -0.05 | YOK | YOK |
| C199:D2_W2D_A | AVR sinama | 545 / 44 | -0.60 [-1.46; +0.25] | -0.52 [-1.08; +0.08] | -0.09 [-0.74; +0.52] | +0.11 | YOK | YOK |
| C199:D2_W2D_A | BIST egitim | 469 / 69 | -0.31 [-2.18; +1.32] | +1.11 [-0.40; +2.50] | -1.42 [-2.66; -0.09] | -1.91 | YOK | YOK |
| C199:D2_W2D_A | BIST sinama | 310 / 37 | -1.13 [-5.11; +2.04] | -0.75 [-3.17; +1.26] | -0.39 [-2.43; +1.66] | -0.59 | YOK | YOK |
| C199:D2_W2D_B | ABD egitim | 51 / 31 | -0.36 [-3.82; +3.28] | -0.77 [-2.32; +0.88] | +0.41 [-2.53; +3.59] | -0.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_B | ABD sinama | 70 / 27 | -0.32 [-4.83; +3.99] | -0.11 [-1.43; +1.12] | -0.21 [-3.71; +3.62] | -0.32 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_B | AVR egitim | 15 / 11 | +0.38 [-4.00; +4.43] | -1.17 [-2.07; -0.29] | +1.55 [-2.67; +5.56] | +1.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_B | AVR sinama | 22 / 15 | +3.78 [-0.94; +8.93] | +0.14 [-0.61; +0.78] | +3.64 [-0.81; +8.88] | +4.82 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_B | BIST egitim | 43 / 23 | +1.39 [-3.86; +7.16] | -0.61 [-3.10; +2.17] | +1.99 [-3.26; +8.30] | +1.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2D_B | BIST sinama | 63 / 19 | +0.61 [-7.42; +8.28] | -0.01 [-3.61; +2.32] | +0.62 [-5.19; +7.10] | +0.47 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_A | ABD egitim | 1752 / 77 | -0.41 [-1.21; +0.31] | +0.01 [-1.21; +1.22] | -0.42 [-1.17; +0.22] | +0.06 | YOK | YOK |
| C199:D2_W2_A | ABD sinama | 1253 / 44 | -0.35 [-1.31; +0.59] | -0.02 [-1.21; +1.12] | -0.33 [-0.80; +0.13] | -0.06 | YOK | YOK |
| C199:D2_W2_A | AVR egitim | 973 / 77 | -0.37 [-1.03; +0.26] | -0.22 [-0.84; +0.36] | -0.15 [-0.64; +0.33] | +0.13 | YOK | YOK |
| C199:D2_W2_A | AVR sinama | 587 / 44 | -0.38 [-1.21; +0.40] | -0.09 [-0.81; +0.57] | -0.29 [-0.77; +0.24] | -0.09 | YOK | YOK |
| C199:D2_W2_A | BIST egitim | 469 / 71 | +1.10 [-1.04; +3.10] | +0.96 [-0.62; +2.46] | +0.14 [-1.02; +1.27] | -0.43 | YOK | YOK |
| C199:D2_W2_A | BIST sinama | 265 / 43 | +1.43 [-2.69; +5.57] | +1.17 [-1.88; +3.96] | +0.26 [-1.74; +2.11] | +0.59 | YOK | YOK |
| C199:D2_W2_B | ABD egitim | 37 / 17 | +1.62 [-3.67; +4.01] | +1.16 [-5.16; +4.09] | +0.46 [-1.51; +4.40] | +1.42 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_B | ABD sinama | 23 / 15 | +1.30 [-3.65; +5.49] | +0.94 [-0.54; +2.28] | +0.37 [-3.56; +4.01] | -0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_B | AVR egitim | 4 / 2 | +4.89 [+2.77; +5.60] | +3.50 [+2.83; +5.53] | +1.39 [-2.76; +2.77] | +1.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_B | AVR sinama | 10 / 9 | +0.99 [-5.89; +6.26] | -0.21 [-2.74; +1.52] | +1.20 [-4.20; +5.53] | +0.79 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_B | BIST egitim | 34 / 17 | -2.49 [-4.56; -0.25] | -1.39 [-3.34; +0.41] | -1.10 [-2.69; +0.95] | -1.88 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C199:D2_W2_B | BIST sinama | 22 / 13 | +3.65 [-5.55; +11.04] | +3.35 [-3.30; +8.44] | +0.31 [-4.33; +4.11] | +0.14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_AYK_A | ABD egitim | 2172 / 76 | -1.19 [-2.21; -0.25] | -0.06 [-1.37; +1.52] | -1.12 [-2.39; -0.11] | -0.28 | YOK | YOK |
| C200:D3_AYK_A | ABD sinama | 1797 / 44 | -0.36 [-1.56; +0.95] | +0.16 [-0.98; +1.38] | -0.51 [-1.05; -0.01] | -0.12 | YOK | YOK |
| C200:D3_AYK_A | AVR egitim | 1124 / 80 | -0.26 [-0.97; +0.43] | -0.11 [-0.67; +0.48] | -0.15 [-0.61; +0.30] | -0.09 | YOK | YOK |
| C200:D3_AYK_A | AVR sinama | 604 / 43 | -0.52 [-1.47; +0.41] | -0.07 [-0.66; +0.53] | -0.45 [-1.14; +0.19] | -0.17 | YOK | YOK |
| C200:D3_AYK_A | BIST egitim | 647 / 77 | -0.87 [-2.66; +0.93] | +0.46 [-1.28; +2.17] | -1.34 [-2.27; -0.47] | -0.50 | YOK | YOK |
| C200:D3_AYK_A | BIST sinama | 662 / 43 | -2.07 [-4.97; +1.01] | -0.82 [-3.39; +1.84] | -1.25 [-2.33; -0.06] | -1.06 | YOK | YOK |
| C200:D3_AYK_B | ABD egitim | 157 / 48 | -1.33 [-3.97; +1.13] | +0.88 [-1.08; +2.90] | -2.21 [-3.84; -0.43] | -2.35 | YOK | YOK |
| C200:D3_AYK_B | ABD sinama | 202 / 43 | +0.59 [-2.08; +2.76] | +0.28 [-0.95; +1.45] | +0.30 [-1.58; +1.96] | +0.22 | YOK | YOK |
| C200:D3_AYK_B | AVR egitim | 41 / 24 | -0.24 [-3.04; +1.95] | -0.03 [-2.02; +1.72] | -0.21 [-2.45; +1.94] | -0.78 | YOK | YOK |
| C200:D3_AYK_B | AVR sinama | 36 / 24 | +1.99 [-2.85; +6.47] | +0.36 [-0.24; +0.94] | +1.63 [-3.00; +5.90] | +1.70 | YOK | YOK |
| C200:D3_AYK_B | BIST egitim | 101 / 35 | -0.42 [-3.89; +3.23] | -1.40 [-3.27; +0.38] | +0.98 [-2.00; +4.21] | +0.91 | YOK | YOK |
| C200:D3_AYK_B | BIST sinama | 184 / 35 | -1.45 [-6.70; +3.52] | -0.36 [-4.94; +3.74] | -1.10 [-3.50; +1.94] | -0.64 | YOK | YOK |
| C200:D3_NR7_A | ABD egitim | 1164 / 77 | -0.99 [-1.93; -0.17] | -0.92 [-2.03; +0.16] | -0.07 [-0.83; +0.62] | +0.05 | YOK | YOK |
| C200:D3_NR7_A | ABD sinama | 755 / 44 | -0.28 [-1.31; +0.72] | -0.08 [-1.14; +0.87] | -0.20 [-0.82; +0.40] | +0.28 | YOK | YOK |
| C200:D3_NR7_A | AVR egitim | 612 / 78 | -0.18 [-0.84; +0.44] | -0.10 [-0.76; +0.52] | -0.08 [-0.62; +0.49] | -0.08 | YOK | YOK |
| C200:D3_NR7_A | AVR sinama | 310 / 43 | -0.65 [-1.42; +0.19] | -0.03 [-0.55; +0.51] | -0.62 [-1.16; -0.09] | -0.44 | YOK | YOK |
| C200:D3_NR7_A | BIST egitim | 381 / 73 | +0.82 [-1.26; +2.99] | +0.76 [-0.80; +2.31] | +0.06 [-1.49; +1.59] | +0.08 | YOK | YOK |
| C200:D3_NR7_A | BIST sinama | 315 / 40 | -1.61 [-4.54; +1.48] | -0.58 [-3.20; +2.20] | -1.03 [-2.28; +0.22] | -1.17 | YOK | YOK |
| C200:D3_NR7_B | ABD egitim | 48 / 28 | -0.66 [-5.60; +3.55] | -0.09 [-3.12; +2.47] | -0.57 [-4.07; +3.28] | -0.46 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_NR7_B | ABD sinama | 63 / 31 | -0.01 [-4.15; +3.63] | +0.05 [-1.77; +1.50] | -0.06 [-2.95; +2.78] | -0.03 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_NR7_B | AVR egitim | 13 / 12 | -1.96 [-5.28; +1.91] | +2.16 [-0.58; +5.34] | -4.12 [-9.45; +0.96] | -5.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_NR7_B | AVR sinama | 6 / 6 | -0.48 [-7.12; +4.65] | -1.32 [-4.99; +1.38] | +0.83 [-2.45; +3.90] | -0.01 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_NR7_B | BIST egitim | 44 / 24 | +0.05 [-3.34; +4.19] | -1.03 [-3.08; +0.82] | +1.08 [-2.00; +5.31] | +1.29 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_NR7_B | BIST sinama | 52 / 18 | -5.08 [-10.35; +1.42] | -2.73 [-7.76; +2.91] | -2.34 [-5.06; +0.58] | -1.63 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_A | ABD egitim | 1978 / 75 | -1.01 [-1.78; -0.36] | -0.60 [-1.56; +0.34] | -0.40 [-1.28; +0.32] | -0.16 | YOK | YOK |
| C200:D3_W1_A | ABD sinama | 1305 / 44 | +0.28 [-0.72; +1.17] | +0.55 [-0.65; +1.59] | -0.27 [-0.72; +0.32] | +0.51 | YOK | YOK |
| C200:D3_W1_A | AVR egitim | 1060 / 78 | -0.32 [-0.97; +0.25] | -0.11 [-0.61; +0.35] | -0.21 [-0.62; +0.18] | -0.18 | YOK | YOK |
| C200:D3_W1_A | AVR sinama | 515 / 44 | -0.36 [-1.24; +0.58] | -0.21 [-0.94; +0.57] | -0.15 [-0.70; +0.36] | -0.09 | YOK | YOK |
| C200:D3_W1_A | BIST egitim | 572 / 73 | +0.81 [-1.25; +3.01] | +1.38 [-0.24; +2.98] | -0.56 [-1.68; +0.70] | -0.51 | YOK | YOK |
| C200:D3_W1_A | BIST sinama | 426 / 42 | -2.12 [-5.91; +1.39] | -0.23 [-3.85; +3.15] | -1.89 [-3.08; -0.58] | -1.76 | YOK | YOK |
| C200:D3_W1_B | ABD egitim | 53 / 33 | +0.61 [-2.29; +3.06] | +0.10 [-1.90; +1.96] | +0.51 [-1.89; +2.99] | +0.30 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_B | ABD sinama | 59 / 26 | -0.09 [-4.20; +4.33] | +1.05 [-0.16; +2.14] | -1.14 [-4.68; +2.97] | -0.34 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_B | AVR egitim | 15 / 14 | -0.07 [-4.35; +3.38] | +0.26 [-0.68; +1.17] | -0.33 [-4.52; +3.22] | +0.66 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_B | AVR sinama | 6 / 6 | +1.51 [-4.01; +7.32] | -0.01 [-1.56; +1.66] | +1.52 [-2.89; +5.93] | +1.70 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_B | BIST egitim | 56 / 31 | -2.66 [-5.58; +0.65] | -1.27 [-3.03; +0.83] | -1.40 [-3.79; +1.57] | -0.87 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W1_B | BIST sinama | 85 / 24 | -0.90 [-6.19; +4.22] | +0.09 [-5.38; +5.02] | -0.99 [-2.50; +0.79] | -0.75 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_A | ABD egitim | 1752 / 73 | -0.93 [-1.74; -0.09] | -0.25 [-1.72; +1.33] | -0.68 [-2.13; +0.55] | -0.46 | YOK | YOK |
| C200:D3_W2D_A | ABD sinama | 1181 / 43 | +0.29 [-0.65; +1.22] | +0.30 [-0.89; +1.39] | -0.01 [-0.79; +0.94] | +0.27 | YOK | YOK |
| C200:D3_W2D_A | AVR egitim | 973 / 79 | -0.34 [-0.93; +0.21] | -0.15 [-0.67; +0.33] | -0.19 [-0.59; +0.23] | -0.05 | YOK | YOK |
| C200:D3_W2D_A | AVR sinama | 545 / 44 | -0.60 [-1.46; +0.25] | -0.52 [-1.08; +0.08] | -0.09 [-0.74; +0.52] | +0.11 | YOK | YOK |
| C200:D3_W2D_A | BIST egitim | 469 / 69 | -0.31 [-2.18; +1.32] | +1.11 [-0.40; +2.50] | -1.42 [-2.66; -0.09] | -1.91 | YOK | YOK |
| C200:D3_W2D_A | BIST sinama | 310 / 37 | -1.13 [-5.11; +2.04] | -0.75 [-3.17; +1.26] | -0.39 [-2.43; +1.66] | -0.59 | YOK | YOK |
| C200:D3_W2D_B | ABD egitim | 51 / 31 | -0.36 [-3.82; +3.28] | -0.77 [-2.32; +0.88] | +0.41 [-2.53; +3.59] | -0.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_B | ABD sinama | 70 / 27 | -0.32 [-4.83; +3.99] | -0.11 [-1.43; +1.12] | -0.21 [-3.71; +3.62] | -0.32 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_B | AVR egitim | 15 / 11 | +0.38 [-4.00; +4.43] | -1.17 [-2.07; -0.29] | +1.55 [-2.67; +5.56] | +1.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_B | AVR sinama | 22 / 15 | +3.78 [-0.94; +8.93] | +0.14 [-0.61; +0.78] | +3.64 [-0.81; +8.88] | +4.82 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_B | BIST egitim | 43 / 23 | +1.39 [-3.86; +7.16] | -0.61 [-3.10; +2.17] | +1.99 [-3.26; +8.30] | +1.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C200:D3_W2D_B | BIST sinama | 63 / 19 | +0.61 [-7.42; +8.28] | -0.01 [-3.61; +2.32] | +0.62 [-5.19; +7.10] | +0.47 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C201:Y13 | ABD egitim | 712 / 76 | -0.28 [-1.57; +0.85] | -0.28 [-1.94; +1.22] | -0.00 [-0.95; +0.91] | -0.26 | YOK | YOK |
| C201:Y13 | ABD sinama | 606 / 44 | -0.39 [-1.54; +0.75] | -0.27 [-1.28; +0.69] | -0.12 [-1.00; +0.79] | -0.26 | YOK | YOK |
| C201:Y13 | AVR egitim | 360 / 76 | +0.35 [-0.52; +1.12] | -0.10 [-0.90; +0.66] | +0.45 [-0.31; +1.24] | +0.21 | YOK | YOK |
| C201:Y13 | AVR sinama | 234 / 43 | -0.06 [-0.97; +0.94] | -0.32 [-0.87; +0.24] | +0.26 [-0.56; +1.12] | +0.21 | YOK | YOK |
| C201:Y13 | BIST egitim | 312 / 64 | -0.66 [-2.96; +1.64] | -0.23 [-1.82; +1.40] | -0.43 [-1.84; +1.09] | -0.01 | YOK | YOK |
| C201:Y13 | BIST sinama | 345 / 37 | -2.12 [-5.71; +0.96] | -0.99 [-4.11; +1.82] | -1.13 [-2.51; +0.05] | -1.32 | YOK | YOK |
| C201:Y13b | ABD egitim | 123 / 46 | +1.21 [-1.91; +3.33] | +1.21 [-1.31; +3.14] | +0.00 [-1.65; +1.85] | -0.40 | YOK | YOK |
| C201:Y13b | ABD sinama | 131 / 41 | -0.52 [-3.32; +2.36] | +0.25 [-0.76; +1.29] | -0.77 [-2.93; +1.53] | -0.38 | YOK | YOK |
| C201:Y13b | AVR egitim | 28 / 20 | +2.11 [-1.52; +5.25] | -0.42 [-2.49; +1.16] | +2.53 [-0.12; +5.27] | +2.25 | YOK | YOK |
| C201:Y13b | AVR sinama | 24 / 17 | +2.89 [-0.99; +7.60] | +0.37 [-0.26; +1.13] | +2.52 [-0.96; +6.66] | +3.22 | YOK | YOK |
| C201:Y13b | BIST egitim | 98 / 35 | -0.79 [-5.00; +4.33] | -1.32 [-3.09; +0.56] | +0.53 [-2.87; +4.91] | +0.56 | YOK | YOK |
| C201:Y13b | BIST sinama | 150 / 30 | -1.48 [-6.30; +2.84] | -0.93 [-5.33; +2.88] | -0.54 [-2.70; +1.13] | -0.73 | YOK | YOK |
| C201:Y13c | ABD egitim | 685 / 74 | -0.20 [-1.51; +1.01] | -0.25 [-1.96; +1.35] | +0.05 [-0.95; +1.02] | -0.23 | YOK | YOK |
| C201:Y13c | ABD sinama | 590 / 44 | -0.34 [-1.46; +0.77] | -0.26 [-1.26; +0.70] | -0.09 [-0.95; +0.80] | -0.22 | YOK | YOK |
| C201:Y13c | AVR egitim | 346 / 75 | +0.40 [-0.46; +1.21] | -0.08 [-0.90; +0.69] | +0.48 [-0.29; +1.28] | +0.23 | YOK | YOK |
| C201:Y13c | AVR sinama | 231 / 43 | +0.04 [-0.90; +1.07] | -0.36 [-0.91; +0.19] | +0.40 [-0.41; +1.26] | +0.31 | YOK | YOK |
| C201:Y13c | BIST egitim | 310 / 64 | -0.72 [-2.96; +1.57] | -0.24 [-1.83; +1.39] | -0.48 [-1.88; +1.02] | -0.08 | YOK | YOK |
| C201:Y13c | BIST sinama | 343 / 37 | -2.01 [-5.59; +1.06] | -0.98 [-4.11; +1.84] | -1.03 [-2.35; +0.15] | -1.18 | YOK | YOK |
| C202:DS01 | ABD egitim | 2813 / 84 | +0.08 [-3.63; +4.03] | +0.36 [-2.65; +3.85] | -0.28 [-1.93; +1.04] | +0.24 | YOK | YOK |
| C202:DS01 | ABD sinama | 1680 / 41 | +1.99 [-0.72; +4.36] | +1.69 [-0.27; +3.54] | +0.30 [-1.08; +1.67] | +0.77 | YOK | YOK |
| C202:DS01 | AVR egitim | 913 / 79 | +0.95 [-2.07; +4.47] | +0.77 [-1.55; +3.41] | +0.19 [-0.96; +1.19] | -0.23 | YOK | YOK |
| C202:DS01 | AVR sinama | 285 / 41 | +2.06 [+0.04; +3.94] | +1.05 [-0.28; +2.59] | +1.00 [-0.12; +2.10] | -0.35 | YOK | YOK |
| C202:DS01 | BIST egitim | 590 / 68 | -0.83 [-3.24; +1.24] | +1.51 [-1.11; +4.25] | -2.34 [-3.85; -0.90] | -0.52 | YOK | YOK |
| C202:DS01 | BIST sinama | 871 / 42 | +0.18 [-3.26; +3.31] | +2.09 [-0.99; +4.92] | -1.90 [-3.20; -0.85] | -0.36 | YOK | YOK |
| C202:DS02 | ABD egitim | 1253 / 76 | -0.51 [-2.83; +1.91] | -0.20 [-2.01; +1.66] | -0.31 [-1.68; +0.85] | -0.12 | YOK | YOK |
| C202:DS02 | ABD sinama | 819 / 42 | -0.27 [-2.71; +1.93] | +0.75 [-0.19; +1.57] | -1.02 [-3.10; +0.81] | +0.42 | YOK | YOK |
| C202:DS02 | AVR egitim | 449 / 71 | +0.55 [-1.43; +2.99] | +0.27 [-1.24; +1.96] | +0.27 [-0.74; +1.53] | -0.01 | YOK | YOK |
| C202:DS02 | AVR sinama | 131 / 38 | +1.81 [-0.59; +4.25] | +0.25 [-0.62; +1.08] | +1.57 [-0.34; +3.63] | +0.53 | YOK | YOK |
| C202:DS02 | BIST egitim | 283 / 27 | -1.95 [-3.82; +0.41] | -2.80 [-4.46; -0.51] | +0.85 [-0.16; +2.28] | +0.45 | YOK | YOK |
| C202:DS02 | BIST sinama | 191 / 21 | +2.93 [-2.01; +6.94] | +2.97 [-1.64; +7.03] | -0.04 [-1.62; +1.43] | -0.56 | YOK | YOK |
| C202:DS03 | ABD egitim | 1407 / 84 | +0.04 [-2.96; +3.08] | +0.51 [-1.12; +2.27] | -0.47 [-2.19; +1.33] | -0.02 | YOK | YOK |
| C202:DS03 | ABD sinama | 1556 / 42 | -0.03 [-1.60; +1.56] | +0.19 [-0.85; +1.15] | -0.22 [-1.23; +0.74] | +0.43 | YOK | YOK |
| C202:DS03 | AVR egitim | 457 / 77 | +3.68 [+1.30; +5.99] | +1.60 [+0.31; +2.69] | +2.08 [+0.71; +3.63] | +1.12 | YOK | YOK |
| C202:DS03 | AVR sinama | 305 / 42 | +1.01 [-0.44; +2.34] | +0.15 [-0.55; +0.84] | +0.86 [-0.45; +2.10] | +0.11 | YOK | YOK |
| C202:DS03 | BIST egitim | 295 / 69 | -3.33 [-6.17; -0.48] | +0.26 [-1.73; +2.25] | -3.59 [-5.77; -1.46] | -1.30 | YOK | YOK |
| C202:DS03 | BIST sinama | 431 / 41 | -3.93 [-5.69; -2.07] | +0.56 [-1.18; +2.40] | -4.49 [-6.05; -2.85] | -1.33 | YOK | YOK |
| C202:DS04 | ABD egitim | 1604 / 82 | +3.43 [-2.66; +7.32] | +3.68 [-1.03; +6.93] | -0.25 [-2.03; +0.91] | +0.12 | YOK | YOK |
| C202:DS04 | ABD sinama | 1082 / 42 | +0.44 [-2.73; +3.33] | +0.51 [-1.41; +2.30] | -0.07 [-1.64; +1.42] | +0.41 | YOK | YOK |
| C202:DS04 | AVR egitim | 319 / 66 | +3.74 [+0.09; +5.39] | +3.20 [-0.21; +4.81] | +0.54 [-0.55; +1.91] | -0.02 | YOK | YOK |
| C202:DS04 | AVR sinama | 181 / 39 | +0.85 [-1.14; +2.63] | +0.40 [-0.61; +1.32] | +0.45 [-1.54; +2.26] | -0.22 | YOK | YOK |
| C202:DS04 | BIST egitim | 159 / 54 | +2.93 [-7.17; +11.94] | +4.58 [-2.31; +10.82] | -1.65 [-5.96; +2.03] | +0.89 | YOK | YOK |
| C202:DS04 | BIST sinama | 77 / 30 | -1.73 [-6.47; +3.41] | +1.88 [-0.56; +4.14] | -3.61 [-8.38; +1.78] | +0.32 | YOK | YOK |
| C202:DS05 | ABD egitim | 5721 / 84 | +1.12 [-1.31; +3.99] | +0.92 [-1.00; +3.10] | +0.19 [-0.74; +1.43] | -0.09 | YOK | YOK |
| C202:DS05 | ABD sinama | 4274 / 42 | +0.83 [-1.21; +2.84] | +0.92 [-0.68; +2.53] | -0.08 [-0.73; +0.54] | -0.29 | YOK | YOK |
| C202:DS05 | AVR egitim | 2058 / 84 | +1.85 [-0.33; +4.36] | +1.13 [-0.40; +2.74] | +0.72 [-0.11; +1.90] | -0.05 | YOK | YOK |
| C202:DS05 | AVR sinama | 902 / 42 | +1.77 [+0.35; +3.09] | +0.78 [-0.23; +1.85] | +0.99 [+0.14; +1.80] | +0.25 | YOK | YOK |
| C202:DS05 | BIST egitim | 876 / 80 | -2.10 [-4.13; +0.15] | +0.22 [-1.73; +2.59] | -2.32 [-3.22; -1.39] | -0.28 | YOK | YOK |
| C202:DS05 | BIST sinama | 1299 / 42 | -0.47 [-2.98; +1.98] | +0.61 [-1.64; +2.82] | -1.08 [-2.01; -0.35] | +0.02 | YOK | YOK |
| C202:DS06 | ABD egitim | 351 / 73 | +1.44 [-1.50; +4.61] | +0.21 [-1.73; +2.40] | +1.23 [-0.30; +2.80] | +0.92 | YOK | YOK |
| C202:DS06 | ABD sinama | 239 / 42 | +0.86 [-1.78; +3.40] | +0.81 [-0.61; +2.10] | +0.04 [-1.87; +1.82] | +0.21 | YOK | YOK |
| C202:DS06 | AVR egitim | 97 / 38 | +2.87 [-1.54; +6.93] | +1.05 [-1.33; +3.42] | +1.82 [-0.79; +3.97] | +0.06 | YOK | YOK |
| C202:DS06 | AVR sinama | 38 / 23 | +1.63 [-1.01; +4.28] | +0.54 [-0.51; +1.88] | +1.08 [-0.97; +3.33] | +0.81 | YOK | YOK |
| C202:DS06 | BIST egitim | 54 / 31 | -1.50 [-5.11; +2.34] | +0.98 [-1.50; +4.14] | -2.48 [-5.35; -0.13] | -2.48 | YOK | YOK |
| C202:DS06 | BIST sinama | 108 / 30 | -0.09 [-3.06; +3.23] | -0.16 [-2.49; +2.36] | +0.08 [-1.92; +2.05] | -0.02 | YOK | YOK |
| C202:DS07 | ABD egitim | 416 / 70 | +0.17 [-3.33; +3.29] | +1.56 [-0.97; +4.18] | -1.39 [-4.36; +1.05] | -0.33 | YOK | YOK |
| C202:DS07 | ABD sinama | 327 / 39 | +2.39 [-0.27; +4.74] | +1.35 [-0.19; +2.76] | +1.03 [-0.60; +2.63] | +0.88 | YOK | YOK |
| C202:DS07 | AVR egitim | 130 / 41 | +3.02 [+0.34; +5.53] | +1.41 [-0.17; +2.89] | +1.61 [-0.23; +3.47] | +1.25 | YOK | YOK |
| C202:DS07 | AVR sinama | 63 / 29 | +0.71 [-2.26; +3.34] | +1.54 [+0.03; +3.54] | -0.83 [-3.56; +2.08] | -1.59 | YOK | YOK |
| C202:DS07 | BIST egitim | 55 / 28 | -3.33 [-5.92; -0.21] | -0.33 [-2.39; +2.46] | -3.00 [-5.83; -0.74] | -0.03 | YOK | YOK |
| C202:DS07 | BIST sinama | 157 / 34 | +0.63 [-3.23; +4.50] | +1.69 [-1.50; +5.46] | -1.06 [-2.90; +0.86] | -0.76 | YOK | YOK |
| C202:DS08 | ABD egitim | 11096 / 83 | +0.72 [-1.65; +3.19] | +0.85 [-0.99; +2.70] | -0.13 [-1.05; +0.86] | -0.14 | YOK | YOK |
| C202:DS08 | ABD sinama | 7734 / 42 | +0.88 [-0.86; +2.60] | +0.84 [-0.59; +2.26] | +0.04 [-0.65; +0.72] | -0.23 | YOK | YOK |
| C202:DS08 | AVR egitim | 4092 / 84 | +1.78 [-0.23; +3.97] | +0.83 [-0.53; +2.29] | +0.94 [+0.17; +1.89] | +0.36 | YOK | YOK |
| C202:DS08 | AVR sinama | 1725 / 42 | +1.72 [+0.52; +2.86] | +0.56 [-0.29; +1.48] | +1.16 [+0.50; +1.75] | +0.31 | YOK | YOK |
| C202:DS08 | BIST egitim | 1701 / 74 | -1.70 [-3.13; -0.23] | -0.58 [-1.99; +1.16] | -1.12 [-1.99; -0.40] | -0.08 | YOK | YOK |
| C202:DS08 | BIST sinama | 3339 / 42 | +1.26 [-1.40; +3.81] | +1.13 [-1.33; +3.52] | +0.13 [-0.42; +0.61] | +0.25 | YOK | YOK |
| C202:DS09 | ABD egitim | 3450 / 84 | -0.90 [-3.80; +2.00] | -0.64 [-3.31; +2.24] | -0.26 [-1.42; +0.83] | +0.00 | YOK | YOK |
| C202:DS09 | ABD sinama | 2330 / 42 | +1.67 [-0.04; +3.36] | +1.25 [-0.45; +2.97] | +0.42 [-0.34; +1.12] | +0.42 | YOK | YOK |
| C202:DS09 | AVR egitim | 1322 / 80 | -0.12 [-2.47; +3.28] | -0.46 [-2.30; +2.14] | +0.34 [-0.34; +1.37] | -0.35 | YOK | YOK |
| C202:DS09 | AVR sinama | 525 / 41 | +2.41 [+0.55; +4.11] | +1.20 [-0.11; +2.74] | +1.21 [+0.23; +2.20] | +0.43 | YOK | YOK |
| C202:DS09 | BIST egitim | 890 / 76 | -0.30 [-2.80; +1.96] | +0.62 [-1.60; +3.00] | -0.92 [-1.95; -0.01] | +0.14 | YOK | YOK |
| C202:DS09 | BIST sinama | 1380 / 42 | -0.49 [-2.24; +1.26] | +0.29 [-1.49; +2.24] | -0.77 [-1.73; +0.14] | -0.12 | YOK | YOK |
| C202:DS10 | ABD egitim | 3815 / 79 | +0.68 [-2.33; +4.17] | +0.83 [-1.68; +3.77] | -0.14 [-1.19; +0.98] | -0.00 | YOK | YOK |
| C202:DS10 | ABD sinama | 2513 / 41 | +1.17 [-0.92; +3.22] | +1.35 [-0.40; +3.30] | -0.18 [-0.96; +0.60] | -0.24 | YOK | YOK |
| C202:DS10 | AVR egitim | 1644 / 82 | +1.57 [-0.79; +4.46] | +0.77 [-0.80; +2.74] | +0.80 [-0.07; +1.93] | +0.16 | YOK | YOK |
| C202:DS10 | AVR sinama | 515 / 41 | +2.14 [+0.29; +3.70] | +1.20 [-0.12; +2.74] | +0.94 [+0.02; +1.85] | +0.18 | YOK | YOK |
| C202:DS10 | BIST egitim | 733 / 69 | +0.61 [-2.70; +3.86] | +1.98 [-1.19; +5.55] | -1.36 [-2.52; -0.24] | +0.02 | YOK | YOK |
| C202:DS10 | BIST sinama | 993 / 42 | +0.27 [-2.99; +3.47] | +1.90 [-1.08; +5.12] | -1.63 [-2.96; -0.57] | -0.31 | YOK | YOK |
| C202:DS11 | ABD egitim | 7715 / 84 | -0.11 [-2.35; +2.40] | +0.13 [-1.73; +2.27] | -0.24 [-1.08; +0.62] | -0.07 | YOK | YOK |
| C202:DS11 | ABD sinama | 5199 / 42 | +1.13 [-0.82; +3.14] | +1.13 [-0.45; +2.75] | -0.00 [-0.84; +0.69] | +0.13 | YOK | YOK |
| C202:DS11 | AVR egitim | 2618 / 84 | +1.08 [-1.18; +3.83] | +0.41 [-1.17; +2.28] | +0.67 [-0.17; +1.66] | +0.08 | YOK | YOK |
| C202:DS11 | AVR sinama | 1017 / 42 | +1.66 [+0.24; +2.91] | +0.82 [-0.16; +1.92] | +0.84 [+0.13; +1.54] | +0.03 | YOK | YOK |
| C202:DS11 | BIST egitim | 1624 / 80 | -0.90 [-3.08; +1.41] | +0.46 [-1.58; +2.96] | -1.36 [-2.13; -0.60] | -0.13 | YOK | YOK |
| C202:DS11 | BIST sinama | 2922 / 42 | -0.19 [-2.30; +1.96] | +0.50 [-1.48; +2.69] | -0.70 [-1.33; -0.17] | -0.09 | YOK | YOK |
| C202:DS12 | ABD egitim | 1038 / 84 | +0.95 [-2.27; +3.87] | +1.10 [-1.31; +3.39] | -0.15 [-1.74; +1.37] | +0.40 | YOK | YOK |
| C202:DS12 | ABD sinama | 751 / 41 | +1.32 [-0.73; +3.30] | +0.85 [-0.42; +2.03] | +0.47 [-0.77; +1.79] | +0.24 | YOK | YOK |
| C202:DS12 | AVR egitim | 325 / 58 | +3.72 [+0.16; +7.13] | +1.49 [-0.55; +3.17] | +2.23 [+0.29; +4.46] | +1.27 | YOK | YOK |
| C202:DS12 | AVR sinama | 131 / 39 | +3.16 [+0.64; +5.37] | +1.07 [+0.17; +1.96] | +2.09 [-0.24; +4.06] | +1.08 | YOK | YOK |
| C202:DS12 | BIST egitim | 199 / 52 | -1.53 [-3.54; +0.47] | -0.57 [-2.36; +1.45] | -0.95 [-2.85; +0.61] | +0.11 | YOK | YOK |
| C202:DS12 | BIST sinama | 442 / 41 | +1.21 [-2.45; +4.72] | +1.07 [-2.01; +4.00] | +0.14 [-1.09; +1.12] | -0.34 | YOK | YOK |
| C202:DS13 | ABD egitim | 332 / 67 | +1.82 [-1.05; +4.76] | +1.04 [-0.64; +2.84] | +0.79 [-1.06; +2.80] | +0.22 | YOK | YOK |
| C202:DS13 | ABD sinama | 218 / 38 | +1.17 [-1.21; +3.72] | +0.82 [-0.93; +2.76] | +0.35 [-1.34; +2.15] | +0.98 | YOK | YOK |
| C202:DS13 | AVR egitim | 144 / 47 | +4.80 [+0.58; +8.21] | +3.63 [-0.00; +7.04] | +1.17 [-0.79; +3.75] | -0.20 | YOK | YOK |
| C202:DS13 | AVR sinama | 46 / 20 | +1.77 [-1.70; +5.44] | +1.00 [-0.42; +2.30] | +0.78 [-2.56; +4.46] | -0.46 | YOK | YOK |
| C202:DS13 | BIST egitim | 81 / 29 | +1.84 [-3.90; +9.84] | +1.72 [-1.41; +6.31] | +0.12 [-3.18; +3.98] | +1.75 | YOK | YOK |
| C202:DS13 | BIST sinama | 186 / 31 | +1.66 [-1.10; +4.72] | -0.23 [-1.73; +1.30] | +1.89 [-0.33; +4.34] | +1.86 | YOK | YOK |
| C202:DS14 | ABD egitim | 74 / 34 | -3.44 [-12.67; +2.80] | -0.05 [-2.59; +2.14] | -3.39 [-11.90; +2.04] | -0.81 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS14 | ABD sinama | 40 / 28 | +7.60 [-0.90; +18.99] | +1.72 [-0.18; +3.69] | +5.88 [-2.27; +17.41] | +5.59 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS14 | AVR egitim | 17 / 11 | -2.53 [-8.13; +3.50] | -0.99 [-3.74; +1.37] | -1.53 [-5.04; +2.62] | -1.79 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS14 | AVR sinama | 13 / 12 | +0.52 [-8.25; +8.21] | -0.09 [-1.57; +1.26] | +0.62 [-7.85; +7.80] | +0.24 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS14 | BIST egitim | 17 / 12 | -4.61 [-9.94; +4.96] | +0.48 [-2.58; +5.02] | -5.09 [-9.50; +3.23] | -7.66 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS14 | BIST sinama | 33 / 17 | +1.26 [-3.21; +5.57] | +3.10 [+0.49; +5.48] | -1.83 [-6.37; +2.33] | -2.41 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS15 | ABD egitim | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS15 | AVR sinama | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS15 | BIST egitim | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS15 | BIST sinama | 2 / 2 | +8.00 [-1.33; +17.34] | +6.19 [+5.30; +7.09] | +1.81 [-6.62; +10.24] | +5.50 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| C202:DS16 | ABD egitim | 1206 / 84 | -0.65 [-2.55; +1.27] | -0.22 [-1.57; +1.23] | -0.43 [-1.59; +0.68] | +0.00 | YOK | YOK |
| C202:DS16 | ABD sinama | 1283 / 42 | +0.12 [-1.51; +1.60] | +0.57 [-0.53; +1.60] | -0.45 [-1.29; +0.29] | -0.76 | YOK | YOK |
| C202:DS16 | AVR egitim | 460 / 77 | +1.31 [-0.62; +3.31] | +0.10 [-1.05; +1.29] | +1.21 [+0.20; +2.27] | +0.89 | YOK | YOK |
| C202:DS16 | AVR sinama | 333 / 41 | +1.22 [-0.37; +2.70] | +0.49 [-0.31; +1.26] | +0.73 [-0.43; +1.90] | +0.32 | YOK | YOK |
| C202:DS16 | BIST egitim | 134 / 47 | -2.52 [-5.09; +0.19] | -1.39 [-2.77; +0.15] | -1.13 [-3.23; +0.85] | +0.82 | YOK | YOK |
| C202:DS16 | BIST sinama | 232 / 38 | -0.51 [-3.24; +2.70] | +0.02 [-2.61; +2.88] | -0.53 [-1.89; +0.86] | +0.05 | YOK | YOK |
| C202:DS17 | ABD egitim | 3516 / 84 | +1.65 [+0.23; +3.42] | +1.44 [-0.14; +3.32] | +0.21 [-0.39; +0.95] | -0.26 | YOK | YOK |
| C202:DS17 | ABD sinama | 2488 / 42 | +0.35 [-1.62; +2.34] | +1.26 [-0.81; +3.37] | -0.91 [-1.80; +0.09] | -1.29 | YOK | YOK |
| C202:DS17 | AVR egitim | 1141 / 81 | +1.71 [-0.16; +3.72] | +1.68 [+0.01; +3.03] | +0.03 [-0.96; +1.22] | -0.57 | YOK | YOK |
| C202:DS17 | AVR sinama | 393 / 41 | +2.82 [+0.94; +4.78] | +1.02 [-0.35; +2.42] | +1.80 [+0.73; +2.96] | +0.81 | YOK | YOK |
| C202:DS17 | BIST egitim | 737 / 67 | -1.62 [-3.76; +0.68] | +1.35 [-1.37; +4.88] | -2.97 [-4.75; -1.46] | -1.17 | YOK | YOK |
| C202:DS17 | BIST sinama | 1343 / 42 | +0.38 [-3.16; +3.59] | +1.44 [-2.08; +4.59] | -1.06 [-1.93; -0.24] | -0.35 | YOK | YOK |
| C202:DS18 | ABD egitim | 2889 / 84 | +0.93 [-1.53; +3.56] | +1.04 [-0.81; +3.11] | -0.11 [-1.36; +1.06] | +0.19 | YOK | YOK |
| C202:DS18 | ABD sinama | 1864 / 42 | +1.46 [-1.02; +3.74] | +1.74 [-0.08; +3.54] | -0.28 [-1.52; +1.11] | -0.02 | YOK | YOK |
| C202:DS18 | AVR egitim | 997 / 74 | +2.18 [-0.35; +4.57] | +1.78 [-0.20; +3.40] | +0.40 [-0.62; +1.66] | -0.15 | YOK | YOK |
| C202:DS18 | AVR sinama | 330 / 41 | +1.73 [-0.23; +3.56] | +0.96 [-0.08; +1.97] | +0.77 [-0.56; +2.12] | -0.46 | YOK | YOK |
| C202:DS18 | BIST egitim | 622 / 62 | -1.27 [-3.90; +2.54] | +0.49 [-2.37; +5.17] | -1.76 [-3.06; -0.68] | -0.10 | YOK | YOK |
| C202:DS18 | BIST sinama | 1157 / 40 | +0.93 [-3.18; +4.95] | +1.54 [-2.14; +5.17] | -0.61 [-1.56; +0.29] | -0.05 | YOK | YOK |
| C202:DS19 | ABD egitim | 1014 / 83 | +0.59 [-1.49; +2.33] | +0.65 [-0.72; +1.99] | -0.07 [-1.74; +1.17] | +0.61 | YOK | YOK |
| C202:DS19 | ABD sinama | 732 / 42 | +0.58 [-1.79; +3.00] | +0.91 [-0.71; +2.47] | -0.33 [-1.61; +1.16] | -0.59 | YOK | YOK |
| C202:DS19 | AVR egitim | 317 / 71 | +1.12 [-1.15; +3.21] | +0.66 [-0.54; +1.88] | +0.46 [-1.03; +1.76] | -0.45 | YOK | YOK |
| C202:DS19 | AVR sinama | 139 / 41 | +1.21 [-0.73; +3.08] | +0.78 [-0.13; +1.72] | +0.43 [-1.18; +2.10] | -0.60 | YOK | YOK |
| C202:DS19 | BIST egitim | 245 / 46 | -0.91 [-3.49; +2.81] | -0.47 [-3.81; +5.23] | -0.44 [-3.16; +1.33] | +0.57 | YOK | YOK |
| C202:DS19 | BIST sinama | 255 / 38 | +0.67 [-2.19; +3.15] | +0.79 [-1.77; +3.38] | -0.12 [-1.66; +1.58] | +0.42 | YOK | YOK |
| C202:DS20 | ABD egitim | 4019 / 84 | -0.01 [-2.29; +2.84] | +0.04 [-1.73; +2.38] | -0.04 [-1.04; +1.11] | +0.05 | YOK | YOK |
| C202:DS20 | ABD sinama | 2463 / 42 | +2.02 [-0.54; +4.38] | +1.67 [-0.50; +3.95] | +0.35 [-0.43; +1.01] | +0.17 | YOK | YOK |
| C202:DS20 | AVR egitim | 1530 / 76 | +1.32 [-0.76; +4.25] | +0.32 [-1.14; +2.33] | +1.01 [+0.22; +2.24] | +0.31 | YOK | YOK |
| C202:DS20 | AVR sinama | 566 / 42 | +2.36 [+0.60; +4.23] | +1.29 [-0.16; +3.04] | +1.06 [+0.37; +1.83] | +0.20 | YOK | YOK |
| C202:DS20 | BIST egitim | 778 / 70 | +1.10 [-2.39; +4.13] | +1.70 [-1.72; +5.38] | -0.60 [-1.72; +0.67] | +0.27 | YOK | YOK |
| C202:DS20 | BIST sinama | 1260 / 41 | +0.89 [-2.51; +4.01] | +1.46 [-1.02; +3.90] | -0.56 [-1.82; +0.31] | -0.54 | YOK | YOK |
| C202:DS21 | ABD egitim | 2878 / 84 | +1.52 [-0.67; +3.93] | +1.54 [-0.46; +3.99] | -0.02 [-0.91; +0.80] | -0.02 | YOK | YOK |
| C202:DS21 | ABD sinama | 1947 / 42 | +2.89 [-0.65; +6.07] | +2.43 [-0.52; +4.99] | +0.46 [-0.45; +1.16] | +0.39 | YOK | YOK |
| C202:DS21 | AVR egitim | 952 / 74 | +2.20 [-0.44; +4.95] | +0.78 [-1.26; +2.94] | +1.42 [+0.59; +2.29] | +1.02 | YOK | YOK |
| C202:DS21 | AVR sinama | 503 / 42 | +2.01 [+0.46; +3.49] | +1.10 [-0.02; +2.24] | +0.91 [+0.08; +1.70] | +0.22 | YOK | YOK |
| C202:DS21 | BIST egitim | 573 / 62 | +0.69 [-4.94; +4.81] | +3.15 [-2.25; +7.56] | -2.45 [-4.14; -1.23] | -0.20 | YOK | YOK |
| C202:DS21 | BIST sinama | 690 / 41 | +0.13 [-3.94; +3.21] | +2.49 [-0.62; +5.12] | -2.36 [-4.06; -1.35] | -1.44 | YOK | YOK |
| C202:DS22 | ABD egitim | 117 / 49 | -0.27 [-7.32; +5.65] | +2.45 [-0.36; +5.54] | -2.72 [-8.53; +1.37] | -0.85 | YOK | YOK |
| C202:DS22 | ABD sinama | 100 / 33 | +0.23 [-4.52; +6.13] | +0.80 [-1.20; +2.70] | -0.57 [-4.17; +4.75] | -0.77 | YOK | YOK |
| C202:DS22 | AVR egitim | 28 / 21 | +1.71 [-3.43; +6.22] | +1.71 [-0.67; +4.25] | +0.01 [-4.23; +3.88] | -0.70 | YOK | YOK |
| C202:DS22 | AVR sinama | 23 / 16 | +6.45 [+0.78; +12.10] | +0.89 [-1.07; +2.77] | +5.56 [+0.40; +10.49] | +4.70 | YOK | YOK |
| C202:DS22 | BIST egitim | 31 / 23 | -3.62 [-8.18; +0.74] | -0.45 [-3.67; +3.33] | -3.17 [-7.04; +0.45] | +0.09 | YOK | YOK |
| C202:DS22 | BIST sinama | 61 / 20 | +2.68 [-4.59; +6.11] | +4.15 [-2.39; +7.29] | -1.47 [-4.22; +1.24] | -1.93 | YOK | YOK |
| C202:DS23 | ABD egitim | 2520 / 84 | -0.07 [-2.44; +2.09] | -0.16 [-1.93; +1.56] | +0.09 [-0.89; +0.92] | -0.13 | YOK | YOK |
| C202:DS23 | ABD sinama | 1909 / 42 | +0.41 [-1.52; +2.19] | +0.99 [-0.72; +2.72] | -0.59 [-1.45; +0.22] | -0.93 | YOK | YOK |
| C202:DS23 | AVR egitim | 1182 / 80 | +1.23 [-0.80; +3.45] | +0.18 [-1.15; +1.66] | +1.06 [+0.20; +1.94] | +0.67 | YOK | YOK |
| C202:DS23 | AVR sinama | 487 / 42 | +1.85 [+0.00; +3.55] | +1.04 [-0.23; +2.46] | +0.81 [-0.04; +1.57] | +0.16 | YOK | YOK |
| C202:DS23 | BIST egitim | 597 / 72 | -1.77 [-3.44; +0.11] | -0.53 [-1.91; +1.23] | -1.25 [-2.43; -0.06] | -0.62 | YOK | YOK |
| C202:DS23 | BIST sinama | 1155 / 42 | +2.63 [-0.28; +5.18] | +1.80 [-1.00; +4.32] | +0.83 [+0.26; +1.34] | +0.59 | YOK | YOK |
| C202:DS25 | ABD egitim | 2666 / 84 | +0.75 [-1.46; +3.02] | +1.02 [-0.78; +2.85] | -0.27 [-1.31; +0.86] | +0.15 | YOK | YOK |
| C202:DS25 | ABD sinama | 1838 / 42 | +0.95 [-1.81; +3.26] | +0.76 [-1.04; +2.41] | +0.18 [-1.03; +1.33] | -0.08 | YOK | YOK |
| C202:DS25 | AVR egitim | 890 / 73 | +2.32 [-0.43; +4.93] | +1.43 [-0.37; +2.93] | +0.89 [-0.40; +2.35] | +0.24 | YOK | YOK |
| C202:DS25 | AVR sinama | 357 / 42 | +2.91 [+0.96; +4.66] | +1.14 [-0.24; +2.49] | +1.77 [+0.65; +2.79] | +0.63 | YOK | YOK |
| C202:DS25 | BIST egitim | 393 / 61 | -1.88 [-4.06; +0.60] | -0.30 [-2.49; +2.80] | -1.58 [-3.05; -0.34] | -0.45 | YOK | YOK |
| C202:DS25 | BIST sinama | 956 / 42 | +2.39 [-1.76; +6.04] | +2.33 [-1.47; +5.57] | +0.06 [-0.93; +0.78] | -0.35 | YOK | YOK |
| C202:DS28 | ABD egitim | 2769 / 75 | +1.15 [-2.79; +5.25] | +0.88 [-1.20; +3.23] | +0.27 [-1.96; +2.46] | +0.36 | YOK | YOK |
| C202:DS28 | ABD sinama | 1796 / 42 | +1.79 [-0.35; +3.89] | +0.80 [-0.57; +2.13] | +0.99 [-0.14; +2.15] | +1.21 | YOK | YOK |
| C202:DS28 | AVR egitim | 504 / 59 | +4.17 [-0.19; +8.45] | +1.56 [-0.17; +3.16] | +2.61 [-0.34; +5.51] | +1.47 | YOK | YOK |
| C202:DS28 | AVR sinama | 197 / 42 | +2.70 [+0.84; +4.59] | +0.38 [-0.41; +1.17] | +2.32 [+0.41; +4.23] | +0.09 | YOK | YOK |
| C202:DS28 | BIST egitim | 472 / 65 | -2.95 [-5.71; -0.19] | -0.77 [-2.27; +0.71] | -2.18 [-4.09; -0.31] | +0.25 | YOK | YOK |
| C202:DS28 | BIST sinama | 684 / 42 | +0.35 [-2.74; +3.58] | +1.30 [-1.12; +3.56] | -0.95 [-2.32; +0.51] | +0.76 | YOK | YOK |
| DS_ANA | ABD egitim | 14061 / 84 | +0.35 [-1.72; +2.60] | +0.57 [-1.14; +2.38] | -0.22 [-1.00; +0.58] | -0.06 | YOK | YOK |
| DS_ANA | ABD sinama | 9950 / 42 | +0.91 [-1.01; +2.77] | +0.89 [-0.59; +2.38] | +0.01 [-0.69; +0.67] | +0.10 | YOK | YOK |
| DS_ANA | AVR egitim | 4562 / 84 | +1.55 [-0.36; +3.73] | +0.75 [-0.52; +2.16] | +0.79 [+0.00; +1.70] | +0.23 | YOK | YOK |
| DS_ANA | AVR sinama | 1912 / 42 | +1.73 [+0.47; +3.00] | +0.66 [-0.24; +1.65] | +1.07 [+0.45; +1.64] | +0.26 | YOK | YOK |
| DS_ANA | BIST egitim | 2947 / 81 | -1.21 [-2.89; +0.79] | +0.07 [-1.67; +2.28] | -1.28 [-1.96; -0.69] | +0.16 | YOK | YOK |
| DS_ANA | BIST sinama | 5823 / 42 | +0.74 [-2.15; +3.46] | +1.04 [-1.72; +3.68] | -0.30 [-0.80; +0.13] | +0.09 | YOK | YOK |
| TUR:T_CEMAL_OLMAZ | ABD egitim | 6 / 5 | -4.97 [-11.16; +0.47] | -2.46 [-4.05; -0.82] | -2.51 [-10.14; +4.30] | -0.89 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLMAZ | ABD sinama | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLMAZ | BIST egitim | 5 / 3 | -2.56 [-7.87; +17.78] | -0.11 [-1.39; +4.90] | -2.44 [-6.51; +12.87] | -1.12 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLMAZ | BIST sinama | 5 / 4 | +4.77 [+0.52; +13.08] | +3.70 [-1.55; +10.59] | +1.07 [-0.78; +3.75] | +0.46 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | ABD egitim | 5 / 4 | +5.10 [-6.42; +22.38] | -0.79 [-6.26; +4.93] | +5.89 [-5.09; +18.02] | +2.43 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | ABD sinama | 7 / 5 | +0.72 [-3.07; +3.57] | -2.17 [-4.58; +1.30] | +2.89 [-3.53; +6.90] | +2.78 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | AVR egitim | 2 / 2 | +8.32 [+7.62; +9.01] | +2.68 [-0.12; +5.48] | +5.64 [+3.53; +7.74] | +4.41 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | AVR sinama | 2 / 2 | +0.56 [-5.23; +6.34] | -1.76 [-2.28; -1.24] | +2.31 [-2.95; +7.58] | +0.62 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | BIST egitim | 7 / 7 | -3.81 [-9.63; +3.21] | +0.31 [-3.66; +4.16] | -4.12 [-9.67; +1.54] | -2.32 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_CEMAL_OLUR | BIST sinama | 9 / 8 | +18.46 [+5.10; +30.18] | +2.34 [-4.67; +8.63] | +16.12 [+4.42; +27.44] | +11.83 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | ABD egitim | 12 / 10 | +1.45 [-5.39; +8.70] | -0.51 [-2.60; +1.69] | +1.97 [-4.46; +8.31] | +1.37 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | ABD sinama | 11 / 9 | -1.93 [-8.66; +3.66] | -1.92 [-4.24; +1.14] | -0.01 [-7.21; +5.78] | +0.60 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | AVR egitim | 3 / 3 | +1.69 [-4.88; +9.01] | +6.64 [+3.02; +11.43] | -4.96 [-16.31; +3.53] | -1.97 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | AVR sinama | 5 / 5 | -2.77 [-13.66; +6.78] | -0.80 [-2.26; +1.10] | -1.97 [-12.66; +6.71] | -2.67 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | BIST egitim | 12 / 9 | -2.05 [-8.25; +5.40] | +2.32 [-0.31; +5.34] | -4.37 [-9.08; +1.33] | -3.41 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLMAZ | BIST sinama | 17 / 10 | +8.38 [-0.65; +16.85] | +2.85 [-3.28; +8.18] | +5.53 [-1.05; +13.24] | +4.26 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLUR | ABD egitim | 3 / 3 | -6.97 [-8.84; -3.34] | -6.36 [-10.43; -0.44] | -0.60 [-2.90; +1.59] | -5.73 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLUR | ABD sinama | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLUR | AVR egitim | 1 / 1 | — | — | — | — | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLUR | BIST egitim | 4 / 4 | -7.34 [-9.84; -5.62] | -3.29 [-7.09; -1.31] | -4.05 [-8.53; +1.36] | -3.68 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TUR:T_MODEL_OLUR | BIST sinama | 11 / 6 | +8.67 [+2.95; +14.82] | +5.94 [-0.54; +11.19] | +2.72 [-3.57; +13.22] | -1.04 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| Y1 | ABD egitim | 8686 / 77 | -1.01 [-1.74; -0.29] | -0.34 [-1.54; +0.97] | -0.66 [-1.65; +0.06] | -0.18 | YOK | YOK |
| Y1 | ABD sinama | 6132 / 44 | -0.34 [-1.12; +0.47] | +0.02 [-0.95; +0.99] | -0.37 [-0.75; +0.05] | -0.09 | YOK | YOK |
| Y1 | AVR egitim | 4496 / 83 | -0.35 [-0.83; +0.09] | -0.18 [-0.69; +0.30] | -0.17 [-0.40; +0.07] | -0.03 | YOK | YOK |
| Y1 | AVR sinama | 2526 / 44 | -0.43 [-1.07; +0.26] | -0.19 [-0.77; +0.37] | -0.23 [-0.52; +0.07] | -0.04 | YOK | YOK |
| Y1 | BIST egitim | 2588 / 79 | +0.24 [-1.23; +1.76] | +1.09 [-0.41; +2.62] | -0.85 [-1.46; -0.23] | -0.80 | YOK | YOK |
| Y1 | BIST sinama | 2096 / 44 | -0.83 [-3.51; +1.85] | +0.07 [-2.31; +2.42] | -0.90 [-1.77; -0.02] | -0.82 | YOK | YOK |

### Ç191 — YAPI_HEDEF 2. tur: Y6 / Y8 / Y8B (Y7 n = 0) (H 15, gecerli; eski: ÖLÇÜLEMEDİ (YAPI_HEDEF 2. tur Y6-Y8; yön aleyhte))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| Y6 | ABD 2016-22 | 867 / 73 | -1.04 [-1.71; -0.46] | -1.36 [-2.32; -0.54] | +0.32 [-0.36; +1.00] | — | YOK | YOK |
| Y6 | ABD 2023 | 163 / 12 | -0.33 [-1.44; +0.64] | +1.08 [-1.81; +2.70] | -1.40 [-3.10; +1.03] | — | YOK | YOK |
| Y6 | ABD 2024-26 | 310 / 30 | -0.70 [-1.70; +0.18] | -0.42 [-1.43; +0.45] | -0.27 [-1.35; +0.71] | — | YOK | YOK |
| Y6 | AVR 2016-22 | 522 / 80 | -0.26 [-0.98; +0.44] | -0.08 [-0.57; +0.38] | -0.18 [-0.72; +0.37] | — | YOK | YOK |
| Y6 | AVR 2023 | 80 / 11 | -1.37 [-3.09; +0.70] | -0.54 [-2.14; +1.34] | -0.83 [-1.72; -0.01] | — | YOK | YOK |
| Y6 | AVR 2024-26 | 181 / 32 | -1.55 [-2.28; -0.76] | -0.25 [-0.87; +0.28] | -1.31 [-2.06; -0.43] | — | YOK | YOK |
| Y6 | BIST 2016-22 | 87 / 40 | +0.55 [-2.29; +3.22] | +1.82 [-0.51; +4.22] | -1.26 [-3.50; +0.89] | — | YOK | YOK |
| Y6 | BIST 2023 | 5 / 3 | -2.44 [-16.29; +31.52] | -4.97 [-17.36; +11.05] | +2.53 [-2.97; +20.48] | — | YOK | YOK |
| Y6 | BIST 2024-26 | 41 / 18 | -1.62 [-5.74; +2.15] | +1.49 [-2.12; +5.50] | -3.11 [-5.64; -0.49] | — | YOK | YOK |
| Y8 | ABD 2016-22 | 694 / 72 | -1.02 [-1.79; -0.36] | -1.36 [-2.49; -0.44] | +0.34 [-0.44; +1.11] | — | YOK | YOK |
| Y8 | ABD 2023 | 93 / 10 | -0.50 [-1.61; +0.62] | +1.17 [-1.57; +2.97] | -1.68 [-3.63; +0.69] | — | YOK | YOK |
| Y8 | ABD 2024-26 | 194 / 28 | -0.77 [-1.80; +0.17] | -0.53 [-1.74; +0.42] | -0.24 [-1.30; +0.82] | — | YOK | YOK |
| Y8 | AVR 2016-22 | 426 / 77 | -0.40 [-1.15; +0.29] | -0.17 [-0.72; +0.31] | -0.23 [-0.80; +0.33] | — | YOK | YOK |
| Y8 | AVR 2023 | 52 / 10 | -1.72 [-3.15; -0.18] | -0.76 [-2.38; +1.08] | -0.96 [-2.17; +0.13] | — | YOK | YOK |
| Y8 | AVR 2024-26 | 136 / 32 | -1.46 [-2.13; -0.69] | -0.37 [-1.05; +0.21] | -1.09 [-1.93; -0.10] | — | YOK | YOK |
| Y8 | BIST 2016-22 | 46 / 30 | -0.73 [-4.58; +3.11] | +1.60 [-0.84; +3.99] | -2.33 [-5.77; +1.03] | — | YOK | YOK |
| Y8 | BIST 2023 | 4 / 3 | -1.59 [-16.29; +31.52] | -4.16 [-17.36; +11.05] | +2.56 [-5.65; +20.48] | — | YOK | YOK |
| Y8 | BIST 2024-26 | 23 / 12 | -1.56 [-7.27; +3.33] | +1.26 [-2.12; +5.14] | -2.82 [-7.14; +0.32] | — | YOK | YOK |
| Y8B | ABD 2016-22 | 175 / 56 | -1.07 [-2.09; -0.06] | -1.33 [-2.18; -0.54] | +0.27 [-0.61; +1.21] | — | YOK | YOK |
| Y8B | ABD 2023 | 70 / 11 | -0.10 [-1.66; +1.21] | +0.95 [-2.54; +3.09] | -1.04 [-3.32; +1.99] | — | YOK | YOK |
| Y8B | ABD 2024-26 | 116 / 29 | -0.58 [-2.14; +0.73] | -0.24 [-1.30; +0.70] | -0.34 [-1.99; +1.03] | — | YOK | YOK |
| Y8B | AVR 2016-22 | 96 / 47 | +0.37 [-1.34; +2.15] | +0.35 [-0.27; +0.96] | +0.02 [-1.47; +1.71] | — | YOK | YOK |
| Y8B | AVR 2023 | 28 / 8 | -0.72 [-3.80; +2.89] | -0.13 [-1.95; +1.70] | -0.59 [-2.73; +1.37] | — | YOK | YOK |
| Y8B | AVR 2024-26 | 45 / 22 | -1.85 [-3.68; +0.12] | +0.12 [-0.44; +0.64] | -1.97 [-3.65; +0.09] | — | YOK | YOK |
| Y8B | BIST 2016-22 | 41 / 26 | +1.99 [-1.60; +5.68] | +2.06 [-0.81; +5.02] | -0.07 [-2.79; +2.77] | — | YOK | YOK |
| Y8B | BIST 2023 | 1 / 1 | — | — | — | — | YOK | YOK |
| Y8B | BIST 2024-26 | 18 / 13 | -1.69 [-6.71; +2.69] | +1.79 [-2.64; +5.82] | -3.48 [-6.83; +0.82] | — | YOK | YOK |

### Ç99 — KAP içeriden alım (K27): net alım, büyük alım, çölde alım (H 60, fi_olcut; eski: İçeriden alım bildirimi olumlu bilgi taşımıyor (eşlerin gerisinde))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| alim | BIST 2023 | 201 / 12 | +1.53 [-17.32; +20.09] | +4.81 [-13.89; +23.13] | -3.28 [-9.15; +2.24] | -4.50 | YOK | YOK |
| alim | BIST 2024-26 | 418 / 29 | -3.30 [-7.12; +1.08] | +0.07 [-3.30; +4.22] | -3.37 [-6.22; -0.40] | -2.62 | YOK | YOK |
| buyuk | BIST 2023 | 12 / 6 | -11.61 [-58.26; +22.28] | +6.91 [-28.02; +35.14] | -18.52 [-45.76; -3.25] | -12.98 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| buyuk | BIST 2024-26 | 30 / 17 | -6.81 [-18.00; +8.26] | -0.68 [-5.75; +4.84] | -6.13 [-18.07; +9.57] | -4.88 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| col_alim | BIST 2023 | 36 / 8 | +15.05 [-18.22; +52.13] | +15.93 [-9.00; +38.76] | -0.89 [-27.05; +19.47] | +0.92 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| col_alim | BIST 2024-26 | 62 / 25 | -4.53 [-14.38; +4.66] | +1.25 [-4.33; +7.80] | -5.78 [-13.33; +1.22] | -5.95 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |

### Ç189 — S+ v2 TAM GİRİLİR (TAM_DIP) (H 60, oc; eski: ÖLÇÜLEMEDİ (TAM_DIP; hiçbir hücrede alt uç > 0))

| Kol | Hücre | n / ay | TOPLAM | ZAMANLAMA | SEÇİM | Eski fark | ZAM karar | TOP karar |
|---|---|---|---|---|---|---|---|---|
| TAM_DIP | ABD 2016-22 | 283 / 63 | -5.25 [-13.69; +1.55] | -2.70 [-6.84; +1.71] | -2.55 [-10.28; +1.85] | +0.24 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | ABD 2023 | 47 / 11 | +13.06 [-2.47; +21.15] | +6.00 [-5.60; +12.71] | +7.06 [+1.41; +10.32] | -1.71 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | ABD 2024-26 | 187 / 29 | +2.74 [-0.90; +6.73] | -0.80 [-3.63; +2.27] | +3.54 [-0.82; +7.33] | +1.14 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR 2016-22 | 156 / 50 | -1.62 [-5.71; +2.87] | -0.97 [-4.30; +2.50] | -0.66 [-3.37; +2.23] | -0.63 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR 2023 | 34 / 10 | +3.12 [-3.94; +10.11] | +0.86 [-2.80; +4.55] | +2.25 [-2.51; +6.75] | -3.85 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | AVR 2024-26 | 132 / 29 | +2.37 [-1.68; +6.89] | -0.02 [-1.22; +1.19] | +2.39 [-1.10; +6.15] | -1.78 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST 2016-22 | 296 / 61 | -8.19 [-12.85; -2.64] | -5.06 [-8.69; -1.04] | -3.13 [-6.63; +0.46] | -1.85 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST 2023 | 101 / 9 | +16.08 [-5.23; +45.01] | +15.50 [-7.28; +40.24] | +0.58 [-3.23; +7.81] | -4.08 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
| TAM_DIP | BIST 2024-26 | 387 / 28 | +5.87 [+0.15; +12.26] | +1.85 [-2.76; +6.59] | +4.02 [-0.16; +9.26] | +2.16 | ÖLÇÜLEMEDİ | ÖLÇÜLEMEDİ |
