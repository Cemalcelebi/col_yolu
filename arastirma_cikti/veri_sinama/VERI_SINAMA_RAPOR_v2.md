# Veri sınaması v2 (22 Kasım 2026): ham + ayarlı fiyatlı göz PDF'i

## Bulgu özeti
- Cemal'in örneği ABT (sayfa 5), 20.04.2020. Yahoo ham değerleri 94,82 / 100,00 / 94,65 / 98,00, hacim 17.251.400: Cemal'in grafikte okuduğuyla (94,82 / 100 / 94,65 / 98 / 17,3 M) TUTUYOR. Bizim 83,92 / 88,51 / 83,77 / 86,74 aynı fiyatın temettü ayarlı hali; ham / ayarlı oranı bu günde 1,1298 (4 fiyatta aynı), hacim aynı. Önceki PDF'in hatası yalnız ayarlı fiyatı yazmasıydı; veri hatası değil.
- ABD (6 hisse) ve AVR (3 hisse): bizim veri Yahoo "Adj Close" ayarlı OHLC ile 120 günün hepsinde eşit (fark <= %0,0001; sabit çarpan çıkarılınca <= %0,00007). Hacim Yahoo hacmiyle birebir. Yahoo ham/ayarlı oranı yalnız temettü günlerinde basamak yapıyor, başka gün basamak yok.
- Sabit çarpan (basamak değil): WTRG 1,0081 ve CAT 1,0024 (bizim / Yahoo ayarlı). Bu pencere sonrasındaki (2023-12-29'a kadar) temettü ayarı kaynağı farkıdır; şekil ve günlük değişim bozulmaz.
- BIST (5 hisse): bizim fiyat = Yahoo ham x sabit çarpan (BURCE 1,3286; LIDFA 0,7294; AVHOL 1,1385; TRMET 1,2166; ENJSA 1,2217), çarpan pencerede sabit (CV <= 3e-16), hacim TERS çarpanla ölçekli (fiyat x hacim birebir). ENJSA'da (pencerede 11.04.2022 temettüsü) bizim veri Yahoo ayarlısına uymuyor (fark %3,9 basamak) ve hamla sabit orandadır: temettü AYARSIZ doğrulandı (yalnız ENJSA'da kanıt var; diğer 4 BIST pencerede temettü yok, onlar için kip FON_IZI kod okumasıyla aynı).
- Çarpanın NEDENİ AÇIKLANAMADI (HATA H-V2-1). Pencere sonrası ve 2023-12-29'a kadar bölünme yok (LIDFA hariç, aşağıda), yani çarpan pencerede görünmeyen farktır; en olası: Yahoo'nun bugünkü (2024-26 dahil) bölünme / bedelsiz ayarı bizim 2023-12-29 kesiğinde yok. 2024+ bölünme listesi sınırdaki yasak yüzünden çekilmedi; doğrulama için gerekir.
- Mum şekli ve günlük değişim yüzdesi bizde ve Yahoo hamında aynı (BIST dahil), yani ölçümleri bozan bir şekil / getiri farkı yok; fark yalnız düzey (çarpan).

## Doğrulama tablosu
| Sayfa | Hisse | Gün (bizim/Yahoo/ortak) | En büyük fark, bizim vs Yahoo ayarlı OHLC | Aynı, bir sabit çarpan çıkarılınca | Yahoo ham/ayarlı oranı (min-maks) | Oran yalnız temettü gününde mi basamak | Hacim eşit mi | Kip |
|---|---|---|---|---|---|---|---|---|
| 1 | NTLA (ABD) | 120/120/120 | 0.0000% | 0.00000% (çarpan 1.0000) | 1.0000-1.0000 | evet; yok (oran sabit) | evet (birebir) | ham ile aynı (bu pencerede temettü yok, ayırt edilemez) |
| 2 | CROX (ABD) | 120/120/120 | 0.0000% | 0.00000% (çarpan 1.0000) | 1.0000-1.0000 | evet; yok (oran sabit) | evet (birebir) | ham ile aynı (bu pencerede temettü yok, ayırt edilemez) |
| 3 | WTRG (ABD) | 120/120/120 | 0.8070% | 0.00007% (çarpan 1.0081) | 1.2096-1.2223 | evet; 2 temettü: 13.02.2020, 14.05.2020 | evet (birebir) | temettü ayarlı |
| 4 | SNPS (ABD) | 120/120/120 | 0.0000% | 0.00000% (çarpan 1.0000) | 1.0000-1.0000 | evet; yok (oran sabit) | evet (birebir) | ham ile aynı (bu pencerede temettü yok, ayırt edilemez) |
| 5 | ABT (ABD) | 120/120/120 | 0.0001% | 0.00005% (çarpan 1.0000) | 1.1298-1.1346 | evet; 1 temettü: 14.04.2020 | evet (birebir) | temettü ayarlı |
| 6 | CAT (ABD) | 120/120/120 | 0.2379% | 0.00005% (çarpan 1.0024) | 1.1159-1.1345 | evet; 2 temettü: 17.04.2020, 17.07.2020 | evet (birebir) | temettü ayarlı |
| 7 | BATS.L (AVR) | 120/120/120 | 0.0000% | 0.00004% (çarpan 1.0000) | 1.0052-1.0055 | evet; 2 temettü: 27.06.2019, 03.10.2019 | evet (birebir) | temettü ayarlı |
| 8 | TEL2-B.ST (AVR) | 120/120/120 | 0.0000% | 0.00004% (çarpan 1.0000) | 1.8214-1.8536 | evet; 1 temettü: 07.05.2019 | evet (birebir) | temettü ayarlı |
| 9 | RCO.PA (AVR) | 120/120/120 | 0.0000% | 0.00003% (çarpan 1.0000) | 1.1605-1.1605 | evet; yok (oran sabit) | evet (birebir) | temettü ayarlı |
| 10 | BURCE (BIST) | 120/120/120 | 33.8608% | 0.00001% (çarpan 1.3386) | 1.0075-1.0075 | evet; yok (oran sabit) | hayır; ters çarpan 0.7527 (fiyat x hacim aynı) | bölünme ayarlı, temettü ayarsız |
| 11 | LIDFA (BIST) | 120/120/120 | 23.2735% | 0.00001% (çarpan 0.7673) | 1.0519-1.0519 | evet; yok (oran sabit) | hayır; ters çarpan 1.3710 (fiyat x hacim aynı) | bölünme ayarlı, temettü ayarsız |
| 12 | AVHOL (BIST) | 120/120/120 | 13.8488% | 0.00000% (çarpan 1.1385) | 1.0000-1.0000 | evet; yok (oran sabit) | hayır; ters çarpan 0.8784 (fiyat x hacim aynı) | bölünme ayarlı, temettü ayarsız |
| 13 | TRMET (BIST) | 120/120/120 | 21.6599% | 0.00000% (çarpan 1.2166) | 1.0000-1.0000 | evet; yok (oran sabit) | hayır; ters çarpan 0.8220 (fiyat x hacim aynı) | bölünme ayarlı, temettü ayarsız |
| 14 | ENJSA (BIST) | 120/120/120 | 61.5112% | 3.93378% (çarpan 1.5540) | 1.2267-1.3220 | evet; 1 temettü: 11.04.2022 | hayır; ters çarpan 0.8185 (fiyat x hacim aynı) | bölünme ayarlı, temettü ayarsız |

Not: "En büyük fark" = bizim OHLC / (Yahoo ham x Adj Close / Close) - 1, 120 günün en büyüğü. NTLA, CROX, SNPS'te ham ile ayarlı aynı olduğundan (temettüsüz, oran 1,0000) kip bu pencerede AYIRT EDİLEMEZ; ABD kipi diğer 3 hisse ve AAPL (v1 raporu) ile "temettü ayarlı".

## Kip
- ABD: bölünme + temettü ayarlı (WTRG, ABT, CAT'ta 120 günde sabit oranla Yahoo ayarlısı). 
- AVR: hisse başına net: BATS.L, TEL2-B.ST, RCO.PA üçü de TEMETTÜ AYARLI (bizim / Yahoo ayarlı = 1,0000; bizim / ham sırasıyla 0,9947, 0,5413, 0,8617). RCO.PA'da pencerede temettü yok ama ayarlı (sonraki temettüler). Örneklem 3 hisse; pazar geneli için yeterli değil ama kod okumasındaki belirsizlik (v1 raporu) bu kanıtla kapandı.
- BIST: bölünme ayarlı, temettü ayarsız (yukarı). Çarpan açıklanamadı.

## PDF
- VERI_SINAMA_GOZ_v2.pdf: 15 sayfa (kapak + 14 hisse). Her sayfada iki blok tablo (1: ham, Cemal'in grafiği; 2: bizim veri + oran), ham mum grafiği, hacim, temettü günleri, AYNI / FARKLI kutuları.
- Pencere gün sayısı Yahoo'da bazen fazladır (tatil / hacimsiz satırlar); hacmi 0 olan Yahoo satırları (BURCE 10, LIDFA 2, AVHOL 1, TRMET 8) bizim temiz veriyle aynı 120 güne indirildi (çizimde yok). Cemal'in grafiğinde bu gün varsa mum eksik görünebilir.
- LIDFA (sayfa 11): Yahoo pencere içinde 04.12.2018'de 1,5 bölünme gösteriyor; pencereden sonra (2023-12-29'a kadar) 11.05.2020 x2, 28.09.2022 x1,5, 23.06.2023 x1,88 (çarpım 5,64). Sayfa notu yazıldı; Yahoo ham zaten bu bölünmelere göre ayarlıdır, ayarsız gösteren uygulamada sayılar 5,64 kat farklı olur. LIDFA fiyatları bu yüzden çok küçük (~0,07 TL): bizim ve Yahoo seviyesi ayarlıdır.

## HATA
- H-V2-1 (BIST, 5 hisse, veri / düzey): bizim fiyat ile Yahoo ham arasında sabit çarpan (BURCE 1,3286; LIDFA 0,7294; AVHOL 1,1385; TRMET 1,2166; ENJSA 1,2217), hacimde ters çarpan; nedeni kanıtlanmadı. Etki: şekil ve getiri yok; düzey ve işlem değeri ölçüleri (TL hacim) bizde yine tutarlı çünkü fiyat x hacim aynı. Önerilen: 2024+ Yahoo bölünme listesiyle çarpan açıklanır (iş tanımı gerekir).
- H-V2-2 (ABD, WTRG 1,0081, CAT 1,0024): bizim / Yahoo ayarlı sabit çarpan; temettü ayarı kaynağı farkı. Etki yok (sabit).
- H-V2-3 (süreç): v1 PDF yalnız ayarlı fiyat yazdı, kapağında "TradingView ADJ" uyarısı vardı ama sayfa tablosunda ham yoktu; Cemal karşılaştırmada "tutmuyor" gördü. Düzeltme: v2.
- H-V2-4 (v1 kapak yanlışı): v1 kapağı BIST için "bölünme ayarı ile aynı, ADJ kapalıyken sayılar birebir tutmalı" diyordu; BIST'te bizim fiyat Yahoo hamıyla sabit çarpanla farklıdır (H-V2-1). v1 BIST sayfaları bu yüzden de tutmazdı.
- Yahoo / bizim gün eşitsizliği: BIST'te Yahoo'da hacimsiz tatil satırı var (yukarı), bizim veride yok; uyuşmazlık değil (K3 elemesi).

## KONTROL LİSTESİ
- K2 geleceğe bakma: EVET. Yahoo istekleri bitiş <= 2023-12-29 (end 2023-12-30 dışlayıcı); bizim veri yalnız /tmp/kasa/acik (en geç 2023-12-29). Pencere sonrası bölünme araması da 2023-12-29'da kesik. Getiri / sinyal ölçülmedi.
- K3 geçerli bar: EVET. Hacmi 0 / boş Yahoo barı grafik ve tablodan atıldı (kaç gün yukarıda); bizim veri H>=L, V>0, C>0 süzgecinden.
- K6 veri birimi: EVET. Kip hisse başına sınandı (yukarı); AVR pens (BATS.L) birimi ham/ayarlı oranıyla tutarlı; BIST çarpanı AÇIKLANAMADI (HATA H-V2-1, kapanmadı).
- K10 ayrıştırma: EVET. Ham satırdan elle >= 3: ABT 20.04.2020 94,82/100/94,65/98 Cemal'in okumasıyla tuttu; sayfa 5, 6, 11 PDF görüntüsünden okundu (tablo = JSON). Hacim sütunu kaynak hacimle.
- K13 süreç: EVET. Tiingo'ya istek yok; Yahoo isteklerinde yalnız sembol ve tarih (e-posta / isim yok); yasak dosyalara dokunulmadı; çakışma kapısı olan modül değişmedi; yahoo_ham_v2.pkl (veri önbelleği) commit edilmedi. Kod değişmedi (yeni betik), "çalışma zamanını yeniden başlat" gerekmez.
