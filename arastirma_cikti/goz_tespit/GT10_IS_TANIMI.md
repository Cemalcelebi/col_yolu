# GOZ_TESPIT EK 10 İŞ TANIMI — KURAL-4: beş işaretli setten, SETE GÖRE DIŞARIDA sınanmış tespit kuralı (28 Kasım 2026)

Yazan: ana model. Durum: KURAL-3 (eski puan üst %10 + YER + ZAMAN) üç sete elle uyduruldu; örneklem içi %81 ✓, yeni sayfalarda %64 (GT5) ve %40 (GT9; Ç279); birikimli 26 yeni sayfada 13 ✓, 8 erken. Rastgele 22 sayfada 1 ✓. Soru: elimizdeki 122 işaretli sayfayla, hiç görmediği sette de Cemal'in gözünü tutan bir kural çıkıyor mu; çıkmıyorsa bunu dürüstçe söylemek. BU İŞTE GETİRİ YOK: hiçbir sayfanın sonrası hesaplanmaz, okunmaz.

## 0. Kesin kurallar
- Başlamadan `python IZ_KARNE.py kontrol istanimi` çıktısını oku; ön kayıtta her satırı EVET / UYGULANMAZ + kanıtla doldur; ölçüm komutu koşmadan önce `IZ_KARNE.ik_kontrol_kapisi(onkayit_yolu)` çağrılır.
- YASAK DOSYALAR (dokunma; yalnız oku): IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, cemal_*.json, GT*_onay_anahtar.json, goz2/ (yalnız import), GOZ_TESPIT.py ve öteki modüller + testleri (yalnız import). `git add -A` / `commit -a` yasak; yalnız kendi dosyalarını ekle. Push yalnız `ccr-82c0570b-j2nhsg`; reddedilirse fetch + merge. Commit mesajına model adı yazma. .csv ve .png gitignore'da: tablolar .json.
- Veri <= 2022-12-31; kitaplık sayfaları (kaynak 'tam') bit tarihinde kesilir (uc_set.tablo'daki gibi). Ölçüler yalnız <= t barlarını kullanır (testle kanıtla: t'den sonraki barlar değişince ölçü değişmez).
- Kod: yeni tek dosya `GOZ_KURAL4.py` (repo kökü; KURAL_MOTORU düzeni, tam hata yakalama, loglama; çakışma kapısı) + `test_goz_kural4.py`. Ölçü tanımları KOPYALANMAZ: `arastirma_cikti/goz_tespit/goz2/uc_set.py` içindeki `olc`, `veri`, `auc` import edilir (beş set için tablo kurma senin kodunda). Komutlar: `tablo` (beş set ölçü tablosu), `onkayit`, `kos` (set dışı sınama + karıştırma), `rapor`, `olay` (kuralı aday havuzuna uygula).
- Sıra: (1) kod + test commit; (2) GT10_ON_KAYIT.md (etiket - ölçü ilişkisi hesaplanmadan ÖNCE; yalnız sayımlar: set x sınıf, set x kol, ölçü eksikleri) commit + push; (3) ölçüm bir kez; (4) rapor commit + push.
- Bulduğun her hata raporda 'HATA' başlığında; 'KONTROL LİSTESİ' başlığı zorunlu. Defter satırı önerini rapora yaz (deftere ben işlerim).

## 1. Veri
Setler (anahtar / işaret; hepsi arastirma_cikti/goz_tespit/): GT1 (GT_onay_anahtar.json / cemal_gt_onay.json), GT3, GT4, GT5, GT9 (GTn_onay_anahtar.json / cemal_gtn_onay.json). Etiket alanı `sinif4`: EVET / KISMEN / ERKEN / HAYIR. GT9 s. 1 işaretsiz: dışarıda. Beklenen: 30 + 28 + 20 + 21 + 23 = 122 sayfa (tutmazsa dur, yaz). Kol alanı anahtarda (`kol`; RASTGELE ve KITAPLIK kolları ayrı).
Ölçüler: uc_set.olc'nin döndürdüğü bütün alanlar (cetvel 12 ölçü, Y / M / S / B / Z, DIPTEN_BAR, SON10_EGIM, SON_DIP, SON5_YER, UST_YARI, P_* ...). İstersen, ön kayıtta tanımını yazarak en çok 6 yeni ölçü ekle (Cemal'in sözleriyle: 'düşüş bitmeli', 'daha derin dip yok', 'son bölümde dipler yukarı parabol', 'küçük mum', 'dip savunması'); hepsi <= t.

## 2. Hedefler
- H1 (asıl): EVET'i ötekilerden ayıran kabul kuralı; bütün sayfalar.
- H2: EVET - ERKEN ayrımı (kodun seçtiği, rastgele olmayan sayfalar): tek ölçü, set dışı AUC.

## 3. Yöntem (hepsi ön kayıtta, sayı görmeden)
- SETE GÖRE DIŞARIDA (5 kat): dört setten öğren, beşincide sına; bütün seçimler (ölçü, yön, eşik, şart sayısı) yalnız eğitim setlerinde.
- Aileler (basitten karmaşığa): A tek ölçü + eşik; B en çok 3 şartlı VE kuralı (ileri seçim; aday eşikler eğitim yüzdelikleri); C L2 lojistik, en çok 4 ölçü (ölçü seçimi eğitim içinde), kabul eşiği eğitimde ✓ payı >= %70 veren en düşük eşik. Ayrıntıyı (amaç fonksiyonu, en az kabul payı) ön kayıtta sabitle.
- Bazlar: KURAL-3 (Y ve DIPTEN_BAR >= 0,5; D1 sayfalarında) ve 'hepsini kabul'. KURAL-3 için GT1 / GT3 / GT4 örneklem içidir: karşılaştırmayı ayrıca yalnız GT5 + GT9 sayfalarında da ver.
- Değerlendirme (set dışı, havuzlanmış + set set): kabul sayısı; kabul içinde ✓ / K / erken / değil payı; rastgele kabul; ✓ yakalama payı; ✓ payı için sayfa düzeyi bootstrap %95 aralığı (2.000).
- Yanlış keşif: etiketleri SET İÇİNDE 200 kez karıştır, bütün hattı (A-C + en iyiyi seçme) yeniden koş; gözlenen en iyi set dışı ✓ payı karıştırma dağılımının %95'ini geçmeli.
- Seçim yanlılığı: GT5 / GT9 sayfaları KURAL-3 ile seçildi (ölçü aralığı dar); set set tabloyla göster, yorumla.

## 4. Karar (Ç279'da önceden yazıldı; değişmez)
- ADAY KURAL: set dışı kabul >= 25 sayfa ve en az 4 sette kabul var; kabul içinde ✓ payı >= %70; erken payı <= %20; rastgele kabul <= 1 / 22; GT5 + GT9 sayfalarında KURAL-3'ten >= 10 puan iyi; karıştırma %95'inin üstünde. Birden çok aile geçerse EN BASİT olan.
- H2: tek ölçü set dışı AUC >= 0,70 ve en az 4 sette aynı yön => 'erken ayırıcı adayı'.
- Hiçbiri geçmezse: 'KURAL YOK (bu ölçülerle)'; en yakın üç adayı ve neden kaldıklarını yaz. Etiket: tespit işi; 'iz' sözü yok.

## 5. Olay listesi (kör set için; getiri yok)
- Geçen kural (yoksa: EN İYİ ADAY, açıkça öyle adlandırılmış) beş setin tamamıyla aynı yöntemle yeniden kurulur; eşikler `arastirma_cikti/goz_tespit/gt10_kural4.json`.
- Aday havuzu: KURAL-3'ün D1 havuzu (GOZ_TESPIT k3esles / k3olay aşamasındaki D1 pencereleri; ABD ve BIST; 2016-22; hisse başına çakışmasız). Kuralı uygula; olay listesi `/root/.kasa/ham/goz_tespit/k4/k4_olay.pkl` (pazar, sembol, s, t, L, kabul eden kural, KURAL-3'e de uyuyor mu); sayım tablosu rapora (pazar x dönem; KURAL-3 ile kesişim). Beş sette gösterilmiş (sembol, pencere) çiftleri işaretlenir (`gosterildi` sütunu).

## 6. Teslim
GOZ_KURAL4.py, test_goz_kural4.py (sentetik: gömülü kuralı set dışı bulur; karıştırılmış etikette bulmaz; t sonrası barlar ölçüyü değiştirmez; sayım 122), GT10_ON_KAYIT.md, GT10_RAPOR.md (tek sayfa özet + tablolar + KONTROL LİSTESİ + HATA + defter önerisi), gt10_ozet.json. Raporun başında düz dille üç satır: kural var mı; set dışı ✓ payı kaç; en büyük kaçak ne.
