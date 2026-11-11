# K60 veri planı (yalnız veri hazırlığı; sinyal ölçümü yok)

Yazım zamanı: 2026-11-11 10:52:39 UTC. K60_veri v1.0 (2026-11-11): K60 veri hazırlığı (SEC frames 2009-2026, Yahoo günlük fiyat 2010-2026); ölçüm yok. Üreten: `python K60_veri.py plan`. Ağ kullanılmadı.

## 1. Neden
K59 temel veriye dayalı sinyalleri 66 ayda ölçebildi (frames önbelleği 2020Q1–2026Q2, geniş evren fiyatı 2020'den). 68 ayda rastgele sinyal
t ≈ 3'e ulaşabiliyor. K60 üç dönemli (KEŞİF 2016–2021, DOĞRULAMA 2022–2023, KASA 2024 – Ağu 2026); KEŞİF için temel veri en geç 2014'ten,
yıllık büyüme ve 8 çeyreklik sürpriz ölçüleri için daha da geriden gerekir. Plan: temel veri 2009Q1'den, fiyat 2010-01-01'den.

## 2. SEC XBRL frames: istek listesi
Uç: `https://data.sec.gov/api/xbrl/frames/{tax}/{etiket}/{birim}/{donem}.json`. Dönem adı: `CYyyyyQn` = çeyreklik süre (yaklaşık 91 gün), `CYyyyyQnI` = çeyrek sonu anlık değer, `CYyyyy` = yıllık süre.
Tam liste (her satır bir istek, adresi ve hedef dosyasıyla): `K60_SEC_ISTEK_LISTESI.csv`.

| grup | taksonomi | etiket | birim | çeyrek dönemleri (adet) | yıllık dönemler (adet) | eski önbellekte | istek | hangi sinyal için | not |
|---|---|---|---|---|---|---|---|---|---|
| A | us-gaap | Revenues | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 32 | 55 | REV_SURP, satış ivmesi, GP_A payı | gelir etiketi (üçünden biri dolu olur) |
| A | us-gaap | RevenueFromContractWithCustomerExcludingAssessedTax | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 32 | 55 | REV_SURP, satış ivmesi, GP_A payı | gelir etiketi (üçünden biri dolu olur) |
| A | us-gaap | SalesRevenueNet | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 32 | 55 | REV_SURP, satış ivmesi, GP_A payı | gelir etiketi (üçünden biri dolu olur) |
| A | us-gaap | NetIncomeLoss | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 32 | 55 | ROE_TTM, ROA_Q, SUE_SRW, EP, ACCRUALS |  |
| A | us-gaap | StockholdersEquity | USD | CY2009Q1I .. CY2026Q2I (70) | — | 26 | 44 | ROE_TTM, BM |  |
| A | us-gaap | Liabilities | USD | CY2009Q1I .. CY2026Q2I (70) | — | 26 | 44 | kaldıraç (X2), F_SCORE |  |
| A | us-gaap | LiabilitiesAndStockholdersEquity | USD | CY2009Q1I .. CY2026Q2I (70) | — | 26 | 44 | toplam varlık yedeği | Assets ile aynı sayı (bilanço eşitliği) |
| A | dei | EntityCommonStockSharesOutstanding | shares | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | NSI_1Y, piyasa değeri (BM, EP, CFP, küçüklük) | kapak sayfası pay sayısı; eski önbellekte YOK, tam aralık iner; tarih çeyrek sonu değil kapak günüdür |
| B | us-gaap | Assets | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | ASSET_G, ROA_Q, GP_A, ACCRUALS, F_SCORE |  |
| B | us-gaap | AssetsCurrent | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | F_SCORE (cari oran) | banka / sigorta bildirmez |
| B | us-gaap | LiabilitiesCurrent | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | F_SCORE (cari oran) | banka / sigorta bildirmez |
| B | us-gaap | CashAndCashEquivalentsAtCarryingValue | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | RUNWAY |  |
| B | us-gaap | LongTermDebt | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | F_SCORE (kaldıraç) | LongTermDebtNoncurrent ile dönüşümlü |
| B | us-gaap | LongTermDebtNoncurrent | USD | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | F_SCORE (kaldıraç) | LongTermDebt ile dönüşümlü |
| B | us-gaap | GrossProfit | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | GP_A, F_SCORE (brüt marj) | yoksa gelir - maliyet |
| B | us-gaap | CostOfRevenue | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | GP_A | CostOfGoodsAndServicesSold ile dönüşümlü |
| B | us-gaap | CostOfGoodsAndServicesSold | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | GP_A | CostOfRevenue ile dönüşümlü |
| B | us-gaap | OperatingIncomeLoss | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | kârlılık ailesi (ikinci dalga) |  |
| B | us-gaap | ResearchAndDevelopmentExpense | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | kârlılık / yatırım ailesi (ikinci dalga) |  |
| B | us-gaap | IncomeTaxExpenseBenefit | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | kârlılık ailesi (ikinci dalga) |  |
| B | us-gaap | DepreciationDepletionAndAmortization | USD | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | ACCRUALS (bilanço yöntemi), nakit kâr | çoğu şirkette nakit akış tablosu kalemi: ÇEYREKLİK EKSİK, YILLIK güvenilir |
| C | us-gaap | NetCashProvidedByUsedInOperatingActivities | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | CFP, ACCRUALS, F_SCORE, RUNWAY | YALNIZ YILLIK |
| C | us-gaap | PaymentsToAcquirePropertyPlantAndEquipment | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | yatırım ailesi | YALNIZ YILLIK |
| C | us-gaap | PaymentsForRepurchaseOfCommonStock | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | NET_PAYOUT_YLD | YALNIZ YILLIK |
| C | us-gaap | ProceedsFromIssuanceOfCommonStock | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | NET_PAYOUT_YLD | YALNIZ YILLIK |
| EK | us-gaap | PaymentsOfDividends | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | NET_PAYOUT_YLD (envanter satır 48 temettü ister) | YALNIZ YILLIK |
| EK | us-gaap | PaymentsOfDividendsCommonStock | USD | — | CY2009 .. CY2025 (17) | 0 | 17 | NET_PAYOUT_YLD | PaymentsOfDividends ile dönüşümlü; YALNIZ YILLIK |
| EK | us-gaap | CommonStockSharesOutstanding | shares | CY2009Q1I .. CY2026Q2I (70) | — | 0 | 70 | NSI_1Y, piyasa değeri (yedek) | bilanço günü pay sayısı; kapak sayısı olmayan / çok sınıflı şirketler için yedek |
| EK | us-gaap | WeightedAverageNumberOfDilutedSharesOutstanding | shares | CY2009Q1 .. CY2026Q2 (70) | CY2009 .. CY2025 (17) | 0 | 87 | NSI_1Y, piyasa değeri (yedek) | ağırlıklı ortalama pay; çok sınıflı şirketlerde tek boyutsuz pay sayısı çoğunlukla budur |

- **A** = K57 / K59'un kullandığı etiketler. 2020Q1–2026Q2 çeyrekleri ve 2020–2025 yılları eski önbellekte (`/tmp/secframes`, K59 girdisi) durur:
  yeniden indirilmez, o klasöre yazılmaz (K59 veri sha256'ları değişmez). İnen bölüm: 2009Q1–2019Q4 (44 çeyrek) ve süreli etiketlerde
  2009–2019 yılları (11). `dei/EntityCommonStockSharesOutstanding` eski önbellekte hiç yok: tam aralık (70 çeyrek sonu) iner.
  Eski önbellek o gün yerinde değilse aynı çerçeveler de yeni klasöre iner (komut kendisi bakar).
- **B** = ilk 30 sinyalin istediği yeni bilanço ve gelir tablosu etiketleri, 2009Q1–2026Q2.
- **C** = nakit akış kalemleri, YALNIZ yıllık çerçeve (2009–2025).
- **EK** = iş tanımındaki listede OLMAYAN, alt ajanın eklediği dört etiket (`--ek hayir` ile çıkarılır): temettü ödemesi (NET_PAYOUT_YLD envanterde
  temettüyü de ister) ve iki yedek pay sayısı (kapak sayfası pay sayısı çok sınıflı şirketlerde boyutlu bildirilir, frames'e girmez).

Sayım: K60'ın istediği toplam çerçeve 1.916; eski önbellekte 206; **indirilecek 1.710 istek**
(A 422, B 1.029, C 68, EK 191).
Bu klasörde şu an inmiş olan: 0; kalan: 1.710.

### Hangi kalem hangi sıklıkta güvenilir
- **Anlık (bilanço) kalemleri** — özkaynak, yükümlülük, varlık, dönen varlık, kısa vadeli yükümlülük, nakit, uzun vadeli borç, pay sayısı:
  her çeyrek sonu güvenilir.
- **Gelir tablosu kalemleri** — gelir, net kâr, brüt kâr, satışların maliyeti, faaliyet kârı, Ar-Ge, vergi: 1.–3. çeyrek çeyreklik çerçevede
  gelir. **4. çeyrek çoğu şirkette ayrı bildirilmez**; yıllık çerçeveden türetilir (yıl − ilk üç çeyrek; K57 `k57_abd_temel_tablo` kuralı).
  Bu yüzden süreli her etiket için yıllık çerçeve de iner.
- **YALNIZ YILLIK güvenilir** — faaliyet nakit akışı, yatırım harcaması, hisse geri alımı, hisse ihraç geliri, temettü ödemesi (grup C ve EK),
  ayrıca amortisman (`DepreciationDepletionAndAmortization`; çeyreklik çerçevesi de iner ama eksiktir). Neden: şirketler nakit akış tablosunu
  yılbaşından bugüne (3, 6, 9 ay) bildirir; frames yalnız ~91 günlük dönemi "çeyrek" sayar, 6 ve 9 aylık değerler hiçbir çerçeveye girmez.
  Çeyreklik nakit akışı gerekiyorsa (ör. RUNWAY'in çeyreklik sürümü) kaynak SEC finansal tablo veri setleridir (envanter bölüm C satır 2);
  bu planda yok. Yıllık değer, mali yıl bittikten sonraki 10-K ile bilinir.
- Pay sayısı: `dei` kapak sayısının tarihi çeyrek sonu değil kapak günüdür (çeyrek sonundan haftalar sonra); frames en yakın çeyreğe yazar.

### İstek sayısı, boyut, süre
| kalem | değer |
|---|---|
| istek sayısı | 1.710 (frames 1.710) |
| hız sınırı | saniyede en çok 8 istek (SEC sınırı 10); bütün iş parçacıkları tek sayaçtan geçer, istekler arası en az 130 ms |
| tahmini boyut | ~1,04 GB (eski önbellekten ölçüldü (174 dosya); anlık 0,78 MB, çeyreklik 0,45 MB, yıllık 0,62 MB / çerçeve). 2009–2011 çerçeveleri daha küçük olacağı için üst tahmindir |
| tahmini süre | en az 3,7 dk (hız sınırının izin verdiği); beklenen 4–11 dk (aktarım hızına bağlı) |
| hedef klasör | `/tmp/k60_secframes` (yeni; `K60_SECFRAMES` ile değişir) |
| kaldığı yerden | diskte geçerli dosyası olan çerçeve yeniden istenmez; yarım dosya (`.yarim`) silinir; her dosyanın sha256'sı `_manifest.json`'da |
| 404 | o etiket o dönemde hiç bildirilmemiş (ör. `RevenueFromContractWithCustomerExcludingAssessedTax` 2017 öncesi): `{}` işareti yazılır, hata değildir |
| 403 / 407 | SEC ya da ağ geçidi reddi: indirme hemen durur; aynı komut sonra kaldığı yerden sürer |

Komut (ana oturum çalıştırır; kimlik satırı yalnız ortam değişkeninden okunur, hiçbir dosyaya ve günlüğe yazılmaz):

    K60_SEC_UA='<ad> <iletişim adresi>' python K60_veri.py indir_sec

Sonra: `python K60_veri.py denetle` (manifest sha256 + etiket x dönem şirket sayıları) ve `python K60_veri.py ozet`.

### İsteğe bağlı: EDGAR başvuru dizini (`indir_sec --dizin evet`)
Frames yanıtında başvuru günü (`filed`) alanı YOKTUR (alanlar: accn, cik, entityName, loc, start, end, val) ve `accn` özgün başvuruyu değil o
değeri EN SON bildiren başvuruyu gösterir. Bilgi tarihi için iki yol var: (a) yedek kural: çeyrek sonu + 90 gün; (b) EDGAR çeyreklik
dizini (`https://www.sec.gov/Archives/edgar/full-index/{yil}/QTR{c}/master.gz`; 71 dosya, 2009Q1–2026Q3, dosya başına ~8 MB, toplam ~0,6 GB) her şirketin her 10-Q / 10-K
başvurusunun gününü verir; K57 `_k57_abd_bilgi_tarihleri` kuralı (çeyrek sonundan sonraki ilk 10-Q / 10-K) bununla 2009'a uzatılabilir.
Dizin varsayılan olarak İNMEZ (iş tanımında yoktu); öneri: `--dizin evet` ile indirilmesi. Aynı kimlik satırı ve hız sınırı kullanılır.

## 3. Yahoo günlük fiyat
| kalem | değer |
|---|---|
| uç | `https://query1.finance.yahoo.com/v8/finance/chart/{T}` (K57-B ile aynı; tarayıcı kimliği, `events=div,splits`, `includeAdjustedClose=true`) |
| aralık | 2010-01-01 .. 2026-11-12 (okuyucular 2026-08-31'de keser; bölünme olayları indirme gününe kadar alınır ki o günkü fiyat doğru kurulsun) |
| evren | 4.755 sembol: K57-B geniş evren tablosu (`evren_b1.csv`) + V_ABD sembolleri; yalnız bugün kodu olanlar |
| istek | sembol başına 1; 3 iş parçacığı, istekler arası 0,3 sn, 4 deneme; art arda 25 başarısızlıkta durur |
| hedef klasör | `/tmp/k60_fiyat` (yeni; `K60_FIYAT` ile değişir). `/tmp/k57b_fiyat` (K59 girdisi) okunmaz, yazılmaz |
| tahmini boyut / süre | ~1,4 GB; ~23–43 dk (11 Kasım koşusunda ölçülen: 1,36 GB, 23 dk) |
| e-posta | gerekmez |

Komut: `python K60_veri.py indir_fiyat`

## 4. Bu planın kapsamadıkları
- Batan şirketler (yaşayanlar evreni; EVREN_SECENEKLERI.md). Çeyreklik nakit akışı (SEC finansal tablo veri setleri). İçeriden işlem, 13F,
  açığa satış, analist verisi (envanter bölüm C satır 3–10). Ham SEC ve fiyat verisi repoya konmaz; türetilmiş tabloların `islenmis-veri`
  dalına konması ana oturumun / Cemal'in kararıdır.
