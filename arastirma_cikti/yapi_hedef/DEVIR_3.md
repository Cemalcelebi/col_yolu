# YAPI_HEDEF — DEVİR 3 BİRLEŞTİRME (2026-11-19)

Girdiler:
- DEVIR_3_RAPOR.md (koşu b86e035, 13:37:06 UTC).
- DEVIR_3_ON_KAYIT.md (650ded5, 13:36:25 UTC).
- devir3_sonuc.json, devir3_esik.json, devir3_prefix.json.
- Üç eleştiri lensi: yeniden üretim, sızıntı kontrolü, çürütme.

Değerler yüzde puandır. P = 15 barda +%5 hedefinin stop'tan önce görülme payı. FARK = P olay - P eş (aynı gün, aynı kova). MARJ = FARK(aday VE kol) - FARK(kol). Etiket karne v3 ile verilir: kol A için ABD ve AVR ayrı, kol B için yalnız ABD (güç >= 0,80 şartıyla). Hücreler eğitim (2016-22) ve ambargolu sınama (2023-26). KATKI+ için ATRP (F55) tercil şartı da gerekir.

**SONUÇ: ENTEGRE ET 0 satır.**
- KATKI+ 0, KATKI− 0, SORGULA 8 (kol A), ÖLÇÜLEMEDİ 8 (kol B, AVR kol B satırları BİLGİ).
- Kol A'daki 8 satırın hiçbirinde ATRP şartı tutmadı.
- En yakın iki SORGULA satırı (NR7 A ABD, AYK A ABD) çürütme lensinde düştü.
- Sızıntı lensi geleceğe bakma bulmadı. Ön kayıtta iki eksik buldu: K8 satırı yanlış işaretli, K9 mühür boşluğu var.
- Seçim yanlılığı var: dört aday DEVİR 1-2'de aynı veride görülmüştü. Kesin karar ancak ileri testte verilir.
- Bu belge iz, emare ya da bulgu iddia etmez.

## 1. Aday tablosu

Kısaltmalar:
- YÜ = yeniden üretim lensi. 48 hücrenin 288 değerinin hepsi TUTTU (en büyük fark 7e-15). Bu tur yalnız n / P / FARK / MARJ / stop değerlerini kapsar; bootstrap, L3O, güç ve ATRP yeniden üretilmedi.
- SZ = sızıntı lensi. Genel sonucu TUTMADI ve bütün satırları etkiler. Neden ön kayıt eksiği (K8 / K9); geleceğe bakma yok.
- ÇR = çürütme lensi. Yalnız NR7 A ve AYK A satırlarına özel olarak uygulandı.

| Aday | Kol | Pazar | Eğitim n / FARK | Sınama n / FARK | Etiket | Eleştiri sonucu |
|---|---|---|---|---|---|---|
| AYK (F47 <= q25) | A | ABD | 2172 / +1,25 | 1601 / +1,78 | SORGULA | **ÇR ÇÜRÜTTÜ**: stop payı dört hücrede de eşten yüksek (%30,8 / %26,8; %32,6 / %28,8). ATRP sınama T0 -3,07, T1 -1,87. Sınama boot alt ucu -0,05 |
| AYK (F47 <= q25) | A | AVR | 1122 / +3,06 | 543 / -0,40 | SORGULA | **ÇR ÇÜRÜTTÜ** (aynı aday). Sınama boot alt ucu -2,75, L3O -0,86. ATRP sınamada üç tercilde de negatif. En iyi 10 olay çıkınca MARJ -1,03 |
| NR7 (F56 == 1) | A | ABD | 1164 / +1,50 | 698 / +4,06 | SORGULA | **ÇR ÇÜRÜTTÜ**: katkı tek pazardan geliyor. Sınamada 2023 MARJ +0,4 (n 176), 2024-26 MARJ +5,4. Eğitim boot alt ucu -0,11. Katkı ATRP T1-T2'de, T0'da MARJ +0,01. Az olaya bağlılık lensi TUTTU (en iyi 5 sembol çıkınca +1,88 / +3,08) |
| NR7 (F56 == 1) | A | AVR | 612 / +0,80 | 287 / -5,91 | SORGULA | Pazarlar arasında işaret değişiyor (MARJ +0,30 / -4,79, DEVİR 2 ile aynı). Sınama güç 0,54, bu hücre ÖLÇÜLEMEDİ düzeyinde. Stop sınamada %24,0 / %19,4 |
| W2D (F32 >= q75) | A | ABD | 1752 / -0,26 | 1098 / +2,43 | SORGULA | ÇR uygulanmadı. Eğitimde FARK < 0. Boot alt ucu iki hücrede < 0. ATRP TUTMADI (sınama T0 -4,37) |
| W2D (F32 >= q75) | A | AVR | 973 / +0,50 | 500 / +0,65 | SORGULA | Eğitimde MARJ -0,00. Stop sınamada %22,6 / %20,5. ATRP TUTMADI |
| W1 (F30 < 1 VE <= q25) | A | ABD | 1977 / -1,15 | 1175 / +1,44 | SORGULA | Eğitimde FARK < 0. ABD'nin 6 ATRP hücresinin hepsi > 0, ama boot alt ucu < 0 |
| W1 (F30 < 1 VE <= q25) | A | AVR | 1060 / +1,75 | 433 / -0,14 | SORGULA | ATRP TUTMADI (T1 eğitim -1,58, sınama -3,57). Sınama güç 0,75 |
| AYK | B | ABD | 157 / -3,09 | 188 / +9,36 | **ÖLÇÜLEMEDİ** | Güç 0,42 / 0,59. MARJ -5,93 / +1,10, dönemler arasında işaret değişiyor |
| NR7 | B | ABD | 48 / +7,43 | 60 / +13,35 | **ÖLÇÜLEMEDİ** | Güç 0,12 / 0,15 |
| W2D | B | ABD | 51 / +4,73 | 66 / +3,34 | **ÖLÇÜLEMEDİ** | Güç 0,12 / 0,17. MARJ +1,89 / -4,93 |
| W1 | B | ABD | 53 / +9,71 | 52 / +12,59 | **ÖLÇÜLEMEDİ** | Güç 0,13 / 0,14. YÜ bu hücreyi birebir üretti (53 / +9,712) |
| AYK | B | AVR | 41 / +15,06 | 34 / +7,87 | BİLGİ (ÖLÇÜLEMEDİ) | Güç 0,14 / 0,13 |
| NR7 | B | AVR | 13 / -5,09 | 6 / +6,53 | BİLGİ (ÖLÇÜLEMEDİ) | n < 30, olaylar raporda listeli |
| W2D | B | AVR | 15 / +5,15 | 22 / +12,30 | BİLGİ (ÖLÇÜLEMEDİ) | n < 30, olaylar raporda listeli |
| W1 | B | AVR | 15 / +4,28 | 5 / -15,89 | BİLGİ (ÖLÇÜLEMEDİ) | n < 30, olaylar raporda listeli |

Kol B hakkında: ABD kol B hücrelerinde güç 0,12-0,59 aralığında. Sekiz kol B satırının hepsi **ÖLÇÜLEMEDİ** okunur. Kol B'deki büyük pozitif FARK değerleri (+7..+15) bulgu değildir ve "iz değil" sözü de kurulmaz.

## 2. ENTEGRE ET

Liste boş. KATKI+ satırı olmadığı için "KATKI+ VE üç lens tuttu" şartını sağlayan satır da yoktur.

## 3. YENİDEN YAP (düşen satırlar, nedenleri ve değişmesi gerekenler)

1. **NR7 kol A (F56 == 1).**
   - Neden düştü: çürütme lensi çürüttü. Katkı yalnız ABD'den geliyor; AVR sınamada MARJ -4,79 ve boot üst ucu -0,88. ABD sınamasındaki katkı 2024-26'dan geliyor (2023'te MARJ +0,4). Eğitim boot aralığı sıfırı içeriyor. Katkı yüksek oynaklıklı olaylarda (ATRP T1-T2) toplanıyor.
   - Ne değişmeli: sınama hücresi 2023 ve 2024-26 olarak AYRI raporlanmalı (proje standardı). Eşik (F56 == 1) sabit kalır. Karar ancak Mart 2027 ileri testinde, aynı eşik ve aynı karneyle verilir. En fazla "ABD'ye özgü, 2024-26 ağırlıklı SORGULA" okunur.
2. **AYK kol A (F47 <= q25).**
   - Neden düştü: çürütme lensi çürüttü. Stop payı dört karar hücresinin dördünde de eşten yüksek; DEVİR 2'de beklenen oynaklık bileşimi ret nedeni bu turda da tuttu. ATRP şartı ABD ve AVR sınamada tutmadı. AVR sınamada FARK -0,40.
   - Ne değişmeli: ATRP içinde MARJ > 0 olmadan yeniden sınanmaz. Aday yalnız ileri test defterinde kalır; eşik (q25, devir2_esik.json) oynanmaz. q25 eşiği 2016-22 eğitiminden ayarlandığı ve DEVİR 1-2'de aynı veride görüldüğü için aşırı uyum riski açıktır.
3. **W2D ve W1 kol A.**
   - Neden düştü: çürütme lensi bu satırlara özel uygulanmadı. Karne ve sızıntı lensi yüzünden SORGULA kaldılar. İki satırda da eğitim ABD FARK < 0 ve ATRP şartı AVR'de tutmadı. W1'de bu satır DEVİR 1 sonucu görüldükten sonra seçilmişti, yani seçim yanlılığı var (K8 / K9).
   - Ne değişmeli: aynı veride yeniden koşu yok. Yalnız ileri testte aynı eşikle (devir3_esik.json) bakılır.
4. **Bütün satırlar (sızıntı lensi).**
   - K8 kontrol satırı EVET yazılmış ama BH uygulanmamış (DEVIR_3_ON_KAYIT.md:194). Satır "SAPMA (önceden yazılı)" olmalıydı.
   - K9 mühür boşluğu: GE_FN_SHA (GOZ_ETIKET ge_s6 / ge_bolge / ge_ozellik_bar) ve V_*.pkl veri sha'sı mühürlenmemiş. Önceki turlarda bunlar mühürlüydü. GOZ_ETIKET.py koşu sırasında başka bir süreçle değişti, ama ilgili fonksiyonlar değişmedi ve prefix denetimi tuttu; sonuca etkisi yok.
   - Ne değişmeli: sonraki ön kayıt bu iki sha'yı da mühürler ve kapı bunları denetler.

## 4. KAPANDI (KATKI−: iki dönemde de eksi)

Liste boş. Bu turda KATKI− satırı yok.
- En yakın satır NR7 A AVR'dir. Sınamada MARJ -4,79 ve boot üst ucu -0,88, ama eğitimde MARJ +0,30 ve sınama gücü 0,54. Bu yüzden bu satır kapanmaz; AVR sınama hücresi ÖLÇÜLEMEDİ düzeyindedir.

## 5. SONRAKİ DEVİR önerileri (en çok 5)

1. **İleri test, Mart 2027.** AYK / NR7 / W2D / W1 için kol A ve kol B, aynı eşikler (devir3_esik.json) ve aynı karne v3 kullanılır. Veri kriz sonrası yeni veridir. Kaynak: rapor 138-140. satırlar, çürütme lensi. Bu, bakılmış veriden bağımsız tek sınamadır.
2. **Karne v4: sınamada 2023 ve 2024-26 ayrı hücre.** Kaynak: çürütme lensi hatası. Birleştirilmiş sınama, NR7 A ABD'de 2023'ün zayıflığını (MARJ +0,4) gizliyor. CLAUDE.md standardı iki dönemi ayrı ister. Değişiklik bir sonraki koşudan önce ön kayda yazılır.
3. **Ön kayıt kapısına mühür ekleme.** GE_FN_SHA ve V_*.pkl sha'sı mühürlenir. K8 satırı BH yoksa EVET kabul etmez; "SAPMA (önceden yazılı)" ister. Kaynak: sızıntı lensi (K8 / K9).
4. **ATRP şartında en küçük pay tanımı.** Sıfıra yakın değerler (NR7 A ABD eğitim T0 +0,01) şartı geçmiş gibi görünüyor. Önceden sabit bir eşik (örneğin MARJ > +0,5 ya da boot alt ucu > 0) yazılmalı. Kaynak: çürütme lensi "ÖLÇÜT (sınırda)" notu.
5. **Kol B güç sorunu.** ABD kol B hücrelerinde güç 0,12-0,59. Aynı tanımla daha fazla olay ancak yeni veriyle gelir. Kol B ileri testte yalnız ABD'de ve güç >= 0,80 olunca karar satırı olur; o zamana kadar BİLGİ olarak kalır. Kaynak: rapor 1. tablo, karne v3.

## 6. Denetim özeti

- **Ön kayıt sırası TUTTU.** Ön kayıt commit'i 650ded5 13:36:46 UTC, koşu 13:37:06 UTC, koşu commit'i b86e035 13:37:51 UTC. Koşu commit'i yalnız rapor ve json ekliyor. YAPI_HEDEF.py, devir3_esik.json ve devir3_prefix.json sha'ları ön kayıtla aynı. Eşikler devir1 / devir2 ile birebir aynı. Not: ön kayıt ile koşu arasında 20 saniye var ve ikisini aynı ajan yazdı.
- **Yeniden üretim TUTTU.** Bağımsız pandas kodu mühürlü satır dosyalarından (olay_Y1, ozellik_Y1_d1 / d2, goz_etiket ozellik_Y1, devir3_esik ambargosu) 16 karar satırını 2 ondalıkta birebir üretti. 48 hücrede 288 değerde en büyük fark 7e-15. Kol B tanımı olay_Y9 ile aynı (1504 = 1504).
  - Kapsam dışı: bootstrap, L3O, güç, tabaka ve ATRP.
  - Not: iş tanımındaki olay_devir3*.csv.gz dosya adı depoda yok; karne olay_Y1'den hesaplanıyor (adlandırma uyuşmazlığı, K11).
- **Sızıntı: geleceğe bakma yok.**
  - yh_d1_bar [0, i-1], yh_d2_bar [0, i] okuyor. Giriş t+1 açılışta.
  - Bağımsız prefix denetimi 36 / 36 tuttu.
  - Ambargo 60 bar ve üç pazarda da uygulanıyor; ufuk 15 bar olduğu için etiket örtüşmesi yok.
  - Kriz kesiği tutuyor.
  - İki commit'te e-posta / anahtar yok.
  - Eksikler: K8 satırı yanlış EVET, K9 mühür boşluğu (bkz. 3.4).
- **Çalışma ağacı.** GOZ_ETIKET.py, test_goz_etiket.py ve tur/TUR_DEFTERI.md commit'siz değişiklik taşıyor; tur/6 ve tur/7 izlenmiyor. Bunlar başka bir oturumun işi. DEVİR 3 commit'lerine ve bu birleştirmeye girmedi. Ana modelin denetlemesi gerekir.

### IK_HATA adayları (ana model işler)

1. K8 kontrol satırı EVET yazılmış, BH yok. Tür: süreç / ifade.
2. K9: GE_FN_SHA ve V_*.pkl sha'sı mühürsüz. Tür: süreç.
3. Sınamada 2023 ile 2024-26 tek hücrede birleşmiş, proje standardından sapma. Tür: ölçüt. Ön kayıtta yazılı.
4. İş tanımı ile depo arasında satır dosyası adı uyuşmazlığı (olay_devir3*). Tür: süreç (K11).
5. ATRP şartında sıfıra yakın pay için tanım yok. Tür: ölçüt.
