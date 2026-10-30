# islenmis-veri — Çöl Yolu işlenmiş veri paketi (main'e birleştirilmez)

Cemal'in izniyle (26 Ekim 2026), KAP paketi (kapfon-veri) gibi ayrı dal. Yeni oturum veriyi yeniden kurmasın diye.

İçerik (veri/, xz + 45 MB parçalar, manifest.json içinde boy ve sha256):
- V_BIST.pkl: BIST günlük fiyat sözlüğü (fi_k1_veri çıktısı, bölünme/marj düzeltmeli), 2016-09 → 2026-10
- V_ABD.pkl: ABD günlük fiyat sözlüğü (1.411 hisse), 2015-06 → 2026-10-22
- G.pkl, oran.pkl, dol.pkl: K25 fon payı tabloları (KAP raporlu fon pozisyonları, bölünme oranı, dolaşım)

Açma (repo kökünde, main dalındaki FON_IZI.py ile):
    git fetch origin islenmis-veri && git worktree add /tmp/iv origin/islenmis-veri
    python FON_IZI.py vpac /tmp/iv/veri /tmp/veri

Sonra sürücülere V_hazir olarak verilir, ör. fon_izi_k26(A, {"BIST": pickle.load(open("/tmp/veri/V_BIST.pkl","rb")), "ABD": ...}).
Her parça sha256 ile doğrulanır; bozuk ya da eksik parçada açma durur.

kap_iceriden/ (26 Ekim 2026, K27): KAP 'Pay Alım Satım Bildirimi' listesi 2022-07 -> 2026-10 (liste.csv.gz), ayrıştırılmış işlem
satırları (islem.csv.gz; tablo + MKK PDF) ve ayrıştırılamayan bildirim numaraları (bos.txt). FI_KAPIC bu klasöre (liste.csv açılarak)
verilirse fi_k27_indir yalnız yeni bildirimleri indirir.

pead/ (27 Ekim 2026, K28): BIST KAP 'Finansal Rapor' listesi 2022-07 -> 2026-10 ve 2016-07 -> 2022-12, ABD Nasdaq bilanço takvimi
2022-12 -> 2026-10 (sembol, analist sürprizi, saat). FI_PEAD bu klasöre (dosyalar açılarak) verilirse fon_izi_k28(indir=False) koşar.

## Genişletme (28 Ekim 2026, Cemal: 'verileri repoya kaydet')
- veri/: V_AVR.pkl eklendi (Avrupa, STOXX Europe 600 + FTSE 250, 581 hisse, Yahoo, 2015-01 → 2026-10; Londra peni / sterlin 100x
  geçişleri düzeltildi; `Kur` sütunu = yerel para → EUR, yalnız likidite için). Karar pazarları artık ABD + AVR (CLAUDE.md, 28 Ekim).
- veri2/ (xz paket, `python FON_IZI.py vpac /tmp/iv/veri2 /tmp/veri2`): k34_yahoo.pkl (nakdi biten 2.246 ABD şirketi, Yahoo),
  k34_bildirim.pkl (SEC finansal özeti, batanlar dahil), k31_fin.pkl, k30_alim.pkl (Form 4 açık piyasa alımları, özet), k28_X_bist / abd
  (bilanço tepkileri), olcut_panel_AVR.pkl, k40_saatlik.pkl (S&P / Euro Stoxx 50 / DAX / FTSE 1 saatlik, son 730 gün). 28 Ekim denetim
  düzeltmeleri sonrası V_AVR (sterlin Kur) ve panel yenilendi.
- secfs/: SEC finansal tablo veri seti özütleri 2021q1-2026q3 (fs_*.csv.gz) + company_tickers.json → FI_SECFS bu klasöre verilir.
- k34/: k34_eski_kod.csv (batan şirketlerin SEC kapak sayfasından eski kodu), k34_orneklem.csv (Tiingo örneklemi, 450).
- k35/: k35_sic.csv (SIC kodları). k36/: surucu.pkl (emtia, kur, faiz, CDS serileri). avr/: evren_avr_ham.csv (Avrupa evren listesi).
- Tiingo fiyatları (batan şirketler, 450 csv) lisans gereği repoya KONMAZ; anahtar .env TIINGO_TOKEN, `fi_k34_tiingo_indir` yeniden indirir.
- SEC Form 4 ham zipleri (sec/) repoya konmaz (27 Ekim kuralı), `fi_k30_indir` ile iner.

## K55 ekleri (30 Ekim 2026, Cemal'in Faz 0 onayı: 'SEC özeti ve Tiingo listesi islenmis-veri altında, sürümlü')
- k55/: `python -c "from K55 import veri_paket; veri_paket.ac('/tmp/iv/k55', '/tmp/k55')"` (repo kökünde, main dalındaki K55/ paketiyle). manifest.json her
  dosya için kaynak, indirme tarihi, veri dönemi, sürüm, orijinal sha256, işleme kodu sürümü ve tür (ham / işlenmiş) tutar; açarken parça ve
  dosya sha256'ları doğrulanır, tutmazsa durur. İçerik: sec_ozet.json (SEC başvuru geçmişi özeti, 3.262 CIK, işlenmiş; ham JSON'lar
  saklanmadı, sec_indir.py ile yeniden üretilir, e-posta yalnız SEC_EPOSTA ortam değişkeninden), supported_tickers.csv (Tiingo sembol listesi, ham),
  sembol_cik.json (işlenmiş), company_tickers.json (SEC, ham). Her oturumda yeniden indirme yok; sürüm doğrulanmadan kullanılmaz.
