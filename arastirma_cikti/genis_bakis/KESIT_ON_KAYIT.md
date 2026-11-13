# GENİŞ KESİT ÖN KAYDI (ölçümden önce)

GENIS_KESIT v1.0 (genis_kesit_20261113): çökmüş 64 BIST hissesi, 31.10'da bilinen özellik vs 1-13 Kasım dönüşü (kesit, ön kayıtlı). Yazılma 2026-11-13 13:08:54 UTC. Bu dosya git'e işlenmeden `python GENIS_KESIT.py kos` çalışmaz (mühür kapısı).

## Soru

Fon krizinde %80+ düşmüş 64 BIST hissesinde 31.10.2026'da BİLİNEN hangi özellik 1-13 Kasım dönüşünün büyüklüğünü önceden gösteriyordu? Kesit, n = 64, açıklayıcı (kural değil). Geleceğe bakma yok: her açıklayıcı yalnız <= 31.10.2026 bilgisiyle.

## Tanımlar, test ve karar cümlesi (GK_ESIK, değişmez)

```json
{
 "agac": {
  "bolme": "Gini; aday eşik = ardışık farklı değerlerin ortası",
  "degisken": "SINANAN açıklayıcılar içinde |rho_Y1| en büyük 2 (her LOO katında eğitim kümesinde yeniden seçilir)",
  "derinlik": 2,
  "eksik": "eğitim medyanıyla doldurulur",
  "hedef": "Y1 >= medyan(Y1) -> 1, değilse 0",
  "loo": "64 kat: seçim + ağaç 63 hissede, tahmin dışarıdaki 1 hissede; LOO doğruluk ve taban (%50 civarı)",
  "not": "YALNIZ AÇIKLAMA; ağaç kural değildir",
  "yaprak_min": 5
 },
 "col4": {
  "T5": "fon payı ilk %5 tarihi = en erken: (a) FON_IZI.fi_k25_pay_tablo'da pay >= 0,05 olan ilk rapor ayının İLK günü (pay o ay sonunda >= %5; alış ay içinde olabilir); (b) KAP geçmişinde (2024-01-01 - 2026-08-31) yayımlayanı portföy yönetim şirketi olan 'Pay Alım Satım Bildirimi'nde (ilgili kodlarda hisse) mevzuat alıntısı dışında '%5' ardından 'ulaş' / 'aşmış' / 'aşarak' / 'üzerine' geçiyorsa (yukarı geçiş) metindeki ilk işlem tarihi (yoksa yayın günü)",
  "hisseler": [
   "TEHOL",
   "KTLEV",
   "DSTKF",
   "BINBN"
  ],
  "not": "Ç97 (fon girmeyen eşlerde çöl sıklığı: ilişkisiz) tekrar edilmez; yalnız 4 hisse için tarih tablosu (BİLGİ)",
  "olcu": "her gün t: COL_v1.col_olc(fiyat <= t) çöl kutusu (tespit) ve GECER; AL kırılımı = col_olc(fiyat <= t-1) kutusu var ve C_t > tavan x COL_v1.AL_PAY; K24 = FON_IZI.fi_k24_tara(fiyat < T5) 'kural' günleri",
  "pencere": 120,
  "pencere_tanim": "T5'ten ÖNCEKİ 120 işlem günü (kendi barları, T5 hariç)"
 },
 "isaret_beklenen": "yön ön kayıtta beklenmez (iki yönlü test)",
 "kesim": "2026-10-31",
 "kesim_tanim": "BİLGİ KESİMİ 31.10.2026 23:59 (TR). Fiyat: tarihi <= 31.10 olan son bar (30.10.2026 Cuma kapanışı; 29.10 tatil). KAP: yayın zamanı <= 31.10.2026 23:59. Bilanço: açıklama tarihi <= 31.10. Fon raporu: bilinme <= 31.10. Bu tarihten sonraki hiçbir bilgi X'e girmez.",
 "orneklem": {
  "kaynak": "/tmp/tavan/canli_cokmus.csv (TAVAN_SERISI canli, 13.11.2026)",
  "kural": "cokmus == True: 1 Haz - 31 Ağu 2026 en yüksek kapanıştan 1 Eyl 2026 sonrası en düşük kapanışa düşüş <= -%80, tepe sonrası veri kırığı yok",
  "n": 64
 },
 "sinir": "n = 64 tek kesit (tek olay: 2-13 Kasım dönüşü; hisseler aynı günlerde ortak piyasa hareketine maruz, bağımsız değil); permütasyon p bağımsızlık varsayar; 18+ açıklayıcı: BH'ye rağmen şans bulgusu olabilir; eşik tabloları yalnız %3 / %5 sınır geçişlerini gösterir; serbest fonlar KAP fon raporlarında eksik; açıklama, kural değil",
 "sonuc": {
  "Y1": "C(13.11.2026 son bar) / C(kesim barı); fiyat Yahoo, 64 hisse için ayrı klasöre (kesit/yahoo_son) yeniden indirilir (TAVAN_SERISI.ts_indir); indirme 13.11 15:10 UTC (18:10 TR, seans kapanışı sonrası) SONRASINDA yapılır (kapanış); kapanış alınamazsa gün içi son bar kullanılır ve raporda 'gün içi' yazılır",
  "Y2": "02.11 - 13.11.2026 barlarında tavan günü sayısı (TAVAN_SERISI.ts_tavan tanımı; 13.11 gün içiyse o bar da sayılır)",
  "Y3": "C(13.11) / en düşük kapanış (01.09.2026 - 13.11.2026)",
  "birincil": "Y1 (karar Y1 üzerinden; Y2 yön teyidi; Y3 BİLGİ)",
  "fiyat": "Yahoo bölünme düzeltmeli kapanış (TAVAN_SERISI.ts_yahoo_oku); oranlar ölçekten bağımsız"
 },
 "surum_etiket": "genis_kesit_20261113",
 "test": {
  "aday": "ADAY EMARE <=> BH sonrası anlamlı (Y1, q = 0,10) VE rho_Y2 işareti rho_Y1 ile aynı (rho_Y2 != 0)",
  "bh_aile": "Y1 permütasyon p'leri, SINANAN bütün açıklayıcılar (Benjamini-Hochberg)",
  "bh_q": 0.1,
  "p": "iki yönlü permütasyon p = (1 + #{|rho*| >= |rho| - 1e-12}) / (1 + B); Y karıştırılır; eksik değerli hisse o değişkende dışarıda",
  "perm": 10000,
  "rho": "Spearman (ortalama sıra; eşitlik düzeltmeli Pearson sıra korelasyonu)",
  "sinanmaz": "geçerli değeri < 20 hisse, tek değerli ya da ikili değişkende küçük grup < 5 hisse -> SINANMAZ (BH ailesine girmez, nedeni yazılır)",
  "tohum": 20261113,
  "yari_fark": "üst yarı / alt yarı farkı = medyan Y1 (X >= medyan X) - medyan Y1 (X < medyan X); ikili X'te medyan Y1 (X=1) - medyan Y1 (X=0); medyan en küçük değere eşitse (sıfır yığılması) üst = X > medyan; Y2 için aynı (ortalama tavan sayısı farkı)"
 },
 "x": {
  "x01_tepe250": "C(kesim) / son 250 barın (<= kesim) en yüksek kapanışı - 1 (en az 20 bar; yeni halka arzda mevcut barlar)",
  "x02_log_fiyat": "log10(ekran fiyatı) kesim barında (Yahoo kapanış x sonraki bölünme çarpanı = o günkü ekran fiyatı)",
  "x03_fon_kriz": "kriz öncesi fon payı = canli_cokmus.csv fon_pay_kriz_oncesi (FON_IZI.fi_k25_pay_tablo, KAP fon raporu bilinme <= 31.08.2026); hisse hiçbir fon raporunda yoksa 0 (serbest fonlar KAP raporunda eksik olabilir: sınır)",
  "x04_tasfiye_kalan": "TASFİYE FONU KALAN PAYI (%): MKK eşik tabloları (esik_tum.csv; KAP 'Kamuyu Aydınlatma Platformu Duyurusu' 12-(4) ekleri, günlük) satırlarından sahibi tasfiye kapsamındaki portföy şirketlerinin (COL_v1.FON_TASFIYE: TERA, PUSULA, HEDEF, ATLAS, A1, PARDUS, BULLS PORTFÖY) bir FONU olanlar; her (hisse, fon) için yayın <= 31.10 olan son satırın 'sonraki %' değeri; fonlar toplanır. Kayıt yoksa 0 (eşik altı bilinmez)",
  "x04b_satis_bitti": "SATIŞ BİTTİ (1/0) = 17.10 - 31.10.2026 yayınlı eşik satırlarında hisse için hiçbir sahipten AZALIŞ (sonraki % < önceki %) yok (son 2 haftada azalış bildirimi yok)",
  "x05_azalis_sayisi": "Eylül - Ekim (yayın 01.09 - 31.10) eşik tablolarında hisse için AZALIŞ satırı sayısı (her sahip; satış baskısı yoğunluğu)",
  "x06_leke": "LEKE (1/0): (a) SPK bülteni (yayın <= 31.10; 2026/56 - 2026/78) metninde '(KOD)' ya da 'KOD Pay Piyasas' geçen satırın 3 satır öncesi - 6 satır sonrası içinde 'suç duyurusu' / 'işlem yasağı' / '107/1' / '106/1' (idari para cezası tek başına sayılmaz); YA DA (b) hissenin kendi KAP bildirimi (stockCodes; yayın 01.09 - 31.10) konu / özet / metninde kayyım|kayyum|TMSF|Tasarruf Mevduatı Sigorta Fonu|tutukla|gözaltı; aynı cümlede olumsuzlama (bulunmamak|yoktur|olmamış|alınmamış|söz konusu değil|ilgisi) varsa sayılmaz",
  "x06b_mkk_yasak": "MKK 'SPK İşlem Yasağı Nedeniyle Pay Duyurusu' (yayın <= 31.10) ilgili paylarında (relatedStocks) geçiyor (1/0)",
  "x07_geri_alim": "GERİ ALIM (1/0): hissenin kendi 'Payların Geri Alınmasına İlişkin Bildirim'i (program ilanı ya da işlem), yayın 01.09 - 31.10",
  "x07b_geri_alim_sayi": "aynı bildirimlerden özeti program başlatma / program kararı OLMAYANLARIN sayısı (gerçekleşen geri alım işlemi yoğunluğu vekili)",
  "x08_pddd": "PD/DD = sermaye_lot (dol.pkl) x ekran kapanış(kesim) / özkaynak; özkaynak = temel_duz.csv son dönem (açıklama <= 31.10); yoksa KAP Finansal Rapor (yayın <= 31.10, en son iki rapor) 'Ana Ortaklığa Ait Özkaynaklar', yoksa 'Toplam Özkaynaklar', yoksa 'ÖZKAYNAKLAR' (finans şirketi biçimi) cari dönem, 'Sunum Para Birimi' çarpanıyla (1.000 TL -> x1000). Özkaynak <= 0 -> 1e6 (en pahalı sıra); bulunamazsa eksik",
  "x09_halka_aciklik": "halka açıklık oranı (dol.pkl 'hao', %; kriz öncesi MKK / KAP değeri)",
  "x10_hacim_oran": "son 10 bar (<= kesim) ortalama TL hacim / önceki 60 bar ortalama TL hacim (TL hacim = Yahoo kapanış x hacim; satış tükenmesi)",
  "x11_dipten_gun": "kesim barına kadar 01.09 sonrası en düşük kapanıştan bu yana geçen bar sayısı (dip kesim barıysa 0)",
  "x12_col": "ÇÖL (1/0): COL_v1.col_olc(fiyat <= kesim) çöl kutusu döndürüyor (D13 dip2 + MIN_UZ / MAX_YUK kapıları) YA DA FON_IZI.fi_k24_tara (fiyat <= kesim) 'kural' günü son 20 barda",
  "x13_bist100": "BIST 100 üyesi (1/0): KAP şirket sayfası 'Şirketin Dahil Olduğu Endeksler' listesinde tam 'BIST 100' (01.10 - 31.12.2026 dönemi; 21.09.2026'da ilan, dönem içinde değişmez; sayfa 13.11'de okunur; liste okunamazsa eksik). MSCI üyeliği ÖLÇÜLMEZ: <= 31.10 tarihli ücretsiz liste yok",
  "x13b_bist500": "BIST 500 üyesi (1/0): aynı liste, tam 'BIST 500' (BIST 100 bu örneklemde tek değerli çıktığı için ön kayıttan önce eklendi)",
  "x14_ortak_alim": "EKİM ORTAK / YÖNETİCİ ALIMI (1/0): (a) KAP 'Pay Alım Satım Bildirimi' (ilgili kodlarda hisse; yayın 01.10 - 31.10; yayımlayan portföy şirketi değil; metin Merrill Lynch / Bank of America değil) metin kuralıyla NET ALIŞ (gk_alim_yonu: MKK formunda 'X TL toplam nominal tutarlı alış' toplamı > satış toplamı; 'adet alış işlemi'; ek PDF metni pdftotext); YA DA (b) Ekim yayınlı eşik satırında artış (sonraki % > önceki %) ve sahip fon / portföy / banka / aracı kurum / yabancı kurum / ihraççının kendisi değil",
  "x15_ayni": "AYNİ ÖDEME ADAYI (1/0): Ziraat'in tasfiye ettiği PUSULA / ATLAS portföy fonlarının hissede son bilinen payı > 0: FON_IZI G (bilinme <= 31.10, son ay, PUSULA / ATLAS fonları toplam pay >= %0,5) ya da eşik tablosunda PUSULA / ATLAS fonunun son 'sonraki %' > 0 (Ziraat 15.10 duyurusu: bazı fonlarda bakiye hisse aktarımıyla ayni)"
 }
}
```

## Ölçümden önce yapılanlar (sonuç içermez)

- Açıklayıcı tablosu X (yalnız <= 31.10 bilgisi; fiyat 30.10 barında kesildi, KAP yayın <= 31.10) ölçümden ÖNCE kuruldu ve sha256 ile donduruldu (aşağıda). Y1 / Y2 / Y3 hesaplanmadı, X ile Y arasında hiçbir ilişki bakılmadı.
- Önceden görülen sonuç bilgisi (dürüst not): canli_cokmus.csv 13.11 sabah tablosunda 'dipten_kat' (Y3'e yakın) ve tavan sayıları vardı; örneklem seçimi için okundu. Tanımlar Cemal'in iş tanımındaki 15 maddeden birebir alındı; seçim sonuçla değişmedi.
- Kodun uçtan uca denenmesi için istatistik, ağaç ve rapor yalnız RASTGELE ÜRETİLMİŞ sahte Y ile (np.random, tohum 0) bir kez koşturuldu; gerçek Y yok.
- 4 hisse çöl tablosu (col4) sonuçla ilgisiz BİLGİ olduğu için ön kayıttan önce çalıştırıldı (T5 kuralı KAP metin biçimine göre ayarlandı: '%5 sınırını aşarak').
- Ön kayıttan önce yapılan tanım düzeltmeleri (sonuç görülmeden): SPK penceresi +-60 -> -3/+6 satır (idari para cezası yanlış eşleşmesi), 'satış bitti' bütün sahiplerin azalışı, BIST 500 eklendi (BIST 100 tek değerli), özkaynak finans biçimi + birim çarpanı, eşik tablosunda çok kodlu unvan eşlemesi.
- X dağılımı (sınanabilirlik denetimi):
- x01_tepe250: n 64, medyan -0.9099, min -0.981, max -0.7749
- x02_log_fiyat: n 64, medyan 0.9452, min -0.3188, max 3.313
- x03_fon_kriz: n 64, medyan 0.00556, min 0, max 0.3076
- x04_tasfiye_kalan: n 64, medyan 0, min 0, max 51.7
- x04b_satis_bitti: n 64, 1 olan 58
- x05_azalis_sayisi: n 64, medyan 1, min 0, max 15
- x06_leke: n 64, 1 olan 16
- x06b_mkk_yasak: n 64, 1 olan 59
- x07_geri_alim: n 64, 1 olan 17
- x07b_geri_alim_sayi: n 64, medyan 0, min 0, max 24
- x08_pddd: n 64, medyan 0.8789, min 0.08064, max 1e+06
- x09_halka_aciklik: n 64, medyan 31.8, min 6.7, max 95.6
- x10_hacim_oran: n 62, medyan 0.2878, min 8.894e-05, max 1.767
- x11_dipten_gun: n 64, medyan 0, min 0, max 21
- x12_col: n 64, 1 olan 4 -> SINANMAZ (ikili, küçük grup 4 < 5)
- x13_bist100: n 56, 1 olan 0 -> SINANMAZ (tek değerli)
- x13b_bist500: n 56, 1 olan 52 -> SINANMAZ (ikili, küçük grup 4 < 5)
- x14_ortak_alim: n 64, 1 olan 12
- x15_ayni: n 64, 1 olan 13

## Bilinen sınırlar

n = 64 tek kesit (tek olay: 2-13 Kasım dönüşü; hisseler aynı günlerde ortak piyasa hareketine maruz, bağımsız değil); permütasyon p bağımsızlık varsayar; 18+ açıklayıcı: BH'ye rağmen şans bulgusu olabilir; eşik tabloları yalnız %3 / %5 sınır geçişlerini gösterir; serbest fonlar KAP fon raporlarında eksik; açıklama, kural değil

ESIK_SHA256: a019c04ea32774b88849bcdc1ebd40a1442d4ba330eb83915076590c636f25d1
KOD_SHA256: 5ef388e253d644cbf81487bdc3f8531aa53f4a29f69598b79eacf6cc74d0b2fb
X_SHA256: 5fcf56e652ca47bf42810865fcc9f6ea3fe7e4a517955583a171be5bcc0d2454
VERI_SHA256: {"G.pkl": "cdde36f074df0a435274ffbb19ed4734b0291964db7e8093acd2a9e623c9fc3c", "canli_cokmus.csv": "bc04c0cb0b9ec3100d31756c339058caaf0b097c8534ede621343f2eeb22f2cd", "dol.pkl": "fcdcf8344d08de62856dd7654b8efe28b38f78c7c5ff22e5a8b15fa77eb20d3c", "esik_tum.csv": "11ec92d75766c2ca5bd46e480b138d276c59e4f434ea91b0873c41bc19b1c8b1", "tum.json": "45d4ff4d51dfc17a6e60f58f1d894cd18c8959b866b0df68e240d5ad825b53cb"}
