# MUM_IZI EK 24 İŞ TANIMI — KODUN SEÇTİĞİ BÜTÜN BÖLGELER: aday kuralı + mum boyu kapısı, göz onayı olmadan, sonrası (15 mum) ön kayıtlı ölçüm (26 Kasım 2026)

Yazan: ana model. Cemal (26 Kas): 'burada daha fazla gerek yok; kod benim seçtiklerimin yüzde 70-90'ını seçiyorsa tamamdır'. Tespit durumu (geçmişli sayfa, 24 bölge): kodun gösterdiği bölgelerin %42'sine BENZİYOR, %75'ine BENZİYOR ya da KISMEN dedi; hakem aşaması tam ✓'de ayırmadığı için 'kod' = ADAY KURALI (MUM_IZI8 taramasının v5M havuzu) + MUM BOYU KAPISI (olağana oran <= 0,70). Kısmenlerin sayılıp sayılmayacağı Cemal'in kararı; bu yüzden bu ölçümün başlığı 'KODUN SEÇTİĞİ BÖLGELER'dir; 'kalıbın sonucu' diye yazılmaz (CLAUDE.md Tespit geçerliliği).

Soru (Cemal'in ilk sorusu): bu bölgeler sonrasında ne yapmış; eşlerinden iyi gitmiş mi. Göz ölçümünde n küçüktü (kapıdan geçen 36 bölge: eşli fark +0,6 [-4,9; +8,1]); bu iş aynı ölçüyü havuzun TAMAMINDA yapar.

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, MUM_IZI_GOZ.py, MUM_IZI_GOZ2.py ve testleri (yalnız import edilir / okunur; başka alt ajan MUM_IZI_GOZ2.py'de çalışıyor), cemal_*.json. `git add -A` / `commit -a` yasak; yalnız kendi yolların.
- KASA AÇILMAZ: veri <= 2022-12-31 (kod en büyük tarihi assert eder); 15 mumluk penceresi kesiği aşan olay ölçülmez. KASA KURALI: tek iz kasa açmaz; en iyi sonuç 'açık veride tutuyor: birleşik iz bileşeni adayı'.
- Yeni tek dosya MUM_IZI_HAVUZ.py (KURAL_MOTORU düzeni, hata yakalama, loglama, çakışma kapısı) + test_mum_izi_havuz.py. ORAN ve olay tanımları için mevcut fonksiyonlar çağrılır (ikinci tanım yazılmaz).
- Sıra: kod + sentetik test -> GETİRİSİZ SAYIM -> ön kayıt MUM_IZI24_ON_KAYIT.md (kod sha, eşik sözlüğü sha, sayımlar, güç, `python IZ_KARNE.py kontrol` tablosu satır satır EVET / UYGULANMAZ + kanıt) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> hesap -> rapor. Eşik / hücre / ölçü sonuca göre değişmez; değişirse SAPMA.
- Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Olaylar (sabit)
- KAPILI = v5M havuz olayları (MUM_IZI8 taraması; evren içi, tekil; MUM_IZI_HAKEM'in aday havuzuyla aynı kaynak) VE ORAN <= 0,70 (ORAN = bölge barlarında (H - L) / C medyanı / bölgeden önceki 120 barın medyanı; en az 40 bar; MUM_IZI_HAKEM'deki fonksiyon). Beklenen (EK 18 sayımı): günlük ~%6,6 x 4.607, haftalık ~%10,8 x 1.361 (yaklaşık 300 + 150).
- KAPISIZ (aynı bağlam kontrolü; K1) = aynı havuzun ORAN > 0,70 olan olayları (ORAN hesaplanabilenler).
- ANA ÖRNEK: sonrası daha önce ölçülmemiş KAPILI olaylar (mum_izi21_olay.csv'deki 181 bölge ve MUM_IZI22 setinin 24 bölgesi HARİÇ; onlar göz ölçümünde ayrı raporlanıyor). DUYARLILIK: hepsi dahil.
- Aynı hissede 15 bar içinde ikinci olay varsa ilki kalır (K4; havuz zaten tekilse sayısı yazılır).

## 2. Ölçü, eş, hücre (sabit)
- MUM_IZI11 tanımları aynen (MUM_IZI_GOZ fonksiyonları): giriş = bölgeden sonraki ilk geçerli bar açılışı (K5); R15 = 15. geçerli bar kapanışı / giriş - 1; stop = bölge dibi x 0,98; +%5 ve +%10 stop'tan önce (hedef payı); eş = CETVEL2 v2.2 konum eşi (aynı giriş günü / haftası, aynı kova; en az 5 eş; aynı gün KAPILI ya da KAPISIZ olayı olan hisseler eşten dışlanır); EŞLİ FARK = R15 - eş ortalaması; hücre içi SIRA; EŞLİ HEDEF PAYI = +%5 payı - eşlerin +%5 payı. Geçerli bar kuralı (K3) GOZ ile aynı.
- Hücreler: zaman dilimi (GÜNLÜK = karar; HAFTALIK = ayrı karar satırı) x pazar-dönem (giriş tarihine göre): ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22 (KARAR); BIST ve 2016 öncesi BİLGİ.
- Her hücre: n; eşli fark ortalaması ve AY KÜMELİ bootstrap %95 aralığı; ortalama sıra; hedef payı ve eşli hedef payı; 10 yuvalı slot portföyü (15 mum tut) gerçek olaylarla, her olay yerine aynı gün aynı kovadan rastgele hisse alınan 200 portföyün yüzde kaçından büyük (FI_OLCUT / ORTAK CETVEL makinesi ufuk 15 ile; repoda C2 / MU / CETVEL2 fonksiyonları varsa onlar kullanılır: UC_IZ2.py örnek); güç (delta +0,02 için; cetvel2_guc varsa o).
- KAPI ETKİSİ: KAPILI - KAPISIZ eşli fark farkı (ay kümeli permütasyon), zaman dilimine göre ve karar hücrelerinde.

## 3. Hüküm (önceden)
- Hücre TUTAR <=> n >= 30 VE eşli fark ortalaması > 0 ve bootstrap alt ucu > 0 VE ortalama sıra > 0,50 VE slot portföyü rastgele portföylerin %90'ından büyük. Aksi halde: n >= 30 ve güç >= 0,80 ise TUTMADI; değilse ÖLÇÜLEMEDİ.
- GENEL (günlük ve haftalık ayrı): dört karar hücresi TUTAR -> 'AÇIK VERİDE TUTUYOR (birleşik iz bileşeni adayı; kasa açılmaz)'; en az bir karar hücresi TUTMADI ve hiçbiri TUTAR değil -> 'TUTMADI'; ötekiler -> 'ÖLÇÜLEMEDİ' (hangi hücreler eksik yazılır). Bir hücrede pozitif, ötekinde negatif anlamlı sonuç -> 'ÇELİŞKİLİ'.
- Evren bugün yaşayanlar (K7): sonuç yukarı yanlı diye yazılır. Çoklu karşılaştırma: aile = 2 zaman dilimi x 4 karar hücresi; BH q 0,10 bilgi satırı.

## 4. Çıktılar
MUM_IZI_HAVUZ.py, test_mum_izi_havuz.py; arastirma_cikti/mum_izi/MUM_IZI24_ON_KAYIT.md, MUM_IZI24_RAPOR.md, mum_izi24_sonuc.json, mum_izi24_olay.csv.gz (olay satırları). PDF yok.
