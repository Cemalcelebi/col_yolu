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

## 9. 25 EYLÜL – 18 EKİM 2026 — SON DURUM (en güncel bölüm budur)

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
- T6 (taban kırılınca çık) testle çelişiyor: tut ya da kaldır.
- Boyut çarpanları (doji/fitil/dar) yeniden doğrulama.
  Aynı işte düzeltilecek (20 Eki inceleme): `dar_hafta_olc`, segmentten önceki haftayı da segmente sayıyor ("ilk" bloğu). Bu yüzden `dar` değeri düşük çıkıyor.
  Düzeltme `dar` değerlerini değiştirir, bu yüzden tek başına yapılmayacak.
- ~~Verisi durmuş hissenin aday olması ve listeden hiç çıkmaması~~ → 20 Eki'de D11/T9 ile düzeltildi (bkz. 9.5).
- GitHub Actions günlük tarama: eski iş akışı 19 Eki 21:01'de elle kapatılmıştı. 20 Eki'de `gunluk_col_tarama.yml` adıyla yeniden kuruldu; ilk başarılı çalışma 20 Eki 21:30 (aday 43, açık 10). CDS verisi eski — güncellenmeli.
- DURDO açık pozisyonda taban serisinde.
- 9 açık pozisyonda gerçek taban yok (yedek ×0.85).
- motor_karne kâğıt işlemleri sürüyor.

---

## KISA BLOK (yeni sohbete yapıştır)

```
ÇÖL YOLU / BIST+ABD; tam özet Drive: col_tarayici/COL_OZET.md (bölüm 9 = son durum).
SİSTEM TEST AŞAMASINDA; bu MD bağlam sigortası, kural defteri değil. Tam iz + doğru metrik hesabı gelince kural olur.
GÜNCEL TESPİT (20 Eki, D12): dip çölü = bölge kuralı + dipte + yeni dip yok + imza (küçük mum, Bollinger, doji, hacim) ≥3/4. Göz testi 12/29 (D7 1/29). Taban (20 gün zirvesi kırılımı) karşısında iz değil (3/6 dönem). Çöl şekil metrikleri iz vermedi (col_ogren).
EYLÜL-EKİM 2026 FON TASFİYE KRİZİ: TERA/DSTKF/ODINE/GUNDG/TRHOL... taban serileri GERÇEK düşüş, bölünme değil. Büyük düşüşte önce COLAB_VERILER/col_tarayici/atlas/taban_serisi_izleme.csv + veri_koru_gunluk.csv.
Ekim eklemeleri: D8 fon süzgeci, D9 uzun çöl + sektör rüzgârı, D10 rüzgâr etiketi (D9b) + tarih hizası, D11/T9 verisi durmuş hisse aday olmaz, D12 dip çölü üretimde (20 Eki); takip T6 taban kırılınca çık (testle çelişiyor), T7, T8; veri_koru.
Kural: col_segment (yerel=5, ≥20 bar ≤6 ATR) → aday; kapanış>tavan×1.002 → AL; %20 → SMA20 trail; 120 bar; stop yok.
Boyut %6×CDS×borç×doji×fitil×dar×kural, max %12. Aday filtresi yok. Segment kodu değişmedi.
Gerçek sayı (tekil, ertesi açılış, 120 bar): BIST 24-26 %64/+8.9 · BIST 23 %88/+38 · ABD 24-26 %62/+8.3 · ABD 22-23 %62/+4.7.
Test setleri OB24/OB23/OBUS (BASLAT) + OBUS21 (onbellek_ABD_2022_23.pkl). Ölçüm: exec OLCUM.py → islemler_olc/dilim/kiyas/esli_kiyas.
Çakışma kapısı: ölçüm dosyası üretim adını ezerse durur. DESEN_TAM arsiv/desen/ altında, kapalı; OLCUM ile birlikte yüklenmez.
Kapananlar: sektör, momentum, onc250, konum250, taban koruması/kırılma, çöl kalitesi filtresi, tutunma/silkeleme, 4h/1h çöl ölçüleri salınım dibinde,
QMLS tahtacı/nakit/onay/dip sırası, giriş zamanlaması, stoplar, 90+ şekil, KNN, VIX/DXY. Tutanlar: alt fitil<0.12, doji, dar hafta, CDS, borç/öz, üç şart.
Açık: genç halka arz (--genc-ay 24) 3. dip bek +1.6 (n=105), 1h kapitülasyon yönü (n=112) — daha uzun 1h veri (Twelve Data) ya da günlük ölçü.
Kurallar: kod yazmadan önce "yaz"; tek dosya, üretim kalitesi; eski doğru kısımlar korunur; uzun tarama = her adımda CSV + devam; süre ilk adımdan;
test resimlerinde hisse adı yok; Drive'a Colab'dan yerinde yaz. Cemal grafiği okur, karar verir; ben ölçerim. Basit hatayı makineye buldur (kapı, test).
```
