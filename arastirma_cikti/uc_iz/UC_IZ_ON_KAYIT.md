# UC_IZ ÖN KAYIT — üç fiyat dışı iz aynı KT02 dip olayında, aynı anda (25 Kasım 2026)

Keşif ölçümü (açık veri, KASA kesik 2022-12-31). KASA AÇILMAZ. Push yok. Bu dosya ölçümden ÖNCE commit edilir; tanım / eşik / hücre / karar kuralı sonuca göre değişmez.

KOD_SHA: 326cbaa1291873096c9e7b8f9b95eb50cf85c9daebae508d277532ec55ab80d6
ESIK_SHA: 6899e36cd05fc57e2deb208f49b5bdfa69198339b246108813f15727fe4ed6f7
Kod commit: 307741f (UC_IZ.py + test_uc_iz.py, 6 sentetik test geçti)
Veri: V_ABD.pkl e96a5728320e59ef (KASA açık, mühür f674b4ee291c2f35, en geç 2022-12-30); uyum_toplam.csv.gz afb151db143f0be8; k30_alim.pkl 99edee82f788d6ee; olay.pkl 15a3439a24afac27

## 1. Tanımlar (kaynak fonksiyon / eşik)

- DİP OLAYI (KT02 aynen): KART_TUR2.k2_y1 (YH.yh_s6_hisse 'al' + GE / YH özellikleri) -> KART_TUR2.k2_panel (OS.os_panel + T2 P2 havuzu) -> KART_TUR2._k2_oc (OC.oc_olay_hazirla, P2, tekil 60) -> F_KT02 = YH.yh_s9_sartlar 'S1'. Ölçüm için C2.c2_olay (CETVEL2 v2.2 havuzu, tekil 15 birleşik takvim satırı, ilk kalır; giriş t+1 açılış). TEK SEÇİM: dar = P2 (KT02) VE CETVEL2 havuzu.
- R (sektör rüzgârı, KT10 aynen): KART_TUR2.k2_d9_durum(Vd, 'ABD', K2_ESIK['d9_olay_bas']='2000-01-01') -> D9_YENIDEN.d9_satir 'c' (RÜZGÂR ∧ ¬D9 ∧ sektör var; sektör sektor_ABD.csv, D9_PARAM eşikleri) olay günü t'de. Bilgi R_any = RÜZGÂR.
- B (bilanço, FON_IZI k28 'ust'): KURULAMADI. k28_X_abd ve pead/liste_abd.csv.gz 2022-12-01'de başlıyor (açık kesikten önce 54 / 230 satır, yalnız Aralık 2022). İki karar hücresi kapsanmıyor. B0 da kurulamadı (2022-12 öncesi bilanço günü listesi yok; secfs 2021+ dosyalama tarihi bilanço günü değil, yeni tanım olur). -> YEDEK Y1.
- I (içeriden alım, FON_IZI k30 A1): KURULAMADI. k30_alim.pkl 2022-01-03'te başlıyor (2016-21 SEC Form 4 setleri repoda yok; indirme yasak). 2016-19 hücresi hiç, 2020-22 hücresinin 2 yılı kapsanmıyor. -> YEDEK Y2. Bilgi: I22 = son 30 takvim gününde (dosyalama günü D <= t, D > t-30) >= 1 A1 alımı (>= 10 bin $), yalnız t >= 2022-02-02.
- Y1 (B yedeği, Ç112): FON_IZI.fi_k38_sinyaller 'S3_blok_taban_yukari' (FI_K38: hacim >= 20 x önceki 20 gün medyanı, gün getirisi <= -%9,5, geçerli bar) hissenin t'ye kadarki son 15 geçerli barında (GE.ge_hazir indeksi, t dahil). Pencere B'nin 15 bar penceresi; Ç112'de pencere yoktu (olay günü) -> bu pencere uyarlamadır.
- Y2 (I yedeği, Ç223 T): uyum_toplam.csv.gz ABD, PFc <= -0,10 ∧ MRc >= 0,30 (UYUM_T_ON_KAYIT), T olay günü hissenin t'ye kadarki son 15 geçerli barında (t dahil).
- N = R + Y1 + Y2.

## 2. Ölçü, eş, taban

- R15 ve konum eşi: C2.c2_panel22_al('ABD', ufuk 15) + C2.c2_es (aynı giriş günü, aynı kova 36'lı ATRP x likidite x F15, >= 5 eş). Dışlanan: aynı gün bütün KT02 olayları (C2.c2_olay tekil 1 eşlemesi). Bütün gruplar aynı eş değerlerini kullanır.
- Ö1: hücre = C2.c2_hucre (yön +, egri cetvel2_guc_v2.2.json ABD x hücre x 15) + MU.mu_sira_boot + MU.mu_hukum (plasebo hariç). TUTAR hücrede C2.c2_plasebo (iki yön ayrı) koşulur ve yazılır.
- Ö2: ÜST10 = SIRA >= 0,90; ALT10 = SIRA <= 0,10. Taban formül olay başına ÜST (N - tavan(0,9 N) + 1) / (N + 1), ALT (taban(0,1 N) + 1) / (N + 1) (UC_IZ.uc_taban; kaba kuvvetle test). Taban plasebo: her olay yerine aynı gün aynı kovadan rastgele üye (dip olayı olmayan), SIRA c2_es ile, 200 tohum (UC_IZ.uc_plasebo). Büyüklük ÜST10 - taban, ay kümeli boot %95 (MU.mu_sira_boot).
- Ö3 (bilgi): h5 / st5 = C2.c2_bilgi (stop0 = hat x 0,98) olay için; eş = plasebo tohum 0 üyesi (aynı gün aynı kova). MU.mu_olc_h5 UYGULANMADI (stop0 = Low(L2) MACD'ye özgü). Piyasa yukarı / aşağı = es_r15 > 0 / <= 0. İkinci eş (bilgi): aynı gün N = 0 dip olaylarının R15 ortalaması (kendisi hariç).
- Hücreler: ABD d1619 (giriş 2016-01-01..2019-12-31), ABD d2022 (2020-01-01..2022-12-31) KARAR. 2010-15 BİLGİ hücresi YOK (V_ABD 2015-06'da başlıyor).

## 3. Karar kuralı (aynen; sonuçtan sonra değişmez)

YÖN TUTARLI(iz) <=> iki karar hücresinin (ABD d1619, ABD d2022) ikisinde de FARK(iz var) > 0 VE FARK(var) - FARK(yok) > 0 VE (ÜST10 - taban_formül) > 0 VE (ÜST10 - taban_plasebo) > 0. TUTAR <=> ayrıca iki hücrede c2 hükmü (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç) TUTAR. Aksi: iki hücrede de iz-var n >= 30 ve güç >= 0,80 ise TUTMADI, değilse ÖLÇÜLEMEDİ. BİRLİKTE ARTIYOR <=> iki hücrede FARK(N=0) < FARK(N=1) < FARK(N>=2) VE N>=2 FARK boot alt > 0 en az bir hücrede, ötekinde FARK > 0. KASA ADAYI <=> en az iki iz YÖN TUTARLI VE BİRLİKTE ARTIYOR (yalnız ÖNERİ; kasa açılmaz). BH q 0,10: aile = 3 tek iz + N>=2 (p = iki hücrenin en büyük permütasyon p'si).

Açık veriye bakış: bu iş açık veriye bir kez bakar (kos). Aile içi çoklu karşılaştırma: BH q 0,10, aile 4 (R, Y1, Y2, N>=2). Evren bugün işlem görenler (K7): dipte sonuç yukarı yanlı. Komisyon / kayma yok.

## 4. Doğrulamalar (getirisiz; ölçümden önce)

- D1 (KART_TUR2 açık çıktısı k2_satir, ABD, ufuk 15, olay günü 2016-01-01..2022-11-30): KT02 k2 1167 / UC 336, ortak 331. Ortak sembollerde (266) k2 353 / UC 331, ortak 331: ortak sembollerde UC olaylarının hepsi k2'de var (331/331); kalan 5 UC olayı k2'de KT02'si olmayan 4 sembolde; k2'nin ortak sembollerdeki 22 fazla olayı P2 / 60 gün tekil zincirinin farklı veri başlangıcından (2000 / 2015-06). Fark nedeni: KART_TUR2 açık çıktısı KASA 2 tezgâh verisiyle (TEZGAH2 ABD evreni, 2000'den; 878 sembolde KT02) koşuldu; bu ortamda yalnız KASA 1 V_ABD (1.361 hisse, 2015-06'dan) var. Evren ve P2 havuz sınırları (kesit) farklı. KT10: k2 20968 / UC 16511, ortak 7558; düşük örtüşme beklenen: sektör sepeti evren ortalaması olduğu için rüzgâr bayrağı evrene bağlı. Yıl dağılımı aynı biçimde (2020 düşük, 2021-22 yüksek KT02). Hüküm: tanım aynı, sayılar evren farkıyla açıklandı (birebir değil).
- D2 (K2): PREFIX (veri bellekte 2019-06-28 ve 2021-06-30'da kesildi, dip olayı + R / Y1 / Y2 / I22 baştan): 2019-06-28 100 / 100 olay birebir, bayrak farkı 0; 2021-06-30 161 / 161 birebir, bayrak farkı 0. Not: Y2 kaynağı (uyum_toplam) Ç217 / Ç223'te kendi prefix denetiminden geçti, burada yeniden hesaplanmadı (yalnız pencere mantığı sınandı). 30 rastgele olayda ham olay günü <= t: True. Olay dosyaları uc_kes ile <= 2022-12-31 kesildi (S3 0, T 0, k30 5.702 satır atıldı) ve assert edildi. İş tanımındaki 'olay başına t'de kesme' yerine iki kesikli prefix testi yapıldı (her olay için bütün evren yeniden hesabı ~3 dk; SAPMA değil, daha geniş denetim).
- D3 (K10): Y1 bayraklı olay YOK (0); 10 rastgele Y2 olayında T satırı (PFc <= -0,10, MRc >= 0,30, T günü <= t ve son 15 barda) elle okundu: 10/10 uygun. 8 I22 olayının (hepsi) Form 4 satırı (dosyalama günü t'den 23-29 gün önce, değer >= 10 bin $, rol, erişim no) okundu: 8/8 uygun. Ayrıntı uc_iz_hazirlik.json 'D3'.

## 5. Getirisiz sayımlar ve güç beklentisi (eşli olay; güç = cetvel2_guc_v2.2, delta +0,02)

KT02 dip olayı 341, eşli 329.

| grup | d1619 n | güç | d2022 n | güç |
|---|---|---|---|---|
| HEPSI | 134 | 0.51 | 195 | 0.55 |
| R=1 | 6 | 0.06 | 9 | 0.06 |
| R=0 | 128 | 0.49 | 186 | 0.53 |
| Y1=1 | 0 | 0.00 | 0 | 0.00 |
| Y1=0 | 134 | 0.51 | 195 | 0.55 |
| Y2=1 | 3 | 0.04 | 10 | 0.06 |
| Y2=0 | 131 | 0.50 | 185 | 0.53 |
| R_any=1 | 6 | 0.06 | 9 | 0.06 |
| I22=1 | 0 | 0.00 | 8 | 0.06 |
| I22=0 | 0 | 0.00 | 110 | 0.33 |
| N=0 | 125 | 0.48 | 176 | 0.50 |
| N=1 | 9 | 0.07 | 19 | 0.09 |
| N=2 | 0 | 0.00 | 0 | 0.00 |
| N=3 | 0 | 0.00 | 0 | 0.00 |
| N>=2 | 0 | 0.00 | 0 | 0.00 |
| R∧Y1 | 0 | 0.00 | 0 | 0.00 |
| R∧Y2 | 0 | 0.00 | 0 | 0.00 |
| Y1∧Y2 | 0 | 0.00 | 0 | 0.00 |

Örtüşme (phi, eşli olaylar): R-Y2 -0.044; Y1 sabit 0 (phi tanımsız).

Güç beklentisi: hiçbir iz-var grubu ve hiçbir N >= 1 grubu n >= 30'a ulaşmıyor; HEPSİ bile güç 0,51 / 0,55. Kural gereği bütün tek izler ÖLÇÜLEMEDİ, BİRLİKTE ARTIYOR değerlendirilemez (N >= 2 n = 0), KASA ADAYI beklenmez. Ölçüm yine koşulur (kural: sonuç ne çıkarsa yazılır).

## 6. KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; aynı gün KT02 dip olayları dışlanır); iz var / yok ve N = 0 aynı dip olay kümesinden; taban formül + plasebo (aynı gün aynı kova rastgele üye, 200 tohum) |
| K2 | geleceğe bakma | EVET | R: D9 durumu t'ye kadar fiyatla; Y1 / Y2: pencere [t-14 geçerli bar, t]; I22: D <= t; olay dosyaları <= 2022-12-31 KES + assert (uc_kes); D2 prefix testi (2019-06-28 ve 2021-06-30 kesik) + 30 rastgele olayda hisse kesik denetimi |
| K3 | geçerli bar | EVET | geçerli bar GE.ge_hazir (H > L, V > 0); KT02 YH S6 / GE özellikleri aynen; Y1 S3 'gecerli' şartı; R15 CETVEL2 panel |
| K4 | tekilleştirme | EVET | dip olayları aynı hissede >= 15 birleşik takvim satırı (C2.c2_olay tekil 15, ilk kalır); Y1 sinyali 60 gün tekil (KT02 aynen); medyan yazılır |
| K5 | giriş fiyatı | EVET | giriş = t + 1 açılış (OC.oc_olay_hazirla); R15 = 15. geçerli bar kapanışı / giriş açılışı - 1 |
| K6 | veri birimi | EVET | fiyat KASA açık V_ABD (fi_k1_veri bölünme düzeltmeli, tek kip); yeni pazar yok; Y1 hacim oranı birim bağımsız |
| K7 | hayatta kalma | EVET | evren bugün işlem gören 1.361 ABD hissesi; batanlar yok; dip olaylarında sonuç yukarı yanlı okunur (raporda) |
| K8 | örneklem ve dönem | EVET | n < 30 hücre ÖLÇÜLEMEDİ; iki dönem (2016-19 / 2020-22) aynı yön şartı; BH q 0,10 aile 4; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | tanım + eşik (UC_ESIK sha) + kod sha + D1-D3 ön kayıtta, ön kayıt commit'i koşudan önce; kapı uc_kapi bunu denetler |
| K10 | ayrıştırma | EVET | D3: 10 rastgele Y1 ve 10 rastgele Y2 (ve 10 I22) bayraklı olayda ham satır (S3 günü hacim / medyan / getiri; T satırı PFc / MRc; Form 4 satırı) yazdırılıp elle okunur; haber / kurum etiketi maddeleri UYGULANMAZ (KAP haberi yok) |
| K11 | yeniden üretim | EVET | D4: en az 2 hücre uc_iz_satir.csv.gz'den bağımsız düz pandas ile yeniden üretilir (raporda) |
| K12 | ifade | EVET | fiyat değişimi (R15) ile kâr / zarar ayrı; 'iz' sözü yalnız karar kuralı geçerse; sayı ile yorum ayrı cümlede |
| K13 | süreç | EVET | çakışma kapısı var; mevcut modüller / defterler değişmez; push yok; yeni dal yok; e-posta / anahtar yok |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; alım-satım önerisi yok; keşif ölçümü |
