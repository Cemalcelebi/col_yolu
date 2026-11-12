# K67 — BİLANÇO SONRASI ANALİST REVİZYONLARI: ÖN KAYIT (ölçümden ÖNCE)

K67 v1.0 (2026-11-12): bilanço sonrası analist revizyonları (Yahoo not günlüğü) x FI_OLCUT; S1 bilanço olayları, S2 çöl etkileşimi
Yazım zamanı: 2026-11-12 06:00:50 UTC (2026-11-12 09:00 TR)
ESIK_SHA256: 377b4fffeb71f5512fad8a89bab658b90bebf4943a483b5c6e712b60c1bcc9be

Bu dosya gerçek veride revizyona bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `indir` ve `kapsam` sayımı koşuldu: §15). `python -I K67.py kos`
bu dosya git'e işlenmeden, işlendikten sonra değişmişse, mühür ya da veri sha256'ları tutmazsa çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- liste_abd.csv.gz: sha256 87539954817d5d551623eeed04fa410844646539093a4e841a7755a2cfc674cb (1 dosya)
- k67_yahoo: sha256 57d127842818959d7e3c98aceb39fa8e52adf4313c3fe831a0be618f1b950464 (2810 dosya)
- FON_IZI.py: sha256 ea0cc19f9b6514c50340df0e331c8d1a5e7961083918eefec45de6d7eb10ac7b (1 dosya)
- K60.py: sha256 d819f93082188688f5a3ed2a5d1bdb39735169125f292c62103b3e842ebd8e66 (1 dosya)
- K64.py: sha256 0255e8b2902228e20665a439e8df529cf4521bbee4ed24d248c1977e08577653 (1 dosya)
k67_yahoo = /tmp/k67_yahoo içindeki not/*.json.gz + takvim/*.html.gz (göreli yol + dosya sha256, sıralı; gzip başlığı sabit). Önbellek repoya konmaz.

## 0. Soru (Cemal'in isteği, aynen)
"Bilanço sonrasında analistlerin EPS ve hedef fiyat tahminlerinde meydana gelen değişimleri ölç: yukarı revizyon yapan analist sayısı, aşağı revizyon yapan analist
sayısı, net revizyon oranı, revizyonların büyüklüğü, analistlerin görüş birliği veya ayrışması, revizyonun bilanço sürpriziyle aynı veya ters yönde olması. Veri yoksa
tahmin üretme; hangi veri sağlayıcısında hangi tarihsel alanın eksik olduğunu belirt."
İki soru: (S1) bu ölçüler bilanço olaylarında sonraki 60 (ve 20) günlük eşli farkı açıklıyor mu, bilanço sürprizini (tepki) kontrol ettikten sonra da? (S2) çöl
sinyaline ek bilgi taşıyorlar mı?

## 1. Veri kaynakları: hangi sağlayıcıda hangi tarihsel alan VAR / YOK
| alan | sağlayıcı | durum (bu işte) | tarihsel derinlik | not |
|---|---|---|---|---|
| hedef fiyat değişimi (kurum, önceki / yeni hedef, yayım anı) | Yahoo not günlüğü (quoteSummary upgradeDowngradeHistory; yfinance upgrades_downgrades) | **VAR, kullanılıyor** | 2012 -> bugün (§15 yıl tablosu) | ücretsiz; resmî olmayan uç; 'bugünkü' görüntü (çekim günü §15); geçmiş kayıtların sonradan eklenip değiştirilmediği doğrulanamaz |
| tavsiye değişimi (up / down / main / reit / init; önceki / yeni not) | Yahoo not günlüğü | **VAR, kullanılıyor** | aynı | önceki tavsiye alanı yıllara göre boş olabilir (K51: 2020-22 %20-25 dolu); eylem alanı her kayıtta dolu |
| analist KİŞİ kimliği | Yahoo | **YOK** | — | yalnız kurum adı; 'analist sayısı' = KURUM sayısı |
| EPS tahmini, analist bazında tarih damgalı seri | Yahoo | **YOK** | — | Yahoo'da yalnız güncel anlık görüntü (earningsTrend / epsRevisions: şimdi, 7 / 30 / 60 / 90 gün önce; yukarı / aşağı revizyon sayısı 7 / 30 gün); geçmiş görüntü saklanmıyor |
| EPS konsensüs revizyonu (çeyreklik donmuş görüntü: 7 / 30 / 60 / 90 gün önceki ortalama, 7 ve 30 günde yukarı / aşağı revizyon sayısı, analist sayısı, en yüksek / en düşük) | Alpha Vantage EARNINGS_ESTIMATES | **VERİ YOK (bu işte)** | 2017-06 -> (K63, demo anahtar IBM) | ücretsiz katman anahtar + günde 25 istek (1.411 hisse = 57 gün); kayıt / anahtar yasak. Ücretli seçenek: 49,99 $ / ay (75 istek / dk, ~1 saatte iner). Görüntünün alındığı gün dosyada YOK (sızıntı riski ayrıca sınanmalı) |
| aynı yapıda EPS revizyon görüntüsü | EODHD Fundamentals 'Earnings Trend' | **VERİ YOK (bu işte)** | 2017-06 -> (demo AAPL) | 59,99 $ / ay |
| analist bazında EPS / gelir tahmini tam geçmişi (nokta-zaman) | I/B/E/S (LSEG / WRDS), FactSet, Bloomberg, Capital IQ | **VERİ YOK** | 1976 -> | kurumsal; bireysel erişim yok |
| gelir (satış) tahmini revizyonu | Yahoo / ücretsiz | **YOK** | — | Alpha Vantage / EODHD görüntüsünde revenue_estimate var (ücretli yol) |
| bilanço açıklama günü + saati (ET; saat çözünürlüğü) | Yahoo bilanço takvimi (finance.yahoo.com/calendar/earnings?symbol=) | **VAR, olay kaynağı** | 25 yıla kadar (100 satır) | saat 'at 4 PM' biçiminde (dakika yok) |
| analist EPS sürprizi (tahmin, gerçekleşen, sürpriz %) | Yahoo bilanço takvimi | **VAR, birincil sürpriz** | §15 | eski yıllarda EPS tahmini boş, sürpriz dolu olabilir |
| bilanço günü + analist sürprizi | Nasdaq takvimi (K28; FON_IZI.fi_k28_liste_abd) | **VAR, çapraz denetim + yedek sürpriz** | 2022-12-01 -> 2026-10 | 2017-2021 YOK (SAPMA §14); saat alanı %99 'time-not-supplied' |
| BIST hedef fiyat / tavsiye / EPS revizyonu | İş Yatırım (güncel, 54 hisse), KAP (analist yok), Matriks (bulunamadı) | **BIST VERİSİ YOK** | — | K63; ABD bulgusu BIST'e GENELLENMEZ |
| Avrupa analist not günlüğü | Yahoo (denenmedi) | **AVRUPA VERİSİ YOK** | — | karar en fazla ABD-ADAY |

## 2. Olay (ABD bilanço açıklaması)
- Kaynak: Yahoo bilanço takvimi (tüm dönem; tek kaynak, iki bağımsız dönemde aynı). Evren: V_ABD.pkl (1.411 hisse; FON_IZI.fi_k1_veri; K64 ile aynı yükleyici
  K64.k64_fiyat_yukle, fon krizi kesiği 2026-08-31). Açıklama günü 2016-06-01 .. 2026-08-31.
- r0 = açıklamaya tepki veren ilk işlem günü (hissenin kendi işlem günleri): saat >= 16:00 ET (kapanış sonrası) -> açıklama gününden SONRAKİ ilk işlem günü;
  aksi (açılış öncesi, gün içi, saat yok = 'at 12 AM') -> açıklama günü ya da sonraki ilk işlem günü. r0 açıklama gününden 7 takvim gününden uzaksa olay yok (hisse işlem görmüyor).
- KARAR GÜNÜ d = r0'dan itibaren 5. işlem günü (d = r0 + 4) KAPANIŞI. GİRİŞ = d'den sonraki ilk işlem günü AÇILIŞI (FI_OLCUT girişi).
- REVİZYON PENCERESİ = [açıklama anı, d günü 16:00 ET]. Açıklama anı = takvimdeki saat (ET); saat yoksa açıklama günü 00:00 ET. Not kaydının yayım anı (epoch, UTC ->
  America/New_York) pencere içinde olmalı. Saat bilgisi olmayan kayıt (epoch tam UTC gece yarısı) gün sonu 23:59:59 ET sayılır (d günündeyse pencereye girmez).
- TEKİLLEŞTİRME: aynı hissede r0'lar arası 60 işlem gününden yakın olay tek olaydır; son TUTULAN olaydan en az 60 işlem günü sonra gelen ilk olay tutulur
  (K64.k64_tekil). Aynı hisse-gün birden çok takvim satırı -> sürprizi dolu olan ilk satır.
- Dönem ataması GİRİŞ gününe göre: 2017-2021 (2017-01-01 .. 2021-12-31), 2022-2026 (2022-01-01 .. 2026-12-31), 2023-2026 (2023-01-01 .. 2026-12-31). Bağımsız dönemler: 2017-2021, 2022-2026; 2023-2026 örtüşür (bilgi; BH ailesine girmez).

## 3. Değişkenler (yalnız revizyon penceresindeki kayıtlar; hepsi <= d kapanışı)
KURUM YÖNÜ (bir kurumun penceredeki kayıtları zaman sırasıyla): ORAN = penceredeki son (hedefi olan) kaydın hedefi / pencerenin ilk (önceki hedefi olan) kaydının önceki
hedefi - 1; (1 + ORAN) [0.3333, 3.0] dışındaysa AYKIRI (olası bölünme / veri hatası; oran yok sayılır). YÖN: ORAN sonlu ve != 0 ise işareti;
değilse hedef eylemleri toplamı ({"Raises": 1, "Lowers": -1}) işareti; değilse tavsiye eylemleri toplamı ({"up": 1, "down": -1}) işareti; değilse bütün kayıtlar
['init'] ise BASLA (yeni kapsama; NET paydasına girmez), aksi AYNI. Hedef fiyat yönü tavsiye yönünden önce gelir (çelişkide hedef). Yahoo hedef 0 = yok.
Kurum adı boş kayıt sayılmaz. AYNI yönlü bir kurumun oranı 0 ise (hedefini korumuş) BUYUKLUK ve AYRISMA'ya 0 olarak girer.

| kod | tür | tanım |
|---|---|---|
| N_UP | sürekli | pencerede revizyon yönü YUKARI olan kurum sayısı (kurum başına tek yön; yön kuralı §3). En az 1 kurum kaydı olan olaylarda tanımlı |
| N_DOWN | sürekli | pencerede revizyon yönü AŞAĞI olan kurum sayısı. En az 1 kurum kaydı olan olaylarda tanımlı |
| NET | sürekli | (N_UP - N_DOWN) / (N_UP + N_DOWN + N_AYNI); payda (yön sınıfı olan kurum) >= 2. Yeni kapsama (init) paydaya girmez |
| BUYUKLUK | sürekli | kurum başına hedef değişim oranlarının medyanı; oran = penceredeki SON kaydın hedefi / pencerenin İLK kaydının önceki hedefi - 1; en az 2 oran |
| AYRISMA | sürekli | kurum başına hedef değişim oranlarının standart sapması (ddof = 1); en az 3 oran |
| YON_UYUM | kategorik | NET işareti x analist EPS sürprizi işareti (sürpriz yoksa tepki EAR): AO (sürpriz +, NET +), TO (sürpriz +, NET -), TU (sürpriz -, NET +), AU (sürpriz -, NET -), NOTR (NET = 0 ya da sürpriz = 0), YOK (NET ya da sürpriz yok). Karşıtlıklar: YU_POZ = AO - TO, YU_NEG = TU - AU |

KAPSAMA sınıfı (bilgi): pencerede hiç kurum kaydı olmayan olay KAYIT_YOK; değişkenler NaN (sıfır sayılmaz). 'Hissenin geçmiş kaydı' = pencere sonuna kadar en az bir kayıt.
EPS REVİZYONU: VERİ YOK (§1). Vekil (fiyat tepkisinden, hedef fiyattan EPS türetme vb.) ÜRETİLMEZ.

## 4. Bilanço sürprizi ve tepki
- SÜRPRİZ (YON_UYUM için): Yahoo analist EPS sürprizi % (birincil); yoksa Nasdaq K28 sürprizi (aynı hisse, ±1 gün); yoksa tepki EAR. Kaynak olay başına kaydedilir.
- TEPKİ EAR (katman için; K28 tanımı): C(b) / C(a) - 1 - aynı pencerede bütün hisselerin medyanı; a = açıklama gününden önceki son işlem günü, b = açıklama gününden sonraki ilk işlem günü (FON_IZI.fi_k28_olaylar tanımı). b <= d her zaman (geleceğe bakmaz).

## 5. Sıra ve gruplar (geleceğe bakmaz)
- OLAY İÇİ SIRA (K64.k64_ic_sira, aynen): olayın değeri, karar günü g için [g - 365 gün, g] aralığındaki tekil bilanço olaylarının (kendisi ve aynı gün dahil) değerleri
  içinde (küçük + 0,5 x eşit) / n; n >= 30. ÜST = sıra >= 2/3, ALT = sıra <= 1/3, ORTA arası (K64.k64_grup). Eşit değerler (sayımlarda sık) ortalama sıra alır.
- EAR aynı kuralla üçte bire ayrılır (KATMAN: UST / ORTA / ALT).
- S2'de NET'in ÇÖL İÇİ sırası: aynı kural, çöl olaylarının sinyal günleri üzerinden (K64 §4 'İÇ' sırası).

## 6. S1 — bilanço olaylarında revizyon (asıl soru)
- Örneklem: tekil, girişi olan, FI_OLCUT ile ölçülebilen bilanço olayları. Temel = dönemdeki bütün olaylar.
- Her sürekli değişken (N_UP, N_DOWN, NET, BUYUKLUK, AYRISMA): ÜST ve ALT üçte birin FI_OLCUT hücresi (60 gün; ek 20 gün), ham ÜST - ALT (K64.k64_grup_farki: ay kümeli
  bootstrap, 2000 çekiliş, tohum 67001, %2.5-%97.5) ve **KATMANLI ÜST - ALT** (karar istatistiği; 'ek katkı' = sürpriz kontrolü): EAR üçte biri
  içinde ort(ÜST) - ort(ALT), ağırlık n_u n_a / (n_u + n_a); iki grubu da >= 10 olan katmanlar; aynı ay kümeli bootstrap (aynı tohum). p = 1 - Φ(nokta / sd).
- YON_UYUM: kategori hücreleri (AO, TO, TU, AU tam; NOTR, YOK hafif) ve iki karşıtlık: YU_POZ = AO - TO (olumlu sürprizde revizyonun yukarı olması),
  YU_NEG = TU - AU (olumsuz sürprizde revizyonun yukarı olması); aynı katmanlı istatistik.
- KAYIT_VAR / KAYIT_YOK (bilgi; karara girmez).
- 'EK KATKI VAR (ÜST yönü)' <=> katmanlı n_ÜST >= 30 ve n_ALT >= 30, katmanlı aralık var, katmanlı %95 alt sınır > 0 VE ham ÜST - ALT > 0.
  ALT yönü ayna (katmanlı üst sınır < 0 ve ham < 0).

## 7. S2 — çöl etkileşimi
- Olay: K24 çöl sinyali (K64.k64_olay_k24, DEĞİŞTİRİLMEDEN; FI_K24 eşikleri; tekil, girişi olan). Çöl olayının sinyal günü t'ye kadar son 60 işlem gününde
  (t dahil) karar günü d olan EN SON tekil bilanço olayının değişkenleri alınır (d <= t: bilgi sinyal gününde biliniyor). Yoksa BILANCO_YOK.
- Değişken: NET (COL_NET); çöl içi sıra (§5) ile ÜST / ALT. Karar istatistiği HAM ÜST - ALT; kural K64.k64_ek_katki (K64 §4): ÜST grubunun ortalama eşli farkı > temel
  (bütün çöl olayları) VE %95 alt sınır > 0; ALT ayna. Katmanlama yok (çöl örneklemi küçük).

## 8. Cetvel (FI_OLCUT, aynen)
{"ufuk": 60, "mom": 60, "likit": 20, "mom_kova": 5, "likit_kova": 3, "kriz": "2026-08-31", "bootstrap": 2000, "tohum": 27, "slot": 10, "n_esik": 30, "port_n": 200, "port_yuzde": 0.9, "donem": [["2023", "2023-01-01", "2023-12-31"], ["2024-26", "2024-01-01", "2026-12-31"]], "karar": ["ABD", "AVR"]}. Olay başına r60 = giriş açılışından 60. gün kapanışına; eşli fark = r60 - aynı giriş günü, aynı 60 gün momentum beşliği x likidite
üçlüsündeki öteki hisselerin ortalaması (FI.fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre; K64.k64_olc / k64_hucre ile). Hücre dört şartı: n >= 30, %95 alt > 0,
sıra > 0,50, slot portföyü > 200 eşli rastgele portföyün %90'ı. Ek ufuk 20 gün (aynı yöntem). Maliyet: ABD gidiş-dönüş 20 bp (her olayın
getirisinden ve eşli farkından düşülür; rastgele eş portföyler maliyetsiz: tutucu). Fon krizi: 60 günlük penceresi 2026-08-31'i aşan olay ölçülmez.

## 9. Karar
- Aile değişkenleri: N_UP, N_DOWN, NET, BUYUKLUK, AYRISMA, YU_POZ, YU_NEG, COL_NET. Her biri İKİ YÖNDE (ÜST daha iyi / ALT daha iyi).
- Pazar kararı (ABD): 'ADAY' <=> iki bağımsız dönemin İKİSİNDE de o yönde 'ek katkı VAR' ve BH'den geçiyor. Bağımsız dönemlerden biri ölçülemiyorsa (n < 30 ya da aralık yok)
  'ÖLÇÜLEMEZ'. Aksi 'İZ DEĞİL'.
- İŞARET: ölçülebilen bütün dönem hücrelerinde (2023-2026 dahil) karar istatistiğinin işareti yönle aynı olmalı; bir hücrede dönerse aday düşer -> İZ DEĞİL.
- Genel karar en fazla **ABD-ADAY** (İZ için Avrupa verisi yok; BIST VERİSİ YOK). Grup hücresinin FI_OLCUT dört şartı (brüt / net) bilgi olarak yazılır.

## 10. Çoklu test
BH q = %10; aile = ölçülebilen bütün (aile değişkeni x yön x bağımsız dönem) hipotezleri: en çok 8 x 2 x 2 = 32.
Bonferroni bilgi olarak yazılır. 2023-2026 ve 20 gün sonuçları aileye girmez.

## 11. Güç
K58 (FI_OLCUT plasebo): δ = +%2 etkiyi tek hücrenin dört şartı n = 30 / 100 / 300 / 1000 / 3000'de %4 / %8 / %11 / %13 / %21 olasılıkla görür; cetvel yalnız büyük etkiyi
görür. ÜST - ALT için kaba saptanabilir en küçük etki ≈ 2,8 x σ x √(1/n_ÜST + 1/n_ALT); σ (60 gün tek hisse eşli fark standart sapması) VARSAYIM ≈ 0,25 (ölçülmedi) ->
n 1.000 / 1.000: ≈ %3,1; n 300 / 300: ≈ %5,7; ay kümelemesi bunu büyütür. Gerçek yarı genişlik koşuda raporlanır. 'İZ DEĞİL' = 'etki yok' değildir, 'bu cetvelle görülmedi'dir.

## 12. Geleceğe bakma
- Değişkenler yalnız yayım anı <= d günü 16:00 ET olan kayıtlarla; tarih-yalnız kayıt gün sonu sayılır. Giriş d+1 açılışı. EAR penceresi b <= d.
- Sıralar yalnız geçmiş 365 gün (ve aynı gün) olaylarıyla; katman da öyle.
- S2: bilanço karar günü d <= çöl sinyal günü t; giriş t'den sonraki ilk işlem günü (K64).
- Yahoo not günlüğü 'bugünkü' görüntüdür: geçmiş kayıtların sonradan eklenmiş / tarihinin düzeltilmiş / silinmiş olabileceği DOĞRULANAMAZ (geriye dönük yazım
  riski). Hedef fiyatlar kayıt anındaki değerdir; bölünme düzeltmesi yapılıp yapılmadığı belgelenmemiştir (AYKIRI kuralı §3).
- Yahoo bilanço takviminde geçmiş sürprizler sonradan düzeltilmiş olabilir (beyan).

## 13. Yanlılık
- YAŞAYAN yanlılığı: V_ABD bugün işlem gören hisseler; borsadan çıkanlar yok. Not günlüğü de bugünkü sembollerle çekildi (sembol değiştiren şirketin eski kayıtları
  eksik olabilir).
- Kapsama yanlılığı: analist kapsamı büyük / likit hissede yoğun; N_UP / N_DOWN kurum sayısıyla ölçeklenir (büyüklük etkisi). Eşli fark likidite üçlüsünü ve momentum
  beşlisini eşler; tam büyüklük kontrolü değildir (beyan).
- Kurum = 'analist' (kişi kimliği yok). Aynı kurumun aynı penceredeki birden çok kaydı tek yön sayılır.

## 14. SAPMA / BOŞLUK (iş tanımına göre)
- SAPMA 1 (olay kaynağı): iş tanımı 'Nasdaq takvimi' diyordu; Nasdaq K28 takvimi yalnız 2022-12-01'den başlıyor -> 2017-2021 bağımsız dönemi için bilanço günü YOK.
  Bu yüzden olay kaynağı iki dönemde de aynı olsun diye Yahoo bilanço takvimi (saat + analist sürprizi dahil) seçildi; Nasdaq çapraz denetim ve yedek sürpriz (§15
  örtüşme sayıları).
- SAPMA 2 (sürpriz): birincil sürpriz Yahoo (Nasdaq 2017-2021'de yok); EAR yalnız yedek ve katman.
- SAPMA 3 (karar günü): 'açıklamadan sonraki 5. işlem günü' = r0 + 4 (r0 tepki veren ilk gün = 1. gün) olarak sabitlendi.
- BOŞLUK: EPS tahmin revizyonu (analist bazında ya da konsensüs) VERİ YOK; gelir tahmini revizyonu VERİ YOK; BIST VERİSİ YOK; AVRUPA VERİSİ YOK; analist kişi kimliği YOK.

## 15. Kapsam (yalnız sayım; getiri yok)
Kapsam sayımı (2026-11-12 06:00:40 UTC; `python -I K67.py kapsam`; yalnız SAYI: getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).

- Fiyat evreni V_ABD: 1411 hisse. Yahoo çekimi 2026-11-12 04:21:21 .. 2026-11-12 05:37:25 UTC; istek durumları {'not_tamam': 1400, 'not_yok': 11, 'takvim_tamam': 1410, 'takvim_yok': 1}.
- Not günlüğü: 262976 kayıt, 1400 hisse; ilk 2011-12-08 09:09:00, son 2026-11-11 16:24:50 (ET); saat bilgisi olmayan kayıt payı %0,00.
- Yahoo bilanço takvimi: 86964 satır, 1410 hisse; 1998-09-30 .. 2027-03-30; saat türü {'acilis_oncesi_gun_ici': 42405, 'kapanis_sonrasi': 44363, 'saat_yok': 196}.
- Nasdaq K28 takvimi (çapraz denetim): 20443 satır (2022-12-01 .. 2026-08-28); Yahoo'da ±1 günde bulunan pay %97,3 (aynı gün %95,7); aynı aralıktaki Yahoo satırlarının Nasdaq'ta bulunan payı %98,6; analist sürprizinin işaret uyumu %87,4 (17608 çift).

**Not günlüğü yıl yıl** (kayıt / hisse / yeni hedef dolu / önceki hedef dolu / tavsiye yükseltme / düşürme / yeni kapsama)

| yıl | kayıt | hisse | hedef | önceki hedef | up | down | init |
|---|---|---|---|---|---|---|---|
| 2011 | 3 | 3 | %66,7 | %0,0 | 0 | 1 | 0 |
| 2012 | 6693 | 601 | %88,4 | %73,9 | 752 | 834 | 750 |
| 2013 | 7701 | 649 | %79,7 | %59,0 | 1350 | 1654 | 1374 |
| 2014 | 7756 | 672 | %85,1 | %66,6 | 1232 | 1090 | 1211 |
| 2015 | 7893 | 718 | %78,5 | %59,8 | 1289 | 1308 | 1447 |
| 2016 | 8421 | 748 | %62,1 | %49,3 | 1285 | 1728 | 1509 |
| 2017 | 6022 | 763 | %63,3 | %47,2 | 1180 | 1156 | 1354 |
| 2018 | 10271 | 825 | %79,5 | %69,9 | 1443 | 1149 | 1526 |
| 2019 | 9572 | 873 | %82,6 | %64,2 | 1252 | 1500 | 1667 |
| 2020 | 18455 | 972 | %93,9 | %79,0 | 1892 | 1689 | 1571 |
| 2021 | 15887 | 1099 | %94,9 | %74,3 | 1577 | 1212 | 2248 |
| 2022 | 22819 | 1177 | %96,2 | %82,9 | 1325 | 1881 | 1865 |
| 2023 | 30333 | 1236 | %97,4 | %73,3 | 1597 | 1760 | 1970 |
| 2024 | 36071 | 1326 | %96,9 | %87,1 | 1614 | 1742 | 2121 |
| 2025 | 37465 | 1346 | %97,7 | %91,5 | 1759 | 1553 | 2064 |
| 2026 | 37614 | 1379 | %98,2 | %92,7 | 1510 | 1591 | 1790 |

**Yahoo bilanço takvimi yıl yıl** (satır / hisse / analist sürprizi dolu / EPS tahmini dolu)

| yıl | satır | hisse | sürpriz | EPS tahmini |
|---|---|---|---|---|
| 2015 | 3334 | 858 | %98,7 | %99,0 |
| 2016 | 3470 | 886 | %98,7 | %99,0 |
| 2017 | 3602 | 924 | %98,7 | %99,2 |
| 2018 | 3830 | 985 | %98,6 | %99,3 |
| 2019 | 4028 | 1033 | %98,3 | %99,2 |
| 2020 | 4239 | 1098 | %98,9 | %99,1 |
| 2021 | 4713 | 1243 | %99,2 | %99,3 |
| 2022 | 5105 | 1300 | %99,3 | %99,2 |
| 2023 | 5228 | 1322 | %99,1 | %99,5 |
| 2024 | 5355 | 1362 | %99,0 | %99,1 |
| 2025 | 5478 | 1378 | %98,8 | %99,1 |
| 2026 | 5498 | 1394 | %95,1 | %99,1 |
| 2027 | 1196 | 1196 | %0,0 | %98,4 |

**Bilanço olayları yıl yıl (karar günü d'nin yılı)** (ham / tekil / pencere = girişi var ve 60 günlük penceresi 31.08.2026'dan önce biten tekil / pencerede en az bir kurum kaydı / NET tanımlı)

| yıl | ham | tekil | pencere | revizyon kaydı var | NET tanımlı |
|---|---|---|---|---|---|
| 2016 | 1786 | 1700 | 1700 | 572 (%33,6) | 231 |
| 2017 | 3585 | 2843 | 2843 | 879 (%30,9) | 375 |
| 2018 | 3818 | 3006 | 3006 | 1455 (%48,4) | 808 |
| 2019 | 4016 | 3136 | 3136 | 1140 (%36,4) | 579 |
| 2020 | 4224 | 3355 | 3355 | 1850 (%55,1) | 1106 |
| 2021 | 4702 | 3720 | 3720 | 1903 (%51,2) | 1089 |
| 2022 | 5105 | 4030 | 4030 | 2428 (%60,2) | 1555 |
| 2023 | 5229 | 4097 | 4097 | 2898 (%70,7) | 2036 |
| 2024 | 5354 | 4216 | 4216 | 3255 (%77,2) | 2418 |
| 2025 | 5479 | 4219 | 4219 | 3221 (%76,3) | 2367 |
| 2026 | 4011 | 2901 | 1653 | 1339 (%81,0) | 1032 |

**S1 olayları (giriş dönemine göre)**

| dönem | ham | tekil | pencere | revizyon kaydı var (pay) | hissenin geçmiş kaydı var | EAR var | sürpriz kaynağı Yahoo / Nasdaq / EAR / yok |
|---|---|---|---|---|---|---|---|
| 2017-2021 | 20347 | 16062 | 16062 | 7227 (%45,0) | 14254 | 16062 | 15859 / 0 / 203 / 0 |
| 2022-2026 | 25176 | 19461 | 18215 | 13141 (%72,1) | 17413 | 18215 | 18041 / 56 / 118 / 0 |
| 2023-2026 | 20071 | 15431 | 14185 | 10713 (%75,5) | 13704 | 14185 | 14041 / 56 / 88 / 0 |

**S1 değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; hücre = değer / ÜST / ORTA / ALT; köşeli parantez = EAR katmanı olan ÜST / ALT, katmanlı karar istatistiğine girecek olanlar)

| değişken | 2017-2021 | 2022-2026 | 2023-2026 |
|---|---|---|---|
| N_UP | 7227 / 2249 / 2928 / 2050 [2249 / 2050] | 13141 / 4413 / 3607 / 5121 [4413 / 5121] | 10713 / 3828 / 2906 / 3979 [3828 / 3979] |
| N_DOWN | 7227 / 2513 / 1311 / 3403 [2513 / 3403] | 13141 / 3961 / 2808 / 6372 [3961 / 6372] | 10713 / 2865 / 2289 / 5559 [2865 / 5559] |
| NET | 3957 / 1976 / 710 / 1271 [1976 / 1271] | 9408 / 3278 / 2910 / 3220 [3278 / 3220] | 7853 / 2868 / 2520 / 2465 [2868 / 2465] |
| BUYUKLUK | 3598 / 1215 / 1171 / 1212 [1215 / 1212] | 8936 / 2964 / 2926 / 3046 [2964 / 3046] | 7452 / 2604 / 2501 / 2347 [2604 / 2347] |
| AYRISMA | 2138 / 753 / 716 / 669 [753 / 669] | 6261 / 2180 / 2054 / 2027 [2180 / 2027] | 5288 / 1796 / 1726 / 1766 [1796 / 1766] |

**Katman (EAR üçte biri) x grup** (ÜST grubu UST / ORTA / ALT katmanında; ALT grubu aynı; pencereli tekil olaylar)

| değişken | dönem | ÜST: EAR üst / orta / alt | ALT: EAR üst / orta / alt |
|---|---|---|---|
| N_UP | 2017-2021 | 1127 / 690 / 432 | 334 / 520 / 1196 |
| N_UP | 2022-2026 | 2352 / 1321 / 740 | 952 / 1389 / 2780 |
| N_UP | 2023-2026 | 2008 / 1165 / 655 | 694 / 1110 / 2175 |
| N_DOWN | 2017-2021 | 479 / 645 / 1389 | 1523 / 1133 / 747 |
| N_DOWN | 2022-2026 | 671 / 1008 / 2282 | 3201 / 2032 / 1139 |
| N_DOWN | 2023-2026 | 380 / 753 / 1732 | 2756 / 1777 / 1026 |
| NET | 2017-2021 | 1041 / 596 / 339 | 213 / 273 / 785 |
| NET | 2022-2026 | 1950 / 947 / 381 | 469 / 776 / 1975 |
| NET | 2023-2026 | 1701 / 836 / 331 | 311 / 610 / 1544 |
| BUYUKLUK | 2017-2021 | 696 / 328 / 191 | 223 / 288 / 701 |
| BUYUKLUK | 2022-2026 | 1792 / 728 / 444 | 504 / 696 / 1846 |
| BUYUKLUK | 2023-2026 | 1558 / 648 / 398 | 334 / 555 / 1458 |
| AYRISMA | 2017-2021 | 352 / 180 / 221 | 252 / 214 / 203 |
| AYRISMA | 2022-2026 | 952 / 409 / 819 | 632 / 743 / 652 |
| AYRISMA | 2023-2026 | 777 / 357 / 662 | 549 / 645 / 572 |

**YON_UYUM kategorileri** (AO / TO / TU / AU / NOTR / YOK; köşeli parantez = EAR katmanı olan AO / TO / TU / AU)

| dönem | sayılar | katmanlı |
|---|---|---|
| 2017-2021 | 2308 / 632 / 296 / 382 / 339 / 12105 | [2308 / 632 / 296 / 382] |
| 2022-2026 | 4028 / 2305 / 823 / 1429 / 823 / 8807 | [4028 / 2305 / 823 / 1429] |
| 2023-2026 | 3564 / 1801 / 726 / 1094 / 668 / 6332 | [3564 / 1801 / 726 / 1094] |

**S2 çöl x revizyon** (K24 tekil çöl olayları, pencereli; son 60 işlem gününde bilanço karar günü olan; NET tanımlı; NET çöl içi ÜST / ORTA / ALT)

| dönem | çöl olayı | bilanço var | NET var | ÜST / ORTA / ALT |
|---|---|---|---|---|
| 2017-2021 | 2589 | 1890 | 477 | 179 / 101 / 167 |
| 2022-2026 | 3519 | 2502 | 1309 | 419 / 316 / 574 |
| 2023-2026 | 2468 | 1905 | 1049 | 351 / 277 / 421 |

Bağımsız dönemlerde grubu n < 30 olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak; ölçülebilen olay daha az olabilir) hücreler: yok.

## 16. Koşu
1. `python K67.py indir`  (yapıldı; önbellek /tmp/k67_yahoo, sha256 yukarıda)
2. `python -I K67.py kapsam`  (yapıldı; sayılar §15)
3. ana oturum bu ön kaydı denetler ve git'e işler
4. `python -I K67.py kos` -> k67_olaylar.csv.gz, k67_s1.csv, k67_s1_fark.csv, k67_s2.csv, k67_karar.csv, k67_meta.json, K67_RAPOR.md
5. `python K67.py rapor` -> raporu çıktılardan yeniden yazar

## 17. Değişmezlik
K67_ESIK ya da içe alınan tanımlar (FI_OLCUT, FI_K24, K64 olay ayarları) değişirse ESIK_SHA256 değişir ve koşu durur. Veri (V_ABD.pkl, liste_abd.csv.gz, Yahoo önbelleği)
ya da içe alınan kod (FON_IZI.py, K60.py, K64.py) değişirse sha256 tutmaz ve koşu durur.
