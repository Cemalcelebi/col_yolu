# GT6 ÖN KAYIT — ÇÖL-K2 KIRILIM: yön ve kırılım sonrası 15 bar (27 Kasım 2026)

# DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)

Bu ölçüm 'çöl tuttu / tutmadı / iz' sorusunu yanıtlamaz; yalnız ÇÖL-K2 dedektörünün (dondurulmuş GT5 olayları) bulduğu bölgelerin tavanı mı dibi mi önce kırdığını ve tavan kırılımından sonraki 15 barı, aynı hissenin sıradan pencereleri / sıradan kırılımlarıyla karşılaştırır.

İş tanımı: arastirma_cikti/goz_tespit/GT6_IS_TANIMI.md (ana model). Bu dosya yön ve getiri hesaplanmadan ÖNCE commit + push edilir. `python GOZ_TESPIT.py k2kirolc` bu dosyanın commit + push edilmiş olmasını (gt_kapi_commit), KONTROL LİSTESİ'nin dolu olmasını (IZ_KARNE.ik_kontrol_kapisi), kod sha / eşik sha / olay sha'nın bu dosyada yazılı ve gt6_sayim.json ile aynı olmasını denetler; gt6_ozet.json varsa ikinci koşu durur.

## 1. Mühürler
- Kod commit: e9f6949 (GOZ_TESPIT.py bölüm 12 ÇÖL-K2 KIRILIM + test_goz_tespit.py; ilk commit f18d869, ikinci commit yalnız YÖN tablosuna bilgi ölçüsü ekledi; ikisi de ölçümden önce).
- GOZ_TESPIT.py sha256 (kod_sha): f597baa461008e695a0c94701aba372c2c979c6e09a585e1372d5fdc20b20575
- ÇÖL-K2 KIRILIM eşik sha (GT_K2K): 75c9445949e921504c7f076a32bd89f1929ffc39eb56e95f831bbaef45497ead
- ÇÖL-K2 eşik sha (GT_K2 + GT_K2_OLAY + GT_K2_OLC; GT5 ile aynı, değişmedi): 457e7ce7f0a2cc15f92651457209471f0b4213fe85e2a052a87538f8b65bbebe
- Olay dosyası /root/.kasa/ham/goz_tespit/k2/k2_olay.pkl sha256 (olay_sha; GT5_ON_KAYIT.md ile aynı, kodda assert): e0ef464c8159b1f403ba03537352e939ea699b3a2a5c6148366485eae99cbf55
- Getirisiz sayımlar: arastirma_cikti/goz_tespit/gt6_sayim.json (sha256 73560e6d56d3b54eb98537f6f7b4f554c6ace45af06165d7c7452e87b7381803; bu commit'te).
- Testler: test_goz_tespit.py 36 / 36 (eski 26 aynen + yeni 10).
- Not (süreç): ön kayıt dosyası ilk yazılırken kabuk metindeki ters tırnaklı komutu bir kez çalıştırdı (12:43:23 UTC); komut dosya olmadığı için ilk kapıda (gt_kapi_commit) DURDU, hiçbir yön / getiri hesaplanmadı, çıktı yazılmadı (gt6_ozet.json ve k2k_*.pkl yok). Bu düzeltme commit'i metindeki boşluğu doldurur.

## 2. Tanımlar (GOZ_TESPIT.GT_K2K; iş tanımından aynen, belirsiz yerlerin yorumu §3'te)
- Bölge [s, t] olay dosyasından; TAVAN = bölgedeki en yüksek High; DİP = en düşük Low (gt_k2k_tavan_dip; yalnız s..t).
- İzleme: t'den sonraki 20 geçerli bar (High > Low; gt_k2k_izleme). 20. bar veride yoksa ya da tarihi > 2022-12-31 ise KESIK (sayım dışı).
- YÖN (gt_k2k_yon): YUKARI = izlemede Close > TAVAN olan ilk bar b; AŞAĞI = Close < DİP olan ilk bar; hangisi önce; 20 barda hiçbiri yoksa KIRILMADI. Kapanış kuralı: fitil delmesi kırılım değildir; Close ile iki yön aynı barda olamaz (TAVAN >= DİP).
- GİRİŞ (yalnız YUKARI önce): b + 1 barı açılışı (MUM_IZI_HAVUZ.hv25_olc_dizi, karar barı b). R15 = b + 15 barı kapanışı / giriş - 1. b + 15 barı veride yoksa ya da tarihi > 2022-12-31 ise KESIK.
- SİMETRİK İLK DOKUNUŞ (gt_k2k_simetrik): b + 1 .. b + 15 barlarında High >= giriş x 1,05 önce mi (ÜST), Low <= giriş x 0,95 önce mi (ALT); aynı barda ikisi BELİRSİZ; hiçbiri YOK. %10 için aynısı. Stop yok.
- KONTROL 1 (yön): aynı hisse, aynı dönem (t + 1 barı tarihine göre), aynı L (20 / 40 / 80), evren şartları aynı (gt_k2_evren: 2016-01-01..2022-12-31, s >= 120, KIL <= 0,20, gövdesiz pay <= 0,30), gt_k2_yer_vek YER = 0 pencere paneli pencereleri (t % 5 == 0); YER = 1 kümesi k2_aday.pkl ile hisse hisse aynı (assert). KESIK olmayanlarda aynı YÖN kuralı. Taban = hisse-dönem-L içinde YUKARI payı; en az 5 pencere (azsa olay A'dan düşer, sayılır). Hücre tabanı = olay ağırlıklı ortalama.
- KONTROL 2 (kırılım sonrası): Kontrol 1 pencerelerinden YUKARI önce gelenlerin b günleri; hisse başına tekil (b artan; önceki tutulandan < 15 bar sonra gelen düşer); dönem = giriş (b + 1) tarihine göre; aynı giriş / R15 / simetrik kuralı. T1k = hisse-dönem içinde KESIK olmayan kırılımların R15 ortalaması (en az 5; azsa olay B'den düşer, T1K_AZ diye sayılır). Tabanlar (simetrik ÜST / ALT payı %5 ve %10, R15 < -%20 / > +%20 payı) aynı kırılımlardan, hücrede olay ağırlıklı.
- Olay kırılımları kol + hisse başına aynı 15 bar tekil kuralı (olaylar zaten >= 40 bar arayla; kural uygulanır, düşen TEKIL_DUSTU diye sayılır).
- T1 (bilgi): GT5 / Ç271 ile aynı (gt_k2_taban: aynı hisse-dönemin bütün uygun günleri, m = 20); bilgi satırı R15 - T1.
- Bootstrap: ay kümeli %95 (KISA_UFUK.ku_boot; 2.000; np.random.default_rng(6) her ölçüde yeniden); küme ayı: TABLO A'da t + 1 ayı, TABLO B'de giriş ayı.
- Beşlik: olayın ATRP20'si (t günü) ve gt5_olay.json besli_sinir (GT5'te getirisiz yazılmış, dondurulmuş).

## 3. Belirsiz yerlerin yorumu (sonuç görülmeden; değişmez)
1. 'Girişten sonraki 15. geçerli bar': giriş barı 1. bar sayıldı (R15 = b + 15 kapanışı), KISA_UFUK / MUM_IZI_HAVUZ / GT5 ile aynı tanım.
2. Simetrik payda: BELİRSİZ olay o ölçünün hem payından hem paydasından çıkar; YOK paydada kalır (pay = ÜST önce / (ÜST + ALT + YOK)). Taban da aynı kuralla.
3. Kontrol 1 en az pencere sayısı iş tanımında yok: 5 seçildi (Kontrol 2 ile aynı); düşen olay sayısı aşağıda (getirisiz).
4. Hücre: olayın dondurulmuş hücresi (t + 1 tarihi). TABLO B'de olayın T1k'si ve Kontrol 1 tabanı aynı dönemden alınır; Kontrol 2 kırılımlarının dönemi kendi giriş tarihine göre.
5. KESIK izleme: 20 barlık pencere tam değilse kırılım önce gelse bile KESIK (sonuçtan bağımsız, takvim kuralı).
6. YÖN kararında 'bölge >= 50' = Kontrol 1 tabanı olan, KESIK olmayan bölge sayısı; paylar aynı kümede.
7. EMARE iki tablo için AYRI yazılır: 'YÖN EMARE' <=> ANA kol (K2) ABD 2016-19 ve ABD 2020-22 YÖN TUTAR; 'KIRILIM SONRASI EMARE' <=> aynı iki hücrede KIRILIM SONRASI TUTAR. İş tanımı tek cümleyle yazmış (HATA'da not).
8. Kontrol 2 kırılımları üç kol için ortaktır (üç kol da YER'i şart koşar; Kontrol 1 = YER'i sağlamayanlar). Olayın b günü bir kontrol kırılımıyla aynı gün olabilir; çıkarılmadı.
9. Kontrol pencereleri örtüşür (5 bar adım, üç L); taban bir paydır, bootstrap yalnız olay ayları üzerinde (taban belirsizliği yok sayılır; hisse-dönem-L başına binlerce pencere).
10. BİLGİ (karara girmez; kodda ölçümden önce eklendi): kırılan bölgeler içinde YUKARI payı (yukarı / (yukarı + aşağı)) ve Kontrol 1'in aynı oranı, fark [GA]. Gerekçe K1 mekanik üstünlük: ÇÖL-K2 kutuları dar (YER kutu / uzak görünüm <= 0,22, küçük mum); dar kutu iki yönde de kırılımı kolaylaştırır, 'yukarı önce' payını kendiliğinden artırabilir. Kırılanlar içinde oran bu etkiye karşı daha dayanıklıdır.

## 4. Getirisiz sayımlar (k2kirsay; yön / kırılım / getiri hesaplanmadı)
Kontrol kırılım adedi, yön adetleri ve T1k (>= 5 kontrol kırılımı) şartından düşen olay sayısı sonuca bağlıdır: ölçümle birlikte raporlanır.

| kol | hücre | bölge | izleme KESIK | bölge (kesiksiz) | hisse | Kontrol 1 tabanlı (>= 5 pencere) | tabansız düşen | ATRP20 beşlik B1 / B2 / B3 / B4 / B5 |
|---|---|---|---|---|---|---|---|---|
| K2 | ABD 2016-19 | 949 | 0 | 949 | 480 | 930 | 19 | 0 / 2 / 10 / 149 / 788 |
| K2 | ABD 2020-22 | 2324 | 50 | 2274 | 1193 | 2252 | 22 | 3 / 35 / 230 / 994 / 1012 |
| K2 | AVR 2016-19 | 16 | 0 | 16 | 10 | 16 | 0 | 0 / 0 / 0 / 0 / 16 |
| K2 | AVR 2020-22 | 37 | 1 | 36 | 27 | 36 | 0 | 0 / 0 / 1 / 4 / 31 |
| K2 | BIST 2016-19 | 79 | 0 | 79 | 48 | 79 | 0 | 2 / 6 / 13 / 27 / 31 |
| K2 | BIST 2020-22 | 93 | 2 | 91 | 69 | 91 | 0 | 24 / 25 / 24 / 16 / 2 |
| YMSB | ABD 2016-19 | 2619 | 0 | 2619 | 723 | 2566 | 53 | 1 / 3 / 25 / 306 / 2284 |
| YMSB | ABD 2020-22 | 5811 | 211 | 5600 | 1603 | 5546 | 54 | 13 / 50 / 430 / 1955 / 3152 |
| YMSB | AVR 2016-19 | 34 | 0 | 34 | 16 | 34 | 0 | 0 / 1 / 0 / 1 / 32 |
| YMSB | AVR 2020-22 | 113 | 3 | 110 | 58 | 110 | 0 | 0 / 0 / 2 / 12 / 96 |
| YMSB | BIST 2016-19 | 191 | 0 | 191 | 76 | 191 | 0 | 8 / 17 / 33 / 54 / 79 |
| YMSB | BIST 2020-22 | 248 | 1 | 247 | 114 | 247 | 0 | 58 / 64 / 51 / 47 / 27 |
| Y | ABD 2016-19 | 3794 | 0 | 3794 | 864 | 3725 | 69 | 1 / 6 / 26 / 362 / 3399 |
| Y | ABD 2020-22 | 8466 | 269 | 8197 | 1899 | 8120 | 77 | 15 / 54 / 507 / 2534 / 5087 |
| Y | AVR 2016-19 | 69 | 0 | 69 | 28 | 69 | 0 | 0 / 1 / 1 / 4 / 63 |
| Y | AVR 2020-22 | 196 | 2 | 194 | 80 | 194 | 0 | 0 / 0 / 1 / 12 / 181 |
| Y | BIST 2016-19 | 292 | 0 | 292 | 96 | 292 | 0 | 13 / 24 / 45 / 67 / 143 |
| Y | BIST 2020-22 | 323 | 1 | 322 | 123 | 322 | 0 | 64 / 74 / 67 / 51 / 66 |

| pazar x dönem | L | Kontrol 1 pencere | izleme KESIK | kesiksiz | hisse |
|---|---|---|---|---|---|
| ABD 2016-19 | 20 | 550.862 | 0 | 550.862 | 3.305 |
| ABD 2016-19 | 40 | 554.034 | 0 | 554.034 | 3.269 |
| ABD 2016-19 | 80 | 554.298 | 0 | 554.298 | 3.211 |
| ABD 2020-22 | 20 | 511.699 | 14.736 | 496.963 | 4.215 |
| ABD 2020-22 | 40 | 522.877 | 15.103 | 507.774 | 4.184 |
| ABD 2020-22 | 80 | 527.924 | 15.324 | 512.600 | 4.136 |
| AVR 2016-19 | 20 | 101.463 | 0 | 101.463 | 536 |
| AVR 2016-19 | 40 | 101.489 | 0 | 101.489 | 534 |
| AVR 2016-19 | 80 | 101.357 | 0 | 101.357 | 530 |
| AVR 2020-22 | 20 | 82.163 | 2.138 | 80.025 | 569 |
| AVR 2020-22 | 40 | 82.446 | 2.144 | 80.302 | 569 |
| AVR 2020-22 | 80 | 82.520 | 2.150 | 80.370 | 567 |
| BIST 2016-19 | 20 | 60.692 | 0 | 60.692 | 374 |
| BIST 2016-19 | 40 | 60.188 | 0 | 60.188 | 371 |
| BIST 2016-19 | 80 | 57.912 | 0 | 57.912 | 366 |
| BIST 2020-22 | 20 | 56.585 | 1.746 | 54.839 | 453 |
| BIST 2020-22 | 40 | 56.668 | 1.728 | 54.940 | 449 |
| BIST 2020-22 | 80 | 56.382 | 1.701 | 54.681 | 439 |

ÖNCEDEN BELLİ OLAN (sonuç görülmeden): ANA kolun AVR hücrelerinde bölge 16 / 36 (< 50) -> YÖN ÖLÇÜLEMEDİ; KIRILIM SONRASI için n giriş <= 16 / 36 olabilir, n < 30 çıkarsa ÖLÇÜLEMEDİ. Karar kuralı EMARE için yalnız ABD iki dönemini ister (iş tanımı); AVR hücreleri yazılır, karara girmez. YMSB ve Y kollarında AVR 2016-19 YÖN de 34 / 69 bölgeyle sınırda.

## 5. Ölçüler ve KARAR KURALI (önceden; değişmez)
- Hücreler: ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22 (KARAR); BIST 2016-19, BIST 2020-22 (BİLGİ). Kollar: K2 (ANA), YMSB, Y.
- TABLO A (YÖN): bölge sayısı, KESIK; yukarı önce / aşağı önce / kırılmadı payları; Kontrol 1 tabanı (yukarı önce; aşağı önce bilgi); fark = ortalama(1[YUKARI] - taban) [GA]; kırılıma kadar geçen bar medyanı (yukarı / aşağı ayrı); bilgi: kırılanlar içinde yukarı payı / taban / fark [GA].
- TABLO B (KIRILIM SONRASI): n giriş (durum adetleri: TAMAM / KESIK / T1K_AZ / TEKIL_DUSTU); TFk15 = ortalama(R15 - T1k) [GA]; medyan fark = medyan(R15) - medyan(T1k); simetrik +%5 ÜST önce payı, Kontrol 2 tabanı, fark [GA]; +%10 için pay ve taban (fark GA bilgi); ALT önce payları ve tabanları; R15 < -%20 ve > +%20 payları ve tabanları; ATRP20 beşliği içinde TFk15 (>= 20 olaylı beşlikler) ve artı sayısı; bilgi: R15 - T1.
- YÖN hücresi TUTAR <=> bölge (tabanlı, kesiksiz) >= 50 VE fark GA alt ucu > 0; < 50 ÖLÇÜLEMEDİ; aksi TUTMAZ.
- KIRILIM SONRASI hücresi TUTAR <=> n >= 30 VE TFk15 GA alt ucu > 0 VE medyan fark > 0 VE simetrik +%5 farkının GA alt ucu > 0 VE >= 20 olaylı beşliklerin en az %75'inde TFk15 > 0 (böyle beşlik 2'den azsa bu şart aranmaz, raporda yazılır); n < 30 ÖLÇÜLEMEDİ; aksi TUTMAZ.
- EMARE (yaşayan evren): §3 madde 7. Hangi sonuç çıkarsa çıksın başlık 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil)'.
- K7 UYARISI (zorunlu): evren bugün yaşayan hisseler; yer şartı en az 2 kat düşmüş hisseleri seçtiği için batanların yokluğu sonucu YUKARI yanlı yapar (Ç263 dersi); kontroller aynı hisseden olduğu için yanlılık farkta kısmen düşer, kalkmaz; artı sonuç en fazla 'EMARE (yaşayan evren)'; batanlar dahil veriyle sınama Aralık'ta.
- Sağlama (K11): iki hücrenin YÖN payı + farkı ve TFk15'i, satır dosyalarından ve ham seriden bağımsız kısa kodla (gt_k2k_* fonksiyonları kullanılmadan) yeniden üretilir.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | YÖN tabanı aynı hisse + dönem + L, YER'i sağlamayan pencereler, aynı TAVAN / DİP / 20 bar kuralı (gt_k2k_pazar, gt_k2k_taban1); kırılım tabanı aynı hissenin aynı dönemdeki sıradan tavan kırılımları, aynı giriş (b + 1 açılış), aynı R15 ve stopsuz simetrik dokunuş (gt_k2k_giris, gt_k2k_taban2): Ç271 stop geometrisi farkı yok; dar kutu mekanik etkisine karşı kırılanlar içinde yukarı payı bilgi olarak ölçümden önce eklendi (§3.10) |
| K2 | geleceğe bakma | EVET | olaylar dondurulmuş (sha assert); kontrol YER'i yalnız t'ye kadar (test_k2k_karar_sonrasi_okunmaz); yön kararı b'de yalnız b'ye kadar, izleme t + 20 ile sınırlı (test_k2k_izleme_sinir_ve_gecerli_bar); giriş ve 15 bar b + 15'ten sonrasını okumaz (test); beşlik sınırları GT5'ten getirisiz; veri <= 2022-12-31 (gt_kesik_kapi assert, izleme ve R15 tarih sınırı) |
| K3 | geçerli bar | EVET | seride High <= Low bar varsa GTHata (gt_k2k_pazar; mi_veri serisi geçerli bar); izleme gt_k2k_izleme geçerli barları sayar (test: geçersiz bar atlanır); kilitli / gövdesiz pay evren şartı GT5 ile aynı |
| K4 | tekilleştirme | EVET | olaylar GT5'te 40 bar tekil; kırılım günleri kol + hisse başına 15 bar (gt_k2k_tekil, test_k2k_tekil_15); kontrol kırılımları hisse başına aynı kural; medyan fark karar şartında |
| K5 | giriş fiyatı | EVET | giriş = kırılım barından sonraki barın açılışı (hv25_olc_dizi g0 = b + 1; test_k2k_giris_kirilim_sonrasi_acilis); kırılım günü kapanışı kullanılmaz |
| K6 | veri birimi | EVET | tek kip: GOZ_TESPIT açık kopyası (MV_YOL gunluk; GT5 ile aynı seri; olay t tarihi seriyle assert); bütün ölçüler oran / pay |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: sonuç YUKARI yanlı; raporda zorunlu uyarı; artı sonuç en fazla EMARE (yaşayan evren); batanlar dahil sınama Aralık |
| K8 | örneklem ve dönem | EVET | YÖN n < 50, KIRILIM n < 30 ÖLÇÜLEMEDİ; iki dönem ayrı hücre; AVR ANA kol 16 / 36 bölge önceden ÖLÇÜLEMEDİ yazıldı; karar yalnız ANA kol ABD iki dönem, BH yok (tek önceden seçilmiş karar ailesi; kollar ve BIST bilgi) |
| K9 | ön kayıt | EVET | bu dosya kod sha, GT_K2K eşik sha, olay sha, sayım json ile yön / getiriden önce commit + push; k2kirolc gt_kapi_commit + ik_kontrol_kapisi + sha denetimiyle başlar, gt6_ozet.json varsa ikinci koşu durur |
| K10 | ayrıştırma | EVET | YER = 1 kümesi k2_aday.pkl ile hisse hisse aynı (assert; sayım koşusunda geçti); pencere t ve olay t tarihleri seriyle assert; aday sha gt5_olay.json ile assert |
| K11 | yeniden üretim | EVET | rapordan önce iki hücrenin YÖN payı / farkı ve TFk15'i satır dosyalarından + ham seriden bağımsız kısa kodla yeniden üretilecek (GT6_RAPOR SAĞLAMA) |
| K12 | ifade | EVET | başlık DEDEKTÖRÜN BULDUĞU BÖLGELER; 'çöl tuttu / iz' cümlesi kurulmaz; TUTAR hücre düzeyinde sayım etiketidir; sayı ile yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (_cakisma_kontrol_gt, test); yalnız GOZ_TESPIT.py, test_goz_tespit.py, GT6_ / gt6_ dosyaları commit; yasak defter dosyalarına dokunulmadı; Colab'da kod değiştiği için çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; dedektör bölgeleri Cemal'in görsel onayını bekliyor |
