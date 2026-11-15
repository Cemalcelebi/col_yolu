# VDYT veri envanteri (yeni indirmeden önce)

Üretim: 2026-11-12 06:14:02 UTC — `python VDYT.py envanter` (VDYT v1.0 (2026-11-12): Faz 1 (envanter, ön kayıt, kod + sentetik test, kapsam sayımı); ölçüm Faz 2'de, ön kayıt git'e işlendikten sonra). Sayılar dosyalardan okundu; getiri hesaplanmadı. Kesik: fiyatlar 2026-08-31'de kesilir
(fon krizi kuralı). Durum: VAR = analizde kullanılabilir; KISMEN = dönem / alan / pazar eksik; EKSİK = yok (ikame / uydurma yapılmadı).

## 1. Özet tablo (veri türü x pazar)

| veri türü | BIST | ABD | VDYT'de kullanım |
|---|---|---|---|
| Günlük OHLCV | VAR: V_BIST 581 hisse, 2015-06-01 → 2026-10-22 (357 hisse 2015-07 öncesinden); yalnız yaşayanlar | VAR: k60_fiyat 4678 hisse, 2010-01-04 → 2026-08-31 (1906 hisse 2010 başından); yalnız yaşayanlar | ana fiyat verisi |
| Uzun geçmiş / kotasyondan çıkanlar | KISMEN: K62 İş Yatırım 715 hisse, 2008-01-02 → 2026-08-31, çıkmış 92; YALNIZ kapanış + hacim (açılış / yüksek / düşük YOK) | KISMEN: k34_yahoo - hisse ama -+ ve neredeyse hepsi yaşayan (- çıkmış); batanların Tiingo fiyatı lisans gereği yok | BIST_K62: yanlılık kontrolü (kapanış tanımları T2-T4); ABD delist: EKSİK |
| Endeks | VAR: XU100.IS ["1997-07-01", "2026-08-31", 7509]; K62 'endeks' sütunu | VAR: SPY ["1993-01-29", "2026-08-31", 8454]; Fama-French günlük piyasa (1926+) | piyasa rejimi, pazar yönü |
| Sektör | VAR: sektor_BIST.csv (BIST alt endekslerinden; 12 grup, 583 hisse) | KISMEN: SIC (k35, CIK→bugünkü kod) 4005 hisse, 55 grup; sektor_ABD.csv yalnız V_ABD | sektör rejimi, rakip bilançosu |
| Bilanço tarihleri | VAR: KAP Finansal Rapor 2009-06+ (K62 kap; 106852 kayıt), yayın saatli | KISMEN: Nasdaq takvimi 2022-12-01 00:00:00 → 2026-10-27 00:00:00 (saat %99 verilmemiş); öncesi 10-Q/10-K başvuru günü (EDGAR, VEKİL) | A planlı olay, beklenen bilanço özelliği |
| Temettü / bölünme / hak kullanım | KISMEN: K62 ham / düzeltilmiş kapanış oranı ve sermaye değişimi (hak kullanım günü; duyuru günü YOK) | VAR: Yahoo olayları (hak kullanım günü; 1789 hisse temettü, 1775 bölünme) | A planlı olay |
| Sermaye artırımı / pay arzı | KISMEN: K62 sermaye değişimi (tescil / işlem günü; karar günü YOK) | VAR: EDGAR S-1, S-3, 424B* başvuru günleri | B olay |
| Genel kurul | EKSİK | KISMEN: DEF 14A (vekâlet bildirimi; toplantı günü değil) | A olay (ABD) |
| İhale / sözleşme / sipariş / ortaklık / yönetim / dava / ürün (KAP özel durum) | EKSİK (KAP ÖDA listesi inmedi) | KISMEN: 8-K (madde kodu YOK), 13D, 425 / SC TO / DEFM14A | B olay; BIST'te 'habersiz' grup kirli (beyan) |
| İçeriden işlem | KISMEN: KAP Pay Alım Satım 2022-07 → 2026-10 (6637 bildirim ayrıştırıldı; bölüm 3) | KISMEN: k30 Form 4 açık piyasa alımları 2022+ (özet; VDYT'de kullanılmıyor) | B olay (BIST) |
| Fon portföy raporları | KISMEN: G.pkl 2023-01-02 19:04:37 → 2026-10-12 15:06:37 (13111 rapor, 549 fon); ham paket kapfon-veri dalında (açılmadı) | — | B olay (fon girişi) |
| Makro takvim | KISMEN: TCMB PPK günleri (`makro`); TÜİK enflasyon günü EKSİK | KISMEN: FOMC günleri (`makro`); CPI / istihdam (BLS 403) EKSİK | C olay; içerik / sürpriz YOK |
| Emtia / kur / faiz | VAR: surucu.pkl (GC, SI, CL, HG, ZW, HRC, ALI, USDTRY, ^TNX 2015+, CDS 2022+) | aynı | C olay (şok günleri), 2010-2014 EKSİK |
| Sektör haberleri | VERİ YOK | VERİ YOK | yok (beyan) |
| Endeks gelişmeleri (endekse giriş / çıkış) | EKSİK | EKSİK | yok |
| Açığa satış | — | VAR: FINRA iki haftalık 20171229 → 20260831 (209 dosya) | VDYT'de kullanılmıyor (olay değil; bilgi) |
| Saatlik veri | — | KISMEN: k40 saatlik yalnız 4 endeks, son 730 gün | kullanılmıyor |
| Önceki sıkışma / volatilite / rejim tabloları | VAR (farklı tanımlar): MUM_SUKUN, SESSIZ_ML, K55 dallanma, COL_GOZ, rejim.py (CDS / EEM) | K55 / K60 kapsam tabloları | KULLANILMAZ: VDYT bağımsız motor; tanımlar ön kayıtta baştan |

## 2. Kaynak ayrıntıları

### 2.1 BIST günlük OHLCV — V_BIST.pkl (islenmis-veri dalı → /tmp/veri)
- Konum: `/tmp/veri/V_BIST.pkl`; FON_IZI fi_k1_veri çıktısı (bölünme / marj düzeltmeli). Alanlar ['Open', 'High', 'Low', 'Close', 'Volume'].
- 581 hisse; ilk gün en erken 2015-06-01 (medyan 2015-06-01); son gün 2026-10-22 … 2026-10-22; 1272889 satır.
- Kalite: H = L 49371 gün, hacim <= 0 26149 gün (VDYT bunları işlemsiz gün sayar, atar), OHLC tutarsız 29 satır (H = max(O,H,C), L = min(O,L,C) ile düzeltilir).
- Delist: YOK (bugün işlem görenler). Durum: VAR (yaşayan yanlılığı beyan).

### 2.2 BIST uzun geçmiş — K62 İş Yatırım günlük (/tmp/k62_veri/fiyat)
- 972 kod dosyası, 715 dolu; ilk 2008-01-02 (319 hisse 2010 başından), son 2026-08-31 (K62 kesiği). Alanlar ['tarih', 'kapanis', 'ham', 'pd', 'pd_usd', 'hacim_tl', 'hacim_usd', 'endeks', 'sermaye'].
- Kotasyondan çıkmış (son gün 2026-06 öncesi): 92; çıkış yılları {"2009": 2, "2011": 1, "2012": 3, "2013": 6, "2014": 9, "2015": 15, "2016": 12, "2017": 7, "2018": 10, "2019": 6, "2020": 17, "2021": 1, "2022": 1, "2026": 2}.
- AÇILIŞ / YÜKSEK / DÜŞÜK YOK → ATR, gövde, fitil, savunma hattı (gövde / fitil tabanı) hesaplanamaz. Durum: KISMEN (yalnız kapanış tanımları T2-T4 ve RV genişlemesi; yanlılık kontrolü).

### 2.3 ABD günlük OHLCV — k60_fiyat (Yahoo, /tmp/k60_fiyat) ve V_ABD
- k60_fiyat: 4755 JSON, fiyatlı 4678; durum {"fiyat": 4706, "yok": 33, "veri yok": 16}; tür {"EQUITY": 4696, "MUTUALFUND": 8, "ETF": 2}; ilk 2010-01-04, son 2026-08-31 (K60 kesiği); 2015 sonundan önce başlayan 2577.
- V_ABD: 1411 hisse, 2015-06-01 → 2026-10-22 (hepsi k60 evreninde; VDYT ABD = k60, V_ABD alt küme bilgisi).
- k34_yahoo (veri2): - hisse, - → -, son günü 2026-06 öncesi - → delist yanlılığını azaltmaz.
- Delist: Yahoo batan şirketin fiyatını vermez; Tiingo fiyatları lisans gereği repoda yok. Durum: VAR (yaşayan yanlılığı büyük, beyan).

### 2.4 Olay kaynakları
- KAP Finansal Rapor (K62 kap, 2009-06+): 161908 kayıt; konu sayımı {"Finansal Rapor": 106852, "Sorumluluk Beyanı (Konsolide)": 14356, "Sorumluluk Beyanı (Konsolide Olmayan)": 14260, "Faaliyet Raporu (Konsolide)": 13144, "Faaliyet Raporu (Konsolide Olmayan)": 11428, "Faaliyet Raporu Sorumluluk Beyanı": 1237, "TSRS Uyumlu Sürdürülebilirlik Raporu": 387, "Finansal Rapor Bildirimi": 130, "Entegre Rapor": 114}; 2009-06-01 08:13:16 → 2026-08-31 21:51:38. pead listeleri: 2022-07+ 14739 satır, 2016-07 → 2022-12 16983 satır (K62 kap bunları kapsar).
- Nasdaq bilanço takvimi (pead/liste_abd): 65474 satır, 4865 kod, 2022-12-01 00:00:00 → 2026-10-27 00:00:00; saat {"time-not-supplied": 64750, "time-after-hours": 370, "time-pre-market": 324}.
- EDGAR üç aylık ana dizin (/tmp/k60_secframes/edgar_master_*): 71 dosya (2009Q1 → 2026Q3), 18681292 satır; seçili formlar 3771867, bugünkü kodla eşlenen 7615882; grup sayımı {"ABD_13D": 82105, "ABD_8K": 893511, "ABD_BILANCO_EDGAR": 295294, "ABD_BIRLESME": 61484, "ABD_GECIKME": 16586, "ABD_SERMAYE": 6197588, "ABD_VEKALET": 69314}. Yalnız form türü ve başvuru GÜNÜ (saat yok, 8-K madde kodu yok); CIK → kod eşlemesi bugünkü company_tickers (8024 CIK).
- Fon portföy raporları: G.pkl 263521 satır, 13111 rapor, 549 fon, 551 hisse, 2023-01-02 19:04:37 → 2026-10-12 15:06:37; ham KAP fon raporu paketi kapfon-veri dalında (["BENIOKU.md", "kapfon/ekler.csv.gz", "kapfon/k9_islem.csv.gz", "kapfon/k9_kontrol.csv.gz", "kapfon/k9_pozisyon.csv.gz", "kapfon/liste.csv.gz", "kapfon/liste_haftalar.txt", "kapfon/manifest.json", "kapfon/metin.tar.xz.000", "kapfon/metin.tar.xz.001", "kapfon/metin.tar.xz.002", "kapfon/metin.tar.xz.0).
- Makro: {"FOMC": 154, "FOMC_planli": 151, "PPK": 126, "ilk_FOMC": "2009-01-28", "ilk_PPK": "2015-01-20", "EKSIK": {"CPI_BLS": "bls.gov 403 (erişim engeli)", "ISTIHDAM_BLS": "bls.gov 403", "TUIK_ENFLASYON": "data.tuik.gov.tr yayın takvimi alınmadı", "sayfa": ["PPK2009", "PPK2010", "PPK2011", "PPK2012", "PPK2013", "PPK2014"]}}.
- Emtia / kur / faiz (k36 surucu.pkl): {"GC=F": ["2015-01-02", "2026-10-28", 2973], "SI=F": ["2015-01-02", "2026-10-28", 2972], "CL=F": ["2015-01-02", "2026-10-28", 2973], "HG=F": ["2015-01-02", "2026-10-28", 2973], "ZW=F": ["2015-01-02", "2026-10-28", 2972], "HRC=F": ["2015-01-02", "2026-10-27", 2960], "ALI=F": ["2015-01-02", "2026-10-27", 2935], "USDTRY=X": ["2015-01-01", "2026-10-28", 3077], "^TNX": ["2015-01-02", "2026-10-27", 2971], "CDS": ["2022-01-03", "2026-10-19", 1229]}.

## 3. '6.637 KAP raporu' kaydı (Cemal'in bildiği kaynak)
- Nerede yazıyor: IZ_DEFTERI.md görev günlüğü 2026-10-26 satırı ve Ç99 (IZ_KARNE.py IK_KAYIT, K27); kod FON_IZI.py `fi_k27_liste`, `fi_k27_ayristir`, `fi_k27_pdf_ayristir`, `fi_k27_indir`, `fi_k27_olaylar`; çıktılar arastirma_cikti/fon_izi/k27_ozet.csv, k27_olay.csv, k27_deneme.csv.
- Ne: finansal rapor DEĞİL; KAP 'Pay Alım Satım Bildirimi' (içeriden işlem bildirimleri; konu 8aca490d50286f620150287614ae005c), 2022-07 → 2026-10.
- Veri: islenmis-veri dalı `kap_iceriden/` (liste.csv.gz, islem.csv.gz, bos.txt) → `/tmp/iv/kap_iceriden` (git worktree; yeniden indirilmedi).
- Dosyadan sayım: liste 8609 bildirim (2022-07-01 09:13:13 → 2026-10-26 18:28:49); aracı kurum / portföy şirketi hariç 7313; ayrıştırılan
  6637 bildirim = 6955 işlem satırı (bildirim başına ilk kaynak {"pdf": 5712, "tablo": 925}); ayrıştırılamayan 676.
  Alanlar: ['indeks', 'tarih', 'alim', 'satim', 'bas', 'son', 'oran_bas', 'oran_son', 'gorev', 'kaynak']. Not: defterde '6.265'i MKK aktarımı PDF' yazıyor; dosyadaki bildirim başına ilk kaynak sayımı yukarıdaki gibidir (fark sayım biçiminden; ana oturum denetlesin).
- VDYT kullanımı: B olayı 'içeriden net alım / net satım bildirimi' (net = gün sonu - gün başı nominal, yoksa alım - satım), bilgi zamanı KAP yayın saati.
- KAP finansal rapor listesi ayrıdır: 2009-06+ 106852 'Finansal Rapor' kaydı (K62), 2016-07+ pead listeleri.

## 4. Önceki sıkışma / volatilite / rejim tabloları
{"mum_sukun": ["MUM_SUKUN_rapor.md", "MUM_SUKUN_zemin_rapor.md", "mum_sukun_olaylar.csv.gz", "mum_sukun_ozet.csv", "zemin_ayrilma_boy.csv", "zemin_ayrilma_boy_hacim.csv", "zemin_kisa_ozet.csv", "zemin_olaylar.csv.gz", "zemin_ozet.csv"], "sessiz_ml": ["SESSIZ_ML_ogretmen.md", "SESSIZ_ML_rapor.md", "modeller.tar.gz", "ogr_islemler.csv", "ogr_kanit.csv", "ogr_kesim_tespit.csv", "ogr_olaylar.csv.gz", "ogr_onem.csv", "ogr_profil.csv", "ogr_tuttu_mu.csv", "sm_alis_tahmin_k20.csv.gz", "sm_basari.csv", "sm_cikis.csv", "sm_degerlendirme.csv", "sm_egitim_kaniti.csv", "sm_fon_2026.csv", "sm_islemler_model_cikis.csv.gz", "sm_islemler_uretim.csv.gz", "sm_onem_k20.csv", "sm_onem_satis.csv", "sm_onem_x2.csv", "sm_portfoy.csv", "sm_satis_degerlendirme.csv", "sm_sizinti.csv"], "k55_dallanma": ["K55_ADAYLAR.md", "K55_COKLU_TEST.csv", "K55_EVREN.csv", "K55_EVREN_DISI.csv", "K55_EVREN_DISI_KISA.csv", "K55_FAZ0_RAPOR.md", "K55_FAZ1_RAPOR.md", "K55_HUCRE_ISKELE.csv", "K55_HUCRE_SONUC.csv", "K55_K54_TUTARLILIK.csv", "K55_KESIM.csv", "K55_KOSU.json", "K55_KOSU_FAZ1.json", "K55_OLAYLAR.csv.gz", "K55_ORNEKLEM.csv", "K55_PLAN.md", "K55_SIZINTI_TESTI.md", "K55_VARYANTLAR.csv", "K55_VERI_KALITESI.csv", "K55_VERI_KAPSAMI.md", "tam_evren"], "col_goz": ["COL_GOZ_rapor.md", "COL_ISARET_yerlesim.json", "col_goz_kapali_eslesme.json"], "k60_veri": ["K60_SEC_ISTEK_LISTESI.csv", "K60_VERI_DENETIM.md", "K60_VERI_OZET.md", "K60_VERI_PLANI.md", "evren_ay.csv", "fiyat_kapsam.csv", "sec_sayim.csv"]}
Bunlar farklı amaçla ve farklı tanımla üretildi (Çöl Yolu, K55, MUM_SUKUN). VDYT bunları GİRDİ olarak kullanmaz; tanımlar ön kayıtta baştan ve bağımsız.

## 5. Kullanım kararı (ön kayıtta bağlayıcı)
- Karar pazarları: BIST = V_BIST (OHLCV, 2015-06+), ABD = k60_fiyat (OHLCV, 2010+). BIST_K62 (kapanış, 2008+, kotasyondan çıkanlar dahil) yalnız yanlılık kontrolü.
- Yeni fiyat / olay indirmesi YOK. Tek ağ işi: `makro` komutu ile resmi FOMC / PPK tarih listesi (bu oturumda indirildiyse yukarıda sayısı var).
