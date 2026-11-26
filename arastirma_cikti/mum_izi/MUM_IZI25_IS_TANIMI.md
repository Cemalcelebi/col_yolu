# MUM_IZI EK 25 İŞ TANIMI — RASTGELE GÜN TABANI: bölgelerin mutlak kârlılığı, zamanlama ve seçim ayrımı (26 Kasım 2026; EK 23 ve EK 24 sonuçları ana modele gelmeden yazıldı)

Yazan: ana model. Cemal (26 Kas; 'eş = aynı gün aynı kovadaki hisseler' tanımına itiraz; yazdığı gibi): "Ama sorun şu ki benzerler eşleri aynı gün değil rastgele günlerde olmalı çünkü olay şu ki biz bu yapıları gördüğümüzde piyasa toplamı yükseliyor ise bizim başarısız sayılmadı mantıksız olur". Ana modelin okuması: aynı gün eşleriyle kıyas piyasanın o günlerdeki yükselişini siler; yapı piyasanın yükseleceği zamanlarda görülüyorsa mutlak olarak kazandırır ama eşli farkta 'başarısız' görünür. Kıyas RASTGELE GÜNLERLE de yapılmalı.

Bu itiraz haklıdır: eşli fark yalnız HİSSE SEÇİMİNİ ölçer, ZAMANLAMAYI ölçmez. Bu iş ikisini ayırır. (CLAUDE.md K1 'kontrol grubu sinyalle aynı bağlamda' kuralı seçim ölçüsü içindir ve yerinde kalır; rastgele gün tabanı ayrı bir sorunun, 'mutlak kârlılık / zamanlama'nın ölçüsüdür.)

## 0. Kesin kurallar
- YASAK DOSYALAR: IZ_DEFTERI.md, IZ_KARNE.py, CLAUDE.md, COL_OZET.md, ONERI_DEFTERI.md, arastirma_cikti/kural_defteri/, MUM_IZI_HAKEM.py, MUM_IZI_GOZ.py, MUM_IZI_GOZ2.py ve testleri (yalnız import), cemal_*.json. `git add -A` / `commit -a` yasak.
- KASA AÇILMAZ: veri <= 2022-12-31; pencere kesiği aşan giriş ölçülmez. Geleceğe bakma yok.
- Kod MUM_IZI_HAVUZ.py'ye eklenir (çalışan kısma ve EK 24 çıktılarına dokunmadan; test). Sıra: kod + test -> GETİRİSİZ SAYIM -> ön kayıt MUM_IZI25_ON_KAYIT.md (kontrol tablosu dahil) commit + push -> `IZ_KARNE.ik_kontrol_kapisi` -> hesap -> rapor. Rapor başlıkları: KONTROL LİSTESİ, HATA, SAPMA, SONUÇ, ÖNERİLEN DEFTER SATIRLARI.

## 1. Tabanlar (sabit)
Her olay için (hisse s, giriş günü t, pazar, dönem d = 2016 öncesi / 2016-19 / 2020-22, zaman dilimi, bölge uzunluğu m):
- T1 AYNI HİSSE, RASTGELE GÜN: s hissesinin aynı dönemde rastgele seçilen 200 giriş barında (olay girişine 15 bardan yakın olanlar hariç; geçerli bar; pencere kesiği içinde; yeterli bar yoksa olan kadar, en az 30) aynı tanımla R15 ortalaması ve +%5'e stop'tan önce ulaşma payı (rastgele günde stop = girişten önceki m barın dibi x 0,98).
- T2 HERHANGİ BÖLGE: aynı pazar, aynı dönem, aynı zaman diliminde bütün evrenden rastgele 5.000 (hisse, giriş barı) çekimi: R15 ortalaması / medyanı ve +%5 payı (stop: önceki 20 barın dibi x 0,98). Hücre başına tek sayı.
- PİYASA(t) = aynı pazarın bütün hisselerinin aynı giriş günü R15 ortalaması (olaylı hisseler hariç).
- Tohum 2511; çekimler raporda sayılır.

## 2. Farklar ve çıkarım (sabit)
- TOPLAM FARK = R15 - T1 (ana; ayrıca R15 - T2): 'bu bölgeler herhangi bir güne göre ne kadar kârlı'.
- ZAMANLAMA = PİYASA(t) - T2: 'bu yapılar görüldüğünde piyasa, rastgele bir güne göre daha çok mu yükseliyor'.
- SEÇİM = R15 - PİYASA(t) (eşli farkın kovasız hali; EK 24'ün eşli farkı yanında yazılır).
- HEDEF: +%5 stop'tan önce payı: olaylar / T1 / T2.
- Çıkarım: AY KÜMELİ bootstrap %95 (küme = giriş ayı; 10.000 tekrar): zamanlama birkaç takvim dönemine dayanabileceği için tek tek olay değil ay sayılır. Her tabloda: olay sayısı, FARKLI AY sayısı, en kalabalık 3 ayın olay payı.
- Örneklemler: (a) EK 24'ün KAPILI ana örneği ve duyarlılık (hepsi); (b) KAPISIZ kontrol; (c) göz ölçümü: gerçek ölçekle işaretlenen setler (set 6-9) Cemal sınıfına göre (BENZİYOR / KISMEN / BENZEMİYOR) ve kapı havuzu (set 7-9); bölge kimlikleri mum_izi23_olay.csv'den (yoksa mum_izi21_olay.csv + MUM_IZI22 anahtarı + cemal_mum_izi22_onay.json etiketi yalnız sınıf için okunur).
- Hücreler: zaman dilimi x (ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22 karar; BIST ve 2016 öncesi bilgi); ayrıca hepsi birlikte.

## 2b. PİYASA TAHMİNİ, TAKVİM ZAMANI (ek; 26 Kasım 2026; EK 23 / EK 24 sonuçları ana modele gelmeden yazıldı)
Cemal (hemen ardından; yazdığı gibi): "Çok bku asıl derdimiz piyasani yükseliş tahmin etmektir" (ana modelin okuması: asıl dert piyasanın yükselişini tahmin etmek).
- Her pazar (ABD, AVR; BIST bilgi) ve GÜNLÜK zaman dilimi için takvim serisi: g günü SAYI(g) = son 5 işlem gününde bölgesi biten KAPILI olay sayısı (bölge sonu <= g; geleceğe bakma yok); PİYASA15(g) = o pazarın bütün hisselerinin g + 1 açılışından 15. işlem günü kapanışına eşit ağırlıklı ortalama getirisi.
- Üç durum (önceden sabit): SAYI = 0; SAYI = 1-2; SAYI >= 3. Her durum için gün sayısı, PİYASA15 ortalaması / medyanı, artıda kapanan gün payı; farklar (SAYI >= 1) - (SAYI = 0) ve (SAYI >= 3) - (SAYI = 0); çıkarım AY KÜMELİ bootstrap %95 (günler örtüşen pencereli olduğu için gün değil ay sayılır). Dönemler: 2016-19, 2020-22 ayrı ve birlikte. Aynısı KAPISIZ olay sayısıyla (kontrol: kapı zamanlamaya bir şey katıyor mu).
- OKUMA: 'PİYASA YÜKSELİŞİNİ ÖNCELİYOR' <=> iki dönemde de (SAYI >= 1) - (SAYI = 0) farkı > 0 ve ay kümeli alt ucu > 0 (ABD'de; AVR aynı yöndeyse 'iki pazarda'). Tek dönemde ise 'TEK DÖNEM'; aralık sıfırı içeriyorsa 'GÖSTERİLEMEDİ'. Uyarı: düşüş sonrası dip yapıları tanım gereği düşüşlerden sonra görülür; düşüşten sonraki toparlanma ortalaması zaten yüksek olabilir: karşılaştırma satırı olarak 'pazar son 20 günde %5'ten fazla düşmüş günler' için PİYASA15 de yazılır (yapı, bu basit bilgiden fazlasını söylüyor mu).

## 3. Okuma (önceden)
- 'MUTLAK KÂRLI (rastgele güne göre)' <=> hücrede n >= 30 VE farklı ay >= 12 VE TOPLAM FARK (T1) ortalaması > 0 ve ay kümeli alt ucu > 0. Aralık sıfırı içeriyorsa 'AYRIŞMIYOR'; üst ucu < 0 ise 'RASTGELE GÜNDEN KÖTÜ'; n ya da ay sayısı yetmezse 'ÖLÇÜLEMEDİ'.
- 'ZAMANLAMA VAR' <=> ZAMANLAMA ortalaması > 0 ve ay kümeli alt ucu > 0 (aynı n / ay şartı).
- KISMEN KABUL KURALI (MUM_IZI23_EK_KURAL.md'nin Cemal'in itirazıyla güncellenmiş hali; sonuç görülmeden): KISMEN kabul sayılır <=> KISMEN sınıfı TOPLAM FARK (T1) ile 'MUTLAK KÂRLI' (n ve ay şartı aranmadan aralık kuralıyla; n < 30 ise 'ÖRNEKLEM YETERSİZ' notu). Eşli farkla okuma ayrıca yazılır; ikisi ayrışırsa ikisi de raporlanır.
- Uyarılar rapora yazılır: evren bugün yaşayanlar (iki taraf da yukarı yanlı); dönem içi piyasa yönü tabanda da var; sonuç birkaç aya dayanıyorsa (en kalabalık 3 ay payı > %30) 'az sayıda döneme dayanıyor' notu.

## 4. Çıktılar
MUM_IZI_HAVUZ.py (ek komut) + test; MUM_IZI25_ON_KAYIT.md, MUM_IZI25_RAPOR.md, mum_izi25_sonuc.json, mum_izi25_olay.csv.gz. PDF yok.
