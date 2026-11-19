# YAPI_HEDEF — DEVİR 1 BİRLEŞTİRME (2026-11-19)

Girdi: DEVIR_1_RAPOR.md (koşu 451acc3), DEVIR_1_ON_KAYIT.md (87173a0), devir1_sonuc.json ve üç eleştiri lensi (yeniden üretim, sızıntı kontrolü, çürütme). Karar pazarı ABD+AVR; değerler yüzde puan (P = 15 barda +%5 hedefin stop'tan önce görülme payı). FARK = P olay - P eş. MARJ = FARK(süzgeçli) - FARK(kol tabanı). Kol A = bütün Y1 olayları; kol B = Y9 alt kümesi (F15 <= 0,25 VE F17 <= -%20).

**SONUÇ: ENTEGRE ET 0 satır. Tek KATKI+ satırı (W2 kol B) çürütme lensinde düştü ve ÖLÇÜLEMEDİ düzeyine indi. KATKI− 11 satır, SORGULA 24 satır, KATKI+ 1 satır (düştü). Sızıntı lensi karne kuralında yapısal eksik buldu (dönem tamponu yok, K1 için mekanik kontrol yok); bu yüzden karne bir sonraki devirde düzeltilmiş kuralla yeniden koşulur.** Bu belgede iz, emare ya da bulgu iddiası yoktur.

## 1. Aday tablosu (ABD+AVR)

Eleştiri sonucu sütunundaki kısaltmalar: YÜ = yeniden üretim lensi (1.824 karşılaştırmanın hepsi TUTTU), SZ = sızıntı lensi (genel olarak TUTMADI: tampon yok, K1 kanıtı eksik; bütün satırları etkiler), ÇR = çürütme lensi (yalnız W2 B'ye özel olarak uygulandı).

| Aday | Kol | Eğitim n / FARK | Sınama n / FARK | Etiket | Eleştiri sonucu |
|---|---|---|---|---|---|
| W1 | A | 3037 / -0,14 | 1818 / +1,13 | SORGULA | YÜ tuttu (sınama hücresi birebir); SZ genel |
| W1t | A | 3035 / -0,06 | 2097 / -0,67 | SORGULA | YÜ tuttu; SZ genel |
| W2 | A | 2723 / -2,15 | 1838 / -2,32 | KATKI− | YÜ tuttu; ÇR: aynı süzgeç kol A'da eksi, yani yön kola göre değişiyor |
| W2t | A | 2725 / +1,90 | 1830 / +2,28 | SORGULA | YÜ tuttu; MARJ üç hücrede artı, stop şartı sınamada tutmadı (%25,8'e karşı %25,1) |
| W2D | A | 2725 / +0,01 | 1723 / +1,89 | SORGULA | YÜ tuttu; stop şartı eğitimde tutmadı |
| W2Dt | A | 2723 / -2,32 | 1917 / -1,00 | KATKI− | YÜ tuttu |
| W3 | A | 2723 / -3,35 | 1470 / -3,91 | KATKI− | YÜ tuttu (sınama hücresi elle denetlendi) |
| W3t | A | 2725 / +1,20 | 1763 / +3,85 | SORGULA | YÜ tuttu; MARJ üç hücrede artı, stop şartı eğitimde tutmadı |
| W4 | A | 2935 / -1,06 | 1724 / -0,61 | KATKI− | YÜ tuttu |
| W4t | A | 2435 / -2,37 | 1463 / -1,71 | KATKI− | YÜ tuttu; tanım ön kayıttan önce düzeltildi (F34 > 0), getirisiz gerekçeyle |
| W5a | A | 2725 / +2,16 | 1900 / -0,04 | SORGULA | YÜ tuttu; sınamada FARK sıfırda |
| W5b | A | 3296 / -2,48 | 2158 / -2,46 | KATKI− | YÜ tuttu (üç hücre elle denetlendi) |
| W6 | A | 3294 / -4,54 | 1762 / -3,53 | KATKI− | YÜ tuttu |
| W6t | A | 3295 / +4,87 | 2670 / +2,30 | SORGULA | YÜ tuttu; MARJ artı, olayın stop payı eşinkinden yüksek (eğitim %26,7'ye %24,4, sınama %31,4'e %26,9) |
| E1 | A | 4965 / -0,80 | 2873 / -0,17 | SORGULA | YÜ tuttu (elle denetlendi); ters hücre eğitimle aynı (sabit eşik) |
| E1t | A | 8210 / -0,56 | 5776 / -0,53 | SORGULA | YÜ tuttu; ters hücre eğitimle aynı |
| E2 | A | 10021 / +0,64 | 6863 / +1,53 | SORGULA | YÜ tuttu; MARJ artı, stop şartı iki dönemde de tutmadı |
| E2t | A | 3148 / -4,71 | 1780 / -7,81 | KATKI− | YÜ tuttu |
| W1 | B | 68 / +8,51 | 65 / +12,36 | SORGULA | YÜ tuttu; n < 1.000 olduğu için ÖLÇÜLEMEDİ |
| W1t | B | 115 / -1,19 | 127 / +3,20 | KATKI− | YÜ tuttu; MARJ eksi (-4,9 / -5,6), ham FARK sınamada artı |
| W2 | B | 41 / +8,27 | 33 / +13,15 | KATKI+ | **ÇR ÇÜRÜTTÜ**: pazar, dönem ve küçük örneklem lenslerinde düştü (ayrıntı bölüm 3) |
| W2t | B | 100 / +8,79 | 128 / +6,24 | SORGULA | YÜ tuttu; sınamada MARJ eksi; ÖLÇÜLEMEDİ |
| W2D | B | 66 / +4,83 | 92 / +7,26 | SORGULA | YÜ tuttu; sınamada MARJ eksi; ÖLÇÜLEMEDİ |
| W2Dt | B | 59 / +6,83 | 46 / +12,27 | SORGULA | YÜ tuttu; ÖLÇÜLEMEDİ |
| W3 | B | 27 / -4,88 | 27 / -0,83 | SORGULA | n < 30, ÖLÇÜLEMEDİ |
| W3t | B | 99 / +3,18 | 116 / +10,24 | SORGULA | YÜ tuttu; eğitimde MARJ eksi; ÖLÇÜLEMEDİ |
| W4 | B | 81 / +0,82 | 68 / +4,14 | KATKI− | YÜ tuttu; MARJ eksi (-2,9 / -4,7) |
| W4t | B | 36 / +5,52 | 56 / +6,49 | SORGULA | YÜ tuttu; ÖLÇÜLEMEDİ |
| W5a | B | 92 / +1,81 | 107 / +9,78 | SORGULA | YÜ tuttu; eğitimde MARJ eksi; ÖLÇÜLEMEDİ |
| W5b | B | 91 / +6,04 | 78 / +6,78 | SORGULA | YÜ tuttu; ÖLÇÜLEMEDİ |
| W6 | B | 21 / +3,01 | 17 / +7,57 | SORGULA | n < 30, ÖLÇÜLEMEDİ |
| W6t | B | 315 / +3,41 | 327 / +7,88 | KATKI− | YÜ tuttu; MARJ eksi (-0,3 / -0,9 / -2,1) |
| E1 | B | 216 / -0,28 | 187 / +10,01 | SORGULA | YÜ tuttu; eğitimde MARJ eksi; ÖLÇÜLEMEDİ |
| E1t | B | 219 / +7,70 | 265 / +7,94 | SORGULA | YÜ tuttu; sınamada MARJ eksi; ÖLÇÜLEMEDİ |
| E2 | B | 261 / +0,27 | 310 / +12,05 | SORGULA | YÜ tuttu (eğitim ve sınama hücreleri elle denetlendi); eğitimde MARJ eksi; ÖLÇÜLEMEDİ |
| E2t | B | 174 / +8,93 | 142 / +1,70 | SORGULA | YÜ tuttu; ÖLÇÜLEMEDİ |

Kol B satırlarında ham FARK çoğunlukla artı çıkıyor, çünkü kol B tabanının kendisi artı (eğitim +3,7). Süzgecin katkısını FARK değil MARJ gösterir.

## 2. ENTEGRE ET

**Yok (0 satır).** Kural: KATKI+ olacak ve üç lensin hepsi tutacak; çürütme lensi satırı özel olarak çürütmediyse de kabul edilir. Bu şartı geçen tek aday W2 B'ydi, o da çürütüldü. Hiçbir süzgeç koda (YAPI_HEDEF ya da üretim zinciri) eklenmez.

## 3. YENİDEN YAP

1. **W2 kol B** (F31 > 0 VE F31 >= q75, kol B içinde). Etiket KATKI+'dan ÖLÇÜLEMEDİ'ye indi.
   - Neden (çürütme lensi):
     - Pazar kırılımı: sınamada ABD n=23, MARJ +6,9; AVR n=10, MARJ -1,6. İki pazarda da n < 30. Eğitimde AVR yalnız 4 olay ama FARK +35,8 ve sonucu o taşıyor. BIST'te işaret ters (eğitim n=34, MARJ -12,3).
     - Dönem kırılımı: eğitimdeki 41 olayın 24'ü 2022'de, bunların FARK'ı +1,0 (kol B tabanının altında). 2025 sınama hücresi eksi (8 olay, FARK -3,0).
     - Küçük örneklem: en çok katkı veren 3 olay çıkarılınca MARJ sıfıra ya da altına iniyor. Bootstrap %95 aralığı eğitimde [-11,2; +19,9], sınamada [-10,6; +19,1]. Rastgele aynı boyutta alt kümede üç hücrenin üçünde de MARJ > 0 çıkma payı yaklaşık %12,9. 36 satırlık bir karnede bir KATKI+ şansla beklenen düzeyde.
     - Aynı süzgeç kol A'da KATKI− çıkıyor (MARJ -1,5 / -1,9). Yönü kola göre değiştiği için iz sayılmaz.
   - Ne değişmeli: KATKI+ şartı her karar pazarında (ABD ve AVR) ayrı ayrı n >= 30 ve MARJ > 0 aramalı. Ay kümeli bootstrap alt ucu > 0 ve 3 olay dışarıda bırakılınca (leave-3-out) MARJ > 0 şartları eklenmeli. F7 / F10 tabakaları içinde ölçülmeli (Spearman F31~F7 0,63, F31~F10 0,46). Mevcut veriyle hücre başına n >= 1.000 mümkün değil; tek yol kriz sonrası verisiyle ileri test.
2. **Karne kuralının kendisi (bütün 36 satır).** Sızıntı lensinde TUTMADI.
   - Eğitim (2016-22) ile sınama (2023-26) arasında 60 günlük tampon yok. YH_ESIK7'de vardı, DEVİR 1'de gerekçesiz kaldırılmış. Aralık 2022 olaylarının 15 barlık sonucu 2023'e taşıyor.
   - K1 için yalnız Spearman raporlanmış, mekanik üstünlük dışlanmamış. Doğru yanıt EVET değil KISMEN olmalıydı.
   - 'Ters yön' hücresi eğitimle aynı 2016-22 olaylarından kuruluyor (E1 / E2'de birebir aynı). Yani 'üç hücre' şartı fiilen iki bağımsız dönemdir.
   - Ne değişmeli: dönem sınırında 60 bar ambargo; ters yön hücresi KATKI+ sayımından çıksın ya da yalnız bilgi olsun; K1 için süzgeçli fark F10 / F15 / F7 tabakası içinde ölçülsün. Bunların hepsi ön kayda sabit eşikle, koşudan önce yazılır.
3. **Kayıt düzeltmesi (süreç).** Bir sonraki iş tanımında kaynak dosyalar doğru adlandırılmalı: olay_Y1.csv.gz + ozellik_Y1_d1.csv.gz + olay_Y9.csv.gz + devir1_esik.json. 'olay_devir1*.csv.gz' adlı bir dosya yok.

## 4. KAPANDI (KATKI−: üç hücrede de MARJ eksi, n >= 30)

- Kol A (her hücrede n >= 1.400, güç yeterli): bu devirde süzgeç adayı olarak kapandı. Satırlar: W2, W2Dt, W3, W4, W4t, W5b, W6, E2t.
  - W2: gün-içi birikim üst çeyrek.
  - W2Dt: D alt çeyrek.
  - W3: Amihud düştü.
  - W4: sıfır getiri payı düştü.
  - W4t: sıfır getiri payı arttı.
  - W5b: ER_10 üst çeyrek.
  - W6: R/MDD üst çeyrek.
  - E2t: yavaş toparlanma.
- Kol B: W1t (n 115 / 127), W4 (81 / 68), W6t (315 / 327). MARJ eksi, ama hücre başına n < 1.000. Bu yüzden 'İZ DEĞİL' değil, **kol B süzgeci olarak kapandı / güç kuralına göre ÖLÇÜLEMEDİ** diye okunur. İleri test yalnız defter kararıyla açılır.

## 5. SONRAKİ DEVİR önerileri (en çok 5; eşikler koşudan önce sabit yazılır)

1. **Karne kuralı v2.** Gerekçe: H-ÇÜR-1, H-ÇÜR-2, H-ÇÜR-3. Kaynak: çürütme lensi; FI_OLCUT bootstrap kapısı. Yeni şartlar:
   - KATKI+ için ABD ve AVR ayrı ayrı n >= 30 ve MARJ > 0;
   - ay kümeli bootstrap %95 alt ucu > 0;
   - leave-3-out MARJ > 0;
   - ters yön hücresi yalnız bilgi.
2. **Dönem tamponu.** Eğitim / sınama sınırında 60 bar ambargo; sınırdaki olaylar iki hücreye de girmez. Gerekçe: sızıntı lensi (c), YH_ESIK7 düzeni. Karne bu kuralla aynı adaylar ve aynı mühürlü eşiklerle yeniden koşulur; eşikler değişmez.
3. **K1 mekanik kontrol.** Her aday için MARJ, F10 (bölge net), F15 ve F7 tercil tabakaları içinde ağırlıklı olarak yeniden hesaplanır; tabaka içi MARJ işaret değiştirirse satır SORGULA olur. Gerekçe: sızıntı lensi (d) ve çürütme lensi (e). Spearman değerleri: F31~F10 0,48, F37~F10 0,43, F35~F10 0,44.
4. **Kol A'da MARJ'ı üç hücrede artı olup stop şartından SORGULA kalan beş satır** (W2t, W2D, W3t, W6t, E2; n 1.700-10.000) v2 kuralıyla yeniden ölçülür. Ek bilgi satırı: stop payı farkı (olay - eş). Kaynak: DEVIR_1_RAPOR.md karne satırları. Bunlar KATKI− satırlarının ters çeyrekleri (W2/W2t, W3/W3t, W6/W6t, E2t/E2). Bu ayna ilişkisi mekanik olabilir (taban etrafında tamamlayıcı çeyrekler), bu yüzden öneri 3'teki kontrol koşulmadan yorum yapılmaz. Stop şartı (olay stop payı <= eş) değiştirilmez.
5. **Bağımsız üçüncü hücre ileri testle.** W2 B ve öneri 4'ün satırları IK_ILERI'ye kaydedilir; sonraki ölçüm kriz sonrası veriyle (Mart 2027) aynı komut ve aynı eşikle yapılır. Gerekçe: 2023-26 hücreleri bakılmış (ön kayıt K8), mevcut veride hücre başına n >= 1.000 kol B için yok. Kaydı yalnız ana model yazar.

## 6. Denetim özeti

- **Ön kayıt sırası: TUTTU.** Ön kayıt b7ee46d 12:04:16 UTC, düzeltilmiş ön kayıt 87173a0 12:04:47, koşu damgası 12:04:51, koşu commit'i 451acc3 12:05:18. devir1_sonuc.json kapi.git_onkayit = 87173a0. Eşik sha'ları iki ön kayıtta ve koşu kapısında aynı. Doğrulanamayan tek nokta: ilk kapı denemesinin b7ee46d'den sonra koştuğu kayıttan ispatlanamıyor. 'Getiri okunmadı' beyanı kodla tutarlı, ama mekanik kanıtı yok.
- **Yeniden üretim: TUTTU.**
  - 48 eşik 1e-9 içinde aynı.
  - 152 karne satırı x 3 blok x 4 ölçü = 1.824 karşılaştırma yapıldı, göreli 1e-3'te uyuşmayan 0, n'ler birebir.
  - Rapor metniyle yuvarlama düzeyinde elle karşılaştırılan hücrelerin hepsi tuttu: W1 A sınama 1818 / +1,13; E2 B eğitim 261 / +0,27; W5b A; W3 A; E1 A; taban.
  - Çürütme lensi W2 B'yi bağımsız kodla yeniden kurdu: 41 / +8,3; 33 / +13,2; 39 / +8,4.
- **Geleceğe bakma: TUTTU, iki küçük not var.**
  - Özellikler t barını okumuyor.
  - Nedensellik denetimi örneklem düzeyinde: pazar başına 25 olay, toplam 75 / 26.663.
  - Yahoo düzeltme çarpanları F33 / F34'e sonradan bilinen bilgi taşıyabilir.
- **Dönem tamponu: TUTMADI** (bölüm 3, madde 2).
- **K1: aşırı iyimser** (EVET yazılmış, KISMEN olmalıydı).
- **Sızıntı (e-posta / anahtar): YOK.** Üç commit diff'inde noreply dışında e-posta yok, anahtar deseni yok.
- **Testler:** test_yapi_hedef.py 283 geçti, 0 kaldı (OC_VERI=/tmp/veri). Yasak dosyalara dokunulmadı.

## HATA (ana modele öneri; IK_HATA'yı yalnız ana model yazar)

- HD1-B1 (ölçüt / süreç): DEVİR 1'de eğitim ile sınama arasında 60 günlük tampon yok, YH_ESIK7'deki tampon gerekçesiz kaldırılmış. Bulan: sızıntı lensi.
- HD1-B2 (kontrol listesi): K1 EVET yazılmış. Mekanik üstünlük dışlanmamış, yalnız raporlanmış; doğru yanıt KISMEN. Bulan: sızıntı lensi.
- HD1-B3 (ölçüt tasarımı): KATKI+ havuzlanmış ABD+AVR'de n arıyor. Pazarlar arası ters yön gizleniyor (W2 B: AVR sınama MARJ eksi). Bulan: çürütme lensi.
- HD1-B4 (ölçüt tasarımı): KATKI+ kuralında belirsizlik kapısı yok (bootstrap / leave-k-out). W2 B, 3 olay çıkarılınca dönüyor. Bulan: çürütme lensi.
- HD1-B5 (yorum riski): 'ters yön' hücresi eğitimle aynı dönem; 'üç hücre' fiilen iki bağımsız hücre. Bulan: sızıntı ve çürütme lensleri.
- HD1-B6 (süreç, doğrulanamaz): ilk kapı denemesinin ön kayıt commit'inden sonra koştuğu kayıttan ispatlanamıyor. Bulan: sızıntı lensi.
- HD1-B7 (iletişim): eleştiri iş tanımında kaynak dosya adı yanlış ('olay_devir1*.csv.gz' yok). Sonucu etkilemiyor. Bulan: yeniden üretim lensi.
- HD1-B8 (rapor eksiği): DEVIR_1_RAPOR.md H-D1-4, W2 B için pazar ve yıl kırılımını vermiyor (eğitimin %59'u 2022'de ve orada FARK tabanın altında). Bulan: çürütme lensi.
