# GOZ_TESPIT EK 6 İŞ TANIMI — KIRILIM GİRİŞİ: bölge tavanı kırılınca giriş; yön (yukarı mı aşağı mı kırıyor) ve kırılım sonrası 15 bar (27 Kasım 2026)

Yazan: ana model. Gerekçe: Ç271 bölge biter bitmez girişle ölçtü (tutmadı). Cemal'in 17 Kas standardı başka: 'kod oluşumu görür; alım-satım mumu bellidir: dip tavanı kırılınca hedef başlar; giriş = kırılım mumu (ölçümde t + 1 açılış)'; ve dersi: 'dip oluşumu + dip savunması = yön yukarı'. Bu iş o ikisini ölçer. Tespit Cemal'in görsel onayını bekliyor (GT3 / GT4): bütün sonuçlar 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)' başlığıyla yazılır.

## 0. Kesin kurallar
- Başlamadan `python IZ_KARNE.py kontrol istanimi`. YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, cemal_*.json, GT*_onay_anahtar.json, goz2/, GT5_* ve gt5_* dosyaları (yalnız okunur), öteki modüller ve testleri (yalnız import). `git add -A` / `commit -a` yasak. Push reddedilirse `git fetch origin ccr-82c0570b-j2nhsg && git merge --no-edit FETCH_HEAD`.
- Olaylar DONDURULMUŞ: /root/.kasa/ham/goz_tespit/k2/k2_olay.pkl (üç kol: K2 ANA, YMSB, Y; sha GT5_ON_KAYIT.md'de; assert). Şart / eşik değişmez. Veri <= 2022-12-31 (assert). Kod GOZ_TESPIT.py'ye yeni bölüm (ÇÖL-K2 KIRILIM; komutlar k2kirsay / k2kirolc) + test_goz_tespit.py'ye testler; çalışan kısma dokunma; mevcut 26 test aynen geçer.
- Ön kayıt (GT6_ON_KAYIT.md: kod sha, tanımlar, GETİRİSİZ sayımlar, karar kuralı, dolu KONTROL LİSTESİ) getiri hesaplanmadan ÖNCE commit + push; `IZ_KARNE.ik_kontrol_kapisi` geçmeden ölçüm başlamaz; ölçüm bir kez. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI. Commit sonu yalnız ana modelin verdiği iki satır; mesaja model adı yazma.

## 1. Tanımlar (sabit)
- Bölge [s, t]; TAVAN = bölgedeki en yüksek High; DİP = en düşük Low. İzleme penceresi: t + 1 .. t + 20 (geçerli barlar; High > Low; tarih <= 2022-12-31).
- YUKARI KIRILIM günü b = izleme penceresinde Close > TAVAN olan ilk bar. AŞAĞI KIRILIM = Close < DİP olan ilk bar. YÖN = hangisi önce (20 barda hiçbiri yoksa 'kırılmadı'; pencere veri sonunu aşıyorsa 'kesik', sayım dışı).
- GİRİŞ (yalnız yukarı kırılım önce geldiyse) = b + 1 barının açılışı. R15 = girişten sonraki 15. geçerli bar kapanışı / giriş - 1 (15. bar 2022-12-31'i aşarsa KESIK). SİMETRİK İLK DOKUNUŞ: girişten sonraki 15 barda High >= giriş x 1,05 mi önce, Low <= giriş x 0,95 mi (aynı barda ikisi de varsa 'belirsiz', iki paya da girmez); aynısı %10 için. Stop yok (Ç271 dersi: stop mesafesi olay ve kontrolde farklıysa hedef payı mekanik olur).
- KONTROL 1 (yön için; K1 aynı bağlam): aynı hissenin aynı dönemdeki, aynı L sınıfındaki (20 / 40 / 80) ve Y şartını SAĞLAMAYAN havuz pencereleri (pencere paneli; evren şartları aynı); her biri için aynı YÖN kuralı. Taban = hisse-dönem-L içinde 'yukarı önce' payı; hücre tabanı olay ağırlıklı.
- KONTROL 2 (kırılım sonrası için): aynı hissenin aynı dönemdeki SIRADAN TAVAN KIRILIMLARI: Kontrol 1 pencerelerinden yukarı kırılımı önce gelenlerin b günleri (aynı giriş kuralı, aynı R15 ve simetrik ölçüler). T1k = hisse-dönem içinde bu kırılımların R15 ortalaması (en az 5 kırılım; azsa olay kontrol karşılaştırmasından düşer, sayılır). Bilgi için ayrıca T1 (bütün günler; Ç271 ile aynı).
- Aynı hisse + kolda kırılım günleri arasında < 15 bar varsa ilk kalır (olay ve kontrolde aynı kural).

## 2. Ölçüler ve karar (önceden)
- Hücreler: ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22 (KARAR); BIST iki dönem (BİLGİ). Kollar: K2 (ANA), YMSB, Y.
- TABLO A (YÖN): bölge sayısı; yukarı önce / aşağı önce / kırılmadı payları; Kontrol 1 tabanı; fark (yukarı önce - taban) ve ay kümeli bootstrap %95 GA (2.000; tohum 6); kırılıma kadar geçen bar medyanı.
- TABLO B (KIRILIM SONRASI): n giriş; TFk15 = ortalama (R15 - T1k) [GA]; medyan R15 - medyan T1k; simetrik +%5 önce payı ve Kontrol 2 tabanı, fark [GA]; +%10 için aynı; R15 < -%20 ve > +%20 payları ve tabanları; ATRP20 beşliği içinde TFk15 (yalnız >= 20 olaylı beşlikler) ve artı sayısı; bilgi: R15 - T1.
- KARAR: YÖN hücresi TUTAR <=> bölge >= 50 ve fark GA alt ucu > 0. KIRILIM SONRASI hücresi TUTAR <=> n >= 30 ve TFk15 GA alt ucu > 0 ve medyan fark > 0 ve simetrik +%5 farkının GA alt ucu > 0 ve >= 20 olaylı beşliklerin en az dörtte üçünde TFk15 > 0 (böyle beşlik 2'den azsa bu şart aranmaz, raporda yazılır). 'EMARE (yaşayan evren)' <=> ANA kol ABD'nin iki döneminde TUTAR (AVR'de olay sayısı önceden az: sayımda n < 30 çıkan hücre ÖLÇÜLEMEDİ; bu ön kayıtta açıkça yazılır). Hangi sonuç çıkarsa çıksın başlık 'DEDEKTÖRÜN BULDUĞU BÖLGELER'; K7 uyarısı zorunlu (yaşayan evren; yer şartı çok düşmüş hisseleri seçer; sonuç yukarı yanlı).
- Sağlama: iki hücrenin YÖN payı ve TFk15'i satır dosyalarından bağımsız kısa kodla yeniden üretilir.

## 3. Çıktılar
GOZ_TESPIT.py, test_goz_tespit.py; arastirma_cikti/goz_tespit/: GT6_ON_KAYIT.md, GT6_RAPOR.md, gt6_sayim.json, gt6_ozet.json. Satır dosyaları /root/.kasa/ham/goz_tespit/k2/ (repoya girmez).
