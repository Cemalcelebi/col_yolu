# DİP SAVUNMASI v3 (DS3) — ÖN KAYIT (Cemal'in işaretleri AÇILMADAN mühürlenir)

Üretim: 2026-11-23T18:09:29Z (UTC). Soru: Cemal'in 23.11.2026 cümlesi ("Çok kolay: eğer bir enstrüman düşüyor ve son bir dipten sonra mumlar bir hat boyunca daha yukarıda kalıp aşağıda fitil boyu küçülüyor ise bu dip savunması.") doğrudan, etiketlerden SEÇİLMEDEN kurala çevrilince, iki kör sette (GOZ_UYUM_KOR.pdf = set 1, TANIM2_KOR.pdf = set 2; 80 sayfa) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/ds3_anahtar.json` sha256: `132c992694615f5d22bf75013c5e2946c55648cc11f8d00989b7a4d370f28c0f`
- kod: `arastirma_cikti/goz_uyum/ds3.py` sha256: `21e64d495b8a1aa9effa54dcffc4e0ce52cc5a138109a9a345408ae3ecf81d29`
- eşik sözlüğü (DS3_ESIK) sha256: `390720bdfcbd6f08b7c80bb989d3dcaba4fdecb15c6ea542ca2d0898aac78e8e`
- kural kaynağı (ds3_parca_dizi + ds3_parca) sha256: `c10dcfa1f5eee4141a8c1495aa137fef2fbe5930837d1d420077a075ee247abc`
- iş tanımı: `arastirma_cikti/goz_uyum/DS3_IS_TANIMI.md` sha256: `369de2407a30fee5edea2a97d9dce104230782783fc022a7cef8af274be4fcf1`
- girdi (yalnız sayfa -> pazar, sembol, sinyal günü okundu): goz_uyum_anahtar.json `f6d4b18a7138860aa001d7dfc0a2fb3c57ad2064c1c497a6887171b0a34ad4d7`, tanim2_anahtar.json `c0cc3e82c2895c222393932f7ab217f626444e516cb159ba6696ac888e00e916`
- bağımlı kod: goz_uyum.py `828258b1f24d45bc`, tanim2.py `61821c517e75728c`, GOZ_ETIKET.py `76d5c76b3a545ed5`

## 2. Kural (ADIM 1'de, etiketler açılmadan commit; parametreler iş tanımından aynen)
Pencere: kör sayfa penceresi (121 geçerli bar, veri sinyal günü t'de kesik); karar penceresi son 60 mum [t-59..t].
- **(b) SON DİP**: d = [t-59 .. t-5] aralığında en düşük Low'un günü (dipten sonra en az 5 mum); m = t - d.
- **(a) DÜŞÜŞ**: d'den önceki 60 mumun en yüksek High'ı / Low(d) - 1 >= 0,20.
- **(c) HAT BOYUNCA YUKARIDA**: (c1) dip sonrası m mumun hiçbirinin Low'u Low(d)'nin altına inmez VE (c2) hat = dip sonrası Low'ların en küçük kareler doğrusu, eğimi >= 0 VE (c3) dip sonrası mumların en az %80'inde min(O,C) >= hattın o gündeki değeri.
- **(d) ALT FİTİL KÜÇÜLÜYOR**: w_i = (min(O_i,C_i) - L_i) / ATR14(d); dip sonrası w'nin zamana göre en küçük kareler eğimi < 0 VE son üçte birin ortalama w'si < ilk üçte birin ortalama w'si.
- **V1 (ANA)** = a ∧ b ∧ c ∧ d (Cemal'in tam cümlesi); **V2** = a ∧ b ∧ c1 ∧ d (hat şartı yok); **V3** = a ∧ b ∧ c (fitil şartı yok).

Tanım belirsizliklerinin çözümü (etiketlerden önce yazıldı):
- dip_esitlik: eşit en düşük Low birden çok günde ise d = EN SON gün (tam eşitlik, float ==)
- dusus: tepe = max High, d'den önceki 60 mum [d-60 .. d-1] (d hariç); oran = tepe / Low(d) - 1
- dip_delinmez: Low_i >= Low(d) (eşitlik delinme sayılmaz), i = d+1..t
- hat: x = 1..m (i - d), y = Low_i; numpy.polyfit derece 1; hat_i = kesişim + eğim x x_i
- egim_sifir: c2: eğim >= -1e-12 x Low(d) (sayısal sıfır yatay sayılır); d: w eğimi < -1e-12 (sayısal sıfır küçülme sayılmaz)
- hat_ustu: min(O_i,C_i) >= hat_i - 1e-9 x |hat_i| (bağıl sayısal tolerans)
- atr: TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = d-13..d
- ucte_bir: k = floor(m / 3) (m >= 5 olduğu için k >= 1); ilk üçte bir = dip sonrası ilk k mum, son üçte bir = son k mum
- b: pencere geçerli ve d bulunduysa b = DOĞRU (m >= 5 tanım gereği); bulunamazsa kural YOK

DS3_ESIK (tam): `{"atr_n": 14, "belirsizlik": {"atr": "TR_j = max(H_j - L_j, |H_j - C_{j-1}|, |L_j - C_{j-1}|); ATR14(d) = ortalama TR, j = d-13..d", "b": "pencere geçerli ve d bulunduysa b = DOĞRU (m >= 5 tanım gereği); bulunamazsa kural YOK", "dip_delinmez": "Low_i >= Low(d) (eşitlik delinme sayılmaz), i = d+1..t", "dip_esitlik": "eşit en düşük Low birden çok günde ise d = EN SON gün (tam eşitlik, float ==)", "dusus": "tepe = max High, d'den önceki 60 mum [d-60 .. d-1] (d hariç); oran = tepe / Low(d) - 1", "egim_sifir": "c2: eğim >= -1e-12 x Low(d) (sayısal sıfır yatay sayılır); d: w eğimi < -1e-12 (sayısal sıfır küçülme sayılmaz)", "hat": "x = 1..m (i - d), y = Low_i; numpy.polyfit derece 1; hat_i = kesişim + eğim x x_i", "hat_ustu": "min(O_i,C_i) >= hat_i - 1e-9 x |hat_i| (bağıl sayısal tolerans)", "ucte_bir": "k = floor(m / 3) (m >= 5 olduğu için k >= 1); ilk üçte bir = dip sonrası ilk k mum, son üçte bir = son k mum"}, "dip_sonrasi_min": 5, "dusus_bar": 60, "dusus_min": 0.2, "hat_egim_min": 0.0, "hat_ust_pay": 0.8, "hukum": "V1 (ANA): iki set birleşik Cemal kararlarıyla (işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı ayrı da raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33) verilir, hüküm sözü yalnız V1 için", "kappa": {"B": 5000, "bonferroni_k": 3, "gecerli": 0.6, "gecerli_alt": 0.4, "guven": 0.95, "karar_min": 30, "kismen": 0.4, "tohum": 20261125}, "karar_pencere": 60, "not": "parametreler (0,20; 60; 5; %80; üçte bir) iş tanımından aynen; etiketlere bakılmadan sabitlendi; GETİRİ YOK", "pencere_bar": 121, "ucte_bir": 3, "varyant": {"V1": "a ∧ b ∧ c ∧ d (ANA; Cemal'in tam cümlesi)", "V2": "a ∧ b ∧ c1 (dip delinmez) ∧ d (hat şartı yok)", "V3": "a ∧ b ∧ c (fitil şartı yok)"}}`

## 3. Mühürlü yanıtlar (ds3_anahtar.json 'sayfalar'; Cemal'in işaretleri AÇILMADAN yazıldı)
| küme | n | (a) düşüş DOĞRU | (c1) delinmez | (c2) eğim >= 0 | (c3) %80 üstte | (c) | (d) fitil küçülüyor | V1 VAR | V2 VAR | V3 VAR |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 40 | 38 | 29 | 8 | 7 | 24 | 3 | 24 | 7 |
| 2 | 40 | 40 | 35 | 33 | 13 | 11 | 21 | 6 | 18 | 11 |
| birlesik | 80 | 80 | 73 | 62 | 21 | 18 | 45 | 9 | 42 | 18 |

## 4. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in set 1 (cemal_isaret.json) ve set 2 (cemal_isaret2.json) VAR / YOK işaretleri ile V1 / V2 / V3 arasında uyum ve Cohen kappa; set 1, set 2 ve birleşik; işaretsiz / '?' sayfa karar dışı, sayısı ayrıca yazılır.
- Aralık: kappa bootstrap (B 5000, tohum 20261125, sayfa yeniden örneklemesi, yüzdelik): V1 için %95; V2 / V3 için Bonferroni 3 ile %98,33 (ayrıca %95 bilgi).
- HÜKÜM: V1 (ANA): iki set birleşik Cemal kararlarıyla (işaretsiz / '?' sayfa karar dışı) kappa >= 0,60 VE bootstrap %95 alt ucu >= 0,40 (B 5000, sayfa yeniden örneklemesi) -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; kappa < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. Set 1 ve set 2 ayrı ayrı da raporlanır; birinde V1 kappa < 0,40 ise 'tutarsız' notu. V2 / V3 yalnız BİLGİ: aralıkları Bonferroni 3 ile (%98,33) verilir, hüküm sözü yalnız V1 için.
- Ek bilgi (hüküm dışı): uyuşmayan sayfaların (a)-(d) değerleri; Cemal VAR / kod YOK sayfalarda düşen parça sayımı; önceki en iyi GOVDE_1 ile aynı sayfalarda karşılaştırma (GOVDE_1 eşiği set 1 etiketleriyle seçildiği için set 1'de iç-örneklem).
- Kural ve eşik sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 5. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralın uyumu, kappa) |
| K2 | geleceğe bakma | EVET | (a)-(d) yalnız kör sayfa penceresinden: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + ds3_pencere mekanik denetimi (W.index.max() <= t, W.index[-1] == t); ds3.py test prefix değişmezliği (t sonrası değişince sonuç aynı); getiri / sinyal sonrası fiyat okunmaz; Cemal'in işaretleri mühürden önce açılmadı (olc açılış zamanı DS3_SONUC'ta) |
| K3 | geçerli bar | EVET | GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); ds3_parca_dizi NaN / H <= L / L <= 0 görürse durur |
| K4 | tekilleştirme | EVET | sayfalar set 1 (goz_uyum_anahtar) ve set 2 (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa, 60 bar tekil; n = 40 + 40 |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (goz_uyum ile aynı); düşüş oranı ve hat payı birimsiz, fitil ATR14(d) birimi; fiyat birimi kuralı etkilemez |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok |
| K8 | örneklem ve dönem | EVET | 79-80 karar (iki set); karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); 3 varyant: Bonferroni 3 (%98,33) V2 / V3 için; hüküm yalnız V1; set 1 ve set 2 ayrı raporlanır (birinde < 0,40 'tutarsız'); kural etiketlerden SEÇİLMEDİ (Ç211 ezber dersi) |
| K9 | ön kayıt | EVET | kural + DS3_ESIK + varyantlar etiketler açılmadan commit (ADIM 1); yanıtlar ds3_anahtar.json'da etiket açılmadan mühürlü; ds3.py + ds3_anahtar.json + DS3_ESIK + kural kaynağı sha'ları bu dosyada; olc sha'ları denetler ve yanıtları veriden yeniden hesaplayıp mühürle karşılaştırır; hüküm eşikleri sabit |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | ds3.py anahtar aynı komutla deterministik yeniden üretilir (rastgelelik yok); olc 80 sayfanın yanıtını veriden yeniden hesaplar ve mühürlü yanıtla eşitliğini şart koşar; bootstrap tohumu sabit (20261125) |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; hüküm sözü yalnız ön kayıttaki eşikle ve yalnız V1 için |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_DS + test; yasak dosyalar (defter, mevcut .py, anahtar / ön kayıt / sonuç dosyaları) değişmedi (git diff boş); e-posta / anahtar yok (_yaz / _jyaz e-posta taraması); git add -A yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 6. Git kaydı (bu dosyanın yazıldığı an)
- ds3.py: 3d25546326866bbe12282da3d645f5a0baece63a 2026-11-23T18:07:45+00:00
- DS3_IS_TANIMI.md: 3d25546326866bbe12282da3d645f5a0baece63a 2026-11-23T18:07:45+00:00

## 7. Not (etiketler açılmadan yazıldı)
- ds3.py ADIM 1 commit'i (3d25546) ile bu mühür arasında yalnız ölçüm / görsel kodu değişti (PDF'e yakın görünüm paneli, 'tutarsız' notunun iki set birden < 0,40 iken ayrı yazılması, etiket dosyasında sayfa olmayan anahtarın atlanması). Kural kaynağı sha'sı (c10dcfa1...) ve DS3_ESIK sha'sı (390720bd...) ADIM 1 commit mesajındakiyle aynı.
- olc / pdf kod yolu mühürden önce yalnız UYDURMA (rastgele) etiketle, scratchpad dizininde (`--deneme`) sınandı; gerçek etiket dosyaları açılmadı.
- Etiketler açılmadan gözlem (yalnız kodun kendi yanıtı): en kısıtlayıcı parça (c3) 'gövde altı hattın üstünde >= %80' (80 sayfanın 21'inde DOĞRU); (a) düşüş 80 sayfanın hepsinde DOĞRU (sayfalar zaten S6 / Ş1 düşüş seçimi). V1 VAR 9 / 80.
