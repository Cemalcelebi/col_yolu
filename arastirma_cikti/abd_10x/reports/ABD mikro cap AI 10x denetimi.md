# Dört mikro-cap'te 10x yok; QMLS tezini seyrelme öldürüyor

**Değerlendirme tarihi: 4 Kasım 2026. Fiyatlar 3 Kasım 2026 kapanışı.** Kaynak türleri: **[R]** resmi SEC/EDGAR belgesi (10-Q, 10-K, 8-K Item 1.01/2.02, 424B4, DEF 14A, 20-F, 6-K, Form 4), **[PR]** şirket basın bülteni veya 8-K Item 7.01 "furnished" sunum (bağımsız kanıt değil), **[İ]** ikincil kaynak (StockAnalysis, Yahoo, yerel basın, blog). "Hesap" = notlardaki kaynak rakamlardan türetilen aritmetik.

Özet (BLUF): Önceki araştırmanın dört adayından hiçbiri bugün "al" seviyesinde değil. Dördü de 30/60/90 günde %30–60 düştü, ama bu düşüş sektör geneliyle aynı; yani ucuzlama değil, risk fiyatlaması var. En sağlam aday **DGXX** (Cerebras ile imzalı, SEC'e exhibit olarak verilmiş 10 yıllık take-or-pay sözleşme; nakit $128M; borç yok). Ama onun da 15 MW'lık ilk fazı 15 Aralık 2026 hedefinde ve $200M kredisi henüz kapanmadı. **QMLS**'in sorunu sözleşmelerin gerçekliği değil (Q2 rakamları birebir doğru), sermaye yapısıdır: ATW tahvili her ay "8 günlük en düşük VWAP'ın %93'ü" ile hisseye dönüyor, özkaynak negatif, 10-Q'da "going concern" şüphesi var ve 12–16 Ocak 2027'de 12,7 milyon hisse (dolaşımın ~%38'i) lock-up'tan çıkıyor. **AIB** Nebius sözleşmesini SEC'e exhibit olarak vermedi, değerini geri çekti, ~$800M projenin finansmanı yok. **VIVO** (doğru kod; VVPR değil) bağlayıcı kiracısı olmayan, nakdi $2M, capex ihtiyacı $411M olan bir şirket. Sektör taban oranları acımasız: 2024–26'da AI sözleşmesi duyuran 12 küçük şirketten hisse başına 10x yapan sıfır; mikro-cap'lerin beşi de duyurudan sonra %50–97 düştü. Mevcut zarardaki QMLS pozisyonu için beklenen getiri ≈ sıfır, ama dağılım sola çarpık: tutmanın gerekçesi yalnız Q3 10-Q (16–23 Kasım) ile ATW/nakit tablosu netleşirse vardır.

---

## 1) Tek sayfalık sonuç

**Karar:** "Hiçbir aday yeterince güçlü değil" sonucu geçerli. Dördünden hiçbiri bugün yeni alım için önerilmiyor. İzleme listesinde kalacak tek isim DGXX; karar noktası 13 Kasım (Q3) ve 15 Aralık (RFS).

**Sıralama (kalite, "al" değil):**

| Sıra | Aday | Neden |
|---|---|---|
| 1 | DGXX | Tek isim: imzalı + exhibit'li sözleşme, kendi trafo merkezi, borçsuz bilanço. Finansman ve teslim henüz kanıtlanmadı. |
| 2 | DUOT (evren dışı) | Nakit $112M, borç ~$1M, iki sözleşme (>$400M + $111M); edge ölçeği küçük. |
| 3 | AIB | EV ≈ $13–30M, yani piyasa Nebius sözleşmesine sıfır değer veriyor. Opsiyon gibi ucuz, ama finansman yok, teslim Q4 2027. |
| Mevcut dörtlü | DGXX > AIB > QMLS > VIVO | |
| Tamamen elenenler | VIVO, GPUS, BGDE, DRK, PWCM, SGRX, SOBR, NUAI | Kiracı yok / seyrelme / bilanço ölü. |
| Şu an alınmayacaklar | Hepsi, DGXX dahil | Tetikleyici tarihler gelmeden önce (bkz. §13). |

**En önemli 5 bulgu:**
1. QMLS'in Q2 2026 rakamları 10-Q ile birebir doğru **[R]**; ama $523,4M sözleşme, $209M ARR, 3.088 GPU ve $123,6M TFC kiralaması yalnız basın bülteninde var, 8-K yok ([10-Q 25 Ağu 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm); [PR 15 Eki 2026](https://finviz.com/news/402901/qumulusai-puts-719-million-blackwell-agreement-into-production-signed-customer-contracts-surpass-500-million)).
2. QMLS'te H1 2026 işletme nakit akışı +$22,3M, ama bunun $30,5M'ı müşteri ön ödemesi; ön ödeme hariç −$8,2M (hesap). 10-Q "substantial doubt about going concern" diyor **[R]**.
3. DGXX–Cerebras sözleşmesi dört adayın tek gerçek bağlayıcı belgesidir: 8-K Item 1.01 + redakte Exhibit 10.1, $195/kW/ay take-or-pay, %3 artış **[R]** ([8-K 8 May 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea0289585-8k_digi.htm); [10-Q](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm)). Ama teslim tarihleri, gecikme cezaları ve ön ödeme tutarı redakte.
4. AIB'nin "$1,32 Mlr sözleşme değeri" ifadesini şirket 20 Ekim sunumunda geri çekti: "No AIB rate or contract value is derived or implied" **[PR]** ([8-K 20 Eki 2026](https://www.sec.gov/Archives/edgar/data/0002070542/000121390026110826/ea030897401ex99-1.htm)).
5. Sektör kohortunda (n=12, 2024–26 AI sözleşmesi duyuranlar) hisse başına 10x: 0. 10x piyasa değeri yapan IREN/WULF/CIFR/APLD/CORZ bunu 2022 diplerinden, sözleşme ÖNCESİ, zaten $0,6–3,9 Mlr değerdeyken yaptı **[İ]** ([sektör notu, StockAnalysis piyasa değeri sayfaları](https://stockanalysis.com/stocks/apld/market-cap/)).

**En önemli 5 düzeltme (önceki araştırma yanlıştı):**
1. QMLS bir IPO değil, **doğrudan listeleme**: şirket sıfır dolar topladı, aracı kurum yok ([424B4](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm)) **[R]**.
2. AIB = AIB Data Centers Inc. (eski BlockchAIn Digital Infrastructure); **Applied UV ile ilgisi yok**. "CLT1" sahası Charlotte NC değil, **Spartanburg County, Güney Carolina** ([10-K FY2025](https://www.sec.gov/Archives/edgar/data/2070542/000121390026036810/ea0282624-10k_blockchain.htm); [10-Q](https://www.sec.gov/Archives/edgar/data/2070542/000121390026089151/ea0301093-10q_aibdata.htm)) **[R]**.
3. VivoPower'ın kodu **VIVO** (VVPR değil); Mo i Rana capex'i $45–55M değil **≈$411M**; kiracı "LOI aşamasında" değil, **bağlayıcı kiracı yok** ve tercih edilen kiracı düşürüldü ([20-F 2 Kas 2026](https://www.sec.gov/Archives/edgar/data/1681348/000149315226049646/form20-f.htm)) **[R]**.
4. DGXX hisse sayısı 108,48M değil: temel **102,06M** (SV eşdeğeri), şirketin kendi tam seyreltilmiş rakamı **111,54M** ([DEF 14A 2 Kas 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm)) **[R]**. Nakit $142,4M değil **$128,1M** (PR'daki rakam $14,3M kriptoyu içeriyor) **[R]**.
5. AIB için "$25–30M Nebius ön ödemesi" hiçbir belgede yok; VIVO için "2,125M koşullu warrant" 20-F'de yok. İkisi de **bulunamadı**.

---

## 2) Önceki araştırmanın rakam rakam denetimi

### QMLS

| İddia | Durum | Doğru değer, kaynak türü, tarih |
|---|---|---|
| Q2 2026 gelir $6,7M (+%118) | DOĞRU | $6.712.805; [R] 10-Q, 25 Ağu 2026 |
| Compute geliri $5,6M (%84) | DOĞRU | $5.608.946; [R] 10-Q |
| Brüt marj %67 | DOĞRU | %66,6; [R] 8-K Ex.99.1 + 10-Q maliyet satırı |
| Net zarar $22,8M, $19,2M nakit dışı tahvil zararı | DOĞRU | $(22.776.206); tahvil ihraç zararı $(19.241.000); H1 toplamı $(73.881.850); [R] 10-Q |
| Düz. FAVÖK −$0,8M | DOĞRU | $(782)k, şirket tanımlı non-GAAP; [PR] 8-K Ex.99.1 |
| İşletme nakit akışı +$22,3M | DOĞRU, EKSİK | $22.305.214; içinde ertelenmiş gelir +$30.460.939; hariç ≈ −$8,2M (hesap); [R] 10-Q |
| Nakit $20M | DOĞRU | $19.967.188 + kısıtlı $19.925.104 (listelemeyle serbest kaldı); [R] 10-Q |
| GPU filosu 952 → 3.088 | DOĞRULANAMADI | Yalnız [PR]; 10-Q'da "3,088" geçmiyor |
| 21 sözleşme, $169,7M take-or-pay | DOĞRU | [R] 10-Q + [PR] 8-K Ex.99.1 |
| Birikmiş sözleşme $523,4M; ARR ~$209M | DOĞRULANAMADI | Yalnız [PR] 15 Eki 2026; 8-K yok, exhibit yok, müşteri adı yok. Resmi karşılığı: RPO $173,1M (30 Haz 2026) [R] 10-Q Not 4 |
| $240,9M Eylül sözleşmeleri ($211,9M + $29,1M) | DOĞRULANAMADI | Yalnız [PR] 29 Eyl 2026 |
| "IPO" 16 Tem 2026 | YANLIŞ | Doğrudan listeleme; $0 hasılat; Chardan "financial adviser"; [R] 424B4 15 Tem 2026 |
| Hisse sayısı 33,46M | DOĞRU | 33.458.515 (20 Ağu 2026); [R] 10-Q kapak |
| ATW $90M dönüştürülebilir | DOĞRU, EKSİK | İki $45M tesis; yalnız $30M fonlandı; kalan $60M "green shoe" şartlı; [R] 424B4 |
| Lock-up 180 gün | DOĞRU | 12.678.323 + 610.376 hisse; "six months"/180 gün → 12–16 Oca 2027; [R] 424B4 |
| TFC kiralama $123,6M | DOĞRULANAMADI | Yalnız [PR] 22 Eki 2026; 8-K yok. Resmi: $26,0M master lease (10-Q Not 25) |
| USD.AI $500M "non-recourse" | YANLIŞ | 424B4: "non-binding memorandum of understanding… does not represent committed financing"; çekilen $18,9M (30 Haz) + $15,3M (7 Ağu); [R] |
| hosted.ai "ortak girişim/yatırım" | YANLIŞ | Yazılım lisansı; ücretleri QMLS ÖDÜYOR ($10k–$168k/ay); [R] 424B4 |
| Going concern yok | YANLIŞ | 10-Q Not 1: "substantial doubt… going concern"; yönetim planlarla gideriyor; [R] |
| Q3 sonuç 25 Kas 2026 | DOĞRULANAMADI | Veri sağlayıcı tahmini [İ]; yasal son tarih 16 Kas, NT 10-Q ile 23 Kas (hesap) |
| Piyasa değeri $118M, EV $229M | DOĞRU [İ] | StockAnalysis 3 Kas; EV Haziran yüz değerle ≈$182M, TFC sonrası ≈$280M (hesap) |

### DGXX

| İddia | Durum | Doğru değer, kaynak türü, tarih |
|---|---|---|
| Cerebras 40 MW, 10 yıl, ~$1,1 Mlr, bağlayıcı | DOĞRU | 8-K Item 1.01 (8 May 2026) + Ex.10.1 redakte sözleşme; imzalar Amar/Feldman 4 May 2026; [R] |
| ~$2,5 Mlr (uzatmayla) | DOĞRULANAMADI | 8-K gövdesinde şirket ifadesi; $195/kW ile 7 yıl uzatma ≈$2,0 Mlr çıkar (hesap); şirket rakamı say |
| $195/kW/ay, %3 artış | DOĞRU | [R] 10-Q Q2 2026 |
| Faz 1 15 MW 15 Ara 2026; Faz 2 25 MW Q1 2027 | DOĞRU (HEDEF) | 8-K "targeted"; Faz 2 finansman + Cerebras onayına bağlı (Ex.10.1 §2.2(b)); [R] |
| $200M borç finansmanı "sağlandı" | DOĞRULANAMADI | Taahhüt mektubu, kredi veren isimsiz, Goldman sendikasyon, 90 günde kapanış (~11 Oca 2027); yalnız [PR] 13 Eki 2026; 8-K yok |
| Nakit $142,4M (30 Haz) | YANLIŞ | $128.121.977 nakit + $14.303.261 dijital varlık; [R] 10-Q. ~$135M (13 Eki) yalnız [PR] |
| Borç yok | DOĞRU | Toplam yükümlülük $14,5M; [R] 10-Q |
| Hisse 108,48M | YANLIŞ | 101.396.689 SV + 3.333 PV (×200 = 666.600) = 102,06M temel; tam seyreltilmiş 111.540.742; [R] DEF 14A 2 Kas 2026 |
| Portföy 201,7 MW | DOĞRU, YANILTICI | 60 MW AL + 141,7 MW NY; AI'ya hazır ≈1 MW (ARMS 200); NY madencilik/peaker; [R] 10-Q, 10-K |
| TSXV: DGX | YANLIŞ | 27 Şub 2026'dan beri Cboe Canada; [İ] |
| Q3 sonuç 13 Kas 2026 | DOĞRU | [PR] 28 Eki 2026, 08:30 ET |
| 2027 kontratlı run-rate ~$140M | DOĞRULANAMADI | 40 MW × $195 = $93,6M/yıl (hesap); fark açıklanmadı; [PR] 14 Ağu |
| CEO içeriden alım | DOĞRU | Michel Amar 20.000 hisse @ $2,7628, 14 Eki 2026; [R] Form 4 |
| Düz. FAVÖK +$3,3M | DOĞRU, DÜŞÜK KALİTE | $5,8M hisse bazlı ödeme eklenmiş; gelir $6,6M; [PR] |

### AIB

| İddia | Durum | Doğru değer, kaynak türü, tarih |
|---|---|---|
| Applied UV / "AIB" | YANLIŞ | AIB Data Centers Inc. (Delaware), eski BlockchAIn Digital Infrastructure; Signing Day Sports ile ters birleşme 16 Mar 2026; [R] 10-K, 8-K 29 Haz 2026 |
| CLT1 Charlotte, NC | YANLIŞ | 389 Tyger River Industrial Dr, Moore, Spartanburg County, SC; "Charlotte metro" pazarlama adı; [R] 10-Q; [İ] |
| Nebius 50 MW, 12 yıl, bağlayıcı | DOĞRULANAMADI | Yalnız [PR] 8-K Item 7.01 (1 Eki 2026) ve sunum; Item 1.01 8-K yok, MCSA exhibit yok; Nebius'tan ayrı bülten yok |
| Sözleşme değeri $1,32 Mlr | YANLIŞ | 30 Eyl sunumundaki "implied rate"; 20 Eki sunumunda silindi ve reddedildi; [PR] |
| Nebius ön ödeme $25–30M | DOĞRULANAMADI | Hiçbir belgede tutar yok; "escrow" ve "prepayments" kelimeleri var; [PR] |
| Nebius garantisi | DOĞRULANAMADI | "Guaranty from Nebius… Expected" (bekleniyor, imzalı değil); [PR] 30 Eyl sunum |
| Hol 1 Q3 2027, Hol 2 Q4 2027 | KISMEN | Eylül sunumu ay-10/ay-14 (≈Ağu/Ara 2027); Ekim sunumu iki hol de "Q4 2027, estimate, not guidance"; [PR] |
| Hisse 75,98M | DOĞRU | 75.979.466 (13 Ağu 2026); +140.667 (31 Ağu) ≈ 76,12M; [R] 10-Q, Form 4 |
| Warrant 1,53M; earnout 3,86M; EIP 7,53M | DOĞRU | [R] 8-K 10/18 Haz 2026; 10-Q Not 9 (earnout "remote") |
| Nakit $52,8M, borç yok | DOĞRU (30 Haz) | Sonra Texas'a ≈$11,2M ödendi; 30 Eyl tahmini $38–40M (hesap); [R] 10-Q, 8-K 11 Eyl |
| ESA 65 MW, 15 yıl | DOĞRU | 8-K Item 1.01 + Ex.10.1; asgari $400K/ay; ilk teslim hedefi 15 Ara 2026; [R] |
| CLT1 maliyeti ~$800M | DOĞRU (İLLÜSTRATİF) | %70 borç / %17,5 imtiyazlı / %12,5 öz kaynak; "not arranged"; [PR] |
| Going concern yok | DOĞRU | 10-Q ve 424B4'te ifade yok; [R] |
| Halka arz $1,65, Haz 2026 | DOĞRU | 38,3M hisse, brüt ≈$63,25M; 180 gün değişken fiyatlı ihraç yasağı (~5 Ara 2026'ya); [R] 8-K 10 Haz |

### VIVO

| İddia | Durum | Doğru değer, kaynak türü, tarih |
|---|---|---|
| Kod VVPR | YANLIŞ | VIVO (Nasdaq CM); VivoPower PLC (13 Mar 2026'dan beri); [R] 20-F kapak |
| Hisse ≈37M (30,72 + 4,36 + 2,13) | YANLIŞ | 31.993.555 adi + 800.000 imtiyazlı (→11.078.431) + 1.244.000 ITM warrant (21 Ağu 6-K); 28 Ağu'da ≈3,3M daha → ≈35,3M temel (tahmin), tam seyreltilmiş ≈48M; [R] 6-K 21/28 Ağu 2026 |
| 2,125M koşullu warrant | DOĞRULANAMADI | 20-F'de yok; ASEAN 345.892 + 575.517 reset warrant var; [R] |
| Capex $45–55M | YANLIŞ | ≈$411M (ilk 40 MW fazı, ön tahmin); [PR] FY2026 sonuçları 3 Kas 2026; 20-F rakam vermiyor |
| Kiracı LOI aşamasında | YANLIŞ | "No binding tenant agreement"; 29 Haz'daki tercihli kiracı bırakıldı; [R] 20-F |
| 41,5 MW hidro, $0,045/kWh | DOĞRU | [R] 20-F (PR'larda $0,035 ve $0,05 varyantları) |
| 30 MW Statnett dengeleme | DOĞRU | 12 MW FCR-D + 18 MW mFRR; [R] 20-F |
| Nakit $2,02M; borç $39,03M | DOĞRU (30 Haz) | AWN anapara Tem–Ağu'da kapatıldı ($16,5M → imtiyazlı, $12,3M nakit); ≈$16M faiz hâlâ ödenmemiş; kira $10,3M; [R] 20-F |
| İnşaat başladı (12 Eki) | DOĞRULANAMADI | PR 6-K olarak verilmedi; 20-F "mobilization" diyor, sonuç PR'ı "site works and maintenance"; M&E ihalesi yok; [PR]/[R] çelişkili |
| Going concern yok | DOĞRU, KOŞULLU | "No material uncertainty", ama $53,3M Ceres alacağı (teminatsız, gecikmiş) + $16M PIPE2 bakiyesi varsayımıyla; [R] 20-F |
| FY2026 zarar | — | Gelir $2,6M; toplam zarar $49,73M; ICFR zayıflığı; FY2025 yeniden düzenlendi; [R] 20-F |

---

## 3) QMLS (QumulusAI, Nasdaq)

**İş modeli gerçeği.** GPU-as-a-service: kolokasyon sahalarında (CoreSite, H5, NOCIX; Marietta, Kansas City, Denver, Philadelphia) kiralık GPU çalıştırıyor; sahaların hiçbiri kendi mülkü değil. Kripto madenciliği kökenli bir roll-up (WAHA + SPRE → Global Digital Holdings, 2022), GPU bulut işi Nisan 2025'te satın alındı; "AI şirketi" geçmişi 18 aydan kısa [R] 424B4. Q2'de 4 müşteri gelirin %90'ı (B %36, D %35, E %10, A %9) [R] 10-Q.

**Sözleşme bağlayıcılığı.** 10-Q'da beş sözleşme ayrıntılı ($99,6M, $19,8M, $18,0M, $32,0M, $71,9M; hepsinde %17–25 ön ödeme) ve RPO $173,1M [R]. Eylül'deki $240,9M ve $523,4M toplamı yalnız PR. Müşteri adı yok; en büyük müşteri ($283,8M = toplamın %54'ü) isimsiz bir "AI inference platform". Tek ödeme kanıtı $71,9M sözleşmedeki ~$14,4M ön ödeme.

**Finansman.** Sermaye maliyeti her katmanda yüksek: ATW %7 kupon + %4 OID + %7 VWAP iskontosu; USD.AI ≈%10; TFC "high single-digit"; ilişkili taraf notu %12 (1 Eki 2026'da vadesi doldu, akıbeti açıklanmadı) [R] 10-Q Not 16. Bilanço (30 Haz 2026): toplam varlık $215,0M, toplam yükümlülük $215,8M, **özkaynak −$0,78M**, birikmiş zarar $109,8M [R].

**Sermaye yapısı ve seyrelme (hesap; temel 33,46M, 20 Ağu 2026 [R]):**

| Senaryo | Hisse (M) | Varsayım |
|---|---|---|
| Düşük | ≈39,2 | + opsiyon 1,18 + warrant 0,87 + Eylül RSU 2,05 + ATW kalan ~$26,9M sabit fiyattan ($11,50/$24,25) |
| Orta | ≈46 | ATW kalanı %93 VWAP ile ~$3,29'dan (~8,2M hisse) + SAFE ~0,3M |
| Yüksek | ≈75–80 | Fiyat ~$2,50 (ATW ~11,6M), 4,77M plan havuzu, $60M green shoe çekilip ~$2,3'ten hisseyle itfa (~26M) |

ATW'nin VWAP mekanizması fiilen kullanılıyor: $3,1M anapara 590.584 hisseye döndü, yani $5,25/hisse, sabit $11,50'nin altında [R] 10-Q Not 26. Aylık itfa ≈$1,3–1,4M; $3,29'da ~400 bin hisse/ay (hesap). Ekim'de fiyat $6,53 → $3,14 düşerken hiçbir dosya yok; izin verilen sürekli satıcı ATW (ve 14 Eki'den sonra Rule 144 bağlı kişiler). Nedensellik kanıtlanmadı. İçeriden piyasa alımı sıfır, piyasa satışı sıfır (25 Form 4, 2 Eyl–2 Kas 2026) [R].

**Öncü sinyaller.** Kolokasyon kiracısı olduğu için izin/şebeke izi beklenmez ve bulunmadı. Atlanta 3,75 MW: Q4 2026'dan "2027 başı"na kaydı; sağlayıcı isimsiz, mevcut kiracının çıkışına bağlı [PR] 15 Eki. Olumlu tek iz: Focus Partners Wealth 13G'de 1,80M → 1,91M hisse (+104 bin) [R].

**Fiyatlanma (30/60/90 gün, 3 Kas):** −45,8% / −40,0% / −41,4%; listelemeden beri −83,5% [İ] Yahoo. 7'li neocloud sepeti (CRWV, NBIS, APLD, IREN, WULF, CIFR, CORZ): −31 / −36 / −39. Nasdaq −4/−8. Yani QMLS'e özgü ek kayıp 5–10 puan; kalan kısım sektör betası. Short interest 1,23M (15 Eki; float'ın %3,7–6,7'si, 2–3 gün) [İ] MarketBeat. Haber günlerinde kapanışta düşüş (20 Ağu −%9,3; 29 Eyl −%8,8; 22 Eki −%8,3) "haberde sat" ve dönüşüm arzı ile uyumlu.

**10x matematiği.** Bugünkü piyasa değeri $118,4M; EV ≈ $182M (Haziran, yüz değer) / ≈$280M (TFC + USD.AI sonrası, hesap).

| Seyrelme | Hisse (M) | 10x hisse fiyatı ($35,40) için gereken piyasa değeri | Piyasa değeri 10x olursa ($1,18 Mlr) hisse fiyatı |
|---|---|---|---|
| Düşük | 39,2 | $1,39 Mlr | $30,2 (8,5x) |
| Orta | 46 | $1,63 Mlr | $25,7 (7,3x) |
| Yüksek | 78 | $2,76 Mlr | $15,2 (4,3x) |

$1,2–1,6 Mlr piyasa değeri = EV/ARR 6–7x (NBIS/APLD/CORZ ileriye dönük çarpanı), EV/FY26 konsensüs 22x, kontratlı MW başına $110M (hesap). Yani 10x, (i) $209M ARR'nin 2027'de fiilen gelire dönmesi, (ii) sektör çarpanlarının bugünkü düzeyde kalması, (iii) seyrelmenin durması halinde "makul" olur. Üçü birden gerekli; üçüncüsü ATW yapısıyla çelişir. 1 yıl: pratikte imkânsız (ATW itfası sürer). 2–3 yıl: mümkün ama düşük olasılık.

**En büyük risk:** Değişken fiyatlı dönüştürülebilir + negatif özkaynak + going concern = fiyat düştükçe seyrelmeyi hızlandıran geri besleme döngüsü. Nasdaq asgari fiyat sorunu bugün yok ($3,54 > $1), ama Nasdaq Global Market özkaynak standardı özkaynak negatif kalırsa risk (şirket henüz uyarı almadı).

**Puan: 3/10.** Operasyon gerçek, sermaye yapısı tezi öldürüyor.

---

## 4) DGXX (Digi Power X, Nasdaq; Cboe Canada: DGX)

**İş modeli gerçeği.** Eski Digihost (bitcoin madencisi). Columbiana, AL'de (eski Grede dökümhanesi, 2022'den beri sahibi) Cerebras için Tier III 40 MW tesis inşa ediyor. New York 141,7 MW gaz peaker + madenci hosting (9.700 cihaz); AI'ya dönüşüm için **yerel moratoryum Temmuz 2027'ye kadar** [R: North Tonawanda Local Law No. 3 of 2026]. North Carolina 200 MW ham arazi (2028–30). AI'ya hazır kapasite bugün ≈1 MW (ARMS 200 podu, 15 May 2026'dan beri; ~0,6 MW GPU) [R] 10-Q, [PR].

**Sözleşme bağlayıcılığı.** Dört adayın en sağlamı. "Data Center Colocation and Master Services Agreement" 4 May 2026, Ex.10.1 olarak dosyalandı [R]. Take-or-pay (§6.1(c)), 10 yıl, $195/kW/ay, %3 artış. Çıkarım: 40 MW × $195 × 12 = $93,6M/yıl; Faz 1 (15 MW) ≈ $35M/yıl. Redakte olanlar: Exhibit A teslim tarihleri, günlük gecikme kredisi yüzdeleri, "Final Outside Delivery Date" gün sayısı (bu tarihten sonra Cerebras ücretsiz fesih + ön ödeme iadesi), ön ödeme tutarı, NRC $/kW. Faz 2 çifte şartlı: DGXX finansman bulacak VE Cerebras onaylayacak (§2.2(b)). 30 Haz bilançosunda Cerebras'tan önemli ön ödeme görünmüyor (deposits payable $1,69M) [R]. Cerebras'ın kendi 10-Q'su DGXX'i isimle anmıyor; "2026'da başlayan ~$1,5 Mlr iptal edilemez kira" ifadesi tutarlı ama özgül değil [R: CBRS 10-Q].

**Finansman.** Nakit $128,1M (30 Haz) [R]; ~$135M (13 Eki) [PR]. Borç yok. H1 2026 capex $96,3M; işletme nakit yakımı $10,6M/6 ay [R]. $200M proje kredisi: **taahhüt mektubu**, kredi veren isimsiz, SPV düzeyinde, şirket garantisi tamamlanana kadar, due diligence + belgeleme şartlı, kapanış "90 gün içinde" (≈11 Oca 2027, yani 15 Aralık hedefinden SONRA) [PR] 13 Eki. 8-K yok. Not: PR'lardaki capex ($95M → $110M → $153M) ile nakit ($155M → $150M → $135M) yürüyüşü uyuşmuyor; Q3 10-Q'da kontrol edilmeli (hesap).

**Sermaye yapısı ve seyrelme:**

| Senaryo | Hisse (M) | Varsayım |
|---|---|---|
| Düşük | 102,06 | Temel (opsiyonlar C$4,90, warrantlar $2,98 zararda); RSU 4,76M eklenirse 106,8 |
| Orta | 111,54 | Şirketin tam seyreltilmiş rakamı [R] DEF 14A |
| Yüksek | ≈123 | + 21 Ara 2026 AGM'de genişleyen RSU/opsiyon havuzu (10,14M'er, 2028'den %10/yıl evergreen) |
| Felaket | 150–190 | $200M kredi kapanmaz, Faz 2 $2–3'ten öz kaynakla finanse edilirse (+65M hisse) |

ATM kapasitesi fiilen tükenmiş görünüyor ($175M eki H1'de ≈$163M + Tem $11,3M); yeni raf gerekir, bu da görünür bir sinyal olur. Q3 2026'da ATM'den hisse ihraç edilmedi [PR]. Temel hisse 31 Ara 2024'ten beri +%207 [R: SEC XBRL].

**Öncü sinyaller (üçüncü taraf).** En yoğun kanıt bu sahada: $7,02M yapı ruhsatı (22 Haz 2026, Dunn Building Co.) [İ: Bham Now]; ADEM taslak hava izni, 42 dizel jeneratör, 29 Eki 2026 (15 gün yorum süresi → en erken Kasım ortası kesinleşir) [İ: E+E Leader]; belediye 12 aylık satış vergisi muafiyeti + $3,5M ödeme (21 Tem 2026) [İ: WBRC]. Olumsuz: belediyenin kendi teşvik evrakında "hizmet Nisan 2027" yazıyor (15 Ara 2026 değil) [İ: Shelby County Reporter, 29 May 2026]; şirketin 1 MW'lık ARMS podu Kas 2025 → Mar → May 2026'ya kaymıştı (5–6 ay); North Tonawanda'da FERC $45k ceza (3 Ağu 2026) + moratoryum. "Enerjilendi" teyidi yok. İş ilanı 0, çalışan ~17 [İ].

**Fiyatlanma.** $2,27; 30/60/90 gün: −40,9 / −39,5 / −39,5; duyuru öncesi (4 May $3,95) seviyesinin %43 altında; 52 hafta zirvesinden −73% [İ] Yahoo. Cerebras haberi 5 May'da +%29, 115,8M hacimle (normalin ~60 katı) fiyatlandı, sonra tamamen geri verildi. $200M PR'ı satışla karşılandı (−2%, ertesi gün −8%). Yani haber fiyatta değil; piyasa finansman ve teslim riskini fiyatlıyor. CEO 14 Eki'de $2,76'dan 20.000 hisse aldı ($55 bin; sembolik) [R].

**10x matematiği.** Piyasa değeri $231,7M; EV ≈ $95–100M.

| Seyrelme | Hisse (M) | 10x fiyat ($22,70) için piyasa değeri | Piyasa değeri 10x ($2,32 Mlr) olursa fiyat |
|---|---|---|---|
| Düşük | 102 | $2,32 Mlr | $22,7 (10x) |
| Orta | 111,5 | $2,53 Mlr | $20,8 (9,2x) |
| Yüksek | 123 | $2,79 Mlr | $18,8 (8,3x) |
| Felaket | 170 | $3,86 Mlr | $13,6 (6,0x) |

40 MW tam gelir $93,6M/yıl; triple-net NOI ~%90 → ~$84M FAVÖK; 18–20x ile EV $1,5–1,7 Mlr (hesap). Yani **Cerebras sözleşmesi tek başına 10x'e yetmez**; $2,3–2,8 Mlr için NY veya NC'de ikinci bir sözleşmeli saha gerekir, onlar 2028+. 1 yıl: hayır. 2 yıl: 40 MW faturalanıyor + ikinci kiracı imzalı ise 3–5x mümkün. 3 yıl: 10x yalnız ikinci saha enerjilenirse.

**En büyük risk:** 15 Ara 2026 teslim tarihinin kayması + $200M'ın kapanmaması aynı anda. Ex.10.1'deki "outside date" bilinmediği için Cerebras'ın ne zaman çekilebileceği hesaplanamıyor.

**Puan: 5,5/10.** Dörtlünün en iyisi; "al" için iki tetikleyici lazım (13 Kas Q3 + 15 Ara RFS veya kredi kapanışı).

---

## 5) AIB (AIB Data Centers, NYSE American)

**İş modeli gerçeği.** Spartanburg SC'de eski 40 MW bitcoin hosting sahası; 5 Haz 2026'da de-energize edildi, Q3'ten itibaren gelir "önemli ölçüde" düşecek [R] 10-Q. 2025 gelirinin %91–92'si tek ilişkili müşteri (Blue Ridge Digital Mining). Texas'ta iki parsel (11 Eyl 2026, ≈$17,2M; 15 MW mevcut + 40 MW FEA) [R] 8-K. Planlanan: CLT1'de iki 25 MW hol, 20 konteynerin yerine tek bina.

**Sözleşme bağlayıcılığı.** Şirket "binding", "executed MCSA" diyor, Nebius CPIO alıntı veriyor; ama 4 Kas itibarıyla Item 1.01 8-K ve exhibit yok, değer yok, ön ödeme tutarı yok, fesih şartı yok, Nebius garantisi "expected" [PR]. En somut olgu: 65 MW / 15 yıl ESA (8-K Ex.10.1, 1 Haz 2026) mevcut 34,5 kV hat üzerinden, "önemli altyapı yükseltmesi yok" [R]. ESA ilk teslim hedefi 15 Ara 2026; asgari $400K/ay (Trigger Date'e kadar yarısı ertelenir).

**Finansman.** Nakit $52,8M (30 Haz) [R]; Texas'a ≈$11,2M sonra; 30 Eyl tahmini $38–40M (hesap). Borç yok. CLT1 ≈$800M "illüstratif": $560M inşaat borcu + $140M imtiyazlı + $100M öz kaynak ("prepayments ile") [PR] 30 Eyl sunum. "Project financing has not been completed" [PR] 20 Eki. COO maaşı "CLT1 finansman kapanışında" artacak → 23 Eki'de kapanmamıştı [R] 8-K 28 Eki. 180 günlük değişken fiyatlı ihraç yasağı ≈5 Ara 2026'da bitiyor; sonrasında ATM/PIPE riski artar [R].

**Sermaye yapısı ve seyrelme:**

| Senaryo | Hisse (M) | Varsayım |
|---|---|---|
| Düşük | 76,1 | Temel (31 Ağu 2026) |
| Orta | 77,7 | + Lucid warrant 1,53M ($1,815; şu an zararda) |
| Yüksek | 81,6 | + earnout 3,86M + Maxim 0,14M (2026 FAVÖK ≥ $25M şartı; fiilen imkânsız) |
| Yüksek + EIP | 89,1 | + 7,53M plan yetkisi (ödül yok) |
| Felaket | 130–150 | $100M öz kaynak payı piyasadan ~$1'den toplanırsa (+60–75M) |

İçeriden: Jerry Tang (Tiger Cloud + VCV) 26,4M hisse ≈ %34,7 [R] Form 4. Tang'ın aynı sanayi parkındaki $3 Mlr "Project Spero" Şubat 2026'da teşvik reddinden sonra geri çekilmişti [İ].

**Öncü sinyaller.** İlçe meclisi geliştirme anlaşması 19 Eki'de ertelendi, 3 Kas'ta ikinci okumadan geçti, üçüncü okuma bekleniyor [İ: WSPA, başlık]. Anlaşma 50 MW IT / 65 MW tavan koyuyor (tavan, genişleme değil). İnşaat ruhsatı, yüklenici, ekipman, iş ilanı: yok. İlçe moratoryumu (>65 MW) AIB'yi kapsamıyor.

**Fiyatlanma.** $0,87; piyasa değeri ≈$66M; EV ≈$13M (StockAnalysis) / $27–30M (tahmini nakitle). Nebius duyuru günü (30 Eyl) **−%22**, 28M hacim (normalin ~15 katı) [İ] Yahoo. 30/60/90: −46 / −31 / −54. Halka arz fiyatının ($1,65) yarısı. Şirket kendi "MW başına EV" karşılaştırmasını iki haftada $2M'dan $1M'a indirdi [PR]. Sonuç: hikâye fiyatlanmamış, tersine piyasa duyuruyu satmış; ya ön ödeme/finansman şüphesi ya da büyük hissedar çıkışı (90 günlük lock-up 6 Eyl'de bitmişti).

**10x matematiği.** Piyasa değeri $66M → 10x = $660M.

| Seyrelme | Hisse (M) | 10x fiyat ($8,70) için piyasa değeri | Piyasa değeri 10x ($661M) olursa fiyat |
|---|---|---|---|
| Düşük | 76,1 | $662M | $8,69 (10x) |
| Orta | 81,6 | $710M | $8,10 (9,3x) |
| Yüksek | 89,1 | $775M | $7,42 (8,5x) |
| Felaket | 140 | $1,22 Mlr | $4,72 (5,4x) |

50 MW × ~$2,0M/MW/yıl NOI = ~$100M FAVÖK → 18–20x ile $1,8–2,0 Mlr EV; proje borcu $560M + imtiyazlı $140M düşülünce öz kaynağa ~$1,1–1,3 Mlr kalır (hesap). Kâğıt üstünde en "kolay" 10x. Ama: (i) sözleşme metni ve ön ödeme tutarı bilinmiyor; (ii) $800M finansman kapanmadı; (iii) ilk kira en erken Ağu–Ara 2027; (iv) Nebius'un kendi finansman baskısı ($20–25 Mlr/yıl capex) altında 50 MW onun için <%1. 1 yıl: hayır. 2 yıl: finansman kapanır + Hol 1 teslim olursa 3–5x. 3 yıl: iki hol faturalanırsa 10x mümkün ama bu, mikro-cap kohortunda henüz hiç görülmemiş bir sonuç.

**En büyük risk:** Finansman kapanmadan Aralık'ta ihraç yasağının bitmesi ve $0,87'den öz kaynak toplanması. İkinci risk: Nebius escrow şartlarının (SLA kilometre taşları) tutturulamaması.

**Puan: 4/10.** Ucuz opsiyon; bilet fiyatı düşük, ama vade 2027 sonu ve her şey başkasının parasına bağlı.

---

## 6) VIVO (VivoPower PLC, Nasdaq)

**İş modeli gerçeği.** Mo i Rana, Norveç'te 41,5 MW enerjilendirilmiş eski Bitfury tesisi (LIAN Group'tan 12 May 2026'da $37,7M'a alındı; arazi Mo Industripark'tan kiralık, 2076'ya kadar) [R] 20-F. Mevcut gelir: Corner Norway AS bitcoin hosting (≈Tem 2027'de bitiyor, uzatma yok) + 30 MW Statnett dengeleme. Eski XRP hazine stratejisi Şubat 2026'da terk edildi; Tembo e-LV işi SPAC'e gidiyor; Finlandiya 291 MW ve BAE 25 MW yalnız "erişim".

**Sözleşme bağlayıcılığı.** Yok. RFP 23 Nis → kısa liste 21 May → "tercihli kiracı, global AI lideri" 29 Haz → 20-F (2 Kas): "no longer pursuing… finalizing terms with another prospective tenant. No definitive lease has been signed" [R]. Going-concern notu yeni kiracının "prepaid rent + investment in VivoPower" getirmesini bekliyor ama tahmine koymuyor.

**Finansman.** Nakit $2,02M (30 Haz) [R]. Net cari yükümlülük $11,95M. AWN anapara Tem–Ağu'da kapatıldı ama ≈$16M birikmiş faiz hâlâ ödenmemiş, "hisseye dönüşüm görüşülüyor" [R]. Ertelenmiş satın alma bedeli $5,0M **12 Kas 2026**'da, $5,1–5,25M 12 May 2027'de. Ceres konsorsiyumu $60,5M taahhüdünün yalnız $8,12M'ını ödedi; $53,3M alacak teminatsız, gecikme "Orta Doğu savaşı" ile açıklanıyor [R]. Capex ≈$411M (≈$10M/MW), "%70–75 proje borcu", hiçbiri sağlanmamış [PR] 3 Kas. FY2026: gelir $2,6M, toplam zarar $49,7M, ICFR etkisiz, FY2025 restated [R].

**Sermaye yapısı ve seyrelme:**

| Senaryo | Hisse (M) | Varsayım |
|---|---|---|
| Düşük | ≈35,3 | Temel (tahmin; 21 Ağu 31,99M + 28 Ağu ≈3,3M) |
| Orta | ≈48 | + imtiyazlı 11,08M (6% PIK hariç) + ITM warrant 1,24M + DSU 0,35M |
| Yüksek | ≈66 | + Ceres kalan ~7,8M + AWN $16M faizi hisseye (~10M @ $1,60) |
| Felaket | 100+ | $411M'ın öz kaynak payı (%25–30 ≈ $100–125M) $1–2'den toplanırsa |

Hisse sayısı 12 ayda +%372 [İ] StockAnalysis. ASEAN reset warrantları piyasa değeri $250M'a ulaşırsa $0,01'e düşer (yani yükselişte ek seyrelme) [R].

**Öncü sinyaller.** Norveç tarafında üçüncü taraf kayıt yok (Rana kommune, Statnett/Linea, Rana Blad). Yerel yükleniciler (Øijord & Aanes, IMTAS, TH Blikk) yalnız şirket duyurusu. M&E EPC ihalesi 4 Kas'ta hâlâ yok; sonuç PR'ında "ihale beklenen zamanda ya da hiç verilmeyebilir" riski yazıyor [PR]. Mo i Rana şebeke düğümü çekişmeli (T1 Energy'nin 60 MW itirazı) [İ].

**Fiyatlanma.** $1,60 (3 Kas, sonuç günü **−%27**); 30/60/90: −52 / −59 / −58; 1 yıl zirvesi $6,60 (1 Haz 2026, kiracı beklentisi). Her duyuruda (29 Haz kiracı, 29 Tem PIPE, 12 Eki inşaat, 3 Kas sonuç) kapanışta düşüş [İ] Yahoo. Hikâye Haziran'da fiyatlandı ve o zamandan beri boşaldı.

**10x matematiği.** Piyasa değeri ≈$56M → 10x = $560M.

| Seyrelme | Hisse (M) | 10x fiyat ($16,00) için piyasa değeri | Piyasa değeri 10x ($565M) olursa fiyat |
|---|---|---|---|
| Düşük | 35,3 | $565M | $16,0 (10x) |
| Orta | 48 | $768M | $11,8 (7,4x) |
| Yüksek | 66 | $1,06 Mlr | $8,6 (5,4x) |

40 MW × $2M NOI = $80M → 18–20x = $1,4–1,6 Mlr EV; $300M proje borcu düşülünce öz kaynak ~$1,1 Mlr (hesap). Ama kiracı yok, finansman yok, nakit $2M, inşaat "mobilize" (PR) / "bakım" (20-F). 1–2 yıl: hayır. 3 yıl: yalnız bir kiracı + $411M finansman + seyrelmenin 2x'te kalması halinde; bu üçlü bugün bir ihtimal olarak bile belgelenmiş değil.

**En büyük risk:** Likidite. 12 Kas'ta $5,0M ödeme, $16M AWN faizi, $53,3M tahsil edilmemiş alacak, $2M nakit. Yönetim "going concern'de belirsizlik yok" diyor; bu görüş Ceres'in ödemesine dayanıyor.

**Puan: 1,5/10.** Elenir.

---

## 7) Evren dışı adaylar

Tarama: ABD borsalarında piyasa değeri ~$30–300M AI veri merkezi altyapısı / GPU bulut / güç sağlayıcı (StockAnalysis, 3 Kas 2026 kapanışı [İ]; sözleşmeler [R]/[PR] işaretli). Son 90 günde >%100 koşan isim YOK; grup tümden Ekim'de çöktü.

| Kod | Piyasa değeri | EV | Nakit / borç | Sözleşme | 12 ay hisse artışı | 30/60/90 g | Daha iyi mi? |
|---|---|---|---|---|---|---|---|
| DUOT | $194M | $82,5M | $112M / $1M | 20 MW 10 yıl >$400M [R] 8-K Ex.99.2 (Q2 2027); 10 MW 5 yıl $111M IG hyperscaler (Q4 2026) [PR] | +%160 | −33/−30/−40 | **Evet (bilanço)**; edge ölçeği küçük; Cantor $24 |
| HOST | $73M (temel) / ≈$125M (48,1M tam seyreltilmiş) | bulunamadı | bulunamadı | 43 MW 15 yıl take-or-pay ≈$1,25 Mlr, IG backstop "bekleniyor" [R] 8-K Ex.99.1; teslim H1 2027 | — (ters birleşme 17 Eyl 2026) | −16/—/−68 | **Kısmen**: en büyük tek sözleşme, en zayıf finansman ($17,5M halka arz); 45,4M hisselik yeniden satış kaydı [R] S-3; going-concern çelişkili |
| SLNG | $80M | $84M | $4,6M / $8,2M | ~$200M 2 yıllık BTM LNG güç sözleşmesi (2027–29), $25M ön ödeme [PR] | −0% | — | Sağlayıcı; seyrelme yok; müşteri isimsiz |
| SLNH | $139M | $65M | $113M / $9M (Generate kapatıldı) | HPC kiracısı yok; APLD JV (%49) + CHRN non-binding LOI | **×86 / +%846** | −45/−53/−54 | Hayır: seyrelme makinesi |
| NUAI | $296M (PIPE sonrası ≈$360M) | $242M | $70M / $15M | 207 MW Vistra PPA [İ]; kiracı yok; $64M PIPE 29 Eki [R] | +%239 | −54/−49/−45 | Hayır: bant üstü, kiracısız |
| VIP (ex-GREE) | $42M | $78M | $3,2M / $39,6M | Kiracı yok; Q1 2026 going concern | +%26 | −22/−38/−35 | Hayır |
| GPUS | $29M | $133M | $37M / $141M | 20 MW isimsiz neocloud [İ]; 30 MW enerjili | +%7.263 | +6/−11/−58 | Hayır: borç > 4× piyasa değeri |
| TSSI | $198M | $169M | $68M / $39M | Rack entegrasyonu (hizmet) | +%9 | −30/−17/−17 | Varlık sahibi değil; farklı iş |
| IPWR | $41M | ≈$0 | $41M / $0,4M | Prototip (800V DC), gelir $30K | +%29 | −37/−49/−47 | Teknoloji opsiyonu; sözleşme yok |
| TGEN | $57M | $53M | $6,8M / $2,6M | Backlog $7M; DC siparişi yok | +%19 | −26/−40/−41 | Hayır |
| PPSI | $27M | $18M | $10,7M / $1,3M | $200M "teklif boru hattı" (sipariş değil) | veri hatalı | −24/−15/−14 | Hayır |
| ZSQR | $198M | bulunamadı | bulunamadı | 8 MW kesintili Entergy; 150 MW hedef; ilçe moratoryumu | — | — | Hayır |
| AGPU | $88M | $67M | $22M / $2M | $260M 36 ay take-or-pay, $43M ön ödeme alındı [İ]; $1,5 Mlr isimsiz | +%412 | — | Hayır: seyrelme, go-live teyitsiz |
| BGDE (ex-MIGI) | $18M | $34M | $16M / $32M | İlişkili taraf kolokasyon | +%246 | — | Hayır: bant altı, delist uyarısı |
| DRK (ex-ANY) | $20M | — | $2,8M | AI sözleşmesi yok | +%50 | — | Hayır |
| PWCM, SGRX, SOBR, POLA, BEEM, NVVE | <$20M | — | — | — | — | — | Ölü |

Bant dışı büyükler (karşılaştırma için): KEEL $1,35 Mlr, BTDR $1,9 Mlr, CIFR $3,4 Mlr, CORZ $4,6 Mlr, APLD $5,4 Mlr, WULF $6,3 Mlr, HUT $7,9 Mlr, IREN $9,6 Mlr, NBIS $41,6 Mlr [İ].

**"Enerjilendirilmiş + sözleşmeli + finansmanı kapanmış" üçlüsünü bugün hiçbir isim tam sağlamıyor.** En yakını DGXX. Sıralama (üçlüye yakınlık): DGXX > DUOT > HOST > AIB > SLNG > QMLS. DUOT evren içindeki tek "nakit zengin + IG kiracılı" isim; ama 30 MW toplam ölçek 10x'e taşımaz ($194M → $1,9 Mlr için ≥100 MW kontratlı gerekir).

---

## 8) Sektör gerçekleri ve 10x'in genel olasılığı

**Birim ekonomi (2025–26 sözleşmeleri, hesap):**

| Model | Gelir/MW/yıl | Capex/MW | Kaynak |
|---|---|---|---|
| Kolokasyon (powered shell) | $1,8–2,3M (APLD–CoreWeave $1,83M; HUT–Fluidstack $1,90M; CIFR $1,79M; DGXX–Cerebras $2,34M taban) | $15–25M (AI'ya hazır kabuk; JLL/Goldman) | [R] APLD, CIFR 8-K; HUT PR; DGXX 10-Q; [İ] CoR Advisors |
| GPU-as-a-service | $9,7–12M (IREN–Microsoft $9,7M) | $40–60M (GPU dâhil; GB300 ~$40M/MW) | [İ] TechInformed, SemiAnalysis aktarımı |
| 2026 kira medyan NOI | $1,66M/MW | — | [İ] datacentres.com 11 Ağu 2026 |

Kolokasyon geliri GPU bulutunun %15–20'si, ama capex'i yarısı ve sözleşmeleri 10–15 yıllık take-or-pay. GPU kirası 12 ayda ±%40 oynadı (H100 1 yıl kontrat $1,70 → $2,35) [İ]. DGXX'in $195/kW'ı örneklemin üstünde; bu güçlü pazarlık değil, Tier III + küçük ölçek + tüm inşaat maliyetini DGXX'in taşıması demek.

**Teslim gecikmesi taban oranları.** Trafo merkezi transformatörü >160 hafta (Wood Mackenzie, 2026); PJM'de 2025'te devreye girenler ortalama 7 yıl [İ: DCK 12 May 2026]. Çitte güç olan eski madencilik sahalarında kira → ilk hol 5–17 ay. Örnek: CORZ "yaz sonu 450 MW" → Temmuz ortası 437 MW; Denton kayması CoreWeave'in 2025 rehberliğini kestirdi (−%13, dava) [İ]. CIFR ~1 ay kayma. DGXX'in kendi 1 MW podu 5–6 ay kaydı. Mikro-cap için 3–6 aylık kayma aynı zamanda nakit yakımı ve ATM olayıdır; kira yalnız RFS'te başlar.

**Seyrelme taban oranları (SEC XBRL kapak sayıları [R]):** APLD +%148 (Oca 2024 → Eki 2026), CORZ +%81, WULF +%65, CIFR +%54, HUT +%38, BTDR +%110 (2 yıl); DGXX +%207, AIB +%102 (5 ay), SLNH ×86, MIGI ters bölünme + delist. 2025–26'da AI sözleşmesi duyuran HER mikro-cap haftalar içinde ATM veya iskontolu ihraç yaptı (DGXX $175M raf Cerebras'tan 4 gün sonra; AIB $55M iskontolu, listelemeden 11 hafta sonra).

**Halka arz / küçük şirket taban oranları (Ritter, 9.195 IPO 1975–2021, 5 yıl [İ]):** >%50 kaybeden %42,6; sıfırın altı %60,6; ≥%500 kazanan %3,0; **≥%1.000 kazanan %1,0**. Satışı $10–20M olan IPO'larda 3 yıl piyasa-ayarlı −%36; dosya fiyatı <$8 olanlarda −%86; 2018–21 doğrudan listelemelerde −%36. Yani 10x : >%50 kayıp oranı kabaca 1 : 15–40.

**Kohort sonucu (n=12, 2024–26 AI sözleşmesi duyuranlar, hisse başına, hesap ±%10–20):** ≥10x: **0**. 3–10x: 2 (CORZ ~4,2x Oca 2024'ten; BTDR ~6x). 1,5–3x: 3 (APLD, WULF, CIFR). Yatay/−40: 2 (IREN, DGXX). >%50 düşüş: 5 (SLNH, MIGI, ANY, AIB, DGXX ATM fiyatına göre). Kazananların dört ortak özelliği: yüzlerce MW enerjili güç, IG veya Google-backstoplu kiracı, $1 Mlr+ dönüştürülebilir erişimi, zaten ≥$500M piyasa değeri. Dördümüzün hiçbirinde bu dört özellik yok.

**Genel olasılık (öznel; bkz. §12):** Bu banttaki bir şirketin 3 yılda hisse başına 10x yapma olasılığı %1–3; >%50 ek kayıp olasılığı %40–50.

---

## 9) Sıralama

**En güçlü 3 aday (izleme; bugün alım değil):**
1. **DGXX** — tek exhibit'li take-or-pay sözleşme, kendi trafo merkezi, borç yok, $128M nakit; CEO alımı. Eksik: RFS kanıtı, $200M kapanışı, Faz 2 onayı.
2. **DUOT** (evren dışı) — $112M nakit, borç yok, IG hyperscaler + halka açık bulut sağlayıcı sözleşmeleri; eksik: ölçek (30 MW), +%160 seyrelme.
3. **AIB** — EV ≈ $13–30M ile piyasa Nebius'u sıfırlamış; ESA ile güç çitte; eksik: sözleşme metni, ön ödeme tutarı, $800M finansman, Aralık'ta biten ihraç yasağı. HOST bu sırada 4.; tek sözleşmesi en büyük, finansmanı en zayıf, 45,4M hisse yeniden satış kaydı.

**Mevcut dördün sırası:** DGXX (5,5) > AIB (4) > QMLS (3) > VIVO (1,5).

**Tamamen elenecekler:** VIVO (kiracı yok, nakit $2M, $411M capex), GPUS, BGDE, DRK, PWCM, SGRX, SOBR, POLA, BEEM, NVVE; NUAI (kiracı yok, +%239 + PIPE, bant üstü); SLNH (×86 hisse; tek HPC projesinin %51'i APLD'de).

**Şu an alınmayacaklar:** Hepsi. DGXX için 13 Kasım Q3 (nakit, capex-kalan, Cerebras ön ödemesi/contract liability) ve 15 Aralık RFS veya kredi kapanışı beklenir. AIB için Q3 10-Q (≤16 Kas) contract liabilities satırı ve ilçe 3. okuma. QMLS için Q3 10-Q (16–23 Kas) ATW kalan anapara + nakit, sonra lock-up (12–19 Oca 2027).

---

## 10) Mevcut zarardaki QMLS pozisyonu

**Veri:** ~%30 zarar → maliyet ≈ $5,06 (3,54/0,70). Bu seviye 20–21 Ağu ($5,36–5,86), 1–4 Eyl ($5,43–5,90), 15–16 Eyl ($5,38–5,51) veya 9 Eki ($5,25) alımına denk; yani Chardan hedefi ($24,50) ve $240,9M sözleşme haberleri dönemi [İ] Yahoo. Pozisyon 30–40 bin TL; QMLS günlük ortalama ~300 bin hisse ≈ $1M işlem değeri → bu boyutta pozisyon için likidite sorun değil (tek emirle çıkılır).

**10 sorunun cevabı:**

| # | Soru | Cevap |
|---|---|---|
| 1 | %30 zarardaki hisseyi tutmak için bugün hâlâ geçerli bir yatırım tezi var mı? | Zayıf. Operasyon gerçek (10-Q'da $173M RPO, beş ön ödemeli sözleşme, Q2 gelir +%118) ama hisse başına tez ATW mekanizmasıyla kırık: tahvil her ay 8 günlük en düşük VWAP'ın %93'ünden hisseye dönüyor (~400 bin hisse/ay, Tem 2028'e kadar), özkaynak −$0,78M, 10-Q'da going-concern şüphesi. "Tut" tezi yalnız Q3 10-Q'nun (16–23 Kas) dört şartı (§10 net öneri) sağlamasıyla doğar; bugün kendi başına ayakta değil. |
| 2 | İlk alış gerekçeleri bozuldu mu? | Kısmen. Alış ($5,06 civarı) Chardan'ın $24,50 hedefi ve $240,9M sözleşme haberleri dönemine denk. Bozulanlar: Chardan hem danışman hem %3,47 hissedar (hedef $23'e indi, yeni kapsamlar $9–11); "IPO" değil doğrudan listeleme, $0 hasılat; USD.AI "non-binding MOU"; Atlanta Q4 2026 → "2027 başı"na kaydı. Bozulmayanlar: Q2 rakamları birebir doğru; sözleşmeler ön ödemeli; içeriden satış yok. Yani gerekçelerin "büyüme" ayağı duruyor, "sermaye yapısı güvenli" ayağı hiç yoktu. |
| 3 | Şirketin temel göstergeleri kötüleşti mi, yoksa piyasa geçici olarak mı cezalandırıyor? | İkisi birden, ağırlık piyasada. 30/60/90 günde QMLS −42/−40/−41 vs akran sepeti −31/−36/−39: kaybın büyük bölümü sektör betası, QMLS'e özgü ek kayıp 5–10 puan. Resmi temel göstergede (10-Q, 30 Haz) yeni kötüleşme yok; ama Ekim'de $6,53 → $3,14 düşerken hiçbir dosya yok ve izin verilen sürekli satıcı ATW. Kötüleşen tek şey seyrelme hızı: fiyat düştükçe aynı anapara daha çok hisse üretiyor. |
| 4 | Hissenin toparlanması için hangi somut katalizörler gerekiyor? | (a) Q3 10-Q'da çeyrek geliri ≥ $15–20M (konsensüs 2H26 ≈ $47M), nakit ≥ $30M, ATW kalan anapara < $15M, going-concern paragrafı yumuşamış; (b) 8-K ile müşteri adı/exhibit ya da büyük müşterinin kimliği; (c) ATW itfasının nakitle yapıldığına dair açıklama; (d) Atlanta 3,75 MW'ın 2027 başında enerjilenmesi; (e) 12–19 Oca 2027 lock-up'ın Form 4 satışı olmadan geçmesi; (f) sektör çarpanlarının toparlanması (akranlar 90 günde −%31…−%57). |
| 5 | Bu katalizörlerin gerçekleşme olasılığı nedir? | Öznel: (a) dördü birden %25–30; (b) %15 (şirket Item 1.01 8-K vermiyor); (c) %10–15 (nakit kısıtlı); (d) %50 (bir kez kaydı); (e) %40 (Bissell artık yönetici değil, 5,86M hisse); (f) %40–50, yüksek varyans. 12 ayda maliyete ($5,06) dönüş %25–30. 3 yılda hisse başına 10x %1–2. |
| 6 | Şirketin finansal yapısı bu süreyi atlatmaya yeterli mi? | Sınırda. Ağustos başı pro forma likidite ≈ $55M (nakit $20M + serbest kalan $19,9M + USD.AI $15,3M) vs. kira ödemeleri ~$9,3M (2026 kalanı) + ~$20M (2027), $2,0M ilişkili taraf notu (1 Eki'de vadesi doldu, akıbeti açıklanmadı), ATW asgari likidite taahhütleri. Çeyrek ön ödemeleri (~$20,9M Temmuz) nefes veriyor ama performans yükümlülüğü. 12 ayda ödeme aczi olasılığı öznel %15–25; ATW senior secured, bütün varlıklarda rehin. Q3 nakit rakamı görülmeden "yeterli" denemez. |
| 7 | Hisse fiyatının daha fazla düşmesi halinde sermaye kaybı ne kadar olabilir? | Stres senaryosunda (%30 olasılık) $0,5–1,5 → bugünkü $3,54'ten −%60 ila −%85, maliyete göre −%70 ila −%90. Sürünme senaryosunda (%45) $2–4 → −%45 ila +%13. Taban oran: küçük/zararlı/düşük fiyatlı listelemelerde >%50 ek kayıp %42,6 (Ritter). Fiyat $1'e inerse Nasdaq asgari teklif riski eklenir. Pozisyon 30–40 bin TL; likidite çıkışı engellemez (~300 bin hisse/gün). |
| 8 | Pozisyonu bugün satmak mı, belirli bir süre beklemek mi daha rasyonel? | 12 aylık beklenen değer ≈ $3,53 (0,25×7,5 + 0,45×3 + 0,30×1) ≈ bugünkü fiyat; beklenen getiri ≈ 0, dağılım sola çarpık; taban oran hesabı −%11. Rasyonel sıra: satış varsayılan; beklemenin tek gerekçesi 16–23 Kas'taki 10-Q'ya kadar 2–3 hafta "bilgi beklemek". 10-Q dört şartı sağlamazsa veya NT 10-Q gelirse lock-up'tan (12 Oca 2027) önce sat. Ortalama düşürme yok. |
| 9 | Satıştan sonra başka hisseye geçmek, mevcut zararı telafi etme psikolojisiyle alınmış aceleci bir karar olur mu? | Bugün evet olur. Dört adayın hiçbiri "al" seviyesinde değil; DGXX bile iki tetikleyici (13 Kas Q3, 15 Ara RFS / ~11 Oca kredi) bekliyor. Telafi psikolojisinin işareti: "aynı sektörde daha ucuz bir 10x" aramak. Sektör kohortunda mikro-cap'ten hisse başına 10x örneği yok; gerçekçi üst senaryo 2–4x. Nakitte beklemek (B) geçerli ve maliyetsiz bir seçenek; C ancak koşullarla. |
| 10 | Yeni hisseye geçilecekse hangi koşullar oluşmadan yatırım yapılmamalı? | DGXX için: 13 Kas Q3'te nakit ≥ kalan Faz 1 capex'i, Cerebras'tan ön ödeme/contract liability görünür, $200M kredi için 8-K Item 1.01 (kesin sözleşme) veya 15 Ara RFS teyidi, kapak hisse sayısı ≤ 103M, NT moratoryum/ADEM izni sürprizi yok. Genel kural (her aday için): imzalı + exhibit'li sözleşme, çitte güç, finansmanı kapanmış, 12 aylık seyrelme < %50, haber günlerinde satış yerine alım. Bu üçlü bugün hiçbir isimde tam sağlanmıyor. |

**A / B / C karşılaştırması (12 ay, öznel):**

| Ölçüt | A: Tut | B: Sat, nakitte bekle | C: Sat, DGXX'e geç |
|---|---|---|---|
| Beklenen getiri | ≈ 0% ($3,53 vs $3,54); taban oranla −%11 | 0% (nakit) | ≈ +%40 (DGXX senaryo: RFS+kredi %35 → $5; 1 çeyrek kayma %35 → $3; kredi başarısız %30 → $1,25; EV $3,18 vs $2,27) |
| Olası kayıp (kötü %30) | −%70 ila −%85 ($0,5–1,5) | 0 | −%45 ila −%55 ($1–1,25) |
| Olası kazanç (iyi %25–35) | +%70 ila +%150 ($6–9) | 0 | +%75 ila +%165 ($4–6) |
| Likidite | İyi (çıkış kolay) | — | DGXX hacmi QMLS'ten yüksek (milyonlarca hisse/gün) |
| Zaman maliyeti | Para Ocak 2027 lock-up'ına kadar bağlı; arz baskısı Tem 2028'e kadar | Sıfır; Kasım bilanço sezonunu dışarıdan izler | 13 Kas ve 15 Ara iki tetikleyici 6 hafta içinde |
| Vergi/psikoloji | Zararı "gerçekleştirmeme" yanlılığı; maliyet $5,06 piyasa için anlamsız | Zararı kabul | Zararı kabul + yeni risk |
| Ne zaman yanlış olur? | Q3 kötü, lock-up satışı | Sektör V dönüşü yapar (akranlar 90 günde −%31…−%57 düştü, geri dönüş varyansı yüksek) | 15 Ara kayar + kredi kapanmaz (ikisi birlikte %30) |

**Net öneri (koşullu; karar Cemal'in):**
- Varsayılan: **B** (sat, nakit). Gerekçe: beklenen getiri sıfır, sol kuyruk kalın, Ocak'a kadar arz baskısı bilinen ve takvimli.
- **A** yalnız şu şartla: 16–23 Kas'ta gelen Q3 10-Q'da (i) nakit ≥ $30M, (ii) ATW kalan anapara < $15M, (iii) çeyrek geliri ≥ $15M, (iv) going-concern ifadesi yumuşamış. Dördü de tutmazsa **lock-up'tan önce (12 Oca 2027'den önce) sat**. NT 10-Q gelirse beklemeden sat.
- **C** (DGXX'e geç) yalnız 13 Kas Q3 sonrası: capex-kalan ≤ nakit, Cerebras'tan ön ödeme/contract liability görünür, kredi kapanış takvimi teyitli ise. 15 Ara'ya kadar beklemek de seçenek: RFS teyidi gelirse daha pahalı ama daha düşük riskli giriş. DGXX de 10x adayı değil; 2–3 yılda 3–5x adayı.
- Hiçbir seçenekte "ortalama düşürme" (QMLS'e ekleme) önerilmiyor: seyrelme mekanizması fiyat düştükçe hisse başına değeri ayrıca eritir.

**İzlenecek tarihler (QMLS):** 16 Kas (10-Q son tarih) / 23 Kas (NT ile) / 25 Kas (tahmin); 1 Ara RSU; 1 Oca plan +%5; 12–16 Oca 2027 lock-up (ilk işlem günü 19 Oca); "2027 başı" Atlanta 3,75 MW enerjilendirme; Mart 2027 10-K; 16 Tem 2028 ATW vadesi.

---

## 11) Karar tablosu

Satır başlıkları görev metnindeki 20 kriteri yansıtacak biçimde kuruldu (orijinal liste elde yok).

| # | Kriter | Sonuç |
|---|---|---|
| 1 | Önceki rakamlar denetlendi mi? | Evet; 4 şirket × 14–20 satır (§2). QMLS mali rakamları doğru; DGXX hisse/nakit, AIB kimlik/saha/değer, VIVO kod/hisse/capex/kiracı yanlış. |
| 2 | Bağlayıcı sözleşme (exhibit'li) | Yalnız DGXX (Ex.10.1). QMLS: 10-Q'da özet, exhibit yok. AIB: PR. VIVO: yok. |
| 3 | Finansman kapanmış mı? | Hiçbirinde. DGXX taahhüt mektubu (~11 Oca 2027); QMLS TFC PR-only; AIB yok; VIVO yok. |
| 4 | Enerjilendirilmiş AI kapasitesi | QMLS 7 MW faturalanan + 1 MW (PR); DGXX ≈1 MW; AIB 0 (CLT1), 15 MW Texas (ilgisiz); VIVO 0 (41,5 MW madencilik). |
| 5 | Going concern | QMLS: var (10-Q). DGXX: bağımlılık cümlesi, denetçi şerhi yok. AIB: yok. VIVO: "belirsizlik yok" (Ceres alacağı varsayımıyla). |
| 6 | Seyrelme 12 ay | QMLS +%49; DGXX +%92; AIB +%102; VIVO +%372. Hepsi >%50 eşiğinde veya üstünde (QMLS sınırda). |
| 7 | Önümüzdeki 6 ay arz baskısı | QMLS en yüksek (ATW + RSU + lock-up); AIB (ihraç yasağı 5 Ara'da biter); VIVO (imtiyazlı, AWN faizi, Ceres); DGXX en düşük (ATM dolu, plan genişlemesi). |
| 8 | Fiyatlanma 30/60/90 | QMLS −46/−40/−41; DGXX −41/−40/−40; AIB −46/−31/−54; VIVO −52/−59/−58. Sektör sepeti −31/−36/−39. Hiçbiri "koşmuş" değil. |
| 9 | İçeriden alım | DGXX: CEO 20.000 @ $2,76 (sembolik). QMLS/AIB/VIVO: yok. |
| 10 | Üçüncü taraf öncü sinyal | DGXX Columbiana: ruhsat, hava izni, teşvik (güçlü ama "enerjilendi" yok). AIB: ilçe 2. okuma. QMLS/VIVO: yok. |
| 11 | Olumsuz üçüncü taraf sinyal | DGXX NY moratoryum + FERC; AIB ilçe muhalefeti; VIVO kiracı kaybı; QMLS Atlanta kayması. |
| 12 | EV / kontratlı yıllık gelir | DGXX ≈1,1x (40 MW), ≈3x (15 MW); QMLS ≈1,1x (ARR PR); AIB hesaplanamıyor (değer gizli); VIVO yok. |
| 13 | 10x hisse fiyatı (orta seyrelme) | QMLS $35,4 → piyasa değeri $1,63 Mlr gerekir; DGXX $22,7 → $2,53 Mlr; AIB $8,7 → $710M; VIVO $16 → $768M. |
| 14 | 10x için ne gerekir? | QMLS: ARR'nin tamamı gelire + seyrelme durması. DGXX: Cerebras 40 MW + ikinci saha. AIB: $800M finansman + iki hol. VIVO: kiracı + $411M + 2x altı seyrelme. |
| 15 | 10x olasılığı (3 yıl, öznel) | QMLS %1–2; DGXX %3–5; AIB %3–4; VIVO <%1. |
| 16 | >%50 ek kayıp olasılığı (12 ay, öznel) | QMLS %30–35; DGXX %25–30; AIB %35–40; VIVO %50+. |
| 17 | En büyük risk | QMLS seyrelme döngüsü; DGXX teslim+kredi; AIB finansman; VIVO likidite. |
| 18 | Mevcut QMLS pozisyonu | Varsayılan sat (B); Q3 dört şartı sağlarsa tut, sağlamazsa lock-up öncesi sat. |
| 19 | Şu an yeni alım | Yok. DGXX 13 Kas / 15 Ara tetikleyicileriyle yeniden değerlendirilir. |
| 20 | Genel sonuç | "Hiçbir aday yeterince güçlü değil." Sektör kohortunda mikro-cap'ten hisse başına 10x örneği yok. |

---

## 12) Olasılık uyarısı

Bu rapordaki bütün olasılıklar (%1–2, %25, %30, %35 vb.) **özneldir**; hiçbiri ölçülmüş bir dağılımdan gelmiyor. Varsayımlar:
- Taban oranlar Ritter'in 1975–2021 IPO örneklemi ve 2024–26 n=12 kohortundan; QMLS'in "listelemeden 4 ay sonra %30 düşmüş küçük şirket" koşulu için yayımlanmış koşullu oran **bulunamadı**.
- Senaryo fiyatları ($6–9, $2–4, $0,5–1,5; DGXX $5 / $3 / $1,25) akran çarpanlarının bugünkü düzeyde kalacağı varsayımıyla kuruldu; sektör çarpanı Ekim'de %30–50 daraldı ve her iki yöne de oynayabilir.
- Şirket PR rakamları ($523M, $209M ARR, $135M nakit, $200M kredi, $411M capex) resmi belgeyle teyit edilene kadar "şirket beyanı" sayıldı; bu rakamlar doğru çıkarsa olasılıklar DGXX lehine, yanlış çıkarsa hepsinin aleyhine kayar.
- Döviz, vergi ve komisyon hesaba katılmadı; TL pozisyonun dolar karşılığı hesaplanmadı.
- "Beklenen değer ≈ 0" sonucu senaryo ağırlıklarına duyarlıdır: toparlanma olasılığı %25 → %40 olursa EV +%25'e çıkar; stres %30 → %45 olursa −%20'ye iner. Rapor bu aralığı "yaklaşık sıfır, sola çarpık" diye özetliyor.
- Notlar arasında çelişen rakamlarda EDGAR belgesi esas alındı (örn. DGXX nakit $128,1M vs PR $142,4M; AIB EV $13M [StockAnalysis] vs $27–30M [tahmini nakit]; QMLS lock-up 12 Oca [180 gün] vs 16 Oca ["six months"]).

---

## 13) İzleme takvimi, Kasım 2026 – Nisan 2027

| Tarih | Olay | Şirket | Ne bakılır |
|---|---|---|---|
| 10 Kas 2026 | FY2026 sonuç çağrısı 08:00 ET | VIVO | Yeni kiracı kimliği/LOI, Kasım nakdi, M&E ihalesi |
| ~10–11 Kas | FINRA 31 Eki short interest | QMLS | 1,23M'dan artış? |
| 12 Kas | $5,0M ertelenmiş satın alma bedeli vadesi | VIVO | Ödendi mi? |
| 12 Kas | Q3 sonuçları | NUAI | (evren dışı, bağlam) |
| 13 Kas | Q3 sonuçları, çağrı 08:30 ET | **DGXX** | Nakit, capex kalan, Cerebras ön ödeme/contract liability, RFS teyidi, kredi takvimi, hisse sayısı |
| ~13 Kas | ADEM jeneratör izni yorum süresi biter | DGXX | Kesinleşme / itiraz |
| ~13 Kas | Q3 sonuçları (tahmin) | AIB | Contract liabilities (Nebius ön ödeme?), nakit, EIP ödülleri |
| 16 Kas | Q3 10-Q yasal son tarih (45 gün) | **QMLS**, AIB | QMLS: kapak hisse, ATW kalan, nakit, going concern, $2M not |
| 16 Kas | 13F son tarihi (30 Eyl) | Hepsi | Kurumsal alıcı var mı? |
| 16 Kas | Q3 | DUOT, SLNH | DUOT: nakit, 20 MW teslim takvimi |
| 17 Kas | Q3 | HOST | Nakit/capex ilk kez |
| Kasım (tarih belirsiz) | İlçe meclisi 3. okuma, geliştirme anlaşması | AIB | Onay; exhibit'ler |
| 23 Kas | NT 10-Q ile uzatılmış son tarih | QMLS | NT gelirse kırmızı bayrak |
| 25 Kas | Veri sağlayıcı sonuç tahmini (teyitsiz) | QMLS | |
| 1 Ara | İlk RSU hak edişi (CEO vd.) | QMLS | Form 4'te satış |
| ~5 Ara | 180 gün değişken fiyatlı ihraç yasağı biter | AIB | ATM/PIPE dosyası (S-3) |
| 15 Ara | Faz 1 15 MW RFS hedefi | **DGXX** | 8-K veya PR ile teyit; gecikme açıklaması |
| 15 Ara | ESA ilk teslim hedefi | AIB | Utility teslimi |
| 21 Ara | Yıllık genel kurul (sanal) | DGXX | SV+PV birleşmesi, RSU/opsiyon havuzu 10,14M'er |
| 1 Oca 2027 | Plan havuzu +%5 evergreen | QMLS | |
| ~11 Oca | $200M taahhüt mektubu 90 gün penceresi | **DGXX** | 8-K Item 1.01/2.03 (kesin kredi) |
| 12–16 Oca | Lock-up bitişi (12,68M + 0,61M hisse); ilk işlem günü 19 Oca | **QMLS** | Form 4 / Form 144 satışları; Bissell, Aderhold, Alder |
| "2027 başı" | Atlanta 3,75 MW enerjilendirme ($211,9M sözleşme) | QMLS | PR; yeni kayma? |
| Mart 2027 (Q1 sonu) | Faz 2 25 MW hedefi (finansman + Cerebras onayı şartlı) | DGXX | |
| 31 Mar 2027 | 10-K son tarihi | QMLS, DGXX, AIB | Denetçi görüşü, going-concern |
| Nisan 2027 | Belediye evrakındaki alternatif "hizmet başlangıcı" | DGXX | Aralık kayarsa gerçekleşme tarihi |
| 12 May 2027 (pencere dışı, not) | $5,1–5,25M ikinci ertelenmiş ödeme | VIVO | |
| Tem 2027 (pencere dışı, not) | NT moratoryum bitişi; Corner hosting sözleşmesi bitişi | DGXX; VIVO | |
| Ağu–Ara 2027 (pencere dışı, not) | Hol 1 / Hol 2 teslim hedefi | AIB | |

---

## 14) Kaynaklar

### QMLS (CIK 2084026)
Resmi: [EDGAR dosya dizini](https://data.sec.gov/submissions/CIK0002084026.json) · [10-Q Q2 2026, 25 Ağu 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028924/quma20260630_10q.htm) · [424B4 doğrudan listeleme izahnamesi, 15 Tem 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023622/quma20260714_424b4.htm) · [8-K 16 Tem 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926023712/quma20260715_8k.htm) · [S-8 31 Ağu 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926029249/quma20260717_s8.htm) · [Form 4 / 13G dizini](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0002084026&owner=include&count=40) · [13G Focus Partners 3 Kas 2026](https://www.sec.gov/Archives/edgar/data/1542153/000154215326000020/primary_doc.xml).
Şirket PR: [8-K Ex.99.1 Q2 sonuçları 25 Ağu 2026](https://www.sec.gov/Archives/edgar/data/2084026/000143774926028918/ex_1008743.htm) · [PR 15 Eki 2026 (finviz aynası)](https://finviz.com/news/402901/qumulusai-puts-719-million-blackwell-agreement-into-production-signed-customer-contracts-surpass-500-million) · [PR 22 Eki 2026 TFC (finviz aynası)](https://finviz.com/news/406325/qumulusai-expands-closed-lease-financing-with-tfc-to-1236-million-funding-its-nvidia-blackwell-gpus-without-new-equity) · [PR 29 Eyl 2026 PDF](https://s21.q4cdn.com/597044239/files/doc_news/QumulusAI-Signs-240-9-Million-in-New-AI-Inference-Customer-Contracts-for-NVIDIA-Blackwell-B300-Capacity-2026.pdf) · [Atlanta 20 Ağu 2026](https://www.qumulusai.com/articles/qumulusai-anchors-metro-atlanta-data-center-site-with-a-contracted-375-mw-and-a-path-to-1075-mw).
İkincil: [Yahoo QMLS geçmişi](https://finance.yahoo.com/quote/QMLS/history/) · [StockAnalysis istatistik](https://stockanalysis.com/stocks/qmls/statistics/) · [StockAnalysis tahmin](https://stockanalysis.com/stocks/qmls/forecast/) · [MarketBeat short interest](https://www.marketbeat.com/stocks/NASDAQ/QMLS/short-interest/) · [MarketBeat analist](https://www.marketbeat.com/stocks/NASDAQ/QMLS/forecast/) · [Chardan başlangıcı (theoutpost)](https://theoutpost.ai/news-story/chardan-initiates-qumulus-ai-coverage-with-buy-rating-sets-24-50-price-target-on-ai-infrastructure-play-29687/) · [Ritter, IPOs: Long-run Returns](https://site.warrington.ufl.edu/ritter/files/IPOs-long-run-returns-on-IPOs.pdf).

### DGXX (CIK 1854368)
Resmi: [8-K Cerebras 8 May 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea0289585-8k_digi.htm) · [Ex.10.1 redakte sözleşme](https://www.sec.gov/Archives/edgar/data/1854368/000121390026053566/ea028958501ex10-1.htm) · [10-Q Q2 2026, 14 Ağu 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026089940/ea0301731-10q_digipower.htm) · [10-K FY2025](https://www.sec.gov/Archives/edgar/data/1854368/000121390026037677/ea0283764-10k_digipower.htm) · [DEF 14A 2 Kas 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026114925/ea0310068-def14a_digi.htm) · [S-3/A 11 Eyl 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026099261/ea0304511-s3a1_digi.htm) · [Form 4 CEO alımı 15 Eki 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026109819/ownership.xml) · [Cerebras 10-Q Q2 2026](https://www.sec.gov/Archives/edgar/data/2021728/000162828026056357/cbrs-20260630.htm) · [North Tonawanda Local Law No. 3 of 2026](https://www.northtonawanda.gov/documents/Website/2026/Local%20Law%202026%20-%20Moratorium%20Extension%20and%20SUP.pdf).
Şirket PR: [MCR/PR 5 May 2026](https://www.sec.gov/Archives/edgar/data/0001854368/000121390026053566/ea028958501ex99-1.htm) · [PR 7 Tem 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026075755/ea029720301ex99-1.htm) · [PR Q2 14 Ağu 2026](https://www.sec.gov/Archives/edgar/data/1854368/000121390026089450/ea030173001ex99-1.htm) · [PR $200M 13 Eki 2026](https://via.tt.se/pressmeddelande/4594325/digi-power-x-announces-dollar200-million-debt-financing-commitment-to-support-completion-of-alabama-ai-data-center-and-provides-expansion-update?lang=en) · [PR Q3 tarihi 28 Eki 2026](https://www.valuethemarkets.com/news/press-releases/digi-power-x-to-announce-2026-q3-financial-results-and-provi).
İkincil / yerel: [Bham Now ruhsat 29 Haz 2026](https://bhamnow.com/2026/06/29/data-center-columbiana-building-permits/) · [Bama Buzz](https://thebamabuzz.com/digi-power-x-data-center-shelby-building-permits/) · [E+E Leader ADEM izni 2 Kas 2026](https://www.environmentenergyleader.com/articles/45497-alabama-proposes-90-hour-cap-on-digi-power-x-diesel-engines) · [WBRC teşvik 24 Tem 2026](https://www.wbrc.com/2026/07/24/columbiana-receive-35m-data-center-deal-heres-how-it-could-change-your-neighborhood/) · [Shelby County Reporter 29 May 2026](https://www.shelbycountyreporter.com/news/columbiana-data-center-signs-1b-agreement-future-plans-revealed-f520ff1b/) · [Couch White FERC](https://www.couchwhite.com/nyiso-interconnection-compliance-in-focus-as-ferc-enforcement-resolves-digihost-investigation/) · [Yahoo DGXX geçmişi](https://finance.yahoo.com/quote/DGXX/history/) · [StockAnalysis DGXX](https://stockanalysis.com/stocks/DGXX/) · [DCD Cerebras](https://www.datacenterdynamics.com/en/news/cerebras-signs-on-for-40mw-of-capacity-at-digi-power-x-data-center-in-alabama/).

### AIB (CIK 2070542)
Resmi: [EDGAR dizini](https://data.sec.gov/submissions/CIK0002070542.json) · [10-K FY2025](https://www.sec.gov/Archives/edgar/data/2070542/000121390026036810/ea0282624-10k_blockchain.htm) · [10-Q Q2 2026, 13 Ağu 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026089151/ea0301093-10q_aibdata.htm) · [8-K ESA 1 Haz 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026063565/ea0292328-8k_blockchain.htm) + [Ex.10.1](https://www.sec.gov/Archives/edgar/data/2070542/000121390026063565/ea029232801ex10-1.htm) · [8-K halka arz 10 Haz 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026067320/ea0293892-8k_blockchain.htm) · [8-K ad değişikliği 29 Haz 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026073221/ea0296132-8k_aibdata.htm) · [8-K Texas 11 Eyl 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026099305/ea0305122-8k_aib.htm) · [8-K Nebius 1 Eki 2026 (Item 7.01)](https://www.sec.gov/Archives/edgar/data/2070542/000121390026105865/ea0307378-8k_aibdata.htm) · [8-K COO 28 Eki 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026113119/ea0309727-8k_aibdata.htm) · [Form 4 Tang 2 Eyl 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026096687/xslF345X06/ownership.xml) · [S-4 Ex.10.3 Lockhart ESA 2021](https://www.sec.gov/Archives/edgar/data/2070542/000121390025116271/ea026686601ex10-3_block.htm).
Şirket PR/sunum: [Nebius PR Ex.99.1](https://www.sec.gov/Archives/edgar/data/2070542/000121390026105865/ea030737801ex99-1.htm) · [Sunum 30 Eyl 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026105249/ea030723301ex99-1.htm) · [CEO mektubu 7 Eki 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026107421/ea030792301ex99-1.htm) · [Sunum 20 Eki 2026](https://www.sec.gov/Archives/edgar/data/2070542/000121390026110826/ea030897401ex99-1.htm).
İkincil / yerel: [Live5News moratoryum 22 Eyl 2026](https://www.live5news.com/2026/09/22/spartanburg-county-council-passes-data-center-moratorium-with-several-amendments/) · [Post and Courier/Yahoo 13 Eki 2026](https://www.yahoo.com/news/articles/data-center-planned-replace-crypto-090000749.html) · [BeBeez/DCD 29 Eki 2026](https://bebeez.eu/2026/10/29/aib-plans-50mw-ai-data-center-at-former-spartanburg-cryptomine-to-serve-nebius/) · [WSPA 3 Kas 2026](https://www.wspa.com/news/three-spartaburg-co-data-center-agreements-move-forward-after-hours-of-public-comment/) · [Compute Atlas CLT-01](https://www.compute-atlas.com/facilities/aib-clt-01-spartanburg-county-sc) · [Yahoo AIB](https://query1.finance.yahoo.com/v8/finance/chart/AIB?range=1y&interval=1d) · [StockAnalysis AIB](https://stockanalysis.com/stocks/aib/statistics/).

### VIVO (CIK 1681348)
Resmi: [EDGAR dizini](https://data.sec.gov/submissions/CIK0001681348.json) · [20-F FY2026, 2 Kas 2026](https://www.sec.gov/Archives/edgar/data/1681348/000149315226049646/form20-f.htm) · [6-K 21 May 2026](https://www.sec.gov/Archives/edgar/data/1681348/000149315226024744/ex99-1.htm) · [6-K 29 Haz 2026](https://www.sec.gov/Archives/edgar/data/1681348/000149315226030378/ex99-1.htm) · [6-K 29 Tem 2026 PIPE2](https://www.sec.gov/Archives/edgar/data/1681348/000149315226035125/ex99-1.htm) · [6-K 3 Ağu 2026 AWN](https://www.sec.gov/Archives/edgar/data/1681348/000149315226035769/ex99-1.htm) · [6-K 21 Ağu 2026 hisse sayısı](https://www.sec.gov/Archives/edgar/data/1681348/000149315226039731/form6-k.htm) · [6-K 28 Ağu 2026 ihraç](https://www.sec.gov/Archives/edgar/data/1681348/000149315226040659/form6-k.htm).
Şirket PR: [FY2026 sonuçları 3 Kas 2026](https://www.vivopower.com/news/vivopower-reports-fy2026-results-including-a-partial-period-contribution-from-mo-i-rana-data-center) · [İnşaat 12 Eki 2026](https://www.vivopower.com/news/vivopower-mobilizes-construction-of-40mw-ai-data-center-conversion-in-mo-i-rana-norway).
İkincil: [Yahoo VIVO](https://query1.finance.yahoo.com/v8/finance/chart/VIVO?range=1y&interval=1d) · [StockAnalysis VIVO](https://stockanalysis.com/stocks/vivo/statistics/) · [DCD T1 Energy Mo i Rana](https://www.datacenterdynamics.com/en/news/t1-energy-secures-50mw-grid-connection-for-former-battery-manufacturing-site-in-norway-set-to-become-data-center/).

### Evren dışı adaylar
Resmi: [HOST 8-K Ex.99.1 kira](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043135/ex99-1.htm) · [HOST 424B5](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226043454/form424b5.htm) · [HOST S-3](https://www.sec.gov/Archives/edgar/data/0001948864/000149315226047468/forms-3.htm) · [DUOT 8-K Ex.99.2](https://www.sec.gov/Archives/edgar/data/1396536/000107997326000262/ex99x2.htm) · [SLNH 10-Q](https://www.sec.gov/Archives/edgar/data/0000064463/000162828026056702/slnh-20260630.htm) · [NUAI 8-K PIPE](https://www.sec.gov/Archives/edgar/data/0002028336/000121390026113530/ea031006601ex99-1.htm) · [ZSQR 8-K](https://www.sec.gov/Archives/edgar/data/0001759186/000118518526003984/zsqrex99-1.htm).
İkincil: StockAnalysis istatistik/geçmiş sayfaları (slnh, vip, host, aib, dgxx, qmls, nuai, vivo, gpus, duot, tssi, ppsi, ipwr, tgen, slng, agpu, zsqr, bgde, any, lmfa, keel, iren, cifr, hut, apld, corz, btdr, nbis), 3 Kas 2026 kapanışı · [Stabilis Q2 2026](https://www.newswire.com/news/stabilis-solutions-announces-second-quarter-2026-results) · [Vulcan Q2 2026](https://www.accessnewswire.com/newsroom/en/oil-gas-and-energy/vulcan-infrastructure-and-power-reports-second-quarter-2026-results-1207572) · [DCD Duos](https://datacenterdynamics.com/en/news/duos-secures-cloud-provider-as-customer-for-20mw-of-data-center-capacity) · [DCD Soluna/APLD](https://datacenterdynamics.com/en/news/soluna-and-applied-digital-to-build-50mw-data-center-in-texas).

### Sektör ve taban oranlar
Resmi: [Nebius 6-K Q2 2026](https://www.sec.gov/Archives/edgar/data/0001513845/000110465926094568/tm2622968d1_ex99-2.htm) · [Core Scientific 8-K Q2 2026](https://www.sec.gov/Archives/edgar/data/0001839341/000183934126000013/q22026corescientificinc-ea.htm) · [Cipher 8-K Fluidstack/Google](https://www.sec.gov/Archives/edgar/data/1819989/000095010325012168/dp234624_ex9901.htm) · [TeraWulf 8-K Google warrant](https://investors.terawulf.com/sec-filings/all-sec-filings/content/0001104659-25-078084/tm2523008d2_8k.htm) · [Cerebras 8-K Q2 2026](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056186/cbrsannouncesfinancialresu.htm) · [SEC XBRL hisse sayısı API](https://data.sec.gov/api/xbrl/companyconcept/CIK0001854368/dei/EntityCommonStockSharesOutstanding.json) · [APLD Q1 FY2026](https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000068/apldq126earningsrelease.htm).
Şirket PR: [Hut 8 River Bend 17 Ara 2025](https://canada.hut8.com/resources/press-releases/hut-8-signs-15-year-245-mw-ai-data-center-lease-at-river-bend-campus-with-total-contract-value-of-usd7-0-billion) · [CoreWeave Q2 2026](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx).
İkincil: [Windsor Drake Q3 2026 değerlemeler](https://windsordrake.com/market-intelligence/reports/ai-infrastructure-valuations-q3-2026) · [DCK transformatör/PJM 12 May 2026](https://datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval) · [CoR Advisors/JLL capex](https://www.coradvisors.net/2026/06/ai-data-center-development-costs-2026.html) · [datacentres.com M&A 11 Ağu 2026](https://www.datacentres.com/news/data-centre-m-a-reaches-187b-peak-as-hyperscalers-consolidate-ai-infrastructure-slot1-2026-08-11) · [S&P Global madenci pivotu Şub 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/02/bitcoin-miners-pivot-to-ai-and-hpc-as-cryptocurrency-market-slumps) · [TechInformed IREN–Microsoft](https://techinformed.com/microsoft-signs-9-7-billion-iren-deal-for-nvidia-gb300-capacity/) · [StreetInsider CoreWeave rehberlik kesintisi](https://www.streetinsider.com/Earnings/CoreWeave+flags+hit+from+data+center+delay%2C+shares+fall/25585703.html) · [amcompute GPU kredileri](https://www.amcompute.com/gpu-debt/largest-gpu-loans) · [Panabee Mawson delist](https://www.panabee.com/news/mawson-infrastructure-rebrands-to-big-digital-energy-amid-nasdaq-delisting-defense) · [24/7 Wall St 2–3 Kas 2026 sektör](https://247wallst.com/investing/2026/11/02/cipher-digital-falls-5-on-revenue-miss-and-keefe-bruyette-target-cut-terawulf-and-iren-drop-4/).
