# ÇÖL YOLU SİSTEMİ — TAM ÖZET (2026-09-18)

Bu dosya bir yıllık çalışmanın tamamıdır: kurallar, dosyalar, her test ve sonucu.
Yeni bir sohbete başlarken en alttaki "KISA BLOK"u yapıştırmak yeterli.

---

## 1. SİSTEM — GÜNCEL KURALLAR

**Evren:** BIST 583 hisse günlük (`veri_1d_turkey.pkl`), ABD 1274 (`veri_1d_america.pkl`), 4h 519.

**Segment (çöl):** `col_segment()` — sıkışma bölgesi. Belirleyici parametre `yerel=5`
(fiyat son 5 barın dibini kırmadan geçen süre). `min_cekirdek/esik/tolerans/band_tol`
etkisiz (test edildi). Şart: ≥20 bar, ≤6 ATR. Tavan = segmentteki en yüksek gövde üstü.
**18 Eylül göz kalibrasyonu (bölüm 7): bu tanım Cemal'in çöllerinin yarısını kaçırıyor; v3 karar bekliyor.**

**Aday:** geçerli segmenti olan her hisse. Üç şart (clv ≥−0.164, bant_son ≥0.509,
ortaust ≥0.40) artık ADAY FİLTRESİ DEĞİL — ağırlık (geçmeyen 0.7x). Taban kırılması
listeden düşürmez; 60 bar içinde kırmayan düşer.

**Giriş:** kapanış > tavan × 1.002 → o kapanıştan AL. Teyit yok, bekleme yok.

**Çıkış:** %20 hedefe dokununca TRAIL (kapanış < SMA20 → SAT). Hedefe ulaşmayan
120. barda SAT. Trail'deki pozisyona ufuk uygulanmaz. STOP YOK.

**Pozisyon boyutu:** %6 × CDS × borç × doji × fitil × dar × kural, üst sınır %12
- CDS pct250: <0.3 → 0.5 | 0.3-0.6 → 1.0 | ≥0.6 → 1.5  (Türkiye riski yüksekken iyi)
- net borç/özsermaye: <0 → 1.5 | 0-0.3 → 1.0 | >0.3 → 0.7  (temel_duz.csv, çeyreklik)
- doji oranı (segmentte |C-O|/(H-L)<0.15): ≥0.23 → 1.5 | <0.13 → 0.7
- alt fitil ort (ATR): <0.12 → 2.5  (4 sette doğrulandı, en güçlü)
- dar hafta (haftalık aralık <0.7 haftalık ATR oranı): ≥0.47 → 1.3 | <0.30 → 0.8
- kural (üç şart): geçer 1.0 | geçmez 0.7

**Doğrulanmış sonuçlar (kırılımda gir, trail):**
| set | kazanan | işlem başı | ağır kayıp |
| BIST 2024-26 (n≈2400-2950) | %73-79 | +13.5..+14.7 | %13 |
| BIST 2023 (n≈540-1066) | %90 | +38..+40 | %4 |
| ABD 2024-26 (n≈2100-3100) | %80 | +11 | — |
Slot simülasyonu (30 slot, sabit sermaye): 2024-26 +109, 2023 +108 portföy.
CDS×BORÇ×DOJİ ağırlık: +3.9 / +6.9 puan (eşit ağırlığa göre).
Çöl şartı vs düz 20-bar Donchian kırılımı: +1.2/+6.9 puan, kazanan +3/+5. Çöl gerçek ama küçük katkı.

---

## 2. DOSYALAR (`/content/drive/MyDrive/col_tarayici/`)

| dosya | iş |
|---|---|
| `BASLAT.py` | tek başlatıcı: veri yenile, tüm modülleri yükle, d/d23/OB24/OB23/OBUS/t |
| `col_atilim_TEK.py` | temel altyapı (hizli_baslat, veri indirme) |
| `COL_v1.py` | col_segment, col_olc, çarpanlar, cds_rejim |
| `takip.py` | `gun()` günlük takip, adaylar/pozisyonlar/kapanan CSV |
| `temel.py` | İş Yatırım finansalları → borç/öz |
| `fon_takip.py` | fonoloji.com API, aylık fon portföyü |
| `onbellek.py` | `onbellek_kur()`, `onbellek_guncelle()` — test önbelleği |
| `DENETIM.py` | tekil/ertesi açılış işlem tablosu, portföy (drawdown), XU100/mevduat kıyası, ayı dönemi |
| `KALIBRE.py` | segment v3 (göz kalibrasyonu), `kalibre()` eski/v3 P&L kıyası, `v3_uygula/v3_kalici/v3_geri` |
| `kalibre_veri.csv`, `kalibre_etiketler.csv`, `kalibre_veri_ek.py` | gözle işaretli çöl/olumsuz seti ve verisi |
| `veri_1d_turkey.pkl` | BIST OHLCV, `veri_yenile` aynı dosyaya yazar |
| `onbellek_2024_26.pkl`, `onbellek_2023.pkl`, `onbellek_ABD.pkl` | test: sinyal + segment + 300 bar ileri |
| `v1_final_BIST.csv`(d), `yeni_BIST_2023.csv`(d23), `yeni_ABD.csv` | sinyal tabloları |
| `cds_2022.csv`, `temel_duz.csv`, `fon_holdings.csv` | dış veri |
| `takip_*.csv` | canlı takip (07 Eylül 2026'dan beri, kâğıt) |
| `arsiv/` | 50+ test scripti, eski sürümler (`*_eski_20260918*`) |

**Günlük:** `exec(open('/content/drive/MyDrive/col_tarayici/BASLAT.py').read()); A,P,Kp=gun()` — 19:30 sonrası.
**Aylık:** `H,yeni=fon_guncelle()` (ayın ortası). Çeyreklik: bilanço xlsx yenile → `temel_duz.csv` sil.
**Kural:** dosyaları Colab'dan yerinde yaz (`open(...,'w')`), Drive API ile yeni kopya oluşturma (çift dosya sorunu yaşandı). Test için `OB24/OB23/OBUS` + `pnl_ob/kirilim_bul/bek` kullan — 30 sn.

---

## 3. TEST EDİLDİ VE KAPANDI

**Giriş noktası / zamanlaması** — hiçbiri kırılımda girmeyi geçmedi:
- Tavan tanımı (9: gövde max, high max, kapanış max, son yarı, son 10, %90, +0.3/0.7/1.0 ATR tampon): fark yok; tampon kötü. Zıpla-düş oranı her tanımda ~%27 (yapısal).
- Teyit (k bar bekle), retest, gecikmeli giriş: kötü. Koşanı bekle (bar 3-8, +1.5-2 ATR): yarılar 2-2, rejime bağlı, alınmadı.
- Kırılım hacmi (3 test, 3 piyasa), kırılım şiddeti (z1/z3, drift burst), gap: fark yok.
- İlk 8 bar: <−5% → %58/+3.3/ağır %25; >+5% → %90/+26.7. Basamak −0.5 ATR. Açıklayıcı ama işlem kuralı değil (yastık etkisi; 8. barda girmek %74).

**Aday filtreleri** — her filtre para kaybettirdi:
- E_ONC (250 gün düşüş) filtresi: 2023'te 550→13 sinyal. Kaldırıldı.
- Üç şart aday kapısı: slot portföy +53 → +109 kaldırınca. Ağırlığa döndü.
- Taban kırılması düşürme: düşüp-kıranlar aynı kâr; kaldırınca toplam +21/+36%.
- Doji-tolerans (kuralı kıl payı kaçıran sessiz çöl): n=21, karar yok.

**Çıkış** — trail SMA20 her varyantı yendi:
- Fiyat stopu (5-30%), felaket sınırı (25-40): hepsi kötü (BIST taban serisi, dipte satış).
- Zaman stopu / ufuk 60-250: portföy nötr; 120 seçildi (6 ay). Trail muaf.
- 8. bar <−5% kes: nötr (−14/+10). + tekrar gir: kötü. + yüklen: ek lot sıradan işlem.
- Doji çıkış, taban kırılınca çık, şartlar bozulunca çık: kötü. Trail zemin (giriş altında satma): test bekliyor.
- Desen sat (ISSEN 2-mum, kümeli 3-8 mum): 3 piyasa, 8 varyant, tut > çık. Desen sonrası 10 bar yazı-tura.
- Şelale (5 pivot, genişleyen tepe + cüce): şelale oranı %25-32 vs taban %26; sinyal zamanında %18-20.
- SMA200 direnç: dokunanların %82-96'sı geçiyor; mesafe fark etmiyor.

**Segment / şekil** — 90+ ölçü:
- Segment motorları (6: PELT, v2, v3, gd, BB, ATR): hepsi eşit.
- Uzunluk, yükseklik (ATR), gövde, BB, NR7, TTM, asimetri, incelik, zikzak, sivri: fark yok. Yükseklik yüzde: en geniş %20 biraz kötü, kuraldan sonra sıfır.
- Pürüz / eğri hata: küçük (+0.5/+1.7), eğri çarpanı bir ara girdi, kod yenilenince düştü.
- Alt iğne yokluğu: GÜÇLÜ (BIST 24-26 +32 vs +13, 2023 +54 vs +38, ABD +18 vs +9). Sistemde.
- Doji oranı (günlük, segment tamamı): monoton (+11.8→+17.4, +29→+51). Sistemde.
- Haftalık doji: tutarsız. Haftalık dar mum oranı: tutarlı küçük. Sistemde.
- Dip sabitliği, alt iğne azalışı, üst iğne: tutarsız.
- Akümülasyon (net_alim, kurum_oran, OBV, CVD): trail ile fark yok.
- 12 elle işaretli çöl (Cemal): kod 9 doğru, 3 sınırda, 0 gerçek kaçırma. Segment sağlam. **(18 Eylül: 29 çöllük geniş sette bu sonuç tutmadı, bkz. bölüm 7.)**

**Rejim / dış veri:**
- CDS: 2 dönemde +2.8/+3.7 → çarpan. EEM: ikinci ışık. TR2Y: CDS'i geçmiyor.
- VIX, DXY, USDTRY, Brent, US10Y, TRY vol: tutarsız.
- Endeks günü, küme günü, XU100 ilk hafta: sinyal sonucunu etkilemiyor.
- Temel: borç/öz güçlü (sistemde). ROE karışık. Kâr/satış büyümesi düz.
- Fon (fonoloji API, 24 fon, 11 ay): fon İLK KEZ girdi → 3 ay +11.9 vs −1.3 (n=90, tek dönem) — izleme listesi. Ağırlık artış/azalış anlamsız. Düşüşte ısrarla topladı n=8. Yoğunlaşma (tek hissede %10+) = yapı riski (TERA/Pusula 17 Eylül).
- Takas verisi: ücretli, T+2. Haber duygu: veri yok.

**Diğer zaman dilimleri / ML:**
- 4h sistem: +5-7/işlem, 24-29 gün, yıl 1 +53 / yıl 2 +104 teorik; kural 4h'de az ekliyor. İkinci sistem adayı, kâğıt.
- Haftalık: 2019-22 çok iyi (2x+ %42), 2024+ negatif. Rejime bağlı.
- KNN (5 ölçü): yön %87 vs kural %84, ama trail kârı düşük (+3.1 vs +6.3). ML kâr eklemedi.

---

## 4. DERSLER

1. Kırılım öncesi her eleme para kaybettirdi. Kırılım tek filtre; öncesi ağırlık.
2. Giriş noktasında avantaj yok. Kazanç: sinyal sayısı × boyut × trail.
3. BIST'te stop çalışmaz (taban serisi). Koruma = pozisyon boyutu (%3-6, üst %12).
4. Hafıza kayıpları saklar: her düşüşün önünde desen var, her desenin önünde düşüş yok. BIST'te 30 barda %15 düşüş taban ihtimali %26.
5. Sonuçtan geriye bakmak (40/40, en iyi/en kötü listesi) yanıltır; tertile + sabit eşik + 2 dönem + ABD + slot sim + taban oran 1.3x standart.
6. Parametre etkisi ölçülmeden "kalibre" denmez (min_cekirdek olayı).
7. Kişisel kayıplar (PAPIL, QMLS, TERA) sinyalden değil boyuttan ve yapı riskinden.
8. Test altyapısı ilk gün kurulmalıydı (önbellek): 15 dk → 30 sn.
9. **Gözle işaretli set (29 çöl + 8 olumsuz) kodun doğruluğunu ölçmenin tek yolu; şekil ölçüleri olumsuzu ayırmaz, ayıran kırılım + trail.**

---

## 5. AÇIK / BEKLEYEN
- **`kalibre()` P&L kararı (bölüm 7) → `v3_kalici()` veya reddet.**
- `denetim(OB24, OB23, OBUS, xu)` ile düzeltilmiş rakamlar (bölüm 6).
- Trail zemin testi (hedef vurmuş pozisyon girişin altında satılmasın).
- Fon "ilk giriş" sinyali 2. dönemde doğrulama (veri biriktikçe).
- Yapı riski bayrağı (fon yoğunlaşması ≥%10 → 0.5x) — muhakeme kuralı, eklenmedi.
- 4h sistemi kâğıtta izleme.
- Canlı kayıt: 07 Eylül 2026'dan beri kâğıt; 6 ay sonra ileriye dönük performans.
- Dar hafta çarpanı: `denetim()` çıktısında iki dönemde fark yoksa 1.0'a çek.

**Durum (18 Eylül 2026):** Sistem tamamlanmış ve dondurulmuş. Cemal sermayesiz; tahvile geçiş kararı. Sistem kâğıtta çalışır, sermaye/faiz ortamı değişince açılır.

---

## 6. DENETİM VE DÜZELTMELER (18 Eylül 2026)

Bir yıllık kod baştan sona denetlendi; 12 sorun bulundu, hepsi düzeltildi. Eski dosyalar `arsiv/*_eski_20260918.py`.

**Kodda kesin hatalar (düzeltildi):**
1. Dar hafta çarpanı özette vardı, kodda yoktu → `dar_hafta_olc()` eklendi (segmentteki haftaların aralığı < 0.7×haftalık ATR olanlarının oranı; ≥0.47→1.3, <0.30→0.8). **Not:** bu tanım özetteki cümleden yeniden yazıldı; eski test scripti arşivde bulunamadı. OB24/OB23'te `denetim()` çıktısındaki "dar>=0.47" satırıyla doğrulanmalı; iki dönemde de fark yoksa çarpan 1.0'a çekilmeli.
2. Negatif özkaynak → `borc_oz` eksi çıkıp 1.5x alıyordu → `oz_negatif` sütunu, çarpan 0.7. `temel_duz.csv` eski formatsa BASLAT yeniden hesaplar.
3. Doji/fitil canlıda kırılım günü yeniden hesaplanıyordu → sinyal günü ölçüleri aday CSV'ye yazılır, boyut oradan.
4. H=L / hacim=0 barlar doji sayılıyor, fitil 0 çıkıyordu → sadece geçerli barlar (H>L, V>0); `gecerli_oran` <0.90 ise doji/fitil nötr + 0.5x.

**Sonucu şişirenler (ölçülebilir hale geldi — `DENETIM.py`):**
5. Giriş kırılım kapanışı ama dolum ertesi açılış → `islemler(OB, giris='acilis')`.
6. 2 haftalık örnekleme aynı kırılımı 4-5 kez sayıyordu → (sembol, kırılım tarihi) tekilleştirme. **Eski n değerleri (2400/540/2100) bağımsız işlem sayısı değil.**
7. `veri_yenile` auto_adjust=True ile ekliyordu, ana veri False ile inmişti; bölünme/temettüde eski seri düzeltilmiyordu → auto_adjust=False + örtüşen barlarda %0.5 sapma kontrolü, sapan hisse baştan indirilir.
8. Evren bugünün listesi (kottan çıkanlar yok) → düzeltilemez, sonuçlar yukarı sapmalı okunmalı.

**Eksik metrikler (eklendi):**
9. Portföy max drawdown + özsermaye eğrisi → `portfoy()`.
10. XU100 / mevduat kıyası → işlem başı endeks üstü getiri, portföy dönemi al-tut ve mevduat.
11. Ayı dönemi → `OB17 = donem_kur('2017-01-01','2022-12-31','2017_22')` (bir kez, ~15 dk).
12. Ağırlıklı tek simülasyon (toplam ≤%100) + canlı CSV'de poz%, açılış fiyatı, XU100 kaydı.

**Küçükler:** `rapor()` beklenti ortalamayla; `portfoy_simulasyon` "YILLIK" kaldırıldı; test ve canlı aynı eşik `AL_PAY=1.002`; `takip_log.txt` eklendi.

**Yeni günlük akış:** aynı (`BASLAT` → `gun()`). Denetim: `denetim(OB24, OB23, OBUS, xu)`.
Eski önbellekler yeni alanları bilmez: `OB24=onbellek_guncelle(OB24, VERI, '2024_26')` (bir kez, birkaç dk); OB23 ve OBUS için de.

**Bekleyen karar:** düzeltilmiş rakamlar (tekil + ertesi açılış + drawdown + endeks üstü) eski %74/+14.5 ile karşılaştırılacak. Eski sayılar iyimser sınır olarak okunmalı.

---

## 7. GÖZ KALİBRASYONU (18 Eylül 2026, öğleden sonra)

Cemal'in gözle işaretlediği 29 çöl + 8 olumsuz (`kalibre_etiketler.csv`; veri `kalibre_veri.csv`, 32 hisse; PEKER veride yok) mevcut `col_segment` ile karşılaştırıldı (sinyal günü = çölün son barı):
- Mevcut kod çöllerin **13/26'sını** aday yapıyor (≥20 bar, ≤6 ATR); 6'sında hiç segment yok (INVES, SUNTK, INFO, OTTO, SKTAS, SMRTG), 8'inde çok kısa (BASCM −68, SEYKM −45, TUKAS −35 bar...), 2'sinde çok sola (BURVA +61, EYGYO +42). Tavan bulunduğunda hep doğru.
- **Nedenler:** (a) `yerel=5` dip kontrolü çölün içindeki küçük sarkmada segmenti sıfırlıyor — 26'nın 11'inde tetikleniyor; (b) çekirdek 5/7 şartı kırılım öncesi büyüyen mumlarda çölü siliyor (4/26); (c) çöküş sonrası ATR şişiyor (TEHOL'de fiyatın %20'si), 0.5 ATR tolerans anlamsızlaşıyor, çöküş mumları segmentte kalıp tavanı yukarı taşıyor.
- **v3** (`KALIBRE.py`): yerel 8 + min_cekirdek 3 + **sol kesme** (Cemal'in tanımı: çölün son 20 barının sakin ATR'si [TR medyanı] ile bant = [min Low, max gövde üstü] ± 1.0×sakin ATR; bant dışında kapanan son bardan sonrası çöl). Sonuç: aday **23/26**, yanlış tavan 4→2, başlangıç ±3 bar 8→11. Kalan: INVES/SUNTK/SKTAS'ta hâlâ yok; BASCM/SEYKM/KATMR'de çölün yavaş yükselen ilk yarısı kesiliyor (aday oluyor ama kısa).
- **Olumsuzlarda:** eski 3/8, v3 6/8 segment buluyor; doji/fitil/dar değerleri gerçek çöllerle aynı bantta — **şekil ölçüleri olumsuzu ayırmıyor.** Ayıran: kırılım (4/8 tavanı hiç kırmadı → sistem girmez) ve trail (PAPIL, SEYKM-26, ALTNY kırıp döndü). ERCB'de hiç segment yok (sıkışma yok; Cemal'in notuyla uyumlu).
- 32 hisselik provada: v3 sinyal 49→67, işlem başı beklenti benzer (+30.6 → +28.7), sermaye tavanı nedeniyle atlanan artıyor. Asıl cevap tam tarama.
- **Karar:** Colab'da `exec(open('.../KALIBRE.py').read()); K1=kalibre()` (~30-40 dk) → 2024-26 ve 2023'te eski vs v3 (tekil, ertesi açılış, ağırlıklı portföy, drawdown). İki dönemde de beklenti ve portföy toplamı geçer, max DD kötüleşmezse `v3_kalici()`. Geçmezse v3 yalnızca "göze uygun" kalır, sistem değişmez.
- Grafikler ve karşılaştırma tabloları sohbette gönderildi; `kalibre()` sonucu `kalibre_sonuc.csv`'ye yazılır.

---

## 8. 24–25 EYLÜL 2026 — DÖRT SET ÖLÇÜMLERİ, KLASÖR DÜZENİ, ÇAKIŞMA KAPISI

Test setleri: OB24 BIST 24-26 n=2064 · OB23 BIST 2023 n=820 · OBUS ABD 24-26 n=3595 · OBUS21 ABD 22-23 n=3138
(onbellek_ABD_2022_23.pkl). Ölçüm: tekil + ertesi açılış + 120 bar + %0.4 (islemler_olc), bootstrap %90 bant, eşli portföy + plasebo.
Eski %74/+14.8 = aynı sinyaller, ufuk 250 + tekilsiz + maliyetsiz; bugünkü %64/+8.9 temkinli cetvel. Segment kodu (YEREL=5) değişmedi.

KAPANANLAR (4 sette, hiçbiri kural olmadı):
- Sıcak sektör: BIST'te ağır kayıp düşük, ABD 24-26 nötr, ABD 22-23 TERS. Rejime bağlı.
- Hisse momentum 60g: işaret sette göre dönüyor. onc250: bant sıfırı kapsıyor (ABD'de U şekli).
- konum250 (çöl yıllık aralığın neresinde): dipte çöl bek yüksek AMA ağır kayıp da yüksek (3/4 set). Oynaklık.
- Taban koruması / kırılma sayısı: kırılan = daha geniş dağılım (ağır kayıp 4/4 yüksek, bek ABD'de yüksek). Oynaklık.
- Çöl kalitesi (küçük mum, taban, eğim, doji): kayıtların ~%15'i; kazanan %70 / ağır %10 vs %63 / %14.6; bek aynı.
  Tutunma/silkeleme beklemek geç giriş (bek +4 vs +9). Sıkı kapılar 4126 kayıtta 3 işlem bırakır.
- Alt dilim (4h/1h) çöl ölçüleri salınım dibinde: BIST 4h/1h ve yerleşik ABD 1h — hiçbiri (1h CLV BIST'te tek set, ABD'de yok).
TEK CÜMLE: Temiz çöl ağır kayıbı azaltır, beklentiyi artırmaz; büyük kazananlar kirli sıkışmalardan. Sistem = sıkışma kırılımı + trail;
boyut çarpanları (doji, alt fitil, dar hafta, CDS, borç/öz, üç şart) kaliteyi zaten taşır. Oynaklığa göre boyut: DENETIM.portfoy(mod='atr') — karar bekliyor.

QMLS / SALINIM (QMLS_Tarayici): yerleşik evrende 3. dip yazı-tura (ABD 1909: +0.1; BIST 410: −0.8). QMLS o evrende YOKTU (halka arz 16 Tem 2026).
Genç halka arz evreni (evren_kur --genc-ay 24 --genc-min-gun 40, fiyat 1–20$, 169 hisse): 105 sinyal, bek +1.6 [−0.7,+3.9], HEDEF +14.9 / STOP −10.6,
QMLS 15 Eyl sinyali HEDEF +29. 1h dipte CLV düşük (kapitülasyon) ve doji az iyi görünüyor, n=112, bant sıfırı kapsıyor; 1h veri 730 günle sınırlı,
büyütmek için Twelve Data anahtarı (ücretsiz) ya da günlük bar ölçüsü. Açık kalan tek soru budur.

KLASÖR DÜZENİ (25 Eyl): col_tarayici = üretim (BASLAT, COL_v1, DENETIM, onbellek, takip, temel, fon_takip, KALIBRE) + OLCUM.py (ölçüm).
arsiv/desen/ = DESEN_TAM ve desen çıktıları (kapalı proje; OLCUM ile aynı oturumda yüklenmez). QMLS_Tarayici = evren_kur v2.1, salinim_arsivi v1.1d,
dip_olcum v1.2, SEKTOR v1.4, tahtaci/nakit kapıları. ÇAKIŞMA KAPISI: ölçüm dosyaları yüklenirken bellekteki bir adı ezerse durur ve adı yazar.
Uzun iş kuralı: her adımda CSV, kaldığı yerden devam, süre ilk adımdan ölçülür. Drive: Colab'dan yerinde yaz; -1/-2 kopyaları adla düzelt.

---

## 9. 25 EYLÜL – 22 EKİM 2026 — SON DURUM (en güncel bölüm budur)

### 9.0 ÇALIŞMA ÇERÇEVESİ — BU DOSYANIN ROLÜ
- Sistem TEST AŞAMASINDA, nihai sürüm yok. Bu MD kural defteri değil; bağlam kopukluğuna karşı SİGORTA.
- Bir ölçü ancak tam iz bulunup (iki dönem aynı yön, simetrik etiket, plasebo/taban kıyası) testleri ve metrik hesabı
  doğru çıkınca KURAL olur. O zamana kadar her şey "deneme".
- Bölüm 1'deki "güncel kurallar" 18 Eylül durumudur. GEÇERLİ TESPİT ŞARTI aşağıdaki 9.1'dir (V1 = COL_v1.py).
- Çöl şekil metrikleri iz vermedi (9.2); bu yüzden tespit küçük muma dayandırıldı.

### 9.1 GÜNCEL TESPİT ŞARTI — KÜÇÜK MUM (V1 D7, 17 Ekim, son test)
- col_segment'te "küçük mum" = GÜN ARALIĞI (H−L, fitil dahil) ≤ 0.65 × ATR30. Eski tanım gövde |C−O| (MUM_OLCU='govde').
- Ölçüm (10 yıl, 583 hisse, aynı gün piyasaya göre), rüzgârlı sektörde dar çölden kırılım:
  2020-22: n=125 hedef %90, 60g +18, 120g +11 | 2023-26: n=97 hedef %83, 60g +5, 120g +9.
  Gövde tanımı aynı koşulda 0 / −1. Sinyal sayısı ~1/5'e iner.
- D9 uzun çöl + sektör rüzgârı (18 Eki): rüzgârlı sektörde ≥1 yıl dip çölü, 120 bar içinde önce +%20 mi önce −%10 mu:
  2016-19 %61 | 2020-22 %58 | 2023-26 %56 (piyasa 58/54/44; sektör çölsüz 45-55/49-55/41-46). Tek başına yön, "yüzde yüz" değil.
  D9b: rüzgâr = sepet − piyasa ≥ %10 VE sepet > 0 (çöküşte "az düşen" sahte rüzgârı keser; 10 yılda sonucu değiştirmedi).
- Durum: V1'de uygulandı, test sürüyor. Kural sayılmaz (9.0).
- 20 Eki: üretimde çöl tespiti artık D12 dip çölü (bkz. 9.5). D7 `col_segment` kodda duruyor (`SEGMENT_MOD='eski'` ile geri açılır); göz testinde Cemal'in 29 çölünden yalnız 1'ini buluyordu.

### 9.2 İZ VERMEYEN ÇÖL METRİKLERİ (küçük muma gidilmesinin nedeni)
- col_ogren v1.3 (9 Eki): 9419 tekil çöl; ayıran ölçüler yalnız tavan/taban etiketinde (geometri payı), simetrik ±%10 etikette
  hiçbiri ayırmıyor → GERÇEK İZ YOK. Doji çekirdeği (5–8 doji) ayırmıyor.
- col_tanim2 (9 Eki): Cemal'in 12 EVET çölünden 4'ünü geçiriyor, 3 HAYIR'dan 0; ayıran K2 (dip başta), K6 (en dip).
- BUYUK_YUKSELIS: büyük yükselişlerin yalnız %5'i çölden (kat 0.78). SIKISMA_TESTI: çöl içi/dışı fark yok.
- Boyut çarpanları (doji, alt fitil, dar hafta) Eylül ölçümleri; col_ogren'de doji ayırmadı → yeniden doğrulanmalı.
  Alt fitil <0.12 col_v2'de hâlâ ayrışıyor (+32 / +8.9; n=31).

### 9.3 FON TASFİYE KRİZİ — UNUTMA
- Eylül 2026'dan beri tasfiye fonu krizi: Tera, Pusula, Hedef, Atlas, A1, Pardus, Bulls portföy (COL_v1 FON_TASFIYE).
  Bu fonların payı olan hisselerde art arda taban serileri; piyasa medyanı 60 günde yaklaşık −%28 (COL_v1 D9b notu).
- 6 Ekim itibarıyla seri: ODINE 26, ANELE 19, GUNDG 18, DSTKF/ALKLC/BIGEN/IEYHO/OZATD/TEHOL/TRHOL 15, TERA/UFUK 14 gün.
  16 Ekim: ODINE, GUNDG, PRZMA, PEKGY ilk tavan; TERA, DSTKF, TRHOL, BINBN, UFUK, DURDO tabanda. SPK TERA'nın ihraç/bedelsiz başvurularını işlemden kaldırdı.
- **BU DÜŞÜŞLER GERÇEKTİR — BÖLÜNME / VERİ HATASI DEĞİL.** veri_koru_gunluk.csv'de bu hisseler için sıçrama kaydı yok;
  taban_serisi_izleme.csv fiyatları birebir tutuyor (TERA 16 Eki 22.20, DSTKF 242.80).
  Büyük düşüş görünce ÖNCE taban_serisi_izleme.csv + veri_koru_gunluk.csv'ye bak, bölünme varsayma.
- Günlük izleme: COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv (eski günler *_eski_TARIH.csv) ve
  motor_karne.csv (silkeleme / zıplama_kağıt / kalkış_kağıt — kâğıt işlemler; 16 Eki: 5 STOP, kalanı açık).

### 9.4 CANLI TAKİP (16 Ekim verisi, 18 Ekim çalıştırması)
- aday 47 | açık 10 | kapanan 6, hepsi zarar: PETKM −10.7 (trail), ISSEN −28, GUBRF −26, GARFA −22.6, TERA −88.6, DSTKF −90.1 (taban, T6).
- Açık: ISDMR ALARK AKBNK BIMAS GARAN YKBNK ISCTR TRCAS DURDO ZRGYO (Eylül 7–15 girişli). 9'unda kayıtlı taban yoktu → giriş×0.85 (yedek).
  DURDO 15–16 Eki iki taban (5.68), yedek tabanı 4.43.
- 17 Eki ilk T6 çalışmasında 81 aday ÇÖL BOZULDU ile düştü (çöküş haftası).

### 9.5 KOD DEĞİŞİKLİKLERİ (üretim)
- 8 Eki bolunme_onar.py: 69 bedelsiz onarıldı. A/B (col_ab_rapor.txt) sonuç değişmedi: 2024-26 bekl +10.4→+10.6, 2023 +40.4→+40.5.
- 9 Eki BASLAT + veri_koru.py (VK_YAMA v1.0): yenileme sonrası bölünme onarımı, B2_NEDEN; olaylar veri_koru_gunluk.csv. Seans açıkken bugünün yarım barı atılır.
- COL_v1 D7 (17 Eki): küçük mum = H−L → bkz. 9.1.
- COL_v1 D8 (17 Eki): fon süzgeci — tasfiye fonu payı ≥ FON_ESIK %5 olan hisse aday olmaz (kap_fon_paylari.json, kap_nobet_ayar.json, yoksa FON_BILINEN).
- COL_v1 D9/D9b (18 Eki): uzun çöl (6/12 ay dar bant, dipte) + sektör rüzgârı (sepet − piyasa ≥ %10 VE sepet > 0), ruzgar_listesi(); sektor_BIST.csv.
- takip T6 (17 Eki): taban kırılınca çık (TABAN_TOL %2; taban yoksa col_segment, o da yoksa giriş×0.85). Cemal'in kuralı.
  DİKKAT: bölüm 3'te "taban kırılınca çık" ve "taban kırılması düşürme" testte kötü çıkmıştı — karar bekliyor.
- takip T7: fon süzgeci (açık pozisyonda yalnız uyarı). T8: D9 uzun çöl + rüzgâr gun() ekranında.
- COL_v1 D10 (20 Eki, inceleme): D10a `bugun_liste`'ye `ruzgar` sütunu eklendi. D9b şartı artık burada da uygulanıyor ve rüzgâr kararı `sektor_ruzgar` içinde tek yerde veriliyor; `takip` BEKLE zaten doğruydu.
  D10b rüzgâr hesabında tarih hizası: verisi `RUZ_BAYAT`=5 iş gününden eski hisse hesaba girmiyor (log'a yazılıyor). Başlangıç kapanışı ortak takvim gününden alınıyor, böylece arada boşluk olan hissenin penceresi uzamıyor.
  Sentetik sınama: tam takvimli 581 hissede sonuç birebir aynı. Boşluklu hissede eski kod −%38, yeni kod +%25 (doğrusu). AL kuralı, segment ve çarpanlar değişmedi.
- COL_v1 D11 + takip T9 (20 Eki): bayat aday. `veri_bayat()` son barı ortak son tarihten `VERI_BAYAT`=5 iş gününden eski olan hisseyi "veri durdu" sayıyor.
  Böyle bir hisse artık aday olmuyor. Listede bekleyen aday "VERI DURDU" yazısıyla düşüyor, `bugun_liste`'de de aday sayılmıyor.
  Açık pozisyon otomatik satılmıyor (işlem durmuş olabilir), yalnızca uyarı basılıyor. Bayat oranı %10'u aşarsa bu toplu veri sorunudur: temizlik yapılmıyor, uyarı basılıyor.
  Sentetik sınama: eski kodda bayat aday listede kalıyor ve yeni bayat hisse aday oluyordu; yenisinde ikisi de düzeldi. %15 bayat senaryosunda aday silinmiyor.
- COL_v1 D12 (20 Eki): DİP ÇÖLÜ — Cemal'in tarifi: düşüş sonrası dipte bölge, bir noktadan sonra yeni dip yok; mumlar küçülür, Bollinger daralır, doji ve hacim kuruması beklenir.
  `col_dip()` = bölge kuralı (GOZ_ESLE v1.3 ile birebir aynı, 2379/2379) + dipte (`DIP_KONUM` 0.35) + son %40'ta yeni dip yok + 4 imzadan ≥3 (küçük mum, Bollinger daralma, doji artışı, hacim kuruma).
  Göz testi (37 etiket): 29 çölden 12'si tam pencereyle (+4 kısmi) bulunuyor; eski D7 1/29. 8 "değil"den 4'ünde de çöl görüyor; şekil ölçüleri "değil"i ayırmıyor, bölüm 7 ile aynı.
  COL_DIP_TEST (atılımda ertesi gün açılış alım, %20 sonra SMA20 trail / 120 bar, tekil; taban = her taze 20 gün zirvesi kırılımı), beklenti dip/taban:
  BIST 16-19 +14.7/+13.8 · 20-22 +15.9/+24.1 · 2023 +42.0/+28.8 · 24-26 +6.9/+9.2 · ABD 22-23 +1.6/+3.2 · ABD 24-26 +11.3/+5.6.
  6 dönemin 3'ünde tabandan iyi → TABANI GEÇMEDİ, iz değil. Asıl kaynak yine atılım + trail (bölüm 8 ile aynı). Kazanan oranı hiçbir dönemde tabanın 1.3 katına çıkmadı.
  Eski D7 ile aynı örneklemde (200 hisse) dip daha iyi: 2023 +47.1/+29.5, 24-26 +8.6/+6.4. Atılımdan önce bozulan aday %28–42.
  Üretimde `SEGMENT_MOD='dip'` (20 Eki): eski tespitten iyi ve Cemal'in çöllerini görüyor; kural sayılmaz.
  COL_GECMIS.py: geçmiş bir günde (ör. 16 Mart 2024) kod hangi çölleri bulurdu + her cuma tarama (grafikli PDF, hisse adsız).
- takip T10 (21 Eki, Cemal'in "yaz" kararı): STOP MALİYETE. Pozisyonda girişin +%8 üstü görüldüyse (önceki barların en yükseği, aynı gün sayılmaz) stop = giriş fiyatı;
  sonraki bir günde Low ≤ giriş ise SAT neden='maliyet', çıkış = giriş, getiri 0. Sıra: taban (T6) > maliyet > trail (%20 sonra SMA20) > ufuk (120 bar).
  `MALIYET_ESIK`=8.0, CSV'de `maliyette` sütunu, TUT satırında 'stop=maliyet'. AL kuralı, çarpanlar, trail ve ufuk değişmedi. test_takip.py 5/5 (maliyet çıkışı, bayrak kalıcılığı, +8 yoksa stop yok, aynı gün sayılmaz, taban önceliği).
  Dayanak COL_YOL B15: BIST 4 dönem 30 slot ort. +157 vs mevcut +144, ağır kayıp %10→%6. ABD (21 Eki, aynı gün): teyit etmedi — ABD ort. maliyet8_sma20 +17 vs mevcut +21 (22-23: −6 vs +6; 24-26: +40 vs +37).
  6 dönemin 3'ünde mevcudu geçiyor → getiri izi değil; tutarlı olan tek şey ağır kaybın yarıya inmesi (6/6 dönem). Üretimde kalıp kalmayacağı Cemal'in kararı (geri alma tek satır: MALIYET_ESIK=999).
- BASLAT B5 + takip T11 (21 Eki, Cemal: "gun() her saatte çalışsın, bugünün mumu bitmediyse dünkü veriyle"): seans açıkken (TR iş günü 09:00–19:00, CANLI değilse) bugünün yarım barı
  VERI'den ve XU100'den her zaman atılır; pkl'de kaldıysa pkl temizlenir. Eskiden yalnız indirme yapıldığında atılıyordu: 21 Eki 12:43'te "veri güncel, indirme atlandı" deyip bugünün barını tuttu, XU100'e hiç uygulanmıyordu.
  gun() kendi içinde de aynı kapıyı taşır (tarih verilmişse/replay'de uygulanmaz). 19:00 sonrası bugünün barı kalır; 19:35 Actions koşusu etkilenmez. test_takip.py 7/7.
  Not: Colab'da gun() çalıştırmak Drive CSV'lerini yazar; takip CSV'lerinin asıl yeri repo (Actions). Gün içi koşu istenirse Actions'ta gunluk_col_tarama elle tetiklenir, dünkü veriyle çalışır.
- COL_v1 D13 (21 Eki, Cemal'in üç kuralı + "kodu bul ve yaz"): `col_dip2()` ÜRETİMDE (`SEGMENT_MOD='dip2'`; geri alma `SEGMENT_MOD='dip'`). Kutu = [yeni dip d, bugün]; d = son 120 barın en düşük Low'u → önceki raf/düşüş kutuya girmez (kural 1).
  Şart: dipten beri ≥15 bar (dip savunuldu), dip pencerenin ilk 3 barında değil, kutu öncesi iniş ≥%10, dipten sonraki Low'lara parabol a>0 ve son eğim>0 (yukarı yuvarlanma), dipten sonra ≥2 küçük mum öbeği (≥3 ardışık bar, aralık ≤ kutu medyanı). Konum ve küçük mum katı şartı yok (ayırmadı). Tespit işlem kararından ayrı: kırılıp toparlanan kutu da tespit edilir, bozulma kararı takip'te (kural 3).
  Seçim COL_TESPIT.py (3456 varyant, arastirma_cikti/col_tespit/): göz testi Cemal'in 29 çölünden 17 (D12 16), 29 "değil" kutusundan 2 yanlış alarm (D12 8); ARZUM en iyi öbek yakalandı, düşen bıçak yakalanmadı. Evren (BIST 2016-26 + ABD 2022-26, 18,7 bin sinyal): 60 barda alım oranı tabandan +12…+26 puan 6/6 dönem, alım sonrası üretim çıkışı getirisi tabandan iyi 6/6 (ör. 2023 +19,9 vs +13,2; 24-26 +4,2 vs +2,8), bozulma %2-9 (taban %31-44); 60 bar ileri getiri 4/6 (20-22 −1,2, ABD 22-23 −1,5). Hiç yakalanmayan 8 çöl: BINBN-24, EMNIS, EUREN, INVES, SKTAS, SMRTG, VRGYO (dipten sonra 15 bar yok ya da parabol yok), PEKER (veri yok).
  Eksen etkileri: yuvarlanma şartı yanlış alarmı en çok düşüren (yok 6,0 → parabol 3,0), N120 N60'tan temiz (2,9 vs 5,9), konum/küçük mum/retest ayırmıyor. D12 `col_dip` ve D7 `col_segment` değişmedi; carpan alanları ortak `_col_alanlar` (D12 çıktısı 1687 karşılaştırmada birebir). test_col_dip2.py 5/5, test_takip 7/7. col_olc kapıları (≥20 bar, ≤6 ATR) D13'te de geçerli.

### 9.6 DİĞER ÖLÇÜMLER (tekil, ertesi açılış, onarılmış veri)
- col_v2 / yeniden_tara (8 Eki; bugünkü col_olc): 2024-26 yeni liste n=989 %69 bekl +10.8, portföy eşit +140% (yıllık +45, DD −14);
  eski liste n=555 %70 +10.3, eşit +72% (yıllık +27, DD −11). 2023 yeni n=415 %86 +40.5 eşit +133%; eski n=379 %87 +40.0 eşit +107%.
  XU100 aynı dönem +20/+73, mevduat %40.
- tahtaci_oyunu v1.3 (8 Eki): klimaks n=304 r10 −2.35, plasebodan kötü → GEÇMEDİ; teyit ve sessiz de geçmedi.
- BUYUK_YUKSELIS (2 Eki; 13 hf +%40, 3328 olay): ÇÖL deseni kazananların %5'i (kat 0.78) — büyük yükselişler çölden gelmiyor.
  Hafif iz: sektör dalgası ≥3 (kat 1.25), genişlik >70 (1.29), konum_52 ≥0.7 (1.24). Haber izi yok.
- TEYIT_BILETI (2 Eki): ertesi açılış, hedef +20, stop teyit dibi: bilet net +1.01; 2022-26 +0.41; 2026 −2.13 → zayıf.
- SIKISMA_TESTI (1 Eki): çöl içinde bilet +0.07, dışında −0.02, çöl+sivrilmiş −1.33 → fark yok.
- COL_KIRILIM_ATLAS (2 Eki): öncü/rüzgâr sırası tutarsız ("öncü yok + rüzgâr var" +8.0, "öncü var + rüzgâr" +0.4).
- QMLS_Tarayici (4 Eki): 4s bant salınımı, QMLS 2 işlem +33; salınım bulucu 266'dan 8 aday (ANGX, PUSA, BMM...). n çok az.
- KAP arşivi (3–4 Eki): kap_bildirimler.csv, kap_ozet (2017–26), fiyat_ozet, m1–m5 tabloları; KAP_ARSIV.py.

### 9.7 KLASÖRLER
- Üretim: MyDrive/col_tarayici. Araştırma çıktıları: MyDrive/COLAB_VERILER/col_tarayici/
  (atlas, sikisma, sikisma_ABD, buyuk_yukselis, teyit_bileti, kap, kap_ozet, fiyat_ozet). teshis/ = islem_goster çıktıları.
- Kod yedekleri: dosya.py.YYYYMMDD_SSDD biçiminde ayrı klasörde.

### 9.8 AÇIK / BEKLEYEN
- Küçük mum (D7) + D9: test sürüyor; tam iz ve doğru metrik hesabı gelince kural.
- D12 dip çölü tabanı geçmedi (9.5). Cemal'in 29 çölünden 8'i imza ölçülerine takılıyor (INVES, HDFGS, INFO, KATMR, EUREN, ARZUM, VRGYO, EMNIS): ya ölçü yanlış ya etiket — Cemal'in gözüyle karar bekliyor (karne grafikleri).
  21 Eki tanı (goz_esle/goz_imza_tani.csv, betik goz_esle/arastirma/imza_tani.py; etiket bitişi ±5 bar, üretim col_dip): 29 çölün 16'sı COL.
  Kaçanlar: 5'i "dipte değil" (SUNTK 0,40 · ARZUM 0,42 · SKTAS 0,38 · EUREN 0,52 · VRGYO 0,57; eşik 0,35) · 6'sı "imza az" (INVES, HDFGS, INFO, KATMR, EMNIS, TEHOL-2026) · 3'ü veri kısa (TATGD-1, BINBN-2, PEKER yok).
  Küçük mum ölçüsü 250 gün yerine önceki 60 güne göre alınırsa INVES 0,14→0,80, HDFGS 0,22→0,61, VRGYO 0,08→0,58 geçer; INFO, KATMR, EUREN yine geçmez (mumları önceki 60 günden de iri).
  OLUMSUZ 8'in 4'ü (PAPIL, ALTNY, TUREX, GARFA) bugünkü kuralla COL çıkıyor; konum, bant genişliği, eğim ve küçük mum hiçbiri bu dördünü Cemal'in çöllerinden ayırmıyor. Sonuç: yakalama için DIP_KONUM ve mum referansı gevşetilebilir, ayırma için Cemal'in PDF notu şart. n=37, bulgu değil, ölçüm.
  21 Eki COL_BUGUN (bugünkü tarama, 583 hisse, arastirma_cikti/col_bugun/): D12 yalnız 4 çöl buluyor (EKGYO, ARZUM, OYLUM, EUYO; hiçbiri kuralı geçmiyor). 354 kutu kapıya takıldı: 223 yeni dip, 74 dipte değil, 57 imza az. Çöküş haftasında aday sayısı 43'ten (D7) 4'e iner.
  Cemal'in notu (21 Eki, OYLUM/EUYO grafiği): kod düşüş ÖNCESİ küçük mumlu rafı + düşüşü + yeni dibi tek kutu sayıyor. Doğrusu: önceki bölge dibi kırılınca biter, çöl yeni dipten sonra sayılır. Ayrıca: aşağı kırılıp sonra toparlanıp giden çöller kaçmamalı (tespit kuralı daraltılmamalı; bu takip/çıkış işi). Kod kırılım yönünü bilmiyor; eldeki yön ölçüleri B12 (son 4 hafta hacmi, IZ_DEFTERI) ve D9 rüzgârı. D12'nin "hacim kuruma" imzası B12 ile ters yönde çalışıyor olabilir.
  21 Eki etiketleme (goz_esle/etiket_2026-10-20.csv): bugünkü 21 kutunun (kodun 4 "çöl"ü dahil) HİÇBİRİ çöl değil. Cemal: "küçük mum tek başına yetmez; dip oluşmalı, dip savunulmalı, parabolik yukarı yuvarlanma ve küçük mum öbekleri sırası birlikte olmalı". #19 VAKKO'da mumlar küçük ama diğerleri yok; öteki 20'de onun gözünde küçük mum yok (kodun 'kucuk' imzası çoğunda geçiyordu).
  COL_SEKIL (arastirma_cikti/col_sekil/, 28 çöl vs 29 değil): ayıran ölçüler dip_pos (dibin kutudaki yeri; çöl 0,09 / değil 0,76, AUC 0,20), dip_oncesi_dusus (4% / 14%, AUC 0,21), dip_sonrasi_bar (26 / 12, AUC 0,79), obek (2 / 0, AUC 0,74), retest (4 / 1, 0,71), son_egim (+3,5 / −2,9, 0,69), hacim_kat60 (0,91 / 0,72, 0,71 → çölde hacim KURUMUYOR, D12'nin hacim kuruma imzası ters). Ayırmayanlar: aralik_ref250 (0,38), kucuk_oran250 (0,58) → kodun küçük mum ölçüsü Cemal'in gözüyle örtüşmüyor; mutlak aralık % da ayırmıyor (0,58).
  Aday bileşik kural E = dip kutunun ilk yarısında + dipten sonra ≥15 bar + dipten sonra ≥1 küçük mum öbeği (≥3 ardışık, aralık ≤ kutu medyanı): çöl 21/28, değil 7/29. Bugünkü imza (kucuk_oran250 ≥0,6): 15/28 vs 15/29 (ayırmıyor). E'yi kaçıran çöller: BURVA, BASCM, SEYKM, INFO, EUREN, SKTAS, ESCAR. E'yi geçen "değil"ler: GEDIK, ALTNY, SDTTR, GARFA, GRSEL (+2). Uyarı: "değil" setinin 21'i çöküş haftasından (dönem etkisi), n küçük → ölçüm, bulgu değil. Üretim değişmedi, "yaz" bekliyor.
  21 Eki ARZUM çizimi: Cemal'in deseni küçük ölçekte de var (dip → savunma → yukarı yuvarlanan küçük mum öbeği, arka arkaya). Etiketleri (goz_esle/etiket_obek_ARZUM.csv): Eki–Kas 2025 öbeği DÜŞEN BIÇAK (çöp), Kas–Ara kabul (alım gelmeden düştü), Oca 2026 EN İYİ (alım + kutuya geri test + ekleme + büyük kazanç), Nis–May kabul (alım gelmeden düştü). Karar: öbek tespitine yön şartı yok; alım gelmeyen de kaydedilir, ayıran ölçü öğrenilir. Alım = YEŞİL mumun kapanışı öbek tavanının üstünde. Cemal'in yolu: alımdan sonra %8–10 görülünce stop maliyete.
  COL_OBEK v1.2 (arastirma_cikti/col_obek/, 583 hisse 2016–26, 69.180 öbek): öbekten sonra ALIM oranı 4 dönemde tabanın 15–20 puan üstünde (16-19 %70/%52 · 20-22 %78/%62 · 2023 %67/%54 · 24-26 %71/%49). AMA alım geldikten sonra "+%8'i stoptan önce gördü" oranı tabanla aynı (%72/%75 · %82/%82 · %79/%83 · %73/%72); 120 bar piyasaya göre medyan +2 puan, 16-19'da 0. Yani öbek yalnız "alım gelir mi" sorusuna cevap veriyor, alım sonrası kazanca bir şey eklemiyor (bölüm 8 dersiyle aynı). Öbek sırası ↑, yuvarlanma ↑, konum250 ↑ iki dönemde de alımı artırıyor; düşen bıçak ölçüsü zayıf. IZ_DEFTERI B14 (ADAY, yalnız yön). Kuruş hisse veri sıçraması: 2016-19 ortalamaları %200'de kırpılı okunur.
  COL_YOL (21 Eki, arastirma_cikti/col_yol/, 50.006 öbek işlemi + 106 bin taban): çıkış varyantları. 30 slot portföy 4 dönem ortalaması: maliyet8_sma20 +157 (2 dönemde birinci) · mevcut+stop +144 · zirve10 +140 · maliyet_20 +134 · cemal merdiveni +123 · mevcut stopsuz +105. Yalnız maliyete çekme işlemlerin çoğunu maliyetten çıkarıyor (medyan −0,4). Hiçbiri mevcut sistemi 1,3x geçmiyor; "+%8'de stop maliyete + %20 sonra SMA20 trail" ağır kaybı %10→%6 düşürüp portföyü biraz artırıyor (1,09x). Öbek, tabana göre ağır kaybı her varyantta düşürüyor. Sabit hedef al-çık (+5/8/10/15/20, yoksa stop): kazanan %84→%64, işlem başı +1,4→+6,5, portföy 4 dönem ort. hedef_8 +130 en iyisi; hiçbiri +157'yi geçmedi. IZ_DEFTERI B15. ABD (21 Eki, 23.096 + 47.843 öbek işlemi): maliyet8_sma20 ABD ort. +17 vs mevcut +21 (22-23: −6 vs +6; 24-26: +40 vs +37); maliyet_8 (trail'siz) +25, mevcut stopsuz +37 en iyi. Getiri üstünlüğü ABD'de yok → İZ DEĞİL (B15). Tutarlı olan: maliyete çekme ağır kaybı her dönemde yarıya indiriyor (BIST %10→%6, ABD %7→%4) ve kazanan oranını düşürüyor (%61→%39). T10 yine de üretime yazıldı (Cemal'in kararı, bkz. 9.5).
  COL_KAZANC (21 Eki, arastirma_cikti/col_kazanc/, Cemal: "her şey aynı kalsın, mevcut koda ne eklersek kazanç artar? hacim öbekte kurusun, alım mumu 2-3-4 kat gelsin"): üretim yolu (öbek → alım → T6/T10/trail) sabit, 25 ölçü kovalara bölünüp 6 dönemde (BIST 4 + ABD 2) tüm işlemlere göre fark ölçüldü; 120 bin öbek + 250 bin taban işlemi.
  HACİM TERS ÇIKTI: alım mumu hacmi ≥4 kat BIST 4 dönemde de kötü (−0,4/−2,3/−7,3/−2,3 puan, kazanan %40→%32), ABD'de hafif iyi (+1,9/+1,7) → iz değil, BIST'te zarar. Düşük hacimli alım (<1 kat) BIST'te 4/4 iyi (+1,9/+4,7/+11,6/+3,6) ama ABD'de eksi → iz değil. Öbek hacmi kuruması (<0,7×) BIST'te 3 dönemde kötü (−0,8/−1,7/−6,0), 24-26 +2,6; ABD +0,2/+0,6 → iz değil.
  6/6 tutarlı tek şart: öbeğin son haftası hacmi öbek ortalamasının altı (<0,8) → +0,8 puan, işlemlerin %15'i, slot portföy −5 (işlem azalıyor); taban işlemlerinde de 5/6 → öbekle ilgisi yok, değersiz. 5/6 olanlar: alım günü piyasa ≥ +%1 (+2,9 puan ama slot −18), küçük alım mumu (<1,5× öbek mumu, +0,8, slot +12), önceki öbek yukarıda (+0,5).
  BIST 4/4 ama ABD'de karışık (tercil sınırları pazar içi): güçlü yuvarlanma (yuv T3 +2,2, slot +30), yüksek öbek (T3 +1,5), düşük likidite (T1 +5,2; kuruş etkisi). BIST'te tutarlı KÖTÜ: w=25 (0/6), en likit üçte bir (0/4, −4,5), yıllık getirisi en düşük üçte bir (0/4, −2,8), yuvarlanması en zayıf üçte bir (0/4, −2,1).
  SONUÇ: üretim koduna eklenecek şart yok; bölüm 8 dersi aynen (kırılım öncesi eleme para kaybettirir). Hacim beklentisi (kuruma + patlama) veride yok, tersi var. IZ_DEFTERI C. Üretim değişmedi.
  K7 DOĞRULAMA (21 Eki, COL_KAZANC v1.1, `python COL_KAZANC.py dogrula` yalnız K7'yi işlem dosyasından çalıştırır; COL_KAZANC_dogrulama.md): Cemal'in planıyla küçük alım mumu (<1,5×) izi sorgulandı. BIST'te güçlü ve tutarlı (4/4 dönem +1,5…+2,9, Bonferroni geçer, 17/20 kova içi artı, desil monoton −0,87, slot aynı n'li rastgeleden 4/4 üstün), ABD'de yok (−0,6/+0,0, desil ters). Kaynak: alım günü göreli hacmi; log RVOL kontrolüyle küçük mum katsayısı BIST'te sıfıra iner (t +6,8 → −0,2), RVOL kovaları içinde fark yok. Fiyat/NATR normalizasyonu değiştirmedi; 5 gün sonrası vol genişlemesi küçük mumda daha düşük (BIST 1,10–1,20 vs 1,32–1,45; ABD 0,98–1,02 vs 1,06–1,10). Cemal'in 5 maddesinden yapılanlar: NATR (1), RVOL (2; free-float devir verisi yok), fiyat grupları (4; piyasa değeri verisi yok, lik60 vekil), 5 gün ileri test (5, üretim yolu içinde). BB/Keltner sıkışması (3) alim_mum_kat ve natr50_pct ile aynı şeyi ölçtüğünden ayrıca eklenmedi (90+ şekil ölçüsü kapalı). SONUÇ: pazar-spesifik BIST bulgusu = düşük hacimli kırılım vekili; iz değil, araştırıldı, alınmadı. IZ_DEFTERI C.
  K8 BİRİKİM (21 Eki, COL_KAZANC v1.2, `python COL_KAZANC.py birikim`; COL_KAZANC_birikim.md, col_kazanc_obekler.csv.gz = alım gelmeyenler dahil tüm öbek/taban kutuları): Cemal'in NVI/CMF kurumsal birikim fikri. Öbek boyunca CMF20, NVI, A/D, OBV → akış sınıfı birikim/dağıtım/karışık. ABD'de birikim öbeği alımı artırıyor (%76 vs %68) ama 60 gün ileri getiri ve alım sonrası getiri düşük/sıfır (−0,9/−1,0; −0,5/+0,3), dağıtım 22-23'te daha iyi → ABD'de ayrışma kâr getirmiyor. BIST'te 4/4 dönem güçlü (ileri60 +2,5…+8,5, alım sonrası +2,4…+9,9) ama tabanda da aynı → öbeğe özgü değil, pazar-spesifik. SONUÇ: iz değil, araştırıldı, alınmadı. IZ_DEFTERI C. Level 2 / FINRA verisi yok.
  COL_TESPIT (21 Eki, arastirma_cikti/col_tespit/COL_TESPIT_rapor.md, col_tespit_varyant.csv): Cemal'in üç kuralıyla tespit motoru adayları, 3456 varyant; kazanan D13 olarak üretimde (9.5). Taban (BIST): alım %52-64, bozulma %31-44, ileri60 +5…+24; D13: alım %75-83, bozulma %2-9. En çok yakalayan varyant (N60 üçte-bir, 22/29) 13/29 yanlış alarm veriyor → alınmadı. İzleme: canlı aday sayısı ve kalitesi D12'ye göre (COL_BUGUN 4 çöl buluyordu).
  Ölçüm (goz_esle/arastirma/kutu_dip_tani.py → goz_esle/goz_kutu_dip_tani.csv): "raf kesme" (kutudaki en düşük dipten önceki kapanış medyanı sonraki kapanışların %90'ının üstündeyse kutu dipten başlar) ve bant 4x, 37 etikette: COL 16→17/30, OLUMSUZ yanlış alarm 4/8 değişmedi, raf 3 etikette kesildi. Cemal'in çöllerinden hiçbirini kaybettirmiyor; faydası tam evrende (OYLUM/EUYO tipi kutular) ölçülecek. Üretime alınmadı, "yaz" bekliyor.
  COL_GOZ (21 Eki akşam, arastirma_cikti/col_goz/; Cemal: "kod binlerce çöl bulmuş, sen tek tek bak karar ver"): D13'ün 2024-26 BIST kutuları (3100; üretim kapısı sonrası 746) grafikle tek tek gözden geçirildi. Gözle ÇÖL 45 (%6), SINIR 105 (%14), DEĞİL 568 (%76; KISA 252 bir aylık duraklama, V 155 dip sıçraması, GENİŞ 70, TREND İÇİ 75, YÜKSELİŞ 16), veri hatası 28. Kodun sistematik hatası: kutu 120 bar dibinden başlayıp ilk uygun günde (20-40 bar) sinyal veriyor; gerçek çöllerde düz bölge kutudan çok önce başlıyor, kod yalnız son parçayı işaretliyor. ÇÖL kutularında alım %89 / bozulma %4 / ileri60 medyan +13,6 (diğerleri %80 / %17 / +0,6) — ama grafiklerde sonraki 40 bar görünüyordu, sonradan bilgi; n=45, iz değil. Basit ölçüler (kutu öncesi düz bar, yuk_atr, kapanış konumu, mum küçüklüğü) göz kararını ayıramadı. Üretim değişmedi; Cemal'in 45+105 kutuyu onaylaması bekleniyor (PDF sohbette).
  Cemal'in kararı (22 Eki, arastirma_cikti/col_goz/col_goz_cemal_2024_26.csv; dokunmatik işaretleme sayfası): 150 kutunun 88'i EVET, 62'si HAYIR (benim ÇÖL 33/45, SINIR 55/105 EVET). Notları ("atılım barı yok", "kutunun devamı var", "daha ilerisi var") kararın sinyal SONRASI atılıma göre verildiğini gösteriyor: EVET'lerde alım %98, bozulma %1, ileri60 medyan +15,6; HAYIR'larda %76, %18, −7,2. Şekil ölçüleri EVET/HAYIR'ı ayırmıyor (bar, yük, düz bar, mum küçüklüğü AUC 0,45-0,53; kapanış konumu 0,62). Yani etiket "çöl mü" değil "atılım geldi mi" etiketi (bölüm 4 ders 5, DERS 4 ile aynı); tespit kuralı bundan öğrenilemez. Yol: sinyal sonrası gizlenerek yeniden etiketleme, ya da tespit D13'te kalır ve ayırma AL kuralına bırakılır (zaten öyle). Üretim değişmedi.
  MUM_SUKUN v1.1 (22 Eki, Cemal'in ANGX notu; arastirma_cikti/mum_sukun/, test_mum_sukun.py 7/7): düşüş sonrası son 3-4 mumun boyu hissenin KENDİ 250 günlük dağılımının yüzdeliğiyle ölçüldü (sabit eşik yok); geçerli mum şartı (H>L, hacim>0) v1.1'de eklendi (v1.0'da BIST sinyallerinin %24'ü kilitli/işlemsiz günlerdendi). 24 varyant × BIST/ABD × 2016-21/2022-26: hiçbir dilimde taban (aynı bağlamda normal mumlar) oranının 1,3 katı yok, ortalama kat 0,96–1,04. Tek eğilim BIST'e özgü (4 mum gövde sıralı küçülme 1,2 / 1,1, n 190/233), ABD'de yok. Büyük hareketi de önceden göstermiyor. İz değil (IZ_DEFTERI C).
  MUM_SUKUN v1.2 zemin modu (22 Eki, Cemal: 'sert düşüş düz zemine çarpar, 4-5 mum zemine yapışık sıra'; test_mum_sukun.py 8/8): dipleri hizalı, boşluksuz, kaymayan 4/5/6 mumluk sıra, ölçüler hissenin kendi normal mum boyu cinsinden; bağlam sert düşüş + 60 bar dibi; taban aynı düşüşte dağınık sıra. 6 varyant × 4 dilim: hiçbiri 4 dilimde 1,3 kat değil (z_siki k=5: ABD 1,24 / 0,93, BIST 1,08 / 1,13); ABD'de 60 gün getiri tabandan kötü. İz değil (IZ_DEFTERI C).
- T6 (taban kırılınca çık) testle çelişiyor: tut ya da kaldır.
- Boyut çarpanları (doji/fitil/dar) yeniden doğrulama.
  Aynı işte düzeltilecek (20 Eki inceleme): `dar_hafta_olc`, segmentten önceki haftayı da segmente sayıyor ("ilk" bloğu). Bu yüzden `dar` değeri düşük çıkıyor.
  Düzeltme `dar` değerlerini değiştirir, bu yüzden tek başına yapılmayacak.
- ~~Verisi durmuş hissenin aday olması ve listeden hiç çıkmaması~~ → 20 Eki'de D11/T9 ile düzeltildi (bkz. 9.5).
- GitHub Actions günlük tarama: eski iş akışı 19 Eki 21:01'de elle kapatılmıştı. 20 Eki'de `gunluk_col_tarama.yml` adıyla yeniden kuruldu; ilk başarılı çalışma 20 Eki 21:30 (aday 43, açık 10). CDS 21 Eki'de güncellendi (investing.com, 21 Eyl–19 Eki 2026; 4–18 Eyl boşluk, kaynak sayfa vermedi): 250,1 bp, pct250 0,84 → çarpan 1,5x (3 Eyl verisiyle 0,22 → 0,5x idi). Boyut 3% → 9% olur; ilk etkisi 21 Eki raporunda.
- DURDO açık pozisyonda taban serisinde.
- 9 açık pozisyonda gerçek taban yok (yedek ×0.85).
- motor_karne kâğıt işlemleri sürüyor.

---

## KISA BLOK (yeni sohbete yapıştır)

```
ÇÖL YOLU / BIST+ABD; tam özet Drive: col_tarayici/COL_OZET.md (bölüm 9 = son durum).
SİSTEM TEST AŞAMASINDA; bu MD bağlam sigortası, kural defteri değil. Tam iz + doğru metrik hesabı gelince kural olur.
GÜNCEL TESPİT (21 Eki, D13 col_dip2): kutu yeni dipten başlar (son 120 barın dibi; önceki raf girmez) + dip ≥15 bar savunuldu + iniş ≥%10 + Low'lara parabol yukarı dönmüş + ≥2 küçük mum öbeği. Göz 17/29, yanlış alarm 2/29 (D12 16/8). COL_GOZ (21 Eki): 2024-26 evreninde kodun 746 kutusundan yalnız 45'i gözle çöl, 105 sınır; kod bölgenin son parçasını işaretliyor, çoğu kutu V ya da bir aylık duraklama. Evren: alım tabandan +12..26p, üretim getirisi 6/6 iyi, ileri60 4/6. Geri alma SEGMENT_MOD='dip'. D12 (bölge + dipte + imza) kodda duruyor; şekil metrikleri iz vermedi (col_ogren).
EYLÜL-EKİM 2026 FON TASFİYE KRİZİ: TERA/DSTKF/ODINE/GUNDG/TRHOL... taban serileri GERÇEK düşüş, bölünme değil. Büyük düşüşte önce COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv + veri_koru_gunluk.csv.
Ekim eklemeleri: D8 fon süzgeci, D9 uzun çöl + sektör rüzgârı, D10 rüzgâr etiketi (D9b) + tarih hizası, D11/T9 verisi durmuş hisse aday olmaz, D12 dip çölü (20 Eki), D13 col_dip2 üretimde (21 Eki, Cemal'in üç kuralı); takip T6 taban kırılınca çık (testle çelişiyor), T7, T8, T10 +%8 görülünce stop maliyete (21 Eki; BIST +157 vs +144, ABD teyit etmedi, ağır kayıp yarıya), B5/T11 seans açıkken bugünün yarım barı her zaman atılır; veri_koru.
Kural: col_dip2 (D13; col_olc ≥20 bar ≤6 ATR) → aday; kapanış>tavan×1.002 → AL; taban −%2 kapanış → çık (T6); +%8 görülünce stop maliyete (T10); %20 → SMA20 trail; 120 bar.
Boyut %6×CDS×borç×doji×fitil×dar×kural, max %12. Aday filtresi yok. Segment kodu değişmedi.
Gerçek sayı (tekil, ertesi açılış, 120 bar): BIST 24-26 %64/+8.9 · BIST 23 %88/+38 · ABD 24-26 %62/+8.3 · ABD 22-23 %62/+4.7.
Test setleri OB24/OB23/OBUS (BASLAT) + OBUS21 (onbellek_ABD_2022_23.pkl). Ölçüm: exec OLCUM.py → islemler_olc/dilim/kiyas/esli_kiyas.
Çakışma kapısı: ölçüm dosyası üretim adını ezerse durur. DESEN_TAM arsiv/desen/ altında, kapalı; OLCUM ile birlikte yüklenmez.
Kapananlar: sektör, momentum, onc250, konum250, taban koruması/kırılma, çöl kalitesi filtresi, tutunma/silkeleme, 4h/1h çöl ölçüleri salınım dibinde,
QMLS tahtacı/nakit/onay/dip sırası, giriş zamanlaması, stoplar, 90+ şekil, KNN, VIX/DXY, öbek yoluna ek şart (hacim 2-3-4 kat, hacim kuruması, 25 ölçü — COL_KAZANC 21 Eki: hiçbiri; küçük alım mumu K7 doğrulama: BIST'te düşük hacim vekili, ABD'de yok; NVI/CMF/A-D birikim ayrışması K8: ABD'de kâr yok, BIST tabanda da aynı; hisseye özel mum küçülmesi MUM_SUKUN 22 Eki: 4 dilimde de yok; düz zemine yapışan 4-6 mum sırası MUM_SUKUN v1.2: yok). Tutanlar: alt fitil<0.12, doji, dar hafta, CDS, borç/öz, üç şart.
Açık: genç halka arz (--genc-ay 24) 3. dip bek +1.6 (n=105), 1h kapitülasyon yönü (n=112) — daha uzun 1h veri (Twelve Data) ya da günlük ölçü.
Kurallar: kod yazmadan önce "yaz"; tek dosya, üretim kalitesi; eski doğru kısımlar korunur; uzun tarama = her adımda CSV + devam; süre ilk adımdan;
test resimlerinde hisse adı yok; Drive'a Colab'dan yerinde yaz. Cemal grafiği okur, karar verir; ben ölçerim. Basit hatayı makineye buldur (kapı, test).
```
