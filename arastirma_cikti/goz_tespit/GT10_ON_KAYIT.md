# GT10 ÖN KAYIT — KURAL-4: beş işaretli setten SETE GÖRE DIŞARIDA sınanmış kabul kuralı (28 Kasım 2026)

İş tanımı: GT10_IS_TANIMI.md (ana model, commit dad8614). Kod: GOZ_KURAL4.py + test_goz_kural4.py, commit **37f1d5d8944b** (2026-11-28 11:13:47 UTC; 12 / 12 sentetik test geçti).
Kod sha256: 3a4120857bcea92869a4781370f22429f4de15bf790addad47819920681172d7. Eşik sözlüğü (GK4) sha256: eea7e212ddbf75c4fe5a089b87bfb400affc26e132ad9b3073dd4b340e609537.

Bu dosya, etiket - ölçü ilişkisi HİÇ hesaplanmadan yazıldı: şu ana kadar yalnız sayfa ölçü tablosu (gt10_tablo.json; getirisiz) kuruldu ve aşağıdaki sayımlar alındı.
GETİRİ YOK: hiçbir sayfanın / bölgenin sonrası hesaplanmaz, okunmaz. Etiket: tespit işi; 'iz' sözü kullanılmaz.

## 0. SAPMA (ölçümden önce yazıldı)
- İş tanımı 30 + 28 + 20 + 21 + 23 = 122 sayfa bekliyordu ("tutmazsa dur, yaz"). Gerçek: GT3 anahtarı (GT3_onay_anahtar.json) ve işaret dosyası (cemal_gt3_onay.json) **32** sayfa (D1 24 + RASTGELE 4 + KİTAPLIK 4; Ç268 kaydı da '32 sayfa' der; uc_set_tablo.json 30 + 32 + 20 = 82). Beş setin işaretli sayfası **126**. Beş sette rastgele sayfa 6 + 4 + 4 + 4 + 4 = 22 (iş tanımındaki '1 / 22' ile uyumlu: rastgele sayfa sayısı doğru, GT3 toplamı yanlış yazılmış). Fark veri hatası değil iş tanımındaki sayım hatası olduğu için durulmadı; 126 ile sürülür, sayım kapısı 126'ya (set set 30 / 32 / 20 / 21 / 23) kurulu (gk4_sayfalar; test_sayim). Ana modele HATA olarak bildirilecek.
- Commit mesajlarında model adı yok (iş tanımı); oturum bağlantısı satırı var.

## 1. Veri
- Sayfalar: beş setin anahtar + işaret dosyaları (GK4['setler']); etiket `sinif4` (EVET / KISMEN / ERKEN / HAYIR); GT9 s. 1 işaretsiz, dışarıda.
- Ölçüler: goz2/uc_set.olc AYNEN (import; 35 sayısal alan) + 4 yeni ölçü (aşağıda). Açık veri sayfaları MUM_IZI.mi_veri(pazar, GT_YOL['acik']) (<= 2022-12-31, assert `_gk4_kesik`); kitaplık sayfaları (kaynak 'tam', 8 sayfa) GT_YOL['tam_bist']'ten, kitaplik_olcu.json 'bit' tarihinde kesik (uc_set.tablo ile aynı). Her sayfada seri ayrıca t'de kesilerek ölçülür (d.iloc[:t + 1]).
- KURAL-3 bayrağı (K3): D1 (GOZ_TESPIT.gt_k3_d1_sira >= 0,90; pencere panelinden (sembol, s, t, L) anahtarıyla) VE Y = 1 VE DIPTEN_BAR >= 0,5. Panelde olmayan sayfa (8 kitaplık sayfası) D1 değil.
- Yeniden üretim (getirisiz): gt10_tablo.json'daki GT1 / GT3 / GT4'ün 82 sayfası uc_set_tablo.json ile 35 ölçünün hepsinde birebir (test_tablo_uc_set_ile_ayni; t'de kesik seri = tam seri: sonrası okunmuyor). GT5 / GT9'un 44 sayfasında K3 bayrağı anahtar koluyla birebir (D1+YER+ZAMAN 11 + 15 sayfa K3 = 1; ötekiler 0).

### Yeni ölçüler (4; hepsi yalnız s..t barları)
- YENI_DIP_SON ('daha derin dip yok'): bölgenin son üçte birindeki (en az 3 bar) barlardan Low'u bölgede o bara kadarki bütün Low'lardan küçük olanların payı.
- ALT_FITIL_SON10 ('dip savunması'): son 10 barın (yalnız H > L) (min(O, C) - L) / (H - L) ortalaması.
- EGIM_FARK ('düşüş bitmeli / yuvarlanma'): (son üçte bir kapanış eğimi - ilk üçte bir kapanış eğimi) x üçte bir uzunluk / kutu yüksekliği.
- SON_BOY_ORAN ('küçük mum' sonda): son 10 barın medyan (H - L)'si / bölgenin medyan (H - L)'si.

## 2. Sayımlar (etiketle ölçü çaprazlanmadan)

### Set x sınıf

| set | ERKEN | EVET | HAYIR | KISMEN | toplam |
|---|---|---|---|---|---|
| GT1 | 3 | 10 | 14 | 3 | 30 |
| GT3 | 11 | 15 | 5 | 1 | 32 |
| GT4 | 5 | 8 | 3 | 4 | 20 |
| GT5 | 5 | 8 | 6 | 2 | 21 |
| GT9 | 6 | 7 | 5 | 5 | 23 |
| toplam | 30 | 48 | 33 | 15 | 126 |

### Set x kol

| set | D1 | D1+YER+ZAMAN | D1+YER_ZAMANSIZ | D1+ZAMAN_YERSIZ | D2 | D3 | K1+DIP | KITAPLIK | KITAPLIK_KARISIK | KITAPLIK_NET | RASTGELE | toplam |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GT1 | 6 | 0 | 0 | 0 | 8 | 6 | 0 | 4 | 0 | 0 | 6 | 30 |
| GT3 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 4 | 32 |
| GT4 | 0 | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 | 4 | 20 |
| GT5 | 0 | 11 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 21 |
| GT9 | 0 | 15 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 23 |
| toplam | 30 | 26 | 8 | 2 | 8 | 6 | 16 | 4 | 2 | 2 | 22 | 126 |

### Ölçü eksikleri
126 sayfanın 39 ölçüsünde boş değer yok. Ölçüler: KUTU_ORAN, KUTU_YER, TEPE_KAT, DUSUS, TEPE_UZAK, ONCE_DIP, EGIM, SON_YER, BOY_ORAN, GOV_ORAN, EN_BUYUK, KUTU_YUZDE, Y, M, S, B, Z, dokunus, K2, YMSB, DIP_KAYMA, DIPTEN_BAR, SON10_EGIM, YARI_ORT, IC, SON_DIP, TABAN_YASI, DUSUS_SONU, ONCE_DUZ, BAR, P_A, P_YUK, P_SONEGIM, SON5_YER, UST_YARI, YENI_DIP_SON, ALT_FITIL_SON10, EGIM_FARK, SON_BOY_ORAN.
D1 sırası bulunan sayfa 118 / 126 (eksik 8: kitaplık). KURAL-3 bayraklı sayfa (etiketle çaprazlanmadı): GT1 2, GT3 6, GT4 1, GT5 11, GT9 15 (toplam 35). Not: GT1 / GT3 / GT4'te KURAL-3 yalnız 9 sayfayı kabul eder (bu kodun D1 + Y + ZAMAN tanımıyla).

## 3. Yöntem (sabit; sonuç görülmeden)
- SETE GÖRE DIŞARIDA, 5 kat: her set bir kez sınama, kalan dört set eğitim; ölçü, yön, eşik, şart sayısı, C'nin ölçüleri ve kabul eşiği YALNIZ eğitimde seçilir. H1 hedefi: y = 1 <=> sinif4 = EVET (bütün 126 sayfa; ötekiler 0).
- **A (tek ölçü + eşik):** aday şart = (ölçü, yön >= / <=, eşik); eşikler = eğitim sayfalarının sonlu değerlerinin %10, 15, ..., 90 yüzdelikleri (tekilleştirilmiş). Amaç = kabul içinde ✓ payının Wilson %95 alt ucu (z 1,96); eğitimde kabul >= 20 sayfa şartı; eşitlikte çok kabul, sonra sıra. Boş değer şartı sağlamaz.
- **B (en çok 3 şartlı VE):** ileri seçim; ilk şart A'nınki; her adımda A'nın aday şartlarından (aynı ölçü ikinci kez yok) eklenince amacı (Wilson alt ucu, eğitim kabulü >= 20) en çok artıran; artış yoksa durur (B, A ile aynı kalabilir).
- **C (L2 lojistik, en çok 4 ölçü):** ölçüler eğitimde EVET - öteki AUC'sinin |AUC - 0,5|'ine göre sıralanır, Spearman |rho| > 0,80 olan atlanır, ilk 4 alınır; boşlar eğitim medyanıyla doldurulur; eğitim ortalaması / sd ile standart; ceza lam = 1 (standart katsayılara; sabit cezasız; Newton). Kabul eşiği = eğitim skorlarında kabul >= 20 ve ✓ payı >= %70 veren EN DÜŞÜK skor; yoksa kural hiçbir sayfayı kabul etmez.
- **Bazlar:** KURAL-3 (K3 bayrağı; GT1 / GT3 / GT4 onun örneklem içidir) ve HEPSİNİ KABUL. Aynı ölçülerle değerlendirilir.
- **Değerlendirme (set dışı; havuz + set set):** kabul sayısı; kabul olan set sayısı; kabul içinde ✓ / K / erken / değil payı; rastgele kabul (22 rastgele sayfadan); ✓ yakalama (48 ✓'nin kaçı kabul); ✓ payı için sayfa düzeyi bootstrap %95 aralığı (2.000; 126 sayfa yerine koyarak, set dışı kabul kararı sabit; tohum 10); GT5 + GT9 sayfalarında ✓ payı (KURAL-3 ile aynı sayfalarda karşılaştırma).
- **Yanlış keşif (etiket karıştırma):** sinif4 SET İÇİNDE karıştırılır, **1.000 kez** (tohum 1028), bütün hat (A, B, C) yeniden koşar. İstatistik T = set dışı kabulü >= 25 olan ailelerin en büyük havuzlanmış set dışı ✓ payı (hiçbiri >= 25 değilse havuz ✓ payı = 48 / 126). Bir ailenin gözlenen ✓ payı karıştırma T dağılımının %95'inin ÜSTÜNDE olmalı (en iyiyi seçme düzeltilmiş). Sayı gerekçesi: sentetik veride bir hat 0,08 sn; 1.000 karıştırma ~1,5 dk (iş tanımının en az 200 şartının 5 katı; p kestiriminin standart hatası daha küçük).
- **Seçim yanlılığı (bilgi):** GT5 / GT9 sayfaları KURAL-3 ile seçildi; set set ölçü aralığı (D1_sira, DIPTEN_BAR, KUTU_ORAN, KUTU_YER, TEPE_KAT, Y: min / medyan / maks) ve set set kabul tablosu raporda yorumlanır.

## 4. Karar (Ç279'da önceden yazıldı; değişmez)
- ADAY KURAL <=> set dışı kabul >= 25 sayfa VE kabul en az 4 sette VE kabul içinde ✓ payı >= %70 VE erken payı <= %20 VE rastgele kabul <= 1 / 22 VE GT5 + GT9 sayfalarında ✓ payı KURAL-3'ünkinden >= 10 puan yüksek VE ✓ payı karıştırma T'sinin %95'inin üstünde. Birden çok aile geçerse EN BASİT olan (A < B < C).
- Hiçbiri geçmezse: 'KURAL YOK (bu ölçülerle)'; üç aile en yakın üç aday olarak, hangi şartta kaldıklarıyla yazılır.
- **H2 (✓ - erken):** yalnız kodun seçtiği sayfalar (kol RASTGELE ve KITAPLIK* değil) ve sinif4 EVET / ERKEN. Her ölçü için her katta yön eğitim AUC'sinden (>= 0,5 olduğu gibi, değilse ters); sınama setinin yönlü değerleri havuzlanır; havuz AUC (EVET > ERKEN). Set set yön = o setin ham AUC'si bütün veri yönüyle aynı tarafta mı (0,5 eşit sayılmaz). 'ERKEN AYIRICI ADAYI' <=> havuz set dışı AUC >= 0,70 VE en az 4 sette aynı yön. En iyi beş ölçü (havuz AUC'ye göre) raporlanır; 39 ölçüden en iyiyi seçmenin şansını görmek için set içi EVET / ERKEN karıştırma (1.000; tohum 1029): en büyük havuz AUC'nin %95'i BİLGİ olarak yazılır (karar şartı değil).

## 5. Olay listesi (kör set için; getirisiz)
- Seçilen kural: karar geçen en basit aile; yoksa **EN İYİ ADAY** = set dışı kabul >= 25 olan ailelerden en yüksek set dışı ✓ payı; o da yoksa en yüksek set dışı Wilson alt ucu (kabul >= 1); açıkça 'EN İYİ ADAY (karar geçmedi)' adıyla. Beş setin tamamıyla (126 sayfa) aynı yöntemle yeniden kurulur; eşikler gt10_kural4.json.
- Havuz: KURAL-3'ün D1 havuzu = GOZ_TESPIT.gt_k2_evren (pencere sonu 2016-01-01 .. 2022-12-31, s >= 120, KIL <= 0,20, gövdesiz pay <= 0,30) ∩ D1 (gt_k3_d1_sira >= 0,90); ABD + BIST (sayım: BIST 34.926, ABD 317.992 pencere). Her pencerede gk4_olc; ölçüsü kurulamayan pencere kabul edilmez, sayılır. Kabul edilenler hisse başına gt_k2_tekil(bar = 40) ile çakışmasız. KURAL-3'e uyuyor mu = k3/k3_aday.pkl'da ANA = 1 (ayrıca olc'nin Y ve DIPTEN_BAR'ıyla uyuşmazlık sayılır). gosterildi = beş setteki aynı pazar + sembol açık veri sayfası ile [s, t] kesişiyor. Dönem pencere sonu tarihine göre (2016-19 / 2020-22).
- Dosya: /root/.kasa/ham/goz_tespit/k4/k4_olay.pkl (pazar, sembol, s, t, L, tarih, dönem, kural, K3, gosterildi, D1_sira, ölçüler). Sayım raporda (pazar x dönem; KURAL-3 kesişimi; gösterilmiş).
- K7: evren bugün yaşayan hisseler; bu iş getirisiz olduğu için sonuca etkisi yok; kör sette sonrası ölçülürse yukarı yanlı okunur.

## 6. Komut sırası
`python GOZ_KURAL4.py kos` (BİR KEZ: kilit /root/.kasa/ham/goz_tespit/k4/kos_kilit.json; kapı: bu dosya commit + push, IZ_KARNE.ik_kontrol_kapisi, eşik sha ve kod commit'i bu dosyada) -> `python GOZ_KURAL4.py olay` -> `python GOZ_KURAL4.py rapor` -> GT10_RAPOR.md + gt10_ozet.json commit + push.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | getiri / eş yok (tespit işi); yerine bazlar: HEPSİNİ KABUL, KURAL-3, 22 rastgele sayfa ve set içi etiket karıştırma 1.000 (gk4_karistir; bütün hat + en iyiyi seçme) |
| K2 | geleceğe bakma | EVET | ölçüler yalnız <= t: tablo d.iloc[:t + 1] ile (gk4_tablo), test_sonrasi_okunmaz, 82 sayfa tam seriyle (uc_set_tablo.json) birebir; açık veri <= 2022-12-31 assert (_gk4_kesik); kitaplık bit tarihinde kesik; set dışı: bütün seçimler yalnız eğitim setlerinde (gk4_hat) |
| K3 | geçerli bar | EVET | ALT_FITIL_SON10 yalnız H > L barlarında; olay havuzu gt_k2_evren (KIL <= 0,20, gövdesiz pay <= 0,30); sayfa ölçüleri uc_set.olc AYNEN (Cemal'in gördüğü sayfalar) |
| K4 | tekilleştirme | EVET | birim = sayfa (126; aynı hisse iki sayfa yalnız TEHOL GT1 s. 12 / s. 28, ayrı kitaplık bölgeleri 2024 / 2026); olay listesi hisse başına gt_k2_tekil(bar = 40) |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri hesaplanmaz (iş tanımı: BU İŞTE GETİRİ YOK); olay listesi yalnız pencere kimliği |
| K6 | veri birimi | EVET | ölçüler oran (kutu / grafik birimi), fiyat biriminden bağımsız; veri kopyası uc_set ile aynı (/tmp/mum_izi/acik, /tmp/veri); 82 sayfa birebir yeniden üretildi |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: getirisiz tespit işinde sonuca etkisi yok; olay listesi ve raporda K7 uyarısı (sonrası ölçülürse yukarı yanlı) |
| K8 | örneklem ve dönem | EVET | n küçük: 126 sayfa, 48 ✓, set başına 20-32; bootstrap aralığı + set set tablo; çoklu deneme karıştırmayla max istatistik (BH yerine); en fazla 'tespit kuralı adayı', 'bulgu' denmez; dönem yerine set dışı (5 set) |
| K9 | ön kayıt | EVET | kod commit 37f1d5d8944b, kod sha 3a412085, eşik sha eea7e212; gk4_kapi: bu dosya commit + push + kontrol kapısı + sha; kos bir kez (kilit) |
| K10 | ayrıştırma | EVET | sinif4 mekanik okunur, bilinmeyen sınıf / anahtarda olmayan sayfa durur (gk4_sayfalar); sayım 126 (SAPMA bölümü); elle 3 satır: GT1 s. 15 ADESE KISMEN, GT5 s. 14 EKIZ ERKEN, GT1 s. 17 IEYHO RASTGELE HAYIR kaynakla aynı; GT5 / GT9 K3 bayrağı 44 / 44 anahtar koluyla aynı |
| K11 | yeniden üretim | EVET | tablo 82 sayfa uc_set_tablo.json ile birebir (test); rapordaki en az iki hücre ozet / tablo dosyasından bağımsız kısa kodla yeniden üretilecek |
| K12 | ifade | EVET | 'iz' sözü yok; sonuç 'tespit kuralı adayı' ya da 'KURAL YOK (bu ölçülerle)'; sayı ile yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_gk4 (test); yasak defter / goz2 / GOZ_TESPIT dosyalarına dokunulmaz; yalnız kendi dosyaları adıyla commit; MI._mi_yaz sızıntı taraması; Colab'da kod değişince çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / alım yok; tespit kuralı sınaması |
