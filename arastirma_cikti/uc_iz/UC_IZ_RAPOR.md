# UC_IZ RAPOR — üç fiyat dışı iz aynı KT02 dip olayında (25 Kasım 2026)

**KASA ADAYI: HAYIR.** İki karar hücresinde de hiçbir iz-var grubu n >= 30'a ulaşmadı. N >= 2 olan dip olayı hiç yok. Kural gereği bütün izler ÖLÇÜLEMEDİ, BİRLİKTE ARTIYOR değerlendirilemedi.

Ön kayıt: UC_IZ_ON_KAYIT.md (commit 6333091, 2026-11-25 06:49:55 UTC). Koşu 06:49:56-06:50:13 UTC. Kod 307741f (KOD_SHA 326cbaa1…, ESIK_SHA 6899e36c…). Satır dosyası uc_iz_satir.csv.gz (sha 00aa7af8…), sonuç uc_iz_sonuc.json. Açık veriye bir kez bakıldı.

## Hangi iz hangi veriyle kuruldu
- R (sektör rüzgârı, KT10 aynen: D9 durumu 'c' satırı = RÜZGÂR ∧ ¬D9) KASA açık V_ABD + sektor_ABD.csv ile kuruldu, kapsam 2015-06..2022-12. R_any (D9 şartsız) dip olaylarında R ile aynı çıktı.
- B (bilanço, k28): KURULAMADI. k28_X_abd / pead liste_abd 2022-12-01'de başlıyor. -> YEDEK Y1 = Ç112 blok hacimli taban günü (FI_K38 S3), son 15 geçerli bar.
- I (içeriden alım, k30): KURULAMADI. k30_alim 2022-01-03'te başlıyor (2016-21 Form 4 repoda yok). -> YEDEK Y2 = Ç223 T (uyum_toplam, PFc <= -0,10 ∧ MRc >= 0,30), son 15 geçerli bar. Bilgi I22 yalnız 2022 olaylarında.
- B0 kurulamadı. 2010-15 bilgi hücresi yok (fiyat 2015-06'da başlıyor).
- Dip olayı: KT02 341 olay; 329'u eşli (d1619 134, d2022 195).

## Tablo 1 — tek izler (FARK = R15 olay − eş ortalaması, yüzde puan; [ay kümeli boot %95])
| iz | hücre | n var / yok | FARK var | var − yok | SIRA | güç | hüküm | ÜST10 − taban_f [%95] | ALT10 − taban_f |
|---|---|---|---|---|---|---|---|---|---|
| R | d1619 | 6 / 128 | +3,20 [−4,98; +7,82] | +2,59 | 0,685 | 0,06 | ÖLÇÜLEMEDİ | +4,2 [−13,5; +48,2] | −12,4 |
| R | d2022 | 9 / 186 | −7,13 [−18,14; +2,55] | −6,76 | 0,405 | 0,06 | ÖLÇÜLEMEDİ | −0,9 [−12,5; +25,5] | +32,5 |
| Y1 | d1619 | 0 / 134 | - | - | - | - | ÖLÇÜLEMEDİ (n 0) | - | - |
| Y1 | d2022 | 0 / 195 | - | - | - | - | ÖLÇÜLEMEDİ (n 0) | - | - |
| Y2 | d1619 | 3 / 131 | +8,66 [+6,40; +12,89] | +8,11 | 0,890 | 0,04 | ÖLÇÜLEMEDİ | +20,4 [−14,3; +87,9] | −13,0 |
| Y2 | d2022 | 10 / 185 | +0,26 [−4,22; +6,57] | +0,99 | 0,482 | 0,06 | ÖLÇÜLEMEDİ | −1,1 [−11,7; +22,8] | −1,1 |
| I22 (bilgi) | d2022 | 8 / 110 | −3,09 [−3,89; −0,29] | −3,12 | 0,436 | 0,06 | ÖLÇÜLEMEDİ | −10,8 | −10,8 |
| hepsi | d1619 | 134 | +0,73 [−1,18; +2,60] (medyan +0,84) | | 0,521 | 0,51 | ÖLÇÜLEMEDİ | +4,2 [−1,6; +10,8] | +4,2 |
| hepsi | d2022 | 195 | −0,68 [−2,75; +1,20] (medyan +0,03) | | 0,498 | 0,55 | ÖLÇÜLEMEDİ | +1,8 [−2,8; +7,5] | +1,8 |

İz kararları: R ÖLÇÜLEMEDİ (d1619 yön şartları tuttu, d2022 tutmadı; güç 0,06), Y1 ÖLÇÜLEMEDİ (bayraklı olay 0), Y2 ÖLÇÜLEMEDİ (d1619 yön şartları tuttu n 3, d2022 tutmadı). YÖN TUTARLI iz: yok. BH (aile 4): p hepsi 1,0 (n < 30 hücre p'si 1 sayılır), geçen yok.

## Tablo 2 — birlikte (N = R + Y1 + Y2)
| N | hücre | n | FARK [%95] | ÜST10 − taban_f | ALT10 − taban_f | h5 olay / eş | stop olay / eş |
|---|---|---|---|---|---|---|---|
| 0 | d1619 | 125 | +0,42 [−1,52; +2,36] | +3,8 [−1,6; +10,0] | +5,4 | %45,6 / %42,4 | %32,0 / %27,2 |
| 0 | d2022 | 176 | −0,40 [−2,27; +1,73] | +2,1 [−2,6; +8,2] | +0,4 | %55,1 / %50,6 | %35,2 / %38,6 |
| 1 | d1619 | 9 | +5,02 [−0,18; +8,66] | +9,6 [−13,2; +38,4] | −12,6 | %55,6 / %55,6 | %33,3 / %22,2 |
| 1 | d2022 | 19 | −3,24 [−9,58; +2,21] | −1,0 [−11,6; +13,6] | +14,8 | %47,4 / %47,4 | %42,1 / %36,8 |
| >= 2 | iki hücre | 0 | - | - | - | - | - |
Çiftler R∧Y1, R∧Y2, Y1∧Y2: n 0 (iki hücrede). BİRLİKTE ARTIYOR: HAYIR (N >= 2 yok; d2022'de N=1 < N=0).
Eş h5 / stop = plasebo tohum 0 üyesi (aynı gün aynı kova), tek üye, gürültülü. MU.mu_olc_h5 uygulanmadı (stop0 = Low(L2) MACD'ye özgü).
Piyasa yönü (bilgi, hepsi): eş ortalaması > 0 günlerde FARK −1,00 / −1,42; <= 0 günlerde +3,45 / +1,03 (d1619 / d2022).
İkinci eş (aynı gün N = 0 dip olayları) bilgi: hepsi fark2 +0,37 / +0,31.

## Ölçülen şans tabanları (ÜST10)
- Formül (olay başına (N − tavan(0,9 N) + 1) / (N + 1) ortalaması): d1619 %12,9, d2022 %11,5 (hepsi). ALT10 formülü aynı: %12,9 / %11,5. Medyan eş sayısı 28 (5..153). Taban %10 değil, çünkü eş sayısı küçük.
- Plasebo (aynı gün aynı kova rastgele üye, 200 tohum): ÜST10 %13,2 / %11,5; ALT10 %12,8 / %11,3. Formülle uyumlu.
- Gözlem (sayı): hepsi grubunda ÜST10 %17,2 / %13,3 ve ALT10 %17,2 / %13,3, yani iki kuyruk birlikte tabanın üstünde. Yorum (çıkarım, doğrulanmadı): dip olayları kovasına göre bile daha oynak; yön bilgisi değil.

## Doğrulamalar
- D1: KT02 olayları KART_TUR2 açık çıktısıyla aynı tanım, ama sayılar birebir değil. 2016-01..2022-11: k2 1.167 / UC 336, ortak 331. Ortak sembollerde UC'nin 331 olayının hepsi k2'de. Kalan 5 olay, k2'de KT02'si olmayan 4 sembolde. Fark nedeni (doğrulanmış): k2 KASA 2 tezgâh verisiyle koşuldu (geniş ABD evreni, 2000'den), burada yalnız KASA 1 V_ABD var (1.361 hisse, 2015-06'dan). k2'nin ortak sembollerdeki 22 fazla olayının nedeni çıkarımdır: P2 havuzu / 60 gün tekil zinciri farklı veri başlangıcına bağlı. KT10 örtüşmesi düşük (ortak 7.558 / UC 16.511), çünkü sektör sepeti evren ortalamasıdır.
- D2: prefix testi (veri 2019-06-28 ve 2021-06-30'da kesildi): 100 / 100 ve 161 / 161 olay birebir, R / Y1 / Y2 / I22 bayrak farkı 0. 30 rastgele olayda ham olay günü <= t. Olay dosyaları <= 2022-12-31 kesildi ve assert edildi (k30'dan 5.702 satır atıldı). İş tanımındaki "olay başına t'de kesme" yerine bu yapıldı. Y2 kaynak dosyası yeniden hesaplanmadı; o dosya Ç217 / Ç223 prefix denetiminden geçmişti.
- D3: Y1 bayraklı olay yok. 10 / 10 Y2 satırı uygun (PFc, MRc eşikte, T günü <= t). 8 / 8 I22 Form 4 satırı uygun (t'den 23-29 gün önce, değer >= 10 bin $). Ham dosyadan bağımsız okuma: APG 2022-06-22 546.966 $ Director; HWM 2018-07-03 PFc −0,294, MRc 0,517.
- D4: satır dosyasından düz pandas ile yeniden üretildi. Hepsi d1619: n 134, FARK +0,7296, SIRA 0,5207, ÜST10 %17,16, taban %12,94, plasebo %13,16. N=1 d2022: n 19, FARK −3,2386. R=1 d2022: n 9, FARK −7,1265. Hepsi JSON'daki değerlerle aynı.

## Dürüst okuma
- Sonuç: üç izden hiçbiri bu ortamda ölçülemedi. İki asıl iz (bilanço, içeriden alım) için 2016-22 olay verisi bu ortamda yok. Yedekler dip olayıyla neredeyse hiç çakışmıyor (Y1 0, Y2 13, R 15 / 329).
- Asıl kısıt: KT02 dip olayı bu evrende az (329 eşli). Tek iz bile her hücrede n 30'a ulaşamıyor.
- Hayatta kalma (K7): evren bugün işlem görenler; dipteki olaylarda sonuç yukarı yanlı.
- Sıradaki deneme için not (öneri, ölçülmedi): bilanço ve içeriden alım izleri ancak (a) 2016-22 Form 4 / bilanço günü verisi yeniden indirilirse (Cemal izni gerekir) ya da (b) dip olayı daha geniş tanımlanırsa ölçülebilir. (b) yeni tanım olur ve ayrı ön kayıt ister.
