# K53 — ÖN KAYIT: Bilgi Direnci (BDS), Analist Dağınıklığı (ADE), Karar Gecikmesi (KGS) (29 Ekim 2026, sonuç görülmeden)

K51 kararı (**İZ DEĞİL**) ve K51 kuralları (üçlü bariyer +%20 / −%10 / 60 gün, maliyet, delist, K51 tabanı e_y = aynı gün aynı oynaklık ondalığı) **değişmez**. Bu ayrı bir keşif deneyidir; Çöl Yolu'nun yerine geçmez. Hiçbir eşik sonuca bakılarak değiştirilmez. Sonuç olumlu çıksa bile "İZ" denmez; bağımsız doğrulama (sinyal ≥ 01.09.2026, en erken Mart 2027) gerekir. Cemal'in K53 mesajı ADE ve KGS tanımlarında kesik geldi; **ADE ve KGS tanımları aşağıda Claude tarafından sabitlendi**, sonuca bakılarak değiştirilmez.

## 1. Veri ve olay

- Veri: K51 v1.2 paneli (ABD, 2.752 likit hisse) + K52 Yahoo analist not günlüğü (310 bin kayıt; EPS, gerekçe yok; saat UTC). Sızıntı: kayıt tarihi ≤ işlem günü d0; d0 = kayıt tarihine eşit ya da sonraki ilk işlem günü (en çok 4 takvim günü sonra, yoksa olay düşer).
- **Olay (d0):** olumlu analist revizyonu = Action up VEYA hedef Raises VEYA init + alım kümesi (K52 ile aynı). "İlk" olumlu revizyon: aynı hissede önceki 20 işlem gününde başka olumlu kayıt yoksa. Aynı gün birden çok kurum tek olay sayılır.
- **Tepki penceresi:** d0 .. d0+4 (5 işlem günü). **Karar anı** = d0+4 kapanışı; **giriş** = d0+5 açılışı (K51 giriş kuralı). Etiket: panelde i = d0+4 satırının y (+%20 önce), net, e_y, e_net. Panelde o gün likit değilse olay ölçülmez (sayısı yazılır).

## 2. Değişkenler (hepsi d0+4 kapanışında bilinen bilgiyle)

Pencere A = [d0, d0+4]; önceki pencere B20 = [d0−20, d0−1]; satış baskısı için A10 = [d0−5, d0+4], B10 = [d0−15, d0−6].
- Tepki ölçüleri: r5 = C[d0+4] / C[d0−1] − 1; SPY göreli r5; sektör göreli r5 (sektör = aynı sektördeki evren hisselerinin eşit ağırlıklı günlük ortalaması; sektör bilinmiyorsa boş); hacim değişimi = ort hacim(A) / ort hacim(B20) − 1; aşağı gün sayısı (A, 0-5); ATR değişimi = ATR5(A) / ATR20(B20) − 1 (gerçek aralık).
- **Satış baskısı** (A10 ve B10 ayrı ayrı): negatif gün oranı; negatif günlerin ortalama büyüklüğü (|getiri|); aşağı günlerde hacim payı (aşağı gün hacmi / toplam hacim); kapanışın günlük aralıktaki yeri (CLV = (C−L)/(H−L), ortalama). **İyileşme sayısı** (0-4) = A10'da B10'a göre: negatif oran ↓, negatif büyüklük ↓, aşağı hacim payı ↓, CLV ↑.
- **BDS (0-3)** = şu üç şartın sayısı: (1) fiyat zayıf: SPY göreli r5 ≤ 0; (2) satış gücü azalıyor: iyileşme sayısı ≥ 3; (3) oynaklık düşüyor: ATR değişimi < 0. Olumlu bilgi olay tanımıyla zaten var. **Yüksek BDS = 3/3.** Bileşik puan başka biçimde kurulmaz; bileşenler ayrı da raporlanır.
- **ADE (Analist Dağınıklık Endeksi; Claude tanımı):** d0'dan önceki 90 takvim günündeki (d0 dahil) kayıtlardan her kurumun en son hedef fiyatı alınır; en az 3 kurum varsa ADE = hedef fiyatların değişim katsayısı (std / ortalama). 3 kurumdan az ise boş (ölçülemez, sayısı yazılır). Olay içi üçte birlik dilimler.
- **KGS (Karar Gecikmesi Süresi; Claude tanımı):** d0−1 kapanışından itibaren SPY'ye göreli birikimli getirinin ilk kez ≥ +%5 olduğu işlem günü sayısı k (1..20). 20 günde olmazsa KGS = "yok". Kova: **hızlı** (1-5), **geç** (6-20), **yok**. KGS testinde karar anı tepkinin gerçekleştiği gün (d0+k kapanışı), giriş ertesi açılış; "yok" kovasında karar anı d0+20. Böylece hiçbir kova gelecek bilgisi kullanmaz.
- Ek: olumlu revizyonun önceki 20 günün dibinden ≥ %10 yükseliş SONRASI gelip gelmediği (K52 H4 ölçüsü).

## 3. Gruplar (K51 tabanıyla ayarlı; karar anı d0+4)

- **G1:** olay ∧ BDS = 3. **G2:** olay ∧ BDS < 3 (alt kırılım BDS 0 / 1 / 2).
- **G3:** grafik var, revizyon yok: panelde P1 ∪ ÇEK günü ∧ önceki 20 işlem gününde olumlu kayıt yok.
- **G4:** hiçbiri: ÇEK dışı likit panel günlerinden rastgele örnek (tohumlu) ∧ önceki 20 günde olumlu kayıt yok ∧ P1 değil.
- **G5 (çürütme kontrolü, "şekil var, bilgi yok"):** G4 örneklemi içinde aynı pencere ölçüleriyle BDS = 3 olan günler (olumlu revizyon olmadan aynı fiyat-hacim-oynaklık deseni).

## 4. Birincil ölçüt ve karar (sabit, K52 ile aynı)

Δ = ortalama(y − e_y | A) − ortalama(y − e_y | B). Hücre TUTAR: n_A ≥ 30 ve n_B ≥ 30, Δ ≥ +0,05, ay kümeli bootstrap %95 alt uç > 0, net fark > 0. Dönemler 2016-22, 2023, 2024-26; üçünde tutarsa "DESTEKLENİYOR (KEŞİFSEL)", birinde n < 30 "YETERSİZ ÖRNEKLEM", aksi "DESTEKLENMİYOR"; Δ ≤ −0,05 ve üst uç < 0 "TERS YÖN". Hisse × çeyrek kümeli aralık yazılır. Çoklu test: T1, T2, T3, T4, T5, T6 bir aile; 2023-26 tek yönlü p'leri Holm. 2023-26 bağımsız değildir.

## 5. Testler (destekleyen ve çürüten birlikte)

| Kod | Soru | Destekler | Çürütür / reddetme |
|---|---|---|---|
| T1 (birincil) | G1 (yüksek BDS) − G2 | Δ ≥ +5, CI > 0, net > 0, üç dönem | koşullardan biri sağlanmaz |
| T1b | BDS 3 − BDS 0 (doz-yanıt) | tek yönlü artış | artış yok |
| T2 | G1 − G3 (grafik var, revizyon yok) | ≥ +5 | < +5 |
| T3 | G1 − G4 (hiçbiri) | ≥ +5 | < +5 |
| **T4 (çürütme A)** | G1 − G5 (aynı şekil, bilgi yok) | ≥ +5 → bilgi gerekli | < +5 → desen tek başına aynı işi yapıyor, "bilgi direnci" diye bir şey yok |
| T5 (KGS) | geç tepki (6-20) − hızlı (1-5); geç − yok | geç > hızlı ve geç > yok, ≥ +5 | aksi; "yok" kovası en iyi ise gecikme değil tepkisizlik |
| T6 (ADE) | üst üçte bir − alt üçte bir | ≥ +5 (görüş ayrılığı primi) | < +5 ya da ters |
| T7 (çapraz, bilgi) | BDS = 3 olaylarda KGS kova payları (BDS = 0 ile karşılaştır); geç ∧ BDS3 − geri kalan | BDS3 olaylar daha çok "geç" tepki veriyorsa iki fikir birbirini destekler | BDS3 olaylar çoğunlukla "yok" ise yüksek direnç = kılık değiştirmiş kötü haber |
| T8 (çürütme B) | G1 içinde revizyon fiyat yükselişinden SONRA gelen vs ÖNCE gelen | fark yok | "önce gelen" çok daha iyiyse etki revizyon zamanlamasından |
| Kırılganlık | en iyi 20 hisse çıkarma, yıl yıl, kaynak (V_ABD / K34), BDS bileşenleri tek tek | | |

**Karar kuralı:** T1, T5, T6 üçünden hiçbiri "DESTEKLENİYOR" değilse hipotez KAPANIR (eşik uydurulmaz). T1 destekleniyor ama T4 < +5 ise "desen etkisi, bilgi etkisi değil" yazılır; K53 yine kapanır. Her durumda K51 kararı değişmez.

## 6. Çıktılar

K53_onkayit.md (bu), K53_OLAYLAR.csv.gz (olay × ölçüler), K53_GRUPLAR.csv, K53_HIPOTEZ_TESTI.csv, K53_RAPOR.md. Kod: COL_YOLU_ABD.py v1.4 (`cy_v14_calistir`), test_col_yolu_abd.py ekleri (BDS / satış baskısı / KGS hesapları sentetik seride).
