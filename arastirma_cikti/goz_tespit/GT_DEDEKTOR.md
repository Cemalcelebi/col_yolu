# GT_DEDEKTOR — üç dedektör (ADIM B; ADIM A'dan sonra, Cemal'in işaretlerinden ve onay setinden ÖNCE sabitlendi)

Parmak izi commit'i: d4f0f4be93; GOZ_TESPIT.py sha 09455d76a79d; eşik sözlüğü sha 5d4c7975e408; dedektör json sha 71bba9c972ca. Getiri / sonrası hesaplanmadı.

## 1. Tanımlar (kesin)

- HAVUZ: evren + s >= 120 (MUM_IZI_UC ölçüleri ve 120 barlık uzak görünüm) + pencerede açılış = kapanış (gövdesiz, fiyat adımına yapışmış) bar payı <= 0,30 + PUAN_ESIT ve bütün imza ölçüleri sonlu + kitaplık bölgeleri ve aynı hissede onlarla örtüşen pencereler çıkar + Cemal'e daha önce gösterilmiş mum izi bölgeleriyle (mum_izi23_olay.csv; aynı pazar / hisse, takvim örtüşmesi) örtüşen pencereler çıkar. Evren: pencere sonu t = hissenin kendi geçerli bar indeksi k, k % 5 == 0 (COL_SKOR6 örneklemesi); pencere sonu tarihi 2016-01-01 .. 2022-12-31; s = t - L + 1 >= 30; COL_SKOR6 kilitli pay <= 0,20; PUAN_ESIT sonlu (COL_SKOR6.cs_dag_maske ile aynı); her ölçünün sırası aynı L'deki evren pencerelerinden o ölçüsü sonlu olanlara göre ((küçük + 0,5 eşit) / n; COL_SKOR6.cs_yuzdelik).
- D1 ESKİ PUAN: PUAN_ESIT'in kendi pazarı ve L'deki evren sırası >= 0,90 (üst %10); sıralama = bu sıra (eşitlikte ham puan).
- İŞ TANIMINDAKİ D2 İMZA: her imza ölçüsünde kitaplık yönüne çevrilmiş sıra (DÜŞÜK yönlüde 1 - sıra) >= maks(0,50; kitaplık yönlü sıralarının alttan (n - ceil(0,8 n)). değeri) (16'da 13 çölün sağladığı sınır); sıralama = yönlü imza sıralarının ortalaması. İş tanımı imza ölçüleri (0): YOK.
- İŞ TANIMINDAKİ D3: standart imza uzayı: z = Φ⁻¹(yönlü sıra, [0,001; 0,999] kırpık); uzaklık = ortak sonlu boyutlarda karekök ortalama kare fark; her kitaplık çölünün aynı L* sınıfında, kendisinden farklı hissedeki en yakın havuz penceresi (pazar başına; çöller sırayla, daha önce seçilen hisse atlanır); sıralama = uzaklık (küçük önce). İmza uzayı boş olduğu için tanımsız.

## 1a. SAPMA: iş tanımındaki imza kuralı hiç ölçü seçmedi; ana modelin ek kuralı

Ana modelin ek kuralı ADIM A tablosu görüldükten SONRA, Cemal'in işaretlerinden ve onay setinden ÖNCE yazıldı; imza kuralının sonucu değişmedi (imza = yok). Ek kural sha 9b6a27ca5ba2 (GT-EK-1 (2026-11-27)).

- D2 YAKIN İMZA (D2'nin yerine): yakın imza ölçüsü <=> medyan sıra >= %75 ya da <= %25 VE tutarlılık >= %55 VE karşı uçta (yön YÜKSEK ise <= %30'da; DÜŞÜK ise >= %70'te) en çok 1 bölge VE ölçüsü olan bölge >= 12; sonra |rho| > 0,80 çiftlerinden tutarlılığı düşük olan atılır (eşitlikte karşı uçta az bölgesi olan kalır); kalan ölçülerin her birinde pencere kitaplığın tarafında ve kitaplık değerlerinin en gevşek %20'lik sınırının içinde (iş tanımındaki D2 sınırı aynen); sıralama = bu ölçülerin kitaplık yönündeki evren yüzdelik sıralarının ortalaması.
- D3 EN YAKIN KOMŞU (sıra uzayı) (imza uzayının yerine): tutarlılığı >= %50 olan ölçüler (BOLGE_L ve PUAN_ESIT hariç), |rho| > 0,80 budamasından sonra; her ölçü evren yüzdelik sırasına çevrilir; uzaklık = ortak (boş olmayan) ölçülerde ortalama mutlak sıra farkı, en az 8 ortak ölçü; kitaplıktaki her çölün (aynı L* sınıfında, farklı hisseden) en yakın komşusu; set için 6 sayfa = komşu uzaklığı en küçük 6 çölün komşuları (farklı çöllerden, farklı hisselerden).
- Uygulama ayrıntısı: D3 aday tablosu pazar başına her çölün en yakın 20 farklı hisseli komşusunu uzaklık sırasıyla tutar; onay seçimi kol_pazar'a göre (BIST 3, ABD 3) bu sıradan alır, bütün D3 kolunda her çöl ve her hisse en çok bir kez (bir çölün en yakın komşusunun hissesi zaten kullanılmışsa o çölün sıradaki komşusu); budama eşitliğinde (D3) medyanı 0,5'ten uzak olan kalır.

D2 ölçü adayları (budama öncesi): GOVDE_ORAN, BOY_YUZDE_ORAN, F5, ONCEKI_DUSUS, BOY_GRAFIK_ORAN; budamada atılan: BOY_YUZDE_ORAN (GOVDE_ORAN ile rho 0,81); ONCEKI_DUSUS (F5 ile rho -0,92); KALAN D2 ölçüleri (3): GOVDE_ORAN (DÜŞÜK), F5 (YÜKSEK), BOY_GRAFIK_ORAN (DÜŞÜK).

D3 ölçü adayları (tutarlılık >= %50): GOVDE_ORAN, BOY_YUZDE_ORAN, F5, F3, ONCEKI_DUSUS, DARALMA, BOY_GRAFIK_ORAN, ZIRVE_DUSUS, F2, RS_UZAK, OYN_SIRA, ATRP20, UST_ALT_PAY, MIKRO; budamada atılan: BOY_YUZDE_ORAN (GOVDE_ORAN ile rho 0,81); ONCEKI_DUSUS (F5 ile rho -0,92); KALAN D3 ölçüleri (12): GOVDE_ORAN, F5, F3, DARALMA, BOY_GRAFIK_ORAN, ZIRVE_DUSUS, F2, RS_UZAK, OYN_SIRA, ATRP20, UST_ALT_PAY, MIKRO.

- TEKİLLEŞTİRME: her dedektörde aynı hissede pencere sonları arasında < 40 bar olan pencerelerden yalnız en yüksek sıralı olan kalır (L = 20 / 40 / 80 dahil; açgözlü, sıra büyükten küçüğe).

## 2. D2 kesim değerleri (yönlü sıra uzayında; kitaplıktan)

| imza ölçüsü | yön | ölçüsü olan çöl | 13/16 kuralı (k) | kitaplık sınırı | uygulanan sınır (maks 0,50) |
|---|---|---|---|---|---|
| GOVDE_ORAN | DÜŞÜK | 14 | 12 | 0,520 | 0,520 |
| F5 | YÜKSEK | 16 | 13 | 0,581 | 0,581 |
| BOY_GRAFIK_ORAN | DÜŞÜK | 14 | 12 | 0,511 | 0,511 |

Yönlü sıra: YÜKSEK yönlüde evren sırası, DÜŞÜK yönlüde 1 - sıra. Ham değer karşılığı BIST'te aynı yüzdelikteki değerdir.

## 3. Havuz ve seçilen pencere sayıları

| | BIST | ABD |
|---|---|---|
| bütün pencereler (L x pencere sonu) | 392.035 | 3.534.499 |
| evren (ön şart. kilitli değil) | 375.237 | 3.412.825 |
| + önceki >= 120 bar | 365.580 | 3.340.282 |
| + gövdesiz bar payı <= %30 | 347.147 | 3.320.939 |
| + PUAN ve imza ölçüleri sonlu | 344.630 | 3.320.898 |
| - kitaplıkla örtüşen | 0 | 0 |
| - mum izi bölgeleriyle örtüşen | 1.598 | 5.978 |
| HAVUZ (pencere) | 343.032 | 3.314.920 |
| havuz hisse sayısı | 457 | 4.246 |
| D1 seçilen (ham / tekil) | 33.845 / 5.907 | 315.142 / 49.717 |
| D2 seçilen (ham / tekil) | 56.276 / 5.709 | 418.699 / 42.427 |
| D1 havuzun yüzde kaçı (ham) | 9,87 | 9,51 |
| D2 havuzun yüzde kaçı (ham) | 16,41 | 12,63 |
| D3 komşusu bulunan çöl (en az 8 ortak ölçü) | 15 | 15 |

D3: çöl başına en yakın komşu uzaklığı (ortalama mutlak sıra farkı; küçük = yakın):

| çöl | BIST | ABD |
|---|---|---|
| 1 BINBN | - | - |
| 2 NUGYO | 0,068 | 0,034 |
| 3 ENSRI | 0,073 | 0,068 |
| 4 TEHOL | 0,050 | 0,076 |
| 5 PAPIL | 0,048 | 0,046 |
| 6 ESCAR | 0,079 | 0,043 |
| 7 KTLEV | 0,051 | 0,031 |
| 8 TEHOL | 0,035 | 0,024 |
| 9 HDFGS | 0,062 | 0,043 |
| 10 ASELS | 0,069 | 0,060 |
| 13 EUREN | 0,043 | 0,074 |
| 16 SMRVA | 0,049 | 0,044 |
| 17 DOGUB | 0,038 | 0,046 |
| 18 MANAS | 0,096 | 0,038 |
| 19 KAPLM | 0,074 | 0,087 |
| 20 KRVGD | 0,068 | 0,073 |

## 4. D2 imza koşullarının havuzda sağlanma payı

| koşul | BIST | ABD |
|---|---|---|
| GOVDE_ORAN (DÜŞÜK) | 47,1 % | 47,9 % |
| F5 (YÜKSEK) | 42,4 % | 41,2 % |
| BOY_GRAFIK_ORAN (DÜŞÜK) | 47,2 % | 48,8 % |

Kaç koşulu birden sağlayan pencere (havuz):

| sağlanan koşul | BIST | ABD |
|---|---|---|
| 0 / 3 | 87.788 | 709.784 |
| 1 / 3 | 97.611 | 1.056.246 |
| 2 / 3 | 101.357 | 1.130.191 |
| 3 / 3 | 56.276 | 418.699 |

## 5. Kitaplığın kendisi (örneklem içi yakalama; bölgeler kuralı kurdu, bu bir sağlama, bulgu değil)

- D1 (PUAN_ESIT sırası >= 0,90): 3 / 16 çöl.
- D2 (bütün imza koşulları): 7 / 16 çöl; koşul başına sağlayan çöl: GOVDE_ORAN 12, F5 13, BOY_GRAFIK_ORAN 12.
- Çöl başına sağlanan D2 koşulu: 1 BINBN 1/3, 2 NUGYO 2/3, 3 ENSRI 2/3, 4 TEHOL 3/3, 5 PAPIL 3/3, 6 ESCAR 2/3, 7 KTLEV 1/3, 8 TEHOL 3/3, 9 HDFGS 3/3, 10 ASELS 3/3, 13 EUREN 3/3, 16 SMRVA 2/3, 17 DOGUB 2/3, 18 MANAS 2/3, 19 KAPLM 2/3, 20 KRVGD 3/3.

## 6. Yorum gerektiren noktalar (ana modele)

- D2 sınırı sıra uzayında: BIST'te ham değer sınırıyla aynı; ABD'de pazarın kendi evren sırası (ham değerler pazarlar arasında karşılaştırılamaz).
- D3'te kitaplık çölünün boş ölçüsü (kısa geçmiş) uzaklığa girmez (ortak sonlu boyutlar); komşu çölün L* sınıfından seçilir.
- Havuzdan ayrıca Cemal'e daha önce gösterilmiş mum izi bölgeleriyle örtüşen pencereler çıkarılır (körlük); kitaplık 2024-26, havuz <= 2022: örtüşme beklenmez, kural yine uygulanır ve sayılır.
- Sayfa: MUM_IZI_HAKEM geçmişli sayfanın grafik fonksiyonu (_hk_grafik_gecmis) ve sınır / yüzde ekseni kuralları içe alınır; sayfa fonksiyonu bu modülde (kutu yazıları '✓ çöl / K kısmen / × değil'; 'Senin kalıbın' mum izi şablonu ve mum boyu satırı bu sette YOK: kalıp Cemal'in kendi çölü, sayfada ölçü ipucu verilmez); yakın görünümde önceki 10 bar (iş tanımı).
- Kitaplık sayfaları tam BIST verisinden (2024-26) bölge bitişinde kesilerek çizilir; tarih / hisse yok.
- SAPMA: iş tanımındaki imza kuralı hiç ölçü seçmedi; ana modelin ek kuralı (bkz. 1a). D2 / D3 ek kuralla kuruldu; kitaplığın D2'yi geçmesi örneklem içidir (kural kitaplıktan kuruldu).
- D1'de sınır 'en yüksek puanlılar' için pazar ve L içinde üst %10 seçildi (Ç262 dilimi); sayfalar sıralamanın en üstünden alınır.
- D2 'kitaplığın tarafı' = yönlü sıra >= 0,50; 'gevşek %20 sınırı' = kitaplık yönlü sıralarının 16'da 13'ünün sağladığı en büyük alt sınır; ikisinin büyüğü.
- Dedektör sayfaları sıralamanın en üstünden: kod en çok benzettiğini gösterir; bütün seçilen kümeyi temsil etmez (rapor bunu yazar).
- Onay setinde her hisse bir kez; kol ve pazar sayıları sabit (GT_ESIK['kol_pazar']); D2 bir pazarda yetmezse öteki pazardan tamamlanır, yine eksikse eksik kalır.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; ölçüm yok: getiri hesaplanmaz)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
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
