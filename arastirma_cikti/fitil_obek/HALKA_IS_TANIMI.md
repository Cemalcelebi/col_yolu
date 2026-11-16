# İŞ TANIMI — FİTİL ÖBEĞİ: HATA NEREDE? (Cemal, 16 Kas: 'kesin bir tanı; kod ya tam şeklimi almadı, ya algılamadı, ya yanlış doğruladı; nerede hata yaptığını ölçmeliyiz')

Üç halka ayrı ayrı sınanır. Ç187 (FITIL_OBEK.py) temel: S+ / S- tanımı, olay dosyası (/tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/fitil_obek/olay_ana.csv.gz), rapor arastirma_cikti/fitil_obek/RAPOR.md. Cemal'in sözlü tanımı: 'alt fitil küçük / yok, üst fitil biraz uzun (kısa), has yukarı çıkma mumları, birkaçı yan yana öbek olunca' — PAPIL 13 Kas - 9 Ara 2025 (ölçülen: alt fitilsiz bar payı 0,47, üst fitil medyan 0,44, kapanış konumu 0,17, yeşil payı 0,26, küçük mumlar); DGXX Eki-Kas 2026 tersi.

## YASAKLAR
Defter dosyaları, FITIL_OBEK.py, S6_TABAN.py, SIKISMA_*.py, ORTAK_CETVEL.py değişmez (yalnız import). git commit / push yok. E-posta / anahtar yok. Yeni: FITIL_KOR.py (tek dosya, çakışma kapısı), arastirma_cikti/fitil_obek/{KOR_SET_ON_KAYIT.md, FITIL_KOR_SET.pdf, kor_anahtar.json (gizli; PDF'te hisse / tarih / sonuç yok), HALKA_RAPOR.md, halka_sonuc.json}. Eşikler önceden yazılı; sonuç görülünce değişmez.

## HALKA 1 — TANIM (bağlam): S+ yalnız TABAN İÇİNDE
- S6_TABAN.s6_taban (v1.1 varsayılanları) ile her hissede açık bölge günleri; S+ (Ç187 tanımı) olan günler iki gruba ayrılır: TABAN İÇİ (S6 açık bölge, sınıf DİP) ve TABAN DIŞI. Aynı şekilde S-.
- Ek varyantlar (önceden yazılı, bilgi): S+ gevşek (ASİM >= 0,10, alt fitilsiz payı >= 0,40), S+ sıkı (ASİM >= 0,30, payı >= 0,60), S+ küçük mum şartlı (pencere medyan R/C <= 0,75 x ATR250).
- ORTAK_CETVEL ile ölçüm: TABAN İÇİ S+ vs (a) eşli hisseler (cetvel) ve (b) TABAN İÇİ ama S+ olmayan günler (aynı bölge ailesi; kontrol K1). Hücreler ABD / AVR / BIST x 2023 / 2024-26 (BIST bilgi; karar ABD + AVR). Etiket kuralı Ç187 ile aynı.

## HALKA 3 — DOĞRULAMA (ölçü): kısa ufuk ve kırılım
- Her S+ günü için (taban içi ve genel): r20 eşli fark (20 gün, cetvel mekaniğiyle), 'önce ne oldu': 60 gün içinde önce S6 tavanını kapanışla kırdı mı (YUKARI) / önce dip x 0,98 altına indi mi (AŞAĞI) / ikisi de olmadı; oranlar S+ vs taban içi S+ olmayan günler; fark ve bootstrap %95. Beklenti (Cemal): YUKARI oranı S+'ta daha yüksek. S- için ayna.

## HALKA 2 — ALGILAMA (kör set)
- Kodun S+ dediği pencerelerden rastgele 30 (15 taban içi, 15 taban dışı; BIST + ABD karışık; 2016-2026-08) ve S- dediği 10 pencere, karıştırılmış sırayla, her biri bir sayfa: pencere (10 mum) + öncesi 40 mum, SONRASI YOK, hisse adı / tarih / pazar yok, fiyat ekseni oransal (normalize), hacim altta; sayfa numarası. Cemal her sayfaya 'benim mumum / değil / belirsiz' yazacak. Anahtar (sayfa -> hisse, tarih, S+/S-, taban içi mi, sonucu) kor_anahtar.json'da; PDF'te yok. Değerlendirme kodu hazır: Cemal'in yanıtları gelince `python FITIL_KOR.py olc --cevap "1:E,2:H,..."` -> kodun S+'ı ile Cemal'in gözü uyumu (E payı S+'ta vs S-'de), taban içi / dışı ayrımı.
- Ayrıca PAPIL 13 Kas - 9 Ara 2025 ve DGXX 20 Eki - 16 Kas 2026 pencereleri aynı biçimde ama ADLI ve tarihli iki sayfa (tanım kalibrasyonu için; kör sete girmez), mumların altında kodun hesapladığı alt / üst fitil payları ve S+/S- bayrağı.

## RAPOR (HALKA_RAPOR.md): ÖZET (bulgu dili: hangi halkada ne çıktı) · HALKA 1 tablosu · HALKA 3 tablosu · HALKA 2 kör set hazır (sayfa sayısı; değerlendirme komutu) · KONTROL LİSTESİ · HATA · ÖNERİLEN DEFTER METNİ. Ön kayıt KOR_SET_ON_KAYIT.md (eşikler, varyantlar, beklentiler) koşudan önce yazılır ve ik_kontrol_kapisi geçer; ana model commit edemezse sha raporda.
