# İZ DEFTERİ — BIST, ölçülmüş bulgular (güncelleme: 21 Ekim 2026, 12:10)

Kural: bir iz ancak (1) n ≥ 100, (2) 2017–21 ve 2022–26 dönemlerinde AYNI yönde, (3) birden fazla ölçüde
(ortalama VE medyan) aynı yönde çıkarsa "GEÇERLİ" sayılır. Tek testte çıkan "ADAY", başka testte tersine dönen "ÇÜRÜDÜ".
YENİ KURAL (18:30): aynı hissede 60 gün içindeki tekrar haberler TEK olay sayılır. Bir hissenin tek bir çılgın dönemi
(ör. FONET Aralık 2023, RTALB Kasım 2020) aksi halde ortalamayı tek başına sürüklüyor.
Getiriler: ar = hissenin kendi yıllık ortalamasına göre arındırılmış; ham = çıplak; piy = aynı gün likit hisselerin ileri getiri medyanına göre fark.
RÜZGÂR = sektör sepeti (medyan) − piyasa medyanı, son 20 / 60 işlem günü.
  YENİ BAŞLAYAN: 60g ≤ 0 ve 20g > +%1 · OLGUN: 60g > +%3 ve 20g > +%1 · TERS: 20g < −%1.

## A. ÇIKIŞ / KAÇINMA İZLERİ
| # | İz | Ölçü | 17–21 | 22–26 | n | Durum |
|---|---|---|---|---|---|---|
| A1 | Bedelsiz bildirimi (SPK başvurusu/onayı) sonrası | ar60 | −12 / −11,5 | −6 / −5,8 | 228 / 682 | GEÇERLİ (tekrar arındırması yapılacak) |
| A2 | Tavan günü (+%9) sonrası | ar60 | −10,8 | −14,5 | 3.004 / 971 | GEÇERLİ (aynı) |
| A3 | Taban günü (−%5 altı) sonrası | ar60 | −4,8 | −4,7 | 7.691 / 19.501 | GEÇERLİ (aynı) |
| A4 | Hisse 20 günde %25+ koşmuşken iş ilişkisi haberi | ar60 | −7,0 | −8,2 | 162 / 599 | GEÇERLİ (aynı) |
| A9 | OLGUN rüzgâr + sözleşme/teşvik (tekrar arındırılmış) | ar60 ort / medyan | −5,4 / −4,4 | −3,3 / −4,3 | 220 / 461 | GEÇERLİ ama nötrden farkı küçük (nötr: −1,9/−3,6 ; −0,8/−3,3) |
| A5 | Söylentiye açıklama + o gün −%5 | ar60 | −32 | −22 | 26 / 46 | ADAY |
| A8 | Sözleşme tutarı yıllık ciroya göre >%50 | ar60 | −6,1 | −8,0 | 29 / 20 | ADAY |
| A7 | Açığa satış | ham60 | + | + | — | ÇÜRÜDÜ |
| A10 | Hacim patlaması (≥3× 60g ortanca) + gün kapanışı −%5 altı | piy20 ort / medyan | −3,5 / −6,3 | −2,8 / −4,2 | 267 / 799 | ADAY (iki dönemde ort+medyan aynı yön, n≥100; 60g medyan −7,3 / −5,6, kazanan %37 / %39) |
| A11 | A10 + hisse önceki 20 günde zaten −%20 düşmüş | piy60 medyan | −13,3 | −12,7 | 40 / 109 | ADAY-zayıf (kazanan %32/%30 ama 17–21'de n=40) |
| A12 | Fiyat 1 yıldır en geride %20 + hacim 1 yılda en çok ARTAN %20 (düşerken hacim = çıkış) | piy250 medyan | −1,7 | −14,3 | 232 / 299 | ADAY-zayıf (ort artı, medyan/kazanan/büyük-kayıp üçü eksi; 22–26 belirgin) |
| A13 | Dipteki doji kutusu (bölge kuralı v1.3 + ≥3 doji, önceki 250 günün alt %35'i) — SERT DÜŞÜŞ RİSKİ DÜŞÜK (19 Eki 2026, DOJI_KUTU_TEST v1.1) | 60 bar içinde −8× normal gün düşüş oranı, her gün tabanına göre | 16–19: %12,8 vs %20,3 · 20–22: %4,2 vs %14,7 | 23–26: %6,2 vs %9,2 · kırılımda da aynı yön (12,5/5,5/7,2 vs 20 gün zirvesi 21,3/17,9/11,0) | 3.332 / 1.980 / 4.369 | BIST'te GEÇERLİ (3 dönem aynı yön, mutlak −%20 ölçüsünde de); ABD testi bekliyor. Yükseliş tarafında fark YOK (sert yukarı 0,90–1,02×) — alım izi değil, risk süzgeci |

## B. ALIM İZLERİ
| # | İz | Ölçü | 17–21 | 22–26 | n | Durum |
|---|---|---|---|---|---|---|
| B1 | Geri alım bildirimi sonrası | ar60 | +4,9 | +2,4 | 1.583 / 7.496 | GEÇERLİ (küçük; tekrar arındırması yapılacak) |
| B1'' | Geri alım + hisse koşmamış + nötr rüzgâr | ar60 | +6,8 | +3,0 | 933 / 2.950 | GEÇERLİ? (tekrar arındırması yapılacak) |
| B9 | Yeni başlayan rüzgâr + sözleşme/teşvik + koşmamış | ar60 ort / medyan | +2,7 / +0,3 | +0,6 / −3,7 | 55 / 112 | ÇÜRÜDÜ — ilk ölçümdeki +9,6, FONET'in Aralık 2023'teki 5 tekrar haberinden geliyordu |
| B5 | Teyit günü | kazanan oranı | 45 vs 37 | sabit | 4.974 | GEÇERLİ ama net +1,0 |
| B6 | Likidite 5–50 mn TL ciro | — | + | + | — | GEÇERLİ (filtre) |
| B8 | Piyasa genişliği yılları | — | + | + | — | GEÇERLİ (zamanlama) |
| B2, B3, B4, B7 | (önceki adaylar) | | | | | ADAY |
| B10 | Kriz teyidi (+%5 dipten) sonrası KÜÇÜK piyasa değeri (sermaye×fiyat, alt üçte bir) | kriz-içi medyana göre 60g ort / medyan | +23,7 / +12,4 | +12,0 / +1,9 | 111 / 639 | ADAY (iki dönemde aynı yön; 17–21'de yalnız 4 kriz). Büyük PD: −9,8/−8,5 ; +2,0/−1,6 |
| B11 | Kriz teyidi sonrası dayanıklı (en az düşen %20) + canlı | 60g ort / medyan | +2,6 / −3,7 | +14,6 / +6,5 (7/7 kriz) | 49 / 355 | REJİME BAĞLI — 17–21'de ters |
| B12 | ÇÖL KIRILIM GÜNÜ yön teyidi: çölün son 4 haftasında hacim ≥ çöl ortalaması → yukarı kırılma | yukarı kırılma oranı | %79 (n 190) | %95 (n 196) | 386 | ADAY — yön bilgisi; hacim kuruyarak biten çöl (<0,7×) %37 / %18 yukarı. Kırılım GÜNÜ hacmi ise yönü ayırmıyor, yalnız hareket büyüklüğünü (26h ±%30 üstü: hacim az %28 → çok %64) |
| B13 | B12 + sektör rüzgârı (20g > +%1), giriş = çölün son günü (sonradan bilinen) | piy60 ort / medyan | +16,6 / +8,0 | +26,9 / +12,3 | 107 / 119 | ADAY ama SONRADAN BİLGİ — gerçek zamanda tutmadı (bkz. C) |
| B14 | YUVARLANMA ÖBEĞİ (21 Eki 2026, COL_OBEK): 10–25 bar, dip ilk %40'ta, yeni dip yok, dipler yukarı yuvarlanıyor, mumlar önceki 60 güne göre küçük. Sinyal = ilk sağlandığı gün. Olay 60 bar: ALIM (kapanış > öbek tavanı) / DÜŞÜŞ (dip −%2) | ALIM oranı vs taban (her 5. gün, 15 bar zirvesi) | 16-19: %70 / %52 · 20-22: %78 / %62 | 2023: %67 / %54 · 24-26: %71 / %49 | 69.180 öbek / 198.120 taban | ADAY — yalnız YÖN: öbekten sonra alım gelme olasılığı 4 dönemde tabanın 15–20 puan üstünde. KAZANÇ YOK: alım geldikten sonra +%8'i stoptan önce görme oranı tabanla aynı (72/75, 82/82, 79/83, 73/72); 120 bar piyasaya göre medyan +2 (16-19'da 0). Öbek sırası ↑ ve yuvarlanma ↑ iki dönemde de alımı artırıyor (ör. 22-26 obek_sira tercilleri %69→%75, fark120 −0,2→+4,5). Düşen bıçak (öbek öncesi 20 gün düşüş) zayıf: en dik tercil alım 70–74 vs 75–78. |
| B15 | ÇIKIŞ KURALI (21 Eki 2026, COL_YOL): öbek → yeşil kapanış tavan üstü → ertesi açılış → ilk stop öbek dibi −%2 → 11 çıkış varyantı, 120 bar | 30 slot portföy (dönem ort.) / işlem başı kazanan / ağır kayıp | 16-19: maliyet8_sma20 +93 · mevcut +101 · zirve10 +70 | 20-22: merdiven +284 · cemal +281 · maliyet8_sma20 +231 | 2023: maliyet8_sma20 +124 · zirve10 +103 | 24-26: maliyet8_sma20 +180 · mevcut +144 | 50.006 işlem | ADAY — "+%8 görülünce stop maliyete + %20 sonra SMA20 trail" (maliyet8_sma20) 4 dönem ortalaması +157 (mevcut +144, 1,09x; 1,3x değil), ağır kayıp %6 (mevcut %10). Yalnız maliyete çekme (5/8/10/20) işlemlerin %70–89'unu maliyetten çıkarır, medyan −0,4, para kazandırmaz. Cemal merdiveni (+8→0, +10→+2) kazanan %61, ağır %6 ama medyan +1,6: kazananı erken kesiyor. Stopsuz mevcut işlem başına en iyi (+18,9) ama ağır kayıp %11 ve 70+ bar tutuyor. Öbek tabana göre her varyantta ağır kaybı düşürüyor (24-26 stop_ufuk %16 vs %27). SABİT HEDEF (al-çık, 21 Eki ek): hedef_5 kazanan %84 ama işlem başı +1,4; hedef_8 %78 / +2,5 / portföy +130; hedef_10 +107; hedef_15 +119; hedef_20 +115. Hiçbiri +%8 maliyete + trail'i (+157) geçmiyor; hedef_8 mevcuda yakın (+144), 2024-26'da +128 vs +180. Kazanan oranı yüksek, kâr küçük: stop kaybı (~−10) hedef kazancını yiyor. ABD (21 Eki, 23.096 + 47.843 öbek işlemi, aynı kod): 30 slot ort. mevcut stopsuz +37 · maliyet_8 +25 · maliyet_10 +23 · mevcut +21 · maliyet8_sma20 +17 · cemal +7 · hedef_8 +7 · hedef_5 −10. 22-23: maliyet8_sma20 −6 vs mevcut +6; 24-26: +40 vs +37. → maliyet8_sma20 6 dönemin 3'ünde mevcudu geçiyor: GETİRİ İZİ DEĞİL. Tutarlı tek bulgu: +%8'de maliyete çekme ağır kaybı (≤−%15) her dönemde yarıya indiriyor (BIST %10→%6, ABD %7→%4), karşılığında kazanan oranı düşüyor (BIST %61→%39, ABD %44→%28). Sabit hedefler ABD'de de para etmedi (hedef_5 −10, hedef_8 +7). T10 ile üretime yazıldı (21 Eki, Cemal'in kararı); 6 ay sonra canlı sonuçla yeniden bakılacak. |

## C. ÇÜRÜYEN / BOŞ İZLER
- DİP ÇÖLÜ (D12, 20 Ekim 2026, COL_DIP_TEST): bölge + dipte + yeni dip yok + imza ≥3/4 tespitinden atılımda alım (ertesi gün açılış, %20 sonra SMA20 trail), taban = her taze 20 gün zirvesi kırılımı aynı çıkışla. Beklenti dip/taban: BIST 16-19 +14,7/+13,8 · 20-22 +15,9/+24,1 · 2023 +42,0/+28,8 · 24-26 +6,9/+9,2 · ABD 22-23 +1,6/+3,2 · ABD 24-26 +11,3/+5,6 (n 1.235–2.472). 6 dönemin 3'ünde iyi, 3'ünde kötü → İZ DEĞİL. Çöl tespiti atılımın üstüne kalıcı bir kazanç eklemiyor (COL_OZET 8. bölüm ile aynı).
- DOJİ KUTUSU → SERT HAREKET (19 Eki 2026, DOJI_KUTU_TEST v1.1, BIST 583 hisse 2016–26): kutu 3. dojisini bulduğu gün ya da kutu kırıldığında, sonraki 60 barda ±%20 sert hareket / önce yukarı oranı her gün tabanıyla ve 20 gün zirvesi kırılımıyla aynı (kat 0,90–1,02, üç dönem). Yükseliş izi yok; düşüş riski izi A13'te.
- Haber türü, büyüklüğü, davranışı tek başına; makine birleşimi (AUC 0,56); D1; teyit+geri alım; merdiven; sektör kümesi; 1 hafta biletleri; ABD salınım fiyat-only
- B9 (yeni rüzgâr + haber): tek hisse tekrarı → çürüdü
- ÖLÜ EŞEK (4 Eki): üç yoldan denendi, hiçbiri ayrışmadı — (a) KAP yapısal kötü haber sınıfları (4.910 metin: konkordato, fabrika kapatma/taşıma, üretim durdurma, SPK tedbiri…) sonrası 60g: hiçbir sınıf iki dönemde tutarlı eksi değil; (b) bilanço (2 yıl satış geride + zarar / 2 yıl faaliyet+net zarar / özkaynak eksi) → rapor sonrası 250g ÖLÜ ort +32,7/+44,5 medyan −9,7/+4,8 — canlıdan kötü değil; (c) fiyat+sektör 1 yıldır geride (İşY 53 sektör) → en çok düşen+geride ort +3,8/+2,8 medyan −4,1/−1,2 (n 7/66). UYARI: fiyat verisi yalnız bugün borsada olan 583 hisse — iflas/kot dışı olanlar yok (hayatta kalma yanlılığı), bu yüzden "ölü eşek tutmaz" DENEMEZ, "mevcut veriyle test edilemiyor" denir. Cemal'in örnekleri: İhlas grubu 5 yılda piyasaya göre −310 puan (5/5 geride), YESIL −411 puan, tekstil 3 yılda −22 puan. Döngüsel sektörler (otomotiv, çimento, beyaz eşya, havacılık) bu kurala takılıyor ama ölü değil — OTKAR/FROTO/ARCLK satış büyüyor, kâr 1 yıl bozuk.
- "Güvenilir isim çok düştü, V yapar": en çok düşen + temettü veren → medyan −3,1 / −4,0 ama ortalama +2,4 / 0,0 → iz değil.
- Para izi (erken toparlanma gücü/hacim), orta düşmüş+güçlü toparlanan: tutmadı.
- ÇÖLDE ERKEN GİRİŞ (gerçek zamanlı, 4 Eki): her hafta o güne kadarki veriyle çöl (52h bant ≤%45, yeni dip yok) + akümülasyon (son 20g hacim ≥ çöl ort.) + rüzgâr/haber/geride → 60g medyan 17–21: −4,0…−7,4 (kazanan %30–36), 22–26: +1,8…+3,7 (çöldeki her hissenin tabanı +3,7). Hiçbir varyant (tavana yakın, sakin fiyat, dar çöl, güçlü akümülasyon) tabanı geçmedi. ÇÜRÜDÜ. Sebep: hacim artışı "para girdi" der, "ne zaman kalkacak" demez; çölde beklemek 17–21'de para kaybettirdi.
- Hacimli YUKARI kırılım (+%5 üstü kapanış) devamı: 60g medyan −2,3 / −2,9, kazanan %46/%45; ortalama artı (birkaç uçan). İz değil.
- DERS 1: 22–26'da tutmayan iz iz değildir.
- DERS 2: aynı hissenin tekrar haberleri tek olay sayılmazsa ortalama yalan söyler. Medyan her zaman yanına yazılır.
- DERS 3 (4 Eki): sektör sınıflaması sonucu değiştirir — kaba 10 grupta TTKOM kulüp ve gazetelerle aynı gruptaydı, "ölü" çıktı; 53'lük İşY kodunda telekom +32 puan önde. Kaba grup kullanılmaz.
- DERS 4: "çölün son günü" sonradan bilinen bilgidir; kırılımla hizalı her test gerçek zamanlı yeniden kurulmadan iz sayılmaz.

## D. SIRADAKİ İŞ
1. Bütün A ve B izlerini "60 günde tek olay" kuralıyla yeniden ölç.
2. Cemal'in verdiği örnek olaylar → aynı hesapla tek tek göster (doğrulama).
3. Mevcut kriz (dip 28 Eyl 2026): +%5 teyit gelince B10 (küçük PD) listesini çıkar; kriz_dava_dosyasi sayfasını güncelle.
4. A10/A11/A12 için akşam motoruna "hacimli aşağı kırılım" uyarısı ekle (çıkış katmanı).
5. B12'yi COL sistemine kırılım günü filtresi olarak ekle: son 4 hafta hacim < 0,7× çöl ort. ise kırılımı alma.
6. Borsadan çıkmış hisselerin fiyatı bulunursa ölü eşek testini yeniden kur.
7. M5 fon portföyü filtresi düzeltilecek (arşivde 0 rapor buldu); M4 yabancı yazılarının 347'si çözülemedi.

## E. YÖNTEM (nasıl hesaplandı)
1. KAP bildirimi → hisse, tarih, saat. Saat 18:00'den sonra gelen haber ertesi işlem gününe sayılır (D0).
2. Giriş fiyatı = D0 kapanışı (haber çıkmış, herkes görmüş).
3. 5 / 20 / 60 işlem günü sonraki kapanış ile getiri.
4. Aynı günün piyasa medyan getirisi çıkarılır → piyasaya göre fark.
5. O hissenin o takvim yılındaki ortalama farkı çıkarılır → "ar" (hisse zaten o yıl uçuyorsa haber ona kredi almaz).
6. Rüzgâr: hissenin sektöründeki hisselerin günlük getirilerinin medyanı − piyasa medyanı, son 20 ve 60 günde toplanır.
7. Kova kova ortalama + medyan, 2017–21 ve 2022–26 ayrı.
8. Hacim testleri (4 Eki): TL hacim = kapanış × adet; patlama = gün hacmi ≥ önceki 60 gün medyanının 3 katı; "piy" ölçüsü = aynı gün likit hisselerin ileri getiri medyanına göre fark (sıradan günlerde medyan ≈ 0, kayma kontrol edildi).
9. Veri sınırı: fiyat yalnız bugün borsada olan 583 hissede (Eyl 2016→); borsadan çıkmış hisseler yok. Ölü eşek ve iflas testleri bu yüzden eksik.
