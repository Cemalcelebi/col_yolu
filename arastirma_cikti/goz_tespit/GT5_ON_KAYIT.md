# GT5 ÖN KAYIT — ÇÖL-K2 (beş şart) olaylarının sonrası (27 Kasım 2026)

DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor; kalıp hükmü değil). Bu ölçüm 'çöl tuttu / tutmadı / iz' sorusunu yanıtlamaz; yalnız beş şartlı dedektörün bulduğu bölgelerden sonra ne olduğunu sayar.

İş tanımı: arastirma_cikti/goz_tespit/GT5_IS_TANIMI.md (ana model). Bu dosya getiri hesaplanmadan ÖNCE commit + push edilir; `python GOZ_TESPIT.py k2olc` bu dosyanın commit + push edilmiş olmasını, KONTROL LİSTESİ'nin dolu olmasını (IZ_KARNE.ik_kontrol_kapisi), olay dosyası sha'sının ve kod sha'sının aşağıdakiyle aynı olmasını denetler; gt5_sonuc.json varsa ikinci koşu durur.

## 1. Mühürler
- Kod commit: 8a11e6e (GOZ_TESPIT.py + test_goz_tespit.py; ÇÖL-K2 bölümü 11).
- GOZ_TESPIT.py sha256 (kod_sha): b39891a0c134d44b99f93cbd5fb955a4250474d08128ceac489befd7ab798e52
- ÇÖL-K2 eşik sha (GT_K2 + GT_K2_OLAY + GT_K2_OLC): 457e7ce7f0a2cc15f92651457209471f0b4213fe85e2a052a87538f8b65bbebe
- Olay dosyası /root/.kasa/ham/goz_tespit/k2/k2_olay.pkl sha256 (olay_sha): e0ef464c8159b1f403ba03537352e939ea699b3a2a5c6148366485eae99cbf55
- Getirisiz sayımlar: arastirma_cikti/goz_tespit/gt5_olay.json (bu commit'te).

## 2. Beş şart ve eşikler (goz2 araçlarından AYNEN; GOZ_TESPIT.GT_K2)
- Y YER: kutu yüksekliği / uzak görünüm (önceki 120 bar + bölge) yüksekliği <= 0,22; kutu ortası uzak görünümün alt %35'inde; önceki 120 barın tepesi / kutu tavanı >= 2.
- M KÜÇÜK MUM: bölge medyan mum boyu (H - L) / önceki 120 bar medyanı <= 0,80 ve medyan gövde oranı <= 0,80.
- S DİP SAVUNMASI: dibi kutunun alt %25'ine dokunan barlar; aralarında >= 3 bar olanlar ayrı dokunuş; >= 3 ayrı dokunuş ve ilk-son dokunuş arası >= bölge uzunluğunun %25'i.
- B DERİN DİP BİTTİ: bölge + önceki 20 barın en derin dibi bölge sonundan en az 5 bar geride.
- Z DİP PARABOLÜ: bölgenin son üçte biri (en az 10 bar) mum diplerine ikinci derece eğri; kavis > 0, sonda eğim > 0, eğrinin dibi x in [-1; 0,5], son 3 barın dibi bölümün en derin dibinin üstünde, son üçte birin dibi bölüm aralığının >= %5 üstünde, r2 >= 0,60, yükseliş >= 0,25 (goz2/dip_parabol_kural.json seçilen basamak).
- Kollar: K2 = beşi (ANA); YMSB = parabolsüz dört şart; Y = yalnız yer (karşılaştırma).

## 3. İŞ A doğrulaması (getirisiz)
- goz2 ile birebir: `python GOZ_TESPIT.py k2esles` -> GT3 32 / 32 sayfa, GT4 20 / 20 sayfa beş şart + K2 + YMSB + dokunuş sayısı AYNI (goz2/k2_onkayit.json).
- Sentetik birebir: goz2/k2.py k2 ile gt_k2, 660 rastgele pencerede aynı (test_k2_goz2_ile_birebir_sentetik); GT_K2 sözlüğü goz2 K2 ve dip_parabol_kural.json ile aynı.
- Yapay dip tipleri (goz2/dip_sina.py üreteci, tohum 28, tip x gürültü başına 400): geçme payı U dönüş 1,00 / 1,00 (sınır >= 0,90); U + sonda daha derin dip 0 / 0; düz 0 / 0; düzenli aşağı kayma 0 / 0; yavaşlayan düşüş 0 / 0; kubbe 0 / 0; rastgele yürüyüş 0,065 / 0,043 (sınır <= 0,10). Hepsi sınırda.
- Beş şart yapay pozitif ve negatifler: pozitif seri beşini sağlar (21 gürültü tohumu); mum iri -> M 0; tek dokunuş -> S 0; son 3 mumda yeni dip -> B 0 ve Z 0; tepede sıkışma -> Y 0. Elle örnekler (savunma, dip bitti, yer / küçük mum, tam parabol) ve 'bölge sonundan sonrası bozulunca sonuç aynı' testleri geçti. test_goz_tespit.py 26 / 26 (eski 17 + yeni 9).
- Ön eleme: YER vektörle (gt_k2_yer_vek), geçenlerin hepsinde gt_k2 YER = 1 (assert), geçmeyenlerden pazar başına 300 pencerede gt_k2 YER = 0 (assert); hata 0.

## 4. Olay evreni ve getirisiz sayımlar (k2olay)
Evren: GOZ_TESPIT pencere paneli (L 20 / 40 / 80; t % 5 == 0), pencere sonu 2016-01-01 .. 2022-12-31, s >= 120, kilitli pay <= 0,20, gövdesiz bar payı <= 0,30. Evren pencere / hisse: ABD 3.332.810 / 4.246; AVR 553.811 / 569; BIST 354.064 / 457. YER'i geçen pencere: ABD 110.007, AVR 2.061, BIST 5.439; beşi (tekilleştirmeden önce): ABD 5.741, AVR 92, BIST 327.
Tekilleştirme: kol ve hisse başına (t, L) artan sırada; son tutulan pencere sonundan >= 40 bar sonra biten tutulur (ilk görülen). Hücre = giriş (t + 1 barı) tarihine göre dönem.

| kol | hücre | olay | hisse | 15. bar 2022 sonrası | L 20 / 40 / 80 |
|---|---|---|---|---|---|
| K2 | ABD 2016-19 | 949 | 480 | 0 | 557 / 246 / 146 |
| K2 | ABD 2020-22 | 2.324 | 1.209 | 29 | 1.430 / 625 / 269 |
| K2 | AVR 2016-19 | 16 | 10 | 0 | 8 / 4 / 4 |
| K2 | AVR 2020-22 | 37 | 28 | 0 | 18 / 13 / 6 |
| K2 | BIST 2016-19 | 79 | 48 | 0 | 41 / 25 / 13 |
| K2 | BIST 2020-22 | 93 | 70 | 1 | 56 / 23 / 14 |
| YMSB | ABD 2016-19 | 2.619 | 723 | 0 | 1.882 / 397 / 340 |
| YMSB | ABD 2020-22 | 5.811 | 1.622 | 144 | 4.125 / 1.004 / 682 |
| YMSB | AVR 2016-19 | 34 | 16 | 0 | 23 / 5 / 6 |
| YMSB | AVR 2020-22 | 113 | 59 | 2 | 82 / 17 / 14 |
| YMSB | BIST 2016-19 | 191 | 76 | 0 | 125 / 31 / 35 |
| YMSB | BIST 2020-22 | 248 | 114 | 1 | 157 / 46 / 45 |
| Y | ABD 2016-19 | 3.794 | 864 | 0 | 3.195 / 322 / 277 |
| Y | ABD 2020-22 | 8.466 | 1.920 | 199 | 7.179 / 651 / 636 |
| Y | AVR 2016-19 | 69 | 28 | 0 | 54 / 8 / 7 |
| Y | AVR 2020-22 | 196 | 81 | 1 | 168 / 14 / 14 |
| Y | BIST 2016-19 | 292 | 96 | 0 | 226 / 28 / 38 |
| Y | BIST 2020-22 | 323 | 123 | 1 | 244 / 30 / 49 |

Girişi 2023'e düşen (hücre 'yok') K2 2, YMSB 11, Y 12 olay ölçülmez. 15. barı 2022 sonrasına düşen olaylar KESIK durumuyla ölçülmez.

ÖNCEDEN BELLİ OLAN: ANA kolun AVR 2016-19 hücresinde en çok 16 olay var (< 30) -> bu hücre ÖLÇÜLEMEDİ olacak; karar kuralı dört karar hücresinin dördünü istediği için ANA kolda 'EMARE' sonucu bu veriyle yapısal olarak olanaksızdır. Ölçüm yine bir kez koşulur ve bütün hücreler yazılır; ABD hücreleri ve kollar arası fark BİLGİ olarak okunur. Bu not sonuç görülmeden yazıldı.

ATRP20 beşlik sınırları (getirisiz, evren pencerelerinden, gt5_olay.json besli_sinir): ABD 2016-19 0,0183 / 0,0247 / 0,0330 / 0,0494; ABD 2020-22 0,0262 / 0,0364 / 0,0512 / 0,0755; AVR 2016-19 0,0150 / 0,0186 / 0,0226 / 0,0291; AVR 2020-22 0,0202 / 0,0259 / 0,0325 / 0,0433; BIST 2016-19 0,0255 / 0,0324 / 0,0399 / 0,0516; BIST 2020-22 0,0333 / 0,0413 / 0,0499 / 0,0626.

## 5. Sonrası tanımları (GOZ_TESPIT.GT_K2_OLC; tanımlar MUM_IZI_HAVUZ / KISA_UFUK fonksiyonlarıyla, yeniden yazılmadı)
- Giriş = t + 1 barı açılışı; R15 = t + 15 barı kapanışı / giriş - 1; R5 bilgi (MUM_IZI_HAVUZ.hv25_olc_dizi).
- Stop: olay = bölge [s, t] dibi x 0,98 (hv25_olc_dizi m = L); taban günü = önceki 20 bar dibi x 0,98 (m = 20).
- HEDEF5 / HEDEF10 = giriş barından 15. bara kadar High >= giriş x 1,05 / 1,10, stop'tan (Low <= stop) ÖNCE; aynı barda ikisi = stop (hv25_olc_dizi aynen; ayrı stop'lu hedef fonksiyonu yazılmadı, mevcut olan kullanıldı).
- Uygunluk (olay ve taban aynı kural, MUM_IZI_HAVUZ.hv25_uygun): t + 15 veride ve tarihi <= 2022-12-31, giriş tarihi dönemde, giriş > 0 ve giriş > stop. Olay değilse durum KESIK / DIS / STOP_ALTI; T1 için uygun gün < 30 ise T1_YOK; bunlar ölçülmez, sayıları raporda.
- T1 = aynı hissenin aynı dönemdeki BÜTÜN uygun günlerinin R15 ortalaması. Taban payları (HEDEF5, HEDEF10, R15 < -%20, R15 > +%20) = aynı hisse-dönemin bütün uygun günlerinde aynı kuralla; hücre tabanı = olaylar üzerinden ortalama.
- TF15 = R15 - T1 (olay başına); hücre ortalaması + ay kümeli bootstrap %95 (giriş ayı; 2.000; np.random.default_rng(5) her kol x hücrede yeniden; ağırlıklar KISA_UFUK.ku_boot'a verilir).
- Medyan fark = medyan(R15) - medyan(T1) (olaylar üzerinden).
- Oynaklık okuması: olayın ATRP20 beşliği (yukarıdaki sınırlar; sınıra eşit değer alt beşliğe) içinde TF15 ortalaması; artı beşlik = olayı olan ve ortalaması > 0 olan beşlik.

## 6. Hücreler ve KARAR KURALI (önceden; değişmez)
- KARAR hücreleri: ABD 2016-19, ABD 2020-22, AVR 2016-19, AVR 2020-22. BİLGİ: BIST 2016-19, BIST 2020-22. Kollar: K2 (ANA), YMSB, Y.
- Bir hücre TUTAR <=> n >= 30 VE TF15 GA alt ucu > 0 VE medyan fark > 0 VE artı beşlik >= 4 VE HEDEF5 katı (pay / taban) > 1. n < 30 ÖLÇÜLEMEDİ. Aksi TUTMAZ.
- EMARE (yaşayan evren) <=> ANA kol dört karar hücresinin dördünde TUTAR. Aksi 'EMARE DEĞİL'. Hangi sonuç çıkarsa çıksın başlık 'DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı bekliyor)'.
- K7: evren bugün yaşayan hisseler; yer şartı en az 2 kat düşmüş hisseleri seçtiği için batanların yokluğu sonucu YUKARI yanlı yapar (Ç263 dersi); artı sonuç en fazla 'EMARE (yaşayan evren)'; batanlar dahil veriyle sınama Aralık'ta.
- Sağlama: en az iki hücrenin TF15'i olay + getiri dosyalarından bağımsız kısa kodla (hv25 fonksiyonlarını kullanmadan) yeniden üretilir.

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban T1 = aynı hissenin aynı dönemdeki bütün uygun günleri, aynı giriş / 15 bar geometrisi (hv25_uygun + hv25_olc_dizi); hedef tabanı aynı kural, stop farkı (olay bölge dibi, taban 20 bar dibi) iş tanımından ve raporda yazılı; TF15 stop'tan bağımsız; mekanik etkiye karşı ATRP20 beşliği içi okuma; aynı gün eş portföy kullanılmadı (iş tanımı Cemal'in ölçütü: rastgele günler) |
| K2 | geleceğe bakma | EVET | beş şart yalnız t'ye kadar okur (gt_k2'ye seri t'de kesilerek verilir; test_k2_bolge_sonrasi_okunmaz); tekilleştirme ilk görülen pencere; beşlik sınırları getirisiz evren dağılımından; veri <= 2022-12-31 (gt_kesik_kapi assert) |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar serisi; kilitli pay <= 0,20 ve gövdesiz pay <= 0,30 pencere evreni; giriş ve 15 bar geçerli bar takviminde |
| K4 | tekilleştirme | EVET | kol ve hisse başına < 40 bar arayla biten pencerelerden ilki (gt_k2_tekil, test elle); n bağımsız olaya yakın; medyan fark ayrıca karar şartında |
| K5 | giriş fiyatı | EVET | giriş = t + 1 barı açılışı (hv25_olc_dizi g0 = gi[t + 1]); sinyal günü kapanışı kullanılmaz |
| K6 | veri birimi | EVET | tek kip: GOZ_TESPIT açık kopyası (MV_YOL gunluk, bölünme düzeltmeli, pencere paneliyle aynı seri; t tarih eşitliği assert); bütün ölçüler oran |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: sonuç YUKARI yanlı, raporda zorunlu uyarı; artı sonuç en fazla EMARE (yaşayan evren); batanlar dahil sınama Aralık |
| K8 | örneklem ve dönem | EVET | n < 30 ÖLÇÜLEMEDİ; iki dönem ayrı hücre; AVR 2016-19 K2 n 16 önceden ÖLÇÜLEMEDİ diye yazıldı; üç kol tek karar kuralıyla, BH yok çünkü karar yalnız ANA kolda ve dört hücrenin dördü isteniyor |
| K9 | ön kayıt | EVET | bu dosya kod sha, eşik sha, olay sha ve getirisiz sayımlarla getiriden önce commit + push; k2olc gt_kapi_commit + ik_kontrol_kapisi + sha denetimiyle başlar, ikinci koşu durur |
| K10 | ayrıştırma | EVET | goz2 ile birebir: GT3 32 / 32 ve GT4 20 / 20 sayfa; sentetik 660 pencere; YER vektör ön elemesi tam ölçüyle assert ve 300 red denetimi; olay t tarihi seriyle assert |
| K11 | yeniden üretim | EVET | rapordan önce iki hücrenin TF15'i olay + getiri dosyalarından bağımsız kısa kodla (hv25 kullanmadan) yeniden üretilecek; GT5_RAPOR'da yazılı |
| K12 | ifade | EVET | başlık DEDEKTÖRÜN BULDUĞU BÖLGELER; 'çöl tuttu / iz' cümlesi kurulmaz; TUTAR hücre düzeyinde bir sayım etiketidir; sayı ile yorum ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (test_cakisma_kapisi); yalnız GOZ_TESPIT.py, test_goz_tespit.py ve GT5_ / gt5_ dosyaları commit; yasak defter dosyalarına dokunulmadı; MI._mi_yaz sızıntı taraması; Colab'da kod değiştiği için çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; dedektör bölgeleri Cemal'in görsel onayını bekliyor |
