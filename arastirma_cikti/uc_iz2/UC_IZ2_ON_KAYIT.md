# UC_IZ2 ÖN KAYIT — üç fiyat dışı iz (R sektör rüzgârı, B bilanço tepkisi, İ içeriden alım) aynı bilanço olayında, ABD 2016-22 (25 Kasım 2026)

İş tanımı: arastirma_cikti/uc_iz2/UC_IZ2_IS_TANIMI.md (commit b325107). Keşif ölçümü, açık veri (kesik 2022-12-31). KASA AÇILMAZ. Bu dosya ölçümden ÖNCE commit edilir; tanım / eşik / hücre / karar kuralı sonuca göre değişmez. Kod: UC_IZ2.py, test: test_uc_iz2.py (13 / 13 geçti).

KOD_SHA: 71d0e23903998e53530ff7dd99a36deeb81a05d1dd24973599fe69b6834516ba
ESIK_SHA: afa47f7add84655826f44f89344e5ee91a2ae73c84ba4fdd2fe9e3a4cb144f35
HAZIRLIK_SHA: 52a19fa6be447fa6dbb2c3eae01beb5206c88c968e1eaba62bc009c6dd61f01b
Kod commit: cef0b7d (UC_IZ2.py + test_uc_iz2.py + uc_iz2_hazirlik.json + uc_iz2_veri.json)
Veri: açık V_ABD.pkl 99e2fa9267058cc4 (TEZGAH2 V_ABD2 cd91b9991d368015, 2012-01-03..2022-12-30, 4450 sembol); form4_a1.pkl 2a1caf97020aac89; k8_202.pkl 0dfb9ecea437c2ad; olay.pkl 5dd75d9cd4d3d87a (/tmp/uc_iz2, repo dışı)

## 1. Veri ve sağlamalar (getirisiz; ölçümden önce)

- V1 fiyat: TEZGAH2_VERI yeniden indirildi (2026-11-25; ABD 5.649 sembol indirildi, V_ABD2 5394 sembol; AVR V_AVR2 578). 2022-12-31 kesikli açık kopyalar: acik_tam (2000..2022-12-30; ABD 4450, AVR 572 sembol) ve acik (ölçüm, 2012-01-03..2022-12-30, ABD 4450 sembol). KASA.kasa_kapisi: en geç 2022-12-30.
- TEZGAH2_DOGRULAMA 21 ana hüküm (acik_tam, d3 = 2016-01..2022-12; T2 / TD fonksiyonları aynen): P1 21 / 21 (orijinal 21), P2 20 / 21 (orijinal 20; düşen A1 d1 KISMEN, r 0,897, işaret 0,917; orijinalde de aynı satır KISMEN), P3 20 / 21. Seçim kuralıyla seçilen havuz P1 (orijinal P1). Kural (yorum, SAPMA bölümünde): seçilen havuz 21 / 21 ve orijinalle aynı -> GEÇTİ.
- V2 Form 4: 29 çeyrek zip (2015q4..2022q4; 310 MB, /root/.kasa/ham/sec2016/form345). A1 (FON_IZI.fi_k30_alimlar aynen + değer >= 10.000 $): 84.054 bildirim, 2015-10-01..2022-12-30, 6.502 ihraççı CIK (CIK'siz 0). Yıl: 2015 3.618, 2016 11.502, 2017 9.730, 2018 12.320, 2019 11.155, 2020 13.207, 2021 10.223, 2022 12.299. Sağlama (2022, fon_izi_k30 süzgeci V_ABD evreni): yeni 2119 / k30_alim.pkl 2119, ortak 2119, fark 0; 5 rastgele satır (CRGY 2022-08-15, TROX 2022-10-31, YEXT 2022-03-10, MSFT 2022-02-01, ECVT 2022-08-09) sembol / tarih / değer / CIK / rol birebir -> TUTTU.
- V3 8-K 2.02: SEC submissions 5580 CIK (TEZGAH2 evren listesi 5649 sembolden 5628 eşlendi), ek sayfa 936, 6517 istek, yeniden deneme 0, 404 0. 2.02 satırı (8-K + 8-K/A, bütün yıllar) 188.048. k55/sec_ozet.json kabul saati (acceptanceDateTime) içermediği için kullanılmadı. acceptanceDateTime UTC'dir (AAPL 16:30 ET duyuruları 20:30 / 21:30 Z; EDGAR sayfası 0000320193-26-000024 'Accepted 2026-11-02 16:30:23' = JSON 21:30:23Z). EDGAR sağlaması (WebFetch, tohum 2512 ile seçilen 5 olay; tarih / NY saati / madde): RYDER 0000085961-22-000050 2022-02-16 07:56:49 2.02/7.01/9.01; Malibu Boats 0001590976-16-000241 2016-09-07 08:25:31 2.02/9.01; Corporate Office Properties 0000860546-21-000045 2021-10-28 16:23:50 2.02/9.01; Pegasystems 0001013857-22-000088 2022-04-28 16:20:08 2.02/9.01; Hawkins 0000046250-22-000025 2022-08-04 16:15:55 2.02/8.01 -> 5 / 5 TUTTU.
- V4 sembol -> CIK (SEC company_tickers.json, sec_bugun): açık panel 4441 sembol, eşlenen 4433, eşlenemeyen 8; birden çok sınıf hissesi olan CIK 42.

## 2. Tanımlar (UC2_ESIK; sha yukarıda; kaynak fonksiyonlar)

- E1 (ANA OLAY) = bilanço günü t: form '8-K' ve items içinde '2.02' (virgülle ayrılmış madde listesinde tam eşleşme; 8-K/A hariç). Kabul saati acceptanceDateTime UTC -> America/New_York; yerel saat < 16:00:00 ise D0 = o gün, >= 16:00:00 ise D0 = ertesi takvim günü; t = birleşik takvimde (bütün hisselerin geçerli barları) D0'a eşit ya da sonraki ilk gün. Aynı CIK'de son TUTULAN olaydan <= 20 takvim günü sonraki 2.02 atılır (aynı gün dahil). Hisse t'de geçerli bar değilse olay düşer. t 2015-10-01..2022-12-31. CIK -> olay sembolü: en çok geçerli barlı sınıf (eşitlikte alfabetik ilk). Evren: TEZGAH2 P2 havuzu (KART_TUR2.k2_panel + k2_P + _k2_oc tekil 1, giriş günü) VE CETVEL2 v2.2 havuzu (C2.c2_olay tekil 1). Giriş = t'den sonraki ilk geçerli bar açılışı (K5). Tekil: bir bilanço = bir olay (H tekili yok).
- B (bilanço tepkisi, t bilgisi): EAR_t = (C_t / C_önceki geçerli - 1) - medyan(aynı gün t, aynı CETVEL2 kova satırı KV[t] (ATRP14 tercili x likidite üçlüsü x F15 çeyreği, t-1'e kadar bilgi), RET sonlu, o gün E1 olayı olan BÜTÜN CIK'lerin bütün sınıf sembolleri hariç, >= 5 eş). ATRP20_{t-1} = önceki geçerli barın 20 bar TR (önceki kapanışla) SMA'sı / C (POZITIF_KONTROL.pk_seri formülü, pencere 20). BVAL = EAR / ATRP20; B = BVAL >= 1,0. BİLGİ: Bm = BVAL <= -1,0. BVAL hesaplanamayan olay ölçüm dışı (huni).
- İ (içeriden alım): (t - 90 takvim günü, t] aralığında FILING_DATE'li >= 1 A1 (ihraççı CIK = olay CIK'i). Bilgi tarihi FILING_DATE <= t (giriş t+1 açılış).
- R (sektör rüzgârı, KT10 aynen): UC_IZ.uc_dip_ham -> KART_TUR2.k2_d9_durum(Vd, 'ABD', K2_ESIK['d9_olay_bas']) -> D9_YENIDEN.d9_satir 'c' (RÜZGÂR ∧ ¬D9 ∧ sektör var; sektor_ABD.csv; D9_PARAM) t günü.
- N = R + B + İ (0-3).
- E2 (BİLGİ, karar vermez): UC_IZ.uc_dip_ham KT02 dip olayı; B = son 15 geçerli barda (t dahil; UC_IZ.uc_pencere_bayrak) B = 1 olan bir E1 günü; İ = (t-90, t] A1; R = KT10 'c'. Ölçüm tekil H (Ç225 ile aynı kural), eş dışlaması aynı gün bütün KT02 olayları.

## 3. Ölçü, eş, taban, hücre

- R_H (H = 15 ve 60 KARAR, 30 BİLGİ) = H. geçerli bar kapanışı / giriş açılışı - 1 (C2.c2_panel22_al, pencere 2H satır, stop yok); ölçüm penceresi 2022-12-30'u aşan olay ölçülmez (veri kesik). Konum eşi C2.c2_es: aynı giriş günü, aynı kova (cetvel2_esik_v2.2.json sınırları), >= 5 eş; dışlanan = o gün E1 olayı olan bütün CIK'lerin bütün sınıf sembolleri (C2.c2_olay tekil 1 ile giriş günleri). FARK = R_H - eş ortalaması; SIRA; ÜST10 = SIRA >= 0,90; ALT10 = SIRA <= 0,10 (UC_IZ.uc_ust_alt).
- Taban: formül UC_IZ.uc_taban (olay başına (N - tavan(0,9 N) + 1) / (N + 1)) VE plasebo UC_IZ.uc_plasebo AYNEN (UC_ESIK: 200 tohum, kök 25112026; her olay yerine aynı gün aynı kovadan rastgele üye, E1 hariç; üyenin SIRA'sı c2_es ile).
- Hücre: uc2_hucre = UC_IZ.uc_hucre ile aynı hesap (C2.c2_hucre yön + + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç); tek fark güç eğrisi parametre (test_uc_iz2: H 15'te uc_hucre ile birebir). Güç: R15 / R30 cetvel2_guc_v2.2.json ABD x hücre (delta +0,02); R60: json'da H 60 yok -> aynı yöntemle (C2.c2_hazirlik22: DS ANA olayları c2_ds_olay_acik_v2.2, c2_olay tekil 60, c2_es, c2_guc_egri) bu panelde hazırlıkta hesaplandı (HAZIRLIK_SHA içinde 'guc60'). c2 hükmü TUTAR olan karar grubu (R=1, B=1, I=1, N>=2) x karar hücresi x karar ufku için C2.c2_plasebo bilgi olarak koşulur.
- Hücreler (KARAR): ABD d1619 (giriş 2016-01-01..2019-12-31), ABD d2022 (2020-01-01..2022-12-31). 'dis' (2015 Q4 girişleri) bilgi. AVRUPA: SEC verisi yok -> 'AVRUPA VERİSİ YOK', karar en fazla ABD-ADAY. BIST yok.

## 4. Karar kuralı (aynen; sonuçtan sonra değişmez)

Her ufuk (R60, R15) ayrı: YÖN TUTARLI(iz) <=> iki karar hücresinin (ABD d1619, ABD d2022) ikisinde de FARK(iz var) > 0 VE FARK(var) - FARK(yok) > 0 VE (ÜST10 - taban_formül) > 0 VE (ÜST10 - taban_plasebo) > 0. TUTAR <=> ayrıca iki hücrede c2 hükmü (C2.c2_hucre + MU.mu_sira_boot + MU.mu_hukum, plasebo hariç) TUTAR. Aksi: iki hücrede de iz-var n >= 30 ve güç >= 0,80 ise TUTMADI, değilse ÖLÇÜLEMEDİ. BİRLİKTE ARTIYOR <=> iki hücrede FARK(N=0) < FARK(N=1) < FARK(N>=2) VE N>=2 FARK boot alt > 0 en az bir hücrede, ötekinde FARK > 0. KASA ADAYI (yalnız öneri; kasa açılmaz) <=> aynı ufukta en az iki iz YÖN TUTARLI VE BİRLİKTE ARTIYOR. BH q 0,10, aile = (R, B, İ, N>=2) x (R60, R15) = 8; p = iki hücrenin en büyük permütasyon p'si (n < 30 hücre p = 1). AVRUPA: SEC verisi yok -> 'AVRUPA VERİSİ YOK', karar en fazla ABD-ADAY. Evren bugün yaşayanlar (K7): sonuç yukarı yanlı.

Açık veriye bakış: bu iş açık veriye bir kez bakar (kos). Komisyon / kayma yok.

## 5. Getirisiz sayımlar ve güç beklentisi (eşli olay; R_H ölçülebilir ve >= 5 eş)

E1 huni: 8-K 2.02 satırı (bütün yıllar, 8-K + 8-K/A) 188.048 -> form 8-K madde 2.02 186.496 -> sembolsüz CIK satırı 3.811 -> takvim dışı (kabul 2022-12-30 sonrası) 54.242 -> 20 gün tekrar atılan 28.509 -> aralık dışı (2015-10..2022-12 dışı) 50.225 -> t'de geçersiz bar 1439 -> E1 73.329 (3.205 CIK) -> P2 54.154 -> B hesaplanabilen ve P2: analiz 53.734 (B hesaplanamayan P2 olayı 420).
- C2 huni R15: girdi 53.734, havuz dışı 0, giriş yok 0, giriş geç 0, sinyal bar geçersiz 0, sembol yok 0, tekil 0, R_H ölçülen 53.670, kova yok 0.
- C2 huni R60: girdi 53.734, havuz dışı 0, giriş yok 0, giriş geç 0, sinyal bar geçersiz 0, sembol yok 0, tekil 0, R_H ölçülen 51.550, kova yok 0.
- C2 huni R30: girdi 53.734, havuz dışı 0, giriş yok 0, giriş geç 0, sinyal bar geçersiz 0, sembol yok 0, tekil 0, R_H ölçülen 53.507, kova yok 0.

| grup | R15 d1619 n | güç | R15 d2022 n | güç | R60 d1619 n | güç | R60 d2022 n | güç |
|---|---|---|---|---|---|---|---|---|
| HEPSI | 26.245 | 1,00 | 25.954 | 1,00 | 26.245 | 1,00 | 23.836 | 1,00 |
| R=1 | 973 | 1,00 | 2.088 | 1,00 | 973 | 0,86 | 1.994 | 0,89 |
| R=0 | 25.272 | 1,00 | 23.866 | 1,00 | 25.272 | 1,00 | 21.842 | 1,00 |
| B=1 | 8.331 | 1,00 | 6.142 | 1,00 | 8.331 | 1,00 | 5.573 | 1,00 |
| B=0 | 17.914 | 1,00 | 19.812 | 1,00 | 17.914 | 1,00 | 18.263 | 1,00 |
| I=1 | 4.173 | 1,00 | 4.350 | 1,00 | 4.173 | 1,00 | 4.033 | 1,00 |
| I=0 | 22.072 | 1,00 | 21.604 | 1,00 | 22.072 | 1,00 | 19.803 | 1,00 |
| Bm=1 | 7.309 | 1,00 | 5.866 | 1,00 | 7.309 | 1,00 | 5.311 | 1,00 |
| N=0 | 14.481 | 1,00 | 15.092 | 1,00 | 14.481 | 1,00 | 13.805 | 1,00 |
| N=1 | 10.088 | 1,00 | 9.210 | 1,00 | 10.088 | 1,00 | 8.524 | 1,00 |
| N=2 | 1.639 | 1,00 | 1.586 | 1,00 | 1.639 | 0,98 | 1.445 | 0,77 |
| N=3 | 37 | 0,17 | 66 | 0,21 | 37 | 0,08 | 62 | 0,07 |
| N>=2 | 1.676 | 1,00 | 1.652 | 1,00 | 1.676 | 0,98 | 1.507 | 0,78 |
| R∧B | 327 | 0,89 | 515 | 0,94 | 327 | 0,40 | 485 | 0,32 |
| R∧I | 131 | 0,50 | 297 | 0,74 | 131 | 0,18 | 280 | 0,20 |
| B∧I | 1.292 | 1,00 | 972 | 1,00 | 1.292 | 0,94 | 866 | 0,53 |

Örtüşme (phi, eşli olaylar): R15 R_B_phi -0,001, R_I_phi -0,014, B_I_phi -0,012; R60 R_B_phi -0,002, R_I_phi -0,015, B_I_phi -0,015.
R30 (bilgi) eşli: 53.464. R60 güç eğrisi (DS ANA, H 60): d1619 N 1778 a -1,375 b -0,530, d2022 N 3316 a -0,952 b -0,543, acik N 5094 a -1,169 b -0,509.
E2 (bilgi) eşli KT02 dip olayı: R15 d1619 HEPSİ 507 (R 11, B 16, İ 116, N>=2 3), d2022 HEPSİ 659 (R 21, B 15, İ 127, N>=2 9); R60 d1619 HEPSİ 507 (R 11, B 16, İ 116, N>=2 3), d2022 HEPSİ 595 (R 19, B 14, İ 120, N>=2 9).

Güç beklentisi: iz-var grupları içinde n < 30 olan: yok. Güç < 0,80 olan: R60 N>=2 d2022 (0,78). Bu gruplarda 'beklenen ÖLÇÜLEMEDİ' (tanım değiştirilmez; ölçüm yine koşulur).

## 6. Doğrulamalar (getirisiz; ölçümden önce)

- D2 (K2) PREFIX: açık kopya 2019-06-28'de kesilip diske yazıldı, olaylar ve bayraklar (E2 hariç) baştan; t <= 2019-05-29 olaylarında tam 33367 / kesik 33367, yalnız tam 0, yalnız kesik 0, bayrak farkı {'R': 0, 'B': 2, 'I': 0, 'p2': 0, 'Bm': 3, 'bval_1e9': 342}; panel farkı {'kv_hucre': 157, 'lq_hucre': 161, 'ok_hucre': 80, 'yalniz_tam_havuz_hucre': 0, 'fark_gun': 72, 'gun': 1862}; KATI TUTMADI, ayrıştırmalı (S7) TUTTU. Kodda mekanik: İ son D <= t, kabul D0 <= t, B girdileri t satırında (RET t, ATRP t-1, KV t), A1 / fiyat <= 2022-12-31 (uc_kes / kasa_kapisi).
- D3 (K10): 10 rastgele A1 bildirimi ham zip'ten yeniden okundu (SUBMISSION FILING_DATE / DOCUMENT_TYPE / ISSUERCIK + NONDERIV_TRANS P / A adet x fiyat toplamı): 10 / 10 birebir. Örnek: CSBB 2019-02-06 32812 $ (ham 32812, 4); BOCH 2018-10-24 230800 $ (ham 230800, 4); AIMC 2018-11-06 157200 $ (ham 157200, 4). 10 rastgele E1 olayının ham satırı (erişim no, kabul UTC -> NY, D0, t) uc_iz2_hazirlik.json 'D3.E1'de; elle okundu.
- V3 EDGAR sağlaması (5 / 5) ve V2 k30 sağlaması (2.119 / 2.119) bölüm 1'de.

## 7. SAPMA / yorum (ölçümden önce yazıldı)

- S1 veri başlangıcı: ölçüm kopyası 2012-01-03'te başlar (bellek; TEZGAH2 2000'den). En uzun girdi penceresi D9 500 bar; 2016 öncesi >= 4 yıl ısınma. TEZGAH2_DOGRULAMA 21 sınaması 2000'den başlayan kopyada (acik_tam) koşuldu.
- S2 T2 21 sınaması 'hepsi geçmeli' yorumu: orijinal koşuda P2 de 20 / 21 idi (A1 2001-07 KISMEN, r 0,90); seçim kuralı P1'i 21 / 21 ile seçmişti ve KART_TUR2 / Ç225 P2'yi kullandı. Bu koşuda P1 21 / 21 ve P2 aynı tek satırda KISMEN (r 0,897): orijinalle birebir aynı hüküm tablosu -> GEÇTİ sayıldı.
- S3 R60 güç eğrisi: cetvel2_guc_v2.2.json'da H 60 yok; aynı yöntemle bu panelde hesaplandı (sayılar HAZIRLIK_SHA içinde).
- S4 k55/sec_ozet.json kabul saati içermediği için data.sec.gov submissions indirildi (iş tanımı V3'ün öngördüğü yol).
- S5 E1 tekili: CETVEL2 varsayılan H tekili yerine iş tanımının 'bir bilanço = bir olay' kuralı (tekil 1 + 20 gün tekrar). R60'ta ardışık çeyrek olaylarının pencereleri az sayıda örtüşebilir; boot ve permütasyon ay kümeli.
- S7 D2 prefix geçme ölçütü: KATI karşılaştırma TUTMADI (B 2, Bm 3, BVAL 342 / 33367 olay); neden bulundu: CETVEL2 taban paneli (DS.ds_veri -> OC.oc_veri) min_bar 80 süzgecini BÜTÜN seriye uygular; kesik veride 80 barı dolmamış genç hisseler panelden düşer ve kesitsel likidite / havuz (OC H, ok) 72 günde değişir (KV 157, LQ 161, ok 80 hücre; ATRP / F15 farkı 0). B / BVAL farklarının 342'i bu günlerde, 0'ı dışında; B değişim payı %0.0060. Getiri görülmeden ayrıştırmalı ölçüt yazıldı (küme / R / İ / P2 birebir VE bütün B farkı panel günlerinde VE B değişimi <= %0,1) -> GEÇTİ. Aynı özellik CETVEL2 konum eşinde de vardır (Ç225 dahil bütün CETVEL2 ölçümleri); HATA olarak raporda.
- S8 20 gün tekrar kuralı sayımı: huni sayısı (28.509) bütün yılları (2015-10 öncesi dosyalar dahil) kapsar; 2015-10..2022-12 penceresinde 8-K 2.02 satırı 78.678, tekrar nedeniyle atılan 3.459 (%4,4).
- S6 c2_plasebo (bilgi) yalnız karar grupları x karar hücreleri x karar ufuklarında TUTAR hücrede (UC_IZ'de bütün TUTAR hücreler); karar kuralında kullanılmaz (c2 hükmü plasebo hariç; ÜST10 - taban_plasebo uc_plasebo ile).

## 8. KONTROL LİSTESİ

| Kod | Madde | Yanıt | Kanıt (dosya / fonksiyon / sayı) |
|---|---|---|---|
| K1 | kontrol grubu | EVET | eş = CETVEL2 v2.2 konum eşi (aynı giriş günü, aynı kova ATRP x likidite x F15, >= 5 eş; o gün E1 olayı olan bütün CIK sınıf sembolleri dışlanır; aynı R_H geometrisi, stop yok); iz var / yok ve N = 0 aynı E1 kümesinden; B eşi aynı gün aynı kova (t satırı); taban formül + plasebo (UC_IZ.uc_plasebo, 200 tohum aynı gün aynı kova rastgele üye) |
| K2 | geleceğe bakma | EVET | kabul UTC -> NY, 16:00 sınırı, t >= D0 (assert); İ FILING_DATE <= t (assert); B: RET t, ATRP20 t-1, KV t (t-1 bilgisi); R: D9 t kapanışı; P2 / havuz giriş günü d'de d-1 bilgisi; fiyat / A1 <= 2022-12-31 (uc_kes, kasa_kapisi); D2 prefix 2019-06-28: küme 33367 / 33367, R / İ / P2 farkı 0, B farkı 2 (hepsi CETVEL2 panel min_bar günlerinde; S7); sembol -> CIK bugünkü company_tickers (CIK kalıcı kimlik; ticker değişimi etkilemez) |
| K3 | geçerli bar | EVET | OC.oc_veri_hazirla (H > L, V > 0, O/H/L/C > 0) temiz bar; olay günü t'de geçerli bar değilse olay düşer (1439); RET / ATRP yalnız geçerli barlarda; R_H CETVEL2 geçerli bar sayımı |
| K4 | tekilleştirme | EVET | bir bilanço = bir olay; aynı CIK'de <= 20 takvim günü içindeki ikinci 2.02 atıldı (28.509); çok sınıflı CIK'de tek sembol (42 CIK); c2_olay tekil 1; medyan FARK raporda; Form 4 erişim no tekil (fi_k30_alimlar) |
| K5 | giriş fiyatı | EVET | giriş = t'den sonraki ilk geçerli bar AÇILIŞI (OC.oc_olay_hazirla d; C2 R_H paydası); 16:00 sonrası kabulde t zaten ertesi gün; eşler aynı gün açılışı |
| K6 | veri birimi | EVET | TEZGAH2 V_ABD2 yfinance auto_adjust tek kip (bölünme + temettü düzeltmeli); R_H / EAR / ATRP oran (birimsiz); Form 4 değeri adet x fiyat USD (fi_k30_alimlar); T2 21 sınaması orijinalle aynı |
| K7 | hayatta kalma | EVET | evren bugün işlem gören 4450 ABD hissesi (TEZGAH2; batanlar yok); sonuç yukarı yanlı okunur, raporda yazılı |
| K8 | örneklem ve dönem | EVET | iki dönem (2016-19 / 2020-22) aynı yön şartı; n < 30 ya da güç < 0,80 hücre ÖLÇÜLEMEDİ; BH q 0,10 aile 8 (R, B, İ, N>=2 x R60, R15); getirisiz sayım ve güç bölüm 5; küçük örneklemden bulgu denmez |
| K9 | ön kayıt | EVET | tanım + eşik (UC2_ESIK sha) + kod sha + hazırlık sha + sayımlar ön kayıtta; kod commit cef0b7d -> ön kayıt commit -> kos; uc2_kapi (ik_kontrol_kapisi + sha + git) ölçümü kilitler; ikinci koşu durur |
| K10 | ayrıştırma | EVET | D3: 10 rastgele A1 ham zip'ten yeniden 10 / 10; V2: 2022 k30_alim.pkl ile 2.119 / 2.119 + 5 satır alan alan; V3: 5 rastgele 8-K 2.02 EDGAR sayfasıyla (WebFetch) tarih / NY saati / madde 5 / 5; 10 E1 ham satırı hazırlık json'da elle okundu |
| K11 | yeniden üretim | EVET | raporda: en az 2 hücre (ör. B=1 R60 d1619, İ=1 R15 d2022) satır dosyasından bağımsız düz pandas ile; 20 olayın R15 / R60'ı ham fiyattan düz döngüyle |
| K12 | ifade | EVET | fiyat değişimi (R_H) ile kâr / zarar ayrı; 'iz' sözü yalnız karar kuralı geçerse; sayı ile yorum ayrı cümlede; ÖLÇÜLEMEDİ 'iz değil' diye yazılmaz |
| K13 | süreç | EVET | çakışma kapısı (_cakisma_kontrol_uc2; testte sınandı); defter dosyaları (IZ_DEFTERI, IZ_KARNE, CLAUDE.md, COL_OZET, ONERI_DEFTERI, kural defteri) değişmedi; SEC User-Agent yalnız /root/.sec_ua (içerik yazılmadı; git grep @gmail / @hotmail boş); ham SEC repo dışı (/root/.kasa/ham/sec2016) |
| K14 | boyut (gerçek para) | UYGULANMAZ | öneri / gerçek para işi değil; alım-satım önerisi yok; keşif ölçümü |
