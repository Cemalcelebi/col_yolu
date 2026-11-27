# GT_RAPOR — GOZ_TESPIT: parmak izi, dedektörler, kör onay seti (yalnız tespit; getiri / sonrası yok)

Kod sha 306fe322b432, eşik sha 5d4c7975e408; parmak izi commit d4f0f4be93 -> dedektör commit a17b6a74e3 -> onay seti (PDF sha e14ffbc7c370, anahtar sha 499bbd016f05).

## SONUÇ

- PARMAK İZİ: 40 ölçü, 16 kitaplık bölgesi. İMZA ölçüleri (0): YOK.
- İmzaya en yakın ama geçemeyen: GOVDE_ORAN DÜŞÜK (%20, 10/14); BOY_YUZDE_ORAN DÜŞÜK (%22, 9/14); F5 YÜKSEK (%87, 10/16); F3 YÜKSEK (%79, 10/16); ONCEKI_DUSUS DÜŞÜK (%10, 8/14).
- Ayırmayan / zayıf ilginç ölçüler: F1 medyan %58 (6/16); BOY_YUZDE_ORAN medyan %22 (9/14); BOY_MUTLAK medyan %64 (6/14); UST_FITIL medyan %65 (6/14); SON_UST_FITIL medyan %56 (3/14); F6 medyan %60 (3/16); HACIM_ORAN medyan %40 (3/16); HACIM_SON5 medyan %60 (5/16).
- Mum izi ✓ / ✗ (bilgi): en yüksek |AUC - 0,5| beş ölçü: BOY_YUZDE_ORAN 0,29; BOY_GRAFIK_ORAN 0,30; BANT_SON 0,68; F2 0,67; GOVDE_ORAN 0,34. Çöl imzaları mum izi ✓'lerinde aynı uçta: 0 / 0.
- DEDEKTÖRLER (havuz BIST 343.032 / ABD 3.314.920 pencere): D1 BIST 33.845 (%9,87; tekil 5.907), ABD 315.142 (%9,51; tekil 49.717); D2 BIST 56.276 (%16,41; tekil 5.709), ABD 418.699 (%12,63; tekil 42.427); D3 (komşusu bulunan çöl) BIST 15, ABD 15. D2'nin 3 koşulu var (GOVDE_ORAN, F5, BOY_GRAFIK_ORAN; iş tanımı imzası yok, EK KURAL yakın imza); D3 ölçüleri (12): GOVDE_ORAN, F5, F3, DARALMA, BOY_GRAFIK_ORAN, ZIRVE_DUSUS, F2, RS_UZAK, OYN_SIRA, ATRP20, UST_ALT_PAY, MIKRO.
- Kitaplığın kendi yakalaması (örneklem içi): D1 üst %10'unda 3 / 16; D2'yi geçen 7 / 16.
- ONAY SETİ: 30 bölge sayfası + kapak; kol sayıları {'D1': 6, 'D2': 8, 'D3': 6, 'RASTGELE': 6, 'KITAPLIK': 4}; pazar {'BIST': 17, 'ABD': 13}; eksik yok; taşınan yok. Kol / hisse / tarih PDF'te yok (pdftotext denetimi); eşleme yalnız mühürlü anahtarda.
- Sayım kuralı (işaretlerden sonra, önceden): işaretlerden sonra ana model sayar: kol başına ✓ payı ve ✓ + K payı; RASTGELE kolun ✓ payı taban; 'KOD GÖZÜ TUTUYOR' <=> bir dedektörün ✓ payı >= 0,70 VE RASTGELE ✓ payından en az 40 puan yüksek; KİTAPLIK sayfalarında ✓ sayısı (4'te kaç); sayılar küçük: 'ilk tur'.

Okuma: dedektör sayfaları her dedektörün sıralamasının en üstünden alındı (kodun en çok benzettiği); seçilen kümenin tamamını temsil etmez. Kol başına 6-8 sayfa: sonuç 'ilk tur'; tutarsa en iyi kol 24 sayfayla yinelenir. Kitaplık imzası kitaplığın kendisinden kuruldu: D2'nin kitaplığı yakalaması örneklem içidir.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban oran = RASTGELE kol (aynı havuz, aynı L dağılımı, aynı sayfa çizimi); kitaplık 4 sayfa Cemal'in tekrar tutarlılığı; getiri karşılaştırması yok |
| K2 | geleceğe bakma | EVET | ölçüler yalnız s..t ve öncesi (test: t + 1 sonrası bozulunca aynı); kitaplıkta bütün BIST serileri bölge bitişinde kesilir (assert); havuz <= 2022-12-31 (assert) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar; kilitli pay > 0,20 ve gövdesiz (O = C) bar payı > 0,30 pencere havuzdan atılır |
| K4 | tekilleştirme | EVET | her dedektörde aynı hissede < 40 bar pencere sonlarından tek pencere; onay setinde her hisse bir kez |
| K5 | giriş fiyatı | UYGULANMAZ | giriş / getiri yok: yalnız tespit (sayfada bölge sonrası çizilmez) |
| K6 | veri birimi | EVET | ölçüler oransal / sıra; ABD ve BIST kendi evren sırasıyla; açık kopya bölünme düzeltmeli |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; tespit sorusunda etkisi küçük, raporda yazılı |
| K8 | örneklem ve dönem | EVET | kitaplık 16 bölge: 'tespit' (bulgu değil); onay kol başına 6-8 sayfa: 'ilk tur', en iyi kol 24 sayfayla yinelenir |
| K9 | ön kayıt | EVET | GT_ESIK sha + kod sha bu dosyada; GT_PARMAK_IZI.md commit + push dedektörden önce, GT_DEDEKTOR.md commit + push onay setinden önce (gt_kapi_commit) |
| K10 | ayrıştırma | EVET | F1..F6 COL_SKOR6 pencere paneliyle birebir (gt_cs_sagla); kitaplık PUAN sırası COL_SKOR6 kitaplik.json ile karşılaştırıldı; ek ölçüler elle örnekli test |
| K11 | yeniden üretim | EVET | rapordan önce >= 2 hücre (kitaplık sırası, D2 kesimi) ham dosyalardan bağımsız kısa kodla yeniden üretilir (GT_RAPOR) |
| K12 | ifade | EVET | 'imza' yalnız önceden yazılı kuralla; kitaplık yakalaması örneklem içi diye yazılır; 'kod gözü tutuyor' yalnız işaret sayımından sonra |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_gt); yasak dosyalara dokunulmaz; yalnız kendi yolları commit; MI._mi_yaz sızıntı taraması; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## YENİDEN ÜRETİM (K11)

- Ana model, pencere_BIST.pkl + kitaplik_olcu.json'dan bağımsız kısa kodla beş hücreyi yeniden üretti (evren: 2016-22, s >= 30, kilitli <= 0,20, puan sonlu; sıra = (küçük + 0,5 eşit) / n): TEHOL-4 F5 %98,8 (tablo %99); TEHOL-4 GOVDE_ORAN %1,4 (%1); KRVGD F5 %68,0 (%68); HDFGS BOY_GRAFIK_ORAN %34,6 (%35); MANAS ONCEKI_DUSUS %11,0 (%11). Tuttu.
- D2 kesimleri tablo satırlarından elle: GOVDE_ORAN yönlü sıraların alttan 3.'sü 0,52 (rapor 0,520); F5 alttan 4.'sü 0,58 (rapor 0,581). Tuttu.
- Onay sayfalarının 26'sında (kitaplık dışı) bölge barları: H = L bar %0, hacimsiz bar %0 (kilitli bar yok).

## HATA

- HATA: gt_onay / seri: sayfa satırı yalnız (pazar, hisse) ile aranıyordu; kitaplık kolunda aynı hissenin iki bölgesi (TEHOL) seçilince ikinci bölge birincinin kesim tarihiyle çizilmek istendi ve 'geçersiz bölge' ile durdu. Düzeltme: satırlar sayfa sırasıyla eşlenir, tarih kapısı korunur (ana model; onay seti üretilmeden).
- HATA: gt_sayfa: çok derin düşüşlü pencerede (önceki tepe son kapanışın 16-80 katı) MUM_IZI_HAKEM yüzde adımı listesi (en çok %500) yetmedi, 'uygun adım yok' ile durdu. Düzeltme: yalnız bu sayfa çiziminde büyük adımlar eklendi (MUM_IZI_HAKEM değişmedi).
- HATA: Süreç: iki alt ajan yarıda durduruldu (sistem 'kullanıcı durdurdu' dedi; Cemal bilerek durdurmadı); onay ve rapor adımları test edilmemiş kodla kaldı; ana model iki hatayı düzeltip adımları kendisi koştu (çalışma düzeninden sapma).
- HATA: GT_RAPOR ilk üretiminde HATA / SAPMA / YENİDEN ÜRETİM boş çıktı (ek dosya yazılmamıştı); bu dosyayla dolduruldu.

## SAPMA

- İş tanımındaki imza kuralı hiç ölçü seçmedi (imza = yok). D2 ve D3 ana modelin EK KURALI ile kuruldu (GT_DEDEKTOR.md 1a; ADIM A tablosu görüldükten sonra, onay setinden ve Cemal'in işaretlerinden önce; commit a17b6a7).
- Kod, ölçü hesabı ve tablolar alt ajanların; dedektör, onay ve rapor komutlarını ana model koştu ve iki küçük kod düzeltmesi yaptı (alt ajanlar iki kez durduruldu).
- Ana modelin göz denetimi (18 sayfa): sayfa düzeni doğru (sonrası, ad, tarih yok). D1 ve D2'nin en üst sıralarında aşırı çöküş sonrası düzleşmiş hisseler var (önceki tepe son kapanışın 16-80 katı; 5 sayfa); set kural gereği DEĞİŞTİRİLMEDİ, Cemal'in işareti sonucu belirler.

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- Ç264 GOZ_TESPIT: 16 çölde 40 ölçü; imza ölçüsü yok; en yakın: küçük gövde (10/14), küçük mum (9/14), derin sol bacak (10/16); kör onay seti 30 sayfa (D1 6, D2 8, D3 6, rastgele 6, kitaplık 4) Cemal'de; sayım kuralı önceden yazılı.
