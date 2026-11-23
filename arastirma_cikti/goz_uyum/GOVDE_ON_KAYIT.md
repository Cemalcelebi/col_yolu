# GÖVDE TEPKİSİ — ÖN KAYIT (ikinci setin Cemal işaretleri gelmeden ÖNCE mühürlenir)

Üretim: 2026-11-23T16:55:21Z (UTC). Soru: Cemal'in 23.11.2026 sözü ("dip delinmiş mi tamam, bu kolay, ancak bu yeterli değil; çünkü mumların fitili değil GÖVDE ile tepki alması gerekir bu diplerde") ölçülebilir bir 'gövde tepkisi' kuralına çevrilince, ikinci bağımsız kör sette (TANIM2_KOR.pdf) Cemal'in VAR / YOK işaretleriyle örtüşüyor mu? GETİRİ ÖLÇÜLMEZ.

**NOT:** ikinci set GOVDE'ye göre tabakalanmadı (ADAY_1 x Ş3 tabakalı); GOVDE ikinci sette ikincil adaydır; tanım Cemal'in 23 Kas sözünden, ikinci setin işaretleri gelmeden mühürlendi.

## 1. Mühür (sha256)
- anahtar: `arastirma_cikti/goz_uyum/govde_anahtar.json` sha256: `0c1c3012c10ca40b3a16effd8b9bcf108d7ddcd85719419e02d4df0a5f5c760b`
- kod: `arastirma_cikti/goz_uyum/govde.py` sha256: `04abb91291bc90bfce182d949c38012b001a0dbba04ddba422466f2043be5a6d`
- eşik sözlüğü (GV_ESIK) sha256: `f1b5706b300937fbe62f039debd3ecc27c9dfccbd01ceca4067e7798819bb2b3`
- tanım sözlüğü (GV_OZ) sha256: `516b49f0fc23f2c4f0717147bbd21aa23f2058d0e1d1852f061fd5a126908a85`
- iş tanımı: `arastirma_cikti/goz_uyum/GOVDE_IS_TANIMI.md` sha256: `0cf4af0e5303302de43d0600ec1c4c7eac719929e36f83147491ae3b9eb31260`
- ikinci set anahtarı (değişmedi; tanim2 mührü): `tanim2_anahtar.json` sha256: `c0cc3e82c2895c222393932f7ab217f626444e516cb159ba6696ac888e00e916`
- bağımlı kod: tanim2.py `61821c517e75728c`, goz_uyum.py `828258b1f24d45bc`, GOZ_ETIKET.py `76d5c76b3a545ed5`

## 2. Tanımlar (ADIM 1'de etiket hesabından önce commit)
Pencere: kör sayfa penceresi (goz_uyum._gu_pencere, veri sinyal günü t'de kesik) içindeki son 40 mum [t-39..t]. Gövde altı = min(Open, Close). S_g = son 40 mumda gövde altlarının en düşüğü (GÖVDE DİBİ); lo = son 40 mumda en düşük Low (FİTİL DİBİ); hi = en yüksek High. ATR14 = son 14 barın gerçek aralık ortalaması; ATRP14 = ATR14 / C_t. Gövde dokunuşu = gövde altı <= S_g x (1 + 0,5 x ATRP14).
- **G1_govde_dokunus_n** (VAR yönü `>=`): GÖVDE DESTEĞİ: son 40 mumda gövde altı (min(O,C)) gövde dibi S_g'nin S_g x (1 + 0,5 x ATRP14) bandında kalan mum sayısı (dip gövdeyle kaç kez savunuldu). NaN: NaN olmaz (S_g barının kendisi her zaman bantta; en az 1).
- **G2_dip_alt_fitil** (VAR yönü `<=`): GÖVDE / FİTİL DİBİ: son 40 mumda dip bölgesi (L <= lo + 0,20 x (hi - lo)) barlarında ortalama alt fitil payı (min(O,C) - L) / (H - L) (küçük = dipte gövde tepkisi, uzun alt fitil yok). NaN: NaN olmaz (lo barı her zaman dip bölgesinde).
- **G3_govdeli_tepki_payi** (VAR yönü `>=`): GÖVDELİ TEPKİ: her gövde dokunuşundan (G1 bandı, bar j) sonraki 3 mum [j+1..min(j+3, t)] içinde C > O ve (C - O) >= 0,5 x (H - L) olan (güçlü gövdeli yükselen) mum bulunan dokunuşların payı; payda = j < t olan dokunuşlar. NaN: j < t olan dokunuş yoksa NaN (kuralda YOK).
- **G4_fitil_govde_arasi** (VAR yönü `<=`): FİTİL DİBİ ile GÖVDE DİBİ ARASI: (S_g - lo) / ATR14 (küçük = dip gövdeyle kurulmuş, fitille aşağı sarkmamış). NaN: ATR14 <= 0 ise NaN (ge_hazir geçerli barda olmaz).

## 3. Seçim kuralı (iş tanımından; etiketlerden önce yazıldı)
Her özellik için YÖN ÖNCEDEN SABİT (GV_OZ['yon']); tek eşik = ilk 40 sayfada (goz_uyum_anahtar.json + cemal_isaret.json; hedef = Cemal VAR) dengeli doğruluğu en yüksek yapan (eşik adayları: ardışık benzersiz sonlu değerlerin orta noktaları; eşitlikte ham doğruluk büyük > eşit eşik listesinin alt-orta elemanı; NaN = YOK). LOOCV kappa: her dışarıda bırakılan sayfa için eşik kalan 39 sayfadan aynı kuralla yeniden seçilir. GOVDE_1 = LOOCV kappa'sı en yüksek tek özellik (eşitlikte 40 sayfa kappa büyük > G sırası); GOVDE_2 = GOVDE_1 VE eski Ş3 (dip delinmemiş: F2 >= -0,01). Eşik 40 sayfanın TAMAMIYLA seçilir ve SAYI olarak mühürlenir.

## 4. İlk set (KEŞİF, 40 sayfa; Cemal VAR 14 / YOK 26; Ş3 kappa 0.400)
| özellik | yön | eşik (40 sayfa) | kappa 40 | LOOCV kappa | VAR medyan [q25, q75] | YOK medyan [q25, q75] | 40'ta VAR | Ş3 ile kappa |
|---|---|---|---|---|---|---|---|---|
| G4_fitil_govde_arasi | <= | 0.4046040192474485 | 0.378 | 0.378 | 0.248 [0.176, 0.360] | 0.440 [0.280, 0.656] | 23 | 0.497 |
| G2_dip_alt_fitil | <= | 0.3005774296955476 | 0.209 | 0.057 | 0.279 [0.261, 0.300] | 0.299 [0.232, 0.336] | 25 | 0.341 |
| G3_govdeli_tepki_payi | >= | 0.8375 | -0.061 | -0.136 | 0.500 [0.333, 0.851] | 0.800 [0.500, 1.000] | 13 | 0.079 |
| G1_govde_dokunus_n | >= | 7.0 | 0.211 | -0.383 | 3.000 [2.250, 5.750] | 3.000 [2.000, 4.750] | 4 | 0.262 |

## 5. Mühürlü kurallar (SAYI; 40 sayfanın tamamıyla seçildi; NaN = YOK)
- **GOVDE_1**: VAR ⇔ G4_fitil_govde_arasi <= 0.4046040192474485. Tanım: FİTİL DİBİ ile GÖVDE DİBİ ARASI: (S_g - lo) / ATR14 (küçük = dip gövdeyle kurulmuş, fitille aşağı sarkmamış). 40 sayfada kappa 0.378, LOOCV kappa 0.378 (keşif).
- **GOVDE_2**: VAR ⇔ GOVDE_1 VE Ş3 (G4_fitil_govde_arasi <= 0.4046040192474485 VE F2 >= -0,01). 40 sayfada kappa 0.497, LOOCV kappa 0.497 (keşif).
- Karşılaştırma (tanim2 mührü, değişmez): ADAY_1, ADAY_2, KONTROL (Ş3) — tanim2_anahtar.json yanıtları.

## 6. İkinci set yanıtları (govde_anahtar.json 'sayfalar'; Cemal'in işareti YOK iken yazıldı)
GOVDE_1 VAR 26 / 40; GOVDE_2 VAR 15 / 40; ADAY_1 VAR 20 / 40; GOVDE_1 ile ADAY_1 18 sayfada ayrışıyor (sayfalar [1, 3, 5, 7, 9, 13, 16, 18, 20, 21, 23, 25, 26, 36, 37, 38, 39, 40]); GOVDE_2 ile ADAY_1 19 sayfada ayrışıyor.

## 7. ÖLÇÜ ve HÜKÜM (önceden yazılı, değişmez)
- Cemal'in ikinci setteki VAR / YOK işaretleri ile GOVDE_1, GOVDE_2 (ve karşılaştırma: ADAY_1, ADAY_2, KONTROL) arasında uyum ve Cohen kappa; '?' karar dışı, sayısı ayrıca yazılır; kappa bootstrap %95 aralığı (B 5000, tohum 20261124, sayfa yeniden örneklemesi).
- HÜKÜM: ikinci sette GOVDE_1 (ve GOVDE_2) kappa >= 0,60 ve bootstrap %95 alt ucu >= 0,40 -> TANIM GEÇERLİ; kappa 0,40-0,60 (ya da kappa >= 0,60 ama alt uç < 0,40) KISMEN; < 0,40 GEÇERSİZ; karar sayısı < 30 ise ÖLÇÜLEMEDİ. ADAY_1 / ADAY_2 / KONTROL (tanim2 mührü) karşılaştırma için yazılır.
- Eşik ve kural sonuca göre oynanmaz; sonuçtan sonra yalnız gösterim değişir.

## 8. KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; `python IZ_KARNE.py kontrol` biçimi)
| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | UYGULANMAZ | bu iş getiri / hedef ölçmez; kontrol grubu gerekmez (yalnız Cemal'in işaretleriyle kuralların uyumu, kappa) |
| K2 | geleceğe bakma | EVET | G1-G4 yalnız kör sayfa penceresinin son 40 barından: tanim2.tz_pencere = goz_uyum._gu_pencere (veri t'de KESİK, 121 bar) + mekanik denetim (W.index.max() <= t, W.index[-1] == t); govde.py test prefix değişmezliği (t sonrası değişince G1-G4 aynı); getiri / sinyal sonrası fiyat okunmaz; ikinci setin Cemal işareti mühür anında yok |
| K3 | geçerli bar | EVET | GE.ge_hazir (H>L, V>0, O/H/L/C>0) geçerli bar (goz_uyum ile aynı); gv_ozellik_dizi H <= L / NaN görürse durur |
| K4 | tekilleştirme | EVET | sayfalar ilk set (goz_uyum_anahtar) ve ikinci set (tanim2_anahtar) ile aynı: aynı hissede en çok 1 sayfa, 60 bar tekil; n = 40 + 40 |
| K5 | giriş fiyatı | UYGULANMAZ | giriş fiyatı / getiri bu işte hesaplanmaz; yalnız sinyal öncesi grafik |
| K6 | veri birimi | EVET | tek kip V_*.pkl (goz_uyum ile aynı); G1 bar sayısı, G2 / G3 pay, G4 ATR birimi: birimsiz |
| K7 | hayatta kalma | EVET | evren bugün işlem gören hisseler (hayatta kalma yanlılığı); görsel uyum sınaması, getiri iddiası yok |
| K8 | örneklem ve dönem | EVET | keşif 40 sayfa küçük örneklem: 'KEŞİF' etiketli; 4 özellik (çoklu karşılaştırma küçük), yön önceden sabit; seçilen kural yalnız ikinci bağımsız 40 sayfada sınanır; karar < 30 ise ÖLÇÜLEMEDİ; kappa bootstrap %95 (B 5000); ikinci set GOVDE'ye göre tabakalanmadı |
| K9 | ön kayıt | EVET | tanımlar (GV_OZ) + sabit yönler + seçim kuralı etiket hesabından önce commit (ADIM 1); eşikler SAYI olarak bu dosyada; govde_anahtar + govde.py + GV_ESIK sha'ları burada; bu dosya ikinci setin Cemal işaretleri gelmeden commit; hüküm eşikleri sabit |
| K10 | ayrıştırma | UYGULANMAZ | metin / haber ayrıştırma yok; yalnız OHLCV |
| K11 | yeniden üretim | EVET | govde.py anahtar aynı komutla deterministik yeniden üretilir (rastgelelik yok); olc tabloyu anahtardan ve tanim2_anahtar'dan yeniden kurar |
| K12 | ifade | EVET | iddia yok; yalnız 'uyum' ve 'kappa' sayısı; keşif sayıları 'bulgu' denmez; hüküm sözü yalnız ön kayıttaki eşikle |
| K13 | süreç | EVET | çakışma kapısı _CK_ONCE_GV + test; yasak dosyalar (defter, mevcut .py, tanim2 / goz_uyum dosyaları ve mühürleri) değişmedi (git diff boş); e-posta / anahtar yok; git add -A yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil |

## 9. Git kaydı (bu dosyanın yazıldığı an)
- govde.py: 10a65faebc8326a2254d1300923c06da8c28c9d5 2026-11-23T16:55:06+00:00
