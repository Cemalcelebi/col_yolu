# YAPI_HEDEF — ÖN KAYIT 4 (4. tur: S7 'Cemal bölge seçici' Y10 / Y10b + Y10c bilgi; TUR 4 örneklemi hazırlığı)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 4. tur eklendi (YAPI_HEDEF_IS_TANIMI_4.md)

- YH_ESIK_SHA: `a829103f78a183a0ddbc0572c13f3450a1bcb7e5704cc38ea26259505bd57917` (4. tur denemeleri dahil)
- ESIK_TUR3_SHA: `e209191952e67c8fdd86ce737507ee3e11a40d714449ed2d008805a65a4b193d` (YH_ESIK'ten Y10-Y10c çıkarılınca; = ON_KAYIT_3.md YH_ESIK_SHA: Y1-Y9d eşikleri AYNEN)
- ESIK_TUR2_SHA: `d4ab206a2d2cf8ed25f2c3fd7f30c7122f6460a40040255788ea62ff9cdfbbe1` (= ON_KAYIT_2.md YH_ESIK_SHA)
- ESIK_TUR1_SHA: `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b` (= ON_KAYIT.md YH_ESIK_SHA = güç tablosu)
- YH_KOD_SHA: `6dd1023114c8c0de85eade6c461ec1f415793659d2b117a8fa5ed67699f98b11` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- FV_KOD_SHA: `c62b736a3da17c33b380d38a59c9b69487c4d78b3a3dd37ae7e019c8ea47cd5e` (FITIL_V2.py)
- GE_KOD_SHA: `7f5e119fff860935a31bc50b985f87b52febd258f31ae438aa3edff4216e5e3f` (GOZ_ETIKET.py; F1-F18 yeniden hesabı, T1.4 örneklemi)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json; 1. turun güç tablosu, aynı kural)
- Y2_OLAY_SHA: `ac6f4a72550e4aecea9ba6de9bc8469adaf6f004a9531cc9653d9734fdb134ea` (değişmedi; 4. turda kullanılmaz)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)
- S7_OZELLIK_SHA: `9463e08e6bb7eb95820eccc9be9dcb3a1d549312dc62cdcc657b2a2b02e6137d` (yapi_hedef/ozellik_Y1_s7.csv.gz; F20-F23, F22a)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)
- ON_KAYIT_3: git d32c2b187f, 2026-11-18T08:44:58+00:00
- IS_TANIMI_4: git 68e146a84b, 2026-11-18T17:44:18+00:00
- ZAMAN (UTC): `2026-11-18 18:15:53 UTC`

Bu dosya 4. tur ölçümünden ÖNCE yazıldı. Y10 / Y10b / Y10c için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni ve olay sayımı; S7 özellik dosyası yalnız fiyat [t-15, t]). `kos --deneme Y10,Y10b,Y10c` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y9d eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.

## S7 TANIMI (iş tanımı 4 §2, AYNEN)

Y1 olayı = olay_Y1.csv.gz satırı (OC tekil); özellikler ozellik_Y1.csv.gz (F1-F18, 6 anlamlı basamak), parmak_Y1_p11.csv.gz (F19). Yeni özellikler (F20-F23) ham fiyattan (oc_veri / ge_hazir: geçerli bar H>L, V>0, kriz kesiği) hesaplanır ve ozellik_Y1_s7.csv.gz dosyasına yazılır (sembol, tarih anahtarlı; prefix değişmezliği: yalnız [t-250, t] barları).
- Ş1 DİPTE (C6 / VD3; Y9 ile aynı): F15 <= 0,25 VE F17 <= -0,20.
- Ş2 HAT NET (C1; Y9b ile aynı): F1 >= 3.
- Ş3 DİP SAVUNULMUŞ (C2): F2 >= -0,01 (son dokunuş dibi ilk dokunuştan en çok %1 aşağıda).
- Ş4 MUMLAR KÜÇÜK (C3): F3 <= 0,90 (bölge medyan mum boyu / ATR250; parmak P1.1 eşiğiyle aynı).
- Ş5 ALT FİTİL KISA (C4): F4 <= 0,25 (bölge medyan alt fitil payı; P1.x eşiğiyle aynı).
- Ş6 KAZAN SAĞ KENARI DÖNMÜŞ (VD6 / VD9 şart 1): F20 = min Low[t-5..t-1] / min Low[t-15..t-6] - 1 >= 0 (geçerli bar sayımı; 15 bar yoksa NaN = tutmaz).
- Ş7 YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM (VD5 / VD8 / C5): F21 = tavan15 = max High[t-15..t-1]; F22 = C_t / F21 - 1 (kırılım payı, yakın tavana göre) > 0 VE O_t < F21 (gövde tavanı ortalıyor: açılış tavanın altında, kapanış üstünde; boşluklu açılış O_t >= F21 elenir) VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (gövdeli; H_t = L_t ise NaN = tutmaz).
- Ş8 YOL ALMAMIŞ (C10 / C11 / VD2): F18 <= 0,20.
Denemeler (hepsi yön +, giriş t+1 açılış, hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir):
- **Y10 S7 ÇEKİRDEK**: Ş1-Ş8 hepsi.
- **Y10b S7 + BÜYÜK RESİM**: Y10 VE F14 >= 0 (250 bar dip noktaları eğimi aşağı değil; VD9 şart 3).
- **Y10c ŞEKİL KURALLARI, KONUMSUZ (bilgi)**: Ş2-Ş8 (Ş1 yok): Cemal'in şekil kuralları tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil.
- Huni: Y1 -> +Ş1 -> +Ş2 -> ... -> +Ş8 -> +F14 adım adım olay sayıları (pazar x dönem), GETİRİSİZ (ön kayıt dosyasına; sonuç görülmeden).

## BAKILMIŞ HÜCRE İŞARETİ

- BAKILMIŞ: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26. Y10 / Y10b Y9'un alt kümesi; Y9 hücreleri 3. turda görüldü (Y10c Y1'in alt kümesi; Y1 hücreleri 1. turda görüldü). Bu hücreler karar hücreleridir ama sonuçları bağımsız kanıt değildir; etiket EN FAZLA EMARE.
- DIŞ SINAMA (bağımsız kanıt): ABD 2016-22, AVR 2016-22 (karar kuralıyla aynı 4 şart; ikisi de TUTAR -> 'EMARE (dış sınama tuttu)'). NOT: Y9 dış sınama hücreleri (2016-22) 3. tur raporunda görüldü; Y10 / Y10b bunların alt kümesidir.
- BIST (bilgi, ayrı başlık): BIST 2016-22, BIST 2023, BIST 2024-26.
- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).

## Ölçü, kontrol grupları, karar kuralı (1. ve 3. turla AYNI; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi)

- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].
- Karar: hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar).
- Hücre durumu: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.
- Kural etiketi (deneme başına): dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.
- 3. tur ek kuralları (4. turda AYNEN): etiket: Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar.
- TERS: hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1.
- Konum eşli KAT: KONUM EŞLİ KAT (zorunlu bilgi satırı): eş = 1. turun eşi (aynı giriş günü, aynı OC kovası, havuzda, olay hissesi hariç, 15 barı ölçülebilir, AYNI d ve kural) VE eşin F15'i olayın F15 çeyreğinde; eşin F15'i = giriş gününden ÖNCEKİ son geçerli barında (olayın t'siyle aynı bilgi anı) t dahil son 120 geçerli kapanışla aynı formül; en az 3 eş; KAT ve ay kümeli %95 1. turla aynı (yh_kat). Olayın çeyreği dosyadaki F15'ten.
- Çeyrek: F15 çeyreği: Ç1 [0, 0,25], Ç2 (0,25, 0,50], Ç3 (0,50, 0,75), Ç4 [0,75, 1] (Y9 / Y9c sınırlarıyla aynı).
- Konum uyumu: olayların panelden hesaplanan F15 çeyreği dosyadaki çeyrekle >= %99 aynı olmalı (aynı formül denetimi), değilse koşu DURUR.

## 4. tur kuralları (önceden yazılı; DEĞİŞMEZ)

- Etiket: 3. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket, bakılmış hücreler ABD / AVR 2023 ve 2024-26 -> etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS iki yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Bakılmış gerekçesi: Y10 / Y10b Y9'un alt kümesi, Y9 hücreleri 3. turda görüldü; Y10c Y1'in alt kümesi, Y1 hücreleri 1. turda görüldü. Bağımsız kanıt dış sınama ve BIST.
- Çoklu karşılaştırma: Y10 / Y10b x 4 karar hücresi (8 p) BH q 0,10 (aile 'bh_tur4'); Y10c bilgi.
- Regresyon: Y10* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y9d eşikleri AYNEN (yh_esik_sha_tur3 = ON_KAYIT_3.md YH_ESIK_SHA).
- Huni: Y1 -> +Ş1 -> +Ş2 -> ... -> +Ş8 (= Y10) -> +F14 >= 0 (= Y10b); ayrıca Y10c (Ş2-Ş8); getirisiz, ön kayıtta.
- S7 özellikleri: F20-F23 (ve F22a) ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal günü (geçerli bar sırası i); yalnız [t-15, t] barları okunur (prefix: [t-250, t] kesiti ve t'de kesik veri aynı değeri vermeli); dosya ozellik_Y1_s7.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak).

## Denemeler (sonuç görülmeden sabit; iş tanımı 4 §2)

- **Y10 S7 ÇEKİRDEK (Cemal bölge seçici)**: Y1 OLAYI (ozellik_Y1.csv.gz + ozellik_Y1_s7.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile) VE Ş1-Ş8 hepsi (her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir.
- **Y10b S7 + BÜYÜK RESİM**: Y10 olayı VE F14 >= 0 (250 bar dip noktaları eğimi aşağı değil; VD9 şart 3; F14 NaN = tutmaz).
- **Y10c ŞEKİL KURALLARI, KONUMSUZ (bilgi)**: Y1 olayı VE Ş2-Ş8 (Ş1 yok): Cemal'in şekil kuralları tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil.

Şartlar (YH_ESIK Y10 'sart_tanim'; eşikler 'esik'):

- Ş1: DİPTE (C6 / VD3; Y9 ile aynı): F15 <= 0,25 VE F17 <= -0,20.
- Ş2: HAT NET (C1; Y9b ile aynı): F1 >= 3.
- Ş3: DİP SAVUNULMUŞ (C2): F2 >= -0,01 (son dokunuş dibi ilk dokunuştan en çok %1 aşağıda; dokunuş yoksa F2 NaN = tutmaz).
- Ş4: MUMLAR KÜÇÜK (C3): F3 <= 0,90 (bölge medyan mum boyu / ATR250; parmak P1.1 eşiğiyle aynı).
- Ş5: ALT FİTİL KISA (C4): F4 <= 0,25 (bölge medyan alt fitil payı).
- Ş6: KAZAN SAĞ KENARI DÖNMÜŞ (VD6 / VD9 şart 1): F20 = min Low[t-5..t-1] / min Low[t-15..t-6] - 1 >= 0 (geçerli bar sayımı; t'den önce 15 geçerli bar yoksa NaN = tutmaz).
- Ş7: YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM (VD5 / VD8 / C5): F21 = max High[t-15..t-1]; F22 = C_t / F21 - 1 > 0 VE F22a = O_t / F21 - 1 < 0 (açılış tavanın altında; boşluklu açılış O_t >= F21 elenir) VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (H_t = L_t ise NaN = tutmaz).
- Ş8: YOL ALMAMIŞ (C10 / C11 / VD2): F18 <= 0,20.

## Yorumlar (iş tanımında açık noktalar; koşudan önce sabit)

- YORUM-1 (Ş7 açılış): O_t < F21 dosyada F22a = O_t / F21 - 1 < 0 olarak tutulur (6 anlamlı basamak; O_t = F21 -> F22a = 0 -> elenir).
- YORUM-2 (F20 / F21 penceresi): t'den önceki 15 GEÇERLİ bar [t-15, t-1]; sağ = [t-5, t-1], sol = [t-15, t-6]; 15 geçerli bar yoksa NaN (şart tutmaz). Bölge (S6) ile ilgisi yok; yalnız son 15 bar.
- YORUM-3 (F2 NaN): F2 dokunuş yoksa NaN; Ş2 (F1 >= 3) tutan olayda F2 tanımlıdır. Y10c'de Ş2 de şart olduğundan aynı.
- YORUM-4 (Y10c bakılmış): Y10c Y1'in alt kümesidir, Y1 hücreleri 1. turda görüldü; bilgi satırıdır, 3. tur etiketi aynı kuralla yazılır.
- YORUM-5 (Cemal uyumu §4): hakem setinde yalnız KÖR yarı (Cemal OLUR / OLMAZ / BELİRSİZ verdi); AÇIK yarıda yanıt modelin kararına DOĞRU / YANLIŞ olduğu için dışarıda. TUR 1 / TUR 2 bütün sayfalar. Bu bölüm h5 okumaz; Fisher OLUR / OLMAZ x S7 tutar (BELİRSİZ ayrı).
- YORUM-6 (TUR 4 örneklemi): GOZ_ETIKET T1.4 olay dosyası olay_Y10.csv.gz (yalnız kimlik sütunları; ölçüm koşusunun çıktısı, sonuç sütunu okunmaz); uygun = deneme Y10, dönem 2023 / 2024-26, giriş <= kriz - 30 gün, gösterilmemiş olay / hisse. `tur ac --no 4` KOŞULMAZ; yalnız kuru örneklem (dosya yazmadan) ve uygun olay sayıları.

## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)

### Y10 hunisi

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y1 olayı (özellik satırı) | 14881 | 8686 / 2042 / 4153 | 7054 | 4496 / 815 / 1743 | 4728 | 2588 / 381 / 1759 |
| + Ş1 DİPTE | 724 | 346 / 146 / 232 | 164 | 89 / 20 / 55 | 616 | 238 / 81 / 297 |
| + Ş2 HAT NET | 439 | 206 / 93 / 140 | 102 | 51 / 15 / 36 | 365 | 145 / 42 / 178 |
| + Ş3 DİP SAVUNULMUŞ | 393 | 176 / 85 / 132 | 88 | 44 / 13 / 31 | 329 | 135 / 37 / 157 |
| + Ş4 MUMLAR KÜÇÜK | 351 | 152 / 79 / 120 | 82 | 41 / 12 / 29 | 328 | 135 / 36 / 157 |
| + Ş5 ALT FİTİL KISA | 171 | 71 / 36 / 64 | 47 | 22 / 10 / 15 | 244 | 85 / 31 / 128 |
| + Ş6 KAZAN SAĞ KENARI DÖNMÜŞ | 134 | 56 / 26 / 52 | 38 | 18 / 8 / 12 | 196 | 72 / 27 / 97 |
| + Ş7 YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM | 70 | 32 / 13 / 25 | 21 | 9 / 6 / 6 | 116 | 40 / 14 / 62 |
| + Ş8 YOL ALMAMIŞ = Y10 | 69 | 31 / 13 / 25 | 21 | 9 / 6 / 6 | 116 | 40 / 14 / 62 |
| + F14 >= 0 (büyük resim) = Y10b | 20 | 8 / 3 / 9 | 4 | 1 / 2 / 1 | 54 | 14 / 13 / 27 |
| (ayrı) Ş2-Ş8, Ş1 yok = Y10c (bilgi) | 1631 | 873 / 282 / 476 | 936 | 566 / 118 / 252 | 929 | 486 / 58 / 385 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: Ş1 tutmayan 14157, Ş2 tutmayan 5971, Ş3 tutmayan 1758, Ş4 tutmayan 765, Ş5 tutmayan 8057, Ş6 tutmayan 3048, Ş7 tutmayan 6550, Ş8 tutmayan 328, F14 < 0 / NaN 4870, F2 NaN 667, F3 NaN 0, F14 NaN 4, F20 NaN 0, F21 NaN 0, F23 NaN 0; AVR: Ş1 tutmayan 6890, Ş2 tutmayan 2755, Ş3 tutmayan 908, Ş4 tutmayan 516, Ş5 tutmayan 3461, Ş6 tutmayan 1324, Ş7 tutmayan 2719, Ş8 tutmayan 76, F14 < 0 / NaN 2504, F2 NaN 497, F3 NaN 0, F14 NaN 0, F20 NaN 0, F21 NaN 0, F23 NaN 0; BIST: Ş1 tutmayan 4112, Ş2 tutmayan 1881, Ş3 tutmayan 413, Ş4 tutmayan 83, Ş5 tutmayan 1573, Ş6 tutmayan 867, Ş7 tutmayan 1851, Ş8 tutmayan 174, F14 < 0 / NaN 1500, F2 NaN 56, F3 NaN 0, F14 NaN 23, F20 NaN 0, F21 NaN 0, F23 NaN 0.

Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): ABD: Y1 sinyal 37969, Y1 olay 14881, özellik 14881, eşleşen 14881; AVR: Y1 sinyal 18783, Y1 olay 7054, özellik 7054, eşleşen 7054; BIST: Y1 sinyal 10242, Y1 olay 4728, özellik 4728, eşleşen 4728.

S7 özellik dosyası denetimi: ABD: 14881 olay, prefix 25 TUTTU, NaN F20 0, F21 0, F22 0, F22a 0, F23 0; AVR: 7054 olay, prefix 25 TUTTU, NaN F20 0, F21 0, F22 0, F22a 0, F23 0; BIST: 4728 olay, prefix 25 TUTTU, NaN F20 0, F21 0, F22 0, F22a 0, F23 0.

| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|
| Y10 | ABD | 67 | 31 / 13 / 25 |
| Y10 | AVR | 21 | 9 / 6 / 6 |
| Y10 | BIST | 104 | 40 / 14 / 62 |
| Y10b | ABD | 20 | 8 / 3 / 9 |
| Y10b | AVR | 4 | 1 / 2 / 1 |
| Y10b | BIST | 52 | 14 / 13 / 27 |
| Y10c | ABD | 831 | 873 / 282 / 476 |
| Y10c | AVR | 408 | 566 / 118 / 252 |
| Y10c | BIST | 376 | 486 / 58 / 385 |

## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)

- Y10: ABD 2023 en çok 13 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); ABD 2024-26 en çok 25 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2023 en çok 6 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2024-26 en çok 6 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y10b: ABD 2023 en çok 3 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); ABD 2024-26 en çok 9 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2023 en çok 2 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2024-26 en çok 1 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y10c (bilgi): ABD 2023 en çok 282 olay (güç %11); ABD 2024-26 en çok 476 olay (güç %57); AVR 2023 en çok 118 olay (güç %11); AVR 2024-26 en çok 252 olay (güç %11). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay o satırdan düşer (k_n ayrı yazılır).
- Hayatta kalma: dipteki (Ş1) hissenin batma olasılığı yüksektir; evrende batan yok -> Y10 / Y10b hedef payı ayrıca yukarı yanlı okunur.

## YH_ESIK 4. tur girdileri (tam metin; geri kalanı ON_KAYIT.md / ON_KAYIT_2.md / ON_KAYIT_3.md ile aynı)

```json
{
 "Y10": {
  "ad": "S7 ÇEKİRDEK (Cemal bölge seçici)",
  "esik": {
   "F15_ust": 0.25,
   "F17_ust": -0.2,
   "F18_ust": 0.2,
   "F1_min": 3,
   "F20_min": 0.0,
   "F22_alt_acik": 0.0,
   "F22a_ust_acik": 0.0,
   "F23_min": 0.5,
   "F2_min": -0.01,
   "F3_ust": 0.9,
   "F4_ust": 0.25
  },
  "s7_prm": {
   "bilgi_azami_gun": 250,
   "sag": 5,
   "sol": 15,
   "tanim": "F20-F23 (ve F22a) ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal günü (geçerli bar sırası i); yalnız [t-15, t] barları okunur (prefix: [t-250, t] kesiti ve t'de kesik veri aynı değeri vermeli); dosya ozellik_Y1_s7.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak)",
   "tavan_gun": 15
  },
  "sart_tanim": {
   "S1": "DİPTE (C6 / VD3; Y9 ile aynı): F15 <= 0,25 VE F17 <= -0,20",
   "S2": "HAT NET (C1; Y9b ile aynı): F1 >= 3",
   "S3": "DİP SAVUNULMUŞ (C2): F2 >= -0,01 (son dokunuş dibi ilk dokunuştan en çok %1 aşağıda; dokunuş yoksa F2 NaN = tutmaz)",
   "S4": "MUMLAR KÜÇÜK (C3): F3 <= 0,90 (bölge medyan mum boyu / ATR250; parmak P1.1 eşiğiyle aynı)",
   "S5": "ALT FİTİL KISA (C4): F4 <= 0,25 (bölge medyan alt fitil payı)",
   "S6": "KAZAN SAĞ KENARI DÖNMÜŞ (VD6 / VD9 şart 1): F20 = min Low[t-5..t-1] / min Low[t-15..t-6] - 1 >= 0 (geçerli bar sayımı; t'den önce 15 geçerli bar yoksa NaN = tutmaz)",
   "S7": "YAKIN TAVAN + GÖVDELİ ORTALAYAN KIRILIM (VD5 / VD8 / C5): F21 = max High[t-15..t-1]; F22 = C_t / F21 - 1 > 0 VE F22a = O_t / F21 - 1 < 0 (açılış tavanın altında; boşluklu açılış O_t >= F21 elenir) VE F23 = |C_t - O_t| / (H_t - L_t) >= 0,50 (H_t = L_t ise NaN = tutmaz)",
   "S8": "YOL ALMAMIŞ (C10 / C11 / VD2): F18 <= 0,20"
  },
  "sartlar": [
   "S1",
   "S2",
   "S3",
   "S4",
   "S5",
   "S6",
   "S7",
   "S8"
  ],
  "taban": "Y1",
  "tanim": "Y1 OLAYI (ozellik_Y1.csv.gz + ozellik_Y1_s7.csv.gz satırı = olay_Y1.csv.gz satırı, sembol + tarih ile) VE Ş1-Ş8 hepsi (her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir",
  "tur": 4,
  "tur4_kural": {
   "bh": "Y10 / Y10b x 4 karar hücresi (8 p) BH q 0,10 (aile 'bh_tur4'); Y10c bilgi",
   "etiket": "3. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket, bakılmış hücreler ABD / AVR 2023 ve 2024-26 -> etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS iki yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Bakılmış gerekçesi: Y10 / Y10b Y9'un alt kümesi, Y9 hücreleri 3. turda görüldü; Y10c Y1'in alt kümesi, Y1 hücreleri 1. turda görüldü. Bağımsız kanıt dış sınama ve BIST",
   "huni": "Y1 -> +Ş1 -> +Ş2 -> ... -> +Ş8 (= Y10) -> +F14 >= 0 (= Y10b); ayrıca Y10c (Ş2-Ş8); getirisiz, ön kayıtta",
   "regresyon": "Y10* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y9d eşikleri AYNEN (yh_esik_sha_tur3 = ON_KAYIT_3.md YH_ESIK_SHA)"
  },
  "yon": 1
 },
 "Y10b": {
  "F14_min": 0.0,
  "ad": "S7 + BÜYÜK RESİM",
  "taban": "Y10",
  "tanim": "Y10 olayı VE F14 >= 0 (250 bar dip noktaları eğimi aşağı değil; VD9 şart 3; F14 NaN = tutmaz)",
  "tur": 4,
  "yon": 1
 },
 "Y10c": {
  "ad": "ŞEKİL KURALLARI, KONUMSUZ (bilgi)",
  "bilgi": true,
  "sartlar": [
   "S2",
   "S3",
   "S4",
   "S5",
   "S6",
   "S7",
   "S8"
  ],
  "taban": "Y1",
  "tanim": "Y1 olayı VE Ş2-Ş8 (Ş1 yok): Cemal'in şekil kuralları tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil",
  "tur": 4,
  "yon": 1
 }
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); hat ve stop0 Y1 ile aynı (yalnız olay kümesi değişir); konum eşli KAT (yh_konum_es_olc, 3. tur kodu): eşin F15'i olayın çeyreğinde (Ş1 dipte şartı momentum kovasıyla karışmasın); plasebo aynı hisse rastgele gün; güç tablosu 1. turunki |
| K2 | geleceğe bakma | EVET | F1-F18 GOZ_ETIKET dosyasından (yalnız [.., t]; aşama A prefix denetimi); F20-F23 yalnız [t-15, t] (yh_s7_ozellik; dosya üretiminde pazar başına 25 rastgele olay t'de kesik veriyle ve [t-250, t] kesitiyle yeniden = tam: denetim json); koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 yeniden = dosya, yoksa DURUR (yh_gelecek4); C_t / O_t sinyal günü (giriş t+1 açılış); eşin F15'i giriş gününden önceki son geçerli bar |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); F20 / F21 pencereleri geçerli bar sayımıyla; H_t = L_t bar veride yok (F23 NaN tutmaz) |
| K4 | tekilleştirme | EVET | Y10* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); Ş7 O_t / C_t sinyal günü (t) değerleri, giriş değil; regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; F2 / F3 / F4 / F11 / F14 / F15 / F17 / F18 / F20 / F22 / F22a / F23 oran, F1 sayı, F21 fiyat (yalnız aynı hissenin C_t / O_t ile oranda kullanılır); AVR yerel para |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Ş1) olaylarda batan hisse eksikliği daha büyük olabilir -> Y10 / Y10b hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | huni ön kayıtta (getirisiz, Ş1..Ş8 adım adım, pazar x dönem); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; Y10 / Y10b x 4 karar hücresi BH q 0,10 (aile 'bh_tur4'); Y10c bilgi; bakılmış hücreler işaretli, etiket en fazla EMARE; dış sınama 2016-22 ABD / AVR ayrı satır; BIST ayrı başlık; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_4.md: YH_ESIK sha (yeni), ESIK_TUR3_SHA (= ON_KAYIT_3.md YH_ESIK_SHA: Y1-Y9d eşikleri aynen), ESIK_TUR2_SHA, ESIK_TUR1_SHA, kod / OC / S6 / FV / GE kod / güç / Y2 sha, OZELLIK_SHA, S7_OZELLIK_SHA, Y1_OLAY_SHA; yh_kapi4 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler iş tanımı §2 AYNEN |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve özellik dosyaları (sha mühürlü; deneme x pazar 5 olay ham veriden yeniden hesaplanıp karşılaştırılır); Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ) |
| K11 | yeniden üretim | EVET | olay_Y10*.csv.gz satır dosyaları; RAPOR_4.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; Y1 regresyonu: ölçülen her Y10* satırı olay_Y1.csv.gz satırına eşit (DURUR); Y1 ABD 2023 n 2040 KAT5 0,9752 sonuc.json'da aynen |
| K12 | ifade | EVET | etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS EMARE iki yönlü kural); Y10c 'bilgi'; Cemal uyum tablosu 'bilgi' (n küçük); 'iz değil' yazılmaz; sayı ve yorum ayrı; bakılmış hücre sonuçları 'bağımsız kanıt' diye sunulmaz |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y10 önekli); yasak defter dosyalarına ve tur/1-3 klasörlerine dokunulmadı (git diff); e-posta / anahtar taraması (_yh_yaz); push yok; tur ac --no 4 KOŞULMADI (yalnız kuru örneklem sayımı); kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## SAPMALAR

(yok)

## Test

`python test_yapi_hedef.py` (önceki turların testleri aynen + 4. tur: F20-F23 yapay vakalar, prefix değişmezliği, Ş7 boşluklu açılış elenir, şart sınırları ve NaN, Y10 / Y10b / Y10c seçimi, ESIK_TUR3_SHA = 3. tur mührü, uçtan uca onkayit4 + kos + kapı + Y1 regresyonu, önceki turların sonuçları değişmez); `python test_goz_etiket.py` (T1.4, tavan_kaynak, TUR 1-3 çıktıları değişmedi kapısı).
