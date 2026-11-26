# YO2 ÖN KAYIT — geriye doğru doğrulama: H1 / H2 / H3, haftalık, kesimler 2016-22, sınama 2000-2015 (bir kez) (2026-11-26T21:11:50Z)

İş tanımı YO2_IS_TANIMI.md (ana model). Bu dosya R3 / Y5 / P3 HİÇBİR dönemde hesaplanmadan ÖNCE commit + push edilir; tanımlar, kesimler, hüküm kuralları sonra değişmez (değişirse SAPMA). Evren bugün yaşayan hisseler (H1 ve P3 yukarı yanlı). KASA açılmaz (veri <= 2022-12-31). HACİM KULLANILMAZ.

## Mühürler

YO_KOD_SHA: ceeb14c8b936458c4b40ee8730689b7f7eccf299f06e78ebd7fdcb07398727d2
YO2_ESIK_SHA: 0fedc026f0028dde235fdf179d3a12d573d21de5a4052b9938e515c560a7eba3
DOSYA_yo2_ozellik_ABD.pkl: 2f4731ba42eedce5b84f4ad768709b3645358217e131e82dd5c8f71e8e50c888
DOSYA_yo2_piyasa_ABD.pkl: 74df4b39654d967e1d7e1601d510da9a42bc4b5b0f718a8461bfb27899881153
DOSYA_yo2_ham_ABD.npz: e2754931c5d0a1e8ba548480501136f30132888c2f68df6143181b7f84b9984e
DOSYA_yo2_ozellik_AVR.pkl: ada6efae173faee4cbb377c0a0c2faea10d6b0a8f6e54a8199dcf8139bf3a94a
DOSYA_yo2_piyasa_AVR.pkl: c755987b0d2f579b4711f4ab02fea7e1b21e03979566044d1422020e64fee1d5
DOSYA_yo2_ham_AVR.npz: ad898c210d9977beb7b1441aeaaa628b51ac5a87a72a2530f6f19b8926be2a02
SAYIM_SHA: 50c1ef30902b033f0190e5de1ce285fa77052fa9b6f4540206d283bccb4997a8
KESIM_SHA: eefc8ab8d058b381adad835d4ec05810a2c4f6b77d6a26d3f0c617a22a80c422
ENDEKS_SHA: 77b31a36ba0ecf488353004137be1fe53593aa2a48ea580c9b1edb8f569472bf
IS_TANIMI_SHA: a924251b598d3e6d70e656858f4c9f76952a5b3ee759ad2a2c02361f2697283a

- Panel dosyaları (repo dışı): /root/.kasa/ham/yukselis_oncesi/yo2

## Üç varsayım (yön, kesim, hüküm SABİT)

- H1 (ARTI): DUSUS_W <= -0.399532 (ABD 2016-22 %10; n 822767) -> TOPLAM FARK > 0
- H2 (EKSİ): BOY_W <= 0.647797 (ABD 2016-22 %10; n 822767) -> TOPLAM FARK < 0
- H3 (ARTI): G40 <= 0.276760 (ABD 2016-22 piyasa haftası %10; n 362) -> ENDEKS 3 haftalık getiri farkı > 0 ve P(>= +%5) farkı > 0
- AVR (bilgi, yön) kesimleri: DUSUS_W -0.275313, BOY_W 0.656744, G40 0.264469 (AVR 2016-22 %10)
- ENDEKS: YOK (yerelde SPY / ^GSPC yok; Tiingo yanıtı: aylık 500 sembol sınırı aşıldı (26 Kasım 2026)); yanıt dosyası sha f3fbb415c16496373598c926a0c929953ebeae85c77310bcf7f510d41477d0e0
- Hüküm: DOĞRULANDI <=> 2000-2015 TOPLAM FARK > 0 VE alt > 0 VE a0007 ve a0815 TOPLAM FARK > 0 (etiket 'YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)'); DOĞRULANDI <=> 2000-2015 TOPLAM FARK < 0 VE üst < 0 VE a0007 ve a0815 TOPLAM FARK < 0; DOĞRULANDI <=> ENDEKS 3 haftalık getiri farkı (düşük - öteki) > 0 VE alt > 0 VE P(>= +%5) farkı > 0 VE ayrı dönem >= 4. Sıra: ÖLÇÜLEMEDİ (hisse: n < 1000 ya da çeyrek < 12; piyasa: düşük hafta < 30 ya da ayrı dönem < 4 ya da ENDEKS YOK) > DOĞRULANDI > TERS (nokta işareti beklenenin tersi) > GÖSTERİLEMEDİ. ADIM 0 (2016-19 ve 2020-22, ABD): H1 TOPLAM FARK > 0, H2 TOPLAM FARK < 0, H3 (ENDEKS; yoksa P3) getiri farkı > 0 ve P(>= +%5) farkı > 0, İKİ dönemde; biri tersse ADIM 1 etiketi 'ÖLÇEK UYMADI | <hüküm>'

## GETİRİSİZ SAYIM (R3 / Y5 / P3 hesaplanmadı)

### Yıl başına hisse (haftalık barı olan / evrende örnek satırı olan) ve hisse-hafta

| yıl | ABD bar | ABD evren | ABD hisse-hafta | AVR bar | AVR evren | AVR hisse-hafta |
|---|---|---|---|---|---|---|
| 2000 | 1611 | 756 | 21395 | 280 | 182 | 5258 |
| 2001 | 1652 | 843 | 35511 | 317 | 209 | 8531 |
| 2002 | 1704 | 875 | 37207 | 347 | 230 | 9153 |
| 2003 | 1779 | 965 | 40608 | 357 | 235 | 9759 |
| 2004 | 1853 | 1134 | 48132 | 374 | 257 | 11174 |
| 2005 | 1946 | 1235 | 53160 | 387 | 292 | 12688 |
| 2006 | 2043 | 1338 | 60145 | 405 | 317 | 14420 |
| 2007 | 2146 | 1483 | 68561 | 425 | 345 | 16227 |
| 2008 | 2207 | 1463 | 66839 | 429 | 334 | 15477 |
| 2009 | 2248 | 1428 | 62938 | 442 | 320 | 14470 |
| 2010 | 2347 | 1517 | 67946 | 462 | 332 | 15340 |
| 2011 | 2406 | 1587 | 72116 | 463 | 335 | 15759 |
| 2012 | 2503 | 1595 | 73246 | 465 | 341 | 15850 |
| 2013 | 2624 | 1771 | 78389 | 475 | 360 | 16784 |
| 2014 | 2772 | 1945 | 87051 | 491 | 385 | 17674 |
| 2015 | 2905 | 2024 | 91215 | 503 | 406 | 19148 |
| 2016 | 3003 | 2070 | 94093 | 514 | 415 | 19750 |
| 2017 | 3154 | 2249 | 101175 | 523 | 431 | 20431 |
| 2018 | 3352 | 2432 | 109766 | 535 | 455 | 21139 |
| 2019 | 3520 | 2530 | 111246 | 546 | 460 | 21629 |
| 2020 | 3797 | 2883 | 121605 | 550 | 489 | 21992 |
| 2021 | 4264 | 3493 | 146547 | 569 | 491 | 22591 |
| 2022 | 4302 | 3330 | 138335 | 569 | 501 | 22108 |

- ABD 2000-2015'te evren hisse sayısı < 300 olan yıl: yok (beklenen ÖLÇÜLEMEDİ değil)

### Dönem başına hisse-hafta ve uç sayısı

| pazar / dönem | hisse-hafta | hisse | çeyrek | DUSUS_W eksik % | H1 uç n | BOY_W eksik % | H2 uç n | DUSUS_W %2 / %10 / %50 | BOY_W %2 / %10 / %50 |
|---|---|---|---|---|---|---|---|---|---|
| ABD a0007 | 364719 | 1585 | 31 | 0,0 | 19358 | 0,0 | 35043 | -0,526 / -0,322 / -0,124 | 0,509 / 0,652 / 0,987 |
| ABD a0815 | 599740 | 2229 | 32 | 0,0 | 39343 | 0,0 | 66203 | -0,549 / -0,342 / -0,127 | 0,497 / 0,636 / 0,978 |
| ABD d1619 | 416280 | 2738 | 16 | 0,0 | 17932 | 0,0 | 39090 | -0,481 / -0,307 / -0,118 | 0,518 / 0,655 / 0,981 |
| ABD d2022 | 406487 | 3743 | 12 | 0,0 | 64345 | 0,0 | 43187 | -0,677 / -0,477 / -0,186 | 0,486 / 0,640 / 0,999 |
| AVR a0007 | 87210 | 360 | 31 | 0,0 | 9785 | 0,0 | 10059 | -0,496 / -0,290 / -0,107 | 0,489 / 0,639 / 0,988 |
| AVR a0815 | 130502 | 425 | 32 | 0,0 | 14424 | 0,0 | 14967 | -0,478 / -0,287 / -0,113 | 0,494 / 0,639 / 0,978 |
| AVR d1619 | 82949 | 481 | 16 | 0,0 | 4081 | 0,0 | 7653 | -0,338 / -0,222 / -0,095 | 0,526 / 0,665 / 0,987 |
| AVR d2022 | 66691 | 515 | 12 | 0,0 | 10883 | 0,0 | 7311 | -0,516 / -0,335 / -0,136 | 0,501 / 0,645 / 1,006 |

### Piyasa haftaları ve düşük genişlik (G40 <= kesim) öbekleri

| pazar / dönem | hafta | düşük hafta | ayrı dönem (öbek) | öbekler (ilk - son yıl-ay) | G40 %2 / %10 / %50 | kesit medyanı |
|---|---|---|---|---|---|---|
| ABD a0007 | 378 | 11 | 3 | 2001-09 - 2001-09; 2002-07 - 2002-10; 2003-01 - 2003-02 | 0,229 / 0,394 / 0,662 | 910 |
| ABD a0815 | 418 | 49 | 5 | 2008-01 - 2008-03; 2008-06 - 2008-06; 2008-09 - 2009-04; 2011-07 - 2011-11; 2015-08 - 2015-08 | 0,077 / 0,241 / 0,666 | 1374 |
| ABD d1619 | 208 | 11 | 2 | 2015-12 - 2016-02; 2018-12 - 2018-12 | 0,189 / 0,400 / 0,661 | 1996 |
| ABD d2022 | 154 | 26 | 2 | 2020-03 - 2020-05; 2022-04 - 2022-10 | 0,094 / 0,212 / 0,532 | 2672 |
| AVR a0007 | 378 | 48 | 3 | 2001-03 - 2001-03; 2001-09 - 2001-11; 2002-07 - 2003-03 | 0,078 / 0,177 / 0,692 | 212 |
| AVR a0815 | 418 | 71 | 3 | 2008-01 - 2008-04; 2008-06 - 2009-04; 2011-07 - 2011-12 | 0,072 / 0,156 / 0,698 | 306 |
| AVR d1619 | 208 | 10 | 2 | 2016-01 - 2016-02; 2018-10 - 2018-12 | 0,223 / 0,334 / 0,658 | 398 |
| AVR d2022 | 154 | 27 | 3 | 2020-03 - 2020-05; 2022-02 - 2022-03; 2022-06 - 2022-10 | 0,087 / 0,198 / 0,538 | 432 |

## Yorum gerektiren noktalar (ölçümden ÖNCE sabit)

1. Birim hisse-hafta t = hissenin kendi haftalık bar indeksi i; örnek HER HAFTA (v1'deki 'her 5 günde bir / 15 gün ufuk' oranının haftalık karşılığı 'her hafta / 3 hafta ufuk'; sonuçlar 3 kat örtüşür). Pencere = i - 2 .. i (3 hafta, t dahil); i - 1 .. i + 3 arasında eksik ISO haftası olan satır atılır.
2. Hedef stopu GİRİŞE değil pencere dibine göre: stop = min Low_{i-2..i} x 0,98 (iş tanımı). Aynı haftada hedef ve stop: STOP ÖNCE (kötümser). E0 stopun altındaysa ilk hafta stop sayılır (Y5 = 0).
3. T1 ve 'aynı hissenin rastgele haftaları' (p_h, q_h) dönem başına: a0007 = 2000-07, a0815 = 2008-15, d1619, d2022. 2000-2015 satırı iki alt dönemin birleşimidir; her satırın T1'i kendi alt döneminden (8 yıllık piyasa düzeyi farkı T1'e karışmasın). T1 / p_h hissenin o dönemdeki BÜTÜN örnek haftalarından (özelliği eksik olanlar dahil); popülasyon (uç payı ve bootstrap kümeleri) özelliği sonlu satırlar.
4. DUSUS_W ve BOY_W ilk 14 haftada tanımsız; haftalık veri 2000-01-03'te başladığı için 2000'in ilk ~3,5 ayı H1 / H2'de, ilk ~10 ayı (SMA40) H3'te eksik (sayımda). P2 havuzunun kendi ısınması (günlük p1 verisi 2000'de başlar) 2000 başında evreni daraltır (yıl sayımında).
5. Kesimler YALNIZ ABD 2016-22 hisse-hafta (H1, H2) ve piyasa haftası (H3) dağılımından; 2000-2015 özellik dağılımı kesime girmez. AVR (bilgi) aynı %10 düzeyinin AVR 2016-22 dağılımındaki değeriyle (ön kayıtta yazılı). AVR hükme girmez (ABD ana; AVR yönü bilgi).
6. G40 kesiti: w haftasında barı olan, bar tarihinde evren bayrağı taşıyan ve SMA40'ı tanımlı hisseler (>= 30). P3(w) = w haftasındaki ÖRNEK satırlarının (evren + boşluksuz + sonuç penceresi veride) R3 ortalaması (>= 5). Piyasa haftası w'nin giriş tarihi = w'nin pazartesisi + 7 gün (dönem ve çeyrek bundan).
7. AYRI DÖNEM (öbek): düşük genişlik haftaları ISO hafta sıra numarasıyla; ardışık iki düşük hafta arasında en az 8 hafta varsa (sıra farkı >= 9) yeni öbek. Öbek tarihleri ilk ve son haftanın yıl-ayı. H1 / H2 için ayrı dönem = farklı çeyrek sayısı (hükme girmez).
8. ENDEKS: yerelde SPY / ^GSPC yok (V_ABD panelleri, /tmp/veri, /tmp/claude-0/tezgah_ref yahoo_kesik.pkl 2015'te başlar, French dosyaları aylık). Tiingo isteği (SPY günlük, 1999-2022) 26 Kasım 2026'da 'aylık 500 sembol sınırı aşıldı' yanıtı verdi (yanıt dosyası repo dışında, sha aşağıda). İş tanımının 'indirme olmazsa' kuralıyla H3 hükmü 'ENDEKS YOK: ÖLÇÜLEMEDİ'; evren ortalaması P3 ile aynı satır BİLGİ olarak yazılır (hayatta kalma yanlı, hüküm değil). ENDEKS durumu ön kayda mühürlüdür; sonradan endeks dosyası konursa ADIM 1 kapısı durur (tek sınama bozulmasın).
9. ADIM 0 'ölçek' sınaması ENDEKS yokken H3 için P3 ile yapılır (bilgi). H1 / H2'de ölçek şartı yalnız TOPLAM FARK işareti (iş tanımı: 'aynı yön'); KAT ve KOTU20 bilgi.
10. Hüküm sırası: ÖLÇÜLEMEDİ > DOĞRULANDI > TERS > GÖSTERİLEMEDİ. TERS = 2000-2015 nokta işareti beklenenin tersi (aralığa bakılmaz). Nokta ve aralık doğru yönde ama bir alt dönem ters ise GÖSTERİLEMEDİ. ÖLÇEK UYMADI ön ektir (hüküm yine hesaplanır).
11. Batan şirketler (BİLGİ satırı): yerelde 2000-2015'i kapsayan batan / kottan çıkan şirket fiyatı YOK (islenmis-veri K34 Yahoo fiyatları 2020-10'da başlar ve 2023 sonrasını içerir; Tiingo batanlar repoda değil, kota dolu). H1 batanlar satırı 'YOK' yazılır.
12. 2000-2015 getirileri yalnız ADIM 1'de bir kez hesaplanır (yo2_sonuc 'adim1' izni); kesim ve sayım fonksiyonları sonuç sütunu olan tabloyu reddeder (assert).

## Tanımlar (YO2_ESIK; sha yukarıda)

```
{
 "surum": "YO2-1.0",
 "veri": "MUM_IZI.mi_veri(pazar, MUM_IZI_HAFTALIK.MH_YOL['tam']) (OS.os_veri geçerli bar: O/H/L/C sonlu > 0, H > L, V > 0) -> MUM_IZI_V2.mv_haftalik_panel (ISO hafta: O = ilk geçerli gün açılışı, H / L = haftanın en yüksek / en düşüğü, C = son gün kapanışı; yarım hafta atılır; 'bosluk' = önceki haftayla arada boş ISO haftası); ABD (ana), AVR (yön, bilgi); veri <= 2022-12-31 (assert + KASA kapısı); HACİM KULLANILMAZ",
 "evren": "TEZGÂH 2 P2 havuzu, haftalık (MUM_IZI_UC.uc_evren_e2 kuralı aynen): bar tarihi t (hafta sonu) için ETIKET2.e6_p2_maske = t'den sonraki ilk geçerli günlük bar <= 10 satır içinde ve o gün P2'de, t geçersiz gün değil; P2 klasörü t <= 2015-12-31 ise MH_YOL['p1'], sonra MH_YOL['p2']",
 "donem": {
  "a0007": [
   "2000-01-01",
   "2007-12-31"
  ],
  "a0815": [
   "2008-01-01",
   "2015-12-31"
  ],
  "d1619": [
   "2016-01-01",
   "2019-12-31"
  ],
  "d2022": [
   "2020-01-01",
   "2022-12-31"
  ]
 },
 "kesim_donem": [
  "d1619",
  "d2022"
 ],
 "sinama_donem": [
  "a0007",
  "a0815"
 ],
 "ornek": "hisse-hafta t = hissenin haftalık bar indeksi i (HER HAFTA; 3 haftalık sonuç pencereleri örtüşür, çıkarım çeyrek kümeli): i >= 2, i + 3 <= son bar; i - 1 .. i + 3 barlarında 'bosluk' yok (pencere ve sonuç ardışık ISO haftaları); t barında evren (P2) bayrağı; giriş = i + 1 haftasının ilk günü (bas) 2000-01-01 .. 2022-12-31; i + 3 barı <= 2022-12-31; dönem = giriş tarihine göre",
 "sonuc": {
  "ufuk": 3,
  "hedef": 0.05,
  "stop_carpan": 0.98,
  "kotu": -0.2,
  "tanim": "E0 = i + 1 haftasının açılışı; R3 = i + 3 haftasının kapanışı / E0 - 1; Y5 = i + 1 .. i + 3 haftalarında ilk High >= E0 x 1,05 haftası, ilk Low <= pencere dibi (min Low i - 2 .. i) x 0,98 haftasından ÖNCE (aynı hafta = stop önce, kötümser; E0 <= stop ise ilk hafta stop); KOTU20 = R3 < -0,20"
 },
 "ozellik": {
  "DUSUS_W": "min Low_{i-2..i} / maks High_{i-14..i-3} - 1 (pencereden önceki 12 haftanın en yükseğinden pencere dibine; i >= 14)",
  "BOY_W": "medyan((H - L) / C)_{i-2..i} / medyan((H - L) / C)_{i-26..i-3} (önceki 24 hafta; en az 12 hafta: i >= 14)",
  "G40": "piyasa haftası w (ISO hafta): w'de barı ve evren bayrağı olan, SMA40 (kendi son 40 haftalık kapanışı, i dahil) tanımlı hisselerde C > SMA40 payı; >= 30 hisse"
 },
 "kesim": {
  "duzey": 0.1,
  "tanim": "DUSUS_W <= q10, BOY_W <= q10 (ABD 2016-22 hisse-hafta dağılımı; özelliği sonlu satırlar), G40 <= q10 (ABD 2016-22 piyasa haftası dağılımı); np.quantile doğrusal; eşitler dahil. AVR (bilgi) aynı düzeyin AVR 2016-22 dağılımındaki değeri"
 },
 "olcu": {
  "T1": "aynı hissenin aynı dönemdeki BÜTÜN örnek haftalarının R3 ortalaması (dönem = a0007 / a0815 / d1619 / d2022)",
  "TOPLAM_FARK": "R3 - T1, uç satırların ortalaması (2000-2015 satırı = iki alt dönemin birleşimi, T1 her satırın kendi alt döneminden)",
  "KAT": "sum Y5 (uç) / sum p_h (uç), p_h = aynı hissenin aynı dönemdeki bütün örnek haftalarının Y5 payı (aynı hissenin rastgele haftası)",
  "KOTU20": "uç satırlarda R3 < -0,20 payı; taban = aynı kuralla aynı hissenin dönem payı (q_h) ortalaması uç satırlarda",
  "piyasa": "P3(w) = w haftası örnek satırlarının (bütün evren; özellikten bağımsız) R3 eşit ağırlıklı ortalaması (>= 5 hisse); ENDEKS(w) = SPY temettü / bölünme düzeltmeli: adjClose(w + 3 haftasının son günü) / adjOpen(w + 1 haftasının ilk günü) - 1 (w + 1 .. w + 3 ISO haftaları veride); düşük genişlik = G40 <= kesim; öteki = aynı dönemdeki öteki haftalar; P(>= +%5), P(<= -%5)",
  "obek": "düşük genişlik haftaları ISO hafta sırasıyla; ardışık iki düşük hafta arasında >= 8 hafta (sıra farkı >= 9) varsa yeni öbek (AYRI DÖNEM)"
 },
 "boot": {
  "B": 10000,
  "tohum": 2000,
  "kume": "giriş çeyreği (YYYY-Qn)",
  "tanim": "çeyrek kümeli bootstrap: çeyrekler yerine koyarak (multinomial ağırlık), her satırda np.random.default_rng(2000) yeniden (tekrarlanabilir); küme kümesi = satırın popülasyonundaki (hisse: özelliği sonlu satırlar; piyasa: dönemdeki bütün haftalar) çeyrekler; %95 = 2,5 / 97,5 yüzdelik; T1 / p_h / q_h sabit"
 },
 "hukum": {
  "n_min": 1000,
  "ceyrek_min": 12,
  "piyasa_n_min": 30,
  "obek_min": 4,
  "H1": "DOĞRULANDI <=> 2000-2015 TOPLAM FARK > 0 VE alt > 0 VE a0007 ve a0815 TOPLAM FARK > 0 (etiket 'YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)')",
  "H2": "DOĞRULANDI <=> 2000-2015 TOPLAM FARK < 0 VE üst < 0 VE a0007 ve a0815 TOPLAM FARK < 0",
  "H3": "DOĞRULANDI <=> ENDEKS 3 haftalık getiri farkı (düşük - öteki) > 0 VE alt > 0 VE P(>= +%5) farkı > 0 VE ayrı dönem >= 4",
  "sira": "ÖLÇÜLEMEDİ (hisse: n < 1000 ya da çeyrek < 12; piyasa: düşük hafta < 30 ya da ayrı dönem < 4 ya da ENDEKS YOK) > DOĞRULANDI > TERS (nokta işareti beklenenin tersi) > GÖSTERİLEMEDİ",
  "olcek": "ADIM 0 (2016-19 ve 2020-22, ABD): H1 TOPLAM FARK > 0, H2 TOPLAM FARK < 0, H3 (ENDEKS; yoksa P3) getiri farkı > 0 ve P(>= +%5) farkı > 0, İKİ dönemde; biri tersse ADIM 1 etiketi 'ÖLÇEK UYMADI | <hüküm>'"
 },
 "kesik": "her pazar veri en büyük tarihi <= 2022-12-31 (HV.hv_kesik_kapi) + KASA.kasa_kapisi(tam, p1, p2 dosyaları, '2022-12-31'); 2023+ giriş assert",
 "sira": "kod + sentetik test -> getirisiz sayım + kesimler -> ön kayıt commit + push -> ik_kontrol_kapisi -> ADIM 0 (2016-22) -> ADIM 1 (2000-2015, bir kez) -> rapor"
}
```

## KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt |
|---|---|---|---|
| K1 | kontrol grubu | EVET | taban aynı hissenin aynı dönemdeki bütün örnek haftaları (TOPLAM FARK = R3 - T1; KAT = Y5 / aynı hissenin Y5 payı; KOTU20 aynı); stop pencere dibine göre (uç ve taban satırlarında aynı geometri); H3 öteki haftalar aynı dönem; sınanan şey önceden sabit üç varsayım (eş portföy yok: ölçü hissenin kendine göre) |
| K2 | geleceğe bakma | EVET | özellikler i barına kadarki barlardan (test: i + 1 ve sonrası bozulunca aynı); G40 w haftasına kadar; giriş i + 1 açılışı; R3 / Y5 / P3 / ENDEKS ayrı fonksiyonda, aşama izni assert (kesim aşaması sonuç okuyamaz; ADIM 0 yalnız d1619 / d2022, ADIM 1 yalnız a0007 / a0815); kesimler yalnız 2016-22 (assert); 2023+ giriş assert + KASA |
| K3 | geçerli bar | EVET | MI.mi_veri geçerli bar (H > L, V > 0, O/H/L/C sonlu > 0); haftalık bar yalnız geçerli günlerden; pencere + sonuç haftalarında boşluk (eksik ISO haftası) yok; evren P2 (likidite / fiyat alt sınırı, bölünme şüphesi dışı); geçersiz gün sinyal değil |
| K4 | tekilleştirme | EVET | her hafta örnek (3 haftalık sonuçlar örtüşür; bağımsız sayılmaz): çıkarım çeyrek kümeli bootstrap; n, farklı çeyrek, en kalabalık 3 çeyrek payı ve H3 için ayrı dönem (öbek) sayısı ayrı yazılır; medyan bilgi |
| K5 | giriş fiyatı | EVET | giriş = sinyal haftasından sonraki haftanın ilk geçerli gününün açılışı (t kapanışı değil); ENDEKS de w + 1 ilk gün adjOpen |
| K6 | veri birimi | EVET | OS / MI bölünme düzeltmeli kopya (tam / p1 MUM_IZI_HAFTALIK hazırlığı); getiriler oransal, yerel para; pazar içi; ENDEKS adjOpen / adjClose aynı kip (temettü + bölünme düzeltmeli) |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler: 2000-2015'te batanlar veride YOK -> H1 ve P3 (evren ortalaması) YUKARI yanlı; H3 hükmü yalnız ENDEKS ile; H1 DOĞRULANDI çıkarsa etiket 'YAŞAYAN EVRENDE DOĞRULANDI (batanlar yok)'; KOTU20 payı yazılır; batan şirket verisi 2000-2015 için yerelde yok |
| K8 | örneklem ve dönem | EVET | hisse satırı n >= 1.000 ve çeyrek >= 12, piyasa satırı düşük hafta >= 30 ve ayrı dönem >= 4 değilse ÖLÇÜLEMEDİ; iki alt dönem (2000-07, 2008-15) işaret şartı H1 / H2 hükmünde; üç sabit varsayım, BH gerekmez (her biri kendi hükmü; ek satır yok) |
| K9 | ön kayıt | EVET | YO2_ON_KAYIT.md: YO_KOD_SHA, YO2_ESIK_SHA, panel sha, SAYIM_SHA, KESIM_SHA, ENDEKS durumu + getirisiz sayım + kesimler + yorum noktaları; ADIM 0 / ADIM 1 ön kayıt commit + push'tan sonra (kapı: kontrol + mühürler + commit + temiz ağaç + KASA); ikinci ADIM 1 koşusu durur |
| K10 | ayrıştırma | EVET | panel şeması ve satır sayıları sayım sha'sıyla; DUSUS_W / BOY_W / G40 / R3 / Y5 elle hesaplanmış sentetik örneklerle; haftalık panel MV / MH fonksiyonlarıyla (değiştirilmedi); ENDEKS dosyası şema denetimi (date, adjOpen, adjClose), yoksa ENDEKS YOK |
| K11 | yeniden üretim | EVET | rapordan önce >= 2 satır (H1 ve H3 / H2) panel + ham depodan bağımsız kısa kodla yeniden üretilir; rapor sayıları yo2_sonuc.json'dan |
| K12 | ifade | EVET | hüküm yalnız önceden yazılmış kuralla (DOĞRULANDI / GÖSTERİLEMEDİ / TERS / ÖLÇÜLEMEDİ / ÖLÇEK UYMADI); DOĞRULANDI = 'birleşik iz bileşeni adayı', kasa açılmaz; sayı ile yorum ayrı cümlede; hayatta kalma uyarısı raporda |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_yo) korundu; yalnız YUKSELIS_ONCESI.py'ye ek + kendi testleri + kendi çıktı yolları commit; mevcut modüller / defter dosyaları değişmez; sızıntı taraması MI._mi_yaz; ENDEKS isteğinde kullanıcı bilgisi yok; kod değişirse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; karar vermez, kasa açılmaz |

## SAPMA

(ön kayıt anında yok)
