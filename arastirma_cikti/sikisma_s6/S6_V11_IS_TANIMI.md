# İŞ TANIMI — S6 TABAN v1.1: S7 fikirlerinin entegrasyonu (Cemal, 16 Kas 2026: 'uygun bulursan entegre et')

Kaynak: Cemal'in gönderdiği 'COL S7 BÖLGE KUTUSU' kullanım metni (kod elimizde yok; yalnız metin). Ana model kararı: 4 fikir S6'ya alınır, kalanlar alınmaz. S6 ölçüm tanımı değişmediği yerler aynen kalır; her yeni şart / değişiklik Python referans + Pine'da BİREBİR ve tasarım sınaması yeniden koşulur (16 etiket; mevcut 13/16 taban çizgisi; kötüleşirse yeni şart varsayılan KAPALI kalır ve rapora yazılır).

## YASAKLAR
Defter dosyaları (IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md), COL_v1.py, takip.py, SIKISMA_*.py, ORTAK_CETVEL.py, COL_S5_OBEK*.pine değişmez. git commit / push yok. E-posta / anahtar yok. Değişecek: S6_TABAN.py (v1.1), test_s6_taban.py (yeni testler), arastirma_cikti/sikisma_s6/COL_S6_TABAN.pine (+ ASCII), PINE_S6_NASIL.md, S6_TASARIM.md (v1.1 bölümü ekle; v1.0 bölümü silinmez), s6_tasarim.json (v1.1 ayrı anahtar).

## DEĞİŞİKLİKLER (Python ve Pine aynı tanım)
1. NORMAL GÜN REFERANSI (S7 fikri 1): (4) küçük mum şartında ATR%250, pencereden ÖNCEKİ 250 geçerli bar üzerinden hesaplanır (pencere [t-n+1, t] ise referans [t-n-250, t-n]); 250 bar yoksa en az 120 bar, o da yoksa şart ölçülemez (pencere geçersiz). Hesap: TR/C_önceki kümülatif toplamıyla O(1) her n için. Girdi `refOnce = true` (false: v1.0 davranışı, t'deki ATR250).
2. BOLLINGER DARALMASI (S7 fikri 2; Cemal Ç184 'bütün bölgelerde şart'): (6) BB(20, 2σ) genişliği (4σ/SMA) pencerenin SON gününde, önceki 250 günün yüzdeliğinde <= bbEsik (varsayılan 0,20; SIKISMA_OBEK tanımı, ta.percentrank KULLANMA, 'önceki 250 BB genişliğinden bugünküne <= olanların payı'). Girdi `bbSart = true`. Tasarım sınamasında bbEsik ızgarası {0,15; 0,20; 0,30; kapalı}: etiket puanı v1.0'ın (13/16) altına düşüyorsa varsayılan KAPALI, düşmüyorsa en sade tutan.
3. ÇİZİM — ONAY GÜNÜ ve KESİK KISIM (S7 fikri 3): kutunun ilk tespit edildiği gün (n ilk kez >= nMin olduğu gün) = ONAY günü; mor elmas (plotshape diamond) basılır; kutunun onay gününden ÖNCEKİ kısmı (geriye uzatma; o günlerde bilinmiyordu) ayrı bir kutu nesnesiyle kesik kenarlı ve çok soluk dolguyla çizilir; onaydan sonraki kısım dolu. Tabloya 'onay günü' satırı.
4. SÖNME (S7 fikri 4): kutu açıkken bir gün hiçbir n şartları sağlamıyorsa ve AL / KIRILDI yoksa kutu 'SÖNDÜ' diye kapanır: gri küçük etiket 'sonme' (mum üstü) ve kutu kenarı griye döner. Python'da bolge_son_tur sütunu: AL / KIRILDI / SONDU / ACIK.
5. TARİH ETİKETLERİ: kutunun ilk ve son mumunun tarihi küçük yazıyla (label, size.tiny) kutu altına; label sayısı max_labels_count=500 ile sınırlı, eskiler silinir.
6. ALINMAYANLAR (yaz): ±%1 kırılım payı (S6: AL = kapanış > tavan; KIRILDI = kapanış < dip x 0,98), Lmax 80 (S6 nMax 70 kalır), eğim şartı (S6'da yok; sakin şartı var), getiri etiketi (zaten yok).

## TESTLER / SINAMA
- test_s6_taban: yeni şartlar için sentetik testler (referans ATR pencere dışı; BB yüzdelik; sönme; onay günü), önek değişmezliği yine fark 0, v1.0 kipiyle (refOnce=false, bbSart=false) eski sonuçların BİREBİR aynı kaldığı testi (16 etiket çıktısı v1.0 ile aynı).
- Tasarım sınaması v1.1: 16 etiket (CEMAL_COL_KURALLARI.md tablosu; KNFRT etiketi 'tarih yanlış, Cemal'den beklenir' notuyla puan dışı) x bbEsik ızgarası x refOnce {true, false}; S7 metnindeki ek örnek: CCOLA 2-20 Ekim 2025 kutusu var mı; sonuç tablosu ve seçim gerekçesi; evren sayımı (hisse-yıl başına bölge ve AL; v1.0 6,9 / 3,3 ile kıyas; SIKLIK: azalıyor mu).
- Pine: v1.0'daki derlenen kalıplardan ayrılma; yeni nesne türleri (label.new, box kesik kenar: border_style=line.style_dashed, plotshape diamond) Pine v5 imzasıyla; iki kez satır satır gözden geçir; ASCII kopya doğrulamalı. Python-Pine birebirliği: Pine aynası fonksiyonu güncellenir ve 4 gerçek hissede fark 0.
- Rapor: S6_TASARIM.md 'v1.1' bölümü (ÖZET, değişiklikler, ızgara, etiket tablosu, evren sayımı, Pine riskli satırlar, KONTROL LİSTESİ, HATA, ÖNERİLEN DEFTER METNİ).
