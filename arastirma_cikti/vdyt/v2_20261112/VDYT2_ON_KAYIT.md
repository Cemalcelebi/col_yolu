# VDYT2 ÖN KAYIT — Volatilite Denge ve Yön Tahmini, SÜRÜM 2 (v2_20261112) — ölçümden ÖNCE

Yazım zamanı: 2026-11-12 09:45:49 UTC (2026-11-12 12:45 TR)
ESIK_SHA256: 3051e5b8ddd99c7c42e36f106bdaede734e8dac5ed6588029c5d50bc2274f5a8
KOD_SHA256: e33b2fd1c611e32930e8e8af29b9a4a9e86607a1df303e0fae8d9e94d0a30741
VDYT_KOD_SHA256: 10ead8062c2c8ec25984a23b68b299cec4d8a7cfd144ad22e542e867d40c932d
Sürüm: VDYT2 v2.0 (v2_20261112): Faz 1 (ön kayıt, kod + sentetik test, yalnız sayım); ölçüm Faz 2'de, ön kayıt git'e işlendikten sonra

Bu dosya, VDYT2.py ve VDYT.py git'e işlenmeden; eşik mührü, iki kod sha256'sı ve veri sha256'ları tutmadan `kos` ve `canli` ÇALIŞMAZ (Vdyt2Hata, çıkış 1).
Sonuç görüldükten sonra tanım, eşik, pencere, ufuk, kontrol, model, temel ya da karar kuralı değişmez; değişirse bu dosyada tarihli SAPMA yazılır, mühür / kod
satırı yeniden işlenir. VDYT sürüm 1 kayıtları, kodu (VDYT.py), ön kaydı, çıktıları ve VDYT_GRAFIK.py DEĞİŞMEZ; v2 ayrı dosya ve ayrı klasördür.

## 0. Hedef (Cemal, aynen) ve sınır
'Sert düşüş veya önceki hareket -> küçük mumların oluşturduğu uzun sessiz bölge -> büyük mumlarla başlayan volatilite genişlemesi.' Bu sessiz bölgeyi BÜYÜK
HAREKET BAŞLAMADAN ÖNCE tespit et; büyük hareketin ne zaman başlayabileceğini, yönünü ve hangi özelliklerin doğru tahmin ihtimalini artırdığını belirle. Amaç
geçmiş grafikte güzel görünen bölgeleri bulmak değil, gerçek zamanda henüz büyük hareket olmamışken yakalamak.
- ÜÇ BAŞARI AYRI AYRI kanıtlanır (bölüm 7): (1) bölgeyi önceden bulmak, (2) genişlemeyi önceden tahmin etmek, (3) yönü önceden tahmin etmek; basit piyasa
  kontrollerinden daha iyi. Biri başarısızsa başarılı gibi sunulmaz. Sonuç olumsuz olabilir; başarısız değişken / test rapordan silinmez.
- Çöl Yolu kuralları, IZ_KARNE kararları, geçmiş kayıtlar (VDYT v1 ve Ç161 dahil) DEĞİŞMEZ. Hacim / mum şekli değişkenleri (Çöl Yolu'nda kapalı konu) yalnız bu
  motorda ölçülür; sonuç Çöl Yolu'na 'yaz' kararı olmadan taşınmaz. VDYT2 sonucu doğrulanmış sinyal değildir; yüksek olasılık alım sinyali değildir.
- Ücretli veri / abonelik (Alpha Vantage, Tiingo, IBorrowDesk) YOK; SEC'e istek yok; yeni büyük indirme yok.

## 1. VDYT v1 dersleri ve v2'deki zorunlu karşılığı
- D1 (genişleme motoru mekanikti): (a) GEÇERLİ KARAR GÜNÜ (bölüm 5.2): t ve önceki 2 günün HER BİRİNİN gerçek aralığı <= 2.0 x bölge
  referansı ve bölge t kapanışında hâlâ açık; etiket YALNIZ t'den SONRA başlayan büyük hareketi sayar (g > t). (b) Aynı model sıkışma DIŞI ve aynı mutlak
  oynaklık ondalığındaki günlerde (DIŞARI) ve rastgele bölgelerde (RASTGELE, aynı süre dağılımı) koşulur; 'bölgenin kendine özgü bilgisi' ancak bu iki
  kontrolden iyiyse vardır (başarı 2b).
- D2 (v1'de hazard yaşla AZALDI): 'olgunlaşma' VARSAYILMAZ; OLG testi (bölüm 9) ve yaş hazard'ı raporlanır; SÜRE grubu modelde serbest işaretli.
- D3 (v1 yön başarısı büyük ölçüde konumdan): yön KARAR temeli B1 (piyasanın son 60 gün yönü); B2 = yalnız KONUM grubu (mekanik temel; BİLGİ); konum-dışı
  model (M_KONUMSUZ) BİLGİ; yön ayrıca işlem sonucuyla (maliyet sonrası getiri) raporlanır.
- D4 (bilanço dışı olay bulgularında plasebo yanlış pozitifi yüksekti): olay bulgusu ancak WF'de BH ile reddedilir, KASA'da aynı işaretle %95 aralığı 0'ı
  dışlar VE WF |fark| aynı tür x pencerenin plasebo |fark| dağılımının %95 yüzdeliğini aşarsa SAYILIR (bölüm 11).
- D5: VDYT_GRAFIK.py ve arastirma_cikti/vdyt/paket'e dokunulmaz; v2 grafikleri kendi paketi + yalnız paketten çizen `ciz` ile (bölüm 14).

## 2. Veri ve dönem (VDYT v1 ile aynı kaynaklar; VDYT.py yükleyicileri içe aktarılır, değiştirilmez)
- BIST = V_BIST (OHLCV, 2015-06+; yaşayan 581). ABD = k60_fiyat (Yahoo OHLCV 2010+; 4.678 hisse; yaşayan). BIST_K62 = K62 kapanış 2008+ (kotasyondan
  çıkanlar dahil; açılış / yüksek / düşük YOK) YALNIZ yanlılık kontrolü: tanım G2K (yalnız kapanış bandı), büyük mumda gövde şartı yok, yalnız başarı (1)
  ve çıkmış / yaşayan ayrımı (BİLGİ).
- Bar temizliği, uygunluk (BIST: >= 252 bar, 20 gün medyan işlem değeri kesitte %20 üstü; ABD: EQUITY, >= 252 bar, ekrandaki fiyat >= 2 $, 20 gün medyan işlem
  değeri >= 1 milyon $), kopukluk (> 15 takvim günü), endeks (XU100 / SPY), sektör, NATR ondalığı, momentum / likidite tertilleri: VDYT v1 ile aynı
  (V1.vdyt_panel). Karar satırı yalnız uygun günde (t).
- Olaylar: KAP Finansal Rapor 2009+ (BIST bilanço; yayın saati kuralı), KAP içeriden işlem 2022-07+, KAP fon girişleri 2023+, K62 hak kullanım / sermaye,
  EDGAR form grupları (8-K, sermaye, 13D, birleşme, gecikme, vekâlet), FOMC / PPK (planlı), emtia şokları, rakip bilançosu. ABD bilanço günü: Yahoo takvimi
  (/tmp/k67_yahoo/takvim; 1.410 hisse, 1998+; K67'de Nasdaq ile %97 uyumlu) BİRİNCİL: takvimi olan hissede v1 bilanço satırları Yahoo ile değişir (saat
  >= 16 ET -> sonraki işlem günü; diğerleri ve 'saat yok' -> o gün); takvimi olmayanda v1 (Nasdaq 2022-12+, öncesi 10-Q / 10-K vekili). Gelecek tarihli
  takvim satırları atılır; özellikte beklenen bilanço günü YALNIZ t'ye kadar bilinen bilançolardan (v1 kuralı) türetilir.
- Fon krizi kesiği 2026-08-31: test fiyatları burada kesilir; etiketi kesiği aşan satır ölçülmez. Canlı çıktı (bölüm 13) son veri gününde, 'CANLI, test dışı'.
- Maliyet (tek yön; yalnız getiri bilgisinde): BIST 30 bp, ABD 10 bp.

## 3. Ön koşul (önceki hareket) alternatifleri — bölge başlangıcı bas'taki bilgiyle
- düşüş120 = C[bas] / max(C[bas-120 .. bas-1]) - 1; yükseliş120 = C[bas] / min(aynı pencere) - 1; geçmiş < 120 bar ise tanımsız (P1 = P2 = yok).
- P0 = koşul yok; P1 (ANA; 'sert düşüş') = düşüş120 <= -0.30; P2 ('önceki büyük hareket') = P1 YA DA yükseliş120 >= +0.30 (|değişim| >= %30).
- Bütün ön koşullar raporlanır. Modeller P0 satırlarıyla eğitilir (ön koşul ölçüleri ONCEKI grubu olarak modelde); değerlendirme ve TEMELLER her alt
  kümede o alt kümenin kendi eğitim satırlarıyla kurulur (temel alt küme bilgisinden yoksun kalmaz). Kontrol satırlarında da aynı ön koşul (sözde bas'a göre).

## 4. Sessiz bölge ('insan gözü') tanımları — günlük DURUM, yalnız [t-L+1, t] (L = 10) ve öncesi
- ATRref(t) = ortalama TR[t-L-249 .. t-L] (sessiz pencereden ÖNCEKİ 250 bar; en az 200); TR = max(H-L, |H-C[-1]|, |L-C[-1]|).
- G1 küçük mum bileşiği: medyan(H-L) / ATRref <= 0.6 (alternatifler 0.5, 0.7) VE medyan |C-O| / ATRref <= 0.3 VE
  maks(H-L) / ATRref <= 1.5 (pencerede büyük mum yok). Ölçü olarak (şart değil): medyan |gövde| / (H-L), üst / alt fitil / ATRref, doji payı
  (|C-O| <= 0.1 x (H-L)).
- G2 dar bant: kapanış bandı KB = (maks C - min C) / ort C (son L) ve gövde bandı GB = (maks max(O,C) - min min(O,C)) / ort C; her biri kendi geçmişinin
  medyanına bölünür (aynı ölçünün [t-L-249, t-L] değerleri; en az 200); İKİSİ de <= 0.5 (alternatifler 0.4, 0.6).
- G3 yaklaşan tepe-dip (kanal daralması): son L günün tepelerinin (H) en küçük kareler eğimi / ATRref <= 0.0 VE diplerinin (L) eğimi / ATRref >= 0.0.
- G4 savunulan destek: VDYT v1 savunma hattı (V1.vdyt_savunma ile aynı kural, kayan pencere [t-19, t]; tol = 0.5 x medyan TR; adaylar aralığın alt
  0.333'ü; hat VAR <=> temas >= 3 ve ilk-son temas arası >= 5 bar) VE ilk temastan sonra kapanışla kırılma YOK ('savunulan').
  Taban: gövde dibi min(O,C) (ANA), fitil dibi (L), kapanış (C) AYRI.
- G5 (ANA) = G1 VE G2 VE (G3 YA DA G4[gövde]): 'küçük mumlar + dar bant + tekrar test edilen dipler / ortak destek'. Aile: G5f (G4 fitil), G5k (G4 kapanış).
  Alternatif eşikler: G1_e0.5, G1_e0.7 (G1 tek başına), G5_g0.4, G5_g0.6 (G2 eşiği). Karşılaştırma: VDYT v1 T1-T5 durumları (v1 eşikleriyle). Pencerede
  kopukluk varsa durum yanlış.
- BÖLGE KURALI: G tanımlarında durum 1 gün doğru (durum zaten son L günün ölçüsü), v1 T tanımlarında 10 gün kesintisiz doğru VE önceki bölgenin bitişinden en az
  L gün sonra -> tespit = o gün, bas = tespit - L + 1 (yaş = t - bas + 1; tespitte 10). Bitiş (tespitten SONRA, gerçek zamanda bilinen ilk olay): BÜYÜK MUM
  (bölüm 5.1, ref başlangıcı bas) | SÖNME: DEVAM durumu 5 gün üst üste yanlış | SANSÜR: veri sonu / kopukluk. DEVAM durumu G5 ailesinde
  çekirdek G1 VE G2'dir (küçük mum + dar bant sürdükçe bölge açık; tepe-dip / destek şartı G3 ∨ G4 AÇILIŞ onayıdır, her gün aranmaz); diğer tanımlarda açılış
  durumunun kendisi. Büyük mumla biten bölgenin ONAYI (bölüm 5.1) süre analizinde olay / rakip olay ayrımıdır.

| tanım | rol | açılış durumu | devam durumu | açılış için kesintisiz gün |
|---|---|---|---|---|
| G5 | ANA | G5 | G12 | 1 |
| G5f | AILE | G5f | G12 | 1 |
| G5k | AILE | G5k | G12 | 1 |
| G1 | ALT | G1 | G1 | 1 |
| G2 | ALT | G2 | G2 | 1 |
| G3 | ALT | G3 | G3 | 1 |
| G4 | ALT | G4 | G4 | 1 |
| G1_e0.5 | ALT | G1_e1 | G1_e1 | 1 |
| G1_e0.7 | ALT | G1_e2 | G1_e2 | 1 |
| G5_g0.4 | ALT | G5_b1 | G12_b1 | 1 |
| G5_g0.6 | ALT | G5_b2 | G12_b2 | 1 |
| T1 | ALT | V1:T1 | V1:T1 | 10 |
| T2 | ALT | V1:T2 | V1:T2 | 10 |
| T3 | ALT | V1:T3 | V1:T3 | 10 |
| T4 | ALT | V1:T4 | V1:T4 | 10 |
| T5 | ALT | V1:T5 | V1:T5 | 10 |
| G2K (BIST_K62) | K62 | G2 (kapanış) | G2 (kapanış) | 1 |
Roller: ANA = bütün analizler; AILE = başarı (1), (2) ve (3) M_TAM (BİLGİ); ALT = başarı (1) + duyarlılık + sayım (BİLGİ); K62 = yanlılık kontrolü.

## 5. Büyük hareket, geçerli karar günü, etiket
### 5.1 Büyük mum ve BH1 (etiket)
- Büyük mum (gün i; yalnız i ve öncesi): TR_i >= k_b x medyan TR[ref] VE |C_i - O_i| >= m x medyan |C - O|[ref]; ref = [max(bas, i-60), i-1], en az
  8 gün; k_b = 2.5, m = 3.0; TR referansı en az 0.001 x C[i-1], gövde referansı en az 0.1 x TR referansı (işlemsiz /
  düz bar tabanı). Kapanış kipinde (K62) gövde şartı yok.
- ONAY: [i, i+9] içinde ilk kapanış > Hi -> YUKARI, < Lo -> AŞAĞI (Lo / Hi = ref penceresinin kapanış aralığı); çıkış yoksa SAHTE (onaysız), veri / kopukluk
  yetmezse BELİRSİZ.
- BH1 (ANA etiket) başlangıcı g = t'den SONRAKİ ilk ONAYLI büyük mum (g > t; ref başlangıcı bölgenin bas'ı; bölge g-1'e kadar sürmüş sayılır; onaysız büyük
  mumlar atlanır, sonraki onaylı mum aranır). y_h = 1 <=> g <= t + h; y_h = 0 <=> (t, t+h] içinde onaylı büyük mum yok; ölçülmez (NaN) <=> t + h + 9 veri
  dışında ya da (t, t+h+9] içinde kopukluk. Ufuklar [5, 10, 20] (ANA 10; başarı (1) için 20). Etiket tamamlanma günü son_h = t + h + 9.
  bar (WF eğitim kuralı bunu kullanır). Yön = çıkılan kenar; büyüklük = ln(C[g+9] / C[g-1]), ln(C[g+19] / C[g-1]), ATR cinsinden (C[g+9] - C[g-1]) / ATR14[g-1].
- BH2 (v1 genişleme tanımı) v2'de koşulmaz: v1 sonuçları zaten kayıtlı; karşılaştırma v1 T1-T5 durumlarının v2 etiketiyle koşulmasıyla yapılır (SAPMA 1).
### 5.2 Geçerli karar günü (D1a) ve karar yaşları
- Karar yaşları [10, 15, 20, 30, 45, 60, 90] (t = bas + yaş - 1); satır ancak: t >= tespit, bölge t kapanışında açık (t < bitiş), t uygun VE GEÇERLİ: TR[t-2..t]'nin her
  biri <= 2.0 x medyan TR[max(bas, t-59), t] (taban 0.001 x C_t). Geçersiz yaş atlanır (kaydırılmaz). Bölge başına çok satır ->
  bütün belirsizlikler HİSSE kümeli bootstrap.
### 5.3 Bölgeden bağımsız büyük hareket (BHU; duyarlılık / kaçırılan için)
- g'de TR >= 2.5 x medyan TR[g-60, g-1] (en az 40) VE |gövde| >= 3.0 x medyan |gövde| (aynı tabanlar) VE [g, g+9] içinde
  [g-20, g-1] kapanış aralığından çıkış; BAŞLANGIÇ = önceki 20 barda tutulmuş BHU yok; g-1 uygun.

## 6. Kontroller (D1b; 'basit piyasa kontrolleri')
- DIŞARI (kontrol a): aynı hisse, aynı yıl, aynı mutlak oynaklık ondalığı (NATR14'ün o günkü uygun kesitteki ondalığı); gün t tanımın HİÇBİR bölgesinin
  [bas, bitiş] aralığında değil, uygun, bar >= 260. Gerçek satırların her (yıl, ondalık) hücresinden hücredeki gerçek satır sayısının
  ANA 5 / AILE 2 / ALT 2 / K62 2 katı gün (yerine koymadan, tohum sha256(sembol, tanım, 'DISARI', 20261115)); sözde yaş = o hissenin gerçek yaşlarından çekilir, sözde bas = t - yaş + 1;
  AYNI geçerlilik (D1a), etiket, ön koşul ve özellikler. Karşılaştırmada tabaka = (hisse, yıl, NATR ondalığı); kontrol, gerçeğin tabaka dağılımına yeniden
  ağırlıklanır; kontrolsüz tabakadaki gerçek satır düşer (sayısı raporda).
- RASTGELE (kontrol b): hisse başına uygun gerçek bölge sayısının 2 katı bölge; süre = o hissenin gerçek bölge sürelerinden (yerine koyarak), başlangıç
  tekdüze [260, n-1-süre-30]; sıkışma şartı YOK; aynı karar yaşları, geçerlilik, etiket, ön koşul ve özellikler. Tabaka = (yıl, yaş).
- Aynı model (bölüm 8) kontrol satırlarında kendi WF'siyle koşulur (ANA; D1b). Tam satır (etiket + özellik + getiri): ANA gerçek ve kontrol satırları, AILE
  gerçek satırları (bütün yıllar; model eğitimi için). Hafif satır (etiket + tabaka; yalnız başarı 1): ALT / K62 satırları ve AILE / ALT / K62 kontrolleri, YALNIZ
  2019-01-01'den sonraki karar günleri (başarı 1 yalnız WF test yılları ve KASA'da ölçülür; önceki yıllar kullanılmaz). Tabaka ve örnekleme bütün yıllardan.

## 7. ÜÇ BAŞARI — KARAR KURALI (önceden; WF test yılları 2019-2023 toplamında VE KASA'da; BIST ve ABD AYRI; hisse kümeli bootstrap B = 2000, tohum 20261112, %95)
ANA hücre: tanım G5, ön koşul P1. P0 ve P2 alt kümeleri aynı kuralla BİLGİ olarak hesaplanır (canlı sınıf kapısında kullanılır, bölüm 13).
- (1) BÖLGEYİ ÖNCEDEN BULMAK = BAŞARILI <=> geçerli karar günlerinin 20 gün içinde BH1'e dönüşme oranı, DIŞARI'nın (tabakalı) oranından VE RASTGELE'nin
  (tabakalı) oranından yüksek: İKİSİNDE oran farkı > 0 ve %95 alt sınır > 0 (oran > 1 bunu izler), WF'de VE KASA'da. Ayrıca (BİLGİ): duyarlılık = dönemdeki
  BHU'ların g-1 gününde (en az 1 işlem günü önce) açık bölgesi olanların payı; kaçırılan büyük hareket sayısı; uyarı süresi (g - tespit, işlem günü; q25 /
  medyan / q75); kapsama (uygun hisse-günlerinin açık bölgedeki payı) ve kaldıraç = duyarlılık / kapsama; yanlış bölge payı (bölgenin ilk geçerli satırında
  y20 = 0 olanların payı).
- (2) GENİŞLEMEYİ ÖNCEDEN TAHMİN = BAŞARILI <=> (2a) M_TAM vs T1 (ufuk 10) Brier skill = 1 - Brier / Brier_T1 > 0 ve %95 alt > 0 VE (2b, D1b) bölgeye özgü:
  skill(gerçek) - skill(DIŞARI) > 0 ve alt > 0 VE skill(gerçek) - skill(RASTGELE) > 0 ve alt > 0 (ortak hisse kümeli bootstrap); WF'de VE KASA'da. 5 / 20 ufuk,
  T0, süre modelleri, tek grup modelleri, ablasyon BİLGİ.
- (3) YÖNÜ ÖNCEDEN TAHMİN = BAŞARILI <=> büyük harekete dönüşen (y20 = 1, yön ±1) geçerli karar günlerinde P(YUKARI) için M_TAM vs B1: Brier skill > 0 ve alt > 0
  VE dengeli doğruluk farkı (eşik 0,5) > 0 ve alt > 0; WF'de VE KASA'da. B0, B2 (yalnız KONUM; mekanik), M_KONUMSUZ vs B1, işlem sonucu, birleşik üç sınıf
  BİLGİ.
- Karar etiketleri: BAŞARILI / BAŞARISIZ / VERİ YOK (n < 30 ya da tek sınıf) / KASA AÇILMADI. (2) yalnız (2a) VE (2b) ile BAŞARILI; (2a) tutup (2b) tutmazsa
  'genişleme tahmini sıkışmaya özgü değil' diye yazılır.

## 8. Model, özellikler, temeller, walk-forward
- Tek model ailesi: sırt cezalı lojistik (V1.vdyt_lojistik; IRLS, ceza 1.0, en çok 25 tur); özellikler yalnız eğitimden uç kırpma
  [0.01, 0.99] + z-ölçek, NaN -> 0; eğitim < 200 satır ise yıl atlanır. Karmaşık model yok.
- Özellik grupları (hepsi t ve öncesi; olaylarda bilgi günü <= t):

| grup | özellikler |
|---|---|
| SURE | yas_log, yk_15, yk_20, yk_30, yk_45, yk_60, yk_90 |
| HISSE | hs_oran, hs_yetersiz, hs_bh_pay |
| REJIM | rj_pazar, rj_sektor |
| ONCEKI | on_dusus120, on_yukselis120, on_p1, on_p2 |
| MUM | m_aralik_atr, m_govde_atr, m_govde_aralik, m_fitil_ust_atr, m_fitil_alt_atr, m_doji_pay, m_maks_aralik |
| BANT | b_kapanis_bant, b_govde_bant, b_bolge_bant_atr, b_egim_tepe, b_egim_dip |
| VOL | v_natr_oran, v_rv_yuzde, v_bbw_yuzde, v_rv5_rv20, v_tr_son3 |
| HACIM | h_hacim_oran, h_hacim_son5, h_yukselen_hacim, h_bolge_hacim |
| HAT | sv_hat_var, sv_temas, sv_korunma, sv_kirilma, sv_fitil_ihlal, sv_son_test, sv_hacim_test, sv_yukselen_dip, sv_alcalan_tepe, sv_kapanis_ustu, svf_hat_var, svf_kirilma, svk_hat_var, svk_kirilma |
| KONUM | k_bolge_konum, k_ust_mesafe_atr, k_alt_mesafe_atr, sv_mesafe |
| EMA | e_ema20, e_ema50, e_ema200, e_sma50, e_sma200, e_sma50_egim, e_ema20_50 |
| FIYAT | f_ret20, f_ret60, f_likidite |
| OLAY | o_bilanco_gun, o_bilanco_yok, o_bilanco_son, o_bilanco_bolgede, o_makro_10, o_olay_son5, o_olay_son20, o_olay_tepki |
| PAZAR | p_pazar_ret60, p_pazar_ret20, p_sektor_ret20 |

- Genişleme modelleri (M_TAM bütün gruplar; ablasyon M_EKSI_<grup>; tek grup M_TEK_<grup>; süre yaklaşımları):

| model | gruplar |
|---|---|
| M_TAM | SURE + HISSE + REJIM + ONCEKI + MUM + BANT + VOL + HACIM + HAT + KONUM + EMA + FIYAT + OLAY + PAZAR |
| A_ORTAK | SURE |
| B_HISSE | SURE + HISSE |
| C_REJIM | SURE + REJIM |
| D_ADAPTIF | SURE + HISSE + REJIM |

- Yön modelleri:

| model | gruplar |
|---|---|
| M_TAM | SURE + HISSE + REJIM + ONCEKI + MUM + BANT + VOL + HACIM + HAT + KONUM + EMA + FIYAT + OLAY + PAZAR |
| M_KONUMSUZ | SURE + HISSE + REJIM + ONCEKI + MUM + BANT + VOL + HACIM + HAT + EMA + FIYAT + OLAY + PAZAR |
| B2_KONUM | KONUM |

- Temeller: genişleme T0 = eğitim sıklığı ['ay'], T1 (KARAR) = ['yas_kova', 'ay'] (pazar ayrı; yaş kovası x takvim ayı; hücre n < 20 ise sondan bir
  anahtar düşer); yön B0 = 0.5, B1 (KARAR) = eğitimde P(yukarı | piyasanın son 60 gün getirisi >= 0 / < 0), B2 = M yalnız KONUM (BİLGİ).
  Yaş kovaları [[10, 14], [15, 19], [20, 29], [30, 44], [45, 59], [60, 89], [90, 100000]].
- WALK-FORWARD: her test yılı Y için eğitim = etiketi Y başından ÖNCE tamamlanmış satırlar (t + h + 9. bar < 1 Ocak Y); genişleyen pencere, yıllık yeniden eğitim. WF test yılları [2019, 2020, 2021, 2022, 2023] (aşama 'wf'; etiketi 2023-12-31'i aşan satır ölçülmez). KASA = 2024-01-01 -> 2026-08-31,
  test yılları [2024, 2025, 2026], aynı eğitim kuralı; YALNIZ `kos --asama kasa` ile ve BİR KEZ açılır (vdyt2_kasa_acildi.json; varsa ret). Bütün ölçüler geriye
  bakar; tam veride hesaplanıp tarihe göre süzülür (geleceğe bakma testi test_vdyt2.py).

## 9. Süre (bölge başına)
- KM (BH1-onaylı büyük mum nedenine özgü; SÖNME ve SAHTE rakip; SANSÜR / BELİRSİZ sansür), Aalen-Johansen CIF, yaş kovası hazard'ı (V1.vdyt_sureklilik); ANA, P0
  ve P1. WF'de 2023-12-31'ten sonra biten / onayı taşan bölge SANSÜR.
- Dört yaklaşım ileriye dönük Brier (bölüm 8 modelleri, T0 ve T1'e karşı): A ORTAK (yalnız SÜRE), B HİSSEYE ÖZGÜ (SÜRE + HİSSE: yalnız t'de onayı bilinen, t'den
  önce biten bölgeler; en az 3 yoksa 'yetersiz' bayrağı), C REJİM (SÜRE + REJİM), D ADAPTİF (SÜRE + HİSSE + REJİM). Bitiş olasılık olarak (p5 / p10 / p20).
- OLG (D2): y10 oranı (yaş >= 30) - (yaş <= 15), hisse kümeli bootstrap; beklenen işaret yazılmaz (iki yanlı), sonuç ne çıkarsa.

## 10. Olaylar (AYNI sisteme girdi; ayrı proje değil)
- Modelde OLAY grubu (bilgi kuralıyla) + ablasyon. E1 (koşul günü c = g0 - 21; pencereler [[-20, -11], [-10, -6], [-5, -1], [0, 0], [1, 5], [6, 10], [11, 20]]) ve E2 (c = g0 - 1; [[0, 0], [1, 5], [6, 10], [11, 20]]):
  gözlenen (ilk onaylı BH penceresi) - beklenen (aynı c ayı / momentum / likidite tertili, yaşı ±2, ölçülen aralıkta aynı türden olayı
  olmayan en çok 5 kontrol; V1.vdyt_olay_analizi) = 'haber mi bitirdi, zaten bitecek miydi'.
- Haberli / habersiz (BH'ye dönüşen bölgenin son geçerli satırı; g'ye göre): haberli = A / B olayı [g-5, g+1];
  habersiz = A / B yok [g-10, g+1] ve makro yok [g-1, g]; yukarı payı ve |büyüklük| farkı (yıl x momentum x
  likidite tabakalı). Habersiz bölgeler hiçbir analizden ÇIKARILMAZ.
- Olay-bölge zaman ilişkisi: olay eşleme tablosu (V1._vdyt_olay_bolge_satir: bölgenin [bas, bitiş + 20] aralığındaki her olay; olay günündeki bölge yaşı,
  onaylı BH günü - olay günü, BH'den önce oynaklık artışı başlamış mı); tür başına özet. Haberli / habersiz satırlarda yön motorunun dengeli doğruluğu ayrı (BİLGİ).

## 11. Çoklu test ve plasebo
- BH q = 0.1 aile içinde: F1_BOLGE, F2_GENISLEME, F2_D1B, F3_YON, F4_OLAY, F5_SURE, F6_KATKI, F6_TEK_GRUP. Bir aile bulgusu 'TUTTU' ancak WF'de
  BH ile reddedilir VE KASA'da aynı işaretle %95 aralığı 0'ı dışlarsa.
- P1 plasebo (D4): her hissede gerçek olay sayısı kadar rastgele olay günü (bar 260 .. n-22), E1 ve E2, 50 tekrar, tür başına en çok 3000 olay;
  tekrar başına BH keşif sayısı (yanlış pozitif oranı) ve tür x kip x pencere |fark| eşiği (%95). E1 / E2 bulgusu ancak bu eşiği de aşarsa sayılır.
- P2 plasebo = RASTGELE kontrolün kendisi (bölüm 6).

## 12. Değerlendirme (bilgi satırları; hepsi raporlanır)
5 / 10 / 20 gün genişleme Brier / log loss skill, kalibrasyon (10 kutu, ECE), kesinlik / duyarlılık (eğitimin %90 eşiği), genişlemeye kadar süre (KM / CIF),
uyarı süresi, yanlış bölge sayısı, kaçırılan büyük hareket sayısı, yön dengeli doğruluk + Brier, işlem sonucu: tahmin edilen yöne işaretli r5 / r10 / r20 (t+1
açılışından) ve rk5 / rk10 / rk20 (kırılım sonrası: çıkış gününün ertesi açılışından), maliyet sonrası, M_TAM - B1 farkı; MFE / MAE (20 gün); birleşik üç sınıf
(20 gün içinde yukarı BH / aşağı BH / yok): M = p20 x p_yukarı vs T1 x B1 (P0 temelleri), çok sınıflı Brier skill, P0 ve P1; sınıf değerlendirmesi (WF / KASA
test satırlarında sınıf başına gerçekleşen y10 / y20 oranı ve yukarı payı; yön kapısı uygulanmadan).

## 13. Sınıflandırma (canlı çıktı; eşikler eğitimden ya da sabit, test sonucuna göre değişmez)
- Canlı model: kesik (2026-08-31) içinde etiketi tamamlanan bütün ANA satırlarıyla eğitilir; q_yüksek = bu eğitim tahminlerinin %80 yüzdeliği (p10).
  WF / KASA sınıf değerlendirmesinde q_yüksek o test yılının eğitiminden.
- Kurallar (öncelik sırası): 'Genişleme başladı' = ANA bölge son 3 işlem gününde büyük mumla bitti. 'Sıkışma yok' / 'Sıkışma oluşuyor' = açık bölge yok
  ve {G1, G2, G3 ∨ G4} üçünden en az 2'si doğru ise 'oluşuyor', değilse 'yok'. Açık bölge: karar günü geçersiz (D1a) ya da (2) o alt kümede
  BAŞARILI değil ya da p10 < q_yüksek -> 'Sıkışma devam ediyor'; p10 >= q_yüksek ve (3) o alt kümede BAŞARILI değil -> 'Yön belirsiz' (yön güvenilir değil); (3)
  BAŞARILI ise p_yukarı >= 0.6 -> 'Yukarı kırılma adayı', <= 0.4 -> 'Aşağı kırılma adayı', arada -> 'Genişlemeye yaklaşan sıkışma'. Alt küme: P1 bayrağı varsa P1,
  yoksa P2, yoksa P0.
- Güvenilirlik: genişleme YÜKSEK <=> (2) BAŞARILI ve KASA ECE <= 0.03 ve KASA skill >= 0.05; ORTA <=> (2) BAŞARILI; DÜŞÜK değilse. Yön sınıflarında
  min(genişleme, yön); yön YÜKSEK <=> (3) BAŞARILI ve KASA ECE <= 0.05 ve KASA dengeli doğruluk farkı >= 0.05.
- Tek nihai çıktı (hisse başına): (1) bölge var mı, (2) başlangıç tarihi, (3) kaç gündür (yaş), (4) sıkışma gücü = 100 x (1 - medyan(H-L) / ATRref) (0-100),
  (5) savunma hattı seviyesi (gövde tabanı), (6) p5 / p10 / p20, (7) zaman aralığı = p_h >= 0,5 olan ilk h ('<= h işlem günü'; yoksa '> 20'), (8) / (9) yukarı /
  aşağı olasılığı (büyük hareket olursa koşullu; ayrıca p20 x p_yukarı, p20 x p_aşağı), (10) güvenilirlik, (11) en önemli dayanaklar = lojistik katkı (katsayı x
  z-değer) mutlak en büyük 3; sınıf; ön koşul; geçerli gün; motor durumları; 'CANLI, test dışı'; veri eskiyse (> 10 gün) bayrak.

## 14. Grafik (seçim kuralı sonuç görülmeden)
Gruplar ['BASARILI', 'BASARISIZ', 'KACIRILAN', 'YON_DOGRU', 'YON_YANLIS', 'HABERSIZ']: BAŞARILI = ANA test satırı p10 >= q80 ve y10 = 1; BAŞARISIZ = p10 >= q80 ve y10 = 0 (yanlış alarm); KAÇIRILAN = BHU, g-1'de açık ANA bölge
yok; YÖN DOĞRU / YANLIŞ = yön testi satırında (p >= 0,5) çıkılan kenarla aynı / değil; HABERSİZ = BH'ye dönüşen, g çevresinde olay yok. Pazar x grup başına 5
örnek, numpy default_rng(sha256 tohum: 20261116, pazar, grup), aday listesi (sembol, t) sıralı. Paket (`paket`): örnek başına [bas-60, son olay+30] OHLCV + meta;
dosya başına < 3.0 MB. `ciz` YALNIZ paketten (Colab'da bağımsız; var olan PNG'nin üstüne yazmaz): [14, 8] inç, 150 dpi, büyük ve net gövde + fitil, ayrı
hacim paneli, küçük mum bölgesi, savunma hattı (t'ye kadar), tespit tarihi, karar günü, büyük hareket başlangıcı, yön; her örnek iki PNG: TAM ve TESPİT GÜNÜ
(yalnız t'ye kadarki mumlar; büyük hareket / yön / sonuç / grup adı YOK). Grafikler Drive'a parçalı yüklenmez; paketten Colab'da yeniden üretilir.

## 15. Sürüm ve çıktılar
Sürüm etiketi v2_20261112; repo arastirma_cikti/vdyt/v2_20261112/ (ön kayıt, kapsam, sonuç JSON, rapor, hata raporu, parametre kaydı, canlı tablo,
grafik paketi); büyük ara tablolar /tmp/vdyt2/<aşama>/ (bölge, satır, kontrol, tahmin, BHU, haber); Drive hedefi MyDrive/COLAB_VERILER/OUTPUT/VDYT/v2_20261112/ (yüklemeyi ana oturum yapar;
dosya < 3 MB). Her çıktıda sürüm, VDYT2.py ve VDYT.py sha256'sı, eşik mührü ve ön kayıt commit'i. Mevcut dosyalar silinmez / ezilmez (ön kayıt, KASA işareti, canlı
tablo ve PNG'ler üzerine yazmaz).

## 16. Yanlılık beyanı
- Yaşayan evren (V_BIST, k60): batan / kotasyondan çıkanlar yok; aşağı yönlü büyük hareketler ve sessizlikten sonra batanlar eksik -> yön sonuçları YUKARI
  lehine yanlı olabilir; BIST_K62 (çıkmış 92 hisse dahil, yalnız kapanış) başarı (1) için çıkmış / yaşayan ayrımıyla BİLGİ. ABD delist: veri yok.
- Yahoo takvimi yalnız bugün Yahoo'da olan 1.410 hisse; kalanında 2022-11 öncesi bilanço günü 10-Q / 10-K vekili (bilanço -> 10-Q medyan 8 gün). KAP saati
  18:00 varsayımı. Makro: yalnız TARİH (CPI / istihdam / TÜİK EKSİK). BIST KAP özel durum açıklamaları EKSİK -> BIST 'habersiz' = kayıtlı veri setlerinde olay yok.
- Etiket ve özellikler tam veride hesaplanıp tarihe göre süzülür; her ölçü geriye bakar (sentetik testte t sonrası barlar bozulunca özellikler ve geçerlilik
  aynı). Panel kesitleri (tertil, ondalık) yalnız aynı günün değerleri.

## 17. SAPMA / BOŞLUK (iş tanımına göre; ölçümden önce)
1. BH2 (v1 genişleme etiketi) ayrıca koşulmaz; v1 sonuçları kayıtlı (Ç162). v1 karşılaştırması v1 T1-T5 DURUMLARININ v2 bölge kuralı + BH1 etiketiyle koşulmasıdır.
2. BH1 başlangıcı 'ilk ONAYLI büyük mum': iş tanımındaki 'ilk büyük mum günü' + '10 günde bant çıkışı' şartının gerçek zamanlı biçimi; onaysız (sahte) büyük
   mumlar etiket olayı değildir, süre analizinde rakip olaydır. Referans pencere bölge başı bas'tan g-1'e (en çok 60 gün).
3. G3 (yaklaşan tepe-dip) eğim ölçüsü L = 10 günlük en küçük kareler eğimi; G4 penceresi 20 gün (tekrar test için 10 gün kısa; v1 savunma kuralı en az 3 temas ve
   5 bar aralık ister). G4 'savunulan' = hat VAR ve kapanışla kırılma YOK.
4. Modeller P0 satırlarıyla eğitilir, değerlendirme ve temeller alt kümede (bölüm 3). AILE tanımlarında yalnız M_TAM; ALT tanımlarında model yok (yalnız başarı 1).
5. Sınıf 'Yön belirsiz' iş tanımındaki gibi yön motoru geçmediğinde verilir; yön motoru geçtiğinde kararsız aralık (0,40-0,60) 'Genişlemeye yaklaşan sıkışma'dır.
   Genişleme motoru (2) geçmediyse 'Genişlemeye yaklaşan' ve aday sınıfları verilmez ('Sıkışma devam ediyor').
6. Plasebo P1 tekrar 50 (v1: 100, yalnız E2); v2'de E1 ve E2 birlikte (aynı toplam hesap) ve bulgu başına eşik.
7. ABD 8-K'ların 'bilanço günü ±3 iş günü' süzgeci v1 bilanço kümesiyle (Nasdaq / EDGAR) yapılır (v1 kodu; Yahoo değişikliğinden önce).
8. BOŞLUK: BIST 2015 öncesi OHLC yok (WF eğitimi 2016+); ABD delist yok; CPI / istihdam / TÜİK takvimi yok; BIST özel durum açıklamaları yok; ABD Yahoo takvimi
   1.410 hisse.
9. Kapsam (bölüm 19) yalnız sayım: bölge, geçerli karar günü, kontrol satırı, BHU TOPLAM sayısı; oran, yön, getiri, süre / bitiş türü dağılımı YOK.
10. Veri sha256'ları bu konteynerdeki /tmp dosyalarına bağlıdır; Faz 2 aynı veriyle koşmalı (değişirse SAPMA + yeni satırlar + kapsam yeniden).
11. Hesap sınırı: ALT / K62 satırları ve AILE / ALT / K62 kontrolleri yalnız 2019-01-01 sonrası etiketlenir (bölüm 6); ALT tanımlarında model yok. ANA'da
    kontrol katsayısı 5, diğerlerinde 2 (ANA'da tabaka kapsaması öncelikli).
12. G5 ailesinde bölgenin devamı çekirdek G1 VE G2 ile (bölüm 4); iş tanımındaki 'G5 = G1 ve G2 ve (G3 ya da G4)' AÇILIŞ şartıdır. Gerekçe: tepe-dip / destek
    şartı her gün yeniden aranırsa uzun sessiz bölge gün aşırı bölünür (sentetik sınamada görülen tasarım sorunu; gerçek veride hiçbir sonuç görülmeden).
13. Birleşik üç sınıf ve sınıf değerlendirmesi P0 temelleriyle (BİLGİ); karar hücreleri bölüm 7.
14. Kapsam sayımı (bölüm 19) ön kayıttan hemen önce AYNI kodla yapıldı (vdyt2_kapsam.json 'kod_sha256' = KOD_SHA256; değilse ret sebebi sayılır, ana oturum denetler).

## 18. Veri sha256 (ön kayıt anı; `kos` / `canli` yeniden hesaplar, farklıysa ret)
- G.pkl: sha256 cdde36f074df0a435274ffbb19ed4734b0291964db7e8093acd2a9e623c9fc3c (1 dosya)
- V_BIST.pkl: sha256 bbd09faa33fc5d1350c72fdfd038962e8079f950b5ae6eddc19c1efa881b1f51 (1 dosya)
- company_tickers.json: sha256 6f9cc4500a98fb4c048328d7df392ed48c092613ec0c3e93cd6c7a3502886074 (1 dosya)
- edgar_master: sha256 57d5329d3603d361e7d81831878dcbe05777a7771d0f845b76a77e21fa2edc77 (71 dosya)
- k35_sic.csv: sha256 1ac089db38678ef6d62b0e22562822f21d90fce6d96845dd4ea8d52e98ec52c9 (1 dosya)
- k58_yahoo: sha256 7059054137b9a6a6e98d16e5dbef012f718df33197c790a417e7ab0c577a4e03 (2 dosya)
- k60_fiyat: sha256 21435ad5b907eeb2dc4e8985e31c602900b2a010b7242c89331210e550dac374 (4757 dosya)
- k62_fiyat: sha256 bf3c29260b2b6d10794fb9338bb74253b291ef6c877c4d53d14f8a7f876bf636 (972 dosya)
- k62_kap: sha256 82cdbb0845835b464b8ed721d6f52afa22e9c682ec848478fc85c5fba7945ab1 (451 dosya)
- k67_takvim: sha256 ff93cf8c278e4fd928e6ff7113a9a66e06d1a516b5175a0bb70f0b84f9a9aefa (1410 dosya)
- kap_iceriden: sha256 14cc588b8499891aeeb249ec20d2e9fa6ec2a787a6b2383b6a24e7cd5c7781a0 (3 dosya)
- liste_abd.csv.gz: sha256 87539954817d5d551623eeed04fa410844646539093a4e841a7755a2cfc674cb (1 dosya)
- sektor_BIST.csv: sha256 0f933f73a6042c95d42275e0b9e1289221cc4f3b4b6d1df81987fcab14fd16d4 (1 dosya)
- surucu.pkl: sha256 c74304c1f921d7f087023559480bc217004e47ddb53684148c992d5d1b2a35bd (1 dosya)
- vdyt_makro_takvim.json: sha256 27a1f678211bedbc083ab5abd9f59b8cbdd7dba99cd41609bee53387828b3900 (1 dosya)

## 19. Kapsam (YALNIZ SAYI; `python -I VDYT2.py kapsam`, 2026-11-12 09:30:25 UTC)
- ABD: hisse 4.678, takvim ['2010-01-04', '2026-08-31']; bölgeden bağımsız büyük hareket başlangıcı (BHU) TOPLAM: 2010-2015 18.792, 2016-2018 16.441, 2019-2023 (WF test) 27.543, 2024-2026 (KASA) 22.588, hepsi 85.364
- BIST: hisse 581, takvim ['2015-06-01', '2026-08-31']; bölgeden bağımsız büyük hareket başlangıcı (BHU) TOPLAM: 2010-2015 0, 2016-2018 3.025, 2019-2023 (WF test) 5.973, 2024-2026 (KASA) 3.580, hepsi 12.578
- BIST_K62: hisse 715, takvim ['2008-01-02', '2026-08-31']; bölgeden bağımsız büyük hareket başlangıcı (BHU) TOPLAM: 2010-2015 12.707, 2016-2018 7.292, 2019-2023 (WF test) 12.509, 2024-2026 (KASA) 8.369, hepsi 42.649

| pazar | tanım | rol | bölge (uygun) | bölge P1 | geçerli karar günü | P1 | WF test 2019-2023 (P1) | KASA 2024-2026 (P1) | DIŞARI kontrol (P1) | RASTGELE kontrol (P1) |
|---|---|---|---|---|---|---|---|---|---|---|
| ABD | G1 | ALT | 68.005 | 19.261 | 146.779 | 49.583 | 25.646 | 14.589 | 208.287 (37.135) | 248.739 (45.527) |
| ABD | G1_e0.5 | ALT | 27.785 | 12.557 | 59.077 | 30.965 | 16.858 | 8.800 | 84.468 (26.188) | 94.284 (23.652) |
| ABD | G1_e0.7 | ALT | 111.464 | 23.468 | 248.625 | 62.274 | 31.125 | 18.633 | 336.675 (43.667) | 429.063 (66.016) |
| ABD | G2 | ALT | 95.573 | 10.256 | 160.497 | 16.994 | 8.442 | 5.219 | 257.050 (30.869) | 274.756 (37.135) |
| ABD | G3 | ALT | 159.934 | 25.718 | 206.078 | 33.871 | 16.326 | 10.071 | 332.504 (52.567) | 331.220 (45.552) |
| ABD | G4 | ALT | 257.216 | 38.345 | 573.160 | 87.749 | 44.309 | 24.770 | 627.299 (94.622) | 1.003.149 (135.411) |
| ABD | G5 | ANA | 22.543 | 5.773 | 36.741 | 9.561 | 4.955 | 2.774 | 140.757 (29.137) | 60.630 (10.760) |
| ABD | G5_g0.4 | ALT | 12.023 | 2.710 | 18.355 | 4.171 | 2.190 | 1.161 | 29.201 (5.500) | 30.036 (5.103) |
| ABD | G5_g0.6 | ALT | 32.160 | 9.072 | 55.405 | 15.981 | 8.343 | 4.715 | 88.005 (19.684) | 92.632 (17.022) |
| ABD | G5f | AILE | 25.029 | 6.263 | 40.516 | 10.313 | 5.339 | 2.994 | 64.808 (13.294) | 67.311 (11.791) |
| ABD | G5k | AILE | 19.697 | 5.017 | 32.232 | 8.350 | 4.279 | 2.442 | 51.723 (10.925) | 53.456 (9.464) |
| ABD | T1 | ALT | 16.066 | 1.575 | 32.648 | 3.271 | 1.951 | 839 | 49.755 (5.416) | 58.847 (8.690) |
| ABD | T2 | ALT | 54.091 | 4.749 | 138.162 | 11.950 | 6.366 | 3.630 | 223.865 (24.528) | 247.818 (32.559) |
| ABD | T3 | ALT | 59.685 | 5.824 | 130.612 | 12.512 | 6.372 | 3.988 | 218.920 (24.912) | 234.888 (31.078) |
| ABD | T4 | ALT | 38.754 | 3.674 | 83.514 | 7.877 | 4.057 | 2.506 | 139.357 (15.411) | 147.489 (19.029) |
| ABD | T5 | ALT | 23.699 | 2.062 | 49.159 | 4.340 | 2.435 | 1.263 | 81.711 (8.583) | 87.733 (12.032) |
| BIST | G1 | ALT | 10.339 | 3.610 | 21.776 | 8.323 | 3.563 | 3.227 | 23.335 (3.870) | 36.359 (7.913) |
| BIST | G1_e0.5 | ALT | 7.034 | 2.946 | 13.876 | 6.328 | 2.755 | 2.520 | 15.759 (3.331) | 23.341 (5.426) |
| BIST | G1_e0.7 | ALT | 12.852 | 4.031 | 27.697 | 9.615 | 4.174 | 3.589 | 28.335 (4.101) | 46.176 (9.688) |
| BIST | G2 | ALT | 13.264 | 3.321 | 21.801 | 5.708 | 2.593 | 2.347 | 28.622 (6.065) | 35.887 (7.383) |
| BIST | G3 | ALT | 22.843 | 4.797 | 31.056 | 6.516 | 3.075 | 2.009 | 44.365 (8.709) | 46.690 (9.236) |
| BIST | G4 | ALT | 31.883 | 6.276 | 67.271 | 13.281 | 6.396 | 4.534 | 54.607 (11.399) | 110.830 (21.471) |
| BIST | G5 | ANA | 5.584 | 2.156 | 9.163 | 3.641 | 1.631 | 1.497 | 27.466 (7.125) | 15.327 (3.378) |
| BIST | G5_g0.4 | ALT | 3.692 | 1.462 | 5.669 | 2.311 | 1.054 | 938 | 7.573 (2.155) | 9.259 (2.111) |
| BIST | G5_g0.6 | ALT | 6.873 | 2.647 | 12.031 | 4.798 | 2.124 | 1.965 | 15.420 (3.888) | 20.082 (4.564) |
| BIST | G5f | AILE | 6.021 | 2.296 | 9.838 | 3.884 | 1.743 | 1.597 | 12.812 (3.294) | 16.304 (3.704) |
| BIST | G5k | AILE | 5.143 | 1.988 | 8.512 | 3.386 | 1.521 | 1.375 | 11.210 (2.932) | 13.977 (3.210) |
| BIST | T1 | ALT | 3.393 | 998 | 6.152 | 1.859 | 923 | 772 | 7.599 (1.568) | 11.176 (2.481) |
| BIST | T2 | ALT | 6.317 | 1.570 | 13.949 | 3.534 | 1.613 | 1.602 | 19.391 (3.980) | 24.568 (5.130) |
| BIST | T3 | ALT | 6.905 | 1.631 | 13.717 | 3.282 | 1.461 | 1.495 | 19.691 (4.260) | 24.048 (4.776) |
| BIST | T4 | ALT | 5.031 | 1.240 | 9.926 | 2.493 | 1.276 | 902 | 13.856 (3.011) | 17.040 (3.513) |
| BIST | T5 | ALT | 3.555 | 946 | 6.711 | 1.825 | 913 | 721 | 9.370 (2.084) | 11.868 (2.479) |
| BIST_K62 | G2K | K62 | 32.754 | 6.599 | 35.877 | 7.691 | 2.183 | 2.010 | 28.278 (5.184) | 46.750 (8.365) |

Ayrıntı: arastirma_cikti/vdyt/v2_20261112/VDYT2_KAPSAM.md.

## 20. Faz 2 komutları
1. (ana oturum) bu dosyayı, VDYT2.py'yi ve test_vdyt2.py'yi denetler, git'e işler (VDYT.py zaten işlenmiş).
2. `python -I VDYT2.py kos --asama wf` -> WF ölçümü + VDYT2_RAPOR_wf.md (mühür, iki kod, veri sha256 ve git doğrulanır; yoksa ret).
3. `python -I VDYT2.py kos --asama kasa` -> KASA bir kez; karar tablosu (üç başarı ayrı) + teyit.
4. `python -I VDYT2.py canli` -> vdyt2_canli_<tarih>.csv (CANLI, test dışı). 5. `python VDYT2.py paket --asama kasa` -> grafik paketi; Colab: `v2_ciz(paket, çıktı)`.
Tahmini süre (bu konteyner, 4 çekirdek, 3 işçi; BIST 40 hisselik ölçümden ölçeklenmiş): kapsam BIST ~3 dk, ABD ~30 dk, BIST_K62 ~2 dk; `kos wf` BIST ~10 dk +
ABD ~60-80 dk + K62 ~5 dk; `kos kasa` aynı (~75-95 dk); canlı ~40 dk (ABD fiyatı kesiksiz yeniden okunur); paket < 5 dk. Bellek: ABD tam satır tabloları birkaç GB.

## 21. Değişmezlik
VDYT2_ESIK, VDYT2_OZELLIK, VDYT2_MODEL (ve içe aktarılan v1 olay / EDGAR tanımları) değişirse ESIK_SHA256; VDYT2.py ya da VDYT.py değişirse KOD satırları; veri
değişirse veri sha256 tutmaz -> `kos` / `canli` durur.
