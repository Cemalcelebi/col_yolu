# TANIM ADIMI 2 — İKİNCİ KÖR SET — ÖN KAYIT (Cemal işaretlemeden ÖNCE mühürlenir)

Üretim: 2026-11-23T16:34:29Z (UTC). Soru: Cemal'in 'dip savunması VAR' gözü, ilk 40 sayfadan seçilen ölçülebilir kuralla (ADAY_1 / ADAY_2) BAĞIMSIZ ikinci sette örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/tanim2_anahtar.json` sha256: `c0cc3e82c2895c222393932f7ab217f626444e516cb159ba6696ac888e00e916`
- PDF: `arastirma_cikti/goz_uyum/TANIM2_KOR.pdf` sha256: `353eeb487c9f6a46ef3143d2215ccc5f98874a0cfd2360932b29176fcdaafe46`
- keşif: `arastirma_cikti/goz_uyum/tanim2_kesif.json` sha256: `2fd1b0d688dbb5d53acf2d1227980a942973754b6ce0a45244dad4e553447235`
- keşif raporu: `arastirma_cikti/goz_uyum/TANIM2_KESIF.md` sha256: `c2034daa00396d1a3c693aad7823bf3cdc8ff3c99c03949e7154a0cb6a8244e5`
- kod: `arastirma_cikti/goz_uyum/tanim2.py` sha256: `61821c517e75728c5c599e0f6978674455329707e7cc785b6cfe44dea54f1314`
- eşik sözlüğü (TZ_ESIK) sha256: `54f1a048fa0346b2a7faeab9cf19defca2ec3f2138ecc6ba6579567ef94d0bd0`
- iş tanımı: `arastirma_cikti/goz_uyum/TANIM2_IS_TANIMI.md` sha256: `244cc9683d6e0d25e05767af51dde291f6815afbcf14667ccbb17dbd7b0d2113`
- bağımlı kod: goz_uyum.py `828258b1f24d45bc`, GOZ_ETIKET.py `76d5c76b3a545ed5`, YAPI_HEDEF.py `812d188c20a64e27`

## 2. Seçim kuralı (iş tanımından aynen; keşiften önce yazıldı)
ADAY_1 = LOOCV kappa'sı en yüksek TEK özellikli kural; ADAY_2 = LOOCV kappa'sı en yüksek iki özellikli kural (ADAY_1'den LOOCV kappa'da en az 0,10 yüksek değilse ADAY_2 = yok, basit olan kalır); her ikisinin eşiği 40 sayfanın TAMAMIYLA yeniden seçilir ve SAYI olarak mühürlenir. Ayrıca KONTROL = eski Ş3 (değişmez).

## 3. Mühürlü kurallar (SAYI; 40 sayfanın tamamıyla seçildi; NaN = YOK)
- **ADAY_1**: VAR ⇔ dip_bolge_n >= 18.5. Tanım: dip_bolge_n: son 40 barda dip bölgesi (alt %20) bar sayısı. 40 sayfada kappa 0.634, LOOCV kappa 0.634 (keşif).
- **ADAY_2**: VAR ⇔ (dip_bolge_n >= 18.5) VEYA (F2 >= 0.007798464610330846) (NaN = YOK); 40 sayfada kappa 0.773, LOOCV 0.773.
- **KONTROL**: eski Ş3, VAR ⇔ F2 >= -0,01 (değişmez); ilk sette kappa 0.400.

## 4. Örneklem (tohum 20261124)
Havuz: goz_uyum.gu_havuz (Y1 ∧ Ş1, P2 benzeri likidite, aynı hissede 60 bar tekil; pencereler ve likidite GU_ESIK ile aynı); ilk setin 40 (pazar, sembol) çifti hariç. Dönem: ABD / AVR 2001-01-01..2023-06-30; BIST 2016-01-01..2017-12-31 ve 2021-03-01..2023-06-30.
40 sayfa: ABD 30, AVR 5, BIST 5; tabaka ADAY_1 x KONTROL (Ş3), hücre başına 10; aynı hisseden en çok 1; sinyal günleri arası >= 30 gün; sayfa sırası rastgele.
Havuz hücreleri: {"ABD": {"n_havuz": 2451, "n_ilk_set_haric": 2390, "hucre": {"A1=True_S3=True": 631, "A1=True_S3=False": 67, "A1=False_S3=True": 1522, "A1=False_S3=False": 170}}, "AVR": {"n_havuz": 221, "n_ilk_set_haric": 209, "hucre": {"A1=True_S3=True": 54, "A1=True_S3=False": 1, "A1=False_S3=True": 142, "A1=False_S3=False": 12}}, "BIST": {"n_havuz": 177, "n_ilk_set_haric": 171, "hucre": {"A1=True_S3=True": 29, "A1=True_S3=False": 5, "A1=False_S3=True": 127, "A1=False_S3=False": 10}}}
Tabaka dağılımı (hücre, pazar -> sayfa): {"A1=False S3=False ABD": 8, "A1=False S3=False AVR": 1, "A1=False S3=False BIST": 1, "A1=False S3=True ABD": 7, "A1=False S3=True AVR": 1, "A1=False S3=True BIST": 2, "A1=True S3=False ABD": 9, "A1=True S3=False BIST": 1, "A1=True S3=True ABD": 8, "A1=True S3=True AVR": 1, "A1=True S3=True BIST": 1}
Yanıt sayıları: ADAY_1 VAR 20, KONTROL VAR 20, ADAY_2 VAR 21.
Notlar: ["hücre A1=True S3=False AVR: kota 2, bulunan 0", "hücre A1=True S3=False: 2 eksik ABD'den tamamlandı (2)", "pazar ABD: 32 sayfa (hedef 30)", "pazar AVR: 3 sayfa (hedef 5)"]

## 5. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in ikinci setteki VAR / YOK işaretleri ile ADAY_1, (varsa) ADAY_2 ve KONTROL arasında uyum ve Cohen kappa; '?' karar dışı, sayısı ayrıca yazılır; kappa bootstrap %95 aralığı (B 5000, tohum 20261124, sayfa yeniden örneklemesi).
- HÜKÜM: ikinci sette ADAY_1 (ve varsa ADAY_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ (getiri ölçümüne geçilir, kasa açılır); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN (üçüncü tur: ilk iki setin 80 sayfası birleşik keşif, üçüncü bağımsız set); < 0,40 GEÇERSİZ (Cemal'le görüşme: neye baktığını çizimle anlatması); karar sayısı < 30 ise ÖLÇÜLEMEDİ. KONTROL (eski Ş3) kappa'sı karşılaştırma için yazılır.
- Eşik ve kural sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 6. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralların uyumu, kappa) |
| K2 | geleceğe bakma | EVET | yeni özellikler yalnız kör sayfa penceresinden: tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, son 121 bar) + mekanik denetim (W.index.max() <= t, W.index[-1] == t); havuz goz_uyum.gu_havuz (veri sinyal çağı sonunda kesik, F1-F23 nedensel); test: tanim2.py test prefix değişmezliği (t sonrası değişince yeni özellikler aynı); getiri / sinyal sonrası fiyat hiç okunmaz |
| K3 | geçerli bar | EVET | GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar; havuz ve pencere goz_uyum ile aynı |
| K4 | tekilleştirme | EVET | havuzda aynı hissede 60 bar tekil (goz_uyum._gu_isci); ikinci sette aynı (pazar, sembol) en çok 1, ilk setin 40 (pazar, sembol) çifti hariç, sinyal günleri arası >= 30 gün (tz_sec_df); n = 40 bağımsız sayfa |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (goz_uyum ile aynı); yeni özellikler birimsiz oran / bar sayısı; AVR likidite EUR (Close x Kur) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok; raporda yazılı |
| K8 | örneklem ve dönem | EVET | keşif 40 sayfa küçük örneklem: TANIM2_KESIF 'keşif' etiketli + çoklu karşılaştırma uyarısı (40 tek özellik, 30 çift kural); seçilen kural YALNIZ ikinci bağımsız 40 sayfada sınanır; karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); pazar dağılımı ABD 30 / AVR 5 / BIST 5 |
| K9 | ön kayıt | EVET | yeni özellik tanımları + seçim kuralı keşiften önce commit (TZ_YENI, TZ_SECIM_KURALI; ilk commit); ADAY eşikleri SAYI olarak bu dosyada; anahtar + PDF + kesif + tanim2.py + TZ_ESIK sha'ları burada; bu dosya Cemal işaretlemeden ÖNCE commit; hüküm eşikleri sabit |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | tohum 20261124 ile anahtar aynı komutla yeniden üretilir; olc komutu anahtardan tabloyu yeniden kurar; keşif tabloları tanim2_kesif.json'dan |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; keşif sayıları 'bulgu' denmez; hüküm sözü yalnız ön kayıttaki eşikle |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_TZ + test; yasak dosyalar (defter, mevcut .py, goz_uyum.py / anahtar / GOZ_UYUM_*, kart / kart2 / kasa) değiştirilmedi (git status); e-posta taraması GU._yaz / _jyaz; kod değiştiyse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 7. Git kaydı (bu dosyanın yazıldığı an)
- tanim2.py: 1f478066bbfca0467e510b82f87ad34847434e35 2026-11-23T16:19:18+00:00
