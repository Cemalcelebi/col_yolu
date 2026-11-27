# GT7 ÖN KAYIT — ÇÖL-K2 x PİYASA REJİMİ: genişlik dipteyken oluşan bölgelerin sonraki 15 barı, aynı günün evreni ve oynaklık eşi karşısında (27 Kasım 2026)

DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil). Bu ölçüm 'çöl tuttu / tutmadı / iz' sorusunu yanıtlamaz; yalnız beş şartlı dedektörün bulduğu bölgelerin, piyasa genişliği dipteyken oluştuklarında, aynı gün öteki hisselerden iyi gidip gitmediğini sayar.

İş tanımı: arastirma_cikti/goz_tespit/GT7_IS_TANIMI.md (ana model). Bu dosya getiri hesaplanmadan ÖNCE commit + push edilir; `python GOZ_TESPIT.py k2rejolc` bu dosyanın commit + push edilmiş olmasını (gt_kapi_commit), KONTROL LİSTESİ'nin dolu olmasını (IZ_KARNE.ik_kontrol_kapisi), gt7_sayim.json'daki kod / eşik sha'sının şimdiki kodla aynı olmasını, G40 dosyası sha'sının sayımdakiyle aynı olmasını, dört sha'nın bu dosyada yazılı olmasını ve dip dönemlerinin sayımdakiyle aynı olmasını denetler; gt7_ozet.json varsa ikinci koşu durur.

## 1. Mühürler
- Kod commit: 142f22c (2026-11-27 13:13:17 UTC; GOZ_TESPIT.py bölüm 13 + test_goz_tespit.py, 45 / 45 test).
- GOZ_TESPIT.py sha256 (kod_sha): 3f9d2a9872c7267aa01d70a589f01faf952ae5acf7367a8aaf35237e49fbbb8b
- GT7 eşik sha (GT_K2R sözlüğü; gt_k2r_esik_sha): c0841e02865e59f0867f03c81fa815a0a08be6aa1691ad60c5ddca53088f7839
- Olay dosyası /root/.kasa/ham/goz_tespit/k2/k2_olay.pkl sha256 (GT5 ile aynı, assert): e0ef464c8159b1f403ba03537352e939ea699b3a2a5c6148366485eae99cbf55
- Yeniden kurulan G40 serisi /root/.kasa/ham/goz_tespit/k2/k2r_g40.pkl sha256: 46ee92ea37592af607cc8c67d49e29bca37b89fab9ca951052ad14f7c5afc10a
- YO2 kaynak dosyaları: yo2_piyasa_ABD.pkl sha256 74df4b39654d967e1d7e1601d510da9a42bc4b5b0f718a8461bfb27899881153; yo2_sayim.json sha256 47742d0aa5cbaefaa88938168bb823f55c32448a7e82ca298571921a1e364d2f
- Getirisiz sayımlar: arastirma_cikti/goz_tespit/gt7_sayim.json (bu commit'te; `python GOZ_TESPIT.py k2rejsay`, 2026-11-27 13:17 UTC).

## 2. Rejim serisi ve kesim (Ç257'den AYNEN)
- SERİ: G40(w) = ABD haftalık evrende (TEZGÂH 2 P2 havuzu, YO.yo2_evren) kapanışı kendi 40 haftalık ortalamasının üstünde olan hisse payı; ISO hafta başına, SMA40'ı tanımlı ve evren bayraklı hisselerde, en az 30 hisse (YO2_ESIK 'ozellik' G40). Veri MUM_IZI.mi_veri('ABD', MUM_IZI_HAFTALIK.MH_YOL['tam']) -> MUM_IZI_V2.mv_haftalik_panel; hacim kullanılmaz.
- YENİDEN KURULDU (gt_k2r_g40_kur; YO2 yapı taşları yo2_evren / yo2_ozellik / yo2_hno ile, 2015-01 .. 2022-12, 416 hafta): YO2'nin sakladığı seriyle 414 ortak haftada (2016-22'de 363) en büyük fark 0,0 ve kesit sayıları aynı (assert).
- GÜNLÜK KULLANIM: günlük seri yok; gün D, D'nin ISO haftasından KÜÇÜK son haftanın G40'ını kullanır (normalde bir önceki hafta; o hafta D'den önce kapanmış). Son hafta 3 haftadan eskiyse rejim YOK (2016-22 takviminde hiç yok, assert).
- KESİM: G40 <= 0,276760218650567. Kaynak: /root/.kasa/ham/yukselis_oncesi/yo2/yo2_sayim.json kesim.ABD.G40 (YO2_ON_KAYIT.md satır 26: 'G40 <= 0.276760 (ABD 2016-22 piyasa haftası %10; n 362)'; YO2_RAPOR.md 'G40 <= 27,7%'). Kod kesimi HESAPLAMAZ; GT_K2R'de sabit sayıdır, k2rejsay / k2rejolc yo2_sayim.json ile birebir olduğunu denetler (test: seri değişince kesim aynı).
- NOT (HATA olarak raporlanacak, kesim değişmedi): iş tanımı kesimin '2000-2015 verisinden' sabitlendiğini yazıyor; YO2'de kesim 2016-22 haftalık G40 dağılımının %10'udur, 2000-2015 ise sınama dönemiydi. Bu yüzden 2016-22'de DİP haftası payı yapı gereği ~%10'dur (364 haftanın 37'si). Kesim getiriden değil yalnız G40 dağılımından gelir; kesim iş tanımı gereği değiştirilmedi.
- DİP günü = önceki hafta G40 <= kesim. AYRI DİP DÖNEMİ: DİP günleri takvim sırasıyla; ardışık iki DİP günü arasında en az 20 işlem günü varsa (takvim sıra farkı >= 21) yeni dönem. Takvim = 2016-01-01 .. 2022-12-31 arasında açık ABD serilerinin en az 100'ünde bar olan günler (1.762 gün).

## 3. Getirisiz sayımlar (k2rejsay; gt7_sayim.json)

DİP günü: 177 / 1.762 (2016-19: 51 / 1.006; 2020-22: 126 / 756). DİP haftası (2016-22): 37 / 364.

| dip dönemi | ilk gün | son gün | DİP günü |
|---|---|---|---|
| 0 | 2016-01-11 | 2016-02-26 | 33 |
| 1 | 2018-12-17 | 2019-01-11 | 18 |
| 2 | 2020-03-16 | 2020-05-22 | 44 |
| 3 | 2022-05-02 | 2022-07-29 | 53 |
| 4 | 2022-09-06 | 2022-10-21 | 29 |

Ayrı dip dönemi: 5 (2016-19'da 2: dönem 0 ve 1; 2020-22'de 3: dönem 2, 3, 4).

Olay sayıları (dondurulmuş k2_olay.pkl, ABD; hücre giriş t + 1 tarihine göre; rejim bölge sonu günü t'ye göre; 15. barı 2022 sonrasına düşen KESIK olacak, sonraki ölçümde STOP_ALTI da düşer):

| kol | hücre | rejim | olay | hisse | 15. bar 2022 sonrası | olayı olan dip dönemi (dağılım) |
|---|---|---|---|---|---|---|
| K2 | ABD 2016-19 | DİPTE | 60 | 58 | 0 | 2 (d0 29, d1 31) |
| K2 | ABD 2016-19 | DİP DIŞI | 889 | 462 | 0 | — |
| K2 | ABD 2020-22 | DİPTE | 565 | 502 | 0 | 3 (d2 93, d3 374, d4 98) |
| K2 | ABD 2020-22 | DİP DIŞI | 1.759 | 985 | 29 | — |
| YMSB | ABD 2016-19 | DİPTE | 140 | 135 | 0 | 2 (77, 63) |
| YMSB | ABD 2016-19 | DİP DIŞI | 2.479 | 706 | 0 | — |
| YMSB | ABD 2020-22 | DİPTE | 1.366 | 933 | 0 | 3 (195, 830, 341) |
| YMSB | ABD 2020-22 | DİP DIŞI | 4.445 | 1.484 | 144 | — |
| Y | ABD 2016-19 | DİPTE | 209 | 200 | 0 | 2 (96, 113) |
| Y | ABD 2016-19 | DİP DIŞI | 3.585 | 832 | 0 | — |
| Y | ABD 2020-22 | DİPTE | 2.153 | 1.375 | 0 | 3 (551, 1.080, 522) |
| Y | ABD 2020-22 | DİP DIŞI | 6.313 | 1.684 | 199 | — |

Rejimi YOK olan olay: 0.

## 4. Sonrası tanımları (GOZ_TESPIT.GT_K2R; sonuçtan sonra değişmez)
- R15: GT5 / Ç271 ile aynı fonksiyon (gt_k2_olay_olc: MUM_IZI_HAVUZ.hv25_uygun m = L + hv25_olc_dizi): giriş = t + 1 barı açılışı, R15 = t + 15 barı kapanışı / giriş - 1; durum TAMAM / KESIK / DIS / STOP_ALTI, yalnız TAMAM ölçülür.
- EVREN (aynı gün D = olayın t günü): o gün girişi yapılabilen bütün ABD hisseleri; pencere paneli evren şartları L = 20 ile, her gün: seri indeksi k >= 139 (s = k - 19 >= 120), D 2016-01-01 .. 2022-12-31, kilitli pay [k - 19, k] <= 0,20, gövdesiz bar payı (O = C) <= 0,30, ATRP20 sonlu, hv25_uygun(m = 20) (k + 15 veride ve <= 2022-12-31, giriş tarihi dönemde, giriş > 20 bar dibi x 0,98). Olayın kendi hisse-günü (TAMAM) her zaman evrende (L = 20 şartını geçmese bile; 'zorla' bayrağı). Evren R15'i aynı fonksiyon (hv25_olc_dizi).
- SEÇİM = R15 - aynı gün evren R15 ortalaması (evren >= 30 hisse; azsa olay SEÇİM'den düşer).
- SEÇİM_O = R15 - aynı gün aynı ATRP20 beşliği evren R15 ortalaması (>= 5 hisse; azsa olay ES_AZ olur, ölçülmez). ATRP20 = YO.yo_hisse_ozellik formülü (olay satırlarında k2_olay ATRP20 ile göreli 1e-4 içinde, assert); beşlik sınırları gt5_olay.json besli_sinir ABD (dondurulmuş; dönem giriş tarihine göre); olayın beşliği kendi evren satırından (GT5 beşliğiyle uyuşmayan sayısı raporda).
- SİMETRİK +%5: giriş barından 15. bara High >= giriş x 1,05 mi önce, Low <= giriş x 0,95 mi (gt_k2k_simetrik; STOP YOK). Aynı barda ikisi BELİRSİZ: paydan ve paydadan çıkar. Olay payı = BELİRSİZ olmayan olaylarda +%5 önce payı; taban = aynı olaylar için aynı gün aynı beşlik evreninin BELİRSİZ olmayan hisselerinde +%5 önce payı, olaylar üzerinden ortalama; fark = pay - taban.
- BOOTSTRAP: SEÇİM / SEÇİM_O ortalaması, küme bootstrap %95, 2.000, np.random.default_rng(7) her çağrıda yeniden, KISA_UFUK.ku_boot. DİPTE küme = dip dönemi; DİP DIŞI küme = giriş ayı (bilgi). Küme < 5 ise GA hesaplanmaz, ÖLÇÜLEMEDİ.
- Hücreler: ABD 2016-19 ve ABD 2020-22, her biri DİPTE ve DİP DIŞI; kollar K2 (ANA), YMSB, Y.

Tanım yorumları (iş tanımı açık bırakmıştı; sonuç görülmeden):
1. 'Evren şartları pencere paneliyle aynı': panel pencereleri her hissede 5 barda bir olduğundan aynı gün için panel satırı yok; şartlar her gün L = 20 penceresiyle uygulandı ve 'girişi yapılabilen' hv25_uygun(m = 20) (GT5 T1 günleriyle aynı kural) ile tanımlandı.
2. 'Olayın kendi hissesi dahil': olay günü evren şartını L = 20 ile geçmese de evrene eklenir (üç kolun TAMAM olay günleri; evren bütün kollar için aynı).
3. 'Aralarında en az 20 işlem günü' = iki DİP günü arasındaki işlem günü sayısı >= 20 (sıra farkı >= 21).
4. DİP DIŞI hücreleri için karar kuralı yazılmadığından BİLGİ olarak okunur; GA'ları ay kümeli.
5. Sonuç etiketi: ANA kol DİPTE hücrelerinden biri ÖLÇÜLEMEDİ ise sonuç 'ÖLÇÜLEMEDİ' (CLAUDE.md: güç yetersizse İZ DEĞİL / EMARE DEĞİL yazılmaz).

## 5. KARAR KURALI (önceden; değişmez)
- DİPTE hücresi TUTAR <=> n >= 30 VE olayı olan ayrı dip dönemi >= 5 VE SEÇİM_O ortalamasının dip dönemi kümeli bootstrap %95 GA alt ucu > 0 VE medyan SEÇİM_O > 0 VE simetrik +%5 farkı > 0. n < 30 ya da dip dönemi < 5 ise ÖLÇÜLEMEDİ. Aksi TUTMAZ.
- 'EMARE (yaşayan evren)' <=> ANA kol (K2) DİPTE hücresi ABD 2016-19 VE ABD 2020-22'de TUTAR. Biri ÖLÇÜLEMEDİ ise 'ÖLÇÜLEMEDİ'; aksi 'EMARE DEĞİL'.
- Ek okuma (karar değil): DİPTE - DİP DIŞI SEÇİM_O farkı (kol x dönem); K2 - Y DİPTE SEÇİM_O farkı (beş şart yalnız yere göre bir şey katıyor mu).
- K7 uyarısı zorunlu: evren bugün yaşayan hisseler; dip dönemlerinde batanların yokluğu hem olayı hem aynı gün evren ortalamasını yukarı çeker; yer şartı en az 2 kat düşmüş hisseleri seçtiği için olay tarafında daha büyük olabilir. Artı sonuç en fazla 'EMARE (yaşayan evren)'.
- Sağlama (K11): K2 ABD 2020-22 DİPTE hücresinin SEÇİM_O ortalaması ve n'i ham seriden (açık ABD verisi) bağımsız kısa kodla (GOZ_TESPIT / MUM_IZI_HAVUZ ölçü fonksiyonları kullanılmadan, düz döngü) yeniden üretilir; ayrıca satır dosyasından gün ortalamaları denetlenir.

## 6. ÖNCEDEN BELLİ OLAN (sonuç görülmeden yazıldı)
- Olayı olan ayrı dip dönemi her kolda 2016-19'da 2, 2020-22'de 3 (< 5). Bu yüzden ALTI DİPTE hücresinin hepsi (K2, YMSB, Y x iki dönem) kural gereği ÖLÇÜLEMEDİ olacak ve küme bootstrap GA'sı hesaplanmayacak (küme < 5). ANA kol için sonuç yapısal olarak 'ÖLÇÜLEMEDİ'dir; bu veriyle 'EMARE' olanaksızdır.
- K2 ABD 2016-19 DİPTE hücresinde en çok 60 olay var ve bunlar iki dönemde (2016 başı 29, 2018 sonu 31) toplanıyor; 2020-22 DİPTE olaylarının %66'sı (374 / 565) tek dönemde (2022 Mayıs-Temmuz).
- Ölçüm yine BİR KEZ koşulur; bütün hücrelerin ortalamaları, medyanları ve simetrik payları BİLGİ olarak yazılır; nokta değerleri az sayıda takvim dönemine dayandığı için yorum 'ölçülemedi' çerçevesinde kalır. DİP DIŞI hücreleri ay kümeli GA ile bilgi.
- 2016-22'nin beş dip dönemi bütün kollarda aynı (rejim hisseden bağımsız); dönemleri birleştiren tek bir 2016-22 hücresi iş tanımında yok, açılmaz.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | aynı giriş günü (aynı t günü, t + 1 açılışı), aynı R15 geometrisi (hv25_olc_dizi; stop yok) ve aynı rejim: SEÇİM = aynı gün bütün girişi yapılabilen evren, SEÇİM_O = aynı gün aynı ATRP20 beşliği (Ç271 dersi: çöl hisseleri en oynak beşlikte); simetrik +%5 stop'suz (GT5 HATA 3 stop geometrisi farkı yok); konum / kutu genişliği eşlenmedi (GT6 HATA 5) ama R15 kırılım yönü gibi mekanik olarak konuma bağlı değil, raporda not; 200 rastgele eş portföy yerine iş tanımındaki aynı gün evren ortalaması kullanıldı |
| K2 | geleceğe bakma | EVET | rejim günü D yalnız D'nin haftasından önce kapanmış haftanın G40'ı (gt_k2r_rejim; test_k2r_rejim_yalniz_onceki_hafta: D'nin haftası ve sonrası bozulunca aynı, önceki hafta değişince ya da seri ileri kaydırılınca değişir); kesim sabit sayı (test_k2r_kesim_sabit); olaylar dondurulmuş (sha assert); evren şartları k'ye kadarki barlardan; beşlik sınırları dondurulmuş; veri <= 2022-12-31 (gt_kesik_kapi, yo_kesik_kapi) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar serisi (açık kopya; H > L, V > 0); evrende kilitli pay <= 0,20 ve gövdesiz pay <= 0,30 (L = 20); haftalık G40 yalnız geçerli günlerden kurulan haftalık barlarla (mv_haftalik_panel) |
| K4 | tekilleştirme | EVET | olaylar GT5 tekilleştirmesiyle (kol + hisse başına 40 bar); evren satırı hisse-gün başına bir; çıkarım dip dönemi kümeli (bağımsız birim = dip dönemi, 2 / 3 < 5 -> ÖLÇÜLEMEDİ); medyan SEÇİM_O karar şartında |
| K5 | giriş fiyatı | EVET | giriş = t + 1 barı açılışı hem olayda hem evrende (hv25_olc_dizi g0 = gi[t + 1]); sinyal günü kapanışı kullanılmaz |
| K6 | veri birimi | EVET | tek kip: açık kopya (bölünme düzeltmeli, pencere paneliyle aynı seri; olay t tarihi ve ATRP20 seriyle assert); getiriler oran; G40 YO2 haftalık tam kopyasından, YO2 serisiyle birebir (en büyük fark 0) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: dip dönemlerinde (2018 sonu, 2020 Mart, 2022) batanlar yok -> olay ve evren ortalaması yukarı yanlı, olay tarafında yer şartı yüzünden daha büyük olabilir; raporda zorunlu K7 uyarısı; artı sonuç en fazla EMARE (yaşayan evren); batanlar dahil sınama Aralık |
| K8 | örneklem ve dönem | EVET | n < 30 ya da olayı olan dip dönemi < 5 ÖLÇÜLEMEDİ; altı DİPTE hücresinin hepsinin ÖLÇÜLEMEDİ olacağı bu dosyada önceden yazıldı (dip dönemi 2 / 3); iki dönem ayrı hücre; karar yalnız ANA kol, BH gerekmez |
| K9 | ön kayıt | EVET | bu dosya kod sha, eşik sha, olay sha, G40 sha ve getirisiz sayımlarla getiriden önce commit + push; k2rejolc gt_kapi_commit + ik_kontrol_kapisi + sha / dip dönemi denetimiyle başlar, ikinci koşu durur |
| K10 | ayrıştırma | EVET | G40 yeniden kurulumu YO2 serisiyle 414 haftada birebir; kesim yo2_sayim.json ile birebir; olay ATRP20 evren formülüyle göreli 1e-4 içinde ve olay R15 evren satırıyla aynı (assert); öbek, rejim, SEÇİM ve SEÇİM_O elle küçük örneklerle test |
| K11 | yeniden üretim | EVET | K2 ABD 2020-22 DİPTE SEÇİM_O ve n ham seriden bağımsız kısa kodla yeniden üretilecek (GT7_RAPOR'da); rapor sayıları gt7_ozet.json'dan |
| K12 | ifade | EVET | başlık DEDEKTÖRÜN BULDUĞU BÖLGELER; 'çöl tuttu / iz' cümlesi kurulmaz; ÖLÇÜLEMEDİ hücrelerde nokta değerler bilgi; sayı ile yorum ayrı; sonuç olduğundan güçlü yazılmaz |
| K13 | süreç | EVET | çakışma kapısı korundu (test_cakisma_kapisi); yalnız GOZ_TESPIT.py, test_goz_tespit.py ve GT7_ / gt7_ dosyaları commit; yasak defter dosyalarına ve GT5 / GT6 dosyalarına dokunulmadı; MI._mi_yaz sızıntı taraması; kod değiştiği için Colab'da çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; dedektör bölgeleri Cemal'in görsel onayını bekliyor |
