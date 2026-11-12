# K66 — ABD AÇIĞA SATIŞ TALEBİ ÇÖL SİNYALİNE EK BİLGİ TAŞIYOR MU: ÖN KAYIT (ölçümden ÖNCE)

K66 v1.0 (2026-11-12): ABD açığa satış talebi (FINRA açık pozisyon) çöl sinyaline ek bilgi; K64 tasarımı aynen, 4 değişken x 2 yön
Yazım zamanı: 2026-11-12 04:38:18 UTC (2026-11-12 07:38 TR)
ESIK_SHA256: 1d820a4e26388b043d6b1f8539813ee2027110e7a4c947cbe56173de8af27c0a

Bu dosya gerçek veride değişkene bağlı HİÇBİR getiri / eşli fark hesaplanmadan yazıldı (yalnız `indir` ve `kapsam` sayımı koşuldu: §12). `python -I K66.py kos`
bu dosya git'e işlenmeden, mühür ya da veri sha256'ları tutmadan çalışmaz. Sonuç görüldükten sonra yeni kural eklenmez. Tasarım K64_K65_ON_KAYIT.md ile aynıdır
(K64.py fonksiyonları içe alınır, kopyalanmaz; K64.py değişmez); burada yalnız farklar ve yeni değişkenler tam yazılır.

## Veri (sha256; `kos` başında yeniden hesaplanır, farklıysa koşu durur)
- V_ABD.pkl: sha256 82871d2c7c28ca939da3217a597864f11fcfa1fd1db7d85f7a8ccd609248d19e (1 dosya)
- k66_finra: sha256 ead6794cd0dfbcfafd9e65e095ce2894f0caf2b3767f8dc0a94a58990c1edff1 (209 dosya)
- K60_ON_KAYIT.md: sha256 eba12e1d060217f2c1fd4ffe5715382d29d343cd29004af5c69617b10b2218c0 (1 dosya)
- K64_K65_ON_KAYIT.md: sha256 0d2e34ab9f6d825636425c1a9897eab6b8fe4e0f18defd49a393f6fd3cd3a73e (1 dosya)
- FON_IZI.py: sha256 ea0cc19f9b6514c50340df0e331c8d1a5e7961083918eefec45de6d7eb10ac7b (1 dosya)
- K60.py: sha256 d819f93082188688f5a3ed2a5d1bdb39735169125f292c62103b3e842ebd8e66 (1 dosya)
- K59.py: sha256 a302656f957d9b99149873ebc0880798d694d03341da1559af79d460b491c655 (1 dosya)
- COL_v1.py: sha256 13597d4209698a7edbeb4fb947c383ffa1c3c2d9eb715e33c5ef6902ce8987b8 (1 dosya)
- K64.py: sha256 0255e8b2902228e20665a439e8df529cf4521bbee4ed24d248c1977e08577653 (1 dosya)
K60 önbellekleri (/tmp/k60_fiyat, /tmp/k60_secframes ...; pay sayısı ve bölünmeler) K60 ön kaydındaki sha256'larla doğrulanır (K60.k60_onkayit_dogrula, veri = True).
K60 mührü ve K64 mührü bu işin mührüne girer.

## 0. Soru (Cemal'in isteği; ana oturum iş tanımı K66)
Çöl tanımı ve mevcut cetvel DEĞİŞMEZ. ABD açığa satış talebi (FINRA açık pozisyon: oran, kapatma günü, değişim) mevcut ÇÖL sinyaline EK BİLGİ taşıyor mu? Her
değişken tek tek ve İKİ YÖNDE sınanır; katkı değişkensiz temel modele (yalnız çöl) karşı ölçülür. Üretim koduna ekleme yapılmaz.
EVREN: yalnız ABD. **BIST VERİSİ YOK**: BIST'te açığa satış 2020'den beri yalnız BIST-30 / 50 hisselerinde (yasak dönemlerinde hiç) var, açık pozisyon yayını yok (K63);
çöl evreni (küçük hisseler) için ölçülemez. ABD bulgusu BIST'e genellenmez.
**ÖDÜNÇ ÜCRETİ / KULLANILABİLİR ADET / KULLANIM ORANI: VERİ YOK** (ücretsiz tarihsel kaynak yok, K63; ücretli: IBorrowDesk API 29 $/ay; karar Cemal'de). Vekil uydurulmadı.

## 1. Olay (K64_K65_ON_KAYIT.md §1 AYNEN; K64.k64_olay_k24 / k64_olay_d13 çağrılır)
- ANA: K24 'iki evre' çöl sinyali — FON_IZI.fi_k24_tara, FI_K24 = {"seri": 5, "once": 10, "once_alt": 0.8, "delen_en_cok": 2, "bbw_oran": 0.7, "bbw_pencere": 15, "dusus": -0.3, "tekrar": 60}. Sinyal günü t; giriş = hissenin t'den sonraki ilk işlem
  günü açılışı. TEKİLLEŞTİRME: son TUTULAN sinyalden en az 60 işlem günü sonra gelen ilk sinyal (FI_K24 'tekrar' = 60 ile birebir; kodda denetlenir).
- İKİNCİL (sağlamlık; BH ailesine ve karara GİRMEZ): üretim D13 + AL kırılımı (COL_v1.col_olc, haftalık tespit ızgarası, GECER şartı; K64 §1 (ii) aynen).
  Gerçek veride D13 olayları K64'ün ara önbelleğinden okunur (aynı fiyat dosyası + aynı COL_v1.py + aynı olay ayarı -> aynı olaylar; dosya adı bunların sha256'sıdır).

## 2. Evren, veri ve BİLGİ TARİHİ
- Fiyat: V_ABD.pkl (islenmis-veri dalı; 1.411 hisse; K24 cetvelinin evreni). Fon krizi: 2026-08-31 sonrası barlar atılır; 60 günlük penceresi bu tarihi aşan olay ölçülmez.
- AÇIK POZİSYON: FINRA iki haftalık açık pozisyon dosyaları (Rule 4560; borsa kotlu + OTC): `https://cdn.finra.org/equity/otcmarket/biweekly/shrtYYYYMMDD.csv`, ücretsiz, anahtarsız;
  en eski erişilebilen 2017-12-29 (daha eskisi 403; K63), son indirilen ödeme günü <= 2026-08-31. 14 sütun: accountingYearMonthNumber, symbolCode, issueName, issuerServicesGroupExchangeCode, marketClassCode, currentShortPositionQuantity, previousShortPositionQuantity, stockSplitFlag, averageDailyVolumeQuantity, daysToCoverQuantity, revisionFlag, changePercent, changePreviousNumber, settlementDate.
  Ödeme (settlement) günleri: ayın 15'i (ödeme günü değilse önceki ödeme günü) ve ayın son ödeme günü. `indir` her yuva için hafta içi adayları (15'inden ve ayın son
  gününden geriye 7 gün) sırayla dener; 403 / 404 sonraki adaya geçer; dosya 14 sütunlu başlık ve tek, dosya adıyla aynı ödeme günü taşımalıdır.
- **BİLGİ TARİHİ (geleceğe bakma kuralı):** bir raporun bilgi günü = ödeme gününün ABD işlem takvimindeki yeri (ödeme günü işlem günü değilse sonraki ilk işlem günü)
  + **12 işlem günü**; t günü yalnız **bilgi günü < t** olan raporlar kullanılır ve bunların EN SONUNCUSU (r0) alınır. Sembolün r0'da satırı yoksa
  değer YOK sayılır (daha eski rapora düşülmez). İşlem takvimi = V_ABD birleşik işlem günleri (FI_OLCUT panelinin takvimi).
  KAYNAK: FINRA 'About Equity Short Interest' ve 'Equity Short Interest Data Glossary' (finra.org/finra-data/browse-catalog/equity-short-interest): veriler 'ödeme
  gününden sonraki 7. iş gününde yayına verilir'; aracı kurumlar ödeme gününden sonraki 2. iş günü 18:00 ET'ye kadar bildirir (Rule 4560); FINRA 2026 takvimi
  (finra.org/filing-reporting/regulatory-filing-systems/short-interest; ör. 15.01.2026 -> 27.01.2026, 15.05.2026 -> 27.05.2026: 7. iş günü); SR-FINRA-2026-012
  ('yayın ödemeden 7 iş günü sonra'). Eski yıllarda yayının 8. iş günü olduğuna dair ikincil (doğrulanamayan) kaynak var. Dosya bazında gerçek yayın günü
  BULUNAMADI (CDN 'Last-Modified' alanı yeniden yükleme günüdür: shrt20180112.csv için 2023-07-27). Bu yüzden iş tanımındaki TUTUCU kural uygulandı: 12 işlem
  günü (7-8 iş gününe en az 4 işlem günü pay; yayın akşam olsa bile t günü kapanışında bilinir).
- REVİZYON: CDN dosyaları revizyonları içerir ('revisionFlag' = R; ilk yayımlanan değer elde yok). Revizyonlu satırlar kullanılır (sayısı §12'de); revizyon günü
  bilinmediği için küçük bir geleceğe bakma riski beyan edilir (§10).
- SEMBOL EŞLEMESİ: FINRA kodu = V_ABD sembolü (büyük harf, harf / rakam dışı karakterler atılır; V_ABD'de böyle karakter yok). İki V_ABD sembolü aynı koda düşerse ikisi de
  dışarıda kalır. **KİMLİK DENETİMİ** (k66_kimlik): FINRA satırının şirketi V_ABD fiyat serisinin şirketiyle aynı olmalı (V_ABD serisinin kimliği BUGÜNKÜ şirkettir; kod
  daha önce başka şirkete aitse eski satırlar başka şirketindir). Ölçü: oran = ADV(r) x b(r) / V_ABD ortalama günlük hacmi (önceki dosyanın ödeme gününden sonraki ilk
  işlem gününden bu ödeme gününe kadar, dahil = FINRA ADV'nin kendi penceresi; ilk dosyada ödeme - 14 takvim günü; en az 3 bar;
  b = ödeme gününden sonraki bölünme çarpanı, V_ABD hacmi bugünkü birimdedir). **1 / 3 <= oran <= 3** ise satır kabul; değilse ya da
  denetlenemiyorsa (ADV = 0, hacim yok) satır YOK. Yalnız ödeme günü ve öncesi hacim kullanılır: geleceğe bakmaz. Şirket adı yalnız BİLGİ olarak sayılır (§12).
  Pazar sınıfı süzgeci yok (OTC'den borsaya geçen şirketin OTC dönemi satırları da, kimliği doğrulanırsa, kullanılır; sayısı §12'de).
- PAY SAYISI: K60 demetindeki 'o gün bilinen' pay okuyucusu K60.k60_pay (K64 PAY_D ile aynı çağrı; kapak sayısı, yoksa bölünmesiz hissede bilanço / ağırlıklı
  ortalama pay; bilgi tarihi < t; BUGÜNKÜ pay biriminde). Halka açık pay (float) verisi YOK: oran toplam paya göredir (beyan; float'a göre oranlardan küçüktür).
- BÖLÜNME: K60 demetinin bölünme kayıtları (tarih, oran). Açık pozisyon bugünkü pay birimine çevrilir: SI x b(ödeme günü), b = ödeme gününden SONRAKİ bölünme
  oranlarının çarpımı (K59.k59_bolunme_carpan). SI_PAY'de pay da bugünkü birimde olduğundan t'den sonraki bölünmeler oranda sadeleşir (geleceğe bakmaz).

## 3. Değişkenler (hepsi yalnız t ve öncesi bilinen raporlarla; r0 = bilgi günü < t olan son rapor, r0 - k = ondan k önceki rapor (bütün dosyalar sırasında))
| kod | tanım | beklenti (bilgi) |
|---|---|---|
| SI_PAY | SI(r0) x b(r0) / PAY(t): son bilinen rapor r0'ın açık pozisyonu (bugünkü pay birimine bölünme çarpanı b ile) / t günü bilinen toplam pay (K60.k60_pay, bugünkü birim). PAY > 0; oran > 2 ise veri hatası sayılır (yok) | açığa satış oranı (yüksek = kötü haber beklentisi; Dechow vd. 2001, Asquith vd. 2005) |
| DTC | SI(r0) / ADV(r0): r0 raporunun açık pozisyonu / aynı raporun ortalama günlük hacmi (FINRA 'days to cover' formülü; dosyadaki 1,00 tabanı ve yuvarlama uygulanmaz); ADV > 0 | kapatma günü (Hong vd. 2016) |
| SI_DEG | ln(SI(r0) x b(r0) / (SI(r0-6) x b(r0-6))): son bilinen rapor ile 6 rapor (~3 ay) önceki rapor; ikisi de > 0. Aradaki 6 raporun birinde FINRA bölünme bayrağı varken K60 bölünme kaydında o aralıkta bölünme yoksa (düzeltilemiyor) yok | açık pozisyon artışı (proje ölçüsü) |
| SI_DEG1 | changePercent(r0) / 100: son raporun bir önceki rapora göre değişimi (dosyadaki alan); önceki pozisyon > 0; r0'da bölünme bayrağı ya da (r0-1, r0] aralığında bilinen bölünme varsa yok | kısa vade değişim (bilgi) |

Beklenti sütunu bilgidir: her değişken İKİ YÖNDE sınanır. DTC dosyadaki 'daysToCoverQuantity' alanının formülüdür (SI / ADV); dosya alanı <= 1 değerleri 1,00'a
basar ve ADV = 0'da 999,99 yazar, bu yüzden aynı iki alandan yeniden hesaplanır (SAPMA 1). SI_DEG1 dosyadaki 'changePercent' alanıdır.

## 4. S1 — 'etkileşim / ek katkı' (asıl soru; K64 §4 aynen, K64.k64_s1)
- Örneklem: yalnız ÇÖL OLAYLARI (tekil; FI_OLCUT ile ölçülebilen). 'EVREN' sırası = aynı gün evren içi yüzdelik sıra (n >= 30); 'İÇ' sırası = sinyal günü
  [t - 365 gün, t] aralığındaki tekil çöl olayları (kendisi dahil, n >= 30) içindeki sıra. ÜST = sıra >= 2/3, ALT = sıra <= 1/3.
- **KARAR SIRASI: İÇ (çöl içi sıra)** (bütün K66 ailesi için). EVREN sırası 'sağlamlık, karar dışı' (karara ve BH ailesine GİRMEZ).
  SEÇİM KURALI (eşikler kapsam sayımı KOŞULMADAN koda yazıldı; k66_sira_sec): ANA tanım, bağımsız dönemler, her değişken için EVREN sırasıyla pencereli ÜST ve ALT olay
  sayısı; bir hücrede küçük grup < 30 ya da küçük / büyük < 0.5 ise çöl olayları evren sırasında bir uçta TOPLANIYOR; herhangi bir hücrede toplanma
  varsa İÇ, yoksa EVREN. Uygulama: toplanma olan hücre: SI_PAY 2022-2026 (ÜST 1451 / ALT 620, oran 0,43) -> İÇ. Ayrıntı §12'de. **Kapsam sayımı görüldü, getiri görülmedi** (hiçbir getiri / eşli fark hesaplanmadı). `onkayit` kapsam
  dosyasındaki kural sonucu ile mühürdeki karar sırası aynı değilse yazmaz.
- Temel model = hücredeki BÜTÜN çöl olayları (değişkensiz). ÜST - ALT = ortalama eşli farkların farkı; ay kümeli bootstrap (2000 çekiliş, tohum 66001;
  iki grubu dolu çekiliş payı < %90 ise aralık yok); %95 aralık = 2.5 / 97.5 yüzdelikleri.
- **'EK KATKI VAR (yön ÜST)'** <=> n_ÜST >= 30 ve n_ALT >= 30 VE ÜST grubunun ortalama eşli farkı > temel modelin VE (ÜST - ALT) %95 alt sınırı > 0.
  **'EK KATKI VAR (yön ALT)'** ayna: ALT grubunun ortalama eşli farkı > temel VE (ÜST - ALT) %95 üst sınırı < 0.

## 5. S2 — 'tek başına' (bilgi; K64 §5 aynen, K64.k64_s2)
Çöl DIŞI evrende, ANA çöl sinyali olan günlerde, değişkenin evren içi ÜST / ALT üçte birindeki hisselerin (giriş = ertesi takvim günü açılışı) 60 günlük eşli farkı ve
ÜST - ALT (ay kümeli bootstrap; 2000 çekiliş, tohum 66002). 'Çöl dışı' = o gün ve önceki 59 işlem gününde tekil ANA çöl sinyali vermemiş hisse.

## 6. Cetvel (FON_IZI FI_OLCUT aynen; K64 §6 aynen)
FI_OLCUT = {"ufuk": 60, "mom": 60, "likit": 20, "mom_kova": 5, "likit_kova": 3, "kriz": "2026-08-31", "bootstrap": 2000, "tohum": 27, "slot": 10, "n_esik": 30, "port_n": 200, "port_yuzde": 0.9}.
- fi_olcut_panel / fi_olcut_olay / fi_olcut_hucre (K64.k64_olc, k64_hucre): giriş = sinyalden sonraki ilk işlem günü açılışı; r60; EŞLİ FARK = r60 - aynı giriş günü aynı
  momentum beşliği x likidite üçlüsü hücresindeki öteki hisselerin ortalama r60'ı; HÜCRE TUTAR <=> n >= 30, aralığın alt ucu > 0, ortalama sıra > 0,50, portföy >
  rastgele %90. Piyasa koşulu katmanı (eşit ağırlıklı evren endeksi 200 günlük ortalamasının üstü / altı; bilgi). Ek ufuk r20 (bilgi).
- MALİYET: ABD gidiş-dönüş 20 bp her olayın getirisinden ve eşli farkından düşülür; rastgele eş portföyler maliyetsiz (tutucu).

## 7. Hücreler ve KARAR (K64 §7 kuralı aynen; K64.k64_karar)
- Hücre = ABD x dönem (giriş gününe göre): 2018-2021 (2018-01-01 .. 2021-12-31), 2022-2026 (2022-01-01 .. 2026-12-31), 2023-2026 (2023-01-01 .. 2026-12-31). Bağımsız dönemler 2018-2021 ve 2022-2026; 2023-2026 örtüşür (tutarlılık; BH ailesine girmez).
- Karar birimi: (değişken, yön); ANA tanım (K24) ve KARAR sırası (İÇ (çöl içi sıra)).
- **'ADAY'** <=> iki bağımsız dönemin İKİSİNDE de aynı yönde 'EK KATKI VAR' ve ikisi de BH'den geçiyor. İki bağımsız dönemden birinde n_ÜST ya da n_ALT < 30
  ise **'ÖLÇÜLEMEZ'** ('İZ DEĞİL' ile karıştırılmaz). Aksi **'İZ DEĞİL'**.
- İŞARET: ölçülebilen bütün hücrelerde (üç dönem) ÜST - ALT nokta farkının işareti yönle aynı olmalı; dönerse aday düşer.
- Genel karar en fazla **'ABD-ADAY'**: İZ = ABD + Avrupa; Avrupa açığa satış verisi bu işte yok (AVRUPA VERİSİ YOK). Grubun dört şartı (brüt / net) ayrıca yazılır.

## 8. Çoklu test
Aile = ANA tanım, KARAR sırası, ölçülebilen bütün (değişken x yön x bağımsız dönem) hipotezleri: en çok 4 x 2 x 2 = 16 (yalnız ABD).
p = 1 - Φ(±(ÜST - ALT) / bootstrap standart sapması) (tek yönlü). Benjamini-Hochberg q = %10 (K60.k60_bh); Bonferroni bilgi olarak yazılır.
K64 / K65'in 84 hipotezlik ailesiyle birleştirilmez (ayrı soru, ayrı veri); ana oturum isterse birleşik BH'yi raporda ayrıca hesaplar.

## 9. GÜÇ BEYANI
K58 (arastirma_cikti/k58_cetvel_sagla/K58_RAPOR.md): FI_OLCUT, 60 günde +%2'lik gerçek etkiyi n = 300 olayda yalnız %11, +%4'ü %45 olasılıkla yakalıyor. Çöl olayları
içindeki üçte bir grupları birkaç yüz olaydır (§12). Her hücrede n ve 'saptanabilir en küçük etki' (aralık yarı genişliği) raporlanır. n < 30 hücre 'ÖLÇÜLEMEZ'dir;
'ek katkı yok' 'etki yok' demek değildir, 'bu veriyle gösterilemedi' demektir.

## 10. Yanlılık beyanı
- YAŞAYAN YANLILIĞI: V_ABD yalnız BUGÜN işlem gören hisselerdir. Yüksek açığa satışlı çöl hisseleri batmaya en açık gruptur; batanlar örneklemde yok, bu grubun
  getirisi YUKARI yanlıdır (yüksek açık pozisyonun kötü haberi örneklemde eksik görünür). Eşli kontrol aynı evrenden seçildiği için yanlılığın bir kısmı farkta götürülür.
- SEMBOL: eşleme bugünkü kodla yapılır; kod değiştiren şirketlerin eski koddaki satırları eşleşmez (veri yok); eski kodu başka şirkete ait satırlar kimlik (hacim)
  denetimiyle düşer. Hacimleri tesadüfen 3 kat içinde olan farklı iki şirketin satırı tam dışlanamaz; kimliği doğru bir satır olağan dışı hacim farkıyla düşebilir.
- OTC satırları: FINRA dosyası OTC menkul kıymetlerini de kapsar; V_ABD sembolüyle eşleşen OTC satırları (OTC'den borsaya geçiş) kullanılır.
- TOPLAM PAY, FLOAT DEĞİL: SI_PAY halka açık paya göre değil toplam paya göredir; kurucu / içeriden payı yüksek şirketlerde oran olduğundan küçüktür.
- REVİZYON: CDN dosyaları sonradan düzeltilmiş değerleri taşıyabilir (revisionFlag); düzeltme günü bilinmiyor.
- FINRA açık pozisyonu aracı kurum bildirimidir (Reg SHO Rule 200 'short' hesapları); piyasa yapıcı ve bazı kurumsal pozisyonlar eksik / gecikmeli olabilir.
- K24 sinyali yalnız fiyatla tanımlıdır (sektör rüzgârı / katalizör şartı yok; K64 §10).

## 11. SAPMA / BOŞLUK listesi (iş tanımına göre; en dar yorum)
SAPMA 1. DTC dosyadaki alan yerine aynı iki alandan (currentShortPositionQuantity / averageDailyVolumeQuantity) yeniden hesaplanır: dosya alanı 1'in altını 1,00'a basar
  (bağ; §12'de pay) ve ADV = 0'da 999,99 yazar; 1'in üstünde iki değer 0,01 içinde birebir aynıdır (K66 örnek dosya denetimi).
SAPMA 2. Dönemler 2018-2021 / 2022-2026 / 2023-2026 (K64'te 2017-2021): FINRA verisi 2017-12-29'dan başlar; 2018-2021, 2017-2021'in veri olan kısmıdır. İlk bilgi günü
  Ocak 2018 ortasıdır; SI_DEG için 6 rapor geçmiş gerektiğinden ~Nisan 2018'den önce yok.
SAPMA 3. Evren yalnız ABD (BIST VERİSİ YOK); karar pazarı ABD; BH ailesi en çok 16 hipotez.
SAPMA 4. Bootstrap tohumları 66001 / 66002 (K64: 64001 / 64002); yöntem aynı.
SAPMA 5. Kimlik denetimi ilk taslakta İSİM eşleşmesiydi (satırdaki adın ilk kelimesi = bugünkü adın ilk kelimesi). Kapsam incelemesinde (yalnız satır sayıları ve
  adlar; getiri görülmedi) adını değiştiren şirketlerin (ör. XOM, NEE, SLB, MSTR, CPB) bütün geçmişini düşürdüğü, kod yeniden kullanımını (ör. BNY: eski satırlar bir
  belediye tahvili fonu) ise hacimle de yakalanabildiği görüldü; ayrıca bugünkü ad sonraki bilgidir. Ön kayıttan ÖNCE hacim uyumuna çevrildi; isim yalnız bilgi.
BOŞLUK 1. Bilgi tarihi tutucu kuralı (ödeme + 12 işlem günü; dosya bazında yayın günü bulunamadı; kaynak §2).
BOŞLUK 2. r0 kuralı: yalnız en son kullanılabilir rapor; sembolün o raporda satırı yoksa değer yok (eski rapora düşülmez).
BOŞLUK 3. SI_DEG adımı bütün dosyalar sırasında 6 rapordur (iki rapor arası ~yarım ay; 6 rapor ~3 ay). Bölünme: K60 bölünme kayıtlarıyla bugünkü birime çevrilir;
  FINRA bölünme bayrağı aradaki raporlarda varken K60 kaydında o aralıkta bölünme yoksa değer yok.
BOŞLUK 4. SI_DEG1 = dosyadaki changePercent / 100; önceki pozisyon 0 (dosya %100 yazar) ya da r0'da bölünme bayrağı / bilinen bölünme varsa yok.
BOŞLUK 5. SI_PAY > 2.0 (toplam payın iki katı) veri hatası sayılır; pay <= 0 / yoksa değer yok.
BOŞLUK 6. Sıfır açık pozisyon geçerli değerdir (SI_PAY = 0, DTC = 0); SI_DEG'de ln için iki uç da > 0 olmalı.
BOŞLUK 7. Kimlik denetiminin bandı 3 kat, penceresi FINRA ADV penceresidir (§2); bant FINRA ADV ile V_ABD hacminin birebire yakın olmasına göre seçildi
  (kapsam incelemesi: medyan log10 oran 0; §12) — getiri görülmedi.
BOŞLUK 8. Aynı dosyada iki kez geçen kod o dosyada atılır (§12'de sayısı).
BOŞLUK 9. K64 BOŞLUK 2, 7, 8, 9, 11-14 aynen geçerlidir (giriş gününe göre dönem; evren sırası için 'uygun hisse'; piyasa koşulu endeksi; D13 haftalık ızgara; maliyet;
  S2 girişi; fi_k24_tara ileriye bakan sütunları kullanılmaz; işaret şartında 0 tutmaz).

## 12. Kapsam (yalnız SAYI; mühre girmez)
Kapsam sayımı (2026-11-12 04:37:18 UTC; `python -I K66.py kapsam`; yalnız SAYI: getiri, eşli fark, FI_OLCUT paneli hesaplanmadı).

- ABD: 1411 hisse (K60 demetinde 1406), takvim 2830 gün (2015-06-01 .. 2026-08-31).
- FINRA: 209 dosya, ödeme günleri 2017-12-29 .. 2026-08-31, toplam 3949157 satır (yinelenen kod satırı 0); V_ABD sembolü eşleşen 1411 / 1411; eşleşen satır 248376; KİMLİK denetiminden geçen satır 246298 (en az bir satırı geçen sembol 1411), reddedilen 2078; log10(ADV x b / V_ABD hacmi) yüzdelikleri 1 / 5 / 50 / 95 / 99: -0.090, -0.050, -0.000, 0.000, 0.013. İsim (bilgi): adı bugünküyle uyuşmayan satır 5179 (bunların kimliği doğrulanan 3969), adı uyuşup kimliği reddedilen 868. OTC sınıfı satır 1237, revizyon bayraklı 4737, bölünme bayraklı 203; çakışan kod 0. Dosyadaki DTC'nin 1,00 tabanında olduğu satır payı %3.8; ADV = 0 payı %0.0.
- Bilgi tarihi: takvim içinde kullanılan rapor 207; ödeme günü -> bilgi günü takvim günü farkı en az 16, medyan 18.0, en çok 21. Evren hisse-günlerinde (2018-01-01 ->) değişken doluluk: DTC %92, SI_DEG %89, SI_DEG1 %92, SI_PAY %83.

**K24 olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay)

| pazar | dönem | ham | tekil | pencere |
|---|---|---|---|---|
| ABD | 2018-2021 | 2661 | 2346 | 2346 |
| ABD | 2022-2026 | 4319 | 3721 | 3519 |
| ABD | 2023-2026 | 3091 | 2670 | 2468 |

**K24: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | ABD 2018-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|
| SI_PAY | EVREN | 1847 / 859 / 463 | 2995 / 1451 / 620 | 2107 / 1083 / 395 |
| SI_PAY | İÇ | 1847 / 566 / 618 | 2995 / 1081 / 947 | 2107 / 824 / 598 |
| DTC | EVREN | 2065 / 673 / 737 | 3347 / 1085 / 1263 | 2360 / 785 / 891 |
| DTC | İÇ | 2065 / 653 / 699 | 3347 / 1102 / 1119 | 2360 / 809 / 770 |
| SI_DEG | EVREN | 1965 / 770 / 587 | 3300 / 1307 / 974 | 2330 / 958 / 660 |
| SI_DEG | İÇ | 1965 / 607 / 688 | 3300 / 1112 / 1073 | 2330 / 802 / 755 |
| SI_DEG1 | EVREN | 2059 / 785 / 667 | 3335 / 1269 / 1020 | 2349 / 902 / 713 |
| SI_DEG1 | İÇ | 2059 / 662 / 696 | 3335 / 1112 / 1086 | 2349 / 795 / 759 |

**D13 olayları** (ham = tekilleştirme öncesi; tekil = 60 işlem günü kuralı sonrası; pencere = 60 günlük penceresi 31.08.2026 kesiğinden önce biten tekil olay; D13'te yalnız GECER)

| pazar | dönem | ham | tekil | pencere |
|---|---|---|---|---|
| ABD | 2018-2021 | 1952 | 1236 | 1236 |
| ABD | 2022-2026 | 3278 | 2084 | 1958 |
| ABD | 2023-2026 | 2430 | 1534 | 1408 |

**D13: değişken kapsamı ve üçte bir grupları** (pencereli tekil olaylar; EVREN = aynı gün evren içi sıra, İÇ = çöl içi sıra; hücre = değer / ÜST / ALT)

| değişken | sıra | ABD 2018-2021 | ABD 2022-2026 | ABD 2023-2026 |
|---|---|---|---|---|
| SI_PAY | EVREN | 993 / 399 / 273 | 1724 / 665 / 496 | 1239 / 489 / 340 |
| SI_PAY | İÇ | 993 / 341 / 309 | 1724 / 612 / 531 | 1239 / 459 / 361 |
| DTC | EVREN | 1095 / 430 / 318 | 1876 / 664 / 597 | 1360 / 490 / 428 |
| DTC | İÇ | 1095 / 359 / 346 | 1876 / 609 / 626 | 1360 / 462 / 425 |
| SI_DEG | EVREN | 1048 / 347 / 334 | 1866 / 636 / 600 | 1350 / 467 / 439 |
| SI_DEG | İÇ | 1048 / 347 / 332 | 1866 / 645 / 603 | 1350 / 450 / 453 |
| SI_DEG1 | EVREN | 1083 / 338 / 350 | 1875 / 620 / 581 | 1359 / 457 / 409 |
| SI_DEG1 | İÇ | 1083 / 341 / 354 | 1875 / 650 / 616 | 1359 / 470 / 446 |

**Karar sırası seçim kuralı uygulaması** (ANA tanım, bağımsız dönemler, EVREN sırası; toplanma = küçük grup < 30 ya da küçük / büyük < 0.5): SI_PAY 2018-2021 ÜST 859 / ALT 463 (oran 0.54); DTC 2018-2021 ÜST 673 / ALT 737 (oran 0.91); SI_DEG 2018-2021 ÜST 770 / ALT 587 (oran 0.76); SI_DEG1 2018-2021 ÜST 785 / ALT 667 (oran 0.85); SI_PAY 2022-2026 ÜST 1451 / ALT 620 (oran 0.43, TOPLANMA); DTC 2022-2026 ÜST 1085 / ALT 1263 (oran 0.86); SI_DEG 2022-2026 ÜST 1307 / ALT 974 (oran 0.75); SI_DEG1 2022-2026 ÜST 1269 / ALT 1020 (oran 0.80). Kuralın sonucu: **İÇ**.

ANA tanım, KARAR sırası (İÇ), bağımsız dönemlerde grubu n < 30 olan (karar kuralında 'ÖLÇÜLEMEZ' kalacak) hücreler (pencereli olay sayısıyla; ölçülebilen olay daha az olabilir): yok.

## 13. Çıktılar ve komutlar
Çıktılar arastirma_cikti/col_dis_bilgi/: k66_olaylar.csv.gz, k66_s1.csv, k66_s1_fark.csv, k66_s2.csv, k66_karar.csv, k66_meta.json, K66_RAPOR.md
(k66_kapsam.csv, k66_kapsam_ozet.json: kapsam). Raporda her değişken için: veri kaynağı ve kapsamı, tanım, örneklem, ortalama ve medyan getiri (20 ve 60 gün),
eşli fark, güven aralığı, dönemler arası tutarlılık, maliyet sonrası sonuç, veri eksikleri, karar.
1. (ana oturum) bu dosyayı denetler ve git'e işler.
2. `python -I K66.py kos`  -> ölçüm + rapor (mühür, veri sha256, K60 verisi, git doğrulanır)
3. `python K66.py rapor`   -> raporu çıktılardan yeniden yazar

## 14. Değişmezlik
K66_ESIK ya da içe alınan tanımlar (FI_K24, FI_OLCUT, K60 bilgi kuralı ve mührü, COL_v1 D13 sabitleri, K64 mührü) değişirse ESIK_SHA256 değişir ve koşu durur. Veri
(V_ABD, FINRA dosyaları), içe alınan ön kayıtlar (K60, K64 + K65) ya da kod dosyaları (FON_IZI.py, K60.py, K59.py, COL_v1.py, K64.py) değişirse sha256 tutmaz ve koşu durur.
