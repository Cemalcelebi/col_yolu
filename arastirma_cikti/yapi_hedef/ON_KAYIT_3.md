# YAPI_HEDEF — ÖN KAYIT 3 (3. tur: Y9 / Y9b / Y9c + Y9d bilgi; konum eşli KAT)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 3. tur eklendi (YAPI_HEDEF_3_IS_TANIMI.md)

- YH_ESIK_SHA: `e209191952e67c8fdd86ce737507ee3e11a40d714449ed2d008805a65a4b193d` (3. tur denemeleri dahil)
- ESIK_TUR2_SHA: `d4ab206a2d2cf8ed25f2c3fd7f30c7122f6460a40040255788ea62ff9cdfbbe1` (YH_ESIK'ten Y9-Y9d çıkarılınca; = ON_KAYIT_2.md YH_ESIK_SHA: Y1-Y8B eşikleri AYNEN)
- ESIK_TUR1_SHA: `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b` (Y6-Y9d çıkarılınca; = ON_KAYIT.md YH_ESIK_SHA = güç tablosu)
- YH_KOD_SHA: `4185c2d983bb62f903054b28eab214800faf4beea83d02e9fbcef33f9e053e90` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- FV_KOD_SHA: `c62b736a3da17c33b380d38a59c9b69487c4d78b3a3dd37ae7e019c8ea47cd5e` (FITIL_V2.py)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json; 1. turun güç tablosu, aynı kural)
- Y2_OLAY_SHA: `ac6f4a72550e4aecea9ba6de9bc8469adaf6f004a9531cc9653d9734fdb134ea` (değişmedi; 3. turda kullanılmaz)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)
- ON_KAYIT_2: git 8b246d11e1, 2026-11-17T13:18:49+00:00
- IS_TANIMI_3: git 5642e89539, 2026-11-18T08:19:39+00:00
- ZAMAN (UTC): `2026-11-18 08:44:47 UTC`

Bu dosya 3. tur ölçümünden ÖNCE yazıldı. Y9 / Y9b / Y9c / Y9d için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni ve olay sayımı). `kos --deneme Y9,Y9b,Y9c,Y9d` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y8B eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.

## GEREKÇE ve DÜRÜSTLÜK NOTU (iş tanımı §2, AYNEN)

Cemal (18 Kas, hakem PDF'ine bakarken): 'neredeyse çoğunda şemsiye şekli oluşmuş; bunlar yukarı kırılması beklenmemeli'. Ana model ön kayıtsız bir BAKIŞ yaptı (IK_HATA'ya yazıldı): ABD + AVR 2023 / 2024-26 Y1 olaylarında (n 8.649) F15 (120 gün konumu) >= 0,75 olanlar %58, <= 0,25 olanlar %7; dipte olanların +%5 payı %51,9 vs eş %44,2 (KAT5 1,17, n 586), tepedekilerin %34,3 vs %37,6 (0,91, n 5.011). Eşikler ÖNCEDEN VAR OLAN tanımlardan (FITIL_V2 bağlam DİP <= 0,25; dönüm >= %20 düşüş) alındı, ama bakış bu hücrelerin sonucunu gördü. Bu yüzden: ABD / AVR 2023 ve 2024-26 hücreleri bu koşuda 'bakılmış' sayılır ve raporda öyle işaretlenir; DIŞ SINAMA = 2016-22 (ABD, AVR) ve BIST (üç dönem) hücreleri (ana model bunlara BAKMADI). Karar etiketi bu kez şöyle: karar hücreleri aynı (ABD / AVR 2023, 2024-26) ama etiket en fazla EMARE; dış sınama hücrelerinde (2016-22 ABD / AVR) de aynı yön + kural tutarsa 'EMARE (dış sınama tuttu)'; Mart 2027 ileri test asıl karar.

## BAKILMIŞ HÜCRE İŞARETİ

- BAKILMIŞ (ana modelin ön kayıtsız bakışı sonucu gördü): ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26. Bu hücreler karar hücreleridir ama sonuçları bağımsız kanıt değildir; etiket EN FAZLA EMARE.
- DIŞ SINAMA (ana model bakmadı): ABD 2016-22, AVR 2016-22 (karar kuralıyla aynı 4 şart; ikisi de TUTAR -> 'EMARE (dış sınama tuttu)').
- BIST (bilgi, ayrı başlık; ana model bakmadı): BIST 2016-22, BIST 2023, BIST 2024-26.
- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).

## Ölçü, kontrol grupları, karar kuralı

1. turla AYNI (ON_KAYIT.md; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi, ESIK_TUR1_SHA / ESIK_TUR2_SHA kanıtı):
- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].
- Karar: hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar).
- Hücre durumu: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.
- Kural etiketi (deneme başına): dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.

## 3. tur ek kuralları (önceden yazılı; DEĞİŞMEZ)

- Etiket: Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar.
- TERS: hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1.
- Konum eşli KAT: KONUM EŞLİ KAT (zorunlu bilgi satırı): eş = 1. turun eşi (aynı giriş günü, aynı OC kovası, havuzda, olay hissesi hariç, 15 barı ölçülebilir, AYNI d ve kural) VE eşin F15'i olayın F15 çeyreğinde; eşin F15'i = giriş gününden ÖNCEKİ son geçerli barında (olayın t'siyle aynı bilgi anı) t dahil son 120 geçerli kapanışla aynı formül; en az 3 eş; KAT ve ay kümeli %95 1. turla aynı (yh_kat). Olayın çeyreği dosyadaki F15'ten.
- Çeyrek: F15 çeyreği: Ç1 [0, 0,25], Ç2 (0,25, 0,50], Ç3 (0,50, 0,75), Ç4 [0,75, 1] (Y9 / Y9c sınırlarıyla aynı).
- Konum uyumu: olayların panelden hesaplanan F15 çeyreği dosyadaki çeyrekle >= %99 aynı olmalı (aynı formül denetimi), değilse koşu DURUR.
- Regresyon: Y9* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit olmalı (göreli 1e-4; dosya 6 anlamlı basamak), değilse koşu DURUR; ayrıca pazar başına ozellik dosyası (sembol, tarih) kümesi = şimdiki kodun Y1 olay kümesi.
- Y9d bilgi satırıdır: etiketi yazılır, karar değildir. BH (bilgi) yalnız Y9 / Y9b / Y9c x 4 karar hücresi (12 p; ayrı aile 'bh_tur3').

## Denemeler (sonuç görülmeden sabit; YAPI_HEDEF_3_IS_TANIMI.md §3)

- **Y9 DÜŞÜŞ SONRASI DİPTE**: Y1 OLAYI (OC tekilleştirmesi sonrası; ozellik_Y1.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile eşlenir) VE F15 <= 0,25 VE F17 <= -0,20. F15 = 120 gün konumu (C_t - min C) / (max C - min C), t DAHİL son 120 geçerli kapanış (GOZ_ETIKET tanımı; C_t sinyal günü kapanışı, giriş t+1 açılış: karar anında bilinir); F17 = bölge öncesi 60 gün düşüş C(sol) / max(C, [sol-60, sol-1]) - 1. Değerler dosyadan (6 anlamlı basamak) okunur; NaN şart tutmaz.
- **Y9b Y9 + HAT NET + GERÇEK KIRILIM**: Y9 olayı VE F1 >= 3 (bölgede Low <= hat x 1,015 dokunuş sayısı) VE F11 >= 0,01 (C_t / tavan - 1; Cemal E2 / E3 dip bağlamında).
- **Y9c TEPEDE (şemsiye karşıtı)**: Y1 olayı VE F15 >= 0,75. Yön + ile ölçülür (kodun yukarı kırılımı); beklenti yazılmaz; iki yönlü etiket (TERS EMARE kuralı).
- **Y9d ORTA (bilgi)**: Y1 olayı VE 0,25 < F15 < 0,75 (bilgi satırı; etiket yazılır, karar değildir).

## Yorumlar (iş tanımında açık ya da çelişik noktalar; koşudan önce sabit)

- YORUM-1 (F15 bilgi anı): iş tanımı §3 'son 120 barın aralığında kapanış konumu; t-1'e kadar' diyor, aynı cümle 'özellikler ozellik_Y1.csv.gz'den (t'ye kadar)' diyor; dosyadaki F15 (GOZ_ETIKET tanımı) C_t'yi ve t DAHİL son 120 kapanışı kullanır ve §2'deki bakış da bu dosyayla yapıldı. Dosya tanımı uygulanır. C_t sinyal günü kapanışıdır, giriş t+1 açılıştır: geleceğe bakma yok. (HATA listesinde iş tanımı tutarsızlığı olarak yazılır.)
- YORUM-2 (Y1 OLAYI): Y9* = Y1 OLAY kümesinin (OC tekil, havuzda, giriş var) alt kümesi; özellik dosyası satırları = olay_Y1.csv.gz satırları (26.663). Y1 sinyali olup Y1 olayı olmayan günler (60 gün içinde önceki Y1 olayı) Y9'a giremez; böylece Y9 sayısı Y1 tekilinden türer (iş tanımı 'Y1 olayı VE ...').
- YORUM-3 (sınırlar): F15 <= 0,25 ve F15 >= 0,75 kapalı, Y9d açık (0,25, 0,75); dosya değerleri 6 anlamlı basamak (eşik kenarında yuvarlama dosya değerine göre). NaN (F15: 120 bar yok / aralık 0; F17: bölge öncesi 60 bar yok) şart tutmaz.
- YORUM-4 (konum eşi F15): eşin F15'i giriş gününden önceki son geçerli barında hesaplanır (olayın t'si de giriş gününden önceki son geçerli bar). Olayın çeyreği dosyadan; panelden hesaplanan olay çeyreği >= %99 aynı olmalı (formül denetimi). Çeyrek sınırında kayan nokta gürültüsü (tam 0,75 konum panelde 0,7499999999) için değer çeyreğe atanmadan önce 9 ondalığa yuvarlanır (yh_ceyrek).
- YORUM-5 (dış sınama 'aynı yön + kural'): ABD 2016-22 VE AVR 2016-22 hücrelerinin ikisi de 1. turun 4 şartlı TUTAR kuralını sağlar. Tersi için ikisi de TERS. Tek hücre tutarsa 'dış sınama tutmadı' yazılır.
- YORUM-6 (TERS iki yarı): 1. turun 'yari1_kat5 / yari2_kat5' bilgisi (hücre olayları giriş sırasına göre ikiye bölünür, Σ h5 / Σ eş h5).
- YORUM-7 (Y9c TERS ve stop): TERS kuralı stop şartı içermez (iş tanımı: KAT5 üst uç < 1 ve iki yarı aynı yön); stop payları raporda bilgi olarak yazılır.

## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)

### Y9 hunisi

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y1 olayı (özellik satırı) | 14881 | 8686 / 2042 / 4153 | 7054 | 4496 / 815 / 1743 | 4728 | 2588 / 381 / 1759 |
| + F15 <= 0,25 (dipte) | 907 | 446 / 179 / 282 | 286 | 160 / 36 / 90 | 719 | 282 / 105 / 332 |
| + F17 <= -0,20 (düşüş sonrası) = Y9 | 724 | 346 / 146 / 232 | 164 | 89 / 20 / 55 | 616 | 238 / 81 / 297 |
| + F1 >= 3 (hat net) | 439 | 206 / 93 / 140 | 102 | 51 / 15 / 36 | 365 | 145 / 42 / 178 |
| + F11 >= 0,01 (gerçek kırılım) = Y9b | 222 | 97 / 52 / 73 | 40 | 18 / 7 / 15 | 224 | 87 / 34 / 103 |
| (ayrı) F15 >= 0,75 TEPEDE = Y9c | 9086 | 5658 / 950 / 2478 | 4678 | 3029 / 476 / 1173 | 1924 | 1253 / 154 / 517 |
| (ayrı) 0,25 < F15 < 0,75 ORTA = Y9d | 4888 | 2582 / 913 / 1393 | 2090 | 1307 / 303 / 480 | 2085 | 1053 / 122 / 910 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: F15_NaN 0, F17_NaN (dipte) 0, F17 > -0,20 (dipte) 183; AVR: F15_NaN 0, F17_NaN (dipte) 0, F17 > -0,20 (dipte) 122; BIST: F15_NaN 0, F17_NaN (dipte) 0, F17 > -0,20 (dipte) 103.

Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): ABD: Y1 sinyal 37969, Y1 olay 14881, özellik 14881, eşleşen 14881; AVR: Y1 sinyal 18783, Y1 olay 7054, özellik 7054, eşleşen 7054; BIST: Y1 sinyal 10242, Y1 olay 4728, özellik 4728, eşleşen 4728.

| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|
| Y9 | ABD | 492 | 346 / 146 / 232 |
| Y9 | AVR | 121 | 89 / 20 / 55 |
| Y9 | BIST | 340 | 238 / 81 / 297 |
| Y9b | ABD | 196 | 97 / 52 / 73 |
| Y9b | AVR | 33 | 18 / 7 / 15 |
| Y9b | BIST | 181 | 87 / 34 / 103 |
| Y9c | ABD | 1139 | 5658 / 950 / 2478 |
| Y9c | AVR | 515 | 3029 / 476 / 1173 |
| Y9c | BIST | 457 | 1253 / 154 / 517 |
| Y9d | ABD | 1134 | 2582 / 913 / 1393 |
| Y9d | AVR | 481 | 1307 / 303 / 480 |
| Y9d | BIST | 494 | 1053 / 122 / 910 |

## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)

- Y9: ABD 2023 en çok 146 olay (güç %11); ABD 2024-26 en çok 232 olay (güç %11); AVR 2023 en çok 20 olay (güç %0); AVR 2024-26 en çok 55 olay (güç %2). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y9b: ABD 2023 en çok 52 olay (güç %2); ABD 2024-26 en çok 73 olay (güç %2); AVR 2023 en çok 7 olay (güç %0); AVR 2024-26 en çok 15 olay (güç %0). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y9c: ABD 2023 en çok 950 olay (güç %57); ABD 2024-26 en çok 2478 olay (güç %97); AVR 2023 en çok 476 olay (güç %57); AVR 2024-26 en çok 1173 olay (güç %97).
- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay o satırdan düşer (k_n ayrı yazılır).
- Hayatta kalma: dipteki (Y9) hissenin batma olasılığı yüksektir; evrende batan yok -> Y9 hedef payı ayrıca yukarı yanlı okunur.

## YH_ESIK 3. tur girdileri (tam metin; geri kalanı ON_KAYIT.md / ON_KAYIT_2.md ile aynı)

```json
{
 "Y9": {
  "F15_ust": 0.25,
  "F17_ust": -0.2,
  "ad": "DÜŞÜŞ SONRASI DİPTE",
  "ozellik_prm": {
   "dusus_gun": 60,
   "hat_bant": 0.015,
   "konum_gun": 120,
   "tanim": "GOZ_ETIKET GE_ESIK['ozellik'] ile aynı (F1 dokunuş bandı, F15 konum penceresi, F17 düşüş penceresi); yalnız geleceğe bakma (prefix) denetiminde yeniden hesap için"
  },
  "taban": "Y1",
  "tanim": "Y1 OLAYI (OC tekilleştirmesi sonrası; ozellik_Y1.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile eşlenir) VE F15 <= 0,25 VE F17 <= -0,20. F15 = 120 gün konumu (C_t - min C) / (max C - min C), t DAHİL son 120 geçerli kapanış (GOZ_ETIKET tanımı; C_t sinyal günü kapanışı, giriş t+1 açılış: karar anında bilinir); F17 = bölge öncesi 60 gün düşüş C(sol) / max(C, [sol-60, sol-1]) - 1. Değerler dosyadan (6 anlamlı basamak) okunur; NaN şart tutmaz",
  "tur": 3,
  "tur3_kural": {
   "bakilmis": [
    [
     "ABD",
     "2023"
    ],
    [
     "ABD",
     "2024-26"
    ],
    [
     "AVR",
     "2023"
    ],
    [
     "AVR",
     "2024-26"
    ]
   ],
   "bist_bilgi": [
    [
     "BIST",
     "2016-22"
    ],
    [
     "BIST",
     "2023"
    ],
    [
     "BIST",
     "2024-26"
    ]
   ],
   "ceyrek": [
    0.25,
    0.5,
    0.75
   ],
   "ceyrek_tanim": "F15 çeyreği: Ç1 [0, 0,25], Ç2 (0,25, 0,50], Ç3 (0,50, 0,75), Ç4 [0,75, 1] (Y9 / Y9c sınırlarıyla aynı)",
   "dis_sinama": [
    [
     "ABD",
     "2016-22"
    ],
    [
     "AVR",
     "2016-22"
    ]
   ],
   "etiket": "Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar",
   "konum_es": "KONUM EŞLİ KAT (zorunlu bilgi satırı): eş = 1. turun eşi (aynı giriş günü, aynı OC kovası, havuzda, olay hissesi hariç, 15 barı ölçülebilir, AYNI d ve kural) VE eşin F15'i olayın F15 çeyreğinde; eşin F15'i = giriş gününden ÖNCEKİ son geçerli barında (olayın t'siyle aynı bilgi anı) t dahil son 120 geçerli kapanışla aynı formül; en az 3 eş; KAT ve ay kümeli %95 1. turla aynı (yh_kat). Olayın çeyreği dosyadaki F15'ten",
   "konum_uyum": "olayların panelden hesaplanan F15 çeyreği dosyadaki çeyrekle >= %99 aynı olmalı (aynı formül denetimi), değilse koşu DURUR",
   "konum_uyum_min": 0.99,
   "regresyon": "Y9* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit olmalı (göreli 1e-4; dosya 6 anlamlı basamak), değilse koşu DURUR; ayrıca pazar başına ozellik dosyası (sembol, tarih) kümesi = şimdiki kodun Y1 olay kümesi",
   "ters": "hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1"
  },
  "yon": 1
 },
 "Y9b": {
  "F11_min": 0.01,
  "F15_ust": 0.25,
  "F17_ust": -0.2,
  "F1_min": 3,
  "ad": "Y9 + HAT NET + GERÇEK KIRILIM",
  "taban": "Y9",
  "tanim": "Y9 olayı VE F1 >= 3 (bölgede Low <= hat x 1,015 dokunuş sayısı) VE F11 >= 0,01 (C_t / tavan - 1; Cemal E2 / E3 dip bağlamında)",
  "tur": 3,
  "yon": 1
 },
 "Y9c": {
  "F15_alt": 0.75,
  "ad": "TEPEDE (şemsiye karşıtı)",
  "iki_yonlu": true,
  "taban": "Y1",
  "tanim": "Y1 olayı VE F15 >= 0,75. Yön + ile ölçülür (kodun yukarı kırılımı); beklenti yazılmaz; iki yönlü etiket (TERS EMARE kuralı)",
  "tur": 3,
  "yon": 1
 },
 "Y9d": {
  "F15_ara": [
   0.25,
   0.75
  ],
  "ad": "ORTA (bilgi)",
  "bilgi": true,
  "taban": "Y1",
  "tanim": "Y1 olayı VE 0,25 < F15 < 0,75 (bilgi satırı; etiket yazılır, karar değildir)",
  "tur": 3,
  "yon": 1
 }
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); EK kontrol 'konum eşli KAT' (yh_konum_es_olc): aynı eşler VE eşin F15'i olayın çeyreğinde (dipte olmanın momentum kovasıyla karışması ayrılır); eşlerin F15 dağılımı her hücrede raporlanır; güç tablosu 1. turunki (aynı kural) |
| K2 | geleceğe bakma | EVET | F1 / F11 / F15 / F17 yalnız [.., t] (GOZ_ETIKET prefix denetimi + bu koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali ve dört özellik yeniden hesaplanır, dosyayla göreli 1e-5 aynı olmalı, yoksa DURUR: yh_gelecek_denetimi); F15 C_t'yi içerir (sinyal günü kapanışı, giriş t+1 açılış); eşin F15'i giriş gününden önceki son geçerli barında; hedef / stop yalnız giriş ve sonrası |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (OC.oc_veri_hazirla + SY.sy_veri_hazirla); F15 paneli hissenin kendi geçerli kapanışlarıyla (120 bar) |
| K4 | tekilleştirme | EVET | Y9* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; F15 / F17 / F11 oran, F1 sayı (birimden bağımsız); AVR yerel para |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Y9) olaylarda batan hisse eksikliği daha büyük olabilir (dipteki hissenin batma olasılığı yüksek) -> Y9 hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | huni ön kayıtta (getirisiz); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; iki yarı KAT (TERS kuralında şart); Y9 / Y9b / Y9c x 4 karar hücresi BH q 0,10 (bilgi, ayrı aile 'bh_tur3'); bakılmış hücreler işaretli, etiket en fazla EMARE; dış sınama 2016-22 ABD / AVR ayrı satır; BIST ayrı başlık; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_3.md: YH_ESIK sha (yeni), ESIK_TUR2_SHA (= ON_KAYIT_2.md YH_ESIK_SHA: Y1-Y8B eşikleri aynen), ESIK_TUR1_SHA, kod / OC / S6 / FV / güç / Y2 sha, OZELLIK_SHA (ozellik_Y1.csv.gz), Y1_OLAY_SHA (regresyon dosyası); yh_kapi(tur 3) hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit, ölçüm ikinci commit; §2 dürüstlük notu aynen: ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldü (bakılmış), etiket en fazla EMARE |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve GOZ_ETIKET özellik dosyası (sha mühürlü; 5 olay / deneme x pazar ham veriden yeniden hesaplanıp karşılaştırılır) |
| K11 | yeniden üretim | EVET | olay_Y9*.csv.gz satır dosyaları; RAPOR_3.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; Y1 regresyonu: ölçülen her Y9* satırı olay_Y1.csv.gz satırına eşit (DURUR) ve Y1 ABD 2023 n 2040 KAT5 0,9752 sonuc.json'da aynen |
| K12 | ifade | EVET | etiket yalnız YH_ESIK Y9 'tur3_kural' ile (en fazla EMARE; TERS EMARE iki yönlü kural); Y9d 'bilgi'; 'iz değil' yazılmaz; sayı ve yorum ayrı; bakılmış hücre sonuçları 'bağımsız kanıt' diye sunulmaz |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y9 önekli); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar taraması; push yok; kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## SAPMALAR

(yok)

## Test

`python test_yapi_hedef.py` (önceki turların testleri aynen + 3. tur: özellik birleştirme sembol + tarih (satır sırası karışık dosya), Y9 / Y9b / Y9c / Y9d seçimi, F1 / F11 / F15 / F17 = GOZ_ETIKET.ge_ozellik_bar, prefix (geleceğe bakma), F15 paneli = elle, konum eşli KAT elle = kod, TERS ve 3. tur etiketi, ESIK_TUR2_SHA = 2. tur mührü, 3. tur uçtan uca onkayit3 + kos + kapı, önceki turların sonuçları değişmez).
