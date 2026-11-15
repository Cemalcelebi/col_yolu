# İZ projesi veri envanteri, VDYT'nin gerçek eksikleri, fiyat kapsam açığı ve ücretli veri karar tablosu

Tarih: 2026-11-12. Yalnız okuma ve sayım: sinyal testi, getiri hesabı, satın alma, kayıt, SEC isteği YOK. Yeni indirme yok (yalnız üç resmî takvim sayfasına erişim denemesi, bölüm 3).
Sayım betikleri (repoya eklenmedi): scratchpad `abd_kapsam.py`, `fiyat_kalite.py`, `spike.py`, çıktılar `abd_kapsam.json`, `fiyat_kalite.json`, `tiingo_yil.csv`
(/tmp/claude-0/-home-user-col-yolu/2d897341-a66f-57df-ba5e-2bfd9dd60c3c/scratchpad/). Güven etiketleri: **[SAYILDI]** bu çalışmada dosyadan sayıldı; **[RAPOR]** repodaki
rapordan alındı (kaynağı yazılı); **[LİSTE]** sağlayıcı sayfası (başka raporun okuduğu); **[GENEL]** yaygın bilgi, doğrulanmadı; **[DRIVE]** Drive'da, bu oturumda doğrulanmadı.

---

## 0. Bir sayfalık özet

**Elde ne var.** Fiyat: BIST 581 hisse OHLCV 2015-06 → 2026-10 (V_BIST), BIST 715 hisse yalnız kapanış 2008 → 2026-08 (K62, kotasyondan çıkan 92 dahil), ABD 4.678 hisse OHLCV
2010 → 2026-08 (k60_fiyat), Avrupa 581 hisse (V_AVR). Olay: KAP finansal rapor 2009-06+ (106.852), KAP içeriden işlem 2022-07+ (8.609 bildirim), KAP fon raporları
Ara 2022+ (45.740), EDGAR üç aylık dizin 2009Q1-2026Q3 (18,7 mn satır), SEC başvuru özeti 3.262 şirket (8-K madde kodlarıyla), Nasdaq takvimi 2022-12+, Yahoo bilanço
takvimi saatli 1.410 hisse 2002+, Yahoo analist not günlüğü, FINRA açık pozisyon 2017-12+, SEC finansal tablolar 2021+, SEC XBRL çerçeveleri 2009+.

**VDYT'nin 'EKSİK' dediklerinin çoğu aslında var ya da ücretsiz.** 17 eksik maddeden:
- elde VAR / KISMEN VAR (VDYT görmedi): ABD 8-K madde kodları (k55 sec_ozet: 570.155 8-K, k60 şirketlerinin %55'i), ABD bilanço günü 2010-2022 ve saati (Yahoo takvimi,
  1.410 hisse, 87.171 satır, saat dolu), BIST KAP özel durum (Drive kap_ozet 2017-26, konu kodlu; [DRIVE]), kod değişikliği eşlemesi (formerNames, k34 eski kod), ABD Form 4 yönü (Drive sec/ ham zipler).
- ÜCRETSİZ kaynak var, indirilmedi: BIST OHLC kotasyondan çıkanlar dahil (Borsa İstanbul günlük bülteni; 2017-01-03 örneğinde sonradan çıkan 10 hisseden 9'u OHLC ile var),
  KAP ÖDA / genel kurul / temettü kararı (KAP API, K62'nin kullandığı uç, sınıf süzgeci), BIST içeriden 2022-07 öncesi (KAP), emtia 2010-14 (Yahoo vadeli), endeks giriş / çıkış (Borsa / S&P duyuruları),
  CPI / istihdam / TÜİK takvimi (resmî sayfalar; bu konteynerden erişilemedi: bls.gov 403, FRED zaman aşımı, TÜİK zaman aşımı).
- **GERÇEKTEN EKSİK (ücretsiz, erişilebilir kaynak yok): 5 tür.** (1) ABD batan / kotasyondan çıkan şirket fiyatları, (2) hisse eşlemeli tarihsel haber / duyarlılık (ABD; BIST hiç yok),
  (3) makro beklenti / sürpriz (ABD konsensüs), (4) tarihsel gün içi hisse verisi (BIST tamamen; ABD yalnız IEX / hesaplı yollar), (5) BIST analist tahmini geçmişi.

**Fiyat kapsam açığı (Tiingo kararı için): KANITLANMIŞ AÇIK VAR, yalnız ABD'de büyük.**
- k60_fiyat'ta kotasyondan çıkan seri pratikte 0 (4.706 serinin 4'ü 2026-06 öncesinde bitiyor). Tiingo'nun ABD borsa hisse listesine göre bir yılda işlem görenlerin
  **sonradan çıkan payı: 2016 %44, 2018 %36, 2020 %28, 2022 %24, 2023 %19, 2024 %11** (adi hisse biçimli kod, SPAC / ADR / kapalı fon dahil, üst sınıra yakın).
  k60 o yıl aktif Tiingo evreninin 2016'da %48'ini, 2024'te %70'ini kapsıyor.
- EDGAR (yerel dizin): 2010-2026 arasında 10-Q veren 16.914 tekil CIK'in **11.514'ünün bugün kodu yok**; yıl yıl kodsuz pay 2010 %74 → 2016 %58 → 2020 %42 → 2024 %25.
  Bunlar borsada olmayan SEC kayıtlılarını da içerir (üst sınır). Kodsuzların son bilinen toplam varlığı: %31 < 10 mn $, %9 10-50 mn $, %15 50-300 mn $ (yarısından fazlası küçük / mikro).
- Yön: yaşayan evren −%50 olasılığını DÜŞÜK, +%100 ve 10x taban oranlarını YÜKSEK gösterir; küçüklük / sıkıntı / oynaklık sinyalleri en açık olanlar. Ama ölçülen etki küçük:
  K54'te delist bandı sonuçları 4. ondalıkta oynatmadı; K34'te küçüklük etkisi batanlar eklenince üçte bire indi.
- BIST'te açık küçük ve ücretsiz kapatılabilir: K62'de çıkan 92 hissenin hiçbiri V_BIST'te yok; 2016'da aktif K62 hissesinin %13'ü, 2019'da %7'si, 2022+ < %1'i sonradan çıkıyor.
- Kalite açığı küçük, Tiingo gerektirmez: V_BIST H = L 49.371 gün (%3,9), hacim 0 26.149 gün, OHLC tutarsız 30 satır, |günlük getiri| > %21 0 gün; V_BIST ile K62 kapanışı
  günlerin %0,29'unda > 5 puan ayrışıyor (91 günde > 20 puan). k60'ta 'uygun' satırlarda (önceki kapanış ≥ 2 $, hacim > 0) tek günlük sıçra-geri dön hatası 1.160 / 10,8 mn.
- **Sonuç: Tiingo'yu yeniden değerlendirme gerekçesi VAR (kapsam açığı ABD'de kanıtlı), satın alma gerekçesi YOK.** Ücretsiz katman (Cemal'in mevcut hesabı, 0 $, ayda 500 sembol)
  açığın 2016+ kısmını kapatır; Power (30 $/ay) yalnız hızdır. Karar Cemal'in; bu çalışma hiçbir kayıt / satın alma yapmadı.

**Kalıcılık riski.** Yalnız bu konteynerde duran ve kopyası olmayan **~3,7 GB** ham veri var. Kaybolursa en zor yeniden kurulanlar (öneri: islenmis-veri dalına xz paketi):
k60_fiyat (1,3 GB → ~150 MB xz), k60_secframes + EDGAR dizini (978 MB → ~85 MB; yeniden indirme SEC e-postası ister), k62_veri (74 MB; tek kotasyondan çıkan BIST kapanış kaynağı),
k67_yahoo (14 MB; tek saatli bilanço takvimi ve analist günlüğü). Ayrıca repoda git dışı 87 çıktı (85 MB, `.gitignore` `*.csv`). **evren_disi_ABD.csv repoda ve git geçmişinde hiç yok**
(CLAUDE.md var diyor; `*.csv` kuralı dışarıda bırakmış): COL_YOLU_ABD.py yeni ortamda bu dosyayı bulamazsa durur.

**Ücretli veri: hiçbir satır 'şimdi al' değil.** En yüksek beklenen katkı ABD batan fiyatı (ücretsiz katmanla kapatılabilir), sonra EPS revizyonu (önce ücretsiz 25 hisselik pilot).
Haber / duyarlılık premium ve arşiv derinliği bilinmiyor; emir defteri ve ödünç ücreti (VDYT dışı) güç / maliyet açısından en zayıf. BIST KAP özel durum ücretsiz; BIST analist geçmişi hiçbir yerde yok.

---

## 1. Tam envanter

Sütunlar: tür | pazar | tarih aralığı | hisse / kayıt | alanlar | kotasyondan çıkan kapsamı | nokta-zaman (bilgi tarihi) güvenilirliği | konum | kalıcılık | kullanan çalışmalar.

### 1a. Repo ana dal (main / bu dal) küçük veri ve ayar dosyaları [SAYILDI]

| dosya | tür | pazar | aralık | boyut | alanlar | çıkan | nokta-zaman | kullanan |
|---|---|---|---|---|---|---|---|---|
| sektor_BIST.csv | sektör ayarı | BIST | anlık | 583 hisse | sembol, sektor, alt, endeks, alt_bist | yok | bugünkü sınıf (geriye uygulanır) | COL_v1, FON_IZI, VDYT rakip |
| sektor_ABD.csv | sektör ayarı (Yahoo) | ABD | anlık | 1.416 | sembol, sektor, endustri | yok | bugünkü sınıf | FON_IZI, K38+ |
| **evren_disi_ABD.csv** | evren dışı (ETF / emtia fonu, 7 kayıt) | ABD | 30 Eki 2026 | **REPODA YOK** | sembol, neden, kaynak, tarih | — | — | COL_YOLU_ABD `cy_veri_yukle` (dosya yoksa main'den indirir, yoksa DURUR). `.gitignore` `*.csv` istisnasında yok; git geçmişinde hiç eklenmemiş. K55_EVREN_DISI.csv (arastirma_cikti/k55_dallanma) benzer liste. |
| cds_2022.csv | TR 5y CDS | TR | 2022-01-03 → | 1.229 gün | date, price | — | günlük kapanış | rejim.py, takip |
| temel_duz.csv | BIST temel (çeyreklik) | BIST | 2022+ | 10.116 satır | net kâr, satış, özkaynak, borç, nakit, açıklama günü | yok | 'aciklama' sütunu var | COL_v1 / takip (Actions) |
| v1_final_BIST.csv, yeni_BIST_2023.csv, kirilim_sonrasi_w.csv | Çöl Yolu olay listeleri | BIST | 2023-2026 | 4.927 / 1.698 / 710 | sembol, tarih, yön, clv … | yok | olay günü | Actions girdisi |
| takip_adaylar / pozisyonlar / kapanan.csv | üretim takip durumu | BIST | 2026-09+ | 7 / 3 / 14 | — | — | — | takip.py, gh_gunluk |
| kalibre_veri.csv, kalibre_etiketler.csv | göz kalibrasyonu | BIST | 2024-26 | 21.333 / 38 | OHLCV / etiket | yok | — | KALIBRE (Ç07) |
| veri_koru_gunluk.csv | veri koruma günlüğü | BIST | 2026-10 | 132 | — | — | — | veri_koru |
| goz_esle/*.csv, goz_formul*.json, tema_*.json, evren_ek_durum.json, K56/envanter_kaynak.json | ayar / ara çıktı | BIST | — | küçük | — | — | — | GOZ_ESLE, tema_*, K56 |
| arastirma_cikti/k60_veri/fiyat_kapsam.csv, evren_ay.csv, K60_SEC_ISTEK_LISTESI.csv | K60 kapsam tabloları | ABD | 2010-2026 | 4.755 / 200 / 1.916 | sembol, ilk, son, gün, bölünme … | — | — | K60, bu çalışma |

### 1b. islenmis-veri dalı (kalıcı; manifest sha256'lı; 212,8 MB) [SAYILDI]

Tek commit fce5d94 (2026-10-30). Açma: `git worktree add /tmp/iv origin/islenmis-veri` + `python FON_IZI.py vpac`. Bu konteynerde /tmp/iv, /tmp/veri, /tmp/veri2, /tmp/secfs, /tmp/pead açılmış durumda.

| yol | tür | pazar | aralık | hisse / kayıt | alanlar | çıkan | nokta-zaman | kullanan |
|---|---|---|---|---|---|---|---|---|
| veri/V_BIST.pkl | günlük OHLCV (bölünme / marj düzeltmeli) | BIST | 2015-06-01 → 2026-10-22 (357 hisse 2015-06'dan; BENIOKU '2016-09' yazıyor, eski) | 581; 1.272.889 satır | O, H, L, C, V | **YOK** (bugün işlem görenler) | düzeltme katsayısı indirme günündeki | FON_IZI K1+, IZ_KARNE, K57-K67, VDYT |
| veri/V_ABD.pkl | günlük OHLCV | ABD | 2015-06-01 → 2026-10-22 | 1.411; 3.435.100 | O, H, L, C, V | YOK | aynı | FON_IZI, K51-K59, K67 |
| veri/V_AVR.pkl | günlük OHLCV + Kur | Avrupa (STOXX 600 + FTSE 250) | 2015-01-01 → 2026-10-27 | 581; 1.646.914 | + Kur (EUR) | 1 seri erken bitiyor; liste bugünkü | aynı | K38+ (karar pazarı) |
| veri/G.pkl, oran.pkl, dol.pkl | KAP fon pozisyonu, bölünme oranı, dolaşım | BIST | 2023-01 → 2026-10-12 | 263.521 satır, 13.111 rapor, 549 fon | indeks, kod, nominal, değer, fon, ay, bilinme, ağırlık | — | 'bilinme' = rapor yayını | K25, K26, VDYT fon girişi |
| veri2/k34_yahoo.pkl | günlük OHLCV (nakdi biten ABD şirketleri, Yahoo) | ABD | 2020-10-01 → 2026-10-27 | 2.261; 2.829.071 | OHLCV | 18 seri 2026-06 öncesi bitiyor → batan yanlılığını AZALTMAZ | — | K34, K51, K54 |
| veri2/k34_bildirim.pkl | SEC finansal özeti (batanlar dahil) | ABD | 2021+ | 131.935 | adsh, cik, filed, form, nakit, ocf, pist, kod | **VAR** (kimlik + bilanço; fiyat yok) | 'filed' = başvuru günü | K34, K54 |
| veri2/k31_fin.pkl, k30_alim.pkl | nakit pisti; Form 4 açık piyasa alımı (özet) | ABD | 2021+ / 2016+ | 99.134 / 7.821 | — | kısmen | filed / başvuru | K30, K31 |
| veri2/k28_X_bist / abd.pkl | bilanço tepki tabloları | ikisi | 2016+ / 2022-12+ | 9.052 / 20.578 | ear, sürpriz, çeyrek | — | d0 = açıklama günü | K28, K41 |
| veri2/olcut_panel_AVR.pkl, k40_saatlik.pkl | ölçüt paneli; 4 endeks saatlik | AVR / endeks | son 730 gün (saatlik) | — | — | — | — | K38-K41 |
| secfs/fs_2021q1-2026q3 + company_tickers.json | SEC finansal tablo özütleri | ABD | 2021 → 2026Q3 | 23 çeyrek | gelir tablosu / bilanço kalemleri, adsh, filed | VAR (başvuranlar) | 'filed' güvenilir | K57, K59, K60 |
| pead/liste_bist(_2016_22), liste_abd | KAP Finansal Rapor listesi; Nasdaq takvimi | BIST / ABD | 2016-07 → 2026-10; 2022-12 → 2026-10 | 16.983 + 14.739; 65.474 | yayın saati; sembol, sürpriz, saat (%99 'time-not-supplied') | KAP çıkanları içerir | KAP saniyeli | K28, K62, VDYT |
| kap_iceriden/ | KAP Pay Alım Satım Bildirimi | BIST | 2022-07-01 → 2026-10-26 | 8.609 bildirim; 6.637 ayrıştırıldı | tarih, alım, satım, oranlar, görev | çıkanları içerir | KAP yayın saati | K27, VDYT |
| k34/k34_eski_kod.csv, k34_orneklem.csv | batanların eski kodu; Tiingo örneklemi (450) | ABD | 2021-26 | 1.303 / 450 | cik, adsh, kod, ad, borsa | **kimlik VAR, fiyat YOK** (Tiingo csv'leri lisans gereği dalda değil) | — | K34, K54 |
| k35/k35_sic.csv | SIC kodu (CIK → bugünkü) | ABD | anlık | 4.556 | — | — | bugünkü sınıf | K35, VDYT sektör |
| k36/surucu.pkl | emtia, kur, faiz, CDS | — | 2015-01 → 2026-10 (CDS 2022+) | 10 seri | — | — | günlük | K36, VDYT C olayı |
| avr/evren_avr_ham.csv | Avrupa evren listesi | AVR | 28 Eki 2026 | 692 | — | yok | bugünkü | K38 |
| k55/sec_ozet.json | **SEC başvuru geçmişi özeti (8-K madde kodları dahil)** | ABD | 1994 → 2026-10-30 | 3.262 CIK; 570.155 8-K (items dolu 570.153) | name, tickers, exchanges, sic, formerNames, form, date, items | 424 CIK bugün kodsuz | başvuru günü | K54, K55, K56; **VDYT kullanmadı** |
| k55/supported_tickers.csv | Tiingo sembol listesi (ham) | ABD + dünya | 1960'lar → 2026-10-29 | 109.165 kod (ABD borsa hissesi 16.591; 7.919'u çıkmış) | ticker, exchange, assetType, startDate, endDate | **kimlik + tarih VAR, fiyat YOK** | anlık görüntü | K54, EVREN2, bu çalışma |
| k55/sembol_cik.json, company_tickers.json | eşleme | ABD | 2026-10-30 | 3.267 / 10.429 | — | — | bugünkü | K54-K56 |

### 1c. kapfon-veri dalı (kalıcı; 229,7 MB) [SAYILDI manifest]

| yol | tür | aralık | kayıt | not |
|---|---|---|---|---|
| kapfon/liste.csv.gz | KAP 'Portföy Dağılım Raporu' listesi | Ara 2022 → 23 Eki 2026 | 45.740 rapor | yayın saati |
| kapfon/k9_pozisyon / islem / kontrol | ayrıştırılmış fon pozisyonları (ayrıştırıcı v1.5) | aynı | 23.102 rapor | G.pkl'in kaynağı |
| kapfon/metin.tar.xz.000-003 | 25.007 ham rapor metni (açılınca 2,3 GB) | aynı | — | kullanan: K9-K11, K25 |

### 1d. Bu konteynerin /tmp önbellekleri — **KALICI DEĞİL** (konteyner gidince silinir) [SAYILDI]

| klasör | boyut | içerik | aralık / sayı | çıkan kapsamı | kalıcı kopya | yeniden kurma | risk |
|---|---|---|---|---|---|---|---|
| /tmp/iv, /tmp/veri, /tmp/veri2, /tmp/secfs, /tmp/pead, /tmp/k57/pead | 204 + 302 + 168 + 33 + 1 MB | islenmis-veri açılmış hali | 1b | 1b | **VAR (dal)** | vpac | yok |
| **/tmp/k60_fiyat** | 1,3 GB | Yahoo günlük JSON (O, H, L, C, V, adjclose, bölünme, temettü) | 4.755 dosya; serisi olan 4.706 (K60 'fiyat' 4.678); 2010-01-04 → 2026-11-10; 1.970 hisse 2010 başından | **YOK** (2026-06 öncesi biten 4 seri) | **YOK** (yalnız manifest sha256 repoda) | `K60_veri.py indir_fiyat` ~23 dk; Yahoo geçmişi değişebilir (29 kırpık seri), bit-aynı olmaz | **YÜKSEK**: VDYT ABD, K60, K60-B, K64-K67 girdisi |
| **/tmp/k60_secframes** | 978 MB | SEC XBRL çerçeveleri 1.710 (28 kavram, 2009-2026) + **EDGAR üç aylık ana dizin 71 dosya (2009Q1-2026Q3, 18,7 mn satır)** | bütün başvuranlar | VAR (kimlik) | YOK | SEC'e yeniden istek, e-postalı User-Agent (Cemal'in izni) | **YÜKSEK** |
| **/tmp/k62_veri** | 74 MB | KAP Finansal Rapor listesi 2009-06+ (106.852 FR; 161.908 kayıt), İş Yatırım günlük kapanış / PD / hacim 715 hisse 2008-01-02 → 2026-08-31, mali tablo 716 | 92 kotasyondan çıkan dahil | **VAR (tek kaynak)** | YOK | `K62.py indir` ~66 dk (KAP ara sıra 429; İş Yatırım ucu resmî değil) | **YÜKSEK** |
| **/tmp/k67_yahoo** | 14 MB | Yahoo analist not günlüğü (1.400 hisse) + **bilanço takvimi (1.410 V_ABD hissesi, 87.171 satır, 1998-2027, saatli: 4 PM 36.554, 7 AM 16.575, 6 AM 12.994 …; EPS tahmin / gerçekleşen / sürpriz)** | yalnız bugün Yahoo'da olanlar | YOK | `K67.py indir`; takvim sayfası 100 satırla sınırlı, not günlüğü geriye dönük değişebilir | **YÜKSEK** (küçük, eşsiz) |
| /tmp/k64_bist_temel | 169 MB | İş Yatırım mali tablo, 581 hisse × 2014-2026 (7.553 json) | yaşayanlar | YOK | `K64.py`; İş Yatırım ucu | ORTA |
| /tmp/k66_finra | 369 MB | FINRA iki haftalık açık pozisyon 209 dosya | 2017-12-29 → 2026-08-31 | OTC + borsa, çıkanlar dahil | YOK (sha256 k66_indir.json'da) | FINRA CDN ücretsiz ~10 dk (2017-12 öncesi 403) | ORTA-DÜŞÜK |
| /tmp/k57b_fiyat | 628 MB | Yahoo günlük JSON 2020-01 → 2026-08 | 4.462 (BWMN, ROKU yalnız burada) | YOK | YOK | k60_fiyat çoğunu kapsar | DÜŞÜK |
| /tmp/secframes | 103 MB | SEC çerçeveleri 206 (2020+, K59) | — | — | YOK | k60_secframes kapsar | DÜŞÜK |
| /tmp/k63_ornek | 32 MB | K63 örnekleri: BIST bülten (thb, 2010-2026 örnek günler), Takasbank ÖPP, IEX, FINRA, demo yanıtları | — | — | YOK | ücretsiz, yeniden alınır | DÜŞÜK (bülten örneği bu rapordaki kanıt) |
| /tmp/av_pilot | 7,9 MB | Alpha Vantage demo yanıtları (AV_PILOT.md) | — | — | YOK | demo | DÜŞÜK |
| /tmp/k58_french, k60_french, k58_yahoo | <2 MB | Fama-French; SPY, XU100.IS | 1926+ / 1993+ | — | YOK | ücretsiz | DÜŞÜK |
| /tmp/vdyt | 754 MB | türetilmiş: fiyat_ABD.pkl (554 MB, k60'tan), EDGAR olay pkl (50 MB), kasa / wf bölge tabloları (152 MB, 280 dosya) | — | — | YOK | `VDYT.py` (saatler) | ORTA (VDYT grafik paketi bu tablolardan) |
| /tmp/k60_panel, /tmp/k64_ara | 983 MB + 0,3 MB | türetilmiş paneller | — | — | YOK | kod + girdi | DÜŞÜK |

Repo içinde git dışı (aynı risk): **87 girdi, 85 MB** (`.gitignore` `*.csv` ve `col_dis_bilgi/*.csv.gz`): k57_yeotk_profili 33 MB, vdyt/grafik 20 MB, col_dis_bilgi 18 MB (k62 / k62b / k64 / k66 / k67 olay ve hücre tabloları),
k60_kutuphane 11 MB, k58 1,5 MB, k59 0,8 MB, k60_veri 0,9 MB. Bunlar denetimde sayıları yeniden üretmenin girdisi.

### 1e. Google Drive — **[DRIVE] bu oturumda doğrulanmadı** (kaynak: CLAUDE.md, IZ_DEFTERI, COL_OZET §9.6-9.7, koddaki sabit yollar)

| konum | içerik | aralık | not / kullanan |
|---|---|---|---|
| MyDrive/col_tarayici/veri_1d_turkey.pkl | BIST günlük önbellek (kayit + veri), 583 sembol | 2023-06 → | üretim zinciri (COL_v1, takip); Actions'ta da önbellek |
| col_tarayici/veri_1d_america.pkl | ABD günlük önbellek | ? | FON_IZI FI_VERI_ABD varsayılanı |
| col_tarayici/veri_1d_turkey.pkl.yedek_bolunme_*, .yedek_20261008, arsiv/eski_ciktilar/…yedek_evren_20261008_0721 | ham / eski önbellek yedekleri | — | bolunme_onar, zincir_denetimi (yerinde kalmalı) |
| onbellek_2024_26(.pkl / _v3), onbellek_2023(_v3), onbellek_ABD.pkl, onbellek_ABD_2022_23.pkl (OB24, OB23, OBUS, OBUS21), onbellek_v2_*, arsiv/…onbellek_*.pkl.yedek_20261008_0913 | test önbellekleri | 2022-2026 | DENETIM, KALIBRE, OLCUM; Eylül OB24 / OB23 seti (n = 2064 / 820) tek kaydı yedekte |
| buyuk_col_kor_anahtar*.pkl, buyuk_col_olaylar.csv, buyuk_col_haftalik.pkl, kalibre_*, goz_*, kor_test/ | kör test / kalibrasyon | — | yerinde kalmalı |
| COLAB_VERILER/col_tarayici/kap_ozet (kap_20*.csv.gz / kap_ozet_tum.csv.gz) | **KAP bildirim özeti: tarih, saat, sembol, tür, konu_id (bütün konular)** | 2017 → 2026 | FON_IZI K8 (10 konu grubu), IZ_KARNE Ç15-Ç28, Ç61-Ç62; sözleşme tutarı / metin YOK |
| COLAB_VERILER/col_tarayici/kap_bildirimler.csv, fiyat_ozet, m1-m5 | KAP_ARSIV.py (3-4 Eki) çıktıları | 2017-26 | Ç15-Ç28 |
| COLAB_VERILER/col_tarayici/kapfon, kap_iceriden, pead, secfs, k36 | dalların Drive kopyaları | — | — |
| COLAB_VERILER/col_tarayici/sec | SEC çeyreklik Form 4 veri setleri ham zipler (repoya konmaz) | 2016-01 → 2026-03 | K30; satış dahil bütün işlemler |
| COLAB_VERILER/col_tarayici/k34 | K34 girdileri; **450 Tiingo csv'si Drive ad aramasında bulunamadı** (EVREN_SECENEKLERI, 11 Kas) | — | K34, K54 |
| COLAB_VERILER/col_tarayici/isy/temel_degerler.html | İş Yatırım fiili dolaşım | anlık | FON_IZI |
| COLAB_VERILER/col_tarayici/atlas*.csv, taban_serisi_izleme.csv, motor_karne.csv; IZ_DEFTERI.md tek kopyası | araştırma çıktıları | — | — |
| COLAB_VERILER/OUTPUT/COL_YOLU_ABD (veri/), OUTPUT/K55, OUTPUT/VDYT (VDYT_RAPOR.md, VDYT_raporlar.zip) | çıktılar | — | grafik paketi yüklenemedi (4,2 MB sınırı) |

---

## 2. Kalıcılık riski: neyin dala / Drive'a alınması gerekir

Yalnız bu konteynerde, kopyası olmayan veri: **~3,7 GB ham + ~1,7 GB türetilmiş + 85 MB repo çıktısı.** Öncelik sırası (dala alma ayrı iş; Cemal'in 'verileri repoya kaydet' izni islenmis-veri için var, Yahoo / İş Yatırım / SEC kamu verisi; Tiingo değil):

| # | veri | neden | tahmini paket (xz) | hedef |
|---|---|---|---|---|
| 1 | /tmp/k67_yahoo (takvim + not) | ABD'de tek saatli bilanço günü kaynağı (2002+) ve analist günlüğü; Yahoo geçmişi yeniden yazabilir; çok küçük | ~14 MB | islenmis-veri `k67/` |
| 2 | /tmp/k62_veri | kotasyondan çıkan 92 BIST hissesinin tek kapanış serisi; KAP FR listesi 2009+ | ~65 MB | islenmis-veri `k62/` |
| 3 | /tmp/k60_secframes (çerçeveler + EDGAR dizini) | yeniden indirme SEC e-postası ister; bu rapordaki kapsam ölçümünün girdisi | ~85 MB (örnek oran 0,085) | islenmis-veri `k60_sec/` |
| 4 | /tmp/k60_fiyat | VDYT / K60 ana ABD fiyatı; Yahoo değişir | ~150 MB (örnek oran 0,11) ya da sıkıştırılmış tablo | islenmis-veri `k60_fiyat/` (45 MB parçalar) |
| 5 | repo git dışı çıktıları (85 MB) | denetim yeniden üretimi | ~30-40 MB | Drive OUTPUT/ ya da dal |
| 6 | evren_disi_ABD.csv | kod durur | < 1 KB | main (`.gitignore` istisnası) — ana model işi |
| 7 | /tmp/k64_bist_temel, /tmp/k66_finra | yeniden indirilebilir (ücretsiz) | ~15 MB / ~95 MB | isteğe bağlı |
| — | /tmp/vdyt, k60_panel, k57b, secframes, k63, av_pilot, french | türetilmiş ya da başka kopya / ücretsiz | — | gerekmez |

---

## 3. VDYT eksikleri — gerçek durum (tam envantere göre)

Durum: **VAR** = elde, kullanılabilir; **KISMEN** = elde ama dönem / evren / alan eksik, ya da ücretsiz kaynak var ama indirilmedi; **GERÇEKTEN EKSİK** = ücretsiz ve erişilebilir kaynak yok.

| veri türü | pazar | VDYT dedi | gerçek durum | mevcut / ücretsiz kaynak | eksik aralık | engellediği VDYT analizi |
|---|---|---|---|---|---|---|
| OHLC 2015-06 öncesi ve kotasyondan çıkanlar | BIST | EKSİK (yalnız K62 kapanış) | **KISMEN — ücretsiz kaynak var, indirilmedi** | Borsa İstanbul günlük bülteni (thb): 2015-12-01'den CSV, açılış / en düşük / en yüksek / kapanış / hacim, sonradan çıkanlar dahil (2017-01-03 bülteninde K62'nin sonradan çıkan 10 hissesinden 9'u OHLC ile; 412 pay satırı) [SAYILDI]; 2005-2015 xls (içerik denenmedi) [RAPOR K63] | 2015-06 → 2015-11 (bülten CSV öncesi) ve 2008-2015 (xls ayrıştırılmalı) | T1 / T5 / mum ölçüleri BIST yanlılık kontrolünde |
| ABD kotasyondan çıkan / batan fiyatları | ABD | EKSİK | **GERÇEKTEN EKSİK** | kimlik + tarih var (Tiingo listesi 7.919 çıkmış kod; EDGAR; k34 eski kod; sec_ozet 8-K 1.03 / 25-NSE); fiyat yok. Yahoo / Stooq vermiyor (K34 sınaması), AV ücretsiz katman yalnız son 100 gün (AV_PILOT) | 2010 → 2026-06 (bölüm 4) | ABD sonuçlarının hepsi 'yaşayan evren' koşullu; aşağı genişlemeler eksik |
| KAP özel durum açıklamaları (sözleşme, ihale, ortaklık, sermaye artırımı kararı, yönetim, dava …) | BIST | EKSİK | **KISMEN** | Drive kap_ozet 2017-2026 (tarih, saat, sembol, tür, konu_id; bütün konular; FON_IZI K8'de 10 konu grubu kullanıldı) [DRIVE]; KAP API ücretsiz (K62'nin `byCriteria` ucu, sınıf süzgeciyle; FR sınıfı 451 pencere ~7 dk, 2009-06'ya iniyor) [RAPOR K62] | metin / tutar yok (ham bildirim sayfası ücretsiz, indirilmedi); 2009-2016 indirilmedi | B olaylarının türe göre ayrımı; BIST 'habersiz' kontrol grubunun temizliği |
| Genel kurul ve temettü / bedelsiz KARAR günleri | BIST | EKSİK | **KISMEN — ücretsiz** | aynı KAP ucu / kap_ozet konu kodları (genel kurul, kâr payı dağıtım bildirimleri) | indirilmedi; elde yalnız hak kullanım günü (K62) | planlı olayın önceden bilinme günü |
| 8-K madde kodları | ABD | EKSİK | **KISMEN VAR** | islenmis-veri k55/sec_ozet.json: 3.262 CIK, 570.155 8-K, madde kodlu (9.01 414.249; 2.02 153.618; 8.01 126.214; 7.01 119.901; 5.02 97.222; 1.01 82.665 …), 1994 → 2026-10 [SAYILDI]. Kapsam: V_ABD 1.403 / 1.406 CIK; k60 2.577 / 4.672 CIK (%55). SEC submissions JSON'da 'items' alanı ücretsiz (sec_indir.py hazır; SEC isteği Cemal'in e-posta izniyle) | k60'ın 2.095 CIK'i (indirilmedi) | 8-K içeriği (sözleşme / yönetim / satın alma); bilanço 8-K'sı tarih yakınlığı yerine madde 2.02 ile |
| Bilanço açıklama günü 2010 → 2022-11 | ABD | KISMEN (10-Q vekili) | **KISMEN VAR** | /tmp/k67_yahoo/takvim: 1.410 V_ABD hissesi, 87.171 satır, 1998-2027 (2010: 2.600, 2016: 3.470, 2022: 5.105 satır) [SAYILDI]; 8-K madde 2.02 günleri (sec_ozet); AV ↔ Yahoo 99 / 99 aynı gün, AV ↔ EDGAR 8-K 71 / 71 [RAPOR AV_PILOT]. k60'ın geri kalanı için K67 indirme kodu ücretsiz | k60'ın V_ABD dışı ~3.300 hissesi; Yahoo 100 satır sınırı (~25 yıl) | A planlı olay; 10-Q günü vekili kötü (bilanço → 10-Q medyan 8 gün) |
| Bilanço saati (Nasdaq %99 boş) | ABD | KISMEN | **KISMEN VAR** | Yahoo takvimi saatli (4 PM / 5 PM / 6 PM ≈ kapanış sonrası; 6-8 AM ≈ açılış öncesi) | V_ABD dışı | olay günü 0 / +1 ayrımı |
| CPI / istihdam yayın günleri | ABD | EKSİK (bls.gov 403) | **EKSİK, ücretli değil** | resmî ücretsiz: BLS takvim arşivi, FRED / ALFRED 'release dates' (CPI rid 10, Employment Situation rid 50). Bu konteynerden: bls.gov 403, fred / alfred zaman aşımı (2026-11-12 denemesi); federalreserve.gov erişilebilir. Colab'dan alınabilir; FRED API anahtar (kayıt) ister, sayfa indirmesi istemez [GENEL] | 2009 → 2026 | C makro günü (enflasyon / istihdam) |
| TÜİK enflasyon günü | BIST | EKSİK | **EKSİK, ücretli değil** | TÜİK yayın takvimi (data.tuik.gov.tr 302, tuik.gov.tr zaman aşımı bu konteynerden); kural: TÜFE ayın 3'ünde 10:00 (tatilde kayar) [GENEL] | 2015 → 2026 | C makro günü |
| Makro içerik / beklenti / sürpriz | ikisi | EKSİK | **GERÇEKTEN EKSİK (ABD); KISMEN (TR)** | ABD konsensüs anketleri ücretli / kurumsal [GENEL]; TR: TCMB Piyasa Katılımcıları Anketi ücretsiz (indirilmedi) [GENEL] | tamamı | 'sürpriz' etkisi |
| Sektör haberleri | ikisi | VERİ YOK | **GERÇEKTEN EKSİK** | hisse eşlemeli tarihsel haber ücretsiz yok; AV NEWS_SENTIMENT premium (bölüm 5); BIST hiçbir kaynakta yok | tamamı | C sektör haberi |
| Endeks giriş / çıkış | ikisi | EKSİK | **KISMEN — ücretsiz, indirilmedi** | BIST endeks dönem değişikliği duyuruları (Borsa İstanbul / KAP); S&P 500 değişiklik listeleri ve Russell yeniden yapılanma listeleri (kamuya açık) [GENEL] | tamamı | endeks gelişmesi olayı |
| Emtia / kur / faiz 2010-2014 | ikisi | EKSİK | **KISMEN — ücretsiz** | Yahoo vadeli serileri 2000'lerden; k36 2015'te kesilmiş [GENEL] | 2010-2014 | 2015 öncesi emtia şoku |
| İçeriden işlem 2022-07 öncesi (BIST); Form 4 yönü (ABD) | ikisi | EKSİK | **KISMEN** | BIST: KAP 'Pay Alım Satım Bildirimi' ücretsiz (fi_k27_liste; konu süzgeci 2016 öncesi dönmüyor); ABD: SEC Form 4 veri setleri 2016-01 → 2026-03 Drive sec/ [DRIVE] (satış dahil), k30 yalnız alım özeti | BIST 2016-2022-06; ABD 2010-2015 | B içeriden olayı |
| Fon raporları 2023 öncesi | BIST | EKSİK | **GERÇEKTEN EKSİK (doğrulanmadı)** | kapfon listesi Ara 2022'de başlıyor; KAP'ta daha eskisi var mı bakılmadı | 2015-2022 | fon girişi olayı |
| Gün içi hisse verisi | ikisi | EKSİK | **GERÇEKTEN EKSİK (tarihsel)** | ABD: Yahoo 1 saatlik son 730 gün; IEX HIST ücretsiz ama yalnız IEX (TOPS 2016-12, DEEP 2017-05; ~10 TB); Alpaca ücretsiz hesap (kayıt) 2016+. BIST: DataStore ücretli / fiyat belirsiz [RAPOR K63] | 2010-2024 (ABD), tamamı (BIST) | kırılımın gün içi sırası, KAP saatine tepki |
| Kod değişikliği / eski kod eşlemesi | ABD | EKSİK (beyan) | **KISMEN VAR** | sec_ozet formerNames + tickers (3.262), k34_eski_kod (1.303), Tiingo listesi start / end | k60'ın sec_ozet dışı CIK'leri | eski başvuruların eşlenmesi |

Ayrıca: **FINRA açık pozisyon VAR** (/tmp/k66_finra, 2017-12-29 → 2026-08-31, 209 dosya; kalıcı değil); **Reg SHO günlük açığa satış ücretsiz, indirilmedi** (2009-08+ borsa bazlı, 2018-08+ birleşik). VDYT bunları olay saymadı (doğru).

Gerçekten eksik olanların özeti: ABD batan fiyatı; hisse eşlemeli tarihsel haber (ikisi); ABD makro beklenti / sürpriz; tarihsel gün içi veri (BIST tümü, ABD büyük kısmı); BIST fon raporları 2023 öncesi (doğrulanmadı). BIST analist tahmini geçmişi de yok (VDYT listesinde değil, bölüm 5).

---

## 4. Kanıtlanmış fiyat kapsam açığı (Tiingo kararı için)

### 4a. ABD: EDGAR'a göre (yerel /tmp/k60_secframes/edgar_master_*, SEC'e istek yok) [SAYILDI]

Tanım: o yıl 10-Q (ya da 10-QT / 10-QSB, düzeltmeler dahil) veren CIK = faaliyetteki raporlayan şirket (ABS tröstleri 10-Q vermez). 'Bugün kodu yok' = company_tickers.json'da (2026-11) yok
(birleşen, batan, kayıttan çıkan; ama hiç borsada olmamış SEC kayıtlıları ve borç ihraççısı iştirakler de burada → **üst sınır**). k60 eşlemesi: 4.678 sembolün 4.672'si CIK'e eşlendi.

| yıl | 10-Q veren | bugün kodu yok | pay | k60 fiyatında | kodlu ama k60 dışı | o yıl son başvurusu, kodsuz |
|---|---|---|---|---|---|---|
| 2010 | 9.128 | 6.779 | %74 | 1.928 | 421 | 810 |
| 2012 | 8.399 | 5.894 | %70 | 2.056 | 449 | 765 |
| 2014 | 7.882 | 5.139 | %65 | 2.261 | 482 | 636 |
| 2016 | 7.160 | 4.178 | %58 | 2.472 | 510 | 621 |
| 2018 | 6.551 | 3.285 | %50 | 2.712 | 554 | 472 |
| 2020 | 6.239 | 2.613 | %42 | 3.030 | 596 | 336 |
| 2021 | 7.080 | 2.982 | %42 | 3.423 | 675 | 366 |
| 2022 | 7.113 | 2.817 | %40 | 3.570 | 726 | 636 |
| 2023 | 6.611 | 2.179 | %33 | 3.663 | 769 | 631 |
| 2024 | 6.150 | 1.543 | %25 | 3.768 | 839 | 471 |
| 2025 | 5.978 | 1.095 | %18 | 3.880 | 1.003 | 412 |
| 2026 (Q3'e kadar) | 5.885 | 696 | %12 | 3.956 | 1.233 | 696 |

Ara yıllar ve tam seri: `abd_kapsam.json`. 2010-2026 toplam: 10-Q veren tekil CIK 16.914; bugün kodu yok **11.514**.

Kodsuzların boyutu (son bilinen us-gaap Assets çerçevesi; boyut vekili, piyasa değeri değil):

| dönem | kodsuz (10-Q veren) | < 10 mn $ | 10-50 mn $ | 50-300 mn $ | 300 mn-2 mr $ | > 2 mr $ | XBRL yok | varlık ≥ 50 mn $ | k60 fiyatında (karşılaştırma) |
|---|---|---|---|---|---|---|---|---|---|
| 2016 (yıl) | 4.178 | 1.343 | 403 | 547 | 828 | 891 | 166 | — | 2.472 |
| 2020 (yıl) | 2.613 | 641 | 270 | 442 | 549 | 627 | 84 | — | 3.030 |
| 2024 (yıl) | 1.543 | 363 | 204 | 226 | 307 | 399 | 44 | — | 3.768 |
| K60 KEŞİF 2016-21 | 5.885 | | | | | | | 3.249 | 3.453 |
| K60 DOĞRULAMA 2022-23 | 2.949 | | | | | | | 1.757 | 3.678 |
| K60 KASA 2024-26 | 1.726 | | | | | | | 1.022 | 4.040 |
| 2010-2026 tekil | 11.514 | 3.527 | 1.080 | 1.704 | 1.989 | 1.427 | 1.787 | — | 4.672 |

'> 2 mr $' kodsuzların önemli kısmı borsada hiç olmamış iştirak / borç ihraççısıdır (kamu hizmeti iştirakleri, sigorta, LP); küçük / mikro (< 300 mn $ varlık) kodsuzlar yıl başına
yaklaşık yarıdır (2016: 2.293 / 4.178).

### 4b. ABD: Tiingo listesine göre borsada işlem görenler (k55/supported_tickers.csv, 2026-10-29 görüntüsü) [SAYILDI]

Süzgeç: NYSE / NASDAQ / AMEX / NYSE MKT / ARCA / BATS, assetType Stock, USD, kod 1-5 harf (5 harfli W / U / R / Z sonekleri atıldı): 11.789 kod. 'Sonradan çıkan' = endDate < 2026-06-01.

| yıl | Tiingo aktif kod | sonradan çıkan | pay | k60'ta aktif | k60 / Tiingo aktif | o yıl çıkan |
|---|---|---|---|---|---|---|
| 2010 | 4.301 | 1.975 | %46 | 2.064 | %48 | 45 |
| 2013 | 4.926 | 2.290 | %46 | 2.341 | %48 | 140 |
| 2016 | 5.600 | 2.454 | %44 | 2.706 | %48 | 333 |
| 2017 | 5.663 | 2.303 | %41 | 2.847 | %50 | 431 |
| 2018 | 5.605 | 2.026 | %36 | 3.025 | %54 | 443 |
| 2019 | 5.493 | 1.702 | %31 | 3.177 | %58 | 308 |
| 2020 | 5.709 | 1.597 | %28 | 3.425 | %60 | 300 |
| 2021 | 6.568 | 1.861 | %28 | 3.866 | %59 | 414 |
| 2022 | 6.501 | 1.588 | %24 | 4.009 | %62 | 477 |
| 2023 | 6.307 | 1.176 | %19 | 4.146 | %66 | 526 |
| 2024 | 6.194 | 707 | %11 | 4.341 | %70 | 306 |
| 2025 | 6.525 | 441 | %7 | 4.549 | %70 | 281 |

Notlar: Tiingo 'Stock' sınıfında SPAC, ADR, kapalı uçlu fon da var (pay üst sınıra yakın). Tiingo'nun 2010-2014 çıkışları azdır (yılda 45-150) ama EDGAR'da aynı yıllarda son başvurusunu
yapıp kodsuz kalan 640-860 şirket var: **Tiingo 2010-2014 çıkışlarını eksik kapsıyor** (kod yeniden kullanımı ya da liste eksikliği; 258 çıkmış Tiingo kodu bugün başka bir k60 hissesinin kodu).
K34'te 1.303 kodsuz şirketin 997'si işlem görüyordu, 824'ü Tiingo'da eşleşti (%83) [RAPOR EVREN_SECENEKLERI]. K54 sınıflaması: 266 çıkışın 159'u birleşme, 79 belirsiz, 19 iflas,
9 kod yeniden kullanımı [RAPOR K54] — çıkışların çoğu birleşmedir (son fiyat ≈ anlaşma bedeli, yanlılığı küçük); yanlılık iflas / belirsiz kısmından gelir.

**Hangi sonuçları hangi yönde yanlı yapabilir:**
- K60 R2 olasılık tablosu ve DÜRÜSTLÜK KURALI taban oranları: −%50 olasılığı (taban %6-7, oynak havuzda %17-21) **olduğundan düşük**, +%100 (taban %4-7) ve 3 yılda 10x (~%1)
  **olduğundan yüksek** (pay yaşayanlardan, payda batanlarsız). Büyüklük ölçülemedi; KEŞİF döneminde Tiingo aktif evreninin %28-44'ü eksik.
- K60-B 'koruma' bulgusu (kârlı / seyreltmeyen hisselerde yarıya inme 0,6-0,8 kat): batanlar kârsız / seyrelten uca yığıldığı için karşılaştırma grubunun −%50 olasılığı eksik ölçülüyor;
  düzeltme büyük olasılıkla korumayı **güçlendirir** (yön kesin değil, ölçülmedi).
- Küçüklük, düşük fiyat, sıkıntı, oynaklık sinyalleri: en açık (K34: küçüklük etkisi batanlarla üçte bire iniyor). Momentum alım bacağı orta, kârlılık / PEAD düşük (EVREN_SECENEKLERI §4).
- VDYT ABD: sıkışmadan sonra batan / çıkan şirketlerin aşağı genişlemeleri ve son düşüşleri yok → 'yön' ve 'aşağı kırılım' sonuçları yukarı yanlı; genişleme tahmini (Motor 1) daha az etkilenir.
- Ölçülen etki küçük: K54'te delist bandı P1 / P2'yi 4. ondalıkta oynatmadı; K51 sonuçları evren düzeltmesinde değişmedi (K56 envanteri). Yanlılık 'yeni iz' bulduracak türden değil;
  asıl etkisi taban oranlarını ve kayıp olasılığını düzeltmek (gerçek para modülünün risk sayıları).

### 4c. BIST [SAYILDI]

- K62 İş Yatırım: 972 aday kod (KAP finansal rapor kodlarından), 715 dolu; **92 kotasyondan çıkan** (çıkış yılı 2009 2, 2011 1, 2012 3, 2013 6, 2014 9, 2015 15, 2016 12, 2017 7,
  2018 10, 2019 6, 2020 17, 2021 1, 2022 1, 2026 2); 64'ünün son günü 2015-06 sonrası (VDYT dönemi). **Hiçbiri V_BIST'te yok.** Yaşayan 623 K62 hissesinin 43'ü de V_BIST'te yok
  (AAGYO, ECOGR, MEYSU …; yeni halka arz / kapsam farkı); V_BIST'in 1 hissesi (DOCO) K62'de boş.
- Sonradan çıkan payı (K62'de o yıl aktif olanlar içinde): 2010 70 / 338 (%21), 2013 83 / 425 (%20), 2016 56 / 421 (%13), 2019 27 / 411 (%7), 2022 3 / 488, 2023-25 2 / 543-595 (< %1).
- Çıkanlar küçük: medyan günlük hacim 0,14 mn $ (yaşayanlar 1,19 mn $).
- OHLC: K62'de yalnız kapanış. Çıkanların OHLC'si Borsa İstanbul günlük bülteninde ücretsiz (2015-12+ CSV; 2017-01-03 örneğinde 10 çıkmış koddan 9'u, örn. MEMSA, AKSEL, ADNAC, TRKCM, ANACM, KIPA, DENIZ, ADANA, PIMAS).
  **BIST'te ücretli veri gerekmez.**

### 4d. Kalite açıkları [SAYILDI]

| kaynak | satır | H = L gün (hisse) | hacim ≤ 0 gün (hisse) | OHLC tutarsız | |günlük getiri| > %50 | not |
|---|---|---|---|---|---|---|
| V_BIST | 1.272.889 | 49.371 (562) — VDYT ile aynı | 26.149 (500) — aynı | 30 satır (VDYT 29) | 0 (> %21 de 0) | K62 kapanışıyla günlük getiri farkı > 5 puan 3.568 gün (%0,29, 467 hisse), > 20 puan 91 gün (çoğu V_BIST'te 0, K62'de ±%20-31: eksik / dolgu gün ya da düzeltme farkı) |
| V_ABD | 3.435.100 | 30.821 (227) | 20.960 (179) | 91 (2026-08-31 sonrası; kesikte 0) | 840 (292 hisse) | — |
| V_AVR | 1.646.914 | 12.777 | 5.429 | **13.622 satır (362 hisse)** | 21 | açılış H-L dışında; Avrupa çalışmalarında mum ölçüsü öncesi düzeltilmeli |
| k60_fiyat | 12.997.918 (≤ 2026-08-31) | 1.208.967 (%9,3; 871.838'i hacim 0) | 1.010.577 | 443 | 34.302; 'uygun' satırda (önceki kapanış ≥ 2 $, hacim > 0) 8.425 | sıçra-geri dön (ertesi gün tersine; veri hatası tipi) uygun satırda 1.160 / 10,8 mn; kırpık seri 29 [RAPOR K60] |
| k34_yahoo | 2.829.071 | 145.670 | 112.922 | 1.677 | 5.797 | nakdi biten küçükler |

Değerlendirme: H = L ve hacim 0 günleri gerçek işlemsizliktir (küçük hisse), veri hatası değildir; VDYT bunları atıyor. Tek günlük hata payı küçük (k60 uygun satırlarda %0,01).
Yahoo'nun düzeltme katsayıları indirme günündeki haliyle (geriye dönük değişir) ve ham fiyat yok: Tiingo ham + düzeltilmiş verir, ama bu bir kalite açığı olarak sonuç değiştirdiği gösterilmedi.
**Kalite açığı: KÜÇÜK, Tiingo gerekçesi değil.**

### 4e. Sonuç

| pazar | kanıtlanmış açık | büyüklük | etkileyebileceği sonuç | ücretsiz kapatma |
|---|---|---|---|---|
| ABD kapsam | **VAR** | KEŞİF yıllarında borsa evreninin %28-46'sı, KASA'da %7-11'i sonradan çıkıyor; k60'ta 0 çıkan seri | taban oranları (−%50 düşük, +%100 / 10x yüksek), küçüklük / sıkıntı sinyalleri, VDYT yön | Tiingo ücretsiz katman (mevcut hesap; 500 sembol / ay: 3.342 + 450 isim ≈ 8 ay); EDGAR + 8-K 1.03 / 25-NSE ile 'en kötü durum bandı' (fiyatsız) |
| BIST kapsam | VAR, küçük | 2016'da %13, 2019'da %7, 2022+ < %1 | VDYT BIST OHLC yalnız yaşayanlarla | evet: K62 kapanış (elde) + Borsa bülteni OHLC (ücretsiz) |
| kalite (ikisi) | küçük | yukarıdaki tablo | tek tük uç değer | mevcut temizlik kuralları |

**Tiingo'yu yeniden değerlendirme gerekçesi: VAR (ABD kapsam).** Satın alma (Power 30 $ / ay) gerekçesi yok: ücretsiz katman aynı veriyi yavaş verir ve beklenen katkı (yeni iz) düşük;
asıl kazanç gerçek para modülünün kayıp olasılıklarının dürüstleşmesidir. Karar Cemal'in.

---

## 5. Ücretli veri karar tablosu

Fiyat / kapsam bilgisi: K63_VERI_ERISIM.md (11 Kas), EVREN_SECENEKLERI.md (11 Kas), AV_PILOT.md (12 Kas). Yeni kayıt / satın alma yok. Güç notu: K58'e göre olay cetveli δ +%2'de
n ≤ 300 iken en çok %11 güçle görür; portföy cetveli (aylık üst %10, NW t > 2) kalibre. Ek veriyle küçük etkileri yakalama gücü sınırlıdır.

| Eksik veri türü | Mevcut kaynak | Eksik tarih aralığı | Sağlayıcı bu açığı kapatıyor mu (evet / kısmen / hayır; neden) | Maliyet (kaynak ve güven düzeyiyle) | Beklenen araştırma katkısı (hangi test, ne kadar güç; dürüst) |
|---|---|---|---|---|---|
| ABD batan / kotasyondan çıkan şirket fiyatları (Tiingo) | k60_fiyat, V_ABD, k34_yahoo: yalnız yaşayanlar (çıkan seri ~0); kimlik + tarih: Tiingo listesi (7.919 çıkmış kod), EDGAR dizini, k34 eski kod, sec_ozet (8-K 1.03, 25-NSE); 450 Tiingo csv'si Drive'da bulunamadı | 2010 → 2026-06; KEŞİF 2016-21'de borsa evreninin %28-44'ü, DOĞRULAMA %19-24, KASA %7-11 | **Kısmen-evet.** 2016+ iyi (K34: işlem gören kodsuzların %83'ü eşleşti); 2010-2014 çıkışları listede az (yılda 45-150 vs EDGAR 640-860) → eksik; OTC yok; birleşme / iflas ayrımı ayrıca SEC'ten | Ücretsiz katman **0 $** (Cemal'in mevcut hesabı; 50 istek / saat, 500 sembol / ay) [LİSTE, EVREN_SECENEKLERI]; Power **30 $ / ay** tek ay yeter (10.000 istek / saat) [LİSTE]. Lisans: yalnız iç kullanım, repoya konmaz | K60 R1 / R2 ve K59 yeniden koşusu, VDYT ABD yön, 10x / −%50 taban oranları. Yön kesin (taban oranları düzelir), büyüklük belirsiz. K54'te delist bandı sonuçları 4. ondalıkta oynatmadı → **yeni iz bulma beklentisi düşük; değeri risk sayılarını dürüstleştirmek.** Önce ücretsiz katman. |
| ABD EPS revizyonu (Alpha Vantage / EODHD) | Yahoo analist not günlüğü 2011-12+ (tavsiye + hedef fiyat; /tmp/k67_yahoo 1.400 hisse, K52 310.568 kayıt); Yahoo takvimi EPS tahmin / gerçekleşen / sürpriz (1.410 hisse, 2002+); EPS konsensüs revizyonu YOK | 7 / 30 / 60 / 90 gün önceki konsensüs: 2017-06 öncesi hiçbir uygun kaynakta yok; 2017-06 → bugün elde yok | **Kısmen.** AV EARNINGS_ESTIMATES ve EODHD Earnings::Trend 2017-06+, çeyrek başına bir donmuş görüntü; **görüntü günü dosyada yok** (sızıntı riski; IBM'de 38 kapanmış çeyreğin 27'si bilanço gününe yakın donmuş); 'aşağı revizyon' alanları %45-60 dolu; BIST: AV'de yok, EODHD'de doğrulanamadı | AV ücretsiz 25 istek / gün (anahtar kaydı gerekir; 4.700 hisse = 188 gün) [LİSTE]; AV **49,99 $ / ay** (≈ 63 dk) [LİSTE]; EODHD Fundamentals **59,99 $ / ay** [LİSTE] | K67 (revizyon, hedef fiyat) İZ DEĞİL; EPS revizyon momentumu bilinen ama büyük hisselerde zayıflamış etki [GENEL]. Test: K60 R2 olasılık tablosu + çöl ek bilgi, 2017-2026 (KEŞİF kısa). Güç düşük-orta. **Önce ücretsiz 25 hisselik pilot** (görüntü günü sınaması); ücretli 1 ay ancak pilot temizse. |
| ABD haber ve duyarlılık (AV NEWS_SENTIMENT; ayrı pilot sürüyor, yalnız bilinen bilgi) | yok. Vekil: 8-K madde kodları (sec_ozet; k60 CIK'lerinin %55'i), EDGAR form türleri | tamamı (haberli / habersiz ayrımı) | **Belirsiz / kısmen.** Uç premium (belge, 12 Kas); demo örneğinde en eski haber 2026-07-03 → arşiv derinliği ölçülemedi; skor kara kutu ve sonradan üretilmiş olabilir (nokta-zaman değil); ilgi skoru şişkin (50 haberin 26'sı konu dışı); BIST yok | AV **49,99 $ / ay** (1 ay ≈ 3-5 saat indirme) [LİSTE + DENENDİ demo, AV_PILOT]; Massive + Benzinga 99 $ / ay (analist notları; haber ayrı) [LİSTE K63] | VDYT K1 haberli / habersiz (ABD), E1 / E2 pencereleri. 8-K madde kodlarıyla aynı ayrım ücretsiz yapılabilir. Arşiv 2022 öncesine inmiyorsa VDYT KEŞİF dönemini kapsamaz. **Katkı düşük; önce 8-K ile ücretsiz deneme.** |
| Ödünç ücreti (IBorrowDesk) — **VDYT dışı, ayrı hipotez** | FINRA açık pozisyon 2017-12+ (/tmp/k66_finra; K66 İZ DEĞİL); Reg SHO günlük ücretsiz (indirilmedi); BIST: Takasbank ÖPP 2008+ ücretsiz (günde 35-90 kıymet) | ABD ödünç ücreti / bulunabilirlik: tamamı | **Evet (ABD, 2015-07+ günlük, IBKR ücret / iade / adet).** Kullanım oranı yok (kurumsal); yalnız IBKR havuzu | **29 $ / ay, 5.000 birim** (1 birim = 1 hisse × 365 gün; tüm evren × 2017-26 ≈ 47.000 birim; ek paket fiyatı okunamadı) [DENENDİ /coverage + LİSTE llms.txt, K63] | Ayrı hipotez (açığa satış baskısı, ödünç bulunabilirliği). K66'da açık pozisyon çöle ek bilgi vermedi → ücretin ek katkısı belirsiz. VDYT'ye katkı yok. |
| Emir defteri / emir akışı | ABD: IEX HIST ücretsiz (TOPS 2016-12, DEEP 2017-05; yalnız IEX borsası; ~10 TB) [DENENDİ]; günlük OHLCV. BIST: günlük bülten (VWAP, seans hacimleri, sözleşme sayısı) ücretsiz 2015-12+ | ABD tüm borsalar kotasyon / işlem: tamamı; BIST kademe / işlem: tamamı | ABD: **kısmen** — Alpaca ücretsiz hesap (kayıt) 2016+ işlem + kotasyon; Databento emir bazında ITCH 2018-05+; Massive işlem (10 yıl) / kotasyon (20+ yıl). BIST: **hayır / belirsiz** (DataStore fiyat sayfası 503) | IEX 0 $; Alpaca 0 $ (kayıt); Databento 125 $ kredi + kullanım (GB fiyatı doğrulanmadı) [LİSTE / İKİNCİL]; Massive 79 / 199 $ / ay [LİSTE / İKİNCİL]; BIST DataStore belirsiz [İKİNCİL] | OFI / işaretli işlem dengesizliği çöl ve VDYT kırılımında. Veri çok büyük, küçük hisselerde IEX payı az; BIST'te hesaplanamaz. **Güç / maliyet en zayıf; önce IEX DEEP 20 günlük pilot (ücretsiz).** |
| BIST KAP özel durum açıklamaları | Drive kap_ozet 2017-26 (konu kodlu, saatli) [DRIVE]; KAP FR listesi 2009+; içeriden 2022-07+; fon raporları | ÖDA 2009-2016 (indirilmedi); bildirim metni / tutar (indirilmedi) | **Ücretli sağlayıcı gerekmez: KAP API ücretsiz** (K62'nin ucu; sınıf süzgeciyle 2009'a iniyor, ara sıra 429); metin KAP bildirim sayfasında ücretsiz. AV / diğerleri BIST'i kapsamıyor | **0 $** [RAPOR K62, DENENDİ FR sınıfıyla] | B olaylarının türe göre ayrımı, BIST 'habersiz' kontrolünün temizliği (VDYT). BIST bilgi hücresi (karar pazarı değil) → karar etkisi sınırlı. |
| BIST analist tahmini (ücretli kaynaklar) | yalnız bugün: İş Yatırım takip listesi 54 hisse [DENENDİ, K63] | tamamı (tarihsel seri yok) | **Hayır / doğrulanamadı.** EODHD'de BIST Trend alanı doğrulanamadı; Matriks / Fintables / Foreks tarihsel toplu indirme bulunamadı; I/B/E/S, FactSet, Bloomberg kurumsal. Yapısal sınır: aracı kurum kapsamı ~50-100 büyük hisse, çöl evreninin çoğunda analist yok | EODHD 59,99 $ / ay [LİSTE]; Fintables 149-299 TL / ay, Matriks 300-980 TL / ay [İKİNCİL]; kurumsal fiyat yok | K62'de SUEAF 'VERİ YOK'. Küçük hisse kapsamı olmadığı için **katkı düşük**. |

Ek (VDYT eksiklerinden ücretli olmayanlar, karar gerektirmez): BIST OHLC çıkanlar (Borsa bülteni 0 $), ABD bilanço günü / saati (Yahoo takvimi K67 kodu, 0 $), 8-K madde kodları k60'ın kalanı
(SEC submissions, 0 $, mevcut e-posta izni), CPI / istihdam / TÜİK takvimi (resmî sayfalar, 0 $; Colab'dan), emtia 2010-14 (Yahoo, 0 $), endeks değişiklikleri (resmî duyurular, 0 $).

---

## 6. VDYT envanterine düzeltmeler / notlar

- k34_yahoo VDYT'de '-' (okunamamış): 2.261 hisse, 2020-10-01 → 2026-10-27, 2026-06 öncesi biten 18 → delist yanlılığını azaltmaz (VDYT'nin vardığı sonuç doğru).
- k60_fiyat 'fiyatlı 4.678' (K60 durum) ile JSON'da satırı olan 4.706 farkı: 28 seri yalnız 2026-08-31 sonrası ya da kırpık.
- V_BIST başlangıcı 2015-06-01 (BENIOKU '2016-09' eski). V_BIST kalite sayıları (H = L 49.371, hacim 0 26.149) bağımsız sayımla aynı; OHLC tutarsız 30 (VDYT 29; tolerans farkı).
- VDYT 'ABD 8-K madde kodu YOK', 'bilanço günü 2010-2022 vekil', 'Nasdaq saati' maddeleri için elde kaynak vardı (k55/sec_ozet, /tmp/k67_yahoo); VDYT bunları kullanmadı.
- VDYT 'KAP ÖDA listesi inmedi': Drive kap_ozet (2017-26) projenin eski çalışmalarında (Ç15-Ç28, FON_IZI K8) kullanıldı; bu oturumda görülemedi.
