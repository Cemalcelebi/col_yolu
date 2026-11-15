# D9_AVR — RAPOR TASLAĞI (AŞAMA 1; ölçüm KOŞULMADI)

Durum: AŞAMA 1 bitti (sektör listesi, kod, test, ön kayıt). `kos` ana model ön kaydı commit edip 'koş' dedikten sonra koşar; `python D9_AVR.py rapor` bu dosyayı sonuçla yeniden yazar (TEST, HATA, SAPMA, DENETİM, ÖNERİLEN DEFTER METNİ bölümleri korunur).

## ÖZET

- Avrupa sektör listesi var: sektor_AVR.csv, 581 sembol (V_AVR ile birebir), 21 sınıf (20 ICB süpersektör + 'Investment Trusts' fon sınıfı), sektörü boş 0 (3 boş Wikipedia STOXX Europe 600 satırından tamamlandı).
- En küçük sınıf 8 üye (Personal Care, Drug and Grocery Stores): RUZ_MIN_UYE 4 altında kalan sınıf YOK.
- Olay sayımı (getiri yok; cetvel sonrası, girişe göre) AVR 2023 / 2024-26: (a) 1.102 / 2.264 (D9_YENIDEN ile AYNI), (b) 110 / 218, (c) 125 / 509.
- Fon sınıfı hiç rüzgâr almadı: (b) / (c) 'Investment Trusts hariç' sayım toplamla aynı (fon olayı 0).
- Güç ön bilgisi: (c) AVR 2023 güç %29, AVR 2024-26 güç %51,5 (eşik %80, n < 1.000). İki hücre de TUTAR değilse sonuç ÖLÇÜLEMEDİ olur; önceden yazılı 'EMARE ZAYIFLADI' dalına bu veriyle ulaşılamaz.

## SEKTÖR LİSTESİ (sektor_AVR.csv 'ust'; ayrıntı sektor_AVR_eslesme.md)

| ust | üye | rüzgâr alabilir mi (öteki üye >= 4) |
|---|---|---|
| Automobiles and Parts | 11 | EVET |
| Banks | 27 | EVET |
| Basic Resources | 15 | EVET |
| Chemicals | 18 | EVET |
| Construction and Materials | 24 | EVET |
| Consumer Products and Services | 27 | EVET |
| Energy | 15 | EVET |
| Financial Services | 38 | EVET |
| Food, Beverage and Tobacco | 20 | EVET |
| Health Care | 33 | EVET |
| Industrial Goods and Services | 95 | EVET |
| Insurance | 21 | EVET |
| Investment Trusts | 77 | EVET |
| Media | 14 | EVET |
| Personal Care, Drug and Grocery Stores | 8 | EVET |
| Real Estate | 27 | EVET |
| Retail | 26 | EVET |
| Technology | 22 | EVET |
| Telecommunications | 17 | EVET |
| Travel and Leisure | 23 | EVET |
| Utilities | 23 | EVET |

- Sembol 581; sektörü boş 0; fon sınıfı 'Investment Trusts' 77 (FTSE 250 'Investment Trusts' 70 + 'Equity Investments' 3 + 'Collective Investments' 3 + 'Hedge Funds' 1; işletme değil fon).
- Wikipedia tamamlamaları: ATCO-A.ST -> Industrial Goods and Services; ERIC-B.ST -> Telecommunications; BT.A.L -> Telecommunications (V_AVR'de yok).
- Sınır: etiket isimden; bazı fonlar 'Financial Services' / 'Energy' etiketli (3IN, INPP, SEQI, SOI, PPET, GCP, VEIL, VOF, SEIT), Man Group (işletme) 'Investment Trusts' etiketli. Etiket BUGÜNKÜ listedir (K2 / K7).

## ÖN KAYIT ÖZETİ

- Dosya: arastirma_cikti/d9_avr/D9_AVR_ON_KAYIT.md (+ d9_avr_tercil.json; AVR tercil sınırları ruz 0,1190 / 0,1531).
- Sabit: D9_PARAM (RUZ_GERI 60, RUZ_ESIK 0,10, RUZ_MIN_UYE 4, RUZ_MUTLAK 0, RUZ_BAYAT 5; D9 sabitleri), ORTAK_CETVEL v1.0 (CETVEL_SHA 4763c458…), sektör sütunu 'ust', satırlar a / b / c.
- KARAR (satır c, hücre = cetvel durumu 'TUTAR'): AVR 2023 ve AVR 2024-26 ikisi TUTAR -> 'Ç181c EMARE GÜÇLENDİ (4 karar hücresinin 3'ü; ABD 2023 alt uç -0,3 olduğu için İZ DEĞİL, bilinen etki)'; biri TUTAR -> 'EMARE (değişmedi), tek pazar tek dönem'; ikisi TUTMADI (güç yeterli) -> 'EMARE ZAYIFLADI: rüzgâr Avrupa'da görünmüyor'; TUTAR yok ve biri ÖLÇÜLEMEDİ -> 'EMARE (değişmedi); AVR ÖLÇÜLEMEDİ'.
- (a) yalnız tutarlılık (ön kayıt sayımı D9_YENIDEN ile AYNI; koşuda hücre n'i de aynı beklenir); (b) BİLGİ, n < 1.000 ÖLÇÜLEMEDİ.
- Kapı: `kos` IZ_KARNE.ik_kontrol_kapisi + OC.oc_kapi + d9a_onkayit_dogrula (D9A_ESIK, D9_PARAM, D9_AVR.py, D9_YENIDEN.py, sektor_AVR.csv, eşleme md, V_AVR.pkl sha; ön kayıt, D9_AVR.py, sektor_AVR.csv, eşleme md, tercil json, D9_YENIDEN.py git'e işlenmiş ve değişmemiş). COL_v1.py sha yalnız bilgi (T8 işi COL_v1'i değiştiriyor); D9_PARAM == COL_v1 sabitleri ayrıca denetlenir.

## TEST

- `python test_d9_avr.py`: 45 geçti, 0 kaldı (sektör listesi V_AVR ile birebir ve ham evrenden yeniden üretilebilir; eşleme md tutarlı; sentetik AVR akışı a / b / c boş değil; d9a_durum == D9_YENIDEN.d9_durum (uzun hisseler); kısa hisse düzeltmesi; geleceğe bakma denetimi AVR sözlüğüyle; D9_YENIDEN.D9_ESIK değişmedi (sha 88c5a047… ön kayıtla aynı); kontrol kapısı eksik / HAYIR satırda durur; karar kuralı dört dal; e-posta / anahtar yok).
- `python test_d9_yeniden.py`: 22 geçti, 0 kaldı (değişmeden).
- Gerçek ön kayıtta: ik_kontrol_kapisi geçti, oc_kapi (git hariç) geçti, d9a_onkayit_dogrula (git hariç) geçti; git kapısı commit olmadığı için beklenen biçimde durdu.

## DENETİM

- K10 elle: sektor_AVR.csv'den rastgele 4 satır (random_state 15) Wikipedia wikitext (15 Kas 2026) ile karşılaştırıldı: IWG.L Support Services (FTSE 250 satırı), WIZZ.L Travel & Leisure (FTSE 250), LSEG.L Financial Services (STOXX Europe 600), UEM.L Investment Trusts (FTSE 250): 4/4 tuttu.
- 3 boş sektör: STOXX Europe 600 wikitext satırları Atlas Copco -> Industrial Goods and Services, Ericsson -> Telecommunications, BT Group -> Telecommunications.

## HATA

- H-a (D9_YENIDEN, gizli hata, Ç181 sonucunu etkilemez): D9_YENIDEN.d9_durum, 250 temiz bardan kısa bir hissede rüzgâr günü varsa AttributeError ile düşer (d9_uzun_seri n < W iken 'bant250' sütununu üretmez). AVR'de SHAW.L (210 bar) bunu tetikledi; Ç181'de AVR rüzgârı yoktu, BIST / ABD koşusu tamamlandığı için o ölçüleri etkilemedi. Düzeltme D9_YENIDEN'e dokunmadan D9_AVR.d9a_durum'da (birebir kopya, eksik bant sütunu NaN; sinyal değişmez; test: uzun hisselerde D9_YENIDEN ile birebir aynı tablo). D9_YENIDEN'in bir sonraki sürümünde aynı düzeltme önerilir.
- H-b (süreç, bilgi): çalışma sırasında COL_v1.py, takip.py, test_takip.py, T8_KALDIR_IS_TANIMI.md başka bir iş (T8 uzun çöl etiketi kaldırma) tarafından çalışma ağacında değiştirildi; bu iş onlara dokunmadı. Bu yüzden COL_v1 sha D9_AVR kapısından çıkarıldı (bilgi satırı); D9_PARAM == COL_v1 sabitleri denetimi (d9_param_denetle) kapıda kaldı. T8 değişikliği commit edilince COL_V1_SHA bilgi satırı eskir; koşuyu durdurmaz.
- H-c (iş tanımı / veri): iş tanımı 'Investment Trusts (FTSE 250, 70 hisse)' diyor; fon etiketli 3 ham ad daha (Equity Investments 3, Collective Investments 3, Hedge Funds 1) aynı fon sınıfına alındı -> sınıf 77. Ayrıca fon olan ama işletme etiketi taşıyan 9 FTSE 250 üyesi ve fon etiketli Man Group etikete dokunulmadan bırakıldı.
- H-d (iş tanımı / cetvel): iş tanımı 'OC dört şartı' diyor; cetvel durumu 'TUTAR' iki alt yarı şartını da ister. Karar 'TUTAR'a bağlandı (Ç181 ile aynı); 'tutar4' bilgi. Ana model onayı gerekir.
- H-e (güç): (c) AVR hücreleri güç eşiğinin altında (n 125 / 509; güç %29 / %51,5): önceden yazılı 'ZAYIFLADI' dalı bu veriyle ulaşılamaz; dördüncü dal ('AVR ÖLÇÜLEMEDİ') sonuç görülmeden eklendi.

## SAPMA

- (koşu sonrası doldurulur; AŞAMA 1'de sapma yok)

## ÖNERİLEN DEFTER METNİ

- (AŞAMA 2 sonunda yazılır)

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL; her satır EVET / UYGULANMAZ + kanıt)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eşler ve plasebo YALNIZ ORTAK_CETVEL.oc_olc (D9_YENIDEN.d9_olc_satir): aynı giriş günü, aynı pazar (AVR), 60 gün momentum beşliği x 20 gün likidite (EUR, Kur sütunu) üçlüsü, aynı açılış girişi / 60. gün çıkışı; 200 plasebo portföy. Mekanik üstünlük: (c) rüzgâr SEKTÖR momentumudur; hisse momentumu eşlenir, sektör momentumu eşlenmez -> sonuç 'bilinen etki' (Moskowitz-Grinblatt 1999) okunur, yeni iz sayılmaz |
| K2 | geleceğe bakma | EVET | D9 t'ye kadar barlarla (rolling, geriye), rüzgâr t'ye kadar kapanışlarla; kos d9a_gelecek_denetimi 30 rastgele olayda seriyi t'de keser, COL_v1 kopyası (d9_uzun_ref / d9_ruzgar_ref) AVR sektör sözlüğüyle aynı D9 / ruz değerini mekanik denetler; test_d9_avr 'geleceğe bakma'. SINIR: sektor_AVR.csv BUGÜNÜN listesi (Wikipedia 2026 bileşenleri ve bugünkü ICB sınıfı), karar günündeki sektör değil; sınıf değişimi nadir ama etiket sabit varsayılır (K7 ile birlikte yazılır) |
| K3 | geçerli bar | EVET | OC.oc_veri temiz bar (H>L, V>0, O/H/L/C > 0, 31.08.2026 kesik) üzerinden sinyal ve rüzgâr paneli; geçersiz bar olay günü olamaz (cetvel 'sinyal barı geçersiz' sayımı) |
| K4 | tekilleştirme | EVET | durum günleri cetvele verilir; OC.oc_olay_hazirla aynı hissede 60 gün tekilleştirir; n bağımsız olay; hücre tablosunda medyan |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar açılışı (OC.oc_olay_hazirla); sinyal t kapanışında |
| K6 | veri birimi | EVET | tek kip V_AVR.pkl (fi_k1_veri düzeltilmiş, yerel para; .L peni); rüzgâr ve D9 oranlardan (birimden bağımsız); likidite EUR (Kur). Ön kayıtta günlük >= 1,8x sıçrama listesi (temiz barlarda 18 gün, 100x birim kayması YOK; bölünme / şirket ayrılması örn. VIV.PA 09.12.2024, HOLN.SW 16.06.2025) yazılı; düzeltilmez (sinyal tanımı değişmez; BIST / ABD ile aynı işlem), sepet ortalamasını 60 gün etkileyebilir -> sınır olarak raporda |
| K7 | hayatta kalma | EVET | evren BUGÜN işlem gören STOXX 600 + FTSE 250 üyeleri (581 sembol); batan / endeksten çıkan YOK -> getiriler yukarı, -%50 olasılığı aşağı yanlı okunur; sektör etiketi de bugünkü (K2 notu). Büyük hisselerde yanlılık küçük (CLAUDE.md) |
| K8 | örneklem ve dönem | EVET | AVR x 3 dönem (2016-22 keşif bilgi; 2023, 2024-26 karar); n < 30 ÖLÇÜLEMEDİ; İZ DEĞİL / zayıfladı yalnız güç yeterliyken; 3 satır, tek sektör sütunu (ikinci koşu yok); olay sayımı ön kayıtta getiri hesaplanmadan |
| K9 | ön kayıt | EVET | D9A_ESIK (eşleme dahil) sha, D9_PARAM sha, D9_AVR.py / D9_YENIDEN.py sha (COL_v1.py sha bilgi), sektor_AVR.csv + eşleme md sha, V_AVR.pkl sha, cetvel üç sha ön kayıtta; kos IZ_KARNE.ik_kontrol_kapisi + OC.oc_kapi + d9a_onkayit_dogrula (git işlenmiş / değişmemiş; sha eşit) geçmezse durur; karar kuralı sonuçtan önce yazılı |
| K10 | ayrıştırma | EVET | ayrıştırma: Wikipedia bileşen listesi (islenmis-veri avr/evren_avr_ham.csv) -> sektör; 3 boş sektör Wikipedia STOXX Europe 600 satırından elle doğrulandı (D9A_WIKI); her ham ad tek ust'a (D9A_ESLESME; test); rastgele 3 satır elle denetlendi (rapor); haber / kurum etiketi maddeleri uygulanmaz (metin yok). SINIR: FTSE 250 etiketleri isimden: bazı fonlar 'Financial Services' / 'Energy' etiketli (3IN, INPP, SEQI, SOI, PPET, GCP, VEIL, VOF, SEIT), Man Group 'Investment Trusts' etiketli; etikete dokunulmadı (eşleme md) |
| K11 | yeniden üretim | EVET | satır verisi /tmp/d9_avr/olay_<satır>.csv.gz + durum.csv.gz; hücre özeti arastirma_cikti/d9_avr/d9_avr_hucre.csv; >= 2 hücre bağımsız denetçi tarafından yeniden üretilir (ana model işi) |
| K12 | ifade | EVET | etiketler yalnız oc_hucre_durum / oc_etiket ve önceden yazılı karar kuralı; 'bilinen etki' etiketi; fiyat değişimi ile işlem kârı ayrı (komisyon yok); sayı ve yorum ayrı cümle |
| K13 | süreç | EVET | çakışma kapısı _cakisma_kontrol_d9a; D9_YENIDEN / ORTAK_CETVEL / COL_v1 / IZ_KARNE / defterler yalnız okunur (git status denetimi); D9_YENIDEN.D9_ESIK kalıcı değişmez (derin kopya; test); e-posta / anahtar taraması testte; ücretli veri yok (Wikipedia + islenmis-veri) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; ölçüm (T8 üretim ekranı kararı Cemal'in) |
