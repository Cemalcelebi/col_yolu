# VDYT ÖN KAYIT — Volatilite Denge ve Yön Tahmini (ölçümden ÖNCE)

Yazım zamanı: 2026-11-12 06:25:36 UTC (2026-11-12 09:25 TR)
ESIK_SHA256: b999ffc73273aa3b2fc54deac7aea96963ea38894ce8a3cdbe3c1159fdec8bd6
KOD_SHA256: 9a11fad3a6c486a6ed72009da8c9b86e63f4cda60586b3ff1d503ac3d6bb8d38
Sürüm: VDYT v1.0 (2026-11-12): Faz 1 (envanter, ön kayıt, kod + sentetik test, kapsam sayımı); ölçüm Faz 2'de, ön kayıt git'e işlendikten sonra

Bu dosya git'e işlenmeden, eşik mührü / kod sha256'sı / veri sha256'ları tutmadan `kos` ÇALIŞMAZ (VdytHata, çıkış 1). Sonuç görüldükten sonra tanım,
eşik, pencere, ufuk, bölme, model ya da karar kuralı değişmez; değişirse bu dosyada SAPMA olarak tarihli yazılır ve mühür / kod satırı yeniden işlenir.

## 0. Sınır ve beyan
- VDYT ayrı araştırma motorudur (Cemal'in açık isteği, 12 Kasım 2026). Çöl Yolu'nu, IZ_KARNE karar ölçütlerini (FI_OLCUT, tek cetvel) ve mevcut kodları
  DEĞİŞTİRMEZ, onlardan kod içe almaz; sonuçları Çöl Yolu kararlarına bağlanmaz.
- Çöl Yolu'nda KAPALI konulara değen değişkenler (hacim / hacim daralması, mum şekli ölçüleri: gövde, fitil, kapanış konumu; sektör rejimi) YALNIZ bu
  motorda, bu ön kayıttaki tanımlarla ölçülür. Kapalı konu yeniden açılmış sayılmaz; VDYT sonucu Çöl Yolu'na 'yaz' kararı olmadan taşınmaz.
- VDYT sonucu doğrulanmış sinyal değildir; yüksek genişleme olasılığı tek başına alım sinyali değildir; ilişki nedensellik diye yorumlanmaz; eğitim
  başarısı tahmin başarısı diye gösterilmez; yeni sinyal ancak bağımsız ileriye dönük testle (KASA) kanıtlanırsa söylenir; başarısız testler rapordan çıkmaz.

## 1. Sorular
S1 sıkışma ne zaman biter; S2 bitiş olasılığı yaşla nasıl değişir (hazard); S3 bitişten önce / sırasında hangi olaylar etkili ('haber bitirdi' ile
'zaten bitecekti' ayrı); S4 bitişin yönü; S5 hisseye özgü süre mi, piyasa rejimi mi, haber / bilanço mu daha açıklayıcı.
NİHAİ SORU: süre + kendi geçmişi + olay takvimi + savunma hattı (+ volatilite / hacim / mum / fiyat ölçüleri) birlikte, genişlemenin NE ZAMAN (Motor 1) ve
HANGİ YÖNE (Motor 2) olacağını basit piyasa kontrollerinden (bölüm 9) daha iyi tahmin ediyor mu?

## 2. Veri ve dönem
- Karar pazarları: BIST = V_BIST (islenmis-veri; OHLCV, bölünme düzeltmeli; yaşayan 581), 2015-06-01+; ABD = k60_fiyat (Yahoo günlük OHLCV 2010+, 4.678 hisse; yaşayan), 2010-01-01+.
  Yanlılık kontrolü: BIST_K62 = K62 İş Yatırım günlük kapanış 2008+ (kotasyondan çıkanlar dahil; açılış / yüksek / düşük YOK); rol: yanlılık kontrolü: yalnız kapanış tanımları (T2, T3, T4) ve RV genişlemesi; karar pazarı değil.
- Kesik: bütün fiyatlar 2026-08-31'de kesilir (fon krizi). Etiket penceresi kesiği aşan karar noktası ölçülmez; açık bölge kesikte SANSÜR.
- Bar temizliği: OHLC eksik / kapanış <= 0 atılır; hacim <= 0 (işlemsiz gün) atılır; H = max(O,H,C), L = min(O,L,C); iki bar arası > 15 takvim günü = kopukluk (açık bölge SANSÜR, koşu sayımı yeniden).
- Uygunluk (bölge tespit gününde; karar noktaları yalnız uygun bölgelerden): BIST >= 252 bar geçmiş ve 20 gün medyan işlem değeri o günün BIST kesitinde
  %20 yüzdeliğinin üstünde; ABD tür EQUITY, >= 252 bar, o gün ekranda görülen fiyat (bölünmeler geri alınmış) >= 2.0 $, 20 gün medyan işlem değeri >= 1 milyon $ (K60 kuralı).
- Maliyet (yalnız bilgi amaçlı getirilerde, tek yön): BIST 30 bp, ABD 10 bp.
- Endeks (rejim ve pazar yönü): BIST XU100.IS, ABD SPY (k58 Yahoo); yoksa eşit ağırlıklı medyan getiri (beyan).
- Sektör: BIST sektor_BIST.csv 'sektor'; ABD SEC SIC 2 haneli ana grup (k35_sic, CIK → bugünkü kod; < 10 üyeli grup SIC bölümüne birleşir).

## 3. Test sırası (Faz 2; hepsi raporlanır)
1. Veri yükleme + mühür / kod / veri sha256 / git doğrulaması (biri tutmazsa ret).
2. Günlük ölçüler (bölüm 4.1), panel (uygunluk, tertiller, rejim).
3. Bütün kombinasyonlarda sıkışma bölgeleri (bölüm 4.3), yön (4.5), karar noktaları ve etiketler (4.6).
4. Süre analizi (bölüm 5): KM, CIF, yaş kovası hazard'ı, rejim tertiline göre hazard; süre yaklaşımları A-D'nin ileriye dönük Brier'i (bölüm 9).
5. Motor 1 (genişleme; 5 ana tanım x 3 ufuk) ve Motor 2 (yön; 5 ana tanım) walk-forward (bölüm 10), temellere karşı (bölüm 9), ablasyon (ana tanım / ana ufuk).
6. Birleşik üç sınıf (bilgi) + basit portföy (bilgi).
7. Olay analizi E1, E2 (bölüm 6), her ana tanım x her olay türü.
8. Savunma hattı H1-H5 (bölüm 7), karşılaştırma grupları K1-K6 (bölüm 8).
9. Plasebolar P1 (rastgele olay günü), P2 (rastgele sıkışma bölgesi) (bölüm 12).
10. Çoklu test (BH) + hipotez tablosu; karar tablosu.
11. Aşama 'wf' biter → rapor. Aşama 'kasa' ayrı komutla BİR KEZ açılır (bölüm 10) → final karar tablosu.
12. Grafik arşivi (bölüm 13), rapor (bölüm 15).

## 4. Tanımlar (hepsi yalnız t ve öncesi barlardan)
### 4.1 Günlük ölçüler (`vdyt_olculer`)
TR = max(H-L, |H-C[-1]|, |L-C[-1]|); TRn = TR / C[-1]; ATR14 = 14 bar TR ortalaması; NATR14 = ATR14 / C; RV20 = 20 bar log getiri std (ddof 1);
BBW20 = 4 x std(C,20, ddof 0) / SMA20; geçmiş penceresi = [t-250, t-1], en az 200 geçerli değer; yüzdelik = (küçük + 0,5 x eşit) / geçerli.
Diğer: RV5/RV20; hacim oranı = medyan(V,20) / medyan(V,250); gövde / aralık, üst ve alt fitil / aralık, kapanış konumu (C-L)/(H-L) (son 10 bar ort.);
gövde / C son 10 ort. ÷ 250 ort.; ln(C/SMA20, 50, 200); SMA50 eğimi (10 bar ln); ln getiri 20 / 60; likidite = ln medyan(C x V, 20); yükselen gün hacim payı (20).
### 4.2 Sıkışma tanımı ALTERNATİFLERİ (önceden; hepsi raporlanır, sonradan seçme yok; ANA = T1)
| kod | ad | tanım | eşikler | veri |
|---|---|---|---|---|
| T1 | ATR oranı | NATR14(t) / medyan(NATR14[t-250..t-1]) <= eşik; NATR14 = 14 günlük ortalama gerçek aralık / kapanış | 0.7, 0.6, 0.8 (ilk = ana) | OHLC |
| T2 | Gerçekleşen volatilite yüzdeliği | RV20(t) (20 günlük log getiri std) hissenin kendi [t-250..t-1] RV20 değerleri içinde yüzdelik <= eşik | 0.2, 0.1, 0.3 (ilk = ana) | kapanış |
| T3 | Bollinger genişliği yüzdeliği | BBW20 = 4 x std(C,20) / SMA20; kendi [t-250..t-1] BBW20 değerleri içinde yüzdelik <= eşik | 0.2, 0.1, 0.3 (ilk = ana) | kapanış |
| T4 | Dar bant (kapanış) | (max C - min C) / ort C (son 20 kapanış) / sigma_ref <= eşik; sigma_ref = medyan(RV20[t-250..t-1]) (günlük sigma birimi) | 3.5, 2.5, 4.5 (ilk = ana) | kapanış |
| T5 | Bileşik | T1-T4'ün ANA eşiklerinden en az 3'ü aynı gün sağlanır | - (ilk = ana) | OHLC |
### 4.3 Bölge başlangıç / bitiş kuralı (`vdyt_bolgeler`)
- Açılış: 'sıkışık' durum 10 işlem günü kesintisiz → bas = koşunun ilk günü, tespit = bas + 9 (bölge tespit kapanışında bilinir; yaş = t - bas + 1, tespitte yaş 10).
- Bitiş (tespitten SONRAKİ ilk gerçekleşen): GENİŞLEME (4.4) | SÖNME: durum 5 gün üst üste yanlış (bitiş = 5. gün) | SANSÜR: veri sonu / kesik / kopukluk.
- Bölge kapandıktan sonra yeni koşu sayımı ertesi günden başlar (aynı tanımda bölgeler çakışmaz).
### 4.4 Genişleme (bitiş) tanımı (eşiklerin hepsi önceden; ANA = TR, k = 2.0)
- TR: ort(TRn[t-2..t]) >= k x medyan(TRn, bölgenin t-3'e kadarki son 60 günü); TRn = gerçek aralık / önceki kapanış; k ∈ [2.0, 1.5, 2.5].
- RV: std(log getiri[t-4..t]) >= k x std(bölgenin t-5'e kadarki son 60 günlük log getirisi) (kapanış verisi için; ANA tanımda duyarlılık).
- Referans gün sayısı < 8 ise genişleme sayılmaz. Genişleme GÜNÜ = bit (genişlemenin bilindiği gün); pencerenin ilk günü gen_bas (grafik ve olay bayrakları için).
### 4.5 Yön
- Y1 (ANA): bölge kapanış aralığı [Lo, Hi] = bas .. gen_bas-1 kapanışları; gen_bas'tan bit + 20'ye kadar ilk kapanış > Hi → YUKARI, < Lo → AŞAĞI, hiçbiri → BELİRSİZ; veri yetmezse ölçülmez.
- Y2: işaret(ln(C[bit + 10] / C[gen_bas - 1])).
### 4.6 Karar noktaları ve etiketler (bağımlılık kuralı)
- Her bölgede yaşlar [10, 20, 40, 60, 90, 120] (o günün kapanışında bölge hâlâ açıksa), her biri ayrı satır; belirsizlik HİSSE kümeli bootstrap (bölgeler hisse içinde iç içe).
- Motor 1 etiketi y_h, h ∈ [5, 10, 20] (ANA 10): GENİŞLEME t < bit <= t+h → 1; bit > t+h ya da SÖNME t+h içinde → 0; SANSÜR t+h içinde ya da t+h veri dışında → ölçülmez.
- Motor 2 etiketi: y20 = 1 olan ve Y1 ∈ (YUKARI, AŞAĞI) satırlarda 'yukarı' = 1(Y1 = YUKARI). Çözülme tarihi = bit + 20.
- Savunma hipotezleri ve bölge karşılaştırmaları bölge başına TEK satır kullanır (genişlemeden önceki son karar noktası).
- Etiket tamamlanma tarihi: son_h = t + h. bar günü; Motor 2 için y1_son.
### 4.7 Kombinasyonlar (tanım x eşik x genişleme)
| ad | rol | tanım | eşik | k | genişleme |
|---|---|---|---|---|---|
| T1 | ana | T1 | 0.7 | 2.0 | TR |
| T2 | ana | T2 | 0.2 | 2.0 | TR |
| T3 | ana | T3 | 0.2 | 2.0 | TR |
| T4 | ana | T4 | 3.5 | 2.0 | TR |
| T5 | ana | T5 | T1-T4 ana, >= 3 | 2.0 | TR |
| T1_e0.6 | duyarlilik | T1 | 0.6 | 2.0 | TR |
| T1_e0.8 | duyarlilik | T1 | 0.8 | 2.0 | TR |
| T2_e0.1 | duyarlilik | T2 | 0.1 | 2.0 | TR |
| T2_e0.3 | duyarlilik | T2 | 0.3 | 2.0 | TR |
| T3_e0.1 | duyarlilik | T3 | 0.1 | 2.0 | TR |
| T3_e0.3 | duyarlilik | T3 | 0.3 | 2.0 | TR |
| T4_e2.5 | duyarlilik | T4 | 2.5 | 2.0 | TR |
| T4_e4.5 | duyarlilik | T4 | 4.5 | 2.0 | TR |
| T1_k1.5 | duyarlilik | T1 | 0.7 | 1.5 | TR |
| T1_k2.5 | duyarlilik | T1 | 0.7 | 2.5 | TR |
| T1_RV | duyarlilik | T1 | 0.7 | 2.0 | RV |
| K62:T2 | ana | T2 | 0.2 | 2.0 | RV |
| K62:T3 | ana | T3 | 0.2 | 2.0 | RV |
| K62:T4 | ana | T4 | 3.5 | 2.0 | RV |
| K62:T2_e0.1 | duyarlilik | T2 | 0.1 | 2.0 | RV |
| K62:T2_e0.3 | duyarlilik | T2 | 0.3 | 2.0 | RV |
| K62:T3_e0.1 | duyarlilik | T3 | 0.1 | 2.0 | RV |
| K62:T3_e0.3 | duyarlilik | T3 | 0.3 | 2.0 | RV |
| K62:T4_e2.5 | duyarlilik | T4 | 2.5 | 2.0 | RV |
| K62:T4_e4.5 | duyarlilik | T4 | 4.5 | 2.0 | RV |
ANA kombinasyonlarda bütün analizler; DUYARLILIK kombinasyonlarında yalnız bölge sayımı + süre analizi (KM, CIF, hazard).

## 5. Süre (S1, S2, S5)
- KM (GENİŞLEME nedenine özgü; SÖNME ve SANSÜR sansür), herhangi bitişe göre hayatta kalma, Aalen-Johansen kümülatif GENİŞLEME olasılığı (CIF), yaş başına
  kesikli hazard; yaş kovaları [[10, 19], [20, 39], [40, 59], [60, 89], [90, 119], [120, 100000]]; tespit günündeki piyasa rejimi tertiline göre hazard. 'Süreye bağlı Markov' ayrıca kurulmaz: kesikli yaş hazard'ı
  zaten süreye bağlı geçiş olasılığıdır (beyan).
- Yaklaşımlar (ileriye dönük, Motor 1 etiketleriyle; özellik grupları bölüm 10): A ORTAK = ['SURE']; B HİSSE = ['SURE', 'HISSE']
  (hissenin yalnız t'den ÖNCE biten GENİŞLEME / SÖNME bölgeleri; en az 3 bölge yoksa 'yetersiz' bayrağı ve oran 0);
  C REJİM = ['SURE', 'REJIM']; D ADAPTİF = ['SURE', 'HISSE', 'REJIM']. Her biri T0 (süresiz) ve T1 (süreli) temeline karşı.
- WF aşamasında 2024-01-01'i aşan bölgeler 2023 son işlem gününde SANSÜR sayılır (KASA verisi görülmez).

## 6. Olaylar (S3) — kategori, bilgi tarihi, pencereler
| kod | pazar | kategori | olay | kaynak | önceden bilinir | bilgi tarihi / g0 kuralı |
|---|---|---|---|---|---|---|
| BIST_BILANCO | BIST | A | bilanço (KAP Finansal Rapor, hisse-yıl-dönemin ilk raporu) | /tmp/k62_veri/kap (2009-06+) | EVET | KAP yayın saati: < 18:00 ise o işlem günü, >= 18:00 ya da tatil ise sonraki işlem günü |
| BIST_TEMETTU | BIST | A | hak kullanım (temettü / bölünme) günü, K62 ham / düzeltilmiş kapanış oranı değişimi | /tmp/k62_veri/fiyat | EVET | hak kullanım günü (duyuru günü bilinmiyor; özellikte yalnız o gün ve sonrası) |
| BIST_SERMAYE | BIST | B | ödenmiş sermaye değişimi (bedelli / bedelsiz), K62 sermaye alanı | /tmp/k62_veri/fiyat | HAYIR | sermayenin değiştiği gün (karar / duyuru günü bilinmiyor) |
| BIST_ICERIDEN_ALIM | BIST | B | içeriden net alım bildirimi (KAP Pay Alım Satım) | kap_iceriden (2022-07+) | HAYIR | KAP yayın saati kuralı |
| BIST_ICERIDEN_SATIM | BIST | B | içeriden net satım bildirimi (KAP Pay Alım Satım) | kap_iceriden (2022-07+) | HAYIR | KAP yayın saati kuralı |
| BIST_FON_GIRIS | BIST | B | fon portföyüne giriş bildirimi (KAP fon raporu; fonun önceki raporunda yok) | G.pkl (2023-01+) | HAYIR | rapor yayın saati (bilinme) KAP kuralı |
| ABD_BILANCO | ABD | A | bilanço günü: 2022-12+ Nasdaq takvimi; öncesi 10-Q / 10-K başvuru günü (VEKİL) | pead/liste_abd + EDGAR | EVET | Nasdaq: o gün (saat çoğunlukla verilmemiş); EDGAR: başvuru günü (özellikte ertesi işlem günü) |
| ABD_TEMETTU | ABD | A | temettü / bölünme hak kullanım günü (Yahoo olayları) | k60_fiyat events | EVET | hak kullanım günü |
| ABD_VEKALET | ABD | A | DEF 14A vekâlet bildirimi (genel kurul yaklaşıyor) | EDGAR | EVET | başvuru günü; özellikte ertesi işlem günü |
| ABD_8K | ABD | B | 8-K (madde kodu YOK; bilanço günü +-3 iş günü dışındakiler) | EDGAR | HAYIR | başvuru günü; özellikte ertesi işlem günü |
| ABD_SERMAYE | ABD | B | pay arzı / raf kaydı (S-1, S-3, S-3ASR, 424B1, 424B3, 424B4, 424B5; 424B2 hariç) | EDGAR | HAYIR | başvuru günü |
| ABD_13D | ABD | B | SC 13D / 13D/A (aktivist / büyük ortak) | EDGAR | HAYIR | başvuru günü |
| ABD_BIRLESME | ABD | B | birleşme / ihale teklifi (425, SC TO-T, SC 14D9, DEFM14A, PREM14A) | EDGAR | HAYIR | başvuru günü |
| ABD_GECIKME | ABD | B | NT 10-K / NT 10-Q (rapor gecikmesi) | EDGAR | HAYIR | başvuru günü |
| BIST_RAKIP | BIST | C | rakip bilançosu: sektörün çeyrekteki ilk bilanço günü | KAP FR + sektor_BIST.csv | EVET | rakibin KAP yayın saati kuralı |
| ABD_RAKIP | ABD | C | rakip bilançosu: SIC grubunun çeyrekteki ilk bilanço günü | ABD_BILANCO + k35_sic | EVET | rakibin bilanço günü |
| MAKRO_FOMC | * | C | FOMC karar günü (planlı toplantılar) | federalreserve.gov | EVET | ABD: o gün (14:00 ET); BIST: sonraki işlem günü |
| MAKRO_PPK | * | C | TCMB PPK karar günü | tcmb.gov.tr | EVET | BIST ve ABD: o gün (14:00 TR) |
| MAKRO_EMTIA | * | C | emtia / kur / faiz şoku (|log getiri| >= 3 x kendi 250 gün std'si; GC, SI, CL, HG, ZW, HRC, ALI, USDTRY, TNX) | k36 surucu.pkl | HAYIR | BIST: ertesi işlem günü; ABD: o gün; özellikte ertesi gün |
- A planlı şirket, B beklenmedik şirket, C sektör / makro, D = habersiz kırılım (kontrol grubu; bölüm 8 K1). EDGAR formları: {"ABD_BILANCO_EDGAR": ["10-Q", "10-K", "10-K405", "10-KT", "10-QT"], "ABD_VEKALET": ["DEF 14A"], "ABD_8K": ["8-K"], "ABD_SERMAYE": ["S-1", "S-3", "S-3ASR", "424B1", "424B3", "424B4", "424B5"], "ABD_13D": ["SC 13D", "SC 13D/A", "SCHEDULE 13D", "SCHEDULE 13D/A"], "ABD_BIRLESME": ["425", "SC TO-T", "SC TO-T/A", "SC 14D9", "SC14D9C", "DEFM14A", "PREM14A"], "ABD_GECIKME": ["NT 10-K", "NT 10-Q"]}.
- g0 = olayın ilk etkili işlem günü (takvim tarihinden sonraki ya da aynı ilk işlem günü). Özelliklerde bir olay ancak bilgi günü <= t ise görülür.
- E1 (uzun): koşul günü c = g0 - 21, c'de açık bölge; pencereler [[-20, -11], [-10, -6], [-5, -1], [0, 0], [1, 5], [6, 10], [11, 20]] (ilk genişlemenin bit - g0 farkı). E2 (kısa): c = g0 - 1; pencereler [[0, 0], [1, 5], [6, 10], [11, 20]].
- 'Haber bitirdi' ile 'zaten bitecekti' AYRIMI: beklenen oran = aynı c ayı (makroda aynı yıl), aynı momentum tertili, aynı likidite tertili, c'deki yaşı
  +-2 gün olan, ölçülen aralıkta aynı türden olayı olmayan başka bölgelerden en çok 5 kontrol (en çok 40 aday, tohum 20261112).
  Fark = gözlenen - beklenen (pencere başına), küme bootstrap (hisse; makroda olay günü). Tür başına en çok 50.000 hisse-olay (rastgele, tohumlu; toplam yazılır).
- Olay-bölge eşleme tablosu (çıktı 3): bölgenin [bas, bit + 20] aralığındaki her olay: bas, olay günündeki yaş, olay tarihi, önceden bilinir mi, kategori,
  genişleme tarihi, olay-genişleme işlem günü (bit - g0), yön (Y1), büyüklük ln(C[bit+5]/C[gen_bas-1]), olaydan önce volatilite artışı (ort TRn[g0-5..g0-1] /
  medyan TRn[bas..g0-6] >= 1.5).

## 7. Savunma hattı (S4) ve H1-H5
- Tanım (`vdyt_savunma`, YALNIZ bas..t barları): taban b ∈ ['govde', 'fitil', 'kapanis'] (ANA govde = min(O,C)); tol = 0.5 x medyan TR;
  adaylar b'nin bölge aralığının alt 0.333'ündeki değerleri; temas(p) = |b - p| <= tol sayısı; p* = en çok temas (eşitlikte en düşük);
  hat VAR ⇔ temas >= 3 ve ilk-son temas arası >= 5 bar. Çıktılar: temas, korunma süresi, kapanışla kırılma, fitil ihlali sayısı,
  mesafe / ATR, son testten beri gün, test hacmi / bölge medyan hacmi, yükselen dipler / alçalan tepeler (5'lik blok eğimi).
- H1: hat korunmuş (VAR, kırılma yok) → YUKARI payı, hatsıza göre yüksek (+). H2: kapanışla kırılmış hat → YUKARI payı korunmuşa göre düşük (-).
  H3: yalnız fitil ihlali (kırılma yok) → YUKARI payı kapanışla kırılmışa göre yüksek (+). H4: hatsız karar noktalarında Motor 2 dengeli doğruluğu B1'den yüksek mi.
  H5: Motor 2'de HAT grubunun bağımsız katkısı (M_TAM vs M_TAM - HAT, Brier skill > 0) — süre ve olay özellikleri modelde varken.
- H1-H3 bölge başına son karar noktası, üç taban için ayrı (govde ANA); fark hisse kümeli bootstrap.

## 8. Karşılaştırma grupları (genişleyen bölgeler; sonuç = YUKARI payı ve büyüklük)
K1 haberli (A/B olayı g0 ∈ [gb-5, gb+1]) vs habersiz (A/B yok [gb-10, gb+1] ve makro yok [gb-1, gb]);
K2 bilanço öncesi (bilanço ∈ [gb+1, gb+10]) vs sonrası ([gb-10, gb]); K3 rakip bilançosu öncesi (∈ [gb+1, gb+10]) vs rakip yok (+-10);
K4 planlı makro öncesi (FOMC / PPK ∈ [gb+1, gb+5]) vs yok (+-5); K5 hatlı vs hatsız (son karar noktası); K6 sıkışma karar noktaları vs sıkışma DIŞI ve
aynı mutlak NATR ondalığında günler (sözde yaş, aynı genişleme kuralı; sonuç y10). Kontroller: tabakalama (yıl x momentum tertili x likidite tertili;
K6'da + NATR ondalığı), grup 0 grup 1'in tabaka dağılımına yeniden ağırlıklanır; hisse kümeli bootstrap. Haber etkisinde sektör eşlerinin tepkisi: olay
günü getirisi - pazar getirisi özelliği (o_olay_tepki) ve rakip bilançosu olayı.

## 9. Temel modeller ('basit piyasa kontrolleri')
- Motor 1: T0 = eğitim sıklığı tablosu ['ay'] (süresiz); T1 (ANA TEMEL) = ['yas_kova', 'ay'] (pazar ayrı model olduğu için pazar x yaş kovası x
  takvim ayı); hücre n < 20 ise sondan bir anahtar düşürülür, en sonda genel oran.
- Motor 2: B0 = 0,5; B1 (ANA TEMEL) = eğitimde P(yukarı | pazarın son 60 gün yönü >= 0 / < 0).

## 10. Motorlar, özellikler, walk-forward
- Model: sırt cezalı lojistik regresyon (IRLS, ceza 1.0, en çok 25 tur); özellikler yalnız eğitimden uç kırpma [0.01, 0.99] + z-ölçek, NaN → 0.
- Özellik grupları (Motor 1 ve Motor 2 aynı tam kümeyi kullanır; ablasyon = grubu çıkarıp yeniden eğitme, ana tanım x ana ufuk):
| grup | özellikler |
|---|---|
| SURE | yas_log, yk_20, yk_40, yk_60, yk_90, yk_120 |
| HISSE | hs_oran, hs_yetersiz, hs_gen_pay |
| REJIM | rj_pazar, rj_sektor |
| VOL | v_natr_oran, v_rv_yuzde, v_bbw_yuzde, v_bant, v_rv5_rv20, v_tr_son3 |
| HACIM | h_hacim_oran, h_hacim_son5, h_yukselen_hacim |
| MUM | m_govde_aralik, m_govde_gecmis, m_fitil_ust, m_fitil_alt, m_kapanis_konum |
| FIYAT | f_sma20, f_sma50, f_sma200, f_sma50_egim, f_ret20, f_ret60, f_likidite, f_bolge_konum |
| OLAY | o_bilanco_gun, o_bilanco_yok, o_bilanco_son, o_makro_10, o_olay_son5, o_olay_son20, o_olay_tepki |
| HAT | sv_hat_var, sv_temas, sv_korunma, sv_kirilma, sv_fitil_ihlal, sv_mesafe, sv_son_test, sv_hacim_test, sv_yukselen_dip, sv_alcalan_tepe |
| PAZAR | p_pazar_ret60, p_sektor_ret20 |
- Olay özelliklerinde bilgi kuralı: beklenen bilanço = t'ye kadar BİLİNEN raporlardan (adaylar: son 12 aydaki raporların yıldönümleri ve son rapor + 91 gün;
  t'den sonraki en yakın aday; takvim günü, 0-90 kırpılır, yoksa 90 + 'yok' bayrağı); gerçekleşen
  gelecek bilanço günü kullanılmaz. Planlı makro (FOMC / PPK takvimi önceden yayımlanır) t+1..t+10 içinde mi. B olayları yalnız bilgi günü <= t.
- WALK-FORWARD: her test yılı Y için eğitim = karar günü + ufuk (işlem günü) < 1 Ocak Y olan bütün satırlar (genişleyen pencere, yıllık yeniden eğitim). KEŞİF-WF test yılları [2019, 2020, 2021, 2022, 2023] (aşama 'wf'; veri 2023-12-31'de kesilir: etiket / çözülme tarihi 2024'e taşan
  test satırı ölçülmez). KASA = 2024-01-01 → 2026-08-31, test yılları [2024, 2025, 2026], eğitim aynı kural (ör. 2024 için 2023 sonuna kadar tamamlanan
  etiketler). KASA yalnız `kos --asama kasa` ile ve BİR KEZ açılır (vdyt_kasa_acildi.json; varsa ret). BIST'te OHLC 2015-06'dan → ilk test yılı 2019 (eğitim 2016-2018).
- Birleşik (bilgi): 20 gün içinde {yukarı genişleme, aşağı genişleme, diğer} çok sınıflı Brier; M = p1 x p2 vs T1 x B1.
- Portföy (bilgi): p1(y20) >= eğitimin %90'lık eşiği ve p2 >= 0,5 → ertesi açılış, 20 gün tut, 10 yuva, maliyet sonrası; işlem sayısı, ort / medyan, isabet, en büyük düşüş.

## 11. Değerlendirme ve BAŞARI ÖLÇÜTÜ (karar kuralı)
- Ölçütler: Brier, log loss, Brier skill = 1 - Brier / Brier_temel, log loss skill, kalibrasyon (10 kutu, ECE), kesinlik / duyarlılık (0,5 ve eğitim %90 eşiği),
  dengeli doğruluk (yön), genişlemeye kadar süre (KM), 5 / 10 / 20 / 60 gün getiri, MFE / MAE (20), maliyet sonrası, işlem sayısı, portföy düşüşü (bilgi).
- Belirsizlik: hisse kümeli bootstrap B = 2000, tohum 20261112, %95 yüzdelik aralık; iki yanlı p = erfc(|nokta| / (bootstrap sd x kök 2))
  (normal yaklaşım; yüzdelik p'nin 1/B tabanı BH'de tek güçlü etkiyi bile reddettirmeyeceği için).
- KARAR: BASİTTEN İYİ <=> (WF test yılları toplamında VE KASA'da) Brier skill > 0 VE hisse kümeli bootstrap %95 alt sınırı > 0; BIST ve ABD AYRI; yön motorunda ayrıca dengeli doğruluk farkı ve log loss skill aynı şartla.
  ANA KARAR HÜCRELERİ: Motor 1 = ANA tanım T1, ANA ufuk 10, M_TAM vs T1; Motor 2 = ANA tanım, M_TAM vs B1 (Brier skill, log loss skill, dengeli doğruluk farkı).
  Pazar başına iki motor → 4 ana karar; 'BASİTTEN İYİ' yalnız WF-TOPLAM ve KASA'nın İKİSİNDE şart tutarsa. Diğer tanım / ufuk / model satırları BİLGİ (BH ailesi F1 / F5).
- Etki büyüklüğü (skill, oran farkı) her satırda yazılır.

## 12. Çoklu test ve plasebo
- Aileler (BH q = 0.1, aile içinde): F1_MOTOR1, F1_MOTOR2 (tanım x ufuk x temel), F5_SURE (A-D x temel), F6_KATKI (ablasyon), F2_OLAY (tanım x tür x
  E1 / E2 x pencere), F3_HAT (H1-H5 x taban), F4_KARSILASTIRMA (K1-K6 x sonuç). Hipotez kimliği: '<test>-<pazar>-<tanım>-<ayrıntı>'.
- Bir aile bulgusu 'tutar' ancak WF'de BH ile reddedilir VE KASA'da aynı işaretle %95 aralığı 0'ı dışlarsa.
- P1 rastgele olay günleri (ana tanım, hisse olay türleri, E2; 100 tekrar, tür başına en çok 3.000 olay): tekrar başına BH keşif sayısı → yanlış pozitif oranı.
- P2 rastgele sıkışma bölgeleri (gerçek sürelerle, rastgele başlangıç, sıkışma şartı yok, aynı genişleme kuralı; 5 tekrar): Motor 1 M_TAM vs T1 skill'i
  gerçek bölgelerinkiyle yan yana (sıkışmanın kendine özgü bilgisi var mı).

## 13. Grafik seçim kuralı (sonuç görülmeden)
Gruplar ['BASARILI', 'BASARISIZ', 'HABERLI', 'HABERSIZ', 'HATLI', 'HATSIZ']: BAŞARILI = Motor 1 ana hücre test satırı p >= eğitim %90 eşiği ve y = 1; BAŞARISIZ = aynı eşik ve y = 0; HABERLİ / HABERSİZ = K1 grupları;
HATLI / HATSIZ = genişlemeden önceki son karar noktasında hat var / yok. Pazar x grup başına 5 örnek, numpy default_rng(sha256 tohum: 20261114,
pazar, grup), aday listesi (sembol, tarih) sıralı. Her örnek iki PNG (150 dpi): tam (bas-40 .. bit+30: mum gövde + fitil, ayrı hacim
paneli, sıkışma alanı, savunma hattı, olay günleri, genişleme başlangıcı, yön) ve SİNYAL GÜNÜ (yalnız karar gününe kadarki mumlar). Seçim sonuç görülerek değiştirilmez.

## 14. Tablo şemaları (bilgi tarihi kuralıyla)
**Sıkışma bölgeleri** (`bolge_<pazar>_<kombo>.csv.gz`): sembol str; bas, tespit, bit, gen_bas int (hisse bar indeksi); bit_tur int (1 GENİŞLEME, 2 SÖNME, 3 SANSÜR);
sure int (bit - bas + 1); bas_tarih, tespit_tarih, bit_tarih datetime; uygun bool (tespit günü); Y1, Y2 float (+1 / -1 / 0 / NaN); y1_son datetime; haberli, habersiz,
bilanco_once, bilanco_sonra, rakip_once, rakip_yok, makro_once, makro_yok float (0 / 1; gb'ye göre); buyukluk float; mom_g, liq_g float (gb-1 tertili); yil_g; rj_tespit
float (tespit günü piyasa rejimi); bit_wf, tur_wf, sure_wf (2023 sonu sansürlü). BİLGİ: bölge tespit kapanışında bilinir; bitiş bit kapanışında; yön çözülme günü y1_son.
**Olay eşleme** (`olay_eslesme_<pazar>_<ana>.csv.gz`): sembol, bolge, bas_tarih, yas_olayda int, olay_tarih (g0), tur, kat (A/B/C), onceden bool, genisleme_tarih,
olay_gen_gun int (bit - g0), yon_Y1, buyukluk, on_vol_artis float, on_vol_basladi (0/1), bit_tur str. BİLGİ: olay g0'da, özelliklerde bilgi günü <= t.
**Karar noktaları** (bellek içi; grafik için ince kopya): sembol, bolge, yas, t, tarih, bit, gen_bas, y5 / y10 / y20 (0/1/NaN), son5 / son10 / son20, Y1, Y2, y1_son, yukari,
mom_t, liq_t, natr_d, pazar_yon, yil, ay, yas_kova + bölüm 10 özellikleri (sv_*, svf_*, svk_*, sv_seviye) + bilgi: r5, r10, r20, r60, mfe, mae. BİLGİ: bütün özellikler <= t.
**Tahminler** (`tahmin_m1_<pazar>_<kombo>_y<h>.csv.gz`, `tahmin_m2_<pazar>_<kombo>.csv.gz`): satir, yil (test yılı), p_<model> (A_ORTAK, B_HISSE, C_REJIM, D_ADAPTIF, M_TAM,
M_EKSI_<grup>, T0, T1 / B0, B1), esik90_M_TAM, sembol, tarih, y. Eğitim yalnız son_h < test yılı başı.
**Hipotez** (`vdyt_sonuc_<aşama>.json` 'hipotez'): aile, id, nokta, alt, ust, p, bh_ret, ana, beklenen_isaret, n1, n0.

## 15. Çıktılar (Cemal'in 13. maddesi; Drive 'MyDrive/COLAB_VERILER/OUTPUT/VDYT' yüklemesini ana oturum yapar)
1 VDYT_VERI_ENVANTERI.md; 2 bolge_*.csv.gz (+ VDYT_KAPSAM.md); 3 olay_eslesme_*.csv.gz; 4 süre karşılaştırma (VDYT_RAPOR.md §Süre, sure_*.csv); 5 haberli-habersiz
(§Karşılaştırma K1, §Olay E1 / E2); 6 genişleme tahmin raporu (§Motor 1); 7 yön tahmin raporu (§Motor 2); 8 savunma hattı raporu (§H1-H5); 9 BIST ve ABD ayrı (her bölüm
pazar ayrı); 10 grafik/ (PNG); 11 VDYT_HATA_VE_EKSIK.md + VDYT_EKSIKLER.md; 12 vdyt_parametre_kaydi.json. Raporlar arastirma_cikti/vdyt/, büyük tablolar /tmp/vdyt/<aşama>/.

## 16. Yanlılık beyanı
- Yaşayan evren: V_BIST ve k60_fiyat bugün işlem görenler; batan / kotasyondan çıkan yok (BIST_K62 kontrolü yalnız kapanış tanımlarında). Aşağı yönlü genişlemeler
  ve sıkışmadan sonra batanlar eksik sayılır → yön sonuçları YUKARI lehine yanlı olabilir.
- Yeniden sunum: VDYT temel (bilanço) DEĞERİ kullanmaz; yalnız olay günü. Frames / yeniden sunum sorunu yok.
- KAP saati: yayın saati var; seans bitişi 18:00 varsayımı (yıllara göre 17:30-18:10 farklı) → kenar olaylarda g0 bir gün kayabilir.
- EDGAR: yalnız başvuru günü (saat yok; özellikte ertesi işlem günü); 8-K madde kodu yok; CIK → bugünkü kod (eski kodlar eşlenmez).
- ABD bilanço 2010 → 2022-11: 10-Q / 10-K başvuru günü VEKİL; Nasdaq saatleri %99 belirsiz.
- Makro takvimde yalnız TARİH (içerik, beklenti, sürpriz yok); CPI / istihdam / TÜİK EKSİK.
- BIST KAP özel durum açıklamaları EKSİK → BIST 'habersiz' = kayıtlı veri setlerinde olay yok (gerçek habersizlik değil).
- Hacim ve mum değişkenleri Çöl Yolu'nda kapalı konudur; burada ayrı motor (bölüm 0).

## 17. SAPMA / BOŞLUK listesi (ana oturumun tasarım kararlarına göre)
1. Walk-forward test yılları: KEŞİF-WF 2019-2023 + KASA 2024-2026 (tasarımdaki '2019-2026' ikiye bölündü; KASA bir kez açılır). KASA yılları da yıllık yeniden eğitilir.
2. Temel T1'de 'ay' = takvim ayı (1-12; mevsimsellik), çünkü aynı takvim ayının oranı test anında bilinemez. Pazar ayrı model olduğundan anahtarda yok.
3. Karar noktası: sıkışma başına çok nokta (yaş 10-120) + hisse kümeli bootstrap; savunma / karşılaştırma testleri bölge başına tek nokta.
4. Motor 2 yalnız 20 gün içinde genişleyen satırlarda eğitilir / sınanır ('genişlerse yönü'); birleşik üç sınıf bilgi.
5. Makro: FOMC (federalreserve.gov) + PPK (tcmb.gov.tr) tarih listesi; CPI / istihdam / TÜİK EKSİK. Emtia: surucu.pkl (2015+), şok = |log getiri| >= 3 x geçmiş std.
6. Sektör haberi VERİ YOK; yerine 'rakip bilançosu' (sektörün çeyrekteki ilk bilanço günü).
7. ABD delist: veri yok (k34 de yaşayan). BIST delist: yalnız kapanış (BIST_K62).
8. Olay analizi tür başına en çok 50.000 hisse-olay (tohumlu rastgele; makro türleri çok büyük); plasebo P1 tür başına 3.000.
9. 'Süreye bağlı Markov' ayrı kurulmadı (kesikli yaş hazard'ı = süreye bağlı geçiş; bölüm 5).
10. BOŞLUK: BIST'te 2015 öncesi OHLC yok → BIST WF eğitimi 2016'dan; T1 / savunma hattı / mum ölçüleri BIST'te yalnız yaşayanlarla.
11. BOŞLUK: KAP özel durum açıklamaları indirilmedi (iş tanımı: gereksiz indirme yok); ana oturum isterse Faz 2 öncesi indirme kararı + SAPMA.
12. Grafikler matplotlib ister (Colab'da var; bu konteynerde yoksa `grafik` komutu durur ve nedeni yazar).
13. p değerleri bootstrap standart hatasıyla normal yaklaşım (bölüm 11); yüzdelik bootstrap p'sinin 1/B tabanı büyük ailelerde BH'yi işlemez kılardı.
14. ABD_SERMAYE'den 424B2 çıkarıldı (bankaların yapılandırılmış ürün / borç senedi akışı; pay arzı değil). FOMC güncel sayfasındaki '*' = projeksiyonlu
    toplantı (planlı); 'unscheduled' / 'cancelled' planlı değil; 'notation vote' toplantı sayılmaz. PPK 2009-2014 sayfaları alınamadı → EKSİK (BIST OHLC 2015-06'dan).
15. KOD_SHA256 kuralı: VDYT.py'nin her değişikliği (yorum dahil) `kos`u durdurur; ön kayıt sonrası düzeltme bu listeye tarihli SAPMA + yeni KOD_SHA256 ile işlenir.
16. Veri sha256'ları bu konteynerdeki /tmp dosyalarına bağlıdır (k60_fiyat Yahoo'dan yeniden inerse sha değişir → ret). Faz 2 aynı veriyle koşmalı; veri
    yenilenirse SAPMA + yeni veri satırları + kapsam yeniden.

## 18. Veri sha256 (ön kayıt anı; `kos` yeniden hesaplar, farklıysa ret)
- G.pkl: sha256 cdde36f074df0a435274ffbb19ed4734b0291964db7e8093acd2a9e623c9fc3c (1 dosya)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- company_tickers.json: sha256 6f9cc4500a98fb4c048328d7df392ed48c092613ec0c3e93cd6c7a3502886074 (1 dosya)
- edgar_master: sha256 57d5329d3603d361e7d81831878dcbe05777a7771d0f845b76a77e21fa2edc77 (71 dosya)
- k35_sic.csv: sha256 1ac089db38678ef6d62b0e22562822f21d90fce6d96845dd4ea8d52e98ec52c9 (1 dosya)
- k58_yahoo: sha256 7059054137b9a6a6e98d16e5dbef012f718df33197c790a417e7ab0c577a4e03 (2 dosya)
- k60_fiyat: sha256 21435ad5b907eeb2dc4e8985e31c602900b2a010b7242c89331210e550dac374 (4757 dosya)
- k62_fiyat: sha256 bf3c29260b2b6d10794fb9338bb74253b291ef6c877c4d53d14f8a7f876bf636 (972 dosya)
- k62_kap: sha256 82cdbb0845835b464b8ed721d6f52afa22e9c682ec848478fc85c5fba7945ab1 (451 dosya)
- kap_iceriden: sha256 14cc588b8499891aeeb249ec20d2e9fa6ec2a787a6b2383b6a24e7cd5c7781a0 (3 dosya)
- liste_abd.csv.gz: sha256 87539954817d5d551623eeed04fa410844646539093a4e841a7755a2cfc674cb (1 dosya)
- sektor_BIST.csv: sha256 0f933f73a6042c95d42275e0b9e1289221cc4f3b4b6d1df81987fcab14fd16d4 (1 dosya)
- surucu.pkl: sha256 c74304c1f921d7f087023559480bc217004e47ddb53684148c992d5d1b2a35bd (1 dosya)
- vdyt_makro_takvim.json: sha256 27a1f678211bedbc083ab5abd9f59b8cbdd7dba99cd41609bee53387828b3900 (1 dosya)

## 19. Kapsam (yalnız SAYI; `python -I VDYT.py kapsam`)
| pazar | ana tanım | bölge (uygun) | medyan süre | karar noktası |
|---|---|---|---|---|
| ABD | T1 | 15.974 | 19 | 23.968 |
| ABD | T2 | 54.161 | 23 | 97.441 |
| ABD | T3 | 59.920 | 20 | 91.262 |
| ABD | T4 | 38.882 | 19 | 58.209 |
| ABD | T5 | 23.794 | 19 | 34.883 |
| BIST | T1 | 3.425 | 18 | 5.000 |
| BIST | T2 | 6.511 | 21 | 10.729 |
| BIST | T3 | 7.061 | 19 | 10.379 |
| BIST | T4 | 5.168 | 19 | 7.554 |
| BIST | T5 | 3.646 | 18 | 5.276 |
| BIST_K62 | T2 | 11.196 | 20 | 18.628 |
| BIST_K62 | T3 | 12.069 | 19 | 17.997 |
| BIST_K62 | T4 | 9.959 | 19 | 15.279 |

Ayrıntı (dönem, duyarlılık kombinasyonları, olay eşleşmeleri): arastirma_cikti/vdyt/VDYT_KAPSAM.md (2026-11-12 06:15:37 UTC).

## 20. Faz 2 komutları
1. (ana oturum) bu dosyayı ve VDYT.py'yi denetler, git'e işler.
2. `python -I VDYT.py kos --asama wf` → KEŞİF-WF ölçümü + rapor (mühür, kod, veri sha256 ve git doğrulanır; yoksa ret).
3. `python -I VDYT.py kos --asama kasa` → KASA bir kez açılır, final karar tablosu.
4. `python VDYT.py grafik --asama wf` (ve kasa), `python VDYT.py rapor --asama kasa`.

## 21. Değişmezlik
VDYT_ESIK, VDYT_OLAY_TUR, VDYT_EDGAR_FORM, VDYT_OZELLIK, VDYT_SURE_MODEL değişirse ESIK_SHA256 değişir; VDYT.py değişirse KOD_SHA256 tutmaz; veri değişirse veri
sha256 tutmaz → `kos` durur.
