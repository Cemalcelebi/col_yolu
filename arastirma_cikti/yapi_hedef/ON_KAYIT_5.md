# YAPI_HEDEF — ÖN KAYIT 5 (5. tur: Ş9 'U DİP + PARABOLİK DEVAM' Y11 / Y11b + Y11c bilgi; TUR 4 kuru sayım T1.5)

YAPI_HEDEF v1.0 (2026-11-17): yapı kuralları Y1-Y5, hedef +%5 / +%10 stop'tan önce 15 bar, geçici takip stopu, eş + plasebo; 5. tur eklendi (YAPI_HEDEF_IS_TANIMI_5.md)

- YH_ESIK_SHA: `bde83033af9c3a4d1f293278679ff33d7739dfc783a1b75fb391f49399d644a9` (5. tur denemeleri dahil)
- ESIK_TUR4_SHA: `a829103f78a183a0ddbc0572c13f3450a1bcb7e5704cc38ea26259505bd57917` (YH_ESIK'ten Y11-Y11c çıkarılınca; = ON_KAYIT_4.md YH_ESIK_SHA: Y1-Y10c eşikleri AYNEN)
- ESIK_TUR3_SHA: `e209191952e67c8fdd86ce737507ee3e11a40d714449ed2d008805a65a4b193d` (= ON_KAYIT_3.md YH_ESIK_SHA)
- ESIK_TUR2_SHA: `d4ab206a2d2cf8ed25f2c3fd7f30c7122f6460a40040255788ea62ff9cdfbbe1` (= ON_KAYIT_2.md YH_ESIK_SHA)
- ESIK_TUR1_SHA: `adf680258917f69edee2d4eeacfe35bff281f2cbb48f9ee9312c54ab0f3d6f7b` (= ON_KAYIT.md YH_ESIK_SHA = güç tablosu)
- YH_KOD_SHA: `ac291437cbbd1d8928154fcab15dce363dea180f911e18097729c36c9875273c` (YAPI_HEDEF.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- FV_KOD_SHA: `c62b736a3da17c33b380d38a59c9b69487c4d78b3a3dd37ae7e019c8ea47cd5e` (FITIL_V2.py)
- GE_KOD_SHA: `e8d3f20293633d0166e35974252ee8539bc92a3bd4163f4c05b8f444da500a46` (GOZ_ETIKET.py; F1-F18 yeniden hesabı, T1.5 örneklemi)
- GUC_SHA: `b7b63dbdbbf6305744e226d4095cc2154c14fbbe8b2ca84545cab8b27436a913` (guc_tablosu.json; 1. turun güç tablosu, aynı kural)
- Y2_OLAY_SHA: `ac6f4a72550e4aecea9ba6de9bc8469adaf6f004a9531cc9653d9734fdb134ea` (değişmedi; 5. turda kullanılmaz)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (goz_etiket/ozellik_Y1.csv.gz; F1-F18)
- S7_OZELLIK_SHA: `9463e08e6bb7eb95820eccc9be9dcb3a1d549312dc62cdcc657b2a2b02e6137d` (yapi_hedef/ozellik_Y1_s7.csv.gz; F20-F23, F22a; 4. turdaki dosya)
- S9_OZELLIK_SHA: `c9a6a4e62673fcc56cc82550c915feed3be4b7235ada8a940d4de09ff0f28756` (yapi_hedef/ozellik_Y1_s9.csv.gz; F24-F29)
- TASARIM5_SHA: `a6cbda2179d4e5f03cd87f8ba9eff573bd1dd0da9642885c7e4f05abeb22bd70` (yapi_hedef/tasarim5.json; tasarım kontrolü kaydı)
- S7PDF_KOD_SHA: `81044ecc0a1e5d7ed67469254e58b0d42bfae1e4645f7f703f78d8c12ee4969c` (yapi_hedef/s7_bolge_pdf.py; No 38 sırası, §5 50 olay)
- Y1_OLAY_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (yapi_hedef/olay_Y1.csv.gz; regresyon dosyası)
- ON_KAYIT_4: git b4b701ce80, 2026-11-18T18:16:10+00:00
- IS_TANIMI_5: git 5fd664b9e8, 2026-11-19T03:47:20+00:00
- ZAMAN (UTC): `2026-11-19 04:20:51 UTC`

Bu dosya 5. tur ölçümünden ÖNCE yazıldı. Y11 / Y11b / Y11c için alt ajan hiçbir hedef payı / stop payı / eş oranı / plasebo / getiri / konum eşli oran hesaplamadı ve okumadı (yalnız aşağıdaki getirisiz huni, olay sayımı ve tasarım kontrolü; S9 özellik dosyası yalnız fiyat [t-291, t-1]). `kos --deneme Y11,Y11b,Y11c` bu dosyanın kontrol listesini, sha'larını, git kaydını ve Y1-Y10c eşik mührünü denetler; biri tutmazsa durur. Eşikler sonuç görüldükten sonra değişmez.

## Ş9 TANIMI (iş tanımı 5 §2, AYNEN)

W = son 40 geçerli barın Low serisi L_x, x = 0..39 (x = 39 -> t-1). 40 bar yoksa NaN = tutmaz. ATR = ATR250 (öncesi; GOZ_ETIKET F3'teki tanım).
İkinci derece en küçük kareler: L ≈ a x² + b x + c. Özellikler (ozellik_Y1_s9.csv.gz; sembol, tarih):
- F24 = a / ATR (çanak katsayısı; > 0 çanak, < 0 şemsiye),
- F25 = x* / 39, x* = -b / (2a) (dip konumu; a <= 0 ise NaN),
- F26 = R² (uyum iyiliği),
- F27 = (uyum(0) - uyum(x*)) / ATR (sol derinlik; x* pencere dışındaysa uyum(min(max(x*,0),39))),
- F28 = (uyum(39) - uyum(x*)) / ATR (sağ kalkış = parabolik devam),
- F29 = argmin(L) - x* (gerçek en düşük dibin uyum dibinden bar uzaklığı; daha derin dip sonra geldiyse büyük pozitif).
Ş9 TUTAR ⇔ F24 > 0 VE 0,20 <= F25 <= 0,75 VE F26 >= 0,40 VE F27 >= 1,0 VE F28 >= 0,5 VE |F29| <= 5.
TASARIM KONTROLÜ (sonuç OKUMADAN, ön kayıttan ÖNCE, bir kez): (a) S7 PDF'i No 38 olayı (s7_bolge_pdf.py'nin sırasıyla AVR 2016-22 listesinden 7. olay; betikle bul) Ş9'u GEÇMEMELİ; (b) Cemal'in OLUR deyip kazan çizdiği TUR 2 sayfaları 1, 3, 11, 22 (tur_2_anahtar.json) Ş9'u en az 3 / 4 GEÇMELİ. (a) ya da (b) tutmazsa yalnız F26 eşiği (0,30..0,50) ve F25 aralığı (alt 0,15..0,25) BİR KEZ ayarlanabilir; ayar ve gerekçesi ON_KAYIT_5.md'ye yazılır; sonra eşik kilitlenir. Bu kontrol h5 / st5 / getiri OKUMAZ.

## TASARIM KONTROLÜ (sonuç OKUMADAN, ön kayıttan ÖNCE; h5 / st5 / getiri okunmadı)

Kayıt 1 (2026-11-19 03:57:29 UTC; eşik F25 [0.2, 0.75], F26 >= 0.4, F27 >= 1.0, F28 >= 0.5, |F29| <= 5.0): (a) No 38 Ş9'u GEÇMEDİ (istenen); (b) TUR 2 kazan sayfaları 2 / 4 geçti (en az 3 istenir) -> TUTMADI.

| Olay | F24 a/ATR | F25 x*/39 | F26 R² | F27 sol derinlik | F28 sağ kalkış | F29 argmin - x* | alt şartlar a·b·c·d·e·f | Ş9 |
|---|---|---|---|---|---|---|---|---|
| S7 PDF No 38 (AVR 2016-22, AVR 7.) | 0,002 | 1,234 | 0,874 | 4,415 | 0,000 | -17,107 | ✓·✓✓·· | tutmaz |
| TUR 2 sayfa 1 | -0,003 | - | 0,372 | - | - | - | ······ | tutmaz |
| TUR 2 sayfa 3 | -0,005 | - | 0,803 | - | - | - | ··✓··· | tutmaz |
| TUR 2 sayfa 11 | 0,005 | 0,585 | 0,487 | 2,637 | 1,329 | -2,809 | ✓✓✓✓✓✓ | TUTAR |
| TUR 2 sayfa 22 | 0,005 | 0,530 | 0,541 | 2,132 | 1,680 | -3,660 | ✓✓✓✓✓✓ | TUTAR |

SONUÇ: TUTMADI (1 kayıt; AYAR YAPILMADI). Eşik bundan sonra KİLİTLİ.

AYAR KULLANILMADI — gerekçe: (b) 2 / 4: TUR 2 sayfa 1 ve 3'te son 40 barın Low uyumunda a < 0 (F24 -0,003 / -0,005: şemsiye, x* tanımsız). İzinli tek ayar yalnız F26_min (0,30..0,50) ve F25_alt (0,15..0,25); ikisi de F24 > 0 şartını değiştiremez, bu iki sayfa hiçbir izinli ayarda geçemez (en iyi 2 / 4). Ayar KULLANILMADI; iş tanımı §2 eşikleri kilitlendi. (a) No 38 geçmedi (F25 1,23 > 0,75; F28 0,00 < 0,5; |F29| 17,1 > 5). Tanı (bilgi, eşiği değiştirmez): sayfa 1 ve 3'te 60-80 barlık pencerede a > 0 (U 40 bardan uzun).

## BAKILMIŞ HÜCRE İŞARETİ

- BAKILMIŞ: ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26. Y11 / Y11b Y9'un alt kümesi (Ş1 = Y9 şartı); Y9 hücreleri 3. turda görüldü (Y11c Y1'in alt kümesi; Y1 hücreleri 1. turda görüldü). Etiket EN FAZLA EMARE.
- DIŞ SINAMA: ABD 2016-22, AVR 2016-22 — kısmen bakılmış (Y9 alt kümesi; Y9 dış sınama hücreleri 3. tur raporunda görüldü); 'bağımsız' denmez (4. tur H-c dersi). Karar kuralıyla aynı 4 şart; ikisi de TUTAR -> 'EMARE (dış sınama tuttu)'.
- BIST (bilgi, ayrı başlık): BIST 2016-22, BIST 2023, BIST 2024-26 — kısmen bakılmış (Y9 alt kümesi).
- Asıl karar: Mart 2027 ileri testi (kriz sonrası veri, aynı eşik, aynı komut).

## Ölçü, kontrol grupları, karar kuralı (1., 3. ve 4. turla AYNI; YH_ESIK 'olcu', 'kontrol', 'kat', 'karar', 'etiket', 'guc' değişmedi)

- Ufuk: giriş barı (bar 0) dahil hissenin ilk 15 geçerli barı; bu 15 bar giriş gününden itibaren en çok 30 birleşik takvim günü içinde olmalı, yoksa (seyrek işlem / kriz kesiği / veri sonu) o hisse o gün ölçülmez (olay, eş, taban, plasebo aynı kural).
- Stop / hedef: bar k: (1) kapanış, bar k-1 sonundaki stop'un ötesinde (yön +: altında) -> STOP (çıkış bar k+1 açılışı); (2) değilse +%5 / +%10 kapanışla görüldü mü işaretlenir (bilgi: High >= hedef; aynı barda kapanış stop'u -> stop önce); (3) stop güncellenir: stop = max(stop, giriş x 1,02 [+%5 görüldüyse], giriş x 1,07 [+%10 görüldüyse], en yüksek kapanış x 0,93). Yön -: min ve aynası (giriş x 0,98 / 0,93, en düşük kapanış x 1,07).
- EŞ: aynı giriş günü d, aynı OC kovası (H[d]), havuzda (ok[d]), olay hissesi hariç, 15 barı ölçülebilir; stop0 = giriş_eş x (1 - d) (yön -: 1 + d), aynı hedefler, aynı takip kuralı.
- PLASEBO: olay başına 1: aynı hisse, aynı dönem (giriş günü dönemi), havuzda (ok), olay gününden farklı rastgele giriş günü; aynı d, aynı kural; ölçülemezse yeniden çekilir (en çok 50); rastgelelik tohum [1717, deneme no, pazar no, d, j].
- Karar: hücre TUTAR = (1) n >= 30 (h5 ve eş h5 ölçülebilir olay) VE (2) KAT5 (eş) %95 alt uç > 1 VE (3) P(stop önce) olay < eş (nokta) VE (4) plasebo KAT5 %95 alt uç > 1 (plasebosu ölçülebilir olaylar).
- Hücre durumu: n < 30 -> ÖLÇÜLEMEDİ; TUTAR; değilse güç yeterli (n >= 1.000 YA DA güç(n, KAT 1,25) >= %80) -> DESTEKLENMEDİ; değilse ÖLÇÜLEMEDİ.
- Kural etiketi (deneme başına): dört karar hücresi TUTAR -> İZ (BIST iki hücre de TUTAR ise 'İZ + BIST'); 2-3 karar hücresi TUTAR (tek pazarın iki dönemi dahil) -> EMARE (hücreler); 1 karar hücresi TUTAR -> öteki üç karar hücresi DESTEKLENMEDİ ise 'DESTEKLENMEDİ (tek hücre tuttu: ...)', değilse 'ÖLÇÜLEMEDİ (tek hücre tuttu: ...)'; 0 -> dördü DESTEKLENMEDİ ise DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ. 'İz değil' sözü yazılmaz.
- 3. tur ek kuralları (5. turda AYNEN): etiket: Karar hücreleri ve hücre kuralı 1. turla AYNI (yh_etiket); ama ABD / AVR 2023 ve 2024-26 hücreleri ana modelin ön kayıtsız bakışında görüldüğü için ('bakılmış') etiket EN FAZLA EMARE: kural İZ ya da EMARE verirse 'EMARE (bakılmış hücreler)'; dış sınama (ABD 2016-22 VE AVR 2016-22) iki hücre de TUTAR ise 'EMARE (dış sınama tuttu)'. Kural EMARE / İZ vermezse kural etiketi aynen yazılır (dış sınama sonucu ayrı satırda). İKİ YÖNLÜ: >= 2 karar hücresi TERS ise 'TERS EMARE (bakılmış hücreler)'; ayrıca ABD 2016-22 VE AVR 2016-22 TERS ise 'TERS EMARE (dış sınama tuttu)'; ters etiket her Y9 denemesi için ayrı satırda yazılır. BIST hücreleri yalnız bilgi (ayrı başlık). Mart 2027 ileri testi asıl karar.
- TERS: hücre TERS = n >= 30 VE KAT5 (eş) %95 ÜST uç < 1 VE iki yarı KAT5 (giriş sırasına göre ilk / ikinci yarı) ikisi de < 1.
- Konum eşli KAT: KONUM EŞLİ KAT (zorunlu bilgi satırı): eş = 1. turun eşi (aynı giriş günü, aynı OC kovası, havuzda, olay hissesi hariç, 15 barı ölçülebilir, AYNI d ve kural) VE eşin F15'i olayın F15 çeyreğinde; eşin F15'i = giriş gününden ÖNCEKİ son geçerli barında (olayın t'siyle aynı bilgi anı) t dahil son 120 geçerli kapanışla aynı formül; en az 3 eş; KAT ve ay kümeli %95 1. turla aynı (yh_kat). Olayın çeyreği dosyadaki F15'ten.
- Çeyrek: F15 çeyreği: Ç1 [0, 0,25], Ç2 (0,25, 0,50], Ç3 (0,50, 0,75), Ç4 [0,75, 1] (Y9 / Y9c sınırlarıyla aynı).
- Konum uyumu: olayların panelden hesaplanan F15 çeyreği dosyadaki çeyrekle >= %99 aynı olmalı (aynı formül denetimi), değilse koşu DURUR.

## 5. tur kuralları (önceden yazılı; DEĞİŞMEZ)

- Etiket: 3. / 4. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket; ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS iki yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Y11 / Y11b Y9'un alt kümesi (Ş1 = Y9 şartı): dış sınama ve BIST hücreleri 'kısmen bakılmış (Y9 alt kümesi)' yazılır, 'bağımsız' denmez (4. tur H-c dersi).
- Çoklu karşılaştırma: Y11 / Y11b x 4 karar hücresi BH q 0,10 (aile 'bh_tur5'); BH yalnız n >= 30 hücreler arasında hesaplanır ve basılır (4. tur H-d dersi); n < 30 hücre 'BH dışı (n < 30)'; Y11c bilgi.
- Regresyon: Y11* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y10c eşikleri AYNEN (yh_esik_sha_tur4 = ON_KAYIT_4.md YH_ESIK_SHA).
- Huni: Y1 -> +Ş1 -> +Ş2 -> +Ş9 (= Y11); Y10 (Ş1-Ş8) -> Ş6 çıkar -> +Ş9 (= Y11b); Y1 -> +Ş9 (= Y11c); pazar x dönem; getirisiz, ön kayıtta.
- S9 özellikleri: F24-F29 ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal günü (geçerli bar sırası i); W = Low[i-40 .. i-1]; ATR = GOZ_ETIKET F3 ATR250 tanımı (öncesi): w0 = i-40, cnt = min(250, w0-1), ATR_göreli = ort(TR / C_önceki, [w0-cnt, w0-1]) (cnt < 120 -> NaN); fiyat birimine pencerenin ortalama kapanışıyla çevrilir: ATR = ATR_göreli x ort(Close[i-40 .. i-1]); yalnız [i-291, i-1] barları okunur (t barı girmez); dosya ozellik_Y1_s9.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak).

## Denemeler (sonuç görülmeden sabit; iş tanımı 5 §3)

- **Y11 U DİP ÇEKİRDEK**: Y1 OLAYI VE Ş1 DİPTE VE Ş2 HAT NET VE Ş9 U DİP (az şart: n korunsun; her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir (şartlar: Ş1, Ş2, Ş9).
- **Y11b S7 v2 (Ş6 yerine Ş9)**: Y1 olayı VE Y10'un sekiz şartı, Ş6 yerine Ş9: Ş1, Ş2, Ş3, Ş4, Ş5, Ş9, Ş7, Ş8 (eşikler Y10 / Y11 ile AYNI) (şartlar: Ş1, Ş2, Ş3, Ş4, Ş5, Ş9, Ş7, Ş8).
- **Y11c Ş9 TEK BAŞINA (bilgi, konumsuz)**: Y1 olayı VE Ş9 (Ş1 yok): U dip şekli tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil (şartlar: Ş9).

Şartlar: Ş1-Ş8 = 4. tur (YH_ESIK Y10 'sart_tanim', eşikler AYNEN); Ş9:

- Ş9: U DİP + PARABOLİK DEVAM (K47 / K40): W = t'den önceki son 40 geçerli barın Low'u (x = 0..39, x = 39 -> t-1); L ≈ a x² + b x + c (en küçük kareler); F24 = a / ATR > 0 VE 0,20 <= F25 = x* / 39 <= 0,75 (x* = -b / 2a) VE F26 = R² >= 0,40 VE F27 = (uyum(0) - uyum(x*)) / ATR >= 1,0 VE F28 = (uyum(39) - uyum(x*)) / ATR >= 0,5 VE |F29| = |argmin(L) - x*| <= 5 (x* pencere dışındaysa uyum(min(max(x*, 0), 39)); a <= 0 ise F25 / F27 / F28 / F29 NaN; 40 bar ya da ATR yoksa NaN = tutmaz).
- Ş9 eşikleri (kilitli): {"F24_alt_acik": 0.0, "F25_alt": 0.2, "F25_ust": 0.75, "F26_min": 0.4, "F27_min": 1.0, "F28_min": 0.5, "F29_mutlak_ust": 5.0}.

## Yorumlar (iş tanımında açık noktalar; koşudan önce sabit)

- YORUM-1 (ATR birimi): GOZ_ETIKET F3'ün ATR250'si göreli (ort(TR / C_önceki)); Ş9'un F24 / F27 / F28'i fiyat farkı olduğundan göreli ATR pencerenin ortalama kapanışıyla fiyat birimine çevrilir (ATR = ATR_göreli x ort(Close[t-40..t-1])). ATR barları F3'teki gibi pencereden ÖNCE: [w0 - min(250, w0 - 1), w0 - 1], w0 = t-40; 120 bardan azsa NaN.
- YORUM-2 (a <= 0): x* tanımsız -> F25, F27, F28, F29 NaN (F24 > 0 şartı zaten tutmaz).
- YORUM-3 (argmin): eşit en düşük Low'larda ilki (np.argmin).
- YORUM-4 (t barı): Ş9 yalnız t'den önceki 40 Low'u okur; t (sinyal) barı girmez; giriş t+1 açılış.
- YORUM-5 (No 38): s7_bolge_pdf.s7b_olaylar(104) sırası (PDF'teki No); betik olay dosyasının 'ölçülemeyen olay yok' kapısını kendi içinde koşar, tasarım yalnız kimlik sütunlarını alır (sonuç sütunu döndürülmez / yazdırılmaz).
- YORUM-6 (TUR 4 kuru sayım): GOZ_ETIKET T1.5 = T1.4, deneme Y11, olay dosyası olay_Y11.csv.gz (yalnız kimlik sütunları); ge_tur_esik(>= 5) -> T1.5; ge_tur_esik(4) T1.4 olarak DEĞİŞMEDİ (TUR 4'ün hangi sürümle açılacağı ana modelin kararı); kuru sayım tur no 4 (gösterilen = 300 + hakem + TUR 1-3) ve T1.5 ile, dosya yazmadan. `tur ac --no 4` KOŞULMAZ.
- YORUM-7 (Cemal uyumu §5): 4. tur §4 gibi (hakem KÖR 19 + TUR 1 + TUR 2 = 79 sayfa); ayrıca S7 PDF'inin 50 olayında Ş9 tutan sayısı (bilgi; No 38 dahil) koşuda hesaplanır (tasarım kontrolünde yalnız No 38 bakıldı).

## Huni ve getirisiz olay sayımı (sinyal: Y1 olay günü; olay: OC tekil sonrası, giriş dönemi)

### Y11 hunisi

| Aşama | ABD sinyal (tümü) | ABD olay 2016-22 / 2023 / 2024-26 | AVR sinyal (tümü) | AVR olay 2016-22 / 2023 / 2024-26 | BIST sinyal (tümü) | BIST olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|---|---|---|
| Y1 olayı (özellik satırı) | 14881 | 8686 / 2042 / 4153 | 7054 | 4496 / 815 / 1743 | 4728 | 2588 / 381 / 1759 |
| + Ş1 DİPTE | 724 | 346 / 146 / 232 | 164 | 89 / 20 / 55 | 616 | 238 / 81 / 297 |
| + Ş2 HAT NET | 439 | 206 / 93 / 140 | 102 | 51 / 15 / 36 | 365 | 145 / 42 / 178 |
| + Ş9 U DİP = Y11 | 38 | 20 / 3 / 15 | 9 | 6 / 1 / 2 | 22 | 10 / 0 / 12 |
| (ayrı) Y10 = Ş1-Ş8 | 69 | 31 / 13 / 25 | 21 | 9 / 6 / 6 | 116 | 40 / 14 / 62 |
| (ayrı) Y10, Ş6 çıkar (Ş1-Ş5, Ş7, Ş8) | 86 | 38 / 18 / 30 | 25 | 11 / 7 / 7 | 136 | 46 / 15 / 75 |
| (ayrı) + Ş9 = Y11b | 7 | 4 / 0 / 3 | 4 | 2 / 1 / 1 | 13 | 4 / 0 / 9 |
| (ayrı) Y1 + Ş9 = Y11c (bilgi) | 823 | 464 / 143 / 216 | 392 | 231 / 52 / 109 | 297 | 141 / 14 / 142 |

Tek başına düşürdüğü taban sinyali (şart tutmayan): ABD: Ş9 tutmayan 14058, F24 <= 0 / NaN 7451, F25 [0,20, 0,75] dışı / NaN 10997, F26 < 0,40 / NaN 3983, F27 < 1 / NaN 10636, F28 < 0,5 / NaN 9799, |F29| > 5 / NaN 12397, F24 NaN 0, F25 NaN 7451, F26 NaN 0, F27 NaN 7451, F28 NaN 7451, F29 NaN 7451; AVR: Ş9 tutmayan 6662, F24 <= 0 / NaN 3602, F25 [0,20, 0,75] dışı / NaN 5208, F26 < 0,40 / NaN 1896, F27 < 1 / NaN 5316, F28 < 0,5 / NaN 4524, |F29| > 5 / NaN 5855, F24 NaN 0, F25 NaN 3602, F26 NaN 0, F27 NaN 3602, F28 NaN 3602, F29 NaN 3602; BIST: Ş9 tutmayan 4431, F24 <= 0 / NaN 2093, F25 [0,20, 0,75] dışı / NaN 3378, F26 < 0,40 / NaN 1272, F27 < 1 / NaN 2946, F28 < 0,5 / NaN 3233, |F29| > 5 / NaN 3867, F24 NaN 0, F25 NaN 2093, F26 NaN 0, F27 NaN 2093, F28 NaN 2093, F29 NaN 2093.

Y1 eşleşmesi (özellik satırı = Y1 olayı; regresyon): ABD: Y1 sinyal 37969, Y1 olay 14881, özellik 14881, eşleşen 14881; AVR: Y1 sinyal 18783, Y1 olay 7054, özellik 7054, eşleşen 7054; BIST: Y1 sinyal 10242, Y1 olay 4728, özellik 4728, eşleşen 4728.

S9 özellik dosyası denetimi: ABD: 14881 olay, prefix 25 TUTTU, NaN F24 0, F25 7451, F26 0, F27 7451, F28 7451, F29 7451; AVR: 7054 olay, prefix 25 TUTTU, NaN F24 0, F25 3602, F26 0, F27 3602, F28 3602, F29 3602; BIST: 4728 olay, prefix 25 TUTTU, NaN F24 0, F25 2093, F26 0, F27 2093, F28 2093, F29 2093.

| Deneme | Pazar | hisse | olay 2016-22 / 2023 / 2024-26 |
|---|---|---|---|
| Y11 | ABD | 37 | 20 / 3 / 15 |
| Y11 | AVR | 9 | 6 / 1 / 2 |
| Y11 | BIST | 21 | 10 / 0 / 12 |
| Y11b | ABD | 7 | 4 / 0 / 3 |
| Y11b | AVR | 4 | 2 / 1 / 1 |
| Y11b | BIST | 13 | 4 / 0 / 9 |
| Y11c | ABD | 561 | 464 / 143 / 216 |
| Y11c | AVR | 264 | 231 / 52 / 109 |
| Y11c | BIST | 211 | 141 / 14 / 142 |

## Önceden bilinen sınırlar (getirisiz sayımdan; sonuç görülmeden)

- Y11: ABD 2023 en çok 3 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); ABD 2024-26 en çok 15 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2023 en çok 1 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2024-26 en çok 2 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y11b: ABD 2023 en çok 0 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); ABD 2024-26 en çok 3 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2023 en çok 1 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)); AVR 2024-26 en çok 1 olay (güç %0, n < 30 -> ÖLÇÜLEMEDİ (n)). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- Y11c (bilgi): ABD 2023 en çok 143 olay (güç %11); ABD 2024-26 en çok 216 olay (güç %11); AVR 2023 en çok 52 olay (güç %2); AVR 2024-26 en çok 109 olay (güç %11). Bütün karar hücrelerinde n < 1.000 ve güç < %80: tutmayan hücre DESTEKLENMEDİ olamaz, ÖLÇÜLEMEDİ yazılır.
- n üst sınırdır: 15 bar ölçülemeyen ve eşi < 3 olan olaylar ölçümde ayrıca düşer; konum eşli KAT'ta çeyrekte eşi < 3 olan olay o satırdan düşer (k_n ayrı yazılır).
- BH (aile 'bh_tur5') yalnız n >= 30 karar hücreleri arasında; n < 30 hücre 'BH dışı'.
- Hayatta kalma: dipteki (Ş1) hissenin batma olasılığı yüksektir; evrende batan yok -> Y11 / Y11b hedef payı ayrıca yukarı yanlı okunur.

## YH_ESIK 5. tur girdileri (tam metin; geri kalanı ON_KAYIT.md .. ON_KAYIT_4.md ile aynı)

```json
{
 "Y11": {
  "ad": "U DİP ÇEKİRDEK",
  "esik": {
   "F24_alt_acik": 0.0,
   "F25_alt": 0.2,
   "F25_ust": 0.75,
   "F26_min": 0.4,
   "F27_min": 1.0,
   "F28_min": 0.5,
   "F29_mutlak_ust": 5.0
  },
  "s9_prm": {
   "atr_gun": 250,
   "atr_min": 120,
   "bilgi_azami_gun": 291,
   "pencere": 40,
   "tanim": "F24-F29 ham fiyattan (_yh_hazir: geçerli bar H > L, V > 0, O/H/L/C > 0, kriz kesiği); t = sinyal günü (geçerli bar sırası i); W = Low[i-40 .. i-1]; ATR = GOZ_ETIKET F3 ATR250 tanımı (öncesi): w0 = i-40, cnt = min(250, w0-1), ATR_göreli = ort(TR / C_önceki, [w0-cnt, w0-1]) (cnt < 120 -> NaN); fiyat birimine pencerenin ortalama kapanışıyla çevrilir: ATR = ATR_göreli x ort(Close[i-40 .. i-1]); yalnız [i-291, i-1] barları okunur (t barı girmez); dosya ozellik_Y1_s9.csv.gz (pazar, sembol, tarih; 6 anlamlı basamak)"
  },
  "sart_tanim": {
   "S9": "U DİP + PARABOLİK DEVAM (K47 / K40): W = t'den önceki son 40 geçerli barın Low'u (x = 0..39, x = 39 -> t-1); L ≈ a x² + b x + c (en küçük kareler); F24 = a / ATR > 0 VE 0,20 <= F25 = x* / 39 <= 0,75 (x* = -b / 2a) VE F26 = R² >= 0,40 VE F27 = (uyum(0) - uyum(x*)) / ATR >= 1,0 VE F28 = (uyum(39) - uyum(x*)) / ATR >= 0,5 VE |F29| = |argmin(L) - x*| <= 5 (x* pencere dışındaysa uyum(min(max(x*, 0), 39)); a <= 0 ise F25 / F27 / F28 / F29 NaN; 40 bar ya da ATR yoksa NaN = tutmaz)"
  },
  "sartlar": [
   "S1",
   "S2",
   "S9"
  ],
  "taban": "Y1",
  "tanim": "Y1 OLAYI VE Ş1 DİPTE VE Ş2 HAT NET VE Ş9 U DİP (az şart: n korunsun; her şart NaN'da tutmaz). Hat ve stop0 = Y1 ile AYNI; yalnız olay kümesi değişir",
  "tur": 5,
  "tur5_kural": {
   "bh": "Y11 / Y11b x 4 karar hücresi BH q 0,10 (aile 'bh_tur5'); BH yalnız n >= 30 hücreler arasında hesaplanır ve basılır (4. tur H-d dersi); n < 30 hücre 'BH dışı (n < 30)'; Y11c bilgi",
   "etiket": "3. / 4. tur kuralı AYNEN (YH_ESIK Y9 tur3_kural: hücre kuralı yh_etiket; ABD / AVR 2023 ve 2024-26 BAKILMIŞ -> etiket EN FAZLA EMARE; dış sınama ABD / AVR 2016-22 iki hücre TUTAR -> 'EMARE (dış sınama tuttu)'; TERS iki yönlü; konum eşli KAT; çeyrek; konum uyumu >= %99). Y11 / Y11b Y9'un alt kümesi (Ş1 = Y9 şartı): dış sınama ve BIST hücreleri 'kısmen bakılmış (Y9 alt kümesi)' yazılır, 'bağımsız' denmez (4. tur H-c dersi)",
   "huni": "Y1 -> +Ş1 -> +Ş2 -> +Ş9 (= Y11); Y10 (Ş1-Ş8) -> Ş6 çıkar -> +Ş9 (= Y11b); Y1 -> +Ş9 (= Y11c); pazar x dönem; getirisiz, ön kayıtta",
   "regresyon": "Y11* ölçülen satırları olay_Y1.csv.gz'deki aynı (sembol, tarih) satırıyla h5, h10, st5, es_h5, es_h10, es_st5, n_es, tb_h5, getiri sütunlarında eşit (göreli 1e-4), değilse DURUR; Y1-Y10c eşikleri AYNEN (yh_esik_sha_tur4 = ON_KAYIT_4.md YH_ESIK_SHA)"
  },
  "yon": 1
 },
 "Y11b": {
  "ad": "S7 v2 (Ş6 yerine Ş9)",
  "sartlar": [
   "S1",
   "S2",
   "S3",
   "S4",
   "S5",
   "S9",
   "S7",
   "S8"
  ],
  "taban": "Y1",
  "tanim": "Y1 olayı VE Y10'un sekiz şartı, Ş6 yerine Ş9: Ş1, Ş2, Ş3, Ş4, Ş5, Ş9, Ş7, Ş8 (eşikler Y10 / Y11 ile AYNI)",
  "tur": 5,
  "yon": 1
 },
 "Y11c": {
  "ad": "Ş9 TEK BAŞINA (bilgi, konumsuz)",
  "bilgi": true,
  "sartlar": [
   "S9"
  ],
  "taban": "Y1",
  "tanim": "Y1 olayı VE Ş9 (Ş1 yok): U dip şekli tepede / ortada da işliyor mu, konum eşli KAT ile; bilgi satırı, karar değil",
  "tur": 5,
  "yon": 1
 }
}
```

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş / taban / plasebo 1. turla AYNI kod (yh_olc_pazar -> yh_olay_olc, yh_sim; aynı gün, aynı OC kovası, AYNI d, aynı hedef / takip / 15 bar); hat ve stop0 Y1 ile aynı (yalnız olay kümesi değişir); konum eşli KAT (yh_konum_es_olc): eşin F15'i olayın çeyreğinde (Ş1 dipte şartı momentum kovasıyla karışmasın); plasebo aynı hisse rastgele gün; güç tablosu 1. turunki |
| K2 | geleceğe bakma | EVET | F1-F23 4. turun mühürlü dosyalarından; F24-F29 yalnız [t-291, t-1] (yh_s9_ozellik; t barı girmez; dosya üretiminde pazar başına 25 rastgele olay t'de kesik veriyle ve [t-291, t] kesitiyle yeniden = tam: denetim json); koşuda her deneme x pazar 5 rastgele olay: veri t'de kesilir, Y1 sinyali + F1-F18 (GOZ_ETIKET.ge_ozellik_hisse) + F20-F23 + F24-F29 yeniden = dosya, yoksa DURUR (yh_gelecek5); giriş t+1 açılış; eşin F15'i giriş gününden önceki son geçerli bar |
| K3 | geçerli bar | EVET | aynı geçerli bar süzgeci (_yh_hazir = SY.sy_veri_hazirla: H > L, V > 0, O/H/L/C > 0, kriz kesiği); Ş9 penceresi (40) ve ATR (250, en az 120) geçerli bar sayımıyla; 40 bar ya da ATR yoksa NaN = tutmaz |
| K4 | tekilleştirme | EVET | Y11* = Y1 OLAY kümesinin (OC 60 gün tekil) alt kümesi; yh_olc_pazar'da OC yeniden geçer ve hiçbir olay düşmemeli (tekil / havuz dışı / giriş yok > 0 ise DURUR); n bağımsız olay; getiri ortalama + medyan |
| K5 | giriş fiyatı | EVET | giriş t+1 açılışı (OC); eş ve plasebo kendi giriş açılışı (1. tur kodu); Ş9 yalnız t'den önceki Low'lar; regresyon: ölçülen satırlar olay_Y1.csv.gz ile aynı |
| K6 | veri birimi | EVET | aynı V_*.pkl tek kip; F24 / F27 / F28 fiyat farkı / ATR (ATR = göreli ATR250 x pencerenin ortalama kapanışı: birimsiz), F25 / F26 oran, F29 bar; AVR yerel para (birimden bağımsız) |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (batan yok): hedef payı yukarı, stop payı aşağı yanlı; DİPTE (Ş1) olaylarda batan hisse eksikliği daha büyük olabilir -> Y11 / Y11b hedef payı ayrıca yukarı yanlı okunur; eş ve plasebo aynı evrenden; rapora yazılır |
| K8 | örneklem ve dönem | EVET | huni ön kayıtta (getirisiz, Y1 -> Ş1 -> Ş2 -> Ş9; Y10 -> Ş6 çıkar -> Ş9; Y1 -> Ş9; pazar x dönem); n < 30 ÖLÇÜLEMEDİ; DESTEKLENMEDİ yalnız n >= 1.000 ya da güç %80; Y11 / Y11b x 4 karar hücresi BH q 0,10 yalnız n >= 30 hücreler (aile 'bh_tur5'); Y11c bilgi; bakılmış hücreler işaretli, etiket en fazla EMARE; dış sınama / BIST 'kısmen bakılmış (Y9 alt kümesi)'; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | ON_KAYIT_5.md: YH_ESIK sha (yeni), ESIK_TUR4_SHA (= ON_KAYIT_4.md YH_ESIK_SHA: Y1-Y10c eşikleri aynen), ESIK_TUR3/2/1_SHA, kod / OC / S6 / FV / GE kod / güç / Y2 sha, OZELLIK_SHA, S7_OZELLIK_SHA, S9_OZELLIK_SHA, TASARIM5_SHA, Y1_OLAY_SHA; yh_kapi5 hepsini + git kaydını + ik_kontrol_kapisi'ni denetler; tasarım kontrolü (No 38 + TUR 2 kazan sayfaları) ön kayıttan ÖNCE, h5 / st5 / getiri okunmadan, bir kez; ön kayıt ayrı commit, ölçüm ikinci commit; eşikler iş tanımı §2 (tasarım ayarı dışında) AYNEN |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve özellik dosyaları (sha mühürlü; deneme x pazar 5 olay ham veriden yeniden hesaplanıp karşılaştırılır); Cemal etiketleri JSON (sayfa -> OLUR / OLMAZ / BELİRSİZ) |
| K11 | yeniden üretim | EVET | olay_Y11*.csv.gz satır dosyaları; RAPOR_5.md 'YENİDEN ÜRETİM' iki hücre (biri konum eşli KAT) bağımsız komutla; İLERLEME tablosu satır dosyalarından yeniden hesaplanır ve sonuc.json hücreleriyle karşılaştırılır; Y1 regresyonu: ölçülen her Y11* satırı olay_Y1.csv.gz satırına eşit (DURUR) |
| K12 | ifade | EVET | etiket yalnız 3. tur kuralıyla (en fazla EMARE; TERS EMARE iki yönlü kural); Y11c 'bilgi'; Cemal uyum tablosu 'bilgi' (n küçük); 'iz değil' yazılmaz; 'bağımsız' sözü yerine 'kısmen bakılmış (Y9 alt kümesi)'; sayı ve yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (yeni adlar yh_ / YH_ / _Y11 önekli); yasak defter dosyalarına ve tur/1-3 klasörlerine dokunulmadı (git diff); e-posta / anahtar taraması (_yh_yaz); push yok; `tur ac --no 4` KOŞULMADI (yalnız T1.5 kuru örneklem sayımı); kod değişti -> Colab'da 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm |

## SAPMALAR

- SAPMA-1: tasarım kontrolü TUTMADI (a No 38 geçmedi, b TUR 2 2 / 4); izinli tek ayar KULLANILMADI (gerekçe yukarıda); iş tanımı §2 gereği eşik kilitlendi, ölçüm bu eşikle koşar; ölçüm sonucu tasarım kontrolünü değiştirmez.

## Test

`python test_yapi_hedef.py` (önceki turların testleri aynen + 5. tur: F24-F29 yapay vakalar (tam parabol geçer, alçalan zincir geçmez, düz taban F27 < 1 geçmez, şemsiye a < 0 geçmez), prefix değişmezliği, Y11 / Y11b / Y11c seçimi, ESIK_TUR4_SHA = 4. tur mührü, uçtan uca s9ozellik + onkayit5 + kos + kapı + Y1 regresyonu, önceki turların sonuçları değişmez); `python test_goz_etiket.py` (T1.5; TUR 1-3 kapısı).
