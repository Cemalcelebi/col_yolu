# HAKEM TURU 4 ve 5 — U DİP HAVUZU, KOTASIZ RASTGELE 40 + 40 — İŞ TANIMI
Yazan: ana model, 19 Kas 2026. Cemal: "kota filan istemem; bulduğu rastgele numaralar olsun; kaç tane buldu (örn. 300), ilk 40 + 40 iki parça halinde rastgele seç; sonra verdiğimiz dersler ışığında tekrar koşup testlere devam edelim."
Yasaklar: 4. / 5. tur YAPI_HEDEF iş tanımlarıyla aynı (defterler, tur/1-3 içerikleri, üretim zinciri; `git add -A` yok; push yok; çakışma kapıları; e-posta / anahtar yok). `python IZ_KARNE.py kontrol istanimi` tablosu raporda; 'HATA' başlığı zorunlu.

## 1. HAVUZ (T1.6)
- Olay: olay_Y1.csv.gz (OC tekil) satırı VE Ş1 DİPTE (F15 <= 0,25 VE F17 <= -0,20; ozellik_Y1.csv.gz) VE Ş9 U DİP (ozellik_Y1_s9.csv.gz F24-F29, YH_ESIK Y11 eşikleri aynen). Hat net (Ş2) ŞART DEĞİL. Bütün dönemler (2016-22 DAHİL, 2023, 2024-26); giriş <= kriz - 30 gün. Ana modelin sayımı: 117 olay (ABD 54, AVR 16, BIST 47).
- Gösterilmiş olay / hisse dışarıda (300'lük örneklem, hakem seti, TUR 1-3 anahtarları, S7 PDF'indeki 50 olay: s7_bolge_pdf.s7b_olaylar(104)). Hisse başına en çok 2 olay (sembol_azami 2).
- Tek permütasyon (tohum_taban + 4), PAZAR / DÖNEM KOTASI YOK: ilk 40 = TUR 4, sonraki 40 = TUR 5 (kalan azsa kalan kadar; sayı rapora). İki turun anahtarları aynı anda yazılır (tur/4, tur/5); TUR 5 PDF'i üretilir ama Cemal'e TUR 4 yanıtından sonra gönderilir (ana model).
- Rapora: havuz büyüklüğü pazar x dönem, gösterilmiş çıkarılınca kalan, TUR 4 / TUR 5 bileşimi (pazar x dönem; parmak F19 bilgi).

## 2. SAYFA (T1.6; ge_tur_sayfa_png'ye yeni parametreler; TUR 1-3 çıktıları DEĞİŞMEZ: yeniden üretim kapısı bayt bayt)
- Kör: veri t'de kesik, 120 bar, hacim; S6 bölgesi + hat (mavi); S7 yakın tavan F21 (kırmızı kesik; ozellik_Y1_s7); Ş9 çanak uyumu (mor kalın kesik, [t-40, t-1]) + uyum dibi x* (mor nokta); pencere başı ince mor çizgi. Hisse adı / tarih YOK, pazar var. Başlık 'HAKEM TURU 4 — Sayfa k / 40 — KÖR'.
- Sorular: A) 'Kodun U / bölge çizimi doğru mu: ✓ / X'; B) 'Bu mumdan girilir mi: ✓ OLUR / X OLMAZ / ? BELİRSİZ'.
- PDF: tur/4/TUR_4_KOR.pdf, tur/5/TUR_5_KOR.pdf (<= 12 MB; sızıntı kapısı 0).

## 3. ÖLÇÜM UYUMU
- `tur olc --no 4 / 5` 40 sayfa ve 2016-22 dönemini desteklemeli (dönem süzgeci kaldırılır / genişletilir; hücre 'dönem' sütunu satır dosyasında). Karar ölçüsü aynı (15 g kapanış +%5 stop'tan önce; üç cetvel bilgi; 'hep OLMAZ' tabanı). Model etiketi ayrı kör ajanla (ana model başlatır) `tur model --no 4` ile mühürlenir.
- TUR_DEFTERI.md'ye TUR 4 / 5 açılış bölümü (T1.6, tohum, havuz, bileşim); TUR 1-3 bölümleri değişmez.
- Testler: test_goz_etiket.py'ye T1.6 testleri (havuz tanımı, kotasız permütasyon, 40 + 40 ayrık, gösterilmiş dışarıda, TUR 1-3 yeniden üretim).

## 4. ÇIKTI ve COMMIT
GOZ_ETIKET.py, test_goz_etiket.py, tur/4/{TUR_4_KOR.pdf, tur_4_anahtar.json}, tur/5/{TUR_5_KOR.pdf, tur_5_anahtar.json}, TUR_DEFTERI.md. PNG'ler scratchpad tur4_png/ ve tur5_png/ (No_k.png). Commit mesajı: "TUR 4 / 5 açılışı: U dip havuzu (dipte + Ş9), kotasız rastgele 40 + 40 (T1.6)" + sonda:
  Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01F7vgWZPNpBhrsGQEHDtRis
RAPOR: havuz sayıları, iki turun bileşimi, kapılar (sayfa sayısı, sızıntı, TUR 1-3 bayt bayt), test sayısı, commit, HATA, KONTROL LİSTESİ, Colab notu.
