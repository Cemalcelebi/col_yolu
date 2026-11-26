# MUM_IZI8 RAPOR (2026-11-26): v5 (etiketlerle seçilen evre kuralı) + Cemal'in kesin şartı M -> v5M; 'kod nasıl tespit ediyor' onay PDF'i

İş tanımı: MUM_IZI8_IS_TANIMI.md (a67a77a) + ana modelin EK'i (Cemal 26 Kas: "Mum yapısı küçük, altta fitil az ya da yok, üstte uzun fitil; mum bu şekilde
KESİN."). Ön kayıt: MUM_IZI8_ON_KAYIT.md (215e28d). Kod: MUM_IZI_V5.py, test_mum_izi8.py (10 / 10). GETİRİ / SONRASI YOK. Veri <= 2022-12-31.
Seçim 61 etiketin İÇİNDE yapıldı (ezber riski); gerçek sınama Cemal'in MUM_IZI8_ONAY.pdf işaretleri.

## SONUÇ (tek bakışta)

- Seçilen aday R4 = yapı + alt bantta gel-git + yeşil mumla kalıcı çıkış + düzenli tırmanış (fiyat) + bandın içinden: 61 etikette VAR 15, isabet 0,53, yakalama 0,50, kappa 0,35 (%95 0,08-0,61); iki sette aynı yön (0,42 / 0,32).
- Nihai v5M = R4 ∧ M (Cemal'in kesin şartı): VAR 5, isabet 0,80, yakalama 0,25, kappa 0,29 (0,03-0,55).
- Cemal'in KENDİ 16 EVET sayfasının yalnız %50'si M'yi geçiyor (45 HAYIR'ın %36'sı): sözle konan kesin şart kendi işaretlerinin yarısını dışarıda bırakıyor.
- Sentetik (v5M): pozitif %10 gürültüde %45 (ölçüt %50: GEÇMEDİ); geçerli negatifler n1 %0, n2 %0, n5 %0,9 (<= %10); rastgele 0,46 / 1.000 bar (<= 1). PDF kapağında 'geçmedi' yazıyor.
- Evrende v5M (evren içi, tekil): günlük ABD 3.326 / AVR 449 / BIST 837; haftalık ABD 1.013 / AVR 151 / BIST 235. Hisse-yıl başına günlük 0,12-0,32, haftalık 0,015-0,08.
- MUM_IZI8_ONAY.pdf: 26 sayfa (kapak + şablonda okuma + 24 rastgele v5M bölgesi: günlük 12, haftalık 12; ABD 17, AVR 5, BIST 2). Onay eşiği 19 / 24. Beklenti %45-65 ✓.

## ADAY TABLOSU (61 etiket: 16 EVET / 45 HAYIR; sayfanın kendi penceresi)

| kural | parçalar | VAR | EVET-VAR / HAYIR-VAR | isabet | yakalama | kappa (%95) | set 1 (VAR, EVET-VAR, kappa) | set 2 (VAR, EVET-VAR, kappa) |
|---|---|---|---|---|---|---|---|---|
| R1 | Y G1 G2 | 26 | 10 / 16 | 0,38 | 0,62 | 0,224 (-0,01..0,46) | 9, 3, 0,070 | 17, 7, 0,323 |
| R2 | R1 + S | 10 | 4 / 6 | 0,40 | 0,25 | 0,133 (-0,12..0,39) | 9, 3, 0,070 | 1, 1, 0,159 |
| R3 | R1 + T | 17 | 8 / 9 | 0,47 | 0,50 | 0,294 (0,03..0,54) | 5, 3, 0,339 | 12, 5, 0,275 |
| R4 | R3 + I | 15 | 8 / 7 | 0,53 | 0,50 | 0,352 (0,08..0,61) | 4, 3, 0,423 | 11, 5, 0,317 |
| R5 | R3 + B | 11 | 5 / 6 | 0,45 | 0,31 | 0,199 (-0,07..0,46) | 4, 2, 0,192 | 7, 3, 0,206 |
| R6 | R3 + I + B | 10 | 5 / 5 | 0,50 | 0,31 | 0,229 (-0,04..0,49) | 3, 2, 0,273 | 7, 3, 0,206 |
| R7 | R6 + F | 7 | 4 / 3 | 0,57 | 0,25 | 0,224 (-0,04..0,49) | 3, 2, 0,273 | 4, 2, 0,186 |
| R8 | R6 + S | 3 | 2 / 1 | 0,67 | 0,12 | 0,139 (-0,06..0,38) | 3, 2, 0,273 | 0, 0, 0,000 |
| v5M = R4 + M | | 5 | 4 / 1 | 0,80 | 0,25 | 0,293 (0,03..0,55) | 4, 3, 0,423 | 1, 1, 0,159 |

Parça geçme payı (EVET / HAYIR): Y %94 / %64, G1 %75 / %42, G2 %69 / %51, T %75 / %33, I %94 / %58, B %63 / %51, F %81 / %49, S %50 / %40.

M ve alt koşulları Cemal'in işaretlerinde (geçme payı EVET / HAYIR; medyan EVET / HAYIR):
- M (dördü birden): %50 / %36
- m1 gövde / boy <= 0,45: %69 / %60 (0,397 / 0,413)
- m2 alt fitil / boy <= 0,25: %81 / %62 (0,215 / 0,234)
- m3 üst fitil / boy >= 0,33: %56 / %49 (0,339 / 0,324)
- m4 üst / alt fitil toplamı >= 1,5: %69 / %40 (1,66 / 1,24)
- Şablon: 0,379 / 0,203 / 0,419 / 3,59 (toplam / toplam; ana modelin notundaki ~2,96 başka bir oranla hesaplanmış olmalı); M geçiyor. Şablon bütün parçalardan geçiyor.

## SEÇİM

- Kural (önceden): VAR >= 8 adaylar (R1-R6) içinde en yüksek kappa R4 (0,352); 0,03 içinde başka aday yok -> R4. Kappa > 0,20: DUR yok.
- Çapraz set (bilgi): set 1'de seç (VAR en az 4) -> R4 (set 1 kappa 0,42), set 2'de kappası 0,32; set 2'de seç (VAR en az 5) -> R1 (set 2 kappa 0,32), set 1'de kappası 0,07. Seçim hangi sete bakıldığına göre oynuyor (R4 / R1); R4 iki sette de pozitif.
- Nihai v5M = R4 ∧ M (M etiketle seçilmedi; Cemal'in sözü). M VAR'ı 15'ten 5'e indiriyor: isabet 0,53 -> 0,80, yakalama 0,50 -> 0,25.

## SENTETİK (bantlar sentetik seride yeniden hesaplanır; 200 tohum x 2 üretici x 2 bağlam x 3 gürültü; başarı = gerçek sonun +-3 barında VAR)

v5M (nihai; ölçüt bunun için):

| tür | kendi ölçüsü (ihlal payı) | geçerli mi | VAR |
|---|---|---|---|
| pozitif | | | %41,8 (gürültü 0 / 0,1 / 0,2: 49,4 / 45,4 / 30,6; dip 57 / yatay 27) |
| n1 fitilsiz büyük gövde | B (%99,8) | GEÇERLİ | %0 |
| n2 fitiller ters | M (%100) | GEÇERLİ | %0 |
| n3 mumlar 2 kat | B (%70,4) | kurgu geçersiz | (%36,6) |
| n5 yatay yol | T (%99,2) | GEÇERLİ | %0,9 |
| n6 V dönüş | G1 (%67,7) | kurgu geçersiz | (%14,9) |
| n7 üst bandın dışından | I (%45,4) | kurgu geçersiz | (%35,5) |
| n8a kırmızı boşluklu çıkış | G2 (%74,1) | kurgu geçersiz | (%21,4) |
| n8b tek dev mum | çıkış gövdesi > 0,9 (%71,9) | kurgu geçersiz | (%34,0) |
| rastgele | | | blok 0,47, ry 0,46 / 1.000 bar |

- Ölçüt: pozitif >= %50 GEÇMEDİ (%45,4); geçerli negatifler <= %10 GEÇTİ; rastgele <= 1 GEÇTİ. Toplam GEÇMEDİ (yalnız pozitif yakalama).
- Seçilen R4 için (bilgi): pozitif %52,0 (geçer); geçerli negatifler n1 %47,3 (B kuralda yok: fitilsiz büyük gövdeyi ayırmıyor), n5 %1,2; rastgele 7,7-8,9 / 1.000 bar (ölçüt 1: GEÇMEDİ). M eklenince n1 / n2 %0'a ve rastgele 0,46'ya iniyor, pozitif %52 -> %45.
- Kurgusu geçersiz beş negatif (n3, n6, n7, n8a, n8b): sentetik bantta hedef koşulu tohumların %80'inden azında bozuyor; sayılmadı (EK 5 / EK 7 dersi uygulandı). Parantez içindeki VAR payları bilgi.

## SAYIM (tekil, getirisiz; hisse-yıl = bar / 252 günlük, / 52 haftalık)

| dilim / pazar | hisse | hisse-yıl | R4 olay (evren içi) | R4 / hisse-yıl | v5M olay (evren içi) | v5M / hisse-yıl (evren içi) |
|---|---|---|---|---|---|---|
| günlük ABD | 4.402 | 23.669 | 46.648 (34.483) | 1,97 | 5.288 (3.326) | 0,22 (0,14) |
| günlük AVR | 571 | 3.756 | 7.950 (6.447) | 2,12 | 611 (449) | 0,16 (0,12) |
| günlük BIST | 467 | 2.613 | 4.303 (2.712) | 1,65 | 1.197 (837) | 0,46 (0,32) |
| haftalık ABD | 4.303 | 55.988 | 22.691 (15.846) | 0,41 | 1.785 (1.013) | 0,03 (0,02) |
| haftalık AVR | 570 | 9.957 | 4.362 (3.280) | 0,44 | 221 (151) | 0,02 (0,02) |
| haftalık BIST | 449 | 2.888 | 973 (571) | 0,34 | 376 (235) | 0,13 (0,08) |

- v5M yılda hisse başına günlükte ~0,1-0,3 kez, haftalıkta ~0,02-0,08 kez: R4'ün 1/9'u kadar seyrek. BIST'te v5M oranı (0,32) ABD / AVR'nin 2-3 katı (mum yapısı BIST'te daha sık).
- KASA kapısı açık (en geç 2022-12-30); P2 / BIST maskeleri MUM_IZI_ETIKET2 ile aynı.

## ONAY SETİ

- MUM_IZI8_ONAY.pdf: 26 sayfa. s1 'KOD NASIL TESPİT EDİYOR' (8 satır: parçalar Cemal'in diliyle, M satırı, 61 işaretle uyum (16 EVET'ten 4'ü bulundu; 5 VAR'ın 4'ü EVET), tekrar uyumu 8'de 6, sentetik uyarısı). s2 şablonda kodun okuması (mavi gel-git, yeşil ok çıkış, turuncu tırmanış; parça sayıları ve M'nin dört sayısı). s3-26: 24 v5M bölgesi (haftalık 12, günlük 12; ABD 17, AVR 5, BIST 2), her birinde aynı renklerle okuma + M sayıları + ✓ / × + 'yanlış okunan parçayı daire içine al'. Hisse / tarih / sonrası yok (pdftotext denetimi 0 eşleşme).
- Seçim: evren içi tekil v5M olaylarından RASTGELE, tohum 25112083; uygun olay günlük 4.508, haftalık 1.368 (önceki setlerin hisseleri hariç); hisse başına bir; önceki iki setle kesişim 0; en geç bölge sonu 2022-07-26.
- Anahtar: mum_izi8_onay_anahtar.json (MÜHÜRLÜ; PDF'e girmez). Yol: arastirma_cikti/mum_izi/MUM_IZI8_ONAY.pdf.
- Beklenen ✓ payı: etiketlerde v5M isabeti 0,80 (5 VAR, aralık geniş), R4 0,53; Cemal'in kendi tekrar uyumu %75 -> kaba beklenti %45-65 ✓; 19 / 24 beklenmiyor ama dışlanmıyor.

## KONTROL LİSTESİ

- K1 EVET: kappa bootstrap; negatifler kendi ölçüsünde doğrulanıp sayıldı; rastgele taban.
- K2 EVET: b her mumun kendi gününe kadarki bantla; seri t'de kesilince aynı sonuç (test); KASA kapısı; veri <= 2022-12-31.
- K3 EVET: geçerli bar, haftalıkta eksik haftalı pencere yok, BIST medyan üstü, ABD / AVR P2.
- K4 EVET: tekil < 15 mum (en yüksek v1 S); onayda hisse başına bir; etiketlerde tekrar sayfaları dışarıda.
- K5 UYGULANMAZ. K6 EVET. K7 EVET.
- K8 EVET: seçim iç örnek (ezber riski yazıldı); çapraz set R4 / R1 oynuyor; v5M 5 VAR'la isabet aralığı geniş.
- K9 EVET: ön kayıt (215e28d) taramadan önce; v5_kapi tarama başında geçti.
- K10 EVET: etiket eşlemesi 61 / 16 denetlendi; set 1'de v1 S = anahtar S.
- K11 EVET: 61 sayfada vektörlü parçalar = düz döngü (M dahil); R1-R8 tablosu M eklenince yeniden üretildi ve birebir aynı çıktı.
- K12 EVET: seçim önceden yazılı kuralla; 'iz' sözü yok.
- K13 EVET: eski kodlar, defterler, UC_IZ2 değişmedi; yalnız kendi yollarım commit.
- K14 UYGULANMAZ.

## HATA

1. (süreç; benim) Aday tablosu ve R4 sentetiği, M şartı gelmeden commit edildi (31be2c2); ön kayıt henüz commit edilmemişti, sıra bozulmadı (M kodlandı, tablo yeniden üretildi, aynı çıktı). Hata değil ama iki commit'te iki farklı aday json'u var; geçerli olan 5ee48cb.
2. (sunum; benim) PDF sayfa 2'de M satırı ilk üretimde sağ kenardan taştı (telefonda okunmazdı); satır ikiye bölündü ve PDF yeniden üretildi. Bu, ön kayıttan sonra koddaki tek değişiklik (SAPMA 1).
3. (bilgi) Ana modelin notunda şablon m4 '~2,96'; tanım (toplam üst / toplam alt fitil) ile 3,59. Karar etkisi yok (ikisi de >= 1,5).

## SAPMA

1. Ön kayıttan sonra MUM_IZI_V5.py'de yalnız PDF sayfa 2 metninin satır kırılımı değişti (kural, eşik, seçim aynı: ESIK8_SHA 02b79be4... değişmedi; KOD8_SHA ön kayıtta af74ac0e..., şimdi 2bd267ad...). Tarama bu değişiklikten önce, ön kayıtlı kodla koştu; PDF yeni kodla yeniden üretildi (ilk PDF silindi, gönderilmedi).
2. Cemal'in EK şartı (M) iş tanımından sonra geldi; ön kayıttan ÖNCE işlendi (ön kayıtta 'Cemal'in EK şartı' bölümü).

## ÖNERİLEN DEFTER SATIRLARI (ana model işler)

- IK_KAYIT Ç234: MUM_IZI EK 8 v5. 61 etikette 8 adaydan önceden yazılı kuralla R4 (yapı + gel-git + yeşil kalıcı çıkış + fiyatla düzenli tırmanış + bandın içinden; kappa 0,35, isabet 0,53, yakalama 0,50) seçildi; Cemal'in kesin şartı M (küçük gövde, az alt fitil, uzun üst fitil) eklenince v5M: VAR 5, isabet 0,80, yakalama 0,25, kappa 0,29. M Cemal'in kendi EVET sayfalarının %50'sinde geçiyor. Sentetik v5M pozitif %45 (ölçüt %50: GEÇMEDİ), geçerli negatifler ve rastgele geçti. Evren v5M hisse-yıl başına günlük 0,12-0,32, haftalık 0,02-0,08. MUM_IZI8_ONAY.pdf (24 rastgele v5M bölgesi, kodun okuması çizili) Cemal'de; eşik 19 / 24. Getiri yok. İç örnek seçim (ezber riski). Commit 31be2c2 / 5ee48cb / 215e28d / (sonuç).
- IK_GOREV: 26 Kas, EK 8 v5 + M + onay PDF'i; açık: Cemal'in işaretleri.
- IK_HATA: (bilgi) sözle konan 'kesin' şart (M) kendi EVET işaretlerinin yarısında yok: sözlü tarif ile göz arasındaki fark ölçüldü (EVET %50 / HAYIR %36).
- IK_ACIK: Cemal MUM_IZI8_ONAY.pdf'i işaretler (✓ / × + yanlış okunan parça); >= 19 / 24 ✓ ise tespit geçerli, sonra ön kayıtlı sonrası ölçümü; değilse yanlış okunan parçalara göre karar.
