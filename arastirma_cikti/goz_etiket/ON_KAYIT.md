# GOZ_ETIKET — ÖN KAYIT (AŞAMA A; etiketlemeden ve ölçümden ÖNCE)

GOZ_ETIKET v1.0 (2026-11-17): AŞAMA A örneklem (300, tohum 11) + kör PNG (t sonrası yok) + F1-F18 özellik + ön kayıt

- GE_ESIK_SHA: `a48cd64da71616bdd19f05c3d3763997096d520252622812c244516f94a84d5d`
- GE_KOD_SHA: `c97833a5433d21542fd5f2dd42f56f798572c27411f22bd2aec1d7283e5bf563` (GOZ_ETIKET.py)
- YH_KOD_SHA: `1d547ae8a4e4224f9337ba9c3aae859f50037d33e07f45246d37c6a19b2a74ab` (YAPI_HEDEF.py)
- S6_KOD_SHA: `ebfc5ae01ee1c7653923f2c3817d23f937f359ca5307f6daacc0ff504a947c2d` (S6_TABAN.py)
- OC_KOD_SHA: `7bd6f6db4bbc10b83ba926ddbbfb74556909400f73f10168e8a5124ccc6e28eb` (ORTAK_CETVEL.py)
- OLAY_Y1_SHA: `e13eb12699a6d749bccc16ee4cde5ac467ea2bf8687b23a6a821fef74bf8871b` (arastirma_cikti/yapi_hedef/olay_Y1.csv.gz)
- ANAHTAR_SHA: `d711b856ba8117998838c6107784d9222f556b3f952d5ef23dce7930923efa98` (anahtar.json; GİZLİ, etiketleyen açmaz)
- OZELLIK_SHA: `bae156939290b421fb2320f85a2639db71726ca6f7449081e2bc292f5043fd76` (ozellik_Y1.csv.gz)
- IS_TANIMI_SHA: `d288b35ec48219d97d6d39d5f52b47771ed770875d559f447a28a24c833d13d5` (GOZ_ETIKET_IS_TANIMI.md)
- GIT_KOD: c4176c8ad1, 2026-11-17T20:26:13+00:00
- GIT_ANAHTAR: c4176c8ad1, 2026-11-17T20:26:13+00:00
- GIT_OZELLIK: c4176c8ad1, 2026-11-17T20:26:13+00:00
- GIT_IS_TANIMI: 543f766b8d, 2026-11-17T20:15:31+00:00
- ZAMAN (UTC): `2026-11-17 20:26:17 UTC`

Bu dosya AŞAMA B (etiketleme) ve AŞAMA C (ölçüm / eğitim) başlamadan ÖNCE yazıldı. AŞAMA A hiçbir sonuç sütununu (h5, h10, st5, eş, plasebo, getiri, olc ...) okumadı: olay_Y1.csv.gz yalnız kimlik (deneme, pazar, sembol, tarih, giris, donem) ve t'de bilinen sinyal (hat, tavan, ek) sütunlarıyla, usecols ile okundu (GOZ_ETIKET.ge_olay_oku izin listesi; test_goz_etiket). Eşikler sonuç görüldükten sonra değişmez; zorunlu sapma SAPMA-n diye bu dosyaya, ölçümden önce yazılır.

## 1. Örneklem (tohum 11; yalnız kimlik sütunları)

olay_Y1.csv.gz yalnız kimlik sütunları (deneme, pazar, sembol, tarih, giris, donem) okunur. Uygun = deneme Y1, dönem 2023 / 2024-26, giriş <= kriz - 30 gün (2026-08-01; 15 geçerli barlık ölçü penceresi en çok 30 takvim günü, kriz kesiğini aşmasın; yalnız tarih kuralı). Uygunlar (pazar, sembol, tarih) sırasına dizilir; rng = numpy default_rng(11); katmanlar yukarıdaki sırayla gezilir, her katmanda rng.permutation sırasıyla olay alınır, aynı (pazar, sembol) bütün örneklemde en çok 2 (aşan atlanır), kota dolunca durulur (kota dolmazsa DURUR). Sonra 300 olay rng.permutation ile karıştırılır ve No 1..300 verilir (numara pazar / dönem / tarih sırası taşımaz).

| Pazar | Dönem | Kota | Seçilen |
|---|---|---|---|
| ABD | 2023 | 60 | 60 |
| ABD | 2024-26 | 80 | 80 |
| AVR | 2023 | 40 | 40 |
| AVR | 2024-26 | 60 | 60 |
| BIST | 2023 | 20 | 20 |
| BIST | 2024-26 | 40 | 40 |
| Toplam | | 300 | 300 |

- Ayrı hisse: 278; aynı hisseden 2 olay: 22; en çok 2 (sınır 2).
- Numara sırası karıştırılmış (pazar / dönem / tarih bilgisi taşımaz). Sembol ve tarihler yalnız anahtar.json'da.

## 2. Kör görsel

hissenin geçerli bar verisi t'de KESİLİR (t dahil; t'den sonrası fonksiyona hiç girmez); S6 kesik veride yeniden hesaplanır ve hat / tavan olay dosyasındakiyle (göreli 1e-5; csv 6 anlamlı basamak) aynı olmalı; son 120 bar: mum (yeşil C >= O, kırmızı C < O; fitil dahil), alt panelde hacim; S6 bölgesi = mavi yarı saydam dikdörtgen [bölge solu, t-1] x [hat, bölge üstü] (AL: kutu_ust(t), AL_BOLGESIZ: TAVAN(t-1)); tavan çizgisi (turuncu kesik) ve hat çizgisi (mavi) bölge solundan t'ye; x ekseni bar sırası (-119..0, tarih yok); y ekseni gerçek fiyat; başlık yalnız 'No k'; PNG metin parçası yok; dosya adı No_k.png

- PNG sayısı: 300 (repo DIŞI klasör: /tmp/claude-0/-home-user-col-yolu/14e1a07f-5469-51eb-acde-431a683fafa5/scratchpad/goz_etiket/png). Her PNG'de hat / tavan kesik veriden yeniden üretildi ve olay dosyasıyla aynı.

## 3. Sayısal özellikler F1-F18 (bütün Y1 olayları; yalnız t'ye kadar)

BÖLGE = [kutu_sol_i(t), t-1] (durum AL) ya da [bas_i(t-1), t-1] (AL_BOLGESIZ); hat = kutu_alt(t) / DİP(t-1); tavan = TAVAN(t-1) (YAPI_HEDEF Y1 / Y6 ile aynı). Bütün ölçüler yalnız [.., t] geçerli barlarıyla.

- F1: hat dokunuş sayısı: bölgede Low <= hat x 1,015 olan bar sayısı
- F2: hat eğimi: son dokunuşun Low'u / ilk dokunuşun Low'u - 1 (dokunuş yoksa NaN)
- F3: bölge mum boyu medyanı / ATR250: medyan((H - L) / C, bölge) / ort(TR / C_önceki, bölgeden ÖNCEKİ min(250, sol - 1) bar); 120 bardan azsa NaN (YAPI_HEDEF Y7 ATR birimi)
- F4: alt fitil payı medyanı: medyan((min(O, C) - L) / (H - L), bölge)
- F5: açılış-dip yakınlığı: medyan((O - L) / (H - L), bölge)
- F6: üst fitil payı medyanı: medyan((H - max(O, C)) / (H - L), bölge)
- F7: yeşil mum payı: pay(C > O, bölge)
- F8: bölge boyu n: bölgedeki geçerli bar sayısı (t - sol)
- F9: bant: tavan / hat - 1
- F10: net: C(t-1) / C(sol) - 1 (bölgenin son / ilk kapanışı)
- F11: kırılım mumu payı: C_t / tavan - 1
- F12: kırılım mumu gövdesi / bölge medyan mumu: |C_t - O_t| / medyan(H - L, bölge)
- F13: kırılım günü hacmi / bölge medyan hacmi: V_t / medyan(V, bölge)
- F14: büyük desen eğimi: [t-250, t-1] 10 parça x 25 bar dip noktalarına doğru, uyum(9) / uyum(0) - 1 (YAPI_HEDEF.yh_buyuk_egim); 250 bar yoksa ya da uyum(0) <= 0 ise NaN
- F15: 120 gün konumu: (C_t - min C) / (max C - min C), t dahil son 120 geçerli kapanış (aralık 0 ise NaN)
- F16: son 250 barda KIRILDI bölge sayısı: [t-250, t-1] içinde S6 durumu 'KIRILDI' olan bar sayısı (bölge KIRILDI ile biter; YAPI_HEDEF Y8 kir250 ile aynı)
- F17: bölge öncesi 60 gün düşüş: C(sol) / max(C, [sol-60, sol-1]) - 1 (60 geçerli bar yoksa NaN)
- F18: stop uzaklığı: C_t / hat - 1

- Dosya: ozellik_Y1.csv.gz, 26663 satır x (pazar, sembol, tarih, durum, F1-F18).
- Denetim: ABD: olay 14881, hat / tavan eşit 14881, prefix denetimi 10 olay tuttu; AVR: olay 7054, hat / tavan eşit 7054, prefix denetimi 10 olay tuttu; BIST: olay 4728, hat / tavan eşit 4728, prefix denetimi 10 olay tuttu.
- NaN sayısı (F3 ATR geçmişi < 120 bar, F14 250 bar yok, F17 60 bar yok): F2 1220, F14 27.

## 4. AŞAMA B kuralları (etiketleyen; iş tanımı §4)

- Etiketleyen yalnız PNG klasörünü ve iş tanımı §4'ü okur; anahtar.json, olay_Y1.csv.gz, ozellik_Y1.csv.gz, YAPI_HEDEF çıktıları AÇILMAZ.
- Çıktı arastirma_cikti/goz_etiket/etiket.json; 300 PNG'nin hepsi; 'sonrası' tahmini yazılmaz.

## 5. ÖLÇÜM PLANI ve EŞİKLER (iş tanımı §5, AYNEN)

## 5. AŞAMA C — ÖLÇÜM ve EĞİTİM (alt ajan C; etiket.json + anahtar + olay_Y1 + ozellik_Y1)
- Birleştir: etiket x olay sonucu (h5, h10, st5, es_h5, es_st5, getiri).
- ÖLÇÜ 1 (önceden yazılı): OLUR grubunun +%5 payı vs OLMAZ grubunun +%5 payı (Fisher); OLUR KAT5 = Σ h5 / Σ es_h5 (ay kümeli bootstrap %95); OLMAZ KAT5 aynı; P(stop önce) OLUR / OLMAZ / eş. Pazar birleşik (n küçük); pazar bazlı bilgi. TUTAR = OLUR KAT5 alt uç > 1 VE OLUR +%5 payı > OLMAZ +%5 payı (Fisher p < 0,05) VE OLUR stop payı < eş. n OLUR < 30 ise ÖLÇÜLEMEDİ.
- ÖLÇÜ 2 (neden kodları): her C kodu için var / yok +%5 payı ve KAT5 (bilgi, BH q 0,10).
- EĞİTİM (önceden yazılı): F1-F18 ile lojistik regresyon, hedef = OLUR (1) / OLMAZ (0) (BELİRSİZ dışarı); 5 katlı çapraz doğrulama AUC (göz ne kadar sayısal özellikten öğrenilebiliyor); eğitilen model bütün 26.663 Y1 olayına uygulanır: 'GÖZ SKORU'. Üst beşte bir (skor) vs alt beşte bir: +%5 payı, KAT5 (eşli), stop payı; karar hücreleri (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) YAPI_HEDEF karar kuralıyla; etiket İZ / EMARE / ÖLÇÜLEMEDİ / DESTEKLENMEDİ aynı kurallarla. Üst beşte bir n >= 1.000 olan hücrelerde güç yeterli sayılır.
- Sızıntı denetimi: etiketlerin sonuç görmeden verildiği (aşama B ajanı anahtar / olay dosyası açmadı: dosya erişim günlüğü + B'nin raporu), özelliklerin t'ye kadar olduğu (prefix testi), skorun eğitimde kullanılan 300 olay dışında da raporlandığı (dış örneklem ayrı satır).
- RAPOR.md: özet, etiket dağılımı (OLUR / OLMAZ / BELİRSİZ, neden kodu sıklığı), ölçü 1-2 tabloları, eğitim (katsayılar: hangi özellik gözü en çok açıklıyor; AUC), göz skoru hücre tablosu, olasılık tablosu, karar, sınırlar (300 etiket, etiketleyen bir dil modeli = Cemal'in gözünün vekili; Cemal'in kendi etiketi değil). HAKEM PDF'İ (Cemal, 17 Kas akşam: 'tarafsız hakem olayım'): 40 sayfa, iki yarı, sonrası hiçbir sayfada yok, hisse adı yok: (1) sayfa 1-20 KÖR: yalnız grafik; Cemal OLUR / OLMAZ + neden yazar; sonra aşama B etiketiyle uyum ölçülür (Cohen kappa + çapraz tablo); (2) sayfa 21-40 AÇIK: grafik + aşama B'nin kararı + neden kodları + tek cümle notu; Cemal 'doğru / yanlış + neden' yazar; hangi C kuralının yanlış uygulandığı sayılır. Sayfalar 300 etiketli olaydan tohum 13 ile, OLUR / OLMAZ / BELİRSİZ dengeli (her yarıda 8 / 8 / 4) seçilir. Dosya: arastirma_cikti/goz_etiket/GOZ_HAKEM_SET.pdf + hakem_anahtar.json (gizli). Cemal'in yanıtı gelince `python GOZ_ETIKET.py hakem --cevap-dosya` ile iki yarı ayrı raporlanır.

## 6. Yorumlar (iş tanımında açık bırakılan noktalar; ölçümden önce sabit)

- Örneklem uygunluğu: giriş <= kriz - 30 gün (2026-08-01) yalnız tarih kuralıdır; olay_Y1 'olc' (ölçülebilir) sütunu OKUNMADI. Örneklemde ölçülemeyen (olc = False) olay kalırsa AŞAMA C onu ölçüden çıkarır ve sayısını yazar (etiket yine kalır).
- AŞAMA C KAT5 için 'h5' ve 'es_h5' olay_Y1 sütunlarıdır (kapanışla +%5 stop'tan önce, 15 bar; eş = aynı gün aynı OC kovası, aynı d); P(stop önce) = 'st5' / 'es_st5'; 'getiri' = takip stoplu getiri (bilgi).
- Göz skoru eğitimi: BELİRSİZ dışarı; F1-F18 NaN değerleri eğitim örnekleminin medyanıyla doldurulur ve standartlaştırılır (yalnız eğitim verisinden; dış örnekleme aynı dönüşüm); beşte bir sınırları skorun bütün 26.663 olaydaki dağılımından; eğitimde kullanılan 300 olay dış örneklem satırında ayrıca çıkarılarak raporlanır.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | AŞAMA A ölçüm yapmaz (etiket / özellik / görsel); kontrol grubu AŞAMA C'de: §5 eşli KAT5 = Σ h5 / Σ es_h5 (olay_Y1 eş sütunları: aynı giriş günü, aynı OC kovası, aynı d ve kural) ve göz skoru üst / alt beşte bir aynı eşli cetvelle |
| K2 | geleceğe bakma | EVET | örneklem yalnız kimlik sütunlarını okur (ge_olay_oku izin listesi; test: sonuç sütunları silinince / karıştırılınca örneklem aynı); görsel veri t'de kesilerek çizilir (test: t sonrası barlar değişince PNG baytları aynı, son bar = t); F1-F18 yalnız [.., t] (test + koşuda 10 olay / pazar prefix denetimi, tutmazsa DURUR); hat / tavan kesik veriden yeniden üretilir ve olay dosyasıyla aynı |
| K3 | geçerli bar | EVET | veri YAPI_HEDEF._yh_hazir (SY.sy_veri_hazirla: H>L, V>0, O/H/L/C>0) ile; S6 ve bütün özellikler geçerli bar dizisinde; olay günleri Y1 (geçerli bar) |
| K4 | tekilleştirme | EVET | olaylar olay_Y1 (OC.oc_olay_hazirla: aynı hissede 60 gün tekil); örneklemde aynı (pazar, sembol) en çok 2; (pazar, sembol, tarih) tekil denetlenir |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu aşamada hesaplanmaz; AŞAMA C olay_Y1 sonuçlarını (giriş t+1 açılış) kullanır |
| K6 | veri birimi | EVET | tek kip V_*.pkl (düzeltilmiş fiyat; YAPI_HEDEF ile aynı veri, hat / tavan eşitliği denetimi); özellikler oran / pay (birimden bağımsız); görselde y ekseni yerel para gerçek fiyat |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (V_ABD 1.411, k34 yok); örneklem ve özellikler aynı evrenden; AŞAMA C raporuna hayatta kalma notu (hedef payı yukarı yanlı) yazılır |
| K8 | örneklem ve dönem | EVET | 300 etiket küçük örneklem: §5 OLUR n < 30 ÖLÇÜLEMEDİ; pazar birleşik karar, pazar bazlı bilgi; göz skoru karar hücreleri n >= 1.000 güç kuralı; ölçü 2 BH q 0,10; katmanlar iki dönem x üç pazar |
| K9 | ön kayıt | EVET | ON_KAYIT.md: GE_ESIK sha + GOZ_ETIKET / YAPI_HEDEF / S6_TABAN / ORTAK_CETVEL kod sha + olay_Y1 / anahtar / özellik dosyası sha + iş tanımı git kaydı; §5 ölçüm planı ve eşikleri iş tanımından aynen; etiketlemeden ve ölçümden ÖNCE ayrı commit; eşik sonuca göre oynanmaz |
| K10 | ayrıştırma | UYGULANMAZ | haber / KAP / metin ayrıştırma yok; yalnız OHLCV ve olay_Y1 kimlik sütunları |
| K11 | yeniden üretim | EVET | anahtar.json + ozellik_Y1.csv.gz satır dosyaları; tohum 11 ile örneklem ve özellikler aynı komutla yeniden üretilir (test: aynı tohum aynı örneklem); AŞAMA C en az iki hücreyi satır dosyasından yeniden üretir |
| K12 | ifade | EVET | AŞAMA A hiçbir sonuç / iz / emare sözü yazmaz; etiket = Cemal'in gözünün VEKİLİ (dil modeli), Cemal'in kendi etiketi değil (§5 sınırlar); karar dili yalnız §5 kuralıyla |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_ge (test); yasak defter dosyalarına dokunulmadı (git diff); e-posta / anahtar taraması yazım öncesi (_ge_sizinti); PNG'ler repoya girmez (scratchpad); push yok; kod değişirse 'çalışma zamanını yeniden başlat' |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; etiket ve ölçüm hazırlığı |

## SAPMA-1 (AŞAMA C; ana model yazdı, SONUÇ GÖRÜLMEDEN; ölçümden ÖNCE ayrı commit)

Neden: AŞAMA B etiketleri OLUR 6 / BELİRSİZ 51 / OLMAZ 243 (etiket.json; dağılım sonuç değildir). OLUR n = 6 < 30 olduğundan §5 ÖLÇÜ 1 önceden yazılı kuralla ÖLÇÜLEMEDİ olur ve §5 eğitim hedefi (OLUR / OLMAZ, BELİRSİZ dışarı) 6 pozitifle kurulamaz. §5 ölçü 1 ve asıl eğitim yine koşulur ve aynen raporlanır (ÖLÇÜLEMEDİ); aşağıdakiler EKTİR, §5'in yerine geçmez.

- ÖLÇÜ 1b: 'OLMAZ-DEĞİL' (OLUR + BELİRSİZ, n 57) vs OLMAZ (n 243): +%5 payı (h5; Fisher iki yönlü), KAT5 = Σ h5 / Σ es_h5 (ay kümeli bootstrap %95; YAPI_HEDEF.yh_kat = ORTAK_CETVEL.oc_kat algoritması, 2000, tohum 27) iki grup ve eş; P(stop önce) st5 / es_st5. TUTAR = OLMAZ-DEĞİL KAT5 alt uç > 1 VE OLMAZ-DEĞİL +%5 payı > OLMAZ payı (Fisher iki yönlü p < 0,05) VE OLMAZ-DEĞİL stop payı < eş stop payı. OLMAZ-DEĞİL n < 30 ise ÖLÇÜLEMEDİ. Pazar ve dönem kırılımı bilgi.
- EĞİTİM HEDEFİ: OLMAZ-DEĞİL (1) vs OLMAZ (0), 300 etiket; F1-F18; boru hattı medyan doldurma + standartlaştırma + lojistik (L2, C = 1), dönüşümler yalnız eğitim katından; StratifiedKFold(5, karıştır, tohum 13) kat dışı AUC + kat AUC ortalaması; etiket permütasyonu 200 (tohum 1301) ile AUC p (bilgi). Son model 300 olayla; katsayılar standart birimde; tek özellik AUC (bilgi).
- ÖLÇÜ 2 genişletildi: neden kodlarının (C1..C13, + ve - ayrı) her biri için var / yok h5 payı (Fisher iki yönlü), KAT5 (var grubu), stop payı; BH q 0,10 (bilgi).
- GÖZ SKORU: son model 26.663 Y1 olayına; beşte bir sınırları 26.663 olayın skor dağılımından; üst beşte bir (B5) vs alt beşte bir (B1); karar hücreleri (ABD 2023, ABD 2024-26, AVR 2023, AVR 2024-26) B5 olayları YAPI_HEDEF karar kuralıyla (yh_hucre: n >= 30, KAT5 eş alt uç > 1, stop önce < eş, plasebo KAT5 alt uç > 1; yh_durum güç tablosu arastirma_cikti/yapi_hedef/guc_tablosu.json, n >= 1.000 ya da güç >= %80 -> DESTEKLENMEDİ, değilse ÖLÇÜLEMEDİ; yh_etiket). B1 ve B5 vs B1 Fisher bilgi. Ana satır bütün olaylar (§6); DIŞ ÖRNEKLEM (300 etiketli olay çıkarılmış) ayrı satır; iki etiket farklıysa muhafazakâr olan yazılır.
- OLASILIK TABLOSU: beşli B1..B5 başına +%5 / +%10 / stop payı, eş payı, KAT5 (%95), takip stoplu getiri medyanı (bilgi); karar pazarları (ABD + AVR, 2023 + 2024-26), aynı dış örneklem, bütün olaylar.
- HAKEM SETİ: iş tanımı §5'teki 8 / 8 / 4 dengesi OLUR 6 ile kurulamaz; ana model kararı: tohum 13, 6 OLUR'un hepsi (3 kör, 3 açık), her yarıda 7 BELİRSİZ + 10 OLMAZ (40 sayfa; 1-20 KÖR, 21-40 AÇIK). hakem_anahtar.json gizli. `python GOZ_ETIKET.py hakem --cevap-dosya` iki yarıyı ayrı raporlar (kör: Cohen kappa + çapraz tablo; açık: doğru / yanlış + kural başına yanlış sayımı).
- VERİ DENETİMİ (bilgi): No 274'teki dev fitil ham veride denetlenir; 300 görselin 120 bar penceresinde High / max(O, C) ya da min(O, C) / Low > 1,5 olan bar sayılır, C13- ile kesişimi yazılır.
- AŞAMA A kapısı (ge_kapi) GE_KOD_SHA'yı denetler; AŞAMA C kodu aynı dosyaya eklendiği için o mühür artık tutmaz. AŞAMA C kapısı ge_kapi_c aşağıdaki mühürleri denetler (GE_ESIK ve A dosyaları değişmedi; etiket.json AŞAMA C'de değiştirilmez).

Mühürler (ölçümden önce):
- GE_C_ESIK_SHA: `f7031494f3f4e08888fb00d9fe72992d4f5a97dc1f0b79566169897cca873295` (GOZ_ETIKET.GE_C_ESIK)
- GE_KOD_SHA_C: `757c3fa204c8de776c77372f07cc64249b44a6a4be5d54717b593b0f5edbf738` (GOZ_ETIKET.py, AŞAMA C kodu dahil)
- TEST_SHA_C: `1077c42accf53a6fae4c5d124dec16f6ac2ac7688e75bd6a60dfa10ceca32cf7` (test_goz_etiket.py; 71 test geçti)
- ETIKET_SHA: `bffcf9a730fe46b350280c6faa2a4bb28c31db41a0d9317f3f581860c7200f23` (etiket.json; git b71e046, 2026-11-17T20:44:22+00:00)
- GE_ESIK_SHA (A, değişmedi): `a48cd64da71616bdd19f05c3d3763997096d520252622812c244516f94a84d5d`
- ZAMAN (UTC): `2026-11-17 20:56:04 UTC`
