# DÜŞÜŞ SONRASI — ELEŞTİRİ VE HAVUZ (KOL E, 20 Kasım 2026)

Yazan: KOL E alt ajanı (eleştirmen + havuz kurucu). Web yok, URL açılmadı, ölçüm yok, fiyat okunmadı, getiri hesaplanmadı. Yasak defter dosyalarına dokunulmadı, commit yok.
Girdi: WEB_A (25), WEB_B (36), WEB_C (24), WEB_D (38) = 123 hipotez; DS_OLCUM_CERCEVE.md; SINYAL_ENVANTERI.md; KURAL_DEFTERI_TASLAK.md (A-K, K1-K51); HAKEM_DERSLER.md + GOZ_ETIKET_IS_TANIMI.md (C1-C13, CD1-CD23, VD1-VD11); COL_OZET.md kapalı konular; IZ_VERI_ENVANTERI.md bölüm 0 (+ ilgili satırlar); KAZANANLAR_2026-10-22.md (H1-H3); WEB_SEKIL_METRIKLERI.md; WEB_GUNCEL_SISTEMLER_2026-11-19.md; GEMINI_ARASTIRMA_2026-11-19.md (tekrar kontrolü).
Bu dosya ön kayıt DEĞİLDİR. Eşikler kaynaktan; kaynakta yoksa "eğitim 2016-22 medyan / çeyrek, sonuç görülmeden" yazıldı. Hiçbir eşik sonuca göre seçilmedi (sonuç yok).

## 0. ÖZET
- 123 hipotez → tekilleştirme sonrası **87 DS** (DS01-DS87).
- Süzgeçten geçen **56**: sınıf **I = 29** (OHLCV, ABD + AVR, t'de bilinir), sınıf **II = 10** (ABD-OLAY: sec_ozet / Form 4 / Yahoo; AVR karşılığı yok → en fazla ABD-ADAY), sınıf **III = 17** (İNDİR gerekir).
- Kalan **31**: piyasa KOŞULU 3, KAPALI 5, bağlam dışı 1, K1 mekanik / tanımca boş küme 3, kova ile sıfırlanan 1, tanım yok 1, veri yok 5, 15 bar ölçülemez / DS olayına girmez 4, mevcut (envanterde / K51) 7, başvuran kimliği yok 1.
- Öncelik listesi: sınıf I'den **25** DS, her birinin **tek ANA kolu** BH'ye girer (m = 25 sabit, q 0,10); öteki kollar BİLGİ. Sosyal / blog İDDİA'sı listede 2 (sınır 5).
- Yön çelişkisi: **34** madde (bölüm 4); 17 DS ön kayıtta "iki yönlü test" işareti taşır.
- Kollar arası ÇELİŞKİ 14, kendi HATA listem 12 madde. En önemli üç bulgu: (1) C7 'geri alma hızı' eşiği (R18 ≥ 0,5) DS olay tanımıyla (F15 ≤ 0,25) neredeyse boş küme verir; (2) A10 (52h dibi yakınlığı) olay tanımıyla mekanik eşdeğer; (3) sınıf III'teki EDGAR tam metin olaylarının hepsi SEC User-Agent e-postası ister (Cemal izni gerekir).

## 1. TEKİLLEŞTİRME (123 → 87)

Kural: aynı ölçüyü (aynı referans, aynı yön mantığı) anlatan satırlar tek DS; farklı referanslı ama aynı aileden satırlar tek DS altında KOL olur (ANA kol bölüm 3'te). Sayım kontrolü: A 25 + B 36 + C 24 + D 38 = 123, hepsi aşağıda tam bir kez geçer.

| DS | birleşik hipotez (kısa ad) | kollar | kodlar | sonuç |
|---|---|---|---|---|
| DS01 | Fiyat yolu konveksliği (kazan / hızlanan düşüş) | A | A14 | I |
| DS02 | Kaybeden × devir (düşük devir döner, yüksek sürer) | A | A2, A12 | I |
| DS03 | Sektör (AVR: piyasa) artığı son ay düşüşü döner | A | A4 | I |
| DS04 | Büyük tek gün düşüşü / dead-cat fazı | A, B | A18, A19, B21, B22 | I |
| DS05 | Kapitülasyon / satış doruğu (geniş aralık + hacim) | A, B, C | B12, C15, C16, A11, A13 | I |
| DS06 | Dip süpürme + geri alma (Turtle Soup, spring, likidite süpürme, Oops) | B, C | B24, C1, C2, B26, B14 | I |
| DS07 | Smash day dönüşü | B | B25 | I |
| DS08 | Weinstein evresi / ortalama eğimi | B | B10, B9 | I |
| DS09 | RSI(2) aşırı satım | B | B1, B4 | I |
| DS10 | DV2 aşırı satım | B | B2 | I |
| DS11 | Kapanış 7 gün dibinde (Double 7) / H2 düşen bıçak | B (+ KAZANANLAR H2) | B3 | I |
| DS12 | Elder Impulse kırmızıdan çıkış | B | B8 | I |
| DS13 | TD Sequential setup 9 / countdown 13 | B | B5, B6 | I |
| DS14 | Düşüş direnci kırılımı (CHoCH / TDST / trend çizgisi) | B, C | C5, B7, B19 | I |
| DS15 | Busted aşağı kırılım | B | B23 | I |
| DS16 | Wyckoff ikinci test | B | B13 | I |
| DS17 | Aşağı gün direnci (asimetrik göreli güç) | B | B17 | I |
| DS18 | Göreli güç eğimi / göreli dip uyumsuzluğu | C | C17, C18 | I |
| DS19 | Bollinger %b W dip | B | B27 | I |
| DS20 | Alt bantta yürüme (−) | B | B28 | I |
| DS21 | Düşüşte gece payı (−) | B | B34 | I |
| DS22 | Aşağı boşluk / dengesizlik doldurma | C | C11, C4 | I |
| DS23 | Yukarıda mıknatıs (dolmamış boşluk / eşit tepeler +%5..+%10) | C | C12, C13 | I |
| DS24 | Yukarı FVG (3 bar itki) | C | C3 | I |
| DS25 | AVWAP (dipten çapalı test / tepeden çapalı geri alma) | C | C8, C9 | I |
| DS26 | POC süpürme + geri alma | C | C10 | I |
| DS27 | 50 gün ortalamadan ATR katı gerilme | C | C14 | I |
| DS28 | Düşüş derinliği | A, C | C23 (+ A1 derinlik kolu) | I |
| DS29 | P&F hedef / alt direk dönüşü | B | B20, B32 | I (öncelik dışı, H15) |
| DS30 | 52 hafta dibi yakınlığı | A | A10 | ELENDİ (g) |
| DS31 | Dipten 18 barda yarı geri alma hızı | C | C7 | ELENDİ (g, boş küme) |
| DS32 | Boyut × düşüş (büyük mü küçük mü) | A, C | C22 (+ A1 küçük kolu) | ELENDİ (kova ile sıfırlanır) |
| DS33 | Order block geri dönüşü | C | C6 | ELENDİ (tanım yok) |
| DS34 | Beklenen kazanç ≥ 3 x zarar | B | B18 | ELENDİ (g) |
| DS35 | Yükseliş / düşüş günü hacim oranı | B | B16 | KAPALI |
| DS36 | Piyasa geçmişte düşmüş (ayı) | A | A5 | KOŞUL |
| DS37 | Zweig genişlik hamlesi | B | B29 | KOŞUL |
| DS38 | Takip günü (FTD) | B | B30 | KOŞUL |
| DS39 | VIX yüksek | A | A6 | KAPALI |
| DS40 | Evre 2 hacim patlaması / SOS + LPS | B | B11, B15 | KAPALI |
| DS41 | Connors çıkışları / TD stop | B | B35, B36 | KAPALI |
| DS42 | RSI7 zayıflıkta al vs onay | C | C21 | KAPALI |
| DS43 | Darvas kutusu | B | B31 | bağlam dışı |
| DS44 | Habersiz büyük düşüş döner, haberli sürer | A, C | A3, C19 | II |
| DS45 | Konveks yol × not düşürme | A | A15 | II |
| DS46 | Düşüş sonrası içeriden alım | A, D | A20, A21, D3 | II |
| DS47 | Zorunlu CEO değişimi + ilk bilanço kötü → V | D | D5 | II |
| DS48 | Form 144 satış niyeti | D | D13 | II |
| DS49 | Yeni pasif %5 ortak (13G) | D | D14 | II |
| DS50 | 8-K 2.03 yeni borç / kredi | D | D20 | II |
| DS51 | 8-K 2.04 borç hızlandırma (−) | D | D21 | II |
| DS52 | 8-K 1.02 sözleşme feshi (−) | D | D22 | II |
| DS53 | Ters bölünme / ortak hakları değişimi (3.03) | D | D7, D23 | II (KISMEN) |
| DS54 | 13G → 13D geçişi | D | D15 | ELENDİ (c) |
| DS55 | Düşen bıçak × ucuz (EV/Satış) | A | A1 | III |
| DS56 | Sıkıntı × kaybeden | A | A8, A25 | III |
| DS57 | F-skoru × kaybeden | A, B, C | A17, B33, C24 | III |
| DS58 | Açık piyasa geri alım programı duyurusu (+ BIST KAP) | A, D | A9, D1, D28 | III |
| DS59 | Hızlandırılmış geri alım (ASR) (−) | D | D2 | III |
| DS60 | Opsiyon dibi (plan dışı CEO tahsisi) | D | D4 | III |
| DS61 | Going concern kalkması | D | D6 | III |
| DS62 | 'Stratejik seçenekler' duyurusu (−) | D | D8 | III |
| DS63 | Borç takas teklifi (duyuru − / tamamlanma +) | D | D9 | III |
| DS64 | Açık pozisyon eğilimi ve kârla / zararla kapanış | D | D16, D17 | III |
| DS65 | Önceden duyurulmuş yatırımcı günü | D | D18 | III |
| DS66 | Hükûmet / savunma sözleşmesi | D | D19 | III |
| DS67 | Temettü kesip yeniden başlatma | D | D24 | III |
| DS68 | Dava uzlaşması | D | D26 | III |
| DS69 | Nasdaq uyumu yeniden kazanma | D | D27 | III |
| DS70 | S&P 500'den çıkarma | A, D | A22, D11 | III |
| DS71 | Russell 1000 → 2000 göçü | D | D12 | III |
| DS72 | İflastan çıkan yeni hisse | D | D10 | ELENDİ (DS olayına girmez) |
| DS73 | Fon çıkışı zorunlu satış | A, D | A7, D25 | ELENDİ (d) |
| DS74 | Not düşürme dalgası sonrası dönüş | A | A16 | ELENDİ (d) |
| DS75 | 13F kurumsal artış | D | D37 | ELENDİ (a, d) |
| DS76 | PDUFA öncesi koşu | D | D29 | MEVCUT (H3 / K51) |
| DS77 | Aktivist 13D | D | D30 | MEVCUT (ACT_13D) |
| DS78 | Analist yükseltme dalgası | D | D31 | MEVCUT (REC_UP) |
| DS79 | ATM / raftan satış | D | D33 | MEVCUT (E_424B5) |
| DS80 | Kayıtsız satış 3.02 | D | D34 | MEVCUT (E_302) |
| DS81 | Endekse ekleme | D | D35 | MEVCUT (E_IDX_ADD) |
| DS82 | Spin-off | D | D36 | MEVCUT (E_SPINOFF) |
| DS83 | Öngörü yükseltme | D | D32 | VERİ YOK (GUIDANCE_UP) |
| DS84 | Google arama ilgisi | A | A23 | VERİ YOK |
| DS85 | Opsiyon IV çarpıklığı | A | A24 | VERİ YOK |
| DS86 | Reddit anılma + hacim | C | C20 | VERİ YOK |
| DS87 | Birleşme söylentisi | D | D38 | VERİ YOK |

Birleştirme gerekçeleri (tek satır): DS04 dört satırın hepsi "tek günlük büyük düşüş + sonrası" (eşik −%15 ya da kendi %2,5 yüzdeliği), fark yalnız zaman fazı; DS05 hepsi "düşüşte geniş aralık + hacim sıçraması" (A11 52h dip kırılımı + hacim bu ailenin değişkeni); DS06 hepsi "önceki dibin altına sarkıp kapanışta üstüne dönme", referans dip farklı (20 gün dibi, onaylı pivot, eşit dipler, önceki gün dibi); DS08 her ikisi "ortalama düşüyorsa bıçak sürer"; DS14 hepsi "son alçalan tepe / direnç kapanışla aşıldı"; DS22 her ikisi "aşağı boşluğun kapanışla doldurulması"; DS23 her ikisi "+%5..+%10'da çekici seviye"; DS25 her ikisi AVWAP; DS46 üçü "düşüşteki içeriden alım"; DS57 üçü "kaybeden × kalite".

## 2. SÜZGEÇ (her DS için)

Sütunlar soru olarak: (a) YENİ mi (envanter / 19 Kas dosyaları / K1-K51 / C1-C13 / Ç kayıtlarında ÖLÇÜLMEMİŞ; listede olup ölçülmemiş = YENİ, 'K' notu); (b) t'de bilinir mi; (c) bugün bizdeki EVET veriyle hesaplanır mı; (d) 15 bar cetvelle ölçülebilir mi; (e) kapalı konu mu; (f) aynı gün eşli farkla sıfırlanan piyasa koşulu mu; (g) K1 mekanik üstünlük riski yüksek mi. GEÇER = a EVET, b EVET, d EVET, e HAYIR, f HAYIR, g HAYIR; c EVET → I / II, c HAYIR (İNDİR) → III. "HAYIR*" = sınırda, ana model kararı gerekir (gerekçe notta).

| DS | a | b | c | d | e | f | g | sonuç | neden (tek cümle) |
|---|---|---|---|---|---|---|---|---|---|
| DS01 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Konvekslik hiçbir listede yok; kapanıştan hesaplanır; içbükeylik H2 ile örtüşür (orta risk, ATRP kovası). |
| DS02 | EVET | EVET | EVET | EVET | HAYIR* | HAYIR | HAYIR | I | Etkileşim yok (STREV_1M, TURN_12M ayrı); 'hacim kuruması' öbek ek şartı olarak kapalı, burada aylık devir düzeyi → ana model kararı. |
| DS03 | EVET | EVET | EVET (ABD sektör; AVR piyasa artığı) | EVET | HAYIR | HAYIR | HAYIR | I | Ölçülen artık kısımdır, sektör ısısı değil; sektör sınıfı bugünkü (K2 notu). |
| DS04 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Olay günü s ≤ t; bölünme hatası −%15 günü üretebilir (K6 denetimi şart). |
| DS05 | EVET (K: VOL_SHOCK, CLV parçalı) | EVET | EVET | EVET | HAYIR* | HAYIR | HAYIR | I | Doruk barı girişten önceki geçmiş olaydır, giriş mumu hacim onayı değil; VOL_SHOCK ile aynı ana model kararı. |
| DS06 | EVET (K: GEMINI #20 listede, ölçülmedi) | EVET (pivot 6 bar onay) | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Kapanışla geri alma t'de tamam; Oops kolu açılışa dayanır (AVR K6). |
| DS07 | EVET | EVET | EVET | EVET | HAYIR* | HAYIR | HAYIR | I | Tetik 'ertesi gün tepe aşımı' t'de tamamlanmış durum özelliği olarak alınır (onay ailesi notu). |
| DS08 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR* | I | DS olaylarının çoğu EVRE4'tür: eş azlığı / güç riski (mekanik değil ama ayırt edicilik düşük). |
| DS09 | EVET (K: E14 RSI14 eski cetvel) | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | RSI(2) ölçülmedi; RSI ailesi 60 günle TUTMADI*, 15 bar ile yeniden açılabilir (UFUK 15). |
| DS10 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | IBS / CLV'den farklı (2 gün düzleştirme + kendi geçmişine sıra). |
| DS11 | EVET (K: H2 planlı, ölçülmedi) | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR* | I | H2 ile aynı ön kayıtta tek satır olmalı (çift sayım yok); dipte sık görülür. |
| DS12 | EVET (K: MACD bataryada) | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | EMA eğimi + histogram eğimi birleşimi ölçülmedi. |
| DS13 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Sayımlar t'de tamamlanır; countdown n küçük olabilir. |
| DS14 | EVET (K: Donchian WEB_SEKIL #19, S6 tavanı) | EVET (pivot 6 bar) | EVET | EVET | HAYIR* | HAYIR | HAYIR | I | Kırılım = 'onay' ailesi; durum özelliği olarak sınanır, giriş zamanlaması karşılaştırması değil. |
| DS15 | EVET | EVET | EVET (S6 / YAPI_HEDEF bölgesi içe alınır) | EVET | HAYIR | HAYIR | HAYIR | I | Bölge t'de tamamlanmış S6 bölgesinden; DS içinde n küçük olabilir. |
| DS16 | EVET | EVET | EVET | EVET | HAYIR* | HAYIR | HAYIR | I | Hacim daralması doruk barına göre (öbek hacim kuruması değil) → ana model kararı. |
| DS17 | EVET (K: RS_BIST toplam) | EVET | EVET (evren eşit ağırlık) | EVET | HAYIR | HAYIR | HAYIR* | I | Düşük beta ile örtüşür; ATRP kovası kısmen kontrol eder. |
| DS18 | EVET | EVET (kırılım öncesi eğim) | EVET (evren endeksi vekil) | EVET | HAYIR | HAYIR | HAYIR | I | Bulkowski'nin kırılım SONRASI RS'i kullanılmaz (geleceğe bakar). |
| DS19 | EVET (K: E14 uyumsuzluk ailesi, %b yok) | EVET (pivot 6 bar) | EVET | EVET | HAYIR | HAYIR | HAYIR | I | %b uyumsuzluğu ölçülmedi. |
| DS20 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR* | I | Dipteki olayda bant altı kapanış sık; derinlikle ilişkili. |
| DS21 | EVET (K: GAP_OVN toplam) | EVET | EVET (AVR açılış temizliği şart) | EVET | HAYIR | HAYIR | HAYIR | I | Düşüşün bileşimi (pay) envanterde yok. |
| DS22 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Dolum DS konumuyla (alt çeyrek) gerilim taşır: n riski. |
| DS23 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Bant (+%5..+%10) cetvelin hedefinden, sonuçtan değil. |
| DS24 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Kaynak forex İDDİA; düşük öncelik. |
| DS25 | EVET (K: CGO WEB_SEKIL #23) | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | I | Tepeden çapalı kol DS konumunda nadir: dipten çapalı kol ANA. |
| DS26 | EVET | EVET | EVET (günlük uyarlama) | EVET | HAYIR | HAYIR | HAYIR | I | Kaynak gün içi profil; günlük profil bizim uyarlamamız. |
| DS27 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR* | I | Derinlik ve ATRP ile örtüşür. |
| DS28 | EVET (K: HIGH52) | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR* | I | DS (a) 120 bar ≥ %30; 252 bar derinliği ayrı bilgi taşır ama ATRP ile ilişkili. |
| DS29 | EVET | EVET | EVET | EVET | HAYIR* (şekil fazlası) | HAYIR | HAYIR | I (öncelik dışı) | Kutu boyu serbest derece, H15 basitlik ilkesi. |
| DS30 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | **EVET** | ELENDİ | DS olayı zaten 120 gün alt çeyreği: LOW52 olay içinde neredeyse sabit (mekanik). |
| DS31 | EVET (K: GEMINI #22) | EVET | EVET | EVET | HAYIR | HAYIR | **EVET** | ELENDİ | R18 ≥ 0,5 (fiyat düşüşün yarısını geri almış) ile F15 ≤ 0,25 birlikte neredeyse olanaksız: boş küme. |
| DS32 | HAYIR (SIZE_ME) | EVET | EVET† | EVET | HAYIR | HAYIR | **EVET** | ELENDİ | Eş kovası likidite üçlüsü boyutu zaten eşler; ancak kova kırılımı BİLGİ. |
| DS33 | EVET | EVET | — | HAYIR | HAYIR | HAYIR | HAYIR | ELENDİ | Kaynak README'de OB tespit kuralı yok: ölçülebilir tanım kurulamaz. |
| DS34 | HAYIR (K23, VD2) | EVET | EVET | EVET | HAYIR | HAYIR | **EVET** | ELENDİ | Sabit +%5 hedefte stop uzaklığına indirgenir: cetvel geometrisi h5 / st5'i mekanik belirler. |
| DS35 | HAYIR (GEMINI #21) | EVET | EVET | EVET | **EVET** | HAYIR | HAYIR | KAPALI | Birikim ayrışması (NVI / CMF / A-D, COL_KAZANC K8) kapalı listede. |
| DS36 | EVET | EVET | EVET | EVET | HAYIR | **EVET** | — | KOŞUL | Aynı gün bütün olaylara ortak; eşli fark sıfırlar. |
| DS37 | EVET | EVET | EVET† | EVET | HAYIR | **EVET** | — | KOŞUL | 2010 sonrası n 1 (K8). |
| DS38 | EVET | EVET | EVET† | EVET | HAYIR* (onay) | **EVET** | — | KOŞUL | Piyasa rejimi; eşik kaynaklar arasında çelişkili. |
| DS39 | HAYIR | EVET | EVET | EVET | **EVET** | EVET | — | KAPALI | VIX / DXY kapalı. |
| DS40 | HAYIR | EVET | EVET | EVET | **EVET** | HAYIR | — | KAPALI | Giriş onayı / hacim kapalı. |
| DS41 | HAYIR | EVET | EVET | — | **EVET** | HAYIR | — | KAPALI | Stop / erken kesme kapalı. |
| DS42 | HAYIR | EVET | EVET | EVET | **EVET** | HAYIR | — | KAPALI | Giriş zamanlaması / onay kapalı. |
| DS43 | EVET | EVET | EVET | **HAYIR** | HAYIR | HAYIR | — | bağlam dışı | 12 ay tepe şartı DS olayında oluşmaz. |
| DS44 | EVET | EVET (başvuru + 1) | EVET (k55 + k67; k67 /tmp kalıcı değil) | EVET | HAYIR | HAYIR | HAYIR | II | AVR olay verisi yok. |
| DS45 | EVET | EVET | EVET (k67) | EVET | HAYIR | HAYIR | HAYIR | II | Kaynak doğrulanamadı: düşük öncelik. |
| DS46 | EVET (INS_* var; DS koşulu yok) | EVET | EVET (k30) | EVET | HAYIR | HAYIR | HAYIR | II | Bağlam etkileşimi YENİ; F4 'çölde içeriden alım' TUTMADI* (eski cetvel). |
| DS47 | EVET | EVET | EVET† (5.02 CEO ayrımı yok) | EVET | HAYIR | HAYIR | HAYIR | II | Kesişim (5.02 × ilk 2.02 tepkisi) yok. |
| DS48 | EVET | EVET | EVET (form 144 bayrağı) | EVET | HAYIR | HAYIR | HAYIR | II | 2023 öncesi kâğıt başvuru kapsamı (K8 dönem yanlılığı). |
| DS49 | EVET | EVET | EVET (iki form adı) | EVET | HAYIR | HAYIR | HAYIR | II | ACT_13D yalnız 13D. |
| DS50 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | II | 1.01 ile birlikte gelenler ayrılır. |
| DS51 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | II | 889 kayıt: hücre n'i büyük olasılıkla < 30 (ÖLÇÜLEMEDİ riski). |
| DS52 | EVET | EVET | EVET | EVET | HAYIR | HAYIR | HAYIR | II | 7.695 kayıt. |
| DS53 | KISMEN (E_RSPLIT var; 3.03 YENİ) | EVET | EVET (3.03) | EVET | HAYIR | HAYIR | HAYIR | II | 3.03 ters bölünmeden geniş (zehir hapı vb.). |
| DS54 | EVET | EVET | **HAYIR** (başvuran kimliği yok) | EVET | HAYIR | HAYIR | HAYIR | ELENDİ | Aynı yatırımcı eşlenemez; kaynak da yok. |
| DS55 | EVET | EVET (filed + 1) | HAYIR (2016-22 finansal /tmp, kalıcı değil) | EVET | HAYIR | HAYIR | HAYIR | III | Eğitim dönemi için çerçeveler paketlenmeli. |
| DS56 | EVET | EVET | HAYIR (aynı) | EVET | HAYIR | HAYIR | HAYIR | III | CHS / O-skor katsayılı. |
| DS57 | EVET (F_SCORE İNDİR) | EVET | HAYIR (F_SCORE envanterde İNDİR) | EVET | HAYIR | HAYIR | HAYIR | III | Kollar EVET† yazdı, envanter İNDİR (ÇELİŞKİ 3). |
| DS58 | EVET | EVET | HAYIR (EDGAR FTS) | EVET | HAYIR | HAYIR | HAYIR | III | BIST kolu kap_ozet [DRIVE]; F12 EMARE ile bağlı. |
| DS59 | EVET | EVET | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | Büyük şirket ağırlıklı olay. |
| DS60 | EVET | EVET (Form 4 başvuru + 1) | HAYIR (DERIV_TRANS ham zip, işlenmemiş) | EVET | HAYIR | HAYIR | HAYIR | III | 2002 sonrası bildirim kuralı etkiyi bilgi gününden önceye çeker. |
| DS61 | EVET (GC_FLAG var; kalkma yok) | EVET | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | Kaynak kalkmada sürüklenme bulmuyor. |
| DS62 | EVET | EVET | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | Kaçınma adayı. |
| DS63 | EVET | EVET | HAYIR (FTS + SC TO-I) | EVET | HAYIR | HAYIR | HAYIR | III | n küçük (kaynak 126). |
| DS64 | EVET | EVET (ödeme + 12 gün) | HAYIR (/tmp/k66 kalıcı değil) | EVET | HAYIR | HAYIR | HAYIR | III | FINRA 2017-12+: eğitim 2018-22'ye kısalır. |
| DS65 | EVET | EVET (duyuru ≤ t) | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | H3 ailesinin genellemesi. |
| DS66 | EVET (E_101 genel) | EVET | HAYIR (defense.gov + ad eşleme) | EVET | HAYIR | HAYIR | HAYIR | III | K10 ad eşleme riski. |
| DS67 | EVET (E_DIV_INIT varyant) | EVET | HAYIR (temettü alanı /tmp/k60) | EVET | HAYIR | HAYIR | HAYIR | III | Kaynak doğrulanamadı. |
| DS68 | EVET | EVET | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | Kaynak yok (tek örnek LQDA). |
| DS69 | EVET (E_301 yalnız uyarı) | EVET | HAYIR (FTS) | EVET | HAYIR | HAYIR | HAYIR | III | Kaynak yok. |
| DS70 | EVET (yalnız ekleme var) | EVET | HAYIR (Wikipedia tablo) | EVET | HAYIR | HAYIR | HAYIR | III | Yılda ~20 olay: ÖLÇÜLEMEDİ riski. |
| DS71 | EVET | EVET | HAYIR (resmî liste / pay sayısı) | EVET | HAYIR | HAYIR | HAYIR | III | Takvim etkisine yakın. |
| DS72 | EVET | EVET | EVET† | **HAYIR** | HAYIR | HAYIR | — | ELENDİ | Yeni hissenin geçmiş fiyatı yok: DS olay tanımına girmez. |
| DS73 | EVET | HAYIR (45-60 gün gecikme) | HAYIR | **HAYIR** | HAYIR | HAYIR | — | ELENDİ | Çeyreklik portföy verisiyle 15 bar zamanlaması kurulamaz. |
| DS74 | KISMEN (REC_DOWN) | EVET | EVET† | **HAYIR** | HAYIR | HAYIR | — | ELENDİ | Etki 1-4 çeyrek. |
| DS75 | HAYIR | HAYIR | HAYIR | **HAYIR** | HAYIR | HAYIR | — | ELENDİ | Çeyreklik, 45 gün gecikme. |
| DS76 | HAYIR (H3 / K51) | EVET | HAYIR | EVET | HAYIR | HAYIR | — | MEVCUT | KAZANANLAR H1-H3 ön kaydında. |
| DS77-DS82 | HAYIR | EVET | EVET / İNDİR | EVET | HAYIR | HAYIR | — | MEVCUT | Envanter olaylarının DS-koşullu hali; DS koşusundan sonra BH dışı BİLGİ satırı olabilir. |
| DS83-DS87 | EVET / HAYIR | — | **HAYIR** (veri yok) | HAYIR | HAYIR | HAYIR | — | VERİ YOK | Ücretsiz tarihsel kaynak yok. |

## 3. HAVUZ

Ortak cetvel (her satır için, tekrar yazılmadı): DS olayı (DS_OLCUM_CERCEVE bölüm 1), giriş t+1 açılış, stop0 = hat (son 20 gün en düşük L) x 0,98, hedef +%5 / +%10, 15 geçerli bar; EŞ = aynı gün, aynı pazar, DS içinde özelliği tutmayan olay, kova = ATRP tercili x likidite üçlüsü; FARK = h5(özellik) − h5(eş); eğitim 2016-22, sınama 2023-26/08 (ambargo 60 bar). "Eğitim çeyreği" = pazar başına eğitim DS kümesinde hesaplanan çeyrek / onda / beşli sınırı; ön kayıtta sayı olarak yazılır, sınamaya aynen taşınır. Bütün pivotlar 6 sol / 6 sağ onaylı (kaynak: stock-pattern, WEB_GUNCEL; B19 aynı) ve yalnız onayı t'ye kadar tamamlananlar kullanılır. Evren endeksi = aynı pazar evreninin eşit ağırlıklı günlük getirisi (SPY / STOXX serisi yerine; K7: yaşayan evren).
Ortak K-riskleri (her satırda geçerli, satırda tekrar yazılmadı): K7 yaşayan evren (ABD batan fiyatı ~0, AVR yaşayan liste) → (+) yönlüler lehine, (−) yönlüler aleyhine yanlı; K5 kaynakların çoğu kapanış girişli, bizde t+1 açılış (etki küçülür); K8 her kolda n ≥ 30 ve güç; K4 hisse başına 15 barda 1 olay (ANA).

### 3.I — HEMEN ÖLÇÜLEBİLİR (OHLCV, ABD + AVR; DS ön kaydının ana listesi)

| DS | düz dil hipotez | ölçülebilir tanım (ANA kol önce; pencere, gecikme) | yön | SABİT eşik | kaynak(lar) ve kaynaktaki sayı | K1-K7 riskleri (satıra özgü) | Cemal'in kurallarıyla ilişki |
|---|---|---|---|---|---|---|---|
| DS01 | Son 10 günde sona doğru hızlanan düşüş (içbükey) kısa vadede iyi, U / kazan biçimli (dışbükey) yol kötü gider. | ANA: KONV10_t = (M − ort(C_{t−9..t})) / M, M = (C_{t−9} + C_t) / 2; alt beşte bir (içbükey) = 1. BİLGİ: üst beşte bir (−), 21 gün penceresi. | − (konvekslik); İKİ YÖNLÜ | Eğitim DS kümesinde KONV10 beşlik sınırları (kaynak: beşli, 10 gün) | Gulen-Woeppel JFQA (PDF doğrulandı): 10 gün / 10 gün alt-üst beşli %0,64 (t 7,31); aylık VW %0,84 (t 6,29); genel kesit, dipte ölçülmedi | K1: içbükeylik = son günlerde hızlanan düşüş (H2 ile örtüşür) → DS11 ile korelasyon raporlanır; K2 yok | ÇELİŞKİ: K3 / K22 / C9 (kazan yukarı), K50 / H2 (son günlerde dibe düşen kaybeder); DESTEK: CD22 (sert düşüş sonrası toparlanma 3 / 3 geldi) |
| DS02 | Kaybeden içinde devri düşük olan döner, devri yüksek olan düşmeye devam eder. | ANA: DEVIR_t = ort(V_{t−20..t}) / medyan(V_{t−251..t}) (pay sayısı yok, göreli devir vekili); alt onda = 1. BİLGİ: üst onda (−). | + (alt onda); AVR İKİ YÖNLÜ | Eğitim DS kümesinde DEVIR onda sınırları (kaynak: onluk) | Medhat-Schmeling RFS 2022 (özet doğrulandı; −%1,41 / t 7,13 doğrulanamadı); Lee-Swaminathan JF 2000 (özet: düşük hacimli kaybeden daha hızlı döner); UK / Avrupa'da ters (arama özeti, doğrulanamadı) | K1: düşük göreli hacim likidite kovasıyla kısmen eşlenmiş; K3 hacim 0 gün devirden çıkar; K6 AVR hacim birimi | DESTEK (zayıf): E5 'hacim kuruması' (eski cetvelde TUTMADI); kapalı listede öbek 'hacim kuruması' → ana model kararı |
| DS03 | Son ay düşüşünün sektörden bağımsız kısmı döner. | ANA: ART21_t = r21(hisse) − r21(sektör eşit ağırlık; sektor_ABD.csv, sektörde ≥ 5 hisse); AVR: r21 − r21(evren eşit ağırlık); alt onda = 1. | + | Eğitim DS kümesinde ART21 alt onda | Da-Liu-Schaumburg MS 2014 / NY Fed SR513 (doğrulandı): artık dönüşü riskten arındırılmış getiride standart dönüşün 3 katı (1982-2009) | K2: sektör sınıfı bugünkü (geriye uygulanır); sektor_ABD 1.416 hisse (V_ABD dışı hisseler sektörsüz → evren artığı kolu); K1: r21 düşüklüğü derinlikle ilişkili | YENİ; D2 (sektör rüzgârı EMARE) ile tamamlayıcı: rüzgâr varken geride kalan hisse |
| DS04 | Tek günlük büyük düşüşten sonra ilk haftalar sıçrama, sonrası düşüşün devamıdır. | ANA: son 120 geçerli barda r_s = C_s / C_{s−1} − 1 ≤ −0,15 ve t − s ∈ [2, 23] = 1. BİLGİ: aynı olay ve t − s > 23 (−); son 5 barda r < hissenin son 252 gün getirilerinin %2,5 yüzdeliği (+). | İKİ YÖNLÜ (faz +, sonrası −) | −%15; [2, 23] bar; %2,5 yüzdelik (hepsi kaynak) | Bulkowski dcb (doğrulandı): olay düşüşü ort. %31, sıçrama ort. %28 / 23 gün, sonra −%30 / 49 gün, %67'si olay dibinin altına; n yok. Guo ve ark. 2024 (İDDİA, Substack özeti): 5 günde +%1,81 (kapanış girişi). Cox-Peterson JF 1994 (künye): dönüş alış-satış farkından, uzun vadede kötü | K6: −%15 günü bölünme / birim hatası olabilir (bölünme marjı denetimi şart); K3 s barı geçerli; K1: ATRP yüksek hissede sık → kova şart | DESTEK: CD22; ÇELİŞKİ: K50 / H2; B9 (yol almış kovalama yok) ile ilişkisiz |
| DS05 | Düşüşte geniş aralıklı, çok hacimli, kapanışı dipten uzak doruk barı dibin yakın olduğunu gösterir. | ANA: s ∈ [t−59, t]: C_s < C_{s−1}, (H−L)_s / ATR20_{s−1} ≥ q, V_s ≥ 2 x SMA20(V)_{s−1}, CLV_s ≥ m = 1. BİLGİ: C15 altı etkenden ≥ 4; C16 doruk sonrası 5 bar içinde C > O ve C > (H_c + L_c) / 2; A11 C_t < min(C_{t−252..t−1}) ve V_t / ort50 ≥ eğitim üst çeyreği; A13 hacim × alış-satış farkı (iki yönlü). | + | V ≥ 2 x SMA20 (C15 kaynak); q = eğitim üst çeyreği (H−L)/ATR20; m = eğitim medyanı CLV; C16 W = 5 kaynakta yok (ön kayıtta sabit, sonuç görülmeden) | Wyckoff ChartSchool (kitap, doğrulandı; sayı yok); Huddart-Lang-Yetman MS 2009 (CXO ikincil): küçük çeyrekte 52h dip kırılımı sonrası 1 haftada ~%5 anormal; C15 / C16 TradingView İDDİA (sayı yok) | K1: hacim sıçraması oynaklıkla ilişkili (ATRP kova); K3 V > 0; K6 AVR hacim; kapalı 'hacim' sınırı | ÇELİŞKİ: K17 / E1 (alt fitili az = yukarı; doruk barı uzun alt fitilli); DESTEK: K26 dip savunması, CD18 ('en dip üstünde oluşum = satıcı bitti') |
| DS06 | Önceki dibin altına sarkıp kapanışta üstüne dönen hisse (sahte kırılım) döner. | ANA (Turtle Soup): L_t < min(L_{t−20..t−1}), o dibin yaşı ≥ 4 bar, C_t ≥ min(L_{t−20..t−1}), (H−L)_t ≤ 3 x ATR14. BİLGİ: C1 son onaylı dip P: L_t < P < C_t; C2 ≥ 2 onaylı dip birbirine %1 içinde, L_t < min, C_t > min; B26 Oops O_t < L_{t−1} < C_t. | + | 20 gün, 4 bar, 3 x ATR14 (therighttrader); %1 (smc range_percent); pivot 6/6 | Connors-Raschke 1996 (kitap; "yayımlanmış güvenilir kazanma oranı yok"); smc README 2.252 yıldız, LuxAlgo (İDDİA, sayı yok); Williams Oops (İDDİA, sayı yok) | K2 pivot onayı; K6 Oops kolu açılışa dayanır (V_AVR'de 13.622 satır açılış H-L dışında); K1 orta (dipte yeni 20 gün dibi sık) | DESTEK: K5 (kapanışla kırılmadıysa hüküm sürer), K26 / C2 dip savunması, B8 savunma hattı; hafif ÇELİŞKİ: K17 (süpürme barı uzun alt fitilli) |
| DS07 | Önceki günün dibinin altında kapanan 8 gün dibi barından sonra tepesi aşılırsa dönüş gelir. | ANA: C_{t−1} < L_{t−2} ve L_{t−1} < min(L_{t−9..t−2}) ve H_t > H_{t−1}. | + | 8 gün (Williams, kaynak) | Larry Williams (kitap); Rogue Quant (İDDİA): yalnız vadeli / endeks, S&P alım kazanma %80 küçük örneklem | K5 tetik t'de tamamlanmış; onay ailesi notu | DESTEK: B7 / K12 'dönüm mumu' |
| DS08 | 30 haftalık ortalama düşerken ve fiyat altındayken (evre 4) düşüş sürer; ortalama düzleşmişse (evre 1) toparlanır. | ANA: EGIM_t = SMA150_t / SMA150_{t−20} − 1; EVRE4 = EGIM < 0 ve C_t < SMA150_t = 1 (−). BİLGİ: EVRE1 = \|EGIM\| ve \|C/SMA150 − 1\| ikisi de eğitim alt çeyreğinde (+); EMA22_t < EMA22_{t−1} (−). | − (EVRE4) / + (EVRE1) | EVRE4 kaynak tanımı (işaret); EVRE1 eğitim alt çeyrekleri | Weinstein; Bulkowski Stages (doğrulandı): evre 1 alım ort. +%13,2 / kârlı %69,3 (n 127); evre 4 alım −%8,3 / %24,4 (n 127); süresiz, stop'suz, seçilmiş işlemler | K8: DS olaylarının büyük çoğunluğu EVRE4 → eş azlığı / güç; ≥ 150 bar geçmiş ister (genç hisse dışarı, yazılır) | DESTEK: K19 / A10 / C6 (alçalan büyük resimde küçük taban girilmez); ÇELİŞKİ: VD10 (dip havuzunda 'büyük resim yükselen' şartı tanımca çelişir) |
| DS09 | 2 günlük RSI aşırı satımdaysa kısa vadeli sıçrama gelir. | ANA: RSI2_t ≤ 5 (Wilder, 2 gün). BİLGİ: RSI2_t + RSI2_{t−1} < 35. | İKİ YÖNLÜ | 5 (Connors / ChartSchool); 35 (doğrulanamadı, BİLGİ) | ChartSchool RSI(2) (doğrulandı; sayı yok); Connors SMA200 ALTINDA açığa satış arar | K1 düşük; RSI ailesi E14 (60 gün, TUTMADI*) | ÇELİŞKİ: K50 / H2; DESTEK: CD22 |
| DS10 | Trendden arındırılmış 2 günlük fiyatın kendi geçmişine göre sırası dipteyse sıçrama gelir. | ANA: DV2_t = yüzdelik sıra( SMA2( C / ((H+L)/2) − 1 ), son 252 bar ) < 10. | + ; İKİ YÖNLÜ (kaynak yalnız SMA200 üstü) | < 10 (kaynak); pencere 252 (kaynak görselde, doğrulanamadı; ön kayıtta sabit) | Quantitativo (İDDİA blog): Russell 3000 batanlar dahil, DV2 < 10 ve C > SMA200, 5 gün ort. +%2,0, pozitif %54 (olay dışı %52), p 0,017 | K1 düşük; DS09 ile korelasyon raporlanır | DS09 ile aynı |
| DS11 | Kapanışı 7 günün en düşüğünde olan dipteki hisse ya sıçrar (Connors) ya bıçak sürer (H2). | ANA: C_t ≤ min(C_{t−6..t}). BİLGİ: H2 kolu F15_t ≤ 0,05 ve r5 ≤ −%3 (KAZANANLAR tanımı; H2 ön kaydıyla tek satır). | İKİ YÖNLÜ | 7 gün (Connors); H2 eşikleri KAZANANLAR'dan | StrategyQuant (İDDİA): SPY 1993-2026, 333 işlem, kâr faktörü 2,35 (hisse testi yok); H2: h5 %64 / st5 %32 vs %71 / %18 (sonradan bakma, bilgi) | K1: dipte sık; DS01 / DS09 ile korelasyon | K50 / H2 (aynı ölçü ailesi), C2, TUR 4 s7 DESTEK (−); CD22 ÇELİŞKİ |
| DS12 | Elder Impulse 'kırmızı'dan çıkınca düşüş ivmesi biter. | ANA: KIRMIZI_i = EMA13_i < EMA13_{i−1} ve HIST_i < HIST_{i−1} (MACD 12,26,9); KIRMIZI_{t−1} ve değil KIRMIZI_t = 1. BİLGİ: son 10 barda kırmızı gün sayısı. | + | EMA13, MACD(12,26,9) (Elder, kaynak); ikili | ChartSchool Elder Impulse (doğrulandı; sayı yok) | K1 düşük | DESTEK (akraba): K47 MACD pozitif uyumsuzluğu |
| DS13 | Art arda 9 kapanış 4 gün öncekinden düşükse satış tükenmiştir. | ANA: C_i < C_{i−4} art arda 9 bar, 9. bar = t (kesişim / mükemmellik şartı YOK). BİLGİ: setup sonrası ≥ 12 bar, C_i ≤ L_{i−2} olan 13. bar t'de. | + | 9 / 13 sayım (DeMark, kaynak) | MarketInOut (doğrulandı; sayı yok) | K8 countdown n küçük; tanım çelişkisi (kesişim) ön kayıtta 'yok' diye sabit | YENİ |
| DS14 | Alçalan tepeler dizisinde son onaylı tepenin kapanışla aşılması düşüşün bittiğini gösterir. | ANA: son iki onaylı 6/6 tepe LH1 > LH2 ve C_{t−1} ≤ LH2 < C_t. BİLGİ: TDST (C_t > son tamamlanan buy setup'ın 9 barının en yükseği); trend çizgisi (son iki onaylı tepe doğrusu, C_t > doğru_t); smc k = 50 kolu. | + | işaret / ilk kapanış; pivot 6/6 | smc README (İDDİA); DeMark TDST (kısmen doğrulandı); Wyckoff alım testi 4 (ChartSchool doğrulandı); hiçbirinde sayı yok | K2 pivot onayı; onay ailesi (durum özelliği olarak sınanır); DS konumunda n riski | DESTEK: B1 (tavanı kapanışla kıran al mumu), K21 / C5 gövdeli kırılım; K29 (tavan = ilk dip yapısının tavanı) referans sorusu |
| DS15 | Aşağı kırılıp %10'dan az düşen, sonra tabanın tepesini kapanışla aşan desen güçlü yükselir. | ANA: taban [L_b, H_b] = t'de tamamlanmış son S6 / YAPI_HEDEF bölgesi; s'de C_s < L_b; min(L)_{s..t} ≥ 0,90 x L_b; C_t > H_b ilk kez. | + ; İKİ YÖNLÜ | %10 (Bulkowski, kaynak) | Bulkowski Busted (doğrulandı): busted / busted olmayan ort. yükseliş alçalan üçgen %54 / %38, simetrik üçgen %52 / %34; n yok, boğa | K2 bölge t'de tamamlanmış olmalı (S6 kodu içe alınır, kopyalanmaz); K8 n küçük | ÇELİŞKİ: K5 (taban kapanışla kırıldıysa hükmü yok), C1 (taban kırılınca çık) |
| DS16 | Doruk dibine daha düşük hacim ve dar aralıkla dönüp üstünde duran ikinci test dibi güvenilir yapar. | ANA: DS05 doruk barı s sonrası u ∈ [s+5, t]: \|L_u / L_s − 1\| ≤ e, V_u / V_s < q1, (H−L)_u / (H−L)_s < q2, L_u ≥ L_s x (1 − e). | + | e, q1, q2 = eğitim medyanları (kaynakta sayı yok) | Wyckoff ChartSchool (doğrulandı; nitel) | DS05'e bağımlı (korelasyon raporlanır); hacim sınırı; serbest derece | DESTEK: K26 dip savunması, CD18, LMW DBOT (WEB_SEKIL #12) |
| DS17 | Piyasa düşerken daha az düşen hisse toparlanmada öndedir. | ANA: DIRENC_t = ort(r_i − r_m,i \| r_m,i < 0), i ∈ [t−39, t]; r_m = evren eşit ağırlık; eğitim üst çeyreği = 1. BİLGİ: yukarı günlerde aynı fark. | + | Eğitim üst çeyreği (kaynakta sayı yok) | Wyckoff alım testi 7 (ChartSchool doğrulandı; nitel) | K1: düşük beta ile örtüşür (ATRP kova kısmen); K7 evren endeksi yaşayan | YENİ; B13 (yükselişte alınca zarar az, TUTTU) ile akraba |
| DS18 | Endekse göre göreli gücü yükselen dipteki hisse daha iyi toparlanır. | ANA: RS = C / E (evren endeksi); SMA22(RS)_{t−1} > SMA22(RS)_{t−2}. BİLGİ: son 60 barda hissenin son iki onaylı dibi P2 > P1 ve endeksin E2 < E1. | + ; İKİ YÖNLÜ (C19 ters) | 0 (işaret; Bulkowski) | Bulkowski RS (doğrulandı): kırılım ÖNCESİ RS eğimine göre fark küçük (%18-21), yazar 'sezgiye aykırı'; C18 kaynağı doğrulanamadı | K2: kırılım sonrası RS kullanılmaz; K7 | DESTEK: B13; ÇELİŞKİ: C19 (stres gününde zayıfı al) |
| DS19 | Alt banda inen ilk dipten sonra daha derin ama bant içinde kalan ikinci dip dönüş işaretidir. | ANA: %b = (C − Alt) / (Üst − Alt), BB(20,2); onaylı dip d1 %b ≤ 0; onaylı dip d2 (d1'den sonra, ara ∈ [Q1, Q3]) L_d2 ≤ L_d1 x (1 + tol), %b_d2 > 0; t ≥ d2 + 6. | + | BB(20,2) kaynak; ara [Q1, Q3] ve tol = eğitim DS kümesinde ardışık onaylı dipler arası bar sayısı çeyrekleri ve \|L_d2/L_d1 − 1\| medyanı | bollingerbands.com kuralları (doğrulandı; W dip adıyla, sayı yok) | K2 pivot; serbest derece | DESTEK: K47 MACD pozitif uyumsuzluğu (aynı aile); E14 uyumsuzluk 60 günle TUTMADI* |
| DS20 | Kapanışların alt bandın altında kalması düşüşün devamıdır. | ANA: YURU_t = Σ 1[C_i < Alt_i], i ∈ [t−9, t], BB(20,2); YURU ≥ eğitim üst çeyreği = 1. | − | Eğitim üst çeyreği | Bollinger kural 7-8 (doğrulandı; sayı yok) | K1: derinlik / hız ile ilişkili; K7 (−) aleyhine | DESTEK: K19 / C6 (alçalan resim); ÇELİŞKİ: DS05 (bant dışı doruk = dip) |
| DS21 | Düşüşün çoğu gece (haber) olmuşsa dönmez; gün içi düşüş döner. | ANA: GECE_PAY_t = Σ ln(O_i / C_{i−1}) / Σ ln(C_i / C_{i−1}), i ∈ [t−19, t], payda < 0 iken; eğitim üst çeyreği = 1. | − | Eğitim üst çeyreği (kaynakta sayı yok) | Miwa (QuantPedia ikincil özeti, doğrulandı): gün içi getiriler döner, gece getirileri dönmez; Lou-Polk-Skouras (GAP_OVN, envanter) | K6: V_AVR açılış H-L dışı 13.622 satır → AVR'de ön temizlik şart; K3 hacim 0 gün | YENİ; DS44 (habersiz düşüş) fiyat vekili |
| DS22 | Düşüşteki büyük aşağı boşluğun kapanışla doldurulması toparlanmayı teyit eder. | ANA: son 60 barda boşluk günü i: r_i ≤ −2 x σ20_{i−1}; C_t ≥ C_{i−1} ilk kez = 1. BİLGİ: son 60 barda dolmamış aşağı FVG (H_i < L_{i−2}, fark ≥ 0,3 x ATR14) üst kenarı L_{i−2} üstünde ilk kapanış. | + | 2σ (tastylive); 0,3 ATR14 (Sucupira) | tastylive (doğrulandı): 20 likit S&P hissesi 5 yıl, ±2 SD boşlukların ~%5'i 1 günde, 'yarıdan fazlası' 45 günde dolar; edgeful iFVG (İDDİA, vadeli 15 dk) | K8: dolum DS konumuyla (alt çeyrek) gerilimli → n riski | DESTEK (akraba): B1 kırılım |
| DS23 | Fiyatın +%5..+%10 üstünde dolmamış boşluk ya da eşit tepeler varsa fiyat oraya çekilir. | ANA: son 120 barda dolmamış 2σ aşağı boşluk i, C_{i−1} / C_t − 1 ∈ (0,05; 0,10]. BİLGİ: ≥ 2 onaylı tepe, \|a − c\| / c ≤ %1, seviye C_t'nin +%5..+%10 üstünde, süpürülmemiş. | + | 2σ (tastylive); %1 (smc); bant cetvel hedefinden | tastylive (doğrulandı); Sucupira (İDDİA); smc / LuxAlgo (İDDİA) | Bant cetvelden (sonuçtan değil); K2 pivot | ÇELİŞKİ: K2 (düz tavan = aşağı formasyon) BİLGİ kolu için |
| DS25 | Dipten çapalı AVWAP'ın üstünde kalıp onu test eden fiyat, dipten alanların kârda olduğunu gösterir. | ANA: AVWAP_low = son 120 barın en düşük L barından t'ye Σ TP·V / Σ V; C_t > AVWAP_low ve min(L_{t−2..t}) ≤ AVWAP_low x (1 + e). BİLGİ: DS tepe barından (son 120 bar max C) çapalı AVWAP için C_{t−1} ≤ AVWAP_peak < C_t. | + | e = eğitim medyanı (kaynakta yok; C tablosundaki 1,01 kaynak değil) | MMT bülteni (İDDİA, tek işlem); takeprofitapp (İDDİA, '~%64', örneklem yok) | K8 tepe kolu DS konumunda nadir; K3 hacim 0 | YENİ; CGO (WEB_SEKIL #23) akraba |
| DS28 | Tepeden çok derin düşmüş hissenin toparlanma olasılığı farklıdır (ortalama + ama tipik −). | ANA: DERIN_t = C_t / max(C, son 252 bar) − 1 ≤ −0,60. BİLGİ: ≤ −0,50. | İKİ YÖNLÜ | −%60 (Brandes, A1); −%50 (C22) | Brandes (İDDİA ikincil): ABD 1.904 olay, 3 yıl ort. +%6,6 üstün ama MEDYAN −%7,7, batma %8,7; Mauboussin (ikincil): 6.500 hisse, %54'ü tepesine dönmedi | K1: derinlik ATRP ile ilişkili (kova); K7 batan yok → toparlanma lehine | DESTEK: CD22 (sert düşüş eleme nedeni değil); I3 ('oynak hisse seçilince yükselme', ÖLÇÜLEMEDİ) |
| DS24 | Dipte oluşan 3 barlık yukarı boşluk (FVG) alıcı geldiğini gösterir. | L_t > H_{t−2} ve (L_t − H_{t−2}) ≥ 0,3 x ATR14 (son 5 barda; yaş eşiği eğitim medyanı). | + | 0,3 ATR14 (Sucupira) | Sucupira (İDDİA, EURUSD 18 işlem; OHLC'de PF 4,28, tik verisinde 1,04) | Kaynak forex, bar içi sıra yanlılığı | YENİ |
| DS26 | Son 60 barın hacim profili POC'unun altına inip üstünde kapanmak dönüş işaretidir. | POC = 60 bar, 50 kova (bar hacmi tipik fiyata); L_t < POC < C_t. | + | 60 / 50 kaynakta yok → ön kayıtta sabit (sonuç görülmeden) | LuxAlgo (İDDİA; gün içi profil, sayı yok) | Günlük uyarlama kaynak dışı | YENİ |
| DS27 | 50 gün ortalamanın ATR katıyla çok altında gerilmiş hisse ya geri döner ya bıçak sürer. | ATRX_t = ((C_t − SMA50_t) / SMA50_t) / (ATR14_t / C_t) ≤ eğitim alt çeyreği. | İKİ YÖNLÜ | Eğitim alt çeyreği (kaynak yalnız üst eşik verir) | Finkle87 TradingView (İDDİA) | K1: derinlik / ATRP ile örtüşür | YENİ |
| DS29 | P&F aşağı hedefi tamamlandıysa ya da alt direk dönüşü oluştuysa düşüş bitmeye yakın. | P&F 3 kutu dönüş, kutu = ATR tabanlı yüzde; dikey sayım hedefi ≤ L_t / alt direk. | + | kutu boyu kaynakta hisseye göre sabit puan → serbest derece | Wyckoff alım testi 1 (doğrulandı); P&F catapult (doğrulandı); low pole (doğrulanamadı) | H15: karmaşık, basit ölçüyü geçmezse seçilmez | YENİ |

### 3.II — ABD-OLAY (sec_ozet / Form 4 / Yahoo; AVR karşılığı yok → karar en fazla ABD-ADAY)
Ortak: olay bilgi günü = başvuru günü + 1 işlem günü ≤ t; 8-K madde bayrakları yalnız 2004-08+; sec_ozet kapsamı 3.262 CIK (k60'ın ~%55'i): kapsam dışı hisse "olay yok" sayılmaz, evrenden çıkarılır (K7); eş = kapsam içi DS olayları.

| DS | düz dil hipotez | ölçülebilir tanım | yön | SABİT eşik | kaynak(lar) ve sayı | K1-K7 riskleri | Cemal ilişkisi |
|---|---|---|---|---|---|---|---|
| DS44 | Büyük düşüş günü habersizse döner, haberliyse sürer. | ANA: s ∈ [t−19, t] için r_s − r_m,s ≤ −0,10; HABER_s = [s−1, s+1]'de Yahoo not değişimi (k67) ya da 8-K başvurusu ya da bilanço günü; HABERSIZ = 1. BİLGİ: C19 kolu (endeks r ≤ −%2 günü evrende alt %10, 8-K yok). | habersiz + / haberli − | −%10 (Savor, kaynak); 5-40 gün kaynak tutma ufku | Savor JFE (CFA özeti doğrulandı): ≥ 5 analistli hisseler 1995-2009, iki yönlü strateji yıllık %35 anormal; Chan 2003 (künye); Nauss (İDDİA) | K2 not / 8-K tarihleri; k67 /tmp kalıcı değil; Savor ≥ 5 analist (bizde azı) | DESTEK: K49 / H1 (bilanço penceresi kuyruk büyüteci) |
| DS45 | Dışbükey yoldan sonra gelen not düşürmesi daha kötü getirir. | KONV10 üst beşte bir ve son 20 günde ≥ 1 not düşürme. | − | DS01 beşli; ≥ 1 | Jacob-Shamsi-Vasudevan (doğrulanamadı) | kaynak doğrulanamadı | DS01 ile aynı ilişki |
| DS46 | Düşüşteki içeriden alım bilgiden çok 'ucuzladı' inancıdır; yine de büyük düşüş sonrası alım güçlü olabilir. | ANA: [t−29, t] içinde ≥ 1 Form 4 P (k30, başvuru + 1). BİLGİ: INS_CLUSTER (≥ 3 alıcı / 30 gün); alım günü C / HIGH52 onluğu (A20); alım + ilk SUE (D3). | İKİ YÖNLÜ | ≥ 1 alım; ≥ 3 alıcı (envanter K31); onluk (Li ve ark.) | Li-Wang-Yan-Zhang 2019 (ikincil doğrulandı): tepeye yakın alım 30 günde ≥ 3,3 puan iyi; 'gülümseme' tezi (doğrulanamadı); Piotroski-Roulstone 2005 (PDF doğrulandı; yön sayısı yok) | K2 Form 4 başvuru günü | ÇELİŞKİ / ZAYIF: F4 (çölde içeriden alım, TUTMADI*); B10 (kim alıyor) |
| DS47 | Zorunlu CEO değişiminden sonra ilk bilanço kötü gelirse fiyat sonra toparlanır. | 8-K 5.02 [t−180, t] takvim günü ve sonraki ilk 2.02 bilanço tepkisi (−1..+1, piyasaya göre) < 0; t = tepkiden sonraki ilk gün. | + | 180 gün (D önerisi; kaynak 'ilk bilgi olayı') ; tepki < 0 | Hu ve ark. 2025 RoF (özet doğrulandı; sayı yok) | 5.02 CEO / zorunlu ayrımı yok (EVET†) | DESTEK: D8 ('önce korkutup aldırmıyorlar') akraba |
| DS48 | Form 144 satış niyeti bildirimi kısa vadede olumsuzdur. | Form 144 başvurusu [t−20, t−1] = 1. | − | bayrak; 20 gün (kaynak 1 ay) | Voelcker CLS (yazar özeti, doğrulandı): >100 bin bildirim 2008-2019, tutan − tamamlayan ertesi ay +0,33 puan | K8: 2023 öncesi kâğıt başvuru kapsamı → eğitim / sınama kapsam farkı (dönem yön karşılaştırması bozulabilir) | YENİ; F5 (içeriden satış, TUTMADI*) akraba |
| DS49 | Düşüşten sonra yeni pasif %5 ortak gelmesi toparlanmayı önceler. | Değişikliksiz 'SC 13G' ya da 'SCHEDULE 13G' [t−60, t] ≥ 1. | + | ≥ 1; 60 gün (ACT_13D penceresi) | kaynak doğrulanamadı | Form adı 2024'te değişti: iki ad birlikte süzülmeli (K10) | YENİ |
| DS50 | Düşüşten sonra yeni borç / kredi anlaşması iflas korkusunu azaltır. | 8-K 2.03 [t−20, t] ≥ 1. | İKİ YÖNLÜ | ≥ 1; 20 gün (E_101 penceresi) | kaynak yok | 1.01 ile birlikte gelenler ayrı kol | YENİ |
| DS51 | Borcu hızlandıran tetikleyici bildiren hisse düşmeye devam eder. | 8-K 2.04 [t−60, t] ≥ 1. | − | ≥ 1; 60 gün | kaynak yok | n küçük (889 kayıt) → ÖLÇÜLEMEDİ olası | YENİ |
| DS52 | Önemli sözleşmesi feshedilen hisse düşmeye devam eder. | 8-K 1.02 [t−20, t] ≥ 1. | − | ≥ 1; 20 gün | kaynak yok | — | F1 'isimli sözleşme' tersi |
| DS53 | Ortak haklarında önemli değişiklik (ters bölünme dahil) kötü işarettir. | ANA: 8-K 3.03 [t−60, t] ≥ 1. BİLGİ: 5.03 / ters bölünme (E_RSPLIT). | − | ≥ 1; 60 gün | Kim-Klein-Rosenfeld 2008 (doğrulandı): 3 yılda anlamlı negatif | (a) KISMEN: E_RSPLIT var | G (boyut) ile ilgili; YENİ değil, bağlam varyantı |

### 3.III — İNDİR GEREKİR
| DS | düz dil hipotez | ölçülebilir tanım | yön | SABİT eşik | kaynak ve sayı | indirilecek kaynak / tahmini iş | Cemal ilişkisi |
|---|---|---|---|---|---|---|---|
| DS55 | Çok düşen hisseler içinde ucuz (EV/Satış) olan daha iyi toparlanır. | C_t / C_{t−252} − 1 < −0,60; piyasa değeri ≥ 100 mn $; EV/Satış alt çeyrek (son 10-Q, filed + 1). | + | −%60, 100 mn $ (Brandes); alt çeyrek | Brandes (İDDİA ikincil): EV/Satış alt çeyrek +%11,6 ABD (3 yıl) | k60_secframes (/tmp, 28 kavram 2009-26) islenmis-veri'ye paketlenir + borç / nakit kavramları; orta iş (1-2 gün) | F1 sıkı dosya akraba; I1 hedefi (+%100) bilgi |
| DS56 | Sıkıntılı ve sert düşmüş hissede dönüş ilk ayda gelir; kaybeden bacağı sıkıntıda sürer. | CHS / O-skor üst onda × r21 alt onda × devir(21) / devir(önceki 63) > 1. | İKİ YÖNLÜ | onda (kaynak); > 1 | Da-Gao 2010 JFQA (doğrulandı): etki yalnız ilk ayda; Avramov-Chordia (doğrulanamadı) | Aynı çerçeveler + katsayılar; orta | F6 (nakit tükenmesi, TUTMADI; batanlarla eridi) |
| DS57 | Kaybedenlerden temeli güçlü olan (F ≥ 7) döner. | DS olayı × F_SCORE ≥ 7 vs ≤ 3; fiyat ≥ 5 $. | + ; İKİ YÖNLÜ (C24) | 7 / 3, 5 $ (kaynak) | Zhu-Sun-Chen 2019 (QuantPedia doğrulandı): büyük hisse %0,95 / ay, maliyet sonrası %0,66, örneklem dışı 'hafif negatif'; peas0c (İDDİA): kalite süzgeci getiriyi düşürdü, anlamsız | F_SCORE kavramları (OCF, cari kalemler, LTD, brüt kâr, pay) 2015+ çerçeveler; orta | F1 / F9 dosya kapısı DESTEK |
| DS58 | Düşüşten sonra geri alım programı duyuran hisse toparlanır. | [t−20, t] 8-K 8.01 / 7.01 metninde 'repurchase program / authorization'; BIST kolu KAP 'pay geri alım' konu kodu. | + | ilk duyuru; 20 gün | Peyer-Vermaelen 2009 RFS (özet doğrulandı; sayı yok) | EDGAR tam metin arama 2001+ (SEC User-Agent e-postası → Cemal izni); BIST kap_ozet [DRIVE]; büyük iş | DESTEK: F12 (KAP geri alım bildirimi tek EMARE, Ç170) |
| DS59 | ASR duyurusu sonrası hisse zayıf kalır. | [t−20, t] 'accelerated share repurchase'. | − | 20 gün | Michel-Oded-Shaked 2010 (doğrulandı): 9 ayda ~−%8,6 | EDGAR FTS; büyük | DS58 ile tür ayrımı |
| DS60 | Yöneticiye plan dışı opsiyon tahsisi dipte yapılır, sonra fiyat yükselir. | Form 4 türev tablosu kod A, opsiyon, [t−10, t]; plan dışı = önceki yıl aynı hafta tahsis yok. | + | 10 gün; plan dışı tanımı (kaynak) | Lie 2005 MS (PDF doğrulandı): 1.668 tahsis, önceki 30 gün −%3, sonraki 10 gün +%2 (1992-2002) | Drive sec/ ham zipler DERIV_TRANS işlenir; orta | YENİ |
| DS61 | Going concern kalkınca hisse toparlanır. | Önceki 10-K'da 'substantial doubt' var, son 10-K'da yok. | ? | geçiş | Kausar-Taffler-Tan 2009 (doğrulandı): verilişte 1 yıl −%14, kalkışı piyasa tam fiyatlıyor | EDGAR FTS; büyük; düşük beklenti | F9 going-concern kapısı |
| DS62 | 'Stratejik seçenekler' duyurusundan sonra fiyat geri verir. | [t−20, t] 'strategic alternatives'. | − | 20 gün | Giedt-Rim (yazar özeti doğrulandı): duyuruda > +%5, 6 ayda ~−%9 | EDGAR FTS; büyük | YENİ |
| DS63 | Borç takas teklifi duyurusu kötü; başarılı tamamlanma iflas riskini düşürür. | [t−60, t] borç-hisse takas teklifi; tamamlanma ayrı bayrak. | − / + | 60 gün | Lie-Lie-McConnell 2001 (PDF doğrulandı): 126 duyuru, 3 yılda Chapter 11 %25 (eş %6) | EDGAR FTS + SC TO-I; büyük; n küçük | YENİ |
| DS64 | Açık pozisyon eğilimi aşağıysa ve açığa satış kârla kapatılıyorsa hisse iyi gider. | ANA: SI / pay son 12 iki-haftalık eğim < 0 (ödeme + 12 gün). BİLGİ: SI son iki dönemde ≥ eğitim üst çeyreği düşüş ve C_t < SI tepe dönemi ort. kapanış (+) / > (−). | + / İKİ YÖNLÜ | işaret; eğitim üst çeyreği (D'nin '%20 ya da çeyrek' çift seçeneği yerine) | SMU / Papadimitriou-Rapanos (doğrulanamadı) | FINRA CDN ücretsiz ~10 dk (2017-12+); kalıcı paket; küçük iş | YENİ |
| DS65 | Önceden duyurulmuş yatırımcı günü yaklaşırken fiyat koşar. | Duyurusu ≤ t olan yatırımcı günü t+1..t+15 arasında. | + | t+1..t+15 (cetvel ufku) | Cabrera-Kolokolova-Zhang 2025 (PDF doğrulandı): ~1.000 olay, olay öncesine BHAR +%3,70 | EDGAR FTS ('investor day', 7.01 / 8.01) duyuru / olay ayrımı; büyük | DESTEK: K51 / H3 (önceden bilinen katalizör) |
| DS66 | Düşüşten sonra büyük hükûmet sözleşmesi alan hisse toparlanır. | DoD duyurusu, tutar / piyasa değeri ≥ eğitim üst çeyreği. | + | eğitim üst çeyreği | kaynak doğrulanamadı | defense.gov + USAspending, ad eşleme (K10); büyük | F1 isimli sözleşme |
| DS67 | Temettüyü kesip yeniden başlatan şirket toparlanır. | Son 12 ayda kesilmiş ve yeniden ödenmiş temettü. | ? | geçiş | ap Gwilym-Seaton (doğrulanamadı; özet: 3 yılda fazla getiri yok) | k60_fiyat JSON temettü alanı (/tmp) paketlenir; küçük | YENİ |
| DS68 | Dava uzlaşması düşüşteki hissede katalizördür. | [t−20, t] 8.01 metninde 'settlement' + dava. | + | 20 gün | kaynak yok (tek örnek LQDA) | EDGAR FTS / Stanford SCAC; büyük | K51 / H3 ailesi |
| DS69 | 1 $ kot uyarısı sonrası uyum yeniden kazanılınca toparlanır. | 3.01 [t−180, t] ve [t−20, t] 'regained compliance'. | ? | 180 / 20 gün | kaynak yok | EDGAR FTS; orta | YENİ |
| DS70 | S&P 500'den çıkarılan hissenin düşüşü geçicidir (ya da kalıcı). | Çıkarma yürürlük günü [t−20, t]. | İKİ YÖNLÜ | 20 gün | Kumar ve ark. 2023 (doğrulandı: kalıcı); Chen-Noronha-Singal 2004 (doğrulanamadı: geçici) | Wikipedia değişiklik tablosu; küçük; yılda ~20 olay | YENİ |
| DS71 | R1000'den R2000'e düşen hisse yeniden yapılanma öncesi alım baskısı görür. | Mayıs sonu piyasa değeri sırası > 1000; giriş yeniden yapılanmadan 20 gün önce. | + (önce) / − (sonra) | −20 / +20 gün (Dimensional) | Dimensional (doğrulandı): öncesi +%1,2, sonrası −%0,95 (etiket ters görünüyor) | FTSE Russell listeleri / pay sayısı; orta | YENİ |

### 3.K — KOŞUL (hipotez değil; aynı gün eşli farkla sıfırlanır)
DS36 (piyasa 24 ay < 0), DS37 (Zweig, n 1), DS38 (FTD, eşik %1 / %1,25 / %1,7 çelişkili). Ölçülecekse yalnız 'DS dışı eş' ya da gün hücresi bazında BİLGİ; BH listesine girmez. DS38 'giriş onayı' kapalı konusuna yakın.

## 4. YÖN ÇELİŞKİLERİ (ön kayıtta 'İKİ YÖNLÜ TEST' işareti)

| # | ölçü (DS) | bir yön | öteki yön | kaynak | ön kayıt |
|---|---|---|---|---|---|
| 1 | Konvekslik (DS01) | dışbükey (U / kazan) − | Cemal kazan + (K3, K22, C9) | Gulen-Woeppel ↔ Cemal | İKİ YÖNLÜ |
| 2 | Son günlerde hızlanan düşüş (DS01, DS11) | içbükey / 7 gün dibi + | H2 / K50 düşen bıçak − | Gulen-Woeppel, Connors ↔ KAZANANLAR | İKİ YÖNLÜ |
| 3 | Aşırı satım (DS09, DS10, DS11) | kısa vadeli sıçrama + | Connors SMA200 altında açığa satış arar | Connors / Quantitativo (yalnız SMA200 üstü) | İKİ YÖNLÜ |
| 4 | Büyük tek gün düşüş (DS04) | 5 günde kaybın ~beşte biri geri + | dönüş yalnız spread, uzun vadede − | Guo ve ark. ↔ Cox-Peterson | İKİ YÖNLÜ |
| 5 | Dead-cat fazı (DS04) | ilk 23 gün sıçrama + | sonra 49 günde −%30 − | Bulkowski (aynı kaynak, ufka göre) | ANA kol faz +, BİLGİ − |
| 6 | 52h dibi (DS30, DS05-A11) | dibe yakın / kırılım sonrası + | dibe yakın − (George-Hwang, Brock) | Chen-Yu, Huddart ↔ (doğrulanamadı) | DS30 elendi; A11 kolu iki yönlü |
| 7 | Kaybeden × hacim (DS02) | ABD düşük hacim + | UK yüksek hacim üstün, Avrupa yok | Lee-Swaminathan ↔ tekrarlar (doğrulanamadı) | AVR İKİ YÖNLÜ |
| 8 | Hacim yönü (DS02 ↔ DS05) | yüksek devirli kaybeden − | yüksek hacimli doruk + | Medhat-Schmeling ↔ Wyckoff | iki ayrı DS, korelasyon raporlanır |
| 9 | Bilgi asimetrisi × hacim (DS05-A13) | bilgili işlemde sürer | bilgisizde döner | Llorente ve ark. | İKİ YÖNLÜ |
| 10 | Doruk barı kapanışı (DS05, DS06) | dipten uzak kapanış (uzun alt fitil) + | alt fitili az mum yukarı (K17, E1) | Wyckoff ↔ Cemal | İKİ YÖNLÜ |
| 11 | Bant dışı kapanış (DS05 ↔ DS20) | doruk = dip + | bant dışı kapanış = devam − | Wyckoff ↔ Bollinger kural 8 | iki DS ayrı |
| 12 | Busted kırılım (DS15) | busted daha güçlü + | taban kapanışla kırıldıysa hükmü yok (K5), C1 | Bulkowski ↔ Cemal | İKİ YÖNLÜ |
| 13 | Weinstein (DS08) | evre 2 en iyi alım | testte evre 1 (+%13,2) > evre 2 (+%4,1) | Weinstein ↔ Bulkowski | EVRE1 BİLGİ |
| 14 | Büyük resim (DS08) | evre 4 − (K19 / C6 destek) | dip havuzunda büyük resim şartı tanımca çelişir (VD10) | Bulkowski / Cemal ↔ VD10 | ANA − ama güç notu |
| 15 | Güçlü mü zayıf mı (DS18 ↔ DS44-C19) | RS yükselen + | stres gününde en zayıf + | Bulkowski ↔ Nauss | DS18 İKİ YÖNLÜ |
| 16 | RS kırılım öncesi (DS18) | yükselen RS + | düşen-düşen grupta kayıp daha küçük ('sezgiye aykırı') | Bulkowski (aynı sayfa) | İKİ YÖNLÜ |
| 17 | Onay mı zayıflık mı (DS06, DS14 ↔ DS09-11) | geri alma / kırılım sonrası + | zayıflıkta almak onaydan iyi (C21) | smc / DeMark ↔ Johnson | ayrı DS; C21 KAPALI |
| 18 | Eşit tepeler (DS23 BİLGİ) | mıknatıs + | düz tavan = aşağı formasyon (K2) | smc ↔ Cemal | İKİ YÖNLÜ |
| 19 | Boşluk dolumu (DS22) | aşağı boşluk daha sık dolar | yukarı / aşağı benzer (doğrulanamadı) | tastylive ↔ arama özeti | tek yön + |
| 20 | Derinlik (DS28) | derin düşen ortalama + | tipik (medyan) −, derinlikçe dönüş azalır | Brandes ↔ Brandes medyan, Mauboussin | İKİ YÖNLÜ |
| 21 | Boyut (DS32) | büyükte dönüş çalışır | küçük + (Brandes, Huddart, SIZE) | Teo, Market Sentiment ↔ A1 / A11 | elendi (kova); BİLGİ |
| 22 | Kaybeden × kalite (DS57) | F ≥ 7 + | kalite süzgeci getiriyi düşürdü | Zhu-Sun-Chen ↔ peas0c | İKİ YÖNLÜ |
| 23 | Sıkıntı × kaybeden (DS56) | ilk ayda dönüş + | kaybeden bacağı sıkıntıda sürer − | Da-Gao ↔ Avramov-Chordia | İKİ YÖNLÜ |
| 24 | İçeriden alım dipte (DS46) | büyük düşüş sonrası alım güçlü ('gülümseme') | tepeden uzak alım daha az bilgili; bilgi değil 'ucuz' inancı | tez ↔ Li ve ark., Piotroski-Roulstone | İKİ YÖNLÜ |
| 25 | Not düşürme (DS74, REC_DOWN) | düşürme − (gün) | sürü satışı sonrası dönüş + (çeyrek) | Womack ↔ Brown-Wei-Wermers | DS74 elendi (ufuk) |
| 26 | S&P çıkarma (DS70) | geçici + | kalıcı − | Chen-Noronha-Singal ↔ Kumar ve ark. | İKİ YÖNLÜ |
| 27 | Geri alım türü (DS58 ↔ DS59) | açık piyasa + | ASR − | Peyer-Vermaelen ↔ Michel-Oded-Shaked | tür ayrı DS |
| 28 | Açığa satış kapanışı (DS64) | kârla kapanış + / zararla − | 'sıkışma = yukarı' inancı | 2026 çalışması (doğrulanamadı) ↔ yaygın inanç | İKİ YÖNLÜ |
| 29 | Stratejik seçenekler (DS62) | duyuru günü + | 6 ayda − | Giedt-Rim (giriş zamanına göre) | giriş duyurudan sonra: − |
| 30 | Borç takası (DS63) | duyuru − | başarılı tamamlanma + | Lie-Lie-McConnell | iki bayrak |
| 31 | Russell göçü (DS71) | yeniden yapılanma öncesi + | sonrası − | Dimensional | pencereye göre |
| 32 | Ters bölünme (DS53) | 3 yıl − | küçük şirkette + (doğrulanamadı) | Kim-Klein-Rosenfeld ↔ Ogwu | tek yön − |
| 33 | Going concern (DS61) | verilişte − sürüklenme | kalkışta sürüklenme yok | Kausar-Taffler-Tan (aynı kaynak) | ? |
| 34 | İflastan çıkış (DS72) | ort. +%40-50 | medyan 0; 2010-19'da üstünlük yok | Eberhart ve ark. ↔ Jiang-Wang-Yang | elendi |

İKİ YÖNLÜ işaretli DS (öncelik listesinde): DS01, DS02 (AVR), DS04, DS08 (EVRE1 kolu), DS09, DS10, DS11, DS15, DS18, DS28; listede olmayan: DS27, DS46, DS50, DS56, DS57, DS64, DS70. Ön kayıtta bunlar için çift yönlü p (ay kümeli permütasyon) kullanılır; yön sonuçtan sonra seçilmez.

## 5. ÖNCELİK (sınıf I'den 25; BH q 0,10, m = 25 sabit)

Sıralama ölçütü (önceden yazılı): (1) kaynak gücü hakemli > kitap / uygulayıcı veri tabanı > blog > sosyal; (2) bağımsız kaynak sayısı (kol sayısı); (3) bağımsız test / sayı varlığı; (4) Cemal'in kurallarına yakınlık (dip savunması, parabol / kazan, çift kazan, dosya; destek ya da çelişki, ikisi de sınama değeri taşır). BH'ye yalnız ANA kol girer (25 p); BİLGİ kolları BH dışı. Dışarıda kalan sınıf I: DS24 (FVG, forex İDDİA), DS26 (POC, gün içi uyarlaması İDDİA), DS27 (ATRX, İDDİA + DS28 / ATRP ile örtüşme), DS29 (P&F, H15). Listedeki sosyal / blog İDDİA: DS10, DS25 (2 ≤ 5).

| sıra | DS | düz dil | ANA kol ve SABİT eşik | kaynak gücü / sayı | bağımsız test | Cemal yakınlığı | iki yönlü |
|---|---|---|---|---|---|---|---|
| 1 | DS01 | Sona doğru hızlanan düşüş iyi, U yol kötü | KONV10 alt beşte bir (eğitim beşlik sınırı) | hakemli JFQA; 1 kaynak | t 7,31; beşlilerin hepsinde %0,78-0,97 | K3 / K22 / H2 çelişki | EVET |
| 2 | DS04 | Büyük tek gün düşüşünden sonraki sıçrama fazı | r_s ≤ −%15 son 120 bar ve t − s ∈ [2, 23] | kitap / uygulayıcı + hakemli (Cox-Peterson) + İDDİA (Guo); 2 kol, 4 kaynak | Bulkowski sayıları (n yok) | CD22 destek, H2 çelişki | EVET |
| 3 | DS02 | Düşük devirli kaybeden döner | DEVIR vekili alt onda (eğitim) | 2 hakemli (RFS, JF) | uluslararası örneklem (Medhat-Schmeling) | E5 destek (zayıf); hacim sınırı | AVR EVET |
| 4 | DS03 | Sektörden bağımsız düşüş döner | ART21 alt onda (eğitim) | hakemli MS + NY Fed | 1982-2009, 3x | D2 tamamlayıcı | HAYIR |
| 5 | DS08 | Evre 4'te bıçak sürer | EGIM150 < 0 ve C < SMA150 | kitap + Bulkowski | n 127 / 127 | K19 / C6 destek, VD10 çelişki | EVRE1 kolu |
| 6 | DS05 | Satış doruğu dibi gösterir | son 60 barda doruk barı (V ≥ 2 x SMA20, aralık eğitim üst çeyreği, CLV eğitim medyanı) | kitap + hakemli (Huddart) + İDDİA; 3 kol | Huddart: küçük çeyrek 1 haftada ~%5 | K26 destek, K17 çelişki | HAYIR (A13 kolu iki yönlü) |
| 7 | DS06 | Sahte kırılım (dip süpürme) döner | Turtle Soup: 20 gün, ≥ 4 bar, 3 x ATR14 | kitap + 4 İDDİA; 2 kol | yok | K5, K26, B8 destek | HAYIR |
| 8 | DS11 | 7 gün dibinde kapanış: sıçrama mı bıçak mı | C_t ≤ min(C_{t−6..t}) | kitap + İDDİA test (SPY) + H2 | SPY 333 işlem | K50 / H2 doğrudan | EVET |
| 9 | DS09 | RSI(2) ≤ 5 sıçrama | RSI2 ≤ 5 | kitap (Connors) | yok (hisse) | H2 çelişki | EVET |
| 10 | DS14 | Son alçalan tepenin kapanışla aşılması | CHoCH: C_{t−1} ≤ LH2 < C_t (6/6 pivot) | kitap (DeMark, Wyckoff) + İDDİA; 2 kol | yok | B1 / K21 destek | HAYIR |
| 11 | DS15 | Busted aşağı kırılım | derinlik ≤ %10, C_t > H_b | uygulayıcı veri tabanı | Bulkowski %54 / %38 | K5 / C1 çelişki | EVET |
| 12 | DS16 | Wyckoff ikinci test | e, q1, q2 eğitim medyanı | kitap | yok | K26, CD18 destek | HAYIR |
| 13 | DS18 | Göreli güç eğimi yukarı | SMA22(RS) eğimi > 0 | uygulayıcı veri tabanı | 15.763 desen (fark küçük) | B13 destek, C19 çelişki | EVET |
| 14 | DS21 | Gece payı yüksek düşüş dönmez | GECE_PAY eğitim üst çeyreği (−) | hakemli (Miwa) ikincil özeti + envanter GAP_OVN | yok (özet) | yeni | HAYIR |
| 15 | DS22 | Aşağı boşluk doldu | r_i ≤ −2σ20, C_t ≥ C_{i−1} ilk kez | uygulayıcı araştırma notu (tastylive) + İDDİA | 20 hisse 5 yıl | B1 akraba | HAYIR |
| 16 | DS13 | TD setup 9 | 9 art arda C < C_{−4}, 9. bar t | kitap | yok | yeni | HAYIR |
| 17 | DS12 | Elder Impulse kırmızıdan çıkış | EMA13 + MACD(12,26,9) | kitap | yok | K47 akraba | HAYIR |
| 18 | DS19 | %b W dip | BB(20,2); ara / tol eğitim | kitap (Bollinger) | yok | K47 destek | HAYIR |
| 19 | DS20 | Alt bantta yürüme (−) | YURU eğitim üst çeyreği | kitap (Bollinger) | yok | K19 destek, DS05 çelişki | HAYIR |
| 20 | DS17 | Aşağı gün direnci | DIRENC eğitim üst çeyreği | kitap (Wyckoff) | yok | B13 akraba | HAYIR |
| 21 | DS07 | Smash day dönüşü | 8 gün; H_t > H_{t−1} | kitap + İDDİA (vadeli) | vadeli küçük örneklem | B7 / K12 destek | HAYIR |
| 22 | DS28 | Derinlik ≤ −%60 | C / max252 − 1 ≤ −0,60 | ikincil (Brandes, Mauboussin); 2 kol | Brandes 1.904 olay (3 yıl) | CD22, I3 | EVET |
| 23 | DS10 | DV2 < 10 | DV2 < 10, pencere 252 | blog İDDİA | Russell 3000 batanlar dahil, p 0,017 | DS09 ile aynı | EVET |
| 24 | DS23 | Yukarıda dolmamış boşluk mıknatısı | 2σ boşluk, +%5..+%10 | uygulayıcı (tastylive) + İDDİA | tastylive | K2 çelişki (BİLGİ kolu) | ANA HAYIR |
| 25 | DS25 | Dipten çapalı AVWAP testi | C > AVWAP_low, son 3 bar değme (e eğitim medyanı) | sosyal İDDİA | tek işlem | yeni | HAYIR |

Korelasyon notu (ön kayıt için, önceden): DS01 ↔ DS11 ↔ DS09 ↔ DS10 (son günlerin zayıflığı) ve DS05 ↔ DS16 (aynı doruk barı) yüksek ilişkili beklenir; BH bağımlılık altında da geçerli (pozitif bağımlılık), ama 'iz' sayımında aynı aileden birden fazla geçen tek bulgu sayılır.

## 6. ÇELİŞKİ (kollar arası ve kaynaklar arası)
1. Açık pozisyon verisi: SINYAL_ENVANTERI SI ailesini İNDİR, IZ_VERI_ENVANTERI 'VAR' (/tmp/k66, kalıcı değil), KOL D EVET†, KOL A 'envanterde var' yazıyor. Karar: sınıf III (FINRA'dan yeniden ~10 dk, kalıcı pakete alınır); eğitim 2018-22'ye kısalır.
2. FTD eşiği %1 / %1,25 / %1,7 (KOL B); başarı oranları (IBD %70-80, Stockbee %80, Hanna 'yazı tura') n vermiyor. DS38 KOŞUL sınıfında, ölçülmez.
3. F_SCORE: KOL A 'EVET† 2021+', KOL B 'EVET† ABD 2021+', SINYAL_ENVANTERI 'İNDİR'. Eğitim 2016-22 için veri yok → sınıf III.
4. Pivot uzunluğu: KOL C P(5) ('3 / 5 / 10 içinden önceden 5' = kaynak dışı seçim), KOL B 6/6, smc 50. Tek standart: 6/6 (stock-pattern, WEB_GUNCEL kaynağı).
5. Turtle Soup önceki dip yaşı 3 / 4 gün (KOL B): açılan sayfadaki 4 sabitlendi.
6. TD Sequential kesişim / mükemmellik tanımı kaynaklar arasında farklı: ANA kol kesişimsiz.
7. 52h dibi yönü: Chen-Yu / Huddart (+) ↔ George-Hwang / Brock (−) (ikincisi doğrulanamadı).
8. KOL A A10'u 'YENİ, ölçülebilir' saydı; DS olay tanımı (F15 ≤ 0,25) ile mekanik eşdeğer → elendi.
9. KOL C C7'yi ön kayıt adayı gösterdi; R18 ≥ 0,5 eşiği DS olayında neredeyse boş küme → elendi.
10. Endeks serisi: KOL C SPY / STOXX 600 der, KOL B evren eşit ağırlık; V_ABD / V_AVR'de endeks serisinin varlığı denetlenmedi. Tek standart: evren eşit ağırlık (K7 yaşayan evren notuyla).
11. sec_ozet form adı 2024'te 'SC 13G / 13D' → 'SCHEDULE 13G / 13D' (KOL D HATA 1); K56/kurumsal_olaylar.py satır 31 ve K56/faz1_yerel.py satır 29 yalnız eski adla süzüyor (2024+ sahiplik olaylarını kaçırır). DS49 iki adı birlikte kullanmalı; kod düzeltmesi ana model işi.
12. Kollar 'YENİ' sayıları: A 23, B 23, C 16, D 25 = 87 'YENİ' beyanı; tekilleştirme + süzgeç sonrası 56 (I 29, II 10, III 17). Fark: aynı ölçünün kollar arası tekrarı (13 satır), mekanik / boş küme (3), kapsam dışı veri, KAPALI ve mevcut.
13. Sektör: KOL A sektor_ABD.csv (1.416 hisse, bugünkü sınıf) kullanır; ABD fiyat evreni 4.678 (k60) / 1.411 (V_ABD). AVR için sektör dosyası yok → DS03 AVR kolu piyasa artığıdır (kaynakla aynı ölçü değil).
14. V_AVR'de 13.622 satırda (362 hisse) açılış H-L dışında (IZ_VERI_ENVANTERI): açılışa dayanan ölçüler (DS06 Oops kolu, DS21, DS05 C15 / C16 renk şartı, DS33) AVR'de ön temizlik olmadan ölçülmez; kollardan hiçbiri bunu yazmadı.

## 7. HATA (bu işte bulunan; ana model IK_HATA'ya işler)
1. KOL C C7 (geri alma hızı): önerilen eşik DS olay tanımıyla çelişir (R18 ≥ 0,5 ve F15 ≤ 0,25 birlikte neredeyse olanaksız); ön kayda girseydi n ≈ 0 ve 'ÖLÇÜLEMEDİ' olurdu. Tür: ölçüt / tanım.
2. KOL A A10 (LOW52) ön kayıt listesinde 8. sırada: DS olayı zaten dip konumunu sabitler (K1 mekanik). KOL A kendisi H-A8'de riski yazmış ama listeden çıkarmamış. Tür: kontrol grubu / mekanik üstünlük.
3. KOL C C8 tablosunda '1,01' eşiği var, notunda 'kaynakta yok → eğitim medyanı' deniyor: iç çelişki. DS25'te eğitim medyanı alındı. Tür: ön kayıt (K9).
4. KOL D D17 ön kayıt önerisi çift seçenekli eşik ('%20 sabit ... eğitim üst çeyrekle değiştirilmesi tek seferlik seçilir'): eşik ön kayıtta tek olmalı. DS64'te eğitim üst çeyreği seçildi (kaynakta sayı yok kuralı). Tür: K9.
5. KOL B B13 ön kayıt önerisi '±%3 (kaynakta yok → eğitim medyanıyla değiştirilebilir)': yine çift seçenek. DS16'da eğitim medyanı. Tür: K9.
6. KOL C C13 pivot P(5) seçimi 'eğitim döneminde 3 / 5 / 10 içinden önceden 5' kaynak da çeyrek de değil; 6/6 ile değiştirildi. Tür: K9.
7. KOL B B19 / B27 ve KOL C C18 'ara 5-40 bar' gibi pencereleri kaynakta olmadan sabitliyor; DS19'da eğitim çeyrekleriyle değiştirildi. C16 W = 5 ve C10 60 / 50 kova kaynakta yok ve çeyreğe çevrilemeyen pencere parametresi: ön kayıtta 'kaynak dışı, sonuç görülmeden sabit' diye açık yazılmalı (DS05 BİLGİ kolu, DS26 öncelik dışı).
8. Sınıf III'teki EDGAR tam metin olayları (DS58, DS59, DS61-DS63, DS65, DS68, DS69): SEC User-Agent'ta iletişim e-postası ister; CLAUDE.md e-postayı yalnız Form 4 (fi_k30_indir) indirmesi için izinli kılar. Yeni kullanım Cemal'in iznine bağlı (KARAR GEREKEN). Kollar bunu 'İNDİR (ücretsiz)' diye yazdı. Tür: süreç (K13).
9. k67 Yahoo analist günlüğü / bilanço takvimi /tmp'de ve kalıcı değil (IZ_VERI_ENVANTERI); iş tanımı (c) bunu EVET sayıyor, KOL A / D EVET yazdı. Sınıf II'de DS44 / DS45 / DS47 bu veriye bağlı: koşudan önce islenmis-veri'ye paketlenmeli. Tür: veri.
10. DS48 (Form 144): 2023 öncesi kâğıt başvurular sec_ozet'te eksik olabilir; eğitim 2016-22 ile sınama 2023-26 kapsamı farklı → iki dönem yön karşılaştırması (K8) yapısal olarak bozulur. Ön kayıtta yalnız 2023+ ya da kapsam düzeltmesi yazılmalı. Tür: veri / dönem.
11. DS04: −%15 tek gün düşüşünü bölünme / birim hatası da üretir (K6; BIST'te 12.03.2020 öncesi ±%20 marjı, ABD Yahoo bölünme düzeltmesi). Ölçümde olay günleri bölünme takvimiyle eşlenmeli. Tür: veri.
12. DS08 / DS20 / DS28: özellik DS olayında çok sık (EVRE4) ya da derinlik / oynaklıkla iç içe; 'eş = DS içi tutmayan' kurulumunda eş sayısı küçük kalabilir. Ön kayıtta tutan / tutmayan olay sayısı huni olarak getirisiz yazılmalı (güç < 0,80 → ÖLÇÜLEMEDİ). Tür: K8 / K1.

## 8. KONTROL LİSTESİ
| madde | durum | kanıt |
|---|---|---|
| K1 kontrol grubu | EVET (süzgeç g) | Her DS için mekanik üstünlük sorusu soruldu; DS30, DS31, DS34 elendi, DS32 kova ile sıfırlandı; DS08 / DS11 / DS17 / DS20 / DS27 / DS28 'HAYIR*' notlu; eş = aynı gün aynı kova DS içi |
| K2 geleceğe bakma | EVET | Bütün pivotlar 6/6 ve onayı t'ye kadar; Bulkowski kırılım sonrası RS dışarıda; olaylar başvuru + 1; FINRA ödeme + 12 gün; sektör sınıfının bugünkü olduğu (DS03) yazıldı |
| K3 geçerli bar | UYGULANMAZ (not) | Ölçüm yok; DS04 / DS05 / DS06 için H > L, V > 0 şartı satırda |
| K4 tekilleştirme | EVET (hipotez düzeyi) | 123 → 87; her kod tam bir kez; ölçümde hisse başına 15 barda 1 olay (ANA) çerçeveden |
| K5 giriş fiyatı | UYGULANMAZ (not) | Kaynakların kapanış girişi (Guo, Huddart, Connors) ortak riskte yazıldı; cetvel t+1 açılış |
| K6 veri birimi | EVET (not) | V_AVR açılış sorunu (ÇELİŞKİ 14), DS04 bölünme riski (HATA 11) yazıldı |
| K7 hayatta kalma | EVET | Ortak risk satırı: ABD batan ~0, AVR yaşayan liste → (+) lehine, (−) aleyhine; sec_ozet kapsam dışı hisseler evrenden çıkarılır |
| K8 örneklem / dönem | EVET (not) | n riski olan DS'ler (DS13 countdown, DS15, DS22, DS51, DS70) ve DS48 dönem kapsam farkı yazıldı; BH m = 25 sabit |
| K9 ön kayıt | EVET | Eşikler kaynaktan ya da eğitim çeyreği; kolların çift seçenekli / kaynak dışı eşikleri (HATA 3-7) tek değere indirildi; bu dosya ön kayıt değil |
| K10 ayrıştırma | UYGULANMAZ (not) | Ham kaynak okunmadı; sec_ozet form adı değişimi (ÇELİŞKİ 11) ve DoD ad eşleme riski (DS66) not edildi |
| K11 yeniden üretim | UYGULANMAZ | Sayı üretilmedi; kaynak sayıları kolların açılan sayfalarından aktarıldı, yeni sayı yazılmadı |
| K12 ifade | EVET | 'İz / anlamlı / emare' sözü kullanılmadı; kaynak sayıları ile yorum ayrı sütunda; İDDİA etiketleri korundu |
| K13 süreç | EVET | Yalnız DS_ELESTIRI.md yazıldı; yasak defter dosyalarına ve üretim zincirine dokunulmadı; commit yok; URL açılmadı; e-posta / anahtar yok; SEC e-posta izni karar olarak işaretlendi (HATA 8) |
| K14 boyut | UYGULANMAZ | Öneri işi değil |
