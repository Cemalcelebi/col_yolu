# KENAR ETKİSİ DENETİMİ: veri sonu kesiği ve geleceğe bakma şüphesi (K2)

Bağımsız denetçi alt ajan, 21 Kasım 2026. Kod sha'ları: HEAD e0976cb (ORTAK_CETVEL, CETVEL2, YAPI_HEDEF, DUSUS_SONRASI, S6_TABAN değiştirilmedi).
Veri: yalnız /tmp/denetim_acik/V_ABD.pkl ve V_AVR.pkl (son gün 2022-12-30). Betikler: /tmp/denetim_kod/ (kenar.py, karsilastir.py, minbar.py, bolunme_ileri.py).
Yöntem: veri iki kez kesildi: KISA = tarih <= 2022-06-30, UZUN = tarih <= 2022-12-30. İki veride aynı fonksiyonlar çağrıldı
(DS.ds_veri -> C2.c2_panel(sinir = cetvel2_esik_v2.2.json); OC.oc_veri(k34 yok) -> OC.oc_panel; YH.yh_sinyaller(['Y1']) -> OC.oc_olay_hazirla;
DS.ds_baglam -> ds_ozellik_pazar -> ds_olay_kur). Yalnız giriş / sinyal günü <= 2022-06-30 (ve <= 2022-03-31) olan kayıtlar karşılaştırıldı.
AVR tam evren (575 hisse); ABD panel tam evren (1.361 hisse), Y1 / DS sinyalleri 200 hisselik rastgele örnek (tohum 7) + BFLY, LWLG, PAR.

## 0. Kısa hüküm

**Geleceğe bakma VAR, ama küçük ve sonuçtan bağımsız; geri kalanı kenar etkisi.** İki mekanizma veri ortasına kadar uzanıyor:

1. **Evren süzgeci `min_bar = 80`** (ORTAK_CETVEL.py satır 311, `if len(x) < E["veri"]["min_bar"]`): hisse, veri SONUNA kadar biriktirdiği
   geçerli bar sayısına göre panele alınıyor ya da tümden atılıyor. Kesik uzayınca 80 bara ulaşan yeni / seyrek işlem gören hisse panele giriyor;
   Lq'su 10 geçerli bardan sonra sonlu olduğu için öteki hisselerin **alt %20 likidite eşiğini** (satır 441) ve **5x3 kova sırasını** değiştiriyor.
   Üç gözlemin üçü de bundan. ABD'de KISA-UZUN farkı kesikten **141 bar önceye** (2021-12-08) kadar uzanıyor.
2. **Bölünme şüphesinin kalıcılık denetimi** (satır 364, `j = min(n - 1, i + B["geri_gun"])`): sıçrama günü i için C[i+10] kullanılıyor;
   havuz günü d'nin geçmiş penceresi [d-61, d-1] içindeki i için bu, d'den **9 bar sonrasına** kadar bakmak demek. Veri ortasında da var
   (KISA-UZUN karşılaştırması bunu göremez; ayrı sayıldı): 2015-2022'de ABD 425, AVR 6 hisse-gün.

Hisse başına sinyal tanımları (S6 'al' günleri, DS günleri, ATRP, F15, momentum, likidite) **nedensel**: KISA ile UZUN arasında kesikten önce
tek fark yok.

## 1. Üç gözlemin açıklaması

| Gözlem | Neden (doğrulandı) | Kod |
|---|---|---|
| (1) ABD kova sınırı havuzu açık veride 1.513.611, tam veride 1.513.661 (fark 50) | Açık veride (2022-12-30'a kadar) 80 geçerli bara ulaşmamış 12 hisse (2022 ikinci yarı halka arzları AMPX, ASPI, BAM, BHVN, BULL, CRBG, GEHC, MBC, MBLY, PRME, RXO + seyrek işlem gören HGRAF) min_bar süzgecinden düşüyor; tam veride 80 bara ulaştıkları için panelde. Açık veriye bu 12 hisse zorla eklenince `c2_kova_sinir` sayımı **tam olarak 1.513.661** çıkıyor (eklemesiz 1.513.611; HGRAF'sız 1.513.660). AVR'de aynı şey: P911.DE (Porsche, halka arz 29.09.2022, 65 geçerli bar) eklenince 753.910 -> **753.886** (v2.1 tam veri değeri birebir). | ORTAK_CETVEL.py 311 (evren), 426-441 (alt %20 likidite kesiti), 443-448 (qcut kova); CETVEL2.py c2_kova_sinir |
| (2) AVR FEV.L: açık veride Y1 olayı 2022-12-13, tam veriyle kurulan eski dosyada aynı kutunun olayı 2023-01-06 | Giriş günü 2022-12-14'te FEV.L alt %20 likidite eşiğinin hemen üstünde. Tam veride P911.DE panelde olduğu için o gün eşik kayıyor ve FEV.L `lik_alt` = True -> `havuz_disi` -> 12-13 sinyali olay olmuyor; 60 gün tekil yuvası boş kaldığı için sonraki S6 'al' günü 2023-01-06 olay oluyor. Doğrulama: UZUN veride FEV.L ok(2022-12-14) = True; P911.DE eklenince False, lik_alt True. | ORTAK_CETVEL.py 311, 441, 478-479 (havuz dışı), 499 (60 gün tekil) |
| (3) DS ANA 2022 sonu: ABD 4 yalnız yeni / 5 yalnız eski (BFLY, LWLG, PAR x3), AVR 1 / 1 (XPP.L) | Aynı evren mekanizması: tam evrende BFLY 12-12/12-14/12-19/12-22, LWLG 12-30, PAR 11-02 havuza GİRİYOR (açıkta alt %20'de), XPP.L 10-28 havuzdan ÇIKIYOR. Havuz üyeliği değişince DS günü olay olup olmuyor ve 15 bar ANA zinciri (DUSUS_SONRASI.py 543) kayıyor: bir gün düşünce sonraki gün ANA oluyor, ya da tersi. Ayrıca 2022-12-30 (son gün) sinyallerinin açık veride girişi yok (`giris_yok`, satır 475); eski dosyada 2023-01-03 girişiyle olay. | ORTAK_CETVEL.py 311, 441, 475; DUSUS_SONRASI.py 543 |

Not: tam veride, 2022 sonundaki sıçramalar için bölünme kalıcılığı 2023 fiyatlarıyla da karar verir (satır 364); bu üç gözlem için gerekmedi
(evren eklemesi sayıyı birebir tutturdu, FEV.L / BFLY / LWLG / PAR / XPP.L değişimleri evrenle yeniden üretildi).

## 2. KISA ve UZUN karşılaştırması (giriş / sinyal günü <= kesik)

| Kalem | AVR <= 06-30 | AVR <= 03-31 | ABD <= 06-30 | ABD <= 03-31 | En erken fark (kenar şeridi) |
|---|---|---|---|---|---|
| (a) havuz `ok` (hisse-gün) | 0 | 0 | 160 | 34 | ABD 2021-12-08 (141 bar) |
| (a) kova `H` (5 mom x 3 lik) | 0 | 0 | 495 | 102 | ABD 141 bar |
| (a) `lik_alt` (alt %20) | 0 | 0 | 163 | 35 | ABD 141 bar |
| (a) bölünme şüphesi `sup` (gün) | 0 | 0 | 1 (GORO 2022-04-20) | 0 | 50 bar (seyrek hisse: 10 GEÇERLİ bar kesiği aşıyor) |
| (a) `sup_gecmis`, M, Lq, ATRP, F15 | 0 | 0 | 0 | 0 | yok |
| (a) c2_kova_sinir maskesi (hisse-gün) | 747.882 / 747.882 | | 1.399.941 / 1.400.097 | | evren |
| (b) Y1 S6 'al' sinyalleri | 11.555 = 11.555 | 11.442 = 11.442 | 3.177 = 3.177 (örnek) | 3.144 = 3.144 | yok (nedensel) |
| (b) Y1 olayları (OC, 60 gün tekil) | 4.176 = 4.176; hücre / giriş farkı 0 | 4.107 = 4.107 | 1.207 = 1.207; hücre farkı 0 | 1.190 = 1.190 | örnekte yok; havuz farkı olan günlere düşen Y1 olayı olursa değişir |
| (c) DS günleri | 42.471 = 42.471 | 36.035 = 36.035 | 24.675 = 24.675 | 21.178 = 21.178 | yok (nedensel) |
| (c) DS havuz olayları | KISA 39.587 / UZUN 39.735: fark yalnız 2022-06-30 sinyalleri (`giris_yok`) | eşit | 18.242 / 18.321: 06-30 sinyalleri + AGEN 2022-06-02 (havuz) | eşit | 1 bar (giriş) + evren |
| (c) DS ANA | 4.016 / 4.031: yalnız 06-30 | eşit | 1.796 / 1.799: 06-30 + HYLN 06-01/02, PBI 05-25/06-13/06-16, NVTS 06-28/29 (ANA zinciri kaydı) | eşit (ANA farkı 0; hücre farkı 4) | ~25 bar (ANA) / 141 bar (hücre) |
| (d) CETVEL2 kova `KV` (ATRP x lik3 x F15) | 0 | 0 | 325 | 68 | ABD 141 bar |

ABD'de yalnız UZUN'da panelde olan 15 hisse (ACDC, AIRJ, ALVO, APLD, CRML, EMBC, ESAB, GCT, GFR, LION, LUNR, NUAI, OABI, SOUN, TNON): 2022-06-30'da 10-73
geçerli bar, 2022-12-30'da >= 80. OABI (ilk geçerli bar 2021-09-30, 06-30'da 73 bar) ve LUNR / GFR gibi seyrek işlem gören SPAC'ler fark şeridini
aylarca geriye taşıyor. **Şerit genişliği sınırsız**: 80 geçerli barı yıllara yayılan hisse için evren farkı o hissenin ilk barına kadar gider.
AVR'de KISA'da fark 0 (tek yeni hisse EXO.AS 06-30'da 0 bar); UZUN'da P911.DE etkisi 2022-10-14'ten (52 bar) başlıyor: 24 havuz, 98 kova (H), 51 KV hisse-gün.

Bölünme kalıcılığı (veri ortası, UZUN, 2015-2022; hisse barı başına d'de bilinenle tam bilgi karşılaştırması): ABD 425 hisse-gün / 56 hisse (219: tam
bilgiyle şüpheli değil ama d'de şüpheli görünürdü -> sıçrama sonradan geri döndüğü için havuzda; 206: tersi), AVR 6 hisse-gün (TEP.PA, MTRO.L).
Olaylara dokunan: AVR 0; ABD örneğinde Y1 0, DS havuz 4 (ASTS 2021-06), DS ANA 0.

## 3. HÜKÜM

- **Geleceğe bakma VAR (iki mekanizma), etkisi küçük.** (i) min_bar evren süzgeci, havuz ve kova sınırlarını d'de bilinmeyen evrenle kuruyor.
  Bu, sinyalin getirisinden bilgi taşımaz (eşik ve sıra kayması); hissenin kendisi için hayatta kalma koşullaması (K7 ile aynı yön) taşır.
  Büyüklük ABD'de 6 ayda yaklaşık 160 havuz hisse-günü / 1,4 milyon (%0,01); olay düzeyinde tek tük olay ve hücre kayması. (ii) Bölünme
  kalıcılığı d+9'a kadar fiyata bakıyor: getiriyle ilişkili (sıçramanın geri dönüp dönmediği), ama 7 yılda ABD 425 / AVR 6 hisse-gün, olay
  düzeyinde örnekte 4 DS havuz olayı. Ölçüm sonucunu (hücre ortalaması, BH kararı) değiştirecek büyüklükte DEĞİL; yine de K2 'EVET' yazılı
  beyanlar (ORTAK_CETVEL.py 148 'kovalar yalnız d günü bilinenle'; bölünme 'geçmiş pencere [d-61, d-1]') harfiyen doğru değil.
- **Kenar etkisi (geleceğe bakma değil):** son bar sinyalinin girişi yok (satır 475; seyrek hissede 10 güne kadar boşluk), 60 / 15 gün tekil
  zinciri yalnız ileri doğru kayar (geriye taşımaz). Bunlar 'veri sonunda henüz ölçülemeyen olay'dır.
- **Hisse başına tanımlar nedensel:** S6 'al', DS günleri, ATRP, F15, M, Lq iki kesikte birebir. c2_prefix / kt_prefix testleri hisse serisini t'de keser
  ama evreni kesmez; bu yüzden (i) ve (ii)'yi yakalayamaz.

**Kasa ve yürüyen ileri test için öneri (kod değiştirmedim):**
1. Blok sınırında karşılaştırma yapılırken (açık / eski dosya, ya da blok k verisi ile blok k+1 verisi) fark ancak şu iki şeritte kabul edilsin:
   (a) son 10 birleşik takvim günü (giriş boşluğu + bölünme kalıcılığı), (b) kesikte < 80 geçerli barlı hisselerin varlığından etkilenen günler.
   (b) sınırsız olduğu için kalıcı çözüm koddadır (madde 3).
2. Yürüyen testte her bloğun olayları O BLOĞUN kesik verisiyle bir kez kurulup dondurulsun; sonraki blok, önceki blokların olaylarını uzun veriyle
   YENİDEN kurmasın. 60 gün tekil zinciri bloklar arası, önceki bloğun dondurulmuş son tutulan olayından devam etsin; son 10 gün içindeki
   sinyaller (girişi blok dışına düşen) sonraki bloğa devredilsin.
3. Bir sonraki sürümde (ön kayıtla; ölçü değişikliği sayılır): min_bar süzgeci kaldırılıp yerine hisse, 80. geçerli barının ertesi gününden itibaren
   evrene alınsın (`evren_bas` mekanizması zaten var, satır 426); bölünme kalıcılığı d günü için en çok d-1'e kadar bilinen bara bakılarak
   (ya da 10 bar dolmadan oran tutan sıçrama 'şüpheli' sayılarak) hesaplansın. Bu iki değişiklikle KISA-UZUN farkı yalnız son giriş günü şeridine iner.
4. Şimdiki koşunun sonuçları bu yüzden geçersiz sayılmamalı; raporda 'K2: evren min_bar ve bölünme kalıcılığı küçük ileri bilgi taşır (%0,01 düzeyi)' notu yeter.

## 4. HATA

- **H-a (geleceğe bakma, veri / evren):** ORTAK_CETVEL.py 311 `min_bar` hisseyi veri sonuna kadarki geçerli bar sayısıyla seçiyor; havuz (alt %20 likidite),
  kova ve CETVEL2 kova sınırları d'de bilinmeyen evrenle kuruluyor. Gözlem (1), (2), (3)'ün nedeni. Kenar şeridi sınırsız (ABD örneğinde 141 bar).
- **H-b (geleceğe bakma, küçük):** ORTAK_CETVEL.py 364 bölünme kalıcılığı C[i+10]; havuz günü d için d+9'a kadar fiyat. ABD 425 / AVR 6 hisse-gün (2015-22).
- **H-c (ifade / kontrol beyanı):** OC_ESIK K2 'EVET' metni (satır 148) ve bölünme tanımı 'geçmiş pencere [d-61, d-1]' bu iki ileri bilgiyi söylemiyor;
  prefix testleri yalnız hisse serisini kestiği için bunları yakalayamıyor (K11 denetiminin kör noktası).
- Yanlış alarm olmayan: Y1 ve DS sinyal tanımlarında, ATRP / F15 / M / Lq'da geleceğe bakma yok.

## 5. KONTROL LİSTESİ

| Madde | Durum | Kanıt |
|---|---|---|
| K2 geleceğe bakma | HAYIR (iki küçük ileri bilgi bulundu) | H-a, H-b; KISA-UZUN tablosu; evren ekleme ile gözlemler birebir üretildi |
| K3 geçerli bar | EVET | oc_veri_hazirla / sy_veri_hazirla H>L, V>0; ABD sparse hisselerde 'geçerli bar' sayısı evren farkını büyütüyor (H-a) |
| K4 tekilleştirme | EVET (kenar) | 60 gün (OC 499) ve 15 bar (DS 543) zinciri yalnız ileri kayıyor; KISA'da 03-31 öncesi Y1 / DS ANA kümeleri eşit |
| K10 ayrıştırma | EVET | Elle doğrulama: FEV.L 2022-12-14 ok / lik_alt; BFLY, LWLG, PAR, XPP.L flip günleri; P911.DE 65 bar, HGRAF 27 bar |
| K11 yeniden üretim | EVET | 1.513.611 ve 753.910 açık veriden aynen; 1.513.661 ve 753.886 tam veri sayıları evren eklemeyle birebir yeniden üretildi |
| K13 süreç | EVET | .py / defter / kart / kasa dosyalarına dokunulmadı; yalnız bu dosya commit; betik ve ara veri /tmp/denetim_kod; nice 19, tek süreç; sızıntı yok |
