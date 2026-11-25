# UC_IZ2 RAPOR — üç fiyat dışı iz (R sektör rüzgârı, B bilanço tepkisi, İ içeriden alım) aynı bilanço olayında, ABD 2016-22 (25 Kasım 2026)

**KASA ADAYI: HAYIR (R60 ve R15).** Üç iz de iki ufukta ve iki karar hücresinde **TUTMADI**. Güç yeterliydi: her iz-var hücresinde n 973-8.331, güç 0,86-1,00. YÖN TUTARLI iz yok. BİRLİKTE ARTIYOR: HAYIR. BH (aile 8): geçen yok, en küçük p 0,061 (N>=2, R60).

Sıra: kod commit cef0b7d (09:10:47 UTC) -> ön kayıt commit b62b806 (09:11:19 UTC) -> push -> koşu 09:11:32-09:16:40 UTC. Kapı (uc2_kapi: ik_kontrol_kapisi + KOD_SHA 71d0e239… + ESIK_SHA afa47f7a… + HAZIRLIK_SHA 52a19fa6… + git) geçti. Açık veriye bir kez bakıldı. Sonuç uc_iz2_sonuc.json. Satır dosyası 6,6 MB olduğu için repo dışında: /root/.kasa/ham/sec2016/uc_iz2_satir.csv.gz (sha 5259d363…, 53.734 satır, en geç tarih 2022-12-30).

## Veri
- Fiyat: TEZGAH2 yeniden indirildi (ABD V_ABD2 5.394, AVR V_AVR2 578 sembol). Açık kopya 2022-12-31'de kesildi; ölçüm kopyası 2012-01-03'ten başlıyor (4.450 ABD sembolü). TEZGAH2_DOGRULAMA'nın 21 hükmü yeniden koşuldu: P1 21 / 21, P2 20 / 21 (A1 2001-07 KISMEN, r 0,897). İkisi de orijinal koşuyla aynı.
- Form 4: 2015q4-2022q4, 29 çeyrek, 310 MB. A1 (fi_k30_alimlar aynen, >= 10.000 $): 84.054 bildirim, 6.502 ihraççı CIK. 2022 sağlaması k30_alim.pkl ile 2.119 / 2.119, 5 satır alan alan birebir.
- 8-K 2.02: data.sec.gov submissions, 5.580 CIK, 6.517 istek, yeniden deneme 0, 404 0. 2.02 satırı 188.048 (bütün yıllar). acceptanceDateTime UTC'dir, New York saatine çevrildi. 5 rastgele olay EDGAR sayfasıyla (WebFetch) karşılaştırıldı: tarih, saat ve madde 5 / 5 aynı.
- E1 huni: E1 73.329 (3.205 CIK) -> P2 54.154 -> analiz 53.734 -> eşli R15 53.627, R60 51.509. Pencere içinde 20 gün kuralıyla atılan 2.02 sayısı 3.459 (%4,4). Eşlenemeyen sembol 8 / 4.441.
- Bayraklı olay (E1): R 3.411, İ 13.344, B 16.394, Bm 14.926. Örtüşme phi -0,015..-0,001, yani izler birbirinden bağımsız.

## Tablo 1 — tek izler (FARK = R_H olay − eş ortalaması, yüzde puan; [ay kümeli boot %95])
| iz | ufuk | hücre | n var / yok | FARK var | var − yok | SIRA | ÜST10 − taban_f | ÜST10 − taban_p | güç | c2 hüküm |
|---|---|---|---|---|---|---|---|---|---|---|
| R | R60 | d1619 | 973 / 25.272 | +1,39 [+0,06; +2,74] | +1,40 | 0,515 | −0,6 | −0,6 | 0,86 | TUTMADI |
| R | R60 | d2022 | 1.994 / 21.842 | +1,37 [−0,53; +3,54] | +1,98 | 0,522 | −0,2 | −0,2 | 0,89 | TUTMADI |
| B | R60 | d1619 | 8.331 / 17.914 | −0,02 [−0,46; +0,39] | −0,09 | 0,500 | −3,0 | −3,0 | 1,00 | TUTMADI |
| B | R60 | d2022 | 5.573 / 18.263 | −0,32 [−1,36; +0,70] | +0,16 | 0,512 | −1,1 | −1,1 | 1,00 | TUTMADI |
| İ | R60 | d1619 | 4.173 / 22.072 | +0,34 [−0,25; +1,04] | +0,35 | 0,502 | −1,4 | −1,4 | 1,00 | TUTMADI |
| İ | R60 | d2022 | 4.033 / 19.803 | −0,71 [−2,60; +1,08] | −0,32 | 0,511 | −1,1 | −1,1 | 1,00 | TUTMADI |
| R | R15 | d1619 | 973 / 25.272 | +0,38 [−0,19; +0,96] | +0,22 | 0,512 | −0,7 | −0,7 | 1,00 | TUTMADI |
| R | R15 | d2022 | 2.088 / 23.866 | −0,53 [−1,41; +0,46] | −0,29 | 0,490 | −1,8 | −1,9 | 1,00 | TUTMADI |
| B | R15 | d1619 | 8.331 / 17.914 | +0,05 [−0,20; +0,30] | −0,17 | 0,499 | −2,2 | −2,3 | 1,00 | TUTMADI |
| B | R15 | d2022 | 6.142 / 19.812 | +0,27 [−0,31; +0,82] | +0,70 | 0,512 | −0,2 | −0,2 | 1,00 | TUTMADI |
| İ | R15 | d1619 | 4.173 / 22.072 | +0,20 [−0,25; +0,72] | +0,04 | 0,504 | −2,0 | −2,0 | 1,00 | TUTMADI |
| İ | R15 | d2022 | 4.350 / 21.604 | −0,15 [−1,05; +0,68] | +0,13 | 0,504 | −1,1 | −1,1 | 1,00 | TUTMADI |

İz kararları (iki ufukta da): R TUTMADI, B TUTMADI, İ TUTMADI. Dört şarttan en az biri her hücrede düştü. ÜST10 − taban 12 satırın hepsinde negatif.
- R60'ta R'nin FARK'ı iki hücrede de pozitif (+1,39 / +1,37) ve var − yok de pozitif (+1,40 / +1,98). Düşen şart ÜST10 − taban (−0,6 / −0,2). c2 hükmünü düşüren SIRA boot alt <= 0,50 (d1619) ile FARK boot alt, SIRA boot alt ve L3O (d2022). BH p 0,107.
- B (güçlü bilanço tepkisi): R60 FARK −0,02 / −0,32, R15 +0,05 / +0,27. Sonraki 15 ya da 60 barda eşlerden ayrışma yok.
- İ (90 gün içinde içeriden alım): R60 +0,34 / −0,71, R15 +0,20 / −0,15. İki dönem ters yönde.

## Tablo 2 — birlikte (N = R + B + İ)
| N | ufuk | hücre | n | FARK [%95] | medyan | SIRA | ÜST10 − taban_f | ALT10 − taban_f |
|---|---|---|---|---|---|---|---|---|
| 0 | R60 | d1619 | 14.481 | +0,00 [−0,49; +0,50] | −0,32 | 0,507 | −2,8 | −3,2 |
| 1 | R60 | d1619 | 10.088 | −0,01 [−0,42; +0,37] | −0,49 | 0,499 | −2,8 | −2,5 |
| >= 2 | R60 | d1619 | 1.676 | +0,80 [+0,13; +1,53] | −0,25 | 0,509 | −0,9 | −2,7 |
| 0 | R60 | d2022 | 13.805 | −0,47 [−2,47; +1,31] | −1,05 | 0,509 | −1,2 | −2,2 |
| 1 | R60 | d2022 | 8.524 | −0,70 [−2,11; +0,55] | −1,31 | 0,510 | −1,0 | −2,1 |
| >= 2 | R60 | d2022 | 1.507 | +1,36 [−0,21; +2,96] | −0,80 | 0,523 | −0,8 | −3,0 |
| 0 | R15 | d1619 | 14.481 | +0,19 [−0,10; +0,48] | +0,03 | 0,505 | −2,8 | −3,4 |
| 1 | R15 | d1619 | 10.088 | +0,15 [−0,07; +0,41] | +0,02 | 0,504 | −2,4 | −2,9 |
| >= 2 | R15 | d1619 | 1.676 | −0,01 [−0,41; +0,43] | −0,13 | 0,493 | −1,1 | −2,2 |
| 0 | R15 | d2022 | 15.092 | −0,40 [−1,52; +0,31] | −0,37 | 0,502 | −1,9 | −1,9 |
| 1 | R15 | d2022 | 9.210 | −0,15 [−0,92; +0,52] | −0,32 | 0,505 | −0,9 | −2,1 |
| >= 2 | R15 | d2022 | 1.652 | +0,36 [−0,42; +1,15] | −0,36 | 0,507 | −0,6 | −2,3 |

- BİRLİKTE ARTIYOR: HAYIR. R60'ta sıra iki hücrede de bozuk: N=1, N=0'dan küçük (−0,01 < +0,00 ve −0,70 < −0,47). R60 N>=2 d1619'da boot alt > 0, ama c2 hükmü TUTMADI (SIRA boot alt <= 0,50). R60 N>=2 d2022'de güç 0,78, hüküm ÖLÇÜLEMEDİ. Bu, ön kayıtta beklenen tek ölçülemeyen gruptu. R15'te sıra yalnız d2022'de tuttu; d1619'da N>=2 FARK −0,01.
- Çiftler (bilgi, karar dışı): R∧B R15 d1619'da n 327, FARK +1,34 [+0,42; +2,26], c2 TUTAR. Aynı çift d2022'de −0,11, TUTMADI. Bir dönem pozitif, öteki negatif olduğu için iz sayılmaz. R∧İ ve B∧İ çiftlerinde güç 0,18-0,94, hepsi ÖLÇÜLEMEDİ ya da TUTMADI.
- N=3: n 37 / 62, güç 0,07-0,21, ÖLÇÜLEMEDİ.

## Ölçülen şans tabanları (ÜST10)
- Formül ile plasebo neredeyse aynı (200 tohum). HEPSİ R60: formül %10,7 / %10,5, plasebo %10,8 / %10,5. Medyan eş sayısı 78 / 121.
- Gözlenen pay: E1 olaylarında ÜST10 %8,1 / %9,4 ve ALT10 %7,8 / %8,3 (HEPSİ, R60). İki kuyruk birlikte tabanın 1-3 puan altında. Bu tablo bütün gruplarda ve iki ufukta da aynı.
- Yorum (çıkarım, doğrulanmadı): bilanço olayı girişte geride kalmış oluyor. Eşlerin çoğu ise kendi bilançosunu 15-60 bar içinde açıklıyor. Bu yüzden olayın R_H dağılımı eşlerinkinden dar kalıyor ve ÜST10 − taban şartı bilanço olaylarında yapısal olarak negatife kayıyor (K1: eş geometrisi aynı değil). Ç225'in dip olayı için yazılmış bu şart, bilanço olayında tarafsız değil. FARK ortalaması bu kaymadan doğrudan etkilenmez, ama oradaki sonuç da tutmadı.

## E2 (BİLGİ; Ç225 kıyas satırı; karar vermez)
- KT02 dip olayı bu evrende 1.394, eşli olay R15'te 507 + 659 (Ç225'te 134 + 195). Gerçek B'li dip olayı yalnız 16 / 15, gerçek İ'li 116 / 127, R'li 11 / 21, N>=2 3 / 9.
- HEPSİ R15 FARK −0,51 [−1,51; +0,44] / −2,56 [−6,28; −0,53]. Ç225'te +0,73 / −0,68 idi. d2022'de boot üst ucu sıfırın altında. İ'li dip olaylarında R15 +0,66 / −2,70 (güç 0,45 / 0,38), ÖLÇÜLEMEDİ.
- R60 HEPSİ: −0,71 / −5,81, güç 0,57 / 0,38, ÖLÇÜLEMEDİ.

## Doğrulamalar
- D1 (V1-V4, ölçümden önce): T2 21 hükmü orijinalle aynı çıktı. k30 sağlaması 2.119 / 2.119. EDGAR karşılaştırması 5 / 5. Ham zip'ten okunan 10 rastgele A1 satırı 10 / 10.
- D2 (K2, prefix 2019-06-28): 33.367 / 33.367 olay ve R / İ / P2 bayrakları birebir aynı. B'de 2 değişim var (%0,006), BVAL'de 342 küçük fark. Bu farkların hepsi CETVEL2 panelinin genç hisse nedeniyle değiştiği 72 günde, öteki günlerde fark 0. Neden: OC.oc_veri min_bar 80 süzgeci (aşağıda HATA H2).
- D4 (K11, bağımsız düz pandas, UC_IZ2 / CETVEL2 kodu kullanılmadı): satır dosyasından 4 hücre yeniden üretildi (B=1 R60 d1619, İ=1 R15 d2022, HEPSİ R60 d2022, N>=2 R15 d1619). n, FARK, SIRA, ÜST10 ve taban_f JSON ile < 1e-9 farkla aynı. 20 rastgele olayın R15 / R60 değeri ham fiyattan düz döngüyle hesaplandı, giriş günüyle birlikte 20 / 20 aynı. 10 olayın ATRP20 değeri ham fiyattan 10 / 10 aynı. Satır dosyasında N = R + B + İ, B = (BVAL >= 1) ve Bm = (BVAL <= −1) her satırda doğru.

## HATA
- H1 (veri, bulan: alt ajan, ölçümden önce): iş tanımı "kabul saati New York 16:00" diyor, ama acceptanceDateTime UTC ('Z'). İlk taslakta saat dilimi yerel varsayıldı. AAPL duyurularıyla (20:30 / 21:30 Z = 16:30 ET) ve EDGAR sayfasıyla sınanıp UTC -> New York dönüşümü yazıldı. Karara etkisi yok.
- H2 (geleceğe bakma, küçük; bulan: alt ajan D2 prefix testi): CETVEL2 taban paneli (DS.ds_veri -> OC.oc_veri) min_bar 80 süzgecini hissenin BÜTÜN serisine uyguluyor. Bu yüzden bir hissenin ileride 80 bara ulaşıp ulaşmayacağı, ilk 80 barındaki günlerde kesitsel likidite (OC H), havuz (ok) ve kova (KV) hesabına giriyor. Prefix testinde 72 gün, KV'de 157 hücre fark çıktı. B'ye etkisi 2 / 33.367 değişim. CETVEL2 c2_prefix bunu denetlemiyor (yalnız ATRP / F15 / hat). Aynı özellik CETVEL2 konum eşini kullanan bütün ölçümlerde var (Ç225 dahil). Öneri: OC paneline nedensel min_bar (evren_bas = 80. bar) ve c2_prefix'e LQ / ok / KV denetimi. Bu karar ana modelin; modüllere dokunulmadı.
- H3 (ölçüt / tasarım, bulan: alt ajan, sonuçtan sonra): ÜST10 − taban şartı bilanço olayında tarafsız değil. E1 olaylarında iki kuyruk da tabanın altında. Nedeni çıkarım: eşlerin bilançosu pencerenin içinde. Karar kuralı değiştirilmedi, sonuç aynen yazıldı. Ders: kuyruk şartı yalnız olayla eşin aynı olay takvimini paylaştığı tasarımlarda kullanılmalı.
- H4 (iletişim, bulan: alt ajan, ölçümden önce): hunideki "20 gün tekrar atılan 28.509" sayısı, 2015 öncesi dosyalar da dahil bütün yılları kapsıyor. Pencere içindeki sayı 3.459. Ön kayıtta S8 olarak düzeltildi.
- H5 (süreç, bulan: test): ilk hazırla koşusu katı prefix ölçütüyle durdu. Ayrıştırmalı ölçüt eklendi (S7), kod değişti ve hazırla baştan koşuldu. Ön kayıt yeni sha'larla yazıldı. Bu sırada getiri görülmedi.
- H6 (veri, küçük): uc2_olay_gunu, D0'ı takvim başından (2012-01-03) önce olan eski dosyaları ilk takvim gününe atıyor. Bu dosyalar sonra aralık süzgeciyle düşüyor, 2015-10 sonrası olaylara etkisi yok, ama tanım temiz değil.
- Yahoo indirmesinde iki kez "crumb 429" uyarısı çıktı. İndirilemeyen sembol 0, veri kaybı yok.

## SAPMA
Hepsi ön kayıtta yazıldı (S1-S8), ölçümden önce. S1: veri 2012'den başlıyor (bellek). S2: T2 21 sınamasının "hepsi geçmeli" yorumu. Seçilen havuz 21 / 21 ve orijinalle aynı; P2'nin tek KISMEN satırı orijinalde de vardı. S3: R60 güç eğrisi aynı yöntemle bu panelde hesaplandı. S4: submissions indirildi, çünkü sec_ozet'te kabul saati yok. S5: E1 tekil 1. S6: c2_plasebo yalnız karar gruplarında koşuldu (TUTAR karar hücresi çıkmadığı için hiç koşmadı). S7: ayrıştırmalı prefix ölçütü. S8: tekrar sayımı. Koşudan sonra sapma yok.

## Dürüst okuma
- Sayı: 2016-22 ABD'de bugün yaşayan hisselerde bilanço günü sonrası sektör rüzgârı, güçlü bilanço tepkisi ve 90 günlük içeriden alım, tek tek de birlikte de 15 ve 60 barda eşlerinden tutarlı ayrışmıyor. Güç yeterli (n binlerle).
- En yakın sonuç: R (rüzgâr) R60'ta FARK +1,4 puan, iki dönemde de pozitif. Boot alt ucu d1619'da +0,06, d2022'de −0,53. Kuyruk şartı ve SIRA boot şartı tutmadı. N>=2 R60'ta da +0,80 / +1,36.
- K7: evren bugün yaşayanlar, sonuçlar yukarı yanlı. Bu yanlılık olaya ve eşe aynı ölçüde biniyor.
- AVRUPA VERİSİ YOK (SEC yalnız ABD). En iyi durumda bile karar ABD-ADAY'ı geçemezdi.

## KONTROL LİSTESİ
| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | CETVEL2 v2.2 konum eşi (aynı giriş günü / kova, >= 5, o gün E1 olan bütün CIK sınıfları dışı); taban formül + plasebo 200 tohum; kuyruk şartı bilanço olayında tarafsız değil (H3) |
| K2 | geleceğe bakma | EVET | kabul UTC -> NY, t >= D0 assert; İ D <= t assert; B girdileri t satırında; fiyat / A1 <= 2022-12-31 (kasa_kapisi, en geç 2022-12-30); prefix 33.367 / 33.367, R / İ / P2 0 fark, B 2 (H2) |
| K3 | geçerli bar | EVET | OC temiz bar; t'de geçersiz bar olan 1.439 olay düştü |
| K4 | tekilleştirme | EVET | 20 gün kuralı (pencere içi 3.459); çok sınıflı 42 CIK'de tek sembol; medyan raporda |
| K5 | giriş fiyatı | EVET | giriş t+1 ilk geçerli bar açılışı; 20 / 20 ham fiyattan aynı |
| K6 | veri birimi | EVET | auto_adjust tek kip; oranlar birimsiz; T2 21 hükmü orijinalle aynı |
| K7 | hayatta kalma | EVET | bugün yaşayan 4.450 ABD hissesi; sonuç yukarı yanlı yazıldı |
| K8 | örneklem ve dönem | EVET | iki dönem; iz-var n 973-8.331; BH aile 8, geçen yok |
| K9 | ön kayıt | EVET | cef0b7d (09:10:47) -> b62b806 (09:11:19) -> push -> koşu 09:11:32; kapı geçti |
| K10 | ayrıştırma | EVET | A1 10 / 10 ham zip; k30 2.119 / 2.119; EDGAR 5 / 5 |
| K11 | yeniden üretim | EVET | 4 hücre düz pandas < 1e-9; R15 / R60 20 / 20; ATRP20 10 / 10 |
| K12 | ifade | EVET | iz sözü kullanılmadı (karar kuralı geçmedi); sayı ve yorum ayrı cümlelerde |
| K13 | süreç | EVET | çakışma kapısı (test); defter dosyalarına dokunulmadı; UA yalnız /root/.sec_ua, içerik hiçbir dosyada yok (tarama 0); ham SEC repo dışında |
| K14 | boyut | UYGULANMAZ | öneri / gerçek para işi değil |
