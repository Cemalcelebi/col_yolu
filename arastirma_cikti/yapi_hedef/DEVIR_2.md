# YAPI_HEDEF — DEVİR 2 BİRLEŞTİRME (2026-11-19)

Girdiler:
- DEVIR_2_RAPOR.md (koşu 1ba870f, 13:00:22 UTC).
- DEVIR_2_ON_KAYIT.md (157d22d, 12:59:43 UTC).
- devir2_sonuc.json.
- Üç eleştiri lensi: yeniden üretim, sızıntı kontrolü, çürütme.

Değerler yüzde puandır. P = 15 barda +%5 hedefinin stop'tan önce görülme payı. FARK = P olay - P eş. MARJ = FARK(aday) - FARK(kol tabanı). Kol A bütün Y1 olaylarıdır. Kol B, Y9 alt kümesidir. Etiket karne v2 ile verilir: ABD ve AVR ayrı ayrı, eğitim (2016-22) ve ambargolu sınama (2023-26) dört hücre. Aşağıdaki tabloda gösterilen FARK değerleri ABD+AVR havuzudur ve yalnız bilgi içindir.

**SONUÇ: ENTEGRE ET 0 satır.**
- KATKI+ satırı yok.
- KATKI− 1 satır (W2 kol A); bu satır da kırılgan, ayrıntısı 4. bölümde.
- SORGULA 19 satır.
- En yakın iki SORGULA satırı (AYK A ve RV A) çürütme lensinde düştü.
- Sızıntı lensi karne ve ön kayıtta dört eksik buldu: K2 kesit evreni, K1 hacim tabakası, K8 / K9 seçim yanlılığı ve n < 30 olay listesi.
- Bu belge iz, emare ya da bulgu iddia etmez.

## 1. Aday tablosu (ABD+AVR havuzu; etiket ABD / AVR ayrı kuralından)

Kısaltmalar:
- YÜ = yeniden üretim lensi. Sekiz hücrenin hepsi TUTTU (fark 0).
- SZ = sızıntı lensi. Genel sonucu TUTMADI ve bütün satırları etkiler: K2 kesit, K1 hacim, K8 / K9.
- ÇR = çürütme lensi. Yalnız AYK A ve RV A satırlarına özel olarak uygulandı.

| Aday | Kol | Eğitim n / FARK | Sınama n / FARK | Etiket | Eleştiri sonucu |
|---|---|---|---|---|---|
| PP (F43; kapalı konu) | A | 6363 / +0,44 | 3790 / -0,46 | SORGULA | YÜ tuttu (eğitim hücresi birebir aynı); SZ: F13 hacmiyle ilişkili, K1 tabakasında hacim yok; mekanik (Y1 olaylarının ~%48'inde PP = 1) |
| AY (F46 <= 0,10) | A | 2634 / -1,23 | 1644 / +0,04 | SORGULA | YÜ tuttu (ABD sınama ve havuz sınama birebir aynı); sınamada FARK sıfırda |
| AYK (F47 <= q25) | A | 3294 / +1,86 | 2144 / +1,23 | SORGULA | **ÇR ÇÜRÜTTÜ**: oynaklık bileşimi (bkz. 3. bölüm) |
| DT (F50) | A | 2797 / -1,99 | 1580 / -1,72 | SORGULA | YÜ tuttu (ABD / AVR eğitim birebir aynı); AVR'de MARJ +0,1 / +0,6 olduğu için KATKI− olmadı |
| RV (F52/F53/F55; kapalı konu) | A | 1170 / +3,44 | 540 / +3,03 | SORGULA | **ÇR ÇÜRÜTTÜ**: F13'ün yeniden adlandırılmışı (Spearman 0,93), pazar ve dönem arasında işaret değişiyor; SZ: kesit evreni bugünün listesi |
| NR7 (F56) | A | 1776 / +1,26 | 985 / +1,15 | SORGULA | ABD sınama MARJ +4,2, AVR sınama -4,8 (n 287): pazarlar arasında işaret değişiyor |
| VCP (F60) | A | 36 / +5,28 | 21 / +0,81 | SORGULA | **ÖLÇÜLEMEDİ** (n < 30) |
| W1 (F30; DEVİR 1 YENİDEN) | A | 3037 / -0,14 | 1608 / +1,02 | SORGULA | SZ: DEVİR 1 sonucu görüldükten sonra seçildi, aynı veride yeniden koşuldu (K8 / K9) |
| W2 (F31; DEVİR 1 YENİDEN) | A | 2723 / -2,15 | 1624 / -1,88 | KATKI− | YÜ tuttu (dört hücrenin MARJ'ı < 0); kırılgan: AVR sınamada MARJ -0,013 ve boot alt -0,039 |
| W2D (F32; DEVİR 1 YENİDEN) | A | 2725 / +0,01 | 1598 / +1,87 | SORGULA | SZ: seçim yanlılığı (K8 / K9); eğitimde FARK sıfırda |
| PP | B | 192 / +7,23 | 191 / +9,82 | SORGULA | AVR hücreleri n 42 / 38; MARJ bootstrap alt ucu dört hücrede de < 0 |
| AY | B | 84 / -6,08 | 127 / +10,82 | SORGULA | AVR n 10 / 16 → **ÖLÇÜLEMEDİ**; dönemler arasında işaret değişiyor |
| AYK | B | 198 / +0,67 | 222 / +9,14 | SORGULA | ABD eğitim MARJ -5,9; dönemler arasında işaret değişiyor |
| DT | B | 30 / +6,41 | 26 / -11,01 | SORGULA | **ÖLÇÜLEMEDİ** (hücre n 24 / 6 / 21 / 5) |
| RV | B | 30 / +16,45 | 16 / +27,85 | SORGULA | **ÖLÇÜLEMEDİ** (hücre n 18 / 12 / 11 / 5); F13'ün yeniden adlandırılmışı, kapalı konu |
| NR7 | B | 61 / +4,76 | 66 / +12,73 | SORGULA | AVR n 13 / 6 → **ÖLÇÜLEMEDİ** |
| VCP | B | 0 / - | 1 / -7,25 | SORGULA | **ÖLÇÜLEMEDİ** (n 0 / 1) |
| W1 | B | 68 / +8,51 | 57 / +10,09 | SORGULA | AVR n 15 / 5 → **ÖLÇÜLEMEDİ**; seçim yanlılığı: DEVİR 1 kol B sonucu görülmüştü, olumlu çıkması döngüsel |
| W2 | B | 41 / +8,27 | 29 / +15,37 | SORGULA | **ÖLÇÜLEMEDİ** (AVR n 4 / 9); YÜ tuttu (AVR eğitim n 4, sayısal eşitlik); DEVİR 1'de ÇR ÇÜRÜTMÜŞTÜ |
| W2D | B | 66 / +4,83 | 88 / +5,58 | SORGULA | AVR n 15 / 22 → **ÖLÇÜLEMEDİ**; ABD sınama MARJ -4,9 |

Kol B hakkında: AVR kol B tabanı yapısal olarak küçüktür (eğitim 89, ambargolu sınama 72 olay). Bu yüzden kol B'deki 10 satırın hiçbiri "ABD ve AVR ayrı ayrı n >= 30" şartını sağlayamaz. Kol B satırları **ÖLÇÜLEMEDİ** okunur. Bu satırlar için "iz değil" sözü kurulmaz.

## 2. ENTEGRE ET

Liste boş. KATKI+ satırı olmadığı için "KATKI+ VE üç lens tuttu" şartını sağlayan satır da yoktur.

## 3. YENİDEN YAP (eleştiride düşen satırlar, nedenleri ve değişmesi gerekenler)

1. **AYK kol A (F47 <= q25).**
   - Neden düştü: çürütme lensi (b) satırı çürüttü. Toplam MARJ'ın pozitif çıkması oynaklık bileşiminden geliyor (Simpson). Stop payı dört hücrede de eşten +2,3..+4,0 puan yüksek. ATRP (F55) tercillerinin içinde sınama MARJ'ı ABD T0 -3,1 ve T1 -1,9; AVR'de üç tercilde de negatif.
   - Ek not: AVR sınamada FARK -0,4. Bu hücrenin MARJ'ı +0,73; en iyi 3 olay çıkarılınca +0,19'a iniyor.
   - Ne değişmeli: K1 tabakasına F55 ATRP girmeli. KATKI+ şartına "oynaklık tabakası içinde MARJ > 0" eklenmeli. Eşik aynı kalır (q25, 2016-22, getirisiz). Bu değişiklik ön kayda koşudan önce yazılır.
2. **RV kol A ve kol B (F52 / F53 / F55).**
   - Neden düştü: çürütme lensi (e) ve (a) satırı çürüttü. F52, kırılım hacmi F13 ile Spearman 0,93 ilişkili; yani F13'ün yeniden adlandırılmışıdır. ABD sınama MARJ'ı -0,45, yıl kırılımında 2025 -7,6 ve 2026 -8,7.
   - Sızıntı lensi: F53 / F54 kesit sırası bugünün hayatta kalan evreninden hesaplanıyor. Bu bir K2 / K7 yanlılığıdır.
   - Ek: RV kapalı konuya dokunuyor (giriş zamanlaması / onay / hacim).
   - Ne değişmeli: RV ayrı aday olarak yeniden koşulmaz. Hacim ancak F13 tabakası içinde, bilgi satırı olarak ölçülebilir. Kapalı konu olduğu için Cemal onayı olmadan yeniden açılmaz.
3. **PP kol A (F43; kapalı konu).**
   - Neden: lensler satırı ayrıca çürütmedi. Sızıntı lensi K1 eksiğini gösterdi: F13 hacim tabakası yok. Ayrıca PP mekanik: Y1 olaylarının ~%48'inde (ABD) PP = 1. Satırın etiketi zaten SORGULA ve tabakada işaret değişiyor.
   - Ne değişmeli: PP yalnız F13 tabakasıyla bilgi olarak ölçülür. Kapalı konu olduğu için yeni aday açılmaz.
4. **Karne ve ön kayıt kuralı (bütün 20 satırı etkiler).** Sızıntı lensi TUTMADI; dört eksik:
   - K2: kesit evreni karar günündeki hali değil. Ön kayıtta EVET yazılmış, KISMİ / HAYIR yazılmalıydı.
   - K1: Spearman tablosu ön kayıtta görülmesine rağmen (F52 / F44 / F64 ile F13 arasında +0,82..+0,95) hacim tabakası yok.
   - K8 / K9: W1 / W2 / W2D adayları DEVİR 1 sonucu görüldükten sonra seçildi ve aynı veride yeniden koşuldu. Bu ön kayıtta yazılı değil.
   - K8: n < 30 olan hücrelerin olayları (VCP, kol B'deki DT / RV / NR7, AVR kol B) tek tek listelenmedi.
   - Ne değişmeli: ATRP (F55) ve F13 K1 tabakasına girer. KATKI− için de bootstrap üst ucu < 0 şartı konur (simetrik kural). Prefix denetimine F53 / F54 ve "t - sol = F8" eşitliği eklenir. n < 30 olan hücrelerin olay listesi rapora basılır. Bu değişikliklerin hepsi koşudan önce ön kayda yazılır.

## 4. KAPANDI (KATKI−: iki dönemde de eksi)

- **W2 kol A (F31, gün içi birikim üst çeyrek).**
  - ABD+AVR havuzunda FARK eğitimde -2,15, sınamada -1,88.
  - Dört hücrenin MARJ'ı: ABD eğitim -1,61 (n 1750), AVR eğitim -1,40 (n 973), ABD sınama -2,05 (n 1108), AVR sınama -0,013 (n 516).
  - Bu süzgeç DEVİR 1'de de KATKI− çıkmıştı. Ancak iki ölçüm aynı veride yapıldı, yani bağımsız değil.
  - Kırılganlık: AVR sınama hücresinde MARJ sıfırdan ayırt edilemez (boot alt -0,039). Ayrıca n 516 < 1.000. Bu hücre için "iz değil" yazılmaz; hücre **ÖLÇÜLEMEDİ** düzeyindedir.
  - Karar: süzgeç adayı olarak bu devirde kapandı (süzgeç kullanılmaz). Sınıflama kesin değildir ve ileri teste bağlıdır.

## 5. SONRAKİ DEVİR önerileri (en çok 5)

1. **Karne v3: oynaklık ve hacim tabakası.**
   - Yapılacak: K1 tabakasına F55 ATRP ve F13 eklenir. KATKI+ için "her oynaklık tercilinde MARJ > 0" şartı konur. KATKI− için bootstrap üst ucu < 0 şartı konur.
   - Kaynak: çürütme lensi (AYK Simpson) ve sızıntı lensi (K1 hacim, KATKI− simetrisi).
2. **AYK'nın oynaklıktan arındırılmış yeniden sınaması.**
   - Yapılacak: aynı F47 q25 eşiği, ATRP tercilleri içinde ve sabit eşikle yeniden sınanır. AYK'nın dört hücrenin hepsinde MARJ > 0 veren tek kol A satırı olduğu korunur.
   - Kaynak: rapor 1. tablo ve çürütme lensi.
3. **Kesit ölçüleri için karar günündeki evren.**
   - Yapılacak: F53 / F54 karar günündeki evrenle (batanlar dahil) yeniden kurulur; kurulamazsa kesit adayları karneden çıkarılır. Prefix denetimine kesit ölçüleri ve "t - sol = F8" eşitliği eklenir.
   - Kaynak: sızıntı lensi (K2 / K7).
4. **W1 / W2 / W2D ve NR7 için ileri test.**
   - Yapılacak: bu adaylar aynı 2016-26 verisinde artık bağımsız sınanamaz. IK_ILERI için öneri: kriz sonrası yeni veride aynı eşikle sınama (en erken Mart 2027). NR7 A'nın pazarlar arasında işaret değiştirmesi (ABD sınama +4,2 / AVR sınama -4,8) de bu teste eklenir.
   - Kaynak: sızıntı lensi (K8 / K9 seçim yanlılığı).
5. **Kol B için güç planı.**
   - Yapılacak: AVR kol B tabanı küçük (89 / 72 olay). Kol B kararı ya yalnız ABD ile ve güç simülasyonuyla ön kayda yazılır ya da kol B bilgi satırı olur. n < 30 olan hücrelerin olayları tek tek listelenir.
   - Kaynak: rapor HATA (GÜÇ) ve sızıntı lensi (K8).

## 6. Denetim özeti

- **Ön kayıt sırası: TUTTU.**
  - Ön kayıt commit'i 157d22d (12:59:43 UTC), koşu 13:00:22, koşu commit'i 1ba870f (13:01:06).
  - YAPI_HEDEF.py sha'sı ve devir2_esik.json sha'sı ön kayıttaki değerle aynı. Eşik koşuda getirisiz yeniden hesaplandı ve eşit çıktı.
- **Yeniden üretim: TUTTU.**
  - Bağımsız pandas koduyla sekiz hücre devir2_sonuc.json ile birebir aynı çıktı (fark 0).
  - Tek KATKI− satırının (W2 A) dört MARJ değeri de yeniden üretildi.
  - Bootstrap, L3O ve K1 tabaka değerleri yeniden üretilmedi; bunlar raporun kendi sayıları olarak kalır.
  - Kaynak satır dosyaları mühürlü olay_Y1 / olay_Y9 / ozellik_Y1_d2 dosyalarıdır. Sha değerleri ön kayıtla aynı.
- **Sızıntı: TUTMADI (karne ve ön kayıt düzeyinde).**
  - Nedensel olan kısımlar: bar penceresi, pivot onayı, ZigZag, 60 bar ambargo. Pazar başına 25 olayda yapılan prefix denetimi tuttu.
  - Eksikler: F53 / F54 kesit evreni bugünün listesi (K2 yanıtı yanlış). K1 hacim tabakası yok. W adaylarında seçim yanlılığı ön kayda yazılmamış. n < 30 olayları listelenmemiş. Prefix denetiminin kapsamı dar (kesit ve F8 içinde değil).
  - KATKI+ çıkmadığı için bu eksiklerin karara etkisi yok. Yine de bir sonraki ön kayıtta düzeltilmeleri gerekir.
- **Çürütme: TUTMADI (satır düzeyinde).** En yakın iki SORGULA satırı (AYK A, RV A) çürütüldü. Hiçbir satır EMARE düzeyine çıkmıyor.
- **E-posta / anahtar: TUTTU.** İki commit'in diff'inde desen bulunmadı.

## HATA (ana modelin IK_HATA'ya işlemesi için öneri; bu belge defter dosyalarına dokunmaz)

- K2 yanıtı yanlış (DEVIR_2_ON_KAYIT.md:253; YAPI_HEDEF.py:7585): F53 / F54 kesit sırası bugünün hayatta kalan evreninden hesaplanıyor. Doğru yanıt EVET değil, KISMİ / HAYIR olmalıydı. Tür: geleceğe bakma / evren.
- K1 eksik (YAPI_HEDEF.py:7563): ön kayıtta F13 ile Spearman ilişkisi +0,82..+0,95 göründüğü halde hacim tabakası yok. ATRP tabakası da yok; AYK'nın pozitif MARJ'ı bu yüzden oynaklık bileşiminden geliyor. Tür: kontrol grubu.
- K8 / K9 eksik: W1 / W2 / W2D adayları DEVİR 1 sonucu görüldükten sonra seçildi ve aynı veride yeniden koşuldu; bu ön kayda yazılmadı. Tür: ön kayıt / seçim yanlılığı.
- K8 eksik: n < 30 olan hücrelerin olayları raporda tek tek listelenmedi, buna karşın K8'de EVET yazıyor. Tür: örneklem.
- Prefix denetiminin kapsamı dar (YAPI_HEDEF.py:7475, 7876-7884): F53 / F54 ve F8 içinde değil. Tür: geleceğe bakma denetiminde eksik (sızıntı bulunmadı).
- RV adayı ayıklanmadan koşuldu: ön kayıtta F13 ile ilişkisi +0,95 yazılıydı, yine de yeniden adlandırılmış bir ölçü olarak aday listesine girdi; kapalı konuya da dokunuyor. Tür: kontrol grubu / süreç.
- KATKI− kuralında güven aralığı şartı yok (YAPI_HEDEF.py:8217): W2 A'nın KATKI− etiketi, AVR sınamada MARJ -0,013 olan bir hücreye dayanıyor. Tür: ifade.
- Süreç: iş tanımı olay_devir2*.csv.gz dosyasını gösteriyordu; böyle bir dosya yok. Yeniden üretim ön kayıtta mühürlü satır dosyalarıyla yapıldı. Tür: süreç.
