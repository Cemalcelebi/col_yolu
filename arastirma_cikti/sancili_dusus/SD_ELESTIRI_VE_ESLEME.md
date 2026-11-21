# SANCILI DÜŞÜŞ (SD): BINBN v4 kodunun eleştirisi ve mevcut modüllerle eşlemesi

Kaynak: `arastirma_cikti/sancili_dusus/BINBN_v4_final_colab.py` (Cemal'in Colab kodu, 293 satır; değiştirilmedi). Bu belgede ölçüm yok, veri indirilmedi, kod yazılmadı.
Kontrol listesi (`python IZ_KARNE.py kontrol istanimi`, K1-K14) okundu ve bölüm 2'de madde madde uygulandı.

## 0. BULGU (kısa)

- SD'nin projede bire bir karşılığı yok. En yakın üç ölçü: S5_DİP (Ç184; eğim −%2..+%10, yani SD'nin yalnız hafif ucunu kapsıyor), DS20 "alt bantta yürüme" (DS havuzu; aşağı sürünmenin Bollinger hali) ve KT05 / KT08 kartları. Hiçbiri "dipte, küçük mumla, aşağı eğimli kutu → yukarı" iddiasını ayrı sınamadı.
- Yakın ölçülerin sonucu SD lehine değil: S5_DİP 60 gün eşli fark ABD 2023 +%0,2 [−2,0; +2,1], ABD 2024-26 %0,0 [−2,2; +2,7] (ÖLÇÜLEMEDİ, olasılık etiketi YOK). DS20 eski h5 cetvelinde önceden yazılan "−" yönün TERSİNE çıktı (ABD sınama FARK +2,4 [+0,3; +4,8]), ama düzeltilmiş CETVEL2 R15 ile SORGULA (4 karar hücresinin 0'ında tuttu). Bu bir emare değil, yalnız bilgi.
- Kodun BINBN üzerindeki "DOGRU" etiketleri karar için kullanılamaz: kutu sonu 3 bar sonra bilinir ama giriş kutu sonu kapanışından alınıyor (geleceğe bakma), "önceki düşüş" şartı hesaplanıyor ama tip kararına girmiyor, küçük mum gövdeyle ölçülüyor (Cemal'in tanımı H−L), N tipinin doğrusu yukarı +%10 istiyor, BASARISIZ etiketi sonraki kutunun varlığına bağlı. Toplam 22 kusur (bölüm 2).
- SD, Cemal'in kendi iki kuralıyla çelişiyor: C2 / K6 / K40 ("alçalan dipler zinciri = güven yok", "dip savunulur") ve SIKISMA_OBEK satır 4 ("yükselişteki bölge sancılı değil dinlenme olmalı"). Bu yüzden ölçümde yön önceden "?" (iki yönlü) yazılmalı; iki tahminin hangisinin tuttuğu ölçüyle görülür.
- Ölçülebilir SD tanımı ve ölçüm planı bölüm 5-6'da. Karar ölçüsü CETVEL2 v2.2 R15 / R30 (giriş t+1 açılış, stop yok), eş = aynı gün aynı ATRP × likidite × F15 kovası, 200 tohum plasebo, KT00 momentum kontrolü aynı koşuda. Kör sınama yalnız KASA'nın açılmamış bloklarında (2024Q1'den sırayla) mümkün; 2023 blokları KART_TUR1 için açıldı, SD için kör değil.

## 1. KOD NE YAPIYOR (10 satır)

1. Veri: tek CSV (BINBN, Drive'dan gdown); sütunlar eşlenir, "," silinir, `body_pct = |C−O| / O`, `gm` = bütün serinin gövde medyanı (satır 22-23).
2. Kutu maskesi (W = 10): son 10 barın gövde medyanı / gm < 0,75 VE 10 bar yüksekliği (maxH − minL) / orta %2 ile %28 arası (satır 27-36).
3. Kutu: maske ilk doğru olduğunda başlangıç 9 bar geriye atılır (`start = i−W+1`); en çok 2 bar maske kopukluğu tolere edilir (GAP_TOL = 2); 3. yanlış barda kutu kapanır, `end` = son doğru bar; uzunluk filtresi `end−start < 5` (satır 58-70).
4. Kutu ölçüleri: üst / alt = kutu içi maxH / minL; `sl_val` = son 10 barın kapanış eğimi / (orta × 10); `dip_yakin` = (C_start − önceki 30 bar min L) / min L; `zirve_yakin` benzeri tepe için; `pslope` = kutu öncesi 25 bar kapanış OLS eğimi / ortalama (satır 71-81).
5. Tip: SD = `sl_val < −0,0003` VE `dip_yakin < 0,35` (önce bakılır); P = `sl_val > 0,0005` VE `dip_yakin < 0,15`; N = `sl_val < −0,0005` VE `zirve_yakin < 0,15`; P? / N? yalnız eğim; ? geri kalan (satır 88-99).
6. Birleştirme: sonraki kutu öncekinin bitişinden en çok 3 takvim günü sonra başlıyorsa birleşir; tip yalnız yeni parça "P" içeriyor ve önceki "N" içermiyorsa değişir (satır 108-122).
7. Sağ ayak (P, P?, SD "pozitif"): kutu sonu kapanışından (`C[ei]`) sonraki 29 barda (`ei+1 .. ei+29`) kutu altının `(1 − tol)` altında 2 ardışık kapanış = İHLAL; tol, o ana kadarki en büyük kazanca göre %1 / 2 / 3 / 5 / 8 (satır 135-174).
8. Tutunma: aynı 29 barda başlangıç kapanışının +%10 üstünde 2 ardışık kapanış (tipten bağımsız, ayrı döngü) (satır 176-188).
9. Puan: o ana kadarki en büyük hareket (MFE) %1 / 10 / 25 / 50 / 100 basamakları → 1P-5P; DOGRU = ihlal yok VE tutunma var (satır 127-133, 190-195).
10. BASARISIZ = DOGRU değil, İHLAL değil ve listede sonraki bir kutu var; yoksa BEKLE. Çıktı: konsol listesi + plotly HTML (Drive'a kopya) (satır 196-293).

## 2. KUSURLAR TABLOSU

| # | Kontrol | Satır / ifade | Kusur | Etki |
|---|---|---|---|---|
| 1 | K1 kontrol grubu | bütün dosya | Eş yok, taban yok, plasebo yok. DOGRU / puan yalnız olayın kendi yolu. | "SD yukarı çözülür" sözü hiçbir kıyasla desteklenmiyor; aynı günlerde rastgele hisse de +%10'a gidebilir. |
| 2 | K1 mekanik üstünlük | 135-141 `ihlal_tolerans(max_hareket)` | Tolerans kazanca göre genişliyor: yükselen kutu daha zor İHLAL olur. | Etiket kazananı kendiliğinden korur; DOGRU payı tanım gereği şişer. |
| 3 | K2 geleceğe bakma | 23 `gm = df["body_pct"].median()` | Küçük mum ölçüsünün paydası bütün serinin (gelecek dahil) medyanı. | Geçmişteki kutular sonradan gelen oynaklığa göre seçilir; gerçek zamanda aynı kutu çıkmayabilir. |
| 4 | K2 geleceğe bakma | 64-68 `gap<=GAP_TOL ... end=i-gap` | Kutu sonu ancak 3. maske-yanlış barda (`end+3`) bilinir. | Giriş `end` kapanışı; sonuç penceresi bilinmeyen 3 barı içeriyor. |
| 5 | K2 geleceğe bakma | 108-122 `merge_cols` | Birleşme, sonraki kutunun gelip gelmemesine bağlı; birleşen kutunun `ei`'si ileri kayar. | Hangi bitişten ölçüldüğü geleceğe bağlı. |
| 6 | K2 geleceğe bakma | 196-204 `basarisiz` | BASARISIZ = sonraki kutu var mı; pencerenin (30 bar) dolup dolmadığına bakılmıyor. | Son kutu pencere dolsa da hep BEKLE; ara kutu pencere dolmadan BASARISIZ olabilir. |
| 7 | K2 / sıra | 153-188 iki ayrı döngü | İhlal ve tutunma ayrı döngüde; hedefin stop'tan ÖNCE gelip gelmediğine bakılmıyor. | 5. barda +%10 tutunup 25. barda ihlal eden kutu İHLAL; CETVEL2 / h5 mantığında bu kazanç sayılırdı. |
| 8 | K2 gerçek zaman | 62 `start=max(0,i-W+1)` | Kutu başı 9 bar geriye atılıyor; `dip_yakin` `C[start]`'tan ölçülüyor. | `i` anında bilinen bilgi (geçmiş barlar), geleceğe bakma değil; ama kutu "başladı" demek `i` gününde mümkün, `start` gününde değil. Grafikteki kutu sol kenarı gerçek zamanda görülmez. |
| 9 | K3 geçerli bar | 17-20, 22 | H>L ve V>0 denetimi yok; Volume yoksa 0 ile dolduruluyor ve hiç kullanılmıyor. | Kilitli tavan / taban (O=H=L=C) ve hacimsiz bayat bar gövde 0 → "en küçük mum"; işlem görmeyen dönem kusursuz çöl gibi görünür (H004, H037 tekrarı). |
| 10 | K4 tekilleştirme | 144-153 | Kutular arası 30 bar beklenmiyor; birleşmeyen yakın kutuların 29 bar sonuç pencereleri örtüşüyor. | Aynı yükseliş birden çok DOGRU sayılabilir; n bağımsız değil. Medyan yok. |
| 11 | K5 giriş fiyatı | 147 `baslangic_fiyat=df["Close"].iloc[ei]` | Giriş kutu sonu kapanışı; doğru giriş kutu sonunun bilindiği barın (`end+3`) ertesi açılışı. | MFE ve +%10 tutunma iyimser; 3 bar ve bir gece boşluğu bedavaya sayılıyor. |
| 12 | K6 veri birimi | 13 `"adj close":"Close"` | Hem Close hem Adj Close varsa iki "Close" sütunu oluşur (satır 18'de hata ya da karışık); yalnız Adj Close varsa düzeltilmiş C ile düzeltilmemiş O / H / L karışır. | Temettü / bedelsiz günlerinde gövde ve eğim yanlış; bölünme denetimi yok. |
| 13 | K6 / K10 ayrıştırma | 18-19 `.str.replace(",","")` | Binlik ayırıcı varsayımı. Türkçe ondalık virgüllü CSV'de "12,34" → 1234. | 100 kat fiyat hatası; elle satır denetimi yok. BINBN CSV'si repoda yok, doğrulanamadı. |
| 14 | K6 tanım (Cemal) | 22, 27 `body_pct=|C−O|/O` | Küçük mum gövdeyle ölçülüyor. Cemal'in tanımı fitiller dahil aralık (H−L); COL_v1.py satır 137 `MUM_OLCU='aralik'`, HİPOTEZ_ENVANTERİ A3 "KAPALI (tanım)". | Uzun fitilli doji dizileri "küçük mum" sayılır; Cemal'in gözüyle seçtiği kutularla aynı kutular çıkmaz. |
| 15 | K7 hayatta kalma | 9-12 | Tek hisse, Cemal'in grafikte gördüğü için seçilmiş (BINBN). | Seçim yanlılığı en üst düzeyde; batanlar yok. |
| 16 | K8 örneklem | 207 `len(cols)` | n = BINBN kutu sayısı (tahminen < 30); tek dönem, tek pazar; ABD / AVR yok. | "Bulgu" denemez; CLAUDE.md karar hücreleri (ABD, AVR × 2 dönem) hiç ölçülmemiş. |
| 17 | K9 ön kayıt | 25, 36, 89-99, 128-141 | Eşikler (0,75; %2-28; −0,0003; 0,35; 0,15; 0,0005; tol basamakları) "v4 final" adıyla aynı grafikte ayıklanmış. | Eşik sonuca göre oynanmış sayılır; aynı veride sınama kör değil. |
| 18 | K11 yeniden üretim | 207-215, 280 | Satır dosyası yok (yalnız print + HTML). | Etiketler bağımsız kodla yeniden üretilemez. |
| 19 | K12 ifade | 195, 210 `DOGRU`, 128 puan | "DOGRU" bir tahminin doğruluğu değil, yol etiketi; puan MFE (en iyi kapanış), gerçekleşen getiri değil. | 5P "kutu %100 kazandırdı" diye okunursa yanıltır. |
| 20 | K13 süreç | 3-293 modül düzeyi | Çakışma kapısı yok (`df`, `n`, `cols`, `t`, `b`, `start`, `end` Colab'daki adları ezer); `except:` çıplak (289); log yok; çıktı adı sabit (`BINBN_v4_final.html`), Drive yolu `COLAB_VERILER` kökü. | Aynı oturumda başka kodla çalışırsa sessiz ad ezme; hata yutulur. |
| 21 | K14 boyut | yok | Gerçek para kuralı yok (boyut tavanı, olay bazlı çıkış, 2x). | Öneri / alım için kullanılırsa kapı (c) eksik. Şu an ölçüm kodu olduğu için UYGULANMAZ. |
| 22 | Tanım hatası | 81 `pslope` ve 88-91 `sancili` | Yorum satırı 40 ve 85 "önceki eğim negatif" diyor; `pslope` hesaplanıyor ama tip kararına girmiyor (yalnız yazdırılıyor). Ayrıca docstring lookback 20, çağrı 25, yorum W_dip (30). | SD "düşüş sonrası" şartını aslında içermiyor: yükseliş içindeki kısa geri çekilme de SD olur. |
| 23 | Tanım hatası | 77, 90 `dip_yakin<0.35` | Ölçü kutunun alt bandı değil ilk kapanışı; alt sınır yok: kutu yeni dip yapıyorsa `dip_yakin` negatif ve geçer. %35 çok geniş. | SD yeni dip yapan "düşen bıçak" kutularını da içeriyor (KT08 ile örtüşme); "dip savunulur" şartı yok. |
| 24 | Tanım hatası | 89 vs 101 | SD eşiği −0,0003, eğim oku eşiği 0,0005: −0,0005..−0,0003 arası kutu grafikte "→" (yatay) ama tip SD. Eğim alt sınırı yok (10 barda −%25 de SD). | Etiket ile grafik çelişir; "hafif" eğim tanımı yok. |
| 25 | Tanım hatası | 73 `sl_val=sl_col.iloc[end]` | Tip yalnız kutunun SON 10 barının eğimine bakıyor, bütün kutuya değil. | 40 barlık kutunun tipi son iki haftaya göre değişir. |
| 26 | Hesap hatası | 70 `if end-start<5` | `start = i−9` ve `end ≥ i` olduğundan `end−start ≥ 9` her zaman; filtre hiç çalışmaz (ölü kod). | Gerçek en kısa kutu 10 bar; "≥ 5 bar" kuralı kodda yok. |
| 27 | Hesap hatası | 119 merge tip kuralı | `"P" in d["tip"]`: önceki SD + sonraki P / P? → tip P olur; önceki ? + sonraki SD → ? kalır; `n`, `pslope`, `dip_yakin`, `ed_price` birleşmede güncellenmiyor. | SD sayısı (başlıktaki `SD=`) birleşme sırasına göre değişir; yazdırılan alanlar bayat. |
| 28 | Hesap hatası | 182 `yukari2 >= 0.10` tipten bağımsız | N / N? / ? tiplerinde de DOGRU için +%10 YUKARI tutunma isteniyor; N'nin ihlali ise yukarı (`t*(1+tol)`). | N tipi DOGRU olamaz gibi; N'nin "doğrusu" yanlış tanımlı. |
| 29 | Küçük hata | 153 `range(ei+1, min(ei+30,n))` | 30 değil 29 bar. | Yorumla tutarsız; etkisi küçük. |
| 30 | Küçük hata | 114 `pd.Timedelta(days=3)` | Birleşme takvim günüyle, kopukluk (GAP_TOL) barla ölçülüyor. | Hafta sonu / bayram kutuları farklı birleştirir. |

## 3. İŞE YARAR FİKİRLER (Cemal'in bu kodda sakladığı bilgi)

1. **Sancılı düşüş sınıfı.** Düşüş sonrası, dip bölgesine yakın, küçük mumlarla HAFİF AŞAĞI sürünen kutu (`sl_val < −0,0003`, `dip_yakin < 0,35`). Hipotez: bu kutu yukarı çözülür (kod SD'yi P ile aynı "pozitif" tipe koyuyor). Projede düşüş sonrası sıkışma hep yatay ya da taban korunan diye tanımlandı (S4 YATAY |net| ≤ %3; S5 eğim ≥ −%2; C2 "dip savunulmuş"). Aşağı eğimli küçük mumlu kutu ayrı sınıf olarak hiç sınanmadı. Yeni olan budur.
2. **Konum × eğim tablosu.** Tip, iki basit ölçünün kesişimi: kutu dipte mi tepede mi (`dip_yakin` / `zirve_yakin`) ve kutu içi eğim (+ / 0 / −). 2 × 3 hücre: P (dip, +), SD (dip, −), N (tepe, −) ve ötekiler. Basit, ölçülebilir, her hücre ayrı sınanabilir. N, Cemal'in "tepede sıkışma dağıtımdır" kuralının mekanik hali.
3. **Sağ ayak doğrulaması, 2 ardışık kapanış.** İhlal de tutunma da tek kapanışla değil, art arda 2 kapanışla sayılıyor. Tek günlük fitil / gürültüyü ayıklayan basit bir onay kuralı. CETVEL2'nin stop'suz R15'ine BİLGİ etiketi olarak eklenebilir (karar ölçüsü değil).
4. **Dinamik tolerans.** Kazanç büyüdükçe kutu altı ihlal payı genişliyor (%1 → %8). Bu bir çıkış kuralı fikridir. Uyarı: "stop / erken kesme" COL_OZET'te KAPALI konu; ölçülmez, yalnız kayıt.
5. **Puan basamakları (%1 / 10 / 25 / 50 / 100).** 30 bar içinde ulaşılan en büyük hareketin sınıfları. CLAUDE.md'nin olasılık tablosu biçimine doğrudan çevrilir: P(+%10), P(+%25), P(+%50), P(+%100) olay / eş. Bu çeviri BİLGİ olarak eklenebilir.
6. **Kopukluk toleransı (GAP_TOL = 2).** Kutu içinde 1-2 barlık bozulmayı görmezden gelmek; S5'in "zıplama mumunu görmezden gel" fikrinin barla yazılmış eşi.
7. **Önceki düşüş eğimi (`pslope`).** Kutu öncesi 25 barın kapanış OLS eğimi / ortalama fiyat. "Düşüş sonrası" şartının en basit ölçüsü (kodda hesaplanıp kullanılmamış; niyet yorumda açık).

## 4. MEVCUT KARŞILIK

| Fikir | Modül / kimlik | Durum (ölçüldü mü, sonuç) |
|---|---|---|
| Küçük mum = H−L (fitil dahil) | COL_v1.py satır 137 `MUM_OLCU='aralik'`; HİPOTEZ_ENVANTERİ A3 | Tanım KAPALI (Cemal'in tanımı). BINBN kodu bu tanıma uymuyor. |
| Dipte küçük mumlu sıkışma | SIKISMA_OBEK.py S5_DİP (Ç184; main); kart taslağı KK10 | Ölçüldü (ORTAK_CETVEL v1.0). 20 gün büyük gün KAT: ABD 2023 / 2024-26 GEÇER → EMARE (yönsüz). 60 gün eşli fark: ABD 2023 n 581 +%0,2 [−2,0; +2,1]; ABD 2024-26 n 756 %0,0 [−2,2; +2,7]; AVR 2023 +%0,5, AVR 2024-26 −%0,4 → ÖLÇÜLEMEDİ; olasılık etiketi YOK; ABD P(+%100) kat eş 0,79 / 0,77 (eşten az). S5 eğim −%2..+%10 (15 bar): SD'nin yalnız hafif kısmı içeride, −%2'den dik kutular dışarıda. |
| "Sancılı" kelimesi | SIKISMA_OBEK.py satır 4 (Cemal, 15 Kas): "yükselişteki bölge sancılı değil dinlenme olmalı" | YOL ÜSTÜ sınıfında sancılı = İSTENMEYEN. BINBN kodunda dipte sancılı = OLUMLU. İki ayrı bağlam; ön kayıtta ayrı yazılmalı. |
| Yatay küçük mumlu sıkışma | SIKISMA_CEMAL.py S4 (Ç183; main) | Ölçüldü. ÖLÇÜLEMEDİ (en büyük n 467). YATAY şartı (|net| ≤ %3) SD'yi büyük ölçüde dışlar. |
| Alçalan dipler = güven yok | Cemal kuralları C2, K6, K40 (HİPOTEZ_ENVANTERİ; aktif dal) | SINANMADI. SD'nin "+" iddiasının tersini söylüyor → yön "?" olmalı. |
| Aşağı sürünme (Bollinger alt bandında yürüme) | DUSUS_SONRASI DS20 (aktif dal; DS havuzu 87 hipotez, ölçülen 25) | h5 cetveli: önceden yazılı yön "−"; ABD eğitim n 3246 FARK +1,7, sınama n 2194 +2,4 [+0,3; +4,8] (yön TERS, p 0,98); BIST sınama −3,1. Ç204 CETVEL2 R15: SORGULA (0 / 4). BİLGİ; h5 oynaklığı ödüllendiriyordu (Ç203). |
| Hızlanan düşüş (konvekslik) | DS01 | SD'nin karşıtı (SD yavaşlayan / sürünen düşüş). h5 ÖLÇÜLEMEDİ; Ç204 R15 SORGULA (0 / 4). |
| Düşüş derinliği / Weinstein evre 4 | DS28, DS08 | Ç204 R15: SORGULA (DS28 1 / 4, DS08 0 / 4). SD'nin "öncesinde düşüş" bağlamı. |
| Y1 (S6 taban kırılımı) ∧ küçük mum | KART_TUR1 KT05 (aktif dal) | 2023Q1-Q4 kasa: ÖLÇÜLEMEDİ (KT00 momentum kontrolü cetvelde görünmedi: "cetvel / ufuk yetersiz"); ABD R15 FARK −0,07 [−0,50; +0,24]. |
| Düşen bıçak (dipte yeni dip, son 5 gün ≤ −%3) | KART_TUR1 KT08 (−) | ÖLÇÜLEMEDİ (güç). SD'nin alt sınırsız `dip_yakin`'i dik düşen kutularda KT08 ile örtüşür. |
| Sağ ayak (çöl sonrası yükseliş) | Ç92 (eski tek cetvel) | İZ DEĞİL (güç bilinmiyor; HİPOTEZ_ENVANTERİ sınıf B*). |
| Büyük mum öncesi profil (eğim, küçük mum dizisi) | TERS_PARMAK.py (Ç182; main) | P1 (B1): büyük mumdan önce `kucuk_dizi_40 <= 1` (küçük mum dizisi YOK) ve son mum büyük → PARMAK İZİ VAR (yönsüz). H1 (BH2): dipte ama GENİŞ bant → EMARE. İkisi de "küçük mum dizisi → büyük hareket" önermesinin tersine işaret ediyor; yön ölçüsü değil, bilgi. |
| Ortak 60 gün cetveli + olasılık tablosu | ORTAK_CETVEL.py (main) | SD için BİLGİ ölçüsü olarak hazır (`OC.oc_olc`). |
| Karar cetveli | CETVEL2.py v2.2 (aktif dal) | R15 / R30 KARAR, R45 BİLGİ. Ayrıntı aşağıda. |
| Mühürlü veri | KASA.py (aktif dal) | Mühür 4a7fbad49def764c, kesik 2022-12-31, 16 çeyrek blok (2023Q1-2026Q4); 2023Q1-Q4 KART_TUR1 için açıldı (21 Kas 12:57-13:52 UTC) → açık kesik şimdi 2023-12-31. |
| Açık kalan kayıt | IZ_KARNE.py IK_ACIK (bu dal): "'Çöl Yolu v3, BINBN sancılı düşüş debug' sohbet kaydı repoda / Drive'da yok; metni gelirse ayıklanıp test edilerek entegre edilir." | Metin geldi (bu dosya); ayıklama bu belge, test bölüm 6'daki plan. |

**Sonuç:** 'sancılı / sürünen / grinding / drift / yavaş düşüş' adıyla bir hipotez DS havuzunda (87), KART TUR 1'de (11 kart) ya da HİPOTEZ_ENVANTERİ'nde yok. Kısmen örtüşenler S5_DİP (hafif eğim kısmı), DS20 (aşağı yürüme) ve KT08 (dik düşen kutu).

### CETVEL2'nin karar ölçüsü ve KASA kesiği (dosyadan)

- Giriş E0 = t'den sonraki ilk geçerli bar AÇILIŞI (`OC.oc_olay_hazirla`; t ile giriş arası ≤ 10 takvim günü).
- R_H = H. geçerli barın kapanışı / E0 − 1 (giriş barı 1.); **stop YOK**; 30 (H = 15) takvim satırında H geçerli bar yoksa ölçülmez; kriz kesiği 31.08.2026. v2.2: H = 15 / 30 KARAR, 45 BİLGİ.
- Not: iş tanımındaki "15 geçerli barda +%5 / +%10 hedef stop'tan önce" tanımı ESKİ h5 cetvelidir (YAPI_HEDEF). CETVEL2'de h5 yalnız `bilgi` sütunudur (C2_ESIK['bilgi']['h5']).
- Eş: aynı giriş günü, aynı pazar, aynı kova = ATRP(14) tercili × likidite üçlüsü × F15 (120 gün konumu) çeyreği (36 kova; sınırlar eğitim 2016-22 havuzundan sayı olarak); aynı denemenin o günkü olay hisseleri eşten çıkar; en az 5 eş.
- FARK = R_H − ort R_H(eş); SIRA; ay kümeli boot %95 (B 2000) + L3O; ay kümeli işaret permütasyonu (R 10000); güç (δ = +2 puan, %80).
- Hücre TUTAR: n ≥ 30 VE güç ≥ 0,80 VE FARK > 0 VE boot alt > 0 VE SIRA > 0,50 VE L3O > 0 (yön "−" ise tersi; "?" iki yönden biri).
- Plasebo kapısı: 200 tohum, her olay yerine aynı gün havuzdan rastgele hisse; |ort FARK| < 0,005 VE TUTAR payı ≤ %7; geçmeyen hücre karar vermez.
- Etiket: KATKI+ / KATKI− / SORGULA / ÖLÇÜLEMEDİ / ÇELİŞKİLİ; karar hücreleri ABD ve AVR (BIST bilgi); BH q 0,10.
- %80 güç için gereken n (cetvel2_guc_v2.2.json eğrisinden): R15 ABD açık ~325, AVR açık ~208, BIST açık ~217; R30 ABD açık ~934, AVR ~325.

**SD kartının bağlanması:** olay tablosu [pazar, sembol, tarih = t (kutu sonunun bilindiği gün), F_SD, F_NK1, F_NK2] → `CETVEL2.c2_olc22(olaylar, {'SD': {'bayrak': 'F_SD', 'yon': '?'}, ...}, ufuk=15 / 30)`. F15 kovası SD'nin "dipte" özelliğini eşte zaten dengeler (konum eşli): SD'nin farkı "dipte olmak"tan değil, "dipte küçük mumla aşağı sürünmek"ten gelmek zorunda. Bu doğru K1 kontrolüdür.

## 5. SD TANIMI TASLAĞI (SD_ESIK; sabit, ölçümden önce yazılı)

Bütün ölçüler yalnız geçerli barlardan (O, H, L, C > 0, H > L, V > 0; `OC.oc_panel`) ve yalnız t'ye kadar olan barlardan. Fiyat: `DUSUS_SONRASI.ds_veri` (= `OC.oc_veri`, düzeltilmiş kip, tek kip).

```
SD_ESIK = {
  "surum": "SD v1 (taslak, 21 Kas 2026)",
  "W": 10,                       # kutu penceresi (Cemal: W=10)
  "mum": "medyan_{u-9..u} (H-L)_u / C_{u-1}  <=  0.75 x ATR250%_u   (ATR250% = ort TR/C_önceki, u-249..u)",
                                 # Cemal 0,75 (gövde / global medyan) -> aralık / geçmiş ATR250; birim ve k_m = S5 (a) ile aynı (SO_ESIK secilen k_m 0,75)
  "yukseklik": "(max H - min L)_{u-9..u} / ((max H + min L)/2)  in  [0.02, 0.28]",   # Cemal'in bandı aynen
  "maske_gunu": "mum VE yukseklik (u gününde)",
  "kutu": "maske günlerinin dizisi; en çok 2 ardışık maske-dışı bar tolere (GAP_TOL 2); bas = ilk maske günü - 9; son = son maske günü",
  "uzunluk": "kutudaki maske günü >= 5  (kutu boyu >= 14 bar)",
  "egim": "sl = (C_son - C_{son-9}) / (orta_son x 10)  <  -0.0003",                   # Cemal'in eşiği; alt sınır YOK (ANA)
  "dip": "dip_yakin = (C_bas - min L_{bas-30..bas-1}) / min L  <  0.35",               # Cemal'in eşiği aynen
  "onceki_dusus": "pslope = OLS eğimi(C_{bas-25..bas-1}) / ort(C_{bas-25..bas-1})  <  0", # Cemal'in yorumdaki niyeti (kodda eksik)
  "sinyal_gunu": "t = son + 3 (üçüncü ardışık maske-dışı bar: kutu sonunun gerçek zamanda bilindiği gün); kutu t'de kapanmamışsa olay yok",
  "giris": "t+1 açılışı (CETVEL2 E0)",
  "tekil": "aynı hissede olaylar >= H işlem günü arayla (CETVEL2 tekil_gun = ufuk)",
  "birlestirme": "YOK (kutu bitişi bir kez, t'de; sonraki kutu yeni olaydır, tekil kuralına tabi)",
  "yon": "?",                    # BINBN kodu '+' der; Cemal'in C2 / K6 / K40 kuralları '-' der -> iki yönlü
  "kontroller": {
    "NK1_dip_degil": "aynı kutu, aynı egim ve onceki_dusus, ama dip_yakin >= 0.35",
    "NK2_egim_pozitif": "aynı kutu, dip ve onceki_dusus, ama sl >= +0.0003",
    "KUTU": "aynı kutu kuralı, tip şartı yok (bütün kutu bitişleri)  -> SD'nin kutu genelinden farkı BİLGİ",
    "KT00": "12-1 momentum üst onda (KART_TUR1 KT00 tanımı aynen): cetvelin bilinen etkiyi gördüğünün sınaması"
  },
  "varyant_BILGI": {
    "SD_HAFIF": "SD VE sl >= -0.005 (10 barda yaklaşık -%5'ten yumuşak)",
    "SD_SAVUNMALI": "SD VE min L_{bas..son} >= min L_{bas-30..bas-1} x 0.98 (kutu yeni dip yapmıyor; Cemal C2)",
    "SD_GOVDE": "Cemal'in özgün gövde ölçüsü, ama gm yerine geçmiş 250 gün gövde medyanı (yalnız eşleme için)"
  }
}
```

Notlar:
- Cemal'in sayıları (0,75; %2-28; −0,0003; 0,35; 25 bar) aynen alındı. Tek değişiklikler kusur düzeltmesi: gövde → aralık (Cemal'in kendi tanımı), global medyan → geçmiş ATR250 (geleceğe bakma), giriş kutu sonu kapanışı → t+1 açılış (t = kutu sonu + 3), `pslope < 0` tip şartına eklendi (Cemal'in yorumdaki niyeti), birleştirme kaldırıldı (geleceğe bakma).
- Eşikler bu taslakta sabittir; ön kayıttan sonra değişmez. SD_HAFIF'teki −0,005 ve SD_SAVUNMALI'daki 0,98 yeni sayıdır; bu yüzden yalnız BİLGİ, kararda kullanılmaz.
- Prefix testi (K2): her pazarda rastgele ≥ 8 olay için F_SD, veri t'de kesilerek yeniden hesaplanır; bütün veriyle aynı çıkmazsa ölçüm durur (KART_TUR1 prefix kuralı).

## 6. ÖLÇÜM PLANI

**Modül.** Yeni tek dosya (öneri: `SANCILI_DUSUS.py`, çakışma kapısı `_CK_ONCE_SD`, `col.sancili_dusus` logu, SDHata). Bayrakları kendisi hesaplar; ölçümü içe aldığı `CETVEL2.c2_olc22` (karar) ve `ORTAK_CETVEL.oc_olc` (bilgi) yapar. Neden yeni dosya: KART_TUR1.py ve SIKISMA_OBEK.py sha'ları ön kayıtlarda mühürlü (KASA_KOD / so_esik_sha); kart eklemek mühürü bozar. SIKISMA_OBEK'e sınıf eklemek de uygun değil: onun sonucu yönsüz büyük hareket (B1 / BH2); SD yön iddiasıdır.
Dal: CETVEL2, KASA, KART_TUR1, DUSUS_SONRASI yalnız `ccr-27195a1e-djv6v3` dalında. İş o dalda yapılmalı.

**Veri ve kesik.**
- Keşif / eğitim (KARAR hücresi 'acik'): `/tmp/kasa/acik` V_ABD, V_AVR, V_BIST; giriş 2016-01-01..2022-12-31. `/tmp/kasa/acik` artık 2023'ü de içeriyor (blok 1-4 açık); ölçüm 'acik' hücresine giriş tarihiyle süzülür ve `KASA.kasa_kapisi` açık kesik (2023-12-31) denetimi çağrılır.
- 2023 (blok 1-4): KART_TUR1 için 21 Kas 12:57 UTC'de açıldı. SD ön kaydı bu saatten sonra işleneceği için `KASA.ac` kuralı gereği SD için KÖR DEĞİL. 2023 hücresi yalnız BİLGİ.
- Kör ileri test: SD ön kaydı işlendikten sonra `python KASA.py ac --blok 2024Q1 --hipotez SD1 --onkayit <yol>` ile 2024Q1'den sırayla. KARAR BAKIŞI 4. SD bloğunda (2024Q1-Q4 birikimli) ve 8. blokta (2024Q1-2025Q4); arada tablolar BİLGİ. Fon krizi kesiği 31.08.2026 (2026Q3 sonrası ölçülmez).
- BIST bilgi (CLAUDE.md karar hücreleri ABD + AVR). BINBN BIST hissesi olduğu için BIST sonucu ayrıca yazılır ama karar vermez.

**Ölçüler.**
1. KARAR: CETVEL2 v2.2 R15 ve R30 (yukarıdaki tanım), hipotez SD yön "?"; BH m = 2 (SD × R15 / R30). NK1, NK2, KUTU ve varyantlar BİLGİ (BH dışı).
2. KT00 momentum kontrolü aynı koşuda: KT00 cetvelde görünmezse SD etiketi "ÖLÇÜLEMEDİ (cetvel / ufuk yetersiz)" (KART_TUR1 kuralı aynen). Not: 2023 kasada KT00 GÖRMEDİ; açık 2016-22'de görmesi beklenir (bilinmiyor, ölçülecek).
3. BİLGİ: `OC.oc_olc` 60 gün eşli fark + olasılık tablosu (250 gün +%100 / −%50 dokunma, eş katı); CLAUDE.md'nin istediği olasılık tablosu buradan.
4. BİLGİ: Cemal'in düzeltilmiş sağ ayak etiketi: giriş E0; 30 geçerli barda (a) kutu altının %1 altında 2 ardışık kapanış = İHLAL, (b) E0'ın +%10 üstünde 2 ardışık kapanış = TUTUNMA; sıra: hangisi önce. Olay payı / eş payı (aynı kova eşlerine aynı kural, eşin kutu altı yerine E0 × (kutu altı / olay E0) uzaklığı). Dinamik tolerans ölçülmez (kapalı konu: stop).
5. BİLGİ: puan basamakları → P(30 barda +%10 / +%25 / +%50 / +%100 kapanış) olay / eş.

**Eş ve plasebo.** CETVEL2 konum eşi (aynı gün, pazar, ATRP tercil × likidite üçlüsü × F15 çeyreği; ≥ 5 eş; o günkü SD olayları eşten çıkar) + 200 tohum plasebo kapısı. Ek BİLGİ eşi: aynı gün aynı kovada KUTU durumunda olan ama SD olmayan hisseler (SD'nin kutu genelinden farkı).

**Beklenen n (tahmin, ölçülmedi).** S5_DİP (daha sıkı: bant %6-8, BB şartı) ABD 2016-22'de 1.432 bölge verdi; SD bandı geniş (%2-28) ama eğim, dip ve önceki düşüş şartı ekliyor. Kabaca ABD açık 1.000-6.000, AVR açık 400-2.000, BIST açık 300-1.500 olay; R15 için gereken ~325 / ~208 aşılır, R30 ABD için ~934 sınırda olabilir. Kör blok başına (çeyrek) ABD 40-250 olay: KARAR BAKIŞI 4 blokta güç sınırda, 8 blokta daha iyi. Gerçek sayı ön kayıttan önce getirisiz prefix / huni sayımıyla yazılır; sayım güç eşiğinin altındaysa ön kayıtta "ÖLÇÜLEMEDİ beklenir" diye yazılır, eşik değiştirilmez.

**Ön kayıt metni taslağı (SD_ON_KAYIT.md).**

```
# SD1 — SANCILI DÜŞÜŞ ÖN KAYDI (taslak)
KASA_HIPOTEZ: SD1
KASA_KOD: SANCILI_DUSUS.py <sha256>
KASA_KOD: CETVEL2.py <sha256 (v2.2, KART_TUR1 ön kaydıyla aynı olmalı: 2c0fd9b9968515f1...)>
Soru: Düşüş sonrası dipte, küçük mumla (H-L) hafif aşağı sürünen 10+ barlık kutunun bitişinden sonra 15 / 30 barda getiri, aynı gün aynı
ATRP x likidite x 120 gün konumu kovasındaki hisselerden farklı mı? Yön önceden yazılmadı ('?'): BINBN kodu '+', Cemal C2 / K6 / K40 '-'.
Tanım: SD_ESIK (tam metin + sha). Karar: CETVEL2 v2.2 R15, R30; hücreler ABD acik, AVR acik (+ kör bloklar 2024Q1-Q4 bakış 1,
2024Q1-2025Q4 bakış 2); BIST, 2023 (kör değil), NK1, NK2, KUTU, SD_HAFIF, SD_SAVUNMALI, OC r60 + olasılık tablosu, sağ ayak etiketi BİLGİ.
Etiket: C2_ESIK etiket kuralı aynen; KT00 görmezse ÖLÇÜLEMEDİ (cetvel). BH q 0,10, m = 2.
Getirisiz sayım (huni): <pazar x hücre olay sayısı, ön kayıttan önce>. Güç: cetvel2_guc_v2.2.json (sha).
Prefix: pazar başına 8 olay, tam eşitlik şartı.
Yeniden üretim (önceden seçildi): SD ABD acik R15 ve SD AVR acik R30, satır dosyasından düz pandas ile n / ort FARK / ort SIRA.
```

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 c2_olc22 konum eşi: aynı giriş günü, pazar, ATRP tercil x likidite üçlüsü x F15 çeyreği, en az 5 eş, deneme olayları eşten çıkar; 200 tohum plasebo (C2_ESIK plasebo); mekanik üstünlük: F15 kovası 'dipte olmayı' dengeler, stop / hedef yok; NK1, NK2, KUTU eşi bilgi; KT00 aynı koşuda |
| K2 | geleceğe bakma | EVET | SD bayrağı yalnız u <= t barlarından; t = kutu sonu + 3 (kutu bitişinin bilindiği gün); ATR250 u-249..u; birleştirme yok; global medyan yok; prefix testi pazar başına 8 olay, tam eşitlik yoksa DURUR; KASA.kasa_kapisi açık kesik 2023-12-31 |
| K3 | geçerli bar | EVET | OC.oc_panel geçerli bar (O/H/L/C > 0, H > L, V > 0); kilitli ve hacimsiz bar maske / ATR / eğim hesabına girmez; giriş günü havuzda |
| K4 | tekilleştirme | EVET | aynı hissede olay >= H işlem günü arayla (CETVEL2 tekil_gun = ufuk); kutu başına tek olay (t); hücrede ortalama + medyan FARK |
| K5 | giriş fiyatı | EVET | E0 = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); kutu sonu kapanışı KULLANILMAZ |
| K6 | veri birimi | EVET | tek kip: DUSUS_SONRASI.ds_veri (OC.oc_veri, düzeltilmiş, açılış H-L kırpması); AVR likidite Kur sütunuyla EUR; geçmiş bölünme şüphesi olan bar havuz dışı (OC) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, k34 yüklenmez); batan yok; SD dipte bir kart olduğu için sonuç yukarı yanlı okunur, raporda yazılı |
| K8 | örneklem ve dönem | EVET | karar ABD + AVR açık (2016-22) ve kör 2024Q1+ ; n < 30 ya da güç < 0,80 ÖLÇÜLEMEDİ; BH q 0,10 m 2; tek pazar / tek dönem sonucu EMARE / ADAY'dan öteye çıkmaz |
| K9 | ön kayıt | EVET | SD_ESIK + SANCILI_DUSUS.py + CETVEL2.py sha ön kayıtta; ön kayıt commit zamanı < koşu ve < KASA ac; KASA_HIPOTEZ / KASA_KOD satırları; eşik sonuçtan sonra değişmez |
| K10 | ayrıştırma | UYGULANMAZ | haber / metin ayrıştırma yok; yalnız fiyat-hacim pkl (islenmis-veri, KASA açık kısmı); BINBN CSV'si kullanılmaz |
| K11 | yeniden üretim | EVET | sd_olay.csv.gz satır dosyası; SD ABD acik R15 ve SD AVR acik R30 düz pandas ile yeniden; fark > 1e-12 DURUR |
| K12 | ifade | EVET | FARK = fiyat değişimi farkı, kâr değil; 'iz / emare' yalnız C2 etiket kuralı geçince; sayı ve yorum ayrı cümlede; DOGRU / puan kelimesi raporda kullanılmaz (sağ ayak etiketi = TUTUNMA / İHLAL payı) |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_SD; logging; tam hata yakalama (SDHata); 'çalışma zamanını yeniden başlat' notu; e-posta / anahtar taraması; defter dosyalarına dokunulmaz; KASA gizli anahtarı yalnız ana model |
| K14 | boyut (gerçek para) | UYGULANMAZ | ölçüm işi, öneri yok; sonuç öneri modülüne giderse kapı (c) ayrıca yazılır |

**Karar sonrası ne söylenir.** KATKI+ (dört karar hücresi yukarı tutar, BH geçer) → SD "aday"; KATKI− → Cemal'in C2 kuralı lehine; SORGULA / ÖLÇÜLEMEDİ → iddia kapanmaz, IK_ILERI'ye kör blok tarihleriyle girer.

## 7. ÖNERİLEN DEFTER METNİ (ana model işler; bu dosyalara dokunulmadı)

- **IK_ACIK (değiştir):** "BINBN sancılı düşüş kodu geldi (arastirma_cikti/sancili_dusus/BINBN_v4_final_colab.py, 21 Kas). Eleştiri ve eşleme: SD_ELESTIRI_VE_ESLEME.md (30 kusur; SD projede ayrı sınanmamış; en yakın S5_DİP 60 gün ÖLÇÜLEMEDİ, DS20 R15 SORGULA). Sıradaki: SD1 ön kaydı + SANCILI_DUSUS.py (CETVEL2 v2.2 R15 / R30, yön '?', KASA 2024Q1'den kör)."
- **IK_KAYIT Ç taslağı (aktif dalda sıradaki numara; o dalın son kaydı Ç205):** "SANCILI DÜŞÜŞ (Cemal'in BINBN v4 Colab kodu): eleştiri + eşleme, ölçüm yok. Kod: kutu (10 bar, gövde < 0,75 x global medyan, yükseklik %2-28) + tip (SD: eğim < −0,0003 ve dipten < %35) + sağ ayak (29 bar, 2 kapanış ihlal / +%10 tutunma). 30 kusur (geleceğe bakma 4, gövde ölçüsü, pslope kullanılmıyor, N doğrusu yukarı, BASARISIZ sonraki kutuya bağlı). Karşılık: S5_DİP (Ç184) 60 gün ABD %0,0..+0,2 ÖLÇÜLEMEDİ; DS20 R15 SORGULA; KT05 / KT08 ÖLÇÜLEMEDİ. Karar: SD ölçülmedi; tanım SD_ESIK taslağı. Durum: ÖLÇÜLMEDİ (plan)."
- **IK_HATA önerileri (her biri ayrı satır):**
  1. 2026-11-21 | BINBN_v4_final_colab.py satır 64-68, 147 | kutu sonu 3 bar sonra bilinir, giriş kutu sonu kapanışı | geleceğe bakma | Claude (SD eleştirisi) | BINBN DOGRU / puan etiketleri iyimser | giriş t = son + 3, E0 = t+1 açılış (SD_ESIK) | kutu / bölge bitişi tanımında 'ne zaman bilinir' ayrı yazılır.
  2. aynı dosya satır 23 | küçük mum paydası bütün serinin medyanı | geleceğe bakma | ... | ATR250 geçmiş pencere.
  3. aynı dosya satır 22, 27 | küçük mum gövdeyle (|C−O|), Cemal'in tanımı H−L | ölçüt | ... | aralık ölçüsü.
  4. aynı dosya satır 81, 88-91 | 'önceki düşüş' şartı hesaplanıyor ama kullanılmıyor | yanlış yorum | ... | pslope < 0 tip şartına eklendi.
  5. aynı dosya satır 182, 195 | N tipinin DOGRU'su yukarı +%10 istiyor | hesap | ... | yönlü tanım.
  6. aynı dosya satır 196-204 | BASARISIZ sonraki kutunun varlığına bağlı | geleceğe bakma | ... | pencere dolumu.
  7. aynı dosya satır 135-141, 153-188 | dinamik tolerans kazananı korur; hedef-stop sırası bakılmıyor | ölçüt (mekanik üstünlük) | ... | CETVEL2 stop'suz R_H + sıralı bilgi etiketi.
  8. iş tanımı (bu görev) | "R15 = +%5 / +%10 hedef stop'tan önce" yazılmış; CETVEL2 R15 stop'suz getiri, h5 yalnız bilgi | iletişim | Claude (alt ajan) | yok (dosyadan düzeltildi) | ön kayıtta C2_ESIK metni kopyalanır.

## HATA

1. **Geleceğe bakma (kod, satır 64-68 + 147):** kutu sonu `end+3`'te bilinir, giriş `C[end]`; sonuç penceresi bilinmeyen 3 barı içerir.
2. **Geleceğe bakma (kod, satır 23):** `gm` bütün serinin gövde medyanı; küçük mum eşiği gelecekteki oynaklığa göre.
3. **Geleceğe bakma (kod, satır 108-122):** kutu birleşmesi ve birleşmiş `ei` sonraki kutunun gelip gelmemesine bağlı.
4. **Geleceğe bakma (kod, satır 196-204):** BASARISIZ / BEKLE ayrımı sonraki kutunun varlığına bağlı, pencere dolumuna değil.
5. **Ölçüt (kod, satır 22 / 27):** küçük mum gövdeyle ölçülüyor; Cemal'in tanımı H−L (COL_v1 `MUM_OLCU='aralik'`).
6. **Tanım (kod, satır 81 / 88-91):** `pslope` (önceki düşüş) hesaplanıyor ama SD kararına girmiyor; yorumla kod çelişiyor. Lookback 20 / 25 / 30 üç yerde farklı.
7. **Tanım (kod, satır 77 / 90):** `dip_yakin` alt sınırsız ve kutunun alt bandı yerine ilk kapanıştan; yeni dip yapan kutu da SD.
8. **Tanım (kod, satır 89 / 101):** SD eşiği (−0,0003) ile eğim oku eşiği (0,0005) farklı; grafikte "→" görünen kutu SD olabiliyor; eğim alt sınırı yok.
9. **Hesap (kod, satır 70):** `end−start<5` hiç çalışmaz (`end−start ≥ 9` her zaman); ölü kod.
10. **Hesap (kod, satır 119):** birleşmede SD tipi P'ye dönebiliyor ya da kayboluyor; `n`, `pslope`, `dip_yakin`, `ed_price` güncellenmiyor.
11. **Hesap (kod, satır 182):** tutunma tipten bağımsız yukarı +%10; N tipinin DOGRU tanımı yanlış.
12. **Hesap (kod, satır 153):** pencere 29 bar (yorum 30).
13. **Mekanik üstünlük (kod, satır 135-141):** ihlal toleransı kazanca göre genişliyor; etiket kazananı kendiliğinden korur. Hedefin stop'tan önce gelip gelmediğine bakılmıyor (iki ayrı döngü).
14. **Geçerli bar (kod, satır 17-22):** H>L, V>0 denetimi yok; kilitli / bayat bar gövde 0 ile en küçük mum sayılır.
15. **Veri birimi / ayrıştırma (kod, satır 13, 18-19):** Close + Adj Close aynı ada eşleniyor (çift sütun ya da kip karışıklığı); "," silme Türkçe ondalık virgülde 100 kat hata verir. BINBN CSV'si repoda yok, doğrulanamadı.
16. **Örneklem / ön kayıt (kod bütünü):** tek hisse, eşik "v4 final" aynı grafikte ayıklanmış; kontrol grubu, plasebo, satır dosyası yok; DOGRU / puan dili K12'ye aykırı.
17. **Süreç (kod, satır 3-293):** çakışma kapısı yok, çıplak `except:` (289), log yok, sabit çıktı adı.
18. **İş tanımı:** R15 "+%5 / +%10 hedef stop'tan önce" diye tarif edilmiş; CETVEL2'de R15 stop'suz getiri (C2_ESIK['r15']), h5 yalnız BİLGİ. Rapor dosyadaki tanımı esas aldı.
19. **İş tanımı / KASA:** "açık kesik 2022-12-31 ya da 2025-12-31" — manifestte mühür kesiği 2022-12-31; 2025-12-31 yalnız KASA_RAPOR'daki kuru sayım örneği; 2023Q1-Q4 açıldığı için güncel açık kesik 2023-12-31. Bu açılış SD'den önce olduğu için 2023, SD için kör değil.
20. **Defter dalları ayrışmış:** bu dalın (ccr-e5e013aa-eqeyj8) IZ_KARNE.py'sinde Ç190-Ç205 yok (aktif dal ccr-27195a1e-djv6v3'te var). SD kaydı yanlış dala yazılırsa Ç numarası çakışır; ana model kaydı aktif dalda (sıradaki Ç206) yazmalı.
21. **Kavram çelişkisi:** "sancılı" SIKISMA_OBEK'te (YOL ÜSTÜ) istenmeyen durum, BINBN kodunda (dip) olumlu tip; Cemal'in C2 / K6 / K40 kuralları da SD'nin "+" yönüne ters. Ön kayıtta yön "?" yazılmazsa sonuç sonradan yorumlanır.
