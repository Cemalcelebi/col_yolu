# GT8 ÖN KAYIT — KURAL-3 (eski kod + yer + zaman): bulduğu bölgelerin sonrası, (A) bölge sonu girişi ve (B) tavan kırılımı girişi (27 Kasım 2026)

# DEDEKTÖRÜN BULDUĞU BÖLGELER (Cemal'in görsel onayı eşiğin hemen altında: yeni sayfalarda %64; kalıp hükmü değil)

Bu ölçüm 'çöl tuttu / tutmadı / iz' sorusunu yanıtlamaz. KURAL-3 dedektörünün bulduğu bölgelerin sonraki 15 barını, aynı hissenin aynı dönemdeki sıradan günleriyle (A) ve sıradan tavan kırılımlarıyla (B) karşılaştırır. Cemal'in görsel onayı yeni sayfalarda %64 (7 / 11; ABD 6 / 8, BIST 1 / 3); ölçütü (%70-90) henüz sağlanmadı.

K7 UYARISI: evren bugün yaşayan hisseler; yer şartı en az 2 kat düşmüş hisseleri seçtiği için batanların / kottan çıkanların yokluğu sonucu YUKARI yanlı yapar (Ç263 dersi); T1 / T1k aynı hisseden olduğu için yanlılık farkta kısmen düşer, kalkmaz; artı sonuç en fazla 'EMARE (yaşayan evren)'; batanlar dahil veriyle sınama Aralık'ta.

İş tanımı: arastirma_cikti/goz_tespit/GT8_IS_TANIMI.md (ana model). Bu dosya hiçbir getiri / kırılım / yön hesaplanmadan ÖNCE commit + push edilir. `python GOZ_TESPIT.py k3olc` bu dosyanın commit + push edilmiş olmasını (gt_kapi_commit), KONTROL LİSTESİ'nin dolu olmasını (IZ_KARNE.ik_kontrol_kapisi), kod sha / eşik sha / olay sha / Kontrol 2 sha'sının bu dosyada yazılı ve gt8_sayim.json ile aynı olmasını denetler; gt8_ozet.json varsa ikinci koşu durur. Ölçüm bir kez.

## 1. Mühürler
- Kod commit: a43071e (GOZ_TESPIT.py bölüm 14 KURAL-3 + test_goz_tespit.py), push edildi; ölçümden önce.
- GOZ_TESPIT.py sha256 (kod_sha): 13520d7006e773d002045558561c3a523e5952baecc89f03b72a35c3841386cb
- KURAL-3 eşik sha (GT_K3): 5abb4adce8761bf42fa9893e0f83b3d2480d164204e1c57173842ca690dbab16
- ÇÖL-K2 eşik sha (GT_K2 + GT_K2_OLAY + GT_K2_OLC; değişmedi, GT5 ile aynı): 457e7ce7f0a2cc15f92651457209471f0b4213fe85e2a052a87538f8b65bbebe
- Olay dosyası /root/.kasa/ham/goz_tespit/k3/k3_olay.pkl sha256 (olay_sha): 609d8e1fa20be56e5741b8219d28ca0418349c735897b895bd2001675e2bccc9
- Aday dosyası /root/.kasa/ham/goz_tespit/k3/k3_aday.pkl sha256 (YER = 1 pencereler + D1 / ZAMAN / kollar): 1573864d37d7908ce0c380f5fa4afa1c300a697bfabef5eac3acbdf29911c104
- GT5 YER kümesi (k2_aday.pkl; hisse hisse aynı olmalı, assert): 1de72c6af86d380f171919cd3b95c288335d4afded2166969187ed044776eb0d
- Kontrol 2 dosyası (GT6 dondurulmuş k2k_kontrol_kir.pkl; gt6_ozet.json satir_sha konkir_pkl; assert): 1cf3ac904550717a078378ece187143455994013808e285a63ad9892e7f278ff
- Getirisiz sayımlar: arastirma_cikti/goz_tespit/gt8_sayim.json (sha256 2e910d20f983b0f6a0aaada637f27c674fcb2247f5be082d5d57f5296a1dc0a0; 2026-11-27 17:18 UTC; bu commit'te).
- Testler: test_goz_tespit.py 54 / 54 (eski 45 aynen + yeni 9).
- Veri: açık kopya (/tmp/mum_izi/acik) ve pencere panelleri; en büyük tarih <= 2022-12-31 (gt_kesik_kapi assert, her pazar).

## 2. Tanımlar (GOZ_TESPIT.GT_K3; iş tanımından aynen)
- D1 = COL_SKOR6 PUAN_ESIT'in kendi pazarı ve L'si (20 / 40 / 80) içindeki evren sırası >= 0,90 (GT_DEDEKTOR D1 AYNEN). Evren = gt_evren_maske (pencere sonu 2016-01-01 .. 2022-12-31, s >= 30, KIL <= 0,20, PUAN_ESIT sonlu); sıra = (küçük + 0,5 eşit) / n (gt_yuzdelik), float32 (gt_sira_ekle ile aynı). Pencere paneli zaten yalnız 2016-22 pencere sonlarını içerir.
- YER = ÇÖL-K2 Y şartı AYNEN (gt_k2_yer_vek; kutu / uzak görünüm <= 0,22, kutu ortası alt %35'te, önceki 120 bar tepesi / kutu tavanı >= 2). YER = 1 kümesi GT5'in k2_aday.pkl'ıyla her hissede birebir (assert; geçti).
- ZAMAN: DIPTEN_BAR = (n - 1 - argmin(Low[s..t])) / n >= 0,5 (eşit diplerde ilk görülen; goz2/uc_set.py olc AYNEN).
- Kollar (ayrık): ANA = D1 ve YER ve ZAMAN; ZAMANSIZ = D1 ve YER ve ZAMAN değil; PUANSIZ = YER ve ZAMAN ve D1 değil.
- Olay evreni = gt_k2_evren (GT5 ile aynı: pencere sonu 2016-22, s >= 120, KIL <= 0,20, gövdesiz pay <= 0,30). Tekilleştirme kol + hisse başına (t, L) artan, son tutulanın sonundan >= 40 bar sonra biten tutulur (ilk görülen; gt_k2_tekil). Hücre = giriş (t + 1) tarihine göre dönem (2016-19 / 2020-22).
- (A) BÖLGE SONU GİRİŞİ (Ç271 fonksiyonları AYNEN): giriş = t + 1 açılışı; R15 = t + 15 kapanışı / giriş - 1 (gt_k2_olay_olc; durum TAMAM / KESIK / DIS / STOP_ALTI / T1_YOK; yalnız TAMAM ölçülür). T1 = aynı hisse-dönemin bütün uygun günlerinin (MUM_IZI_HAVUZ.hv25_uygun m = 20) R15 ortalaması (gt_k2_taban; < 30 gün ise T1_YOK). TF15 = R15 - T1. SİMETRİK İLK DOKUNUŞ (gt_k2k_simetrik): t + 1 .. t + 15 barlarında High >= giriş x 1,05 mi önce, Low <= giriş x 0,95 mi; aynı barda ikisi BELİRSİZ; %10 için aynısı; stop yok. Taban = aynı hisse-dönemin aynı uygun günlerinde aynı ölçü. R15 < -%20 / > +%20 payları ve tabanları (gt_k2_taban).
- (B) TAVAN KIRILIMI GİRİŞİ (Ç272 fonksiyonları AYNEN): TAVAN = bölgedeki en yüksek High, DİP = en düşük Low; t'den sonraki 20 geçerli barda Close > TAVAN olan ilk bar b, Close < DİP'ten ÖNCE gelirse (gt_k2k_yon, YUKARI önce); izleme 20. barı veride yok ya da > 2022-12-31 ise KESIK. Giriş = b + 1 açılışı, R15 = b + 15 kapanışı (gt_k2k_giris); kol + hisse başına 15 bar tekil (gt_k2k_tekil). KONTROL 2 = aynı hissenin aynı dönemdeki sıradan tavan kırılımları: GT6'nın dondurulmuş k2k_kontrol_kir.pkl'ı (evrenin YER = 0 pencerelerinin YUKARI önce kırılımları, hisse başına 15 bar tekil). KURAL-3'ün üç kolu da YER'i şart koştuğu için kontrol kümesi kollarla örtüşmez. T1k = hisse-dönem içinde KESIK olmayan kontrol kırılımlarının R15 ortalaması (en az 5; azsa T1K_AZ, sayılır); simetrik +%5 / +%10 ve R15 uç tabanları aynı kırılımlardan (gt_k2k_taban2). TFk15 = R15 - T1k. Yön payları (yukarı önce / aşağı önce / kırılmadı) yalnız BİLGİ.
- Bootstrap: ay kümeli %95 (KISA_UFUK.ku_boot; 2.000; np.random.default_rng(8) her ölçüde yeniden); küme = giriş ayı.
- Beşlik: olayın ATRP20'si (t günü, pencere paneli); sınırlar o pazar x dönemin evren pencerelerinin %20/40/60/80'i (gt_k2_besli_sinir; GT5 besli_sinir ile birebir, assert); yalnız >= 20 olaylı beşliklerde ortalama fark.

## 3. Karar kuralı (önceden; değişmez)
- Hücre TUTAR <=> n >= 30 VE ortalama fark (A: TF15; B: TFk15) GA alt ucu > 0 VE medyan fark (medyan R15 - medyan T1; B'de T1k) > 0 VE simetrik +%5 farkının (olay başına 1[üst önce] - taban) GA alt ucu > 0 VE >= 20 olaylı beşliklerin en az %75'inde ortalama fark > 0 (böyle beşlik 2'den azsa şart aranmaz, yazılır). n < 30 ÖLÇÜLEMEDİ; aksi TUTMAZ.
- Hücreler: ABD 2016-19, ABD 2020-22 KARAR; AVR iki dönem n >= 30 ise KARAR, değilse ÖLÇÜLEMEDİ; BIST iki dönem BİLGİ.
- EMARE (yaşayan evren) <=> ANA kol ABD 2016-19 VE ABD 2020-22'de TUTAR; ikisinden biri ÖLÇÜLEMEDİ ise 'ÖLÇÜLEMEDİ'; aksi 'EMARE DEĞİL'. (A) ve (B) ayrı ayrı karara bağlanır; iki giriş türü denendiği raporda yazılır (çoklu karşılaştırma: iki tablo x iki ABD hücresi).
- Ek okuma (karar değil): ANA - ZAMANSIZ ve ANA - PUANSIZ ortalama fark ve simetrik +%5 farkı (kol x hücre).

## 4. Belirsiz yerlerin yorumu (sonuç görülmeden; değişmez)
1. (B) 'bölgeden sonraki 20 barda Close > TAVAN ilk bar': Ç272 düzeni aynen, yani yalnız tavan dipten ÖNCE kırıldıysa giriş var (Kontrol 2 kırılımları da aynı kuralla). Dip önce kırılmışsa giriş yok (BİLGİ satırında 'aşağı önce').
2. (A) STOP_ALTI: Ç271 uygunluk kuralı aynen (giriş > bölge dibi x 0,98); stop ölçüde kullanılmaz, yalnız uygunluk. Taban günleri m = 20 kuralıyla (gt_k2_taban aynen).
3. Simetrik payda: BELİRSİZ olay o ölçünün hem payından hem paydasından çıkar; YOK paydada kalır; taban da aynı kuralla.
4. 'Havuzun yüzde kaçı' = kol pencere sayısı (tekilleştirme öncesi) / olay evreni pencere sayısı (pazar başına; §5).
5. Kontrol 2 yeniden hesaplanmaz, GT6 dosyası kullanılır (sha assert); ölçüm sırasında 25 hissede (pazar başına 8, tohum 8) GT6 fonksiyonlarıyla yeniden hesaplanıp birebir olduğu denetlenir (gt_k3_kr_denetim; aksi durur). Kontrol 2 kırılımlarının ortalamaları GT6 ölçümünde (bilgi olarak) görülmüştü; KURAL-3 olaylarının hiçbir sonrası görülmedi.
6. AVR hücrelerinde olay 40-120 (kesiksiz); T1_YOK / STOP_ALTI / KESIK düşüşleri ve (B)'de kırılım adedi sonuca bağlı olduğundan n >= 30 olup olmayacağı önceden belli değil; AVR 2016-19 (A) üç kolda da sınırda (40-43 olay).
7. EMARE'de 'ÖLÇÜLEMEDİ' ayrımı: CLAUDE.md 'emin olma yolu' (ÖLÇÜLEMEDİ, 'EMARE DEĞİL' yerine kullanılır).

## 5. Getirisiz sayımlar (k3olay; getiri / kırılım / yön hesaplanmadı)
Pazar başına pencere sayıları (olay evreni = gt_k2_evren; parantez içinde evrenin yüzdesi):

| pazar | evren pencere (hisse) | YER | D1 | ZAMAN | ANA (ham) | ZAMANSIZ (ham) | PUANSIZ (ham) | bilgi: D1 + ZAMAN, YER yok |
|---|---|---|---|---|---|---|---|---|
| ABD | 3.332.810 (4246) | 110.007 (3.30) | 317.992 (9.54) | 1.832.629 (55.0) | 22.123 (0.664) | 31.457 (0.944) | 22.687 (0.681) | 131.718 |
| AVR | 553.811 (569) | 2.061 (0.37) | 54.088 (9.77) | 313.704 (56.6) | 435 (0.079) | 592 (0.107) | 461 (0.083) | 30.679 |
| BIST | 354.064 (457) | 5.439 (1.54) | 34.926 (9.86) | 220.338 (62.2) | 677 (0.191) | 868 (0.245) | 1.819 (0.514) | 16.852 |

Tekilleştirilmiş olaylar (kol x hücre; 15. bar kesik = t + 15 veride yok ya da > 2022-12-31; izleme kesik = (B) için 20. bar kesik; ATRP20 beşliği GT5 sınırlarıyla):

| kol | hücre | olay | hisse | 15. bar kesik | kesiksiz | (B) izleme kesik | L 20 / 40 / 80 | ATRP20 B1 / B2 / B3 / B4 / B5 | rol |
|---|---|---|---|---|---|---|---|---|---|
| ANA | ABD 2016-19 | 2057 | 697 | 0 | 2057 | 0 | 1568 / 230 / 259 | 0 / 3 / 19 / 207 / 1828 | KARAR |
| ANA | ABD 2020-22 | 4596 | 1617 | 84 | 4512 | 117 | 3593 / 527 / 476 | 9 / 33 / 288 / 1483 / 2783 | KARAR |
| ANA | AVR 2016-19 | 43 | 21 | 0 | 43 | 0 | 31 / 4 / 8 | 0 / 0 / 1 / 2 / 40 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| ANA | AVR 2020-22 | 104 | 65 | 0 | 104 | 1 | 79 / 14 / 11 | 0 / 0 / 1 / 13 / 90 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| ANA | BIST 2016-19 | 109 | 60 | 0 | 109 | 0 | 80 / 10 / 19 | 4 / 8 / 14 / 28 / 55 | BİLGİ |
| ANA | BIST 2020-22 | 128 | 80 | 0 | 128 | 0 | 91 / 14 / 23 | 27 / 29 / 14 / 38 / 20 | BİLGİ |
| ZAMANSIZ | ABD 2016-19 | 2221 | 702 | 0 | 2221 | 0 | 1545 / 338 / 338 | 1 / 2 / 22 / 182 / 2014 | KARAR |
| ZAMANSIZ | ABD 2020-22 | 5350 | 1564 | 178 | 5172 | 217 | 3753 / 822 / 775 | 9 / 29 / 304 / 1608 / 3400 | KARAR |
| ZAMANSIZ | AVR 2016-19 | 41 | 20 | 0 | 41 | 0 | 29 / 8 / 4 | 0 / 0 / 1 / 3 / 37 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| ZAMANSIZ | AVR 2020-22 | 120 | 58 | 3 | 117 | 4 | 94 / 15 / 11 | 0 / 0 / 1 / 4 / 115 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| ZAMANSIZ | BIST 2016-19 | 133 | 62 | 0 | 133 | 0 | 93 / 9 / 31 | 7 / 10 / 17 / 30 / 69 | BİLGİ |
| ZAMANSIZ | BIST 2020-22 | 135 | 78 | 0 | 135 | 0 | 88 / 14 / 33 | 33 / 23 / 27 / 27 / 25 | BİLGİ |
| PUANSIZ | ABD 2016-19 | 2039 | 726 | 0 | 2039 | 0 | 1637 / 260 / 142 | 0 / 1 / 20 / 207 / 1811 | KARAR |
| PUANSIZ | ABD 2020-22 | 4390 | 1622 | 81 | 4309 | 133 | 3573 / 525 / 292 | 5 / 32 / 309 / 1450 / 2594 | KARAR |
| PUANSIZ | AVR 2016-19 | 40 | 23 | 0 | 40 | 0 | 31 / 6 / 3 | 0 / 1 / 1 / 2 / 36 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| PUANSIZ | AVR 2020-22 | 98 | 62 | 0 | 98 | 0 | 82 / 10 / 6 | 0 / 0 / 0 / 10 / 88 | KARAR (n >= 30) / ÖLÇÜLEMEDİ |
| PUANSIZ | BIST 2016-19 | 185 | 82 | 0 | 185 | 0 | 139 / 25 / 21 | 6 / 17 / 20 / 58 / 84 | BİLGİ |
| PUANSIZ | BIST 2020-22 | 195 | 103 | 2 | 193 | 2 | 146 / 26 / 23 | 40 / 43 / 44 / 33 / 35 | BİLGİ |

- n < 30 olacağı önceden belli hücre: YOK (en küçük kesiksiz hücre AVR 2016-19 PUANSIZ 40). AVR 2016-19 hücreleri sınırda (§4.6).
- Önceden görülen yapı: ABD olaylarının %88-89'u en oynak iki beşlikte (B4 + B5); ABD'de >= 20 olaylı beşlik 2-3 tane olacak (beşlik şartı 2 / 2 ya da 3 / 3 gibi sert çalışır). AVR'de olayların %85-96'sı B5'te: büyük beşlik çoğu hücrede 1 olacak, şart aranmaz (yazılır).
- (B)'nin kırılım adetleri, T1K_AZ ve tekil düşüşler sonuca bağlıdır: ölçümle birlikte raporlanır.

## 6. Birebirlik (k3esles; getirisiz)
GT5_onay_anahtar.json'daki 21 sayfa: kural kolu olan 17 sayfanın 17'si bu kodla aynı kolda; 4 RASTGELE sayfanın hiçbiri KURAL-3'ün üç kolundan birinde değil (s. 21 kodla D1 + ZAMAN ama YER yok: eski kol adıyla D1+ZAMAN_YERSIZ). uc_set_tablo.json (GT1 / GT3 / GT4; 82 sayfa): açık veri sayfalarının 74 / 74'ünde Y ve DIPTEN_BAR birebir; 8 kitaplık sayfası 2024-26 verisi olduğu için okunmadı (veri <= 2022 kuralı).

| sayfa | pazar | anahtar kolu | kod kolu | KURAL-3 kolu | D1 sırası | Y | DIPTEN_BAR | aynı |
|---|---|---|---|---|---|---|---|---|
| 1 | BIST | D1+YER_ZAMANSIZ | D1+YER_ZAMANSIZ | ZAMANSIZ | 0.9997 | 1 | 0.100 | EVET |
| 2 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.850 | EVET |
| 3 | BIST | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 0.9995 | 1 | 0.950 | EVET |
| 4 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.500 | EVET |
| 5 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.775 | EVET |
| 6 | ABD | RASTGELE | KURAL_DISI | — | 0.5876 | 0 | 0.950 | — |
| 7 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.725 | EVET |
| 8 | BIST | D1+YER_ZAMANSIZ | D1+YER_ZAMANSIZ | ZAMANSIZ | 0.9996 | 1 | 0.300 | EVET |
| 9 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.800 | EVET |
| 10 | ABD | RASTGELE | KURAL_DISI | — | 0.8739 | 0 | 0.600 | — |
| 11 | BIST | RASTGELE | KURAL_DISI | — | 0.1187 | 0 | 0.000 | — |
| 12 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.950 | EVET |
| 13 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.875 | EVET |
| 14 | BIST | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 0.9997 | 1 | 0.550 | EVET |
| 15 | ABD | D1+ZAMAN_YERSIZ | D1+ZAMAN_YERSIZ | — | 1.0000 | 0 | 0.713 | EVET |
| 16 | BIST | D1+ZAMAN_YERSIZ | D1+ZAMAN_YERSIZ | — | 0.9998 | 0 | 0.662 | EVET |
| 17 | ABD | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 1.0000 | 1 | 0.500 | EVET |
| 18 | ABD | D1+YER_ZAMANSIZ | D1+YER_ZAMANSIZ | ZAMANSIZ | 1.0000 | 1 | 0.250 | EVET |
| 19 | BIST | D1+YER+ZAMAN | D1+YER+ZAMAN | ANA | 0.9992 | 1 | 0.750 | EVET |
| 20 | ABD | D1+YER_ZAMANSIZ | D1+YER_ZAMANSIZ | ZAMANSIZ | 1.0000 | 1 | 0.237 | EVET |
| 21 | BIST | RASTGELE | D1+ZAMAN_YERSIZ | — | 0.9968 | 0 | 0.988 | — |

## 7. HATA (ölçümden önce bulunanlar)
1. İş tanımı: 'uc_set_tablo.json'daki Y ve DIPTEN_BAR değerleriyle aynı' denmiş, ama uc_set_tablo.json GT5 sayfalarını içermiyor (GT1 30, GT3 32, GT4 20 sayfa). GT5'in 21 sayfası anahtardaki kolla, uc_set_tablo ise kendi 74 açık veri sayfasıyla ayrı ayrı denetlendi (ikisi de birebir).
2. İş tanımı / görev mesajı: '21 sayfanın kolu aynen çıkmalı' denmiş; 4 sayfa RASTGELE (anahtarda kural kolu yok). Bu sayfalar için ölçüt 'KURAL-3 kolunda değil' alındı (4 / 4). s. 21 (rastgele) kodla D1 + ZAMAN sağlıyor ama YER yok: rastgele seçim D1'e düşmüş; KURAL-3 kolu değil.
3. Bilgi: GT5 anahtarındaki 'd1_sira' alanı pencere panelindeki satır indeksinin bir fazlası (s. 2: d1_sira 2242571, panel satırı 2242570 = NSPR s 731 t 770); kol ve sıra hesabını etkilemiyor (eşleşme sembol + s + t + L ile).
4. Ölçüt tasarımı (K1, önceden görülen): olaylar ABD'de en oynak iki beşlikte yoğun; T1 aynı hissenin bütün günleri olduğu için oynaklık farkı kısmen eşlenir, beşlik içi fark ayrıca yazılır. Konum (bölge sonunun kutudaki yeri) ve kutu genişliği A'da eşlenmiyor (GT6 HATA 5 dersi); B'de Kontrol 2 aynı kırılım geometrisinde (tavan kırılımı, b + 1 giriş).
5. Kod (benim, commit öncesi düzeltildi): uçtan uca sentetik testte elle beklenen simetrik kodun 'yok' nöbetçisi 99 seçilmişti (bar indeksleri 99'u aşıyor); test düzeltildi, kod değişmedi. İlk sentetik seri YER pencere üretmiyordu; döngülü düşüş serisi yazıldı.

## KONTROL LİSTESİ (IZ_KARNE.IK_KONTROL)

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | (A) T1 = aynı hisse-dönemin bütün uygun günleri, aynı giriş (t + 1 açılış), aynı R15, aynı stopsuz simetrik ölçü (gt_k3_taban; Ç271 stop geometrisi farkı yok); (B) Kontrol 2 = aynı hisse-dönemin sıradan tavan kırılımları, aynı b + 1 giriş ve aynı ölçüler (GT6 dosyası, sha + 25 hisse yeniden hesap); 200 rastgele eş portföy yerine iş tanımındaki aynı hisse tabanı; ATRP20 beşliği içinde fark ayrıca; konum A'da eşlenmedi (HATA 4) |
| K2 | geleceğe bakma | EVET | D1 / YER / ZAMAN yalnız s..t ve önceki 120 bar (test_k3_sartlar_bolge_sonrasi_okunmaz: t sonrası bozulunca aynı; t'de kesilmiş seriyle aynı); D1 dağılımı yalnız 2016-22 evren pencereleri (test_k3_d1_sira_evren_ici_ve_2016_22); beşlik sınırları getirisiz; veri <= 2022-12-31 (gt_kesik_kapi) |
| K3 | geçerli bar | EVET | açık kopya MI.mi_veri geçerli bar; KIL <= 0,20 ve gövdesiz pay <= 0,30 evren şartı (gt_k2_evren); izleme yalnız High > Low barlar (gt_k2k_izleme); hv25_uygun giriş > 0 |
| K4 | tekilleştirme | EVET | kol + hisse başına >= 40 bar (gt_k2_tekil; test_k3_tekil_40); (B) kırılımlar 15 bar tekil (gt_k2k_tekil); medyan fark karar şartında |
| K5 | giriş fiyatı | EVET | (A) t + 1 açılışı (bölge son barının ertesi); (B) kırılım barı b'nin ertesi b + 1 açılışı; R15 giriş barı 1. bar (hv25_olc_dizi; uçtan uca testte elle) |
| K6 | veri birimi | EVET | oransal ölçüler (R15, simetrik %5 / %10, sıra); açık kopya bölünme düzeltmeli tek kip; pazarlar kendi evren sırasıyla; ATRP20 oransal |
| K7 | hayatta kalma | EVET | evren bugün yaşayan hisseler; yer şartı çok düşmüş hisseleri seçer: sonuç YUKARI yanlı; başlıkta ve raporda K7 uyarısı; artı sonuç en fazla 'EMARE (yaşayan evren)' |
| K8 | örneklem ve dönem | EVET | iki dönem (2016-19 / 2020-22) iki pazar (ABD, AVR) ayrı hücre; n < 30 ÖLÇÜLEMEDİ; önceden belli n < 30 hücre yok (§5); iki giriş türü (A, B) raporda yazılır; BH yok: karar ön kayıtlı dört şartın hepsi, iki dönem birlikte |
| K9 | ön kayıt | EVET | bu dosya k3olc'den önce commit + push (gt_kapi_commit); kod / eşik / olay / Kontrol 2 sha'ları bu dosyada ve kodda assert; ikinci koşu durur (gt8_ozet.json); eşikler GT_K3 (test_k3_esik_sabit) |
| K10 | ayrıştırma | EVET | pencere t indeksi seri tarihiyle assert; YER kümesi k2_aday.pkl ile her hissede assert; beşlik sınırları GT5 ile assert; GT5 21 sayfa + uc_set 74 sayfa birebir (k3esles) |
| K11 | yeniden üretim | EVET | ölçümden sonra iki hücre (A: ANA ABD 2016-19; B: ANA ABD 2020-22) satır dosyalarından bağımsız kısa kodla (arastirma_cikti/goz_tespit/gt8_sagla.py) yeniden üretilecek; Kontrol 2 25 hissede yeniden hesap (gt_k3_kr_denetim) |
| K12 | ifade | EVET | başlık 'DEDEKTÖRÜN BULDUĞU BÖLGELER (görsel onay %64; kalıp hükmü değil)'; 'iz / tuttu' denmez; sonuç etiketi yalnız TUTAR / TUTMAZ / ÖLÇÜLEMEDİ / EMARE (yaşayan evren); fiyat değişimi (R15) ile kâr ayrı |
| K13 | süreç | EVET | çakışma kapısı korundu (_cakisma_kontrol_gt); yasak defter dosyalarına dokunulmadı; yalnız kendi yollar commit (git add -A yok); e-posta / anahtar yok; Colab'da kod değiştiyse çalışma zamanını yeniden başlat |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para kararı yok; yalnız dedektör bölgelerinin sonrası ölçülüyor (araştırma) |
