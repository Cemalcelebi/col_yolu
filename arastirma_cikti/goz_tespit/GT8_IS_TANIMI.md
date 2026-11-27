# GOZ_TESPIT EK 8 İŞ TANIMI — KURAL-3 (eski kod + yer + zaman) asıl koda + bulduğu bölgelerin sonrası (27 Kasım 2026)

Yazan: ana model. Durum: dört kör setten sonra Cemal'in gözüne en yakın kural: D1 (eski altı ölçülü puan üst %10) + YER + ZAMAN. Örneklem içi 16 sayfada 13 ✓; yeni 11 sayfada 7 ✓ (%64; ABD 6 / 8, BIST 1 / 3); rastgele 18 sayfada 0 ✓. Cemal'in ölçütü (%70-90) henüz tam sağlanmadı: bütün sonuçlar 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı eşiğin hemen altında: yeni sayfalarda %64; kalıp hükmü değil)' başlığıyla yazılır. Cemal (27 Kas): 'devam et, bekleme'.

## 0. Kesin kurallar
- Başlamadan `python IZ_KARNE.py kontrol istanimi`. YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, cemal_*.json, GT*_onay_anahtar.json, goz2/, GT5_* .. GT7_* ve gt5_* .. gt7_* dosyaları (yalnız okunur), öteki modüller ve testleri (yalnız import). `git add -A` / `commit -a` yasak. Push reddedilirse fetch + merge.
- Veri <= 2022-12-31 (KASA açılmaz). Kod GOZ_TESPIT.py'ye yeni bölüm (KURAL-3; komutlar k3esles / k3olay / k3olc) + testler; çalışan kısma dokunma; mevcut 45 test aynen geçer.
- Ön kayıt (GT8_ON_KAYIT.md) getiri hesaplanmadan ÖNCE commit + push; `IZ_KARNE.ik_kontrol_kapisi`; ölçüm bir kez. Ön kayıtta YALNIZ getirisiz sayımlar: kol x hücre olay ve hisse sayısı, L dağılımı, ATRP20 beşliklerine dağılım, kesik sayısı. (B) tablosunun kırılım adetleri sonuca bağlıdır: ölçümle birlikte raporlanır. Bu iş tanımı ile görev mesajı çelişirse İŞ TANIMI geçerlidir. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI. Commit sonu yalnız ana modelin verdiği iki satır.

## 1. KURAL-3 (sabit; eşik değişmez)
- D1 = COL_SKOR6 PUAN_ESIT'in kendi pazarı ve L'si içindeki evren sırası >= 0,90 (GT_DEDEKTOR.md D1 tanımı AYNEN; pencere panellerindeki PUAN_ESIT).
- YER = ÇÖL-K2'nin Y şartı (kutu <= grafiğin %22'si, kutunun yeri <= 0,35, önceki 120 mumun tepesi >= kutu tavanının 2 katı; gt_k2 Y).
- ZAMAN = bölgenin en derin dibi (Low) bölgenin ilk yarısında: DIPTEN_BAR = (n - 1 - argmin(Low[s..t])) / n >= 0,5 (goz2/uc_set.py olc ile aynı).
- Birebirlik testi (k3esles): arastirma_cikti/goz_tespit/GT5_onay_anahtar.json'daki 21 sayfanın kolu (D1+YER+ZAMAN / D1+YER_ZAMANSIZ / D1+ZAMAN_YERSIZ) bu kodla aynen çıkmalı; uc_set_tablo.json'daki Y ve DIPTEN_BAR değerleriyle aynı.
- Kollar: ANA = D1 ve YER ve ZAMAN; ZAMANSIZ = D1 ve YER ve ZAMAN değil; PUANSIZ = YER ve ZAMAN ve D1 değil (eski puan bir şey katıyor mu).
- Olay: pencere panelleri (ABD, AVR, BIST; pencere sonu 2016-01-01 .. 2022-12-31; s >= 120; KIL <= 0,20; govdesiz_pay <= 0,30); aynı hisse + kolda pencere sonları arasında < 40 bar ise ilk görülen kalır.

## 2. Ölçüm (tanımlar Ç271 / Ç272 ile AYNEN; gt_k2 ölçüm fonksiyonları yeniden kullanılır)
- (A) BÖLGE SONU GİRİŞİ: giriş = t + 1 açılış; R15; TF15 = R15 - T1 (aynı hissenin aynı dönemdeki bütün uygun günleri); simetrik ilk dokunuş +%5 / -%5 ve +%10 / -%10 (stop yok); taban = aynı hissenin aynı dönemdeki bütün günlerinde aynı ölçü.
- (B) TAVAN KIRILIMI GİRİŞİ (Ç272 düzeni): bölgeden sonraki 20 barda Close > TAVAN ilk bar; giriş ertesi açılış; R15; kontrol = aynı hissenin aynı dönemdeki sıradan tavan kırılımları (T1k; en az 5); simetrik +%5 payı ve kontrol tabanı. Yön payları yalnız bilgi (konum eşlenmediği için karar değil).
- Hücreler: ABD 2016-19, ABD 2020-22 (KARAR); AVR iki dönem (n >= 30 ise KARAR, değilse ÖLÇÜLEMEDİ); BIST iki dönem (BİLGİ).
- Satırlar: n, hisse; TF15 (ya da TFk15) ortalama [ay kümeli bootstrap %95; 2.000; tohum 8]; medyan fark; simetrik +%5 önce payı, tabanı, farkı [GA]; +%10 payı / tabanı; R15 < -%20 ve > +%20 payları / tabanları; ATRP20 beşliği içinde ortalama fark (yalnız >= 20 olaylı beşlikler) ve artı sayısı.
- KARAR (önceden): hücre TUTAR <=> n >= 30 VE ortalama fark GA alt ucu > 0 VE medyan fark > 0 VE simetrik +%5 farkının GA alt ucu > 0 VE >= 20 olaylı beşliklerin en az dörtte üçünde ortalama fark > 0 (böyle beşlik 2'den azsa bu şart aranmaz, yazılır). 'EMARE (yaşayan evren)' <=> ANA kol ABD'nin iki döneminde TUTAR; (A) ve (B) ayrı ayrı karara bağlanır (iki giriş türü denendiği raporda yazılır). Ek okuma (karar değil): ANA - ZAMANSIZ ve ANA - PUANSIZ farkları.
- K7 uyarısı zorunlu (yaşayan evren; yer şartı çok düşmüş hisseleri seçer; sonuç yukarı yanlı). Sağlama: iki hücre satır dosyalarından bağımsız kısa kodla yeniden üretilir.

## 3. Çıktılar
GOZ_TESPIT.py, test_goz_tespit.py; arastirma_cikti/goz_tespit/: GT8_ON_KAYIT.md, GT8_RAPOR.md, gt8_sayim.json, gt8_ozet.json. Satır dosyaları /root/.kasa/ham/goz_tespit/k3/.
