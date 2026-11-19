# HAKEM TURU 6 — DİP SAVUNMASI + ALT FİTİL KISA + PARABOLİK U HAVUZU — İŞ TANIMI
Yazan: ana model, 19 Kas 2026. Cemal: "PDF'leri ver, ben yorumlayayım; özellikle dip savunması ve parabolik yuvarlama olanları; ilkin 40".
Yasaklar: TUR 4 iş tanımıyla aynı (defterler, tur/1-5 içerikleri, üretim zinciri; `git add -A` yok; push yok; çakışma kapıları; e-posta / anahtar yok). Kontrol tablosu raporda; 'HATA' zorunlu.

## 1. HAVUZ (T1.7)
- Olay: olay_Y1.csv.gz satırı VE Ş3 dip savunulmuş (F2 >= -0,01) VE Ş5 alt fitil kısa (F4 <= 0,25) VE Ş9 U dip (ozellik_Y1_s9 F24-F29, YH_ESIK Y11 eşikleri aynen) VE F15 <= 0,50 (120 günün alt yarısı; Ş1 dipte ŞART DEĞİL, Ş1 bilgi sütunu). Bütün dönemler; giriş <= kriz - 30 gün. Ana modelin sayımı: Ş3+Ş5+Ş9 konumsuz 715 (gösterilmemiş 505); F15 <= 0,50 ile sayı rapora.
- Gösterilmiş olay / hisse dışarıda (300 + hakem + TUR 1-5 + S7 PDF 50); hisse başına en çok 2 olay; tek permütasyon (tohum_taban + 6), KOTASIZ: ilk 40 = TUR 6 (kalan havuz rapora; TUR 7 için saklanır, PDF üretilmez).
- Rapora: havuz pazar x dönem, bileşim, Ş1 (dipte) olan sayfa sayısı (bilgi).

## 2. SAYFA: T1.6 ile AYNI (kör; S6 bölge + hat, S7 yakın tavan, Ş9 çanak + x*; A / B soruları; 'HAKEM TURU 6 — Sayfa k / 40 — KÖR'; kapakta YOK ama ilk sayfanın üst notunda 'havuz: dip savunulmuş + alt fitil kısa + parabolik U, 120 günün alt yarısı' yazılır — hisse adı / tarih yok). PDF tur/6/TUR_6_KOR.pdf, anahtar tur/6/tur_6_anahtar.json; PNG'ler scratchpad tur6_png/.
## 3. ÖLÇÜM: `tur olc --no 6` T1.6 gibi çalışır. TUR_DEFTERI.md'ye TUR 6 açılış bölümü. Testler: test_goz_etiket.py'ye T1.7 (havuz tanımı, kotasız, gösterilmiş dışarıda, TUR 1-5 yeniden üretim kapısı bayt bayt).
## 4. COMMIT: GOZ_ETIKET.py, test_goz_etiket.py, tur/6/{TUR_6_KOR.pdf, tur_6_anahtar.json}, TUR_DEFTERI.md; mesaj "TUR 6 açılışı: dip savunması + alt fitil kısa + parabolik U havuzu (T1.7), kotasız 40" + Co-Authored-By / Claude-Session satırları.
RAPOR: havuz sayıları, bileşim, kapılar, test sayısı, commit, HATA, KONTROL LİSTESİ, Colab notu.
