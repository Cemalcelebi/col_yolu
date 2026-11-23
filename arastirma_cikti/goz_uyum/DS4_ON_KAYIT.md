# DİP SAVUNMASI v4 (DS4) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: 2026-11-23T18:35:55Z (UTC). Soru: Cemal'in 23.11.2026 tarifi ("Burada kodun yanlışını buldum: en dip noktasında çizgi çekip bir düşeni kırmış mı, ve artık düşmüyor, yukarı daha yukarıdan dönüyorsa VAR.") üç parçalı kurala çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? Ayrıca iki set dışından 24 sayfalık GÖRSEL ONAY (EK, 23 Kas) PDF'i (Cemal'e henüz gönderilmedi). GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds4_anahtar.json` sha256: `0aaa9e9515aaf62996ca33db9a2431367f3f9ddb1b5af9ddf41991214b3ed222`
- kod: `arastirma_cikti/goz_uyum/ds4.py` sha256: `f454520cafa333c5332bbbc33d9aa4c1f8ea1f07863e3a946497441dd9ae210a`
- eşik sözlüğü (DS4_ESIK) sha256: `e8b36572a3ce3e02ce6585ceb5a91a15a9b2ad0c789d616b062d579411da04b0`
- kural kaynağı (ds4_parca_dizi + ds4_parca) sha256: `12edb54e24b47f62b119119ec5b1870849a9c6f45c34f91b73293f2b17d88d6f`
- görsel onay PDF: `arastirma_cikti/goz_uyum/DS4_ONAY.pdf` sha256: `57d377634bff26b56d362fddd82832e41cbe8b10771b66eca99b24f6f2cdc166`
- görsel onay anahtarı: `arastirma_cikti/goz_uyum/ds4_onay_anahtar.json` sha256: `66187af9b125bb2c1a4d8422b5362bec291c4471d47b9a5ffc71d2a806642f15`
- iş tanımı: `arastirma_cikti/goz_uyum/DS4_IS_TANIMI.md` sha256: `1fb3216fc43b762fe07798640362f288a4b81db7520de724b4e34928523bb7f9`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `f6d4b18a7138860aa001d7dfc0a2fb3c57ad2064c1c497a6887171b0a34ad4d7`, tanim2_anahtar.json `c0cc3e82c2895c222393932f7ab217f626444e516cb159ba6696ac888e00e916`
- olay havuzu (görsel onay; pazar, sembol, tarih) sha256: `47afd46429a53cd57272ead2e126217957385d8ea5bda61c737c25092ac1d781` ({"havuz_n": 2849, "iki_set_haric_n": 2695, "havuz_pazar": {"ABD": 2451, "AVR": 221, "BIST": 177}, "iki_set_haric_pazar": {"ABD": 2329, "AVR": 202, "BIST": 164}, "havuz_V1_VAR": {"ABD": 409, "AVR": 38, "BIST": 36}, "havuz_parca": {"P1": 2644, "P2": 1739, "P3i": 2510, "P3ii": 1004, "P3iii": 2104, "P3": 720, "V1": 483, "V2": 713, "V3": 1613}, "VAR_pazar_sayfa": {"ABD": 12, "AVR": 2, "BIST": 2}, "notlar": []})
- bağımlı kod: goz_uyum.py `828258b1f24d45bc`, tanim2.py `61821c517e75728c`, GOZ_ETIKET.py `76d5c76b3a545ed5`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); kural penceresi son 120 mum [t-119 .. t].
- **DİP**: d = [t-119 .. t-5] aralığında en düşük Low'un günü (eşitlikte en son); dip çizgisi = Low(d).
- **P1 DÜŞÜŞTEN DİP**: d'den önceki pencere kısmında en yüksek High / Low(d) - 1 >= 0,20.
- **P2 DÜŞEN TREND KIRILIMI**: d'den önceki pivot tepeler (High, 5 sol / 5 sağ; pivot günü + 5 <= d). H1 = en yüksek pivot tepe; H2 = H1'den sonra, H1'den alçak SON pivot tepe (yoksa H1'den sonraki en yüksek pivot tepe; o da yoksa P2 YOK). Düşen çizgi = H1-H2 doğrusu (eğim < 0 şart). Kırılım = d'den sonra en az bir mumun KAPANIŞI çizginin o gündeki değerinin üstünde.
- **P3 ARTIK DÜŞMÜYOR, DAHA YUKARIDAN DÖNÜYOR**: (i) d'den sonra hiçbir Low < Low(d); (ii) d'den sonra en az bir pivot dip (Low, 3 sol / 3 sağ; pivot günü + 3 <= t) var ve HEPSİ Low(d) + 0,5 x ATR14(d) üstünde; (iii) birden çok pivot dip varsa son pivot dip ilkinden düşük değil.
- **V1 (ANA)** = P1 ∧ P2 ∧ P3; **V2** = P1 ∧ P3 (trend kırılımı yok); **V3** = P1 ∧ P2 ∧ P3(i) (yükselen dip yok). Bonferroni 3.

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
- dip: d = [t-119 .. t-5] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low son 4 mumdaysa (t-4..t) d oraya gidemez; o mum dibi deldiği için P3(i) YANLIŞ olur ('dip çok yeni' = delinme)
- p1: tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20
- pivot_tepe: H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d (pivot yalnız d'ye kadar onaylı tepeler)
- h1: en yüksek pivot tepe; eşit yükseklikte EN ERKEN olan
- h2: H1'den sonra (j > j1), H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki en yüksek pivot tepe (bu durumda eşit yükseklik -> eğim 0 -> P2 YOK); H1'den sonra pivot tepe yoksa P2 YOK
- cizgi: çizgi_i = H1 + eğim x (i - j1), eğim = (H2 - H1) / (j2 - j1); eğim < 0 şart; sağa t'ye kadar uzatılır
- kirilim: d < i <= t için Close_i > çizgi_i olan İLK gün = kırılım mumu; yoksa P2 YANLIŞ
- delinme: P3(i): Low_i >= Low(d) bütün d < i <= t (eşitlik delinme sayılmaz)
- pivot_dip: L_j < min(L_{j-3..j-1}) (sol kesin) ve L_j <= min(L_{j+1..j+3}); d < j, j+3 <= t (t'ye kadar onaylı), j-3 >= t-119
- atr: TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir)
- bant: P3(ii): her pivot dip L_j > Low(d) + 0,5 x ATR14(d) (kesin büyük); pivot dip yoksa P3(ii) YANLIŞ
- yukselen: P3(iii): pivot dip sayısı >= 2 ise L(son) >= L(ilk); 0-1 pivot dipte DOĞRU (P3(ii) zaten pivot dip ister)

DS4_ESIK (tam): `{"atr_n": 14, "bant_atr": 0.5, "belirsizlik": {"atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = max(1, d-13) .. d (121 barlık pencerenin dizini; dizin 0 yalnız önceki kapanış olarak kullanılabilir)", "bant": "P3(ii): her pivot dip L_j > Low(d) + 0,5 x ATR14(d) (kesin büyük); pivot dip yoksa P3(ii) YANLIŞ", "cizgi": "çizgi_i = H1 + eğim x (i - j1), eğim = (H2 - H1) / (j2 - j1); eğim < 0 şart; sağa t'ye kadar uzatılır", "delinme": "P3(i): Low_i >= Low(d) bütün d < i <= t (eşitlik delinme sayılmaz)", "dip": "d = [t-119 .. t-5] aralığında en düşük Low'un günü; eşit en düşük Low birden çok günde ise EN SON gün (float ==). En düşük Low son 4 mumdaysa (t-4..t) d oraya gidemez; o mum dibi deldiği için P3(i) YANLIŞ olur ('dip çok yeni' = delinme)", "h1": "en yüksek pivot tepe; eşit yükseklikte EN ERKEN olan", "h2": "H1'den sonra (j > j1), H1'den KESİN alçak pivot tepelerin EN SONU; yoksa H1'den sonraki en yüksek pivot tepe (bu durumda eşit yükseklik -> eğim 0 -> P2 YOK); H1'den sonra pivot tepe yoksa P2 YOK", "kirilim": "d < i <= t için Close_i > çizgi_i olan İLK gün = kırılım mumu; yoksa P2 YANLIŞ", "p1": "tepe = max High [t-119 .. d-1] (d hariç; d = t-119 ise tepe yok -> P1 YANLIŞ); oran = tepe / Low(d) - 1 >= 0,20", "pivot_dip": "L_j < min(L_{j-3..j-1}) (sol kesin) ve L_j <= min(L_{j+1..j+3}); d < j, j+3 <= t (t'ye kadar onaylı), j-3 >= t-119", "pivot_tepe": "H_j > max(H_{j-5..j-1}) (sol kesin) ve H_j >= max(H_{j+1..j+5}) (sağ eşit olabilir); j-5 >= t-119 ve j+5 <= d (pivot yalnız d'ye kadar onaylı tepeler)", "yukselen": "P3(iii): pivot dip sayısı >= 2 ise L(son) >= L(ilk); 0-1 pivot dipte DOĞRU (P3(ii) zaten pivot dip ister)"}, "dip_sag": 3, "dip_sol": 3, "dip_sonrasi_min": 5, "dusus_min": 0.2, "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek verdi; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33)", "kappa": {"B": 5000, "bonferroni_k": 3, "gecerli": 0.6, "gecerli_alt": 0.4, "guven": 0.95, "karar_min": 30, "kismen": 0.4, "tohum": 20261125}, "kural_bar": 120, "not": "parametreler (0,20; 5/5 tepe; 3/3 dip; 0,5 ATR14; d <= t-5) iş tanımından aynen; etiketlere bakılmadan sabitlendi; GETİRİ YOK", "onay": {"VAR": 16, "VAR_pazar": {"ABD": 12, "AVR": 2, "BIST": 2}, "YOK_P2": 2, "YOK_P3": 2, "YOK_rastgele": 4, "secim": "EK (ana model, 23 Kas): 24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST; iki setteki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261125) karıştırılmış sırada gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık sırada ilk 4 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra P1 ∧ P3 ∧ ¬P2 -> 'P2 düştü' (2); P1 ∧ P2 ∧ ¬P3 -> 'P3 düştü' (2). Sayfa sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı", "tohum": 20261125}, "pencere_bar": 121, "tepe_sag": 5, "tepe_sol": 5, "varyant": {"V1": "P1 ∧ P2 ∧ P3 (ANA)", "V2": "P1 ∧ P3 (trend kırılımı şartı yok)", "V3": "P1 ∧ P2 ∧ P3(i) (yükselen dip şartı yok)"}}`

## 3. Sentetik sınama (`python arastirma_cikti/goz_uyum/ds4.py test`; kör / gerçek veriden ÖNCE; dizinler t'ye göre)
| seri | tarif | beklenen V1 / V2 / V3 | çıkan V1 / V2 / V3 | P1 | P2 | P3(i) | P3(ii) | P3(iii) | d | H1 | H2 | kırılım | dönüş dipleri (ATR) | eşit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | düşüş -> dip -> düşen çizgiyi kıran yükseliş -> dibin üstünde dönen geri çekilme | VAR / VAR / VAR | VAR / VAR / VAR | ✓ | ✓ | ✓ | ✓ | ✓ | t-40 | t-112 | t-54 | t-36 | t-20 (3.89) | EVET |
| S2 | S1 gibi ama geri çekilme dibi deliyor (97 < 100; yeni dip sonrası dönüş dibi yok) | YOK / YOK / VAR | YOK / YOK / VAR | ✓ | ✓ | ✓ | ✗ | ✓ | t-20 | t-112 | t-28 | t-12 | - | EVET |
| S3 | dip ve yükselen dip var ama yavaş düşen çizgi (H1-H2) kırılmamış | YOK / VAR / YOK | YOK / VAR / YOK | ✓ | ✗ | ✓ | ✓ | ✓ | t-40 | t-110 | t-50 | - | t-20 (1.74) | EVET |
| S4 | dip sonrası yatay, dönüş dibi dibe yapışık (< 0,5 ATR) | YOK / YOK / VAR | YOK / YOK / VAR | ✓ | ✓ | ✓ | ✗ | ✓ | t-40 | t-112 | t-54 | t-35 | t-28 (0.25) | EVET |
| S5 | düşüş yok, yatay dalgalı seri | YOK / YOK / YOK | YOK / YOK / YOK | ✗ | ✗ | ✓ | ✗ | ✓ | t-53 | t-73 | - | - | t-16 (0.00) | EVET |
| S6 | dip çok yeni: en düşük Low t-3'te (d t-5'ten sonraya gidemez, o mum dibi deler) | YOK / YOK / YOK | YOK / YOK / YOK | ✓ | ✓ | ✗ | ✗ | ✓ | t-5 | t-112 | t-54 | t-4 | t-3 (-0.77) | EVET |
| S7 | S1 gibi ama son 4 mumda (t-2) dip deliniyor | YOK / YOK / YOK | YOK / YOK / YOK | ✓ | ✓ | ✗ | ✓ | ✓ | t-40 | t-112 | t-54 | t-36 | t-20 (3.89) | EVET |
| S8 | tek düz düşüş (pivot tepe yok -> düşen çizgi kurulamaz), dip sonrası S1 gibi | YOK / VAR / YOK | YOK / VAR / YOK | ✓ | ✗ | ✓ | ✓ | ✓ | t-40 | - | - | - | t-20 (5.05) | EVET |
| S9 | S1 gibi ama ikinci dönüş dibi ilkinden alçak (105 -> 103, ikisi de bandın üstünde) | YOK / YOK / VAR | YOK / YOK / VAR | ✓ | ✓ | ✓ | ✓ | ✗ | t-40 | t-112 | t-54 | t-37 | t-28 (3.27), t-16 (2.04) | EVET |

Ek testler: eşit en düşük Low -> en son gün; prefix değişmezliği (3 kesik, dizi + DataFrame); kısa pencere ve H <= L penceresi reddedilir; hüküm fonksiyonu. Sonuç: 9 / 9 seri beklenene eşit.

## 4. Mühürlü yanıtlar (ds4_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
| küme | n | P1 | P2 | P3(i) | P3(ii) | P3(iii) | P3 | V1 VAR | V2 VAR | V3 VAR |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 40 | 25 | 39 | 16 | 31 | 13 | 9 | 13 | 24 |
| 2 | 40 | 39 | 29 | 36 | 14 | 29 | 11 | 9 | 10 | 28 |
| birlesik | 80 | 79 | 54 | 75 | 30 | 60 | 24 | 18 | 23 | 52 |

## 5. Görsel onay PDF'i (DS4_ONAY.pdf; iki set dışından 24 yeni sayfa; anahtar ds4_onay_anahtar.json)
Seçim: EK (ana model, 23 Kas): 24 sayfa. Havuz = goz_uyum.gu_havuz (Y1 ∧ Ş1, likidite) ABD + AVR + BIST; iki setteki (pazar, sembol) çiftleri hariç; olaylar tohumla (20261125) karıştırılmış sırada gezilir, her (pazar, sembol) en çok 1 sayfa. V1 VAR 16: karışık sıradaki İLK V1 VAR olaylar, pazar hedefi ABD 12 / AVR 2 / BIST 2 (seçme / ayıklama yok); bir pazarda yetmezse eksik, aynı karışık sırada öteki pazarların sıradaki V1 VAR olaylarıyla doldurulur ve yazılır. V1 YOK 8: karışık sırada ilk 4 V1 YOK -> 'rastgele' (nedeni ne olursa); sonra P1 ∧ P3 ∧ ¬P2 -> 'P2 düştü' (2); P1 ∧ P2 ∧ ¬P3 -> 'P3 düştü' (2). Sayfa sırası: önce 16 VAR (karışık sıradaki geliş sırası), sonra 8 YOK (tohumla karıştırılmış); PDF kör değil, onay amaçlı.

| sayfa | grup (seçim) | V1 | P1 | P2 | P3 | düşen parça |
|---|---|---|---|---|---|---|
| 1 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 2 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 3 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 4 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 5 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 6 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 7 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 8 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 9 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 10 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 11 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 12 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 13 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 14 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 15 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 16 | VAR | VAR | ✓ | ✓ | ✓ | - |
| 17 | YOK_rastgele | YOK | ✓ | ✗ | ✓ | P2 |
| 18 | YOK_P2 | YOK | ✓ | ✗ | ✓ | P2 |
| 19 | YOK_rastgele | YOK | ✓ | ✓ | ✗ | P3(iii) |
| 20 | YOK_rastgele | YOK | ✗ | ✗ | ✗ | P1, P2, P3(ii) |
| 21 | YOK_P2 | YOK | ✓ | ✗ | ✓ | P2 |
| 22 | YOK_rastgele | YOK | ✓ | ✓ | ✗ | P3(ii) |
| 23 | YOK_P3 | YOK | ✓ | ✓ | ✗ | P3(iii) |
| 24 | YOK_P3 | YOK | ✓ | ✓ | ✗ | P3(ii) |

## 6. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B 5000, tohum 20261125, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: V1 (ANA): iki set birleşik Cemal kararlarıyla (79 etiket; işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> YARI BAĞIMSIZ GEÇERLİ (Cemal tarifini DS3 görselindeki 6 set-1 sayfasını görerek verdi; kesin hüküm yalnız Cemal'in görsel onayı + üçüncü bağımsız kör setle); kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33).
- Ek bilgi (hüküm dışı): uyuşmayan sayfalar ve düşen parça (P1 / P2 / P3(i) / P3(ii) / P3(iii)); Cemal VAR / kod YOK sayfalarda düşen parça sayımı; GOVDE_1 (önceki birleşik kappa 0,35) ve DS3 V1 (-0,15) ile aynı sayfalarda karşılaştırma.
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 7. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa) |
| K2 | geleceğe bakma | EVET | P1 / P2 / P3 yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds4_pencere mekanik denetimi (W.index.max() <= t, W.index[-1] == t, 121 bar); pivot tepe j+5 <= d, pivot dip j+3 <= t (yalnız t'ye kadar onaylı); ds4.py test prefix değişmezliği (3 kesik + DataFrame); getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri mühürden önce açılmadı (olc açılış zamanı DS4_SONUC'ta) |
| K3 | geçerli bar | EVET | GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds4_parca_dizi NaN / H <= L / L <= 0 görürse durur (testte sınandı) |
| K4 | tekilleştirme | EVET | 80 sayfa set 1 (goz_uyum_anahtar) + set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa; görsel onay 24 sayfası iki setin (pazar, sembol) çiftleri hariç, her çift en çok 1 sayfa |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı birimsiz, bant ve dönüş dibi uzaklığı ATR14(d) birimi; fiyat birimi kuralı etkilemez |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok |
| K8 | örneklem ve dönem | EVET | 79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; hüküm yalnız V1 ve 'YARI BAĞIMSIZ' (Cemal tarifi DS3 görselindeki 6 set-1 sayfasını görerek verdi); set 1 ve set 2 ayrı; kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi) |
| K9 | ön kayıt | EVET | kural + DS4_ESIK + sentetik test ADIM 1'de etiketler açılmadan commit; 80 yanıt ds4_anahtar.json + görsel onay (DS4_ONAY.pdf, ds4_onay_anahtar.json) etiket açılmadan mühürlü; ds4.py + ds4_anahtar.json + DS4_ESIK + kural kaynağı + PDF + onay anahtarı sha'ları bu dosyada; olc sha'ları denetler ve 80 yanıtı veriden yeniden hesaplayıp mühürle karşılaştırır; hüküm eşikleri sabit |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | ds4.py anahtar / onay aynı komutla deterministik yeniden üretilir (tohum 20261125); olc 80 sayfanın yanıtını veriden yeniden hesaplar, mühürlü yanıtla eşitliğini şart koşar; sentetik seriler beklenen yanıtla birebir (9 / 9) |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için; 'YARI BAĞIMSIZ' sınırı yazılı |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_DS4 + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi (git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok; PDF Cemal'e gönderilmedi |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 8. Git kaydı (bu dosyanın yazıldığı an)
- ds4.py: f348cfefb75f99e1079fb70b99d84a8cc06583bd 2026-11-23T18:27:38+00:00
- DS4_IS_TANIMI.md: f348cfefb75f99e1079fb70b99d84a8cc06583bd 2026-11-23T18:27:38+00:00

## 9. Not (etiketler açılmadan yazıldı)
- ds4.py ADIM 1 commit'i (f348cfe) ile bu mühür arasında yalnız gösterim kodu değişti: görsel onay kapağında açıklama metninin yeri (üst üste binme düzeltildi) ve `olc --deneme` başlığının 'mühür denetimi YAPILMADI' demesi. Kural kaynağı sha'sı (12edb54e...) ve DS4_ESIK sha'sı (e8b36572...) ADIM 1 commit'indekiyle aynı.
- Görsel onay olay havuzu `goz_uyum.gu_havuz` ile bu oturumda hesaplandı (ABD 2.451 / AVR 221 / BIST 177 olay; ABD 638 sn) ve hız için scratchpad önbelleğinden (`ds4.py onay --havuz_onbellek`) okundu; havuzun (pazar, sembol, tarih) sha'sı yukarıda; önbelleksiz `ds4.py onay` aynı havuzu yeniden üretir.
- `olc` kod yolu mühürden önce yalnız UYDURMA (rastgele) etiketle, scratchpad dizininde (`--deneme`) sınandı; gerçek etiket dosyaları açılmadı.
- Etiketler açılmadan gözlem (yalnız kodun kendi yanıtı): 80 sayfada V1 VAR 18 (set 1: 9, set 2: 9); en kısıtlayıcı parça P3(ii) 'dönüş dipleri dibin yarım ATR üstünde' (80 sayfanın 30'unda DOĞRU). Görsel onayda gözlem: H2 = dibe en yakın alçak tepe olduğu için düşen çizgi çoğu sayfada dik ve dibe yakın; kırılım çoğunlukla dipten birkaç mum sonra geliyor (kural iş tanımındaki gibi bırakıldı; Cemal'in görsel onayı bunu sınar).
- DS4_ONAY.pdf Cemal'e GÖNDERİLMEDİ (ana model karar verir).
