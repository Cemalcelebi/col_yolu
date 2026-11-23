# DİP SAVUNMASI v5 (DS5) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: 2026-11-23T18:58:58Z (UTC). Soru: Cemal'in 23.11.2026 tarifi ("... dip savunması en derinden yukarı veya yatay bir çizgi takip eden mumları takip ederek var / yok demeli." + EK: "... bu yukarıdan sayılan mumların bir düşeni kırıyor olması gerekir; yani basit bir tepki içindeki dizilmiş mumlara dip savunması var demesin kod.") gövde altı destek çizgisi + düşen çizgi kırılımı kuralına çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca iki set ve DS4 onay seti dışından 24 sayfalık GÖRSEL ONAY PDF'i (Cemal'e henüz gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds5_anahtar.json` sha256: `97789ae147de8529e74d687847def5084f509db2f1a6f7175d8e420a30544908`
- kod: `arastirma_cikti/goz_uyum/ds5.py` sha256: `151de815229f071fafa20cb3639c99877d3f5a7e6b13017621b00ff099f422f4`
- eşik sözlüğü (DS5_ESIK) sha256: `0f02689ffc9f89d42cee4da925ed90a14984f33803f8dc8997f64de8c87723fd`
- kural kaynağı (_ds5_cizgi + ds5_parca_dizi + ds5_parca) sha256: `0ff9d59595ca2709eceeafe8fa775e14f66bcfcf96028f9929cdfda493a526c0`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS5_ONAY.pdf` sha256: `ab7ff1a247f03b90fd505c522caff79b3d1dfe4327978f72b603693466026fa3`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds5_onay_anahtar.json` sha256: `92ac3e7406d367d52a8b11c83abfcd97b1142f50188220ef1a0bc19edfd569a0`
- iş tanımı: `arastirma_cikti/goz_uyum/DS5_IS_TANIMI.md` sha256: `084639360ccc7d2e4cc6323ede5ec7fc357d20638d4f2815b553aff0e2790b54`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `f6d4b18a7138860aa001d7dfc0a2fb3c57ad2064c1c497a6887171b0a34ad4d7`, tanim2_anahtar.json `c0cc3e82c2895c222393932f7ab217f626444e516cb159ba6696ac888e00e916`; DS4 onay seti dışlaması için ds4_onay_anahtar.json `66187af9b125bb2c1a4d8422b5362bec291c4471d47b9a5ffc71d2a806642f15`
- olay havuzu (görsel onay; pazar, sembol, tarih) sha256: `47afd46429a53cd57272ead2e126217957385d8ea5bda61c737c25092ac1d781` (DS4 görsel onay havuzuyla aynı) ({"havuz_n": 2849, "haric_n": 2643, "havuz_pazar": {"ABD": 2451, "AVR": 221, "BIST": 177}, "haric_pazar": {"ABD": 2291, "AVR": 193, "BIST": 159}, "haric_V1_VAR": {"ABD": 359, "AVR": 30, "BIST": 32}, "haric_parca": {"P1": 2589, "P2": 1539, "P3": 1197, "P4": 2419, "P5": 897, "fitil_kucuk": 1944, "V1": 421, "V2": 311, "V3": 898}, "VAR_pazar_sayfa": {"ABD": 12, "AVR": 2, "BIST": 2}, "notlar": []})
- bağımlı kod: goz_uyum.py `828258b1f24d45bc`, tanim2.py `61821c517e75728c`, GOZ_ETIKET.py `76d5c76b3a545ed5`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); kural penceresi son 120 mum [t-119 .. t]. B_i = min(Open_i, Close_i) (gövde altı); ATR = ATR14(d).
- **DİP**: d = [t-119 .. t-8] aralığında en düşük Low'un günü (eşitlikte en son); m = t - d (>= 8, bilgi için kaydedilir).
- **P1 DÜŞÜŞTEN DİP**: d'den önceki pencere kısmında en yüksek High / Low(d) - 1 >= 0,20.
- **ÇİZGİ**: çapa (d, B_d); s* = min over i = d+1 .. t of (B_i - B_d) / (i - d) (çapadan geçen, sonraki bütün gövde altlarının altında kalan en dik doğru); L(i) = B_d + s* (i - d).
- **P2 YATAY YA DA YUKARI**: s* >= -0,05 x ATR / 20.
- **P3 TAKİP**: dokunuş = dipten sonraki mum, B_i - L(i) < 0,35 x ATR; en az 3 dokunuş VE dipten sonraki sürenin ilk yarısında en az 1 VE ikinci yarısında en az 1.
- **P4 DİP KORUNUR**: dipten sonra hiçbir Low < Low(d) - 0,25 x ATR.
- **P5 DİZİ DÜŞEN ÇİZGİYİ KIRIYOR** (EK, 23 Kas): düşen çizgi DS4 tanımıyla (d'den önceki pivot tepeler 5/5, pivot günü + 5 <= d; H1 = en yüksek pivot tepe; H2 = H1'den sonra, H1'den alçak SON pivot tepe; yoksa H1'den sonraki en yüksek; eğim < 0 değilse P5 YOK); dipten sonra KAPANIŞI düşen çizginin üstünde en az 3 mum VE son mumun (t) kapanışı çizginin üstünde VE P3 dokunuşlarından en az biri ilk kırılım gününden SONRA.
- **V1 (ANA)** = P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5; **V2** = V1 ∧ (dip sonrası ortalama alt fitil (B_i - Low_i) dipten önceki 20 mumunkinden küçük); **V3** = P1 ∧ P2 ∧ P3 ∧ P4 (V1 ama P5 yok; basit tepki dahil). Bonferroni 3.

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
- dip: d = [t-119 .. t-8] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low son 7 mumdaysa (t-7..t) d oraya gidemez; o mum dibi 0,25 ATR'den fazla deliyorsa P4 YANLIŞ olur. Bu tanım gereği d+1 .. t-8 arasında Low(d)'den düşük Low yoktur; P4 yalnız son 7 mumda bağlayıcıdır
- p1: tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20
- govde: B_i = min(Open_i, Close_i) (gövde altı; doji'de Open = Close)
- cizgi: çapa (d, B_d); s* = min (B_i - B_d) / (i - d), i = d+1 .. t (tanım gereği bütün dip sonrası gövde altları çizginin üstünde ya da üzerinde; en az bir mum çizginin ÜZERİNDE = mesafe 0); L(i) = B_d + s* (i - d), sağa t'ye kadar
- atr: TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir) (DS4 ile aynı)
- p2: s* >= -0,05 x ATR14(d) / 20 (eşitlik geçer)
- dokunus: d < i <= t ve B_i - L(i) < 0,35 x ATR14(d) (kesin küçük); k = i - d; ilk yarı k <= m / 2, ikinci yarı k > m / 2 (m tek ise orta mum ikinci yarıdadır, ör. m = 9: ilk yarı k 1..4, ikinci yarı k 5..9)
- p3: dokunuş sayısı >= 3 VE ilk yarıda >= 1 VE ikinci yarıda >= 1
- p4: d < i <= t için Low_i >= Low(d) - 0,25 x ATR14(d) (eşitlik geçer)
- v2: alt fitil_i = B_i - Low_i; ortalama (i = d+1 .. t) < ortalama (i = max(t-119, d-20) .. d-1) (kesin küçük; dip mumu ikisine de girmez; dipten önce mum yoksa V2 YANLIŞ); V2 = V1 ∧ bu şart
- pivot_tepe: H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d (DS4 ile aynı)
- h1_h2: H1 = en yüksek pivot tepe (eşitte EN ERKEN); H2 = H1'den sonra, H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki en yüksek pivot tepe (eşit -> eğim 0 -> P5 YOK); H1'den sonra pivot tepe yoksa ya da pivot tepe yoksa P5 YOK (DS4 ile aynı)
- p5: düşen çizgi_i = H1 + eğim (i - j1), eğim < 0 şart; d < i <= t kapanışları: Close_i > çizgi_i olan mum sayısı >= 3 VE Close_t > çizgi_t VE kırılım günü kb = ilk Close_i > çizgi_i (d < i) olmak üzere en az bir P3 dokunuşu j > kb (kesin sonra)
- v3: V3 = P1 ∧ P2 ∧ P3 ∧ P4 (V1'den P5 çıkarılmış; basit tepki dahil) (EK, 23 Kas: DS3 tipi Low çizgisi yerine)

DS5_ESIK (tam): `{"atr_n": 14, "belirsizlik": {"atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir) (DS4 ile aynı)", "cizgi": "çapa (d, B_d); s* = min (B_i - B_d) / (i - d), i = d+1 .. t (tanım gereği bütün dip sonrası gövde altları çizginin üstünde ya da üzerinde; en az bir mum çizginin ÜZERİNDE = mesafe 0); L(i) = B_d + s* (i - d), sağa t'ye kadar", "dip": "d = [t-119 .. t-8] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low son 7 mumdaysa (t-7..t) d oraya gidemez; o mum dibi 0,25 ATR'den fazla deliyorsa P4 YANLIŞ olur. Bu tanım gereği d+1 .. t-8 arasında Low(d)'den düşük Low yoktur; P4 yalnız son 7 mumda bağlayıcıdır", "dokunus": "d < i <= t ve B_i - L(i) < 0,35 x ATR14(d) (kesin küçük); k = i - d; ilk yarı k <= m / 2, ikinci yarı k > m / 2 (m tek ise orta mum ikinci yarıdadır, ör. m = 9: ilk yarı k 1..4, ikinci yarı k 5..9)", "govde": "B_i = min(Open_i, Close_i) (gövde altı; doji'de Open = Close)", "h1_h2": "H1 = en yüksek pivot tepe (eşitte EN ERKEN); H2 = H1'den sonra, H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki en yüksek pivot tepe (eşit -> eğim 0 -> P5 YOK); H1'den sonra pivot tepe yoksa ya da pivot tepe yoksa P5 YOK (DS4 ile aynı)", "p1": "tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20", "p2": "s* >= -0,05 x ATR14(d) / 20 (eşitlik geçer)", "p3": "dokunuş sayısı >= 3 VE ilk yarıda >= 1 VE ikinci yarıda >= 1", "p4": "d < i <= t için Low_i >= Low(d) - 0,25 x ATR14(d) (eşitlik geçer)", "p5": "düşen çizgi_i = H1 + eğim (i - j1), eğim < 0 şart; d < i <= t kapanışları: Close_i > çizgi_i olan mum sayısı >= 3 VE Close_t > çizgi_t VE kırılım günü kb = ilk Close_i > çizgi_i (d < i) olmak üzere en az bir P3 dokunuşu j > kb (kesin sonra)", "pivot_tepe": "H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d (DS4 ile aynı)", "v2": "alt fitil_i = B_i - Low_i; ortalama (i = d+1 .. t) < ortalama (i = max(t-119, d-20) .. d-1) (kesin küçük; dip mumu ikisine de girmez; dipten önce mum yoksa V2 YANLIŞ); V2 = V1 ∧ bu şart", "v3": "V3 = P1 ∧ P2 ∧ P3 ∧ P4 (V1'den P5 çıkarılmış; basit tepki dahil) (EK, 23 Kas: DS3 tipi Low çizgisi yerine)"}, "delinme_atr": 0.25, "dip_sonrasi_min": 8, "dokunus_atr": 0.35, "dokunus_min": 3, "dusus_min": 0.2, "egim_atr": 0.05, "egim_bar": 20, "fitil_once_bar": 20, "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS4 görselini görerek verdi; set 1 / set 2 sayfaları daha önce DS3 / DS4 çalışmalarında kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)", "kappa": {"B": 5000, "bonferroni_k": 3, "gecerli": 0.6, "gecerli_alt": 0.4, "guven": 0.95, "karar_min": 30, "kismen": 0.4, "tohum": 20261126}, "kirilim_kapanis_min": 3, "kural_bar": 120, "not": "parametreler (0,20; d <= t-8; 0,05 ATR / 20 mum; 0,35 ATR; 3 dokunuş + iki yarı; 0,25 ATR; P5: 5/5 pivot tepe, 3 kapanış) iş tanımından ve EK'ten aynen; etiketlere bakılmadan sabitlendi; GETİRİ YOK", "onay": {"VAR": 16, "VAR_pazar": {"ABD": 12, "AVR": 2, "BIST": 2}, "YOK_P2": 2, "YOK_P3": 2, "YOK_P5": 2, "YOK_rastgele": 2, "secim": "24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST (DS4 görsel onayıyla aynı havuz; sha denetlenir); iki kör setteki VE DS4 görsel onay setindeki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261126) karıştırılmış sırada gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık sırada ilk 2 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra P1 ∧ P2 ∧ P4 ∧ P5 ∧ ¬P3 -> 'P3 düştü: tek mum / takip yok' (2); P1 ∧ P3 ∧ P4 ∧ P5 ∧ ¬P2 -> 'P2 düştü: çizgi alçalan' (2); P1 ∧ P2 ∧ P3 ∧ P4 ∧ ¬P5 -> 'P5 düştü: basit tepki' (2) (EK, 23 Kas: iş tanımındaki 4 rastgeleden 2'si P5'e verildi). Sayfa sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı", "tohum": 20261126}, "pencere_bar": 121, "tepe_sag": 5, "tepe_sol": 5, "varyant": {"V1": "P1 ∧ P2 ∧ P3 ∧ P4 ∧ P5 (ANA; gövde altı çizgisi + düşen çizgi kırılımı)", "V2": "V1 ∧ dip sonrası alt fitil dipten önceki 20 mumdan küçük", "V3": "P1 ∧ P2 ∧ P3 ∧ P4 (V1 ama P5 yok; basit tepki dahil)"}}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds5.py test`; gerçek veriden ÖNCE; dizinler t'ye göre)
| seri | tarif | beklenen V1 (düşen) | çıkan V1 / V2 / V3 | P1 | P2 | P3 | P4 | P5 | d | çizgi eğimi (ATR / 20 mum) | dokunuş (ilk / ikinci yarı) | dip sonrası en düşük Low (ATR) | H1 / H2 / kırılım | düşen çizgi üstü kapanış (son mum üstte) | eşit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | düşüş -> dip -> gövde altları yükselen çizgiye 4 kez değen 15 mumluk tırmanış; düşen çizgiyi kırıyor | VAR; V2 VAR, V3 VAR | VAR / VAR / VAR | ✓ | ✓ | ✓ | ✓ | ✓ | t-15 | +5.07 | 4 (2 / 2) | +1.02 | t-110 / t-34 / t-11 | 12 (evet) | EVET |
| S2 | düşüş -> dip -> yatay gövde tabanı, 4 dokunuş (12 mum); düşen çizgiyi kırıyor | VAR; V3 VAR | VAR / VAR / VAR | ✓ | ✓ | ✓ | ✓ | ✓ | t-12 | +0.06 | 4 (2 / 2) | +0.25 | t-110 / t-31 / t-5 | 5 (evet) | EVET |
| S3 | dipten sonra TEK büyük mumla sıçrama, sonra dokunuşsuz yukarıda gezinme (tek dokunuş kırılım mumunun kendisi -> P5 de düşer: kırılımdan sonra dokunuş yok) | YOK (P3, P5) | YOK / YOK / YOK | ✓ | ✓ | ✗ | ✓ | ✗ | t-12 | +1.00 | 1 (1 / 0) | +0.30 | t-110 / t-31 / t-11 | 12 (evet) | EVET |
| S4 | dipten sonra gövde altları alçalıyor (0,12 ATR / mum; dip delinmiyor) | YOK (P2) | YOK / YOK / YOK | ✓ | ✗ | ✓ | ✓ | ✓ | t-12 | -2.40 | 12 (6 / 6) | +0.27 | t-110 / t-31 / t-7 | 8 (evet) | EVET |
| S5 | S2 gibi ama dip sonrası (t-5, t-2) iki mumun fitili dibi ~0,55 ATR deliyor | YOK (P4) | YOK / YOK / YOK | ✓ | ✓ | ✓ | ✗ | ✓ | t-12 | +0.06 | 4 (2 / 2) | -0.55 | t-110 / t-31 / t-5 | 5 (evet) | EVET |
| S6 | düşüş yok (112 -> 100 hafif eğimli dalgalı seri, < %20), dip sonrası 0,5 ATR / mum tırmanış, 4 dokunuş | YOK (P1) | YOK / YOK / YOK | ✗ | ✓ | ✓ | ✓ | ✓ | t-15 | +10.07 | 4 (2 / 2) | +1.60 | t-97 / t-22 / t-11 | 12 (evet) | EVET |
| S7 | dokunuşlar yalnız dipten hemen sonraki 3 mumda, sonra çizgiden uzaklaşma (15 mum; dokunuşlar kırılımdan önce -> P5 de düşer) | YOK (P3, P5) | YOK / YOK / YOK | ✓ | ✓ | ✗ | ✓ | ✗ | t-15 | +0.40 | 3 (3 / 0) | +0.29 | t-110 / t-34 / t-11 | 12 (evet) | EVET |
| S8 | basit tepki: sert çöküş sonrası dip; gövde altları yükselen çizgiye 4 dokunuş ama bütün kapanışlar düşen çizginin altında | YOK (P5); V3 VAR | YOK / YOK / VAR | ✓ | ✓ | ✓ | ✓ | ✗ | t-12 | +2.47 | 4 (2 / 2) | +0.49 | t-110 / t-31 / - | 0 (hayır) | EVET |
| S9 | tek mum düşen çizgiyi kırıyor (t-6), sonraki mumlar yatay tabana, çizginin altına dönüyor | YOK (P5); V3 VAR | YOK / YOK / VAR | ✓ | ✓ | ✓ | ✓ | ✗ | t-12 | +0.06 | 5 (3 / 2) | +0.24 | t-110 / t-31 / t-6 | 1 (hayır) | EVET |
| S10 | en düşük Low t-3'te (dibi ~2 ATR deliyor; d t-8'den sonraya gidemez) | YOK (P4) | YOK / YOK / YOK | ✓ | ✓ | ✓ | ✗ | ✓ | t-12 | +0.06 | 4 (2 / 2) | -2.00 | t-110 / t-31 / t-5 | 5 (evet) | EVET |
| S11 | S2 gibi (V1 VAR) ama dip sonrası alt fitiller uzun (V2 YOK) | VAR; V2 YOK | VAR / YOK / VAR | ✓ | ✓ | ✓ | ✓ | ✓ | t-12 | +0.06 | 4 (2 / 2) | +0.05 | t-110 / t-31 / t-5 | 5 (evet) | EVET |
| S12 | gövde altları hep yukarıda, çizgiye yalnız son mumlar değiyor (ilk yarıda dokunuş yok) | YOK (P3) | YOK / YOK / YOK | ✓ | ✓ | ✗ | ✓ | ✓ | t-12 | +6.00 | 1 (0 / 1) | +1.70 | t-110 / t-31 / t-9 | 10 (evet) | EVET |

Ek testler: eşit en düşük Low -> en son gün; prefix değişmezliği (3 kesik, dizi + DataFrame); tanım değişmezi (hiçbir dip sonrası gövde altı çizginin altında değil, en az biri üzerinde; bütün sentetik serilerde); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: 12 / 12 seri beklenene (V1 ve düşen parça kümesi) eşit.

## 4. Mühürlü yanıtlar (ds5_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
| küme | n | P1 | P2 | P3 | P4 | P5 | fitil küçük | V1 VAR | V2 VAR | V3 VAR |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 40 | 25 | 21 | 36 | 13 | 28 | 8 | 6 | 16 |
| 2 | 40 | 39 | 27 | 24 | 35 | 19 | 32 | 12 | 8 | 20 |
| birlesik | 80 | 79 | 52 | 45 | 71 | 32 | 60 | 20 | 14 | 36 |

## 5. Görsel onay PDF'i (DS5_ONAY.pdf; iki set + DS4 onay seti dışından 24 yeni sayfa; anahtar ds5_onay_anahtar.json)
Seçim: 24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST (DS4 görsel onayıyla aynı havuz; sha denetlenir); iki kör setteki VE DS4 görsel onay setindeki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261126) karıştırılmış sırada gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık sırada ilk 2 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra P1 ∧ P2 ∧ P4 ∧ P5 ∧ ¬P3 -> 'P3 düştü: tek mum / takip yok' (2); P1 ∧ P3 ∧ P4 ∧ P5 ∧ ¬P2 -> 'P2 düştü: çizgi alçalan' (2); P1 ∧ P2 ∧ P3 ∧ P4 ∧ ¬P5 -> 'P5 düştü: basit tepki' (2) (EK, 23 Kas: iş tanımındaki 4 rastgeleden 2'si P5'e verildi). Sayfa sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı.

| sayfa | pazar | grup (seçim) | V1 | P1 | P2 | P3 (dokunuş: ilk / ikinci) | P4 | P5 (üst kapanış) | düşen parça |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ABD | VAR | VAR | ✓ | ✓ | ✓ (3: 1 / 2) | ✓ | ✓ (15) | - |
| 2 | ABD | VAR | VAR | ✓ | ✓ | ✓ (6: 4 / 2) | ✓ | ✓ (10) | - |
| 3 | ABD | VAR | VAR | ✓ | ✓ | ✓ (5: 4 / 1) | ✓ | ✓ (18) | - |
| 4 | ABD | VAR | VAR | ✓ | ✓ | ✓ (3: 2 / 1) | ✓ | ✓ (6) | - |
| 5 | ABD | VAR | VAR | ✓ | ✓ | ✓ (5: 1 / 4) | ✓ | ✓ (18) | - |
| 6 | ABD | VAR | VAR | ✓ | ✓ | ✓ (6: 2 / 4) | ✓ | ✓ (9) | - |
| 7 | ABD | VAR | VAR | ✓ | ✓ | ✓ (11: 6 / 5) | ✓ | ✓ (24) | - |
| 8 | ABD | VAR | VAR | ✓ | ✓ | ✓ (4: 3 / 1) | ✓ | ✓ (5) | - |
| 9 | ABD | VAR | VAR | ✓ | ✓ | ✓ (8: 4 / 4) | ✓ | ✓ (16) | - |
| 10 | ABD | VAR | VAR | ✓ | ✓ | ✓ (5: 2 / 3) | ✓ | ✓ (11) | - |
| 11 | ABD | VAR | VAR | ✓ | ✓ | ✓ (12: 5 / 7) | ✓ | ✓ (19) | - |
| 12 | ABD | VAR | VAR | ✓ | ✓ | ✓ (4: 1 / 3) | ✓ | ✓ (11) | - |
| 13 | AVR | VAR | VAR | ✓ | ✓ | ✓ (6: 1 / 5) | ✓ | ✓ (20) | - |
| 14 | BIST | VAR | VAR | ✓ | ✓ | ✓ (7: 1 / 6) | ✓ | ✓ (5) | - |
| 15 | BIST | VAR | VAR | ✓ | ✓ | ✓ (12: 2 / 10) | ✓ | ✓ (14) | - |
| 16 | AVR | VAR | VAR | ✓ | ✓ | ✓ (7: 5 / 2) | ✓ | ✓ (21) | - |
| 17 | AVR | YOK_P2 | YOK | ✓ | ✗ | ✓ (9: 2 / 7) | ✓ | ✓ (20) | P2 |
| 18 | AVR | YOK_P5 | YOK | ✓ | ✓ | ✓ (5: 3 / 2) | ✓ | ✗ (2) | P5 |
| 19 | ABD | YOK_P3 | YOK | ✓ | ✓ | ✗ (4: 0 / 4) | ✓ | ✓ (29) | P3 |
| 20 | ABD | YOK_P3 | YOK | ✓ | ✓ | ✗ (3: 0 / 3) | ✓ | ✓ (19) | P3 |
| 21 | ABD | YOK_rastgele | YOK | ✓ | ✗ | ✗ (1: 1 / 0) | ✓ | ✗ (34) | P2, P3, P5 |
| 22 | ABD | YOK_rastgele | YOK | ✓ | ✗ | ✓ (10: 1 / 9) | ✓ | ✗ (0) | P2, P5 |
| 23 | AVR | YOK_P2 | YOK | ✓ | ✗ | ✓ (5: 4 / 1) | ✓ | ✓ (27) | P2 |
| 24 | ABD | YOK_P5 | YOK | ✓ | ✓ | ✓ (6: 3 / 3) | ✓ | ✗ (2) | P5 |

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B 5000, tohum 20261126, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS4 görselini görerek verdi; set 1 / set 2 sayfaları daha önce DS3 / DS4 çalışmalarında kullanıldı; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3 / P4 / P5); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; GOVDE_1 (önceki birleşik kappa 0,35), DS4 V1 (0,13) ve DS3 V1 (-0,15) ile aynı sayfalarda karşılaştırma.
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa) |
| K2 | geleceğe bakma | EVET | P1-P5 yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds5_pencere mekanik denetimi (W.index.max() <= t, W.index[-1] == t, 121 bar); çizgi ve dokunuşlar yalnız d+1 .. t; pivot tepe j+5 <= d; ds5.py test prefix değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri ve önceki sonuç dosyaları mühürden önce açılmadı (olc açılış zamanı DS5_SONUC'ta) |
| K3 | geçerli bar | EVET | GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds5_parca_dizi NaN / H <= L / L <= 0 görürse durur (testte sınandı) |
| K4 | tekilleştirme | EVET | 80 sayfa set 1 (goz_uyum_anahtar) + set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa; görsel onay 24 sayfası iki setin VE DS4 görsel onay setinin (pazar, sembol) çiftleri hariç, her çift en çok 1 sayfa |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, eğim / dokunuş / delinme ATR14(d) biriminde; fiyat birimi kuralı etkilemez |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok |
| K8 | örneklem ve dönem | EVET | 79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (Cemal tarifi DS4 görselini görerek verdi; iki set önceki DS3 / DS4 işlerinde kullanıldı); set 1 ve set 2 ayrı; kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi); kesin hüküm üçüncü bağımsız kör setle |
| K9 | ön kayıt | EVET | kural + DS5_ESIK + sentetik test ADIM 1'de etiketler açılmadan commit; 80 yanıt ds5_anahtar.json + görsel onay (DS5_ONAY.pdf, ds5_onay_anahtar.json) etiket açılmadan mühürlü; ds5.py + ds5_anahtar.json + DS5_ESIK + kural kaynağı + PDF + onay anahtarı sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle karşılaştırır; hüküm eşikleri sabit |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | ds5.py anahtar / onay aynı komutla deterministik yeniden üretilir (tohum 20261126; havuz sha DS4 havuzuyla eşit şartı); olc 80 sayfanın yanıtını veriden yeniden hesaplar, mühürlü yanıtla eşitliğini şart koşar; sentetik seriler beklenen yanıt ve düşen parçayla birebir |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_DS5 + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi (git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e gönderilmedi |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds5.py: c56fadcf3d3bc4975e94ea54ebce9c5d9eb17b8b 2026-11-23T18:57:53+00:00
- DS5_IS_TANIMI.md: c56fadcf3d3bc4975e94ea54ebce9c5d9eb17b8b 2026-11-23T18:57:53+00:00

## 9. Not (etiketler ve önceki sonuç dosyaları açılmadan yazıldı)
- EK (ana model, 23 Kas: P5 düşen çizgi kırılımı; V3 = V1 ama P5 yok; YOK sayfalarından 2'si P5) ADIM 1 commit'inden (c56fadc) ÖNCE koda ve iş tanımına girdi; tek ADIM 1 commit'i var.
- ADIM 1 commit'i ile bu mühür arasında ds5.py'de yalnız gösterim değişti: görsel onay kapağında açıklama bloğunun yeri (kapak metniyle üst üste biniyordu; 0,47 -> 0,41). Kural kaynağı sha'sı (0ff9d595...) ve DS5_ESIK sha'sı (0f02689f...) ADIM 1 commit'indekiyle aynı.
- Sentetik serilerin tasarımı ADIM 1 commit'inden önce iki kez düzeltildi (kural değişmedi): (1) dipten önceki düşüş başta dalgasız doğrusaldı, pivot tepe yoktu -> P5 hiçbir seride kurulamadı; dört tepeli zikzak düşüşe çevrildi (DS4 _DUSUS gibi). (2) S6 (düşüş yok) dip sonrası yatay tabanla kurulmuştu; düşen çizgi kırılmadığı için P5 de düşüyordu; dip sonrası 0,5 ATR / mum tırmanışla yeniden kuruldu (yalnız P1 düşsün diye). S3 ve S7'de P5'in de düşmesi tanım gereğidir (tek dokunuş kırılım mumunun kendisi / dokunuşlar kırılımdan önce) ve beklenen kümeye ilk koşudan ÖNCE yazıldı.
- Görsel onay olay havuzu DS4'ün bu oturumda hesapladığı `goz_uyum.gu_havuz` önbelleğinden (scratchpad havuz.pkl) okundu; ds5_havuz okunan havuzun sha'sının ds4_onay_anahtar.json'daki havuz sha'sına (47afd464...) eşit olmasını şart koşar (eşit çıktı).
- `olc` kod yolu mühürden önce yalnız UYDURMA (rastgele) etiketle, scratchpad dizininde (`--deneme`) sınandı; gerçek etiket dosyaları ve *SONUC* / *sonuc* dosyaları açılmadı.
- Etiketler açılmadan gözlem (yalnız kodun kendi yanıtı): 80 sayfada V1 VAR 20 (set 1: 8, set 2: 12); V3 (P5 yok) VAR 36; en kısıtlayıcı parça P5 (80 sayfanın 32'sinde DOĞRU), sonra P3 (45). Havuzda (iki set + DS4 onay dışı, 2.643 olay) V1 VAR: ABD 359 / 2.291, AVR 30 / 193, BIST 32 / 159.
- DS5_ONAY.pdf Cemal'e GÖNDERİLMEDİ (ana model karar verir).
