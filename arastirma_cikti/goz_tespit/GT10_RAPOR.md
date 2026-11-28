# GT10 RAPOR — KURAL-4: beş işaretli setten sete göre dışarıda sınanmış kabul kuralı (28 Kasım 2026)

**Düz dille üç satır**
1. **KURAL YOK (bu ölçülerle).** Dört setten öğrenip beşincide sınanan üç kural ailesinin (tek ölçü, en çok 3 şartlı VE, 4 ölçülü lojistik) hiçbiri karar şartlarını geçmedi; etiket karıştırmasını da geçen yok.
2. Set dışı ✓ payı: en iyisi lojistik (C) **%53** (32 kabulün 17'si; sayfa bootstrap %95 [%35; %70]); tek ölçü (A) %43 [%27; %59], VE kuralı (B) %43 [%22; %64]; hepsini kabul %38. Karıştırma (1.000) en iyi aile payının %95'i %56 (C'nin p ~ 0,10). Eşik %70.
3. En büyük kaçak yine **'erken'**: A'nın kabulünde %24, B'de %29, KURAL-3'te %26; C'de erken %16 ama kısmen %19. Yeni setlerde (GT5 + GT9) hiçbir aile KURAL-3'ü (%50) geçmedi: A %50, C %48, B %40.

GETİRİSİZ: hiçbir sayfanın sonrası hesaplanmadı. Etiket: tespit işi ('iz' sözü yok). Sayfa sayısı 126 (iş tanımı 122 yazıyordu; GT3 32 sayfa: ön kayıt SAPMA bölümü).
Sıra: kod 37f1d5d (11:13:47 UTC) -> ön kayıt d5e6ad5 (11:16:17 UTC, push; kontrol kapısı geçti) -> kos tek koşu 11:16:24-11:17:55 UTC (kilit k4/kos_kilit.json) -> olay -> bu rapor.

## Karar tablosu (önceden yazılı şartlar)

| Şart | A | B | C |
|---|---|---|---|
| set dışı kabul >= 25 | 37 ✔ | 21 ✘ | 32 ✔ |
| kabul en az 4 sette | 5 ✔ | 5 ✔ | 4 ✔ |
| ✓ payı >= %70 | %43 ✘ | %43 ✘ | %53 ✘ |
| erken payı <= %20 | %24 ✘ | %29 ✘ | %16 ✔ |
| rastgele kabul <= 1 / 22 | 1 ✔ | 0 ✔ | 1 ✔ |
| GT5 + GT9'da KURAL-3 + 10 puan (K3 %50) | %50 ✘ | %40 ✘ | %48 ✘ |
| ✓ payı > karıştırma %95 (%56,0) | ✘ | ✘ | ✘ |

En yakın üç aday ve neden kaldıkları: (1) C lojistik: kabul yeterli, erken az, ama ✓ payı %53 (eşik %70), yeni setlerde KURAL-3'ten iyi değil, şanstan ayrılmıyor (karıştırmaların %9,5'i en az bu kadar). (2) A tek ölçü: kat katta seçilen ölçü değişiyor (UST_YARI, KUTU_ORAN, EN_BUYUK): kararlı bir tek ölçü yok. (3) B: ikinci / üçüncü şart eğitimde artış verdi, sınamada kabulü 21'e düşürdü, ✓ payını artırmadı (aşırı uyum).

## KURAL-3 ile karşılaştırma (yalnız GT5 + GT9; 44 sayfa)
- KURAL-3 (bu sayfaları o seçti; 26 kabul): ✓ %50 (13), kısmen %12, erken %31 (8), değil %8. Rastgele kabul 0.
- A: 18 kabul, ✓ %50; B: 10 kabul, ✓ %40; C: 21 kabul, ✓ %48 (GT9'da 16 kabul / 6 ✓ / 4 erken).
- Bütün 126 sayfada KURAL-3 %60 (35 kabul) görünür ama GT1 / GT3 / GT4'teki 9 kabulü (8 ✓) örneklem içidir; set dışı karşılaştırma yalnız GT5 + GT9'da anlamlıdır ve orada fark yok.

## Seçim yanlılığı (Tablo 5 yorumu)
GT5 / GT9 sayfalarının 26'sı KURAL-3 ile seçildi: DIPTEN_BAR medyanı 0,71 (GT1 / GT3 / GT4'te 0,33-0,50), Y medyanı 1, KUTU_ORAN maksimumu GT9'da 0,54. Bu setlerde ölçü aralığı dar olduğu için eski setlerde ✓'yi ayıran ölçüler (DIPTEN_BAR, EGIM) yeni setlerde zayıflıyor: H2'de DIPTEN_BAR GT5'te ters yönde (0,47), EGIM GT5 / GT9'da 0,65 / 0,58. Kuralların yeni setlerde KURAL-3'ü geçememesinin bir kısmı bu dar aralıktan; ama aralık içinde de ✓ ile erkeni ayıracak ölçü bu 39 ölçüde yok.

## H2 (✓ - erken; kodun seçtiği 70 sayfa: 42 ✓, 28 erken)
- Önceden yazılı şartı (havuz set dışı AUC >= 0,70 ve >= 4 sette aynı yön) üç ölçü geçti: **EGIM 0,75** (5 / 5 set), **DIPTEN_BAR 0,72** (4 / 5; GT5 ters), **IC 0,70** (5 / 5). Etiket: 'erken ayırıcı adayı'.
- Uyarı (bilgi satırı, ön kayıtlı): 39 ölçüden en iyiyi seçmenin şans düzeyi (set içi karıştırma 1.000) %95'te 0,71: IC bunun altında, DIPTEN_BAR sınırda, EGIM biraz üstünde. Üçü de birbirine yakın şeyi ölçüyor (bölge içinde kapanışların gidişi / dibin yeri) ve güçleri GT1 / GT3 / GT4'ten geliyor (GT3'te 0,91-0,97), yeni setlerde 0,47-0,67.
- Düz dille: 'bölge içinde fiyat yukarı eğimli ve en derin dip ilk yarıda' olan sayfalarda Cemal erken demiyor; bu eski setlerde güçlü, KURAL-3'ün zaten seçtiği yeni sayfalarda zayıf. Tek başına kabul kuralı değil (A ailesi bunu denedi ve %70'e ulaşmadı).

## Tablo 1 — Set dışı (havuz, 126 sayfa)

| Kural | kabul | set | ✓ | K | erken | değil | ✓ payı [%95] | rastgele kabul | ✓ yakalama | karıştırma %95 (T) | karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 37 | 5 | %43 | %14 | %24 | %19 | %43 [%27; %59] | 1 / 22 | %33 | %56 | kaldı: evet_pay>=0,70, erken_pay<=0,20, gt5_gt9>=K3+10, karistirma>q95 |
| B | 21 | 5 | %43 | %5 | %29 | %24 | %43 [%22; %64] | 0 / 22 | %19 | %56 | kaldı: kabul>=25, evet_pay>=0,70, erken_pay<=0,20, gt5_gt9>=K3+10, karistirma>q95 |
| C | 32 | 4 | %53 | %19 | %16 | %12 | %53 [%35; %70] | 1 / 22 | %35 | %56 | kaldı: evet_pay>=0,70, gt5_gt9>=K3+10, karistirma>q95 |
| K3 | 35 | 5 | %60 | %9 | %26 | %6 | %60 [%43; %75] | 0 / 22 | %44 | %56 | baz |
| HEPSI | 126 | 5 | %38 | %12 | %24 | %26 | %38 [%29; %47] | 22 / 22 | %100 | %56 | baz |

Gözlenen T = %53.1; karıştırma (1000 kez) T %95 = %56.0. Seçim: EN İYİ ADAY (C; karar geçmedi).

## Tablo 2 — Set set (set dışı kabul: kabul / ✓ / K / erken / değil)

| Kural | GT1 | GT3 | GT4 | GT5 | GT9 | GT5 + GT9 ✓ payı |
|---|---|---|---|---|---|---|
| A | 10 / 3 / 3 / 2 / 2 | 5 / 3 / 0 / 2 / 0 | 4 / 1 / 2 / 0 / 1 | 10 / 6 / 0 / 2 / 2 | 8 / 3 / 0 / 3 / 2 | %50 (18) |
| B | 5 / 2 / 1 / 0 / 2 | 4 / 2 / 0 / 2 / 0 | 2 / 1 / 0 / 0 / 1 | 3 / 1 / 0 / 1 / 1 | 7 / 3 / 0 / 3 / 1 | %40 (10) |
| C | 5 / 4 / 0 / 0 / 1 | 0 / 0 / 0 / 0 / 0 | 6 / 3 / 3 / 0 / 0 | 5 / 4 / 0 / 1 / 0 | 16 / 6 / 3 / 4 / 3 | %48 (21) |
| K3 | 2 / 2 / 0 / 0 / 0 | 6 / 5 / 0 / 1 / 0 | 1 / 1 / 0 / 0 / 0 | 11 / 7 / 0 / 3 / 1 | 15 / 6 / 3 / 5 / 1 | %50 (26) |
| HEPSI | 30 / 10 / 3 / 3 / 14 | 32 / 15 / 1 / 11 / 5 | 20 / 8 / 4 / 5 / 3 | 21 / 8 / 2 / 5 / 6 | 23 / 7 / 5 / 6 / 5 | %34 (44) |

## Tablo 3 — Kat kuralları (eğitim dört set)

| Aile | sınama seti | kural |
|---|---|---|
| A | GT1 | UST_YARI <= 0.248 |
| A | GT3 | KUTU_ORAN <= 0.09474 |
| A | GT4 | UST_YARI <= 0.1875 |
| A | GT5 | EN_BUYUK >= 0.4944 |
| A | GT9 | KUTU_ORAN <= 0.09459 |
| B | GT1 | UST_YARI <= 0.248 VE DIPTEN_BAR >= 0.25 VE KUTU_ORAN <= 0.4519 |
| B | GT3 | KUTU_ORAN <= 0.09474 VE TEPE_UZAK <= 117 |
| B | GT4 | UST_YARI <= 0.1875 VE DIP_KAYMA >= -0.1427 |
| B | GT5 | EN_BUYUK >= 0.4944 VE DIP_KAYMA >= 0.02541 VE SON_BOY_ORAN <= 1 |
| B | GT9 | KUTU_ORAN <= 0.09459 VE ONCE_DIP <= 0.3271 |
| C | GT1 | lojistik(EN_BUYUK, UST_YARI, DIPTEN_BAR, DIP_KAYMA) >= 0.538 |
| C | GT3 | (boş: kabul yok) |
| C | GT4 | lojistik(EN_BUYUK, KUTU_ORAN, UST_YARI, DIPTEN_BAR) >= 0.458 |
| C | GT5 | lojistik(DIPTEN_BAR, EN_BUYUK, UST_YARI, SON10_EGIM) >= 0.591 |
| C | GT9 | lojistik(KUTU_ORAN, EN_BUYUK, GOV_ORAN, DIPTEN_BAR) >= 0.506 |

## Tablo 4 — H2: ✓ - erken (kodun seçtiği sayfalar; 42 ✓, 28 erken)

| Ölçü | havuz set dışı AUC | bütün veri AUC | GT1 | GT3 | GT4 | GT5 | GT9 | aynı yön set | aday |
|---|---|---|---|---|---|---|---|---|---|
| EGIM | 0,75 | 0,75 | 0,83 | 0,97 | 0,79 | 0,65 | 0,58 | 5 | EVET |
| DIPTEN_BAR | 0,72 | 0,72 | 0,81 | 0,91 | 0,71 | 0,47 | 0,67 | 4 | EVET |
| IC | 0,70 | 0,70 | 0,83 | 0,80 | 0,75 | 0,62 | 0,65 | 5 | EVET |
| YARI_ORT | 0,69 | 0,69 | 0,79 | 0,95 | 0,75 | 0,60 | 0,56 | 5 | hayır |
| UST_YARI | 0,69 | 0,31 | 0,58 | 0,27 | 0,17 | 0,31 | 0,17 | 4 | hayır |

Karıştırma (set içi ✓ / erken, 1000 kez): en büyük havuz AUC'nin %95'i = 0,71. H2 adayları: EGIM, DIPTEN_BAR, IC.

## Tablo 5 — Seçim yanlılığı (set set ölçü aralığı: min / medyan / maks)

| Ölçü | GT1 | GT3 | GT4 | GT5 | GT9 |
|---|---|---|---|---|---|
| D1_sira | 0,05 / 0,95 / 1,00 | 0,20 / 1,00 / 1,00 | 0,01 / 0,61 / 0,99 | 0,12 / 1,00 / 1,00 | 0,18 / 0,95 / 1,00 |
| DIPTEN_BAR | 0,00 / 0,40 / 0,99 | 0,00 / 0,50 / 0,96 | 0,00 / 0,33 / 0,99 | 0,00 / 0,71 / 0,99 | 0,00 / 0,71 / 0,97 |
| KUTU_ORAN | 0,01 / 0,15 / 1,00 | 0,05 / 0,16 / 0,80 | 0,07 / 0,14 / 0,87 | 0,01 / 0,12 / 1,00 | 0,05 / 0,12 / 0,54 |
| KUTU_YER | 0,01 / 0,11 / 0,65 | 0,04 / 0,14 / 0,68 | 0,03 / 0,12 / 0,78 | 0,01 / 0,12 / 0,70 | 0,02 / 0,08 / 0,81 |
| TEPE_KAT | 0,34 / 2,63 / 40,00 | 0,74 / 1,99 / 4,70 | 0,57 / 2,65 / 5,44 | 0,99 / 2,73 / 21,75 | 1,01 / 2,49 / 8,75 |
| Y | 0,00 / 1,00 / 1,00 | 0,00 / 0,00 / 1,00 | 0,00 / 1,00 / 1,00 | 0,00 / 1,00 / 1,00 | 0,00 / 1,00 / 1,00 |

## Tablo 6 — Olay listesi (EN İYİ ADAY (C; karar geçmedi): lojistik(EN_BUYUK, KUTU_ORAN, UST_YARI, DIPTEN_BAR) >= 0.489; getirisiz)

| Pazar | D1 havuz | ölçü hatası | kabul (ham) | olay (tekil 40) | hisse | 2016-19 olay / K3 / gösterildi | 2020-22 olay / K3 / gösterildi |
|---|---|---|---|---|---|---|---|
| ABD | 317992 | 0 | 40502 | 15268 | 3168 | 6333 / 1350 / 18 | 8935 / 2780 / 49 |
| BIST | 34926 | 0 | 4858 | 2216 | 395 | 1143 / 68 / 23 | 1073 / 76 / 22 |

Dosya: /root/.kasa/ham/goz_tespit/k4/k4_olay.pkl (sha e09c26aca2f5); eşikler arastirma_cikti/goz_tespit/gt10_kural4.json.


Karar geçen aile: YOK.



Olay listesi notları: seçilen kural **EN İYİ ADAY (C; karar geçmedi)**: lojistik(EN_BUYUK +, KUTU_ORAN -, UST_YARI -, DIPTEN_BAR +) >= 0,489 (126 sayfayla yeniden kuruldu; 126'nın 41'ini kabul eder; katsayılar gt10_kural4.json). D1 havuzunun %12,7'sini (ABD) / %13,9'unu (BIST) kabul ediyor: ayırıcılığı düşük, kör set için olay havuzu olarak kullanılırsa 'karar geçmemiş aday' diye adlandırılmalı. Olay listesindeki KURAL-3 kesişimi: ABD 4.130 / 15.268 (%27), BIST 144 / 2.216 (%6,5). 'gosterildi' = beş setteki aynı hisse sayfasıyla pencere kesişen olay sayısı (bir sayfa birden çok olayla kesişebilir). K3 bayrağı olc'nin Y + DIPTEN_BAR'ıyla 0 uyuşmazlık. ölçü hatası 0. K7: evren bugün yaşayan hisseler; getirisiz liste olduğu için etkisiz, sonrası ölçülürse yukarı yanlı okunur.

## Denetim / yeniden üretim
- gt10_tablo.json'daki 82 sayfa (GT1 / GT3 / GT4) uc_set_tablo.json ile 35 ölçünün hepsinde birebir (t'de kesik seri ile tam seri aynı: sonrası okunmuyor).
- Bağımsız kısa kodla (set_disi_kabul + tablo): A 37 kabul / ✓ 0,4324 / erken 0,2432 / rastgele 1; B 21 / 0,4286 / 0,2857 / 0; C 32 / 0,5312 / 0,1562 / 1; KURAL-3 GT5 + GT9 26 / 0,50; H2 EGIM havuz AUC 0,7466 (n 70, 42 ✓): özetle birebir.
- Testler: test_goz_kural4.py 12 / 12, test_goz_tespit.py 54 / 54 geçti.

## KONTROL LİSTESİ
Ön kayıttaki tablo (GT10_ON_KAYIT.md; IZ_KARNE.ik_kontrol_kapisi geçti) aynen geçerli. Özet: K1 UYGULANMAZ (getiri yok; bazlar + 22 rastgele + 1.000 karıştırma), K2 EVET (<= t testli, 82 sayfa birebir, <= 2022 assert, seçim yalnız eğitimde), K3 EVET, K4 EVET (sayfa birimi; olay tekil 40), K5 UYGULANMAZ, K6 EVET, K7 EVET (uyarı yazılı), K8 EVET (n küçük; 'bulgu' denmedi), K9 EVET (kod -> ön kayıt -> tek koşu sırası git zamanlarıyla), K10 EVET (sayım 126, 3 satır elle, 44 / 44 K3 bayrağı), K11 EVET (yukarıda), K12 EVET ('iz' yok), K13 EVET (çakışma kapısı; yasak dosyalara dokunulmadı), K14 UYGULANMAZ. Sonradan HAYIR'a dönen madde yok.

## HATA
1. (iş tanımı, sayım) Beklenen 122 sayfa yanlış: GT3 32 sayfa (28 değil), toplam 126. Veri doğru, iş tanımındaki sayı yanlış; durulmadı, ön kayıtta SAPMA olarak yazıldı.
2. (iş tanımı, kurgu) 'KURAL-3 örneklem içi %81': GOZ_TESPIT'in KURAL-3 tanımıyla (D1 sırası + Y + ZAMAN) GT1 / GT3 / GT4'te yalnız 9 sayfa kabul ediliyor (8 ✓). %81'in hangi sayfa kümesinden geldiği bu işte doğrulanmadı; kayıtlardaki sayı ile kodun tanımı arasında fark olabilir, ana model denetlemeli.
3. (iş tanımı, kurgu) H2 karar şartı 39 ölçüden en iyiyi seçmeyi düzeltmiyor: IC şartı geçiyor ama karıştırma %95'inin (0,71) altında. 'Erken ayırıcı adayı' etiketi bu yüzden zayıf okunmalı.
4. (iş tanımı, kurgu) 'GT5 + GT9'da KURAL-3 + 10 puan' şartı, KURAL-3'ün seçtiği dar aralıkta sınanıyor (44 sayfanın 26'sı KURAL-3 kolu): yeni kuralın KURAL-3'ten iyi olma şansı yapısal olarak düşük; şart değişmeden uygulandı.
5. (kendi, süreç) İlk commit denemesinde ortak-yazar satırında model adı vardı (iş tanımı yasaklar); izin reddi üzerine model adı çıkarılarak commit edildi; geçmişte model adı yok.
6. (kendi, yöntem notu) C ailesinin kabul eşiği eğitim içi skorlarla seçiliyor (iyimser); GT3 katında %70 eşiği bulunamadı, o katta kabul 0. Ön kayıttaki tanım budur; sapma değil.
7. (bilgi) goz2/uc_set import edilince logging.disable(INFO) genel olarak açılıyor; GOZ_KURAL4 geri açar (goz2 değiştirilmedi).

## Defter satırı önerisi (ana model işler)
Ç280 | 2026-11-28 | KURAL-4 (GT10): beş işaretli setin 126 sayfasıyla (iş tanımı 122 yazmıştı; GT3 32) sete göre dışarıda (dört setten öğren, beşincide sına) kabul kuralı; aileler A tek ölçü, B <= 3 şartlı VE, C L2 lojistik <= 4 ölçü; bazlar KURAL-3 ve hepsi; set içi etiket karıştırma 1.000; getirisiz | GOZ_KURAL4.py, test_goz_kural4.py | kod 37f1d5d -> ön kayıt d5e6ad5 (kapı geçti) -> tek koşu 11:16 UTC | KURAL YOK (bu ölçülerle). Set dışı ✓ payı A %43 (37 kabul), B %43 (21), C %53 (32; %95 [%35; %70]); hepsi %38; karıştırma %95 %56 (C p ~ 0,10). Erken payı A %24, B %29, C %16, KURAL-3 %26. GT5 + GT9'da KURAL-3 %50 (26), A %50, C %48, B %40: yeni setlerde KURAL-3'ten iyi kural yok. Rastgele kabul 0-1 / 22. H2 (✓ - erken, 70 sayfa): EGIM 0,75, DIPTEN_BAR 0,72, IC 0,70 önceden yazılı şartı geçti (erken ayırıcı adayı) ama çoklu seçim şans düzeyi 0,71 ve güçleri eski setlerden (GT5 / GT9'da 0,47-0,67). EN İYİ ADAY (C) D1 havuzunda ABD 15.268 / BIST 2.216 olay (KURAL-3 kesişimi %27 / %6,5; k4/k4_olay.pkl): ayırıcılığı düşük. Ders: 126 işaretle elde edilen ölçüler Cemal'in ✓'sini %50'nin üstüne taşımıyor; eksik bilgi ölçülerde değil, daha çok işaret / farklı ölçü ailesinde (görüntü, uzak görünüm) aranmalı. Sıradaki: GT10 kör seti KURAL-3 ile işaret biriktirme (Ç279 deneme 3); H2 adaylarının (EGIM, DIPTEN_BAR) yeni sette ileri testi (sabit eşik: havuz AUC >= 0,70, aynı yön).
