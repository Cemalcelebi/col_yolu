# K55 — ÖN KAYIT VE KİLİT (30 Ekim 2026; Cemal'in Faz 0 onayı; koşudan önce yazıldı)

Bu belge K55 olay tanımlarını, karşılaştırma grubunu, ölçütleri, çoklu test düzeltmesini ve raporlama kurallarını kilitler. Kilit sonrası değişiklik yalnız gerçek kod / veri hatasında, eski sürüm korunarak ve gerekçesiyle yeni sürüm numarasıyla yapılır (bölüm 9). Plan: `arastirma_cikti/k55_dallanma/K55_PLAN.md` (commit 4a012ee). Cemal'in kararları (30 Ekim): kod yapısı K55/ modüller + K55.py; dönem kilidi; SEC özeti ve Tiingo listesi islenmis-veri'de sürümlü; 13F / Form 4 yalnız Faz 2'de; kapalı hücreler kapalı; olay tanımı ve ölçütler kilitli.

## 1. Evren (`K55/evren.py`)
- ABD: `COL_YOLU_ABD.cy_veri_yukle` çıktısı (V_ABD + K34 Yahoo + K34 Tiingo batanlar), `evren_disi_ABD.csv` uygulanmış (7 fon dışarıda). K54 sınıfı (`K54_SIRKET_DURUMU.csv`: 1 aktif, 2 iflas, 3 birleşme, 4 sembol / kod, 5 belirsiz, 6 doğrulanamayan) ve 4b kesim tarihi her sembole bağlanır; sınıf 6 evren dışı; 4b kesim sonrası günler dışı.
- Seri sonu işlemi (olay etiketinde ve getiri ölçüsünde): sınıf 2 → seri sonunda −%100; sınıf 3 → son kapanış, ek kayıp yok; sınıf 5 ve seri erken biten sınıf 1 → K51 kuralı (son kapanış; son 60 gün getirisi negatifse ek −%30); sınıf 4a (doğrulanamayan) → K51 kuralı.
- Fon krizi: fiyatlar 31.08.2026'da kesilir; 60 günlük pencere bu tarihi aşan gün değerlendirilmez.
- Likit gün: K51 tanımı (`cy_likit_esik`: 20 günlük işlem değeri evren alt %20 eşiği ve ≥ 1 M$, fiyat ≥ 1 $, seri başından ≥ 260 gün, evren başlangıcından sonra). Sinyal günleri yalnız likit günlerdir.
- Avrupa (V_AVR) doğrulama pazarı, BIST bilgi; ikisi de Faz 1'de aynı kurallarla (likit eşiği pazar başına).
- Evren sürümü = girdi dosyalarının sha256 listesi + evren_disi + K54 sınıf dosyası sha256 → `evren_surum` (raporda).

## 2. Dönem kilidi
- KEŞİF 2016-01-01 → 2021-12-31; İÇ DOĞRULAMA 2022-01-01 → 2023-12-31; BAĞIMSIZ 2024-01-01 → 2026-06-05 (son giriş; 60 gün pencere 31.08.2026'ya sığar); İLERİ ≥ 2026-09-01 (Mart 2027'de).
- Özellik seçimi, eşik keşfi, dallanma kararı yalnız KEŞİF'te. İÇ DOĞRULAMA adayların dayanıklılığı için. BAĞIMSIZ, bir hücre ailesi için yalnız aday ve ölçüt kilitlendikten sonra ve bir kez açılır; açıldığı tarih ve commit `K55_BAGIMSIZ_ACILIS.csv`'ye yazılır. Açılmış dönem tekrar "bağımsız" sayılmaz.
- Purging: olay penceresi (60 / 120 / 250 gün) dönem sınırını aşan olaylar bir sonraki döneme sızmaz: olay günü dönem içindeyse olay o döneme aittir; dönem sınırından önceki son 60 gün içindeki olaylar eğitim-benzeri kullanımlarda atılır (purge 60), embargo 10 gün.

## 3. Olay tanımları (geriye doğru yöntem; keşif amaçlı; sabit)
- Giriş fiyatı: olay gününden sonraki ilk işlem günü açılışı (O[t0+1]). Y60: C[t0+60] / O[t0+1] − 1 ≥ +0,30. Y120: 120. gün, ≥ +0,50. Y250: 250. gün, ≥ +1,00. (Bilgi sütunu: pencere içinde en yüksek kapanışla ulaşılan en büyük getiri.)
- Olay günü t0 = pencerenin ilk günü (sinyal günü); yalnız likit günler. Bir sembolde olaylar örtüşmez: t0'dan sonra t0 + ufuk gününe kadar yeni olay yok (ilk olay alınır). Üç ufuk ayrı olay kümeleridir.
- Pencere seri sonunu aşıyorsa olay tanımsız (ne olay ne olay değil); seri sonu kesimi (sınıf 2 / 3 / 5) yalnız getiri ölçüsünde uygulanır. Olay günü fon krizi kesimini aşan pencereler tanımsız.
- Aynı olayın birden fazla sayılması: sembol × t0 tekil; örtüşme kuralı; sembol değişimi / kod yeniden kullanımı (K54 4b kesim) sonrası günler yok. Denetim: `olay_tanimlari.olay_tekillik_denetimi` (yineleme = 0, örtüşen pencere = 0).

## 4. Olay öncesi pencereler ve değişkenler
- Olay öncesi pencereler: 5, 10, 20, 40, 60 işlem günü (t0 − p … t0). Değişken t0 gününe kadar olan veriyle hesaplanır (t0 dahil); `sizinti.kesme_testi` her değişken fonksiyonu için zorunlu (seri t0'da kesilince aynı değer).
- Her hücrenin değişkeni önce `K55/hucreler.py`'de tanımlanır (ad, formül, pencere), sonra koşulur; tanım sonradan değişmez (yeni tanım = yeni hücre kimliği, ör. D01-S01b).

## 5. Karşılaştırma grubu (sabit)
- Aynı gün (±0 gün olay öncesi yöntemde; eşleşmiş ileri yöntemde ±10 işlem günü), aynı oynaklık ondalığı (vol60, gün içi evren sıralaması), aynı likidite üçlüsü (log işlem değeri 20 gün), aynı sektör (sektor_ABD.csv; bilinmiyorsa sektör şartı yok), aynı rejim (SPY 200 gün üstü / altı), |dd250 farkı| ≤ 0,10; hisse farklı; en yakın k = 5 (standartlaştırılmış dd250, vol60, log_dv20, r60, ar20 uzaklığı). K51 v1.2 `cy_v12_eslestir` ile aynı mantık; K55'te yeniden yazılır ve sentetik testle doğrulanır.
- Olay öncesi yöntemde (A) karşılaştırma: aynı tarihte olay olmayan hisseler (tanımsızlar hariç), aynı hücrelerle ağırlıklandırılmış.

## 6. Ölçütler (hücre × dönem; sabit)
- Asgari: n ≥ 30 olay (A) / n ≥ 30 sinyal (B) / n ≥ 30 değişim noktası (C); altı VERİ YETERSİZ. Değişken eksik payı > %20 → VERİ YETERSİZ.
- A etki: |Cohen d| ≥ 0,20 ve bootstrap (ay kümeli, 2.000) %95 aralığı sıfırı dışlıyor; AUC ≥ 0,56 veya ≤ 0,44.
- B etki: üst (ya da alt; yön önceden hücrede yazılır) beşte bir sinyal; FI_OLCUT eşli fark r60 ≥ +0,05, ay kümeli alt uç > 0, hisse × çeyrek kümeli alt uç > 0, 10 yuvalı slot portföyü 200 rastgele portföyün %90'ından büyük, maliyet sonrası (K51 komisyon + kayma) eşli fark > 0.
- C: değişim noktası (CUSUM, eşik h = 4σ, pencere 250) olaydan önce 60 gün içinde; lift = P(olay | değişim) / P(olay) ≥ 1,3; yanlış pozitif = değişim olup olay olmayan payı raporlanır.
- Tekrar: işaret keşif döneminde en az 5 / 6 yılda aynı. Rejim: BOĞA ve AYI alt kümelerinde (n ≥ 30 olanlarda) işaret aynı.
- Durum: KEŞİF = keşif döneminde A veya B ölçütleri (FDR sonrası) + tekrar + rejim; DERİNLEŞTİR; DOĞRULAMA BEKLİYOR = iç doğrulamada da geçti; DOĞRULANDI = bağımsız dönem + AVR geçti; REDDEDİLDİ; VERİ YETERSİZ.

## 7. Çoklu test
- Aile = ana dal (10 aile). Hücre içi varyantlar (5 pencere × 3 olay × yön) Holm; aile içinde hücre başına en iyi düzeltilmiş p ile BH-FDR %10. Bütün varyantlar `K55_VARYANTLAR.csv`'de; başarısız olanlar silinmez. DOĞRULAMA BEKLİYOR adayları için PBO ve Deflated Sharpe (K51 yöntemi) ayrıca.

## 8. Raporlama (her koşu)
- Koşu kimliği = tarih-saat + git commit + evren sürümü + veri paketi sha256 listesi. Çıktılar: `K55_HUCRE_SONUC.csv`, `K55_VARYANTLAR.csv`, `K55_ADAYLAR.md`, `K55_VERI_KAPSAMI.md`, `K55_COKLU_TEST.csv`, `K55_RAPOR.md`; başarısız hücreler aynı tabloda, durum sütunuyla; hiçbir satır silinmez.
- Faz 0 çıktıları: `K55_FAZ0_RAPOR.md`, `K55_VERI_KAPSAMI.md`, `K55_VERI_KALITESI.csv`, `K55_EVREN.csv`, `K55_OLAYLAR.csv.gz` (olay tablosu), `K55_SIZINTI_TESTI.md`.

## 9. Değişiklik kuralı
- Kilit sonrası ölçüt / olay tanımı değişmez. Gerçek kod veya veri hatası: eski sürüm dosya ve sonuçları kalır (git), yeni sürüm (ONKAYIT_K55 v1.1 …) gerekçesiyle eklenir; etkilenen hücreler yeniden koşulur ve iki sürüm yan yana raporlanır.

## 10. Kilit öncesi denetimler (Faz 0'da kanıtlanır; `test_k55.py` + `sizinti.py`)
- Gelecek bilgisi sızıntısı: (a) kesme testi: her değişken t0'da kesilmiş seride aynı değeri verir; (b) olumlu kontrol: geleceğe bakan yapay değişken (t0+60 getirisi) pipeline'da çok büyük etki verir (dedektör çalışıyor); (c) olumsuz kontrol: rastgele değişken etki vermez; (d) olay etiketi yalnız t0+1 … t0+ufuk verisinden; (e) eşleşmiş kontrol yalnız t0'a kadar bilinen özelliklerle.
- Aynı olayın birden fazla sayılması: tekillik ve örtüşme denetimi (0 olmalı).
- Delist ve sembol değişimi: K54 sınıfı ve kesim tarihi her sembolde; sınıf 6 dışarıda; seri sonu işlemi 1. bölümdeki kural.
- Karşılaştırma grubu: 5. bölüm; sentetik testle (bilinen eşleşme) doğrulanır.
- Çoklu test: 7. bölüm. Asgari olay sayısı: 6. bölüm. Başarısız raporlama: 8. bölüm.
