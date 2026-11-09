# K57 canlı tarama: BIST'te 3Ç26 sonuçlarına göre "YEOTK profili" (durum 9 Kasım 2026, kapanış sonrası)

Kaynak türleri: [R] KAP, [R*] KAP verisi bir toplayıcı üzerinden (fon.org.tr XBRL API, borsacoo KAP özetleri), [Ş] şirket, [İ] ikincil (Yahoo fiyat, İş Yatırım sermaye tablosu, haber siteleri), [T] kendi hesabım.
Ham veri ve kod (scratchpad, repoda değil): /tmp/claude-0/-home-user-col-yolu/2d897341-a66f-57df-ba5e-2bfd9dd60c3c/scratchpad/k57/ (raw2/api_bil.json, bil/*.json, hisse/*.json, yahoo_1y.json, sermaye.json, web/bc_*.html, kod/*.py, tara2.pkl, tepki.pkl).

Yöntem özeti [T]:
- Evren: fon.org.tr `/api/bilancolar` içindeki tüm 2026/9 (3Ç26) raporları. Bankalar (taksonomi "banks") çıkarıldı. Kalan 362 şirketin hepsi tarandı.
- 9A26 hasılat, 3Ç tek başına hasılat (`revenueQ` = KAP XBRL 3 aylık sütun), 9A ve 3Ç net kâr, net borç, FAVÖK (yaklaşık), özkaynak ve 3Ç25 karşılaştırma sütunu: [R*] fon.org.tr API (`/api/bilancolar`, `/api/bilanco/{KOD}`).
- **Hızlanma oranı (hız)** = 3Ç26 hasılatı / ((9A26 − 3Ç26) / 2). Yani 3Ç, aynı rapordaki H1'in çeyrek ortalamasına bölünür. İkisi de aynı satın alma gücündedir: TMS 29 yeniden düzenlemesi (Eylül 2026 TL'si). İkinci kontrol olan "hız(temel)", 3Ç'yi temel_duz.csv'deki nominal 1Ç ve 2Ç ortalamasına böler. TL raporlayanlarda hız(temel) ~%5-10 yüksek çıkıyor. USD fonksiyonel para birimli THYAO ve TAVHL'de iki oran eşit (1,35/1,35 ve 1,45/1,45). Buradan 2026 tablolarının hâlâ enflasyona göre düzeltildiği çıkıyor. Bu nedenle 9A yıllık büyüme rakamları **reel büyümedir** [T, çıkarım].
- Net kâr hızlanması: 3Ç26 net kâr ile H1 (9A − 3Ç, aynı rapordan) karşılaştırıldı.
- Seyreltme: İş Yatırım "Sermaye Artırımları" verisi (`CompanyInfoAjax.aspx/GetSermayeArttirimlari`, tamamlanan ve planlanan) [İ]. Bunun yanında borsacoo'daki son 25 KAP bildirimi tarandı [R*].
- Fon payı: K25 `fon_pay_ay.csv`, ay=24320 (Eylül 2026 portföyleri). Pay %, yani fon nominali / sermaye [T]. Karşılaştırma için fon.org.tr `fundOwnPct` de alındı (31 Ekim'e kadar).
- Fiyat: Yahoo v8 chart, 1 yıllık günlük veri, 9 Kasım 2026 kapanışı dahil [İ]. Yahoo `regularMarketTime` 15:08 UTC, yani 18:08 TR; değer kesin kapanış.
- Tepki günü, borsacoo'daki KAP saatine göre seçildi [R*]. Rapor 18:00'den önce bir işlem gününde geldiyse o gün, sonra geldiyse bir sonraki işlem günü. Bu kural MEGMT (6 Kas 07:57), SASA, THYAO (4 Kas 08:01), ZERGY ve 9 Kas sabah açıklayanlar (KZBGY, SNGYO, ULUSE) için aynı günü verir.

## 1. 9 Kasım 2026 itibarıyla kaç şirket 3Ç26 açıkladı ve kaçı YEOTK'un kriter 2–3'ünü geçiyor?

### Takeaway
Kontrol anında 378 şirketin 3Ç26 raporu vardı (362 banka dışı, 16 banka). Bunların hepsi tarandı. "9A hasılat ≥ +%20 (reel), hız ≥ 1,3 ve 3Ç net kâr > H1 net kâr" üç şartını birden geçen yalnız 12 şirket var. YEOTK bunlardan biri. Kalan 11'in 3'ü 100 milyar TL üstü dev şirket, 2'si nakit seyreltmeli, 3'ü GYO, 1'i (BRSAN) zirveden düşmemiş. İşletme şirketi olarak yalnız **PNLSN** ve **FORTE** kalıyor.

### Cited Findings
- fon.org.tr API `asOf=2026-11-09`: 1.112 rapor, 624 şirket. 2026/3. çeyrek dönemine ait satır sayısı 378 (yayın tarihleri 20 Ekim – 9 Kasım). Bunların 362'si genel taksonomide, 16'sı banka. 233 şirketin son raporu hâlâ 2026/6 [R*] — [fon.org.tr API](https://fon.org.tr/api/bilancolar)
- Yayın günlerine göre dağılım: 30 Ekim'de 104, 6 Kasım'da 80, 27 Ekim'de 58, 5 Kasım'da 30, 4 Kasım'da 23. 9 Kasım'da API'ye o ana kadar yalnız 4 rapor girmişti [R*] — [fon.org.tr API](https://fon.org.tr/api/bilancolar). Bir arama özeti konsolide 3Ç tabloları için son günün 9 Kasım 2026 olduğunu söylüyor, ama bunu birincil kaynakta doğrulayamadım [İ, doğrulanmadı]. 9 Kasım akşamı gelen raporlar sayıma girmedi.
- 26–30 Ekim haftasında 103 şirket 3Ç sonucunu açıkladı [İ] — [cnbce](https://www.cnbce.com/sirket-bilancolari/borsada-103-sirket-bilancosunu-acikladi-bir-sirketin-kari-150-katina-cikti-g40715)
- 362 banka dışı şirkette [T]: 9A hasılatı ≥ +%20 olan 71 şirket, hız ≥ 1,3 olan 58, 3Ç net kârı pozitif ve H1'den büyük olan 82. Üç şart birlikte 12 şirket: BRSAN, CONSE, CVKMD, FORTE, ISGYO, KZBGY, PNLSN, SNGYO, TAVHL, THYAO, TUPRS, YEOTK.
- 362 şirketin 312'si temel_duz.csv'de 1Ç ve 2Ç verisiyle eşleşti [T]. Eşleşmeyen 50 şirket (ör. ECOGR, ZERGY, EKDMR, BLUME) yalnız aynı rapordan hesaplanan hızla değerlendirildi.
- Piyasa bağlamı [İ/T]: XU100 9 Kasım'da 11.712,7 puanda kapandı. 52 haftalık zirvesi 15.133,5 (11 Mayıs 2026); zirveye göre −%22,6, 90 günde −%14,5 — [Yahoo XU100.IS](https://query1.finance.yahoo.com/v8/finance/chart/XU100.IS?range=1y&interval=1d). Fiyatı çekilen 219 aday hissenin %88'i rapor öncesinde 52 hafta zirvesinin ≥%30 altındaydı, %66'sı ≥%50 altındaydı [T]. Bu yüzden kriter 6 (sert düşüş) bu ortamda neredeyse herkeste var ve ayırt edici değil.

### Inferences
- Asıl seçici kriter 3 (hızlanma) ile kriter 4–5'in (seyreltme ve fon lekesi) birleşimi. Kriter 6 kriz sonrası piyasada genel durum.
- 9A yıllık büyüme TMS 29 ile reel olduğu için YEOTK'un %31'i enflasyonun "üstünde" değil, enflasyondan arındırılmış %31'dir. Görev tanımındaki "enflasyonun çok üstünde" ifadesi bu anlamda zaten sağlanıyor [T, çıkarım].
- 3Ç tek başına hasılatta mevsimsellik var: otel (TEKTU, PKENT), GES ve inşaatta 3Ç doğal olarak yüksek. Bu yüzden 3Ç26/3Ç25 yıllık oranı da tabloya eklendi. YEOTK'ta bu oran yalnız +%18. Hızlanmanın bir kısmı 2025'te de görülen 3Ç mevsimselliğidir [R*/T].

### Gaps
- 9 Kasım akşamı (son gün) gelen raporlar dahil değil. Son sayı muhtemelen 378'in belirgin üstünde olacak; kesin sayı bulunamadı.
- KAP'a doğrudan erişilemedi (403). Bütün tablo rakamları XBRL toplayıcısından [R*]. Rastgele örnekte (YEOTK) API rakamları görev tanımındaki 9A +%31 ile tutuyor.

## 2. Sıralı aday tablosu (kriter 2–6) ve tek satır hüküm

### Takeaway
Profile en yakın iki işletme şirketi PNLSN ve FORTE. Kriter 2–6'nın hepsini geçiyorlar ve ertesi gün tavan oldular. PNLSN'de isimli büyük sözleşme yok. FORTE'de fon payı YEOTK'un yaklaşık 6 katı. ECOGR, PENTA, KBORU, ULUSE ve SMRTG birer kriterden kaçırıyor. GYO'lar (KZBGY, SNGYO, ISGYO, VKGYO) teslim muhasebesi nedeniyle "hızlanma"yı tekrar etmeyebilir.

### Cited Findings (tablo; sayılar [R*] fon.org.tr XBRL API, fiyatlar [İ] Yahoo, oranlar [T])
Sütunlar:
- 9A hasılat: milyar TL.
- y/y: 9A26 / 9A25 (aynı rapordaki düzeltilmiş karşılaştırma).
- 3Ç: 3Ç26 tek başına hasılat, milyar TL.
- 3Ç y/y: 3Ç26 / 3Ç25 tek çeyrek.
- hız: 3Ç / H1 çeyrek ortalaması (aynı rapor).
- hız(temel): 3Ç / temel_duz.csv'deki 1Ç-2Ç ortalaması.
- NK 3Ç/H1: konsolide net kâr, milyon TL.
- Ana ort. 3Ç/H1: ana ortaklık payı, milyon TL.
- NB/FAVÖK: 9A yaklaşık FAVÖK ile (yıllıklaştırılmamış).
- NB/Öz: net borç / özkaynak.
- PD: piyasa değeri, milyar TL, 6 Kasım fiyatıyla (fon.org.tr [İ]).
- K25 fon%: Eylül 2026.
- Zirve(ön) ve 90g(ön): rapor öncesi son kapanışın 52 hafta zirvesine uzaklığı ve 90 günlük getirisi.
- Tepki: ilk tepki günü kapanış değişimi; parantez içinde aynı gün XU100.
- Bugün: 9 Kasım kapanışının zirveye uzaklığı / rapordan bu yana getiri.

| Kod | Yayın | 9A hasılat | y/y | 3Ç | 3Ç y/y | hız | hız(temel) | NK 3Ç / H1 | Ana ort. 3Ç / H1 | NB/FAVÖK | NB/Öz | PD | K25 fon% | Zirve(ön) | 90g(ön) | Tepki | Bugün zirve / rapordan |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| YEOTK (referans) | 2026-11-05 | 17.50 | 31% | 8.73 | 18% | 1.99 | 2.10 | 1,184 / 867 | 827 / 707 | 1.4 | 0.76 | 21.3 | 0.39 | -56% | -41% | 2026-11-06 9.9% (XU 1.3%) | -47% / 21% |
| 1 PNLSN | 2026-11-06 | 3.26 | 23% | 1.30 | 31% | 1.32 | 1.40 | 127 / 19 | 127 / 19 | 0.6 | 0.07 | 2.1 | 0.12 | -51% | -41% | 2026-11-09 10.0% (XU 2.0%) | -46% / 10% |
| 2 FORTE | 2026-11-06 | 4.82 | 234% | 2.61 | 267% | 2.37 | 2.50 | 336 / 226 | 337 / 225 | 1.8 | 0.53 | 5.4 | 2.23 | -45% | -29% | 2026-11-09 10.0% (XU 2.0%) | -40% / 10% |
| 3 ECOGR | 2026-11-07 | 7.00 | 19% | 3.41 | 180% | 1.90 | — | 717 / 141 | 717 / 141 | 5.6 | 0.46 | 10.1 | bulunamadı (fon.org.tr %0,03) | -59% | -45% | 2026-11-09 9.9% (XU 2.0%) | -55% / 10% |
| 4 PENTA | 2026-11-03 | 28.14 | 26% | 10.84 | 31% | 1.25 | 1.25 | 110 / 44 | 110 / 44 | 1.3 | 0.28 | 3.5 | 1.82 | -52% | -39% | 2026-11-04 9.9% (XU 4.1%) | -47% / 11% |
| 5 KBORU | 2026-10-30 | 7.43 | 54% | 2.80 | 93% | 1.21 | 1.28 | 229 / 274 | 229 / 274 | 2.6 | 0.84 | 6.5 | 0.20 | -72% | -67% | 2026-11-02 9.9% (XU 1.9%) | -61% / 37% |
| 6 ULUSE | 2026-11-09 | 10.65 | 92% | 3.76 | 70% | 1.09 | 1.15 | 514 / 857 | 514 / 857 | 4.1 | 1.04 | 11.1 | bulunamadı | -62% | -54% | 2026-11-09 9.9% (XU 2.0%) | -58% / 10% |
| 7 SMRTG | 2026-11-07 | 11.55 | 20% | 4.35 | 18% | 1.21 | 1.27 | 37 / 100 | 37 / 115 | 5.6 | 1.67 | 7.4 | 0.11 | -70% | -62% | 2026-11-09 9.9% (XU 2.0%) | -67% / 10% |
| 8 KZBGY | 2026-11-09 | 3.68 | 130% | 2.50 | 894% | 4.23 | 4.96 | 628 / -86 | 638 / -85 | 2.5 | 0.20 | 4.6 | 0.03 | -75% | -42% | 2026-11-09 7.8% (XU 2.0%) | -73% / 8% |
| 9 SNGYO | 2026-11-09 | 10.34 | 140% | 5.51 | 548% | 2.28 | 3.18 | 1,343 / 86 | 1,131 / 117 | 2.5 | 0.13 | 10.0 | 0.87 | -54% | -21% | 2026-11-09 9.6% (XU 2.0%) | -50% / 10% |
| 10 MEGMT | 2026-11-06 | 27.96 | 66% | 10.26 | 71% | 1.16 | 1.16 | 289 / 605 | 289 / 605 | 3.8 | 1.09 | 9.3 | 0.62 | -67% | -54% | 2026-11-06 9.9% (XU 1.3%) | -63% / 11% |
| 11 TCKRC | 2026-10-27 | 6.07 | 184% | 2.38 | 233% | 1.29 | 1.36 | 756 / 1,199 | 756 / 1,199 | 0.4 | 0.10 | 21.1 | 0.15 | -40% | -24% | 2026-10-28 6.3% (XU 0.1%) | -29% / 17% |
| 12 BMSTL | 2026-10-30 | 2.42 | 33% | 0.91 | 45% | 1.21 | 1.21 | 15 / -11 | 15 / -11 | 2.5 | 0.25 | 11.3 | 0.00 | -53% | -28% | 2026-11-02 -7.6% (XU 1.9%) | -42% / 23% |
| 13 ISGYO | 2026-10-27 | 4.71 | 55% | 2.93 | 291% | 3.29 | 3.47 | 654 / -939 | 654 / -939 | net nakit | -0.01 | 18.5 | 1.37 | -39% | -30% | 2026-10-28 -0.5% (XU 0.1%) | -33% / 9% |
| 14 VKGYO | 2026-10-30 | 3.67 | 63% | 2.44 | 251% | 3.97 | 4.19 | 312 / 360 | 312 / 360 | 0.6 | 0.04 | 6.6 | 0.04 | -45% | -29% | 2026-11-02 2.2% (XU 1.9%) | -38% / 14% |
| 15 KOPOL | 2026-10-30 | 5.18 | 28% | 2.12 | 55% | 1.39 | 1.39 | 204 / 440 | 204 / 440 | 3.8 | 0.43 | 3.8 | 0.01 | -68% | -54% | 2026-11-02 2.8% (XU 1.9%) | -60% / 25% |
| 16 INGRM | 2026-11-06 | 29.63 | 67% | 12.10 | 87% | 1.38 | 1.38 | 17 / 36 | 2 / 20 | 8.9 | 2.53 | 5.2 | 0.39 | -60% | -46% | 2026-11-09 2.9% (XU 2.0%) | -58% / 3% |
| 17 YUNSA | 2026-11-03 | 3.20 | 24% | 1.22 | 18% | 1.24 | 1.31 | 73 / 187 | 73 / 187 | net nakit | -0.07 | 3.0 | 0.39 | -52% | -38% | 2026-11-04 9.9% (XU 4.1%) | -44% / 17% |
| 18 FMIZP | 2026-10-27 | 0.68 | 39% | 0.25 | 38% | 1.16 | 1.16 | 53 / 97 | 53 / 97 | net nakit | -0.63 | 3.1 | bulunamadı | -50% | -34% | 2026-10-28 10.0% (XU 0.1%) | -40% / 20% |
| 19 BLUME | 2026-11-06 | 0.37 | 152% | 0.14 | 78% | 1.19 | — | 2 / -92 | 2 / -92 | 1.0 | 0.09 | 4.9 | 0.00 | -51% | -22% | 2026-11-09 8.3% (XU 2.0%) | -47% / 8% |

24 aylık seyreltme (İş Yatırım [İ], 9 Kas 2024 – 9 Kas 2026, planlananlar dahil) ve hüküm:
1. **PNLSN — profil TAMA YAKIN (2–7 tamam, 1 zayıf).**
   - Seyreltme: bedelli/tahsisli yok. Yalnız nakit temettü var (3 Eyl 2025 %17,6; 8 Tem 2026 %68,8).
   - 3Ç net kâr 127 mn TL, H1'in (19 mn TL) yaklaşık 6,6 katı. Net borç/FAVÖK 0,6.
   - Zayıf yanı: son KAP bildirimlerinde isimli büyük sözleşme yok, yalnız kendi Elazığ GES yatırımı [R*]. 9A işletme nakit akışı −243 mn TL [R*].
   - Fon krizi: 30 Eyl 2026 KAP açıklaması "tasfiye edilen fonlarla ilişki, risk ya da yükümlülük yok" [R*]. K25 fon payı Eylül %0,12, Mart %0,94 [T].
   - Kaynaklar: [borsacoo PNLSN](https://borsacoo.com/firma/PNLSN/bildirimler), [fon.org.tr](https://fon.org.tr/api/bilanco/PNLSN)
2. **FORTE — TAMA YAKIN, fon payı yüzünden kısmen.**
   - Seyreltme: bedelli/tahsisli yok. Yalnız Aralık 2024 nakit temettüsü var.
   - İsimli işler [R*]: yurt içi savunma şirketinden 621 bin $ donanım siparişi (26 Eki 2026); MEB ihalesi 49,1 mn TL (2 Eki); Milsoft'a 700 bin $ sipariş (28 Eyl); AFAD ihalesi 31,9 mn TL (23 Eyl).
   - Fon payı: K25 Eylül %2,23; fon.org.tr'de 31 Ekim'e kadar %2,77, YEOTK'un yaklaşık 6 katı. AK Portföy fonları 1 Eki'de payı %2,48'den %3,27'ye çıkardı [R*].
   - 9A net kâr yıllık −%76. Nedeni 3Ç25'teki 2,4 mlr TL'lik tek seferlik kâr; 2026 içinde hızlanma gerçek [R*/T].
   - Kaynaklar: [borsacoo FORTE](https://borsacoo.com/firma/FORTE/bildirimler), [fon.org.tr](https://fon.org.tr/api/bilanco/FORTE)
3. **ECOGR — kısmen.**
   - Seyreltme: 22 Eki 2025'te sermaye artırımlı halka arz (RHK %20,4), yani 24 ay içinde nakit girişi. Halka arz geliri kullanım raporu-3, 28 Ağu 2026.
   - 9A +%19 (eşiğin hemen altında). NB/FAVÖK 5,6 ile yüksek borçlu.
   - Artıları: 3Ç net kâr 717 mn TL, H1 141 mn TL. İsimli ihale sonuçları var: YEKA GES-2026 G26-Elazığ 40 MWe'de en iyi teklif (3 Kas); YEKA RES-2026 Kütahya'da olumlu teklif (2 Kas) [R*].
   - VBTS: açığa satış ve kredili işlem yasağı 25 Mar – 24 Nis 2026; 6 aylık pencerenin dışında [İ].
   - Kaynaklar: [borsacoo ECOGR](https://borsacoo.com/firma/ECOGR/bildirimler), [rotaborsa](https://rotaborsa.com/?p=428692)
4. **PENTA — kısmen.**
   - Seyreltme: 24 ayda sermaye kaydı yok.
   - Hız 1,25, eşik 1,3'ün altında. Dağıtıcı olduğu için brüt marj yalnız %7,3.
   - Tavan günü (4 Kas) XU100 de +%4,1 yükseldi; tavanın bir kısmı piyasadan.
   - İsimli dağıtım anlaşmaları var (Constructor Tech, Oki) [R*]. K25 fon payı %1,82.
   - Kaynak: [borsacoo PENTA](https://borsacoo.com/firma/PENTA/bildirimler)
5. **KBORU — kısmen.**
   - Seyreltme: bedelsiz %500 (Haz 2025), bedelli yok.
   - 3Ç net kâr (229) H1'in (274) altında, kriter 3b sağlanmıyor.
   - İsimli işler: DSİ Adatepe ihalesinde birinci, 408,9 mn TL + KDV; 155,9 mn TL boru satışı [R*].
   - Fon payı Haziran %1,74'ten Eylül %0,20'ye düştü [T]; fon çıkışı oldu.
   - Kaynak: [borsacoo KBORU](https://borsacoo.com/firma/KBORU/bildirimler)
6. **ULUSE — kısmen.**
   - Seyreltme: 24 ayda kayıt yok.
   - Hız 1,09, 3Ç net kâr H1'in altında; yani çeyrek bazında hızlanma yok. Buna karşın 3Ç yıllık +%70 ve 9A +%92.
   - Rapor 9 Kas sabah geldi, aynı gün tavan oldu. 2025 için kâr dağıtmayacak (2025'te 188 mn TL zarar) [R*].
7. **SMRTG — kısmen.**
   - Seyreltme: yalnız bedelsiz %200 (Oca 2026).
   - İsimli sözleşmeler [R*]: 23,4 mn $ anahtar teslim GES (21 Eki); Arçelik Pazarlama ile 19,5 mn $ (8 Eki); 14 mn $ GES (6 Eki).
   - Zayıf yanlar: 3Ç net kâr 37 mn TL, H1 115 mn TL. 9A işletme nakit akışı −2,4 mlr TL. Borç/öz 1,67.
   - Kaynak: [borsacoo SMRTG](https://borsacoo.com/firma/SMRTG/bildirimler)
8. **KZBGY — kısmen (GYO).**
   - Hasılat, devre mülk teslimlerinin muhasebeye alınmasından geliyor; tekrar edip etmeyeceği belirsiz. Toplam ön satış 33.136 adet, 11,96 mlr TL; Ekim satışı 160,8 mn TL [R*].
   - 2,68 mlr TL'lik idari para cezasının iptali şirket lehine kesinleşti (19–20 Eki) [R*].
   - Seyreltme: bedelsiz %300 (Oca 2025) ve %233 (Şub 2026). 9A işletme nakit akışı −122 mn TL.
9. **SNGYO — kısmen (GYO).**
   - Seyreltme: bedelsiz %166,7 (Ara 2024).
   - Fon payı Ocak %3,3'ten Eylül %0,87'ye düştü. İstanbul Portföy fonlarının oy hakkı 20 Eki'de %3'ün altına (%2,97) indi [R*].
10. **MEGMT — kısmen.**
    - Seyreltme: bedelsiz %860 (Eyl 2026).
    - 3Ç net kâr H1'in altında. Brüt marj %7. ABD (South Carolina) tesisinde ticari üretim başladı (27 Eki) [R*].
11. **TCKRC — kısmen.**
    - Seyreltme: 24 ayda kayıt yok. Pay geri alımı sürüyor.
    - 3Ç net kâr H1'in altında.
    - Fon payı Temmuz %3,29'dan Eylül %0,15'e düştü. MSB Askeri Fabrikalar onaylı tedarikçi oldu (2 Kas) [R*].
12. **BMSTL — kısmen.**
    - Seyreltme: bedelsiz %100 (Tem 2026).
    - İsimli siparişler: 1,73 mn $ ve 1,44 mn $ [R*].
    - Rapor ertesi gün −%7,6 tepki. Tutarlar küçük.
13. **ISGYO, VKGYO — kısmen/değil (GYO).**
    - ISGYO: H1 zararlı. K25 fon payı %1,37.
    - VKGYO: 3Ç net kâr H1'in altında; brüt marj 3Ç25'te %78'di, 3Ç26'da %27.
14. **KOPOL, INGRM, YUNSA, FMIZP, BLUME — değil.** Net kâr hızlanması yok ya da marj çok düşük:
    - INGRM: 3Ç net kâr marjı yaklaşık %0,1.
    - FMIZP: Nisan'da "azalan siparişler" nedeniyle İzmit üretimini durdurdu [R*].
    - BLUME: 2025 birleşmesi var.

### Inferences
- YEOTK'a en çok benzeyen iki ad PNLSN ve FORTE. İkisi de 6 Kas 18:1x'te açıkladı ve 9 Kasım'da tavan oldu. Tavanın bir kısmı piyasadan; XU100 o gün +%2,0.
- PNLSN küçük: piyasa değeri yaklaşık 2,1 mlr TL, likidite riski var.
- FORTE'de fon payı ve geçen yılın tek seferlik kârı yüzünden "temiz" sayılmaz.
- Aynı gün (9 Kas) tavan olan geniş bir grup var: PNLSN, FORTE, ECOGR, ULUSE, SMRTG, SNGYO. Bu, 9 Kasım'daki tavanların tek başına profil sinyali olmadığını gösteriyor [T].
- Kaynakların gösterdiği desen: kriz sonrası fon çıkışı (KBORU, TCKRC, YUNSA, SNGYO'da K25 payının sert düşüşü) ile güçlü 3Ç raporu üst üste geliyor. Bu, YEOTK hikâyesindeki "fon satışı bitti + hızlanan rapor" bileşimine benziyor. Ölçülmüş bir iz değil, yalnız gözlem.

### Gaps
- Kriter (1) "isimli sözleşme": yalnız borsacoo'daki son 25 bildirime bakıldı. Daha eski sözleşme akışı her aday için taranmadı.
- VBTS: 9 Kasım itibarıyla tam ve güncel tedbir listesi bulunamadı. Gedik ve GCM sayfaları JS ile yükleniyor. Son 6 ay için yalnız şu kanıtlar var:
  - CATES: 14 Eki'ye kadar açığa satış ve kredi yasağı.
  - ECOGR: Mart–Nisan, pencere dışında.
  - Ekim listelerinde BIGEN, ANELE, OZATD, ODINE, PASEU, SELEC var; bunlar zaten SPK listesinde.
  - Kaynaklar: [cnbce](https://www.cnbce.com/borsa/bu-hafta-7-hisse-uzerindeki-yasaklar-kalkacak-h39178), [Gedik](https://gedik.com/analiz/hisse-senetleri/tedbir-kapsamindaki-pay-senetleri)
  - PNLSN, FORTE, PENTA, KBORU, ULUSE ve SMRTG için VBTS kaydı bulunamadı; bu "yok" anlamına gelmez.
- Tasfiye fonu yoğunluğu: hisse bazında tasfiyedeki fonların payı ölçülemedi. fon.org.tr fon listelerinde adında "TASFİYE" geçen fon çıkmadı. YEOTK kendisi açıkladı: tasfiyedeki yalnız 1 fonda 27.001 lot, sermayenin %0,003'ü (22 Eyl 2026) [R*].
- NB/FAVÖK, 9A yaklaşık FAVÖK (faaliyet kârı + amortisman) ile hesaplandı, yıllıklaştırılmadı. Şirketlerin açıkladığı FAVÖK ile farklı olabilir.

## 3. YEOTK: 5 Kasım sonrası fiyat ve 6–9 Kasım KAP

### Takeaway
YEOTK raporu 5 Kasım 22:52'de açıkladı. Sonraki iki işlem gününün ikisinde de tavan oldu: 23,32 → 25,64 → 28,20 TL, toplam +%20,9. 6–9 Kasım arasında yeni şirket bildirimi bulunamadı.

### Cited Findings
- KAP zaman damgaları [R*]: 2026/9 bilanço 5 Kas 2026 22:52:05; konsolide faaliyet raporu 23:02:07. Ondan önceki bildirimler:
  - 2 Kas: 300 mn TL yeşil bononun 3. kuponu ödendi.
  - 23 Eki: 247 mn TL'lik bono vadesinden önce itfa edildi.
  - 20 Eki: Azerbaycan'daki 250 MWh batarya depolama projesi için Pasha Bank ile finansman anlaşması.
  - Kaynak: [borsacoo YEOTK](https://borsacoo.com/firma/YEOTK/bildirimler)
- Kapanışlar [İ]: 4 Kas 24,32; 5 Kas 23,32; 6 Kas 25,64 (+%9,95, tavan; XU100 +%1,3); 9 Kas 28,20 (+%10,0, tavan; XU100 +%2,0) — [Yahoo YEOTK.IS](https://query1.finance.yahoo.com/v8/finance/chart/YEOTK.IS?range=1y&interval=1d). 6 Kas kapanışı 25,64 / +%9,95 borsacoo ile aynı [R*].
- 6 Kas işlem hacmi, son 20 gün ortalamasının 0,48 katı [İ/T]. Tavanda alıcı kilitli kaldığı için hacim düşük.
- 52 hafta zirvesi 53,04 (3 Haz 2026). 9 Kas kapanışı zirvenin −%46,8 altında. Rapor öncesi 90 günlük getiri −%40,7 [T].
- 3Ç26 rakamları [R*]:
  - Hasılat 8,73 mlr TL; 3Ç25'e göre +%17,7.
  - Konsolide net kâr 1.184 mn TL; ana ortaklık payı 826,6 mn TL. H1 ana ortaklık payı 707 mn TL (9A 1.533,6 − 3Ç).
  - 9A işletme nakit akışı +3,31 mlr TL. Net borç 5,59 mlr TL (31 Ara 2025'te 6,48 mlr TL).
  - Kaynak: [fon.org.tr YEOTK](https://fon.org.tr/api/bilanco/YEOTK)
- 24 aylık seyreltme [İ]: yalnız bedelsiz (28 Kas 2024 %269,8; 31 Tem 2026 %133,8). Bedelli ve tahsisli yok — [İş Yatırım](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=YEOTK)

### Inferences
- Görev tanımındaki "Q3 net kâr ≈864 mn > H1 670 mn" büyük olasılıkla ana ortaklık payına dayanıyor. API'deki ana ortaklık 3Ç 826,6 / H1 707 mn TL. Fark, ana ortaklık payı ile TMS 29 düzeltmesinden kaynaklanıyor olabilir; ikisi de "3Ç > H1" sonucunu veriyor [T].

### Gaps
- KAP'a doğrudan erişilemedi. "6–9 Kas yeni bildirim yok" sonucu borsacoo listesine dayanıyor; liste 9 Kas ~18:25 TR'ye kadar güncel [R*].

## 4. Leke veya seyreltme nedeniyle elenenler

### Takeaway
Hızlanma şartlarını geçen ama elenen adaylar:
- **Nakit seyreltme:** CONSE (bekleyen %100 bedelli), CVKMD (%170 bedelli), ENTRA (%19 bedelli), ORCAY (%200 bedelli), SASA (2026'da tahsisli).
- **24 ay içinde sermaye artırımlı halka arz:** ECOGR, ZERGY, EMPAE, EKDMR, RUBNS. ECOGR yine de "kısmen" olarak tabloda tutuldu.
- **Fon payı yüksek:** FONET.
- **SPK listesi:** BIGEN.

### Cited Findings
- **CONSE**: hasılat 9A +%252, hız 10,6. Ancak:
  - Sermayeyi 771 mn TL'den 1,542 mlr TL'ye çıkaracak %100 bedelli artırım için SPK'ya başvurdu (27 Nis 2026). Güncellenmiş izahname 19 Ağu'da, SPK ile mutabık kalınan izahname 23 Eyl 2026'da Kurul'a sunuldu [R*].
  - İş Yatırım tablosunda bu artırım görünmüyor (planlanan) [İ].
  - Brüt marj 3Ç26'da %3,9 (3Ç25 %14,4). NB/FAVÖK 14,0.
  - Kaynak: [borsacoo CONSE](https://borsacoo.com/firma/CONSE/bildirimler)
- **CVKMD**: %170 bedelli sermaye artırımı, 5 Ağu 2026 [İ]. 3Ç net kâr 1.099 mn TL; yalnız bedelli nedeniyle elendi — [İş Yatırım](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse=CVKMD)
- **ENTRA**: bedelli %19 + bedelsiz %100 (1 Haz 2026). 9A hasılat −%22 [İ/R*].
- **ORCAY**: bedelli %200 (4 Kas 2025). 3Ç net kâr yalnız 2 mn TL [İ/R*].
- **SASA**: rüçhan kısıtlamalı (tahsisli) artırımlar: 25 May, 12 Haz, 9 Tem 2026 (%5,6, %1,7, %11,6). 3Ç net zarar 1.910 mn TL [İ/R*].
- Sermaye artırımlı halka arzlar [İ]: ZERGY (10 Ara 2025, %25,1), EMPAE (19 Şub 2026, %22,4), EKDMR (13 May 2026, %16,2), RUBNS (9 May 2025, %10), ECOGR (22 Eki 2025, %20,4).
- **FONET**: K25 fon payı Eylül %6,01 (Ocak %4,47'den yükseliyor). Taranan adaylar arasında en yüksek [T].
- **BIGEN**: SPK suç duyurusu listesinde; 3Ç tepkisi +%10. Zirveden −%97, bu yüzden aday değil [T/İ].
- Taranan adaylarda SPK listesindeki diğer adlar (KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS, PEKGY, TERA, HEDEF, HDFGS) hızlanma filtresine girmedi [T].

### Inferences
- "Hızlanma + düşmüş fiyat" filtresinin en büyük tuzağı bekleyen bedelli. CONSE en yüksek hızlanmaya sahip ama yakında %100 nakit seyreltme bekliyor. Bu tür adayları ancak "planlanan sermaye artırımı" taraması yakalar.

### Gaps
- Tahsisli artırımların hepsinin İş Yatırım tablosunda "Rüçhan Hakkı Kısıtlanarak" diye göründüğü doğrulanmadı. Bekleyen başvurular (CONSE gibi) yalnız KAP bildirimleriyle yakalanabiliyor. Bu kontrol yalnız tablodaki 19 aday ile elenenler için yapıldı.

## 5. Çok büyük olduğu için atlananlar (>100 mlr TL piyasa değeri)

### Takeaway
Üç hızlanma şartını geçen 4 dev şirket profil dışı bırakıldı: TUPRS, THYAO, TAVHL, ASELS. Hepsi zirveye yakın ve fon sahipliği yüksek. BRSAN 100 mlr TL sınırının hemen altında ama zirveden düşmemiş.

### Cited Findings ([R*] fon.org.tr, [İ] Yahoo, [T])
- **TUPRS**: piyasa değeri 650,3 mlr TL. 9A +%51; hız 1,36; 3Ç net kâr 69,0 mlr TL, H1 53,1 mlr TL. Rapor öncesi zirveye uzaklık −%20; tepki −%1,6.
- **THYAO**: 413,0 mlr TL. 9A +%42 (USD fonksiyonel); hız 1,35; 3Ç net kâr 61,5 mlr TL, H1 18,8 mlr TL. 4 Kas tavan, ama XU100 o gün +%4,1.
- **TAVHL**: 107,0 mlr TL. 9A +%28; hız 1,45; 3Ç net kâr 9,57 mlr TL, H1 0,87 mlr TL. Tepki −%7,0.
- **ASELS**: 1.512,8 mlr TL. Hız 1,24; 3Ç net kâr H1'in altında. Tepki +%5,2.
- **BRSAN**: 96,7 mlr TL (sınırın altında). 9A +%44; hız 1,40; 3Ç net kâr 2,12 mlr TL, H1 1,80 mlr TL. Zirveye uzaklık yalnız −%14; 90 günde +%19. Kriter 6 sağlanmıyor.

### Inferences
- Dev şirketlerdeki hızlanma, YEOTK tipi "unutulmuş küçük şirket" hikâyesi değil; bunlar zirveye yakın işlem görüyor.

### Gaps
- Piyasa değerleri fon.org.tr'nin 6 Kasım fiyatına dayanıyor [İ]. 9 Kasım fiyatıyla güncellenmedi; sınır üstü/altı sonucu değişmez.
