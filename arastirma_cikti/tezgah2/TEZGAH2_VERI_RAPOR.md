# TEZGÂH 2 VERİ RAPORU (22 Kasım 2026): indirme + biçim + kalite (ölçüm yok)

Veri sonu: 2026-11-20 (indirme günü 22.11 Pazar; bugünkü bar her durumda atılır). Veri başı 2000-01-03. Fiyat kipi: yfinance `auto_adjust=True` (bölünme + temettü düzeltmeli), mevcut V_ABD / V_AVR ile aynı. Dosyalar repoda değil: `/root/.kasa/ham/veri3/` (V_ABD2.pkl 905 MB, V_AVR2.pkl 174 MB, evren2_ABD.csv, supheli.csv, kalite_*.json, oran_*.csv, atilan_*.csv, negatif_kesilen_*.csv, birim_duzeltme_AVR.csv, ham/ parçalar). Kod: `TEZGAH2_VERI.py`, test `test_tezgah2_veri.py` (31 kontrol, ağsız).

## Sayılar
- ABD evreni: nasdaqtrader (nasdaqlisted + otherlisted, 20.11.2026) 5.649 sembol (ETF / test / warrant / unit / right / preferred / tahvil / fon elendi; NYSE Arca / Cboe / IEX tek kayıtları elendi; 7.667 kayıt elendi); eski V_ABD'den listede olmayan 16 sembol 'eski_liste' olarak eklendi. İndirilen 5.649, indirilemeyen 0. V_ABD2 = 5.396 sembol (253 sembol < 150 bar: yeni halka arz / SPAC, 70'i SPAC, 11'i ADR; V_ABD ile aynı 150 bar şartı). ADR bayrağı 304, SPAC bayrağı 237 (elenmedi).
- Eski V_ABD'nin 1.411 sembolünden 1.401'i V_ABD2'de; 10'u yok: ACHV, ACVA, ATKR, BKH, CBZ, INDV, KVUE, RAMP, ROKU, WEAV (Yahoo bugün 1-70 bar veriyor: sembol değişmiş / yeniden listelenmiş; 'bar < 150').
- AVR: 581 indirildi, 0 indirilemeyen; V_AVR2 = 578. Dışarıda 3 (eski V_AVR'de vardı): FRAS.L (2007-02-27'de 43x sıçrama), LOGN.SW (2001-01-08'de 0,024x), PPH.L (2007-07-12'de 47x): 2015 öncesi açıklanamayan sıçrama kuralı (fi_avr_evren ile aynı: 80-125x dışı >= 20x sıçrama = hisse dışarıda). İstenirse 2015 sonrası kısım ayrı alınabilir (karar sonra).
- Aktif hisse sayısı (yılda en az bir bar): ABD 2000: 1.619, 2005: 1.963, 2010: 2.370, 2015: 2.939, 2020: 3.817, 2025: 5.249. AVR 2000: 331, 2005: 402, 2010: 463, 2015: 505, 2020: 550, 2025: 577.
- ABD ilk bar: 1.619 sembol 2000'de başlıyor (en eskisi), geri kalan yıllık 42-482 yeni sembol (2021 en yüksek: 482). 

## Kalite (a)-(f)
(a) Kapsam yukarıda; yıl yıl tam tablo `tezgah2_veri.json` aktif_yil / ilk_bar_yil.
(b) Eski veriyle örtüşme (ABD 1.401, AVR 578 ortak sembol): kapanış oranı (yeni / eski) hisse içi değişim katsayısı medyanı ABD 1,2e-4, AVR 1e-7; > %1 olan: ABD 1 (ARCC, %1,09: temettü ayarı farkı), AVR 1 (BCG.L %1,64: Londra birim düzeltmesi sonrası kalan fark). Open / High / Low aynı büyüklükte. Sabit çarpan farkı (oran hisse içinde sabit ama 1'den uzak): ABD ARI (0,364) ve VISN (0,727), eski veride ayar farkı; AVR CLDN.L 100 (pound / peni birim kaydı, EUR değeri aynı). EUR değeri (Close x Kur) yeni / eski medyan oranı AVR'de 578 sembolün 4'ünde %2'den uzak: BCG.L 0,979, NTGY.MC 0,980, PEY.L 0,953, UPM.HE 0,967 (temettü ayarı, 100x değil). Hacim: ABD'de hisse içi CV medyanı %1,8 görünüyor ama farkın tamamı eski V_ABD'nin son barından (2026-10-22, eski veride yarım bar: 400 sembol örneğinde 963.474 hisse-gününün 442'sinde fark, bunların 400'ü 22 Ekim) gelir; öteki günlerde hacim birebir aynı. AVR hacim CV medyanı 0.
(c) Bar geçerliliği (yeni veri): H < L = 0 (süzgeçte atılıyor). ABD toplam 19.722.165 bar; O/C aralık dışı 16 (0,0001%); hacim 0: 796.519 (%4,0; 2000: %6,5, 2013: %6,0, 2026: %1,9); H = L: 1.048.978 (%5,3; 2000: %11,7, 2026: %3,2). AVR 3.236.972 bar; O/C aralık dışı 39.270 (%1,2; 2005: %3,0, 2026: %0,17; eski V_AVR'de de var: 13.622 bar, 2015+); hacim 0: 91.887 (%2,8; 2000: %13,2); H = L: 120.831 (%3,7; 2000: %23,4). |günlük getiri| > %50: ABD 13.003 gün, bunların 229'u bölünme günüyle (+-1 iş günü) eşleşiyor (%1,8); AVR 170 gün, 4'ü eşleşiyor. Yahoo bölünme kaydı: ABD 5.138, AVR 352 olay. Eşleşmeyen büyük hareketlerin çoğu küçük hisse hareketi ya da yfinance'in bölünme kaydını almadığı olaylar; ayrıştırılmadı.
(d) Sıçra-geri dön (tek gün > %40, iki günde net < %10): ABD 1.453, AVR 47. Ters bölünme: ABD 2.644 olay, bölünme gününde > %40 süreksizlik 174 (%6,6); AVR 123 olay, 2 süreksizlik. ABD sıçra-geri sayısı 2000-2026 peni hisseleri ve düşük hacimli günlerden gelir.
(e) Aynı kapanış serisine sahip sembol çifti: 0 (ABD, AVR). Ad eşitliği (sınıf A / B): ABD 34 grup (örnek AGM / AGM-A, BATRA / BATRK, FOX / FOXA, FWONA / FWONK); AVR 0 (ad listesi yok). Bayrak, elenmedi.
(f) Hayatta kalma: evren yalnız bugün yaşayanlar. ABD'de 2000'de aktif sayı 2025'in %30,8'i (1.619 / 5.249), AVR %57,4 (331 / 577). Gerçek 2000-2010 aktif hisse sayısı için kaynak yok: BİLİNMİYOR. Batan / kottan çıkan hisseler yok; 2000-2015 sonuçları yukarı yanlıdır.
Şüpheli semboller: `supheli.csv` 1.346 satır, 1.344 sembol (ABD 1.322, AVR 22); ABD'de ağırlık sıçra-geri nedenli (1.340 satır).

## Düzeltmeler (indirme sonrası, ham veri değişmeden birleştirme kodunda)
1. Negatif / sıfır düzeltmeli fiyat: auto_adjust bazı hisselerde çok eski barları negatife çeviriyor (ABD 12, AVR 22 sembol; örnek ANA.MC 2000-01). Son bozuk bara kadar kesildi (ABD 11 sembol, AVR 22 sembol kesildi; bozuk bar son 5 bar içindeyse yalnız o bar atılır). `negatif_kesilen_*.csv`.
2. Londra birimi: eski fi_avr_evren kuralı (80-125x sıçrama => sonraki parçayı önceki birime çek) yeni 2000+ geçmişte PNL.L (2009-2011 arası geçici 100x parça) ve ANA.MC için yanlış ölçek verdi. Yeni kural: birim sıçramaları SON parçanın birimine çekilir (EUR değeri eski kuralla aynı); sonra eski V_AVR ile EUR değeri medyan oranı 100 / 0,01'e yakınsa Kur 100 / 0,01 ile düzeltilir (yalnız BCG.L: Yahoo tüm geçmişi pound veriyor). Yahoo para birimi kaydı (fast_info currency) güvenilmez (BCG.L 'EUR' diyor), kullanılmadı.

## HATA
- H1 ilk ABD indirmesi çöktü: 'NAN' sembolü pandas'ta boş (NaN) okundu (keep_default_na=False ile düzeltildi; parça 0 yazılmadan durdu, veri bozulmadı).
- H2 kalite() 'yil' KeyError (kod hatası, düzeltildi).
- H3 ilk evren süzgeci gerçek hisseleri eledi (MLP 'Common Units', REIT 'Beneficial Interest', BDC 'Closed End Fund'): istisna kuralları eklendi; kapalı uçlu fon / BDC ayrımı ad desenidir, kenarda hatalı kalan olabilir (örnek ArrowMark Financial Corp. kapalı uçlu fon geçti).
- H4 Londra birim kuralı (yukarıda, madde 2) ve negatif düzeltilmiş fiyat (madde 1): ilk birleştirmede ANA.MC, BCG.L, PNL.L yanlıştı; eski veriyle EUR karşılaştırması bulundu, düzeltildi.
- H5 eski V_ABD son barı (2026-10-22) hacmi yarım bar; eski veriyle hacim karşılaştırması bu yüzden bozuk görünür (yeni veri etkilenmez).
- Açık: 3 AVR hissesi (FRAS.L, LOGN.SW, PPH.L) dışarıda; eski V_ABD'den 10 sembol bugünkü Yahoo'da < 150 bar.

## KONTROL LİSTESİ
| Madde | Durum | Kanıt |
|---|---|---|
| K1 kontrol grubu | UYGULANMAZ | ölçüm yok |
| K2 geleceğe bakma | EVET | olay / getiri yok; veri satırı tarihi = Yahoo bar tarihi; bugünkü bar atılır (testte) |
| K3 geçerli bar | EVET | H>=L, Close>0, boş OHLC atılır; hacim 0 / H=L bar sayıları yıl yıl yazıldı, ölçü üretmez; bugünkü yarım bar atılır |
| K4 tekilleştirme | UYGULANMAZ | olay yok |
| K5 giriş fiyatı | UYGULANMAZ | ölçüm yok |
| K6 veri birimi | EVET | tek kip auto_adjust; eski veriyle oran / EUR değeri karşılaştırıldı; Londra 100x ve negatif düzeltme bulundu / düzeltildi; ters bölünme sürekliliği sayıldı |
| K7 hayatta kalma | EVET | evren yalnız bugün yaşayanlar; 2000 / 2025 aktif oranı yazıldı; gerçek sayı bilinmiyor |
| K8 örneklem / dönem | UYGULANMAZ | ölçüm yok |
| K9 ön kayıt | UYGULANMAZ | ölçüm yok; iş tanımı kodlanan standart |
| K10 ayrıştırma | EVET | nasdaqlisted / otherlisted başlıkları ve 5 örnek satır elle denetlendi; dosya sonu damgası ('File Creation Time') atlandı; ETF / test bayrağı sütunu; hisse adı süzgeci elle örneklendi (H3) |
| K11 yeniden üretim | UYGULANMAZ | ölçüm yok; sayımlar kalite json'dan; ARCC / BCG.L / ANA.MC eski veriyle elle karşılaştırıldı |
| K12 ifade | UYGULANMAZ | iz / anlamlı iddiası yok |
| K13 süreç | EVET | çakışma kapısı var; defter ve mevcut modüllere dokunulmadı; e-posta / anahtar yok (testte); Tiingo yok; /tmp/veri, /tmp/veri2, /tmp/kasa'ya dokunulmadı; veri repoda değil |
| K14 boyut | UYGULANMAZ | öneri işi değil |
